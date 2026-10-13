"""Reusable Matplotlib helpers for publication-ready scientific figures."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


@dataclass
class JournalDesign:
    dpi: int = 600
    figsize_one_col: tuple[float, float] = (3.35, 2.6)
    figsize_one_half_col: tuple[float, float] = (5.2, 3.6)
    figsize_two_col: tuple[float, float] = (7.1, 4.8)
    panel_aspect: float = 0.78
    wspace: float = 0.28
    hspace: float = 0.38
    font_family: list[str] = field(
        default_factory=lambda: ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"]
    )
    axis_label_size: float = 8.5
    tick_label_size: float = 7.5
    title_size: float = 8.5
    panel_label_size: float = 11.0
    annotation_size: float = 7.5
    axis_linewidth: float = 0.8
    tick_width: float = 0.8
    tick_length: float = 3.0
    curve_linewidth: float = 1.1
    errorbar_linewidth: float = 0.8
    errorbar_capsize: float = 2.0
    marker_size: float = 14.0
    line_marker_size: float = 3.2
    bar_width: float = 0.62
    bar_alpha: float = 0.62
    palette: tuple[str, ...] = (
        "#4C78A8",
        "#B279A2",
        "#59A14F",
        "#E15759",
        "#9C755F",
        "#76B7B2",
        "#BAB0AC",
    )


DESIGN = JournalDesign()


def setup_publication_style(design: JournalDesign = DESIGN) -> None:
    """Set global Matplotlib defaults for editable vector publication figures."""
    mpl.rcParams["font.family"] = "sans-serif"
    mpl.rcParams["font.sans-serif"] = design.font_family
    mpl.rcParams["svg.fonttype"] = "none"
    mpl.rcParams["pdf.fonttype"] = 42
    mpl.rcParams["ps.fonttype"] = 42
    mpl.rcParams["figure.dpi"] = design.dpi
    mpl.rcParams["savefig.dpi"] = design.dpi
    mpl.rcParams["axes.linewidth"] = design.axis_linewidth
    mpl.rcParams["axes.unicode_minus"] = False
    mpl.rcParams["axes.grid"] = False
    mpl.rcParams["legend.frameon"] = False


def apply_axis_style(
    ax: plt.Axes,
    design: JournalDesign = DESIGN,
    *,
    box_aspect: Optional[float] = None,
    preserve_aspect: bool = False,
    hide_top_right: bool = True,
) -> None:
    """Apply restrained top-journal axis styling to one axes."""
    if not preserve_aspect:
        ax.set_box_aspect(design.panel_aspect if box_aspect is None else box_aspect)
    ax.tick_params(
        labelsize=design.tick_label_size,
        width=design.tick_width,
        length=design.tick_length,
        direction="out",
        color="black",
    )

    for name, spine in ax.spines.items():
        spine.set_linewidth(design.axis_linewidth)
        spine.set_color("black")
        if hide_top_right and name in {"top", "right"}:
            spine.set_visible(False)


def add_panel_label(
    ax: plt.Axes,
    label: str,
    design: JournalDesign = DESIGN,
    *,
    x: float = -0.18,
    y: float = 1.04,
) -> None:
    """Add a compact bold panel label such as a, b, c, or d."""
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=design.panel_label_size,
        fontweight="bold",
        color="black",
    )


def mean_sd(values: Sequence[Sequence[float]], axis: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Return mean and sample SD for replicate data."""
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 2 or np.isinf(arr).any():
        raise ValueError("Expected a two-dimensional replicate matrix without infinity")
    n = np.sum(~np.isnan(arr), axis=axis)
    if np.any(n == 0):
        raise ValueError("Cannot summarize an empty group")
    mean = np.nansum(arr, axis=axis) / n
    centered = arr - np.expand_dims(mean, axis)
    sums = np.nansum(centered ** 2, axis=axis)
    sd = np.sqrt(np.divide(sums, n - 1, out=np.full_like(mean, np.nan), where=n > 1))
    return mean, sd


def plot_bar_scatter(
    ax: plt.Axes,
    values_matrix: Sequence[Sequence[float]],
    labels: Sequence[str],
    *,
    color: str | None = None,
    ylabel: str = "",
    xlabel: str = "",
    title: Optional[str] = None,
    rotate_labels: bool = False,
    design: JournalDesign = DESIGN,
) -> None:
    """Draw bar + vertically aligned replicate points for small-n experiments."""
    apply_axis_style(ax, design)
    values = np.asarray(values_matrix, dtype=float)
    mean, sd = mean_sd(values, axis=0)
    if values.shape[1] != len(labels):
        raise ValueError("Group labels must match matrix columns")
    x = np.arange(len(labels))

    ax.bar(
        x,
        mean,
        yerr=sd,
        width=design.bar_width,
        color=color or design.palette[0],
        alpha=design.bar_alpha,
        edgecolor="black",
        linewidth=design.axis_linewidth,
        capsize=design.errorbar_capsize,
        error_kw={"elinewidth": design.errorbar_linewidth, "ecolor": "black"},
        zorder=2,
    )

    for idx in range(values.shape[1]):
        vals = values[:, idx]
        vals = vals[~np.isnan(vals)]
        ax.scatter(
            x[idx] + np.random.default_rng(idx).uniform(-0.065, 0.065, len(vals)),
            vals,
            s=design.marker_size,
            color="black",
            linewidths=0,
            zorder=4,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45 if rotate_labels else 0, ha="right" if rotate_labels else "center")
    ax.set_xlabel(xlabel, fontsize=design.axis_label_size)
    ax.set_ylabel(ylabel, fontsize=design.axis_label_size)
    if title:
        ax.set_title(title, fontsize=design.title_size, pad=5)


def plot_mean_sd_line(
    ax: plt.Axes,
    x: Sequence[float],
    values_matrix: Sequence[Sequence[float]],
    *,
    ylabel: str = "",
    xlabel: str = "",
    title: Optional[str] = None,
    color: str = "black",
    design: JournalDesign = DESIGN,
) -> None:
    """Draw a line plot with mean +/- SD across replicate rows."""
    apply_axis_style(ax, design)
    mean, sd = mean_sd(values_matrix, axis=0)
    if len(x) != len(mean):
        raise ValueError("x must match the number of columns")
    ax.errorbar(
        x,
        mean,
        yerr=sd,
        fmt="o-",
        color=color,
        markersize=design.line_marker_size,
        linewidth=design.curve_linewidth,
        elinewidth=design.errorbar_linewidth,
        capsize=design.errorbar_capsize,
        zorder=3,
    )
    ax.set_xlabel(xlabel, fontsize=design.axis_label_size)
    ax.set_ylabel(ylabel, fontsize=design.axis_label_size)
    if title:
        ax.set_title(title, fontsize=design.title_size, pad=5)


def save_publication_figure(
    fig: plt.Figure,
    basename: str | Path,
    *,
    dpi: int = DESIGN.dpi,
    formats: Iterable[str] = ("svg", "pdf", "png"),
    tight: bool = False,
) -> list[Path]:
    """Save a figure in vector and raster formats."""
    base = Path(basename)
    base.parent.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for ext in formats:
        path = base.with_suffix(f".{ext}")
        kwargs = {"bbox_inches": "tight" if tight else None, "facecolor": "white"}
        if ext.lower() in {"png", "tif", "tiff", "jpg", "jpeg"}:
            kwargs["dpi"] = dpi
        fig.savefig(path, **kwargs)
        paths.append(path)
    return paths


def plot_dot_summary(ax, values_matrix, labels, *, paired=False, seed=0, design=DESIGN, ylabel=""):
    """Rows are confirmed experimental units; paired rows must refer to the same unit."""
    values = np.asarray(values_matrix, dtype=float)
    mean, sd = mean_sd(values)
    if values.shape[1] != len(labels):
        raise ValueError("Labels must match columns")
    apply_axis_style(ax, design)
    rng = np.random.default_rng(seed)
    offsets = rng.uniform(-0.07, 0.07, len(values))
    x = np.arange(len(labels))
    if paired:
        for row, offset in zip(values, offsets):
            # NaN breaks a line; never bridge missing observations.
            ax.plot(x + offset, row, color="0.7", lw=0.6, zorder=1)
    for i, label in enumerate(labels):
        valid = np.isfinite(values[:, i])
        ax.scatter(i + offsets[valid], values[valid, i], s=design.marker_size,
                   color=design.palette[i % len(design.palette)], zorder=3)
    ax.errorbar(x, mean, yerr=sd, fmt="_", color="black", markersize=10,
                capsize=design.errorbar_capsize, linewidth=design.errorbar_linewidth, zorder=4)
    ax.set_xticks(x, labels)
    ax.set_ylabel(ylabel, fontsize=design.axis_label_size)
    return {"n": np.sum(np.isfinite(values), axis=0).tolist(),
            "mean": mean.tolist(), "sd": [float(v) if np.isfinite(v) else None for v in sd]}
