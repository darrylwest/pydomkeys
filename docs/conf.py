# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../pydomkeys'))


# -- Project information -----------------------------------------------------

project = 'pydomkeys'
copyright = '2023, Darryl West'
author = 'Darryl West'
master_doc = 'index'
# version = pydomkeys.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.githubpages',
]
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
source_suffix = [".rst", ".md"]

# represent classes as 'Class' rather than 'module.Class'
add_module_names = False
autodoc_typehints = 'none'
autodoc_typehints_format = 'short'
autodoc_preserve_defaults = True

autodoc_default_options = {
    'members': 'True',
    'special-members': '__init__',
}

# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'
