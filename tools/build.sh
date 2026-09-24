#!/bin/sh
# Rebuild the site from the purchased template. Run from the repo root after
# dropping a fresh export in place; each stage is idempotent only against the
# untouched template, so always start from a clean export.
set -e
python3 tools/recolor.py          # template palette -> Global Bridge tokens
python3 tools/logo.py             # template mark -> the GB monogram
python3 tools/rewrite-content.py  # wellness copy -> VIP travel copy
python3 tools/rewrite-js.py       # and in the page modules React hydrates from
python3 tools/rewrite-cms.py      # the same, inside Framer's CMS data files
python3 tools/rewrite-meta.py     # and inside the site search index
