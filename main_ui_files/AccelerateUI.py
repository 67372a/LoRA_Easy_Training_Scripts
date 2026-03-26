import json
from pathlib import Path

from PySide6.QtWidgets import QWidget
from ui_files.AccelerateUI import Ui_accelerate_ui
from modules.BaseWidget import BaseWidget


class AccelerateWidget(BaseWidget):
    """Widget for configuring multi-GPU training with accelerate launch.

    Unlike other widgets, this one saves settings to config.json instead of
    using self.args, because accelerate settings are machine-specific and
    should not be saved to training TOML files.
    """

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Multi-GPU Training (Accelerate)")
        self.widget = Ui_accelerate_ui()

        # Use a unique name but we won't use self.args for training config
        self.name = "accelerate_args"
        self.args = {}  # Keep empty - accelerate settings go to config.json
        self.dataset_args = {}

        self.setup_widget()
        self.setup_connections()
        self.load_from_config()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)

    def setup_connections(self) -> None:
        # Save to config.json whenever any setting changes
        self.widget.accelerate_group.clicked.connect(self.save_to_config)
        self.widget.num_processes_input.valueChanged.connect(self.save_to_config)
        self.widget.main_process_port_input.valueChanged.connect(self.save_to_config)

    def get_accelerate_settings(self) -> dict:
        """Return accelerate settings for passing to backend."""
        if not self.widget.accelerate_group.isChecked():
            return {"enabled": False}

        return {
            "enabled": True,
            "num_processes": self.widget.num_processes_input.value(),
            "main_process_port": self.widget.main_process_port_input.value(),
        }

    def save_to_config(self) -> None:
        """Persist accelerate settings to config.json."""
        config_path = Path("config.json")
        config_dict = json.loads(config_path.read_text()) if config_path.exists() else {}
        config_dict["accelerate"] = self.get_accelerate_settings()
        config_path.write_text(json.dumps(config_dict, indent=2))

    def load_from_config(self) -> None:
        """Load accelerate settings from config.json."""
        config_path = Path("config.json")
        if not config_path.exists():
            return

        config_dict = json.loads(config_path.read_text())
        accel = config_dict.get("accelerate", {})

        self.widget.accelerate_group.setChecked(accel.get("enabled", False))
        self.widget.num_processes_input.setValue(accel.get("num_processes", 2))
        self.widget.main_process_port_input.setValue(accel.get("main_process_port", 29500))

    def load_args(self, args: dict) -> bool:
        """Load accelerate settings from config.json (not from TOML args)."""
        self.load_from_config()
        return True

    def load_dataset_args(self, dataset_args: dict) -> bool:
        """No dataset args for accelerate settings."""
        return True
