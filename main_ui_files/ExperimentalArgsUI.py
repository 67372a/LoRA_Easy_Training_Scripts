from PySide6.QtWidgets import QWidget
from ui_files.ExperimentalArgsUI import Ui_base_args_ui as Ui_ExperimentalArgsUi


class ExperimentalArgsUI(QWidget):
    """Handles all experimental args UI logic and state management."""

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.widget = Ui_ExperimentalArgsUi()
        self.args = {}

        self.setObjectName("experimental_args_widget")
        self.setContentsMargins(0, 0, 0, 0)
        self.widget.setupUi(self)

        self.setup_connections()

    def setup_connections(self) -> None:
        """Wire up all experimental args UI elements."""
        self.widget.vae_reflection_enable.clicked.connect(
            lambda x: self.edit_args("vae_reflection", x, True)
        )
        self.widget.flow_optimal_transport_enable.clicked.connect(
            lambda x: self.edit_args("flow_use_ot", x, True)
        )
        self.widget.flow_timestep_distribution_selector.currentTextChanged.connect(
            lambda x: self.edit_args("flow_timestep_distribution", x, True)
        )
        self.widget.flow_unfirom_static_ratio_shift_selector.valueChanged.connect(
            lambda x: self.edit_args("flow_uniform_static_ratio_shift", x, True)
        )
        self.widget.flow_logit_mean_selector.valueChanged.connect(
            lambda x: self.edit_args("flow_logit_mean", x, True)
        )
        self.widget.flow_logit_std_selector.valueChanged.connect(
            lambda x: self.edit_args("flow_logit_std", x, True)
        )
        self.widget.flow_cfm_enable.clicked.connect(
            lambda x: self.edit_args("flow_cfm", x, True)
        )

    def edit_args(self, name: str, value: object, optional: bool = False) -> None:
        """Update args dict, handling optional values."""
        if name in self.args:
            del self.args[name]
        if optional and (not value or value is False):
            return
        self.args[name] = value

    def set_flow_model_enabled(self, enabled: bool) -> None:
        """Enable/disable the flow model settings group."""
        self.widget.flow_model_settings_group.setEnabled(enabled)

    def load_args(self, args: dict) -> bool:
        """Load experimental args from dict."""
        args = args.get("experimental_args", {})

        self.widget.vae_reflection_enable.setChecked(args.get("vae_reflection", False))
        self.widget.flow_model_settings_group.setChecked(args.get("flow_model", False))
        self.widget.flow_optimal_transport_enable.setChecked(args.get("flow_use_ot", True))
        self.widget.flow_timestep_distribution_selector.setCurrentText(
            args.get("flow_timestep_distribution", "logit_normal")
        )
        self.widget.flow_unfirom_static_ratio_shift_selector.setValue(
            args.get("flow_uniform_static_ratio_shift", 2.0)
        )
        self.widget.flow_logit_mean_selector.setValue(args.get("flow_logit_mean", 0.0))
        self.widget.flow_logit_std_selector.setValue(args.get("flow_logit_std", 1.0))
        self.widget.flow_cfm_enable.setChecked(args.get("flow_cfm", False))

        # sync args from UI
        self.edit_args("vae_reflection", self.widget.vae_reflection_enable.isChecked(), True)
        self.edit_args("flow_model", self.widget.flow_model_settings_group.isChecked(), True)
        self.edit_args("flow_use_ot", self.widget.flow_optimal_transport_enable.isChecked(), True)
        self.edit_args(
            "flow_timestep_distribution",
            self.widget.flow_timestep_distribution_selector.currentText(),
            True,
        )
        self.edit_args(
            "flow_uniform_static_ratio_shift",
            self.widget.flow_unfirom_static_ratio_shift_selector.value(),
            True,
        )
        self.edit_args("flow_logit_mean", self.widget.flow_logit_mean_selector.value(), True)
        self.edit_args("flow_logit_std", self.widget.flow_logit_std_selector.value(), True)
        self.edit_args("flow_cfm", self.widget.flow_cfm_enable.isChecked(), True)

        return True

    def save_args(self) -> dict:
        """Return current args dict."""
        return self.args
