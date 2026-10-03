---
id: ui-shop-screens
title: The shop screens — the menu list, the trade panel, and the item list
status: "DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS; documented_rule READY): GI-17 answered 2026-10-01 (OPUS, static - the id-20 arm helpers `002D45C0`/`002CFCF0`/`0027EE80` read, see the GI-17 section; review requested from SWE2-AUDIT-SEM). GI-5 answered 2026-09-29 (FABLE), review (FABLE-REQ-AUDITSEM-REVIEW-GI-UI, ACCEPT, d998217e2). History: PARTIAL on GI-17 from 2026-10-01 (SWE2-FRONTIER, on SWE2-AUDIT-SEM's REJECT of c97af7156, record dd-restatus-gi-0930); earlier PARTIAL on: +0xE4 mode values beyond 0x1C0/0x2C0 are not established; 0057A4E0's contents read 2026-09-18 (a styled text element torn down at shop state 3)"
evidence_tier: 1
tags: [ui, shop, menu-screens]
addresses:
  - "0057B890"
  - "0056D370"
  - "0057AC10"
  - "0057A620"
  - "0057A4E0"
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation delta - every function this document cites whose record differs between the stamped snapshot and GN161's gained a plate comment and tags ONLY (empty comment before, tag set a subset, checked field by field), and this document makes no uncorrected absence claim about any of them; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 7 cited address(es) among the 128 records changed across GN158..GN161; each differs only in comment and tags; 0 live absence claims (check_stranded_absence.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-DELTA-RELIANCE-BASIS; re-measured and applied for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-14
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: opus-shop-screens-pass-1 - the menu list's dispatch read from the image at GN160 and it is exact: bound 0x13 at 0057B89D, table 0057BCE4, ELEVEN ids at the eleven published arm addresses, and 3-7/9/11/13/17 all resolving to the published default 0057BCD6. No correction
  crossref_clean: false
  reopened_count: 0
---

# The shop screens

~~**Status:** PARTIAL~~ *(Superseded 2026-10-01, OPUS: DOCUMENTED - see the status line; GI-17 answered)* — — the five widget procedures, the installer chain, both dispatch tables, and every listed screen-region member are cited below with interior citations (2026-09-15); the 157 shared listed subtree members are cited as engine-helper families.

## The tree

Two related widgets form the shop. The **shop menu list** `0057B890` (atlas label "shop + menu list", requesting `Shop_8_c.tm2`) is the top-level screen the menu system enters — its construct arm at `0057B8BD` stores `msg->arg` (the shop id) at `+0xC0`, reads the active member index `[global + 0xDE0]` into `+0xC1` at `0057B92F`, and allocates a `0x7D0`-byte state block via `002497E0` at `0057B906`. The **trade panel** `0056D370` (atlas label "shop", `ShopItem` layout keys) is the item-quantity surface — its id-2 arm at `0056D5C7` calls the installers `0057A480` and `0057A980` (`0056D618`/`0056D64B`), so the two "child" rows belong to it:

| procedure | role | installed by |
|---|---|---|
| `0057B890` | shop menu-list screen (root) | `0057B800` |
| `0056D370` | trade/quantity panel | `0056C950` |
| `0057A620` | item-list container | `0057A980` (called by `0056D370`) |
| `0057AC10` | shop item list | `0057A620` |
| `0057A4E0` | leaf widget (construct/reconcile only) | `0057A480` (called by `0056D370`) |

## `0057B890` — the menu list

Dispatches `msg->id` bounded to `0x13` at `0057B89D` through the table at `0057BCE4`:

| id | arm | role |
|---|---|---|
| 1 | `0057B8BD` | construct: shop id → `+0xC0`, member index → `+0xC1`, `0x7D0` state alloc, `0057B780`/`003678F0`/`0057B400` init, `00292FA0`(3) + `002CF8B0`(1) + `002839B0` |
| 2 | `0057BA31` | reconcile: if `+0x150 & 0x10` and `00283980` reports ready → `00283940` + `00245020` |
| 8 | `0057BA60` | cursor move: when `+0x150 & 0x20` (or not `& 8`), clears `+0xC4`, calls `0057BD40`, then highlights the row — indexes `+0x148`'s cursor through the same `(+0xF2 + +0xF4) * +0xEC + +0xEE + +0xED` slot math (`0057BA9B`–`0057BAC5`) and posts to `+0xD0`'s row table |
| 10 | `0057BB00` | directional input forwarded to `+0x148` via `002D3900` |
| 12 | `0057BB1D` | sub-commands: `0x8000` re-highlight row `msg->b` (`0057BB4B`); `0xF` toggle `+0x150 & 0x20` and clear the child's `+0xE0 & 0x200000` list-mode bit (`0057BB8C`); `0x12` → `002470D0` + set that bit (`0057BB6E`); `0x8001` → `0057C070` (mode switch) |
| 14 | `0057B9E2` | transition started: `+0x150 &= ~8` |
| 15 | `0057BC18` | about-to-destroy: `+0x150 |= 8`; unless `& 4`, tears down via `002CA110`/`00291D40`/`00292B10`/`002CF870` |
| 16 | `0057B977` | refresh: `002FAE40` on `+0xC0` (shop-name lookup), `00246AD0`/`00291D80`/`002CFCF0`/`003EABE0`/`002CA150`/`002CE7A0` repaint |
| 18 | `0057BC6D` | destroy |
| 19 | `0057B9F1` | `+0x150 & 4` → clear it; else `002470D0` + `0057B4A0` if `& 2` |
| 20 | `0057BC52` | flag set |
| 3–7,9,11,13,17 | `0057BCD6` | default → `005C5230` |

The `0x8001` arm `0057C070` calls `002CBDA0`/`002CC2A0` then `0056DD50` + `0057BD40` + `0057BEE0` — the buy/sell mode switch that rebuilds the panel.

## `0056D370` — the trade panel

Dispatches ids 1, 2, 12, 18 (`0056D399`–`0056D3B3`):

- **id 1** `0056D66A`: construct
- **id 2** `0056D5C7`: reconcile — when `+0xE4 & 0x10` and `002A2620` is ready, clears the bit and the parent's `+0xE0 & 0xE3FFFF` mask (`0056D5F3`), then branches on `+0xE4 & 0x3FC0`: `0x2C0` → `0057A480` (`0056D61E`); else if `003933D0` passes → `0057A980` + `002CC4F0` (`0056D648`)
- **id 12** `0056D3E5`: sub-commands `0xF`, `0x8000`, `0x8001`, `0x8002` — `0x8001` (`0056D42B`) requires `+0xC8` set, then when `+0xE4 & 2` computes `count × price` — `imul` of `[+0xD0]+0x10` by `+0xDC` with `btr ebx,0x1F` (`0056D45A`–`0056D46C`) — formatted through `00310870`/`002FEEB0`; ~~`+0xE4 & 0x3FC0 == 0x1C0` selects the sell-side path~~ **Corrected 2026-09-29 (FABLE, GI-5):** the sell path is `+0xE4` **bit 0** (`0056D46F` → `Shop_CommitSaleItemAndGil`, else `Shop_CommitPurchaseItemAndGil` at `0056D49A`); `& 0x3FC0 == 0x1C0` (kind 7, loot) only adds the loot-sale counter `00316A50(0xE, …)` (`0056D488`–`0056D498`) — §*GI-5 answered 2026-09-29*
- **id 18** `0056D3C2`: destroy — frees `+0xC8` through `003697F0` (`0056D3D2`)

`+0xDC` is the quantity and `[+0xD0]+0x10` the unit price — this is the "how many" counter where cost accumulates. ~~`+0xE4 & 0x3FC0` distinguishes the panel modes (buy `0x1C0` vs sell `0x2C0` choose which child gets installed at reconcile).~~ **Corrected 2026-09-29 (FABLE, GI-5):** `+0xE4 & 0x3FC0` is the **goods kind** of the current tab shifted left 6 — `0x1C0` is kind 7 (loot), `0x2C0` kind 11 (bazaar); buy versus sell is bit 0. Kind 11 rebuilds through the bazaar leaf `0057A480`; the item-list container `0057A980` follows a purchase whose goods pass `003933D0` (`0056D604`–`0056D64B`). All fields and values: §*GI-5 answered 2026-09-29*.

## `0057A620` and `0057AC10` — the item list

`0057A620` (827 B, ids 1, 12, 18) is the container `0056D370` installs through `0057A980` (`lea 0057A620` inside `0057A980`). `0057AC10` is the item list proper — installed by `0057A620`, an 18-id dispatch through `0057B154`: id 1 `0057AC51` reads the window rect `[msg->arg]+4..+0xA` into `+0x98..+0x9E` (`0057AC6A`–`0057AC96`) and takes `+0xC0`/`+0xC4` from the arg's `+8`/`+0xA` words (shop id / category), id 10 `0057ADE8` directional input, id 12 `0057B0FD` sub-commands, id 14 `0057AD4C`, id 15 `0057B112`, id 18 `0057B125`, id 3 `0057B0C8` draw.

## `0057A4E0` — the leaf

`0057A4E0` (313 B) answers only ids 1 and 2 — construct and reconcile. It and its twin `0057A300` both call `0030BAF0` + `0035D380` — a stock/availability descriptor row, not a screen.

*Contents read 2026-09-18 (FABLE).* **Id 1** stores the argument's `+8` at `+0xE8` (its owner), calls the twin `0057A300(argWord, &+0xC0)`, asks `0056E880([02CA9790]+0xC0 kind, 0xB, 1)` and, by its answer, chooses the style byte `01E0C3D0` or `01E0C3DC`; it then builds a **0x18-byte element descriptor** on the stack — flags 3, that style byte, the byte `01E0C3CC`, a word of `−1`, and the two procedures `0057B6A0` and `0057C010` (`0057A593`–`0057A5D3`) — and creates the element through `003F47E0(twinResult, &+0xC0, descriptor, [02CA9790]+0x158)`, which is a thin wrapper that calls the widget factory `00244F50` with procedure `003F4840` and a `0x130`-byte record; finally it registers with `0208EA28` (`00244960`). **Id 2** asks the shop state getter `003F4670` — the byte `[02B5F1F8]+0xC0`, or 3 when the shop object is absent — and, at state 3, posts command `0xF` to its owner unless `+0xCA` is set and destroys itself (`0057A502`–`0057A52F`). So the leaf is a one-line text element with a style chosen by the pane kind, torn down when the shop leaves its trading state. Static: the body decoded in full.

## The screen-region members

Every listed member of the five shop subtrees (`0057B890`, `0056D370`, `0057A620`, `0057AC10`,
`0057A4E0` — union 226, atlas subtree rule: depth ≤3, stop at other widget procedures and
>12-caller helpers) living in the screen region `0x56xxxx`–`0x57xxxx`, each with a role and an
interior citation (2026-09-15). The remaining **157 listed** subtree members are shared engine
helpers, cited as families each named with representative members: the `002Cxxxx` menu controls
and `002Dxxxx` text/list draws (the same families the gambit screens use —
`002CA3B0`/`002CA5C0`/`002CA5D0`/`002CAFE0`/`002CB1F0`/`002CB360`/`002CB790`/`002CB850`/
`002CB8B0`/`002CBA50`/`002CBC20`/`002CBC50`/`002CC5F0`/`002CC630`/`002CC660`/`002CC780`/
`002CCB10`/`002CCCA0`/`002CCD40`/`002CD150`/`002CF890`/`002D14E0`/`002D8B00`), the `002Fxxxx`
string fetchers and resource helpers (`002F83E0`/`002FABD0`), the `shop_table` accessors
documented under `12-Items-Equipment-Shops-License` (`0030A4E0`/`0030B180`/`0030B270`/`0030C410`/
`0030F9A0`/`00317930`/`00317B70`/`00318B40`/`0031A510`/`00323C60` plus `0030B4B0`/`0030B630`/
`0030BAF0`) and the `Boundary.ItemsEquipment` support (`002CA7C0`/`00324380`/`00324470`/
`0037B4B0`/`0037CA80`/`003FEAD0`/`00469E80`), the `PlatformOnlineAchievements` accessors the
panel's `00315420`-family calls reach (`0020CE00`/`0020CE60`/`00254E80`/`00282FA0`/`00315E90`/
`003160C0`/`003161A0`/`003165C0`/`003166F0`/`00316760`/`00316A50`/`00316BF0`/`008632B0`), the
Input predicates (`00197700`/`001986D0`/`001E0A10`/`001E0E30`/`001E0E50`, boundary `00368360`),
the UI transform evaluator and UI helpers (`00367820`/`00368010`/`003687C0`/`003688E0`/`00368940`,
`0027F210`/`00285F20`/`0028E8B0`/`002BE020`), the `0028xxxx`/`0029xxxx` format-and-character
helpers (`002699D0`/`0027ED10`/`0027F360`/`00282EE0`/`00282F80`/`00283840`/`00292140`/`002922F0`/
`00293170`/`002A1D20`/`002A1DC0`) and the encoded-message formatters `002B4810`/`002B49F0`,
`003933B0`/`00394790`/`003948B0`/`003949B0`/`003985B0`/`00398910`/`003938B0` stock gates and
texture helpers, the `0020E600`/`0020E620` record walkers, `00246450`/`00246480`/`002524C0`/
`002E42D0`/`002ECEC0`/`003F47E0`/`003FE3F0`/`003FE410` misc predicates and adapters,
`00300E40` (ActorEntity), `0030ADC0` (Gameplay.Combat), `003105D0` (CombatAction), `00225570`
(Audio), `00320D50` (SaveLoad boundary), `005112A0`/`00235DC0` thunks, and `00808C40`/`00861EC0`
CRT. A further **28 call-targets carry no census entry**
(`002CABB6`, `002CBB55`, `00316045`, `00316B73`, `00316BD1`, `00317AEE`, `00317AF3`, `00318317`,
`00318A6C`, `0036878A`, `003687A2`, `0038A691`, `003957E0`, `003FED9C`, `004078D0`, `004F0700`,
`0056C815`, `0056D845`, `0056D847`, `0056E9A0`, `0057A941`, `0057A943`, `0057AB86`, `0057ADC4`,
`0057B13A`, `0057BA14`, `00582777`, `00596B19`) — arm bodies inside listed owners, covered by those
rows rather than re-entered.

| member | role | interior cite |
|---|---|---|
| `00564780` | inventory-count query — `002526F0`/`00252D10`/`00252D40` + the `0057D5E0`/`0057D610` stubs | `005647BB` `lea rcx,[rip+0x19c83ce]` |
| `00564AC0` | child create — `00244F50` + `00808C40` | `00564AC6` `mov rax,[rip+0x19dfd63]` |
| `005655F0` | row cleanup — `0020E620`/`002D48C0`/`002F9860`/`003697F0` + `00565A00`/`0057CF20` | `00565639` `call 003697F0` |
| `005670F0` | leaf helper under `00567690` | `005670F3` `mov r8,rcx` |
| `00567190` | child create — `lea 00567200` | `00567197` `mov rax,[rip+0x19dd692]` |
| `005674B0` | leaf setup (shared with the gambit list) — `00247870`/`002D04F0` + `00566B70`/`00566FE0` | `005675B7` `call 002D04F0` |
| `00567690` | `002D04F0` + `005670F0` leaf pair | `005676FE` `call 002D04F0` |
| `0056C490` | **the quantity-entry body** (959 B) — `00243260` + `00291D80`/`0029FA40`/`0029FB50`/`002F9860` + `00567690`/`0056E700`; the "how many" number pad | `0056C4F0` `lea rcx,[rip+0x7b7089]` |
| `0056C850` | panel child create/refresh — `002445C0`/`00244F00`/`00246AD0`/`00293110`/`002D45C0` + `0056C490`/`0056E410`/`0056E5D0` | `0056C899` `call 002D45C0` |
| `0056C950` | `0056D370` installer — `lea` at entry, `00244F50`/`00246AD0`/`002D45C0` | `0056C95A` `mov rax,[rip+0x19d7ecf]` |
| `0056D370` | the trade panel proc — §above | `0056D37F` `mov rax,[rip+0x19d74aa]` |
| `0056DC30` | `0056DD50` helper — `lea` on a screen-region proc | `0056DC37` `lea rdx,[rip-0x44dc3e]` |
| `0056DD50` | **panel rebuild** — installs the whole child set (`00564780`/`00564AC0`/`00567190`/`005674B0`/`0056C950`) and the `0056E140` widget (`lea` at `0056DD66`) | `0056DD66` `lea r9,[rip+0x3d3]` |
| `0056E410` | stock-row builder — `0030B4B0`/`0035D380`/`003697F0`/`003933B0` + `005655F0` | `0056E49D` `call 003933B0` |
| `0056E580` | leaf/format helper | `0056E5AB` `mov rcx,[rip+0x1b20476]` |
| `0056E5D0` | row text emitter (name + price) — `00291D80`/`00293100`/`002CC2A0`/`002CC4F0`/`002F9860` + `0056E880` | `0056E61C` `call 0056E880` |
| `0056E700` | leaf/format helper under `0056C490` | `0056E702` `xor eax,eax` |
| `0056E880` | price-format dispatch into the `0057D5E0`/`0057D600`/`0057D610` stubs → `0057D620` | `0056E8AF` `call 0057D600` |
| `0057A300` | twin of `0057A4E0` — `0030BAF0` + `0035D380` descriptor row | `0057A32C` `call 0035D380` |
| `0057A480` | `0057A4E0` installer | `0057A484` `mov rax,[rip+0x19ca3a5]` |
| `0057A4E0` | leaf proc (ids 1,2) — stock/availability descriptor row | `0057A502` `call 003F4670` |
| `0057A620` | item-list container proc (ids 1,12,18) | `0057A62B` `mov rax,[rip+0x19ca1fe]` |
| `0057A980` | `0057A620` installer — `lea 0057A620` inside | `0057A984` `mov rax,[rip+0x19c9ea5]` |
| `0057AA00` | item-list row builder — `0020E600`/`00254A10` + `002B4090`/`002B40C0`/`002B58B0` + `002F9860`/`0035D380` + `003948B0`/`003949B0` | `0057AA40` `call 0035D380` |
| `0057AC10` | the shop item-list proc — §above | `0057AC1C` `mov rax,[rip+0x19c9c0d]` |
| `0057B1A0` | per-row emitter incl. character/equip state — `0016D6A0` + `00282DF0`/`00282EA0` + `0029FB50`/`002B58B0`/`002CA490`/`002CC2A0`/`002CC4F0`/`002F9860` | `0057B1B2` `mov rax,[rip+0x19c9677]` |
| `0057B400` | init — `002C9BF0` + `002CD3C0`/`002CD4D0` | `0057B421` `call 002CD4D0` |
| `0057B4A0` | select+lookup — `00249C60` + `002F9860` + `003949B0` | `0057B4D4` `call 002F9860` |
| `0057B500` | the Buy/Sell menu-option rows — `0020E600` + `00252F40`/`00252FA0` + `002FA920`/`002FAD30` + `0056E840`/`0056E860` | `0057B570` `lea rcx,[rip-0x45b577]` |
| `0057B660` | leaf helper under `0057BEE0` | `0057B663` `test dl,dl` |
| `0057B680` | leaf helper — `0056E140` id-1 calls it with 0 | `0057B687` `test rdx,rdx` |
| `0057B6F0` | gil/price text — `002FA920`/`002FAD30` + `0030B4B0`/`0030B630` | `0057B715` `call 002FAD30` |
| `0057B780` | construct init — `002491B0`/`00249580`/`002920C0`/`00292190`/`002CBD50`/`002F8040`/`003933F0` | `0057B78D` `call 00249580` |
| `0057B890` | the menu-list proc — §above | `0057B8A6` `lea rcx,[rip-0x45b8ad]` |
| `0057BD40` | header/column repaint — `002C9F20`/`002CD420`/`002DD7E0`/`002F9860` + `0056E880`/`0057B6F0` | `0057BD5C` `mov rax,[rip+0x19c8acd]` |
| `0057BEE0` | window rebuild — `00292B70`/`002932F0`/`002B3050` + `0057B500`/`0057B660` | `0057BEF4` `mov rax,[rip+0x19c8935]` |
| `0057C070` | **mode switch** — `002CBDA0`/`002CC2A0` + `0056DD50` + `0057BD40` + `0057BEE0` (the `0x8001` arm target) | `0057C0C1` `mov rax,[rip+0x272d6c8]` |
| `0057D5E0` | format stub → `0057D620` family | `0057D5E4` `lea rcx,[rip-0x45d5eb]` |
| `0057D600` | format stub (`mov eax,6` then shared tail) | `0057D602` `mov eax,6` |
| `0057D610` | format stub (`jmp 0057D620`) | `0057D613` `jmp 0057D620` |
| `0057D620` | **the price/name formatter** (1,088 B) — `0020E600` + `00252F40`/`00252F70`/`00252FA0` + `002FAD30` + `0057CE10`/`0057DAD0`/`0057DD60`/`0057DED0` | `0057D646` `call 0057CE10` |

## The layout-key readers

*(2026-09-14, FRONTIER — LAYOUT-KEY-READERS.)*

| reader (→ owner) | keys | what the values do at the use site |
|---|---|---|
| `0056C490` (→`0056D370`, the trade panel) | `ShopItemCursorOffsetX` | `eax = key`, halved and added into the cursor word at `[+0xC0]+0xFA` — the item-list cursor's X step (`0056C747`…`0056C769`) |
| `0056D940` (→`0056CA60`) | `ShopItemCursorOffsetX` | `key/2` negated then `ax − rowIndex·…` — the centered cursor X written into the row record (`0056D970`…`0056D997`) |
| `0057A4E0` P (leaf widget, `0057A480`) | `DefUnderBlackBandH`, `DeftopBlackBandH`, `ListHelpBlackBandH` | `movzx` byte loads, `cmovne` between top/under heights, packed into a `[rsp+0x24]`-family band descriptor — the leaf's three band heights (`0057A583`…`0057A5AD`) |
| `0056DD50` (→`0057C070`, the `0x8001` buy/sell switch) | `ListHelpBlackBandH`, `PartyBlackBandGradH`, `BlackBandAnimTime` | band rebuild on mode switch: heights → `ecx`/`edx`, anim → `r8d`, `002C9490` (`0056DE94`…`0056DEA1`) |
| `0057B400` (→`0057B890`, the menu list) | `mCommandMenuStrHeight` | `eax = key` → `[rsp+0x28]` then `002C9BF0` — the row height fed to the shared menu-list geometry call (`0057B453`) |
| `0057B800` (→`0027FB70`, inside `0057B890`'s install path) | `PartyBlackBandGradH`, `PartyBlackBandTime` | the party band's gradient → `edx`, anim ms → `ecx`, `r8d` = 1 → `002C99A0` — the shared party-band animation call (`0057B82D`, `0057B839`) |
| `003F3E40` (→`003F4060`, a shop child widget) | `PartyBlackBandGradH`, `BlackBandAnimTime` | gradient → `edx`, anim ms → `r8d` (`ecx`/`edx` zeroed at the other site) → `002C9060` — the shop child's band build (`003F3FCB`, `003F3EB4`) |

## What this screen does

`0057B890` is the shop's outer menu — the "Buy / Sell / …" list with the `Shop_8_c.tm2` banner — owning the cursor and forwarding input to its `+0x148` menu-list child. Its `0x8001` sub-command is the mode switch into the trade panel `0056D370`, which owns the quantity counter (`+0xDC` × unit price at `[+0xD0]+0x10`, `0056D45A`–`0056D46C`) and installs ~~the `0057A620`→`0057AC10` item list (buy mode) or the `0057A4E0` leaf (sell mode) depending on `+0xE4 & 0x3FC0`.~~ **Corrected 2026-09-29 (FABLE, GI-5):** after a commit, the `0057A4E0` leaf for a bazaar good (kind 11) or the `0057A620`→`0057AC10` item list after a purchase whose goods pass `003933D0`; buy versus sell is `+0xE4` bit 0. The item list renders each row through `0057AA00`/`0057B1A0` (name, stock via `003933B0`/`0030B4B0`, price via the `0056E880`→`0057D620` formatter) and the equipment state through the `00282DF0`/`00282EA0` character calls. Shop data comes from the `12-Items-Equipment-Shops-License` tables — `0030B4B0`/`0030B630`/`0030BAF0` are the same `shop_table` accessors that page documents.

## The `0056E140` widget, decoded (SWE2-FRONTIER, switch-families package)

The widget `0056DD50` installs is a 20-id message procedure (632 B; RVA table `0056E3B8`,
site `0056E15F`; unhandled ids share the `0056E3AB` return-0 tail):

| msg id | arm | work |
|---|---|---|
| 1 | `0056E16D` | init: `msg+8 → +0x192`; `0057B680(0)`; `002432B0(+0x50, ret, 1, self)`; copies the returned record's words `+4/+6/+8/+A` into `+0x98`–`+0x9E`; `00394700(self, 2)`; sets `+0x180 \| 0x4000000`, clears `+0x194 & ~6`, `+0x40 & ~0x80`, zeroes `+0x190`/`+0x198`/`+0xC0`/`+0x188` |
| 8, 9 | `0056E2B4` / `0056E2F6` | same call pair `002D45C0` + `002445C0` — two directions of one step |
| 10 | `0056E259` | `0056DED0` — directional-input helper |
| 12 | `0056E269` | `00293110`, `00244F00` (mark-delete), `0056E5D0` |
| 14 | `0056E212` | `002470D0` |
| 15 | `0056E322` | `0056DD00` gate, then `00247510(self+0x188, 0xF, (self+0x194)>>2 & 1)` (`0056E322`–`0056E355`) |
| 18 | `0056E374` | `00247510`, `003697F0` — deferred free |
| 19 | `0056E222` | `0056E5D0` |
| 20 | `0056E356` | `0056DD00` gate, then `002CFCF0`, `0027EE80` (`0056E356`–`0056E373`) |

ids 2–7, 11, 13, 16, 17 are unhandled. ~~The arm bodies' per-helper roles (`002D45C0`,
`002CFCF0`, `0027EE80`) are named by call site only — not read in this pass; registered as **GI-17**.~~
**GI-17 answered 2026-10-01 (OPUS, static: the three bodies read):**
- `002D45C0(widget, on)` (134 B) writes `on & 1` into bit 16 of the widget's `+0xE0`. Then, when the focused widget
  `00244820` returns is this widget or one of its `+0x10` ancestors, and every widget on that chain up to the root is live (`+0x40` bits 0 and 3) and of a
  kind whose signed `+0x7C` low nibble is not 0, 1 or 4 - it calls `003689E0(on)`. Arms 8 and 9 pair it with `002445C0`.
- `002CFCF0` (32 B) re-attaches the shared UI record `[0209AC30]`'s `+0x278` widget under the UI root `0208EA28`
  (`00246AD0`) when that widget exists, and otherwise does nothing.
- `0027EE80` (75 B) sets word `+0x44` of the `[0209AC30]` sub-widgets at `+0x2B8` and `+0x2C8` to `0x6E` (`002C9400` /
  `002C9890` -> `00247930`, only when the value changes, which also marks the parent dirty) and starts a 200 ms move of
  each to `(56, 4)` and `(32, 4)` (`002C9060` / `002C9490` record the change and convert 200 ms to frames; the four
  values are the `.data` dwords `01E0C3CC`, `01E0C3D0`, `01E0C3BC`, `01E0C3E8`, ~~which no instruction writes~~ the layout keys `DeftopBlackBandH`, `DefUnderBlackBandH`, `PartyBlackBandGradH` and `BlackBandAnimTime`, written through the slot pointers `001AF470` installs, e.g. `001AF470+0x214` `lea rax, [01E0C3D0]` *(corrected 2026-10-02, OPUS: `layout-key-slots.tsv`)*).

What the player sees for the bit, the two widgets and the `0x6E` id is not claimed.

## The `01E0C490` query-class dispatch — NOCALLER-INSTALLERS, 2026-09-14 (FRONTIER)

`00292B70` (the shop helper chain's dispatcher — `0057BEE0` reaches it on the window rebuild,
`00564430` on the item-helper path) routes a `{kind@0, param@4}` record through a 15-slot pointer
table at `01E0C490`: `movsxd rax, edi ; mov r10, [01E0C490 + rax*8] ; test r10,r10 ;
call r10` (`00292D08`–`00292D3B`). Outer kinds `0x1`–`0xE` index directly except three remaps:
kind 3 resolves `word[record+2]` through `0035D330` and the record's `+0x4C` into `edi` ∈
{0,1,2,3,4,5} (`00292C9A`–`00292D03` — `edi=2` at `00292CC7` behind the `002CCA00` predicate,
`edi=0` via the `mov edi, r14d` fallback at `00292CE9`); kind 6 becomes 7 behind a `002CCB00` predicate (`00292C79`–
`00292C98`); kind 0xA first range-checks the param's high word against `0x8060`–`0x81FF`
(`00292C2B`–`00292C4A`). Before the call it fetches the handler's record with `00295C20(edi)`
(`00292D21`) and passes `(record, arg2, &slot-array, &0x200-workbuf)`.

Every populated slot is one family: fetch the context through `002AC2E0`, then split the param
word's high 16 bits against `0xFFFF`. The no-caller members — slots 4/5 included (a raw E8/E9
scan finds **zero** call sites image-wide for `00293FE0`/`00293310`; they are lea-installed
only) — and the three 147-B twins at slots 9/10/12 bind as:

| idx | address | role | interior |
|---:|---|---|---|
| 1 | `00295900` | equipment-block query: `002AC2E0` context, then param high-word split | `00295933` |
| 2 | `00295390` | same shape — `002AC2E0`, high-word split | `002953C1` |
| 3 | `00294B50` | `002AC2E0` + `00254A10` gate + `002AC290` — the 2,104-B query body | `00294B7D` |
| 4 | `00293FE0` | `002AC2E0` + `00254A10` + `002AC290` — the 2,052-B twin | `0029400D` |
| 5 | `00293310` | `002AC2E0` + high-word split — the 2,501-B equip-block reader | `0029333D` |
| 6 | `00294860` | `002AC2E0` + high-word split (578 B) | `0029488F` |
| 7 | `002957C0` | `002AC2E0` + high-word split (315 B) | `002957F3` |
| 8 | `00293E10` | `002AC2E0` + high-word split (291 B) | `00293E43` |
| 9 | `00293F40` | the first 147-B twin — `002AC2E0` context fetch + `0035D330`/`0017D2E0`/`0016D6A0`, splits the param word against `0xFFFF` and writes into the out array | `00293F63` |
| 10 | `00294AB0` | same 147-B twin shape | `00294AD3` |
| 11, 13 | — | NULL — `test r10,r10 / je` skips | `00292D16` |
| 12 | `00295720` | same 147-B twin shape | `00295743` |
| 14 | `002956B0` | writes `byte[rdx+4]=1`, resolves a class-`0x1A` record via `0035D330`, stores its `+0x10` into `out` | `002956C2` |
| 0 | — | NULL | |

Slots 0, 11 and 13 are the `je`-guarded no-op paths; `00295C20` reads the adjacent record array
at `01E0C510`+ to produce the handler's `rcx` (`00295C45`–`00295C6D`). The five largest members are the menu-side equipment-block
readers the query-record census already counts (`the-encoded-id-space-and-the-query-record.md`
§"the equipment block is read as a block"); the dispatch is how they are reached — no caller
calls them directly.

## Not yet established

- ~~which `0xF`/`0x12` sub-command ids correspond to which parent notifications~~ — *closed 2026-09-30 by the owner read (SWE2-FRONTIER): both are decoded below, which answers the question.* **narrowed
  2026-09-15**: `0xF` is the `0056E140` child's own post (`00247510(self+0x188, 0xF, (+0x194)>>2 & 1)`
  from its id-15 arm, `0056E322`) — a pre-destroy flag report to `+0x188`. `0x12` on the menu list
  does `002470D0` + sets the child's `+0xE0 & 0x200000` list-mode bit — the enter-list-mode notify.
- ~~the exact `+0xE4` mode-field values beyond `0x1C0`/`0x2C0`~~ — **answered 2026-09-29 (FABLE, GI-5)**: a bitfield; `0x1C0`/`0x2C0` are the loot and bazaar kinds — §*GI-5 answered 2026-09-29* below
- ~~`0057A4E0`'s contents beyond "descriptor row"~~ — *closed 2026-09-30 by the owner read (SWE2-FRONTIER): read 2026-09-18 (FABLE) in the `0057A4E0` section above, a styled text element built at id 1.*

## GI-5 answered 2026-09-29 (FABLE) — the trade panel's `+0xE4` bitfield

*(FABLE, Claude Opus 5.5 — NATIVE/STATIC, bodies and tables read; control
[`gi5_shop_panel_e4.py`](../../_index/candidates/gi-0929-ui/gi5_shop_panel_e4.py), FAILS 0.)*

**`+0xE4` of the trade panel `0056D370` is a packed bitfield.** The published `0x1C0`/`0x2C0` are values of its bits
6–13, the **goods kind** of the shop tab the player is on: `0x1C0` = kind 7 (loot), `0x2C0` = kind 11 (bazaar). Buy
versus sell is bit 0.

| bits | meaning | written at |
|---|---|---|
| 0 | **sell** (1) / buy (0), the create record's `+4` bit 0 | `0056D71D`–`0056D736` |
| 1 | quantity window open (mirrors `+0xD8` bit 1) | `0056C833`–`0056C83E` |
| 2 | quantity can go up (`0056E700` returned 0) | `0056C7B8`, `0056C7C1`, `0056DA00`, `0056DA09` |
| 3 | quantity can go down (quantity ≠ 1) | `0056C7C8`, `0056DA10`, `0056DA22` |
| 4 | committed, waiting for id 2 to rebuild | set `0056D4FD`, cleared `0056D5EC` |
| 5 | committed, list refresh pending | set `0056D4FD`, cleared `0056C927` |
| 6–13 | **goods kind** = create record byte `+0` | `0056D69C`–`0056D712` |
| 14–21 | row-layout variant `00D235E8[kind]` (image-base-relative, `0056D6F8`) | `0056D712` |
| 22–29 | the selected quantity digit (0 ones, 1 tens) | `0056D9A8`, `0056D9BD`; cleared `0056C770` |

**Every writer.** An image-wide displacement sweep for `+0xE4` writes, whose control is `0056D370`'s own four writes,
finds **17 panel writes in five functions** — `0056D370` (4), `0056C490` (6), `0056C850` (1), `0056D940` (2),
`0056D9D0` (4) — each reached only with the panel in hand (`0056C490` from `0056D370`/`0056C850`; `0056D940`/`0056D9D0`
from the quantity input `0056CA60`). The other shop-region hits (`005641F0`, `00564650`, `00564C80`, `0056CA3A`) write
the panel's list control, which `0056C950` stores at the mode object's `+0xD8` (`0056C9E6`–`0056C9ED`).

**Every kind value.** The kind is `0056DC30(category)` of the current tab (32-entry map, `0056DCD4`/`0056DCA0`). Each
kind is named by the inventory list it counts — goods code `kind + 8` (sell) or `kind + 0x14` (buy), `0056E945`–`0056E956`;
code `8 + kind` indexes `00D23D00`, whose first word is the list `00252F40` opens (`0057D70F`–`0057D72D`; list names
from [the encoded-id page](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)):

| kind | `& 0x3FC0` | goods | categories | max quantity (`00D235F8`) | row variant | offered by |
|---:|---|---|---|---:|---:|---|
| 0 | `0x000` | weapons | 1–4 | 99 | 0 | Buy, Sell |
| 1 | `0x040` | shield / helm / chest | 5–8 | 99 | 0 | Buy, Sell |
| 2 | `0x080` | accessories | 9 | 99 | 0 | Buy, Sell |
| 3 | `0x0C0` | ammunition | 10, 27–30 | 99 | 0 | Buy, Sell |
| 4 | `0x100` | items | 11 | 99 | 0 | Buy, Sell |
| 5 | `0x140` | technicks | 15 | 1 | 1 | Buy |
| 6 | `0x180` | magicks | 16–21 | 1 | 1 | Buy |
| **7** | **`0x1C0`** | **loot** | 26 | 99 | 0 | Buy, Sell |
| 8 | `0x200` | the `0x5000` class (list 5) | 12, 31 | 1 | 2 | no shop verb |
| 9 | `0x240` | gambits | 13 | 1 | 1 | Buy |
| 10 | `0x280` | the `0x7000` class (list 7) | 14 | 1 | 1 | no shop verb |
| **11** | **`0x2C0`** | **bazaar goods** | 0 | 255 | 3 | Bazaar |

**Which verb sets which values.** The menu list's id-12 `0x8001` arm calls `0057C070(self, option)`, which hands key
`00D23920[option]` to `0056DD50` (`0057C0F0`–`0057C101`) — the only creator of the mode object (sole `lea` of `0056E140`
at `0056DD66`) that installs the panel through `0056C950`. Option 0 (key `0x5AF`, category set 32) offers kinds 0–7
and 9; option 1 (key `0x5A2`, set 19) offers kinds 0–4 and 7 and is the only key in the sell range
`0x597`–`0x59D` / `0x59F`–`0x5A2` (`0056DE3D`–`0056DE65`), so it alone sets bit 0; option 2 (key `0x5AE`, set 31)
offers kind 11. The prompts confirm bit 0: `0xC6B + 2 × bit0` reads "Select an item to buy." / "Select an item to
sell." (`0056C4C5`, `0056E632`).

**What the panel does per value.** On confirm with the window open (bit 1): total = unit price × `+0xDC`
(`0056D45A`–`0056D46C`); bit 0 set → `Shop_CommitSaleItemAndGil`, plus `00316A50(0xE, quantity)` for kind 7
(`0056D478`–`0056D498`); bit 0 clear → `Shop_CommitPurchaseItemAndGil`, plus the good's flag
(`BattleIdClassD_SetRuntimeFlagBit2`, `0056D4C0`) for kind 11, and `00316A50(0x13, id)` for every purchase; then
bits 4–5 are set. On id 2 with bit 4 set: kind 11 → `0057A480`; otherwise a purchase whose goods pass `003933D0` →
`0057A980` + `002CC4F0`; else `0056C850` (`0056D5C7`–`0056D660`). Quantity entry runs only for row variant 0 — kinds
0–4 and 7 (`0056C4CD`, `0056CAB6`); the technick, magick, gambit and bazaar tabs sell one at a time. *Inference, not
read here: the on-screen labels of options 0/1/2 (taken from what each option offers and the sell bit) and what the
counters `0xE`/`0x13` of `00316A50` count.*

## Falsification pass

**Pass 1 — 2026-09-14 (OPUS).** Attacked at parent `GN160` (`fa0db293…`), EXE `73461d08…`.
Instrument: `Tools/work/OPUS/falsify_shop_dialogs.py`. **Two claims attacked, both survived. No
correction.**

| claim | the killer | result |
|---|---|---|
| `0057B890` bounds `msg->id` to `0x13` at `0057B89D` through the table at `0057BCE4` | a different bound, compare address or table | **survived** — all three exact |
| it answers ids 1, 2, 8, 10, 12, 14, 15, 16, 18, 19, 20 at the published arms, with 3–7, 9, 11, 13, 17 defaulting to `0057BCD6` | any other id reaching a real arm, any arm not where the page puts it, or a different default | **survived** — **eleven ids, eleven exact arm addresses, and every listed default id really defaults** |

**Eleven id→arm pairs is the largest dispatch table checked in this round and it is exact in every
entry**, including the default set: the page lists 3–7, 9, 11, 13 and 17 as falling through, and all
nine do, to the address it names.

**Not attacked by this pass:** the arm interiors — the `0x8001` mode-switch chain through `0057C070`,
the sub-command semantics inside `0057BB1D`, and the per-row emitter bodies the status line already
marks as signature-classified only.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — CLIENT.** `FUN_0038ebe0`, owned by that layer, calls `00320D50` on this page. That caller is a 349-byte row-timing computation on the same two definition tables: it demands **bit 0 of the row's `byte[+0x12]`**, then divides a counter by 1,000 before indexing the `0x1C8`-byte records; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 37 edges measured).** The shop
screens draw through the render layer's widget machinery: `00579420`
(`Presentation.UI.Quest.ListScreenSelectionStateMachine`, 7 edges) and `002BAF80`/`002B7B80`
(`Presentation.UI.InputConsumerStateMachine`) drive `002470D0`/`00247510`/`00247870`/`00249580`/
`002526F0`/`002D3900`/`002D45C0`; the widget draw pass `00245E60`
(`Presentation.Widget.WidgetTreeRecursiveDrawPass`) calls `00246480`/`003985B0`; the nine-patch
backgrounds `002455A0`/`00245170`, icon draws `002BCB00`/`002B8EE0`, ShaderMaterial `002B0280`/
`00578450` and ScreenCapture `002D2DB0` reach the same helpers. The screens are rendered by these
bodies — the crossing is the draw path, not a second owner.

**Save_Load_Settings — CLIENT (SWE2-CONTRACT 2026-09-15, 24 edges).** The save/load controller
callbacks share this page's widget helpers: `SaveLoad_ControllerLifecycleHandler` (6 edges) calls
`00247510`/`00247870`/`002497E0`/`002CA150`/`003678F0`/`00394700`; `SaveWrite_OperationStateCallback`,
`SaveLoad_FullImageStorageCompletionCallback`, `SaveSlotScan_ControllerCallback`,
`SaveSlotProbe_StorageCompletionCallback`, `SaveStorageQueue_ControllerStateHandler`,
`SaveLoad_ControllerTransitionStateMachine`, `SaveSlotMetadata_BuildSubmissionDescriptor`,
`SaveImage_FinalizeHeaderAndChecksum` and `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` each
reach one or two of the same helpers. The save/load flow reuses the shop screen's widget layer —
the helpers are shared, not owned twice.

**Rewards_Progression_Economy — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 10 edges).** The shop reads and writes
Gil directly: `002CE7A0`/`002FEEB0`/`00310870`/`0056D370` call `GameState_GetGil` `00253690` (4
edges); `002FEEB0`/`00310870` call `GameState_SetGil` `00254EE0` (which itself reaches `00316A50`);
`00316A50`/`00469E80` are reached by `BattleUnit_ProcessDefeatRewardsAndLoot` and
`GameState_AddGilClampedAndNotify`. The Gil accessors are the crossing — a real economy
relationship, not fan-in.

**Script_VM_Native_Bridge — SERVICE (7 edges, all six callers read).** Six script verb handlers
reach five functions cited here, and every one of them has the same shape: pop the arguments off the
VM value stack, call the engine function, and in one case push the answer back.

`0034C170` pops one integer through `00267E10` `VMValueStack_PopInt32CoerceFloat32`, calls
`002FAE40`, and returns the result to the script through `00267F90` `VMValueStack_PushInt32` — it is
the only one of the six that answers the script rather than just acting. `0034C730` is two
instructions, `mov rcx, rdx / jmp 002E42D0`, handing the context straight through. `00351000` calls
`002E42D0` and then tail-jumps to `002EC5D0`. `00352250` pops one integer and tail-jumps to
`008632B0`.

Two are worth stating exactly. `0034E1F0` **takes no argument at all** — it calls `00313550` and
`00314D40` with a literal `1` before tail-jumping to `0037CA80`, so the verb is a fixed action, not
a parameterised one. And `0034B9A0` pops an integer and calls `003EABE0` **only when that value is
negative** (`0034B9B7 test eax, eax / jns`); a non-negative argument skips the call entirely.

The crossing is that the script layer calls these; nothing here is shared ownership. Read from the
shipping bytes 2026-09-14 (OPUS).

**Gameplay — CLIENT (14 edges, five neighbour bodies read).** *This replaces an earlier
`OPUS-MECHANICAL` registry row whose note said "pass-22 section names the crossing" when the section
did not, and which recorded three edges where `edges.tsv` has fourteen. The row was wrong on both
counts; the reading below is what is actually there.*

Six of the fourteen edges are one function: `00322C50` `BattleEncodedId_IsValidForClass`, reached by
`0030B180`, `0030B4B0`, `0030B630`, `00317930`, `0031A510` and `00323C60`. It takes `class - 1`,
**refuses anything above `0x1F`** — so thirty-two classes — and dispatches through a jump table of
image-relative offsets at `+0x203054`. Four more edges are the same family's decode entries:
`00309EC0` and `0030ADC0`, which are instruction-for-instruction identical at the top — `0xFFFF`
means "no id" and returns `-1`, and any id whose top nibble exceeds `0xE` is refused the same way.
`0031C5D0`, reached twice, repeats the thirty-two-class bound after clearing `[rcx+0x18]`. The last
edge is `003105D0` calling `00316CF0` `BattleTargetBuffer_ResetPreservingFlag0`, which saves bit 0
of the first byte, zeroes `0x208` bytes, and puts that one bit back.

So the crossing is that this page's equipment and licence functions ask the encoded-id layer whether
an id is valid for a class, and that layer answers from one bounded table. It is a client
relationship with a shared query family, not shared ownership of it. Read from the shipping bytes
2026-09-14 (OPUS).
- **ActorEntity - CLIENT and SERVICE (33 edges).** `002699D0`, `002B58B0`, `002E42D0`, `002ECEC0` (+3 more) are called by bodies filed to ActorEntity: `00233EA0`, BattleUnit_UpdateLifecycleAndCombatFrame (`00233F70`), `002348E0`, BattleUnit_FindByDefinitionSelector (`002367A0`) (+8 more); `002699D0`, `002B7B80`, BattleUnit_TeardownAndDespawn (`00300E40`), BattleUnit_CancelAndResetCurrentAction (`003105D0`) (+4 more) reach bodies filed to ActorEntity: `00233CF0`, BattleUnit_GetBySlotIndex (`00236820`), BattleUnit_GetSlotCount (`00236850`), BattleUnit_ApplyUnitDefinition (`0023A570`) (+9 more) - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT (16 edges).** BattleEncodedId_DispatchQueryMode0Value (`00309EC0`), BattleUnit_CancelAndResetCurrentAction (`003105D0`), BattleTargetBuffer_ResetPreservingFlag0 (`00316CF0`), BattleEncodedId_IsValidForClass (`00322C50`) are called by bodies filed to CombatAI: AiOrder_EvaluateAndResolveActionTarget (`003014C0`), AiOrder_EvaluateTargetSelector (`00301AD0`), BattleUnit_UpdateCombatFrame (`00308610`), AiOrder_SelectFinalTargetFromCandidates (`003087E0`) (+10 more) - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (17 edges).** `00197700`, `001986D0`, `00225570` are called by bodies filed to Input: `001E0A10`, `001E0E30`, `001E0E50`, `001E0F20`; `001E0A10`, `001E0E30`, `001E0E50`, `002B7B80` (+4 more) reach bodies filed to Input: `00197700`, `001986D0`, InputManager_GetSingleton (`00198790`), `001E0A10` (+5 more) - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - CLIENT and SERVICE (49 edges).** `0020CE00`, `0020CE60`, `00254E80`, `00282FA0` (+10 more) are called by bodies filed to PlatformOnlineAchievements: `003154B0`, `00315E90`, `003161A0`, `003162E0` (+9 more); GameState_SetGil (`00254EE0`), `00315E90`, `003161A0`, `00316760` (+4 more) reach bodies filed to PlatformOnlineAchievements: `0020CE00`, `0020CE60`, `00315420`, `00315E90` (+8 more) - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (10 edges).** `002B7B80`, `002BAF80`, `002CBD50`, `002CC5F0` (+4 more) reach bodies filed to Resource: `00249320`, `002493D0`, `00249580`, `0024A5A0` (+2 more) - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT and SERVICE (6 edges).** BattleUnit_CancelAndResetCurrentAction (`003105D0`), BattleEncodedId_IsValidForClass (`00322C50`) are called by bodies filed to Status_Periodic_Terminal: BattleUnit_ResetActionControlForStatusTransition (`00300140`), BattleUnit_RecoverFromTerminalStatusSetIfClear (`00301140`), BattleStats_ModifyStatusLayerStateAndProcessSideEffects (`0030E130`), BattleStats_RecomputeDerivedStateAndAutoStatuses (`0030FED0`) (+1 more); BattleStats_SetEquipmentSlotByMappedId (`0031A510`) reaches bodies filed to Status_Periodic_Terminal: BattleStats_RecomputeDerivedStateAndAutoStatuses (`0030FED0`) - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (1 edge).** `00314D40` is called by bodies filed to World: `00266D10` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (7 edges).** `0029FB50`, BattleEncodedId_DispatchQueryMode0Value (`00309EC0`) are called by bodies filed to WorldAreaField: `00576A50`, `0057FB00`; `002B7B80`, `002BAF80`, `003160C0`, `003161A0` (+1 more) reach bodies filed to WorldAreaField: FieldData_GetVariable0 (`00265270`), FieldData_GetActiveFieldRecordBit15 (`00313F60`), WorldTransition_GetActiveOrPendingFieldId (`003148F0`) - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (3 edges).** `AiOrder_EvaluateAndResolveActionTarget` (`003014C0`) reaches `BattleData_ResolveWeightedId` (`00308EC0`) and `RNG_SharedGameplayLCG_NextU32` (`00328370`); `AiOrder_SelectFinalTargetFromCandidates` (`003087E0`) also pulls the shared LCG - the AI-order bodies consume the documented RNG stream.

## SWE2-EC7-68 update (2026-09-19) - `00293110` mode-gated shop helper

`00293110` (93 B) is the gate the shop/license widget bodies run
before `00293170`: `ecx == 0 && edx == 0` tails it as
`00293170(0, 1, 0)`; otherwise it walks `[0209AC30] -> +0x2F8 ->
+0xC0 -> dword[+0x40] & 1` and tails `00293170(ecx, 0, flag)` with
the UI-mode bit as the third argument, a dead link producing
`00293170(ecx, 0, 0)`. Interior anchor `00293146` (the `& 1` test).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-shop-screens-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00282EE0` | 37 B | compares `ecx` with the low dword of the pointer `qword [0209AC30] + 0x408 + i*0xC0` for i = 0 to 8 (signed `cmp eax, 9` loop bound) and returns the first i that matches, or 0 when none matches | `00282EE7`, `00282EF0`, `00282EF6`, `00282EFD`, `00282F02` |
| `00292190` | 120 B | for the constants 0xA, 0x14, 0xE and 0x10 in that order calls `002F8040(constant)` and, only when that returns 0, `002491B0(rcx, constant)`; the 0x10 call to `002491B0` is a tail jump, and when `002F8040(0x10)` is non-zero the function returns that value | `0029219E`, `002921AD`, `002921B7`, `002921E9`, `002921FD` |
| `002A2620` | 39 B | returns 1 when qword `0209C4C8` is null; otherwise returns 0 when byte `+0xC0` of that object has bit 0 or bit 1 set (`test 3`) or when its byte `+0xF2` is greater than -1 as a signed byte (0x00-0x7F), and returns 1 when that byte is 0x80-0xFF | `002A2627`, `002A262C`, `002A2638`, `002A263F`, `002A2641` |
| `002CB850` | 84 B | loads qword `+0x2E0` of qword `0209AC30` and returns when it is null; otherwise, when `ecx` is 0 it sets bit `0x20000` of that object's dword `+0x168` and calls `00247870(qword +0xC0, 1)`, and when `ecx` is non-zero it clears that bit (AND `0xFFFDFFFF`) and calls `00247870(qword +0xC0, 0)`; both paths then tail-jump to `002CC2A0` | `002CB867`, `002CB86D`, `002CB87E`, `002CB891`, `002CB89A` |
| `002CCB00` | 15 B | returns 1 when `ecx` minus 0x4000 (added as `0xFFFFC000`) is 0x17 or less as an unsigned compare, that is `ecx` in 0x4000-0x4017, and 0 otherwise | `002CCB02`, `002CCB08`, `002CCB0B` |
| `002EC5D0` | 89 B | returns when `rcx` is null, when its qword `+0xC0` is null, or when the dword that qword points to is -1; otherwise, unless the word at that pointer is -1, it forms the record `qword [022C6F28] + word*0x740` (word sign-extended) and calls `00426E20` with it when the record is non-null and its dword `+0x284` is non-zero; on every path past the three returns it then stores 0 to dword `+0xEC` of `rcx` | `002EC5E9`, `002EC5FB`, `002EC60B`, `002EC614`, `002EC619` |
| `00351000` | 30 B | calls `002E42D0(rdx)` and then tail-jumps to `002EC5D0(rdx)`, passing its second argument as the first argument of both | `00351006`, `0035100C`, `00351019` |
| `003933D0` | 24 B | calls `002FABD0` and returns 1 when its result is 3 or less as an unsigned compare, else 0 | `003933D4`, `003933DB`, `003933DE` |
| `003F4060` | 337 B | switches on dword `[rdx]`: 1 copies qwords `+0`, `+8`, `+0x10` of qword `[rdx+8]` to `+0xC0`, `+0xC8`, `+0xE8` of `rcx`, stores byte `+0xA` of the first qword's target to byte `+0xE0` and widens that many words from the target's `+0x1C` into dwords from `+0xD0`, zeroes byte `+0xE1`, then calls `00246AD0(qword [0208EA28], rcx)` when `003F3E40(rcx)` is non-zero or `00244F00(rcx)` when it is 0; 2 returns unless `001EDEC0(dword +0xB4)` is non-zero, then when byte `+0xE1` is 4 also requires `002A2BF0()` non-zero, otherwise decrements word `+0xE2` and returns while it stays above 0 (signed), and finally calls `00244F00(rcx)` only when `003F3E40(rcx)` returns 0; 0x12 calls `00247510(qword +0xE8, 0x12, 0)` when that qword is non-null; every other value tail-jumps to `005C5230(rcx, rdx)`; the three handled values return 0 | `003F4173`, `003F41A4`, `003F40DA`, `003F40A2`, `003F4086` |
| `003F47E0` | 95 B | stores `rcx`, `rdx`, `r8`, `r9` in four consecutive stack qwords and builds a stack record of dword 0 at `+0`, a pointer to those four qwords at `+8` and qword 0 at `+0x10`, then calls `00244F50(0x130, 003F4840, &record)`; the stack cookie from `01F44830` is checked through `00808C40` before it returns | `003F47F6`, `003F4808`, `003F4824`, `003F4828`, `003F4835` |
| `0056DD00` | 67 B | returns 0 when `0057A960(rcx)` is non-zero; otherwise returns 1 when byte `+0x194` of `rcx` has bit `0x4` set, and else returns 1 when the result of `0057A440` is not 2 and 0 when it is 2 | `0056DD0E`, `0056DD1A`, `0056DD23`, `0056DD2E`, `0056DD38` |
| `0056DED0` | 617 B | when byte `+0xE4` of qword `+0xC0` (the object) has bit `0x2` set (`test 2`), calls `0056CA60(object)` then `002D3900(qword +0xD8)` and returns; otherwise takes signed fields L = bits 16-20 and I = bits 21-25 of dword `+0x180` (L < 2 goes to `002D3900`), calls `00563EC0(rcx)` when word `02F97368` AND `0xCA0` is exactly `0x400` or `0x80` with that bit set in word `02F9736C` and (I > 0 or word `02F9736A` AND `0x480` non-zero), and calls `00564300(rcx)` when it is exactly `0x800` or `0x20` with that bit in `02F9736C` and (I < L-1 or `02F9736A` AND `0x820` non-zero); if I is then unchanged it goes to `002D3900`, otherwise it writes words `+0xF0`/`+0xF2`/`+0xF4` of slot `rcx+I*8` (word `+8` of a 32-byte record of the object's qword `+0xC8`, 0xFFFF when that is null, and two sums of fields `+0xEC`-`+0xF4` of qword `+0xD8`), calls `005674B0(qword +0xC8 of rcx, rcx+0xF0+newI*8)`, stores `0056DC30(signed byte +0xF7 of the new slot)` to byte `+0x191`, and calls `0056C950(rcx, that byte, dword +0x194 AND 1)`, `0056E410(rcx)`, `0056E5D0(rcx, 1)` and `00249C60(0xA)` | `0056DF06`, `0056DF8F`, `0056DFC6`, `0056E031`, `0056E10A` |
| `0057B6A0` | 78 B | calls `002CA110`, then `00244DD0(qword [02CA9798])` only when that qword is non-null, then `00291D80(0, 0)`, `00293110(0, 0)` and `005112A0`, ORs 4 into dword `+0x150` of qword `02CA9790`, calls `00244DD0(qword [02CA9790])` and returns 0xC | `0057B6B5`, `0057B6BE`, `0057B6D8`, `0057B6DF`, `0057B6E4` |

## Homed bodies: functions reached only indirectly whose callees this page cites (OPUS, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted locally and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-shop-screens-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002947F0` | 106 B | stores byte 1 at `rdx+4`; calls `0035D330(0x12, the fifth (stack) argument)` and stores that record's qword `+0x10` at `[r8]`; calls `002AC2E0()` (with `rdx` still holding that qword) and passes its result as the third argument of `0017D2E0(r9, rcx, result)`; when `0017D2E0` returns `0x200` or more (unsigned) it calls `0016D6A0(0x20000)`, otherwise skips it; returns 1 on both paths | `00294802`, `0029481E`, `00294821`, `0029482F`, `00294839` |
| `002CCA40` | 190 B | calls `00252FA0(4)` and returns 0 when that count is not greater than 0 (signed); otherwise calls `00252F40(4)`, passes its dword `+4` to `0020E600` and walks the array `0020E600` returns, one word per step, for as many steps as `00252FA0` counted, skipping `0xffff`: for each id it calls `0035D330(6, id << 0x10)` and, when that record's dword `+0x38` equals `ecx`, returns 1 if the id equals `edx` or the record's dword `+0x20` is greater than 0 (signed); returns 0 when the loop ends without a match | `002CCA5E`, `002CCA85`, `002CCAA4`, `002CCABC`, `002CCAC7` |
| `00342F50` | 38 B | calls `0037CB80` with the incoming registers unchanged and returns 0 when it returns 0; otherwise calls `00314D40(1)` and returns 1 | `00342F54`, `00342F5B`, `00342F67`, `00342F6C` |
| `003453D0` | 45 B | returns 0 when word `[r8]` is 0; otherwise calls `0035A0A0` with the incoming registers unchanged, returns 0 when it returns non-zero, and when it returns 0 calls `00314D40(1)` and returns 1 | `003453D4`, `003453DB`, `003453E2`, `003453E7` |
| `00346020` | 55 B | returns 0 when word `[r8]` is -1 or 0; otherwise calls `0035A0A0` with the incoming registers unchanged, returns 0 when it returns 0, and when it returns non-zero calls `00314D40(1)` and returns 1 | `00346028`, `00346031`, `0034603A`, `00346041` |
| `003491B0` | 43 B | calls `0035A220(dword [r8])`; returns 0 when it returns 0, otherwise calls `00314D40(1)` and returns 1 | `003491B4`, `003491B7`, `003491BE`, `003491C5` |
| `00349A30` | 38 B | calls `0030BAD0` with the incoming registers unchanged; returns 0 when it returns non-zero, and when it returns 0 calls `00314D40(1)` and returns 1 | `00349A34`, `00349A3B`, `00349A3D`, `00349A40` |
| `00353720` | 43 B | calls `002E2550(dword [r8])`; returns 0 when it returns 0, otherwise calls `00314D40(1)` and returns 1 | `00353724`, `00353727`, `0035372E`, `00353735` |
| `00356050` | 40 B | calls `0035B7A0` with the incoming registers unchanged; returns 0 when it returns non-zero, and when it returns 0 calls `00314D40(1)` and returns 1 | `00356054`, `0035605B`, `0035605D`, `00356069` |
| `00357300` | 43 B | calls `0035B740` with the incoming registers unchanged; when its result minus 1 is above 2 (unsigned, so the result is not 1, 2 or 3) returns 0, otherwise calls `00314D40(1)` and returns 1 | `00357304`, `00357309`, `0035730E`, `00357315` |
| `003C95C0` | 630 B | dispatches on dword `[rdx]`: 1 calls `002432B0(rcx+0x50, qword +0x10 of qword 0209AC30, 4, rcx)`, copies the result's words `+4`..`+0xa` to `+0x98`..`+0x9e` when `rcx` is non-null, calls `00247930(rcx, 0x64)` and `00394700(rcx, 3)` and stores word 7 at `+0xc0` and byte 0 at `+0xc2`; 2 acts only when `001EDEC0(dword +0xb4)` and byte `+0xc2` are non-zero: it decrements byte `+0xc2` and, when that reaches 0, reloads bytes `+0xc1`/`+0xc2` from byte tables at image base + `0xbf1720`/`0xbf1728` indexed by the old `+0xc1`, and only for a new `+0xc1` of 3 or 4 sets byte `+0xc3` to 1 or 0 and writes byte `+0xc0` plus 7 (or plus 0) as word `+0xa`, and byte `+7` of that 8-byte entry of its qword `+0x20` as byte `+0x39`, of the object at `[[rcx+0x60]]`; 3 writes words `+0x58`/`+0x5a` of qword `[rcx+0x38]` by byte `+0xc1` (0: 0, 0; 1: ((3 - c2) << 7) / 3, `0xff`; 2: `0x80`, (c2 << 7) / 10 + `0x7f`; 5: `0x80`, ((3 - c2) << 7) / 3 + `0x7f`; 6: (c2 << 7) / 5, `0xff`; else `0x80`, `0x80`; c2 = byte `+0xc2`, low bytes); 0xe stores word `0xa02` at `+0xc1`; 0xf stores word `0x507` at `+0xc0` and byte 3 at `+0xc2`; all these return 0, and any other value tail-jumps to `005C5230(rcx)` | `003C974F`, `003C9819`, `003C96EC`, `003C9611`, `003C95F4` |
| `003FCFE0` | 494 B | takes `D` = qword `+8` of `[rdx+0x10]` and `s` = `002DD7E0(0)`; when qword `rcx+0xe0` is null it calls `00243580(rdx, 0, byte rcx+0x180)`, sets bit `0x1` of `D` dword `+8`, calls `002B4090(0x80, 02B5F220, 002F9860(0x867), qword +0x18 of qword [rcx+0x60] slot byte rcx+0x180)` and stores `s`, `02B5F220`, `0020E620(0)`, word `[D]+4` minus `0x14` and word `[D]+6` at `D` `+0x24/+0x18/+0x20/+0xc/+0xe`; otherwise, with `E` = `[rcx+0xe0]` + `r9d`*0x20, it calls `0027F030(0031C4C0(00282EA0(signed word +0xde0 of qword 0209AC30)), word E+8, byte E+0xb, signed byte rcx+0x17e, 0)`, clears bit `0x1` of dword `+8` of `[[rdx+0x10]]` when byte `E+0xa` is `0xff`, else sets it and writes that byte to its word `+0xa` and byte `+7` of that 8-byte entry of its qword `+0x20` to byte `+0x39`, stores qword `[E]`, `0020E620(0)`, words `[D]+4/+6` and `002DD7E0(2 if 0027F030 was non-zero, else 0)` at `D` `+0x18/+0x20/+0xc/+0xe/+0x24`, and calls `0029FF60(qword +0x18 of [rdx+0x10], 0, 0, word E+0xe minus signed word E+0xc, 0, 0)`, `0029FF60(qword +0x10 of [rdx+0x10], 0, 0, word E+0xe, 0, 0)` and `003FCAD0(rdx, E, 5, 0xa)`; returns 1 on both paths | `003FD016`, `003FD056`, `003FD0AC`, `003FD0E7`, `003FD1AC` |
| `003FD1D0` | 228 B | dispatches on dword `[rdx]`: 1 calls `002432B0(rcx+0x50, qword +0x40 of qword 0209AC30, 0xb, rcx)`, copies the result's words `+4/+6/+8/+0xa` to `+0x98/+0x9a/+0x9c/+0x9e` when `rcx` is non-null, stores qword `+0x18` of the object at qword `+0x20` of `[rcx+0x60]` at qword `+0xc0` and `003FCFE0` at qword `+0x120` of the object that qword points to, then calls `00254A10` and, only when it returns 0, `0029FB50(qword +0x30 of [rcx+0x60])`, and returns 0; 0xc tail-jumps through the function pointer at `[[rcx+0x10]]` with `rcx` = `[rcx+0x10]`, or returns 0 when `rcx`, that qword or the pointer is null; 0x12 returns 0; any other value tail-jumps to `005C5230(rcx)` | `003FD1E8`, `003FD216`, `003FD28F`, `003FD29D`, `003FD2A7` |
| `003FDDE0` | 508 B | takes `D` = qword `+8` of `[rdx+0x10]` and `s` = `002DD7E0(0)`; when qword `rcx+0xe0` is null it calls `00243580(rdx, 0, byte rcx+0x180)`, sets bit `0x1` of `D` dword `+8`, calls `002B4090(0x80, 02B5F220, 002F9860(0x867), qword +0x18 of qword [rcx+0x60] slot byte rcx+0x180)` and stores `s`, `02B5F220`, `0020E620(0)`, word `[D]+4` minus `0x14` and word `[D]+6` at `D` `+0x24/+0x18/+0x20/+0xc/+0xe`; otherwise, with `E` = `[rcx+0xe0]` + `r9d`*0x20, it calls `0027F030(0031C4C0(00282EA0(signed word +0xde0 of qword 0209AC30)), word E+8, byte E+0xb, signed byte rcx+0x17e, 0)`, clears bit `0x1` of `D` dword `+8` when byte `E+0xa` is `0xff`, else sets it and writes that byte to word `+0xa` and byte `+7` of that 8-byte entry of qword `+0x20` to byte `+0x39` of `[[rdx+0x10]]`, stores qword `[E]`, `0020E620(0)`, words `[D]+4/+6` and `002DD7E0(2 if 0027F030 was non-zero, else 0)` at `D` `+0x18/+0x20/+0xc/+0xe/+0x24`, and calls `0029FF60(qword +0x18 of [rdx+0x10], 0, 0, word E+0xe minus signed word E+0xc, 0, 0)`, `0029FF60(qword +0x10 of [rdx+0x10], 0, 0, word E+0xe, 0, 0)` and `003FCAD0(rdx, E, 5, 0xa)`; returns 1 on both paths | `003FDE16`, `003FDE57`, `003FDEBA`, `003FDEF0`, `003FDFB5` |
| `003FF1F0` | 367 B | with `B` = qword `+0x10` of `[rdx+0x10]`, stores qword `+0x10` of 0x20-byte entry `r9d` of qword `[rcx+0xc8]` at `B+0x18` and `0020E620(0)` at dword `B+0x20`, and calls `0029FB50(B)`; from the 0x10-byte record at qword `0209AC30` + (`r9d` + 0x6a)*0x20 it keeps word `+8` as `w`, qword `+0` as `p` and byte `+0xa` as `k`, except that when dword `[rcx+0x178]` is `0x402` and word `r9d` of `02B5F210` differs from `w`, `w` becomes that word and `p`, `k` become `002F9860(0x3ea)`, `0xff` when it is `0xffff`, else `002B58B0(qword +0x18 of R, 0)` and byte `R+0x2c` for `R` = `0035D330(1, w << 0x10)`; `D` = qword `+8` of `[rdx+0x10]` gets dword `+0x24` = `002DD7E0(5 if replaced, else 0)`, overwritten by `002DD7E0(4)` when `k` is `0xff`, qword `+0x18` = `p` and dword `+0x20` = `0020E620(0)`; on `[[rdx+0x10]]` it clears bit `0x1` of dword `+8` when `w` is `0xffff`, else writes `k` to word `+0xa` and byte `+7` of 8-byte entry `k` of its qword `+0x20` to byte `+0x39`; returns 1 | `003FF255`, `003FF25A`, `003FF2A1`, `003FF2FA`, `003FF33B` |
| `0053EEA0` | 273 B | dispatches on dword `[rdx]`: 1 stores `rcx` at qword `02CA8A78`, calls `0024A680(qword 02CA8A88, 1)` and zeroes `02CA8A88` when that qword is non-null, calls `002F83E0(0x19)` and `002F83E0(0x1a)` each only when `002F8040` of the same value is non-zero, calls `00365570` with 7 through `0xc`, then `0016D6A0(r)` and `00249410(r)` for `r` = `00249580(rcx)`, and `00247950(rcx, 0)`; 2 returns at once when dword `rcx+0xc0` is 0, else zeroes qword `02CA8A78` and calls `00245020` with `rcx` unchanged; 0x10 calls `0016D6A0` with `rcx` unchanged and stores dword 1 at `+0xc0`; these return 0, and any other value tail-jumps to `005C5230(rcx)` | `0053EF1E`, `0053EF4C`, `0053EF73`, `0053EEFC`, `0053EED8` |
| `0057F8C0` | 357 B | takes `k` = byte `[rcx + r9d + 0xef]`; when bit `0x1` of byte `rcx+0xe0` is clear it calls `003BB3E0(k)` and, when that record's dword `+0` is 2, calls `0057FB00(rdx, r8, qword rcx+0x1c0 + k*0xa0)`; otherwise (bit set, using a local dword pair 5, 1 as the record, or record dword not 2) it calls `00393240(qword +0xb0 of [rdx+0x10], 0 when byte rcx+0xea is 0 and the record's dword +4 is non-zero, else 1)` and `0057FA30(rdx, r8, record)`; then when byte `rcx+0xea` is 1 and `k` is 0 it clears bit `0x1` of dword `+8` in the six objects of `[rdx+0x10]` indexed by the dword table at `01F2CD10`, sets it in the object at qword `+0xd0` of `[rdx+0x10]` and returns 1; else it calls `00393160(rdx, 4, 3, 9, m)` and `00393160(rdx, 1, 3, 9, m)` with `m` = `k` capped at `0xc7` (unsigned) and returns 1 | `0057F8FB`, `0057F92B`, `0057F957`, `0057F9B2`, `0057F9E9` |
