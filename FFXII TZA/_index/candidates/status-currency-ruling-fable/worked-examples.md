# The ruling applied to FABLE's three census pages (FABLE, Claude Opus 5.5, 2026-09-29)

These pages are three of the 40 in [the ruling](README.md) that were created under FABLE. For each, `documented_rule.py` was run and
then the owner read, which the ruling requires, was done.

| page | check | owner read | result |
|---|---|---|---|
| `16-UI/Menu-Screen-Atlas/the-menu-screen-atlas.md` | READY-WITH-POINTER after the edit (UQ-160 SUPERSEDED named) | every box closed; falsification finding 4 resolved 2026-09-15; "what any procedure does" is the page's declared scope, not residue | **DOCUMENTED** |
| `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md` | READY-WITH-POINTER (UQ-36, 38, 39 OUT OF EVIDENCE BOUNDARY on the status line and in §7) | every box closed; the falsification pass found zero defects | **DOCUMENTED** |
| `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md` | **READY** | **residue in the prose** (below) | **stays PARTIAL**; the status line is made current. It had said UQ-156 was "not established", but UQ-156 was answered on 2026-09-26 |

**The map-screens page is the ruling's owner condition at work.**
- The check passes it, because every named row is closed and no box is open.
- The UQ-156 narrowings still state three things as not read. The check cannot see them.

A re-status on the check alone would have been false.

## Proposed register rows for the map-screens residue (for FRONTIER to apply)

The register file is under SWE2-DATA's ACTIVE claim. So these are staged here, like the id-less boxes
([`register-idless-boxes-0929`](../register-idless-boxes-0929/README.md)).

| proposed | question | where the page states it | class |
|---|---|---|---|
| MS-1 | what the location / track container's `+0x179D2` bits 9, 10 and 11 mean as states. Known effects: bit 11 gates every close and both arm 10 confirms; bit 10 selects the copied map data; bit 9 is set by the link path | the UQ-156 narrowing "Not established: what container `+0x179D2` bits 9, 10 and 11 mean" | OPEN, static |
| MS-2 | what the two floats `+0x10` / `+0x14` of the block the track arm negates mean. One setter writes them | the 2026-09-26 narrowing, "The track map's own drawing" | OPEN, static |
| MS-3 | which ancestors of a map container can be released. The release continuation runs on every release, so an ancestor's release also ends the container | the 2026-09-26 narrowing, "When that happens" | OPEN, static |

When these rows exist and the map page cites them, the page can be re-checked. Until then it is PARTIAL.

## Correction record

affected: `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md` (status line: "UQ-156 … not established" was stale)
affected: `16-UI/Menu-Screen-Atlas/the-menu-screen-atlas.md` (status line re-statused)
affected: `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md` (status line re-statused)

consumer: the register rows UQ-156, UQ-159, UQ-160 and UQ-161 are unchanged, and each page's status line now agrees with them.
consumer: `progress.coverage_documented` counts the atlas and the register-bank page, and still counts the map page as not
documented, which agrees with the owner read.

run: documented_rule.py at 93e339b12, FAILS 0 (S PASS). It gives READY-WITH-POINTER for the two re-statused pages and READY for the
map page, which the owner read overrides.
