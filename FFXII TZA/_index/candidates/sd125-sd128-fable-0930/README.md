# SD-125 and SD-128 answered: the command menu's bit 0x4000 means "the top command list is open", and 002C7660 is the per-unit overhead-display evaluation (FABLE helper for FABLE, Claude Opus 5.5, 2026-09-30)

Static reads of the shipping exe (`73461D08…`). Nothing was launched. The image was read at HEAD `96ed44563`; this
directory is untracked. Scripts and outputs:
- [`sd125_senders.py`](sd125_senders.py) → [`sd125_senders.out`](sd125_senders.out): 35 PASS, FAILS 0.
- [`sd128_read.py`](sd128_read.py) → [`sd128_read.out`](sd128_read.out): 28 PASS, FAILS 0.

Each script has positive controls: a known sender, caller or reader must be found by the same sweep.

---

## SD-125: what `+0x2FF0` bit `0x4000` means and who sets it

**Row question:** "What the command-menu widget's `+0x2FF0` bit `0x4000` means, and who sets it."
**Verdict: ANSWERED (static).**

### The setter (correcting the 2026-09-30 narrowing)

The bit is set and cleared only in `002778C0`'s **message-31 arm** (`00279187`). The narrowing also named message
arm 2 as a path. That was an instrument artefact.
- **One path.** On the dispatcher's control-flow graph, only arm 31 reaches `002795AE` at all. Its jump tables are
  read to their `cmp` bounds. At `002795AE`, `r12` is defined only by `002778EC mov r12, rdx` (the message) and
  `rdi` only by `002791A7 mov edi, 1` (P2, P3).
- **Where the arm-2 path came from.** `sd125_reachdef.py` reads a jump table until a target leaves the function. The
  inner table at `00278D86` has 8 entries (`cmp eax, 7`). Read that way, it continues into the next table, `00279E04`.
  That table's targets `0027956B`–`00279595` fall through to `002795AE`. The extra edges are what made arm 2 reach
  the test and `00278A5B` look like a definition of `rdi` (P5b reproduces this).
- **What the arm does.** It stores the first parameter's low word as the dispatcher's window kind (`002791A1` /
  `002791AC` → `+0xD8`, the word `0027DED0` sizes the window from, P7). It sets the parent's bit `0x4000` when that
  parameter equals 1 (`002795AE`–`002795B5`) and clears it otherwise (`002795C2`). `r15` is the parent menu widget
  `[+0xD0]` (`002778EF`).

### What the bit means

The bit means **"the window kind the dispatcher last opened is 1"**. In `0027E050`'s table (indexed kind − 1,
`0027E06B`), kind 1 stores list code 6 (P7). List code 6 is the top-level battle command list: Attack, Magicks &
Technicks, Mist, Dismiss, Gambits, Items (UQ-68 W9). Message 31 is the dispatcher's "open window kind k" (UQ-68 W5).
So the bit is set while the top command list is the open window, and clear in every sub-list.

### Who sends message 31, and with what parameter

The census is image-wide (P4): a raw sweep for the imm32 31 decoded back to instruction boundaries, register-sourced
stores, and static records. The controls find id 30's `00278CE8`, the six known id-31 builds, and the `{18}` record
`00915070`. It finds **13** id-31 builds (P5):

| site | sender | receiver | first parameter (`+8`) |
|---|---|---|---|
| `0027A5D3` | controller `00279E20`, its **message-2 arm only** (P6) | the menu child it has just built and attached, through the subtree broadcast `002753F0` (`0027A5DA`, `rcx = rdi`) | `(i64) word [controller + 0x61B8]` (`0027A5B6`) |
| `00278882` | dispatcher → itself (`call rax`, `rcx = rsi`) | dispatcher | **forward:** `0027C3D0`'s next kind (`00278423` → `00278559` → `002785F0`). **Back:** the kind saved on the navigation stack, `[[+0x2FE8] + 0x70 + depth*4]` (`00278860`) |
| `00277C9B`, `00278030`, `00278212`, `00278F80` | dispatcher → itself | dispatcher | its current kind, `movsx word [rsi + 0xD8]` (re-opens) |
| `002BB7C4`, `002BBA0B` | `002BAF80`, the location-map page (its own widget, `002BAFC4 mov r14, rcx`) | its **ancestors** (`00275440`, which starts at `[rcx+0x10]`) | **1** (`00915BB0`) |
| `005541CD` | `00553F40` (world map) | ancestors | **0**: the record still holds 1 from the `{34}` send, but the shared tail `0055423A` zeroes `+8` before `00554249` |
| `003CA245`, `00551E32`, `00551F3D` | `003CA200`, `00551E00`, `00551F00` | object `[global]+0x2A0` / ancestors | 0 |
| `00832417` | `00832390` | `0085E680` | not a widget record (`[rcx+8] = 0x1F`) |

**The controller's word `+0x61B8`** is the kind the controller opens the menu at. It has three writers (P6):
- `0027670D` sets it to **1** when `00276650` builds the controller (`r14d = 1` from `002766A3`, P6).
- `0027A793` is the controller's message-33 arm. It stores the message's first parameter (`0027A78E`).
- `0027A6F0` zeroes it after each open (`rsi = 0` from `0027A058`).

**Message 33 senders, and what they pass (P4b, P6b):**
- `0027AA70` sends **`{33, 1}`** at both its sends, `0027AB88` and `0027AC65` (`00915BB0`). Its widget is built in
  the controller's child slot and attached under the controller (`0027A369`–`0027A3B7`, P6b).
- The dispatcher sends `{33, k}` up after opening kind k (`002788C0`). Its `+8` is the same `rcx` the 31-send carried.
- `0027B430` sends `{33, 0027C730's result}`.

**So parameter 1 reaches the dispatcher in three ways:**
1. The controller opens the menu while `+0x61B8` = 1. That holds when the controller is first built, and after
   `0027AA70`'s `{33, 1}`.
2. Backing out restores a saved kind 1.
3. A re-open happens while the top list is current.

Whether `0027C3D0`'s forward path can return 1 is not read. It does not change the meaning, because the receiver
decides the bit.

**Foreign senders.** Outside the battle-menu family, only the location-map page `002BAF80` builds `{31, 1}`. It sends
it up its own parent chain.
- The attach census is a raw rel32 index on `00244960` / `00248220`, 108 sites (P9). It shows the dispatcher attaches
  only its two `0027AD70` windows (`00277A25`, `00277A34`). Each window attaches only its `002D14E0` list
  (`0027AEC3`).
- **Limit:** a map page beneath the dispatcher is not excluded beyond that census. Inference: it is not there.

### What the bit does in play

The bit is read once, in the menu widget's **message-2 arm** `00276FA0` (GENERATION RECONCILE, every frame, P8).
After the `001EDEC0(+0xB4)` gate and the bit-8 early-out:
1. `r14d = 00253BA0()`, the effective force-fight flag. It is 0 while the party is FLEEING
   ([force-fight page](../../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md) §1).
2. Bit `0x4000` forces `r14d = 1` (`00276FF2 cmovne`).
3. `r14d = 0` goes straight to the close (`00277034 je 0027704E`): set `+0x2FF0` bit `0x200`, then call the destroy
   entry `00244F00` on the menu.
4. `r14d ≠ 0` closes only when bit 17 is clear and the `00254550` / `002878A0` / `00228480` gates agree, or when the
   member slot's flags byte `& 9` is set.

**Reading (static, inference on the player-facing words):** while the party is fleeing, the battle command menu
closes itself unless it is on the top command list.

**Not read:** the `001EDEC0` gate and the three gate functions; the member flags bits; whether `0027C3D0` can return 1.

### Proposed register status (SD-125)

> **ANSWERED 2026-09-30 (FABLE, static; record [`sd125-sd128-fable-0930`](README.md)):** bit `0x4000` means "the battle command dispatcher's open window is kind 1, the top command list" (list code 6: Attack, Magicks & Technicks, Mist, Dismiss, Gambits, Items). Its only writer is `002778C0`'s message-31 arm (`00279187`), the "open window kind k" message: it stores k as the window kind (`002791AC` → `+0xD8`) and sets the bit when k = 1 (`002795AE`–`002795B5`), clearing it otherwise. *Correction to the narrowing:* message arm 2 does not reach `002795AE`; that path, and `00278A5B` as a definition of `rdi`, came from reading the 8-entry table at `00278D86` past its bound into `00279E04` (`sd125_senders.py` P2, P5b). Senders of `{31, k}` (image-wide census, `sd125_senders.py` P4/P5, FAILS 0): the controller `00279E20`'s message-2 arm opens the menu at its word `+0x61B8` (`0027A5D3`). That word is 1 when `00276650` builds the controller, takes the parameter of each `{33, k}` (arm `0027A78E`, e.g. `0027AA70`'s `{33, 1}`) and is zeroed after the open. The dispatcher re-sends to itself the current kind, the kind restored on Back, or `0027C3D0`'s next kind. Outside that family only the location-map page `002BAF80` builds `{31, 1}`, and it sends it up its own parent chain. In play: the menu's per-frame message-2 arm (`00276FA0`) treats a set bit as force-fight on (`00276FF2`). With the effective flag 0 (FLEEING) and the bit clear, it closes the menu (`0027704E`: bit `0x200` + `00244F00`). So while fleeing, the command menu closes itself unless the top list is showing.

### Page and box sentences that would change (SD-125)

- `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`, row SD-125. The whole status cell is replaced by the paragraph
  above. It currently reads "**OPEN 2026-09-30 (SWE2-DATA), static:** *Narrowed 2026-09-30 …* … the reaching paths
  are message arm 2 (GENERATION RECONCILE) and private arm 31 (`sd125_reachdef.py`) … which sender passes parameter
  1, and so the bit's meaning in play, is open. …"
- `Database/FFXII TZA/16-UI/the-selection-the-menu-publishes.md`:
  - **Line 176 (box).** Currently "- [ ] What `+0x2FF0` bit `0x4000` means and who sets it: … *(Narrowed 2026-09-30
    … `rdi` = 1 from `00278A5B` / `002791A7`, the only definitions reaching there) … the reaching paths are message
    arm 2 (GENERATION RECONCILE) and private arm 31 …)*". It becomes `[x]` with the answer.
  - **The correction.** Strike "`00278A5B` /" and "message arm 2 (GENERATION RECONCILE) and" as an instrument artefact.
  - **Line 153.** Currently "`+0x2FF0  u32  flags: bit 8 early-out, 0x200 set on accept, 0x4000 forces the
    force-fight flag (id-2 arm)`". Proposed: "… `0x4000` = the dispatcher's open window is kind 1 (the top command
    list), set by `002778C0`'s message-31 arm; read by the id-2 arm as force-fight on".
  - **Line 4 (status).** Currently "… and what +0x2FF0 bit 0x4000 means (SD-125) are open …". Move SD-125 to answered.
- `Database/FFXII TZA/_index/candidates/sd124-125-menu-fable-0930/README.md` is a committed record and stays as
  is. Its "rdi = 1 … `00278A5B`" and "message arm 2" lines are superseded by this record, which carries the correction.
- **Optional, UQ-68 record limit.** "A message-31 sender outside the family that reaches this widget by another route
  is not excluded". This census narrows it: outside the family, only `002BAF80` builds `{31, 1}`, and it sends upward.

---

## SD-128: what `002C7660` is

**Row question:** "What `002C7660` is, the parent of both the HP-gauge colour path and the overhead-status path."
**Verdict: ANSWERED (static).**

### Shape and caller

- **Extent.** 1,190 B. It decodes to one `ret` at `002C7B05`, with no indirect jump and no jump table (R0).
- **One caller.** The raw rel32 index (with a rip/imm scan and relocations) finds one caller: `002C632F` in
  `002C62B0`. Its address is taken nowhere. Control: the same index finds `0028EDAD` → `002C62B0` (R1).
- **What drives it.** `002C62B0` is called by the menu draw `0028EAB0` under draw-layer bit 2 (`0028ED7E`) on the object
  `hud = [[0209BE80] + 0x10F80]`. It calls `002C7660` once per node of the linked list at `[hud + 0x1D70]` (next at
  `+0x18`).
- **Arguments (R2):**
  - `hud`, then `node`.
  - Three pass-through contexts: `r8`, `r9` and arg5.
  - arg6 is never read.
  - arg7 = `(002E0FA0() >> 10) & 1`, which gates the gauge/status pair.
  - arg8 = the focus unit, `003588B0(003590D0())`.
- **The node.** Each node is keyed by a packed actor handle at `+0x10`. The function also reads node `+0x14`, `+0x17`,
  `+0x2C` and `+0x2E`. It is **not** the 0xC0 StatusView record that `00329220` builds: none of that builder or its
  four callers is called, and the StatusView's `+0x10` is a name pointer (R10).

### What it computes, per node (= per unit with an overhead display)

1. **Level (fade).** `(int)(00272DE0(handle) × ((word hud+0x1D78 × byte node+0x14) >> 7))` (R3).
   `00272DE0` is 0.0 for an unresolved unit, else `002E7E90(unit)`.
2. **Unit and class.** The unit is `[022C8700 + node+0x2E × 8]` (`0035D4F0`), and its class nibble comes from
   `00263C20` (R4).
3. **Placement mode and float f.** Both come from `002ED0B0` (mode 1, f = 0 without a model) (R5). Mode 1 is forced
   when the unit is the battle-menu focus handle `022C806C`. Under `0037C8F0()` this applies only for class ≠ 8, and
   it then also arms the element init when `00273460()` (the first accepted member with flag bit 2) is non-zero.
4. **Anchor offset V.** In mode 2, `V = f × normalize(02AED5F0 − node position)`; otherwise V = 0 (R6).
5. **Gauge kind.** 0 for a unit that is one of the battle menu's accepted members (`00273320` ≥ 0) (R7). Otherwise:
   - class 1, 2 or 7 → 1 or 2 (`00322950`);
   - class 3 or 8 → 0 or 2 (`003229A0`, stats `+0xE9C` bit 0);
   - any other class → −1, which means no gauge and no status.
6. **The four element calls (R8):**
   - `002C8920`, the element init.
   - **`002C8310`, the HP gauge.** It is called when arg7 = 0, kind ≥ 0, node `+0x17` bit 1 and `hud+0x1D7A` bit 0 all
     hold, and receives the kind. This is the path to the `HpGauge{Enmey,Other,Side}` colour lerp `002C5F90`.
   - **`002C7B10`, the overhead status.** Same gate without the hud bit, which it receives as an argument. This is the
     path to the `OverHeadStatus*` keys in `002C84E0`.
   - `002C8820`, the scaled emit, called when node `+0x2C` ≠ 0.
7. **The label slot (R9).** If one of the two 0x1C0-byte draw records at `hud + 0x1800 + i × 0x1C0` is active for
   this handle:
   - **Position.** Copied from the node, or from `002E9A90(handle)` when flag bit 3 is set.
   - **Distance scale.** From the focus unit, with `R = hud+0x1D7C`: 1.0 within R/3, 0.8 beyond R, and linear between
     (continuous at both ends).
   - **Text size.** The text extent of `+0x1930`, times the scale, stored as size and as a centring offset.
   - **Level.** Stored too, plus an optional font-metric y shift (flag bit 2).
   - `002C62B0` then appends each active slot to its draw list (`003F14D0`).

**So `002C7660` is the per-unit overhead-display evaluation.** For each unit in the overhead manager's list, it
computes the display's fade level, anchor and gauge kind. It runs that unit's HP gauge, status numbers and element
emits, and lays out its name label. The old label "display-record channel evaluation" fits neither half: there is no
per-channel loop, and the record is not the StatusView.

**Not read:** what builds the `+0x1D70` nodes; `002ED0B0`'s model branch `003E4EA0` (what modes 0 and 2 mean); the
class nibble values' names; `00322950` / `003229A0` beyond their bodies; `002C8920` / `002C8820` beyond the
unit-display page.

### Proposed register status (SD-128)

> **ANSWERED 2026-09-30 (FABLE, static; record [`sd125-sd128-fable-0930`](README.md), `sd128_read.py` FAILS 0):** `002C7660` (1,190 B, no jump table) is the per-unit overhead-display evaluation. Its one caller `002C62B0` (raw call index, control `0028EDAD`) calls it from the menu draw `0028EAB0` (layer bit 2) for each node of the `[[0209BE80]+0x10F80] + 0x1D70` list, each node keyed by a packed actor handle at `+0x10`. Per node it computes a fade level (`00272DE0(handle)` × `hud+0x1D78` × node `+0x14` >> 7), a placement mode and anchor offset (`002ED0B0`; mode 1 forced for the battle-menu focus handle `022C806C`) and a gauge kind (0 for an accepted battle-menu member, else 1/2/0/−1 by class nibble). It then calls the element init `002C8920`, the HP gauge `002C8310` (→ the colour lerp `002C5F90`), the overhead status `002C7B10` (→ `002C84E0`) and the scaled emit `002C8820` under the gates `sd128_read.py` R8 lists. Last, it lays out the unit's name label in one of two 0x1C0-byte draw records at `hud+0x1800`: distance scale 1.0 → 0.8 over R/3..R from the focus unit (R = `hud+0x1D7C`), scaled text extent and centring. It neither builds nor reads the 0xC0 StatusView record, so the "display-record channel evaluation" placement on the unit-display page is call-signature only.

### Page and box sentences that would change (SD-128)

- `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`, row SD-128. The status cell is replaced by the paragraph above. It
  currently reads "**OPEN 2026-09-30 (SWE2-DATA), static:** *Narrowed 2026-09-30 …* `002C7660` has a label and a
  page … what remains is a fuller read. It calls `002C8310` and `002C7B10` … it has no label and no page." (The cell's
  last sentence also contradicts its own narrowing.)
- `Database/FFXII TZA/16-UI/Battle-Hud/the-battle-hud-layout-readers.md`:
  - **Line 59.** Currently "`| 002C7660 | the unlabelled parent of the HP-gauge and overhead-status paths |`".
    Proposed: "the per-unit overhead-display evaluation (one call per `[hud+0x1D70]` node from `002C62B0`): fade
    level, anchor, gauge kind, then the HP-gauge and overhead-status paths and the name-label layout".
  - **Lines 121–126 (box `- [ ]` … **SD-128**).** It becomes `[x]` with the answer.
  - **Line 4 (status).** "… and the 002C7660 parent (SD-128) are open". Move SD-128 to answered.
- `Database/FFXII TZA/04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md`, line 296 (residual
  placements row). Currently "`| 002C7660 | 1190 | display-record channel evaluation (caller 002C62B0): [rcx+0x1D78]
  context, 0035D4F0 getter, …`". Proposed: re-label as the per-unit overhead-display evaluation, and add that it does
  not read the 0xC0 record this page documents. Better still, move the row to the battle-HUD page.

---

## Instrument notes (for the kit, not for the pages)

- **Table bound.** `sd125_reachdef.py` (`sd124-125-menu-fable-0930`) reads jump tables "until a target leaves the
  function". With two adjacent tables, that adds false edges. `sd125_senders.py`'s `jump_table()` takes the bound from
  the preceding `cmp`/`ja`, and the byte map when there is one.
- **Word stores missed.** `tk.disp_refs(0x61B8, 0x61BA)` returned the three 66h-prefixed word stores (`0027670D`,
  `0027A6F0`, `0027A793`) only in its raw-unverified list, so a writer census through it reads "0 stores". P6 uses its
  own boundary-checked decode (`disp_sites`), with `0027A5B6` as the control.
- **Payload by path.** A payload read off a fixed window around the id store mis-assigned `005541CD` (it found the
  `{34}` payload 1). `consumer()` now follows the taken path to the send and takes the last `+8` writer on it.

---

## Publish staging (FABLE helper, 2026-09-30)

The apply is `Database/Tools/work/FABLE/sd125128/apply_sd125128.py`. It anchors once per file, is CRLF-safe and
all-or-nothing, and has `--check`. It leaves the committed sd124-125 record as is.

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`
affected: `Database/FFXII TZA/16-UI/the-selection-the-menu-publishes.md`
affected: `Database/FFXII TZA/16-UI/Battle-Hud/the-battle-hud-layout-readers.md`
affected: `Database/FFXII TZA/04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md`

## Consumer check

- consumer: `_index/OPEN-QUESTIONS.md` rows SD-125 and SD-128: revised-here. The new ANSWERED lead keeps the old status after *Was:*. SD-125's lead states the correction to the narrowing.
- consumer: `16-UI/the-selection-the-menu-publishes.md`: revised-here.
  - The status line and the `+0x2FF0` field note change.
  - The SD-125 box is ticked and answered.
  - Two narrowing phrases are struck as an instrument artefact: the `00278A5B` definition and the arm-2 path.
- consumer: `16-UI/Battle-Hud/the-battle-hud-layout-readers.md`: revised-here. The status line, the `002C7660` table row and the SD-128 box change.
- consumer: `04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md` residual-placements row: revised-here. It is re-labelled, and says the function does not read this page's 0xC0 record.
- consumer: `_index/candidates/sd124-125-menu-fable-0930/README.md` (committed record of the narrowing): agrees with the correction recorded here, not edited.
- consumer: `_index/candidates/uq68-kind5-foecraft/README.md` Limits ("A message-31 sender outside the family that reaches this widget by another route is not excluded"): routed-to its owner (FABLE, UQ-68). The census here narrows it: outside the family, only `002BAF80` builds `{31, 1}`, and it sends upward. The record is not edited.
- consumer: `16-UI/Widget-Object-Model/the-widget-message-protocol.md` (message 30/31 shapes): agrees; nothing to change.
- consumer: `00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md` (the effective-flag reader and the flag polarity): agrees; nothing to change.

## Regression

run: sd125_senders.py at cea938e19 (FAILS 0, 35 PASS)
run: sd128_read.py at cea938e19 (FAILS 0, 28 PASS)

The battle-HUD page is not clean. It carries an uncommitted narrowing overlay of the SD-128 box from before this
package (` M` in `git status`). The apply anchors match both that overlay and the HEAD text (`--check` passes on both).
Whoever owns the overlay should commit or drop it before the publish.
