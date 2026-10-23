#!/usr/bin/env python3
"""
verify_bdsg.py -- compare reference/bdsg.md with the official BDSG text.

The official source is the XML that gesetze-im-internet.de publishes. Because
that site is not reachable from every build environment, the default URL is the
QuantLaw daily archive of exactly that XML (github.com/QuantLaw/gesetze-im-internet,
branch "data"). Pass a local XML file or another URL to compare against that instead.

For every Absatz printed in reference/bdsg.md it checks that the text is identical
(whitespace-normalised) to the official text, and prints the official "Stand".

Usage:
  python audit/verify_bdsg.py                 # fetch the latest archived XML
  python audit/verify_bdsg.py path/to/BJNR209710017.xml
Exit code 0 if every Absatz matches, 1 otherwise. Stdlib only.
"""
import sys, os, re, html, difflib, urllib.request

DEFAULT_SRC = ("https://raw.githubusercontent.com/QuantLaw/gesetze-im-internet/"
               "data/data/items/bdsg_2018/BJNR209710017.xml")

def load(src):
    if re.match(r'https?://', src):
        with urllib.request.urlopen(src, timeout=30) as r:
            return r.read().decode("utf-8")
    with open(src, encoding="utf-8") as f:
        return f.read()

def official_norms(xml):
    """{"§ 26": plain text of the norm} from the gesetze-im-internet XML."""
    out = {}
    for norm in re.findall(r'<norm\b.*?</norm>', xml, re.S):
        m = re.search(r'<enbez>(.*?)</enbez>', norm)
        c = re.search(r'<textdaten>.*?<Content>(.*?)</Content>', norm, re.S)
        if not m or not c:
            continue
        body = re.sub(r'<(FnR|SUP)[^>]*/?>.*?(</\1>)?', '', c.group(1))
        body = re.sub(r'<BR\s*/>|</?(P|DT|DD|LA|DL)\b[^>]*>', ' ', body)
        body = re.sub(r'<[^>]+>', '', body)
        out[html.unescape(m.group(1)).strip()] = re.sub(r'\s+', ' ', html.unescape(body)).strip()
    return out

def stand(xml):
    return [re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip()
            for s in re.findall(r'<standangabe[^>]*>.*?</standangabe>', xml, re.S)]

def split_absaetze(text):
    parts = re.split(r'(?:(?<=^)|(?<=\s))\((\d+)\)\s', text)
    return {int(parts[i]): re.sub(r'\s+', ' ', parts[i + 1]).strip()
            for i in range(1, len(parts), 2)}

def module_absaetze(path):
    """{"26": {1: text, ...}} from reference/bdsg.md (law text below the --- line)."""
    with open(path, encoding="utf-8") as f:
        body = f.read().split("\n---\n", 1)[1]
    out = {}
    for sec in re.split(r'(?m)^## ', body)[1:]:
        head, rest = sec.split("\n", 1)
        n = re.match(r'§ (\d+) BDSG', head).group(1)
        lines = [l.strip() for l in rest.split("\n")
                 if l.strip() and not l.strip().startswith(("_", ">"))]
        text = " ".join(re.sub(r'^\*\*\((\d+)\)\*\*', r'(\1)', l) for l in lines)
        out[n] = split_absaetze(text)
    return out

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    xml = load(src)
    off = official_norms(xml)
    mod = module_absaetze(os.path.join(base, "reference", "bdsg.md"))

    print(f"# BDSG-Abgleich: reference/bdsg.md gegen amtlichen Text\n\nQuelle: {src}")
    for s in stand(xml):
        print(f"- {s}")
    print("\n| Paragraf | Absatz | Ergebnis |\n|---|---|---|")
    same = diff = 0
    notes = []
    for n, absd in mod.items():
        o = split_absaetze(off.get(f"§ {n}", ""))
        for k, t in absd.items():
            ot = o.get(k)
            if ot == t:
                same += 1
                print(f"| § {n} | {k} | identisch |")
                continue
            diff += 1
            print(f"| § {n} | {k} | ABWEICHUNG |")
            if ot is None:
                notes.append(f"§ {n} Abs. {k}: im amtlichen Text nicht gefunden")
                continue
            a, b = t.split(), ot.split()
            for tag, a1, a2, b1, b2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
                if tag != "equal":
                    notes.append(f"§ {n} Abs. {k}: Modul «{' '.join(a[a1:a2])}» / amtlich «{' '.join(b[b1:b2])}»")
    if notes:
        print("\n## Abweichungen")
        for x in notes:
            print(f"- {x}")
    print(f"\n**{same} identisch, {diff} abweichend: {'PASS' if diff == 0 else 'FAIL'}**")
    sys.exit(0 if diff == 0 else 1)

if __name__ == "__main__":
    main()
