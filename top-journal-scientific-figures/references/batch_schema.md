# Batch JSON configuration

Run from the skill directory:

```sh
python scripts/figure_pipeline.py examples/batch.json
python scripts/figure_pipeline.py examples/batch.json --inspect examples/demo_replicates.csv
```

Install dependencies from `requirements.txt` in a suitable Python environment. CSV must be UTF-8, long format, with unique headers; each row is one confirmed experimental unit in one group. Explicitly preprocess XLSX/TSV or technical replicates outside this helper and record the source/method. No data conversion is implicit.

`shared`: `group_order` (unique ordered names), `colors` (group → Matplotlib color), optional `size_mm` [width,height], `formats` (must include svg/pdf; png/tiff supported), optional `ylim`. A common ylim is only appropriate for scientifically comparable measurements with identical units/transforms; the agent must check this before configuration.

`figures`: unique safe `id`, `source` (relative to config), `group`, `value`, `unit_id` column names; `experimental_unit_confirmed: true`; `replicate_level: "experimental_unit"`; `unit_description`; `design: "independent" | "paired"`; `missing_policy: "error" | "omit_report"`; `measurement_label`; `units`; optional `group_label`, `transform: "none" | "log10"`, `missing_tokens`, `seed`, `size_mm`, `ylim`, `preprocessing`.

`output`: output directory relative to config. It must not exist; choose a fresh path for a rerun. A failed figure is reported while other figures continue; process exit code is nonzero if any fails. Partial failed directories may contain intake audit/source but are not completed figures. Output status remains `generated_needs_visual_review` until inspection. No inference, p-values, CI, smoothing, or fitting is performed automatically.

Each completed directory contains raw source, SVG/PDF/PNG, grayscale preview, audit.json, qa.json, caption.txt, config.json, and copies of the exact scripts. Run `python scripts/figure_pipeline.py config.json` from that directory to reproduce into a fresh `rerun` directory.
