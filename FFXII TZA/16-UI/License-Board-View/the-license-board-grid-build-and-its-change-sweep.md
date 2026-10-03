---
system: The License Board view - how the grid is built from licd, and the change sweep that is not in the census
category: 16-UI
status: DOCUMENTED — the grid build, the change sweep, the square layout, its state alphabet and the selection-preview flag are read; UQ-153, UQ-154 and UQ-155 answered 2026-09-17
owner_layer: PrimaryOwner:UI
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: both functions decoded in full; the dimension fields traced to the licd header offsets the
    format page already documents; the displacement census run image-wide over the six fields
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_kind: derivation
  last_pass_state: opus-license-board-view-1 - reached from UD-1. 0055B310, the change sweep, is
    one of the referenced-but-unlisted bodies; its caller 0055BFF0 was already documented and the
    sweep itself was not.
  crossref_clean: false
  reopened_count: 0
---

# The License Board view: building the grid, and sweeping it for changes

> `0055B310` is **not in the function census**. It is reached by a tail `jmp` from `0055BFF0`, which
> the encoded-id page already documents - and it is the routine that decides which board squares
> changed this frame.

## 1. The grid comes from `licd`'s own header

`0055B3F0(view)` builds the runtime grid, and where it gets the dimensions settles what this object
is:

```
0055B40C  ecx = [view+0x160]                  ; a party/character key
0055B412  rax = 00282DF0(ecx)                 ; the character record
0055B429  if [view+0x128] != 0: return        ; already built
0055B436  if !([view+0x570] & 0x400):
0055B442      ecx = byte [rax+0x60]           ; the character's job
0055B446      [view+0x558] = 003236B0(ecx)    ; job -> board index
0055B458  if [view+0x558] == 0xFF:
0055B45C      [view+0x559] = 0 (both bytes at once); return    ; no board for this job
0055B47D  rcx = boardTable[index]             ; 8 bytes per entry
0055B481  rax = *rcx                          ; the licd blob
0055B484  [view+0x559] = byte[blob + 4] + 1   ; width  + 1
0055B493  [view+0x55A] = byte[blob + 6] + 1   ; height + 1
0055B4AA  buf = alloc((w+1) * (h+1))
0055B4B7  [view+0x128] = buf
0055B4BE  memset(buf, 0, (w+1) * (h+1))
```

**`+0x04` is `width` and `+0x06` is `height` in the `licd` header** -
[`the format page`](../../12-Items-Equipment-Shops-License/license-board-grid-format.md) records
exactly that, `24` and `24` in 13 of 13 files. So the view's two dimension bytes are **the board's
own dimensions plus one**, and the byte map it allocates is **25 x 25 for a 24 x 24 board** - a
one-square border.

> **This identifies the object.** A UI-owned view whose grid dimensions are read from a `licd`
> header, selected by the character's job with `0xFF` meaning "no board", is the License Board
> screen.

## 2. What the build does *not* appear to read

After the `memset`, a double loop walks `[view+0x55A]` rows of `[view+0x559]` columns writing into
the byte map at `[view+0x128]`, indexed row-major as `[view+0x559] * row + col` (`0055B4FB`-
`0055B50C`). What it writes comes from an **8-byte pattern table built on the stack**,
`06 04 02 00 / 07 05 03 01` (`0055B419`, `0055B421`), selected by `result & 3` from a call through
`[rip+0x367bb2]` and by `(col + row) & 1`.

**That is a per-square variant index with a checkerboard term - the board's backdrop tiling.** It
does **not** read the `u16` node numbers at `licd + 8`.

> The format page's open question - *"what parses the grid is not known"* - is **narrowed, not
> closed**: the header's `width` and `height` now have a named reader, and the 576 `u16` cells still
> do not. **Routed to that page's owner rather than edited here.**

## 3. The change sweep - `0055B310`, the body the census does not have

`0055BFF0` tail-jumps into it. It walks the **`0x38`-stride cell array at `[view+0x120]`** - a
different pointer from the byte map at `+0x128` - row-major over the same dimensions:

```
0055B313  if [view+0x570] & 1:  [view+0x408] = 0        ; collecting: reset the count
          for row in 0 .. [view+0x55A]-1:
0055B340      base = [view+0x120] + ([view+0x559] * row) * 0x38
              for col in 0 .. [view+0x559]-1:
0055B361          v = [cell+0x18]
0055B365          if ((v >> 4) ^ v) & 0xF0:              ; nibble 1 != nibble 2 -> changed
0055B370              if [view+0x570] & 1:
0055B379                  n = [view+0x408]
0055B380                  if n < 0x20:
0055B388                      [view + n*8 + 0x308] = cell   ; collect the pointer
0055B390                      [view+0x408] = n + 1
                      else:
0055B398                  v = (v ^ (v << 4)) & 0xF00 ^ v   ; nibble 2 := nibble 1
0055B3A6                  [cell+0x18] = v
0055B3AA              changed = 1
0055B3D6  [view+0x570] &= ~1
0055B3DD  return changed
```

**`+0x18` carries a square's state twice, one nibble each** - bits 4-7 against bits 8-11. The test
is whether they disagree; the sync branch copies the first into the second. This is a
**previous-vs-current comparison**, and the collected pointers are the squares whose appearance owes
an update.

| field | what it is |
|---|---|
| `+0x120` | the `0x38`-stride square array |
| `+0x128` | the `(w+1) x (h+1)` backdrop byte map |
| `+0x308` | **32 pointers** to changed squares |
| `+0x408` | how many of the 32 are filled |
| `+0x558` | the board index, `0xFF` for none |
| `+0x559` / `+0x55A` | `width + 1` / `height + 1` |
| `+0x570` | flags - **bit 0 "collect this pass"**, bit 10 (`0x400`) suppresses the job lookup |

`0x308 + 32 * 8 = 0x408` **exactly**, so the buffer and its counter are adjacent and the capacity is
the layout, not a guess.

**Bit 0 is cleared at the end of every sweep**, so a collection happens once per request: whoever
wants the changed list sets the bit, calls, and reads `+0x308`/`+0x408`.

## 3b. The square, its state alphabet and the purchase flags — 2026-09-17 (FABLE)

`0055BFF0`, the sweep the confirm-commit driver calls before tail-jumping into §3, is also the **fill**:
it walks the `0x38` squares row-major and rebuilds each from the `licd` cell and the licence row.

| square | written from | meaning |
|---|---|---|
| `+0x00` | `002B58B0(row +0x18, 0)` | the name text; for a Quickening (kind 2) the job's own name, table `00D230B0` (`0055C224`) |
| `+0x08` | `licd` cell `u16` | the licence id; `0xFFFF` on the border and on hidden squares |
| `+0x0B` | row `+0x22` | kind: 2 Quickening, 3 Esper, else ordinary (`0055C16F`, `0055C257`) |
| `+0x0C` | row `+0x20` | the LP cost, compared with the character's LP `+0xB0` (`0055C492`) |
| `+0x0E` | the id again | the driver indexes 64-byte rows at `[02CA9670]` by it, row 361 as the default (`0055F0C2`..`0055F0E0`) |
| `+0x10` | row `+0x10` | a text pointer; an Esper's is replaced by the name (`0055C284`) |
| `+0x18` | the sweep and the passes below | the state word |
| `+0x20`, `+0x21` | the loop | column, row |
| `+0x22`, `+0x23` | `0055DD70` | transition phase (2 armed) and pending state |
| `+0x24` | the `(w+1) x (h+1)` byte map | backdrop variant (§2) |
| `+0x25`..`+0x28`, `+0x29`, `+0x2A`, `+0x2C` | `0055F010` | a `0x80` parameter, a flag, the countdown, a handle released through `003B2AA0` |
| `+0x30` | row `+0x21` | a category byte; `0x1E` is special-cased (`0055C302`) |
| `+0x34`..`+0x37` | — | written by nothing read here |

**The state word.** Bits 4..7 are the current display state, bits 8..11 the previous one (§3), and bits
12..15 are purchase flags the sweep derives from `BattleStats_CheckLicenseNodeAcquireReason`
(`00323600` picks the character's stats block ~~`02EBF190 + 8 + slot * 0x1C8`~~ `[02EBF190] + 8 + slot * 0x1C8` *(corrected 2026-10-02, OPUS: `02EBF190` holds a pointer — `00323600+0x19` `mov rax, [02EBF190]`, then `00323600+0x20` `add rax, 8`)*, `00323D10` decides):

| reason | meaning (`00323D10`) | what `0055BFF0` does (`0055C504` table) |
|---:|---|---|
| 1 | the node bit is set at stats `+0x194` | both nibbles 5, bits 12 and 13 (`0055C472`) |
| 0 | allowed: an ordinary node, a Quickening below three, an Esper whose summon is obtained, a node nobody else holds | bit 14 when cost is within LP, then bit 15 unless bit 12 (`0055C492`) |
| 2 | a kind 4+ node costing more than the LP | bit 15 unless bit 12 (`0055C4A6`) |
| 3 | already licensed by an active party member (`00324280`, seven slots, byte `+0` bit 3) | blanked: id `0xFFFF`, previous nibble kept (`0055C4CA`) |
| 4 | three Quickenings already (`BattleStats_CountLicenseBits00To17` at or above 3) | blanked |
| 5 | an Esper node `0x12`..`0x1E` whose summon flag `0030B0E0(node + 0xC000)` is unset | blanked |
| 8 | a category-`0x1E` node without flag `0xC01F` | blanked |
| 6, 7, 9 | no character, invalid node, a kind 4+ node that is affordable | untouched |

Then three passes finish the word. `0055E090` walks every owned square (bit 13) and, on each of its four
neighbours that carries bit 15 and not bit 12, clears 15 and sets 12: **eligible becomes adjacent**.
`0055E3F0(view, n, predicate)` raises the current nibble of the four neighbours of every square the
predicate accepts to `n` when it is lower (`0055E499`..`0055E4B6`), skipping `0xFFFF` squares; it runs
with `n = 4` over squares with bit 13 (`00556580`) and `n = 1` over every real square (`00556570`).

**So the nibble alphabet is `{0, 1, 4, 5}`**, exactly the values the driver distinguishes (UQ-153's
narrowing): **0** blank or hidden, **1** a licence out of reach, **4** a licence next to one the character
owns — the state that animates in with transition `0x2E` — and **5** owned. The commit step writes 5 into
the chosen square directly (`0055F641`), and the transition driver `0055F010` copies the pending state
`+0x23` into the nibble when the countdown `+0x2A` reaches zero, clearing bits 4..7 first
(`0055F0FE`..`0055F10B`). Ten nodes, `0x10A`..`0x113`, are blanked outright unless story flag `0x4B9` is
set (`0055C34E`..`0055C369`).

**Bit 10 of `+0x570`** (UQ-155) is the selection preview: copied from the owner's `+0x10C` bit 2, which
the owner sets only while a board is being chosen for a character whose selector is `0xFF`, it makes the
build keep the pre-chosen index in `+0x558` instead of looking the job up (§1).

## 4. What is not known

- [x] ~~**UQ-153.** **What the two nibbles of `+0x18` encode.** They are compared and copied; **no value is~~
      interpreted**, and nothing here says what a square's state means.
      *Narrowed 2026-09-14 (FABLE, UF-1):* bits 4–7 are the current state and bits 8–11 the previous one. The driver
      `0055DD70` distinguishes values 0, 1, 4 and 5, and 4 is the only one that gets transition id `0x2E`. The commit step
      makes both nibbles of the chosen square exactly `0x5` and sets bits 12–13, leaving bits 14–15 as they were (`and eax, 0xFFFFF55F` / `or eax, 0x3550`, `0055F641`–`0055F646`). What each
      value means on the board is computed by `0055BFF0`, which is not read here; 5 = "taken" is a reading and is not asserted.
      ***ANSWERED 2026-09-17 (FABLE): a four-value display state derived from four purchase flags (§3b).** The sweep `0055BFF0` asks `BattleStats_CheckLicenseNodeAcquireReason` (`00323600` for the character's slot, body `00323D10`) for each square and maps the reason through the table at `0055C504`: **1** (the node bit is set at stats `+0x194`) makes both nibbles 5 and sets bits 12 and 13 (`0055C472`); **0** (allowed) sets bit 14 when the LP cost at `+0xC` is within the character's LP at `+0xB0`, then bit 15 unless bit 12 (`0055C492`); **2** (a kind 4+ node costing more than the LP) sets bit 15 unless bit 12 (`0055C4A6`); **3** (already licensed by an active party member, `00324280` over the seven slots), **4** (three Quickenings already, `BattleStats_CountLicenseBits00To17` at or above 3), **5** (an Esper node `0x12`..`0x1E` whose summon flag `0030B0E0(node + 0xC000)` is unset) and **8** (a category-`0x1E` node without flag `0xC01F`) blank the square to id `0xFFFF` keeping only the previous nibble (`0055C4CA`); 6, 7 and 9 leave it untouched. Then `0055E090` turns bit 15 into bit 12 on every neighbour of an owned square, and `0055E3F0` raises the current nibble of the four neighbours of every square with bit 13 to **4** and of every real square to **1**, never lowering (`0055E499`..`0055E4B6`). So the alphabet is the one the driver distinguishes: **0** blank or hidden, **1** a licence out of reach, **4** a licence next to one the character owns (the value that animates in with `0x2E`), **5** owned; bit 12 adjacent and eligible, bit 13 owned, bit 14 affordable, bit 15 eligible but not adjacent. The commit step writes 5 directly (`0055F641`) and the transition driver `0055F010` copies the pending state `+0x23` into the nibble when the countdown `+0x2A` ends (`0055F0FE`..`0055F10B`). Static, bodies read.*
- [x] **Who sets `+0x570` bit 0 and who reads the 32 pointers.** The consumers were not censused.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (UF-2):* **both ends are one function,
      `0055DD70`, and its one caller is the confirm-commit step `0055F3E0` (`0055F651`).** The step first rewrites the
      current square's `+0x18` (`0055F63E`–`0055F64B`). `0055DD70` sets bit 0 (`0055DD7F`) and runs the sweep through
      `0055BFF0` (whose tail `0055C453` jumps into `0055B310`). It re-arms the current square (`+0x22 = 2`, `+0x23` = its
      state), then walks the collected pointers (count byte `+0x408`, list `+0x308`, `0055DDC6`–`0055DE80`). For each
      one it copies the current-state nibble into the previous one and arms a transition on the square: `+0x22 = 2`,
      `+0x23` = new state, `+0x2A` = `0x2E` for state 4, else 0. States 1 and 5 skip the arming; state 0 also sets
      `+0x26`/`+0x27`/`+0x29`. **Nothing else addresses `+0x408` or `+0x308`** in a raw sweep of 0x540000 up to
      0x5A0000 (exclusive) that includes unlisted code ([`members/rawsweep_disp.py`](members/rawsweep_disp.py)). The only
      other hit, `00540B49`, is a float store on a different object.
- [x] **What happens when more than 32 squares change in one pass.** The 33rd is **silently not
      collected** - `0055B380` compares against `0x20` and skips - but `changed` is still returned.
      Whether a caller can observe the loss is not established.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (UF-3):* **nothing is lost, only deferred.**
      The sweep syncs a square's nibbles only when it is not collecting (`0055B377 je 0055B398`). A 33rd square
      during a collecting sweep jumps straight to `changed = 1` (`0055B382 jge 0055B3AA`), and `0055DD70` syncs only the
      collected 32. The overflow square therefore keeps unequal nibbles and is found again by the next sweep. That sweep
      is either the next confirm-commit (collected and animated then), or the non-collecting call from `0055B560`
      (`0055B6BD`, reached from the rebuild `0055DBD0` and from `0055CD40`), which syncs it without a transition. The
      visible effect of a very large change is that some squares animate one commit late or not at all. That is read
      from the code; how many squares a single commit can change was not checked.
- [x] ~~**UQ-154.** **The other 0x30 bytes of each `0x38` square.** Only `+0x18` is touched here.~~
      ***ANSWERED 2026-09-17 (FABLE): the square is filled by `0055BFF0` and animated by `0055F010`, and between them every byte but four is named (§3b).** `+0` the name text (`002B58B0` over the licence row's `+0x18` block; for a Quickening the job's own name from the table at `00D230B0`); `+8` the licence id from the `licd` cell, `0xFFFF` outside the board or hidden; `+0xB` the kind byte (row `+0x22`: 2 Quickening, 3 Esper); `+0xC` the LP cost (row `+0x20`); `+0xE` a second copy of the id, which the driver uses to index the 64-byte rows at `[02CA9670]` (row 361 as the default) for the word it plays when a square turns 5; `+0x10` the row's `+0x10` text, replaced for an Esper by the name; `+0x18` the state word (UQ-153); `+0x20`/`+0x21` column and row; `+0x22` the transition phase (2 armed), `+0x23` the pending state, `+0x24` the backdrop variant from the `(w+1) x (h+1)` byte map, `+0x25`..`+0x28` a parameter set to `0x80`, `+0x29` a flag byte, `+0x2A` the countdown, `+0x2C` a handle released through `003B2AA0`; `+0x30` the row's category byte `+0x21` (`0x1E` is the special case). Bytes `+0x34`..`+0x37` are written by nothing read here. Static.*
- [x] **Whether anything reads the `u16` node numbers at `licd + 8`.** Still open on the format page.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (UF-4): yes, six functions.* The census is
      already on [the grid format page](../../12-Items-Equipment-Shops-License/license-board-grid-format.md) (2026-09-13,
      `OPUS-REQ-LICD-HEADER-READER`); this box predates it.
      - **The readers.** `00328990`, `0055E2C0`, `0055E600`, `00560070`, `0055F830` and `003FC900` read
        `cell(col, row) = [blob + (row × width + col) × 2 + 8]`.
      - **What a cell is.** `003FC900` indexes the licence table `02EBF038` by the cell (`003FC9E8`–`003FC9F0`), and
        `00328990` uses it as a licence id in a class-`0x20` record query (`00328A2D`–`00328A35`). A node number is
        therefore a licence id.
      - **The view's builder** `0055B3F0` reads only the header, which is what this page measured.
- [x] ~~**UQ-155.** **What `[view+0x570] & 0x400` means** - it skips the job lookup and keeps the existing board~~
      index, which looks like "the board was chosen explicitly", and that is a reading.
      *Narrowed 2026-09-14 (FABLE): the bit is inherited from the owner record, and the owner sets it only while a board is
      being chosen for a character that has none.* No register id carries this box, so it is not queued.
      - **At construction** the view proc `0055CD40` copies owner `[view+0x130]` `+0x10C` bit 2 into `+0x570` bit 10
        (`shl eax, 8` … `and eax, 0x400`, `0055CEB2`–`0055CEC6`). When that bit is set it also takes the owner byte `+0x108`
        as the board index `+0x558` (`0055CF73`–`0055CF80`), which is the index the grid build then keeps.
      - **The owner's bit 2 is set in two arms,** `0055D68C` (in `0055CD40`) and `0055F4CB` (in the confirm-commit step
        `0055F3E0`). Both sit on the path where the character's board selector is unset: `BattleStats_GetLicenseBoardSelectorB`
        returns `0xFF` (`0055D641`–`0055D648`), and the same arms set `+0x570` bit 9 and clear or copy owner bit 0.
      - **It is cleared** at `0055D5C8` once the chosen board byte equals `+0x558` (`0055D5A1`–`0055D5C8`), just before the
        view tears itself down.
      - **So bit 10 marks a view re-created during a board choice, showing the board being chosen** rather than the job's
        board. The job lookup is skipped because a character with no board has no job board to look up. The on-screen
        flow is not observed.
      ***ANSWERED 2026-09-17 (FABLE): bit 10 is “the board is being chosen for a character who has none”.** The 2026-09-14 narrowing is the mechanism: the view copies owner `+0x10C` bit 2 into `+0x570` bit 10 at construction and, when set, takes the owner's pre-chosen board byte `+0x108` as `+0x558` instead of the job lookup; the owner sets that bit only on the arms where `BattleStats_GetLicenseBoardSelectorB` returns `0xFF` (`0055D641`, `0055F4CB`) and clears it once the chosen board equals `+0x558` (`0055D5C8`). So the flag marks the board-selection preview, where the grid must show the candidate board rather than the character's job board. Static, bodies read.*

## 5. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| the dimensions come from `licd + 4` and `+ 6`, plus one | `0055B484` and `0055B493`, against the header the format page documents | 1 |
| the board is chosen from the character's job, `0xFF` = none | `0055B442`-`0055B45C` | 1 |
| the backdrop map is `(w+1) * (h+1)` bytes, memset to 0 | `0055B49F`-`0055B4BE` | 1 |
| the square array is `0x38`-stride, row-major | `0055B340`-`0055B356` | 1 |
| `+0x18`'s two nibbles are compared and synced | `0055B361`-`0055B3A6` | 1 |
| the collector holds exactly 32 and counts at `+0x408` | `0055B380`-`0055B390`, and `0x308 + 32*8 = 0x408` | 1 |
| **this object is the License Board view** | the `licd` header match, UI ownership, and the job-indexed board table | 2 |
| the backdrop loop does not read the node `u16`s | it reads only the stack pattern table and a call result - **absence of a read in one function, not image-wide** | 2 |

## 6. Related

- [`../../12-Items-Equipment-Shops-License/license-board-grid-format.md`](../../12-Items-Equipment-Shops-License/license-board-grid-format.md) - the `licd` files, 24 x 24, and the open question this narrows
- [`../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md`](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) - documents `0055BFF0`, the caller
- [`../../99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md`](../../99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md) - where `0055B310` was found

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Story_Event_Quest_Hunt — SERVICE.** `00583D60` on this page calls `PersistentFlag_QueryPrimaryOrAuthoredTable`, owned by that layer. What it reaches is the flag query whose id is masked to `0x3FFF` while **bit 14 selects between the primary and the authored table**; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — consumed by this page (2 edges).** `0055F3E0` and `00560070` call `002D6620`/`002D6680` — the input-read leaves the directional arms share.

**Presentation — consumed by this page (1 edge).** `0055CD40` calls `003B2D80`, the menu-effect registry entry the grid uses for its effect teardown — the same registry family the other menu screens cite.

**Gameplay — consumed by this page (1 edge).** `00328990` calls `0031C5D0` — a shared gameplay-data callee.

**Script_VM_Native_Bridge — CLIENT (1 edge).** `00560070` is also called by `00511F50`, a script-bridge-side body — the helper is shared.

**Save_Load_Settings — CLIENT (1 edge).** `00282DF0` (the character resolver) is also called by `00583D60`, the save/load screen — the same accessor serves both surfaces.

**PlatformOnlineAchievements — CLIENT (2 edges).** `00583D60`, the save/load caller named above, itself calls the achievements accessors `00315390`/`003166F0` — the chain's second hop, not a crossing this page owns.

**ActorEntity — CLIENT (1 edge).** `002B58B0` is also called from the actor-entity layer — the grid build shares the helper.

**CombatAI — CLIENT (1 edge).** `00309EC0`'s encoded-id class dispatch is also consulted from the combat-AI layer.

**CombatAction — CLIENT (4 edges).** `00309EC0` and `0030B0E0` — the mode-0 class dispatch and its booleanized sibling above — are both called from the combat-action layer; the predicates serve the action code, not only the grid.

**Rewards_Progression_Economy — CLIENT (1 edge).** `0030B0E0` is also called from the rewards/economy layer — the same query predicate.

**CoreRuntimeScheduling — SERVICE (6 edges).** The grid sweep's helpers `002418F0` and `00244DD0` call the core runtime's scheduling leaves `00229DF0`/`00229E70`/`00229EA0` and their siblings — engine-side plumbing the screen consumes, not grid-owned machinery.


### Interior citation — frontier hub `0030B0E0` (2026-09-18, SWE2-EC7)

`0030B0E0` — 146 B, 7 callers, `BattleEncodedId_QueryMode0Positive`: the
booleanized sibling of `00309EC0`'s dispatch — same `0xFFFF`/`> 0xE000`
rejects, same `0x58`-stride `01EEBCC0` row select and `[+0x3C]-1` bounds
check, but calls `[row+0x50]` and returns `result > 0` at
[`0030B154`](../../_index/ADDRESS-INDEX.md). The predicate arm the grid sweep
tests.

## SWE2-EC7-25 update (2026-09-18) — `00323600` row accessor

`00323600` (47 B) bounds-checks `cl <= 0x27` (out-of-range passes `rcx = 0`),
strides `cl * 0x1C8` into `[02EBF190] + 8`, and tail-jumps `00323D10` —
the row-address stage the license-board and gambit callers share. Interior
anchor `00323612` (the `imul 0x1C8`).

## SWE2-EC7-39 update (2026-09-19) - `0055E090`

`0055E090` (413 B) is a call-free `0x38`-stride record walk - `[rcx+0x55a]`/`+0x559` byte fields, `test dword,0x2000` flag gate, `[rcx+0x54c]` word bound, records at `[rcx+0x120]+0x18`. Interior anchor `0055E0D0` (the `0x2000` flag test).

## SWE2-EC7-39 update (2026-09-19) - `0055DBD0`

`0055DBD0` (407 B) is the board teardown/rebuild the page names - `0209AC30`, `003697F0` free plus `0055B3F0`/`0055C530`/`0055B560`/`00561830`/`00282DF0`/`00323630` and `00244F00` pair. Interior anchor `0055DC52` (a `003697F0` call).

## SWE2-EC7-59 update (2026-09-19) - `00561830`

`00561830` (161 B) is a license-board body - `00244F50`/`00246AD0`/`00808C40` plus `01F44830`/`0208EA28`/`02CA8FE8`. Interior anchor `0056188A` (a `00244F50` call).


## SWE2-EC7-81 update (2026-09-20) - `00560FA0` + `00560F20` + `00559860` + `00559800` + `005597C0` measured

`00560FA0` (119 B) is the `+0x144` six-word writer on
`[0209AC30]+0x158`: `r9d == -1` fills all six `+0x144..+0x14E`
words with `dx`; else `r9d` is matched against the six `+0x120`
dword slots and `dx` lands at the matching `+0x144 + i*2`.
Interior anchor `00560FBC` (the first word store).

`00560F20` (119 B) is the identical sibling writing
`+0x138..+0x142` - same `-1`-fill / match-write shape.
Interior anchor `00560F3C` (the first word store).

`00559860` (171 B, stack-cookie) is the four-slot lazy-create on
`[+0x140]`: each NULL slot runs `00244F50(0x208, 005599D0, &args)`
with `rsi`/`rbp`/index/`[+0x160]` packed into the stack block.
Interior anchor `005598D6` (the `00244F50` call).

`00559800` (92 B) is the four-slot bit-16 propagate: each live
`[+0x140]` element gets `+0x40` bit16 rewritten to `(edx & 1) << 16`,
then `00244DD0` runs on it.
Interior anchor `00559828` (the `+0x40` and).

`005597C0` (56 B) is the matching release pass: `00244F00` on each
live `[+0x140]` element, four slots.
Interior anchor `005597DE` (the `00244F00` call).

## SWE2-EC7-82 update (2026-09-20) - `00247680` slot-flag init measured

`00247680` (87 B) is the flag/parameter init `005599D0` runs on its
elements: `+0x40` loses `0x08000100` and gains bit7, `+0xA3` takes
`dl`, `+0xA4`/`+0xA5` take the negated globals `020812B0`/`020812C3`,
and `+0xA6`/`+0xA7` take `020812D2`/`020812E1` doubled - the same
`+0x40`-flagged object `00559800`'s bit16 propagate touches.
Interior anchor `00247693` (the `bts` on `+0x40`).

## SWE2-EC7-102 update (2026-09-20) - `00283730` measured

`00283730` (220 B) is the command-id predicate
`002C1000`, `0055BFF0` and `0055F830` call: `ecx -
0x4B3` bounds a 12-arm `0028380C` jump table whose
arms mostly answer `setne` on
`0032A8A0(0x4004..0x4010)` capability ids, two arms
first gate on `00254A50() == 0`, one arm returns 1
outright, and the default returns 0 - the
license-command capability check the grid builds
run.
Interior anchor `0028374D` (the table load).

`00561300` (131 B) is the ensure-create for the board spine `00558FB0`/`00560910` call: a null `[+0xC8]` is `00244F50(0x110, 00561390, &ctx)`-created with context `{this, edx, movsx r8b}` and `+0x187` cleared — the `00561390` record is the object the board children hang off.

Interior anchor `00561364` (function `00561300`).

`00558F20` (132 B) is the sibling ensure-create `00560910`/`00561390` call: a null `[+0xC8]` is `00244F50(0xE8, 00558FB0, &ctx)`-created with the same `{this, edx, movsx r8b}` context but `+0x187` set to 1 — the `00558FB0` child.

Interior anchor `00558F85` (function `00558F20`).

`0055C690` (166 B) is the license-board create `00561390` runs: a null `[+0xC8]` is `00244F50(0x580, 0055CD40, &ctx{this})`-created, stored into `[0209AC30]+0x320` as well as `[+0xC8]`, registered through `00246AD0(0208EA28, obj)`, and `002470D0`'d — the `0x580`-byte `0055CD40` view record is the board object the whole `0055xxxx` cluster serves.

Interior anchor `0055C6EA` (function `0055C690`).

`0055A810` (140 B) is the per-slot child ensure-create `00561390` runs: `this + r8·8`'s `+0xD8` slot, when null, is `00244F50(0xD8, 0055A8A0, &ctx{this, rdx, r8d})`-created and `00246AD0(0208EA28)`-registered — one `0055A8A0` record per board sub-pane index.

Interior anchor `0055A86E` (function `0055A810`).

`0055F1C0` (543 B) is the cursor-move animation driver `0055E9E0` runs on the board record: `+0x530` bits 0-1 gate a `00248F40(0208F570 - +0x540, +0x53C, (+0x530>>2)&0xF)` ease; finished ease commits `+0x544` = `+0x534 + +0x538` and `+0x546` = `+0x536 + +0x53A`, clears `+0x530` bits 0-1, sets `+0x570` bits 0xC0, arms `+0x190` = 1 with the default step table `0x1E04061E` at `+0x195`; mid-ease `+0x544`/`+0x546` take `+0x534`/`+0x536` + delta·ease and `+0x570` bits 0xC0 clear. Under `+0x570` bit 0x40 a second sequencer steps `+0x190` through the `+0x194[]` byte delays at `+0x193`, wrapping at 5 when `+0x570` bit 0x80 is set (else stopping at 0), and `+0x191` takes a `00248F40`-eased 8-division pulse for modes 2 and 3.

Interior anchor `0055F385` (function `0055F1C0`).

`0055EF10` (254 B) is the per-cell timer tick `0055F3E0` runs: over the `+0x55A` rows by `+0x559` columns of the `+0x120` grid (`0x38` stride), each cell is `0055F010(cell, (+0x570>>9)&1)`-advanced — a 0x10 return sets the sound flag — and a live `+0x28` decrements `+0x26` then recomputes `+0x25` = `+0x26`·0x80/`+0x27` (inverted when `+0x29` is set), or pins `+0x25` to 0x80. Any 0x10 tail-enters `00249C60(0x4A)` — the per-cell completion cue.

Interior anchor `0055EF70` (function `0055EF10`).

`0055E230` (139 B) is the grid floor-flag pass `0055BFF0` runs: over the same `+0x55A`/`+0x559`/`0x38` grid at the `+0x18` state word, any cell whose `+8` id is not 0xFFFF and whose `+0x18` high nibble (`& 0xF0`) is below 0x10 is rewritten `& ~0x1F | 0x10` — the sweep's minimum display-state enforcement for real squares.

Interior anchor `0055E294` (function `0055E230`).

`0055DEA0` (489 B) is the connectivity sweep `0055BFF0` runs: per cell it probes the left and right neighbours (`esi`/`ebx` index arithmetic bounded by `+0x54C`, skipping `+0x8` = 0xFFFF rows) and reads each neighbour's `+0x18 & 0xF0` into a three-bit pattern; when the cell's own high nibble is already set the pattern is inverted bit-by-bit, and the `00D230F8` 8-row link-shape table (`0x1C` stride) maps the pattern to the new low nibble folded into `+0x18` — the licence-link direction bits.

Interior anchor `0055E04D` (function `0055DEA0`).

`0055C740` (1530 B) is the board input handler `0055CD40` runs: `+0x80` bit 4 and `+0x570` bit 0x100 gate out early (after `00282DF0(+0xDE0)` + `002C1A80` key-context and the `002CE2D0` reject path); `0029DBE0(0x117)` on `02F9736A` runs the `+0x570`-bit-0x400-gated `00323630`/`003242F0` SE+0x51 arm with `00247570` on `[+0x138]`; `ebp & 0xC00` arms `005611A0`/`0055B840` (0x800) and `0055FFC0`/`0055AE00` (0x400) or SE 5; `01E0C2A4` (confirm) picks `00559800`+SE 3+bit-2 clear, `0055A1F0`+SE 4+bit-2 set, or `00247510(0x8001)` under bit 0xA; `01E0C2A0` (cancel) mirrors with `0055A1F0`/SE 5/`0x8001`; `0029DBE0(0x110)` toggles zoom — `+0xDE6` ^= 1, `+0x40` |= 0x200000, `00247300` lerps between the `00D23080` float pair — when `+0x80` bit 4 is clear. `r14b` dpad bits 0x20/0x80/0x40/0x10 wrap `+0x550`/`+0x551` inside `+0x552`/`+0x553` (with `sil` edge-repeat), a changed cursor sets `+0x524` bit 0, re-reads the cell, runs `0055B8C0` + `0055A180`, posts `00247510(0x8000)` and SE 1; the stick pan reads `02F97398`/`02F97399` (or `02F9739A`/`02F9739B` fallback) sar-5 through `001E0A40`/`001E0A70`/`00228480` into `+0x51C`/`+0x51E`, clamped to the `+0x514`..`+0x51B` rectangle, and `+0x570` bit 0x100 clears once the pan returns to its resting point.

Interior anchor `0055CBDE` (function `0055C740`).

`0055B6D0` (360 B) is the single-cell icon draw `0055CD40` runs: `[+0x188]+0x20`+0x30's `{count@+0x14, index@+0x16}` header resolves the cell's `{w0, w2, packed dword4}` icon record; the packed coords (`dword4 & 0xFFF` / `>>0xC`, `>>1` & 0x7FF / `>>0xD`) are centered on `+0x554`/`+0x555`, offset by `+0x544`/`+0x546` + `+0x51C`/`+0x51E` minus `(8 - +0x191)>>1`, palette byte `+0x5C` = `base[b7>>4] + (b7 & 0xF)`, and `002D8C80` emits the sprite.

Interior anchor `0055B826` (function `0055B6D0`).

`0055B2B0` (94 B) is the any-cell-active predicate `0055F3E0` consults: scans the `+0x559` by `+0x55A` `0x38`-stride grid and returns 1 the moment a cell's `+0x22` (armed transition) or `+0x28` (live handle) byte is nonzero, else 0 — the sweep-completion test.

Interior anchor `0055B308` (function `0055B2B0`).

`0055AE80` (1060 B) is the two-pass grid draw `0055CD40` runs on `[+0x168]`'s palette resource: `002D9C40` opens the viewport at `+0x51C`/`+0x51E` + half of `01F2CACC`, then pass one walks `+0x553` rows by `+0x552` columns at the `+0x24` link cell — `+0x18` high-nibble nonzero draws a `002D9380` sprite per cell with palette `+0x67·3`-indexed and a +8 bump on the `+0x550`/`+0x551` cursor cell — and pass two walks `+0x55A` by `+0x559` at `+0x18` for the low-nibble node icons; both passes batch `002D9B00`/`002D9C40` viewport transitions twelve cells at a time. The licence link-lines and the node icons, in that order.

Interior anchor `0055B060` (function `0055AE80`).

`0055AB20` (730 B) is the tiled-backdrop pass `0055CD40` runs: `[+0x180]+0x20`+0x30's icon record gives the tile `w = dword4 & 0xFFF` / `h = >>0xC & 0xFFF`; `+0x520`/`+0x522` plus a full `01F2CACC` set the cell counts, the `+0x51C`/`+0x51E` pan is wrapped into negative tile-space and then forward-filled to the `01E0C1D8`/`01E0C1DC` (0x1C0/0x191) bounds, and a nested loop `002D9380`-draws the tile grid with a `0x80808080` tint quad, twelve-per-`002D9B00`/`002D9C40` batch.

Interior anchor `0055AD88` (function `0055AB20`).

`0055AA00` (276 B) is the `+0x563` cursor-settle machine `0055CD40` runs under `+0x565`: mode 3 `002D66A0`-steps `+0x550`/`+0x551` toward `+0x567`/`+0x568` in 0x20/0x80 or 0x10/0x40 strides until aligned, then drops to mode 2 with `+0x56A` = 0x18 and `+0x566` = 0; mode 2 decrements `+0x56A` and restores `+0x563` = `+0x564` at zero; the `+0x569`-armed arm writes `+0x563` = 0x302, `+0x56A` = 0x20; mode 0 clears `+0x565`.

Interior anchor `0055AA5E` (function `0055AA00`).

`0055A180` (108 B) is the detail-pane refresh `0055C740`/`0055F3E0` run: `+0x570` ~~bit 2~~ bit 1 (`& 2`) set tail-enters `0055A1F0(this)` *(corrected 2026-10-02, OPUS: `0055A180+0x6` `test byte ptr [rcx+0x570], 2`)*; else `rsi` is stored into `+0xD0` of each of the four `[+0x140]`..`[+0x158]` children and `00559E30` rebuilds each — the four detail lines track the selected square.

Interior anchor `0055A1CD` (function `0055A180`).

`00559E30` (844 B) is the licence-detail builder `0055A180`/`0055A1F0`/`005599D0` run on a detail child: `[+0xD0]`'s `+8` id = 0xFFFF only clears `+0xDE`/`+0xE2`; otherwise `[+0x60]`'s subobjects get bit-0 flags folded (`[+0x30]+8` &= ~1, `[+0x28]+8` ^= `([+0x18]>>0xD ^ +8)&1`), `0020E620`/`002DD7E0` ids land in `+0x20`/`+0x24`, `0029FF60` + `0035D330(0x19, id)` resolve the licence name, and `+0x21` class byte picks the `[+0x20]` palette (`+7`/`+0xA` fields, or the 0x1E `+0x97` fallback). The 8-entry `[+0xE8]`/`[+0x100]` `0x20`-stride table is then zeroed and refilled — per entry `0035D330` class 0x1D / 0x14 / `(word<<0x10, 1)` + `002B58B0` text, with `00285F40(6)`/`002B3050` and the `id-0x9E <= 0x17` Quickening arm — before `002D48C0([+0xC0], r15d or 1)` posts the count.

Interior anchor `00559FEB` (function `00559E30`).

`00558E70` (174 B) is the text-record setter `00557DB0`/`00558CE0` run: `00282DF0([+0xC8])` resolves the record, `003236B0`/`00323670`/`00323630` map its `+0x60` byte; a non-0xFF result sets bit 0 of `[+0x60]`'s `+0x18` record's `+8`, replaces it with `00556380(base+0x60, bpl, al, -2)`'s return, and `0020E620()` stamps `+0x20` — while `[+0x60]`'s `+0x20` record's `+8` bit 0 clears.

Interior anchor `00558EEA` (function `00558E70`).

`00556380` (371 B) is the licence-name composer `00558E70`, `00283E40`'s flag-propagate chain and the `005618E0` detail pane share: slot `ecx` selects `02CA8FF0 + ecx·0x100`, the id pair `{edx, r8d}` is sorted ascending, `002F9860(id + 0x3ED)` resolves each name and `002F9860(0x3F9)` the separator, `002DD7E0(3)`/`002DD7E0(0)` feed `002AB870` the two colour prefixes at `02F974C0`/`02F974D0`, and `0017D2E0` writes `"%s"` / `"%s%s%s"` / `"%s%s%s%s"` / `"%s%s%s%s%s"` by mode `r9d` (-2 plain join, id-match coloured, default five-part) — the composed string is the return, and is what `00558E70` swaps into the `+0x18` record's `+8`.

Interior anchor `00556413` (function `00556380`).

`005611A0` (182 B) is the last-eligible-record test `0055C740`/`00557B90` run on `[0209AC30]+0x158`: scanning `[+0x120 + i·4]` backward from `byte[+0x182] − 1`, each dword is `00282DF0`-resolved and `00323670(rec+0x60)`-classified until one returns not-0xFF; that index's `[+0x120 + i·4]` is then compared against `word[0209AC30 + 0xDE0]` — return 1 when the last eligible record is the armed one.

Interior anchor `005611F0` (function `005611A0`).

`0055FFC0` (165 B) is the `005611A0` mirror `0055C740`/`00557B90` run: forward scan from 0 over the same `[+0x120]` list for the first record whose `00323670` classification is not 0xFF, then the same `word[+0xDE0]` compare — the pair of boundary tests the page-up/page-down arms gate on.

Interior anchor `00560000` (function `0055FFC0`).

`0055B8C0` (158 B) is the cursor-cell retarget `0055C740` runs when `+0x550`/`+0x551` moves: target `{x, y}` = `{+0x554·+0x550, +0x555·+0x551} + 01F2CACC/2` (half-cell centre); when it differs from `+0x544`/`+0x546`, `+0x530` bits are rewritten `& ~0x3A | 5`, the old pair lands in `+0x534`/`+0x536`, the new in `+0x538`/`+0x53A`, `+0x53C` = 6 arms the countdown and `+0x540` = `0208F570` stamps the tick — the from→to record `0055F1C0`'s ease then plays out.

Interior anchor `0055B90C` (function `0055B8C0`).

`0055B840` (123 B) is the page-up commit arm `0055C740` runs on `ebp & 0xC00 = 0x800`: `0027F430(&0209AC30+0xDE0, 1, 005617E0)` queries the armed slot and, on 1, `+0x570` bit 0x800 first `00247570`s `00D23030` onto `[+0x138]`, the bit clears, `00249C60(0x51)` cues, and `0055DBD0(this)` re-drives — returns the query result.

Interior anchor `0055B873` (function `0055B840`).

`0055AE00` (123 B) is the `0055B840` sibling on `ebp & 0xC00 = 0x400`: identical shape but the query is `0027EDA0(&0209AC30+0xDE0, 1, 005617E0)` — the page-down commit arm, same `+0x570`-bit-0x800 rename, SE `0x51`, `0055DBD0` re-drive.

Interior anchor `0055AE33` (function `0055AE00`).

`00558C40` (159 B) is the `+0xC8` ensure-create `00557DB0`/`00558760` run: a null slot is `00244F50(0xD0, 00558CE0, &ctx)`-created, `[+0xE8]` is published into `02CA8FE0`, and the child `00246AD0`-attaches under `0208EA28` — the `00558CE0` record is the pane's `0xD0` child.

Interior anchor `00558C62` (function `00558C40`).

`00558AF0` (187 B) is the eased scroll stepper `00557DB0` runs while `+0x158` low bits are live: elapsed `0208F570 − +0x168` over duration `+0x164` feeds `00248F40` under shape `(+0x158 >> 2) & 0xF`; ease complete (1.0f) snaps `+0x350` = `+0x15C + +0x160` and clears the low bits, mid-ease writes `+0x350` = `+0x15C + +0x160·ease`, and `+0x34C` always takes `(0x168 − +0x350) / 180.0f · π` — the remaining-distance phase the renderer spins on.

Interior anchor `00558B2E` (function `00558AF0`).

`005587E0` (219 B) is the six-slot collector `00557DB0` runs: `[this+0x16C]` is `00861EC0`-zeroed for 0x1E0, then `ebx` walks `00282DF0`-resolved records, `00282FA0`-gated, and each whose `00323670` classification is not 0xFF (max six, `ebp < 6`) files `word[+0x60]` into the `(class + 0xA)·40`-indexed slot under `rsi` — the per-class table the detail panes read.

Interior anchor `00558810` (function `005587E0`).

`00557B90` (537 B) is the licence-pane input dispatch `00557DB0` runs: `r9d & 0xC00` picks the `005611A0` (0x800) / `0055FFC0` (0x400) boundary tests before `00557A90`/`00557A40` fire — each gated on `[[+0xC0]+0xC0]+0x188 == -1`; `r9d & 0xA0` cycles `byte[+0x358]` — 0x80 wraps 0..0xB forward, 0x20 backward — with `00247510(this, 0x8000, dir)` per move; `edi & word[01E0C2A4]` (confirm) under the `+0x188 == -1` gate sets `+0x388` bit 0 and posts `00247510(this, 0x8002, -1)`, returning 3; `edi & word[01E0C2A0]` (cancel) posts `00247510(this, 0x8001, 0)`; the tail re-posts `00247510(this, …, byte[+0x358])` and `00249C60(2 or 3)` cues the move SE.

Interior anchor `00557C36` (function `00557B90`).

`00557AE0` (166 B) is the `+0xC8` ensure-create `00558FB0` runs for the `00557DB0` pane itself: `00244F50(0x390, 00557DB0, &ctx)`-created, published into `[0209AC30]+0x320` beside `[+0xC8]`, `00246AD0`-attached under `0208EA28`, then `002470D0`'d — the licence detail pane's whole `0x390`-byte record.

Interior anchor `00557B35` (function `00557AE0`).

`00556EC0` (143 B) is the `+0xD0` ensure-create `00557DB0` runs: `00244F50(0x3D8, 00556F90, &ctx{this, byte[+0x358]})`-created and `00246AD0`-attached — the `0x3D8` child seeded with the pane's current index byte.

Interior anchor `00556F17` (function `00556EC0`).

`00556D20` (136 B) is the `+0xD0` ensure-create `00558FB0` runs: `00244F50(0xD0, 00556DB0, &ctx)`-created and `00246AD0`-attached — the sibling `0xD0` child under the same spine.

Interior anchor `00556D75` (function `00556D20`).

`00556590` (70 B) is the cell-record word resolver `0055F010` calls per advancing cell: `(byte[+0x18] & 0xF0) == 0x40` selects the `word[+0xE]` index — `0xFFFF` reads the fixed `02CA9670 + 0x5A60` slot's `+2` word, else `02CA9670 + 0x20 + word·0x40`'s `+2` word; other kinds return 0 — the per-cell table lookup the pending-state animation feeds on.

Interior anchor `005565A7` (function `00556590`).

`00557A90` (75 B) is the page-up commit `00557B90` fires after `005611A0` passes: `0027F430(0209AC30+0xDE0, 1, 0)` queries the armed slot and, on 1, `00249C60(ret+0x50)` cues and `00558760(this)` re-drives — the query result is the return.

Interior anchor `00557ABE` (function `00557A90`).

`00557A40` (75 B) is the `00557A90` sibling `00557B90` fires after `0055FFC0` passes: identical shape on `0027EDA0(0209AC30+0xDE0, 1, 0)` — the page-down commit arm, same `00249C60(ret+0x50)` cue and `00558760` re-drive.

Interior anchor `00557A6E` (function `00557A40`).

`00558760` (127 B) is the pane re-drive `00557A90`/`00557A40` call after the armed-slot query passes: `word[0209AC30+0xDE0]` (the armed index) publishes into `this+0x354` and `[this+0xC0]+0xD8`, the `+0xC8` child is `00244F00`-released and rebuilt through `00558C40`'s ensure-create, `005588C0` refreshes, and `002527B0(6, 4, armed)` ~~re-lays the pane~~ stores `armed` into word 4 of bank 6 *(corrected 2026-10-02, OPUS: `002527B0` writes its third argument into one of three banks at `[020927C0]` — bank 6's words at `+0x30`, `002527B0+0x69`; it lays nothing out)* — the detail pane's whole rebuild on a page commit.

Interior anchor `005587AE` (function `00558760`).

`0027F430` (270 B) is the forward ring-query `00557A90` and `0055B840` share (`002C1320` also calls): `word[rcx]+1` folds mod 9 by the `0x38E38E39` multiply, then the `[0209AC30+0xAC8]` 8-byte-entry ring walks — when `byte[+0xD3C]` bit 0x10 is set, records with `word[+0x60]` negative, `byte[+0]` bit 1 set, or `word[+0x60]` above 5 are skipped; the caller's `r8` predicate can veto any candidate; the walk ends when `word[+0x60]` reads negative or the start index closes the loop. The page-up armed-slot search.

Interior anchor `0027F471` (function `0027F430`).

`0027EDA0` (216 B) is the `0027F430` mirror `00557A40` and `0055AE00` share (`002C12B0` also calls): `word[rcx]-1` wraps to 8 under `cmovs`, the same `+0xAC8` ring, the same `+0xD3C`-bit-0x10 gate, the same `word[+0x60]`/`byte[+0]` eligibility tests and `r8` predicate — the page-down armed-slot search.

Interior anchor `0027EDD0` (function `0027EDA0`).

`00282A40` (834 B) is the view proc `0055CD40` calls: `0031C4C0`, `00252F40` x2, `0020E600` x2, `00252FA0` x4, `0031C5D0`, `0016D6A0`, `002CCA00`, `00317B70` and `00306340` run the grid row's emit under the cookie check - the license-board view's per-cell builder.

Interior anchor `00282AE4` (function `00282A40`).

`002858A0` (355 B) is the nine-column layout sweep behind the grid build: `r13 = qword[[0209AC30] + 0xF8]` supplies the column-records parent and `r14` walks `+0xC0` in 8-byte steps for `ebp` = 0..8; when the caller's flag arg is nonzero each record's `dword[+0xC0]` takes the column index, bit 3 of `dword[+0xFC]` tracks the `+0xB10`-indexed flag byte for the signed `word[rsi+0x60]` class (negative clears the bit), `00247870` and `00283E40` run per column, and the `edi` x-accumulator - starting at `sx word[r13+0x10A]`, adding `sx word[r13+0x10E]` for later columns plus `[r12+0x34]` or `[+0xC]` by `byte[rsi] & 2` - lands as `word[rbx+0x9A]`, the column's horizontal slot.

Interior anchor `00285930` (function `002858A0`).

`00283E40` (1547 B) is the board-grid rebuild the widget, license-board and layout callers share: `rcx`'s `dword[+0xC0]` indexes ~~`qword[0209AC30 + idx*8 + 0xAC8]`~~ `qword[[0209AC30] + idx*8 + 0xAC8]` *(corrected 2026-10-02, OPUS: `00283E40+0x26` loads the pointer `[0209AC30]`, `00283E40+0x43` indexes it)* for the slot record `r14`, `[+0xC8]`'s back-link self-heals through `002845E0`, `00243E90(rbx+0x50)` syncs the element flags, and `00247930(rbx, 0x5D - 2*word[r14+0x60])` arms the row count. With `word[r14+0x60] < 0` the body only clears bit 0 on `([rbx+0x50]>>2)&0xFFFF` elements of the `+0x60` array; otherwise it sets `dword[rbx+0x50] |= 1`, clears bit 0 on the ten fixed slots `+0x120..+0x190` and the `0x118`-entry head range, then on `byte[rbx+0xF8] == 0` pulls up to 0xB text rows through `002D0280`/`002D02C0`/`002D03B0`, marking each slot whose row byte differs from 0x1D dirty (`|= 1`) and copying `[r8+0x20]+row*8+7` into the row's `+0x39`/`+0xA`. The `+0xFC` bit6 lane gates `0032A8A0(0x4006)` license checks, mode `word[r14+0x60]` (sign-/-2/-gated) feeds `003236B0`/`00323670`/`00323630`/`00556380` font+icon resolves on `+0xB8`, the `+0xA8/+0xB0` pair gets the `edx` visibility bit, `0029FF60(rbx+0xD0)` formats the cost, and `0029F6E0` writers fill `+0x00/+0x10` (mode byte `r14+0xBA`), `+0x20/+0x40`/`+0x48` (LP `r14+0x20/+0x24/+0x2C/+0x30`) while `002DD7E0(0 or 4)` and `0035D330` (mode 2) build the two picture records `+0x148`/rsi - `+0x87` rows get bit0 set or cleared against `+0x86`, and `+0x150`-block rows copy their `+0x39`/`+0xA` pair.

Interior anchor `00283E83` (function `00283E40`).

`002D02C0` (225 B) is the bitmask-to-row-table expander the grid build pulls through `002D0280`: for each set bit `i` of `r8d` over `edx` positions it fetches the category-0x1A record `0035D330(0x1A, i)` and emits a 4-byte row `{index i, field byte selected by `r9d` (0..4 map to record `+0x20..+0x24`), the record's `+0x25` low bit}`, advancing the write cursor by 4 per row; the return value counts the rows whose field byte is not 0xFF - the populated-license mask the caller's row renderer consumes.

Interior anchor `002D0300` (function `002D02C0`).

`002D03B0` (83 B) is the enumeration shim paired with `002D02C0`: under a stack cookie it invokes `00249CE0` on `rcx` with callback `002D0270`, a local 4-byte state slot and bound `r8d = 4` - the fixed four-item iteration the license-grid callers run per pull.

Interior anchor `002D03E6` (function `002D03B0`).

`002845E0` (472 B) is the license-board link fixup `00283E40` runs inside the grid change sweep: it clears bit 0 of the `[rdi+0x60]` node's `+0x40` and `+0x38` children, picks the `[rbp+0xFC]`-bit-3 alternate record (`+0x168` vs `+0x170`) and stamps the `+0xA1` code byte `0x80`/`0x58`, merges the `[rsi+0x60]`-signed and `[rsi]` `0x20000`/`0x2` flag conditions into the matching child-enable bits, accumulates the record's `+0xE`/`+0xC` words into `[rbp+0x9A]`/`[+0x98]`, runs `00247930(rdi, 0x2F - 2*[rsi+0x60])`, then calls `00247870` with argument 0 or 1 by the `+0x60` sign; `[rsi+0x44]` bits `0x80000003` light the `+0x28` child and pick the `002DD7E0` argument whose result fills `[rbx+0x28..0x34]`, `[rbp+0xFC]` bits 0x30 copy a byte of the `+0x30` node's `+0x20` table into `+0x39`/`+0xA`, and the tail `002C9BD0([rsi+0x60])` index copies `[+0x20]` entries into `[rbx+0x39]`/`+0xA` the same way.

Interior anchor `002846EF` (function `002845E0`).

`00247300` (163 B) is the lerp setter `0055C740` runs when the zoom toggle fires: gated by `+0x80` bits `0xB` clear and `+0x8C != xmm2`, it arms `+0x80` bit 2, stores `xmm1` at `+0x84`/`+0x8C` and the `xmm2 - xmm1` delta at `+0x88`, packs `r9d & 0xF` into `+0x80` bits 10-13, stamps `+0x94` with `0208F570` and `+0x90` with the `arg*60`-scaled frame count (`0x10624DD3` magic divide), then `002418F0` commits - returning 1

Interior anchor `00247394` (function `00247300`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Resource — SERVICE, eight edges: the board is built on the menu object-and-slot machinery.** The board spine
`00558FB0` / `00560910` and the board record's builder `00561390` call four helpers that every menu uses to name,
bind and request its objects: the slot-name wrapper `002493D0`, the context supplier `00249580`, `0024A5A0` and the
menu-set request `00249210`. The ledger files them under Resource. Their mechanism belongs to
`a-typed-list-measured-once-and-built-in-one-allocation` and `five-small-bin-tables`; nothing about the licence
grid lives there.

**Party — CLIENT, one edge.** The cell reader `00328990`, one of the six readers of `cell(col, row)`, is called by
the party-filed `00328BD0`. So a party body reads the licence board's cells. Why it does is the party layer's
subject; this page owns the cell layout.

**WorldAreaField — MECHANICAL, two edges.**
- `World_UpdateSimulationTick` calls `00228480`, the pan helper this page cites, which the application's slot-7
  tick also calls (`game-application`).
- The world-area-field-tagged `00576A50` consults `BattleEncodedId_DispatchQueryMode0Value` (`00309EC0`), the
  encoded-id dispatch the grid build shares.

Both are shared helpers, not a field relationship of the board.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page and the cited pages read them; no new body read
(OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-license-board-grid-build-and-its-cha-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001E0A40` | 40 B | returns 0 when `00198790()` returns null, otherwise calls `00198790()` again and returns the zero-extended byte `001976E0(that pointer)` returns | `001E0A44`, `001E0A4E`, `001E0A56`, `001E0A5B` |
| `001E0A70` | 40 B | returns 0 when `00198790()` returns null, otherwise calls `00198790()` again and returns the zero-extended byte `001976F0(that pointer)` returns | `001E0A74`, `001E0A7E`, `001E0A86`, `001E0A8B` |
| `002C1000` | 687 B | switches on dword `[rdx]`: 2 calls `002D0410(rcx)` and returns 0, 18 returns 0, values other than 1 tail-jump `005C5230`; for 1 resolves `00282DF0(word +0xDE0 of qword 0209AC30)`, reads its dwords `+0x90`, `+0xB0`, `+0x94` (-1 read as 0, then capped unsigned at `0x5F5E0FF`, `0x1869F`, `0xF423F`), calls `002432B0(rcx+0x50, qword +0x30 of qword 0209AC30, 0xF, rcx)` and copies its words `+4`..`+0xA` to `+0x98`..`+0x9E`, and prints the values with `0029FF60(child, buffer, 0x20, value, 0, 0)` into children (qwords of `[rcx+0x60]`): `+0x30` from `+0xD4` with the first; then when record word `+0x60` is not negative and bit 1 of its byte `+0` is set, clears bit 0 of dword `+8` of child `+0x10`, prints the third into `+0x38` from `+0xF4` and gives child `+0x20` `002F9860(0x3EB)`, `0020E620(0)` and `002DD7E0(2)` at `+0x18`/`+0x20`/`+0x24`; otherwise clears bit 0 of children `+0x10`, `+0x20`, prints the third into `+0x38`, sets bit 0 of children `+0x28` and `+0x18` to `00283730(0x4B5)` AND 1 and prints the second into `+0x28` from `+0x114`; finally clears bit 11 of dword `+0x40` and returns 0 | `002C1062`, `002C10EE`, `002C113C`, `002C123B`, `002C128C` |
| `002C12B0` | 75 B | when qword `+0x118` of qword `0209AC30` is non-null and `0027EDA0(that+0xC8, 0, 0)` returns 1, calls `00249C60(0x51)`, `002C1800()`, `002C38B0()` and `002C4720()`; returns 0 on every path | `002C12C2`, `002C12D3`, `002C12DD`, `002C12E0`, `002C12EF` |
| `002C1320` | 75 B | when qword `+0x118` of qword `0209AC30` is non-null and `0027F430(that+0xC8, 0, 0)` returns 1, calls `00249C60(0x51)`, `002C1800()`, `002C38B0()` and `002C4720()`; returns 0 on every path | `002C1332`, `002C1343`, `002C134D`, `002C1350`, `002C135F` |
| `002D0270` | 13 B | returns the sign-extended byte `+1` of `rdx` minus the sign-extended byte `+1` of `rcx` | `002D0275`, `002D0279` |
| `002D6680` | 20 B | returns the byte at `02F973A1` zero-extended when it is non-zero, else 8 | `002D6687`, `002D6689`, `002D668E` |
| `00556570` | 15 B | returns 1 when word `+8` of `rcx` is not `0xFFFF`, else 0 | `00556572`, `00556577`, `0055657B` |
| `00556580` | 10 B | returns bit 13 of dword `+0x18` of `rcx` (shift right by `0xD`, AND 1) | `00556583`, `00556586` |
| `00558CE0` | 386 B | switches on dword `[rdx]`: 2 returns 0; 18 returns 0 after, when dword `02CA9678` is non-zero, zeroing qword `02CA8FE0`, calling `00247730(qword 0209AC18, 0)` when that is non-null and zeroing `02CA9678`; values other than 1 tail-jump `005C5230`; for 1 calls `002432B0(rcx+0x50, qword +0x98 of qword 0209AC30, 1, rcx)`, copies its words `+4`..`+0xA` to `+0x98`..`+0x9E` (skipped for a null `rcx`), calls `00247570(rcx, 00D23030)`, stores the payload's first qword at `+0xC0` and its dword `+0x354` at `+0xC8`, resolves `00282DF0(that dword)`, fills child `+0x10` (`+0x18` from `002B58B0`, `+0x20` from `0020E620(0)`) and child `+8` (word `+0xA` from `002C9BD0`, byte `+0x39` from that entry's byte `+7`), then calls `00558E70(rcx)`, `00247930(rcx, 0x5F)` and `00247730(rcx, 1)` and returns 0 | `00558D14`, `00558D3D`, `00558D74`, `00558DF5`, `00558E4B` |
