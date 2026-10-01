#!/usr/bin/env python3
"""transfer_audit.py -- the disposition transfers are routing, not answers
(FRONTIER-TODO-TRANSFER-DESTINATION-AUDIT, 2026-09-27 directive).

The register's SCOPE-OR-PROCESS batch (batch-K-scope-rulings.md) closed rows
two ways, and both transfer an obligation rather than answering it:

  class 1: SUPERSEDED onto a named instrument - "population: X; instrument:
           the unresolved worklist, <path>.md". The members stay unread; the
           destination file IS the tracker's visibility of that debt.
  class 2: NOT A QUESTION, carried by a named board task - the process item
           lives or dies with that task's owner.

If a destination file is deleted, a worklist drained without a landed
propagation, or a carrier task vanishes from the board, the row reads
SUPERSEDED while the obligation has no owner anywhere - and the goal gate,
which only counts verdicts, would report MET over a lost requirement.

This audit is READ-ONLY and checks exactly that:
  - every class-1 row's named destination files exist (document .md under the
    database; worklist/tsv tokens resolved against the doc's directory, the
    database root, and Database/Tools/work);
  - every class-2 row's carrier task exists on the board with a live owner
    (agent or assigned_to set); a DONE carrier is a landed disposition.

Usage: transfer_audit.py [--db <path>] [--board <path>]
Exit 0 = all destinations live; 1 = at least one obligation is untracked;
2 = the audit itself could not run (missing record/board - fail closed).
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402

BATCH = os.path.join("_index", "candidates", "register-triage",
                     "batch-K-scope-rulings.md")
ROW = re.compile(r"^\|\s*([A-Z]{1,5}-?\d+[a-z]?)\s*\|(.*)$")
PATH_TOK = re.compile(r"[\w()/.-]+\.(?:md|tsv|csv|json)")
TASK_TOK = re.compile(r"`([A-Z][A-Z0-9-]{6,})`")


def _resolve(token, hints):
    for base in hints:
        cand = os.path.normpath(os.path.join(base, token))
        if os.path.isfile(cand):
            return cand
    return None


def _table_rows(text, header_after):
    """Markdown rows of the table that follows a heading containing
    header_after. Returns [(row_id, [cells])]."""
    rows, in_sec, cols = [], False, []
    for line in text.splitlines():
        if line.startswith("##"):
            in_sec = header_after in line.lower()
            continue
        if not in_sec or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or all(set(c) <= set("-: ") for c in cells):
            continue
        if cells[0].lower() in ("row", "id"):
            cols = cells
            continue
        m = ROW.match(line)
        if m and len(cells) >= 2:
            rows.append((m.group(1), cells[1:]))
    return rows


def audit(db, board_path, batch_path=None):
    """Return (problems, checked) - list of failure strings and rows seen."""
    problems, checked = [], []
    batch = batch_path or os.path.join(db, BATCH)
    try:
        text = open(batch, encoding="utf-8", errors="replace").read()
    except OSError:
        return ["transfer record unreadable: %s" % batch], checked

    try:
        board = json.load(open(board_path, encoding="utf-8"))
        live_tasks = {t["id"]: t for t in board.get("tasks", [])}
    except (OSError, KeyError, ValueError):
        return ["board unreadable: %s" % board_path], checked

    # class 1: SUPERSEDED onto the instrument -> destination files must exist.
    for rid, cells in _table_rows(text, "class 1"):
        checked.append(rid)
        instrument = cells[-1]
        tokens = PATH_TOK.findall(instrument)
        if not tokens:
            problems.append("%s: class-1 destination names no file: %s"
                            % (rid, instrument[:80]))
            continue
        doc_dirs = []
        for tok in tokens:
            hints = [os.path.join(db), db,
                     os.path.join(KP.ROOT, "Database", "Tools"),
                     os.path.join(KP.ROOT, "Database", "Tools", "work")]
            hints += doc_dirs
            hit = _resolve(tok, hints)
            if hit is None and "/" not in tok:
                # bare filename: sibling of a resolved doc, or db-wide search
                hit = _resolve(tok, doc_dirs)
                if hit is None:
                    for dp, _, fs in os.walk(db):
                        if "_inbox" in dp:
                            continue
                        if tok in fs:
                            hit = os.path.join(dp, tok)
                            break
            if hit is None:
                problems.append("%s: class-1 destination file missing: %s"
                                % (rid, tok))
            elif tok.endswith(".md"):
                doc_dirs.append(os.path.dirname(hit))
                if not os.path.getsize(hit):
                    problems.append("%s: class-1 destination is empty: %s"
                                    % (rid, tok))

    # class 2: NOT A QUESTION with a carrier -> carrier task must be on the
    # board with a live owner (any status; DONE means landed).
    for rid, cells in _table_rows(text, "class 2"):
        checked.append(rid)
        carriers = TASK_TOK.findall(" ".join(cells))
        if not carriers:
            problems.append("%s: class-2 row names no carrier task" % rid)
            continue
        for cid in carriers:
            t = live_tasks.get(cid)
            if t is None:
                problems.append("%s: carrier task %s is not on the board"
                                % (rid, cid))
            elif not (t.get("agent") or t.get("assigned_to")):
                problems.append("%s: carrier task %s has no owner"
                                % (rid, cid))
    return problems, checked


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--board",
                    default=os.path.join(KP.DB, "_index", "_inbox",
                                         "TEAM.json"))
    a = ap.parse_args(argv)
    problems, checked = audit(a.db, a.board)
    for p in problems:
        print("untracked: %s" % p)
    print("transfer audit: %d obligations checked, %d untracked"
          % (len(checked), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
