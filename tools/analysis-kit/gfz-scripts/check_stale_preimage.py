#!/usr/bin/env python3
"""check_stale_preimage.py - refuse a publish that silently reverts a peer's recent commit (SWE2-FRONTIER, 2026-10-03).

OPUS-REQ-FRONTIER-STALE-PREIMAGE-GATE-1003, from AUDIT-SEM's systemic finding #1 in the user's audit follow-up:
95b1f3a4c (SWE2-CONTRACT, a 38-package batch) committed CONTRACT-ui-request-router.md from a pre-image older than
FABLE's fa2f75e21. FABLE's correction vanished and the struck original text came back. No gate caught it, because
publish_paths commits the worktree bytes and nothing compared them with what peers had committed since.

THE SIGNATURE. For each named path, the text about to be committed (NEW) is compared with HEAD, and with every recent
commit X on that path made by ANOTHER identity (subject prefix before ':'). X is "reverted" when:
  (a) X added at least MIN_LINES substantive lines (stripped length >= MIN_LEN, not themselves a strike), and at least
      FRACTION of them are present at HEAD but absent from NEW - not even kept inside a ~~strike~~ (a correction that
      strikes a peer's text keeps it, so it is never a revert); and
  (b) either X removed lines and at least one of them comes back in NEW (the pre-X text is restored), or X removed
      nothing (a pure addition that disappears).
Rewording a peer's paragraph satisfies (a) but rarely (b), which is the false-positive guard. The sweep in the record
measures the rate over recent history.

OVERRIDE. A deliberate revert names the commit in the publish message: a line `reverts: <sha>[, <sha>...]` (7+ hex).
That is an auditable act in the commit message, like the correction gate's override contract.

    python check_stale_preimage.py <repo-root> <message-file> <path>...   -> exit 0 clean, 9 refuse, 2 bad call
    python check_stale_preimage.py --self-test
Environment: TEAM_AGENT names the publisher (its own commits are never "peers"); STALE_PREIMAGE_DAYS (default 14).
"""
import os, re, subprocess, sys

MIN_LEN = 40
MIN_LINES = 3
FRACTION = 0.6
MAX_COMMITS = 25
STRIKE = re.compile(r"~~(.+?)~~")
REVERTS = re.compile(r"(?im)^\s*reverts:\s*(.+)$")


def ident(subject):
    m = re.match(r"^([A-Z][A-Z0-9-]+):", subject or "")
    return m.group(1) if m else ""


def same_lane(a, b):
    """SWE2-CONTRACT and SWE2CONTRACT-PUB-... are one lane; FABLE-PUB-x is FABLE."""
    n = lambda s: re.sub(r"[^A-Z0-9]", "", (s or "").upper()).split("PUB")[0]
    return bool(a) and bool(b) and (n(a) == n(b) or n(a).startswith(n(b)) or n(b).startswith(n(a)))


def lines(text):
    return [l.strip() for l in (text or "").replace("\r\n", "\n").split("\n")]


def substantive(ls):
    return [l for l in ls if len(l) >= MIN_LEN and "~~" not in l]


def struck_text(text):
    return " ".join(m.group(1) for m in STRIKE.finditer(text or ""))


def reverted(head_text, new_text, peer):
    """peer = (sha, subject, added_lines, removed_lines). Returns a finding dict or None."""
    sha, subject, added, removed = peer
    head, new = set(lines(head_text)), set(lines(new_text))
    kept_in_strikes = struck_text(new_text)
    add = [a for a in substantive(added) if a in head]            # X's lines still standing at HEAD
    if len(add) < MIN_LINES:
        return None
    gone = [a for a in add if a not in new and a not in kept_in_strikes]
    if len(gone) < FRACTION * len(add):
        return None
    rem = [r for r in substantive(removed)]
    back = [r for r in rem if r in new and r not in head]
    if rem and not back:
        return None                                                  # (b) fails: X removed text that does not come back
    return {"commit": sha, "subject": subject, "added": len(add), "gone": len(gone), "restored": len(back),
            "example": gone[0][:120]}


def git(root, *a):
    r = subprocess.run(["git", "-c", "core.longpaths=true", "-C", root, *a], capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def peers(root, path, agent, base="HEAD", days=None, since=None):
    """Recent commits on `path` reachable from `base`, by identities other than `agent`. `since` (an ISO date) replaces
    the relative window when replaying history."""
    days = days or int(os.environ.get("STALE_PREIMAGE_DAYS", "14"))
    window = "--since=%s" % since if since else "--since=%d.days" % days
    rc, out = git(root, "log", "--format=%h%x09%s", window, "-n", str(MAX_COMMITS), base, "--", path)
    res = []
    for line in out.splitlines():
        sha, _, subj = line.partition("\t")
        if agent and same_lane(ident(subj), agent):
            continue
        _, d = git(root, "show", "--format=", "-U0", sha, "--", path)
        add = [l[1:] for l in d.splitlines() if l.startswith("+") and not l.startswith("+++")]
        rem = [l[1:] for l in d.splitlines() if l.startswith("-") and not l.startswith("---")]
        res.append((sha, subj, [x.strip() for x in add], [x.strip() for x in rem]))
    return res


def overrides(msg_text):
    out = set()
    for m in REVERTS.finditer(msg_text or ""):
        out |= {x.lower() for x in re.findall(r"\b[0-9a-fA-F]{7,40}\b", m.group(1))}
    return out


def generated_outputs(root, paths):
    """{output path: binding path} for outputs of a GENERATION-BINDING.json published in the same batch whose worktree
    bytes are exactly what that binding records (OPUS, 2026-10-03). A generator replaces such a file WHOLE on every
    generation, so a new generation always 'removes' the previous one's lines; that is regeneration, not a revert of a
    peer's edit, and the binding proves the bytes are the generator's (derived_binding.py)."""
    out = {}
    try:
        import derived_binding as DB_
    except Exception:
        return out
    for b in paths:
        b = b[2:] if b.startswith("./") else b
        if not b.endswith("GENERATION-BINDING.json"):
            continue
        try:
            with open(os.path.join(root, b), "rb") as f:
                binding = DB_.load(f.read())
        except Exception:
            continue
        for o, want in binding.get("outputs", {}).items():
            try:
                with open(os.path.join(root, o), "rb") as f:
                    if DB_.sha(f.read()) == want:
                        out[o] = b
            except OSError:
                pass
    return out


def gate(root, paths, msg_text, agent=None):
    """(ok, findings, notes). A finding is refused unless the message names its commit on a `reverts:` line."""
    ov = overrides(msg_text)
    findings, notes = [], []
    gen = generated_outputs(root, paths)
    for p in paths:
        p = p[2:] if p.startswith("./") else p
        if not p.endswith((".md", ".tsv", ".py", ".json", ".txt")):
            continue
        if p in gen:
            notes.append("generated output of %s (whole-file regeneration, bound bytes): not a revert" % gen[p])
            continue
        rc, head_text = git(root, "show", "HEAD:" + p)
        if rc != 0:
            continue                                                 # a new file reverts nothing
        try:
            new_text = open(os.path.join(root, p), encoding="utf-8", errors="replace").read()
        except OSError:
            continue                                                 # a deletion is named explicitly; not this gate's case
        for pe in peers(root, p, agent):
            f = reverted(head_text, new_text, pe)
            if not f:
                continue
            f["path"] = p
            if any(f["commit"].lower().startswith(o) or o.startswith(f["commit"].lower()) for o in ov):
                notes.append("declared revert of %s on %s (reverts: line)" % (f["commit"], p))
            else:
                findings.append(f)
    return not findings, findings, notes


def replay(root, commit, path, days=14):
    """Evaluate `commit`'s change to `path` as this gate would have at publish time: HEAD = the commit's parent, NEW =
    the commit's blob, peers = other identities' commits on the path in the `days` before it."""
    _, subj = git(root, "log", "-1", "--format=%s", commit)
    _, when = git(root, "log", "-1", "--format=%cI", commit)
    import datetime
    since = (datetime.datetime.fromisoformat(when.strip()) - datetime.timedelta(days=days)).isoformat()
    rc, head_text = git(root, "show", "%s~1:%s" % (commit, path))
    rc2, new_text = git(root, "show", "%s:%s" % (commit, path))
    if rc != 0 or rc2 != 0:
        return []
    out = []
    for pe in peers(root, path, ident(subj.strip()), base=commit + "~1", since=since):
        f = reverted(head_text, new_text, pe)
        if f:
            f["path"] = path
            out.append(f)
    return out


def self_test():
    ok = 0
    L = lambda n, tag: ["%s line %02d - long enough to count as a substantive database sentence here" % (tag, i) for i in range(n)]
    old, newx = L(4, "ORIGINAL"), L(5, "CORRECTED")
    head_text = "\n".join(["# page"] + newx + ["tail"])
    peer = ("abc1234", "FABLE: correction", newx, old)
    # 1. a stale pre-image: the corrected lines vanish and the original lines come back -> refused
    stale = "\n".join(["# page"] + old + ["tail"])
    assert reverted(head_text, stale, peer), "stale pre-image not caught"
    ok += 1
    # 2. a clean publish that keeps the peer's lines and adds its own -> passes
    clean = head_text + "\nmy own new sentence, long enough to be substantive for the gate here"
    assert reverted(head_text, clean, peer) is None
    ok += 1
    # 3. a correction that STRIKES the peer's lines keeps them -> passes
    struck = "\n".join(["# page"] + ["~~%s~~ replaced by a new reading" % l for l in newx] + ["tail"])
    assert reverted(head_text, struck, peer) is None
    ok += 1
    # 4. rewording the peer's lines without restoring the old text -> passes (condition b)
    reword = "\n".join(["# page"] + L(5, "REWORDED") + ["tail"])
    assert reverted(head_text, reword, peer) is None
    ok += 1
    # 5. a pure addition by a peer that disappears -> refused
    add_only = ("def5678", "OPUS: new section", L(4, "ADDED"), [])
    h2 = head_text + "\n" + "\n".join(L(4, "ADDED"))
    assert reverted(h2, head_text, add_only)
    ok += 1
    # 6. overrides: a `reverts:` line names the commit
    assert overrides("subject\n\nreverts: abc1234, def5678\n") == {"abc1234", "def5678"}
    ok += 1
    # 7. lane identity: SWE2CONTRACT-PUB-X is SWE2-CONTRACT; FABLE-PUB-Y is FABLE; FABLE is not OPUS
    assert same_lane(ident("SWE2CONTRACT-PUB-CONTRA-01F68168: x"), "SWE2-CONTRACT") and same_lane("FABLE-PUB-A", "FABLE")
    assert not same_lane("FABLE", "OPUS")
    ok += 1
    print("self-test: %d case(s) passed" % ok)
    return 0


def main(argv):
    if argv[1:2] == ["--self-test"]:
        return self_test()
    if len(argv) < 4:
        print(__doc__.split("\n")[0]); return 2
    root, msgf, paths = argv[1], argv[2], argv[3:]
    msg = open(msgf, encoding="utf-8", errors="replace").read() if os.path.isfile(msgf) else ""
    ok, findings, notes = gate(root, paths, msg, os.environ.get("TEAM_AGENT"))
    for n in notes:
        print("note: " + n)
    for f in findings:
        print("STALE PRE-IMAGE: %s would remove %d of %d lines %s added (%s) and restore %d line(s) it replaced - e.g. %r"
              % (f["path"], f["gone"], f["added"], f["commit"], f["subject"][:70], f["restored"], f["example"]))
    return 0 if ok else 9


if __name__ == "__main__":
    sys.exit(main(sys.argv))
