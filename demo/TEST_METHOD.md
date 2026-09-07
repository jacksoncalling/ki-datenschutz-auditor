# TEST_METHOD.md — frozen before the run

Written and committed **before** the cold agent runs, so the method cannot be shaped to the result. (Discipline borrowed from Adam James, Comp Cartographer winner: freeze the test, then let it hurt.)

## What is being tested

Whether a **cold agent**, given nothing but this folder and one vendor dossier, produces a valid, well-formed, correctly reasoned audit, by following the folder's own instructions alone. If the folder is built right, a stranger's agent reaches a usable report without coaching. If it is not, we find out here.

## The setup

- **Cold agent:** a fresh general-purpose agent with no access to this conversation, no keys, no hints about expected outcomes.
- **Given to it:** the repository path, and the instruction to act as the auditor by reading `identity.md`, `rules.md`, `checklist.md` and `reference/`, then audit `demo/dossier.md`.
- **Not given to it:** any expected classes, any answer key, any of my reasoning. `demo/dossier.md` was written to be genuinely mixed (not all-PASS or all-FAIL), and no key for it exists anywhere in the repo.
- **It writes:** `demo/cold-run/report.md` (the audit, in the format `rules.md` defines) and `demo/cold-run/walk-log.md` (which files it read, in what order, and anything that confused it or that it got wrong).

## What counts as a pass

1. **Machine gate:** `python audit/checks.py demo/cold-run/report.md` exits 0 (coverage, valid severity, every citation resolves against `reference/`, discretion lines present, header counts honest). This is run *after* the cold agent finishes, on whatever it produced.
2. **Independent-judgment check:** my own expected classes for the mixed dossier (recorded below, before reading the cold agent's output) versus what the cold agent concluded. Divergences are reported, not hidden.

## My expected classes (recorded before the run)

For `demo/dossier.md`, reading it against `checklist.md`:

| Prüfschritt | Erwartet | Grund |
|---|---|---|
| PS-0 | NARROW FLAG | DSFA nur "empfohlen", nicht durchgeführt, keine konkrete Zulieferung. |
| PS-1 | CLEAR PASS | System entscheidet nicht, dokumentierter Prüf-/Freigabeschritt mit Verantwortung. |
| PS-2 | NARROW FLAG | AVV vorhanden, EU-Hosting, aber Unterauftragnehmerliste nicht beigefügt und US-Konzern-Support-Zugriff/Übermittlungsmechanismus ungeklärt. |
| PS-3 | CLEAR PASS | Ausdrücklicher Trainingsausschluss, produktseitig deaktiviert (Eingabe-Historie bleibt ein kleiner Nebenpunkt). |
| PS-4 | NARROW FLAG | Technische Doku vorhanden, aber keine bürgerverständliche Erläuterung für Art. 13/15. |

Erwartet gesamt: CLEAR PASS 2 · NARROW FLAG 3 · CLEAR FAIL 0.

This table is the human baseline. A strong cold run lands on or very near it; where it does not, that is either an auditor-design gap or a defensible reading, and the review says which.
