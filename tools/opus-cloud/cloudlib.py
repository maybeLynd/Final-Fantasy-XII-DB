"""cloudlib.py - shared helpers for OPUS's cloud-session program (OPUS, 2026-10-01).

The program: docs/CLOUD_PROGRAM.md in maybeLynd/Final-Fantasy-XII-DB. These helpers keep cloud work from duplicating
anything OPUS, FABLE, ASTRA or the SWE2 (Devin) lanes are doing, and record each cloud task on the team board."""
import io, json, os, re, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
XII = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))     # XIIOnline
DBROOT = os.path.join(XII, "Database")
DB = os.path.join(DBROOT, "FFXII TZA")
KIT = os.path.join(DBROOT, "Tools", "analysis-kit", "gfz-scripts")
TEAM_PY = os.path.join(KIT, "team.py")
TEAM_JSON = os.path.join(DB, "_index", "_inbox", "TEAM.json")
INBOX = os.path.join(DB, "_index", "_inbox")
CENSUS = os.path.join(DB, "_index", "candidates", "overlay-drop-census-2026-09-25.tsv")
GHDB = os.path.normpath(os.path.join(XII, "..", "Final-Fantasy-XII-DB"))      # the GitHub snapshot checkout
GHRE = os.path.normpath(os.path.join(XII, "..", "Final-Fantasy-XII-RE"))
OPEN = ("READY", "ACTIVE", "BLOCKED", "PENDING", "CLAIMED")


def tasks():
    t = json.load(io.open(TEAM_JSON, encoding="utf-8"))
    items = t if isinstance(t, list) else t.get("tasks", t.get("items", []))
    return list(items.values()) if isinstance(items, dict) else items


def owner(task):
    for k in ("claimed_by", "agent", "assigned_to", "owner"):
        v = task.get(k)
        if v:
            return str(v)
    return ""


def board_apply(op):
    """Apply one team.py op as OPUS; returns the interesting output lines. The op file is temporary and removed."""
    fd, p = tempfile.mkstemp(suffix=".json", dir=HERE)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(op, f)
    try:
        r = subprocess.run([sys.executable, "-B", TEAM_PY, "apply", "--agent", "OPUS", "--file", p], capture_output=True,
                           text=True, cwd=DBROOT)
    finally:
        os.remove(p)
    out = (r.stdout + r.stderr).strip().splitlines()
    keep = [l for l in out if re.search(r"Saved revision|error|refus|only|missing|not ", l, re.I)][:4]
    if r.returncode and not keep:
        keep = ["FAILED rc=%d: %s" % (r.returncode, " / ".join(out[-3:]))]
    return keep


def git(*args, cwd=XII):
    return subprocess.run(["git", "-C", cwd] + list(args), capture_output=True, text=True, encoding="utf-8",
                          errors="replace").stdout


def dirty_paths():
    """Database-relative paths ('FFXII TZA/...') that are modified or untracked in XIIOnline's working tree."""
    out = set()
    for l in git("status", "--porcelain", "-z", "--", "Database").split("\0"):
        if len(l) > 3 and l[2] == " ":
            p = l[3:]
            if p.startswith("Database/"):
                out.add(p[len("Database/"):])
    return out


def recent_peer_commits(path_db_rel, hours=72):
    """Commits in the last `hours` touching the path whose subject is not OPUS's own (subject not starting 'OPUS')."""
    log = git("log", "--since=%d.hours" % hours, "--format=%h\t%s", "--", "Database/" + path_db_rel)
    return [l for l in log.splitlines() if l and not l.split("\t", 1)[1].startswith("OPUS")]


def carriers():
    try:
        return io.open(CENSUS, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def inbox_mentions(needle):
    """Inbox files other than OPUS.md / TEAM.json that mention needle (FABLE, ASTRA, ASTRA-QUEUE, SWE2-*)."""
    hits = []
    for f in os.listdir(INBOX):
        if not f.endswith(".md") or f in ("OPUS.md",):
            continue
        try:
            t = io.open(os.path.join(INBOX, f), encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        if needle in t:
            hits.append(f)
    return hits


def stamp():
    return time.strftime("%Y-%m-%d %H:%M", time.localtime())
