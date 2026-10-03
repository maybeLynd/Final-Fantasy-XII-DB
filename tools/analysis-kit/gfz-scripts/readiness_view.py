#!/usr/bin/env python3
"""readiness_view.py [--db DB] [--lifecycle P] [--board P] [--out TSV] [--self-test] - per-system reconstruction-readiness
rows as a dashboard-generation input (SWE2-STRUCT, 2026-10-03).

Design: _index/candidates/swe2struct-design-readiness-views-1003/README.md, accepted by FABLE with one refinement (its
section 11). Addendum section 16, P2 item 15. It is a VIEW INPUT, not a gate. No score, no percentage, no new completion
metric: every column is a count on one DASHBOARD-MEANINGS axis, fed by an existing file. goal_gate.py stays the
whole-database authority.

ONE ROW PER REGISTERED SYSTEM (important-subsystems.tsv), plus an UNATTRIBUTED row for production residue pages that no
system lists (shown, never dropped and never guessed onto a system).

MATURITY (DASHBOARD-MEANINGS section 6.4, FABLE's ruling 2026-10-03). The label vocabulary is PROJECT-LIFECYCLE.json's
maturity_ladder; this script defines no label. While current_primary_phase is DATABASE, the one label a row may carry is
SPECIFICATION READY. Every later label appears only as a database-phase PROBE (the parity pilots column). A missing or
unreadable lifecycle file, or any other phase, gives UNMEASURED: fail closed, never a guessed label. SPECIFICATION READY
needs all of the following:
  scoped L2 verdict MET; no OPEN / PARTIAL / BLOCKED register row owned by a page or contract of the system; no
  unresolved contradiction naming them; no readiness-batch edit still standing on them; no contract section-14 line that
  names no register id; and no PARTIAL / REOPENED production page of the system that check_status_residue.py classes
  UNMAPPED.
A missing input makes its column UNMEASURED, and an UNMEASURED evidence column withholds the label. It is never zero.

--self-test drives the pure rule functions on synthetic rows: the phase cap, each SPECIFICATION READY condition including
UNMAPPED, and fail-closed lifecycle handling. It prints FAILS n.
"""
import argparse, collections, datetime, glob, io, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DB0 = os.path.normpath(os.path.join(HERE, "..", "..", "..", "FFXII TZA"))
SR = "SPECIFICATION READY"
UNM = "UNMEASURED"
RID = re.compile(r"\b([A-Z]{1,4}-\d{1,3}[a-z]?)\b")
LIVE = {"OPEN", "PARTIAL", "BLOCKED"}
RESOLVED_CONTRA = {"CORRECTED", "RESOLVED", "WITHDRAWN", "SUPERSEDED", "UPHELD", "REFUTED", "ANSWERED", "DUPLICATE"}
COLUMNS = ["system", "name", "l2", "pages", "contracts", "types", "fields", "gap_spans", "census_rows", "register_live",
           "register_closed", "contradictions_unresolved", "residue_partial_pages", "residue_unmapped",
           "readiness_pending", "unresolved_unregistered", "runtime_exp", "parity_probes", "board_open", "maturity",
           "maturity_withheld_by"]


def rd(p):
    with open(p, "rb") as fh:
        return fh.read().decode("utf-8", "replace")


# ------------------------------------------------------------------ pure rule functions (self-tested)
def lifecycle_phase(lc):
    """(phase, ladder) from a parsed lifecycle dict, or (None, None) when it cannot be trusted."""
    if not isinstance(lc, dict):
        return None, None
    ph, lad = lc.get("current_primary_phase"), lc.get("maturity_ladder")
    if not isinstance(ph, str) or not isinstance(lad, list) or SR not in lad:
        return None, None
    return ph, lad


def sr_withheld_by(row):
    """The SPECIFICATION READY conditions a row fails (empty list = all hold). UNMEASURED evidence withholds."""
    out = []
    def need(col, ok):
        v = row.get(col)
        if v == UNM or v is None:
            out.append(col + "=UNMEASURED")
        elif not ok(v):
            out.append("%s=%s" % (col, v))
    need("l2", lambda v: v == "MET")
    need("register_live", lambda v: int(v) == 0)
    need("contradictions_unresolved", lambda v: int(v) == 0)
    need("readiness_pending", lambda v: int(v) == 0)
    need("unresolved_unregistered", lambda v: int(v) == 0)
    need("residue_unmapped", lambda v: int(v) == 0)
    return out


def maturity(row, phase, ladder):
    """(label, withheld_by). The phase cap: in DATABASE only SPECIFICATION READY may be shown."""
    if phase is None or ladder is None:
        return UNM, "lifecycle contract missing or unreadable"
    if phase != "DATABASE":
        return UNM, "phase %s: labels past %s need section-6 criteria this view does not evaluate" % (phase, SR)
    w = sr_withheld_by(row)
    return ("" if w else SR), "; ".join(w)


CLOSED_WORD = re.compile(r"\b(ANSWERED|RESOLVED|CLOSED|WITHDRAWN|SUPERSEDED|REFUTED|none)\b", re.I)


def unregistered_items(sec):
    """Contract section-14 items that name no register id and carry no closing word. An item starts at column 0 with
    '- ', '* ' or 'N. ' and runs until the next item; struck text (~~...~~, across lines) is removed first."""
    items, cur = [], None
    for ln in sec.splitlines():
        if re.match(r"^(?:[-*]|\d+\.)\s+\S", ln):
            if cur is not None:
                items.append(cur)
            cur = ln
        elif cur is not None and (ln.startswith((" ", "\t")) and ln.strip()):
            cur += "\n" + ln
        elif not ln.strip() and cur is not None:
            items.append(cur); cur = None
    if cur is not None:
        items.append(cur)
    out = []
    for it in items:
        live = re.sub(r"~~.*?~~", "", it, flags=re.S)
        if len(live.strip(" -*0123456789.\n")) < 4:
            continue
        if not RID.search(live) and not CLOSED_WORD.search(live):
            out.append(it)
    return out


def capped(label, phase):
    """True when a label is allowed to be shown in this phase (labels past SR are probes only in DATABASE)."""
    return phase != "DATABASE" or label in ("", SR, UNM)


# ------------------------------------------------------------------ measurement
def register_rows(db):
    import check_questions as cq
    states, _ = cq.read_table(db)
    rows = []
    for l in rd(os.path.join(db, "_index", "OPEN-QUESTIONS.md")).splitlines():
        if not l.startswith("| ") or l.startswith("| ID"):
            continue
        c = cq.row_cells(l)
        if len(c) >= 3:
            rid = c[0].strip()
            if rid in states:
                rows.append((rid, c[2], states[rid]))
    return rows


def contradictions(db):
    lines = [l for l in rd(os.path.join(db, "_index", "CONTRADICTIONS.tsv")).splitlines() if l and not l.startswith("#")]
    hdr = lines[0].split("\t")
    ki = hdr.index("kind")
    return [(l.split("\t")[ki] if len(l.split("\t")) > ki else "?", l) for l in lines[1:]]


def readiness_edits(db):
    """(page basename, old, new) for every edit in the opus-*-readiness-fixes-* apply scripts."""
    out = []
    for d in sorted(glob.glob(os.path.join(db, "_index", "candidates", "opus-*-readiness-fixes-*"))):
        for ap in glob.glob(os.path.join(d, "apply_*.py")):
            if os.path.basename(ap) == "apply_by_owner.py":
                continue
            name = "_rv_" + re.sub(r"\W", "_", os.path.relpath(ap, db))
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location(name, ap)
                m = importlib.util.module_from_spec(spec)
                sys.path.insert(0, d)
                spec.loader.exec_module(m)
                for e in getattr(m, "EDITS", []):
                    if isinstance(e, (list, tuple)) and len(e) >= 3:
                        out.append((e[0].replace("\\", "/"), e[1], e[2]))
            except Exception:
                out.append(("__FAILED__", ap, ""))
            finally:
                if sys.path and sys.path[0] == d:
                    sys.path.pop(0)
    return out


def l2_verdicts(db):
    """{S-id: L2 verdict word} through the one shared table reader (l2_verdict_table -> progress_report). The old regex
    took the first S-id row anywhere in the file and the word after its first `|` - the contract column, or a cell of an
    earlier table - and read 45 systems L2 MET against the table's 31 (SWE2-FRONTIER, 2026-10-03)."""
    import l2_verdict_table
    p = os.path.join(db, "_index", "L2-VERDICTS.md")
    return l2_verdict_table.l2_by_system(p) if os.path.exists(p) else {}


def measure(db, lifecycle_path, board_path):
    idx = os.path.join(db, "_index")
    subs = [l.rstrip("\r\n").split("\t") for l in rd(os.path.join(idx, "important-subsystems.tsv")).splitlines()][1:]
    l2 = l2_verdicts(db)
    types = {}
    for l in rd(os.path.join(db, "_types", "types.tsv")).splitlines()[1:]:
        c = l.split("\t")
        if c and c[0]:
            types[c[0]] = c
    fields = collections.defaultdict(list)
    for l in rd(os.path.join(db, "_types", "fields.tsv")).splitlines()[1:]:
        c = l.split("\t")
        if len(c) > 3:
            fields[c[0]].append(c)
    cw = rd(os.path.join(HERE, "check_census_widths.py"))
    cmap = dict(re.findall(r'"([A-Za-z0-9_]+)":\s*"([^"]+-accesses\.tsv)"', cw))
    census_files = {os.path.basename(p): p for p in glob.glob(os.path.join(db, "**", "*-accesses.tsv"), recursive=True)}
    census_rows = {}
    reg = register_rows(db)
    contra = contradictions(db)
    import check_status_residue as csr
    import check_questions as cq
    _, res_pages = csr.census(db, cq.read_table(db)[0])
    edits = readiness_edits(db)
    parity = rd(os.path.join(idx, "PARITY-STATUS.md")) if os.path.exists(os.path.join(idx, "PARITY-STATUS.md")) else None
    try:
        phase, ladder = lifecycle_phase(json.loads(rd(lifecycle_path)))
    except Exception:
        phase, ladder = None, None
    board = None
    if board_path and os.path.exists(board_path):
        try:
            board = json.loads(open(board_path, "rb").read())
        except Exception:
            board = None
    page_text = {}

    def text(p):
        if p not in page_text:
            page_text[p] = rd(p).replace("\r\n", "\n") if os.path.exists(p) else None
        return page_text[p]

    attributed = set()
    rows = []
    for s in subs:
        sid = s[0]
        pages = [os.path.normpath(os.path.join(idx, p)) for p in s[4].split(";") if p]
        cons = [os.path.normpath(os.path.join(idx, p)) for p in s[5].split(";") if p] if len(s) > 5 else []
        files = pages + cons
        rels = {os.path.relpath(p, db).replace(os.sep, "/") for p in files}
        attributed |= rels
        names = {os.path.basename(p) for p in files}
        named = collections.OrderedDict()
        unreg = 0
        exps = set()
        for cp in cons:
            t = text(cp)
            if t is None:
                continue
            m = re.search(r"^## 3\. Types(.*?)^## ", t, re.S | re.M)
            for tok in re.findall(r"\b([A-Z][A-Za-z0-9_]{3,})\b", m.group(1) if m else ""):
                if tok in types:
                    named[tok] = 1
            m14 = re.search(r"^## 14\.[^\n]*\n(.*?)(?=^## )", t, re.S | re.M)
            unreg += len(unregistered_items(m14.group(1) if m14 else ""))
            for sec in ("13", "13a"):
                ms = re.search(r"^## %s\.[^\n]*\n(.*?)(?=^## )" % re.escape(sec), t, re.S | re.M)
                exps |= set(re.findall(r"EXP-\d+", ms.group(1) if ms else ""))
        nf = sum(len(fields[t]) for t in named)
        gaps = sum(1 for t in named for f in fields[t] if f[3].lower().startswith("unobservedspan"))
        crows = 0
        for t in named:
            f = cmap.get(t)
            p = census_files.get(os.path.basename(f)) if f else None
            if p:
                if p not in census_rows:
                    census_rows[p] = sum(1 for l in rd(p).splitlines()[1:] if l.strip())
                crows += census_rows[p]
        rl = sum(1 for rid, owner, st in reg if st in LIVE and any(n in owner for n in names))
        rc = sum(1 for rid, owner, st in reg if st not in LIVE and any(n in owner for n in names))
        cu = sum(1 for k, l in contra if any(n in l for n in names) and k.upper() not in RESOLVED_CONTRA)
        rp = [p for p in res_pages if p["page"] in rels]
        pend = 0
        failed_edits = any(e[0] == "__FAILED__" for e in edits)
        for pg, old, new in edits:
            b = pg.rsplit("/", 1)[-1]
            if b not in names:
                continue
            for f in files:
                if os.path.basename(f) == b and (pg in f.replace(os.sep, "/") or True):
                    t = text(f)
                    if t is not None and new not in t and old in t:
                        pend += 1
                    break
        probes = UNM if parity is None else sum(
            1 for c in cons if re.search(r"^- \*\*contract:\*\* `%s`" % re.escape(os.path.relpath(c, db).replace(os.sep, "/")), parity, re.M))
        bo = UNM
        if board is not None:
            bo = 0
            for tk in board.get("tasks", []):
                if tk.get("status") in ("ACTIVE", "READY", "BLOCKED"):
                    blob = json.dumps({k: tk.get(k) for k in ("target", "scope", "question", "resources")}).lower()
                    if any(n.lower() in blob for n in names) or re.search(r"\b%s\b" % sid.lower(), blob):
                        bo += 1
        row = {"system": sid, "name": s[2][:80], "l2": l2.get(sid, UNM), "pages": len(pages), "contracts": len(cons),
               "types": len(named), "fields": nf, "gap_spans": gaps, "census_rows": crows, "register_live": rl,
               "register_closed": rc, "contradictions_unresolved": cu, "residue_partial_pages": len(rp),
               "residue_unmapped": sum(1 for p in rp if p["class"] == "UNMAPPED"),
               "readiness_pending": UNM if failed_edits else pend, "unresolved_unregistered": unreg,
               "runtime_exp": len(exps), "parity_probes": probes, "board_open": bo}
        row["maturity"], row["maturity_withheld_by"] = maturity(row, phase, ladder)
        rows.append(row)
    un = [p for p in res_pages if p["page"] not in attributed]
    rows.append({"system": "UNATTRIBUTED", "name": "production residue pages no registered system lists",
                 "l2": "", "pages": len(un), "contracts": "", "types": "", "fields": "", "gap_spans": "", "census_rows": "",
                 "register_live": "", "register_closed": "", "contradictions_unresolved": "",
                 "residue_partial_pages": len(un), "residue_unmapped": sum(1 for p in un if p["class"] == "UNMAPPED"),
                 "readiness_pending": "", "unresolved_unregistered": "", "runtime_exp": "", "parity_probes": "",
                 "board_open": "", "maturity": "", "maturity_withheld_by": "not a system; listed so no residue is dropped"})
    return rows, phase, un


def self_test():
    lad = ["SPECIFICATION READY", "SEMANTIC CORE IMPLEMENTED", "PARITY CERTIFIED"]
    good = {"l2": "MET", "register_live": 0, "contradictions_unresolved": 0, "readiness_pending": 0,
            "unresolved_unregistered": 0, "residue_unmapped": 0}
    cases = []
    cases.append(("all evidence holds, DATABASE -> SR", maturity(good, "DATABASE", lad)[0] == SR))
    cases.append(("UNMAPPED residue withholds SR", maturity(dict(good, residue_unmapped=1), "DATABASE", lad)[0] == ""))
    for col, bad in (("l2", "NOT MET"), ("register_live", 2), ("contradictions_unresolved", 1), ("readiness_pending", 3),
                     ("unresolved_unregistered", 1)):
        cases.append(("%s=%s withholds SR" % (col, bad), maturity(dict(good, **{col: bad}), "DATABASE", lad)[0] == ""))
    cases.append(("UNMEASURED evidence withholds SR, never a zero", maturity(dict(good, residue_unmapped=UNM), "DATABASE", lad)[0] == ""
                  and "residue_unmapped=UNMEASURED" in maturity(dict(good, residue_unmapped=UNM), "DATABASE", lad)[1]))
    cases.append(("missing lifecycle -> UNMEASURED", maturity(good, *lifecycle_phase(None))[0] == UNM))
    cases.append(("ladder without SR -> UNMEASURED", maturity(good, *lifecycle_phase({"current_primary_phase": "DATABASE", "maturity_ladder": ["X"]}))[0] == UNM))
    cases.append(("non-DATABASE phase -> UNMEASURED, no label guessed", maturity(good, "RECONSTRUCTION", lad)[0] == UNM))
    cases.append(("phase cap: SEMANTIC CORE IMPLEMENTED not showable in DATABASE", not capped("SEMANTIC CORE IMPLEMENTED", "DATABASE")))
    cases.append(("phase cap: SR showable in DATABASE", capped(SR, "DATABASE")))
    cases.append(("maturity() never returns a label past SR in DATABASE",
                  all(maturity(dict(good, **o), "DATABASE", lad)[0] in ("", SR) for o in ({}, {"l2": "NOT MET"}))))
    sec = ("1. ~~**Old question** spanning\n   two lines.~~ **ANSWERED 2026-09-22** by citation.\n"
           "2. Whether X happens; registered as OV-12.\n"
           "- Why the rings are twins.\n"
           "- ~~struck entirely~~\n")
    got = unregistered_items(sec)
    cases.append(("section 14: multi-line struck+ANSWERED item is closed, RID item registered, bare bullet counted",
                  len(got) == 1 and "twins" in got[0]))
    fails = 0
    for name, ok in cases:
        print("  %-4s %s" % ("ok" if ok else "FAIL", name))
        fails += 0 if ok else 1
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB0)
    ap.add_argument("--lifecycle", default=None)
    ap.add_argument("--board", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        f = self_test()
        print("FAILS %d" % f)
        return 1 if f else 0
    lc = a.lifecycle or os.path.join(a.db, "_index", "workflow", "PROJECT-LIFECYCLE.json")
    bd = a.board or os.path.join(a.db, "_index", "_inbox", "TEAM.json")
    rows, phase, un = measure(a.db, lc, bd)
    try:
        head = subprocess.run(["git", "-C", a.db, "rev-parse", "--short=9", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        head = "?"
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = io.StringIO()
    out.write("# readiness_view.py generated %s at HEAD %s; phase=%s; a view input, not a gate - no score; "
              "goal_gate.py owns DB_GOAL\n" % (now, head, phase or UNM))
    out.write("\t".join(COLUMNS) + "\n")
    for r in rows:
        if not capped(r["maturity"], phase):
            raise SystemExit("phase cap violated for %s: %s" % (r["system"], r["maturity"]))
        out.write("\t".join(str(r.get(c, "")) for c in COLUMNS) + "\n")
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(out.getvalue())
    else:
        sys.stdout.write(out.getvalue())
    n_sr = sum(1 for r in rows if r["maturity"] == SR)
    print("systems %d; %s %d; withheld %d; UNATTRIBUTED residue pages %d; phase %s"
          % (len(rows) - 1, SR, n_sr, len(rows) - 1 - n_sr, len(un), phase or UNM), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
