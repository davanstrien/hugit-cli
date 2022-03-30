<<<<<<< Updated upstream
"""Core tests."""
=======
#!/usr/bin/env python3
from pathlib import Path

>>>>>>> Stashed changes
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


<<<<<<< Updated upstream
def test_print_frequency_dict():
    """It runs"""
    freqs = {"A": 100, "B": 200}
    core.print_table_from_frequency_dict(freqs)
    core.print_table_from_frequency_dict(freqs, sort_by_value=True)
=======
def test_get_images(image_files) -> None:
    files = core.get_images(image_files)
    assert files


def test_get_image_labels_from_folder() -> None:
    path = Path("test/label/image_01.png")
    label = core.get_image_label_from_folder(Path(path))
    assert label
    assert isinstance(label, str)
    assert label == "label"
>>>>>>> Stashed changes
