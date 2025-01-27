# Glossary

```{glossary}
Adapter sequences
adapter sequences
    Short, synthetic DNA or RNA sequences that are ligated to the ends of DNA or RNA fragments during library preparation for sequencing. These adapters are essential for binding the fragments to the flowcell and enabling amplification and sequencing. However, if adapters are not properly removed or trimmed after sequencing, they can appear in the reads, potentially interfering with alignment and downstream analyses.

Algorithm
Algorithms
    A pre-defined set of instructions to solve a problem.

AnnData
AnnDatas
    A Python package for annotated data matrices. The primary data structure used in the scverse ecosystem.

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
    Contrary to single-cell sequencing, bulk sequencing measures the average expression values of several cells. Therefore, resolution is lost, but bulk sequencing is usually cheaper, less laborious and faster to analyze.

Cell
    The fundamental unit of life. Consists of cytoplasm enclosed within a membrane that contains many biomolecules such as proteins and nucleic acids. Cells acquire specific functions, transition to cell types, divide, communicate and keep the organism going. Learning about the structure, activity and communication of cells helps deciphering biology.

Cell barcode
    See {term}`barcode`

Cell type annotation
    The process of labeling groups of {term}`clusters` of cells by {term}`cell type`. Commonly done based on {term}`cell type` specific markers, automatically with classifiers or by mapping against a reference.

Cell type
    Cells that share common morphological or phenotypic features.

Cell state
    Cells can be annotated according to {term}`cell type` or other cell states as defined by the cell-cycle, perturbational state or other features.

Chromatin
    The complex of DNA and proteins efficiently packaging the DNA inside the nucleus and involved in regulating gene expression.

Cluster
Clusters
    A group of a population or data points that share similarities. In single-cell, clusters usually share a common function or marker gene expression that is used for annotation (see {term}`cell type annotation`).

Complementary DNA (cDNA)
cDNA
    DNA synthesized from an RNA template by the enzyme reverse transcriptase. cDNA is commonly used in RNA-seq library preparation because it is more stable than RNA and allows the captured transcripts to be amplified and sequenced for gene expression analysis.

Demultiplexing
    The process of determining which sequencing reads belong to which cell using {term}`barcodes`.

DNA
    DNA is the acronym of Deoxyribonucleic acid. It is the organic chemical storing hereditary information and instructions for protein synthesis. DNA gets transcribed into {term}`RNA`.

Doublets
    Reads obtained from droplet based assays might be mistakenly associated to a single cell while the RNA expression origins from two or more cells (a doublet).

Downstream analysis
downstream analyses
    A phase of data analysis that follows the initial processing of raw data. In the context of scRNA-seq, this includes tasks such as normalization, integration, filtering, cell type identification, trajectory inference, and studying expression dynamics.

Dropout
    A gene with low expression that is observed in one cell, but not in other cells of the same {term}`cell type`. The reason for dropouts are commonly low amounts of mRNA expression in cells and the general stochasticity of mRNA expression. Dropouts are one of the reasons why scRNA-seq data is sparse.

Drop-seq
    A protocol for scRNA-seq that separates cells into nano-liter sized aqueous droplets enabling large-scale profiling.

FASTQ reads
    Sequencing reads that are saved in the FASTQ format. FASTQ files are then used to map against the reference genome of interest to obtain gene counts for cells.

Flowcell
flowcell
    A consumable device used in sequencing platforms, such as those from Illumina, where DNA or RNA fragments are sequenced. It consists of a glass or polymer surface with lanes or channels coated with oligonucleotides, which capture and anchor DNA or RNA fragments. During sequencing, these fragments are amplified into clusters, and their sequences are determined by detecting fluorescent signals emitted during nucleotide incorporation. The flowcell enables high-throughput sequencing by allowing millions of fragments to be sequenced simultaneously.

Gene expression matrix
    A cell (barcode) by gene (scverse ecosystem) or gene by cell (barcode) matrix storing counts in the cell values.

Imputation
    The replacement of missing values with usually artificial values.

Indrop
    A Droplet based protocol for scRNA-seq.

Library
    Also known as sequencing library. A pool of DNA fragments with attached sequencing adapters.

Locus
Loci
loci
    Specific position or region on a genome or transcriptome where a particular sequence or genetic feature is located. In sequencing, loci refer to the potential origins of a read or fragment, such as a gene, exon, or intergenic region. Accurate identification of loci is critical for mapping reads and understanding the genomic or transcriptomic context of the data.

MuData
    A Python package for multimodal annotated data matrices. The primary data structure in the scverse ecosystem for multimodal data.

Muon
muon
    A Python package for multi-modal single-cell analysis in Python by scverse.

Negative binomial distribution
    A discrete probability distribution that models the number of successes in a sequence of independent and identically distributed Bernoulli trials before a specified number of failures.

RNA
    Ribonucleic acid. Single-stranded nucleic acid present in all living cells that encodes and regulates gene expression.

RT-qPCR
    Quantitative reverse transcription PCR (RT-qPCR) monitors the amplification of a targeted {term}`DNA` molecule during the PCR.

PCR
    Polymercase chain reaction (PCR) is a method to amplify sequences to create billions of copies. PCR requires primers, which are short synthetic {term}`DNA` fragments, to select the genome segments to be amplified and subsequently multiple rounds of {term}`DNA` synthesis to amplify the targeted segments.

Pipeline
    Also often times denoted as workflow. A pre-specified selection of steps that are commonly executed in order.

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

signal-to-noise ratio
    A measure of the clarity of a signal relative to background noise. In sequencing, the signal represents the detectable information derived from the DNA or RNA molecules being sequenced, while the noise includes random errors or unwanted signals that can obscure or distort the true data. A high SNR indicates that the signal is strong and reliable compared to the noise, resulting in better data quality. Conversely, a low SNR means the noise may interfere with or reduce the accuracy of the sequencing results.

Spike-in RNA
    RNA transcripts of known sequence and quantity to calibrate measurements in RNA hybridization steps for RNA-seq.

Trajectory inference
    Also known as pseudotemporal ordering. The computational recovery of dynamic processes by ordering cells by similarity or other means.

Unique Molecular Identifier (UMI)
unique molecular identifiers (UMIs)
    Specific type of molecular barcodes aiding with error correction and increased accuracy during sequencing. UMIs unique tag molecules in sample libraries enabling estimation of PCR duplication rates.
```
