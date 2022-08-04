# Motivation

One of the main reasons for designing any biological study is to compare and to evaluate conditions: How does gene expression change in brain cells of Parkinson’s Disease patients compared to healthy adults? What is the effect of a gene knockout on a specific pathway? What is the cellular response to a certain stimulus? Does the cellular composition change after drug use?
Modeling and predicting the effects of such interventions, also known as perturbations, is a key task of systems biology.
Conceiving perturbations at the systems level demands a strong understanding of the interactions of mechanisms at a molecular, cellular, and tissue level.
To allow for the inference of such knowledge, experiments are commonly designed to include one reference condition, which is usually a healthy sample, and one or more perturbations.
This allows for the statistical determination of genes that are over- or underexpressed in any of the conditions. These candidate genes could then serve as biological markers for the specific conditions of interest and be validated experimentally with for example stainings or qPCR.
Besides the determination of marker genes for conditions, the actual composition, such as the cell-type composition, may vary across the conditions. Determining these changes may provide insights into the system's response for perturbations.
The space of possible perturbations is vast and it is not always possible to induce all potential desired perturbations. Advanced deep-learning methods allow for the insilico prediction of the effects of unseen perturbations or even specific drug dosages. This greatly reduces the amount of experimental work and allows for exploration of the perturbation space.
Finally, many perturbations have strong effects on pathways. Knowing about these effects allows researchers to learn about the actual effects of, for example, differentially expressed genes on immune response pathways, potentially generating drug targets.
