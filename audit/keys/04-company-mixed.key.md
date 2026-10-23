# Answer key: fixture 04-company-mixed

Kept outside `fixtures/`. Correct conclusion for `fixtures/04-company-mixed/dossier.md`, audited with `fixtures/04-company-mixed/einsatzkontext.md` (a company in NRW pre-sorting job applications). Written and committed **before** the cold run, so the test cannot be shaped to the result.

| Prüfschritt | Erwartete Klasse | Warum |
|---|---|---|
| PS-0 | CLEAR PASS | The vendor states a DSFA is required and supplies a Muster-DSFA plus the system information the company needs to run its own (Art. 35, DSK 2.3). |
| PS-1 | CLEAR FAIL | "Auto-Absage" sends rejections to applicants with no human check, switched on by default: the DSK 1.6 example of a violation of Art. 22 Abs. 1, quotable from the dossier. |
| PS-2 | CLEAR PASS | AVV names the Art. 28 Abs. 3 elements, closed sub-processor list with 30-day notice and objection right (Art. 28 Abs. 2), processing and support only in Germany, no third-country transfer. |
| PS-3 | NARROW FLAG | Training of the underlying language models is excluded and the model operator is bound, so the conditional escalation to FAIL does not apply. But "Rückmeldungen … zur Verbesserung des Dienstes" leaves open whether the ranking model is trained on the company's data and whether across customers, and history (12 months) is on by default, with no default-off. Ambiguity and missing default-off are the NARROW FLAG signature (DSK 1.9, 2.5). |
| PS-4 | NARROW FLAG | Technical documentation of the logic exists, but no plain-language explanation for applicants (DSK 1.8, Art. 13 Abs. 2 lit. f). |

Erwartete Gesamtzählung: CLEAR PASS 2 · NARROW FLAG 2 · CLEAR FAIL 1.

## What else a correct report contains (checked by reading, not by `checks.py --key`)

- **Einsatzkontext line** naming the company, the use (applicant pre-sorting) and the affected people (Bewerber:innen).
- **Geprüft gegen** names the BDSG, not DSG NRW; no `[DSG-NRW-…]` citation anywhere (`checks.py` module-consistency gate enforces this).
- **Zuständige Aufsicht:** LDI NRW (company seat in Köln, `[BDSG-§40-1]`).
- **Ergänzende Ebene / BDSG:** applicants count as Beschäftigte (`[BDSG-§26-8]`); processing for the hiring decision is employee-data processing (`[BDSG-§26-1]`, with the EuGH C-34/21 caveat: classification, not sole legal basis); the works council's rights stay untouched (`[BDSG-§26-6]`); because a DSFA is required, the company must have a Datenschutzbeauftragte(n) regardless of size (`[BDSG-§38-1]`).
- **PS-1** may cite `[BDSG-§37-1]` only to note that it does not help here (insurance contracts only).
- No municipal wording ("Kommune", "Bürger") for this company.

Purpose: the first company case, and the first fixture that mixes all three classes, as `REVIEW.md` asked for ("one mixed fixture with a genuine CLEAR FAIL among passes"). It also exercises the BDSG module end to end.
