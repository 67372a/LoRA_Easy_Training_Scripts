from PySide6.QtWidgets import QWidget
from ui_files.BucketUI import Ui_bucket_ui
from modules.BaseWidget import BaseWidget


class BucketWidget(BaseWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Bucket Args")
        self.widget = Ui_bucket_ui()

        self.name = "bucket_args"
        self.dataset_args = {}

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)
        # Populate dataset_args with initial widget values
        self.enable_disable(self.widget.bucket_group.isChecked())

    def setup_connections(self) -> None:
        self.widget.bucket_no_upscale.clicked.connect(self.handle_no_upscale_clicked)
        self.widget.multires_training.clicked.connect(self.handle_multires_training_clicked)
        self.widget.min_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("min_bucket_reso", x)
        )
        self.widget.max_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("max_bucket_reso", x)
        )
        self.widget.steps_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("bucket_reso_steps", x)
        )
        self.widget.bucket_group.clicked.connect(self.enable_disable)

    def handle_no_upscale_clicked(self, checked: bool) -> None:
        self.edit_dataset_args("bucket_no_upscale", checked, True)
        if checked:
            self.widget.multires_training.setChecked(False)
            self.edit_dataset_args("multires_training", False, True)

    def handle_multires_training_clicked(self, checked: bool) -> None:
        self.edit_dataset_args("multires_training", checked, True)
        if checked:
            self.widget.bucket_no_upscale.setChecked(False)
            self.edit_dataset_args("bucket_no_upscale", False, True)

    def enable_disable(self, checked: bool) -> None:
        self.dataset_args = {}
        if not checked:
            self.edit_dataset_args("enable_bucket", False)
            return
        self.edit_dataset_args("enable_bucket", True)
        self.edit_dataset_args(
            "bucket_no_upscale", self.widget.bucket_no_upscale.isChecked(), True
        )
        self.edit_dataset_args(
            "multires_training", self.widget.multires_training.isChecked(), True
        )
        self.edit_dataset_args("min_bucket_reso", self.widget.min_input.value())
        self.edit_dataset_args("max_bucket_reso", self.widget.max_input.value())
        self.edit_dataset_args("bucket_reso_steps", self.widget.steps_input.value())

    def load_dataset_args(self, dataset_args: dict) -> bool:
        dataset_args: dict = dataset_args.get(self.name, {})

        # update element inputs - use widget's current value as default if not in saved config
        self.widget.bucket_group.setChecked(dataset_args.get("enable_bucket", self.widget.bucket_group.isChecked()))
        no_upscale = dataset_args.get("bucket_no_upscale", self.widget.bucket_no_upscale.isChecked())
        multires = dataset_args.get("multires_training", self.widget.multires_training.isChecked())
        if no_upscale and multires:
            multires = False

        self.widget.bucket_no_upscale.setChecked(no_upscale)
        self.widget.multires_training.setChecked(multires)
        self.widget.min_input.setValue(dataset_args.get("min_bucket_reso", self.widget.min_input.value()))
        self.widget.max_input.setValue(dataset_args.get("max_bucket_reso", self.widget.max_input.value()))
        self.widget.steps_input.setValue(dataset_args.get("bucket_reso_steps", self.widget.steps_input.value()))

        # edit dataset_args to match
        self.enable_disable(self.widget.bucket_group.isChecked())
        return True
