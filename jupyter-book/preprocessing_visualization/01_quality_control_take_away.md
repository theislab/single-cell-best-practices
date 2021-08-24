# Pitfalls & recommendations

<!-- Quick wrap-up for the module -->

*TODO AS DO THIS AS adjust main take aways during and after hackthon. this corrently is taken from BP1.0.*

In this module, you learned:

- perform QC by finding outlier peaks ib the number of genes, the count depth and the fraction of mitochondrial reads. 
Consider these covariates jointly instead of separatly;
- Be as permissive of QC thresholding as possible, and revisit QC if downstream clustering cannot be interpreted;
- If the distribution of QC covariates differ between samples, QC thresholds should be determined separately for each 
sample to account for sample quality differences as in Plasschaert et al (2018).

## To go further

<!-- Some extra links of content to go further -->

You can refer to the following examples and papers which are related to
the concepts approached during this module:

- [Predictive machine learning pipeline with mixed data types](https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html#sphx-glr-auto-examples-compose-plot-column-transformer-mixed-types-py)
- [Importance of feature scaling](https://scikit-learn.org/stable/auto_examples/preprocessing/plot_scaling_importance.html#sphx-glr-auto-examples-preprocessing-plot-scaling-importance-py)
