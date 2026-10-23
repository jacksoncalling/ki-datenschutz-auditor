#!/usr/bin/env python3
"""
reference_impl.py -- the web engine's deterministic parts, as a reference.

The web service (Lovable + Supabase edge function) gets a JSON report from Claude
and must then do three things in code. This file is the reference for all three;
the TypeScript edge function ports it function by function, and
`web/test_parity.py` proves that what passes here also passes `audit/checks.py`.

  module_for(org_type, bundesland)     which extra law module applies
  run_gates(report, module, valid_ids) the gates (a mirror of audit/checks.py)
  to_markdown(report, module, org_type) the downloadable report (rules.md format)

Plus `from_markdown()`, used only to turn the repo's existing receipts into JSON
examples for tests and mock data.

Stdlib only.
"""
import re

PS_IDS = ["PS-0", "PS-1", "PS-2", "PS-3", "PS-4"]
SEVERITIES = ["CLEAR PASS", "NARROW FLAG", "CLEAR FAIL"]
NEEDS_DECISION = ["NARROW FLAG", "CLEAR FAIL"]
# Same pattern as CITE_RE in audit/checks.py.
CITE_RE = re.compile(r'\[((?:DSGVO-Art|DSK-OH-|DSG-NRW-§|BDSG-§)[^\]]+)\]')
CORE = "DSGVO + DSK-Orientierungshilfe KI (06.05.2024)"
HINWEIS = ("Diese Vorprüfung ersetzt nicht die Entscheidung der oder des "
           "Datenschutzbeauftragten bzw. der Verantwortlichen. Sie strukturiert und beschleunigt sie.")

# ---------------------------------------------------------------- module

def module_for(org_type, bundesland):
    """'BDSG', 'DSG NRW' or None. Decided in code, never by the model
    (checklist.md, "Ergänzende Ebene")."""
    if org_type == "unternehmen":
        return "BDSG"
    if org_type == "oeffentlich" and bundesland in ("NRW", "Nordrhein-Westfalen"):
        return "DSG NRW"
    return None

def module_line(module, bundesland):
    """The line passed to the model as 'Anzuwendendes Zusatzmodul'."""
    if module == "BDSG":
        return "BDSG (reference/bdsg.md)"
    if module == "DSG NRW":
        return "DSG NRW (reference/dsg-nrw.md)"
    return (f"keines (Landesmodul für {bundesland or 'das Bundesland'} noch nicht enthalten; "
            "im Bericht unter Ergänzendes Recht vermerken)")

def geprueft_gegen(module):
    return CORE + (f" + {module}" if module else "")

# ---------------------------------------------------------------- gates

def applicable(report):
    s = report["schwelle"]
    return bool(s["personenbezogene_daten"]) and bool(s["ki_anwendung"])

def _texts(report):
    """Every free-text field a citation could hide in."""
    out = [report.get("ergaenzendes_recht_hinweis", ""),
           report.get("wichtigste_offene_entscheidung", ""),
           report.get("kurzfazit", ""),
           report.get("einsatzkontext_zusammenfassung", "")]
    for b in report["befunde"]:
        out += [b["fundstelle_dossier"], b["quelle_dokument"], b["bewertung"],
                b["offene_entscheidung"], b["nutzer_naechste_handlung"],
                b["anbieter_naechster_nachweis"], b["titel"]]
        out += [s["zitat"] for s in b["standard"]]
    return out

def clean_id(raw):
    return raw.strip().strip("[]").strip()

def all_citations(report):
    ids = {clean_id(s["id"]) for b in report["befunde"] for s in b["standard"]}
    for t in _texts(report):
        ids |= {clean_id(m) for m in CITE_RE.findall(t or "")}
    return ids

def run_gates(report, module, valid_ids):
    """List of violations as German sentences; empty = report may be shown.
    Call only when applicable(report) is true."""
    v = []
    befunde = report["befunde"]
    present = [b["pruefschritt"] for b in befunde]
    missing = [p for p in PS_IDS if p not in present]
    dupes = sorted({p for p in present if present.count(p) > 1})
    if missing:
        v.append(f"Prüfschritte fehlen: {', '.join(missing)}.")
    if dupes:
        v.append(f"Prüfschritte doppelt: {', '.join(dupes)}.")
    for b in befunde:
        ps = b["pruefschritt"]
        if b["klasse"] not in SEVERITIES:
            v.append(f"{ps}: ungültige Klasse „{b['klasse']}“.")
        if not b["standard"]:
            v.append(f"{ps}: keine Fundstelle im Standard zitiert.")
        if b["klasse"] in NEEDS_DECISION and not b["offene_entscheidung"].strip():
            v.append(f"{ps}: {b['klasse']} ohne Offene Entscheidung.")
        if not b["fundstelle_dossier"].strip():
            v.append(f"{ps}: Fundstelle im Dossier fehlt (Zitat oder „keine Angabe“).")
    ids = all_citations(report)
    phantom = sorted(i for i in ids if i not in valid_ids)
    if phantom:
        v.append(f"Zitate existieren nicht im Standard: {', '.join(phantom)}.")
    foreign = {"BDSG": ("DSG-NRW-",), "DSG NRW": ("BDSG-",), None: ("DSG-NRW-", "BDSG-")}[module]
    mixed = sorted(i for i in ids if i.startswith(foreign))
    if mixed:
        v.append(f"Zitate aus einem nicht anwendbaren Modul ({module or 'kein Zusatzmodul'}): {', '.join(mixed)}.")
    return v

def counts(report):
    return {s: sum(1 for b in report["befunde"] if b["klasse"] == s) for s in SEVERITIES}

# ---------------------------------------------------------------- markdown

def _one_line(s):
    return re.sub(r'\s+', ' ', (s or "").strip())

def _cell(s):
    # table cells: one line, no pipe (checks.py and render.py split on "|")
    return _one_line(s).replace("|", "/")

def _list(xs):
    return "; ".join(_one_line(x) for x in xs) if xs else "keine"

def party_label(org_type):
    return {"unternehmen": "Unternehmen", "oeffentlich": "Öffentliche Stelle"}.get(org_type, "Nutzer")

def to_markdown(report, module, org_type):
    """The downloadable report: rules.md single-column format, then the
    'Ergänzendes Recht' section, then the two-sided table (perspectives.md)."""
    c = counts(report)
    befunde = sorted(report["befunde"], key=lambda b: PS_IDS.index(b["pruefschritt"]))
    L = [f"# Datenschutz-Vorprüfung: {_one_line(report['produkt'])} / {_one_line(report['anbieter'])}",
         f"Einsatzkontext: {_one_line(report['einsatzkontext_zusammenfassung'])}",
         f"Geprüft gegen: {geprueft_gegen(module)}",
         f"Vorgelegte Unterlagen: {_list(report['vorgelegte_unterlagen'])} | Fehlend: {_list(report['fehlende_unterlagen'])}",
         f"Datum: {report['datum']}  ·  Zuständige Aufsicht: {_one_line(report['zustaendige_aufsicht'])}",
         "",
         "## Ergebnis auf einen Blick",
         f"CLEAR PASS: {c['CLEAR PASS']}   ·   NARROW FLAG: {c['NARROW FLAG']}   ·   CLEAR FAIL: {c['CLEAR FAIL']}",
         f"Wichtigste offene Entscheidung: {_one_line(report['wichtigste_offene_entscheidung'])}",
         "",
         "## Befunde"]
    for b in befunde:
        quelle = f" (Quelle: {_one_line(b['quelle_dokument'])})" if b["quelle_dokument"].strip() else ""
        std = "; ".join(f"[{clean_id(s['id'])}] „{_one_line(s['zitat'])}“" for s in b["standard"])
        L += [f"### [{b['pruefschritt']}] {_one_line(b['titel'])} — {b['klasse']}",
              f"- Fundstelle im Dossier: {_one_line(b['fundstelle_dossier'])}{quelle}",
              f"- Standard: {std}",
              f"- Bewertung: {_one_line(b['bewertung'])}"]
        if b["klasse"] in NEEDS_DECISION:
            L.append(f"- Offene Entscheidung (DSB): {_one_line(b['offene_entscheidung'])}")
        L.append("")
    L += ["## Ergänzendes Recht",
          _one_line(report["ergaenzendes_recht_hinweis"]) or "Kein Zusatzmodul angewendet.",
          "",
          "## Befunde (beidseitig)",
          f"| Prüfschritt | Klasse | Standard | {party_label(org_type)}: nächste Handlung | Anbieter: nächster Nachweis |",
          "|---|---|---|---|---|"]
    for b in befunde:
        ids = " ".join(f"[{clean_id(s['id'])}]" for s in b["standard"])
        L.append(f"| [{b['pruefschritt']}] {_cell(b['titel'])} | {b['klasse']} | {ids} | "
                 f"{_cell(b['nutzer_naechste_handlung'])} | {_cell(b['anbieter_naechster_nachweis'])} |")
    L += ["", "## Hinweis", HINWEIS, ""]
    return "\n".join(L)

# ---------------------------------------------------------------- receipts -> JSON (tests/mock data only)

def _field(block, label):
    m = re.search(r'(?m)^- ' + re.escape(label) + r'[^:\n]*:\s*(.*)$', block)
    return m.group(1).strip() if m else ""

def _standard(text):
    out = []
    for part in re.split(r';\s*(?=\[)', text):
        m = re.match(r'\s*\[([^\]]+)\]\s*(.*)', part)
        if m:
            out.append({"id": m.group(1).strip(),
                        "zitat": m.group(2).strip().rstrip(".").strip().strip('„“"').strip()})
    return out

def from_markdown(md, platform_md=None):
    """Turn a single-column receipt (rules.md format) into the report JSON.
    Two-sided action columns come from platform_md when given."""
    head = lambda pat: (re.search(pat, md, re.M).group(1).strip() if re.search(pat, md, re.M) else "")
    title = head(r'^# Datenschutz-Vorprüfung:\s*(.+)$')
    produkt, _, anbieter = title.partition(" / ")
    unterlagen = head(r'^Vorgelegte Unterlagen:\s*(.+)$')
    vorgelegt, _, fehlend = unterlagen.partition("| Fehlend:")
    split = lambda s: [x.strip() for x in re.split(r'[;,]\s*(?![^()]*\))', s) if x.strip() and x.strip() != "keine"]
    dm = re.search(r'(?m)^Datum:\s*(\S+)\s*·\s*Zuständige Aufsicht:\s*(.+)$', md)
    actions = {}
    if platform_md:
        for line in platform_md.splitlines():
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            m = re.match(r'\[(PS-\d)\]', cols[0]) if cols else None
            if m and len(cols) >= 5:
                actions[m.group(1)] = (cols[3], cols[4])
    befunde = []
    for part in re.split(r'(?m)^### ', md)[1:]:
        hm = re.match(r'\[(PS-\d)\]\s*(.+?)\s+—\s+(CLEAR PASS|NARROW FLAG|CLEAR FAIL)', part)
        if not hm:
            continue
        block = re.split(r'(?m)^## ', part)[0]
        ps, cls = hm.group(1), hm.group(3)
        fund = _field(block, "Fundstelle im Dossier")
        qm = re.search(r'\(Abschnitt[^)]*\)\.?$', fund)
        decision = _field(block, "Offene Entscheidung")
        nutzer, anbieter_a = actions.get(ps, ("Erfüllt." if cls == "CLEAR PASS" else decision,
                                              "Erfüllt." if cls == "CLEAR PASS" else "Siehe Offene Entscheidung."))
        befunde.append({
            "pruefschritt": ps, "titel": hm.group(2).strip(), "klasse": cls,
            "fundstelle_dossier": fund,
            "quelle_dokument": qm.group(0).strip("(). ") if qm else "Dossier",
            "standard": _standard(_field(block, "Standard")),
            "bewertung": _field(block, "Bewertung"),
            "offene_entscheidung": decision if cls != "CLEAR PASS" else "",
            "nutzer_naechste_handlung": nutzer, "anbieter_naechster_nachweis": anbieter_a})
    erg = re.search(r'(?ms)^## Ergänzendes Recht[^\n]*\n(.*?)(?=^## )', md)
    schwelle = head(r'^Schwelle:\s*(.+)$')
    c = {s: sum(1 for b in befunde if b["klasse"] == s) for s in SEVERITIES}
    return {
        "produkt": produkt.strip(), "anbieter": anbieter.strip(),
        "datum": dm.group(1) if dm else "",
        "einsatzkontext_zusammenfassung": head(r'^Einsatzkontext:\s*(.+)$') or "nicht angegeben",
        "vorgelegte_unterlagen": split(vorgelegt), "fehlende_unterlagen": split(fehlend),
        "geprueft_gegen": head(r'^Geprüft gegen:\s*(.+)$'),
        "zustaendige_aufsicht": dm.group(2).strip() if dm else "",
        "schwelle": {"personenbezogene_daten": True, "ki_anwendung": True, "begruendung": schwelle},
        "befunde": befunde,
        "ergaenzendes_recht_hinweis": re.sub(r'\s+', ' ', erg.group(1)).strip() if erg else "",
        "wichtigste_offene_entscheidung": head(r'^Wichtigste offene Entscheidung:\s*(.+)$'),
        "kurzfazit": f"{c['CLEAR PASS']} von 5 Prüfschritten erfüllt, {c['NARROW FLAG']} Klärungen offen, "
                     f"{c['CLEAR FAIL']} K.-o.-Kriterien.",
    }
