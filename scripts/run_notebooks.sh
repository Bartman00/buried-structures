#!/bin/bash
set -e
find notebooks/ -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" | while read nb; do
    echo "Running $nb..."
    jupyter nbconvert --to notebook --execute --inplace \
        --ExecutePreprocessor.timeout=300 "$nb"
done
echo "Done."