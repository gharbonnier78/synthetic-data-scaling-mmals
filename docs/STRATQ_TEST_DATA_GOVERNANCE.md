# STRAT-Q and Test Data Governance orientation

A test dataset is evidence, not just volume.

## Evidence Passport fields

- identity and version
- real/simulated/generative origin
- parent lineage and generation depth
- model, prompt, seed, temperature, top-p, filters
- oracle and verifier
- verifier calibration and independence
- freshness
- tail coverage
- claim supported
- permitted use
- reviewer status

## Residual-risk decomposition

```text
R_residual = R_tested + R_missing + R_oracle + R_drift + R_dependence
```

Synthetic tests often reduce uncertainty inside known regimes. They do not automatically reduce risk from missing regimes.
