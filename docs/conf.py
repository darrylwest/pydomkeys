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

project = 'PyDomKeys'
author = 'Darryl West'

from datetime import datetime
year = datetime.now().year
if year > 2023:
    copyright = f'2023-{year}, {author}'
else:
    copyright = f'2023, {author}'

master_doc = 'index'

import imp
mod = imp.load_source('pydomkeys', '../pydomkeys/__init__.py')
release = mod.__version__

# version = pydomkeys.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.githubpages',
    'sphinx_multiversion',
]

# autoclass_content = 'both'
# html_favicon = '_static/favicon.io'

templates_path = [
    "_templates",
]
html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        "sidebar/versions.html",
        "sidebar/scroll-end.html",
    ],
}
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
