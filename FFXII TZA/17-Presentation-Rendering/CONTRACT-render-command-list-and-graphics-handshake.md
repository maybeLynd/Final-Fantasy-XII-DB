---
contract: build a frame's render jobs as a list of heap objects, run them in two masked parts, apply the deferred settings commands, destroy them, and kick the command stream through the one shared word the graphics handshake is made of
category: 17-Presentation-Rendering
scope: subsystem
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md, 17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md
entries: ["0018B480", "0018AD00", "0018C9E0", "0018C610", "0018B100", "0018B1B0", "0018B040", "0018B810", "0018C8F0", "0036F2C0"]
registry_slots: []
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every body in sections 2, 3, 5 and 7 was disassembled from the authority image with
    disasm_fn.py on 2026-09-21 (OPUS) and is cited at an interior address. The handshake half is
    carried from an AUDITED page (`passes: 1`) and is SPOT-VERIFIED rather than re-derived - the
    settle-spin at `0036F2C0` and the `MainLoop_Draw` inline copy at `0022B2C0` were read here; the
    thread topology, the eleven-site census and the DMA reading are that page's and are cited to it.
    Where the list half's page did not survive the re-reading it is named in section 14 and filed in
    CONTRADICTIONS.tsv.
last_reviewed: 2026-09-21
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-29
  last_pass_state: opus-falsification-pass-1-2026-09-29-exe-73461d08
  crossref_clean: false
  reopened_count: 0
---

# Contract — the ordered render command list and the graphics handshake

> **Why this exists, and why it is one contract and not two.** S-39 carried **no contract at all**;
> its L2 verdict read `NOT MET` with the contract cell as the binding gap. Its two halves — the
> list ([the ordered render command list](Render-Command-List/the-ordered-render-command-list.md))
> and the handshake ([the shared command-state word](Graphics-Thread-Handshake/the-shared-command-state-word.md))
> — are separately well read. What neither states is the thing that binds them: **one frame's
> ordering**, from the enqueue that allocates a job through the two masked walks that run it, the
> flush that applies the deferred settings commands, the teardown that frees everything, and the
> word the command stream is kicked with. Every invariant below is a property of that ordering
> rather than of any one operation, which is the test this database applies to contract scope.
>
> **Provenance.** Sections 2–7 and 9–12 on the **list** half are **NATIVE/STATIC**, read here. The
> **handshake** half is carried from an AUDITED page and spot-verified; every claim about thread
> topology is that page's and is cited as such. Section 13 is **empty**: nothing here is observed
> live.

## 1. Purpose

The picture is built in layers and the layers must not fight. Rather than calling passes in
sequence, the frame **allocates a small object per job**, appends it to a list, and later walks the
list running each job's `execute`. Because the jobs are objects, a pass can be enqueued from
anywhere in the frame; because the walk is masked, turning one effect off never shifts the others.
When the jobs have run, the frame hands the resulting command stream to a graphics backend through
a single shared word — a protocol inherited from the PS2 that, on this build, **has nobody on the
other end**.

## 2. Interface

| | |
|---|---|
| entry point(s) | `0018B480` (85 B) make the **ordered list**, `0018AD00` (105 B) its constructor, `0018B4E0` (33 B) its getter · `0018C9E0` (95 B) make the **owning vector**, `0018CA40` (8 B) its getter · ~40 enqueue functions *(scope named 2026-10-02, OPUS: 36 builders - the `0018xxxx` callers of `0018AFF0`; 40 counts every appender, four of which allocate nothing)*, `0018C610` (148 B) the worked example · `0018B100` (173 B) the forward walk · `0018B1B0` (361 B) the reverse/class-filtered walk · `0018B040` (36 B) clear the ordered list · `0018B810` (159 B) destroy the objects · `0018C8F0` (233 B) flush-then-destroy · `0036F2C0` (43 B) the settle-spin clear |
| calling convention | Microsoft x64 throughout. `enqueue(rcx = owning vector, edx…= the command's own arguments)`; `0018B100(rcx = ordered list, dl = part, r8 = device)`; `0018B1B0(rcx = ordered list, rdx = device, r8d = class mask, r9b = reverse)`; the manager methods all take the list in `rcx`. |
| parameters | `0018B100`'s `dl` selects the half: **non-zero = part 1**, entries `[0, split)`; **zero = part 0**, entries `[split, count)` (`0018B11B`–`0018B138`). `0018B1B0`'s `r8d` is ANDed with each command's order key. |
| return type | The enqueue functions return nothing useful; `0018C610` **tail-jumps** into `0018AFF0` at `0018C69F`, so its result is that call's. The walks return `void`. |
| return semantics | Failure is silent everywhere. A failed `malloc` in an enqueue leaves `rbx = 0` (`0018C655`) and **a null is still appended to both lists**; both walks skip a null entry (`0018B159`, `0018B23F`). |
| callbacks / indirect dispatch | Every job runs through its own vtable: slot 0 `+0x00` destructor, slot 1 `+0x08` **execute**, slot 2 `+0x10` **order key**. The walks call slots 2 and 1 indirectly (`0018B164`, `0018B187`; `0018B247`, `0018B258`, `0018B26D`). The list's allocator is also virtual — `0018B320` calls `[allocator+0x10]` to allocate (`0018B36D`) and `[allocator+0x18]` to free (`0018B3AF`). |

## 3. Types

**There are TWO lists and they are not the same type.** This is the structural fact the pages blur
by calling one "the list" and the other "a SECOND list".

```
OrderedCommandList                 [01F7F5E0], 0x30 bytes, malloc'd at 0018B4AE
  +0x00  void**  pBegin
  +0x08  void**  pEnd               the push_back cursor
  +0x10  void**  pCapacityEnd
  +0x18  void*   allocatorVftable   an EASTL allocator object; 001EDF00 stores vtable 00902720
  +0x20  u32     classMask          0xFFFFFFFF at construction; bit 1 toggled by 0018B070
  +0x24  u32     forwardSplit       0 at construction; set by 0018B510
  +0x28  u8      splitArmed         0018B515 writes (arg != 0) here
  +0x29  u8      chrOpaqueActive    1 while a chr-opaque class-2 walk runs; see §14.2
  +0x2A  u8      afterwaterActive   1 while the chr-afterwater class-2 walk runs; see §14.2
  +0x2B  u8      (pad)              never written, never read; aligns reverseMark to +0x2C
  +0x2C  s32     reverseMark        0xFFFFFFFF at construction and on every clear; set by 0018B030

RenderCommandOwnerList             [01F7F5E8], 0x20 bytes, malloc'd at 0018C9FE
  +0x00  void**  pBegin
  +0x08  void**  pEnd
  +0x10  void**  pCapacityEnd
  +0x18  void*   allocatorVftable   same allocator construction, same discarded name

OrderedObject                       0x18 bytes base; subclasses are larger (0018C610 mallocs 0x20
                                    via ctor 001F1B80, which uses +0x18 for a subclass dword)
  +0x00  void*   vftable            3 slots in subclasses; base vtable 009010B8 has 7;   <- corrected 2026-10-02, OPUS - 009010B8 has 3 slots; the qword at 009010D0 is MapOrderedObject's complete object locator, and its vtable 009010D8 follows
                                    42 subclass vtables exist
  +0x08  void*   executeTarget      nullable delegate target: slot-1 execute trampolines
                                    load it and forward it as the callee's 'this' - see §14.3
  +0x10  u8      flushSelector      1 by default; ONE reader, at ~~0018C934~~ 0018C933 (pass 1) - see I-6
  +0x11  u8[7]   unobservedSpan0011 the base constructor does not touch it; no reader found
```

**The 0x30 is the allocation, not an inference:** `0018B4AB` is `lea ecx, [rbx + 0x30]` into
`malloc`, and `0018AD00` writes every field except `+0x28`/`+0x2B` and nothing past `+0x2F` —
`+0x2B` is never written anywhere. The 0x20 likewise
is `mov ecx, 0x20` at `0018C9F9`. **The two allocations are 0x10 apart in size and their globals are
8 bytes apart in `.data`**, which is exactly the coincidence that makes them easy to conflate.

**The allocator's name is authored and discarded.** Both constructors pass
`lea rdx, "EASTL vector"` (`0018AD2C`, `0018CA21`), and `001EDF00` **never reads `rdx`** — its whole
14-byte body stores vtable `00902720` at `[rcx]` and returns. The string is real evidence that this
is EASTL, and EASTL's allocator naming is compiled out in this build; it is not a name the running
program holds.

## 4. Preconditions · postconditions · invariants

**I-1 — OWNERSHIP IS SPLIT, AND ONLY ONE LIST OWNS.** ~~Every enqueue appends~~ The 36 owner-side enqueues append *(corrected 2026-10-02, OPUS: not every appender - `001E5270`+0x1A and `001F89B0`+0x1F tail-jump to `0018AFF0` with no owner push; the list page counts 40 = 36 + 4)* the same pointer to
both lists: to the owning vector inline (`0018C65C`–`0018C673`) and to the ordered list through the
tail call (`0018C68A`–`0018C69F`). **The owning vector destroys; the ordered list never does.**
`0018B810` walks `[01F7F5E8]` and calls each object's slot 0 with `edx = 1` — the scalar-deleting
form, so `free` runs (`0018B850`–`0018B860`). `0018B040`, the ordered list's clear, calls
`0018B3F0(list, 0)`, which only moves `pEnd` back to `pBegin` (`0018B43B`–`0018B46B`); it touches no
object. A reconstruction that gives either list ownership of the objects double-frees or leaks.
**The owner destroys in a second place too** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 312; bytes re-read.)*: the flush `0018C8F0`, used by the scene teardown
`001E0590`, first executes every entry whose `+0x10` is 0 (slot 1, `0018C930`–`0018C948`). It then calls
**slot 0 with `edx = 1` on every entry** (`0018C977`–`0018C987`), and finally empties the vector
(`0018C995`–`0018C9CB`). So a flush is also a destroy.

**I-2 — AND THE TEARDOWN ORDER FOLLOWS FROM I-1.** At ~~**both**~~ **all three** teardown sites the non-owning list
is cleared **first** and the owner destroys **second**: `0017CD53` then `0017CD60` in the frame
tick, `00188204` then `00188211` at the end of the render pass, and `001E05A9` then the flush `001E05B6` in the
scene teardown *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 312; bytes re-read.)*. That order is what stops the
ordered list from holding freed pointers for even one instruction. It is not incidental — it is the
same pair, in the same order, at ~~two~~ **three** independently written sites *(pass 1: the image-wide census of both
destroyers' callers finds exactly these three, each with the clear first)*.

**I-3 — THE ~~LIST~~ ORDERED LIST NEVER GROWS IN PRACTICE; THE OWNING VECTOR DOES.** `0018AD00` calls `0018B320(this, 0x1388)` at `0018AD48`
— a reserve of **5,000 entries** at construction. The grow path `001AB570` exists and the
push_backs branch to it (`0018C664`, `0018B004`), but ~~a frame would need five thousand commands to~~ only the ordered list's needs five thousand commands to *(corrected 2026-10-02, OPUS: the first cited branch is `0018C610`+0x54, the OWNING vector's push, whose capacity starts at 0, so its grow call `0018C610`+0x70 runs from the first enqueue)*
reach it. A reimplementation that reserves nothing is functionally correct and allocates on a path
the original never takes.
**The owning vector `[01F7F5E8]` is the opposite.** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 312; bytes re-read.)* `0018C9E0` creates it with begin, end and
capacity all zero (`0018CA10`–`0018CA19`), with no reserve. It therefore grows on push_back from the first
enqueue: OPUS's execution measured capacities 1 → 2 → 4 → 8 on the 1st, 2nd, 3rd and 5th enqueue.

**I-4 — THE ORDER KEY IS A MASK, NOT A SORT KEY, AND NOTHING SORTS.** Both walks read the list in
stored order. Slot 2's constant is **ANDed** — with the list's `classMask` in the forward walk
(`0018B167` `test dword ptr [rsi + 0x20], eax`) and with **both** the caller's mask and the list's
in the reverse walk (`0018B24A`, `0018B25B`). No comparator is called in any manager body.
*(The page's §4.3 still presents the key as placing `VideoObj` last; the correction is FABLE's
UQ-230 and is confirmed here instruction by instruction.)*

**I-5 — THE REVERSE WALK CALLS THE ORDER KEY TWICE PER ENTRY.** `0018B247` and `0018B258` are two
separate indirect calls to slot 2 on the same object, one per mask test, with the element re-loaded
from `pBegin` in between (`0018B24E`–`0018B251`). The forward walk calls it once.
*Sharpened by pass 1:* `0018B1B0` has **two** arms, split on `r9b` (`0018B1CB`), and its **forward** arm does the same:
`0018B2D3` and `0018B2E4`. So "twice per entry" is a property of `0018B1B0` in both directions, and "once" is
`0018B100`'s. A reimplementation
that caches the key has changed the call pattern even though every observed implementation of that
slot is a constant return.

**I-6 — `+0x10` IS NOT AN "ENABLED" FLAG.** It has exactly one reader in the family — ~~`0018C934`~~ **`0018C933`** *(CORRECTED 2026-09-29, falsification pass 1: the
4-byte instruction starts one byte earlier; `0018C934` is inside it)*, `cmp byte ptr [rdi + 0x10], bpl` with `bpl = 0` — and the flush **executes the entry when the byte
is ZERO** (`0018C937` jumps past the call when it is non-zero). Neither walk tests it at all. The
base constructor sets it to **1** (`00212CD5`), and exactly **four** command constructors clear it:
`001F1799`, `001F196A`, `001F1CE4`, `001F1E3E` — whose vtables are `009030B0`
`ApplyJsonForCutSceneObj`, `00903390` `EnableDofObj`, `009030D0` `ReadPresetDofForCutSceneObj` and
`009033B0` `SetDofObj`. **All four are settings commands, not draw jobs** — the JSON cutscene
overrides and the depth-of-field pair. So the byte selects *whom the flush applies*, and the four
classes it selects are coherent; reading it as an enable inverts its sense.

**I-7 — THE FORWARD WALK CAN TERMINATE EARLY, AND AMBIENT OCCLUSION IS WHAT TRIPS IT.** *Placement, *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 312; bytes re-read.)*:*
the test sits **after** the entry's mask test and **before** its execute (`0018B167` → `0018B16C`–`0018B17C` →
`0018B187`). So the first entry that passes the mask after AO has run is reached but **not** executed, and the
walk exits there.
`0018B16C`–`0018B17C`: when `byte[01DF08FC] == 0` **and** `byte[01F7F594] != 0`, the walk jumps to
`0018B192` — the **exit**, not the next entry. `01F7F594` is written by exactly two functions, and
one of them is `AmbientOcclusionObj::Execute`, whose last instruction before the epilogue is
`001F29A3` `mov byte ptr [01F7F594], 1` — on the path taken **only when AO actually ran**, since
both of its early-outs (`001F28C5`, `001F28D2`) jump past it. The render pass arms the mechanism
immediately before the part-0 walk — `00188103` tests `byte[renderParams + 0x199]` and, when set,
zeroes **both** globals (`0018810C`, `00188113`) — and restores `01DF08FC` after
(`00188132`–`00188144`). **So under one ~~authored switch~~ debug toggle, the developer console's "Display AO Only",
the second half of the frame's command list stops at the first job that runs after ambient occlusion.** Neither
page mentions this gate. *(GC-1 answered 2026-09-25, FABLE, Claude Opus 5.5. The engine's own label names it: developer-console command 42 is "Display AO Only:" ([the console's command names](../00-Engine-Core-Runtime/Developer-Tuning-Console/console-command-names.md)), and its arm flips `+0x199` of the same render-parameter block through a one-store setter whose only caller is that arm. A sweep of `.text` for byte stores at displacement `0x199` finds that setter and nothing else. Wider stores, such as a block initialiser, are outside the sweep. OPUS block 315's per-id run shows id 42 writing that byte and nothing else.)* *So the gate is how the engine shows the ambient-occlusion result alone: every
later job is skipped once AO has run. It is not a shipped rendering path. It is reachable only through the
console.*

**I-8 — TWO INDEPENDENT MARKS, NOT ONE.** `+0x24` bounds the **forward** split and is set by
`0018B510`: armed (`arg != 0`) it writes 0, otherwise it writes the current element count
(`0018B524`–`0018B52F`). `+0x2C` bounds the **reverse** walk and is set by `0018B030`, which always
writes the current count. `0xFFFFFFFF` in `+0x2C` means "no mark" and the reverse walk reads it as
"the whole list" (`0018B1E8`, `0018B214`). Both are reset by the clear (`0018B050`, `0018B057`).

**I-9 — THE NULL GUARDS ARE REAL AND THE ASSERTS ARE NOT.** The push_back's `test rdx, rdx` after a
capacity compare (`0018C66E`, `0018B00E`) is the hand-written EASTL shape, and both walks skip null
entries. But `0018B4E0` and `0018B480` compute a null test into `cl` and pass it to `0016D6A0`
(`0018B4F0`, `0018B49D`) — and **`0016D6A0` is `ret 0`, three bytes.** The assertion is compiled to
nothing; the getter returns whatever is in the global, including null.

**I-10 — THE HANDSHAKE WAIT NEVER WAITS.** The settle-spin is two loads of `02EBA3F8` into two
registers, compared, looping while they differ (`0036F2D0`–`0036F2DE`), and then one
`and [02EBA3F8], 0xFFFFFEF3`. Its inline copy inside `MainLoop_Draw` at `0022B2C0`–`0022B2CE`
**then calls the clearer at `0022B2D0`**, so the wait is performed twice on that path. Per
[the handshake page](Graphics-Thread-Handshake/the-shared-command-state-word.md) §7 (`CG-3`, `CG-4`)
every writer of the word runs on the main thread and the fence `02EAF6D8` has no writer at all, so
both spins agree on their first pass. **Keep the protocol for fidelity; never block on it.**

**Postcondition.** After a complete frame: the ordered list's `pEnd == pBegin`, its `+0x24` is 0 and
its `+0x2C` is `-1`; every command object allocated this frame has had slot 0 called with the free
bit set; the owning vector's `pEnd == pBegin`; and `02EBA3F8` has bits 2, 3 and 8 clear.

## 5. State

| | fields / globals | evidence |
|---|---|---|
| read | `[01F7F5E0]`, `[01F7F5E8]`; `byte[01DF08FC]`, `byte[01F7F594]`; `byte[01FD4A88]`; render params `+0x199` and `+0x49C`; `dword[02EBA3F8]` | `0018B4F5`, `0018CA40`, `0018B16C`, `0018B175`, `0017CD42`, `00188103`, `0018D630`, `0036F2D0` |
| written | `[01F7F5E0]` (`0018B4C8`), `[01F7F5E8]` (`0018CA32`), the two marks and the mask, `byte[01DF08FC]`/`byte[01F7F594]` (`0018810C`, `00188113`, `00188144`, `001F29A3`), `dword[02EBA3F8]` | as cited |
| allocated | the two lists, once each, through `malloc` `0085E730` (0x30 and 0x20); ~~one element array per list, 5,000 entries reserved~~ 5,000 entries reserved for the ordered list only (`0018AD00`+0x48), none for the owning vector, which `0018C9E0` creates empty (`0018C9E0`+0x30) *(corrected 2026-10-02, OPUS: I-3's dated note)*; **one command object per enqueue per frame** | `0018B4AE`, `0018C9FE`, `0018AD48`, `0018C632` |
| deallocated | every command object, once per frame, by slot 0 with the free bit — `0018B860` and `0018C987`. **The two lists themselves are never freed on any path read here.** | as cited |

**Reader/writer census** (`globals_index.py`; its blind spot is RIP-relative references only):

| global | writers | readers |
|---|---|---|
| `01F7F5E0` | `0018B480` only | `0018B480`, `0018B4E0` |
| `01F7F5E8` | `0018C9E0` only | `0018C9E0`, `0018CA40` |
| `01DF08FC` | `00187950` only | `00187950`, `0018B100` |
| `01F7F594` | `00187950`, **`001F28B0`** (`AmbientOcclusionObj::Execute`) | `0018B100` only |

## 6. Relationships

```
0017CCD0  the frame tick (237 B)
   gate byte[01FD4A88]
   0018B4E0 -> 0018B040          clear the ordered list          [non-owning]
   0018CA40 -> 0018B810          destroy every command object    [owner]

00187950  the render pass (3311 B), profile scope "render ordered objects" (008C5E28)
   0018B4E0 -> 0016D6A0 (the folded assert)
   0018B100(list, dl=1, device)  at 00187D05     part 1, [0, split)
   ...
   if byte[renderParams+0x199]: 01DF08FC = 0 ; 01F7F594 = 0      arm I-7
   0018B100(list, dl=0, device)  at 00188128     part 0, [split, count)
   restore 01DF08FC                              at 00188144
   0018B040  at 00188204   then   0018B810  at 00188211          I-2

001E0590  the scene teardown (79 B)
   0018B040  at 001E05A9   then   0018C8F0  at 001E05B6          flush, then destroy

enqueue (x40)   e.g. 0018C610   <- corrected 2026-10-02, OPUS - 36 builders; 40 counts the four appenders that allocate nothing
   malloc(0x18|0x20|0x28) -> class ctor -> 00212CC0 base ctor
   push_back onto the OWNER inline
   tail -> 0018AFF0(0018B4E0(), node)  push_back onto the ORDERED list

0018B1B0  the reverse / class-filtered walk - five callers, all in 001F0xxx/001F3xxx
   001F06D0, 001F3510, 001F3570, 001F3650, 001F36B0

the command stream          see Graphics-Thread-Handshake/the-shared-command-state-word.md
   0036F360 / 003A2D80 / 003A2E30   ->  [02EBA3F8] = 0x100
   the frame's settle-spins         ->  and [02EBA3F8], 0xFFFFFEF3
```

Substrate excluded as neighbours: `malloc` (`0085E730`), `free` (`00809950`), `memmove`
(`[008C2A40]`) and the folded stub `0016D6A0`.

## 7. State transitions

The command list is a per-frame object with four states and one strict cycle.

| previous | resulting | condition, and the exact test |
|---|---|---|
| absent | constructed | first call of `0018B480` / `0018C9E0` — `cmp qword [glob], 0` at `0018B4A2` / `0018C9EF`; the constructors run **once per process** |
| empty | accumulating | any enqueue; the ~~push_back's capacity test at `0018C660` never takes the grow arm in practice (I-3)~~ ordered list's push never grows in practice, but the owning vector's capacity test `0018C610`+0x50 takes the grow arm from the first enqueue *(corrected 2026-10-02, OPUS: I-3's dated note, capacities 1, 2, 4, 8)* |
| accumulating | split | `0018B510` via the wrapper `0018CB10` — the only caller |
| accumulating | marked | `0018B030` via the wrapper `001829F0` — the only caller |
| accumulating | part 1 run | `0018B100(dl != 0)`; entries `[0, split)` whose key ANDs with `classMask` |
| part 1 run | part 0 run | `0018B100(dl == 0)`; entries `[split, count)`, **subject to the early exit of I-7** |
| any | filtered run | `0018B1B0`, from five sites, forward or reverse, bounded by `+0x2C` |
| run | flushed | `0018C8F0` — executes every entry whose `+0x10` is 0, then destroys |
| run | torn down | `0018B040` then `0018B810` — I-2's ordered pair |
| torn down | empty | both `pEnd = pBegin`; `+0x24 = 0`, `+0x2C = -1` |

## 8. Script · resource · event interactions

**The settings commands are the authored-data seam, and they are exactly the four of I-6.**
`ApplyJsonForCutSceneObj` and `ReadPresetDofForCutSceneObj` apply JSON-authored render settings —
`JsonData/init.json` for the defaults and `JsonData/CutScenes/<scene>.json` (plus a `_2ndScreen`
twin) per cut, with absent keys falling back to `init.json`
([the list page](Render-Command-List/the-ordered-render-command-list.md) §6, UQ-232) —
and `EnableDofObj` / `SetDofObj` carry the depth-of-field state. **That those four, and only those
four, clear `+0x10` is the mechanism that makes them settings rather than draws**: the flush applies
them at teardown regardless of what the masked walks did.

**The per-effect switches are authored too**, in the render-parameter block `00193D50()`: `+0x198`
gates ambient occlusion, `+0x19A` / `+0x180` / `+0x3E8` the gaussian filter, `+0x199` arms the
early-exit of I-7 (**not authored**: it is the console's "Display AO Only" toggle, I-7), and `+0x49C` (read through `0018D630`) chooses which side of the `+0x2C` mark the
reverse walk covers.

**No script verb reaches this subsystem.** Nothing in the vocabulary enqueues, walks or clears
either list; the producers are all internal pass wrappers of 30–70 bytes.

## 9. Determinism

**RNG — none.** No body on this path draws from any generator.

**Timing / update ordering.** The whole cycle is one frame on one thread. The two walks are ordered
by the render pass and the teardown follows them; the frame tick's teardown is the fallback when the
render pass did not run (it is gated on `byte[01FD4A88]` at `0017CD42`). **Nothing here is
frame-rate dependent and nothing is interpolated.**

**Threading.** The push_back is unguarded — no lock, no atomic, no barrier — and so is the grow
path. The graphics handshake *looks* like synchronisation and is not: per I-10 and the handshake
page's `CG-3`/`CG-4`, all writers run on the main thread and the fence word has no writer, so every
settle-spin completes on its first pass. **A reimplementation that adds a real second thread here
must add the synchronisation too, because the original has none to inherit.**

## 10. Failure paths and edge conditions

1. **`malloc` returns null in an enqueue** → `0018C644` skips the constructor, `rbx = 0`, and **the
   null is appended to both lists anyway** (`0018C657`). Both walks skip nulls; the destroy pass
   skips nulls (`0018B853`). So the failure is absorbed silently and the frame draws one job short.
2. **A list global is null** → the getters return it; the folded assert (I-9) does nothing. The
   caller dereferences it.
3. **`split == 0`** → part 1 walks nothing and part 0 walks everything. This is the state the
   constructor and every clear leave behind, so a frame that never calls `0018B510` runs entirely in
   part 0.
4. **`+0x2C == -1`** → the reverse walk covers the whole list (`0018B1EB`, `0018B217`).
5. **Early exit (I-7)** → every remaining entry of part 0 is skipped, including the teardown-relevant
   ones; the teardown itself still runs, because it is not inside the walk.
6. **Capacity exhausted** → `001AB570` reallocates and moves. ~~Unreached in practice (I-3) and~~ Reached on the owning vector from the first enqueue (`0018C610`+0x70), so exercised every frame *(corrected 2026-10-02, OPUS: I-3's dated note)*.
   ~~therefore **untested by the shipped game**, which is a risk a reimplementation inherits.~~
7. **An entry with no vtable** is impossible by construction — the base constructor writes one
   before any list sees the pointer.

## 11. Observable behaviour

- **The engine names this operation itself.** `001880E7` pushes the profile scope literal
  `"render ordered objects"` (`008C5DD0`'s neighbour `008C5E28`) around the second walk, so the
  operation is visible by name in any GPU or CPU profile capture.
- **Turning `01DFE0C4` off** empties the execute bodies while the objects are still allocated,
  ordered and destroyed — the list machinery keeps running with nothing drawn.
- **I-7 is externally observable and is the differential test this contract most wants run**: set
  ~~the authored switch~~ console command 42, "Display AO Only", which sets render params `+0x199`, and observe that
  every command enqueued after the
  ambient-occlusion job stops running, while the frame still completes and tears down cleanly.
- **I-6 is observable too**: a depth-of-field or JSON settings command takes effect even on a frame
  whose class mask excluded it from both walks, because the flush applies it.
- Per-frame allocation is measurable: one `malloc` and one `free` per enqueued job, every frame.

## 12. Reproduction formula

```
enqueue(owner, args):                             # 0018C610 and ~39 siblings   # <- corrected 2026-10-02, OPUS - 35 siblings: 36 builders call 0018AFF0 from 0018xxxx
    node = malloc(0x18 | 0x20 | 0x28)             # 0085E730(size, 0, -1)
    if node: node = ClassCtor(node, args)         # which calls 00212CC0:
                                                  #   [node+8] = 0 ; [node] = vftable ; [node+0x10] = 1
    else:    node = NULL
    push_back(owner, node)                        # inline
    push_back(ordered(), node)                    # 0018AFF0, a tail call

push_back(list, v):                               # 0018AFF0 / inline
    p = list.pEnd
    if p < list.pCapacityEnd:
        list.pEnd = p + 8
        if p: *p = v
    else: grow_and_insert(list, p, &v)            # 001AB570 - never reached, see I-3   # <- corrected 2026-10-02, OPUS - reached on the owning vector from its first push (0018C610+0x70); only the reserved ordered list never grows

walkForward(list, part, device):                  # 0018B100
    if part: lo, hi = 0, list.forwardSplit
    else:    lo, hi = list.forwardSplit, (list.pEnd - list.pBegin) / 8
    for i in lo .. hi-1:
        e = list.pBegin[i]
        if not e: continue
        if (e.vftable[2](e) & list.classMask) == 0: continue
        if byte[01DF08FC] == 0 and byte[01F7F594] != 0: return    # I-7: RETURN, not continue
        e.vftable[1](e, device)

walkFiltered(list, device, mask, reverse):        # 0018B1B0, reverse arm
    m = list.reverseMark
    hi = (m == -1) ? count-1 : (renderParams[0x49C] ? count-1 : m-1)
    lo = (m == -1) ? 0       : (renderParams[0x49C] ? m       : 0)
    for i in hi down to lo:
        e = list.pBegin[i]
        if not e: continue
        if (e.vftable[2](e) & mask) == 0: continue                # first call
        if (e.vftable[2](e) & list.classMask) == 0: continue      # second call, I-5
        e.vftable[1](e, device)

clearOrdered(list):                               # 0018B040
    resize(list, 0)                               # 0018B3F0 - moves pEnd only
    list.forwardSplit = 0 ; list.reverseMark = -1

destroyOwner(owner):                              # 0018B810
    for e in owner: if e: e.vftable[0](e, 1)      # scalar-deleting: frees
    resize(owner, 0)

flushOwner(owner):                                # 0018C8F0
    for e in owner: if e.flushSelector == 0: e.vftable[1](e, device())
    for e in owner: if e: e.vftable[0](e, 1)
    resize(owner, 0)

frame:
    ... enqueues ...
    walkForward(ordered, 1, device)               # 00187D05
    if renderParams[0x199]: 01DF08FC = 0 ; 01F7F594 = 0
    walkForward(ordered, 0, device)               # 00188128
    clearOrdered(ordered) ; destroyOwner(owner)   # 00188204 ; 00188211  - ORDER IS I-2

settleSpin():                                     # 0036F2C0
    do { a = [02EBA3F8]; b = [02EBA3F8]; } while (a != b)
    [02EBA3F8] &= 0xFFFFFEF3
```

## 13. Runtime validation

**Empty. Nothing in this contract has been observed on a running game.** Every claim is static —
the shipping image. That is what holds this contract at `BEHAVIORALLY UNDERSTOOD`, and what §16
routes.

| claim | how it was observed live | date | result |
|---|---|---|---|
| — | — | — | — |

## 14. Unresolved

Each is registered in `OPEN-QUESTIONS.md`; the first three are new with this contract.

1. ~~**Why does ambient occlusion terminate the walk?**~~ *(answered: see §4 - GC-1 answered 2026-09-25, the console's "Display AO Only" view; 2026-10-02, OPUS)* I-7 is instruction-exact and its purpose is
   not in the bytes. *Resolved by:* the live probe in §11, or by reading what the render pass does
   between the two walks with the switch set. Routed to ASTRA.
2. **`+0x29`–`+0x2B` — RESOLVED (SWE2-CONTRACT).** The "u16 at `+0x29`" was wrong: it is two
   independent `u8` **pass-context flags** plus a dead pad byte, and the earlier "no reader" was
   a RIP-relative blind spot — every accessor reaches the list through getter `0018B4E0`, whose
   return pointer sits in a register. The mechanism: the class-2 walk drivers cannot pass a
   parameter through the `0018B1B0` → vtable-callback interface, so they arm a list byte before
   the walk and the re-entrant routine `001F5D70` reads it back.
   - **`+0x29` `chrOpaqueActive`** — armed `1` by the three chr-opaque pass drivers
     `001F3570` ("chr opaque objects render" + "map opaque objects render"),
     `001F3650` ("chr opaque objects render for mon"), `001F36B0` ("chr opaque objects render"),
     each around `0018B1B0(list, arg, classMask=2, r9b=1)`, cleared `0` after.
   - **`+0x2A` `afterwaterActive`** — armed `1` only by `001F3510` ("chr afterwater objects
     render") around the same class-2 walk shape, cleared `0` after.
   - **The sole reader `001F5D70`** samples both bytes at entry (`+0x29`→`[rbp+1]`, `+0x2A`→`edi`)
     and uses them twice: in the `this+0x4A4 == 1` path either flag nonzero early-returns
     (`001F635C`/`001F6366` → epilogue `001F68A0`); in the later per-entry pass the flags select
     the mode code stamped on each entry's `+0x98` — `4` when `+0x29`, `5` when `+0x2A`, the
     default arm otherwise (`001F6684`/`001F672A`/`001F67CD`).
   - **`+0x2B` is dead padding.** The constructor's `word [rbx+0x29]` covers `+0x29`/`+0x2A`
     only; `+0x2B` is never written anywhere, and a disp-`0x2B` census over all 56
     `0018B4E0`-caller functions finds zero operands — it exists to align `reverseMark` to `+0x2C`.
3. **`orderValue` (`+0x08`) — RESOLVED: NOT DEAD, AND NOT AN ORDER VALUE (GC-3, OPUS;
   confirmed SWE2-CONTRACT).** The field is a **nullable execute-target pointer** that two
   slot-1 execute bodies read and forward as the callee's `this`:
   `MapOrderedObject`'s `00212C60` (`mov rcx,[rcx+8]; test rcx,rcx; jne 001E2AF0` — the
   null-gated map draw delegate, also base vtable `009010B8` slot 5) and
   `CharacterOrderedObject`'s `00215320` (`mov rcx,[rcx+8]; jmp 001F5D70` — unconditional,
   the routine that reads the `+0x29`/`+0x2A` pass flags). RTTI complete-object locators
   carry subobject offset 0 for all three vtables, so `[rcx+8]` is this field unadjusted.
   The earlier "neither walk reads it" was correct about the walk *loops* but missed that
   the slot-1 dispatches they call are themselves the readers. **Residual:** where the
   pointer is assigned is not statically established — a bounded census (all 42 subclass
   ctor bodies, all 40 `0018AFF0` appenders, all 41 construction-site callers, the base
   vtable slots, `rep movs`/wide stores in those bodies) finds **no writer**; the field may
   be assigned through an aliased/computed path the census cannot see, or every shipped
   instance may keep the ctor's `0` (survivable for `00212C60`, which null-checks; for
   `00215320` it means `001F5D70(NULL)` — survivable only via the `[rax+0xA8]` early-out
   before `rsi` is dereferenced). Naming: `orderValue` → `executeTarget`; ordering itself
   is insertion order plus the slot-2 class mask (I-4).
4. **UQ-228's residue — what consumes the staging buffers.** The three publishers program a
   DMA-shaped sequence into one dword and hand the buffer to nothing traced; owned by
   [the handshake page](Graphics-Thread-Handshake/the-shared-command-state-word.md) §7.
5. **`CG-3`'s limit.** The Tk workers dispatch through per-thread callback tables that the thread
   walk could not follow, so "the main thread and no other party" is bounded by that.
6. ~~**The grow path is untested by the shipped game** (§10.6) and therefore unverifiable from~~ The grow path runs on the owning vector every frame (`0018C610`+0x70) *(corrected 2026-10-02, OPUS: I-3's dated note)*.
   ~~behaviour.~~

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| Two distinct list types, 0x30 and 0x20 | complete bodies of `0018B480` (85 B), `0018AD00` (105 B), `0018C9E0` (95 B); the two `malloc` sizes are immediates at `0018B4AB` and `0018C9F9` | 1 | PROVEN |
| I-1/I-2 — ownership and teardown order | complete bodies of `0018B810` (159 B), `0018B040` (36 B), `0018B3F0` (138 B); ~~both~~ all three call sites read in context (`0017CD53`/`0017CD60`, `00188204`/`00188211`, `001E05A9`/`001E05B6`), and they are every caller of both destroyers image-wide (pass 1) | 1 | PROVEN |
| I-3 — 5,000 reserved at construction | `0018AD40` `mov edx, 0x1388` into `0018B320`, whose body is the reserve | 1 | PROVEN |
| I-4 — the key is ANDed and nothing sorts | complete bodies of `0018B100` (173 B) and `0018B1B0` (361 B); no comparator call in either | 1 | PROVEN |
| I-5 — slot 2 called twice per entry in the reverse walk | `0018B247` and `0018B258`, with the element reloaded at `0018B24E` | 1 | PROVEN |
| I-6 — `+0x10` selects the flush's execute set | the sole reader ~~`0018C934`~~ `0018C933` (pass 1); the base store `00212CD5`; the four clearing stores `001F1799`, `001F196A`, `001F1CE4`, `001F1E3E` and the vtables they write (`009030B0`, `00903390`, `009030D0`, `009033B0`) | 1 | PROVEN |
| I-7 — the early exit, and AO arms it | `0018B16C`–`0018B17C` (the branch target is the exit at `0018B192`); `001F29A3` on the ran-path of `001F28B0`; the arming at `00188103`–`00188113` and the restore at `00188144`; `globals_index.py` shows `01F7F594` has exactly one reader | 1 | PROVEN |
| I-8 — two independent marks | `0018B510` (35 B) and `0018B030` (15 B), each with exactly one caller (`0018CB10`, `001829F0`) per `edges.tsv` | 1 | PROVEN |
| I-9 — the assert is `ret 0` | complete 3-byte body of `0016D6A0`; the two call sites `0018B4F0`, `0018B49D` | 1 | PROVEN |
| The allocator name is discarded | complete 14-byte body of `001EDF00`; `rdx` is never read | 1 | PROVEN |
| I-10 — the settle-spin, and the double wait | complete 43-byte body of `0036F2C0`; the inline copy at `0022B2C0`–`0022B2CE` followed by the call at `0022B2D0` | 1 | PROVEN |
| Thread topology; the eleven-site census; the DMA reading | [the handshake page](Graphics-Thread-Handshake/the-shared-command-state-word.md) §2, §7 (`CG-1`–`CG-4`, UQ-211), `audit.passes: 1` | carried, tier 1 at source | VERY HIGH |
| The pass → class map and the 43-class slot matrix | [the list page](Render-Command-List/the-ordered-render-command-list.md) §2.3, §2.5 and `members/ordered-object-vtable-slots.tsv` | carried, tier 1 at source | VERY HIGH |
| `+0x29`/`+0x2A` are u8 pass-context flags, `+0x2B` is dead pad | writer/reader bodies `001F3570` (arm `001F3582`, clear `001F3628`), `001F3650` (`001F3671`/`001F3696`), `001F36B0` (`001F36F4`/`001F3719`), `001F3510` (`001F3531`/`001F3556`), each around `0018B1B0` with `classMask=2`; reader `001F5D70` (`001F5DD6`/`001F5DE2`, guards `001F635C`/`001F6366`, mode-select `001F6684`/`001F672A`/`001F67CD`); ctor word store `0018AD50`; zero disp-`0x2B` operands across all 56 `0018B4E0`-caller functions | 1 | PROVEN |
| `+0x08` is a live nullable execute-target pointer, not an order value | readers `00212C60` and `00215320` read in full; base vtable `009010B8` slot map (~~7 slots, slot 5 = `00212C60`~~ 3 slots; `00212C60` is slot 1 of `MapOrderedObject` `009010D8` *(corrected 2026-10-02, OPUS: the complete object locator at `009010D0` ends the base vtable)*), `MapOrderedObject 009010D8` slot 1, `CharacterOrderedObject 00903940` slot 1; zero-subobject-offset RTTI locators `01CED7C8`/`01CEECD8`; no writer in the 42-ctor / 40-appender / 41-caller / rep-movs census — assignment path open | 1 | PROVEN (readers); OPEN (writer) |

**Superseded by this contract** — filed in `CONTRADICTIONS.tsv`:

- *Old:* `OrderedObject +0x10` is `enabled`, "on by default". *New:* its one reader executes the
  object when it is **zero**, and exactly the four settings classes clear it.
- *Old:* the two lists are "the list" and "a SECOND list" of the same kind. *New:* they are
  different types of different sizes with different roles — one owns, one is a masked view.
- *Old:* `0018B4E0` "asserts non-null". *New:* the assert is `ret 0`.

## 16. Parity plan

| dimension | tested how |
|---|---|
| **STRUCTURAL** | both list layouts and `OrderedObject` against §3; the two allocation sizes are the discriminator |
| **STATE-TRANSITION** | §7's table, especially the clear-then-destroy pair of I-2 and the two marks of I-8 |
| **CONTRACT** | I-5 (assert two slot-2 calls per entry in the reverse walk) and I-6 (assert the flush's selection) — both are invisible to an output comparison |
| **EDGE-CASE** | §10's seven paths, including the null-append of §10.1 and the `split == 0` default |
| **INTEGRATION** | the frame ordering of §12, with the teardown pair asserted at ~~both~~ all three sites |
| **TIMING** | only in the weak sense that the whole cycle is one frame on one thread; no phase-level claim is made |

**Not tested, and why:**

- **RNG** — nothing on this path draws.
- **CALCULATION** — there is no arithmetic here beyond pointer differences.
- **PRESENTATION** — what each `execute` draws belongs to the individual pass documents and to
  S-38/S-40, not to this contract.
- **SERIALIZATION** — nothing here is persisted.
- **FULL SUBSYSTEM** — cannot be claimed while §13 is empty, and the grow path (§10.6) cannot be
  claimed at all from a build that never reaches it.

## Falsification pass 1 — 2026-09-29 (OPUS): the machinery holds; one citation was a byte late

Every static claim was re-derived from the shipping image (`73461d08…`) by
[`falsify_render_command_list.py`](../../Tools/analysis-kit/gfz-scripts/falsify_render_command_list.py). Whole-image
sweeps decode every listed body. Each check states its killer first. `audit_crossrefs.py` ran on this contract first.

| check | killer searched for | result |
|---|---|---|
| R0 §2 | a different extent | survives: 19 bodies |
| R1 I-1 | an object call in the clear; a destroyer without the free bit | survives: the inline owner push at `0018C65C`–`0018C673` and the tail into `0018AFF0`; slot 0 with `edx = 1` at `0018B860` and `0018C987`; the clear path's only indirect call is `memmove` through its import slot |
| R2 I-2 | a destroyer called without the clear first, anywhere | survives, **image-wide**: exactly three destroy/flush sites, each preceded by its clear; the page's leftover "two" is corrected |
| R3 I-3 | a reserve on the owner; another reserve size | survives: `mov edx, 0x1388` into `0018B320` in the ordered ctor only |
| R4 I-4 | a comparator in either walk | survives: the key is ANDed (`0018B167`); the only direct calls are the render-parameter getter and the `+0x49C` reader |
| R5 I-5 | a single slot-2 call per entry | survives, **sharpened**: two per entry in both arms of `0018B1B0` (`0018B247`/`0018B258` and `0018B2D3`/`0018B2E4`); once in `0018B100` |
| R6 I-6 | a second `+0x10` reader; another base or clearing store | survives, **citation corrected**: the one reader starts at `0018C933`, and `0018C934` is inside it. `00212CD5` stores 1; the four clears carry their four settings vtables |
| R7 I-7 | an exit that is not `0018B192`; an AO store on an early-out path | survives: `jne 0x18b192`; `001F29A3` stores 1, and both early-outs jump past it; the arming at `00188103` and the restore |
| R8 I-8 | a setter with a second caller; a clear that keeps a mark | survives: `0018B510` ← `0018CB10` and `0018B030` ← `001829F0` only; the clear resets `+0x24 = 0` and `+0x2C = -1` |
| R9 I-9 | an assert that is not `ret 0` | survives: `C2 00 00` at `0016D6A0`, called from `0018B4F0` and `0018B49D` |
| R10 I-10 | a spin of another shape | survives: two loads, compare, loop, `and 0xFFFFFEF3`; the inline copy at `0022B2C0`, then the call at `0022B2D0` |
| R11 §3 | another allocation size; an allocator that reads its name | survives: `0x30` and `0x20`; "EASTL vector" at both sites; `001EDF00` never reads `rdx` |
| R12 §5 | another writer or reader of the four globals | survives, **whole-image**: exactly as tabled |
| R13 §6 | a sixth caller of `0018B1B0` | survives: the five cited |

**My own checks were wrong four times before the page was.**
- R1 looked for the owner in a global, where it is actually an argument.
- R4 counted the mark-side readers as comparators.
- R5 did not know `0018B1B0` has two arms.
- R6 expected the page's address.

The corrected script asserts the corrected facts.

**Crossref (audit_crossrefs): recorded rather than resolved.**
- Neighbour edges: Presentation 42, CoreRuntime 20, Resource 3, Audio 1.
- They arrive through the render pass `00187950`'s other callees, the heap allocator `001A1470`, the
  render-parameter getter `00193D50`, and the grow path `001AB570`, all named as substrate or neighbours in §6.

`crossref_clean` stays `false`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**CoreRuntimeScheduling — CLIENT, 20 edges: the frame's owner drives the list, and this contract owns the list.**
- **The frame tick** `0017CCD0` (`GameApplication` slot 4) and the scene teardown `001E0590` call this contract's
  list getters and clears (`0018B4E0`, `0018B040`, `0018CA40`, `0018B810`) and the flush `0018C8F0`.
- **The frame reset** `0017D6E0` calls `001E0590`. Both are frame-order bodies filed in the scheduling layer, as are
  `001E0590`'s leaves `001A14D0` and `001DB620`.
- **The handshake clear** `GraphicsSync_ClearSharedCommandStateBits` (`0036F2C0`) is called by
  `MainLoop_UpdateAndRenderFrame` and by six scheduler bodies (`0022A770`, `0022AF50`, `0022B000`, `0022B6E0` among
  them).
- **The render pass** `00187950` allocates through the heap singleton's `001A1470`.

When these run is owned by the main-loop pages (`game-application`, `CONTRACT-world-simulation-tick`). This contract
owns the list, its entries and the handshake bits.

**Resource — CLIENT, three edges, and none of them exclusive to this system** (as §6 already says):
- the render-parameter getter `00193D50` is also called from `001A7A50`;
- the vector grow `001AB570` is also called by the asset-header manifest parser `0019E7B0`;
- the re-entrant routine `001F5D70` resolves a path through the resource path-table lookup `002DF980`.

**UI — MECHANICAL, one edge.** The heap allocator `001A1470` has a UI caller, `0018EEE0`, like every other layer.

**Audio — LABEL-UNSUPPORTED, one edge.** The render pass `00187950` calls `00182E80`, the display object's
height getter (`[display+0x14]`, default `0x438`). The ledger files it under Audio, but nothing in it touches audio.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page and the cited pages read them; no new body read
(OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-contract-render-command-list-and-graphic-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0018B030` | 15 B | subtracts qword `+0` of `rcx` from qword `+8`, shifts the difference right arithmetically by 3 and stores the low dword at `+0x2C` | `0018B034`, `0018B037`, `0018B03B` |
| `0018CB10` | 28 B | calls `0018B4E0` with `rcx` unchanged and tail-jumps `0018B510(result, edx)` | `0018CB18`, `0018CB20`, `0018CB27` |
| `001A14D0` | 9 B | copies qword `+0x18` of `rcx` into qword `+8` | `001A14D4` |
| `00212C60` | 14 B | loads qword `+8` of `rcx` and, when it is non-null, tail-jumps `001E2AF0` with it as `rcx`; otherwise returns | `00212C64`, `00212C67` |
