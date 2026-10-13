---
name: top-journal-scientific-figures
description: Create, revise, batch-style, and audit scientific figures from source data or existing plotting code for manuscripts, grants, and presentations. Includes traceable data handling, journal-aware styling, editable exports, and visual review.
metadata:
  short-description: Trustworthy publication figures and batch visual QA
---

# Top-Journal Scientific Figures

中文名称：顶刊科研图表美学与生成。Use accurate, readable figures with quiet hierarchy. Treat journal aesthetics as adaptable design references; claim submission compliance only against verified requirements for the exact journal, article type, and submission stage.

## Workflow

1. Identify the claim, field, audience, figure type, final physical size, and requested journal. Inspect source files and existing code before choosing a plot. Read `references/field_patterns.md` for domain choices.
2. Inspect candidate column types, but do not infer experimental units, pairing, technical/biological hierarchy, units, exclusions, or statistical tests from names alone. Clarify only scientifically consequential unknowns. Read `references/data_statistics.md` before analysis.
3. Preserve raw files, raw replicates, missingness, and transformations. Never invent measurements, p-values, n, intervals, scale bars, or metadata. Never silently delete outliers or impute missing observations. Distinguish missing from zero and below-detection-limit measurements.
4. Prefer points plus a defined summary for small-n experiments. Use paired lines when IDs confirm pairing. SD describes sample spread; SEM/CI require explicit justification. n counts experimental units, not technical readings. No inference is preferable to an unsupported test.
5. Read `references/style_tokens.md` for design defaults and `references/journal_profiles.md` for source-backed journal routing. User/scientific requirements override aesthetic defaults. Preserve image/map/matrix aspect ratios, encode groups with redundant cues when necessary, and use meaningful labels and units.
6. Assemble panels around the scientific story: align plot areas; retain comparable scales, consistent colors/order, readable panel letters, and close legends. Do not impose common scales across incompatible units or transformations.
7. Export SVG/PDF plus requested raster formats at the final physical size. Inspect actual rendered exports, not just plotting code. Check clipping, text/data overlaps, uncertainty, scale bars, legends, grayscale/color vision accessibility, and typography. Read `references/visual_qa.md`. Automated QA is partial; do not call its warnings a definitive pass.
8. Deliver figures, untouched source or source references, executable code, configuration, audit report, caption draft, and QA findings. Explicitly separate completed automatic checks from outstanding scientific/manual checks.

## Executable helpers

- `scripts/journal_style.py`: compatible original helpers plus deterministic dot-summary/paired plots, validated matrices, n<2 handling, and fixed-canvas export. Pass `preserve_aspect=True` for axes requiring native proportions. Original pre-upgrade source is in `scripts/original/journal_style.py`.
- `scripts/figure_pipeline.py`: long-format CSV batch workflow for independent/paired point + mean/SD plots. Reads explicit mappings; snapshots source and code; writes source SHA-256, row audit, summaries, caption, QA, and batch failure report. Never overwrites an existing output directory.
- `scripts/accessibility_preview.py`: optional Colorspacious-based protan/deutan/tritan previews; requires `colorspacious` and does not certify accessibility.
- Read `references/batch_schema.md` for configuration and commands. `examples/batch.json` and `examples/demo_replicates.csv` are runnable, explicitly synthetic examples. Never use example outputs as research evidence.
- Existing `examples/make_examples.py` remains a gallery of domain layouts; any generated/demo data is illustrative, not the user's evidence. For additional figure types or XLSX/TSV, adapt source code transparently and record preprocessing; the CSV helper is not a universal statistical engine.

## Boundaries

Do not smooth, fit, estimate IC50/EC50, calculate statistical annotations, normalize images, or aggregate technical replicates without scientific support and recorded methods. Do not reconstruct raw values from a picture as if they were measured data; disclose digitization uncertainty. For microscopy, preserve original images and metadata and report crops, global adjustments, and splices. Schematics must remain distinguishable from observed data.

Low saturation, black fits, hidden top/right spines, and omitting `ns` are starting preferences, not universal rules. Use perceptually uniform quantitative maps and meaningful diverging centers. Keep plot text editable in SVG and embed PDF fonts where possible; inspect font portability and final exported dimensions.

Validation evidence and environmental limitations: `references/validation_record.md`.
