"""activity.py - which agent is working on which part of FF12 knowledge, from authoritative state only (OPUS, 2026-09-29).

Inputs, all read, none written:
  board      TEAM.json - who holds which claim (ACTIVE, agent) and who has what queued (READY, assigned_to)
  fleet      the controller's own records: the newest `poll` event of watchdog-log.jsonl (SWE2 lanes: busy-* / free) and
             watchdog-state.json `claude_lanes` (Claude lanes: ACTIVE / UNKNOWN ...)
  facts      the CURRENT generation's requirement facts + category map, to place register ids, function addresses and
             pages into the My Progress categories (the same placement the tab uses)
  packages   _index/completion-packages/PKG-*.md, whose page links place a package

LIVENESS, never inferred from a claim alone:
  active     the controller reports the lane busy (SWE2), or the Claude-lane adapter classifies it ACTIVE
  recent     no fleet feed for the lane, but the lane itself issued a board operation within RECENT_S - the board history's
             issuer, not a task's timestamp (board-evidenced; labelled as such)
  idle       the feed reports the lane free / not running
  UNKNOWN    no feed, no recent write, or the feed itself is older than FEED_STALE_S
An ACTIVE claim on an idle or UNKNOWN lane is shown as a claim with that liveness - never as active production.

KINDS of activity per category:
  working    an ACTIVE claim on a lane whose liveness is active or recent
  claimed    an ACTIVE claim on a lane that is idle or UNKNOWN (stale claim; shown muted)
  waiting    a READY review / verify / sign request queued for the lane (review-only; shown muted, outlined)
"""
import collections, datetime, json, os, re

RECENT_S = 3600
FEED_STALE_S = 900
CATEGORIES = [("W", "World & maps"), ("C", "Combat & damage"), ("E", "Enemies & AI"), ("S", "Spawning, death & respawn"),
              ("P", "Player & party"), ("I", "Items, equipment & progression"), ("T", "Story, quests & events"),
              ("M", "Menus & controls"), ("G", "Animation, graphics & audio"), ("V", "Save/load & persistence"),
              ("D", "Scripts & game data/VBF"), ("N", "Engine & supporting systems"),
              ("whole", "Whole database / cross-cutting"), ("untied", "Code not yet tied to a game system")]
# Stable legend: (light-theme, dark-theme) text colors chosen for >= 4.5:1 contrast on their backgrounds, all distinct.
PALETTE = collections.OrderedDict([
    ("OPUS", ("#1f5fa8", "#6ea8fe")), ("FABLE", ("#7b3fb3", "#c29ffa")), ("ASTRA", ("#b3261e", "#ff8a80")),
    ("SWE2-FRONTIER", ("#1e7b34", "#6fdd8b")), ("SWE2-DATA", ("#a8530a", "#ffb366")), ("SWE2-ORACLE", ("#6b4a2f", "#d9b38c")),
    ("SWE2-STRUCT", ("#b0306e", "#ff8cc6")), ("SWE2-EC7", ("#0e7c86", "#5fdbe6")), ("SWE2-CONTRACT", ("#6d6a00", "#dcd75c")),
    ("SWE2-AUDIT-SPEC", ("#3b3f99", "#a4a8ff")), ("SWE2-AUDIT-SEM", ("#8a2c2c", "#f2a5a5"))])
OVERFLOW = [("#5a6b00", "#c5dd66"), ("#00665c", "#66e0cf"), ("#7a4a00", "#f0b866"), ("#4a3c8c", "#b8aaff"), ("#8c3b5e", "#f5a3c7"),
            ("#2d5f73", "#8fd0ea")]
ALIASES = {"SOL": "ASTRA", "FRONTIER": "SWE2-FRONTIER"}
REVIEWISH = re.compile(r"REVIEW|VERIFY|SIGN|AUDIT", re.I)


def colors(lanes):
    """lane -> (light, dark): the fixed legend for known lanes; unknown lanes take overflow colors in sorted order, never a
    color already in use."""
    out = {l: PALETTE[l] for l in lanes if l in PALETTE}
    used = set(out.values())
    free = [c for c in OVERFLOW if c not in used]
    for l in sorted(x for x in lanes if x not in PALETTE):
        out[l] = free.pop(0) if free else ("#555555", "#bbbbbb")
    return out


def order(lanes):
    known = [l for l in PALETTE if l in lanes]
    return known + sorted(l for l in lanes if l not in PALETTE)


def _age(ts, now):
    try:
        return now - datetime.datetime.fromisoformat(str(ts).replace("Z", "+00:00")).timestamp()
    except (TypeError, ValueError):
        return None


def board_writes(board, now):
    """lane -> epoch of the newest board operation that lane ISSUED, from the board's own operation history (`agent` is the
    identity team.apply ran as). A task's updated_at is not used: it says when the row changed, not who changed it, so a
    review another lane queues for this one would credit this one (ASTRA 00fd54fda, REJECT of 8ddc8c7e8). No history ->
    no writes, never a guess."""
    out = collections.defaultdict(float)
    for e in board.get("history") or []:
        a = e.get("agent") if isinstance(e, dict) else None
        age = _age(e.get("at"), now) if a else None
        if age is not None:
            a = ALIASES.get(a, a)
            out[a] = max(out[a], now - age)
    return out


def liveness(lanes, board, poll, claude, now):
    """lane -> (state, basis)."""
    out = {}
    feed_age = _age((poll or {}).get("ts"), now) if poll else None
    ls = (poll or {}).get("lane_state", {})
    last_write = board_writes(board, now)
    for l in lanes:
        if l in ls:
            if feed_age is None or feed_age > FEED_STALE_S:
                out[l] = ("UNKNOWN", "controller poll is %s old" % ("?" if feed_age is None else "%d s" % feed_age))
            elif ls[l].startswith("busy"):
                out[l] = ("active", "controller: %s (poll %d s ago)" % (ls[l], feed_age))
            else:
                out[l] = ("idle", "controller: %s (poll %d s ago)" % (ls[l], feed_age))
            continue
        c = (claude or {}).get(l)
        if c:
            cls = (c.get("classification") or "").rstrip(":").upper()
            if cls == "ACTIVE":
                out[l] = ("active", "Claude-lane adapter: session running")
                continue
            if cls in ("IDLE", "PAUSED", "EXITED", "STOPPED"):
                out[l] = ("idle", "Claude-lane adapter: %s" % cls)
                continue
        w = last_write.get(l)
        if w and now - w <= RECENT_S:
            out[l] = ("recent", "no session feed; wrote the board %d min ago" % ((now - w) // 60))
        else:
            out[l] = ("UNKNOWN", "no session feed for this lane" + ("; last board write %d min ago" % ((now - w) // 60) if w else ""))
    return out


class Placer:
    """Places a task's text into the My Progress categories through the same map and facts the tab uses."""

    def __init__(self, cmap, facts, packages):
        import requirements as R
        self.R, self.cmap = R, cmap
        self.byid = {}
        for f in (facts or {}).get("facts", []):
            if f["f"] in ("Q", "F"):
                g = R.place(f, cmap)
                if g:
                    self.byid[f["k"].split(":", 1)[1]] = g
        self.pkg = packages or {}

    def groups(self, text):
        g = set()
        for code in re.findall(r"\b(\d\d)-[A-Z][A-Za-z]", text):
            g.update(self.cmap.get("folder", {}).get(code, []))
        for tok in set(re.findall(r"\b([A-Z]{1,4}-\d{1,4}[a-z]?)\b", text)):
            g.update(self.byid.get(tok, []))
        for tok in set(re.findall(r"\b(0[0-9A-F]{7})\b", text)):
            g.update(self.byid.get(tok, []))
        for p in set(re.findall(r"\b(PKG-[A-Z0-9-]+)", text)):
            g.update(self.pkg.get(p, []))
        if not g and re.search(r"dashboard|migration|workflow|_index/|goal_gate|TEAM|controller|board|transitions|generation|"
                               r"Database/Tools|gfz-scripts|prereq|seal\.py|composer|publish", text, re.I):
            g.add("whole")
        return sorted(g)


def package_groups(pkgdir, cmap):
    out = {}
    if not pkgdir or not os.path.isdir(pkgdir):
        return out
    for fn in os.listdir(pkgdir):
        if fn.startswith("PKG-") and fn.endswith(".md"):
            t = open(os.path.join(pkgdir, fn), encoding="utf-8", errors="replace").read()
            g = set()
            for code in re.findall(r"\b(\d\d)-[A-Z][A-Za-z]", t):
                g.update(cmap.get("folder", {}).get(code, []))
            out[fn[:-3]] = sorted(g)
    return out


def compute(board, poll, claude, placer, now, extra_lanes=()):
    tasks = board.get("tasks", [])
    lanes = set(extra_lanes)
    for t in tasks:
        if t.get("status") == "ACTIVE" and t.get("agent"):
            lanes.add(ALIASES.get(t["agent"], t["agent"]))
        if t.get("status") == "READY" and t.get("assigned_to"):
            lanes.add(ALIASES.get(t["assigned_to"], t["assigned_to"]))
    lanes |= set(PALETTE)
    live = liveness(lanes, board, poll, claude, now)
    items = []
    for t in tasks:
        st = t.get("status")
        if st == "ACTIVE" and t.get("agent"):
            lane = ALIASES.get(t["agent"], t["agent"])
            kind = "working" if live[lane][0] in ("active", "recent") else "claimed"
        elif st == "READY" and t.get("assigned_to") and REVIEWISH.search(t["id"]):
            lane = ALIASES.get(t["assigned_to"], t["assigned_to"])
            kind = "waiting"
        else:
            continue
        text = " ".join(str(t.get(k) or "") for k in ("id", "target", "scope", "question"))[:4000]
        items.append({"lane": lane, "kind": kind, "task": t["id"], "status": st, "priority": t.get("priority"),
                      "groups": placer.groups(text), "stage": (t.get("checkpoint") or "")[:160],
                      "updated_at": t.get("updated_at"),
                      "blocker": ", ".join(t.get("dependencies") or []) or ("queued for review" if kind == "waiting" else ""),
                      "next": (t.get("completion") or "")[:160]})
    cats = []
    for code, label in CATEGORIES:
        here = [i for i in items if code in i["groups"]]
        work = order({i["lane"] for i in here if i["kind"] == "working"})
        others = order({i["lane"] for i in here if i["kind"] != "working"} - set(work))
        cats.append({"code": code, "label": label, "working": work, "muted": others,
                     "items": sorted(here, key=lambda i: (list(PALETTE).index(i["lane"]) if i["lane"] in PALETTE else 99, i["lane"], i["task"]))})
    shown = order({i["lane"] for i in items} | set(PALETTE))
    col = colors(set(shown))
    by_agent = []
    for l in shown:
        mine = [i for i in items if i["lane"] == l]
        by_agent.append({"lane": l, "liveness": live[l][0], "basis": live[l][1], "color": col[l],
                         "working": [i for i in mine if i["kind"] in ("working", "claimed")],
                         "waiting": sorted([i for i in mine if i["kind"] == "waiting"], key=lambda i: (i["priority"] or "P9", i["task"]))[:6],
                         "waiting_count": sum(1 for i in mine if i["kind"] == "waiting")})
    return {"lanes": shown, "colors": col, "liveness": {l: live[l] for l in shown}, "categories": cats, "by_agent": by_agent,
            "feed": {"poll_ts": (poll or {}).get("ts"), "board_revision": board.get("revision")}}
