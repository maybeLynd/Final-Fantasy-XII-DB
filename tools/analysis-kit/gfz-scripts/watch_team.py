#!/usr/bin/env python3
"""watch_team.py - emit a line whenever the helper sessions' state changes.

Polls every 60 s and prints ONLY on change, so a quiet team produces no notifications and the
moment they go idle produces exactly one.

Coverage: silence must not look like success. It emits on EVERY transition, not just the one that
is convenient -- any session going idle, all of them going idle, a session disappearing, and read
errors. A watcher that only reported "all idle" would stay silent through a session dying.
"""
import glob
import io
import json
import os
import sys
import time

DIRS = [os.path.expanduser("~/.claude-trial1/sessions"),
        os.path.expanduser("~/.claude-trial2/sessions")]


def snapshot():
    out = {}
    for d in DIRS:
        for p in glob.glob(os.path.join(d, "*.json")):
            try:
                j = json.load(io.open(p, encoding="utf-8"))
                if j.get("name"):
                    out[j["name"]] = j.get("status", "?")
            except Exception:
                pass
    return out


SUSTAIN = 3          # consecutive idle polls before a session counts as needing a prompt
RENOTIFY = 20        # re-report an UNCHANGED idle set this often, in polls (~minutes)

# Why RENOTIFY exists, added 2026-09-04 after it cost five hours.
#
# The first version reported a set once and then stayed silent until the set CHANGED. That is
# right for churn and **wrong for a stall**: on 2026-09-04 it reported "ALL 6 IDLE" at 14:07 and
# said nothing more until 19:19, because the set never changed. The team sat idle for **five
# hours and twelve minutes** and produced nothing, and the watcher was behaving exactly as
# designed the entire time.
#
# **A condition that persists is not less urgent than one that just started; it is more.**
# Suppressing the repeat optimised for the watcher's tidiness over the thing being watched.


def main():
    """Emit only ACTIONABLE states.

    A session flips to `idle` between its own turns, so reporting every transition produced a
    notification a minute of pure churn. **A transient idle is not a session waiting for input.**
    So a session must be idle for SUSTAIN consecutive polls before it is reported, and a set that
    has already been reported is not reported again until it changes.
    """
    streak = {}
    reported = None
    first = True
    while True:
        try:
            cur = snapshot()
        except Exception as e:
            print("WATCH ERROR: %s" % e, flush=True)
            time.sleep(60)
            continue

        if not cur:
            if reported != "GONE":
                print("%s  NO SESSIONS VISIBLE - all gone from the registries"
                      % time.strftime("%H:%M:%S"), flush=True)
                reported = "GONE"
            time.sleep(60)
            continue

        for n, s in cur.items():
            streak[n] = streak.get(n, 0) + 1 if s == "idle" else 0
        stuck = sorted(n for n in cur if streak.get(n, 0) >= SUSTAIN)
        key = ",".join(stuck)
        ts = time.strftime("%H:%M:%S")

        if first:
            print("%s  watching %d sessions (reporting only idle >= %d min)"
                  % (ts, len(cur), SUSTAIN), flush=True)
            first = False
            same = 0
        elif key == reported and stuck:
            # Unchanged AND still stalled: nag on a slow cadence rather than going quiet.
            same += 1
            if same >= RENOTIFY:
                mins = SUSTAIN + RENOTIFY * (same // RENOTIFY)
                print("%s  STILL IDLE after ~%d min, nothing landed: %s"
                      % (ts, mins, " ".join(stuck)), flush=True)
                same = 0
        elif key != reported:
            same = 0
            if not stuck:
                print("%s  all working again" % ts, flush=True)
            elif len(stuck) == len(cur):
                print("%s  *** ALL %d IDLE for %d+ min *** they need a prompt: %s"
                      % (ts, len(stuck), SUSTAIN, " ".join(stuck)), flush=True)
            else:
                print("%s  idle %d+ min, need a prompt: %s   (%d still working)"
                      % (ts, SUSTAIN, " ".join(stuck), len(cur) - len(stuck)), flush=True)
            reported = key
        time.sleep(60)


if __name__ == "__main__":
    sys.exit(main())
