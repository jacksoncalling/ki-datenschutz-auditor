# checklist.md — The Prüfschritte

The ordered checks. Each names the provision(s) it tests, the evidence it needs from the dossier, and how the three finding classes apply to it. Run them in order (see `rules.md`). Produce exactly one finding per check.

The five checks are deliberately the ones that (a) are mandatory for lawfulness, (b) are the recurring reasons an AI deployment stalls, and (c) map to a locatable provision. They rest on the DSGVO and the DSK guidance, which apply to public bodies and companies alike. This is the shared core that "Einer prüft für alle" makes portable, across Länder and across sectors.

**Which extra law module applies** is set by the organisation type in the Einsatzkontext (`rules.md`, step 0): a **public body** (Kommune, Behörde) gets the state module (`reference/dsg-nrw.md`); a **company** (nichtöffentliche Stelle, `[BDSG-§2-4]`) gets the federal module `reference/bdsg.md`. Lines marked *(öffentliche Stelle)* or *(Unternehmen)* below apply only to that type. "The organisation" below means whoever wants to use the tool (the Kommune or the company); "affected people" means citizens, customers, employees or applicants, whoever the Einsatzkontext names. Write the report in those terms too: never call a company a Kommune or its customers Bürger.

---

## [PS-0] Schwelle und DSFA-Pflicht

**Tests:** `[DSGVO-Art35-1]`, `[DSK-OH-2.3]`
**Evidence needed:** any statement of purpose and data categories; whether a DSFA exists or is planned. Read it against the Einsatzkontext: the stated use, the affected people, whether special categories (Art. 9) are involved.

- **CLEAR FAIL:** high-risk personal-data processing is described and the dossier states no DSFA is needed. Contradicts the mandatory Vorabbewertung.
- **NARROW FLAG:** personal data is processed, DSFA is likely required, but the dossier is silent on whether one was done. (Very common.)
- **CLEAR PASS:** a DSFA per Art. 35 is documented or explicitly committed, and the vendor supplies the system information the organisation needs to run it (`[DSK-OH-2.3]`).

*(Unternehmen)* Where a DSFA is required, the company must also have a Datenschutzbeauftragte(n), whatever its size (`[BDSG-§38-1]`: "unabhängig von der Anzahl der mit der Verarbeitung beschäftigten Personen"). Name this in the Offene Entscheidung. Where special categories are processed, `[BDSG-§22-2]` lists the protective measures expected; where they are employee data, `[BDSG-§26-3]`.

If the tool clearly processes no personal data, record that and stop the whole audit here.

---

## [PS-1] Menschliche Letztentscheidung (Human-in-the-Loop)

**Tests:** `[DSGVO-Art22-1]`, `[DSGVO-Art22-3]`, `[DSK-OH-1.6]`; *(öffentliche Stelle in NRW)* `[DSG-NRW-§46-1]`; *(Unternehmen)* `[BDSG-§37-1]`, `[BDSG-§26-1]` where employees or applicants are affected
**Evidence needed:** description of what the system decides or recommends; whether a human caseworker makes the final call; whether that human has a real Entscheidungsspielraum or only signs off.

- **CLEAR FAIL:** the system issues decisions with legal or similarly significant effect on individuals with no human in the loop (e.g. auto-sends rejections). Cite the DSK example verbatim from `[DSK-OH-1.6]`. *(öffentliche Stelle)* For a fully automated Verwaltungsakt: FAIL unless the dossier shows a *gebundene Entscheidung* with an express legal basis (§ 35a VwVfG), because with Ermessen the fully automated route is barred (`[DSK-OH-1.6]`).
- **NARROW FLAG:** a human is nominally involved but the dossier suggests only *formelle Beteiligung* (rubber-stamp), or the Entscheidungsspielraum is not described. The DSK is explicit that a merely formal human role is not enough (`[DSK-OH-1.6]`).
- **CLEAR PASS:** documented genuine human review with real discretion. Where the system does make or materially drive an Art. 22 decision, the Art. 22(3) safeguards must also be present (`[DSGVO-Art22-3]`: right to obtain human intervention, to state one's view, to contest). Where the system makes no Art. 22 decision at all (it only drafts and a human decides), Art. 22(3) is not engaged and its absence is not a gap.

Use the Einsatzkontext: if the user states the tool makes or prepares no decisions about people (e.g. it drafts e-mails), Art. 22 is likely not engaged, but say that this rests on the stated use. *(Unternehmen)* The BDSG adds no general exception to Art. 22; `[BDSG-§37-1]` covers only decisions under an insurance contract. Applicant screening and other decisions about employees are the common company case: cite `[DSGVO-Art22-1]` together with `[BDSG-§26-1]` (Bewerber:innen count as Beschäftigte, `[BDSG-§26-8]`).

---

## [PS-2] Auftragsverarbeitung, Unterauftragnehmer und Datenstandort

**Tests:** `[DSGVO-Art28-3]`, `[DSGVO-Art28-2]`, `[DSGVO-Art44]`, `[DSK-OH-2.1]`
**Evidence needed:** the AVV and whether it meets Art. 28(3); a full, current list of sub-processors; where data is processed (EU vs third country) and, if third country, the Kapitel-V safeguard.

- **CLEAR FAIL:** no AVV for a cloud tool that processes personal data on the organisation's behalf; or undisclosed sub-processors; or personal data transferred to a third country with no safeguard named. Any of these contradicts a mandatory element.
- **NARROW FLAG:** an AVV exists but omits one or more Art. 28(3) elements; or the sub-processor list is present but not guaranteed complete/current; or data residency is stated as EU but third-country access (e.g. support, parent company) is not addressed.
- **CLEAR PASS:** Art. 28(3)-compliant AVV, complete sub-processor list with change-notification rights (`[DSGVO-Art28-2]`), and EU residency or a valid Kapitel-V mechanism.

---

## [PS-3] Trainingsverbot und datenschutzfreundliche Voreinstellungen

**Tests:** `[DSK-OH-1.9]`, `[DSK-OH-2.5]`, `[DSGVO-Art5-1]` (Zweckbindung, lit. b)
**Evidence needed:** an explicit contractual clause on whether the vendor may use the organisation's inputs/outputs (prompts, documents, results) to train or fine-tune its models; and whether training and history are switched off by default (data protection by default).

- **CLEAR FAIL:** the terms permit the vendor to use the organisation's data for model training or fine-tuning; or it is an open system where inputs demonstrably feed provider training (`[DSK-OH-1.7]`). **Conditional escalation:** a *missing* exclusion becomes a CLEAR FAIL, not a flag, once personal data is actually processed through an upstream model with no contractual training bar and no separate legal basis. The dossier need not say "we will train"; per `[DSK-OH-1.9]` an exclusion is then required, and sending affected people's data to a model whose training bar is explicitly absent is itself the violation, closed systems being *vorzugswürdig* (`[DSK-OH-1.7]`).
- **NARROW FLAG:** the dossier is **silent or ambiguous** on training rights (the single most common gap); *or* no exclusion exists yet but no personal data has flowed to the upstream model (the gap is closable before processing begins); *or* an opt-out exists but is not the default setting (`[DSK-OH-2.5]`). The DSK is clear that applications which do not use inputs/outputs for training are *vorzugswürdig* and that an exclusion should be secured (`[DSK-OH-1.9]`).
- **CLEAR PASS:** an explicit contractual exclusion of training/fine-tuning on the organisation's data, with default-off settings for training and input history.

---

## [PS-4] Transparenz und Erklärbarkeit

**Tests:** `[DSGVO-Art13-2f]` (the "involvierte Logik" duty proper), `[DSGVO-Art13-1]` (the general information duty), `[DSK-OH-1.8]`
**Evidence needed:** whether the vendor provides documentation of the system's *Logik* (Funktionsweise) sufficient for the organisation to meet its Art. 12 ff. information duties to affected people, including a plain-language management summary. The specific "aussagekräftige Informationen über die involvierte Logik" obligation lives in Art. 13(2)(f); cite it as the primary anchor for the logic point, `[DSGVO-Art13-1]` for the base information duty.

- **CLEAR FAIL:** a decision-relevant system with no explainability documentation at all, so the organisation cannot answer information requests from affected people. Contradicts the Art. 13 duty the organisation cannot discharge without vendor input (`[DSK-OH-1.8]`).
- **NARROW FLAG:** some technical documentation exists but no plain-language explanation for affected people of the logic, scope, and possible effects (`[DSK-OH-1.8]`).
- **CLEAR PASS:** documented logic plus a plain-language explanation the organisation can pass to affected people.

---

## Ergänzende Ebene (state layer or BDSG)

After [PS-0] through [PS-4], apply the extra module that fits the organisation type. Record it as a short confirmation, not a sixth check, unless it changes an outcome.

**Never mix the modules.** A company report cites no `[DSG-NRW-…]`, a public-body report cites no `[BDSG-…]`. `audit/checks.py` enforces this from the "Geprüft gegen" line.

**Öffentliche Stelle in NRW:** apply `reference/dsg-nrw.md`: confirm the competent authority (LDI NRW) and note any Land-specific provision that changes a finding. For NRW, `[DSG-NRW-§46-1]` reinforces [PS-1] (prohibition of adverse purely automated decisions unless a law expressly permits) and `[DSG-NRW-§46-3]` bars discriminatory profiling. To audit for another Bundesland, replace only the state module and the authority name. Nothing in [PS-0]..[PS-4] changes.

**Öffentliche Stelle in another Land:** only the NRW module exists so far. Do **not** apply DSG NRW. Run the core checks, write "Geprüft gegen: DSGVO + DSK-Orientierungshilfe KI (06.05.2024)", name the authority as "Landesdatenschutzbehörde für öffentliche Stellen in <Land>", and state under "Ergänzendes Recht" that the <Land> module is not yet included.

**Organisation type unknown** (still unknown after asking once): apply no extra module. Write "Geprüft gegen: DSGVO + DSK-Orientierungshilfe KI (06.05.2024)" and state that the result is missing the extra layer: BDSG for a company, the Landesdatenschutzgesetz for a public body. This keeps runs reproducible: the same unknown input always yields the core-only report.

**Unternehmen:** apply `reference/bdsg.md`:
- Authority: the state authority at the company's seat (`[BDSG-§40-1]`; several sites → main establishment, `[BDSG-§40-2]`). Name it if the Einsatzkontext gives the Bundesland; otherwise say "Landesdatenschutzbehörde am Sitz des Unternehmens". In some Länder this is a different authority from the one for public bodies (e.g. Bayern: BayLDA for companies, BayLfD for public bodies); in NRW both are the LDI NRW.
- **Employee data** (Mitarbeitende or Bewerber:innen in the Einsatzkontext): note that employee data is processed for employment purposes (`[BDSG-§26-1]`). Caveat to state in the report: the EuGH (30.03.2023, C-34/21) held that a national rule worded like § 26 Abs. 1 Satz 1 may only be applied if it meets Art. 88 Abs. 2 DSGVO, so this sentence is widely regarded as no longer usable as a legal basis; employee data then rests on Art. 6 Abs. 1 DSGVO directly (Art. 6 is not in `reference/`: name it in prose, never as a `[DSGVO-Art6-…]` citation). Cite § 26 to classify the situation, never as the sole legal basis. Further, note that consent in the employment relationship is only valid under the conditions of `[BDSG-§26-2]`, and that the works council's participation rights stay untouched (`[BDSG-§26-6]`). The open decision then names: legal basis, a Betriebsvereinbarung where one is used (`[BDSG-§26-4]`), and involving the works council.
- **DSB duty:** if PS-0 found a DSFA likely, restate `[BDSG-§38-1]`.

The extra module never upgrades a core finding on its own; it adds what the organisation must also decide.
