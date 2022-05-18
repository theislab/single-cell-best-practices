# Raw data processing

## What output does the sequencer give us (base calling)

## From BCF to FASTQ

## Read QC

FASTQC
and many more

## Multiplexing/Demultiplexing (with barcodes)

UMI tools

## Alignment

Reference vs reference free alignment

BWA
Kallisto
Starsolo

## Filtering

BUStools

## Quantification

Alevin

## Collecting results with Multiqc

Might not be a section, but noteworthy

## Pipelines

cell ranger
nf-core <- alevin

just that they exist

## Raw data QC issues that might lead to downstream errors

Determining droplets that have no droplet inside them (part of raw processing pipelines QC <- e.g. cell ranger)
dropletutils

## useful links

https://training.galaxyproject.org/training-material/topics/transcriptomics/tutorials/scrna-preprocessing-tenx/tutorial.html

https://training.galaxyproject.org/training-material/topics/transcriptomics/tutorials/scrna-preprocessing/tutorial.html