import contextlib
from pathlib import Path

from PySide6.QtCore import QSignalBlocker, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QCheckBox, QFileDialog, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QWidget

from modules.BaseWidget import BaseWidget
from modules.DragDropLineEdit import DragDropLineEdit
from modules.ScrollOnSelect import SpinBox
from ui_files.sub_dataset_extra_input import Ui_sub_dataset_extra_input
from ui_files.sub_dataset_input import Ui_sub_dataset_input


class SubsetWidget(BaseWidget):
    DATASET_DEFAULTS = {
        "num_repeats": 1,
        "caption_extension": ".txt",
        "random_crop_padding_percent": 0.05,
    }
    edited = Signal(dict, str)

    def __init__(
        self, parent: QWidget = None, display_name: str = "", name: str = ""
    ) -> None:
        super().__init__(parent)
        self.colap.set_title(display_name)
        self.colap.set_extra("remove")
        self.widget = Ui_sub_dataset_input()
        self.extra_content = QWidget()
        self.extra_widget = Ui_sub_dataset_extra_input()
        self.name = name
        self.inherited_dataset_args = {}
        self.dataset_args["name"] = self.name

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)
        self.widget.extra_args.add_widget(self.extra_content, "main_widget")
        self.extra_widget.setupUi(self.extra_content)
        self.widget.extra_args.set_title("Optional Args")
        self.widget.image_folder_input.setMode("folder")
        self.widget.image_folder_input.highlight = True
        self.widget.image_folder_selector.setIcon(
            QIcon(str(Path("icons/more-horizontal.svg")))
        )
        self.widget.target_image_folder_input.setMode("folder")
        self.widget.target_image_folder_input.highlight = True
        self.widget.target_image_folder_input.allow_empty = True
        self.widget.target_image_folder_selector.setIcon(
            QIcon(str(Path("icons/more-horizontal.svg")))
        )
        self.widget.masked_image_input.setMode("folder")
        self.widget.masked_image_input.highlight = True
        self.widget.masked_image_selector.setIcon(
            QIcon(str(Path("icons/more-horizontal.svg")))
        )
        self.extra_widget.protected_tags_input.setMode("file", [".txt"])
        self.extra_widget.protected_tags_input.highlight = True
        self.extra_widget.protected_tags_input.allow_empty = True
        self.extra_widget.protected_tags_selector.setIcon(
            QIcon(str(Path("icons/more-horizontal.svg")))
        )

        self._setup_resolution_controls()

        self.extra_widget.face_crop_group.setChecked(False)
        self.extra_widget.caption_dropout_group.setChecked(False)
        self.extra_widget.gamma_aug_group.setChecked(False)
        self.extra_widget.token_warmup_group.setChecked(False)

    def _setup_resolution_controls(self) -> None:
        """Create optional per-subset resolution and bucket controls.

        The source .ui templates are generated and intentionally left
        untouched. These controls are added to the empty grid row at runtime
        so they remain optional and absent values continue to inherit from the
        parent dataset.
        """
        self.resolution_overrides_group = QGroupBox(self.content)
        self.resolution_overrides_group.setObjectName("resolution_overrides_group")
        self.resolution_overrides_group.setTitle("Resolution / Bucket / Batch Size Overrides")
        layout = QFormLayout(self.resolution_overrides_group)
        layout.setObjectName("resolution_overrides_layout")

        self.resolution_override_enable = QCheckBox(self.resolution_overrides_group)
        self.resolution_override_enable.setText("Override resolution")
        self.resolution_width_input = SpinBox(self.resolution_overrides_group)
        self.resolution_width_input.setRange(1, 16384)
        self.resolution_width_input.setValue(1024)
        self.resolution_height_input = SpinBox(self.resolution_overrides_group)
        self.resolution_height_input.setRange(1, 16384)
        self.resolution_height_input.setValue(1024)
        resolution_inputs = QWidget(self.resolution_overrides_group)
        resolution_layout = QHBoxLayout(resolution_inputs)
        resolution_layout.setContentsMargins(0, 0, 0, 0)
        resolution_layout.addWidget(QLabel("Width", resolution_inputs))
        resolution_layout.addWidget(self.resolution_width_input)
        resolution_layout.addWidget(QLabel("Height", resolution_inputs))
        resolution_layout.addWidget(self.resolution_height_input)
        layout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.resolution_override_enable)
        layout.setWidget(0, QFormLayout.ItemRole.FieldRole, resolution_inputs)

        self.min_bucket_override_enable = QCheckBox(self.resolution_overrides_group)
        self.min_bucket_override_enable.setText("Override min bucket size")
        self.min_bucket_reso_input = SpinBox(self.resolution_overrides_group)
        self.min_bucket_reso_input.setRange(1, 16384)
        self.min_bucket_reso_input.setSingleStep(64)
        self.min_bucket_reso_input.setValue(256)
        layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.min_bucket_override_enable)
        layout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.min_bucket_reso_input)

        self.max_bucket_override_enable = QCheckBox(self.resolution_overrides_group)
        self.max_bucket_override_enable.setText("Override max bucket size")
        self.max_bucket_reso_input = SpinBox(self.resolution_overrides_group)
        self.max_bucket_reso_input.setRange(1, 16384)
        self.max_bucket_reso_input.setSingleStep(64)
        self.max_bucket_reso_input.setValue(1024)
        layout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.max_bucket_override_enable)
        layout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.max_bucket_reso_input)

        self.batch_size_override_enable = QCheckBox(self.resolution_overrides_group)
        self.batch_size_override_enable.setText("Override batch size")
        self.batch_size_input = SpinBox(self.resolution_overrides_group)
        self.batch_size_input.setRange(1, 64)
        self.batch_size_input.setValue(1)
        layout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.batch_size_override_enable)
        layout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.batch_size_input)

        self.widget.gridLayout.addWidget(self.resolution_overrides_group, 3, 0, 1, 2)
        self._set_resolution_controls_enabled(False)
        self.min_bucket_reso_input.setEnabled(False)
        self.max_bucket_reso_input.setEnabled(False)
        self.batch_size_input.setEnabled(False)
        self.extra_widget.shuffle_caption_group.setChecked(False)

    def setup_connections(self) -> None:
        self.widget.image_folder_input.textChanged.connect(
            lambda x: self.edit_dataset_args("image_dir", x, True)
        )
        self.widget.image_folder_selector.clicked.connect(
            lambda: self.set_folder_from_dialog(
                "Subset Image Folder", self.widget.image_folder_input
            )
        )
        self.widget.target_image_folder_input.textChanged.connect(
            lambda x: self.edit_dataset_args("target_image_dir", x, True)
        )
        self.widget.target_image_folder_selector.clicked.connect(
            lambda: self.set_folder_from_dialog(
                "Target Image Folder", self.widget.target_image_folder_input, False
            )
         )
        self.widget.masked_image_input.textChanged.connect(
            lambda x: self.edit_dataset_args("conditioning_data_dir", x, True)
        )
        self.widget.masked_image_selector.clicked.connect(
            lambda: self.set_folder_from_dialog(
                "Masked Image Folder", self.widget.masked_image_input, False
            )
        )
        self.widget.repeats_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("num_repeats", x)
        )
        self.widget.shuffle_captions_enable.clicked.connect(
            lambda x: self.edit_dataset_args("shuffle_caption", x, True)
        )
        self.widget.flip_augment_enable.clicked.connect(
            lambda x: self.edit_dataset_args("flip_aug", x, True)
        )
        self.widget.keep_tokens_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("keep_tokens", x, True)
        )
        self.widget.color_augment_enable.clicked.connect(
            lambda x: self.edit_dataset_args("color_aug", x, True)
        )
        self.widget.random_crop_enable.clicked.connect(
            lambda x: self.edit_dataset_args("random_crop", x, True)
        )
        self.widget.random_crop_padding_percent_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("random_crop_padding_percent", x, False)
        )

        self.widget.caption_extension_selector.currentTextChanged.connect(
            lambda x: self.edit_dataset_args("caption_extension", x)
        )
        self.widget.regularization_images_enable.clicked.connect(
            lambda x: self.edit_dataset_args("is_reg", x, True)
        )
        self.widget.validation_images_enable.clicked.connect(
            lambda x: self.edit_dataset_args("is_val", x, True)
        )
        self.extra_widget.face_crop_group.clicked.connect(self.enable_disable_face_crop)
        self.extra_widget.face_crop_width_input.valueChanged.connect(
            lambda: self.enable_disable_face_crop(True)
        )
        self.extra_widget.face_crop_height_input.valueChanged.connect(
            lambda: self.enable_disable_face_crop(True)
        )
        self.extra_widget.caption_dropout_group.clicked.connect(
            self.enable_disable_caption_dropout
        )
        self.extra_widget.caption_dropout_rate_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("caption_dropout_rate", x, True)
        )
        self.extra_widget.caption_epoch_dropout_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("caption_dropout_every_n_epochs", x, True)
        )
        self.extra_widget.caption_tag_dropout_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("caption_tag_dropout_rate", x, True)
        )
        self.extra_widget.gamma_aug_group.clicked.connect(
            self.enable_disable_gamma_aug
        )
        self.extra_widget.gamma_aug_min_input.valueChanged.connect(
            lambda: self.enable_disable_gamma_aug(self.extra_widget.gamma_aug_group.isChecked())
        )
        self.extra_widget.gamma_aug_max_input.valueChanged.connect(
            lambda: self.enable_disable_gamma_aug(self.extra_widget.gamma_aug_group.isChecked())
        )
        self.extra_widget.gamma_aug_rate_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("gamma_aug_rate", x, True)
        )
        self.extra_widget.shuffle_caption_group.clicked.connect(
            self.enable_disable_shuffle_caption_modifers
        )
        self.extra_widget.shuffle_caption_sigma_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("shuffle_caption_sigma", x, True)
        )
        self.extra_widget.token_warmup_group.clicked.connect(
            self.enable_disable_token_warmup
        )
        self.extra_widget.token_minimum_warmup_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("token_warmup_min", x)
        )
        self.extra_widget.token_warmup_step_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("token_warmup_step", x)
        )
        self.extra_widget.protected_tags_input.textChanged.connect(
            lambda x: self.edit_dataset_args("protected_tags_file", x, True)
        )
        self.extra_widget.protected_tags_selector.clicked.connect(
            lambda: self.set_file_from_dialog(
                "Protected Tags File", self.extra_widget.protected_tags_input
            )
        )
        self.resolution_override_enable.toggled.connect(self._update_resolution_override)
        self.resolution_width_input.valueChanged.connect(lambda: self._update_resolution_override(self.resolution_override_enable.isChecked()))
        self.resolution_height_input.valueChanged.connect(lambda: self._update_resolution_override(self.resolution_override_enable.isChecked()))
        self.min_bucket_override_enable.toggled.connect(self._update_min_bucket_override)
        self.min_bucket_reso_input.valueChanged.connect(lambda: self._update_min_bucket_override(self.min_bucket_override_enable.isChecked()))
        self.max_bucket_override_enable.toggled.connect(self._update_max_bucket_override)
        self.max_bucket_reso_input.valueChanged.connect(lambda: self._update_max_bucket_override(self.max_bucket_override_enable.isChecked()))
        self.batch_size_override_enable.toggled.connect(self._update_batch_size_override)
        self.batch_size_input.valueChanged.connect(lambda: self._update_batch_size_override(self.batch_size_override_enable.isChecked()))

    def _set_resolution_controls_enabled(self, enabled: bool) -> None:
        self.resolution_width_input.setEnabled(enabled)
        self.resolution_height_input.setEnabled(enabled)

    def _update_resolution_override(self, checked: bool) -> None:
        self._set_resolution_controls_enabled(checked)
        if not checked:
            self._set_resolution_inputs(self.inherited_dataset_args.get("resolution", 1024))
            self._remove_dataset_override("resolution")
            return
        value = [self.resolution_width_input.value(), self.resolution_height_input.value()]
        self.edit_dataset_args("resolution", value)

    def _update_min_bucket_override(self, checked: bool) -> None:
        self.min_bucket_reso_input.setEnabled(checked)
        if not checked:
            self._set_spinbox_value(self.min_bucket_reso_input, self.inherited_dataset_args.get("min_bucket_reso", 256))
            self._remove_dataset_override("min_bucket_reso")
            return
        self.edit_dataset_args("min_bucket_reso", self.min_bucket_reso_input.value())

    def _update_max_bucket_override(self, checked: bool) -> None:
        self.max_bucket_reso_input.setEnabled(checked)
        if not checked:
            self._set_spinbox_value(self.max_bucket_reso_input, self.inherited_dataset_args.get("max_bucket_reso", 1024))
            self._remove_dataset_override("max_bucket_reso")
            return
        self.edit_dataset_args("max_bucket_reso", self.max_bucket_reso_input.value())

    def _update_batch_size_override(self, checked: bool) -> None:
        self.batch_size_input.setEnabled(checked)
        if not checked:
            self._set_spinbox_value(self.batch_size_input, self.inherited_dataset_args.get("batch_size", 1))
            self._remove_dataset_override("batch_size")
            return
        self.edit_dataset_args("batch_size", self.batch_size_input.value())

    def _remove_dataset_override(self, name: str) -> None:
        self.dataset_args.pop(name, None)
        self.edited.emit(self.dataset_args, self.name)

    @staticmethod
    def _set_spinbox_value(spinbox: SpinBox, value: int) -> None:
        blocker = QSignalBlocker(spinbox)
        spinbox.setValue(int(value))
        del blocker

    def _set_resolution_inputs(self, resolution) -> None:
        if isinstance(resolution, (list, tuple)) and len(resolution) == 2:
            width, height = resolution
        elif resolution is not None:
            width = height = resolution
        else:
            width = height = 1024
        width_blocker = QSignalBlocker(self.resolution_width_input)
        height_blocker = QSignalBlocker(self.resolution_height_input)
        self.resolution_width_input.setValue(int(width))
        self.resolution_height_input.setValue(int(height))
        del width_blocker, height_blocker

    def set_inherited_dataset_args(self, dataset_args: dict) -> None:
        """Update disabled override fields without adding subset config keys."""
        self.inherited_dataset_args = dict(dataset_args)
        if not self.resolution_override_enable.isChecked():
            self._set_resolution_inputs(self.inherited_dataset_args.get("resolution", 1024))
        if not self.min_bucket_override_enable.isChecked():
            self._set_spinbox_value(self.min_bucket_reso_input, self.inherited_dataset_args.get("min_bucket_reso", 256))
        if not self.max_bucket_override_enable.isChecked():
            self._set_spinbox_value(self.max_bucket_reso_input, self.inherited_dataset_args.get("max_bucket_reso", 1024))
        if not self.batch_size_override_enable.isChecked():
            self._set_spinbox_value(self.batch_size_input, self.inherited_dataset_args.get("batch_size", 1))

    def edit_dataset_args(
        self, name: str, value: object, optional: bool = False
    ) -> None:
        super().edit_dataset_args(name, value, optional)
        self.edited.emit(self.dataset_args, self.name)

    def set_folder_from_dialog(
        self,
        title_str: str,
        element: DragDropLineEdit,
        calc_repeats: bool = True,
        path: Path = None,
    ) -> None:
        if path and path.exists():
            file_name = path
        else:
            default_dir = Path(element.text())
            file_name = QFileDialog.getExistingDirectory(
                self,
                title_str,
                dir=str(default_dir) if default_dir.exists() else "",
            )
            if not file_name:
                return
            file_name = Path(file_name)
        element.setText(file_name.as_posix())
        element.update_stylesheet()
        if not calc_repeats:
            return
        with contextlib.suppress(ValueError):
            repeats = int(file_name.name.split("_")[0])
            self.widget.repeats_input.setValue(repeats)

    def set_file_from_dialog(
        self,
        title_str: str,
        element: DragDropLineEdit,
        extensions: str = "Text Files (*.txt);;All Files (*.*)",
    ) -> None:
        """Open file picker dialog for file selection"""
        default_dir = Path(element.text())
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            title_str,
            dir=str(default_dir. parent) if default_dir. exists() else "",
            filter=extensions,
        )
        if not file_name:
            return
        file_name = Path(file_name)
        element.setText(file_name.as_posix())
        element.update_stylesheet()


    def enable_disable_masked_loss(self, checked: bool) -> None:
        if "conditioning_data_dir" in self.dataset_args:
            del self.dataset_args["conditioning_data_dir"]
        self.widget.masked_image_input.setEnabled(checked)
        self.widget.masked_image_selector.setEnabled(checked)
        self.edit_dataset_args(
            "conditioning_data_dir",
            self.widget.masked_image_input.text() if checked else False,
            True,
        )

    def enable_disable_face_crop(self, checked: bool) -> None:
        if "face_crop_aug_range" in self.dataset_args:
            del self.dataset_args["face_crop_aug_range"]
        if not checked:
            return
        self.edit_dataset_args(
            "face_crop_aug_range",
            [
                self.extra_widget.face_crop_width_input.value(),
                self.extra_widget.face_crop_height_input.value(),
            ],
        )

    def enable_disable_caption_dropout(self, checked: bool) -> None:
        args = [
            "caption_dropout_rate",
            "caption_dropout_every_n_epochs",
            "caption_tag_dropout_rate",
        ]
        for arg in args:
            if arg in self.dataset_args:
                del self.dataset_args[arg]
        if not checked:
            return
        self.edit_dataset_args(
            args[0], self.extra_widget.caption_dropout_rate_input.value(), True
        )
        self.edit_dataset_args(
            args[1], self.extra_widget.caption_epoch_dropout_input.value(), True
        )
        self.edit_dataset_args(
            args[2], self.extra_widget.caption_tag_dropout_input.value(), True
        )

    def enable_disable_gamma_aug(self, checked: bool) -> None:
        args = ["gamma_aug", "gamma_aug_range", "gamma_aug_rate"]
        for arg in args:
            if arg in self.dataset_args:
                del self.dataset_args[arg]
        if not checked:
            return
        self.edit_dataset_args("gamma_aug", True, True)
        self.edit_dataset_args(
            "gamma_aug_range",
            [
                self.extra_widget.gamma_aug_min_input.value(),
                self.extra_widget.gamma_aug_max_input.value(),
            ],
        )
        self.edit_dataset_args(
            "gamma_aug_rate", self.extra_widget.gamma_aug_rate_input.value(), True
        )

    def enable_disable_token_warmup(self, checked: bool) -> None:
        args = ["token_warmup_min", "token_warmup_step"]
        for arg in args:
            if arg in self.dataset_args:
                del self.dataset_args[arg]
        if not checked:
            self.edited.emit(self.dataset_args, self.name)
            return
        self.edit_dataset_args(
            args[0], self.extra_widget.token_minimum_warmup_input.value()
        )
        self.edit_dataset_args(
            args[1], self.extra_widget.token_warmup_step_input.value()
        )

    def enable_disable_random_crop(self, checked: bool) -> None:
        if "random_crop" in self.dataset_args:
            del self.dataset_args["random_crop"]
        self.widget.random_crop_enable.setEnabled(not checked)
        self.edit_dataset_args(
            "random_crop",
            False if checked else self.widget.random_crop_enable.isChecked(),
            True,
        )

    def enable_disable_color_aug(self, checked: bool) -> None:
        if "color_aug" in self.dataset_args:
            del self.dataset_args["color_aug"]
        self.widget.color_augment_enable.setEnabled(not checked)
        self.edit_dataset_args(
            "color_aug",
            False if checked else self.widget.color_augment_enable.isChecked(),
            True,
        )

    def enable_disable_keep_tokens(self, checked: bool) -> None:
        if "keep_tokens" in self.dataset_args:
            del self.dataset_args["keep_tokens"]
        self.widget.keep_tokens_input.setEnabled(not checked)
        self.edit_dataset_args(
            "keep_tokens",
            False if checked else self.widget.keep_tokens_input.value(),
            True,
        )

    def enable_disable_random_crop_padding_percent(self, checked: bool) -> None:
        self.widget.random_crop_padding_percent_input.setEnabled(not checked)
        self.edit_dataset_args(
            "random_crop_padding_percent",
            self.widget.random_crop_padding_percent_input.value(),
            True,
        )

    def enable_disable_shuffle_caption_modifers(self, checked: bool) -> None:
        args = ["shuffle_caption_sigma"]
        for arg in args:
            if arg in self.dataset_args:
                del self.dataset_args[arg]
        if not checked:
            return
        self.edit_dataset_args(
            args[0], self.extra_widget.shuffle_caption_sigma_input.value()
        )

    def load_dataset_args(self, dataset_args: dict) -> bool:
        # update element inputs
        self.widget.image_folder_input.setText(dataset_args.get("image_dir", ""))
        self.widget.target_image_folder_input.setText(
            dataset_args.get("target_image_dir", "")
        )
        
        self.widget.masked_image_input.setText(
            dataset_args.get("conditioning_data_dir", "")
        )
        self.widget.repeats_input.setValue(dataset_args.get("num_repeats", 1))
        self.widget.shuffle_captions_enable.setChecked(
            dataset_args.get("shuffle_caption", False)
        )
        self.widget.flip_augment_enable.setChecked(dataset_args.get("flip_aug", False))
        self.widget.keep_tokens_input.setValue(dataset_args.get("keep_tokens", 0))
        self.widget.random_crop_padding_percent_input.setValue(dataset_args.get("random_crop_padding_percent", 0.05))
        self.widget.color_augment_enable.setChecked(
            dataset_args.get("color_aug", False)
        )
        self.widget.random_crop_enable.setChecked(
            dataset_args.get("random_crop", False)
        )
        self.widget.caption_extension_selector.setCurrentText(
            dataset_args.get("caption_extension", ".txt")
        )
        self.widget.regularization_images_enable.setChecked(
            dataset_args.get("is_reg", False)
        )
        self.widget.validation_images_enable.setChecked(
            dataset_args.get("is_val", False)
        )
        self.extra_widget.face_crop_group.setChecked(
            bool(dataset_args.get("face_crop_aug_range", False))
        )
        self.extra_widget.face_crop_width_input.setValue(
            dataset_args.get("face_crop_aug_range", [1.0, 1.0])[0]
        )
        self.extra_widget.face_crop_height_input.setValue(
            dataset_args.get("face_crop_aug_range", [1.0, 1.0])[1]
        )
        self.extra_widget.caption_dropout_group.setChecked(
            any(
                arg in dataset_args
                for arg in [
                    "caption_dropout_rate",
                    "caption_dropout_every_n_epochs",
                    "caption_tag_dropout_rate",
                ]
            )
        )

        self.extra_widget.gamma_aug_group.setChecked(
            bool(dataset_args.get("gamma_aug", False))
        )
        self.extra_widget.gamma_aug_min_input.setValue(
            dataset_args.get("gamma_aug_range", [0.95, 1.05])[0]
        )
        self.extra_widget.gamma_aug_max_input.setValue(
            dataset_args.get("gamma_aug_range", [0.95, 1.05])[1]
        )
        self.extra_widget.gamma_aug_rate_input.setValue(
            dataset_args.get("gamma_aug_rate", 0.5)
        )

        self.extra_widget.shuffle_caption_group.setChecked(
            any(
                arg in dataset_args
                for arg in [
                    "shuffle_caption_sigma",
                ]
            )
        )
        self.extra_widget.caption_dropout_rate_input.setValue(
            dataset_args.get("caption_dropout_rate", 0.0)
        )
        self.extra_widget.caption_epoch_dropout_input.setValue(
            dataset_args.get("caption_dropout_every_n_epochs", 0)
        )
        self.extra_widget.caption_tag_dropout_input.setValue(
            dataset_args.get("caption_tag_dropout_rate", 0.0)
        )
        self.extra_widget.shuffle_caption_sigma_input.setValue(
            dataset_args.get("shuffle_caption_sigma", 0)
        )
        self.extra_widget.token_warmup_group.setChecked(
            any(
                arg in dataset_args for arg in ["token_warmup_step", "token_warmup_min"]
            )
        )
        self.extra_widget.token_minimum_warmup_input.setValue(
            dataset_args.get("token_warmup_min", 1)
        )
        self.extra_widget.token_warmup_step_input.setValue(
            dataset_args.get("token_warmup_step", 1)
        )
        self.extra_widget.protected_tags_input.setText(
            dataset_args.get("protected_tags_file", "")
        )

        resolution = dataset_args.get("resolution")
        if isinstance(resolution, (list, tuple)) and len(resolution) == 2:
            resolution_width, resolution_height = resolution
        elif resolution is not None:
            resolution_width = resolution_height = resolution
        else:
            resolution_width = resolution_height = 1024
        self._set_resolution_inputs([resolution_width, resolution_height])
        self.resolution_override_enable.setChecked(resolution is not None)

        min_bucket_reso = dataset_args.get("min_bucket_reso")
        self._set_spinbox_value(self.min_bucket_reso_input, min_bucket_reso if min_bucket_reso is not None else 256)
        self.min_bucket_override_enable.setChecked(min_bucket_reso is not None)

        max_bucket_reso = dataset_args.get("max_bucket_reso")
        self._set_spinbox_value(self.max_bucket_reso_input, max_bucket_reso if max_bucket_reso is not None else 1024)
        self.max_bucket_override_enable.setChecked(max_bucket_reso is not None)

        batch_size = dataset_args.get("batch_size")
        self._set_spinbox_value(self.batch_size_input, batch_size if batch_size is not None else 1)
        self.batch_size_override_enable.setChecked(batch_size is not None)

        # edit dataset args to match
        self.edit_dataset_args("image_dir", self.widget.image_folder_input.text(), True)
        self.edit_dataset_args(
            "target_image_dir", self.widget.target_image_folder_input.text(), True
        )
        self.edit_dataset_args(
            "conditioning_data_dir", self.widget.masked_image_input.text(), True
        )
        self.edit_dataset_args("num_repeats", self.widget.repeats_input.value())
        self.edit_dataset_args(
            "shuffle_caption", self.widget.shuffle_captions_enable.isChecked(), True
        )
        self.edit_dataset_args(
            "flip_aug", self.widget.flip_augment_enable.isChecked(), True
        )
        self.edit_dataset_args(
            "keep_tokens", self.widget.keep_tokens_input.value(), True
        )
        self.edit_dataset_args(
            "color_aug", self.widget.color_augment_enable.isChecked(), True
        )
        self.edit_dataset_args(
            "random_crop", self.widget.random_crop_enable.isChecked(), True
        )
        self.edit_dataset_args(
            "caption_extension", self.widget.caption_extension_selector.currentText()
        )
        self.edit_dataset_args(
            "random_crop_padding_percent", self.widget.random_crop_padding_percent_input.value(), False
        )
        self.edit_dataset_args(
            "is_reg", self.widget.regularization_images_enable.isChecked(), True
        )
        self.edit_dataset_args(
            "is_val", self.widget.validation_images_enable.isChecked(), True
        )
        self.enable_disable_face_crop(self.extra_widget.face_crop_group.isChecked())
        self.enable_disable_caption_dropout(
            self.extra_widget.caption_dropout_group.isChecked()
        )
        self.enable_disable_gamma_aug(
            self.extra_widget.gamma_aug_group.isChecked()
        )
        self.enable_disable_token_warmup(
            self.extra_widget.token_warmup_group.isChecked()
        )
        self.enable_disable_shuffle_caption_modifers(
            self.extra_widget.shuffle_caption_group.isChecked()
        )
        self.edit_dataset_args(
            "protected_tags_file", self.extra_widget.protected_tags_input.text(), True
        )

        self.edited.emit(self.dataset_args, self.name)
