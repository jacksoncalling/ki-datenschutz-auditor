# KI-Datenschutz-Prüfassistent as a web service — plan

**Goal:** a website where **any organisation** that wants to use an AI tool can ask *"Is this vendor okay for what we want to do?"*: say what they want to use it for, upload the vendor's paperwork (or paste links), and get a German pre-check report with every finding tied to a real provision. Kommunen remain a supported option. Built with Lovable, shown publicly as part of Building Out Loud.

**Status (2026-10-23):** the website isn't built yet. The folder is ready for companies: the Einsatzkontext rule and the BDSG module are in (BDSG verified against the official text). Files next to this one:
- `USER_STORIES.md`: what users can do, with acceptance criteria (including **PDF download**, US-6)
- `LOVABLE_PROMPTS.md`: copy-paste prompts to build it in Lovable

Audience: companies first, Kommunen as an option. Model: Sonnet 5.5 by default, Haiku 5.5 tested as the cheap option.

---

## 1. The one big idea: the folder stays the brain, the website is a shell

The website does not re-invent the auditor. It:

1. **Sends the folder to Claude as the system prompt** (method + verbatim law).
2. **Sends the user's use case + the vendor documents** as the input.
3. **Runs the same gates `audit/checks.py` runs** before a report is shown: all five checks present, valid class, every citation resolves to a real provision, every FLAG/FAIL has an *Offene Entscheidung*.
4. **Shows the result** as a page, plus downloads (**PDF**, Markdown, HTML; see `USER_STORIES.md` US-6).

So the "agent" is **one Claude call with the folder as its instructions, plus the gate check.** No agent loop, no sandbox. Simple means cheap, fast, and easy to explain out loud.

The GitHub repo stays the **single source of truth**. The site uses a pinned *bundle* of it, and each audit records which auditor version and model produced it.

---

## 2. Does "Kommune vs. company" change the check? Yes, but only at the edges

I went through the five checks against the law in `reference/`:

| Part of the check | Kommune | Company | Same? |
|---|---|---|---|
| PS-0 DSFA duty (Art. 35 DSGVO, DSK 2.3) | applies | applies | ✅ same |
| PS-1 human decision (Art. 22 DSGVO, DSK 1.6) | applies, **plus** administrative-law specifics (Verwaltungsakt, Ermessen, § 35a VwVfG) | applies, without the admin-law part | ⚠️ mostly same, one paragraph differs |
| PS-2 processor contract, sub-processors, data location (Art. 28, 44, DSK 2.1) | applies | applies | ✅ same |
| PS-3 no training on your data, privacy by default (DSK 1.9/2.5, Art. 5) | applies | applies | ✅ same |
| PS-4 transparency (Art. 13, DSK 1.8) | applies | applies | ✅ same |
| **Extra legal layer** | Landesdatenschutzgesetz of the state (currently **DSG NRW**) | **BDSG** (federal law for private companies), **not** the state law | ❌ different |
| Supervisory authority | state authority for public bodies | state authority for companies, by the company's location (in NRW both are the LDI NRW; in e.g. Bayern they differ) | ⚠️ differs |
| Who decides at the end | the Kommune's DSB | the company's DSB or management (Verantwortlicher) | wording only |

**Conclusion:** the core (DSGVO + DSK guidance) is the same for everyone. That's the "Einer prüft für alle" idea, and it now holds across sectors too. What changes:
1. **Which extra law module** is applied: DSG NRW for public bodies, BDSG for companies.
2. **PS-1's public-administration paragraph** only applies to public bodies.
3. **Wording** in the report: "Kommune" → "Ihr Unternehmen", "DSB" → "Datenschutzbeauftragte(r) bzw. Verantwortliche".

So yes, ask **"Unternehmen oder öffentliche Stelle?"**, but as one question that switches the law module and wording, not two separate products.

**BDSG gap: closed.** `reference/bdsg.md` holds the verbatim BDSG sections a company check needs: § 1(1) and § 2(4) (when the BDSG applies to a company), § 22 (sensitive data), § 26 (employee and applicant data), § 37 (automated decisions), § 38 (when a company must have a DSB; any processing that needs a DSFA triggers it), § 40 (which authority). `checklist.md` ("Ergänzende Ebene") says when each is used, and `checks.py` accepts `[BDSG-§n-k]` citations. **Verified:** all 18 Absätze are word for word identical with the official gesetze-im-internet.de text (Stand 12.5.2026); `python audit/verify_bdsg.py` repeats the check.

**Worth knowing for companies, but outside the current standard (possible later modules):** AI tools used on employee data usually need the works council (§ 87 Abs. 1 Nr. 6 BetrVG), and the EU AI Act gives users of AI systems their own obligations (e.g. AI literacy, Art. 4). Don't put these in the check now. Mention them as "nicht Teil dieser Prüfung" so nobody assumes they're covered.

---

## 3. The use-case intake: "Wofür wollen Sie das Tool einsetzen?"

The folder today audits only the vendor's paperwork. For "is this okay **for us**", the check also needs to know the **intended use**, because it decides several outcomes:

| Question (German in the UI) | Why it matters |
|---|---|
| **Wofür wollen Sie das Tool einsetzen?** (free text, 1–3 sentences, with examples: "E-Mails an Kunden entwerfen", "Bewerbungen vorsortieren", "Protokolle zusammenfassen") | the whole check is read against this |
| **Wessen Daten fließen hinein?** Mitarbeitende · Kund:innen · Bewerber:innen · Bürger:innen · Patient:innen · keine personenbezogenen Daten | threshold (PS-0); no personal data → most of the check doesn't apply |
| **Sind besondere Daten dabei?** Gesundheit, Religion, Gewerkschaft, biometrische Daten … (ja / nein / weiß nicht) | Art. 9 data → DSFA much more likely (PS-0) |
| **Trifft oder bereitet das Tool Entscheidungen über Menschen vor?** (z. B. Bewerbungen, Kredite, Leistungen) | decides whether Art. 22 is engaged at all (PS-1) |
| **Organisation:** Unternehmen / öffentliche Stelle (+ Bundesland) | law module and wording (section 2) |
| **Wer prüft?** Wir wollen das Tool nutzen / Wir sind der Anbieter und prüfen unsere eigenen Unterlagen | which action column the report leads with (the folder's two-sided platform view) |

**Rule, now in the folder (`rules.md`, step 0):** the use case is the **user's statement about their own plans**. The auditor uses it to decide *what applies* (threshold, DSFA likelihood, whether Art. 22 is engaged). It never uses it as *evidence that the vendor complies*. Evidence still comes only from the vendor documents. The report shows the use case it assumed at the top, so the reader sees what the result depends on: *"Diese Bewertung gilt für den angegebenen Einsatzzweck: …"*

That makes the report much more useful for a company ("for drafting customer e-mails: 4 checks fine, PS-3 open"), and it's still traceable.

---

## 4. What the user provides

Companies often don't have the signed contract in hand when they ask "is this tool okay?". They have the vendor's website. So **links are a first-class input**, not an afterthought.

**Option A: upload documents** (best when you have them)

| Slot | What it is | Feeds which check |
|---|---|---|
| AVV / DPA | data processing agreement | PS-2 |
| TOMs | security measures | PS-2, PS-3 |
| Produkt-/Systembeschreibung | what it does, which models, data flows | PS-0, PS-1, PS-3 |
| AGB / Nutzungsbedingungen | terms (training, data location) | PS-3, PS-2 |
| Unterauftragnehmerliste | sub-processors | PS-2 |
| DSFA (optional) | existing impact assessment | PS-0 |
| Sonstiges | privacy policy, trust center PDF, FAQ | any |

**Option B: paste links** (a list: DPA page, sub-processor page, terms, trust center). The server fetches each page **once** and stores the text with the audit, so the report can always be re-checked against exactly what was read.

**Option C (phase 2): just enter the vendor's website.** A small helper call (Haiku, with web search) finds the likely DPA, sub-processor list, terms and trust-center pages and **shows them to the user to confirm** before the audit runs. This is the "Is ChatGPT Team okay for us?" experience. It's not in the MVP because the found pages must be confirmed by a human, and public website terms can differ from a negotiated enterprise contract. The report has to say which one it read.

Nothing is strictly required; a missing document becomes a flagged gap (the folder's own rule).

---

## 5. Architecture

```
 Browser (Lovable front end, React)
   │  sign in · use case · upload/links · live status · report · download
   ▼
 Lovable Cloud (managed Supabase)
   ├── Auth          email magic link
   ├── Storage       private bucket "dossiers"  /{user_id}/{audit_id}/{file}
   ├── Database      audits · audit_documents · (later: audit_members, usage)
   └── Edge Function "run-audit"   ← the only place the Claude API key lives
          1. load documents (PDF → sent as PDF; DOCX/TXT/MD → text; links → fetched once, snapshot stored)
          2. call Claude: system = auditor bundle (cached), user = use case + documents, output = JSON report (schema-enforced)
          3. run the gates (same as checks.py, incl. citations in the prose and module consistency); retry once; else mark failed
          4. save report_json + generated report_md + report_html; status = done
   ▼
 Anthropic API (Claude Sonnet 5.5 by default)
```

- **JSON from Claude, Markdown generated by code:** the schema guarantees the classes and fields; code calculates the counts and writes the exact `rules.md` report format, so downloads match the folder's output and still pass `checks.py`.
- **Prompt injection:** an uploaded PDF or a fetched web page can contain instructions. Documents are passed as evidence, not instructions, and the gates catch a manipulated or sloppy answer instead of showing it.

---

## 6. Model choice: Sonnet 5.5 or Haiku 5.5

The model is a **setting** (`AUDIT_MODEL` secret), recorded on every audit, so switching takes one change and every report shows which model wrote it.

| | Sonnet 5.5 (`claude-sonnet-5-5`) | Haiku 5.5 (`claude-haiku-5-5`) |
|---|---|---|
| Price per 1M tokens (in / out) | $2 / $10 | $0.10 / $0.50 (prompts up to 100k tokens; $0.50 / $2.50 above) |
| Rough cost per audit (~60–90k tokens in, ~8k out) | **~$0.15–0.30** | **~$0.01–0.05** |
| Judgment on subtle cases | strong | to be measured |
| Settings | effort `high` | effort `high` (its default is `medium`, so set it) |

**Recommendation:** start with **Sonnet 5.5** for the audit itself, and decide on Haiku with evidence, not by feel:
- run the three fixtures (`audit/fixtures/`, expected results in `audit/keys/`) and `demo/dossier.md` through both;
- watch especially **PS-3 on the demo dossier**: that's the subtle case where the folder's cold run had to apply "silence is never a PASS" against the most persuasive sentence in the document;
- if Haiku matches the keys and that PS-3 call, switch to Haiku. That's roughly 10× cheaper and makes a generous free tier easy.

Either way, **use Haiku for the helper jobs**: cleaning fetched web pages, the phase-2 link finder.

The gates catch form errors (fake citations, missing decisions) whatever the model. They don't catch a wrong judgment, which is why the fixture comparison is the real test.

---

## 7. Multiple users and separate storage

| Need | How | Phase |
|---|---|---|
| Each user sees only their own audits | Auth + **Row Level Security** on every table (`user_id = auth.uid()`) | MVP |
| Files private, per user | Private bucket, path `{user_id}/{audit_id}/…`, storage policy on the first folder; downloads via short-lived signed URLs | MVP |
| Long audits don't time out | Function answers immediately, works in the background, page updates live (Realtime) | MVP |
| Cost control | Free quota per user (e.g. 3/month on Sonnet, more if Haiku holds up), size limits, one running audit per user | MVP |
| Delete my data | Delete button + **auto-delete uploads after 30 days** | MVP |
| Customer + vendor work on one audit | `audit_members` + invite link; both see the same findings, each their own action column | Phase 2 |
| Vendor-website link finder | section 4, option C | Phase 2 |
| Teams / organisations | `organizations` + `memberships` | Phase 3 |
| Payment | Stripe | Phase 3 |
| More law modules | `reference/bdsg.md` (companies) first, then more Länder for public bodies | BDSG soon, Länder on demand |

---

## 8. What else is needed

### a) Changes in the auditor repo (the source of truth; I can build these)
1. ✅ **Use-case rule** in `rules.md` + an `Einsatzkontext` line in the report header (section 3).
2. ✅ **Organisation type** in `rules.md`/`checklist.md`: public body → state module + PS-1 admin-law paragraph; company → BDSG module, admin-law paragraph skipped, company wording.
3. ✅ **`reference/bdsg.md`**: verbatim BDSG excerpts + `SOURCES.md` entry; `checks.py`/`conventions.json` accept `[BDSG-§n-k]` citation IDs (116 valid IDs). ✅ Verified against the official text.
4. **One company fixture** with an answer key (e.g. a SaaS AI writing assistant for a mid-size company) to sit next to the three municipal ones.
5. **`web/export_bundle.py`** → `web/bundle/`: `system-prompt.md`, `valid-ids.json` (116 IDs with the BDSG module), `report.schema.json`, `VERSION`.
6. **Parity test:** bundle JSON → generated Markdown → `python audit/checks.py` passes.

### b) Accounts and keys
- Anthropic API key → Lovable Cloud Secrets as `ANTHROPIC_API_KEY`; model in `AUDIT_MODEL`. Set a monthly spend limit in the Anthropic console.
- Lovable paid plan (check current Cloud pricing).

### c) Data protection of the service itself
- **Impressum** + **Datenschutzerklärung**.
- Name the sub-processors: Lovable/Supabase (check whether your project runs in an EU region; if not, connect your own Supabase project in Frankfurt), Anthropic. The direct Anthropic API currently has no EU-only processing option (US/global). If customers ask for EU processing, the same Claude models run via AWS Bedrock (Frankfurt) or Google Vertex AI (EU).
- UI text: upload vendor paperwork, not personal data; uploads auto-delete after 30 days; not used for training.
- **RDG:** keep the framing (structured pre-check, the human decides, no legal verdict) in the UI and terms; get a short lawyer's look before charging.
- **Building Out Loud:** run the auditor on your own site's vendors (Lovable/Supabase, Anthropic). It'll probably flag the US transfer. Honest and shareable.

### d) Tie it to the consulting offer
The report's natural next step for a company is "and now how do we use this tool well and safely?". That's exactly your ICM offer. Put one quiet line at the end of every company report and on the landing page: *"Sie wollen das Tool sicher und sinnvoll einführen? Sprechen Sie mit uns."* The free tool becomes the warm door to a paid engagement.

---

## 9. Build order (each step is demoable = one Building Out Loud post)

| Step | What | Who | Done when |
|---|---|---|---|
| 0 | Repo changes 8a.1–8a.6 (1–3 done) | Claude | bundle exists; company fixture + parity test pass `checks.py` |
| 1 | Landing page + use-case intake + upload flow, mock data (prompt 1) | you in Lovable | clickable prototype to screen-record |
| 2 | Auth, database, storage, RLS (prompt 2) | Lovable | two accounts can't see each other's audits |
| 3 | `run-audit` with Claude (prompt 3) | Lovable + bundle | `01-clean-pass` → 5× CLEAR PASS |
| 4 | Report page + downloads incl. PDF (prompt 4) | Lovable | report matches `rules.md` format; US-6 acceptance criteria met |
| 5 | History, delete, auto-delete, quota, legal pages (prompt 5) | Lovable | ready for outside testers |
| 6 | Sonnet vs Haiku on all fixtures + demo dossier | Claude/you | model decision made on evidence |
| 7 | Phase 2: link finder, shared customer↔vendor audits | later | |

---

## 10. Decisions still open

1. **Free tier size** once the model is decided (Haiku makes generous free use cheap).
2. **Where Claude runs** if customers ask for EU-only processing (direct API vs. Bedrock/Vertex).
3. **Domain/name:** e.g. a subdomain of stepintomore.co. The name could also move from "Kommune" language to something like "KI-Anbieter-Check".

---

## 11. Honest limits (put these on the site too)

- It checks what the **paperwork says**, not what the system **does**.
- Public website terms can differ from a signed enterprise contract; the report names what it read.
- Five core checks. Public bodies: NRW only so far.
- Works council and EU AI Act duties are not part of this check.
- It's a pre-check that gives the decision-maker a map; the decision stays with them.
