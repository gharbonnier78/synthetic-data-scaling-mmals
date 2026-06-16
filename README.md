# Synthetic Data in the Age of Scaling

A multilevel analysis of Julia Kempe's public lecture **“Synthetic Data – Friend or Foe in the Age of Scaling?”**, with research orientations for:

- MMALS and Geometry-MMALS
- STRAT-Q and probabilistic Master Test Plans
- Test Data Governance and Verifiable Evidence
- Continual learning, host specialization, and dual memory
- Geometric filtering and uncertainty on manifolds

## Primary video

https://www.youtube.com/watch?v=D9x3DT16mGg&list=PLx5f8IelFRgHrJ9W6_fbfO3ahDrXMEIWn

## Important status

This is an independent video analysis and research note. It is not a transcript, not an official summary, and not endorsed by Julia Kempe, IHES, NYU, or Meta.

## Repository structure

```text
paper/
  main.tex
  references.bib
  sections/
  figures/
code/
  generate_figures.py
notebooks/
  synthetic_data_scaling_tutorial.ipynb
data/
  reproducible toy CSV outputs
docs/
  research and architecture notes
video_notes/
  lecture-to-document map
```

## Build

```bash
python code/generate_figures.py
cd paper
latexmk -pdf -interaction=nonstopmode main.tex
```

The compiled preprint is provided in the repository root.

## Reading tracks

- **12-year-old track:** intuitive stories about copies, rare books, and referees.
- **Engineer track:** distributions, pseudo-label drift, failure modes, governance, cost, and deployment.
- **PhD track:** asymptotic laws, recursive models, kernel ridge regression, verification theory, and research hypotheses.

## Reproducibility

The plots and CSV files are educational reconstructions. They do not claim to reproduce the original large-scale experiments exactly. Follow the cited papers and authors' repositories for exact replication.

## Suggested citation

See `CITATION.cff`.

## License

- Original text and figures: CC BY 4.0.
- Code: MIT.
- Lecture, papers, trademarks, and third-party materials remain the property of their respective owners.
