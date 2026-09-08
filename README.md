# KI-Datenschutz-Prüfassistent

A folder-based AI auditor that checks a vendor's AI-tool dossier against German data-protection law and reports where it passes, where it is silent, and where it fails, with every finding citing a specific provision you can open and read.

Drop this folder into a Claude project (or point any capable agent at it). Claude becomes the auditor. Feed it an AI vendor's paperwork; get back a structured German pre-check report in minutes.

## Quick start

1. Create a Claude project and add every file in this folder (keep the structure).
2. Paste or attach the vendor dossier. Ideally the data processing agreement (AVV), the technical and organizational measures (TOMs), a system / architecture description, and the product terms (especially model training and data location). Missing documents are fine; they become flagged gaps, not blockers.
3. Prompt:

   > Du bist der KI-Datenschutz-Prüfassistent aus diesem Projekt. Lies `identity.md`, `rules.md` und `checklist.md`, dann prüfe das folgende Anbieter-Dossier für eine Kommune in NRW. Erstelle den Bericht im Format aus `rules.md`.

You get a German report: an at-a-glance count, one finding per check (**CLEAR PASS / NARROW FLAG / CLEAR FAIL**) with a provision citation and a dossier quote, and an *Offene Entscheidung* line on every gap telling the officer what to decide next. The auditor flags and cites; it never delivers the final legal verdict. That stays with the municipality's Datenschutzbeauftragte(r).

## Why it exists

Germany has 16 states, 16 state data-protection laws, and 16 supervisory authorities, all interpreting the same DSGVO. When a vendor sells one AI tool to many municipalities, each municipality's data-protection officer redoes the same 3-to-5-day preliminary audit from scratch. The fix is **auditing once and reusing everywhere** ("one audits for all"): the shared core (DSGVO plus the joint DSK guidance) is checked once and travels; only the state-specific layer is re-checked per state. This prototype aims to cut that preliminary check to 15 to 30 minutes, so the human officer starts from a map instead of a blank page.

## What it checks against (the standard is in `reference/`)

Not a summary. The actual standard, verbatim, so any finding is verifiable:

- **`reference/dsgvo-artikel.md`**: DSGVO Art. 5, 13, 22, 28, 35, 44 (verbatim).
- **`reference/dsk-oh-ki.md`**: DSK "Orientierungshilfe KI und Datenschutz" v1.0 (06.05.2024), the cited sections (verbatim).
- **`reference/dsg-nrw.md`**: the swappable state module (currently Nordrhein-Westfalen) plus the competent authority.
- **`reference/SOURCES.md`**: where every excerpt came from and how to cross-check it.

## The five checks (see `checklist.md`)

| # | Prüfschritt | Anchored in |
|---|---|---|
| PS-0 | Schwelle und DSFA-Pflicht | Art. 35 · DSK 2.3 |
| PS-1 | Menschliche Letztentscheidung (Human-in-the-Loop) | Art. 22 · DSK 1.6 · § 46 DSG NRW |
| PS-2 | Auftragsverarbeitung, Unterauftragnehmer, Datenstandort | Art. 28 · Art. 44 · DSK 2.1 |
| PS-3 | Trainingsverbot und Voreinstellungen | DSK 1.9 · DSK 2.5 · Art. 5 |
| PS-4 | Transparenz und Erklärbarkeit | Art. 13 · DSK 1.8 |

## Verifying the auditor (`audit/`)

An auditor you cannot check is just an opinion generator. `audit/checks.py` reads a report and confirms mechanically that every finding covers a required check, carries a valid severity, and cites an ID that **actually resolves in `reference/`** (the base wins; a phantom citation fails). The answer keys live in `audit/keys/`, outside the drop-in folder, so the test never carries its own answer into the room. `audit/compliance-judge.md` adds the one call code cannot make: does the cited provision actually support the finding? Run the whole suite with `python audit/checks.py --all`.

**The evidence that matters** (`demo/stepintomore-loop/`): a cold agent audited a real dossier and returned 1 pass + 4 flags; each gap was then closed in the documents; a fresh cold agent re-audited the corrected set and returned **5 of 5 CLEAR PASS**, verified by `checks.py`. The flags were real *and* closable, and the expectation was frozen before the re-run. `demo/retest/` shows the same loop in the two-sided platform format, proving `checks.py` validates that format too.

## Two sides of the same audit (platform mode)

The common case is not a city auditing a stranger; it is a **municipality and a startup already trying to work together**, both needing the same contract to reach signature. The audit can be rendered from both sides at once: one set of findings and citations, one severity per check, but two next-action columns, what the **municipality** must clarify and what the **service provider** must document. A NARROW FLAG becomes a concrete task for one party, and the audit turns into a shared punch-list to signature instead of a verdict handed down. This is a rendering, not a re-audit: the underlying single-column report still passes `audit/`. See `perspectives.md` and `demo/platform-report.md`; `render/render.py` turns any report into a forwardable HTML one-pager.

## Scaling to other states (Bundesländer)

Swap `reference/dsg-nrw.md` for the target state's data-protection act (Landesdatenschutzgesetz) and competent authority, and update the "state layer" name in `checklist.md`. Nothing in PS-0 through PS-4 changes, because that core is DSGVO plus the all-German DSK guidance. That is "one audits for all" made literal.

## Files and scope

```
identity.md      who the auditor is, the three finding classes, the discretion guardrail
rules.md         the procedure, citation format, severity logic, output format, run flow
checklist.md     the five ordered Prüfschritte, each anchored to a provision
examples.md      three worked audits (a PASS, a NARROW FLAG, a CLEAR FAIL)
perspectives.md  the two-sided (platform) rendering
reference/       the standard, verbatim: DSGVO, DSK guidance, DSG NRW, SOURCES
audit/           the eval: proof the auditor catches what it should
render/          template + script that renders a report into an HTML one-pager
jobs/            one folder per audit: inputs + report + html + eval receipt (git-ignored)
```

On real documents, follow the **run flow** in `rules.md`: open a `jobs/` folder, save the inputs, produce the report, run `checks.py` on your own output, then render. The audit step is not optional; a report that fails its own auditor is not handed over.

This is a preliminary-check accelerator, not legal advice and not a compliance guarantee. It reads what a dossier says; it cannot verify that a vendor does what it claims. A real pilot must involve the municipality's Datenschutzbeauftragte(r) and, where relevant, a full DSFA.

---

*Method: Interpretable Context Methodology (folder as agent architecture). Standard: DSGVO + DSK-Orientierungshilfe KI + DSG NRW. Built for the German municipal AI-procurement bottleneck.*
