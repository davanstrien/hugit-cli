"""Image dataset."""
from __future__ import annotations

from pathlib import Path

import click
import typed_settings as ts
from attrs import define
from datasets import load_dataset
from datasets.dataset_dict import DatasetDict
from PIL.Image import ANTIALIAS
from PIL.Image import Image
from toolz import itertoolz

from hugit import core


def resize_image(image: Image, size: int = 224) -> Image:
    """Resizes an image retaining the aspect ratio."""
    w, h = image.size
    if w == h:
        image = image.resize((size, size), ANTIALIAS)
        return image

    if w > h:
        height_percent = size / float(h)
        width_size = int(float(w) * float(height_percent))
        image = image.resize((width_size, size), ANTIALIAS)
        return image
    if w < h:
        width_percent = size / float(w)
        height_size = int(float(w) * float(width_percent))
        image = image.resize((size, height_size), ANTIALIAS)
        return image


@define
class ImageDataset:
    """ImageDataset container."""

    dataset: DatasetDict
    label2id: dict[str, dict[str, int]]
    id2label: dict[str, dict[int, str]]

    @classmethod
    def from_image_directory(
        cls,
        directory: Path,
        train_dir: Path | None = None,
        valid_dir: Path | None = None,
        test_dir: Path | None = None,
    ):
        """Intilize an ImageDataset from a ImageFolder style dataset."""
        data_files = {}
        if train_dir is not None:
            train_files = directory / Path(train_dir)
            data_files["train"] = f"{train_files}/**/*"
        if valid_dir is not None:
            valid_files = directory / Path(valid_dir)
            data_files["valid"] = f"{valid_files}/**/*"
        if test_dir is not None:
            test_files = directory / Path(test_dir)
            data_files["test"] = f"{test_files}/**/*"
        # if (train_dir and valid_dir and test_dir) is None:
        #     data_files["train"] = f"{directory}"
        if data_files:
            ds = load_dataset("imagefolder", data_files=data_files)
        else:
            ds = load_dataset("imagefolder", data_dir=str(directory))
        if isinstance(ds, DatasetDict):
            id2labels = {}
            label2ids = {}
            for split in ds:
                id2label = dict(enumerate(ds[split].features["label"].names))
                label2id = {v: k for k, v in id2label.items()}
                label2ids[split] = label2id
                id2labels[split] = id2label
            return cls(ds, label2ids, id2labels)

    @property
    def label_frequencies(self) -> dict[str, dict[str, int]]:
        """Return the frequency of labels."""
        frequencies_dict = {}
        for split in self.dataset:
            labels = self.dataset[split]["label"]
            mapping = self.id2label[split]
            frequencies_dict[split] = dict(
                itertoolz.frequencies([mapping[label] for label in labels])
            )
        return frequencies_dict

    def resize_images(self, size=448, writer_batch_size=8):
        """Resizes images to `size` with `writer_batch_size`."""
        self.dataset = self.dataset.map(
            lambda example: {"image": resize_image(example["image"])},
            writer_batch_size=writer_batch_size,
        )

    def push_to_hub(self, repo_id: str) -> None:  # pragma: no cover
        """Push dataset to hub at `repo_id`."""
        self.dataset.push_to_hub(
            repo_id=repo_id, private=True, embed_external_files=True
        )


@ts.settings
class Settings:
    """A container for settings."""

    repo_id: str = ts.option(help="Repo id for the Hugging Face Hub")
    private: bool = ts.option(
        default=True, help="Whether to keep dataset private on the Hub"
    )
    do_resize: bool = ts.option(
        default=False, help="Whether to resize images before upload"
    )
    size: int = ts.option(
        default=None,
        help="""Size to resize image.
        This will be used on the shortest side of the image
        i.e. the aspect rato will be maintained""",
    )


@click.command(name="load_image_dataset")
@click.argument(
    "directory",
    type=click.Path(exists=True, dir_okay=True, readable=True, resolve_path=True),
)
@click.option("--train-directory", help="Name of train directory", type=str)
@click.option("--valid-directory", help="name of valid directory", type=str)
@click.option("--test-directory", help="name of test directory", type=str)
@ts.click_options(
    Settings,
    ts.default_loaders(
        appname="load_image_dataset",
        config_files=[ts.find("project.toml")],
        config_file_section="tool.huggit",
        env_prefix=None,
    ),
)
def load_image_dataset(
    settings, directory, test_directory, valid_directory, train_directory
):
    """Load an ImageFolder style dataset."""
    dataset = ImageDataset.from_image_directory(
        directory,
        train_dir=train_directory,
        test_dir=test_directory,
        valid_dir=valid_directory,
    )
    label_freqs = dataset.label_frequencies
    for split_name, label_freq in label_freqs.items():
        print(split_name)
        core.print_table_from_frequency_dict(frequency_dict=label_freq)
    if settings.do_resize:
        dataset.resize_images(size=settings.size)
    dataset.push_to_hub(repo_id=settings.repo_id)


if __name__ == "__main__":
    load_image_dataset()  # pragma: no cover
