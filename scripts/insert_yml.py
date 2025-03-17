import json
import os
from pathlib import Path


def insert_to_ipynb(notebook_path, n):
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
    nb_path_folder = os.path.split(notebook_path)[0]
    nb_path_file = os.path.split(notebook_path)[1]
    yml_file = nb_path_file.split(".")[0] + ".yml"

    if not (Path(nb_path_folder) / yml_file).is_file():
        # print((Path(nb_path_folder) / yml_file))
        yml_file = nb_path_folder.split("/")[-1] + ".yml"
        # print(yml_file)

    return md_env_setup.replace("?yml_file_path?", yml_file)


# Load reusable content
with open("scripts/env_setup.md") as f:
    md_env_setup = f.read()

# Process notebooks
notebooks_ipynb = Path("jupyter-book").glob("**/*.ipynb")

for notebook in notebooks_ipynb:
    # Insert yml box after the anchor, only look for the anchor in the first 5 cells
    if "_build" not in str(notebook):
        # print(str(notebook))
        nb = insert_to_ipynb(notebook, 5)
        if nb is not None:
            with open(notebook, "w", encoding="utf-8") as f:
                json.dump(nb, f, indent=2)
        else:
            print(f"Skipping {notebook} due to errors.")


def insert_to_md(md_path, n):
    try:
        with open(md_path, encoding="utf-8") as f:
            content = f.readlines()
    except Exception as e:
        print(f"Error loading {md_path}: {e}")
        return None

    if not content:
        print(f"Markdown file {md_path} is empty.")
        return None

    n_lines_checked = 0
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
                print(f"{md_path} !!!YML Box inserted!!!")
                return

        n_lines_checked += 1
        if n_lines_checked >= n:
            break

    # print(md_path)


notebooks_md = Path("jupyter-book/introduction").glob("**/*.md")
for notebook in notebooks_md:
    print(str(notebook))
    insert_to_md(notebook, 5)
