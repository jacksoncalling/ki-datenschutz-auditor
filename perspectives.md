# perspectives.md — the two-sided (platform) rendering

The same audit, read from both sides of the table. One dossier, one set of findings, one set of citations, one severity per Prüfschritt. What differs is only the **next action**, because a gap means something different to each party:

- **Kommune (Nachfrageseite):** what to require or clarify before approving.
- **Anbieter (Angebotsseite):** what to document or contractually secure before offering.

This exists because the real situation is usually not a city auditing a stranger. It is a **Kommune and a Startup already trying to work together**, both needing the same contract to get to signature. The audit becomes a shared punch-list, not a verdict handed down. Both parties open the same report and see the same gaps, described in their own terms.

## What is shared and what is not

Shared, single-homed, never duplicated: `reference/` (the standard), `checklist.md` (the five checks), the three finding classes, and every citation. The platform view does not re-audit; it re-renders. The class of a finding is identical in both columns, because it comes from the dossier against the standard, not from who is reading.

Not shared: the closing action line. Each finding carries two.

## The rendering

Run the normal audit first (`rules.md`). That canonical single-column report is what `audit/checks.py` validates, so verifiability is untouched. Then render the platform view from those same findings:

```
# Deal-Vorprüfung: <Produkt / Anbieter> ↔ <Kommune>
Geprüft gegen: DSGVO + DSK-Orientierungshilfe KI + DSG NRW
Datum: <YYYY-MM-DD>  ·  Zuständige Aufsicht: <LDI ...>

## Deal-Reifegrad (beide Seiten)
Erfüllt: n von 5   ·   Klärungen offen: n   ·   K.-o.-Kriterien (CLEAR FAIL): n
Kurz: <ein Satz, ob und unter welchen Bedingungen unterschriftsreif>

## Befunde (beidseitig)
| Prüfschritt | Klasse | Standard | Kommune: nächste Handlung | Anbieter: nächster Nachweis |
|---|---|---|---|---|
| [PS-0] ... | NARROW FLAG | <ID> | <fordere/prüfe ...> | <lege bei / sichere zu ...> |
| ...
```

## The action-line rule

- **CLEAR PASS:** both columns say "erfüllt" and name the evidence. No action either side.
- **NARROW FLAG:** Kommune column = what to request or clarify. Anbieter column = what to attach or contractually secure. This is where the platform earns its keep: most findings are here, and each becomes a concrete task for exactly one party.
- **CLEAR FAIL:** a K.-o.-Kriterium. Kommune column = do not approve until resolved. Anbieter column = must change the product or contract, not just the paperwork. Mark it clearly; a FAIL is not a document to attach, it is a thing to fix.

## Honesty carried over

Same limit as the one-sided audit, stated to both parties: this checks whether the **paperwork says** the right things, not whether the running system **does** them. For the Anbieter that is exactly the value (it tells them what to document and prove). For the Kommune it is the start of due diligence, not the end. The named human on each side still decides.

## Scope note

The platform view changes nothing about how a Bundesland is added: swap `reference/dsg-<land>.md`, and both columns speak that state's rules. The plan is national spine first (DSGVO + DSK, done), then one state module per regional expert conversation, each conversation also a relationship and a possible pilot.
