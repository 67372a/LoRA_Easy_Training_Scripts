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
        
        # DiT Path
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
        
        # Qwen3 Path
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
        
        # VAE Path
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
        
        # LLM Adapter Path
        self.label_llm = QLabel(self.anima_training_box)
        self.label_llm.setObjectName(u"label_llm")
        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.label_llm)
        self.horizontalLayout_llm = QHBoxLayout()
        self.horizontalLayout_llm.setObjectName(u"horizontalLayout_llm")
        self.llm_adapter_input = DragDropLineEdit(self.anima_training_box)
        self.llm_adapter_input.setObjectName(u"llm_adapter_input")
        self.horizontalLayout_llm.addWidget(self.llm_adapter_input)
        self.llm_adapter_selector = QPushButton(self.anima_training_box)
        self.llm_adapter_selector.setObjectName(u"llm_adapter_selector")
        self.horizontalLayout_llm.addWidget(self.llm_adapter_selector)
        self.formLayout_3.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_llm)

        # T5 Tokenizer Path
        self.label_t5 = QLabel(self.anima_training_box)
        self.label_t5.setObjectName(u"label_t5")
        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.label_t5)
        self.horizontalLayout_t5 = QHBoxLayout()
        self.horizontalLayout_t5.setObjectName(u"horizontalLayout_t5")
        self.t5_tokenizer_input = DragDropLineEdit(self.anima_training_box)
        self.t5_tokenizer_input.setObjectName(u"t5_tokenizer_input")
        self.horizontalLayout_t5.addWidget(self.t5_tokenizer_input)
        self.t5_tokenizer_selector = QPushButton(self.anima_training_box)
        self.t5_tokenizer_selector.setObjectName(u"t5_tokenizer_selector")
        self.horizontalLayout_t5.addWidget(self.t5_tokenizer_selector)
        self.formLayout_3.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_t5)

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
        
        self.formLayout_3.setLayout(5, QFormLayout.SpanningRole, self.horizontalLayout_tokens)

        # Sampling Params
        self.horizontalLayout_sampling = QHBoxLayout()
        
        self.label_sampling = QLabel(self.anima_training_box)
        self.label_sampling.setObjectName(u"label_sampling")
        self.horizontalLayout_sampling.addWidget(self.label_sampling)
        self.timestep_sampling_selector = ComboBox(self.anima_training_box)
        self.timestep_sampling_selector.addItem("logit_normal")
        self.timestep_sampling_selector.addItem("uniform")
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
        
        self.formLayout_3.setLayout(6, QFormLayout.SpanningRole, self.horizontalLayout_sampling)

        # Misc
        self.horizontalLayout_misc = QHBoxLayout()
        self.flash_attn_enable = QCheckBox(self.anima_training_box)
        self.flash_attn_enable.setObjectName(u"flash_attn_enable")
        self.horizontalLayout_misc.addWidget(self.flash_attn_enable)

        self.train_llm_adapter_checkbox = QCheckBox(self.anima_training_box)
        self.train_llm_adapter_checkbox.setObjectName(u"train_llm_adapter_checkbox")
        self.horizontalLayout_misc.addWidget(self.train_llm_adapter_checkbox)
        
        self.label_dtype = QLabel(self.anima_training_box)
        self.label_dtype.setObjectName(u"label_dtype")
        self.horizontalLayout_misc.addWidget(self.label_dtype)
        self.transformer_dtype_selector = ComboBox(self.anima_training_box)
        self.transformer_dtype_selector.addItem("") # None/Default
        self.transformer_dtype_selector.addItem("float16")
        self.transformer_dtype_selector.addItem("bfloat16")
        self.transformer_dtype_selector.addItem("float32")
        self.horizontalLayout_misc.addWidget(self.transformer_dtype_selector)
        
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
        self.label_3.setText(QCoreApplication.translate("anima_ui", u"WanVAE Model", None))
        self.label_llm.setText(QCoreApplication.translate("anima_ui", u"LLM Adapter", None))
        self.label_t5.setText(QCoreApplication.translate("anima_ui", u"T5 Tokenizer", None))
        self.qwen3_len_label.setText(QCoreApplication.translate("anima_ui", u"Qwen3 Max Tokens", None))
        self.t5_len_label.setText(QCoreApplication.translate("anima_ui", u"T5 Max Tokens", None))
        self.label_sampling.setText(QCoreApplication.translate("anima_ui", u"Timestep Sampling", None))
        self.label_shift.setText(QCoreApplication.translate("anima_ui", u"Discrete Flow Shift", None))
        self.label_sigmoid.setText(QCoreApplication.translate("anima_ui", u"Sigmoid Scale", None))
        self.flash_attn_enable.setText(QCoreApplication.translate("anima_ui", u"Flash Attention", None))
        self.train_llm_adapter_checkbox.setText(QCoreApplication.translate("anima_ui", u"Train LLM Adapter", None))
        self.label_dtype.setText(QCoreApplication.translate("anima_ui", u"Transformer Dtype", None))

        # Tooltips and Placeholders
        self.dit_model_input.setPlaceholderText(QCoreApplication.translate("anima_ui", u"Path to DiT model file [Required]", None))
        self.dit_model_input.setToolTip(QCoreApplication.translate("anima_ui", u"Path to the Anima DiT model file (.safetensors). [Required]", None))

        self.qwen3_model_input.setPlaceholderText(QCoreApplication.translate("anima_ui", u"Path to Qwen3 model [Required]", None))
        self.qwen3_model_input.setToolTip(QCoreApplication.translate("anima_ui", u"Path to the Qwen3-0.6B text encoder model file or directory. [Required]", None))

        self.vae_model_input.setPlaceholderText(QCoreApplication.translate("anima_ui", u"Path to WanVAE model [Required]", None))
        self.vae_model_input.setToolTip(QCoreApplication.translate("anima_ui", u"Path to the WanVAE model file. [Required]", None))

        self.llm_adapter_input.setPlaceholderText(QCoreApplication.translate("anima_ui", u"LLM Adapter path (Optional)", None))
        self.llm_adapter_input.setToolTip(QCoreApplication.translate("anima_ui", u"Path to the LLM Adapter weights. If not provided, it will attempt to load from the DiT model file. [Optional]", None))

        self.t5_tokenizer_input.setPlaceholderText(QCoreApplication.translate("anima_ui", u"T5 Tokenizer path (Optional)", None))
        self.t5_tokenizer_input.setToolTip(QCoreApplication.translate("anima_ui", u"Path to the T5 tokenizer directory. If not provided, uses the built-in configuration. [Optional]", None))

        self.qwen3_max_token_input.setToolTip(QCoreApplication.translate("anima_ui", u"Maximum token length for Qwen3 tokenizer. Default: 512. [Optional]", None))
        self.t5_max_token_input.setToolTip(QCoreApplication.translate("anima_ui", u"Maximum token length for T5 tokenizer. Default: 512. [Optional]", None))

        self.timestep_sampling_selector.setToolTip(QCoreApplication.translate("anima_ui", u"Method for sampling timesteps during training. 'logit_normal' is recommended. [Optional]", None))
        self.discrete_flow_shift_input.setToolTip(QCoreApplication.translate("anima_ui", u"Shift value for the Rectified Flow timestep distribution. Default: 3.0. [Optional]", None))
        self.sigmoid_scale_input.setToolTip(QCoreApplication.translate("anima_ui", u"Scale factor for logit_normal sampling. Default: 1.0. [Optional]", None))

        self.flash_attn_enable.setToolTip(QCoreApplication.translate("anima_ui", u"Enable Flash Attention for faster training and lower VRAM usage. Requires flash-attn package. [Optional]", None))
        self.train_llm_adapter_checkbox.setToolTip(QCoreApplication.translate("anima_ui", u"Enable training of the LLM adapter (e.g. Qwen3). Required if you are training the text encoder/adapter. [Optional]", None))
        self.transformer_dtype_selector.setToolTip(QCoreApplication.translate("anima_ui", u"Override the data type for the transformer blocks. If unset, uses the mixed precision setting. [Optional]", None))
