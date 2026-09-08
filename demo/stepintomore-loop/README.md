# Test → correct → re-test: does a fixed dossier actually pass?

The discipline that separates an auditor from an opinion generator is that it **flags real gaps and then recognises when they are closed**. This folder is that loop, run end to end by a **cold agent** (a fresh session given only the folder and the documents), on a real dossier: the Step Into More ICM platform proposed to the Stadt Aachen.

It is published in full because the subject is our own platform, nothing confidential. Real client jobs stay in the git-ignored `jobs/`; publishable runs like this one live here in `demo/`.

## 1. First audit — the flags (`01-first-audit/`)

The cold agent audited the original four documents in `01-first-audit/input/` and returned **1 CLEAR PASS, 4 NARROW FLAG** (`report.md`):

| Prüfschritt | Erste Klasse | Warum |
|---|---|---|
| PS-0 DSFA | NARROW FLAG | keine DSFA erwähnt |
| PS-1 Human-in-the-Loop | **CLEAR PASS** | 4-Augen-Prinzip ausdrücklich dokumentiert |
| PS-2 Auftragsverarbeitung | NARROW FLAG | AVV ohne Art.-28-Abs.-3-Katalog, Subunternehmer nur „auf Anfrage" |
| PS-3 Trainingsverbot | NARROW FLAG | AGB räumen ein: kein Trainingsausschluss |
| PS-4 Transparenz | NARROW FLAG | keine bürgerverständliche Logik-Erläuterung |

`layer2-judge.md` is the second check: do those findings actually match the source text? Four of five are fully supported; PS-3 was the one genuine judgment call (silent-vs-permits training), which is what sharpened the checklist's PS-3 rule (a missing exclusion becomes a CLEAR FAIL once personal data actually flows to the upstream model).

## 2. Correct, then re-test (`02-corrected-retest/`)

Each flagged gap was then closed in the documents, exactly as the first report's "Anbieter: nächster Nachweis" column asked: the AVV got the full Art. 28(3) a–h catalog and a disclosed sub-processor list, the AGB got an explicit training-exclusion plus default-off, a plain-language logic explanation was added, and a DSFA was supplied. Those corrected documents are in `02-corrected-retest/input/`.

`RETEST_METHOD.md` froze the expectation (5/5 CLEAR PASS) **before** the re-run. A fresh cold agent then audited the corrected set and returned exactly that: **5 CLEAR PASS, 0 FLAG, 0 FAIL** (`report.md`), and it ran the eval on its own output (`eval.md`, `checks.py` exit 0, every citation resolves).

## Why this is the evidence that matters

- The four flags were **real and closable**: fix the documents, and the same auditor passes them. It does not flag forever.
- The re-run was **verified, not eyeballed**: `checks.py` confirms coverage, resolvable citations, and honest counts on both the first and the corrected report.
- The expectation was **frozen before the run**, and the cold agent **ran the audit itself** the second time (the folder's run-flow held where the first cold run had skipped it).

That is the loop the strongest audits are built on: prove you catch the gap, then prove the fix clears it.
