# Layer-2 check: do the findings match the source documents?

Run per `audit/compliance-judge.md` against the four documents in `input/`. For each finding: does the cited provision, read against the actual dossier text, support the assigned class?

| PS | Klasse | Beleg im Dossier | Urteil |
|---|---|---|---|
| PS-0 | NARROW FLAG | Keine DSFA in den Unterlagen erwähnt; personenbezogene Verwaltungsdaten werden verarbeitet. | **Supported.** Schweigen zur DSFA-Pflicht = Lücke, kein Verstoß. |
| PS-1 | CLEAR PASS | Systemarchitektur: "trifft KEINE selbstständigen Entscheidungen ... Beschlussvorlagen ... Sachbearbeiter prüft jeden Entwurf zwingend eigenhändig ... 4-Augen-Prinzip / Human-in-the-Loop." | **Supported.** Ausdrücklich dokumentierte, echte menschliche Letztentscheidung. Art. 22(3)-Garantien nicht einschlägig, da keine Art.-22-Entscheidung erfolgt. Stärkster Befund. |
| PS-2 | NARROW FLAG | AVV vorhanden aber dünn (nur §§1–4, ohne den Pflichtkatalog Art. 28 Abs. 3 lit. a–h); §3 Unterauftragnehmerliste "nicht öffentlich, auf Anfrage"; §2 EU-Standort Frankfurt, kein Drittlandexport. | **Supported, aber am oberen Rand.** AVV existiert und ist ergänzbar → FLAG vertretbar. Ein strengerer Prüfer könnte den vollständig fehlenden Art.-28-Abs.-3-Katalog als schwerer werten. |
| PS-3 | NARROW FLAG | AGB §5: "Eine explizite Klausel zum Verzicht auf die Nutzung von Prompts zu Modell-Trainingszwecken durch vorgelagerte API-Anbieter ist in diesen AGB nicht enthalten." + Cloud-LLM-Anbindung (Systemarchitektur). TOM-Statelessness betrifft nur die Plattform, nicht den vorgelagerten LLM. | **PLAUSIBLE, zu mild.** Siehe unten. |
| PS-4 | NARROW FLAG | Keine allgemeinverständliche Erläuterung der LLM-Logik für Bürgerauskünfte; nur "fortschrittliche Sprachmodelle". | **Supported.** Technisch/vage, keine Logik-Erläuterung nach Art. 13(2)(f) / DSK 1.8. |

## Die eine strittige Stelle: PS-3

Der Prüfschritt-Wortlaut für CLEAR FAIL verlangt, dass die Bedingungen das Training **erlauben** oder ein offenes System Eingaben **nachweislich** ins Anbietertraining speist. Die AGB *erlauben* Training nicht ausdrücklich, sie stellen fest, dass **kein Ausschluss existiert**; "nachweislich" ist nicht belegt. Nach dem Buchstaben der Checkliste ist NARROW FLAG daher zulässig, und die Nichtregel des Auditors ("ein FAIL braucht einen zitierbaren Widerspruch") stützt das.

Aber es ist das milde Ende. Die tatsächliche Lage: personenbezogene Bürgerdaten fließen an einen vorgelagerten Cloud-LLM, für den vertraglich **kein** Trainingsverbot besteht. `[DSK-OH-1.9]` sagt: fehlt ein Ausschluss und sind personenbezogene Daten betroffen, ist "für diesen Zweck eine Rechtsgrundlage erforderlich" (hier nicht vorhanden), und `[DSK-OH-1.7]` erklärt geschlossene Systeme für vorzugswürdig. Ein realer DSB könnte das als **CLEAR FAIL** einstufen, solange Bürgerdaten ohne Ausschluss und ohne Rechtsgrundlage an das Modell gehen.

**Empfehlung:** Den Befund als *bedingten* FLAG schärfen: NARROW FLAG nur, solange keine personenbezogenen Daten verarbeitet werden, bevor die Klausel gesichert ist; fließen jetzt schon Bürgerdaten über den vorgelagerten LLM ohne Ausschluss, auf CLEAR FAIL heben. Die vom Bericht genannte Anbieter-Handlung ("Ausschluss sichern oder auf ein geschlossenes System wechseln") ist bereits die richtige Abhilfe; nur das Schwere-Label ist die Entscheidung, die dem Menschen gehört.

## Gesamturteil

4 von 5 Befunden sind durch die Quelldokumente vollständig gedeckt; der Auditor hat die Unterlagen **treu gelesen** (jeder Befund lässt sich auf konkreten Dokumenttext zurückführen, nichts erfunden). PS-3 ist substanziell richtig mit einer strittigen, zu milden Schwere-Einstufung, genau die Art Grenzfall, für die die Ermessens-Leitplanke da ist. Das System funktioniert; die eine Einstufung gehört auf den Tisch der oder des Datenschutzbeauftragten.
