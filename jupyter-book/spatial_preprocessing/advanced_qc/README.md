# NAME

- Please install the following conda [conda env](advanced_qc.yml) for the tutorial.

## Data format

- Nothing special needed as we will use example data.
- Please run the notebook [xenium_breast_cancer]() first.

### Input

The data we will use has the following structure:

```
SpatialData object, with associated Zarr store: path/
├── Images
│     ├── 'morphology_focus': DataTree[cyx] (1, 25778, 35416), (1, 12889, 17708), (1, 6444, 8854), (1, 3222, 4427), (1, 1611, 2213)
│     └── 'morphology_mip': DataTree[cyx] (1, 25778, 35416), (1, 12889, 17708), (1, 6444, 8854), (1, 3222, 4427), (1, 1611, 2213)
├── Labels
│     ├── 'cell_labels': DataTree[yx] (25778, 35416), (12889, 17708), (6444, 8854), (3222, 4427), (1611, 2213)
│     └── 'nucleus_labels': DataTree[yx] (25778, 35416), (12889, 17708), (6444, 8854), (3222, 4427), (1611, 2213)
├── Points
│     └── 'transcripts': DataFrame with shape: (<Delayed>, 8) (3D points)
├── Shapes
│     ├── 'cell_boundaries': GeoDataFrame shape: (167780, 1) (2D shapes)
│     ├── 'cell_circles': GeoDataFrame shape: (167780, 2) (2D shapes)
│     └── 'nucleus_boundaries': GeoDataFrame shape: (167780, 1) (2D shapes)
└── Tables
      └── 'table': AnnData (167780, 313)
with coordinate systems:
    ▸ 'global', with elements:
        morphology_focus (Images), morphology_mip (Images), cell_labels (Labels), nucleus_labels (Labels), transcripts (Points), cell_boundaries (Shapes), cell_circles (Shapes), nucleus_boundaries (Shapes)

AnnData object with n_obs × n_vars = 167780 × 313
    obs: 'cell_id', 'transcript_counts', 'control_probe_counts', 'control_codeword_counts', 'total_counts', 'cell_area', 'nucleus_area', 'region', 'celltype'
    var: 'gene_ids', 'feature_types', 'genome'
    uns: 'spatialdata_attrs'
    obsm: 'spatial'
```

### Output

## Metrics

### Level 1: Single-molecule spatial observations

- Transcript quality density
- Transcript location density (outside cell, inside cell, in nuclei)
- Negative control probe density
- Doublet detection (z-stack investigation) with overlpy
- Gene panel (ambient) RNA analysis
- Positve and negative marker investigation

### Level 2: Segmentation

- Conventional single cell QC
    - total counts
    - gene counts
    - mt coverage
    - ribosomal coverage

### Level 3: Image-based

- Invalid geometries check and correction
- Background intensity check and correction
- H&E artefact detection
