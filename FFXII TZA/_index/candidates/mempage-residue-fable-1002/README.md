# Memory-page residue: arena backing, the second link pair, the `+0x0C1` nibble, and `00210EC0`'s callers (FABLE, 2026-10-02)

This record covers four pieces of residue on
[where-the-games-memory-comes-from.md](../../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md).
None of them has been answered or registered there yet. All of the work is static and reads the shipping exe only
(sha256 `73461d08…21f8`, checked by [mp_lib.py](mp_lib.py)). Each script names its method and controls in its
docstring, and its `.out` file is the output at the HEAD named at the end of this file. FABLE edits the page; this
folder does not touch it.

| item | page residue | result |
|---|---|---|
| 1 | §2 and intro: "the arena's backing is not established" | **ANSWERED** (static) |
| 2 | "where that second list is rooted" | **ANSWERED** (static) |
| 3 | CharacterRenderRecord `+0x0C1`: other writers, and the domain of the source nibble | **ANSWERED** for every receiver-identified writer. **NARROWED** to one static typing fact |
| 4 | "`00210EC0`'s caller-visible contract beyond malloc(n)" | **ANSWERED** (static) |

---

## 1. Where each arena's backing memory comes from

**Question.** The arena initializer `00369D30(id, block, size, slots)` carves a block that some other code obtained.
Which function obtains each block, and from which call site?

**Method** ([item1_arena_backing.py](item1_arena_backing.py), [output](item1_arena_backing.out)).
- M1: a raw E8/E9/jcc index of `00369D30`, plus rip operands, absolute qwords and RVA dwords that equal it.
- M2: the writers of the enable mask `022D89B8`, from a rip-operand census over all 38,161 listed bodies.
- M3: at each call, the id, block, size and slot count, read backward from the call site. A block loaded from a
  global is traced to the store into that global and the call that produced it.
- M4: the producers' bodies, and the import each one reaches, resolved through the PE import directory.
- M5: arena 12's only route, and that route's arguments in FABLE's decompiled US script corpus.

**Controls.**
- C1: boot `0022A0B0` gives exactly nine calls, with ids 2–9 and 11. This matches the page's table and EXP-142.
- C2: the shim's thunk `0085E730` resolves to `malloc` in `api-ms-win-crt-heap-l1-1-0.dll`, and the free shim's
  thunk `0019C590` resolves to `free`.
- C3: the mask census finds the initializer's own store at `00369DE7`.

All three pass (`FAILS 0`).

**Result.** `00369D30` has **13** aligned raw sites and no pointer route. The three RVA-dword copies are its unwind
entries, and there are 0 absolute qwords and 0 rip operands. The mask has exactly two writers: the initializer's OR
(`00369DE7`) and the clear in `0036D160` (`0036D169`).

| id | backing | obtained by | at | initialised at |
|---:|---|---|---|---|
| 2–9, 11 | CRT heap | `0036D240` (14-byte shim: `movsxd rcx, ecx` / `or r8d, -1` / `xor edx, edx` / `jmp 0085E730` → `malloc`). Each request is `size + slots` bytes | boot `0022A1E1`, `0022A1F2`, `0022A203`, `0022A214`, `0022A225`, `0022A236`, `0022A247`, `0022A258`, `0022A269` | `0022A2AE`–`0022A394` |
| 11 (regrowth) | CRT heap | the same shim. The request is 3.75 or 4 MiB, without the slot tail. The old block is released first through `0036D250` → `free` (`0037B419`) | `0037B420` in `0037B3D0` | `0037B43D` |
| 12 | **arena 6** in the shipped game | `0036A190` (`mov edx, 1` / `jmp 0036A1A0`), under the selection push `0036C1D0(source < 0 ? 6 : source, 5)` | `003E9AC2`, `003E9AC9` in `003E9AA0` | `003E9AEF` |
| 13 | arena 5, 1 MiB, tagged `EVTM` | `0036A190` under push (5, 5) | `0025A9D0`, `0025A9DA` | tail jump `0025AA21` |
| 14 | arena 5, 100 KiB (102,400 bytes) | `0036A190` under push (5, 5) | `0025AA70`, `0025AA7A` | tail jump `0025AAC1` |
| 0, 1, 10 | none | not initialised. No call site passes them, and only the initializer sets a mask bit | — | — |

Arena 12 has a single route. `003E9AA0`'s only raw site is the tail jump `0034D0AD` in `0034D080`, which is script
verb 0395 `setexpandvoicememory`. `0034D080` has no raw site, and the image holds one absolute qword of it, the
verb-table slot `01EF49C0`. The decompiled US corpus has 1,114 scripts. Exactly two of them call the verb, `byu_z9900`
and `rrp_z9900`, both with source −1 and a size of 1 MiB (1,048,576 bytes): source −1 → arena 6.

So the arena's own memory comes from the CRT heap through one shim. No `VirtualAlloc` call and no static region is
involved. The nested arenas are carved from arenas 5 and 6.

**Limits.**
- A call through a pointer assembled at run time would not be seen, though none of the pointer forms exist.
- Only the US decompiled corpus was read for the verb's arguments. The other eight language copies were not.

**Proposed page sentence (§2, replacing "Where the arena's backing is obtained … is not established on this
page", and the intro's "whose backing is not established"):**

> Every arena's backing is obtained at run time from the C runtime heap or from another arena. Ids 2–9 and 11 come
> from `malloc` through the shim `0036D240` at boot (`0022A1E1`–`0022A269`), and id 11 again when it regrows
> (`0037B420`). The nested ids come from other arenas through `0036A190`: 13 and 14 from arena 5 (`0025A9DA`,
> `0025AA7A`), and 12 from the arena named by `setexpandvoicememory`, which is arena 6 for the shipped argument −1
> (`003E9AC2`–`003E9AC9`). Ids 0, 1 and 10 are never initialised. The initializer has 13 raw call sites, and it is
> the only code that sets an enable bit (`00369DE7`). (Record: `_index/candidates/mempage-residue-fable-1002/`.)

---

## 2. Where the `+0x0C` / `+0x10` link pair is rooted

**Question.** The page says the second link pair exists and the coalescer uses it, but "what is NOT established is
where that second list is rooted". Which code writes and reads these links, and where does the chain start?

**Method** ([item2_phys_links.py](item2_phys_links.py), [output](item2_phys_links.out)).
- S1 is a width-aware sweep of the arena module: 76 listed bodies whose entries lie in `00369700`..`0036D300`. It takes
  every memory operand whose byte range overlaps header bytes `+0x0C`..`+0x13`, at any width. A dword load into `ecx`
  that feeds the decoder `0020E600` is tagged **DEC**. A dword store of the encoder `0020E620`'s `eax` is tagged
  **ENC**. Everything else is printed as `other` (35 operands, for example descriptor `+0x10` reads and slot-record
  qwords), so nothing is dropped silently.
- S2 works image-wide from the codec's raw call index: 4,371 decoder sites and 767 encoder sites.
- S3 reads the anchor stores.

**Controls.**
- K1: the page's coalescer citation `0036B235` is tagged DEC.
- K2: the header fill's `0036A4EE` and `0036A501` are tagged ENC.
- K3: the unlinker `0036C9D0` shows ENC stores.

All three pass.

**Result.** The module has **16 DEC** and **14 ENC** sites. The writers are:
- the header fill `0036A490`, which sets both links to `encode(0)` (`0036A4EE`, `0036A501`);
- `0036B7F0`, which inserts a block **after** a neighbour (`0036B853`, `0036B867`, `0036B87F`, `0036B895`);
- `0036B8B0`, which inserts **before** one (`0036B913`, `0036B927`, `0036B93F`, `0036B955`);
- the unlinker `0036C9D0` (`0036CA75`, `0036CA8A`, `0036CAA3`, `0036CAAB`). It re-points both neighbours, then
  resets its own links to `encode(0)` and writes `0xFF99`.

The insert helpers are called by the carve in `0036BC60`, by `0036B980`, `0036C290`, `0036C380` and by the realloc
path `0036CB00`.

The readers are:
- the free path `00369860` (`00369B49`, `00369B6B`);
- `0036ABE0`, and the bucket searches `0036ACE0` / `0036AE00`;
- the coalescer `0036B210` and the merge `0036B2C0`;
- the two insert helpers;
- the allocator (`0036BD6C`, `0036BD83`);
- the unlinker;
- the realloc path `0036CB00`;
- **the dump walker `0036A570`**.

**The chain has a fixed anchor: the descriptor's `+0x10`, the first block header.**
- Only the initializer writes it (`00369F74`). It sets `+0x90` and `+0x98` to the same header (`00369F8C`, `00369F95`)
  and then fills that header with null links (`00369FD4` → `0036A4EE` / `0036A501`).
- No module store rewrites descriptor `+0x10`. The other qword stores at `+0x10` go through `r14`, the backing block
  being zero-filled, or through `r11`, the stack.
- Descriptor `+0x10` is read by:
  - the emptiness check `00369760`, which compares it with `+0x90` and `+0x98` (`00369798`);
  - the 64 KiB bucket arithmetic (`0036AD12`, `0036AE32`, `0036B318`, `0036B359`, `0036B5FE`, `0036C916`, `0036C968`);
  - the walker. `0036A570` loads it (`0036A5C7`) and follows `+0x10` from block to block (`0036A72F`) until the
    decoded link is null.

So the second pair is a physical-order chain. Its root is the lowest block, held at descriptor `+0x10`, and both ends
are `encode(0)`.

Outside the module there are 1,565 codec sites on a `+0x0C`/`+0x10` dword, in 439 bodies. The same codec serves the
authored tables, so these sites cannot be told apart by offset. The script narrows them to bodies that call a module
function, touch an arena global (`022D7FD0`..`022D8F10`) or use the header magic. That leaves 5 bodies:
`003B1BA0`, `003EA710`, `00503D50`, `00503DE0` and `00503E30`. They were read. Their `+0x10` belongs to their own
records: an effect record, the ARD root, and a 28-byte node whose decoded `+0x10` is handed to the payload free
`003697F0`, so it holds a payload, not a header. No body reads the base cell `01F83530` inline.

**Limits.** The outside filter is a heuristic. An arena-header writer outside the module that neither calls the
module nor checks the magic would be missed.

The null ends rely on `decode(encode(0)) == 0`, which holds only when the base cell `01F83530` is 0: encode is
`sub ecx, low32(base)` and decode adds the full base. EXP-079 observed base 0 in the running game.

**Proposed page sentence (replacing "What is NOT established is where that second list is rooted … Recorded as open
below rather than assigned a root."):**

> The second pair is a physical-order chain, and it is rooted at the descriptor's `+0x10`, the first block header.
> Only the initializer writes that field (`00369F74`). The chain's ends are `encode(0)` (`0036A4EE`, `0036A501`). The
> dump walker `0036A570` starts there (`0036A5C7`) and follows `+0x10` (`0036A72F`). The emptiness check `00369760`
> compares it with `+0x90`/`+0x98` (`00369798`). The links are written only by the header fill `0036A490`, the
> insert-after / insert-before pair `0036B7F0` / `0036B8B0` and the unlinker `0036C9D0`. (Record:
> `_index/candidates/mempage-residue-fable-1002/`.)

---

## 3. CharacterRenderRecord `+0x0C1`: other writers, and the domain of the nibble

**Question.** OPUS ([consumer check](../opus-c1-workspace-1001/consumer-check.md), `b83439b6c`) showed that
`002E28E0` and `002E3110` store a source byte's upper nibble at `+0x0C1`. That leaves two questions:
- (a) Are there other writers, counting wider stores and stores through other base registers?
- (b) Can the source byte's bits 5..7 be set, which would make the accounting index 2 or more?

**Method** ([item3_c1_writers_and_domain.py](item3_c1_writers_and_domain.py), [output](item3_c1_writers_and_domain.out)).

(a) **A1** is an image-wide store sweep over all 38,161 bodies. It takes every write, through any base other than
`rsp`/`rip`, whose byte range covers byte `0xC1`:

| width | displacements that cover `0xC1` |
|---|---|
| byte | `0xC1` |
| word | `0xC0` |
| dword | `0xBE`..`0xC1` |
| qword | `0xBA`..`0xC1` |
| xmm | `0xB2`..`0xC1` |
| ymm | `0xA2`..`0xC1` |

Each hit is checked against the published CRR receiver census
([character-render-record-accesses.tsv](../../../17-Presentation-Rendering/Character-Render-Records/character-render-record-accesses.tsv),
cell and constructor seeds, CFG fixpoint): is the **site** receiver-proven, or does only the body appear there?
**A2** lists bulk writers in CRR bodies: `rep stos` / `rep movs`, and calls to the `memset` / `memcpy` import thunks.

(b) **B1** is a census of the nibble setter `002EBC90`: raw sites, pointer routes, and the `r8` value at each site.

**B2** takes every store whose byte range covers an element's byte `+0x10`. Element *k* is at context + `0x30`*k*,
for *k* = 0..5. Three sources are unioned:
- a linear register tracker that follows a `+0xC0` qword pointer. It covers 795 bodies: those that load the pointer
  themselves, and those that call one of the five small getters returning it (`002E97B0`, `00269E20`, `00269E40`,
  `006CB530`, `00802500`);
- the published SecondaryContext context and element censuses;
- the actor storage record census, for the inline context reached at record `+0x350`.

Each store is classified with a bit-mask evaluation of its source.

**B3** checks `002E3110`'s own read.

**Controls.**
- K1: both known byte stores (`002E29E9`, `002E33B3`) come back as receiver-proven census sites.
- K2 is a width check. Asked for byte `0xBF`, the same coverage test finds ResetDefaults' **dword** store at `+0xBC`
  (`0041F80A`).
- K3: the bulk scan finds ResetDefaults' 1,856-byte (`0x740`) memset (`0041F754`).
- K4: B1 finds `0026DF40`'s six setter sites, five calls and one tail jump.

All four pass.

**Result (a).** 736 stores cover byte `0xC1` across the image, in 537 bodies. By width: 20 byte, 27 word, 343 dword,
299 qword and 47 xmm. **Exactly 2 are receiver-proven CRR stores: the two known byte writers.**

Seven more lie in CRR-census bodies, at sites the census does not attribute to the record: `00371501`, `00371D34`,
`00372097`, `003B5850`, `003B66B4`, `003B9DF4` and `0053ABF6`. They are `movaps`, `movss`, qword and indexed-dword
stores. The record's `+0x0C0` is a byte bitfield, operated on only by byte and/or and test (`fields.tsv`), so a float
or qword store there would clash with the type.

The bulk writer is ResetDefaults' full-record memset, which writes 0. Two other bulk sites were checked. The factory's
`0041F509` and `0041F5E7` write the workspace buffer, not `r14`. The remaining 19 memset/memcpy calls in CRR bodies are
listed in the `.out` file, and their destinations were not traced one by one.

**Result (b).**
- The source byte is byte `+0x10` of a SecondaryContext element. The [party read-in page](../../../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md)
  §7 gives the element map.
- **B1:** the only store that ORs a value into the upper nibble is `002EBC90` (`shl r8b, 4` / `or byte ptr [rcx + 0x10], r8b`).
  It has 27 raw sites and no pointer route. **Every site passes a constant 0 or 1**, by `xor r8d, r8d`, `mov r8d, 1`,
  or `lea r8d, [rdx ± k]` on a known `edx`.
- **B2:** B2 finds 55 element `+0x10` stores: 54 through the tracker and 1 from the published element census.
  Every one with an identified receiver clears bits or sets only bits 0–3, except `002EBC90` itself. These are:
  - the reset `00265B60`, `(old & 4) | 0xB`;
  - `and 0xF`, in `002E3110`, `002E35B0` and `002EBC90`, and `or 0xB` in `002E3110`;
  - bit 0 from `and dl, 1`, in `002ECD50`, `002ECDC0` and `002ECE00`;
  - bit 1 in `003B70B0`, `003B7880` and `003B8090`;
  - bit 1 in `003B7770`, read by hand;
  - bit 2 in `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` (`0025E37E`), read by hand;
  - bit 3 from `and dl, 1` / `shl dl, 3`, in `002EBB80`.

  Two of these stores were read by hand, and the script re-checks every cited instruction against the bytes:
  - At `0025E37E`, `sil` is 0 or 1. `ebp` is zeroed at entry, every path passes `mov esi, ebp` at `0025E255`, and the
    only later write is `and esi, 1`.
  - At `003B7833`, `r12` is 1. It is set once from the zeroed loop counter before the loop head.

  The actor storage record census has 0 of its 1,130 rows at record `+0x340`..`+0x47F`, so nothing reaches the
  context through the record itself.
- **B3:** in `002E3110` the `and byte ptr [rbx + 0x10], 0xf` at `002E3315` lies on every path that reaches the read at
  `002E3367`. The `rbx == 0` branch at `002E32E1` would fault on that read. The calls in between are `00269D60`,
  `002E8FD0` and `0042FB80`. Their transitive closure has 59 bodies and contains neither `002EBC90` nor any B2 store.
  **So `002E3110` always stores 0 at `+0x0C1`.** `002E28E0` stores element 0's nibble, which is 0 or 1.
- **The forwarded index is therefore 0 or 1 on every identified path.** `0036C5D0`'s credit stays within
  `022D8E10`'s two dwords. The value set is fixed by code constants, not by authored data, so no shipped data file is
  involved.

**Narrowed residue (static).** The tracker follows any `+0xC0` qword pointer, whatever its type. In 12 bodies it
reaches 17 wider stores at element `+0x10` offsets (word, dword, qword, xmm, plus one byte store from `sil`):
`00292390`, `002986E0`, `00299090`, `0029A0A0`, `002CBA50`, `00408780`, `0053E640`, `00558FB0`, `00561390`,
`00564E10`, `007DACF0` and `007E01F0`. Each load site is printed in the `.out` file. Three of the twelve are already
typed or ruled out:
- the type store types `00408780`'s pointer as `WidgetSingleton02B62D80`;
- `0029A0A0` is a widget message procedure, whose default arm calls `005C5230`;
- in `007DACF0` the "pointer" is a stack argument (`[rsp + 0xc0]`).

The other stores clash with the element's layout. Bytes `+0x10`/`+0x11`, the word `+0x12` and the floats `+0x14`..`+0x1C`
are all written by `00265B60`, and a word counter or a qword at `+0x10` would overwrite them. The missing fact is
static: **the type of the object whose `+0xC0` those 12 bodies load.** If it is not an actor, the answer is closed.

**Proposed page sentence (§"The closure qualified", replacing "Whether the shipped game ever supplies such a byte,
and whether other writers of `+0x0C1` exist, is not established statically."):**

> No other receiver-proven writer of `+0x0C1` exists. An image-wide sweep of stores at every width that covers the
> byte finds only `002E29E9` and `002E33B3` at CRR sites, and ResetDefaults' memset zeroes it (`0041F754`). The
> source nibble is written only by `002EBC90` (`shl r8b, 4`), and all 27 of its call sites pass 0 or 1. Other element
> `+0x10` stores touch bits 0–3 only. `002E3110` clears the nibble (`002E3315`) on every path to its read
> (`002E3367`), so it always stores 0. The index is therefore 0 or 1 on every identified path, and the credit stays
> in `022D8E10`'s two dwords. Not established: the type of the `+0xC0` object in twelve bodies whose wider stores land
> on element offsets (record `_index/candidates/mempage-residue-fable-1002/`).

---

## 4. `00210EC0`'s callers and the dead second argument

**Question.** Does any caller pass a second argument to `00210EC0`, or rely on its dead-argument form?

**Method** ([item4_malloc_forwarder.py](item4_malloc_forwarder.py), [output](item4_malloc_forwarder.out)).
- F1 reads the body: `or r8d, -1` / `xor edx, edx` / `jmp 0085E730` → `malloc`. Whatever a caller leaves in `edx` or
  `r8d` is overwritten before it could reach `malloc`.
- F2 is a raw E8/E9/jcc index, plus pointer routes.
- F3 finds the last writer of `rdx` and `r8` in the same basic block before each transfer, using capstone's register
  write lists. A one-operand `mul`/`div`/`cqo` that writes `rdx` is flagged as a side effect.
- F4 checks whether `rdx` or `r8` is read after a call before it is rewritten. A register is dropped from the check
  once it is written.
- F5 follows the address-taken route.

**Controls.**
- C1: F2 finds `0017D029`, which is in the edge table.
- C2 tests whether F3 can see a prepared argument at all. It runs the census on the two-argument sibling `0017D260`
  (`or r9d, -1` / `xor r8d, r8d` / jmp to the `_aligned_malloc` thunk), and **all 283 of its sites prepare `rdx`**.

Both pass.

**Result.**
- `00210EC0` has **258 raw sites in 181 functions**: 257 calls and one tail jump (`00221773` in `00221770`). The
  page's "81 frontier callers" is a frontier measure, not this count. There are no absolute qwords and no RVA dwords.
- One rip operand takes the address. At `0021082A` in `00210760`, `{00210EC0, 00210EB0 → free}` is built into a
  library allocator table and handed to `007A4D50`. That function's only caller is `00210760`. It stores the pair
  through `007AD620` (only caller `007A4E39`) into the cell `02EAD0B0`, which has one writer. The cell is called
  indirectly at four sites: `007AD47F`, `007AD4F0`, `007AD563` and `007AD5C4`. Each passes the size, plus the library's
  header and alignment bytes, in `rcx` alone, and keeps its own `rdx`/`r8` inputs in callee-saved registers.
- **No caller prepares `r8`.** The 11 in-block `rdx` writes are all the high half of a one-operand `mul`, the
  overflow-checked `new[]` size, not an argument.
- **No site reads `rdx` or `r8` after the call before rewriting it**, at a direct site or an indirect one.

So no caller passes or relies on a second argument. The caller-visible contract is `malloc(n)`.

**Limits.** F3 and F4 walk linearly inside a basic block, stopping at jumps, calls and jump targets. A value prepared
in a predecessor block and consumed by no instruction in the call's block would still be overwritten by F1's body, so
it could not matter.

**Proposed page sentence (replacing "NOT claimed: `00210EC0`'s caller-visible contract beyond `malloc(n)` — whether a
caller relies on the dead-arg form is not established."):**

> `00210EC0` has 258 raw sites (257 calls and one tail jump, `00221773`) in 181 functions. It has one address-taken
> use, `0021082A`, which installs it in a library allocator table that is called at four indirect sites in
> `007AD460`–`007AD5A0`. No caller prepares `r8`. The 11 in-block `rdx` writes are the high half of an
> overflow-checked `mul`, and no site reads `rdx`/`r8` after the call. No caller relies on the dead-argument form,
> so the contract is `malloc(n)`. (Record: `_index/candidates/mempage-residue-fable-1002/`.)

---

run: item1_arena_backing.py at 8c1f67c0d
run: item2_phys_links.py at 8c1f67c0d
run: item3_c1_writers_and_domain.py at 8c1f67c0d
run: item4_malloc_forwarder.py at 8c1f67c0d

## Consumer check (FABLE)

affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md`

- consumer: the memory page's intro, §2 backing paragraph, second-list paragraph, `+0x0C1` closure note and `00210EC0` note: revised-here (struck and restated by role; the addresses stay in this record so no new cross-layer citation lands on the page).
- consumer: the memory page's status line: revised-here (REOPENED -> PARTIAL; open: the `+0xC0` receiver type, static, and the arena blocks' run-time placement).
- consumer: OPUS's accounting-array closure (`opus-accounting-qualify-1002`) and the type store's CharacterRenderRecord `+0x0C1` row: agrees (index 0 or 1 on every identified path tightens, not contradicts, them).

run: item1_arena_backing.py, item2_phys_links.py, item3_c1_writers_and_domain.py and item4_malloc_forwarder.py at 8c1f67c0d (FAILS 0)
