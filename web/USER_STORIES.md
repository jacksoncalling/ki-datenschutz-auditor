# User stories: KI-Anbieter-Check (web service)

The web version of the KI-Datenschutz-Prüfassistent, as seen by the people using it. Each story has acceptance criteria that can be checked by clicking through the site. The architecture behind them is in `PLAN.md`; the prompts that build them in Lovable are in `LOVABLE_PROMPTS.md`.

**Who uses it**

- **Nutzer (company):** someone at a company (owner, IT lead, DSB, team lead) who wants to know whether an AI tool is okay for a specific use. The main audience.
- **Nutzer (public body):** the same question from a Kommune or Behörde.
- **Anbieter:** an AI vendor checking its own paperwork before it pitches a customer.

---

## US-1: Sign in

**As a** visitor, **I want to** sign in with just my e-mail address, **so that** my audits are private and I can come back to them.

- A magic link is sent to the e-mail address; no password.
- After signing in I land on "Meine Prüfungen".
- Another account can never see my audits or files (checked with two test accounts).

## US-2: Describe my use case

**As a** Nutzer, **I want to** say what I want to use the tool for, **so that** the check answers *my* question and not a generic one.

- I can describe the use in 1–3 sentences or pick an example ("Kunden-E-Mails entwerfen", "Bewerbungen vorsortieren", …).
- I can say whose data goes in (Mitarbeitende, Bewerber:innen, Kund:innen, Bürger:innen, Patient:innen, keine), whether sensitive data (Art. 9) is involved, and whether the tool makes or prepares decisions about people. "Weiß nicht" is allowed.
- I choose Unternehmen or Öffentliche Stelle, and my Bundesland.
- The report later shows my use case at the top ("Diese Bewertung gilt für Ihren Einsatzzweck: …").

## US-3: Provide the vendor's documents

**As a** Nutzer, **I want to** upload the vendor's documents or paste links to them, **so that** I can run a check even when I only have the vendor's website.

- Upload slots for AVV/DPA, TOMs, product/system description, terms, sub-processor list, DSFA (optional), other; PDF, DOCX, TXT, MD; max 20 MB in total.
- A list of links with a type per link; max 10.
- Missing documents don't block the check; the screen says they become open gaps in the report.
- The screen asks me not to upload personal data.

## US-4: Run the check and see progress

**As a** Nutzer, **I want to** start the check and see that it is working, **so that** I know to wait 1–3 minutes.

- I must tick "Vorprüfung, keine Rechtsberatung" before starting.
- The page shows live steps (reading documents → checks running → report being verified) without reloading.
- If something fails I see a plain German message and a "Erneut versuchen" button.
- A report that fails the built-in quality gates (all five checks, real citations anywhere in the text, only the law module that fits my organisation, open decision on every gap) is never shown. The gates are the same as the repo's `checks.py`.
- If the check takes too long, the audit is marked failed after 10 minutes instead of spinning forever.
- If the tool processes no personal data or is not an AI application, I get "Prüfung nicht anwendbar" with the reason, and no report or downloads.

## US-5: Read the report

**As a** Nutzer, **I want to** read the result as a clear page, **so that** I know in a minute whether the tool is okay and what's still open.

- Top: product, vendor, date, use case, which law was applied (DSGVO + DSK + BDSG for companies, + DSG NRW for public bodies in NRW), competent authority.
- Three counters (CLEAR PASS / NARROW FLAG / CLEAR FAIL), a one-sentence summary, and the most important open decision.
- One card per check with the quote from the documents (and which document), the legal citation with its wording, the assessment, the open decision, and "Ihr nächster Schritt".
- A two-sided view (Nutzer next step / Anbieter next proof).

## US-6: Download the report as a PDF ⭐

**As a** Nutzer, **I want to** download the finished report as a PDF, **so that** I can forward it to my DSB, my manager or the vendor, file it with the procurement records, or print it.

**Acceptance criteria**

1. **When:** a "PDF herunterladen" button appears on the report page as soon as the audit status is `done`. It is not shown while the audit is running or after it failed.
2. **One click:** the PDF downloads directly (no print dialog), on desktop and on mobile (iOS Safari and Android Chrome).
3. **File name:** `<Produkt>-Datenschutz-Vorpruefung-<YYYY-MM-DD>.pdf` (umlauts and spaces made file-name safe).
4. **Content:** the PDF contains everything the report page shows, in this order:
   - title "Datenschutz-Vorprüfung: <Produkt> / <Anbieter>", date, use case (Einsatzkontext), "Geprüft gegen", competent authority, provided and missing documents;
   - the three counters, summary and most important open decision;
   - every finding PS-0 to PS-4 with class, document quote and source document, citations with their verbatim wording, assessment, open decision (for FLAG/FAIL) and next step;
   - the note on the extra module (BDSG or state law), including anything not yet covered;
   - the two-sided table;
   - the disclaimer "Diese Vorprüfung ersetzt nicht die Entscheidung … Sie strukturiert und beschleunigt sie." and "Nicht Teil dieser Prüfung: Betriebsrat, KI-Verordnung";
   - a footer on every page: "KI-Anbieter-Check · Prüfassistent-Version <version> · Modell <model> · Seite x von y".
5. **Looks right:** A4 portrait; the three classes are recognisable without colour (label text, not only green/amber/red), so it prints well in black and white; German characters (ä ö ü ß „ ") render correctly; findings don't get cut awkwardly across pages (a finding's heading never sits alone at the bottom of a page).
6. **Real text:** the text in the PDF can be selected, searched and copied (not a screenshot of the page), so a DSB can quote from it.
7. **Same content as the report:** the PDF is generated from the same saved report data as the page and the Markdown download, so the three can never disagree.
8. **Privacy:** generating the PDF sends no data to any additional service. Either it is built in the browser, or it is built by our own backend function and delivered via a short-lived signed link.
9. **Speed:** the download starts within 3 seconds for a normal report.
10. **After deletion:** once the user deletes the audit, the PDF can no longer be downloaded (no stored copy left behind).

**Implementation note (for Lovable):** generate the PDF in the browser from `report_json` with `@react-pdf/renderer`: real vector text, page footers and page-break control, no server and no stored file. Register a font that covers German characters (e.g. Inter or Source Sans 3). A stored server-side PDF is only needed later if users want to share a link instead of a file.

## US-7: Other downloads

**As a** Nutzer, **I want** the report as Markdown and HTML too, **so that** I can paste it into our wiki or e-mail it.

- "Als Markdown herunterladen" gives the exact `rules.md` report format; running `python audit/checks.py` on it passes.
- "Als HTML herunterladen" gives a self-contained one-pager.

## US-8: My audits

**As a** Nutzer, **I want** a list of my past audits, **so that** I can find a report again or check a vendor a second time.

- List with product, vendor, use case, date, counters, status.
- Opening an old audit shows the report and all downloads (PDF included).

## US-9: Delete my data

**As a** Nutzer, **I want to** delete an audit and its documents, **so that** nothing of mine stays on the service longer than needed.

- "Löschen" removes the audit, its documents and its files immediately.
- Uploaded documents are deleted automatically after 30 days; the report stays, with the note "Unterlagen nach 30 Tagen automatisch gelöscht".

## US-10: Fair use

**As the** operator, **I want** a monthly limit per user, **so that** costs stay predictable while the service is free.

- Default 3 audits per month per user (a setting, easy to raise); one running audit at a time.
- A friendly German message when the limit is reached, with a contact link.

## US-11: Vendor checks its own paperwork

**As an** Anbieter, **I want to** run the check on my own documents, **so that** I can close the gaps before a customer's DSB finds them.

- Role "Wir sind der Anbieter" in the wizard.
- The report leads with "Anbieter: nächster Nachweis" for each finding.

## US-12: Next step with Step Into More

**As a** company Nutzer, **I want** an easy way to get help introducing the tool, **so that** I don't stop at "okay in principle".

- A quiet box under company reports: "Sie wollen das Tool sicher und sinnvoll einführen? Step Into More begleitet Sie dabei." with a contact button.
- Not shown on public-body reports, never inside the PDF findings.

---

## Later (not in the MVP)

- **US-13 Vendor website finder:** enter only the vendor's website; the service finds the DPA, sub-processor list, terms and trust-center pages and asks me to confirm them before the check.
- **US-14 Shared audit:** invite the vendor (or the customer) to the same audit; both see the same findings and their own action column.
- **US-15 Teams:** several people of one organisation share audits.
