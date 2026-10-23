# FINDINGS.md — the honest read of the first pass

Kept in on purpose. An eval that only advertises its strengths is doing the same thing a rubber-stamp auditor does.

## What this eval genuinely proves

- Every finding in every produced report cites a provision that **actually exists** in `reference/`. This is mechanical and complete: `checks.py` resolves 116 valid IDs from the standard (91 before the BDSG module) and rejects anything else, anywhere in the report.
- The auditor **discriminates**: it passes a clean dossier, flags an ambiguous one, and fails a violating one, verified against answer keys held outside the fixtures.
- The checker **refuses**: six planted defects, six catches, exit 1.

## Where it is deliberately shallow

- **The fixtures are calibrated, not natural.** The first three are engineered so all five checks land in one class (all PASS / all FLAG / all FAIL). Real dossiers are mixed. `04-company-mixed` (added 2026-10-23) is the first mixed one: 2 PASS, 2 FLAG, 1 FAIL, for a company; see below.
- **Layer 1 checks form, not truth.** `checks.py` confirms a citation resolves; it cannot confirm the cited provision *supports* the finding. That is layer 2 (`compliance-judge.md`), which is a human/agent sample, not an automated gate. A report could cite a real but wrong provision and pass layer 1. That is by design (Torres's split), but it is a real limit to state plainly.
- **The reports were authored by the same session that built the auditor.** They demonstrate the format and the end-to-end flow honestly, but they are not an independent run. The stronger evidence is that a stranger can drop the folder into a fresh Claude project, feed it a fixture, and reproduce a report that passes `checks.py`.
- **The standard is excerpted, not exhaustive.** `reference/` holds only the provisions the five checks cite. A dossier problem outside those five checks (for example a retention-period question under Art. 5(1)(e)) would not be caught, because there is no check for it yet.

## Two things this eval does not touch

- It cannot verify that a vendor **does** what its dossier **says**. It audits the paperwork, not the running system.
- It does not deliver a legal verdict, and neither does the auditor. Both stop at "here is the gap, here is the provision, a human decides."

## The company cold run (2026-10-23)

`04-company-mixed`: a company in Köln pre-sorting job applications. The answer key was committed (`87e18bb`) before the run. A fresh agent got a copy of the drop-in folder **without** `audit/keys/`, `audit/reports/`, `audit/fixtures/`, `demo/` or `web/`, plus the dossier and the Einsatzkontext, and was told to follow the folder's run flow and keep a walk-log.

**Result:** 2 PASS / 2 FLAG / 1 FAIL, matching the key on every check; all `checks.py` gates pass, including key-match and module-consistency. Its BDSG section covers everything the key lists (applicants as Beschäftigte, § 26 with the EuGH caveat, works council, § 38 DSB duty, LDI NRW) and cites no DSG NRW. Receipts: `reports/04-company-mixed.report.md`, `.eval.md`, `.walk-log.md`.

**What the run broke, and the fixes** (from its walk-log):
1. **`render.py` silently rendered a single-column report as "0 Prüfschritte"**, which would hide a CLEAR FAIL if forwarded, while `rules.md` said both formats were fine. Fixed: `render.py` now exits 1 with an explanation; `rules.md` step 5 and the job template say to render the two-sided version.
2. **No place in the output format for the extra module, and its citations went unchecked** (`checks.py` only read finding blocks). Fixed: `## Ergänzendes Recht` is now part of the format, and `citations-resolve` / `module-consistency` read every citation in the report. Regression-tested with a phantom and a foreign-module citation planted in that section.
3. **The § 38 DSB instruction contradicted the PASS rule** (it said "name it in the Offene Entscheidung", but a PASS has none). Fixed: FLAG/FAIL → Offene Entscheidung; PASS → Bewertung + Ergänzendes Recht.

**Borderline calls the agent flagged itself:** PS-2 PASS (a strict reading of "silence is never a PASS" could make it a FLAG because the AVV's Satz-1 particulars are only shown elsewhere and sub-processors are named by function); PS-3 FLAG rather than FAIL (the upstream model has a training bar, so the escalation rule does not apply). Both match the key; PS-2 is the call to watch in future runs.

**Still true:** one agent, one dossier. It is real independent evidence, not a sample.
