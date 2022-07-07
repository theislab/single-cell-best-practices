(raw-proc)=
# Raw data processing

In this section, we discuss some of the fundamental issues that surround what is commonly called "pre-processing" of sc/snRNA-seq data. Though this is common terminology, it seems a bit of a misnomer, as this process involves several
steps that make important decisions about how to deal with and represent the data that can enable or preclude subsequent analyses. Here, we will primarily refer to this phase of processing as "raw data processing", and our focus will be on the phase of data analysis that begins with lane-demultiplexed `FASTQ` files, and ends with a count matrix representing the estimated number of distinct molecules arising from each gene within each quantified cell, potentially stratified by the inferred splicing status of each molecule.  

This count matrix then serves as the input for the myriad methods that have been developed for various analyses carried out with scRNA-seq data {cite}`Zappia2021`, from methods for normalization, integration, and filtering through methods for inferring cell types, developmental trajectories, and expression dynamics. Given that it serves as the starting point for all of these analyses, a robust and accurate estimation of this matrix is a foundational and critical step to support and enable accurate and reliable subsequent analyses. Fundamental misestimation in raw data processing can contribute to invalid inferences in higher-level analyses and can preclude discoveries based on the signal present in the raw data, which has been missed, diminished, or distorted by raw data processing. As we will see in this section, despite the intuitive nature of the input and output, we seek from this step in the processing pipeline several important and difficult challenges arise during raw data processing, and improved computational methodology for dealing with these challenges is still being actively developed. In particular, we will cover the fundamental steps in raw data processing, including read alignment/mapping, cell barcode (CB) identification, and correction, and the estimation of molecule counts through the resolution of unique molecular identifiers (UMIs), and will mention the choices and challenges that surface when performing these processing steps.

```{admonition} A note on what precedes raw data processing
The decision of where to begin discussing raw data processing is somewhat arbitrary. We note that while, here, we consider starting with lane-demultiplexed `FASTQ` files as the _raw_ input, even this already represents data that has been processed 
and transformed from raw measurements. Further, some of the processing that precedes the generation of the `FASTQ` files is relevant to challenges that may arise in subsequent processing. For example, the process of base calling and base quality estimation affects the errors that arise in the `FASTQ` representation of the sequenced fragments, as well as the instrument's estimation of the confidence of each called nucleotide. Further, issues can arise upstream of `FASTQ` generation, such as index hopping {cite}`farouni2020model`, though these issues can be largely mitigated both with _in silico_ approaches {cite}`farouni2020model` and through enhanced protocols such as [dual indexing](https://www.10xgenomics.com/blog/sequence-with-confidence-understand-index-hopping-and-how-to-resolve-it). In this section, however, we will not consider upstream effects such as these, and instead will consider the `FASTQ` files, derived from e.g. BCL files via [appropriate tools](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/bcl2fastq-direct) as the raw input under consideration. Once raw `FASTQ` files have been obtained, the quality of the reads themselves can be quickly diagnosed by running a quality control tool, for example [fastqc](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) to assess read quality, sequence content, etc.
```

(raw-proc:aln-map)=
## Alignment and Mapping

Mapping or alignment is a fundamental step in the single-cell raw data processing. It refers to the process of determining the potential loci of origin of each sequenced fragment (e.g., the set of genomic or transcriptomic loci that are similar to the read). Depending on the sequencing protocol, the resulting raw sequence file contains the cell-level information, commonly known as cell barcodes (CB), a unique molecule identifier (UMI), and the raw cDNA sequence (read sequence) generated from the molecule. As discussed in the previous section, the raw data processing of a single-cell sample can be divided into three steps: mapping the read sequence to targets of interest, identifying individual cells (demultiplexing and barcode correction), and resolving UMI sequences to obtain the final estimate of the number of molecules from each transcript/gene in each cell. Executing the first step accurately is instrumental for all downstream analyses since incorrect read-to-transcript/gene mapping can lead to wrong count matrices. 

While mapping read sequences to reference sequences _far_ predates the advent of single-cell RNA-sequencing, the current and quickly growing scale of scRNA-seq samples (typically hundreds of millions to billions of reads) makes this stage particularly computationally intensive. Additionally, using pre-existing RNA-seq aligners that are agnostic to any specific scRNA-seq protocol -- like the length and position of cell barcodes, UMI, etc. -- requires making use of separate tools for performing other steps such as demultiplexing and UMI resolutions{cite}`Smith2017`. This added overhead can be computationally cumbersome. Further, it typically carries a substantial disk space requirement for storing intermediate files
and the extra input and output operations required for processing such intermediate files further increase runtime requirements. 

To this end, several dedicated tools have been built specifically for aligning or mapping single-cell sequencing data, which handle these additional processing requirements automatically and internally. Tools such as `Cell Ranger` (commercial software from 10x Genomics){cite}`Zheng2017`, `zUMIs`{cite}`zumis`, `Alevin`{cite}`Srivastava2019`, `kallisto|bustools`{cite}`Melsted2021`, `STARsolo`{cite}`Kaminow2021` and `alevin-fry`{cite}`He2022` provide dedicated treatment for aligning scRNA-seq reads along with parsing of technical read content (CBs and UMIs), as well as methods for demultiplexing and UMI resolution. 
While all provide relatively simplified interfaces to the user, these tools use a variety of different approaches internally, with some generating traditional intermediate files (e.g., `BAM` files) and subsequently processing them, and others either working entirely in memory or making use of reduced intermediate representations to reduce the input/output burden.  

%A further benefit of all these tools is their reliance on pre-existing mapping/alignment engine that the tool relies on. As a result, the pre-existing user base and the tutorials make these tools more amenable to new users. 

While the specific algorithms, data structures, and time and space trade-offs made by different alignment and mapping approaches can vary greatly, we can roughly categorize existing approaches along two axes: 
- The type of mapping they perform and
- The type of reference sequence against which they map reads.

(raw-proc:types-of-mapping)=
### Types of mapping 

Here we consider three main types of mapping algorithms that are most commonly applied in the context of mapping sc/sn RNA-seq data: spliced-alignment, contiguous alignment, and variations of lightweight mapping.

First, let us draw a distinction here between alignment-based approaches and lightweight mapping-based approaches. Alignment approaches apply a range of different heuristics to determine the potential loci from which reads may arise and then subsequently score, at each putative locus, the best nucleotide-level alignment between the read and reference, typically using dynamic programming-based approaches. In addition to the alignment score, a backtrace of the actual alignment that yields this score may be obtained (such information is typically encoded as a `CIGAR` string within the `SAM` or `BAM` file that is output). Thus, at the cost of computing such scores, these alignment-based approaches know the quality of each potential mapping of a read, which they can then use to filter reads that align well to the reference from mappings that arise as the result of low complexity or "spurious" matches between the read and reference. Alignment-based approaches include both traditional "full-alignment" approaches, as implemented in tools such as `STAR`{cite}`dobin2013star` and `STARsolo`{cite}`Kaminow2021` as well as approaches like _selective-alignment_ implemented in `salmon`{cite}`Srivastava2020Alignment` and `alevin`{cite}`Srivastava2019`, which score mappings but omit the computation of the optimal alignment's backtrace.  

Second, alignment-based approaches can be further categorized into spliced-alignment and contiguous alignment approaches (currently, there are no lightweight-mapping approaches that perform spliced mapping). Spliced-alignment approaches are capable of aligning a sequence read over several distinct segments of a reference, allowing potentially large gaps between the regions of the reference that align well with the corresponding parts of the read. Such alignment approaches are typical when aligning RNA-seq reads to the genome since the alignment procedure must be able to align reads that span across one or more splice junctions of the transcript, where a sequence that is contiguous in the read may be separated by intron and exon subsequences in the reference. Spliced alignment is a challenging problem, particularly in cases where only a small region of the read spans a splicing junction, since very little informative sequence may be available to place the segment of the read that overhangs the splice junction by only a small amount. On the other hand, contiguous alignment seeks a contiguous substring of the reference that aligns well against the read. In such alignment problems, though small insertions and deletions may be allowed, large gaps such as those observed in spliced alignments are typically not tolerated. Contiguous alignment may seek to align the entire read end-to-end, or it may optionally allow "soft clipping" of one or both ends of the read, in which case a high-quality alignment is sought between a contiguous interval of the reference and an infix of the read.

Finally, we can draw a distinction between alignment-based methods and lightweight mapping methods, which include approaches such as pseudoalignment{cite}`Bray2016`, quasi-mapping{cite}`srivastava2016rapmap`, and pseudoalignment with structural constraints{cite}`He2022`. Such approaches generally achieve superior speed by avoiding nucleotide-level alignment between the read and reference sequences. Instead, they base the determination of the reported mapping loci of a read on a separate set of rules and heuristics that may look only at the set of matching k-mers or other types of exact matches and potentially their orientations and relative positions with respect to each other. This can lead to substantially increased speed and mapping throughput, but also precludes easily-interpretable score-based assessments of whether or not the matches between the read and reference constitute a good match capable of supporting a high-quality alignment.

(raw-proc:mapping-references)=
### Mapping against different reference sequences

While different choices can be made among the mapping algorithms themselves, different choices can _also_ be made about the reference against which the read is mapped. We consider three main categories of reference sequence against which a method might map:

- The full (likely annotated) reference genome
- The annotated transcriptome
- An augmented transcriptome

It is also worth noting that, currently, not all combinations of mapping algorithms and reference sequences are possible. For example, lightweight mapping-based algorithms do not currently exist that can perform spliced-mapping of reads against a reference genome.

(raw-proc:genome-mapping)=
#### Mapping to the full genome 

The first type of reference against which a method may map consists of the entire genome of the target organism, usually with the annotated transcripts considered during mapping. Tools like `zUMIs`{cite}`zumis`, `Cell Ranger`{cite}`Zheng2017` and `STARsolo`{cite}`Kaminow2021` take this approach.  Since many of the reads arise from spliced transcripts, such an approach also requires the use of a splice-aware alignment algorithm where the alignment for a read can be split across one or more splicing junctions. The main benefits of this approach are that reads arising from any location in the genome, not just from annotated transcripts, can be accounted for. Since these approaches require constructing a genome-wide index, there is the little marginal cost for reporting not only the reads the map to known spliced transcripts but also reads that overlap or align within introns, making the alignment cost when using such approaches very similar for both single-cell and single-nucleus data. A final benefit is that even reads residing outside of the annotated transcripts, exons, and introns can be accounted for by such methods, which can enable _post hoc_ augmentation of the set of quantified loci (e.g., as is done in {cite:t}`Pool2022` by adding expressed UTRs to transcript annotations in a sample-specific and data-driven manner) and potentially increase gene detection and quantification sensitivity.

On the other hand, the versatility of the strategy of performing spliced alignment against the full genome comes with certain trade-offs. First, the most commonly-used alignment tools that adopt this strategy in the single-cell space have substantial memory requirements. Most of these tools are based upon the STAR{cite}`dobin2013star` aligner due to its speed and versatility. Yet, for a human-scale genome, constructing and storing the index can require upwards of 32GB of memory. The use of a sparse suffix array can reduce the final index size by close to a factor of 2, but this comes at a reduction in alignment speed, and it still requires larger memory for the initial construction. Second, the increased difficulty of spliced alignment compared to contiguous alignment and the fact that current spliced alignment tools must explicitly compute a score for each read alignment means that this approach comes at an increased computational cost compared to the alternatives. Finally, such an approach requires the genome of the organism under study is available. While this is not problematic for the most commonly-studied reference organisms and is rarely an issue, it can affect the usability of such tools difficult for non-model organisms where only a transcriptome assembly may be available.

(raw-proc:txome-mapping)=
#### Mapping to the spliced transcriptome

To reduce the computational overhead of spliced-alignment to a genome, the widely-adopted alternative is to use just the sequences of the annotated transcripts themselves as a reference. Since the majority of single-cell experiments are generated from model organisms (such as mouse), which have well-annotated transcriptomes, such transcriptome-based quantification methods may provide similar read coverage to their genome-based counterparts. Compared to the genome, transcriptome sequences are much smaller in size, minimizing the computational resources required for running the mapping pipeline. Additionally, since the relevant splicing patterns are already represented in the transcript sequences themselves, this approach dispenses with the need to solve the difficult spliced-alignment problem. Instead, one can simply search for contiguous alignments or mappings for the read. Since only contiguous mappings need to be discovered, both alignment and lightweight mapping techniques are amenable to transcriptome references, and both approaches have been used in popular tools that adopt the spliced transcriptome as the target of reference mapping.

However, while such approaches can greatly reduce the memory and time required for alignment and mapping, they will fail to capture reads that arise from outside of the spliced transcriptome. Such an approach is therefore not adequate when processing single-nucleus data. Even in single-cell experiments, reads arising from outside of the spliced transcriptome can constitute a substantial fraction of all data, and there is growing evidence that such reads should be incorporated into subsequent analysis {cite}`technote_10x_intronic_reads,Pool2022`. Further, when paired with lightweight mapping approaches, short matches shared between the spliced transcriptome and the reference sequences that truly give rise to a read may lead to spurious read mappings, which, in turn, can lead to spurious and even biologically-implausible estimates of the expression of certain genes {cite}`Kaminow2021,Bruning2022Comparative,He2022`.

(raw-proc:aug-txome-mapping)=
#### Mapping to an augmented transcriptome

To deal with the fact that sequenced reads may arise from outside of spliced transcripts, it is possible to augment the spliced transcript sequences with other reference sequences that may be expected to give rise to reads (e.g., full-length unspliced transcripts or excised intronic sequences). Transcriptome references, when augmented with further sequences such as introns, allow reference indices typically smaller than those required for the full genome while simultaneously retaining the ability to search only for contiguous read alignments. This means they can potentially enable both faster and less memory-hungry alignment than when mapping against the full genome while still accounting for many of the reads that arise from outside of the spliced transcriptome. Finally, by mapping to an expanded collection of reference sequences, not only are the mapping locations of more reads recovered compared to mapping against just the spliced transcriptome, but when using lightweight mapping-based approaches, spurious mappings can be greatly reduced{cite}`He2022`. Such an expanded or augmented transcriptome is commonly used among approaches (those that do not map to the full genome) when they need to quantify single-nucleus data or prepare data for RNA-velocity analysis{cite}`Soneson2021Preprocessing`, therefore such augmented references can be constructed for all of the common methods that don't make use of spliced-alignment to the full genome{cite}`Srivastava2019,Melsted2021,He2022`. 

{cite:t}`He2022` argue that such an approach is valuable even when processing standard single-cell RNA-seq data and recommends constructing an augmented _splici_ (meaning spliced + intronic) reference for mapping and quantification. The _splici_ reference is constructed using the spliced transcriptome sequence along with the sequences containing the merged intervals corresponding to the introns of the annotated genes. Each reference is then labeled with its annotated splicing status, and the mapping to this reference is subsequently paired with splicing-status aware methods for [UMI resolution](raw-proc:umi-resolution). The main benefits of this approach are that it admits the use of lightweight mapping methods while substantially reducing the prevalence of spurious mappings. It enables the detection of reads of both spliced and unspliced origin which can increase the sensitivity of subsequent analysis{cite}`technote_10x_intronic_reads,Pool2022`, and, since splicing status is tracked during quantification and reported separately in the output, it unifies the processing pipeline for single-cell, single-nucleus, and RNA-velocity pre-processing.


(raw-proc:cb-correction)=
## Cell Barcode Correction
<!-- ## Intoduction to cell barcodes -->
Droplet-based single-cell segregation systems, such as those provided by 10x Genomics, have become an important tool for studying the cause and the consequences of cellular heterogeneity. In this segregation system, the RNA material of each captured cell is extracted within a water-based droplet encapsulation along with a barcoded bead. These beads tag the RNA content of individual cells with unique oligonucleotides, called cell barcodes (CBs), that are later sequenced along with the RNA. The beads contain high-diversity DNA barcodes enabling parallel barcoding of the cell's molecular content and _in silico_ demultiplexing of the RNA-seq reads into individual cellular bins.

### Type of errors in barcoding
The tag, sequence, and demultiplex method for single-cell profiling generally works well, but the number of observed cell barcodes (CBs) in a droplet-based library significantly exceeds the number of originally encapsulated cells by several fold. Several main sources of error can lead to such observation:

* Doublets / Multiplets: A single barcode can be associated with two or more cells
* Empty Droplet: A droplet can be captured with no encapsulated cell, and ambient RNA tagged with this barcode can be sequenced
* Sequence error: Errors can arise during PCR amplification or sequencing process

Computational tools for demultiplexing the RNA-seq reads into cell-specific bins use a wide range of diagnostic indicators to filter out artefactual or low-quality data. For example, numerous methods exist for the removal of ambient RNA contamination{cite}`Young2020,Muskovic2021,Lun2019`, doublet detection{cite}`DePasquale2019,McGinnis2019,Wolock2019,Bais2019` and cell barcodes correction for sequence errors based on nucleotide sequence similarity.

Several common strategies are used for cell barcode identification and correction.

* Correction against a known list of _potential_ barcodes: Certain chemistries, such as 10x Chromium, draw CBs from a known pool of potential barcode sequences. Thus, the set of barcodes observed in any sample is expected to be a subset of this known list, often called a "whitelist", "permit list", or "pass list". In this case, a common strategy is to assume each barcode that exactly matches some element from the known list is correct and for all other barcodes to be correct against the known list of barcodes (i.e., to find barcodes from the permit list that are some small Hamming distance or edit distance away from the observed barcodes). This approach leverages the known permit list to allow efficient correction of many barcodes that have been corrupted. However, one difficulty with this approach is that a given corrupted barcode may have multiple potential corrections in the permit list (i.e., its correction may be ambiguous). In fact, if one considers a barcode that is taken from the [10x Chromium V3 permit list](https://github.com/10XGenomics/cellranger/blob/master/lib/python/cellranger/barcodes/3M-february-2018.txt.gz) and mutated at a single position to a barcode, not in the list, there is a $\sim 81\%$ chance that it sits at Hamming distance 1 from 2 or more barcodes in the permit list. The probability of such collisions can be reduced by only considering correcting against barcodes from the known permit list, which, themselves, occur exactly in the given sample (or even only those that occur exactly in the given sample above some nominal frequency threshold). Also, information such as the base quality at the "corrected" position can be used to potentially break ties in the case of ambiguous corrections. Yet, as the number of assayed cells increases, insufficient sequence diversity in the set of potential cell barcodes increases the frequency of ambiguous corrections and reads tagged with barcodes having ambiguous corrections are most commonly discarded.

* Knee or elbow-based methods: If a set of potential barcodes is unknown — or even if it is known, but one wishes to correct directly from the observed data itself without consulting an external list — one can adopt a method based on the observation that the list of "true" or high-quality barcodes in a sample is likely those associated with the greatest number of reads.
To do this, one can construct the cumulative frequency plot of the barcodes, in which barcodes are sorted in descending order of the number of distinct reads or UMIs with which they are associated. Often, this ranked cumulative frequency plot will contain a "knee" or "elbow" – an inflection point that can be used to characterize frequently occurring barcodes from infrequent (and therefore likely erroneous) barcodes. Many methods exist for attempting to identify such an inflection point {cite}`Smith2017,Lun2019,He2022` as a likely point of discrimination between properly captured cells and empty droplets. Subsequently, the set of barcodes that appear "above" the knee can be treated as a permit list against which the rest of the barcodes may be corrected, as in the first method list above. Such an approach is flexible as it can be applied in chemistries that have an external permit list and those that don't. Further parameters of the knee-finding algorithms can be altered to yield more or less restrictive selected barcode sets. Yet, such an approach can have certain drawbacks, like a tendency to be overly conservative and sometimes failing to work robustly in samples where no clear knee is present.

* Filtering and correction based on an expected cell count provided by the user: These approaches seek to estimate a robust list of high-quality or present barcodes in the cases where the CB frequency distribution may not have a clear knee or may exhibit bimodality due to technical artifacts. In such an approach, the user provides an estimate of the expected number of assayed cells. Then, the barcodes are ordered by descending frequency, the frequency $f$ at a robust quantile index near the expected cell count is obtained, and all cells having a frequency within a small constant fraction of $f$ (e.g., $\ge \frac{f}{10}$) are considered as valid barcodes. Again, the remaining barcodes are corrected against this valid list by attempting to correct uniquely to one of these valid barcodes based on sequence similarity.

* Filtering based on a forced number of valid cells: Perhaps the simplest approach, although potentially problematic, is for the user to directly provide the index in the sorted frequency plot above which barcodes will be considered valid. All barcodes with a frequency greater than or equal to the frequency at the selected index are considered valid and treated as constituting the permit list. The remaining set of barcodes is then corrected against this list using the same approach described in the other methods above. If there are at least as many distinct barcodes as the number of cells the user requests, then this many cells will always be selected. Of course, such an approach is only reasonable when the user has a good reason to believe that the threshold frequency should be set around the provided index. 

%In the `alevin-fry` framework, the frequency of every observed cell barcode is generated, and there are four customizable options to select the high-quality cell barcodes for downstream analysis:

### Future challenges

While cellular barcoding of high-throughput single-cell profiling has been a tremendously successful approach, some challenges still remain, especially as the scale of experiments continues to grow. For example, the design of a robust method for selecting high-quality cell barcodes from the set of all the observations is still an active area of research, with distinct challenges arising, e.g., between single-cell and single-nucleus experiments. Also, as single-cell technologies have advanced to profile increasing numbers of cells, insufficient sequence diversity in the CB sequence can result in sequence corrections leading to CB collision. Addressing this latter problem may require more intelligent barcode design methods and continuing increases in the lengths of oligonucleotides used for cell barcoding.

(raw-proc:umi-resolution)=
## UMI resolution

After cell barcode (CB) correction, reads have either been discarded or assigned to a corrected CB. Subsequently, we wish to quantify the abundance of each gene within each corrected CB.

% **TODO**: add a label to section 2.5.4 (and any other referenced sections) and use cross-ref here.

Because of the amplification bias as discussed in <span style=" color:red ">Section 2.5.2</span>, reads must be deduplicated, based upon their UMI, to assess the true count of sampled molecules. Additionally, several other complicating factors present challenges when attempting to perform this estimation.

The UMI deduplication step aims to identify the set of reads and UMIs derived from each original, pre-PCR molecule in each cell captured and sequenced in the experiment. The result of this process is to allocate a molecule count to each gene in each cell, which is subsequently used in the downstream analysis as the raw expression estimate for this gene. We refer to this process of looking at the collection of observed UMIs and their associated mapped reads and attempting to infer the original number of observed molecules arising from each gene as the process of _UMI resolution_.

To simplify the explanation, in the following text, the reads that map to a reference, for example, a genomic locus of a gene, are called the reads of that reference, and their UMI tags are called the UMIs of that gene; the set of reads that are tagged by a UMI is called the reads of that UMI. A read can only be tagged by one UMI but can belong to multiple references if it maps to multiple references. Furthermore, as the molecule barcoding process for each cell in scRNA-seq is usually isolated and independent (apart from the issues related to accurately resolving cell barcodes raised earlier), without loss of generality, _UMI resolution_ will be explained for a specific cell. The same procedure will be applied to all cells independently.

(raw-proc:need-for-umi-resolution)=
### The need for UMI resolution

In the ideal case, where the correct (unaltered) UMI tags each read, the reads of each UMI uniquely map to a common reference gene, and there is a bijection between UMIs and pre-PCR molecules, the UMI deduplication procedure is conceptually straightforward: the reads of a UMI are the PCR duplicates from a single pre-PCR molecule. The number of captured and sequenced molecules of each gene in the cell is the number of distinct UMIs observed for this gene.

However, the problems encountered in practice make the simple rules described above insufficient for identifying the gene origin of UMIs in general and necessitate the development of more sophisticated models. Here, we concern ourselves primarily with two challenges.

* The first problem we discuss is errors in UMIs. These occur when the sequenced UMI tag of reads contains errors introduced during PCR or the sequencing process. Common UMI errors include nucleotide substitutions during PCR and read errors during sequencing. Failing to address such UMI errors can inflate the estimated number of molecules {cite}`Smith2017,ziegenhain2022molecular`.

* The second issue we discuss is multimapping, which arises in cases where a read or UMI belongs to multiple references, for example, multi-gene reads/UMIs. This happens if different reads of a UMI map to different genes, a read maps to multiple genes or both. The consequence of this issue is that the gene origin of the multi-gene reads/UMIs is ambiguous, which results in uncertainty about the sampled pre-PCR molecule count of those genes. Simply discarding multi-gene reads/UMIs can lead to a loss of data or a biased estimate among genes that tend to produce multimapping reads, such as sequence-similar gene families{cite}`Srivastava2019`.

There exist other challenges that we do not focus upon here, such as "convergent" and "divergent" UMI collisions. We consider the case where the same UMI is used to tag two different pre-PCR molecules arising from the same gene, in the same cell, as a convergent collision. When two or more distinct UMIs arise from the same pre-PCR molecule, e.g., due to the sampling of multiple priming sites from this molecule, we consider this a divergent collision. We expect convergent UMI collisions to be rare and, therefore, their effect typically small. Further, transcript-level mapping information can sometimes be used to resolve such collisions{cite}`Srivastava2019`. Divergent UMI collisions occur primarily among introns of unspliced transcripts{cite}`technote_10x_intronic_reads`, and approaches to addressing the issues they raise are an area of active research{cite}`technote_10x_intronic_reads,Gorin2021`.

% **TODO**: If needed, come up with a section name for the following two paragraphs.

UMI errors, especially those due to nucleotide substitutions and miscallings, are prevalent in single-cell experiments. {cite:t}`Smith2017` establish that the average number of bases different (edit distance) between the observed UMI sequences in the tested single-cell experiments is lower than randomly sampled UMI sequences, and the enrichment of low edit distances is well correlated with the degree of PCR amplification. Multimapping also exists in single-cell data and, depending upon the gene being considered, can occur at a non-trivial rate. {cite:t}`Srivastava2019` show that discarding the multimapping reads can negatively bias the predicted molecule counts.

Given that the use of UMIs is near ubiquitous in high-throughput scRNA-seq protocols and the fact that addressing these errors improves the estimation of gene abundances, there has been much attention paid to the problem of UMI resolution in recent literature {cite}`Islam2013,Bose2015,Macosko2015,Smith2017,Srivastava2019,Kaminow2021,Melsted2021,He2022,calib,umic,zumis`.

(raw-proc:graph-based-umi-resolution)=
### Graph-based UMI resolution

As a result of the problems that arise when attempting to resolve UMIs, many methods have been developed to address the problem of UMI resolution. While there are a host of different approaches for UMI resolution, we will focus on a framework for representing problem instances, modified from a framework initially proposed by {cite:t}`Smith2017`, that relies upon the notion of a _UMI graph_. Each connected component of this graph represents a sub-problem wherein certain subsets of UMIs are collapsed (i.e., resolved as evidence of the same pre-PCR molecule). Many popular UMI resolution approaches can be interpreted in this framework by simply modifying precisely how the graph is refined and how the collapse or resolution procedure carried out over this graph works. 

In the context of single-cell data, a UMI graph $G(V,E)$ is a directed graph with a node set $V$ and an edge set $E$. Each node $v_i \in V$ represents an equivalence class (EC) of reads, and the edge set $E$ encodes the relationship between the ECS. The equivalence relation $\sim_r$ defined on reads is based on their UMI and mapping information. We say reads $r_x$ and $r_y$ are equivalent, $r_x \sim_r r_y$, if and only if they have identical UMI tags and map to the same set of references. UMI resolution approaches may define a "reference" as a genomic locus{cite}`Smith2017`, transcript{cite}`Srivastava2019,He2022` or gene{cite}`Zheng2017,Kaminow2021`. Other UMI resolution approaches exist, for example, the reference-free model{cite}`umic` and the method of moments as used in {cite}`Melsted2021`, but they may not be easily represented in this framework and are not discussed in further detail here.

In the UMI graph framework, a UMI resolution approach can be divided into three major steps, each of which has different options that can be modularly composed by different approaches. The three steps are defining nodes, defining adjacency relationships, and resolving components. Additionally, these steps may sometimes be preceded (and/or followed) by filtering steps designed to discard or heuristically assign (by modifying the set of reference mappings reported) reads and UMIs exhibiting certain types of mapping ambiguity.

(raw-proc:umi-graph-node-def)=
#### Defining nodes

As described above, a node $v_i \in V$ is an equivalence class of reads. Therefore, $V$ can be defined based on the full or filtered set of mapped reads and their associated _uncorrected_ UMIs. All subsets of reads that satisfy the equivalence relation $\sim_r$ based on their reference sets and UMI tags are associated with the same vertex $v \in V$. An EC is a multi-gene EC if its UMI is a multi-gene UMI. Some approaches will avoid the creation of such ECs by filtering or heuristically assigning reads prior to node creation, while other approaches will retain and process these ambiguous vertices and attempt and resolve their gene origin via parsimony, probabilistic assignment, or based on a related rule or model {cite}`Srivastava2019,Kaminow2021,He2022`.

(raw-proc:umi-graph-edge-def)=
#### Defining adjacency relationship

After creating the node set $V$ of a UMI graph, the adjacency of nodes in $V$ is defined based on the distance, typically the Hamming or edit distance, between their UMI sequences and the content of their associated reference sets.

Here we define the following functions on the node $v_i \in V$:
* $u(v_i)$ is the UMI tag of $v_i$.
* $c(v_i) = |v_i|$ as the cardinality of $v_i$, i.e., the number of reads associated with $v_i$ that are equivalent under $\sim_r$.
* $m(v_i)$ is the reference set encoded in the the mapping information, for $v_i$.
* $D(v_i, v_j)$ is the distance between $u(v_i)$ and $u(v_j)$, where $v_j \in V$. 

Given these function definitions, any two nodes $v_i, v_j \in V$ will be incident with a bi-directed edge if and only if $m(v_i) \cap m(v_j) \ne \emptyset$ and $D(v_i,v_j) \le \theta$, where $\theta$ is a distance threshold and is often set as $\theta=1${cite}`Smith2017,Kaminow2021,Srivastava2019`. Additionally, the bi-directed edge might be replaced by a directed edge incident from $v_i$ to $v_j$ if $c(v_i) \ge 2c(v_j) -1$ or vice versa{cite}`Smith2017,Srivastava2019`. Though these edge definitions are among the most common, others are possible, so long as they are completely defined by the $u$, $c$, $m$ and $D$ functions. With $V$ and $E$ in hand, the UMI graph $G = (V,E)$ is now defined.

(raw-proc:umi-graph-resolution-def)=
#### Defining graph resolution

Given the defined UMI graph, many different resolution approaches may be applied. A resolution method may be as simple as finding the set of connected components, clustering the graph, greedily collapsing nodes or contracting edges{cite}`Smith2017`, or searching for a cover of the graph by structures following certain rules (e.g., monochromatic arboresences{cite}`Srivastava2019`) to reduce the graph. As a result, each node in the reduced UMI graph, or each element in the cover in the case that the graph is not modified dynamically, represents a pre-PCR molecule. The collapsed nodes or covering sets are regarded as the PCR duplicates of that molecule. 

Different rules for defining the adjacency relationship and different approaches for graph resolution itself can seek to preserve different properties and can define a wide variety of distinct overall UMI resolution approaches. Note that for the approaches that aim to probabilistically resolve the ambiguity caused by multimapping, the resolved UMI graph might contain multi-gene ECs, and their gene origin will be resolved in the following step.

(raw-proc:umi-graph-quantification)=
#### Quantification

The last step in UMI resolution is quantifying the abundance of each gene using the resolved UMI graph. For approaches that discard multi-gene ECs, the molecule count vector for the genes in this cell (or count vector for short) is generated by counting the number of ECs labeled with each gene. On the other hand, approaches that process, rather than discard, multi-gene ECs usually resolve the ambiguity by applying some statistical inference procedure. For example, {cite:t}`Srivastava2019` introduce an expectation-maximization (EM) approach for probabilistically assigning multi-gene UMIs, and related EM algorithms have also been introduced as optional steps in subsequent tools{cite}`Melsted2021,Kaminow2021,He2022`. In this model, the collapsed EC to gene assignments are latent variables, and the deduplicated molecule counts of each gene are the main parameters. Intuitively, evidence from gene-unique ECs will be used to help probabilistically apportion the multi-gene ECs. The EM algorithm seeks the parameters that together have the (locally) highest likelihood of generating the observed ECs.

Usually, the UMI resolution and quantification process described above will be performed separately for each cell, represented by a corrected CB, to create a complete count matrix for all genes in all cells. However, the relative paucity of per-cell information in high-throughput single-cell samples limits the evidence available when performing UMI resolution, which in turn limits the potential efficacy of model-based solutions like the statistical inference procedure described above.
Thus, further research here is certainly warranted. For example, {cite:t}`Srivastava2020-lf` introduced an approach that allows sharing information between transcriptionally-similar cells to improve the quantification result further.

(raw-proc:count-qc)=
## Count matrix quality control (QC)

Once a count matrix has been generated, it is important to perform a quality control (QC) assessment.
There are several distinct assessments that generally fall under the rubric of quality control.
Basic global metrics are often recorded and reported to help assess the overall quality of the sequencing measurement itself. These metrics consist of quantities such as the total fraction of mapped reads, the distribution of distinct UMIs observed per cell, the distribution of UMI deduplication rates, the distribution of detected genes per cell, etc. These and similar metrics are often recorded by the quantification tools themselves{cite}`Zheng2017,Kaminow2021,Melsted2021,He2022` since they arise naturally and can be computed during the process of read mapping, cell barcode correction, and UMI resolution. Likewise, there exist several tools to help organize and visualize these basic metrics, such as the [Loupe browser](https://support.10xgenomics.com/single-cell-gene-expression/software/visualization/latest/what-is-loupe-cell-browser), [alevinQC](https://github.com/csoneson/alevinQC), or a [kb_python report](https://github.com/pachterlab/kb_python), depending upon the quantification pipeline being used. Beyond these basic global metrics, at this stage of analysis, QC metrics are designed primarily to help determine which cells (barcodes) have been sequenced "successfully", and which exhibit artifacts that warrant filtering or correction.

One of the first QC steps is determining which cell barcodes correspond to "high-confidence" sequenced cells. It is common in droplet-based protocols{cite}`Macosko2015` that certain barcodes are associated with ambient RNA instead of the RNA of a captured cell. This happens when droplets fail to capture a cell. These empty droplets still tend to produce sequenced reads, though the characteristics of these reads look markedly different from those associated with barcodes corresponding to properly captured cells. Many approaches exist to assess whether a barcode likely corresponds to an empty droplet or not. One simple method is to examine the cumulative frequency plot of the barcodes, in which barcodes are sorted in descending order of the number of distinct UMIs with which they are associated. This plot often contains a "knee" that can be identified{cite}`Smith2017,He2022` as a likely point of discrimination between properly captured cells and empty droplets.
While this "knee" method is intuitive and can often estimate a reasonable threshold, it has several drawbacks. For example, not all cumulative histograms display an obvious knee, and it is notoriously difficult to design algorithms that can robustly and automatically detect such knees. Finally, the total UMI count associated with a barcode may not, alone, be the best signal to determine if the barcode was associated with an empty or damaged cell.

This led to the development of several tools specifically designed to detect empty or damaged droplets, or cells generally deemed to be of "low quality" {cite}`Lun2019,Heiser2021,Hippen2021,Muskovic2021,Alvarez2020,Young2020`. These tools incorporate a variety of different measures of cell quality, including the frequencies of distinct UMIs, the number of detected genes, and the fraction of mitochondrial RNA, and typically work by applying a statistical model to these features to classify high-quality cells from putative empty droplets or damaged cells. This means that cells can typically be scored, and a final filtering can be selected based on an estimated posterior probability that cells are not empty or compromised. While these models generally work well for single-cell RNA-seq data, one may have to apply several additional filters or heuristics to obtain robust filtering in single-nucleus RNA-seq data{cite}`Kaminow2021,He2022`, like those exposed in the [`empty_drops_cell_ranger`](https://github.com/MarioniLab/DropletUtils/blob/master/R/emptyDropsCellRanger.R) function of DropletUtils{cite}`Lun2019`.

In addition to determining which cell barcodes correspond to empty droplets or damaged cells, one may also wish to identify those cell barcodes that correspond to doublets or multiplets. When a given droplet captures two (doublets) or more (multiplets) cells, this can result in a skewed distribution for these cell barcodes in terms of quantities like the number of reads and UMIs they represent, as well as gene expression profiles they display. Many tools have also been developed to predict the doublet status of cell barcodes{cite}`DePasquale2019,McGinnis2019,Wolock2019,Bais2019,Bernstein2020`. Once detected, cells determined to likely be doublets can be removed or otherwise adjusted for in the subsequent analysis.

% **Should anything else go in this basic QC section?**

(raw-proc:output-representation)=
## Count data representation

As one completes initial raw data processing and quality control and moves on to subsequent analyses, it is important to acknowledge and remember that the cell-by-gene count matrix is, at best, an approximation of the sequenced molecules in the original sample. At several stages of the raw data processing pipeline, heuristics are applied, and simplifications are made to enable the generation of this count matrix. For example, read mapping is imperfect, as is cell barcode correction. The accurate resolution of UMIs is particularly challenging, and issues related to UMIs attached to multi-mapping reads are often ignored, as is the fact that multiple priming sites, particularly among unspliced molecules, can violate the one-molecule to one-UMI relationship that is often assumed.

In light of these challenges and the simplifications adopted to address them, there remains active research as to how best to represent the pre-processed data to downstream tools. For example, several quantification tools{cite}`Srivastava2019,Melsted2021,Kaminow2021,He2022` implement an *optional* EM algorithm, initially introduced in this context by {cite:t}`Srivastava2019`, that probabilistically apportions UMIs associated with reads that map to more than one gene. This, however, can result in non-integer count matrices that may be unexpected by certain downstream tools. Alternatively, one may choose to resolve UMIs to *gene groups* instead of individual genes, retaining the multi-mapping information in the pre-processed output (it is worth noting that a similar representation, but at the transcript level, has been used for over a decade as a succinct internal representation in bulk RNA-seq transcript quantification tools{cite}`Turro2011,Nicolae2011,Patro2014,Bray2016,Patro2017,Ju2017`, and such a transcript-level representation has even been proposed for use in the clustering and dimensionality reduction of full-length single-cell RNA-seq data{cite}`Ntranos2016` and differential expression analysis of single-cell RNA-seq data{cite}`Ntranos2019`). In this case, instead of the resulting count matrix having dimensions $C \times G$, where $G$ is the number of genes in the quantified annotation, it will have dimension $C \times E$ where $E$ is the number of distinct *gene groups* (commonly called equivalence class labels) across all cells in the given sample. By propagating this information to the output count matrix, one can avoid the application of heuristic or probabilistic UMI resolution methods that can result in loss of data, or bias, in the counts used in downstream analysis. Of course, to make use of this information, downstream analyses must expect the information in this format. Further, those downstream methods must typically have a way to resolve these counts, eventually, to the level of genes, as the abundance of *gene groups* lacks the intuitive biological interpretability of gene abundance. Nonetheless, the benefits provided by such representations, in terms of conveying more complete and accurate information to downstream analysis tools, can be substantial, and tools taking advantage of such representations are being developed (e.g. [DifferentialRegulation](https://github.com/SimoneTiberi/DifferentialRegulation)); this is still an active area of research.

(raw-proc:example-workflow)=
## A real world example

Given that we have now covered the concepts underlying approaches for raw data processing, we now turn our attention to demonstrating how a specific tool (in this case, `alevin-fry`) can be used to process a small example dataset. To start, we need the sequenced read records in [`FASTQ` format](https://en.wikipedia.org/wiki/FASTQ_format) and the reference of the sample against which the reads will be mapped. Usually, a reference includes the genome sequences and the corresponding gene annotations of the sequenced species in the [FASTA](https://en.wikipedia.org/wiki/FASTA_format) and [GTF](https://useast.ensembl.org/info/website/upload/gff.html) format, respectively. 

In this example, we will use _chromosome 5_ of the human genome and its related gene annotations as the reference, which is a subset of the [Human reference, GRCh38 (GENCODE v32/Ensembl 98) reference](https://support.10xgenomics.com/single-cell-gene-expression/software/release-notes/build#GRCh38_2020A) from the 10x Genomics. Correspondingly, we extract the subset of reads that map to the generated reference from a [human brain tumor dataset](https://www.10xgenomics.com/resources/datasets/200-sorted-cells-from-human-glioblastoma-multiforme-3-lt-v-3-1-3-1-low-6-0-0) from the 10x Genomics. 

[`Alevin-fry`](https://alevin-fry.readthedocs.io/en/latest/){cite}`He2022` is a fast, accurate, and memory-frugal single-cell data processing tool. Here we show how to process the example dataset described above using `alevin-fry` from the command line. While simplified [wrapper scripts](https://github.com/COMBINE-lab/usefulaf) and [workflows](https://github.com/COMBINE-lab/quantaf) exist to process data with this tool, we will describe here the full set of commands to outline 
where the steps described in this section occur and to convey what different processing options are possible. These commands will be run from the command line, and [`conda`](https://docs.conda.io/en/latest/) will be used for installing all of the software required for running this example.

(raw-proc:example-prep)=
### Preparation

Before we start, we create a conda environment in the terminal and install the required packages. In this procedure, we will install [`alevin-fry`](https://alevin-fry.readthedocs.io/en/latest/), [`salmon`](https://salmon.readthedocs.io/en/latest/) and [`pyroe`](https://github.com/COMBINE-lab/pyroe).

"`bash
conda create -n af_xmpl -y -c bioconda python=3.9 salmon alevin-fry pyroe
conda activate af_xmpl
```

"`{admonition} Note on using an M1/M2-based device

Conda does not currently build most packages natively for Apple silicon. Therefore, if you 
are using a non-Intel-based Apple computer (e.g., with an M1(Pro/Max/Ultra) or M2 chip), you 
should make sure to specify that your environment uses the Rosetta2 translation layer.  
To do this, you can replace the above commands with the following (instructions adopted 
from [here](https://github.com/Haydnspass/miniforge#rosetta-on-mac-with-apple-silicon-hardware)):

"`bash
CONDA_SUBDIR=osx-64 conda create -n af_xmpl -y -c bioconda python=3.9 salmon alevin-fry pyroe   # create a new environment
conda activate af_xmpl
conda env config vars set CONDA_SUBDIR=osx-64  # subsequent commands use intel packages
```

Next, we create a working directory `af_xmpl_run`, and download and uncompress the example dataset from a remote host.

```bash
# create a working dir 
mkdir af_xmpl_run && cd af_xmpl_run

# download the example dataset
wget -qO- https://umd.box.com/shared/static/lx2xownlrhz3us8496tyu9c4dgade814.gz | tar xzf - --strip-components=1 -C .

# download CB permit list 
wget https://raw.githubusercontent.com/10XGenomics/cellranger/master/lib/python/cellranger/barcodes/3M-february-2018.txt.gz && gunzip 3M-february-2018.txt.gz

```

(raw-proc:example-map)=
### Mapping the data

Now, we process the data to obtain the mapping information. This includes three steps:
1. Build the _splici_ reference (<u>splic</u>ed transcripts + <u>i</u>ntrons), using the genome and gene annotation file.
2. Index the _splici_ reference.
3. Map the reads against the _splici_ index.

```bash
# making splici reference
# pyroe make-splici genome_file gtf_file read_length out_dir
pyroe make-splici \
toy_human_ref/fasta/genome.fa \
toy_human_ref/genes/genes.gtf \
90 \
splici_ref

# Indexing the reference
# salmon index -t extend_txome.fa -i idx_out_dir -p num_threads
salmon index \
-t $(ls splici_ref/*.fa) \
-i splici_idx \
-p 8 

# collecting reads files
fastq_dir="toy_read_fastq"
reads1_pat="_R1_"
reads2_pat="_R2_"
reads1="$(find -L $fastq_dir -name "*$reads1_pat*" -type f | xargs | sort | awk '{print $0}')"
reads2="$(find -L $fastq_dir -name "*$reads2_pat*" -type f | xargs | sort | awk '{print $0}')"

# Mapping
# salmon alevin -i idx_out_dir -l library_type -1 reads1_files -2 reads2_files -p num_threads -o map_out_dir
salmon alevin \
-i splici_idx \
-l ISR \
-1 ${reads1} \
-2 ${reads2} \
-p 8 \
-o alevin_map \
--chromiumV3 \
--sketch
```

This will produce an output folder called `alevin_map` that contains all the information we need to process the mapped reads using `alevin-fry`. 

(raw-proc:example-quant)=
### Processing the mapped reads

Next, we run the cell barcode correction, UMI resolution, and quantification steps described previously using `alevin-fry`. This procedure involves three `alevin-fry` commands:

1. The `generate-permit-list` command is used for cell barcode correction.
2. The `collate` command filters out invalid mapping records, corrects cell barcodes, and collates mapping records originating from the same cell.
3. The `quant` command performs UMI resolution and quantification.

```bash
# cell barcode correction
# alevin-fry generate-permit-list -u CB_permit_list -d expected_orientation -o gpl_out_dir 
alevin-fry generate-permit-list \
-u 3M-february-2018.txt \
-d fw \
-i alevin_map \
-o gpl
 
# filtering mapping information
# alevin-fry collate -i gpl_out_dir -r alevin_map_dir -t num_threads
alevin-fry collate \
-i gpl \
-r alevin_map \
-t 8

# UMI resolution + quantification
# alevin-fry quant -r resolution -m txp_to_gene_mapping -i gpl_out_dir -o quant_out_dir -t num_threads
alevin-fry quant -r cr-like \
-m $(ls splici_ref/*3col.tsv) \
-i gpl \
-o quant \
-t 8
```

After running these commands, the resulting quantification information can be found in `quant/alevin`. Within this directory, there are three files: `quants_mat.mtx`, `quants_mat_cols.txt`, and `quants_mat_rows.txt`, which correspond, respectively, to the count matrix, the gene names for each column of this matrix, and the corrected, filtered cell barcodes for each row of this matrix. Of note here is the fact that `alevin-fry` was run in USA-mode, and so quantification was performed for both the spliced and unspliced status of each gene — the resulting `quants_mat_cols.txt` fill will then have a number of rows equal to 3 times the number of annotated genes which correspond, to the names used for the spliced, unspliced, and splicing-ambiguous variants of each gene. Other relevant information concerning the mapping, CB correction, and UMI resolution steps can be found in the `alevin_map`, `gpl`, and `quant` folders, respectively.

% TODO: cross ref to the chapter for AnnData
We can load the count matrix into python as an [`AnnData`](https://anndata.readthedocs.io/en/latest/) object using the `load_fry` function from [`pyroe`](https://github.com/COMBINE-lab/pyroe). A similar function has been implemented in the [`roe`](https://github.com/COMBINE-lab/roe) R package.

"`python
import pyroe

quant_dir = 'quant'
anndata = pyroe.load_fry(quant_dir)
```

The default behavior loads the `X` layer of the `anndata` object as the sum of the spliced and ambiguous counts for each gene. However, recent work{cite}`Pool2022` and [updated practices](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/release-notes) suggest that the inclusion of intronic counts, even in single-cell RNA-seq data, may increase sensitivity and benefit downstream analysis. While the best way to make use of this information is the subject of ongoing research since `alevin-fry` automatically quantifies spliced, unspliced, and ambiguous reads in each sample, the count matrix containing the total counts for each gene can be simply obtained as follows:

"`python
import pyroe

quant_dir = 'quant'
anndata = pyroe.load_fry(quant_dir, output_format={'X' : ['U','S','A']})
```

In the example given here, we demonstrate using `alevin-fry` to process a 10x Chromium 3' v3 dataset. `Alevin-fry` provides many other options for processing different single-cell protocols, including but not limited to Dropseq{cite}`Macosko2015`, sci-RNA-seq3{cite}`Cao2019` and other 10x Chromium platforms. A more comprehensive list and description of available options for different stages of processing can be found in the [`alevin-fry` documentation](https://alevin-fry.readthedocs.io/en/latest/). `alevin-fry` also provides a [nextflow](https://www.nextflow.io/docs/latest/)-based workflow, called [quantaf](https://github.com/COMBINE-lab/quantaf), for conveniently processing many samples from a simply-defined sample sheet.

Of course, similar resources exist for many of the other raw data processing tools referenced and described throughout this section, including [`zUMIs`](https://github.com/sdparekh/zUMIs/wiki){cite}`zumis`, [`alevin`](https://salmon.readthedocs.io/en/latest/alevin.html){cite}`Srivastava2019`, [`kallisto|bustools`](https://www.kallistobus.tools/){cite}`Melsted2021`, [`STARsolo`](https://github.com/alexdobin/STAR/blob/master/docs/STARsolo.md){cite}`Kaminow2021` and [`CellRanger`](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/what-is-cell-ranger). The [`scrnaseq`](https://nf-co.re/scrnaseq) pipeline from [`nf-core`](https://nf-co.re/) also provides a nextflow-based pipeline for processing single-cell RNA-seq data generated using a range of different chemistries, and integrates several of the tools described in this section. 

(raw-proc:useful-links)=
## Useful links

[Alevin-fry tutorials](https://combine-lab.github.io/alevin-fry-tutorials/) provide tutorials for processing different types of data. 

[`quantaf`](https://github.com/COMBINE-lab/quantaf) is a nextflow-based workflow of the `alevin-fry` pipeline for conveniently processing single-cell data based on the input sheets. The pre-processed quantification information of publicly available single-cell datasets are available on its [webpage](https://combine-lab.github.io/quantaf).

[`pyroe`](https://github.com/COMBINE-lab/pyroe) in python and [`roe`](https://github.com/COMBINE-lab/roe) in R provide helper functions for processing `alevin-fry` quantification information. They also provide an interface to the pre-processed datasets in [`quantaf`](https://combine-lab.github.io/quantaf).

Tutorials for processing scRNA-seq raw data from [the galaxy project](https://galaxyproject.org/) can be found at [here](https://training.galaxyproject.org/training-material/topics/transcriptomics/tutorials/scrna-preprocessing-tenx/tutorial.html) and [here](https://training.galaxyproject.org/training-material/topics/transcriptomics/tutorials/scrna-preprocessing/tutorial.html).

(raw-proc:references)=
## References

```{bibliography}
:filter: docname in docnames
```




%## From BCF to `FASTQ`
%
%## Read QC
%`FASTQ'C and others
%
%## Alignment
%
% Hirak's section goes here
%
%## Collecting results with Multiqc
%Might not be a section, but noteworthy
%
%## Pipelines
%
%alevin
%alevin-fry
%cell ranger
%kallisto|bustools
%STARsolo
%zUMIs
%nf-core 