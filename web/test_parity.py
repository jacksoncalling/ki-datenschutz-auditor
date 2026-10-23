#!/usr/bin/env python3
"""
test_parity.py -- prove the web engine and audit/checks.py agree.

The web service shows a report only if web/reference_impl.py run_gates() passes,
and offers the Markdown that to_markdown() writes. The promise to users is:
"anything the website shows also passes audit/checks.py". This test checks it:

1. Round trip: every example in web/bundle/examples/ passes the web gates, and its
   generated Markdown passes checks.py (including key-match where a key exists).
2. Defects: each planted defect is rejected by the web gates AND, where checks.py
   can see it in the Markdown, by checks.py too.
3. Freshness: web/bundle/ matches a fresh build of export_bundle.py.

Usage: python web/test_parity.py   (exit 0 = all agree). Stdlib only.
"""
import sys, os, json, copy, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "audit"))
sys.path.insert(0, os.path.join(BASE, "web"))
import checks                 # noqa: E402
import reference_impl as ref  # noqa: E402
import export_bundle          # noqa: E402

KEYS = {"company-applicant-screening": "audit/keys/04-company-mixed.key.md",
        "public-body-clean-pass": "audit/keys/01-clean-pass.key.md"}

def checks_verdict(md, key=None):
    conv = checks.load_conventions(os.path.join(BASE, "audit", "conventions.json"))
    valid = checks.valid_ids_from_reference(conv, os.path.join(BASE, "audit"))
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(md)
        path = f.name
    try:
        ok, gates, _ = checks.evaluate(path, os.path.join(BASE, key) if key else None, conv, valid)
    finally:
        os.unlink(path)
    return ok, [g[0] for g in gates if not g[1]]

def defects(report):
    """(name, mutated report, checks.py can see it in the Markdown?)"""
    out = []
    def mut(name, fn, visible=True):
        r = copy.deepcopy(report); fn(r); out.append((name, r, visible))
    flags = [n for n, b in enumerate(report["befunde"]) if b["klasse"] != "CLEAR PASS"]
    i = flags[0] if flags else 0
    mut("phantom citation in bewertung",
        lambda r: r["befunde"][0].__setitem__("bewertung", r["befunde"][0]["bewertung"] + " Vgl. [DSGVO-Art6-1]."))
    mut("phantom citation in ergaenzendes_recht_hinweis",
        lambda r: r.__setitem__("ergaenzendes_recht_hinweis", r["ergaenzendes_recht_hinweis"] + " Siehe [BDSG-§99-1]."))
    mut("phantom id in standard",
        lambda r: r["befunde"][1]["standard"].append({"id": "DSK-OH-9.9", "zitat": "x"}))
    mut("missing PS-4", lambda r: r.__setitem__("befunde", [b for b in r["befunde"] if b["pruefschritt"] != "PS-4"]))
    mut("duplicate PS-0", lambda r: r["befunde"].append(copy.deepcopy(r["befunde"][0])))
    def no_decision(r):
        # on an all-PASS report, turn one finding into a FLAG first
        r["befunde"][i]["klasse"] = r["befunde"][i]["klasse"] if flags else "NARROW FLAG"
        r["befunde"][i]["offene_entscheidung"] = ""
    mut("FLAG/FAIL without offene_entscheidung", no_decision)
    mut("finding without standard", lambda r: r["befunde"][2].__setitem__("standard", []))
    mut("empty fundstelle_dossier", lambda r: r["befunde"][3].__setitem__("fundstelle_dossier", ""), visible=False)
    return out

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    valid = set(json.load(open(os.path.join(BASE, "web", "bundle", "valid-ids.json"), encoding="utf-8")))
    failures, rows = [], []

    for name in sorted(KEYS):
        ex = json.load(open(os.path.join(BASE, "web", "bundle", "examples", name + ".json"), encoding="utf-8"))
        org, report = ex["org_type"], ex["report"]
        module = ref.module_for(org, ex["bundesland"])
        v = ref.run_gates(report, module, valid)
        ok, failed = checks_verdict(ref.to_markdown(report, module, org), KEYS[name])
        good = not v and ok
        rows.append((f"{name}: round trip", "web PASS, checks PASS",
                     f"web {'PASS' if not v else 'FAIL'}, checks {'PASS' if ok else 'FAIL ' + str(failed)}", good))
        if not good:
            failures.append(name + " round trip: " + "; ".join(v) + str(failed))

        # module consistency: the same report under the other module must fail both
        other = "oeffentlich" if org == "unternehmen" else "unternehmen"
        om = ref.module_for(other, "NRW")
        v2 = ref.run_gates(report, om, valid)
        ok2, _ = checks_verdict(ref.to_markdown(report, om, other))
        uses_module = any(i.startswith(("BDSG-", "DSG-NRW-")) for i in ref.all_citations(report))
        if uses_module:
            good = bool(v2) and not ok2
            rows.append((f"{name}: under the wrong module", "web FAIL, checks FAIL",
                         f"web {'FAIL' if v2 else 'PASS'}, checks {'FAIL' if not ok2 else 'PASS'}", good))
            if not good:
                failures.append(name + " wrong module not caught")

        for dname, bad, visible in defects(report):
            vb = ref.run_gates(bad, module, valid)
            okb, failedb = checks_verdict(ref.to_markdown(bad, module, org))
            good = bool(vb) and (not okb if visible else True)
            want = "web FAIL, checks FAIL" if visible else "web FAIL (checks blind)"
            rows.append((f"{name}: {dname}", want,
                         f"web {'FAIL' if vb else 'PASS'}, checks {'FAIL' if not okb else 'PASS'}", good))
            if not good:
                failures.append(f"{name}: {dname}")

    stale = [rel for rel, content in export_bundle.build().items()
             if not os.path.exists(os.path.join(BASE, "web", "bundle", rel))
             or open(os.path.join(BASE, "web", "bundle", rel), encoding="utf-8").read() != content]
    rows.append(("bundle freshness", "up to date", "up to date" if not stale else f"stale: {stale}", not stale))
    if stale:
        failures.append("bundle out of date: run python web/export_bundle.py")

    print("# Parity: web engine vs audit/checks.py\n")
    print("| Case | Expected | Got | ok? |\n|---|---|---|---|")
    for case, want, got, good in rows:
        print(f"| {case} | {want} | {got} | {'ok' if good else 'X'} |")
    print(f"\n**Parity: {'PASS' if not failures else 'FAIL'}**")
    for f in failures:
        print(f"- {f}")
    sys.exit(0 if not failures else 1)

if __name__ == "__main__":
    main()
