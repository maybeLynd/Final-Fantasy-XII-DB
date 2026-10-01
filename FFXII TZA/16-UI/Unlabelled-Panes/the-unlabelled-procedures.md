---
id: ui-unlabelled-panes
title: The 25 unlabelled atlas procedures — sorted by installer ancestry into their owning screens
status: "DOCUMENTED — GI-6 answered 2026-09-29 (FABLE), review (FABLE-REQ-AUDITSEM-REVIEW-GI-UI, ACCEPT, d998217e2); documented_rule.py READY, no open box or live id; owner re-status 2026-09-30 (SWE2-FRONTIER, record dd-restatus-gi-0930). Was PARTIAL on: the pages' own kind byte (2 vs 5) and which selections each 0056EF60 kind sets are not established; the 0xC0368C / 0xC036A4 contents decoded 2026-09-18"
evidence_tier: 1
tags: [ui, menu-screens, unlabelled]
addresses:
  - "00560910"
  - "005701B0"
  - "00571A50"
  - "005742D0"
  - "005789D0"
  - "00579420"
  - "00579AF0"
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
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: opus-unlabelled-panes-pass-1 - all 25 rows attacked three ways at GN160 and every one holds: each row's named installer really carries a rip-relative lea of its procedure (25 of 25, from the image), every subtree size matches the menu screen atlas (25 of 25), and the atlas names an installer the page also names on every row (25 of 25). The page's one id-set claim, 00578450 answering ids 1/10/12/14, is exact. No correction
  crossref_clean: false
  reopened_count: 0
---

# The unlabelled procedures

**Status:** PARTIAL — the 25 atlas rows with no layout-key evidence, grouped by installer ancestry and dispatch shape. "Unlabelled" does not mean unexplained: every row's installer lands inside a labelled screen's subtree, so each is a pane of a known screen or a screen the key-family evidence can't see. Roles below are structural + signature-level; the four big families got dispatch reads.

## The classification

| procedure | subtree | installed by | resolves to |
|---|---:|---|---|
| `00560910` | 41 | `005601B0` | **license-board launcher** (screen) | · `0056091F`
| `005599D0` | 15 | `00559860` | license-list pane — its subtree carries `00559E30`, the license-entry builder | · `005599EC`
| `00558BB0` | 3 | `00560910` | license pane (leaf) | · `00558BE3`
| `005595E0` | 2 | `00561E90` | license pane (leaf) | · `005595E9`
| `005618E0` | 6 | `00561830` | license pane (subtree `00556380`) | · `0056191A`
| `005701B0` | 47 | `0056EC10` | **handbook text pane** — calls the `00181B90`–`00181DD0` markup-parser family | · `005701C6`
| `00571A50` | 47 | `00570BF0` | **handbook content page** — kind byte `arg+8` → `+0xE8`, `003946B0` layout `0x2C`/`0x2F` | · `00571A69`
| `005742D0` | 35 | `00570080` | **handbook content page** — kind byte `arg+8` → `+0x8060`, `0x3E80`-byte record array at `+0x41E0` (`00574381`–`00574390`), `003946B0` layout `0x23`/`0x26`/`0x27` | · `005742D8`
| `00570630` | 9 | `00570080` | handbook pane (subtree `00576C70`) | · `00570641`
| `00570530` | 3 | `0056EF60` | handbook pane (leaf) | · `00570560`
| `0056FCB0` | 2 | `005742D0` | handbook pane (leaf) | · `0056FCDE`
| `0056FD30` | 1 | `0056FEF0` | handbook pane (leaf) | · `0056FE26`
| `00570460` | 1 | `0056FEF0` | handbook pane (leaf) | · `0057047F`
| `00573B40` | 1 | `00574BA0` | handbook pane (leaf) | · `00573B70`
| `00574AD0` | 1 | `00574A00` | handbook pane (leaf) | · `00574AF4`
| `00579AF0` | 33 | `00579990`/`00579A40` | ~~**the item/equip host**~~ **the Hunts host** (corrected 2026-09-29, FABLE, GI-6: pane kind 6 is the handbook category "Hunts", and `00579990`/`00579A40` are called only from `0056EE10`) — `0056EE10` installs it for `0056EF60` pane-kind 6; its id-`0x10` arm installs `00579420` always and `005789D0` + a `00577F00`-pane when `+0xD0` bits 1|2|0x10 are set (`00579CDF`–`00579D25`) | · `00579B41`
| `005789D0` | 42 | `00578920` | **item/equip screen** — `arg+0` dword → `+0xC0`, `0029DBE0`/`0029DF20`/`0029E330`/`0029E770` family | · `005789EF`
| `00579420` | 27 | `00579130` | **item/equip screen** — `002526F0`/`002527B0` inventory accessors + `0037E4F0` | · `00579444`
| `00578450` | 5 | `005781A0` | item-screen input pane (ids 1,10,12,14; `005781A0` inside `005789D0`'s subtree) | · `00578463`
| `00577F90` | 2 | `00577F00` | quest-list pane (leaf) | · `00577FBC`
| `00566A70` | 2 | `00567200` | shop pane — `00567200` is installed by `00567190` (shop subtree) | · `00566A9E`
| `00567200` | 1 | `00564010`/`00567190` | shop pane (leaf) | · `00567209`
| `0056C060` | 2 | `0056C170` | gambit pane — child of the `0056C170` leaf slot | · `0056C090`
| `005677A0` | 2 | `00567770` | **member-scoped pane of the `00280DE0`/`002D70F0` screen family** — installed by config-root `00280DE0`'s id-16 rebuild arm (`00280E98`) and by `002D70F0`'s `+0x278`==`0x40` command arm (`002D725D`); its `0056C3A0` resolves the `+0xDE0`-indexed character record via `00282DF0` → `+0xC0`, `+0xC4` | · `005677E3`
| `0057F7D0` | 5 | `00583990` | save/load pane — `00583990` sits next to `00583FD0` (`SaveWrite` subtree) | · `0057F80A`

## `00560910` — the license-board launcher

The largest unlabelled procedure (1401 B, 20 arms through `00560E8C`) and the one that is a screen in its own right:

- **id 1** `005609D9`: clears `+0x38 & ~0x80` on two `[global]` widgets via `0024A5A0` (`005609E0`/`005609F8`), installs a dialog descriptor `005D2680` via `00247570` (`00560A09`), `+0x185` = 1, `+0x188` = −1, `00285F20` on `msg->a` (the member index), registers `self` into `[global]+0x158` (`00560A40`), sets `[global2]+0xD3C |= 0x10`, spins on `[global3]` (`00560A60`), `00249580` + child create
- **id 18** `00560956`: the mirror — sets `+0x38 |= 0x80` on the same two globals, `0055FA50` + `002922F0` teardown, `002814E0`(0x4B5), clears `[global]+0x158`
- **id 12** `00560D54`: sub-commands `0x8000`–`0x8003` — `0x8000` reads the cursor slot off `+0xC0` with the standard list math and indexes a `+0x120` row table (`00560E17`–`00560E4C`); `0x8001` resolves `+0xD0` → character via `00282DF0`, reads `[char+0x60]` through `00323670`, calls `00561DC0`, then `00244DD0` (`00560DC2`–`00560DFB`) — the member's license state drives the pick; `0x8002` → `00283840`(2) + `00244F00` + `002CA110`; `0x8003` → `+0x180` = `0x401` + `002D7580`
- **id 16** `00560AB2`, **id 10** `00560CE8`, **id 14** `00560BAD`, **id 8/9** `00560C12`/`00560C64`, **id 19/20** `00560BFF`/`00560BCF`

Its subtree contains `00561300` — the license-screen lazy-create — and `00558F20` (the tile-view installer): this screen *can install the board itself*. It is the intermediate license screen the menu opens before the grid — the board/member chooser.

## `005701B0` — the handbook text pane

608 B, ids 1,10,12,14,15,16,18,19. Installed by `0056EC10` (inside `0056EF60`'s pane subtree). Its call set is the `00181B90`–`00181DD0` block plus `001846B0`/`001846F0` — a self-contained text/markup family no other screen touches — and the quest-list cluster `00575A50`/`00575B80`/`00575D10`/`00575DD0`/`005760A0`/`00576300`/`00576860`/`00576E30`/`005778F0`/`00577A00`. This is the pane that renders a handbook page's body text — the markup reader.

## `00571A50` and `005742D0` — the handbook content pages

Both take `msg->arg+8` as a kind byte (`+0xE8` / `+0x8060`) ~~compared against 2 and 5 (`00571ABD`, `00574373`)~~ **Corrected 2026-09-29 (FABLE, GI-6):** `00571A50` compares its byte only against 5 (`00571ABD` and three more sites); `005742D0` against 5 (`0057432F`, `00574373`) and 2 (`0057439C`); the byte is the `0056EF60` pane kind itself — §*GI-6 answered 2026-09-29* — then pick `003946B0` layout sets `0x2C`/`0x2F` and `0x23`/`0x26`/`0x27` respectively. `005742D0` additionally zeroes a `0x3E80`-byte record array at `+0x41E0` (500 × `0x20` records — the large-chapter list) and reads `arg+0x10`/`+0x18` into `+0xE8`/`+0xD0`. They are sibling content pages the handbook viewer hosts — chapter lists vs. detail pages. `00579AF0` is the third sibling (installed by `0056EF60`-subtree members `00579990`/`00579A40`).

## `005789D0` / `00579420` — the item/equip pair (split resolved 2026-09-15)

*Note 2026-09-29 (FABLE, GI-6): their host `00579AF0` serves `0056EF60` pane kind 6, which `0056F2A0` titles **Hunts** (§*GI-6 answered 2026-09-29*); the "item/equip" reading below was not re-derived against that and is routed to this page's owner.*

Both are children of **`00579AF0`**, the kind-6 pane of the `0056EF60` content host (`00574E80`
frame, launched through `002814E0`→`00575580`/`00574CB0`). The host's id-`0x10` notification arm
installs them from the same context record `{+0xC0 kind, +0xD8 ptr, +0x110 ptr}`:

- **`00579420`** (0xE0 widget, `[global]+0x118`) — the **always-installed list pane**: its
  installer `00579130` forwards only the kind byte. Calls `002526F0`/`002527B0` (the
  inventory-count accessors the shop's `00564780` also uses), `002D48C0` count publish,
  `0037E760`×2 + `00579FA0` category→count (`ecx`∈{0,1,2}→`edi`), and `005C5230` default
  dispatch. This is the bag/category list half.
- **`005789D0`** (0x1A8 widget, `[global]+0x120`) — the **conditional member-scoped pane**,
  installed only once `+0xD0` bits 1, 2 and 0x10 are all set. Its installer `00578920` forwards a
  richer record — `+0x130` dword, member byte (`+0x138 >> 0xB`, sourced from `arg+9`),
  `+0x13C`/`+0x13D` bytes — and it drives the `0029DBE0`/`0029DF20`/`0029E330`/`0029E770`
  item-data family, `0037EDB0`/`0037F130`/`0037FD50`/`0037E5B0`/`0037E8D0` accessors, and
  installs the input pane `00578450` (ids 1,10,12,14) via `005781A0` twice (`00578BBE`,
  `00578BEE`). This is the per-member detail half — the equip/use-target view.
- Both call `00577E10` (shared close) and sit under menu command routing that pairs them with a
  `00577F00`-installed leaf (`00577F90`).

`00579AF0` itself dispatches ids {1, 2, 0x10, 0x12} (default `005C5230`): id 1 copies the
`arg` record (`arg+8` kind→`+0xC0`, `arg+0x10`→`+0xC8`, `arg+0`→`+0x130`, `arg+4`→`+0x134`,
`arg+9`→`+0x138` bits, `arg+0xA`/`+0xB`/`+0xC`→`+0x13C`/`+0x13D`/`+0x13E`); id 0x10 handles
sub-notifications {0, 2, 8, 9} on `msg->a` (0 and 2 set `+0xD0` bits 1/4 and drive the install
path, 8 sets bit 2 + `003800A0(1)`/`0037FE40(1)` when `+0xC0`==1, 9 destroys via `00244F00`);
id 2 runs the `+0xC2` countdown; id 0x12 is the teardown (`002CC9C0(0xC8)`, `00393900`/
`003938B0`, `00285EE0` on `+0x130`, posts `{0x12,0xF}` to `+0xC8`, clears `[rip+0x272fb59]`).

The item/equip family's two `uisize.json` readers (LAYOUT-KEY-READERS, 2026-09-14):

- **`005789D0` P** reads `NaSPArtSignalOffsetX/Y` — `edx − OffsetY`, `ecx = OffsetX` → `0029E770`
  (`00578C6F`, `00578C75`): the same signal-sprite placement call the location map's `002BA700`
  uses — the help/N-A signal on the member detail pane.
- **`00565E00`** (the tail-jump-installed widget the protocol page's DL-2 list names) reads
  `mCommandMenuStrHeight` → `eax` beside the `[rdi+0xC0]` record (`00565F65`), `mCommandMenuOffsetY`
  → byte `[rdi+0x1F9]` (`00566013`), and the `BlackBandAnimTime`/`PartyBlackBandGradH`/
  `ListHelpBlackBandH` triple → `ecx`/`edx`/`r8d` into `002C9490` (`00566171`–`00566184`) — the
  item screen's band plus command-menu metrics in one body.

**The same arm pair installs the kind-6 host under the `0056EF60` content host** — `0056EE10`
reads the `+0xC8` kind byte (set by `0056F2A0` from `00574E80`'s `00575480` arm): kinds 0–5 →
`00570BF0`→`00571A50` pages at slot-arg 4, kind 6 → `00579AF0` (via `00579990` or `00579A40`
when `[global]+0xC0` bit `0x40` is set), kind 7 → `00572E10` (0x1208 B viewer) — all at
slot-arg `0xA`. `0056EF60` is therefore not handbook-specific: it is the shared content-pane
host the `00574E80` frame instantiates per menu selection.

## What this settles

All 25 unlabelled rows resolve to panes of documented screens or to three screen families the key evidence missed (license launcher, handbook content pages, item/equip). None is a previously-unknown top-level surface — the atlas's "no evidence" set is explainable by shared `MenuList`/`General`/`ItemSort` keys that the labeller correctly refused to count.

## Not yet established

- ~~the `arg+8` page-kind values inside `00571A50`/`005742D0` (2 vs 5 → which page type) — the
  pane-level kind byte is resolved (`0056EF60`/`+0xC8`: 0–5 `00570BF0` pages, 6 `00579AF0`,
  7 `00572E10`), but the second-level kind the pages read is not~~ — **answered 2026-09-29 (FABLE, GI-6)**: there is no
  second-level kind; the pages read the pane kind, which is the handbook category — §*GI-6 answered 2026-09-29* below
- ~~which concrete menu selection sets each `0056EF60` kind value~~ — **answered 2026-09-29 (FABLE, GI-6)**, same section
- ~~the `0xC0368C`/`0xC036A4` shared lookup tables' full contents~~ — **decoded 2026-09-18**: ~~both are 6-byte records `{paneKind, flag, u16, u16}`;~~ **Corrected 2026-09-29 (FABLE, GI-6):** they are one run of 6-byte records `{u16 title, u16 help, u8 value, u8 flag}` starting at `00D23688` — four category-menu rows (value = the kind the row posts) then eight kind rows at `00D236A0` (value = the category's cursor slot); the reads at `+0xC0368C`/`+0xC036A4` land on the value byte, `+4` into each record (§*GI-6 answered 2026-09-29*); the four `0xC0368C` rows are on [the shared dialogs page](../Shared-Dialogs/the-shared-dialog-widgets.md) and the eight `0xC036A4` rows on [the handbook page](../Handbook/the-handbook-screen.md).

## GI-6 answered 2026-09-29 (FABLE) — the kind byte is the handbook category

*(FABLE, Claude Opus 5.5 — NATIVE/STATIC, bodies read; titles resolved from the shipped `penelosdiary.bin` /
`help_penelosdiary.bin`; control [`gi6_handbook_category.py`](../../_index/candidates/gi-0929-ui/gi6_handbook_category.py),
FAILS 0.)*

**There is no second-level kind.** Both pages take the `0056EF60` pane kind unchanged: `00571A50` through `00570BF0`,
whose only caller passes the pane's `+0xC8` (`0056EE28`, `0056EF1A`, `0056EF27`; stored at `00571A99`); `005742D0`
through `0056EC10` → `005701B0 +0xE1` → `00570080` (`0056EC63`, `00570202`, `005700E4`; stored at `00574328`). And the
kind is the **handbook (Clan Primer) category**: `0056F2A0` titles it from 6-byte records
`{u16 title, u16 help, u8 slot, u8 flag}` at `00D236A0` (`0056F324`–`0056F32F`):

| kind | title (help) | cursor slot | page |
|---:|---|---:|---|
| 0–3 | rows 0–3 of `penelosdiary.bin` — empty in `us`, "Unused" in `de` | 11–14 | none reaches them |
| 4 | **Traveler's Tips** ("Hints for the wary adventurer.") | 15 | `00571A50` |
| 5 | **Bestiary** ("Insights on foes you have defeated.") | 17 | `00571A50`; its detail page opens the monster viewer (`00570245`–`0057025A`) |
| 6 | **Hunts** ("Hunt information and progress.") | 16 | `00579AF0` |
| 7 | **Sky Pirate's Den** ("What will it take to fill the den?") | 18 | `00572E10`, the `menuhandbook_order.bin` viewer |

The slot is where each category keeps its cursor: the page teardown stores it with `002527B0(6, slot, cursor)`
(`00571ECD`–`00571EDB`).

**Which selection sets each kind.** `0056F2A0` has one caller, the back panel's `0x8001` arm (`00575424`–`00575480`),
and two bodies post that `0x8001`:

* **The category menu `0056F810`**, whose rows come from the four records just before the kind rows, at
  `00D23688` — same shape, same text ids (labels read at `0056F694`–`0056F69A`) — in fixed order, each shown only when
  unlocked (`0056F750`): **Hunts → kind 6**, **Bestiary → 5**, **Sky Pirate's Den → 7**, **Traveler's Tips → 4**. The
  row's value byte is read at `0056F98D` and posted at `0056F9B5`. Hunts and Bestiary need the unlock sync `00577550`
  and persistent flag `0x400B`; Sky Pirate's Den needs `0x400B` only; Traveler's Tips needs the sync only. The last
  category is kept in counter bank 6 slot 3 (`0056FA4F`).
* **A direct open into Hunts:** a back panel created with a payload — `00575580`, reached only from the request router
  `002814E0` — sets `+0xC0` = `0x40` (`00574F3C`), and `00574D00` then posts kind 6 itself (`00574D92`–`00574DA9`);
  `0056EE10` routes it through `00579A40`. The plain main-menu open `00574CB0` (from `00281ED0`) carries no payload.

**Nothing sets kinds 0–3.** So in `005742D0` (layout `0x26` for kind 2, `0x23` for 5, `0x27` otherwise,
`0057439C`–`005743B9`) kind 5 is the Bestiary detail page, kind 4 the Traveler's Tips page, and the kind-2 branch —
like `0056EF60`'s own `kind == 2` test at `0056F1D1` — belongs to a category no menu row reaches. The same table's
framing on [the handbook page](../Handbook/the-handbook-screen.md) is corrected by that page's owner. *Not tied here:
which router request the player triggers for the direct Hunts open.*

## Falsification pass

**Pass 1 — 2026-09-14 (OPUS).** Attacked at parent `GN160` (`fa0db293…`), EXE `73461d08…`.
Instrument: `Tools/work/OPUS/falsify_unlabelled.py`, which parses the 25 rows **from this page's own
table** rather than transcribing them, because 25 hand-copied rows is itself a place to introduce an
error. **Four claims attacked, four survived. No correction.**

This page's whole argument is the installer ancestry — *"'Unlabelled' does not mean unexplained:
every row's installer lands inside a labelled screen's subtree"* — so the killer is an installer that
does not install what its row says, which would remove the evidence for that row's placement.

| claim | the killer | result |
|---|---|---|
| every row is installed by the procedure(s) named | a named installer with **no** rip-relative `lea` of its procedure | **survived — 25 of 25**, decoded from the image |
| the 25 subtree sizes match the menu screen atlas | any row differing from the atlas | **survived — 25 of 25** |
| the atlas names an installer this page also names | a row where the two disagree | **survived — 25 of 25** |
| `00578450` answers ids 1, 10, 12, 14 | any other id reaching a real arm | **survived — exact** |

**Every one of the 25 placements rests on an installer relationship that is really in the image**, so
the classification stands on its stated evidence rather than on adjacency.

**Two rows name two installers each** — `00579AF0` from `00579990`/`00579A40` and `00567200` from
`00564010`/`00567190` — and the atlas records both of each in a single cell. Comparing that cell as
one string reported both rows as disagreements; they agree.

**Not attacked by this pass:** the *"resolves to"* column's role attributions, which are structural
and signature-level by the page's own statement, and the four big families' dispatch interiors.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **World — CLIENT.** A cited procedure is called by a 122-byte World-labelled body.
- **WorldAreaField — SERVICE.** Cited procedures call `WorldTransition_GetActiveOrPendingFieldId` (2), `FieldData_GetVariable0` and a 529-byte field body.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Movement — SERVICE.** `002D70F0` on this page calls `FUN_00326bb0`, owned by that layer. What it reaches is a one-time reset guarded by bit 0 of `[022C25A0]`: it stamps a table of `0x30`-byte slots from `022C25B0` with `0xFFFF` sentinels and zeroed counters; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — SERVICE.** `005760A0` on this page calls `FUN_00315420`, owned by that layer. What it reaches is an 80-byte per-id lookup: ids at or above `0x200` return `-1`, and the rest index `byte[singleton + id + 0x3404]` - the same query the equipment-slot eligibility test recurses into; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 44 edges measured).** The unlabelled
procedures run inside the render layer's UI machinery: `00579420`
(`Presentation.UI.Quest.ListScreenSelectionStateMachine`, 11 edges) and the input-consumer state
machines `002BAF80`/`002B7B80` drive `00244DD0`/`00249580`/`002526F0`/`002527B0`/`002D48C0`/
`0029DBE0`/`0029E330`, `00181DD0` is called by ten Presentation bodies
(`VFXSystem_RenderLayerPass`, the fullscreen-overlay `002512B0`,
`CharacterRender_UpdateCombatLookAndAuxControllers`, …), and `00570630`/`005789D0`/`00572E10` reach
the quad-emit `002D9DB0`/`002DA2D0` and quest-metadata `0037E5B0`/`0037E8D0` callees. The panes are
procedures the render pass installs and calls — the crossing is their runtime home.

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 16 edges).** 9 edges are the
`0020E600`/`0020E620` image-pointer pair; the rest are the frame-mode getters
`00229DF0`/`00229E70`/`00229EA0` consulted by `00244DD0`, the `001E0580` helper and
`MainLoop_UpdateAndRenderFrame` reaching `00181DD0`.

**Resource — SERVICE (SWE2-CONTRACT 2026-09-15, 21 edges).** The pane procedures call the Resource layer's generic
helpers: `00249580` (8 edges, from `002B7B80`/`002BAF80`/`002D70F0`/`00560910`/`0056F2A0`/`00572E10`),
`0024A5A0` (4, from `00280DE0`/`002814E0`/`002D70F0`/`00560910`), `0024A680` (3), `003933F0` (2),
`002493D0`/`003934F0`/`0024A440`/`00393460` (1 each). The panes fetch their resources through these
helpers — mechanical helper-sharing, named.

**ActorEntity — SERVICE (SWE2-CONTRACT 2026-09-15, 2 edges).** The input-consumer `002B7B80` calls `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0` and `Actor_GetWorldPosition` `00265020` — the pane resolves the actor it displays. Small, real.

**Script_VM_Native_Bridge — SERVICE (24 edges, one shared subject; the accessor and a caller read in
full).** Twenty-three of the twenty-four edges are script bodies reading one function cited here,
`Actor_GetWorldPosition` `00265020`, which has seventy-nine callers in all. It is worth stating
exactly what it answers, because it is a script verb's whole view of where something is: a null
actor writes **zero into all three out-parameters** and returns; a non-null one has its kind taken
from `byte[actor+3] >> 5` and must be **1 or 3**, and anything else gets the same three zeros; only
then are three dwords copied out of `[actor+0xB8]`. So a script that asks for the position of the
wrong kind of thing is told the origin, not told no.

`00345830` is the worked example of a caller — a verb handler that pops its arguments through
`00267DB0` `VMValueStack_PopNumericDiscard` into `xmm6`/`xmm7` before asking. The twenty-fourth edge
is `00354D00` reading `00229EA0`, two instructions: `movsx eax, byte [02064AD3] / ret`.

So the crossing is **one shared position read with twenty-three callers on that layer**, not
twenty-three relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14
(OPUS).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22, FRONTIER's debt (SWE2-FRONTIER, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, `SWE2-FRONTIER-PASS22-DEBT-OWN`, batch 2): the layers pass 22 still reported for this page. Every edge was listed in full and the cited function's body was read.*

**Save_Load_Settings — CLIENT (8 edges).** The save controllers drive this page's pane helpers. `SaveLoad_ControllerTransitionStateMachine` (`00580EB0`), `SaveLoad_ControllerLifecycleHandler` (`00582860`, e.g. `00582E64`–`00582E67` with message index `rdi + 0xE`) and `SaveLoad_HandleStorageStatusResultAndAdvanceController` (`00583040`, `0058321A`–`0058321F`) call `00583990`. That routine is the save/load message dialog: it indexes a 31-entry `{text id, kind}` table, fetches the strings, picks one of two texts by the game-mode test `00254A10`, and builds the dialog widgets. `SaveWrite_OperationStateCallback` (`0057E4D0`) calls its sibling `00583FD0` at `0057E569`, which reads the same table. `00582860` also lays itself out through `003946B0` with layout 6 (`005829C0`–`005829D0`); that routine copies four words from a layout record to `+0x98`..`+0x9E`. It calls the menu routine `002814E0` with `-2` (`00582F09`–`00582F0E`). `00583040` passes its dialog's widget at `+0xC8` to the widget updater `00244DD0` (`0058315C`–`00583168`). `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`) reads a character record through `00282DF0`, which returns `qword [[0209AC30] + idx*8 + 0xAC8]`. The save layer owns the controllers and uses this page's pane routines to show state; nothing here writes save data.

**SaveLoad — CLIENT (1 edge).** `00582790` (197 B, filed to no owner, resolved by the audit to SaveLoad) claims a slot through `00249580` on entry (`0058279D`). That routine takes the first free entry of a 12-entry, 32-byte table, clears it and stores its argument at `+8`. The body then loads a file through `00249210` (`005827FE`). It is a client of the shared slot table.
