# Research on EEG-Based Methods for Depression Diagnosis

This repository contains the code and selected artifacts for my undergraduate thesis, which studies **EEG-based diagnosis of Major Depressive Disorder (MDD)** and **subtype discovery within the MDD cohort** using the **TDBRAIN** dataset.

The thesis compares **ShallowConvNet** and **M-ShallowConvNet** across six EEG frequency bands:

- Delta
- Theta
- Alpha
- Beta
- Low Gamma
- High Gamma

The final conclusion is that **High Gamma** provides the strongest discriminative power for MDD-vs-HC classification in this study. The repository also includes the follow-up subtype analysis workflow based on **K-means clustering**, **PCA visualization**, **channel-level heatmaps**, and **functional connectivity analysis**.

## Included Files

- `data pre processing.py`
  Band-specific EEG preprocessing with MNE.
- `training shallow.ipynb`
  ShallowConvNet training notebook.
- `training m-shallow.ipynb`
  M-ShallowConvNet training notebook.
- `cluster.ipynb`
  High-Gamma MDD clustering workflow.
- `visualization.ipynb`
  Result plotting and figure generation.
- `training_shallow *.csv`
  Exported training metrics for different frequency bands.
- `training_mshallow *.csv`
  Exported training metrics for different frequency bands.
- `brain_map_high_gamma.png`
- `correlation_matrix.png`
- `3d_brain_network.png`
- `montage.png`
- `montage_64.png`
- thesis PDF
- thesis presentation slides

## Not Included

This repository intentionally does **not** include:

- raw TDBRAIN EEG data
- preprocessed `.fif` files generated on the local `E:` drive
- participant metadata spreadsheets
- administrative school documents
- literature PDFs collected for reference
- exploratory scripts that were not part of the final thesis package

This keeps the repository lightweight, reproducible, and safer to publish publicly.

## Method Overview

1. Preprocess raw EEG recordings with filtering, resampling, bad-channel handling, epoching, re-referencing, and ICA.
2. Build band-specific training sets for MDD and healthy controls.
3. Train both ShallowConvNet and M-ShallowConvNet with Focal Loss under class imbalance.
4. Compare performance across six frequency bands.
5. Focus on the High-Gamma band for subtype discovery within the MDD group.
6. Use elbow and silhouette analysis to select the number of clusters.
7. Visualize cluster structure with PCA, channel-level heatmaps, and functional connectivity matrices.

## Main Findings

- M-ShallowConvNet outperforms the baseline ShallowConvNet in this project.
- High Gamma is the best-performing band for MDD-vs-HC classification.
- The MDD cohort separates into two interpretable subtypes in the High-Gamma setting.
- The two subtypes show distinct posterior vs. fronto-temporal functional connectivity patterns.

## Environment Notes

The current notebooks and scripts were developed on Windows with local absolute paths on `E:`. Before rerunning the pipeline on another machine, update the dataset and output paths accordingly.

Typical dependencies include:

- Python 3.10+
- numpy
- pandas
- scipy
- mne
- matplotlib
- seaborn
- scikit-learn
- torch

## Suggested Reproduction Order

1. Prepare the TDBRAIN labels and raw EEG files locally.
2. Run `data pre processing.py` for the target frequency band.
3. Run `training shallow.ipynb` and `training m-shallow.ipynb`.
4. Compare the exported CSV metrics across bands.
5. Run `cluster.ipynb` for the High-Gamma subtype analysis.
6. Run `visualization.ipynb` to generate summary figures.

## Thesis Context

The thesis document included here is written in Chinese, while this README is intended for a broader GitHub audience.
