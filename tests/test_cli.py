"""Tests for cli module."""
import pytest
from click.testing import CliRunner

from hugit.cli import cli


# flake8: noqa
# mypy: allow-untyped-defs

runner = CliRunner()


def test_main_cli() -> None:
    """Basic tests for Cli"""
    result = runner.invoke(cli)
    assert result.exit_code == 0
    result = runner.invoke(cli, ["load_image_dataset"])
    assert result.exit_code == 0
