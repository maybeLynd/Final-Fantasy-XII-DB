"""apply_by_owner.py OWNER [--apply] - run apply_02resource_b.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, FRONTIER, SWE2-EC7, SWE2-CONTRACT, SWE2-DATA,
SWE2-FRONTIER.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN and EC7-NN count as SWE2-EC7; a tie including OPUS stays OPUS.
OPUS: README.md OPUS 2 + 5 shared / FRONTIER 1; authored-data-table-registry.md OPUS 12 + 27 shared / FABLE 9;
CONTRACT-authored-table-row-lookup.md OPUS 13 + 30 shared / SWE2-EC7 14; authored-reference-lifetime-evidence.md
OPUS 4 + 23 shared / FRONTIER 5; resource-section-addressing.md OPUS 6 + 18 shared / SWE2-EC7 17;
CONTRACT-resource-entry-tree.md OPUS 6 + 8 shared / SWE2-EC7 2; a-typed-list-measured-once-and-built-in-one-allocation.md
OPUS 3 + 13 shared / SWE2-CONTRACT 4; the-resource-request-queue.md OPUS 7 + 25 shared / FABLE 6, FRONTIER 6;
Authored-Expressions/CONTRACT-authored-expression-evaluation.md OPUS 1 + 4 shared / SWE2-EC7 1;
Loose-Files-And-Size-Tables/file-size-tables-fst.md OPUS 5 + 8 shared / SWE2-EC7 12;
Standard-Formats/shipped-standard-formats.md OPUS 2 + 7 shared / FABLE 4; Prefetch-And-Json-Data/README.md 0 + 2 shared;
Prefetch-And-Json-Data/ah-asset-header-manifests.md OPUS 2 + 7 shared / SWE2-EC7 5;
VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md OPUS 4 + 26 shared / FABLE 6;
VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md OPUS 3 + 4 shared / SWE2-CONTRACT 3;
VBF-Archive-And-Authored-Tables/the-dat-and-bin-extension-buckets.md 0 + 3 shared / SWE2-DATA 2;
St2e-Carriers/README.md OPUS 1 + 2 shared; St2e-Carriers/area-nmb-index.md OPUS 1 + 11 shared / SWE2-CONTRACT 3;
St2e-Carriers/battle-text-banks.md OPUS 3 + 19 shared / SWE2-EC7 16; St2e-Carriers/how-the-ard-loader-binds-area-
battle-data.md OPUS 2 + 18 shared / SWE2-EC7 7; PS2-Image-Data-Formats/README.md OPUS 1 + 6 shared;
PS2-Image-Data-Formats/amap-menumap-area-table.md OPUS 1 / SWE2-AUDIT-SPEC 1, SWE2-FRONTIER 1, SWE2-DATA 1 (tie, stays
OPUS); unnamed-bin-families.md OPUS 2 + 8 shared / SWE2-DATA 3; five-small-bin-tables.md OPUS 6 + 11 shared / FABLE 4;
himg-handbook-image-bundles.md 0 + 5 shared / SWE2-FRONTIER 2; lst-menuquest-list.md OPUS 2 + 2 shared /
SWE2-CONTRACT 3; binmenu-guest-face-and-map-effect-images.md 0 + 6 shared / SWE2-DATA 3; chse-character-se-tables.md
OPUS 3 + 5 shared / SWE2-CONTRACT 2; gmap-menumap-guide-texts.md OPUS 1 / SWE2-AUDIT-SPEC 1, SWE2-DATA 1 (tie, stays
OPUS); lmap-menumap-location-graph.md OPUS 5 + 16 shared / SWE2-CONTRACT 4; sloc-menumap-container.md OPUS 2 + 5 shared
/ SWE2-CONTRACT 1; wmap-menumap-world-map-graph.md OPUS 2 + 3 shared / SWE2-FRONTIER 1, SWE2-DATA 1, FABLE 1,
FRONTIER 1; tim2-images-and-the-seven-slot-registry.md OPUS 2 + 7 shared / SWE2-EC7 5;
cmap-menumap-common-sublocation-directory.md OPUS 3 + 3 shared / SWE2-FRONTIER 1, SWE2-DATA 1, FABLE 1, FRONTIER 1.
FABLE: CONTRACT-ard-area-binder.md FABLE 4 / OPUS 3 (OPUS's interior-citation section published at 6201f4be2).
SWE2-EC7: Authored-Expressions/how-an-authored-number-gets-its-randomness.md SWE2-EC7 29 / OPUS 3 + 19 shared;
Prefetch-And-Json-Data/ta-texture-animation-lists.md 41 / OPUS 2 + 11 shared; PS2-Image-Data-Formats/loader-bound-bin-
families.md 38 / OPUS 2 + 5 shared; the-external-source-owner-and-borrowed-view-lifetime.md 10 / OPUS 1 + 1 shared;
Prefetch-And-Json-Data/how-the-prefetch-manifests-are-read.md 13 / OPUS 1 + 6 shared.
SWE2-CONTRACT: PS2-Image-Data-Formats/btm-exfont-bitmaps.md 6 / OPUS 1 + 2 shared; cl2-menu-colour-tables.md 6 /
OPUS 1 + 2 shared; the-resource-owner-from-copy-or-borrow-to-disposal.md 6 / OPUS 1 + 1 shared (part A's routed edits
published at f06980e06; the OLD string here does not overlap them).
SWE2-DATA: PS2-Image-Data-Formats/hchk-hctg-hdat-handbook-indexes.md SWE2-DATA 9 / OPUS 0 + 3 shared.
FRONTIER: the-indexed-source-request-from-arm-to-terminal-pump.md FRONTIER 2 / OPUS 1 + 0 shared.
SWE2-FRONTIER: the-nonempty-prf-registration-and-specialized-relocation.md SWE2-FRONTIER 3 / OPUS 1; and the three
overlay carriers in overlay-drop-census-2026-09-25.tsv (scope_guard.py 2026-10-02): CONTRACT-efx-source-rebase.md
(OPUS 9 + 14 shared / SWE2-EC7 23, a tie that would stay OPUS), CONTRACT-resource-input-ownership.md (0 + 2 shared /
SWE2-FRONTIER 2, a tie that would stay OPUS) and CONTRACT-resource-request-queue.md (OPUS 1 + 6 shared / SWE2-FRONTIER 2).
Held (OPUS-HELD): none. sloc-menumap-container.md and cmap-menumap-common-sublocation-directory.md are dirty in the
working tree with OPUS's own uncommitted interior-citation / neighbour sections only (at their ends); no OLD string here
overlaps them (sloc §1 corpus row, §2.1 heading and §8 related line; cmap §4 struct line), so they stay OPUS.
No other lane's ACTIVE task edits an OPUS page here: OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929 (SWE2-CONTRACT) and
ORACLE-REQ-AUDITSPEC-SD7-REVIEW-1002 (SWE2-AUDIT-SPEC) reach the three READMEs only through the README basename
collision (dd-owner-read-0929/README.md and sd7-stored-app-pointer-0930/README.md); the other board entries the guard
names are READY or BLOCKED, and the peer commits it lists are finished sweeps.
Guard on the OPUS pages (scope_guard.py, 2026-10-02): CLEAR the expression contract and the entry-tree contract; WARN
ah, amap, unnamed-bin, five-small, himg, binmenu, gmap, wmap, the VBF page, fst, the row-lookup contract, the buckets
page and tim2 (peer commits 24-72 h or inbox mentions); BLOCK the loader, nmb, battle-text-banks, registry, typed-list,
standard-formats, lst, chse, lmap, queue, section-addressing, lifetime-evidence and bigfile pages (finished sweeps
de4492e21 / d0809ac13 / 0d1334a84 under 24 h, BLOCKED ASTRA runtime requests, a READY SWE2-STRUCT request), the three
READMEs (basename collision) and sloc / cmap (dirty with OPUS's own sections, above). None of those is a hold reason.
Re-run the guard before --apply.
No census TSV is edited (members/atlas-name-census.tsv regenerates byte-identical from the shipped VBF; the typed-list
prose is corrected to it).
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led pages): SWE2-EC7 last wrote the standard-formats
page's `002DF980` hub line (3460e7b7b), the `.ah` page's `0019EB60` enlist line (e4950fd34) and the fst page's
`001D6FB0` neighbour line (670e2fc40); SWE2-DATA the amap request-size row, the five-small-tables superseded note and
the gmap corpus_validated line (bafa49c9f) and the buckets page's two "six token families" lines (81278ca35); FABLE the
unnamed-bin `_name` tables line (347566aa4) and lmap's two menumap_sub size lines (2c8b1c81a); FRONTIER the chse
`002E60F0` subtree line (3668e438d). Every other edited line on those pages was last written by an OPUS or an
unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import apply_02resource_b as base  # noqa: E402

F = "02-Resource-And-Asset-Pipeline/"
P = F + "PS2-Image-Data-Formats/"
J = F + "Prefetch-And-Json-Data/"
OWNERS = {
    "FABLE": {
        F + "CONTRACT-ard-area-binder.md",
    },
    "SWE2-EC7": {
        F + "Authored-Expressions/how-an-authored-number-gets-its-randomness.md",
        J + "ta-texture-animation-lists.md",
        P + "loader-bound-bin-families.md",
        F + "the-external-source-owner-and-borrowed-view-lifetime.md",
        J + "how-the-prefetch-manifests-are-read.md",
    },
    "SWE2-CONTRACT": {
        P + "btm-exfont-bitmaps.md",
        P + "cl2-menu-colour-tables.md",
        F + "the-resource-owner-from-copy-or-borrow-to-disposal.md",
    },
    "SWE2-DATA": {
        P + "hchk-hctg-hdat-handbook-indexes.md",
    },
    "FRONTIER": {
        F + "the-indexed-source-request-from-arm-to-terminal-pump.md",
    },
    # Led page plus the three overlay carriers (overlay-drop-census-2026-09-25.tsv; scope_guard.py 2026-10-02).
    "SWE2-FRONTIER": {
        F + "the-nonempty-prf-registration-and-specialized-relocation.md",
        F + "CONTRACT-efx-source-rebase.md",
        F + "CONTRACT-resource-input-ownership.md",
        F + "CONTRACT-resource-request-queue.md",
    },
    # No page is held this time (sloc and cmap carry only OPUS's own uncommitted end sections, not overlapped);
    # kept so the call shape matches other folders.
    "OPUS-HELD": set(),
}
LINE_OWNERS = {
    "SWE2-EC7": ("`002DF980` — 22 B, 34 callers;",
                 "`+0x120` self-links,",
                 "The `001D6FB0` read-item constructor's alloc/enqueue"),
    "SWE2-DATA": ("| request size | `.fst` kind 7 id `0xA5`",
                  "*Superseded 2026-09-29 (below): `dP<d`",
                  "corpus_validated: \"all 35 menumap_guide",
                  "units, six token families no document names",
                  "- **Not settled:** `.bin`'s families."),
    "FABLE": ("      - **The two `_name` tables**",
              "\"double buffer\" or 512 KB",
              "4–11 MB, every one above"),
    "FRONTIER": ("`002E60F0` (~62 B)",),
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
