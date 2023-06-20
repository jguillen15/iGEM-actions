#!/bin/sh

# Install dependencies
# TODO: Install node
pip install -r requirements.txt

# Directories and excel
python3 scripts/regularize_directories.py
python3 scripts/export_csvs.py
python3 scripts/export_sbol.py

# Retrieve parts
python3 scripts/import_parts.py
python3 scripts/convert_sbol_2to3.py

# Build package
python3 scripts/collate_packages.py
python3 scripts/expand_combinations.py
python3 scripts/generate_markdown.py

# Build distribution
python3 scripts/build_distribution.py
