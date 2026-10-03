---
id: ui-handbook
title: The handbook screen — the back panel, the page viewer, and the order file
status: "DOCUMENTED — GI-2 answered 2026-09-29 (FABLE), review (FABLE-REQ-AUDITSEM-REVIEW-GI-DIALOGS, ACCEPT, d998217e2); documented_rule.py READY, no open box or live id; owner re-status 2026-09-30 (SWE2-FRONTIER, record dd-restatus-gi-0930). Was PARTIAL on: the hcom node semantics and the hodr link pair's traversal are not established; menuhandbook_order.bin's record format and the 0xC036A4 map resolved 2026-09-16; 0056EF60's role read 2026-09-18 (the content-pane host)"
evidence_tier: 1
tags: [ui, handbook, menu-screens]
addresses:
  - "00574E80"
  - "00572E10"
  - "00572460"
  - "00572600"
  - "0056EF60"
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation delta - every function this document cites whose record differs between the stamped snapshot and GN161's gained a plate comment and tags ONLY (empty comment before, tag set a subset, checked field by field), and this document makes no uncorrected absence claim about any of them; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 2 cited address(es) among the 128 records changed across GN158..GN161; each differs only in comment and tags; 0 live absence claims (check_stranded_absence.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-DELTA-RELIANCE-BASIS; re-measured and applied for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-14
falsification_passes: 1
archive_formats:
  - "hcom | explained | menuhandbook.bin (.bin member): {hcom, u32 103, u16 self-relative node web, u32 constants} - (kind 7, 0xC8) by 003158B0 into 022C2550, walked by 00315D50; node semantics settled 2026-09-29 (GI-2): five length-prefixed sections, not a node web"
  - "hodr | explained | menuhandbook_order.bin (.bin member): {hodr, u32 101, u32 33, 32-byte records[33]} (12 + 33*32 = 1068) - (kind 7, 0xC9) by 00572D80 into rbx+0x1200, placement walk 00572460; the +0x16/+0x17 pair settled 2026-09-29 (GI-2): statue effect ids, not links"
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: opus-handbook-screen-pass-1 - sixteen claims attacked by decoding the image at GN160 and ALL SIXTEEN SURVIVED; both dispatch tables reproduce exactly (bound, compare address, table address, every arm and the default), all four leaf id sets are exact, and all seven installer claims hold. No correction. One gap filled rather than falsified: 0056F410 answers id 1 at 0056F428, where the page had said only that no ids were listed
  crossref_clean: false
  reopened_count: 0
---

# The handbook screen

**Status:** ~~PARTIAL~~ DOCUMENTED *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`, GI-2 answered 2026-09-29)* — both dispatch tables, the install chain, and every listed screen-region member are cited below with interior citations (2026-09-15); the 93 shared listed subtree members are cited as engine-helper families. The `menuhandbook_order.bin` record layout is read only through `00572460`'s page descriptor walk.

## The tree

The handbook is a two-screen composite: `00574E80` is the **back panel** (it requests `HandBack2_c.tm2`, installed by `00574CB0`/`00575580`), and it installs `0056EF60` — the pane whose own subtree member `0056EE10` installs `00572E10`, the ~~**content viewer**~~ **Sky Pirate's Den screen** (page kind 7 only; corrected 2026-09-29, FABLE, GI-2) that requests `menuhandbook_order.bin` and drives all four menu-effect-registry calls. The remaining handbook-labelled rows are panes of these two:

| procedure | role | installed by |
|---|---|---|
| `00574E80` | handbook back panel (outer screen) | `00574CB0`, `00575580` |
| `0056EF60` | mid pane | `00574E80` |
| `0056EA40` | leaf pane (ids 1,3,18,19) | `00574E80` |
| `00570890` | leaf pane (ids 1,18) | `00574E80` |
| `0056F410` | leaf pane (id 1 only — construct) | `0056F3C0`, `00574E00` |
| `0056F550` | leaf pane (ids 1,18) | `00574D00` |
| `00572E10` | ~~handbook content viewer~~ **the Sky Pirate's Den screen** (page kind 7 only; corrected 2026-09-29, FABLE, GI-2) | `0056EE10` (inside `0056EF60`'s subtree) |
| `00572460` | page descriptor | `00572E10` |
| `00572600` | ~~page view~~ **statue description popup** (corrected 2026-09-29, FABLE, GI-2) (ids 1,10,14,15,18) | `00572E10` |

`00574CB0`/`00575580` are the `00574E80` installers and `0056EE10` is the `00572E10` installer — all installer-family bodies, consistent with the label being structural.

## `00574E80` — the back panel

Dispatches `msg->id` bounded to `0x11` at `00574EA5` through the table at `0057552C`:

| id | arm | role |
|---|---|---|
| 1 | `00574EC4` | construct: window dims from globals into `+0x98`/`+0x9C`/`+0x9E`, zeroes the three child slots `+0xD8`/`+0xE0`/`+0xE8` (`00574EF2`), registers the screen pointer globally at `00574ED2` |
| 2 | `00575144` | reconcile: when `+0xC0 & 8` and not `0x10`, waits on `002CD7D0` then `00244F00` and sets `+0xC0 \|= 0x10` (`0057516A`–`0057516F`) |
| 12 | `0057517D` | sub-commands `0xE`, `0xF`, `0x12`, `0x13`: `0x12` with arg 2–6 clears the `+0xF0`/`+0xF8`-family refs (`005751D9`–`005751F7`); `0xE` → `00575381`, `0xF` → `005752BB`, `0x13` → `005753C3` |
| 14 | `005750C2` | transition: `00574E00` + `00574D00` + `00244F50` create with record `{0xC8, self, +0x128}` (`005750D2`–`005750FD`) — installing a pane |
| 16 | `00574FC7` | refresh: sets `+0xC0` bits on `msg->a` (1→bit2 at `00574FE5`, 2→bit3 at `00574FDC`), creates a `0x100` record via `00244F50` (`00575017`) |
| 18 | `00575498` | destroy: `00393900`/`003938B0` on `+0x118`/`+0x128`, `005755D0`, and if the parent's `+0xC0 & 0x20` swaps its own vtable to `lea 0057...` (`005754D6`) and clears the global pointer; else requests `0x4BC` |
| 3–11,13,15,17 | `00575505` | default → `005C5230` |

The panel is a frame: it owns the `HandBack2_c.tm2` background, three child slots, and forwards lifecycle ids. It never reads handbook content itself.

## `00572E10` — the content viewer

**Corrected 2026-09-29 (FABLE, GI-2):** this procedure is the **Sky Pirate's Den** screen, not a viewer generic over the handbook's chapters — `0056EE10` installs it only for page kind 7; see [§ The Sky Pirate's Den](#the-sky-pirates-den-and-the-two-data-files-decoded-2026-09-29-fable-gi-2). The arm table below is exact; the struck role words are corrected in place.

Dispatches `msg->id` bounded to `0x12` at `00572E35` through the table at `005733A0`:

| id | arm | role |
|---|---|---|
| 1 | `00572E54` | construct: `msg->arg` → `+0xC0` (ptr) / `+0xC8` (page kind byte) / `+0x11D8` (arg+0x10); zeroes an inline `0x1100`-byte record array at `+0xD0` via `00861EC0` (`00572EBB`); ~~`+0xCB` = `0x1E` default count~~ `+0xCB` = `0x1E`, the selected statue with `0x1E` meaning none (corrected 2026-09-29, FABLE, GI-2); `00249580` + `0057A2D0` installs a child at `+0x11F8`; `00394700` + `00247930`(0x64) layout/resource; posts id 1 to `[global + 0x100]` (`00572F02`) |
| 2 | `00572FE3` | reconcile → `00573980` then the shared `00572F02` tail |
| 10 | `00573078` | directional input, only when `+0xC9 == 5` (page mode): pad-mask tests; one key calls `00572890` + `00249C60`(3) (`00573097`), ~~another runs the index math on `+0xCB` bounds (`005730AD`–`00573136`)~~ with a statue selected, confirm opens the `00572600` description popup (`005730CF`–`00573123`) and a direction key picks the nearest statue that way through `00572BD0` and reselects it through `005734C0` (`00573136`–`0057317E`) (corrected 2026-09-29, FABLE, GI-2) |
| 12 | `005731A7` | sub-commands `0xE`, `0x12`, `0x8100`–`0x8102`: `0xE` with arg `0xC` → `00572920` + `005704A0` (`00573244`) — ~~page select~~ builds the statue groups (corrected 2026-09-29, FABLE, GI-2); `0x12` clears `+0x11E0`/`+0x11E8` refs; `0x8100`–`0x8102` → `005704A0` + `+0xC9` = `0x1004` (`005731D2`) — transition state |
| 14 | `00573376` | transition started — immediate return |
| 15 | `0057325E` | about-to-destroy: `002470C0` + `002CD800`/`002CD880`(0x62) — releases resource `0x62` |
| 16 | `00572F23` | refresh: `+0x11D0 & 1` is a page-built flag — if **clear**, `005738D0` builds the page, `003B29B0` fx-reset on `+0x11F8`, `003697F0` frees it, `00572D80` cleans, then sets the flag (`00572F31`–`00572F68`); if **set** (`00572F74`), it sets `+0x98`/`+0x9C`/`+0x9E` dims and posts to `[global + 0x100]` via `00247870` |
| 18 | `0057328D` | destroy: `002527B0` ~~with a resource id looked up from table `0xC036A4` indexed by `+0xC8` (`005732A8`–`005732B8` — page kind → resource)~~ stores the selected statue `+0xCB` into saved-cursor bank 6 at the slot the `0xC036A4` key byte gives for kind `+0xC8` (`005732A8`–`005732B8`; corrected 2026-09-29, FABLE, GI-2), `00393900` on `+0x11F0`, `002F83E0`(0x18) if `+0x11D0 & 2`, frees `+0x1200` and `[global + 0x100]` |
| 19 | `00572FED` | builds a `{0xD8, self, +0x11F0, +0x11D8}` record and posts it to the `00572460` child (`lea rdx` → `00572460` at `00573008`) |

~~The `+0xC8` byte is the page kind and `0xC036A4` its resource table — the viewer is generic over the handbook's chapters; `menuhandbook_order.bin` supplies the page ordering the `+0xCB` count and the index math walk.~~

**Corrected 2026-09-29 (FABLE, GI-2):** `+0xC8` is always 7 here (the Den), the `0xC036A4` byte is a saved-cursor slot, not a resource, and `menuhandbook_order.bin` is the Den's statue layout; `+0xCB` is the selected statue. See [§ The Sky Pirate's Den](#the-sky-pirates-den-and-the-two-data-files-decoded-2026-09-29-fable-gi-2).

## The children

- `00572460` (412 B, ids 1,3,14,15,18): the page descriptor. Its id-3 draw arm (`005724D3`–`00572572`) walks the record at `[+0xD0]+0x20 + 0x30` — a word-indexed table of 8-byte entries (`+0x14` word index, `+0x10` base offset, per-entry x/y words plus two 12-bit nibbles at `+4`/`>>0xC` and a flags byte at `+7` split into hi/lo nibbles) — the glyph/sprite placement list for one handbook page. Ids 14/15/18 forward `0xE`/`0xF`/`0x12` to the `+0xC0` parent (`005724AF`–`005724C6`).
- `00572600` (654 B, ids 1,10,14,15,18, `General` layout keys): ~~the scrollable page view — the only child with a directional arm, so it owns the page cursor.~~ **Corrected 2026-09-29 (FABLE, GI-2):** the statue description popup. The Den creates it when a statue is confirmed (`005730EC`); its construct shows title `0x1B68` + achievement id and text `0x5DDE` + id and takes its window position from the statue record's `+0x0A`/`+0x0C` (`00572742`–`005727CF`), and its id-10 arm only closes it on confirm or cancel (`005726A7`–`005726CF`). The Den's own cursor is `+0xCB` of `00572E10`.
- `0056EF60` (830 B): the mid pane that hosts the viewer; its subtree carries `0056EE10` (the `00572E10` installer) plus `00570BF0`/`00576740`/`00579990`/`00579A40` helpers.
- `0056EA40`, `00570890`, `0056F550`, `0056F410`: leaf panes — construct/destroy plus one draw or notify arm each; `0056F410` has no listed message ids (a pure install record).

## The screen-region members

Every listed member of the nine handbook subtrees (`00574E80`, `00572E10`, `00572460`, `00572600`,
`0056EF60`, `0056EA40`, `00570890`, `0056F550`, `0056F410` — union 170, atlas subtree rule) living
in the screen region `0x56xxxx`–`0x57xxxx`, each with a role and an interior citation
(2026-09-15). The remaining **93 listed** subtree members are shared engine helpers cited as
families, each named with its representative members: the `0024xxxx` widget object model
(`00244F50`/`00246AD0`/`00244F00`/`00245020`/`00247510`/`00247870`/`00247930`/`00247920`/
`0024B270`/`0024B3A0`/`0024C550`/`0024F410`/`0024F610`/`00252610`/`0028F570`), the
`002Cxxxx`/`002Dxxxx` menu controls and text draws (`002CC960`/`002CCB10`/`002CCCA0`/`002CD150`/
`002CD7B0`), the `00315xxx`/`00316xxx` **PlatformOnlineAchievements** data accessors the
page-select path reads through `00576E10` → `003154B0` (`00315390`/`003153F0`/`00315470`/
`003154B0`/`00315620`/`00315910`/`00315AD0`/`00315B50`/`00315DC0`/`00315E90`/`003162E0`/
`00316480`/`003165B0`/`003165C0`/`00316670`/`003166F0`/`00316930`), the `003B2xxx` menu-effect
registry and its Presentation boundary (`003B0130`/`003B1310`/`003B28F0`/`003B29B0`/`003B2AA0`/
`003B2B40`/`003B2BC0`/`003B2D80`/`003B2F50`), the `003A7xxx`/`003A9xxx` effect-record accessors
on the `02EBEFxx` tables and the EFX loader (`003A76F0`/`003A79C0`/`003A7B50`/`003A7D00`/
`003A7E80`/`003A9560`/`003A9730`/`003A9920`/`003A9A70`/`003A9CC0`, `003EDAD0`/`003EE2D0`), the
`00367820`/`00368010`/`00368360`/`003687C0`/`003688E0`/`00368A60` UI transform evaluator with its
`001E0A10`/`001E0E30`/`001E0E50` Input predicates, the `0039xxxx` resource/TIM2/font helpers
(`003933F0`/`00393460`/`003934F0`/`003938B0`/`00393900`/`00394850`/`003949B0`/`0039BB60`), the
text-emit and leaf layer (`0017FA50`/`001816F0`/`001B1F80`/`0036DD90`/`0036DDA0`/`00374930`),
`002F9860`/`002F8040`/`002F83E0`/`002FBEF0`/`002EFD20` string fetch and resource-slot test, and
`0024A4E0` the `Resource`-owned text-label create (`0024A536`/`0024A569`),
~~`002527B0`/~~`002CD7D0`/`002CD800`/`002CD880` resource release *(corrected 2026-10-02, OPUS: `002527B0` is no release — it stores a value into one of three banks at `[020927C0]`, `002527B0+0x7`–`002527B0+0x69`)*, `003BD6F0` the pane record
rebuild, and `00808C40`/`00861EC0`/`00235DC0` CRT helpers. **25 call-targets carry no census
entry** — arm bodies inside listed owners.

| member | role | interior cite |
|---|---|---|
| `0056EA40` | leaf pane (ids 1,3,18,19) | `0056EA8B` `call 00247510` |
| `0056EC10` | pane child create — `00244F50` + `0058454D` + `00808C40` | `0056EC21` `mov rax,[rip+0x19d5c08]` |
| `0056ECC0` | pane refresh — `00247510` + `00252610`/`002527B0` + `003678F0`/`00368A60` + `0056ED98`/`00574A90` | `0056ED00` `mov rax,[rip+0x273aa11]` |
| `0056EE10` | `00572E10` installer | `0056EE16` `mov rax,[rip+0x19d5a13]` |
| `0056EF60` | the mid pane (830 B) — hosts the viewer | `0056EF66` `mov rax,[rip+0x19d58c3]` |
| `0056F2A0` | `00574E80` subtree helper — `002493D0`/`00249410`/`00249580`/`0024A680` + `002F9860` + `005704E0`/`00574A00`/`005776D0`/`00577880` | `0056F2CF` `call 005776D0` |
| `0056F3C0` | `0056F410` installer | `0056F3C4` `mov rax,[rip+0x19d5465]` |
| `0056F410` | leaf pane, id 1 only — construct (`003946B0` r8d=0x17, `0056F470`, `00394700` edx=2, `00247930` `+0x44`=0x64) | `0056F432` `call 003946B0` |
| `0056F470` | leaf helper — `00315390` (the recomputed clan rank) → `00394850` display call | `0056F482` `call 00315390` |
| `0056F550` | leaf pane (ids 1,18) | `0056F58E` `call 00247510` |
| `005704A0` | page-select path — `rip`-table `+0x273926d` | `005704A4` `mov rax,[rip+0x273926d]` |
| `005704E0` | pane helper — `002CCCA0` + `002CD150` | `005704E4` `mov rax,[rip+0x273922d]` |
| `00570890` | leaf pane (ids 1,18) | `005708CE` `call 00247510` |
| `00570BF0` | pane child create — `00244F50` + `00576030` + `00576740` | `00570BFF` `mov rax,[rip+0x19d3c2a]` |
| `00572460` | the page descriptor (ids 1,3,14,15,18) — §children | `005724C1` `call 00247510` |
| `00572600` | ~~the scrollable page view (ids 1,10,14,15,18) — owns the cursor~~ the statue description popup (corrected 2026-09-29, FABLE, GI-2) | `0057264D` `call 00247510` |
| `00572890` | directional helper — `00247510` + `002CCCA0`/`002CD150` | `00572896` `mov rax,[rip+0x2736e7b]` |
| `00572920` | ~~page-select~~ Den statue build: a group per awarded achievement, `0xFF` records anchored through `003165B0` (corrected 2026-09-29, FABLE, GI-2) — `003165B0` + `003B2AA0`/`003B2D80`/`003B2F50` + `00576E10` | `0057294B` `call 00576E10` |
| `00572BD0` | `003BD6F0` + `00202C90` + `00808C40` — ~~record refresh~~ picks the nearest other statue in the pressed direction from the records' `+2`/`+4` positions (corrected 2026-09-29, FABLE, GI-2) | `00572BDE` `mov rax,[rip+0x19d1c4b]` |
| `00572D80` | ~~post-build cleanup — `00249580`~~ a resource requester: opens a batch (`00249580`), requests through `002491B0`/`00249210` (`00572D80+0x45`, `00572D80+0x6B`) and tail-jumps to the seal `00249410` (`00572D80+0x88`) *(corrected 2026-10-02, OPUS)* | `00572D8D` `call 00249580` |
| `00572E10` | ~~the content viewer~~ the Sky Pirate's Den screen (corrected 2026-09-29, FABLE, GI-2) (1,422 B) — §above | `00572E1F` `mov rax,[rip+0x19d1a0a]` |
| `005733F0` | viewer helper — `00368360`/`00368A60` + `00808C40` | `005733F4` `mov rax,[rip+0x19d1435]` |
| `005734C0` | ~~menu-effect reset~~ selection change: redraws the old statue with its `+0x16` effect and the new one with `+0x17` (corrected 2026-09-29, FABLE, GI-2) — `003B2AA0`/`003B2D80`/`003B2F50` | `00573510` `call 003B2AA0` |
| `00573690` | menu-effect reset + `0056EFE9` arm call | `00573738` `call 003B2AA0` |
| `005738D0` | page build — `00247730`/`00247920`/`0028F570` | `005738D6` `mov rax,[rip+0x1b27353]` |
| `00573980` | reconcile body — `00244F00` + `002CCCA0`/`002CD150` + `002F9860`/`003949B0` + `003B28F0`/`003B2B40` + `00572890`/`00573690`/`005738D0`/`00573A00` | `005739F8` `call 00244F00` |
| `005749B0` | child teardown — `00244F00` + `00245020` | `005749B4` `mov rax,[rip+0x2734d5d]` |
| `00574A00` | pane create/destroy — `00244F00`/`00244F50`/`00245020` + `00808C40` | `00574A04` `mov rax,[rip+0x19cfe25]` |
| `00574A90` | string helper — `002F9860` + `00574A00`; `lea rax,[rip]` table | `00574AA6` `lea rax,[rip+0x7aebf3]` |
| `00574D00` | pane installer (also `0056F550`) | `00574D0A` `mov rax,[rip+0x19cfb1f]` |
| `00574E00` | pane installer (id 14 path) | `00574E06` `mov rax,[rip+0x19cfa23]` |
| `00574E80` | the back panel (1,708 B) — §above | `00574E8F` `mov rax,[rip+0x19cf99a]` |
| `005755D0` | destroy helper — `0024A5A0` | `005755DF` `mov rax,[rip+0x1896c12]` |
| `00575640` | message post — `0017FA50`/`0017FA70` + `00247510` + `003697F0`/`0039BB60` + `00575A10` | `00575674` `call 00575A10` |
| `00575A10` | `0024A680` leaf | `00575A27` `call 0024A680` |
| `00575A50` | `00575640` + `00575C30` pair | `00575B20` `call 00575640` |
| `00575E80` | `00265270` + `00315470`/`00315620`/`0032A8A0` — gated record read | `00575E93` `call 00315470` |
| `00575F10` | `00244F00` + `00575640` — destroy+notify | `00575F14` `mov rax,[rip+0x273381d]` |
| `00576030` | `+0xC9`==1 gated descriptor fill on `[rip-global]+0x108` — `+0xD2` family ordinal + `hctg` header words | `00576037` `mov rdx,[rax+0x108]` |
| `005760A0` | detail-panel resolver — name/subtitle/flag/kill-count/tail slots into the descriptor | `00576104` `mov rcx,[rdx+0xF0]` |
| `00576740` | `00576A50` + `00576CA0` pair | `0057674C` `mov rax,[rip+0x2732fe5]` |
| `00576860` | `edx`==5-gated fetch on `+0xF0` — returns `[+0xC]`-based record or 0xFF | `00576863` `cmp edx,5` |
| `005768E0` | `edx`==5-gated `+0xF0` walk — `movsxd r8d*0x10` index, reads `[rax+rcx+0xE]` word | `005768E3` `je` short + `00576902` `shl rax,4` |
| `00576E10` | `003154B0(7, cl)` → bool (`setne`) | `00576E19` `call 003154B0` |
| `00577100` | child create — `00244F50` + `00808C40` | `00577104` `mov rax,[rip+0x19cd725]` |
| `00577550` | kind-5 record set — `00315910`/`00315AD0`/`00316930` + `00575E80`/`00576860`/`005768E0` | `00577554` `mov r11,[rip+0x27321dd]` |
| `005776D0` | `00247510` post + `00575640` | `005776D6` `mov rbx,[rip+0x273205b]` |
| `00577880` | `00247510` post + `00575A50` | `00577886` `mov rbx,[rip+0x2731eab]` |
| `005779E0` | byte-table index `[rip-table + ecx]` then tail `00315B50` | `005779E3` `lea rcx,[rip+0x7abd66]` |
| `00577A00` | stores `rcx` into `[rip-global]+0xC0` — a register-the-screen setter | `00577A0C` `mov [rax+0xC0],rcx` |
| `00579990` | child create — `00244F50` + `0058DACF` | `00579999` `mov rax,[rip+0x19cae90]` |
| `00579A40` | child create — `00244F50` + `00808C40` | `00579A44` `mov rax,[rip+0x19cade5]` |
| `0057A2D0` | `00249210` leaf installer | `0057A2E8` `call 00249210` |

## The layout-key readers

*(2026-09-14, FRONTIER — LAYOUT-KEY-READERS.)*

| reader (→ owner) | keys | what the values do at the use site |
|---|---|---|
| `00572E10` P (~~content viewer~~ the Sky Pirate's Den; corrected 2026-09-29, FABLE, GI-2) | `PartyBlackBandTime` | `mov ecx` → duration arg for the viewer's party-band fade call on `[rdx+0xF8]` (`0057326A`) |
| `00574E80` P (back panel) | `PartyBlackBandTime` | `mov ecx` → duration arg for the back panel's party-band fade call on `[rdx+0xF8]` (`0057508E`) |

## What this screen does

`00574E80` puts up the `HandBack2_c.tm2` frame and owns three child slots; ~~`00572E10` runs inside it as the chapter viewer — it loads `menuhandbook_order.bin`, keeps a `0x1100`-byte record array of page entries (`+0xD0`), walks `+0xCB` entries under directional input, resets the menu effects on each page flip (id 16 → `003B29B0`), and picks the page's art through the `0xC036A4` table on teardown. `00572460` parses the per-page 8-byte placement entries and `00572600` holds the cursor. The screen is generic over chapters — the page kind arrives in `msg->arg` at construct and indexes the resource table.~~

**Corrected 2026-09-29 (FABLE, GI-2):** `00572E10` is the Sky Pirate's Den, installed for page kind 7 only. It loads `menuhandbook_order.bin` (the statue layout), keeps one `0x80`-byte group per awarded achievement at `+0xD0` (`00572920`), moves the selection `+0xCB` between statues by direction (`00572BD0`), swaps the statues' normal and highlighted effects on selection (`005734C0`), opens `00572600` as the statue's description popup, and on teardown stores the selected statue in the saved-cursor bank (`005732B8`). `00572460`'s role was not re-read.

## The two data files — `hcom` and `hodr`, decoded 2026-09-16 (SWE2-DATA)

Both handbook `.bin` files are ordinary `(kind 7, id)` resources requested through the shared
`0032E400`/`0032E620` path — there is no per-format loader:

| file | signature | kind | id | requester | size |
|---|---|---:|---:|---|---:|
| `…\<locale>\handbook\menuhandbook.bin` | `hcom` | 7 | `0xC8` | `003158B0` | 312–320 by locale |
| `…\<locale>\handbook\menuhandbook_order.bin` | `hodr` | 7 | `0xC9` | `00572D80` → `00249210` | 1068, all locales |

The bind mechanics (release-then-request for `hcom`, blob → `rbx+0x1200` for `hodr`) are in
[the loader-bound `.bin` families](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md) §4.

### `hodr` — the display-order permutation, 33 × 32-byte records

**Corrected 2026-09-29 (FABLE, GI-2): the field names in the block below are wrong from `+0x00` to `+0x17`.** `+0x00` is a key (selection priority and child anchor), `+0x01` a draw depth (not a page kind), `+0x02`/`+0x04` the statue position, `+0x06`/`+0x08` the pointer offset, `+0x0A`/`+0x0C` the description popup's position, and `+0x16`/`+0x17` the normal and highlighted menu-effect ids — not links, and not a perfect pairing (records 31 and 32 repeat one id). The last three records are not inactive: two child sprites and a backdrop. The decoded layout is in [§ The Sky Pirate's Den](#the-sky-pirates-den-and-the-two-data-files-decoded-2026-09-29-fable-gi-2).

```
+0x00  char[4]  "hodr"
+0x04  u32      101        per-format tag (himg=100, hcom=103; same dword slot)
+0x08  u32      33         record count — 12 + 33*32 = 1068 exactly
+0x0C  rec[33]  32 B each:
       +0x00   u8   display-order index — a permutation of 0..0x1D over the first 30
                    records; the last three carry 0xFF/0xFF/0xFE = inactive
       +0x01   u8   page kind — all 33 values 0x00..0x20 present exactly once; this is
                    the same kind space as the +0xC8 field and the table below
       +0x02   u16  primary id   (0x2F..0x1B8)
       +0x04   u16  secondary id (0x28..0x18B)
       +0x06   i16  dx — signed nav/layout delta (-30..+56)
       +0x08   i16  dy — signed nav/layout delta (-25..+20)
       +0x0A   u16  field a (0x48..0x6E)
       +0x0C   u16  field b (0x5C or 0x13A — two bands, top/bottom rows)
       +0x16   u8   link lo — } pair {2k+1, 2k+2}: a perfect pairing over the 66-entry
       +0x17   u8   link hi — } sub-entry index space, correlated with the permutation
```

~~The order column is what `+0xCB` bounds and the id-10 index math walk; the page-kind column is
what selects the record `00572460` later parses.~~ *(Corrected 2026-09-29, FABLE, GI-2 — `+0xCB` is the selected statue and `+0x01` a draw depth; see the note above the block.)*

### `hcom` — the shared node/constant block

**Corrected 2026-09-29 (FABLE, GI-2): the block below misreads the format.** There is no node web: `hcom` is five length-prefixed sections `{u16 byteLength, u16 count, …}` chained by `p += u16[p]` from `+8`, and the `0xFFFF` words are set bits of section 0's bitmap. The constants are section 4 at `+0xF8` (us), `{u16 len, u16 count, u32 idMask, u32 value[count]}`; the mask `0x800661FF` is in every locale, not a `de` insertion, and the 312/316/320 size deltas are one extra section-1 rule (all eight non-us locales) and one extra section-4 value (in/kr/cn/ch). The decoded sections are in [§ The Sky Pirate's Den](#the-sky-pirates-den-and-the-two-data-files-decoded-2026-09-29-fable-gi-2).

```
+0x00  char[4]  "hcom"
+0x04  u32      103        per-format tag
+0x08  …        u16 self-relative-offset web — every u16 is an offset to the next node,
                0xFFFF marks a dead end; the majority of the body is this web
+0x100 u32[14-16] constants — a shared run of round values (300, 200, 100, 50, 500,
                50000, 100000, 1000000, 50 … 8, 1000, 500000, 50, 16) with 0–2
                locale-specific entries inserted at the head or inside the block
                (`de` adds `0x800661FF`; `ch`/`cn`/`in`/`kr` add `0x800669FF` and
                `0xBB80` = 48000) — that insertion is the whole 312/316/320 size delta
```

The consumer shape is proven at `00315D50`: the record global `022C2550` (the `rax` stored by
`003158B0`) is walked as `p += u16[p]` chains starting at `+8` — ~~a linked-node traversal, not a
record array.~~ *(Corrected 2026-09-29, FABLE, GI-2: each hop skips one whole section; the hop count selects the section, three for `00315D50`.)*

### The `0xC036A4` lookup, decoded

**Corrected 2026-09-29 (FABLE, GI-2 / GI-4): the framing below is four bytes late.** The records are `{u16 label; u16 help; u8 key; u8 flag}` starting at `00D236A0`; `0xC036A4` is the `+4` key byte of record 0, so each row of the struck table pairs one page's key with the NEXT page's two text ids, and the "kind 7 terminator" `0x0000`/`0x8000` is the first dword of the next table (`00D236D0`). The key is a saved-cursor slot, not a resource id. The reader-framed table follows the struck one, and both halves are decoded on [the shared-dialog page](../Shared-Dialogs/the-shared-dialog-widgets.md#the-title-table-the-two-single-installer-widgets-and-the-0x630-word--read-2026-09-29-fable-gi-4).

~~The teardown arm indexes **`[r9 + pagekind*6 + 0xC036A4]`** — a 6-byte-record table at image
base + `0xC036A4` (VA `0xD236A4`), clamped to kinds < 8 for this call. The eight entries:~~

| page kind | resource id | +2 u16 | +4 u16 |
|---|---|---|---|
| ~~0~~ | ~~`0x0B`~~ | ~~`0x1B59`~~ | ~~`0x1F41`~~ |
| ~~1~~ | ~~`0x0C`~~ | ~~`0x1B5B`~~ | ~~`0x1F43`~~ |
| ~~2~~ | ~~`0x0D`~~ | ~~`0x1B5A`~~ | ~~`0x1F42`~~ |
| ~~3~~ | ~~`0x0E`~~ | ~~`0x1B5E`~~ | ~~`0x1F46`~~ |
| ~~4~~ | ~~`0x0F`~~ | ~~`0x1B5C`~~ | ~~`0x1F44`~~ |
| ~~5~~ | ~~`0x11`~~ | ~~`0x1B5F`~~ | ~~`0x1F47`~~ |
| ~~6~~ | ~~`0x10`~~ | ~~`0x1B5D`~~ | ~~`0x1F45`~~ |
| ~~7~~ | ~~`0x12`~~ | ~~`0x0000`~~ | ~~`0x8000`~~ |

**Corrected 2026-09-29 (FABLE, GI-2; agrees with the GI-6 reader): the struck rows pair each page's key with the next page's two texts.** Read from the record starts, `00D236A0 + 6 × kind` (`0056F32B` and `00574AAD` read the title word there):

| page kind | title / help (`penelosdiary.bin` / `help_penelosdiary.bin`) | `+4` key = saved-cursor slot |
|---:|---|---:|
| 0–3 | `0x1B58`/`0x1B59`/`0x1B5B`/`0x1B5A` — one shared placeholder row (empty in us, "NOT USED" in fr) | `0x0B`–`0x0E` |
| 4 | `0x1B5E` Traveler's Tips / `0x1F46` "Hints for the wary adventurer." | `0x0F` |
| 5 | `0x1B5C` Bestiary / `0x1F44` "Insights on foes you have defeated." | `0x11` |
| 6 | `0x1B5F` Hunts / `0x1F47` "Hunt information and progress." | `0x10` |
| 7 | `0x1B5D` Sky Pirate's Den / `0x1F45` "What will it take to fill the den?" | `0x12` |

~~So page kinds 0–6 map to kind-7 resource ids `0x0B`–`0x12` (the handbook page art), each carrying
a pair of `u16` fields (`0x1B5*`/`0x1F4*` — consecutive pairs, likely a resource window or
coordinate pair). Kind 7's entry is a `0x8000`-flagged terminator.~~ *(Corrected 2026-09-29, FABLE, GI-2: see the note above the table.)*

## The unlock layer — `hctg`/`hchk`/`hdat`, decoded 2026-09-18 (SWE2-DATA)

The six family `.bin` files are `hctg` catalogs, the unnumbered `menuhandbook_<fam>.dat` files are
`hchk` unlock-predicate tables, and the low-numbered `NNN.dat` files are `hdat` record headers —
full layouts, consumers, and the resource-id enumeration are in
[the sibling-format page](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/hchk-hctg-hdat-handbook-indexes.md).
The screen-side facts:

- The menu singleton at `02CA9738` holds the six family `hchk` buffers at `+0xC8`–`+0xF0`,
  the `menuquest.dat` handle at `+0xF8`, and bound resource objects at `+0x108`/`+0x110`/`+0x118`.
  `00576F50` performs the bind (six family loads via the `00D23740` base table + id `0x128`).
- `00577550(root, kind)` is the unlock **sync pass**, invoked from the panel's message arms
  (`0056F79B`, `0056FB5C`, `00571FC1`, `005750AF`): it evaluates each `hchk` record's predicate
  (`00575E80` — a four-slot conjunctive gate over the save block's `+0x336C` nibble array,
  `+0x334C` bit array, `+0x14F4` bit array, and `global_flag[0]` story progress) and persists
  the result into the save's `+0x32CC` bit array via `00315910`. Monster records (`u16[8]`,
  evaluated per-slot by `00576E30`/`00576860` against the `+0x3404` counter bank = kill counts)
  persist to the `+0x3604` per-record flag bytes via `00315AD0` bank 6.
- `00576920(tab)` reads those persisted flags back through `003154B0`/`00315670` to drive the
  per-tab entry counts and the newly-unlocked badge index.
- `00575D10` issues a page request from an `hctg` 12-byte record (`{u32 textId; u32 group;
  u32 index}` at `hctg + word[hctg+0x0A] + i*12`), `00576030` copies the hctg header fields into
  the request descriptor, and `00577970` dispatches pages through the record's index field.
- `00576A50` resolves **conditional captions** out of the `hctg` `+0x18` aux table
  (`u32 textId[word+0x12]` + a `{count; relOff[]}` blob index, shipped only by monster):
  a gate blob's `condId`s are probed via `00309EC0` and its `navimapId`s against the
  current/visited map — any pass resolves the real caption (`002F9920`), all fail resolves
  placeholder text id `0x3EC` (`002F9860`).
- `005760A0(out, recIdx)` is the **detail-panel resolver**: name via `002F9920(textId)` (monster:
  `bank:index` decode `002B58B0(003214B0(textId), 0)`), a subtitle line for the 13 Esper
  records (`textId 0x4210..0x421C` → `00D23790` 13-dword table → `0035D330(entry+0x106)` →
  `+0x18` name), the record's group word and `+0x0A` flag byte, the live kill counter
  (`00315420`, save `+0x3404`), and — through the monster `hctg` tail (`hctg + recTableOff +
  recordCount·12`, `{count; relOff[]}` → 8-byte aux record whose byte 0 = the slot count) — the
  materialized `hchk` `v[slot]` operands via `00576860`. `00576030` copies the family fields
  (`obj+0xD2` family ordinal, `hctg +0x08>>4`, `+0x12`, `+0x0E`, `+0x10`) into the same
  descriptor.

## The Sky Pirate's Den and the two data files, decoded 2026-09-29 (FABLE, GI-2)

*Static and authored-data census. Every claim below is a check in [`gi2_hcom_hodr.py`](../../_index/candidates/gi-0929-dialogs/gi2_hcom_hodr.py) (FAILS 0; output in [`gi2_hcom_hodr.out`](../../_index/candidates/gi-0929-dialogs/gi2_hcom_hodr.out)), which also carries the regressions that reject the struck readings above.*

**`00572E10` is the Sky Pirate's Den.** `0056EE10` installs it only for page kind 7 (`0056EE3F` `cmp al, 7`, then `0056EE7A`, its only rip reference), and `menuhandbook_order.bin` (`hodr`) is the Den's statue table.

**`hodr` — 33 records of 32 bytes.**

| offset | field | read by | meaning |
|---|---|---|---|
| `+0x00` | u8 key | `00572920`, `00573690` | records 0–29: a permutation of 0–29, and the lowest key among the awarded statues is selected first (`00573690`). `0xFF` = child sprite, anchored to the group whose key equals `003165C0(recordIndex)` (through the `003165B0` thunk, `005729BE`); `0xFE` = always drawn |
| `+0x01` | u8 depth | every draw | `(0xFF − v) × 10000` to `003B2F50` (`00572A8B`/`00572A8F`); all 33 values 0–32 distinct |
| `+0x02`/`+0x04` | i16 x, y | every draw, `00572BD0` | statue position; the only navigation input — `00572BD0` picks the nearest other awarded statue in the pressed direction |
| `+0x06`/`+0x08` | i16 dx, dy | `005733F0` | the hand pointer sits at (x+dx, y+dy) (`0057346B`/`00573479`) and faces 2 when dx > 0, else 0 |
| `+0x0A`/`+0x0C` | u16 x, y | `00572600` | the description popup's position (`005727BF`/`005727BB`); y is 92 or 314, above or below |
| `+0x16` | u8 | `00572920`, `005734C0`, `00573690` | the statue's **normal** menu-effect id (`r9d` of `003B2D80`) |
| `+0x17` | u8 | `005734C0`, `00573690` | the statue's **highlighted** effect id; `005734C0` redraws the old selection and its children with `+0x16` and the new one with `+0x17` (`0057351C`, `005735F5`) |

The group for achievement `i` exists only when `00576E10(i)` holds — `003154B0` category 7, the award bit at save `+0x3844` (`003155F4`, `00315612`) — so a statue appears once its achievement is earned. The thirty statues (title `0x1B68 + i`, description `0x5DDE + i`, e.g. 0 "Balthier": *"Awarded for Attacking over 300 times, earning you the title of Assault Striker."*): Balthier, Fran, Vayne, Vaan, Basch, Chocobo, Penelo, Gurdy, Ashe, Crystal, Vossler, Rasler, Belias, Gabranth, Migelo, Old Dalan, Ba'Gamnan, Reks, Montblanc, Mimic?, Trickster, Gilgamesh, Behemoth King, Fafnir, Carrot, Deathgaze, Yiazmat, Hell Wyrm, Ultima, Zodiark. Record 30 anchors to key 0 (`003165C0(30)` = 0, no mask bit) and sits exactly on Balthier's position — an overlay drawn and highlighted with it; record 31 anchors to key 16 (`003165C0(31)` = 16, the id-31 value of `hcom` section 4) and sits beside Ba'Gamnan; record 32 (`0xFE`, depth 0) is drawn at (80, 40) always — the backdrop. Records 0–30 use effect ids `2k+1`/`2k+2`; 31 and 32 reuse one id each (`0x3F`, `0x40`). Nothing traverses `+0x16`/`+0x17`: all eleven byte reads of them in `0x570000`–`0x578000` are the effect-id argument of the next `003B2D80` call.

**`hcom` — five length-prefixed sections**, each `{u16 byteLength, u16 count, …}`, reached by hopping `p += u16[p]` from `+8`; the chain ends exactly at the file size in all nine locales.

| hops | us offset | content | readers |
|---:|---|---|---|
| 0 | `+0x08` | 369-bit bitmap over the navigation-map ids (359 set) | `003160C0` — achievement mode 5: every flagged map visited |
| 1 | `+0x3C` | bestiary rules: `u16 384` (entries), `u16 0`, `u16 nRec`, then `{u16 type<<12 or id, u16 value}`; type 0 = counts once story progress (`FieldData_GetVariable0`) ≥ value, type 1 = counts once monster *value* is defeated; unlisted ids need their own defeat count | `003161A0` (mode 6, all 384), `003154B0` category 6 (one entry) |
| 2 | `+0x7C` | 45 `{u8 quest, u8 threshold}` pairs, quests `0x80`–`0xAC` | `00316480` (clan rank, via `00315390`): quest ordered or cleared and its progress byte ≥ threshold; `00315DC0` per quest |
| 3 | `+0xDC` | 11 monster ids: Trickster, Gilgamesh, Behemoth King, Fafnir, Carrot, Deathgaze, Yiazmat, Hell Wyrm, Ultima, Zodiark, Shadowseer | `00315D50` (own counters in `01EED130`; `00315820` skips them), achievement mode 7 |
| 4 | `+0xF8` | `u32 idMask` + one `u32` per set bit — the achievement threshold overrides | `003165C0` (achievement catalogue, UQ-274) **and** the Den's child anchors above |

The 14 us bestiary rules: Battery Mimic and Tiny Battery (story ≥ 341), Miriam Guardian and Miriam Facer (≥ 2200), Ba'Gamnan (≥ 660), Ahriman (≥ 3200), Imperial (≥ 253), Judge Ghis (≥ 1015), Imperial Elite (≥ 966), Judge Bergan (≥ 2350), Imperial Armament (≥ 3500), Judge Gabranth (≥ 5500), Doctor Cid (≥ 3500), and Enkidu (counts once Gilgamesh is defeated). All eight non-us locales add Rogue Tomato (story ≥ 78); in/kr/cn/ch also set mask bit 11 with 48000 (`ACH_MASTER_LICENSE`'s override). Section 3's first ten ids are, in order, the statues of achievements 20–29. *(Quest ids `0x80`–`0xAC` read as the 45 hunts from the count, the id block and the order/clear bitsets `+0x1000`/`+0x1020`; no quest name was resolved.)*

**The two `u16`s of each `0xC036A4` record** are the page's label and help text ids — `{u16 label; u16 help; u8 key; u8 flag}` from `00D236A0`; kinds 4–7 are Traveler's Tips, Bestiary, Hunts, Sky Pirate's Den, kinds 0–3 placeholder rows ("NOT USED" in fr). The label is the page title (`0056F32B`, `00574AAD`); the help word of this half has no reader; the key is the page's saved-cursor slot. Full table and readers on [the shared-dialog page](../Shared-Dialogs/the-shared-dialog-widgets.md#the-title-table-the-two-single-installer-widgets-and-the-0x630-word--read-2026-09-29-fable-gi-4).

## Not yet established

- ~~the `menuhandbook_order.bin` record format beyond the `00572460` placement walk~~ —
  **resolved above**: 33 × 32 B permutation records, 2026-09-16
- ~~which `0xC8` page kinds map to which resource ids in `0xC036A4`~~ — ~~**resolved above** for
  kinds 0–7 (`0x0B`–`0x12`), 2026-09-16; the table continues but the caller clamps to < 8~~ **Corrected 2026-09-29 (FABLE, GI-2):** `0x0B`–`0x12` are saved-cursor slots, not resource ids, and the table ends at `00D236D0`; see [§ The Sky Pirate's Den](#the-sky-pirates-den-and-the-two-data-files-decoded-2026-09-29-fable-gi-2)
- ~~the `0056EF60` pane's own role (frame vs. list chrome)~~ — **read 2026-09-18 (FABLE): it is the content-pane host, neither frame nor list.** Its four arms: **id 1** (`0056F20D`) takes layout `0x1B` through `003946B0`, keeps the parent at `+0xC0` and the creation argument at `+0xF0`, zeroes `+0xCC`–`+0xF8`, takes resource `0x64` and registers with the parent (`00244960`); **id 12** sub-commands — 6 creates the page-list child with procedure `00570530` into `+0xE8` (`0056F0DB`–`0056F13E`), 7 destroys it (`00244F00`), `0xE` sets bit `0x20` on the global handbook state `[02CA9718]+0xC0` when the parent says `0x12`, `0xF` destroys the global's `+0x100` child, `0x12` and `0x14` forward their argument to `0056ECC0` / `0056EC10`, and `0x8001` records the **selection** — word into `+0xCA`, `+0xCC` bit 0 — and for kinds 2 and `≥ 5` runs `005749B0` then `00291D80(0, 0)` (`0056F1B8`–`0056F1E6`); **id 16** reconciles (kind 5 keeps a pending flag in `+0xCC` bits 3 / 2, then `0056EE10` installs the kind's pages and clears the global's bit `0x40`); **id 18** destroys (`0024A680` on `+0xF8`, posts `{0x12, 6}` to the parent). So the mid pane hosts whichever content page the kind byte `+0xC8` names and carries the selection up — the same reading [the unlabelled procedures](../Unlabelled-Panes/the-unlabelled-procedures.md) reached from the installer side.
- ~~the `hcom` u16 offset-web's node semantics (which nodes are topics vs. links), and the two
  `u16` fields in each `0xC036A4` record~~ — **answered 2026-09-29 (FABLE, GI-2):** no web — five sections; the two `u16`s are label and help text ids ([§ The Sky Pirate's Den](#the-sky-pirates-den-and-the-two-data-files-decoded-2026-09-29-fable-gi-2))
- ~~the `hodr` `+0x16`/`+0x17` link pair's exact traversal semantics (a pairing, not yet walked)~~ — **answered 2026-09-29 (FABLE, GI-2):** not links — a statue's normal and highlighted effect ids ([§ The Sky Pirate's Den](#the-sky-pirates-den-and-the-two-data-files-decoded-2026-09-29-fable-gi-2))

## Falsification pass

**Pass 1 — 2026-09-14 (OPUS).** Attacked at parent `GN160` (`fa0db293…`), EXE `73461d08…`, decoding
with capstone. Instrument: `Tools/work/OPUS/falsify_handbook.py`. **Sixteen claims attacked, sixteen
survived. No correction.**

| claim | the killer | result |
|---|---|---|
| `00574E80` bounds to `0x11` at `00574EA5`, table `0057552C` | a different bound, compare address or table | **survived** — all three exact |
| its ids are 1,2,12,14,16,18 at the published arms | any other id reaching a real arm, or an arm elsewhere | **survived** — `00574EC4`/`00575144`/`0057517D`/`005750C2`/`00574FC7`/`00575498` |
| ids 3–11,13,15,17 fall to `00575505` | a different default | **survived** |
| `00572E10` bounds to `0x12` at `00572E35`, table `005733A0` | same | **survived** — all three exact |
| its ids are 1,2,10,12,14,15,16,18,19 at the published arms | same | **survived** — **nine arms, nine exact** |
| `0056EA40` answers 1,3,18,19 | any other id reaching a real arm | **survived** |
| `00570890` answers 1,18 | same | **survived** |
| `0056F550` answers 1,18 | same | **survived** |
| `00572600` answers 1,10,14,15,18 | same | **survived** |
| seven installer claims (`00574CB0`, `00575580`, `0056EE10`, `00574D00`, `0056F3C0`, `00574E00`, and `00572E10` → `00572460`) | the procedure absent from the installer's RIP-relative `lea`s | **survived** — all seven |

**`00572E10`'s nine-arm table is the strongest single result here**: nine ids, nine published
addresses, and the table produces every one of them with no tenth id reaching a real arm.

**One gap filled rather than falsified.** The tree said `0056F410` had *"no msg ids listed"* — a
statement about the page, not the body, so nothing could falsify it. Measured: **it answers id 1**,
at `0056F428`, and its arm is a construct (`003946B0` with `r8d=0x17`, `0056F470`, `00394700` with
`edx=2`, then `+0x44 = 0x64` through `00247930`). The row now says so.

> **That leaf is worth comparing with `0057E610` in
> [the save/load widgets](../../19-Save-Load-Settings/the-save-load-screen-widgets.md).** The two
> bodies have the same shape — `cmp dword ptr [rdx], 1`, a construct arm, `00247930` setting `+0x44`
> — and that page asserted its leaf *"answers no message ids"*, which pass 1 there falsified. **The
> difference between a page that was wrong and a page that was merely silent is only visible by
> reading the body**, and my own id-set reader missed both until it learned to see a compare against
> `[rdx]` that never loads it into a register.

**Not attacked by this pass:** the arm interiors below entry level — the sub-command semantics of
`0057517D` and `005731A7`, the `0xC036A4` page-kind→resource lookup beyond its presence, and the
`+0xCB` index math.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **World — CLIENT.** A cited function is called by a 122-byte World-labelled body.
- **WorldAreaField — CLIENT and SERVICE.** Cited functions are called by `WorldTransition_StageFieldTransition`, `WorldTransition_RequestFieldTransition` and two field bodies (203 and 229 bytes). They call `FieldData_GetVariable0` (2), `WorldTransition_GetActiveOrPendingFieldId` and a 529-byte field body.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — CLIENT.** `FUN_002fc3c0`, owned by that layer, calls `0024F410` on this page. That caller is a 183-byte dispatcher: `byte[rec+0x23] & 0xF`, bounded to 7, into an eight-entry jump table; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Script_VM_Native_Bridge — CLIENT.** `FUN_0033fd40`, owned by that layer, calls `002EFD20` on this page. That caller is a 29-byte guard that returns its argument only when the mode query answers exactly **1**, and zero otherwise; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**StoryEvent — CLIENT.** `FUN_001ed240`, owned by that layer, calls `00265270` on this page. That caller is a 2,192-byte cutscene-override table: it matches the current area id against hard-coded values such as `0xD70` and `0xD48`, the story-progress word selected by `[01DFE40C]` out of `01F832B0` against a step number, the model's name against string literals such as `g0999` and `c1004`, and the animation time against a window, returning a small override index when all four agree; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, GI follow-up): the layer the GI answers newly brought into this page's audit.*

**PlatformOnlineAchievements — SERVICE and DEPENDENCY (48 edges).** The handbook's own readers call the achievement-counter family: `00576E10`, `00576920` and `00576CA0` go through the category tester `003154B0` (category 7 is the award bitmap at `+0x3844`); the detail-panel resolver `005760A0` and the per-slot evaluator `00576E30` read the bestiary byte `00315420` (the `+0x3404` kill-count bank); the Clan Primer leaf `0056F470` calls the clan-rank body `00315390` and the counter read `003166F0`; and `00577550` calls the re-check sweep `00316930`. The other edges run inside that family, between bodies this page cites for the tables they read: the evaluator `00315E90` calls `00315420`, `003160C0`, `003161A0`, `003165C0`, `003166F0`, `00316760`, the award thunk `008632B0` and `BattleEncodedId_DispatchQueryMode0Value` (`00309EC0`), and is called by the sweep `00316930` and by `AchievementCounter_UpdateAndMaybeFire` (`00316A50`); `003154B0` and `003161A0` call `00315420` and read story progress through `FieldData_GetVariable0` (`00265270`); `00315390` calls `00316480` and `00316670`, and `00316670` calls `00316930`; `00316930` calls `003162E0` and is the caller of `00315DC0`; `003162E0` calls `003165C0`, `00863280` and `008632B0`; `003165C0` and `003166F0` are also called by `00316A50`, and `003166F0` by `00316760`; and `00315820` calls `00315D50`. The Sky Pirate's Den statues, the Clan Primer rank and the bestiary pages display state the achievement family owns and evaluates, so this page depends on that family's award bits, counters and thresholds and writes none of them.

## Evidence-only read — frontier hub `00394700` (2026-09-18, SWE2-EC7)

`00394700` — 28 B, 7 A-measured callers; the 4-way dispatch both citing screens run. Read
against the shipping image (page stays PARTIAL — evidence-only): `edx >= 4` returns
immediately; otherwise `edx*40` indexes the four-entry `00D112E0` record table
([`0039470B`](../../_index/ADDRESS-INDEX.md) computes `table + edx*5*8`) and `jmp 00247570` tail-calls the record
op on it — the `00247510`-family handler dispatch, table-driven.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22, FRONTIER's debt (SWE2-FRONTIER, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, `SWE2-FRONTIER-PASS22-DEBT-OWN`, batch 8). These are the six layers pass 22 still reported for this page at HEAD `acb04148d`. Every edge was listed in full, and each helper named here was read at its instructions. The page cites these helpers as families; the readings below say what each helper is. Far ends are named from the call graph.*

**Presentation — SERVICE and CLIENT (106 edges).** Most of the count is shared helpers the render layer also calls. `00202C90` is a 16-byte copy (`movups [rcx], [rdx]`) with 24 render callers (`00274CB0` to `00562A30`). `0024A5A0` looks a name up in the 64-entry resource-name registry (six callers, `00291320` to `00506700`). `0024F610` looks an entry up in the bucket table at `020910A0` by `byte [rcx]` and `word [rcx+4]`. `0024B270` and `0024B3A0` allocate and insert into that table and publish the entry, and render code calls them (`0026F470`, `003B02A0`, `003B2D80`, `003B3550`; `003B2220`, `003B38B0`). `0024B270` in turn calls three `003A7xxx`/`003A8xxx` effect-record bodies. `0036DD90` and `0036DDA0` set bits `0x80` and `0x40` of one global flag word, and `0040ACF0` / `0040D890` call both. `003B1310` walks the `0x30`-stride registry `02EBE5E0`..`02EBEBE0` and tests resource tickets through `0032E4D0` / `0032E520` / `0032E590`. The chunk walker `003EDAD0` and its registrars are the same code the nonempty-PRF page reads. The handbook's own effect panes `005734C0`, `00573690` and `00572920` call the menu-effect bodies `003B2AA0` / `003B2D80` / `003B2F50`; `00572E10` calls `003B29B0` and reaches those three only through `005734C0` and `00572920` (narrowed 2026-10-01, AUDIT-SEM review N1). The rest are single edges through the widget helpers (`00247510`, `00247870`, `002527B0`), the slot and handler helpers (`00249410`, `00249580`), the string fetch `002F9920`, the encoded-id wrapper `0035D330` and `001816F0`. Presentation owns the effects and records; the handbook draws through them.

**Resource — SERVICE and CLIENT (62 edges).** The load path the page names (`0032E400`/`0032E620`: no per-format loader) is the resource layer's. `0032E400(kind, id)` returns the dword at `[022C51F0][kind][id]` for `id < 0x400`; kind `0xFF` returns −1 at once (`0032E40A`), and only a missing table or `id >= 0x400` takes the fallback call `0046DE70` (corrected 2026-10-01, AUDIT-SEM review C2). `0032E620` is the queue requester. Both are called by nine loaders (`00249210`, `0024AC30`, `00259DF0`, `00379E90`, `00384420`, `0039C3F0`, `0051ED10` and peers). `00249210` is the slot-table loader that five Resource bodies (`00249180` to `002493D0`) call, and it calls both back. `0024A4E0` is the text-label create. The handbook panes `0056F2A0`, `00572D80`, `00574E80`, `00575C30` and `00576F50` call `00249210`, `00249580`, `0024A680` and the kind-7 request fan-out `003933F0` / `00393460` / `003934F0`. `0024A680` walks the list at `0208F580` for its object. `003B1310` tests tickets through `0032E4D0` / `0032E520` / `0032E590`. `FieldData_GetVariable0` (`00265270`) is called by `001DA220` and `001DA970`. The handbook requests its resources through the shared loader and queue and owns neither.

**Save_Load_Settings — CLIENT and SERVICE (24 edges).** The save controllers call the same widget helpers these panes use: `00247510`, the message post of kind `0xC` to `[obj+0]`'s handler (six callers); `00247870`, the show/hide bit 1 of `+0x40` (five); `00244960`, which attaches a child whose parent link is empty (four); and `00245020`. `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`) reads `00315390` and `003166F0`, two readers of the game-state block (its `+0x3868` and `+0x384C` cells), and `0032A8A0`, which reads the save image's persistent payload through `002EF2B0`. The save header reads those values, and the save layer owns none of this page's state.

**Input — CLIENT and SERVICE (12 edges).** The UI transform evaluator `00368360` reads three Input bodies (`001E0A10`, `001E0E30`, `001E0E50`), and those call `InputManager_GetSingleton` (`00198790`), `001986D0` and `00197700`. `InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`) calls `FieldData_GetVariable0` (`00265270`) and `0032A8A0`. `00291D90` calls `0024A680` and `00291C80` calls the requester `0032E620`. These are shared input reads and helpers; no handbook state drives input.

**SaveLoad — CLIENT (7 edges).** `00582790` claims a request batch record (`00249580`), loads (`00249210`), closes the batch with `00249410` and requests kind-7 resources (`003933F0`, `00393460`). `00280140` calls `00245020` and `002EFD20`, which clamps its index to 0..6 and returns the byte at `022BDD64 + idx × 0x30` (corrected 2026-10-01, AUDIT-SEM review C1, N2). It shares the helpers and nothing else.

**CombatAI — CLIENT (1 edge).** `AiOrder_EvaluateTargetSelector` (`00301AD0`) calls `BattleEncodedId_DispatchQueryMode0Value` (`00309EC0`), an encoded-id query this page also cites. It is the same query, with no handbook role.

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-handbook-screen-cloudint-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001B1F80` | 31 B | stores the fifth (stack) argument at dword `+0x3a58` and `edx`, `r8d` and `r9d` at dwords `+0x3a4c`, `+0x3a50` and `+0x3a54` of `rcx` | `001B1F84`, `001B1F8A`, `001B1F90`, `001B1F97` |
| `003A7E80` | 90 B | with `p` = `rcx`+4, stores byte `[rcx+2]` at byte `p+0xc2` and byte `[rcx]` as word `p+0xc0`, stores `p` in the qword slot byte `[rcx]` of the array at qword `[qword 02EBEFA0]`, calls `004FF270(p, dword 02EBB738 + the low dword of p)` and returns `p` + `edx` (sign-extended) | `003A7E9F`, `003A7EA5`, `003A7EB7`, `003A7EC3`, `003A7ECC` |
