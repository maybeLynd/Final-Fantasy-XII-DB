"""build_views.py - build one dashboard generation from declared inputs (OPUS, 2026-09-29; migration M3).

    python build_views.py [--root <store>]        (default store: Database/Tools/work/dashboard)

Deterministic code, no model call. Each view is `view-<name>.json` per VIEW-SCHEMA.md, written into one
`gfz-scripts/generation.py` generation. It is committed only when the declared inputs did not move during the build.

COHERENCE: every adapter reads the input SNAPSHOT captured by generation.Build (build.dir/inputs/<name>), never the live
file. Two instruments are run once, before begin(), and their outputs become declared inputs with their capture time:
`goal_gate.py --json` and `check_questions.py`. So each number shown is bound to exact bytes and an instrument time.

VOLATILE: the board and the watchdog state change every few seconds and are read only from their snapshots, so they
are declared volatile (drift, not a refused commit); every other input is strict, with up to three attempts.

HONESTY: an adapter that raises emits a FAILED view with the reason; it is never dropped or zeroed. A dimension no adapter
measures yet stays UNMEASURED (the server shows absent required views that way). Adapters are first-pass (OPUS); DATA
extends them under the M3 split.
"""
import argparse, collections, datetime, glob, hashlib, json, os, re, subprocess, sys, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE); DBROOT = os.path.dirname(TOOLS); DB = os.path.join(DBROOT, "FFXII TZA")
GS = os.path.join(TOOLS, "analysis-kit", "gfz-scripts")
sys.path.insert(0, GS)
import generation as G  # noqa: E402

NOW = lambda: datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha12(p):
    return G.sha256_file(p)[:12]


def M(i, label, num, den, scope, instrument, as_of, limits):
    return {"id": i, "label": label, "numerator": num, "denominator": den, "scope": scope, "instrument": instrument,
            "as_of": as_of, "limits": limits}


# ------------------------------------------------------------------ adapters (read snapshots only)
def v_overview(inp, t):
    gg = json.load(open(inp["goal_gate"], encoding="utf-8"))
    q = open(inp["check_questions"], encoding="utf-8").read()
    cnt = {k: int(re.search(r"^\s+%s\s+(\d+)" % k, q, re.M).group(1)) for k in ("ANSWERED", "PARTIAL", "OPEN", "BLOCKED")}
    rows = int(re.search(r"^\s+rows:\s+(\d+)", q, re.M).group(1))
    inst = "goal_gate.py --json / check_questions.py, captured %s" % t
    detail = [d.split(":", 1) for d in gg["detail"]]
    _, board_tasks = _board(inp)
    pkgs = package_checks(inp["_pkgdir"], {x["id"]: x for x in board_tasks})
    flags = collections.Counter(f for p in pkgs for it in p["items"] for f in it["flags"]) + collections.Counter(f for p in pkgs for f in p["flags"])
    return {"view": "overview", "title": "Overview - where the whole database stands", "status": "OK",
            "source": {"identity": "goal gate %s; register rows %d" % (gg["verdict"], rows), "as_of": t, "instrument": inst,
                       "limits": "DB_GOAL is the gate's verdict, not this dashboard's; a package stage is as recorded in its file"},
            "measures": _register_measures(inp, cnt, rows, inst, t) + [
                         M("pkg-false-complete", "package items claiming completion while a linked board task is open (A02)", flags.get("FALSE-COMPLETE", 0),
                           sum(len(p["items"]) for p in pkgs), "completion-packages/*.md x board", "package_checks", t, "a consistency check, not a derivation of acceptance"),
                         M("pkg-link-done", "package items whose linked board tasks are all DONE but whose stage has not moved", flags.get("LINK-DONE", 0),
                           sum(len(p["items"]) for p in pkgs), "completion-packages/*.md x board", "package_checks", t, "likely stale item stages; FABLE updates them"),
                         M("pkg-stage-mismatch", "packages whose recorded stage is not their earliest item's stage", flags.get("STAGE-MISMATCH", 0),
                           len(pkgs), "completion-packages/*.md", "package_checks", t, "FABLE's rule: the package stage is the earliest non-adjacent item stage")],
            "rows": {"columns": ["state", "value"], "data":
                     # V5 (FABLE DASHBOARD-MEANINGS 4c): three separate states, never merged
                     [["1. migration acceptance (M0-M5)", "NOT ACCEPTED - no migration acceptance receipt exists; matrix items are NOT_RUN until a "
                       "non-author receipt names its commit (see _index/workflow/IMPLEMENTATION-MAP.md delivery links)"],
                      ["2. package acceptance", "%d of %d completion packages accepted-and-incorporated (as recorded; stages: %s)"
                       % (sum(1 for p in pkgs if p["stage"] == "accepted-and-incorporated"), len(pkgs), ", ".join("%s %s" % (p["id"], p["stage"]) for p in pkgs))],
                      ["3. whole database (goal_gate)", "%s - %s" % (gg["verdict"], gg.get("remaining", ""))]] +
                     [["goal gate: " + a.strip(), b.strip()] for a, b in detail] + [["goal gate: next", gg.get("next", "")]]},
            "tree": [{"id": "packages", "label": "completion packages - recorded stages, checked against their items and the board", "children":
                      [{"id": p["id"], "label": p["id"], "state": p["stage"], "counts": dict({"items": len(p["items"])}, **{f: "yes" for f in p["flags"]}),
                        "children": [{"id": p["id"] + ":" + it["item"], "label": "%s %s" % (it["item"], it["kind"]), "state": it["stage"],
                                      "counts": dict({"owner": it["owner"], "reviewer": it["reviewer"], "board links": ", ".join(it["links"]) or "none"},
                                                     **{f: "yes" for f in it["flags"]})} for it in p["items"]]} for p in pkgs]}]}


def _register_measures(inp, cnt, rows, inst, t):
    """V1-V3 (FABLE-REQ-OPUS-DASHBOARD-VIEW-MEANINGS-V1-V5): the register split the way DATA's reporter classifies it, read
    from its snapshot (the one source of these counts) with the reporter's own freshness verdict. Answers and dispositions
    are separate; withdrawn rows, transfers and page-local obligations are visible; what nothing measures is UNMEASURED."""
    ps = json.load(open(inp["progress_snapshot"], encoding="utf-8"))
    chk = open(inp["progress_check"], encoding="utf-8").read().strip().splitlines()
    fresh = chk[-1] if chk else "no check output"
    src = "progress_report.py snapshot %s (%s); %s" % (ps.get("commit_id"), ps.get("generated_at_utc"), fresh)
    L1 = ps["levels"]["L1_modding_grade"]; oq = L1["open_questions"]; dp = L1["open_questions_dispositions"]
    scored = sum(v for v in oq.values() if isinstance(v, int))
    wd = dp.get("withdrawn_by_lead", {}); pb = ps.get("page_boxes", {}); tr = ps.get("transfers", {})
    lim = "reporter's L1 scoring (%d rows scored); counted once each; %s" % (scored, "STALE per the reporter's own check" if "STALE" in fresh else "reporter CURRENT")
    return [M("register-answered", "register rows ANSWERED (accepted answers)", dp.get("accepted_answers", 0), scored, "OPEN-QUESTIONS (reporter)", src, t, lim),
            M("register-dispositioned", "rows DISPOSITIONED: closed for the gate, UNANSWERED in fact (NAS %d, OEB %d)"
              % (dp.get("no_admissible_source", 0), dp.get("out_of_evidence_boundary", 0)),
              dp.get("no_admissible_source", 0) + dp.get("out_of_evidence_boundary", 0), scored, "OPEN-QUESTIONS (reporter)", src, t, lim),
            M("register-withdrawn", "rows WITHDRAWN / superseded / not a question (%s)" % ", ".join("%s %d" % kv for kv in sorted(wd.items())),
              sum(wd.values()), scored, "OPEN-QUESTIONS (reporter)", src, t, "not learned; not counted as answers"),
            M("register-partial", "rows PARTIAL (block the gate)", oq.get("PARTIAL", cnt["PARTIAL"]), scored, "OPEN-QUESTIONS (reporter)", src, t,
              "residue named on each row; check_questions (captured) agrees: PARTIAL %d of %d rows" % (cnt["PARTIAL"], rows)),
            M("register-open", "rows OPEN or BLOCKED", oq.get("OPEN", 0) + oq.get("BLOCKED", 0), scored, "OPEN-QUESTIONS (reporter)", src, t, lim),
            M("register-other", "rows in no class above (other status words: %s)" % ", ".join("%s %d" % (k, v) for k, v in sorted(oq.items())
                                                                                      if k not in ("ANSWERED", "WITHDRAWN", "PARTIAL", "OPEN", "BLOCKED") and isinstance(v, int)),
              scored - dp.get("accepted_answers", 0) - dp.get("no_admissible_source", 0) - dp.get("out_of_evidence_boundary", 0) - sum(wd.values())
              - oq.get("PARTIAL", 0) - oq.get("OPEN", 0) - oq.get("BLOCKED", 0), scored, "OPEN-QUESTIONS (reporter)", src, t,
              "the remainder, shown so nothing is silently dropped; each needs a class"),
            M("page-local", "page-local obligations: unticked page boxes with no register id (%d on untracked pages)" % pb.get("no_id_untracked", 0),
              pb.get("no_id", 0), None, "page checklists (check_questions.read_boxes via the reporter)", src, t,
              "required unless dispositioned; %d further unticked boxes belong to live register rows" % pb.get("open_id", 0)),
            M("transfers", "obligations transferred with their residue (untracked %d)" % tr.get("untracked", 0), tr.get("obligations", 0), None,
              "batch-K transfers (transfer_audit via the reporter)", src, t, "a transfer is not closure: it blocks until its destination resolves it")]


STAGES = ("research", "evidence-ready", "review", "repair", "incorporation", "accepted-and-incorporated", "dispositioned")


def package_checks(pkgdir, tasks):
    """Each package's work items with their recorded stage, and three consistency flags (not a derivation of acceptance -
    that judgment is the package owner's): STAGE-MISMATCH (package stage != its earliest item stage), LINK-DONE (the item
    still says research..incorporation while every board task it links is DONE), FALSE-COMPLETE (the item says
    accepted-and-incorporated or dispositioned while a linked board task is not DONE)."""
    out = []
    for p in sorted(glob.glob(os.path.join(pkgdir, "PKG-*.md"))):
        s = open(p, encoding="utf-8").read()
        m = re.search(r"^\*\*stage\.\*\*\s*`([a-z-]+)`", s, re.M)
        rec = m.group(1) if m else "UNKNOWN"
        items = []
        sec = s[s.find("**work items.**"):] if "**work items.**" in s else ""
        for line in sec.splitlines():
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) < 7 or not re.fullmatch(r"[A-Z]{1,3}\d+", c[0]):
                continue
            sm = re.match(r"^`?([a-z-]+)`?", c[-1])
            stage = sm.group(1) if sm and sm.group(1) in STAGES else "UNKNOWN"
            links = sorted(set(x for x in re.findall(r"\b[A-Z][A-Z0-9]+(?:-[A-Z0-9]+){2,}\b", line) if x in tasks))
            flags = []
            if links and stage in STAGES[:5] and all(tasks[x]["status"] == "DONE" for x in links):
                flags.append("LINK-DONE")
            if links and stage in ("accepted-and-incorporated", "dispositioned") and any(tasks[x]["status"] != "DONE" for x in links):
                flags.append("FALSE-COMPLETE")
            items.append({"item": c[0], "kind": c[2], "owner": c[4], "reviewer": c[5], "stage": stage, "links": links, "flags": flags})
        known = [STAGES.index(i["stage"]) for i in items if i["stage"] in STAGES[:6]]
        earliest = STAGES[min(known)] if known else None
        pflags = ["STAGE-MISMATCH"] if earliest and rec in STAGES and rec != earliest else []
        out.append({"id": os.path.basename(p)[:-3], "stage": rec if rec in STAGES else "UNKNOWN", "earliest": earliest, "items": items, "flags": pflags})
    return out


def v_systems(inp, t):
    subs = [l.rstrip("\r\n").split("\t") for l in open(inp["subsystems"], encoding="utf-8")][1:]
    ver = {}
    for m in re.finditer(r"^\|\s*\*?\*?(S-\d+)\*?\*?[^|]*\|\s*\**(MET|NOT MET|PARTIAL|UNMET)?", open(inp["l2"], encoding="utf-8").read(), re.M):
        ver.setdefault(m.group(1), m.group(2) or "UNKNOWN")
    cats = json.load(open(inp["_tree"], encoding="utf-8"))
    bycat = collections.defaultdict(list)
    for r in subs:
        bycat[r[1][:2]].append({"id": r[0], "label": "%s %s" % (r[0], r[2][:90]), "state": "UNMEASURED", "counts": {"scoped L2 verdict": ver.get(r[0], "UNKNOWN"), "open obligations under this system": "UNMEASURED (no system-to-obligation link yet)"},
                                "links": [{"label": "page", "href": x} for x in r[4].split(";") if x][:2]})
    tree = []
    for c in cats:
        node = {"id": c["name"], "label": c["name"], "counts": {"documents": c["docs"], "subcategories": len(c["subs"])},
                "children": [{"id": s["name"], "label": s["name"], "counts": {"documents": s["docs"]}} for s in c["subs"]]}
        if bycat.get(c["name"][:2]):
            node["children"] = bycat[c["name"][:2]] + node["children"]
        tree.append(node)
    met = sum(1 for r in subs if ver.get(r[0]) == "MET")
    return {"view": "systems", "title": "Game systems - repository categories and the 52 registered systems", "status": "OK",
            "source": {"identity": "important-subsystems.tsv %s; L2-VERDICTS.md %s" % (sha12(inp["subsystems"]), sha12(inp["l2"])), "as_of": t,
                       "instrument": "build_views.v_systems", "limits": "document counts are inventory, not understanding; scoped L2 MET is not whole-database completion"},
            "measures": [M("l2-met", "L2-specific (scoped) requirements: registered systems with verdict MET", met, len(subs),
                           "important-subsystems.tsv x L2-VERDICTS.md", "v_systems", t,
                           "L2-specific / scoped only - not cumulative L2, which is gated by L1 (My Progress); residual register rows and "
                           "terminal audit are separate (overview)"),
                         M("categories", "repository categories", len(cats), None, "top-level folders of FFXII TZA", "v_systems", t, "includes residual and library categories")],
            "tree": tree}


def v_vbf(inp, t):
    """v2 (2026-09-29): the tree comes from the INSTALLED archive's own header, read at every build (vbf_index.py, ASTRA's
    A17 parser), not from the 2026-09-02 listing; the format stages come from the captured X-family requirement facts
    and the archive_formats claims. A failed archive read is FAILED, never a silent fallback to the old listing."""
    idx = json.load(open(inp["vbf_index"], encoding="utf-8"))
    facts = json.load(open(inp["requirement_facts"], encoding="utf-8"))
    if "failed" in idx:
        return {"view": "vbf", "title": "VBF archive - the installed archive's own folder tree", "status": "FAILED",
                "source": {"identity": "vbf_index capture", "as_of": t, "instrument": "vbf_index.py", "limits": "the archive index could not be read: " + idx["failed"]},
                "measures": [], "rows": {"columns": ["failure"], "data": [[idx["failed"]]]}}
    files, byts, ext, eb = 0, 0, collections.Counter(), collections.Counter()
    node = lambda: {"files": 0, "bytes": 0, "kids": {}}
    root = node()
    for p, sz in idx["entries"]:
        parts = p.replace("\\", "/").split("/")
        e = parts[-1].rsplit(".", 1)[-1].lower() if "." in parts[-1] else "(none)"
        files += 1; byts += sz; ext[e] += 1; eb[e] += sz
        n = root
        for seg in parts[:-1][:3]:
            n = n["kids"].setdefault(seg, node()); n["files"] += 1; n["bytes"] += sz
    def conv(name, n, path):
        return {"id": path, "label": name, "counts": {"files": n["files"], "bytes": n["bytes"]},
                "children": [conv(k, v, path + "/" + k) for k, v in sorted(n["kids"].items())]}
    X = [f for f in facts.get("facts", []) if f.get("f") == "X"]
    xe = [f for f in X if "/" not in f["k"]]; xm = [f for f in X if "/" in f["k"]]
    members = collections.Counter(f["k"][2:].split("/")[0] for f in xm)
    xgap = (facts.get("gaps") or {}).get("X"); xfail = (facts.get("failed") or {}).get("X")
    claims = idx.get("format_claims") or {}
    # The listing comparison is measured only when the capture recorded one with all three counts; an absent, missing,
    # unreadable or malformed comparison is UNMEASURED and named, never a drift of 0 (ASTRA's REJECT of eae0ed3c7).
    vs = idx.get("vs_listing")
    keys = ("missing_from_archive", "missing_from_listing", "size_mismatch")
    if isinstance(vs, dict) and all(isinstance(vs.get(k), int) for k in keys):
        drift, cmp_fail = sum(vs[k] for k in keys), None
    else:
        drift, cmp_fail = None, idx.get("vs_listing_failed") or ("malformed listing comparison" if vs is not None else "no listing comparison in the capture")
    rec = idx["archive_index"]
    measured = not (xgap or xfail or idx.get("format_claims_failed"))
    idn = "installed archive header sha256 %s (%d entries, file %d bytes)" % (rec["header_sha256"][:12], rec["entry_count"], idx["archive_file_bytes"])
    ms = [M("files", "files in the archive", files, None, "installed archive index", "vbf_index", t, "a file count; distinct formats and bytes are other denominators"),
          M("bytes", "bytes in the archive (uncompressed)", byts, None, "installed archive index", "vbf_index", t, "uncompressed sizes from the header"),
          M("extensions", "distinct file extensions", len(ext), None, "installed archive index", "vbf_index", t, "an extension is not a format variant"),
          M("formats-ext", "archive extensions with an accepted format disposition", sum(1 for f in xe if f.get("ok")), len(xe),
            "X family, extensions (requirement facts)", "requirements.py X", t, "explained / standard / external; a bucketed extension counts through its members"),
          M("formats-members", "bucket member formats explained", sum(1 for f in xm if f.get("ok")), len(xm),
            "X family, bucket members (requirement facts)", "requirements.py X", t, "a signature-scoped archive_formats claim explains the member")]
    if drift is not None:
        ms.insert(3, M("listing-drift", "entries where the old 2026-09-02 listing differs from the installed archive", drift, None,
                       "installed index vs vbf_list.txt", "vbf_index", t,
                       "0 = the old listing still describes the archive exactly (ASTRA A17's check, re-run every build)"))
    rows = [[e, c, eb[e], ",".join(claims.get(e, [])) or ("bucket (%d members)" % members[e] if members.get(e) else "-")] for e, c in ext.most_common()]
    lim = ("the tree IS the installed archive's folder tree (the VBF Browser has no category table), read from its header at this build; payload bytes, "
           "decompression and a running game's binding to this archive are not claimed. Format stages: disposition and layout explanation per "
           "extension and bucket member; field meaning is the format sheets' own claim")
    if not measured:
        lim += ". UNMEASURED: " + (xgap or xfail or idx.get("format_claims_failed"))
    if cmp_fail:
        lim += ". Listing comparison UNMEASURED: " + cmp_fail
        rows.insert(0, ["(listing comparison)", "UNMEASURED", "-", cmp_fail])
    return {"view": "vbf", "title": "VBF archive - the installed archive's own folder tree", "status": "OK" if measured and drift == 0 else "PARTIAL",
            "source": {"identity": idn, "as_of": t, "instrument": "vbf_index.py (ASTRA A17 header parser) + requirements.py X", "limits": lim},
            "measures": ms, "tree": [conv(k, v, k) for k, v in sorted(root["kids"].items())],
            "rows": {"columns": ["extension", "files", "bytes", "format disposition"], "data": rows}}


def v_executable(inp, t):
    s = open(inp["coverage_dims"], encoding="utf-8").read()
    ms, sec = [], ""
    for line in s.splitlines():
        h = re.match(r"^##\s+(.*)$", line)
        if h: sec = h.group(1).strip(); continue
        c = [x.strip().strip("*").strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 3 and re.fullmatch(r"\d+", c[1] or "") and re.fullmatch(r"\d+", (c[2].split()[0] if c[2] else "")):
            lab = c[0].replace("*", "").strip()
            ms.append(M(re.sub(r"\W+", "-", lab.lower())[:40], lab, int(c[1]), int(c[2].split()[0]), sec, "program_coverage.py (COVERAGE-DIMENSIONS.md)", t,
                        "as generated; citation is attention, not understanding"))
    bands = tuple(inp[k] for k in sorted((k for k in inp if k.startswith("uc1_band_")), key=lambda k: int(k.rsplit("_", 1)[1])))
    iv = text_intervals(inp["functions"], bands, inp["exe"], inp["extent_errata"])
    N = iv["text_size"]; scope = ".text %08X..%08X (%d bytes), each byte counted once" % (iv["text_lo"], iv["text_lo"] + N, N)
    inst = ("build_views.text_intervals over functions.tsv + uc1_band.apply + the adjudicated errata extents (%s) + the certified image"
            % uc1_band_describe_extents(iv["extents"]))
    lim = "physical boundary axis only: a byte inside a body is not READ or EXPLAINED (behavior is UNMEASURED here)"
    ims = [M("bytes-" + k, lab, iv["bytes"][k], N, scope, inst, t, lim) for k, lab in (
        ("listed", "bytes in listed function bodies (population)"), ("frontier", "bytes in UC-1 frontier bodies (population, unexplained by ruling)"),
        ("funclet", "bytes in EH funclets (code outside the population)"), ("held", "bytes in held rows (declared uncertainty, never counted as code)"),
        ("fill", "alignment fill: runs of int3 (CC) / nop (90) bytes outside every body"), ("unknown", "UNKNOWN bytes (no body, no held row, not fill)"))]
    ims.append(M("bytes-overlap", "bytes claimed by more than one population body (each such byte once; counted once above)", iv["overlap"], N, scope, inst, t,
                 "listed extents that overlap a neighbour; unique bytes, not covers (%d additional covers over them). Definition v2: "
                 "v1 generations counted additional covers here, so no delta is taken across the change" % iv["overlap_extra_covers"]))
    ims.append(M("population", "functions in the population (%s)" % iv["describe"], iv["population"], None, "uc1_band.apply", inst, t,
                 "a versioned population; admitted frontier bodies are not explained"))
    # The BEHAVIOUR axis (2026-09-29): each population body's F-family disposition from the captured requirement facts -
    # A explained individually, B explained as a class, C dispositioned, or none yet - laid over its bytes, each byte once
    # (the first body to reach a byte keeps it, as for the boundary classes). Observed execution stays UNMEASURED.
    facts = json.load(open(inp["requirement_facts"], encoding="utf-8"))
    fdisp = {}
    for f in facts.get("facts", []):
        if f.get("f") == "F" and f.get("k", "").startswith("F:"):
            try:
                fdisp[int(f["k"][2:], 16)] = f["st"] if f.get("ok") and f.get("st") in ("A", "B", "C") else "none"
            except ValueError:
                pass
    lo, n = iv["text_lo"], iv["text_size"]
    beh = bytearray(n); code = {"A": 1, "B": 2, "C": 3, "none": 4}
    fcount = collections.Counter()
    for e, z in sorted(iv["pop"].items()):
        k = fdisp.get(e, "none"); fcount[k] += 1
        a, b = max(e - lo, 0), min(e + z - lo, n)
        if a < b:
            beh[a:b] = bytes(code[k] if c == 0 else c for c in beh[a:b])
    bc = collections.Counter(beh); popb = sum(bc[c] for c in (1, 2, 3, 4))
    blim = "behaviour axis: the F-family disposition of the body a byte belongs to; bytes, each once, over the population's bodies"
    for k, lab in (("A", "individually explained (A)"), ("B", "explained as a class (B)"), ("C", "dispositioned without explanation (C)"),
                   ("none", "no disposition yet")):
        ims.append(M("behavior-" + k.lower(), "population body bytes " + lab, bc[code[k]], popb, "population bodies (behaviour axis)", "requirements.py F + " + inst, t, blim))
        ims.append(M("functions-" + k.lower(), "population functions " + lab, fcount[k], iv["population"], "population (behaviour axis)", "requirements.py F", t,
                     "function counts; a large body and a thunk weigh the same here"))
    return {"view": "executable", "title": "Executable - every .text byte once, and the function-level dimensions", "status": "PARTIAL",
            "source": {"identity": "image %s; functions.tsv %s; COVERAGE-DIMENSIONS.md %s" % (iv["exe_sha"][:12], sha12(inp["functions"]), sha12(inp["coverage_dims"])),
                       "as_of": t, "instrument": inst + "; program_coverage.py",
                       "limits": "byte classes are the boundary axis; the behaviour axis is each body's F-family disposition (A / B / C / none); observed execution (live or isolated) is UNMEASURED here - no execution-coverage instrument maps runs to functions yet; "
                                 "data inside .text other than held rows is counted as UNKNOWN until a ruling classifies it; the fill rule is single-byte: multi-byte NOP fill counts as UNKNOWN, and a CC/90 byte inside unclassified data would count as fill"},
            "measures": ims + ms,
            "rows": {"columns": ["largest UNKNOWN gaps", "bytes", "next body"], "data": iv["gaps"]}}


_DEPTH = bytes([1, 2] + [2] * 254)   # cover depth, capped at 2: 0 -> 1 -> 2 -> 2


def population_cover(pop, front, lo, n):
    """Classify each population body's bytes (1 listed, 2 frontier; the first body to reach a byte keeps it) and count
    the overlap. Returns (cls, overlap, extra): overlap is the number of UNIQUE bytes covered by two or more bodies;
    extra is the number of additional covers (a byte in three bodies adds 2). Until 2026-09-29 the measure was `extra`
    under the name of `overlap` (ASTRA 0d9d9330c: 0032E040..0032E041 lies in three listed extents and was counted twice)."""
    cls = bytearray(n); depth = bytearray(n)
    overlap = extra = 0
    for e, z in pop.items():
        a, b = max(e - lo, 0), min(e + z - lo, n)
        if a >= b: continue
        seg = bytes(depth[a:b])
        overlap += seg.count(1); extra += (b - a) - seg.count(0)
        depth[a:b] = seg.translate(_DEPTH)
        k = 2 if e in front else 1
        cls[a:b] = bytes(k if c == 0 else c for c in cls[a:b])
    return cls, overlap, extra


def uc1_band_describe_extents(x):
    import uc1_band
    return uc1_band.describe_extents(x) if x else "none applied"


def text_intervals(functions_tsv, band_tsvs, exe, errata_tsv=None):
    """Each byte of .text in exactly one class: listed / frontier (the uc1_band population), funclet, held, fill, unknown.
    Definition v4 (2026-09-30): with errata_tsv, a listed body's extent is its listed range union its adjudicated `underrun`
    errata end (uc1_band.apply_extents; the chained-tails ruling), so a chained tail counts as its function's bytes."""
    import pefile, uc1_band
    pe = pefile.PE(exe, fast_load=True); B = pe.OPTIONAL_HEADER.ImageBase
    sec = next(s for s in pe.sections if s.Name.rstrip(b"\0") == b".text")
    lo, n = B + sec.VirtualAddress, sec.Misc_VirtualSize
    data = sec.get_data()[:n]
    sizes, funclets = {}, []
    for i, line in enumerate(open(functions_tsv, encoding="utf-8", errors="replace")):
        p = line.rstrip("\n").split("\t")
        if i == 0 or len(p) < 3: continue
        try: e, z = int(p[0], 16), int(p[2])
        except ValueError: continue
        (funclets.append((e, z)) if p[1].startswith(("Unwind@", "Catch_All@")) else sizes.__setitem__(e, z))
    saved = uc1_band.BAND_TSVS
    try:
        uc1_band.BAND_TSVS = tuple(band_tsvs); band = uc1_band.load()
    finally:
        uc1_band.BAND_TSVS = saved
    pop, info = uc1_band.apply(sizes, band)
    xinfo = None
    if errata_tsv:
        pop, xinfo = uc1_band.apply_extents(pop, errata_tsv)
    cls, overlap, extra = population_cover(pop, set(band["frontier"]), lo, n)   # 0 unknown, 1 listed, 2 frontier, 3 funclet, 4 held, 5 fill
    for code, spans in ((3, funclets), (4, [(s, e - s) for s, e in band["held"]])):
        for e, z in spans:
            a, b = max(e - lo, 0), min(e + z - lo, n)
            if a < b: cls[a:b] = bytes(code if c == 0 else c for c in cls[a:b])
    for m in re.finditer(rb"[\xcc\x90]+", data):
        a, b = m.span()
        cls[a:b] = bytes(5 if c == 0 else c for c in cls[a:b])
    names = {0: "unknown", 1: "listed", 2: "frontier", 3: "funclet", 4: "held", 5: "fill"}
    cnt = collections.Counter(cls)
    gaps, starts = [], sorted(pop)
    import bisect
    for m in re.finditer(rb"\x00+", bytes(cls)):
        a, b = m.span(); nx = bisect.bisect_left(starts, lo + b)
        gaps.append((b - a, "%08X..%08X" % (lo + a, lo + b), "%08X" % starts[nx] if nx < len(starts) else "-"))
    gaps.sort(reverse=True)
    return {"text_lo": lo, "text_size": n, "pop": pop, "bytes": {names[k]: cnt.get(k, 0) for k in names}, "overlap": overlap, "overlap_extra_covers": extra,
            "population": info["total"], "describe": uc1_band.describe(info), "exe_sha": G.sha256_file(exe), "extents": xinfo,
            "gaps": [[g[1], g[0], g[2]] for g in gaps[:30]]}


def v_types(inp, t):
    rows = [l.rstrip("\r\n").split("\t") for l in open(inp["fields"], encoding="utf-8")][1:]
    ntypes = sum(1 for _ in open(inp["types"], encoding="utf-8")) - 1
    rd = collections.Counter(r[6] for r in rows if len(r) > 7)
    cf = collections.Counter(r[7] for r in rows if len(r) > 7)
    return {"view": "types", "title": "Types - the record store (representation axis)", "status": "OK",
            "source": {"identity": "types.tsv %s; fields.tsv %s" % (sha12(inp["types"]), sha12(inp["fields"])), "as_of": t, "instrument": "v_types",
                       "limits": "readiness is representation, not meaning (three axes); a row count is not byte coverage"},
            "measures": [M("types", "types in the store", ntypes, None, "_types/types.tsv", "v_types", t, "includes interior/embedded types"),
                         M("fields-resolved", "field rows TYPE RESOLVED", rd.get("TYPE RESOLVED", 0), len(rows), "_types/fields.tsv", "v_types", t,
                           "representation readiness only; meaning is a separate column")],
            "rows": {"columns": ["readiness", "rows"], "data": [[k, v] for k, v in rd.most_common()] + [["confidence: " + k, v] for k, v in cf.most_common()]}}


DEPTH_LABELS = {
    "engine_explained": "functions explained on an evidence page (the strict rule)",
    "ledger_resolved": "functions resolved in the coverage ledger",
    "audit_coverage": "documents with an audit pass",
    "registry_explained": "registry entries explained",
    "ebp_explained": "EBP script families explained",
    "formats_explained": "archive formats explained",
    "questions_closed": "register questions closed",
    "final_audits": "terminal final-audit passes",
}


def v_depth(inp, t):
    """The weighted depth score of gfz-scripts/progress.py (user request 2026-09-30: "add the percentages we're missing").
    Eight dimensions with fixed weights; OVERALL is their weighted mean. It differs from My Progress by design: a function
    counts here only when an evidence page explains it (engine_explained, weight 0.55), while My Progress counts one unit
    per governing requirement and accepts any function disposition. Read from progress.py --json every build."""
    try:
        d = json.load(open(inp["progress_py"], encoding="utf-8"))
    except (OSError, ValueError) as e:
        return {"view": "depth", "title": "Depth - progress.py's weighted score", "status": "FAILED",
                "source": {"identity": "progress.py capture", "as_of": t, "instrument": "progress.py --json",
                           "limits": "the capture could not be read: %s" % type(e).__name__}, "measures": []}
    ms = []
    if d.get("overall") is not None:
        ms.append(M("overall", "OVERALL - weighted depth score (progress.py)", round(d["overall"], 2), 100, "progress.py weights",
                    "progress.py --json", t, "the weighted mean of the dimensions below; weights are fixed in progress.py"))
    rows = []
    for x in d.get("dimensions", []):
        lab = "%s (weight %.2f)" % (DEPTH_LABELS.get(x["id"], x["id"]), x["weight"])
        if x.get("unavailable"):
            rows.append([x["id"], "UNAVAILABLE", x["numerator"], x["denominator"], x["weight"]]); continue
        ms.append(M(x["id"], lab, x["numerator"], x["denominator"], "progress.py " + x["id"], "progress.py --json", t,
                    "weight %.2f of the overall" % x["weight"]))
        rows.append([x["id"], "%.2f%%" % (100.0 * x["numerator"] / x["denominator"]), x["numerator"], x["denominator"], x["weight"]])
    st = "OK" if d.get("overall") is not None and not d.get("broken") else "PARTIAL"
    return {"view": "depth", "title": "Depth - progress.py's weighted score", "status": st,
            "source": {"identity": "progress.py %s" % sha12(inp["progress.py"]), "as_of": t, "instrument": "progress.py --json",
                       "limits": "a weighted composite: engine_explained (0.55) counts a function only when a page explains it, "
                                 "so it runs below My Progress, which accepts any function disposition; the two are not summed"},
            "measures": ms,
            "rows": {"columns": ["dimension", "percent", "numerator", "denominator", "weight"], "data": rows}}


def _board(inp):
    b = json.load(open(inp["team"], encoding="utf-8"))
    return b, (b["tasks"] if isinstance(b["tasks"], list) else list(b["tasks"].values()))


_VERDICT = re.compile(r"verdict:(ACCEPT|ACCEPT-WITH-NARROWING|REJECT|ESCALATE-FABLE|ESCALATE-OPUS|ESCALATE-ASTRA)")   # team.REVIEW_VERDICTS


def v_evidence(inp, t):
    """v2 (2026-09-29): verdicts from the structured `verdict:` result ref team.py now requires (A16, ed127d443), prose only
    as a labelled fallback for the legacy rows; seal.py receipts (intact, publishable) and live PENDING PROPAGATION markers
    from the evidence scan captured at this build."""
    b, ts = _board(inp)
    ev = json.load(open(inp["evidence_scan"], encoding="utf-8"))
    rev = [x for x in ts if re.search(r"REVIEW|SIGN|VERIFY", x["id"]) or "review" in (x.get("scope") or "").lower()]
    st = collections.Counter(x["status"] for x in rev)
    done = [x for x in rev if x["status"] == "DONE" and not x.get("retired")]
    formal = [x for x in done if isinstance(x.get("reviews"), dict)]
    vd = {x["id"]: [m.group(1) for r in (x.get("result_refs") or []) if isinstance(r, str) for m in [_VERDICT.fullmatch(r)] if m] for x in formal}
    structured = [i for i, v in vd.items() if len(v) == 1]
    vc = collections.Counter(vd[i][0] for i in structured)
    prose_acc = sum(1 for x in done if not isinstance(x.get("reviews"), dict) and re.match(r"\s*(ACCEPT|SIGNED)", x.get("checkpoint") or "", re.I))
    waiting = sorted((x for x in rev if x["status"] == "READY"), key=lambda x: x.get("updated_at") or "")[:40]
    ms = [M("reviews-done", "review/sign/verify tasks DONE", st.get("DONE", 0), len(rev), "board", "v_evidence", t, "DONE is not acceptance"),
          M("reviews-structured", "formal reviews (a reviews field) DONE with one structured verdict", len(structured), len(formal), "board, formal reviews",
            "v_evidence", t, "the rest predate the A16 gate (ed127d443) and are being ratified additively; a verdict is never read from prose here"),
          M("reviews-accepted", "structured verdicts ACCEPT or ACCEPT-WITH-NARROWING", vc["ACCEPT"] + vc["ACCEPT-WITH-NARROWING"], len(structured),
            "board, structured verdicts", "v_evidence", t, "REJECT %d, ESCALATE %d; informal reviews whose checkpoint begins ACCEPT/SIGNED (prose, "
            "not a verdict): %d" % (vc["REJECT"], sum(v for k, v in vc.items() if k.startswith("ESCALATE")), prose_acc))]
    lim = "review tasks recognised by id/scope; verdicts only from structured refs"
    ok = "failed" not in ev
    if ok:
        rc = ev["receipts"]
        ms += [M("receipts-intact", "sealed run receipts intact (seal.verify)", sum(1 for r in rc if r["intact"]), len(rc), "seal.py receipt stores",
                 "evidence_scan + seal.verify", t, "a stored copy that no longer matches its hash fails"),
               M("receipts-publishable", "sealed run receipts that pass the publication gate (seal.publishable)", sum(1 for r in rc if r["publishable"]), len(rc),
                 "seal.py receipt stores", "evidence_scan + seal.publishable", t, "committed drivers, exact case map, no WIP, valid cumulative reuse"),
               M("pending-propagation", "documents with a live PENDING PROPAGATION marker", len(ev["pending"]), None, "the database's .md files",
                 "evidence_scan", t, "a routed correction not yet in every consumer; a struck (~~) marker is not counted")]
        rows_extra = [["(receipt) %s/%s" % (r["store"], r["run_id"]), "intact" if r["intact"] else "BROKEN", "publishable" if r["publishable"] else "; ".join(r["problems"])]
                      for r in rc if not (r["intact"] and r["publishable"])]
    else:
        lim += "; the evidence scan FAILED (%s): receipts and pending propagation are UNMEASURED" % ev["failed"]
        rows_extra = []
    # v3 (2026-09-30, user request: the Radiata dashboard's Evidence tab): the same review measures, drawn by
    # pages/evidence.html beside the lessons ledger, the verification checks, the format registry and the question register.
    # A section that cannot be built carries {"failed": why}; the view is then PARTIAL and the page shows it unmeasured.
    sections = {}
    for key, fn in (("lessons", ev_lessons), ("findings", ev_findings), ("checks", ev_checks), ("register", ev_register)):
        try:
            sections[key] = fn(inp)
        except Exception as e:
            sections[key] = {"failed": "%s: %s" % (type(e).__name__, e)}
    try:
        sections["formats"] = ev_formats(inp, sections["checks"] if "failed" not in sections["checks"] else {})
    except Exception as e:
        sections["formats"] = {"failed": "%s: %s" % (type(e).__name__, e)}
    bad = sorted(k for k, s in sections.items() if "failed" in s)
    if bad:
        lim += "; section(s) FAILED: %s" % "; ".join("%s (%s)" % (k, sections[k]["failed"]) for k in bad)
    return {"view": "evidence", "title": "Evidence & lessons", "status": "OK" if ok and not bad else "PARTIAL", "page": "evidence",
            "source": {"identity": "TEAM.json rev %s epoch %s; evidence scan and checker run at this build" % (b.get("revision"), b.get("recovery_epoch")), "as_of": t,
                       "instrument": "v_evidence + evidence_scan.py + run_checks.py", "limits": lim},
            "measures": ms,
            "rows": {"columns": ["waiting review (oldest first)", "assigned to", "since"],
                     "data": rows_extra + [[x["id"], x.get("assigned_to"), (x.get("updated_at") or "")[:16]] for x in waiting]},
            "evidence": sections}


# ------------------------------------------------------------------ Evidence & lessons (v3, 2026-09-30)
# The Radiata dashboard's Evidence tab, for FF12 (user request 2026-09-30: "add something like this into our dashboard as
# well"). Each section reads only this build's captured inputs; a section that cannot be built says FAILED with the
# reason and the page shows it unmeasured, never empty.
DBREL = "Database/FFXII TZA"


def _lines(p):
    """A text input split on \\n or \\r\\n (the database's TSVs and pages have mixed line endings)."""
    return re.split(r"\r?\n", open(p, encoding="utf-8", errors="replace").read())


def ev_lessons(inp):
    """CONTRADICTIONS.tsv: every recorded correction. Comment lines start with #; the first other line is the header
    (contradiction_index.read_ledger's rule). A row's state follows goal_gate.check_contradictions: resolved when its kind
    is one of goal_gate.RESOLVED_CONTRA_KINDS, open when OPEN/FILED, otherwise unrecognised (the gate fails it)."""
    import goal_gate as GGT
    head, rows = None, []
    for line in _lines(inp["contradictions"]):
        if not line.strip() or line.startswith("#"):
            continue
        cells = line.split("\t")
        if head is None:
            head = cells
            continue
        r = dict(zip(head, cells))
        kind = (r.get("kind") or "").strip().upper()
        state = "resolved" if kind in GGT.RESOLVED_CONTRA_KINDS else "open" if kind in ("OPEN", "FILED") else "unrecognised"
        doc = r.get("document") or ""
        rows.append({"id": r.get("id", ""), "date": r.get("date", ""), "kind": r.get("kind", ""), "category": r.get("category", ""),
                     "document": doc, "line": r.get("line", ""), "claim": r.get("claim", ""), "correction": r.get("correction", ""),
                     "instrument": r.get("instrument", ""), "source_status": r.get("source_status", ""), "state": state,
                     "path": "%s/%s" % (DBREL, doc) if doc else ""})
    if head is None or "id" not in head:
        raise ValueError("CONTRADICTIONS.tsv has no header row")
    blank = lambda x: (x or "").strip() in ("", "UNSUMMARISED")
    inst = collections.Counter(r["instrument"] for r in rows if not blank(r["instrument"]))
    return {"source": DBREL + "/_index/CONTRADICTIONS.tsv", "identity": "sha %s" % sha12(inp["contradictions"]),
            "kpis": {"recorded": len(rows), "open": sum(r["state"] != "resolved" for r in rows), "resolved": sum(r["state"] == "resolved" for r in rows),
                     "unsummarised": sum(blank(r["correction"]) or blank(r["instrument"]) for r in rows),
                     "source_gone": sum((r["source_status"] or "present") != "present" for r in rows)},
            "kinds": dict(collections.Counter(r["kind"] for r in rows).most_common()),
            "instruments": inst.most_common(12), "rows": rows}


def ev_findings(inp):
    """RULES.md's "Instrument findings - how measurement goes wrong" section: each entry a titled link into COVERAGE.md,
    nested by indentation. Paths are made repo-relative so the page can hand them to the reader."""
    t = open(inp["rules"], encoding="utf-8", errors="replace").read()
    m = re.search(r"^## (Instrument findings[^\r\n]*)", t, re.M)
    if not m:
        raise ValueError("RULES.md has no 'Instrument findings' section")
    end = re.search(r"^## ", t[m.end():], re.M)
    sec = t[m.end(): m.end() + end.start() if end else len(t)]
    intro = next((l.strip() for l in re.split(r"\r?\n", sec) if l.strip() and not l.lstrip().startswith(("-", "**", "#"))), "")
    src = re.search(r"\*\*Source: \[`?([^`\]]+)`?\]\(([^)]+)\)\*\*", sec)
    base = DBREL + "/_index/"
    def rel(h):
        p, _, a = h.partition("#")
        return os.path.normpath(base + p).replace("\\", "/") + ("#" + a if a else "")
    entries = [[len(e.group(1)) // 2, e.group(2).replace("`", ""), rel(e.group(3))]
               for e in re.finditer(r"^( *)- \[(.+?)\]\(([^)\s]+)\)\s*$", sec, re.M)]
    if not entries:
        raise ValueError("the Instrument findings section lists no entries")
    return {"heading": m.group(1).strip(), "intro": intro, "source_label": src.group(1) if src else "COVERAGE.md",
            "source_path": rel(src.group(2)) if src else base + "COVERAGE.md", "entries": entries}


def _baseline(p):
    out = {}
    if p and os.path.isfile(p):
        for line in _lines(p):
            c = line.split("\t")
            if line.strip() and not line.startswith("#") and len(c) >= 2:
                out[c[0]] = c[1]
    return out


def classify_captured(kind, text, rc=None):
    """(status, reason) for the three instruments the build already runs. Fail-closed: PASS only on the instrument's own
    success line; an exit other than its documented codes, a traceback or silence is UNMEASURED."""
    text = text or ""
    if "Traceback (most recent call last)" in text:
        return "UNMEASURED", "the instrument crashed"
    if kind == "goal_gate":
        try:
            g = json.loads(text)
        except ValueError:
            return "UNMEASURED", "goal_gate.py printed no JSON (exit %s)" % rc
        if rc not in (None, 0, 1):
            return "UNMEASURED", "exit %s: the gate itself failed" % rc
        v = g.get("verdict") if isinstance(g, dict) else None
        return {"MET": ("PASS", "verdict MET"), "NOT_MET": ("FAIL", "verdict NOT_MET: %s" % g.get("remaining", ""))}.get(v, ("UNMEASURED", "no verdict (%r)" % v))
    if not text.strip():
        return "UNMEASURED", "the instrument printed nothing (exit %s)" % rc
    if rc not in (None, 0, 1, 2) or (kind == "check_questions" and rc not in (None, 0, 1)):
        return "UNMEASURED", "exit %s is not a verdict" % rc
    if kind == "check_questions":
        if re.search(r"QUESTION LEDGER INCONSISTENT", text):
            return "FAIL", "the question ledger is INCONSISTENT (the gate fails even though the script exits 0)"
        if re.search(r"^questions consistent", text, re.M):
            return "PASS", "the table and the document checklists agree"
        return "UNMEASURED", "no consistency verdict in the output"
    if kind == "progress_check":
        m = re.match(r"\s*(CURRENT|STALE|MISSING|INCOMPLETE)\b", text)
        if not m:
            return "UNMEASURED", "no CURRENT / STALE verdict in the output"
        return ("PASS", "the published progress snapshot is current") if m.group(1) == "CURRENT" else ("FAIL", text.strip().splitlines()[0][:200])
    return "UNMEASURED", "unknown instrument %s" % kind


def ev_checks(inp):
    import run_checks as RC
    ins = {}
    if inp.get("instruments") and os.path.isfile(inp["instruments"]):
        try:
            ins = json.load(open(inp["instruments"], encoding="utf-8"))
        except ValueError:
            ins = {}
    base = _baseline(inp.get("gate_baseline"))
    cards = []
    def captured(cid, kind, path, what, script, numbers, shown=None):
        rec = ins.get(kind) or {}
        text = open(path, encoding="utf-8", errors="replace").read() if path and os.path.isfile(path) else ""
        st, why = classify_captured(kind, text, rec.get("exit"))
        cards.append({"id": cid, "what": what, "status": st, "reason": why, "exit": rec.get("exit"), "seconds": rec.get("seconds"),
                      "ran_at": rec.get("ran_at"), "numbers": numbers(text) if st != "UNMEASURED" else [[k, None] for k, _ in numbers("")],
                      "output": (shown(text) if shown and st != "UNMEASURED" else text), "script": script,
                      "args": (["check"] if kind == "progress_check" else []) + ["--db", "<db>"] + (["--json"] if kind == "goal_gate" else []),
                      "captured": "captured once per build, shared with the other tabs", "baseline_exit": base.get(os.path.basename(script))})
    def gg(text):
        try:
            g = json.loads(text)
            return g if isinstance(g, dict) else {}
        except ValueError:
            return {}
    def gg_nums(text):
        d = gg(text).get("detail") or []
        return [["conditions met", sum(1 for x in d if ": OK" in x) if d else None], ["conditions unmet", sum(1 for x in d if ": UNMET" in x) if d else None]]
    def gg_shown(text):
        g = gg(text)
        return "\n".join(["verdict: %s" % g.get("verdict"), ""] + list(g.get("detail") or []) + ["", "remaining: %s" % g.get("remaining", ""), "next: %s" % g.get("next", "")])
    def cq_nums(text):
        g = lambda rx: (lambda m: int(m.group(1)) if m else None)(re.search(rx, text, re.M))
        return [["rows", g(r"rows: (\d+)")]] + [[k.lower(), g(r"^\s+%s\s+(\d+)" % k)] for k in ("ANSWERED", "PARTIAL", "OPEN", "BLOCKED")]
    def pc_nums(text):
        m = re.search(r"all (\d+) outputs coherent", text)
        return [["outputs coherent", int(m.group(1)) if m else None]]
    captured("goal_gate", "goal_gate", inp["goal_gate"], "The database's own finish line: every condition the goal requires, from the committed records only.",
             "Database/Tools/analysis-kit/gfz-scripts/goal_gate.py", gg_nums, gg_shown)
    captured("check_questions", "check_questions", inp["check_questions"], "The question register and the per-page checklists agree, and every row carries a status word the gate knows.",
             "Database/Tools/analysis-kit/gfz-scripts/check_questions.py", cq_nums)
    captured("progress_report", "progress_check", inp["progress_check"], "The published progress snapshot was measured from the database as it is now.",
             "Database/FFXII TZA/_index/progress/progress_report.py", pc_nums)
    run, failed = None, None
    if inp.get("checks") and os.path.isfile(inp["checks"]):
        try:
            run = json.load(open(inp["checks"], encoding="utf-8"))
        except ValueError as e:
            failed = "checks.json unreadable: %s" % e
    else:
        failed = "run_checks.py produced no record at this build"
    by_id = {c["id"]: c for c in (run or {}).get("checks", [])}
    for spec in RC.CHECKS:
        c = by_id.get(spec["id"])
        if c is None:
            c = {"id": spec["id"], "what": spec.get("what", ""), "status": "UNMEASURED", "reason": failed or "not in this build's check run",
                 "numbers": [[k[0], None] for k in spec.get("keys", [])], "output": "", "script": spec["script"], "args": spec.get("args", [])}
        c = dict(c)
        c["baseline_exit"] = base.get(os.path.basename(spec["script"]))
        c["captured"] = "run at this build"
        cards.append(c)
    return {"cards": cards, "excluded": RC.EXCLUDED, "run_seconds": (run or {}).get("seconds"), "run_failed": failed}


def ev_formats(inp, checks):
    """The shipped-file-format registry: the population from the archive census TSV (census_archive_formats.py's output,
    the denominator check_assets scores against) joined with check_assets' own verdict per extension, read from this
    build's check run. When check_assets is unmeasured every state is a dash, never 'undeclared'."""
    rows, head = [], None
    for line in _lines(inp["format_census"]):
        if not line.strip() or line.startswith("#"):
            continue
        c = line.split("\t")
        if head is None:
            head = c
            continue
        r = dict(zip(head, c))
        rows.append({"ext": r["ext"], "files": int(r["files"]), "bytes": int(r["bytes"]), "dirs": r.get("top_dirs", ""),
                     "state": None, "sheet": "", "sheet_path": "", "twice": False})
    ca = next((c for c in checks.get("cards", []) if c["id"] == "check_assets"), None)
    measured = bool(ca and ca.get("status") in ("PASS", "FAIL") and ca.get("output"))
    sigs, twice = [], set()
    if measured:
        out = ca["output"]
        st = {}
        for m in re.finditer(r"^\s+\[(x|~| )\]\s+(\S+)\s+(.*)$", out, re.M):
            ext, rest = m.group(2), m.group(3).strip()
            if m.group(1) == " ":
                st[ext] = ("undeclared", "")
            else:
                p = rest.split(None, 1)
                st[ext] = (p[0], p[1].strip() if len(p) > 1 else "")
        block = re.search(r"FORMATS CLAIMED TWICE[^\n]*\n((?:\s{4}\S.*\n?)*)", out)
        if block:
            twice = {l.split()[0] for l in block.group(1).splitlines() if l.strip()}
        sigs = [[m.group(1), m.group(2), m.group(3), "%s/%s" % (DBREL, m.group(2))]
                for m in re.finditer(r"^\s{4}(\S+)\s+(\S+\.md)\s+\(signature inside \.(\w+)\)", out, re.M)]
        for r in rows:
            s = st.get(r["ext"])
            r["state"] = s[0] if s else "undeclared"
            r["sheet"] = s[1] if s else ""
            r["sheet_path"] = "%s/%s" % (DBREL, s[1]) if s and s[1] else ""
            r["twice"] = r["ext"] in twice
    order = {"undeclared": 0, "bucket": 1, "external": 2, "standard": 3, "explained": 4}
    rows.sort(key=lambda r: (order.get(r["state"], 9), -r["files"]))
    cnt = collections.Counter(r["state"] for r in rows)
    k = {"extensions": len(rows), "files": sum(r["files"] for r in rows),
         "covered": (cnt["explained"] + cnt["standard"] + cnt["external"]) if measured else None,
         "bucket": cnt["bucket"] if measured else None, "undeclared": cnt["undeclared"] if measured else None}
    return {"kpis": k, "rows": rows, "signatures": sigs, "measured": measured,
            "limits": "Population: archive-extension-census.tsv (%s). States: check_assets.py at this build%s." %
                      (sha12(inp["format_census"]), "" if measured else " - UNMEASURED (%s)" % ((ca or {}).get("reason") or "no record")),
            "docs": [DBREL + "/_index/ASSET-FORMATS.md", DBREL + "/_index/FORMATS-DECLARATION.md"]}


def _plain(s, n):
    s = re.sub(r"\\\|", "|", s or "")
    s = re.sub(r"~~(.+?)~~", r"\1", s)
    s = re.sub(r"\*\*|`|<br\s*/?>", " ", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def ev_register(inp):
    """Every register row, parsed with check_questions' own QID, classify and row_cells, one row per id with the last
    occurrence winning (read_table's rule), so the counts are the gate's. Section = the nearest ## heading above."""
    import bisect
    import check_questions as CQ
    t = open(inp["register"], encoding="utf-8", errors="replace").read()
    heads = [(m.start(), m.group(1).strip()) for m in re.finditer(r"^## +(.+?)\s*$", t, re.M)]
    hpos = [h[0] for h in heads]
    table, seen, dupes = {}, set(), []
    for m in re.finditer(r"^\|\s*(%s)\s*\|(.*)$" % CQ.QID, t, re.M):
        qid = m.group(1)
        st, _ = CQ.classify(m.group(2))
        cells = [c.strip() for c in CQ.row_cells(m.group(0))]
        i = bisect.bisect_right(hpos, m.start()) - 1
        body = [c for c in cells[1:]]
        q = body[0] if body else ""
        rest = [c for c in body[1:] if c]
        if qid in seen:
            dupes.append(qid)
        seen.add(qid)
        table[qid] = {"id": qid, "status": st, "section": heads[i][1] if i >= 0 else "(before the first section)",
                      "question": _plain(q, 280), "answer": _plain(CQ.live_lead(rest[-1]), 240) if rest else ""}
    rows = list(table.values())
    counts = dict(collections.Counter(r["status"] for r in rows))
    gate = {}
    try:
        txt = open(inp["check_questions"], encoding="utf-8", errors="replace").read()
        mrow = re.search(r"rows: (\d+)", txt)
        if mrow:
            gate["rows"] = int(mrow.group(1))
            for mm in re.finditer(r"^\s{6}(ANSWERED|PARTIAL|OPEN|BLOCKED|UNMARKED)\s+(\d+)\s*$", txt, re.M):
                gate[mm.group(1)] = int(mm.group(2))
    except OSError:
        pass
    agree = bool(gate) and gate.get("rows") == len(rows) and all(counts.get(k, 0) == v for k, v in gate.items() if k != "rows")
    note = "" if agree else ("The gate's printed counts differ from this snapshot of the register (it moved between the gate run and the snapshot); "
                             "the rows below are the snapshot." if gate else "The gate's printed counts could not be read; the rows below are the snapshot.")
    if dupes:
        note = (note + " " if note else "") + "Duplicate ids (the last row wins, as in check_questions): %s." % ", ".join(sorted(set(dupes)))
    return {"total": len(rows), "counts": counts, "gate_counts": gate, "gate_agrees": agree, "note": note, "rows": rows}


def v_fleet(inp, t):
    b, ts = _board(inp)
    act = [x for x in ts if x["status"] == "ACTIVE"]
    ws = {}
    if inp.get("watchdog") and os.path.isfile(inp["watchdog"]):
        ws = json.load(open(inp["watchdog"], encoding="utf-8"))
    rows = [[x.get("agent"), x["id"], (x.get("updated_at") or "")[:16], (x.get("checkpoint") or "")[:80]] for x in sorted(act, key=lambda x: x.get("agent") or "")]
    return {"view": "fleet", "title": "Fleet - lanes and their active work", "status": "PARTIAL",
            "source": {"identity": "TEAM.json rev %s; watchdog-state %s" % (b.get("revision"), "present" if ws else "absent"), "as_of": t, "instrument": "v_fleet",
                       "limits": "model, effort, account limits and utilisation are UNKNOWN (not exposed to this adapter); Claude lanes are not in the watchdog"},
            "measures": [M("active", "tasks ACTIVE on the board", len(act), None, "board", "v_fleet", t, "one row per active claim")],
            "rows": {"columns": ["lane", "active task", "updated", "checkpoint"], "data": rows +
                     [["(watchdog) " + k, "in flight", "", ""] for k in sorted(ws.get("inflight", {}))]}}


def v_progress(inp, t):
    """My Progress (MP-2, FABLE review C1-C4 applied): requirement accounting from the captured facts, the category map, the board, DATA's reporter
    snapshot and the goal gate. Every headline number is also a validated measure; the drill-down rides alongside."""
    import requirements as R
    facts = json.load(open(inp["requirement_facts"], encoding="utf-8"))
    b, _ts = _board(inp)
    prior = json.load(open(inp["_prior_progress"], encoding="utf-8")) if inp.get("_prior_progress") else None
    r = R.measure(facts, R.load_map(inp["category_map"]), b, json.load(open(inp["progress_snapshot"], encoding="utf-8")),
                  json.load(open(inp["goal_gate"], encoding="utf-8")), inp["subsystems"], prior)
    inst = "requirements.py %s over captured facts (%s)" % (R.VERSION, sha12(inp["requirement_facts"]))
    defs = "_index/workflow/MY-PROGRESS-METRICS.md"
    lim = "counts requirements (one governing criterion on one canonical object), not effort or time; " + (
        "every family measured" if r["measured"] else "UNMEASURED - known requirements only; %s" % r["why_not_ready"])
    sc = r["scopes"]
    ms = [M("union", "governing requirements accepted, L1+L2 (deduplicated union)", sc["union"]["accepted"], sc["union"]["total"], "L1 u L2", inst, t, lim),
          M("L1", "L1 requirements accepted", sc["L1"]["accepted"], sc["L1"]["total"], "L1 (modding grade)", inst, t, lim),
          M("L2", "L2-scoped requirements accepted (L2-tagged, including requirements shared with L1)", sc["L2"]["accepted"], sc["L2"]["total"],
            "L2 scope (reconstruction grade)", inst, t, lim),
          M("L2-specific", "L2-specific (scoped) requirements accepted - the L2-only requirements", sc["L2_specific"]["accepted"],
            sc["L2_specific"]["total"], "L2-specific", inst, t, lim + "; L2-specific at 100 % is not cumulative L2"),
          M("L2-cumulative", "cumulative L2 - gated by L1, never above L1: %s (bounded by %s)" % (sc["L2_cumulative"]["state"],
            sc["L2_cumulative"]["bounded_by"]), sc["L2_cumulative"]["accepted"], sc["L2_cumulative"]["total"], "cumulative L2 (L1-gated)", inst, t,
            "the lower of L1 and L2-specific, each with its own denominator (no averaging); COMPLETE only when both are complete. "
            + (sc["L2_cumulative"]["why"] or "")),
          M("union-exf", "governing requirements accepted, L1+L2, excluding the 35,065 function dispositions (C1)", sc["union_exF"]["accepted"],
            sc["union_exF"]["total"], "L1 u L2 without family F", inst, t, lim),
          M("terminal", "terminal final-audit passes accepted", r["terminal"]["accepted"] or 0, r["terminal"]["required"], "FINAL-AUDIT-PROTOCOL", inst, t,
            "30 consecutive passes; counted from the governing gate's acceptance check and the receipted counter")]
    ms += [M("fam-" + k.lower(), R.FAMILIES[k], v["accepted"], v["total"], "family " + k, inst, t, defs) for k, v in r["families"].items()]
    ms += [M("cat-" + k, (R.GROUPS.get(k) or k), v["accepted"], v["total"], "category " + k, inst, t,
             "shared requirements appear under every category they belong to; each counts once globally") for k, v in r["categories"].items()]
    cats = []
    for code, v in r["categories"].items():
        items = r["remaining"].get(code, [])
        fn = [f for f in items if f["f"] == "F"]
        by = collections.defaultdict(list)
        for f in fn:
            by["%s | %s" % (f["st"], f["o"] or next((h[1] for h in f.get("h", []) if h[0] in ("domain", "boundary")), "no owner, generic shape"))].append(f["k"][2:])
        fam = collections.Counter(f["f"] for f in items)
        cats.append({"code": code, "label": R.GROUPS.get(code) or {"whole": "Whole database (final certification, cross-cutting)",
                                                                     "untied": "Code not yet tied to a game system"}[code],
                     "accepted": v["accepted"], "total": v["total"], "remaining_by_family": dict(fam),
                     "change": (r["change"] or {}).get("categories", {}).get(code) if r["change"] and r["change"].get("comparable") else None,
                     "items": [{k: f.get(k) for k in ("k", "f", "st", "o", "n", "e", "lv")} for f in items if f["f"] != "F"],
                     "functions": [[k, len(v2), " ".join(sorted(v2))] for k, v2 in sorted(by.items(), key=lambda kv: -len(kv[1]))]})
    ready = r["ready"]
    return {"view": "progress", "title": "My Progress", "status": "OK" if r["measured"] else "PARTIAL",
            "source": {"identity": "facts %s; category map %s; board rev %s; reporter %s; gate %s" % (
                sha12(inp["requirement_facts"]), sha12(inp["category_map"]), b.get("revision"),
                json.load(open(inp["progress_snapshot"], encoding="utf-8")).get("commit_id"), json.load(open(inp["goal_gate"], encoding="utf-8")).get("verdict")),
                       "as_of": t, "instrument": inst, "limits": lim + "; definitions " + defs},
            "measures": ms,
            "progress": {"version": r["version"], "measured": r["measured"], "failed": r["failed"], "gaps": r["gaps"], "q_split": r["q_split"],
                         "review": "_index/candidates/mp1-meanings-review/ (FABLE: ACCEPT with C1-C4, applied in MP-2)", "definitions": defs,
                         "map": "_index/workflow/my-progress/category-map.tsv",
                         "unit": "One requirement = one governing criterion applied to one canonical object the database already names "
                                 "(a register row, a page box, a function, a document, a registry slot, a format, an EBP unit, a contradiction, "
                                 "an S-id x L2 dimension, a terminal pass). Accepted = fully satisfied under the governing record. "
                                 "This measures requirements, not elapsed time or equal-sized engineering effort.",
                         "scopes": sc, "families": {k: dict(v, label=R.FAMILIES[k]) for k, v in r["families"].items()},
                         "terminal": r["terminal"], "terminal_observed": r.get("terminal_observed"),
                         "reconstruction": {"state": "DATABASE READY - awaiting user authorization" if ready else "NOT READY", "why": r["why_not_ready"]},
                         "categories": cats, "change": r["change"], "excluded": r["excluded"], "unplaced": r["unplaced"],
                         "duplicates_merged": r["duplicates_merged"]}}


VERDICT_RE = re.compile(r"\b(ACCEPT-WITH-NARROWING|ACCEPT|REJECT|ESCALATE-[A-Z]+|ESCALATE)\b")
PRIO = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


def v_glance(inp, t):
    """At a glance - the DWNO database dashboard's one-page layout for FF12 (user request 2026-09-30: "can we also make a
    view like the one used for the dwno database"). Headline tiles, the trend over generations, the priority ladder, the
    identities (lanes), the question register by section, the audit exchange, recent commits and the frontier. Every
    number comes from this build's captured inputs; the page (pages/glance.html) only draws it."""
    import check_questions as CQ
    prog = v_progress(inp, t)
    pm = {m["id"]: m for m in prog["measures"]}
    gg = json.load(open(inp["goal_gate"], encoding="utf-8"))
    try:
        pp = json.load(open(inp["progress_py"], encoding="utf-8"))
    except (OSError, ValueError, KeyError):
        pp = {}
    board, _ = _board(inp)
    tasks = board.get("tasks", [])
    now = datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)

    def age_h(ts):
        try:
            d = datetime.datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        except ValueError:
            return None
        if d.tzinfo is None:          # some board records carry naive UTC stamps
            d = d.replace(tzinfo=datetime.timezone.utc)
        return (now - d).total_seconds() / 3600.0
    # the register, row by row, by section prefix (the id's letters)
    reg = open(inp["register"], encoding="utf-8", errors="replace").read()
    sec = collections.defaultdict(collections.Counter)
    open_rows = []
    for mm in re.finditer(r"^\|\s*(%s)\s*\|(.*)$" % CQ.QID, reg, re.M):
        st, cells = CQ.classify(mm.group(2))
        sec[re.match(r"[A-Z]+", mm.group(1)).group(0)][st] += 1
        if st in ("OPEN", "PARTIAL"):
            open_rows.append([mm.group(1), st, re.sub(r"[*`]", "", cells[0] if cells else "")[:160]])
    sections = sorted(([k, dict(v)] for k, v in sec.items()), key=lambda kv: -(kv[1].get("OPEN", 0) + kv[1].get("PARTIAL", 0)))
    # identities (lanes): active claims, ready work addressed to them, done in 24 h, commits in 24 h
    commits = []
    for line in open(inp["gitlog"], encoding="utf-8", errors="replace"):
        p = line.rstrip("\n").split("\t", 2)
        if len(p) == 3:
            commits.append(p)
    ident = lambda s: (re.match(r"^([A-Z][A-Z0-9-]+):", s) or re.match(r"^()", s)).group(1)
    lanes = collections.defaultdict(lambda: {"active": [], "ready": 0, "done24": 0, "commits24": 0, "last_commit": None})
    for tk in tasks:
        st, who, to = tk.get("status"), tk.get("agent"), tk.get("assigned_to")
        if st == "ACTIVE" and who:
            lanes[who]["active"].append([tk["id"], (tk.get("target") or "")[:120], tk.get("priority")])
        if st == "READY" and to:
            lanes[to]["ready"] += 1
        if st == "DONE" and who and (age_h(tk.get("updated_at")) or 1e9) <= 24:
            lanes[who]["done24"] += 1
    for h, ts, s in commits:
        who = ident(s)
        if not who:
            continue
        if (age_h(ts) or 1e9) <= 24:
            lanes[who]["commits24"] += 1
        if lanes[who]["last_commit"] is None:
            lanes[who]["last_commit"] = [h, ts, s[:140]]
    lanes = {k: v for k, v in lanes.items() if v["active"] or v["commits24"] or v["done24"] or v["ready"]}
    # the priority ladder: every ACTIVE or READY task, most urgent first
    ladder = sorted(([tk["id"], tk.get("status"), tk.get("priority"), tk.get("agent") or tk.get("assigned_to") or "",
                      (tk.get("target") or "")[:140]] for tk in tasks if tk.get("status") in ("ACTIVE", "READY")),
                    key=lambda r: (PRIO.get(r[2], 9), r[1] != "ACTIVE", r[0]))
    # the audit exchange: review requests and their verdicts
    audits, verdicts = [], collections.Counter()
    for tk in tasks:
        if not re.search(r"REVIEW|AUDITSPEC|AUDITSEM|AUDIT-SPEC|AUDIT-SEM", tk["id"]):
            continue
        v = VERDICT_RE.search(" ".join(str(tk.get(k) or "") for k in ("note", "checkpoint", "result")))
        vd = v.group(1) if v and tk.get("status") == "DONE" else ("pending" if tk.get("status") != "DONE" else "done")
        verdicts[vd] += 1
        audits.append([tk["id"], tk.get("status"), vd, tk.get("assigned_to") or tk.get("agent") or "", tk.get("updated_at") or ""])
    audits.sort(key=lambda r: r[4], reverse=True)
    # the trend: one point per generation from the measure history
    series = []
    try:
        for line in open(inp["history"], encoding="utf-8"):
            h = json.loads(line)
            d = {(x[0], x[2]): (x[3], x[4]) for x in h.get("measures", [])}
            u, o = d.get(("progress", "union")), d.get(("depth", "overall"))
            q = d.get(("progress", "fam-q"))
            series.append([h.get("committed_at"), round(100.0 * u[0] / u[1], 3) if u and u[1] else None,
                           round(o[0], 3) if o else None, (q[1] - q[0]) if q else None])
    except OSError:
        pass
    step = max(1, len(series) // 240)
    series = series[::step] + ([series[-1]] if series and (len(series) - 1) % step else [])
    fams = {x.split("=")[0]: int(x.split("=")[1]) for x in re.findall(r"\b(?:DA|DD|F|P)=\d+", " ".join(gg.get("detail", [])))}
    ms = [dict(pm[k], id=k) for k in ("union", "L1", "L2-specific", "L2-cumulative", "terminal") if k in pm]
    if pp.get("overall") is not None:
        ms.append(M("overall", "progress.py OVERALL (weighted depth)", round(pp["overall"], 2), 100, "progress.py", "progress.py --json", t,
                    "a weighted composite; see the Depth tab"))
    qo = sum(v.get("OPEN", 0) for _, v in sections); qp = sum(v.get("PARTIAL", 0) for _, v in sections)
    qtot = sum(sum(v.values()) for _, v in sections)
    ms.append(M("register-closed", "register rows neither OPEN nor PARTIAL", qtot - qo - qp, qtot, "OPEN-QUESTIONS.md", "check_questions.classify", t,
                "a row's lead word decides its state, as the goal gate reads it"))
    return {"view": "glance", "title": "At a glance", "status": "OK", "page": "glance",
            "source": {"identity": "goal gate %s; board rev %s; facts %s" % (gg.get("verdict"), board.get("revision"), sha12(inp["requirement_facts"])),
                       "as_of": t, "instrument": "build_views.v_glance",
                       "limits": "one page over the same inputs as the other tabs; lanes count board records and commit subjects, not effort"},
            "measures": ms,
            "glance": {"verdict": gg.get("verdict"), "remaining": gg.get("remaining"), "next": gg.get("next"), "detail": gg.get("detail", []),
                       "families_unmet": fams, "open": qo, "partial": qp, "sections": sections, "open_rows": open_rows[:60],
                       "lanes": lanes, "ladder": ladder[:40], "audits": audits[:30], "verdicts": dict(verdicts),
                       "commits": commits[:40], "series": series}}


# Player progression (user request 2026-09-30, modelled on the Wizardry local server's tab): the game's content as a
# player meets it, from the game's own files (ff12_content.py), each family beside two measures - how much of the
# mechanism behind it the database explains (its My Progress category) and co-op support in XIIOnline (a ledger;
# unmeasured until it has rows, never zero).
JOURNEY = [
    ("world", "The world of Ivalice", "Regions, areas, locations and the maps inside them, with the enemies each map spawns.", "W"),
    ("story", "Story, events & hunts", "Enemy units the game's own data flags as hunts (its 'Is Hunt?' column, one row per area file). Cutscenes, scripted events and side quests are not yet catalogued.", "T"),
    ("party", "Party, guests & espers", "The playable characters, guests who join for a while, and the espers.", "P"),
    ("licences", "The License Board", "Every licence a character can learn.", "I"),
    ("abilities", "Magicks, technicks & skills", "Action names: magicks, technicks, items used in battle and enemy skills.", "C"),
    ("commands", "Battle commands", "The commands on the battle menu.", "C"),
    ("gambits", "Gambits", "The conditions a gambit can test.", "E"),
    ("statuses", "Status effects", "Every status a character or enemy can carry.", "C"),
    ("equipment", "Equipment", "Weapons, armour and accessories.", "I"),
    ("key_items", "Key items", "Items the story hands out.", "I"),
    ("bazaar", "The bazaar", "Goods the bazaar sells once their loot is traded.", "I"),
    ("loot", "Loot", "Loot dropped by enemies and traded at shops.", "I"),
    ("enemies", "Enemies & bestiary", "Enemy units by name - hunt marks, bosses and the rest - and the maps they appear on.", "E"),
]


def v_journey(inp, t):
    """Player progression - the Wizardry-style player-facing tab for FF12 (see JOURNEY). Reads the content catalogue
    captured this build, the My Progress category measures, and the co-op ledger."""
    prog = v_progress(inp, t)
    cat = {m["id"][4:]: m for m in prog["measures"] if m["id"].startswith("cat-")}
    try:
        c = json.load(open(inp["content"], encoding="utf-8"))
    except (OSError, ValueError, KeyError) as e:
        c = None
        why = "the content catalogue could not be read (%s); run ff12_content.py" % type(e).__name__
    coop = collections.defaultdict(lambda: collections.Counter())
    try:
        for line in open(inp["coop"], encoding="utf-8"):
            p = line.rstrip("\r\n").split("\t")
            if len(p) >= 3 and not line.startswith(("#", "family\t")):
                coop[p[0]][p[2].strip().upper()] += 1
    except (OSError, KeyError):
        pass
    fams, ms = [], []
    for fid, title, blurb, code in JOURNEY:
        cm = cat.get(code)
        und = {"accepted": cm["numerator"], "total": cm["denominator"], "category": code, "label": cm["label"]} if cm else None
        if cm:
            ms.append(M("u-" + fid, "%s - database understanding (My Progress category %s)" % (title, code), cm["numerator"], cm["denominator"],
                        "category " + code, "requirements.py via v_progress", t, "one category's requirements; a category can hold several families"))
        entries, count = [], None
        if c and fid == "world":
            w = c.get("world", {})
            count = len(w.get("maps", []))          # unplaced maps are among these, listed again by code
        elif c and fid == "story":
            entries = [e for e in (c.get("families") or {}).get("enemies", []) if e.get("isHunt")]
            count = len(entries)
        elif c and fid in (c.get("families") or {}):
            entries = c["families"][fid]
            count = len(entries)
        cv = coop.get(fid)
        fams.append({"id": fid, "title": title, "blurb": blurb, "count": count, "understanding": und,
                     "coop": ({"works": cv.get("WORKS", 0), "partial": cv.get("PARTIAL", 0), "broken": cv.get("BROKEN", 0),
                               "rows": sum(cv.values())} if cv else None),
                     "entries": [{k: e.get(k) for k in ("key", "name", "display", "kind", "genus", "maps", "blank", "duplicate", "placeholder", "isHunt", "isBoss")
                                 if k in e} for e in entries]})
    tree, _entries, links = journey_tree(c, {f["id"]: f for f in fams}) if c else (None, None, None)
    status = "OK" if c else "PARTIAL"
    src = "content %s (%s); facts %s" % (sha12(inp["content"]) if c else "missing", (c or {}).get("generated_at", "-"), sha12(inp["requirement_facts"]))
    return {"view": "journey", "title": "Player progression", "status": status, "page": "journey",
            "source": {"identity": src, "as_of": t, "instrument": "build_views.v_journey over ff12_content.py",
                       "limits": "names come from the game's own files; understanding is the family's My Progress category, not a per-item "
                                 "score; co-op support is unmeasured until _index/workflow/coop-support.tsv has rows" +
                                 ("" if c else "; " + why)},
            "measures": ms,
            "journey": {"tree": tree, "links": links, "controls": (c or {}).get("controls", []), "sources": (c or {}).get("sources", {}),
                        "recovered": {k: v.get("recovered") for k, v in ((c or {}).get("recovered") or {}).items()}
                        if isinstance((c or {}).get("recovered"), dict) else None}}


def v_journey_entries(inp, t):
    """The Player progression pages (each entry's sections, about text and modder block), a view of their own so the tab's
    tree loads light and the pages load once, when a reader first opens one. Not a tab (server.py HIDDEN)."""
    try:
        c = json.load(open(inp["content"], encoding="utf-8"))
    except (OSError, ValueError, KeyError) as e:
        return {"view": "journey_entries", "title": "Player progression pages", "status": "PARTIAL", "measures": [],
                "source": {"identity": "content missing", "as_of": t, "instrument": "build_views.v_journey_entries",
                           "limits": "the content catalogue could not be read (%s)" % type(e).__name__}, "entries": {}}
    _tree, entries, _links = journey_tree(c, {})
    return {"view": "journey_entries", "title": "Player progression pages", "status": "OK", "measures": [],
            "source": {"identity": "content %s (%s)" % (sha12(inp["content"]), c.get("generated_at", "-")), "as_of": t,
                       "instrument": "build_views.v_journey_entries over ff12_content.py",
                       "limits": "values appear only where a database page documents the field; enemy values come from the hub catalog"},
            "entries": entries}


# The Player progression tree (user request 2026-09-30: "nest ... organized based on its in game category and semantic
# reasoning", after the Wizardry tab's organize.py). Rules, as there: a group comes only from an explicit relationship in
# the game's data - the world map's region/area/location records, a map's spawn list, the party row kind, the hunt/boss
# flags, an authored category field (entry "group" from ff12_content.py) or an authored name prefix - never from a guessed
# order. Entries with the same name collapse into one item that lists every row; unused slots (No name / Reserve
# placeholders, blank names) go to their own "Unused slots" group instead of mixing with real content.
JOURNEY_TREE = [
    ("world", "The world", "Ivalice as the world map shows it: regions, their areas, and the maps inside each area.", ["world"]),
    ("party", "Characters", "Who fights for you: the main party, guests who join for a while, and the espers.", ["party"]),
    ("growth", "License Board", "What a character can learn: every licence on the board.", ["licences"]),
    ("battle", "Battle", "Everything used in a fight: the battle menu, actions, gambits and status effects.",
     ["commands", "abilities", "gambits", "statuses"]),
    ("items", "Items & equipment", "What you carry: equipment, loot, key items and bazaar goods.", ["equipment", "loot", "key_items", "bazaar"]),
    ("bestiary", "Bestiary", "Every enemy by name: bosses, hunt-flagged fights, by class and genus, and by the region where it appears.", ["enemies"]),
    ("story", "Story & quests", "The story's scenes, side quests and the hunt board. Not catalogued from the game files yet.", ["story"]),
]
SUB_TITLES = {"commands": ("Battle menu", "The commands on the battle menu."),
              "abilities": ("Actions", "Magicks, technicks, items used in battle and enemy skills - every named action."),
              "gambits": ("Gambits", "The targets and conditions a gambit can test."),
              "statuses": ("Status effects", "Every status a character or enemy can carry."),
              "equipment": ("Equipment", "Weapons, armour and accessories."),
              "loot": ("Loot", "Loot dropped by enemies and traded at shops."),
              "key_items": ("Key items", "Items the story hands out."),
              "bazaar": ("Bazaar goods", "Goods the bazaar sells once their loot is traded."),
              "augments": ("Augments", "The passive abilities licences grant, and what each one does.")}


def _jname(e):
    return (e.get("display") or e.get("name") or e.get("fallback_name") or "").strip()


def _jworld(s):
    """A world-map name for display: drops the 0x0F escape runs (colour codes) the menu text wraps some names in."""
    return re.sub(r"<0F>(?:<[0-9A-F]{2}>){0,3}", "", s or "").strip()


def _junused(e):
    return bool(e.get("placeholder") or e.get("blank") or not _jname(e))


def journey_tree(c, fams):
    """Build the nested Player progression tree from the content catalogue (see JOURNEY_TREE)."""
    F, w = c.get("families") or {}, c.get("world") or {}
    areas = {a["id"]: a for a in w.get("areas", [])}
    locs = {l["id"]: l for l in w.get("locations", [])}
    regions = {r["id"]: r for r in w.get("regions", [])}
    area_region = {a: r["id"] for r in w.get("regions", []) for a in r.get("areas", [])}
    rtitle = {}                                          # region id -> display name; a region without a readable name of its own
    for r in w.get("regions", []):                       # (the two airship regions) shows its areas' names
        rn = _jworld(r.get("name"))
        rtitle[r["id"]] = (rn if rn and not re.search(r"<[0-9A-F]{2}>", rn) else
                           " / ".join(_jworld((areas.get(a) or {}).get("name")) for a in r.get("areas", []) if a in areas) or "Region %d" % r["id"])
    place = {}                                            # map code -> (region name, area name, own location name)
    for m in w.get("maps", []):
        a = m.get("area")
        if a is None and m.get("location") is not None:
            a = (locs.get(m["location"]) or {}).get("area")
        l = locs.get(m.get("location"))
        place[m["mapCode"]] = (rtitle.get(area_region.get(a)), _jworld((areas.get(a) or {}).get("name")) or None,
                               (l.get("name") or "").strip() if l else "")
    enemies = F.get("enemies", [])
    ename = {e["key"]: _jname(e) for e in enemies}
    ebyname = collections.defaultdict(list)
    for e in enemies:
        ebyname[_jname(e)].append(e)
    area_node = {_jworld(a.get("name")): "area-%d" % a["id"] for a in w.get("areas", []) if _jworld(a.get("name"))}

    def meas(fids):
        und, seen, coop = {"accepted": 0, "total": 0, "labels": []}, set(), None
        for fid in fids:
            f = fams.get(fid) or {}
            u = f.get("understanding")
            if u and u["category"] not in seen:
                seen.add(u["category"]); und["accepted"] += u["accepted"]; und["total"] += u["total"]; und["labels"].append(u["label"])
            if f.get("coop"):
                coop = coop or {"works": 0, "partial": 0, "broken": 0, "rows": 0}
                for k in coop: coop[k] += f["coop"].get(k, 0)
        return (und if seen else None), coop

    def node(nid, title, blurb, fids=(), basis=None, children=None, items=None, unit="entries", note=None, kids=None, sections=None):
        n = {"id": nid, "title": title, "blurb": blurb}
        if sections: n["sections"] = sections
        if kids: n["kids"] = kids                          # what the children are called on a card ("3 areas")
        if fids:
            n["und"], n["coop"] = meas(fids)
            if len(fids) == 1: n["mid"] = "u-" + fids[0]          # the measure carrying this node's pp delta
        if basis: n["basis"] = basis
        if note: n["note"] = note
        if children is not None:
            n["children"] = [ch for ch in children if ch]
            n["count"] = sum(ch.get("count") or 0 for ch in n["children"] if not ch["id"].endswith("-unused"))
            us = {ch.get("unit") for ch in n["children"] if not ch["id"].endswith("-unused")}
            n["unit"] = us.pop() if len(us) == 1 else "entries"
        if items is not None:
            n["items"] = items
            n["count"] = len(items)
            n["unit"] = unit
            if children is not None:                       # a list with side groups (its unused slots): the list sets the count
                n["count"] = len(items)
        return n

    def where(maps):
        regs, ars = [], []
        for mc in maps or []:
            r, a, _ = place.get(mc, (None, None, ""))
            if r and r not in regs: regs.append(r)
            if a and a not in ars: ars.append(a)
        return regs, ars

    entries = {}        # eid -> the page a player reads (sections, about) and the modder block (dev); stored once, however
                        # many lists show the entry (an enemy is listed under bosses, its family, its region and each area)

    def page(rs, facts_of=None):
        pg = {}
        secs = list(facts_of(rs)) if facts_of else []
        secs += [x for x in (rs[0].get("sections") or []) if x.get("entries")]
        for sec in secs:                               # one line per distinct fact ("Used by: Imperial Magus" once, not four times)
            seen, keep = set(), []
            for e in sec["entries"]:
                k = (e.get("label"), str(e.get("value")))
                if k not in seen:
                    seen.add(k); keep.append(e)
            sec["entries"] = keep
        if secs: pg["sections"] = secs
        if rs[0].get("about"): pg["about"] = rs[0]["about"]
        pg["dev"] = {"keys": [e["key"] for e in rs]}
        if rs[0].get("group_basis"): pg["dev"]["grouped_by"] = rs[0]["group_basis"]
        rows_dev = [e["dev"] for e in rs if e.get("dev")]
        if rows_dev: pg["dev"]["rows"] = rows_dev
        if rs[0].get("group") is None and rs[0].get("group_raw") is not None:
            pg["dev"]["undocumented_category_value"] = rs[0]["group_raw"]
        return pg

    def collapse(rows, facts_of=None, sub_of=None, home=True, eid_of=None, full=None):
        """Rows with the same name become one item: {name, n, eid, sub?, home?}. Its page is entries[eid], built once from
        `full(name)` (every row of that name) when given, else from the rows listed here."""
        by = collections.OrderedDict()
        for e in rows:
            by.setdefault(_jname(e), []).append(e)
        out = []
        for name, rs in by.items():
            eid = eid_of(name, rs) if eid_of else rs[0]["key"]
            if eid not in entries:
                entries[eid] = page(full(name) if full else rs, facts_of)
            it = {"name": name, "n": len(rs), "eid": eid}
            if home: it["home"] = True
            if sub_of: it["sub"] = sub_of(rs)
            out.append(it)
        return out

    keyname = {e["key"]: _jname(e) for rows in F.values() for e in rows if isinstance(e, dict) and e.get("key")}
    E = lambda label, value, link=None: dict({"label": label, "value": value}, **({"link": link} if link else {}))

    def extra(fid, rs):
        """Summary facts a family's rows carry beyond their name, until the extractor's own sections cover them."""
        e, out = rs[0], []
        if any(x.get("sections") for x in rs):
            return out
        if fid == "licences":
            ent = ([E("LP cost", ", ".join(str(x) for x in e["lp"]))] if e.get("lp") else []) + \
                  [E("Grants", keyname.get(k, k), k) for k in e.get("grants") or []]
            if ent: out.append({"title": "Licence", "entries": ent})
        if fid == "bazaar":
            ent = [E("Gives", "%s x%d" % (g.get("name") or g.get("key"), g.get("count", 1)), g.get("key")) for g in e.get("gives") or []]
            if "repeatable" in e: ent.append(E("Can be bought again", "yes" if e["repeatable"] else "no, once only"))
            if ent: out.append({"title": "Bazaar", "entries": ent})
        return out

    def plain(rows, fid=None):
        return collapse(rows, facts_of=(lambda rs: extra(fid, rs)) if fid else None)

    def unused(fid, rows):
        u = [e for e in rows if _junused(e)]
        if not u: return None
        return node(fid + "-unused", "Unused slots", "Rows the game reserves but leaves empty (No name / Reserve placeholders, blank names).",
                    basis="the row is a placeholder or has no name", unit="slots",
                    items=[unused_item(e) for e in u])

    def unused_item(e):
        entries.setdefault(e["key"], {"dev": {"keys": [e["key"]]}})
        return {"name": _jname(e) or "(blank)", "n": 1, "unused": True, "eid": e["key"], "home": True}

    def enemy_items(rows, home=False):
        def facts(rs):
            maps = sorted({m for e in rs for m in e.get("maps") or []})
            ars = []
            for mc in maps:
                a = place.get(mc, (None, None, ""))[1]
                if a and a not in [x[0] for x in ars]: ars.append((a, area_node.get(a)))
            gn = sorted({e.get("genus_name") for e in rs if e.get("genus_name")})
            cl = sorted({glabel("enemies", e["group"][0]) for e in rs if e.get("group")})
            fl = [x for x, k in (("Boss", "isBoss"), ("Hunt", "isHunt")) if any(e.get(k) for e in rs)]
            prof = ([E("Class", ", ".join(cl))] if cl else []) + ([E("Genus", ", ".join(gn))] if gn else []) + \
                   ([E("Marked as", ", ".join(fl))] if fl else [])
            out = [{"title": "Profile", "entries": prof}] if prof and not any(e.get("sections") for e in rs) else []
            where_ = [E("Area", a, ("node:" + nid) if nid else None) for a, nid in ars]
            if len(rs) > 1: where_.append(E("Separate encounters in the game's data", len(rs)))
            if not ars: where_.append(E("Area", "not placed on the world map yet"))
            out.append({"title": "Where to find it", "entries": where_})
            return out
        return collapse(rows, facts_of=facts, sub_of=lambda rs: ", ".join(where(sorted({m for e in rs for m in e.get("maps") or []}))[1][:3]),
                        home=home, eid_of=lambda name, rs: "enemy:" + name, full=lambda name: ebyname.get(name, []))

    def by_region(fid, rows, what):
        """One child per region an enemy appears in (an enemy in two regions is listed under both)."""
        groups = collections.OrderedDict((rtitle[r["id"]], []) for r in w.get("regions", []))
        groups["Not yet placed on the world map"] = []
        for e in rows:
            regs = where(e.get("maps"))[0] or ["Not yet placed on the world map"]
            for r in regs: groups[r].append(e)
        return [node("%s-%s" % (fid, re.sub(r"[^a-z0-9]+", "-", r.lower()).strip("-")), r, "%s that appear in %s." % (what, r),
                     basis="the maps each unit spawns on, placed by the world map", unit="names", items=enemy_items(rs))
                for r, rs in groups.items() if rs]

    def natural(codes):
        """Codes like class:3 / lg:0x15 sort in the game's own numeric order."""
        def k(c):
            m = re.match(r"^[a-z_]+:(0x[0-9a-fA-F]+|\d+)$", str(c))
            return (0, int(m.group(1), 0)) if m else (1, 0)
        return sorted(codes, key=k) if all(re.match(r"^[a-z_]+:(0x[0-9a-fA-F]+|\d+)$", str(c)) for c in codes if c not in LAST) else list(codes)

    # Friendlier titles for authored groups whose label only lists their members (a rename, never a regroup).
    TITLE = {("equipment", "rc:1"): "Unarmed", ("equipment", "rc:2"): "One-handed weapons", ("equipment", "rc:3"): "Two-handed melee weapons",
             ("equipment", "rc:4"): "Ranged weapons", ("equipment", "rc:5"): "Ammunition", ("equipment", "rc:6"): "Shields",
             ("equipment", "rc:7"): "Helms", ("equipment", "rc:8"): "Body armour", ("equipment", "rc:9"): "Accessories"}
    NOTYET, OTHER = "\x00notyet", "\x00other"
    LAST = (NOTYET, OTHER, "kind:unused")

    def glabel(fid, code):
        if code == NOTYET: return "Not yet classified"
        if code == OTHER: return "Other"
        if (fid, code) in TITLE: return TITLE[(fid, code)]
        lab = re.sub(r"\s*\(ids [^)]*\)", "", ((c.get("groups") or {}).get(fid) or {}).get(code, code))
        if re.search(r"<[0-9A-F]{2}>", lab) or not lab.strip():          # the game's text has no readable name for it
            return "Unnamed group (%s)" % code.split(":")[-1]
        return lab

    def slug(*parts):
        return "-".join(re.sub(r"[^a-z0-9]+", "-", str(x).lower()).strip("-") or "x" for x in parts)

    def notyet_note(fid):
        u = (c.get("notes") or {}).get(fid + "_undocumented_kinds") or {}
        vals = sorted(((v.get("rows", 0), k, v.get("command_list_row_name")) for k, v in (u.get("values") or {}).items()), reverse=True)
        if not vals: return None
        return ("The game gives these rows a category value no database page explains yet, so they are not grouped. Unverified lead: "
                "the command list row with the same number names " + "; ".join("value %s '%s' (%d rows)" % (k, nm, n) for n, k, nm in vals[:3]) + ".")

    def grouped(fid, rows, items_fn=None):
        """Children from the entry's authored group ([top, sub] codes + group_basis, from ff12_content.py). group None = the
        field's value is undocumented ("Not yet classified"); [] = the entry has no category ("Other"). None when the
        family has no grouping at all."""
        live = [e for e in rows if not _junused(e)]
        if not any(e.get("group") for e in live): return None
        items_fn = items_fn or (lambda rs: plain(rs, fid))
        top = collections.OrderedDict()
        for e in live:
            g = e.get("group")
            k = tuple(g) if g else ((NOTYET,) if g is None else (OTHER,))
            top.setdefault(k[0], []).append((e, k))
        for code in natural(list(top)):
            top.move_to_end(code)
        for code in LAST:
            if code in top: top.move_to_end(code)
        out = []
        for code, eks in top.items():
            rs = [e for e, _ in eks]
            basis = next((e.get("group_basis") for e in rs if e.get("group") and e.get("group_basis")), None)
            note = notyet_note(fid) if code == NOTYET else None
            blurb = ("Rows whose category value has no documented meaning yet." if code == NOTYET else
                     "Rows with no category field." if code == OTHER else "")
            subs = collections.OrderedDict()
            for e, k in eks:
                subs.setdefault(k[1] if len(k) > 1 else None, []).append(e)
            for sc in natural([x for x in subs if x is not None]):
                subs.move_to_end(sc)
            if len(subs) > 1:
                n = node(slug(fid, code), glabel(fid, code), blurb, basis=basis, note=note, kids="groups",
                         children=[node(slug(fid, code, sc or "other"), glabel(fid, sc) if sc else "Other", "", basis=basis, items=items_fn(ss))
                                   for sc, ss in subs.items()])
            else:
                n = node(slug(fid, code), glabel(fid, code), blurb, basis=basis, note=note, items=items_fn(rs))
            out.append(n)
        return out

    def family(fid):
        rows = F.get(fid, [])
        title, blurb = SUB_TITLES[fid]
        g = grouped(fid, rows)
        if g:
            return node(fid, title, blurb, [fid], children=g + [unused(fid, rows)], kids="groups")
        u = unused(fid, rows)
        return node(fid, title, blurb, [fid], items=plain([e for e in rows if not _junused(e)], fid), children=[u] if u else None)

    # The world: region -> area -> maps (listed under their location when the location has its own name).
    def map_item(m):
        names = []
        for k in m.get("enemies") or []:
            if ename.get(k) and ename[k] != "No name" and (ename[k], k) not in names: names.append((ename[k], k))
        seen, uniq = set(), []
        for nm, k in names:
            if nm not in seen: seen.add(nm); uniq.append((nm, k))
        _, _, ln = place.get(m["mapCode"], (None, None, ""))
        secs = [{"title": "Enemies here", "entries": [E("Enemy", nm, k) for nm, k in uniq]}] if uniq else []
        secs += [x for x in (m.get("sections") or []) if x.get("entries")]
        eid = "map:" + m["mapCode"]
        entries[eid] = dict({"sections": secs} if secs else {}, dev=dict({"keys": [m["mapCode"]], "map": m.get("mapCode"),
                                                                           "areaId": m.get("areaId")}, **(m.get("dev") or {})))
        return {"name": m["mapCode"], "n": 1, "mono": True, "group": ln or None, "eid": eid, "home": True,
                "sub": ", ".join(x[0] for x in uniq[:4]) + (" +%d" % (len(uniq) - 4) if len(uniq) > 4 else "")}
    maps_by_area = collections.defaultdict(list)
    for m in w.get("maps", []):
        a = m.get("area")
        if a is None and m.get("location") is not None:
            a = (locs.get(m["location"]) or {}).get("area")
        maps_by_area[a].append(m)
    reg_nodes = []
    for r in w.get("regions", []):
        an = []
        for aid in r.get("areas", []):
            a = areas.get(aid)
            if not a: continue
            ms = maps_by_area.get(aid, [])
            its = sorted((map_item(m) for m in ms), key=lambda i: (i["group"] is None, i["group"] or "", i["name"]))
            ekeys = {k for m in ms for k in m.get("enemies") or []}
            here = [e for e in enemies if e["key"] in ekeys and not _junused(e) and _jname(e) != "No name"]
            travel = [E("Next to it on the world map", _jworld((areas.get(x) or {}).get("name")) or "area %d" % x, "node:area-%d" % x)
                      for x in dict.fromkeys(a.get("links") or []) if x in areas]
            travel.append(E("Airship (Strahl) can land here", "yes" if a.get("strahl") else "no"))
            places = [E("Place", (locs[l].get("name") or "").strip()) for l in a.get("locations") or [] if l in locs and (locs[l].get("name") or "").strip()]
            secs = [{"title": "Travel", "entries": travel}] + ([{"title": "Places in this area", "entries": places}] if places else [])
            mapsn = node("area-%d-maps" % aid, "Maps", "The game's map files for this area, with the enemies each one spawns.", unit="maps", items=its,
                         basis="each map's placement on the world map")
            an_node = node("area-%d" % aid, _jworld(a["name"]), "Enemies found here, where it leads, and its maps.", unit="enemies",
                           items=enemy_items(here), children=[mapsn], sections=secs, kids="groups",
                           basis="the world map's area record and each map's placement")
            an_node["count"], an_node["unit"] = len(ms), "maps"          # the world counts maps; the page lists the enemies
            an.append(an_node)
        own = rtitle[r["id"]] == _jworld(r.get("name"))
        reg_nodes.append(node("region-%d" % r["id"], rtitle[r["id"]],
                              "" if own else "This region record has no readable name of its own; its area's name is shown.",
                              basis="the world map's region record", children=an, kids="areas"))
    un = [m for m in w.get("maps", []) if m.get("area") is None and m.get("location") is None]
    if un:
        reg_nodes.append(node("region-unplaced", "Not yet placed", "Maps the world map does not place in any area.", unit="maps",
                              basis="no world-map record names this map", items=[map_item(m) for m in un]))
    world = node("world", "The world", JOURNEY_TREE[0][2], ["world"], children=reg_nodes, kids="regions")
    world["unit"] = "maps"

    # Characters: the party row kind.
    party = F.get("party", [])
    kinds = [("main", "Main party", "The six who travel with you."), ("guest", "Guests", "Characters who join for part of the story; a name "
             "can hold several rows, one per stint."), ("esper", "Espers", "The summons, one row each.")]
    chars = node("party", "Characters", JOURNEY_TREE[1][2], ["party"], basis="the party row kind (ff12_content.py notes)",
                 children=[node("party-" + k, t, b, unit="names", items=plain([e for e in party if e.get("kind") == k and not _junused(e)]))
                           for k, t, b in kinds] +
                          [node("party-other", "Other rows", "Named rows outside the three kinds (for example the chocobo).", unit="names",
                                items=plain([e for e in party if e.get("kind") not in ("main", "guest", "esper") and not _junused(e)])) if
                           any(e.get("kind") not in ("main", "guest", "esper") and not _junused(e) for e in party) else None, unused("party", party)])

    def augments_node():
        n = family("augments")
        n["basis"] = "the augment table, a family of its own beside the licences that grant each augment"
        return n

    lic = F.get("licences", [])
    lg = grouped("licences", lic)
    growth = node("growth", "License Board", JOURNEY_TREE[2][2], ["licences"],
                  children=lg + [unused("licences", lic)] + ([augments_node()] if F.get("augments") else []), kids="groups") if lg else node("growth", "License Board", JOURNEY_TREE[2][2], ["licences"],
                                                                           items=plain([e for e in lic if not _junused(e)], "licences"),
                                                                           note="Grouping by licence kind needs the licence table's kind field.")
    battle = node("battle", "Battle", JOURNEY_TREE[3][2], JOURNEY_TREE[3][3], children=[family(f) for f in JOURNEY_TREE[3][3]], kids="sections")
    items = node("items", "Items & equipment", JOURNEY_TREE[4][2], JOURNEY_TREE[4][3], children=[family(f) for f in JOURNEY_TREE[4][3]], kids="sections")

    named = [e for e in enemies if not _junused(e) and _jname(e) != "No name"]
    bosses = [e for e in named if e.get("isBoss")]
    hunts = [e for e in named if e.get("isHunt") and not e.get("isBoss")]
    distinct = lambda rows: len({_jname(e) for e in rows})

    def flagged(nid, title, blurb, basis, rows):
        n = node(nid, title, blurb, basis=basis, unit="names", children=by_region(nid, rows, title), kids="regions")
        n["count"] = distinct(rows)                        # a name in two regions is listed twice, counted once
        return n
    fam_nodes = grouped("enemies", named, items_fn=lambda rs: enemy_items(rs, home=True))
    if fam_nodes:
        kinds_node = node("bestiary-kinds", "By family", "Every enemy by its class and genus, the way the bestiary sorts them.", unit="names",
                          children=fam_nodes, kids="classes")
        kinds_node["count"] = distinct(named)
    else:
        kinds_node = None
    regions_node = flagged("bestiary-regions", "By region", "Every enemy by the region where it appears.", None, named)
    nameless = [e for e in enemies if e not in named]
    bestiary = node("bestiary", "Bestiary", JOURNEY_TREE[5][2], ["enemies"], kids="views", children=[
        flagged("bestiary-bosses", "Bosses", "Units the catalogue flags as bosses: story fights, espers and the strongest marks.",
                "the hub enemy catalogue's 'Is Boss?' column", bosses),
        flagged("bestiary-hunts", "Flagged as hunt", "Units the catalogue flags as hunts and not as bosses. The flag is wider than the hunt "
                "board: it also marks trial and story fights.", "the hub enemy catalogue's 'Is Hunt?' column", hunts),
        kinds_node, regions_node,
    ] + [node("bestiary-unused", "Unused slots", "Units with no name in the game's text (\"No name\").", unit="slots",
                    basis="the unit's name is a placeholder", items=enemy_items(nameless)) if nameless else None])
    bestiary["count"], bestiary["unit"] = distinct(named), "names"
    story = node("story", "Story & quests", JOURNEY_TREE[6][2], ["story"], unit="entries", items=[],
                 note="Story scenes, side quests and the hunt board are not catalogued from the game files yet. The event scripts decode per "
                      "map (ff12-script); a scene and quest catalogue is the next step. Fights the game flags as bosses or hunts are in the Bestiary.")
    story["count"] = None
    root = node("root", "All categories", "", children=[world, chars, growth, battle, items, bestiary, story], kids="categories")
    # links: catalogue key -> [node id, item index] of the entry's home listing (a map code links to its map entry)
    links = {}

    def homes(n):
        for i, it in enumerate(n.get("items") or []):
            for k in [it.get("eid")] + ((entries.get(it.get("eid")) or {}).get("dev", {}).get("keys") or []):
                if k and (it.get("home") or k not in links):
                    links[k] = [n["id"], i]
        for ch in n.get("children") or []:
            homes(ch)
    homes(root)
    # the extractor's world links (area:N / region:N / location:N) open the world tree's own pages
    tree_ids = set()

    def ids(n):
        tree_ids.add(n["id"])
        for ch in n.get("children") or []:
            ids(ch)
    ids(root)
    for a in areas:
        if "area-%d" % a in tree_ids: links["area:%d" % a] = ["area-%d" % a, None]
    for r in regions:
        if "region-%d" % r in tree_ids: links["region:%d" % r] = ["region-%d" % r, None]
    for l, lo in locs.items():
        if "area-%s" % lo.get("area") in tree_ids: links["location:%d" % l] = ["area-%s" % lo.get("area"), None]
    return root, entries, links


ADAPTERS = {"progress": v_progress, "depth": v_depth, "glance": v_glance, "journey": v_journey, "journey_entries": v_journey_entries, "overview": v_overview, "systems": v_systems, "vbf": v_vbf, "executable": v_executable, "types": v_types,
            "evidence": v_evidence, "fleet": v_fleet}


def category_tree(path):
    out = []
    for c in sorted(os.listdir(DB)):
        p = os.path.join(DB, c)
        if not os.path.isdir(p) or not re.match(r"^\d\d-", c): continue
        subs = [{"name": s, "docs": sum(len([f for f in fs if f.endswith(".md")]) for _, _, fs in os.walk(os.path.join(p, s)))}
                for s in sorted(os.listdir(p)) if os.path.isdir(os.path.join(p, s))]
        out.append({"name": c, "docs": sum(len([f for f in fs if f.endswith(".md")]) for _, _, fs in os.walk(p)), "subs": subs})
    json.dump(out, open(path, "w", encoding="utf-8"), indent=0)


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--root", default=os.path.join(TOOLS, "work", "dashboard"))
    ap.add_argument("--every", type=int, default=0, help="rebuild every N seconds (a stop-gap until the controller schedules it)")
    a = ap.parse_args(argv)
    if a.every:
        import time
        while True:            # a failed build keeps the last good generation; FAILURE.json records why
            try:
                build_once(a)
            except Exception as e:
                print("%s build failed: %s" % (NOW(), e), flush=True)
            time.sleep(max(60, a.every))
    return build_once(a)


def build_once(a):
    """One full reconciliation. `building.json` in the store root marks it in progress for the refresh countdown."""
    os.makedirs(a.root, exist_ok=True)
    mark = os.path.join(a.root, "building.json")
    import time as _time
    open(mark, "w", encoding="utf-8").write(json.dumps({"started": _time.time(), "pid": os.getpid()}))
    try:
        return _build_once(a)
    finally:
        try:
            os.remove(mark)
        except OSError:
            pass


def _build_once(a):
    cap = os.path.join(a.root, "_capture"); os.makedirs(cap, exist_ok=True)
    t = NOW()
    import time as _time
    inst = {}                      # exit code, seconds and start time of each captured instrument (Evidence & lessons cards)

    def timed(name, argv):
        t0, at = _time.time(), NOW()
        r = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
        inst[name] = {"exit": r.returncode, "seconds": round(_time.time() - t0, 1), "ran_at": at}
        return r
    r = timed("goal_gate", [sys.executable, os.path.join(GS, "goal_gate.py"), "--db", DB, "--json"])
    open(os.path.join(cap, "goal_gate.json"), "w", encoding="utf-8").write(r.stdout)
    r = timed("check_questions", [sys.executable, os.path.join(GS, "check_questions.py"), "--db", DB])
    open(os.path.join(cap, "check_questions.txt"), "w", encoding="utf-8").write(r.stdout)
    category_tree(os.path.join(cap, "category_tree.json"))
    r = timed("progress_check", [sys.executable, os.path.join(DB, "_index", "progress", "progress_report.py"), "check", "--db", DB])
    open(os.path.join(cap, "progress_check.txt"), "w", encoding="utf-8").write((r.stdout + r.stderr).strip() + "\n")
    open(os.path.join(cap, "instruments.json"), "w", encoding="utf-8").write(json.dumps(inst, indent=1))
    # the Evidence & lessons tab's verification checks: a curated set of read-only checkers (run_checks.CHECKS), in
    # parallel; a failed run leaves no record, and every card then reads UNMEASURED rather than a previous build's verdict
    try:
        os.remove(os.path.join(cap, "checks.json"))
    except OSError:
        pass
    try:
        subprocess.run([sys.executable, "-B", os.path.join(HERE, "run_checks.py"), "--db", DB, "--out", os.path.join(cap, "checks.json")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    except subprocess.TimeoutExpired:
        pass
    r = subprocess.run([sys.executable, os.path.join(HERE, "requirements.py"), "--db", DB, "--out", os.path.join(cap, "requirement_facts.json"),
                        "--residual", os.path.join(TOOLS, "work", "verify_GFZ_PARENT", "residual_addrs.txt")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    if r.returncode != 0:          # the facts file keeps its previous bytes; the view reports the failure rather than stale facts
        open(os.path.join(cap, "requirement_facts.json"), "w", encoding="utf-8").write(json.dumps(
            {"version": "MP-1", "facts": [], "failed": {"collect": (r.stderr or r.stdout)[-300:]}, "excluded": []}))
    # the installed VBF archive's header, every build (header only; a missing archive is a recorded failure, not the old listing)
    subprocess.run([sys.executable, os.path.join(HERE, "vbf_index.py"), "--listing", os.path.join(TOOLS, "work", "repos-2d", "vbf_list.txt"),
                    "--db", DB, "--out", os.path.join(cap, "vbf_index.json")], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    subprocess.run([sys.executable, os.path.join(HERE, "evidence_scan.py"), "--db", DB, "--out", os.path.join(cap, "evidence_scan.json")],
                   capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    # progress.py's weighted depth score for the Depth tab (user request 2026-09-30); a failed run leaves no file and the view says FAILED
    try:
        os.remove(os.path.join(cap, "progress_py.json"))
    except OSError:
        pass
    subprocess.run([sys.executable, os.path.join(GS, "progress.py"), "--db", DB, "--json", os.path.join(cap, "progress_py.json")],
                   capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    # Player progression's content catalogue (ff12_content.py), re-extracted only when the extractor, the installed archive or
    # the hub's enemy catalog changes; a failed extraction leaves no file and the tab says PARTIAL
    ex = os.path.join(HERE, "ff12_content.py")
    if os.path.isfile(ex):
        cc, stamp_p = os.path.join(cap, "ff12_content.json"), os.path.join(cap, "ff12_content.stamp")
        vbf = os.environ.get("FFXII_VBF", "D:/FFXII MP Mod/FFXII_TestClient1/FFXII_TZA.vbf")
        hub = os.path.join(os.path.dirname(DB), "..", "XIIOnlineHub", "XIIOnlineHub", "Assets", "enemies", "enemy_catalog.json")
        st_ = lambda p: "%d:%d" % (os.stat(p).st_size, os.stat(p).st_mtime) if os.path.exists(p) else "-"
        stamp = "%s %s %s" % (sha12(ex), st_(vbf), st_(hub))
        try:
            old = open(stamp_p, encoding="utf-8").read()
        except OSError:
            old = ""
        if old != stamp or not os.path.isfile(cc):
            try:
                os.remove(cc)
            except OSError:
                pass
            r = subprocess.run([sys.executable, ex, "--out", cc], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
            if r.returncode == 0 and os.path.isfile(cc):
                open(stamp_p, "w", encoding="utf-8").write(stamp)
    # recent commits for the At a glance tab (subject prefixes name the identity)
    r = subprocess.run(["git", "-C", DB, "log", "-200", "--format=%h%x09%aI%x09%s"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    open(os.path.join(cap, "gitlog.txt"), "w", encoding="utf-8").write(r.stdout)
    inputs = declare_inputs(cap)
    I = os.path.join(DB, "_index")
    st = G.Store(a.root)
    for attempt in range(3):          # a strict input moved mid-build: retry briefly; the failure is recorded each time
        try:
            return _build(st, inputs, t, I)
        except G.GenerationError as e:
            if "inputs moved" not in str(e) or attempt == 2:
                raise
            print("retrying after: %s" % e, flush=True)


def declare_inputs(cap):
    """Every input a view reads, by name. A test may redirect one; adapters only ever see the snapshots. Code a view
    consumes is an input too: requirements.py, this file, and uc1_band.py, bound at the path of the module actually
    imported (ASTRA c7bd09b49: generations before 2026-09-29 bound the builder but not the helper text_intervals calls, so
    their manifests prove the builder's identity only - their helper identity is unrecorded, never inferred)."""
    import uc1_band
    I = os.path.join(DB, "_index"); UC = os.path.join(DB, "99-Unresolved-Residual", "Unlisted-Code")
    inputs = {"goal_gate": {"path": os.path.join(cap, "goal_gate.json")}, "check_questions": {"path": os.path.join(cap, "check_questions.txt")},
              "_tree": {"path": os.path.join(cap, "category_tree.json")},
              "progress_snapshot": {"path": os.path.join(I, "progress", "snapshot.json"), "volatile": True},
              "progress_check": {"path": os.path.join(cap, "progress_check.txt")},
              "subsystems": {"path": os.path.join(I, "important-subsystems.tsv")}, "l2": {"path": os.path.join(I, "L2-VERDICTS.md")},
              "vbf_list": {"path": os.path.join(TOOLS, "work", "repos-2d", "vbf_list.txt")},
              "vbf_index": {"path": os.path.join(cap, "vbf_index.json")},          # the installed archive's own index, read every build
              "vbf_index.py": {"path": os.path.join(HERE, "vbf_index.py")},
              "evidence_scan": {"path": os.path.join(cap, "evidence_scan.json")},    # seal.py receipts + live propagation markers, every build
              "evidence_scan.py": {"path": os.path.join(HERE, "evidence_scan.py")},
              "progress_py": {"path": os.path.join(cap, "progress_py.json"), "required": False},  # progress.py --json, every build (Depth tab)
              "progress.py": {"path": os.path.join(GS, "progress.py")},
              # the At a glance tab (DWNO layout): the register itself, recent commits, and the dashboard's own measure history
              "register": {"path": os.path.join(I, "OPEN-QUESTIONS.md"), "volatile": True},
              "check_questions.py": {"path": os.path.join(GS, "check_questions.py")},
              # Evidence & lessons (v3): the mistakes ledger, the instrument findings index, the checker run and the times of
              # the captured instruments, the accepted checker baseline, the archive format census; and the code they use
              "contradictions": {"path": os.path.join(I, "CONTRADICTIONS.tsv")},
              "rules": {"path": os.path.join(I, "RULES.md")},
              # volatile: per-build records (run times and seconds differ on every run, and the next build rewrites them
              # before its own snapshot), read only from this generation's snapshot; strict, they would mark every tab
              # STALE for the whole of each following build
              "checks": {"path": os.path.join(cap, "checks.json"), "required": False, "volatile": True},
              "instruments": {"path": os.path.join(cap, "instruments.json"), "required": False, "volatile": True},
              "gate_baseline": {"path": os.path.join(I, "gate-baseline.tsv"), "required": False},
              "format_census": {"path": os.path.join(TOOLS, "work", "formats", "archive-extension-census.tsv")},
              "run_checks.py": {"path": os.path.join(HERE, "run_checks.py")},
              "goal_gate.py": {"path": os.path.join(GS, "goal_gate.py")},
              "gitlog": {"path": os.path.join(cap, "gitlog.txt")},
              # Player progression: the content catalogue from the game's files (ff12_content.py) and the co-op ledger
              "content": {"path": os.path.join(cap, "ff12_content.json"), "required": False},
              "ff12_content.py": {"path": os.path.join(HERE, "ff12_content.py"), "required": False},
              "coop": {"path": os.path.join(I, "workflow", "coop-support.tsv"), "required": False},
              "history": {"path": os.path.join(os.path.dirname(cap), HISTORY_MEASURES), "volatile": True, "required": False},
              "coverage_dims": {"path": os.path.join(I, "COVERAGE-DIMENSIONS.md")},
              "functions": {"path": os.path.join(TOOLS, "work", "graph", "functions.tsv")},
              "exe": {"path": os.path.join(TOOLS, "work", "exe", "FFXII_TZA.exe"), "snapshot": False},   # certified image: hashed, never copied or exported
              "extent_errata": {"path": os.path.join(DB, "_index", "FUNCTION-EXTENT-ERRATA.tsv")},
              # every applied UC-1 band the population library reads (uc1_band.BAND_TSVS), not a fixed list: a third band
              # (257-up, 2026-09-30) was invisible to the dashboard while it hard-coded the first two
              **{"uc1_band_%d" % k: {"path": os.path.abspath(p)} for k, p in enumerate(uc1_band.BAND_TSVS)},
              "types": {"path": os.path.join(DB, "_types", "types.tsv")}, "fields": {"path": os.path.join(DB, "_types", "fields.tsv")},
              "team": {"path": os.path.join(I, "_inbox", "TEAM.json"), "volatile": True},        # written every few seconds
              "watchdog": {"path": os.path.expandvars(os.path.join("%USERPROFILE%", ".swe2-fleet", "watchdog-state.json")), "required": False, "volatile": True},
              "requirement_facts": {"path": os.path.join(cap, "requirement_facts.json")},
              "category_map": {"path": os.path.join(I, "workflow", "my-progress", "category-map.tsv")},
              "requirements.py": {"path": os.path.join(HERE, "requirements.py")},
              "build_views.py": {"path": os.path.abspath(__file__)}, "uc1_band.py": {"path": os.path.abspath(uc1_band.__file__)}}
    for p in sorted(glob.glob(os.path.join(I, "completion-packages", "PKG-*.md"))):
        inputs["pkg:" + os.path.basename(p)] = {"path": p}
    return inputs


# Each view's DEFINITION version: a delta is numeric only between two generations whose view carries the same version,
# the same measure id, scope and denominator. Bump a view's version whenever its counting rule changes.
DEFINITIONS = {"progress": None, "depth": "v1", "glance": "v1", "journey": "v3", "journey_entries": "v1", "overview": "v1", "systems": "v1", "vbf": "v2", "executable": "v4", "types": "v1",
               "evidence": "v3", "fleet": "v1"}
HISTORY_MEASURES = "measures-history.jsonl"
# Which way is progress, per measure (FABLE-REQ-OPUS-DELTA-COLOUR-DIRECTION): "up" (a rise is progress), "down" (a rise
# is regression: open rows, false completions, unknown bytes) or "none" (a population with no good direction). A delta's
# colour follows it; "none" is muted whatever the sign; a measure with no entry is "none", never "up".
# test_build_views B7 fails when an overview, executable or progress measure has no entry.
DIRECTIONS = {
    'progress': {
        'union': 'up', 'L1': 'up', 'L2': 'up', 'L2-specific': 'up', 'L2-cumulative': 'up', 'union-exf': 'up', 'terminal': 'up', 'fam-q': 'up', 'fam-f': 'up',
        'fam-dd': 'up', 'fam-da': 'up', 'fam-dv': 'up', 'fam-r': 'up', 'fam-x': 'up', 'fam-e': 'up', 'fam-k': 'up',
        'fam-l2': 'up', 'fam-t': 'up', 'cat-W': 'up', 'cat-C': 'up', 'cat-E': 'up', 'cat-S': 'up', 'cat-P': 'up',
        'cat-I': 'up', 'cat-T': 'up', 'cat-M': 'up', 'cat-G': 'up', 'cat-V': 'up', 'cat-D': 'up', 'cat-N': 'up',
        'cat-whole': 'up', 'cat-untied': 'up', 'fam-p': 'down',
    },
    'journey': {
        'u-world': 'up', 'u-story': 'up', 'u-party': 'up', 'u-licences': 'up', 'u-abilities': 'up', 'u-commands': 'up',
        'u-gambits': 'up', 'u-statuses': 'up', 'u-equipment': 'up', 'u-key_items': 'up', 'u-bazaar': 'up', 'u-loot': 'up', 'u-enemies': 'up',
    },
    'glance': {
        'union': 'up', 'L1': 'up', 'L2': 'up', 'terminal': 'up', 'overall': 'up', 'register-closed': 'up',
    },
    'depth': {
        'overall': 'up', 'engine_explained': 'up', 'ledger_resolved': 'up', 'audit_coverage': 'up', 'registry_explained': 'up',
        'ebp_explained': 'up', 'formats_explained': 'up', 'questions_closed': 'up', 'final_audits': 'up',
    },
    'overview': {
        'register-answered': 'up', 'register-dispositioned': 'down', 'register-withdrawn': 'none',
        'register-partial': 'down', 'register-open': 'down', 'register-other': 'down', 'page-local': 'down',
        'transfers': 'none', 'pkg-false-complete': 'down', 'pkg-link-done': 'down', 'pkg-stage-mismatch': 'down',
    },
    'executable': {
        'behavior-a': 'up', 'behavior-b': 'up', 'behavior-c': 'none', 'behavior-none': 'down',
        'functions-a': 'up', 'functions-b': 'up', 'functions-c': 'none', 'functions-none': 'down',
        'bytes-listed': 'none', 'bytes-frontier': 'down', 'bytes-funclet': 'none', 'bytes-held': 'down',
        'bytes-fill': 'none', 'bytes-unknown': 'down', 'bytes-overlap': 'down', 'population': 'none',
        'compiler-template-generated': 'none', 'thunks': 'none', 'authored-functions-neither-': 'none',
        'authored-functions-with-a-semantic-name': 'up', 'authored-functions-with-an-owner-assigne': 'up',
        'authored-functions-cited-anywhere-in-a-s': 'up', 'authored-functions-in-a-document-s-key-a': 'up',
        'recorded-only-in-a-tsv-side-file-explain': 'down', 'edges-whose-caller-is-an-eh-funclet-hand': 'none',
        'authored-functions-with-1-non-eh-caller': 'none', 'of-those-having-at-least-one-writer': 'none',
        'of-those-cited-in-any-system-document': 'up', 'accesses-in-the-committed-artifact': 'none',
        'distinct-offsets': 'none', 'contributing-functions': 'none', 'types-in-the-store': 'none',
        'of-those-non-phyre': 'none', 'behavioural-contracts': 'up', 'of-those-at-contract-ready-or-beyond': 'up',
        'documents-citing-any-runtime-live-proces': 'up',
    },
    'evidence': {
        'reviews-done': 'up', 'reviews-accepted': 'up', 'reviews-structured': 'up', 'receipts-intact': 'up',
        'receipts-publishable': 'up', 'pending-propagation': 'down',
    },
    'systems': {
        'l2-met': 'up', 'categories': 'none',
    },
    'types': {
        'types': 'none', 'fields-resolved': 'up',
    },
    'vbf': {
        'files': 'none', 'bytes': 'none', 'extensions': 'none', 'listing-drift': 'down', 'formats-ext': 'up', 'formats-members': 'up',
    },
    'fleet': {
        'active': 'none',
    },
}


def undeclared(views, strict=("overview", "executable", "progress")):
    """[(view, id)] of measures in the strict views with no declared direction."""
    return [(n, m["id"]) for n, v in views.items() if n in strict for m in v.get("measures", [])
            if m["id"] not in DIRECTIONS.get(n, {})]


def prior_generation(st):
    """The immediately prior coherent generation: the newest entry of the success history that still VERIFIES
    (open_generation with its recorded manifest hash). Never a rejected candidate - those are not in the history.
    Returns (manifest, dir) or (None, None)."""
    hp = os.path.join(st.root, G.HISTORY)
    if not os.path.exists(hp):
        return None, None
    rows = [json.loads(l) for l in open(hp, encoding="utf-8") if l.strip()]
    for r in reversed(rows[-50:]):
        m, d, probs = st.open_generation(r.get("generation"), r.get("manifest_sha256"))
        if not probs:
            return m, d
    return None, None


def annotate_deltas(views, prior_dir, prior_man):
    """Percentage-point change of every measure with a denominator against the prior coherent generation:
    delta = 100*n/d - 100*pn/pd. Numeric only when the view's definition version, the measure id, its scope and its
    denominator are all unchanged; otherwise a labelled N/A with both sides and the reason (a denominator that grew is
    never shown as a regression, nor hidden as progress)."""
    for name, v in views.items():
        prev = None
        if prior_dir:
            pp = os.path.join(prior_dir, "outputs", "view-%s.json" % name)
            if os.path.exists(pp):
                try:
                    prev = json.load(open(pp, encoding="utf-8"))
                except ValueError:
                    prev = None
        v["delta_basis"] = {"generation": (prior_man or {}).get("generation"), "committed_at": (prior_man or {}).get("committed_at")}
        pm = {m["id"]: m for m in (prev or {}).get("measures", [])} if prev else {}
        for m in v.get("measures", []):
            o = pm.get(m["id"])
            # A plain count has denominator None; a ratio has a number, and 0 is a ratio with nothing in scope (0 of 0).
            # The two are never conflated, and a measure that moved between them gets no numeric change at all (ASTRA's
            # REJECT of eae0ed3c7, RESULT.md: 0/0 -> 5/null was shown as a count +5 and the prior basis rewritten to null).
            if o is not None and prev is not None and (o.get("denominator") is None) != (m.get("denominator") is None):
                m["delta"] = {"na": "N/A - basis changed", "why": "count/ratio basis changed: denominator %s -> %s" % (o.get("denominator"), m.get("denominator")),
                              "old": {"numerator": o.get("numerator"), "denominator": o.get("denominator")},
                              "new": {"numerator": m.get("numerator"), "denominator": m.get("denominator")}}
                continue
            if m.get("denominator") is None:
                # A count with no denominator (files, bytes, active tasks, types) still changes between refreshes: its
                # signed change and relative change, on the same like-for-like basis (definition, id, scope unchanged).
                # A count is never turned into a percentage of completion (user request 2026-09-29: a change on every tile).
                if not isinstance(m.get("numerator"), (int, float)):
                    continue
                newc = {"numerator": m["numerator"], "denominator": None}
                if prev is None or o is None or not isinstance(o.get("numerator"), (int, float)):
                    m["delta"] = {"na": "no prior", "why": "no comparable measure in the prior generation", "new": newc}
                elif prev.get("definition") != v.get("definition") or o.get("scope") != m.get("scope"):
                    m["delta"] = {"na": "N/A - definition changed", "why": "definition or scope changed", "old": {"numerator": o["numerator"],
                                  "denominator": o.get("denominator")}, "new": newc}
                else:
                    dc = m["numerator"] - o["numerator"]
                    m["delta"] = {"count": dc, "rel": (round(100.0 * dc / o["numerator"], 3) if o["numerator"] else None),
                                  "old": {"numerator": o["numerator"], "denominator": None}, "new": newc}
                continue
            new = {"numerator": m["numerator"], "denominator": m["denominator"]}
            if prev is None or o is None:
                m["delta"] = {"na": "no prior", "why": "no comparable measure in the prior generation", "new": new}
            elif prev.get("definition") != v.get("definition"):
                m["delta"] = {"na": "N/A - definition changed", "why": "view definition %s -> %s" % (prev.get("definition"), v.get("definition")),
                              "old": {"numerator": o["numerator"], "denominator": o.get("denominator")}, "new": new}
            elif o.get("scope") != m.get("scope") or o.get("denominator") != m["denominator"]:
                # No percentage-point delta across a moved denominator (like-for-like rule), but both sides' changes are
                # shown, so a refresh that found new requirements and closed some is visible as exactly that.
                m["delta"] = {"na": "scope changed", "why": "scope %r -> %r; denominator %s -> %s" % (o.get("scope"), m.get("scope"), o.get("denominator"), m["denominator"]),
                              "old": {"numerator": o["numerator"], "denominator": o.get("denominator")}, "new": new,
                              "dnum": (m["numerator"] - o["numerator"]) if isinstance(o.get("numerator"), (int, float)) else None,
                              "dden": (m["denominator"] - o["denominator"]) if isinstance(o.get("denominator"), (int, float)) else None}
                # USER DIRECTIVE 2026-09-30: the tile's change is how much the completion percentage rose or fell since the
                # last refresh, also when the denominator moved (it overrides the like-for-like rule for the headline; the
                # counts stay in dnum/dden for the tooltip, and "na" still says the scope moved).
                # A denominator of 0 has nothing left to do, so it counts as 100 % complete: a scope that goes from 0 of 0 to
                # 0 of 10 shows its completion falling 100 points, never an unlabelled "0 of +10" (user, 2026-09-30).
                pct = lambda n, d: (100.0 * n / d) if d else 100.0
                if isinstance(o.get("denominator"), (int, float)) and isinstance(o.get("numerator"), (int, float))                         and isinstance(m.get("denominator"), (int, float)):
                    m["delta"]["pp"] = round(pct(m["numerator"], m["denominator"]) - pct(o["numerator"], o["denominator"]), 3)
            else:
                # same scope and same denominator; 0 of 0 is 100 % complete (user, 2026-09-30), never a division by zero
                pct = lambda n, d: (100.0 * n / d) if d else 100.0
                pp_ = pct(m["numerator"], m["denominator"]) - pct(o["numerator"], o["denominator"])
                m["delta"] = {"pp": round(pp_, 3), "old": {"numerator": o["numerator"], "denominator": o["denominator"]}, "new": new}


def prior_progress(prior_man, prior_dir):
    """My Progress's prior checkpoint, read from THE SAME generation prior_generation() chose for every other delta.
    If that generation has no progress view there is no prior: the change block and the measure deltas both say so, and
    delta_basis names the generation that was compared. It never falls back to an older generation that has one (ASTRA
    9e84de620: prior_progress skipped a newer verified generation without a progress view, so the change came from an
    older generation while delta_basis named the newer)."""
    if not prior_dir:
        return None
    p = os.path.join(prior_dir, "outputs", "view-progress.json")
    if not os.path.exists(p):
        return None
    try:
        v = json.load(open(p, encoding="utf-8")).get("progress") or {}
    except ValueError:
        return None
    return {"version": v.get("version"), "generation": prior_man["generation"], "committed_at": prior_man.get("committed_at"),
            "scopes": v.get("scopes", {}), "categories": {c["code"]: {"accepted": c["accepted"], "total": c["total"]} for c in v.get("categories", [])}}


def _build(st, inputs, t, I):
    b = st.begin(inputs, {"name": "build_views.py", "sha256": G.sha256_file(os.path.abspath(__file__))})
    snap = {n: (inputs[n]["path"] if not inputs[n].get("snapshot", True) else b.input_path(n)) for n in inputs}   # portable names (A23)
    snap["_pkgdir"] = os.path.join(b.dir, "_pkg"); os.makedirs(snap["_pkgdir"])
    for n in inputs:
        if n.startswith("pkg:") and os.path.exists(snap[n]):
            import shutil; shutil.copyfile(snap[n], os.path.join(snap["_pkgdir"], n[4:]))
    pman, pdir = prior_generation(st)          # ONE basis for the progress change block and every measure delta
    pp = prior_progress(pman, pdir)
    if pp:
        snap["_prior_progress"] = os.path.join(b.dir, "_prior_progress.json")
        json.dump(pp, open(snap["_prior_progress"], "w", encoding="utf-8"))
    views = {}
    for name, fn in ADAPTERS.items():
        try:
            v = fn(snap, t)
        except Exception as e:
            v = {"view": name, "title": name, "status": "FAILED", "source": {"limits": "adapter raised %s: %s" % (type(e).__name__, e),
                 "trace": traceback.format_exc()[-600:]}, "measures": []}
        v["definition"] = DEFINITIONS.get(name) or (v.get("progress") or {}).get("version") or "v1"
        for m in v.get("measures", []):
            m["direction"] = DIRECTIONS.get(name, {}).get(m["id"], "none")
        views[name] = v
    annotate_deltas(views, pdir, pman)
    for name, v in views.items():
        json.dump(v, open(b.output_path("view-%s.json" % name), "w", encoding="utf-8"), indent=1)
    gid = st.commit(b, ["view-%s.json" % n for n in ADAPTERS])
    try:                           # a compact history for later trend charts; outside the generation, never read back as data
        with open(os.path.join(st.root, HISTORY_MEASURES), "a", encoding="utf-8") as h:
            h.write(json.dumps({"generation": gid, "committed_at": t, "measures": [[n, v.get("definition"), m["id"], m["numerator"], m["denominator"]]
                                for n, v in views.items() for m in v.get("measures", []) if m.get("denominator")]}) + "\n")
    except OSError:
        pass
    print("committed", gid, "->", st.root)
    return gid


if __name__ == "__main__":
    main()
