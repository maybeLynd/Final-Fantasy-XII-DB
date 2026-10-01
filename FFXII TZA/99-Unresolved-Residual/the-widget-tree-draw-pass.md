---
system: The widget tree draw pass
category: 99-Unresolved-Residual
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS): all five cluster members are read (00245170, 002455A0 and 002DA2D0 on the widget-background page); what the second bracket pass draws (SD-101: flag bit 24 is a per-subtree second-pass switch set by six screens) and the glyph emitters' commands (SD-102) answered 2026-09-30; §7's four small callees read 2026-09-18 (the glyph run's flag getter, the fontcolor shadow byte, and two render-command emitters)
owner_layer: CodeDomain:Presentation.Widget
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range - re-run the additivity test at each checkpoint
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-30
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: residual-cluster-5-repos-55
  crossref_clean: false
  reopened_count: 0
---

# The widget tree draw pass

**`00245E60` is the recursive draw of the whole UI.** It is the 158 survey's residual cluster 5 root — classified at GN161 `Presentation.Widget.WidgetTreeRecursiveDrawPass` — it calls
itself, and it is the function that turns a tree of widgets into drawing.

**Two of the cluster's five members are read here** — `00245E60` (1,416 B) and `002DA7C0` (1,193 B).
`00245170`, `002455A0` and `002DA2D0` are ~~**not read**~~ read on [the widget background and its atlas sets](the-widget-background-and-its-atlas-sets.md) *(corrected 2026-09-30, SWE2-DATA: that page closes cluster 5)*; §7 says what is known about them and what is
not.

## 1. What the player sees

**Every menu, panel, gauge and label is a node in one tree, and this walks it.** A widget draws
itself, then its children draw inside it, and each child's position is the parent's position
combined with its own. **That is why moving a window moves everything in it.**

**And every widget is clipped twice** — once against its parent's rectangle and once against its own
declared size. **A label longer than its box is cut off by the box, and the box is cut off by the
window**, without either of them knowing about the other.

## 2. The walk

```c
if ((node.flags & 0x405) != 5) return;          // bits 0 and 2 set, bit 10 clear
...build this node's transform and clip...
...draw this node's own background...
for (child = node[3]; child != 0; child = *(long *)(child + 0x20))
    FUN_00245e60(child, &this_transform);       // 00245E60 recursing
```

**`node[3]` is the first child and `child + 0x20` is the next sibling** — the standard two-pointer
tree, walked depth-first with the accumulated transform passed down.

**The gate is three bits at once**, and it is the first thing the function does:

```asm
00245E88  mov  eax, dword ptr [rcx + 0x40]   ; the node's flags
00245E8E  mov  rsi, qword ptr [rcx + 0x10]   ; the node's definition pointer
00245E92  and  eax, 0x405
00245E9A  cmp  eax, 0x5
00245E9D  jnz  0x002463C6                    ; -> the epilogue
```

`(flags & 0x405) == 5` requires bit 0 and bit 2 set **and bit 10 clear**; a node failing it is
skipped **along with its entire subtree**, because the recursion is inside the guard.

> **The flags live at `node + 0x40`** — the decompilation's `param_1 + 8` in qwords — which is worth
> stating in bytes because every other document in this folder addresses fields that way.

## 3. The node's own handler is called with a message id

```c
if ((code *)*param_1 != 0) (*(code *)*param_1)(param_1, &UNK_009151C0);   // before content
...
if ((code *)*param_1 != 0) (*(code *)*param_1)(param_1, &UNK_009151D8);   // after content
...children walked...
if ((code *)*param_1 != 0) (*(code *)*param_1)(param_1, &UNK_009151F0);   // after children
```

**Those three constants are not strings.** Read as memory they are **24-byte records whose first
dword is a small integer**:

```
009151C0:  03 00 00 00  00 …    -> id 3
009151D8:  04 00 00 00  00 …    -> id 4
009151F0:  05 00 00 00  00 …    -> id 5
```

> **So a widget's handler receives messages `3`, `4` and `5` at three points of its own draw** — one
> before its content, one after, one after its children. **`node[0]` being the handler is the same
> slot `002465F0` installs at construction**, per
> [the widget constructor and object sizes](../16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md),
> **and that document records the constructor calling the handler once** — so construction is
> presumably another id in the same enum.
>
> **The id space around them is now enumerated** — 32 distinct ids over 211 handlers, in
> [the widget message protocol](../16-UI/Widget-Object-Model/the-widget-message-protocol.md).
> **3, 4 and 5 are answered by 28, 63 and 4 handlers respectively**, so the three draw messages are
> not equally universal: message 4 reaches almost a third of the game's widgets and message 5
> fewer than one in fifty. What they *mean* is still only what this document establishes.
>
> **This document does not claim what 3, 4 and 5 mean**, only that they are distinct ids delivered at
> three fixed points.

**The third call is gated on flag bit 12** and the first two on bit 24 matching a global
(`uRam_0208F564`), so a node can take part in some phases and not others. *(Anchored and completed 2026-09-30, SWE2-DATA: all three calls need bit 24 to equal `0208F564`. Messages 3 and 4 also need bit 28 clear (`0024623A`–`00246255`); message 5 needs bit 12 set (`00246388`–`0024639F`). The child loop (`0024635C`–`00246386`) sits outside both gates, so children are visited either way. `_index/candidates/dd-data-3-0930/widget_draw_checks.py` W1.)*

## 4. Clipped twice, by the function already documented

Both clips go through `00249EE0`, the rectangle intersection read in
[the second icon drawer](the-second-icon-drawer-and-what-it-adds.md) §3:

```c
parent_rect = *(rect *)(definition + 0x40);
parent_rect.x -= this.x;  parent_rect.y -= this.y;     // into local space
Rect_Intersect(&clip, &parent_rect, &scratch);         // against the parent
...
own_size = { …, node[+0x9C], node[+0x9E] };
Rect_Intersect(&clip, &clip, &own_size);               // and against itself
```

**The parent's rectangle is translated into this node's space before the test**, which is what makes
the clip compose down the tree.

## 5. The transform

`00203170` produces an identity; `003985B0` and `00398C50` are applied **only when their respective
float is non-zero**; `0039ADE0` scales by a value at `node + 0x8C`, gated on flag bit 21 *(anchored 2026-09-30, SWE2-DATA: the `ucomiss`/`je` pairs at `0024601F` and `0024603F`, and `shr eax, 0x15` at `002460FA`; `_index/candidates/dd-data-3-0930/widget_draw_checks.py` W4)*; and
`thunk_FUN_00217150` multiplies. The node's own offset is added around the **centre** of its
rectangle:

**Adjacency note.** `00203170` is the shared workbench identity-store — 19 of its callers are
**Movement**-layer bodies (`00338490`, `0033C310`, `0033DB60`, `003ED190`…), documented on
[the two transform primitives](../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md).
Its presence here is the draw pass *reusing* the helper, not the pass owning it.

```c
pivot.x = rect.x + rect.w * 0.5f;
pivot.y = rect.y + rect.h * 0.5f;
```

> **Rotation and scale happen about the widget's centre, not its corner.** That is a design choice
> visible in one pair of multiplications, and it is why a scaling widget grows in place.

**The brightness is inherited multiplicatively:** `(node[+0xA1] × parent[+0x5A]) >> 7` — **the same
1/128 fixed point** as the tint in [drawing one coloured rectangle](drawing-one-coloured-rectangle.md).

## 6. `002DA7C0` — the textured quad, and the filtering bit

The primitive takes a **source rectangle** (`short[4]`) and a **destination** (four ints), four
corner colours, and a 64-bit texture descriptor. It writes twelve 16-byte words into a cursor at
`param_1 + 0x10` — descriptor, then per corner a colour, a source (u, v) and a destination (x, y, z).

**And it sets a flag when the two rectangles disagree:**

```c
if (src[2] != dst_w || src[3] != dst_h) flags |= 2;
```

> **This is the filtering bit.** [The glyph-run document](Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md)
> reports that *"text drawn at its natural size is point-sampled and crisp; text the game has scaled
> is filtered and soft — a single bit in a single command, set only when the size is not exactly
> 100 %."* **Here is that bit in a shared primitive with the exact rule: source extent ≠ destination
> extent.** It is not a text feature; **it is how every scaled quad in the UI behaves.**

**The descriptor is unpacked into four fields** — `FUN_00181890(1, d & 3, (d >> 4) & 0x3FF,
(d >> 0xE) & 0x3FF)` — and **two further 10-bit fields at `>> 0x18` and `>> 0x22` are extracted and
then not used** in the decompilation. Reported as measured; ~~whether they are dead or the~~
~~decompilation lost their consumer is **not established.**~~ *(Corrected 2026-09-30, SWE2-DATA: they are not dead. They are the source rectangle's `v` pair ([the widget background and its atlas sets](the-widget-background-and-its-atlas-sets.md) §3).)*

## 7. What is not read

| function | bytes | what is known |
|---|---:|---|
| `00245170` | 927 | called by `00245E60` when flag bit 8 is **clear**; calls `002DA7C0`, `002DAC70`, `002DAF30`, `002DD4B0`, `002DD7B0` and the palette `002DD7E0` |
| `002455A0` | 2,232 | called when bit 8 is **set**; the same callee set **plus `002DA2D0`** |
| `002DA2D0` | 1,262 | a primitive with the same three callees as `002DA7C0` (`00181460`, `00181890`, `00202B70`); **three callers** |

**The pair `00245170` / `002455A0` is the same shape as the two nine-patch dispatchers** — one
routine and its richer variant, selected by a flag. **That is a pattern, not a reading**: it is
stated because it is the third time this subsystem has shown it, and it is what the next reader
should try to falsify first.

*(Reconciled 2026-09-30, SWE2-DATA: all three are now read on [the widget background and its atlas sets](the-widget-background-and-its-atlas-sets.md) §6 and §6b. The pattern held: `002455A0` is `00245170`'s richer variant, with a drop shadow and `002DA2D0` as a second primitive. Flag bit 8 picks between them only when bit 7 is set and bit 24 matches the pass (`002461BB`–`002461F0`, `_index/candidates/dd-data-3-0930/widget_draw_checks.py` W3).)*

## 7b. Key addresses (SWE2-DATA, 2026-09-30)

| address | role |
|---|---|
| `00245E60` | the recursive draw pass: gate, transform, clip, background, messages, children |
| `002450B0` / `00245110` | the two draw brackets: they set the pass index `0208F564` to 0 / 1 and walk the tree |
| `00245170` / `002455A0` | the background drawers, picked by flag bit 8 |
| `002DA7C0` / `002DA2D0` | the textured-quad primitives |
| `00249EE0` | the rectangle intersection used for both clips |
| `002435C0` | the typed-list draw run on node `+0x50` |
| `009151C0` / `009151D8` / `009151F0` | the message records 3, 4, 5 |

## 7c. Call chain (SWE2-DATA, 2026-09-30)

```
MainLoop_Draw and twelve sites -> 002450B0 (pass 0)     00252990 -> 00245110 (pass 1)
  -> 00245E60 on root 0208EC90
       -> 00245170 / 002455A0 -> 002DA7C0 (and 002DA2D0)
       -> node handler [node+0]: messages 3, 4 (before / after content), 5 (after children)
       -> 002435C0 (typed list at node +0x50)
       -> 00245E60 for each child (node+0x18 first, +0x20 next)
```

The bracket callers are from [the cutscene name-slot page](Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md); the rest are this function's call sites (`_index/candidates/dd-data-3-0930/widget_draw_checks.py`).

## 7d. Modding notes (SWE2-DATA, 2026-09-30)

- Clearing bit 0 or bit 2, or setting bit 10, of a node's `+0x40` flags hides the node and its whole subtree.
- Bit 24 decides which of the two bracket passes draws the node's background and sends it messages 3 and 4. Its children are walked in both passes, so a child can draw in the other pass.
- A scaled quad is filtered and an unscaled one point-sampled (§6), so a UI mod that resizes a widget's destination rectangle also softens it.

### Evidence (SWE2-DATA, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| the `0x405` gate and the tree walk | `00245E88`–`00245E9D`; `0024635C`–`00246386` | 1 |
| the message gates (bits 24, 28, 12) and the pass index | `_index/candidates/dd-data-3-0930/widget_draw_checks.py` W1, W2 | 1 |
| the background gate and the bit-8 choice | `_index/candidates/dd-data-3-0930/widget_draw_checks.py` W3 | 1 |
| the transform gates | `_index/candidates/dd-data-3-0930/widget_draw_checks.py` W4 | 1 |
| the textured quad's filtering bit | §6, decompilation | 2 |
| message positions 3/4/5 | [the widget message protocol](../16-UI/Widget-Object-Model/the-widget-message-protocol.md) | 1 |

## 8. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the recursion really a tree walk and not a retry loop? | `for (child = node[3]; child; child = *(long *)(child + 0x20))` with the recursive call taking `child` — **a different object each iteration**, and the link field is at a different offset from the child field. |
| Are `009151C0` / `D8` / `F0` really ids and not strings? | Read as memory: `03 00 00 00` then twenty zero bytes, then `04`, then `05`, **24 bytes apart**. No printable content. |
| Is the subtree really skipped when the gate fails? | The `for` loop is **inside** the `if ((flags & 0x405) == 5)` block. **A failing node's children are never visited.** |
| Is the clip really composed, or are the two tests independent? | The second intersection takes the **result of the first** as one operand (`Rect_Intersect(&clip, &clip, &own)`). **Composed.** |
| Is the pivot really the centre? | `-(w * 0.5)` and `-(h * 0.5)` are written into the transform's translation, and `rect.x + w*0.5` into a global pair used by the multiply. **Half-extents on both axes.** |
| How much of this is anchored? | **`00245E60` has a zero-byte body in the live program**, so `search_instructions` cannot see it — a search for `0x405` scanned 567,156 instructions and returned seven hits, **none of them the `and eax, 0x405` at `00245E92`.** The gate was read with `disassemble_bytes`; the rest of §2–§5 rests on decompilation. **This is the fourth function in this folder with that property.** |
| Is the filtering bit this document's inference or the glyph document's? | **The rule here is read from this function** — an inequality on two rectangle fields setting bit 1 of a flags word. **The glyph document supplies what the bit is for**; neither derived the other. |

## 9. What this document does not claim

~~What messages `3`, `4` and `5` mean, or what else is in their 24-byte records.~~ ~~What `002435C0` does~~
~~with `node + 0x50` when its bit is set.~~ What the global `uRam_0208F564` selects — it is compared
against flag bit 24, so it partitions nodes into two sets that draw on alternate passes or contexts,
~~**and which is not established.**~~

*(Corrected 2026-09-30, SWE2-DATA: the protocol names the three messages by their place in the draw (before content, after content, after children), and the records' other fields are 0 ([the widget message protocol](../16-UI/Widget-Object-Model/the-widget-message-protocol.md)). `002435C0` is the typed-list draw, run on the list at node `+0x50` when its bit 0 is set ([the typed list](../02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md) §3; `_index/candidates/dd-data-3-0930/widget_draw_checks.py` W5). `0208F564` is the bracket's pass index: `002450B0` sets 0 and `00245110` sets 1 before each walk (W2).)*

- [x] **What the second bracket pass draws.** `00245110` sets pass 1 and is reached from `00252990`; a node draws its background and messages 3/4 only in the pass equal to its flag bit 24. Which widgets carry bit 24, and so what the player sees drawn in pass 1, is not traced. **SD-101** (SWE2-DATA, 2026-09-30). *(SD-101 answered 2026-09-30 by OPUS `b545fdb02`, [record](../_index/candidates/sd101-pass1-widgets-0930/README.md).)*
- [x] **What the two glyph emitters put in their commands.** `002DAF30` loads four rows from `02EBEFC0` / `02EBEFF0` into the shared workbench and emits through `00181560` / `001816F0`; `002DAC70` emits through `002DD350` and the `00181330` family (the 2026-09-18 note below). The command words each writes, and what they set on the GPU side, are not read. **SD-102** (SWE2-DATA, 2026-09-30). ~~What `002DAC70`, `002DAF30`, `002DD4B0`, `002DD7B0` do.~~ *(Read 2026-09-18, FABLE, the four small callees:* **`002DD4B0`** (7 B) returns the word `0215E6D0` — a flag `002DD4C0` sets to 1 and `002DD4A0` / `002DD420` clear to 0, which five glyph primitives test before touching the workbench (`002D9C40`, `002DAF30`, `002DB080`, `002DC290`, `002DD1E0`); **`002DD7B0`** (35 B) is the `fontcolor` shadow-byte getter beside the palette `002DD7E0` ([the blinking icon](the-blinking-icon-and-its-atlas.md) §5: `fontcolor.bin`'s colour pairs, grey wherever the file does not ship); **`002DAF30`** (324 B) tests that flag, loads four `xmm` rows from `02EBEFC0` / `02EBEFF0` into the shared workbench `022D8F30`–`022D8F60` and emits through the render-command helpers `00181560` / `001816F0`; **`002DAC70`** (690 B) emits through `002DD350` and the `00181330` / `001816B0` / `00181910` / `001819A0` command family and swaps the command buffer with `RenderCommand_SubmitCurrentBufferAndSwap` `003A1DB0`. So the four are the glyph run's emit side; what the two emitters put in the commands is not read.)* ~~Whether~~
~~the two unused 10-bit descriptor fields in §6 are dead.~~ *(Answered: they are the `v` pair, §6 note.)* *(SD-102 answered 2026-09-30 by OPUS `d1f7f06ac`, [record](../_index/candidates/sd102-glyph-emitter-commands-0930/README.md).)*

*(Pass 22 adjacency, 2026-09-14, tail rows: beyond the Movement note above — `002DD7E0` is
called by **save** `00581930`, `00203170` is called by **gameplay** `00339630` and **actor**
`003F1E90`, and `002465F0` calls **scheduler** `001EDDA0` (4 edges). The draw pass keeps pulling
shared helpers whose callers span layers; the pass reuses them, it does not own them.)*

*(Pass 22 live-graph completion, 2026-09-15: `001EDDA0` is also called by `Audio` `003B99D0`,
`00581930` calls `00225580`, `00338490` calls `Party` `003272A0`, `00339630` calls `0031B7E0`,
and `00339630` is called by `CombatAction` `00304850` (5 edges) — the draw pass's helpers are
consumed from audio, party and combat code like every other shared accessor on this page.)*

*(Pass 22 live-graph sweep 2, 2026-09-15: `003272A0` is called by `Spawn_Encounter_Lifecycle`
`00234AF0` (and one more, 2 edges) — the party callee is shared with spawn code.)*

*(Pass 22 live-graph sweep 3, 2026-09-15: `00234AF0` — the spawn caller noted above — calls
`RNG_Random_Selection` `00328370` (1 edge); the spawn body carries the random stream with it.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — SERVICE.** A cited function calls `BattleStats_ChangeStatusAndProcessSideEffects`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `AiOrder_CheckActionPreconditions`, owned by that layer, calls `00328370` on this page. That caller is the precondition check: a `0x650`-byte frame with a stack cookie into which it copies **twelve `0x80`-byte blocks** from the unit's `+0x80` before testing the order's `word[+0]` and signed `word[+2]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — SERVICE.** `00304850` on this page calls `BattleRuntime_ResolveAndCacheEffectiveActionId`, owned by that layer. What it reaches is the writing half of the effective-action-id pair: it resolves the same two definition tables - `0208D480` by `byte[+4]` when `byte[+5] == 0`, `0208DE80` by the owning unit's `byte[+0xEA9]` otherwise - and **stores** the recomputed id into the row's `word[+0x10]` when the unit's `word[+0x714]` is `0x9F`, returning `0xFFFF` when there is no owning unit at all; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Script_VM_Native_Bridge — CLIENT.** `FUN_00356160`, owned by that layer, calls `00203170` on this page. That caller is a 220-byte routine in a `0xA0`-byte frame with a stack cookie that asks the same object for two scalars and then a third of a different kind; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**Audio — MECHANICAL, 26 edges.** `003B99D0` calls `002DEE80`, `002DEF40`, `002DEFA0`, `002DF0F0` and 9 more; `00225580` is called by `00222740`, `00222F20`, `00223190`, `00223DA0` and 6 more; `001EDDA0` is called by `003B99D0`; `002DB080` calls `00182E80`; `00581930` calls `00225580`.

**CombatAction — MECHANICAL, 43 edges.** `BattleUnit_ResolveByFocusHandle` (`0031B7E0`) is called by `002FE660`, `BattleAction_CheckCurrentActionInterruptReason` (`002FFB60`), `BattleUnit_AdvanceStandardActionState` (`00304850`), `00305110` and 18 more; `BattleUnit_AdvanceStandardActionState` (`00304850`) calls `BattleAction_ComputeChargeLimitTicks` (`002F8410`), `BattleAction_ComputeChargeProgressStep` (`002F9C00`), `002FA1A0`, `BattleAction_ComputeEffectiveRangeBands` (`002FEB80`) and 15 more; `BattleUnit_AdvanceStandardActionState` (`00304850`) is called by `BattleUnit_AdvanceActionState` (`00307BE0`); `BattleAction_FindApproachGeometryAroundTarget` (`00339630`) is called by `BattleUnit_AdvanceStandardActionState` (`00304850`).

**Party — MECHANICAL, 8 edges.** `BattleUnit_AdvanceStandardActionState` (`00304850`) calls `BattleUnit_ResolveByFocusHandle` (`0031B7E0`), `PartyFocus_IsCurrentPackedActorHandle` (`003273B0`); `Spawn_TrySelectCandidatePosition` (`00234AF0`) calls `BattleUnit_GetPartyLeader` (`003272A0`); `BattleUnit_GetPartyLeader` (`003272A0`) calls `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`); `BattleUnit_GetPartyLeader` (`003272A0`) is called by `PartyControl_RecomputeSuppressionFromLeaderBattleState` (`0023B040`); `RNG_SharedGameplayLCG_NextU32` (`00328370`) is called by `BattleUnit_SeedPartyCombatStanceRecheckTimer` (`003081E0`); `PartyFollow_SolveFormation` (`00338490`) calls `BattleUnit_GetPartyLeader` (`003272A0`); `BattleAction_FindApproachGeometryAroundTarget` (`00339630`) calls `BattleUnit_ResolveByFocusHandle` (`0031B7E0`).

**Presentation — MECHANICAL, 350 edges.** `0039ADE0` is called by `00245E60`, `003A4290`, `003D92C0`, `004428F0` and 45 more; `001EDDA0` is called by `002F2530`, `002F3BC0`, `002F4020`, `003337B0` and 26 more; `00203170` is called by `00245E60`, `00258350`, `002B7B80`, `002DB080` and 26 more; `00181560` is called by `0022FFE0`, `00274CB0`, `0028D980`, `002AFDC0` and 21 more; `001816B0` is called by `0022FFE0`, `00274CB0`, `0028D980`, `002AFDC0` and 21 more; `00181910` is called by `0022FFE0`, `00274CB0`, `0028D980`, `002AFDC0` and 21 more; `00181330` is called by `00274CB0`, `002AFDC0`, `002DB080`, `002DBDD0` and 16 more; `00181890` is called by `0022FFE0`, `00274CB0`, `0028D980`, `002D9DB0` and 16 more; `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`) is called by `0024A710`, `002B0280`, `002DB080`, `002DC290` and 12 more; `00181460` is called by `002AFDC0`, `002D9DB0`, `002DA2D0`, `002DA7C0` and 10 more; `001819A0` is called by `002AFDC0`, `002DB080`, `003C4B20`, `003C6420` and 8 more; `002DD7E0` is called by `00245170`, `002455A0`, `0029A930`, `002B8EE0` and 6 more; `00398C50` is called by `00245E60`, `002DB080`, `003C2E60`, `003C37B0` and 6 more; `002DD4B0` is called by `00245170`, `002455A0`, `0029E840`, `0029ED50` and 3 more; `002DAC70` is called by `00245170`, `002455A0`, `002D0650`, `002D6990` and 1 more; `002DAF30` is called by `00245170`, `002455A0`, `002D0650`, `002D6990` and 1 more; `002DD350` is called by `003C2870`, `003C2E60`, `003C37B0`, `003C4B20` and 1 more; `002DD7B0` is called by `00245170`, `002455A0`, `002D0650`, `00506700`; `00245E60` calls `00245170`, `002455A0`, `00245E60`; `00249EE0` is called by `00245E60`, `002BCB00`, `003F1530`; `002DA7C0` is called by `00245170`, `002455A0`, `002D6990`; `003985B0` is called by `00245E60`, `003C4070`, `003C46B0`; `001816F0` is called by `002DB080`, `002DC290`; `002455A0` calls `002DA2D0`, `002DA7C0`; `002D9C40` is called by `0029E840`, `0029ED50`; `00181330` calls `001B03D0`; `00181460` calls `001B06D0`; `00225580` is called by `0029A930`; `002435C0` calls `0029ED50`; `002435C0` is called by `00245E60`; `00245170` calls `002DA7C0`; `00245170` is called by `00245E60`; `002455A0` is called by `00245E60`; `00245E60` is called by `00245E60`; `002DA2D0` is called by `002455A0`; `002DAC70` calls `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`); `002DB080` calls `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`); `002DC290` calls `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`); `002DC290` is called by `00392CE0`; `002DD1E0` is called by `00392A10`; `002DD350` calls `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`); `002DD420` calls `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`); `002DD4C0` calls `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`); `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`) calls `GraphicsCommand_PublishCompletedBatchState100` (`0036F360`); `003ED190` is called by `002F6AB0`.

**UI — MECHANICAL, 65 edges.** `002DD7E0` is called by `00280DE0`, `0028B140`, `002986E0`, `002A86A0` and 16 more; `00203170` is called by `00247AE0`, `002D2600`, `002D28E0`, `00368010` and 3 more; `002D9C40` is called by `002435C0`, `00243C00`, `0055AB20`, `0055AE80` and 1 more; `00249EE0` is called by `002D2600`, `002D28E0`, `00367AA0`, `003EE420`; `002DB080` is called by `005565E0`, `005574C0`, `0055A340`, `0055BAC0`; `00181890` is called by `002A0440`, `002D8D40`, `002D9380`; `00225580` is called by `002986E0`, `00299090`, `002C0400`; `00398C50` is called by `00368010`, `003C5500`; `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`) is called by `002AC5F0`, `002AF960`; `00181330` is called by `002A0440`; `00181560` is called by `002A0440`; `001816B0` is called by `002A0440`; `00181910` is called by `002A0440`; `001819A0` is called by `002A0440`; `001EDDA0` is called by `0024B9B0`; `002435C0` calls `002D9380`; `002435C0` is called by `002D28E0`; `00245E60` calls `002435C0`; `002465F0` is called by `00247AE0`; `002DD350` is called by `002A0440`; `BattleUnit_ResolveByFocusHandle` (`0031B7E0`) is called by `BattleMenu_BuildCommandEntryList` (`0031EB20`); `BattleUnit_GetPartyLeader` (`003272A0`) is called by `00318CD0`; `003985B0` is called by `00368010`; `0039ADE0` is called by `00247AE0`.

**WorldAreaField — MECHANICAL, 6 edges.** `Spawn_TrySelectCandidatePosition` (`00234AF0`) calls `FieldRegion_ContainsWorldPosition` (`002374E0`), `003209C0`; `002DC290` is called by `0057FB00`; `BattleUnit_GetPartyLeader` (`003272A0`) is called by `BattleSystem_RunFieldFrameOrchestrator` (`00234590`); `0033DB60` calls `FieldData_GetFormat0RecordVectorByIndex` (`00320940`); `003ED190` calls `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`).

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*
