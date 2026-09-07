# checklist.md — The Prüfschritte

The ordered checks. Each names the provision(s) it tests, the evidence it needs from the dossier, and how the three finding classes apply to it. Run them in order (see `rules.md`). Produce exactly one finding per check.

The five checks are deliberately the ones that (a) are mandatory for lawfulness, (b) are the recurring reasons a municipal AI deployment stalls, and (c) map to a locatable provision. This is the shared core that "Einer prüft für alle" makes portable.

---

## [PS-0] Schwelle und DSFA-Pflicht

**Tests:** `[DSGVO-Art35-1]`, `[DSK-OH-2.3]`
**Evidence needed:** any statement of purpose and data categories; whether a DSFA exists or is planned.

- **CLEAR FAIL:** high-risk personal-data processing is described and the dossier states no DSFA is needed. Contradicts the mandatory Vorabbewertung.
- **NARROW FLAG:** personal data is processed, DSFA is likely required, but the dossier is silent on whether one was done. (Very common.)
- **CLEAR PASS:** a DSFA per Art. 35 is documented or explicitly committed, and the vendor supplies the system information the municipality needs to run it (`[DSK-OH-2.3]`).

If the tool clearly processes no personal data, record that and stop the whole audit here.

---

## [PS-1] Menschliche Letztentscheidung (Human-in-the-Loop)

**Tests:** `[DSGVO-Art22-1]`, `[DSGVO-Art22-3]`, `[DSK-OH-1.6]`, `[DSG-NRW-§46-1]`
**Evidence needed:** description of what the system decides or recommends; whether a human caseworker makes the final call; whether that human has a real Entscheidungsspielraum or only signs off.

- **CLEAR FAIL:** the system issues decisions with legal or similarly significant effect on individuals with no human in the loop (e.g. auto-sends rejections). Cite the DSK example verbatim from `[DSK-OH-1.6]`. For a fully automated Verwaltungsakt: FAIL unless the dossier shows a *gebundene Entscheidung* with an express legal basis (§ 35a VwVfG), because with Ermessen the fully automated route is barred (`[DSK-OH-1.6]`).
- **NARROW FLAG:** a human is nominally involved but the dossier suggests only *formelle Beteiligung* (rubber-stamp), or the Entscheidungsspielraum is not described. The DSK is explicit that a merely formal human role is not enough (`[DSK-OH-1.6]`).
- **CLEAR PASS:** documented genuine human review with real discretion, and safeguards per `[DSGVO-Art22-3]` (right to obtain human intervention, to state one's view, to contest).

---

## [PS-2] Auftragsverarbeitung, Unterauftragnehmer und Datenstandort

**Tests:** `[DSGVO-Art28-3]`, `[DSGVO-Art28-2]`, `[DSGVO-Art44]`, `[DSK-OH-2.1]`
**Evidence needed:** the AVV and whether it meets Art. 28(3); a full, current list of sub-processors; where data is processed (EU vs third country) and, if third country, the Kapitel-V safeguard.

- **CLEAR FAIL:** no AVV for a cloud tool that processes personal data on the municipality's behalf; or undisclosed sub-processors; or personal data transferred to a third country with no safeguard named. Any of these contradicts a mandatory element.
- **NARROW FLAG:** an AVV exists but omits one or more Art. 28(3) elements; or the sub-processor list is present but not guaranteed complete/current; or data residency is stated as EU but third-country access (e.g. support, parent company) is not addressed.
- **CLEAR PASS:** Art. 28(3)-compliant AVV, complete sub-processor list with change-notification rights (`[DSGVO-Art28-2]`), and EU residency or a valid Kapitel-V mechanism.

---

## [PS-3] Trainingsverbot und datenschutzfreundliche Voreinstellungen

**Tests:** `[DSK-OH-1.9]`, `[DSK-OH-2.5]`, `[DSGVO-Art5-1]` (Zweckbindung, lit. b)
**Evidence needed:** an explicit contractual clause on whether the vendor may use the municipality's inputs/outputs (prompts, documents, results) to train or fine-tune its models; and whether training and history are switched off by default (data protection by default).

- **CLEAR FAIL:** the terms permit the vendor to use municipal data for model training or fine-tuning; or it is an open system where inputs demonstrably feed provider training (`[DSK-OH-1.7]`).
- **NARROW FLAG:** the dossier is **silent or ambiguous** on training rights (the single most common gap), or an opt-out exists but is not the default setting (`[DSK-OH-2.5]`). The DSK is clear that applications which do not use inputs/outputs for training are *vorzugswürdig* and that an exclusion should be secured (`[DSK-OH-1.9]`).
- **CLEAR PASS:** an explicit contractual exclusion of training/fine-tuning on municipal data, with default-off settings for training and input history.

---

## [PS-4] Transparenz und Erklärbarkeit

**Tests:** `[DSGVO-Art13-1]`, `[DSK-OH-1.8]`
**Evidence needed:** whether the vendor provides documentation of the system's *Logik* (Funktionsweise) sufficient for the municipality to meet its Art. 12 ff. information duties to citizens, including a plain-language management summary.

- **CLEAR FAIL:** a decision-relevant system with no explainability documentation at all, so the municipality cannot answer citizen information requests. Contradicts the Art. 13 duty the municipality cannot discharge without vendor input (`[DSK-OH-1.8]`).
- **NARROW FLAG:** some technical documentation exists but no citizen-facing plain-language explanation of the logic, scope, and possible effects (`[DSK-OH-1.8]`).
- **CLEAR PASS:** documented logic plus a plain-language explanation the municipality can pass to affected citizens.

---

## State layer

After [PS-0] through [PS-4], apply `reference/dsg-nrw.md`: confirm the competent authority (LDI NRW) and note any Land-specific provision that changes a finding. For NRW, `[DSG-NRW-§46-1]` reinforces [PS-1] (prohibition of adverse purely automated decisions unless a law expressly permits) and `[DSG-NRW-§46-3]` bars discriminatory profiling. Record this as a short confirmation, not a sixth check, unless the state law changes an outcome.

To audit for another Bundesland, replace only the state module and this section's authority name. Nothing in [PS-0]..[PS-4] changes. That is the portability the whole tool is built to demonstrate.
