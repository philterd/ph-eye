#!/bin/bash -e

for model_file in models/*.py; do
    module=$(basename "$model_file" .py)

    if [ "$module" = "__init__" ]; then
        continue
    fi

    echo "Downloading model: $module"
    PHEYE_MODEL="$module" python3 download_model.py
done

echo "All models downloaded."
