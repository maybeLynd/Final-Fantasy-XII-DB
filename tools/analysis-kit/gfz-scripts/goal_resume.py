#!/usr/bin/env python3
"""goal_resume.py -- classify a stopped goal lane and resume the SAME session.

Built for the observed failure: the built-in /goal evaluator returned met=true
on lanes whose transcripts still named unfinished research ("three packages;
next RNG contract", "UQ-289 reframed; next nine context-switch variants"). When
that happens the goal is cleared by the false verdict, so resuming must restore
the goal's EXACT condition -- recovered from the session's own goal_status
records, never paraphrased.

This script never guesses a session. It requires an exact --session id, finds
the transcript under ~/.claude/projects/**/, classifies the stop from the
transcript tail, and refuses everything that is not an ordinary false
completion or an ordinary stop with the goal still active:

    FALSE_COMPLETION   last goal_status met=true AND goal_gate says NOT_MET
                       -> resumable; the goal is re-issued verbatim
    ORDINARY_STOP      goal still active (no met/failed record), session dead
                       -> resumable; the stored goal persists on --resume
    COMPLETE           met=true AND the gate agrees -> do nothing
    IMPOSSIBLE         failed=true (evaluator declared impossible) -> report only
    USER_STOP          /goal clear or user-side interrupt near the tail -> honour
    USAGE_LIMIT        rate-limit/usage-limit records in the tail -> wait, report
    ERROR              api_error / unrecoverable records -> report only
    ACTIVE             session still listed by `claude agents --json` -> refuse
    UNKNOWN            anything else -> report only; never retry

Retry storms are bounded by work/goal-gate/resume-state.json: a session whose
transcript did not grow across the last resume is not resumed again (max 3
attempts, then it reports STALLED for a human).

Without --execute it only prints the classification and the exact supported
command it would run. With --execute it spawns:

    claude -p --resume <id> --input-format stream-json --output-format json

feeding `/goal <exact condition>` (goal cleared by the false verdict) or a
plain continue nudge (goal still active). On this install (2.1.278) that form
was verified to resume the same session id and re-register a goal; an
interactive `claude --resume <id>` is the equivalent manual path.
"""
import argparse, glob, json, os, re, subprocess, sys, time

_HERE = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.normpath(os.path.join(_HERE, os.pardir, os.pardir, "work", "goal-gate"))
STATE_PATH = os.path.join(STATE_DIR, "resume-state.json")
GATE = os.path.join(_HERE, "goal_gate.py")
MAX_RESUMES = 3
DB_GOAL_SIG = re.compile(r"(?i)(ffxii|ff12).*(database|reconstruction|knowledge)|(database|reconstruction).*(ffxii|ff12)")


def find_transcript(session_id):
    pat = os.path.expanduser(os.path.join("~", ".claude", "projects", "*",
                                          session_id + ".jsonl"))
    hits = glob.glob(pat)
    return hits[0] if hits else None


def live_sessions():
    try:
        r = subprocess.run(["claude", "agents", "--json"],
                           capture_output=True, text=True, timeout=30)
        return {s.get("sessionId") for s in json.loads(r.stdout)}
    except Exception:
        return None  # unknown -> fail closed, do not resume


def tail_records(path, n=400):
    """Last n records of the transcript (line-oriented jsonl)."""
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            f.seek(-min(size, 2 << 20), os.SEEK_END)
            lines = f.read().decode("utf-8", "replace").splitlines()
    except OSError:
        return []
    out = []
    for l in lines:
        try:
            out.append(json.loads(l))
        except ValueError:
            pass
    return out[-n:]


def classify(recs):
    """-> (state, goal_condition_or_None, evidence_line)."""
    goal = None
    for r in reversed(recs):
        att = (r.get("attachment") or {})
        if r.get("type") == "attachment" and att.get("type") == "goal_status":
            goal = att
            break
    user_clear = False
    hard_limit = False
    api_error = False
    for r in recs:
        if r.get("type") == "user":
            c = r.get("message", {}).get("content")
            s = c if isinstance(c, str) else json.dumps(c)
            if "<command-name>/goal" in s and re.search(
                    r"<command-args>\s*(clear|stop|off|reset|none|cancel)", s):
                user_clear = True
        if r.get("type") == "rate_limit_event":
            st = (r.get("rate_limit_info") or {}).get("status", "")
            if st in ("rate_limited", "rejected", "usage_limit"):
                hard_limit = True
        if r.get("type") == "user" and r.get("usageLimitNote"):
            hard_limit = True
        if r.get("api_error_status") or (r.get("type") == "system" and
                "api_error" in str(r.get("subtype", ""))):
            api_error = True
    if goal is not None and DB_GOAL_SIG.search(str(goal.get("condition") or "")) is None:
        return "NOT_A_DB_GOAL", None, "latest goal is not the database-completion goal"
    if goal and goal.get("met"):
        cond = goal.get("condition")
        try:
            g = subprocess.run([sys.executable, GATE, "--json"], capture_output=True,
                               text=True, timeout=600)
            verdict = json.loads(g.stdout).get("verdict")
            rem = json.loads(g.stdout).get("remaining")
        except Exception:
            verdict, rem = "NOT_MET", "gate unreadable -- fail closed"
        if verdict == "MET":
            return "COMPLETE", None, "gate agrees with met=true"
        return "FALSE_COMPLETION", cond, \
            "evaluator met=true but gate NOT_MET (%s)" % rem
    if goal and goal.get("failed"):
        return "IMPOSSIBLE", None, "evaluator declared the goal impossible"
    if user_clear:
        return "USER_STOP", None, "/goal clear or explicit cancel in tail"
    if hard_limit:
        return "USAGE_LIMIT", None, "rate/usage-limit records in tail"
    if api_error:
        return "ERROR", None, "api_error records in tail"
    if goal is not None:
        return "ORDINARY_STOP", goal.get("condition"), \
            "goal still active, no terminal record"
    return "UNKNOWN", None, "no goal_status records found"


def _state():
    try:
        return json.load(open(STATE_PATH, encoding="utf-8"))
    except Exception:
        return {}


def _save(st):
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = STATE_PATH + ".tmp"
    json.dump(st, open(tmp, "w", encoding="utf-8"))
    os.replace(tmp, STATE_PATH)


def session_cwd(recs, transcript):
    for r in recs:
        att = r.get("attachment") or {}
        if r.get("type") == "attachment" and att.get("type") == "environment":
            wd = (att.get("snapshot") or {}).get("workingDirectory")
            if wd:
                return wd
    return os.path.expanduser("~")


def resume(session_id, condition, transcript, execute, cwd):
    st = _state()
    ent = st.get(session_id, {"attempts": 0, "last_sig": 0})
    sig = os.path.getsize(transcript)
    if ent["attempts"] >= MAX_RESUMES and ent.get("last_sig") == sig:
        return "STALLED", "%d resumes produced no transcript growth" % ent["attempts"]
    if ent["attempts"] >= MAX_RESUMES and ent.get("last_sig") != sig:
        ent["attempts"] = 0  # progress happened; the budget resets
    goal_cleared = condition is not None
    # Restore the goal only if it was cleared (a met record clears it); an
    # active goal survives --resume on its own.
    msg = ("/goal " + condition) if goal_cleared else \
        "Continue. The database goal is still active; resume the highest-priority unfinished obligation."
    cmd = ["claude", "-p", "--resume", session_id,
           "--input-format", "stream-json", "--output-format", "json"]
    wire = json.dumps({"type": "user", "message": {"role": "user",
                                                   "content": msg}})
    if not execute:
        return "PLANNED", " ".join(cmd) + "   <<< " + wire[:160]
    log = os.path.join(STATE_DIR, "resume-%s.log" % session_id)
    os.makedirs(STATE_DIR, exist_ok=True)
    lf = open(log, "ab")
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=lf, stderr=lf,
                         cwd=cwd)
    p.stdin.write(wire.encode() + b"\n")
    p.stdin.close()
    ent["attempts"] += 1
    ent["last_sig"] = sig
    ent["last_at"] = time.time()
    ent["log"] = log
    st[session_id] = ent
    _save(st)
    return "RESUMED", "pid %d, log %s" % (p.pid, log)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", required=True, help="exact session id")
    ap.add_argument("--execute", action="store_true")
    a = ap.parse_args(argv)

    t = find_transcript(a.session)
    if not t:
        print("UNKNOWN: no transcript for session %s" % a.session)
        return 2
    live = live_sessions()
    if live is None:
        print("UNKNOWN: `claude agents --json` unreadable; refusing to risk a duplicate")
        return 2
    if a.session in live:
        print("ACTIVE: session %s is running; never resume an active session" % a.session)
        return 2

    recs = tail_records(t)
    state, cond, why = classify(recs)
    print("%s: %s" % (state, why))
    if state not in ("FALSE_COMPLETION", "ORDINARY_STOP"):
        return 1
    # A cleared goal needs re-issue; an active one does not.
    need_goal = state == "FALSE_COMPLETION"
    cwd = session_cwd(recs, t)
    result, detail = resume(a.session, cond if need_goal else None, t,
                            a.execute, cwd)
    print("%s: %s" % (result, detail))
    return 0 if result in ("RESUMED", "PLANNED") else 1


if __name__ == "__main__":
    sys.exit(main())
