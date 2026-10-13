# Export and visual QA

## Automated checks in the CSV pipeline
Draw the renderer at final physical size; report text outside the canvas, fonts below the configured 6 pt review threshold, candidate text-box overlaps, actual raster pixel dimensions/DPI, file sizes, and SVG text nodes. Export a grayscale preview. These checks do not validate scientific meaning or guarantee font embedding/accessibility. The report always retains manual-review status.

## Required review
Open the exported color and grayscale PNG at full resolution and intended manuscript width. Inspect panel letters, plot-area alignment, labels/ticks/legends, point/uncertainty overlaps, scale bars, scientific symbols, font fallback, and comparable scales. Dense plots need color vision simulation and redundant marker/line encodings; grayscale alone is insufficient. Resolve significant text clipping before delivery; optional rotated labels or wider canvases may help.

Inspect SVG text after reopening in an editor; text remains editable but fonts must be installed on the recipient machine. For PDF, use `pdffonts` when available or a PDF font inspector; record results or explicitly report that embedding was not independently verified. Validate physical PDF page/SVG viewBox/raster dimensions after exporting. `bbox_inches="tight"` changes the canvas: use only deliberately and remeasure.

Raster requirements depend on artwork class and current journal instructions; 600 dpi line art is a toolkit default, not universal compliance. Never upsample a low-resolution original and call it higher-quality source data. Record source image resolution separately from export DPI.

Deliver a caption defining experimental unit, per-group n, summaries/error bars, pairing, transformations, exclusions, and statistical method. Label synthetic gallery/example files. Do not describe an automatic report as a completed visual or scientific audit.

Optional color vision previews: install `colorspacious`, then run `python scripts/accessibility_preview.py figure.png`. It uses the Colorspacious Machado model at severity 100; inspect the resulting protanomaly/deuteranomaly/tritanomaly previews and add redundant marker/line cues where colors merge. Simulation approximates vision; it is not a guarantee.
