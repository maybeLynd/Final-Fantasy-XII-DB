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
PAGE = '08-Combat-Formula/CONTRACT-environmental-element-scaling.md'   # repo-relative path under Database/FFXII TZA/
EDITS = [
    ('E1 section 13: three native replays execute the stage and its getters',
     "**None.** No experiment executes these four bodies. S-22's runtime cell is not addressed by this\ncontract. *Stated rather than left blank so a CONTRACT READY header is not read as evidence of\nexecution.*",
     "**Isolated native replay, not a running game.** Evidence class NATIVE-REPLAY (unicorn), `live_game: false`:\nthe shipped bytes run at their own addresses, with no application stub and planted data only. FABLE re-ran\neach package on 2026-10-03 under unicorn 2.1.4, and every result file reproduced byte-identically.\n\n- [`s22-opus-replay-steps-and-element-scaling`](../_index/candidates/s22-opus-replay-steps-and-element-scaling/README.md)\n  (2026-09-25, md5 `99336e05…`) calls the stage `0038B220` directly, with the three getters live behind\n  their thunks.\n  - `WE-4`/`WE-5`, asserted: bit 16 on the target's mutable byte `+0x6A`, on its derived byte `+0x7A`, or on\n    the caster's merged bitmap `+0x1C` skips the whole stage. With none set, the same action scales.\n  - `WE-6`, asserted as a write-set bound: the stage writes only `02AEE054` and the cached unit pointer\n    `02EBF188`.\n  - `WE-2` and the rule table: all 288 element × environment × MWeather × terrain combinations executed. The\n    multipliers are recorded, not asserted. The record includes the shared multiply named by the\n    2026-10-02 correction: where an environment rule and a terrain rule for one element both hold, the\n    recorded factor is 1.2, not 1.44. Those cells are Lightning e0/t0, Ice e2/t2, Earth e1/t1, and Water e3/t0\n    outside MWeather 2.\n    [`check_s22_envscaling.py`](../_index/candidates/fable-l2exp-s22-envscaling-1003/check_s22_envscaling.py)\n    asserts those cells from the record and reads the one `mulss` (`0038B420`) at the bytes.\n- [`s22-opus-replay-recipe-resolver`](../_index/candidates/s22-opus-replay-recipe-resolver/README.md)\n  `we1.py` (2026-09-26, 4/4, md5 `5680857b…`) covers `WE-1`'s order and read site.\n  - Through the real recipe resolver `BattleFormula_ResolveTargetResult` (its contract is\n    [`CONTRACT-weapon-recipes.md`](CONTRACT-weapon-recipes.md)), recipes 7, 63, 83, 105 and 106 run step 94 (`0038B220`) immediately\n    before step 95 (`0038B6A0`), and both read the action row's `+0x13`.\n  - The planted row carries only `+0x08`, so that byte is 0 and no element rule fires on this path. The\n    composition of the two stages is not executed.\n- [`s22-opus-replay-severe-weather-gate`](../_index/candidates/s22-opus-replay-severe-weather-gate/README.md)\n  (2026-09-26, md5 `867bbaf3…`) asserts `WE-3`'s consumer side: `00263E20` returns `[02099DAC]` verbatim\n  for 0, 1, 2 and 5.\n\n**Static only:** the banding boundaries (`WE-3`, which belong to the publisher) and whether `WE-4`'s\nasymmetry is deliberate (§14). Nothing here has been observed in a running game."),
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
