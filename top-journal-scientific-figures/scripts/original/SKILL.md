---
name: top-journal-scientific-figures
description: Use when creating, redesigning, critiquing, or coding scientific plots and multi-panel research figures with Nature, Science, Cell, Lancet, NEJM, PNAS, or other top-journal aesthetics across biology, medicine, chemistry, materials science, physics, engineering, earth science, omics, AI/ML, and quantitative social science. Use for manuscript figures, publication-ready charts, data visualization style systems, Matplotlib/ggplot figure scripts, figure polishing, and journal-style visual QA.
metadata:
  short-description: Publication-ready scientific figures
---

# Top-Journal Scientific Figures

Create research figures that are accurate, restrained, readable, and ready for manuscript assembly. The goal is not to imitate a single journal mechanically; it is to use the shared editorial language of high-impact scientific figures: clean structure, honest data display, precise labels, and quiet visual hierarchy.

## 中文信息

**中文名称**：顶刊科研图表美学与生成

**Skill ID**：`top-journal-scientific-figures`

**简介**：这是一个面向科研论文、基金申请、学术汇报和投稿前图件润色的科研可视化 skill。它帮助 Codex 按照 Nature、Science、Cell、The Lancet、NEJM、PNAS、JACS、Angew、Advanced Materials、Nature Materials 等高水平期刊中常见的审美逻辑，生成、重绘、审查和优化科研图表。它强调白底、细轴、低饱和配色、真实单位、可追溯数据、清晰统计标注、可编辑矢量导出，以及跨 panel 的视觉一致性。

**介绍**：这个 skill 的核心目标不是把所有图都机械地做成某一本期刊的模板，而是提炼顶刊科研图件背后的共通原则：让数据先被看见，让结论自然浮现，让审稿人和读者能快速判断图中变量、单位、样本量、误差来源和比较关系。它适合处理从单张实验图到复杂 multi-panel manuscript figure 的各种任务，包括 dose-response、bar + scatter、line + error、volcano plot、heatmap、PCA/UMAP、forest plot、ROC/PR curve、calibration plot、XRD、光谱、粒径分布、循环性能、时间序列、空间地图、模型评估和临床统计图等。

这个 skill 特别重视科研图的“可信度”。它会优先保留 replicate points，避免只给 mean bar；会区分 SD、SEM、CI 的不同含义；会提醒不要强行拟合 IC50/EC50、不要随意标注不支持的数据结论、不要发明 p-value、sample size、scale bar 或实验条件。对于小样本实验，它倾向于展示 individual points + mean/SD；对于高维数据，它强调阈值、色标、聚类方法和多重检验校正；对于临床和机器学习图，它会关注 calibration、class imbalance、confidence interval 和 subgroup performance；对于材料、化学和物理图，它会关注峰位标注、baseline、单位、offset trace、双 y 轴解释和测试条件。

在视觉风格上，这个 skill 使用克制、干净、可投稿的设计语言：白底、无阴影、无渐变、黑色细轴线、统一 sans-serif 字体、低饱和分组色、可读的 panel label、适当的留白和一致的 panel aspect ratio。它默认导出 SVG/PDF 以便在 Illustrator、Inkscape 或 Affinity Designer 中继续编辑，同时导出高分辨率 PNG/TIFF 供预览、汇报或投稿系统使用。

当用户给出真实数据、已有图、绘图脚本、Excel/CSV、论文 figure 草稿或审稿意见时，这个 skill 可以用于三类工作：第一，直接生成 publication-ready figure；第二，把已有图重绘成顶刊风格；第三，从审稿人视角检查图中是否存在标签错误、比例不一致、统计表达不清、颜色不可区分、字体过小、legend 冗余、panel 对齐差、数据可追溯性不足等问题。它既适合科研人员快速做出漂亮且严谨的图，也适合把已经完成的数据分析包装成更有说服力的论文图件。

## Core Workflow

1. Identify the scientific claim, audience, target journal family, field, figure type, and output format.
2. Inspect the data structure before plotting. Preserve raw replicates, units, sample sizes, missing values, and transformations.
3. Choose the visual grammar from the data and claim, not from decoration. If the domain is unclear, read `references/field_patterns.md`.
4. Apply a top-journal style system: white background, black axes, restrained color, editable vector text, consistent panel geometry.
5. Show uncertainty and individual data where scientifically appropriate. Never hide distribution shape behind only bars.
6. Compose multi-panel figures with aligned axes, shared scales where comparisons require them, and panel labels that are easy to scan.
7. Export at least SVG/PDF plus high-DPI PNG/TIFF when needed. Verify typography, overlap, scale bars, legends, color accessibility, and statistical annotations.

## Style Defaults

- Background: white, no gradients, shadows, decorative frames, or chart junk.
- Typography: Arial, Helvetica, Liberation Sans, or a close sans-serif fallback.
- Axes: black, thin, outward ticks, no unnecessary top/right spines unless the plot type benefits from a full box.
- Lines: use black or near-black for primary fits, model curves, error bars, and important reference lines.
- Color: use low-saturation, color-blind-considerate palettes only to encode groups or categories.
- Panels: near-square or slightly flat, with consistent aspect ratios across related panels.
- Labels: use real experimental variables and units. Do not write placeholder labels such as `Treatment`, `Sample`, or `Dose` if the data provides the true name.
- Statistics: show meaningful comparisons only; do not label non-significant comparisons as `ns` unless the journal or user explicitly asks.
- Vector editing: keep SVG text editable and PDF fonts embedded when possible.

For detailed values, palettes, and export settings, read `references/style_tokens.md`.

## Data Integrity Rules

- Keep and plot biological/technical replicates when available.
- For small-n experimental data, prefer dot/box/violin plus mean/median and uncertainty over bar-only summaries.
- Use mean +/- SD for descriptive replicate spread; use SEM or CI only when that is scientifically justified and labeled.
- Use log scales for concentrations, rates, p-values, fold changes, spectra, or heavy-tailed measurements when appropriate; label transformed axes clearly.
- Keep related y-axis ranges consistent when the visual comparison depends on magnitude.
- Do not force curve fitting, IC50/EC50, regression, smoothing, or statistical annotations when the data do not support them.
- Do not invent data, p-values, sample sizes, scale bars, microscopy metadata, or uncertainty intervals.

## Figure-Type Guidance

Load `references/field_patterns.md` when deciding between domain-specific plots. Common defaults:

- Replicate group comparison: dot + mean +/- SD, box/violin + points, or estimation plot.
- Dose-response/time-course: log x-axis when dose spans orders of magnitude; mean +/- SD/CI with restrained fit.
- Correlation/regression: scatter with fit only when model assumptions are acceptable; show n and uncertainty when useful.
- Omics/high-dimensional: volcano, heatmap, PCA/UMAP, enrichment dot plot, or clustered matrix with careful color scaling.
- Imaging: include scale bars, channel labels, consistent contrast, and non-misleading crops.
- Model performance: calibration, ROC/PR, confusion matrix, residual/error distribution, ablation, and uncertainty where relevant.

## Python Implementation

When using Python/Matplotlib, prefer the helper in `scripts/journal_style.py`.

Minimal pattern:

```python
from scripts.journal_style import (
    DESIGN,
    setup_publication_style,
    apply_axis_style,
    add_panel_label,
    save_publication_figure,
)

setup_publication_style()
```

Use the user's existing codebase style when present. If no project style exists, use Matplotlib for static publication figures; use seaborn only as a statistical plotting helper and restyle the final axes.

## Multi-Panel Assembly

- Start from the manuscript story: each panel should answer one visible question.
- Use panel letters `a`, `b`, `c` or the target journal's convention.
- Align plot areas, not just outer figure bounds.
- Minimize repeated legends and axis labels; keep enough labels that each panel remains interpretable.
- Put legends close to the data or outside the plotting area without shrinking panels awkwardly.
- Ensure all text is readable at final print width: one-column, 1.5-column, or two-column.

## Visual QA Checklist

Before delivering:

- Data values, group names, units, transformations, and sample sizes are traceable to the source.
- Text does not overlap ticks, legends, annotations, points, error bars, or panel labels.
- Scales are comparable where intended and explicitly different where not.
- Colors remain distinguishable in grayscale or color-blind simulation when group identity matters.
- Error bars and statistical annotations are defined in the caption or labels.
- SVG/PDF exports keep text editable or fonts embedded.
- Raster exports are at least 300 dpi for photos and 600 dpi for line art when practical.
