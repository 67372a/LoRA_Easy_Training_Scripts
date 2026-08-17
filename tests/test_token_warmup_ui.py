"""Functional tests for token warmup enable/disable UI behavior.

These tests verify that disabling the Token Warmup group clears
``token_warmup_min`` and ``token_warmup_step`` from the subset args *and*
propagates that removal to the parent ``SubsetListWidget`` so stale values are
not saved to the training TOML.

Run from the repo root:

    python -m pytest tests/test_token_warmup_ui.py -v
"""

import os
import sys
from pathlib import Path

# Must be set before PySide6 is imported to allow headless test runs.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

pytest.importorskip("PySide6")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PySide6.QtWidgets import QApplication

from main_ui_files.SubsetListUI import SubsetListWidget
from main_ui_files.SubsetUI import SubsetWidget


@pytest.fixture(scope="module")
def qapp():
    """Single QApplication instance for all UI tests in this module."""
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def subset_list(qapp):
    widget = SubsetListWidget()
    yield widget
    widget.deleteLater()


def _assert_token_warmup_cleared(subset: SubsetWidget, subset_list: SubsetListWidget) -> None:
    assert "token_warmup_min" not in subset.dataset_args
    assert "token_warmup_step" not in subset.dataset_args
    assert "token_warmup_min" not in subset_list.dataset_args[subset.name]
    assert "token_warmup_step" not in subset_list.dataset_args[subset.name]


def test_disable_clears_subset_and_parent_args(subset_list: SubsetListWidget) -> None:
    """Disabling token warmup must remove both keys from both stored dicts."""
    subset = subset_list.add_empty_subset("test")

    subset.enable_disable_token_warmup(True)
    assert subset_list.dataset_args["test"]["token_warmup_min"] == 1
    assert subset_list.dataset_args["test"]["token_warmup_step"] == 1

    subset.enable_disable_token_warmup(False)
    _assert_token_warmup_cleared(subset, subset_list)


def test_enable_reads_current_spinbox_values(subset_list: SubsetListWidget) -> None:
    """Enabling token warmup should capture the values in the spin boxes."""
    subset = subset_list.add_empty_subset("test")

    subset.extra_widget.token_warmup_group.setChecked(True)
    subset.extra_widget.token_minimum_warmup_input.setValue(5)
    subset.extra_widget.token_warmup_step_input.setValue(10)

    assert subset.dataset_args["token_warmup_min"] == 5
    assert subset.dataset_args["token_warmup_step"] == 10
    assert subset_list.dataset_args["test"]["token_warmup_min"] == 5
    assert subset_list.dataset_args["test"]["token_warmup_step"] == 10


def test_load_without_token_warmup_leaves_args_cleared(qapp) -> None:
    """Loading a config without token warmup should not add the values."""
    widget = SubsetListWidget()
    widget.load_dataset_args(
        {
            "subsets": [
                {
                    "image_dir": "x",
                    "num_repeats": 1,
                    "caption_extension": ".txt",
                    "name": "test",
                }
            ]
        }
    )
    subset = widget.elements[0]
    _assert_token_warmup_cleared(subset, widget)
    widget.deleteLater()


def test_load_with_token_warmup_restores_values(qapp) -> None:
    """Loading a config with token warmup should restore both values."""
    widget = SubsetListWidget()
    widget.load_dataset_args(
        {
            "subsets": [
                {
                    "image_dir": "x",
                    "num_repeats": 1,
                    "caption_extension": ".txt",
                    "name": "test",
                    "token_warmup_min": 3,
                    "token_warmup_step": 7,
                }
            ]
        }
    )
    subset = widget.elements[0]

    assert subset.dataset_args["token_warmup_min"] == 3
    assert subset.dataset_args["token_warmup_step"] == 7
    assert widget.dataset_args["test"]["token_warmup_min"] == 3
    assert widget.dataset_args["test"]["token_warmup_step"] == 7
    widget.deleteLater()
