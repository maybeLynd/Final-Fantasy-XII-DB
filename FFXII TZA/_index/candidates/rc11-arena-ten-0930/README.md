# RC-11: the arena-10 selection, an uninitialised arena, and the 15 register-passed pushes (ORACLE, 2026-09-30)

Static evidence only: shipping image `73461d08…` (`Database/Tools/work/exe/FFXII_TZA.exe`), the full game extract
(`D:/FFXII_TZA_extract`), and the shipped `.ebp` bytecode. Every script here runs from this folder, reads only, and
exits 1 if a control fails. All of them passed.

## The question

RC-11 (`_index/OPEN-QUESTIONS.md`, from `what-the-engine-fixes-at-boot.md`, the memory budget, id 10) asks three things:

1. Can shipped effect data reach the arena-10 selection at `00504398`? It sits in `00504350`, the loader for the
   `0x59` record kind, and is taken when the current effect context's first byte is 10 or more.
2. What does an allocation through the wrappers do when the selected arena was never initialised?
3. Which arenas do the 15 push sites select that SWE2-CONTRACT's `arena_select.py` left unresolved?

## Method

- `img.py`: shared image helpers (copied from `rc5-event-slot-routes-0930`).
- `riprefs.py`: every rip-relative reference to an address range, over every `.pdata` fragment. Control: the push's
  store to `022D89BC`.
- `basedisp.py`: the same census for image-base-indexed operands. Control: the map read at `0036C272`.
- `closure.py`: the direct call and tail-jump closure of the EFX parse `003EDAD0`, and every store to `02F97340`
  inside it.
- `reach59.py` (part 1): asserts, instruction by instruction, the only route to `00504350` and the context type
  that route can carry.
- `b00_census.py` (part 1, authored data): the record kinds that shipped effect streams store through chunk type
  `0xB00`. It uses FABLE's `type_census.py` walker unchanged.
- `uninit.py` (part 2): asserts the allocator path taken on an arena whose init bit is clear.
- `arena_sites.py` (part 3): OPUS's value-set dataflow `rc9_channels.py`, imported unchanged and pointed at
  `0036C1D0`, over all 135 push sites.
- `residue5.py` (part 3): closes the five sites the dataflow leaves open, by reading and asserting the instructions
  that feed them.
- `verb_census.py` (part 3, authored data): shipped bytecode calls of the script verbs whose argument reaches a push.

## Result

### Part 1: the arena-10 branch cannot run on shipped data

**The byte is the context's type.** `02F97340` holds the published effect context. Its byte `+0` is the type, which
`0024B3A0` copies from the constructor's `0x890`-byte template. The same byte indexes the per-type list heads
`020910A0[type]` (`0024B435`–`0024B457`).

**There is exactly one route to the loader** (`reach59.py` A1). The chain is:
- the parse `003EDAD0` → `003EE2D0` (at `003EE1F2`);
- `003EE2D0` → `003ED8A0`, for chunk flag `0x100` (`003EE39B`);
- `003ED8A0` → `003A9EF0`, for chunk type `0xB00` (`003EDAA0`);
- `003A9EF0` → `00504350`, either directly on a miss (`003AA109`) or through `00500980` on a hit (`00500A20`).

None of these entries has another reference. The only other hits are `.pdata` records, plus three chained-unwind
parent records for `003A9EF0` in `.rdata`.

**The parse runs only under a context its caller has just built** (A2–A4):
- The parse has exactly six callers, the same six functions that call `0024B3A0`.
- Each one stores a constant type into its template, then publishes the copy and parses it.
- None of them changes `02F97340` between the publish and the parse.

| constructor | type byte store | publish → parse |
|---|---|---|
| `002FC4A0` | 1 (`002FC541`) | `002FC54B` → `002FC5D2` |
| `0026FB90` (EFB) | 2 (`0026FC6C`) | `0026FC8A` → `0026FCEE`; `0026FC9F` republishes the same result |
| `003B38B0` | 3 (`003B3977`) | `003B39A4` → `003B39B3` |
| `003B29B0` | 4 (`003B2A60`) | `003B2A6A` → `003B2A75` |
| `003B0660` | 5 (`003B0730`) | `003B073A` → `003B0745` |
| `003B2220` | 7 (`003B2250`) | `003B2255` → `003B226D` |

**Nothing inside the parse changes the context on shipped data** (A5):
- In the parse's direct closure (1,124 bodies), the only store to `02F97340` is `0024ED87` in `0024ED80`.
- `0024ED80` is reached there only from `003EE2D0`'s arms for chunk flags `0x101` and `0x102`.
- `b00_census.py` C1 walks all 4,229 shipped EFX streams to their declared size, and every one of the 242,875 chunks
  carries flag `0x100`. Those two arms are never taken.

**The type is always below 10.** When `00504350` runs, the type is 1, 2, 3, 4, 5 or 7. So `cmp byte [ctx], 10`
(`00504392`) always takes the `jb` to `005043A7`, which calls `0036C1D0(8, 10)` and then `0036A190`. The engine's
own layout agrees (A6):
- the list heads `020910A0` hold 10 entries, and the next table `020910F0` starts `0x50` later;
- the parse reads the type as at most 9 (`003EDBA5`: `cmp al, 9`, then `bt 0x37D`).

**The loader does run on shipped data.** Shipped streams store 284 records of kind `0x59` (`b00_census.py`). They
are in 88 `.efx` files, 44 under `effect_finish/jp` and 44 under `effect_finish/us` (magic `m01xx`–`m03xx`, and
`event/e0195`). Controls: C2, all 40,750 `0xB00` kinds lie in the store's range `0x50`–`0x59`; C3, the `0xA00`
record total equals the published 48,868. **Every one of those loads selects arena 8.**

**A second, independent line of evidence** covers what the direct closure cannot see (indirect calls). Every value
ever stored to `02F97340` (`riprefs_02F97340.out`) is one of:
- a `0024B3A0` result;
- a context taken from the `020910A0` lists, through the lookup `0024F610` or the unlink `0024F410`;
- an owner's `+0x340` field, which its writers fill from `0024F610` or from a record's `+8`;
- a saved earlier value of `02F97340` being restored.

All the list-held and freshly built contexts carry one of the six constant types.

### Part 2: an allocation from arena 10 hangs the thread

This is `uninit.py`, all steps asserted.

1. **The push installs arena 10.** `0036C1D0(10, …)` raises stack 0's depth, then installs the active arena
   `022D89BC = map[10] = 10`. The map is identity.
2. **The wrapper asks the allocator.** `0036A100` (and `0036A1A0` / `0036A190`) calls `0036BC60(10, size, 0, …)`.
3. **The allocator refuses.** `0036BC60` does not take its no-selection spin (`0036BC87`), because the depth is at
   least 1. It picks descriptor `022D7FD0 + 10 × 0xA8 = 022D8660` and writes byte 1 at `022D8662`, the descriptor's
   `+2` live mark (`0036BCC5`). It then tests bit 10 of the init mask `022D89B8` (`0036BCD8`). The bit is clear, so
   it returns 0 without touching the free list.
4. **The retry spins forever.** The wrapper calls the retry `0036BFE0` with arena 10 (`0036A149`, `0036A1F0`). The
   retry's first act is the same bit test (`0036BFF8`). With the bit clear it falls into `jmp 0x36c000` at
   `0036C000`, a jump to itself.

**So the thread spins forever.** No block is returned, no header is stamped, and the matching pop `0036C140` never
runs. The one side effect is the stray mark byte at `022D8662`.

**Bit 10 is never set.** The mask has one store, `00369DE7` in the initializer `00369D30` (`riprefs_022D89B8.out`;
`basedisp_022D89B8.out` has none). No caller passes 10 (`../swe2contract-ddres-b1-0930/arena_ids.out`).

### Part 3: the 15 unresolved push sites

Controls, `arena_sites.py`:
- C1: all 135 sites in 109 functions are counted. One literal site, `002E6246` (arena 6), lies where the dataflow's
  decode does not reach, so it is taken from the linear decode.
- C2: `0025A990` resolves to 5.
- C3: all 120 literal sites contain their literal.
- C4: `00504398` resolves to 10.

The five dataflow-open sites are closed in `residue5.py` (42 assertions, RESULT PASS). The two verb-fed sites also
use `verb_census.py`. Its controls: C1, `skipexec` is found (171 calls); C2, `setexpandvoicememory` is found; C3, the
call-opcode total equals FABLE's full histogram, 25,794,237.

| function | site | arena(s) | how |
|---|---|---|---|
| `00249210` | `002492B4` | 2, 3 | the 4th argument. 23 callers resolve to 2 or 3. The pass-throughs `00249180` and `002493D0` resolve to 2 or 3 as well, except three memory reads, each 2: the stack record at `002B7CEF` / `002BB0F7` / `003CB5CB`; the `.rdata` table `00D23658`; and `[rsp+0x20]` at `00563325` |
| `002497E0` | `002497ED` | 2 | the 1st argument (dataflow; 8 callers) |
| `00249810` | `0024981D` | 2, 3 | the 1st argument (dataflow; 8 callers) |
| `0026FAD0` | `0026FB22` | 8 | `lea ecx, [rax+8]` with `rax` = 0 |
| `00377DC0` | `00377FA3` | 6 | `lea ecx, [rdx+1]` on the path from `00377F24` |
| `00384420` | `00384466` | 3, 4 | the 4th argument. `00238260` passes 3 and `003843F0` passes 4; `002385D0` passes `008478A0()`, whose body is `mov eax, 3; ret` |
| `003DD4C0` | `003DD5A1` | 11 | `lea ecx, [rax+9]` with `eax` = 2 |
| `003DF440` | `003DF4B4` | 6 | `lea ecx, [rax+6]` with `rax` = 0 |
| `003E9AA0` | `003E9AC2` | 6 on shipped data | the argument if it is 0 or more, else 6. The only caller is the handler of `setexpandvoicememory` (0x0395) `0034D080`, which passes the script's first argument. All 10 shipped calls (`byu_z9900`, `rrp_z9900` ×9 locales) push -1 |
| `003E9F80` | `003EA031` | 2, 12 | 12 when `[02B5E0B0]` is non-zero, else 2 |
| `003EC8D0` | `003EC8DD` | 6 | the 1st argument (dataflow) |
| `003EC910` | `003EC924` | 6 | the 1st argument (dataflow) |
| `003EDAD0` | `003EDE9B` | 8 | `lea ecx, [rdx-2]` with `edx` = 10, on the jump from `003EDE56`: the `(8, 10)` selection of the parse |
| `0050D8F0` | `0050D93F` | none on shipped data | a popped script int, so any value. It is reached only through the debug verbs 0x2003 / 0x2004 (`debug_tkmalloc`), which shipped bytecode calls 0 times |
| `0050DAD0` | `0050DB1F` | none on shipped data | the same, through 0x2008 / 0x2009 (`debug_tkmallochandle`), 0 shipped calls |

**No push site selects arena 10 on shipped data.** `00504398` is the only site whose value set contains 10, and
part 1 shows it never runs there.

Over all 135 sites the selected arenas are 2, 3, 4, 5, 6, 8, 9, 11, 12, 13 and 14 (`arena_sites.out`, `arena_sites.tsv`).
Every one of them has an initializer call.

## Verdict

**ANSWERED.**
- The arena-10 branch is unreachable with shipped data. The context type is always 1–5 or 7, so every one of the
  284 shipped `0x59` records selects arena 8 instead.
- An allocation from the never-initialised arena 10 hangs the thread. `0036BC60` marks descriptor byte `022D8662`
  and returns 0, and the retry `0036BFE0` spins at `0036C000`.
- The 15 sites select 2, 3, 4, 6, 8, 11 and 12 as tabled. Two debug-verb sites are script-fed and never called by
  shipped scripts.

## Not claimed

- **Indirect calls inside the parse closure are not followed.** It has 911 indirect sites, mostly import thunks and
  jump tables. The value-domain argument in part 1 covers them, with this residue:
  - the owner `+0x340` values taken from a record's `+8` (`002FCE4E`, `003B1D1F`);
  - the argument of `003B3480`.

  These are read as contexts, but their writers are not enumerated here.
- **What the `0x101` / `0x102` chunk arms would do is not claimed.** Their owner globals `02096B98` and `02096C70`
  have no writer on either census form (`riprefs_02096Axx.out`, `basedisp_02096Axx.out`). Shipped data never takes
  those arms.
- **Script-fed values are bounded for shipped scripts only.** A modded script could pass 10 to
  `setexpandvoicememory`, or call the `debug_tkmalloc` verbs with 10. By part 2, that would hang the thread.
- **The identity of the `022D89A8` map is cited from the memory page**, not re-derived here.
- **Whether arena 12 is live whenever `003EA031` selects it is not claimed.** That case is `[02B5E0B0]` non-zero,
  and arena 12 is initialised by `003E9AA0`.
