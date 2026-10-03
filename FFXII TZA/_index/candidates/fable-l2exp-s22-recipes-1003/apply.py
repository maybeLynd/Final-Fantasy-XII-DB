"""apply.py - FABLE staged correction applier (2026-10-03, on SWE2-AUDIT-SPEC's L2 expansion).

Default is a DRY RUN: it reports what it would change and writes nothing. --apply writes the page.
- Anchored: every edit's OLD text must occur EXACTLY ONCE on the page, or the edit FAILs.
- Refuses a dirty page: if `git status --porcelain` lists the page, --apply refuses; a dry run then
  measures against the HEAD blob instead of the working tree and says so.
- Keeps the page's line endings (CRLF or LF) and writes bytes back unchanged elsewhere.
- Idempotent: an edit whose full replacement is already present is SKIPPED (already applied).
- Prints FAILS N last.
"""
import os
import subprocess
import sys

STAMP = "*(corrected 2026-10-03, FABLE, on SWE2-AUDIT-SPEC's L2 expansion)*"
PAGE = '08-Combat-Formula/CONTRACT-weapon-recipes.md'   # repo-relative path under Database/FFXII TZA/
EDITS = [
    ('E1 section 13: two native replays execute the resolver and the RW-5 steps',
     "**None.** No experiment executes this resolver. S-22's runtime cell is not addressed by this\ncontract. *Stated rather than left blank so a CONTRACT READY header is not read as evidence of\nexecution.*",
     '**Isolated native replay, not a running game.** Evidence class NATIVE-REPLAY (unicorn), `live_game: false`:\nthe shipped bytes run at their own addresses with no application stub. The recipes are the shipped ones\n(pointer table `01EF96C0`, step table `01EFA5C0`); only the stats blocks, the result record and the action\nrows are planted. FABLE re-ran both packages on 2026-10-03 under unicorn 2.1.4, and every result file\nreproduced byte-identically.\n\n- [`s22-opus-replay-recipe-resolver`](../_index/candidates/s22-opus-replay-recipe-resolver/README.md)\n  (2026-09-25, md5 `a226db98…`, 871-function allowed set) runs the resolver `00385F60` on authored recipes.\n  - The static parts of `RW-1`, `RW-2` and `RW-4` are read from the mapped image.\n  - `RW-2`, executed and asserted: the committed path runs only the second list. Recipe 39 (first list\n    `[193]`, second list empty) calls no step. Recipes 74, 90, 5 and 4 call exactly their second lists, in\n    order.\n  - The cut-short arm executed. Recipe 6 stops after slot 4 and recipe 2 after slot 40, each when the step\n    just run left `02AEDFB8 = 1`. The package records this without asserting it;\n    [`check_s22_recipes.py`](../_index/candidates/fable-l2exp-s22-recipes-1003/check_s22_recipes.py)\n    asserts it from the record.\n  - Not covered: recipe 25 (bow) stops in its first committed slot, 29, at a read of `0x1C` that the\n    fixture does not plant, so no weapon family\'s committed run executes. The skip-entirely arm\n    (`00386249`–`003862AE`), the recipe taken from the equipped item (`0038618B`–`00386210`) and the effects\n    of the post-loop `00390F20` are static only.\n- [`s22-opus-replay-severe-weather-gate`](../_index/candidates/s22-opus-replay-severe-weather-gate/README.md)\n  (2026-09-26, 5/5, md5 `867bbaf3…`) asserts `RW-5` on steps 35 (`003895D0`) and 36 (`00389610`).\n  - With context byte `+0x1A` bit `0x04` clear and weather class 2, a hit chance of 100 becomes 80 and 50.\n  - With that bit set, or with class 0 or 1, it is unchanged.\n  - No other bit of `+0x18`..`+0x1B`, the element bypass\'s included, opens or closes the gate.\n  - The package measures the byte. "Merged bit 2" names the same bit only if the merged context is counted\n    from `+0x1A`; it is bit 18 of a dword at `+0x18`.\n\nNothing here has been observed in a running game.'),
]   # list of (label, old, new_text); the page gets "~~old~~ new_text STAMP"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
REL = "Database/FFXII TZA/" + PAGE
ABS = os.path.join(ROOT, *REL.split("/"))


def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True).stdout


def replacement(old, new):
    return "~~" + old + "~~ " + new + " " + STAMP


def main():
    do_apply = "--apply" in sys.argv
    fails = 0
    dirty = git("status", "--porcelain", "--", REL).decode("utf-8", "replace").strip()
    if dirty:
        print("NOTE page is dirty in the shared tree: %s" % dirty)
        if do_apply:
            print("FAIL refusing --apply on a dirty page")
            print("FAILS 1")
            return 1
        raw = git("show", "HEAD:" + REL)
        src = "HEAD blob"
    else:
        raw = open(ABS, "rb").read()
        src = "working tree (clean)"
    head = git("rev-parse", "--short", "HEAD").decode().strip()
    print("page %s  source %s  HEAD %s  mode %s" % (REL, src, head, "APPLY" if do_apply else "dry-run"))
    text = raw.decode("utf-8")
    crlf = "\r\n" in text
    nl = "\r\n" if crlf else "\n"
    work = text.replace("\r\n", "\n") if crlf else text
    print("line endings %s" % ("CRLF" if crlf else "LF"))
    changed = 0
    for label, old, new in EDITS:
        rep = replacement(old, new)
        n_old = work.count(old)
        n_rep = work.count(rep)
        if n_rep == 1:
            print("SKIP %s: already applied" % label)
            continue
        if n_old != 1:
            print("FAIL %s: OLD text occurs %d times (needs exactly 1)" % (label, n_old))
            fails += 1
            continue
        work = work.replace(old, rep, 1)
        changed += 1
        print("PASS %s: anchored once, would %s (+%d chars)" % (label, "write" if do_apply else "replace", len(rep) - len(old)))
    out = work.replace("\n", nl) if crlf else work
    if do_apply and changed and not fails:
        with open(ABS, "wb") as f:
            f.write(out.encode("utf-8"))
        print("WROTE %s (%d edits)" % (REL, changed))
    elif do_apply and fails:
        print("not written: failures above")
    print("edits %d, to change %d" % (len(EDITS), changed))
    print("FAILS %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
