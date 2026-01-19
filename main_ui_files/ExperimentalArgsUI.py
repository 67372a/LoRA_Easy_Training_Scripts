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

        # (sdxl) flow args
        self.widget.flow_optimal_transport_enable.clicked.connect(
            lambda x: self.edit_args("flow_use_ot", x, True)
        )
        self.widget.flow_timestep_distribution_selector.currentTextChanged.connect(
            lambda x: self.edit_args("flow_timestep_distribution", x, True)
        )
        self.widget.flow_uniform_static_ratio_shift_input.valueChanged.connect(
            lambda x: self.edit_args("flow_uniform_static_ratio", x, True)
        )
        self.widget.flow_logit_mean_input.valueChanged.connect(
            lambda x: self.edit_args("flow_logit_mean", x, True)
        )
        self.widget.flow_logit_std_input.valueChanged.connect(
            lambda x: self.edit_args("flow_logit_std", x, True)
        )


        # adv. vae args
        self.widget.vae_reflection_enable.clicked.connect(
            lambda x: self.edit_args("vae_reflection", x, True)
        )

        # misc args
        self.widget.cfm_enable.clicked.connect(
            lambda x: self.edit_args("contrastive_flow_matching", x, True)
        )
        self.widget.debiased_estimation_loss_enable.clicked.connect(
            lambda x: self.edit_args("debiased_estimation_loss", x, True)
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
        self.widget.flow_model_settings_box.setEnabled(enabled)

    def load_args(self, args: dict) -> bool:
        """Load experimental args from dict."""
        args = args.get("experimental_args", {})

        # (sdxl) flow args
        self.widget.flow_model_settings_box.setChecked(args.get("flow_model", False))
        self.widget.flow_optimal_transport_enable.setChecked(args.get("flow_use_ot", True))
        self.widget.flow_timestep_distribution_selector.setCurrentText(
            args.get("flow_timestep_distribution", "logit_normal")
        )
        self.widget.flow_uniform_static_ratio_shift_input.setValue(
            args.get("flow_uniform_static_ratio", 2.0)
        )
        self.widget.flow_logit_mean_input.setValue(args.get("flow_logit_mean", 0.0))
        self.widget.flow_logit_std_input.setValue(args.get("flow_logit_std", 1.0))

        # adv. vae args
        self.widget.vae_reflection_enable.setChecked(args.get("vae_reflection", False))

        # misc args
        self.widget.cfm_enable.setChecked(args.get("contrastive_flow_matching", False))
        self.widget.debiased_estimation_loss_enable.setChecked(args.get("debiased_estimation_loss", False))


        # sync args from UI
        # (sdxl) flow args
        self.edit_args("flow_model", self.widget.flow_model_settings_box.isChecked(), True)
        self.edit_args("flow_use_ot", self.widget.flow_optimal_transport_enable.isChecked(), True)
        self.edit_args(
            "flow_timestep_distribution",
            self.widget.flow_timestep_distribution_selector.currentText(),
            True,
        )
        self.edit_args(
            "flow_uniform_static_ratio",
            self.widget.flow_uniform_static_ratio_shift_input.value(),
            True,
        )
        self.edit_args("flow_logit_mean", self.widget.flow_logit_mean_input.value(), True)
        self.edit_args("flow_logit_std", self.widget.flow_logit_std_input.value(), True)

        # adv. vae args
        self.edit_args("vae_reflection", self.widget.vae_reflection_enable.isChecked(), True)

        # misc args
        self.edit_args("contrastive_flow_matching", self.widget.cfm_enable.isChecked(), True)
        self.edit_args("debiased_estimation_loss", self.widget.debiased_estimation_loss_enable.isChecked(), True)

        return True

    def save_args(self) -> dict:
        """Return current args dict."""
        return self.args
