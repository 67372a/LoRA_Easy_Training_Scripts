from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget
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
        # Default log_prefix_mode and run_name_mode
        self.args = {"log_prefix_mode": "disabled", "run_name_mode": "default"}

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)
        self.widget.log_output_input.setMode("folder")
        self.widget.log_output_input.highlight = True
        self.widget.log_wandb_key_input.setEnabled(False)
        self.widget.log_prefix_input.setEnabled(False)
        self.widget.run_name_input.setEnabled(False) # Disable new input initially
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
        # Log Prefix Connections
        self.widget.log_prefix_mode_selector.currentIndexChanged.connect(
            self.change_log_prefix_mode
        )
        self.widget.log_prefix_input.textChanged.connect(
            self.update_manual_log_prefix
        )

        # Run Name Connections (NEW)
        self.widget.run_name_mode_selector.currentIndexChanged.connect(
            self.change_run_name_mode
        )
        self.widget.run_name_input.textChanged.connect(
            self.update_manual_run_name
        )

        # Tracker Name Connection
        self.widget.log_tracker_name_enable.clicked.connect(
            lambda x: self.enable_disable_lineEdit(
                x, self.widget.log_tracker_name_input, "log_tracker_name"
            )
        )
        self.widget.log_tracker_name_input.textChanged.connect(
            lambda x: self.edit_args("log_tracker_name", x, True)
        )
        # Wandb Key Connection
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
            # Reset args, keeping only the mode defaults
            self.args = {"log_prefix_mode": "disabled", "run_name_mode": "default"}
            self.widget.log_output_input.setStyleSheet("")
            # Ensure prefix input is disabled and args cleared
            self.widget.log_prefix_input.setEnabled(False)
            # Reset prefix mode selector to default (Disabled)
            self.widget.log_prefix_mode_selector.setCurrentIndex(0)
            # Ensure run name input is disabled and args cleared
            self.widget.run_name_input.setEnabled(False)
            # Reset run name mode selector to default
            self.widget.run_name_mode_selector.setCurrentIndex(0)
            return

        # Re-populate args based on current UI state when enabled
        self.edit_args("logging_dir", self.widget.log_output_input.text())
        # Apply prefix mode logic
        self.change_log_prefix_mode(self.widget.log_prefix_mode_selector.currentIndex())
        # Apply run name mode logic (NEW)
        self.change_run_name_mode(self.widget.run_name_mode_selector.currentIndex())
        # Apply tracker name logic
        if self.widget.log_tracker_name_enable.isChecked():
            self.enable_disable_lineEdit(
                True, self.widget.log_tracker_name_input, "log_tracker_name"
            )
        # Apply log system logic (handles wandb key)
        self.change_log_system(self.widget.log_mode_selector.currentIndex())
        # Update stylesheet if needed
        if self.widget.log_output_input.dirty:
            self.widget.log_output_input.update_stylesheet()

    @Slot(int)
    def change_log_prefix_mode(self, index: int) -> None:
        """Handles changes in the log_prefix_mode_selector."""
        if not self.widget.logging_group.isChecked(): return # Ignore if group disabled
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
        if not self.widget.logging_group.isChecked(): return # Ignore if group disabled
        if self.widget.log_prefix_mode_selector.currentText() == "Manual":
            self.edit_args("log_prefix", text, True)
        # If mode is not Manual but text changes (e.g., user typed then changed mode),
        # ensure log_prefix is not in args (handled by change_log_prefix_mode)

    @Slot(int)
    def change_run_name_mode(self, index: int) -> None:
        """Handles changes in the run_name_mode_selector."""
        if not self.widget.logging_group.isChecked(): return # Ignore if group disabled
        mode = self.widget.run_name_mode_selector.currentText().lower().replace(" ", "_")
        self.edit_args("run_name_mode", mode, True)

        is_manual_mode = (mode == "manual")
        self.widget.run_name_input.setEnabled(is_manual_mode)

        # Clear run_name arg if not in manual mode
        if "run_name" in self.args and not is_manual_mode:
            del self.args["run_name"]
        # If switching to manual, add the current input value to args
        elif is_manual_mode:
            self.update_manual_run_name(self.widget.run_name_input.text())

    @Slot(str)
    def update_manual_run_name(self, text: str) -> None:
        """Updates the run_name arg only if the mode is Manual."""
        if not self.widget.logging_group.isChecked(): return # Ignore if group disabled
        if self.widget.run_name_mode_selector.currentText() == "Manual":
            self.edit_args("run_name", text, True)
        # If mode is not Manual but text changes (e.g., user typed then changed mode),
        # ensure run_name is not in args (handled by change_run_name_mode)


    def change_log_system(self, index: int) -> None:
        if not self.widget.logging_group.isChecked(): return # Ignore if group disabled
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
        if not self.widget.logging_group.isChecked(): return # Ignore if group disabled
        elem.setEnabled(checked)
        self.edit_args(name, elem.text() if checked else None, True)

    def load_args(self, args: dict) -> bool:
        args_logging: dict = args.get(self.name, {})

        # update element inputs
        is_enabled = bool(args_logging.get("log_with", False))
        self.widget.logging_group.setChecked(is_enabled)

        self.widget.log_mode_selector.setCurrentText(
            args_logging.get("log_with", "tensorboard").capitalize()
        )
        self.widget.log_output_input.setText(args_logging.get("logging_dir", ""))

        # Load Log Prefix
        self.widget.log_prefix_mode_selector.setCurrentText(
            args_logging.get("log_prefix_mode", "disabled").replace("_", " ").title()
        )
        self.widget.log_prefix_input.setText(args_logging.get("log_prefix", ""))

        # Load Run Name
        self.widget.run_name_mode_selector.setCurrentText(
            args_logging.get("run_name_mode", "default").replace("_", " ").title()
        )
        self.widget.run_name_input.setText(args_logging.get("run_name", ""))

        # Load Tracker Name
        self.widget.log_tracker_name_enable.setChecked("log_tracker_name" in args_logging)
        self.widget.log_tracker_name_input.setText(args_logging.get("log_tracker_name", ""))

        # Load Wandb Key
        self.widget.log_wandb_key_input.setText(args_logging.get("wandb_api_key", ""))

        # Apply enable/disable logic based on loaded state
        self.enable_disable(is_enabled)
        # Ensure correct state of manual inputs based on loaded modes *after* main enable_disable
        if is_enabled:
            self.change_log_prefix_mode(self.widget.log_prefix_mode_selector.currentIndex())
            self.change_run_name_mode(self.widget.run_name_mode_selector.currentIndex())
            self.change_log_system(self.widget.log_mode_selector.currentIndex()) # Ensure wandb key enabled state is correct
            # Ensure tracker name input enabled state is correct
            self.widget.log_tracker_name_input.setEnabled(self.widget.log_tracker_name_enable.isChecked())


        return True