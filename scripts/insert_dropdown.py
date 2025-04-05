import json
import logging
import os
from collections.abc import Sequence
from pathlib import Path

from keytakeaways import Key_takeaways


def insert_to_ipynb(notebook_path: Path, n_cells: int) -> dict[str, list | dict | int]:
    try:
        with open(notebook_path, encoding="utf-8") as f:
            nb = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading {notebook_path}: {e}")
        raise

    if nb is None:
        raise ValueError(f"Notebook {notebook_path} is empty or malformed.")

    n_cells_checked = 0
    # Check if in the first n cells there is a markdown cell with the anchors
    # "<!-- START ENV-SETUP/LAMIN-SETUP/KEY-TAKEAWAYS -->" and "<!-- END ENV-SETUP/LAMIN-SETUP/KEY-TAKEAWAYS -->". If so, we replace
    # the content between the anchors with the newly loaded dropdown string.
    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            # I will replace this redundant code block with a function if we stick to the anchor approach
            index_start_env = _get_index_in_cell(
                "<!-- START ENV-SETUP -->\n", cell["source"]
            )
            index_end_env = _get_index_in_cell(
                "<!-- END ENV-SETUP -->\n", cell["source"]
            )

            anchor_found = False
            if index_start_env is not None and index_end_env is not None:
                del cell["source"][index_start_env + 1 : index_end_env]
                cell["source"][index_start_env + 1 : index_start_env] = [
                    _get_env_setup_str(notebook_path, md_env_setup)
                ]
                anchor_found = True

            index_start_lamin = _get_index_in_cell(
                "<!-- START LAMIN-SETUP -->\n", cell["source"]
            )
            index_end_lamin = _get_index_in_cell(
                "<!-- END LAMIN-SETUP -->\n", cell["source"]
            )

            if index_start_lamin is not None and index_end_lamin is not None:
                del cell["source"][index_start_lamin + 1 : index_end_lamin]
                cell["source"][index_start_lamin + 1 : index_start_lamin] = [
                    md_lamin_setup
                ]
                anchor_found = True

            index_start_key_takeaways = _get_index_in_cell(
                "<!-- START KEY-TAKEAWAYS -->\n", cell["source"]
            )
            index_end_key_takeaways = _get_index_in_cell(
                "<!-- END KEY-TAKEAWAYS -->\n", cell["source"]
            )

            if (
                index_start_key_takeaways is not None
                and index_end_key_takeaways is not None
            ):
                del cell["source"][
                    index_start_key_takeaways + 1 : index_end_key_takeaways
                ]
                cell["source"][
                    index_start_key_takeaways + 1 : index_start_key_takeaways
                ] = [_get_key_takeaways_str(notebook_path)]
                anchor_found = True

            if anchor_found:
                return nb

        n_cells_checked += 1

        if n_cells_checked >= n_cells:
            return nb

    return nb


def insert_to_md(md_path: Path, n_lines: int) -> None:
    try:
        with open(md_path, encoding="utf-8") as f:
            content = f.readlines()
    except FileNotFoundError:
        logging.error(f"File not found: {md_path}", exc_info=True)
        raise

    if not content:
        raise RuntimeError(f"Markdown file {md_path} is empty.")

    n_lines_checked = 0
    # Check if in the first n lines there is a markdown cell with the anchors
    # "<!-- START ENV-SETUP -->" and "<!-- END ENV-SETUP -->". If so, we replace
    # the content between the anchors with the newly loaded dropdown string
    # and write the file.
    for line_number, line in enumerate(content):
        if "<!-- START ENV-SETUP -->" in line:
            index_start = line_number
            index_end = None
            # Search for the end anchor within the next `n` lines
            for line_number_after_start_anchor in range(
                line_number, min(line_number + n_lines, len(content))
            ):
                if "<!-- END ENV-SETUP -->" in content[line_number_after_start_anchor]:
                    index_end = line_number_after_start_anchor
                    break

            if index_start is not None and index_end is not None:
                # Replace the content between the anchors
                env_setup_str = _get_env_setup_str(md_path, md_env_setup)
                new_content = (
                    content[: index_start + 1]
                    + [env_setup_str + "\n"]
                    + content[index_end:]
                )
                with open(md_path, "w", encoding="utf-8") as f:
                    f.writelines(new_content)
                return

        n_lines_checked += 1
        if n_lines_checked >= n_lines:
            break


def _get_index_in_cell(str_anchor: str, cell_content: Sequence[str]) -> int | None:
    if str_anchor in cell_content:
        return cell_content.index(str_anchor)
    elif str_anchor.strip() in cell_content:
        return cell_content.index(str_anchor.strip())
    else:
        return None


def _get_env_setup_str(notebook_path: Path, md_env_setup: str) -> str:
    nb_path_folder = os.path.split(notebook_path)[0]
    nb_path_file = os.path.split(notebook_path)[1]
    yml_file = nb_path_file.split(".")[0] + ".yml"

    # replace notebook yml with section yml if yml_file doesn't exist
    if not (Path(nb_path_folder) / yml_file).is_file():
        yml_file = nb_path_folder.split("/")[-1] + ".yml"

    return md_env_setup.replace("?yml_file_path?", yml_file)


def _get_key_takeaways_str(notebook_path: Path) -> str:
    nb_path_folder = os.path.split(notebook_path)[0]
    nb_path_file = os.path.split(notebook_path)[1]
    keytakeaways_file = nb_path_file.split(".")[0] + ".keytakeaways"
    keytakeaways_path = Path(nb_path_folder) / keytakeaways_file
    if not keytakeaways_path.is_file():
        return "<!-- " + keytakeaways_file + " DOES NOT EXIST -->"
    else:
        keytakeaways_cur = Key_takeaways(keytakeaways_path)
        return keytakeaways_cur.get_key_takeaway_dropdown_str()


with open("scripts/env_setup.md") as f:
    md_env_setup = f.read()

with open("scripts/lamin_setup.md") as f:
    md_lamin_setup = f.read()

# insert env dropdown to all .ipynb's
notebooks_ipynb = Path("jupyter-book").glob("**/*.ipynb")
for notebook in notebooks_ipynb:
    if "_build" not in str(notebook):
        nb = insert_to_ipynb(notebook, 5)

        if nb is not None:
            with open(notebook, "w", encoding="utf-8") as f:
                json.dump(nb, f, indent=2)
        else:
            raise RuntimeError(f"Failed to process notebook: {notebook}")

# insert env dropdown to all .md's
notebooks_md = Path("jupyter-book/introduction").glob("**/*.md")
for notebook in notebooks_md:
    insert_to_md(notebook, 100)
