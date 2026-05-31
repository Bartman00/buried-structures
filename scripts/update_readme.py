# Update the readme for notebooks because Github
# can't reliably show jupyter notebooks.

# TODO: Review this AI slop code before using.


import os
import re
import argparse
from pathlib import Path
import json

def get_notebook_title(nb_path):
    """Extract title from first markdown cell, fallback to filename."""
    with open(nb_path) as f:
        nb = json.load(f)
    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            for line in cell["source"]:
                line = line.strip()
                if line.startswith("#"):
                    return line.lstrip("#").strip()
    return Path(nb_path).stem.replace("_", " ").title()

def build_notebooks_section(user, repo, branch, notebooks_dir):
    """Build the Notebooks section of the README."""
    base_url = f"https://nbviewer.org/github/{user}/{repo}/blob/{branch}"
    
    # Group notebooks by subfolder
    folders = {}
    for nb_path in sorted(Path(notebooks_dir).rglob("*.ipynb")):
        if ".ipynb_checkpoints" in str(nb_path):
            continue
        folder = nb_path.parent
        folders.setdefault(folder, []).append(nb_path)

    lines = ["## Notebooks\n"]

    for folder, notebooks in sorted(folders.items()):
        # Subfolder header (skip if root notebooks/ folder)
        if folder != Path(notebooks_dir):
            rel_folder = folder.relative_to(notebooks_dir)
            lines.append(f"\n### {str(rel_folder).replace(os.sep, ' / ').title()}\n")

        lines.append("| Notebook | Description |")
        lines.append("|----------|-------------|")
        for nb_path in notebooks:
            title = get_notebook_title(nb_path)
            url = f"{base_url}/{nb_path.as_posix()}"
            lines.append(f"| [{title}]({url}) | |")
        lines.append("")

    return "\n".join(lines)

def update_readme(readme_path, notebooks_section):
    """Replace the Notebooks section in README.md, or append if not present."""
    with open(readme_path) as f:
        content = f.read()

    # Replace existing Notebooks section
    pattern = r"## Notebooks\n.*?(?=\n## |\Z)"
    replacement = notebooks_section
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)

    if count == 0:
        # Section doesn't exist yet, append it
        new_content = content.rstrip() + "\n\n" + notebooks_section

    with open(readme_path, "w") as f:
        f.write(new_content)

    print("README.md updated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--branch", default="main")
    parser.add_argument("--notebooks-dir", default="notebooks")
    parser.add_argument("--readme", default="README.md")
    args = parser.parse_args()

    section = build_notebooks_section(args.user, args.repo, args.branch, args.notebooks_dir)
    update_readme(args.readme, section)