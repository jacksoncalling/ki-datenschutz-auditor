# examples.md — Worked findings

Three worked findings, one per class, to calibrate how a finding should read: a dossier quote, a resolvable citation with a short verbatim excerpt of the standard, a classification, and (for gaps) the open decision left to the human. Full end-to-end reports on real fixtures live in `audit/reports/`; these are the pattern in miniature.

The rule underneath all three: **the class comes from the relationship between the dossier and the provision, never from the auditor's taste.** Contradiction is a FAIL, explicit satisfaction is a PASS, silence or ambiguity is a NARROW FLAG.

---

## Example 1 — CLEAR FAIL

Input (dossier): *"AutoDecide entscheidet und antwortet vollautomatisch rund um die Uhr. Ein menschlicher Prüf- oder Freigabeschritt ist nicht vorgesehen."*

```
### [PS-1] Menschliche Letztentscheidung — CLEAR FAIL
- Fundstelle im Dossier: "AutoDecide entscheidet und antwortet vollautomatisch ... kein Prüf- oder Freigabeschritt".
- Standard: [DSGVO-Art22-1] Recht, "nicht einer ausschließlich auf einer automatisierten Verarbeitung ... beruhenden Entscheidung unterworfen zu werden"; [DSK-OH-1.6] Beispiel: der selbstständige Versand von Entscheidungen "stellt einen Verstoß gegen Art. 22 Abs. 1 DS-GVO dar".
- Bewertung: Vollautomatische belastende Einzelentscheidungen ohne Mensch widersprechen Art. 22 Abs. 1 unmittelbar.
- Offene Entscheidung (DSB): verbindlichen Human-in-the-Loop mit echtem Entscheidungsspielraum verlangen oder den Einsatz ablehnen.
```

Why FAIL and not FLAG: the dossier does not merely omit a human, it explicitly excludes one. That is a quotable contradiction of the provision, which is the bar for CLEAR FAIL.

---

## Example 2 — NARROW FLAG

Input (dossier): *"Daten werden sicher und vertraulich verarbeitet."* (no statement on model training)

```
### [PS-3] Trainingsverbot und datenschutzfreundliche Voreinstellungen — NARROW FLAG
- Fundstelle im Dossier: "Daten werden sicher und vertraulich verarbeitet" (keine Aussage zur Trainingsnutzung).
- Standard: [DSK-OH-1.9] "vorzugswürdig sind daher Anwendungen, die die Ein- und Ausgabedaten nicht zu Trainingszwecken verwenden".
- Bewertung: Eine allgemeine Sicherheitszusage ist kein Trainingsausschluss. Das Dossier ist an diesem Punkt schlicht stumm, kein Verstoß, aber eine zu schließende Lücke.
- Offene Entscheidung (DSB): ausdrücklichen vertraglichen Ausschluss der Trainings-/Fine-Tuning-Nutzung plus Default-off verlangen.
```

Why FLAG and not FAIL or PASS: "sicher" neither satisfies nor contradicts the training-exclusion provision. Silence is the signature of the NARROW FLAG, and this is the single most common gap in real vendor paperwork. Marking it PASS would be wishful; marking it FAIL would be the rigid over-judgment the DSK warns against.

---

## Example 3 — CLEAR PASS

Input (dossier): *"Der Anbieter verwendet Eingaben, Prompts, Dokumente und Ausgaben der Kommune nicht zum Training oder Fine-Tuning ... standardmäßig deaktiviert."*

```
### [PS-3] Trainingsverbot und datenschutzfreundliche Voreinstellungen — CLEAR PASS
- Fundstelle im Dossier: "verwendet ... nicht zum Training oder Fine-Tuning ... standardmäßig deaktiviert".
- Standard: [DSK-OH-1.9] Ausschluss der Trainingsnutzung; [DSK-OH-2.5] Voreinstellungen so, "dass keine Eingabedaten zu Trainingszwecken verarbeitet werden".
- Bewertung: Ausdrücklicher vertraglicher Ausschluss plus Default-off erfüllen die Vorgabe vollständig; die Fundstelle trägt die Klasse.
```

Why PASS: the dossier states the exact thing the provision asks for, in locatable words. A PASS needs that explicit, quotable satisfaction, and it needs no open-decision line, because nothing is left open.

---

Same discipline as the whole tool: open the finding, open the cited provision in `reference/`, and the two match. If they do not, it is not a finding.
