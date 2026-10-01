#!/usr/bin/env python3
"""goal_gate_hook.py -- Claude Code Stop hook: veto a /goal verdict the database
gate does not support.

Registered for the `Stop` event in the lanes' project settings
(C:/Users/Kristian/source/repos/.claude/settings.json). Claude Code 2.1.278 runs
user Stop hooks AFTER the built-in goal evaluator records its verdict -- observed
on this install: a `goal_status met=true` attachment at T, then the Stop hook ran
and its {"decision":"block"} turned the turn back. So this hook is the backstop
that makes a transcript's claim irrelevant to whether the session may end.

Behaviour:

* Only sessions whose latest `goal_status` condition names the FF12 database
  completion goal are gated. Sessions with no goal, or a different goal, pass
  through untouched.
* The transcript is authoritative for goal state, not the model's report: the
  last `goal_status` attachment wins. `failed` (evaluator declared impossible)
  is honoured -- that is a terminal verdict for the user to review, not a stop
  we convert into more work. `met` and active goals both run the gate.
* The gate is goal_gate.py: read-only, records-backed, fail closed. Its
  remaining=/next= output is injected as the block reason so the evaluator and
  the model see the concrete unmet obligation at this checkpoint.
* No-progress bound: consecutive blocks are counted per session in
  work/goal-gate/hook-state.json, keyed on the transcript's tool_use +
  tool_result record count - substantive work, not prose growth (a blocked
  continuation that only restates adds assistant text but no tool records,
  so the signature holds still). When the sig is unchanged on an
  already-triggered continuation (`stop_hook_active` true) or after two
  consecutive unchanged-sig blocks, the session is not producing work --
  typically context exhaustion AFTER checkpointing, observed live
  2026-09-26 on OPUS session 7af7f6f5 (306 vetoes, last 8 with zero tool
  growth, then the host block-cap paused it). The hook then ALLOWS the stop:
  a bounded pause for the lane's controller/user, and emits {} so no
  continuation feedback is injected. The pause is recorded in hook-state.json
  with the gate verdict, so the verdict stays readable independently of the
  stop permission. The built-in CLAUDE_CODE_STOP_HOOK_BLOCK_CAP remains the
  outer bound for storms this hook does not see; this hook never fights it.
* Fail closed: a gate error on a gated session blocks with the error named --
  unless the session is already in the no-progress state above, in which case
  the pause is allowed and the error is recorded in the pause record.
  Everything else passes {}.

Input contract (observed 2.1.278): stdin JSON carries session_id, cwd,
transcript_path, stop_hook_active, last_assistant_message, hook_event_name.
"""
import json, os, subprocess, sys, re

_HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(_HERE, "goal_gate.py")
STATE_DIR = os.path.normpath(os.path.join(_HERE, os.pardir, os.pardir, "work", "goal-gate"))
STATE_PATH = os.path.join(STATE_DIR, "hook-state.json")

# The condition signatures of the fleet's database-completion goals. A goal
# counts as DB-scoped when its condition names the game AND the database /
# reconstruction mission. Ordinary goals in this project pass through.
DB_GOAL_SIG = re.compile(r"(?i)(ffxii|ff12).*(database|reconstruction|knowledge)|(database|reconstruction).*(ffxii|ff12)")


def _emit(obj):
    sys.stdout.write(json.dumps(obj))


def _now_iso():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S+00:00")


def _last_goal(transcript_path):
    """Latest goal_status attachment in the transcript, or None."""
    try:
        size = os.path.getsize(transcript_path)
        # goal_status attachments are written at stop-attempt boundaries, i.e.
        # near the tail; read the last 4 MiB first, fall back to whole file.
        tail = min(size, 4 << 20)
        with open(transcript_path, "rb") as f:
            f.seek(-tail, os.SEEK_END)
            chunk = f.read().decode("utf-8", "replace")
        last = None
        for line in chunk.splitlines():
            if '"goal_status"' not in line:
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            att = rec.get("attachment") or {}
            if att.get("type") == "goal_status":
                last = att
        if last is None and tail < size:  # goal record may predate the tail
            with open(transcript_path, "rb") as f:
                for raw in f:
                    line = raw.decode("utf-8", "replace")
                    if '"goal_status"' not in line:
                        continue
                    try:
                        att = json.loads(line).get("attachment") or {}
                    except ValueError:
                        continue
                    if att.get("type") == "goal_status":
                        last = att
        return last
    except OSError:
        return None


def _load_state():
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_state(state):
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f)
    os.replace(tmp, STATE_PATH)


def _transcript_sig(path):
    """Tool-backed progress, not heartbeat text: the transcript's tool_use +
    tool_result record count. A lane that only restates adds text but no tool
    calls, so the signature holds still while assistant prose keeps growing.
    Counting records rather than bytes keeps a delayed flush from looking like
    progress -- the flush lands before the NEXT stop attempt, and one extra
    unchanged-sig block is the cost of being sure."""
    try:
        tools, carry = 0, b""
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                window = carry + chunk
                tools += window.count(b'"tool_use"')
                tools += window.count(b'"tool_result"')
                carry = window[-16:]
        return tools
    except OSError:
        return -1


def _run_gate():
    r = subprocess.run([sys.executable, GATE, "--json"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=600)
    try:
        return json.loads(r.stdout), None
    except ValueError:
        return None, "goal_gate.py produced no verdict (exit %s): %s" % (
            r.returncode, (r.stderr or r.stdout).strip()[:200])


def main():
    try:
        inp = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        return _emit({})
    if inp.get("hook_event_name") != "Stop":
        return _emit({})

    transcript = inp.get("transcript_path") or ""
    session = inp.get("session_id") or "unknown"
    goal = _last_goal(transcript) if transcript else None
    if goal is None or not DB_GOAL_SIG.search(str(goal.get("condition") or "")):
        return _emit({})  # not a database-goal session: never gated

    if goal.get("failed"):
        return _emit({})  # evaluator declared impossible: terminal, user reviews

    cleared_by_met = bool(goal.get("met"))

    # Track consecutive no-progress blocks for this session BEFORE the gate
    # runs, so the gate-error path can honour the same pause.
    state = _load_state()
    ent = state.get(session, {"blocks": 0, "sig": None, "noprogress": 0})
    sig = _transcript_sig(transcript)
    if ent.get("sig") == sig:
        ent["noprogress"] = ent.get("noprogress", 0) + 1
    else:
        ent["noprogress"] = 0
        ent.pop("paused", None)  # progress resumed: the pause is over
    ent["blocks"] = ent.get("blocks", 0) + 1
    ent["sig"] = sig

    # An already-triggered continuation (`stop_hook_active`) that produced no
    # new tool work, or two consecutive unchanged-sig blocks on a host that
    # never sets the flag: the session cannot convert another veto into work.
    # Allow a bounded pause; emit {} so no continuation feedback is injected.
    allow_pause = ent["noprogress"] >= 2 or (
        bool(inp.get("stop_hook_active")) and ent["noprogress"] >= 1)

    gate, err = _run_gate()
    verdict = (gate or {}).get("verdict")
    ent["last_verdict"] = verdict or ("GATE_ERROR: %s" % err)
    if verdict == "MET":
        # accepted evidence supports completion - allow, and record the
        # verdict so it stays readable independently of the stop permission
        state[session] = ent
        try:
            _save_state(state)
        except OSError:
            pass
        return _emit({})
    if allow_pause:
        # The pause record is what a controller or the next session reads;
        # the live verdict is preserved here, never promoted.
        ent["paused"] = {"at": _now_iso(), "reason": "no-progress",
                         "verdict": ent["last_verdict"],
                         "gate_error": err,
                         "blocks": ent["blocks"],
                         "remaining": (gate or {}).get("remaining")}
        state[session] = ent
        try:
            _save_state(state)
        except OSError:
            pass
        return _emit({})
    state[session] = ent
    try:
        _save_state(state)
    except OSError:
        pass

    if err is not None:
        return _emit({"decision": "block", "reason":
                      "DB_GOAL=NOT_MET -- the completion gate itself failed "
                      "closed (%s). Verify goal_gate.py, then continue." % err})

    prefix = ("The /goal evaluator recorded met while the gate is unmet; the "
              "verdict is void and the goal is cleared. Continue the named "
              "obligation now -- the lane controller restores the exact goal "
              "on resume; " if cleared_by_met else "")
    reason = ("%sDB_GOAL=NOT_MET remaining=%s next=%s "
              "(verified from records by goal_gate.py; a report of work done is "
              "not the gate)" % (prefix, gate.get("remaining"), gate.get("next")))
    if ent["noprogress"] >= 1:
        reason += (" | %d consecutive block(s) with no tool-backed progress -- "
                   "one more unchanged stop allows a bounded pause for the "
                   "controller/user to rotate the lane" % ent["noprogress"])
    return _emit({"decision": "block", "reason": reason})


if __name__ == "__main__":
    main()
