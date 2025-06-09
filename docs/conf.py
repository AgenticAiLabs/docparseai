# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'docparseai'
copyright = '2025, Paul Onyekwelu'
author = 'Paul Onyekwelu'
release = '0.1.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",       # For Markdown support
    "sphinx.ext.autodoc",  # Auto API docs from docstrings (optional but useful)
    "sphinx.ext.napoleon", # Support for Google-style/NumPy-style docstrings
    "sphinx.ext.viewcode", # Add links to highlighted source code
]


templates_path = ['_templates']
exclude_patterns = []


# Use Furo theme
html_theme = "furo"
html_static_path = ['_static']


# Allow both .rst and .md files
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

