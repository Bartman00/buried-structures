# Update the readme for notebooks because Github
# can't reliably show jupyter notebooks.

# TODO: Review this AI slop code before using.


import json
import os
import re
from pathlib import Path


def get_first_markdown_cell(nb_path):
    # Takes json and returns the first markdown cell
    with open(nb_path) as f:
        nb = json.load(f)
    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            return cell["source"]
    return None


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


def get_notebook_description(nb_path):

    md = get_first_markdown_cell(nb_path)
    if md is None:
        return ""

    found_start = False
    ret_lines = []
    for line in md:
        line = line.strip()

        # print(f"{line=}")

        if line.startswith("### Description"):
            # print("found start")
            found_start = True
            continue

        if "#" in line and found_start:
            return " ".join(ret_lines)
            
        if found_start:
            if len(line) > 1:
                ret_lines.append(line)


    return ""


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

    lines = ["## Notebooks"]

    lines.append("""
Github has problems rendering larger notebooks so links to nbviewer are included here.
                 """)

    for folder, notebooks in sorted(folders.items()):
        # Subfolder header (skip if root notebooks/ folder)
        if folder != Path(notebooks_dir):
            rel_folder = folder.relative_to(notebooks_dir)
            lines.append(f"\n### {str(rel_folder).replace(os.sep, ' / ').title()}\n")

        folder_lines = []
        folder_lines.append("| Notebook | Description |")
        folder_lines.append("|----------|-------------|")
        notebooks_in_folder = 0
        for nb_path in notebooks:
            if "XX" in str(nb_path):
                # Ignore things like templates
                continue

            notebooks_in_folder += 1

            title = get_notebook_title(nb_path)
            url = f"{base_url}/{nb_path.as_posix()}"
            description = get_notebook_description(nb_path)
            folder_lines.append(f"| [{title}]({url}) |{description} |")

        folder_lines.append("")

        if notebooks_in_folder > 0:
            lines.extend(folder_lines)

    return "\n".join(lines)


def update_readme(readme_path, notebooks_section):
    """Replace the Notebooks section in README.md, or append if not present."""
    with open(readme_path) as f:
        content = f.read()

    # Replace existing Notebooks section
    # Goes until another ## HEADER 2
    pattern = r"## Notebooks\n.*?(?=\n## |\Z)"
    replacement = notebooks_section
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)

    if count == 0:
        # Section doesn't exist yet, append it
        new_content = content.rstrip() + "\n\n" + notebooks_section

    with open(readme_path, "w") as f:
        f.write(new_content)

    print("README.md updated.")


def get_env(file_path=r"./scripts/.env"):
    # Return environment variables.

    with open(file_path, "r") as file:
        lines = file.readlines()

    ret = {}
    for line in lines:
        line = line.replace("\n", "")
        splits = line.split("=")

        ret[splits[0]] = splits[1]

    return ret


if __name__ == "__main__":
    environment = get_env()
    notebooks_dir = "notebooks"
    section = build_notebooks_section(
        environment["GITHUB_USER"],
        environment["GITHUB_REPO"],
        environment["TARGET_BRANCH"],
        notebooks_dir,
    )

    # print(section)
    update_readme("README.md", section)

