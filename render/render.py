#!/usr/bin/env python3
"""
render.py -- turn a platform (two-sided) report .md into a standalone HTML page.

Same idea as the DTO demo-scroll pattern: a fixed template with slots, and the
content poured in. Here the content is not hand-written, it is parsed from the
auditor's own markdown output, so the page is a translation of the folder's
report, not a separate design artifact. Content is baked in at generation time
(no runtime JS needed), so the page reads correctly at rest.

Usage:
  python render/render.py [report.md] [-o out.html]
Defaults: report = demo/platform-report.md, out = <report>.html
Stdlib only.
"""
import re, sys, os, argparse, html

CLS = {"CLEAR PASS": "pass", "NARROW FLAG": "flag", "CLEAR FAIL": "fail"}
LABEL = {"CLEAR PASS": "Clear Pass", "NARROW FLAG": "Narrow Flag", "CLEAR FAIL": "Clear Fail"}
WHO = {
    "pass": ("Kommune", "Anbieter"),
    "flag": ("Kommune · nächste Handlung", "Anbieter · nächster Nachweis"),
    "fail": ("Kommune · nicht freigeben", "Anbieter · muss geändert werden"),
}

def esc(s):
    return html.escape(s.strip())

def parse(md):
    d = {}
    # title line: # Deal-...: <Produkt> (<Anbieter>) <arrow> <Kommune> (<Region>)
    m = re.search(r'^#\s*([^:\n]+):\s*(.+?)\s*\(([^)]+)\)\s*↔\s*(.+?)\s*\(([^)]+)\)', md, re.M)
    if m:
        d["TITLE"], d["PRODUKT"], d["ANBIETER"], d["KOMMUNE"], d["REGION"] = \
            (m.group(1).strip(), m.group(2), m.group(3), m.group(4), m.group(5))
    else:
        # graceful fallback: always show the title, warn that the header is partial
        d.update(PRODUKT="", ANBIETER="", KOMMUNE="", REGION="")
        m2 = re.search(r'(?m)^#\s*([^:\n]+):\s*(.+)$', md)
        m1 = re.search(r'(?m)^#\s*(.+)$', md)
        if m2:
            d["TITLE"], d["PRODUKT"] = m2.group(1).strip(), m2.group(2).strip()
        else:
            d["TITLE"] = m1.group(1).strip() if m1 else "Deal-Vorprüfung"
        sys.stderr.write("render.py: warning: title not in 'Produkt (Anbieter) "
                         "↔ Kommune (Region)' form; header filled partially.\n")

    m = re.search(r'(?m)^Geprüft gegen:\s*(.+)$', md)
    d["STANDARD"] = "Geprüft gegen " + m.group(1).strip() if m else ""
    m = re.search(r'(?m)^Datum:\s*(.+?)\s*·\s*Zuständige Aufsicht:\s*(.+)$', md)
    d["DATUM"], d["AUFSICHT"] = (m.group(1).strip(), m.group(2).strip()) if m else ("", "")

    m = re.search(r'(?m)^Kurz:\s*(.+)$', md)
    verdict = m.group(1).strip() if m else ""
    if ". " in verdict:
        lead, rest = verdict.split(". ", 1)
        d["VERDICT_LEAD"], d["VERDICT_REST"] = lead + ".", rest
    else:
        d["VERDICT_LEAD"], d["VERDICT_REST"] = "", verdict

    # findings: table rows beginning "| [PS-"
    findings = []
    for line in md.splitlines():
        if not re.match(r'\s*\|\s*\[PS-', line):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 5:
            sys.stderr.write("render.py: warning: skipping PS row with %d columns "
                             "(expected 5): %s\n" % (len(cols), line.strip()[:70]))
            continue
        ps_m = re.match(r'\[(PS-\d+)\]\s*(.+)', cols[0])
        ps, title = (ps_m.group(1), ps_m.group(2)) if ps_m else ("PS-?", cols[0])
        klass = cols[1].strip()
        cls = CLS.get(klass.upper(), "flag")
        cites = re.findall(r'\[([^\]]+)\]', cols[2])
        findings.append(dict(ps=ps, title=title, klass=klass, cls=cls,
                             cites=cites, kommune=cols[3], anbieter=cols[4]))
    d["_findings"] = findings
    return d

ROW = """    <article class="row {cls}" tabindex="0">
      <div class="row-head">
        <div class="ps"><span class="num">{ps}</span>{title}</div>
        <span class="pill {cls}">{label}</span>
      </div>
      <div class="cites">{cites}</div>
      <div class="cols">
        <div class="col kommune"><div class="who">{who_k}</div><p>{kommune}</p></div>
        <div class="col anbieter"><div class="who">{who_a}</div><p>{anbieter}</p></div>
      </div>
    </article>"""

def build(d):
    f = d["_findings"]
    counts = {"pass": 0, "flag": 0, "fail": 0}
    for x in f:
        counts[x["cls"]] += 1

    rows, segs, labels = [], [], []
    for x in f:
        cls = x["cls"]
        who_k, who_a = WHO[cls]
        cites = "".join('<span class="cite">%s</span>' % esc(c) for c in x["cites"])
        rows.append(ROW.format(cls=cls, ps=esc(x["ps"]), title=esc(x["title"]),
                               label=LABEL.get(x["klass"].upper(), x["klass"]),
                               cites=cites, who_k=esc(who_k), who_a=esc(who_a),
                               kommune=esc(x["kommune"]), anbieter=esc(x["anbieter"])))
        segs.append('<div class="seg %s"></div>' % cls)
        labels.append('<span>%s</span>' % esc(x["ps"]))

    repl = {
        "TITLE": esc(d["TITLE"]), "PRODUKT": esc(d["PRODUKT"]), "ANBIETER": esc(d["ANBIETER"]),
        "KOMMUNE": esc(d["KOMMUNE"]), "REGION": esc(d["REGION"]), "STANDARD": esc(d["STANDARD"]),
        "DATUM": esc(d["DATUM"]), "AUFSICHT": esc(d["AUFSICHT"]), "DEMO_TAG": esc(d["DEMO_TAG"]),
        "N_PASS": str(counts["pass"]), "N_FLAG": str(counts["flag"]), "N_FAIL": str(counts["fail"]),
        "N_TOTAL": str(len(f)), "STRIP_N": str(max(1, len(f))),
        "STRIP_SEGS": "".join(segs), "STRIP_LABELS": "".join(labels),
        "VERDICT_LEAD": esc(d["VERDICT_LEAD"]), "VERDICT_REST": esc(d["VERDICT_REST"]),
        "FINDINGS": "\n".join(rows),
    }
    tpl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.html")
    with open(tpl_path, encoding="utf-8") as f:
        out = f.read()
    for k, v in repl.items():
        out = out.replace("{{%s}}" % k, v)
    if not d["DEMO_TAG"]:
        out = out.replace('<span class="demo-tag"></span>', "")
    return out

def main():
    ap = argparse.ArgumentParser()
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("report", nargs="?", default=os.path.join(base, "demo", "platform-report.md"))
    ap.add_argument("-o", "--out")
    ap.add_argument("--demo", action="store_true",
                    help="stamp the page 'Musterbericht · fiktives Beispiel' (use for synthetic reports)")
    args = ap.parse_args()
    with open(args.report, encoding="utf-8") as f:
        md = f.read()
    data = parse(md)
    data["DEMO_TAG"] = "Musterbericht · fiktives Beispiel" if args.demo else ""
    out = build(data)
    dest = args.out or os.path.splitext(args.report)[0] + ".html"
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(out)
    print("wrote", dest, "(%d bytes)" % len(out.encode("utf-8")))

if __name__ == "__main__":
    main()
