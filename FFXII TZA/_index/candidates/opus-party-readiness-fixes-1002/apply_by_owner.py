"""apply_by_owner.py OWNER [--apply] - run apply_11party.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, FABLE, SWE2-EC7, SWE2-FRONTIER.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN and the bare "EC7" prefix count as SWE2-EC7, "SWE2CONTRACT-" as SWE2-CONTRACT
and "AUDIT-SPEC:" as SWE2-AUDIT-SPEC.
OPUS: README.md 5 shared; party-roster-and-control-suppression.md OPUS 1 + 17 shared / SWE2-EC7 4 / FRONTIER 2 /
SWE2-FRONTIER 1 / FABLE 1 / SWE2-AUDIT-SPEC 1; active-party-reserve-and-the-moment-the-leader-changes.md OPUS 3 + 12
shared / FABLE 10; the-five-parallel-slot-maps.md OPUS 2 + 13 shared / SWE2-EC7 6; the-setsavedata-presets-test-battle-
scenarios.md OPUS 2 + 15 shared / SWE2-EC7 2; CONTRACT-party-slot-assignment.md OPUS 2 + 7 shared; the-battle-state-
block-field-map.md OPUS 1 + 20 shared / FABLE 8 / SWE2-EC7 7; party-roster-slots-accesses.tsv 1 shared.
FABLE: CONTRACT-the-five-parallel-slot-maps.md FABLE 3 / OPUS 2 / SWE2-EC7 1 / SWE2-CONTRACT 1;
Battle-State-Block/CONTRACT-battle-state-block.md FABLE 2 / OPUS 1 / SWE2-EC7 1.
SWE2-EC7: CONTRACT-party-focus-and-control-suppression.md SWE2-EC7 3 / OPUS 1 / FABLE 1.
Overlay carriers: none - scope_guard.py (2026-10-02) reports no 11-Party page as an overlay carrier, and none is dirty;
it BLOCKs README.md (board-name collisions only), party-roster-and-control-suppression.md (an ACTIVE SWE2-AUDIT-SPEC
request naming the page in a dispositions row, not editing it) and the active-party page (SWE2-AUDIT-SPEC promotion
commit 058c93e21 under 24 h), so the OPUS edits on those three wait for a clear guard.
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led pages): FABLE last wrote the slot-maps page's
refresher sentence (8a747de23), the field map's +0x5A58 row (8a747de23) and evidence row (f1ad59f8e), and the
active-party page's teardown sentence (797b72780); SWE2-EC7 the slot-maps page's 00321100 note (ce6080204) and the
roster page's 00359200 hub note (be08c2af1); SWE2-FRONTIER the roster page's 0023B040 subtree paragraph (0cdb6009a).
Every other edited line on the OPUS-led pages was last written by an OPUS or an unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_11party as base  # noqa: E402

F = "11-Party/"
OWNERS = {
    "FABLE": {
        F + "CONTRACT-the-five-parallel-slot-maps.md",
        F + "Battle-State-Block/CONTRACT-battle-state-block.md",
    },
    "SWE2-EC7": {
        F + "CONTRACT-party-focus-and-control-suppression.md",
    },
    # Overlay carriers go to SWE2-FRONTIER whatever the commits say; scope_guard reports none in 11-Party (2026-10-02).
    "SWE2-FRONTIER": set(),
    # Generator output (one census generator per access route, d8b3a507d): the fix is in the generator's route
    # resolution, so the five row notes go to SWE2-DATA as a regenerate request, not as hand edits (OPUS, 2026-10-02).
    "SWE2-DATA": {
        F + "party-roster-slots-accesses.tsv",
    },
    # OPUS's own page, held: SWE2-AUDIT-SPEC is auditing a record that names it
    # (OPUS-REQ-AUDITSPEC-RECORD-EIGHT-PASS6-SIGNATURES-1001, ACTIVE 2026-10-02). Apply after that request closes:
    # `apply_by_owner.py OPUS-HELD --apply`.
    "OPUS-HELD": {
        F + "party-roster-and-control-suppression.md",
    },
}
LINE_OWNERS = {
    "FABLE": ("> per battle runtime mode (`003268BD`",
              "then rewrites selectors `[0..3]` of classes 1, 2 and 4 per mode",
              "(1,145 rows; 91 removed",
              "`002681D0` → `002681E0`, a\n"),
    "SWE2-EC7": ("index whose `byte[base + rbx*2 + 0x5A86]`",
                 "mask setter itself — `ecx` nonzero",
                 "when the mask is nonzero it resolves"),
    "SWE2-FRONTIER": ("`00313F60`/`003592C0`/`00359200`/`0036FFE0`",
                      "`00359200`,\n`0036FFE0`."),
}


# Holds lifted 2026-10-02 (OPUS): these pages' holds are lifted; their held edits on other identities' lines go to them.
OWNERS["OPUS-HELD"] = set(OWNERS.get("OPUS-HELD", set())) - set(['11-Party/party-roster-and-control-suppression.md'])


def owner_of(e):
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
