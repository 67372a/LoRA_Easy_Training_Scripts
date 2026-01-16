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

from modules.ScrollOnSelect import (ComboBox, DoubleSpinBox)

class Ui_base_args_ui(object):
    def setupUi(self, base_args_ui):
        if not base_args_ui.objectName():
            base_args_ui.setObjectName(u"base_args_ui")
        base_args_ui.resize(749, 663)
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
        self.experimental_args_notice_label.setOpenExternalLinks(True)

        self.misc_experimental_args_tab_notice.addWidget(self.experimental_args_notice_label)


        self.verticalLayout_2.addLayout(self.misc_experimental_args_tab_notice)

        self.flow_model_settings_group = QGroupBox(base_args_ui)
        self.flow_model_settings_group.setObjectName(u"flow_model_settings_group")
        self.flow_model_settings_group.setEnabled(True)
        self.flow_model_settings_group.setFlat(True)
        self.flow_model_settings_group.setCheckable(True)
        self.flow_model_settings_group.setChecked(False)
        self.verticalLayout = QVBoxLayout(self.flow_model_settings_group)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.line_2 = QFrame(self.flow_model_settings_group)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.flow_notice_label = QLabel(self.flow_model_settings_group)
        self.flow_notice_label.setObjectName(u"flow_notice_label")
        self.flow_notice_label.setWordWrap(True)
        self.flow_notice_label.setOpenExternalLinks(False)

        self.horizontalLayout.addWidget(self.flow_notice_label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(-1, -1, 3, -1)
        self.label_4 = QLabel(self.flow_model_settings_group)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.flow_timestep_distribution_selector = ComboBox(self.flow_model_settings_group)
        self.flow_timestep_distribution_selector.addItem("")
        self.flow_timestep_distribution_selector.addItem("")
        self.flow_timestep_distribution_selector.setObjectName(u"flow_timestep_distribution_selector")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.flow_timestep_distribution_selector)

        self.label_8 = QLabel(self.flow_model_settings_group)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.flow_unfirom_static_ratio_shift_selector = DoubleSpinBox(self.flow_model_settings_group)
        self.flow_unfirom_static_ratio_shift_selector.setObjectName(u"flow_unfirom_static_ratio_shift_selector")
        self.flow_unfirom_static_ratio_shift_selector.setMaximum(100.000000000000000)
        self.flow_unfirom_static_ratio_shift_selector.setSingleStep(0.100000000000000)
        self.flow_unfirom_static_ratio_shift_selector.setValue(2.000000000000000)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.flow_unfirom_static_ratio_shift_selector)


        self.horizontalLayout_2.addLayout(self.formLayout_3)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(3, -1, -1, -1)
        self.label = QLabel(self.flow_model_settings_group)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.flow_logit_mean_selector = DoubleSpinBox(self.flow_model_settings_group)
        self.flow_logit_mean_selector.setObjectName(u"flow_logit_mean_selector")
        self.flow_logit_mean_selector.setMinimum(-100.000000000000000)
        self.flow_logit_mean_selector.setMaximum(100.000000000000000)
        self.flow_logit_mean_selector.setSingleStep(0.100000000000000)
        self.flow_logit_mean_selector.setValue(0.000000000000000)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.flow_logit_mean_selector)

        self.label_2 = QLabel(self.flow_model_settings_group)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.flow_logit_std_selector = DoubleSpinBox(self.flow_model_settings_group)
        self.flow_logit_std_selector.setObjectName(u"flow_logit_std_selector")
        self.flow_logit_std_selector.setMaximum(100.000000000000000)
        self.flow_logit_std_selector.setSingleStep(0.100000000000000)
        self.flow_logit_std_selector.setValue(1.000000000000000)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.flow_logit_std_selector)


        self.horizontalLayout_2.addLayout(self.formLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.flow_optimal_transport_enable = QCheckBox(self.flow_model_settings_group)
        self.flow_optimal_transport_enable.setObjectName(u"flow_optimal_transport_enable")
        self.flow_optimal_transport_enable.setChecked(True)

        self.verticalLayout.addWidget(self.flow_optimal_transport_enable)


        self.verticalLayout_2.addWidget(self.flow_model_settings_group)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.flow_cfm_enable = QCheckBox(base_args_ui)
        self.flow_cfm_enable.setObjectName(u"flow_cfm_enable")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.flow_cfm_enable.sizePolicy().hasHeightForWidth())
        self.flow_cfm_enable.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.flow_cfm_enable)

        self.line_3 = QFrame(base_args_ui)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line_3)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.checkBox = QCheckBox(base_args_ui)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setEnabled(False)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.checkBox)

        self.doubleSpinBox = DoubleSpinBox(base_args_ui)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setEnabled(False)
        self.doubleSpinBox.setMaximum(100.000000000000000)
        self.doubleSpinBox.setSingleStep(0.001000000000000)
        self.doubleSpinBox.setValue(0.050000000000000)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.doubleSpinBox)


        self.horizontalLayout_4.addLayout(self.formLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.groupBox = QGroupBox(base_args_ui)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setCheckable(True)
        self.vae_reflection_enable = QCheckBox(self.groupBox)
        self.vae_reflection_enable.setObjectName(u"vae_reflection_enable")
        self.vae_reflection_enable.setGeometry(QRect(130, 40, 261, 31))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.vae_reflection_enable.sizePolicy().hasHeightForWidth())
        self.vae_reflection_enable.setSizePolicy(sizePolicy1)
        self.checkBox_2 = QCheckBox(self.groupBox)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(270, 40, 121, 21))
        self.checkBox_3 = QCheckBox(self.groupBox)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(420, 30, 141, 21))

        self.verticalLayout_2.addWidget(self.groupBox)

        self.checkBox_4 = QCheckBox(base_args_ui)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.verticalLayout_2.addWidget(self.checkBox_4)


        self.retranslateUi(base_args_ui)

        QMetaObject.connectSlotsByName(base_args_ui)
    # setupUi

    def retranslateUi(self, base_args_ui):
        base_args_ui.setWindowTitle(QCoreApplication.translate("base_args_ui", u"Form", None))
        self.experimental_args_notice_label.setText(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>This section contains some less commonly used and/or advanced/experimental settings.<br/>Usually there is no need to enable these unless you know what you are doing.<br/>Do not rely on the defaults.</p></body></html>", None))
        self.flow_model_settings_group.setTitle(QCoreApplication.translate("base_args_ui", u"Flow Model", None))
        self.flow_notice_label.setText(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Experimental Rectified Flow settings, incompatible with V Param; Enables <span style=\" font-family:'JetBrainsMono Nerd Font';\">--flow_model</span><br/>Made with SDXL-based NoobAI-RF models by <a href=\"https://huggingface.co/CabalResearch\"><span style=\" text-decoration: underline; color:#00d9cb;\">CabalResearch</span></a> in mind.</p><p>For Flux.1 training please visit the corresponding section.</p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("base_args_ui", u"Timestep Distribution", None))
        self.flow_timestep_distribution_selector.setItemText(0, QCoreApplication.translate("base_args_ui", u"logit_normal", None))
        self.flow_timestep_distribution_selector.setItemText(1, QCoreApplication.translate("base_args_ui", u"uniform", None))

        self.label_8.setText(QCoreApplication.translate("base_args_ui", u"Uniform Static Shift", None))
        self.label.setText(QCoreApplication.translate("base_args_ui", u"Logit Mean", None))
        self.label_2.setText(QCoreApplication.translate("base_args_ui", u"Logit std", None))
#if QT_CONFIG(tooltip)
        self.flow_optimal_transport_enable.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Pair latents and noise with cosine optimal transport when using Rectified Flow</p><p><code>--flow_use_ot</code></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.flow_optimal_transport_enable.setText(QCoreApplication.translate("base_args_ui", u"Optimal Transport", None))
        self.flow_cfm_enable.setText(QCoreApplication.translate("base_args_ui", u"Contrastive Flow Matching", None))
        self.checkBox.setText(QCoreApplication.translate("base_args_ui", u"Contrastive Flow Matching Lamdba", None))
        self.groupBox.setTitle(QCoreApplication.translate("base_args_ui", u"Advanced VAE settings", None))
#if QT_CONFIG(tooltip)
        self.vae_reflection_enable.setToolTip(QCoreApplication.translate("base_args_ui", u"<html><head/><body><p>Only applicable to models and VAEs that were trained together with reflect padding.</p><p>Uses reflect padding to mirror image edges in the conv layers of the VAE which helps avoiding edge artifacts.<br/>If you don't know what this is, you can likely ignore it</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.vae_reflection_enable.setText(QCoreApplication.translate("base_args_ui", u"VAE Reflection", None))
        self.checkBox_2.setText(QCoreApplication.translate("base_args_ui", u"VAE Custom Shift", None))
        self.checkBox_3.setText(QCoreApplication.translate("base_args_ui", u"VAE Custom Scale", None))
        self.checkBox_4.setText(QCoreApplication.translate("base_args_ui", u"Zero Conditioning Dropout", None))
    # retranslateUi

