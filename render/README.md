# render/ — markdown report to HTML one-pager

A small, dependency-free renderer that turns a **platform report** (the two-sided markdown from `perspectives.md`) into a standalone, styled HTML page a founder or a Kommune can actually be shown or forwarded.

Same idea as a template-and-data split: `template.html` is the fixed design (structure + CSS + slots), `render.py` reads the report's markdown, parses it into content, and pours it into the slots. The content is **not hand-written**; it comes from the auditor's own output. So the page is a translation of the folder's report, not a separate artifact that could drift from it.

Content is baked in at generation time (no runtime JavaScript), so the page reads correctly at rest, in a thumbnail, or when forwarded.

## Run it

```bash
# renders demo/platform-report.md -> demo/platform-report.html
python render/render.py

# or point it at any platform report
python render/render.py path/to/report.md -o out.html
```

## What it parses

From the platform report markdown:
- the title line (`# Deal-Vorprüfung: <Produkt> (<Anbieter>) ↔ <Kommune> (<Region>)`),
- the meta lines (`Geprüft gegen:`, `Datum:`, `Zuständige Aufsicht:`),
- the `Kurz:` verdict (split into a lead clause and the rest),
- the findings table rows (`| [PS-n] … | Klasse | Standard | Kommune … | Anbieter … |`).

The **counts and the outcome strip are derived from the findings themselves**, not read from the header, so the summary can never disagree with the rows. Citation IDs are pulled straight from the `Standard` column, so every chip on the page is a real provision ID from `reference/`.

## Files

```
template.html   the design: page shell, CSS, and {{slots}} + a {{FINDINGS}} block
render.py       parse the markdown, build the finding rows, fill the template
```

To restyle the page, edit `template.html`; the parse logic in `render.py` does not change. To change what is parsed, edit `render.py`; the design does not change.

## Honesty note

This renders the two-sided report. The two-sided report is itself a rendering of the canonical single-column audit (see `perspectives.md`), which is what `audit/checks.py` validates. So the chain is: audited dossier → canonical report (machine-checked) → two-sided markdown → this HTML. The design and colors are a presentation layer; the findings, classes, and citations trace back to a real audit against the standard in `reference/`.

*Pattern borrowed from the discovery-triage-operator's `demo-scroll` template.*
