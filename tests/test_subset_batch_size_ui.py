"""Functional tests for subset-level batch size overrides."""

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


def test_subset_batch_size_override_is_saved_and_can_be_cleared(subset_list):
    subset = subset_list.add_empty_subset("test")

    subset.batch_size_override_enable.setChecked(True)
    subset.batch_size_input.setValue(2)

    assert subset.dataset_args["batch_size"] == 2
    assert subset_list.dataset_args["test"]["batch_size"] == 2

    subset.batch_size_override_enable.setChecked(False)

    assert "batch_size" not in subset.dataset_args
    assert "batch_size" not in subset_list.dataset_args["test"]


def test_unchecked_batch_size_displays_inherited_value(subset_list):
    subset_list.set_inherited_dataset_args({"batch_size": 4})
    subset = subset_list.add_empty_subset("test")

    assert not subset.batch_size_override_enable.isChecked()
    assert not subset.batch_size_input.isEnabled()
    assert subset.batch_size_input.value() == 4

    subset_list.set_inherited_dataset_args({"batch_size": 8})
    assert subset.batch_size_input.value() == 8


def test_loading_subset_batch_size_restores_controls(subset_list):
    subset_list.load_dataset_args(
        {
            "subsets": [
                {
                    "name": "test",
                    "image_dir": "x",
                    "batch_size": 2,
                }
            ]
        }
    )
    subset = subset_list.elements[0]

    assert subset.batch_size_override_enable.isChecked()
    assert subset.batch_size_input.value() == 2
    assert subset_list.dataset_args["test"]["batch_size"] == 2


def test_loading_subset_without_batch_size_leaves_override_unchecked(subset_list):
    subset_list.load_dataset_args(
        {
            "subsets": [
                {
                    "name": "test",
                    "image_dir": "x",
                }
            ]
        }
    )
    subset = subset_list.elements[0]

    assert not subset.batch_size_override_enable.isChecked()
    assert not subset.batch_size_input.isEnabled()
    assert "batch_size" not in subset_list.dataset_args["test"]


def test_main_widget_propagates_parent_batch_size_to_unchecked_subset(qapp):
    widget = MainWidget()
    subset = widget.subset_widget.elements[0]
    general = widget.args_widget.args_widget_array[0]

    assert subset.batch_size_input.value() == general.widget.batch_size_input.value()
    assert not subset.batch_size_input.isEnabled()

    general.widget.batch_size_input.setValue(4)

    assert subset.batch_size_input.value() == 4
    widget.deleteLater()
