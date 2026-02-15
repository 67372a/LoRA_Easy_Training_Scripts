# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AnimaUI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

from modules.DragDropLineEdit import DragDropLineEdit
from modules.ScrollOnSelect import (ComboBox, DoubleSpinBox, SpinBox)

class Ui_anima_ui(object):
    def setupUi(self, anima_ui):
        if not anima_ui.objectName():
            anima_ui.setObjectName(u"anima_ui")
        anima_ui.resize(523, 500)
        self.gridLayout = QGridLayout(anima_ui)
        self.gridLayout.setObjectName(u"gridLayout")
        self.anima_training_box = QGroupBox(anima_ui)
        self.anima_training_box.setObjectName(u"anima_training_box")
        self.anima_training_box.setCheckable(True)
        self.anima_training_box.setChecked(False)
        self.gridLayout_2 = QGridLayout(self.anima_training_box)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        
        # DiT Path (maps to pretrained_model_name_or_path)
        self.label = QLabel(self.anima_training_box)
        self.label.setObjectName(u"label")
        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.dit_model_input = DragDropLineEdit(self.anima_training_box)
        self.dit_model_input.setObjectName(u"dit_model_input")
        self.horizontalLayout.addWidget(self.dit_model_input)
        self.dit_model_selector = QPushButton(self.anima_training_box)
        self.dit_model_selector.setObjectName(u"dit_model_selector")
        self.horizontalLayout.addWidget(self.dit_model_selector)
        self.formLayout_3.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)
        
        # Qwen3 Path (maps to --qwen3)
        self.label_2 = QLabel(self.anima_training_box)
        self.label_2.setObjectName(u"label_2")
        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.qwen3_model_input = DragDropLineEdit(self.anima_training_box)
        self.qwen3_model_input.setObjectName(u"qwen3_model_input")
        self.horizontalLayout_2.addWidget(self.qwen3_model_input)
        self.qwen3_model_selector = QPushButton(self.anima_training_box)
        self.qwen3_model_selector.setObjectName(u"qwen3_model_selector")
        self.horizontalLayout_2.addWidget(self.qwen3_model_selector)
        self.formLayout_3.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_2)
        
        # VAE Path (maps to --vae)
        self.label_3 = QLabel(self.anima_training_box)
        self.label_3.setObjectName(u"label_3")
        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.vae_model_input = DragDropLineEdit(self.anima_training_box)
        self.vae_model_input.setObjectName(u"vae_model_input")
        self.horizontalLayout_3.addWidget(self.vae_model_input)
        self.vae_model_selector = QPushButton(self.anima_training_box)
        self.vae_model_selector.setObjectName(u"vae_model_selector")
        self.horizontalLayout_3.addWidget(self.vae_model_selector)
        self.formLayout_3.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_3)

        # T5 Tokenizer Path
        self.label_t5 = QLabel(self.anima_training_box)
        self.label_t5.setObjectName(u"label_t5")
        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.label_t5)
        self.horizontalLayout_t5 = QHBoxLayout()
        self.horizontalLayout_t5.setObjectName(u"horizontalLayout_t5")
        self.t5_tokenizer_input = DragDropLineEdit(self.anima_training_box)
        self.t5_tokenizer_input.setObjectName(u"t5_tokenizer_input")
        self.horizontalLayout_t5.addWidget(self.t5_tokenizer_input)
        self.t5_tokenizer_selector = QPushButton(self.anima_training_box)
        self.t5_tokenizer_selector.setObjectName(u"t5_tokenizer_selector")
        self.horizontalLayout_t5.addWidget(self.t5_tokenizer_selector)
        self.formLayout_3.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_t5)

        # Token Lengths
        self.horizontalLayout_tokens = QHBoxLayout()
        
        self.qwen3_len_label = QLabel(self.anima_training_box)
        self.qwen3_len_label.setObjectName(u"qwen3_len_label")
        self.horizontalLayout_tokens.addWidget(self.qwen3_len_label)
        self.qwen3_max_token_input = SpinBox(self.anima_training_box)
        self.qwen3_max_token_input.setMaximum(16777215)
        self.qwen3_max_token_input.setValue(512)
        self.horizontalLayout_tokens.addWidget(self.qwen3_max_token_input)
        
        self.t5_len_label = QLabel(self.anima_training_box)
        self.t5_len_label.setObjectName(u"t5_len_label")
        self.horizontalLayout_tokens.addWidget(self.t5_len_label)
        self.t5_max_token_input = SpinBox(self.anima_training_box)
        self.t5_max_token_input.setMaximum(16777215)
        self.t5_max_token_input.setValue(512)
        self.horizontalLayout_tokens.addWidget(self.t5_max_token_input)
        
        self.formLayout_3.setLayout(4, QFormLayout.SpanningRole, self.horizontalLayout_tokens)

        # Sampling Params
        self.horizontalLayout_sampling = QHBoxLayout()
        
        self.label_sampling = QLabel(self.anima_training_box)
        self.label_sampling.setObjectName(u"label_sampling")
        self.horizontalLayout_sampling.addWidget(self.label_sampling)
        self.timestep_sampling_selector = ComboBox(self.anima_training_box)
        self.timestep_sampling_selector.addItem("sigma")
        self.timestep_sampling_selector.addItem("uniform")
        self.timestep_sampling_selector.addItem("sigmoid")
        self.timestep_sampling_selector.addItem("shift")
        self.timestep_sampling_selector.addItem("flux_shift")
        self.horizontalLayout_sampling.addWidget(self.timestep_sampling_selector)
        
        self.label_shift = QLabel(self.anima_training_box)
        self.label_shift.setObjectName(u"label_shift")
        self.horizontalLayout_sampling.addWidget(self.label_shift)
        self.discrete_flow_shift_input = DoubleSpinBox(self.anima_training_box)
        self.discrete_flow_shift_input.setDecimals(2)
        self.discrete_flow_shift_input.setSingleStep(0.1)
        self.discrete_flow_shift_input.setValue(3.0)
        self.horizontalLayout_sampling.addWidget(self.discrete_flow_shift_input)

        self.label_sigmoid = QLabel(self.anima_training_box)
        self.label_sigmoid.setObjectName(u"label_sigmoid")
        self.horizontalLayout_sampling.addWidget(self.label_sigmoid)
        self.sigmoid_scale_input = DoubleSpinBox(self.anima_training_box)
        self.sigmoid_scale_input.setDecimals(2)
        self.sigmoid_scale_input.setSingleStep(0.1)
        self.sigmoid_scale_input.setValue(1.0)
        self.horizontalLayout_sampling.addWidget(self.sigmoid_scale_input)
        
        self.formLayout_3.setLayout(5, QFormLayout.SpanningRole, self.horizontalLayout_sampling)

        # VAE / Memory Options
        self.horizontalLayout_vae_mem = QHBoxLayout()

        self.label_vae_chunk = QLabel(self.anima_training_box)
        self.label_vae_chunk.setObjectName(u"label_vae_chunk")
        self.horizontalLayout_vae_mem.addWidget(self.label_vae_chunk)
        self.vae_chunk_size_input = SpinBox(self.anima_training_box)
        self.vae_chunk_size_input.setObjectName(u"vae_chunk_size_input")
        self.vae_chunk_size_input.setMinimum(0)
        self.vae_chunk_size_input.setMaximum(16777215)
        self.vae_chunk_size_input.setSingleStep(2)
        self.vae_chunk_size_input.setValue(0)
        self.horizontalLayout_vae_mem.addWidget(self.vae_chunk_size_input)

        self.vae_disable_cache_enable = QCheckBox(self.anima_training_box)
        self.vae_disable_cache_enable.setObjectName(u"vae_disable_cache_enable")
        self.horizontalLayout_vae_mem.addWidget(self.vae_disable_cache_enable)

        self.label_blocks_to_swap = QLabel(self.anima_training_box)
        self.label_blocks_to_swap.setObjectName(u"label_blocks_to_swap")
        self.horizontalLayout_vae_mem.addWidget(self.label_blocks_to_swap)
        self.blocks_to_swap_input = SpinBox(self.anima_training_box)
        self.blocks_to_swap_input.setObjectName(u"blocks_to_swap_input")
        self.blocks_to_swap_input.setMinimum(0)
        self.blocks_to_swap_input.setMaximum(100)
        self.blocks_to_swap_input.setValue(0)
        self.horizontalLayout_vae_mem.addWidget(self.blocks_to_swap_input)

        self.formLayout_3.setLayout(6, QFormLayout.SpanningRole, self.horizontalLayout_vae_mem)

        # Misc Checkboxes
        self.horizontalLayout_misc = QHBoxLayout()

        self.flash_attn_enable = QCheckBox(self.anima_training_box)
        self.flash_attn_enable.setObjectName(u"flash_attn_enable")
        self.horizontalLayout_misc.addWidget(self.flash_attn_enable)

        self.split_attn_enable = QCheckBox(self.anima_training_box)
        self.split_attn_enable.setObjectName(u"split_attn_enable")
        self.horizontalLayout_misc.addWidget(self.split_attn_enable)

        self.unsloth_offload_checkpointing = QCheckBox(self.anima_training_box)
        self.unsloth_offload_checkpointing.setObjectName(u"unsloth_offload_checkpointing")
        self.horizontalLayout_misc.addWidget(self.unsloth_offload_checkpointing)
        
        self.formLayout_3.setLayout(7, QFormLayout.SpanningRole, self.horizontalLayout_misc)

        self.gridLayout_2.addLayout(self.formLayout_3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.anima_training_box, 0, 0, 1, 1)

        self.retranslateUi(anima_ui)
        QMetaObject.connectSlotsByName(anima_ui)

    def retranslateUi(self, anima_ui):
        anima_ui.setWindowTitle(QCoreApplication.translate("anima_ui", u"Form", None))
        self.anima_training_box.setTitle(QCoreApplication.translate("anima_ui", u"Train Anima", None))
        self.label.setText(QCoreApplication.translate("anima_ui", u"DiT Model", None))
        self.label_2.setText(QCoreApplication.translate("anima_ui", u"Qwen3 Model", None))
        self.label_3.setText(QCoreApplication.translate("anima_ui", u"VAE Model", None))
        self.label_t5.setText(QCoreApplication.translate("anima_ui", u"T5 Tokenizer", None))
        self.qwen3_len_label.setText(QCoreApplication.translate("anima_ui", u"Qwen3 Max Tokens", None))
        self.t5_len_label.setText(QCoreApplication.translate("anima_ui", u"T5 Max Tokens", None))
        self.label_sampling.setText(QCoreApplication.translate("anima_ui", u"Timestep Sampling", None))
        self.label_shift.setText(QCoreApplication.translate("anima_ui", u"Discrete Flow Shift", None))
        self.label_sigmoid.setText(QCoreApplication.translate("anima_ui", u"Sigmoid Scale", None))
        self.label_vae_chunk.setText(QCoreApplication.translate("anima_ui", u"VAE Chunk Size", None))
        self.vae_disable_cache_enable.setText(QCoreApplication.translate("anima_ui", u"VAE Disable Cache", None))
        self.label_blocks_to_swap.setText(QCoreApplication.translate("anima_ui", u"Blocks to Swap", None))
        self.flash_attn_enable.setText(QCoreApplication.translate("anima_ui", u"Flash Attention", None))
        self.split_attn_enable.setText(QCoreApplication.translate("anima_ui", u"Split Attention", None))
        self.unsloth_offload_checkpointing.setText(QCoreApplication.translate("anima_ui", u"Unsloth Offload", None))

        # Tooltips and Placeholders
        self.dit_model_input.setPlaceholderText(QCoreApplication.translate("anima_ui",
            u"Path to DiT model file (.safetensors) [Required]", None))
        self.dit_model_input.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Path to the Anima DiT model file (.safetensors). "
            u"This maps to <code>--pretrained_model_name_or_path</code> in sd_scripts.</p></body></html>", None))

        self.qwen3_model_input.setPlaceholderText(QCoreApplication.translate("anima_ui",
            u"Path to Qwen3-0.6B model file or directory [Required]", None))
        self.qwen3_model_input.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Path to the Qwen3-0.6B text encoder model file (.safetensors) or "
            u"HuggingFace directory. Maps to <code>--qwen3</code> in sd_scripts.</p></body></html>", None))

        self.vae_model_input.setPlaceholderText(QCoreApplication.translate("anima_ui",
            u"Path to Qwen-Image VAE model file [Required]", None))
        self.vae_model_input.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Path to the Qwen-Image VAE model file (.safetensors). "
            u"Maps to <code>--vae</code> in sd_scripts.</p></body></html>", None))

        self.t5_tokenizer_input.setPlaceholderText(QCoreApplication.translate("anima_ui",
            u"T5 Tokenizer directory (Optional, uses built-in config if empty)", None))
        self.t5_tokenizer_input.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Path to the T5 tokenizer directory. If not provided, uses the built-in "
            u"<code>configs/t5_old/</code> configuration. Maps to <code>--t5_tokenizer_path</code>.</p></body></html>", None))

        self.qwen3_max_token_input.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Maximum token length for the Qwen3 tokenizer. Default: 512.</p></body></html>", None))
        self.t5_max_token_input.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Maximum token length for the T5 tokenizer. Default: 512.</p></body></html>", None))

        self.timestep_sampling_selector.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Method for sampling timesteps during training. "
            u"<code>sigmoid</code> (logit normal) is recommended for Anima.</p></body></html>", None))
        self.discrete_flow_shift_input.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Shift value for the Rectified Flow timestep distribution. Default: 3.0.</p></body></html>", None))
        self.sigmoid_scale_input.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Scale factor for logit_normal (sigmoid) timestep sampling. Default: 1.0.</p></body></html>", None))

        self.vae_chunk_size_input.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Spatial chunk size for Qwen-Image VAE encoding/decoding. "
            u"Reduces VRAM usage at the cost of speed. Must be an even number. "
            u"Set to 0 to disable chunking (default behavior).</p></body></html>", None))
        self.vae_disable_cache_enable.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Disable internal VAE caching mechanism to reduce VRAM usage. "
            u"Encoding/decoding will also be faster, but this differs from official behavior.</p></body></html>", None))
        self.blocks_to_swap_input.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Number of Transformer blocks to swap between CPU and GPU during "
            u"forward/backward passes. Reduces VRAM usage at the cost of training speed. "
            u"Set to 0 to disable (default).</p></body></html>", None))

        self.flash_attn_enable.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Use Flash Attention for faster training and lower VRAM usage. "
            u"Requires the <code>flash-attn</code> package. Maps to <code>--attn_mode flash</code>.</p></body></html>", None))
        self.split_attn_enable.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Split attention computation to reduce memory usage. "
            u"Automatically enabled when xFormers attention is selected in General Args. "
            u"Maps to <code>--split_attn</code>.</p></body></html>", None))
        self.unsloth_offload_checkpointing.setToolTip(QCoreApplication.translate("anima_ui",
            u"<html><head/><body><p>Offload activations to CPU RAM using async non-blocking transfers. "
            u"Faster than standard CPU offload checkpointing. Cannot be used with "
            u"<code>--cpu_offload_checkpointing</code> or <code>--blocks_to_swap</code>.</p></body></html>", None))
