# Usage

## Loading a local dataset to the 🤗 hub 

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
