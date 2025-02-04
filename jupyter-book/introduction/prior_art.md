# Prior art

Single-cell analysis has evolving from a niche area of interest into a well-established field of study.
As a result, we are certainly not the first to produce a book on this subject, nor to provide guides and tutorials.
In the sections that follow, we review two notable and ongoing initiatives aimed at teaching single-cell analysis, highlighting both their similarities to and differences from this book.

## This is a test for html-preview

Here are some changes...
Some more changes. Do we have an own comment in the PR now?

## Bioconductor OSCA and OSTA books

Orchestrating Single-Cell Analysis with Bioconductor (Bioconductor OSCA) {cite}`osca`, available online at https://bioconductor.org/books/release/OSCA/, is an online book designed to teach common workflows for analyzing of single-cell {term}`RNA`-Sequencing (scRNA-seq) data using the R based Bioconductor ecosystem {cite}`pa:Huber2015`.
An accompanying paper with the same title {cite}`Amezquita2020`provides an overview of single-cell analysis with Bioconductor, while the online book offers more in-depth coverage, featuring detailed explanations and extensive code examples.

The OSCA book is highly comprehensive in its treatment of basic scRNA-seq analysis, offering clear explanations and detailed workflow examples.
However, it does not extend to other single-cell omics, such as single-cell ATAC-seq (scATAC-seq).
Spatial transcriptomics is addressed separately in the complementary book Orchestrating Spatially-Resolved Transcriptomics Analysis with Bioconductor (Bioconductor OSTA), available at https://lmweber.org/OSTA-book/.

As both books are tailored to the Bioconductor ecosystem, they exclusively use tools available within Bioconductor.
While these tools are highly effective, they may not always provide the most optimal solution for every analysis, as acknowledged by the books themselves.
Overall, the Bioconductor books are particularly well-suited for individuals with a foundational knowledge of R and a strong background in biology who wish to learn how to analyze single-cell and spatial transcriptomics data within the Bioconductor framework.

## Current best practices in single-cell RNA-seq analysis: a tutorial

Current Best Practices in Single-Cell {term}`RNA`-Seq Analysis: A Tutorial {cite}`pa:Lücken2019` by Malte Lücken and Fabian Theis introduces best practices for scRNA-seq analysis.
Its key contribution lies in not only reviewing potential analysis steps but also recommending best practices based on independent benchmarks.
When specific best-practice guidelines are unavailable, the authors provide general recommendations for analysis approaches.
The fundamental idea of focusing on independent benchmarks inspired our work substantially.
The paper is complemented by an [example analysis of mouse intestinal epithelium regions](https://github.com/theislab/single-cell-tutorial/) from Haber et al. {cite}`pa:Haber2017`.

In comparison to Bioconductor OSCA, this paper and its associated analysis are not constrained by a specific tool ecosystem, offering a broader perspective on the range of topics covered.
However, the accompanying example analysis lacks beginner-friendliness and has become outdated.
Analogously to Bioconductor OSCA, Lücken & Theis do not address newer developments such as RNA velocity, spatial transcriptomics, or multi-omics.

Despite these limitations, we highly recommend this paper as a valuable introduction to the field and as a guide to initial best practices in scRNA-seq analysis.
The chapters in this book build on the latest best practices, offering an updated perspective on the field. Furthermore, the workflows in this book are explained in greater detail, providing readers with the background information necessary to effectively apply the methods.
We advise against relying on the example case study provided with the paper and instead encourage readers to explore the detailed chapters in this book for a more comprehensive and up to date understanding.

## References

```{bibliography}
:filter: docname in docnames
:labelprefix: pa
```
