---
id: ui-gambit-screens
title: The gambit screens — the list, the editor, the icon, and the bank-commit protocol
status: "DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS; documented_rule READY): GI-18 answered 2026-10-01 (OPUS, static - every arm of both procedures read one level down, see the GI-18 section; review requested from SWE2-AUDIT-SEM). GI-1 answered 2026-09-29 (FABLE), review (FABLE-REQ-AUDITSEM-REVIEW-GI-UI, ACCEPT, d998217e2). History: PARTIAL on GI-18 from 2026-10-01 (SWE2-FRONTIER, on SWE2-AUDIT-SEM's REJECT of c97af7156, record dd-restatus-gi-0930); earlier PARTIAL on: which value of the gambit row's +0x14 bit 0 selects condition art and which action art (GI-1); the earlier 02F8F570 was a misread of 0208F570, the tick counter (corrected 2026-09-18)"
evidence_tier: 1
tags: [ui, gambits, menu-screens]
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `005680E0`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-14
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: opus-gambit-screens-pass-1 - nine claims attacked by decoding the image at GN160; eight survive, including both jump tables reproducing every documented arm from the image base, the r15 lea resolving to 0x120000 exactly, the 0x121 peel, the slot-0 vtable post and both installers; ONE FALSIFIED and corrected in place - the id bound is at 0056B4F8, not the published 0056B4F5, which is `mov rsi, rcx`
  crossref_clean: false
  reopened_count: 0
addresses:
  - "0056B4D0"
  - "005691E0"
  - "00566C10"
  - "0056C170"
  - "003282C0"
  - "003282D0"
---

# The gambit screens

~~**Status:** PARTIAL~~ *(Superseded 2026-10-01, OPUS: DOCUMENTED - see the status line; GI-18 answered)* — the four widget procedures, the parent→child `0x121` destroy notification, the bank-commit-on-close arm, and every screen-region helper are cited below. The editor's 12 sub-commands, the list's 19 arms and the list's `0x8000`/`0x8001`/`0x8002`/`0x8005` sub-command arms are decoded; every listed screen-region member carries a role and an interior citation (2026-09-15). The ~123 shared subtree members are cited as engine-helper families, not re-read.

## The tree

The gambit UI is two related screens, not one: ~~the **gambit list** (the per-member twelve-slot display with the "gambits + message window" atlas label) is the parent, and the **gambit editor** (the condition/action picker) is its `+0xC8` child.~~ **Corrected 2026-09-29 (FABLE, GI-1):** the direction is the other way. The editor `005691E0` creates `0056B4D0`: its id-12 `0x8001` arm calls `00567D80` (`00569E63`), which calls the installer `0056B350` (`00567E43`, `00567E73`) with mode 1 or 2 according to the editor's column byte `+0x33E` (`00567E0E`–`00567E73`); `0056B350` stores the new widget in the editor's `+0xE8` (`0056B3CA`), and the list's `+0xC8` is the create record's `+0` — the editor itself (`0056B38A`, copied at `0056B69E`–`0056B6A1`). So `0056B4D0` is the condition/action **pick list** the editor opens (mode 1 target conditions, mode 2 actions — §*GI-1 answered 2026-09-29* below), and the `0x121` post described next goes from the pick list to its creator, not to a child. The list's **id-18 destroy arm** posts message `0x121` through the child's vtable — `0056B4D0` arm `0056B516` checks `+0x58E`, reads `[self + 0xC8]`, and posts `{0x121, 0, 0}` at `0056B51F`–`0056B549`; the editor `005691E0` peels `0x121` ahead of its dispatch table with `cmp eax,0x121` / `je 00569EE3` at `00569204`–`0056920F` (the arm sets `+0x331 = 6` when that byte is nonzero — the "parent is going away" latch).

| procedure | role | atlas label |
|---|---|---|
| `0056B4D0` | ~~gambit list screen (parent)~~ condition/action pick list, created by the editor (corrected 2026-09-29, FABLE, GI-1) | gambits + message window |
| `005691E0` | gambit editor screen ~~(child)~~ — the pick list's creator (corrected 2026-09-29, FABLE, GI-1) | gambits |
| `00566C10` | ~~GambitIcon draw widget~~ tab-strip marker: page arrows and a sliding pointer, named after the `GambitIcon…` keys it reads (corrected 2026-09-29, FABLE, GI-1) | gambits |
| `0056C170` | ~~leaf slot widget~~ the pick list's tab-strip container (corrected 2026-09-29, FABLE, GI-1) | gambits + message window (child) |

`0056B350` is the list's installer (it `lea`s `0056B4D0` and performs the standard lazy-create, calling `00244F50`/`002468A0`/`00246AD0`/`002470D0`); `0056ADA0` is the leaf `0056C170`'s installer (it `lea`s `0056C170` inside the list subtree).

## `0056B4D0` — the gambit list

`0056B4D0` dispatches on `msg->id` (`0056B4EE` loads `[rdx]`, `0056B4F3` decrements it, and `0056B4F8` bounds it to `0x12`) through the jump table at `0056BB80`:

> **CORRECTED 2026-09-14 (OPUS, falsification pass 1): the bound is at `0056B4F8`, not `0056B4F5`.** ~~`0056B4F5` bounds it to `0x12`~~ — `0056B4F5` is `mov rsi, rcx`. The compare is `0056B4F8 cmp eax, 0x12`, three bytes later, and `0056B4FB ja 0056BB53` takes the out-of-range path to the default arm this page already documents. The decrement that makes the table index `id−1` is `0056B4F3 dec eax`, which the sentence omitted. **The bound itself, its value and the table address are all as published**; only the cited address was wrong.

| id | arm | role |
|---|---|---|
| 1 | `0056B57F` | construct: ~~clears the editor's `+0xC8` byte, builds a two-entry child table (`0056B4D0` `lea`s `0056BB60`/`0056BB70` records), copies `msg->arg` into `+0x5A4`, then installs the editor child~~ clears `[02CA96D8]+0xC8`, builds the layout descriptors `00D234A8` / `00D234D0` (callbacks `0056BBD0` / `0056A780`), copies `msg->arg` into `+0x5A4` and the create record into `+0xC8` *(corrected 2026-10-01, OPUS: GI-18 section)* |
| 2 | `0056B9D4` | reconcile: calls `0056BE40` (layout refresh), ~~decrements `+0x580`; on the last pending request posts~~ counts the frame countdown `+0x580` (`0xB4` from `0056AC50`) down and at zero posts `{0x8000,0,0}` to self via `00247510` *(corrected 2026-10-01, OPUS: GI-18 section)* |
| 8 | `0056B7E9` | ~~enable on~~ focus gained: `or +0x5A0,2` and ~~sends id 1 to `+0xC0`~~ `002D45C0([+0xC0], 1)` *(corrected 2026-10-01, OPUS: GI-18 section)* |
| 9 | `0056B808` | ~~enable off~~ focus lost *(corrected 2026-10-01, OPUS: GI-18 section)*: `and +0x5A0,~2`, zeroes `+0x580` |
| 10 | `0056B81E` | directional input: reads the three pad-mask globals, tests `+0xE0 & 0x200000` (list mode), ~~routes confirm/cancel through `002D3A50`/`002D45C0` on `+0xC0`~~ pages up / down (`0056AAC0` / `0056AD50`) or hands the input to the list child (`002D3A50`) *(corrected 2026-10-01, OPUS: GI-18 section)* |
| 12 | `0056BA10` | sub-command: computes the slot index `(+0xF2 + +0xF4) * +0xEC + +0xEE + +0xED` (row×cols + col) and dispatches sub-ids `0x8000`–`0x8002` plus `0x8005` (`0x8003`/`0x8004` fall to the `0056BB4F` default) |
| 15 | `0056B80F` | about-to-destroy: shared with the enable-off tail, zeroes `+0x580` |
| 18 | `0056B516` | destroy: if `+0x58E` is set, builds `{0x121,0,0}` and calls the `+0xC8` ~~editor child's~~ editor's — its creator's — first vtable slot (`0056B516`–`0056B549`) — the ~~parent→child~~ child→creator destroy notification *(corrected 2026-10-02, OPUS: the editor's `00567D80` builds this list through `0056B350`, which stores it at the editor's `+0xE8`, `0056B350+0x7A`)* |
| 19 | `0056B7AE` | transition-in flag: if `+0x58E` set, writes `0x302`/`0x18` into `+0x58C`/`+0x58F`; if `+0x5A0 & 4`, sets bit 1 on the child's `+0x358` |
| 3,4,5,6,7,11,13,14,16,17 | `0056BB53` | default → `005C5230` tail |

The id-12 slot-math (`0056BA10`) is the same row/column indexing the quest list uses — `+0xEC` is the per-row column count, `+0xEE`/`+0xED` the cursor column/row, `+0xF2`/`+0xF4` the scroll offset. The list is the twelve-slot grid.

## `005691E0` — the gambit editor

`005691E0` dispatches `msg->id` (`005691E5` loads `[rdx]`): `0x121` is peeled first by `cmp eax,0x121` / `je 00569EE3` at `00569204`–`0056920F` (`>0x121` and out-of-range go to the `00569EF7` default), then ids `1`–`0x1A` go through the rel32 jump table at **`00569F1C`** (base `r15 = 0x120000` set by `lea r15,[rip-0x449229]` at `00569222`, index `id−1`, target `r15 + rel32`):

| id | arm | role |
|---|---|---|
| 1 | `005692A2` | construct |
| 2 | `005696A5` | reconcile |
| 5 | `00569718` | draw pass |
| 8 | `0056961E` | ~~enable on~~ focus gained *(corrected 2026-10-01, OPUS: GI-18 section)* |
| 9 | `00569671` | ~~enable off~~ focus lost *(corrected 2026-10-01, OPUS: GI-18 section)* |
| 10 | `0056981E` | directional input: if `+0x360` (modal picker) is clear, indexes the child table `[rip+0x273FEA7]` by `+0x35C`, tests `+0x340 & 1`, reads pad masks `0x800`/`0x400`/`0x200`/`0x100`, and drives `+0xD8` through `002D45C0`; `00282DF0`+`002C1A80` map pad→cursor |
| 12 | `00569DC1` | bank sub-command dispatcher (below) |
| 16 | `0056955F` | ~~refresh~~ resource batch complete: snapshots the set into `+0x128` *(corrected 2026-10-01, OPUS: GI-18 section)* |
| 17 | `00569781` | ~~secondary input~~ position tween finished: commits a pending edit *(corrected 2026-10-01, OPUS: GI-18 section)* |
| 18 | `00569236` | close: `002922F0`, checks `[global + 0xDEB]`, ~~commits the edited bank~~ only when it is set writes the id-16 snapshot `+0x128` through `003282C0` (`GambitConfig_CommitBankAndRebuildRuntimeOrders`), then ~~clears `+0x35C`/`+0x360` and the global arrays~~ nulls `02CA96E0` / `02CA96F8` at `+0x35C` *(corrected 2026-10-01, OPUS: GI-18 section)* |
| 19,20 | `0056960B` | ~~transition flags~~ transition finished: `002D7580(0, 1)` *(corrected 2026-10-01, OPUS: GI-18 section)* |
| 22 | `005696B9` | ~~secondary enable~~ position tween stepped: `002D78B0(6, rect)` *(corrected 2026-10-01, OPUS: GI-18 section)* |
| 26 | `00569ED4` | ~~`+0x331` byte → 6~~ `00568FE0(self, b, a)`, the per-row slide step (the `+0x331` store is the `0x121` arm) *(corrected 2026-10-01, OPUS: GI-18 section)* |
| 3,4,6,7,11,13,14,15,21,23,24,25 | `00569EF7` | default → `005C5230` |
| 0x121 | `00569EE3` (peeled `cmp`/`je`, not a table entry) | parent-destroy notification: sets `+0x331 = 6` when `+0x331` is nonzero |

The id-12 arm (`00569DC1`) is a five-way switch on `msg->a − 0x8000`:

- `0x8000` → loads strings `0xCEE`/`0xCEF`/`0xCF1`/`0xCF2` via `002F9860` (selected by `+0x33E`), formats through `00291D70`/`00291D80`, ~~stores the prompt id at `+0x344`~~ stores the tick `[0208F570]` at `+0x344` *(corrected 2026-10-01, OPUS: GI-18 section)* — the copy/paste-confirm prompt
- `0x8001` → `00569E4C` → `00567D80` (bank ops dispatcher), gated on `[[02CA9700]+0x360] == 0`
- `0x8002` → `00569E42` → `005679D0` (~~bank clear~~ pane rebuild *(corrected 2026-10-01, OPUS: GI-18 section)*)
- `0x8003` → ~~`0056A1D0` picker, then `00249C60` on the chosen index~~ when `00264150()` is 0, `0056A1D0(self, -1, b, 0, 0)` empties row `b`; a result other than -1 goes to `00249C60` *(corrected 2026-10-01, OPUS: GI-18 section)*
- `0x8004` → `005680E0` (~~bank move~~ pane reset *(corrected 2026-10-01, OPUS: GI-18 section)*) when `+0x342` is clear

## The screen-region members

Every listed member of the four gambit subtrees (`005691E0`, `0056B4D0`, `00566C10`, `0056C170` — union
172, per the atlas subtree rule: depth ≤3, stop at other widget procedures and >12-caller helpers) that
lives in the screen region `0x566xxx`–`0x56Cxxx` is below, each read and given a role and an interior
citation. The remaining ~123 subtree members are shared engine helpers, cited as families rather than
re-read: the menu-control `002Cxxxx` block (45 — button fields, pad helpers, `002C9430`'s sibling readers),
the text/list draw `002Dxxxx` block (32), the picker/sub-window `0027Exxx`–`0027Fxxx` five, text emit
`002Axxxx`/`002Bxxxx` (5), string fetch `002F8040`/`002F83E0`, the gambit-bank accessors `00327BA0`–
`00327BD0` + `GambitConfig_*`/`GambitRuntime_*` (documented on `09-Combat-AI-And-Gambits`), the
config-field setters `003682xx`/`003688xx`/`00368A60`, `0035F110`, `00367FA0`, `005C3A30`, and ten
interior call-targets the census has no entry for (`00567F6D`, `005687B9`, `005687D0`, `005691A6`,
`005693B0`, `00569659`, `00569BED`, `00569C12`, `00569EFC`, `0056A394`, `0056B372`, `0056BB5E`,
`0056C012`, `002C1CA6`, `002C3172`, `002C31BD`, `002C3357`, `002C338B`, `002D3FD8`–`002D42F8`,
`006F6033`) — these are arm addresses the procedures `call` directly, covered by their owners' rows.

| member | role | interior cite |
|---|---|---|
| `00566B70` | leaf-slot state write — `+0xE8` bit0 and `+0xE0`!=r11 gates; stores the `(r9&0xF)<<2|1` index nibble into `+0xC0`, positions `+0xC4`/`+0xC6`/`+0xC8`/`+0xCA`, a rip-global timestamp at `+0xD0`, the index at `+0xE0` | `00566BD9` `mov eax,[rip+0x1b28991]` |
| `00566C10` | ~~GambitIcon widget proc~~ tab-strip marker proc (ids 1,2,3,4; corrected 2026-09-29, GI-1) — see below | `00566C6C` `sub r8d,[rip+..]` (scroll global) |
| `00566FE0` | child-record flag clear — for the `+0x60` table's `+0xDA`/`+0xD8` indexed records, clears `rec+8` bit0; two paths by `+0x150` | `00567012` `and dword ptr [rax+8],~1` |
| `005674B0` | leaf setup — loops the `+0xC8` child array `+0x150` times; `002D04F0` picks show/hide per `[record+7]==+0xD4`, `00247870` each, writes positions `+0x98`..`+0x9E`, calls `00566B70` on the selected slot, `00566FE0` at the tail | `005675B7` `call 002D04F0` |
| `005678C0` | kind→value selector — `ecx`≠3 returns `dword_table[ecx]` via `lea rcx,[rip]`; `ecx`==3 returns 8 or 9 by `00254A10` | `005678CC` `lea rcx,[rip+0x7bbc25]` |
| `005678F0` | cursor blink/fade tick — `+0xC0` bits0-1 gate; elapsed `rip-global − +0xD0` through `00248F40` (curve `((+0xC0)>>2)&0xF`); `+0x343` = `+0xC4` + `+0xC8`·α; clears `+0xC0` bits0-1 at completion | `00567902` `mov r8d,[rip+0x1b27c67]` |
| `00567990` | bank-select refresh — `0056A010` + `00249C60` | `0056799D` `call 0027ED10` |
| `005679D0` | ~~bank clear~~ pane rebuild (the-two-transform-primitives.md) *(corrected 2026-10-01, OPUS: GI-18 section)* — `lea rbx` on the bank record, `0027Fxxx` ops | `005679E1` `lea rbx,[rip+0x2741cf8]` |
| `00567B60` | bank-copy row UI — `GambitConfig_CopySelectedBankForStatsIndex` (`00327C40`) + text emit | `00567B83` `call 00861EC0` |
| `00567D80` | bank-ops dispatcher — `00368240` + the `00567F90`/`005680E0`/`005687F0`/`00569F90`/`0056B350` cluster | `00567DA5` `call 00368240` |
| `00567F90` | bank edit (move/copy path) | `00567F95` `push rdi` |
| `005680E0` | ~~bank move~~ pane reset (the-two-transform-primitives.md) *(corrected 2026-10-01, OPUS: GI-18 section)* — `002CB9C0` + `00368830`/`00368A60` field setters | `005680EA` `mov rax,[rip+0x19dc73f]` |
| `00568280` | bank edit — `0056A010` + `00249C60` | `0056828D` `call 0027F360` |
| `005682C0` | editor fade controller — `+0x354`=`0x80808080`; `edx`→`+0x352` bits + `+0x350`=0x80; else ramps `+0x350` ±0x20 clamped [0x80,0xFF] | `005682CA` `cmp byte ptr [rcx+0x174],0` |
| `00568460` | `002B3050` layout position | `0056857D` `call 002B3050` |
| `005685B0` | `00243260` register + `002B3050` layout | `0056867C` `call 00243260` |
| `005687F0` | bank edit — `002CB9C0` + `00368830`/`00368A60` | `005687FF` `call 00368240` |
| `00568FE0` | commit wrapper — `lea rcx` on the config record then `00368250`→`00367FA0` | `00569002` `lea rcx,[rip+0x27406d7]` |
| `005691E0` | the gambit editor proc — §`005691E0` above | `00569222` `lea r15,[rip-0x449229]` (r15=image base) |
| `00569F90` | **bank→widget copy + commit** — loops `+0x126` times: copies `{word,word}` from `+0x192+i*0x20` to `+0xF4+i*4`, sets/clears bit `i` of `+0x124` by `+0x194` byte; tails `003282C0` (`GambitConfig_CommitBankAndRebuildRuntimeOrders`) | `00569FB0` `movzx eax,word ptr [r8-2]` |
| `0056A010` | character-change refresh — `00254A10` + `00282DF0` + `002CC2A0`/`002CEE00`/`002D1AC0` + `00567B60` | `0056A019` `call 002CC2A0` |
| `0056A1D0` | picker list builder — `002B58B0` + `002F9860` + `0035D330` + `00569F90` | `0056A23F` `call 002F9860` |
| `0056A3D0` | editor init/layout — `002497B0` + `002D66A0`/`002D78B0`/`002D7CB0` + `005685B0` + row emitters | `0056A3E9` `lea rcx,[rip-0x44a3f0]` |
| `0056A890` | picker-row emitter (list side) — `002B58B0`,`002D4650`,`002D48C0`,`002F9860`,`0031EB20`,`0035D330` | `0056A897` `call 00808F10` |
| `0056AAC0` | list page-up — `+0x595`-- (borrows `+0x596` when already 0), writes `8` to `[rip-global]+0xDE9`, zeroes `+0x580` | `0056AADA` `mov rax,[rip+0x1b3014f]` |
| `0056AB00` | picker close/apply — `0020E600` + `00244F00`/`002468A0`/`002470C0` + `002CC760`/`002D49C0`/`002D6620` | `0056AB1E` `mov rax,[rip+0x1b3010b]` |
| `0056AC50` | picker open — `00291D70`/`00291D80` + `002F9860` + `0056A1D0` | `0056ACAF` `call 002F9860` |
| `0056AD50` | list page-down — `+0x595`++ clamped `< +0x596−1`, wraps to 0, writes `4` to `[rip-global]+0xDE9`, zeroes `+0x580` | `0056AD79` `mov rax,[rip+0x1b2feb0]` |
| `0056ADA0` | leaf installer — `lea 0056C170`, `00244F50` + `005674B0`/`0056AE80`/`0056B100` | `0056ADAA` `mov rax,[rip+0x19d9a7f]` |
| `0056AE80` | ~~row-text emitter, condition side~~ **action**-picker tab builder — pages `byte[0208D300]`, menu kind `0x22`, tab frame 1 (corrected 2026-09-29, FABLE, GI-1) — `0031EB20` + `00327BA0`/`00327BB0` + `0035D330` | `0056AE89` `call 00808F10` |
| `0056B100` | ~~row-text emitter, action side~~ **condition**-picker tab builder — pages `byte[0208D310]`, menu kind `0x23`, tab frame 0 (corrected 2026-09-29, FABLE, GI-1) — `0031EB20` + `00327BC0`/`00327BD0` + `0035D330` | `0056B109` `call 00808F10` |
| `0056B350` | list installer — `lea 0056B4D0`, `00244F50`/`002468A0`/`00246AD0`/`002470D0` | `0056B35B` `mov rax,[rip+0x19d94ce]` |
| `0056B4D0` | the gambit list proc — §`0056B4D0` above | `0056B4DF` `mov rax,[rip+0x19d934a]` |
| `0056BC70` | picker-row emitter (twin) — same call set as `0056A890` | `0056BC77` `call 00808F10` |
| `0056BE40` | list layout refresh — `002D66A0` + `002D78B0`/`002D7CB0` + `00568460` | `0056BE66` `lea rcx,[rip-0x44be6d]` |
| `0056C170` | leaf slot proc (ids 1,18) — ~~per-slot container~~ tab-strip container: tabs `0056C060` plus the marker `00566C10` (corrected 2026-09-29, GI-1) | `0056C176` `mov rax,[rip+0x19d86b3]` |

### The list's id-12 sub-commands, decoded

The page's id-12 arm (`0056BA10`) computes `slot = (+0xF2 + +0xF4) * +0xEC + +0xEE + +0xED`, reads
`msg->a = [r8+8]` and the slot's record at `self + (slot+7)*0x20`, then:

| sub-id | arm | what it does |
|---|---|---|
| `0x8000` | `0056BAFD` | zeroes `+0x580`; copies the slot record's `+0x18` text into the `+0x380` double-buffer (page `+0x59E`, 0x100 each, `002B5680`), flips `+0x59E`, formats through `00291D80`/`00291D70` — **load the picked slot's text for the confirm prompt** |
| `0x8001` | `0056BABA` | `0056AC50(slot)` — **open the picker** on the selected slot; on success clears `+0xE0` bit `0x200000`, sets `+0x598`=0x20 and `[+0xC0]+0xFC`=0x18 |
| `0x8002` | `0056BA85` | three tests are *skip* conditions, not a conjunctive gate: `0056AB00` runs when `+0x5A0` bit2 is **clear**, or `+0x59B` != `+0x588`, or (both hold and) `+0x59C` == 0xFFFF — `+0x59C` != 0xFFFF instead returns 1 without calling — **picker close/apply** |
| `0x8003`/`0x8004` | `0056BB4F` | default arm — no dedicated handler |
| `0x8005` | `0056BA77` | `or +0x5A0, 1` — **set the list-mode flag** (`cmp rax,3` after `a−0x8002` reaches it only at `a==0x8005`) |

## `00566C10` — the GambitIcon widget

`00566C10` handles only ids 1, 2, 3, 4 (`00566C1F`–`00566C39`). Id 4 is a before-content draw: when `+0xE8 & 1` it calls `00242B90` with `[+0x38]` at position `+0xD4`/`+0xD6` minus the scroll globals (`00566C5A`–`00566C7D`). ~~Id 3 (`00566C8F`) loads resource `0x80`-family index `+0xDC` via `002CC8D0`/`002DD7E0` and draws the icon through `[+0x60][+0xD8]`. This is the small gambit-type icon the list renders per slot — a shared dialog, not a screen of its own (it has no input arm and answers only the construct/reconcile/draw ids).~~ **Corrected 2026-09-29 (FABLE, GI-1):** id 3 draws no icon: it computes a sine alpha `002CC8D0(0x80, 0x30, +0xDC, 2)` and writes it into the colours of layout elements `+0xD8`/`+0xDA` (`00566C8F`–`00566D2F`). The widget is the marker of a tab strip — two page arrows plus, when `+0xE8` bit 0 is set, one sliding pointer — and it is shared with the shop (`00567200` installs it too); see §*GI-1 answered 2026-09-29* below.

## `0056C170` — the leaf slot

`0056C170` handles only ids 1 and 18 (`0056C18A`–`0056C192`): construct and destroy. With no draw, no input, and no sub-command arm it is ~~a per-slot container the list installs through `0056ADA0` — the invisible parent rect each gambit row hangs its text and icon children on, not a separate screen.~~ **Corrected 2026-09-29 (FABLE, GI-1):** the pick list's **tab strip**, installed through `0056ADA0`: its construct builds one `0056C060` tab per page (`list+0x596` of them, records at `list+0x300`, `0056C250`–`0056C29E`) and then the marker `00566C10` with create-record `+0x14` = 1 (`0056C2D5`–`0056C35E`).

## The layout-key readers

*(2026-09-14, FRONTIER — LAYOUT-KEY-READERS.)* The `Gambit*` keys these bodies read — the "scroll
globals" the GambitIcon section above subtracts are in fact `GambitIconOffsetX`/`Y`:

| reader (→ owner) | keys | what the values do at the use site |
|---|---|---|
| `00566C10` P (GambitIcon widget) | `GambitIconOffsetX`, `GambitIconOffsetY` | `r8d − OffsetY`, `edx − OffsetX` then `00242B90` on `[rbx+0x38]` — the icon's draw offset inside its slot (`00566C6C`, `00566C73`) |
| `0056B350` (→`00567D80`→`005691E0`, editor) | `GambitActionListMoveX`, `GambitTargetListMoveX` | ~~`edx = −key`~~ **Corrected 2026-09-29 (FABLE, GI-1):** mode 1 (the target-condition list) reads `GambitTargetListMoveX` into `edx` unchanged (`0056B482`, key `01F2CB10`); any other mode (the action list) reads `GambitActionListMoveX` and negates it (`0056B48A`, key `01F2CB14`) → `002468A0` animated move — the X slide the action/target pick lists take when the editor opens them |
| `005691E0` P (gambit editor) | `BlackBandAnimTime` | `r8d` = band-anim ms → `002C9060`/`002C9890` (`005695B7`) |
| `005679D0` (→`005691E0`, the editor) | `DeftopBlackBandH`, `DefUnderBlackBandH`, `PartyBlackBandGradH`, `BlackBandAnimTime` | the editor's default/party band pair — heights → `002C9060` (`00567A98`) and `002C9490` (`00567ABA`), gradient → `edx` (`00567A92`), anim ms → `r8d` (`00567A8B`) |
| `00568460` (→`0056BE40`→`0056B4D0`, the list) | `GambitTutorial` Action/Target `OffsetX`/`OffsetY`/`Width`, `ChipHeight` | the tutorial hint's geometry — `OffsetX`/`OffsetY` word-added into the chip rect `[rbx]`/`[rbx+2]` (`00568511`, `0056851B`), widths/height consumed the same way down the body |
| `005685B0` (→`005691E0`, `0056A3D0`) | `GambitTutorialAction_ExtraWidth`, `GambitTutorialRectWindow_XOffset`, `…_YOffset` | `RectWindow_XOffset` word-added into the tutorial backing-rect origin `[rsp+0x68]` (`005686ED`) |

*(The two `GambitTutorial` readers left the frontier when the list/editor members above were cited;
their role lines are included here for completeness of the family.)*

## What this screen does

The list `0056B4D0` shows a member's twelve gambit slots; its id-12 arm maps the cursor through the same row/column math the quest list uses and forwards the pick to the editor. The editor `005691E0` is the actual editing surface: its id-10 arm moves the cursor over the child table, id-12 runs the bank operations (copy/paste/clear via `005679D0`/`00567D80`/`00567F90`/`005680E0`/`005687F0`, the condition/action pickers via `0056A1D0`/`0056A890`/`0056BC70`), and id-18 commits — `003282C0` is `GambitConfig_CommitBankAndRebuildRuntimeOrders`, the same function `09-Combat-AI-And-Gambits` documents as rewriting the runtime order-set the walk at `00305CC0` consumes. The screen→config→runtime chain is: editor close → `GambitConfig_CommitBankAndRebuildRuntimeOrders` → `GambitRuntime_RebuildOrderSetFromConfig` (`00328140`) → the battle walk.

## Not yet established

- ~~the per-leaf roles of `00566B70`..`0056AD50`~~ — all eight read 2026-09-15 (member table):
  `00566B70` slot-state write, `00566FE0` record flag clear, `005678C0` kind selector,
  `005678F0` cursor blink tick, `005682C0` fade ramp, `00569F90` bank→widget copy + commit,
  `0056AAC0`/`0056AD50` list page-up/down writing `8`/`4` to `[rip-global]+0xDE9`.
- ~~which `0x8000`–`0x8004` sub-command the list posts~~ — the `0056BA10` arm is decoded above:
  `0x8000` slot text for the confirm prompt, `0x8001` picker open, `0x8002` picker close/apply,
  `0x8005` list-mode flag (`0x8003`/`0x8004` go to the default arm).
- ~~whether `00566C10`'s icon set is condition- or action-type art~~ — **answered 2026-09-29 (FABLE, GI-1): neither; the premise was wrong** — §*GI-1 answered 2026-09-29* below. *History:* **narrowed 2026-09-15**: the
  icon index `+0xDC` is the only writer-visible field and it is populated inside `00566C10` from
  the global dword `02F8F570` (`mov eax,[rip+0x1b2860a]` at `00566F60`), not from a per-slot
  record. The question is now *who writes `02F8F570`* — that global's writer decides whether the
  art varies per gambit type.
  **Corrected 2026-09-18 (FABLE): the address was misread, and the record does decide.** The operand at `00566F60` resolves to **`0208F570`**, the 60 Hz tick counter every UI frame advances ([the blinking icon](../../99-Unresolved-Residual/the-blinking-icon-and-its-atlas.md) §5), and no `02F8F570` is referenced anywhere in the image; `+0xDC` therefore takes a timestamp, not an icon index. The type bit sits four instructions earlier: `00566F4E`–`00566F5A` take bit 0 of the row's `+0x14` dword (`[rdi+0x14]`) and merge it into the widget's `+0xE8` bit 0 by xor, ~~so the icon set does follow a per-slot record field. Which value of that bit is condition art and which action art is not established.~~ **Corrected 2026-09-29 (FABLE, GI-1):** `rdi` there is the widget's own create record, not a gambit row, and bit 0 means "draw and slide a pointer" (1 for the gambit strip, 0 for the shop strip); condition versus action is the pick list's `+0x588` and shows as the tab frame — §*GI-1 answered 2026-09-29* below.

## GI-1 answered 2026-09-29 (FABLE) — the tab-strip marker, and where condition vs action is decided

*(FABLE, Claude Opus 5.5 — NATIVE/STATIC, bodies read; control
[`gi1_tabstrip_marker.py`](../../_index/candidates/gi-0929-ui/gi1_tabstrip_marker.py), FAILS 0.)*

**The question's premise does not hold.** `+0x14` bit 0 does not select condition or action art, and `00566C10` draws
no condition or action icon.

**`00566C10` is the marker of a horizontal tab strip.** The `rdi` of `00566F4E` is the widget's own create record —
`+0`/`+8` its layout, `+0xC`/`+0xE` the two elements it animates, `+0x10`/`+0x12` elements hidden at construct,
`+0x14` flags (`00566ED8`–`00566F9C`) — built on the stack by its only two installers (the only rip references to
`00566C10`; no E8/E9 call reaches it):

| installer | strip | create `+0x14` | cite |
|---|---|---:|---|
| `0056C170` | the pick list's tab strip (one `0056C060` tab per page) | 1 | `0056C2F6`, `0056C304`; then sets `+0xE8` bit 1 (`0056C35E`) |
| `00567200` | the shop / bazaar tab strip (`00566A70` tabs) | 0 | `00567319`, `005673A3`, `00567438` |

Every reader of bit 0 is a pointer reader: id 4 draws one fixed frame through `00242B90` (its only caller is
`00566C7D`; the frame comes from the sheet `[[0209AC30]+0x378]`, no per-row index) at `+0xD4`/`+0xD6` minus
`GambitIconOffsetX`/`Y` (`00566C4D`–`00566C7D`); id 2 advances the pointer's slide (`00566DBB`); `00566B70` starts a
slide only when it is set, and `005674B0` calls it for the selected tab (`00567630`); construct seeds the pointer
position (`00566FB1`). **So bit 0 means "this strip has a sliding pointer"** — 1 for the gambit strip whether it lists
conditions or actions, 0 for the shop, whose selected tab is marked by brightness alone (`002D04F0` `0x80` vs `0x40`,
`005675AA`–`005675C5`). Whatever the bit, elements `+0xD8`/`+0xDA` are the two page arrows: id 3 pulses their alpha with
`002CC8D0(0x80, 0x30, +0xDC, 2)` = `0x80 + 0x30·sin(π·(now − t0)/30)` over table colour `002DD7E0(2)`
(`00566C8F`–`00566D2F`; `+0xDC` is the tick `0208F570` taken at construct, `00566F60`), and id 2 pushes them outwards
over four frames when `[0209AC30]+0xDE9` carries 8 or 4 (`00566D6B`–`00566DA9`) — the values the page flips write
(the gambit list's page-up and page-down `0056AAC0`/`0056AD50`; the shop's `00563EC0`, `00564300`).

**Where condition versus action is decided.** The pick list's `+0x588` comes from its create record `+0x18`
(`0056B6BC`–`0056B6BF`), which is the mode `0056B350` receives: `00567D80` passes 1 when the editor's column byte
`+0x33E` is 1 and 2 when it is 2 (`00567E0E`–`00567E73`); the editor's re-init `0056A3D0` rebuilds it from `+0x336`
(`0056A45B`–`0056A462`). `0056ADA0` then builds the tabs with `0056B100` when it is 1 and with `0056AE80` otherwise
(`0056ADC1`–`0056ADD1`):

| | mode 1 — **condition (target) picker** | mode 2 — **action picker** |
|---|---|---|
| tab builder | `0056B100` | `0056AE80` |
| pages | `byte[0208D310]` through `00327BD0` — the grid `GambitTargetDefinition_BindAndBuildMenuLookup` builds from the class-11 target-condition rows | `byte[0208D300]` through `00327BB0` — the action table's menu-position grid |
| `BattleMenu_BuildCommandEntryList` kind | `0x23` (`0056B1D4`) | `0x22` (`0056AF65`) |
| per-tab query | class 11 (`0056B273`) | class `0x14`, then class 1 (`0056B005`) |
| **tab frame** (record word `+4`) | **0** (`0056B1B8`); 2 when the page has nothing selectable (`0056B2B7`) | **1** (`0056AF49`); 3 when empty (`0056B060`) |
| list slide (`0056B350`) | `GambitTargetListMoveX` (`0056B482`) | `−GambitActionListMoveX` (`0056B48A`) |

The tab pane `0056C060` shows that word as the node's frame index (`0056C264` → `0056C0F9`). **Condition art is tab
frame 0 (2 when empty), action art frame 1 (3 when empty)**; what each frame depicts is in the atlas of layout
`[0209AC30]+0x50` entry 9, not in the code.

## GI-18: the editor's and the pick list's arms below entry level (OPUS, 2026-10-01)

Static, read whole from the shipping image, one level into each callee. The message names are the framework's
(the-widget-message-protocol.md): 1 construct, 2 reconcile, 5 draw after children, 8 / 9 focus gained / lost,
10 directional input, 12 sub-command, 15 about to be destroyed, 16 resource batch complete, 17 position tween
finished, 18 being destroyed, 19 / 20 transition finished, 22 position tween stepped, 26 per-element query.
Id-12 messages are `{12, a, b}` records from `00247510`. Both screens post them to themselves through
`002D1AC0(child, a)`, which supplies the child's cursor slot `(+0xF2 + +0xF4) * +0xEC + +0xEE + +0xED` as `b`.
The editor's row `i` is `self + 0x160 + i * 0x20`. `02CA96E0`, `02CA96F8` and `02CA9700` / `02CA9708` are the
three-editor pointer tables, one editor per gambit set.

**The editor `005691E0`.** Twelve table arms (ids 1, 2, 5, 8, 9, 10, 12, 16, 17, 18, 19/20, 22, 26 - 19 and 20 share
one) plus the peeled `0x121`:

| id | arm | work |
|---|---|---|
| 1 | `005692A2` | Setup. `+0x360 = 0`; claims the first free entry of `02CA96E0[0..2]` (`005692EB`) into `+0x35C`. Compared with the member's current set index (`dword [[02EBF190] + 0x7370 + member * 4]`), it places itself as the centre pane (`02CA9700`, layout element 6), the next pane (`02CA9708`, element 8) or the previous one (`02CA96F8`, element 7), each through `002432B0`. It wires the two list children, calls `002D45C0(child, 0)` (`0056945E`) and seeds nine word pairs at `+0x300`: the first word 1, the second 0 when `00264150()` is non-zero and 1 otherwise (`005694C6`-`005694F2`). It sets `+0x354 = 0x80808080`, `00285F20(member)` and `+0x343 = 0x80`. It then opens a resource batch (`00249580` / `00292210` / `00249410`) whose completion is message 16. |
| 2 | `005696A5` | `0056A3D0(self)` (the pane-transition state machine), then `005678F0(self)` (the cursor blink tick). |
| 5 | `00569718` | When the cursor row's byte `+0x17` is set (`00569751`), draws one fixed sprite from `[+0x38]` at `+0x348` / `+0x34A` (`002426F0`); `0056B350` writes all three when the pick list opens. |
| 8 | `0056961E` | `+0x358 \|= 1`; `002D45C0([+0xD8], 1)`; then posts `0x8000` to itself (`002D1AC0`). |
| 9 | `00569671` | `+0x358 &= ~1`; `002D45C0([+0xD8], 0)`. |
| 10 | `0056981E` | Nothing while `+0x360` is set. If the active editor's `+0x340` bit 0 is set, the input goes to the list child (`002D3A50`). Otherwise `002D45C0(child, 1)`; a non-zero `002C1A80` party gate undoes it and returns. It stores the slot and `+0x33E` in the editor's pair table. One pad branch moves the member's set index -1 mod 3 (`005699F0`), the other +1 mod 3 (`00569AF1`). Each plays sound `0x51`, slides the three panes (`002468A0`) and rotates the three pane pointers (`00569BED`-`00569C0C`). Masks `0x800` / `0x400` step to the next / previous member (`00568280` / `00567990`). With a non-zero slot, two more bits cycle `+0x33E` through 0-2. |
| 12 | `00569DC1` | Sub-command switch on `msg->a - 0x8000` (below). |
| 16 | `0056955F` | Starts the forward transition (`00246AD0`), lazy-creates two helper widgets (`002CBE40`, `002CF3E0`), then **snapshots** the live set `+0xF4..+0x127` into `+0x128..+0x15B` (`005695CE`-`005695FE`). |
| 17 | `00569781` | Only for `msg->a == 1`. A pending edit (`+0x360`) is committed through `00569F90` and cleared. A pending pick-list close (`+0x342`) clears the cursor row's `+0x17` (`005697F5`) and re-enables the list child (`002D49C0(child, 0)`). |
| 18 | `00569236` | `002922F0()`. **Only when byte `[[0209AC30] + 0xDEB]` is set** does it write the id-16 snapshot `+0x128`, not the live set, through `003282C0(member, self + 0x128)` (`0056924B`-`00569259`). The centre editor also calls `002814E0(0x4B9)`. It then nulls `02CA96E0` / `02CA96F8` at `+0x35C` (`0056928F`, `00569293`). |
| 19, 20 | `0056960B` | `002D7580(0, 1)`. |
| 22 | `005696B9` | When `+0x33B` is set, `005685B0(+0x336, +0x337, &rect)` and `002D78B0(6, rect)`. |
| 26 | `00569ED4` | `00568FE0(self, msg->b, msg->a)`: the per-row slide step (rows `+0x18` state, `+0x1A` current, `+0x1C` target, 4 units per call), copied to the child's `+0x114` / `+0x116`. |
| `0x121` | `00569EE3` | `+0x331 = 6` when `+0x331` is non-zero. |

| id-12 sub-id | arm | work |
|---|---|---|
| `0x8000` | `00569E6D` | Prompt text `0xCF1`, or `0xCEE` / `0xCEF` for `+0x33E` 1 / 2, or `0xCF2` when `msg->b` is 0 (`002F9860`, `00291D70`, `00291D80`); then `+0x344 = [0208F570]`, the tick (`00569ECA`). |
| `0x8001` | `00569E4C` | `00567D80(self, msg->b)` when the centre editor's `+0x360` is clear: opens the pick list (`0056B350`, modes 1 / 2). |
| `0x8002` | `00569E42` | `005679D0(self)`, the pane rebuild. |
| `0x8003` | `00569E06` | When `00264150()` is 0: `0056A1D0(self, -1, msg->b, 0, 0)`, mode -1. That empties row `b`: both texts `0x3EB`, id `-1`, bit `b - 1` of `+0x124` cleared, then committed. A result other than -1 is played as a sound (`00249C60`). |
| `0x8004` | `00569DED` | `005680E0(self)`, the pane reset, when `+0x342` is clear. |
| other | `00569EF3` | returns 0. |

**The pick list `0056B4D0`.** The 19 table entries; ids 3-7, 11, 13, 14, 16 and 17 share `0056BB53` (`005C5230`,
`xor eax, eax; ret`):

| id | arm | work |
|---|---|---|
| 1 | `0056B57F` | `[02CA96D8] + 0xC8 = 0` (`0056B58D`). Builds two layout descriptors, `00D234A8` (callback `0056BBD0`) and `00D234D0` (callback `0056A780`). It copies the create record (editor `+0xC8`, `+0x584`, `+0xD0`, mode `+0x588`) and the editor's cursor bytes into `+0x58E`..`+0x59C`, then lays out the first page (`0056ADA0`, `0056BC70` / `0056A890`). |
| 2 | `0056B9D4` | `0056BE40(self)`; then counts `+0x580` down. At zero it posts `0x8000` to itself (`0056BA04`). `+0x580` is a frame countdown, set to `0xB4` by `0056AC50` (`0056ACBB`). |
| 8 | `0056B7E9` | `+0x5A0 \|= 2`; `002D45C0([+0xC0], 1)`. |
| 9 | `0056B808` | `+0x5A0 &= ~2`, then the id-15 tail. |
| 10 | `0056B81E` | Page up / page down on the pad masks (`0056AAC0` / `0056AD50`; wrapping needs a second mask), clamping the cursor to the new page's count. Without a page change the input goes to the list child (`002D3A50`). |
| 12 | `0056BA10` | `0x8001` → `0056AC50(self, row)`. It shows a refusal text and arms the `0xB4` countdown for a disabled row. Otherwise `0056A1D0` writes the picked id into the editor's row (mode 1: word `+0x10`, mode 2: word `+0x12`) and commits. `0x8002` → `0056AB00`, the close. |
| 15 | `0056B80F` | `+0x580 = 0`. |
| 18 | `0056B516` | Sends `{0x121}` to the editor `[+0xC8]` when `+0x58E` is set; `[02CA96D8] + 0xC8 = 1`. |
| 19 | `0056B7AE` | With `+0x58E`: `+0x58F = 0x18`, word `+0x58C = 0x302`; with `+0x5A0` bit 2: editor `+0x358 \|= 2`. |

**Not established here:** what sets `[0209AC30] + 0xDEB` (no writer in the gambit region), so whether id 18's
snapshot write is a revert-on-cancel; which of the three pad words `02F97390` / `02F97392` / `02F97394` is pressed,
repeat or held. What the player sees is not claimed.

## Falsification pass

**Pass 1 — 2026-09-14 (OPUS).** Attacked at parent `GN160` (`fa0db293…`), EXE `73461d08…`, every
test decoding the instruction stream with capstone rather than matching bytes. Instrument:
`Tools/work/OPUS/falsify_gambit_screens.py`. **Nine claims attacked, eight survived, one falsified
and corrected above.**

| claim | the killer | result |
|---|---|---|
| `0056B4EE` loads `[rdx]` | the instruction does not dereference `rdx` | **survived** — `mov eax, dword ptr [rdx]` |
| `0056B4F5` bounds `msg->id` to `0x12` | the instruction there is not a compare against `0x12` | **FALSIFIED** — `0056B4F5` is `mov rsi, rcx`; the bound is `0056B4F8 cmp eax, 0x12` |
| the table at `0056BB80` carries the 9 documented arms | an arm the table does not carry | **survived** — **9 of 9**, read as image-base + `rel32`, index `id−1` |
| arm `0056B516` checks `+0x58E`, reads `[self+0xC8]`, posts `{0x121,0,0}` through the child's **first** vtable slot | `0x121` absent, no indirect call, or the call is not through slot 0 | **survived** — `cmp byte [rsi+0x58e],0`; `mov rcx,[rsi+0xc8]`; `mov dword [rsp+0x60],0x121`; `mov rax,[rcx]`; `call rax` |
| `cmp eax,0x121` / `je 00569EE3` at `00569204`–`0056920F` | either instruction is not as published | **survived** — both exact |
| `lea r15,[rip-0x449229]` at `00569222` sets `r15` = `0x120000` | the `lea` resolves anywhere else | **survived** — resolves to `00120000` exactly |
| the editor's table at `00569F1C`, target = `0x120000 + rel32`, index `id−1` | a documented arm the table does not produce | **survived** — ids 1/2/5/8 → `005692A2`/`005696A5`/`00569718`/`0056961E` |
| `0056B350` `lea`s `0056B4D0` | the procedure is not among the installer's RIP-relative `lea`s | **survived** |
| `0056ADA0` `lea`s `0056C170` | same | **survived** |

**Two of the three tests that first reported a failure were the instrument, not the page**, and both
are recorded in the script so the mistake is not repeated: a vtable call need not carry a bracket
(`mov rax,[rcx]` then `call rax` **is** a slot-0 call, and demanding `[` in the operand reported the
page false), and the destroy window was read correctly but judged by the wrong predicate. **The
sharpest claim on the page — that a `lea` with a specific displacement yields exactly the image
base — is also the one that would have been easiest to get wrong, and it is exact.**

**Not attacked by this pass**, and ~~still `PARTIAL` on the editor's 12 sub-commands and the
list's 19 arms below entry level~~ *(read 2026-10-01, OPUS: the GI-18 section)* — registered as **GI-18**. The other two reasons the page
gave are settled: ~~the per-leaf roles in *Not yet established*~~ *(all eight read 2026-09-15,
member table)* ~~and whether `00566C10`'s icon set is condition- or action-type art~~
*(settled 2026-09-29 (FABLE, GI-1): `00566C10` is a tab-strip pointer, not condition/action
art)*.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (33 edges through 11 of this page's functions).** The ActorEntity layer reaches this page at `00263E30`, `00326D60`, `0031EB20`, `00326BB0` and 7 more. `FUN_002367a0` is the worked example, read in full - it is a 126-byte search over the battle-unit pool at `[0208E688]`, bounded by the same `[0208E6A0]` slot count, and entered only when the id passes its validity query with **selector `2`**; **7 of the 17 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleStats_ResolveByActorHandle`, owned by that layer, calls `00263E30` on this page. That caller is a 55-byte resolver behind the same `byte[02089340] & 0x10` gate as the focus-handle pair: it takes the handle through `003588B0` and `00263E30` and returns the resulting unit's `+0x698` **stats record** rather than the unit itself; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — SERVICE.** `0031EB20` on this page calls `BattleUnit_ResolveByFocusHandle`, owned by that layer. What it reaches is a 42-byte resolver gated on bit 4 of `byte[02089340]`: it takes the focus handle through `003588B0` and tail-jumps to `00263E30`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 32 edges measured).** The gambit
screens draw through the render layer's widget machinery: `00579420`
(`Presentation.UI.Quest.ListScreenSelectionStateMachine`, 5 edges) and `002BAF80`
(`Presentation.UI.InputConsumerStateMachine`) drive `002470D0`/`00247510`/`00247870`/`00249C60`/
`002D45C0`/`002D48C0`; the nine-patch backgrounds `002455A0`/`00245170`, icon draws `002BCB00`/
`002B8EE0`, ShaderMaterial `002B0280`/`00578450`, ScreenCapture `002D2DB0` and post-process binding
`0029A930` reach the same helpers via `00243260`/`00248F40`/`002DD7E0`/`0035D330`/`005C3A30`;
`0031EB20` calls `BattleUnit_TestActorViewFrustumAtCurrentPosition`. The screens are rendered by
these bodies — the crossing is the draw path, not a second owner.

**Movement — MECHANICAL (SWE2-CONTRACT 2026-09-15, 10 edges).** All 10 edges are Movement bodies
(`00326BB0`/`00326D60`/`003911D0`/`00329B00`/`003377C0`/`00329A80`/`00319490`/`0033C310`/
`BattleLocomotion_QueryDynamicActorObstruction`/`PartyFollow_SolveFormation`) sharing the single
cited accessor `00263E30`. Pure fan-in.
- **Input - CLIENT and SERVICE (8 edges).** `005C3A30` is called by bodies filed to Input: `001E0A10`, `001E0D80`; `002BAF80`, `002D3A50`, `0056A3D0`, `0056AB00` (+1 more) reach bodies filed to Input: `001E0A10`, `001E0E30`, InputGameplay_TestFilteredMask92Bit0WithTemporalGate (`00250130`), `002D6620` (+1 more) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (6 edges).** `002D66A0`, `002D78B0`, `002D7CB0`, `00568460` (+1 more) are called by bodies filed to Script_VM_Native_Bridge: `005109B0`, `00510A40`, `00510AE0`, `00510B80` (+2 more) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - SERVICE (7 edges).** `002BAF80`, BattleMenu_BuildCommandEntryList (`0031EB20`), `00326D60`, `00329A80` (+2 more) reach bodies filed to WorldAreaField: MapRef_GetPersistenceGroupId (`00264F90`), FieldData_GetActiveFieldRecordBit15 (`00313F60`), WorldTransition_GetActiveOrPendingFieldId (`003148F0`) - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - MECHANICAL and SERVICE (3 edges).** `003160C0` calls `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) - accessor fan-in - while `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`) reaches `00315390`/`003166F0`.
- **Spawn_Encounter_Lifecycle - MECHANICAL (3 edges).** all 3 edges are spawn-lifecycle bodies (`Spawn_ValidateCandidateDistanceToPlayers` `00234DA0`, `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0`, `SpawnKeep_RotatePersistenceBanksForAreaTransition` `00233780`) calling the shared accessors `FieldData_GetActiveFieldRecordBit15` (`00313F60`) and `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) - fan-in on two accessors, not a per-caller relationship.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22, FRONTIER's debt (SWE2-FRONTIER, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, `SWE2-FRONTIER-PASS22-DEBT-OWN`, batch 2): the layers pass 22 still reported for this page. Every edge was listed in full and the cited function's body was read.*

**Save_Load_Settings — CLIENT (14 edges).** The save controllers call the widget helpers the gambit panes use: `00247510` sends a widget message: it builds a kind-`0xC` message carrying the caller's two arguments and calls the handler at `[obj+0]` when the object and handler are non-null (six callers); `00247870(w, on)` sets or clears bit 1 of the widget flags at `+0x40`, and refreshes the widget through its layout routine when bit `0x20` is set (five callers). `SaveSlotMetadata_BuildSubmissionDescriptor` (`005832B0`) calls the game-mode test `00254A10`, which returns 1 when the game mode is 0, 7, 8, 10 or 11 (bit mask `0xD81`). `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`) reads a character record through `00282DF0` (`qword [[0209AC30] + idx*8 + 0xAC8]`). `00581930` looks an id up through `002DD7E0`, which returns the id's dword from a bounded table or `0x80808080` when the id is out of range or the table is absent. These are shared UI and lookup helpers; the save layer owns the controllers and shares no gambit state.

**Resource — SERVICE (1 edge).** The gambit editor `005691E0` claims a slot through `00249580`, which takes the first free entry of a 12-entry, 32-byte table, clears it and stores its argument at `+8`. The resource layer owns that table; the editor is one of its clients.

**Input — CLIENT and SERVICE (7 edges, batch 6).** `002D3A50` calls the Input bodies `001E0A10` and `001E0E30`. The pick list's handlers call two small Input-owned setters: `0056A3D0` and `0056BE40` call `002D66A0`, which stores a non-zero word into three adjacent globals; `0056AB00` calls `002D6620`, which sets one byte to 1 and one qword to -1. In the other direction, the Input bodies `001E0A10` and `001E0D80` call `005C3A30`, a four-byte getter of `dword [rcx+0xC]`. The gambit screens read and reset shared input state through these calls and own none of it.

**Script_VM_Native_Bridge — CLIENT (6 edges, batch 6).** Five script-command bodies call helpers this page cites. `005116E0` calls the word setter `002D66A0`. `005109B0` calls `002D78B0`, which writes four words into record `i` (at most 7, stride `0x18` from `+0xC0`) of the object at `[[0209AC30]+0xF0]` and clears bit 4 of its `+0x14`. `00510A40` and `00510AE0` call `002D7CB0`, which sets or clears a flag in the same record. `00510B80` and `00510C80` call `00568460` and `005685B0`, which first resolve the active character's gambit set from the pointer table at `02CA96E0`. Scripts set these records and gambit state through the same entry points the screens use.

**WorldAreaField — SERVICE (4 edges, batch 6).** `BattleMenu_BuildCommandEntryList` (`0031EB20`), `00326D60`, `00329A80` and `003911D0` call `FieldData_GetActiveFieldRecordBit15` (`00313F60`), a tail jump to the field record's bit-15 read. These bodies ask the field's permission bit, and the field layer owns it.

## SWE2-EC7-213 update (2026-10-03) - the fsmenu chip verbs on the gambit editor

Four `fsmenu_*` Script-VM verbs (family 7, the fullscreen-menu set) drive the gambit editor `005691E0` from a script. The editor's setup arm stores the centre editor (`02CA9700`) at `[0209AC30] + 0x160` (`0056951A`), and the centre editor's destroy arm clears it (`0056927A`). Three of the bodies (the two begins and the `registopenchip` poll) index the three-editor table `02CA96E0` by the member's current set index, `dword [[02EBF190] + 0x7370 + member * 4]`, with `member` = dword `+0xF0` of the `+0x160` editor, which they read without a null test. The two begins and the chip poll use the pane-transition state byte `+0x331` that `0056A3D0` switches on. `005688A0` (37 B; the poll of `fsmenu_changechip` `0x700B`, `fsmenu_movechip` `0x700C` and `fsmenu_movelist` `0x700D`) returns 1 when `[0209AC30] + 0x160` is null; otherwise it returns 1 when that editor's byte `+0x331` is 0, and 0 when it is not (`sete`).

Interior anchor `005688B5` (function `005688A0`).

`00568940` (70 B; the poll of `fsmenu_registopenchip`, `0x7035`) looks up that table entry and returns 1 when it is null, else bit 1 of its dword `+0x358` (`shr eax, 1` then `and eax, 1`), the bit the pick list's id-19 arm sets on the editor.

Interior anchor `0056897A` (function `00568940`).

`00568990` (159 B; the begin of `fsmenu_movechip`, whose handler pops the verb's one argument into `ecx`) acts only when the table entry is non-null and its byte `+0x331` is 0. It stores `+0x331` = 1, `+0x336` = `cl`, `+0x337` = the cursor slot of the list child at qword `+0xD8` (`(+0xF4 + +0xF2) * +0xEC + +0xEE + +0xED` on bytes, kept to 8 bits), `+0x330` = 1, `+0x339` = 1 and `+0x33B` = 0.

Interior anchor `005689D5` (function `00568990`).

`00568A30` (111 B; the begin of `fsmenu_movelist`, argument in `ecx`) has the same guard and stores `+0x336` = byte `+0x33E` (the column), word `+0x330` = `0x101` (bytes `+0x330` and `+0x331` both 1), `+0x337` = `cl`, `+0x339` = 1 and `+0x33B` = 0. Both begins therefore put the editor in state 1 of `0056A3D0`. The begins write the table entry, while the `005688A0` poll reads the `+0x160` editor and waits for its `+0x331` to return to 0.

Interior anchor `00568A7D` (function `00568A30`).
