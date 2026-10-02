"""interior_ingest.py - turn a cloud session's F-interior report into a verified OPUS record (OPUS, 2026-10-01).

  check REPORT.json [--session URL]
      Mechanical checks, then a record folder _index/candidates/opus-<slug>-cloudint-<MMDD>/ (rows.json + applier) and a
      review sheet Tools/work/OPUS/cloud/review/<slug>.md (each row beside its annotated listing). Refuses a page the
      scope guard now BLOCKs. Per row it checks: the function is still an entry-only F-frontier function of that page;
      1-5 anchors, each an instruction boundary strictly inside the extent with the recorded mnemonic; no '|'; every
      8-hex address the sentence names appears in the function's annotated listing; no named address is .text outside
      every function extent (a text-gap citation would flag the page). Rejected rows are dropped from rows.json and
      listed. Functions neither rowed nor skipped are listed as MISSING.
  apply RECORD_DIR [--allow-before-verdict]
      Only after OPUS has re-read every row in the review sheet (edit rows.json; add "corrections": [...]). Refuses
      until SWE2-AUDIT-SPEC has ACCEPTed the interior method (board task OPUS-REQ-AUDITSPEC-PFGATE-INTERIOR-1001 DONE)
      unless --allow-before-verdict. Applies, writes the .out, runs the page gates (check_links, check_self_contradiction
      --db, check_consistency = 4 known, verify_doc_addresses 0) and the frontier measurement, writes README.md, the
      commit message and the publish-queue spec with the SWE2-AUDIT-SPEC review request."""
import io, json, os, re, shutil, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cloudlib as cl  # noqa: E402
import listing as L  # noqa: E402

REVIEW = os.path.join(cl.HERE, "review")
QUEUE = os.path.normpath(os.path.join(cl.HERE, "..", "queue"))
ADDR = re.compile(r"\b([0-9A-F]{8})\b")


def text_section_gap(va):
    """True when va is in .text but inside no listed function extent."""
    if L.section(va) != ".text":
        return False
    sz = L.sizes()
    import bisect
    keys = sorted(sz)
    i = bisect.bisect_right(keys, va) - 1
    return not (i >= 0 and keys[i] <= va < keys[i] + sz[keys[i]])


def check(report, session):
    rep = json.load(io.open(report, encoding="utf-8"))
    page = rep["page"]
    import f_pack
    slug = f_pack.slug_of(page)
    g = json.loads(subprocess.run([sys.executable, "-B", os.path.join(cl.HERE, "scope_guard.py"), page, "--json"],
                                  capture_output=True, text=True).stdout)[0]
    if g["verdict"] == "BLOCK":
        print("REFUSED: scope guard BLOCKs %s now: %s" % (page, "; ".join(g["reasons"])))
        return 1
    targets = f_pack.entry_only_pages().get(page, set())
    ok, bad = [], []
    for r in rep.get("rows", []):
        fn = r.get("fn", "").upper()
        why = []
        f = int(fn, 16) if re.fullmatch(r"[0-9A-F]{8}", fn) else None
        if f is None or f not in targets:
            why.append("not an entry-only frontier function of the page")
        else:
            lines, tokens = L.listing(f)
            bnd = L.boundaries(f)
            n = L.sizes()[f]
            anchors = [(a.upper(), m) for a, m in r.get("anchors", [])]
            if not 1 <= len(anchors) <= 5:
                why.append("%d anchors" % len(anchors))
            for a, m in anchors:
                av = int(a, 16)
                if not (f < av < f + n):
                    why.append("anchor %s outside the body" % a)
                elif bnd.get(av) != m:
                    why.append("anchor %s decodes to %s, not %s" % (a, bnd.get(av), m))
            t = r.get("text", "")
            if "|" in t:
                why.append("pipe in text")
            if len(t) > 1200:
                why.append("sentence over 1200 chars")
            for h in set(ADDR.findall(t)):
                if h not in tokens:
                    why.append("names %s, not in its listing" % h)
                elif int(h, 16) != f and text_section_gap(int(h, 16)):
                    why.append("names %s, .text outside every function (text-gap)" % h)
            r = {"fn": fn, "text": t, "anchors": [list(x) for x in anchors]}
        (bad if why else ok).append((r, why))
    rowed = {r["fn"] for r, _w in ok + bad}
    skipped = {s.get("fn", "").upper(): s.get("why", "") for s in rep.get("skipped", [])}
    missing = sorted("%08X" % f for f in targets if "%08X" % f not in rowed and "%08X" % f not in skipped)
    rec = "opus-%s-cloudint-%s" % (slug[:40], time.strftime("%m%d"))
    rdir = os.path.join(cl.DB, "_index", "candidates", rec)
    os.makedirs(rdir, exist_ok=True)
    shutil.copyfile(os.path.join(cl.HERE, "interior_applier.py"), os.path.join(rdir, "interior_applier.py"))
    cfg = {"page": page, "date": time.strftime("%Y-%m-%d"), "session": session or rep.get("session", ""),
           "report": os.path.basename(report), "rows": [r for r, _w in ok],
           "rejected": [{"fn": r["fn"], "why": w} for r, w in bad], "skipped": skipped, "missing": missing,
           "corrections": []}
    json.dump(cfg, io.open(os.path.join(rdir, "rows.json"), "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
    os.makedirs(REVIEW, exist_ok=True)
    out = ["# Review: %s (%s)" % (page, rec), "", "Re-read every row against its listing; edit rows.json; record each change "
           "in rows.json 'corrections'. Then: interior_ingest.py apply %s" % rec, ""]
    for r, w in ok + bad:
        f = int(r["fn"], 16)
        lines, _t = L.listing(f) if L.sizes().get(f) else ([], set())
        out += ["## %s %s" % (r["fn"], "REJECTED: " + "; ".join(w) if w else ""), "", r.get("text", ""), "",
                "anchors: " + ", ".join("%s %s" % tuple(a) for a in r.get("anchors", [])), "", "```"] + lines + ["```", ""]
    io.open(os.path.join(REVIEW, slug + ".md"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("RECORD %s\nrows ok %d, rejected %d, skipped %d, missing %d\nreview sheet: %s" % (
        rec, len(ok), len(bad), len(skipped), len(missing), os.path.join(REVIEW, slug + ".md")))
    for r, w in bad:
        print("  REJECTED %s: %s" % (r["fn"], "; ".join(w)))
    for s, why in skipped.items():
        print("  SKIPPED %s: %s" % (s, why[:120]))
    if missing:
        print("  MISSING " + " ".join(missing))
    return 0


def verdict_ok():
    for t in cl.tasks():
        if t.get("id") == "OPUS-REQ-AUDITSPEC-PFGATE-INTERIOR-1001":
            return str(t.get("status", "")).upper() == "DONE" and "REJECT" not in json.dumps(t).upper()
    return False


def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout + r.stderr


def new_contradictions(page):
    """check_self_contradiction hits on the working page minus those already on its HEAD version (2026-10-02: a
    heuristic hit already committed on CONTRACT-auto-status-rebuild.md held an unrelated interior append)."""
    import tempfile
    rel = page.replace("\\", "/")
    counts = []
    with tempfile.TemporaryDirectory() as td:
        for tag in ("h", "w"):
            dst = os.path.join(td, tag, *rel.split("/"))
            os.makedirs(os.path.dirname(dst))
            if tag == "h":
                blob = subprocess.run(["git", "show", "HEAD:Database/FFXII TZA/" + rel], cwd=cl.DBROOT,
                                      capture_output=True).stdout
                open(dst, "wb").write(blob)
            else:
                shutil.copyfile(os.path.join(cl.DB, *rel.split("/")), dst)
            o = run([sys.executable, "-B", "check_self_contradiction.py", "--db", os.path.join(td, tag)], cl.KIT)
            counts.append(sum(1 for l in o.splitlines() if re.match(r"\s+line \d+ says", l)))
    return max(0, counts[1] - counts[0])


def apply(rec, allow):
    rdir = os.path.join(cl.DB, "_index", "candidates", rec)
    cfg = json.load(io.open(os.path.join(rdir, "rows.json"), encoding="utf-8"))
    if not (verdict_ok() or allow):
        print("REFUSED: the interior method has no SWE2-AUDIT-SPEC ACCEPT yet (OPUS-REQ-AUDITSPEC-PFGATE-INTERIOR-1001)."
              " The record stays staged; re-run after the verdict, or pass --allow-before-verdict deliberately.")
        return 1
    page = cfg["page"]
    g = json.loads(subprocess.run([sys.executable, "-B", os.path.join(cl.HERE, "scope_guard.py"), page, "--json"],
                                  capture_output=True, text=True).stdout)[0]
    py = [sys.executable, "-B", "interior_applier.py"]
    # A re-run after a gate fix: the page is dirty only because this record's own edit is in place (2026-10-02).
    own_dirt = g["verdict"] == "BLOCK" and g["reasons"] == ["dirty in the working tree"] \
        and "ALREADY" in run(py, rdir) and "FAILS 0" in run(py, rdir)
    if g["verdict"] == "BLOCK" and not own_dirt:
        print("REFUSED: scope guard BLOCKs %s now: %s" % (page, "; ".join(g["reasons"]))); return 1
    o = run(py + ["--apply"], rdir)
    print(o.strip())
    if "FAILS 0" not in o:
        return 1
    io.open(os.path.join(rdir, "interior_applier.out"), "w", encoding="utf-8", newline="\n").write(run(py, rdir))
    stem = os.path.splitext(os.path.basename(page))[0]
    gates = {
        # Source side only: another file's broken link that names this page is not this page's (2026-10-02).
        "check_links": sum(1 for l in run([sys.executable, "-B", "check_links.py"], cl.KIT).splitlines()
                           if stem in l.split("->")[0] or rec in l.split("->")[0]),
        "self_contradiction": new_contradictions(page),
        "consistency": run([sys.executable, "-B", "check_consistency.py"], cl.KIT).count("disagreement(s) to resolve") and
        re.search(r"(\d+) disagreement\(s\) to resolve", run([sys.executable, "-B", "check_consistency.py"], cl.KIT)).group(1),
        # The review line, not the first "N document(s)" total (2026-10-02 fix: the total, 491, was read as a failure).
        "verify_doc_addresses": (lambda m: m.group(1) if m else "0")(re.search(
            r"(\d+) document\(s\) with \.text non-function", run([sys.executable, "-B", "verify_doc_addresses.py", "--all"], cl.KIT))),
        # Pass-22 neighbours preview (FABLE's condition 3, 2026-10-02): new UNACCOUNTED NEIGHBOUR hits this page gains
        # against HEAD. The full check_publish_neighbours.py still runs once per batch before publishing.
        "neighbours_new": sum(1 for l in run([sys.executable, "-B", os.path.join(cl.HERE, "..", "nb_page.py"), page],
                                             cl.KIT).splitlines() if l.startswith("      + ")),
    }
    import f_pack
    still = f_pack.entry_only_pages().get(page, set())
    left = sorted("%08X" % int(r["fn"], 16) for r in cfg["rows"] if int(r["fn"], 16) in still)
    clean = gates["check_links"] == 0 and gates["self_contradiction"] == 0 and str(gates["consistency"]) == "4" \
        and gates["verify_doc_addresses"] == "0" and gates["neighbours_new"] == 0 and not left
    print("GATES", gates, "still entry-only:", left or "none")
    if not clean:
        print("NOT QUEUED: a gate is not clean; fix and re-run apply (the page edit is in place).")
        return 1
    n, na = len(cfg["rows"]), sum(len(r["anchors"]) for r in cfg["rows"])
    corr = [("`%s`: %s" % (c.get("fn", "?"), c.get("why", ""))).replace("|", "/")
            if isinstance(c, dict) else str(c) for c in (cfg.get("corrections") or [])] or ["none needed"]
    readme = ["# Interior citations, cloud-drafted: %s's entry-cited functions (OPUS, %s)" % (os.path.basename(page), cfg["date"]), "",
              "The page named %d F-frontier functions only at their entry. A Claude Code cloud session (%s) drafted one sentence "
              "and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the "
              "private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every "
              "sentence against the bytes before applying." % (len(cfg["rows"]) + len(cfg["rejected"]) + len(cfg["skipped"]),
                                                            cfg.get("session") or "session id in rows.json"), "",
              "**Rows.** %d applied with %d anchors. Rejected by the mechanical check: %d. Skipped by the session: %d. Missing: %d." % (
                  n, na, len(cfg["rejected"]), len(cfg["skipped"]), len(cfg["missing"])), "",
              "**OPUS corrections on re-read.**", ""] + ["- %s" % c for c in corr] + ["",
              "**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes "
              "every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic "
              "([`.out`](interior_applier.out): FAILS 0; idempotent).", "",
              "**Effect and gates.** All %d rowed functions now measure A. On the page: `check_links` %d, "
              "`check_self_contradiction --db` %d, `check_consistency` %s (the pre-existing four), `verify_doc_addresses "
              "--all` %s documents to confirm." % (n, gates["check_links"], gates["self_contradiction"], gates["consistency"],
                                                    gates["verify_doc_addresses"]), "",
              "**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is "
              "OPUS's re-read. The session's agreement with OPUS is not independent review.", "",
              "## Review (OPUS)", "", "A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.", ""]
    io.open(os.path.join(rdir, "README.md"), "w", encoding="utf-8", newline="\n").write("\n".join(readme))
    tag = re.sub(r"[^A-Z0-9]+", "-", rec.upper())[:48].strip("-")
    title = "OPUS: interior citations (cloud-drafted, OPUS-verified) for %s - %d functions, %d anchors verified; all %d now A" % (
        os.path.basename(page), n, na, n)
    # A short digest keeps two slugs with the same tail apart (2026-10-02: contract-auto-status-rebuild overwrote
    # the-auto-status-rebuild's queued spec and message).
    import hashlib
    name = "99zzzzzzzzzzzx_%s%s" % (rec[-24:].replace("-", ""), hashlib.sha1(rec.encode()).hexdigest()[:4])
    msgf = "msg_%s.txt" % name
    io.open(os.path.join(cl.HERE, "..", msgf), "w", encoding="utf-8", newline="\n").write(
        title + "\n\nRecord: _index/candidates/%s/ (rows drafted by a cloud session, checked by interior_ingest.py, every "
        "sentence re-read by OPUS). Gates clean. Review requested from SWE2-AUDIT-SPEC.\n" % rec)
    R = "Database/FFXII TZA/_index/candidates/%s/" % rec
    spec = {"id": "OPUS-PUB-%s" % tag, "title": title, "msg": "Tools/work/OPUS/" + msgf,
            "gate": "(cd 'FFXII TZA/_index/candidates/%s' && python -B interior_applier.py | tail -1 | grep -qx 'FAILS 0') && echo CINT-OK || echo GATE-FAIL cint" % rec,
            "paths": ["Database/FFXII TZA/" + page, R + "README.md", R + "rows.json", R + "interior_applier.py", R + "interior_applier.out"],
            "requests": [{"id": "OPUS-REQ-AUDITSPEC-%s" % tag, "to": "SWE2-AUDIT-SPEC", "target": "_index/candidates/%s/" % rec,
                          "scope": "review", "priority": "P2",
                          "question": "At {commit}: %d cloud-drafted, OPUS-verified interior citations on %s (all now A). Please spot-check at least 15 rows against the bytes; interior_applier.py re-verifies anchors and mnemonics, not sentences." % (n, page),
                          "blocked": "acceptance of %d F dispositions" % n, "why": "cloud-drafted rows need the same non-author check",
                          "completion": "a review record with a verdict"}]}
    json.dump(spec, io.open(os.path.join(QUEUE, name + ".json"), "w", encoding="utf-8"), indent=1)
    print("QUEUED", name, "->", spec["id"])
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "check":
        sess = a[a.index("--session") + 1] if "--session" in a else ""
        sys.exit(check(a[1], sess))
    if a and a[0] == "apply":
        sys.exit(apply(a[1], "--allow-before-verdict" in a))
    print(__doc__); sys.exit(2)
