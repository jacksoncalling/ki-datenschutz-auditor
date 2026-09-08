# rules.md — How this auditor works

The order of the audit, how findings cite the standard, how severity is decided, and the exact output format. `checklist.md` holds the individual checks; this file holds the method they all follow.

## Procedure

1. **Intake.** Confirm what the user handed you. The expected input is an *AI-vendor deployment dossier* for a municipality: typically an Auftragsverarbeitungsvertrag (AVV / DPA), the technisch-organisatorische Maßnahmen (TOMs), a system or architecture description, and the product terms. Name which of these are present and which are missing. A missing document is not yet a finding, but it will drive NARROW FLAGs downstream because absence of evidence is a gap to close.

2. **Threshold.** Establish two facts before checking anything else: (a) does the tool process personal data (personenbezogene Daten), and (b) is it an AI application in the sense of the DSK guidance. If either is clearly "no", say so and stop, this auditor does not apply. If yes, note that a Datenschutz-Folgenabschätzung under Art. 35 is likely required (`[DSGVO-Art35-1]`, `[DSK-OH-2.3]`) and proceed.

3. **Run the checklist in order.** Work `checklist.md` top to bottom. Each check names the provision(s) it tests and the dossier evidence it needs. Produce one finding per check (never skip a check silently; if you cannot assess it, that itself is a NARROW FLAG with the reason).

4. **State layer last.** After the federal checks, apply the state module (`reference/dsg-nrw.md`): confirm the competent authority and any Land-specific rule. This is the only part that changes when the auditor is pointed at another Bundesland.

5. **Summarise.** Roll the findings into the report header: counts per class and the single most important open decision for the DSB.

## Run flow and where to save (do all of it, in order)

When you operate this folder on real documents, the audit is not the last step, and it is not optional. A report you produce but never check is exactly what this tool exists to prevent. One job = one vendor, one date, one folder that keeps the submitted and the created files together. Do all of this:

1. **Open a job folder.** Copy `jobs/_template/` to `jobs/<anbieter>-<YYYY-MM-DD>/` and put the submitted documents in its `input/`. Never audit documents that live only in the chat; save them first, so the report can be re-checked against them later.
2. **Read** the documents in `input/`.
3. **Produce `report.md`** in the job folder. Either the single-column format defined below, or the two-sided platform format in `perspectives.md`. Both are accepted.
4. **Audit your own output.** Run `python audit/checks.py jobs/<this>/report.md --report jobs/<this>/eval.md`. It validates both formats: coverage, valid severities, that every citation resolves against `reference/`, open decisions present, and honest counts. If any gate fails, fix the report and rerun. **Never hand over a report that fails its own auditor.** (This is the step a cold run skipped; it is the one that makes the result trustworthy.)
5. **Render the page.** Run `python render/render.py jobs/<this>/report.md -o jobs/<this>/report.html` (add `--demo` for a synthetic or example report). This turns the report into the forwardable one-pager automatically; do not hand-build the HTML.

The finished job folder holds `input/`, `report.md`, `report.html` and `eval.md`: a self-contained, reproducible record. Job folders are confidential and git-ignored; do not commit real ones.

## How to cite

Every finding must carry at least one citation ID that exists verbatim in `reference/`. The reader must be able to open the finding, open the cited provision, and check that the two match. No ID, no finding.

- DSGVO: `[DSGVO-Art<article>-<paragraph><letter>]`, e.g. `[DSGVO-Art28-3a]`, `[DSGVO-Art22-1]`.
- DSK guidance: `[DSK-OH-<section>]`, e.g. `[DSK-OH-1.9]`.
- State module: `[DSG-NRW-§<n>-<paragraph>]`, e.g. `[DSG-NRW-§46-1]`.

When you cite, quote the short operative phrase from the reference (in German, verbatim) so the match is visible without a second lookup. Do not paraphrase the standard inside a citation.

## How severity is decided

Apply this test to each check, in this order:

1. Does the dossier **contradict** the provision (states or implies something the provision forbids, or omits something the provision makes mandatory for lawfulness)? → **CLEAR FAIL**.
2. Does the dossier **explicitly satisfy** the provision, with locatable evidence? → **CLEAR PASS**.
3. Otherwise (silent, ambiguous, partial, or evidence missing)? → **NARROW FLAG**.

Two rules keep this honest:

- **Silence is never a PASS.** If the dossier does not address a mandatory point, the floor is NARROW FLAG, even if nothing suggests a problem. "They probably do it" is not evidence.
- **A FAIL needs a contradiction you can point to.** If you cannot quote the dossier text (or name the specific mandatory element that is absent) that conflicts with the cited provision, it is a NARROW FLAG, not a FAIL. Never escalate to FAIL on suspicion.

## The discretion guardrail

You classify against the standard; you do not deliver the legal verdict. End every FAIL and every NARROW FLAG with an **"Offene Entscheidung"** line naming what the human DSB must now decide or obtain. This preserves the administration's Ermessensspielraum and matches the DSK's warning against rigid automated judgments on ambiguous text. A PASS does not need an open-decision line.

## Output format

Produce the report in **German** (the reader is the municipal DSB). Use exactly this structure:

```
# Datenschutz-Vorprüfung: <Produkt / Anbieter>
Geprüft gegen: DSGVO + DSK-Orientierungshilfe KI (06.05.2024) + DSG NRW
Vorgelegte Unterlagen: <Liste> | Fehlend: <Liste>
Datum: <YYYY-MM-DD>  ·  Zuständige Aufsicht: LDI NRW

## Ergebnis auf einen Blick
CLEAR PASS: n   ·   NARROW FLAG: n   ·   CLEAR FAIL: n
Wichtigste offene Entscheidung: <ein Satz>

## Befunde
### [PS-n] <Prüfschritt-Titel> — <CLEAR PASS | NARROW FLAG | CLEAR FAIL>
- Fundstelle im Dossier: <Zitat oder "keine Angabe">
- Standard: <ID> „<verbatim Kurzzitat>"
- Bewertung: <ein bis drei Sätze>
- Offene Entscheidung (DSB): <nur bei FLAG/FAIL>

## Hinweis
Diese Vorprüfung ersetzt nicht die Entscheidung der oder des Datenschutzbeauftragten. Sie strukturiert und beschleunigt sie.
```

Keep the whole report readable in one sitting. One finding per check, no filler.
