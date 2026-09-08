# Deal-Vorprüfung: Step Into More ICM-Plattform ↔ Stadt Aachen
Geprüft gegen: DSGVO + DSK-Orientierungshilfe KI (06.05.2024) + DSG NRW
Vorgelegte Unterlagen: Systemarchitektur, AVV, TOM, AGB (Auszug), DSFA-Zulieferung | Fehlend: keine
Datum: 2026-09-08  ·  Zuständige Aufsicht: LDI NRW

## Deal-Reifegrad (beide Seiten)
Erfüllt: 5 von 5   ·   Klärungen offen: 0   ·   K.-o.-Kriterien (CLEAR FAIL): 0
Kurz: Alle fünf Prüfschritte sind durch die vorgelegten Unterlagen abgedeckt; der Deal ist aus Sicht dieser Vorprüfung unterschriftsreif.

## Befunde (beidseitig)
| Prüfschritt | Klasse | Standard | Kommune: nächste Handlung | Anbieter: nächster Nachweis |
|---|---|---|---|---|
| [PS-0] Schwelle und DSFA-Pflicht | CLEAR PASS | [DSGVO-Art35-1], [DSK-OH-2.3] | erfüllt (DSFA durchgeführt, Anbieter-Zulieferung liegt vor) | erfüllt (Funktionsinformationen zur DSFA bereitgestellt) |
| [PS-1] Menschliche Letztentscheidung | CLEAR PASS | [DSGVO-Art22-1], [DSK-OH-1.6], [DSG-NRW-§46-1] | erfüllt (4-Augen-Prinzip / HITL dokumentiert) | erfüllt (System trifft keine Fallentscheidungen, nur Beschlussvorlagen) |
| [PS-2] Auftragsverarbeitung, Unterauftragnehmer, Datenstandort | CLEAR PASS | [DSGVO-Art28-3], [DSGVO-Art28-2], [DSGVO-Art44], [DSK-OH-2.1] | erfüllt (AVV mit Art.-28-Abs.-3-Katalog, EU-Hosting, Unterauftragnehmer offengelegt) | erfüllt (vollständige Unterauftragnehmerliste, Änderungsmitteilung und Widerspruchsrecht zugesichert) |
| [PS-3] Trainingsverbot und Voreinstellungen | CLEAR PASS | [DSK-OH-1.9], [DSK-OH-2.5], [DSGVO-Art5-1] | erfüllt (vertraglicher Trainingsausschluss und Default-off dokumentiert) | erfüllt (Trainingsausschluss dem LLM-Anbieter auferlegt, Default-off für Training und Historie) |
| [PS-4] Transparenz und Erklärbarkeit | CLEAR PASS | [DSGVO-Art13-2f], [DSGVO-Art13-1], [DSK-OH-1.8] | erfüllt (allgemeinverständliche Logik-Erläuterung für Bürgerauskünfte liegt vor) | erfüllt (Funktionsweise-Dokumentation und Kurzfassung in einfacher Sprache bereitgestellt) |

## Befunde (Einzeldarstellung)

### [PS-0] Schwelle und DSFA-Pflicht — CLEAR PASS
- Fundstelle im Dossier: „Wegen der Verarbeitung personenbezogener Verwaltungsdaten mit einer KI-Anwendung wurde ein voraussichtlich hohes Risiko angenommen und eine Datenschutz-Folgenabschätzung nach Art. 35 DSGVO durchgeführt." (DSFA, Abschnitt 1)
- Standard: [DSGVO-Art35-1] „Hat eine Form der Verarbeitung, insbesondere bei Verwendung neuer Technologien, aufgrund der Art, des Umfangs, der Umstände und der Zwecke der Verarbeitung voraussichtlich ein hohes Risiko für die Rechte und Freiheiten natürlicher Personen zur Folge, so führt der Verantwortliche vorab eine Abschätzung der Folgen der vorgesehenen Verarbeitungsvorgänge für den Schutz personenbezogener Daten durch." [DSK-OH-2.3] „Beim Einsatz von KI-Anwendungen wird dies vielfach der Fall sein."
- Bewertung: Eine DSFA wurde durchgeführt; der Anbieter stellt die zur Durchführung erforderlichen Informationen zur Funktionsweise bereit (Verarbeitungszwecke, Datenarten, Datenflüsse inkl. LLM, TOMs, Risikominderungsmaßnahmen). Die abschließende Bewertung obliegt dem DSB der Stadt Aachen, was korrekt vermerkt ist.

### [PS-1] Menschliche Letztentscheidung (Human-in-the-Loop) — CLEAR PASS
- Fundstelle im Dossier: „Das System trifft KEINE selbstständigen rechtlichen oder administrativen Fallentscheidungen. Sämtliche Prüfergebnisse stellen lediglich Beschlussvorlagen dar. Ein Sachbearbeiter der Stadt Aachen prüft jeden Entwurf zwingend eigenhändig vor der Freigabe (4-Augen-Prinzip / Human-in-the-Loop)." (Systemarchitektur, Abschnitt 2)
- Standard: [DSGVO-Art22-1] „nicht einer ausschließlich auf einer automatisierten Verarbeitung ... beruhenden Entscheidung unterworfen zu werden"; [DSK-OH-1.6] „muss das Verfahren so gestaltet werden, dass dem entscheidenden Menschen ein tatsächlicher Entscheidungsspielraum zukommt"; [DSG-NRW-§46-1] „Entscheidungen, die für die betroffene Person mit einer nachteiligen Rechtsfolge verbunden sind ... dürfen nicht ausschließlich auf eine automatische Verarbeitung ... gestützt werden".
- Bewertung: Das System erstellt Beschlussvorlagen, keine Entscheidungen. Der Sachbearbeiter prüft eigenhändig mit echtem Entscheidungsspielraum (4-Augen-Prinzip). Da das System keine Art.-22-Entscheidung trifft, sondern nur Entwürfe liefert, ist Art. 22(3) nicht einschlägig und dessen Fehlen kein Defizit. Die Anforderung ist vollständig erfüllt.

### [PS-2] Auftragsverarbeitung, Unterauftragnehmer und Datenstandort — CLEAR PASS
- Fundstelle im Dossier: AVV §§ 1-5, insbesondere § 4 lit. a-h (vollständiger Art.-28-Abs.-3-Katalog); § 3 Unterauftragnehmer: „AWS Europe (eu-central-1, Frankfurt) — Hosting; Aleph Alpha GmbH (Heidelberg, EU) — Cloud-LLM / Textgenerierung"; „Weitere Unterauftragnehmer werden nur mit vorheriger Genehmigung hinzugezogen. Der Auftragnehmer informiert den Auftraggeber vorab über jede beabsichtigte Änderung; der Auftraggeber kann Einspruch erheben"; § 2: „Sämtliche Datenverarbeitungen und Serverinfrastrukturen befinden sich im Rechenzentrum Frankfurt am Main (AWS Region eu-central-1). Es findet kein Datenexport in Drittstaaten außerhalb des EWR statt."
- Standard: [DSGVO-Art28-3] „Dieser Vertrag ... sieht insbesondere vor, dass der Auftragsverarbeiter a) die personenbezogenen Daten nur auf dokumentierte Weisung des Verantwortlichen ... verarbeitet"; [DSGVO-Art28-2] „informiert der Auftragsverarbeiter den Verantwortlichen immer über jede beabsichtigte Änderung ... wodurch der Verantwortliche die Möglichkeit erhält, gegen derartige Änderungen Einspruch zu erheben"; [DSGVO-Art44] Drittstaatenübermittlung nur unter Kapitel-V-Bedingungen; [DSK-OH-2.1] Auftragsverarbeitungsverhältnis bei Cloud-KI.
- Bewertung: Der AVV deckt alle Pflichten nach Art. 28 Abs. 3 lit. a-h ab. Die Unterauftragnehmerliste ist vollständig und namentlich offengelegt, mit Änderungsmitteilung und Widerspruchsrecht. Hosting und LLM-Anbieter befinden sich in der EU (Frankfurt, Heidelberg). Ein Drittstaatenexport findet nicht statt.

### [PS-3] Trainingsverbot und datenschutzfreundliche Voreinstellungen — CLEAR PASS
- Fundstelle im Dossier: „Der Auftragnehmer schließt vertraglich aus, dass Eingaben, Prompts, hochgeladene Dokumente oder Ausgaben der Stadt Aachen zum Training oder Fine-Tuning eigener oder fremder Modelle verwendet werden. Dieser Ausschluss ist dem vorgelagerten LLM-Anbieter (Aleph Alpha GmbH) vertraglich auferlegt und dem Auftraggeber gegenüber zugesichert." und „Für die von der Stadt Aachen genutzten Zugänge sind die Funktionen zur Nutzung von Eingaben für das KI-Training sowie die Speicherung einer Eingabe-Historie standardmäßig deaktiviert und können nur durch den Auftraggeber aktiviert werden." (AGB § 5)
- Standard: [DSK-OH-1.9] „Datenschutzrechtlich vorzugswürdig sind daher Anwendungen, die die Ein- und Ausgabedaten nicht zu Trainingszwecken verwenden."; [DSK-OH-2.5] „so gewählt werden, dass keine Eingabedaten zu Trainingszwecken verarbeitet werden und keine Eingabe-Historie über die Sitzung hinaus gespeichert wird"; [DSGVO-Art5-1] Zweckbindung (lit. b).
- Bewertung: Der vertragliche Trainingsausschluss ist ausdrücklich, umfasst Ein- und Ausgabedaten, und ist dem vorgelagerten LLM-Anbieter auferlegt. Training und Eingabe-Historie sind standardmäßig deaktiviert (Default-off). Die Vorgabe ist vollständig erfüllt.

### [PS-4] Transparenz und Erklärbarkeit — CLEAR PASS
- Fundstelle im Dossier: „Für die Erfüllung der Informationspflichten nach Art. 13 und 15 DSGVO stellt der Anbieter eine bürgerverständliche Erläuterung der Logik bereit"; „Das System ordnet eingereichte Angaben festen Feldern zu (Extraktion) und erstellt daraus einen Textentwurf mit einem Sprachmodell (Generierung). Es bewertet nichts eigenständig und vergibt keine Scores; es schlägt Formulierungen vor, die ein Mensch prüft und verantwortet." und „Eine Kurzfassung dieser Erläuterung wird Betroffenen auf Anfrage in einfacher Sprache ausgehändigt." (Systemarchitektur, Abschnitt 3)
- Standard: [DSGVO-Art13-2f] „aussagekräftige Informationen über die involvierte Logik sowie die Tragweite und die angestrebten Auswirkungen einer derartigen Verarbeitung für die betroffene Person"; [DSGVO-Art13-1] allgemeine Informationspflicht; [DSK-OH-1.8] „müssen sie darauf achten, dass Ihnen vom Anbieter ausreichend Informationen zur Verfügung gestellt werden, um die Transparenzanforderungen der Art. 12 ff. DS-GVO umsetzen zu können."
- Bewertung: Der Anbieter stellt eine allgemeinverständliche Erläuterung der Funktionsweise bereit, die für Bürgerauskünfte nach Art. 13/15 geeignet ist. Die Erläuterung beschreibt Extraktion und Generierung ohne technischen Jargon. Eine Kurzfassung in einfacher Sprache wird Betroffenen auf Anfrage ausgehändigt.

## Landesebene (NRW)
Zuständige Aufsichtsbehörde: LDI NRW. § 46 Abs. 1 DSG NRW (Verbot nachteiliger automatisierter Einzelentscheidungen) ist durch den dokumentierten Human-in-the-Loop (PS-1) gewahrt. § 46 Abs. 3 DSG NRW (Diskriminierungsverbot beim Profiling) ist nicht einschlägig, da das System kein Profiling betreibt und keine eigenständigen Bewertungen oder Scores vergibt.

## Hinweis
Diese Vorprüfung ersetzt nicht die Entscheidung der oder des Datenschutzbeauftragten. Sie strukturiert und beschleunigt sie.
