"""Sphinx configuration."""
project = "Hugit"
author = "Daniel van Strien"
copyright = "2022, Daniel van Strien"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
