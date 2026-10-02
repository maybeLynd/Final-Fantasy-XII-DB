"""apply_by_owner.py OWNER [--apply] - run apply_23thirdparty.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, SWE2-FRONTIER, SWE2-EC7.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN and EC7 / EC7-NN count as SWE2-EC7; FRONTIER and SWE2-FRONTIER are separate
identities; a tie including OPUS stays OPUS.
OPUS: README.md 1 + 1 shared; third-party-middleware-inventory.md 5 + 22 / FABLE 20, SWE2-EC7 12, FRONTIER 8, SWE2-DATA
1; phyre-to-bullet-rigid-body-materialization.md 3 + 10 / FABLE 4, SWE2-EC7 3; eastl-strings-containers-and-the-
logging-allocator.md 3 + 12 / SWE2-EC7 3, FABLE 2; the-vp8-codec-interface-and-its-control-map.md 2 + 9 / FRONTIER 1;
CONTRACT-lua-chunk-loader.md 3 + 7 / FABLE 3; the-lua-loader-and-what-it-accepts.md 2 + 10 / FABLE 4, SWE2-FRONTIER 2.
SWE2-EC7: yebis-ppfx-source-map.md 14 + 6 (EC7) / OPUS 7 + 10.
No overlay carrier among these pages and none is dirty (scope_guard.py, git status, 2026-10-02).
Held: none. OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929 (SWE2-CONTRACT, ACTIVE) targets the dd-owner-read-0929
worksheet's KEEP-PARTIAL pages, the inventory and the EASTL page among them, but its checkpoint (85718f321, batch 21)
says no unregistered prose residue remains in scope, and both pages have left PARTIAL (DOCUMENTED / AUDITED); the guard
names that task only through README basename collisions. Re-run the guard first.
Guard on the OPUS pages (2026-10-02): BLOCKs are the README basename collisions and SWE2-AUDIT-SPEC's finished
promotion sweep 058c93e21 (Bullet and EASTL pages); the inventory and the loader page WARN (sweeps 24-72 h, inbox
mentions); the libvpx page and the contract are CLEAR. No census TSV is edited: members/libvpx-vp8-decoder-uc1.tsv's
refs value 2 for 0016EFF0 (a misaligned byte match) is reported to SWE2-DATA instead.
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led pages): SWE2-EC7 last wrote the Bullet page's
006A0A50 paragraph (44fb9c05f, EC7-201), the EASTL front-matter string-initialiser row (fb1511935), the inventory's
libvpx UC-1 row (9e90a97ea) and MSVC runtime tail row (8428f38e4); FABLE the EASTL BS-5 narrowing (a29f77fd6), the
inventory's "libvorbis is unreached" line (aa88216bb), its libvorbis clients sentence (f75c10f85), the Tremor heading
line (7b59f70c3), the X-8 serializer-name and X-8-stays-open lines (9ec3636ef), and the Bullet page's serializer-name
line (19ba6d1f2) and 006883A0 line (8d5127b5b). Every other edited line on the OPUS-led pages was last written by an
OPUS or an unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_23thirdparty as base  # noqa: E402

F = "23-Third-Party-Libraries/"
OWNERS = {
    "SWE2-EC7": {
        F + "PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md",
    },
    # No held OPUS page and no overlay carrier at drafting (see above); kept so every owner runs and reports.
    "FABLE": set(),
    "OPUS-HELD": set(),
    "SWE2-FRONTIER": set(),
}
LINE_OWNERS = {
    "SWE2-EC7": ("`006A0A50` (249 B) is the basis-write",
                 "and stored back into `+0x160`..`+0x164` - then",
                 "and which game string each object holds. Selector:",
                 "and none reaches anything outside the span that the listed members do not.",
                 "Two members left the family on the 2026-09-17 re-sweep"),
    "FABLE": ("`EASTL vector` (`007A4D58`)",
              "libvorbis is unreached",
              "`00679600`, `00679A50`, `00679F40`; CF-2's",
              "**Tremor, 106 members",
              "`btCollisionObjectFloatData` / `btCollisionShapeData` (~~",
              "at file offsets `0x1BAC800`",
              "**X-8 stays open for those",
              "decided by whatever installs `006883A0`"),
}


def owner_of(e):
    for o, pages in OWNERS.items():
        if e[0] in pages:
            return o
    for o, prefixes in LINE_OWNERS.items():
        if e[1].startswith(prefixes):
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
