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

# 4. Build the authenticated URL directly from the .env variables
AUTH_URL="https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git"

# 5. Temporarily point Git to the authenticated URL
git remote set-url origin "$AUTH_URL"

# 6. Default message
COMMIT_MSG="${1:-Automated update: $(date +'%Y-%m-%d %H:%M:%S')}"

# 7. Run the Git commands
echo "🚀 Pushing updates to your repository..."
git add .
git commit -m "$COMMIT_MSG"
git push origin "$TARGET_BRANCH"

echo "✅ Push complete!"