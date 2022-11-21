"""Tests for convert module."""

# mypy: allow-untyped-defs

import pathlib
from pathlib import Path

import pytest
from click.testing import CliRunner
from PIL import Image

from hugit import convert
from hugit.cli import cli


# flake8: noqa
# mypy: allow-untyped-defs

runner = CliRunner()

Image.init()
IMAGE_EXTENSIONS = [
    ext[1:]
    for ext, image_format in Image.EXTENSION.items()
    if image_format in Image.OPEN
]


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
    """Test image search returns paths"""
    images = list(convert.search_for_images(image_directory))
    assert images
    assert isinstance(images[0], pathlib.Path)
    assert len(images) == 30


runner = CliRunner()


def test_convert_format(image_directory):
    """Test convert format"""
    result = runner.invoke(convert.convert_format, ["--help"])
    assert result.exit_code == 0
    assert image_directory
    runner.invoke(convert.convert_format, ["convert_images", image_directory, ".jpeg"])
