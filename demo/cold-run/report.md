# Datenschutz-Vorprüfung: OfficeAssist 365 (Nordlicht Software GmbH)
Geprüft gegen: DSGVO + DSK-Orientierungshilfe KI (06.05.2024) + DSG NRW
Vorgelegte Unterlagen: Produkt-/Systembeschreibung, Auftragsverarbeitungsvertrag (AVV), technisch-organisatorische Maßnahmen (TOMs), Nutzungs-/Datenschutzbedingungen | Fehlend: aktuelles Unterauftragnehmer-Verzeichnis (im AVV referenziert, nicht beigefügt), durchgeführte DSFA
Datum: 2026-09-07  ·  Zuständige Aufsicht: LDI NRW

## Ergebnis auf einen Blick
CLEAR PASS: 1   ·   NARROW FLAG: 4   ·   CLEAR FAIL: 0
Wichtigste offene Entscheidung: Vor einer Freigabe ist zu klären, ob Wartungs-/Support-Personal der US-Muttergesellschaft auf Klardaten zugreifen kann, und falls ja ein Übermittlungsmechanismus nach Kapitel V DSGVO zu sichern; parallel ist die empfohlene DSFA tatsächlich durchzuführen.

## Vorbemerkung (Schwelle)
Das Werkzeug verarbeitet personenbezogene Daten (Bürger:innen und Beschäftigte) und ist eine KI-Anwendung (LLM) im Sinne der Orientierungshilfe. Die Vorprüfung ist damit einschlägig, und eine DSFA nach Art. 35 ist voraussichtlich erforderlich (`[DSGVO-Art35-1]`, `[DSK-OH-2.3]`). Die fünf Prüfschritte werden der Reihe nach abgearbeitet.

## Befunde

### [PS-0] Schwelle und DSFA-Pflicht — NARROW FLAG
- Fundstelle im Dossier: "Eine Datenschutz-Folgenabschätzung wird empfohlen und kann durch den Anbieter unterstützt werden." Eine durchgeführte DSFA oder eine konkrete Zulieferung der dafür nötigen Informationen liegt nicht bei.
- Standard: `[DSGVO-Art35-1]` „voraussichtlich ein hohes Risiko für die Rechte und Freiheiten natürlicher Personen"; `[DSK-OH-2.3]` „Beim Einsatz von KI-Anwendungen wird dies vielfach der Fall sein."
- Bewertung: Das Dossier bestreitet die DSFA-Pflicht nicht, erfüllt sie aber auch nicht. Es bleibt bei einer Empfehlung; weder ist eine DSFA durchgeführt, noch liegt die dafür nötige Zulieferung zur Funktionsweise bei. Das ist kein Verstoß, aber eine vor der Freigabe zu schließende Lücke.
- Offene Entscheidung (DSB): DSFA nach Art. 35 durchführen (oder dokumentiert begründen, warum entbehrlich) und vom Anbieter die dafür erforderlichen Systeminformationen verbindlich einfordern.

### [PS-1] Menschliche Letztentscheidung (Human-in-the-Loop) — CLEAR PASS
- Fundstelle im Dossier: "OfficeAssist 365 erstellt ausschließlich Entwürfe und Vorschläge. Jede Ausgabe wird von der zuständigen Sachbearbeiterin oder dem zuständigen Sachbearbeiter geprüft, bearbeitet und verantwortet. Das System versendet nichts eigenständig und trifft keine Entscheidungen." Ein Freigabe- und Bearbeitungsschritt ist im Workflow dokumentiert.
- Standard: `[DSGVO-Art22-1]` Recht, „nicht einer ausschließlich auf einer automatisierten Verarbeitung ... beruhenden Entscheidung unterworfen zu werden"; `[DSK-OH-1.6]` „Eine lediglich formelle Beteiligung eines Menschen im Entscheidungsprozess ist nicht ausreichend."
- Bewertung: Das System trifft keine Entscheidungen, sondern liefert Zuarbeit; die Ausgabe wird von einem Menschen geprüft, bearbeitet und verantwortet. Dass die Ausgabe nicht nur abgezeichnet, sondern bearbeitet wird, spricht für einen tatsächlichen Entscheidungsspielraum und gegen eine bloß formelle Beteiligung. Die Fundstelle trägt die Klasse.

### [PS-2] Auftragsverarbeitung, Unterauftragnehmer und Datenstandort — NARROW FLAG
- Fundstelle im Dossier: AVV nach Art. 28 (Weisungsbindung, Vertraulichkeit, Art. 32, Unterstützung, Löschung/Rückgabe) liegt vor; zur Unterauftragnehmer-Liste verweist der AVV auf ein "jeweils aktuelles Unterauftragnehmer-Verzeichnis im Anbieterportal", dem Dossier ist keine Liste beigefügt; Datenstandort EU (Frankfurt, Amsterdam), aber "Fernwartung und Second-Level-Support erfolgen durch qualifiziertes Personal der Unternehmensgruppe" (Muttergesellschaft in den USA), "ob dieses Personal aus den USA auf Klardaten zugreifen kann und welcher Übermittlungsmechanismus dann greift, wird nicht ausgeführt."
- Standard: `[DSGVO-Art28-2]` „informiert der Auftragsverarbeiter den Verantwortlichen immer über jede beabsichtigte Änderung ... gegen derartige Änderungen Einspruch zu erheben"; `[DSGVO-Art44]` „Allgemeine Grundsätze der Datenübermittlung" (Kapitel V, Drittstaatentransfer).
- Bewertung: Der AVV und ein Widerspruchsrecht bei Änderungen sind vorhanden, damit ist die Auftragsverarbeitung im Kern geregelt und keine Unterauftragnehmer sind aktiv verschwiegen. Zwei Punkte bleiben aber offen: die konkrete Unterauftragnehmer-Liste liegt nicht bei (nur ein Verweis), und ein möglicher Drittstaatenzugriff durch US-Konzernpersonal bei Fernwartung ist weder ausgeschlossen noch mit einem Kapitel-V-Mechanismus unterlegt. Kein Verstoß, aber zwei zu schließende Lücken.
- Offene Entscheidung (DSB): das aktuelle Unterauftragnehmer-Verzeichnis einholen und auf Vollständigkeit prüfen; verbindlich klären, ob US-Konzernpersonal auf Klardaten zugreift, und falls ja einen Übermittlungsmechanismus nach Kapitel V (z. B. Angemessenheitsbeschluss/Standardvertragsklauseln plus Zusatzmaßnahmen) vertraglich sichern.

### [PS-3] Trainingsverbot und datenschutzfreundliche Voreinstellungen — NARROW FLAG
- Fundstelle im Dossier: "Kundeninhalte (Eingaben, hochgeladene Dokumente und Ausgaben) werden nicht zum Training oder zur Verbesserung der Modelle des Anbieters oder Dritter verwendet"; die Trainingsnutzung ist für behördliche Mandanten "produktseitig deaktiviert und kann nicht aktiviert werden". "Zur Speicherung der Eingabe-Historie trifft das Dossier keine Aussage."
- Standard: `[DSK-OH-1.9]` „vorzugswürdig sind daher Anwendungen, die die Ein- und Ausgabedaten nicht zu Trainingszwecken verwenden"; `[DSK-OH-2.5]` Voreinstellungen so, „dass keine Eingabedaten zu Trainingszwecken verarbeitet werden und keine Eingabe-Historie über die Sitzung hinaus gespeichert wird".
- Bewertung: Der Trainingsausschluss ist ausdrücklich, vertraglich und produktseitig hart deaktiviert; das ist der stärkste Punkt des Dossiers und erfüllt die Trainingsvorgabe für sich genommen. Der Prüfschritt verlangt jedoch zusätzlich datenschutzfreundliche Voreinstellungen einschließlich der Eingabe-Historie, und dazu ist das Dossier ausdrücklich stumm. Stille zu einem Pflichtelement bildet den Boden NARROW FLAG; ein voller PASS setzt auch die Default-Einstellung zur Eingabe-Historie voraus.
- Offene Entscheidung (DSB): vom Anbieter bestätigen lassen, dass die Speicherung der Eingabe-Historie über die Sitzung hinaus standardmäßig deaktiviert ist bzw. durch die Nutzer:innen steuerbar bleibt.

### [PS-4] Transparenz und Erklärbarkeit — NARROW FLAG
- Fundstelle im Dossier: "Der Anbieter stellt eine technische Dokumentation der Systemarchitektur und der Modellintegration bereit. Eine allgemeinverständliche Erläuterung der Funktionsweise ('Logik'), mit der die Verwaltung Bürger:innen im Rahmen von Art. 13/15 DSGVO Auskunft geben könnte, ist nicht enthalten."
- Standard: `[DSGVO-Art13-1]` Pflicht, der betroffenen Person „zum Zeitpunkt der Erhebung dieser Daten" die vorgesehenen Informationen mitzuteilen; `[DSK-OH-1.8]` „eine Erläuterung der Methode der Datenverarbeitung bezogen auf die Funktionsweise des Programmablaufs im Zusammenhang mit der konkreten Anwendung".
- Bewertung: Technische Dokumentation liegt vor, eine allgemeinverständliche, bürgertaugliche Erläuterung der Logik fehlt. Damit kann die Verwaltung ihre Informations- und Auskunftspflichten gegenüber Betroffenen nicht vollständig aus Anbieterunterlagen bedienen. Nicht das völlige Fehlen jeder Dokumentation (kein FAIL), aber eine Lücke bei der verständlichen Erklärbarkeit.
- Offene Entscheidung (DSB): vom Anbieter eine allgemeinverständliche Beschreibung der Funktionsweise, Tragweite und möglichen Auswirkungen anfordern, die an Betroffene weitergegeben werden kann.

## Staaten-Ebene (NRW)
Zuständige Aufsicht: LDI NRW, die die DSK-Orientierungshilfe KI ausdrücklich als Prüfmaßstab zugrunde legt. `[DSG-NRW-§46-1]` (Verbot rein automatisierter nachteiliger Einzelentscheidungen, „es sei denn eine Rechtsvorschrift lässt dies ausdrücklich zu") gilt unmittelbar für Gefahrenabwehr/Strafverfolgung und dient hier als Auslegungsmaßstab; da das System keine Entscheidungen trifft (siehe PS-1), ändert es das Ergebnis nicht. Das Diskriminierungsverbot beim Profiling nach § 46 Abs. 3 ist nicht ausgelöst. Keine Änderung eines Befunds durch die Landesebene.

## Hinweis
Diese Vorprüfung ersetzt nicht die Entscheidung der oder des Datenschutzbeauftragten. Sie strukturiert und beschleunigt sie.
