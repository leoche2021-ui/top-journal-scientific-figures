# Style Tokens

Use these as starting values, then adapt to the dataset, journal width, and field conventions.

## Geometry

```python
DESIGN = {
    "dpi": 600,
    "figsize_one_col": (3.35, 2.6),
    "figsize_one_half_col": (5.2, 3.6),
    "figsize_two_col": (7.1, 4.8),
    "panel_aspect": 0.78,
    "wspace": 0.28,
    "hspace": 0.38,
}
```

Panel aspect guide:

- `0.60`: wide/flat, useful for time series, spectra, timelines.
- `0.70`: slightly flat, good for many biomedical panels.
- `0.78`: default top-journal balance.
- `0.85`: near square, good for scatter, PCA/UMAP, images.
- `1.00`: square, useful for correlation matrices, confusion matrices, some microscopy crops.

## Typography

```python
TYPOGRAPHY = {
    "font_family": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
    "axis_label_size": 8.5,
    "tick_label_size": 7.5,
    "title_size": 8.5,
    "panel_label_size": 11.0,
    "annotation_size": 7.5,
}
```

For large standalone figures, increase by 1-2 pt. For dense multi-panel figures, reduce only if labels remain readable at final export size.

## Lines, Markers, and Bars

```python
MARKS = {
    "axis_linewidth": 0.8,
    "tick_width": 0.8,
    "tick_length": 3.0,
    "curve_linewidth": 1.1,
    "errorbar_linewidth": 0.8,
    "errorbar_capsize": 2.0,
    "marker_size": 14,
    "line_marker_size": 3.2,
    "bar_width": 0.62,
    "bar_alpha": 0.62,
}
```

Use bars sparingly. When bars are used for small-n experiments, overlay all replicate points at the exact group x-coordinate unless there are enough points to require jitter.

## Palettes

Primary palette for groups:

```python
PALETTE = [
    "#4C78A8",  # muted blue
    "#B279A2",  # muted magenta
    "#59A14F",  # muted green
    "#E15759",  # muted red
    "#9C755F",  # muted brown
    "#76B7B2",  # muted teal
    "#BAB0AC",  # neutral gray
]
```

Use black for:

- Primary data points in small-n experiments.
- Fits and model curves.
- Error bars and confidence bands outlines.
- Axis text and key annotations.

Sequential maps:

- Viridis, cividis, or magma for ordered intensity.
- Avoid rainbow maps for quantitative heatmaps.
- Center diverging maps at a meaningful zero or baseline.

## Export

```python
import matplotlib as mpl

mpl.rcParams["svg.fonttype"] = "none"
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42

fig.savefig("figure.svg", bbox_inches=None)
fig.savefig("figure.pdf", bbox_inches=None)
fig.savefig("figure.png", dpi=600, bbox_inches=None)
```

Use TIFF when the journal requests it. Use SVG/PDF for Illustrator, Inkscape, Affinity Designer, or final manuscript assembly.


## Overrides and accessibility

These dimensions and colors are aesthetic presets, not verified journal requirements. Preserve native aspect ratios for images/maps/matrices. Use category colors consistently across figures, adding marker/line encodings where necessary; the listed palette is not certified color-blind safe. Check grayscale and a color vision simulation. Black curves are a default: colored curves can identify groups when scientific clarity benefits. Use deterministic jitter for repeated points; do not obscure n by stacking identical measurements.
