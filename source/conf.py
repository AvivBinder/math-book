# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = 'ספר מתמטיקה'
copyright = 'כל הזכויות שמורות לאביב בינדר. אין להעתיק או לפרסם אלא ברשותו'
author = 'AvivBinder'
release = '2026'

# -- General configuration ---------------------------------------------------

extensions = ['myst_parser', 'sphinx.ext.mathjax']

templates_path = ['_templates']
exclude_patterns = []

language = 'he'

myst_enable_extensions = ["dollarmath", "amsmath"]

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['rtl.css']
html_show_sourcelink = False
html_show_sphinx = False