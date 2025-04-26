# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoggingUI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
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
from modules.ScrollOnSelect import ComboBox # Keep ComboBox import

class Ui_logging_ui(object):
    def setupUi(self, logging_ui):
        if not logging_ui.objectName():
            logging_ui.setObjectName(u"logging_ui")
        # Increased height slightly to accommodate the change
        logging_ui.resize(440, 230)
        logging_ui.setMinimumSize(QSize(440, 0))
        self.verticalLayout = QVBoxLayout(logging_ui)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.logging_group = QGroupBox(logging_ui)
        self.logging_group.setObjectName(u"logging_group")
        self.logging_group.setCheckable(True)
        self.logging_group.setChecked(False)
        self.formLayout = QFormLayout(self.logging_group)
        self.formLayout.setObjectName(u"formLayout")

        # Row 0: Logging System
        self.label_2 = QLabel(self.logging_group)
        self.label_2.setObjectName(u"label_2")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.log_mode_selector = ComboBox(self.logging_group)
        self.log_mode_selector.addItem(QCoreApplication.translate("logging_ui", u"Tensorboard", None))
        self.log_mode_selector.addItem(QCoreApplication.translate("logging_ui", u"Wandb", None))
        self.log_mode_selector.addItem(QCoreApplication.translate("logging_ui", u"All", None))
        self.log_mode_selector.setObjectName(u"log_mode_selector")
        self.log_mode_selector.setFocusPolicy(Qt.StrongFocus)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.log_mode_selector)

        # Row 1: Log Output Directory
        self.label = QLabel(self.logging_group)
        self.label.setObjectName(u"label")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.log_output_input = DragDropLineEdit(self.logging_group)
        self.log_output_input.setObjectName(u"log_output_input")
        self.horizontalLayout.addWidget(self.log_output_input)

        self.log_output_selector = QPushButton(self.logging_group)
        self.log_output_selector.setObjectName(u"log_output_selector")
        self.horizontalLayout.addWidget(self.log_output_selector)
        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)

        # Row 2: Log Prefix Mode (NEW)
        self.log_prefix_mode_label = QLabel(self.logging_group)
        self.log_prefix_mode_label.setObjectName(u"log_prefix_mode_label")
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.log_prefix_mode_label)

        self.log_prefix_mode_selector = ComboBox(self.logging_group)
        self.log_prefix_mode_selector.addItem(QCoreApplication.translate("logging_ui", u"Disabled", None))
        self.log_prefix_mode_selector.addItem(QCoreApplication.translate("logging_ui", u"Manual", None))
        self.log_prefix_mode_selector.addItem(QCoreApplication.translate("logging_ui", u"Output Name", None))
        self.log_prefix_mode_selector.setObjectName(u"log_prefix_mode_selector")
        self.log_prefix_mode_selector.setFocusPolicy(Qt.StrongFocus)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.log_prefix_mode_selector)

        # Row 3: Manual Log Prefix (Previously Row 2 Field)
        self.manual_log_prefix_label = QLabel(self.logging_group) # Optional: Add label for clarity
        self.manual_log_prefix_label.setObjectName(u"manual_log_prefix_label")
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.manual_log_prefix_label)

        self.log_prefix_input = LineEditWithHighlight(self.logging_group)
        self.log_prefix_input.setObjectName(u"log_prefix_input")
        # Start disabled, enabled only when "Manual" mode is selected
        self.log_prefix_input.setEnabled(False)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.log_prefix_input)


        # Row 4: Log Tracker Name (Shifted down)
        self.log_tracker_name_enable = QCheckBox(self.logging_group)
        self.log_tracker_name_enable.setObjectName(u"log_tracker_name_enable")
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.log_tracker_name_enable)

        self.log_tracker_name_input = LineEditWithHighlight(self.logging_group)
        self.log_tracker_name_input.setObjectName(u"log_tracker_name_input")
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.log_tracker_name_input)


        # Row 5: Wandb API Key (Shifted down)
        self.label_5 = QLabel(self.logging_group)
        self.label_5.setObjectName(u"label_5")
        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_5)

        self.log_wandb_key_input = LineEditWithHighlight(self.logging_group)
        self.log_wandb_key_input.setObjectName(u"log_wandb_key_input")
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.log_wandb_key_input)

        # Removed: self.log_prefix_enable (QCheckBox)

        self.verticalLayout.addWidget(self.logging_group)

        self.retranslateUi(logging_ui)

        QMetaObject.connectSlotsByName(logging_ui)
    # setupUi

    def retranslateUi(self, logging_ui):
        logging_ui.setWindowTitle(QCoreApplication.translate("logging_ui", u"Form", None))
        self.logging_group.setTitle(QCoreApplication.translate("logging_ui", u"Enable", None))

        # Row 0: Logging System
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Logging System is the system that is used to log values such as LRs and loss</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("logging_ui", u"Logging System", None))
#if QT_CONFIG(tooltip)
        self.log_mode_selector.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Logging System is the system that is used to log values such as LRs and loss</p></body></html>", None))
#endif // QT_CONFIG(tooltip)

        # Row 1: Log Output Directory
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Log Output Directory is the location the logging folder will be placed at. Note that this is not going to be created if you are logging with wandb</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("logging_ui", u"Log Output Directory", None))
#if QT_CONFIG(tooltip)
        self.log_output_input.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Log Output Directory is the location the logging folder will be placed at. Note that this is not going to be created if you are logging with wandb</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.log_output_input.setPlaceholderText(QCoreApplication.translate("logging_ui", u"Output Directory", None))
#if QT_CONFIG(tooltip)
        self.log_output_selector.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Log Output Directory is the location the logging folder will be placed at. Note that this is not going to be created if you are logging with wandb</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.log_output_selector.setText("")

        # Row 2: Log Prefix Mode (NEW)
#if QT_CONFIG(tooltip)
        self.log_prefix_mode_label.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Determines how the log folder prefix is set.</p><p>- Disabled: No prefix is used.</p><p>- Manual: Use the prefix entered below.</p><p>- Output Name: Use the 'Output Name' specified in the Saving Args section (if provided).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.log_prefix_mode_label.setText(QCoreApplication.translate("logging_ui", u"Log Prefix Mode", None))
#if QT_CONFIG(tooltip)
        self.log_prefix_mode_selector.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Determines how the log folder prefix is set.</p><p>- Disabled: No prefix is used.</p><p>- Manual: Use the prefix entered below.</p><p>- Output Name: Use the 'Output Name' specified in the Saving Args section (if provided).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)

        # Row 3: Manual Log Prefix
#if QT_CONFIG(tooltip)
        self.manual_log_prefix_label.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Prefix For Log Folders prepends the log directory with a user provided prefix. Typically this is used to allow for an easier time differentiating different runs. Only used when 'Log Prefix Mode' is set to 'Manual'.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.manual_log_prefix_label.setText(QCoreApplication.translate("logging_ui", u"Manual Prefix", None)) # Label text
#if QT_CONFIG(tooltip)
        self.log_prefix_input.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Prefix For Log Folders prepends the log directory with a user provided prefix. Typically this is used to allow for an easier time differentiating different runs. Only used when 'Log Prefix Mode' is set to 'Manual'.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.log_prefix_input.setPlaceholderText(QCoreApplication.translate("logging_ui", u"Prefix (Manual Mode)", None)) # Updated placeholder

        # Row 4: Log Tracker Name
#if QT_CONFIG(tooltip)
        self.log_tracker_name_enable.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Name For Log Tracker is the name of the log tracker.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.log_tracker_name_enable.setText(QCoreApplication.translate("logging_ui", u"Name For Log Tracker", None))
#if QT_CONFIG(tooltip)
        self.log_tracker_name_input.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Name For Log Tracker is the name of the log tracker.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.log_tracker_name_input.setPlaceholderText(QCoreApplication.translate("logging_ui", u"Tracker Name", None))

        # Row 5: Wandb API Key
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Wandb API Key is a required field so that sd-scripts is able to interface with your Wandb account to log to it, without this key, it cannot log to Wandb</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("logging_ui", u"Wandb API Key", None))
#if QT_CONFIG(tooltip)
        self.log_wandb_key_input.setToolTip(QCoreApplication.translate("logging_ui", u"<html><head/><body><p>Wandb API Key is a required field so that sd-scripts is able to interface with your Wandb account to log to it, without this key, it cannot log to Wandb</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.log_wandb_key_input.setPlaceholderText(QCoreApplication.translate("logging_ui", u"API Key", None))

        # Removed retranslate for log_prefix_enable

    # retranslateUi

