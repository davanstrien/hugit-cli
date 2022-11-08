"""Tests for convert module."""
# mypy: allow-untyped-defs

import pathlib


from pathlib import Path
import numpy as np
import pytest
from PIL import Image
import PIL
from hugit import convert
from PIL import Image


IMAGE_EXTENSIONS = []
Image.init()
for ext, image_format in Image.EXTENSION.items():
    if image_format in Image.OPEN:
        IMAGE_EXTENSIONS.append(ext[1:])


@pytest.fixture()
def image_directory(tmp_path):
    """Fixture for image directory."""
    image_dir = tmp_path / "image_dir"
    image_dir.mkdir()
    for label in ["dog", "cat", "monkey"]:
        label_dir = image_dir / label
        label_dir.mkdir()
        for fname in range(10):
            file = label_dir / f"file_{fname}.tif"
            file.touch()
    return image_dir


def test_search_images(image_directory):
    images = list(convert.search_for_images(image_directory))
    assert images
    assert isinstance(images[0], pathlib.Path)
    assert len(images) == 30
