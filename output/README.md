# output/

Where produced reports land. When you operate this folder on real vendor documents (see the "Run flow and where to save" section in `rules.md`), save both the report and its rendered page here:

```
output/<anbieter>-<YYYY-MM-DD>.md      the audit report (single-column or platform format)
output/<anbieter>-<YYYY-MM-DD>.html    the one-pager, from: python render/render.py <report> -o <html>
```

Before saving, the report must pass its own auditor: `python audit/checks.py output/<report>.md` (exit 0). A report that fails its own checks does not belong here.

Per-run products in this folder are git-ignored (each run is specific to a vendor and often not for publication); this `README.md` is kept so the folder and its purpose travel with the repo. The synthetic worked example lives in `demo/` instead.
