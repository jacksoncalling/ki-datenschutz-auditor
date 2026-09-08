# <Anbieter> — Datenschutz-Vorprüfung (<YYYY-MM-DD>)

Copy this `_template/` folder to `jobs/<anbieter>-<YYYY-MM-DD>/` and rename this heading. One job = one vendor, one date.

## What is here

- `input/` — the documents that were submitted for this audit. Put them here first.
- `report.md` — the audit report you produce (created during the run).
- `report.html` — the rendered one-pager (created during the run).
- `eval.md` — the `checks.py` receipt proving the report passed its own auditor (created during the run).

## The run (from `rules.md`)

1. Put the submitted documents in `input/`.
2. Produce `report.md` by auditing them against the folder's checklist.
3. `python audit/checks.py jobs/<this>/report.md --report jobs/<this>/eval.md` (must exit 0).
4. `python render/render.py jobs/<this>/report.md -o jobs/<this>/report.html`.

Notes for this job (contacts, scope, what was missing) can go below.
