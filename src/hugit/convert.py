"""Convert images."""
from __future__ import annotations

from pathlib import Path
from typing import Iterator

import click
from PIL import Image
from PIL import UnidentifiedImageError
from rich.progress import track


Image.init()
IMAGE_EXTENSIONS = [
    ext[1:]
    for ext, image_format in Image.EXTENSION.items()
    if image_format in Image.OPEN
]


def search_for_images(directory: Path) -> Iterator[Path]:
    """Yields image files from directory"""
    files = Path(directory).rglob("*")
    for file in files:
        print(file)
        if file.suffix.strip(".") in IMAGE_EXTENSIONS:
            yield file
        else:
            continue


def convert_image(image_file: Path, save_format=".jpeg") -> None:  # pragma: no cover
    """Convert `image_file` to `save_format`"""
    try:
        out_filename = image_file.with_suffix(save_format)
        image = Image.open(image_file)
        image = image.convert("RGB")
        image.save(out_filename)
        image_file.unlink()
    except UnidentifiedImageError:
        image_file.unlink()


@click.command(name="convert_images")
@click.argument(
    "directory",
    type=click.Path(exists=True, dir_okay=True, readable=True, resolve_path=True),
)
@click.argument("save_format", type=click.STRING)
def convert_format(save_format, directory) -> None:
    """Convert images in directory to `save_format`"""
    image_files = search_for_images(directory)
    image_files = search_for_images(directory)
    for file in track(list(image_files)):
        convert_image(file)
