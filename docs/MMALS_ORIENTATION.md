# MMALS orientation from synthetic-data scaling research

## Central risk

MMALS can recursively generate its own route labels, memories, host activations, and summaries. A small initial routing preference can become the training truth of later versions.

## Design principle

**Local simplicity, global functional diversity.**

A simple input should use a short route. Rare but causally useful routes must remain globally accessible.

## Required metrics

- Functional Tail Coverage
- host dominance and route entropy
- host ablation impact
- route swaps and candidate permutations
- synthetic lineage depth
- recovery delay after real anchors
- cost versus verified residual reduction

## Required treatments

- independent/oracle traces only
- recursive synthetic traces only
- fixed real anchor plus synthetic
- accumulated fresh real plus synthetic
- verified synthetic route candidates
- lineage-aware consolidation
- reconstructive versus compiled memory
- fixed versus state-dependent route temperature

## Backbone rule

MMALS must remain backbone-agnostic. Start with equal dense base backbones across hosts; replicate with a second model family; introduce heterogeneous hosts only after causal specialization is demonstrated.
