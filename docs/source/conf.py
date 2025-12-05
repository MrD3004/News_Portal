# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Project information -----------------------------------------------------
import django

project = "news_portal"
copyright = "2025, Dian"
author = "Dian"
release = "1.0.0"  # optional, set your project version

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",  # auto-generate docs from docstrings
    "sphinx.ext.viewcode",  # add links to highlighted source code
    "sphinx.ext.napoleon",  # support Google/NumPy style docstrings
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Django setup ------------------------------------------------------------

# Add the project root (where manage.py lives) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Set Django settings module
os.environ["DJANGO_SETTINGS_MODULE"] = "news_portal.settings"

# Initialize Django
django.setup()

# -- Options for HTML output -------------------------------------------------
# cleaner look, requires pip install sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
