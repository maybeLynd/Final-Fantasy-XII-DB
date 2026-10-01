#!/usr/bin/env python3
"""Correction-publish consumer-check gate (SWE2-FRONTIER, 2026-09-26).

Implements FABLE-REQ-FRONTIER-CONTRACT-CORRECTION-PUBLISH-NEEDS-CONSUMER-CHECK:
EVIDENCE-POLICY rule 4a says a correction updates every affected current
consumer; until now that lived in memory, and the drift cases are recorded
(EXP-189's '8 dwords' receipt surviving its own contract; the (0, cx) /
handler(id, 0) swap; 69e9cad19's 01EC81F0 reverted with no record of which
reading was right). This gate makes the check a shape the publish either
carries or is refused for lacking.

A publish is a CORRECTION publish when a named path's `git diff HEAD` adds a
hunk containing BOTH a struck claim (a real '~~text~~' pair, not a mention of
the marker) and a correction keyword (Corrected / Superseded / REFUTED,
case-insensitive) among its added lines. Strike-only or keyword-only hunks do
not trigger, nor do files under _index/_inbox/ -- inbox text is operational
narrative (resume blocks describe corrections, they are not claims), while the
canonical claims the rule protects live in the database pages.

When it triggers, the publish must carry a consumer-check record either
  - staged: a named path under Database/FFXII TZA/_index/candidates/, or
  - named: a _index/candidates/ path written in the commit message.
A qualifying record lists current consumers (the word 'consumer' plus an
agreement token 'agrees', 'revised-here' or 'routed-to-') and names a
regression. When the corrected claim is an executable shape (reset
widths/masks, argument order, register/byte bindings), the named regression
must be an existing .py control - matching words is not the control.

Records marked PENDING PROPAGATION or listing routed-to-<task> consumers
pass the gate but are printed, so the publish transcript shows the
correction is not yet propagated.

Extended 2026-09-27 (FRONTIER-TODO-CORRECTION-DECLARATION-AND-OVERRIDE):
a qualifying record must carry an explicit affected-claim declaration - an
'affected'/'corrects' line naming a row id or path - and any path it declares
must be among this publish's touched database files. Detection (strike +
keyword) is only the supplement that catches UNDECLARED corrections; a
declared correction needs no ~~markers~~. A record naming a .py control for
an executable claim must also pin the run to a commit that is an ancestor of
HEAD (run:/receipt:/verified at <sha>) - naming the script is not proof it
ran, and a receipt at a non-ancestor revision is the EXP-201/214 failure
shape (same count, different bytes). The env override moved to an auditable
contract in publish_paths.sh (correction-override: + override-reason: lines
in the commit message).

Usage (from publish_paths.sh):
    python publish_correction_gate.py <repo-root> <message-file> <path>...
Exit 0 clean, 8 refuse, 2 bad invocation. Prints verdict lines to stdout.
"""
import re, subprocess, sys
from pathlib import Path

CANDIDATES = "Database/FFXII TZA/_index/candidates/"
DB_MD = re.compile(r"^Database/FFXII TZA/(?!_index/_inbox/).*\.md$", re.I)
KEYWORD = re.compile(r"\b(corrected|superseded|refuted)\b", re.I)
STRIKE = re.compile(r"~~[^~\s][^~]*~~")  # a real strike pair, not a `~~` mention
AGREE = re.compile(r"agrees|revised-here|routed-to-", re.I)
PENDING = re.compile(r"pending propagation", re.I)
# A record must say WHAT it corrects (2026-09-27 directive): an 'affected' or
# 'corrects' declaration naming a row id or a path. Strike/keyword detection
# only finds the undeclared corrections; the declaration is the contract.
AFFECTED = re.compile(
    r"(?im)^.*\b(?:affected|corrects?)\b[^\n]{0,240}?"
    r"(?:[A-Z]{1,5}-?\d+[a-z]?|[\w./\\-]+\.(?:md|tsv|py))")
# A receipted run (2026-09-27): 'run'/'receipt'/'verified'/'executed' naming a
# commit. A named script is not proof it ran; the commit must exist and be an
# ancestor of HEAD.
RECEIPT = re.compile(
    r"(?im)\b(?:run|receipt|verified|executed)\b[^\n]{0,80}?"
    r"\b([0-9a-f]{7,40})\b")
# Executable claim shapes: widths/masks with hex, argument orders, byte/register binds.
EXEC_CLAIM = re.compile(
    r"(zeroed|cleared|anded|masked|bytes)\b[^\n]{0,80}0x[0-9a-fA-F]+"
    r"|0x[0-9a-fA-F]+[^\n]{0,60}\b(bytes|dwords|zeroed|masked)\b"
    r"|\(\s*0\s*,|\bhandler\s*\(|argument order|argument capture|\becx\b|\bedx\b",
    re.I)
PYREF = re.compile(r"[\w./\\-]+\.py\b")


def diff_paths(root, paths):
    out = {}
    for p in paths:
        rel = p[2:] if p.startswith("./") else p
        if not DB_MD.match(rel):
            continue
        d = subprocess.run(["git", "-C", root, "diff", "HEAD", "--", rel],
                           capture_output=True, text=True).stdout
        if d:
            out[rel] = d
    return out


def find_correction_hunks(diff):
    """Hunks whose added lines carry both ~~ and a correction keyword that
    the hunk's removed lines did not already carry.

    The markers are compared as multisets, not presence flags: a ledger row
    is one line, so once a publish has struck text in a row, every later
    edit to that row re-adds the whole line - strike pair and 'Superseded'
    included - and a presence test re-fires on a correction that is already
    at HEAD with its consumer-check record (UQ-156, FABLE's
    2026-09-26 container-bits publish). Counting only markers the removed
    lines did not already carry keeps the gate aimed at NEW corrections:
    a re-edited row whose strike/keyword text survives verbatim is not a
    new correction; a hunk that strikes new text or names a new keyword is.
    """
    from collections import Counter
    hits, cur_h, cur_added, cur_removed = [], "", [], []
    for line in diff.splitlines() + ["@@ end @@"]:
        if line.startswith("@@"):
            new_strikes = Counter(m.group(0) for a in cur_added
                                  for m in STRIKE.finditer(a))
            new_strikes.subtract(m.group(0) for a in cur_removed
                                 for m in STRIKE.finditer(a))
            new_kw = Counter(m.group(0).lower() for a in cur_added
                             for m in KEYWORD.finditer(a))
            new_kw.subtract(m.group(0).lower() for a in cur_removed
                            for m in KEYWORD.finditer(a))
            if sum(new_strikes.values()) > 0 and sum(new_kw.values()) > 0:
                hits.append((cur_h, cur_added))
            cur_h, cur_added, cur_removed = line, [], []
        elif line.startswith("+") and not line.startswith("+++"):
            cur_added.append(line[1:])
        elif line.startswith("-") and not line.startswith("---"):
            cur_removed.append(line[1:])
    return hits


def needs_exec_control(added_lines):
    return any(EXEC_CLAIM.search(a) for a in added_lines)


_norm = lambda s: re.sub(r"\s+", " ", s).strip()


def unquoted_strikes(root, rel, diff):
    """Added ~~spans~~ in a correction file whose (whitespace-normalised,
    `**`-ignored) text occurs in none of the file's removed lines and in no
    earlier revision of the file.

    A struck span is a claim that the page once said those words. FABLE
    caught the failure twice on 2026-09-26: an invented phrase struck to
    dress an append as a correction, and AC-7 (fbe583be5) whose struck body
    merged a heading clause, so the strike was not verbatim. The history
    fallback keeps verbatim re-quotes of older revisions legal; spans of
    <=8 normalised chars are exempt as punctuation noise.
    """
    removed_norm = _norm(" ".join(
        l[1:] for l in diff.splitlines()
        if l.startswith("-") and not l.startswith("---"))).replace("**", "")
    out = []
    for line in diff.splitlines():
        if not (line.startswith("+") and not line.startswith("+++")):
            continue
        for m in re.finditer(r"~~(.+?)~~", line):
            s = _norm(m.group(1))
            if len(s) <= 8 or s.replace("**", "") in removed_norm:
                continue
            probe = max(re.split(r"[`*\[\]()]", s.replace("**", "")),
                        key=len).strip()[:60]
            if probe and subprocess.run(
                    ["git", "-C", root, "log", "--format=%h", "-S", probe,
                     "--", rel],
                    capture_output=True, text=True).stdout.strip():
                continue
            out.append(s)
    return out


def is_record(root, rel):
    """True if rel is a consumer-check record under _index/candidates/."""
    p = Path(root) / rel
    if not rel.startswith(CANDIDATES) or not p.is_file():
        return False, None
    text = p.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"consumer", text, re.I) or not AGREE.search(text) \
            or not AFFECTED.search(text):
        return False, text
    return True, text


def record_regression(root, text):
    """An existing .py control the record names, or None."""
    for m in PYREF.finditer(text):
        cand = m.group(0).lstrip("./")
        if (Path(root) / cand).is_file():
            return cand
        for base in (CANDIDATES, "Database/FFXII TZA/_index/candidates"):
            hit = list((Path(root) / base).rglob(Path(cand).name)) if Path(root, base).is_dir() else []
            if hit:
                return str(hit[0])
    return None


def record_pending(text):
    if not text:
        return False
    return bool(PENDING.search(text) or re.search(r"routed-to-\w", text, re.I))


def record_receipts(root, text):
    """Commit tokens the record pins a run/verification to.

    Returns (good, bad): good tokens resolve to a commit that is an ancestor
    of HEAD; bad tokens either do not resolve or point at a commit that is not
    in history - a receipt at the wrong revision is the EXP-201/214 failure:
    the same count attached to different bytes.
    """
    good, bad = [], []
    for m in RECEIPT.finditer(text or ""):
        sha = m.group(1).lower()
        if subprocess.run(["git", "-C", root, "rev-parse", "--verify",
                           "--quiet", sha + "^{commit}"],
                          capture_output=True).returncode \
                or subprocess.run(["git", "-C", root, "merge-base",
                                   "--is-ancestor", sha, "HEAD"],
                                  capture_output=True).returncode:
            bad.append(sha)
        else:
            good.append(sha)
    return good, bad


def gate(root, paths, msg_text):
    """Return (ok, refuse_lines, note_lines)."""
    refuse, notes = [], []
    corrections = {}
    diffs = diff_paths(root, paths)
    for rel, d in diffs.items():
        hits = find_correction_hunks(d)
        if hits:
            corrections[rel] = hits
    # Strike provenance (FABLE-REQ-FRONTIER-STRIKE-MUST-QUOTE-REMOVED-TEXT):
    # every added ~~span~~ in a correcting file must quote text the file
    # actually carried - in this publish's removed lines, or verbatim in an
    # earlier revision.
    for rel in corrections:
        for s in unquoted_strikes(root, rel, diffs[rel]):
            refuse.append("%s strikes text it never said: %s" % (rel, s[:90]))

    # collect candidate record references: staged paths + msg text. A record
    # is validated whenever present - a declared correction (explicit
    # affected-claim declaration) needs no strike marker to be a correction;
    # detection only catches the undeclared kind.
    refs = [p[2:] if p.startswith("./") else p for p in paths
            if (p[2:] if p.startswith("./") else p).startswith(CANDIDATES)]
    for m in re.finditer(r"(?:Database/FFXII TZA/)?_index/candidates/[\w./\\-]+", msg_text):
        refs.append(m.group(0) if m.group(0).startswith("Database/") else
                    "Database/FFXII TZA/" + m.group(0))
    records = [r for r in refs if is_record(root, r)[0]]
    if not corrections:
        # No detected markers: a publish carrying only a candidate file is
        # free to go (it may be preparation). It still cannot smuggle a
        # malformed record - files named as records are checked below.
        if not records and not refuse:
            return True, refuse, notes
    elif not records:
        refuse.append(
            "correction marker(s) found in %s but no consumer-check record" %
            ", ".join(sorted(corrections)))

    # Declared affected paths must be touched by this publish.
    declared_paths = set()
    for r in records:
        _, text = is_record(root, r)
        for m in re.finditer(r"(?im)^.*\baffected\b[^\n]*", text or ""):
            for p in re.finditer(r"[\w./\\-]+\.(?:md|tsv)", m.group(0)):
                p2 = p.group(0).replace("\\", "/")
                if not p2.startswith("Database/"):
                    p2 = "Database/FFXII TZA/" + p2
                declared_paths.add(p2)
    touched = {p[2:] if p.startswith("./") else p for p in paths
               if DB_MD.match(p[2:] if p.startswith("./") else p)}
    touched_names = {t.rsplit("/", 1)[-1] for t in touched}
    for dp in sorted(declared_paths):
        if dp not in touched and dp.rsplit("/", 1)[-1] not in touched_names \
                and not any(t.endswith("/" + dp) for t in touched):
            refuse.append("record declares affected path %s but this "
                          "publish does not touch it" % dp)

    # exec_needed: detected correction hunks OR a record's own affected-claim
    # declaration carrying executable wording - a declared no-strike
    # correction of a width/mask claim is an exec claim too.
    exec_needed = any(EXEC_CLAIM.search(a)
                      for hits in corrections.values()
                      for _, added in hits for a in added)
    for r in records:
        ok, text = is_record(root, r)
        for m in re.finditer(r"(?im)^.*\baffected\b[^\n]*", text or ""):
            if EXEC_CLAIM.search(m.group(0)):
                exec_needed = True
    for r in records:
        ok, text = is_record(root, r)
        reg = record_regression(root, text or "")
        if exec_needed and not reg:
            refuse.append(
                "record %s names no existing .py regression; this claim "
                "shape needs an executed control, not matched words" % r)
        if reg and exec_needed:
            good, bad = record_receipts(root, text or "")
            for sha in bad:
                refuse.append(
                    "record %s pins a run to %s, which is not an ancestor of "
                    "HEAD - a wrong-revision receipt is not a receipt" %
                    (r, sha))
            if not good:
                refuse.append(
                    "record %s names control %s but pins no run commit "
                    "(run:/receipt:/verified at <sha>) - naming the script is "
                    "not proof it ran" % (r, reg))
        if record_pending(text):
            notes.append("record %s is PENDING PROPAGATION / has "
                         "routed-to- consumers" % r)
    details = ["%s::%s" % (rel, h) for rel, hits in corrections.items()
               for h, _ in hits]
    notes = details + notes
    return not refuse, refuse, notes


def main():
    if len(sys.argv) < 4:
        print("usage: publish_correction_gate.py <root> <msg-file> <path>...", file=sys.stderr)
        sys.exit(2)
    root, msg, paths = sys.argv[1], sys.argv[2], sys.argv[3:]
    # Callers may run this from a different cwd than the publish wrapper's
    # (publish_paths.sh cds into gfz-scripts first). A repo-relative msg
    # path then silently reads as "no message" and records named in it are
    # never seen - resolve relative paths against root too.
    msg_path = Path(msg)
    if not msg_path.is_file() and not msg_path.is_absolute():
        msg_path = Path(root) / msg
    msg_text = msg_path.read_text(encoding="utf-8", errors="replace") \
        if msg_path.is_file() else ""
    ok, refuse, notes = gate(root, paths, msg_text)
    for n in notes:
        print("note:", n)
    for r in refuse:
        print("refuse:", r)
    print("verdict:", "PASS" if ok else "REFUSE")
    sys.exit(0 if ok else 8)


if __name__ == "__main__":
    main()
