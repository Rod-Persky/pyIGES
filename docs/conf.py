#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, time

sys.path.append(os.path.abspath('../'))        # Base folder
sys.path.append(os.path.abspath('./'))         # This folder, for import of examples
#sys.path.append(os.path.abspath('../pyiges'))  # Source code folder
sys.path.append(os.path.abspath('_themes'))    # Themes folder

print("System Path:")
for key in sys.path:
    print('\t', key)


# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.todo',
              'sphinx.ext.doctest',
              'sphinx.ext.mathjax',
              'sphinx.ext.doctest']

todo_include_todos = True

templates_path = ['_themes']

project = 'Python IGES Geometry Library'
copyright = '%s, Rodney Persky' % time.strftime('%Y')

# The short X.Y version.
version = '0.0'
version_file = open("../pyIGESVersion", 'r')
version = version_file.read()
version_file.close()
# The full version, including alpha/beta/rc tags.
release = '%s alpha' % version

rst_epilog = """
.. |project| replace:: {project}""".format(project = project)

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', '_uicache', 'examples/benchmarks/benchmark_links.rst']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme_path = ['_themes']
html_theme = 'sphinx-theme-okfn-master'



html_short_title = 'Documentation'

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True

# Custom sidebar templates, filenames relative to this file.
html_sidebars = {
        '**': ['globaltoc.html', 'localtoc.html', 'relations.html']
    }

# Additional templates that should be rendered to pages.
#html_additional_pages = {
#    'download': 'download.html',
#    'index': 'indexcontent.html',
#}

# Additional static files.
#html_static_path = ['_tools/sphinxext/static']

# Split the index
html_split_index = False

# Output file base name for HTML help builder.
htmlhelp_basename = 'PYIGESGeomTool'


# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
'papersize': 'a4paper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'PYIGESGeomTool.tex', project,
   'Rodney Persky', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'PYIGESGeomTool', project,
     ['Rodney Persky'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'PYIGESGeomTool', project,
   'Rodney Persky', 'PYIGESGeomTool', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False
