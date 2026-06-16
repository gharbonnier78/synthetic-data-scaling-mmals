# Build instructions

## Requirements

- Python 3.10+
- `numpy`, `pandas`, `matplotlib`, `networkx`, `nbformat`, `qrcode`, `Pillow`
- TeX Live with `pdflatex`, `latexmk`, and a working BibTeX implementation

## Full build

From the repository root:

```bash
make
```

This regenerates the figures and compiles:

```text
Synthetic_Data_Age_MMALS_STRATQ.pdf
```

## Manual build

```bash
python code/generate_figures.py
cd paper
latexmk -pdf -interaction=nonstopmode main.tex
```

The repository includes a small BibTeX wrapper that falls back to `bibtex.original` or `bibtex8` when needed.
