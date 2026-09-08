# Re-test: do the corrections hold?

Adam James's winning loop: test → correct the failures → feed the documents again and see whether the fixes actually clear. Frozen **before** the re-run so the expectation cannot be shaped to the result.

## What is being tested

The first audit (`../stepintomore-aachen-2026-09-08/report.md`) returned 1 CLEAR PASS + 4 NARROW FLAG. The `input/` here is the **corrected** document set: each flagged gap closed exactly as the report's "Anbieter: nächster Nachweis" column asked. A cold agent auditing these corrected documents should now return mostly CLEAR PASS. If a gap that was "fixed" still flags, either the fix was incomplete or the checklist is miscalibrated, and that is the useful signal.

## The run (later, low-token)

1. Point a cold agent (or this folder) at `input/` here.
2. Produce `report.md`, then `python audit/checks.py report.md` (must exit 0), then render.
3. Compare the classes to the frozen expectation below.

## What was corrected (maps to the first audit's Anbieter actions)

| PS | War | Korrektur im input/ |
|---|---|---|
| PS-0 | FLAG (keine DSFA) | `05-dsfa.md`: DSFA nach Art. 35 durchgeführt, Anbieter liefert die Funktionsinformationen zu. |
| PS-1 | PASS | unverändert (4-Augen / HITL bleibt dokumentiert). |
| PS-2 | FLAG (AVV dünn, Subunternehmer "auf Anfrage") | `02-avv.md`: voller Art.-28-Abs.-3-Katalog lit. a–h; Unterauftragnehmerliste offengelegt (inkl. LLM-Anbieter, EU), Änderungsmitteilung + Widerspruchsrecht. |
| PS-3 | FLAG (kein Trainingsausschluss) | `04-agb.md`: ausdrücklicher vertraglicher Trainingsausschluss beim vorgelagerten LLM, Default-off für Training und Eingabe-Historie. |
| PS-4 | FLAG (keine Logik-Erläuterung) | `01-systemarchitektur.md`: allgemeinverständliche Erläuterung der Funktionsweise/Logik für Bürgerauskünfte ergänzt. |

## Frozen expectation (recorded before the re-run)

| Prüfschritt | Erwartete Klasse nach Korrektur |
|---|---|
| PS-0 | CLEAR PASS |
| PS-1 | CLEAR PASS |
| PS-2 | CLEAR PASS |
| PS-3 | CLEAR PASS |
| PS-4 | CLEAR PASS |

Erwartet gesamt: **CLEAR PASS 5 · NARROW FLAG 0 · CLEAR FAIL 0.**

A clean 5-of-5 proves two things at once: the first audit's flags were real and closable, and the auditor recognises remediation instead of flagging forever. If any check stays FLAG, keep that result exactly as produced (do not smooth it), and treat it as the next thing to fix, in the corrected doc or in the checklist.
