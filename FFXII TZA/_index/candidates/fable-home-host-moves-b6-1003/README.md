# FABLE: homed rows moved, dropped or narrowed for host fit, batch 6 (AUDIT-SPEC P11, P12, P14)

*Draft record, FABLE, 2026-10-03. Not applied and not published. It answers every SWE2-AUDIT-SPEC review of a FABLE
1003 homing record that is committed at HEAD, has the verdict REJECT or ACCEPT-WITH-NARROWING, and that no earlier
FABLE repair settled (b4, b4b and b5 took the steal roll and the 1002 records; `fable-empty-homed-section-1003` took
the gambit-evaluation section). That is twelve REJECTs, two narrowings of `-home-` records, and the narrowings of two
cloud F-homing records: the battle action handler table (review committed in `e8b1a961a`) and the numeric-formatting
page (review committed in `c84cc1deb`).*

*It is built on the b5 record. `move_rows.py` is that script with one new rule and four new mechanisms (next
sections).*

## FABLE headline

| measure | count |
|---|---:|
| rows moved, host documents the caller (`host: caller`) | **9** |
| rows moved through a thunk (`host: thunk`) | **1** (`00408AD0`) |
| rows narrowed in place (`edits`, strike-and-replace) | **4** (`00623D70`, `00346780`, `00346EF0`, `003CA530`) |
| rows dropped, already documented elsewhere (`already_bound_on`) | **1** (`003B6DE0`) |
| rows dropped to the frontier, the named host fails the host rule (`host_fails`) | **8** |
| rows HELD (target page modified in the shared tree) | **8** |
| `move_rows.py`, all rows, verify on the real tree | `VERIFY 18 functions, 77 anchors, 11 target pages, 4 edits, 9 drops` / `FAILS 0` ([`move_rows.all.out`](move_rows.all.out)) |
| `move_rows.py --only` (the 23 rows not held), verify on the real tree | `VERIFY 10 functions, 41 anchors, 6 target pages, 4 edits, 9 drops` / `FAILS 0` ([`move_rows.out`](move_rows.out)) |
| `--apply --root` on a clean detached `76143cef7` worktree, `--only`, twice | first pass 56 `PATCHED`, `FAILS 0`; second pass 56 `ALREADY`, `FAILS 0` ([`worktree_apply1.out`](worktree_apply1.out), [`worktree_apply2.out`](worktree_apply2.out)) |
| sensitivity controls ([`controls.py`](controls.py)) | `CONTROLS 11, NOT REFUSED 0` ([`controls.out`](controls.out)) |

## FABLE: the host rule

The reviews' common defect was a host page that only *mentioned* the caller. b5's check accepted any page on which
the address string occurred. In this batch a host must **document** the caller as a subject, outside this record's
own section (`subjects.py`):

- an address in a heading;
- the first address of a table row (the first cell in the usual address-keyed table; the first address-bearing
  cell when the key cell is a number or a name, as in the efx subtype table);
- the first address of a paragraph or list item (after any bold lead label).

For `host: callee` rows the callee must be documented in the same way. For `host: thunk` it is the thunk's callers.
Controls 1 and 2 are moves that the b5 rule passes and this rule refuses. Control 3 is a drop that names a page
where the caller is a subject, and it is refused too.

Two limits of the rule, stated so they are not mistaken for findings:

- **A crossing-list item that leads with an address counts as a subject.** The informational `LEAD` lines show
  this: `0017D940` is a subject only on the lazy-statics page (its pass-22 neighbour item, L796), and `0035C630` only
  on the vbf page (OPUS's interior row, L1302). Both pages are the hosts the reviews rejected, so neither is used here.
- **The first address of a paragraph is not always its topic.** The authored-commands page passes for `0041FCF0`
  through a paragraph whose subject is the field `word[+0x2F8]` (L449-451, "both writers agree: `0041FCF0` and
  `00420480`"). That row is HELD for another reason. FABLE marks the host as borderline, to be re-judged when the
  page is clean.

## FABLE: the rows

Page paths are below `FFXII TZA/`, shortened (`00/` = `00-Engine-Core-Runtime/`, and so on). `moves.json` has the
full paths, the evidence lines and quotes, and the anchors. Line numbers are from the shared tree at `89538d085`.

| fn | from | to / drop / edit | why | review |
|---|---|---|---|---|
| `0029D4D0` | `02/PS2-Image-Data-Formats/five-small-bin-tables.md` | `16/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md` | caller `0029E110` is the first address of the `NgSignal…` reader row (L210) and of the "one reader is the legend's host" item (L504). The review's wording "the procedure `0029D550`" replaces "the address loaded by the `lea` at `0029D4DB`" (the `lea` is checked at the bytes) | [five-small-bin-tables](../auditspec-review-fable-home-five-small-bin-tables-1003/REVIEW.md) |
| `00408AD0` | `99/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md` | `00/Battle-Frame/the-world-tick-and-the-field-frame.md` | thunk host: `003EC850` is one `jmp 00408AD0`. The page documents its callers `002628B0` (heading L529, lead L531) and `0026C8C0` (table row L179). The review's line "`003EC850` is a 5-byte thunk to `00408AD0`; `002628B0` + 0x2E4 and `0026C8C0` + 0x192 call it" leads its own bullet in the section (below) | [glyph-quads](../auditspec-review-fable-home-how-a-line-of-text-becomes-glyph-quads-1003/REVIEW.md) |
| `0027F150`, `003FF160`, `003FF9F0` | `16/License-Board-View/the-license-board-screen-widgets.md` | `16/Shared-Dialogs/the-shared-dialog-widgets.md` | caller `002C2320` leads the Items_Equipment_Shops_License SERVICE paragraph ("`002C2320` on this page calls", L243). The section lands directly after the section that holds `003FF9A0`, which stays put (the cross-record ruling) | [license-board widgets](../auditspec-review-fable-home-the-license-board-screen-widgets-1003/REVIEW.md) |
| `00420860` | `02/the-source-block-mover-and-separate-consumer-refresh.md` | `17/Character-Render-Records/the-character-render-record-array.md` | caller `00427DE0` leads the five-pass paragraph (L785) and a list item (L386). The review's replacement wording: "the floats `xmm1`, `xmm2` and `xmm3` passed through" | [source-block mover](../auditspec-review-fable-home-the-source-block-mover-and-separate-con-1003/REVIEW.md), Repair 3 |
| `004209F0` | same | same | same caller; text unchanged | same, Repair 2 |
| `00366A30` | `17/Effect-File-Formats/effect-element-type-dispatch.md` | `15/Modal-Toggles/r2-force-fight-toggle.md` | caller `00366B80` is the first cell of its key-address row (L300) | [effect-element-type-dispatch](../auditspec-review-fable-home-effect-element-type-dispatch-1003/REVIEW.md), N2 |
| `004FF230` | same | `17/Effect-File-Formats/efx-and-efb-effect-containers.md`, a section before `## 2c.` (the review: "after §2b") | caller `00537C80` is the subtype-0 row's address (L240). The page already read the body ("Each body runs `004FF230`", L246), so this is a re-cite with interior anchors, as the review says | same, N3 |
| `004FE4A0` | same | same | caller `00538350` is the subtype-2 row's address (L242) | same, N3 |
| `00623D70` | same | **edit** on its page | strike-and-replace of the clause "clears bit 31 of dword `rcx+0x18`; when the result is above 1 (unsigned)" and of each of the three "`edx` * 0x10" | same, N1 |
| `00346780`, `00346EF0` | `07/Action-Dispatch/battle-action-handler-table.md` (F-homing section) | **edit** on its page and in its record | strike "with `xmm1` = the scaled float" / "with `xmm1` = scaled f3", replaced by the same text with "`xmm0` = that call's float result, " in front. With the replacements made, each sentence reads exactly as the review's wording (build_moves.py checks it) | [battle action handler table](../auditspec-review-fable-battle-action-handler-table-homing-1003/REVIEW.md) |
| `003CA530` | `16/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md` (F-homing section) | **edit** on its page and in its record | strike the review's old clause "(int)(`003CA530`+0x105((dword `0208F570` - dword `rcx+0xc0`)*pi/30)*64+128)", replaced by its new clause, which adds ", converted as an unsigned 32-bit value" | [numeric formatting](../auditspec-review-fable-numeric-formatting-and-character-mapping-homing-1003/REVIEW.md) |
| `003B6DE0` | `17/Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md` | **drop**, already documented | `04/Actor-Storage-Record/the-record-behind-every-actor.md` reads it ("`003B6DE0`, the routine `003B6F80` hands its list to.", L669) | [element types 40-42](../auditspec-review-fable-home-the-element-types-40-42-a0-ab-d0-d1-1003/REVIEW.md), N1 |
| `001AD670` | `06/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md` | **drop**, held by the review | no page cites `0017F5B0` as a subject (`LEAD 0017F5B0 ... 0`). The review says to home it with its caller (`ta-texture-animation-lists.md`, once `0017F5B0` is cited there) | [3d-or-flat](../auditspec-review-fable-home-how-the-engine-chooses-3d-or-flat-movem-1003/REVIEW.md), Repair 3 |
| `001D9F70` | `24/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md` | **drop**, host fails | the named host `game-application.md` cites `0017D940` only in passing, inside the `001A07B0` paragraph (L1747, "`001A1240` run: `0017D940(0)`"). The review names no alternative, and the body is a leaf (no callee host) | [lazy statics](../auditspec-review-fable-home-lazy-statics-and-the-one-time-init-lock-1003/REVIEW.md) |
| `004068B0`, `00407240`, `00408140` | `05/spawn-placement-and-retirement.md` | **drop**, host fails | the named host `numeric-formatting-and-character-mapping.md` cites neither caller (`004061F0`, `00406770`). The review's step 2 homes the callers first, which needs new sentences: a homing package, not a move | [spawn placement](../auditspec-review-fable-home-spawn-placement-and-retirement-1003/REVIEW.md) |
| `0028FF80`, `003C98E0`, `003CA280` | `02/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md` | **drop**, host fails | the named host `the-message-window-layout-readers.md` cites `0035C630` only inside the call chain of its `002BDCE0` row (L70; that row's first address is `002BDCE0`). The review names no alternative host | [vbf/st2e](../auditspec-review-fable-home-vbf-archive-and-st2e-tables-1003/REVIEW.md) |
| `00623EB0`, `00624040`, `00624690`, `006246E0` | `16/Dynamic-Geometry-Instances/dyngeo-instance-family.md` | **HELD** -> `17/Gi-Render-Commands/gi-render-command-family.md` | host passes (`0062A0A0` leads the interpreter paragraph, L1770). Target modified in the shared tree | [dyngeo](../auditspec-review-fable-home-dyngeo-instance-family-1003/REVIEW.md) |
| `003DB150` | `06/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md` | **HELD** -> `06/heading-speed-to-position-delta.md` | host passes (`002E54A0` key-address row, L255). Target modified | [3d-or-flat](../auditspec-review-fable-home-how-the-engine-chooses-3d-or-flat-movem-1003/REVIEW.md), Repair 2 |
| `003AC870` | `00/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md` | **HELD** -> `22/The-Frame/what-happens-between-two-frames.md` | host passes (`00376470` in the heading L1216 and its lead L1220). Target modified | [ee-vu0 bank](../auditspec-review-fable-home-the-ee-and-vu0-register-bank-1003/REVIEW.md) |
| `00243EE0` | `00/the-encoded-id-class-registry.md` | **HELD** -> `16/Battle-Hud/the-battle-hud-layout-readers.md` | host passes (`002C4720` first cell of its reader row, L82). Target modified | [encoded-id](../auditspec-review-fable-home-the-encoded-id-class-registry-1003/REVIEW.md) |
| `003AED50` | `02/the-external-source-owner-and-borrowed-view-lifetime.md` | **HELD** -> `17/Authored-Commands/the-authored-presentation-command-handlers.md` | host borderline (see the host rule). Target modified. The review's alternative, `the-character-render-record-array.md`, fails: `0041FCF0` appears there only mid-paragraph (L376) and in a parenthesis (L572) | [external source owner](../auditspec-review-fable-home-the-external-source-owner-and-borrowed--1003/REVIEW.md) |

Every moved row keeps its anchors and entered_from. Its text is copied from the source page's current row, which
`build_moves.py` checks against the record. The only exceptions are the two replacement wordings above: their
target never said the old wording, so it receives the new text without a strike, and the record's `moved` entry
keeps `text_edit` (removed / kept) and `moved_text`.

## FABLE: the --only list and the held rows

Five target pages show ` M` in `git status --short` on the shared tree. On each of them the working file is CRLF and
the HEAD blob is LF, and the content is identical once CR is stripped. So the change is line endings only, but the
pages are not clean, so their rows are HELD. All other paths this record touches are clean at `89538d085`. The
license-board page was modified when this record was started (the peer section SWE2-EC7-213). That section is now
committed (`61a7567f4`) and the page is clean, so its three rows are applied.

Held (8): `00623EB0`, `00624040`, `00624690`, `006246E0` (gi-render-command-family.md); `003DB150`
(heading-speed-to-position-delta.md); `003AC870` (what-happens-between-two-frames.md); `00243EE0`
(the-battle-hud-layout-readers.md); `003AED50` (the-authored-presentation-command-handlers.md).

```
python -B move_rows.py --apply --only 0029D4D0,00408AD0,0027F150,003FF160,003FF9F0,00420860,004209F0,00366A30,004FF230,004FE4A0,00623D70,00346780,00346EF0,003CA530,001AD670,001D9F70,004068B0,00407240,00408140,0028FF80,003C98E0,003CA280,003B6DE0
```

The held rows verify on the real tree (the all-rows pass above). Once a held target is clean, the same script moves
those rows with `--only` naming them, and no row needs to be rebuilt.

## FABLE: what is new in move_rows.py

- **`host: thunk`** (`00408AD0`). Verify checks four things. The entered_from caller is the thunk. The thunk is one
  `jmp` to the body. Each listed site (`002628B0` + 0x2E4, `0026C8C0` + 0x192) is a direct call to the thunk inside
  the named function. Each of those functions is a subject of the target.
  The review asked for "a body line" citing the thunk. FABLE writes it as the lead of its own bullet in this record's
  section and not inside a peer's section, which would be a change under a heading that does not name FABLE. The host
  basis does not rest on that line: the tool checks the thunk's callers outside the section.
- **`edits`**. A struck span must occur on the row exactly the recorded number of times, so a strike only strikes
  text the row says (controls 5 and 6). The cell becomes `~~old~~ new` for each span, then one dated note. The
  record's `rows.json` text is set to the same cell, so the record's own applier stays `ALREADY`; for the two
  F-homing records that is the applier that re-renders a block whose rows.json differs. The edit itself is kept in the record's
  `narrowed` list, with the previous text and the plain wording. In the applied worktree all four page cells equal
  their rows.json text.
- **`host_fails` drops**. The raw transfer index into the body (E8/E9, 0F 8x, EB/7x, decoded) must equal the
  record's callers. On every page the review named, the caller must *not* be a subject (control 3 names a page where
  it is). The quoted passing mentions must still be there. The `LEAD` lines list every bearing page where a caller
  is a subject; these are the routes for re-homing later.
- **`lea_checks`** (`0029D4D0`): `0029D4DB` is a RIP-relative `lea` that loads `0029D550` (control 8).
- **`target_before`**: the efx section is inserted before `## 2c.` instead of at the end of the page.

## FABLE: notes and leads

- **Optional review additions not taken.** The lazy-statics, ee-vu0 and external-source reviews each offer an
  optional parenthetical for the sentence. The first row is dropped and the other two are held; the parentheticals
  can go in with the move once the pages are clean. The dyngeo review allows `00624690`'s second site
  (`0062A0A0` + 0x4AA). The row keeps its recorded site.
- **Advisories not acted on.** The dyngeo page's line 749 ("for the dyngeo records"), the spawn page's stale
  pass-22 line 3781, and the encoded-id intro's "no page cited" wording belong to their owners' pages. This record
  does not edit them.
- **Leads for the dropped rows.** `001AD670` and `001D9F70` wait for a page that documents `0017F5B0` or
  `0017D940`. The three spawn rows wait for a homing of `00406770` (entered from `00406DD0` + 0x7B, which the
  numeric page homes) and of `004061F0` (a widget procedure that `00405310` + 0x102 passes to `00244F50`). The three
  vbf rows wait for a page that documents `0035C630`. OPUS's interior row for it is on the vbf page, the host the
  review rejected.

## Consumer check (FABLE)

affected: Database/FFXII TZA/00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md
affected: Database/FFXII TZA/02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md
affected: Database/FFXII TZA/02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md
affected: Database/FFXII TZA/02-Resource-And-Asset-Pipeline/the-source-block-mover-and-separate-consumer-refresh.md
affected: Database/FFXII TZA/05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md
affected: Database/FFXII TZA/06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md
affected: Database/FFXII TZA/07-Combat-Action/Action-Dispatch/battle-action-handler-table.md
affected: Database/FFXII TZA/15-Input/Modal-Toggles/r2-force-fight-toggle.md
affected: Database/FFXII TZA/16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md
affected: Database/FFXII TZA/16-UI/License-Board-View/the-license-board-screen-widgets.md
affected: Database/FFXII TZA/16-UI/Shared-Dialogs/the-shared-dialog-widgets.md
affected: Database/FFXII TZA/16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md
affected: Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md
affected: Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md
affected: Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md
affected: Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md
affected: Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md
affected: Database/FFXII TZA/99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md

- consumer: the FABLE homed sections (2026-10-03, cloud-drafted) on five-small-bin-tables, glyph-quads, license-board
  widgets, source-block mover, lazy statics, spawn placement and vbf/st2e: revised-here (every row removed; section
  withdrawn).
- consumer: the FABLE homed section on how-the-engine-chooses-3d-or-flat-movement: revised-here (`001AD670`
  dropped). `003DB150` is held, and the four rows the review accepts stay.
- consumer: the FABLE homed section on effect-element-type-dispatch: revised-here (`00366A30`, `004FF230` and
  `004FE4A0` moved; `00623D70` narrowed). The four rows the review accepts stay unchanged.
- consumer: the FABLE homed section on the-element-types-40-42: revised-here (`003B6DE0` dropped; six rows stay).
- consumer: the FABLE F-homing section on battle-action-handler-table: revised-here (two cells narrowed by
  strike-and-replace; the anchors are unchanged).
- consumer: the FABLE F-homing section on numeric-formatting-and-character-mapping: revised-here (the `003CA530` cell
  narrowed by strike-and-replace; the anchors and the `00404E10` row are unchanged).
- consumer: the numeric-formatting F-homing review: agrees (its old clause struck, its new clause written).
- consumer: the world-tick, ui-layout, shared-dialog, character-render-record, r2-force-fight and efx pages:
  revised-here (each gains the batch-6 section; no existing line changes; the efx section sits before §2c).
- consumer: the twelve source records' rows.json: revised-here (rows moved to `moved` or `dropped` with the reason,
  or narrowed in place with a `narrowed` entry).
- consumer: the five-small-bin-tables, glyph-quads, license-board, source-block and effect-element (N1-N3) reviews:
  agrees (the hosts and wordings they name, applied as written; the glyph-quads thunk line placed as the lead of a
  bullet in this section).
- consumer: the battle-action-handler-table review: agrees (both replacement wordings, reached by a strike of real
  text only).
- consumer: the element-types-40-42 review: agrees (N1, the row deleted; the optional anchored line on the actor
  record page is not added).
- consumer: the 3d-or-flat review: agrees (Repair 3, `001AD670` held to the frontier; Repair 2 waits on a clean
  target).
- consumer: the lazy-statics, spawn-placement and vbf/st2e reviews: agrees on the defect (the rejected host). Each
  named host fails FABLE's host rule, so the rows return to the frontier instead of moving (reasons in `moves.json`
  and in each record's `dropped` entry).
- consumer: the cross-record ruling on `003FF9A0`: agrees (`003FF9A0` stays; the three license-board callees join
  in the section after it).
- consumer: the dyngeo, ee-vu0, encoded-id and external-source reviews: agrees on the defect. Their moves are built
  and verified, and held only while their target pages are modified in the shared tree.

run: move_rows.py at 89538d085 (VERIFY 10 functions, 41 anchors, 6 target pages, 4 edits, 9 drops / FAILS 0)

Proof of the apply: on a clean detached worktree of `76143cef7`, two `--apply --root` passes with the `--only` list
gave 56 `PATCHED` then 56 `ALREADY`, with `FAILS 0` both times. No commit between `76143cef7` and `89538d085` touches
any of these paths. `git status --short` there listed 30 files: the 18 pages above and the 12 source records. That
is the same set the `--only` rows name. `git diff --stat` showed 445 insertions(+) and 242 deletions(-).

## FABLE: files

| file | what |
|---|---|
| `moves.json` | 18 `moves` (each with `host`, evidence lines, 8 `held`), 4 `edits`, 9 `drops` (8 `host_fails`, 1 `already_bound_on`) |
| `build_moves.py` | rebuilds `moves.json` from the source pages and records (texts copied, not retyped; review wordings checked) |
| `subjects.py` | the host rule: which mentions on a page are subjects; `python -B subjects.py PAGE ADDR` prints them |
| `move_rows.py` | the b5 script plus the host rule, `thunk`, `edits`, `host_fails`, `lea_checks` and `target_before`; verify-only by default; `--apply`, `--root`, `--only`, `--moves` |
| `move_rows.out` / `move_rows.all.out` | the verify-only passes on the shared tree at `89538d085`, `--only` and all rows |
| `worktree_apply1.out` / `worktree_apply2.out` | the two `--apply --root` passes on the clean worktree |
| `controls.py` / `controls.out` | eleven one-entry mutations of `moves.json`; each must be refused |
