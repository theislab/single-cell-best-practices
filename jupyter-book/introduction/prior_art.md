# Prior art

Single-cell analysis is slowly transitioning from an interesting niche topic to a more mature field. Hence, we are arguably not the first to write a book on single-cell analysis, let alone guides and tutorials. In the following sections, we highlight two existing and ongoing efforts to teach single-cell analysis and emphasize commonalities and differences to this book.

## Bioconductor OSCA

Orchestrating Single-Cell Analysis with Bioconductor (Bioconductor OSCA){cite}`osca` accessible at https://bioconductor.org/books/release/OSCA/ is a digital book which aims to teach common workflows for the analysis of single-cell {term}`RNA`-Seq with the R based Bioconductor{cite}`pa:Huber2015` ecosystem. A paper with the same name{cite}`Amezquita2020` presented an overview of single-cell analysis with Bioconductor and the book is an associated online version which goes into greater detail with extensive code examples.

The book is very comprehensive with respect to basic single-cell RNA-Seq analysis with great explanations and extensive workflow examples. However, it does not comprise advanced topics such as RNA velocity, spatial transcriptomics and others. Moreover, additional modalities such as ATAC-Seq or CITE-Seq data, or the multimodal integration of these are not covered. Since the book is designed for the Bioconductor ecosystem it only employs tools available on Bioconductor. These do not necessarily result in an optimal analysis as denoted in the book itself. We perceive the Bioconductor OSCA book as especially useful for people with a basic R and stronger biology background who are interested in learning how to analyze single-cell RNA-Seq data analysis with Bioconductor.

## Current best practices in single-cell RNA-seq analysis: a tutorial

Current best practices in single-cell {term}`RNA`-seq analysis: a tutorial{cite}`pa:Lücken2019` is a paper written by Malte Lücken and Fabian Theis which introduces best practice single-cell {term}`RNA`-Seq analysis. The unique contribution of the paper to the field is that it not only serves as a review of the possible analysis steps, but always suggests best practices based on independent benchmarks. Whenever recommendations for best practices are not available, general recommendations for analysis approaches are suggested. The paper itself is accompanied with an [example analysis of mouse intestinal epithelium regions](https://github.com/theislab/single-cell-tutorial/) from Haber et al. {cite}`pa:Haber2017`.

Compared to Bioconductor OSCA, the paper and the example analysis is not biased by the tools that it showcases and more complete in content with respect to the breadth of covered topics. Nevertheless, the associated example analysis lacks in newbie friendliness and has already become outdated. Moreover, similarly to the Bioconductor OSCA paper and book, Lücken and Theis do not cover more recent topics such as RNA velocity, spatial transcriptomics or multi-omics. We strongly recommend the paper as an introduction and overview to the field and initial analysis best-practice recommendations. The chapters in this book are based on the most recent best practices and provide an updated view on the field. Additionally, the analysis workflows in this book are explained in much more detail to provide readers more background information needed to run the methods. We generally advise against examining the associated case-study and suggest to instead read the chapters of this book in detail.

## References

```{bibliography}
:filter: docname in docnames
:labelprefix: pa
```
