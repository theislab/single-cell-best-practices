import json
import logging
import os
from collections.abc import Sequence
from pathlib import Path

from keytakeaways import Key_takeaways

black_list_directories = ["_build", "_static", "src"]
black_list_files_yml = ["prior_art", "scrna_seq", "introduction", "muon_to_seurat"]
black_list_files_lamin = [
    # IPYNB files
    "introduction",
    "gene_regulatory_networks_atac",
    "quality_control",
    "muon_to_seurat",
    "feature_selection",
    "normalization",
    "dimensionality_reduction",
    "cell_cell_communication",
    "gene_regulatory_networks",
    "clonotype",
    "multimodal_integration",
    "ir_profiling",
    "specificity",
    "analysis_tools",
    "annotation",
    "integration",
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
    "rna_velocity",
    # MD files
    "data_infrastructure",
    "scrna_seq",
    "prior_art",
    "raw_data_processing",
]


with open("scripts/env_setup.md") as f:
    md_env_setup = f.read()

with open("scripts/lamin_setup.md") as f:
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
    r"""Inserts the dropdowns after the title and adds "<!-- END DROPDOWNS -->\n" so that we can call the python script multiple times without adding multiple dropdown.

    :param lines: The list of lines in a document (from our md's and ipynb's)
    :param index_title: The index of the element in the list that contains the title
    :param notebook_path: the path to our current notebook
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
    """Returns the template of the lamin dropdown string if the name of the file is not contained in the blacklist. Otherwise, an empty string is returned."""
    if os.path.split(notebook_path)[1].split(".")[0] not in black_list_files_lamin:
        return md_lamin_setup
    else:
        return ""


def _get_env_setup_str(notebook_path: Path) -> str:
    """Returns the template of the env dropdown string if the name of the file is not contained in the blacklist. Otherwise, an empty string is returned. If there is no specific yml for the notebook, the yml section file is used."""
    if os.path.split(notebook_path)[1].split(".")[0] not in black_list_files_yml:
        nb_path_folder = os.path.split(notebook_path)[0]
        nb_path_file = os.path.split(notebook_path)[1]
        yml_file = nb_path_file.split(".")[0] + ".yml"

        # replace notebook yml with section yml if yml_file doesn't exist
        if not (Path(nb_path_folder) / yml_file).is_file():
            yml_file = nb_path_folder.split("/")[-1] + ".yml"

        return md_env_setup.replace("?yml_file_path?", yml_file)
    else:
        return ""


def _get_key_takeaways_str(notebook_path: Path) -> str:
    """Returns the key takeaways dropdown string if a <notebook-name>.keytakeaways file exists. Otherwise, an empty string is returned."""
    nb_path_folder = os.path.split(notebook_path)[0]
    nb_path_file = os.path.split(notebook_path)[1]
    keytakeaways_file = nb_path_file.split(".")[0] + ".keytakeaways"
    keytakeaways_path = Path(nb_path_folder) / keytakeaways_file

    if not keytakeaways_path.is_file():
        return ""
    else:
        keytakeaways_cur = Key_takeaways(keytakeaways_path)
        return keytakeaways_cur.get_key_takeaway_dropdown_str()


def insert_to_ipynb(notebook_path: Path, n_cells: int) -> None:
    """The function tries to find the title in the first n_cells. If there is a title, it then inserts the dropdown templates after the title and writes the new .ipynb file. Otherwise, the function skips this notebook and does nothing.

    :param notebook_path: the path to the current notebook
    :param n_cells: the number of the first n cells the function should check to find the title before it breaks
    """
    try:
        with open(notebook_path, encoding="utf-8") as f:
            nb = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading {notebook_path}: {e}")
        raise

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
    """The function tries to find the title in the first n_lines. If there is a title, it then inserts the dropdown templates after the title and writes the new .md file. Otherwise, the function skips this notebook and does nothing.

    :param notebook_path: the path to the current notebook
    :param n_lines: the number of the first n lines the function should check to find the title before it breakes
    """
    try:
        with open(md_path, encoding="utf-8") as f:
            content = f.readlines()
    except FileNotFoundError:
        logging.error(f"File not found: {md_path}", exc_info=True)
        raise

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
        insert_to_ipynb(notebook, 5)

    for notebook in notebooks_md:
        insert_to_md(notebook, 100)


if __name__ == "__main__":
    main()
