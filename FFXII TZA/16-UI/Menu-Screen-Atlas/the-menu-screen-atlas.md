---
system: The menu screen atlas — which screen each menu widget procedure in 00550000-00580000 belongs to, and the evidence
category: 16-UI
status: DOCUMENTED — an atlas (which screen each procedure belongs to), not a reading of what each does; UQ-159 answered 2026-09-17 (the fifteen leaf panes and the launcher read); UQ-161 answered 2026-09-17; UQ-160 SUPERSEDED 2026-09-26 under FRONTIER's class-1 ruling (population coverage: the 114 unlabelled procedures outside the menu range stay unread, carried by this page's census and the register row). Re-statused 2026-09-29 (FABLE) under _index/candidates/status-currency-ruling-fable
owner_layer: CodeDomain:UI (menu screens)
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: each of the 80 widget procedures of the handler census in 0x00550000-0x00580000 is walked to its callee subtree
    (raw E8/E9 index, depth <= 3, stopping at other widget procedures and at functions with more than 12 callers); the
    subtree is labelled by the layout-key readers it contains, the files it requests by constant and its installer's name
    (members/ui_atlas.py)
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: falsification-pass-GN161
  crossref_clean: false
  reopened_count: 0
---

# The menu screen atlas

> **Most of the menu code between `00550000` and `00580000` can now be assigned to a screen without reading it.** Three
> independent kinds of evidence each name a screen:
> - the layout keys a function reads (`LicenseBoard…`, `WorldMap…`, `Gambit…`, `ShopItem…`), from the
>   [key readers](../Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md);
> - the files it requests by constant (`lic_*.tm2`, `w_*.tm2`, `menuhandbook_order.bin`, `menuquest.dat`), from the
>   [request census](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) §13;
> - its installer's name (the save / load controller).
>
> The 80 widget procedures of the [handler census](../Widget-Object-Model/widget-message-handlers.tsv) in the range own
> **1,065 frontier functions** in their subtrees. **913** of those sit under a labelled procedure (v2 rules, §2).

**PARTIAL.** This is an atlas, not a reading. A label names the screen a procedure belongs to, not what the procedure does.

## 1. What the player sees

The main-menu screens: the license board, the world map, gambits, shops, the handbook, the quest list, item sorting, the
confirm window and save / load.

## 2. Method

1. **Procedures.** Every handler-census procedure in `00550000`–`00580000` (74).
2. **Subtrees.** Callees from the raw call index to depth 3. The walk stops at other widget procedures, so a child screen is
   not folded into its parent, and at functions with more than 12 callers, so shared helpers are not claimed.
3. **Evidence.** The layout-key families read in the subtree. Shared families (`FontBase…`, `BlackBand…`, `PartyBlack…`)
   are excluded. Also the files requested by constant, the menu effect registry calls (`fx-reset` / `-spawn` / `-remove` /
   `-set`, [the registry](../../17-Presentation-Rendering/Effect-File-Formats/the-menu-effect-registry.md)), and the
   installer (the function whose `lea` names the procedure).
4. **Labels.** A procedure is labelled when its own subtree carries the evidence. Several matches are joined with `+`, and
   three or more read "several screens". A procedure with no evidence of its own is marked **child** when it is installed by
   a labelled procedure or one of that procedure's direct callees — a structural fact about who creates it, not a claim
   about what it shows. Excluded as evidence: the fade-band keys (`…BlackBandH`, read by the shared fades). Excluded as
   children: the ICF return-0 stub `005C5230` and its thunk `0017CDE0`, which many procedures install as a null procedure.

**Controls.** The world map row reproduces the independently read [map screens](../Map-Screens/the-map-screens-and-their-shared-map-data.md)
(`00552250` / `005528C0` / `00553AE0`). The save / load rows reproduce the named controller functions.

**Screens read so far.** [The quest list](../Quest-List/the-quest-list-screen.md): `005771F0` plus its three
`00575870` pane children — full message protocol, member roles, load/teardown.
[The license board](../License-Board-View/the-license-board-screen-widgets.md): the three-layer tree
`00561390` → `0055CD40` (grid view) / `00558FB0` (tile panel), the `00557DB0` cursor handler, all protocols
decoded.
[The gambit screens](../Gambit-Screens/the-gambit-screens.md): `0056B4D0` (list, parent) → `005691E0` (editor,
child on `+0xC8`, answers `0x121`), the `00566C10` icon widget and `0056C170` leaf slot; bank-commit on close
through `003282C0`.
[The shop screens](../Shop-Screens/the-shop-screens.md): `0057B890` (menu list, root) and `0056D370` (trade
panel with the quantity×price counter) → `0057A620` → `0057AC10` (item list) / `0057A4E0` (leaf).
[The handbook](../Handbook/the-handbook-screen.md): `00574E80` (back panel) → `0056EF60` → `00572E10` (viewer,
`menuhandbook_order.bin`) → `00572460`/`00572600` page children.
[The shared dialogs](../Shared-Dialogs/the-shared-dialog-widgets.md): `0056F810` menu list, `0057C480` confirm,
`00556F90` message window, `00566680` item-sort bar — the reusable leaf layer.
[The save/load widgets](../../19-Save-Load-Settings/the-save-load-screen-widgets.md): `0057FE80` slot screen +
the `SaveLoad_*`/`SaveWrite_*` controller panes.
[The unlabelled procedures](../Unlabelled-Panes/the-unlabelled-procedures.md): all 25 sorted by installer —
license launcher `00560910`, handbook content pages `00571A50`/`005742D0`/`00579AF0` + text pane `005701B0`,
item/equip `005789D0`/`00579420`, and the leaf panes of documented screens.

**Limits.** A subtree can contain a helper shared with another screen when that helper has at most 12 callers. Subtree
frontier counts overlap between procedures, so the page's unique figure is the 1,065 / 913 above. 25 procedures carry no evidence yet.

## 3. The atlas (00550000–00580000)
*(Regenerated 2026-09-13 with the rules in §2 as corrected: v1's child rule counted any installer inside a labelled subtree
and moved four procedures — `00556F90`, `00567200`, `0056F810`, `00574AD0` — plus `0057F7D0` into a screen on that basis alone.)*

#### Confirm window + message window

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `0057C480` | 38 / 30 | evidence | `0057C380` | 1,2,4,10,12,18,19 | `ConfirmCaption…`, `ConfirmWindow…`, `GeneralFrame…`, `MessageLine…`, `NobuMessage…` | — | — |

#### Gambits

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `00566C10` | 3 / 3 | evidence | `00567200`, `0056C170` | 1,2,3,4 | `GambitIcon…` | — | — |

#### Gambits + action list

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `005691E0` | 120 / 111 | evidence | `00568B30` | 1,2,5,8,9,10,12,16,17,18,19,20,22,26,289 | `ActionList…`, `GambitAction…`, `GambitTarget…`, `GambitTutorial…` | — | — |

#### Gambits + message window

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `0056B4D0` | 56 / 53 | evidence | `0056B350` | 1,2,8,9,10,12,15,18,19 | `GambitTutorial…`, `General…`, `MessageLine…`, `NobuMessage…` | — | — |
| `0056C170` | 1 / 1 | child of a gambits + message window procedure | `0056ADA0` | 1,18 | — | — | — |

#### Handbook

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `0056EA40` | 4 / 3 | child of a handbook procedure | `00574E80` | 1,3,18,19 | — | — | — |
| `0056EF60` | 15 / 14 | child of a handbook procedure | `00574E80` | 1,12,16,18 | — | — | — |
| `0056F410` | 8 / 6 | child of a handbook procedure | `0056F3C0`, `00574E00` | — | — | — | — |
| `0056F550` | 1 / 1 | child of a handbook procedure | `00574D00` | 1,18 | — | — | — |
| `00570890` | 1 / 1 | child of a handbook procedure | `00574E80` | 1,18 | — | — | — |
| `00572460` | 1 / 1 | child of a handbook procedure | `00572E10` | 1,3,14,15,18 | — | — | — |
| `00572600` | 4 / 3 | child of a handbook procedure | `00572E10` | 1,10,14,15,18 | `General…` | — | — |
| `00572E10` | 75 / 72 | evidence | `0056EE10` | 1,2,10,12,14,15,16,18,19 | — | `menuhandbook_order.bin` | fx-remove,fx-reset,fx-set,fx-spawn |
| `00574E80` | 47 / 38 | evidence | `00574CB0`, `00575580` | 1,2,12,14,16,18 | — | `HandBack2_c.tm2` | — |

#### Item sort + confirm window

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `00566680` | 27 / 25 | evidence | `005665B0` | 1,2,12,15,18 | `ConfirmWindow…`, `ItemSort…` | — | — |

#### License board

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `005565E0` | 16 / 15 | evidence | `005572B0` | 1,4,18,25 | `LicenseBoard…` | — | — |
| `00556DB0` | 1 / 1 | child of a license board procedure | `00556D20` | 1,18 | — | — | — |
| `00557760` | 9 / 8 | child of a license board procedure | `00557370` | 1,4,18 | — | — | — |
| `00557DB0` | 55 / 50 | evidence | `00557AE0` | 10 | `LicenseBoard…` | — | fx-remove,fx-spawn |
| `00558CE0` | 7 / 6 | child of a license board procedure | `00558C40` | 1,2,18 | — | — | — |
| `00558FB0` | 37 / 37 | evidence | `00558F20` | 1,2,15,16,18,20 | — | `Maru_c.tm2`, `Maru_c_2.tm2`, `lic_B_4_c.tm2`, `lic_B_8_c.tm2` | fx-reset |
| `0055A340` | 17 / 16 | evidence | `00557430` | 1,2,4,18,25 | `LicenseBoard…` | — | — |

#### License board + message window

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `005569F0` | 50 / 37 | evidence | `005571F0` | 1,2,4,18 | `LicenseBoard…`, `MessageLine…`, `NobuMessage…` | — | — |

#### License board + world map

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `0055CD40` | 141 / 127 | child of a license board + world map procedure | `0055C690` | 1,2,4,8,9,10,12,15,18,19,20,23,285 | `General…`, `Na…` | — | fx-remove,fx-spawn |
| `00561390` | 38 / 38 | evidence | `00561300` | 1,15,16,18,20 | — | `Lic_Bk.tm2`, `cm2_win_c.tm2`, `lic_8_c.tm2`, `lic_8_c2.tm2`, `lic_8_c3.tm2`, `license_chip.bin`, `meshdata.mg` | fx-reset |

#### Menu list

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `0056F810` | 26 / 20 | evidence | `00574D00` | 1,10,12,14,15,18 | `CommandMenu…`, `MenuList…` | — | — |

#### Message window

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `00556F90` | 47 / 36 | evidence | `00556EC0` | 1,2,18 | `MessageLine…`, `NobuMessage…` | — | — |

#### Quest list

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `00575870` | 23 / 17 | child of a quest list procedure | `00575810` | 1,2,16,18 | — | — | — |
| `005771F0` | 10 / 9 | evidence | `00577100` | 1,2,12,14,16,18 | — | `menuquest.dat` | — |

#### Save / load UI (installer name)

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `0057E4D0` | 19 / 15 | evidence | SaveWrite_OpenOperationController | 1,2,4,12 | — | — | — |
| `0057E610` | 1 / 1 | child of a save / load UI (installer name) procedure | `0057EDB0` | — | — | — | — |
| `0057E8D0` | 1 / 1 | evidence | SaveLoad_ControllerLifecycleHandler | 1,18 | — | — | — |
| `0057EB30` | 1 / 1 | evidence | SaveLoad_ControllerLifecycleHandler | 1,18 | — | — | — |
| `0057EDB0` | 2 / 2 | evidence | SaveLoad_HandleStorageStatusResultAndAdvanceController | 1,15,18 | — | — | — |
| `0057F360` | 16 / 16 | evidence | SaveLoad_ControllerLifecycleHandler | 1,2,12,15,18 | — | — | — |
| `0057FE80` | 32 / 31 | evidence | SaveLoad_HandleStorageStatusResultAndAdvanceController | 1,2,10,12,14,15,18 | — | — | — |

#### Shop

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `0056D370` | 57 / 49 | evidence | `0056C950` | 1,2,12,18 | `ShopItem…` | — | — |
| `0057A4E0` | 10 / 10 | child of a shop procedure | `0057A480` | 1,2 | — | — | — |
| `0057A620` | 26 / 26 | child of a shop procedure | `0057A980` | 1,12,18 | — | — | — |
| `0057AC10` | 75 / 67 | evidence | `0057A620` | 1,2,3,10,12,14,15,18 | `ShopItem…` | — | — |

#### Shop + menu list

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `0057B890` | 84 / 78 | evidence | `0057B800` | 1,2,8,10,12,14,15,16,18,19,20 | `CommandMenu…`, `MenuList…` | `Shop_8_c.tm2` | — |

#### World map

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `00551E00` | 6 / 6 | child of a world map procedure | `005528C0` | 1,24 | — | — | — |
| `00551F00` | 15 / 15 | child of a world map procedure | `005528C0` | 1,14,24 | — | — | — |
| `005528C0` | 98 / 96 | evidence | `00552250` | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42 | `WorldMap…` | — | — |
| `00553AE0` | 1 / 1 | evidence | `005528C0` | 1,4 | `MapName…`, `RegionText…` | — | — |
| `005542D0` | 27 / 27 | child of a world map procedure | `005528C0` | 1,2,10,12,14,15 | — | — | — |
| `0055A8A0` | 16 / 16 | evidence | `0055A810` | 1,4,18 | `WorldMap…` | — | — |

#### World map + help message

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `00552250` | 64 / 61 | evidence | `00550400` | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41 | `HelpMessage…`, `WorldMap…` | — | — |
| `00555330` | 1 / 1 | child of a world map + help message procedure | `00552250` | 1,4,24 | — | — | — |

#### Unlabelled

| procedure | subtree / frontier | label | installed by | message ids | layout-key families | constant files | effect registry |
|---|---:|---|---|---|---|---|---|
| `00558BB0` | 3 / 3 | — | `00560910` | 1,2 | — | — | — |
| `005595E0` | 2 / 2 | — | `00561E90` | 1,18 | — | — | — |
| `005599D0` | 15 / 13 | — | `00559860` | 1,2,4,18,19,20 | `General…` | — | — |
| `00560910` | 41 / 36 | — | `005601B0` | 1,2,8,9,10,12,14,16,18,19,20 | — | — | — |
| `005618E0` | 6 / 5 | — | `00561830` | 1,2,18 | — | — | — |
| `00566A70` | 2 / 2 | — | `00567200` | 1,2 | — | — | — |
| `00567200` | 1 / 1 | — | `00564010`, `00567190` | 1,18 | — | — | — |
| `005677A0` | 2 / 2 | — | `00567770` | 1,2,14,18 | — | — | — |
| `0056C060` | 2 / 2 | — | `0056C170` | 1,2 | — | — | — |
| `0056FCB0` | 2 / 2 | — | `005742D0` | — | — | — | — |
| `0056FD30` | 1 / 1 | — | `0056FEF0` | 1,3 | — | — | — |
| `005701B0` | 47 / 41 | — | `0056EC10` | 1,10,12,14,15,16,18,19 | — | — | — |
| `00570460` | 1 / 1 | — | `0056FEF0` | — | — | — | — |
| `00570530` | 3 / 3 | — | `0056EF60` | — | — | — | — |
| `00570630` | 9 / 8 | — | `00570080` | 1,3 | — | — | — |
| `00571A50` | 47 / 41 | — | `00570BF0` | 1,2,10,12,14,15,18,20 | — | — | — |
| `00573B40` | 1 / 1 | — | `00574BA0` | — | — | — | — |
| `005742D0` | 35 / 30 | — | `00570080` | 1,3,10,12,14,15,18 | — | — | — |
| `00574AD0` | 1 / 1 | — | `00574A00` | — | — | — | — |
| `00577F90` | 2 / 2 | — | `00577F00` | 1,18,19 | — | — | — |
| `00578450` | 5 / 5 | — | `005781A0` | 1,10,12,14 | — | — | — |
| `005789D0` | 42 / 40 | — | `00578920` | 1,10,12,14,15,16,18 | `Na…` | — | — |
| `00579420` | 27 / 25 | — | `00579130` | 1,2,10,12,14,15,18,19,20 | — | — | — |
| `00579AF0` | 33 / 33 | — | `00579990`, `00579A40` | 1,2,16,18 | — | — | — |
| `0057F7D0` | 5 / 5 | — | `00583990` | 1,2,18 | — | — | — |

## 4. Beyond the menu range — all 267 handler-census procedures

The same instrument over every procedure of the handler census ([`members/ui_atlas_all.tsv`](members/ui_atlas_all.tsv)):
**2,648** frontier functions in the subtrees, and **1,830** under a label. A label joined with `+` means the subtree carries
evidence for both, and "several screens" marks three or more (a dispatcher). Such rows name what the subtree reaches,
not a single owner.

| label | procedures |
|---|---:|
| unlabelled | 137 |
| menu list | 16 |
| save / load UI (installer name) | 12 |
| handbook | 10 |
| message window | 9 |
| license board | 8 |
| shop | 8 |
| world map | 6 |
| location map | 4 |
| menu list + action list | 4 |
| status window | 4 |
| battle command menu | 3 |
| handbook + battle log | 3 |
| pause menu | 3 |
| quest list | 3 |
| scroll bar / list | 3 |
| world map + help message | 3 |
| NG signal | 2 |
| action list | 2 |
| boss gauge | 2 |
| confirm window + message window | 2 |
| gambits + message window | 2 |
| help message | 2 |
| license board + world map | 2 |
| world map + location map | 2 |
| auto window | 1 |
| battle command menu + help message | 1 |
| battle log | 1 |
| confirm window | 1 |
| gambits | 1 |
| gambits + action list | 1 |
| item sort + confirm window | 1 |
| level-up blink | 1 |
| license board + message window | 1 |
| screen mask | 1 |
| shop + menu list | 1 |
| silhouette | 1 |
| status window + action list | 1 |
| target info | 1 |
| track map | 1 |

## 7. What is not known

- [x] ~~**UQ-159.** What each procedure draws and does; the labels are ownership only.~~
      ***PARTIAL 2026-09-17 (FABLE): 59 of the 74 procedures are read on a screen page; 15 are placed but not read.** A census of §3's 74 procedure addresses against the 16-UI and save/load screen pages (the atlas, the unlabelled page and the widget-object-model pages excluded) finds 59 cited on at least one screen page, whose protocols and members those pages read. The 15 not cited are leaf panes [the unlabelled-procedures page](../Unlabelled-Panes/the-unlabelled-procedures.md) places by installer ancestry only: `00558BB0`, `005595E0`, `005618E0` (license), `00566A70` (shop), `005677A0` (config family), `0056C060` (gambit), `0056FCB0`, `0056FD30`, `00570460`, `00570530`, `00570630`, `00573B40`, `00574AD0` (handbook), `00577F90` (quest list), `0057F7D0` (save/load), and the launcher `00560910`. Reading those bodies is what closes this; the labels are no longer ownership only for the other 59.*
      ***ANSWERED 2026-09-17 (FABLE): the fifteen leaf panes and the launcher are read, each to its message arms and what they build.** Licence family: `00558BB0` (a `0xC8` child the launcher builds at `00560A9E`) takes the payload's pointer into `+0xC0` on message 1 and attaches (`00247950`); on message 2 it polls twelve slots through `00237630(k)` and, when none answers, releases `+0xC0` (`002494F0`) and tears itself down (`00245020`): a child that lives while any of twelve slots is active. `005595E0` (messages 1..17): builds its layout (`002432B0`), a text node `0029DA70`, the string `0x467C` (`002F9860`), an `0x80`-byte buffer (`002B4090`), record `+0x18 = 02CA95F0`, posts `0x5F`: a caption pane for string `0x467C`. `005618E0` (messages 1 and 16): publishes itself into `02CA8FE8`, clears `02CA9678`, names two children `00D23058` and `00D23030` (`00247570`), renders a query-record row through `0035D330` and `002B58B0` into `+0x18`: a licence detail pane. Shop: `00566A70` (1, 2): sets the sprite node's frame `+0xA` and opacity byte from the payload index, copies the payload word `+0x10` into node `+0x10` for indexes in the mask `0x07C12E22` and sets `+0xD8` bit 0; message 2 runs `002D0410`: a shop icon pane. Config family: `005677A0` (1, 2, 14, 18): 18 clears `02CA96D8`, 14 runs `0056C3A0`, 2 mirrors `+0xC8` bit 0 into bit 0 of two children's `+8` (`00567814`..`00567837`): a config row driving two children. Gambit: `0056C060` (1, 2): layout with kind 9, `+0xD4` from the record byte `+7`, the sprite frame from payload `+0x10`, and the table colour `002DD7E0(record word +0)` into the four corner words `+0x2C`..`+0x34`: a gambit icon pane. Handbook: `0056FCB0` text record `003946B0(payload +8, 0xE)` then `00394800(3, 1, payload +0x10)` and post `0x62`; `00570460` `003946B0(payload +8, 0)` and post `0x64`, the plainest line; `00570530` two table colours `002DD7E0(0x100)`/`(0x101)`, text kind `0x1D`, `0029F4B0`, `00225580`, `0029F480`, post `0x5F`; `0056FD30` (1, 2) a sixteen-byte layout of words `0xFFF`, `002D8C80`, geometry from `01E0C1D8`/`01E0C1DC`, post `0x64`; `00570630` (1, 2; subtree `00576C70`) two sprite strips through `002DAF30`, `002D9DB0`, `002DA2D0` and `002DAC70` with colour words `0x80808080`, results at `+0xC0`..`+0xD0`: a picture pane; `00573B40` text kind `0x2B` from record `+0x10`, `+0x98` widened by record `+0x18`, node `+0x18`/`+0x20` from the record and `0020E620`, post `0x64`, attach under the root `0208EA28`; `00574AD0` text kind `0x1A` from `[02CA9718] + 0x128`, publishes itself into `[02CA9718] + 0x100`, post `0x64`: the current-entry pane. Quest list: `00577F90` (1, 18, 19): clears `[02CA9748] + 0x128`, layout words, text `00394720(0xC8)`, post `0x61`, attaches under `02CA9748`, then `00244960` and `00247870`: a quest row. Save/load: `0057F7D0` (1, 2, 18): publishes into `02CA99E0`, `+0xCC` from `001EDEC0()` or `0xE`, `002CCB10`, `00244F00`, text control `002CCCA0(00D23E98, 0xC8)` into `+0xC0` and `002CD150(0x33)` into `+0xC8`, attaches through `00244960`: the caption pane. The launcher `00560910` (312 instructions): looks up the images `01E0C248` and `01E0C268` (`0024A5A0`), string `0x4B5` (`002814E0`), the name `00D22FE0`, builds the `0xC8` child `00558BB0` (`00560A9E`), registers `00560210` and `00560610` as callbacks, assembles the board through `0055F780`, `00560EE0`, `002D7580` twice, `00291D70`/`00291D80` (string `0xCDF`), `002D45C0`, `00561DC0`, `00561100`, `00558F20` and `00561300`, and under `02F9736A` bit 15 starts the backward transition `00244DD0`: the licence-board screen's launcher. Static, all sixteen bodies read.*
- [x] **UQ-160.** The 25 unlabelled procedures in the menu range, and 137 image-wide. The largest are `00560910` (installed by `005601B0`, called from `00281ED0` / `002D70F0`),
  `005701B0`, `00571A50`, `005742D0`, `005789D0`, `00579420` and `00579AF0`.
      ***PARTIAL 2026-09-17 (FABLE): the 25 in range are sorted; the image-wide count is unsettled.** All 25 are placed by installer ancestry on [the unlabelled-procedures page](../Unlabelled-Panes/the-unlabelled-procedures.md): the license-board launcher `00560910` and four license panes, the handbook text pane `005701B0`, the content pages `00571A50`/`005742D0` and seven handbook leaf panes, the item/equip host `00579AF0` with `005789D0`/`00579420` and an input pane, a quest-list leaf, two shop panes, a gambit pane, a member-scoped pane of the config family and a save/load pane. What remains is the image-wide set outside the menu range, which this page counts as 137 and the register row as 135; the figure has to be re-measured before either is repeated.*
      ***NARROWED 2026-09-17 (FABLE), the count settled from the table itself:** `members/ui_atlas_all.tsv` as regenerated on 2026-09-14 (`0c0ae7f9`) lists 267 widget procedures image-wide, of which **137** carry no label: **23** inside the menu range `00550000`..`0057FFFF` (the regeneration retired two of the 25 the box counted) and **114** outside it, against 73 labelled outside the range. The 114 sit in the 64K buckets `0x23` (16), `0x29` (12), `0x3C` (12), `0x2D` (10), `0x2C` (9), `0x2B` (8), `0x3F` (7), `0x27`, `0x28` and `0x3E` (5 each), `0x35`, `0x39` and `0x40` (4 each), `0x22` and `0x53` (3 each), `0x24` (2) and one each in `0x17`, `0x25`, `0x2A`, `0x36` and `0x5C`. So the register's 135 was stale and 137 is the figure; what remains is placing the 114 outside the menu range, which the atlas does not attempt.*
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 16-UI/Menu-Screen-Atlas/the-menu-screen-atlas.md. See the register row.*
- [x] ~~**UQ-161.** Whether each **child** row is a screen of its parent or a shared dialog created from it.~~
      ***ANSWERED 2026-09-17 (FABLE): every child row is a pane of its parent; the shared dialogs are labelled rows of their own.** The four reusable dialogs [the shared-dialog page](../Shared-Dialogs/the-shared-dialog-widgets.md) reads (`0056F810` menu list, `0057C480` confirm window, `00556F90` message window, `00566680` item-sort bar) each carry their own layout-key evidence and their own installer (`00574D00`, `0057C380`, `00556EC0`, `005665B0`), so they sit in §3 as *evidence* rows, not as children. Of the 20 child rows, 19 have exactly one installer and it lies inside the tree of the screen the row is filed under (the license grid view `0055CD40` under `0055C690`, the quest pane `00575870`, the shop `0057A620`/`0057A4E0`, the world-map children of `005528C0`, the handbook children of `00574E80`/`00572E10`, and so on); the one with two installers, `0056F410` (`0056F3C0` and `00574E00`), has both inside the handbook. No child row is created from more than one screen, which is the property that would make it a shared dialog. Static, from the census columns.*

## 8. Evidence

- **Tier 1, instrument-derived.** [`members/ui_atlas.py`](members/ui_atlas.py) (with the key-family map in [`members/ui_atlas_label.py`](members/ui_atlas_label.py)) → [`members/ui_atlas.tsv`](members/ui_atlas.tsv); `ATLAS_LO=00100000 ATLAS_HI=00900000 ATLAS_OUT=ui_atlas_all.tsv` for §4.
  All inputs are tracked since `OPUS-REQ-SWE2-FRONTIER-ATLAS-GENERATOR-INPUTS` (`7ed031e7`): the call graph is rebuilt by `call_graph.py` from the EXE + `functions.tsv` (tail jumps included), and the frontier is `frontier_census.frontier_set()` — both live under `Database/Tools/analysis-kit/gfz-scripts/`.
## Falsification pass 1 — 2026-09-14 (OPUS), SURVIVED

**Attacked against the handler census, this page's own side files and an independently written
page, not re-read from its prose.**

| # | claim attacked | verdict |
|--:|---|---|
| 1 | 74 widget procedures in `00550000`–`00580000` | **SURVIVED**, from the census itself |
| 2 | 25 procedures carry no evidence yet | **SURVIVED** |
| 3 | the world-map control reproduces the map-screens page | **SURVIVED**, and more strongly than stated |
| 4 | 1,019 frontier functions owned, 860 under a label | **NOT REPRODUCIBLE, not contradicted** |

**1.** `widget-message-handlers.tsv` has exactly **74** rows whose handler address falls in
`0x00550000`–`0x00580000`, counted from the census rather than from this page, and
`members/ui_atlas.tsv` carries 74 procedure rows. The two agree.

**2.** **25** rows in `ui_atlas.tsv` carry no label at all. The remaining 49 split **29 labelled by
evidence** and **20 labelled child**, which the page does not state and which is worth having: the
child rule is structural, so the evidence-backed population is 29, not 49.

**3. The control is stronger than the page claims.** The three world-map procedures come back
labelled `world map + help message`, `world map` and `world map` — and their `installed_by` column
gives `00550400 → 00552250 → 005528C0 → 00553AE0`. The map-screens page, written from layout-key
readers and constructors rather than from subtrees, records `00550400` installing `00552250` at
`00550444` and `00552250` installing `005528C0` at `00552301`. **The same chain, in the same order,
from two methods that share no input.**

**4. The unique figures cannot be recomputed here, and the checkable bounds do not contradict them.**
The `frontier` column sums to **1,604**, which is expected and not a refutation: the page states that
subtrees overlap and that 1,019 is the *unique* union. Evidence-labelled rows sum to **1,024** and
evidence-or-child to **1,299**, so `860 ≤ 1,024` and `1,019 ≤ 1,604` both hold. **Consistency is
not confirmation**, and it is recorded as consistency.

### The finding, and it is the same one the map-screens page has

`members/ui_atlas.py` is tracked and sits beside this page. It opens `tools/rawcalls.json`,
`arch_frontier.txt` and `c_frontier.txt`, and **none of those three is in the repository** — all
live under `Database/Tools/work/`, which `.gitignore` excludes. The union that produces 1,019 and
860 is exactly the part the side files do not carry, so those two figures are the ones a peer
cannot check at all. Filed as `OPUS-REQ-SWE2-FRONTIER-ATLAS-GENERATOR-INPUTS`.

> **Resolved 2026-09-15.** `ATLAS-GENERATOR-INPUTS` closed at `7ed031e7`: the generator rebuilds
> the call graph from the EXE + `functions.tsv` via `call_graph.py` (tail jumps included, which
> `edges.tsv` drops) and takes the frontier live from `frontier_census.frontier_set()` — the union
> figures are reproducible. And the widget-census regen (`OPUS-REQ-SWE2-FRONTIER-WIDGETPROC-REGEN`)
> moved this page's figures: **74 → 80** region rows, **1,019/860 → 1,065/913** unique frontier,
> **251 → 267** census procedures and **2,619/1,764 → 2,648/1,830** in §4. The unlabelled count
> stayed **25** — the new procedures all carry evidence. The figures above the resolution line are
> the falsification's own dated record.

**Not attacked, and not claimed:** what any procedure does. This page says it is an atlas and not a
reading, and this pass did not turn it into one.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT and SERVICE, 21 edges.** Cited atlas functions are called by Presentation bodies, among them the two `0xBC08` map-screen pages (4,810 and 4,847 bytes) and bodies of 1,420, 1,422 and 2,882 bytes. They call Presentation bodies of 61 to 3,406 bytes.
- **Resource — SERVICE, 20 edges.** Cited atlas functions call small Resource helpers (60 bytes 8 times, 75 bytes 4 times, 57 and 104 bytes twice each, and 265 bytes).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Movement — SERVICE.** `002D70F0` on this page calls `FUN_00326bb0`, owned by that layer. What it reaches is a one-time reset guarded by bit 0 of `[022C25A0]`: it stamps a table of `0x30`-byte slots from `022C25B0` with `0xFFFF` sentinels and zeroed counters; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — SERVICE.** `0056D370` on this page calls `FUN_00316a50`, owned by that layer. What it reaches is a 411-byte achievement routine bounded at **`0x1E` ids**; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 19 edges).** 14 edges are the
`0020E600`/`0020E620` image-pointer pair inside this page's installer/registration bodies; the other
5 are `001EDEC0` calls from `005528C0`/`005542D0`/`0057C480`/`0057F7D0`/`0057FE80`.

**Audio — MECHANICAL (SWE2-CONTRACT 2026-09-15, 18 edges).** 17 edges are the shared helper
`00249C60` (Audio-tagged) called by this page's screen-registration bodies
(`00281ED0`/`00552250`/`005528C0`/`005542D0`/`00557DB0`/`0055CD40`, …); the last is `00225580` via
`00570530`. Same generic-helper fan-in as the layout-parameter row — no audio relationship the atlas
owns.

**Rewards_Progression_Economy — SERVICE (SWE2-CONTRACT 2026-09-15, 1 edge).** The screen-registration body `0056D370` calls `GameState_GetGil` `00253690` — a menu screen reads the wallet. Small, real.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Items_Equipment_Shops_License — SERVICE (18 edges).** The license-board procedures call the board's selector and node accessors: the cursor handler `00557DB0` calls `BattleStats_GetLicenseBoardSelectorB` (`00323630`), `BattleStats_GetLicenseBoardSelectorA` (`00323670`), `BattleStats_GetActiveLicenseBoardSelector` (`003236B0`), `BattleStats_SetLicenseBoardSelectorBAndActive` (`003236F0`) and `BattleStats_SetLicenseBoardSelectorAAndActive` (`00323740`); the grid view `0055CD40` calls `BattleStats_SetLicenseNodeStateByStatsIndex` (`003235C0`), `00323630` and `00323670`; the launcher `00560910` calls `00323670`; and the license pane `005618E0` calls `00323630`, `00323670` and `003236B0`. The shop procedures call the trade and equipment bodies: the trade screen `0056D370` calls `Shop_CommitPurchaseItemAndGil` (`002FEEB0`), `Shop_CommitSaleItemAndGil` (`00310870`) and `BattleIdClassD_SetRuntimeFlagBit2` (`0030B630`); `0057A620` and the item list `0057AC10` call `Equipment_CheckItemEligibleAgainstCurrentLoadoutByStatsIndex` (`00317B70`), and `0057AC10` calls `BattleStats_SetEquipmentSlotByMappedId` (`0031A510`). The atlas's license and shop screens are the front ends of those operations: they read and switch the character's board selector, set node states, commit purchases and sales, and test and equip items through that layer's own bodies.

**Save_Load_Settings — CLIENT and SERVICE (19 edges).** The save/load procedures call into that layer: `0057F360` calls `0057EA40`, `0057F6B0`, `005812B0`, `005813E0`, `005817D0` and `00581860`; the slot screen `0057FE80` calls `SaveImage_GetActiveRuntimeBuffer` (`002EF640`), `00580A80`, `00580B40`, `00580CD0` and `SaveLoad_ControllerTransitionStateMachine` (`00580EB0`); and `SaveWrite_OperationStateCallback` (`0057E4D0`) calls `SaveWrite_PrepareAndSubmitFullImage` (`0057E310`). In the other direction, `00580EB0`, `SaveLoad_ControllerLifecycleHandler` (`00582860`) and `SaveLoad_HandleStorageStatusResultAndAdvanceController` (`00583040`) call `00583990`, the installer of the `0057F7D0` procedure; `00582860` calls `001EDEC0`, a 40-byte predicate over two runtime globals; and `005812B0`, `005817D0` and `00581930` call `00225580`, a 4-byte store of its second argument at `+0x18`. The save/load screens and the save controller are one exchange: the screens drive the controller's transitions and the full-image write, and the controller installs the screen procedures and uses two tiny shared helpers.

**WorldAreaField — SERVICE (1 edge).** The handbook content page `005742D0` calls `00576A50`, a 529-byte body filed by domain to `WorldAreaField.ConditionalBattleIdResolution` that reads an entry, bounded by the count at `+0x12`, from a table hung off the object at `02CA9738` (read to that point only). What the handbook page looks up through it is not read here; the edge is one screen's call into a world-domain lookup.

`0055F780` (173 B) is the subtree refresh `00560910` runs on a mode change: a nonzero `edx` first calls `00561100` to rebuild the slot tables, then `002D48C0` on `+0xC0` with the count (1 when zero); `edx==0` instead reads the count from `0209AC30`'s `+0xB2C` byte - either way `0055F830` rebinds, the `+0x120` dword array scans for the current `+0xDE0` word and `002D47C0` flags the match, and the count stores at `+0x182`.

Interior anchor `0055F7F0` (function `0055F780`).

`00561DC0` (155 B) is the flag broadcast `00560910` runs beside `0055F780`: `cl` stores to `0209AC30`'s `+0xDEA` byte, `00247920`/`00295CF0`/`0028F570` resolve the live nodes, and `00247730` propagates the byte to each of them and then to the `+0x118`/`+0x120`/`+0x128` chain - the same-value write that keeps the panel tree's flag coherent.

Interior anchor `00561E09` (function `00561DC0`).

`00561100` (150 B) is the nine-slot enumerator `0055F780` and `00560910` call: slots 0..8 resolve through `00282DF0` and pass `00282FA0`'s validity check; each live slot records its index at `+0x120 + hit*4` and two `002526F0`-computed u16 fields into the packed `+0x138`/`+0x144` arrays - returns the live count that seeds the caller's scan bound.

Interior anchor `00561146` (function `00561100`).
