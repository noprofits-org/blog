# Advocacy funding audit

Start with [NOTES.md](NOTES.md). It contains the findings, publishable sentences,
organization profiles, claim verdicts and exact search boundaries.
[STATE.md](STATE.md) identifies unresolved questions and the public documents
needed to close them.

## Reproduce

From this directory:

```bash
.venv/bin/python compute.py
```

For validation without image regeneration:

```bash
.venv/bin/python compute.py --check-only
```

The supplied environment includes the dependencies. For a fresh environment:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python compute.py
```

`compute.py` reads the CSV register, checks the pinned input hashes and primary
field matches, independently checks report-version selection, recalculates every
aggregate and compares it with frozen expectations. It does not fetch data or
silently update expected values. Changes to the evidence require a reviewed new
snapshot and a deliberate update to the lock and expected-value register.

## Files

- `research/`: row-keyed evidence, calculations, bounded searches, verdicts,
  unresolved records and the mapping from every plotted value to its source rows.
- `figures/`: publication PNG and SVG files. PNG dimensions are
  **1200 × 630** [M-WIDTH; M-HEIGHT].
- `sources/`: exact public responses, original URLs, resolved URLs, snapshot
  dates, hashes and cached robots policies. Some response bodies are gzip data
  despite an HTML suffix; acquisition code detects this from the bytes.
- `extracted/`: field-path caches derived from the primary IRS visual renders.
  The caches used in validation are pinned alongside the original responses.
- `LOCK.json`: hashes for the evidence and source snapshots. Verification fails
  when a file changes or disappears.
- Acquisition scripts (`fetch_sources.py`, `parse_filings.py`,
  `assemble_evidence.py`, `parse_lda.py` and supplemental scripts) document how the
  source rows were obtained. These are separate from the reproducible calculator.

The compact matrix reports cash grants by legal payer. It is not a total of
unique original funding: a grant can be followed by a separately reported
regrant. DAF-sponsor ratios use the identified cash pool only. They do not
establish confirmed donor-advised shares or total donor coverage. These limits
are part of the captions and the claim register.

The deliverable remains local. It has not been committed or published.
