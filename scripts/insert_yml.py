import json
import os
from pathlib import Path


def insert(notebook_path, n):
    try:
        with open(notebook_path, encoding="utf-8") as f:
            nb = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading {notebook_path}: {e}")
        return None

    if nb is None:
        print(f"Notebook {notebook_path} is empty or malformed.")
        return None

    n_cells_checked = 0
    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            index_start = get_index_in_cell(
                "<!-- START ENV-SETUP -->\n", cell["source"]
            )
            index_end = get_index_in_cell("<!-- END ENV-SETUP -->\n", cell["source"])

            if index_start is not None and index_end is not None:
                del cell["source"][index_start + 1 : index_end]
                cell["source"][index_start + 1 : index_start] = [
                    get_env_setup_str(notebook_path, md_env_setup)
                ]
                print(str(notebook_path) + " !!!YML Box inserted!!!")
                return nb

        n_cells_checked += 1

        if n_cells_checked >= n:
            # Return the notebook even if no modification was made
            print(notebook_path)
            return nb

    print(notebook_path)
    return nb  # Ensure the function always returns a notebook dictionary


def get_index_in_cell(str_anchor, cell_content):
    if str_anchor in cell_content:
        return cell_content.index(str_anchor)
    elif str_anchor.strip() in cell_content:
        return cell_content.index(str_anchor.strip())
    else:
        return None


def get_env_setup_str(notebook_path, md_env_setup):
    os.path.split(notebook_path)[0]
    nb_path_file = os.path.split(notebook_path)[1]
    yml_file = nb_path_file.split(".")[0] + ".yml"
    return md_env_setup.replace("?yml_file_path?", yml_file)


# Load reusable content
with open("scripts/env_setup.md") as f:
    md_env_setup = f.read()

# Process notebooks
notebooks = Path("jupyter-book").glob("**/*.ipynb")

for notebook in notebooks:
    # Insert yml box after the anchor, only look for the anchor in the first 5 cells
    if "_build" not in str(notebook):
        # print(str(notebook))
        nb = insert(notebook, 5)
        if nb is not None:
            with open(notebook, "w", encoding="utf-8") as f:
                json.dump(nb, f, indent=2)
        else:
            print(f"Skipping {notebook} due to errors.")
