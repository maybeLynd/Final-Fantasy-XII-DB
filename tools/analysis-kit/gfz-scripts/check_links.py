#!/usr/bin/env python3
"""Verify every relative markdown link in the database resolves."""
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import head_scope as HS  # noqa: E402
import kit_paths as KP  # noqa: E402

ROOTS = [
    os.path.join(KP.ROOT, "Database", "FFXII TZA"),
    os.path.join(KP.ROOT, "Database", "Tools"),
]

# Session scratch.  `Tools/work/<session>/` holds working notes, staged rows and disposition
# drafts; their links point at wherever the author was standing and are not database links.
# On 2026-09-03 a live session's scratch file turned this gate red, which under the
# non-atomic-gates rule cost a diagnosis before anyone could act on the real result.
SKIP_DIRS = {"work", "__pycache__", ".git", "node_modules"}

# `--db` was ACCEPTED AND SILENTLY IGNORED.  Every invocation in this project passes
# `--db "FFXII TZA"`, and the checker walked BOTH roots regardless -- so every "N links all
# resolve" figure the fleet has quoted was measured over a population nobody chose, database
# plus all of Tools.  **A selector nothing reads is worse than no selector: it tells the caller
# a population was chosen.**  Same defect class as the audit counter that counted the wrong
# noun, in the gate everyone quotes.
if "--db" in sys.argv:
    i = sys.argv.index("--db")
    if i + 1 >= len(sys.argv):
        sys.exit("--db needs a path")
    arg = sys.argv[i + 1]
    ROOTS = [arg if os.path.isabs(arg) else os.path.abspath(arg)]
    if not os.path.isdir(ROOTS[0]):
        sys.exit("--db path does not exist: %s" % ROOTS[0])
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE = re.compile(r"```.*?```", re.S)
CODE_SPAN = re.compile(r"`[^`\n]*`")

# THREE SCOPE CORRECTIONS, OPUS 2026-09-30 (pass-29 dry run found 4,565 "broken at HEAD", 4 of them real):
#
#   CAPTURES   `_experiments/evidence/<package>/` holds immutable evidence. Its package-level files (README, RESULT,
#              PLAN ...) are documents and are judged. Anything in a SUBDIRECTORY of a package (`retained/`,
#              `current-preimages/`, `private-source/`, `run-01/...`) is a byte-exact capture of a page as it stood
#              elsewhere; its relative links point from where the page lived, and the capture may not be edited to
#              "fix" them. 4,537 of the 4,565 were such captures. They are counted and printed as a total, never
#              judged.
#   CODE SPANS `vtbl[0xD0](+0x6C0, word[part+0x8A])` inside backticks is not a link - Markdown renders it as code.
#              Only a code span that itself contains `](` is blanked; `[`name`](target)` stays a link. 9 cases.
#   PERCENT    Markdown decodes `%20`; `../../FFXII%20TZA/...` resolves to `FFXII TZA`. The target is unquoted
#              before resolving.
#
# THREE REPAIRS, OPUS 2026-10-01, on SWE2-AUDIT-SPEC's links-scope review (auditspec-review-links-scope-0930, AWN):
#   CODE SPANS are paired the CommonMark way across the paragraph (a backtick run opens, the next run of the SAME length
#              closes, an unmatched run is literal); the line-local regex mis-paired ``a`b`` and hid a real link (B1).
#   CAPTURES   the "subdirectory = capture" rule stays a convention, now written down where packages are made
#              (_experiments/README.md, "Evidence package layout"): authored documents go at package level. Judging
#              README-named files inside subdirectories was tried and rejected: on 2026-10-01 it flagged ~25 links, all in
#              true byte captures (`run-01/source/Database/...` mirrors, a `retained/` copy), none in an authored file.
#   PERCENT    a target whose decoding adds a path separator (`%2F`, `%5C`) is broken: browsers do not split on them (C3).
def is_capture(root, dirpath):
    rel = os.path.relpath(dirpath, root).replace(os.sep, "/").split("/")
    return len(rel) >= 4 and rel[0] == "_experiments" and rel[1] == "evidence"


def cm_spans(par):
    """CommonMark code spans in one paragraph: (start, end) offsets."""
    runs = [(m.start(), m.end()) for m in re.finditer(r"`+", par)]
    spans, i = [], 0
    while i < len(runs):
        s, e = runs[i]
        n = e - s
        j = next((k for k in range(i + 1, len(runs)) if runs[k][1] - runs[k][0] == n), None)
        if j is None:
            i += 1
            continue
        spans.append((s, runs[j][1]))
        i = j + 1
    return spans


def blank_code_spans(text):
    """Blank (keeping newlines and length) every CommonMark code span that contains `](`; it renders as code."""
    out = []
    for part in re.split(r"(\n[ \t]*\n)", text):
        chars = list(part)
        for s, e in cm_spans(part):
            if "](" in part[s:e]:
                for k in range(s, e):
                    if chars[k] != "\n":
                        chars[k] = " "
        out.append("".join(chars))
    return "".join(out)


n_captures = 0

# `os.path.exists` ANSWERS A DIFFERENT QUESTION ON WINDOWS THAN ON POSIX, and this gate has been
# quoting the Windows answer.  Two link classes resolve here and would not resolve on a
# case-sensitive filesystem, so a broken link can sit in the corpus with the gate green:
#
#   DOTS-ONLY   Win32 strips trailing dots from a path component, so `foo/...` collapses to `foo`
#               and `os.path.exists` returns True.  `[label](...)` - a placeholder target written
#               while quoting a link in prose - therefore PASSES.  Found 2026-09-14 after the
#               U+2026 variant of the same placeholder (`[label](<ellipsis>)`, which Win32 does NOT
#               strip) turned this gate red and blocked every publisher on the board
#               (FABLE-NOTE-OPUS-BROKEN-LINK-HEAD).  The repair substituted `...` for the ellipsis
#               and the gate went green - green because of the platform, not because of the link.
#   CASE        Windows matches filenames case-insensitively.
#               `.../contract-group-completion-and-respawn.md` resolved for a file actually named
#               `CONTRACT-...`; one such link was in the corpus, in EXP-019.
#
# So resolve the way the strict platform does: walk the target component by component and require
# each to appear in its parent's listing under its EXACT spelling.
def resolves_strictly(dirpath, target):
    cur = dirpath
    for part in os.path.normpath(target).split(os.sep):
        if part in ("", "."):
            continue
        if part == "..":
            cur = os.path.dirname(cur)
            continue
        try:
            names = os.listdir(cur or ".")
        except OSError:
            return False
        if part not in names:
            return False
        cur = os.path.join(cur, part) if cur else part
    return True


# Links known to fail the strict test that this gate may not go red for yet, because the file is
# claimed by another identity and turning the gate red would block every publisher on a file its
# owner alone may edit - the exact failure this hardening exists to prevent.  Each entry names the
# request that clears it.  A waiver is DEBT, printed loudly on every run, never a tolerance: when
# the owner lands the fix, delete the row and the class hard-fails everywhere.
#
# Empty since 2026-09-15 (OPUS-PASS29-HEAD-LINKS-REPAIR). The two AUDIT-LOG `[label](...)` rows were
# the only entries; the prose now quotes the label without link syntax, so both are repaired rather
# than waived and the class hard-fails everywhere, as the paragraph above intends.
STRICT_WAIVERS = {}

bad = []
weak = []
n_files = 0
n_links = 0

for root in ROOTS:
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.lower().endswith(".md"):
                continue
            p = os.path.join(dirpath, fn)
            n_files += 1
            with open(p, encoding="utf-8") as f:
                text = f.read()
            # Markdown link syntax inside a fenced code block is not a link.  Added
            # 2026-09-02 after `stepTable[slotId](rcx, rdx, r8)` in a disassembly listing was
            # reported as a broken link to "rcx, rdx, r8".  check_consistency.py already
            # strips fences for the same reason.
            text = blank_code_spans(FENCE.sub("", text))
            if is_capture(root, dirpath):
                n_captures += len(LINK.findall(text))
                continue
            for m in LINK.finditer(text):
                target = m.group(1).strip()
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                raw = target.split("#", 1)[0]
                target = urllib.parse.unquote(raw)
                if not target:
                    continue
                if any(target.count(c) > raw.count(c) for c in "/\\"):
                    n_links += 1
                    bad.append((os.path.relpath(p, root), "%s  [an encoded path separator (%%2F / %%5C) is not a separator in a "
                                "browser]" % raw, p, dirpath))
                    continue
                resolved = os.path.normpath(os.path.join(dirpath, target))
                n_links += 1
                if not os.path.exists(resolved):
                    bad.append((os.path.relpath(p, root), target, p, dirpath))
                elif not resolves_strictly(dirpath, target):
                    rel = os.path.relpath(p, root).replace(os.sep, "/")
                    waiver = STRICT_WAIVERS.get((rel, target))
                    if waiver:
                        weak.append((rel, target, waiver))
                    else:
                        bad.append((os.path.relpath(p, root),
                                    "%s  [resolves only on a case-insensitive / "
                                    "trailing-dot-stripping filesystem]" % target, p, dirpath))


# --raw: machine output for the publish guard. check_publish_neighbours.py runs this inside each
# of its two detached worktrees, where the published paths are WORKING-TREE edits - the
# head_scope split below would file every break they introduce as "not published debt" and the
# gate would see nothing. Raw mode reports every broken link on both sides and lets the guard do
# the before/after diff itself. Added 2026-09-17 for OPUS-REQ-FRONTIER-PASS29-THIRTY-BROKEN-RELATIVE-LINKS.
if "--raw" in sys.argv:
    for src, tgt, _p, _d in sorted(bad):
        print("BROKEN\t%s\t%s" % (src.replace(os.sep, "/"), tgt))
    sys.exit(1 if bad else 0)


# ---- THE FIX IS COMPUTABLE, SO THE GATE NAMES IT ------------------------------------------------
# FABLE censused all 39 pages that link to ADDRESS-INDEX.md and found the shape of this defect
# (FABLE-NOTICE-OPUS-ADDRESS-INDEX-LINKS-ARE-BEING-WRITTEN-AT-THE-WRONG-DEPTH): all 27 depth-2
# pages write `../../_index/` and are right; every depth-1 page written before 2026-09-15 writes
# `../_index/` and is right; three depth-1 pages now write `../../_index/` and are wrong. The wrong
# form is CORRECT on the majority of pages that link to the index, so it survives being copied and
# breaks only when it lands one directory shallower.
#
# That is why a prose convention would not have helped: nobody is getting a rule wrong, they are
# copying a line that is true where it came from. The number of `../` is not a convention at all -
# it is a function of the page's depth, computable from the page itself. So the gate computes it.
# A gate that says "broken" sends someone to work it out by hand; a gate that says "you wrote two
# and the answer is one" is mechanical enforcement of a definition, which is what this class of
# defect needs. OPUS ruling, 2026-09-15.
def suggest(dirpath, target):
    """The same target at a different `../` depth, if exactly one such depth resolves."""
    t = target.replace("\\", "/")
    stripped = t
    while stripped.startswith("../"):
        stripped = stripped[3:]
    if stripped == t and not t.startswith("./"):
        return None                      # not a parent-relative link; nothing to re-depth
    hits = []
    for depth in range(0, 5):
        cand = "../" * depth + stripped
        if cand == t:
            continue
        if os.path.exists(os.path.normpath(os.path.join(dirpath, cand))) \
                and resolves_strictly(dirpath, cand):
            hits.append(cand)
    return hits[0] if len(hits) == 1 else None


print("scanned %d markdown files, %d relative links" % (n_files, n_links))
print("evidence captures not judged (package subdirectories under _experiments/evidence): %d link(s)" % n_captures)
# THE WAIVER TABLE IS REPORTED EVEN WHEN IT IS EMPTY, because an empty waiver table and an absent
# waiver mechanism print exactly the same thing: nothing. FINAL-AUDIT pass 29's standing objection
# was that two case-sensitive links had been cleared by WAIVER rather than by repair. They were
# since repaired and STRICT_WAIVERS emptied - but a reader of this output could not tell that from
# a run in which waivers were simply never considered, and on 2026-09-15 a reader did read it the
# other way. A gate that has stopped excusing anything should say so out loud; it is the same rule
# run_gates.py applies to the checkers it cannot run. OPUS, 2026-09-15.
print("case-sensitivity waivers in STRICT_WAIVERS: %d%s"
      % (len(STRICT_WAIVERS),
         "" if STRICT_WAIVERS else "  - nothing is being excused; every link below is judged"))
if weak:
    print("\nWAIVED, STILL BROKEN ON A CASE-SENSITIVE FILESYSTEM (%d) -- debt, not a pass:" % len(weak))
    for src, tgt, req in weak:
        print("  %s  ->  %s   cleared by %s" % (src, tgt, req))
if bad:
    # ---- WHOSE RED IS IT --------------------------------------------------------------------
    # This gate reads the WORKING TREE, and several lanes write it at once. On 2026-09-15 all nine
    # broken links were in three files that are clean at HEAD - a peer's in-flight edit, published
    # by nobody. The gate simply said BROKEN, so the next person to publish had to either repair a
    # page they do not own or argue that a global gate being red was acceptable. FABLE did the
    # latter twice in one session, correctly but by hand. That is how a shared gate stops being
    # read: it goes red for something the reader cannot act on and has no way to see that.
    #
    # So the two populations are separated, because they need opposite responses. A link broken at
    # HEAD is published debt and blocks. A link broken only in the working tree belongs to whoever
    # is holding that file and will leave with their commit - and it is also why a FINAL-AUDIT run
    # must be taken at HEAD: a terminal-streak run over a dirty tree can be reddened by an edit
    # that was never published. OPUS, 2026-09-15.
    # The split itself lives in head_scope, with its own both-ways self-test, because this is the
    # third gate to need it and a second copy of a definition is a second definition.
    if not HS.self_test_quiet():
        print("\n  CONTROL FAILED: head_scope's self-test does not pass, so every link below")
        print("  would be classified by a test that does not work. Run head_scope.py.")
        sys.exit(2)

    at_head, worktree_only = [], []
    for src, tgt, p, dirpath in bad:
        raw = tgt.split("  [")[0]
        (worktree_only if HS.worktree_only(p, raw) else at_head).append((src, tgt, dirpath))

    for label, group in (("BROKEN AT HEAD", at_head),
                         ("BROKEN ONLY IN THE WORKING TREE - an uncommitted edit, not published "
                          "debt", worktree_only)):
        if not group:
            continue
        print("\n%s (%d):" % (label, len(group)))
        for src, tgt, dirpath in group:
            fix = suggest(dirpath, tgt.split("  [")[0])
            print("  %s  ->  %s%s" % (src, tgt, ("\n      write %s - the number of `../` is the "
                                                 "page's own depth" % fix) if fix else ""))
    if at_head:
        sys.exit(1)
    print("\nnothing is broken at HEAD. The %d above live in uncommitted edits and belong to "
          "whoever holds\nthose files; publishing a path of your own is not blocked by them."
          % len(worktree_only))
    sys.exit(0)
if weak:
    print("all relative links resolve HERE; %d resolve only on this filesystem (see above)" % len(weak))
else:
    print("all relative links resolve, on this filesystem and on a case-sensitive one")
