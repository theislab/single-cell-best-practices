# Mapping targeted in situ technologies to genome-scale expression maps

Unlike spot-based spatial transcriptomics, targeted in situ technologies (such as MERFISH, smFISH, or seqFISH+) are not limited in their spatial resolution but gene throughput, typically limited to a few hundreds of preselected genes. As a consequence, we face the orthogonal problem of increasing resolution with respect to genes instead of increasing spatial resolution and identifying cellular features. 

A method that is widely applicable in the context of aligning spatial profiling measurements with common sc/snRNA-seq profiles is Tangram. While Tangram can also be applied in the previously described deconvolution context, we focus on its ability to map MERFISH data to whole genome expression profiles. The underlying idea of Tangram is the probabilistic alignment of two different technologies by means of a single shared modality, typically RNA-seq data. This way, limitation with respect to the number of genes that are measured or spatial resolution can be overcome. 

The mapping algorithm of Tangram builds on count matrices from the two technologies at hand. For sc/snRNa-seq data, this means to compute the matrix $S$ whose entry $S_{ik}$ indicates the expression level for cell $i$ and gene $k$: 
$$
S \in \mathbb{R}_+^{n_{\text{cells}}\times n_{\text{genes}}} \ \ \text{ with } \ \ S_{ik}>0 \quad . 
$$
The same procedure applies to spatial data. We build the matrix $G$ according to: 
$$
G \in \mathbb{R}_+^{n_{\text{voxels}}\times n_{\text{genes}}} \ \ \text{ with } \ \ G_{jk}>0
$$

For MERFISH data, a voxel means the aggregation of single gene measurements to individual cells while a voxels refers to the individual spots for Visium. Note that the specific order in the voxel dimension is arbitrary and that $n_genes$ corresponds to the shared subset of genes present in both technologies. 

<!-- I am not sure what the density for MERFISH would look like, all ones maybe? -->
Tangram makes further use of a voxel density vector $\textbf d$. This density corresponds to estimated cell densities which, for example, can be deduced from an image segmentation in the case of Visium data. Formally, we write: 

$$
\textbf{d} \in \mathbb{R}^{n_\text{voxels}} \ \ \text{ with } \ \ d_j \in [0,1]  \ \ \text{ and } \ \ \sum_j d_j = 1 \quad .
$$  

Given the matrices $S$ and $G$ as well as the density $\textbf d$, Tangram aims to learn a thrid matrix $M$ that expresses the probability $M_{ij} \in [0,1]$ that cell $i$ belongs to voxel $j$. Being probabilitistic, every cells has to be mapped exactly once, that is the rows of $M$ have to be normalised: 

$$
M \in \mathbb{R}^{n_{\text{cells}}\times n_{\text{voxels}}}_+ \ \ \text{ with } \ \ \sum_{j}^{n_\text{voxel}} M_{ij}=1 \quad . 
$$

Note that the sum across cells indicates the number of cells that are assigned to a voxel $j$. Knowing about the number of cells in $S$, we can estimate the voxel density as 
$$
m_j = \sum_{i}^{n_\text{cells}} \frac{M_{ij}}{n_\text{cells}} \quad . 
$$

Putting all parts together, we arrive at the objective function of Tangram: 
$$
L = \mathbb{KL}[\mathbf m, \mathbf d] - \sum_{k}^{n_\text{genes}} d_{\cos}(M^TS_{:k}, G_{:k}) - \sum_{j}^{n_\text{voxels}} d_{\cos}(M^TS_{j:}, G_{j:}) \quad , 
$$
where $M^TS$ is the predicted spatial gene expression, $\mathbb{KL}$ the Kullback-Leibler divergence and $d_{\cos}$ the cosine similarity. The first term matches the predicted voxel density $\textbf m$ with the estimated one $\textbf d$. The second term ensures that for each gene $k$ the predicted profile matches the expected profile from $G$. The third term serves the same purpose for each individual voxel: the predicted voxel expression should be close to the expected one from $G$. 

<!-- For MERFISH we have to use the filtered approach, maybe to cumbersome to introduce it? -->
In order to infer genome-scale expression maps for MERFISH data, we first identify the shared gene set which should result in about $\sim 200$ genes. Second, we compute the $S$ and $G$ matrices from the sc/scRNA-seq reference and the spatial assay, respectively. For MERFISH, the voxel density has uniform entries $1/n_{\text{voxels}}$ as the voxels correspond to cells themselve. Given this, we only have to optimise the obective $L$ and obtain the probabilistic mapping $M$. 

To infer the spatial expression for the whole genome $f_j$ for voxel $j$, one can either compute a weighted sum using the probabilistic cell assignments $f_j = \sum_i M_{ij} c_i$, where $c_i \in \mathbb{R}_+^{n'_\text{genes}}$ is the genome-wide expression profile from sc/snRNA-seq, or first compute a deterministic mapping via $i^*(j) = \argmax_i M_{ij}$ and then build the genome-scale profile as $f_j = c_{i^*(j)}$ . 