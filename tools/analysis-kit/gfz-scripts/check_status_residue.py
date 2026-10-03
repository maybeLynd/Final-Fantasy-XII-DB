#!/usr/bin/env python3
"""check_status_residue.py [--db DB] [--json OUT] [--self-test] - production system status residue (FABLE, 2026-10-03,
from the user's FFXII_INDEPENDENT_CORPUS_AUDIT_FOLLOWUP_2026-10-03, sections 2, 9 and 10).

WHY. The register's OPEN/PARTIAL count can look nearly empty while production system pages still carry PARTIAL or
REOPENED status lines whose residue no live row owns. The audit found one (the kind-0x54 mesh page). This makes that
mechanically visible. It is generated from source and adds no completion score.

WHAT. For every system document (front matter with `system:`), it reads the status word. For each PARTIAL / REOPENED /
STUB page it extracts every register id the status line names (e.g. OV-10, SD-196, GR-18) and looks each up in
OPEN-QUESTIONS.md through check_questions.read_table. Then it classifies the page:
  LIVE-ROW          at least one named row is OPEN / PARTIAL / BLOCKED: the residue is registered;
  PROCESS-ONLY      every named row is closed, and the line names a process item only (a review, an acceptance, an
                    owner read, an adjudication, a peer acceptance): no missing knowledge, but the status is waiting;
  UNMAPPED          no named row is live and no process item is named: open semantics nothing owns, OR a stale
                    status. Either way, someone must register the residue or re-status the page.
Then it prints the census and the classified list, and `FAILS N` = the number of UNMAPPED pages. A REOPENED page whose
named rows are all closed also counts as a finding, because REOPENED needs a current reason.

--self-test runs synthetic status lines against a synthetic register; each class must come out as expected."""
import argparse, io, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_questions as cq  # noqa: E402

DB0 = os.path.normpath(os.path.join(HERE, "..", "..", "..", "FFXII TZA"))
SKIP = ("_index", "_experiments", "_templates", "_types")
RID = re.compile(r"\b([A-Z]{1,4}-\d{1,3}[a-z]?(?:/[a-z])?)\b")
PROCESS = re.compile(r"acceptance pending|review pending|adjudication pending|awaits? (?:the )?owner|owner read|peer "
                     r"acceptance|process item|waits for (?:OPUS|FABLE|the owner)|re-?status pending", re.I)
LIVE = {"OPEN", "PARTIAL", "BLOCKED"}


def front(text):
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    return parts[1] if len(parts) >= 3 else None


def status_of(fm):
    m = re.search(r"^status:\s*(.*)$", fm, re.M)
    if not m:
        return None, ""
    s = m.group(1).strip().strip('"').strip("'")
    w = re.match(r"([A-Z][A-Z-]*)", s)
    return (w.group(1) if w else "?"), s


def unstruck(s):
    return re.sub(r"~~.*?~~", "", s)


# OPUS, 2026-10-03 (the user's root-cause directive, item 5): three ways hidden debt still passed.
#  1. A status word the census did not know was simply not examined: only PARTIAL/REOPENED/STUB were. FINAL is now the
#     explicit allow-list and EVERY other word is non-final (fail closed) - a new "DRAFT" or "PROVISIONAL" is examined.
#  2. PROCESS-ONLY accepted waiting WORDING ("review pending") with no identifier, so a page could wait forever on a
#     review nobody holds. A waiting state now needs an exact identifier that resolves: an open board task id, or an
#     existing _index/candidates/ record. Wording without one is UNMAPPED.
#  3. A page whose named rows are all closed and that names no waiting state is STALE-STATUS (re-status it), reported
#     apart from UNMAPPED (nothing named at all). Both fail.
FINAL = {"AUDITED", "DOCUMENTED"}
TASK_ID = re.compile(r"\b([A-Z][A-Z0-9]+(?:-[A-Z0-9]+){2,})\b")
RECORD = re.compile(r"_index/candidates/([A-Za-z0-9._-]+)")


def waiting_ids(line, tasks, db):
    """Exact identifiers of a waiting state named on the line that resolve now: open board tasks, existing records."""
    out = []
    for t in TASK_ID.findall(line):
        if tasks.get(t) in ("READY", "ACTIVE", "BLOCKED"):
            out.append(t)
    for r in RECORD.findall(line):
        if db and os.path.isdir(os.path.join(db, "_index", "candidates", r)):
            out.append("_index/candidates/" + r)
    return out


def classify(word, line, reg, tasks=None, db=None):
    live_part = re.split(r"\(was\b", unstruck(line))[0]   # the "(was ...)" tail is history
    ids = sorted(set(RID.findall(live_part)))
    states = {i: reg.get(i, "UNREGISTERED") for i in ids}
    live = [i for i, s in states.items() if s in LIVE]
    if live:
        return "LIVE-ROW", states
    if PROCESS.search(live_part):
        if waiting_ids(live_part, tasks or {}, db):
            return "WAITING-ID", states
        return "UNMAPPED", dict(states, _why="waiting wording with no open task id or record")
    if ids:
        return "STALE-STATUS", states
    return "UNMAPPED", states


def census(db, reg, tasks=None):
    pages, counts = [], {}
    for dp, dn, fns in os.walk(db):
        rel = os.path.relpath(dp, db).replace(os.sep, "/")
        if rel.split("/")[0] in SKIP:
            continue
        for f in fns:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dp, f)
            fm = front(io.open(p, encoding="utf-8", errors="replace").read(8000))
            if not fm or not re.search(r"^system:", fm, re.M):
                continue
            word, line = status_of(fm)
            counts[word] = counts.get(word, 0) + 1
            if word not in FINAL:
                cls, states = classify(word, line, reg, tasks, db)
                if word == "REOPENED" and cls not in ("LIVE-ROW", "WAITING-ID"):
                    cls = "UNMAPPED"
                pages.append({"page": os.path.relpath(p, db).replace(os.sep, "/"), "status": word, "class": cls,
                              "rows": states, "line": line[:400]})
    return counts, sorted(pages, key=lambda x: (x["class"], x["page"]))


def self_test():
    reg = {"OV-10": "PARTIAL", "RC-12": "ANSWERED", "SD-1": "ANSWERED", "OV-5": "PARTIAL"}
    tasks = {"FABLE-REQ-X-REVIEW-1": "ACTIVE", "FABLE-REQ-X-DONE-2": "DONE"}
    cases = [
        ("PARTIAL", "PARTIAL — OV-10 stays open (runtime)", "LIVE-ROW"),
        ("PARTIAL", "PARTIAL — SD-1 answered; peer acceptance is a process item", "UNMAPPED"),
        ("PARTIAL", "PARTIAL — SD-1 answered; review pending FABLE-REQ-X-REVIEW-1 (peer acceptance)", "WAITING-ID"),
        ("PARTIAL", "PARTIAL — SD-1 answered; review pending FABLE-REQ-X-DONE-2", "UNMAPPED"),
        ("PARTIAL", "PARTIAL — SD-1 answered", "STALE-STATUS"),
        ("DRAFT", "DRAFT — open: the scalars", "UNMAPPED"),
        ("PARTIAL", "PARTIAL — open: what the matrices hold at draw time", "UNMAPPED"),
        ("PARTIAL", "PARTIAL — SD-1 answered; open: the scalars (was — OV-10 open)", "STALE-STATUS"),
        ("REOPENED", "REOPENED — RC-12 answered, FABLE adjudication pending", "UNMAPPED"),
        ("REOPENED", "REOPENED — RC-12 answered, FABLE adjudication pending FABLE-REQ-X-REVIEW-1", "WAITING-ID"),
        ("PARTIAL", "PARTIAL — ~~OV-10 open~~ SD-1 answered", "STALE-STATUS"),
    ]
    ok = True
    for word, line, want in cases:
        got = classify(word, line, reg, tasks)[0]
        print("  %-12s <- %-60s %s" % (got, line[:60], "ok" if got == want else "WRONG (want %s)" % want))
        ok = ok and got == want
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB0)
    ap.add_argument("--json")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        ok = self_test()
        print("SELF-TEST %s" % ("PASS" if ok else "FAIL")); print("FAILS %d" % (0 if ok else 1))
        return 0 if ok else 1
    reg, _ = cq.read_table(a.db)
    tasks = {}
    try:
        b = json.load(io.open(os.path.join(a.db, "_index", "_inbox", "TEAM.json"), encoding="utf-8"))
        tasks = {t.get("id"): str(t.get("status", "")).upper() for t in b.get("tasks", [])}
    except Exception:
        pass
    counts, pages = census(a.db, reg, tasks)
    print("production system pages: " + ", ".join("%s %d" % kv for kv in sorted(counts.items())) +
          " (total %d)" % sum(counts.values()))
    by = {}
    for p in pages:
        by.setdefault(p["class"], []).append(p)
    for cls in ("LIVE-ROW", "WAITING-ID", "STALE-STATUS", "UNMAPPED"):
        print("%s: %d" % (cls, len(by.get(cls, []))))
        for p in by.get(cls, []):
            rows = ", ".join("%s=%s" % kv for kv in sorted(p["rows"].items())) or "no row named"
            print("  %-8s %s  [%s]" % (p["status"], p["page"], rows))
    if a.json:
        json.dump({"db": a.db, "counts": counts, "pages": pages}, open(a.json, "w", encoding="utf-8"), indent=1)
    n = len(by.get("UNMAPPED", [])) + len(by.get("STALE-STATUS", []))
    print("FAILS %d" % n)
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
