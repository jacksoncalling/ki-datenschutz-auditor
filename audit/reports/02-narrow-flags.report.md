# Datenschutz-Vorprüfung: FlowDesk für Verwaltungen / FlowDesk AI
Geprüft gegen: DSGVO + DSK-Orientierungshilfe KI (06.05.2024) + DSG NRW
Vorgelegte Unterlagen: Produktbeschreibung, AVV, TOMs | Fehlend: DSFA, gesonderte Trainingsklausel
Datum: 2026-09-07  ·  Zuständige Aufsicht: LDI NRW

## Ergebnis auf einen Blick
CLEAR PASS: 0   ·   NARROW FLAG: 5   ·   CLEAR FAIL: 0
Wichtigste offene Entscheidung: Vor einer Freigabe muss der Anbieter die Trainingsnutzung vertraglich ausschließen und den Drittstaatenzugriff der US-Muttergesellschaft klären.

## Befunde

### [PS-0] Schwelle und DSFA-Pflicht — NARROW FLAG
- Fundstelle im Dossier: "Zur Datenschutz-Folgenabschätzung nach Art. 35 DSGVO enthält das Dossier keine Angaben."
- Standard: [DSGVO-Art35-1] „führt der Verantwortliche vorab eine Abschätzung der Folgen ... durch"; [DSK-OH-2.3] „Beim Einsatz von KI-Anwendungen wird dies vielfach der Fall sein."
- Bewertung: Es werden personenbezogene Daten in der Sachbearbeitung verarbeitet, eine DSFA ist wahrscheinlich erforderlich, das Dossier schweigt jedoch dazu. Kein Verstoß, aber eine zu schließende Lücke.
- Offene Entscheidung (DSB): DSFA-Pflicht anhand der Muss-Liste der LDI NRW feststellen und vom Anbieter die dafür nötigen Systeminformationen anfordern.

### [PS-1] Menschliche Letztentscheidung — NARROW FLAG
- Fundstelle im Dossier: "prüft eine Sachbearbeiterin oder ein Sachbearbeiter die Vorschläge und gibt sie frei" (Umfang des Entscheidungsspielraums nicht beschrieben).
- Standard: [DSGVO-Art22-1]; [DSK-OH-1.6] „Eine lediglich formelle Beteiligung eines Menschen im Entscheidungsprozess ist nicht ausreichend."; [DSG-NRW-§46-1].
- Bewertung: Ein Mensch gibt frei, aber ob ein tatsächlicher Entscheidungsspielraum besteht oder nur formal abgezeichnet wird, ist nicht belegt.
- Offene Entscheidung (DSB): vom Anbieter die Prozessbeschreibung anfordern, die den tatsächlichen Entscheidungsspielraum der Sachbearbeitung nachweist.

### [PS-2] Auftragsverarbeitung, Unterauftragnehmer und Datenstandort — NARROW FLAG
- Fundstelle im Dossier: "Eine Liste der Unterauftragnehmer wird 'auf Anfrage bereitgestellt' ... Zu Support- und Wartungszugriffen durch die Muttergesellschaft trifft das Dossier keine Aussage."
- Standard: [DSGVO-Art28-2] Genehmigung/Information bei Unterauftragnehmern; [DSGVO-Art44] allgemeine Grundsätze der Datenübermittlung; [DSK-OH-2.1].
- Bewertung: Ein AVV liegt vor, doch die Unterauftragnehmerliste fehlt im Dossier und ein möglicher Drittstaatenzugriff der US-Mutter ist nicht adressiert.
- Offene Entscheidung (DSB): vollständige Unterauftragnehmerliste einholen und den Zugriff aus Drittstaaten (Support, Konzernmutter) samt Kapitel-V-Mechanismus klären.

### [PS-3] Trainingsverbot und datenschutzfreundliche Voreinstellungen — NARROW FLAG
- Fundstelle im Dossier: "Daten würden 'sicher und vertraulich' verarbeitet. Ob Eingaben oder Ausgaben ... zum Training ... verwendet werden, wird nicht ausdrücklich geregelt."
- Standard: [DSK-OH-1.9] Nutzung zu Trainingszwecken ausschließen; [DSK-OH-2.5] Default-Voreinstellungen; [DSGVO-Art5-1] Zweckbindung.
- Bewertung: Die häufigste Lücke: allgemeine Sicherheitszusage ohne ausdrücklichen Trainingsausschluss und ohne dokumentierte Voreinstellung. „Sicher" ist kein Trainingsverbot.
- Offene Entscheidung (DSB): ausdrücklichen vertraglichen Ausschluss der Trainings-/Fine-Tuning-Nutzung sowie Default-off verlangen.

### [PS-4] Transparenz und Erklärbarkeit — NARROW FLAG
- Fundstelle im Dossier: "technische Dokumentation der Systemarchitektur ... Eine allgemeinverständliche Erläuterung der Logik für die Auskunft gegenüber Bürger:innen ... ist nicht enthalten."
- Standard: [DSGVO-Art13-1]; [DSK-OH-1.8] „Erläuterung der Methode der Datenverarbeitung ... auf ein verständliches Maß".
- Bewertung: Technische Doku vorhanden, aber ohne bürgerverständliche Erläuterung kann die Kommune Auskunftsersuchen nach Art. 13/15 nicht sicher bedienen.
- Offene Entscheidung (DSB): eine allgemeinverständliche Erläuterung der Logik für Betroffene nachfordern.

## Hinweis
Diese Vorprüfung ersetzt nicht die Entscheidung der oder des Datenschutzbeauftragten. Sie strukturiert und beschleunigt sie.
