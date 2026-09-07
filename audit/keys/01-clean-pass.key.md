# Answer key: fixture 01-clean-pass

Kept outside `fixtures/` on purpose: the fixture must not contain its own answer. This is what a correct audit of `fixtures/01-clean-pass/dossier.md` should conclude, and what `checks.py --key` verifies the produced report against.

Expected class per Prüfschritt:

| Prüfschritt | Erwartete Klasse | Warum |
|---|---|---|
| PS-0 | CLEAR PASS | DSFA zugeliefert, Anbieter liefert Systeminfos (Art. 35, DSK 2.3). |
| PS-1 | CLEAR PASS | System entscheidet nicht, dokumentiertes Vier-Augen-Prinzip mit Entscheidungsspielraum, Art.-22-Abs.-3-Rechte gewahrt. |
| PS-2 | CLEAR PASS | Art.-28-Abs.-3-konformer AVV, vollständige Unterauftragnehmerliste, EU-Standort. |
| PS-3 | CLEAR PASS | Ausdrückliche Trainingsausschluss-Klausel plus Default-off. |
| PS-4 | CLEAR PASS | Logik-Dokumentation plus allgemeinverständliche Zusammenfassung. |

Erwartete Gesamtzählung: CLEAR PASS 5 · NARROW FLAG 0 · CLEAR FAIL 0.

Purpose: proves the auditor does not manufacture problems. An auditor that flags a clean dossier is as broken as one that passes a bad one.
