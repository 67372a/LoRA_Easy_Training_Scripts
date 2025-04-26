from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QComboBox # Import QComboBox
from modules.DragDropLineEdit import DragDropLineEdit
from modules.LineEditHighlight import LineEditWithHighlight
from ui_files.LoggingUI import Ui_logging_ui
from modules.BaseWidget import BaseWidget
from pathlib import Path


class LoggingWidget(BaseWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Logging Args")
        self.widget = Ui_logging_ui()

        self.name = "logging_args"
        # Default log_prefix_mode to disabled
        self.args = {"log_prefix_mode": "disabled"}

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)
        self.widget.log_output_input.setMode("folder")
        self.widget.log_output_input.highlight = True
        self.widget.log_wandb_key_input.setEnabled(False)
        self.widget.log_prefix_input.setEnabled(False)
        self.widget.log_tracker_name_input.setEnabled(False)
        self.widget.log_output_selector.setIcon(
            QIcon(str(Path("icons/more-horizontal.svg")))
        )

    def setup_connections(self) -> None:
        self.widget.logging_group.clicked.connect(self.enable_disable)
        self.widget.log_mode_selector.currentIndexChanged.connect(
            self.change_log_system
        )
        self.widget.log_output_input.textChanged.connect(
            lambda x: self.edit_args("logging_dir", x)
        )
        self.widget.log_output_input.editingFinished.connect(
            lambda: self.check_validity(self.widget.log_output_input)
        )
        self.widget.log_output_selector.clicked.connect(
            lambda: self.set_folder_from_dialog(
                self.widget.log_output_input, "Open Logging Directory"
            )
        )
        self.widget.log_prefix_mode_selector.currentIndexChanged.connect(
            self.change_log_prefix_mode
        )
        self.widget.log_prefix_input.textChanged.connect(
            self.update_manual_log_prefix
        )

        self.widget.log_tracker_name_enable.clicked.connect(
            lambda x: self.enable_disable_lineEdit(
                x, self.widget.log_tracker_name_input, "log_tracker_name"
            )
        )
        self.widget.log_tracker_name_input.textChanged.connect(
            lambda x: self.edit_args("log_tracker_name", x, True)
        )
        self.widget.log_wandb_key_input.textChanged.connect(
            lambda x: self.edit_args("wandb_api_key", x)
        )

    def check_validity(self, elem: DragDropLineEdit) -> None:
        elem.dirty = True
        if not elem.allow_empty or elem.text() != "":
            elem.update_stylesheet()
        else:
            elem.setStyleSheet("")

    @Slot(bool)
    def enable_disable(self, checked: bool) -> None:
        # Clear relevant args when disabled
        if not checked:
            self.args = {}
            self.widget.log_output_input.setStyleSheet("")
            # Ensure prefix input is disabled and args cleared
            self.widget.log_prefix_input.setEnabled(False)
            # Reset prefix mode selector to default (Disabled)
            self.widget.log_prefix_mode_selector.setCurrentIndex(0)
            return

        # Re-populate args based on current UI state when enabled
        self.edit_args("logging_dir", self.widget.log_output_input.text())
        # Apply prefix mode logic
        self.change_log_prefix_mode(self.widget.log_prefix_mode_selector.currentIndex())
        # Apply tracker name logic
        if self.widget.log_tracker_name_enable.isChecked():
            self.enable_disable_lineEdit(
                True, self.widget.log_tracker_name_input, "log_tracker_name"
            )
        self.change_log_system(self.widget.log_mode_selector.currentIndex())
        if self.widget.log_output_input.dirty:
            self.widget.log_output_input.update_stylesheet()

    @Slot(int)
    def change_log_prefix_mode(self, index: int) -> None:
        """Handles changes in the log_prefix_mode_selector."""
        mode = self.widget.log_prefix_mode_selector.currentText().lower().replace(" ", "_")
        self.edit_args("log_prefix_mode", mode, True)

        is_manual_mode = (mode == "manual")
        self.widget.log_prefix_input.setEnabled(is_manual_mode)

        # Clear log_prefix arg if not in manual mode
        if "log_prefix" in self.args and not is_manual_mode:
            del self.args["log_prefix"]
        # If switching to manual, add the current input value to args
        elif is_manual_mode:
            self.update_manual_log_prefix(self.widget.log_prefix_input.text())

    @Slot(str)
    def update_manual_log_prefix(self, text: str) -> None:
        """Updates the log_prefix arg only if the mode is Manual."""
        if self.widget.log_prefix_mode_selector.currentText() == "Manual":
            self.edit_args("log_prefix", text, True)
        # If mode is not Manual but text changes (e.g., user typed then changed mode),
        # ensure log_prefix is not in args (handled by change_log_prefix_mode)

    def change_log_system(self, index: int) -> None:
        if "wandb_api_key" in self.args:
            del self.args["wandb_api_key"]
        is_wandb_or_all = (index != 0) # 0 = Tensorboard, 1 = Wandb, 2 = All
        self.widget.log_wandb_key_input.setEnabled(is_wandb_or_all)
        self.edit_args(
            "wandb_api_key",
            self.widget.log_wandb_key_input.text() if is_wandb_or_all else None,
            True,
        )
        self.edit_args(
            "log_with", self.widget.log_mode_selector.currentText().lower(), True
        )

    def enable_disable_lineEdit(
        self, checked: bool, elem: LineEditWithHighlight, name: str
    ) -> None:
        elem.setEnabled(checked)
        self.edit_args(name, elem.text() if checked else None, True)

    def load_args(self, args: dict) -> bool:
        args_logging: dict = args.get(self.name, {})

        # update element inputs
        self.widget.logging_group.setChecked(bool(args_logging.get("log_with", False)))
        self.widget.log_mode_selector.setCurrentText(
            args_logging.get("log_with", "tensorboard").capitalize()
        )
        self.widget.log_output_input.setText(args_logging.get("logging_dir", ""))

        self.widget.log_prefix_mode_selector.setCurrentText(args_logging.get("log_prefix_mode", "disabled").replace("_", " ").title())
        self.widget.log_prefix_input.setText(args_logging.get("log_prefix", ""))

        self.widget.log_tracker_name_enable.setChecked("log_tracker_name" in args_logging)
        self.widget.log_tracker_name_input.setText(args_logging.get("log_tracker_name", ""))
        self.widget.log_wandb_key_input.setText(args_logging.get("wandb_api_key", ""))

        self.enable_disable(self.widget.logging_group.isChecked())

        return True

