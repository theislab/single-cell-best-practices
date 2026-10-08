---
numbering: false
---

# Outlook

Single-cell analysis has moved from a niche technology to a routine part of biology and medicine.
Datasets now span hundreds of millions of cells, models are pretrained on all of them, and software agents are starting to run analyses on their own.
None of this makes careful analysis less important; it raises the cost of getting it wrong.

## Benchmarking

New tools appear faster than anyone can evaluate them by hand.
Living benchmarks such as [Open Problems in Single-Cell Analysis](https://openproblems.bio/) {cite:p}`ol:Luecken2025` compare methods on shared datasets and metrics, and we will keep updating our recommendations as their results change.
Benchmarks are only as good as their metrics, so agreeing on what defines a good result for each task remains an open problem.

## Foundation models and virtual cells

Models pretrained on tens of millions of cells promise general cell representations that transfer to annotation, integration, and perturbation prediction.
The long-term goal is a virtual cell that predicts how any cell responds to any perturbation {cite:p}`ol:Bunne2024`.
So far, careful evaluations show that these models often do not beat simple baselines, both for zero-shot embeddings {cite:p}`ol:Kedzierska2025` and for perturbation effect prediction {cite:p}`ol:AhlmannEltze2025`.
Until that changes, any foundation model should be compared against a simple baseline on the data at hand.

## Agentic analysis

Large language model agents can now plan an analysis, write the code, and run it {cite:p}`ol:Huang2025`.
This lowers the barrier to single-cell analysis, but it does not remove the need to know what a good analysis looks like.
An agent can pick an unsuitable normalization, leak information between training and test data, or over-interpret clusters just as confidently as a person can, only faster.
We expect best practices like the ones in this book to become the reference that agents follow and that people use to check their output.

## Scale

Perturbation atlases such as Tahoe-100M {cite:p}`ol:Zhang2025` profile more than 100 million cells in a single study.
At this scale, CPU-based analysis becomes the bottleneck, and GPU-accelerated tools such as [rapids-singlecell](introduction/rapids_singlecell.ipynb) {cite:p}`ol:Dicks2026` are becoming the default.
Jointly reanalyzing existing datasets at this scale could also uncover biology that individual studies missed.

## Spatial and multimodal data

Spatial transcriptomics now measures thousands of genes at subcellular resolution, placing cell states back into their tissue context.
Measuring every modality in every cell remains infeasible, so methods that predict missing modalities and integrate unpaired data will stay important.
Single-cell proteomics {cite:p}`ol:Brunner2022` adds the layer closest to cellular function, and its analysis tools will mature as high-quality datasets become routine.

## From cells to patients

Single-cell studies increasingly profile cohorts of hundreds of donors, which turns cell-level findings into patient-level questions.
Answering them requires linking single-cell data to clinical records such as diagnoses, laboratory values, and outcomes.
Electronic health records (EHRs) come with their own pitfalls, including missing values, inconsistent coding, and confounding by treatment.
Frameworks such as ehrapy {cite:p}`ol:Heumos2024` bring the AnnData-based analysis patterns of this book to EHR data, so that both data types can be analyzed in the same ecosystem.
