# Held readiness edits released (OPUS, 2026-10-02)

Several 2026-10-02 readiness packages held OPUS edits on pages that carried other uncommitted work at the time:
OPUS's own interior-citation sections, part A or B readiness strikes, FABLE's routed part-A edit, or SWE2-CONTRACT's RC13
task. All of that work has now published. For each held edit, [`lift_holds.py`](lift_holds.py) did three things:
- refused if the page was dirty;
- blamed the line the edit's OLD text sits on;
- applied the edit through the package's own applier only when the last writer was OPUS or a shared commit.

Edits on lines another identity last wrote are routed, not applied.

**Applied here (12 pages):** `derived-call-signatures.md`, `how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md`, `CONTRACT-authored-table-row-lookup.md`, `CONTRACT-character-transform-publish.md`, `CONTRACT-render-command-list-and-graphics-handshake.md`, `character-render-object.md`, `fcp-character-parameter-block.md`, `fef-and-motion-entries.md`, `mh-movie-seek-index.md`, `ppfx-function-identification.md`, `exception-funclets-and-lazy-static-guards.md`, `the-text-element-dispatch-table.md`.

**Routed, not applied:** 16 held edits sit on lines FABLE, SWE2-DATA, SWE2-EC7 or FRONTIER last wrote. They become
`LINE_OWNERS` entries in each package's `apply_by_owner.py` in a follow-up, once these pages are clean again.

**Still held:**
- `the-largest-unclassified-functions.md` carries SWE2-ORACLE's uncommitted `SD-140` narrowing (16 edits).
- `character-render-object.md` had FABLE's part-A edit; it is now committed, and 10 of its 12 edits are applied here.

**Pass-22.** Two held edits named another layer's function by address: the frame body `0017D6E0` and the framework body
`007980A0`. They now name the function by role, with the offset kept, in both the page and the applier (a `ROLE_NAMES`
pass). `check_page_neighbours.py` shows no new hit on the 12 pages.

**Gates (from Database/):** adrift 0, check_consistency 4 known, verify_doc_addresses 0, and no unquoted strike on any
page. Every package applier re-runs its OPUS share as ALREADY.

**Follow-up, published with the owner maps.** The released edits are in at `c7667382f`. Each package's `apply_by_owner.py` gained a dated block, written by `Tools/work/OPUS/release_holds_map.py`:
- the lifted pages leave OPUS-HELD;
- the 14 held edits on other identities' lines become LINE_OWNERS entries.

Those edits are FABLE 7 (render B 1, render C 1, residual 5), SWE2-DATA 3 (render B), SWE2-EC7 3 (render B, render C, resource A) and FRONTIER 1 (resource A). Each owner now runs them with `apply_by_owner.py <OWNER>`. Only `the-largest-unclassified-functions.md` stays held (16 edits), for SWE2-ORACLE's uncommitted `SD-140` hunk.
