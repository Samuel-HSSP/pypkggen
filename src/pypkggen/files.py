PP_TOML = """[build-system]
requires = [
    "setuptools>=42",
    "wheel"
]
build-backend = "setuptools.build_meta"
"""


INIT = """\"""
{}
\"""
__title__ = "{}"
__author__ = "{}"

"""

MANIFEST = """include pat1 pat2...
exclude pat1 pat2...
recursive-include dir-pattern pat1 pat2...
recursive-exclude dir-pattern pat1 pat2...
global-include pat1 pat2...
global-exclude pat1 pat2...
graft dir-pattern
prune dir-pattern
"""

SETUP = """[metadata]
name = {}
version = {}
author = {}
author_email = {}
description = {}
long_description = file: README.md
long_description_content_type = text/markdown
url = {}
project_urls =
    Bug Tracker = {}
classifiers =
    Programming Language :: Python :: 3
    License :: {}
    Operating System :: {}

[options]
package_dir =
    = src
packages = find:
python_requires = {}
install_requires =
{}
[options.packages.find]
where = src
"""
