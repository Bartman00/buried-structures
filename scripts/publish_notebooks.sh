#!/bin/bash

# Activate environment
./scripts/activat_env.sh

# Add .env variables
source ./scripts/add_env.sh


if [ ! -d $NOTEBOOKS ]; then
    echo "❌ Error: seed folder '$NOTEBOOKS' not found."
    exit 1
else
    echo "✅ found notebooks folder"
fi

if [ ! -d $DOCS ]; then
    echo "⚠️ Creating '$DOCS' folder."
    mkdir -p "$DOCS"
else
    echo "✅ found docs folder"
    echo "$DOCS"
fi


# Copy all /images subfolders into the docs output tree
find "$NOTEBOOKS" -type d -name "images" | while read -r img_dir; do
    relative="${img_dir#$NOTEBOOKS/}"
    # echo "relative: $relative"

    # Take off last folder for paste or it goes into docs/sub_folder/images/images
    paste_dir="${relative%/*}"
    # echo "paste_dir: $paste_dir"
    # echo "NOTEBOOKS: $NOTEBOOKS"
    # echo "Copying from: $img_dir"
    

    # echo "Copying to: $DOCS/$paste_dir"

    cp -r "$img_dir" "$DOCS/$paste_dir"
    echo "📁 Copied images: $img_dir"
done

find "$NOTEBOOKS" -name "*.ipynb" | while read -r notebook; do
    
    if [[ ! "$notebook" == *"XX"* ]]; then
        # Ignore notebooks with XX in the title like the template

        # Create children folders
        relative="${notebook#$NOTEBOOKS/}"
        out_dir="$DOCS/$(dirname "$relative")"
        mkdir -p "$out_dir"

        echo "Converting: $notebook"
        jupyter nbconvert \
            --to html \
            --execute \
            --ExecutePreprocessor.timeout=300 \
            --output-dir "$out_dir" \
            "$notebook"

        echo "✅ Converted: $notebook"
    fi
done

COMMIT_MSG=${1:-"Update notebooks and README"}




./scripts/update_code.sh "$COMMIT_MSG"


echo "✅ FINISHED PUBLISHING NOTEBOOKS!!!"
