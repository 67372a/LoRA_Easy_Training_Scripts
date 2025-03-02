from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QApplication
from qt_material import QtStyleTools, apply_stylesheet
from ui_files.MainUI import Ui_MainWindow
from main_ui_files.MainUI import MainWidget
from pathlib import Path
import json
from modules.LoraResizePopupUi import LoraResizePopup


class MainWindow(QMainWindow, QtStyleTools):
    def __init__(self, app: QApplication = None) -> None:
        super().__init__()
        self.app = app
        self.widget = Ui_MainWindow()
        self.main_widget = MainWidget()
        self.dark_themes: list[QAction] = []
        self.light_themes: list[QAction] = []
        self.no_theme = QAction("", self)
        self.tensorboard_process = None  

        self.setup_widget()
        self.setup_themes()
        self.setup_connections()

    def setup_widget(self) -> None:
        self.widget.setupUi(self)
        
        # Add TensorBoard action to Utils menu
        self.tensorboard_action = QAction("Toggle TensorBoard", self)  # Changed text to indicate toggle functionality
        self.widget.menuUtils.addAction(self.tensorboard_action)
        
        self.setMinimumWidth(739)
        screen_size = QApplication.screens()[0].size()
        self.setGeometry(
            screen_size.width() / 2 - (self.geometry().width() / 2),
            screen_size.height() / 2 - (self.geometry().height() / 2),
            self.geometry().width() + 10,
            750,
        )
        self.centralWidget().layout().addWidget(self.main_widget)

    def setup_themes(self) -> None:
        themes_path = Path("css/themes")
        for theme in themes_path.iterdir():
            if len(theme.name.split("500")) > 1:
                continue
            if len(theme.name.split("dark")) > 1:
                self.dark_themes.append(QAction(theme.stem.split("_")[1], self))
            else:
                self.light_themes.append(QAction(theme.stem.split("_")[1], self))
        for theme in self.dark_themes:
            self.widget.dark_theme_menu.addAction(theme)
        for theme in self.light_themes:
            self.widget.light_theme_menu.addAction(theme)

    def setup_connections(self) -> None:
        self.widget.save_toml.triggered.connect(self.main_widget.save_toml)
        self.widget.load_toml.triggered.connect(self.main_widget.load_toml)
        for i, action in enumerate(self.dark_themes):
            action.triggered.connect(
                lambda _=False, index=i: self.change_theme(index, False)
            )
        for i, action in enumerate(self.light_themes):
            action.triggered.connect(
                lambda _=False, index=i: self.change_theme(index, True)
            )
        self.widget.no_theme_action.triggered.connect(
            lambda _=False: self.change_theme(0, False, True)
        )
        self.widget.lora_resize_action.triggered.connect(self.run_resize)
        self.widget.set_train_lora_action.triggered.connect(
            self.main_widget.set_train_lora
        )
        self.widget.set_train_ti_action.triggered.connect(self.main_widget.set_train_ti)
        self.tensorboard_action.triggered.connect(self.launch_tensorboard)

    def launch_tensorboard(self) -> None:
        try:
            # If TensorBoard is already running, stop it
            if hasattr(self, 'tensorboard_process') and self.tensorboard_process is not None:
                self.tensorboard_process.terminate()
                self.tensorboard_process = None
                print("Stopped previous TensorBoard instance")
                return

            # Get the logging directory from args
            args = self.main_widget.args_widget.get_args()
            log_dir = args["args"]["logging_args"].get("logging_dir")
                
            if not log_dir:
                print("No logging directory specified. Please set --logging_dir in training arguments")
                return
                
            print(f"Using log directory: {log_dir}")

            import subprocess
            import os
            import sys

            # Construct path to backend's virtual environment
            # Start from the root directory of LoRA_Easy_Training_Scripts
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up two levels from main_ui_files
            tensorboard_exe = os.path.join(root_dir, "backend", "sd_scripts", "venv", "Scripts", "tensorboard.exe")

            print(f"Looking for TensorBoard at: {tensorboard_exe}")
            if not os.path.exists(tensorboard_exe):
                print(f"TensorBoard not found at expected path: {tensorboard_exe}")
                return

            # Build the command
            cmd = [
                tensorboard_exe,
                "--logdir", log_dir,
                "--host", "127.0.0.1",
                "--port", "6006"
            ]
            
            print(f"Running command: {' '.join(cmd)}")
            
            # Launch tensorboard in background
            self.tensorboard_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            # Wait a bit to make sure TensorBoard starts up
            import time
            time.sleep(2)
            
            # Check if process is still running
            if self.tensorboard_process.poll() is None:
                print("TensorBoard launched successfully")
                print("You can access TensorBoard at http://127.0.0.1:6006")
                
                # Read any error output
                error_output = self.tensorboard_process.stderr.readline().decode().strip()
                if error_output:
                    print(f"TensorBoard message: {error_output}")
            else:
                # Process terminated, get error message
                _, stderr = self.tensorboard_process.communicate()
                error_msg = stderr.decode().strip()
                print(f"TensorBoard failed to start: {error_msg}")
                self.tensorboard_process = None
                
        except Exception as e:
            print(f"Failed to launch TensorBoard: {e}")
            if hasattr(self, 'tensorboard_process') and self.tensorboard_process is not None:
                self.tensorboard_process.terminate()
                self.tensorboard_process = None

    def closeEvent(self, event):
        # Clean up TensorBoard process if it's running
        if hasattr(self, 'tensorboard_process') and self.tensorboard_process is not None:
            print("Shutting down TensorBoard...")
            self.tensorboard_process.terminate()
            try:
                # Wait for process to terminate
                self.tensorboard_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # If process doesn't terminate within 5 seconds, kill it
                self.tensorboard_process.kill()
            self.tensorboard_process = None

        # Call the parent class closeEvent
        super().closeEvent(event)

    def change_theme(
        self, index: int, is_light: bool = False, no_theme: bool = False
    ) -> None:
        if no_theme:
            theme_path = None
            self.app.setStyleSheet("")
        else:
            prefix = "light" if is_light else "dark"
            if is_light:
                name = self.light_themes[index].text()
            else:
                name = self.dark_themes[index].text()
            theme_path = Path(f"css/themes/{prefix}_{name}.xml")
            apply_stylesheet(
                self.app,
                theme=str(theme_path),
                invert_secondary=is_light,
            )
        config = Path("config.json")
        config_dict = json.loads(config.read_text()) if config.exists() else {}
        config_dict["theme"] = {
            "location": theme_path.as_posix() if theme_path else None,
            "is_light": is_light,
        }
        config.write_text(json.dumps(config_dict, indent=2))

    def run_resize(self):
        popup = LoraResizePopup(self)
        popup.setModal(True)
        popup.exec()
