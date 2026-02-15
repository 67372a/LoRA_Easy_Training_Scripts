from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QPushButton
from modules.DragDropLineEdit import DragDropLineEdit
from ui_files.AnimaUI import Ui_anima_ui
from modules.BaseWidget import BaseWidget
from pathlib import Path


class AnimaWidget(BaseWidget):
    Toggled = Signal(bool)  # send to general args

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Anima Args")
        self.widget = Ui_anima_ui()

        self.name = "anima_args"

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)

        def setup_file(elem: DragDropLineEdit, selector: QPushButton, folder=False):
            selector_icon = QIcon(str(Path("icons/more-horizontal.svg")))
            if folder:
                elem.setMode("folder")
            else:
                elem.setMode("file", [".ckpt", ".pt", ".safetensors", ".sft", ".pth"])
            elem.highlight = True
            selector.setIcon(selector_icon)

        setup_file(self.widget.dit_model_input, self.widget.dit_model_selector)
        setup_file(self.widget.qwen3_model_input, self.widget.qwen3_model_selector)
        setup_file(self.widget.vae_model_input, self.widget.vae_model_selector)
        setup_file(self.widget.t5_tokenizer_input, self.widget.t5_tokenizer_selector, folder=True)

    def setup_connections(self) -> None:
        self.widget.anima_training_box.clicked.connect(self.enable_disable)
        
        # File inputs — keys match sd_scripts argparse names
        self.widget.dit_model_input.textChanged.connect(lambda x: self.edit_args("pretrained_model_name_or_path", x))
        self.widget.dit_model_selector.clicked.connect(
            lambda: self.set_file_from_dialog(self.widget.dit_model_input, "Anima DiT Model", "Model File")
        )
        
        self.widget.qwen3_model_input.textChanged.connect(lambda x: self.edit_args("qwen3", x))
        self.widget.qwen3_model_selector.clicked.connect(
            lambda: self.set_file_from_dialog(self.widget.qwen3_model_input, "Qwen3 Model", "Model File")
        )
        
        self.widget.vae_model_input.textChanged.connect(lambda x: self.edit_args("vae", x))
        self.widget.vae_model_selector.clicked.connect(
            lambda: self.set_file_from_dialog(self.widget.vae_model_input, "VAE Model", "Model File")
        )
        
        self.widget.t5_tokenizer_input.textChanged.connect(lambda x: self.edit_args("t5_tokenizer_path", x, optional=True))
        self.widget.t5_tokenizer_selector.clicked.connect(
            lambda: self.set_folder_from_dialog(self.widget.t5_tokenizer_input, "T5 Tokenizer Folder")
        )

        # Token Lengths
        self.widget.qwen3_max_token_input.valueChanged.connect(
            lambda x: self.edit_args("qwen3_max_token_length", x)
        )
        self.widget.t5_max_token_input.valueChanged.connect(
            lambda x: self.edit_args("t5_max_token_length", x)
        )

        # Sampling Params
        self.widget.timestep_sampling_selector.currentIndexChanged.connect(self.change_timestep_sampling_type)
        self.widget.discrete_flow_shift_input.valueChanged.connect(
            lambda x: self.edit_args("discrete_flow_shift", x)
        )
        self.widget.sigmoid_scale_input.valueChanged.connect(
            lambda x: self.edit_args("sigmoid_scale", x)
        )

        # VAE / Memory Options
        self.widget.vae_chunk_size_input.valueChanged.connect(self.change_vae_chunk_size)
        self.widget.vae_disable_cache_enable.clicked.connect(
            lambda x: self.edit_args("vae_disable_cache", x, True)
        )
        self.widget.blocks_to_swap_input.valueChanged.connect(self.change_blocks_to_swap)

        # Misc
        self.widget.flash_attn_enable.clicked.connect(self.change_flash_attn)
        self.widget.split_attn_enable.clicked.connect(
            lambda x: self.edit_args("split_attn", x, True)
        )
        self.widget.unsloth_offload_checkpointing.clicked.connect(
            lambda x: self.edit_args("unsloth_offload_checkpointing", x, True)
        )

    def enable_disable(self, checked: bool) -> None:
        self.args = {}
        self.Toggled.emit(checked)
        if not checked:
            return
            
        self.edit_args("pretrained_model_name_or_path", self.widget.dit_model_input.text())
        self.edit_args("qwen3", self.widget.qwen3_model_input.text())
        self.edit_args("vae", self.widget.vae_model_input.text())
        self.edit_args("t5_tokenizer_path", self.widget.t5_tokenizer_input.text(), optional=True)
        
        self.edit_args("qwen3_max_token_length", self.widget.qwen3_max_token_input.value())
        self.edit_args("t5_max_token_length", self.widget.t5_max_token_input.value())
        
        self.change_timestep_sampling_type(self.widget.timestep_sampling_selector.currentIndex())
        self.edit_args("discrete_flow_shift", self.widget.discrete_flow_shift_input.value())
        
        self.change_vae_chunk_size(self.widget.vae_chunk_size_input.value())
        self.edit_args("vae_disable_cache", self.widget.vae_disable_cache_enable.isChecked(), True)
        self.change_blocks_to_swap(self.widget.blocks_to_swap_input.value())

        self.change_flash_attn(self.widget.flash_attn_enable.isChecked())
        self.edit_args("split_attn", self.widget.split_attn_enable.isChecked(), True)
        self.edit_args("unsloth_offload_checkpointing", self.widget.unsloth_offload_checkpointing.isChecked(), True)

    def external_enable_disable(self, checked: bool) -> None:
        self.args = {}
        self.widget.anima_training_box.setEnabled(not checked)
        if self.widget.anima_training_box.isEnabled() and self.widget.anima_training_box.isChecked():
            self.enable_disable(True)

    def change_timestep_sampling_type(self, index: int) -> None:
        sampling_type = self.widget.timestep_sampling_selector.currentText()
        self.edit_args("timestep_sampling", sampling_type)
        
        # Enable/Disable sigmoid scale based on selection (only for sigmoid/logit_normal)
        self.widget.sigmoid_scale_input.setEnabled(sampling_type == "sigmoid")
        if sampling_type == "sigmoid":
             self.edit_args("sigmoid_scale", self.widget.sigmoid_scale_input.value())
        elif "sigmoid_scale" in self.args:
            del self.args["sigmoid_scale"]

    def change_vae_chunk_size(self, value: int) -> None:
        """VAE chunk size: 0 means disabled (None), any positive value is used as-is."""
        if value > 0:
            self.edit_args("vae_chunk_size", value)
        elif "vae_chunk_size" in self.args:
            del self.args["vae_chunk_size"]

    def change_blocks_to_swap(self, value: int) -> None:
        """Blocks to swap: 0 means disabled (None), any positive value is used as-is."""
        if value > 0:
            self.edit_args("blocks_to_swap", value)
        elif "blocks_to_swap" in self.args:
            del self.args["blocks_to_swap"]

    def change_flash_attn(self, checked: bool) -> None:
        """Flash attention: sets attn_mode to 'flash' when enabled, removes it when disabled."""
        if checked:
            self.edit_args("attn_mode", "flash")
        elif "attn_mode" in self.args:
            del self.args["attn_mode"]

    def update_split_attn_from_general(self, xformers_enabled: bool, sdpa_enabled: bool) -> None:
        """Called from ArgsListUI when attention mode changes in GeneralUI.
        
        When xFormers is enabled with Anima, split_attn should be forcibly enabled.
        When SDPA is enabled, split_attn is automatically enabled internally by sd_scripts.
        """
        if xformers_enabled:
            self.widget.split_attn_enable.setChecked(True)
            self.widget.split_attn_enable.setEnabled(False)
            self.edit_args("split_attn", True, True)
        else:
            self.widget.split_attn_enable.setEnabled(True)

    def load_args(self, args: dict) -> bool:
        args: dict = args.get(self.name, {})

        self.widget.anima_training_box.setChecked(bool(args))
        self.widget.dit_model_input.setText(args.get("pretrained_model_name_or_path", ""))
        self.widget.qwen3_model_input.setText(args.get("qwen3", ""))
        self.widget.vae_model_input.setText(args.get("vae", ""))
        self.widget.t5_tokenizer_input.setText(args.get("t5_tokenizer_path", ""))
        
        self.widget.qwen3_max_token_input.setValue(args.get("qwen3_max_token_length", 512))
        self.widget.t5_max_token_input.setValue(args.get("t5_max_token_length", 512))
        
        self.widget.timestep_sampling_selector.setCurrentText(args.get("timestep_sampling", "sigmoid"))
        self.widget.discrete_flow_shift_input.setValue(args.get("discrete_flow_shift", 3.0))
        self.widget.sigmoid_scale_input.setValue(args.get("sigmoid_scale", 1.0))

        self.widget.vae_chunk_size_input.setValue(args.get("vae_chunk_size", 0))
        self.widget.vae_disable_cache_enable.setChecked(args.get("vae_disable_cache", False))
        self.widget.blocks_to_swap_input.setValue(args.get("blocks_to_swap", 0))
        
        # flash_attn is stored as attn_mode="flash"
        self.widget.flash_attn_enable.setChecked(args.get("attn_mode", "") == "flash")
        self.widget.split_attn_enable.setChecked(args.get("split_attn", False))
        self.widget.unsloth_offload_checkpointing.setChecked(args.get("unsloth_offload_checkpointing", False))

        self.enable_disable(self.widget.anima_training_box.isChecked())
