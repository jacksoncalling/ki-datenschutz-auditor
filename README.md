# KI-Datenschutz-Prüfassistent

A folder-based AI auditor that checks a vendor's AI-tool dossier against German data-protection law and reports where it passes, where it is silent, and where it fails, with every finding citing a specific provision you can open and read.

Drop this folder into a Claude project (or point any capable agent at it). Claude becomes the auditor. Feed it an AI vendor's paperwork; get back a structured German pre-check report in minutes.

---

## The problem it solves

Germany has 16 states, 16 state data-protection laws, and 16 supervisory authorities, all interpreting the same DSGVO. When a vendor sells one AI tool to many municipalities, each municipality's data-protection officer redoes the same preliminary audit from scratch, 3 to 5 days each. This is the bottleneck the report behind this project names: data-protection rules that differ from one federal state to the next cause redundant data-protection audits of the very same set of facts.

The fix is the principle of **auditing once and reusing everywhere** ("one audits for all"): the shared, identical core of the check (DSGVO plus the joint DSK guidance) is done once and travels; only the state-specific layer is re-checked. This auditor is a working prototype of that idea, aimed at cutting the preliminary check from 3 to 5 days to 15 to 30 minutes so the human officer starts from a map instead of a blank page.

## What it checks against (the standard is in `reference/`)

Not a summary. The actual standard, verbatim, so any finding is verifiable:

- **`reference/dsgvo-artikel.md`** — DSGVO Art. 5, 13, 22, 28, 35, 44 (verbatim).
- **`reference/dsk-oh-ki.md`** — DSK "Orientierungshilfe KI und Datenschutz" v1.0 (06.05.2024), the cited sections (verbatim).
- **`reference/dsg-nrw.md`** — the swappable state module (currently Nordrhein-Westfalen) plus the competent authority.
- **`reference/SOURCES.md`** — where every excerpt came from and how to cross-check it.

## What to feed it

An **AI-vendor deployment dossier** for a municipality. Ideally:

- the **data processing agreement (AVV)**,
- the **technical and organizational measures (TOMs)**,
- a **system / architecture description**, and
- the **product terms** (especially anything about model training and data location).

Missing documents are fine; they become flagged gaps rather than blocking the run.

## How to use it

1. Create a Claude project and add every file in this folder (keep the structure).
2. Paste, or attach, the vendor dossier.
3. Prompt:

   > Du bist der KI-Datenschutz-Prüfassistent aus diesem Projekt. Lies `identity.md`, `rules.md` und `checklist.md`, dann prüfe das folgende Anbieter-Dossier für eine Kommune in NRW. Erstelle den Bericht im Format aus `rules.md`.

4. You get a German report: an at-a-glance count, one finding per check (**CLEAR PASS / NARROW FLAG / CLEAR FAIL**) with a provision citation and a dossier quote, and for every gap an *Offene Entscheidung* line telling the human officer what to decide next.

The auditor flags and cites. It never delivers the final legal verdict; that stays with the municipality's Datenschutzbeauftragte(r), preserving the administration's discretion.

## The five checks (see `checklist.md`)

| # | Prüfschritt | Anchored in |
|---|---|---|
| PS-0 | Schwelle und DSFA-Pflicht | Art. 35 · DSK 2.3 |
| PS-1 | Menschliche Letztentscheidung (Human-in-the-Loop) | Art. 22 · DSK 1.6 · § 46 DSG NRW |
| PS-2 | Auftragsverarbeitung, Unterauftragnehmer, Datenstandort | Art. 28 · Art. 44 · DSK 2.1 |
| PS-3 | Trainingsverbot und Voreinstellungen | DSK 1.9 · DSK 2.5 · Art. 5 |
| PS-4 | Transparenz und Erklärbarkeit | Art. 13 · DSK 1.8 |

## Files

```
identity.md      who the auditor is, the three finding classes, the discretion guardrail
rules.md         the procedure, citation format, severity logic, output format
checklist.md     the five ordered Prüfschritte, each anchored to a provision
examples.md      three worked audits (a PASS, a NARROW FLAG, a CLEAR FAIL)
perspectives.md  the two-sided (platform) rendering: same findings, both parties' next actions
reference/       the standard, verbatim: DSGVO, DSK guidance, DSG NRW, SOURCES
audit/           the eval: proof the auditor catches what it should (see below)
render/          template + script that renders a report into an HTML one-pager
jobs/            one folder per audit: input documents + report + html + eval receipt
```

When you operate this folder on real documents, follow the **run flow** in `rules.md`: open a job folder (`jobs/<anbieter>-<date>/`, copied from `jobs/_template/`) and put the submitted documents in its `input/`; produce the report; **run `python audit/checks.py` on your own output** (it validates both the single-column and the two-sided platform format); render the HTML with `render/render.py`; the finished job folder holds input, report, html and the eval receipt together. The audit step is not optional; a report that fails its own auditor is not handed over. Job folders are confidential and git-ignored.

## Two sides of the same audit (platform mode)

The common case is not a city auditing a stranger; it is a **Community and a startup already trying to work together**, both needing the same contract to reach signature (several Agentic-AI-Hub pilot applicants were exactly such pairs). So the audit can be rendered from both sides at once: one dossier, one set of findings and citations, one severity per check, but two next-action columns, what the **Community** must require or clarify, and what the **service provider** must document or contractually secure. A NARROW FLAG becomes a concrete task for exactly one party; the audit turns into a shared punch-list to signature instead of a verdict handed down.

This is a rendering, not a re-audit: `reference/`, `checklist.md`, the classes and the citations stay single-homed, and the machine-checkable single-column report underneath still passes `audit/`. See `perspectives.md` for the format and `demo/platform-report.md` for a worked both-sides example.

To turn a both-sides report into a forwardable HTML one-pager (a founder or a Community can be shown the page directly), run the small template-based renderer:

```bash
python render/render.py demo/platform-report.md   # writes demo/platform-report.html
```

The page's content is parsed from the markdown, not hand-written, so it stays a translation of the report. See `render/README.md`.

## Scaling to other states (Bundesländer)

The whole design is built so this is cheap. To audit for, say, Bayern instead of NRW:

1. Replace `reference/dsg-nrw.md` with the equivalent state data-protection act (Landesdatenschutzgesetz) excerpt and the competent authority (there, the BayLDA / LfD Bayern).
2. Update the "state layer" section name in `checklist.md`.

Nothing in PS-0 through PS-4 changes, because that core is DSGVO plus the all-German DSK guidance. That is "one audits for all" made literal: the shared check is written once and reused; only the delta moves.

## Verifying this auditor (`audit/`)

An auditor you cannot check is just an opinion generator. `audit/` is a two-layer eval that proves this one earns trust:

- **`audit/checks.py`** (deterministic): every finding in a report cites an ID that actually exists in `reference/`, uses a valid severity class, and covers every check. No model, runs in a second.
- **`audit/compliance-judge.md`** (one binary judgment): does the cited provision actually support the finding? The single call code cannot make.
- **`audit/fixtures/`**: three synthetic vendor dossiers (a clean one, a gap-ridden one, a clearly failing one). The answer key lives in **`audit/keys/`, outside the drop-in folder**, so the test never carries its own answer into the room.
- **`audit/reports/`**: the receipts, the auditor run on each fixture, showing it passes the clean dossier and fails the bad ones.

See `audit/README.md` to run it.

## The evidence: a full test → correct → re-test loop

`demo/stepintomore-loop/` is the strongest proof the auditor discriminates. A cold agent audited a real dossier and returned 1 pass + 4 flags; each flagged gap was then closed in the documents; a fresh cold agent re-audited the corrected set and returned **5 of 5 CLEAR PASS**, verified by `checks.py`. The flags were real *and* closable, and the auditor recognises the fix instead of flagging forever. The expectation was frozen before the re-run, and the second cold agent ran the audit on its own output. See `demo/stepintomore-loop/README.md`.

`demo/retest/` is the same corrected set re-audited in the **two-sided platform format** (Community column + service-provider column), with its own frozen method and passing eval. Its job is to show `audit/checks.py` validates that format too, not just the single-column report. See `demo/retest/README.md`.

## Honesty about scope

This is a preliminary-check accelerator, not legal advice and not a compliance guarantee. It reads what a dossier says; it cannot verify that a vendor does what it claims. A real pilot must involve the municipality's Datenschutzbeauftragte(r) and, where relevant, a full DSFA. The auditor's value is speed and structure on the shared core, so the scarce human hours go to the genuinely contested calls.

---

*Method: Interpretable Context Methodology (folder as agent architecture). Standard: DSGVO + DSK-Orientierungshilfe KI + DSG NRW. Built for the German municipal AI-procurement bottleneck.*
