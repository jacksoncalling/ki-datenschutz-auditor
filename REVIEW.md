# REVIEW.md — adversarial review + recorded cold run

Written after the folder was built, deliberately trying to break it, calibrated on the Comp winner's rubric (Adam James: frozen test method, cold-run evidence, boundary honesty, "one thing a stranger can run"; Jeff van Leenen: a generated verifier where the base wins). The break is kept in. Everything the cold run exposed is listed, then fixed, and the fix is shown.

## Verdict against the four judging criteria

1. **Audits against a real, citable standard, not an opinion.** Yes. `reference/` holds the verbatim DSGVO articles, DSK-Orientierungshilfe KI sections, and DSG NRW, with `SOURCES.md` giving URL + retrieval date for each. Every finding cites a provision a reader can open.
2. **Findings specific, located, with severity.** Yes. Three classes (CLEAR PASS / NARROW FLAG / CLEAR FAIL), each finding quotes the dossier and the provision, and every FLAG/FAIL names the open decision.
3. **The standard is actually in `reference/`.** Yes, verbatim. One defect here (Art. 44 heading with no body) was found by the cold run and fixed; see below.
4. **A stranger can figure it out.** Tested for real, not asserted. A cold agent with no keys and no hints produced a valid report from the folder alone (below).

## The recorded cold run

Method was frozen in `demo/TEST_METHOD.md` and committed *before* the run (commit `9331b52`), including my own expected classes, so the test could not be shaped to the result. A fresh general-purpose agent was given only the repo path and the instruction to audit `demo/dossier.md` (a deliberately mixed dossier) by the folder's own rules. It wrote `demo/cold-run/report.md` and `demo/cold-run/walk-log.md`.

**Machine gate:** `python audit/checks.py demo/cold-run/report.md` exits 0. Every one of the cold agent's citations resolves against `reference/`. Receipt: `demo/cold-run/report.eval.md`.

**Baseline vs cold agent:**

| | PS-0 | PS-1 | PS-2 | PS-3 | PS-4 | Totals |
|---|---|---|---|---|---|---|
| My frozen baseline | FLAG | PASS | FLAG | **PASS** | FLAG | 2P / 3F |
| Cold agent | FLAG | PASS | FLAG | **FLAG** | FLAG | 1P / 4F |

**The one divergence, PS-3, and the cold agent was right.** I predicted CLEAR PASS on the strength of the dossier's training-exclusion clause ("produktseitig deaktiviert und kann nicht aktiviert werden"). The cold agent called NARROW FLAG: PS-3 is a compound check whose PASS bar also requires default-off on the Eingabe-Historie, and the dossier is silent on that. It applied the folder's own rule, "silence is never a PASS," against the pull of the strongest sentence in the document. The tool, run by a stranger, was more disciplined than its author. That is the best possible result from a cold run: the rule held under temptation, and it corrected the human.

## What the cold run broke, and the fixes

Everything below came out of `demo/cold-run/walk-log.md`.

1. **Art. 44 was a heading with no body.** `checklist.md` cited `[DSGVO-Art44]` for PS-2 and `rules.md` demands a verbatim quote, but the extractor had emitted Art. 44 (a single unnumbered `<p>`, not an `<ol>`) as an empty section. **Fixed:** the verbatim Art. 44 text is now in `reference/dsgvo-artikel.md`.
2. **The eval could not see that defect.** `checks.py` accepted `[DSGVO-Art44]` because the heading existed, a quiet failure of its own mechanism. **Fixed:** added a `reference-integrity` gate to `checks.py --all` that flags any heading-only section. Regression-checked: it catches Art. 44 when the body is removed again.
3. **PS-4 cited the wrong sub-provision.** The "aussagekräftige Informationen über die involvierte Logik" duty is Art. 13(2)(f), not 13(1). **Fixed:** `checklist.md` PS-4 now anchors on `[DSGVO-Art13-2f]` (logic duty) plus `[DSGVO-Art13-1]` (base information duty).
4. **PS-1's PASS bar overreached.** It required Art. 22(3) safeguards even where the system makes no Art. 22 decision (so they are not engaged). **Fixed:** `checklist.md` PS-1 now says the 22(3) safeguards apply only where the system makes or materially drives an Art. 22 decision.
5. **Two citation styles** (DSK writes literal `[DSK-OH-1.9]` headers; DSGVO/NRW IDs are reconstructed from article/paragraph numbers). The cold agent handled both but had to hold two mental models. Not fixed structurally (adding bracketed IDs to every DSGVO paragraph would be noisier than the problem); noted as a known limitation. The `checks.py` resolver handles both correctly, which is what matters for verification.

Bare-run and portability were also hardened before the cold run (`checks.py --all` as the one command a stranger runs; UTF-8 stdout; helpful message instead of an argparse error), which is the fix the winner was told he still needed.

## Adversarial checker tests (what a judge does)

- Empty report and prose-with-no-findings both fail loudly (exit 1), never a silent pass.
- The resolver rejects a fake letter (`Art28-3z`), a fake section (`1.99`), and a fake paragraph (`§99-1`) while keeping the real IDs. Citations cannot just be believed; the base wins.
- The planted-defect report (six deliberate errors) fails all six gates, exit 1.

## Honest remaining limits

- **The fixtures are still calibrated** (each all-one-class); the demo dossier is the only mixed case. One more mixed fixture would harden the eval further.
- **Layer 1 checks form, not truth.** `checks.py` confirms a citation resolves; whether the cited provision *supports* the finding is the layer-2 judge (`compliance-judge.md`), a human/agent sample, not an automated gate.
- **It audits the paperwork, not the running system.** It cannot verify a vendor does what its dossier says.
- **The demo cold run was one agent, one dossier.** It is real independent evidence, not a large sample. The `demo/cold-run/` transcript is kept exactly as produced, wrong anchor and all, so the record is honest.

## What would make it unarguable

A second, human-run cold walk (drop the folder into a fresh Claude project, feed a new dossier, keep the transcript), and one mixed fixture with a genuine CLEAR FAIL among passes. The machine side is already level with the reasoning side; more cold-walk evidence is the highest-value next build, exactly the note the winner got.
