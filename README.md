# Research on EEG-Based Methods for Depression Diagnosis

This repository contains the public code and manuscript for an EEG-based depression-diagnosis study built on the **TDBRAIN** dataset.

The workflow combines:

- band-specific EEG preprocessing
- MDD-versus-control classification with **ShallowConvNet** and **M-ShallowConvNet**
- high-gamma-focused subtype discovery with clustering
- figure generation for channel-level and connectivity-level analysis

## Included Materials

- `data pre processing.py`
  EEG preprocessing and band-specific data preparation.
- `training shallow.ipynb`
  ShallowConvNet training workflow.
- `training m-shallow.ipynb`
  M-ShallowConvNet training workflow.
- `cluster.ipynb`
  High-gamma clustering and subtype analysis workflow.
- `visualization.ipynb`
  Result aggregation and figure generation.
- thesis manuscript PDF

## Method Summary

1. Preprocess raw EEG recordings with filtering, resampling, bad-channel handling, epoching, re-referencing, and ICA.
2. Build band-specific datasets for the MDD and control groups.
3. Train ShallowConvNet and M-ShallowConvNet across six frequency bands.
4. Compare performance across Delta, Theta, Alpha, Beta, Low Gamma, and High Gamma.
5. Use the High-Gamma setting for subtype discovery within the MDD group.
6. Apply clustering, PCA visualization, channel-level heatmaps, and functional-connectivity analysis.

## Main Findings

- **M-ShallowConvNet** performs better than the baseline **ShallowConvNet** in this study.
- **High Gamma** is the strongest-performing band for **MDD-versus-control classification**.
- The **MDD cohort** separates into **two interpretable subtypes** in the high-gamma setting.
- The identified subtypes show **distinct posterior and fronto-temporal connectivity patterns**.

## Public Scope

This public version intentionally excludes:

- raw TDBRAIN EEG data
- locally generated `.fif` files
- exported training-metrics `.csv` files generated from notebook runs
- participant metadata spreadsheets
- administrative documents
- local reference-library files
- exploratory scripts that are not part of the final public workflow

## Environment Notes

The notebooks and scripts were developed on Windows and still contain local absolute paths on `E:`. Update dataset and output paths before rerunning the full pipeline on another machine.

`visualization.ipynb` expects band-wise metrics tables exported from the training notebooks. In this public version, those `.csv` files are omitted; rerun `training shallow.ipynb` and `training m-shallow.ipynb` to regenerate them locally before running the full visualization workflow.

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

## Language Note

The manuscript included in this repository is written in Chinese, while this README is written for a broader GitHub audience.
