# jobs/

One folder per audit job. Each job keeps the **submitted documents and the created ones together**, so an audit is a self-contained, reproducible record: anyone can open the job folder and re-check the report against the exact documents it was based on.

## Structure

Copy `_template/` to start a job (ICM: instantiate by copying, don't start blank):

```
jobs/<anbieter>-<YYYY-MM-DD>/
  input/          the submitted vendor documents (AVV, TOMs, system description, terms)
  report.md       the audit report (single-column or platform format)
  report.html     the rendered one-pager  (render/render.py report.md -o report.html)
  eval.md         the checks.py receipt    (python audit/checks.py report.md --report eval.md)
```

The run flow that fills this in is in `rules.md` ("Run flow and where to save").

## Confidentiality

Real submitted documents are vendor/municipality confidential. **Everything under `jobs/` is git-ignored except this README and `_template/`,** so real input documents and real reports never enter the public repository. Do not force-add a real job folder.

**Publishable vs confidential is a location choice, not a gitignore exception.** If a run is safe to publish (your own synthetic data, or evidence for a submission), copy it into `demo/` (which is tracked), the way `demo/stepintomore-loop/` was. Keep `jobs/` for confidential real-client work only. That way the ignore rule stays simple and never has to be poked with per-folder exceptions.
