# demo/retest — the corrected dossier, re-audited in platform format

The same test → correct → re-test loop as [`../stepintomore-loop/`](../stepintomore-loop/README.md), but this run produces the **two-sided platform report** (the `Deal-Vorprüfung` with a *Community* column and a *service provider* column, per [`../../perspectives.md`](../../perspectives.md)) instead of the single-column report.

The point of keeping it separate: it proves `audit/checks.py` validates **both** report formats. The checker parses the platform table (one severity per row, both action columns filled, every citation resolving against `reference/`) exactly as it parses the single-column format. A cold run that produced the platform format used to be unparseable; this folder is the frozen evidence that it now passes.

## What is here

- `RETEST_METHOD.md` — the expectation (5/5 CLEAR PASS), frozen **before** the re-run so it cannot be shaped to the result.
- `input/` — the corrected document set: each gap the first audit flagged, closed exactly as the report's *service provider: next proof* column asked (full Art. 28(3) a–h catalog and disclosed sub-processors in the AVV, explicit training exclusion plus default-off in the terms, a plain-language logic explanation, and a supplied DSFA).
- `report.md` — the re-audit, in the two-sided platform format: **5 CLEAR PASS, 0 FLAG, 0 FAIL**.
- `report.html` — the same report rendered as a forwardable one-pager (`render/render.py`).
- `eval.md` — the receipt: `checks.py` run on `report.md`, every gate PASS, all 5 citations resolve.

## The first audit it re-tests

The original run that returned 1 CLEAR PASS + 4 NARROW FLAG is the Step Into More ↔ Stadt Aachen job. The full flag → fix → pass narrative, with the layer-2 judge notes, lives in [`../stepintomore-loop/README.md`](../stepintomore-loop/README.md). This folder is the platform-format cut of the same corrected set.

## Re-run it yourself

```bash
python audit/checks.py demo/retest/report.md        # exits 0, every citation resolves
```
