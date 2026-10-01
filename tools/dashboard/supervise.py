"""supervise.py - keep the dashboard server running and on the current code (OPUS, 2026-09-30, at the user's request).

    python supervise.py --root <dashboard generation root> [--port 8765] [--interval 2]

Runs `server.py` as a child and watches the code it loads: every non-test `.py` beside this file, plus
`analysis-kit/gfz-scripts/generation.py`. When any of them changes (sha256, so an edit that keeps size and mtime still
counts), the change must hold still for one interval, and every changed file must compile. Then the child is stopped and
a fresh one is started on the new code. A change that does not compile leaves the running server up and is logged, so a
half-saved edit never takes the page down. A child that exits by itself is restarted, with a back-off while it keeps
failing (for example a port still held by another process).

REFRESH (user request 2026-09-30: "refresh every 5 seconds"). Every --refresh seconds (default 5; 0 turns it off) the
supervisor asks `generation.py status <root>` whether CURRENT still matches its inputs, and when it does not - and no build
is already running (its own, or the fleet controller's `building.json`) - it runs `build_views.py` for a new generation.
A full build takes about 45 s, so the page is at most one build behind the database. `<root>/refresher.json` is the
refresher's heartbeat, which the server shows instead of the controller's 30-minute countdown while it is fresh.
RETENTION: a generation is ~100 MB, so the refresher deletes only generations IT built (listed in
`<root>/refresher-built.txt`), keeping CURRENT, the newest 30, the first of every hour, and any generation named by an
export ZIP in `Tools/work/dashboard-exports`. Generations it did not build are never touched.

One supervisor per root: its pid is written to `<root>/supervisor.pid`, and a second start while that process is alive
exits at once. STOP-DASHBOARD.cmd ends the supervisor's process tree before the listener.
"""
import argparse, glob, hashlib, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.abspath(os.path.join(HERE, "..", "analysis-kit", "gfz-scripts", "generation.py"))


def watched():
    return sorted([p for p in glob.glob(os.path.join(HERE, "*.py"))
                   if not os.path.basename(p).startswith("test_") and os.path.basename(p) != "supervise.py"] + [GEN])


def fingerprint(paths):
    out = {}
    for p in paths:
        try:
            with open(p, "rb") as f:
                out[p] = hashlib.sha256(f.read()).hexdigest()
        except OSError:
            out[p] = None
    return out


def log(msg):
    print("%s supervise: %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), msg), flush=True)


def alive(pid):
    if sys.platform == "win32":
        r = subprocess.run(["tasklist", "/FI", "PID eq %d" % pid, "/NH"], capture_output=True, text=True, creationflags=NO_WINDOW)
        return str(pid) in r.stdout
    try:
        os.kill(pid, 0); return True
    except OSError:
        return False


def compiles(paths):
    bad = []
    for p in paths:
        try:
            compile(open(p, "rb").read(), p, "exec")
        except (SyntaxError, ValueError, OSError) as e:
            bad.append("%s: %s" % (os.path.basename(p), e))
    return bad


GENPY = GEN
EXPORTS = os.path.abspath(os.path.join(HERE, "..", "work", "dashboard-exports"))
KEEP_NEWEST = 30


NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)   # children never open a console window (OPUS, 2026-10-01)


def write_json(path, obj):
    import json
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f)
    # Windows refuses to replace a file another process has open (the server reads refresher.json): retry briefly
    # instead of failing the refresher step (the "[WinError 5] Access is denied" lines in server.log).
    for attempt in range(20):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            if attempt == 19:
                raise
            time.sleep(0.1)


def generation_state(root):
    """First word of `generation.py status`: CURRENT, STALE, INVALID, ... ('ERROR' when it cannot run)."""
    try:
        r = subprocess.run([sys.executable, "-B", GENPY, "status", root], capture_output=True, text=True, timeout=60, creationflags=NO_WINDOW)
        return (r.stdout.split() or ["ERROR"])[0]
    except (OSError, subprocess.TimeoutExpired):
        return "ERROR"


def controller_building(root):
    import json
    try:
        b = json.load(open(os.path.join(root, "building.json"), encoding="utf-8"))
        return time.time() - b.get("started", 0) < 900
    except (OSError, ValueError):
        return False


def prune(root):
    """Delete refresher-built generations beyond the retention rule; never anything the refresher did not build."""
    import json, shutil
    lst = os.path.join(root, "refresher-built.txt")
    try:
        mine = [l.strip() for l in open(lst, encoding="utf-8") if l.strip()]
    except OSError:
        return 0
    try:
        cur = json.load(open(os.path.join(root, "CURRENT"), encoding="utf-8")).get("generation")
    except (OSError, ValueError):
        return 0                                  # no readable CURRENT: delete nothing
    exported = set()
    if os.path.isdir(EXPORTS):
        exported = {os.path.splitext(n)[0] for n in os.listdir(EXPORTS) if n.endswith(".zip")}
    present = sorted(g for g in mine if os.path.isdir(os.path.join(root, g)))
    keep = set(present[-KEEP_NEWEST:]) | {cur} | exported
    hours = {}
    for g in present:                             # ids are g<YYYYMMDD>T<HHMMSS>Z-...: the first of each hour stays
        hours.setdefault(g[1:12], g)
    keep |= set(hours.values())
    gone = 0
    for g in present:
        if g not in keep:
            shutil.rmtree(os.path.join(root, g), ignore_errors=True)
            gone += 1
    left = [g for g in mine if os.path.isdir(os.path.join(root, g))]
    with open(lst + ".tmp", "w", encoding="utf-8") as f:
        f.write("\n".join(left) + ("\n" if left else ""))
    os.replace(lst + ".tmp", lst)
    return gone


class Refresher:
    def __init__(self, root, interval):
        self.root, self.interval = root, interval
        self.proc, self.next_check, self.started = None, 0.0, None
        self.hb = {"interval": interval, "checked_at": None, "state": None, "last_build_started": None,
                   "last_build_ended": None, "last_rc": None, "last_generation": None, "pruned": 0}

    def step(self):
        import json
        now = time.time()
        self.hb["alive_at"] = now                       # the heartbeat also covers the time a build is running
        if self.proc is not None:
            if self.proc.poll() is None:
                self.hb["building"] = True
                write_json(os.path.join(self.root, "refresher.json"), self.hb)
                return
            self.hb["building"] = False
            rc = self.proc.returncode; self.proc = None
            self.hb.update(last_build_ended=now, last_rc=rc)
            if rc == 0:
                try:
                    g = json.load(open(os.path.join(self.root, "CURRENT"), encoding="utf-8")).get("generation")
                except (OSError, ValueError):
                    g = None
                if g and g != self.hb.get("last_generation"):
                    with open(os.path.join(self.root, "refresher-built.txt"), "a", encoding="utf-8") as f:
                        f.write(g + "\n")
                    self.hb["last_generation"] = g
                self.hb["pruned"] += prune(self.root)
            else:
                log("refresh build exited %s; the last good generation stays displayed" % rc)
        if now < self.next_check:
            return
        self.next_check = now + self.interval
        st = generation_state(self.root)
        self.hb.update(checked_at=time.time(), state=st)
        if st != "CURRENT" and st != "ERROR" and not controller_building(self.root):
            self.proc = subprocess.Popen([sys.executable, "-B", os.path.join(HERE, "build_views.py"), "--root", self.root],
                                         cwd=HERE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                         creationflags=NO_WINDOW)
            self.hb["last_build_started"] = time.time()
        write_json(os.path.join(self.root, "refresher.json"), self.hb)


def start(root, port):
    cmd = [sys.executable, "-B", os.path.join(HERE, "server.py"), "--root", root, "--port", str(port)]
    p = subprocess.Popen(cmd, cwd=HERE, stdout=sys.stdout, stderr=sys.stderr, creationflags=NO_WINDOW)
    p._t0 = time.time()
    log("server started, pid %d, port %d" % (p.pid, port))
    return p


def stop(p):
    if p and p.poll() is None:
        p.terminate()
        try:
            p.wait(10)
        except subprocess.TimeoutExpired:
            p.kill(); p.wait(5)
        log("server pid %d stopped" % p.pid)


def main():
    ap = argparse.ArgumentParser(description="restart the dashboard server whenever its code changes")
    ap.add_argument("--root", required=True); ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--interval", type=float, default=2.0)
    ap.add_argument("--refresh", type=float, default=5.0, help="seconds between generation checks; 0 disables the refresher")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    pidfile = os.path.join(root, "supervisor.pid")
    try:
        old = int(open(pidfile).read().strip())
        if old != os.getpid() and alive(old):
            log("another supervisor (pid %d) already runs for %s - exiting" % (old, root)); return 0
    except (OSError, ValueError):
        pass
    open(pidfile, "w").write(str(os.getpid()))
    paths = watched(); seen = fingerprint(paths)
    child = start(root, a.port); fails = 0
    ref = Refresher(root, a.refresh) if a.refresh > 0 else None
    last_code = 0.0
    try:
        while True:
            time.sleep(min(a.interval, a.refresh) if ref else a.interval)
            if ref:
                try:
                    ref.step()
                except Exception as e:                  # the refresher never takes the server down
                    log("refresher error: %s" % e)
            if time.time() - last_code < a.interval:
                continue
            last_code = time.time()
            if child.poll() is not None:
                fails += 1
                wait = min(30, 2 ** min(fails, 5))
                log("server exited with %s; restarting in %ds" % (child.returncode, wait))
                time.sleep(wait)
                child = start(root, a.port)
                continue
            if time.time() - child._t0 > 60:
                fails = 0                               # a minute of uptime ends a failure streak
            paths = watched(); now = fingerprint(paths)
            if now == seen:
                continue
            time.sleep(a.interval)                      # let a multi-file save settle
            again = fingerprint(watched())
            if again != now:
                continue                                # still changing - look again next round
            changed = sorted(os.path.basename(p) for p in set(now) | set(seen) if now.get(p) != seen.get(p))
            bad = compiles([p for p in now if now[p] and now.get(p) != seen.get(p)])
            if bad:
                log("code changed (%s) but does not compile - keeping the running server: %s" % (", ".join(changed), "; ".join(bad)))
                seen = now
                continue
            log("code changed: %s - restarting the server" % ", ".join(changed))
            stop(child)
            child = start(root, a.port)
            seen = now
    except KeyboardInterrupt:
        pass
    finally:
        stop(child)
        try:
            if int(open(pidfile).read().strip()) == os.getpid():
                os.remove(pidfile)
        except (OSError, ValueError):
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
