# Datenschutz-Vorprüfung: PLANTED DEFECTS (Testbericht mit absichtlichen Fehlern)
Geprüft gegen: DSGVO + DSK-Orientierungshilfe KI (06.05.2024) + DSG NRW
Vorgelegte Unterlagen: (Testfall) | Fehlend: (Testfall)
Datum: 2026-09-07  ·  Zuständige Aufsicht: LDI NRW

> Dieser Bericht ist bewusst fehlerhaft. Er dient als Gegenprobe: `checks.py` muss
> jeden der fünf eingebauten Defekte erkennen und mit Exit-Code 1 abbrechen. Ein
> Auditor, der nur besteht, ist wertlos. Erwartete Antwortdatei: `audit/keys/planted-defect.key.md`.

## Ergebnis auf einen Blick
CLEAR PASS: 2   ·   NARROW FLAG: 1   ·   CLEAR FAIL: 1

## Befunde

### [PS-0] Schwelle und DSFA-Pflicht — UNKLAR
- Fundstelle im Dossier: (Testfall)
- Standard: [DSGVO-Art35-1]
- Bewertung: DEFEKT 1: ungültige Severity-Klasse "UNKLAR".

### [PS-1] Menschliche Letztentscheidung — CLEAR FAIL
- Fundstelle im Dossier: (Testfall)
- Standard: [DSGVO-Art99-9]
- Bewertung: DEFEKT 2: Phantomzitat, Art. 99 Abs. 9 existiert nicht in reference/. DEFEKT 3: CLEAR FAIL ohne "Offene Entscheidung"-Zeile.

### [PS-2] Auftragsverarbeitung — NARROW FLAG
- Fundstelle im Dossier: (Testfall)
- Standard: (kein Zitat)
- Bewertung: DEFEKT 4: Befund ohne jede Zitat-ID.
- Offene Entscheidung (DSB): (Testfall)

### [PS-3] Trainingsverbot und Voreinstellungen — CLEAR PASS
- Fundstelle im Dossier: (Testfall)
- Standard: [DSK-OH-1.9]
- Bewertung: DEFEKT 5 (indirekt): PS-4 fehlt vollständig, und die Kopfzahlen oben stimmen nicht mit den tatsächlichen Klassen überein.

## Hinweis
Diese Vorprüfung ersetzt nicht die Entscheidung der oder des Datenschutzbeauftragten.
