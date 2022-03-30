#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from functools import cached_property
from pathlib import Path
from typing import Dict
from typing import Iterable
from typing import List

from attr import define
from attr import field
from attrs import define
from datasets import Dataset
from datasets import features
from toolz import itertoolz

from hugit.console import console
from hugit.core import get_image_label_from_folder
from hugit.core import get_images


@define
class ImageDataset:
    dataset: Dataset
    label2id: dict[str, int] = field()
    id2label: dict[int, str] = field()

    def __len__(self):
        return len(self.dataset)

    @classmethod
    def from_image_directory(cls, directory: Path) -> ImageDataset:
        image_data = defaultdict(list)
        with console.status(
            f"Loading from {directory}...",
            spinner="dots",
        ):  # pragma: no cover
            image_files = get_images(directory)
            for image_file in image_files:
                image_data["filepath"].append(str(image_file))
                label = get_image_label_from_folder(image_file)
                image_data["label"].append(label)
        dataset = Dataset.from_dict(dict(image_data))
        labels = dataset.unique("label")
        id2label: dict[int, str] = dict(enumerate(labels))
        label2id: dict[str, int] = {label: id_ for id_, label in id2label.items()}
        dataset = dataset.map(lambda example: {"label": label2id[example["label"]]})
        dataset = dataset.cast_column(
            "label", features.ClassLabel(names=list(label2id.keys()))
        )
        dataset = dataset.map(lambda example: {"image": example['filepath']})
        dataset = dataset.cast_column('image',features.Image())
        return cls(dataset, label2id, id2label)

    @property
    def label_frequencies(self) -> dict[str, int]:
        """label frequencies"""
        mapping = self.id2label

        def _yield_labels() -> Iterable[int]:
            for row in self.dataset:
                yield row["label"]

        return itertoolz.frequencies(mapping[label] for label in _yield_labels())

    def push_to_hub(self,repo_id): # pragma: no cover
        """push dataset to hub"""
        self.dataset.push_to_hub(repo_id=repo_id,private=True)
