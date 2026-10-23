# The auditor's eval

An auditor you cannot check is just an opinion generator. This folder is the proof that the KI-Datenschutz-Prüfassistent earns trust: it runs on the auditor's **output reports**, not on its factory files, the way `tests/` is evidence about the work rather than part of it. The auditor never reads this folder.

## Two layers

**Layer 1, `checks.py`** (deterministic, no model). Given a report, it verifies:

| Gate | Invariant |
|---|---|
| coverage | every required Prüfschritt (PS-0..PS-4) is present |
| valid-severity | every finding is CLEAR PASS / NARROW FLAG / CLEAR FAIL |
| has-citation | every finding cites at least one provision |
| citations-resolve | every cited ID actually exists in `reference/` (no phantom cites) |
| open-decision | every NARROW FLAG / CLEAR FAIL names an "Offene Entscheidung" |
| count-honesty | the header counts match the findings actually present |
| module-consistency | if the header names one extra module (BDSG or DSG NRW), no citation comes from the other one |
| key-match | (optional, `--key`) each Prüfschritt's class matches the answer key |

The clever part is `citations-resolve`: `checks.py` reads `reference/` at startup and builds the set of valid IDs from the actual structure of the standard (every article, paragraph, letter; every DSK section; every DSG-NRW paragraph). A finding that cites `[DSGVO-Art99-9]` fails, because Art. 99(9) is not in the reference. That is the mechanical version of the comp's own rule: every finding cites a provision a reader can open.

**Layer 2, `compliance-judge.md`** (one binary judgment). The call code cannot make: does the cited provision actually *support* the finding's class? Made by a human or an agent on a small sample, kept deliberately simple.

## Run it

```bash
# validate a single report
python audit/checks.py audit/reports/03-clear-fail.report.md

# validate against the answer key too
python audit/checks.py audit/reports/03-clear-fail.report.md --key audit/keys/03-clear-fail.key.md --report audit/reports/03-clear-fail.eval.md
```

Exit code 0 if every hard gate passes, 1 if any fails. Usable as a CI gate before a report is trusted.

## The fixtures and what they prove

Four synthetic vendor dossiers in `fixtures/`: one per outcome, so the auditor is shown to *discriminate*, not just pass, plus one mixed company case:

- `01-clean-pass/` → a compliant, EU-hosted, closed-system tool → all five checks CLEAR PASS.
- `02-narrow-flags/` → an ambiguous SaaS that is silent on the load-bearing points → all five NARROW FLAG. This is the class the tool exists for.
- `03-clear-fail/` → a US open system with autonomous decisions and training on customer data → all five CLEAR FAIL.
- `04-company-mixed/` → a **company** (Köln, works council) pre-sorting job applications, with an `einsatzkontext.md` next to the dossier → 2 PASS, 2 FLAG, 1 FAIL (auto-sent rejections). The first mixed fixture and the first that exercises the BDSG module. Its key was committed before a cold agent ran it; the cold run matched the key on all five checks (`reports/04-company-mixed.*`, including the agent's `walk-log.md`).

The answer keys live in `keys/`, **outside `fixtures/`**, so a fixture never carries its own answer into the room.

## The receipts (`reports/`)

- `01-clean-pass.report.md`, `02-narrow-flags.report.md`, `03-clear-fail.report.md`: the auditor's actual output on each fixture.
- `*.eval.md`: `checks.py` run on each report. All pass, all match their key.
- `planted-defects.eval.md`: `checks.py` run on `fixtures/planted-defect.report.md`, a report with six deliberate defects. Every one is caught; the run fails with exit 1, as it must. An auditor that only ever passes is worthless; this is the proof it refuses. See `keys/planted-defect.key.md`.

## Pointing it at another reference set or language

Everything configurable lives in `conventions.json`: the reference directory and file names, the valid severities, the required checks, and the open-decision marker. `checks.py` holds no conventions of its own. To run the same eval on, say, a Bayern build, swap the state file in `reference/` and, if needed, edit `conventions.json`. Nothing in the code changes.

See `FINDINGS.md` for the honest read of the first pass, including where this eval is deliberately shallow.

## Checking the BDSG module against the official law

`verify_bdsg.py` compares every Absatz in `reference/bdsg.md` with the official BDSG XML from gesetze-im-internet.de (by default the daily QuantLaw archive of it, because the official site is not reachable from every environment) and prints the official "Stand". Exit 0 if all match. Run it whenever the BDSG may have changed: `python audit/verify_bdsg.py`. Last receipt: `reports/bdsg.verify.md`.
