![alt text](_static/images/title.jpg "Title")

<div style="page-break-after: always;"></div>

# Cross-modal Single-cell Best-practices

## Introduction

The human body is a complex machine that heavily relies on the basic units of life - cells. Cells can be separated into different types, which even undergo transitions during development, under disease or when regenerating. This cellular heterogeneity is reflected in their morphology, function, and gene expression profiles. Strong disruptions causing deregulations of the cell types influence the entire system causing potentially even serious diseases like cancer{cite}`Macaulay2017`. It is therefore vital to understand how cells behave in a normal state and under perturbations to improve our understanding of the entire cellular systems.

This monumental task is approached in different ways of which the most promising one is to profile cells at the individual level. So far, each cells' transcriptome was primarily examined in a process known as single-cell {term}`RNA` sequencing. With recent advances in single-cell genomics, it is now possible to enrich the transcriptome information with spatial, chromatin accessibility or protein information. These advances generate not only insight into complex regulatory mechanisms, but also go along with additional complexity for data analysts.

Nowadays, data analysts are facing a vast analysis tool landscape with a collection of more than 1000 computational single-cell analysis methods. It is becoming increasingly challenging to navigate this large range of different tools to generate sound results which are at the forefront of science.

## What this book covers

The goal of this book is to teach newcomers and advanced professionals alike, the **best-practices** of single-cell sequencing analysis.
This book will teach you the most common analysis steps ranging from preprocessing to visualization to statistical evaluation and beyond. A read through the entire book will enable you to analyze unimodal and multimodal single-cell sequencing data on your own. The guidelines and recommendations in this book are not only tailored to teach you how to do single-cell analysis in general, but how to do them right. We base our suggestions on external benchmarks and reviews whenever possible. Finally, we consider this book to be a living resource for single-cell data analysts which can easily be updated when the recommendations change.

## What this book does not cover

This book does not cover fundamental basics of biology or computer science, including programming. Furthermore, this book does not function as a complete collection of all analysis tools designed for a specific tasks. We especially highlight externally verified tools, which work best for the data at hand or methods which proved to be community-verified best practices. Whenever this is not possible, we only recommend workflows based on our extensive experience.

## Structure of the book

Each chapter in this book corresponds to a different stage of a typical single-cell data analysis project. Generally, an analysis workflow would follow the order of the chapters. Chapters are labeled as basic or advanced. Newcomers are recommended to start with all basic chapters and potentially revisit the advanced chapters of interest afterwards. Advanced chapters introduce analysis steps that may require more prerequisites compared to other chapters of the book. Most single-cell data analysts do not conduct all advanced analyses in their daily work, but being aware of the possibilities is still beneficial.

Chapters are additionally labeled with a traffic light system. We differentiate the chapters into three groups:

- Chapters labeled with white are rather novel and no best-practices exist in any way. For these, we cannot recommend the best analysis tool and hence, we show one way to tackle the underlying task.

- For yellow chapters, no clear, community-agreed, best practices exist. A few independent benchmarks may exist, but they might be in preprint or evidence might be sparse. In this chapter, we recommend analysis workflows that proved well-working according to our vast experience, and we can therefore wholeheartedly recommend the stated tools.

- Green chapters are validated by several independent benchmarks and there is a strong community agreement on the preferred tool that should be used for this analysis step. Generally, we are confident in our recommendations and strongly recommend readers to take our suggestions into account for their own analyses.

SHOW SOME OF MESHALS COOL IMAGES HERE

All of our chapters feature extensive lists of references, and we encourage readers to consult the primary sources for our statements. Our summaries cannot always capture the full reasoning for our recommendations, although we try to provide the required background whenever possible.

## Prerequisites

Bioinformatics is a challenging research field for newcomers as it requires knowledge in both biology and computer science. Single-cell is even more demanding as it combines many subfields and datasets are often large. This book cannot cover all prerequisites for computational single-cell analysis, we therefore recommend a coarse overview of various topics below. The following links might increase your learning experience throughout the book:

- Basic Python programming. You should be familiar with control flow (loops, conditional statements, ...), basic data structures (lists, dictionaries, sets) and core functionality of the most used libraries such as Pandas and Numpy. If you are new to programming and Python we can highly recommend the free [Automate the boring stuff with Python](https://automatetheboringstuff.com/) book.

- Basics of the AnnData and scanpy packages are beneficial, but not absolutely required. This book covers AnnData in sufficient detail to follow along and introduces the workflow of working with scanpy. However, we are not able to introduce all of scanpy's functionalities in the course of this book. If you are new to scanpy we strongly suggest to work through the [scanpy tutorials](https://scanpy.readthedocs.io/en/stable/tutorials.html) with the occasional glance to the [scanpy API reference](https://scanpy.readthedocs.io/en/stable/api.html).

- If you are interested in multimodal data analysis, the basics of muon and MuData are recommended. This book covers MuData in greater detail, but only briefly introduces muon analogously to AnnData and scanpy. The excellent [muon tutorials](https://muon-tutorials.readthedocs.io/en/latest/) serve as a great introduction to multimodal data analysis with muon.

- Basics R programming. Familiarity with control flow and basic data structures suffices. If you are new to programming and R we recommend the free [R for data science](https://r4ds.had.co.nz/) book.

- Basics of biology. While we roughly introduce the generation of the data, we will not cover the fundamentals of {term}`DNA`, {term}`RNA` and proteins. If you are completely new to molecular biology in general, it might be advisable to work through _Molecular Biology of the Cell_ by Bruce Alberts et al.

## Citation

TBD

## Contributing

We would like to invite the community to further improve the tutorial and the teaching material.
Please read [contributing](https://github.com/theislab/cross-modal-single-cell-best-practices/blob/development/CONTRIBUTING.md) for further instructions.

In case of questions or problems, please get in touch by posting an issue in this repository.

## Alternative formats

PDF versions of this book are available on our [releases page](https://github.com/theislab/cross-modal-single-cell-best-practices/releases).

## Contact us

You can report issues and requests in our [issue tracker](https://github.com/theislab/cross-modal-single-cell-best-practices/issues). For speaking engagements or collaborations, send an email at anna DOT schaar AT helmholtz-munich DOT de or lukas DOT heumos AT helmholtz-munich DOT de.

## License

This book is licensed under the [Apache 2.0 license](https://github.com/theislab/cross-modal-single-cell-best-practices/blob/development/LICENSE).

## References

```{bibliography}
:filter: docname in docnames
```
