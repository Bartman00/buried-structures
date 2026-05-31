#!/bin/bash

# TODO: REVIEW THIS AI CODE BEFORE RUNNING!!!!
set -e

# Usage: bash scripts/publish_notebooks.sh "your commit message"
COMMIT_MSG=${1:-"Update notebooks and README"}

GITHUB_USER="Bartman00"
GITHUB_REPO="your-repo"
BRANCH="main"
NOTEBOOKS_DIR="notebooks"

echo "=== Running notebooks ==="
find $NOTEBOOKS_DIR -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" | while read nb; do
    echo "Running $nb..."
    jupyter nbconvert --to notebook --execute --inplace \
        --ExecutePreprocessor.timeout=300 "$nb"
done

echo "=== Updating README ==="
python scripts/update_readme.py 

echo "=== Pushing to GitHub ==="
./scripts/update_code.sh

echo "=== Done ==="
