from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "paper" / "figures"
DATA = ROOT / "data"
FIG.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "legend.fontsize": 8,
    "figure.dpi": 160,
    "savefig.bbox": "tight",
})


def save(fig, name: str) -> None:
    fig.savefig(FIG / f"{name}.pdf")
    fig.savefig(FIG / f"{name}.png", dpi=220)
    plt.close(fig)


def scaling_cutoff() -> pd.DataFrame:
    beta = 1.5
    c = (beta - 1.0) / beta
    T = np.logspace(1, 6, 240)
    rows = []
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for k in [100, 1_000, 10_000, 100_000]:
        err = T ** (-c) + k ** (-(beta - 1.0))
        ax.loglog(T, err, label=f"cutoff k={k:,}")
        for t, e in zip(T, err):
            rows.append({"T": t, "k": k, "beta": beta, "test_error": e})
    ax.set_xlabel("Training sample size T")
    ax.set_ylabel("Test error")
    ax.set_title("Chopped-tail scaling: more samples cannot remove missing support")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend()
    save(fig, "chopped_tail_scaling")
    df = pd.DataFrame(rows)
    df.to_csv(DATA / "chopped_tail_scaling.csv", index=False)
    return df


def real_synthetic_mix() -> pd.DataFrame:
    beta = 1.5
    c = 1 - 1 / beta
    k = 1000
    tai = np.logspace(1, 6, 240)
    rows = []
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for tr in [100, 1_000, 10_000, 100_000]:
        err = (tr + tai) ** (-c) + k ** (-(beta - 1))
        real_only = tr ** (-c)
        ax.loglog(tai, err, label=f"T_real={tr:,}")
        ax.axhline(real_only, linestyle="--", linewidth=0.8, alpha=0.45)
        for a, e in zip(tai, err):
            rows.append({"T_real": tr, "T_AI": a, "k": k, "beta": beta, "test_error": e})
    ax.set_xlabel("Added synthetic samples $T_{AI}$")
    ax.set_ylabel("Test error")
    ax.set_title("Synthetic data helps most when real data are scarce")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend()
    save(fig, "real_synthetic_mix")
    df = pd.DataFrame(rows)
    df.to_csv(DATA / "real_synthetic_mix.csv", index=False)
    return df


def recursive_regression() -> pd.DataFrame:
    rng = np.random.default_rng(7)
    x = np.linspace(-3, 3, 120)
    w0 = 0.9
    b0 = 0.15
    sigma = 0.6
    rows = []
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    base_y = w0 * x + b0
    ax.plot(x, base_y, linewidth=2.2, label="ground truth $w_0$")
    wg, bg = w0, b0
    for g in range(1, 6):
        # finite-sample + regularization-inspired drift
        wg = 0.92 * wg + rng.normal(0, 0.055)
        bg = 0.90 * bg + rng.normal(0, 0.035)
        y = wg * x + bg
        ax.plot(x, y, linewidth=1.1, alpha=0.82, label=f"generation {g}")
        for xv, yv in zip(x, y):
            rows.append({"generation": g, "x": xv, "prediction": yv, "slope": wg, "intercept": bg})
    sample_x = rng.normal(0, 1.2, 45)
    sample_y = w0 * sample_x + b0 + rng.normal(0, sigma, 45)
    ax.scatter(sample_x, sample_y, s=15, alpha=0.45, label="real observations")
    ax.set_xlabel("Input feature")
    ax.set_ylabel("Label / prediction")
    ax.set_title("Recursive relabeling: precision can increase around a drifting target")
    ax.grid(True, alpha=0.25)
    ax.legend(ncol=2)
    save(fig, "recursive_relabeling")
    df = pd.DataFrame(rows)
    df.to_csv(DATA / "recursive_relabeling.csv", index=False)
    return df


def verification_bootstrap() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 3.6))
    ax.set_axis_off()
    boxes = [
        (0.02, 0.34, 0.15, 0.34, "200k verified\nseed examples"),
        (0.23, 0.34, 0.15, 0.34, "Imperfect\ngenerator"),
        (0.44, 0.34, 0.15, 0.34, "12M candidate\npseudo-labels"),
        (0.65, 0.34, 0.15, 0.34, "Independent\nverifier"),
        (0.84, 0.34, 0.14, 0.34, "Filtered data\n+ retraining"),
    ]
    for x, y, w, h, text in boxes:
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.018", linewidth=1.3, facecolor="white")
        ax.add_patch(p)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=10)
    for i in range(len(boxes)-1):
        x1 = boxes[i][0] + boxes[i][2]
        y1 = boxes[i][1] + boxes[i][3]/2
        x2 = boxes[i+1][0]
        y2 = boxes[i+1][1] + boxes[i+1][3]/2
        ax.add_patch(FancyArrowPatch((x1+0.01, y1), (x2-0.01, y2), arrowstyle="-|>", mutation_scale=15, linewidth=1.2))
    ax.text(0.72, 0.17, "keep if residual < threshold", ha="center", fontsize=9)
    ax.text(0.52, 0.87, "Generate many; consolidate only independently verified novelty", ha="center", fontsize=13, weight="bold")
    save(fig, "verification_bootstrap")


def mmals_ecology() -> pd.DataFrame:
    t = np.arange(0, 60)
    # synthetic recursive reinforcement collapse scenario
    h1_c = 0.45 + 0.5 * (1 - np.exp(-t / 15))
    h2_c = 0.25 * np.exp(-t / 20)
    h3_c = 0.20 * np.exp(-t / 18)
    h4_c = 1 - h1_c - h2_c - h3_c
    # verified / anchored scenario
    h1_v = 0.45 + 0.12 * (1 - np.exp(-t / 18))
    h2_v = 0.22 + 0.03 * np.sin(t / 8)
    h3_v = 0.18 + 0.025 * np.cos(t / 9)
    h4_v = 1 - h1_v - h2_v - h3_v
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(t, h1_c, label="H1 recursive-only")
    ax.plot(t, h2_c, label="H2 recursive-only")
    ax.plot(t, h3_c, label="H3 recursive-only")
    ax.plot(t, h1_v, linestyle="--", label="H1 with independent anchors")
    ax.plot(t, h2_v, linestyle="--", label="H2 with independent anchors")
    ax.plot(t, h3_v, linestyle="--", label="H3 with independent anchors")
    ax.set_ylim(0, 1)
    ax.set_xlabel("Learning / replay cycles")
    ax.set_ylabel("Route share")
    ax.set_title("MMALS functional collapse versus anchored host ecology (conceptual)")
    ax.grid(True, alpha=0.25)
    ax.legend(ncol=2)
    save(fig, "mmals_host_ecology")
    df = pd.DataFrame({
        "cycle": t,
        "H1_recursive": h1_c,
        "H2_recursive": h2_c,
        "H3_recursive": h3_c,
        "H4_recursive": h4_c,
        "H1_anchored": h1_v,
        "H2_anchored": h2_v,
        "H3_anchored": h3_v,
        "H4_anchored": h4_v,
    })
    df.to_csv(DATA / "mmals_host_ecology.csv", index=False)
    return df


def evidence_passport() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    ax.set_axis_off()
    left = [
        (0.03, 0.72, "Real observations"),
        (0.03, 0.52, "Simulation / digital twin"),
        (0.03, 0.32, "Generative candidates"),
        (0.03, 0.12, "Human / expert evidence"),
    ]
    for x, y, text in left:
        p = FancyBboxPatch((x, y), 0.22, 0.12, boxstyle="round,pad=0.012", facecolor="white")
        ax.add_patch(p)
        ax.text(x+0.11, y+0.06, text, ha="center", va="center")
        ax.add_patch(FancyArrowPatch((x+0.225, y+0.06), (0.37, 0.50), arrowstyle="-|>", mutation_scale=13, alpha=0.8))
    center = FancyBboxPatch((0.37, 0.34), 0.27, 0.32, boxstyle="round,pad=0.02", facecolor="white", linewidth=1.5)
    ax.add_patch(center)
    ax.text(0.505, 0.59, "Evidence Passport", ha="center", va="center", fontsize=13, weight="bold")
    fields = ["lineage", "freshness", "independence", "verification", "tail coverage", "permitted claim"]
    for i, f in enumerate(fields):
        ax.text(0.41 + (i%2)*0.13, 0.51 - (i//2)*0.075, f"• {f}", fontsize=9)
    ax.add_patch(FancyArrowPatch((0.65, 0.50), (0.78, 0.50), arrowstyle="-|>", mutation_scale=15))
    right = FancyBboxPatch((0.79, 0.31), 0.18, 0.38, boxstyle="round,pad=0.018", facecolor="white", linewidth=1.5)
    ax.add_patch(right)
    ax.text(0.88, 0.61, "STRAT-Q / MTP", ha="center", fontsize=12, weight="bold")
    ax.text(0.88, 0.51, "claim support", ha="center")
    ax.text(0.88, 0.44, "residual risk", ha="center")
    ax.text(0.88, 0.37, "decision", ha="center")
    ax.text(0.50, 0.86, "Trust is claim-relative: provenance is necessary but not sufficient", ha="center", fontsize=13, weight="bold")
    save(fig, "evidence_passport")


def audience_ladder() -> None:
    fig, ax = plt.subplots(figsize=(9.8, 4.1))
    ax.set_axis_off()
    levels = [
        (0.04, 0.16, 0.27, 0.56, "12-year-old track", "Stories, long tails, copies of copies,\nwhy a referee matters"),
        (0.365, 0.16, 0.27, 0.56, "Engineer track", "Failure modes, sampling, governance,\nmetrics, cost and deployment"),
        (0.69, 0.16, 0.27, 0.56, "PhD / research track", "Scaling exponents, kernel ridge,\nrecursive error and verification theory"),
    ]
    for x, y, w, h, title, body in levels:
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.018", facecolor="white", linewidth=1.4)
        ax.add_patch(p)
        ax.text(x+w/2, y+h*0.72, title, ha="center", fontsize=12, weight="bold")
        ax.text(x+w/2, y+h*0.39, body, ha="center", va="center", fontsize=9)
    ax.text(0.5, 0.88, "One lecture, three reading depths", ha="center", fontsize=14, weight="bold")
    save(fig, "audience_ladder")


def collaboration_network() -> None:
    G = nx.Graph()
    people = ["Julia Kempe", "Elvis Dohmatob", "Yunzhen Feng", "Pu Yang", "Francois Charton", "Arjun Subramonian"]
    orgs = ["NYU CDS / Courant", "Meta FAIR", "Peking University", "IHES lecture ecosystem", "FoRT"]
    G.add_nodes_from(people, bipartite=0)
    G.add_nodes_from(orgs, bipartite=1)
    edges = [
        ("Julia Kempe", "NYU CDS / Courant"), ("Julia Kempe", "Meta FAIR"), ("Julia Kempe", "FoRT"),
        ("Elvis Dohmatob", "Meta FAIR"), ("Yunzhen Feng", "NYU CDS / Courant"), ("Yunzhen Feng", "Meta FAIR"),
        ("Pu Yang", "Peking University"), ("Pu Yang", "Meta FAIR"), ("Francois Charton", "Meta FAIR"),
        ("Arjun Subramonian", "Meta FAIR"), ("Julia Kempe", "IHES lecture ecosystem"),
    ]
    G.add_edges_from(edges)
    # collaboration paper edges
    paper_pairs = [
        ("Julia Kempe", "Elvis Dohmatob"), ("Julia Kempe", "Yunzhen Feng"), ("Julia Kempe", "Pu Yang"),
        ("Julia Kempe", "Francois Charton"), ("Julia Kempe", "Arjun Subramonian"),
        ("Elvis Dohmatob", "Yunzhen Feng"), ("Elvis Dohmatob", "Pu Yang"), ("Elvis Dohmatob", "Francois Charton"),
        ("Yunzhen Feng", "Pu Yang"), ("Yunzhen Feng", "Francois Charton"),
    ]
    G.add_edges_from(paper_pairs)
    pos = {
        "Julia Kempe": (0.50, 0.52),
        "Elvis Dohmatob": (0.18, 0.72),
        "Yunzhen Feng": (0.25, 0.30),
        "Pu Yang": (0.73, 0.22),
        "Francois Charton": (0.80, 0.68),
        "Arjun Subramonian": (0.52, 0.87),
        "NYU CDS / Courant": (0.06, 0.18),
        "Meta FAIR": (0.94, 0.46),
        "Peking University": (0.86, 0.05),
        "IHES lecture ecosystem": (0.08, 0.92),
        "FoRT": (0.62, 0.03),
    }
    fig, ax = plt.subplots(figsize=(9.8, 5.3))
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.35, width=1.0)
    nx.draw_networkx_nodes(G, pos, nodelist=people, node_size=1700, node_shape="o", ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=orgs, node_size=2100, node_shape="s", ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8.5, ax=ax)
    ax.set_title("Julia Kempe's synthetic-data collaboration environment (selected, not exhaustive)")
    ax.set_axis_off()
    save(fig, "julia_collaboration_network")


def research_roadmap() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    ax.set_axis_off()
    cols = [0.04, 0.28, 0.52, 0.76]
    titles = ["Foundation", "Controlled experiments", "Integrated systems", "Qualification"]
    bodies = [
        "Reproduce tails, mixing,\nrecursive regression, verification",
        "MMALS route-tail tests;\nMTP evidence weighting;\nbiometric synthetic controls",
        "Joint memory-lineage state;\ndynamic compute; geometric\nuncertainty and control",
        "Independent real anchors;\ncausal ablations; reviewer\nclaims and deployment limits",
    ]
    for x, title, body in zip(cols, titles, bodies):
        p = FancyBboxPatch((x, 0.27), 0.19, 0.44, boxstyle="round,pad=0.015", facecolor="white", linewidth=1.4)
        ax.add_patch(p)
        ax.text(x+0.095, 0.61, title, ha="center", fontsize=11, weight="bold")
        ax.text(x+0.095, 0.45, body, ha="center", va="center", fontsize=9)
    for i in range(3):
        ax.add_patch(FancyArrowPatch((cols[i]+0.195, 0.49), (cols[i+1]-0.008, 0.49), arrowstyle="-|>", mutation_scale=15))
    ax.text(0.5, 0.88, "Research orientation: from lecture analysis to qualified evidence", ha="center", fontsize=14, weight="bold")
    ax.text(0.5, 0.13, "Principle: local simplicity, global functional diversity, and independent verification", ha="center", fontsize=11)
    save(fig, "research_roadmap")


def main() -> None:
    scaling_cutoff()
    real_synthetic_mix()
    recursive_regression()
    verification_bootstrap()
    mmals_ecology()
    evidence_passport()
    audience_ladder()
    collaboration_network()
    research_roadmap()
    print(f"Generated figures in {FIG}")


if __name__ == "__main__":
    main()
