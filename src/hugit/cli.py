"""Command-line interface."""
import click

from hugit import convert
from hugit import image_dataset


@click.group()
def cli():
    """Hugit Command Line"""
    pass  # pragma: no cover


cli.add_command(image_dataset.load_image_dataset)
cli.add_command(convert.convert_format)

if __name__ == "__main__":
    cli()  # pragma: no cover
