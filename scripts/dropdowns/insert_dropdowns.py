import json
from collections.abc import Sequence
from pathlib import Path

from keytakeaways import Key_takeaways

black_list_directories = ["_build", "_static", "src"]
black_list_files_yml = ["prior_art", "scrna_seq", "introduction", "muon_to_seurat"]
black_list_files_lamin = [
    # IPYNB files
    "introduction",
    "gene_regulatory_networks_atac",
    "muon_to_seurat",
    "cell_cell_communication",
    "gene_regulatory_networks",
    "clonotype",
    "multimodal_integration",
    "ir_profiling",
    "specificity",
    "analysis_tools",
    "annotation",
    "clustering",
    "bulk_deconvolution",
    "paired_integration",
    "advanced_integration",
    "perturbation_modeling",
    "differential_gene_expression",
    "gsea_pathway",
    "compositional",
    "batch_correction",
    "doublet_detection",
    "imputation",
    "deconvolution",
    "neighborhood",
    "spatially_variable_genes",
    "domains",
    "lineage_tracing",
    # MD files
    "data_infrastructure",
    "scrna_seq",
    "prior_art",
    "raw_data_processing",
]


with open("scripts/dropdowns/env_setup.md") as f:
    md_env_setup = f.read()

with open("scripts/dropdowns/lamin_setup.md") as f:
    md_lamin_setup = f.read()


def get_dropdowns_str(notebook_path: Path) -> list[str]:
    """Puts together all the different dropdown strings into one big string."""
    dropdowns_str = ""
    dropdowns_str += _get_key_takeaways_str(notebook_path)
    dropdowns_str += _get_env_setup_str(notebook_path)
    dropdowns_str += _get_lamin_setup_str(notebook_path)
    return dropdowns_str


def insert_dropdowns_in_lines(
    lines: list[str], index_title: int, notebook_path: Path
) -> None:
    r"""Inserts the dropdowns after the title.

    Adds "<!-- END DROPDOWNS -->\n" so that we can call the python script multiple times without adding multiple dropdown.

    Args:
        lines: Lines of ``.md`` or ``.ipynb`` files
        index_title: The index of the element in the list that contains the title
        notebook_path: The path to our current notebook
    """
    if "\n" not in lines[index_title]:
        lines[index_title] += "\n"

    index_anchor_dropdown = _get_index_in_cell("<!-- END DROPDOWNS -->\n", lines)
    if index_anchor_dropdown is not None:
        del lines[index_title + 1 : index_anchor_dropdown]
    else:
        lines.insert(index_title + 1, "<!-- END DROPDOWNS -->\n")

    lines.insert(index_title + 1, get_dropdowns_str(notebook_path))


def _get_lamin_setup_str(notebook_path: Path) -> str:
    """Returns the lamin dropdown template if the filename isn’t blacklisted, otherwise returns an empty string."""
    if notebook_path.stem not in black_list_files_lamin:
        return md_lamin_setup
    else:
        return ""


def _get_env_setup_str(notebook_path: Path) -> str:
    """Returns the template of the env dropdown string if the name of the file is not contained in the blacklist.

    Otherwise, an empty string is returned. If there is no specific yml for the notebook, the yml section file is used.
    """
    if notebook_path.stem not in black_list_files_yml:
        nb_path_folder = notebook_path.parent
        yml_file = f"{notebook_path.stem}.yml"

        # replace notebook yml with section yml if yml_file doesn't exist
        if not (Path(nb_path_folder) / yml_file).is_file():
            yml_file = str(nb_path_folder).split("/")[-1] + ".yml"

        return md_env_setup.replace("?yml_file_path?", yml_file)
    else:
        return ""


def _get_key_takeaways_str(notebook_path: Path) -> str:
    """Returns the key takeaways dropdown string if a <notebook-name>_keytakeaways.txt file exists, otherwise an empty string."""
    keytakeaways_path = notebook_path.parent / f"{notebook_path.stem}_keytakeaways.txt"

    if not keytakeaways_path.is_file():
        return ""
    else:
        keytakeaways_cur = Key_takeaways(keytakeaways_path)
        return keytakeaways_cur.get_key_takeaway_dropdown_str()


def insert_to_ipynb(notebook_path: Path, n_cells: int) -> None:
    """Inserts the dropdowns to ipynb-files.

    The function tries to find the title in the first n_cells. If there is a title, it then inserts the dropdown templates after the title and writes the new .ipynb file. Otherwise, the function skips this notebook and does nothing.

    Args:
        notebook_path: The path to the current notebook
        n_cells: The number of the first ``n`` cells the function should check to find the title before it breaks
    """
    try:
        with open(notebook_path, encoding="utf-8") as f:
            nb = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Error loading {notebook_path}: {e.msg}", e.doc, e.pos
        ) from e

    if nb is None:
        raise ValueError(f"Notebook {notebook_path} is empty or malformed.")

    n_cells_checked = 0
    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            index_title = next(
                (
                    index
                    for index, line in enumerate(cell["source"])
                    if line.startswith("# ")
                ),
                None,
            )
            if index_title is not None:
                insert_dropdowns_in_lines(cell["source"], index_title, notebook_path)

                if nb is not None:
                    with open(notebook_path, "w", encoding="utf-8") as f:
                        json.dump(nb, f, indent=2)
                else:
                    raise RuntimeError(f"Failed to process notebook: {notebook}")

                return

        n_cells_checked += 1

        if n_cells_checked >= n_cells:
            return


def insert_to_md(md_path: Path, n_lines: int) -> None:
    """Inserts the dropdowns to md-files.

    The function tries to find the title in the first n_lines. If there is a title, it then inserts the dropdown templates after the title and writes the new .md file. Otherwise, the function skips this notebook and does nothing.

    Args:
        notebook_path: The path to the current notebook
        n_lines: The number of the first ``n`` lines the function should check to find the title before it stops
    """
    try:
        with open(md_path, encoding="utf-8") as f:
            content = f.readlines()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {md_path}") from e

    if not content:
        raise RuntimeError(f"Markdown file {md_path} is empty.")

    n_lines_checked = 0
    for line_number, line in enumerate(content):
        if line.startswith("# "):
            index_title = line_number
            insert_dropdowns_in_lines(content, index_title, md_path)

            with open(md_path, "w", encoding="utf-8") as f:
                f.writelines(content)

            return

        n_lines_checked += 1
        if n_lines_checked >= n_lines:
            return


def _get_index_in_cell(str_anchor: str, cell_content: Sequence[str]) -> int | None:
    """Returns the index of a specific anchor in a list of strings."""
    if str_anchor in cell_content:
        return cell_content.index(str_anchor)
    elif str_anchor.strip() in cell_content:
        return cell_content.index(str_anchor.strip())
    else:
        return None


def main():
    """Only inserts dropdowns to .ipynb- and .md-files that are in direct subfolders of "jupyter-book" and not in black_list_directories."""
    # creates the list of relevant notebooks
    notebooks_ipynb = []
    notebooks_md = []
    for subdir in Path("jupyter-book").iterdir():
        if subdir.is_dir() and all(
            excluded not in str(subdir) for excluded in black_list_directories
        ):
            notebooks_ipynb.extend(subdir.glob("*.ipynb"))
            notebooks_md.extend(subdir.glob("*.md"))

    # insert dropdowns to notebooks
    for notebook in notebooks_ipynb:
        insert_to_ipynb(notebook, n_cells=5)

    for notebook in notebooks_md:
        insert_to_md(notebook, n_lines=100)


if __name__ == "__main__":
    main()
