get_ipython().run_line_magic("load_ext", " autoreload")
get_ipython().run_line_magic("autoreload", " 2")


import importlib
import warnings

import pandas as pd

warnings.filterwarnings("ignore")

import scanpy as sc
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import altair as alt


adata = sc.read("haber_count.h5ad")


adata


adata.obs


healthy_tissue = [2000, 2000, 2000]
diseased_tissue = [4000, 2000, 2000]
example_data_global = pd.DataFrame(
    data=np.array([healthy_tissue, diseased_tissue]),
    index=[1, 2],
    columns=["A", "B", "C"],
)
example_data_global["Disease status"] = ["Healthy", "Diseased"]
example_data_global


plot_data_global = example_data_global.melt(
    "Disease status", ["A", "B", "C"], "Cell type", "count"
)

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
sns.barplot(
    data=plot_data_global, x="Disease status", y="count", hue="Cell type", ax=ax[0]
)
ax[0].set_title("Global abundances, by status")

sns.barplot(
    data=plot_data_global, x="Cell type", y="count", hue="Disease status", ax=ax[1]
)
ax[1].set_title("Global abundances, by cell type")

plt.show()


np.random.seed(1234)
healthy_sample = np.random.multinomial(
    pvals=healthy_tissue / np.sum(healthy_tissue), n=600
)
diseased_sample = np.random.multinomial(
    pvals=diseased_tissue / np.sum(diseased_tissue), n=600
)
example_data_sample = pd.DataFrame(
    data=np.array([healthy_sample, diseased_sample]),
    index=[1, 2],
    columns=["A", "B", "C"],
)
example_data_sample["Disease status"] = ["Healthy", "Diseased"]
example_data_sample


plot_data_sample = example_data_sample.melt(
    "Disease status", ["A", "B", "C"], "Cell type", "count"
)

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
sns.barplot(
    data=plot_data_sample, x="Disease status", y="count", hue="Cell type", ax=ax[0]
)
ax[0].set_title("Sampled abundances, by status")

sns.barplot(
    data=plot_data_sample, x="Cell type", y="count", hue="Disease status", ax=ax[1]
)
ax[1].set_title("Sampled abundances, by cell type")
plt.show()


import sccoda.util.cell_composition_data as scc_dat
import sccoda.util.comp_ana as scc_ana
import sccoda.util.data_visualization as scc_viz


frac_by_condition = (
    adata.obs.loc[
        lambda x: x["condition"].isin(
            ["Control", "Salmonella", "Hpoly.Day3", "Hpoly.Day10"]
        )
    ]
    .groupby(["condition", "batch"])
    .apply(lambda x: x.value_counts("cell_label", normalize=False))
    .reset_index(name="n_cells")
    .assign(condition=lambda x: x["condition"].astype(str))
)
frac_by_condition


frac_pivot = frac_by_condition.pivot(
    index=["batch", "condition"],
    columns="cell_label",
    values="n_cells",
).reset_index()
frac_pivot


scc_df = scc_dat.from_pandas(frac_pivot, covariate_columns=["batch", "condition"])
scc_df


scc_viz.boxplots(
    scc_df,
    feature_name="condition",
    figsize=(12, 5),
    add_dots=True,
    args_swarmplot={"palette": ["red"]},
)
plt.show()


scc_viz.stacked_barplot(scc_df, feature_name="condition")
plt.show()


sccoda_mod = scc_ana.CompositionalAnalysis(
    scc_df,
    formula="condition",
    reference_cell_type="Endocrine",
)
sccoda_res = sccoda_mod.sample_hmc(num_results=20000)


sccoda_res


sccoda_res.set_fdr(0.2)


sccoda_res.credible_effects()


credible_effects_salmonella = sccoda_res.credible_effects()["condition[T.Salmonella]"]
credible_effects_hpoly_day3 = sccoda_res.credible_effects()["condition[T.Hpoly.Day3]"]
credible_effects_hpoly_day10 = sccoda_res.credible_effects()["condition[T.Hpoly.Day10]"]
print(credible_effects_salmonella)


salmonella_effect = sccoda_res.effect_df.loc["condition[T.Salmonella]"]
hpoly_effect_3 = sccoda_res.effect_df.loc["condition[T.Hpoly.Day3]"]
hpoly_effected_10 = sccoda_res.effect_df.loc["condition[T.Hpoly.Day10]"]

salmonella_effect


(
    alt.Chart(
        salmonella_effect.loc[credible_effects_salmonella].reset_index(),
        title="Salmonella",
    )
    .mark_bar()
    .encode(
        x=alt.X("Cell Type", sort="y"),
        y="log2-fold change",
        color=alt.Color("Cell Type"),
    )
    | alt.Chart(
        hpoly_effect_3.loc[credible_effects_hpoly_day3].reset_index(),
        title="Heligmosomoides polygyrus day 3",
    )
    .mark_bar()
    .encode(
        x=alt.X("Cell Type", sort="y"),
        y="log2-fold change",
        color=alt.Color("Cell Type"),
    )
    | alt.Chart(
        hpoly_effected_10.loc[credible_effects_hpoly_day10].reset_index(),
        title="Heligmosomoides polygyrus day 10",
    )
    .mark_bar()
    .encode(
        x=alt.X("Cell Type", sort="y"),
        y="log2-fold change",
        color=alt.Color("Cell Type"),
    )
).resolve_scale(y="shared", color="shared")


import toytree as tt
import tasccoda.tree_ana as ta
import tasccoda.tree_utils as tu

import schist


# use logcounts to calculate PCA and neighbors
adata.layers["counts"] = adata.X.copy()
adata.layers["logcounts"] = sc.pp.log1p(adata.layers["counts"]).copy()
adata.X = adata.layers["logcounts"].copy()
sc.pp.neighbors(adata, n_neighbors=10, n_pcs=30)

# Calculate UMAP for visualization purposes
sc.tl.umap(adata)


schist.inference.nested_model(adata, samples=100, random_seed=1234)
adata.obs


sc.pl.umap(
    adata, color=["nsbm_level_1", "nsbm_level_2", "cell_label"], ncols=3, wspace=0.5
)


# Group data
tasccoda_frac = (
    adata.obs.loc[
        lambda x: x["condition"].isin(
            ["Control", "Salmonella", "Hpoly.Day3", "Hpoly.Day10"]
        )
    ]
    .groupby(["condition", "batch"])
    .apply(lambda x: x.value_counts("nsbm_level_1", normalize=False))
    .reset_index(name="n_cells")
    .assign(condition=lambda x: x["condition"].astype(str))
)

# Pivot data
tasccoda_pivot = tasccoda_frac.pivot(
    index=["batch", "condition"],
    columns="nsbm_level_1",
    values="n_cells",
).reset_index()

tasccoda_data = scc_dat.from_pandas(
    tasccoda_pivot, covariate_columns=["batch", "condition"]
)
tasccoda_data


# Convert cluster names to strings
n_levels = 6
for i in range(n_levels):
    adata.obs[f"nsbm_level_{i}"] = adata.obs[f"nsbm_level_{i}"].astype(str)

# Generate tree
newick = tu.df2newick(
    adata.obs.reset_index(),
    levels=[
        "nsbm_level_5",
        "nsbm_level_4",
        "nsbm_level_3",
        "nsbm_level_2",
        "nsbm_level_1",
    ],
)
tree = tt.tree(newick)

tasccoda_data.uns["phylo_tree"] = tree
tasccoda_data.var.index = tasccoda_data.var.index.astype(str)
# draw tree
tree.draw(
    tip_labels_align=True,
    node_sizes=10,
    node_labels="name",
    width=600,
    node_markers="r2x1.25",
    node_colors="lightblue",
    layout="d",
)

# Replace NaN values with 0 counts
tasccoda_data.X = np.nan_to_num(tasccoda_data.X)


tasccoda_mod = ta.CompositionalAnalysisTree(
    tasccoda_data,
    reference_cell_type="19",
    formula="condition",
    pen_args={"phi": 0, "lambda_1": 1.7},
)

tasccoda_res = tasccoda_mod.sample_hmc_da()


covariate = "condition[T.Salmonella]_node"
tasccoda_res.draw_tree_effects(tree, covariate)


covariate = "condition[T.Hpoly.Day3]_node"
tasccoda_res.draw_tree_effects(tree, covariate)


covariate = "condition[T.Hpoly.Day10]_node"
tasccoda_res.draw_tree_effects(tree, covariate)


salmonella_effect = tasccoda_res.effect_df.loc["condition[T.Salmonella]"]
hpoly_effect_3 = tasccoda_res.effect_df.loc["condition[T.Hpoly.Day3]"]
hpoly_effect_10 = tasccoda_res.effect_df.loc["condition[T.Hpoly.Day10]"]

credible_effects_salmonella = salmonella_effect["Effect"] get_ipython().getoutput("= 0")
credible_effects_hpoly_day3 = hpoly_effect_3["Effect"] get_ipython().getoutput("= 0")
credible_effects_hpoly_day10 = hpoly_effect_10["Effect"] get_ipython().getoutput("= 0")
(
    alt.Chart(
        salmonella_effect.loc[credible_effects_salmonella].reset_index(),
        title="Salmonella",
    )
    .mark_bar()
    .encode(
        x=alt.X("Cell Type", sort="y"),
        y="log2-fold change",
        color=alt.Color("Cell Type"),
    )
    | alt.Chart(
        hpoly_effect_3.loc[credible_effects_hpoly_day3].reset_index(),
        title="Heligmosomoides polygyrus day 3",
    )
    .mark_bar()
    .encode(
        x=alt.X("Cell Type", sort="y"),
        y="log2-fold change",
        color=alt.Color("Cell Type"),
    )
    | alt.Chart(
        hpoly_effect_10.loc[credible_effects_hpoly_day10].reset_index(),
        title="Heligmosomoides polygyrus day 10",
    )
    .mark_bar()
    .encode(
        x=alt.X("Cell Type", sort="y"),
        y="log2-fold change",
        color=alt.Color("Cell Type"),
    )
).resolve_scale(y="shared", color="shared")


adata.obs["salmonella_effect_tasccoda"] = [
    tasccoda_res.effect_df.loc[("condition[T.Salmonella]", c), "Effect"]
    for c in adata.obs["nsbm_level_1"]
]
adata.obs["H.poly_3_effect_tasccoda"] = [
    tasccoda_res.effect_df.loc[("condition[T.Hpoly.Day3]", c), "Effect"]
    for c in adata.obs["nsbm_level_1"]
]
adata.obs["H.poly_10_effect_tasccoda"] = [
    tasccoda_res.effect_df.loc[("condition[T.Hpoly.Day10]", c), "Effect"]
    for c in adata.obs["nsbm_level_1"]
]

sc.pl.umap(
    adata,
    color=[
        "salmonella_effect_tasccoda",
        "H.poly_3_effect_tasccoda",
        "H.poly_10_effect_tasccoda",
    ],
    ncols=3,
    wspace=0.25,
    vcenter=0,
    vmax=1.5,
    vmin=-1.5,
)
sc.pl.umap(adata, color=["cell_label", "nsbm_level_1"], ncols=2, wspace=0.5)


import milopy
import milopy.core as milo


adata = sc.read("haber_count.h5ad")


# use logcounts to calculate PCA and neighbors
adata.layers["counts"] = adata.X.copy()
adata.layers["logcounts"] = sc.pp.log1p(adata.layers["counts"]).copy()
adata.X = adata.layers["logcounts"].copy()

sc.pp.highly_variable_genes(
    adata, n_top_genes=3000, subset=False
)  # 3k genes as used by authors for clustering

sc.pp.pca(adata)
sc.pp.neighbors(adata, n_neighbors=10, n_pcs=30)
sc.tl.umap(adata)


sc.pl.umap(adata, color=["condition", "batch", "cell_label"], ncols=3, wspace=0.25)


import scvi

adata_scvi = adata[:, adata.var["highly_variable"]].copy()
scvi.model.SCVI.setup_anndata(adata_scvi, layer="counts", batch_key="batch")
model_scvi = scvi.model.SCVI(adata_scvi)
max_epochs_scvi = np.min([round((20000 / adata.n_obs) * 400), 400])
model_scvi.train(max_epochs=max_epochs_scvi)
adata.obsm["X_scVI"] = model_scvi.get_latent_representation()


sc.pp.neighbors(adata, use_rep="X_scVI")
sc.tl.umap(adata)


sc.pl.umap(adata, color=["condition", "batch", "cell_label"], ncols=3, wspace=0.25)


milo.make_nhoods(adata, prop=0.1)


adata.obsm["nhoods"]


nhood_size = adata.obsm["nhoods"].toarray().sum(0)
plt.hist(nhood_size, bins=20)
plt.xlabel("# cells in neighbourhood")
plt.ylabel("# neighbouthoods");


np.median(nhood_size)


sc.pp.neighbors(adata, n_neighbors=30, use_rep="X_scVI", key_added="milo")
milo.make_nhoods(adata, neighbors_key="milo", prop=0.1)


nhood_size = adata.obsm["nhoods"].toarray().sum(0)
plt.hist(nhood_size, bins=20)
plt.xlabel("# cells in neighbourhood")
plt.ylabel("# neighbouthoods");


milo.count_nhoods(adata, sample_col="batch")


adata.uns["nhood_adata"]


mean_n_cells = adata.uns["nhood_adata"].X.toarray().mean(1)
plt.plot(nhood_size, mean_n_cells, ".")
plt.xlabel("# cells in nhood")
plt.ylabel("Mean # cells per sample in nhood");


milo.DA_nhoods(
    adata, design="~condition", model_contrasts="conditionSalmonella-conditionControl"
)
milo_results_salmonella = adata.uns["nhood_adata"].obs.copy()
milo_results_salmonella


def plot_milo_diagnostics(adata):
    nhood_adata = adata.uns["nhood_adata"].copy()
    alpha = 0.1  ## significance threshold

    with matplotlib.rc_context({"figure.figsize": [12, 12]}):

        ## Check P-value histogram
        plt.subplot(2, 2, 1)
        plt.hist(nhood_adata.obs["PValue"], bins=20)
        plt.xlabel("Uncorrected P-value")

        ## Visualize extent of multiple-testing correction
        plt.subplot(2, 2, 2)
        plt.scatter(nhood_adata.obs["PValue"], nhood_adata.obs["SpatialFDR"], s=3)
        plt.xlabel("Uncorrected P-value")
        plt.ylabel("SpatialFDR")

        ## Visualize volcano plot
        plt.subplot(2, 2, 3)
        plt.scatter(
            nhood_adata.obs["logFC"], -np.log10(nhood_adata.obs["SpatialFDR"]), s=3
        )
        plt.axhline(
            y=-np.log10(alpha),
            color="red",
            linewidth=1,
            label=f"{int(alpha*100)} % SpatialFDR",
        )
        plt.legend()
        plt.xlabel("log-Fold Change")
        plt.ylabel("- log10(SpatialFDR)")
        plt.tight_layout()

        ## Visualize MA plot
        df = nhood_adata.obs
        emp_null = df[df["SpatialFDR"] >= alpha]["logFC"].mean()
        df["Sig"] = df["SpatialFDR"] < alpha

        plt.subplot(2, 2, 4)
        sns.scatterplot(data=df, x="logCPM", y="logFC", hue="Sig")
        plt.axhline(y=0, color="grey", linewidth=1)
        plt.axhline(y=emp_null, color="purple", linewidth=1)
        plt.legend(title=f"< {int(alpha*100)} % SpatialFDR")
        plt.xlabel("Mean log-counts")
        plt.ylabel("log-Fold Change")
        plt.show()


plot_milo_diagnostics(adata)


milopy.utils.build_nhood_graph(adata)
with matplotlib.rc_context({"figure.figsize": [10, 10]}):
    milopy.plot.plot_nhood_graph(adata, alpha=0.1, min_size=5, plot_edges=False)
    sc.pl.umap(adata, color="cell_label", legend_loc="on data")


milopy.utils.annotate_nhoods(adata, anno_col="cell_label")
# Define as mixed if fraction of cells in nhood with same label is lower than 0.75
nhood_adata = adata.uns["nhood_adata"].copy()
nhood_adata.obs.loc[
    nhood_adata.obs["nhood_annotation_frac"] < 0.75, "nhood_annotation"
] = "Mixed"
adata.uns["nhood_adata"] = nhood_adata.copy()


milopy.plot.plot_DA_beeswarm(adata)


## Turn into continuous variable
adata.obs["Hpoly_timecourse"] = adata.obs["condition"].cat.reorder_categories(
    ["Salmonella", "Control", "Hpoly.Day3", "Hpoly.Day10"]
)
adata.obs["Hpoly_timecourse"] = adata.obs["Hpoly_timecourse"].cat.codes

## Here we exclude salmonella samples
test_samples = (
    adata.obs.batch[adata.obs.condition get_ipython().getoutput("= "Salmonella"].astype("str").unique()")
)
milo.DA_nhoods(adata, design="~ Hpoly_timecourse", subset_samples=test_samples)


plot_milo_diagnostics(adata)


with matplotlib.rc_context({"figure.figsize": [10, 10]}):
    milopy.plot.plot_nhood_graph(adata, alpha=0.1, min_size=5, plot_edges=False)


milopy.plot.plot_DA_beeswarm(adata)


def plot_nhood_counts_by_cond(nhood_adata, n_ixs):
    pl_df = pd.DataFrame(nhood_adata[n_ixs].X.A, columns=nhood_adata.var_names).melt(
        var_name="batch", value_name="n_cells"
    )
    pl_df = pd.merge(pl_df, nhood_adata.var)
    pl_df = pl_df[pl_df["Hpoly_timecourse"] >= 0]
    pl_df["log_n_cells"] = np.log1p(pl_df["n_cells"])
    sns.boxplot(data=pl_df, x="Hpoly_timecourse", y="n_cells", color="lightblue")
    sns.stripplot(data=pl_df, x="Hpoly_timecourse", y="n_cells", color="black", s=3)
    plt.xticks(rotation=90)
    plt.xlabel("H.Poly time course")
    plt.ylabel("# cells")


nhood_adata = adata.uns["nhood_adata"].copy()

plt.subplot(121)
entero_ixs = nhood_adata.obs_names[
    (nhood_adata.obs["SpatialFDR"] < 0.1)
    & (nhood_adata.obs["logFC"] < 0)
    & (nhood_adata.obs["nhood_annotation"] == "Enterocyte")
]
plot_nhood_counts_by_cond(adata.uns["nhood_adata"][:, test_samples], entero_ixs)
plt.title("Enterocytes")

plt.subplot(122)
tuft_ixs = nhood_adata.obs_names[
    (nhood_adata.obs["SpatialFDR"] < 0.1)
    & (nhood_adata.obs["logFC"] > 0)
    & (nhood_adata.obs["nhood_annotation"] == "Tuft")
]
plot_nhood_counts_by_cond(adata.uns["nhood_adata"][:, test_samples], tuft_ixs)
plt.title("Tuft cells")
plt.tight_layout()


## Compute average Retnlb expression per neighbourhood
# (you can add mean expression for all genes using milopy.utils.add_nhood_expression)
adata.obs["Retnlb_expression"] = (
    adata[:, "Retnlb"].layers["logcounts"].toarray().ravel()
)
milopy.utils.annotate_nhoods_continuous(adata, "Retnlb_expression")

## Subset to Goblet cell neighbourhoods
nhood_df = adata.uns["nhood_adata"].obs.copy()
nhood_df = nhood_df[nhood_df["nhood_annotation"] == "Goblet"]

sns.scatterplot(data=nhood_df, x="logFC", y="nhood_Retnlb_expression")


## Make dummy confounder for the sake of this example
np.random.seed(42)
nhood_adata = adata.uns["nhood_adata"].copy()
conf_dict = dict(
    zip(
        nhood_adata.var_names,
        np.random.choice(["group1", "group2"], nhood_adata.n_vars),
    )
)
adata.obs["dummy_confounder"] = [conf_dict[x] for x in adata.obs["batch"]]

milo.DA_nhoods(adata, design="~ dummy_confounder+condition")


adata.uns["nhood_adata"].obs
