# ASTRA labelled child-entry substitution: original imported definitions below are unchanged.
if __name__ == '__main__':
    import json,os,sys
    receipt={'argv':sys.argv,'exit_code':int(os.environ['ASTRA_WRITER_CONTROL_EXIT']),'stdout':os.environ['ASTRA_WRITER_CONTROL_STDOUT'],'real_writer_executed':False}
    fp=sys.argv[sys.argv.index('--file')+1]
    receipt['received_op']=json.load(open(fp,encoding='utf-8'))
    json.dump(receipt,open(os.environ['ASTRA_WRITER_CONTROL_RECEIPT'],'w',encoding='utf-8'),indent=2)
    sys.stdout.write(receipt['stdout'])
    sys.exit(receipt['exit_code'])
#!/usr/bin/env python3
"""Team claims and handoffs; atomic JSON transactions, never a semantic authority.

python team.py show [--agent ASTRA]
python team.py apply --agent ASTRA --file operation.json
python team.py validate
All paths default to the canonical checkout containing this script. No external packages.
Since 2026-09-12 `apply` also records the issuing session on the history entry when --session (or
$TEAM_SESSION) is given, so that one agent id served by two sessions is visible from the board.
"""
import argparse
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[4]
BOARD = ROOT / "Database/FFXII TZA/_index/_inbox/TEAM.json"
# The durability journal lives outside the board's own directory: the
# 2026-09-25 incident showed TEAM.json can be overwritten in place by a
# stale in-memory copy, and a restore of _inbox must not take the journal
# with it. work/ is the fleet's existing evidence area.
JOURNAL_DIR = ROOT / "Database/Tools/work/_team-journal"
# The fixed production identities. SWE2 was one generic worker until 2026-09-13, when it was split
# into eight lanes; the old "SWE2" id migrated to SWE2-CONTRACT, which is where its active claim and
# its routed request went. History entries keep the id that was current when they were written -
# renaming them would falsify the record. See TEAM.md staffing and REVIEW-POLICY.md for the tiers.
AGENTS = {
    "FABLE", "OPUS", "ASTRA",
    "SWE2-FRONTIER", "SWE2-EC7", "SWE2-CONTRACT", "SWE2-STRUCT",
    "SWE2-DATA", "SWE2-ORACLE", "SWE2-AUDIT-SEM", "SWE2-AUDIT-SPEC",
}
STATES = {"READY", "ACTIVE", "BLOCKED", "DONE"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def nonempty(row, names):
    for name in names:
        require(isinstance(row.get(name), str) and row[name].strip(), "missing " + name)


def resource(r):
    nonempty(r, ["key"])
    k = r["key"]
    require(k == k.casefold() == k.strip() and "\\" not in k
            and all(part not in {"", ".", ".."} for part in k.split("/")),
            "resource keys must be lowercase normalized paths/identities")
    if k.startswith("file:"):
        require(k[5:] and not k[5:].startswith("/") and ":" not in k[5:],
                "file keys must be repository-relative")
    require(not ((k.startswith("file:") or k.startswith("@")) and "start" in r),
            "files and exclusive resources cannot be range-split")
    require(("start" in r) == ("end" in r), "range needs start and end")
    if "start" in r:
        require(type(r["start"]) is int and type(r["end"]) is int
                and 0 <= r["start"] < r["end"], "range must be nonempty [start,end)")


def overlap(a, b):
    x, y = a["key"], b["key"]
    if x != y:
        return x.startswith(y + "/") or y.startswith(x + "/")
    if "start" not in a or "start" not in b:
        return True
    return a["start"] < b["end"] and b["start"] < a["end"]


def hold_set(t):
    # An ACTIVE task holds what its claim actually named (claimed_resources),
    # defaulting to its declared resources when the claim listed none.
    return t.get("claimed_resources") or t["resources"]


def conflicts(board, task):
    return [t["id"] for t in board["tasks"] if t["status"] == "ACTIVE"
            and t["id"] != task["id"]
            and any(overlap(a, b) for a in hold_set(t) for b in hold_set(task))]


def ready(board, agent=None):
    done = {t["id"] for t in board["tasks"] if t["status"] == "DONE"}
    return sorted([t for t in board["tasks"] if t["status"] == "READY"
                   and set(t["dependencies"]) <= done and not conflicts(board, t)
                   and (t.get("kind") == "research" or not t.get("assigned_to")
                        or t["assigned_to"] == agent or agent is None)],
                  key=lambda t: (t["priority"], t["id"]))


def refresh(board):
    for name, agent in board["agents"].items():
        active = [t for t in board["tasks"] if t["agent"] == name and t["status"] == "ACTIVE"]
        blocked = [t for t in board["tasks"] if t["agent"] == name and t["status"] == "BLOCKED"]
        agent.update(current_task=[t["id"] for t in active],
                     claimed_scope=[r for t in active for r in hold_set(t)],
                     dependencies=sorted({d for t in active + blocked for d in t["dependencies"]}),
                     blockers=[{"task": t["id"], "reason": t["checkpoint"]} for t in blocked],
                     status="ACTIVE" if active else "READY")


def validate(board):
    require(board["schema_version"] == 1, "unsupported schema")
    require(board["phase"] in {"DATABASE", "RECONSTRUCTION"}, "invalid phase")
    require(set(board["agents"]) == AGENTS, "board must carry exactly the AGENTS identities")
    for name, a in board["agents"].items():
        require(a["agent_id"] == name, "identity mismatch")
        nonempty(a, ["primary_specialty", "last_checkpoint", "status"])
        for field in ["current_task", "claimed_scope", "dependencies", "blockers"]:
            require(isinstance(a[field], list), "agent " + field + " must be a list")
    ids = [t["id"] for t in board["tasks"]]
    require(len(ids) == len(set(ids)), "duplicate task id")
    for t in board["tasks"]:
        nonempty(t, ["id", "target", "scope", "completion", "checkpoint", "updated_at"])
        require(re.fullmatch(r"[A-Z][A-Z0-9-]+", t["id"]), "invalid task id")
        require(t["status"] in STATES, "invalid status")
        require(t.get("kind") in {"research", "request", "runtime", "contradiction"}, "invalid task kind")
        require(t["priority"] in ["P0", "P1", "P2", "P3"], "invalid priority")
        require(t["agent"] in AGENTS | {None}, "invalid owner")
        require(t.get("assigned_to") in AGENTS | {None}, "invalid request recipient")
        require(isinstance(t["dependencies"], list) and set(t["dependencies"]) <= set(ids)
                and t["id"] not in t["dependencies"], "unknown/self dependency")
        require(isinstance(t["resources"], list) and t["resources"], "claim resources required")
        for r in t["resources"]:
            resource(r)
        if t["status"] == "ACTIVE":
            require(t["agent"] in AGENTS and t.get("started_at"), "active claim needs owner/start")
            require(not conflicts(board, t), "overlap: " + t["id"])
        if t.get("kind") in {"request", "runtime", "contradiction"}:
            nonempty(t, ["requester", "assigned_to", "question", "known_evidence",
                         "missing_information", "why_it_matters", "what_is_blocked"])
            require(t["requester"] in AGENTS, "invalid requester")
        if t.get("kind") == "contradiction":
            nonempty(t, ["original_claim", "counter_evidence", "affected_documents"])
        if t["status"] == "DONE":
            # A retired row is an adjudicated closure - its durable record is the history
            # entry, so result_refs are not required of it. Any OTHER DONE row without
            # refs is exactly the board wedge of 2026-09-25 (a record written outside
            # `finish`); the check stays loud rather than self-repairing.
            require(t.get("result_refs") or t.get("retired"),
                    "completion needs durable result references")
    def walk(key, visiting):
        require(key not in visiting, "dependency cycle")
        for dep in next(t for t in board["tasks"] if t["id"] == key)["dependencies"]:
            walk(dep, visiting | {key})
    for key in ids:
        walk(key, set())
    expected = deepcopy(board)
    refresh(expected)
    require(expected["agents"] == board["agents"], "agent summaries disagree with claims")


def apply(board, agent, op, session=None):
    require(agent in AGENTS, "unknown agent")
    action = op["action"]
    stamp = now()
    if action == "add":
        t = deepcopy(op["task"])
        require(t["id"] not in {x["id"] for x in board["tasks"]}, "task already exists")
        if t.get("kind") in {"request", "runtime", "contradiction"}:
            require(t.get("requester") == agent, "requester must be author")
        t.update(agent=None, status="READY", started_at=None, updated_at=stamp,
                 checkpoint="Queued by " + agent)
        board["tasks"].append(t)
    elif action == "note":
        # Board-level execution note (the `checkpoints` array). Before this
        # action existed, lanes appended notes by read-modify-writing the whole
        # file outside the lock - the 2026-09-25 rollback was exactly such a
        # write from an 11-hour-stale in-memory copy. This is the only
        # sanctioned path.
        nonempty(op, ["note"])
        board.setdefault("checkpoints", []).append(
            {"ts": stamp[:10], "author": agent, "note": op["note"]})
    else:
        t = next((t for t in board["tasks"] if t["id"] == op["task"]), None)
        require(t is not None, "unknown task")
        if action == "claim":
            # A claim may name its own hold set; omitted keeps the task's declared
            # resources (previous behavior). Whatever is named is checked
            # all-or-nothing and recorded as the actual hold. Before this the op's
            # resources were never evaluated: a contested key mixed with free ones
            # was silently dropped (OPUS-REQ-FRONTIER-TEAM-PY-GRANTS-PARTIAL-
            # CLAIMS-SILENTLY) and a requester could never claim against a narrower
            # set than the task declared (OPUS-REQ-FRONTIER-DIRECTORY-CLAIM-
            # STARVES-PEER-REQUESTS).
            res_keys = t["resources"]
            hold = op.get("resources")
            if hold is not None:
                require(isinstance(hold, list) and hold,
                        "claim resources must be a non-empty list")
                res_keys = []
                for r in hold:
                    if isinstance(r, str):
                        r = {"key": r}
                    require(isinstance(r, dict), "claim resource must be {key} or a key string")
                    resource(r)
                    res_keys.append(r)
            done = {x["id"] for x in board["tasks"] if x["status"] == "DONE"}
            require(t["status"] == "READY" and set(t["dependencies"]) <= done
                    and (t.get("kind") == "research" or not t.get("assigned_to")
                         or t["assigned_to"] == agent),
                    "not ready for this agent; check dependencies/claims/recipient")
            probe = dict(t, resources=res_keys)
            probe.pop("claimed_resources", None)
            held = conflicts(board, probe)
            require(not held, "resource(s) held by: " + ", ".join(sorted(held)))
            t.update(agent=agent, status="ACTIVE", started_at=stamp)
            if hold is not None:
                t["claimed_resources"] = res_keys
        elif action in {"release_publication", "retire"}:
            # Adjudicated board operations (TEAM.md's stopped-publisher rule and the
            # UC1 circular-row retirement): SWE2-FRONTIER or OPUS only, never the
            # holder and never an actor waiting on the released key.
            require(agent in {"SWE2-FRONTIER", "OPUS"},
                    "only FRONTIER or OPUS may adjudicate")
            if action == "release_publication":
                require(t["status"] == "ACTIVE" and t.get("agent"),
                        "target is not an active claim")
                require(t["agent"] != agent, "the holder must release its own lease")
                require(any(r["key"] == "@publication" for r in hold_set(t)),
                        "target does not hold @publication")
                require(not any(x["status"] in {"READY", "ACTIVE", "BLOCKED"}
                                and x["id"] != t["id"]
                                and (x.get("agent") == agent
                                     or (x.get("agent") is None
                                         and x.get("assigned_to") == agent))
                                and any(r["key"] == "@publication" for r in x["resources"])
                                for x in board["tasks"]),
                        "the adjudicator must not be the next claimant")
                # The three TEAM.md measurements, verified where the board carries
                # the data and cited where it does not (commit/process/path checks
                # are external evidence, carried as citations).
                try:
                    idle = (datetime.now(timezone.utc)
                            - datetime.fromisoformat(t["updated_at"])).total_seconds()
                except (TypeError, ValueError):
                    idle = -1
                require(idle >= 6 * 3600,
                        "checkpoint must be at least 6 hours old")
                req = next((x for x in board["tasks"]
                            if x["id"] == op.get("unanswered_request")), None)
                require(req is not None and req["status"] == "READY"
                        and req.get("assigned_to") == t["agent"],
                        "unanswered_request must name a READY request addressed to the holder")
                try:
                    req_age = (datetime.now(timezone.utc)
                               - datetime.fromisoformat(req["updated_at"])).total_seconds()
                    quiet = (datetime.now(timezone.utc)
                             - datetime.fromisoformat(op.get("no_activity_since"))
                             ).total_seconds()
                except (TypeError, ValueError):
                    req_age = quiet = -1
                require(req_age >= 2 * 3600,
                        "the checkpoint/release request must be at least 2 hours old")
                require(quiet >= 2 * 3600,
                        "no_activity_since must be an ISO timestamp at least 2 hours old")
                t["claimed_resources"] = [r for r in hold_set(t)
                                          if r["key"] != "@publication"]
                t.setdefault("history", []).append(
                    {"at": stamp, "event": "adjudicated @publication release",
                     "by": agent,
                     "checkpoint_idle_s": int(idle),
                     "unanswered_request": op["unanswered_request"],
                     "no_activity_since": op["no_activity_since"]})
            else:  # retire
                require(t["status"] in {"READY", "BLOCKED"},
                        "only an unclaimed row can be retired")
                # Request-shaped rows are filed under BOTH kinds across the
                # fleet (FABLE-REQ-ASTRA-GF4-* is kind=research); the guard is
                # about request semantics, not the label.
                require(t.get("kind") in {"request", "research"},
                        "retire is board hygiene for request-shaped rows only")
                # Never write an empty result_refs: [] is falsy and would trip the
                # DONE-row check above - the same wedge class a bypassing writer
                # caused on 2026-09-25. `retired` is the marker the check accepts.
                t.update(status="DONE", retired=True)
                if op.get("result_refs"):
                    t["result_refs"] = op["result_refs"]
        elif action in {"checkpoint", "finish", "block", "release", "resume"}:
            require(t["agent"] == agent, "only the owner can change a claim")
            require(t["status"] == ("BLOCKED" if action == "resume" else "ACTIVE"),
                    "invalid transition")
            if action == "finish":
                require(isinstance(op.get("result_refs"), list) and op["result_refs"],
                        "result_refs must point to durable evidence/handoff")
                t.update(status="DONE", result_refs=op["result_refs"])
            if action == "block":
                require(op.get("resume_when"), "block needs resume_when")
                t.update(status="BLOCKED", resume_when=op["resume_when"])
                if "dependencies" in op:
                    t["dependencies"] = op["dependencies"]
            if action in {"release", "resume"}:
                t.update(status="READY", agent=None)
                t.pop("claimed_resources", None)
        else:
            raise ValueError("unknown action")
        nonempty(op, ["note"])
        t.update(checkpoint=op["note"], updated_at=stamp)
    board["agents"][agent]["last_checkpoint"] = stamp
    entry = {"at": stamp, "agent": agent, "operation": deepcopy(op)}
    if session:
        # The issuing SESSION, not only the identity: two sessions answering as one agent id both pass
        # validate, and without this field the duplication is visible only when their operations happen
        # not to interleave (OPUS-NOTICE-SWAP-MIRROR, 2026-09-12). Optional; older entries lack it.
        entry["session"] = session
    board["history"].append(entry)
    board["revision"] += 1
    refresh(board)
    validate(board)


# ---------------------------------------------------------------------------
# Generated CURRENT blocks - operative headers (2026-09-26 freshness directive)
#
# Lane inbox files carry a generated "current" block: a small projection of the
# board the lane reads at resume/handoff instead of trusting hand-maintained
# NEXT lines and counts (which silently went stale after every peer op and,
# once, after a board rollback). The block stamps board_rev + epoch and a
# queue_sha of exactly the selection-relevant state for that agent - an
# unrelated peer op moves board_rev without touching queue_sha, while an
# accepted review, a reopen, a new request or a claim changes it. Authored
# notes and dated history live OUTSIDE the generated region; never hand-edit
# between the markers.

CURRENT_BEGIN = "<!-- TEAM-CURRENT:begin"
CURRENT_END = "<!-- TEAM-CURRENT:end -->"
_CURRENT_HEAD = re.compile(
    r"<!--\s*TEAM-CURRENT:begin\s+agent=(?P<agent>[A-Z0-9-]+)"
    r"\s+board_rev=(?P<rev>\d+)\s+epoch=(?P<epoch>\d+)"
    r"\s+queue_sha=(?P<sha>[0-9a-f]+)")


def _queue_view(board, agent):
    """The selection-relevant slice for one identity. Everything a resume or
    work-selection needs to re-derive; nothing else (so peer churn elsewhere
    does not mark this view stale)."""
    r = ready(board, agent)
    targeted = [t for t in r if t.get("assigned_to") == agent]
    pool = sorted(t["id"] for t in r if not t.get("assigned_to"))
    active = sorted(t["id"] for t in board["tasks"]
                    if t["status"] == "ACTIVE" and t.get("agent") == agent)
    blocked = sorted(t["id"] for t in board["tasks"]
                     if t["status"] == "BLOCKED" and t.get("agent") == agent)
    holds = sorted({x["key"] for t in board["tasks"]
                    if t["status"] == "ACTIVE" and t.get("agent") == agent
                    for x in hold_set(t)})
    return {"active": active, "blocked": blocked,
            "targeted": [[t["priority"], t["id"]] for t in targeted],
            "pool": pool, "holds": holds}


def current_state(board, agent):
    """(board_rev, epoch, queue_sha) - the fingerprint an embed is checked against."""
    view = _queue_view(board, agent)
    return (board["revision"], board.get("recovery_epoch", 0),
            _sha_text(json.dumps(view, sort_keys=True))[:16])


def current_block(board, agent):
    """Pure: the generated block text for one agent's operative header."""
    rev, epoch, sha = current_state(board, agent)
    view = _queue_view(board, agent)
    tgt = ", ".join("%s %s" % (p, i) for p, i in view["targeted"]) or "none"
    return "\n".join([
        "%s agent=%s board_rev=%d epoch=%d queue_sha=%s -->"
        % (CURRENT_BEGIN, agent, rev, epoch, sha),
        "> generated %s by `team.py current` - do not hand-edit; hand-maintained"
        % now(),
        "> counts and NEXT lines anywhere else are superseded by this block.",
        "> ACTIVE: %s" % (", ".join(view["active"]) or "none"),
        "> READY addressed to you: %s" % tgt,
        "> READY pool: %d | BLOCKED: %d" % (len(view["pool"]), len(view["blocked"])),
        CURRENT_END])


def check_current(text, board):
    """(agent, verdict) per embedded block. CURRENT = board unchanged for this
    view; MOVED = board advanced but this agent's queue did not (the embed may
    still select correctly; refresh at the next boundary); STALE-QUEUE = the
    embedded selections no longer match the board - never act on them."""
    out = []
    for m in _CURRENT_HEAD.finditer(text):
        agent = m.group("agent")
        line = text[m.start():text.find("\n", m.start())]
        if "stale-inputs" in line:
            out.append((agent, "STALE-LABELLED (inputs moved during generation)"))
            continue
        if agent not in AGENTS:
            out.append((agent, "UNKNOWN-AGENT"))
            continue
        rev, epoch, sha = current_state(board, agent)
        if sha != m.group("sha"):
            out.append((agent, "STALE-QUEUE rev %s->%s" % (m.group("rev"), rev)))
        elif rev != int(m.group("rev")) or epoch != int(m.group("epoch")):
            out.append((agent, "MOVED rev %s->%s (queue unchanged)"
                        % (m.group("rev"), rev)))
        else:
            out.append((agent, "CURRENT"))
    return out


def write_current(text, agent, board, stale=False):
    """Return `text` with agent's generated block refreshed (or inserted at the
    top when absent). stale=True labels the block honestly when the inputs
    moved during generation."""
    block = current_block(board, agent)
    if stale:
        block = block.replace(" -->", " stale-inputs -->", 1)
    for m in _CURRENT_HEAD.finditer(text):
        if m.group("agent") != agent:
            continue
        start = m.start()
        end = text.find(CURRENT_END, start)
        require(end != -1, "TEAM-CURRENT block opened but never closed")
        end += len(CURRENT_END)
        return text[:start] + block + text[end:]
    return block + "\n\n" + text.lstrip("\n")


# ---------------------------------------------------------------------------
# Durability journal and rollback detection (2026-09-25 incident)
#
# The board is authoritative, but it is a single file that can be overwritten
# by anything with write access - on 2026-09-25 a long-running process dumped
# an 11-hour-stale in-memory copy over ~1,050 live operations. The journal is
# an append-only ledger in work/_team-journal/ (outside the board's restore
# domain) recording every write's revision, content hash and epoch. Any write
# path through `transaction` first proves the on-disk board still matches the
# journaled high-water; a rollback, a same-revision divergent file, an
# epoch-stale file or unjournaled advancement all fail closed with an
# incident, so a stale writer can never silently seed a fork.
#
# Journal record kinds:
#   genesis  - first sighting of a board this journal tracks
#   intent   - an accepted op about to be written (rev = board.rev + 1)
#   commit   - the write landed; carries the exact byte sha of the file
#   abort    - a pending intent whose write never landed (crash self-heal)
#   recovery - a coordinator-installed board; advances recovery_epoch and
#              invalidates every writer still holding an older-epoch copy

class BoardIncident(ValueError):
    """Raised when the on-disk board contradicts the durability journal."""


def _sha_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def journal_path(path):
    path = Path(path)
    if path.resolve() == BOARD.resolve():
        return JOURNAL_DIR / "TEAM.journal.jsonl"
    return path.parent / (path.name + ".journal.jsonl")


def journal_records(path):
    jp = journal_path(path)
    if not jp.exists():
        return []
    out = []
    for line in jp.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except ValueError:
                out.append({"kind": "corrupt", "raw": line[:200]})
    return out


def _journal_append(path, rec):
    jp = journal_path(path)
    jp.parent.mkdir(parents=True, exist_ok=True)
    rec = dict(rec)
    rec.setdefault("at", now())
    with open(jp, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def _tail_state(recs):
    """The journal's settled view: last commit/recovery/genesis record, plus
    any intent still pending after it (a crash between intent and commit)."""
    settled = None
    pending = None
    for r in recs:
        if r.get("kind") in ("commit", "recovery", "genesis"):
            settled = r
            pending = None
        elif r.get("kind") == "intent":
            pending = r
        elif r.get("kind") == "abort":
            pending = None
    return settled, pending


def check_against_journal(file_text, board, recs):
    """Compare the on-disk board with the journal. Returns a plan dict:
    {"action": ...} describing what transaction() must do next, or raises
    BoardIncident. Never mutates."""
    sha = _sha_text(file_text)
    epoch = board.get("recovery_epoch", 0)
    if not recs:
        return {"action": "genesis", "board_sha": sha, "epoch": epoch}
    if any(r.get("kind") == "corrupt" for r in recs[-5:]):
        raise BoardIncident("durability journal has corrupt tail records - "
                            "inspect " + str(journal_path(BOARD)) + " before writing")
    settled, pending = _tail_state(recs)
    if pending is not None:
        # Crash window: an intent was journaled but no commit followed.
        if board["revision"] == pending["rev"] - 1:
            return {"action": "abort", "pending": pending}
        last = board["history"][-1] if board.get("history") else {}
        if board["revision"] == pending["rev"] and _sha_text(
                json.dumps(last.get("operation"), sort_keys=True,
                           ensure_ascii=False)) == pending.get("op_sha"):
            return {"action": "heal", "pending": pending, "board_sha": sha}
        raise BoardIncident(
            "journal shows a pending intent for revision %d but the board is "
            "revision %d with a different last op - interrupted write; "
            "recover deliberately" % (pending["rev"], board["revision"]))
    if settled is None:
        return {"action": "genesis", "board_sha": sha, "epoch": epoch}
    jepoch = settled.get("epoch", 0)
    if epoch < jepoch:
        raise BoardIncident(
            "board carries recovery_epoch %s but the journal is at epoch %s - "
            "a pre-recovery copy was restored" % (epoch, jepoch))
    if epoch > jepoch:
        raise BoardIncident(
            "board claims recovery_epoch %s but the journal last settled at "
            "%s - unjournaled recovery install" % (epoch, jepoch))
    if board["revision"] < settled["rev"]:
        raise BoardIncident(
            "board rollback detected: on-disk revision %d is below the "
            "journaled high-water %d (sha %s); a stale copy was written "
            "over live state" % (board["revision"], settled["rev"],
                                 str(settled.get("board_sha"))[:12]))
    if board["revision"] == settled["rev"] and sha != settled.get("board_sha"):
        raise BoardIncident(
            "same-revision divergence: on-disk revision %d matches the "
            "journal but the content hash does not (expected %s, got %s)"
            % (board["revision"], str(settled.get("board_sha"))[:12],
               sha[:12]))
    if board["revision"] > settled["rev"]:
        raise BoardIncident(
            "unjournaled advancement: board revision %d is ahead of the "
            "journal's settled revision %d - writes bypassed the journal"
            % (board["revision"], settled["rev"]))
    return {"action": "ok"}


def board_status(path):
    """Non-mutating integrity verdict for callers (watchdog, publish guard).

    Returns (ok, detail). ok=False means the board is in incident state -
    dispatch and publication must stop, and the detail says why.

    The board and its journal are two separate reads, so a sanctioned
    commit landing between them produces a mixed snapshot - an old board
    text against a new journal mimics a rollback, a new board against an
    old journal mimics unjournaled advancement (ASTRA-NOTICE-FRONTIER-
    BOARD-PREFLIGHT-37999). A real incident persists across a re-read; a
    mixed snapshot does not. An incident verdict is therefore reported
    only after the same inconsistent reading repeats on a fresh pair."""
    last = None
    for _ in range(3):
        try:
            text = Path(path).read_text(encoding="utf-8")
            board = json.loads(text)
        except (OSError, ValueError) as e:
            return False, "board unreadable: %s" % e
        try:
            recs = journal_records(path)
            plan = check_against_journal(text, board, recs)
        except BoardIncident as e:
            last = str(e)
            continue
        return True, plan["action"]
    return False, last


def _write_board(path, board):
    """Serialize + atomic replace; returns (text, sha)."""
    text = json.dumps(board, indent=2, ensure_ascii=False) + "\n"
    fd, name = tempfile.mkstemp(prefix="TEAM-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        # WinError 5/32 are TRANSIENT at the tmp->target replace: a peer's
        # read handle or an antivirus scan denies the rename for milliseconds.
        # Observed live on 2026-09-28 - ASTRA's capture at
        # work/ASTRA/nav-mask-zero-count/board-write-failure.json shows
        # PermissionError WinError5 here with the board left fully consistent.
        # Bounded retry absorbs the transient class; anything else, or the
        # bound exhausted, propagates so the journaled intent stays pending
        # and the next transaction reconciles it - fail closed, not silent.
        for attempt in range(8):
            try:
                os.replace(name, path)
                break
            except PermissionError as e:
                if getattr(e, "winerror", None) in (5, 32) and attempt < 7:
                    time.sleep(0.025 * (1 << attempt))
                    continue
                raise
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return text, _sha_text(text)


def _open_failed_means_dead(err):
    """Whether an OpenProcess NULL proves the pid is gone. Only
    ERROR_INVALID_PARAMETER (87) means the pid does not exist; ACCESS_DENIED
    (5) and everything else mean it may be live but unqueryable - fail closed.
    """
    return err == 87


def _proc_start(pid):
    """Process creation time as an int, True for a live process whose start
    time could not be read, or None only when the process is provably dead
    (terminated, or OpenProcess reports the pid does not exist). An
    existing-but-unqueryable process returns True - fail closed.

    Windows: OpenProcess + WaitForSingleObject (OpenProcess alone succeeds on
    zombies while a handle lingers - only the wait proves termination) +
    GetProcessTimes. POSIX: os.kill(pid, 0); start-time probing is not
    portable here, so a live pid returns True and reuse fails safe - the lock
    is respected longer.
    """
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        # use_last_error so GetLastError below is reliable after OpenProcess.
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        h = k32.OpenProcess(0x1000 | 0x100000, False, pid)  # QUERY_LIMITED | SYNCHRONIZE
        if not h:
            # OpenProcess NULL is ambiguous. ERROR_INVALID_PARAMETER (87) means
            # the pid does not exist - the holder is dead. ERROR_ACCESS_DENIED
            # (5) means the process is LIVE but not queryable at our access
            # level (ASTRA-RETURN-FRONTIER-TEAM-ACCESS-DENIED-LIVENESS,
            # 2026-09-21: error 5 on a live holder mapped to dead here, and the
            # lock was reaped under it). Fail closed: only 87 proves dead.
            if _open_failed_means_dead(ctypes.get_last_error()):
                return None
            return True  # exists but not queryable - respect the lock
        try:
            if k32.WaitForSingleObject(h, 0) == 0:  # WAIT_OBJECT_0: terminated
                return None
            ct = wintypes.FILETIME()
            et = wintypes.FILETIME()
            kt = wintypes.FILETIME()
            ut = wintypes.FILETIME()
            ok = k32.GetProcessTimes(
                h, ctypes.byref(ct), ctypes.byref(et), ctypes.byref(kt), ctypes.byref(ut))
            if not ok:
                return True
            return (ct.dwHighDateTime << 32) | ct.dwLowDateTime
        finally:
            k32.CloseHandle(h)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return None
    except PermissionError:
        return True


def _holder_is_live(lock):
    """True when the recorded holder may still be running (fail-safe)."""
    try:
        holder = json.loads(lock.read_text(encoding="utf-8"))
        pid = int(holder["pid"])
    except (OSError, ValueError, KeyError, TypeError):
        return True  # unreadable record: cannot prove the holder dead
    started = _proc_start(pid)
    if started is None:
        return False  # pid is gone - the holder is certainly dead
    recorded = holder.get("started")
    if (recorded is not None and recorded is not True and started is not True
            and int(recorded) != int(started)):
        # pid was recycled: the process owning it is not our holder. A record
        # whose own start could not be read ("started": true) is not comparable
        # - int(True)==1 would reap a live holder (the 2026-09-27 same-revision
        # double-commit window; ACCESS_DENIED on OpenProcess is documented here).
        return False
    return True


#: How long to wait out a LIVE lock holder before giving up, and how often to look.
#  A board write takes milliseconds; anything past this is a wedged holder, not contention.
LOCK_WAIT_SECONDS = 30.0
LOCK_POLL_SECONDS = 0.25


if os.name == "nt":

    @contextmanager
    def _mutex_held(name):
        """Hold a named Windows mutex for the duration of the critical section.

        Kernel objects do not depend on a file path: no unlink, rename or stale
        record can admit a second holder, and a holder that dies mid-write
        surfaces to the next waiter as WAIT_ABANDONED (still ownership), not a
        wedge. The Local\\ namespace scopes it to this logon session."""
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.CreateMutexW.restype = wintypes.HANDLE
        k32.CreateMutexW.argtypes = [wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR]
        k32.WaitForSingleObject.restype = wintypes.DWORD
        k32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        k32.ReleaseMutex.argtypes = [wintypes.HANDLE]
        k32.CloseHandle.argtypes = [wintypes.HANDLE]
        h = k32.CreateMutexW(None, False, name)
        if not h:
            raise OSError(ctypes.get_last_error(), "CreateMutexW failed")
        acquired = False
        try:
            # No deadline here: a kernel mutex cannot wedge - if the holder dies
            # the wait returns WAIT_ABANDONED (still ownership). Timing out at
            # LOCK_WAIT_SECONDS was wrong: a holder can legitimately spend ~30s
            # inside waiting out a legacy peer's TEAM.lock, and under sustained
            # traffic that convoyed every other mutex waiter into expiry while
            # the board kept progressing (ASTRA-REQ-FRONTIER-PUBLICATION-MUTEX-
            # DELIVERY, three ordinary claims rejected). The 30s deadline lives
            # on the inner file-lock wait, where a wedged holder is possible.
            while True:
                r = k32.WaitForSingleObject(h, int(LOCK_POLL_SECONDS * 1000))
                if r in (0, 0x80):  # WAIT_OBJECT_0, WAIT_ABANDONED
                    acquired = True
                    break
                if r != 0x102:  # not WAIT_TIMEOUT: a real wait failure
                    raise OSError(ctypes.get_last_error(),
                                  "WaitForSingleObject returned %s" % r)
            yield
        finally:
            if acquired:
                k32.ReleaseMutex(h)
            k32.CloseHandle(h)


@contextmanager
def locked(path):
    """Take the board lock, waiting out a live holder instead of failing on sight.

    IT USED TO RAISE THE INSTANT A LIVE HOLDER EXISTED, and that is a worse failure than it
    looks, because of what sits downstream of it. `publish_paths.sh`'s own header records the
    2026-09-13 incident: an `add` died on a transient lock, its output was discarded, the six
    following claim retries all reported "unknown task", and by then nobody held @publication so
    the guard let the batch through as an unidentified publisher. It happened again on 2026-09-18,
    same shape - an `add` lost the lock race, forty subsequent claim attempts said "unknown task",
    and the diagnosis cost a round because the message names the TASK rather than the lock.

    A peer holds this lock for the length of one JSON rewrite. Waiting a fraction of a second is
    always right and failing is never right, so the wait is the default now. What is NOT changed:
    a DEAD holder is still reaped immediately (that is a different fault, and respecting it would
    wedge the board forever), and a holder still live after LOCK_WAIT_SECONDS still raises - but
    now says how long it waited and who it waited for, because at that point it IS a wedged holder
    and reaping it silently would be the dangerous choice.
    """
    if os.name == "nt":
        # Named kernel mutex FIRST: exclusion cannot be defeated by deleting or
        # renaming a file, and the OS releases it if the holder dies mid-write
        # (WAIT_ABANDONED still grants ownership, and the journal's
        # intent/commit check detects the torn write). The 2026-09-27
        # same-revision double-commits (35478/35479) came from the file-exists
        # scheme: once any unlink removed a live holder's lock - a manual reap
        # racing a rotating lock file was observed in the EC7 wake log - the
        # displaced holder's own finally:unlink deleted the NEXT generation's
        # file and the collision cascaded.
        # The TEAM.lock file is STILL created inside the mutex, with the same
        # wait/reap semantics, because a peer running an older team.py honours
        # only the file: holding both keeps exclusion correct for as long as an
        # unrefreshed writer may still be in flight. For new code the file is
        # just the diagnostic record of who holds the mutex.
        lock = path.with_suffix(".lock")
        with _mutex_held("Local\\XIIOnlineTEAMBoardLock"):
            deadline = time.time() + LOCK_WAIT_SECONDS
            reaps = 0
            while True:
                try:
                    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                    break
                except FileExistsError:
                    if not _holder_is_live(lock):
                        reaps += 1
                        if reaps > 20:
                            raise FileExistsError(
                                f"{lock}: lock raced after 20 reaps")
                        try:
                            lock.unlink()
                        except FileNotFoundError:
                            pass
                        continue
                    if time.time() >= deadline:
                        try:
                            who = lock.read_text(encoding="utf-8")
                        except OSError:
                            who = "unreadable"
                        raise FileExistsError(
                            f"{lock}: held by a LIVE process for more than "
                            f"{LOCK_WAIT_SECONDS:g}s - holder {who}. A wedged "
                            f"holder, not contention; establish whether it is "
                            f"alive, reap it deliberately, then re-run.")
                    time.sleep(LOCK_POLL_SECONDS)
            try:
                os.write(fd, json.dumps(
                    {"pid": os.getpid(), "at": now(),
                     "started": _proc_start(os.getpid())}).encode())
                os.close(fd)
                fd = None
                yield
            finally:
                if fd is not None:
                    os.close(fd)
                try:
                    lock.unlink()
                except OSError:
                    pass
        return
    lock = path.with_suffix(".lock")
    deadline = time.time() + LOCK_WAIT_SECONDS
    reaps = 0
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            if not _holder_is_live(lock):
                reaps += 1
                if reaps > 20:
                    raise FileExistsError(f"{lock}: lock raced after 20 reaps")
                try:
                    lock.unlink()
                except FileNotFoundError:
                    pass
                continue
            if time.time() >= deadline:
                try:
                    who = lock.read_text(encoding="utf-8")
                except OSError:
                    who = "unreadable"
                raise FileExistsError(
                    f"{lock}: held by a LIVE process for more than {LOCK_WAIT_SECONDS:g}s "
                    f"- holder {who}. That is a wedged holder, not contention; establish "
                    f"whether it is alive, reap it deliberately, then re-run.")
            time.sleep(LOCK_POLL_SECONDS)
    try:
        os.write(fd, json.dumps({"pid": os.getpid(), "at": now(),
                                 "started": _proc_start(os.getpid())}).encode())
        os.close(fd)
        fd = None
        yield
    finally:
        if fd is not None:
            os.close(fd)
        lock.unlink()


def transaction(path, agent, op, session=None, expect_revision=None):
    """Journal-checked board mutation. Under the lock: prove the on-disk board
    still matches the journaled high-water (fails closed on a rollback,
    divergence, stale epoch or unjournaled advancement), apply the op, journal
    the intent, write the file atomically, then journal the commit. A crash
    between intent and commit is detected and reconciled by the next
    transaction's check."""
    with locked(path):
        file_text = path.read_text(encoding="utf-8")
        board = json.loads(file_text)
        validate(board)
        plan = check_against_journal(file_text, board, journal_records(path))
        if plan["action"] == "genesis":
            _journal_append(path, {"kind": "genesis", "rev": board["revision"],
                                   "board_sha": plan["board_sha"],
                                   "epoch": plan["epoch"],
                                   "note": "journal bootstrap; not a trust "
                                           "assertion about earlier history"})
        elif plan["action"] == "abort":
            _journal_append(path, {"kind": "abort",
                                   "intent_rev": plan["pending"]["rev"],
                                   "note": "pending intent never landed"})
        elif plan["action"] == "heal":
            _journal_append(path, {"kind": "commit",
                                   "rev": plan["pending"]["rev"],
                                   "board_sha": plan["board_sha"],
                                   "op_sha": plan["pending"].get("op_sha"),
                                   "epoch": board.get("recovery_epoch", 0),
                                   "healed": True})
        if expect_revision is not None:
            require(expect_revision == board["revision"],
                    "expected revision %s, board is at %s"
                    % (expect_revision, board["revision"]))
        apply(board, agent, op, session)
        op_sha = _sha_text(json.dumps(op, sort_keys=True, ensure_ascii=False))
        _journal_append(path, {"kind": "intent", "rev": board["revision"],
                               "op_sha": op_sha, "agent": agent,
                               "session": session,
                               "epoch": board.get("recovery_epoch", 0)})
        text, sha = _write_board(path, board)
        _journal_append(path, {"kind": "commit", "rev": board["revision"],
                               "board_sha": sha, "op_sha": op_sha,
                               "agent": agent, "session": session,
                               "epoch": board.get("recovery_epoch", 0)})
    return board


def recover(path, candidate_path, note, agent, expect_revision=None,
            expect_sha=None):
    """Recovery-barrier install: replace the board with a validated candidate
    under the lock, only while the live board still matches the caller's
    captured preimage. Advances recovery_epoch so every pre-recovery copy and
    writer token is stale on its next touch. Returns the installed board."""
    path = Path(path)
    cand_text = Path(candidate_path).read_text(encoding="utf-8")
    cand_board = json.loads(cand_text)
    validate(cand_board)
    with locked(path):
        file_text = path.read_text(encoding="utf-8")
        cur = json.loads(file_text)
        cur_sha = _sha_text(file_text)
        if expect_revision is not None:
            require(cur["revision"] == expect_revision,
                    "preimage revision mismatch: live is %s, captured %s"
                    % (cur["revision"], expect_revision))
        if expect_sha is not None:
            require(cur_sha == expect_sha,
                    "preimage sha mismatch: the board moved since capture")
        epoch = cur.get("recovery_epoch", 0) + 1
        cand_board["recovery_epoch"] = epoch
        cand_board.setdefault("lineage", []).append(
            {"at": now(), "event": "recovery-install", "by": agent,
             "preimage_rev": cur["revision"], "preimage_sha": cur_sha,
             "note": note})
        text, sha = _write_board(path, cand_board)
        _journal_append(path, {"kind": "recovery", "epoch": epoch,
                               "rev": cand_board["revision"],
                               "from_rev": cur["revision"], "from_sha": cur_sha,
                               "to_rev": cand_board["revision"],
                               "board_sha": sha, "by": agent, "note": note})
    return cand_board


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["show", "validate", "apply", "boardcheck",
                                      "recover", "current"])
    p.add_argument("--agent", choices=sorted(AGENTS))
    p.add_argument("--file", type=Path)
    p.add_argument("--board", type=Path, default=BOARD, help="test fixtures only; live team uses default")
    p.add_argument("--session", default=os.environ.get("TEAM_SESSION") or None,
                   help="issuing session identifier recorded on the history entry (default: $TEAM_SESSION)")
    p.add_argument("--expect-revision", type=int,
                   help="apply only while the board is exactly this revision")
    p.add_argument("--install", type=Path,
                   help="recover: candidate board file to install")
    p.add_argument("--expect-sha", help="recover: sha256 the live board must still match")
    p.add_argument("--note", help="recover: receipt note")
    p.add_argument("--check", action="store_true",
                   help="current: verify embedded CURRENT blocks in --file against the live board")
    p.add_argument("--write", action="store_true",
                   help="current: regenerate the agent's CURRENT block inside --file")
    args = p.parse_args()
    try:
        if args.command == "boardcheck":
            ok, detail = board_status(args.board)
            if not ok:
                p.exit(2, "BOARD INCIDENT: " + detail + "\n")
            print("board ok:", detail)
            return
        if args.command == "recover":
            require(args.agent and args.install and args.note,
                    "recover needs --agent, --install and --note")
            b = recover(args.board, args.install, args.note, args.agent,
                        expect_revision=args.expect_revision,
                        expect_sha=args.expect_sha)
            print("Recovery installed: revision", b["revision"],
                  "recovery_epoch", b["recovery_epoch"])
            return
        if args.command == "current":
            if args.check:
                require(args.file, "current --check needs --file <inbox md>")
                text = args.file.read_text(encoding="utf-8")
                board = json.loads(args.board.read_text(encoding="utf-8"))
                verdicts = check_current(text, board)
                if not verdicts:
                    print("no TEAM-CURRENT blocks in", args.file)
                    return
                worst = 0
                for agent, verdict in verdicts:
                    print("%-16s %s" % (agent, verdict))
                    if verdict.startswith("STALE"):
                        worst = 2
                    elif verdict.startswith("MOVED"):
                        worst = max(worst, 0)
                p.exit(worst)
            if args.write:
                require(args.agent and args.file,
                        "current --write needs --agent and --file")
                text = args.file.read_text(encoding="utf-8")
                board = None
                out = None
                for _ in range(3):
                    t1 = args.board.read_text(encoding="utf-8")
                    cand = json.loads(t1)
                    if _sha_text(args.board.read_text(encoding="utf-8")) == _sha_text(t1):
                        board, out = cand, write_current(text, args.agent, cand)
                        break
                if out is None:
                    # inputs kept moving - write the honest label, never a
                    # silently-stale "current" block
                    board = json.loads(args.board.read_text(encoding="utf-8"))
                    out = write_current(text, args.agent, board, stale=True)
                    print("inputs moved during generation - block written",
                          "with stale-inputs label; rerun to refresh")
                args.file.write_text(out, encoding="utf-8")
                print("current block refreshed in %s (rev %d)"
                      % (args.file, board["revision"]))
                return
            require(args.agent, "current needs --agent (or --check/--write)")
            board = json.loads(args.board.read_text(encoding="utf-8"))
            print(current_block(board, args.agent))
            return
        if args.command == "apply":
            require(args.agent and args.file, "apply needs --agent and --file")
            b = transaction(args.board, args.agent, json.loads(args.file.read_text(encoding="utf-8-sig")), args.session,
                            expect_revision=args.expect_revision)
            print("Saved revision", b["revision"])
            # TEAM.md's publication rule is the seventh incident's lesson: every publish must go
            # through publish_paths.sh (private index, named paths only, directory refusal).
            # Agents who never read to that line still all run `apply` -- so the pointer lives
            # where a publishable action lands.
            if json.loads(args.file.read_text(encoding="utf-8-sig")).get("action") == "finish":
                print("note: publish document changes with publish_paths.sh <msg> <path>... "
                      "(TEAM.md) -- never `git add` of shared or unstaged-by-you paths")
        else:
            b = json.loads(args.board.read_text(encoding="utf-8"))
            validate(b)
            if args.command == "validate":
                print("PASS: %d identities (%s); claims, dependencies, handoffs and summaries valid"
                      % (len(AGENTS), ", ".join(sorted(AGENTS))))
            else:
                print(json.dumps({"phase": b["phase"], "revision": b["revision"], "agents": b["agents"],
                    "active": [t for t in b["tasks"] if t["status"] == "ACTIVE"],
                    "ready": ready(b, args.agent),
                    "requests": [t for t in b["tasks"] if t.get("assigned_to") == args.agent
                                 and t["status"] != "DONE"],
                    "blocked": [t for t in b["tasks"] if t["status"] == "BLOCKED"],
                    "contradictions": [t for t in b["tasks"] if t.get("kind") == "contradiction"
                                       and t["status"] != "DONE"]}, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as e:
        p.exit(1, str(e) + "\n")


if __name__ == "__main__":
    main()
