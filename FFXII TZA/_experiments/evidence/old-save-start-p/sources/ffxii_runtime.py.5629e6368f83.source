#!/usr/bin/env python3
"""ffxii_runtime.py - stage 1 of the FFXII runtime research harness: lifecycle and clean state.

What was already here, and what was missing
-------------------------------------------
`runtime_probe.py` already attaches to a live `FFXII_TZA.exe`, proves the module loaded at its
preferred base, proves the read path with a known constant, and dumps a type's fields from
`_types/`. What it cannot do is **get a game running**, or say whether the process it found is a
legitimate reference for the database. Every runtime question therefore ended at *"needs the
operator to launch the game"*, and one designed experiment (`EXP-001`) sat unrun for that reason
alone.

This adds the missing half: **resolve, verify, launch, wait, observe, close** - and, above all,
**refuse to call a contaminated process a reference.**

The reference environment, and why it is not the modding install
----------------------------------------------------------------
Four copies of this build exist on this machine and they are not interchangeable:

    D:\\FFXII MP Mod\\FFXII_TestClient1..3   the MODDING clients -- dinput8 proxy + hook.ini +
                                            modules\\ (XIIOnlineNet.dll, tkmalloc, ...)
    D:\\SteamLibrary\\...\\FINAL FANTASY XII THE ZODIAC AGE   the reference

All four executables hash to the certified authority SHA-256. **The mod clients are still not valid
reference environments**, because `XIIOnlineNet.dll` writes engine state, which is exactly what
`EXP-001`'s control variables forbid. **A matching build hash is a build control, not an
environment control.**

Contamination is not always a file in the folder
------------------------------------------------
The first version of this tool checked a **blocklist** of loader DLL names, and on 2026-09-08 both
of a blocklist's failure modes fired within a day:

* **It could not see DynamoRIO.** FFXII's *Steam launch options* had been left set to
  ``drrun.exe -c dr_spawn_trace.dll -- %command%``, so every Steam launch ran the game under
  dynamic instrumentation. Nothing in the game's directory says so, and **reinstalling the game
  does not clear it** - the wrapper lives in Steam's user config.
* **It rejected a clean install.** It listed `xinput1_3.dll` as a loader; a verified reinstall
  restored exactly that file and none of the others, and Steam restores only what it ships.

So the check is now an **allowlist of shipped files** plus a reader for the app's Steam launch
options, and the *complete* live module list is recorded as evidence rather than a list of hits
against names this tool happens to know. `self-test` proves the launch-options reader still fires,
because it shipped broken once and an empty result from a broken check is indistinguishable from a
clean machine.

Four controls, all mandatory before any evidence is reported
------------------------------------------------------------
1. **Build control** - the executable's SHA-256 must equal the authority hash from `CLAUDE.md`.
2. **Environment control** - nothing unshipped in the directory, no `modules\\`, no `hook.ini`,
   and **no Steam launch-option wrapper**.
3. **Process control** - the full module list of the running process is captured; watched
   instrumentation modules are called out.
4. **Read control** - inherited from `runtime_probe`: the module must load at `ImageBase` and a
   known `.rdata` constant must read back exactly, or every address in the database is wrong for
   this process.

A harness that reports numbers from an unverified process manufactures evidence. Failing closed is
the whole design.

Usage
-----
    ffxii_runtime.py env                       resolve and verify the reference environment
    ffxii_runtime.py status                    running FFXII processes, classified clean/dirty
    ffxii_runtime.py launch [--wait-ready]     launch the reference build
    ffxii_runtime.py close                     close every reference instance, verify exit
    ffxii_runtime.py run EXP-001-....tsv       the whole loop, and write the evidence file
"""
import argparse
import ctypes
import glob
import re
import ctypes.wintypes as wt
import hashlib
import io
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runtime_probe as RP
import kit_paths as KP  # noqa: E402

ROOT = KP.ROOT
DB = os.path.join(ROOT, "Database", "FFXII TZA")
EXPERIMENTS = os.path.join(DB, "_experiments")
# Raw evidence lives with the experiment record and IS TRACKED. `Tools/work/` is gitignored,
# so writing there would satisfy "record the raw evidence location" while making the evidence
# invisible to a clone -- a provenance requirement met on paper only.
EVIDENCE = os.path.join(DB, "_experiments", "evidence")

AUTHORITY_SHA256 = ("73461d0896204b1c259c52f61aef4efbc95a2ffc"
                    "388cadb36493d5d1d89721f8")

# Candidate reference roots, most-preferred first. The mod clients are listed so that `env` can
# say WHY it rejected them rather than silently not seeing them.
CANDIDATES = [
    (r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64", "steam-vanilla"),
    (r"D:\FFXII MP Mod\FFXII_TestClient3\x64", "mod-client-3"),
    (r"D:\FFXII MP Mod\FFXII_TestClient1\x64", "mod-client-1"),
    (r"D:\FFXII MP Mod\FFXII_TestClient2\x64", "mod-client-2"),
]

# ---------------------------------------------------------------------------------------------
# What the game SHIPS, established by a verified Steam reinstall on 2026-09-08.
#
# This is an ALLOWLIST and that is the whole point. The first version of this check was a
# blocklist of loader names, and a blocklist has two failure modes which both fired within a day:
#
#   FALSE NEGATIVE - it listed `dinput8.dll`, `simpleLog.dll`, `ff12-trampoline.dll` and could not
#     see DynamoRIO at all, because `drrun.exe` does not put a file next to the executable. It
#     wraps the LAUNCH, through Steam's per-app launch options. A file check cannot detect a
#     contaminant that is not a file.
#
#   FALSE POSITIVE - it listed `xinput1_3.dll` as a loader. The reinstall restored that file and
#     restored none of the others, and Steam restores only what it ships. So `xinput1_3.dll` is
#     the game's own XInput redistributable and flagging it rejected a genuinely clean install.
#
# An allowlist inverts the failure: anything unexpected is visible by default, named or not.
SHIPPED_FILES = frozenset(x.lower() for x in (
    "CSteamworks.dll", "FFXII_TZA.exe", "FFXII_TZA_GameSetting.exe", "SettingsLoc.xml",
    "SharpDX.DXGI.dll", "SharpDX.DirectInput.dll", "SharpDX.dll", "Steamworks.NET.dll",
    "d3dcompiler_47.dll", "steam_api.dll", "steam_api64.dll", "xinput1_3.dll",
    "steam_appid.txt",
))
# The game writes these itself; they are output, not contamination. It uses TWO dump naming
# conventions -- `Dump_2026_9_8_...dmp` and `FFXII_TZA.exe.20260908_085630.dmp` -- and the second
# one rejected a genuinely clean install until `.dmp` was added here.
IGNORED_PATTERNS = ("dump_", ".log", ".modbak", ".dmp", ".txt")
# Highlighted in reports when present in a live process. NOT the definition of dirty -- the full
# module list is recorded as evidence and this only decides what gets shouted about.
WATCH_MODULES = ("xiionlinenet.dll", "00-ff12-tkmalloc.dll", "ff12-trampoline.dll",
                 "ivalice-together-autostart.dll", "simplelog.dll", "dinput8.dll",
                 "dynamorio.dll", "drrun.exe", "dr_spawn_trace.dll", "drmemorylib.dll")
STEAM_APPID = "595520"
STEAM_USERDATA = r"C:\Program Files (x86)\Steam\userdata"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def inspect_dir(d):
    """Structural cleanliness of one install directory. Facts only, no verdict wording."""
    exe = os.path.join(d, "FFXII_TZA.exe")
    r = {"dir": d, "exe": exe, "exists": os.path.isfile(exe)}
    if not r["exists"]:
        return r
    try:
        present = os.listdir(d)
    except OSError:
        present = []
    extra = []
    for n in present:
        low = n.lower()
        if low in SHIPPED_FILES or os.path.isdir(os.path.join(d, n)):
            continue
        if any(low.startswith(p) or low.endswith(p) for p in IGNORED_PATTERNS):
            continue
        extra.append(n)
    r["unexpected_files"] = sorted(extra)
    r["modules_dir"] = os.path.isdir(os.path.join(d, "modules"))
    r["hook_ini"] = os.path.isfile(os.path.join(d, "hook.ini"))
    if r["modules_dir"]:
        try:
            r["module_files"] = sorted(os.listdir(os.path.join(d, "modules")))
        except OSError:
            r["module_files"] = []
    r["launch_options"] = steam_launch_options()
    r["clean"] = not (r["unexpected_files"] or r["modules_dir"] or r["hook_ini"]
                      or r["launch_options"])
    return r


def steam_launch_options():
    """Steam's per-app launch options for FFXII, or "" if none.

    This exists because of a real incident. FFXII's launch options had been left set to

        drrun.exe -c dr_spawn_trace.dll -- %command%

    so **every Steam launch ran the game under DynamoRIO instrumentation**, and no check over the
    game's own directory could ever see it. The wrapper lives in Steam's user config, which means
    **reinstalling the game does not clear it**. Contamination is not always a file in the folder.
    """
    try:
        roots = glob.glob(os.path.join(STEAM_USERDATA, "*", "config", "localconfig.vdf"))
    except OSError:
        return ""
    for path in roots:
        try:
            t = io.open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        # Brace-matched rather than regex-matched. A regex over VDF has to guess how deeply the
        # app block is indented, and the first version guessed wrong and returned "" for a file
        # that plainly contained the wrapper -- a check whose negative meant nothing. `--self-test`
        # exists so that cannot happen silently again.
        key = '"%s"' % STEAM_APPID
        i = 0
        while True:
            i = t.find(key, i)
            if i < 0:
                break
            j = t.find("{", i)
            if j < 0 or t[i + len(key):j].strip():      # must be `"id"` then `{`
                i += len(key)
                continue
            depth, k = 1, j + 1
            while k < len(t) and depth:
                if t[k] == "{":
                    depth += 1
                elif t[k] == "}":
                    depth -= 1
                k += 1
            block = t[j + 1:k - 1]
            lo = re.search(r'"LaunchOptions"\s+"(.*)"', block)
            if lo and lo.group(1).strip():
                return lo.group(1)
            i = k
    return ""


def resolve_environment(want_hash=True):
    """The first candidate that is structurally clean AND hashes to the authority build."""
    report = []
    chosen = None
    for d, label in CANDIDATES:
        r = inspect_dir(d)
        r["label"] = label
        if r["exists"] and want_hash:
            r["sha256"] = sha256(r["exe"])
            r["build_ok"] = (r["sha256"] == AUTHORITY_SHA256)
        report.append(r)
        if chosen is None and r["exists"] and r.get("clean") and r.get("build_ok", True):
            chosen = r
    return chosen, report


# --- process lifecycle ----------------------------------------------------------------------

def list_processes():
    """Every live FFXII_TZA.exe with its image path.

    `runtime_probe.find_process` already does this, and using it keeps ONE definition of what
    counts as the game -- a second enumerator that disagreed about, say, the GameSetting launcher
    would let this harness verify one process and read another.
    """
    return [{"pid": pid, "path": path} for pid, path in RP.find_process("FFXII_TZA")
            if os.path.basename(path).lower() == "ffxii_tza.exe"]


def live_modules(pid, attempts=12, pause=0.5):
    """Loaded module file names, lower-cased. A clean directory does not prove a clean process.

    **Retried, because the snapshot legitimately fails while a process is still loading.**
    `CreateToolhelp32Snapshot(TH32CS_SNAPMODULE)` returns `ERROR_BAD_LENGTH` when the target's
    module list changes underneath it, and Microsoft's documented remedy is to try again. The
    first version did not, and aborted a whole experiment run on a transient with
    ``process 15048 is unreadable``.

    Refusing to report was the right response to *"I cannot see the modules"*; the defect was
    calling a transient a permanent. Still returns None after `attempts`, and the caller still
    refuses - failing closed is not what changed.
    """
    TH32CS_SNAPMODULE = 0x00000008 | 0x00000010

    class MENTRY(ctypes.Structure):
        _fields_ = [("dwSize", wt.DWORD), ("th32ModuleID", wt.DWORD), ("th32ProcessID", wt.DWORD),
                    ("GlblcntUsage", wt.DWORD), ("ProccntUsage", wt.DWORD),
                    ("modBaseAddr", ctypes.POINTER(ctypes.c_byte)), ("modBaseSize", wt.DWORD),
                    ("hModule", wt.HMODULE), ("szModule", ctypes.c_char * 256),
                    ("szExePath", ctypes.c_char * 260)]

    k = ctypes.windll.kernel32
    for _ in range(attempts):
        snap = k.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, pid)
        if snap == -1 or snap == 0xFFFFFFFFFFFFFFFF:
            time.sleep(pause)
            continue
        m = MENTRY()
        m.dwSize = ctypes.sizeof(MENTRY)
        names = []
        if k.Module32First(snap, ctypes.byref(m)):
            while True:
                names.append(m.szExePath.decode("mbcs", "replace").lower())
                if not k.Module32Next(snap, ctypes.byref(m)):
                    break
        k.CloseHandle(snap)
        # An empty list is also a failed snapshot: a live process always has its own image and
        # ntdll. Treating [] as "clean" would be the worst possible reading of a broken check.
        if names:
            return names
        time.sleep(pause)
    return None


def classify(pid):
    """(verdict, watched-hits, full module list).

    The full list is returned and recorded, not just the hits. The previous version returned only
    blocklist matches, which meant that after the DynamoRIO incident the question *"was that run
    instrumented?"* was **unanswerable from the evidence file** -- the harness had recorded the
    absence of names it happened to know rather than what was actually loaded.
    """
    mods = live_modules(pid)
    if mods is None:
        return "unreadable", [], []
    hits = [m for m in mods if is_injected(m)]
    return ("contaminated" if hits else "clean"), hits, mods


def is_injected(path):
    """Is this module instrumentation, or is it the platform / the game itself?

    Matching a BASE NAME is not enough, and this fired on the very first clean process it saw:
    the game loads **System32's** `dinput8.dll` legitimately (it ships SharpDX.DirectInput), and
    `dinput8.dll` is also the name the FFXII mod stack proxies. Same name, opposite meaning --
    the path is what separates them. Full paths are now recorded for exactly this reason.
    """
    low = path.lower()
    import ntpath
    if r"\windows\system32" in low or r"\windows\syswow64" in low:
        return False
    if "\final fantasy xii the zodiac age\\" in low:
        return False
    return ntpath.basename(low) in WATCH_MODULES


def launch(env, timeout, ready_addr=None):
    """Start the reference build and wait until it is a usable subject.

    Readiness is not "the window appeared" -- it is **the harness's own controls passing**: the
    module at its preferred base and the known constant reading back. Optionally also a pointer
    the experiment needs, so that the wait ends when the DATA is there rather than after a guess
    at how long a title screen takes.
    """
    before = set(p["pid"] for p in list_processes())
    subprocess.Popen([env["exe"]], cwd=env["dir"], close_fds=True)
    t0 = time.time()
    pid = None
    while time.time() - t0 < timeout:
        new = [p for p in list_processes() if p["pid"] not in before]
        if new:
            pid = new[0]["pid"]
            break
        time.sleep(0.25)
    if pid is None:
        return None, "no new FFXII_TZA.exe appeared within %ds" % timeout

    # Readiness is `runtime_probe --attach` succeeding: module at its preferred base AND the
    # known .rdata constant reading back. Asking the probe rather than re-deriving it means the
    # harness cannot drift from the tool that will do the actual reading.
    while time.time() - t0 < timeout:
        if probe(["--attach"]).returncode == 0:
            if ready_addr is None:
                return settle_restart(pid, timeout), None
            # ...and, when the experiment names one, until the singleton it needs is constructed.
            r = probe(["--read", "0x%08X" % ready_addr, "--size", "8"])
            if r.returncode == 0 and r.stdout.strip().split()[-1] != "0" * 16:
                return settle_restart(pid, timeout), None
        time.sleep(1.0)
    return pid, "process %d started but never became ready within %ds" % (pid, timeout)


def settle_restart(pid, timeout, quiet=6.0):
    """The process we launched is not necessarily the process that runs the game.

    FFXII restarts itself through Steam: the launched process reaches readiness, exits, and Steam
    starts a second one. The harness spent six recorded "crashes" watching the FIRST process die --
    which is what it is supposed to do. `EO-2` was that, plus a blocklist that could not tell
    System32's `dinput8.dll` from the mod stack's.

    So after readiness, wait `quiet` seconds; if the process is gone, adopt whichever FFXII process
    is alive instead. Returns the pid to actually observe.
    """
    t = time.time()
    while time.time() - t < quiet:
        time.sleep(0.5)
        if any(p["pid"] == pid for p in list_processes()):
            continue
        # it exited -- Steam should be bringing up its replacement
        deadline = time.time() + min(60.0, timeout)
        while time.time() < deadline:
            others = [p["pid"] for p in list_processes() if p["pid"] != pid]
            if others:
                print("  the launched process exited; adopting pid %d "
                      "(the game restarts itself through Steam)" % others[0])
                return others[0]
            time.sleep(1.0)
        return pid
    return pid


def probe(args):
    """Run runtime_probe.py. It is the single authority on reading this process."""
    return subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                        "runtime_probe.py")] + args,
                          capture_output=True, text=True)


def close_all(timeout=30):
    """Ask nicely, then insist. Returns the pids that actually exited."""
    pids = [p["pid"] for p in list_processes()]
    if not pids:
        return [], []
    for pid in pids:
        subprocess.run(["taskkill", "/PID", str(pid)], capture_output=True)
    t0 = time.time()
    while time.time() - t0 < timeout:
        still = set(p["pid"] for p in list_processes())
        if not (still & set(pids)):
            return pids, []
        time.sleep(0.5)
    still = [p for p in pids if p in set(x["pid"] for x in list_processes())]
    for pid in still:
        subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)
    time.sleep(1.0)
    left = [p for p in still if p in set(x["pid"] for x in list_processes())]
    return [p for p in pids if p not in left], left


# --- commands -------------------------------------------------------------------------------

def cmd_env(a):
    chosen, report = resolve_environment()
    for r in report:
        if not r["exists"]:
            print("  %-14s MISSING            %s" % (r["label"], r["dir"]))
            continue
        why = []
        if r["unexpected_files"]:
            why.append("unshipped file(s): " + ",".join(r["unexpected_files"][:6]))
        if r["modules_dir"]:
            why.append("modules/ (%d file(s))" % len(r.get("module_files", [])))
        if r["hook_ini"]:
            why.append("hook.ini")
        if r.get("launch_options"):
            why.append("STEAM LAUNCH OPTIONS SET: %s" % r["launch_options"][:90])
        if not r.get("build_ok", False):
            why.append("BUILD MISMATCH %s" % r.get("sha256", "?")[:16])
        print("  %-14s %-12s %s" % (r["label"], "CLEAN" if not why else "rejected",
                                    r["dir"] if not why else "; ".join(why)))
    print()
    if chosen is None:
        print("NO CLEAN REFERENCE ENVIRONMENT. Refusing to nominate a contaminated one.")
        return 1
    print("reference: %s" % chosen["exe"])
    print("build    : %s  (authority match)" % chosen["sha256"])
    return 0


def cmd_status(a):
    procs = list_processes()
    if not procs:
        print("no FFXII_TZA.exe running")
        return 0
    for p in procs:
        state, hits, mods = classify(p["pid"])
        print("  pid %-6d %-13s %s" % (p["pid"], state, p["path"]))
        if hits:
            print("           injected: %s" % ", ".join(hits))
    return 0


def cmd_launch(a):
    chosen, _ = resolve_environment()
    if chosen is None:
        print("no clean reference environment; refusing to launch")
        return 1
    pid, err = launch(chosen, a.timeout, num_or_none(a.ready_ptr))
    if pid:
        state, hits, mods = classify(pid)
        print("pid %d  %s%s" % (pid, state, ("  injected: " + ",".join(hits)) if hits else ""))
    if err:
        print("NOT READY: %s" % err)
        return 1
    print("ready: controls pass")
    return 0


def cmd_close(a):
    gone, left = close_all()
    print("exited: %s" % (", ".join(str(p) for p in gone) or "none"))
    if left:
        print("STILL RUNNING: %s" % ", ".join(str(p) for p in left))
        return 1
    return 0


def num_or_none(x):
    if not x:
        return None
    return int(x, 16) if str(x).lower().startswith("0x") else int(x)


def cmd_run(a):
    """The loop: verify -> launch -> wait -> observe -> record -> close."""
    started = time.strftime("%Y-%m-%dT%H:%M:%S")
    chosen, _ = resolve_environment()
    if chosen is None:
        print("no clean reference environment; refusing to run an experiment")
        return 1

    launched_here = False
    procs = list_processes()
    clean = [p for p in procs if classify(p["pid"])[0] == "clean"]
    if clean:
        pid = clean[0]["pid"]
        ready_at = time.time()
        print("attaching to existing clean pid %d" % pid)
    else:
        if procs:
            print("%d running instance(s), none clean; refusing to reuse a contaminated process"
                  % len(procs))
            for p in procs:
                print("   pid %d  %s" % (p["pid"], classify(p["pid"])[1]))
            return 1
        print("launching %s" % chosen["exe"])
        pid, err = launch(chosen, a.timeout, num_or_none(a.ready_ptr))
        launched_here = True
        if err:
            print("NOT READY: %s" % err)
            if not a.keep:
                close_all()
            return 1
        ready_at = time.time()
        print("pid %d ready" % pid)

    state, hits, mods = classify(pid)
    if state != "clean":
        # "unreadable ()" was the message for a process that had simply DIED between reaching
        # readiness and being classified -- true but useless, and it reads like a permissions
        # problem. A harness that refuses must say which thing it could not establish.
        alive = any(p["pid"] == pid for p in list_processes())
        if state == "unreadable" and not alive:
            print("process %d reached readiness and then EXITED before it could be classified; "
                  "no evidence is reported" % pid)
        else:
            print("process %d is %s%s; refusing to report evidence"
                  % (pid, state, (" (" + ",".join(hits) + ")") if hits else
                     " - the module list could not be read while it is still running"))
        if launched_here and not a.keep:
            close_all()
        return 1

    tsv = a.experiment
    if not os.path.isabs(tsv):
        tsv = os.path.join(EXPERIMENTS, tsv)

    # Readiness says the object EXISTS. It does not say every value that will ever be written to
    # it has been. A single observation taken at the first readable instant cannot distinguish
    # "the database's claim is wrong" from "we looked before the writer ran" -- and the first run
    # of EXP-001 produced exactly that ambiguity. So: settle, and repeat, and record both.
    passes = []
    for i in range(max(1, a.repeat)):
        if a.settle and (i == 0 or a.settle_each):
            time.sleep(a.settle)
        elif i:
            time.sleep(a.interval)
        obs = observe(tsv)
        obs["at_seconds_after_ready"] = round(time.time() - ready_at, 1)
        passes.append(obs)
    obs = passes[-1]

    os.makedirs(EVIDENCE, exist_ok=True)
    stem = os.path.splitext(os.path.basename(tsv))[0]
    out = os.path.join(EVIDENCE, "%s-%s.json" % (stem, time.strftime("%Y%m%dT%H%M%S")))
    record = {
        "experiment": stem,
        "started": started,
        "finished": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "harness": os.path.basename(__file__),
        "reference_exe": chosen["exe"],
        "reference_sha256": chosen["sha256"],
        "authority_sha256": AUTHORITY_SHA256,
        "environment": {"unexpected_files": chosen["unexpected_files"],
                        "modules_dir": chosen["modules_dir"],
                        "hook_ini": chosen["hook_ini"],
                        "steam_launch_options": chosen["launch_options"]},
        "pid": pid,
        "state_establishment": ("launched by this harness, no input automation, "
                                "observed at the first frame where the controls pass")
        if launched_here else "attached to an already-running clean process",
        "live_modules_watched_hits": hits,
        "live_modules": sorted(mods),
        "settle_seconds": a.settle,
        "passes": passes,
        "observation": obs,
    }
    io.open(out, "w", encoding="utf-8", newline="\n").write(
        json.dumps(record, indent=2) + "\n")

    for i, o in enumerate(passes):
        print("--- pass %d, %.1fs after ready" % (i + 1, o["at_seconds_after_ready"]))
        print(o["stdout"].rstrip())
        if o["stderr"].strip():
            print(o["stderr"].rstrip())
    print()
    print("evidence: %s" % out)
    if launched_here and not a.keep:
        gone, left = close_all()
        print("closed: %s%s" % (", ".join(str(p) for p in gone) or "none",
                                ("  STILL RUNNING " + ",".join(str(p) for p in left))
                                if left else ""))
    return 0


def observe(tsv):
    """Run the experiment through runtime_probe --check and keep its output verbatim.

    Deliberately NOT reimplemented here. `runtime_probe` already owns the address-expression
    grammar, the type decoding and -- most importantly -- the two mandatory controls and the
    refusal semantics. A second implementation would be a second place for those to be subtly
    wrong, and the whole point of a control is that it is the same one every time.
    """
    r = probe(["--check", tsv])
    return {"argv": ["runtime_probe.py", "--check", os.path.basename(tsv)],
            "returncode": r.returncode,
            "stdout": r.stdout,
            "stderr": r.stderr}


def _eq(val, want):
    try:
        return int(val) == int(want)
    except (TypeError, ValueError):
        return str(val) == str(want)


def cmd_selftest(a):
    """Prove the environment checks still FIRE. A negative from a broken check is worthless.

    The launch-options reader shipped broken for one iteration: it returned "" for a file that
    plainly contained the DynamoRIO wrapper, because a regex over VDF has to guess the indent
    depth. On the live machine that empty string is indistinguishable from "no wrapper set" --
    which is the exact shape of failure this project keeps finding in its own instruments.
    """
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp(prefix="ffxii-selftest")
    d = os.path.join(tmp, "85625008", "config")
    os.makedirs(d)
    lo = ('\t\t\t"LaunchOptions"\t\t"\\"C:\\\\drrun.exe\\" -c '
          '\\"C:\\\\dr_spawn_trace.dll\\" -- %command%"\n')
    body = ('"apps"\n\t{\n'
            '\t\t"1963040"\n\t\t{\n\t\t\t"Playtime"\t\t"545"\n\t\t}\n'
            '\t\t"595520"\n\t\t{\n\t\t\t"LastPlayed"\t\t"1788875309"\n' + lo +
            '\t\t\t"cloud"\n\t\t\t{\n\t\t\t\t"last_sync_state"\t\t"synchronized"\n'
            '\t\t\t}\n\t\t}\n'
            '\t\t"2767030"\n\t\t{\n\t\t\t"Playtime"\t\t"1"\n\t\t}\n\t}\n')
    p = os.path.join(d, "localconfig.vdf")
    global STEAM_USERDATA
    real = STEAM_USERDATA
    STEAM_USERDATA = tmp
    ok = True
    try:
        cases = [
            ("wrapper present, nested block after it", body, True),
            ("no LaunchOptions key", body.replace(lo, ""), False),
            ("wrapper on a different app only",
             body.replace('"595520"', '"9999999"', 1), False),
            ("LaunchOptions present but empty",
             body.replace(lo, '\t\t\t"LaunchOptions"\t\t""\n'), False),
        ]
        for name, text, expect in cases:
            io.open(p, "w", encoding="utf-8", newline=chr(10)).write(text)
            got = bool(steam_launch_options())
            good = (got == expect)
            ok = ok and good
            print("  %-42s expect %-5s got %-5s %s"
                  % (name, expect, got, "PASS" if good else "FAIL"))
    finally:
        STEAM_USERDATA = real
        shutil.rmtree(tmp, ignore_errors=True)
    print()
    print("allowlist: %d shipped names; anything else in the directory is reported by default"
          % len(SHIPPED_FILES))
    print("self-test %s" % ("ok" if ok else "FAILED - the launch-options check is not firing"))
    return 0 if ok else 1


# ---------------------------------------------------------------------------------------------
# Observables that say WHERE the game is.
#
# Every one of these was baselined at the title screen on 2026-09-08 (EXP-002, EXP-003), so a
# reading that differs from the baseline is a state change rather than a guess. The entity free
# list is the sharpest: with no map loaded all 128 records are chained head-to-tail, and a map
# cannot place anything without taking slots off that list.
ENTITY_TABLE = 0x0215FDA0
ENTITY_SLOTS = 128
ENTITY_STRIDE = 64
ST2E_TABLE = 0x02F973C0
SAVE_BUFFER = 0x02164280          # SaveImage_GetActiveBuffer's target
PAYLOAD_AREA_ID = SAVE_BUFFER + 0x200 + 0x1044
SETTINGS_PTR = 0x01F82D20

TITLE_BASELINE = {"free_slots": 128, "st2e_groups": 16}
# Observed at the main menu (New Game / Load Game / Trial Mode / Credits / Exit) on a cold
# launch, and unchanged while the cursor moved and while the Load screen listed six saves --
# so it identifies the FRONT-END, not a screen within it. EW-1.
MENU_AREA_ID = 12


def read_bytes(va, n):
    """Read through runtime_probe, so the controls run and a bad read cannot be mistaken for data."""
    r = probe(["--read", "0x%08X" % va, "--size", str(n)])
    if r.returncode != 0:
        return None
    parts = r.stdout.strip().split()
    if not parts:
        return None
    try:
        return bytes.fromhex(parts[-1])
    except ValueError:
        return None


def observe_state():
    """A dict of observables, or None if the process is not readable."""
    import struct
    out = {}
    b = read_bytes(ENTITY_TABLE, ENTITY_SLOTS * ENTITY_STRIDE)
    if b is None:
        return None
    recs = [b[i * ENTITY_STRIDE:(i + 1) * ENTITY_STRIDE] for i in range(ENTITY_SLOTS)]
    # A record is ON THE FREE LIST if it has a next or a prev. The head has no prev and the tail
    # has no next, so "both null" means detached -- i.e. handed out.
    linked = 0
    for r in recs:
        prev = struct.unpack_from("<Q", r, 0)[0]
        nxt = struct.unpack_from("<Q", r, 8)[0]
        if prev or nxt:
            linked += 1
    out["free_slots"] = linked
    out["entity_slots"] = ENTITY_SLOTS

    t = read_bytes(ST2E_TABLE, 224)
    if t:
        q = struct.unpack("<28Q", t)
        out["st2e_groups"] = sum(1 for v in q if v)
        out["st2e_which"] = [i for i, v in enumerate(q) if v]

    a = read_bytes(PAYLOAD_AREA_ID, 4)
    if a:
        out["area_id"] = struct.unpack("<i", a)[0]
    sb = read_bytes(SAVE_BUFFER, 16)
    if sb:
        out["save_buffer_head"] = sb.hex()
    return out


def state_verdict(st):
    """in-world | menu | unknown -- and never a guess dressed as a fact.

    CORRECTED 2026-09-08 (EW-1). This used to answer "title" whenever all 128 script-entity
    slots were on the free list, and it said TITLE while **Vaan was standing in Dalmasca
    Estersand with a save loaded** -- photographed. Two separate errors:

      1. `0215FDA0` is the SCRIPT VM's entity-name table, not a general entity table. Nothing
         puts a slot on it merely because the world has bodies in it.
      2. "on the free list" and "has content" are INDEPENDENT. With a map loaded every one of
         the 128 records carries a populated body AND is still linked into the free list.

    So the free list is reported as what it is -- a fact about the script table -- and the
    verdict is taken from the two observables that actually moved when a save loaded: the save
    buffer filled, and the area id left its menu value.

    **No verdict here identifies a SCREEN.** `window_capture.py` does that, and it is the only
    thing that can: a menu and a field share every number this function reads.
    """
    if st is None:
        return "unknown", "the process is not readable"
    sb = st.get("save_buffer_head") or ""
    loaded = bool(sb) and set(sb) != {"0"}
    area = st.get("area_id")
    if loaded and area not in (None, MENU_AREA_ID):
        return "in-world", ("a save is loaded and the area id is %s, not the menu's %d"
                            % (area, MENU_AREA_ID))
    if not loaded and area == MENU_AREA_ID:
        return "menu", ("save buffer empty and area id %d -- the front-end. WHICH menu screen "
                        "is not knowable from memory alone; photograph it" % MENU_AREA_ID)
    return "unknown", ("save buffer %s, area id %s -- this combination has no baseline"
                       % ("populated" if loaded else "empty", area))


def cmd_state(a):
    procs = list_processes()
    if not procs:
        print("no FFXII_TZA.exe running")
        return 1
    pid = procs[0]["pid"]
    verdict, why = state_verdict(observe_state())
    st = observe_state()
    print("pid %d" % pid)
    print("  verdict        %s   (%s)" % (verdict.upper(), why))
    if st:
        print("  script slots   %d of %d on the free list   (a fact about the SCRIPT table, "
              "not about the world)" % (st.get("free_slots", -1), ENTITY_SLOTS))
        print("  st2e groups    %s of 28        title baseline %d"
              % (st.get("st2e_groups", "?"), TITLE_BASELINE["st2e_groups"]))
        print("  area id        %s" % st.get("area_id", "?"))
        print("  save buffer    %s" % st.get("save_buffer_head", "?"))
    print("  screen         NOT KNOWABLE FROM MEMORY -- run window_capture.py")
    return 0


# ---------------------------------------------------------------------------------------------
# ET-1: snapshot and diff.
#
# `state` can tell "title" from "a map is loaded" and nothing in between, so an input attempt that
# failed could not be told from one that never arrived. This is the instrument that makes the
# difference visible: capture memory, do a thing, capture again, and report what moved.
#
# The regions are the writable data the database actually knows about. `.data`'s file-backed part
# is included because a diff that covers only BSS cannot see a static being written; the BSS spans
# are where every runtime table this project has found so far lives.
SNAPSHOT_REGIONS = [
    ("data",      0x01DF0000, 0x01F80000 - 0x01DF0000),   # file-backed .data
    ("bss_low",   0x01F80000, 0x02200000 - 0x01F80000),   # settings ptr, save buffer, entity table
    ("bss_mid",   0x02200000, 0x02400000 - 0x02200000),   # the shared workbench lives here
    ("bss_high",  0x02E00000, 0x03000000 - 0x02E00000),   # the st2e group tables
]
SNAPSHOT_DIR = os.path.join(ROOT, "Database", "Tools", "work", "runtime", "snapshots")


def cmd_snapshot(a):
    procs = list_processes()
    if not procs:
        print("no FFXII_TZA.exe running")
        return 1
    pid = procs[0]["pid"]
    state, hits, mods = classify(pid)
    if state != "clean":
        print("process %d is %s; refusing to snapshot an unverified process" % (pid, state))
        return 1
    d = os.path.join(SNAPSHOT_DIR, a.name)
    os.makedirs(d, exist_ok=True)
    meta = {"pid": pid, "taken": time.strftime("%Y-%m-%dT%H:%M:%S"), "regions": [],
            "state": observe_state()}
    total = holes = 0
    for name, va, size in SNAPSHOT_REGIONS:
        path = os.path.join(d, "%s.bin" % name)
        r = probe(["--read", "0x%08X" % va, "--size", str(size), "--dump", path])
        if r.returncode != 0:
            print("  %-9s FAILED" % name)
            continue
        # "VA..VA  N byte(s) written, H unreadable page(s)"
        # The dump line is the LAST line -- the two control lines come first, and splitting the
        # whole of stdout picked a word out of "CONTROL 1 base match".
        try:
            parts = r.stdout.strip().splitlines()[-1].split()
            got = int(parts[1].replace(",", ""))
            hole = int(parts[4])
        except (IndexError, ValueError):
            got, hole = -1, -1
        total += max(got, 0)
        holes += max(hole, 0)
        meta["regions"].append({"name": name, "va": "0x%08X" % va, "size": size,
                                "bytes_read": got, "unreadable_pages": hole})
        print("  %-9s 0x%08X + 0x%-8X  %10d bytes, %d hole(s)" % (name, va, size, got, hole))
    io.open(os.path.join(d, "manifest.json"), "w", encoding="utf-8", newline=chr(10)).write(
        json.dumps(meta, indent=2) + chr(10))
    print("snapshot %r: %s bytes, %d unreadable page(s)  ->  %s"
          % (a.name, "{:,}".format(total), holes, d))
    return 0


def changed_offsets(da, db, name):
    A = io.open(os.path.join(da, "%s.bin" % name), "rb").read()
    B = io.open(os.path.join(db, "%s.bin" % name), "rb").read()
    n = min(len(A), len(B))
    return set(i for i in range(n) if A[i] != B[i])


def cmd_churn(a):
    """Churn-subtracted diff: what the TEST window changed that the BASELINE window did not.

    A running game rewrites thousands of bytes a second, so a raw diff across "do a thing" proves
    nothing. This subtracts a no-input window from a test window -- and, crucially, prints the
    REVERSED comparison too, because a real effect is asymmetric and noise is not. On the first
    use, a keypress scored 319 and the reversal scored 311: symmetric, therefore noise.
    """
    root = SNAPSHOT_DIR
    def window(x):
        return tuple(os.path.join(root, n) for n in x.split(":"))
    base = window(a.baseline)
    test = window(a.test)
    for pair in (base, test):
        for d in pair:
            if not os.path.isdir(d):
                print("no snapshot named %r" % os.path.basename(d))
                return 1
    fwd = rev = 0
    print("%-9s %10s %10s %10s" % ("region", "baseline", "test", "NEW"))
    for name, _va, _sz in SNAPSHOT_REGIONS:
        b = changed_offsets(base[0], base[1], name)
        t = changed_offsets(test[0], test[1], name)
        fwd += len(t - b)
        rev += len(b - t)
        print("%-9s %10d %10d %10d" % (name, len(b), len(t), len(t - b)))
    print()
    print("NEW in test, not in baseline : %d" % fwd)
    print("NEW in baseline, not in test : %d   <- the REVERSAL" % rev)
    if rev and 0.6 <= fwd / float(rev) <= 1.7:
        print()
        print("SYMMETRIC. A real effect shows up in one direction; this shows up in both, so it is")
        print("window-to-window noise and NOT evidence that the test action did anything.")
    return 0


def cmd_diff(a):
    import struct
    da = os.path.join(SNAPSHOT_DIR, a.before)
    db = os.path.join(SNAPSHOT_DIR, a.after)
    for d in (da, db):
        if not os.path.isdir(d):
            print("no snapshot named %r" % os.path.basename(d))
            return 1
    ma = json.load(io.open(os.path.join(da, "manifest.json"), encoding="utf-8"))
    mb = json.load(io.open(os.path.join(db, "manifest.json"), encoding="utf-8"))
    if ma["pid"] != mb["pid"]:
        print("NOTE: different pids (%d vs %d) -- addresses are comparable because the module "
              "loads at its preferred base, but heap contents are not." % (ma["pid"], mb["pid"]))
    print("%s -> %s" % (ma["taken"], mb["taken"]))
    print()
    grand = 0
    for name, va, size in SNAPSHOT_REGIONS:
        pa = os.path.join(da, "%s.bin" % name)
        pb = os.path.join(db, "%s.bin" % name)
        if not (os.path.exists(pa) and os.path.exists(pb)):
            continue
        A = io.open(pa, "rb").read()
        B = io.open(pb, "rb").read()
        n = min(len(A), len(B))
        runs = []
        i = 0
        while i < n:
            if A[i] != B[i]:
                j = i
                # coalesce across gaps of up to 16 identical bytes, so one field does not
                # come out as four runs
                gap = 0
                while j < n and (A[j] != B[j] or gap < 16):
                    gap = 0 if A[j] != B[j] else gap + 1
                    j += 1
                end = j - gap
                runs.append((va + i, end - i))
                i = j
            else:
                i += 1
        changed = sum(r[1] for r in runs)
        grand += changed
        print("%-9s %6d run(s), %s byte(s) changed" % (name, len(runs), "{:,}".format(changed)))
        for start, ln in runs[:a.show]:
            off = start - va
            print("   0x%08X + %-5d  %s  ->  %s" % (start, ln,
                  A[off:off + min(ln, 12)].hex(), B[off:off + min(ln, 12)].hex()))
        if len(runs) > a.show:
            print("   ... %d more run(s)" % (len(runs) - a.show))
    print()
    print("total changed: %s byte(s)" % "{:,}".format(grand))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("env")
    sub.add_parser("status")
    for name in ("launch", "run"):
        q = sub.add_parser(name)
        q.add_argument("--timeout", type=int, default=180)
        q.add_argument("--ready-ptr", default=None,
                       help="wait until this VA holds a non-null pointer")
        if name == "run":
            q.add_argument("experiment")
            q.add_argument("--keep", action="store_true", help="leave the game running")
            q.add_argument("--settle", type=float, default=0.0,
                           help="seconds to wait after ready before observing")
            q.add_argument("--settle-each", action="store_true",
                           help="apply --settle before every pass, not only the first")
            q.add_argument("--repeat", type=int, default=1)
            q.add_argument("--interval", type=float, default=5.0,
                           help="seconds between repeated passes")
    sub.add_parser("close")
    sub.add_parser("self-test")
    sub.add_parser("state")
    q = sub.add_parser("snapshot")
    q.add_argument("name")
    q = sub.add_parser("churn")
    q.add_argument("baseline", help="two snapshot names, colon-separated: A:B")
    q.add_argument("test", help="two snapshot names, colon-separated: C:D")
    q = sub.add_parser("diff")
    q.add_argument("before")
    q.add_argument("after")
    q.add_argument("--show", type=int, default=8)
    a = ap.parse_args()
    fn = {"env": cmd_env, "status": cmd_status, "launch": cmd_launch,
          "close": cmd_close, "run": cmd_run, "self-test": cmd_selftest, "state": cmd_state, "snapshot": cmd_snapshot, "diff": cmd_diff, "churn": cmd_churn}.get(a.cmd)
    if fn is None:
        ap.print_help()
        return 2
    return fn(a)


if __name__ == "__main__":
    sys.exit(main())
