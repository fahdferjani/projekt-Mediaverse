# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


from recommonmark.parser import CommonMarkParser
import django
import sys
import os

sys.path.insert(0, os.path.abspath('../..'))  
os.environ['DJANGO_SETTINGS_MODULE'] = 'app_mediaverse.settings'
django.setup()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Mediaverse'
copyright = '2023, irp0'
author = 'irp0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc'
]

source_suffix = ['.rst', '.md', '.MD']

source_parsers = {
    '.md': CommonMarkParser,
    '.MD': CommonMarkParser,
}

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


 