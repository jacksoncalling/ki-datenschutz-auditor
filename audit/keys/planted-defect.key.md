# Answer key: planted-defect report

`fixtures/planted-defect.report.md` is a deliberately broken report. It exists to prove `checks.py` refuses bad work. Running the checker on it must exit **1** and flag exactly these six gates:

| Gate | Muss FAIL sein | Eingebauter Defekt |
|---|---|---|
| coverage | ja | PS-4 fehlt vollständig. |
| valid-severity | ja | PS-0 trägt die ungültige Klasse "UNKLAR". |
| has-citation | ja | PS-2 zitiert keine Provision. |
| citations-resolve | ja | PS-1 zitiert `[DSGVO-Art99-9]`, das es in reference/ nicht gibt. |
| open-decision | ja | PS-1 ist CLEAR FAIL ohne strukturierte "Offene Entscheidung"-Zeile. |
| count-honesty | ja | Kopf sagt CLEAR PASS 2, tatsächlich ist es 1. |

Kept outside `fixtures/` on purpose. Receipt of the run: `reports/planted-defects.eval.md`.
