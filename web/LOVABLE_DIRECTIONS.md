# Building the KI-Anbieter-Check in Lovable: step by step

What to do, in order, to turn this repo into the website. The prompts you paste are in `LOVABLE_PROMPTS.md`; what the site must do is in `USER_STORIES.md`; the why is in `PLAN.md`. Plan for about **one afternoon** for steps 1–6 and a second session for testing (step 7).

You don't copy any auditor files into Lovable. The website loads the auditor from this repo's **bundle** (`web/bundle/`) through a fixed web address. When the auditor improves, you point the site at the new bundle with a single setting (step 9).

---

## 0. Before you start (one time, ~15 minutes)

| What | Where | Note |
|---|---|---|
| Lovable account on a paid plan | lovable.dev | Cloud features (database, login, storage, backend functions) need it. |
| Anthropic API key | console.anthropic.com → API Keys | Copy it once, straight into Lovable (step 4). Set a **monthly spend limit** in the console first (e.g. €20). |
| The bundle tag `bundle-v1` | this repo | Created once PR #1 is merged (Claude can do it). It pins the website to one tested version of the auditor. |
| Impressum details | you | Name, address, contact for the legal pages (step 6). |

Check that the bundle is reachable: open
`https://raw.githubusercontent.com/jacksoncalling/ki-datenschutz-auditor/bundle-v1/web/bundle/VERSION`
in a browser. You should see four short lines (`source_commit`, `built`, `valid_ids: 116`, `system_prompt_chars`).

---

## 1. Create the project and the front end (prompt 1)

1. In Lovable: **New project**. Name it e.g. `ki-anbieter-check`.
2. Paste **Prompt 1** from `LOVABLE_PROMPTS.md`.
3. Click through the result: landing page → "Prüfung starten" → the 4-step wizard → the mock report.
4. Fix what you don't like with short follow-up messages ("make the headline smaller", "the counters should be in one row on mobile"). One change per message works best.

✅ **Done when:** you can click through the whole flow on your phone and the mock report shows 1 PASS / 3 FLAG / 1 FAIL.
🎥 Building Out Loud: record the click-through.

## 2. Turn on Lovable Cloud and connect GitHub

1. In the project: enable **Lovable Cloud** (database, auth, storage, functions).
2. Settings → **GitHub** → connect, and let Lovable create its own repository for the project. This is *not* the auditor repo; it holds the website's code and lets Claude read it later if something needs debugging.
3. Check the hosting region if Lovable offers a choice and pick the EU (Frankfurt). If it doesn't offer one, note that for the Datenschutzerklärung (step 6) and see `PLAN.md` section 8c.

## 3. Accounts, database, storage (prompt 2)

1. Paste **Prompt 2**.
2. Test with **two different e-mail addresses**: create an audit with the first one, sign in with the second, and confirm the second account sees nothing of the first (no audits, no files).
3. Try to upload more than 20 MB, and start a fourth audit in a month: both should give a friendly German message.

✅ **Done when:** the two-account test passes. Nothing is checked yet; audits stop at "queued".

## 4. Add the three secrets

In Lovable: **Cloud → Secrets**, add:

| Name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | your key from step 0 |
| `AUDIT_MODEL` | `claude-sonnet-5-5` |
| `BUNDLE_BASE_URL` | `https://raw.githubusercontent.com/jacksoncalling/ki-datenschutz-auditor/bundle-v1/web/bundle/` |

Never paste the API key into the chat or the code. Lovable keeps secrets on the server side only.

## 5. The audit engine (prompt 3)

1. Paste **Prompt 3**. It is long on purpose: it spells out the checks so the website gives exactly the same result as the folder.
2. If Lovable asks questions, answer from `PLAN.md` / `USER_STORIES.md`, or bring the question to Claude.
3. First test: start an audit with the file `audit/fixtures/01-clean-pass/dossier.md` from this repo (download it from GitHub), organisation **Öffentliche Stelle, NRW**. Expect **5× CLEAR PASS** after 1–3 minutes.

✅ **Done when:** that test gives 5× CLEAR PASS, and the audit row shows the model and the bundle version.

If it fails, the audit page shows the error. The common ones:
- "Prüfassistent nicht erreichbar" → `BUNDLE_BASE_URL` is wrong or the tag doesn't exist yet. It must end with `/web/bundle/`.
- "Zeitüberschreitung" → ask Lovable: "the run-audit function times out; make sure it streams the Claude call and runs in EdgeRuntime.waitUntil".
- A gate error such as "Zitate existieren nicht im Standard" → the checks did their job. Click "Erneut versuchen" once; if it repeats, send Claude the error text.

## 6. Report page, PDF, housekeeping (prompts 4 and 5)

1. Paste **Prompt 4** (report polish + **PDF download**). Check user story **US-6** in `USER_STORIES.md` point by point: phone download, umlauts, footer on every page, text selectable, prints fine in black and white.
2. Paste **Prompt 5** (delete, 30-day auto-delete, legal pages). Fill in the Impressum and Datenschutzerklärung placeholders yourself. Those are your legal texts; the generated drafts are only a start.

## 7. Test before you share (second session, ~1 hour)

Run these through the live site and compare with the expected results in this repo:

| Upload (from `audit/fixtures/`) | Wizard settings | Expected |
|---|---|---|
| `01-clean-pass/dossier.md` | Öffentliche Stelle, NRW | 5× CLEAR PASS |
| `02-narrow-flags/dossier.md` | Öffentliche Stelle, NRW | 5× NARROW FLAG |
| `03-clear-fail/dossier.md` | Öffentliche Stelle, NRW | 5× CLEAR FAIL |
| `04-company-mixed/dossier.md` | Unternehmen, NRW; use case and data from `04-company-mixed/einsatzkontext.md` | PASS · FAIL · PASS · FLAG · FLAG; cites the BDSG, no DSG NRW |
| `demo/dossier.md` | Öffentliche Stelle, NRW | PS-3 must be NARROW FLAG |

Then:
- Download a report as Markdown and run `python audit/checks.py <file>` on it (or send it to Claude): it must pass.
- **Cheaper model test:** change `AUDIT_MODEL` to `claude-haiku-5-5` and run the table again. If every row still matches, keep Haiku (roughly 10× cheaper); otherwise switch back.
- Upload something that is clearly not an AI tool: the page should say "Prüfung nicht anwendbar".

✅ **Done when:** every row matches. Then share the link with the first outside testers.

## 8. Go live

- Connect your domain (e.g. a subdomain of stepintomore.co) in Lovable's domain settings.
- Run the auditor on your own site's vendors (Lovable/Supabase, Anthropic) and post the result: a good Building Out Loud piece (`PLAN.md` 8c).

## 9. When the auditor changes later

The website always uses the bundle the tag points to, so changes in this repo don't reach the site by accident.

1. Change the auditor in this repo (rules, checklist, law modules).
2. Rebuild and test: `python web/export_bundle.py`, then `python web/test_parity.py` and `python audit/checks.py --all` must all pass. Commit `web/bundle/`.
3. Tag the commit `bundle-v2` (Claude can do steps 1–3).
4. In Lovable: change the secret `BUNDLE_BASE_URL` to `…/bundle-v2/web/bundle/`. No new prompt and no new deploy are needed.
5. Re-run the step 7 table. Each audit stores the bundle version it ran on, so old reports stay traceable.

---

## What's in the bundle

| File | Used for |
|---|---|
| `system-prompt.md` | Claude's instructions: the auditor + the verbatim law (DSGVO, DSK guidance, DSG NRW, BDSG), with a web-mode preamble. ~88k characters, cached by the API. |
| `report.schema.json` | the exact JSON structure Claude must return |
| `valid-ids.json` | the 116 citation IDs that exist in the law files; anything else is rejected |
| `gates.json` | the check settings (five checks, three classes, citation pattern, which module forbids which citations) |
| `examples/*.json` + `*.report.md` | real reports as JSON plus the exact Markdown the site must generate from them; good mock data |
| `VERSION` | which repo commit the bundle was built from |

The reference code behind the engine's checks and Markdown is `web/reference_impl.py`, and `web/test_parity.py` proves that anything passing it also passes `audit/checks.py`.
