"""Core tests."""

import pytest

from hugit import core


@pytest.fixture()
def image_files(tmpdir_factory) -> None:
    """Fixture for image files"""
    a_dir = tmpdir_factory.mktemp("image_dir")
    for fname in range(2000):
        file = a_dir.join(f"file_{fname}.tif")
        file.ensure()
    for fname in range(1000):
        file = a_dir.join(f"file_{fname}.jpg")
        file.ensure()
    return a_dir


def test_print_frequency_dict():
    """Print frequency runs."""
    freqs = {"A": 100, "B": 200}
    core.print_table_from_frequency_dict(freqs)
    core.print_table_from_frequency_dict(freqs, sort_by_value=True)
