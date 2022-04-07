# Tutorial

## Pushing a local dataset to the 🤗 hub

We can upload an ImageFolder style dataset to the hub directly using `hugit`. An ImageFolder dataset is where the labels are encoded in the part of the folder structure. This often looks something like:

```
data/
    Dog/
        Image1.jpg
    Cat/
        Image1.jpg
```

Where `dog` and `cat` refer to the label of the images contained witin that folder. This type of folder structure is often used for sharing machine learning datasets. It is also one of the possible output formats we might have from an annotation tool. To upload our local data from our machine (or server) to the Hugging Face hub.

Let's have a look at the help for the `push_image_dataset` command.

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
  --train-directory TEXT        Name of train directory
  --valid-directory TEXT        name of valid directory
  --test-directory TEXT         name of test directory
  --repo-id TEXT                Repo id for the Hugging Face Hub  [required]
  --private / --no-private      Whether to keep dataset private on the Hub
                                [default: private]
  --do-resize / --no-do-resize  Whether to resize images before upload
                                [default: do-resize]
  --size INTEGER                Size to resize image. This will be used on the
                                shortest side of the image i.e. the aspect rato
                                will be maintained  [default: 224]
  --help                        Show this message and exit.

```

<!-- [[[end]]] -->

As you can see we have to pass `hugit` some required arguments and some options.

```bash
hugit load_image_dataset cifar10 --repo-id davanstrin/cifar10
```

## Configuration

When we upload an image to the Hugging Face Hub using `hugit` we have a few settings we can configure. These settings include the hugginface hub ID for where the model will be stored e.g. `davanstrien/CIFAR10` and whether to resize your images before uploading. There are two types of setting:

- optional: these you can specify or not
- required: these you must tell hugit about

There are two main ways in which we can specify these settings:

- through the command line interface of `hugit`
- through a `TOML` configuration file.

### Passing settings through the Command-Line

```
--do-resize
```

### Storing settings in a configuration file

You can also specify your setting in a `TOML` configuration file. `TOML`

As an example configuration

```toml
[tool.huggit]
hub_id = "davanstrien/CIFAR10"
do_resize = true
size = 224

```

### Which format to use?

The command line overwrites the toml configs
settings which don't change much can be stored in config

### Example
