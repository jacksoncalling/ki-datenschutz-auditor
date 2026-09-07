# SOURCES.md — Provenance of the standard

Everything in `reference/` is a verbatim excerpt of a real, external, published standard. This file records exactly where each excerpt came from, so a reviewer can open the finding, open the cited provision here, and open the official source, and confirm all three match. Retrieval date for all sources: **2026-09-07**.

## dsgvo-artikel.md — Datenschutz-Grundverordnung (DSGVO)

- **Instrument:** Verordnung (EU) 2016/679 des Europäischen Parlaments und des Rates vom 27. April 2016 (Datenschutz-Grundverordnung). Official EU law.
- **Articles included:** 5, 13, 22, 28, 35, 44 (the provisions the checklist cites; the full regulation has 99 articles).
- **Verbatim source used:** per-article full text on https://dsgvo-gesetz.de (Art. 5: /art-5-dsgvo/, and so on).
- **Authoritative cross-reference:** EUR-Lex, CELEX 32016R0679, German language version: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679
- **Editorial notes:** sentence markers `[1] [2]` were added to number the Sätze of an Absatz for precise citation; they are not part of the legal text. Article headings were reformatted (title on its own line). No wording was changed. In Art. 28(3) the closing sub-paragraph ("Mit Blick auf Unterabsatz 1 Buchstabe h ...") is placed after item h), matching the official structure.

## dsk-oh-ki.md — DSK-Orientierungshilfe KI und Datenschutz

- **Instrument:** Konferenz der unabhängigen Datenschutzaufsichtsbehörden des Bundes und der Länder (DSK), *Orientierungshilfe "Künstliche Intelligenz und Datenschutz"*, Version 1.0, 06.05.2024.
- **Official PDF:** https://www.datenschutzkonferenz-online.de/media/oh/20240506_DSK_Orientierungshilfe_KI_und_Datenschutz.pdf
- **Sections included:** 1.4, 1.6, 1.7, 1.8, 1.9, 1.10, 2.1, 2.3, 2.5 (the sections the checklist cites; the full guidance has three parts).
- **Editorial notes:** text was extracted from the official PDF by page coordinates. The DSK's own Randnummern (printed in the outer page margin) and running page numbers/footnote URLs were removed so they do not interrupt the sentences; citation is therefore by **section number**, which is unchanged. Line-break hyphenation was rejoined. No wording was changed. One line-order artifact in section 2.3 ("Muss-Listen") and the section 2.5 heading wrap were corrected back to the source order.
- **Status of this document:** the Orientierungshilfe is guidance (Auslegung), not a statute. It is the joint position of all German supervisory authorities and is what the LDI NRW points controllers to, which is why it is the interpretive spine of this auditor. Findings that rely on it say so.

## dsg-nrw.md — Datenschutzgesetz Nordrhein-Westfalen (the state module)

- **Instrument:** Datenschutzgesetz Nordrhein-Westfalen (DSG NRW) vom 25.05.2018.
- **Sections included:** § 5 (Anwendungsbereich, Absätze 1 to 4) and § 46 (Automatisierte Einzelentscheidungen).
- **Verbatim source used:** per-section full text on https://dsgvo-gesetz.de/dsg-nrw/
- **Authoritative cross-reference:** https://recht.nrw.de/lrgv/gesetz/25052018-datenschutzgesetz-nordrhein-westfalen-dsg-nrw/
- **Competent authority:** Landesbeauftragte für Datenschutz und Informationsfreiheit Nordrhein-Westfalen (LDI NRW), https://www.ldi.nrw.de , which adopts the DSK-Orientierungshilfe KI as the yardstick for Unternehmen und Behörden.
- **Applicability note on § 46:** § 46 DSG NRW implements the JI-Directive (police/justice). It is included as the NRW legislator's expression of the ban on adverse purely automated decisions; for ordinary municipal administration Art. 22 DSGVO applies directly, plus § 35a VwVfG for a fully automated Verwaltungsakt. This nuance is stated in the file itself and in `[DSK-OH-1.6]`.

## Fixtures

The vendor dossiers in `audit/fixtures/` are **synthetic**. They were written for this auditor and model the structure of real German municipal AI-procurement material, in particular the CC0-licensed templates published by **KI:connect.nrw** (RWTH Aachen): the Muster-DSFA (https://kiconnect.pages.rwth-aachen.de/pages/provision-dsfa/) and the RWTH Muster-AVV nach Art. 28 DSGVO. No real vendor, contract, or municipality is depicted. See `audit/keys/` for what each fixture was built to contain.
