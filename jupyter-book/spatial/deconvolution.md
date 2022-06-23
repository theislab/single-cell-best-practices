# Deconvolution methods
In spatial transciptomics, the observed transcriptome can be described as a latent variable model. The observed counts $x_{sg}$ for gene $g$ and spot $s$ is the sum of the cell's contributions $x_{sig}$ that belong to this spot:
$$
    x_{sg} = \sum_{i=1}^{C(s)} x_{sig}
$$

If one ignores the variability within cell types, the problem of deconvolution simplifies to the identification of cell type counts, that is to infer how often a cell type occures $\tilde \beta_{st}$ in each spot:
$$
    x_{sg} = \sum_{i=1}^{C(s)} c_{t(i)g} = \sum_{t=1}^{T} \beta_{st} c_{tg} ,
$$

where $t(i)$ is cell's $i$ cell type and $c_{tg}$ the prototype expression profiles. Note that the sum changes from summing over individual cells $i$ to summing over the disctinct set of cell types $t$. The parameter $\tilde \beta_{st}$ simply counts how often a cell type occures in a spot. Through normalisation of the spot's library size $l_s$, this count vector can be changed to indicate cell type proportions:
$$
    x_{sg} = l_s \sum_{t=1}^{T} \beta_{st} c_{tg}
$$

This problem of identifying cell type proportions $\beta_{st}$ is not easy to solve. One reason for this is limited number of spots within a dataset, usually 3-5k, spots while essaying all 20000 protein encoding genes of the human genome.

A good way to alleviate this issue is to use reference scRNA-seq measurements and use these to compute the prototype expression profile $\boldsymbol{c}_{t}$. If these are known, the problem reduces to finding the cell type proportions within a spot. Of course such a transfer across technologies is only sensible if one can assume that the scRNA-seq profiles are representable for the measures counts in the spatial assay. Ideally, both experiments were conducted on the same tissue slice. 

Over the past two years, multiple methods were introduced that tackle the problem of deconvolution in spatial transcriptomics data. Among others, there are Setreoscope, DestVI, RCTD, SPOTlight, and Cell2Location which we will describe in more detail for exemplary purposes.

## Stereoscope

Stereoscope is a reference deconvolution model, which uses the negative binomial distribution (\ref{nbdist}) for model both single cell and spatial transcriptomics expression data. \\

It makes the simplifying assumption, that gene expression of cells of one cell type is constant, not just within one spot but globally in the entire dataset:
$$
    c_{tsg} = c_{ts'g} \quad  \forall s,s' \in \{1, ..., N_s\}
$$

Stereoscope uses the above formulation as the rate parameter of a negative binomial distribution and extends it by two additional parameters. First, in order to model the technology dependent capture efficiencies of different genes, they introduce the capture efficiency parameter $e_g$. In addition, they introduce the second parameter of the negative binomial distribution, the success probability $p_g$. This parameter is considered to be shared between genes (this ensures that the $NB$ distribution is closed under summation):
$$
    x_{sg} \sim NB(l_s e_g \sum_{t=1}^{T} \beta_{st} c_{tg}, p_g)
$$

The expression profiles $c_{tg}$ as well as the success probabilities $p_g$ are obtained from the cell expressions $y_{ig}$ of a reference dataset: 
$$
    y_{ig} \sim NB(d_i c_{tg},p_g)
$$

where $d_c = \sum_{g = 1}^G y_{ig}$ is the count depth, i.e. the total number of a cell's transcripts.

As a technical adjustment, a dummy cell type is considered for each spot to model additive shifts between technologies due to differences in the underlying cell types:
$$
    x_{sg} \sim NB(l_s e_g \sum_{t=1}^{T} \beta_{st} c_{tg} + \kappa_s \epsilon_g, p_g)
$$

## Cell2location

Another deconvolution model which uses the negative binomial distribution is Cell2Location. In contrast to Stereoscope it uses the mean parameterisation of the negative binomial. The cell counts for each cell type are modeled directly via the mean $\mu_{sg}$ and the dispersion $a_g$, which, similar to Stereoscope, is also shared between genes. Additionally, technical parameters $l_s$, $e_g$ and $\epsilon_g$ are used as in stereoscope to account for multiplicative and additive shift:
$$
    x_{sg} \sim {NB}(\mu_{sg}, a_g) \\ =  {NB}(l_s (e_g \sum_{t=1}^{T} \beta_{st} c_{stg} + \epsilon_g), a_g)
$$

Note that cell2location also considers batch and technology effects from using data collected over multiple batches. In order to make the comparison between the models shown easier, this will not be considered here.

Cell2location makes extensive use of priors, to regularize parameters and attempt to match them closely to their biological meaning. All parameters of the spatial and reference model have priors of some form. These are most often constructed in a hierarchical fashion, that is the parameters of the prior distributions have themselves priors. Details can be found in the supplementary information of \cite{cell2location}.

One particularly interesting modeling assumption is to consider the abundance of cell types $\beta_{st}$ itself as a linear combination of contributions from cell type combination prototypes $\rho_{r}$ or tissue prototypes. These are modeled to be distributed on the slide with proportion $\pi_s$. All this is wrapped in a gamma prior with (fixed) prior strength parameter $v$:
$$
    \beta_{st} \sim \text{Gamma}((\mu_{sf} v , v)) \\
     = \text{Gamma}((\sum_{r=1}^R \pi_{sf} \rho_{fr} v , v))
$$
As a reference-based model, Cell2location also relies on scRNA-seq measurements for the cell type profiles $\boldsymbol{c}_t$. The single-cell model is quite similar to the one of Stereoscope but is mean-parametrised and further includes the technical parameter $\hat{\epsilon}_g$:
$$
    y_{cg} \sim {NB}(\mu_{cg}, \hat{a}_g)\\
    =  {NB}(\beta_{tg} + \hat{\epsilon}_g , \hat{a}_g)
$$

The posteriors of the hierarchical models shown here are all intractable. Thus variational inference is used in Cell2Location to infer the full posteriors.

## Further Models in Reference Based Deconvolution

DestVI incorporates complex nonlinear relationships into the latent variable setup through the use of neural networks. It is the first model that allows for variation of cell type expression prototypes in the data set through a latent variable. These concepts combine to parameterize the mean of a standard negative binomial distribution with gene dependent success probability $p_g$ as in Stereoscope.

RCTD is a reference based deconvolution model which uses the Poisson distribution instead of the more common negative binomial. For its reference cell type archetypes it simply uses mean expressions for each cell type. This straightforward approach aims for maximum robustness and has shown particular promise in the deconvolution of cell doublets.

SPOTlight uses non-negative matrix factorisation to first decompose the cells by genes matrix from a reference into two parts. First, a cells by topics matrix $H$ and a topics by genes matrix $W$. The matrix $W$ is then transferred to ST where a spots by topics matrix $H'$ is inferred. Topics are not exactly cell types and much care has to be put to ensure that correct latent features are modeled. 