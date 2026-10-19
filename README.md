# Wodby platform and stacks documentation

[![Build Status](https://github.com/wodby/docs/workflows/Build%20docs/badge.svg)](https://github.com/wodby/docs/actions)

See https://wodby.com/docs

Docs built using [mkdocs](http://www.mkdocs.org) with [material theme](https://github.com/squidfunk/mkdocs-material)

Custom theme CSS, JavaScript, logos, and favicons receive content-hashed filenames
at build time through `scripts/version_assets.py` (MkDocs 1.6 or newer). Edit the
source assets normally; their public URLs change automatically when their contents
change. Material's bundled assets already use versioned filenames.

Run the asset-versioning checks with `python -m unittest discover -s scripts`.
