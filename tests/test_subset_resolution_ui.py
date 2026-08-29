"""Functional tests for subset-level resolution and bucket overrides."""

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

pytest.importorskip("PySide6")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PySide6.QtWidgets import QApplication

from main_ui_files.MainUI import MainWidget
from main_ui_files.SubsetListUI import SubsetListWidget


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def subset_list(qapp):
    widget = SubsetListWidget()
    yield widget
    widget.deleteLater()


def test_subset_overrides_are_saved_and_can_be_cleared(subset_list):
    subset = subset_list.add_empty_subset("test")

    subset.resolution_override_enable.setChecked(True)
    subset.resolution_width_input.setValue(640)
    subset.resolution_height_input.setValue(768)
    subset.min_bucket_override_enable.setChecked(True)
    subset.min_bucket_reso_input.setValue(512)
    subset.max_bucket_override_enable.setChecked(True)
    subset.max_bucket_reso_input.setValue(1536)

    assert subset.dataset_args["resolution"] == [640, 768]
    assert subset.dataset_args["min_bucket_reso"] == 512
    assert subset.dataset_args["max_bucket_reso"] == 1536
    assert subset_list.dataset_args["test"]["resolution"] == [640, 768]

    subset.resolution_override_enable.setChecked(False)
    subset.min_bucket_override_enable.setChecked(False)
    subset.max_bucket_override_enable.setChecked(False)

    assert "resolution" not in subset.dataset_args
    assert "min_bucket_reso" not in subset.dataset_args
    assert "max_bucket_reso" not in subset.dataset_args
    assert "resolution" not in subset_list.dataset_args["test"]


def test_unchecked_controls_display_inherited_values(subset_list):
    subset_list.set_inherited_dataset_args(
        {"resolution": [640, 768], "min_bucket_reso": 320, "max_bucket_reso": 1280}
    )
    subset = subset_list.add_empty_subset("test")

    assert not subset.resolution_override_enable.isChecked()
    assert not subset.resolution_width_input.isEnabled()
    assert not subset.resolution_height_input.isEnabled()
    assert subset.resolution_width_input.value() == 640
    assert subset.resolution_height_input.value() == 768
    assert not subset.min_bucket_override_enable.isChecked()
    assert not subset.min_bucket_reso_input.isEnabled()
    assert subset.min_bucket_reso_input.value() == 320
    assert not subset.max_bucket_override_enable.isChecked()
    assert not subset.max_bucket_reso_input.isEnabled()
    assert subset.max_bucket_reso_input.value() == 1280

    subset_list.set_inherited_dataset_args(
        {"resolution": 896, "min_bucket_reso": 256, "max_bucket_reso": 1024}
    )
    assert subset.resolution_width_input.value() == 896
    assert subset.resolution_height_input.value() == 896
    assert subset.min_bucket_reso_input.value() == 256
    assert subset.max_bucket_reso_input.value() == 1024


def test_loading_subset_overrides_restores_controls_and_values(qapp):
    widget = SubsetListWidget()
    widget.load_dataset_args(
        {
            "subsets": [
                {
                    "name": "test",
                    "image_dir": "x",
                    "resolution": [640, 768],
                    "min_bucket_reso": 512,
                    "max_bucket_reso": 1536,
                }
            ]
        }
    )
    subset = widget.elements[0]

    assert subset.resolution_override_enable.isChecked()
    assert subset.resolution_width_input.value() == 640
    assert subset.resolution_height_input.value() == 768
    assert subset.min_bucket_override_enable.isChecked()
    assert subset.min_bucket_reso_input.value() == 512
    assert subset.max_bucket_override_enable.isChecked()
    assert subset.max_bucket_reso_input.value() == 1536
    assert widget.dataset_args["test"]["resolution"] == [640, 768]
    assert widget.dataset_args["test"]["min_bucket_reso"] == 512
    assert widget.dataset_args["test"]["max_bucket_reso"] == 1536
    widget.deleteLater()


def test_main_widget_propagates_parent_values_to_unchecked_subset(qapp):
    widget = MainWidget()
    subset = widget.subset_widget.elements[0]
    general = widget.args_widget.args_widget_array[0]
    bucket = next(item for item in widget.args_widget.args_widget_array if item.name == "bucket_args")

    assert subset.resolution_width_input.value() == general.widget.width_input.value()
    assert subset.resolution_height_input.value() == general.widget.height_input.value()
    assert subset.min_bucket_reso_input.value() == bucket.widget.min_input.value()
    assert subset.max_bucket_reso_input.value() == bucket.widget.max_input.value()
    assert not subset.resolution_width_input.isEnabled()
    assert not subset.min_bucket_reso_input.isEnabled()
    assert not subset.max_bucket_reso_input.isEnabled()

    general.widget.width_input.setValue(896)
    bucket.widget.min_input.setValue(320)
    bucket.widget.max_input.setValue(1280)

    assert subset.resolution_width_input.value() == 896
    assert subset.resolution_height_input.value() == 896
    assert subset.min_bucket_reso_input.value() == 320
    assert subset.max_bucket_reso_input.value() == 1280
    widget.deleteLater()
