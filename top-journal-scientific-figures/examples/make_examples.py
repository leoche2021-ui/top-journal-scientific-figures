"""Generate example figures for the top-journal-scientific-figures skill."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from journal_style import (  # noqa: E402
    DESIGN,
    add_panel_label,
    apply_axis_style,
    plot_bar_scatter,
    plot_mean_sd_line,
    save_publication_figure,
    setup_publication_style,
)


def stars(p_value: float) -> str:
    if p_value < 0.0001:
        return "****"
    if p_value < 0.001:
        return "***"
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return ""


def make_biomedical_example(outdir: Path) -> None:
    setup_publication_style()
    rng = np.random.default_rng(7)

    concentrations = np.array([0.3, 1, 3, 10, 30, 100])
    base = np.array([101, 98, 92, 73, 48, 22])
    viability = np.vstack([base + rng.normal(0, 4, len(base)) for _ in range(4)])

    groups = ["Vehicle", "Low", "Mid", "High"]
    apoptosis = np.array(
        [
            [4.8, 12.1, 28.2, 51.0],
            [5.1, 13.8, 31.4, 48.7],
            [4.3, 11.5, 30.1, 53.2],
            [5.4, 12.9, 29.3, 50.4],
        ]
    )

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.8))

    plot_mean_sd_line(
        axes[0],
        concentrations,
        viability,
        xlabel="Concentration (nM)",
        ylabel="Cell viability (%)",
    )
    axes[0].set_xscale("log")
    axes[0].set_ylim(0, 120)
    add_panel_label(axes[0], "a")

    plot_bar_scatter(
        axes[1],
        apoptosis,
        groups,
        color=DESIGN.palette[1],
        ylabel="Apoptotic cells (%)",
        rotate_labels=False,
    )
    axes[1].set_ylim(0, 65)
    y = 58
    axes[1].plot([0, 0, 3, 3], [y - 2, y, y, y - 2], color="black", lw=0.8)
    axes[1].text(1.5, y + 1.5, stars(0.0006), ha="center", va="bottom", fontsize=8, style="italic")
    add_panel_label(axes[1], "b")

    fig.subplots_adjust(left=0.09, right=0.98, bottom=0.2, top=0.9, wspace=0.42)
    save_publication_figure(fig, outdir / "example_biomedical")
    plt.close(fig)


def make_omics_example(outdir: Path) -> None:
    setup_publication_style()
    rng = np.random.default_rng(11)

    n = 450
    log2_fc = rng.normal(0, 1.15, n)
    neg_log10_q = np.clip(rng.gamma(1.7, 1.1, n), 0, 7)
    significant = (np.abs(log2_fc) > 1.0) & (neg_log10_q > 1.3)

    expression = rng.normal(0, 0.7, (18, 8))
    expression[:6, :4] += 1.1
    expression[6:12, 4:] -= 1.0
    expression = np.clip(expression, -2.2, 2.2)

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 3.0))

    ax = axes[0]
    apply_axis_style(ax, box_aspect=0.88)
    ax.scatter(log2_fc[~significant], neg_log10_q[~significant], s=8, color="#BAB0AC", alpha=0.75, lw=0)
    ax.scatter(log2_fc[significant], neg_log10_q[significant], s=9, color=DESIGN.palette[3], alpha=0.85, lw=0)
    ax.axvline(-1, color="black", lw=0.7, ls=":")
    ax.axvline(1, color="black", lw=0.7, ls=":")
    ax.axhline(1.3, color="black", lw=0.7, ls=":")
    ax.set_xlabel("log2 fold change", fontsize=DESIGN.axis_label_size)
    ax.set_ylabel("-log10 adjusted P", fontsize=DESIGN.axis_label_size)
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 7)
    add_panel_label(ax, "a")

    ax = axes[1]
    apply_axis_style(ax, box_aspect=0.88, hide_top_right=False)
    image = ax.imshow(expression, cmap="vlag" if "vlag" in plt.colormaps() else "coolwarm", vmin=-2.2, vmax=2.2, aspect="auto")
    ax.set_xticks(range(8))
    ax.set_xticklabels([f"S{i + 1}" for i in range(8)], fontsize=7)
    ax.set_yticks([0, 5, 11, 17])
    ax.set_yticklabels(["Gene 1", "Gene 6", "Gene 12", "Gene 18"], fontsize=7)
    cbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.035)
    cbar.set_label("z-score", fontsize=7.5)
    cbar.ax.tick_params(labelsize=7, width=0.7, length=2.5)
    add_panel_label(ax, "b")

    fig.subplots_adjust(left=0.08, right=0.94, bottom=0.17, top=0.92, wspace=0.55)
    save_publication_figure(fig, outdir / "example_omics")
    plt.close(fig)


def make_ml_clinical_example(outdir: Path) -> None:
    setup_publication_style()

    recall = np.array([0.02, 0.12, 0.25, 0.41, 0.58, 0.74, 0.87, 0.96, 1.00])
    precision = np.array([0.94, 0.91, 0.88, 0.82, 0.76, 0.63, 0.49, 0.34, 0.21])
    predicted = np.linspace(0.05, 0.95, 10)
    observed = np.array([0.04, 0.10, 0.17, 0.26, 0.38, 0.51, 0.62, 0.75, 0.84, 0.91])

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.8))

    ax = axes[0]
    apply_axis_style(ax, box_aspect=0.86)
    ax.plot(recall, precision, color="black", lw=1.2)
    ax.scatter(recall, precision, s=14, color=DESIGN.palette[0], edgecolor="black", linewidth=0.35, zorder=3)
    ax.set_xlabel("Recall", fontsize=DESIGN.axis_label_size)
    ax.set_ylabel("Precision", fontsize=DESIGN.axis_label_size)
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 1.02)
    add_panel_label(ax, "a")

    ax = axes[1]
    apply_axis_style(ax, box_aspect=0.86)
    ax.plot([0, 1], [0, 1], color="#777777", lw=0.9, ls="--")
    ax.plot(predicted, observed, color="black", lw=1.1)
    ax.scatter(predicted, observed, s=16, color=DESIGN.palette[2], edgecolor="black", linewidth=0.35, zorder=3)
    ax.set_xlabel("Predicted risk", fontsize=DESIGN.axis_label_size)
    ax.set_ylabel("Observed risk", fontsize=DESIGN.axis_label_size)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    add_panel_label(ax, "b")

    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.19, top=0.9, wspace=0.42)
    save_publication_figure(fig, outdir / "example_ml_clinical")
    plt.close(fig)


def add_sig_bar(ax: plt.Axes, x0: float, x1: float, y: float, text: str) -> None:
    ax.plot([x0, x0, x1, x1], [y - 1.8, y, y, y - 1.8], color="black", lw=0.8)
    ax.text((x0 + x1) / 2, y + 1.2, text, ha="center", va="bottom", fontsize=8, style="italic")


def make_complex_combined_example(outdir: Path) -> None:
    setup_publication_style()
    rng = np.random.default_rng(29)

    fig = plt.figure(figsize=(7.2, 9.2))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.0, 1.05, 1.0], wspace=0.48, hspace=0.64)

    # a: biomedical dose response with two conditions and replicate-level points.
    ax = fig.add_subplot(gs[0, 0])
    apply_axis_style(ax, box_aspect=0.78)
    concentrations = np.array([0.1, 0.3, 1, 3, 10, 30, 100])
    curves = {
        "Cell line A": (np.array([101, 99, 94, 79, 56, 31, 15]), DESIGN.palette[0]),
        "Cell line B": (np.array([103, 101, 98, 89, 71, 49, 25]), DESIGN.palette[1]),
    }
    for label, (base, color) in curves.items():
        reps = np.vstack([base + rng.normal(0, 3.0, len(base)) for _ in range(4)])
        mean = reps.mean(axis=0)
        sd = reps.std(axis=0, ddof=1)
        ax.fill_between(concentrations, mean - sd, mean + sd, color=color, alpha=0.18, lw=0)
        ax.plot(concentrations, mean, color="black", lw=1.05)
        ax.scatter(concentrations, mean, s=16, color=color, edgecolor="black", linewidth=0.35, zorder=4, label=label)
        for row in reps:
            ax.scatter(concentrations, row, s=6, color=color, alpha=0.35, lw=0, zorder=2)
    ax.axhline(50, color="#666666", lw=0.75, ls=":")
    ax.set_xscale("log")
    ax.set_ylim(0, 120)
    ax.set_xlabel("Concentration (nM)", fontsize=DESIGN.axis_label_size)
    ax.set_ylabel("Cell viability (%)", fontsize=DESIGN.axis_label_size)
    ax.legend(loc="upper right", fontsize=7, handlelength=1.0, borderpad=0.2)
    add_panel_label(ax, "a")

    # b: response phenotype summary with aligned replicates and selected significance.
    ax = fig.add_subplot(gs[0, 1])
    apoptosis = np.array(
        [
            [5.0, 13.2, 30.1, 52.6],
            [4.4, 14.8, 28.7, 50.9],
            [5.5, 12.6, 31.5, 54.1],
            [4.9, 13.9, 29.8, 51.4],
        ]
    )
    plot_bar_scatter(
        ax,
        apoptosis,
        ["Veh.", "Low", "Mid", "High"],
        color=DESIGN.palette[1],
        ylabel="Apoptotic cells (%)",
    )
    ax.set_ylim(0, 68)
    add_sig_bar(ax, 0, 2, 55, stars(0.004))
    add_sig_bar(ax, 0, 3, 63, stars(0.0002))
    add_panel_label(ax, "b")

    # c: volcano plot with thresholds and labeled leading features.
    ax = fig.add_subplot(gs[1, 0])
    apply_axis_style(ax, box_aspect=0.86)
    n = 900
    log2_fc = rng.normal(0, 1.1, n)
    neg_log10_q = np.clip(rng.gamma(1.55, 1.05, n), 0, 8)
    up = (log2_fc > 1.0) & (neg_log10_q > 1.3)
    down = (log2_fc < -1.0) & (neg_log10_q > 1.3)
    ax.scatter(log2_fc[~(up | down)], neg_log10_q[~(up | down)], s=7, color="#BDB8B3", alpha=0.62, lw=0)
    ax.scatter(log2_fc[down], neg_log10_q[down], s=8, color=DESIGN.palette[0], alpha=0.82, lw=0)
    ax.scatter(log2_fc[up], neg_log10_q[up], s=8, color=DESIGN.palette[3], alpha=0.82, lw=0)
    ax.axvline(-1, color="black", lw=0.65, ls=":")
    ax.axvline(1, color="black", lw=0.65, ls=":")
    ax.axhline(1.3, color="black", lw=0.65, ls=":")
    for name, xy in {"CXCL8": (2.55, 6.5), "MKI67": (1.95, 5.4), "IL7R": (-2.25, 5.8)}.items():
        ax.scatter([xy[0]], [xy[1]], s=18, color="black", lw=0, zorder=5)
        ax.text(xy[0] + 0.1, xy[1] + 0.08, name, fontsize=7.2, ha="left", va="bottom")
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(0, 8)
    ax.set_xlabel("log2 fold change", fontsize=DESIGN.axis_label_size)
    ax.set_ylabel("-log10 adjusted P", fontsize=DESIGN.axis_label_size)
    add_panel_label(ax, "c")

    # d: expression heatmap with compact sample annotations.
    ax = fig.add_subplot(gs[1, 1])
    apply_axis_style(ax, box_aspect=0.86, hide_top_right=False)
    expression = rng.normal(0, 0.55, (24, 10))
    expression[:8, :5] += 1.15
    expression[8:16, 5:] -= 1.05
    expression[16:, 2:8] += 0.55
    expression = np.clip(expression, -2.2, 2.2)
    image = ax.imshow(expression, cmap="coolwarm", vmin=-2.2, vmax=2.2, aspect="auto")
    ax.set_xticks(range(10))
    ax.set_xticklabels([f"S{i + 1}" for i in range(10)], fontsize=6.7)
    ax.set_yticks([0, 7, 15, 23])
    ax.set_yticklabels(["G1", "G8", "G16", "G24"], fontsize=6.7)
    ax.tick_params(length=0)
    annotation = ax.inset_axes([0, 1.02, 1, 0.06])
    annotation.imshow(np.array([[0] * 5 + [1] * 5]), cmap=ListedColormap([DESIGN.palette[0], DESIGN.palette[3]]), aspect="auto")
    annotation.set_axis_off()
    cbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.035)
    cbar.set_label("z-score", fontsize=7.2)
    cbar.ax.tick_params(labelsize=6.8, width=0.7, length=2.4)
    add_panel_label(ax, "d")

    # e: model precision-recall curves across three candidate models.
    ax = fig.add_subplot(gs[2, 0])
    apply_axis_style(ax, box_aspect=0.82)
    recall = np.linspace(0.02, 1.0, 13)
    model_curves = {
        "Model 1": (0.92 - 0.58 * recall**1.6, DESIGN.palette[0]),
        "Model 2": (0.88 - 0.50 * recall**1.35, DESIGN.palette[2]),
        "Clinical": (0.80 - 0.47 * recall**1.2, "#6F6F6F"),
    }
    for label, (precision, color) in model_curves.items():
        precision = np.clip(precision + rng.normal(0, 0.012, len(recall)), 0.16, 0.96)
        ax.plot(recall, precision, color=color if label != "Clinical" else "black", lw=1.05, label=label)
        ax.scatter(recall[::2], precision[::2], s=12, color=color, edgecolor="black", linewidth=0.3, zorder=3)
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0.15, 1.02)
    ax.set_xlabel("Recall", fontsize=DESIGN.axis_label_size)
    ax.set_ylabel("Precision", fontsize=DESIGN.axis_label_size)
    ax.legend(loc="upper right", fontsize=7, handlelength=1.2, borderpad=0.2)
    add_panel_label(ax, "e")

    # f: calibration with binomial-style uncertainty intervals.
    ax = fig.add_subplot(gs[2, 1])
    apply_axis_style(ax, box_aspect=0.82)
    predicted = np.linspace(0.06, 0.94, 9)
    observed = np.clip(predicted * 0.92 + np.array([-0.01, 0.02, -0.01, 0.015, 0.03, 0.005, -0.02, 0.015, -0.015]), 0, 1)
    err = np.array([0.035, 0.04, 0.045, 0.05, 0.052, 0.055, 0.06, 0.062, 0.065])
    ax.plot([0, 1], [0, 1], color="#777777", lw=0.85, ls="--")
    ax.errorbar(
        predicted,
        observed,
        yerr=err,
        fmt="o-",
        color="black",
        markerfacecolor=DESIGN.palette[2],
        markeredgecolor="black",
        markeredgewidth=0.35,
        markersize=3.6,
        linewidth=1.05,
        elinewidth=0.75,
        capsize=2,
        zorder=3,
    )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Predicted risk", fontsize=DESIGN.axis_label_size)
    ax.set_ylabel("Observed risk", fontsize=DESIGN.axis_label_size)
    add_panel_label(ax, "f")

    fig.text(0.02, 0.955, "Biomedical response", fontsize=8.5, fontweight="bold", ha="left", va="center")
    fig.text(0.02, 0.635, "Transcriptomic profile", fontsize=8.5, fontweight="bold", ha="left", va="center")
    fig.text(0.02, 0.315, "Clinical model evaluation", fontsize=8.5, fontweight="bold", ha="left", va="center")
    fig.subplots_adjust(left=0.11, right=0.96, bottom=0.065, top=0.94)
    save_publication_figure(fig, outdir / "example_complex_combined")
    plt.close(fig)


def gaussian(x: np.ndarray, center: float, width: float, height: float) -> np.ndarray:
    return height * np.exp(-0.5 * ((x - center) / width) ** 2)


def make_materials_science_example(outdir: Path) -> None:
    setup_publication_style()
    rng = np.random.default_rng(43)

    fig = plt.figure(figsize=(7.2, 5.7))
    gs = fig.add_gridspec(2, 2, wspace=0.46, hspace=0.58)

    # a: XRD patterns with offset traces and indexed reflections.
    ax = fig.add_subplot(gs[0, 0])
    apply_axis_style(ax, box_aspect=0.78)
    two_theta = np.linspace(10, 80, 1400)
    peak_positions = [18.7, 31.3, 36.8, 44.6, 55.2, 59.0, 65.1]
    offsets = [0, 1.05, 2.1]
    labels = ["Pristine", "Doped", "Annealed"]
    colors = ["#6F6F6F", DESIGN.palette[0], DESIGN.palette[3]]
    for idx, (offset, label, color) in enumerate(zip(offsets, labels, colors)):
        intensity = np.zeros_like(two_theta) + 0.06
        for pos in peak_positions:
            intensity += gaussian(two_theta, pos + idx * 0.08, 0.22 + 0.03 * idx, 0.55 + 0.08 * idx)
        intensity += 0.015 * rng.normal(size=len(two_theta))
        ax.plot(two_theta, intensity + offset, color=color if idx else "black", lw=0.95)
        ax.text(79.0, offset + 0.18, label, fontsize=7.2, ha="right", va="center")
    for pos, hkl in zip([31.3, 36.8, 44.6], ["(220)", "(311)", "(400)"]):
        ax.text(pos, 3.12, hkl, fontsize=6.8, rotation=90, ha="center", va="bottom")
    ax.set_xlabel(r"2$\theta$ (degree)", fontsize=DESIGN.axis_label_size)
    ax.set_ylabel("Intensity (a.u.)", fontsize=DESIGN.axis_label_size)
    ax.set_xlim(10, 80)
    ax.set_ylim(-0.05, 3.45)
    ax.set_yticklabels([])
    add_panel_label(ax, "a")

    # b: UV-vis absorption and Tauc-style inset.
    ax = fig.add_subplot(gs[0, 1])
    apply_axis_style(ax, box_aspect=0.78)
    wavelength = np.linspace(350, 850, 500)
    absorption_a = 0.18 + 0.95 / (1 + np.exp((wavelength - 610) / 35)) + 0.03 * np.sin(wavelength / 35)
    absorption_b = 0.14 + 1.05 / (1 + np.exp((wavelength - 655) / 42)) + 0.025 * np.cos(wavelength / 37)
    ax.plot(wavelength, absorption_a, color="black", lw=1.05, label="Pristine")
    ax.plot(wavelength, absorption_b, color=DESIGN.palette[0], lw=1.05, label="Doped")
    ax.set_xlabel("Wavelength (nm)", fontsize=DESIGN.axis_label_size)
    ax.set_ylabel("Absorbance (a.u.)", fontsize=DESIGN.axis_label_size)
    ax.set_xlim(350, 850)
    ax.set_ylim(0, 1.35)
    ax.legend(loc="upper right", fontsize=7, handlelength=1.2, borderpad=0.2)
    inset = ax.inset_axes([0.52, 0.18, 0.42, 0.38])
    hv = np.linspace(1.5, 3.1, 120)
    tauc = np.clip(hv - 2.08, 0, None) ** 2 * 2.0
    inset.plot(hv, tauc, color="black", lw=0.9)
    inset.axvline(2.08, color=DESIGN.palette[3], lw=0.75, ls=":")
    inset.set_xlabel("hν (eV)", fontsize=6.4)
    inset.set_ylabel(r"$(\alpha h\nu)^2$", fontsize=6.4)
    inset.tick_params(labelsize=6, width=0.6, length=2, direction="out")
    for spine in inset.spines.values():
        spine.set_linewidth(0.65)
    add_panel_label(ax, "b")

    # c: particle size distribution with median and quartile guide lines.
    ax = fig.add_subplot(gs[1, 0])
    apply_axis_style(ax, box_aspect=0.82)
    sizes = rng.lognormal(mean=np.log(72), sigma=0.28, size=420)
    bins = np.linspace(20, 170, 26)
    ax.hist(sizes, bins=bins, color=DESIGN.palette[2], edgecolor="black", linewidth=0.45, alpha=0.7, density=True)
    xs = np.linspace(20, 170, 300)
    mu = np.log(np.median(sizes))
    sigma = np.std(np.log(sizes))
    pdf = np.exp(-((np.log(xs) - mu) ** 2) / (2 * sigma**2)) / (xs * sigma * np.sqrt(2 * np.pi))
    ax.plot(xs, pdf, color="black", lw=1.05)
    for value, line_style in zip(np.percentile(sizes, [25, 50, 75]), [":", "-", ":"]):
        ax.axvline(value, color="#555555", lw=0.75, ls=line_style)
    ax.text(0.97, 0.9, f"median = {np.median(sizes):.0f} nm", transform=ax.transAxes, fontsize=7.2, ha="right", va="top")
    ax.set_xlabel("Particle diameter (nm)", fontsize=DESIGN.axis_label_size)
    ax.set_ylabel("Density", fontsize=DESIGN.axis_label_size)
    ax.set_xlim(20, 170)
    add_panel_label(ax, "c")

    # d: cycling performance and Coulombic efficiency.
    ax = fig.add_subplot(gs[1, 1])
    apply_axis_style(ax, box_aspect=0.82)
    cycles = np.arange(1, 201)
    capacity = 148 - 0.085 * cycles + 3.4 * np.exp(-cycles / 18) + rng.normal(0, 0.75, len(cycles))
    efficiency = 98.6 + 0.9 * (1 - np.exp(-cycles / 30)) + rng.normal(0, 0.07, len(cycles))
    ax.plot(cycles, capacity, color="black", lw=1.05)
    ax.scatter(cycles[::10], capacity[::10], s=12, color=DESIGN.palette[0], edgecolor="black", linewidth=0.3, zorder=3)
    ax.set_xlabel("Cycle number", fontsize=DESIGN.axis_label_size)
    ax.set_ylabel(r"Capacity (mAh g$^{-1}$)", fontsize=DESIGN.axis_label_size)
    ax.set_xlim(0, 205)
    ax.set_ylim(120, 155)
    ax2 = ax.twinx()
    ax2.plot(cycles, efficiency, color=DESIGN.palette[3], lw=0.95)
    ax2.set_ylabel("Coulombic efficiency (%)", fontsize=DESIGN.axis_label_size)
    ax2.set_ylim(97.5, 100.2)
    ax2.tick_params(labelsize=DESIGN.tick_label_size, width=DESIGN.tick_width, length=DESIGN.tick_length, direction="out")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_linewidth(DESIGN.axis_linewidth)
    ax.text(0.05, 0.12, "1 C, 25 degC", transform=ax.transAxes, fontsize=7.2, ha="left", va="bottom")
    add_panel_label(ax, "d")

    fig.text(0.03, 0.965, "Materials characterization and device performance", fontsize=9, fontweight="bold", ha="left", va="center")
    fig.subplots_adjust(left=0.09, right=0.91, bottom=0.095, top=0.91)
    save_publication_figure(fig, outdir / "example_materials_science")
    plt.close(fig)


def main() -> None:
    outdir = Path(__file__).resolve().parent / "outputs"
    outdir.mkdir(exist_ok=True)
    make_biomedical_example(outdir)
    make_omics_example(outdir)
    make_ml_clinical_example(outdir)
    make_complex_combined_example(outdir)
    make_materials_science_example(outdir)


if __name__ == "__main__":
    main()
