# Outlook

The single-cell field is progressing at a rapid pace. This process is accompanied by a massive amount of newly developed tools, which do not allow for new discoveries, but also extend the pool of tools to select from.

## Benchmarking

Due to the vast amount of tools to choose from, we expect further and regular benchmarking to become even more important. Efforts such as [Open Problems in Single-Cell Analysis](https://openproblems.bio/), which aim to benchmark tools using well-defined metrics applied to standard datasets, will become essential.
However, for benchmarking to be successful, the single-cell community has to agree on a set of metrics per task.
We therefore expect discussions on what defines "good" or "bad" analysis steps to become increasingly important.
As soon as new benchmarking results and tool recommendations become available, we will update our chapters.

## Atlas building and reference mapping

With the advent of more single-cell atlases, we expect a slow transition from less manual annotation to more automated annotation _via_ reference mapping.
For this to become a reality, the single-cell community needs not only healthy reference atlases, but also reference atlases for various conditions such as diseases.
We envision reference mapping to also allow for automated quality control through uncertainty estimation.
Cells that have a hard time getting mapped onto high quality references are either of low quality or highly biologically relevant.

## Modality prediction

Single-cell analysis is slowly starting to move on from unimodal to cross-modal perspectives to obtain complete views of cells.
Though, it is not always possible to obtain all modalities. We therefore expect modality prediction and unpaired integration methods to become more important.

## End-to-end pipelines

The amount of single-cell data and analysis possibilities is growing on such a big scale that it is inevitable that as many processes as possible should be automated.
With the advent of reference mapping to atlases to automate cell type annotation and automated quality control tools, the development of highly automated pipelines is becoming a real possibility.
Especially, the reanalysis of "old", existing datasets could uncover previously missed biology.
The first pipelines are starting to appear {cite}`ol:Khozoie2021`, and we expect more pipelines with support for modalities beyond {term}`RNA` to be developed.

## Single-cell proteomics

Furthermore, the young and fast evolving field of single-cell proteomics {cite}`Brunner2022` will bring an additional modality into the single-cell space with more integration challenges, but also great potential for new discoveries.
Currently, single-cell proteomics suffers from a lack of high quality datasets, making it challenging to develop tools and pipelines for sound statistical analysis.
As soon as high quality single-cell proteomics datasets are generated on a regular basis, we expect the single-cell community to develop new tools for the analysis.

## References

```{bibliography}
:filter: docname in docnames
:labelprefix: ol
```
