# Top-Journal Scientific Figures

**Turn research data into figures that are beautiful to read, honest to interpret, and possible to reproduce.**

A reusable scientific visualization skill and Python toolkit for researchers and AI assistants. It brings together scientific reasoning, editorial design, data provenance, and figure review to support manuscript preparation, grant applications, presentations, and submission polishing.

The workflow is portable: use the instructions with an assistant that can read project files, adapt the package to a supported skill system, or run the Python tools directly. Codex is one integration, not a prerequisite for the plotting code.

## The idea

A research figure is a compact scientific argument. Its visual structure should make the claim understandable, its data display should make the evidence inspectable, and its accompanying files should make the result reproducible. This skill treats those three responsibilities as one design problem.

Beautiful scientific communication comes from deliberate choices: selecting the right comparison, preserving the relevant variability, establishing a clear reading order, and removing visual elements that compete with the evidence. A polished figure should help a reader understand what was measured, what changed, how much uncertainty remains, and which conclusions the data can support.

The aim is to make that reasoning reusable across a single panel, a complete manuscript, and a batch of related figures.

## Design philosophy

### Start with the scientific question

Before choosing colors or drawing axes, identify the claim, the experimental design, the audience, and the measurement. A group comparison, a dose-response relationship, a survival analysis, and a spectrum require different visual grammars. The plot should follow the question and the data structure.

### Make evidence visible

Retain individual observations when appropriate. Distinguish experimental units from technical readings, show meaningful uncertainty, and disclose transformations and missingness. A summary should clarify the observations rather than conceal their distribution. Pairing, repeated measurements, normalization, and detection limits are scientific properties that must survive the transition from source data to figure.

### Use restraint to establish hierarchy

White space, readable typography, thin axes, coherent panel geometry, and purposeful color create a clear reading order. Color encodes a variable or group; panel structure organizes the argument; labels provide the context needed to interpret it. These are adaptable defaults: microscopy, maps, structures, spectra, and statistical plots have different needs.

### Keep the manuscript visually coherent

A figure set benefits from a stable visual vocabulary. Preserve group colors and ordering across panels, use comparable scales when the scientific comparison requires them, and align plot areas rather than only outer boundaries. Consistency should support comparison without forcing unrelated measurements into the same scale or aspect ratio.

### Preserve the path back to the source

A finished image is only one part of the deliverable. Source references, exact code, configuration, effective sample sizes, transformations, exclusions, and software versions make a figure reviewable and reproducible. File hashes establish source identity; they do not establish scientific validity.

### Treat review as part of creation

Check the exported figure at its intended size. Inspect labels, uncertainty, clipping, legends, scale bars, accessibility, and the relationship between the image and the source. Automated checks help find problems, while scientific interpretation and final visual judgment remain essential.

## Journal-aware visual language

The design approach draws on the clarity and editorial discipline associated with **Nature, Science, Cell, The Lancet, NEJM, PNAS, JACS, Angewandte Chemie, and Advanced Materials**. It translates shared principles into an adaptable workflow rather than prescribing one appearance for every field.

Aesthetic references and submission requirements are handled separately. Exact dimensions, accepted formats, resolution, typography, and image policies depend on the journal, article type, and submission stage. The package includes an official-source registry with explicit verification status; current requirements must be checked before submission. This project is independent of those journals and does not certify acceptance or compliance.

## What you can do

| Task | What the skill contributes |
| --- | --- |
| Create a figure from source data | Inspect the structure, establish scientific semantics, choose a plot, and produce traceable outputs |
| Improve an existing figure | Review visual grammar, uncertainty, labeling, geometry, and export quality |
| Assemble multiple panels | Organize the scientific story, align panels, coordinate legends, and retain useful comparisons |
| Standardize a figure collection | Maintain group mappings, typography, dimensions, and scientifically justified shared scales |
| Review before submission | Audit data handling, examine actual exports, and identify unresolved journal checks |
| Hand off editable work | Provide vector files, plotting code, configuration, and supporting records |

Domain references cover biology, medicine, chemistry, materials, physics, engineering, environmental science, omics, machine learning, and quantitative social science. They guide plot selection and review; the executable batch helper has a deliberately narrower scope.

## What is implemented today

The CSV batch pipeline supports **independent or paired point plots with mean and sample SD**. It requires explicit column mappings and confirmation of the experimental unit. It records missing measurements and effective n, rejects duplicated units and unsupported design assumptions, and refuses log transformations or axis limits that would misrepresent the data.

Each completed result includes an untouched source snapshot, source SHA-256, descriptive summaries, row-level audit records, configuration, exact plotting scripts, a caption draft, and SVG/PDF/PNG exports. TIFF is optional. Fixed-canvas export preserves the requested physical size.

Automated QA reports text outside the canvas, small text, candidate text overlaps, raster dimensions and DPI, and editable SVG text. A grayscale preview is included; an optional helper provides model-based color-vision previews when its dependency is installed. Batch failures are reported individually so another valid figure can still complete. Existing output directories are protected from overwriting.

Broader figure types use the domain guidance and example code. Workbook conversion, technical-replicate aggregation, inferential statistics, complex modeling, and new plot types require explicit preprocessing or additional analysis code.

## Example

![Synthetic point plot with visible observations, mean, sample SD, and effective sample sizes](top-journal-scientific-figures/examples/verified_batch_outputs/synthetic_demo/synthetic_demo.png)

This demonstration uses synthetic data only. Control has four valid observations; Exposed has three, with one missing measurement recorded in the audit. Example data and gallery outputs are illustrative and must never be presented as experimental evidence.

## Use it with your preferred assistant

**Assistants with skill support:** place the folder containing `SKILL.md` in the location supported by your application. Discovery rules, invocation syntax, and tool access vary by host. The bundled `agents/openai.yaml` is host-specific metadata; the Markdown instructions and Python helpers can be used independently.

**Other file-aware assistants:** provide `SKILL.md` as task guidance and give access to the referenced files, data, and scripts. Ask the assistant to follow the data-integrity and QA rules. This is a portable workflow, not a claim of tested native integration with every platform.

**Python users:** run the scripts directly without an AI assistant.

A platform-neutral request:

```text
Use the Top-Journal Scientific Figures workflow for this dataset.
Inspect the source and identify any unresolved experimental-unit, pairing, or unit information.
Create a figure that makes the observations and uncertainty readable at manuscript size.
Keep group mappings consistent and deliver editable exports, code, configuration,
a data audit, a caption draft, and a clear record of completed and pending QA checks.
```

## Run the batch example

```sh
git clone https://github.com/leoche2021-ui/top-journal-scientific-figures.git
cd top-journal-scientific-figures/top-journal-scientific-figures
python3 -m pip install -r requirements.txt
python3 scripts/figure_pipeline.py examples/batch.json
```

Use a fresh output directory for each run. Every completed result contains `reproduce.txt` with its rerun command.

## Explore the package

- [Core skill instructions](top-journal-scientific-figures/SKILL.md)
- [Data provenance and statistical boundaries](top-journal-scientific-figures/references/data_statistics.md)
- [Domain-specific figure patterns](top-journal-scientific-figures/references/field_patterns.md)
- [Visual style system](top-journal-scientific-figures/references/style_tokens.md)
- [Journal sources and verification status](top-journal-scientific-figures/references/journal_profiles.md)
- [Batch configuration](top-journal-scientific-figures/references/batch_schema.md)
- [Visual QA](top-journal-scientific-figures/references/visual_qa.md)
- [Validation record](top-journal-scientific-figures/references/validation_record.md)
- [Original source code](top-journal-scientific-figures/scripts/original/)

## Scientific integrity and validation

The instructions prohibit fabrication of measurements, p-values, sample sizes, intervals, microscopy metadata, and scale bars. They require scientific support for fitting, smoothing, exclusions, image adjustments, and statistical annotations. Automated type inspection can propose column roles; it cannot establish the experimental design.

Eight behavior tests and a batch failure-isolation check passed in the documented validation environment. The final synthetic export was visually inspected. PDF font embedding was requested but not independently verified, and the optional color-vision simulation was not executed in that environment because its dependency was unavailable. Automated QA therefore retains a manual-review status.

Run the behavior tests from the package directory:

```sh
python3 -m unittest discover -s tests -v
```

The intended outcome is a complete scientific communication artifact: a figure readers can understand, evidence researchers can inspect, and a workflow collaborators can reproduce.
