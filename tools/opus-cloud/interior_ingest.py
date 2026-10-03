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


def own_disagreements(cons, page, rows):
    """check_consistency lines naming `page` under an address the rows name (fn or any address in the text)."""
    named = set()
    for r in rows:
        named.add("%08X" % int(r["fn"], 16))
        named |= set(ADDR.findall(r["text"]))
    cur, n = None, 0
    for l in cons.splitlines():
        m = re.match(r"^   ([0-9A-F]{8})\s*$", l)
        if m:
            cur = m.group(1)
        elif l.startswith("      ") and page.replace("/", "\\") in l and cur in named:
            n += 1
    return n


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
    homing = rep.get("mode") == "homing"
    uc1 = rep.get("mode") == "uc1"
    ee = rep.get("mode") == "ee"
    member = rep.get("mode") == "member"
    if member:
        # family members (OPUS, 2026-10-03, mem_pack.py): unexplained members of a family the page declares
        targets = member_targets(page)
    elif ee:
        # engine_explained (OPUS, 2026-10-03): unexplained bodies >= 128 B the page cites only at the entry, F or family
        targets = ee_targets(page)
    elif uc1:
        # UC-1 game-code bodies (OPUS, 2026-10-03; FABLE ruling fable-uc1-gamecode-route-ruling-1003): the 59 F-unmet
        # UC-1 frontier bodies measured by uc1_credible.py; each row must carry the literal series-break phrase.
        targets = uc1_targets()
    elif homing:
        # F homing (OPUS, 2026-10-03, FABLE's split FABLE-REQ-OPUS-F-HOMING-SPLIT-1003): the body is in OPUS's
        # callee-host class and no page cites it; the host page must cite one of its callees, and the sentence must
        # name that callee (the row says why it lives on this page).
        targets = homing_targets()
        page_text = io.open(os.path.join(cl.DB, *page.split("/")), encoding="utf-8", errors="replace").read()
    else:
        targets = f_pack.entry_only_pages().get(page, set())
    ok, bad = [], []
    for r in rep.get("rows", []):
        fn = r.get("fn", "").upper()
        why = []
        f = int(fn, 16) if re.fullmatch(r"[0-9A-F]{8}", fn) else None
        if f is None or f not in targets:
            why.append("not an unexplained UC-1 game-code body" if uc1 else
                       "not a callee-host homing body (or already explained)" if homing
                       else "not an entry-only frontier function of the page")
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
            if uc1:
                # test 1 (FABLE's route ruling): the row states how the body is entered, so the calling functions,
                # call / jump sites, rip-reference sites and table slots uc1_credible.py measured are nameable too
                tokens = set(tokens) | uc1_entry_tokens().get(f, set())
            for h in set(ADDR.findall(t)):
                if h not in tokens:
                    why.append("names %s, not in its listing" % h)
                elif int(h, 16) != f and text_section_gap(int(h, 16)):
                    why.append("names %s, .text outside every function (text-gap)" % h)
            if uc1 and UC1_PHRASE not in t:
                why.append("uc1: the series-break phrase is missing")
            if homing and not any(h != fn and ("`%s`" % h) in page_text for h in set(ADDR.findall(t))):
                why.append("homing: the sentence names no callee the host page cites")
            r = {"fn": fn, "text": t, "anchors": [list(x) for x in anchors]}
        (bad if why else ok).append((r, why))
    rowed = {r["fn"] for r, _w in ok + bad}
    skipped = {s.get("fn", "").upper(): s.get("why", "") for s in rep.get("skipped", [])}
    # member mode (2026-10-03): a pack covers part of the page's families, so 'missing' is not measured against them all
    missing = [] if (homing or member) else sorted("%08X" % f for f in targets if "%08X" % f not in rowed and "%08X" % f not in skipped)
    rec = "opus-%s-%s-%s" % (slug[:40], "ee" if ee else "uc1" if uc1 else "homing" if homing else "cloudint", time.strftime("%m%d"))
    if member:
        # one record per pack part: the report name carries the family slug and part number
        part = os.path.splitext(os.path.basename(report))[0]
        rec = "opus-%s-%s" % ("member" if member else "ee" if ee else "", part[-56:].strip("-"))
    rdir = os.path.join(cl.DB, "_index", "candidates", rec)
    os.makedirs(rdir, exist_ok=True)
    shutil.copyfile(os.path.join(cl.HERE, "interior_applier.py"), os.path.join(rdir, "interior_applier.py"))
    cfg = {"page": page, "date": time.strftime("%Y-%m-%d"), "session": session or rep.get("session", ""),
           "report": os.path.basename(report), "rows": [r for r, _w in ok],
           "rejected": [{"fn": r["fn"], "why": w} for r, w in bad], "skipped": skipped, "missing": missing,
           "corrections": [], "mode": "member" if member else "ee" if ee else "uc1" if uc1 else "homing" if homing else "interior",
           "family": rep.get("family", "")}
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


UC1_PHRASE = "UC-1 body admitted to frontier 2026-09-28, explained by interior citation"


EB_JSON = os.path.normpath(os.path.join(cl.HERE, "..", "family", "entry_big.json"))


def member_targets(page):
    """Unexplained members of every family the page declares (mem_pack.py), measured now."""
    import mem_pack
    return {f for fs in mem_pack.unexplained_members(page).values() for f in fs}


def ee_targets(page, fresh=False):
    """The page's unexplained entry-only bodies of 128 B or more (entry_big.py; fresh=True re-measures)."""
    if fresh:
        subprocess.run([sys.executable, "-B", os.path.join(os.path.dirname(EB_JSON), "entry_big.py")],
                       capture_output=True, text=True)
    return {int(h, 16) for h in json.load(open(EB_JSON)).get(page, [])}


def uc1_entry_tokens():
    """body -> the 8-hex addresses of its entry evidence in uc1_credible.json (callers, sites, tables)."""
    out = {}
    for o in json.load(io.open(os.path.join(cl.HERE, "uc1_credible.json"), encoding="utf-8")):
        toks = set()
        for k in ("direct", "rip", "tables"):
            for v in o.get(k, []):
                toks |= set(ADDR.findall(v.upper()))
        out[int(o["body"], 16)] = toks
    return out


def uc1_targets():
    """The F-unmet UC-1 game-code bodies uc1_credible.py measured, minus any explained since."""
    sys.path.insert(0, cl.KIT)
    import check_dispositions as CD
    fs = {int(o["body"], 16) for o in json.load(io.open(os.path.join(cl.HERE, "uc1_credible.json"), encoding="utf-8"))}
    return fs - set(CD.evaluate(cl.DB, CD.load_functions())["explained_set"])


HOMING_TSV = os.path.join(cl.DB, "_index", "candidates", "fable-homing-stream-1003", "callee-host-bodies.tsv")


def homing_targets():
    """OPUS's callee-host class minus every body already explained (A/B/C) now."""
    sys.path.insert(0, cl.KIT)
    import check_dispositions as CD
    fs = {int(l.split("\t")[0], 16) for l in io.open(HOMING_TSV, encoding="utf-8")
          if l[:1] not in "#\n" and "\t" in l}
    sizes = CD.load_functions()
    return fs - set(CD.evaluate(cl.DB, sizes)["explained_set"])


def verdict_ok():
    for t in cl.tasks():
        if t.get("id") == "OPUS-REQ-AUDITSPEC-PFGATE-INTERIOR-1001":
            return str(t.get("status", "")).upper() == "DONE" and "REJECT" not in json.dumps(t).upper()
    return False


_MEMO = None          # apply-batch: tree-wide gate outputs computed once, after every page edit is in place


def run(cmd, cwd):
    key = (tuple(cmd), cwd)
    tree_wide = any(x.endswith(("check_consistency.py", "verify_doc_addresses.py", "check_links.py")) for x in cmd)
    if _MEMO is not None and tree_wide and key in _MEMO:
        return _MEMO[key]
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = r.stdout + r.stderr
    if _MEMO is not None and tree_wide:
        _MEMO[key] = out
    return out


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
        and ("ALREADY" in run(py, rdir) or "block differs" in run(py, rdir)) and "FAILS 0" in run(py, rdir)
    if g["verdict"] == "BLOCK" and not own_dirt:
        print("REFUSED: scope guard BLOCKs %s now: %s" % (page, "; ".join(g["reasons"]))); return 1
    o = run(py + ["--apply"], rdir)
    print(o.strip())
    if "FAILS 0" not in o:
        return 1
    io.open(os.path.join(rdir, "interior_applier.out"), "w", encoding="utf-8", newline="\n").write(run(py, rdir))
    stem = os.path.splitext(os.path.basename(page))[0]
    cons = run([sys.executable, "-B", "check_consistency.py"], cl.KIT)
    vda = run([sys.executable, "-B", "verify_doc_addresses.py", "--all"], cl.KIT)
    tree = ((lambda m: m.group(1) if m else "0")(re.search(r"(\d+) disagreement\(s\) to resolve", cons)),
            (lambda m: m.group(1) if m else "0")(re.search(r"(\d+) document\(s\) with \.text non-function", vda)))
    gates = {
        # Source side only: another file's broken link that names this page is not this page's (2026-10-02).
        "check_links": sum(1 for l in run([sys.executable, "-B", "check_links.py"], cl.KIT).splitlines()
                           if stem in l.split("->")[0] or rec in l.split("->")[0]),
        "self_contradiction": new_contradictions(page),
        # Page-scoped (2026-10-02, OPUS): the tree-wide totals also count other lanes' uncommitted hunks (a foreign
        # 5th disagreement or REVIEW blocked every record). The gate is that THIS page is in no disagreement and no
        # REVIEW; the tree totals are still reported in the README.
        # Narrowed again (2026-10-02, OPUS): only disagreements over an address this record's rows name - a stale
        # count in another lane's line on the same page (FABLE's 003A1DB0 "16 callers") is not this record's.
        "consistency": own_disagreements(cons, page, cfg["rows"]),
        "verify_doc_addresses": sum(1 for l in vda.splitlines() if l.startswith("REVIEW") and page.replace("/", "\\") in l),
        # Pass-22 neighbours preview (FABLE's condition 3, 2026-10-02): new UNACCOUNTED NEIGHBOUR hits this page gains
        # against HEAD. The full check_publish_neighbours.py still runs once per batch before publishing.
        "neighbours_new": sum(1 for l in run([sys.executable, "-B", os.path.join(cl.HERE, "..", "nb_page.py"), page],
                                             cl.KIT).splitlines() if l.startswith("      + ")),
    }
    import f_pack
    # uc1 (2026-10-03): SWE2-FRONTIER's gate change a46d39253 credits a UC-1 body cited inside its extent by a row
    # carrying the break phrase, so every applied uc1 row must now measure A like any other.
    still = (member_targets(page) if cfg.get("mode") == "member" else
             ee_targets(page, fresh=True) if cfg.get("mode") == "ee" else
             uc1_targets() if cfg.get("mode") == "uc1" else homing_targets() if cfg.get("mode") == "homing"
             else f_pack.entry_only_pages().get(page, set()))
    left = sorted("%08X" % int(r["fn"], 16) for r in cfg["rows"] if int(r["fn"], 16) in still)
    clean = gates["check_links"] == 0 and gates["self_contradiction"] == 0 and gates["consistency"] == 0 \
        and gates["verify_doc_addresses"] == 0 and gates["neighbours_new"] == 0 and not left
    print("GATES", gates, "still entry-only:", left or "none")
    if not clean:
        print("NOT QUEUED: a gate is not clean; fix and re-run apply (the page edit is in place).")
        return 1
    n, na = len(cfg["rows"]), sum(len(r["anchors"]) for r in cfg["rows"])
    corr = [("`%s`: %s" % (c.get("fn", "?"), c.get("why", ""))).replace("|", "/")
            if isinstance(c, dict) else str(c) for c in (cfg.get("corrections") or [])] or ["none needed"]
    readme = ["# Interior citations, cloud-drafted: %s's entry-cited functions (OPUS, %s)" % (os.path.basename(page), cfg["date"]), "",
              "The page named %d F-frontier functions only at their entry. %s drafted one sentence "
              "and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the "
              "private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every "
              "sentence against the bytes before applying." % (len(cfg["rows"]) + len(cfg["rejected"]) + len(cfg["skipped"]),
                                                            ("A local drafting agent (%s, no cloud credit)" % cfg["session"]) if str(cfg.get("session", "")).startswith("local")
                                                            else "A Claude Code cloud session (%s)" % (cfg.get("session") or "session id in rows.json")), "",
              "**Rows.** %d applied with %d anchors. Rejected by the mechanical check: %d. Skipped by the session: %d. Missing: %d." % (
                  n, na, len(cfg["rejected"]), len(cfg["skipped"]), len(cfg["missing"])), "",
              "**OPUS corrections on re-read.**", ""] + ["- %s" % c for c in corr] + ["",
              "**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes "
              "every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic "
              "([`.out`](interior_applier.out): FAILS 0; idempotent).", "",
              "**Effect and gates.** All %d rowed functions now measure A. On the page: `check_links` %d, "
              "`check_self_contradiction --db` %d, `check_consistency` %d disagreements naming this page (tree total %s), "
              "`verify_doc_addresses --all` %d REVIEW on this page (tree total %s)." % (
                  n, gates["check_links"], gates["self_contradiction"], gates["consistency"], tree[0],
                  gates["verify_doc_addresses"], tree[1]), "",
              "**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is "
              "OPUS's re-read. The session's agreement with OPUS is not independent review.", "",
              "## Review (OPUS)", "", "A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.", ""]
    if cfg.get("mode") == "member":
        readme[0] = "# Family members explained one by one: %d %s members on %s (OPUS, %s)" % (
            n, cfg.get("family", ""), os.path.basename(page), cfg["date"])
        readme[2] = ("The page declares the family `%s` (a classification family: ordinary functions grouped by module, not "
                     "template copies). No page explained these members. %s drafted one sentence and 1-5 interior anchors per "
                     "body from OPUS's pack (`mem_pack.py`); OPUS checked every row mechanically with `interior_ingest.py` "
                     "(member mode: the body is an unexplained member of a family this page declares) and re-read every "
                     "sentence against the bytes before applying." % (cfg.get("family", ""),
                         ("A local drafting agent (%s)" % cfg["session"]) if str(cfg.get("session", "")).startswith("local")
                         else "A session (%s)" % cfg.get("session", "")))
    if cfg.get("mode") == "homing":
        # F homing (2026-10-03): say what these rows are; the entry-cited wording above does not apply.
        readme[0] = "# Homed bodies: %s hosts %d functions no page cited (OPUS, %s, F homing)" % (os.path.basename(page), n, cfg["date"])
        readme[2] = ("OPUS's callee-host class (FABLE's split, `fable-homing-stream-1003/callee-host-bodies.tsv`): functions "
                     "no bearing page cited and whose callers are undocumented. Each is homed on this page because it calls a "
                     "function the page documents; the row names that callee. %s drafted one sentence and 1-5 interior "
                     "anchors per body from OPUS's homing pack (`cloud-input/f-homing/`). OPUS checked every row mechanically "
                     "with `interior_ingest.py` (homing mode: the body is in the class and the sentence names a callee the "
                     "page cites) and re-read every sentence against the bytes before applying." % (
                         ("A local drafting agent (%s)" % cfg["session"]) if str(cfg.get("session", "")).startswith("local")
                         else "A session (%s)" % cfg.get("session", "")))
    if cfg.get("mode") == "uc1":
        readme[0] = "# UC-1 game-code bodies explained by interior citation: %d rows on %s (OPUS, %s)" % (n, os.path.basename(page), cfg["date"])
        readme[2] = ("FABLE's route ruling (`fable-uc1-gamecode-route-ruling-1003`, R1 amendment): a game-code UC-1 frontier "
                     "body may be explained by an interior citation that passes tests 1-3. Test 1 (a credible start) is "
                     "measured by `uc1_credible.py` and stated at the head of each row (the entry site, or no reference "
                     "found and what the start follows). Test 2: %s drafted the sentences and anchors from OPUS's pack; "
                     "OPUS, the non-drafting identity, checked every row mechanically (`interior_ingest.py`, uc1 mode) and "
                     "re-read every sentence at the bytes. Test 3: every row carries the literal series-break phrase." % (
                         ("a local drafting agent (%s)" % cfg["session"]) if str(cfg.get("session", "")).startswith("local")
                         else "a session (%s)" % cfg.get("session", "")))
        i = next(k for k, l in enumerate(readme) if l.startswith("**Effect and gates.**"))
        readme[i] = ("**Effect and gates.** All %d rowed bodies now measure A through SWE2-FRONTIER's gate change "
                     "a46d39253 (`measure_a` credits a UC-1 body cited inside its extent by a row carrying the phrase). "
                     "On the page: `check_links` %d, `check_self_contradiction --db` %d, "
                     "`check_consistency` %d disagreements over addresses these rows name (tree total %s), "
                     "`verify_doc_addresses --all` %d REVIEW on this page (tree total %s)." % (
                         n, gates["check_links"], gates["self_contradiction"], gates["consistency"], tree[0],
                         gates["verify_doc_addresses"], tree[1]))
    if cfg.get("method"):
        # 2026-10-03: a record verified other than by OPUS re-reading every sentence states its own method
        readme[2] = cfg["method"]
    io.open(os.path.join(rdir, "README.md"), "w", encoding="utf-8", newline="\n").write("\n".join(readme))
    # 2026-10-03: a 48-character cut collided for sibling records (five member reviews refused "already exists" in
    # 1003M); a digest of the full record name keeps the ids apart
    import hashlib as _h
    tag = re.sub(r"[^A-Z0-9]+", "-", rec.upper())[:42].strip("-") + "-" + _h.sha1(rec.encode()).hexdigest()[:5].upper()
    title = "OPUS: interior citations (cloud-drafted, OPUS-verified) for %s - %d functions, %d anchors verified; all %d now A" % (
        os.path.basename(page), n, na, n)
    if cfg.get("session") == "opus-self":
        title = "OPUS: interior citations (OPUS-drafted) for %s - %d functions, %d anchors verified; all %d now A" % (
            os.path.basename(page), n, na, n)
    if cfg.get("mode") == "uc1":
        title = ("OPUS: %d UC-1 game-code bodies explained by interior citation on %s (FABLE's route ruling; drafted by a "
                 "non-OPUS agent, OPUS re-read, %d anchors)" % (n, os.path.basename(page), na))
    if cfg.get("mode") == "member":
        title = "OPUS: %d %s members explained one by one on %s (drafted locally, OPUS-verified, %d anchors)" % (
            n, cfg.get("family", ""), os.path.basename(page), na)
    if cfg.get("mode") == "homing":
        title = "OPUS: F homing - %d uncited bodies homed on %s by a documented callee (OPUS-verified, %d anchors); all %d now A" % (
            n, os.path.basename(page), na, n)
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
                          "question": ("At {commit}: %d UC-1 game-code rows on %s under FABLE's route ruling (fable-uc1-gamecode-route-ruling-1003, test 2 SPEC review). Drafted by a non-OPUS agent, re-read by OPUS. Please check at least 15 rows against the bytes, including each row's entry statement (test 1) and the series-break phrase (test 3)." % (n, page)) if cfg.get("mode") == "uc1" else
                                      "At {commit}: %d cloud-drafted, OPUS-verified interior citations on %s (all now A). Please spot-check at least 15 rows against the bytes; interior_applier.py re-verifies anchors and mnemonics, not sentences." % (n, page),
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
    if a and a[0] == "apply-batch":
        # 2026-10-03 (OPUS): every record's page edit first, then the tree-wide gates (check_links, check_consistency,
        # verify_doc_addresses) once for all of them; nb_page, self-contradiction and the queue spec stay per record.
        recs = [x for x in a[1:] if not x.startswith("--")]
        for rec in recs:
            rdir = os.path.join(cl.DB, "_index", "candidates", rec)
            o = run([sys.executable, "-B", "interior_applier.py", "--apply"], rdir)
            print("pre-apply %s: %s" % (rec, o.strip().splitlines()[-1] if o.strip() else "no output"))
        _MEMO = {}
        rc = 0
        for rec in recs:
            rc |= apply(rec, "--allow-before-verdict" in a)
        sys.exit(rc)
    print(__doc__); sys.exit(2)
