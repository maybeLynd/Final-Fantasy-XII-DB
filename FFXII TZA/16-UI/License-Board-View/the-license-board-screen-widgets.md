---
system: The license board screen — the widget tree of the main-menu board view, its message protocols, and the
  roles of its subtree members
category: 16-UI
status: "DOCUMENTED — GI-3 answered 2026-09-29 (FABLE), review (FABLE-REQ-AUDITSEM-REVIEW-GI-UI, ACCEPT, d998217e2); documented_rule.py READY, no open box or live id; owner re-status 2026-09-30 (SWE2-FRONTIER, record dd-restatus-gi-0930). Was PARTIAL on: id 285's 18 sub-commands and which of 005565E0/0055A340/00557760 draws which layer are unresolved; the +0x37D move mode narrowed 2026-09-18 to a four-state byte written at six sites in 00557DB0"
owner_layer: CodeDomain:UI (menu screens)
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: 'procedure membership from the menu screen atlas (../Menu-Screen-Atlas/members/ui_atlas.tsv); dispatches
    decoded from the function bodies; the grid view widget ''s data path is the one
    [the grid build page](the-license-board-grid-build-and-its-change-sweep.md) already documents'
last_reviewed: 2026-09-14
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: opus-license-board-pass-1 - the ten-row procedure tree attacked three ways at GN160 and all three hold: every named installer really carries a rip-relative lea of its procedure (10 of 10, from the image), every subtree size matches the menu screen atlas the page cites as its source (10 of 10), and the page's installer agrees with the atlas's on every row (10 of 10). No correction. Separately noted: the atlas's message_ids for 00557DB0, one of these rows, lists only id 10 while the body answers 1, 2 and 10 - that is an atlas row, not a claim of this page, and is routed to the atlas owner
  crossref_clean: false
  reopened_count: 0
---

# The license board screen widgets

> **The license board is a three-layer widget tree.** `00561390` is the screen — created lazily by `00561300` into a
> slot on the menu container, owning the board textures and the top-level open/close transition. Under it sits
> `0055CD40`, the board **view** widget — a 141-member subtree that owns the `licd` grid, the cursor, the tile art,
> and the change sweep [already documented for its data path](the-license-board-grid-build-and-its-change-sweep.md).
> `00557DB0` ~~is the directional-input handler: the only application message it answers is id 10, the cursor-move
> command.~~ **Corrected 2026-09-29 (FABLE, GI-3):** is the licence-board **chooser**, the twelve-board wheel whose three draw layers it
> installs, and it also answers id 285 for its own two dialogs (§8a). `00558FB0` is the tile/panel art window (`Maru_c.tm2`, `lic_B_4_c.tm2`, `lic_B_8_c.tm2`).

**PARTIAL.** Read: the tree, every procedure's decoded dispatch, and each screen-region member's role. The ~190
members that are shared engine helpers are cited as families, each named with representative members (2026-09-15):
the resource loader `00249xxx` and resource helpers (`0024A4E0`, `002FBEF0`), the `0024xxxx` widget object model
(`002418F0`/`00243E90`/`00247300`/`0024ABA0`/`0024B270`/`0024B3A0`/`0024C550`/`0024F410`/`0024F610`/`00252F40`/
`00252FA0`/`00254A00`), the text-object cache `001Bxxxx` (`001B1F70`/`001B1F80`/`001B2410`), the TIM2 slot table
`0039Bxxx` and its `003FFxxx` wrappers calling `0039BA00` (`0039BA30`, `003FFAB0`/`003FFB00`/`003FFBC0`/`003FFC60`/
`003FFDA0`/`003FFEE0`, `00474650` → `003A22A0`), the text-format engine `002A9F00`/`002AE450`/`002B2150` and its
emitters `0017F7C0`/`0017F850`/`0017F8E0`/`0017F920`/`0017FA10`/`0017FAE0`/`0017FB00`/`0017FC90`/`0017FD00`/
`0017FD30`/`001813F0`/`001816F0`/`00181A10`/`00182EB0`/`00182EE0`, the `002Cxxxx`/`002Dxxxx` menu controls and
draw-batch ops (`002C12B0`/`002C1320`/`002C19E0`/`002C1A80`/`002C3C10`/`002C5480`/`002C9060`/`002C9400`/`002C9890`/
`002C9BD0`/`002CCA00`/`002CCBA0`/`002CD470`/`002CDEA0`/`002CE2D0`, `002D0280`/`002D02C0`/`002D03B0`/`002D0410`/
`002D04F0`/`002D7A90`/`002D7B40`/`002D8B00`/`002DD350`/`002DD910`/`002DDC50`), the license-node accessors
(`00300B80`/`00317930`/`00317B70`/`003235C0`/`003236F0`/`00323740`/`00323910`/`00323D10`/`00324020`/`003242F0`,
boundary `00282A40`/`0030A310`), the Input predicates and boundary (`001976E0`/`001976F0`/`001E0A40`/`001E0A70`,
`002AEB20`), the StoryEvent boundary (`00263990`/`002639E0`/`00283730`/`00283E40`), the Audio helpers and boundary
(`00182E80`, `002C2F90`/`002C4220`, `0055AE00`/`0055B840`), the CoreRuntimeScheduling pair `00229DF0`/`00229E70`,
the `003Axxxx` Presentation/effect accessors and the EFX loader (`003A1FE0`/`003A2020`/`003A2090`/`003A72A0`/
`003A76F0`/`003A77F0`/`003A79C0`/`003A7B50`/`003A7D00`/`003A7E80`/`003A8000`/`003A8900`/`003A9560`/`003A9730`/
`003A9920`/`003A9A70`/`003A9CC0`, `003B0130`/`003B1310`/`003B2BC0`/`003B2CE0`, `003EDAD0`/`003EE2D0`), the
`0029xxxx` format helpers (`0029DF20`/`0029E330`/`0029E6B0`/`0029E730`/`0029E750`/`0029E770`/`0029E790`), the
`00364xxx`/`00365B50`/`00366xxx` text-template helpers (`00364210`/`003647E0`/`00364980`/`00365B50`/`00365FD0`/
`003666E0`), `00306340` with the CombatAction pair `003064F0`/`00308FF0`, the widget field setter `002845E0`, and
the leaf layer `002B1C90`/`002B1D20`/`002B4730`/`00374930`.

## 1. What the player sees

The license board: a 24×24 grid of license tiles per character, a cursor that walks the grid, a side panel with
the highlighted license's art and cost, and the LP total.

## 2. The procedure tree

```
00561390  license board screen        installed by 00561300 (lazy-create into container+0xC8)   subtree 38
  +-- 0055CD40  board grid view       installed by 0055C690 (in 00561390's subtree)             subtree 141
  |     +-- 00557DB0  cursor/input    installed by 00557AE0 (in 0055CD40's subtree)             subtree 55
  |     +-- 005565E0  draw widget     installed by 005572B0 (in 0055CD40's subtree)             subtree 16
  |     +-- 005569F0  board+message   installed by 005571F0 (in 0055CD40's subtree)             subtree 50
  |     +-- 00557760  draw widget     installed by 00557370 (in 0055CD40's subtree)             subtree 9
  |     +-- 0055A340  draw widget     installed by 00557430 (in 0055CD40's subtree)             subtree 17
  |     +-- 00558CE0  child window    installed by 00558C40 (in 00558FB0's subtree)             subtree 7
  +-- 00558FB0  tile/panel window     installed by 00558F20 (in 00561390's subtree)             subtree 37
  +-- 00556DB0  leaf child            installed by 00556D20 (in 00558FB0's subtree)             subtree 1
```

Every `installed by` edge is a `lea <proc>` inside the named member — the same factory shape as the quest list
(`{0x100/0x110-byte, proc, payload}` create record into `00244F50`), e.g. `00561300` `lea rdx,[rip+0x31]` =
`00561390` at `00561358`, `0055C690` `lea` = `0055CD40`, `00558F20` `lea rdx,[rip+0x37]` = `00558FB0` at
`00558F72`. The three rows the atlas labels "child" (`00556DB0`, `00557760`, `00558CE0`) plus `005565E0`,
`005569F0`, `0055A340` are all installed only from inside this screen — screen children, not shared dialogs.

**Corrected 2026-09-29 (FABLE, GI-3):** the tree above draws `005565E0`, `005569F0`, `00557760` and `0055A340` as children of `0055CD40`. Each one's installer has a single caller, in `00557DB0`'s construct arm (`005581AC`, `005581BC`, `005581CA`, `005581D7`), so they are **`00557DB0`'s** children; `00557DB0` itself is installed by `00557AE0` (`00557B21`), called from `00558FB0` (`0055937C`). The tree lines are left as drawn; this sentence supersedes them (§8a).

## 3. The screen root — `00561390` (1,091 B)

Chain dispatch at `005613AC`–`005613D1`: live ids **1, 15, 16, 18, 20**.

| id | arm | what it does |
|---:|---|---|
| 1 CONSTRUCT | `0056153C` | registers the widget (`00247570` with a name pointer at `0056156C`), stashes the parent from the create record (`rdi+0xC0 ← [rsi]`), copies `+0xD0`/`+0x10C` mode bits and `+0x108` from it (`00561587`–`005615BE`), then loads the screen's textures through `00249580`/`00249210`/`002493D0` — indices `0xA8` (`0056162B`), `0x7E` (`lea r8d,[rdx+0x77]` with `edx = 7`, `0056165F`), `0x7A` (`00561692`), `0x2B` (`005616CA`), `0x78` (`005616FA`), `0x7D` (`0056175A`) of container 7 — into `parent+0x110`, `+0x118`, `+0x100`, `+0x108`, `+0xE8`, `+0xF0`, `+0xF8`; a `0057A2D0` call seeds `+0xD8`; ends `002470D0` (push focus). The constant-request census already ties this path to `Lic_Bk.tm2`, `cm2_win_c.tm2`, `lic_8_c.tm2`. |
| 15 ABOUT-TO-BE-DESTROYED | `00561522` | broadcasts `00244F00` to the `+0xE0` child. |
| 16 | `005614AB` | full teardown-and-return: releases `+0x108` (`00247720`), resets the `+0xD8` effect (`003B29B0` fx-reset + `003697F0` free), runs `0055C690` (install the grid view), `0055A810`, `00247930(self, 0x74)`, and `00246AD0` on the UI singleton. |
| 18 BEING DESTROYED | `00561403` | unpublishes (`parent+0xC8 = 0`), `003B2B40`, `00561020` on the container; if `+0x10C & 1` sends `{0x8003}` up; else plays sound `0x4B5` (`00280CA0` → `002CA150` → `0027EE80`) and re-opens the tile window `00558FB0` through `00558F20` when `+0x10C & 4`, else `00246AC0`. |
| 20 | `005613E0` | forwards the record verbatim to the `+0xC8` child's handler — `call [rcx]` (`005613F0`–`005613FC`). |

## 4. The board view — `0055CD40` (3,564 B)

Two-level dispatch: `cmp eax,0x11D` at `0055CD53` separates the out-of-range id **285** (`0x11D`) from a rel32
table at `0055DB2C` covering ids 1–23 (`0055CD71`–`0055CD82`). Live arms:

| id | arm | role |
|---:|---|---|
| 1 CONSTRUCT | `0055CDE6` | registers via `002432B0` on the UI singleton's `+0x58` list (`0055CDEE`–`0055CE02`); publishes viewport metrics from `self+0x60` into globals (`0055CE1B`–`0055CE61`); stashes parent `+0x130`, copies `+0x160` mode and `+0x570 & 0x400` from `parent+0x10C` (`0055CE95`–`0055CEC6`), takes the shared map/licence data pointer `parent+0xC0+0xE8` into `+0x168`. |
| 2 GEN-RECONCILE | `0055D1F9` | `0055AA00` + `0055E9E0` — reconcile then the input/confirm step. |
| 4 draw-after-content | `0055D814` | the draw pass proper: `0055AB20` + `0055AE80` (batch setup, `002D9380`/`002D9B00`/`002D9C40`), `0055BAC0` (per-cell draw), `0055B6D0` (`002D8C80` flush). |
| 8 / 9 | `0055D1D1` / `0055D1E5` | set / clear `+0x570` bit `0x8` — a visibility flag. |
| 10 directional input | `0055D4EA` | gated by `+0x570 & 4`; reads three input globals and calls `0055C740` — the cursor move. |
| 12 enable | `0055D520` | sub-commands `0x8000/0x8001/0x8002` on `msg->a`: `0x8000` toggles `+0x570 \|= 0x200` and repaints; `0x8001` flips the `+0x10C` bit on `+0x130` and clears the selected node (`+0x188 = 0xFFFF`, `0055D5B7`); `0x8002` path tears down via `00244F00` + `00561800`/`005597C0`/`00561E60` + `003B28F0`. |
| 15 | `0055D174` | `00251F00(0/1)` + `002D7760` — disable-state entry/exit. |
| 18 | `0055CD84` | frees the grid byte-map `+0x128` and the cell array `+0x120` (`003697F0` ×2), clears `+0x40` bit `0x200000`, unpublishes the view from the singleton's `+0x320` and `+0x130+0xC8`. |
| 19 | `0055D151` | `00251F00(1)` + `002D7580(0,2)` — the inverse transition of 15. |
| 20 | `0055D1A0` | `002858A0(0,0)`; removes the `+0x548` effect if present (`003B2AA0` fx-remove). |
| 23 | `0055D213` | layout: recentres the board rect at `+0x50C` from the window-size globals and a `+0x528` scale, then `0055B960` — the resize/scale path. |
| 285 | `0055D84B` | a second rel32 table at `0055DB88` on `msg->a - 0xA` (18 arms) — ~~the application-specific command set: node-select, confirm, LP spend (arm heads read `+0x4F1` mode, `+0x55B` state, `+0x418` node table).~~ **Corrected 2026-09-29 (FABLE, GI-3):** the **reply of the dialogs the board opens**: `msg->a` is the dialog code, `msg->b` the answer; codes outside `0xA`–`0x1B` take the `ja` to `0055D978`. Every slot in §8a. |

## 5. The cursor handler — `00557DB0` (2,475 B)

~~Chain dispatch: ids **1, 2, 10** (`0057DC5`–`0057DE2`).~~ **Corrected 2026-09-29 (FABLE, GI-3):** besides construct (`00557FD3`, which builds the twelve-board wheel) and id 10, it answers id 285 at `00558598` for the two dialogs it opens — code `0x18` (`00557F23`) and the Yes/No code `0x19` "Choose this license board?" (`00558468`, `005584C6`), whose Yes commits the board (`005585CF`); see §8a. Id 10's arm at `00558261` ~~is the only application logic~~ —
it calls `0058xxx` helpers `00557B90`/`0055FFC0`/`005611A0` that resolve the character record (`00282DF0`) and the
license-node accessors `003236B0`/`00323670` — the same `BattleStats_GetLicenseBoardSelector*` family already named
in the census. The `+0x37D` byte at `00557DF0` is the cursor's move-mode. *(Narrowed 2026-09-18, FABLE, from its six sites — all inside `00557DB0`, the id-10 arm's owner:* it is read once, after `00558AF0`, and switched on 0 / 1 / other (`00557DF0`–`00557DFF`); from 0 it becomes **1** with the byte `+0x37E = 0x10` when `00252D10(0xBB)` denies (one word store, `00557F4C`) and **2** when it allows (`00557F57`); **2** is also the id-10 arm's exit value (`00558707`); **3** is stored on each of the three action paths — after the effect removal `003B2AA0` (`00557E5F`), after the helper chain `005588C0` / `00558C40` / `00556EC0` (`00557EF1`), and after the `002CE2F0` / `002CE280` pair (`00557F35`). So it is a four-state field — idle, denied-with-countdown, free, settling — whose state names are readings; what each state does to the pad on screen is not read. The earlier anchor `0057DF0` was missing a digit.)*

## 6. The tile/panel window — `00558FB0` (1,332 B)

Table dispatch at `0055DB2C`-style table `005594E4`, live ids **1, 2, 15, 16, 18, 20**. The construct arm
(`005590EF` onward) loads the panel art — `Maru_c.tm2`, `Maru_c_2.tm2`, `lic_B_4_c.tm2`, `lic_B_8_c.tm2` per the
constant-request census — and the id-18 arm at `00558FF0` plays sound `0x4B5`, unpublishes `parent+0xC8`, and runs
`00561020`. Its `00558CE0` child (ids 1, 2, 18) handles the confirm reply; `00556DB0` is a one-message leaf.

## 7. Member roles (screen region `0x556380`–`0x561F20`)

Grouped by what the bodies do — every entry read, citation is the first distinctive instruction:

| member | role |
|---|---|
| `00561300` | lazy-create `00561390` into `parent+0xC8` — `lea rdx,[rip+0x31]` at `00561358` |
| `00561390` | screen root; §3 |
| `0055C690` | install/focus `0055CD40` — `lea` `0055CD40`, `00244F50` + `00246AD0` + `002470D0` |
| `00558F20` | lazy-create `00558FB0` into `+0xC8`, sets `+0x187` — `00558F42`–`00558F7E` |
| `0055CD40` | board grid view; §4 |
| `0055C740` | cursor move — reads the three input globals (`0055D4F7` call site), walks `+0x418` node table via `00282DF0`/`0029DBE0`, emits through `00247510`/`00247570` |
| `0055B3F0` | **the licd grid build** — already documented: `+0x559/+0x55A` = `licd` width+1/height+1, byte map at `+0x128` |
| `0055BFF0` (+ `0055B310`) | **the change sweep** — already documented: walks `+0x120` cell array row-major |
| `0055DBD0` | board teardown/rebuild — frees (`003697F0`), `0055B3F0` + `0055B560` + `0055C530` + `0055A1F0`, then `00244F00` (`0055DBD0`–`0055DCxx`) |
| `0055B560` | free the grid resources — `002497E0`, `003697F0`, `003B2AA0` fx-remove |
| `0055C530` | node-state apply pair — `0055E2C0` + `0055E600` |
| `0055E2C0` | node eligibility — `00282DF0` char record + `BattleStats_CheckLicenseNodeAcquireReason` (`00323600`) |
| `0055E600` | node-state write — `00282DF0` + `BattleStats_GetLicenseBoardSelectorB` (`00323630`) + `00560F20`/`00560FA0` |
| `0055E9E0` | confirm/purchase step — `00247 870`, `00252D10`/`00252D40`, `00282DF0`, `00295D20`/`00295D70`, `002CE280`/`002CE2F0` |
| `0055F3E0` | the same shape as `0055E9E0` plus `00295CA0`/`002D6620` — confirm-commit variant |
| `0055A1F0` | rebuild the 8-row license list — `00244DD0`, `00246AD0`, `00247680`, `00282DF0`, `00559E30` |
| `00559E30` | the license-list row builder — 8-iteration loop (`00559FB2`/`0055A109`), `0035D330` message-table lookups (`ecx` = `0x1D`/`0x14`/`1`), `00285F40` icon, `002B58B0` text emit, `002D48C0` count publish |
| `0055A180` | list-rebuild wrapper gated on `+0x570 & 2` — `0055A180` |
| `00557B90` | LP-spend flow — `00282DF0` + `003236B0` selector + `00557A40`/`00557A90` effect pair + `0055FFC0`/`005611A0` |
| `00557A40`/`00557A90` | twin 75-B effect triggers — `00249C60` + `0027EDA0`/`0027F430` + `00558760` |
| `00558760` | confirm helper — `00244F00` + `002527B0` + `005588C0`/`00558C40` |
| `005587E0` | node check — `00282DF0` + `00282FA0` + `00323630`/`00323670` |
| `005588C0`/`00558960`/`00558A10` | effect spawn/remove chain — `003B2AA0`/`003B2D80` (fx-remove/fx-spawn), `00558A10` wraps `00558960` |
| `00558AF0`/`0055F1C0` | command dispatch — `00248F40` on `+0x158`/`+0x530` |
| `0055AA00` | reconcile helper — `002D66A0` on `+0x565` flag |
| `0055AB20`/`0055AE80` | draw-batch setup — `002D9380`/`002D9B00`/`002D9C40` |
| `0055BAC0` | per-cell draw — `00282DF0`, `002D8910`, `002DB080`, `002DD7E0`, `002F9860`, `00365B30` |
| `0055B6D0` | draw flush — `002D8C80` |
| `0055B2B0`/`0055E090`/`0055E230`/`0055DEA0`/`0055E3F0` | leaf grid iterators — loop over `+0x55A` rows/`+0x554` cols, no calls |
| `0055B8C0`/`0055B960` | geometry — board-rect math against `+0x550`/`+0x554` |
| `0055DD70` | sweep wrapper — tail `0055BFF0` |
| `0055EF10` | wrapper — `0055F010` |
| `0055FFC0`/`005611A0` | job/board lookup — read a global table, `00282DF0` + `00323670` |
| `00560F20`/`00560FA0` | twin 119-B table readers on the same global — `00560F20`/`00560FA0` heads |
| `00561020` | release a `+0x24`-ish object — `0024A680` + `003697F0` |
| `00561830`/`00561E90` | create factories — `lea` `005618E0`/`005595E0`, `00244F50` + `00246AD0` |
| `00561800`/`00561E60`/`005571C0`/`00557280`/`00557340`/`00557400`/`005597C0` | child destroyers — 43 B each, `00244F00` on a fixed slot (`+0xE8`/`+0xF0`/…) |
| `005571F0`/`005572B0`/`00557370`/`00557430`/`00558C40`/`00556D20`/`00556EC0`/`0055A810`/`00559860` | child factories — the `cmp [rcx+slot],0 / 00244F50 / 00246AD0` shape, each `lea`s its procedure (`005569F0`, `005565E0`, `00557760`, `0055A340`, `00558CE0`, `00556DB0`, `00556F90`, `0055A8A0`, `005599D0`) |
| `00557760` | draw child — ids 1/4/18, arm 4 calls `005574C0` (`002DB080` draw) with ~~`+0xDA` scroll word~~ `+0xD8`/`+0xDA` the wheel centre from the create record — the **backdrop disc** of `00557DB0`'s wheel (corrected 2026-09-29, FABLE, GI-3; §8a) |
| `005565E0`/`0055A340` | draw children — ids 1/4/18/25 (`0055A340` also 2), ~~arm 4 `002472A0(self, xmm1=[+0xD8]+0x34C, 2)` — scroll/alpha~~ **Corrected 2026-09-29 (FABLE, GI-3):** the `002472A0` call with the owner's `+0x34C` angle is the id-25 arm (`0055661C`, `0055A385`); arm 4 draws the **twelve board emblems** (`005565E0`) and the **members' faces** (`0055A340`) of the wheel (§8a) |
| `005569F0` | board+message window — ids 1/2/4/18; construct builds the `NobuMessage`/`MessageLine` text, draw arm walks `+0xE8`/`+0xEA` counters emitting via `002B3050`/`002B3400`/`002D8690` |
| `00558CE0` | confirm-window child — ids 1/2/18, calls `00558E70` + `0020E620`/`002B58B0` text + `00323630`/`00323670`/`003236B0` selectors |
| `00558E70` | node-info read for the confirm child — `0020E620`, `00282DF0`, `00323630`/`00323670`/`003236B0`, `00556380` |
| `00556380` | text emit — `0017D2E0` format + `002AB870`/`002DD7E0`/`002F9860` |
| `00556DB0` | leaf child — ids 1/18, `002432B0` register + `002445C0`/`002D45C0` |
| `0055A810` | factory `lea` `0055A8A0` |
| `00559800` | single-message send — `00244DD0` |
| `00561020` | release helper (above) |
| `0057A2D0` | 38-B resource-load wrapper — `00249210` with `+0x20` flag 1 |
| `00561F20` | bounds check — `+8` vs `+0x10` word compare |

Shared engine helpers in the subtrees (families, not re-read): `00244F50`/`002465F0`/`00246AD0`/`002470D0`/
`00244F00`/`002473B0`/`002482E0` — the widget framework from
[the widget contract](../Widget-Object-Model/CONTRACT-widget-object.md); `00249210`/`002493D0`/`00249580`/
`002497B0`/`002497E0` — the container-7 resource loader (`menuquest.dat`'s loader at §4 of the quest-list page);
`00282DF0` — the character-record resolver; `00323600`–`00324470` — the `BattleStats_*License*`/`Selector*` family
already named in the census; `003B28F0`–`003B2D80` — the menu effect registry (`fx-reset`/`fx-spawn`/`fx-remove`);
`002D5xxx`–`002DExxx` — draw batch + text emit; `0035D330` — the message/string-table lookup;
`0017Fxxx`/`001Bxxxx` — CRT tail-call adapters and the text-object cache (both already in their member TSVs);
`0039BB60`/`0039BEC0`/`0039BF50` — the TIM2 slot table + `FontBaseHeight` readers.

## 8. Controls and limits

- The grid-build and change-sweep data path (`0055B3F0`, `0055BFF0`/`0055B310`) is **independently documented** on
  [the sibling page](the-license-board-grid-build-and-its-change-sweep.md) and sits inside `0055CD40`'s subtree —
  the two pages agree on which object owns the `licd` grid.
- `00557DB0`'s id-10 arm is the same input protocol the Config screen documented for message 10 — directional
  input becomes a cursor delta.
- Not resolved: ~~the 18 sub-commands of id 285 (the board's own vocabulary — select/confirm/sort are reachable but
  not yet named), which of `005565E0`/`0055A340`/`00557760` draws which layer, and~~ the `+0x37D` cursor move-mode
  values. *(The first two answered 2026-09-29 (FABLE, GI-3) — §8a.)*

## 8a. GI-3 answered 2026-09-29 (FABLE) — id 285 is the dialog reply; the wheel's three layers

*(FABLE, Claude Opus 5.5 — NATIVE/STATIC, bodies read; dialog texts resolved from the shipped `us` tables; control
[`gi3_dialog_reply_and_wheel_layers.py`](../../_index/candidates/gi-0929-ui/gi3_dialog_reply_and_wheel_layers.py), FAILS 0.)*

**Id 285 (`0x11D`) is the reply a shared dialog posts to the widget that opened it:** `{0x11D, a = the code the opener
passed, b = the answer}`. Only three bodies store `0x11D` into a message — `002C2899`, `002CE103`, `002CE417` — in
`002C2320`, the Yes/No box `002CDF20` and the message box `002CE370`. The message box is opened by
`002CE2F0(owner, code)` (`lea` at `002CE33D`), keeps the owner at `+0xC8` and the code at `+0xD0`
(`002CE4BB`–`002CE4C5`), picks its text by the code through the table `002CE728`, and on close posts `b = −2` for
`0x8100`, else 0 (`002CE404`–`002CE459`). The Yes/No box is opened by `002CDEA0(owner, code)` (`lea` at `002CDEED`); its
options "Yes" `0x3E8` → `0x8100` and "No" `0x3E9` → `0x8101` (`002CE093`–`002CE0B3`) reply **`b = 1` for Yes**, −1 for
No, −3 for `0x8102` (`002CE0F1`–`002CE187`). `0055CD40` switches on `a − 0xA` through `0055DB88`
(`0055D84F`–`0055D86E`); any `a` outside `0xA`–`0x1B` takes the `ja` to `0055D978`.

| `a` | arm | opened by the board at | text (shipped `us`) | what the arm does |
|---|---|---|---|---|
| `0xA` | `0055DB10` | `0055D711` — confirm on a node with bit 12 set and `0x6000` clear | "Insufficient license points." (`0xCD9`) | nothing |
| `0xB` | `0055D870` | `0055EC58`–`0055EC73`, once per node of the `+0x418` list while `+0x4F1 < +0x4F0` | "The license for the Esper … has been added to the board!" (`0x426B`) | sets the node's seen flag (`00252D40`), `00559860(node)`, `+0x4F1` + 1, `+0x55D` cycles |
| `0xC` | `0055D93B` | `0055F557`–`0055F566`, when `+0x570` bit 5 is set | "… has learned a new Mist ability!" (`0x426C`) | `+0x55E` = 3, `+0x560` = `0x18` |
| `0xD` | `0055D925` | `0055EC9F`, once, after the Esper notices (flag `0x4B`) | "Only one character can obtain this license. When a character obtains the license, it will be removed from the boards of all other characters." (`0x4268`) | `+0x55B` = 3, `+0x55C` = `0x18` |
| `0xE` | `0055D95B` | `0055F5B0`: node `+0xB` = 3, once (flag `0x4C`) | "The character can now summon Espers under the Mist command …" (`0x4269`) | `+0x55E` = 4, `+0x560` = 0 |
| `0xF` | `0055D95B` | `0055F5D6`: node `+0xB` = 2, once (flag `0x4D`) | "The character can now perform quickenings under the Mist command …" (`0x426A`) | as `0xE` |
| `0x10`–`0x19` | `0055D978` | never by the board — `0x10`–`0x17` are menu help texts, `0x18`/`0x19` the chooser `00557DB0`'s | — | the shared out-of-range arm |
| `0x1A` | `0055D8D8` | `0055ECEA`, when `+0x4E8` is set and its flag is not | "The Second Board license has been added to the license board!" (`0x428A`) | sets the flag, `00559860(+0x4E8)`, `+0x55D` cycles |
| `0x1B` | `0055D906` | `0055ECF8`, once that flag is set | "Characters who have earned the Second Board license can access an additional license board." (`0x88C`) | `+0x55B` = 3, `+0x55C` = `0x18`, `+0x4E8` = 0 |
| 5, 6, 7, 8, `0x1C` (out of range) | `0055D978` | the Yes/No box at `0055D77C`, code by node `+0xB`: 1 → 6, 2 → 7, 3 → 8, else `[node+0x30] = 0x1E` → `0x1C`, else 5 (`0055D73A`–`0055D774`) | 5 "Obtain …?" (`0x860`); 6 "Only one character can obtain this license. Obtain …?" (`0x861`); 7 "Each character can obtain up to three quickening licenses … Learn …?" (`0x863`); 8 "Only one character can obtain the license for this Esper. Obtain …?" (`0x864`); `0x1C` "You will be unable to return to the License menu until you confirm your new board. Proceed anyway?" (`0x88D`) | **Yes (`b = 1`, `0055D978`)**: the counter update `002526F0`/`002527B0`, `BattleStats_SetLicenseNodeStateByStatsIndex(member, node, 1)` (`0055DA6E`), the refresh, `+0x570` bit 5 when a new Mist ability appeared, `+0x55E` = 1; **No**: `+0x570` bit 2 cleared, bits 6–7 set (`0055DAE5`–`0055DB06`) |

So of the 18 slots, eight carry the board's own notices and the rest share the arm that is really the Yes/No box's
out-of-range path; node select and cursor moves arrive on ids 10 and 12, not here.

**The three draw children are the layers of the board chooser `00557DB0`.** Its construct arm marks in `+0x364` the
boards any of nine members holds (selectors A and B, `00558081`–`005580D6`), keeps the selected board at `+0x358` and
the wheel angle `+0x350 = 30 × board`, and installs all four children centred on the screen (`005581AC`–`005581D7`).
Their art comes from the screen root's loads — `lic_bk` into root `+0x100`, `lic_8_c2` into `+0xF0`, `lic_8_c3` into
`+0xF8` (`00561679`–`00561765`) — which `00557DB0` copies to its `+0x150`/`+0x140`/`+0x148` (`00557FFE`–`0055802F`):

| child | art | what its id-4 arm draws |
|---|---|---|
| `00557760` | `lic_8_c2`, `lic_8_c3` (`005579D2`–`005579EE`) | **the backdrop disc**: ten `005574C0` passes, each drawing one sub-image four times with flip modes 4, 5, 6, 7 (`005575CB`–`00557721`), at y offsets 0, +3, +0x18, +4, +2, 0, 0, 0, −2, −3; the flagged passes draw in `0x50000000` — a translucent shadow (`005575A6`) |
| `005565E0` | `lic_bk` (`00556986`) | **the twelve board emblems**: 12 sprites at 90°, 120° … 420° (`00556695`, `005568DB`–`005568EB`) on radius `LicenseBoardBallLength × 0.8`, sub-image group 3 for a board some member holds (`00556763`), group 2 otherwise |
| `0055A340` | `lic_8_c3` (`0055A796`) | **each member's face beside the board(s) the member holds**: per board the member list `005587E0` builds at `+0x16C + 0x28 × board` (count at `+0x190 + 0x28 × board`), angle `90 + 30 × board` plus a small spread (bytes `00D23088`), radius `(LicenseBoardBallLength + LicenseBoardFaceLength) × 0.8`, the fourth face on pushed out by `LicenseBoardBallFaceSecondOffsetY × (index / 3)` (`0055A5C2`–`0055A5E6`) |

All three answer id 25 with `002472A0(self, [owner+0x34C], 2)` and pass `−[owner+0x34C]` into their draws
(`0055661C`, `0055A385`, `0055758C`), so the wheel turns as one piece. Which pixels each sub-image holds was not viewed.

## 9. The layout-key readers

*(2026-09-14, FRONTIER — LAYOUT-KEY-READERS.)* The `LicenseBoard…` keys all position the board's
node-ball layer — the moving "ball" is the cursor/highlight sprite the screen draws over the grid.
`LicenseBoardBallLength` is read in every reader: it is the ball's pixel size, converted to float for
the render math.

| reader (→ owner) | keys | what the values do at the use site |
|---|---|---|
| `005565E0` P (board pane, installed by `005572B0`) | `LicenseBoardBallLength` | `movd xmm7` — the ball size enters the pane's float render state (`005566A9`) |
| `005569F0` P (board pane, `005571F0`) | `LicenseBoardBallLength`, `LicenseBoardNameNoSelectSize`, `LicenseBoardBallNameOffsetY` | `BallLength` → `xmm9` render scale (`00556AAD`); `NameNoSelectSize` → `xmm8`, the unselected node-name scale (`00556A9B`); `BallNameOffsetY` subtracted into the name Y before `00861F08` trig placement (`00556BBB`) |
| `005588C0` (→`00557DB0`, the cursor handler) | `LicenseBoardBallLength`, `LicenseBoardBallEffectOffsetY` | `eax = BallLength − BallEffectOffsetY`, floated and scaled by `1/5`-style factors — the ball's selection-effect Y offset (`00558905`) |
| `0055A340` P (board pane, `00557430`) | `LicenseBoardBallLength`, `LicenseBoardFaceLength`, `LicenseBoardBallFaceSecondOffsetY` | `ecx = BallLength + FaceLength` — the two-segment span of the face display (`0055A3CC`/`0055A3D2`); ~~`BallFaceSecondOffsetY` `imul` into the per-second hand offset (`0055A5E6`)~~ **Corrected 2026-09-29 (FABLE, GI-3):** `BallFaceSecondOffsetY` is multiplied by `index / 3` (`0055A5C2`–`0055A5E6`): the push-out of the **second row** of member faces beside a board (§8a) |
| `00558FB0` P (tile/panel window) | `BlackBandAnimTime` | `r8d` = band animation ms → `002C9060`/`002C9890` (the standard band triple, `0055915C`) |
| `00561390` P (screen root) | `BlackBandAnimTime` | same band-anim feed on the root's fade (`005615D0`) |
| `0055E9E0` (→`0055CD40`, the board view) | `NaSPArtSignalOffsetX`, `NaSPArtSignalOffsetY` | `edx − OffsetY`, `ecx = OffsetX` → `0029E770` — the signal sprite the board draws (`0055EDA0`, `0055EDA6`) |

## Falsification pass

**Pass 1 — 2026-09-14 (OPUS).** Attacked at parent `GN160` (`fa0db293…`), EXE `73461d08…`.
Instrument: `Tools/work/OPUS/falsify_licenseboard.py`. **Three claims attacked, three survived. No
correction.**

The spine of this page is its procedure tree, and each of its ten rows makes three separable claims:

| claim | the killer | result |
|---|---|---|
| each row is installed by the procedure the page names | a named installer with **no** rip-relative `lea` of its procedure | **survived — 10 of 10**, decoded from the image |
| the ten subtree sizes match the menu screen atlas the page cites as its source | any row differing from the atlas | **survived — 10 of 10** |
| the page's installer for each row is the atlas's installer | page and atlas naming different installers | **survived — 10 of 10** |

**The third is the one worth having.** This page states that its membership comes from
`../Menu-Screen-Atlas/members/ui_atlas.tsv`; a disagreement between the page and that file would be
a defect in one of them, with the image to break the tie. There is none — **and the installers the
two agree on are the ones the image confirms**, so all three legs meet.

> **One thing this pass found that is not this page's claim.** The atlas's `message_ids` for
> `00557DB0` — the cursor/input widget in this tree — lists only **id 10**, while the body answers
> **1, 2 and 10**: `sub ecx,1 / je 00557FD3`, `cmp ecx,1 / jne 005585A0` (the fall-through is the
> arm), and `cmp ecx,0xa / je 00558261`. **That is a row of the atlas, not a sentence of this page**,
> so it is routed to the atlas's owner rather than corrected here.

**Not attacked by this pass:** the dispatch arms and field semantics of the individual widgets, the
`licd` grid build and the change sweep (both owned by
[the sibling page](the-license-board-grid-build-and-its-change-sweep.md)), and the shared-helper
families the page cites to their existing member TSVs rather than re-reading.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — SERVICE.** A cited function calls `BattleStats_RecomputeDerivedStateAndAutoStatuses`.
- **Input - CLIENT and SERVICE (23 edges).** `001976E0`, `001976F0`, `00229DF0`, `0024A680` are called by bodies filed to Input: `001E0A40`, `001E0A70`, `001E0CE0`, `001E0D30` (+4 more); `001E0A40`, `001E0A70`, `002AEB20`, `002B7B80` (+6 more) reach bodies filed to Input: `001976E0`, `001976F0`, InputManager_GetSingleton (`00198790`), `001E0A10` (+9 more) - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (29 edges).** `00249210`, `002493D0`, `0024A4E0`, `0024F410` are called by bodies filed to Resource: `00249180`, `00249320`, `00249350`, `00249380` (+6 more); `00249210`, `002493D0`, `002B7B80`, `002BAF80` (+5 more) reach bodies filed to Resource: `00249210`, `002493D0`, `00249580`, `0024A4E0` (+7 more) - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (2 edges).** `00249210`, `00249580` are called by bodies filed to SaveLoad: `00582790` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT (16 edges).** `00244DD0`, `00247510`, `00247870`, `002497E0` (+3 more) are called by bodies filed to Save_Load_Settings: SaveWrite_OperationStateCallback (`0057E4D0`), `0057E950`, `0057EBB0`, SaveLoad_FullImageStorageCompletionCallback (`00580840`) (+7 more) - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (1 edge).** `0024A680` is called by bodies filed to World: `003C63A0` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (4 edges).** BattleEncodedId_DispatchQueryMode0Value (`00309EC0`) is called by bodies filed to WorldAreaField: `00576A50`; `002B7B80`, `002BAF80`, `00324470` reach bodies filed to WorldAreaField: FieldData_GetActiveFieldRecordBit15 (`00313F60`), WorldTransition_GetActiveOrPendingFieldId (`003148F0`) - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - MECHANICAL (3 edges).** all 3 edges are spawn-lifecycle bodies (`Spawn_ValidateCandidateDistanceToPlayers` `00234DA0`, `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0`, `SpawnKeep_RotatePersistenceBanksForAreaTransition` `00233780`) calling the shared accessors `FieldData_GetActiveFieldRecordBit15` (`00313F60`) and `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) - fan-in on two accessors.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (11 edges through 6 of this page's functions).** The ActorEntity layer reaches this page at `00263990`, `002B7B80`, `002B58B0`, `00316DF0` and 2 more. `BattleUnit_ApplyUnitDefinition` is the worked example, read in full - it is the definition apply, and the split is the id: **`definition >> 8`** chooses the authored table while **`definition & 0xFF`** indexes it, which is the same high-byte/low-byte division the record initialiser uses; **4 of the 10 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — CLIENT.** `AiOrder_EvaluateTargetSelector`, owned by that layer, calls `00309EC0` on this page. That caller is the selector evaluation, 6,963 bytes of it: it indexes its table at a **six-byte stride** and takes a word at `+6`, two bytes at `+8` and `+9` and a signed word at `+0xA` before deciding anything; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleStats_InitializeDefinitionRecord`, owned by that layer, calls `00323910` on this page. That caller is the `0x1C8`-byte record initialiser, and it states the sentinels: `qword[+0x50]` becomes `-1`, `word[+0x58]` and `word[+0x1C3]` become `0xFFFF` and `byte[+0x1C5]` becomes `0xFF`, after which the definition id's **high byte** selects which authored table its low byte indexes; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — mixed (9 edges).** `00282A40` (ItemsEquipment boundary) calls `0031C5D0`; `00300B80` is also called by `00316DF0`/`00323540`; `00317930` calls `00309EC0` — the license/item accessor family the grid consults is itself consumed by gameplay code, and its callees reach the same gameplay accessors.

**Script_VM_Native_Bridge — CLIENT (6 edges).** The `002Dxxxx` control helpers this page cites (`002D66A0`, `002D7760`, `002D7B40`, …) are also called by script-bridge bodies `005116E0`/`00511A10`/`00511850`/`005117B0` — the shared menu-control layer serves the script-facing screens too.

**PlatformOnlineAchievements — CLIENT (2 edges).** `00282FA0` (achievements boundary) is also called by `003162E0`/`00316760` — the same accessors the LP/trophy display path uses.

**Rewards_Progression_Economy — CLIENT (2 edges).** `00300B80` is also called by `003F4AA0`/`00319920` — the license/item accessor is shared with the LP/economy read path.

**Party — CLIENT (6 edges).** `00316DF0`/`00323540` (the license accessors' callers named above) are themselves called by party-side bodies `00326110`/`003172E0`/`00329080` — the accessor family is shared between the party screens and the board.

**Presentation — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 221 edges measured).** The widgets
this page maps are *drawn* by the render layer: the `Presentation.UI.InputConsumerStateMachine`
bodies `002BAF80`/`002B7B80` and `Presentation.UI.Quest.ListScreenSelectionStateMachine` `00579420`
(interior read 2026-09-17, SWE2-FRONTIER: 1,307 B — `002432B0` first at [`00579490`](../../_index/ADDRESS-INDEX.md), `00247870` ×3 + `005791B0`/`0037E760`/`00247930` ×2 — a state-machine body dispatching into the widget family)
call the widget bodies (`00246AC0`/`002470D0`/`00244DD0`/`00247510`/…), and the page's text helpers
(`0017F7C0`–`0017FD30` glyph-run emitters) sit inside the shared `Presentation.Text.*` family —
`003649A0` (glyph-run quad emission), `002AAE40` (glyph-run width batch split), `00364530`
(non-drawing advance), `00366110` (brace-tag markup), `002B0280` (ShaderMaterial, 27 edges),
`002DB080` (ScreenCapture) and `RenderCommand_SubmitCurrentBufferAndSwap`. The crossing is the draw
path the widgets live on, not a second owner.

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 34 edges measured).** 26 edges are
the image-pointer fixup pair `0020E600`/`0020E620`; the rest are the frame-mode getters
`00229D20`/`00229DF0`/`00229E70`/`00229EA0` and the `001EDDA0` frame helper — mechanical
infrastructure every screen body carries.

## Evidence-only read — frontier hub `002CA150` (2026-09-18, SWE2-EC7)

`002CA150` — 154 B, 8 A-measured callers; the `[0209AC30]+0x2D8` record rebuild. Read against
the shipping image (page stays PARTIAL — evidence-only): any existing record at
`[0209AC30]+0x2D8` is released via `00244F00` (`002CA18E`), a fresh `0x140`-byte record is
built by `00244F50` from the inline template at `002CA1F0` — the `lea rdx,[rip+0x3A]` at
`002CA1AF` points just past this function's own end — with the `{0, arg1, arg2}` stack block
as parameters, the new pointer stores back to `+0x2D8` ([`002CA1B6`](../../_index/ADDRESS-INDEX.md)–`002CA1C5`),
and `00246AD0(0208EA28, rax)` registers it. Same `[0209AC30]` band state record `002C9490`
writes.
