# FINDINGS.md — the honest read of the first pass

Kept in on purpose. An eval that only advertises its strengths is doing the same thing a rubber-stamp auditor does.

## What this eval genuinely proves

- Every finding in every produced report cites a provision that **actually exists** in `reference/`. This is mechanical and complete: `checks.py` resolves 91 valid IDs from the standard and rejects anything else.
- The auditor **discriminates**: it passes a clean dossier, flags an ambiguous one, and fails a violating one, verified against answer keys held outside the fixtures.
- The checker **refuses**: six planted defects, six catches, exit 1.

## Where it is deliberately shallow

- **The fixtures are calibrated, not natural.** Each of the three is engineered so all five checks land in one class (all PASS / all FLAG / all FAIL). Real dossiers are mixed. This makes the discrimination legible but easy; a harder test would be a dossier that passes three checks and fails two. Adding one mixed fixture is the obvious next step.
- **Layer 1 checks form, not truth.** `checks.py` confirms a citation resolves; it cannot confirm the cited provision *supports* the finding. That is layer 2 (`compliance-judge.md`), which is a human/agent sample, not an automated gate. A report could cite a real but wrong provision and pass layer 1. That is by design (Torres's split), but it is a real limit to state plainly.
- **The reports were authored by the same session that built the auditor.** They demonstrate the format and the end-to-end flow honestly, but they are not an independent run. The stronger evidence is that a stranger can drop the folder into a fresh Claude project, feed it a fixture, and reproduce a report that passes `checks.py`.
- **The standard is excerpted, not exhaustive.** `reference/` holds only the provisions the five checks cite. A dossier problem outside those five checks (for example a retention-period question under Art. 5(1)(e)) would not be caught, because there is no check for it yet.

## Two things this eval does not touch

- It cannot verify that a vendor **does** what its dossier **says**. It audits the paperwork, not the running system.
- It does not deliver a legal verdict, and neither does the auditor. Both stop at "here is the gap, here is the provision, a human decides."
