# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'Bot Maker'
copyright = '2020, Blank'
author = 'Blank'
# The full version, including alpha/beta/rc tags
release = 'now'
autodoc_mock_imports = ["discord"]

# -- General configuration ---------------------------------------------------

import sphinx_rtd_theme
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon', "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode", "sphinx_rtd_theme", "recommonmark"]

autoclass_content = 'both'
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
autodoc_member_order = 'bysource'

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
