# Glossary

```{glossary}
Algorithm
Algorithms
    A pre-defined set of instructions to solve a problem.

AnnData
AnnDatas
    A Python package for annotated data matrices. The primary data structure used in the scverse ecosystem.

Amplification bias
    A distortion that occurs during DNA or RNA amplification (e.g., PCR), where certain sequences are copied more efficiently than others. This can lead to uneven or inaccurate representation of the original genetic material, affecting results in experiments like sequencing or gene expression analysis.


Barcode
Barcodes
Bar code
Bar codes
    Short DNA barcode fragments ("tags") that are used to identify reads originating from the same cell. Reads are later grouped by their barcode during raw data processing steps.

Batch effect
    Technical confounding factors in an experiment that cause dataset distribution shifts. Usually lead to inaccurate conclusions if the causes of the batch effects are correlated with outcomes of interest in an experiment and should be accounted for (usually removed).

Benchmark
    An (independent) comparison of performance of several tools with respect to pre-defined metrics.

Bulk RNA sequencing
bulk RNA-Seq
bulk sequencing
    Contrary to single-cell sequencing, bulk sequencing measures the average expression values of several cells. Therefore, resolution is lost, but bulk sequencing is usually cheaper, less laborious and faster to analyze.

Cell
cells
    The fundamental unit of life. Consists of cytoplasm enclosed within a membrane that contains many biomolecules such as proteins and nucleic acids. Cells acquire specific functions, transition to cell types, divide, communicate and keep the organism going. Learning about the structure, activity and communication of cells helps deciphering biology.

Cell barcode
    See {term}`barcode`

Cluster
Clusters
    A group of a population or data points that share similarities. In single-cell, clusters usually share a common function or marker gene expression that is used for annotation (see {term}`cell type annotation`).

Cell type annotation
    The process of labeling groups of {term}`clusters` of cells by {term}`cell type`. Commonly done based on {term}`cell type` specific markers, automatically with classifiers or by mapping against a reference.

Cell type
    Cells that share common morphological or phenotypic features.

Cell state
    Cells can be annotated according to {term}`cell type` or other cell states as defined by the cell-cycle, perturbational state or other features.

Chromatin
    The complex of DNA and proteins efficiently packaging the DNA inside the nucleus and involved in regulating gene expression.

Codon
    A sequence of three nucleotides corresponding to a specific amino acid or a start/stop signal in protein synthesis.
    Codons are the basic units of the genetic code, determining how genetic information is translated into proteins.

CpG
    A DNA sequence in which a cytosine (C) is followed by a guanine (G) along the 5' &rarr; 3' direction, linked by a phosphodiester bond.
    CpG sites are often found in clusters called CpG islands near gene promoters.
    Unmethylated CpG sites are associated with gene activation, while methylated CpG sites can lead to gene inhibition.

Demultiplexing
    The process of determining which sequencing reads belong to which cell using {term}`barcodes`.

DNA
    DNA is the acronym of Deoxyribonucleic acid. It is the organic chemical storing hereditary information and instructions for protein synthesis. DNA gets transcribed into {term}`RNA`.

Doublets
    Reads obtained from droplet based assays might be mistakenly associated to a single cell while the RNA expression origins from two or more cells (a doublet).

Dropout
    A gene with low expression that is observed in one cell, but not in other cells of the same {term}`cell type`. The reason for dropouts are commonly low amounts of mRNA expression in cells and the general stochasticity of mRNA expression. Dropouts are one of the reasons why scRNA-seq data is sparse.

Drop-seq
    A protocol for scRNA-seq that separates cells into nano-liter sized aqueous droplets enabling large-scale profiling.

FASTQ reads
    Sequencing reads that are saved in the FASTQ format. FASTQ files are then used to map against the reference genome of interest to obtain gene counts for cells.

Gene expression matrix
    A cell (barcode) by gene (scverse ecosystem) or gene by cell (barcode) matrix storing counts in the cell values.

Imputation
    The replacement of missing values with usually artificial values.

Indrop
    A Droplet based protocol for scRNA-seq.

Library
    Also known as sequencing library. A pool of DNA fragments with attached sequencing adapters.

Modalities
Multimodal
    Different types of biological information measured at the single-cell level.
    These include gene expression, chromatin accessibility, surface proteins, immune receptor sequences, and spatial organization.
    Combining these modalities provides a more complete understanding of cell identity, function, and interactions.

MuData
    A Python package for multimodal annotated data matrices. The primary data structure in the scverse ecosystem for multimodal data.

muon
    A Python package for multi-modal single-cell analysis in Python by scverse.

Negative binomial distribution
    A discrete probability distribution that models the number of successes in a sequence of independent and identically distributed Bernoulli trials before a specified number of failures.

Pipeline
    Also often times denoted as workflow. A pre-specified selection of steps that are commonly executed in order.

RNA
    Ribonucleic acid. Single-stranded nucleic acid present in all living cells that encodes and regulates gene expression.

RT-qPCR
    Quantitative reverse transcription PCR (RT-qPCR) monitors the amplification of a targeted {term}`DNA` molecule during the PCR.

PCR
    Polymercase chain reaction (PCR) is a method to amplify sequences to create billions of copies. PCR requires primers, which are short synthetic {term}`DNA` fragments, to select the genome segments to be amplified and subsequently multiple rounds of {term}`DNA` synthesis to amplify the targeted segments.

Poisson distribution
    Discrete probability distribution denoting the probability of a specified number of events occurring in a fixed interval of time or space with the events occurring independently at a known constant mean rate.

Promoter
    Sequence of DNA to which proteins bind to initiate and control transcription.

Pseudotime
    Latent and therefore unobserved dimension reflecting cells' progression through transitions. Pseudotime is usually related to real time events, but not necessarily the same.

scanpy
    A Python package for single-cell analysis in Python by scverse.

scverse
    A consortium for fundamental single-cell tools in the life sciences that are maintaining computational analysis tools like scanpy, muon and scvi-tools. See: https://scverse.org/

Spike-in RNA
    RNA transcripts of known sequence and quantity to calibrate measurements in RNA hybridization steps for RNA-seq.

Trajectory inference
    Also known as pseudotemporal ordering. The computational recovery of dynamic processes by ordering cells by similarity or other means.

UMI
Unique Molecular Identifier (UMI)
    A unique molecular identifier (UMI) is a special type of molecular barcode that uniquely tags each molecule in a sample library.
    This, for example, enables the estimation of PCR duplication rates (see {term}`amplification bias`), which leads to error correction and increases accuracy.
```
