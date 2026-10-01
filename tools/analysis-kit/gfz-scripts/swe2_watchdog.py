#!/usr/bin/env python3
"""swe2_watchdog.py -- dynamic scheduler for the eight fixed SWE2 fleet sessions.

Replaces the original "keep everyone awake" recovery monitor (2026-09-13) with a
capacity-limited controller. It keeps AT MOST ``TARGET_ACTIVE`` fleet workers
turning over, never more than ``HARD_MAX_ACTIVE``, and chooses the set from
SWE2-FRONTIER's plan (``fleet-plan.json``) or, failing that, from the TEAM board.

Host interface (verified end-to-end 2026-09-13, Devin Desktop 1.126.0,
CLI 3000.10.21/3000.10.23):

    devin list --format json          session inventory (id, title, activity)
    devin auth status                 credential gate for the resume path
    devin -r <id> -p "Continue"       resumes a session IN PLACE - same id, same
                                    chain - and holds its lock for the turn.
    session_locks/<id>.lock           exclusively held while ANY process has the
                                    session open. Devin Desktop holds locks on
                                    the workspace's visible sessions, so a
                                    fleet session that is open in the desktop
                                    CANNOT be resumed: session/load fails with
                                    "already open in another process"
                                    (session_locked, retryable). The wake path
                                    only works on a session whose lock is FREE.

Consequences baked into the logic below:
  * "lock held" is NOT "working". It means open somewhere (idle desktop tab or
    a live turn). A held-but-stale session is parked-by-desktop: visible, not
    wakeable. Only a FREE lock is resumable.
  * A live turn is detected by the spawned wake PID staying alive, or by fresh
    last_activity on the session. Held+stale never counts as a worker.
  * A spawned wake writes its stdout/stderr to wakes/<id>-<ts>.log; the tail is
    classified on exit: rate-limit text trips the breaker, "already open in
    another process" means the desktop grabbed it (environmental, not a fault).

Scheduling rules:
  * the automated pool is the seven specialist lanes - every SWE2 identity
    except SWE2-FRONTIER. desired set membership and the TARGET_ACTIVE /
    HARD_MAX_ACTIVE concurrency limit apply ONLY to specialists.
    SWE2-FRONTIER is the control plane: it is never in the desired set and
    never consumes a specialist slot. A manually continued FRONTIER session
    (or an inflight planner wake) runs IN ADDITION TO the specialists - it
    does not evict one and does not count toward capacity.
  * desired set comes from fleet-plan.json when fresh (written by SWE2-FRONTIER
    at its checkpoints); otherwise derived from TEAM.json - ordered by the
    priority of each lane's best work (P0 first), with rank breaking ties:
    active claims first, then targeted ready requests, then unblocked lane
    research. FRONTIER's own need is tracked for status only.
  * event-driven replanning: workers NEVER wake anyone. A worker that hits a
    replan condition writes a durable event with
        swe2_watchdog.py replan --identity SWE2-X --reason REASON --note "..."
    Events aggregate into one pending replan in replan-state.json; after
    REPLAN_DEBOUNCE seconds of quiet the watchdog wakes SWE2-FRONTIER once as
    planner. The planner wake is slot-free - it proceeds even at specialist
    capacity and does not consume one of the three slots. If FRONTIER is
    already working it is not re-woken; it sees the pending replan at its
    next board pass and clears it with `swe2_watchdog.py replan --clear`.
  * auditors (SWE2-AUDIT-SEM / SWE2-AUDIT-SPEC) are desired only while review
    work exists: an ACTIVE audit claim or a READY request routed to them.
  * lanes whose board work is DONE/BLOCKED/empty are parked; a parked lane with
    no claim holds nothing and is simply not woken. Lanes rotate in when their
    queue gains ready work or a slot frees.
  * staggered wakes: at most one wake per poll and at least MIN_WAKE_GAP
    seconds between any two spawns.
  * circuit breaker: a wake process that dies reporting a Windsurf
    overall-message-rate error opens the breaker for the reported reset
    interval plus BREAKER_MARGIN; while open NO new wakes are spawned. After it
    closes, exactly one probe wake runs and must survive PROVE_WINDOW before
    normal staggered scheduling resumes.
  * never-wake list: tree-coaster and universal-coral are never resumed and
    never counted as fleet workers. No session id outside the eight mapped
    identities is ever resumed.
  * fail closed on missing auth, CLI errors, ambiguous activity or a stale
    plan. Never creates sessions; only `devin -r` on ids it already knows.
    Never kills or interrupts a running session.

Files (all under %USERPROFILE%\\.swe2-fleet, outside the shared tree):
    fleet-map.json        identity -> canonical/current session ids
    fleet-plan.json       FRONTIER's desired-set decision (optional override)
    replan-state.json     pending aggregated replan request + reasons
    watchdog-state.json   counters, inflight wakes, breaker, queued workers
    watchdog-log.jsonl    every observation and decision (concurrency telemetry)
    wakes\\*.log          stdout/stderr of each spawned wake

Usage:
    python swe2_watchdog.py --once               one poll, send wakes if due
    python swe2_watchdog.py --loop               poll forever (default 120s)
    python swe2_watchdog.py --status             report only, never send
    python swe2_watchdog.py --once --dry-run     full decision pass, no spawns
    python swe2_watchdog.py replan --identity SWE2-EC7 --reason ROLE_QUEUE_DRAINED
    python swe2_watchdog.py replan --clear       planner processed the replan
    python swe2_watchdog.py wake --identity SWE2-DATA
                                                 one manual bounded wake through
                                                 the normal eligibility gates
"""

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
import kit_paths as KP  # noqa: E402

# pythonw (the logon-startup interpreter) has no console: sys.stdout and
# sys.stderr are None there and every print() would crash the unattended
# run. Redirect both to devnull so headless launches stay silent.
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

# --------------------------------------------------------------------------
# Hidden child processes (Windows)
#
# The controller runs detached with no console of its own, so every
# console-subsystem child it spawns WITHOUT the no-window flag gets a fresh
# VISIBLE console window. That was the periodic burst of ~8-14 CMD flashes
# reported 2026-09-15: per poll the old code windowed `devin list`,
# `devin auth status`, N x tasklist, N x powershell and the odd taskkill.
# Every automated launch below goes through run_hidden()/popen_hidden();
# no call site builds raw subprocess flags, so a future command cannot
# reintroduce a console flash. Every command names its executable directly
# (devin.exe, tasklist, powershell, taskkill, schtasks, reg, python) - no
# command-shell wrappers, no fresh consoles.


def _hidden_kwargs(detached=False):
    """Popen/run kwargs that guarantee no visible console on Windows.

    The no-window creation flag prevents console allocation; a hidden
    STARTUPINFO is belt-and-braces for a child that tries to create a
    window anyway. stdin is DEVNULL so an unattended child can never block
    on input; stdout/stderr stay caller-controlled (captured for telemetry
    or redirected into wake/controller log files). detached=True adds the
    detached-process/new-process-group flags for the survivor controller
    child only."""
    kw = {"stdin": subprocess.DEVNULL}
    if os.name == "nt":
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        if detached:
            flags |= (getattr(subprocess, "DETACHED_PROCESS", 0)
                      | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0))
        kw["creationflags"] = flags
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0  # SW_HIDE
        kw["startupinfo"] = si
    return kw


def run_hidden(cmd, **kw):
    """subprocess.run() that cannot open, focus or flash a console."""
    merged = _hidden_kwargs()
    merged.update(kw)
    return subprocess.run(cmd, **merged)


def popen_hidden(cmd, detached=False, **kw):
    """subprocess.Popen() that cannot open, focus or flash a console."""
    merged = _hidden_kwargs(detached=detached)
    merged.update(kw)
    return subprocess.Popen(cmd, **merged)


# --------------------------------------------------------------------------
# Host interface and paths

DEVIN_CANDIDATES = [
    os.environ.get("DEVIN_CLI", ""),
    r"E:\Devin\resources\app\extensions\windsurf\devin\bin\devin.exe",
    "devin",  # PATH (WinGet install)
]
WORKDIR = KP.ROOT
LOCK_DIR = os.path.expandvars(r"%APPDATA%\devin\cli\session_locks")
STATE_DIR = os.path.expandvars(r"%USERPROFILE%\.swe2-fleet")
STATE_FILE = os.path.join(STATE_DIR, "watchdog-state.json")
MAP_FILE = os.path.join(STATE_DIR, "fleet-map.json")
PLAN_FILE = os.path.join(STATE_DIR, "fleet-plan.json")
LOG_FILE = os.path.join(STATE_DIR, "watchdog-log.jsonl")
REPLAN_DIR = os.path.join(STATE_DIR, "replan-events")
CONSUMED_DIR = os.path.join(REPLAN_DIR, "consumed")
QUAR_DIR = os.path.join(REPLAN_DIR, "quarantine")
PID_FILE = os.path.join(STATE_DIR, "controller.pid")
CTRL_LOG = os.path.join(STATE_DIR, "controller.log")
WAKE_LOG_DIR = os.path.join(STATE_DIR, "wakes")

BOARD_FILE = os.path.join(
    WORKDIR, "Database", "FFXII TZA", "_index", "_inbox", "TEAM.json")

# identity -> canonical session id (the eight stable ids from `devin list`).
FLEET_TITLES = {
    "SWE2-FRONTIER": "crystal-thread",
    "SWE2-EC7": "zesty-condition",
    "SWE2-CONTRACT": "right-ocean",
    "SWE2-STRUCT": "fish-jupiter",
    "SWE2-DATA": "holy-rock",
    "SWE2-ORACLE": "tulip-krypton",
    "SWE2-AUDIT-SEM": "legend-pipe",
    "SWE2-AUDIT-SPEC": "sapphire-porkpie",
}
AUDITORS = {"SWE2-AUDIT-SEM", "SWE2-AUDIT-SPEC"}
# The automated worker pool is the seven specialist lanes. SWE2-FRONTIER is
# the control plane - it is woken only as the replan planner (or manually by
# the user) and never occupies one of the TARGET_ACTIVE specialist slots.
PLANNER = "SWE2-FRONTIER"
SPECIALISTS = [i for i in FLEET_TITLES if i != PLANNER]
NEVER_WAKE_SESSIONS = {"tree-coaster", "universal-coral",
                       "atom-dianella", "heathered-cheshire"}
NEVER_WAKE_TITLES = {
    "Comprehensive Audit: XIIOnline, Hub, EnetServer", "FFXIIOnline"}

# --------------------------------------------------------------------------
# Tunables

TARGET_ACTIVE = 3           # desired simultaneous workers (plan may lower it)
HARD_MAX_ACTIVE = 3         # absolute ceiling, plan cannot raise it
POLL_INTERVAL = 120         # --loop default
BUSY_WINDOW = 600           # last_activity fresher than this = a live turn
MIN_WAKE_GAP = 120          # stagger: minimum seconds between any two wakes
DEBOUNCE_SECONDS = 900      # at most one wake per identity per 15 min
MAX_WAKES_PER_DAY = 16      # per identity hard cap
MAX_CONSECUTIVE_FAILURES = 3
WAKE_TIMEOUT = 7200         # long turns are legal; only logged past this
PLAN_TTL = 6 * 3600         # a plan older than this is stale -> board heuristic
BREAKER_MARGIN = 25         # safety margin over the reported reset interval
BREAKER_DEFAULT = 900       # used when the error reports no reset interval
PROVE_WINDOW = 180          # post-breaker probe must stay alive this long
STARVATION_ELIGIBLE_WARN = 3 * 3600  # eligible-but-unselected this long
STARVATION_USEFUL_WARN = 6 * 3600    # with no attributable TEAM op this long
NO_ENGAGE_SECONDS = 180     # wake exit under this with no TEAM op = no-engage
INEFFECTIVE_STREAK_PARK = 3 # consecutive nonproductive wakes parks a lane
REPLAN_DEBOUNCE = 90        # quiet window before the aggregated replan wakes
                            # the planner once
PLANNER_DEBOUNCE = 180      # planner wakes get a tighter per-lane debounce than
                            # the 15-min worker default - a legitimate replan
                            # must not wait 15 min behind an unrelated FRONTIER
                            # wake. Daily cap, stagger and breaker still apply.
WAKE_PROMPT = "Continue"
# Noninteractive `devin -r` wakes run in -p mode where a permission prompt
# is an automatic rejection ("rejected a tool call ... non-interactive
# mode"). CLI 3000.10.x documents --permission-mode: "smart" auto-approves
# workspace edits and auto-runs actions a fast model judges safe, while
# installs, mutating git ops, rm/sudo and destructive cloud commands STILL
# prompt (and therefore still fail closed in -p). Changed to "dangerous"
# 2026-09-16: the smart carve-outs turned out to cover the fleet's entire
# output channel - team.py board ops and publish_paths.sh/git commit were
# the denied calls - so every woken lane did analysis-only work the
# attribution instrument cannot see, then streaked to a day-park
# (OPUS-NOTICE-FRONTIER-INEFFECTIVE-WAKES-STALL-SEVEN-OPUS-REQUESTS).
# "dangerous" auto-approves all tools; these are dedicated single-repo
# worker sessions and unattended board ops are the design intent.
WAKE_PERMISSION_MODE = "dangerous"

REPLAN_REASONS = {
    "NO_LOCAL_WORK",
    "BLOCKED_NEEDS_SPECIALIST",
    "REVIEW_QUEUE_READY",
    "HIGH_PRIORITY_REQUEST_RECEIVED",
    "ROLE_QUEUE_DRAINED",
    "ERROR_OR_COORDINATION_CONFLICT",
}

RATE_PAT = re.compile(
    r"overall message rate|message rate limit|rate.?limit(?:ed)?|rate_limit|"
    r"too many requests|\b429\b|quota exceeded|usage limit|throttl",
    re.IGNORECASE)
LOCKED_PAT = re.compile(
    r"already open in another process|session_locked|session is locked",
    re.IGNORECASE)
NOSESSION_PAT = re.compile(r"no session found matching", re.IGNORECASE)
DENIED_PAT = re.compile(
    r"rejected a tool call|requires confirmation|non-interactive mode|"
    r"permission-mode", re.IGNORECASE)
RESET_PATTERNS = [
    re.compile(r"retry[- ]?after[:\s]+(\d+)\s*(s|sec|m|min|h|hr|hour)?",
               re.IGNORECASE),
    re.compile(r"(?:try again|resets?|reset|available|wait|back)\s+(?:after|in|at)?"
               r"\s*[:~]?\s*(\d+)\s*(seconds?|secs?|s|minutes?|mins?|m|hours?|hrs?|h)\b",
               re.IGNORECASE),
    re.compile(r"\b(\d+)\s*(seconds?|minutes?|hours?)\b\s*(?:until|to|before)\s+"
               r"(?:reset|retry|next)", re.IGNORECASE),
]
UNIT_SECONDS = {"s": 1, "sec": 1, "seconds": 1, "second": 1, "secs": 1,
                "m": 60, "min": 60, "mins": 60, "minute": 60, "minutes": 60,
                "h": 3600, "hr": 3600, "hrs": 3600, "hour": 3600, "hours": 3600}


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def log(event):
    os.makedirs(STATE_DIR, exist_ok=True)
    event["ts"] = now_iso()
    line = json.dumps(event, default=str)
    with open(LOG_FILE, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line, flush=True)


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return default


def save_json(path, obj):
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1)
    os.replace(tmp, path)


def load_state():
    st = load_json(STATE_FILE, {})
    st.setdefault("wakes", {})        # identity -> {date: {count,last}}
    st.setdefault("failures", {})     # identity -> consecutive failed wakes
    st.setdefault("inflight", {})     # identity -> {pid,session,spawned_at,log}
    st.setdefault("breaker", {"open_until": 0, "reason": "",
                              "opened_at": 0, "recovering": False})
    st.setdefault("last_wake_at", 0)
    st.setdefault("queued", {})       # ident -> reason it wants a slot
    st.setdefault("replan", {})       # {"planner_wake_sent_at": ts}
    st.setdefault("starvation", {})   # ident -> eligible_since/last_useful_at
    st.setdefault("wake_quality", {}) # ident -> productive/nonproductive/streak
    st.setdefault("parked_ineffective", {})  # ident -> date parked for
    return st


# --------------------------------------------------------------------------
# Replan events (workers write; the watchdog is the only component that wakes)
#
# Append-only design: each event is ONE file in replan-events/, written
# atomically (tmp + os.replace). Concurrent workers can never overwrite each
# other, and an event that lands while the planner consumes the batch survives
# - clear only moves the files it listed. Malformed files stay pending and are
# quarantined on clear; fail closed, never silently drop.

def _event_files():
    try:
        names = sorted(os.listdir(REPLAN_DIR))
    except OSError:
        return []
    return [os.path.join(REPLAN_DIR, n) for n in names if n.endswith(".json")]


def replan_events():
    """(parsed events, malformed paths) - everything currently pending."""
    evs, bad = [], []
    for path in _event_files():
        try:
            with open(path, encoding="utf-8") as fh:
                ev = json.load(fh)
            ev["_file"] = path
            evs.append(ev)
        except (OSError, json.JSONDecodeError):
            bad.append(path)
    return evs, bad


def append_replan(identity, reason, note, test=False):
    """Worker-side API: file one durable event. Never wakes anyone."""
    os.makedirs(REPLAN_DIR, exist_ok=True)
    now = time.time()
    ev = {"identity": identity, "reason": reason, "note": note,
          "test": bool(test), "ts": now_iso(), "epoch": now}
    name = "%d-%s-%d.json" % (int(now * 1e6), identity, os.getpid())
    tmp = os.path.join(REPLAN_DIR, "." + name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(ev, fh)
    os.replace(tmp, os.path.join(REPLAN_DIR, name))
    log({"event": "replan_requested", "identity": identity, "reason": reason,
         "note": note, "test": bool(test), "file": name})
    return ev


def replan_view(state):
    """Aggregated pending view used by the poll loop."""
    evs, bad = replan_events()
    epochs = [e.get("epoch", 0) for e in evs]
    for p in bad:
        try:
            epochs.append(os.path.getmtime(p))
        except OSError:
            epochs.append(time.time())
    return {"pending": bool(evs or bad),
            "opened_at": min(epochs) if epochs else 0,
            "updated_at": max(epochs) if epochs else 0,
            "events": evs, "malformed": bad,
            "planner_wake_sent_at":
                state.get("replan", {}).get("planner_wake_sent_at", 0)}


def clear_replan():
    """Planner-only consumption. Moves listed events to consumed/, malformed
    files to quarantine/. An event arriving mid-clear was never listed and
    stays pending."""
    os.makedirs(CONSUMED_DIR, exist_ok=True)
    os.makedirs(QUAR_DIR, exist_ok=True)
    n = q = 0
    for path in _event_files():
        try:
            json.load(open(path, encoding="utf-8"))
            dst = os.path.join(CONSUMED_DIR, os.path.basename(path))
            n += 1
        except (OSError, json.JSONDecodeError):
            dst = os.path.join(QUAR_DIR, os.path.basename(path))
            q += 1
        try:
            os.replace(path, dst)
        except OSError:
            pass
    log({"event": "replan_cleared", "events_consumed": n, "quarantined": q})
    return n


def replan_due(rp, now):
    """Pending replan quiet for REPLAN_DEBOUNCE that has not already been
    handed to the planner (or gained new events since)."""
    if not rp["pending"]:
        return False
    if now - rp["updated_at"] < REPLAN_DEBOUNCE:
        return False
    sent = rp.get("planner_wake_sent_at", 0)
    return sent == 0 or rp["updated_at"] > sent


# --------------------------------------------------------------------------
# devin CLI

_DEVIN = None


def devin_bin():
    global _DEVIN
    if _DEVIN:
        return _DEVIN
    for cand in DEVIN_CANDIDATES:
        if not cand:
            continue
        try:
            proc = run_hidden([cand, "version"], capture_output=True,
                              text=True, timeout=15)
            if proc.returncode == 0:
                _DEVIN = cand
                return cand
        except (OSError, subprocess.TimeoutExpired):
            continue
    return None


def run_cli(args, timeout=30):
    exe = devin_bin()
    if not exe:
        return -1, "no devin binary"
    try:
        proc = run_hidden([exe] + args, cwd=WORKDIR, capture_output=True,
                          text=True, timeout=timeout)
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except (OSError, subprocess.TimeoutExpired) as exc:
        return -1, str(exc)


def list_sessions():
    """{session_id: {title, last_activity_at}} or None on failure."""
    rc, out = run_cli(["list", "--format", "json"])
    if rc != 0:
        return None
    try:
        return {s["id"]: s for s in json.loads(out) if "id" in s}
    except json.JSONDecodeError:
        return None


def auth_ok():
    rc, out = run_cli(["auth", "status"])
    return rc == 0 and "not logged in" not in out.lower()


def lock_held(session_id):
    """True while any process holds the session (live turn OR open desktop tab)."""
    path = os.path.join(LOCK_DIR, session_id + ".lock")
    try:
        with open(path, "rb") as fh:
            fh.read()
        return False
    except PermissionError:
        return True
    except OSError:
        return False


def pid_alive(pid, spawned_at=None):
    if not pid:
        return False
    out = run_hidden(
        ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
        capture_output=True, text=True).stdout
    if f"{pid}," not in out and f'"{pid}"' not in out:
        return False
    if spawned_at:
        # Guard against PID reuse: the process must have started near spawn time.
        try:
            q = run_hidden(
                ["powershell", "-NoProfile", "-Command",
                 f"(Get-Process -Id {pid} -ErrorAction Stop).StartTime."
                 "ToUniversalTime().ToString('o')"],
                capture_output=True, text=True, timeout=15).stdout.strip()
            start = datetime.fromisoformat(q.replace("Z", "+00:00")).timestamp()
            if abs(start - spawned_at) > 300:
                return False
        except Exception:
            pass  # if we cannot verify, the live PID is still our best signal
    return True


# --------------------------------------------------------------------------
# Fleet map: identity <-> sessions

def load_map():
    m = load_json(MAP_FILE, {})
    m.setdefault("identities", {})
    for ident, canon in FLEET_TITLES.items():
        rec = m["identities"].setdefault(ident, {})
        rec.setdefault("canonical", canon)
        rec.setdefault("current", canon)
    m.setdefault("never_wake_sessions", sorted(NEVER_WAKE_SESSIONS))
    m.setdefault("never_wake_titles", sorted(NEVER_WAKE_TITLES))
    return m


def reconcile_map(fleet_map, sessions):
    """Refresh canonical ids if a fleet title moved (fleet relaunched)."""
    by_title = {}
    for sid, s in sessions.items():
        by_title.setdefault((s.get("title") or "").strip(), []).append(sid)
    for ident in FLEET_TITLES:
        rec = fleet_map["identities"][ident]
        ids = [sid for sid in by_title.get(ident, [])
               if sid not in NEVER_WAKE_SESSIONS]
        if ids and rec["canonical"] not in ids:
            log({"event": "canonical_moved", "identity": ident,
                 "was": rec["canonical"], "now": ids})
            rec["canonical"] = ids[0]
            if rec.get("current") == rec.get("canonical"):
                rec["current"] = ids[0]


def identity_sessions(fleet_map, ident):
    """All session ids currently attributable to this lane."""
    rec = fleet_map["identities"][ident]
    out = [rec["canonical"]]
    if rec.get("current") and rec["current"] not in out:
        out.append(rec["current"])
    return out


def last_activity(sessions, sid):
    s = sessions.get(sid)
    return (s.get("last_activity_at") or 0) if s else 0


def identity_state(fleet_map, state, sessions, ident, now):
    """(state, detail): busy-* / held-idle / free."""
    w = state["inflight"].get(ident)
    if w and pid_alive(w.get("pid"), w.get("spawned_at")):
        return "busy-wake", "pid:%s" % w.get("pid")
    fresh = [sid for sid in identity_sessions(fleet_map, ident)
             if now - last_activity(sessions, sid) < BUSY_WINDOW]
    if fresh:
        return "busy-active", "fresh:%s" % fresh[0]
    held = [sid for sid in identity_sessions(fleet_map, ident)
            if lock_held(sid)]
    if held:
        return "held-idle", "open:%s" % held[0]
    return "free", "-"


def foreign_active(sessions, fleet_map, now):
    """Non-fleet sessions showing fresh activity; they consume rate budget."""
    fleet_sids = set()
    for ident in fleet_map["identities"]:
        fleet_sids.update(identity_sessions(fleet_map, ident))
    out = []
    for sid, s in sessions.items():
        if sid in fleet_sids or sid in NEVER_WAKE_SESSIONS:
            continue
        if (s.get("title") or "").strip() in NEVER_WAKE_TITLES:
            continue
        if now - last_activity(sessions, sid) < BUSY_WINDOW:
            out.append(sid)
    return out


# --------------------------------------------------------------------------
# Board-derived need

def board_integrity():
    """(ok, detail) for the live board's durability journal.

    The 2026-09-25 rollback showed a stale writer can overwrite TEAM.json
    without any op failing at the time; the journal makes the next touch
    detect it. While the board is in incident state the controller must not
    dispatch: a lane woken onto a rolled-back board would build more fork
    work, and an incident must never masquerade as an empty healthy frontier.
    """
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import team
        return team.board_status(BOARD_FILE)
    except Exception as exc:
        return False, "board integrity check failed to run: %s" % exc


def board_need():
    """Per-lane scheduling need from TEAM.json. Returns
    {ident: (rank, priority, reason)}.

    Ordering: desired lanes are chosen by best work priority first (P0 wins),
    then rank as the tiebreaker. Rank: 0 = ACTIVE claim held, 1 = targeted
    READY request, 2 = lane/unassigned READY research (production lanes only;
    auditors never get lane research and FRONTIER never does - they wake only
    for routed work / planner duty).
    """
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import team
        board = json.loads(open(BOARD_FILE, encoding="utf-8").read())
        tasks = board["tasks"]
        ready = team.ready(board, None)
    except Exception as exc:
        return {"__error__": str(exc)}

    need = {}
    for ident in FLEET_TITLES:
        active = [t for t in tasks if t["status"] == "ACTIVE"
                  and (t.get("agent") == ident or t.get("assigned_to") == ident)]
        if active:
            need[ident] = (0, min(t["priority"] for t in active),
                           "active-claim:" + ",".join(t["id"] for t in active))
            continue
        mine_ready = [t for t in ready
                      if t.get("assigned_to") == ident
                      or t["id"].startswith(ident + "-")]
        if mine_ready:
            best = min(t["priority"] for t in mine_ready)
            need[ident] = (1, best, "ready-targeted:%s:%s"
                           % (best, ",".join(t["id"] for t in mine_ready[:4])))
            continue
        if ident in AUDITORS or ident == PLANNER:
            continue
        pool = [t for t in ready if t.get("kind") == "research"
                and not t.get("assigned_to")
                and not any(t["id"].startswith(p + "-") for p in FLEET_TITLES)]
        if pool:
            best = min(t["priority"] for t in pool)
            need[ident] = (2, best, "ready-pool:%s:%d" % (best, len(pool)))
    return need


def useful_ops():
    """ident -> epoch of its most recent TEAM.json history op.

    'Useful' here is deliberately narrow and measurable: a board operation
    attributable to the lane. Analysis-only work is invisible to it - the
    starvation warning therefore also requires the lane to have been
    eligible-but-unselected for a while before it speaks.
    """
    try:
        board = json.loads(open(BOARD_FILE, encoding="utf-8").read())
    except Exception:
        return {}
    out = {}
    for e in board.get("history", []):
        a = e.get("agent")
        if a not in FLEET_TITLES:
            continue
        try:
            t = datetime.fromisoformat(
                e.get("at", "").replace("Z", "+00:00")).timestamp()
        except Exception:
            continue
        if t > out.get(a, 0):
            out[a] = t
    return out


def useful_op_since(ident, epoch):
    """True if TEAM.json history attributes an op to ident after `epoch`."""
    try:
        board = json.loads(open(BOARD_FILE, encoding="utf-8").read())
    except Exception:
        return False
    for e in reversed(board.get("history", [])):
        try:
            t = datetime.fromisoformat(
                e.get("at", "").replace("Z", "+00:00")).timestamp()
        except Exception:
            continue
        if t <= epoch:
            break
        if e.get("agent") == ident:
            return True
    return False


def load_plan():
    plan = load_json(PLAN_FILE, None)
    if not plan:
        return None
    try:
        stamp = datetime.fromisoformat(
            plan["updated_at"].replace("Z", "+00:00")).timestamp()
        if time.time() - stamp > PLAN_TTL:
            return {"__stale__": plan.get("updated_at")}
    except Exception:
        return {"__invalid__": True}
    return plan


def _prio_num(prio):
    """'P0'..'P9' -> 0..9; anything else sorts last."""
    if isinstance(prio, str) and prio[:1] == "P" and prio[1:].isdigit():
        return int(prio[1:])
    return 9


def dep_blocked_owners(board):
    """{lane: [dep_task_ids]} - lanes that own an unfinished dependency of a
    BLOCKED task.

    A lane paused on another lane's work must never be woken; the DEPENDENCY
    owner is the scheduling target. This is the mechanic behind 'worker
    legitimately paused on dependencies' vs 'project stalled': the blocked
    side produces no need entry at all (a BLOCKED task is not READY and not
    ACTIVE), while the dep owner is promoted into the desired set below.
    Non-SWE2 owners (OPUS/FABLE/ASTRA) are reported for visibility but are
    never a wake target - the controller cannot spawn them.
    """
    by_id = {t["id"]: t for t in board.get("tasks", [])}
    done = {t["id"] for t in board.get("tasks", [])
            if t.get("status") == "DONE"}
    out = {}
    for t in board.get("tasks", []):
        if t.get("status") != "BLOCKED":
            continue
        for dep in t.get("dependencies") or []:
            d = by_id.get(dep)
            if not d or dep in done:
                continue
            owner = d.get("agent") or d.get("assigned_to")
            if owner:
                out.setdefault(owner, set()).add(dep)
    return out


def desired_set(plan, need, dep=None):
    """Return (desired_list, target_active, source).

    The desired set contains only specialists. SWE2-FRONTIER is the control
    plane: it is never a member, never consumes one of the slots, and its
    only automatic wake is the replan planner path in poll().

    `dep` (from dep_blocked_owners) promotes lanes that own an unfinished
    dependency of someone's BLOCKED work ahead of the plan's choices - the
    blocking chain outranks a manually pinned rotation, and a stale plan can
    no longer starve the one lane holding everyone else's gate. Dep owners
    with no schedulable board work (nothing ACTIVE/READY for them) still do
    not enter `need`, so they are never selected by name alone.
    """
    # HELD BY A SUBAGENT (2026-09-30, FABLE for SWE2-FRONTIER, OPUS-REQ-FRONTIER-FLEET-LANE-DOUBLE-WAKE-0930): an identity
    # a Claude session is running through a subagent must never be woken as a second writer under the same name - that
    # produced dc6c5f065 / 280006c24 / b47a560bd (SWE2-DATA) and five orphaned claims (SWE2-CONTRACT). The plan lists
    # such identities in "held_by_subagent"; they are dropped here even when they own a blocking dependency.
    held = set((plan or {}).get("held_by_subagent", []) or [])
    dep_first = [i for i in (dep or {}) if i in SPECIALISTS and i not in held]
    if plan and "desired" in plan:
        target = min(int(plan.get("target_active", TARGET_ACTIVE)),
                     HARD_MAX_ACTIVE)
        pinned = [i for i in plan["desired"] if i in SPECIALISTS and i not in held]
        desired = dep_first + [i for i in pinned if i not in dep_first]
        return desired[:max(target, len(dep_first))], target, \
            "plan+deps" if dep_first else "plan"
    # Board heuristic: best work priority first (P0 wins), rank breaks ties
    # (active claim > targeted ready > lane research), name last. FRONTIER is
    # excluded outright - a manually active FRONTIER runs beside the three
    # specialists, not instead of one.
    target = TARGET_ACTIVE
    ranked = sorted(((k, v) for k, v in need.items() if k in SPECIALISTS),
                    key=lambda kv: (_prio_num(kv[1][1]), kv[1][0], kv[0]))
    desired = [ident for ident, _ in ranked][:target]
    return desired[:HARD_MAX_ACTIVE], target, "board"


# --------------------------------------------------------------------------
# Circuit breaker and wake reaping

def parse_reset_seconds(text):
    for pat in RESET_PATTERNS:
        m = pat.search(text)
        if m:
            mult = UNIT_SECONDS.get((m.group(2) or "s").lower(), 1)
            return max(30, int(m.group(1)) * mult)
    return None


def lane_fresh(fleet_map, sessions, ident):
    """True when the lane's own session(s) show activity inside BUSY_WINDOW -
    meaning a fast wake exit is a no-op nudge to a session already mid-turn,
    not a failed engagement. Denied-tool exits stay chargeable either way."""
    if not fleet_map:
        return False
    now = time.time()
    return any(now - last_activity(sessions, sid) < BUSY_WINDOW
               for sid in identity_sessions(fleet_map, ident))


def reap_inflight(state, sessions, fleet_map=None):
    """Check finished wake processes; classify the exit; maybe trip breaker."""
    for ident, w in list(state["inflight"].items()):
        pid = w.get("pid")
        if pid_alive(pid, w.get("spawned_at")):
            # A recovery probe that stays healthy past PROVE_WINDOW closes
            # recovery; normal staggered scheduling resumes alongside it.
            if w.get("recovery_probe") and state["breaker"].get("recovering") \
                    and time.time() - w.get("spawned_at", 0) > PROVE_WINDOW:
                state["breaker"]["recovering"] = False
                log({"event": "recovery_probe_proved", "identity": ident,
                     "pid": pid})
            if time.time() - w.get("spawned_at", 0) > WAKE_TIMEOUT \
                    and not w.get("warned_long"):
                w["warned_long"] = True
                log({"event": "wake_long_running", "identity": ident,
                     "pid": pid})
            continue
        tail = ""
        try:
            with open(w["log"], "rb") as fh:
                fh.seek(0, 2)
                size = fh.tell()
                fh.seek(max(0, size - 16384))
                tail = fh.read().decode("utf-8", "replace")
        except OSError:
            pass
        ev = {"event": "wake_exited", "identity": ident, "pid": pid,
              "session": w.get("session"),
              "ran_seconds": int(time.time() - w.get("spawned_at", 0))}
        m = RATE_PAT.search(tail)
        if m:
            reset = parse_reset_seconds(tail) or BREAKER_DEFAULT
            until = time.time() + reset + BREAKER_MARGIN
            state["breaker"] = {"open_until": until, "opened_at": time.time(),
                                "reason": tail[m.start():m.start() + 200],
                                "recovering": True}
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            ev.update(breaker="OPEN", reset_seconds=reset,
                      rate_limited=True,
                      inflight=sorted(state["inflight"]),
                      wakes_today=sum(d.get(today, {}).get("count", 0)
                                      for d in state["wakes"].values()))
        elif LOCKED_PAT.search(tail) or lock_held(w.get("session") or ""):
            # Desktop/another process holds the session: environmental, not a
            # lane fault and not a rate event.
            ev["exit_class"] = "session-held"
        elif NOSESSION_PAT.search(tail):
            ev["exit_class"] = "session-gone"
            state["failures"][ident] = state["failures"].get(ident, 0) + 1
        elif ev["ran_seconds"] < 120 and re.search(r"\berror\b|\bfailed\b",
                                                 tail, re.IGNORECASE):
            # Died fast on a generic error (e.g. ACP startup): a lane fault.
            ev["exit_class"] = "error"
            state["failures"][ident] = state["failures"].get(ident, 0) + 1
        elif w.get("recovery_probe"):
            state["breaker"]["recovering"] = False
            ev["exit_class"] = "clean"
            ev["breaker"] = "recovery-complete"
        else:
            ev["exit_class"] = "clean"
        if not m and ev.get("exit_class") != "session-held":
            # Wake-cap quality: a wake whose turn died on tool-denial (the
            # non-interactive approval wall) or that exited fast with no
            # attributable TEAM op produced nothing but consumed a daily
            # wake. Refund it and track the streak; three consecutive
            # nonproductive wakes parks the lane for the day and files a
            # replan event so the planner sees it. Ambiguous exits (ran a
            # while, no denial, no board op) keep the charge and leave the
            # streak untouched.
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            denied = bool(DENIED_PAT.search(tail))
            if useful_op_since(ident, w.get("spawned_at", 0)):
                wq = state["wake_quality"].setdefault(
                    ident, {"productive": 0, "nonproductive": 0, "streak": 0})
                wq["productive"] += 1
                wq["streak"] = 0
                state["parked_ineffective"].pop(ident, None)
            elif denied or (ev["ran_seconds"] < NO_ENGAGE_SECONDS
                            and not lane_fresh(fleet_map, sessions, ident)):
                wq = state["wake_quality"].setdefault(
                    ident, {"productive": 0, "nonproductive": 0, "streak": 0})
                wq["nonproductive"] += 1
                wq["streak"] += 1
                day = state["wakes"].setdefault(ident, {}).setdefault(
                    today, {"count": 0, "last": 0})
                if day["count"]:
                    day["count"] -= 1   # refund the consumed daily wake
                ev["nonproductive"] = True
                if denied:
                    ev["denied_tool"] = True
                if wq["streak"] >= INEFFECTIVE_STREAK_PARK \
                        and state["parked_ineffective"].get(ident) != today:
                    state["parked_ineffective"][ident] = today
                    append_replan(
                        ident, "ERROR_OR_COORDINATION_CONFLICT",
                        "%d consecutive nonproductive wakes (%s) - lane "
                        "parked for the day; fix its approval/env or "
                        "re-point its queue"
                        % (wq["streak"],
                           "tool-denial" if denied else "no-engage"))
                    ev["parked_ineffective"] = True
        log(ev)
        del state["inflight"][ident]


def starvation_pass(state, istate, need, desired, skipped, woken, now):
    """Measure starvation per specialist without reordering selection.

    Tracks, per lane, the time it has been continuously eligible-but-
    unselected (has need, idle, not the lane just woken) and the age of its
    last attributable TEAM op. A lane deferred by genuine higher-priority
    work simply accrues the gap - reporting only. When both the eligibility
    gap and the no-useful-op gap exceed their warn windows, log the metrics
    and file one replan event per episode (reset when the lane runs or
    records an op)."""
    starv = state["starvation"]
    useful = useful_ops()
    warned = []
    for ident in SPECIALISTS:
        rec = starv.setdefault(ident, {})
        rec.setdefault("first_seen", now)
        if useful.get(ident, 0) > rec.get("last_useful_at", 0):
            rec["last_useful_at"] = useful[ident]
            rec.pop("warned", None)
        has_need = ident in need
        idle = istate[ident][0] == "free"
        if has_need and idle and ident != woken:
            rec.setdefault("eligible_since", now)
            rec["defer"] = skipped.get(ident) or (
                "desired-but-unwoken" if ident in desired
                else "behind:" + ",".join(desired) if desired
                else "not-desired")
        else:
            rec.pop("eligible_since", None)
            rec.pop("defer", None)
            rec.pop("warned", None)
            continue
        elig_gap = now - rec["eligible_since"]
        useful_gap = now - (rec.get("last_useful_at") or rec["first_seen"])
        if elig_gap >= STARVATION_ELIGIBLE_WARN \
                and useful_gap >= STARVATION_USEFUL_WARN \
                and not rec.get("warned"):
            rec["warned"] = now
            note = ("idle-eligible %.1fh, no attributable TEAM op in %.1fh "
                    "(defer: %s)"
                    % (elig_gap / 3600, useful_gap / 3600, rec["defer"]))
            log({"event": "starvation_warn", "identity": ident,
                 "eligible_gap_s": int(elig_gap),
                 "useful_gap_s": int(useful_gap),
                 "defer": rec["defer"]})
            append_replan(ident, "BLOCKED_NEEDS_SPECIALIST", note)
            warned.append(ident)
    return warned


def breaker_open(state):
    return time.time() < state["breaker"].get("open_until", 0)


# --------------------------------------------------------------------------
# Wake

def wake_target(fleet_map, sessions, ident):
    """The session id to resume: `current` if it still exists, else canonical."""
    rec = fleet_map["identities"][ident]
    cur = rec.get("current")
    if cur and cur in sessions and cur not in NEVER_WAKE_SESSIONS:
        return cur
    if rec["canonical"] in sessions \
            and rec["canonical"] not in NEVER_WAKE_SESSIONS:
        return rec["canonical"]
    return None


def eligible(state, fleet_map, sessions, ident, now, today, planner=False):
    """(ok, reason) - per-identity wake gates. planner=True swaps the 15-min
    worker debounce for PLANNER_DEBOUNCE so a legitimate replan cannot be
    starved behind an unrelated recent FRONTIER wake; the daily cap, stagger
    gap and breaker still apply."""
    sid = wake_target(fleet_map, sessions, ident)
    if sid is None:
        return False, "no-session"
    if lock_held(sid):
        return False, "session-held"
    wakes = state["wakes"].setdefault(ident, {})
    if today not in wakes:
        wakes.clear()
        wakes[today] = {"count": 0, "last": 0}
    day = wakes[today]
    if state["failures"].get(ident, 0) >= MAX_CONSECUTIVE_FAILURES:
        return False, "consecutive-failures"
    if state["parked_ineffective"].get(ident) == today:
        return False, "ineffective-wakes"
    if day["count"] >= MAX_WAKES_PER_DAY:
        return False, "daily-cap"
    debounce = PLANNER_DEBOUNCE if planner else DEBOUNCE_SECONDS
    if now - day["last"] < debounce:
        return False, "debounce"
    if now - state.get("last_wake_at", 0) < MIN_WAKE_GAP:
        return False, "stagger-gap"
    return True, "ok"


def spawn_wake(state, fleet_map, sessions, ident, now, today, dry_run):
    sid = wake_target(fleet_map, sessions, ident)
    day = state["wakes"][ident][today]
    if dry_run:
        return {"action": "would_wake", "identity": ident, "session": sid}
    os.makedirs(WAKE_LOG_DIR, exist_ok=True)
    wlog = os.path.join(
        WAKE_LOG_DIR, "%s-%s.log"
        % (ident, datetime.now().strftime("%Y%m%d-%H%M%S")))
    try:
        fh = open(wlog, "ab")
        proc = popen_hidden(
            [devin_bin(), "-r", sid, "-p", WAKE_PROMPT,
             "--permission-mode", WAKE_PERMISSION_MODE],
            cwd=WORKDIR, stdout=fh, stderr=subprocess.STDOUT)
    except OSError as exc:
        state["failures"][ident] = state["failures"].get(ident, 0) + 1
        return {"action": "skip", "identity": ident,
                "reason": "spawn-failed:%s" % exc}
    state["inflight"][ident] = {
        "pid": proc.pid, "session": sid, "spawned_at": now, "log": wlog,
        "recovery_probe": bool(state["breaker"].get("recovering")),
    }
    day["count"] += 1
    day["last"] = now
    state["last_wake_at"] = now
    return {"action": "wake", "identity": ident, "session": sid,
            "pid": proc.pid, "log": wlog}


# --------------------------------------------------------------------------
# Poll

PROGRESS_DIR = os.path.join(WORKDIR, "Database", "FFXII TZA", "_index",
                            "progress")
PROGRESS_SCRIPT = os.path.join(PROGRESS_DIR, "progress_report.py")
PROGRESS_DIRTY = os.path.join(PROGRESS_DIR, ".dirty")
PROGRESS_INTERVAL = 1800          # 30-min cadence (directive 2026-09-27)


def maybe_progress_report(state):
    """Refresh the L1/L2 route report on the controller cadence.

    Time-gated here; fingerprint-skipping is the generator's own job
    (`auto` stamps checked_at and exits when inputs did not move). A
    `.dirty` mark left by publish_paths.sh forces regeneration. First
    loop iteration after startup always runs it (last_run defaults 0).
    The hook never blocks the loop on a missing package or a hung run.
    """
    if not os.path.exists(PROGRESS_SCRIPT):
        return
    st = state.setdefault("progress_report", {})
    now = time.time()
    dirty = os.path.exists(PROGRESS_DIRTY)
    if not dirty and now - st.get("last_run", 0) < PROGRESS_INTERVAL:
        return
    try:
        r = run_hidden([sys.executable, PROGRESS_SCRIPT, "auto"],
                       cwd=WORKDIR, capture_output=True, timeout=180)
        st["last_run"] = now
        st["last_rc"] = r.returncode
        st["last_out"] = (r.stdout or b"").decode("utf-8", "replace")[-200:]
        # The .dirty mark is a debt, not a hint: it is consumed ONLY after a
        # successful generation/publication (rc 0). A failed or incomplete
        # run leaves the mark so the next tick retries and the last-good
        # output set is never silently treated as current.
        if dirty and r.returncode == 0:
            try:
                os.unlink(PROGRESS_DIRTY)
            except OSError:
                pass
        log({"event": "progress_report", "rc": r.returncode,
             "dirty": dirty, "dirty_consumed": bool(dirty and r.returncode == 0),
             "out": st["last_out"]})
    except Exception as e:
        st["last_error"] = str(e)
        log({"event": "progress_report_error", "error": str(e)})


DASH_SCRIPT = os.path.join(WORKDIR, "Database", "Tools", "dashboard",
                           "build_views.py")
DASH_BOARD = os.path.join(WORKDIR, "Database", "FFXII TZA", "_index",
                          "_inbox", "TEAM.json")
DASH_INTERVAL = 1800          # 30-min reconciliation cadence
DASH_DEBOUNCE = 300           # board transitions rebuild at most every 5 min


def maybe_dashboard_build(state):
    """Refresh the dashboard generation on the controller cadence.

    Triggers: first loop iteration, a TEAM.json mtime change debounced to
    one build per DASH_DEBOUNCE, and an unconditional DASH_INTERVAL
    reconciliation. The builder refuses to commit when a strict input
    moved mid-build, so a racing write is a retry, not corruption, and
    board/watchdog state are declared volatile snapshots. Deterministic
    code only - no model call, and never blocks the loop on a missing
    script or a hung build.
    """
    if not os.path.exists(DASH_SCRIPT):
        return
    st = state.setdefault("dashboard", {})
    now = time.time()
    # Exposed for the dashboard's countdown: the cadence this controller is
    # actually configured with, and when the next reconciliation is due.
    # Board-triggered debounced builds reset last_run, so next_due slides with
    # them - that matches how the dashboard already computes it.
    st["interval"] = DASH_INTERVAL
    st["next_due"] = (st.get("last_run") or now) + DASH_INTERVAL
    try:
        board_mtime = os.path.getmtime(DASH_BOARD)
    except OSError:
        board_mtime = 0
    moved = board_mtime != st.get("board_mtime", 0)
    due = now - st.get("last_run", 0) >= DASH_INTERVAL
    debounced = moved and now - st.get("last_run", 0) >= DASH_DEBOUNCE
    if not ("last_run" not in st or due or debounced):
        return
    try:
        r = run_hidden([sys.executable, DASH_SCRIPT],
                       cwd=os.path.dirname(DASH_SCRIPT),
                       capture_output=True, timeout=300)
        st["last_run"] = now
        st["board_mtime"] = board_mtime
        st["last_rc"] = r.returncode
        st["last_out"] = (r.stdout or b"").decode("utf-8", "replace")[-200:]
        log({"event": "dashboard_build", "rc": r.returncode,
             "trigger": "interval" if due else "board",
             "out": st["last_out"]})
    except Exception as e:
        st["last_error"] = str(e)
        log({"event": "dashboard_build_error", "error": str(e)})


TRANSITIONS_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "transitions.py")
TRANSITIONS_SHADOW_CYCLES = 3   # dry-run cycles before --apply activates


def maybe_transitions(state):
    """Run the review->next-step transition pass from the controller.

    M2/A16: deterministic and idempotent - transitions.py only files a
    transition task for a DONE review that carries the `reviews` field and
    a `verdict:` result ref, through team.py. Adoption is shadowed first:
    the first TRANSITIONS_SHADOW_CYCLES iterations run dry and are logged
    as `transitions_shadow`; from then on the pass runs with --apply
    (created/exists/planned statuses are all logged, so an unexpected
    transition is visible in the controller log). Never blocks the loop.
    """
    if not os.path.exists(TRANSITIONS_SCRIPT):
        return
    st = state.setdefault("transitions", {})
    apply_mode = st.get("shadow_ok", 0) >= TRANSITIONS_SHADOW_CYCLES
    cmd = [sys.executable, TRANSITIONS_SCRIPT, "--agent", "SWE2-FRONTIER",
           "--json"]
    if apply_mode:
        # A team.py apply serializes under contention (~60-240 s measured); the
        # budget defers overflow ops to the next cycle instead of dying mid-write
        # at the timeout (SWE2-FRONTIER-DEFECT-TRANSITIONS-APPLY-120S).
        cmd += ["--apply", "--apply-budget-s", "240"]
    try:
        r = run_hidden(cmd, cwd=os.path.dirname(TRANSITIONS_SCRIPT),
                       capture_output=True, timeout=300)
        if r.returncode == 0:
            st["shadow_ok"] = st.get("shadow_ok", 0) + 1
        st["last_rc"] = r.returncode
        st["last_out"] = (r.stdout or b"").decode("utf-8", "replace")[-400:]
        log({"event": "transitions_apply" if apply_mode else "transitions_shadow",
             "rc": r.returncode, "planned_or_applied": st["last_out"]})
    except Exception as e:
        st["last_error"] = str(e)
        log({"event": "transitions_error", "error": str(e)})


GOAL_RESUME_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "goal_resume.py")
# Claude lanes (OPUS-REQ-FRONTIER-CLAUDE-LANE-ADAPTER, M2/A15). Registered exact
# session ids verified against live transcripts 2026-09-29:
#   OPUS  96b9c437 - "You are Opus 5.5 in the structural OPUS lane" (live, busy)
#   FABLE a632bd57 - most recent FABLE transcript on this host (ended 09-18)
CLAUDE_LANES = {"OPUS": "96b9c437-785b-434d-8ab7-046701b2ae88",
                "FABLE": "a632bd57-8ef6-4919-ba38-655e8201c26c"}
CLAUDE_LANE_SHADOW_CYCLES = 1   # dry-run classification passes before --execute
CLAUDE_LANE_INTERVAL = 900      # re-classify each lane at most every 15 min
GOAL_RESUME_RESUMABLE = {"FALSE_COMPLETION", "ORDINARY_STOP"}


def maybe_claude_lanes(state):
    """Classify the registered Claude lanes from the controller cadence.

    A15: every lane gets a dry-run `goal_resume.py --session <id>` and the
    classification is logged and exposed in watchdog-state (the dashboard
    fleet view reads it). After CLAUDE_LANE_SHADOW_CYCLES clean shadow
    passes, resumable verdicts (FALSE_COMPLETION / ORDINARY_STOP only) run
    with --execute. goal_resume itself refuses USER_STOP / USAGE_LIMIT /
    ERROR / ACTIVE / UNKNOWN, and its retry budget is bounded by
    work/goal-gate/resume-state.json - this hook adds no retries of its own
    and never bypasses a user stop or a limit.
    """
    if not os.path.exists(GOAL_RESUME_SCRIPT):
        return
    st = state.setdefault("claude_lanes", {})
    now = time.time()
    for lane, sid in CLAUDE_LANES.items():
        ent = st.setdefault(lane, {"session": sid, "shadow_ok": 0})
        ent["session"] = sid
        if now - ent.get("last_run", 0) < CLAUDE_LANE_INTERVAL:
            continue
        execute = ent.get("shadow_ok", 0) >= CLAUDE_LANE_SHADOW_CYCLES
        cmd = [sys.executable, GOAL_RESUME_SCRIPT, "--session", sid]
        if execute:
            cmd.append("--execute")
        try:
            r = run_hidden(cmd, cwd=os.path.dirname(GOAL_RESUME_SCRIPT),
                           capture_output=True, timeout=660)
            out = (r.stdout or b"").decode("utf-8", "replace")
            # First token on the first line is the classification
            # (FALSE_COMPLETION / ORDINARY_STOP / USER_STOP / ... / RESUMED).
            cls = out.split(None, 1)[0] if out.split() else "NO_OUTPUT"
            ent["last_run"] = now
            ent["last_rc"] = r.returncode
            ent["classification"] = cls
            ent["last_out"] = out[-300:]
            if r.returncode == 0 and not execute:
                ent["shadow_ok"] = ent.get("shadow_ok", 0) + 1
            # --execute is only ever passed after shadow cycles; goal_resume
            # additionally gates on the resumable set. A non-resumable
            # classification under --execute prints PLANNED/refusal only.
            log({"event": "claude_lane_execute" if execute else
                 "claude_lane_shadow", "lane": lane, "session": sid,
                 "classification": cls, "rc": r.returncode})
        except Exception as e:
            ent["last_run"] = now
            ent["last_error"] = str(e)
            log({"event": "claude_lane_error", "lane": lane, "error": str(e)})


def poll(state, send, dry_run):
    sessions = list_sessions()
    if sessions is None:
        log({"event": "list_failed"})
        return
    fleet_map = load_map()
    now = time.time()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    reap_inflight(state, sessions, fleet_map)
    reconcile_map(fleet_map, sessions)

    authed = auth_ok()
    plan = load_plan()
    board_ok, board_detail = board_integrity()
    need = board_need() if board_ok else {}
    dep = {}
    if board_ok:
        try:
            dep = dep_blocked_owners(
                json.loads(open(BOARD_FILE, encoding="utf-8").read()))
        except Exception:
            dep = {}
    valid_plan = plan if isinstance(plan, dict) and "desired" in plan else None
    desired, target, source = desired_set(valid_plan, need, dep)

    istate = {}
    for ident in FLEET_TITLES:
        istate[ident] = identity_state(fleet_map, state, sessions, ident, now)
    busy = {k: v for k, v in istate.items() if v[0].startswith("busy")}
    foreign = foreign_active(sessions, fleet_map, now)
    # Only specialist lanes consume the TARGET_ACTIVE slots. A busy FRONTIER
    # (an inflight planner wake or a manually continued session) runs
    # alongside them and must not evict a specialist.
    spec_busy = {k: v for k, v in busy.items() if k in SPECIALISTS}
    active_count = len(spec_busy) + len(foreign)

    rp = replan_view(state)
    due = replan_due(rp, now)
    # A planner held by a subagent (see desired_set) is not woken either: the subagent IS the planner.
    if valid_plan and PLANNER in (valid_plan.get("held_by_subagent") or []):
        due = False
    planner = PLANNER
    wakes_today = sum(d.get(today, {}).get("count", 0)
                      for d in state["wakes"].values())

    ev = {"event": "poll", "desired": desired, "source": source,
          "target": target, "authed": authed,
          "lane_state": {k: v[0] for k, v in istate.items()},
          "foreign_active": foreign, "active_count": active_count,
          "breaker_open": breaker_open(state),
          "wakes_today": wakes_today,
          "replan_pending": rp["pending"],
          "replan_due": due,
          "replan_events": len(rp["events"]),
          "replan_malformed": len(rp["malformed"]),
          "need": {k: v[2] for k, v in need.items() if not k.startswith("__")}}
    if dep:
        # Lanes (incl. non-SWE2, which are informational only) holding an
        # unfinished dependency of someone's BLOCKED work.
        ev["dep_need"] = {k: sorted(v) for k, v in dep.items()}
    if rp["pending"]:
        ev["replan_reasons"] = sorted({e["reason"] for e in rp["events"]})
    if isinstance(plan, dict) and "__stale__" in plan:
        ev["plan"] = "stale:" + str(plan["__stale__"])
    if need.get("__error__"):
        ev["need_error"] = need["__error__"]
    if not board_ok:
        ev["board_incident"] = board_detail

    wake_result = None
    if not send:
        ev["mode"] = "status"
    elif not authed:
        ev["mode"] = "no-auth"
    elif not board_ok:
        # A rolled-back or divergent board is an incident, not an empty
        # frontier: hold every wake until recovery installs the candidate.
        ev["mode"] = "board-incident"
    elif breaker_open(state):
        ev["mode"] = "breaker-open"
    elif state["breaker"].get("recovering") and any(
            w.get("recovery_probe") for w in state["inflight"].values()):
        # Hold spawns only while an actual probe is in flight. Any inflight
        # non-probe wake used to satisfy this test too, which wedged recovery
        # permanently: no probe could spawn while an ordinary wake ran, so
        # `recovering` never cleared and every desired lane starved.
        ev["mode"] = "recovery-probe-in-flight"
    else:
        at_cap = active_count >= min(target, HARD_MAX_ACTIVE)
        candidates = []
        skipped = {}
        if due:
            # The planner wake is slot-free: it proceeds at specialist
            # capacity and does not consume a slot. If FRONTIER is already
            # working it sees the pending replan at its next board pass - no
            # duplicate wake.
            if istate[planner][0].startswith("busy"):
                ev["replan"] = "frontier-already-busy"
            else:
                ok, reason = eligible(state, fleet_map, sessions,
                                      planner, now, today, planner=True)
                if ok:
                    candidates.append((-1, -1, planner))
                else:
                    ev["replan"] = "frontier-not-eligible:" + reason
        if at_cap:
            for ident in desired:
                if not istate[ident][0].startswith("busy"):
                    skipped[ident] = "at-capacity"
            if due and not candidates and "replan" not in ev:
                ev["replan"] = "deferred-planner-ineligible"
        else:
            for ident in desired:
                if istate[ident][0].startswith("busy"):
                    skipped[ident] = istate[ident][0]
                    continue
                ok, reason = eligible(state, fleet_map, sessions, ident,
                                      now, today)
                if not ok:
                    skipped[ident] = reason
                    continue
                n = need.get(ident, (3, "P9", "plan-pinned"))
                candidates.append((_prio_num(n[1]), n[0], ident))
        if skipped:
            ev["skipped"] = skipped
        if not candidates:
            ev["mode"] = "at-capacity" if at_cap else "none-eligible"
        else:
            candidates.sort()
            wake_result = spawn_wake(state, fleet_map, sessions,
                                     candidates[0][2], now, today,
                                     dry_run or not send)
            ev["mode"] = "dry-run" if dry_run else "send"
            if wake_result.get("identity") == planner and due \
                    and wake_result.get("action") in ("wake", "would_wake"):
                state["replan"]["planner_wake_sent_at"] = now

    # Persist which desired lanes still want a slot ("queued workers").
    woken = wake_result.get("identity") if wake_result else None
    queued = {}
    for ident in desired:
        if ident == woken or istate[ident][0].startswith("busy"):
            continue
        queued[ident] = ev.get("skipped", {}).get(ident, ev["mode"])
    state["queued"] = queued

    # A dependency owner squeezed out of the desired set by the target cap
    # still stalls the whole chain - that is a scheduling defect, so it
    # files a replan event for the planner instead of waiting silently.
    if send and dep:
        excluded = [k for k in dep if k in SPECIALISTS
                    and k not in desired and not istate[k][0].startswith("busy")]
        for ident in excluded:
            append_replan(ident, "DEP_STARVED",
                          "owns deps %s of BLOCKED work but got no slot"
                          % sorted(dep[ident]))

    # Starvation telemetry: eligible-but-unselected gap and last-useful-op
    # age per specialist. Reporting only - it never reorders selection; a
    # material case logs starvation_warn and files one replan event.
    starved = starvation_pass(state, istate, need, desired,
                              ev.get("skipped", {}), woken, now)
    if starved:
        ev["starvation_warned"] = starved

    if wake_result:
        ev["decision"] = wake_result
    log(ev)
    save_json(MAP_FILE, fleet_map)


# --------------------------------------------------------------------------

def resume_block_status(ident, tasks=None):
    """Semantic resume-block check: the block must exist, name this identity,
    and its `Current package/claim` must match a live board task owned by or
    routed to this lane. TEAM.json is authoritative - a mismatch is flagged
    'stale:*' for repair at the worker's next checkpoint, never auto-fixed."""
    path = os.path.join(WORKDIR, "Database", "FFXII TZA", "_index", "_inbox",
                        ident + ".md")
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return "no-inbox-file"
    blocks = re.findall(r"## Resume state\b(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if not blocks:
        return "no-resume-block"
    if len(blocks) > 1:
        return "stale:duplicate-blocks"
    block = blocks[0]
    if ident not in block:
        return "stale:wrong-identity"
    claim_line = next((ln for ln in block.splitlines()
                       if "package/claim" in ln.lower()), "")
    tm = re.search(r"`([A-Z][A-Z0-9-]+)`", claim_line)
    if not tm:
        # declared none / unparseable - valid only while the lane holds no
        # ACTIVE board claim
        if tasks and any(t["status"] == "ACTIVE"
                         and (t.get("agent") == ident
                              or t.get("assigned_to") == ident)
                         for t in tasks.values()):
            return "stale:none-vs-active-claim"
        return "ok" if "none" in claim_line.lower() else "no-claim-line"
    task_id = tm.group(1)
    if tasks is None:
        return "claim:%s" % task_id
    t = tasks.get(task_id)
    if t is None:
        return "stale:claim-not-on-board"
    if t.get("agent") != ident and t.get("assigned_to") != ident:
        return "stale:claim-owner=%s" % (t.get("agent") or t.get("assigned_to"))
    if t["status"] not in ("ACTIVE", "READY"):
        return "stale:claim-%s" % t["status"].lower()
    return "ok"


def status_report(state):
    sessions = list_sessions() or {}
    fleet_map = load_map()
    now = time.time()
    plan = load_plan()
    need = board_need()
    valid_plan = plan if isinstance(plan, dict) and "desired" in plan else None
    desired, target, source = desired_set(valid_plan, need)
    rp = replan_view(state)
    try:
        tasks = {t["id"]: t for t in json.loads(
            open(BOARD_FILE, encoding="utf-8").read())["tasks"]}
    except Exception:
        tasks = None
    print("fleet-map: %s" % MAP_FILE)
    print("plan:      %s (%s)" % (PLAN_FILE,
          "fresh, source=plan" if valid_plan else "absent/stale -> board"))
    print("target_active=%d hard_max=%d  breaker=%s" % (
        target, HARD_MAX_ACTIVE,
        "OPEN until %s" % datetime.fromtimestamp(
            state["breaker"].get("open_until", 0)).isoformat()
        if breaker_open(state) else "closed"))
    if rp["pending"]:
        print("replan:    PENDING (%d events%s: %s) due=%s" % (
            len(rp["events"]),
            " +%d malformed" % len(rp["malformed"]) if rp["malformed"] else "",
            ", ".join(sorted({e.get("reason", "?") for e in rp["events"]})),
            replan_due(rp, now)))
    else:
        print("replan:    none pending")
    cpid = controller_pid()
    print("controller:%s" % (" pid %d %s" % (
        cpid, "alive" if pid_is_watchdog(cpid) else "DEAD") if cpid
        else " not running"))
    queued = state.get("queued") or {}
    if queued:
        print("queued:    %s" % ", ".join(
            "%s(%s)" % kv for kv in sorted(queued.items())))
    starv = state.get("starvation") or {}
    rows = []
    for ident in SPECIALISTS:
        rec = starv.get(ident) or {}
        if rec.get("eligible_since"):
            rows.append("%s(elig %.1fh, no-op %.1fh, %s)" % (
                ident,
                (now - rec["eligible_since"]) / 3600,
                (now - (rec.get("last_useful_at")
                        or rec.get("first_seen", now))) / 3600,
                rec.get("defer", "?")))
    if rows:
        print("starving:  %s" % ", ".join(rows))
    print("%-18s %-8s %-16s %-24s %-16s %s" % (
        "identity", "desired", "session", "state", "resume", "need"))
    for ident in FLEET_TITLES:
        rec = fleet_map["identities"][ident]
        st, detail = identity_state(fleet_map, state, sessions, ident, now)
        print("%-18s %-8s %-16s %-24s %-16s %s" % (
            ident, "ctrl" if ident == PLANNER
            else ("yes" if ident in desired else "-"),
            rec.get("current"), "%s %s" % (st, detail),
            resume_block_status(ident, tasks),
            need.get(ident, ("", "", "parked"))[2]))


# --------------------------------------------------------------------------
# Controller lifecycle (single instance, survivable)

def controller_pid():
    try:
        return int(open(PID_FILE).read().strip())
    except (OSError, ValueError):
        return None


def pid_is_watchdog(pid):
    """Alive AND its command line names this script - guards against PID
    reuse, so a stale pidfile can never make us kill or trust a stranger."""
    if not pid:
        return False
    try:
        out = run_hidden(
            ["powershell", "-NoProfile", "-Command",
             "(Get-CimInstance Win32_Process -Filter 'ProcessId=%d')"
             ".CommandLine" % pid],
            capture_output=True, text=True, timeout=15).stdout or ""
    except (OSError, subprocess.TimeoutExpired):
        return False
    return "swe2_watchdog" in out


def controller_start(interval=POLL_INTERVAL):
    pid = controller_pid()
    if pid and pid_is_watchdog(pid):
        print("controller already running: pid %d" % pid)
        return False
    os.makedirs(STATE_DIR, exist_ok=True)
    logf = open(CTRL_LOG, "ab")
    proc = popen_hidden(
        [sys.executable, "-u", os.path.abspath(__file__),
         "--loop", "--interval=%d" % interval],
        detached=True,
        cwd=WORKDIR, stdout=logf, stderr=subprocess.STDOUT,
        close_fds=True)
    with open(PID_FILE, "w") as fh:
        fh.write(str(proc.pid))
    print("controller started: pid %d interval %ds log %s"
          % (proc.pid, interval, CTRL_LOG))
    return True


def controller_stop():
    pid = controller_pid()
    if not pid:
        print("no controller pidfile")
        return
    if not pid_is_watchdog(pid):
        print("pidfile stale (pid %s is not this watchdog) - clearing" % pid)
        try:
            os.remove(PID_FILE)
        except OSError:
            pass
        return
    # No /T: in-flight wakes (devin -r children) are independent sessions and
    # must survive a controller turnover - killing the tree kills a live
    # worker, which is exactly what the handover rule forbids.
    run_hidden(["taskkill", "/PID", str(pid), "/F"],
               capture_output=True)
    try:
        os.remove(PID_FILE)
    except OSError:
        pass
    print("controller stopped: pid %d" % pid)


CONTROLLER_STALE_S = 3 * POLL_INTERVAL + 60


def watchdog_loop_pids():
    """Every live pid running this script with --loop - the authoritative
    controller set, discovered from the process table, not the pidfile."""
    try:
        out = run_hidden(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" |"
             " Select-Object ProcessId,CommandLine |"
             " ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
            capture_output=True, text=True, timeout=20).stdout or ""
    except (OSError, subprocess.TimeoutExpired):
        return None   # scan failed -> unknown, fail closed
    me = os.path.abspath(__file__).lower().replace("/", "\\")
    pids = []
    for line in out.splitlines():
        parts = line.strip().split(None, 1)
        if len(parts) != 2 or not parts[0].isdigit():
            continue
        pid_s, cmd = parts
        cmd_l = cmd.replace("/", "\\").lower()
        if "swe2_watchdog" in cmd_l and "--loop" in cmd_l \
                and (me.split("\\")[-1] in cmd_l):
            pids.append(int(pid_s))
    return pids


def ensure_decision(pids, heartbeat_age, stale_s=CONTROLLER_STALE_S):
    """Pure liveness verdict for the controller, unit-testable.

    pids: live `swe2_watchdog --loop` processes (None = scan failed).
    heartbeat_age: seconds since the state file's last write (None = gone).
    """
    if pids is None:
        return "refuse-unknown"
    if len(pids) > 1:
        return "refuse-duplicate"
    if len(pids) == 1:
        if heartbeat_age is not None and heartbeat_age <= stale_s:
            return "healthy"
        return "restart"
    return "start"


def ensure_controller(interval=POLL_INTERVAL):
    """Single-owner controller reconciliation - the supported recovery path.

    - two or more live controller loops: fail closed, touch nothing (a
      duplicate scheduler is worse than a paused one; a human resolves it)
    - exactly one, heartbeat fresh: report healthy, no action
    - exactly one, heartbeat stale: it is wedged; stop it (children survive)
      and start one replacement
    - none: start one
    Returns True if a (re)start was issued.
    """
    pids = watchdog_loop_pids()
    try:
        age = time.time() - os.path.getmtime(STATE_FILE)
    except OSError:
        age = None
    verdict = ensure_decision(pids, age)
    if verdict == "healthy":
        print("ensure: controller healthy - pid %d, heartbeat %.0fs"
              % (pids[0], age))
        return False
    if verdict == "refuse-duplicate":
        print("ensure: REFUSED - %d live controllers %s; resolve to one "
              "manually" % (len(pids), pids))
        return False
    if verdict == "refuse-unknown":
        print("ensure: process scan failed - refusing to start (could not "
              "prove no other controller)")
        return False
    if verdict == "restart":
        print("ensure: controller pid %d wedged (heartbeat %s) - restarting"
              % (pids[0], "no state file" if age is None else
                 "%.0fs old" % age))
        run_hidden(["taskkill", "/PID", str(pids[0]), "/F"],
                   capture_output=True)
        try:
            os.remove(PID_FILE)
        except OSError:
            pass
        controller_start(interval)
        return True
    print("ensure: no controller running - starting one")
    controller_start(interval)
    return True


def install_startup():
    """Register logon startup via Windows Task Scheduler - the smallest
    supported persistence. Falls back to the HKCU Run key when schtasks is
    denied (non-elevated shells cannot write scheduler tasks).
    Remove with: schtasks /Delete /TN SWE2-Fleet-Watchdog
             or: reg delete HKCU\\Software\\Microsoft\\Windows\\
                 CurrentVersion\\Run /v SWE2FleetWatchdog"""
    # Register pythonw, not python: a console-subsystem interpreter flashes
    # a visible CMD window at every logon. The script is print-safe under
    # pythonw (stdout/stderr redirect to devnull at import).
    exe = sys.executable
    if os.name == "nt":
        pyw = os.path.join(os.path.dirname(exe), "pythonw.exe")
        if os.path.exists(pyw):
            exe = pyw
    tr = '"%s" -u "%s" controller start' % (
        exe, os.path.abspath(__file__))
    cmd = ["schtasks", "/Create", "/TN", "SWE2-Fleet-Watchdog",
           "/SC", "ONLOGON", "/RL", "LIMITED", "/F", "/TR", tr]
    proc = run_hidden(cmd, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0:
        print(out.strip())
        return
    if "denied" not in out.lower():
        print(out.strip())
        return
    print("schtasks denied - falling back to HKCU Run key")
    reg = ["reg", "add",
           r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
           "/v", "SWE2FleetWatchdog", "/t", "REG_SZ",
           "/d", tr, "/f"]
    proc = run_hidden(reg, capture_output=True, text=True)
    print((proc.stdout or proc.stderr or "").strip())


def rebuild_state():
    """Regenerate durable fleet state from `devin list`. Fail closed on any
    ambiguous or missing fleet identity - never guess a mapping."""
    sessions = list_sessions()
    if sessions is None:
        print("fail closed: `devin list --format json` unavailable")
        sys.exit(3)
    by_title = {}
    for sid, s in sessions.items():
        by_title.setdefault((s.get("title") or "").strip(), []).append(sid)
    fmap = {"identities": {},
            "never_wake_sessions": sorted(NEVER_WAKE_SESSIONS),
            "never_wake_titles": sorted(NEVER_WAKE_TITLES),
            "rebuilt_at": now_iso()}
    problems = []
    for ident in FLEET_TITLES:
        ids = [sid for sid in by_title.get(ident, [])
               if sid not in NEVER_WAKE_SESSIONS]
        if len(ids) != 1:
            problems.append("%s: %s" % (ident, ids or "no session found"))
            continue
        fmap["identities"][ident] = {"canonical": ids[0], "current": ids[0]}
    if problems:
        print("fail closed - ambiguous fleet titles:")
        for p in problems:
            print("  " + p)
        sys.exit(3)
    save_json(MAP_FILE, fmap)
    if not os.path.exists(STATE_FILE):
        save_json(STATE_FILE, load_state())
    print("rebuilt %s" % MAP_FILE)
    for ident in FLEET_TITLES:
        print("  %-18s %s" % (ident, fmap["identities"][ident]["canonical"]))
    print("never-wake sessions: %s" % ", ".join(fmap["never_wake_sessions"]))


def main():
    args = sys.argv[1:]

    def opt(name, default=None):
        for i, a in enumerate(args):
            if a == name and i + 1 < len(args):
                return args[i + 1]
            if a.startswith(name + "="):
                return a.split("=", 1)[1]
        return default

    if args and args[0] == "replan":
        if "--clear" in args:
            # Planner-only: mechanically restricted to SWE2-FRONTIER.
            if opt("--identity") != "SWE2-FRONTIER":
                print("refused: replan --clear requires "
                      "--identity SWE2-FRONTIER")
                sys.exit(2)
            n = clear_replan()
            print("replan cleared: %d events consumed" % n)
            return
        identity = opt("--identity")
        reason = opt("--reason")
        note = opt("--note", "")
        test = "--test" in args
        if test:
            if not (identity or "").startswith("SWE2-TEST-"):
                print("refused: --test identities must be SWE2-TEST-*")
                sys.exit(2)
        elif identity not in FLEET_TITLES:
            print("refused: --identity must be one of the 8 fleet identities "
                  "(test events need --test and SWE2-TEST-*)")
            sys.exit(2)
        if reason not in REPLAN_REASONS:
            print("refused: --reason must be one of %s"
                  % ", ".join(sorted(REPLAN_REASONS)))
            sys.exit(2)
        append_replan(identity, reason, note, test=test)
        evs, bad = replan_events()
        print("replan pending: %d events%s (%s)" % (
            len(evs), " +%d malformed" % len(bad) if bad else "",
            ", ".join(sorted({e.get("reason", "?") for e in evs}))))
        return

    if args and args[0] == "controller":
        sub = args[1] if len(args) > 1 else "status"
        if sub == "start":
            interval = int(opt("--interval", str(POLL_INTERVAL)) or 0)
            controller_start(interval)
        elif sub == "stop":
            controller_stop()
        elif sub == "restart":
            controller_stop()
            controller_start(int(opt("--interval", str(POLL_INTERVAL)) or 0))
        elif sub == "ensure":
            # Idempotent single-owner reconciliation (A15/incident response):
            # safe for any lane or startup hook to run - it refuses when a
            # healthy or duplicate controller exists.
            ensure_controller(int(opt("--interval", str(POLL_INTERVAL)) or 0))
        elif sub == "status":
            status_report(load_state())
        elif sub == "install-startup":
            install_startup()
        else:
            print("usage: controller start|stop|restart|status|install-startup")
            sys.exit(2)
        return

    if args and args[0] == "rebuild":
        rebuild_state()
        return

    if args and args[0] == "wake":
        # Manual ops wake: spawn ONE bounded wake through the normal
        # eligibility gates (session lock, daily cap, debounce, stagger,
        # parked lanes) and the same inflight/telemetry accounting the
        # poll loop uses. It does NOT consult the desired set - it is for
        # validating a lane outside the scheduled trio (e.g. after an env
        # fix) - so it can briefly take the fleet over TARGET_ACTIVE. The
        # circuit breaker is still honoured: never wake into an open one.
        #
        # A running controller owns the state file: it holds `state` in
        # memory and rewrites the file every poll, which silently drops the
        # inflight record a manual wake just wrote (seen 2026-09-15 - the
        # wake ran, its exit was never classified). Refuse while the loop
        # is up; --force overrides when losing the accounting is acceptable.
        identity = opt("--identity")
        if identity not in FLEET_TITLES:
            print("refused: --identity must be one of the 8 fleet "
                  "identities")
            sys.exit(2)
        cpid = controller_pid()
        if cpid and pid_is_watchdog(cpid) and "--force" not in args:
            print("refused: controller pid %d is running - a manual wake's "
                  "inflight record is overwritten by its next save; either "
                  "let the scheduler wake this lane, stop the controller "
                  "first, or pass --force (accounting may be lost)" % cpid)
            sys.exit(2)
        state = load_state()
        sessions = list_sessions()
        if sessions is None:
            print("fail closed: `devin list` unavailable")
            sys.exit(3)
        if breaker_open(state):
            print("refused: circuit breaker open until %s"
                  % datetime.fromtimestamp(
                      state["breaker"]["open_until"]).isoformat())
            sys.exit(2)
        fleet_map = load_map()
        now = time.time()
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        ok, reason = eligible(state, fleet_map, sessions, identity,
                              now, today, planner=(identity == PLANNER))
        if not ok:
            print("refused: %s not eligible (%s)" % (identity, reason))
            sys.exit(2)
        res = spawn_wake(state, fleet_map, sessions, identity, now, today,
                         dry_run=False)
        save_json(STATE_FILE, state)
        print(json.dumps(res))
        return

    send = "--status" not in args
    dry_run = "--dry-run" in args
    state = load_state()

    if "--once" in args or ("--loop" not in args and send):
        # A manual poll writes the state file; a running loop rewrites it
        # from its own in-memory copy on its next poll, silently dropping
        # whatever this poll recorded (inflight entries, cap charges).
        # Warn, don't refuse: --once is also the recovery tool for a dead
        # controller, and refusing here would break it.
        cpid = controller_pid()
        if cpid and pid_is_watchdog(cpid) and cpid != os.getpid():
            print("note: controller pid %d is running - this poll's state "
                  "writes may be overwritten by its next save" % cpid)

    if "--status" in args:
        status_report(state)
        return

    if "--loop" in args:
        interval = POLL_INTERVAL
        for a in args:
            if a.startswith("--interval="):
                interval = int(a.split("=", 1)[1])
        pid = controller_pid()
        if pid and pid != os.getpid() and pid_is_watchdog(pid):
            print("refusing: another controller is running (pid %d)" % pid)
            sys.exit(3)
        with open(PID_FILE, "w") as fh:
            fh.write(str(os.getpid()))
        log({"event": "controller_start", "interval": interval,
             "target": TARGET_ACTIVE, "hard_max": HARD_MAX_ACTIVE,
             "dry_run": dry_run, "pid": os.getpid()})
        while True:
            poll(state, send, dry_run)
            maybe_progress_report(state)
            maybe_dashboard_build(state)
            maybe_transitions(state)
            maybe_claude_lanes(state)
            # Liveness heartbeat for `controller ensure` - the state file's
            # mtime is the observable pulse; the field makes the contract
            # explicit for readers.
            state["heartbeat"] = time.time()
            save_json(STATE_FILE, state)
            time.sleep(interval)
    else:
        poll(state, send, dry_run)
        save_json(STATE_FILE, state)


if __name__ == "__main__":
    main()
