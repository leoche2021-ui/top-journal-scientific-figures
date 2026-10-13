# Field Patterns

Use this reference to select a figure grammar for different research domains.

## Biology and Biomedicine

- Cell viability, cytotoxicity, enzyme activity: dose-response with log concentration, mean +/- SD, individual replicate points, optional 4PL fit only when supported.
- qPCR, western blot quantification, ELISA: dot + summary or bar + points; label normalization baseline precisely.
- Flow cytometry: representative gating plus quantitative summary; avoid rainbow density unless needed.
- Microscopy: scale bars, channel labels, identical intensity scaling for comparisons, representative images paired with quantification.
- Survival: Kaplan-Meier with risk table when possible; report censoring and test used.

Red flags: bar-only n=3 summaries, hidden replicates, unlabeled normalization, forced IC50, inconsistent image contrast.

## Clinical, Epidemiology, and Public Health

- Cohort baseline: compact table or dot/forest plot for effect sizes.
- Treatment effects: forest plot with confidence intervals.
- Time-to-event: Kaplan-Meier or cumulative incidence with risk table.
- Diagnostic models: ROC plus PR curve when classes are imbalanced; calibration plot and decision curve when clinically relevant.
- Geographic data: choropleth only with appropriate normalization; show uncertainty or sample size if uneven.

Red flags: odds ratios shown without CI, truncated axes exaggerating effects, no denominators, class imbalance hidden behind accuracy.

## Chemistry, Materials, and Nanoscience

- Spectra: thin line plots, offset only when explicitly labeled, consistent baselines.
- XRD/XPS/FTIR/Raman: annotate peaks sparingly; avoid filled decorative gradients.
- Particle size/zeta: distribution plus summary, not only mean.
- Materials performance: cycle number/time on x-axis, retention/efficiency on y-axis, consistent units.
- Structure-property: scatter/regression with uncertainty and sample identity when useful.

Red flags: unlabeled peak assignments, inconsistent smoothing, cropped baselines that change interpretation.

## Physics, Engineering, and Computation

- Scaling laws: log-log plots with slope annotations and confidence intervals when fitted.
- Simulations: compare theory, simulation, and experiment with distinct line styles before adding colors.
- Control/robotics/systems: time series with event markers and uncertainty bands.
- Benchmarking: paired comparisons, rank plots, performance profiles, or error distributions.

Red flags: too many colored lines, missing units, unreported smoothing/windowing, cherry-picked time windows.

## Earth, Climate, and Environmental Science

- Time series: show seasonality, anomalies, or rolling summaries only when defined.
- Maps: use perceptually uniform color maps, projection labels, scale bars when useful, and uncertainty layers when possible.
- Depth/altitude profiles: orient axes according to field convention.
- Concentrations and fluxes: log scales for orders of magnitude; include detection limits.

Red flags: rainbow maps, missing projection or normalization, mixing raw and anomaly values without labels.

## Omics and High-Dimensional Biology

- Differential expression: volcano with effect size and adjusted p-value thresholds; label only selected genes/features.
- Expression patterns: heatmap with controlled scaling, annotation bars, and clear clustering method.
- Dimension reduction: PCA/UMAP/t-SNE with explained variance where relevant; avoid implying distances that the method does not support.
- Pathways: enrichment dot plot, bar chart, or network only when it clarifies the biology.

Red flags: unlabeled color scales, too many gene labels, p-values without multiple-testing correction, decorative networks.

## AI, ML, and Data Science

- Classification: ROC, PR, calibration, confusion matrix, subgroup performance, and uncertainty from resampling.
- Regression: predicted vs observed, residuals, error distribution, and subgroup slices.
- Ablations: paired dot/line comparisons when repeated seeds exist; show variance across seeds.
- Training curves: mean +/- CI across seeds; avoid smoothing that hides instability.

Red flags: only best-run metrics, accuracy on imbalanced data, missing confidence intervals, unclear train/test split.

## Quantitative Social Science and Economics

- Effects: coefficient/forest plots with confidence intervals.
- Time and policy: event studies with pre-trend visibility.
- Distributions: histograms, ridgelines, ECDFs, or box/violin plots.
- Survey results: dot plots or diverging bars; show weighting and denominators when relevant.

Red flags: stacked bars with too many categories, missing sample sizes, no uncertainty, arbitrary axis truncation.

