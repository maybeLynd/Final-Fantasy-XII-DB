---
id: ui-shared-dialogs
title: The shared dialog widgets — menu list, confirm window, message window, item-sort bar
status: "DOCUMENTED — GI-4 answered 2026-09-29 (FABLE), review (FABLE-REQ-AUDITSEM-REVIEW-GI-DIALOGS, ACCEPT, d998217e2); documented_rule.py READY, no open box or live id; owner re-status 2026-09-30 (SWE2-FRONTIER, record dd-restatus-gi-0930). Was PARTIAL on: the +0x630 flag classes are not established; 00556F90's id-2 arm read on the message-window page and the 0xC0368C / 0xC036A4 tables decoded (pane kind, flag, two resource ids) 2026-09-18"
evidence_tier: 1
tags: [ui, menu-screens, shared-widgets]
addresses:
  - "0056F810"
  - "0057C480"
  - "00556F90"
  - "00566680"
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 002AC5F0 00566680 0056F810, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
    verified: 22 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-14
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: opus-shared-dialogs-pass-1 - the table at 0056FA80 read entry by entry at GN160. The page's HEADER id set (1,10,12,14,15,18) is exact and its own BULLETS were mislabelled - 0056F889 is id 14 not id 2, 0056FA09 is id 18 not id 14, and id 2 goes to the default 0056FA73, so this widget never answers id 2. Arm addresses and behaviour were right; the id labels were not. The confirm window's seven ids and its 0057C4D9 singleton store, and the message window's 1/2/18 with no input or sub-command arm, all hold
  crossref_clean: false
  reopened_count: 0
---

# The shared dialog widgets

**Status:** ~~PARTIAL~~ DOCUMENTED *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`, GI-4 answered 2026-09-29)* — the four procedures' dispatch shapes and arm interiors are cited below; `0057C480`'s full id-4/10/12/19 arm set is now read (2026-09-15) and every listed screen-region member of the two dialog subtrees has an interior citation. These are the **shared dialogs** the atlas rows' "(child)" entries refer to: reusable widgets screens install, not screens of their own. None of them owns a layout surface of its own beyond its frame.

## `0056F810` — the menu list (CommandMenu/MenuList keys)

~~The generic vertical-option list every screen embeds as its `+0x148`-style child.~~ **Corrected 2026-09-29 (FABLE, GI-4):** the Clan Primer's category menu — Hunts, Bestiary, Sky Pirate's Den, Traveler's Tips. Its only installer is `00574D00` (from the handbook back panel `00574E80`), its rows are always the four menu records of the `00D23688` table filtered by unlock (`0056F750`), and its id 18 keeps the chosen option in saved-cursor bank 6, slot 3; see [§ The title table](#the-title-table-the-two-single-installer-widgets-and-the-0x630-word--read-2026-09-29-fable-gi-4). Dispatches ids 1, 10, 12, 14, 15, 18 through the table at `0056FA80`:

- **id 1** `0056F83C`: `msg->a` → `+0xC0` (parent), `msg->b` → `+0x170` (option-table ptr), `+0xCC` = `0xFF` cursor, `0056F5F0` init, `00247930`(0x63) resource (`0056F874`)
- **id 14** `0056F889`: reconcile — sets `+0xC8 |= 1`, runs the standard cursor slot math on `+0x168` (`(+0xF2 + +0xF4) * +0xEC + +0xEE + +0xED` at `0056F89C`–`0056F8C6`), highlights the row via `00291D80`, posts `{0xE, 3}` to the parent, `002470D0`
- **id 10** `0056F906`: directional input → `002D3900` on `+0x168`
- **id 12** `0056F923`: sub-commands — `0x8000` highlight row `msg->b` when `+0xC8 & 1` (`0056F9C2`); `0x8001` looks up `[+0x170] + 0xCE + row` in the `0xC0368C` table and posts `0x8001` to the parent (`0056F96A`–`0056F9B5`); `0x8002` posts `0x8002` to the parent + `002CC9C0`(0xC8) (`0056F943`)
- **id 18** `0056FA09`: slot math → `002527B0`(6) on `+0xCE` table
- **id 15** `0056F9F2`: clear highlight + `+0xC8 &= ~1`, posts `{0xF, 6}`

> **CORRECTED 2026-09-14 (OPUS, falsification pass 1): two of these bullets were labelled with the
> wrong ids, and this widget never answers id 2.** ~~id 2 `0056F889`~~ is **id 14**; ~~id 14
> `0056FA09`~~ is **id 18**. Read entry by entry, the table at `0056FA80` gives
> `1`→`0056F83C`, `10`→`0056F906`, `12`→`0056F923`, `14`→`0056F889`, `15`→`0056F9F2`,
> `18`→`0056FA09`, and **`id 2` resolves to the default arm `0056FA73`** along with 3–9, 11, 13, 16
> and 17. **The arm addresses and the behaviour described against them were correct** — the slot
> math at `0056F89C`–`0056F8C6` and the `+0xC8 |= 1` really are in `0056F889` — only the id labels
> were wrong. **The section heading above, *"Dispatches ids 1, 10, 12, 14, 15, 18"*, was right all
> along**, so the page contradicted itself and the heading won.

**The `0xC0368C` table, decoded from its reader 2026-09-18 (FABLE).** The id-12 arm's `0x8001` path (`0056F96A`–`0056F9B5`) takes the option table's byte at `+0xCE + row`, stores it as the cursor kind `+0xCC`, clamps values `≥ 4` to 0, and ~~reads the **6-byte record** `[image + 0xC0368C + kind × 6]`, posting the record's first byte to the parent as sub-command `0x8001` unless it is `0xFF`. The four records are `06 01 5C1B 441F`, `05 01 5D1B 451F`, `07 01 5E1B 461F`, `04 02 581B 401F` — a pane kind (6, 5, 7, 4), a flag byte, and two `u16` (`0x1B5C`… and `0x1F44`…, resource-id shaped). The handbook's `0xC036A4` table follows in the same shape (`0B 00 591B 411F` …, kinds 0–7 to resource ids `0x0B`–`0x12`, decoded on [the handbook page](../Handbook/the-handbook-screen.md) §“The 0xC036A4 lookup”), so the two are one record type: **pane kind → flag → two resource ids**, the menu list's four rows for option kinds 0–3 and the handbook's eight for page kinds 0–7.~~

**Corrected 2026-09-29 (FABLE, GI-4): the framing was four bytes late, and it paired each key with the next record's texts.** `0xC0368C` is the `+4` key byte of 6-byte records `{u16 label; u16 help; u8 key; u8 flag}` that start at `00D23688`; the arm reads the option's key and posts it to the parent as the argument of sub-command `0x8001` unless it is `0xFF`. So the first menu record is `{0x1B5F "Hunts", 0x1F47, key 6, flag 1}` — kind 6 is **Hunts**, not Bestiary (`0x1B5C`, the published pairing) — then Bestiary → 5, Sky Pirate's Den → 7, Traveler's Tips → 4. The handbook half follows at `00D236A0`, and its key is a saved-cursor slot, not a resource id. Both halves are decoded in [§ The title table](#the-title-table-the-two-single-installer-widgets-and-the-0x630-word--read-2026-09-29-fable-gi-4). `00556F90`'s id-2 arm is read on [the message-window page](../Message-Windows/the-message-window-layout-readers.md) (the title row `0x3ED + page` and the body row `0x838 + page`, wrapped into three lines). ~~What the `+0x630` flag bits mean as classes stays open.~~ *(Read 2026-09-29, FABLE, GI-4 — [§ The title table](#the-title-table-the-two-single-installer-widgets-and-the-0x630-word--read-2026-09-29-fable-gi-4); one bit's effect stays open.)*

## `0057C480` — the confirm window (ConfirmCaption/ConfirmWindow/GeneralFrame/MessageLine/NobuMessage keys)

The generic choice dialog — a singleton: construct stores `self` into `[global + 0x328]` at `0057C4D9`. Dispatches ids 1, 2, 4, 10, 12, 18, 19 through `0057CCA8`. Its id-1 arm (`0057C4BF`–`0057C682`) is the largest seen in the region:

- copies `arg+0` (the caption) into an inline `0x400` buffer at `+0x1B0` via `00254F30`, or zeroes it via `00861EC0` when absent (`0057C5A6`)
- measures the caption: `002B3400`/`002B3280` text extents → `+0x120`/`+0x114`, `002B3050`/`002B1E20` layout, window width clamped to `0x60` minimum (`0057C5FD`)
- `+0x630` = `arg+0x20` flags, `+0x634` = `arg+0x1C` byte, `+0xC8`/`+0xD0` = `arg+0x10`/`+0x8`
- zeroes eight `0x30`-stride option slots `+0x5B0`..`+0x62C` (`0057C643`–`0057C674`) — the choice rows

The remaining arms, read against the table at `0057CCA8` (2026-09-15):

- **id 4** `0057C901`: draw — fetches layout string `0x4B48` via `002F9860`; `+0x630` bit `0x20` selects `002D8650` over `002D8550` on the `+0xE0` text block, bit `0x8000` appends string `0x4B42`; `002D8BB0`/`002D8910` render with a negative x-offset taken from `[rip+0x188f769]`/`[rip+0x188f75c]` (right-align/center math), saving and restoring `[+0x38]+0x5C`
- **id 10** `0057C9A3`: input — when `+0x630` bit 8 is clear it forwards to `002D3900` on `+0xC0` (the embedded list child). When set, `002B3930` must still be animating-gated (`+0x190`==1) and the pad word at `[rip+0x2a1a981]` is tested: ~~bit `0xC` of `+0x630` runs an auto-confirm countdown at `+0x63A` (decrement; on 0 picks `1` when pad bit `0x10` is set, `2` when clear — `and eax,0x10000; neg; sbb; lea r14d,[rax+2]` at `0057CA09`–`0057CA12`); bit `0x10` picks `1` when the pad word is non-zero.~~ **Corrected 2026-09-29 (FABLE, GI-4):** `bt ecx, 0xC` is bit 12 (mask `0x1000`) of `+0x630`: it counts `+0x63A` down and at zero answers `1` when `+0x630` mask `0x10000` is set, `2` when clear (`0057CA09`–`0057CA12` test the flag word, not the pad); `bt ecx, 0x10` is mask `0x10000`, which also makes any pad press answer `1` (`0057CA16`–`0057CA25`). The masks `8`, `0x20`, `2` elsewhere in these bullets are masks, not bit numbers. A confirm-mask hit `[rip+0x188f870]` (`01E0C2A0`, tested at `0057CA29`) plays SE `3`/`2` via `00249C60` and posts `0x8001` to self; a cancel-mask hit `[rip+0x188f865]` (`01E0C2A4`, tested at `0057CA38`) plays SE `3` and posts `0x8002` (`0057CA29`–`0057CA93`)
- **id 12** `0057CAAB`: sub-commands on `msg->a-0x8000` —
  - `0x8000` (`0057CC09`): if bit 8 is clear and `+0x637` non-zero, post `0x8103` to the `[+0xC8]` child carrying the parent list's current cursor index (the standard `+0xF2/+0xF4 × +0xEC + +0xEE/+0xED` walk on `[+0xC0]`); then increment `+0x637`, capped at 2 — the dialog's stage counter
  - `0x8001` (`0057CB16`): option pick. With bit 8 set it just posts `0x8100` to `[+0xC8]`. Otherwise it computes the embedded list's cursor row, checks the option slot's `+0x5BC` flag bit, and writes ~~the parent list's `+0xFC` result byte~~ **its own embedded list's `+0xFC` decide-sound id** (corrected 2026-09-29, FABLE, GI-4: `r8` = `+0xC0`, and the list plays that byte as its confirm sound at `002D4114` when the owner declines the pick) from the `+0x630` flag class: option id `0x8101` → `3`; `0x04` → `0x37`; `0x40` → `0x19`; `0x80` → `0x18`; `0x100` → `3`; `0x200` → `4`; `0x400` → `0x45` — the last three via `bt edx, 8/9/0xA` (`0057CB8F`–`0057CBD7`). It then posts the slot's `+0x5B8` word (the option id) to `[+0xC8]` and returns 1 only when the child answered 1
  - `0x8002` (`0057CACB`): with `+0x630` bit 2 set, post `0x8102` to `[+0xC8]` and clear `+0x40` bit 3; with bit 8 clear, `002D4650` on `+0xC0` with `movsx +0x634` — the back/scroll path
- **id 19** `0057C88C`: same `002D4650` back-path as `0x8002`, gated on bit 8 clear and `+0x637`==1 — the "leave stage 1" message
- **id 2** `0057C8C0`: reconcile — `001EDEC0` FrameLimit mode predicate on `+0xB4`; when it passes and bit `0x20` is clear, window-record `002ABEC0` + `002B1E20`(0) re-lay out `+0xE0`
- **id 18** `0057CC79`: clears `[rip+0x1b1dfb0]+0x328` — the singleton pointer teardown complementing the `0057C4D9` store

## `00556F90` — the message window (MessageLine/NobuMessage keys)

Display-only: answers ids 1, 2, 18 — construct, reconcile, destroy. No input arm, no sub-command arm. ~~This is the scrolling message box the gambit list and confirm window both cite in their key families.~~ **Corrected 2026-09-29 (FABLE, GI-4):** it is the license-board chooser's board-description box — one installer, `00556EC0`, called only from `00557DB0`, which also writes the board index it shows (`00558549`); title `0x3ED + board` (White Mage … Shikari), body `0x838 + board`. See [§ The title table](#the-title-table-the-two-single-installer-widgets-and-the-0x630-word--read-2026-09-29-fable-gi-4).

## `00566680` — the item-sort bar (ItemSort + ConfirmWindow keys)

The sort strip inside the item screen (installed by `005665B0`). Dispatches ids 1, 2, 12, 15, 18:

- **id 12** `00566794`: sub-commands `0x8102`–`0x8106` — the five sort modes; ~~each walks the parent's `[+0xC0]+0x180`-indexed option table at `0x1E` stride 8 (`005666D4`–`005666F3`) via `00567690`~~ *(corrected 2026-10-02, OPUS: that walk opens the id-18 arm — the dispatch sends 18 to `00566680+0x54` — and the id-12 arm `00566680+0x114` never branches into `00566680+0x54`–`00566680+0x73`)*
- **id 15** `00566771`: frees `+0xD8` via `0057C340`
- **id 18** `005666D4`: clears the row highlights through `00291D70`/`00291D80`, sets the parent's `+0x180 |= 0x40000000` (sort-changed flag), clears `[global]+0x2F0`
- **id 2** `0056688D` / **id 1** `005668BB`: reconcile / construct

## The screen-region members

Every listed member of the `00566680`/`0057C480` subtrees (union 64, atlas subtree rule) in the
screen region, each with a role and an interior citation (2026-09-15). The remaining **44 listed**
members are shared engine helpers cited as families: the `0024xxxx` widget object model
(`00244F50`/`00246AD0`/`00247510`/`00249C60`/`0024A5A0`), the `002Bxxxx` text layout/draw
(`002B1E20`/`002B3050`/`002B3280`/`002B3400`/`002B3930`), the `002Dxxxx` menu controls
(`002CC9C0`/`002CCB30`/`002D04F0`/`002D3900`/`002D4650`/`002D8550`/`002D8650`/`002D8910`/
`002D8BB0`), `002F9860` string fetch, `002527B0`/`00254F30`/`00291D70`/`00291D80` helpers,
`001EDEC0` FrameLimit mode predicate, `002ABEC0` window records, and `00861EC0`/`00808C40` CRT. **8 call-targets carry no
census entry** — arm bodies inside listed owners.

| member | role | interior cite |
|---|---|---|
| `00566680` | the item-sort bar (997 B) — §above | `0056668A` `mov rax,[rip+0x19de19f]` |
| `00564380` | item-screen `+0x17E`-keyed jump-table dispatcher (7 cases) — sort-bar installer's sibling | `0056439A` `mov edx,[rcx+rax*4+0x444410]` |
| `00565CD0` | sort-bar side installer — `0xB0` frame + rsp-cookie | `00565CE7` `mov rax,[rip+0x19deb42]` |
| `005670F0` | pure pointer walk on `rcx+0x10` — option-table indexer (no calls) | `005670F3` `mov r8,rcx` + `005670FE` `mov rax,[rcx+0x10]` |
| `00567690` | sort-mode option walker — `+0x150` byte count, `002D04F0` per row | `005676FE` `call 002D04F0` |
| `0057C480` | the confirm window (2,088 B) — §above | `0057C4A8` `lea rcx,[rip-0x45c4af]` |
| `0057C140` | confirm-singleton message dispatcher (475 B) — `0x138` frame, rsp-cookie | `0057C155` `mov rax,[rip+0x19c86d4]` |
| `0057C320` | forwarder — loads `[rip+0x1b1e902]`→`+0x328` then tails `0057C140` ("post to the confirm singleton") | `0057C32E` `mov rcx,[rcx+0x328]` |
| `0057C340` | frees `+0xD8`-family field, gated on `+0x630` bit `0x4000` — `002CCB30` | `0057C361` `call 002CCB30` |
| `0057C380` | message packer — `0x48` rsp-cookie frame, `lea r8,[rsp+0x20]` out-param | `0057C38B` `xor rax,rsp` |
| `0057CD00` | `+0x636`-indexed option-slot walk (movzx byte count) | `0057CD0C` `movzx r8d,byte[rcx+0x636]` |
| `0057CD40` | message builder — `0x40` rsp-cookie frame | `0057CD4E` `mov rax,[rip+0x19c7adb]` |

## The layout-key readers

*(2026-09-14, FRONTIER — LAYOUT-KEY-READERS.)* The `uisize.json` readers inside this layer, with the
use-site instruction. The confirm family is read by **two** confirm procs — `0057C480` above and the
`00241D40` variant (atlas "confirm window + message window", installed by `00241BF0`/`00241C90`) —
which share the same `Confirm*` globals.

| reader (→ owner) | keys | what the values do at the use site |
|---|---|---|
| `0057C480` P (confirm window) | `ConfirmCaptionOffsetX/Y`, `ConfirmWindowSelectHeight`, `FontBaseWidth` | caption `edx`/`r8d` → `002D8910` right-aligned draw (`0057C976`, `0057C96C`); `SelectHeight` → `[rbp-0x24]` row height (`0057C719`); `FontBaseWidth` doubled via `lea ecx,[rax+rax]` — the two-column caption measure (`0057C5EE`) |
| `00241D40` P (the second confirm window) | same family + `ConfirmCursorOffsetX/Y`, `ConfirmWindowBaseWidth` | caption/cursor offsets into `002D8910`/`002D8BB0` (`002423AF`, `00242327`, `00242346`); `BaseWidth` is the window-width floor — `cmp`/`cmovl ecx` at `0x60` (`00241E01`); `SelectHeight` → `[rbp-0xD]` (`00241F06`); `FontBaseWidth` doubled (`00241EF5`) |
| `0057C140` (→`0057C320`→`002CDF20`, the confirm-singleton dispatcher) | `ConfirmWindowSelectHeight`, `FontBaseWidth` | `imul eax, SelectHeight` — row height × index for the option slot walk (`0057C236`); `FontBaseWidth` → `r9d` measure arg (`0057C1EC`) |
| `00566680` P (item-sort bar) | `ItemSortWindowOffsetX`, `ItemSortWindowOffsetY` | `OffsetX` word → `[rbx+0x98]` window field (`00566A27`); `OffsetY` `sub`ed twice into the row base (`00566A1A`) |
| `0056F5F0` (→`0056F810` id-1 init) | `mCommandMenuStrHeight` | `eax` = row height, with `movss 1.0` beside it — the list's per-row pitch (`0056F6C7`) |
| `00281AE0` (→`00280DE0`, the menu-list proc) | `mCommandMenuOffsetY`, `mCommandMenuStrHeight` | `OffsetY` → `r8d` position arg (`00281D23`); `StrHeight` → `eax` + `movss 1.0` row pitch (`00281CCD`) |
| `00281ED0` (→`00280DE0`) | `ConfigBlackBandH`, `PartyBlackBandGradH`, `BlackBandAnimTime` | the menu list's band: `ecx`/`edx`/`r8d` → `002C9490` (`002821CA`/`002821C4`/`002821BD`) |
| `0028D460` (→`0028C970`) | `m2DSideCursorCenterX`, `m2DSideCursorCenterY` | `neg ecx` then `movd` — the side cursor's centre subtracted from the anchor point (`0028D6F5`, `0028D718`) |
| `00292390` P (menu list, `ListItem` keys) | `ListItemIconW`, `ListItemIconH` | `IconW`/`IconH` are the column and row counts of the clear and copy loops that write a W×H block into the icon texture — plus the atlas steps `01E0C478`/`01E0C47C` — not an icon-width argument and a height guard (`002925AA`, `002925D0`) |
| `002C9BF0` (→`002C2320` geometry pass) | `MenuListWindowHeightModifer` | `add ecx, edx` — the height modifier added to the list window's base height (`002C9C6A`) |
| `002CD170` P (menu-list marks pane) | `MenuListMarkOffsetX/Y`, `MenuListNewOffsetX/Y`, `MenuListWindowHeightModifer`, `MenuListWindowWidth` | `Mark`/`New` offsets `neg`/`add`ed into `00243030`/`00243160` — the "mark" and "New" badge positions (`002CD220`, `002CD22A`, `002CD1E2`, `002CD1EB`); `WindowWidth`/`HeightModifer` → `cvtdq2ps` → `[rdi+0x9A]` (`002CD361`, `002CD36B`) |
| `002D1750` (→`002D2DB0`, the scroll-bar proc) | `ScrollUpCursorOffsetY`, `ScrollDownCursorOffsetY`, `ScrollMarkOffsetX`, `ScrollMarkOffsetY` | up/down cursor Ys `sub`/`add`ed around `[rbx+0xFA]` (`002D17BD`, `002D17DD`); mark X `sub`ed, mark Y `add`ed (`002D1783`, `002D178F`) |
| `002D2DB0` P (scroll bar / list) | `ScrollBarOffsetPosX`, `ScrollTableFadeHeight` | `OffsetPosX` `sub`ed then `cvtdq2ps` — the bar's X as float (`002D35F5`); `FadeHeight` compared against `[+0x9A]` — the scroll-fade gate (`002D2F7A`) |
| `002CEB40` P (the scroll-mark widget — tail-jump installed) | — | reads no key: the two sites are `lea` end bounds of the `0x10`-stride array at `0209E638` (`002CEC25`) — loop bounds, not a `ScrollMarkOffsetY` read |
| `00247590` (→`002778C0`) | `General_Frame_Shadow_WH` | byte → `[rbx+0xAE]` — the frame shadow's W/H field (`002475A9`) |
| `002475D0` (→`00227EE0`, the message window) | `mGeneralFrameBackOffset`, `mGeneralFrameFrontOffset` | bytes `neg`ed → `[rcx+0xA8]`/`[rcx+0xA4]` — the frame's back/front offsets (`0024763D`, `00247601`) |
| `00247680` (→`00572600`, handbook pane) | `General_Frame_Common_Offset` | byte `neg`ed → `[rcx+0xA4]` — same front-offset field (`0024769A`) |

`0056F810` and `00556F90` read no key directly — the menu list's `mCommandMenuStrHeight` comes in
through its `0056F5F0` init helper, and the message window's `MessageLine`/`NobuMessage` keys are
read inside `002A70B0`/`002AC5F0`-family geometry helpers (covered on the message-window page).

## What these are

~~All four are the reusable leaf layer the labelled screens share: `0056F810` is the list widget every menu embeds (its reconcile arm is where every screen's `+0xF2/+0xF4 × +0xEC + +0xEE/+0xED` cursor math comes from — the screen procedures read it off this child's record, not their own);~~ **Corrected 2026-09-29 (FABLE, GI-4):** two of the four are single-screen widgets — `0056F810` is the Clan Primer category menu (installer `00574D00` only) and `00556F90` the license-board description box (installer `00556EC0` only); the `+0xF2/+0xF4 × +0xEC + +0xEE/+0xED` cursor arithmetic belongs to the list control's record (`002D3900` family), which is why it appears in every screen. `0057C480` is the one-shot choice dialog (three producers: `002CDF20`, `002CE370`, `00566680`); ~~`00556F90` the passive message box;~~ `00566680` the item sort bar. None is a screen — they have no resource load of their own beyond `0x63`/`0x62` and no page state. The atlas's `installed by` column naming them children is structural fact: screens instantiate them.

## The title table, the two single-installer widgets and the `+0x630` word — read 2026-09-29 (FABLE, GI-4)

*Static and authored-data census. Every claim below is a check in [`gi4_dialog_tables.py`](../../_index/candidates/gi-0929-dialogs/gi4_dialog_tables.py) (FAILS 0; output in [`gi4_dialog_tables.out`](../../_index/candidates/gi-0929-dialogs/gi4_dialog_tables.out)), which carries the regression that rejects the struck framing.*

**The `00D23688` table — twelve records `{u16 label; u16 help; u8 key; u8 flag}`, ending where the next object (`00D236D0`, lea'd at `0056EB88`) starts.** The word readers use the record starts (`0056F678` lea `00D23688` → `0056F694`/`0056F69A` into `002CD3C0`; `0056F324`/`00574AA6` lea `00D236A0` → the page title through `002F9860`); every byte reader uses `+4` (`0056F98D` `+0xC0368C`, `005732AC`/`00571ECD` `+0xC036A4`, `0056F795` `[r14+k*6+4]`, `0056EDB4`/`005721EB` via lea `00D236A4`). A rip sweep of the table range finds exactly those seven leas and a displacement sweep exactly those three displacements. Control: under this framing all four menu keys name the handbook page whose title is the menu row's own label; under the struck `{kind, flag, u16, u16}` framing none does.

| record | half | label | help | key | flag |
|---:|---|---|---|---:|---:|
| 0 | menu option 0 | `0x1B5F` Hunts | `0x1F47` "Hunt information and progress." | 6 | 1 |
| 1 | menu option 1 | `0x1B5C` Bestiary | `0x1F44` "Insights on foes you have defeated." | 5 | 1 |
| 2 | menu option 2 | `0x1B5D` Sky Pirate's Den | `0x1F45` "What will it take to fill the den?" | 7 | 1 |
| 3 | menu option 3 | `0x1B5E` Traveler's Tips | `0x1F46` "Hints for the wary adventurer." | 4 | 2 |
| 4–7 | handbook kinds 0–3 | `0x1B58`/`59`/`5B`/`5A` placeholder | `0x1F40`/`41`/`43`/`42` | `0x0B`–`0x0E` | 0 |
| 8 | handbook kind 4 | `0x1B5E` Traveler's Tips | `0x1F46` | `0x0F` | 0 |
| 9 | handbook kind 5 | `0x1B5C` Bestiary | `0x1F44` | `0x11` | 0 |
| 10 | handbook kind 6 | `0x1B5F` Hunts | `0x1F47` | `0x10` | 0 |
| 11 | handbook kind 7 | `0x1B5D` Sky Pirate's Den | `0x1F45` | `0x12` | 0 |

The placeholder titles are one shared row of `penelosdiary.bin` in all nine locales — empty in us/it, "NOT USED" in fr, "DUMMY" in es. **The menu key** is the handbook page kind the option opens: posted as the argument of sub-command `0x8001` (`0056F9A5`–`0056F9B5`), and it gates the option through `00577550(kind)` and `00576550(kind)` in `0056F750`/`0056FAD0` (option 2 skips `00577550`; options 0–2 also need flag `0x400B`; kind 7 skips `00576550`). **The handbook key** is the page's slot in saved-cursor bank 6: `002527B0` is three clamped stores into `[020927C0]` (`+0x30` words, `+0x70` bytes, `+0x90` dwords — banks 6/7/8) and releases nothing; the pages store their cursor with it (`005732B8`, `00571EDB`), restore it with `002526F0` (`005721F3`) and zero it with `00252610` (`0056EDDC`), always with bank 6. The handbook half's help word and every flag byte have no reader.

**`00556F90` is fed by the license board.** Its only installer is `00556EC0` (`00556EF3`), called only from `00557DB0` (`00557E76`, `00557EE5`), which seeds `+0x3D1` with its board index and rewrites it on each cursor step (`00558549`); the id-2 arm (already read on [the message-window page](../Message-Windows/the-message-window-layout-readers.md)) fetches title `0x3ED + board` — the twelve board names, White Mage … Shikari — and body `0x838 + board`, the board description ending "Preview License Board".

**The confirm window's `+0x630`** is the create record's `+0x20` (`0057C4E4`/`0057C4E8`). Its only creator `0057C380` has exactly three callers, each passing constants:

| producer | flags | what it is |
|---|---|---|
| `002CDF20` (installed by `002CDEA0`) | `0xC812` | the Yes/No question (`0x3E8` Yes → `0x8100`, `0x3E9` No → `0x8101`, default row 1) — license-board and license-obtain questions |
| `002CE370` (installed by `002CE2F0`) | `0x411A`; `0x511A`, `0x1411A`, `0x1511A` for error toasts; `0x611A` for tutorials and license announcements | the notice (28 caption cases) |
| `00566680` | `0x8036` | the item sort picker ("Sort") |

| mask | effect (test site) |
|---|---|
| `0x2` | cancellable — cancel posts `0x8102` to the owner (`0057CAD1`); else cancel only moves the list cursor to the default row |
| `0x8` | notice mode — no list child is built (`0057C6F3`), input reads the pad directly, `0x8001` posts `0x8100` straight to the owner |
| `0x10` / `0x2000` | frame variant 1 / 4 for `002475D0` (`0057C7EE`–`0057C802`) |
| `0x20` | single-line caption measure and draw (`0057C506`, `0057C90F`) |
| `0x800` | holds the hand pointer on the highlighted row while the window closes — list child `+0xE4` bit `0x80` (`0057C7CC`); see "Mask `0x800`" below |
| `0x1000` | timed dismiss over `+0x63A` (`002CE370` sets 180 frames) (`0057C9E1`) |
| `0x4000` | dimmed backdrop layer at `+0xD8` (`0057CD77`), released on close (`0057C34A`) |
| `0x8000` | header label `0x4B42` instead of `0x4B48` (`0057C93E`): "SELECTION" instead of "INFO" (de "AUSWAHL"/"HINWEIS"; empty in us) |
| `0x10000` | any button confirms, and the timed dismiss answers confirm (`0057CA16`) |
| `0x4`, `0x40`, `0x80`, `0x100`, `0x200`, `0x400` | confirm-sound class: the list's `+0xFC` decide-sound id becomes `0x37`, `0x19`, `0x18`, 3, 4, `0x45` (`0057CB8F`–`0057CBD7`); "No" (`0x8101`) takes 3 |

The `+0xFC` byte `0057CB16` writes is the embedded list's decide sound: the list reads it after its owner declines the `0x8001` pick and plays it (default 2, `-1` silent) at `002D4114`. No producer sets `0x40`, `0x80`, `0x200` or `0x400` — those sound classes are dead in the shipped image.

**Mask `0x800`, read 2026-09-29 (FABLE, GI-4 follow-up).** Only the Yes/No question `002CDF20` passes it (`0xC812`). It ORs bit `0x80` into the option list's `+0xE4` (`0057C7CC`), next to the bit `0x40` every list gets from its constructor (`002D1643`). On each reconcile pass the list (`002D2DB0`, arm `002D37AE`) walks from itself up its `+0x10` parent chain; every node must be enabled (`+0x40` bit 0) and still live (bit 3), and the focused widget (`0208EBC0`) must be on the chain. A node that has started a transition arms a hold when it is **running forward** (state 2 of the `+0x7C` nibble, list bit `0x40`) or **running backward** (state 4, list bit `0x80`, `002D3829`). The hold calls `002D4330`, which retargets the shared hand pointer (`00368360`) to the list's highlighted row without changing the selection. So the mask asks the question to keep the pointer on its row while the window **closes**, as every list does while it opens. It does not act on the player's own answer or cancel: both clear the window's `+0x40` bit 3 (`0057CAE9`) before the close, so the walk stops at the window. It can act only when the question closes still unanswered — through the license screens' closer `002CE2D0` (five call sites in `0055C740`, `0055CD40` and `0055F3E0`), which destroys whichever host is registered at `[0209AC30]+0x2E8`; whether that ever happens with focus inside an open Yes/No is not settled statically (a runtime check: break on `002CE2D0` with a Yes/No open and read `0208EBC0`). *(Check: [`gi4_mask800.py`](../../_index/candidates/gi-0929-dialogs/gi4_mask800.py), FAILS 0.)*

*Out of this row (a note, not residue):* the cue names behind sound ids 3 / 4 / `0x18` / `0x19` / `0x37` / `0x45` are not resolved.

## Not yet established

- ~~`00556F90`'s id-2 arm (how the message text is fed)~~ — **answered 2026-09-29 (FABLE, GI-4):** pulled by the license board's index ([§ The title table](#the-title-table-the-two-single-installer-widgets-and-the-0x630-word--read-2026-09-29-fable-gi-4))
- ~~the `0xC0368C`/`0xC036A4` shared lookup tables' full contents~~ — **answered 2026-09-29 (FABLE, GI-4):** twelve `{u16 label, u16 help, u8 key, u8 flag}` records from `00D23688` (same section)
- ~~the `+0x630` flag classes' full semantics beyond the classes `0057CB16` maps to `+0xFC` result bytes~~ — **read 2026-09-29 (FABLE, GI-4)**, mask `0x800` by the follow-up paragraph "Mask `0x800`" (same section)
- **answered 2026-09-29 (FABLE, GI-4 follow-up):** what `+0x630` mask `0x800` does for the player — it holds the hand pointer on the highlighted row during the window's closing transition, and acts only when the question closes unanswered (["Mask `0x800`"](#the-title-table-the-two-single-installer-widgets-and-the-0x630-word--read-2026-09-29-fable-gi-4))

## Falsification pass

**Pass 1 — 2026-09-14 (OPUS).** Attacked at parent `GN160` (`fa0db293…`), EXE `73461d08…`.
Instrument: `Tools/work/OPUS/falsify_shop_dialogs.py`. **Six claims attacked, five survived.**

| claim | the killer | result |
|---|---|---|
| `0056F810` dispatches through the table at `0056FA80` | a different table | **survived** |
| its ids are 1, 10, 12, 14, 15, 18 *(the heading)* | the image answering a different set | **survived — exact** |
| its bullets' id→arm pairs *(the bullet list)* | the image answering a different set, or an arm elsewhere | **FALSIFIED** — `0056F889` is id 14, `0056FA09` is id 18, and id 2 is the default |
| `0057C480` answers 1, 2, 4, 10, 12, 18, 19 through `0057CCA8` | any other id reaching a real arm | **survived** — seven ids, seven arms |
| `0057C480` stores `self` into `[global + 0x328]` at `0057C4D9` | that address not being such a store | **survived** — `mov qword ptr [rax + 0x328], rsi` |
| `00556F90` answers 1, 2, 18 with **no input and no sub-command arm** | id 10 or id 12 reaching a real arm | **survived** — `{1, 2, 18}` and nothing else |

> **The one that failed is the page disagreeing with itself**, and that is worth more than a wrong
> address: a heading and a bullet list stated different id sets, and nothing in the kit compares two
> statements *within* one page. `check_self_contradiction` works at address level, not at the level
> of "this table says the widget answers id 2 and this one says it does not".

**The never-claim held this time.** `00556F90`'s *"No input arm, no sub-command arm"* is exact — ids
10 and 12 both resolve to its default. The last never-claim attacked, `0057E610` in
[the save/load widgets](../../19-Save-Load-Settings/the-save-load-screen-widgets.md), was false, so
this one was tested the same way rather than assumed.

**Not attacked:** the arm interiors — the `0xC0368C` lookup in `0056F810`'s id-12, the confirm
window's option-slot layout beyond the zeroing, and the message window's scroll behaviour.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Items_Equipment_Shops_License — SERVICE.** `002C2320` on this page calls `Equipment_CheckPrimarySecondaryPairReasonByStatsIndex`, owned by that layer. What it reaches is the pair check over the same `0x1C8`-byte stats records: the index is bounded at **`0x27`**, and with no explicit second operand it takes the record's own `+0x50` word; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — CLIENT (8 edges through 2 of this page's functions).** The Party layer reaches this page at `003589B0`, `00265020`. `FUN_00303cc0` is the worked example, read in full - it is a 205-byte step that runs only when the mode query answers **2**, and then works through selector `3`; **3 of the 8 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT (SWE2-CONTRACT 2026-09-15, 24 edges).** The shared dialogs are driven by the render layer's
UI machinery: `002BAF80`/`002B7B80`/`002BC3E0` (InputConsumer/AnalogCursor state machines, 6 edges)
drive `001EDEC0`/`002470D0`/`00249C60`/`002CC9C0`; `00579420` (quest-list selection, 4 edges) drives
`002470D0`/`00247510`/`002527B0`/`002D3900`; ShaderMaterial `00366B80`/`0035C160`/`00578450`,
ScreenCapture `002D2DB0`, `TargetLine.Runtime` `00291320`, `PartyGuardEffect.Runtime` `002CE7E0` and
`00506700`/`003F70F0`/`003F3710` reach `001EDEC0`/`0024A5A0`/`002B3050`/`002B3400`/`002D3900`/
`002D8650`. The dialogs are widgets the render pass calls — the crossing is the draw/input path.

**ActorEntity — SERVICE (SWE2-CONTRACT 2026-09-15, 4 edges).** The dialog bodies anchor to actors: `002B7B80` calls `Actor_GetWorldPosition` `00265020` and `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0`; `00506700` calls `ActorHandle_EncodeRegistryEntry` `003589B0`; `00291320` calls `00273780`. Dialog icons resolve the actor they attach to — a small service call set, not shared ownership.

`00367110` (227 B) is the alignment-mode offset calculator `00366B80` calls per row: a four-way switch on the mode selects how `word[+0xC]`/`+0xE` combine with extents `+0x10`/`+0x12` - raw, `+0xC + (+0x10 >> 2)`, `+0xC - (+0x10 >> 1)`, and the fourth variant - yielding the s16 x/y pair the dialog row is positioned with; `00862980` closes the frame and `00808C40` is the cookie.

Interior anchor `003671CB` (function `00367110`).

*Added 2026-09-29 (FABLE, GI follow-up): the layers the GI answers newly brought into, or widened on, this page's audit.*

**PlatformOnlineAchievements — SERVICE and DEPENDENCY (2 edges).** The two handbook option gates this page reads in `0056F750` / `0056FAD0` call into the achievement-counter family: `00576550` calls the category tester `003154B0`, and `00577550` calls the re-check sweep `00316930`. Whether a handbook option is offered therefore depends on award and counter state that family evaluates; the dialog only asks.

**Resource — SERVICE, MECHANICAL (8 edges).** The menu-list proc `00280DE0` calls `0024A5A0`, a lookup that walks a 64-entry, `0x48`-stride registry comparing a name string and returns the matching entry (or 0); `00281AE0` calls `0024A5A0` and `00249580`, which claims the first free slot of a 12-entry, 32-byte table and stores its argument there; the `ListItem` menu list `00292390` calls the image member callback `0024A1D0` (the `"%s%03d"` name builder); the scroll-mark widget `002CEB40` calls `0032E4D0`, which answers whether a resource request ticket (table indexed by the id's low six bits, `0x80` stride) is live and ready; and the handbook back panel `00574E80` calls `00249580`, `003933F0` (requests one kind-7 resource per id in a list) and the record-factory fan-out `003934F0`. The widgets obtain their names, slots and resources through the resource layer's registries and request tickets; the resource layer owns those tables, and the dialog pages own only what is drawn from them.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22, FRONTIER's debt (SWE2-FRONTIER, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, `SWE2-FRONTIER-PASS22-DEBT-OWN`): the layers pass 22 still reported for this page at HEAD `9a4cd5784`. Every edge was listed in full and the cited function's body was read.*

**Save_Load_Settings — CLIENT (7 edges).** `00247510` (95 B) sends a widget message. It builds a message of kind `0xC` with the caller's two arguments on the stack. When the object and its handler at `[obj+0]` are non-null, it calls the handler with that message; otherwise it returns 0. The save and load controllers use it to notify their listener: `0057E950`, `0057EBB0`, `SaveLoad_FullImageStorageCompletionCallback` (`00580840`), `SaveSlotScan_ControllerCallback` (`005819F0`), `SaveSlotProbe_StorageCompletionCallback` (`00581B70`) and `SaveLoad_ControllerLifecycleHandler` (`00582860`). For example, `00581B70` posts `0x1D` to the object at its `+0xC0` (`00581D41`–`00581D52`), and `00582860` posts `0x8001` (`00582B0B`–`00582B19`). `00582860` also calls `001EDEC0` on its `+0xB4` (`00582A31`–`00582A37`), the FrameLimit mode predicate of CONTRACT-boot-fixups 13c/13d: 1 unless the mode is on and unsuppressed, then (~arg) & 1. The save layer uses these helpers to talk to its dialogs and owns nothing on this page.
