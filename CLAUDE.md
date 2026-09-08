# CLAUDE.md — KI-Datenschutz-Prüfassistent

## What This Is

A folder-based ICM auditor (drop into a Claude project, Claude becomes the auditor) that checks a vendor's AI-tool dossier against German data-protection law and reports pass/gap/fail per provision, with every finding citing a resolvable provision. Built as the entry for Skool Weekly Comp "The Auditor" ($500), and as a sellable/reusable method for Joshua's consulting practice. Origin problem: German federalism forces redundant municipal Datenschutzprüfungen (3-5 days each); this is a prototype of the "Einer prüft für alle" pre-check (target 15-30 min).

## Current State (2026-09-07)

Complete and committed locally. NOT yet pushed to GitHub (submission needs a public repo; deadline Fri 11 Sep 2026).

- Auditor files done: `identity.md`, `rules.md`, `checklist.md` (5 Prüfschritte), `examples.md`, `README.md`.
- `reference/` holds the verbatim standard (DSGVO Art. 5/13/22/28/35/44, DSK Orientierungshilfe KI v1.0 cited sections, DSG NRW state module, SOURCES.md). All byte-clean UTF-8.
- `audit/` eval: `checks.py` (deterministic, resolves 91 valid IDs from reference/), `compliance-judge.md` (binary layer 2), 3 synthetic fixtures + planted-defect, keys outside the drop-in, receipts. `python audit/checks.py --all` runs the whole suite (real reports PASS, planted defect FAILs).
- `demo/`: frozen `TEST_METHOD.md`, a mixed dossier, the recorded cold-agent run (`cold-run/`), and the two-sided `platform-report.md`.
- Platform mode built: `perspectives.md` renders the same findings from both sides (Kommune next action + Anbieter next action), for the real customer = a startup+municipality pair getting a deal to signature.
- `checks.py` validates BOTH the single-column and the two-sided platform format (a cold run produced the platform format, which the checker could not parse before). `render/` turns a report into an HTML one-pager. Each audit is a `jobs/<anbieter>-<date>/` folder holding `input/` (the submitted documents) + `report.md` + `report.html` + `eval.md` together, so a run is reproducible and re-checkable against its own sources. `rules.md` "Run flow" tells the operating agent to open a job folder, save the submitted docs to input/, produce the report, run the audit on its own output, and render (the cold run had skipped the audit, produced an unparseable format, and saved to a scratchpad). Job folders are confidential and git-ignored (only README + `_template/` are tracked), so real vendor documents never reach the public repo.
- Open thread: which side to lead the go-to-market (startup readiness vs the pair), and adding state modules via regional-expert conversations (each convo = a relationship + a module + a possible pilot).

## Stack

None. Pure ICM: markdown files as agent architecture. One Python 3 stdlib script (`audit/checks.py`, no dependencies) for the deterministic eval. No server, no DB, no build.

## Architecture

Pipeline shape (dossier in, report out) with a factory/product split. Factory (stable across runs): `reference/` + `identity`/`rules`/`checklist`. Product (new each run): the German audit report. Quality gate: `audit/` (evidence about the output, never read by the auditor). State layer (`reference/dsg-nrw.md`) is swappable per Bundesland; the DSGVO+DSK core does not change. That swap is the "Einer prüft für alle" claim in file form.

## Data Model

Findings are three classes only: CLEAR PASS / NARROW FLAG / CLEAR FAIL. Citation IDs: `[DSGVO-Art<n>-<abs><lit>]`, `[DSK-OH-<section>]`, `[DSG-NRW-§<n>-<abs>]`. `checks.py` builds the valid-ID set by parsing `reference/` at runtime, so a citation that does not resolve fails (base wins, cannot be believed).

## Key File Paths

- Entry/route: `README.md`
- The auditor: `identity.md`, `rules.md`, `checklist.md`, `examples.md`
- The standard: `reference/*.md` (+ `reference/SOURCES.md` for provenance)
- The eval: `audit/checks.py`, `audit/compliance-judge.md`, `audit/conventions.json`
- Fixtures/keys/receipts: `audit/fixtures/`, `audit/keys/`, `audit/reports/`
- Demo: `demo/TEST_METHOD.md`, `demo/dossier.md`, `demo/cold-run/`

## Dev Server

None. To run the eval: `python audit/checks.py --all`. To use the auditor: load the folder into a Claude project and feed it a dossier (see README).

## Patterns & Gotchas

- **Encoding split:** GDPR HTML (dsgvo-gesetz.de) is UTF-8; the DSK PDF via pdftotext is cp1252. German string literals in Bash heredocs get mangled, so extraction scripts must be all-ASCII and pull text from decoded bytes. The DSK PDF needed pdfplumber coordinate extraction to drop margin-Randnummern (right margin x0>=505, left <95) and de-hyphenation with a compound/conjunction rule.
- **`checks.py` prints UTF-8** via `sys.stdout.reconfigure` so it runs on any console.
- **The eval audits the auditor's OUTPUT report,** not the auditor's factory files. Different role than in handover-operator, where it audited a produced workspace.

## Phase History

- 2026-09-07: built end to end (reference extraction, auditor files, eval, fixtures). Reviewed against Comp winner patterns (Adam James: frozen test method + cold-run evidence + boundary honesty; Jeff van Leenen: generated verifier, base wins). Added `--all` runner and cold-agent demo.

## Workflow Rules

- Keep the repo generic and public-safe: no client data, no real vendor/municipality. Synthetic fixtures only.
- `reference/` is verbatim standard only; never paraphrase into it. New provisions go in with a SOURCES.md entry.
- To add a Bundesland: replace `reference/dsg-nrw.md` and the state section in `checklist.md`. Nothing in PS-0..PS-4 changes.
- Registered in HQ at `~/step-into-more/commons/repos.md`.
