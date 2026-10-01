#!/usr/bin/env python3
"""Offline TEAM.json reconstruction after a board rollback incident.

Builds a candidate board from a verified witness snapshot plus the fleet's
per-lane op payloads, then merges the post-reset fork's accepted ops. The
output is an evidence package - candidate board + reconciliation log +
accepted/rejected/ambiguous op reports - never an automatic replacement.

    python team_recover.py build --witness W.json --fork F.json \
        --inventory op-inventory.json --window-start ISO --reset-time ISO \
        --out OUTDIR

Rules that matter (from the 2026-09-25 rollback directive):

- An op file's existence never proves it was applied; the board's own
  `history` entries are the receipts. Ops with no receipt anywhere are
  replayed only if they validate, and are logged as unreceipted.
- No mtime-only total order: mtimes order candidates, but an op is accepted
  only when `team.apply` accepts it against the reconstructed state, with
  fixpoint retries for cross-lane ordering skew.
- No DONE-wins: a post-reset op that duplicates a recovered op is logged as a
  duplicate receipt; a conflicting one goes to the ambiguous list.
- Stale leases are evidence, never live ownership: post-reset ACTIVE claims
  survive only if their ops replay cleanly.
"""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import team


def canon(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def board_sha(board):
    return sha256_bytes(canon(board).encode("utf-8"))


def parse_ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


LANE_DIRS = {
    "FABLE": "FABLE", "OPUS": "OPUS", "ASTRA": "ASTRA",
    "DATA": "SWE2-DATA", "STRUCT": "SWE2-STRUCT", "SWE2": "SWE2-CONTRACT",
    "SWE2-DATA": "SWE2-DATA", "SWE2-ORACLE": "SWE2-ORACLE",
    "SWE2-STRUCT": "SWE2-STRUCT", "SWE2-EC7": "SWE2-EC7",
    "SWE2-CONTRACT": "SWE2-CONTRACT", "SWE2-AUDIT-SEM": "SWE2-AUDIT-SEM",
    "SWE2-AUDIT-SPEC": "SWE2-AUDIT-SPEC", "SWE2-FRONTIER": "SWE2-FRONTIER",
}

ID_PREFIX = [
    ("FABLE", "FABLE"), ("OPUS", "OPUS"), ("ASTRA", "ASTRA"),
    ("AUDITSEM", "SWE2-AUDIT-SEM"), ("AUDITSPEC", "SWE2-AUDIT-SPEC"),
    ("SWE2CONTRACT", "SWE2-CONTRACT"), ("SWE2STRUCT", "SWE2-STRUCT"),
    ("SWE2DATA", "SWE2-DATA"), ("SWE2ORACLE", "SWE2-ORACLE"),
    ("SWE2-CONTRACT", "SWE2-CONTRACT"), ("SWE2-STRUCT", "SWE2-STRUCT"),
    ("SWE2-DATA", "SWE2-DATA"), ("SWE2-ORACLE", "SWE2-ORACLE"),
    ("SWE2-EC7", "SWE2-EC7"), ("SWE2-AUDIT-SEM", "SWE2-AUDIT-SEM"),
    ("SWE2-AUDIT-SPEC", "SWE2-AUDIT-SPEC"), ("FRONTIER", "SWE2-FRONTIER"),
    ("SWE2-FRONTIER", "SWE2-FRONTIER"), ("EXP", "SWE2-ORACLE"),
]


def task_id_of(op):
    t = op.get("task")
    if isinstance(t, str):
        return t
    if isinstance(t, dict):
        return t.get("id")
    return None


def guess_agents(op, path, board):
    """Ordered plausible issuing agents for an op payload."""
    out = []
    t = op.get("task")
    if isinstance(t, dict) and t.get("requester") in team.AGENTS:
        out.append(t["requester"])
    parts = str(path).replace("\\", "/").split("/")
    if "work" in parts:
        i = parts.index("work")
        if i + 1 < len(parts) and parts[i + 1] in LANE_DIRS:
            out.append(LANE_DIRS[parts[i + 1]])
    tid = task_id_of(op) or ""
    for prefix, agent in ID_PREFIX:
        if tid.startswith(prefix + "-") or tid.startswith(prefix):
            out.append(agent)
            break
    if op.get("action") in ("claim", "finish", "checkpoint", "block", "release", "resume"):
        row = next((x for x in board["tasks"] if x["id"] == tid), None)
        if row is not None:
            for k in ("agent", "assigned_to", "requester"):
                if row.get(k) in team.AGENTS:
                    out.append(row[k])
    for a in sorted(team.AGENTS):
        out.append(a)
    seen, res = set(), []
    for a in out:
        if a and a not in seen:
            seen.add(a)
            res.append(a)
    return res


class ReplayError(Exception):
    """Fatal: the reconstructed board itself failed validation mid-replay."""


class OpReject(ValueError):
    """This op is invalid against the reconstructed state - a normal reject."""


def _quick_task_check(board):
    """Cheap per-op structural gate: the checks a corrupt add can violate.
    Full validate() still runs at intervals and at the end."""
    ids = [t["id"] for t in board["tasks"]]
    if len(ids) != len(set(ids)):
        raise OpReject("duplicate task id")
    for t in board["tasks"]:
        if t.get("kind") not in {"research", "request", "runtime",
                               "contradiction"}:
            raise OpReject("invalid task kind: %s" % t.get("id"))
        if t["status"] == "DONE" and not (t.get("result_refs")
                                        or t.get("retired")):
            raise OpReject("DONE without result refs: %s" % t["id"])


def try_apply(board, agent, op, session=None):
    """Apply op, restoring board state on failure. Raises the apply error."""
    rev = board["revision"]
    nhist = len(board["history"])
    nckp = len(board.get("checkpoints", []))
    agents = deepcopy(board["agents"])
    tid = task_id_of(op)
    idx = next((i for i, x in enumerate(board["tasks"]) if x["id"] == tid), None)
    old_task = deepcopy(board["tasks"][idx]) if idx is not None else None
    try:
        team.apply(board, agent, deepcopy(op), session)
        _quick_task_check(board)
    except Exception:
        board["revision"] = rev
        del board["history"][nhist:]
        if "checkpoints" in board:
            del board["checkpoints"][nckp:]
        board["agents"] = agents
        if op.get("action") == "add":
            if idx is not None:
                board["tasks"][idx] = old_task  # defensive: restore in place
            else:
                board["tasks"] = [t for t in board["tasks"] if t["id"] != tid]
        elif old_task is not None:
            board["tasks"][idx] = old_task
        raise


def receipts_of(board, start=0):
    """canon(op) -> list of history indices."""
    rec = {}
    for i, e in enumerate(board["history"][start:], start=start):
        rec.setdefault(canon(e.get("operation")), []).append(i)
    return rec


def replay_ops(board, ops, label, log, used_receipts=None):
    """Replay candidate ops in (mtime, file) order with fixpoint retries.

    `ops` items: {op, file, mtime, source}. Returns (applied, remaining).
    Each applied entry records the agent that succeeded and the new revision.
    """
    pending = list(ops)
    applied = []
    passes = 0
    while pending and passes < 4:
        passes += 1
        n0 = len(pending)
        still = []
        for item in pending:
            op = item["op"]
            err = None
            agents = guess_agents(op, item.get("file"), board)
            done = False
            for agent in agents:
                try:
                    try_apply(board, agent, op,
                              session="recover/" + label)
                    applied.append(dict(item, agent=agent,
                                        revision=board["revision"],
                                        pass_no=passes))
                    done = True
                    break
                except ReplayError:
                    raise  # mid-replay validation failure is fatal, not a bad op
                except Exception as e:
                    err = str(e)
            if not done:
                item = dict(item, last_error=err)
                still.append(item)
        pending = still
        log.append(f"{label} pass {passes}: applied {n0 - len(pending)}, "
                   f"pending {len(pending)}")
        if len(pending) == n0:
            break
    return applied, pending


def state_matches(board, op):
    """For a failed post-reset op, is the task already in the post-state the
    op would have produced? If so this is a duplicate of a recovered op."""
    tid = task_id_of(op)
    row = next((x for x in board["tasks"] if x["id"] == tid), None)
    a = op.get("action")
    if a == "add":
        if row is None:
            return None
        new = op["task"]
        same_core = all(row.get(k) == new.get(k)
                        for k in ("target", "scope", "kind", "priority"))
        return ("duplicate add; task exists" +
                ("" if same_core else " (CONTENT DIVERGES - flag)"))
    if row is None:
        return None
    if a == "claim" and row["status"] == "ACTIVE":
        return "duplicate claim; already ACTIVE by " + str(row.get("agent"))
    if a == "finish" and row["status"] == "DONE":
        return "duplicate finish; already DONE"
    if a in ("release", "resume") and row["status"] == "READY":
        return "duplicate %s; already READY" % a
    if a == "block" and row["status"] == "BLOCKED":
        return "duplicate block; already BLOCKED"
    return None


def build(args):
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    log = []

    witness = json.loads(Path(args.witness).read_text(encoding="utf-8"))
    team.validate(witness)

    # Bulk replay runs every structural require() inside apply() but defers
    # the full validate() deepcopy-equality pass to checkpoints and the end -
    # the op-level requires are what prove an op's transition was legal.
    real_validate = team.validate
    pending_checks = [0]
    check_failures = []
    def _light_validate(b):
        pending_checks[0] += 1
        if pending_checks[0] % 40 == 0:
            try:
                real_validate(b)
            except Exception as e:
                check_failures.append(str(e))
                raise ReplayError(
                    "mid-replay board validation failed: %s" % e)
    team.validate = _light_validate
    log.append(f"witness: rev {witness['revision']}, "
               f"{len(witness['tasks'])} tasks, {len(witness['history'])} history, "
               f"sha {board_sha(witness)[:16]}")

    fork = json.loads(Path(args.fork).read_text(encoding="utf-8"))
    base_nhist = len(witness["history"])  # baseline prefix inside fork history
    # locate the fork boundary: the longest witness-history prefix inside fork
    fh = fork["history"]
    b = 0
    while b < len(fh) and b < len(witness["history"]) and \
            canon(fh[b]) == canon(witness["history"][b]):
        b += 1
    # the fork's own baseline may end before witness start; find the divergence
    # point between fork history and witness history
    log.append(f"fork: rev {fork['revision']}, {len(fh)} history; "
               f"shared prefix with witness: {b} entries")
    fork_tail = fh[b:]
    wit_tail = witness["history"][b:]
    log.append(f"witness-only entries after divergence: {len(wit_tail)}; "
               f"fork-only entries: {len(fork_tail)}")

    board = deepcopy(witness)
    inv = json.loads(Path(args.inventory).read_text(encoding="utf-8"))
    wit_receipts = receipts_of(witness)
    fork_receipt_keys = {canon(e.get("operation")) for e in fork_tail}

    w0 = parse_ts(args.window_start)
    r0 = parse_ts(args.reset_time)

    # Tail candidates: no receipt in witness, plausibly applied after the
    # witness was captured (file mtime past window start) and before the
    # reset. Ops written after the reset with no fork receipt are drafts /
    # unapplied retries - listed, never applied.
    cands, drafts = [], []
    for row in inv:
        c = canon(row["op"])
        if c in wit_receipts:
            continue  # already inside witness - receipt exists
        if row["mtime"] <= w0:
            drafts.append(dict(row, why="older than window; no receipt"))
            continue
        item = dict(op=row["op"], file=row["file"], mtime=row["mtime"],
                    mt=row.get("mt"), source="op-file")
        if row["mtime"] <= r0:
            cands.append(item)
        else:
            drafts.append(dict(row, why="written after reset; no fork receipt"))

    cands.sort(key=lambda x: (x["mtime"], x["file"]))
    log.append(f"tail candidates (unreceipted, in-window): {len(cands)}; "
               f"drafts/excluded: {len(drafts)}")

    applied_tail, rejected = replay_ops(board, cands, "tail", log)

    # Post-reset merge: fork-tail entries are authoritative receipts.
    merged, dupes, ambig = [], [], []
    applied_canon = {canon(a["op"]) for a in applied_tail}
    for i, e in enumerate(fork_tail):
        op = e.get("operation")
        c = canon(op)
        if c in applied_canon:
            dupes.append(dict(index=b + i, at=e.get("at"), agent=e.get("agent"),
                              op=op, note="post-reset op duplicates a "
                                          "recovered pre-reset op"))
            continue
        try:
            try_apply(board, e["agent"], op, session=e.get("session"))
            merged.append(dict(index=b + i, at=e.get("at"),
                               agent=e.get("agent"), op=op,
                               revision=board["revision"]))
        except Exception as ex:
            m = state_matches(board, op)
            if m:
                dupes.append(dict(index=b + i, at=e.get("at"),
                                  agent=e.get("agent"), op=op, note=m))
            else:
                ambig.append(dict(index=b + i, at=e.get("at"),
                                  agent=e.get("agent"), op=op,
                                  error=str(ex)))
    log.append(f"post-reset: merged {len(merged)}, duplicate receipts "
               f"{len(dupes)}, ambiguous {len(ambig)}")

    # ---- validation report on the candidate ----
    team.validate = real_validate
    team.validate(board)
    done_pre = {t["id"] for t in witness["tasks"] if t["status"] == "DONE"}
    done_now = {t["id"] for t in board["tasks"] if t["status"] == "DONE"}
    lost_done = sorted(done_pre - done_now)
    ids = {t["id"] for t in board["tasks"]}
    baddeps = sorted({d for t in board["tasks"] for d in t["dependencies"]
                      if d not in ids})
    report = dict(
        witness_revision=witness["revision"],
        witness_sha=board_sha(witness),
        candidate_revision=board["revision"],
        candidate_sha=board_sha(board),
        candidate_tasks=len(board["tasks"]),
        candidate_done=len(done_now),
        witness_done=len(done_pre),
        done_ids_lost_in_replay=lost_done,
        dangling_dependencies=baddeps,
        tail_applied=len(applied_tail),
        tail_rejected=[dict(file=r["file"], task=task_id_of(r["op"]),
                            action=r["op"].get("action"),
                            error=r.get("last_error")) for r in rejected],
        drafts_excluded=[dict(file=d["file"], why=d["why"]) for d in drafts],
        post_reset_merged=len(merged),
        post_reset_duplicates=len(dupes),
        post_reset_ambiguous=[dict(index=a["index"], agent=a["agent"],
                                   task=task_id_of(a["op"]),
                                   action=a["op"].get("action"),
                                   error=a["error"]) for a in ambig],
        log=log,
    )
    (outdir / "TEAM.candidate.json").write_text(
        json.dumps(board, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (outdir / "recovery-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    (outdir / "applied-ops.jsonl").write_text(
        "\n".join(canon(dict(src="tail", **a)) for a in applied_tail) + "\n" +
        "\n".join(canon(dict(src="post-reset", **m)) for m in merged),
        encoding="utf-8")
    print(json.dumps({k: report[k] for k in
                      ("witness_revision", "candidate_revision",
                       "candidate_tasks", "candidate_done", "tail_applied",
                       "post_reset_merged", "post_reset_duplicates",
                       "post_reset_ambiguous")}, indent=2))
    print("\n".join(log))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["build"])
    p.add_argument("--witness", required=True)
    p.add_argument("--fork", required=True)
    p.add_argument("--inventory", required=True)
    p.add_argument("--window-start", required=True)
    p.add_argument("--reset-time", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    try:
        build(args)
    except (ValueError, KeyError, OSError) as e:
        p.exit(1, str(e) + "\n")


if __name__ == "__main__":
    main()
