"""apply_by_owner.py OWNER [--apply] - run apply_06movement.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another lane leads go to that lane as requests; each lane can run this script with its own name. OWNER is one
of OPUS, SWE2-EC7, FABLE, SWE2-DATA.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02; unprefixed subjects are
shared and do not lead; SWE2-EC7-NN task subjects count as the SWE2-EC7 lane, SWE2-FRONTIER as FRONTIER; a tie that
includes OPUS stays with OPUS, as shared pages do):
CONTRACT-facing-and-steering.md SWE2-EC7 14 / SWE2-CONTRACT 5 / FABLE 3 / OPUS 1 / FRONTIER 1;
heading-speed-to-position-delta.md SWE2-EC7 17 / FABLE 4 / OPUS 2 / FRONTIER 2;
the-movement-body-pool-and-the-separation-pass.md SWE2-EC7 12 / OPUS 3 / FABLE 2 / FRONTIER 1;
Facing-And-Steering/how-a-character-turns.md SWE2-EC7 6 / OPUS 2 / SWE2-CONTRACT 1;
Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md SWE2-EC7 12 / SWE2-DATA 3 /
OPUS 2 / FABLE 2 / FRONTIER 2 / SWE2-AUDIT-SPEC 1 / SWE2-AUDIT-SEM 1;
how-a-unit-finds-its-way-across-the-navigation-mesh.md FABLE 8 / OPUS 2 / SWE2-AUDIT-SPEC 1 / SWE2-STRUCT 1 /
SWE2-EC7 1; CONTRACT-navigation-search-and-follow.md FABLE 2 / OPUS 1; CONTRACT-separation-pass.md FABLE 4 / OPUS 1;
README.md FABLE 2 (4 shared);
clamping-a-point-into-a-volume.md SWE2-DATA 4 / OPUS 2 / SWE2-AUDIT-SPEC 1 / FABLE 1 / SWE2-AUDIT-SEM 1;
OPUS: CONTRACT-corridor-query-family.md OPUS 9; CONTRACT-heading-speed-to-position-delta.md OPUS 14 / FABLE 3 /
SWE2-CONTRACT 1; CONTRACT-movement-body-pool.md OPUS 1 (9 shared); ties with OPUS:
CONTRACT-battle-locomotion-turn-limiter.md OPUS 1 / FABLE 1; the-unit-shape-distance-primitives.md OPUS 2 /
SWE2-DATA 2; Battle-Locomotion/battle-locomotion-steering-and-recovery.md OPUS 2 / SWE2-DATA 2 / FABLE 2;
Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md OPUS 3 / SWE2-DATA 3;
how-an-animation-moves-and-turns-a-character-toward-its-target.md OPUS 1 / FABLE 1 / SWE2-AUDIT-SPEC 1;
Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md OPUS 1 / FABLE 1 / FRONTIER 1.
Lines on OPUS-led pages whose last writer is another lane (git blame --porcelain, 2026-10-02) go to that lane
(LINE_OWNERS): FABLE wrote the turn limiter contract's BL-6 line ("FABLE: contract for the battle locomotion turn
limiter") and the animation page's section 4 window lines and its switch sentence in section 6 ("FABLE: how an animation
moves and turns a character toward its target"); SWE2-DATA wrote the shape page's D5A0 code line ("SWE2-DATA: DD owner
read batch 5"). Every other edited line on an OPUS-led page was last written by OPUS or by an unprefixed commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_06movement as base  # noqa: E402

F = "06-Movement-And-Navigation/"
OWNERS = {
    "SWE2-EC7": {
        F + "CONTRACT-facing-and-steering.md",
        F + "heading-speed-to-position-delta.md",
        F + "the-movement-body-pool-and-the-separation-pass.md",
        F + "Facing-And-Steering/how-a-character-turns.md",
        F + "Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md",
    },
    "FABLE": {
        F + "how-a-unit-finds-its-way-across-the-navigation-mesh.md",
        F + "CONTRACT-navigation-search-and-follow.md",
        F + "CONTRACT-separation-pass.md",
        F + "README.md",
    },
    "SWE2-DATA": {
        F + "clamping-a-point-into-a-volume.md",
    },
}
LINE_OWNERS = {
    "FABLE": (
        "**BL-6 — Arrival SNAPS, and the snap is what clears the loop.**",
        "- the frame counter `+4` goes up; past `duration`",
        "- **while the counter is below `moveFrames`**",
        "- **while it is below `turnFrames`**",
        "- Two global switches and a per-list enable",
    ),
    "SWE2-DATA": ("ellA = A1D30(DA730(capA, posB, posA))",),
}


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
