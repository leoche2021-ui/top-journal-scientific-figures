# Validation record — 2026-10-13

Python 3.9, Matplotlib 3.9.4, NumPy 1.26.4. Skill frontmatter validation passed. Eight behavior tests passed: effective n/missing rows/source hash, standalone reproduction, non-overwrite, duplicate-unit rejection, false-independence rejection, unconfirmed-unit rejection, log-zero rejection, paired missingness, clipping rejection, and singleton/empty SD behavior (some assertions share a test).

Synthetic example generated SVG/PDF/PNG. Raster is 2125 × 1653 pixels at approximately 600 dpi for a 90 × 70 mm canvas. Editable SVG text detected. Renderer reported no outside-canvas text, undersized text, or candidate text-box overlaps. Actual exported color PNG was visually inspected after the final spacing fix: labels, n, points and mean/SD are readable. Its source summary is Control n=4, mean=10, sample SD≈0.8165; Exposed n=3, mean≈13.6667, SD≈1.5275; one explicit missing measurement. All data are synthetic.

Limitations: PDF font embedding was requested via Type 42 but not independently inspected (pdffonts/pypdf unavailable). Optional color vision preview helper requires Colorspacious, absent in this environment; its help/dependency-failure behavior and syntax were verified, but simulation output was not executed. Batch QA therefore honestly retains manual-review status. Journal sources unavailable or only located are explicitly marked unverified; no universal submission compliance claim is made.

An additional batch integration check passed: one unconfirmed figure failed, a following valid figure still exported successfully, and the batch returned nonzero with both statuses recorded.
