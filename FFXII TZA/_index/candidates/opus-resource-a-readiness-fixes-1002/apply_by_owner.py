"""apply_by_owner.py OWNER [--apply] - run apply_02resource_a.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, FRONTIER, SWE2-EC7, SWE2-CONTRACT, SWE2-STRUCT,
SWE2-FRONTIER.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN and EC7-NN count as SWE2-EC7; a tie including OPUS stays OPUS.
OPUS: Loose-Files-And-Size-Tables/file-size-tables-fst.md OPUS 4 + 8 shared / SWE2-EC7 12 (tie, stays OPUS);
the-resource-request-queue.md OPUS 6 + 25 shared / FABLE 6, FRONTIER 6; resource-section-addressing.md OPUS 5 + 18
shared / SWE2-EC7 17; authored-reference-lifetime-evidence.md OPUS 3 + 23 shared / FRONTIER 5;
CONTRACT-resource-section-addressing.md OPUS 2 + 1 shared / SWE2-EC7 1, FABLE 1; authored-data-table-registry.md
OPUS 11 + 27 shared / FABLE 8; README.md OPUS 1 + 5 shared / FRONTIER 1; VBF-Archive-And-Authored-Tables/
vbf-archive-and-st2e-tables.md OPUS 3 + 26 shared / FABLE 6; St2e-Carriers/README.md 0 + 2 shared;
St2e-Carriers/battle-text-banks.md OPUS 2 + 19 shared / SWE2-EC7 16; how-the-bigfile-index-loads-and-is-verified.md
OPUS 3 + 4 shared / SWE2-CONTRACT 3.
SWE2-EC7: the-external-source-owner-and-borrowed-view-lifetime.md SWE2-EC7 10 / OPUS 1 + 1 shared.
SWE2-CONTRACT: the-resource-owner-from-copy-or-borrow-to-disposal.md SWE2-CONTRACT 4 / OPUS 1 + 1 shared.
FABLE: how-a-path-is-resolved-to-bytes.md FABLE 4 / OPUS 2 + 1 shared.
SWE2-FRONTIER: CONTRACT-efx-source-rebase.md (OPUS 9 + 14 shared / SWE2-EC7 23, a tie that would stay OPUS) is an
overlay carrier in overlay-drop-census-2026-09-25.tsv (scope_guard.py 2026-10-02), so its six edits go to SWE2-FRONTIER.
Held (OPUS-HELD): CONTRACT-resource-entry-tree.md (OPUS 5 + 8 shared) and CONTRACT-authored-table-row-lookup.md
(OPUS 12 + 30 shared / SWE2-EC7 14) are dirty in the working tree with OPUS's own uncommitted "Interior citations for
the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)" sections only. Their 13 edits wait until that work
publishes; no OLD string here overlaps those sections. On the held pages two edited lines were last written by other
identities, and those edits go to them once the hold lifts: SWE2-EC7 the entry-tree "027A2E10 flag" line (cfd5e9a57);
FRONTIER the row-lookup "0036BC60 (~179 B)" line (a3a2396b9).
No other lane's ACTIVE task edits an OPUS page here: OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929 and
SWE2CONTRACT-PUB-B21Z4-1002 (SWE2-CONTRACT) reach the two READMEs only through the README basename collision
(dd-owner-read-0929/README.md, a bare "README"); the ASTRA tasks naming the queue page (FABLE-REQ-ASTRA-EO3-PATH-POINTER)
and the registry and lifetime-evidence pages (OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME) are BLOCKED runtime requests, not
edits in progress.
Guard on the OPUS pages (scope_guard.py, 2026-10-02): CLEAR CONTRACT-resource-section-addressing.md; WARN the fst page
(peer commits 24-72 h, 69b8ed680 / ac4d7d901) and the VBF page (02d59b826 / 01c2429f6); BLOCK the queue page (the
BLOCKED ASTRA task above; finished sweeps d0809ac13, de4492e21), resource-section-addressing.md, battle-text-banks.md
and the bigfile page (finished sweep de4492e21), the lifetime-evidence and registry pages (the BLOCKED ASTRA task;
de4492e21 on the registry), and the two READMEs (basename collision). None of those is a hold reason. Re-run the guard
before --apply.
No census TSV is edited.
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led pages that are not held): SWE2-EC7 last wrote
the fst page's 0046DD50 line (f2f8eff33) and 002DF6C0 line (02cc89e7e), the queue page's 0032E040 hub line
(6d4e5224b), the section-addressing contract's 00409780 line (577806707) and the registry's 0037C2E0 line (2886cda60);
FRONTIER the queue page's 003EADE0 subtree line (04dc361cf) and resource-section-addressing.md's 00409780 subtree line
(220aa0449); FABLE resource-section-addressing.md's two J-4 lines (7654a3a9a) and the registry's AG-2 band-ruling lines
"34 lea" and "63 separately-named globals" (ecd3a9b2a); SWE2-STRUCT the registry's 0x02EBF198 lines - the AG-4
"NARROWED" bullet, the upper-slot table row, the "image-initial values" line, the disposition lead, the "Initialised in
the image" bullet, the "38 slot addresses" line and the "Bounded claim" bullet (0e8004f68); SWE2-FRONTIER the bigfile
page's 001F3FD0 and 001F4720 member rows (0cdb6009a). Every other edited line on those pages was last written by an
OPUS or an unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import apply_02resource_a as base  # noqa: E402

F = "02-Resource-And-Asset-Pipeline/"
OWNERS = {
    "FABLE": {
        F + "VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md",
    },
    "SWE2-EC7": {
        F + "the-external-source-owner-and-borrowed-view-lifetime.md",
    },
    "SWE2-CONTRACT": {
        F + "the-resource-owner-from-copy-or-borrow-to-disposal.md",
    },
    # Held 2026-10-02 (OPUS): dirty with OPUS's own uncommitted interior-citation sections; apply after those publish
    # (the line owners named in the docstring then take their lines).
    "OPUS-HELD": {
        F + "CONTRACT-resource-entry-tree.md",
        F + "CONTRACT-authored-table-row-lookup.md",
    },
    # Overlay carrier (overlay-drop-census-2026-09-25.tsv; scope_guard.py 2026-10-02).
    "SWE2-FRONTIER": {
        F + "CONTRACT-efx-source-rebase.md",
    },
}
LINE_OWNERS = {
    "SWE2-EC7": ("after the `0016D6A0` fill, state 4 gates on `0053DD10`",
                 "is the gated submit-or-decline wrapper `0032E070` runs per request:",
                 "`0032E040` — 38 B, 8 A-measured callers;",
                 "the first hit writes its index to `*rsi`",
                 "state `3` exits - the `4`-write"),
    "FRONTIER": ("`003EADE0` (512 B) — the request state machine",
                 "`00409780` (`ResourceEntry_FindSectionIndexAndOffset`, ~101 B) —"),
    "FABLE": ("So these rows are **`0xC0`",
              "`0x50` family (root `+0x000`) is a different descriptor",
              "contains **34 `lea <slot>`",
              "> fields; the band is 63 separately-named globals"),
    "SWE2-STRUCT": ("It is also **not** among the 38",
                    "the slot is *initialised in the image*",
                    "| `0x02EBF198` | 0 | **Initialised but never named**",
                    "read (the image-initial values below are already pointers)",
                    "Allocated and initialised, never named",
                    "- **Initialised in the image.**",
                    "- **Bounded claim.** The slot is populated"),
    "SWE2-FRONTIER": ("parent walk `[rdx+0x18]` (",
                      "| `001F4720` (176 B) | index-record accessor"),
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
