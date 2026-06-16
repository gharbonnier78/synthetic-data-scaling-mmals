# Notebook Companion Paper

This directory contains the short companion paper for:

`notebooks/synthetic_data_scaling_tutorial.ipynb`

## Title

**A Reproducible Tutorial on Synthetic-Data Scaling and Functional Collapse: Design, Scope, and Research Use of the Companion Notebook**

## Purpose

The note explains:

- what each notebook module computes;
- which cells are exact calculations, theoretical illustrations, or conceptual hypotheses;
- what the notebook does and does not prove;
- how the tutorial connects synthetic-data collapse to MMALS host and route ecology;
- which experiments are required to replace scripted curves with real evidence.

## Build

```bash
latexmk -pdf -interaction=nonstopmode main.tex
```

The compiled file is:

`Synthetic_Data_Scaling_Notebook_Companion.pdf`

## Status

This is a pedagogical companion note. It is not an empirical reproduction of the published LLM experiments and not a validation of MMALS.
