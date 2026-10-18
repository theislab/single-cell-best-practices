import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import anndata as ad
import seaborn as sns

from typing import Dict, List, Union, Tuple, Any, Optional

def plot_scatter_density(
    data: Union[pd.DataFrame, ad.AnnData],
    scattercat: Optional[str],
    densitycat: Optional[str],
    palette: Optional[Any],
    title: Optional[str],
    *,
    plot_legend: bool = True,
    category: Optional[str] = None,
    cbar_title: Optional[str] = None,
    pointsize: float = 10.0,
    figsize: Tuple[int,int] = (10, 5),
    title_text_size: Optional[float] = None,
) -> None:
    """
    Plot spatial points as a scatter plot with an optional density (KDE) overlay.
    Supports either a plain DataFrame with 'x'/'y' columns or an AnnData object
    with spatial coordinates in `obsm['spatial']` and per-cell metadata in `obs`.

    Parameters
    ----------
    data
        Either:
          - A pandas DataFrame containing at least columns 'x' and 'y', and
            optionally columns named by `scattercat`, `densitycat`, and `category`.
          - An AnnData object with:
                * `obsm['spatial']` shaped (n_obs, 2) for x/y coordinates, and
                * `obs` containing any requested metadata columns.
    scattercat
        Column name to use for color/hue in the scatter plot (e.g., a cell type).
        Pass None for an uncolored scatter.
    densitycat
        Column name whose values are used as weights for the KDE (density) layer.
        Pass None for an unweighted KDE (or no KDE if data are insufficient).
    palette
        Seaborn/Matplotlib palette specification (string or iterable). Ignored if
        `scattercat` is None.
    plot_legend
        If the legend should be plotted.
    title
        Optional title for the (non-faceted) plot. Ignored when `category` is set.
    category
        Optional column name to facet by. When provided, creates one subplot per
        category level, each showing scatter + KDE for that subset.
    cbar_title
        Optional cbar_title for the (non-faceted) plot.
    pointsize
        Marker size for the scatter points.
    title_text_size
        Optional title_text_size to define the size of the title text.

    Notes
    -----
    - For AnnData input, 'x'/'y' are taken from `obsm['spatial'][:, 0/1]`.
    - The function calls `plt.show()` and returns None.
    """

    
    df = data
    weights = None  
    
    if ( isinstance(df, ad.AnnData) ): 

        df = pd.DataFrame({
            'x': data.obsm['spatial'][:,0],
            'y': data.obsm['spatial'][:,1]
        })

        # Add scatter category
        if ( scattercat != None ):
            df[scattercat] = list(data.obs[scattercat])
        if densitycat is not None:
            df[densitycat] = list(data.obs[densitycat])
            weights = df[densitycat]
        if category is not None:
            df[category] = list(data.obs[category])

    if ( category != None ):
        categories = df[category].unique()
        n_categories = len(categories)

        ncol = 5
        if n_categories < ncol:
            ncol = n_categories
        nrow = np.ceil(n_categories/ncol).astype(int)

        plt.figure(figsize=figsize)
        for i, cat in enumerate(categories):
            plt.subplot(nrow, ncol, i + 1)
            subset = df[df[category] == cat]

            sns.scatterplot(data=subset, x='x', y='y', s=pointsize, palette=palette, legend=False)
            if densitycat is not None:
                sns.kdeplot(
                    data=subset, x='x', y='y', cmap="viridis", fill=True, alpha=0.5, bw_adjust=0.5,
                    cbar=True, cbar_kws={'label': f'{cbar_title} {cat}'}
                )
            plt.title(cat, **({'fontsize': title_text_size} if title_text_size is not None else {}))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.xlim(np.min(df['x']), np.max(df['x']))
            plt.ylim(np.min(df['y']), np.max(df['y']))
            plt.gca().invert_yaxis()

        plt.show()

    else:

        plt.figure(figsize=figsize)
        scatter = sns.scatterplot(data=df, x='x', y='y', s=pointsize, hue=scattercat, palette=palette)
        handles, labels = scatter.get_legend_handles_labels()
        if plot_legend and handles:
            plt.legend(handles=handles, labels=labels, bbox_to_anchor=(1.35, 1),
                    loc='upper left', borderaxespad=0., markerscale=1)
        elif scatter.get_legend() is not None:
            scatter.get_legend().remove()

        try:
            kde = sns.kdeplot(
                data=df,
                x='x', y='y',
                fill=True,
                alpha=0.5,
                cmap="viridis",
                bw_adjust=0.5,
                weights=weights,
                cbar=True,
                cbar_kws={'label': f'{cbar_title}'}
            )
        except Exception as e:
            print(f"[WARNING] Failed to plot density with KDE " +
                f"probably because not enough data points for your chosen density category: {e}")
            print("Just plotting scatter plot.")

        if ( title ):
            plt.title(title, **({'fontsize': title_text_size} if title_text_size is not None else {}))

        plt.xlabel('x')
        plt.ylabel('y')
        plt.xlim(np.min(df['x']), np.max(df['x']))
        plt.ylim(np.min(df['y']), np.max(df['y']))
        plt.show()


def plot_marker_density_and_scatter(
    sdata: Dict[str, Any],
    markers: Dict[str, List[str]],
    figsize: Tuple[int, int] = (15, 5)
) -> None:
    """
    Plot scatter and density (KDE) maps for marker gene expression.

    Parameters
    ----------
    sdata : dict
        Spatial data container with:
        - `sdata['table']` as an AnnData-like object containing:
            * `obsm['spatial']` : ndarray of shape (n_obs, 2) with x/y coordinates.
            * `var.index` : index containing marker (gene) names.
            * `X` : expression matrix (sparse or dense) of shape (n_obs, n_vars).
    markers : dict
        Dictionary mapping cell type names (str) to lists of marker names (str)
        to be plotted for each cell type.

    Returns
    -------
    None
        Displays scatter + KDE plots for each marker in each cell type.
    """

    df = pd.DataFrame({
            'x': sdata['table'].obsm['spatial'][:,0],
            'y': sdata['table'].obsm['spatial'][:,1]
        })

    # Get expression values for each marker
    for celltype_markers in markers.values():
        for marker in celltype_markers:
            idx = list(sdata['table'].var.index).index(marker)
            df[marker] = sdata['table'].X.todense()[:,idx].flatten().tolist()[0]

    for celltype in markers:
        celltype_markers = markers[celltype]
        n_celltype_markers = len(celltype_markers)
        plt.figure(figsize=figsize)

        ncol = 5
        if n_celltype_markers < ncol:
            ncol = n_celltype_markers
        nrow = np.ceil(n_celltype_markers/ncol).astype(int)

        for i, marker in enumerate(celltype_markers):
            plt.subplot(nrow, len(celltype_markers), i + 1)
            plt.title(f'{celltype}_{marker}')
            sns.scatterplot(data=df, x='x', y='y', s=20, hue=marker, legend=False)
            sns.kdeplot(
                data=df, x='x', y='y', cmap="viridis", weights=marker,
                shade=True, alpha=0.5, bw_adjust=0.5, cbar=True
            )
            plt.xlabel('x')
            plt.ylabel('y')
            plt.xlim(np.min(df['x']), np.max(df['x']))
            plt.ylim(np.min(df['y']), np.max(df['y']))
        plt.show()

def plot_marker_boxplot(
    sdata: Dict[str, Any],
    markers: Dict[str, List[str]],
    ANNOTATION_KEY: str,
    name: str
) -> None:
    """
    Plot boxplots of log2 fold change in marker expression between each cell type
    and all other cells.

    Parameters
    ----------
    sdata : dict
        Spatial data container with:
        - `sdata['table']` as an AnnData-like object containing:
            * `var.index` : index of feature/marker names.
            * `obs` : DataFrame with cell annotations (includes `ANNOTATION_KEY`).
            * `X` : expression matrix (sparse or dense) of shape (n_obs, n_vars).
    markers : dict
        Dictionary mapping cell type names to lists of marker names to analyze.
    ANNOTATION_KEY : str
        Column in `sdata['table'].obs` used to identify the cell type of each cell.
    name : str
        Descriptive name of the marker set, used in the y-axis label.

    Returns
    -------
    None
        Displays the boxplot using matplotlib.
    """
    log2fc_list = []
    celltype_list = []

    rna = sdata['table']
    rna.X = sdata['table'].X

    for celltype in markers.keys():
        idx_var = [True if v in markers[celltype] else False for v in rna.var.index]
        num_features = len(markers[celltype])
        celltype_list = celltype_list + [celltype] * num_features

        # Just take cells of celltype
        idx_obs = rna.obs[ANNOTATION_KEY] == celltype
        subset_rna = rna[idx_obs,idx_var]

        mtx = subset_rna.X.todense()
        celltype_mean_list = [np.mean(mtx[:,i]) for i in range(0,num_features)]
            
        # For background take all cells that are not celltype                
        idx_obs = rna.obs[ANNOTATION_KEY] != celltype
        subset_rna = rna[idx_obs,idx_var]

        mtx = subset_rna.X.todense()
        background_mean_list = [np.mean(mtx[:,i]) for i in range(0,num_features)]

        for i in range(0, num_features):
            log2fc_list.append(np.log2(celltype_mean_list[i] / background_mean_list[i]))
        
    df = pd.DataFrame({'celltype': celltype_list,
                    'log2fc': log2fc_list})

    plt.figure(figsize=(8, 8))

    sns.boxplot(data=df, x='celltype', y='log2fc')

    plt.xticks(rotation=45, fontsize=18)
    plt.yticks(fontsize=18)
    plt.xlabel('Celltype', fontsize=18)
    plt.ylabel(f"Log2 foldchange {name.replace('_',' ')} expression", fontsize=18)
    plt.title("Celltype vs Non-Celltype", fontsize=20)

    plt.tight_layout()
    plt.show()