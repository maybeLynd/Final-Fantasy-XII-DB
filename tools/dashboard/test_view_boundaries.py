"""test_view_boundaries.py - the two view boundaries ASTRA rejected in eae0ed3c7, on the real invocation paths (OPUS, 2026-10-01).

Review: OPUS-REQ-ASTRA-VERIFY-DASHBOARD-VIEWS-0929-R (REJECT; _experiments/evidence/dashboard-view-boundary-review/).

Deltas - build_views.annotate_deltas on prior/current view fixtures written to a scratch generation:
  D1 count 10 -> 15: count +5, rel +50 % (control)
  D2 ratio 10/100 -> 15/200: "scope changed", dnum +5, dden +100, both bases kept (control)
  D3 a count whose scope changed: no numeric count (control)
  D4 ratio 0/0 -> count 5/null: "N/A - basis changed", no count/rel/pp, the prior denominator stays 0 (was: count +5, 0 -> null)
  D5 ratio 1/2 -> 0/0: the current denominator stays 0, no division by zero (was: rewritten to null)
  D6 ratio 0/0 -> 0/0: pp 0.0 with both zero denominators kept (was: both erased)
  D7 count 5/null -> ratio 3/10: "N/A - basis changed", no numeric change
VBF - the actual vbf_index.py CLI into build_views.v_vbf, on a disclosed two-entry synthetic header (ASTRA's fixture shape):
  V1 matching listing: 2 files, 300 bytes, drift 0, OK (control)
  V2 drifted listing: drift 2, PARTIAL (control)
  V3 missing archive and V4 corrupt archive: exit 1, FAILED, no measures (controls)
  V5 a supplied listing that does not exist: inventory kept (2 files), NO listing-drift measure, PARTIAL, the limits and a
     row say "Listing comparison UNMEASURED: listing not found" (was: drift 0 shown as measured, status OK)
  V6 no listing argument, V7 a listing with no '<size> <name>' rows: UNMEASURED with the reason
  V8 a capture whose vs_listing is malformed: UNMEASURED, never a drift
Every view must pass server.check_view.
Discriminator: D4-D6 and V5 run again against the rejected eae0ed3c7 source (from git, AST-extracted like ASTRA's probe)
and must FAIL there - the checks see the defect, so their PASS here is the repair.
Prints PASS/FAIL per check and FAILS n; exit 1 on any failure.
"""
import ast, collections, json, os, shutil, struct, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "analysis-kit", "gfz-scripts"))
import build_views as BV  # noqa: E402
import server as S  # noqa: E402
REJECTED = "eae0ed3c7"
fails = 0


def check(tag, ok, text=""):
    global fails
    print("%s %s %s" % ("PASS" if ok else "FAIL", tag, str(text)[:400]))
    fails += 0 if ok else 1


def view(measures, definition="v1"):
    return {"view": "fixture", "title": "fixture", "status": "OK", "definition": definition,
            "source": {"identity": "fixture", "as_of": "t", "instrument": "fixture", "limits": "fixture"},
            "measures": [BV.M(i, i, n, d, sc, "fixture", "t", "fixture") for i, n, d, sc in measures]}


PAIRS = {  # id: (prior (n, d, scope), current (n, d, scope))
    "count": ((10, None, "s"), (15, None, "s")),
    "ratio-moved": ((10, 100, "s"), (15, 200, "s")),
    "count-scope": ((10, None, "s"), (15, None, "s2")),
    "zero-to-count": ((0, 0, "s"), (5, None, "s")),
    "ratio-to-zero": ((1, 2, "s"), (0, 0, "s")),
    "zero-zero": ((0, 0, "s"), (0, 0, "s")),
    "count-to-ratio": ((5, None, "s"), (3, 10, "s")),
}


def run_deltas(annotate, T):
    pd = os.path.join(T, "prior"); os.makedirs(os.path.join(pd, "outputs"), exist_ok=True)
    pv = view([(k, *v[0]) for k, v in PAIRS.items()])
    json.dump(pv, open(os.path.join(pd, "outputs", "view-fixture.json"), "w", encoding="utf-8"))
    cur = {"fixture": view([(k, *v[1]) for k, v in PAIRS.items()])}
    annotate(cur, pd, {"generation": "g-prior"})
    bad = [S.check_view(v) for v in (pv, cur["fixture"])]
    return {m["id"]: m.get("delta") or {} for m in cur["fixture"]["measures"]}, bad


NUMERIC = ("count", "rel", "pp", "dnum", "dden")


def delta_checks(d):
    """tag -> ok, for D4-D6 (the discriminating ones) and D1-D3, D7."""
    z, rz, zz, cr = d["zero-to-count"], d["ratio-to-zero"], d["zero-zero"], d["count-to-ratio"]
    return {
        "D1": d["count"].get("count") == 5 and d["count"].get("rel") == 50.0,
        "D2": d["ratio-moved"].get("na") == "scope changed" and d["ratio-moved"].get("dnum") == 5 and d["ratio-moved"].get("dden") == 100
              and d["ratio-moved"]["old"] == {"numerator": 10, "denominator": 100},
        "D3": "count" not in d["count-scope"] and "rel" not in d["count-scope"],
        "D4": z.get("na") == "N/A - basis changed" and not any(k in z for k in NUMERIC) and (z.get("old") or {}).get("denominator") == 0
              and (z.get("new") or {}).get("denominator") is None,
        "D5": (rz.get("new") or {}).get("denominator") == 0 and (rz.get("old") or {}).get("denominator") == 2 and rz.get("pp") == 50.0,
        "D6": zz.get("pp") == 0.0 and (zz.get("old") or {}).get("denominator") == 0 and (zz.get("new") or {}).get("denominator") == 0,
        "D7": cr.get("na") == "N/A - basis changed" and not any(k in cr for k in NUMERIC),
    }


def write_fixture(W):
    names = b"folder/a.dat\0folder/b.src\0"
    size = 16 + 32 + 64 + 4 + len(names)
    h = struct.pack("<4sIQ", b"SRYK", size, 2) + bytes(32)
    h += struct.pack("<IIQQQ", 0, 0, 100, 0, 0) + struct.pack("<IIQQQ", 0, 0, 200, 0, 13)
    h += struct.pack("<I", 4 + len(names)) + names
    f = {"archive": os.path.join(W, "positive.vbf"), "corrupt": os.path.join(W, "corrupt.vbf"),
         "listing": os.path.join(W, "listing.txt"), "drift": os.path.join(W, "drift.txt"), "empty": os.path.join(W, "empty.txt"),
         "facts": os.path.join(W, "facts.json")}
    open(f["archive"], "wb").write(h); open(f["corrupt"], "wb").write(b"WRNG" + h[4:])
    open(f["listing"], "w", encoding="utf-8").write("100 folder/a.dat\n200 folder/b.src\n")
    open(f["drift"], "w", encoding="utf-8").write("100 folder/a.dat\n201 folder/b.src\n2 folder/c.dat\n")
    open(f["empty"], "w", encoding="utf-8").write("not a listing\n")
    json.dump({"facts": [], "gaps": {}, "failed": {}}, open(f["facts"], "w", encoding="utf-8"))
    return f


def capture_case(W, name, archive, listing, cli):
    out = os.path.join(W, name + ".json")
    json.dump({"entries": [["stale/file.dat", 999]], "archive_index": {"stale": True}}, open(out, "w", encoding="utf-8"))
    argv = [sys.executable, "-B", cli, "--archive", archive, "--out", out] + (["--listing", listing] if listing else [])
    r = subprocess.run(argv, capture_output=True, text=True, timeout=60)
    return r.returncode, out


def vbf_view(v_vbf, out, facts):
    return v_vbf({"vbf_index": out, "requirement_facts": facts}, "fixture")


def ms(v):
    return {m["id"]: m for m in v.get("measures", [])}


def v5_ok(rc, v):
    m = ms(v)
    return rc == 0 and m.get("files", {}).get("numerator") == 2 and "listing-drift" not in m and v["status"] == "PARTIAL" \
        and "Listing comparison UNMEASURED: listing not found" in v["source"]["limits"] and not S.check_view(v)


T = tempfile.mkdtemp(prefix="viewbound_")
try:
    # ---- deltas, current code
    d, bad = run_deltas(BV.annotate_deltas, os.path.join(T, "cur"))
    check("fixtures valid", bad == [None, None], bad)
    res = delta_checks(d)
    for tag in sorted(res):
        check(tag, res[tag], {k: d[k] for k in PAIRS})
    # ---- VBF chain, current code
    W = os.path.join(T, "vbf"); os.makedirs(W)
    fx = write_fixture(W)
    CLI = os.path.join(HERE, "vbf_index.py")
    rc, out = capture_case(W, "positive", fx["archive"], fx["listing"], CLI); v1 = vbf_view(BV.v_vbf, out, fx["facts"])
    check("V1", rc == 0 and ms(v1)["files"]["numerator"] == 2 and ms(v1)["bytes"]["numerator"] == 300 and ms(v1)["listing-drift"]["numerator"] == 0
          and v1["status"] == "OK" and not S.check_view(v1), (rc, v1["status"]))
    rc, out = capture_case(W, "drift", fx["archive"], fx["drift"], CLI); v2 = vbf_view(BV.v_vbf, out, fx["facts"])
    check("V2", rc == 0 and ms(v2)["listing-drift"]["numerator"] == 2 and v2["status"] == "PARTIAL" and not S.check_view(v2), (rc, v2["status"]))
    for tag, arc in (("V3", os.path.join(W, "missing.vbf")), ("V4", fx["corrupt"])):
        rc, out = capture_case(W, tag, arc, fx["listing"], CLI); vx = vbf_view(BV.v_vbf, out, fx["facts"])
        cap = json.load(open(out, encoding="utf-8"))
        check(tag, rc == 1 and vx["status"] == "FAILED" and vx["measures"] == [] and "entries" not in cap and not S.check_view(vx), (rc, vx["status"]))
    rc, out5 = capture_case(W, "missing-listing", fx["archive"], os.path.join(W, "missing-listing.txt"), CLI)
    v5 = vbf_view(BV.v_vbf, out5, fx["facts"])
    check("V5", v5_ok(rc, v5), (rc, v5["status"], sorted(ms(v5)), v5["source"]["limits"][-120:]))
    for tag, lst, why in (("V6", None, "no listing supplied"), ("V7", fx["empty"], "has no '<size> <name>' rows")):
        rc, out = capture_case(W, tag, fx["archive"], lst, CLI); vx = vbf_view(BV.v_vbf, out, fx["facts"])
        check(tag, rc == 0 and "listing-drift" not in ms(vx) and vx["status"] == "PARTIAL" and why in vx["source"]["limits"]
              and not S.check_view(vx), (rc, vx["status"], vx["source"]["limits"][-100:]))
    cap = json.load(open(out5, encoding="utf-8")); cap.pop("vs_listing_failed", None); cap["vs_listing"] = {"listing_path": "x"}
    p8 = os.path.join(W, "malformed.json"); json.dump(cap, open(p8, "w", encoding="utf-8"))
    v8 = vbf_view(BV.v_vbf, p8, fx["facts"])
    check("V8", "listing-drift" not in ms(v8) and v8["status"] == "PARTIAL" and "malformed listing comparison" in v8["source"]["limits"], v8["status"])
    # ---- discriminator: the rejected eae0ed3c7 source must fail D4-D6 and V5
    root = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
    src = subprocess.run(["git", "show", REJECTED + ":Database/Tools/dashboard/build_views.py"], cwd=root, capture_output=True)
    cli_old = subprocess.run(["git", "show", REJECTED + ":Database/Tools/dashboard/vbf_index.py"], cwd=root, capture_output=True)
    if src.returncode or not src.stdout or cli_old.returncode or not cli_old.stdout:
        check("discriminator", False, "cannot read the rejected source from git")
    else:
        tree = ast.parse(src.stdout)
        env = {"json": json, "os": os, "collections": collections}
        exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {"M", "annotate_deltas", "v_vbf"}],
                                type_ignores=[]), "<rejected eae0ed3c7>", "exec"), env)
        od, _ = run_deltas(env["annotate_deltas"], os.path.join(T, "old"))
        ores = delta_checks(od)
        oldcli = os.path.join(T, "vbf_index_old.py"); open(oldcli, "wb").write(cli_old.stdout)
        rc, o5 = capture_case(W, "missing-listing-old", fx["archive"], os.path.join(W, "missing-listing.txt"), oldcli)
        ov5 = vbf_view(env["v_vbf"], o5, fx["facts"])
        seen = {"D4": not ores["D4"], "D5": not ores["D5"], "D6": not ores["D6"], "V5": not v5_ok(rc, ov5),
                "controls hold there": ores["D1"] and ores["D3"]}
        check("discriminator", all(seen.values()), seen)
finally:
    shutil.rmtree(T, ignore_errors=True)
print("FAILS", fails)
sys.exit(1 if fails else 0)
