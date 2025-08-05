from PySide6.QtWidgets import QWidget
from ui_files.EDMLossUI import Ui_edm_loss_UI
from modules.BaseWidget import BaseWidget
from PySide6.QtGui import QIcon
from pathlib import Path

class EDMLossWidget(BaseWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("EDM² Loss Weighting")
        self.widget = Ui_edm_loss_UI()
        self.name = "edm_loss_args"
        
        self.setup_widget()
        self.setup_connections()
        self.setup_defaults()
        
        # Initialize the UI state based on the checkbox
        self.enable_disable(self.widget.enable_checkbox.isChecked())

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)
        
        # Set icons
        self.widget.graph_output_button.setIcon(QIcon(str(Path("icons/more-horizontal.svg"))))
        self.widget.initial_weights_button.setIcon(QIcon(str(Path("icons/more-horizontal.svg"))))

        # Configure spinboxes
        self.widget.warmup_input.setRange(0.0, 1.0)
        self.widget.warmup_input.setSingleStep(0.01)
        self.widget.constant_input.setRange(0.0, 1.0)
        self.widget.constant_input.setSingleStep(0.01)
        
        # Configure new spinboxes
        self.widget.num_channels_input.setRange(1, 2048)
        self.widget.graph_steps_input.setRange(1, 1000)
        self.widget.graph_y_limit_input.setRange(1, 100)
        
        # Configure DragDropLineEdit widgets
        self.widget.initial_weights_input.setMode("file")
        self.widget.initial_weights_input.extensions = [".pt", ".pth", ".safetensors"]
        self.widget.initial_weights_input.highlight = True
        
        self.widget.graph_output_input.setMode("folder")
        self.widget.graph_output_input.highlight = True

        # Disable scheduler inputs initially
        self.widget.warmup_input.setEnabled(False)
        self.widget.constant_input.setEnabled(False)

        # Disable graph inputs initially
        self.widget.graph_output_input.setEnabled(False)
        self.widget.graph_output_button.setEnabled(False)
        self.widget.graph_steps_input.setEnabled(False)
        self.widget.graph_y_limit_input.setEnabled(False)

    def setup_connections(self) -> None:
        # Main enable
        self.widget.enable_checkbox.clicked.connect(self.enable_disable)
        self.widget.enable_checkbox.clicked.connect(
            lambda x: self.edit_args("edm2_loss_weighting", x))
        
        # Optimizer
        self.widget.optimizer_type_input.textChanged.connect(
            lambda x: self.edit_args("edm2_loss_weighting_optimizer", x))
        self.widget.lr_input.textChanged.connect(
            lambda x: self.edit_args("edm2_loss_weighting_optimizer_lr", x))
        self.widget.optimizer_args_input.textChanged.connect(
            lambda x: self.edit_args("edm2_loss_weighting_optimizer_args", x))
        
        # Scheduler
        self.widget.scheduler_enable.clicked.connect(self.enable_disable_scheduler)
        self.widget.warmup_input.valueChanged.connect(
            lambda x: self.edit_args("edm2_loss_weighting_lr_scheduler_warmup_percent", x))
        self.widget.constant_input.valueChanged.connect(
            lambda x: self.edit_args("edm2_loss_weighting_lr_scheduler_constant_percent", x))
        
        # Advanced
        self.widget.initial_weights_button.clicked.connect(
            lambda: self.set_file_from_dialog(
                self.widget.initial_weights_input,
                "Select Initial Weights File",
                "PyTorch Model"
            )
        )
        self.widget.initial_weights_input.textChanged.connect(
            lambda x: self.edit_args("edm2_loss_weighting_initial_weights", x)
        )
        self.widget.num_channels_input.valueChanged.connect(
            lambda x: self.edit_args("edm2_loss_weighting_num_channels", x)
        )
        
        # Graph Settings
        self.widget.generate_graph_enable.clicked.connect(self.enable_disable_graph)
        self.widget.graph_output_button.clicked.connect(
            lambda: self.set_folder_from_dialog(
                self.widget.graph_output_input,
                "Select Graph Output Directory"
            )
        )
        self.widget.graph_output_input.textChanged.connect(
            lambda x: self.edit_args("edm2_loss_weighting_generate_graph_output_dir", x)
        )
        self.widget.graph_steps_input.valueChanged.connect(
            lambda x: self.edit_args("edm2_loss_weighting_generate_graph_every_x_steps", x)
        )
        self.widget.graph_y_limit_input.valueChanged.connect(
            lambda x: self.edit_args("edm2_loss_weighting_generate_graph_y_limit", x)
        )

    def setup_defaults(self):
        # Set default values
        self.widget.optimizer_type_input.setText("LoraEasyCustomOptimizer.adopt.ADOPT")
        self.widget.lr_input.setText("2e-2")
        self.widget.optimizer_args_input.setText("{'weight_decay':0}")
        self.widget.warmup_input.setValue(0.1)
        self.widget.constant_input.setValue(0.9)
        self.widget.num_channels_input.setValue(128)
        self.widget.generate_graph_enable.setChecked(False)
        self.widget.graph_steps_input.setValue(10)
        self.widget.graph_y_limit_input.setValue(50)

    def enable_disable(self, checked: bool):
        self.args = {}
        # Set the main enable argument
        self.edit_args("edm2_loss_weighting", checked)
        
        for widget in [
            self.widget.optimizer_group,
            self.widget.scheduler_group,
            self.widget.advanced_group,
            self.widget.graph_group
        ]:
            widget.setEnabled(checked)
        
        if checked:
            # Trigger updates for all fields
            self.widget.optimizer_type_input.textChanged.emit(self.widget.optimizer_type_input.text())
            self.widget.lr_input.textChanged.emit(self.widget.lr_input.text())
            self.widget.optimizer_args_input.textChanged.emit(self.widget.optimizer_args_input.text())
            
            # Call the enable/disable methods with current checkbox states
            self.enable_disable_scheduler(self.widget.scheduler_enable.isChecked())
            self.enable_disable_graph(self.widget.generate_graph_enable.isChecked())
            
            self.widget.initial_weights_input.textChanged.emit(self.widget.initial_weights_input.text())
            self.widget.num_channels_input.valueChanged.emit(self.widget.num_channels_input.value())

    def enable_disable_scheduler(self, checked: bool):
        """Enable or disable scheduler settings based on checkbox"""
        # Enable/disable the scheduler input fields
        self.widget.warmup_input.setEnabled(checked)
        self.widget.constant_input.setEnabled(checked)
        
        # Update the args
        self.edit_args("edm2_loss_weighting_lr_scheduler", checked, True)
        
        if checked:
            # Update values if enabled
            self.widget.warmup_input.valueChanged.emit(self.widget.warmup_input.value())
            self.widget.constant_input.valueChanged.emit(self.widget.constant_input.value())

    def enable_disable_graph(self, checked: bool):
        """Enable or disable graph settings based on checkbox"""
        # Enable/disable the graph input fields
        self.widget.graph_output_input.setEnabled(checked)
        self.widget.graph_output_button.setEnabled(checked)
        self.widget.graph_steps_input.setEnabled(checked)
        self.widget.graph_y_limit_input.setEnabled(checked)
        
        # Update the args - use False for optional to ensure it's always included
        self.edit_args("edm2_loss_weighting_generate_graph", checked, False)
        
        if checked:
            # Update values if enabled
            self.widget.graph_output_input.textChanged.emit(self.widget.graph_output_input.text())
            self.widget.graph_steps_input.valueChanged.emit(self.widget.graph_steps_input.value())
            self.widget.graph_y_limit_input.valueChanged.emit(self.widget.graph_y_limit_input.value())

    def load_args(self, args: dict) -> bool:
        args = args.get(self.name, {})
        self.widget.enable_checkbox.setChecked(bool(args.get("edm2_loss_weighting", False)))
        
        # Load optimizer arguments
        self.widget.optimizer_type_input.setText(args.get("edm2_loss_weighting_optimizer", ""))
        self.widget.lr_input.setText(args.get("edm2_loss_weighting_optimizer_lr", ""))
        self.widget.optimizer_args_input.setText(args.get("edm2_loss_weighting_optimizer_args", ""))
        
        # Load scheduler arguments
        self.widget.scheduler_enable.setChecked(args.get("edm2_loss_weighting_lr_scheduler", False))
        self.widget.warmup_input.setValue(float(args.get("edm2_loss_weighting_lr_scheduler_warmup_percent", 0.1)))
        self.widget.constant_input.setValue(float(args.get("edm2_loss_weighting_lr_scheduler_constant_percent", 0.9)))
        
        # Load advanced arguments
        self.widget.initial_weights_input.setText(args.get("edm2_loss_weighting_initial_weights", ""))
        self.widget.num_channels_input.setValue(int(args.get("edm2_loss_weighting_num_channels", 448)))
        
        # Load graph arguments
        self.widget.generate_graph_enable.setChecked(args.get("edm2_loss_weighting_generate_graph", False))
        self.widget.graph_output_input.setText(args.get("edm2_loss_weighting_generate_graph_output_dir", ""))
        self.widget.graph_steps_input.setValue(int(args.get("edm2_loss_weighting_generate_graph_every_x_steps", 10)))
        self.widget.graph_y_limit_input.setValue(int(args.get("edm2_loss_weighting_generate_graph_y_limit", 5)))
        
        self.enable_disable(self.widget.enable_checkbox.isChecked())
        return True