"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Hugit."""


if __name__ == "__main__":
    main(prog_name="hugit")  # pragma: no cover
