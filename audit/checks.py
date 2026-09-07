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

# ---------- build the set of VALID citation IDs from reference/ ----------

def valid_ids_from_reference(conv, base):
    ref_dir = os.path.normpath(os.path.join(base, conv["reference_dir"]))
    ids = set()

    # DSGVO: "## Art. N DSGVO" opens an article; "**(k)**" opens paragraph k;
    # "  a) " is a lettered point belonging to the paragraph currently open.
    dsgvo = os.path.join(ref_dir, conv["reference_files"]["dsgvo"])
    if os.path.exists(dsgvo):
        cur = para = None
        for line in open(dsgvo, encoding="utf-8"):
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
        for line in open(dsk, encoding="utf-8"):
            for m in re.findall(r'\[(DSK-OH-[0-9.]+)\]', line):
                ids.add(m)

    # State: ## § N DSG NRW ; **(k)**
    state = os.path.join(ref_dir, conv["reference_files"]["state"])
    if os.path.exists(state):
        cur = None
        for line in open(state, encoding="utf-8"):
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

def parse_report(path):
    text = open(path, encoding="utf-8").read()
    # header counts
    counts = {}
    mc = re.search(r'CLEAR PASS:\s*(\d+).*?NARROW FLAG:\s*(\d+).*?CLEAR FAIL:\s*(\d+)', text, re.S)
    if mc:
        counts = {"CLEAR PASS": int(mc.group(1)),
                  "NARROW FLAG": int(mc.group(2)),
                  "CLEAR FAIL": int(mc.group(3))}
    # findings: ### [PS-n] <title> — <CLASS>
    findings = []
    parts = re.split(r'(?m)^### ', text)
    for p in parts[1:]:
        head = p.splitlines()[0]
        mh = re.match(r'\[(PS-\d+)\]\s*(.*)', head)
        if not mh:
            continue
        ps = mh.group(1)
        # class = last severity token appearing in the heading line
        cls = None
        for sev in ["CLEAR PASS", "NARROW FLAG", "CLEAR FAIL"]:
            if sev in head:
                cls = sev
        body_end = parts_next_marker(p)
        block = p[:body_end]
        cites = [normalize_id(c) for c in CITE_RE.findall(block)]
        # require the structured field line, not the bare phrase in prose
        has_decision = re.search(r'(?m)^\s*[-*]?\s*Offene Entscheidung[^\n]*:', block) is not None
        findings.append({"ps": ps, "class": cls, "cites": cites,
                         "has_decision": has_decision})
    return counts, findings

def parts_next_marker(p):
    # a finding block ends at the next "## " section or end of string
    m = re.search(r'(?m)^## ', p)
    return m.start() if m else len(p)

# ---------- key ----------

def parse_key(path):
    text = open(path, encoding="utf-8").read()
    expected = {}
    for m in re.finditer(r'\|\s*(PS-\d+)\s*\|\s*(CLEAR PASS|NARROW FLAG|CLEAR FAIL)\s*\|', text):
        expected[m.group(1)] = m.group(2)
    return expected

# ---------- run ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--key")
    ap.add_argument("--report", dest="out")
    ap.add_argument("--conventions", default=None)
    args = ap.parse_args()

    base = os.path.dirname(os.path.abspath(__file__))
    conv_path = args.conventions or os.path.join(base, "conventions.json")
    conv = load_conventions(conv_path)

    valid = valid_ids_from_reference(conv, base)
    counts, findings = parse_report(args.report)

    gates = []  # (name, ok, detail)
    advisory = []

    # G1 coverage
    present = {f["ps"] for f in findings}
    missing = [c for c in conv["required_checks"] if c not in present]
    gates.append(("coverage", not missing,
                  "alle Prüfschritte vorhanden" if not missing else f"fehlend: {missing}"))

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
    key_gate = None
    if args.key:
        expected = parse_key(args.key)
        mism = []
        for f in findings:
            exp = expected.get(f["ps"])
            if exp and exp != f["class"]:
                mism.append(f"{f['ps']}: erwartet {exp}, erhalten {f['class']}")
        key_gate = ("key-match", not mism,
                    "Klassen entsprechen dem Schlüssel" if not mism else "; ".join(mism))
        gates.append(key_gate)

    ok = all(g[1] for g in gates)

    lines = []
    lines.append(f"# Auditor-Eval-Report: {os.path.basename(args.report)}")
    lines.append("")
    lines.append(f"Valide Zitat-IDs in reference/: {len(valid)}  ·  Befunde im Bericht: {len(findings)}")
    lines.append("")
    lines.append("| Gate | Ergebnis | Detail |")
    lines.append("|---|---|---|")
    for name, passed, detail in gates:
        lines.append(f"| {name} | {'PASS' if passed else 'FAIL'} | {detail} |")
    lines.append("")
    lines.append(f"**Gesamt: {'PASS' if ok else 'FAIL'}**")
    out = "\n".join(lines) + "\n"

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
    print(out)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
