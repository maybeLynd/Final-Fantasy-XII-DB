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
PAGE = '08-Combat-Formula/CONTRACT-formula-step-table.md'   # repo-relative path under Database/FFXII TZA/
EDITS = [
    ('E1 section 3 types fence: the three words are one channel, not the only one',
     'the shared scratch record — the ONLY channel between steps (ST-4)',
     'three words (+0x9C/+0xA0/+0xA4) of the shared scratch record BattleFormulaScratch 02AEDFB8 (0xA8): the preparation-to-finalize channel, one of 15 cross-step cells of the block, not the only one (ST-4)'),
    ('E2 ST-4 lead: the channel is the whole scratch block',
     '**ST-4 — The steps share NO arguments and NO return values; they communicate only through the\nscratch record, so the ORDER in the recipe is the semantics.**',
     '**ST-4 — No step hands an argument or a return value to the next: the loop reloads the same three\narguments before every call (`003863C5`–`003863CD`) and never reads `rax`. The steps communicate through\nthe shared scratch record, which is the whole `BattleFormulaScratch` block (`02AEDFB8`, 0xA8) and not only\nits three words `02AEE054`/`58`/`5C`, so the ORDER in the recipe is the semantics.** In the 152 target\nbodies themselves (callees not followed), 15 cells of the block are written by one step and read by a\ndifferent step, and 12 of them lie outside the three words. For example, slot 21 (`00388F20`) writes the\nhit chance `02AEDFE0` (`+0x28`) at `00388F37` and `00388FA1`. Slot 40 (`00389670`) compares that cell with\nits draw at `0038968D` and, on a miss, sets `02AEDFB8` (`003896A0`), which ends the recipe at `003863D7`.\nNo cell outside the block passes between step bodies.'),
    ('E3 section 5: the cross-operation state is the block',
     'the three scratch words (`ST-4`)',
     'the `BattleFormulaScratch` block `02AEDFB8` (0xA8). It holds the three words `02AEE054`/`58`/`5C` between preparation and finalize, and further cells such as the hit chance `02AEDFE0` and the stop flag `02AEDFB8` (`ST-4`)'),
    ('E4 section 7: no return path; the block is the channel',
     'There is no\nother channel and no return path (`ST-4`).',
     'There is no\nreturn path. The channel is the scratch block, and a step that leaves `02AEDFB8 == 1` ends the list at\n`003863D7` (`ST-4`).'),
    ('E5 section 13: three native replays execute this dispatch',
     "**None.** No experiment executes this dispatch. S-22's runtime cell is not addressed by this\ncontract. *Stated rather than left blank so a CONTRACT READY header is not read as evidence of\nexecution.*",
     "**Isolated native replay, not a running game.** Evidence class NATIVE-REPLAY (unicorn), `live_game: false`:\nthe shipped bytes run at their own addresses, with no application stub and planted data only. Three OPUS\npackages execute this dispatch. FABLE re-ran all of them on 2026-10-03 under unicorn 2.1.4, and every\n`result.json` reproduced byte-identically.\n\n- [`s22-opus-replay-steps-and-element-scaling`](../_index/candidates/s22-opus-replay-steps-and-element-scaling/README.md)\n  (2026-09-25, 9/9; `result.json` md5 `99336e05…`):\n  - §12's table facts, read from the mapped image (`ST-1`, `ST-2`, `ST-3`, `ST-5`; these are static by nature).\n  - All 42 no-op ids executed, and none writes anything (`ST-3`).\n  - Id 65 then id 113, called through `stepTable[id]`. The preparation writes exactly `02AEE054`/`58`/`5C`\n    and draws the shared MT19937 once (`ST-7`). The finalize writes `trunc((058 − 05C) × 054)`; that is\n    `ST-4`'s three-word part.\n  - Ids 113 and 125 run one body (`ST-5`).\n- [`s22-opus-replay-recipe-resolver`](../_index/candidates/s22-opus-replay-recipe-resolver/README.md)\n  (2026-09-25, md5 `a226db98…`) and its `we1.py` (2026-09-26, 4/4, md5 `5680857b…`):\n  - Steps are called by the real loop (`003863D0`) on shipped recipes 2, 4, 5, 6, 39, 74 and 90, and on\n    the seven dual-stage recipes.\n  - The loop stopping on `02AEDFB8 == 1` is recorded, not asserted.\n- [`s22-opus-replay-severe-weather-gate`](../_index/candidates/s22-opus-replay-severe-weather-gate/README.md)\n  (2026-09-26, 5/5, md5 `867bbaf3…`): steps 35 and 36 scale the hit chance `02AEDFE0` by 0.8 and 0.5.\n\n**What is static, or executed only in isolation.**\n- `ST-4` as corrected on 2026-10-03: none of the three packages asserts a hand-off through a block cell\n  outside the three words. Recipe 14 (`[21, 31, 32, 40]`, run by `we1.py`) does run slot 21 before slot 40,\n  but the run records only the slot list.\n- [`check_s22.py`](../_index/candidates/fable-l2exp-s22-1003/check_s22.py) executes that hand-off\n  directly. With the three words equal, slot 40 ends the recipe when it runs alone and does not when slot 21\n  ran first.\n- The 15-cell figure is an own-body census; callees are not followed.\n- `ST-6` (no shipped user) is a corpus fact.\n- These packages do not pin unicorn (SWE2-AUDIT-SPEC's L2 expansion, item 5).\n\nNothing here has been observed in a running game."),
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
