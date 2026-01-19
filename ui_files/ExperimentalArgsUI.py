# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExperimentalArgsUI.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

from modules.ScrollOnSelect import (ComboBox, DoubleSpinBox, SpinBox)

class Ui_base_args_ui(object):
    def setupUi(self, base_args_ui):
        if not base_args_ui.objectName():
            base_args_ui.setObjectName(u"base_args_ui")
        base_args_ui.resize(788, 561)
        self.verticalLayout_2 = QVBoxLayout(base_args_ui)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.misc_experimental_args_tab_notice = QHBoxLayout()
        self.misc_experimental_args_tab_notice.setObjectName(u"misc_experimental_args_tab_notice")
        self.line = QFrame(base_args_ui)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.misc_experimental_args_tab_notice.addWidget(self.line)

        self.experimental_args_notice_label = QLabel(base_args_ui)
        self.experimental_args_notice_label.setObjectName(u"experimental_args_notice_label")
        self.experimental_args_notice_label.setWordWrap(True)

        self.misc_experimental_args_tab_notice.addWidget(self.experimental_args_notice_label)


        self.verticalLayout_2.addLayout(self.misc_experimental_args_tab_notice)

        self.flow_model_settings_box = QGroupBox(base_args_ui)
        self.flow_model_settings_box.setObjectName(u"flow_model_settings_box")
        self.flow_model_settings_box.setEnabled(True)
        self.flow_model_settings_box.setFlat(True)
        self.flow_model_settings_box.setCheckable(True)
        self.flow_model_settings_box.setChecked(False)
        self.verticalLayout = QVBoxLayout(self.flow_model_settings_box)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.line_2 = QFrame(self.flow_model_settings_box)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.flow_notice_label = QLabel(self.flow_model_settings_box)
        self.flow_notice_label.setObjectName(u"flow_notice_label")
        self.flow_notice_label.setWordWrap(True)
        self.flow_notice_label.setOpenExternalLinks(False)

        self.horizontalLayout.addWidget(self.flow_notice_label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.formLayout_7 = QFormLayout()
        self.formLayout_7.setObjectName(u"formLayout_7")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(3, -1, -1, -1)
        self.label = QLabel(self.flow_model_settings_box)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.flow_logit_mean_input = DoubleSpinBox(self.flow_model_settings_box)
        self.flow_logit_mean_input.setObjectName(u"flow_logit_mean_input")
        self.flow_logit_mean_input.setMinimum(-100.000000000000000)
        self.flow_logit_mean_input.setMaximum(100.000000000000000)
        self.flow_logit_mean_input.setSingleStep(0.100000000000000)
        self.flow_logit_mean_input.setValue(0.000000000000000)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.flow_logit_mean_input)

        self.label_2 = QLabel(self.flow_model_settings_box)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.flow_logit_std_input = DoubleSpinBox(self.flow_model_settings_box)
        self.flow_logit_std_input.setObjectName(u"flow_logit_std_input")
        self.flow_logit_std_input.setMaximum(100.000000000000000)
        self.flow_logit_std_input.setSingleStep(0.100000000000000)
        self.flow_logit_std_input.setValue(1.000000000000000)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.flow_logit_std_input)


        self.formLayout_7.setLayout(0, QFormLayout.ItemRole.FieldRole, self.formLayout_2)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(-1, -1, 3, -1)
        self.label_4 = QLabel(self.flow_model_settings_box)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.flow_timestep_distribution_selector = ComboBox(self.flow_model_settings_box)
        self.flow_timestep_distribution_selector.addItem("")
        self.flow_timestep_distribution_selector.addItem("")
        self.flow_timestep_distribution_selector.setObjectName(u"flow_timestep_distribution_selector")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.flow_timestep_distribution_selector)

        self.label_8 = QLabel(self.flow_model_settings_box)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.flow_uniform_static_ratio_shift_input = DoubleSpinBox(self.flow_model_settings_box)
        self.flow_uniform_static_ratio_shift_input.setObjectName(u"flow_uniform_static_ratio_shift_input")
        self.flow_uniform_static_ratio_shift_input.setMaximum(100.000000000000000)
        self.flow_uniform_static_ratio_shift_input.setSingleStep(0.100000000000000)
        self.flow_uniform_static_ratio_shift_input.setValue(2.000000000000000)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.flow_uniform_static_ratio_shift_input)

        self.flow_optimal_transport_enable = QCheckBox(self.flow_model_settings_box)
        self.flow_optimal_transport_enable.setObjectName(u"flow_optimal_transport_enable")
        self.flow_optimal_transport_enable.setChecked(True)

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.SpanningRole, self.flow_optimal_transport_enable)


        self.formLayout_7.setLayout(0, QFormLayout.ItemRole.LabelRole, self.formLayout_3)


        self.verticalLayout.addLayout(self.formLayout_7)


        self.verticalLayout_2.addWidget(self.flow_model_settings_box)

        self.advanced_vae_settings_box = QGroupBox(base_args_ui)
        self.advanced_vae_settings_box.setObjectName(u"advanced_vae_settings_box")
        self.advanced_vae_settings_box.setCheckable(False)
        self.verticalLayout_3 = QVBoxLayout(self.advanced_vae_settings_box)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.advanced_vae_settings_formLayout = QFormLayout()
        self.advanced_vae_settings_formLayout.setObjectName(u"advanced_vae_settings_formLayout")
        self.formLayout_5 = QFormLayout()
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.formLayout_5.setContentsMargins(-1, -1, 3, -1)
        self.vae_batch_size_label = QLabel(self.advanced_vae_settings_box)
        self.vae_batch_size_label.setObjectName(u"vae_batch_size_label")

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.LabelRole, self.vae_batch_size_label)

        self.vae_batch_size_input = SpinBox(self.advanced_vae_settings_box)
        self.vae_batch_size_input.setObjectName(u"vae_batch_size_input")
        self.vae_batch_size_input.setMinimum(1)
        self.vae_batch_size_input.setMaximum(100)

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.FieldRole, self.vae_batch_size_input)

        self.vae_reflection_enable = QCheckBox(self.advanced_vae_settings_box)
        self.vae_reflection_enable.setObjectName(u"vae_reflection_enable")

        self.formLayout_5.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.vae_reflection_enable)


        self.advanced_vae_settings_formLayout.setLayout(0, QFormLayout.ItemRole.LabelRole, self.formLayout_5)

        self.formLayout_6 = QFormLayout()
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.formLayout_6.setContentsMargins(3, -1, -1, -1)
        self.vae_custom_scale_enable = QCheckBox(self.advanced_vae_settings_box)
        self.vae_custom_scale_enable.setObjectName(u"vae_custom_scale_enable")

        self.formLayout_6.setWidget(0, QFormLayout.ItemRole.LabelRole, self.vae_custom_scale_enable)

        self.vae_custom_scale_input = DoubleSpinBox(self.advanced_vae_settings_box)
        self.vae_custom_scale_input.setObjectName(u"vae_custom_scale_input")
        self.vae_custom_scale_input.setEnabled(False)

        self.formLayout_6.setWidget(0, QFormLayout.ItemRole.FieldRole, self.vae_custom_scale_input)

        self.vae_custom_shift_enable = QCheckBox(self.advanced_vae_settings_box)
        self.vae_custom_shift_enable.setObjectName(u"vae_custom_shift_enable")

        self.formLayout_6.setWidget(1, QFormLayout.ItemRole.LabelRole, self.vae_custom_shift_enable)

        self.vae_custom_shift_input = DoubleSpinBox(self.advanced_vae_settings_box)
        self.vae_custom_shift_input.setObjectName(u"vae_custom_shift_input")
        self.vae_custom_shift_input.setEnabled(False)

        self.formLayout_6.setWidget(1, QFormLayout.ItemRole.FieldRole, self.vae_custom_shift_input)


        self.advanced_vae_settings_formLayout.setLayout(0, QFormLayout.ItemRole.FieldRole, self.formLayout_6)


        self.verticalLayout_3.addLayout(self.advanced_vae_settings_formLayout)


        self.verticalLayout_2.addWidget(self.advanced_vae_settings_box)

        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_8 = QFormLayout()
        self.formLayout_8.setObjectName(u"formLayout_8")
        self.zero_cond_dropout_enable = QCheckBox(base_args_ui)
        self.zero_cond_dropout_enable.setObjectName(u"zero_cond_dropout_enable")

        self.formLayout_8.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.zero_cond_dropout_enable)

        self.cfm_enable = QCheckBox(base_args_ui)
        self.cfm_enable.setObjectName(u"cfm_enable")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfm_enable.sizePolicy().hasHeightForWidth())
        self.cfm_enable.setSizePolicy(sizePolicy)

        self.formLayout_8.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.cfm_enable)


        self.formLayout_4.setLayout(0, QFormLayout.ItemRole.LabelRole, self.formLayout_8)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.cfm_lambda_enable = QCheckBox(base_args_ui)
        self.cfm_lambda_enable.setObjectName(u"cfm_lambda_enable")
        self.cfm_lambda_enable.setEnabled(False)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.cfm_lambda_enable)

        self.cfm_lambda_input = DoubleSpinBox(base_args_ui)
        self.cfm_lambda_input.setObjectName(u"cfm_lambda_input")
        self.cfm_lambda_input.setEnabled(False)
        self.cfm_lambda_input.setMaximum(100.000000000000000)
        self.cfm_lambda_input.setSingleStep(0.001000000000000)
        self.cfm_lambda_input.setValue(0.050000000000000)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cfm_lambda_input)


        self.formLayout_4.setLayout(0, QFormLayout.ItemRole.FieldRole, self.formLayout)


        self.verticalLayout_2.addLayout(self.formLayout_4)


        self.retranslateUi(base_args_ui)

        QMetaObject.connectSlotsByName(base_args_ui)
    # setupUi

    def retranslateUi(self, base_args_ui):
        base_args_ui.setWindowTitle(QCoreApplication.translate("base_args_ui", u"Form", None))
        self.experimental_args_notice_label.setText(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>This section contains some less commonly used and/or advanced/experimental settings.<br/>Usually there is no need to enable these unless you know what you are doing.<br/>Do not rely on the defaults.</p></body></html>", None))
        self.flow_model_settings_box.setTitle(QCoreApplication.translate("base_args_ui", u"Flow Model", None))
        self.flow_notice_label.setText(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Experimental Rectified Flow settings, incompatible with V Param; Enables <code>--flow_model</code><br/>Made with SDXL-based NoobAI-RF models by <a href=\"https://huggingface.co/CabalResearch\"><span style=\" text-decoration: underline; color:#00d9cb;\">CabalResearch</span></a> in mind.<br/>(For Flux.1 training please visit the corresponding section)</p></body></html>", None))
        self.label.setText(QCoreApplication.translate("base_args_ui", u"Logit Mean", None))
        self.label_2.setText(QCoreApplication.translate("base_args_ui", u"Logit std", None))
        self.label_4.setText(QCoreApplication.translate("base_args_ui", u"Timestep Distribution", None))
        self.flow_timestep_distribution_selector.setItemText(0, QCoreApplication.translate("base_args_ui", u"logit_normal", None))
        self.flow_timestep_distribution_selector.setItemText(1, QCoreApplication.translate("base_args_ui", u"uniform", None))

        self.label_8.setText(QCoreApplication.translate("base_args_ui", u"Uniform Static Shift", None))
#if QT_CONFIG(tooltip)
        self.flow_optimal_transport_enable.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Pair latents and noise with cosine optimal transport when using Rectified Flow</p><p><code>--flow_use_ot</code></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.flow_optimal_transport_enable.setText(QCoreApplication.translate("base_args_ui", u"Optimal Transport", None))
        self.advanced_vae_settings_box.setTitle(QCoreApplication.translate("base_args_ui", u"Advanced VAE settings", None))
        self.vae_batch_size_label.setText(QCoreApplication.translate("base_args_ui", u"VAE Batch Size", None))
#if QT_CONFIG(tooltip)
        self.vae_reflection_enable.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Only applicable to models and VAEs that were trained together with reflect padding.</p><p>Uses reflect padding to mirror image edges in the conv layers of the VAE which helps avoiding edge artifacts.<br/>If you don't know what this is, you can likely ignore it</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.vae_reflection_enable.setText(QCoreApplication.translate("base_args_ui", u"VAE Reflection", None))
        self.vae_custom_scale_enable.setText(QCoreApplication.translate("base_args_ui", u"VAE Custom Scale", None))
        self.vae_custom_shift_enable.setText(QCoreApplication.translate("base_args_ui", u"VAE Custom Shift", None))
        self.zero_cond_dropout_enable.setText(QCoreApplication.translate("base_args_ui", u"Zero Conditioning Dropout", None))
        self.cfm_enable.setText(QCoreApplication.translate("base_args_ui", u"Contrastive Flow Matching", None))
        self.cfm_lambda_enable.setText(QCoreApplication.translate("base_args_ui", u"Contrastive Flow Matching Lamdba", None))
    # retranslateUi

