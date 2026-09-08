#!/usr/bin/env python3
"""
checks.py -- deterministic layer of the auditor's eval.

Runs on a REPORT produced by the KI-Datenschutz-Prüfassistent (not on the
auditor's own factory files). It answers, mechanically, the questions a stranger
would ask before trusting the report:

  1. Does it cover every required Prüfschritt?
  2. Is every finding classified with a valid severity?
  3. Does every finding cite at least one provision?
  4. Does every cited provision actually EXIST in reference/ (no phantom cites)?
  5. Does every NARROW FLAG / CLEAR FAIL carry an "Offene Entscheidung" line?
  6. Do the header counts match the findings actually present (gate honesty)?
  7. (optional, --key) Does each Prüfschritt's class match the answer key?

No model, no judgment. The one semantic call -- does the cited text actually
support the finding -- is layer 2, audit/compliance-judge.md.

Usage:
  python checks.py <report.md> [--key <key.md>] [--report <out.md>]
                   [--conventions <conventions.json>]
Exit code 0 if every hard gate passes, 1 otherwise.
"""
import sys, os, re, json, argparse

def load_conventions(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

# ---------- build the set of VALID citation IDs from reference/ ----------

def valid_ids_from_reference(conv, base):
    ref_dir = os.path.normpath(os.path.join(base, conv["reference_dir"]))
    ids = set()

    # DSGVO: "## Art. N DSGVO" opens an article; "**(k)**" opens paragraph k;
    # "  a) " is a lettered point belonging to the paragraph currently open.
    dsgvo = os.path.join(ref_dir, conv["reference_files"]["dsgvo"])
    if os.path.exists(dsgvo):
        cur = para = None
        for line in read_text(dsgvo).splitlines():
            m = re.match(r'## Art\. (\d+) DSGVO', line)
            if m:
                cur = m.group(1); para = None
                ids.add(f"DSGVO-Art{cur}")
                continue
            mp = re.match(r'\*\*\((\d+)\)\*\*', line.strip())
            if mp and cur:
                para = mp.group(1)
                ids.add(f"DSGVO-Art{cur}-{para}")
            ml = re.match(r'\s*([a-p])\)\s', line)
            if ml and cur and para:
                ids.add(f"DSGVO-Art{cur}-{para}{ml.group(1)}")

    # DSK: ## [DSK-OH-X.Y] (literal id)
    dsk = os.path.join(ref_dir, conv["reference_files"]["dsk"])
    if os.path.exists(dsk):
        for line in read_text(dsk).splitlines():
            for m in re.findall(r'\[(DSK-OH-[0-9.]+)\]', line):
                ids.add(m)

    # State: ## § N DSG NRW ; **(k)**
    state = os.path.join(ref_dir, conv["reference_files"]["state"])
    if os.path.exists(state):
        cur = None
        for line in read_text(state).splitlines():
            m = re.match(r'## § (\d+) DSG NRW', line)
            if m:
                cur = m.group(1); ids.add(f"DSG-NRW-§{cur}"); continue
            if cur:
                for k in re.findall(r'\*\*\((\d+)\)\*\*', line):
                    ids.add(f"DSG-NRW-§{cur}-{k}")
    return ids

# ---------- parse the report ----------

CITE_RE = re.compile(r'\[((?:DSGVO-Art|DSK-OH-|DSG-NRW-§)[^\]]+)\]')

def normalize_id(raw):
    # strip spaces; unify. Accept DSGVO-Art22-1, DSK-OH-1.9, DSG-NRW-§46-1
    return raw.strip()

def reference_integrity(conv, base):
    """Guard against a quiet failure of our own mechanism: a citation ID
    resolves because its heading exists, but the section has no body to quote.
    Returns a list of heading-only sections. (Found by the cold run: Art. 44
    was a heading with an empty body.)"""
    ref_dir = os.path.normpath(os.path.join(base, conv["reference_dir"]))
    empty = []
    for fname in conv["reference_files"].values():
        path = os.path.join(ref_dir, fname)
        if not os.path.exists(path):
            continue
        lines = read_text(path).split("\n")
        idxs = [i for i, l in enumerate(lines) if l.startswith("## ")]
        for k, start in enumerate(idxs):
            end = idxs[k + 1] if k + 1 < len(idxs) else len(lines)
            body = []
            for l in lines[start + 1:end]:
                s = l.strip()
                if not s:
                    continue
                if s.startswith("_") and s.endswith("_"):   # subtitle line
                    continue
                s = s.lstrip(">").strip()                    # drop blockquote marker
                if s:
                    body.append(s)
            if len(" ".join(body)) < 20:
                empty.append(f"{fname}: {lines[start].strip()}")
    return empty

def parse_report(path, conv):
    text = read_text(path)
    severities = conv["severities"]
    labels = conv.get("count_line_labels", {s: s for s in severities})
    marker = conv.get("open_decision_marker", "Offene Entscheidung")

    # header counts: built from the configured severities and their labels, in order.
    # Try the single-column labels first, then the platform "Deal-Reifegrad" labels.
    counts = {}
    count_re = r'.*?'.join(re.escape(labels[s]) + r':\s*(\d+)' for s in severities)
    mc = re.search(count_re, text, re.S)
    if not mc and conv.get("platform_count_labels"):
        plabels = conv["platform_count_labels"]
        pcount_re = r'.*?'.join(re.escape(plabels[s]) + r'[^:\n]*:\s*(\d+)' for s in severities)
        mc = re.search(pcount_re, text, re.S)
    if mc:
        counts = {s: int(n) for s, n in zip(severities, mc.groups())}

    # findings, two supported formats:
    #  - single-column canonical: "### [PS-n] <title> — <CLASS>" + "Offene Entscheidung:" line
    #  - two-sided platform table: "| [PS-n] title | CLASS | STANDARD | Kommune… | Anbieter… |"
    findings = []
    dec_re = re.compile(r'(?m)^\s*[-*]?\s*' + re.escape(marker) + r'[^\n]*:')
    parts = re.split(r'(?m)^### ', text)
    for p in parts[1:]:
        head = p.splitlines()[0]
        mh = re.match(r'\[(PS-\d+)\]\s*(.*)', head)
        if not mh:
            continue
        ps = mh.group(1)
        # class = the configured severity token present in the heading line
        cls = next((sev for sev in severities if sev in head), None)
        block = p[:parts_next_marker(p)]
        cites = [normalize_id(c) for c in CITE_RE.findall(block)]
        # require the structured field line, not the bare phrase in prose
        has_decision = dec_re.search(block) is not None
        findings.append({"ps": ps, "class": cls, "cites": cites,
                         "has_decision": has_decision})

    if not findings:  # fall back to the platform (two-sided) table format
        for line in text.splitlines():
            if not re.match(r'\s*\|\s*\[PS-', line):
                continue
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if not re.match(r'\[PS-\d+\]', cols[0]):
                continue
            ps = re.match(r'\[(PS-\d+)\]', cols[0]).group(1)
            klass = cols[1] if len(cols) > 1 else ""
            cls = next((s for s in severities if s == klass or s in klass), None)
            cites = [normalize_id(c) for c in CITE_RE.findall(line)]
            # the two action columns ARE the open decision; both must be filled
            actions = [c for c in cols[3:] if c]
            has_decision = len(actions) >= 2
            findings.append({"ps": ps, "class": cls, "cites": cites,
                             "has_decision": has_decision})
    return counts, findings

def parts_next_marker(p):
    # a finding block ends at the next "## " section or end of string
    m = re.search(r'(?m)^## ', p)
    return m.start() if m else len(p)

# ---------- key ----------

def parse_key(path):
    text = read_text(path)
    expected = {}
    for m in re.finditer(r'\|\s*(PS-\d+)\s*\|\s*(CLEAR PASS|NARROW FLAG|CLEAR FAIL)\s*\|', text):
        expected[m.group(1)] = m.group(2)
    return expected

# ---------- run ----------

def evaluate(report_path, key_path, conv, valid):
    """Run all gates on one report. Returns (ok, gates, findings)."""
    counts, findings = parse_report(report_path, conv)

    gates = []  # (name, ok, detail)

    # G1 coverage: every required Prüfschritt present, and none duplicated
    present = [f["ps"] for f in findings]
    missing = [c for c in conv["required_checks"] if c not in present]
    dupes = sorted({ps for ps in present if present.count(ps) > 1})
    cov_ok = not missing and not dupes
    detail = "alle Prüfschritte vorhanden"
    if missing:
        detail = f"fehlend: {missing}"
    elif dupes:
        detail = f"doppelt: {dupes}"
    gates.append(("coverage", cov_ok, detail))

    # G2 valid severity
    bad_sev = [f["ps"] for f in findings if f["class"] not in conv["severities"]]
    gates.append(("valid-severity", not bad_sev,
                  "alle Befunde klassifiziert" if not bad_sev else f"ohne gültige Klasse: {bad_sev}"))

    # G3 each finding cites at least one provision
    no_cite = [f["ps"] for f in findings if not f["cites"]]
    gates.append(("has-citation", not no_cite,
                  "jeder Befund zitiert" if not no_cite else f"ohne Zitat: {no_cite}"))

    # G4 no phantom citations
    phantom = sorted({c for f in findings for c in f["cites"] if c not in valid})
    gates.append(("citations-resolve", not phantom,
                  "alle Zitate existieren in reference/" if not phantom
                  else f"nicht auffindbar: {phantom}"))

    # G5 open-decision on FLAG/FAIL
    missing_dec = [f["ps"] for f in findings
                   if f["class"] in conv["requires_open_decision"] and not f["has_decision"]]
    gates.append(("open-decision", not missing_dec,
                  "jede FLAG/FAIL hat Offene Entscheidung" if not missing_dec
                  else f"ohne Offene Entscheidung: {missing_dec}"))

    # G6 header counts honest
    actual = {s: sum(1 for f in findings if f["class"] == s) for s in conv["severities"]}
    counts_ok = (counts == actual) if counts else False
    gates.append(("count-honesty", counts_ok,
                  f"Kopfzahl stimmt {actual}" if counts_ok
                  else f"Kopf={counts} vs. tatsächlich={actual}"))

    # G7 key match (optional)
    if key_path:
        expected = parse_key(key_path)
        mism = []
        for f in findings:
            exp = expected.get(f["ps"])
            if exp and exp != f["class"]:
                mism.append(f"{f['ps']}: erwartet {exp}, erhalten {f['class']}")
        gates.append(("key-match", not mism,
                      "Klassen entsprechen dem Schlüssel" if not mism else "; ".join(mism)))

    ok = all(g[1] for g in gates)
    return ok, gates, findings

def render(report_path, valid, ok, gates, findings):
    lines = [f"# Auditor-Eval-Report: {os.path.basename(report_path)}", "",
             f"Valide Zitat-IDs in reference/: {len(valid)}  ·  Befunde im Bericht: {len(findings)}",
             "", "| Gate | Ergebnis | Detail |", "|---|---|---|"]
    for name, passed, detail in gates:
        lines.append(f"| {name} | {'PASS' if passed else 'FAIL'} | {detail} |")
    lines.append("")
    lines.append(f"**Gesamt: {'PASS' if ok else 'FAIL'}**")
    return "\n".join(lines) + "\n"

def run_all(base, conv, valid):
    """Run every real report against its key, plus the planted-defect fixture
    (which MUST fail). This is the one command a stranger can run to see the
    whole eval at once."""
    rep_dir = os.path.join(base, "reports")
    key_dir = os.path.join(base, "keys")
    rows, all_ok = [], True
    # reference integrity first: every cited section must have a body to quote
    empty_sections = reference_integrity(conv, base)
    for name in sorted(os.listdir(rep_dir)):
        if not name.endswith(".report.md"):
            continue
        stem = name[:-len(".report.md")]
        key = os.path.join(key_dir, stem + ".key.md")
        key = key if os.path.exists(key) else None
        ok, _, _ = evaluate(os.path.join(rep_dir, name), key, conv, valid)
        rows.append((name, ok, True))          # expected to pass
        all_ok = all_ok and ok
    # planted defect: expected to FAIL, so it "passes the suite" when it fails
    planted = os.path.join(base, "fixtures", "planted-defect.report.md")
    if os.path.exists(planted):
        ok, _, _ = evaluate(planted, None, conv, valid)
        rows.append(("planted-defect.report.md (muss FAIL sein)", ok, False))
        all_ok = all_ok and (not ok)
    ref_ok = not empty_sections
    all_ok = all_ok and ref_ok
    print("# Auditor-Eval: Gesamtlauf\n")
    print(f"Valide Zitat-IDs in reference/: {len(valid)}\n")
    print("## Referenz-Integrität")
    if ref_ok:
        print("Alle zitierbaren Abschnitte in reference/ haben einen Textkörper. PASS\n")
    else:
        print("FAIL: Abschnitte ohne Textkörper (Überschrift ohne zitierbaren Inhalt):")
        for e in empty_sections:
            print(f"  - {e}")
        print()
    print("## Berichte")
    print("| Bericht | erwartet | Ergebnis | ok? |")
    print("|---|---|---|---|")
    for name, ok, expect_pass in rows:
        got = "PASS" if ok else "FAIL"
        want = "PASS" if expect_pass else "FAIL"
        good = (ok == expect_pass)
        print(f"| {name} | {want} | {got} | {'ok' if good else 'X'} |")
    print(f"\n**Suite: {'PASS' if all_ok else 'FAIL'}**")
    return all_ok

USAGE = """KI-Datenschutz-Auditor -- eval (checks.py)

Ein Bericht wird gegen reference/ geprüft: Abdeckung, Severity, auflösbare
Zitate, Offene-Entscheidung-Zeilen, ehrliche Kopfzahlen.

Das eine, was ein Prüfer sofort laufen lassen kann:
    python audit/checks.py --all

Einzelnen Bericht prüfen:
    python audit/checks.py audit/reports/03-clear-fail.report.md
    python audit/checks.py audit/reports/03-clear-fail.report.md --key audit/keys/03-clear-fail.key.md
"""

def main():
    # print UTF-8 regardless of the platform's default console encoding
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(add_help=True, usage=USAGE)
    ap.add_argument("report", nargs="?")
    ap.add_argument("--all", action="store_true", help="run every report + fixture at once")
    ap.add_argument("--key")
    ap.add_argument("--report", dest="out")
    ap.add_argument("--conventions", default=None)
    args = ap.parse_args()

    base = os.path.dirname(os.path.abspath(__file__))
    conv_path = args.conventions or os.path.join(base, "conventions.json")
    conv = load_conventions(conv_path)
    valid = valid_ids_from_reference(conv, base)

    if args.all:
        sys.exit(0 if run_all(base, conv, valid) else 1)

    if not args.report:
        print(USAGE)
        sys.exit(0)

    ok, gates, findings = evaluate(args.report, args.key, conv, valid)
    out = render(args.report, valid, ok, gates, findings)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
    print(out)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
