# Hugit

[![PyPI](https://img.shields.io/pypi/v/hugit.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/hugit.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/hugit)][python version]
[![License](https://img.shields.io/pypi/l/hugit)][license]

[![Read the documentation at https://hugit.readthedocs.io/](https://img.shields.io/readthedocs/hugit-cli/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/davanstrien/hugit-cli/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/davanstrien/hugit-cli/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/hugit/
[status]: https://pypi.org/project/hugit/
[python version]: https://pypi.org/project/hugit
[license]: https://opensource.org/licenses/MIT
[read the docs]: https://hugit-cli.readthedocs.io/
[tests]: https://github.com/davanstrien/hugit/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/davanstrien/hugit
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

**Warning**: this code is very much a work in progress and is primarily being intended for a particular workflow. It may not work well (or at all) for your workflow.

`hugit` is a command line tool for loading ImageFolder style datasets into a 🤗 `datasets` `Dataset` and pushing to the 🤗 hub.

The primary goal of `hugit` is to help quickly get a local dataset into a format that can be used for training computer vision models. `hugit` was developed to support the workflow for [`flyswot`](https://github.com/davanstrien/flyswot/) where we wanted a quicker iteration between creating new training data, training a model, and using the new model inside [`flyswot`](https://github.com/davanstrien/flyswot/).

![hugit workflow diagram](/docs/assets/hugit-workflow.png)

## Supported formats

At the moment **hugit** supports ImageFolder style datasets i.e:

```bash
data/
    dog/
        dog1.jpg
    cat/
        cat.1.jpg

```

## Features

- A command line interface for quickly loading a dataset stored on disk into a 🤗 `datasets.Dataset`
- Push your local dataset to the 🤗 hub
- Get statistics about your dataset. These statistics focus on 'high level' statistic that would be useful to include in Datasheets and Model Cards. Currently these statistics include:
  - label frequencies, organised by split
  - train, test, valid split sizes

## Installation

You can install _Hugit_ via [pip] from [PyPI], inside a virtual environment install `hugit` using

```console
$ pip install hugit
```

Alternatively, you can use [pipx](https://pypa.github.io/pipx/) to install `hugit`

```console
$ pipx install hugit
```

## Usage

You can see help for `hugit` using `hugit --help`

<!-- [[[cog
import cog
from hugit import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["--help"])
help = result.output.replace("Usage: cli", "Usage: hugit")
cog.out(
    "```\n{}\n```".format(help)
)
]]] -->

```
Usage: hugit [OPTIONS] COMMAND [ARGS]...

  Hugit Command Line

Options:
  --help  Show this message and exit.

Commands:
  push_image_dataset  Load an ImageFolder style dataset.

```

<!-- [[[end]]] -->

To load an ImageFolder style dataset onto the 🤗 Hub you can use the `push_image_dataset` command.

<!-- [[[cog
import cog
from hugit import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["push_image_dataset", "--help"])
help = result.output.replace("Usage: cli", "Usage: hugit")
cog.out(
    "```\n{}\n```".format(help)
)
]]] -->

```
Usage: hugit push_image_dataset [OPTIONS] DIRECTORY

  Load an ImageFolder style dataset.

Options:
  --repo-id TEXT                  Repo id for the Hugging Face Hub  [required]
  --private / --no-private        Whether to keep dataset private on the Hub
                                  [default: private]
  --do-resize / --no-do-resize    Whether to resize images before upload
                                  [default: do-resize]
  --size INTEGER                  Size to resize image. This will be used on the
                                  shortest side of the image i.e. the aspect
                                  rato will be maintained  [default: 224]
  --preserve-file-path / --no-preserve-file-path
                                  preserve_orginal_file_path  [default:
                                  preserve-file-path]
  --help                          Show this message and exit.

```

<!-- [[[end]]] -->

Under the hood `hugit` uses [`typed-settings`](https://typed-settings.readthedocs.io/en/latest/index.html), which means that configuration can either be done through the command line or through a `TOML` file. See [usage] for more detailed discussion of how to use `hugit`.

## Contributing

It is likely that _Hugit_ may only work for our particular workflow. With that said if you have suggestions please open an issue.

## License

Distributed under the terms of the [MIT license],
_Hugit_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[cookiecutter]: https://github.com/audreyr/cookiecutter
[mit license]: https://opensource.org/licenses/MIT
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/davanstrien/hugit/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[contributor guide]: https://github.com/davanstrien/hugit/blob/main/CONTRIBUTING.md
[usage]: https://hugit-cli.readthedocs.io/en/latest/usage.html
