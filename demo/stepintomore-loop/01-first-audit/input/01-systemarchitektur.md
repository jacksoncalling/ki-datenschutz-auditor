# Systemarchitektur & Prozessbeschreibung: Step Into More ICM-Plattform

1. Zweck des Systems
Das System "Step Into More ICM" dient der automatisierten Aufbereitung und Strukturierung kommunaler Verwaltungsdaten für die Sachbearbeitung der Stadt Aachen.

2. Datenverarbeitung & Workflow
- Das System liest unstrukturierte Antragsdaten ein und strukturiert diese in standardisierte Markdown-Ordner.
- Für die Textgenerierung wird eine Schnittstelle zu einem Cloud-LLM-Anbieter genutzt.
- Entscheidungskompetenz: Das System trifft KEINE selbstständigen rechtlichen oder administrativen Fallentscheidungen. Sämtliche Prüfergebnisse stellen lediglich Beschlussvorlagen dar. Ein Sachbearbeiter der Stadt Aachen prüft jeden Entwurf zwingend eigenhändig vor der Freigabe (4-Augen-Prinzip / Human-in-the-Loop).
