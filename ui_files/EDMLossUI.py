# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EDMLossUI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

from modules.DragDropLineEdit import DragDropLineEdit
from modules.LineEditHighlight import LineEditWithHighlight
from modules.ScrollOnSelect import (DoubleSpinBox, SpinBox)
class Ui_edm_loss_UI(object):
    def setupUi(self, edm_loss_UI):
        if not edm_loss_UI.objectName():
            edm_loss_UI.setObjectName(u"edm_loss_UI")
        edm_loss_UI.resize(600, 400)
        self.verticalLayout = QVBoxLayout(edm_loss_UI)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.enable_checkbox = QCheckBox(edm_loss_UI)
        self.enable_checkbox.setObjectName(u"enable_checkbox")

        self.verticalLayout.addWidget(self.enable_checkbox)

        self.optimizer_group = QGroupBox(edm_loss_UI)
        self.optimizer_group.setObjectName(u"optimizer_group")
        self.formLayout = QFormLayout(self.optimizer_group)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.optimizer_group)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.optimizer_type_input = LineEditWithHighlight(self.optimizer_group)
        self.optimizer_type_input.setObjectName(u"optimizer_type_input")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.optimizer_type_input)

        self.label1 = QLabel(self.optimizer_group)
        self.label1.setObjectName(u"label1")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label1)

        self.lr_input = LineEditWithHighlight(self.optimizer_group)
        self.lr_input.setObjectName(u"lr_input")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lr_input)

        self.label2 = QLabel(self.optimizer_group)
        self.label2.setObjectName(u"label2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label2)

        self.optimizer_args_input = LineEditWithHighlight(self.optimizer_group)
        self.optimizer_args_input.setObjectName(u"optimizer_args_input")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.optimizer_args_input)

        self.verticalLayout.addWidget(self.optimizer_group)

        self.scheduler_group = QGroupBox(edm_loss_UI)
        self.scheduler_group.setObjectName(u"scheduler_group")
        self.formLayout_2 = QFormLayout(self.scheduler_group)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.scheduler_enable = QCheckBox(self.scheduler_group)
        self.scheduler_enable.setObjectName(u"scheduler_enable")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.scheduler_enable)

        self.label4 = QLabel(self.scheduler_group)
        self.label4.setObjectName(u"label4")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label4)

        self.warmup_input = DoubleSpinBox(self.scheduler_group)
        self.warmup_input.setObjectName(u"warmup_input")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.warmup_input)

        self.label5 = QLabel(self.scheduler_group)
        self.label5.setObjectName(u"label5")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label5)

        self.constant_input = DoubleSpinBox(self.scheduler_group)
        self.constant_input.setObjectName(u"constant_input")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.constant_input)


        self.verticalLayout.addWidget(self.scheduler_group)

        self.advanced_group = QGroupBox(edm_loss_UI)
        self.advanced_group.setObjectName(u"advanced_group")
        self.formLayout_3 = QFormLayout(self.advanced_group)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label6 = QLabel(self.advanced_group)
        self.label6.setObjectName(u"label6")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label6)

        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.initial_weights_input = DragDropLineEdit(self.advanced_group)
        self.initial_weights_input.setObjectName(u"initial_weights_input")

        self.hboxLayout.addWidget(self.initial_weights_input)

        self.initial_weights_button = QPushButton(self.advanced_group)
        self.initial_weights_button.setObjectName(u"initial_weights_button")

        self.hboxLayout.addWidget(self.initial_weights_button)


        self.formLayout_3.setLayout(0, QFormLayout.FieldRole, self.hboxLayout)

        self.label7 = QLabel(self.advanced_group)
        self.label7.setObjectName(u"label7")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label7)

        self.num_channels_input = SpinBox(self.advanced_group)
        self.num_channels_input.setObjectName(u"num_channels_input")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.num_channels_input)


        self.verticalLayout.addWidget(self.advanced_group)

        self.graph_group = QGroupBox(edm_loss_UI)
        self.graph_group.setObjectName(u"graph_group")
        self.formLayout_4 = QFormLayout(self.graph_group)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.generate_graph_enable = QCheckBox(self.graph_group)
        self.generate_graph_enable.setObjectName(u"generate_graph_enable")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.generate_graph_enable)

        self.label8 = QLabel(self.graph_group)
        self.label8.setObjectName(u"label8")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label8)

        self.hboxLayout1 = QHBoxLayout()
        self.hboxLayout1.setObjectName(u"hboxLayout1")
        self.graph_output_input = DragDropLineEdit(self.graph_group)
        self.graph_output_input.setObjectName(u"graph_output_input")

        self.hboxLayout1.addWidget(self.graph_output_input)

        self.graph_output_button = QPushButton(self.graph_group)
        self.graph_output_button.setObjectName(u"graph_output_button")

        self.hboxLayout1.addWidget(self.graph_output_button)


        self.formLayout_4.setLayout(1, QFormLayout.FieldRole, self.hboxLayout1)

        self.label9 = QLabel(self.graph_group)
        self.label9.setObjectName(u"label9")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.label9)

        self.graph_steps_input = SpinBox(self.graph_group)
        self.graph_steps_input.setObjectName(u"graph_steps_input")

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.graph_steps_input)

        self.label10 = QLabel(self.graph_group)
        self.label10.setObjectName(u"label10")

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.label10)

        self.graph_y_limit_input = SpinBox(self.graph_group)
        self.graph_y_limit_input.setObjectName(u"graph_y_limit_input")

        self.formLayout_4.setWidget(3, QFormLayout.FieldRole, self.graph_y_limit_input)


        self.verticalLayout.addWidget(self.graph_group)


        self.retranslateUi(edm_loss_UI)

        QMetaObject.connectSlotsByName(edm_loss_UI)
    # setupUi

    def retranslateUi(self, edm_loss_UI):
        self.enable_checkbox.setText(QCoreApplication.translate("edm_loss_UI", u"Enable EDM\u00b2 Loss Weighting", None))
        self.optimizer_group.setTitle(QCoreApplication.translate("edm_loss_UI", u"Optimizer Settings", None))
        self.label.setText(QCoreApplication.translate("edm_loss_UI", u"Optimizer Type:", None))
        self.label1.setText(QCoreApplication.translate("edm_loss_UI", u"Learning Rate:", None))
        self.label2.setText(QCoreApplication.translate("edm_loss_UI", u"Optimizer Args:", None))
        self.scheduler_group.setTitle(QCoreApplication.translate("edm_loss_UI", u"Learning Rate Scheduler", None))
        self.scheduler_enable.setText(QCoreApplication.translate("edm_loss_UI", u"Enable Scheduler", None))
        self.label4.setText(QCoreApplication.translate("edm_loss_UI", u"Warmup %:", None))
        self.label5.setText(QCoreApplication.translate("edm_loss_UI", u"Constant %:", None))
        self.advanced_group.setTitle(QCoreApplication.translate("edm_loss_UI", u"Advanced Settings", None))
        self.label6.setText(QCoreApplication.translate("edm_loss_UI", u"Initial Weights:", None))
        self.initial_weights_button.setText("")
        self.label7.setText(QCoreApplication.translate("edm_loss_UI", u"Num Channels:", None))
        self.graph_group.setTitle(QCoreApplication.translate("edm_loss_UI", u"Graph Settings", None))
        self.generate_graph_enable.setText(QCoreApplication.translate("edm_loss_UI", u"Generate Graph", None))
        self.label8.setText(QCoreApplication.translate("edm_loss_UI", u"Graph Output:", None))
        self.graph_output_button.setText("")
        self.label9.setText(QCoreApplication.translate("edm_loss_UI", u"Every X Steps:", None))
        self.label10.setText(QCoreApplication.translate("edm_loss_UI", u"Y Limit:", None))
        pass
    # retranslateUi

