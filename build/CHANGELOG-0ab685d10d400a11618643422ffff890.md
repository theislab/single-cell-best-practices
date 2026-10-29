---
numbering: false
---

# Changelog

## [v0.2.0](https://github.com/theislab/single-cell-best-practices/releases/tag/0.2.0) <sub>2026-10-29</sub>

### Added

- Add env- and lamin-setup dropdown with `make dropdown`. ([#348](https://github.com/theislab/single-cell-best-practices/pull/348)) <sub>`@LuisHenzlmeier`</sub>
- Adding UMIs explanation figure ([#363](https://github.com/theislab/single-cell-best-practices/pull/363)) <sub>`@LuisHeinzlmeier`</sub>
- Add a style guide and chapter template for contributors ([#367](https://github.com/theislab/single-cell-best-practices/pull/367)) <sub>`@LuisHeinzlmeier`</sub>
- Update `scRNA-seq` chapter and add a paragraph on quantification of gene expression ([#371](https://github.com/theislab/single-cell-best-practices/pull/371)) <sub>`@LuisHeinzlmeier`</sub>
- Restructure the introduction into `fundamental` and `advanced` data structures and frameworks chapters ([#417](https://github.com/theislab/single-cell-best-practices/pull/417)) <sub>`@LuisHeinzlmeier`</sub>
- Add a figure style guide for contributors ([#420](https://github.com/theislab/single-cell-best-practices/pull/420)) <sub>`@LuisHeinzlmeier`</sub>
- Add a GPU acceleration chapter (`RAPIDS-singlecell`) ([#431](https://github.com/theislab/single-cell-best-practices/pull/431)) <sub>`@Zethson`</sub>
- Add intersphinx mapping and hyperlink API mentions throughout the book ([#441](https://github.com/theislab/single-cell-best-practices/pull/441)) <sub>`@Zethson`</sub>
- Mention GPU-accelerated alignment with NVIDIA Parabricks in the raw data processing chapter ([#446](https://github.com/theislab/single-cell-best-practices/pull/446)) <sub>`@Zethson`</sub>
- Add a GSEA figure ([#463](https://github.com/theislab/single-cell-best-practices/pull/463)) <sub>`@LuisHeinzlmeier`</sub>
- Add guidance on integrating tumor samples ([#499](https://github.com/theislab/single-cell-best-practices/pull/499)) <sub>`@Zethson`</sub>
- Add the new `pertpy` DGE plots to the differential expression chapter ([#500](https://github.com/theislab/single-cell-best-practices/pull/500)) <sub>`@Zethson`</sub>
- Add a pull request template with a contribution checklist ([#501](https://github.com/theislab/single-cell-best-practices/pull/501)) <sub>`@Zethson`</sub>
- Discuss LLM and foundation model annotation in the annotation chapter ([#508](https://github.com/theislab/single-cell-best-practices/pull/508)) <sub>`@Zethson`</sub>
- Add a cell-cell communication chapter ([#451](https://github.com/theislab/single-cell-best-practices/pull/451)) <sub>`@cesarogiul`</sub>
- Link the Simplified Chinese translation from the landing page ([#484](https://github.com/theislab/single-cell-best-practices/pull/484)) <sub>`@Zethson`</sub>
- Link UMAP, t-SNE and four more glossary terms across the book ([#491](https://github.com/theislab/single-cell-best-practices/pull/491)) <sub>`@Zethson`</sub>
- Explain the negative binomial in the scRNA-seq chapter ([#478](https://github.com/theislab/single-cell-best-practices/pull/478)) <sub>`@Zethson`</sub>
- Explain why the dimensionality reduction chapter does not scale genes ([#473](https://github.com/theislab/single-cell-best-practices/pull/473)) <sub>`@Zethson`</sub>
- Attach a complete PDF of the book to every release ([#519](https://github.com/theislab/single-cell-best-practices/pull/519)) <sub>`@Zethson`</sub>

### Changed

- Add dataset generator and update texts in `Interoperability` chapter. ([#347](https://github.com/theislab/single-cell-best-practices/pull/347)) <sub>`@seohyonkim`</sub>
- Update `make dropdown` by adding key takeaways dropdown and removing anchors ([#352](https://github.com/theislab/single-cell-best-practices/pull/352)) <sub>`@LuisHeinzlmeier`</sub>
- Load datasets via `lamindb`, use `localconverter` instead of `anndata2ri.activate()`, and add descriptions to the plots in `Preprocessing and visualization` section ([#356](https://github.com/theislab/single-cell-best-practices/pull/356)) <sub>`@seohyonkim`</sub>
- Update dropdown chapter of `CONTRIBUTING.md` based on practical feedback ([#360](https://github.com/theislab/single-cell-best-practices/pull/360)) <sub>`@LuisHeinzlmeier`</sub>
- Use new connect syntax ([#404](https://github.com/theislab/single-cell-best-practices/pull/404)) <sub>`@Zethson`</sub>
- Update `10. Clustering` ([#406](https://github.com/theislab/single-cell-best-practices/pull/406)) <sub>`@seohyonkim`</sub>
- Use the proper dataset for `10. Clustering` ([#411](https://github.com/theislab/single-cell-best-practices/pull/411)) <sub>`@seohyonkim`</sub>
- Update `11. Annotation` ([#412](https://github.com/theislab/single-cell-best-practices/pull/412)) <sub>`@seohyonkim`</sub>
- Update `12. Data integration` ([#413](https://github.com/theislab/single-cell-best-practices/pull/413)) <sub>`@seohyonkim`</sub>
- Update `13. Pseudotemporal ordering` ([#414](https://github.com/theislab/single-cell-best-practices/pull/414)) <sub>`@seohyonkim`</sub>
- Update `14. RNA velocity` ([#415](https://github.com/theislab/single-cell-best-practices/pull/415)) <sub>`@seohyonkim`</sub>
- Update surface protein notebooks and key takeaways ([#423](https://github.com/theislab/single-cell-best-practices/pull/423)) <sub>`@javier-marchena-hurtado`</sub>
- Insert dropdowns for deployments ([#424](https://github.com/theislab/single-cell-best-practices/pull/424)) <sub>`@Zethson`</sub>
- Update the differential gene expression chapter ([#430](https://github.com/theislab/single-cell-best-practices/pull/430)) <sub>`@LuisHeinzlmeier`</sub>
- Add memory management details for `RAPIDS-singlecell` ([#432](https://github.com/theislab/single-cell-best-practices/pull/432)) <sub>`@Zethson`</sub>
- Migrate to Jupyter Book v2 ([#436](https://github.com/theislab/single-cell-best-practices/pull/436)) <sub>`@seohyonkim`</sub>
- Update the gene set enrichment analysis chapter ([#459](https://github.com/theislab/single-cell-best-practices/pull/459)) <sub>`@LuisHeinzlmeier`</sub>
- Update the compositional analysis chapter ([#448](https://github.com/theislab/single-cell-best-practices/pull/448)) <sub>`@LuisHeinzlmeier`</sub>
- Update the surface protein chapters ([#455](https://github.com/theislab/single-cell-best-practices/pull/455)) <sub>`@javier-marchena-hurtado`</sub>
- Replace `scArches` with `cellmapper` in the annotation chapter ([#457](https://github.com/theislab/single-cell-best-practices/pull/457)) <sub>`@seohyonkim`</sub>
- Improve the quiz cards used in the chapters ([#461](https://github.com/theislab/single-cell-best-practices/pull/461)) <sub>`@seohyonkim`</sub>
- Address the prose review points on the quality control chapter ([#474](https://github.com/theislab/single-cell-best-practices/pull/474)) <sub>`@Zethson`</sub>
- Hide noisy cell output and explain five core concepts ([#479](https://github.com/theislab/single-cell-best-practices/pull/479)) <sub>`@Zethson`</sub>
- Group the RNA chapters under one RNA header ([#487](https://github.com/theislab/single-cell-best-practices/pull/487)) <sub>`@Zethson`</sub>
- Revise quality control and embeddings, and rerun preprocessing on current scverse ([#489](https://github.com/theislab/single-cell-best-practices/pull/489)) <sub>`@Zethson`</sub>
- Point to batch-aware deviance in feature selection ([#490](https://github.com/theislab/single-cell-best-practices/pull/490)) <sub>`@Zethson`</sub>
- Hide the remaining noisy cell output ([#492](https://github.com/theislab/single-cell-best-practices/pull/492)) <sub>`@Zethson`</sub>
- Say which QC steps apply to plate-based protocols ([#493](https://github.com/theislab/single-cell-best-practices/pull/493)) <sub>`@Zethson`</sub>
- Cluster and annotate the preprocessed sample instead of a broken subset ([#494](https://github.com/theislab/single-cell-best-practices/pull/494)) <sub>`@Zethson`</sub>
- Rewrite the gene regulatory network chapter around `decoupler` and CollecTRI ([#495](https://github.com/theislab/single-cell-best-practices/pull/495)) <sub>`@Zethson`</sub>
- Connect to `lamindb` and track notebooks the same way in every chapter ([#496](https://github.com/theislab/single-cell-best-practices/pull/496)) <sub>`@Zethson`</sub>
- Rewrite the chromatin accessibility section around `SnapATAC2` ([#497](https://github.com/theislab/single-cell-best-practices/pull/497)) <sub>`@Zethson`</sub>
- Rewrite the adaptive immune receptor section around `scirpy` 0.25 ([#498](https://github.com/theislab/single-cell-best-practices/pull/498)) <sub>`@Zethson`</sub>
- Group acknowledgements, glossary and changelog under Appendix ([#503](https://github.com/theislab/single-cell-best-practices/pull/503)) <sub>`@Zethson`</sub>
- Rewrite the multimodal integration chapters in Python with public data ([#504](https://github.com/theislab/single-cell-best-practices/pull/504)) <sub>`@Zethson`</sub>
- Rewrite the perturbation modeling chapter around current screen analysis ([#505](https://github.com/theislab/single-cell-best-practices/pull/505)) <sub>`@Zethson`</sub>
- Restore the GRN rewrite and match environment files to chapters ([#506](https://github.com/theislab/single-cell-best-practices/pull/506)) <sub>`@Zethson`</sub>
- Bring the contributing guide in line with the current build setup ([#507](https://github.com/theislab/single-cell-best-practices/pull/507)) <sub>`@Zethson`</sub>
- Collapse the doubled spacing between notebook cells ([#510](https://github.com/theislab/single-cell-best-practices/pull/510)) <sub>`@Zethson`</sub>
- Update the contact details and shrink the cover ([#511](https://github.com/theislab/single-cell-best-practices/pull/511)) <sub>`@Zethson`</sub>
- Rewrite the outlook for foundation models, agents and clinical data ([#512](https://github.com/theislab/single-cell-best-practices/pull/512)) <sub>`@Zethson`</sub>
- Split the introduction by modality ([#515](https://github.com/theislab/single-cell-best-practices/pull/515)) <sub>`@Zethson`</sub>

### Fixed

- Pin `jupyter-book==1.0.4.post1` to restore compatibility after upstream v2 release broke PR preview and publish builds ([#400](https://github.com/theislab/single-cell-best-practices/pull/400)) <sub>`@seohyonkim`</sub>
- Fix precommit action to v3.0.0 ([#357](https://github.com/theislab/single-cell-best-practices/pull/357)) <sub>`@seohyonkim`</sub>
- Fix missed glossary links in `scRNA sequencing` and `raw data processing` ([#361](https://github.com/theislab/single-cell-best-practices/pull/361)) <sub>`@seohyonkim`</sub>
- Generating subset of human bmmcs and use it in chapter `10. Clustering` ([#410](https://github.com/theislab/single-cell-best-practices/pull/410)) <sub>`@seohyonkim`</sub>
- Minor factual fix ([#425](https://github.com/theislab/single-cell-best-practices/pull/425)) <sub>`@ArchKudo`</sub>
- Fix `scran` normalization to use raw counts for `computeSumFactors` ([#428](https://github.com/theislab/single-cell-best-practices/pull/428)) <sub>`@matthiaspeterhans`</sub>
- Update link for Cell Ranger output annotations ([#437](https://github.com/theislab/single-cell-best-practices/pull/437)) <sub>`@Chloe-Shen`</sub>
- Bound the `DataFrame` preview in the data-structures chapter ([#440](https://github.com/theislab/single-cell-best-practices/pull/440)) <sub>`@Zethson`</sub>
- Fix silently dropped citations by deduplicating BibTeX keys ([#442](https://github.com/theislab/single-cell-best-practices/pull/442)) <sub>`@Zethson`</sub>
- Fix invisible MuData/AnnData object summaries caused by a quiz CSS rule leaking `--pst-color-text-base: transparent` to all cell outputs ([#444](https://github.com/theislab/single-cell-best-practices/pull/444)) <sub>`@Zethson`</sub>
- Remove duplicated paragraph in section 6.5 ([#445](https://github.com/theislab/single-cell-best-practices/pull/445)) <sub>`@durr1602`</sub>
- Fix a few typos ([#449](https://github.com/theislab/single-cell-best-practices/pull/449)) <sub>`@durr1602`</sub>
- Fix inline code and cell output formatting ([#456](https://github.com/theislab/single-cell-best-practices/pull/456)) <sub>`@Zethson`</sub>
- Fix the annotation environment ([#464](https://github.com/theislab/single-cell-best-practices/pull/464)) <sub>`@Zethson`</sub>
- Fix deployment issues of the Jupyter Book v2 site ([#467](https://github.com/theislab/single-cell-best-practices/pull/467)) <sub>`@seohyonkim`</sub>
- Redirect the pre v2 URLs of the book instead of returning 404 ([#471](https://github.com/theislab/single-cell-best-practices/pull/471)) <sub>`@Zethson`</sub>
- Fix the toy dataset download in the raw data processing chapter ([#476](https://github.com/theislab/single-cell-best-practices/pull/476)) <sub>`@Zethson`</sub>
- Stop presenting an underflowed p-value as a p-value of zero ([#477](https://github.com/theislab/single-cell-best-practices/pull/477)) <sub>`@Zethson`</sub>
- Point the `liana` intersphinx inventory at its new docs domain ([#485](https://github.com/theislab/single-cell-best-practices/pull/485)) <sub>`@Zethson`</sub>
- Show dropdown content in the PDF ([#502](https://github.com/theislab/single-cell-best-practices/pull/502)) <sub>`@Zethson`</sub>
- Fix the contributing guide link ([#517](https://github.com/theislab/single-cell-best-practices/pull/517)) <sub>`@Zethson`</sub>
- Replace dead links across the book ([#518](https://github.com/theislab/single-cell-best-practices/pull/518)) <sub>`@Zethson`</sub>

### Removed

- Remove the PR preview deployment from GitHub Actions ([#427](https://github.com/theislab/single-cell-best-practices/pull/427)) <sub>`@Zethson`</sub>
- Remove the Dockerfile ([#513](https://github.com/theislab/single-cell-best-practices/pull/513)) <sub>`@Zethson`</sub>

## [v0.1.0](https://github.com/theislab/single-cell-best-practices/releases/tag/0.1.0) <sub>2023-11-14</sub>

### Added

- Add simpleaf example to the raw data processing section ([#116](https://github.com/theislab/single-cell-best-practices/pull/116)) <sub>`@DongzeHE`</sub>
- Add `inferring trajectories` section ([#101](https://github.com/theislab/single-cell-best-practices/pull/101)) <sub>`@WeilerP`</sub>
- Add `perturbation modelling` chapter ([#79](https://github.com/theislab/single-cell-best-practices/pull/79)) <sub>`@Zethson`</sub>
- Add Annotation ([#85](https://github.com/theislab/single-cell-best-practices/pull/85)) <sub>`@LisaSikkema`</sub>
- Add `gsea pathway` chapter ([#62](https://github.com/theislab/single-cell-best-practices/pull/62)) <sub>`@soroorh`</sub>
- Add `neighborhood analysis`, `spatial domains`, `spacially variable genes` chapters ([#86](https://github.com/theislab/single-cell-best-practices/pull/86)) <sub>`@giovp`</sub>
- Add `cell-cell communication` chapter ([#140](https://github.com/theislab/single-cell-best-practices/pull/140)) <sub>`@dbdimitrov`</sub>
- Add `paired integration` chapter ([#103](https://github.com/theislab/single-cell-best-practices/pull/103)) <sub>`@alitinet`</sub>
- Add multiple multimodal immune receptor chapters ([#63](https://github.com/theislab/single-cell-best-practices/pull/63)) <sub>`@drEast`</sub>
- Add `spatial deconvolution` and `imputation` chapter ([#142](https://github.com/theislab/single-cell-best-practices/pull/142)) <sub>`@AnnaChristina`</sub>
- Add feedback from Robin Browaeys to `cell-cell communication` chapter ([#157](https://github.com/theislab/single-cell-best-practices/pull/157)) <sub>`@dbdimitrov`</sub>
- Add docker container & improve environments ([#124](https://github.com/theislab/single-cell-best-practices/pull/124)) <sub>`@Zethson`</sub>
- Add `compositional analysis` chapter ([#89](https://github.com/theislab/single-cell-best-practices/pull/89)) <sub>`@Zethson`</sub>
- Add `lineage tracing` chapter ([#88](https://github.com/theislab/single-cell-best-practices/pull/88)) <sub>`@mattjones315`</sub>
- Add `preprocessing and visualization` section ([#59](https://github.com/theislab/single-cell-best-practices/pull/59)) <sub>`@AnnaChristina`</sub>
- Add `clustering` chapter ([#72](https://github.com/theislab/single-cell-best-practices/pull/72)) <sub>`@AnnaChristina`</sub>
- Add PDF job ([#65](https://github.com/theislab/single-cell-best-practices/pull/65)) <sub>`@Zethson`</sub>
- Add `prior art` chapter ([#58](https://github.com/theislab/single-cell-best-practices/pull/58)) <sub>`@Zethson`</sub>
- Add new book CI ([#57](https://github.com/theislab/single-cell-best-practices/pull/57)) <sub>`@Zethson`</sub>
- Add `preamble` chapter ([#53](https://github.com/theislab/single-cell-best-practices/pull/53)) <sub>`@Zethson`</sub>
- Add scATAC part ([#162](https://github.com/theislab/single-cell-best-practices/pull/162)) <sub>`@lauradmartens`</sub>
- Add `modelling mechanism` section ([#96](https://github.com/theislab/single-cell-best-practices/pull/96)) <sub>`@ilibarra`</sub>
- Add `Integration` chapter ([#17](https://github.com/theislab/single-cell-best-practices/pull/17)) <sub>`@lazappi`</sub>

### Changed

- Fix typos ([#164](https://github.com/theislab/single-cell-best-practices/pull/164)) (`@mjstrumillo`)
- Correct 2 spelling mistakes ([#155](https://github.com/theislab/single-cell-best-practices/pull/155)) (`@namsaraeva`)
- Fix typos in chapter Normalization ([#118](https://github.com/theislab/single-cell-best-practices/pull/118)) (`@galicae`)
- Update `RNA velocity` chapter ([#100](https://github.com/theislab/single-cell-best-practices/pull/100)) (`@WeilerP`)
- Update `pseudotime` chapter ([#148](https://github.com/theislab/single-cell-best-practices/pull/148)) (`@WeilerP`)
- Update multimodal immune receptor chapters ([#110](https://github.com/theislab/single-cell-best-practices/pull/110)) (`@drEast`)
- Simplify `GSEA` chapter and improve performance ([#119](https://github.com/theislab/single-cell-best-practices/pull/119)) (`@ivirshup`)
- Improve `integration` chapter ([#109](https://github.com/theislab/single-cell-best-practices/pull/109)) (`@lazappi`)
- Update B-cell clonotype analysis ([#105](https://github.com/theislab/single-cell-best-practices/pull/105)) (`@jdhenaos`)
- Citeseq proofread ([#102](https://github.com/theislab/single-cell-best-practices/pull/102)) (`@cramsuig`)
- Review of analysis frameworks ([#98](https://github.com/theislab/single-cell-best-practices/pull/98)) (`@ivirshup`)
- Citeseq pp notebook ([#60](https://github.com/theislab/single-cell-best-practices/pull/60)) (`@danielStrobl`)
- Update `perturbation modeling` chapter ([#91](https://github.com/theislab/single-cell-best-practices/pull/91)) (`@yugeji`)
- Update `compositional analysis` chapter ([#76](https://github.com/theislab/single-cell-best-practices/pull/76)) (`@johannesostner`)
- Update `raw data processing` chapter ([#77](https://github.com/theislab/single-cell-best-practices/pull/77)) (`@DongzeHE`)
- Update `differential gene expression` chapter ([#80](https://github.com/theislab/single-cell-best-practices/pull/80)) (`@alitinet`)
- Update `preprocessing` section ([#139](https://github.com/theislab/single-cell-best-practices/pull/139)) (`@AnnaChristina`)
- Update `compositional analysis` chapter ([#149](https://github.com/theislab/single-cell-best-practices/pull/149)) (`@xinyuejohn`)
- Update `paired integration` and `advanced integration` chapter ([#135](https://github.com/theislab/single-cell-best-practices/pull/135)) (`@alitinet`)
- Improve pseudobulk plots for `differential gene expression` chapter ([#131](https://github.com/theislab/single-cell-best-practices/pull/131)) (`@alitinet`)
- Update `advanced integration` chapter ([#112](https://github.com/theislab/single-cell-best-practices/pull/112)) (`@alitinet`)
- Fix typos ([#166](https://github.com/theislab/single-cell-best-practices/pull/166)) (`@alitinet`)
- Update `compositional analysis` chapter according to changes of `pertpy` ([#152](https://github.com/theislab/single-cell-best-practices/pull/152)) (`@xinyuejohn`)
- Update link in `README.md` ([#107](https://github.com/theislab/single-cell-best-practices/pull/107)) (`@WeilerP`)
- Update `spatial deconvolution` chapter ([#93](https://github.com/theislab/single-cell-best-practices/pull/93)) (`@amitfrish`)
- Update `experimental data collection` chapter ([#71](https://github.com/theislab/single-cell-best-practices/pull/71)) (`@AnnaChristina`)
- Update `introduction` section ([#70](https://github.com/theislab/single-cell-best-practices/pull/70)) (`@AnnaChristina`)
- Update `preamble` ([#69](https://github.com/theislab/single-cell-best-practices/pull/69)) (`@AnnaChristina`)

### Fixed

- Fix broken link on edit button ([#115](https://github.com/theislab/single-cell-best-practices/pull/115)) (`@emiller88`)
- Fix environment CI ([#158](https://github.com/theislab/single-cell-best-practices/pull/158)) (`@Zethson`)
- Fix surface protein environment and small bugs ([#154](https://github.com/theislab/single-cell-best-practices/pull/154)) (`@danielStrobl`)
- Add missing links to other chapters in `Compositional analysis` chapter ([#145](https://github.com/theislab/single-cell-best-practices/pull/145)) (`@dbdimitrov`)
- Fix environments for `surface protein` section and small bugs ([#154](https://github.com/theislab/single-cell-best-practices/pull/154)) (`@danielStrobl`)
