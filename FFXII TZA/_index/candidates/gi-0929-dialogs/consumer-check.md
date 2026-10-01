# Consumer-check record — GI-2, GI-4 and GI-13 answers and the dialog/handbook corrections (FABLE, Claude Opus 5.5, 2026-09-29)

affected: `Database/FFXII TZA/16-UI/Handbook/the-handbook-screen.md`
affected: `Database/FFXII TZA/16-UI/Shared-Dialogs/the-shared-dialog-widgets.md`
affected: `Database/FFXII TZA/19-Save-Load-Settings/the-save-load-screen-widgets.md`
affected: `Database/FFXII TZA/20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md`
affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md` (rows GI-2, GI-4, GI-13)

Consumer search: grep over `Database/FFXII TZA` (`*.md`, `*.tsv`; `_experiments` and `AUDIT-LOG` excluded) for each
address, offset and wording below. States: **revised-here** (this publish edits it), **agrees** (unchanged, consistent),
**routed-to-<owner>** (exact text given). Wrong statements are struck on the pages with the correction beside them.

Two page facts to know before splicing:
- the handbook page's working tree carries a peer's uncommitted overlay (two `archive_formats:` front-matter lines);
- this publish is built on the HEAD copy of that page, and none of its substitutions depends on the overlay text.

## C1 — the `0xC0368C` / `0xC036A4` table framing

**Was:** 6-byte records `{paneKind, flag, u16, u16}` starting at `0xC0368C` / `0xC036A4`. Under that reading:
- the handbook byte was a resource id (page art);
- kind 7's `0x0000`/`0x8000` was a terminator;
- the first menu row paired kind 6 with `0x1B5C` Bestiary.

**Is:**
- The records are `{u16 label; u16 help; u8 key; u8 flag}` from `00D23688`, and the two displacements address the `+4` key byte.
- Menu row 0 is Hunts with key 6; Bestiary is 5, Sky Pirate's Den 7 and Traveler's Tips 4.
- The handbook key is the page's slot in saved-cursor bank 6, stored through `002527B0`.
- The "terminator" is the first dword of the next table at `00D236D0`.

The UI batch's GI-6 reader found the same framing and the Hunts → 6 row independently; its §C-5 and §C-6 text is merged into this publish.

- consumer: handbook page — tree prose, id-18 row, the paragraph after the arm table, "What this screen does", the `0xC036A4` section (table rows struck, reader-framed table added), the "Not yet established" bullet on page kinds: revised-here
- consumer: handbook page, falsification-pass line "the `0xC036A4` page-kind→resource lookup beyond its presence": agrees (a record of what the pass did not attack; left as history)
- consumer: shared-dialog page — the `0xC0368C` paragraph and the "Not yet established" bullets: revised-here
- consumer: `16-UI/Unlabelled-Panes/the-unlabelled-procedures.md` line 146 and its status line: routed-to-UI-batch (GI-6 owner). Append after the struck bullet: " **Corrected 2026-09-29 (FABLE, GI-4):** the `{paneKind, flag, u16, u16}` framing is four bytes late — the records are `{u16 label; u16 help; u8 key; u8 flag}` from `00D23688`, and `0xC0368C`/`0xC036A4` address the key byte; decoded on the shared-dialog page (link target `../Shared-Dialogs/the-shared-dialog-widgets.md#the-title-table-the-two-single-installer-widgets-and-the-0x630-word--read-2026-09-29-fable-gi-4`, relative to the receiving page)."
- consumer: `16-UI/Message-Windows/the-message-window-layout-readers.md` line 41 ("the `0xC0368C`-family lookup tables are the parts still open"): routed-to-page-owner. Replace that clause with "(the `0xC0368C`-family tables are decoded on the shared-dialog page, 2026-09-29, GI-4)".
- consumer: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/hchk-hctg-hdat-handbook-indexes.md` lines 476/480: agrees. It already reads `00D23688` / `00D236A0` triples.
  - Separate note, routed-to-page-owner: line 476's `002526F0(3, 6)` should read `002526F0(6, 3)`, i.e. bank 6, slot 3 (`ecx` = 6, `edx` = 3).
- consumer: `_index/OPEN-QUESTIONS.md` GI-2 / GI-4 question text: agrees (question wording kept as history; status cells replaced)
- consumer: `_index/progress/crosswalk.md`: agrees (derived; regenerated, not hand-edited)

## C2 — `hcom` as a "u16 self-relative node web", with `0xFFFF` dead ends and a `de` insertion of `0x800661FF`

**Is:** five length-prefixed sections chained by `p += u16[p]` from `+8`:
1. a navigation-map bitmap;
2. bestiary unlock rules;
3. hunt thresholds;
4. the Den monster ids;
5. the achievement overrides.

The `0xFFFF` words are bitmap bits, and the mask `0x800661FF` is in all nine locales. The size deltas are a section-1 Rogue Tomato rule (every non-us locale) and a section-4 value of 48000 (in/kr/cn/ch).

- consumer: handbook page `hcom` block (correction note above the fence, closing sentence struck) and the residue bullet: revised-here
- consumer: handbook page front matter, the peer's uncommitted `archive_formats` line for `hcom` ("u16 self-relative node web … node semantics still open"): routed-to-overlay-author. Replace with `- "hcom | explained | menuhandbook.bin (.bin member): {hcom, u32 103, then five sections {u16 len, u16 count, …} chained p += u16[p] from +8: navimap bitmap, bestiary rules, hunt thresholds, Den monster ids, achievement overrides} - (kind 7, 0xC8) by 003158B0 into 022C2550; sections decoded 2026-09-29 (GI-2)"`
- consumer: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md` line 381 ("the same offset-chain encoding `hcom` uses"): routed-to-page-owner. Replace the parenthesis with "(`hcom` also chains u16 relative offsets, but as section lengths with no `0x8000` sentinel — the handbook page, 2026-09-29)"
- consumer: `loader-bound-bin-families.md` line 271: agrees (a pointer to the handbook sheet, no format claim)

## C3 — `hodr` fields and the identity of `00572E10`, `00572600` and `+0xCB`

**Was:**
- `+0x00` is a display order and `+0x01` a page kind;
- `+0x16`/`+0x17` are a link pair forming a perfect pairing, and the last three records are inactive;
- `00572E10` is a viewer generic over chapters; `+0xCB` is a count; `00572600` is the page view that owns the cursor;
- the member rows name `00572920` "page-select", `00572BD0` "record refresh" and `005734C0` "menu-effect reset".

**Is:**
- The table is the Sky Pirate's Den statue layout, and `00572E10` is installed for page kind 7 only.
- `+0` is the selection key and child anchor; `+1` is the draw depth.
- `+0x16`/`+0x17` are the normal and highlighted effect ids.
- `+0xCB` is the selected statue.
- `00572600` is the statue description popup.

- consumer: handbook page — tree prose and rows, the `00572E10` heading note, the id-1/10/12/18 rows, "The children", the member rows, the layout-key row, "What this screen does", the `hodr` block, and a new Den section: revised-here. `00572460`'s own role was not re-read and is left as it stands.
- consumer: handbook page front matter, the peer's uncommitted `archive_formats` line for `hodr` ("the +0x16/+0x17 link pair's traversal still open"): routed-to-overlay-author. Replace with `- "hodr | explained | menuhandbook_order.bin (.bin member): {hodr, u32 101, u32 33, 32-byte records[33]} (12 + 33*32 = 1068) - (kind 7, 0xC9) by 00572D80 into rbx+0x1200; the Sky Pirate's Den statue layout (key, depth, x/y, pointer dx/dy, popup x/y, normal/highlight effect ids at +0x16/+0x17) (GI-2, 2026-09-29)"`
- consumer: `16-UI/Menu-Screen-Atlas/the-menu-screen-atlas.md` lines 70–71: routed-to-atlas-owner. Replace with "`00572E10` (the Sky Pirate's Den, page kind 7; `menuhandbook_order.bin` is its statue layout) → `00572460` / `00572600` (statue description popup)"

## C4 — `0056F810` "the generic list every screen embeds"; `00556F90` "the scrolling message box … both cite"

**Is:** `0056F810` has one installer, `00574D00`: it is the Clan Primer category menu. `00556F90` has one installer, `00556EC0`, called only from `00557DB0`: it is the license-board description box.

- consumer: shared-dialog page — the `0056F810` opening sentence, the `00556F90` section, "What these are": revised-here
- consumer: `16-UI/Menu-Screen-Atlas/the-menu-screen-atlas.md` lines 72–73: routed-to-atlas-owner. Replace with "`0056F810` the Clan Primer category menu, `0057C480` confirm, `00556F90` the license-board description box, `00566680` item-sort bar — `0057C480` is the one with several producers; `0056F810` and `00556F90` each have one installer (GI-4, 2026-09-29)."
- consumer: same atlas, line 312 ("The four reusable dialogs …"): routed-to-atlas-owner. Append " *Note 2026-09-29 (FABLE, GI-4): `0056F810` (the Clan Primer category menu) and `00556F90` (the license-board description box) each have a single installer, so of the four only `0057C480` is reused across screens; the evidence-row placement is unchanged.*"
- consumer: `_index/OPEN-QUESTIONS.md` UQ-161 (answered; the same "four reusable dialogs" sentence): routed-to-register-editor. Append to the status cell: " *Note 2026-09-29 (FABLE, GI-4): of the four, only `0057C480` is reused — `0056F810` (Clan Primer category menu, installer `00574D00` only) and `00556F90` (license-board description box, installer `00556EC0` only) are single-screen; the answer's placement conclusion stands. Check: `_index/candidates/gi-0929-dialogs/gi4_dialog_tables.py`.*"
- consumer: `16-UI/Widget-Object-Model/CONTRACT-widget-object.md` line 977 ("menu-list widget procedure"): agrees

## C5 — the confirm window's `+0xFC` "result byte" on "the parent list"

**Is:** the window's own embedded list (`+0xC0`), and the byte is the list's decide-sound id, which the list plays when its owner declines the pick.

- consumer: shared-dialog page, the `0057CB16` bullet and residue bullet: revised-here
- consumer: `_index/PROGRAM-STATE.md` line 6007 ("mapping `+0x630` flag classes to parent `+0xFC` result bytes"): routed-to-FRONTIER. Change to "mapping `+0x630` flag classes to the embedded list's `+0xFC` decide-sound id (GI-4, 2026-09-29)"
- consumer: GI-4 question text: agrees (kept as history)

## C6 — the confirm window's id-10 bit notation ("bit `0xC`", "bit `0x10`", "pad bit `0x10`")

**Is:** masks `0x1000` and `0x10000` of the `+0x630` flag word; the countdown answer depends on the flag word, not on a pad bit.

- consumer: shared-dialog page, the id-10 bullet: revised-here
- consumer: `_index/PROGRAM-STATE.md` line 6005 (countdown only, no bit claim): agrees

## C7 — "3 / `0xD` / `0xF` are the storage-result values"; the handlers "destroy the pane"; `00580CD0` "re-enumerates"

**Is:** they are notification classes of sub-command `0x1D`, and the status is the payload's `+8`. What the handlers release at `+0xD8` is the popup, not the pane. `00580CD0` copies the new header record out of the active image.

- consumer: save/load widgets page, the second struck bullet, a new section, and the status line (appended to): revised-here
- consumer: the same page's leading status clause ("what the three storage-result values 3 / 0xD / 0xF mean is not read"): routed-to-page-owner for re-status. Suggested: "the three `0x1D` notification classes and all fifteen controller states named 2026-09-29 (GI-13)"
- consumer: `19-Save-Load-Settings/CONTRACT-storage-read-completion.md` (subtype `0x1D` arms, "payload 3", "releases `+0xD8`"): agrees
- consumer: `how-a-manual-save-is-committed.md` ("message `0x1D` with payload `0xF`") and `spawn-placement-and-retirement.md` §24 ("tags 3/13/15"): agrees
- consumer: GI-13 question text: agrees (kept as history)

## C8 — the achievement catalogue's UQ-274 note that id 31's override "ships unread"

**Is:** no achievement check reads it. The Sky Pirate's Den layout does: `00572920` calls `003165C0` through the `003165B0` thunk with each `0xFF`-keyed `hodr` record's index. For record 31 the returned 16 is the key of Ba'Gamnan's statue, which the extra sprite is drawn with and beside.

- consumer: the catalogue page, the UQ-274 item (struck and corrected) and its status line (appended to): revised-here
- consumer: `_index/OPEN-QUESTIONS.md` UQ-274 (ANSWERED 2026-09-14; the cell does not state the id-31 claim, and its answer stands): routed-to-register-editor. Append to the status cell: " *Note 2026-09-29 (FABLE, GI-2): the page's sentence that id 31's override \"ships unread\" is corrected — no achievement check reads it, but the Sky Pirate's Den layout `00572920` calls `003165C0` (through `003165B0`, `005729BE`) with each `0xFF`-keyed `hodr` record's index, and id 31's value 16 anchors the extra Den sprite to Ba'Gamnan's statue. See the handbook page (link target `../16-UI/Handbook/the-handbook-screen.md`, relative to the receiving page) section The Sky Pirate's Den; check `_index/candidates/gi-0929-dialogs/gi2_hcom_hodr.py` FAILS 0.*"
- consumer: `20-Platform-Online-Achievements/members/menuhandbook-achievement-records.tsv`: agrees (no "unread" claim)
- consumer: `_index/_inbox/SWE2-DATA.md` line 1223 ("entry 10 (`0x0103`) ships unread"): routed-to-SWE2-DATA (FYI). `00315D50` reads all 11 section-3 entries, since its loop bound is `cmp ecx, 0xb`. So entry 10 is looked up as a separate-counter monster even though achievement mode 7 indexes only 0–9.

## Regression

Each check script sits in this folder, beside its output:
- `gi4_dialog_tables.py` → `gi4_dialog_tables.out`: C1, C4, C5 and C6.
- `gi2_hcom_hodr.py` → `gi2_hcom_hodr.out`: C2, C3 and C8.
- `gi13_saveload_states.py` → `gi13_saveload_states.out`: C7.

Each script exits 1 on any failed check, and each old reading fails a named check. The checks per correction:
- **C1:** "REGRESSION: the published framing … agrees 0 of 4". The reader framing agrees 4 of 4. Two further checks: "the next object starts at 00D236D0" and "002527B0 stores word +0x30, byte +0x70, dword +0x90".
- **C2:** "REGRESSION: every 0xFFFF word … lies inside section 0's bitmap", "section-4 mask carries 0x800661FF's bits" in all nine locales, and the chain-ends-at-file-size checks.
- **C3:** "installs 00572E10 only for page kind 7", "REGRESSION: +1 is a depth", "REGRESSION: every +0x16/+0x17 read is the r9d effect id".
- **C4:** the single-installer checks for the two procedures.
- **C5:** "the list plays its +0xFC byte as the decide sound".
- **C6:** the bit-test checks at the two `bt` sites.
- **C7:** "reads the status at payload+8" for all three handlers.
- **C8:** "children anchor through 003165B0 = jmp 003165C0" and "record 31 anchors to record 16".

Positive controls: text resolver ("Yes", "Save complete."), battle-text bank ("Petrify"), the `0x1D` post scan (the save transaction's post), the table rip sweep, and the state scan (states 6 and 8).

run: gi2_hcom_hodr.py at 6facc53bc (HEAD when it ran), 68 checks pass, FAILS 0
run: gi4_dialog_tables.py at 6facc53bc (HEAD when it ran), 75 checks pass, FAILS 0
run: gi13_saveload_states.py at 6facc53bc (HEAD when it ran), 60 checks pass, FAILS 0
run: gi4_mask800.py at ed127d443 (HEAD when it ran), 39 checks pass, FAILS 0
