#!/bin/bash

# 1. Dynamically find the absolute path of the folder containing THIS script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# 2. Define the exact path to the expected .env file
ENV_PATH="$SCRIPT_DIR/.env"

# 3. Verify found the .env file
if [ -f "$ENV_PATH" ]; then
    source "$ENV_PATH"

    echo "✅ found .env"
else
    echo "❌ Error: .env file not found!"
    exit 1
fi

