---
system: The font painter's public API
category: 99-Unresolved-Residual
status: AUDITED
owner_layer: CodeDomain:Presentation.Text
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `001E9D20`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
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
  last_pass_state: api-surface-repos-55
  crossref_clean: true
  reopened_count: 0
---

# The font painter's public API

**Every function in FFXII that draws text goes through ~~eighteen~~ twenty-one entry points** *(corrected 2026-10-02, OPUS: a rel32 sweep finds 25 call sites of `001B5FA0` in 23 functions: 21 in the band, including `0017FC00`, `0017FC50` and `0017FC70`, which §2's table lacks, and the two consumers)*, and they were found
by one mechanical test rather than by judgement: **`001B5FA0` is the one-line accessor that returns
the font painter singleton `DAT_01F811F8`, so anything that calls it is holding the painter.**

**~~22 call sites, 18 distinct functions. Sixteen~~ 25 call sites, 23 distinct functions. Twenty-one sit in one contiguous band, `0017F650`–`0017FD30`.** *(corrected 2026-10-02, OPUS: rel32 sweep of `.text` for calls to `001B5FA0`)*
Two are elsewhere (`001C76E0`, `00184460`) and are consumers rather than API entries — they fetch the
singleton to use it, not to expose it.

> **The band is the interface.** Every one of the sixteen has the same three-line body: fetch the
> singleton, forward the arguments, return. **The whole text system presents itself as free functions
> over a hidden global**, which is why no caller anywhere needs a font-painter pointer.

## 1. What a modder is actually looking at

**This is the complete list of things the game can ask its text renderer to do.** Not a subset, not
the ones that happened to be documented — the closure of a call graph query.

If you want to know why a UI mod cannot make a caption do something, **the answer is that the verb is
not in this table.** There is no "draw string": the engine draws **one glyph at a time**, and
everything above — line breaking, markup, colour changes mid-sentence — is the caller's work,
performed against these eighteen calls.

## 2. The surface

| entry | forwards to | what it does |
|---|---|---|
| `0017F650` | `001E9C30` | set the **mode byte** `+0x2379` |
| `0017F7C0` | `001E8070` | **draw one glyph** — copies a 160-byte record and emits six vertices |
| `0017F850` | `001E8580` | **flush and present**, inside the profiler scope `"display : draw Font"` |
| `0017F880` | `001E93C0` | a metric — **fallback `23.0f`** when no font is loaded |
| `0017F8A0` | `001E9450` | a metric — **fallback `20.0f`** when no font is loaded |
| `0017F8C0` | `001E9860` | **codepoint → glyph index**, through an optional remap table |
| `0017F8E0` | `001E9780` then `001E9BD0` | a two-step measurement returning an `int` |
| `0017F920` | `001E9840` | a query with **two sources chosen by a flag** |
| `0017F940` | `005C52D0` | getter: `return *(qword*)(ctx + 0x28)` |
| `0017F960` | `001E9580` | a metric — **fallback `23.0f`**, font slot **3** |
| `0017F980` | `001E9610` | a metric — **fallback `20.0f`**, font slot **3** |
| `0017F9C0` | `001E9BD0` | scale a value by the font's own divisor |
| `0017FA10` | `001E9920` | **begin** — reset both records, take the two handles and the mode argument |
| `0017FAE0` | `00848C20` | setter: `*(qword*)(ctx + 0x28) = arg` |
| `0017FB00` | `001E9C80` | **set the 4×4 transform** — copies 64 bytes to `+0xE30` |
| `0017FC90` | `001E9C40` | **set the next glyph's corner gradient** (§4) |
| `0017FD00` | `001E9D20` | select, with the second argument fixed at **2** |
| `0017FD30` | `001E9D20` | select, with a caller-supplied owner key |

**The surface is ~~now closed — all eighteen implementations have been opened~~ not closed** *(corrected 2026-10-02, OPUS: three band entries that fetch the singleton, `0017FC00`, `0017FC50` and `0017FC70`, are not in the table)*. The three that were
listed as unread in this document's first version turned out to be the least surprising of the
eighteen: two more metrics and one setter (§5, §5b).

> **They were listed rather than omitted, and reading them changed one table and no conclusion.**
> That is the outcome the marking convention is *for* — the cost of naming an unread callee is a row
> in a table; the cost of quietly leaving it out is a surface that looks complete and is not.

**`0017FD00` passes three arguments to a four-parameter function.** Whether the fourth register
carries anything meaningful at that call is **not established**; the parameter is only consumed on
the claiming path.

## 3. Drawing one glyph takes a 160-byte record

`0017F7C0` null-checks its argument, copies **`0xA0` bytes** onto the stack, and hands the copy to
the emitter at `0017F82B`–`0017F836`. The record's layout, read from how the emitter indexes it:

| offset | contents |
|---|---|
| `+0x00`–`+0x07` | two floats — **source U** in the font texture |
| `+0x08`–`+0x0F` | two floats — **source V** |
| `+0x10`–`+0x1B` | three dwords — **not established** |
| `+0x1C`, `+0x2C` | four floats each — **screen X and screen Y per corner**, the two the bounding box tracks |
| `+0x3C`, `+0x4C` | four floats each — **contents not established**; they land in the vertex beside X and Y |
| `+0x5C`, `+0x6C`, `+0x7C` | four floats each — **per-corner colour weights** |
| `+0x8C` | four ints — **per-corner alpha**, in 1/128 fixed point |
| `+0x9C` | the palette index, taken **mod 28** |

**Eight parallel four-element arrays at stride `0x10`, one element per corner**, which is why the
emitter's inner loop reads `pfVar16[k*4]` for every attribute at once. `0x1C + 8*0x10 + 4 = 0xA0`
exactly.

## 4. A gradient across a single glyph, set and consumed once

`0017FC90(a, b, c, d)` takes four floats and writes four:

```asm
001E9C40  movaps xmm0, xmm2          ; xmm1 = a, xmm2 = b, xmm3 = c, [rsp+0x28] = d
001E9C43  movaps xmm4, xmm1
001E9C46  mulss  xmm2, dword ptr [rsp + 0x28]     ; b*d
001E9C4C  mulss  xmm1, dword ptr [rsp + 0x28]     ; a*d
001E9C52  mulss  xmm0, xmm3                       ; b*c
001E9C56  mulss  xmm4, xmm3                       ; a*c
001E9C5A  movss  dword ptr [rcx + 0x137c], xmm0   ; b*c
001E9C62  movss  dword ptr [rcx + 0x1384], xmm2   ; b*d
001E9C6A  movss  dword ptr [rcx + 0x1380], xmm4   ; a*c
001E9C72  movss  dword ptr [rcx + 0x1388], xmm1   ; a*d
```

**That is an outer product** — two pairs in, four corner weights out, and **each of the four inputs
is used exactly twice**. The emitter multiplies each corner's alpha by its weight (`001E82AD`), and
then **puts all four back to `1.0f`** at the end of every glyph — two `qword` stores of
`0x3F8000003F800000` at `001E8563` and `001E856A`.

> **So the engine can paint a gradient across one character, and the setting survives exactly one
> glyph.** A caller wanting a gradient across a whole word has to compute each character's four
> corners itself and call this before each one.

**This is the mechanism behind text that fades left-to-right or top-to-bottom within a line**, and
it is invisible from the emitter alone: from inside `001E8070` the multipliers look like state that
is mysteriously always `1.0`, because the function that sets them is the one that also resets them.

## 5. Two metrics, two different fallbacks

`001E93C0` and `001E9450` have the same five-step shape — fetch a font, bail with a constant, branch
on `001B1620`, divide by `001FDDB0` and `ceilf` — and **differ in exactly two places**:

**There are four of them, not two, and they are one function specialised along two axes.** Every one
has the identical five-step body — fetch a font by slot, bail with a constant, branch on `001B1620`,
divide by `001FDDB0`, `ceilf` — and they differ **only** in the slot number and the source call:

| | source `0079CFA0`, fallback **23.0f** | source `00225670`, fallback **20.0f** |
|---|---|---|
| **font slot 1** | `001E93C0` ← `0017F880` | `001E9450` ← `0017F8A0` |
| **font slot 3** | `001E9580` ← `0017F960` | `001E9610` ← `0017F980` |

> **Four of the eighteen API entries are one routine written four times.** The second argument to
> `001B51C0` is `1` or `3`.

**`001B51C0` is not an array index.** It is an **ordered-tree lookup** — the same red-black shape as
the selector's — walking from a root at `param_1 + 0x40` against a header node at `+0x30`, comparing
the key at node `+0x20`, and returning the node's value or `0`:

```c
while (n) { if (n->key < k) n = n->left; else { last = n; n = n->right; } }
return (last != header && !(k < last->key)) ? last->value : 0;    // 001B51C0
```

Measured against the shipping image 2026-09-19 (SWE2-EC7-69): the body (69 B) is exactly this —
root `qword[rcx+0x40]`, header sentinel `rcx+0x30`, children `+0`/`+8`, key compare at
`node+0x20`, value `node+0x28`, NULL on a header-terminal search. Interior anchor `001B51D0`
(the `cmp dword[r8+0x20], edx` key compare).

> **So `1` and `3` are keys into a map of loaded fonts, not slots in an array** — and a map has no
> obligation to use consecutive keys. **This document originally asked "why is `2` never requested",
> which presumed a dense array.** The question was withdrawn rather than answered.

| | `001E93C0` (`0017F880`) | `001E9450` (`0017F8A0`) |
|---|---|---|
| no-font guard | `001E93DE` | — |
| fallback loaded from | `001E9433` → `0090198C` = **23.0f** | `00901988` = **20.0f** |
| source call | `001E93EC` → `0079CFA0` | `00225670` |

> **Two hardcoded pixel sizes for text with no font loaded**, 23 and 20 — and **the two constants sit
> adjacent in memory**, `00901988` and `0090198C`, which is how a compiler lays out two literals from
> one translation unit. **Neither is an immediate**; both are `movss` loads, so a search for `41B80000`
> in the instruction stream finds nothing.

**The two sources are adjacent dwords on the font object:**

```c
undefined4 FUN_0079cfa0(longlong f) { return *(undefined4 *)(f + 0x30); }   // fallback 23.0f
undefined4 FUN_00225670(longlong f) { return *(undefined4 *)(f + 0x2c); }   // fallback 20.0f
```

> **This document originally asked "which of 23.0f and 20.0f is height and which is width."** Nothing
> establishes that the pair is height and width at all — they are **two adjacent font metrics**, and
> the pair could as easily be cell width and cell height, advance and line height, or ascent and
> descent. **The question presumed its own answer's shape and has been replaced** by the one the
> evidence supports: *what are the font fields `+0x2C` and `+0x30`?*

`001B1620` selects between the raw value and the value divided by the font's own divisor and rounded
up. **What that predicate tests is not established.**

## 5b. Two accessors that live six megabytes from everything else

`0017F940` and `0017FAE0` are the getter and setter for one qword at `ctx + 0x28`:

```c
undefined8 FUN_005c52d0(longlong c) { return *(undefined8 *)(c + 0x28); }
void       FUN_00848c20(longlong c, undefined8 v) { *(undefined8 *)(c + 0x28) = v; }
```

**Both sit far outside the `001Exxxx` band that holds the rest of the subsystem** — at `005C52D0`
and `00848C20`. The obvious guess is that they are generic accessors shared across the engine, **and
that guess is wrong: each has exactly one caller, its own wrapper.** They are font-painter code that
the linker placed elsewhere. **Why is not established**, and it is not identical-function folding —
folding would have given them many callers, not one.

> **An address far from its subsystem is not evidence of anything on its own.** The check cost one
> query each and killed a plausible reading that would otherwise have gone into this table.

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the singleton test really a complete API criterion? | It finds every function that *holds* the painter. **A wrapper that received the pointer as an argument would be missed** — but all sixteen band members fetch it themselves, and the two outliers are ordinary consumers. **Complete for this design, not complete by construction.** |
| Are all sixteen really three-line forwarders? | **No — two are not**, and the table says which: `0017F7C0` copies 160 bytes first, `0017F8E0` fetches the singleton **twice** and chains two calls. The rest are. |
| Is the glyph record 160 bytes, or does the copy over-read? | `param_1[0]`–`param_1[0x13]` inclusive is `0xA0`, and the stack block from `local_a8` to `uStack_c` is `0xA0`. **Two independent counts.** |
| Is `001E9C40` really an outer product and not four independent parameters? | Four products of two pairs, each pair used twice, in four consecutive stores. **`a` and `b` never appear together, nor do `c` and `d`.** |
| Do the corner weights really reset every glyph? | The two `qword` stores at the tail of `001E8070` write `0x3F8000003F800000` to `+0x137C` and `+0x1384`, covering all four. **Unconditional — not inside any branch.** |
| Could `0017F940`'s `+0x28` getter be reading something other than the descriptor? | `001E9780` reads `*(uint *)(ctx[5] + 0x20)`, and `ctx[5]` is the same `+0x28`. **The same slot is used as a descriptor pointer by a second function** — but what the descriptor is is not established here. |
| Are the fallback constants really 23 and 20, or did the decompiler render a load as an immediate? | **Both are `movss` loads from data**, and the bytes at `00901988` are `00 00 A0 41 00 00 B8 41` — `20.0f` then `23.0f`, read from memory rather than from the decompilation. |
| Are the four metric routines really identical apart from two tokens? | Read side by side: same call sequence, same branch, same `ceilf`. **The differences are the literal `1` vs `3` to `001B51C0` and the source function.** No other statement differs. |
| Is this document's evidence interior or entry-only? | **It was entry-only when first written** — 42 cited addresses, 0 interior, which is the exact false positive this project's own coverage checker warns about. Anchors were added afterwards for every load-bearing claim; **the three unread callees still carry none, and are marked unread rather than anchored.** |

## 7. What this document does not claim

**What the font-object fields `+0x2C` and `+0x30` are** (§5 — replacing a malformed question about
which is height and which is width). **What the font-map keys `1` and `3` identify** (§5 — replacing
a malformed question about why key `2` is unused). What `001B1620` tests. What the qword at
`ctx + 0x28` holds, or why its two accessors are placed outside the subsystem's band. What
`+0x3C`/`+0x4C` of a glyph record hold — **this document called them "two further position
components", which is an inference from where they land in the vertex, not something established.** What the three dwords at `+0x10` of a glyph record hold. What the
second pair of position components at `+0x3C`/`+0x4C` are for. Whether the fourth argument at
`0017FD00`'s call site is meaningful.

## 8. Related

- [painting-a-line-of-text-into-a-render-target](painting-a-line-of-text-into-a-render-target.md) —
  what `0017F850` and `0017FA10` do inside, and the record they share.
- [choosing-the-render-target-for-a-text-run](choosing-the-render-target-for-a-text-run.md) —
  what `0017FD00` and `0017FD30` select.
- [how-a-line-of-text-becomes-glyph-quads](how-a-line-of-text-becomes-glyph-quads.md) — the markup
  language and the callers that turn a string into repeated `0017F7C0` calls.

*(Pass 22 adjacency, 2026-09-14: the painter API crosses two layers — `00184460` is called by
**scheduler** `0022B8C0`, `001E8580` calls scheduler `001A1470`, and `001E8070` calls **audio**
`00225690` while `00225670` is called by `00222280` (4 edges). The font path yields to the
scheduler like the rest of the text walk, and the audio edges are the shared `0022xxxx` accessor
family, not font logic.)*

*(Pass 22 live-graph completion, 2026-09-15: `00225690` is called by `Platform` bodies
`0061F200`/`006209C0`/`0061F710`/`006239C0` (4); the scheduler body `0022B8C0` calls
`Movement` `00263560`/`0037CF00`, `Party` `00358BB0` and `Resource` `00324510` (4). The
painter API's neighbours fan out through the same shared helpers the rest of the walk uses.)*

*(Pass 22 live-graph sweep 2, 2026-09-15: the `CoreRuntimeScheduling` adjacency is wider than
the first note — `00184460` is called by `0022B8C0`, `001E8580` calls `001A1470`, `0022B8C0`
is called by `0022A580` and calls more scheduler bodies (13 edges); and `00263560` is called
by `ActorEntity` bodies `002628B0`/`0037B4D0` and four more (6). The paint path's scheduler
neighbour is itself a hub consumed by actor code.)*

*(Pass 22 live-graph sweep 3, 2026-09-15: `0037B4D0` calls `Gameplay` `00321380`/`002E9C00` (2
edges) — the actor caller of `00263560` reaches gameplay state like every actor body.)*

*(Pass 22 live-graph sweep 4, 2026-09-15: `002E9C00` is called by `CombatAI` `003014C0` (1 edge)
— the gameplay caller's own caller sits in the AI layer.)*

*(Pass 22 live-graph sweep 5, 2026-09-15: `003014C0` calls `RNG_Random_Selection` `00328370`/
`00308EC0` (2 edges) — the AI caller reaches the random stream like every combat body.)*

*(Pass 22 live-graph sweep 6, 2026-09-15: `00328370` is called by `Spawn_Encounter_Lifecycle`
bodies `00236450`/`002355A0` and three more (5 edges) — the random-stream accessor is shared
with the spawn layer; the hop chain ends there.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — SERVICE.** `003014C0` on this page calls `BattleAction_CheckActionAvailabilityReason`, owned by that layer. What it reaches is the action-availability cascade: bit 4 of `byte[+0]`, then the `+0x3C`/`+0x64` pair against `0x80000003` - and when that is set, the shared action-permission bit has to agree as well - followed by `byte[+5] == 1` and a `& 0x30` block on what `[+0x6A0]` points at; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — CLIENT (13 edges through 4 of this page's functions).** The Input layer reaches this page at `0022B8C0`, `0022A580`, `002628B0`, `00266D10`. `FUN_00226be0` is the worked example, read in full - it is a 1,936-byte channel step whose first act is to test `1 << channel` against the mask at `[01FD46D4]`; **1 of the 13 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Script_VM_Native_Bridge — CLIENT (5 edges, one fan-in).** All 5 edges are Script_VM_Native_Bridge bodies reaching `002E9C00` on this page. `FUN_0050ce70` is the worked example - it is a 77-byte verb body: it evaluates one operand, puts it through a second query, and passes both results on. The crossing is **one shared subject with 5 callers on that layer**, not 5 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**World — CLIENT (1 edges, one fan-in).** All 1 edges are World bodies reaching `00263560` on this page. `FUN_00266d10` is the worked example - it is a 1,185-byte area reset: it clears `byte[02099DE0]`, zeroes the `xmmword` at `02099DC0` and the two bytes at `02099DA4`/`02099DA5`, and then runs the per-area initialisation in fixed order. The crossing is **one shared subject with 1 callers on that layer**, not 1 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

## The `0017F8A0`/`0017F960`/`0017F980` exclusive-subtree cluster — all 3 roots bound (SWE2-FRONTIER, followup queue)

Three identical unconditional forwarders: `call 001B5FA0` (the font
singleton getter) then tail-jump to the member method on the returned
object — no null gate.

| root | member (forward target) | interior |
| --- | --- | --- |
| `0017F8A0` (21 B) | `001E9450` | [`0017F8B0`](../../_index/ADDRESS-INDEX.md) |
| `0017F960` (21 B) | `001E9580` | [`0017F970`](../../_index/ADDRESS-INDEX.md) |
| `0017F980` (21 B) | `001E9610` | [`0017F990`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001B5FA0`. The sibling `0017F9A0`
forwards to `001B5FB0`/`001B5210` the same way — these are the font
painter's public entry points into the `001Exxxx`/`001B5xxx` bodies.


### Interior citation — frontier hub `0017FC90` (2026-09-18, SWE2-EC7)

`0017FC90` — 97 B, 6 callers: the corner-gradient setter, read in full —
`001B5FA0()` resolves the paint context, then `001E9C40(ctx, xmm0..xmm3,
stack6)` receives all four floats plus the fifth lane at
[`0017FCD1`](../../_index/ADDRESS-INDEX.md). The §4 primitive the drawing
passes share.

### Interior citation — frontier hub `0017F8E0` (2026-09-18, SWE2-EC7)

`0017F8E0` — 50 B, 4 callers: the glyph-width query — `001B5FA0()` context *(corrected 2026-10-02, OPUS: fetched twice, at `0017F8E0`+0x8 and +0x19, once before each callee — §5's reading)*,
`001E9780(ctx, ecx)` at [`0017F8F2`](../../_index/ADDRESS-INDEX.md), then
`001E9BD0(ctx, result)` returns a float converted `cvttss2si` to int. The
pixel-width read the layout pass uses before breaking a line.
## SWE2-EC7-42 update (2026-09-19) - `006239C0`

`006239C0` (325 B) is the Platform yield body the group names - `00615BC0`/`005FD050`/`00861EBA`/`005FCF20` triple/`00225690`/`005CD7D0`. Interior anchor `00623A1A` (a `00615BC0` call).

## SWE2-EC7-49 update (2026-09-19) - `00222280`

`00222280` (191 B) is a body - `00221210`/`00221710`/`00225670`/`00225680` plus a `call [r9+0x18]` vcall. Interior anchor `002222B8` (a `00221210` call).

## SWE2-EC7-60 update (2026-09-19) - `001E9C80`

`001E9C80` (157 B) is a call-free 4x4 transform copy - 64 bytes `[rdx]` -> `[rcx+0xE30]` sixteen dwords (verifies the font-painters page's `+0xE30` claim). Interior anchor `001E9CA1` (the `+0xE38` dword store).


## SWE2-EC7-67 update - `001E9450`

`001E9450` (129 B) is a font-slot metric row - `001B5FB0`/`001B51C0`/`001B1620`/`00225670` x2/`001FDDB0` plus `00901988`. Interior anchor `001E9456` (a `001B5FB0` call).

## SWE2-EC7-67 update - `001E9580`

`001E9580` (129 B) is the font-slot-3 `0017F960` metric - `001B5FB0`/`001B51C0`/`001B1620`/`0079CFA0` x2/`001FDDB0` plus `0090198C`. Interior anchor `001E9586` (a `001B5FB0` call).

## SWE2-EC7-67 update - `001E9610`

`001E9610` (129 B) is the font-slot-3 `0017F980` metric - `001B5FB0`/`001B51C0`/`001B1620`/`00225670` x2/`001FDDB0` plus `00901988` (`001E9450` sibling). Interior anchor `001E9616` (a `001B5FB0` call).

## SWE2-EC7-87 update (2026-09-20) - `003DE320` painter-state seed measured

`003DE320` (36 B) is the three-field init the font-painter
callers run: `[02B58C38]` is zeroed, `dword[02B58C38]` takes
`0x01000101`, and `float[02B58C40]` takes 0.5f - the painter
defaults, call-free.
Interior anchor `003DE33B` (the `movss` store).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**Movement — MECHANICAL, 28 edges.** `0037B4D0` calls `00263560`, `002681D0`, `Actor_SetDesiredMovementHeading` (`0026A0D0`), `0026AF80` and 7 more; `002628B0` calls `00263560`, `0026A1D0`, `00379070`, `003791C0` and 2 more; `MainLoop_UpdateAndRenderFrame` (`0022B8C0`) calls `00263560`, `0037CF00`; `00263560` is called by `0026A1D0`, `0026A290`; `RNG_SharedGameplayLCG_NextU32` (`00328370`) is called by `00239210`, `00312DF0`; `0037CF00` calls `002E49B0`, `002E4A40`; `00226BE0` is called by `0026A1D0`; `00263560` calls `Movement_SetRequestedSpeed` (`0026D6F0`); `PartyFocus_CommitPendingPackedActorHandle_Thunk` (`00358BB0`) is called by `0026C3E0`.

**Party — MECHANICAL, 9 edges.** `00226BE0` calls `PartyRoster_GetActorBySlot` (`00263750`), `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`); `002628B0` calls `PartyFocus_ClearCurrentActorIfEligible` (`00358B40`), `PartyControl_SetMovementSuppressionBit` (`00359200`); `MainLoop_UpdateAndRenderFrame` (`0022B8C0`) calls `PartyFocus_CommitPendingPackedActorHandle_Thunk` (`00358BB0`); `RNG_SharedGameplayLCG_NextU32` (`00328370`) is called by `BattleUnit_SeedPartyCombatStanceRecheckTimer` (`003081E0`); `PartyFocus_CommitPendingPackedActorHandle_Thunk` (`00358BB0`) is called by `PartyRoster_AssignActorAndCommitFocusWhenEligible` (`0050C610`); `0037B4D0` calls `PartyRoster_IsFourSlotIndex` (`002647C0`); `0037CF00` calls `PartyRoster_GetActorBySlot` (`00263750`).

**Platform — MECHANICAL, 29 edges.** `00615BC0` is called by `001DD170`, `001DD420`, `0061F200`, `0061F710` and 2 more; `00225690` is called by `0061F200`, `0061F710`, `006209C0`, `006239C0`; `005CD7D0` is called by `0061F200`, `0061F710`, `006209C0`, `006239C0`; `005FCF20` is called by `0061F200`, `0061F710`, `006209C0`, `006239C0`; `005FD050` is called by `0061F200`, `0061F710`, `006209C0`, `006239C0`; `0061F200` calls `0061F200`, `0061F710`, `006209C0`; `0061F200` is called by `0061F200`, `00650D40`; `0061F710` is called by `0061F200`; `006209C0` is called by `0061F200`.

**Resource — MECHANICAL, 3 edges.** `MainLoop_UpdateAndRenderFrame` (`0022B8C0`) calls `00324510`; `002628B0` calls `0032E520`; `00324510` calls `0032E620`.

**Save_Load_Settings — MECHANICAL, 1 edge.** `002628B0` calls `SaveImage_GetPersistentPayloadBase` (`002EF2B0`).

**UI — MECHANICAL, 33 edges.** `0017FAE0` is called by `002AC5F0`, `002AE610`, `002AF340`, `002AF960` and 1 more; `0017F880` is called by `002A4830`, `002AC5F0`, `002AE610`, `002AF960`; `0017F940` is called by `002AC5F0`, `002AE610`, `002AF340`, `002B2150`; `0017F850` is called by `002AC5F0`, `002AF960`, `002D28E0`; `0017FA10` is called by `002AC5F0`, `002AF960`, `002D28E0`; `0017FB00` is called by `002AC5F0`, `002AF960`, `002D28E0`; `0017F8C0` is called by `002AF340`, `002B2150`; `0017FD30` is called by `002AC5F0`, `002AF960`; `0017F650` is called by `002D28E0`; `0017F8A0` is called by `002AF960`; `0017F920` is called by `002AC5F0`; `0017F960` is called by `002AF960`; `0017F980` is called by `002AF960`; `0017F9C0` is called by `002AC5F0`; `001A1470` is called by `0018EEE0`.

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-the-font-painters-public-api-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `001E9380` | 51 B | `0017FC50` + 0x10 | calls the site `001E9380` + 0x19 on each of 0x40 consecutive 0x38-byte elements starting at `rcx+0x1500` | Interior anchor `001E938A`; Interior anchor `001E9391`; Interior anchor `001E9399`; Interior anchor `001E939E`; Interior anchor `001E93A6` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted, continued)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-the-font-painters-public-api-h7-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `00213090` | 33 B | `001E9380` + 0x19 | stores byte 1 at `rcx+0x20` and the dword 0x3F800000 (the f32 bit pattern of 1.0) at `rcx+0x30`, `rcx+0x2C`, `rcx+0x28` and `rcx+0x24`, in that order, then returns | Interior anchor `00213094`; Interior anchor `0021309B`; Interior anchor `002130A2`; Interior anchor `002130A9` |
