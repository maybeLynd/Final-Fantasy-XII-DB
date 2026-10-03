---
system: The second icon drawer and what it adds
category: 99-Unresolved-Residual
status: AUDITED
owner_layer: CodeDomain:Presentation.Icon
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `004EDB50`, `004F5360`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range - re-run the additivity test at each checkpoint
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: residual-walk-repos-55
  crossref_clean: true
  reopened_count: 0
---

# The second icon drawer and what it adds

**`002BCB00` (2,703 B) is `002B8EE0` (2,865 B) again** — same pulse, same palette ids, same atlas
decode, same three drawing paths, same sub-item loop. **This document describes only the
differences**, because describing the rest twice would be describing it wrong once.

The shared machinery is in [the blinking icon and its atlas](the-blinking-icon-and-its-atlas.md).

> **This is the residual set's second specialisation pair.** The first —
> `004EDB50` / `004F5360`, 7,440 bytes each — is already in
> [the unresolved 158](the-unresolved-158.md) §8b. **Two of the fourteen residual clusters are the
> same routine written twice**, which is a property of the set worth knowing before reading any more
> of it.

## 1. What the player sees

**The same icon, drawn somewhere it can be scrolled off the edge and zoomed.** This variant does
three things its twin does not:

- **it is culled** — if the icon does not overlap the visible area it is not drawn at all;
- **it is scaled by a percentage** taken from a global, not just by the caller's factor;
- **it gets a second pass over a rectangle 128 units larger on every side**, which is the shape of a
  border, glow or hit region rather than of the icon itself.

## 2. The differences, in full

| | `002B8EE0` | `002BCB00` |
|---|---|---|
| position offset globals | `0209E5A8` / `0209E5AC` | **`0209E5D8` / `0209E5DC`** |
| atlas size | the raw 12-bit fields × scale | **÷ (`01E0CE80` / 100)** as well |
| cull | none | **`00249EE0` first; everything is skipped when it returns 0** |
| second pass | none | **`002DD2F0(context, expanded_rect)` after every rectangle** |
| depth to `00403970` | computed from `01E0C1D8` / `01E0C1DC` | **literal `0`** |
| scale word to `00403970` | the caller's `param_7` | **`0x3F800000`** — a literal `1.0` |
| `00404120` mode argument | `2` | **`1`** |
| `00403BC0` | four arguments | **three** |

**Everything else is instruction-for-instruction the same shape**, including both `sinf` pulses, the
six palette ids `0x6B`–`0x70`, the two-level atlas index, and the `record + 0x20 == 0xFF` sentinel.

**The atlas decode, read here rather than taken from the twin's document:**

```asm
002BCD6C  cmp   byte ptr [r13 + 0x2], 0x1        ; the atlas-kind test
002BCD7F  mov   rcx, qword ptr [r10 + 0x20]
002BCD83  add   rcx, 0x30                        ; the header base
002BCD87  movzx eax, word ptr [rcx + 0x14]       ; atlas[+0x44]
002BCD8B  movzx edx, word ptr [rcx + 0x10]       ; atlas[+0x40]
002BCD8F  add   rdx, rcx                         ;   -> the entry array
002BCD92  movzx r8d, word ptr [rcx + rax*0x2 + 0x14]   ; atlas[0x44 + atlas[0x44]*2]
002BCD98  mov   ecx, 0xfff                       ; the 12-bit mask
```

> **The index table at `+0x44` being indexed by its own first element is visible in one
> instruction**, `movzx r8d, word ptr [rcx + rax*2 + 0x14]`, where `rax` was loaded from that same
> `+0x14`. **Two documents now assert that shape and this is the one that read it as assembly.**

## 3. The cull is a rectangle intersection

`00249EE0` is small and unambiguous:

```c
// 00249EE0 — intersect two short[4] {x, y, w, h} rects into a third
// x axis: take the greater origin; the overlap ends at the lesser right edge
if (right_of_lower <= origin_of_upper) { out = {0,0,0,0}; return 0; }
// ...same again on y...
return 1;
```

**It writes the intersection into its first argument and returns whether it is non-empty**, zeroing
the output on a miss. The caller uses only the return value.

**The clip rectangle it tests against is the context's own extent, expanded:**

```c
clip = { -128, -128, context[0x4C] + 256, context[0x4E] + 256 };   // 0xFF80FF80 is (-128, -128)
if (!Rect_Intersect(&scratch, &icon_rect, &clip)) return;
```

> **The margin is 128 units on every side and it is not tolerance — it is the same 128 that appears
> everywhere else in this subsystem**, as the `>> 7` divisor in the
> [rectangle primitive](drawing-one-coloured-rectangle.md)'s tint and as `0x80` = `1.0` in the glyph
> record. **One unit of scale, reused as one unit of margin.**

## 4. The percentage divisor

```c
size_x = ((atlas_entry & 0xFFF) * scale) / (float)(iRam_01E0CE80 / 100);
```

**The divisor is an integer divide by 100 first, then converted to float** — so `01E0CE80` holds a
percentage and the whole expression is *"scale, then divide by the zoom percent"*. **An integer
divide by 100 truncates**, so a value of 250 gives 2, not 2.5, and the size steps rather than varies
smoothly.

> **This appears only on the atlas path.** The non-atlas path takes width and height from
> `record + 0x24` / `+0x26` and applies the caller's scale alone, exactly as the twin does.

## 5. The expanded second pass

```asm
002BCD40  sub   ax, cx                        ; cx = 0x80 -- x - 128
002BCD43  mov   word ptr [rbp + -0x68], ax
002BCD4C  sub   ax, cx                        ;              y - 128
002BCD4F  mov   ecx, 0x100
002BCD5D  add   ax, cx                        ;              w + 256
002BCD69  add   ax, cx                        ;              h + 256
002BCD71  mov   word ptr [rbp + -0x62], ax
```

```c
FUN_002DBDD0(context, &icon_rect);      // the icon's own rectangle
FUN_002DD2F0(context, &expanded);       // 128 units larger on every side
```

**Both calls happen on all three of the non-atlas drawing paths**, in that order, and `002DD2F0`
appears nowhere in the twin. **~~What it draws is not established~~** *(answered: see SWE2-EC7-18 below and the rectangle page: `002DD2F0` translates a child rectangle by its parent's origin and clips, it draws nothing; the blinking-icon page answers what the drawer shows, the track map's markers; 2026-10-02, OPUS)* — only that it receives a
rectangle inflated by exactly the margin the cull uses.

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Are these really the same routine, or two functions that merely resemble each other? | Both contain **the same `sinf((frame × π) / 30)` in the same two branches**, the same six palette ids in the same three pairs, the same two-level atlas index `atlas[0x44 + atlas[0x44]*2]`, and the same `0xFF` sentinel. **A resemblance does not extend to a two-level index expression.** |
| Is `00249EE0` a cull or a layout helper? | It returns `0` and zeroes its output when the rectangles miss; **the caller branches on the return and ignores the output.** Used as a predicate. |
| Is `0xFF80FF80` really (−128, −128)? | Two `short`s of `0xFF80` = −128. The other two clip fields are `context[0x4C] + 0x100` and `context[0x4E] + 0x100`, **+256 to cover the 128 subtracted from each side.** |
| Is `01E0CE80` a percentage, or a fixed-point value that happens to be divided by 100? | **Not established.** The `/ 100` is an integer divide in the source operand order, which is what a percent-to-multiplier conversion looks like; **the name is the reading.** |
| Could the `00403970` differences be the decompiler assigning arguments differently? | The twin passes a value computed from two globals and `param_7`; this one passes the literal `0` and the literal `0x3F800000`. **Literals against computed expressions is not an argument-numbering difference.** |
| Why is so little of this document anchored? | **`002BCB00` has a zero-byte body in the live program**, so `search_instructions` cannot see into it — a search for `01E0CE80` scanned 566,028 instructions and matched none. **`get_xrefs_to(00249EE0)` likewise does not list this function's call to it**, while `edges.tsv` does. Anchors came from `disassemble_bytes` on a guessed range; §2 and §5 have them, the rest is decompilation. |
| Which of the two is the "original"? | **Not established, and probably not a meaningful question** — neither calls the other and both are reached through their own caller. |

## 7. What this document does not claim

~~What `002DD2F0` draws.~~ *(answered: see the note above; 2026-10-02, OPUS)* What `01E0CE80` is set from. Why the two variants read different position
offsets — the two global pairs sit `0x30` apart and nothing here says what distinguishes them. What
`00403970`'s depth argument means, such that one caller computes it and the other passes zero. Which
subsystem either drawer serves; **the twin's document does not claim this either, and finding the
same code twice does not make the answer any more available.**

## 8. Cluster 3 is closed

[The unresolved 158](the-unresolved-158.md) groups `002B8EE0`, `002BCB00` and `002DBDD0` as residual
cluster 3, 6,775 bytes. **All three are now read and classified at GN161**:

- `002B8EE0` — [the blinking icon and its atlas](the-blinking-icon-and-its-atlas.md)
- `002DBDD0` — [drawing one coloured rectangle](drawing-one-coloured-rectangle.md)
- `002BCB00` — this document

**The cluster was a real call cluster**: both drawers call the primitive, `002B8EE0` twice and
`002BCB00` twice more. **It was grouped by the call graph and it survived being read** — which is
worth recording, because the clustering was done before any of the three had been opened.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT and SERVICE, 20 edges.** Cited drawer functions are called by Presentation bodies of 2,703 bytes (6), 2,865 bytes (4), 1,027 and 1,416 bytes. They call Presentation bodies of 54 to 1,207 bytes.

**UI — CLIENT (5 edges, one shared subject plus one, all four bodies read; OPUS 2026-09-14, tier 1
from the shipping bytes).** Four of the five edges are UI bodies reaching one function cited here,
`00249EE0`, and that function is the **rectangle clip**: it takes two four-`int16` rects, picks
whichever has the larger left edge with a pair of `cmovge`, and works out the overlap from there.
`002DD2F0` is the worked example of how it is used — it translates a child rect by the parent
object's origin `word[+0x50]`/`word[+0x52]` into a stack rect, then clips that against the parent's
own box at `[parent+0x48]` and branches on whether anything survived. The fifth edge is `003EE420` (interior read 2026-09-17, SWE2-FRONTIER: 1,171 B — `002D8530` first at [`003EE481`](../_index/ADDRESS-INDEX.md), `003EEA80`/`00272310` ×2, carries the `bt_win_0_c` battle-window texture name),
a UI message handler dispatching on `dword[rdx]`, reaching `002DD2F0` itself. So the crossing is
**one shared clip primitive with four callers on that layer, plus one caller of its wrapper**, not
five separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

## SWE2-EC7-18 update (2026-05-15) — `002D8530` record-init arm

`002D8530` (25 B) is the flag-gated forward the icon-drawer reaches: `test dword[rcx+0x5C], 0x20000` selects `rcx+0x48` or null via `cmove` (`002D8530`..`002D8540`), then tails `00249FD0` (`002D8544`) — the bit-17 test that forwards either the `+0x48` sub-record or a null argument into the shared `00249FD0` continuation.

## SWE2-EC7-34 update (2026-09-19) - `00403BC0`

`00403BC0` (830 B) is the second drawer's big-frame body - a `0x1588` `00808F10` alloca probe, `00861F0E`/`003DFBB0`/`00202C70`/`00400190`/`003FFF40`. Interior anchor `00403C5C` (an `00861F0E` call).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — MECHANICAL (SWE2-EC7-34, 1 edge).** `00202C70` — the shared UI-object helper this page cites inside the `00403BC0` big-frame body — is called by `003F1E90` on the ActorEntity layer. Shared-helper fan-in; no actor relationship to the drawer.

**Audio — MECHANICAL (SWE2-EC7-34, 1 edge).** `00202C70` is also called by `00362850` on the Audio layer. Same shared-helper fan-in.

**Movement — MECHANICAL (SWE2-EC7-34, 2 edges).** `00202C70` is called by `00230790` and `00338490` on the Movement layer. Same shared-helper fan-in.

**Story_Event_Quest_Hunt — MECHANICAL (SWE2-EC7-34, 1 edge).** `003FFF40` — the other shared callee the `00403BC0` body names — calls `0032A8A0` on the Story_Event_Quest_Hunt layer. Shared-helper fan-in below the draw.

**WorldAreaField — MECHANICAL (SWE2-EC7-59, 1 edge).** `003C4070` — the callee this page's `00404120` section names — calls `00377780` on the WorldAreaField layer. Shared-helper fan-out below the draw.

## SWE2-EC7-41 update (2026-09-19) - `003EEA80`

`003EEA80` (333 B) is a second-icon-drawer body - `002D8CB0` single call. Interior anchor `003EEB82` (the `002D8CB0` call).

## SWE2-EC7-59 update (2026-09-19) - `00404120`

`00404120` (163 B) is a second-icon-drawer mode body - `003C4070`/`00808C40` plus `00916A08`/`01F44830`. Interior anchor `004041AC` (a `003C4070` call).


## SWE2-EC7-86 update (2026-09-20) - `003BEC50` + `00400190` measured

`003BEC50` (65 B) is the four-arg query over the same `02B457E0`
table the second icon drawer shares: `003C0380` supplies the
category, then `003BF5E0(table, category, ecx-arg, edx-arg,
out=&stack)` runs the resolve and the qword written into the
stack out-slot is returned.
Interior anchor `003BEC7C` (the `003BF5E0` call).

`00400190` (54 B) is the doubly-linked push_back the icon-drawer
and config-screen callers run: an empty `[rcx]` head seeds head
and `+8` tail and sets `word[+0x1412] = 1`; otherwise the node is
spliced after the tail (`tail->+0x28 = node`, `node->+0x30 =
tail`, `word[+0x1412]` incremented, `+8` updated).
Interior anchor `004001AA` (the splice arm).

`004001D0` (585 B) is the per-entry emit `003C4070` calls: `003C8060` resolves the record, `[rdi+0x20]`'s `word[+0x14]`/`+0x16` become `xmm8`/`xmm9`, `00400E80` then `00203170` on the stack block (whose callers are Gameplay- and Script_VM-side crossings, named at subsystem level, not by address), `rbx+4`/`+8` floats with `00D120EC` feed `00377780`/`00398C50`/`004006A0`..`00401D40`/`00808C40` - the drawer's row emit.

Interior anchor `00400236` (function `004001D0`).

`00377780` (28 B) is the two-call probe `004001D0`, `004006A0`, `00400E80`, `004017D0`, `00401D40` and `003C4070` all run first: `003148F0` then `00314A80`, return `eax != 0` - the availability test every emit arm shares. The probe's far ends are CombatAction-, Platform-, Save/Load-, Spawn- and Input-side crossings, named at subsystem level, not by address.

Interior anchor `00377784` (function `00377780`).

`004010A0` (1083 B) is the drawer's longest arm `004001D0` calls: `0208F570`'s counter runs `cvtsi2ss` x `00916318`-family constants (0x40490FDB = pi), `00270FF0`/`271080`/`271100`/`271450`/`2714A0`/`2714E0` build the vector stack, then `004005E0`/`004009C0`/`004019F0`/`00181330`/`00861F0E` emit - the rotating element's row.

Interior anchor `00401130` (function `004010A0`).

`00400E80` (533 B) is the literal-block writer `004001D0` calls: `00271450`/`2714A0`/`2714E0`/`2714C0` build the stack block, then qword pairs `{0x1001,0x47}`, `{0x44,0x42}`, `{0x60,..}` march a growing cursor at `[rbp-0x30]`, with `00181560`/`1816B0`/`181870`/`181890`/`181910`/`1819A0`/`181A70`/`002E0FA0`/`00377780` behind - the emit-stream fill.

Interior anchor `00400E99` (function `00400E80`).

`004017D0` (542 B) is the probe-gated emit `004001D0` calls: `00377780` first (`r15d` keeps its answer), `00271450`/`2714A0`/`2714E0` build the block, then `00202C70` copies it over `[rbp+0x40]`/`rbp` and onward with `00270FF0`/`271080`/`271100`/`2714A0`/`2714E0`/`2714E0` feeding - the conditional quad emit.

Interior anchor `004017FF` (function `004017D0`).

`00401D40` (656 B) is the counted emit `004001D0` calls: `00202D70` initialises the `[rsp+0x30]` block, `esi` walks `word[r14+2]` entries over `02B5F2AC` data at `00916318` (0x42800000 = 64.0f) scale, calling `00377780`/`00202B70`/`00202CA0`/`00808C40` per element - the per-entry row emit.

Interior anchor `00401D87` (function `00401D40`).

`004019F0` (837 B) is the drawer's largest arm `004010A0` calls: `00202D70` initialises the `[rsp+0x40]` block from `r8`/`r9`, then `ebx`-counted entries loop with `008C5A98` (0x44200000 = 640.0f) scale and the `00202B70`/`00202CA0`/`00808C40` emit chain - the drawer's per-row fill.

Interior anchor `00401A34` (function `004019F0`).

`004006A0` (464 B) is the emit arm `004001D0` calls: `word[rcx+4]` bounds, `00377780` runs first, then `edi < 0x18` / `esi < word[+4]` nested loops walk `rbx` entries through `00270FF0`/`00271080`/`00271100`/`00271450`/`002714A0`/`002714E0`/`00181330`, with `movabs` masks `0x3025C00000008000`/`0x302DC00000008000` doing the bit-pack - the drawer's masked-entry writer.

Interior anchor `004006D6` (function `004006A0`).

`00401620` (429 B) is the emit-record builder `004001D0` calls: `00271450`/`002714A0`/`002714E0`/`002714C0` assemble a `[rbp-0x40]` record whose cursor writes `0x3001`/`0x47` tag pairs, then `002710C0`/`00271100`/`00271080`/`00270FF0` and the `00181560`..`00181800`/`002E0FA0` render helpers run the emit - the drawer's record assembly.

Interior anchor `00401639` (function `00401620`).

`00400870` (323 B) is the quad builder `004006A0` calls: for `edx` elements it loops 3 vertices per quad, reading index pairs off `[rcx+0x20]` (`movsxd` from `r9-0x10`/`r9`), gathers the `02A3F2A0`/`02A3F2D0`/`02A3F820` atlas rows (`rsi + idx*8 + const`), cvttss2si the float coords to ints, and writes 0x30-stride vertex records on the stack (`+4`=i, `+8`=1.0f) - the drawer's per-element vertex expansion.

Interior anchor `004008F1` (function `00400870`).

`004014E0` (316 B) is the element constructor `004001D0` calls: `00271450`/`002714A0`/`002714E0` init the stack context, `00202C70` copies the caller strings into `rsi+0x10`/`+0x50`/`+0x90`, `dword[rsi]=0x280`, `+0xE0`/`+0xE4`/`+0xE8`=0x80, `word[rbp+0x58]` -> `+0xEC`, `rsi+0xF0` finishes through `00271100` with flags `02EBB78C | 0xA0000007 >> 3` and `0x10000000` - the drawer's record populate.

Interior anchor `0040152F` (function `004014E0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**CombatAction — MECHANICAL, 2 edges.** `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) is called by `BattleUnit_TryTriggerNearbyAuthoredFieldAction` (`002F8060`), `002FA740`.

**CoreRuntimeScheduling — MECHANICAL, 1 edge.** The core runtime object fetch `001B1C00`, whose result `00181800` hands to `001B2410` (interior row below), is also called by `0017D4C0`. *(added 2026-10-03, OPUS, with the interior citations)*

**Gameplay — MECHANICAL, 1 edge.** `00203170` is called by `BattleAction_FindApproachGeometryAroundTarget` (`00339630`).

**Input — MECHANICAL, 1 edge.** `002E0FA0` is called by `InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`).

**PlatformOnlineAchievements — MECHANICAL, 1 edge.** `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) is called by `003160C0`.

**Save_Load_Settings — MECHANICAL, 3 edges.** `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) calls `SaveImage_GetPersistentPayloadBase` (`002EF2B0`); `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) is called by `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`); `00314A80` calls `SaveImage_GetPersistentPayloadBase` (`002EF2B0`).

**Script_VM_Native_Bridge — MECHANICAL, 3 edges.** `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) is called by `0033F310`, `00357450`; `00203170` is called by `00356160`.

**Spawn_Encounter_Lifecycle — MECHANICAL, 1 edge.** `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) is called by `SpawnKeep_RotatePersistenceBanksForAreaTransition` (`00233780`).

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-the-second-icon-drawer-and-what-it-adds-cloudint-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00181800` | 106 B | calls `001B2410` on the result of the core runtime object fetch `001B1C00()`, as `001B2410(that, ecx, edx, r8, 0, r9d, 0, 1, 1, 0)` with the incoming `ecx`, `edx`, `r8` and `r9d`, the fifth to tenth as stack arguments | `0018181E`, `00181834`, `00181848`, `00181850` |
| `00272310` | 127 B | calls `00246480(rcx, &t)` and stores qword `t` at `[rdx]`; then, when `rcx` is non-null, for each node of the chain qword `+0x10` (from `rcx`'s) it calls `00246480(node, &t)` and adds words `t+0`/`t+2` to words `[rdx]`/`[rdx+2]`; the frame carries the stack cookie (`01F44830`, checked by `00808C40`) | `00272334`, `0027233E`, `00272358`, `00272362`, `0027236A` |
