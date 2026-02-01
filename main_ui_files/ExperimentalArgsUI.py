from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from ui_files.ExperimentalArgsUI import Ui_base_args_ui as Ui_ExperimentalArgsUi


class ExperimentalArgsUI(QWidget):
    """Handles all experimental args UI logic and state management."""

    # Signals for cross-file logic
    flowModelToggled = Signal(bool)  # Send to GeneralUI

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
        self.widget.flow_optimal_transport_enable.clicked.connect(lambda x: self.edit_flow_arg("flow_use_ot", x))
        self.widget.flow_timestep_distribution_selector.currentTextChanged.connect(
            lambda x: self.edit_flow_arg("flow_timestep_distribution", x)
        )
        self.widget.flow_uniform_static_ratio_shift_input.valueChanged.connect(
            lambda x: self.edit_flow_arg("flow_uniform_static_ratio", x)
        )
        self.widget.flow_logit_mean_input.valueChanged.connect(lambda x: self.edit_flow_arg("flow_logit_mean", x))
        self.widget.flow_logit_std_input.valueChanged.connect(lambda x: self.edit_flow_arg("flow_logit_std", x))
        # Flow model group checkbox
        self.widget.flow_model_settings_box.clicked.connect(self.on_flow_model_toggled)

        # adv. vae args
        self.widget.vae_reflection_enable.clicked.connect(lambda x: self.edit_args("vae_reflection", x, True))
        self.widget.vae_batch_size_input.valueChanged.connect(lambda x: self.edit_args("vae_batch_size", x, True))
        self.widget.vae_custom_scale_enable.clicked.connect(self.on_vae_custom_scale_toggled)
        self.widget.vae_custom_scale_input.valueChanged.connect(
            lambda x: self.edit_vae_custom_arg("vae_custom_scale", x, self.widget.vae_custom_scale_enable)
        )
        self.widget.vae_custom_shift_enable.clicked.connect(self.on_vae_custom_shift_toggled)
        self.widget.vae_custom_shift_input.valueChanged.connect(
            lambda x: self.edit_vae_custom_arg("vae_custom_shift", x, self.widget.vae_custom_shift_enable)
        )

        # misc args
        self.widget.zero_cond_dropout_enable.clicked.connect(lambda x: self.edit_args("zero_cond_dropout", x, True))
        self.widget.cfm_enable.clicked.connect(self.on_cfm_toggled)
        self.widget.cfm_lambda_enable.clicked.connect(self.on_cfm_lambda_toggled)
        self.widget.cfm_lambda_input.valueChanged.connect(self.edit_cfm_lambda_value)
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

    def edit_flow_arg(self, name: str, value: object) -> None:
        if self.widget.flow_model_settings_box.isChecked():
            self.edit_args(name, value, True)

    def edit_vae_custom_arg(self, name: str, value: object, toggle: QWidget) -> None:
        if toggle.isChecked():
            self.edit_args(name, value, True)
        elif name in self.args:
            del self.args[name]

    def edit_cfm_lambda_value(self, value: object) -> None:
        if self.widget.cfm_lambda_enable.isChecked():
            self.edit_args("cfm_lambda", value, True)
        elif "cfm_lambda" in self.args:
            del self.args["cfm_lambda"]

    def _sync_flow_args(self) -> None:
        self.edit_args("flow_model", True)
        self.edit_flow_arg("flow_use_ot", self.widget.flow_optimal_transport_enable.isChecked())
        self.edit_flow_arg("flow_timestep_distribution", self.widget.flow_timestep_distribution_selector.currentText())
        self.edit_flow_arg("flow_uniform_static_ratio", self.widget.flow_uniform_static_ratio_shift_input.value())
        self.edit_flow_arg("flow_logit_mean", self.widget.flow_logit_mean_input.value())
        self.edit_flow_arg("flow_logit_std", self.widget.flow_logit_std_input.value())

    def _clear_flow_args(self) -> None:
        for arg in [
            "flow_model",
            "flow_use_ot",
            "flow_timestep_distribution",
            "flow_uniform_static_ratio",
            "flow_logit_mean",
            "flow_logit_std",
        ]:
            if arg in self.args:
                del self.args[arg]

    def on_flow_model_toggled(self, checked: bool) -> None:
        """Handle flow model group checkbox toggle."""
        # Emit signal for cross-file logic
        self.flowModelToggled.emit(checked)
        self.widget.debiased_estimation_loss_enable.setEnabled(not checked)
        if checked:
            self._sync_flow_args()
        else:
            self._clear_flow_args()

    def update_cfm_availability(self, v_param_enabled: bool) -> None:
        """Update CFM availability based on flow model and v_param states."""
        flow_enabled = self.widget.flow_model_settings_box.isChecked()
        cfm_should_be_enabled = flow_enabled or v_param_enabled
        self.widget.cfm_enable.setEnabled(cfm_should_be_enabled)
        if not cfm_should_be_enabled:
            self.widget.cfm_lambda_enable.setEnabled(False)
            self.widget.cfm_lambda_input.setEnabled(False)
        elif self.widget.cfm_enable.isChecked():
            self.widget.cfm_lambda_enable.setEnabled(True)
            self.widget.cfm_lambda_input.setEnabled(self.widget.cfm_lambda_enable.isChecked())

    def on_vae_custom_scale_toggled(self, checked: bool) -> None:
        """Handle VAE custom scale checkbox toggle."""
        self.widget.vae_custom_scale_input.setEnabled(checked)

    def on_vae_custom_shift_toggled(self, checked: bool) -> None:
        """Handle VAE custom shift checkbox toggle."""
        self.widget.vae_custom_shift_input.setEnabled(checked)

    def on_cfm_toggled(self, checked: bool) -> None:
        """Handle CFM enable checkbox toggle."""
        self.widget.cfm_lambda_enable.setEnabled(checked)
        self.widget.cfm_lambda_input.setEnabled(checked)
        if not checked:
            # Clear CFM args when disabled
            if "contrastive_flow_matching" in self.args:
                del self.args["contrastive_flow_matching"]
            if "cfm_lambda" in self.args:
                del self.args["cfm_lambda"]

    def on_cfm_lambda_toggled(self, checked: bool) -> None:
        """Handle CFM lambda enable checkbox toggle."""
        self.widget.cfm_lambda_input.setEnabled(checked)

    def set_flow_model_enabled(self, enabled: bool) -> None:
        """Enable/disable the flow model settings group."""
        self.widget.flow_model_settings_box.setEnabled(enabled)

    def set_flux_enabled(self, enabled: bool) -> None:
        """External method to disable flow model when flux is enabled."""
        if not enabled:
            # Re-enable if flux is being disabled
            self.widget.flow_model_settings_box.setEnabled(True)
        else:
            # Disable and uncheck flow model when flux is enabled
            self.widget.flow_model_settings_box.setChecked(False)
            self.widget.flow_model_settings_box.setEnabled(False)
            self.on_flow_model_toggled(False)

    def _apply_post_load_state(self) -> None:
        self.widget.vae_custom_scale_input.setEnabled(self.widget.vae_custom_scale_enable.isChecked())
        self.widget.vae_custom_shift_input.setEnabled(self.widget.vae_custom_shift_enable.isChecked())
        self.widget.cfm_lambda_input.setEnabled(self.widget.cfm_lambda_enable.isChecked())
        self.widget.cfm_lambda_enable.setEnabled(self.widget.cfm_enable.isChecked())
        self.widget.debiased_estimation_loss_enable.setEnabled(not self.widget.flow_model_settings_box.isChecked())
        self.on_flow_model_toggled(self.widget.flow_model_settings_box.isChecked())

    def load_args(self, args: dict) -> bool:
        """Load experimental args from dict (args are at root level, not nested)."""
        self.args.clear()

        # (sdxl) flow args
        self.widget.flow_model_settings_box.setChecked(args.get("flow_model", False))
        self.widget.flow_optimal_transport_enable.setChecked(args.get("flow_use_ot", True))
        self.widget.flow_timestep_distribution_selector.setCurrentText(
            args.get("flow_timestep_distribution", "logit_normal")
        )
        self.widget.flow_uniform_static_ratio_shift_input.setValue(args.get("flow_uniform_static_ratio", 2.0))
        self.widget.flow_logit_mean_input.setValue(args.get("flow_logit_mean", 0.0))
        self.widget.flow_logit_std_input.setValue(args.get("flow_logit_std", 1.0))

        # adv. vae args
        self.widget.vae_reflection_enable.setChecked(args.get("vae_reflection", False))
        self.widget.vae_batch_size_input.setValue(args.get("vae_batch_size", 1))
        self.widget.vae_custom_scale_enable.setChecked(bool(args.get("vae_custom_scale", False)))
        self.widget.vae_custom_scale_input.setValue(args.get("vae_custom_scale", 0.0))
        self.widget.vae_custom_shift_enable.setChecked(bool(args.get("vae_custom_shift", False)))
        self.widget.vae_custom_shift_input.setValue(args.get("vae_custom_shift", 0.0))

        # misc args
        self.widget.zero_cond_dropout_enable.setChecked(args.get("zero_cond_dropout", False))
        self.widget.cfm_enable.setChecked(args.get("contrastive_flow_matching", False))
        self.widget.cfm_lambda_enable.setChecked(bool(args.get("cfm_lambda", False)))
        self.widget.cfm_lambda_input.setValue(args.get("cfm_lambda", 0.05))
        self.widget.debiased_estimation_loss_enable.setChecked(args.get("debiased_estimation_loss", False))

        self._apply_post_load_state()

        # (sdxl) flow args - only add if flow model is checked
        if self.widget.flow_model_settings_box.isChecked():
            self.edit_args("flow_model", True)
            self.edit_args("flow_use_ot", self.widget.flow_optimal_transport_enable.isChecked(), True)
            self.edit_args("flow_timestep_distribution", self.widget.flow_timestep_distribution_selector.currentText(), True)
            self.edit_args("flow_uniform_static_ratio", self.widget.flow_uniform_static_ratio_shift_input.value(), True)
            self.edit_args("flow_logit_mean", self.widget.flow_logit_mean_input.value(), True)
            self.edit_args("flow_logit_std", self.widget.flow_logit_std_input.value(), True)

        # adv. vae args
        self.edit_args("vae_reflection", self.widget.vae_reflection_enable.isChecked(), True)
        if self.widget.vae_batch_size_input.value() != 1:
            self.edit_args("vae_batch_size", self.widget.vae_batch_size_input.value(), True)
        if self.widget.vae_custom_scale_enable.isChecked():
            self.edit_args("vae_custom_scale", self.widget.vae_custom_scale_input.value(), True)
        if self.widget.vae_custom_shift_enable.isChecked():
            self.edit_args("vae_custom_shift", self.widget.vae_custom_shift_input.value(), True)

        # misc args
        self.edit_args("zero_cond_dropout", self.widget.zero_cond_dropout_enable.isChecked(), True)
        if self.widget.cfm_enable.isChecked():
            self.edit_args("contrastive_flow_matching", True)
            if self.widget.cfm_lambda_enable.isChecked():
                self.edit_args("cfm_lambda", self.widget.cfm_lambda_input.value(), True)
        self.edit_args("debiased_estimation_loss", self.widget.debiased_estimation_loss_enable.isChecked(), True)

        return True

    def save_args(self) -> dict:
        """Rebuild and return current args dict from UI state."""
        self.args.clear()

        # (sdxl) flow args - only include if flow model is checked and enabled
        if self.widget.flow_model_settings_box.isChecked() and self.widget.flow_model_settings_box.isEnabled():
            self.edit_args("flow_model", True)
            self.edit_args("flow_use_ot", self.widget.flow_optimal_transport_enable.isChecked(), True)
            self.edit_args(
                "flow_timestep_distribution", self.widget.flow_timestep_distribution_selector.currentText(), True
            )
            self.edit_args("flow_uniform_static_ratio", self.widget.flow_uniform_static_ratio_shift_input.value(), True)
            self.edit_args("flow_logit_mean", self.widget.flow_logit_mean_input.value(), True)
            self.edit_args("flow_logit_std", self.widget.flow_logit_std_input.value(), True)
        else:
            # Explicitly remove all flow args when flow model is disabled
            for arg in [
                "flow_model",
                "flow_use_ot",
                "flow_timestep_distribution",
                "flow_uniform_static_ratio",
                "flow_logit_mean",
                "flow_logit_std",
            ]:
                if arg in self.args:
                    del self.args[arg]

        # adv. vae args
        self.edit_args("vae_reflection", self.widget.vae_reflection_enable.isChecked(), True)
        if self.widget.vae_batch_size_input.value() != 1:  # no need to add if it's default value
            self.edit_args("vae_batch_size", self.widget.vae_batch_size_input.value(), True)
        if self.widget.vae_custom_scale_enable.isChecked() and self.widget.vae_custom_scale_enable.isEnabled():
            self.edit_args("vae_custom_scale", self.widget.vae_custom_scale_input.value(), True)
        else:
            if "vae_custom_scale" in self.args:
                del self.args["vae_custom_scale"]
        if self.widget.vae_custom_shift_enable.isChecked() and self.widget.vae_custom_shift_enable.isEnabled():
            self.edit_args("vae_custom_shift", self.widget.vae_custom_shift_input.value(), True)
        else:
            if "vae_custom_shift" in self.args:
                del self.args["vae_custom_shift"]

        # misc args
        self.edit_args("zero_cond_dropout", self.widget.zero_cond_dropout_enable.isChecked(), True)
        if self.widget.cfm_enable.isChecked() and self.widget.cfm_enable.isEnabled():
            self.edit_args("contrastive_flow_matching", True)
            if self.widget.cfm_lambda_enable.isChecked() and self.widget.cfm_lambda_enable.isEnabled():
                self.edit_args("cfm_lambda", self.widget.cfm_lambda_input.value(), True)
            else:
                if "cfm_lambda" in self.args:
                    del self.args["cfm_lambda"]
        else:
            # Explicitly remove CFM args when CFM is disabled
            if "contrastive_flow_matching" in self.args:
                del self.args["contrastive_flow_matching"]
            if "cfm_lambda" in self.args:
                del self.args["cfm_lambda"]
        if (
            self.widget.debiased_estimation_loss_enable.isChecked()
            and self.widget.debiased_estimation_loss_enable.isEnabled()
        ):
            self.edit_args("debiased_estimation_loss", True, True)
        else:
            if "debiased_estimation_loss" in self.args:
                del self.args["debiased_estimation_loss"]

        return self.args
