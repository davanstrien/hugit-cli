"""Tests for dataset module."""
# mypy: allow-untyped-defs

from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from hugit import image_dataset


# @pytest.fixture()
# def image_files(tmpdir_factory):
#     """Fixture for image files"""
#     image_dir = tmpdir_factory.mktemp("image_dir")
#     for fname in range(2000):
#         file = image_dir.join(f"file_{fname}.tif")
#         file.ensure()
#     for fname in range(1000):
#         file = image_dir.join(f"file_{fname}.jpg")
#         file.ensure()
#     return image_dir


@pytest.fixture()
def image_directory(tmp_path):
    """Fixture for image directory."""
    image_dir = tmp_path / "image_dir"
    print(image_dir)
    image_dir.mkdir()
    for label in ["dog", "cat", "monkey"]:
        label_dir = image_dir / label
        label_dir.mkdir()
        for fname in range(100):
            file = label_dir / f"file_{fname}.jpg"
            file.touch()
    return image_dir


def test_imagedataset(image_directory):
    """Tests imagedataset."""
    assert Path(image_directory / "monkey").exists()
    dataset = image_dataset.ImageDataset.from_image_directory(image_directory)
    assert dataset
    assert isinstance(dataset, image_dataset.ImageDataset)
    for split in dataset.dataset:
        assert len(dataset.dataset[split].unique("label")) == 3
    assert dataset.label_frequencies
    assert isinstance(dataset.label_frequencies, dict)
    freqs = dataset.label_frequencies
    freqs = freqs["train"]
    assert not set(freqs.keys()).difference({"dog", "cat", "monkey"})


@pytest.fixture()
def image_directory_with_folder(tmp_path):
    """Fixture for image directory."""
    image_dir = tmp_path / "image_dir"
    print(image_dir)
    image_dir.mkdir()
    for split in ["train", "test"]:
        split_dir = image_dir / split
        split_dir.mkdir()
        for label in ["dog", "cat", "monkey"]:
            label_dir = split_dir / label
            label_dir.mkdir()
            for fname in range(100):
                file = label_dir / f"file_{fname}.jpg"
                file.touch()
    return image_dir


def test_image_dataset_with_test(image_directory_with_folder):
    """Tests imagedataset with test folder."""
    dataset = image_dataset.ImageDataset.from_image_directory(
        image_directory_with_folder, train_dir="train", test_dir="test"
    )
    assert dataset


def create_image(w, h):
    """Create an image for testing"""
    data = np.zeros((h, w, 3), dtype=np.uint8)
    return Image.fromarray(data, "RGB")


test_images = [((224, 224), (224, 224)), ((512, 512), (512, 512))]


@pytest.mark.parametrize("image_size,expected", test_images)
def test_image(image_size, expected):
    """Test test image"""
    image = create_image(image_size[0], image_size[1])
    assert image
    assert isinstance(image, Image.Image)
    w, h = image.size
    assert w, h == expected


test_image_resize = [((224, 224), (224, 224), 224)]


# @pytest.mark.parametrize("image,expected,resize",test_image_resize)
def test_resize_image():
    """It resizes images"""
    w, h = 512, 512
    image = create_image(w, h)
    resized = image_dataset.resize_image(image, size=224)
    assert resized
    assert isinstance(resized, Image.Image)
    w, h = resized.size
    assert w == 224
    assert h == 224


def test_resize_image_not_square():
    """It resizes images"""
    w, h = 250, 512
    image = create_image(w, h)
    resized = image_dataset.resize_image(image, size=224)
    assert resized
    assert isinstance(resized, Image.Image)
    w, h = resized.size
    assert w == 224
    w, h = 512, 250
    image = create_image(w, h)
    resized = image_dataset.resize_image(image, size=224)
    assert resized
    assert isinstance(resized, Image.Image)
    w, h = resized.size
    assert h == 224
