![alt text](_static/images/title.jpg "Title")

<div style="page-break-after: always;"></div>

# Extended Single-cell Best-practices

## Overview

The goal of this book is to teach newcomers and advanced professionals alike, the **best-practices** of single-cell sequencing analysis.
This book will teach you about the most common analysis steps ranging from preprocessing over visualization to statistical evaluation.
After having worked through this book you will be able to analyze unimodal and multimodal sequencing data on your own.

## Motivation

As once newcomers ourselves in the field, we noticed that while teaching materials exist they are often scattered in various places. Furthermore, in a rapidly developing research area like single-cell, many tools exist and even more get published every day. It is difficult to know which tool to use for which steps and why.
Hence, we committed to writing our guidelines on not only how to do things, but how to do things right. These suggestions are based on external benchmarks and reviews whereever possible. Finally, we consider this book to be a living book which can easily be updated when the recommendations change.

## What this book covers

This book aims to be comprehensive and to cover as many analysis steps as possible. We cover all steps depicted in figure X while adding additional information for situations that an analyst run into. A simple example might be the conversion between analysis ecosystems and data formats.

## What this book does not cover

This book does not aim to cover the fundamental basics of biology or computer science including programming. Moreover, this book does not describe all possible tools to approach a specific issue and only focuses on the tools, which ideally were externally verified to work best for the data at hand. Whenever this is not possible and we cannot cover explicit community verified best-practices, we only recommend workflows based on our extensive experience.

## Structure of the book

This book is divided into chapters which correspond to different stages of a typical single-cell data analysis project. Generally, a typical analysis would follow the order of the chapters. We further divide the chapters into basic and advanced chapters. As the name suggests, the advanced chapters cover advanced analysis steps and may require more prerequisites than the other chapters of the book. We recommend that newcomers to the field start with all basic chapters and afterwards revisit the advanced chapters of interest. Most single-cell data analysts do not conduct all of the advanced analyses in their day to day work, but being aware of the possibilities is still beneficial.

Further, the chapters are labeled with a traffic light system. We differentiate the chapters into three groups:

* No best-practices exist in any way and the topic is very recent. We cannot recommend best practices nor do we know how to conduct this analysis step properly. We show one way to tackle the issue. The traffic light color for these chapters is SOMETHING.

* For COLOR colored chapters no clear, community agreed, best practices exist. There may be one benchmark paper already out, but evidence is sparse. Furthermore, we may be very experienced in the analysis of discussion and can therefore wholeheartedly recommend an analysis workflow and know the pitfalls to be aware of.

* Topics for which explicit best practices exist with evidence of several strong benchmarking are colored in COLOR. Generally, we are confident in our recommendations and strongly recommend readers to take our suggestions into account for their own analyses.

SHOW SOME OF MESHALS COOL IMAGES HERE

All of our chapters feature extensive lists of references and we encourage readers to consult the primary sources for our statements. Our summaries cannot always capture the full reasoning for our recommendations although we try to provide the required background whenever possible.

## Prerequisites

Trying to get into bioinformatics is difficult since a background is required in not only biology, but also computer science. Single-cell especially combines many subfields making it challenging to get into it. This book cannot cover all prerequisites for computational single-cell analysis. To get the most out of this book we recommend a coarse overview over the following topics:

* Basic Python programming. You should be familiar with control flow (loops, conditional statements, ...), basic data structures (lists, dictionaries, sets) and core functionality of the most used libraries such as Pandas and Numpy. If you are new to programming and Python we can highly recommend the free [Automate the boring stuff with Python](https://automatetheboringstuff.com/) book.

* Basics of the AnnData and scanpy packages are beneficial, but not absolutely required. This book covers AnnData in sufficient detail to follow along and introduces the workflow of working with scanpy. However, it is not possible to introduce all of scanpy's functions in the course of this book. If you are new to scanpy we strongly suggest to work through the [scanpy tutorials](https://scanpy.readthedocs.io/en/stable/tutorials.html) with the occasional glance to the [scanpy API reference](https://scanpy.readthedocs.io/en/stable/api.html).

* If you are interested in multimodal data analysis, the basics of muon and MuData are recommended. This book covers MuData in greater detail, but only briefly introduces muon analogously to AnnData and scanpy. The excellent [muon tutorials](https://muon-tutorials.readthedocs.io/en/latest/) serve as a great introduction to multimodal data analysis with muon.

* Basics R programming. Familiarity with control flow and basic data structures suffices. If you are new to programming and R we recommend the free [R for data science](https://r4ds.had.co.nz/) book.

* Basics of biology. While we roughly introduce the generation of the data, we will not cover the fundamentals of DNA, RNA and proteins. If you are completely new to molecular biology in general, it might be advisable to work through *Molecular Biology of the Cell* by Bruce Alberts et al.

## References

```{bibliography}
:filter: docname in docnames
```
