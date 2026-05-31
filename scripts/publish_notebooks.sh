#!/bin/bash

# TODO: REVIEW THIS AI CODE BEFORE RUNNING!!!!
set -e

# Usage: bash scripts/publish_notebooks.sh "your commit message"
COMMIT_MSG=${1:-"Update notebooks and README"}

echo "=== Running notebooks ==="
find $NOTEBOOKS_DIR -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" | while read nb; do
    echo "Running $nb..."
    jupyter nbconvert --to notebook --execute --inplace \
        --ExecutePreprocessor.timeout=300 "$nb"
done

echo "=== Updating README ==="
python scripts/update_readme.py 
echo "✅ Updated readme!"

echo "=== Pushing to GitHub ==="
./scripts/update_code.sh "$COMMIT_MSG"

echo "✅ FINISHED PUBLISHING NOTEBOOKS!!!"
