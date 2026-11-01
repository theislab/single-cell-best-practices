# Quiz: Advanced QC of image-based technologies

Questions for [advanced_qc.ipynb](advanced_qc.ipynb), following the chapter's three QC levels and its eight key takeaways.
Type: **MCQ** = multiple choice (`multiple_choice_question`), **Card** = flip card (`flip_card`) in `scripts/quiz.py`.

---

## Q1 (MCQ): Which three levels does QC of image-based spatial data cover?

- Sample, batch and cell type: these are not the QC levels used in this chapter.
- Read, UMI and barcode: these are sequencing-based QC concepts, not image-based ones.
- **Single-molecule, segmentation and image** ✔
- Gene, cell and cluster: clustering is a downstream analysis step, not a QC level.

## Q2 (Card): Only ~3% of transcripts lie outside cells. Why should you still check where they are?

**Answer:** Unassigned transcripts can cluster in specific regions, such as sparse tissue or holes, and mark low-quality areas.

## Q3 (MCQ): What spatial pattern do you expect for negative control probes in good-quality data?

- **Random, scattered across the tissue** ✔
- Enriched in dense tissue regions: dense clusters of negative control probes mark regions to treat with caution.
- Co-localized with positive markers: negative control probes target sequences that should not be in the sample.
- Restricted to the tissue border: a spatially restricted pattern points to an artifact.

## Q4 (Card): How can vertical doublets form in image-based spatial data?

**Answer:** Segmentation collapses the 5-15 µm thick section into 2D, so cells at different depths can merge into one segmented object.

## Q5 (MCQ): What does a low vertical signal integrity (VSI) computed by ovrlpy indicate?

- A high-quality cell: high VSI (close to 1) means the top and bottom z-levels agree.
- Ambient RNA contamination: ambient RNA is assessed with Moran's I, not VSI.
- An invalid polygon: invalid geometries are found with shapely's `is_valid`.
- **A potential doublet** ✔

## Q6 (MCQ): Which global Moran's I value of a gene may hint at ambient RNA?

- Close to 1: strong positive autocorrelation suggests a real spatial expression pattern.
- **Close to 0** ✔
- Close to -1: strong negative autocorrelation is not the expected pattern of ambient RNA.

## Q7 (Card): What should you do with invalid cell or nucleus geometries?

**Answer:** Correct them, for example with the convex hull, or remove them before downstream analysis.

## Q8 (MCQ): What does Otsu's method do in the background intensity QC?

- **Picks the intensity threshold that maximizes the between-class variance** ✔
- Detects tissue folds in H&E images: this is done with tools such as GrandQC.
- Removes low-quality transcripts: transcript quality is assessed with the `qv` score.
- Assigns transcripts to cells: this is a segmentation task.

## Q9 (Card): Why should H&E artifact masks from tools such as GrandQC only be used as a guide?

**Answer:** These tools are built for regular pathology slides and struggle with post-Xenium H&E stains. The mask must also be aligned to the in-situ image before it can be applied to the data.
