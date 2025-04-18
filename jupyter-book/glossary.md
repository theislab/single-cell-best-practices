# Glossary

```{glossary}
Adapter sequences
    Short, synthetic DNA or RNA sequences that are ligated to the ends of DNA or RNA fragments during library preparation for sequencing.
    These adapters are essential for binding the fragments to the flowcell and enabling amplification and sequencing.
    However, if adapters are not trimmed after sequencing, they can appear in the reads, potentially interfering with alignment and downstream analyses.

Algorithm
    A pre-defined set of instructions to solve a problem.

AnnData
    A Python package for handling annotated data matrices, commonly used in single-cell and other omics analyses.
    It provides an efficient way to store data as a matrix where rows (observations) and columns (features) can have associated metadata.
    [AnnData](https://anndata.readthedocs.io/en/latest/index.html) supports slicing, subsetting, and saving to disk in formats like H5AD and Zarr.

BAM
    BAM files are binary, compressed versions of SAM (Sequence Alignment/Map) files that store sequencing read alignments to a reference genome.
    They contain the same information as {term}`SAM` files - including read sequences, quality scores, and alignment positions - but in a more space-efficient format that enables faster processing and reduced storage requirements.

Amplification bias
    A distortion that occurs during DNA or RNA amplification (e.g., PCR), where certain sequences are copied more efficiently than others. This can lead to uneven or inaccurate representation of the original genetic material, affecting results in experiments like sequencing or gene expression analysis.

Barcode
    Short DNA barcode fragments ("tags") that are used to identify reads originating from the same cell.
    Reads are later grouped by their barcode during raw data processing steps.

Batch effect
    Technical confounding factors in an experiment that cause dataset distribution shifts.
    Usually lead to inaccurate conclusions if the causes of the batch effects are correlated with outcomes of interest in an experiment and should be accounted for (usually removed).

Benchmark
    An (independent) comparison of performance of several tools with respect to pre-defined metrics.

Bulk RNA sequencing
    Contrary to single-cell sequencing, bulk sequencing measures the average expression values of several cells. Therefore, resolution is lost, but bulk sequencing is usually cheaper, less laborious and faster to analyze.

Cell
    The fundamental unit of life, consisting of cytoplasm enclosed within a membrane, containing biomolecules such as proteins and nucleic acids.
    Cells acquire specific functions, transition into different types, divide, and communicate to sustain an organism.
    Studying cell structure, activity, and interactions enables insights into gene expression dynamics, cellular trajectories, developmental lineages, and disease mechanisms.

Cell type annotation
    The process of labeling groups of {term}`clusters` of cells by {term}`cell type`.
    Commonly done based on {term}`cell type` specific markers, automatically with classifiers or by mapping against a reference.

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

Cluster
    A group of a population or data points that share similarities.
    In single-cell, clusters usually share a common function or marker gene expression that is used for annotation (see {term}`cell type annotation`).

Complementary DNA (cDNA)
    DNA synthesized from an RNA template by the enzyme reverse transcriptase.
    cDNA is commonly used in RNA-seq library preparation because it is more stable than RNA and allows the captured transcripts to be amplified and sequenced for gene expression analysis.

Demultiplexing
    The process of determining which sequencing reads belong to which cell using {term}`barcodes`.

directed graph
    A directed graph (or digraph) is a graph consisting of a set of nodes (vertices) connected by edges (arcs), where each edge has a direction indicating a one-way relationship between nodes.

DNA
    DNA is the acronym of Deoxyribonucleic acid.
    It is the organic chemical storing hereditary information and instructions for protein synthesis.
    DNA gets transcribed into {term}`RNA`.

Doublets
    Reads obtained from droplet based assays might be mistakenly associated to a single cell while the RNA expression origins from two or more cells (a doublet).

Downstream analysis
    A phase of data analysis that follows the initial processing of raw data.
    In the context of scRNA-seq, this includes tasks such as normalization, integration, filtering, cell type identification, trajectory inference, and studying expression dynamics.

Dropout
    A gene with low expression that is observed in one cell, but not in other cells of the same {term}`cell type`.
    The reason for dropouts are commonly low amounts of mRNA expression in cells and the general stochasticity of mRNA expression.
    Dropouts are one of the reasons why scRNA-seq data is sparse.

Drop-seq
    A protocol for scRNA-seq that separates cells into nano-liter sized aqueous droplets enabling large-scale profiling.

Edit distance
    Edit distance (often referred to as Levenshtein distance) measures the minimum number of operations (Substitution, Insertion, Deletion) required to transform one string into another.

FASTQ
    Sequencing reads that are saved in the FASTQ format.
    A FASTQ file stores DNA/RNA sequences and their corresponding quality scores in a 4-line format: identifier, sequence, optional description, and quality scores encoded in ASCII characters.
    FASTQ files are then used to map against the reference genome of interest to obtain gene counts for cells.

Flowcell
    A consumable device used in sequencing platforms where DNA or RNA fragments are sequenced.
    It consists of a glass or polymer surface with lanes or channels coated with oligonucleotides, which capture and anchor DNA or RNA fragments.
    During sequencing, these fragments are amplified into clusters, and their sequences are determined by detecting fluorescent signals emitted during nucleotide incorporation.
    The flowcell enables high-throughput sequencing by allowing millions of fragments to be sequenced simultaneously.

Gene expression matrix
    A cell (barcode) by gene (scverse ecosystem) or gene by cell (barcode) matrix storing counts in the cell values.

Hamming distance
    A measure of the number of positions at which two strings of equal length differ.
    It is commonly used in error detection and correction, including barcode correction in sequencing data.

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

Locus
    Specific position or region on a genome or transcriptome where a particular sequence or genetic feature is located.
    In sequencing, loci refer to the potential origins of a read or fragment, such as a gene, exon, or intergenic region.
    Accurate identification of loci is critical for mapping reads and understanding the genomic or transcriptomic context of the data.

MuData
    A Python package for multimodal annotated data matrices that builds on {term}`AnnData`.
    The primary data structure in the scverse ecosystem for multimodal data.

Muon
    A Python package for multi-modal single-cell analysis in Python by scverse.

Negative binomial distribution
    A discrete probability distribution that models the number of successes in a sequence of independent and identically distributed Bernoulli trials before a specified number of failures.

PCR
    Polymercase chain reaction (PCR) is a method to amplify sequences to create billions of copies.
    PCR requires primers, which are short synthetic {term}`DNA` fragments, to select the genome segments to be amplified and subsequently multiple rounds of {term}`DNA` synthesis to amplify the targeted segments.

Pipeline
    Also often times denoted as workflow.
    A pre-specified selection of steps that are commonly executed in order.

Poisson distribution
    Discrete probability distribution denoting the probability of a specified number of events occurring in a fixed interval of time or space with the events occurring independently at a known constant mean rate.

Promoter
    Sequence of DNA to which proteins bind to initiate and control transcription.

Pseudotime
    Latent and therefore unobserved dimension reflecting cells' progression through transitions.
    Pseudotime is usually related to real time events, but not necessarily the same.

RNA
    Ribonucleic acid (RNA) is a single-stranded nucleic acid present in all living cells that encodes and regulates gene expression.
    Unlike DNA, RNA can be highly dynamic, acting as a messenger (mRNA) to carry genetic instructions, a structural or catalytic component (rRNA, snRNA), or a regulator of gene expression (miRNA, siRNA, lncRNA).
    RNA plays a central role in transcription, translation, and cellular responses, making it essential for understanding gene regulation, development, and disease.

RNA velocity
    RNA velocity measures the rate of change in gene expression by comparing the ratio of unspliced (pre-mRNA) to spliced (mature) mRNA transcripts in single-cell RNA sequencing data.
    This ratio provides insight into whether genes are being actively transcribed (increasing expression) or degraded (decreasing expression), allowing researchers to predict the future state of cells.
    The concept leverages the fact that pre-mRNA signals indicate new transcription while mature mRNA levels reflect steady-state expression, enabling inference of cellular trajectory and developmental dynamics.

RT-qPCR
    Quantitative reverse transcription {term}`PCR` (RT-qPCR) monitors the amplification of a targeted {term}`DNA` molecule during the PCR.

SAM
    SAM (Sequence Alignment/Map) files are tab-delimited text files that store sequencing alignment data, showing how sequencing reads map to a reference genome.
    Each line in a SAM file contains information about a single read alignment, including the read sequence, base quality scores, mapping position, and mapping quality.

scanpy
    A Python package for single-cell analysis in Python by scverse.

scverse
    A consortium for fundamental single-cell tools in the life sciences that are maintaining computational analysis tools like scanpy, muon and scvi-tools.
    See: https://scverse.org/

signal-to-noise ratio
    A measure of the clarity of a signal relative to background noise.
    In sequencing, the signal represents the detectable information derived from the DNA or RNA molecules being sequenced, while the noise includes random errors or unwanted signals that can obscure or distort the true data.
    A high signal-to-noise ratio (SNR) indicates that the signal is strong and reliable compared to the noise, resulting in better data quality.
    Conversely, a low SNR means the noise may interfere with or reduce the accuracy of the sequencing results.

Spike-in RNA
    RNA transcripts of known sequence and quantity to calibrate measurements in RNA hybridization steps for RNA-seq.

Splice Junctions
    Locations where introns are removed, and exons are joined together in a mature RNA transcript during RNA splicing.
    These junctions occur at specific nucleotide sequences and are critical for the proper assembly of functional mRNA.

Trajectory inference
    Also known as pseudotemporal ordering.
    The computational recovery of dynamic processes by ordering cells by similarity or other means.

Unique Molecular Identifier (UMI)
    A special type of molecular barcode that uniquely tags each molecule in a sample library.
    This, for example, enables the estimation of PCR duplication rates (see {term}`amplification bias`), which leads to error correction and increases accuracy.

Untranslated Region (UTR)
    A segment of an mRNA transcript that is transcribed but not translated into protein.
    UTRs are located at both ends of the coding sequence.
```
