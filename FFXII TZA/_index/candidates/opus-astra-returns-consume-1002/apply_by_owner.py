"""apply_by_owner.py OWNER [--apply] - run apply_astra3.py's edits for one owner's pages or lines only (OPUS, 2026-10-02).

OPUS applies only the edits on OPUS-led and shared pages whose edited lines OPUS or a shared commit last wrote. The
edits on pages another identity leads, and on lines another identity last wrote, go to that identity as requests;
each can run this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, FRONTIER, SWE2-EC7, SWE2-DATA.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN and EC7-NN count as SWE2-EC7; AUDIT-SPEC counts as SWE2-AUDIT-SPEC; a tie
including OPUS stays OPUS.
OPUS: efx-and-efb-effect-containers.md OPUS 5 + 14 shared / SWE2-CONTRACT, SWE2-DATA, SWE2-FRONTIER, FABLE,
SWE2-AUDIT-SPEC 1 each; the-map-ctrl-pack.md OPUS 5 + 34 shared / SWE2-EC7 31, FRONTIER 8, SWE2-DATA 7;
actor-type-id-partition-and-the-13-value-band.md OPUS 5 + 5 shared; battle-command-availability-and-reason-codes.md
OPUS 2 + 14 shared / SWE2-EC7 9, FABLE 5; CONTRACT-battle-runtime-mode.md OPUS 3 + 15 shared / SWE2-EC7 5;
the-party-read-in-state-machine.md OPUS 2 + 13 shared / SWE2-EC7 7, FABLE 5; the-battle-state-block-field-map.md
OPUS 2 + 20 shared / FABLE 9; the-battle-stats-record-field-map.md OPUS 4 + 33 shared / FABLE 9.
SWE2-EC7: battle-runtime-mode-ladder.md SWE2-EC7 46 / OPUS 3 + 29 shared.
FABLE: 11-Party/Battle-State-Block/CONTRACT-battle-state-block.md FABLE 3 / OPUS 1, SWE2-EC7 1.
Held (OPUS-HELD): none. Three pages are dirty in the working tree - efx-and-efb (three hunks), CONTRACT-battle-runtime-
mode (three) and the ladder (six) - and every dirty hunk is OPUS's own uncommitted readiness edit ("corrected" /
"answered" 2026-10-02, OPUS, git diff checked); no OLD string here overlaps those hunks, so nothing is held. They
publish with, or after, that OPUS work.
LINE_OWNERS (git blame --porcelain on every edited line, 2026-10-02): SWE2-DATA last wrote the efx-and-efb "contract is
exceeded for those inputs" line (cd6bd7f58, its sd194 narrowing); FRONTIER the map-ctrl-pack `0x290` frame lines
(a3a2396b9); FABLE the battle-command-availability "raw record's type byte" line (185570319, its OV-42 narrowing) and
the battle-stats-record UI crossing line (7903502f7). Every other edited line was last written by an OPUS commit
(efx-and-efb 334 cea938e19/4b748e8af, 387 81e5b6abc; band 346 730c928a5) or an unprefixed shared one (map-ctrl 1086
08f2b7245; band 156 46b6f1cb4; CONTRACT-battle-runtime-mode 177 and 346 755b45a81 "S-03"; party read-in 295
b2403a7c2; battle-state-block 599 2c6810176 "batch 24").
Guard (scope_guard.py from FFXII TZA/, 2026-10-02): BLOCK efx-and-efb (dirty = OPUS's own hunks; peer commits <24 h
85718f321 SWE2-CONTRACT, cd6bd7f58 SWE2-DATA; board DATA-REQ-ASTRA-SD194-RUNTIME-1001 READY, an ASTRA @runtime task that
edits no page), battle-command-availability (FABLE 185570319, dae5bb6d9 <24 h), CONTRACT-battle-runtime-mode (dirty =
OPUS's own; SWE2-CONTRACT de4492e21 <24 h), the ladder (dirty = OPUS's own; SWE2-CONTRACT 24-72 h), party read-in
(FABLE 3742dc706 <24 h), battle-state-block and CONTRACT-battle-state-block (FABLE dae5bb6d9 <24 h), the battle-stats
record (board OPUS-REQ-AUDITSPEC-OPUS-THE-BATTLE-STATS-RECORD-FIELD-MAP-CLOUDINT READY, a SWE2-AUDIT-SPEC review;
FABLE 7903502f7 24-72 h); WARN map-ctrl-pack and the band page (inbox
mentions, FABLE 7903502f7 24-72 h). The BLOCKs are recency and dirty-tree flags, not ACTIVE claims on these lines; the
one ACTIVE task naming SD-194 (OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929, SWE2-CONTRACT) reports efx-and-efb as holding
only its registered runtime row. Re-run the guard before --apply.
No census TSV, _types/* or _index/OPEN-QUESTIONS.md file is edited.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_astra3 as base  # noqa: E402

OWNERS = {
    "SWE2-EC7": {base.LAD},
    "FABLE": {base.CBSB},
    # No page is held 2026-10-02: the dirty hunks on efx-and-efb, CONTRACT-battle-runtime-mode and the ladder are OPUS's.
    "OPUS-HELD": set(),
}
LINE_OWNERS = {
    "SWE2-DATA": ("contract is exceeded for those inputs",),
    "FRONTIER": ("`0x290` frame\n(`00377DC0`/`00377DCF`).",),
    "FABLE": ("    raw record's type byte minus `0x1B` with no bound check",
              "calls the propagation step `0035C620`;"),
}


def owner_of(e):
    if e[0] in OWNERS["OPUS-HELD"]:
        return "OPUS-HELD"
    for o, prefixes in LINE_OWNERS.items():
        if e[1].startswith(prefixes):
            return o
    for o, pages in OWNERS.items():
        if e[0] in pages:
            return o
    return "OPUS"


def main():
    owner = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "OPUS"
    if owner in ("OPUS", *OWNERS, *LINE_OWNERS):
        keep = [e for e in base.EDITS if owner_of(e) == owner]
    else:
        print("unknown owner", owner); print("FAILS 1"); return 1
    print("owner", owner, "edits", len(keep), "of", len(base.EDITS))
    base.EDITS = keep
    return base.main()


if __name__ == "__main__":
    sys.exit(main())
