#!/usr/bin/env python3
"""test_swe2_watchdog_nowin.py -- regression test for the hidden-launch
invariant added 2026-09-15.

The fleet controller runs detached with no console, so any console-subsystem
child it spawns without the no-window creation flag pops a fresh VISIBLE CMD
window on the user's desktop (the periodic ~8-14 window bursts). Every
automated launch in swe2_watchdog.py must go through run_hidden() /
popen_hidden(), which attach:

  * the CREATE_NO_WINDOW creation flag (Windows)
  * a hidden STARTUPINFO (STARTF_USESHOWWINDOW + SW_HIDE)
  * stdin=DEVNULL (unattended children can never block on input)

and for the survivor controller child additionally the detached-process and
new-process-group flags. A fresh console flag and shell wrappers are banned
everywhere. Run: python test_swe2_watchdog_nowin.py
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import swe2_watchdog as wd

FAILURES = []


def check(cond, msg):
    if cond:
        print("PASS  %s" % msg)
    else:
        FAILURES.append(msg)
        print("FAIL  %s" % msg)


def check_hidden(kw, label):
    check(kw.get("stdin") == subprocess.DEVNULL,
          "%s: stdin is DEVNULL" % label)
    if os.name == "nt":
        flags = kw.get("creationflags", 0)
        check(flags & getattr(subprocess, "CREATE_NO_WINDOW", 0),
              "%s: creationflags request no console window" % label)
        check(not flags & getattr(subprocess, "CREATE_NEW_CONSOLE", 0),
              "%s: creationflags never allocate a fresh console" % label)
        si = kw.get("startupinfo")
        check(si is not None
              and si.dwFlags & subprocess.STARTF_USESHOWWINDOW
              and si.wShowWindow == 0,
              "%s: STARTUPINFO requests hidden window (SW_HIDE)" % label)


# 1. The kwargs builder itself.
check_hidden(wd._hidden_kwargs(), "_hidden_kwargs()")
check_hidden(wd._hidden_kwargs(detached=True), "_hidden_kwargs(detached)")
if os.name == "nt":
    dflags = wd._hidden_kwargs(detached=True)["creationflags"]
    check(dflags & getattr(subprocess, "DETACHED_PROCESS", 0)
          and dflags & getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
          "detached child gets DETACHED_PROCESS|CREATE_NEW_PROCESS_GROUP")

# 2. The wrappers actually deliver the flags to subprocess.
captured = {}


class _FakeProc:
    returncode = 0
    stdout = ""
    stderr = ""
    pid = 0


def _fake_run(cmd, **kw):
    captured.clear()
    captured.update(kw)
    captured["cmd"] = cmd
    return _FakeProc()


orig_run, orig_popen = subprocess.run, subprocess.Popen
subprocess.run = subprocess.Popen = _fake_run
try:
    wd.run_hidden(["devin", "version"], capture_output=True, text=True,
                  timeout=5)
    check_hidden(captured, "run_hidden(devin version)")
    check(captured.get("capture_output") and captured.get("timeout") == 5,
          "run_hidden forwards caller kwargs (capture/timeout)")
    wd.popen_hidden(["devin", "-r", "x", "-p", "Continue"], stdout=None)
    check_hidden(captured, "popen_hidden(wake)")
    wd.popen_hidden(["python", "x", "--loop"], detached=True)
    if os.name == "nt":
        check(captured["creationflags"]
              & getattr(subprocess, "DETACHED_PROCESS", 0),
              "popen_hidden(detached=True) carries detached flags")
finally:
    subprocess.run, subprocess.Popen = orig_run, orig_popen

# 3. Static sweep: no call site may bypass the helpers. Exactly one raw
#    subprocess.run and one raw subprocess.Popen exist - inside the helpers.
src = open(wd.__file__, encoding="utf-8").read()
# Count real call sites (non-empty argument lists) only - helper docstrings
# mention the API names without calling them.
raw_calls = re.findall(r"subprocess\.(?:run|Popen)\([^)\s]", src)
check(len(re.findall(r"subprocess\.run\([^)\s]", src)) == 1,
      "exactly one raw subprocess.run call site (inside run_hidden)")
check(len(re.findall(r"subprocess\.Popen\([^)\s]", src)) == 1,
      "exactly one raw subprocess.Popen call site (inside popen_hidden)")
check(len(raw_calls) == 2,
      "no other raw subprocess.run/Popen call sites exist")
check(not re.search(r"shell\s*=\s*True", src),
      "no shell=True anywhere in the watchdog")
check("CREATE_NEW_CONSOLE" not in src,
      "no fresh-console flag anywhere in the watchdog")
check(not re.search(r"\bcmd\.exe\b|\bcmd /c\b|\bstart /", src),
      "no cmd/start shell wrappers in the watchdog")
check("--permission-mode" in src
      and 'WAKE_PERMISSION_MODE = "dangerous"' in src,
      "noninteractive wakes run with --permission-mode dangerous "
      "(deliberate 2026-09-16: smart denied team.py/publish_paths, the "
      "fleet's whole output channel)")

# 4. The logon-startup registration must name a windowless interpreter.
check("pythonw.exe" in src,
      "install_startup prefers pythonw.exe (no login console)")

# 5. The recovery gate must hold spawns only while a genuine recovery probe
#    is in flight, never on any inflight wake. The 2026-09-26 wedge: a
#    non-probe wake in `inflight` satisfied `... and state["inflight"]`, so
#    no probe could ever spawn while an ordinary wake ran and `recovering`
#    never cleared - every desired lane starved behind a phantom probe.
check(not re.search(
        r"recovering\"\)\]\s*and\s*state\[\"inflight\"\]\s*:", src),
      "recovery gate is not keyed on bare inflight (the wedge)")
check(re.search(r"recovery_probe\"\)\s+for\s+w\s+in\s+state\[\"inflight\"\]",
                src) is not None,
      "recovery gate tests for an actual in-flight recovery probe")

print()
if FAILURES:
    print("%d FAILURE(S)" % len(FAILURES))
    sys.exit(1)
print("all hidden-launch checks passed")
