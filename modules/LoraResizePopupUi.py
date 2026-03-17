import json
from pathlib import Path
from PySide6 import QtWidgets
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton
import requests
from ui_files.LoraResizePopupUI import Ui_lora_resize_ui
from modules.BaseDialog import BaseDialog
from modules.DragDropLineEdit import DragDropLineEdit
from modules.ScrollOnSelect import ComboBox

# Threshold semantics: HIGHER (less negative) = more pruning (aggressive).
# score_i = log10(S_i / fro_norm_base); keep dim if score_i >= threshold.
# -3.0 => keep S > 0.1% of base norm  (mild, little reduction)
# -2.0 => keep S > 1% of base norm    (moderate reduction)
# -1.6990 => keep S > 2% of base norm   (heavy reduction)
RECIPE_PRESETS = [
    ("Conservative", "fro_ckpt=1,thr=-3.0"),
    ("Balanced", "fro_ckpt=1,thr=-2.0"),
    ("Aggressive", "fro_ckpt=1,thr=-1.6990"),
    ("Spectral Norm", "spn_ckpt=1,thr=-2.0"),
    ("Subspace-Aware", "fro_ckpt=0.5,subspace=0.5,thr=-2.0"),
    ("Custom", ""),
]


class LoraResizePopup(BaseDialog):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.widget = Ui_lora_resize_ui()
        self.args = {
            "save_precision": "bf16",
            "new_rank": 4,
            "device": "cuda",
            "dynamic_method": "sv_fro",
            "verbose": True,
        }
        self.setup_widget()
        self.setup_connections()
        # Sync initial state for checkboxes that start checked
        if self.widget.dynamic_param_enable.isChecked():
            self.enable_disable_dynamic(True)

    def setup_widget(self) -> None:
        self.widget.setupUi(self)
        self.widget.model_input.setMode("file", [".ckpt", ".safetensors"])
        self.widget.model_input.highlight = True
        self.widget.model_input_selector.setIcon(
            QIcon(str(Path("icons/more-horizontal.svg")))
        )
        self.widget.output_folder_input.setMode("folder")
        self.widget.output_folder_selector.setIcon(
            QIcon(str(Path("icons/more-horizontal.svg")))
        )

        self.widget.verbose_enable.setChecked(True)

        # ── Base Model Scoring section ──
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.widget.formLayout.addRow(separator)

        self.base_model_enable = QCheckBox(self)
        self.base_model_enable.setText("Base Model Scoring")
        self.base_model_enable.setToolTip(
            "Enable scoring-based resize using a base model checkpoint.\n"
            "Singular values are scored against base-model statistics\n"
            "for more effective rank selection. Disables standard resize controls."
        )
        base_model_layout = QHBoxLayout()
        self.base_model_input = DragDropLineEdit(self)
        self.base_model_input.setMode("file", [".safetensors"])
        self.base_model_input.setEnabled(False)
        self.base_model_input.setPlaceholderText(
            "Path to base model checkpoint (.safetensors)"
        )
        self.base_model_selector = QPushButton(self)
        self.base_model_selector.setIcon(
            QIcon(str(Path("icons/more-horizontal.svg")))
        )
        self.base_model_selector.setEnabled(False)
        base_model_layout.addWidget(self.base_model_input)
        base_model_layout.addWidget(self.base_model_selector)
        self.widget.formLayout.addRow(self.base_model_enable, base_model_layout)

        self.base_model_type_label = QLabel("Model Type", self)
        self.base_model_type_label.setToolTip(
            "Type of base model. 'auto' detects from checkpoint keys."
        )
        self.base_model_type_select = ComboBox(self)
        self.base_model_type_select.addItems(["auto", "sdxl", "anima"])
        self.base_model_type_select.setEnabled(False)
        self.widget.formLayout.addRow(
            self.base_model_type_label, self.base_model_type_select
        )

        self.recipe_preset_label = QLabel("Resize Recipe", self)
        self.recipe_preset_label.setToolTip(
            "Scoring recipe preset for base-model-aware resize.\n"
            "Score = log10(singular_value / base_norm). Keep dim if score >= threshold.\n"
            "Higher (less negative) threshold = more aggressive pruning.\n\n"
            "Conservative (thr=-3.0): mild, keeps dims > 0.1% of base norm.\n"
            "Balanced (thr=-2.0): moderate, keeps dims > 1% of base norm.\n"
            "Aggressive (thr=-1.6990): heavy, keeps dims > 2% of base norm.\n"
            "Spectral Norm: like Balanced but uses spectral norm for scoring.\n"
            "Subspace-Aware: mixes base-norm and subspace alignment scoring."
        )
        self.recipe_preset_select = ComboBox(self)
        for name, _ in RECIPE_PRESETS:
            self.recipe_preset_select.addItem(name)
        self.recipe_preset_select.setEnabled(False)
        self.widget.formLayout.addRow(
            self.recipe_preset_label, self.recipe_preset_select
        )

        self.custom_recipe_label = QLabel("Custom Recipe", self)
        self.custom_recipe_label.setToolTip(
            "Custom scoring recipe string. Format: key=val,key=val,...\n"
            "Score keys: spn_lora, spn_ckpt, subspace, fro_lora, fro_ckpt, params\n"
            "Control keys: size=<MB>, thr=<threshold>, rescale=<factor>"
        )
        self.custom_recipe_input = QLineEdit(self)
        self.custom_recipe_input.setPlaceholderText("e.g. fro_ckpt=1,thr=-4.0")
        self.custom_recipe_input.setEnabled(False)
        self.custom_recipe_label.setVisible(False)
        self.custom_recipe_input.setVisible(False)
        self.widget.formLayout.addRow(
            self.custom_recipe_label, self.custom_recipe_input
        )

        self.adjustSize()

    def setup_connections(self) -> None:
        self.widget.model_input.textChanged.connect(
            lambda x: self.edit_args("model", x)
        )
        self.widget.model_input_selector.clicked.connect(
            lambda: self.set_file_from_dialog(
                self.widget.model_input, "Model To Resize", "lora files"
            )
        )
        self.widget.save_precision_select.currentTextChanged.connect(
            lambda x: self.edit_args("save_precision", x)
        )
        self.widget.new_rank_input.valueChanged.connect(
            lambda x: self.edit_args("new_rank", x)
        )
        self.widget.new_conv_enable.clicked.connect(self.enable_disable_conv_dims)
        self.widget.new_conv_rank_input.valueChanged.connect(
            lambda x: self.edit_args("new_conv_rank", x, True)
        )
        self.widget.output_folder_enable.clicked.connect(
            self.enable_disable_output_folder
        )
        self.widget.output_folder_input.textChanged.connect(
            lambda x: self.edit_args("output_folder", x, True)
        )
        self.widget.output_folder_selector.clicked.connect(
            lambda: self.set_folder_from_dialog(
                self.widget.output_folder_input, "Output Folder"
            )
        )
        self.widget.output_name_enable.clicked.connect(self.enable_disable_output_name)
        self.widget.output_name_input.textChanged.connect(
            lambda x: self.edit_args("output_name", x.split(".")[0], True)
        )
        self.widget.dynamic_param_enable.clicked.connect(self.enable_disable_dynamic)
        self.widget.dynamic_param_select.currentTextChanged.connect(
            self.on_dynamic_method_changed
        )
        self.widget.dynamic_param_input.valueChanged.connect(
            lambda x: self.edit_args("dynamic_param", round(x, 4))
        )
        self.widget.use_gpu_enable.clicked.connect(
            lambda x: self.edit_args("device", "cuda" if x else False, True)
        )
        self.widget.verbose_enable.clicked.connect(
            lambda x: self.edit_args("verbose", x, True)
        )
        self.widget.remove_conv_dims_enable.clicked.connect(
            lambda x: self.edit_args("del_conv", x, True)
        )
        self.widget.remove_linear_dims_enable.clicked.connect(
            lambda x: self.edit_args("del_linear", x, True)
        )
        self.base_model_enable.clicked.connect(self.enable_disable_base_model)
        self.base_model_selector.clicked.connect(
            lambda: self.set_file_from_dialog(
                self.base_model_input, "Base Model Checkpoint", "safetensors files"
            )
        )
        self.base_model_input.textChanged.connect(
            lambda x: self.edit_args("base_model", x, True)
        )
        self.base_model_type_select.currentTextChanged.connect(
            lambda x: self.edit_args("base_model_type", x)
        )
        self.recipe_preset_select.currentTextChanged.connect(
            self.on_recipe_preset_changed
        )
        self.custom_recipe_input.textChanged.connect(
            lambda x: self.edit_args("score_recipe", x, True)
        )
        self.widget.begin_resize_button.clicked.connect(self.start_resize)

    def enable_disable_conv_dims(self, toggle: bool) -> None:
        if "new_conv_rank" in self.args:
            del self.args["new_conv_rank"]
        self.widget.new_conv_rank_input.setEnabled(toggle)
        if not toggle:
            return
        self.edit_args("new_conv_rank", self.widget.new_conv_rank_input.value(), True)

    def enable_disable_output_folder(self, toggle: bool) -> None:
        if "output_folder" in self.args:
            del self.args["output_folder"]
        self.widget.output_folder_input.setEnabled(toggle)
        self.widget.output_folder_selector.setEnabled(toggle)
        if not toggle:
            return
        self.edit_args("output_folder", self.widget.output_folder_input.text(), True)

    def enable_disable_output_name(self, toggle: bool) -> None:
        if "output_name" in self.args:
            del self.args["output_name"]
        self.widget.output_name_input.setEnabled(toggle)
        if not toggle:
            return
        self.edit_args("output_name", self.widget.output_name_input.text(), True)

    def on_dynamic_method_changed(self, method: str) -> None:
        self.edit_args("dynamic_method", method)
        if method == "sv_ratio":
            self.widget.dynamic_param_input.setMinimum(1.0)
            self.widget.dynamic_param_input.setMaximum(10.0)
            self.widget.dynamic_param_input.setSingleStep(0.1)
            self.widget.dynamic_param_input.setDecimals(1)
            if self.widget.dynamic_param_input.value() < 1.0:
                self.widget.dynamic_param_input.setValue(2.0)
        else:
            self.widget.dynamic_param_input.setMinimum(0.0001)
            self.widget.dynamic_param_input.setMaximum(1.0)
            self.widget.dynamic_param_input.setSingleStep(0.01)
            self.widget.dynamic_param_input.setDecimals(4)
            if self.widget.dynamic_param_input.value() > 1.0:
                self.widget.dynamic_param_input.setValue(0.97)

    def enable_disable_dynamic(self, toggle: bool) -> None:
        for arg in ["dynamic_param", "dynamic_method"]:
            if arg in self.args:
                del self.args[arg]
        self.widget.dynamic_param_select.setEnabled(toggle)
        self.widget.dynamic_param_input.setEnabled(toggle)

        if not toggle:
            self.widget.new_rank_label.setText("New Rank")
            self.widget.new_conv_enable.setText("New Conv Rank")
            return
        self.widget.new_rank_label.setText("Max Rank")
        self.widget.new_conv_enable.setText("Max Conv Rank")
        self.edit_args("dynamic_method", self.widget.dynamic_param_select.currentText())
        self.edit_args(
            "dynamic_param", round(self.widget.dynamic_param_input.value(), 4)
        )

    def enable_disable_base_model(self, toggle: bool) -> None:
        # Enable/disable base model controls
        self.base_model_input.setEnabled(toggle)
        self.base_model_selector.setEnabled(toggle)
        self.base_model_type_select.setEnabled(toggle)
        self.recipe_preset_select.setEnabled(toggle)

        if toggle:
            # Remove standard-mode args
            for arg in ["new_rank", "new_conv_rank", "dynamic_method",
                        "dynamic_param", "del_conv", "del_linear"]:
                self.args.pop(arg, None)
            # Disable standard controls
            self.widget.new_rank_input.setEnabled(False)
            self.widget.new_conv_enable.setEnabled(False)
            self.widget.new_conv_rank_input.setEnabled(False)
            self.widget.dynamic_param_enable.setEnabled(False)
            self.widget.dynamic_param_select.setEnabled(False)
            self.widget.dynamic_param_input.setEnabled(False)
            self.widget.remove_conv_dims_enable.setEnabled(False)
            self.widget.remove_linear_dims_enable.setEnabled(False)
            # Add base model args
            self.edit_args("base_model", self.base_model_input.text(), True)
            self.edit_args("base_model_type", self.base_model_type_select.currentText())
            preset_idx = self.recipe_preset_select.currentIndex()
            if preset_idx < len(RECIPE_PRESETS) - 1:  # Not "Custom"
                self.edit_args("score_recipe", RECIPE_PRESETS[preset_idx][1])
            else:
                self.edit_args("score_recipe", self.custom_recipe_input.text(), True)
        else:
            # Remove base model args
            for arg in ["base_model", "base_model_type", "score_recipe"]:
                self.args.pop(arg, None)
            # Re-enable standard controls
            self.widget.new_rank_input.setEnabled(True)
            self.widget.new_conv_enable.setEnabled(True)
            self.widget.dynamic_param_enable.setEnabled(True)
            self.widget.remove_conv_dims_enable.setEnabled(True)
            self.widget.remove_linear_dims_enable.setEnabled(True)
            # Restore standard args
            self.edit_args("new_rank", self.widget.new_rank_input.value())
            # Re-sync dynamic method state
            self.enable_disable_dynamic(
                self.widget.dynamic_param_enable.isChecked()
            )
            # Re-sync conv rank state
            if self.widget.new_conv_enable.isChecked():
                self.widget.new_conv_rank_input.setEnabled(True)
                self.edit_args(
                    "new_conv_rank",
                    self.widget.new_conv_rank_input.value(),
                    True,
                )

        # Hide/show custom recipe based on current selection
        is_custom = self.recipe_preset_select.currentText() == "Custom"
        self.custom_recipe_label.setVisible(toggle and is_custom)
        self.custom_recipe_input.setVisible(toggle and is_custom)
        self.custom_recipe_input.setEnabled(toggle and is_custom)

    def on_recipe_preset_changed(self, text: str) -> None:
        is_custom = text == "Custom"
        is_enabled = self.base_model_enable.isChecked()
        self.custom_recipe_label.setVisible(is_custom and is_enabled)
        self.custom_recipe_input.setVisible(is_custom and is_enabled)
        self.custom_recipe_input.setEnabled(is_custom and is_enabled)
        if not is_custom:
            for name, recipe in RECIPE_PRESETS:
                if name == text:
                    self.edit_args("score_recipe", recipe)
                    break
        else:
            self.edit_args("score_recipe", self.custom_recipe_input.text(), True)

    def start_resize(self) -> None:
        if "model" not in self.args:
            return
        args = [f"--save_to={self.get_output_name()}"]
        for key, value in self.args.items():
            if key in ["output_name", "output_folder"]:
                continue
            if key in ("model", "base_model"):
                value = Path(value).as_posix()
            if value is True:
                args.append(f"--{key}")
            else:
                args.append(f"--{key}={value}")
        self.resize_helper(args)

    def resize_helper(self, args: str) -> bool:
        config = Path("config.json")
        config_dict = json.loads(config.read_text()) if config.exists() else {}
        url = config_dict.get("backend_url", "http://127.0.0.1:8000")
        try:
            response = requests.post(
                f"{url}/resize",
                data=json.dumps(args),
                timeout=0.05,
            )
        except ConnectionError as e:
            print(e)
            return False
        except requests.exceptions.Timeout:
            return True
        if response.status_code != 200:
            print(f"Failed to resize: {response.text}")
            return False

    def get_output_name(self) -> str:
        if "output_name" in self.args:
            name = self.args["output_name"]
        else:
            name = Path(self.args["model"]).stem

        if "base_model" in self.args:
            preset = self.recipe_preset_select.currentText()
            name += f"-scored-{preset.lower().replace(' ', '_')}"
        else:
            if "dynamic_method" in self.args:
                name += f"-{self.args['dynamic_method']}-{self.args['dynamic_param']}"
            if "del_linear" in self.args:
                name += "-no_linear"
            else:
                name += f"-{self.args['new_rank']}"
            if "del_conv" in self.args:
                name += "-no_conv"
            elif "new_conv_rank" in self.args:
                name += f"-{self.args['new_conv_rank']}"

        output_folder = self.args.get("output_folder", "default_output")
        return Path(output_folder).joinpath(f"{name}.safetensors").as_posix()
