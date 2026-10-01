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
            "measures": [M("l2-met", "registered systems with verdict MET", met, len(subs), "important-subsystems.tsv x L2-VERDICTS.md", "v_systems", t,
                           "scoped L2 only; residual register rows and terminal audit are separate (overview)"),
                         M("categories", "repository categories", len(cats), None, "top-level folders of FFXII TZA", "v_systems", t, "includes residual and library categories")],
            "tree": tree}


def v_vbf(inp, t):
    files, byts, ext = 0, 0, collections.Counter()
    node = lambda: {"files": 0, "bytes": 0, "kids": {}}
    root = node()
    for l in open(inp["vbf_list"], encoding="utf-8", errors="replace"):
        l = l.rstrip("\r\n")
        if not l: continue
        sz, _, p = l.partition(" "); sz = int(sz); parts = p.replace("\\", "/").split("/")
        files += 1; byts += sz; ext[parts[-1].rsplit(".", 1)[-1].lower() if "." in parts[-1] else "(none)"] += 1
        n = root
        for depth, seg in enumerate(parts[:-1][:3]):
            n = n["kids"].setdefault(seg, node()); n["files"] += 1; n["bytes"] += sz
    def conv(name, n, path):
        return {"id": path, "label": name, "counts": {"files": n["files"], "bytes": n["bytes"]},
                "children": [conv(k, v, path + "/" + k) for k, v in sorted(n["kids"].items())]}
    return {"view": "vbf", "title": "VBF archive - the browser's own folder tree", "status": "PARTIAL",
            "source": {"identity": "vbf_list.txt sha256 %s" % sha12(inp["vbf_list"]), "as_of": t, "instrument": "v_vbf over the archive file table",
                       "limits": "the VBF Browser has no category table: its tree IS the archive's folder tree. This listing is from 2026-09-02 and the "
                                 "archive itself is not yet pinned by hash (PARTIAL). Tree shown to depth 3; formats/parse/field-meaning stages are UNMEASURED"},
            "measures": [M("files", "files in the archive", files, None, "archive file table", "v_vbf", t, "a file count; distinct formats and bytes are other denominators"),
                         M("bytes", "bytes in the archive", byts, None, "archive file table", "v_vbf", t, "uncompressed sizes as listed"),
                         M("extensions", "distinct file extensions", len(ext), None, "archive file table", "v_vbf", t, "an extension is not a format variant")],
            "tree": [conv(k, v, k) for k, v in sorted(root["kids"].items())],
            "rows": {"columns": ["extension", "files"], "data": [[e, c] for e, c in ext.most_common()]}}


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
    iv = text_intervals(inp["functions"], (inp["uc1_1_64"], inp["uc1_65_256"]), inp["exe"])
    N = iv["text_size"]; scope = ".text %08X..%08X (%d bytes), each byte counted once" % (iv["text_lo"], iv["text_lo"] + N, N)
    inst = "build_views.text_intervals over functions.tsv + uc1_band.apply + the certified image"
    lim = "physical boundary axis only: a byte inside a body is not READ or EXPLAINED (behavior is UNMEASURED here)"
    ims = [M("bytes-" + k, lab, iv["bytes"][k], N, scope, inst, t, lim) for k, lab in (
        ("listed", "bytes in listed function bodies (population)"), ("frontier", "bytes in UC-1 frontier bodies (population, unexplained by ruling)"),
        ("funclet", "bytes in EH funclets (code outside the population)"), ("held", "bytes in held rows (declared uncertainty, never counted as code)"),
        ("fill", "alignment fill: runs of int3 (CC) / nop (90) bytes outside every body"), ("unknown", "UNKNOWN bytes (no body, no held row, not fill)"))]
    ims.append(M("bytes-overlap", "bytes claimed by more than one population body (counted once above)", iv["overlap"], N, scope, inst, t,
                 "listed extents that overlap a neighbour"))
    ims.append(M("population", "functions in the population (%s)" % iv["describe"], iv["population"], None, "uc1_band.apply", inst, t,
                 "a versioned population; admitted frontier bodies are not explained"))
    return {"view": "executable", "title": "Executable - every .text byte once, and the function-level dimensions", "status": "PARTIAL",
            "source": {"identity": "image %s; functions.tsv %s; COVERAGE-DIMENSIONS.md %s" % (iv["exe_sha"][:12], sha12(inp["functions"]), sha12(inp["coverage_dims"])),
                       "as_of": t, "instrument": inst + "; program_coverage.py",
                       "limits": "byte classes are the boundary axis; behavior (READ / EXPLAINED) and observed execution are UNMEASURED here; "
                                 "data inside .text other than held rows is counted as UNKNOWN until a ruling classifies it; the fill rule is single-byte: multi-byte NOP fill counts as UNKNOWN, and a CC/90 byte inside unclassified data would count as fill"},
            "measures": ims + ms,
            "rows": {"columns": ["largest UNKNOWN gaps", "bytes", "next body"], "data": iv["gaps"]}}


def text_intervals(functions_tsv, band_tsvs, exe):
    """Each byte of .text in exactly one class: listed / frontier (the uc1_band population), funclet, held, fill, unknown."""
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
    front = set(band["frontier"])
    cls = bytearray(n); seen = bytearray(n)       # 0 unknown, 1 listed, 2 frontier, 3 funclet, 4 held, 5 fill
    overlap = 0
    for e, z in pop.items():
        a, b = max(e - lo, 0), min(e + z - lo, n)
        if a >= b: continue
        overlap += sum(seen[a:b]); seen[a:b] = b"\x01" * (b - a)
        k = 2 if e in front else 1
        cls[a:b] = bytes(k if c == 0 else c for c in cls[a:b])
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
    return {"text_lo": lo, "text_size": n, "bytes": {names[k]: cnt.get(k, 0) for k in names}, "overlap": overlap,
            "population": info["total"], "describe": uc1_band.describe(info), "exe_sha": G.sha256_file(exe),
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


def _board(inp):
    b = json.load(open(inp["team"], encoding="utf-8"))
    return b, (b["tasks"] if isinstance(b["tasks"], list) else list(b["tasks"].values()))


def v_evidence(inp, t):
    b, ts = _board(inp)
    rev = [x for x in ts if re.search(r"REVIEW|SIGN|VERIFY", x["id"]) or "review" in (x.get("scope") or "").lower()]
    st = collections.Counter(x["status"] for x in rev)
    done = [x for x in rev if x["status"] == "DONE"]
    acc = sum(1 for x in done if re.match(r"\s*(ACCEPT|SIGNED)", x.get("checkpoint") or "", re.I))
    rej = sum(1 for x in done if re.match(r"\s*(REJECT|DECLINED|RETURN)", x.get("checkpoint") or "", re.I))
    waiting = sorted((x for x in rev if x["status"] == "READY"), key=lambda x: x.get("updated_at") or "")[:40]
    return {"view": "evidence", "title": "Evidence and review health (board)", "status": "PARTIAL",
            "source": {"identity": "TEAM.json rev %s epoch %s" % (b.get("revision"), b.get("recovery_epoch")), "as_of": t, "instrument": "v_evidence",
                       "limits": "review tasks recognised by id/scope; ACCEPT/REJECT read from the checkpoint's leading word; pending-propagation records "
                                 "and receipt sealing are UNMEASURED here"},
            "measures": [M("reviews-done", "review/sign/verify tasks DONE", st.get("DONE", 0), len(rev), "board", "v_evidence", t, "DONE is not acceptance"),
                         M("reviews-accepted", "DONE reviews whose checkpoint begins ACCEPT/SIGNED", acc, len(done), "board", "v_evidence", t,
                           "%d begin REJECT/DECLINED/RETURN; the rest state no verdict word" % rej)],
            "rows": {"columns": ["waiting review (oldest first)", "assigned to", "since"],
                     "data": [[x["id"], x.get("assigned_to"), (x.get("updated_at") or "")[:16]] for x in waiting]}}


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
          M("L2", "L2 requirements accepted", sc["L2"]["accepted"], sc["L2"]["total"], "L2 (reconstruction grade)", inst, t, lim),
          M("union-exf", "governing requirements accepted, L1+L2, excluding the 35,064 function dispositions (C1)", sc["union_exF"]["accepted"],
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
                         "terminal": r["terminal"],
                         "reconstruction": {"state": "DATABASE READY - awaiting user authorization" if ready else "NOT READY", "why": r["why_not_ready"]},
                         "categories": cats, "change": r["change"], "excluded": r["excluded"], "unplaced": r["unplaced"],
                         "duplicates_merged": r["duplicates_merged"]}}


ADAPTERS = {"progress": v_progress, "overview": v_overview, "systems": v_systems, "vbf": v_vbf, "executable": v_executable, "types": v_types,
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
    cap = os.path.join(a.root, "_capture"); os.makedirs(cap, exist_ok=True)
    t = NOW()
    r = subprocess.run([sys.executable, os.path.join(GS, "goal_gate.py"), "--db", DB, "--json"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    open(os.path.join(cap, "goal_gate.json"), "w", encoding="utf-8").write(r.stdout)
    r = subprocess.run([sys.executable, os.path.join(GS, "check_questions.py"), "--db", DB], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    open(os.path.join(cap, "check_questions.txt"), "w", encoding="utf-8").write(r.stdout)
    category_tree(os.path.join(cap, "category_tree.json"))
    r = subprocess.run([sys.executable, os.path.join(DB, "_index", "progress", "progress_report.py"), "check", "--db", DB], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    open(os.path.join(cap, "progress_check.txt"), "w", encoding="utf-8").write((r.stdout + r.stderr).strip() + "\n")
    r = subprocess.run([sys.executable, os.path.join(HERE, "requirements.py"), "--db", DB, "--out", os.path.join(cap, "requirement_facts.json"),
                        "--residual", os.path.join(TOOLS, "work", "verify_GFZ_PARENT", "residual_addrs.txt")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    if r.returncode != 0:          # the facts file keeps its previous bytes; the view reports the failure rather than stale facts
        open(os.path.join(cap, "requirement_facts.json"), "w", encoding="utf-8").write(json.dumps(
            {"version": "MP-1", "facts": [], "failed": {"collect": (r.stderr or r.stdout)[-300:]}, "excluded": []}))
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
    """Every input a view reads, by name. A test may redirect one; adapters only ever see the snapshots."""
    I = os.path.join(DB, "_index"); UC = os.path.join(DB, "99-Unresolved-Residual", "Unlisted-Code")
    inputs = {"goal_gate": {"path": os.path.join(cap, "goal_gate.json")}, "check_questions": {"path": os.path.join(cap, "check_questions.txt")},
              "_tree": {"path": os.path.join(cap, "category_tree.json")},
              "progress_snapshot": {"path": os.path.join(I, "progress", "snapshot.json"), "volatile": True},
              "progress_check": {"path": os.path.join(cap, "progress_check.txt")},
              "subsystems": {"path": os.path.join(I, "important-subsystems.tsv")}, "l2": {"path": os.path.join(I, "L2-VERDICTS.md")},
              "vbf_list": {"path": os.path.join(TOOLS, "work", "repos-2d", "vbf_list.txt")},
              "coverage_dims": {"path": os.path.join(I, "COVERAGE-DIMENSIONS.md")},
              "functions": {"path": os.path.join(TOOLS, "work", "graph", "functions.tsv")},
              "exe": {"path": os.path.join(TOOLS, "work", "exe", "FFXII_TZA.exe"), "snapshot": False},   # certified image: hashed, never copied or exported
              "uc1_1_64": {"path": os.path.join(UC, "uc1-applied-population-1-64.tsv")}, "uc1_65_256": {"path": os.path.join(UC, "uc1-applied-population-65-256.tsv")},
              "types": {"path": os.path.join(DB, "_types", "types.tsv")}, "fields": {"path": os.path.join(DB, "_types", "fields.tsv")},
              "team": {"path": os.path.join(I, "_inbox", "TEAM.json"), "volatile": True},        # written every few seconds
              "watchdog": {"path": os.path.expandvars(os.path.join("%USERPROFILE%", ".swe2-fleet", "watchdog-state.json")), "required": False, "volatile": True},
              "requirement_facts": {"path": os.path.join(cap, "requirement_facts.json")},
              "category_map": {"path": os.path.join(I, "workflow", "my-progress", "category-map.tsv")},
              "requirements.py": {"path": os.path.join(HERE, "requirements.py")},
              "build_views.py": {"path": os.path.abspath(__file__)}}
    for p in sorted(glob.glob(os.path.join(I, "completion-packages", "PKG-*.md"))):
        inputs["pkg:" + os.path.basename(p)] = {"path": p}
    return inputs


def prior_progress(st, t):
    """The prior checkpoint for My Progress: the newest generation committed before 00:00Z of the build day that still
    VERIFIES (open_generation with its recorded manifest hash) and carries a progress view; if none is that old, the
    earliest verified one today. Never a rejected candidate: those are not in the success history. None when absent."""
    hp = os.path.join(st.root, G.HISTORY)
    if not os.path.exists(hp):
        return None
    rows = [json.loads(l) for l in open(hp, encoding="utf-8") if l.strip()]
    day = t[:10] + "T00:00:00Z"
    before = [r for r in rows if (r.get("committed_at") or "") < day]
    order = list(reversed(before)) + [r for r in rows if (r.get("committed_at") or "") >= day]
    for r in order:
        if not os.path.exists(os.path.join(st.root, r.get("generation") or "-", "outputs", "view-progress.json")):
            continue                     # cheap pre-check; the verification below is what admits it
        m, d, probs = st.open_generation(r.get("generation"), r.get("manifest_sha256"))
        p = os.path.join(d or "", "outputs", "view-progress.json")
        if probs or not os.path.exists(p):
            continue
        v = json.load(open(p, encoding="utf-8")).get("progress") or {}
        return {"version": v.get("version"), "generation": m["generation"], "committed_at": m.get("committed_at"),
                "scopes": v.get("scopes", {}), "categories": {c["code"]: {"accepted": c["accepted"], "total": c["total"]} for c in v.get("categories", [])}}
    return None


def _build(st, inputs, t, I):
    b = st.begin(inputs, {"name": "build_views.py", "sha256": G.sha256_file(os.path.abspath(__file__))})
    snap = {n: (inputs[n]["path"] if not inputs[n].get("snapshot", True) else os.path.join(b.dir, "inputs", n)) for n in inputs}
    snap["_pkgdir"] = os.path.join(b.dir, "_pkg"); os.makedirs(snap["_pkgdir"])
    for n in inputs:
        if n.startswith("pkg:") and os.path.exists(snap[n]):
            import shutil; shutil.copyfile(snap[n], os.path.join(snap["_pkgdir"], n[4:]))
    pp = prior_progress(st, t)
    if pp:
        snap["_prior_progress"] = os.path.join(b.dir, "_prior_progress.json")
        json.dump(pp, open(snap["_prior_progress"], "w", encoding="utf-8"))
    for name, fn in ADAPTERS.items():
        try:
            v = fn(snap, t)
        except Exception as e:
            v = {"view": name, "title": name, "status": "FAILED", "source": {"limits": "adapter raised %s: %s" % (type(e).__name__, e),
                 "trace": traceback.format_exc()[-600:]}, "measures": []}
        json.dump(v, open(b.output_path("view-%s.json" % name), "w", encoding="utf-8"), indent=1)
    gid = st.commit(b, ["view-%s.json" % n for n in ADAPTERS])
    print("committed", gid, "->", st.root)
    return gid


if __name__ == "__main__":
    main()
