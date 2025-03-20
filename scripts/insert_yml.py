import json
import os
from pathlib import Path


def insert_to_ipynb(notebook_path: Path, n: int) -> dict:
    try:
        with open(notebook_path, encoding="utf-8") as f:
            nb = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading {notebook_path}: {e}")
        return None

    if nb is None:
        raise ValueError(f"Notebook {notebook_path} is empty or malformed.")
        return None

    n_cells_checked = 0
    # Check if in the first n cells there is a markdown cell with the anchors
    # "<!-- START ENV-SETUP -->" and "<!-- END ENV-SETUP -->". If so, we replace
    # the content between the anchors with the newly loaded dropdown string.
    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            index_start = _get_index_in_cell(
                "<!-- START ENV-SETUP -->\n", cell["source"]
            )
            index_end = _get_index_in_cell("<!-- END ENV-SETUP -->\n", cell["source"])

            if index_start is not None and index_end is not None:
                del cell["source"][index_start + 1 : index_end]
                cell["source"][index_start + 1 : index_start] = [
                    get_env_setup_str(notebook_path, md_env_setup)
                ]
                return nb

        n_cells_checked += 1

        if n_cells_checked >= n:
            return nb

    return nb


def insert_to_md(md_path: Path, n: int) -> None:
    try:
        with open(md_path, encoding="utf-8") as f:
            content = f.readlines()
    except FileNotFoundError:
        print(f"File not found: {md_path}")
        raise

    if not content:
        print(f"Markdown file {md_path} is empty.")
        return None

    n_lines_checked = 0
    # Check if in the first n lines there is a markdown cell with the anchors
    # "<!-- START ENV-SETUP -->" and "<!-- END ENV-SETUP -->". If so, we replace
    # the content between the anchors with the newly loaded dropdown string
    # and write the file.
    for i, line in enumerate(content):
        if "<!-- START ENV-SETUP -->" in line:
            index_start = i
            index_end = None
            # Search for the end anchor within the next `n` lines
            for j in range(i, min(i + n, len(content))):
                if "<!-- END ENV-SETUP -->" in content[j]:
                    index_end = j
                    break

            if index_start is not None and index_end is not None:
                # Replace the content between the anchors
                env_setup_str = get_env_setup_str(md_path, md_env_setup)
                new_content = (
                    content[: index_start + 1]
                    + [env_setup_str + "\n"]
                    + content[index_end:]
                )
                with open(md_path, "w", encoding="utf-8") as f:
                    f.writelines(new_content)
                return

        n_lines_checked += 1
        if n_lines_checked >= n:
            break


def _get_index_in_cell(str_anchor: str, cell_content: list) -> int | None:
    if str_anchor in cell_content:
        return cell_content.index(str_anchor)
    elif str_anchor.strip() in cell_content:
        return cell_content.index(str_anchor.strip())
    else:
        return None


def get_env_setup_str(notebook_path: Path, md_env_setup: str) -> str:
    nb_path_folder = os.path.split(notebook_path)[0]
    nb_path_file = os.path.split(notebook_path)[1]
    yml_file = nb_path_file.split(".")[0] + ".yml"

    # replace notebook yml with section yml if yml_file doesn't exist
    if not (Path(nb_path_folder) / yml_file).is_file():
        yml_file = nb_path_folder.split("/")[-1] + ".yml"

    return md_env_setup.replace("?yml_file_path?", yml_file)


with open("scripts/env_setup.md") as f:
    md_env_setup = f.read()

# insert env dropdown to all .ipynb's
notebooks_ipynb = Path("jupyter-book").glob("**/*.ipynb")
for notebook in notebooks_ipynb:
    if "_build" not in str(notebook):
        nb = insert_to_ipynb(notebook, 5)

        if nb is not None:
            with open(notebook, "w", encoding="utf-8") as f:
                json.dump(nb, f, indent=2)
        else:
            print(f"Skipping {notebook} due to errors.")

# insert env dropdown to all .md's
notebooks_md = Path("jupyter-book/introduction").glob("**/*.md")
for notebook in notebooks_md:
    insert_to_md(notebook, 100)
