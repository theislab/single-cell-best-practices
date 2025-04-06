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
    dropdowns_str = ""
    dropdowns_str += _get_key_takeaways_str(notebook_path)
    dropdowns_str += _get_env_setup_str(notebook_path)
    dropdowns_str += _get_lamin_setup_str(notebook_path)
    return dropdowns_str


def insert_dropdowns_in_lines(
    lines: list[str], index_title: int, notebook_path: Path
) -> None:
    if "\n" not in lines[index_title]:
        lines[index_title] += "\n"

    index_anchor_dropdown = _get_index_in_cell("<!-- END DROPDOWNS -->\n", lines)
    if index_anchor_dropdown is not None:
        del lines[index_title + 1 : index_anchor_dropdown]
    else:
        lines.insert(index_title + 1, "<!-- END DROPDOWNS -->\n")

    lines.insert(index_title + 1, get_dropdowns_str(notebook_path))


def _get_lamin_setup_str(notebook_path: Path) -> str:
    name_yml_file = os.path.split(notebook_path)[1].split(".")[0]

    # replace notebook yml with section yml if yml_file doesn't exist
    if name_yml_file not in black_list_files_lamin:
        return md_lamin_setup
    else:
        return ""


def _get_env_setup_str(notebook_path: Path) -> str:
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
    nb_path_folder = os.path.split(notebook_path)[0]
    nb_path_file = os.path.split(notebook_path)[1]
    keytakeaways_file = nb_path_file.split(".")[0] + ".keytakeaways"
    keytakeaways_path = Path(nb_path_folder) / keytakeaways_file
    if not keytakeaways_path.is_file():
        return ""
    else:
        keytakeaways_cur = Key_takeaways(keytakeaways_path)
        return keytakeaways_cur.get_key_takeaway_dropdown_str()


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

            index_title = next(
                (
                    index
                    for index, line in enumerate(cell["source"])
                    if line.startswith("#")
                ),
                None,
            )
            if index_title is not None:
                insert_dropdowns_in_lines(cell["source"], index_title, notebook_path)
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

    # n_lines_to_check_for_anchor =
    n_lines_checked = 0
    # Check if in the first n lines there is a markdown cell with the anchors
    # "<!-- START ENV-SETUP -->" and "<!-- END ENV-SETUP -->". If so, we replace
    # the content between the anchors with the newly loaded dropdown string
    # and write the file.
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
    if str_anchor in cell_content:
        return cell_content.index(str_anchor)
    elif str_anchor.strip() in cell_content:
        return cell_content.index(str_anchor.strip())
    else:
        return None


def main():
    # insert env dropdown to all .ipynb's
    notebooks_ipynb = Path("jupyter-book").glob("**/*.ipynb")

    # Only insert dropdowns to .ipynb- and .md-files that are in direct subfolders of "jupyter-book" and not in black_list_directories
    notebooks_ipynb = []
    notebooks_md = []
    for subdir in Path("jupyter-book").iterdir():
        if subdir.is_dir() and all(
            excluded not in str(subdir) for excluded in black_list_directories
        ):
            notebooks_ipynb.extend(subdir.glob("*.ipynb"))
            notebooks_md.extend(subdir.glob("*.md"))

    for notebook in notebooks_ipynb:
        nb = insert_to_ipynb(notebook, 5)

        if nb is not None:
            with open(notebook, "w", encoding="utf-8") as f:
                json.dump(nb, f, indent=2)
        else:
            raise RuntimeError(f"Failed to process notebook: {notebook}")

    for notebook in notebooks_md:
        insert_to_md(notebook, 100)


if __name__ == "__main__":
    main()
else:
    with open("scripts/env_setup.md") as f:
        md_env_setup = f.read()

    with open("scripts/lamin_setup.md") as f:
        md_lamin_setup = f.read()

    # insert env dropdown to all .ipynb's
    notebooks_ipynb = Path("jupyter-book").glob("**/*.ipynb")

    # Only .ipynb files in direct subfolders of "jupyter-book"
    notebooks_ipynb = []
    notebooks_md = []

    for subdir in Path("jupyter-book").iterdir():
        if subdir.is_dir() and all(
            excluded not in str(subdir) for excluded in black_list_directories
        ):
            notebooks_ipynb.extend(subdir.glob("*.ipynb"))
            notebooks_md.extend(subdir.glob("*.md"))

            # Only consider directories (not files)
            # notebooks_ipynb.extend(subdir.glob("*.ipynb"))  # Find all .ipynb files in the subfolder

    # Print aller Pfade (formatiert)
    # print("IPYNB-Files:")
    # for path in notebooks_ipynb:
    #     print(f"  - {path}")

    # print("\nMD-Files:")
    # for path in notebooks_md:
    #     print(f"  - {path}")

    for notebook in notebooks_ipynb:
        nb = insert_to_ipynb(notebook, 5)

        if nb is not None:
            with open(notebook, "w", encoding="utf-8") as f:
                json.dump(nb, f, indent=2)
        else:
            raise RuntimeError(f"Failed to process notebook: {notebook}")

    # insert env dropdown to all .md's
    notebooks_md = Path("jupyter-book/introduction").glob("**/*.md")
    for notebook in notebooks_md:
        md = insert_to_md(notebook, 100)
