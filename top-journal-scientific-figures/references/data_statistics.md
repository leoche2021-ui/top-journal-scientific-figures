# Data provenance and statistical boundaries

## Intake and provenance
Record source path/sheet/table, SHA-256, variables, units, experimental-unit ID, hierarchy, pairing/time structure, missing tokens, valid n, preprocessing, excluded row IDs with reasons, transformations, random seed, software versions, and final group/color/scale mappings. Keep original files immutable. Exported subsets or workbook-to-CSV conversion must name their original sheet/range and conversion code. SHA-256 proves file identity, not scientific validity.

Automatic type inspection only proposes roles. Confirm experimental unit, biological/technical replication, paired/repeated design, denominator, and below-detection handling before summarizing. Technical repeats require an explicitly documented aggregation or hierarchical model; never inflate n. If metadata is unknown, offer exploratory raw points and label uncertainty rather than inventing design.

## Missingness, scales, summaries
Report per-group effective n and missing rows; never replace missing with zero. For n=1, plot the point/mean and state SD undefined. For n=0, stop that figure. Use sample SD (ddof=1). SEM = SD/sqrt(n) only for independent experimental units with a clearly labeled purpose. CI needs method, confidence level, and appropriate resampling unit/model. Tiny-n violin/KDE distributions can imply unjustified density; prefer visible points.

Do not silently add pseudocounts for log scales. Record log base and whether summaries were computed before or after transformation. Do not force zero on scatter/spectra; magnitude bars normally need zero. State truncated axes and ensure limits do not hide data or uncertainty. Preserve units and normalization baseline.

## Inference and fitting
Require scientific question, design, test/model assumptions, effect size, CI method, multiple-testing family/correction, and statistical code. Do not choose significance thresholds after looking at results. Paired data require pairing; repeated observations need clustered/hierarchical treatment; bootstrap at the experimental-unit level. Do not turn random seeds, pixels, cells within one organism, or technical reads into independent biological n.

IC50/EC50 requires adequate dose coverage and response support; report model, constraints, fitting uncertainty, diagnostics and failed fits. Regression needs model support and residual checks. Never invent p-values or reverse-engineer significance stars. Precomputed statistics may be plotted only with their source and methods. The bundled pipeline intentionally performs descriptive statistics only.

## Image integrity
Keep uncropped originals and acquisition metadata. Verify scale bars from calibrated pixel size, never from visual guesswork. Record global contrast/color adjustments, use comparable settings for comparisons, label splices and crops, and do not selectively remove or enhance features. Check the target journal's current AI/image policies for schematics or generated illustrations.
