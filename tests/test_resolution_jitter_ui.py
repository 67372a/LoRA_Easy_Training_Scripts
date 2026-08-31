"""Functional tests for resolution jitter UI (dataset-level and subset-level)."""

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

pytest.importorskip("PySide6")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PySide6.QtWidgets import QApplication

from main_ui_files.GeneralUI import GeneralWidget
from main_ui_files.MainUI import MainWidget
from main_ui_files.SubsetListUI import SubsetListWidget

JITTER_KEYS = (
    "resolution_jitter_resolutions",
    "resolution_jitter_batch_sizes",
    "resolution_jitter_weights",
)


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def general(qapp):
    widget = GeneralWidget()
    yield widget
    widget.deleteLater()


@pytest.fixture
def subset_list(qapp):
    widget = SubsetListWidget()
    yield widget
    widget.deleteLater()


def _fill_jitter_fields(widget, resolutions="256, 512, 768, 1024", batch_sizes="32, 16, 8, 4", weights="0.25, 0.25, 0.25, 0.25"):
    widget.jitter_resolutions_input.setText(resolutions)
    widget.jitter_batch_sizes_input.setText(batch_sizes)
    widget.jitter_weights_input.setText(weights)


# ---------------------------------------------------------------------------
# dataset-level (GeneralWidget)
# ---------------------------------------------------------------------------


def test_dataset_level_jitter_writes_and_clears_keys(general):
    general.resolution_jitter_enable.setChecked(True)
    _fill_jitter_fields(general)

    assert general.dataset_args["resolution_jitter_resolutions"] == [256, 512, 768, 1024]
    assert general.dataset_args["resolution_jitter_batch_sizes"] == [32, 16, 8, 4]
    assert general.dataset_args["resolution_jitter_weights"] == [0.25, 0.25, 0.25, 0.25]

    general.resolution_jitter_enable.setChecked(False)

    for key in JITTER_KEYS:
        assert key not in general.dataset_args
    assert not general.jitter_resolutions_input.isEnabled()


def test_dataset_level_jitter_invalid_input_is_rejected(general):
    general.resolution_jitter_enable.setChecked(True)
    _fill_jitter_fields(general, batch_sizes="32, 16")

    for key in JITTER_KEYS:
        assert key not in general.dataset_args, "length mismatch must not write keys"

    _fill_jitter_fields(general, weights="0.5, 0.0")
    for key in JITTER_KEYS:
        assert key not in general.dataset_args, "non-positive weights must not write keys"

    _fill_jitter_fields(general)
    assert general.dataset_args["resolution_jitter_resolutions"] == [256, 512, 768, 1024]


def test_dataset_level_jitter_load_dataset_args_round_trip(general):
    general.load_dataset_args(
        {
            "general_args": {
                "resolution": 768,
                "batch_size": 2,
                "resolution_jitter_resolutions": [512, 1024],
                "resolution_jitter_batch_sizes": [16, 4],
                "resolution_jitter_weights": [0.75, 0.25],
            }
        }
    )

    assert general.resolution_jitter_enable.isChecked()
    assert general.jitter_resolutions_input.text() == "512, 1024"
    assert general.jitter_batch_sizes_input.text() == "16, 4"
    assert general.jitter_weights_input.text() == "0.75, 0.25"
    assert general.dataset_args["resolution_jitter_resolutions"] == [512, 1024]

    general.load_dataset_args({"general_args": {"resolution": 512}})
    assert not general.resolution_jitter_enable.isChecked()
    for key in JITTER_KEYS:
        assert key not in general.dataset_args


# ---------------------------------------------------------------------------
# subset-level (SubsetWidget via SubsetListWidget)
# ---------------------------------------------------------------------------


def test_subset_jitter_override_writes_and_clears_keys(subset_list):
    subset = subset_list.add_empty_subset("test")

    subset.jitter_override_enable.setChecked(True)
    _fill_jitter_fields(subset, resolutions="512, 1024", batch_sizes="16, 4", weights="0.75, 0.25")

    assert subset.dataset_args["resolution_jitter_resolutions"] == [512, 1024]
    assert subset.dataset_args["resolution_jitter_batch_sizes"] == [16, 4]
    assert subset.dataset_args["resolution_jitter_weights"] == [0.75, 0.25]
    assert subset_list.dataset_args["test"]["resolution_jitter_resolutions"] == [512, 1024]

    subset.jitter_override_enable.setChecked(False)

    for key in JITTER_KEYS:
        assert key not in subset.dataset_args
        assert key not in subset_list.dataset_args["test"]
    assert not subset.jitter_resolutions_input.isEnabled()


def test_subset_jitter_invalid_override_is_rejected(subset_list):
    subset = subset_list.add_empty_subset("test")

    subset.jitter_override_enable.setChecked(True)
    _fill_jitter_fields(subset, resolutions="512", batch_sizes="16, 4", weights="0.75, 0.25")

    for key in JITTER_KEYS:
        assert key not in subset.dataset_args


def test_subset_jitter_unchecked_displays_inherited_values(subset_list):
    subset_list.set_inherited_dataset_args(
        {
            "resolution_jitter_resolutions": [256, 512],
            "resolution_jitter_batch_sizes": [32, 16],
            "resolution_jitter_weights": [0.5, 0.5],
        }
    )
    subset = subset_list.add_empty_subset("test")

    assert not subset.jitter_override_enable.isChecked()
    assert not subset.jitter_resolutions_input.isEnabled()
    assert subset.jitter_resolutions_input.text() == "256, 512"
    assert subset.jitter_batch_sizes_input.text() == "32, 16"
    assert subset.jitter_weights_input.text() == "0.5, 0.5"

    # clearing the dataset-level config clears the displayed inherited values
    subset_list.set_inherited_dataset_args({})
    assert subset.jitter_resolutions_input.text() == ""


def test_loading_subset_jitter_override_restores_controls(subset_list):
    subset_list.load_dataset_args(
        {
            "subsets": [
                {
                    "name": "test",
                    "image_dir": "x",
                    "resolution_jitter_resolutions": [384, 640],
                    "resolution_jitter_batch_sizes": [8, 2],
                    "resolution_jitter_weights": [0.9, 0.1],
                }
            ]
        }
    )
    subset = subset_list.elements[0]

    assert subset.jitter_override_enable.isChecked()
    assert subset.jitter_resolutions_input.text() == "384, 640"
    assert subset.jitter_batch_sizes_input.text() == "8, 2"
    assert subset.jitter_weights_input.text() == "0.9, 0.1"
    assert subset_list.dataset_args["test"]["resolution_jitter_resolutions"] == [384, 640]


# ---------------------------------------------------------------------------
# propagation (MainWidget)
# ---------------------------------------------------------------------------


def test_main_widget_propagates_jitter_to_unchecked_subsets(qapp):
    widget = MainWidget()
    subset = widget.subset_widget.elements[0]
    general = widget.args_widget.args_widget_array[0]

    general.resolution_jitter_enable.setChecked(True)
    _fill_jitter_fields(general, resolutions="256, 512", batch_sizes="32, 16", weights="0.5, 0.5")

    assert not subset.jitter_override_enable.isChecked()
    assert subset.jitter_resolutions_input.text() == "256, 512"
    assert subset.jitter_batch_sizes_input.text() == "32, 16"
    assert subset.jitter_weights_input.text() == "0.5, 0.5"

    general.resolution_jitter_enable.setChecked(False)
    assert subset.jitter_resolutions_input.text() == ""
    widget.deleteLater()
