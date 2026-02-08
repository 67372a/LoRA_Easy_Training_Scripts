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
        setup_file(self.widget.llm_adapter_input, self.widget.llm_adapter_selector)
        setup_file(self.widget.t5_tokenizer_input, self.widget.t5_tokenizer_selector, folder=True)

    def setup_connections(self) -> None:
        self.widget.anima_training_box.clicked.connect(self.enable_disable)
        
        # File inputs
        self.widget.dit_model_input.textChanged.connect(lambda x: self.edit_args("dit_path", x))
        self.widget.dit_model_selector.clicked.connect(
            lambda: self.set_file_from_dialog(self.widget.dit_model_input, "Anima DiT Model", "Model File")
        )
        
        self.widget.qwen3_model_input.textChanged.connect(lambda x: self.edit_args("qwen3_path", x))
        self.widget.qwen3_model_selector.clicked.connect(
            lambda: self.set_file_from_dialog(self.widget.qwen3_model_input, "Qwen3 Model", "Model File")
        )
        
        self.widget.vae_model_input.textChanged.connect(lambda x: self.edit_args("vae_path", x))
        self.widget.vae_model_selector.clicked.connect(
            lambda: self.set_file_from_dialog(self.widget.vae_model_input, "VAE Model", "Model File")
        )
        
        self.widget.llm_adapter_input.textChanged.connect(lambda x: self.edit_args("llm_adapter_path", x, optional=True))
        self.widget.llm_adapter_selector.clicked.connect(
            lambda: self.set_file_from_dialog(self.widget.llm_adapter_input, "LLM Adapter Model", "Model File")
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

        # Misc
        self.widget.flash_attn_enable.clicked.connect(
            lambda x: self.edit_args("flash_attn", x, True)
        )
        self.widget.transformer_dtype_selector.currentTextChanged.connect(
            lambda x: self.edit_args("transformer_dtype", x if x else False, True)
        )
        self.widget.train_llm_adapter_checkbox.clicked.connect(
            lambda x: self.edit_args("train_llm_adapter", x, True)
        )
        self.widget.unsloth_offload_checkpointing.clicked.connect(
            lambda x: self.edit_args("unsloth_offload_checkpointing", x, True)
        )

    def enable_disable(self, checked: bool) -> None:
        self.args = {}
        self.Toggled.emit(checked)
        if not checked:
            return
            
        self.edit_args("dit_path", self.widget.dit_model_input.text())
        self.edit_args("qwen3_path", self.widget.qwen3_model_input.text())
        self.edit_args("vae_path", self.widget.vae_model_input.text())
        self.edit_args("llm_adapter_path", self.widget.llm_adapter_input.text(), optional=True)
        self.edit_args("t5_tokenizer_path", self.widget.t5_tokenizer_input.text(), optional=True)
        
        self.edit_args("qwen3_max_token_length", self.widget.qwen3_max_token_input.value())
        self.edit_args("t5_max_token_length", self.widget.t5_max_token_input.value())
        
        self.change_timestep_sampling_type(self.widget.timestep_sampling_selector.currentIndex())
        self.edit_args("discrete_flow_shift", self.widget.discrete_flow_shift_input.value())
        
        self.edit_args("flash_attn", self.widget.flash_attn_enable.isChecked(), True)
        self.edit_args("train_llm_adapter", self.widget.train_llm_adapter_checkbox.isChecked(), True)
        self.edit_args("unsloth_offload_checkpointing", self.widget.unsloth_offload_checkpointing.isChecked(), True)
        
        dtype = self.widget.transformer_dtype_selector.currentText()
        if dtype:
            self.edit_args("transformer_dtype", dtype)

    def external_enable_disable(self, checked: bool) -> None:
        self.args = {}
        self.widget.anima_training_box.setEnabled(not checked)
        if self.widget.anima_training_box.isEnabled() and self.widget.anima_training_box.isChecked():
            self.enable_disable(True)

    def change_timestep_sampling_type(self, index: int) -> None:
        sampling_type = self.widget.timestep_sampling_selector.currentText()
        self.edit_args("timestep_sample_method", sampling_type)
        
        # Enable/Disable sigmoid scale based on selection (only for logit_normal)
        self.widget.sigmoid_scale_input.setEnabled(sampling_type == "logit_normal")
        if sampling_type == "logit_normal":
             self.edit_args("sigmoid_scale", self.widget.sigmoid_scale_input.value())
        elif "sigmoid_scale" in self.args:
            del self.args["sigmoid_scale"]

    def load_args(self, args: dict) -> bool:
        args: dict = args.get(self.name, {})

        self.widget.anima_training_box.setChecked(bool(args))
        self.widget.dit_model_input.setText(args.get("dit_path", ""))
        self.widget.qwen3_model_input.setText(args.get("qwen3_path", ""))
        self.widget.vae_model_input.setText(args.get("vae_path", ""))
        self.widget.llm_adapter_input.setText(args.get("llm_adapter_path", ""))
        self.widget.t5_tokenizer_input.setText(args.get("t5_tokenizer_path", ""))
        
        self.widget.qwen3_max_token_input.setValue(args.get("qwen3_max_token_length", 512))
        self.widget.t5_max_token_input.setValue(args.get("t5_max_token_length", 512))
        
        self.widget.timestep_sampling_selector.setCurrentText(args.get("timestep_sample_method", "logit_normal"))
        self.widget.discrete_flow_shift_input.setValue(args.get("discrete_flow_shift", 3.0))
        self.widget.sigmoid_scale_input.setValue(args.get("sigmoid_scale", 1.0))
        
        self.widget.flash_attn_enable.setChecked(args.get("flash_attn", False))
        self.widget.train_llm_adapter_checkbox.setChecked(args.get("train_llm_adapter", False))
        self.widget.unsloth_offload_checkpointing.setChecked(args.get("unsloth_offload_checkpointing", False))
        
        self.widget.transformer_dtype_selector.setCurrentText(args.get("transformer_dtype", ""))

        self.enable_disable(self.widget.anima_training_box.isChecked())
