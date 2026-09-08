# Systemarchitektur & Prozessbeschreibung: Step Into More ICM-Plattform — korrigierte Fassung

1. Zweck des Systems
Das System "Step Into More ICM" dient der automatisierten Aufbereitung und Strukturierung kommunaler Verwaltungsdaten für die Sachbearbeitung der Stadt Aachen.

2. Datenverarbeitung & Workflow
- Das System liest unstrukturierte Antragsdaten ein und strukturiert diese in standardisierte Markdown-Ordner.
- Für die Textgenerierung wird eine Schnittstelle zu einem Cloud-LLM-Anbieter (Aleph Alpha GmbH, EU) genutzt.
- Entscheidungskompetenz: Das System trifft KEINE selbstständigen rechtlichen oder administrativen Fallentscheidungen. Sämtliche Prüfergebnisse stellen lediglich Beschlussvorlagen dar. Ein Sachbearbeiter der Stadt Aachen prüft jeden Entwurf zwingend eigenhändig vor der Freigabe (4-Augen-Prinzip / Human-in-the-Loop).

3. Transparenz und Funktionsweise (allgemeinverständliche Erläuterung)
Für die Erfüllung der Informationspflichten nach Art. 13 und 15 DSGVO stellt der Anbieter eine bürgerverständliche Erläuterung der Logik bereit:
- Das System ordnet eingereichte Angaben festen Feldern zu (Extraktion) und erstellt daraus einen Textentwurf mit einem Sprachmodell (Generierung).
- Es bewertet nichts eigenständig und vergibt keine Scores; es schlägt Formulierungen vor, die ein Mensch prüft und verantwortet.
- Grundlage der Textgenerierung ist ein vortrainiertes Sprachmodell; die Daten der Stadt Aachen fließen nicht in dessen Training (siehe AGB § 5).
Eine Kurzfassung dieser Erläuterung wird Betroffenen auf Anfrage in einfacher Sprache ausgehändigt.
