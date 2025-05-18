# Single-cell RNA sequencing

This chapter briefly introduces the most widely used single-cell ribonucleic acid ({term}`RNA`) sequencing assays and associated basic molecular biology concepts.
{term}`Multimodal <Modalities>` or spatial assays are not covered here but are introduced in the respective advanced chapters.
All {term}`sequencing` assays have individual strengths and limitations, which must be known by data analysts to be aware of possible biases in the data.

## The building block of life

Life, as we know it, is the characteristic that distinguishes living from dead or inanimate entities.
Most definitions of the term life share a common entity - {term}`cells <Cell>`.
Cells form open systems which maintain homeostasis, have a metabolism, grow, adapt to their environment, reproduce, respond to stimuli, and organize themselves.
Therefore, cells are the fundamental building blocks of life, and they were first discovered in 1665 by the British scientist Robert Hooke.
Hooke investigated a thin slice of cork with a very rudimentary microscope and, to his surprise, noticed that the slice appeared to resemble a honeycomb.
He named these tiny units "cells".

:::{figure-md} markdown-fig
<img src="../_static/images/scrna_seq/hooke_cork.jpg" alt="Robert Hook cell" class="bg-primary mb-1" width="100%">

Robert Hooke's drawing of cork cells. Image obtained from Micrographia.
:::

In 1839, Matthias Jakob Schleiden and Theodor Schwann first described Cell Theory, stating that all living organisms are made up of cells.
Since the early definition of Cell Theory, researchers have discovered that all cells have almost the same chemical composition and exhibit a dynamic flow of information passing the genetic code from one cell to another in the form of deoxyribonucleic acid ({term}`DNA`).
Two general types of cells exist: eukaryotes and prokaryotes.
Eukaryotic cells contain a nucleus, where the nuclear membrane encapsulates the chromosomes; while prokaryotic cells only have a nucleoid region but no nucleus.
The nucleus hosts the cells' genomic DNA, which is why they are called eukaryotes: _Nucleus_ is Latin for kernel or seed.
The DNA replication machinery reads the hereditary information that is stored in the DNA in the nucleus to replicate themselves and keep the life cycle going.
The eukaryotic DNA is divided into several linear bundles called chromosomes, which are separated by the microtubular spindle during nuclear division.
Understanding the hereditary information hidden in DNA is key to understanding many evolutionary and disease-related processes.

Sequencing is the process of deciphering the order of DNA nucleotides.
It is primarily used to unveil the genetic information that is carried by a specific DNA segment, a complete genome, or even a complex microbiome.
DNA sequencing allows researchers to identify a gene's location, function, and regulation. For example, it uncovers genetic features such as open reading frames (ORF), the protein-coding sequences between start & stop codons, or {term}`CpG` islands, which indicate {term}`promotor` regions.
Another widespread application area is evolutionary analysis, where homologous DNA sequences from different organisms are compared.
DNA sequencing can additionally be applied for the associations between mutations and diseases or sometimes even disease resistance, deeming it one of the most valuable applications.

(introduction-scrna-seq-key-takeaway-1)=

## A brief history of sequencing

### First-generation sequencing

Although DNA was already first isolated in 1869 by Friedrich Miescher, it took the scientific community more than 100 years to develop high-throughput sequencing technologies.
In 1953, Watson, Crick, and Franklin discovered the structure of DNA, and in 1965, Robert Holley sequenced the first tRNA.
Seven years later, in 1972, Walter Fiers was the first to sequence a complete gene (the coat protein of bacteriophage MS2) using RNases to digest the virus RNA, isolate oligonucleotides and finally separate them with electrophoresis and chromatography {cite}`Jou1972`.
In parallel, Frederick Sanger developed a DNA sequencing method using radiolabeled, partially digested fragments termed "chain termination method", which is more commonly known as "Sanger Sequencing".
Although Sanger Sequencing is still used today, it has suffered from several shortcomings, including lack of automation and being time-consuming.
In 1987, Leroy Hood and Michael Hunkapiller developed the ABI 370, an instrument that automates the Sanger Sequencing process.
Its most crucial innovative accomplishment was the automatic labeling of DNA fragments with fluorescent dyes instead of radioactive molecules.
This change not only made the method safer to perform but also allowed computers to analyze the acquired data {cite}`Hood1987`.

```{dropdown} <i class="fa-solid fa-thumbs-up"></i>   Strengths

- Sanger sequencing is simple and affordable.
- If done correctly, the error rate is very low (<0.001%).
```

```{dropdown} <i class="fa-solid fa-thumbs-down"></i></i>   Limitations
:class: open
- Sanger methods can only sequence short pieces of DNA of about 300 to 1000 base pairs.
- The quality of a Sanger sequence is often poor in the first 15 to 40 bases because this is where the primers bind.
- Sequencing degrades after 700 to 900 bases.
- If the sequenced DNA fragment has been cloned, some of the cloning vector sequence (a DNA carrier for copying, storing, and amplifying genes) may find its way into the final sequence.
- Sanger sequencing is more expensive than second or third-generation sequencing per sequenced base.
```

### Second-generation sequencing

Nine years later, in 1996, Mostafa Ronaghi, Mathias Uhlen, and Pȧl Nyŕen revolutionized DNA sequencing by developing pyrosequencing, marking the beginning of second-generation sequencing.
Second-generation sequencing, also known as next-generation sequencing (NGS), was primarily made possible by further automation in the lab, the usage of computers, and the miniaturization of reactions.
Pyrosequencing measures luminescence that is generated by pyrophosphate synthesis during sequencing.
This process is also commonly known as "sequencing-by-synthesis".
Two years later, Shankar Balasubramanian and David Klenerman developed and adapted the sequencing-by-synthesis process for a new method that utilizes fluorescent dyes at the company Solexa.
Solexa’s technology also forms the basis of Illumina’s sequencers, which dominate today's market.
The Roche 454 sequencer, developed in 2005, was the first sequencer to fully automate the pyrosequencing process in a single, automated machine.
Life Technologies introduced several other platforms, including SOLiD in 2007 (a "sequencing-by-ligation" system) and Ion Torrent in 2011 (detecting hydrogen ions during the synthesis of new DNA).
In general, sequencing-by-synthesis involves adding single nucleotides to a growing DNA strand and detecting each addition.
At the same time, sequencing-by-ligation relies on detecting the joining of short DNA probes to the fragment to determine the sequence.

```{dropdown} <i class="fa-solid fa-thumbs-up"></i>   Strengths
- Second-generation sequencing is often the cheapest option concerning required chemicals.
- Sparse material can still be used as input.
- High sensitivity to detect low-frequency variants and comprehensive genome coverage.
- High capacity with sample multiplexing.
- Ability to sequence thousands of genes simultaneously.
```

```{dropdown} <i class="fa-solid fa-thumbs-down"></i></i>   Limitations
- The sequencing machines are expensive and often must be shared with colleagues.
- Second-generation sequencers are big, stationary machines that are not designed for fieldwork.
- Generally, second-generation sequencing results in many short sequencing fragments (reads) that are hard to use for novel genomes.
- The quality of the sequencing result depends on the reference genome.
```

### Third-generation sequencing

The third generation of sequencing, nowadays also known as next-generation sequencing, has brought two innovations to the market.
First, long-read sequencing, which enables the detection of nucleotide fragments that are much longer than those generated by second-generation sequencing.
The typical Illumina short-read sequencers generate fragments ranging from 75 to 300 base pairs, depending on the model.
With third-generation sequencing, sequencers can read tens of thousands of base pairs.
This is especially important for the assembly of novel genomes without an available reference genome.
Second, the ability to sequence in real-time is another major advancement in third-generation sequencing.
Combined with portable sequencers, which are small in size and do not require further complex machines for the chemistry, sequencing is now "field-ready" and can be used even far away from laboratory facilities to collect samples.

```{admonition} A note on sequencing length
:class: note, dropdown
- 1 base pair (bp)
- 1 kilo base pair (kb) = 1,000 bp
- 1 mega base pair (Mb) = 1,000,000 bp
- 1 giga base pair (Gb) = 1,000,000,000 bp
```

Pacific Biosciences (PacBio) introduced zero-mode waveguide sequencing in 2010, which uses so-called nanoholes containing a single DNA polymerase.
This allows the incorporation of any single nucleotide to be directly observed by detectors attached below the nanoholes.
Each type of nucleotide is labeled with a specific fluorescent dye that emits fluorescent signals during the incorporation process, which are subsequently measured as sequence readout.
Reads obtained from PacBio sequencers are usually 8 to 15 kb, with possibilities for up to 70 kb.

Oxford Nanopore Technologies introduced the GridION in 2012. The GridION and its successors, MinION and Flongle, are portable sequencers for DNA and RNA sequencing, which produce reads of more than 2 Mb.
Notably, such a sequencing device even fits into a single human hand.
The idea of Oxford Nanopore sequencers is to detect changes in the electrical current as nucleic acids migrate through protein nanopores {cite}`Jain2016`.

```{dropdown} <i class="fa-solid fa-thumbs-up"></i>   Strengths
- Long reads will allow for the assembly of large novel genomes.
- Sequencers are portable, making them ideal for fieldwork.
- Possibility to directly detect epigenetic modifications of DNA and RNA sequences.
- Speed! Third-generation sequencers are fast.
```

```{dropdown} <i class="fa-solid fa-thumbs-down"></i></i>   Limitations
- Some third-generation sequencers exhibit higher error rates than second-generation sequencers (Roche's new sequencing by expansion technology, for example, attempts to solve this problem {cite}`Jain2016`
{cite}`roche`).
- The reagents are generally more expensive than second-generation sequencing.
```

```{admonition} Comparison of sequencing technologies across generations
:class: note, dropdown

:::{table} Performance comparison of common sequencing techniques sorted for maximum read length. We obtained the numbers for Sanger sequencing from individual sources ([a](https://assets.thermofisher.com/TFS-Assets/GSD/brochures/sanger-sequencing-workflow-brochure.pdf), [b](https://www.sciencedirect.com/science/article/abs/pii/B9780128154991000132), [c](https://www.base4.co.uk/cost-comparison-of-dna-sequencing-technologies/#:~:text=$500%20per%20megabase.), [d](https://www.thermofisher.com/de/de/home/life-science/cloning/cloning-learning-center/invitrogen-school-of-molecular-biology/next-generation-sequencing/dna-sequencing-history.html#:~:text=Although%20DNA%20sequencers%20using%20Sanger,base%20pairs)), while all other methods were obtained from {cite:t}`logsdon2020long`.
:label: table
:align: center

| Name                                 | Max read length (kb) | Accuracy (%)  | Cost ($/Gb)     | Throughput (Mb/year) | Generation |
| ------------------------------------ | -------------------- | ------------- | --------------- | -------------------- | ---------- |
| Illumina NextSeq 550                 | 0.15                 | >99.9         | >47,782         | 50-63                | 2          |
| Illumina NovaSeq 6000                | 0.25                 | >99.9         | 10-35           | >1,194,545           | 2          |
| Sanger sequecing (e.g. ThermoFisher) | 1{sup}`b`            | 99.99{sup}`a` | 500,000{sup}`c` | 0.73{sup}`d`         | 1          |
| PacBio (Sequel II, HiFi)             | >20                  | >99           | 43–86           | 10,220               | 3          |
| PacBio (Sequel II, CLR)              | >200                 | 87–92         | 13-26           | 93,440               | 3          |
| Nanopore (PromethION)                | >1,000               | 87–98         | 21-42           | 3,153,600            | 3          |
| Nanopore (MinION/GridION)            | >1,500               | 87–98         | 50-2,000        | 913-109,500          | 3          |

:::

```

## Overview of the NGS process

Even though a variety of NGS technologies exist, the general steps to sequence DNA (and therefore reverse transcribed RNA) are largely the same.
The differences lie primarily in the chemistry of the respective sequencing technologies.

1. **Sample and library preparation**: As a first step, a so-called {term}`library` is prepared by fragmenting the DNA samples and ligating them with {term}`adapter molecules <Adapter sequences>`.
   These adapters participate in the hybridization of the library fragments to the matrix and form a priming site.

2. **Amplification and sequencing**: In the second step, the library gets converted into single-strand molecules.
   During an amplification step (such as a polymerase chain reaction), clusters of DNA molecules are created.
   All of the clusters perform individual reactions during a single sequencing run.

3. **Data output and analysis**: The output of a sequencing experiment depends on the sequencing technology and chemistry.
   Some sequencers generate fluorescence signals, which are stored in specific output files.
   Others may generate electric signals, which are stored in corresponding file formats.
   Generally, the amount of generated data, the raw data, is huge.
   Such data requires complex and computationally heavy processing.
   This is further discussed in the raw data processing chapter.

(introduction-scrna-seq-key-takeaway-3)=
(exp-data:rna-sequencing)=

## RNA sequencing

So far, we have only introduced sequencing with the unmentioned assumption that the DNA is being sequenced.
However, knowing the DNA sequence of an organism and the positions of its regulatory elements tells us very little about a cell's dynamic and real-time processes.
RNA sequencing (RNA-Seq) allows scientists to obtain snapshots of cells, tissues, or organisms at the time of sequencing in the form of expression profiles of genes.
This information can be used to detect changes in disease states in response to therapeutics, environmental factors, genotypes, and other experimental conditions.

RNA-Seq largely follows the DNA sequencing protocols but includes a reverse transcription step where {term}`complementary DNA (cDNA)` is synthesized from the RNA template.
Modern RNA sequencing allows for an unbiased sampling of transcripts in contrast to, for example, microarray-based assays or quantitative reverse transcription PCR, which require probe design to specifically target the regions of interest.
{ref}`Microarray-based assays <videos>` use probes, complementary sequences, to detect specific sequences (e.g. genes) of interest.
{ref}`Quantitative reverse transcription PCR <videos>` measures the amount of target RNA by monitoring the amplification of a complementary DNA (cDNA) molecule during PCR.

The obtained gene expression profiles further enable the detection of gene isoforms, gene fusions, single nucleotide variants, and many other interesting properties.
Modern RNA sequencing is not limited by prior knowledge and allows for the capture of both known and novel features.
This results in rich data sets that can be used for exploratory data analysis.

(introduction-scrna-seq-key-takeaway-2)=

## Single-cell RNA sequencing

### Bulk sequencing vs single-cell RNA sequencing

RNA-Seq can be mainly conducted in two ways: Either by sequencing the mixed RNA from the source of interest across cells ({term}`bulk sequencing <Bulk RNA sequencing>`) or by sequencing the transcriptomes of the cells individually (single-cell sequencing).
Mixing the RNA of all cells is, in most cases, cheaper and easier than experimentally complex single-cell RNA-Seq (scRNA-Seq)
Bulk RNA-Seq results in cell-averaged expression profiles, which are generally easier to analyze, but also hide some of the complexity, such as cell expression profile heterogeneity, which may help answer the question of interest.
Some drugs or perturbations may affect only specific {term}`cell types <Cell type>` or interactions between cell types.
For example, in oncology, it is possible to have rare drug-resistant tumor cells causing relapse, which is difficult to identify by simple bulk RNA-Seq, even on cultured cells.

To uncover such relationships, examining gene expression on a single-cell level is vital.
ScRNA-Seq does, however, come with several caveats.
First, single-cell experiments are generally more expensive and more difficult to properly conduct.
Second, the {term}`downstream analysis` becomes more complex due to the increased resolution, and it is easier to draw false conclusions.

A single-cell experiment generally follows similar steps as a bulk RNA-Seq experiment (see above) but requires several adaptations.
Like bulk sequencing, single-cell sequencing requires lysis, reverse transcription, amplification, and eventual sequencing.
In addition, single-cell sequencing requires cell isolation and a physical separation into smaller reaction chambers or another form of cell labeling to be able to map the obtained transcriptomes back to the cells of origin later on.
Hence, these are also the steps where most single-cell assays differ: single-cell isolation, transcript amplification, and sequencing, depending on the sequencing machine.
But before we can start explaining the intricacies of single-cell RNA sequencing, it’s essential to understand the biological and technical challenges that arise when measuring {term}`mRNA <Messenger RNA (mRNA)>` at such a fine resolution.

(introduction-scrna-seq-key-takeaway-4)=

### Central dogma in numbers

```{figure} ../_static/images/scrna_seq/central_dogma_in_numbers.png
:name: central-dogma-in-numbers
:alt: Central dogma in numbers figure
:with: 100%

The steps of the central dogma, supported by estimated values. These values are approximations intended to give a general impression and may vary depending on the context or in the future.
```

#### Measuring "messengers"

At the core of scRNA-Seq lies a fundamental question: What **exactly** are we trying to measure?
In RNA-seq experiments, our focus is on quantifying messenger RNA (mRNA) within individual cells.
This molecule is "an unstable intermediate that carries information from genes to ribosomes for protein synthesis" as Brenner, Jacob and Meselson described it in 1961 and thus coined the term "messenger" {cite}`brenner1961unstable`.
Therefore, mRNA serves as the crucial link between DNA and protein production — the very essence of the central dogma of molecular biology.
Yet, mRNA makes up only a small fraction of a cell’s total RNA.
Roughly 3–7% of RNA mass is mRNA, while the overwhelming majority is non-coding RNA: 80–90% ribosomal RNA (rRNA), 10–15% transfer RNA (tRNA), and ~1% other non-coding species {cite}`palazzo2015non` ([overview of none coding RNA](https://www.bio-rad.com/de-de/applications-technologies/coding-non-coding-rna?ID=Q1070M70KWE7)).
Estimates suggest there are between 100,000 to 1,000,000 mRNA molecules in a typical mammalian cell, covering up to ~50% of all genes {cite}`velculescu1999analysis, Islam2014`.
This means that a notable number of genes are not transcribed at all in any given cell — a reflection of the cell’s specific identity and function.
However, technical limitations in current scRNA-seq technologies further complicate measurement. For example, popular platforms like 10X Genomics capture only up to 65% of cells per run and recover just ~14% of each cell’s mRNA {cite}`aljanahi2018introduction`. These constraints make it especially challenging to detect weakly expressed genes.

Understanding the central dogma through these numerical lenses reveals not only the biological complexity but also the limitations of our tools. To appreciate this more deeply, let’s walk step by step from gene to protein.

#### From Gene to Protein

Our journey begins with a gene, a defined region in the DNA that acts as a template for mRNA synthesis.
While the number of genes can vary slightly between individuals (~70 genes), the average human genome contains roughly 22,000 genes {cite}`pertea2010between`.
Gene transcription is far from continuous.
Instead, it occurs in stochastic bursts — short, irregular periods of activity during which a gene might suddenly produce multiple mRNA transcripts before returning to silence {cite}`suter2011mammalian`.
This is also the reason why we model mRNA transcription with a negative binomial distribution.
This distribution is ideal because it models event counts (mRNA) while capturing overdispersion (variance exceeding the mean) caused by transcriptional bursts {cite}`ren2020negative,love2015deseq2`.

The initial RNA transcript, known as pre-mRNA, then undergoes alternative splicing, a process that allows different regions (called introns and exons) of the transcript to be joined in multiple ways.
This means that a single gene can give rise to multiple distinct mRNA isoforms.
On average, each human gene produces about 3.4 mRNA isoforms {cite}`lee2015mechanisms`.
While all human genes have at least two alternative isoforms, some push the limits of complexity.
The human basonuclin 2 gene, for instance, has the potential to generate up to 90,000 mRNA isoforms, resulting in over 2,000 different proteins {cite}`vanhoutteghem2007human`.
In some cases, however, alternative splicing could also lead to a non-functioning enzyme and an induced disease state.
Finally, this "mature" mRNA is translated into proteins.
Here, too, the numbers vary dramatically.
In mammels, the median protein-to-mRNA ratio is estimated to be around 10,000 proteins per mRNA {cite}`li2014system`.
However, this can range from just a few hundred to nearly a million proteins per transcript, depending on the gene, cell type and many other factors {cite}`edfors2016gene`.
Ultimately, this process results in approximately one billion proteins within a single human cell {cite}`milo2013total`.

Understanding these layers — from transcriptional bursts and alternative splicing to protein translation — highlights how the central dogma is not just a static pathway, but a dynamic and probabilistic system. Measuring it at single-cell resolution offers profound insights, but also reveals the challenges and limits of our current technologies.

(exp-data:transcript-quantification)=

### Transcript quantification

Transcript quantification is the process of converting the raw data into a table of estimated transcript counts per gene per sample (for bulk sequencing) or per cell (for single-cell sequencing).
More details on this computational process will be described in the next chapter.

There are two major approaches to transcript quantification: full-length and tag-based.
Full-length protocols try to cover the whole transcript uniformly with sequencing reads, whereas tag-based protocols only capture the 5' or 3' ends.
The transcript quantification method has strong implications on the captured genes, and analysts must therefore be aware of the used quantification process.
Full-length sequencing is restricted to plate-based protocols [(see below)](#plate-based), and the library preparation is comparable to bulk RNA-seq sequencing approaches.
An even coverage of transcripts is not always achieved with full-length protocols, and therefore specific regions across the gene body may still be biased.
A major advantage of full-length protocols is that they allow for the detection of splice variants.

Tag-based protocols only sequence either the transcripts' 3' or 5' end.
This comes at the cost of not (necessarily) covering the full gene length, making it difficult to unambiguously align reads to a transcript and distinguishing between different isoforms {cite}`Archer2016`.
However, it allows for the usage of unique molecular identifiers ({term}`UMIs <Unique Molecular Identifier (UMI)>`), which are useful to resolve biases in the transcript amplification process.

The transcript amplification process is a critical step in any RNA-seq sequencing run to ensure that the transcripts are abundant enough for quality control and sequencing.
During this process, which is typically conducted with polymerase chain reaction ({term}`PCR`), copies are made from identical fragments of the original molecule.
Since the copies and the original molecules are indistinguishable, determining the original number of molecules in samples becomes challenging.
UMIs are a common solution for quantifying original, non-duplicated molecules.

UMIs serve as molecular {term}`barcodes <barcode>` and are sometimes called random barcodes.
These ‘barcodes’ consist of short random nucleotide sequences that are added to every molecule in the sample as a unique tag.
UMIs must be added during library generation before the amplification step.
Accurately identifying PCR duplicates is important for downstream analysis to rule out - or be aware of {term}`amplification biases <amplification bias>` {cite}`Aird2011`.

Amplification bias is a term for the RNA/cDNA sequences that are preferentially amplified and will therefore be sequenced more often, resulting in higher counts.
It can harm any gene expression analysis because the not-very-active genes may suddenly appear to be highly expressed.
This is especially true for sequences that are amplified at a later stage of the PCR step, where the error rate may already be comparably higher than earlier PCR stages.
Although it is computationally possible to detect and remove such sequences by filtering out reads with identical alignment coordinates, it is generally advised to always design the experiment with UMIs, if possible.
Using UMIs further allows for normalizing gene counts without a loss of accuracy {cite}`Kivioja2012`.

(introduction-scrna-seq-key-takeaway-5)=

### Single-cell sequencing protocols

Numerous protocols exist for sequencing the transcriptomes of individual cells. However, the terminology can often be ambiguous, especially for those new to the field. To clarify, we categorize these techniques into two broad classes based on how cells are isolated:

- **Separation in droplets**: These methods encapsulate individual cells into tiny droplets within an emulsion, enabling high-throughput processing.
- **Separation in physical compartments**: These techniques isolate cells into distinct physical compartments, often referred to as wells.

Each approach differs in the ability to recover transcripts, the number of sequenced cells, and many other aspects.
In the following subsections, we will briefly discuss how they work, their strengths and weaknesses, and possible biases that data analysts should be aware of regarding the respective protocols.

#### Separation in Droplets

##### Most common protocols

The most widely used protocols are **inDrop** {cite}`Klein2015`, **Drop-seq** {cite}`exp:Macosko2015` and the commercially available **10x Genomics Chromium** {cite}`exp:Zheng2017`.
These protocols use microfluids to trap cells in tiny, watery bubbles known as droplets.
Each droplet forms a separate spaces containing only one cell and the required chemicals (beads).
The mentioned protocols can generate droplets thousands of times per second.
This massively parallel process generates very high numbers of droplets for a relatively low cost.

```{admonition} Droplets by vortexing
:class: dropdown, note
The PIP-seq protocol offers a simplified alternative to traditional microfluidic methods for generating monodispersed water-in-oil droplets.
Unlike complex microfluidic devices that require specialized equipment and expertise, PIP-seq achieves droplet formation through simple vortexing of the solution.
This method can be easily scaled by increasing the container volume without being constrained by emulsion time, a common limitation of microfluidics {cite}`clark2023microfluidics`.

However, despite its simplicity, independent {term}`benchmarks <benchmark>` indicate that PIP-seq still has limitations compared to well-established methods.
For instance, PIP-seq achieved approximately 1,500 gene counts, whereas the best 10x Genomics Chromium kit showed around 4,000 gene counts {cite}`de2025comprehensive`.
These findings highlight a trade-off between ease of use and performance in the current version of the PIP-seq protocol.
```

Although all three protocols differ in detail, nanoliter-sized droplets containing encapsulated cells are always designed to capture beads and cells simultaneously.
The encapsulation process is conducted with specialized microbeads with on-bead primers containing a PCR handle, a cell barcode, and a 4-8b base pairs-long UMI and a poly-T tail (or in the case of a 5' kit, there will be a poly-T primer).
Upon lysis, the cell's mRNA is instantaneously released and captured by the barcoded oligonucleotides that are attached to the beads.
Next, the droplets are collected and broken to release single-cell transcriptomes attached to microparticles (STAMPs).
This is followed by PCR and reverse transcription to capture and amplify the transcripts.
Finally, tagmentation takes place where the transcripts are randomly cut and sequencing adaptors get attached.
This process results in sequencing libraries that are ready for sequencing, as described above.
In droplet-based protocols, only about 10% of cell transcripts are recovered {cite}`Islam2014`.
Notably, this low sequencing is sufficient for a robust identification of cell types.

All three methods result in characteristic biases.
The material of the used beads differs between the protocols.
{term}`Drop-seq` uses brittle resin for the bead.
Therefore, the beads are encapsulated with a {term}`Poisson distribution`, whereas the {term}`InDrop` and 10X Genomics beads are deformable resulting in bead occupancies of over 80% {cite}`Zhang2019`.

Moreover, capture efficiency is likely influenced by the use of surface-tethered primers in Drop-Seq.
InDrop uses primers that are released with photocleavage, and 10X genomics dissolves the beads.
This disparity also affects the location of the reverse transcription process.
In Drop-seq, reverse transcription occurs after the beads are released from the droplets, while reverse transcription takes place inside the droplets for the InDrop and 10X genomics protocols {cite}`Zhang2019`.

A comparison from Zhang et al. in 2019 uncovered that inDrop and Drop-seq are outperformed by 10X Genomics with respect to bead quality, as the cell barcodes in the former two systems contained obvious mismatches.
Moreover, the proportion of reads originating from valid barcodes was 75% for 10X Genomics, compared to only 25% for InDrop and 30% for Drop-seq.

Similar advantages regarding sensitivity were demonstrated for 10X Genomics.
During their comparison, 10X Genomics captured about 17000 transcripts from 3000 genes on average, compared to 8000 transcripts from 2500 genes for Drop-seq and 2700 transcripts from 1250 genes for InDrop.
Technical noise was the lowest for 10X Genomics, followed by Drop-seq and InDrop {cite}`Zhang2019`.

The actual generated data demonstrated large protocol biases.
10X Genomics favored the capture and amplification of shorter genes and genes with higher GC content, while Drop-seq, in comparison, preferred genes with lower GC content.
Although 10X Genomics was shown to outperform the other protocols in various aspects, it is also about twice as expensive per cell.
Moreover, except the beads, Drop-seq is open-source and the protocol can more easily be adapted if required.
InDrop is completely open-source, where even the beads can be manufactured and modified in labs.
Hence, InDrop is the most flexible of the three protocols.

```{dropdown} <i class="fa-solid fa-thumbs-up"></i>   Strengths
- Allows for the cost-efficient sequencing of cells in large quantities to identify the overall composition of a tissue and characterize rare cell types.
- UMIs can be incorporated.
```

```{dropdown} <i class="fa-solid fa-thumbs-down"></i></i>   Limitations
- Low detection rates of transcripts compared to other methods.
- Captures only 3' ends (or 5' ends, depending on kit) and not full transcripts.
```

##### Nanopore sequencing meets droplet technology

Long-read single-cell sequencing approaches rarely use UMI {cite}`Singh2019` or do not perform UMI correction {cite}`Gupta2018` and therefore misassign some reads to novel UMIs.
Due to the higher sequencing error rate of long-read sequencers, this causes serious issues {cite}`Lebrigand2020`.
Lebrigand et al. introduced ScNaUmi-seq (Single-cell Nanopore sequencing with UMIs), combining Nanopore sequencing with cell barcode and UMI assignment.
The barcode assignment is guided with Illumina data by comparing the cell bar code sequences found in the Nanopore reads with those recovered from the Illumina reads for the same region or gene {cite}`Lebrigand2020`.
However, this effectively requires two single-cell libraries.
ScCOLOR-seq computationally identifies barcodes without errors using nucleotide pair complementary across the full length of the barcode.
These barcodes are then used as guides to correct the remaining erroneous barcodes {cite}`Philpott2021`.
A modified UMI-tools directional network-based method corrects for UMI sequence duplication.

```{dropdown} <i class="fa-solid fa-thumbs-up"></i>   Strengths
- Recovers splicing and sequence heterogeneity information
```

```{dropdown} <i class="fa-solid fa-thumbs-down"></i></i>   Limitations
- Nanopore reagents are expensive.
- High cell barcode recovery error rates.
- Depending on the protocol, barcode assignment is guided with Illumina data requiring two sequencing assays.
```

#### Separation in physical compartments

(plate-based)=

##### Plate-based protocols

Typically, plate-based protocols physically separate the cells into microwell plates.
The first step entails cell sorting by, for example, fluorescent-activated cell sorting (FACS), where cells are sorted according to specific cell surface markers; or by micro pipetting.
The selected cells are then placed into individual wells containing cell lysis buffers.
A reverse transcription is then carried out in these wells.
This allows several hundred cells to be analyzed in a single experiment with 5000 to 10000 captured genes each.

Plate-based sequencing protocols include but are not limited to, SMART-seq2, MARS-seq, QUARTZ-seq, and SRCB-seq.
Generally speaking, the protocols differ in their multiplexing ability.
For example, MARS-seq allows for three barcode levels, namely molecular, cellular, and plate-level tags, for robust multiplexing capabilities.
SMART-seq2, on the contrary, does not allow for early multiplexing, limiting cell numbers.
A systematic comparison of protocols by Mereu et al. in 2020 revealed that QUARTZ-seq2 can capture more genes than SMART-seq2, MARS-seq, or SRCB-seq per cell {cite}`Mereu2020`.
This means QUARTZ-seq2 can capture cell-type specific marker genes well, allowing for confident cell-type annotation.

```{dropdown} <i class="fa-solid fa-thumbs-up"></i>   Strengths
- Recovers many genes per cell, allowing for a deep characterization.
- It is possible to gather information before the library preparation, e.g., through FACS sorting to associate information such as cell size and the intensity of any used labels with good coordinates.
- Allows for full-length transcript recovery.
```

```{dropdown} <i class="fa-solid fa-thumbs-down"></i></i>   Limitations
- The scale of plate-based experiments is limited by the lower throughput of their individual processing units.
- Fragmentation step eliminates strand-specific information {cite}`Hrdlickova2017`.
- Depending on the protocol, plate-based protocols might be labor-intensive with many required pipetting steps, leading to potential technical noise and {term}`batch effects <batch effect>`.
```

##### Fluidigm C1

The commercial Fluidigm C1 system is a microfluidic chip that loads and separates cells into small reaction chambers in an automated manner.
The CEL-seq2 and SMART-seq (version 1) protocols use the Fluidigm C1 chips in their workflow, allowing the RNA extraction and library preparation steps to be conducted together, thereby decreasing the required manual labor.
However, the Fluidigm C1 requires rather homogeneous cell mixtures since the cells will reach different locations on the microfluidic chip based on their size, which could introduce potential location bias.
Full-length sequencing is possible since the amplification step is carried out in individual wells, effectively reducing the 3' bias of many other single-cell RNA-seq sequencing protocols.
The protocol is generally also more expensive and is therefore primarily useful for an extensive examination of a specific cell population.

```{dropdown} <i class="fa-solid fa-thumbs-up"></i>   Strengths
- Allows for full-length transcript coverage.
- Splicing variants and T/B cell receptor repertoire diversity can be recovered.
```

```{dropdown} <i class="fa-solid fa-thumbs-down"></i></i>   Limitations
- Only allows for the sequencing of up to 800 cells {cite}`fluidigm`.
- More expensive per cell than other protocols.
- Only about 10% of the extracted cells are captured, which makes this protocol unsuitable for rare cell types or low input.
- The used arrays only capture specific cell sizes, which may bias the captured transcripts.
```

#### Summary

In summary, we strongly recommend that wet lab and dry lab scientists select the sequencing protocol based on the aim of the study.
Is a deep characterization of a specific cell type population desired?
In this case, one of the plate-based methods may be more suitable.
On the contrary, droplet-based assays will capture heterogeneous mixtures better, allowing for a broader characterization of the sequenced cells.
Moreover, if the budget is a limiting factor, the protocol of choice should be more cost-effective and robust.
When analyzing the data, be aware of the sequencing assay-specific biases.
For an extensive comparison of all single-cell sequencing protocols, we recommend the "Benchmarking single-cell RNA-sequencing protocols for cell atlas projects" paper by Mereu et al. {cite}`Mereu2020`.

(introduction-scrna-seq-key-takeaway-5)=

### Single-cell vs single-nuclei

So far, we have only been discussing single-cell assays, but it is also possible to sequence only the nuclei of the cells.
Single-cell profiling does not always provide an unbiased view of cell types for specific tissues or organs, such as, for example, the brain.
During the tissue dissociation process, some cell types are more vulnerable and therefore difficult to capture. For example, fast-spiking parvalbumin-positive interneurons and subcortically projecting glutamatergic neurons were observed in lower proportions than expected in mouse neocortex {cite}`Tasic2018`.
On the contrary, non-neuronal cells survive dissociation better than neurons and are overrepresented in single-cell suspensions in the adult human neocortex {cite}`darmanis2015`.
Moreover, single-cell sequencing highly relies on fresh tissue, making it difficult to use tissue biobanks.

On the other hand, the nuclei are more resistant to mechanical force and can be safely isolated from frozen tissue without the use of tissue dissociation enzymes {cite}`Krishnaswami2016`.
Both options have varying applicability across tissues and sample types, and the resulting biases and uncertainties are still not fully uncovered.
It has been shown already that nuclei accurately reflect all transcriptional patterns of cells {cite}`Ding2020`.
The choice of single-cell versus single-nuclei in the experimental design is mostly driven by the type of tissue sample.
Data analysis, however, should be aware of the fact that dissociation ability will have a strong effect on the potentially observable cell types.
Therefore, we strongly encourage discussions between wet lab and dry lab scientists concerning the experimental design.

```{seealso}
:class: dropdown
To get a more elaborate understanding of the experimental assays, we recommend the following papers:

- Comparative Analysis of Single-Cell RNA Sequencing Methods {cite}`Ziegenhain2017`
- Power analysis of single-cell RNA-sequencing experiments {cite}`Svensson2017`
- Single-nucleus and single-cell transcriptomes compared in matched cortical cell types {cite}`Bakken2018`
- Guidelines for the experimental design of single-cell RNA sequencing studies {cite}`Lafzi2018`
- Benchmarking single-cell RNA-sequencing protocols for cell atlas projects {cite}`Mereu2020`
- Direct Comparative Analyses of 10X Genomics Chromium and Smart-seq2 {cite}`Wang2021`


(videos)=
Videos

TODO (link does not work)
[Microarray-based assays](https://www.youtube.com/watch?v=NgRfc6atXQ8)
[Quantitative reverse transcription PCR](https://www.youtube.com/watch?v=XH6vIBLwC2M)

```

### Questions

multiple_choice_question(
"q1",
"What is the primary purpose of scRNA-seq?",
[
"To sequence the genome of a single cell",
"To measure gene expression in individual cells",
"To capture DNA methylation patterns",
"To determine cell surface markers"
],
"To measure gene expression in individual cells",
)

multiple_choice_question(
"q2",
"What is reverse transcription in the context of scRNA-seq?",
[
"Converting cDNA to mRNA",
"Sequencing the DNA",
"Converting mRNA to cDNA",
"Labeling cell surface markers"
],
"Converting mRNA to cDNA",
)

multiple_choice_question(
"q3",
"What is the main difference between single-cell and single-nuclei sequencing?",
[
"Single-cell captures whole cells, while single-nuclei captures only nuclei",
"Single-nuclei sequencing has higher throughput",
"Single-cell is more accurate",
"Single-nuclei sequencing is cheaper"
],
"Single-cell captures whole cells, while single-nuclei captures only nuclei",
)

multiple_choice_question(
"q4",
"Which of the following best describes PIP-seq?",
[
"A protocol using microfluidics",
"A plate-based protocol",
"A simplified droplet-based method using vortexing",
"A long-read sequencing method"
],
"A simplified droplet-based method using vortexing",
)

flip_card("q5", "What are the two main categories we introduced for scRNA-seq protocols?", "Separation in droplets and separation in physical compartments.")

flip_card("q6", "What is the main advantage of droplet-based protocols?", "High throughput")

flip_card("q7", "What characterizes Second-Generation sequencing?", "High-throughput, short-read sequencing technologies, like Illumina and Ion Torrent.")

flip_card("q8", "What is the key advantage of Third-Generation sequencing?", "Long-read sequencing without amplification, as seen in Nanopore and PacBio.")

## References

```{bibliography}
:filter: docname in docnames
:labelprefix: exp
```

## Contributors

We gratefully acknowledge the contributions of:

### Authors

- Lukas Heumos
- Luis Heinzlmeier

### Reviewers

- Yuexin Chen
