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

This book does not aim to cover the fundamental basics of biology or computer science including programming. Moreover, this book does not describe all possible tools to approach a specific issue and only focuses on the tools, which ideally were externally verified to work best for the data at hand. Whenever this is not possible and we cannot cover the explicit community verified best-practices, we only recommend a workflow based on our extensive experience.

## Prerequisites

Trying to get into bioinformatics is difficult since a background is required in not only biology, but also computer science. Single-cell especially combines many subfields making it challenging to get into it. This book cannot cover all prerequisites for computational single-cell analysis.

We therefore recommend to have a coarse overview over the following topics:

* Basic Python programming. You should be familiar with control flow (loops, conditional statements, ...), basic data structures (lists, dictionaries, sets) and core functionality of the most used libraries such as Pandas and Numpy. WE RECOMMEND TO LEARN USING WHAT
* Basics of scanpy and AnnData are beneficial. If interested in multimodal data analysis, the basics of muon and MuData are recommended. NOTE THAT WE COVER DATA STRUCTES AND RECOMMEND READING WHAT
* Basics R programming. Familiarity with control flow and basic data structures suffices. WE RECOMMEND LEARNING WITH WHAT
* Basics of biology. While we roughly introduce the generation of the data, we will not cover the fundamentals of DNA, RNA and proteins. WE RECOMMEND LEARNING WITH WHAT
