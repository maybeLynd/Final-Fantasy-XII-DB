---
id: ui-shop-screens
title: The shop screens — the menu list, the trade panel, and the item list
status: "PARTIAL — GI-17 registered 2026-10-01 (SWE2-FRONTIER, on SWE2-AUDIT-SEM's REJECT of c97af7156, record dd-restatus-gi-0930): the id-20 arm helpers `002D45C0`/`002CFCF0`/`0027EE80` are live. GI-5 answered 2026-09-29 (FABLE), review (FABLE-REQ-AUDITSEM-REVIEW-GI-UI, ACCEPT, d998217e2). Was PARTIAL on: +0xE4 mode values beyond 0x1C0/0x2C0 are not established; 0057A4E0's contents read 2026-09-18 (a styled text element torn down at shop state 3)"
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

**Status:** PARTIAL — the five widget procedures, the installer chain, both dispatch tables, and every listed screen-region member are cited below with interior citations (2026-09-15); the 157 shared listed subtree members are cited as engine-helper families.

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

ids 2–7, 11, 13, 16, 17 are unhandled. The arm bodies' per-helper roles (`002D45C0`,
`002CFCF0`, `0027EE80`) are named by call site only — not read in this pass; registered as **GI-17**.

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
