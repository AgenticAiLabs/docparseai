import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'docparseai'
author = 'Paul Onyekwelu'
release = '0.1.1'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser', 
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

html_theme = 'furo'
