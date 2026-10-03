---
system: Where the game's memory comes from
category: 24-Compiler-And-CRT-Runtime
status: PARTIAL — owner re-status 2026-10-02 (FABLE) from REOPENED: the reopening cause is resolved (SECTION-07 ACCEPTed, auditspec-review-section07-10-1001) and four residues are answered statically (_index/candidates/mempage-residue-fable-1002); the +0xC0 receiver type answered 2026-10-02 (_index/candidates/c0-receiver-fable-1002); open: the run-time placement of the arena blocks (GR-18's fourth case)
owner_layer: CodeDomain:Runtime.Memory + Runtime.ContainerAllocator + Microsoft.MSVCCRT_STL_Runtime
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: "additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `001C22A0`, `005DD890`, `005DF890`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30"
    verified: "re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS"
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-where-the-games-memory-comes-from-pass-1
  crossref_clean: false
  reopened_count: 0
external_production:
  section: SECTION-07
  date: 2026-09-23
  status: "locally validated; formal independent acceptance pending"
  evidence: _experiments/evidence/continuation-section07-source-movement/REVIEW.md
---

# Where the game's memory comes from

> Every byte FFXII allocates while it runs comes from **one** heap — the C runtime's, inside a
> Windows DLL the game does not ship — through exactly ~~**six**~~ **eight** doors *(corrected 2026-10-02, OPUS: all eight heap imports `008C2B40`–`008C2B78` are reached: `_aligned_malloc` by tail jumps in `0019C580`, `001EDF10+0x5D` and `001EDF80+0x53`, `_set_new_mode` through `00862046`; §1's table)*. ~~The game never creates a
> heap of its own, never reserves a pool up front, and never checks whether the memory it just
> asked for actually arrived.~~ *(corrected 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's allocator-retry
> return; re-derived in [`_index/candidates/fable-returns-0928g/`](../../_index/candidates/fable-returns-0928g/alloc_nav_check.py))* Above those doors the game runs
> its own fifteen-heap arena (§2), ~~whose backing is not established~~ whose backing comes from the C runtime heap or from another arena *(answered 2026-10-02, FABLE, static; addresses and controls in [`mempage-residue-fable-1002`](../../_index/candidates/mempage-residue-fable-1002/README.md) item 1)*. Its wrappers do check arrival:
> `0036A1A0` tests both allocators' results and skips its header stamps on null, and the retry allocator
> `0036BFE0` asks the heap's callback and a reclaim pass before it returns null. Callers differ: some test
> the result and some write through it unchecked (§1).

## 1. What the player sees

Watch FFXII in Task Manager while you play. The memory figure is not flat. It climbs as you walk
into Rabanastre, climbs again when the Bazaar crowd streams in, drops back when you leave for the
Estersand, climbs hard on a summon cinematic. The game is asking Windows for memory and giving it
back, continuously, all the way through a session — ~~it does not grab one big block at startup and~~
~~live inside it the way a console game does.~~ It also takes nine large blocks at startup, about 256 MiB, and its arenas live inside them *(corrected 2026-10-02, OPUS: `0022A0B0+0x131` through `0022A0B0+0x1B9` call `0036D240`, which reaches `malloc` through `0085E730`, for arenas 2–9 and 11; §2)*.

That has two consequences a player can actually feel.

**The game's appetite is set by what is on screen, not by a setting.** There is no memory slider
in the options, and no texture budget that the game enforces on itself. It loads what the zone
asks for. On a machine with plenty of RAM this is invisible. On a machine that is short of it,
Windows starts paging, and the symptom is the one everybody knows: the game keeps running at a
normal frame rate right up until a zone transition, and then the loading screen takes ten times as
long as it did an hour ago.

~~**When memory genuinely runs out, FFXII does not tell you.** There is no out-of-memory message in
this game, and no graceful fallback. The code that builds a zone's actors asks for its block, gets
nothing back, and then writes to it anyway. The result is an instant close to desktop with no
dialog — the classic "it just disappeared" report. It is not a corrupted save and it is not a bad
install; it is the engine trusting an allocation that failed.~~
*(corrected 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's allocator-retry return: the crash narrative was never observed, and it leaves out the retries and the null checks the code does have.)* **What the game does when memory runs out has not been observed.** In the code:
- **The arena retries before it fails.** `0036BFE0` returns null only when the heap's callback slot answered 0 (or is empty) and the reclaim step (`0036AAD0` / `0036ABE0`) produced 0 (`0036C0AE`–`0036C0C4`). Otherwise it tries again — and when the selected arena's init bit is clear it spins forever at `0036C000` instead (RC-11 part 2; added 2026-09-30 on SWE2-AUDIT-SEM's batch-4 review §5). ~~What the callback and the reclaim do is not established.~~ *(Reconciled 2026-09-30, SWE2-DATA: the reclaim is the compaction. `0036AAD0` / `0036ABE0` pick a tagged source block and `0036A2A0` relocates it, so a retry can succeed after a move (the SECTION-07 section below). What the heap's callback slot holds is `SD-164`.)*
- **Some callers handle a null.** The nav grid's allocation helper skips its initializer, and two effect constructors take an allocation-failure branch (§2).
- **Some do not.** The nav grid rebuild stores the result and `memset`s it with no test (both sites in [the record](../../_index/candidates/fable-returns-0928g/README.md)), so a null there would fault on the first write.
- **Not established here:** whether any player-visible message, fallback or crash follows. No census of which callers test the result has been made (`SD-165`, SWE2-DATA, 2026-09-30).

This also explains something modders run into immediately. Because the game leans on the C runtime
that *Windows* supplies rather than one it ships in its own folder, two machines running the same
copy of FFXII are not running the same allocator code. A memory bug that reproduces on one PC and
not on another, with identical game files, is behaving exactly as designed.

## 2. Native mechanism

### One heap, six doors

`FFXII_TZA.exe` imports **538 symbols across 30 DLLs**. Of those, exactly **eight** are heap
functions, and all eight come from `api-ms-win-crt-heap-l1-1-0.dll` — the API-set stub that
forwards to `ucrtbase.dll`, the Universal C Runtime that ships with Windows. ~~Six of the eight are~~ All eight are *(corrected 2026-10-02, OPUS: the table's own `_set_new_mode` row is corrected to 1, and `_aligned_malloc` is reached through `0019C580`)*
actually called:

| door | call sites | distinct calling functions |
|---|---:|---:|
| `free` | 860 | 683 |
| `malloc` | 78 | 60 |
| `calloc` | 30 | 16 |
| `_aligned_free` | 17 direct, plus one guarded wrapper with 2,309 callers (below) | 4 direct |
| `realloc` | 5 | 4 |
| `_msize` | 1 | 1 |
| `_aligned_malloc` | 0 direct — reached only through the adapters in §3 | — |
| `_set_new_mode` | ~~**0**~~ **1**, through the import thunk `00862046` *(corrected 2026-09-30, SWE2-DATA, `pf_mem_checks.py` M1d)* | 1, the first C++ initializer `00808D5C` |

**And there is nothing else.** The import table contains no `VirtualAlloc`, no `HeapAlloc`, no
`HeapCreate`, no `CreateFileMapping` and no `MapViewOfFile`. The only other allocating Win32 calls
in the whole binary are `LocalAlloc` (16 sites) and `GlobalAlloc`/`GlobalLock` — the Win32
clipboard and shell idiom, not a memory system. So the statement is unusually clean for a 32 MB
game executable: **FFXII TZA runs entirely out of the C runtime's default heap** *at the operating-system
level*. It does not partition memory into pools, arenas or banks **through the OS**, and it does not
reserve address space in advance.

> **QUALIFIED 2026-09-12 (ASTRA-CONTRA-FABLE-RESOURCE-ARENA): the game does run its own arena, above
> the OS layer.** The import census above stands, and it says nothing about in-process allocators.
> `0036BC60` (887 B) is the game's own arena allocator: fifteen heaps (index ≤ `0xE`) as `0xA8`-byte
> records at `022D7FD0`, an enable mask at `022D89B8`, request sizes rounded up to 64 bytes, a `0x40`-byte
> block header, first-fit from the free list's head (`+0x90`) or last-fit from its tail (`+0x98`), and
> splitting (`0036BC89`–`0036BDE0`). **Its block links are 32-bit values decoded through
> `ImageAddress_ResolveRuntimePointer` `0020E600`** (`0036BD09`, `0036BD37`, `0036BD6C`–`0036BDA4`) — the
> same `base + (u32)x` pair the authored tables use — so the arena's own bookkeeping only works if every
> block lies within 4 GiB above the base `01F83530`. `0036A100` / `0036A190` / `0036A1A0` are its entry
> wrappers (`0036BFE0` retries and reclaims). Resource payloads (`.ebp` files, authored tables, the BGM stream
> buffer) come from it, and `0036C660` tags a block's header with a 7-character name. ~~Where the
> arena's backing is obtained — through the CRT imports listed here or otherwise — is not established
> on this page (ASTRA's EXP-077 / EXP-078).~~ Every arena's backing is obtained at run time from the C runtime heap or from another arena. Arenas 2 to 9 and 11
> get it from `malloc`, through a shim, during boot, and arena 11 again whenever it is reallocated at a new size. Arenas 13 and 14 are carved from arena 5,
> and arena 12 from the arena the script verb `setexpandvoicememory` names, which is arena 6 for the only argument shipped scripts pass (-1). Arenas 0, 1 and 10 are never set up: the initializer is the only code that sets an arena's enable bit *(answered 2026-10-02, FABLE, static; addresses and controls in [`mempage-residue-fable-1002`](../../_index/candidates/mempage-residue-fable-1002/README.md) item 1)*. Where the running process places those blocks stays a run-time fact (ASTRA's EXP-077 / EXP-078); it is registered as `GR-18`'s fourth case, whether the `.ard` buffer can sit at or above 4 GiB *(linked 2026-10-02, FABLE)*. "There is no pool to size" is withdrawn for the resource
> path.
>
> **Where the backing comes from (2026-09-12, ASTRA's supplement re-read by FABLE).** At boot,
> `0022A0B0` allocates nine blocks through `0036D240(size)` — a 14-byte shim that tail-jumps to the CRT
> `malloc` thunk (`0085E730` → import `008C2B40`) — and hands each to the arena initializer `00369D30(id,
> block, size, ~~alignment~~ slotCount)` (`0022A1DC`–`0022A394`) — *the fourth argument is a handle-slot count,
> corrected below:*
> 
> | id | size | handle slots | | id | size | handle slots |
> |---:|---:|---:|---|---:|---:|---:|
> | 2 | 29.75 MiB | 16 | | 7 | 48 MiB | 256 |
> | 3 | 13.125 MiB | 256 | | 8 | 32 MiB | 256 |
> | 4 | 1 MiB | 16 | | 9 | 18 MiB | 16 |
> | 5 | 1.75 MiB | 256 | | 11 | 4 MiB | 256 |
> | 6 | 108 MiB | 1,024 | | | | |
> 
> About 256 MiB in all, from the CRT heap. Arena 11 is later freed (`0036D250`) and re-`malloc`ed at
> 3.75 or 4 MiB depending on `02ADD930` (`0037B3D0`). Higher ids are **nested**: `0025A990` allocates a 1 MiB
> block through the arena selector (`0036C1D0(5, 5)` then `0036A190`), tags it `EVTM` with `0036C660`, and initializes
> arena 13 inside it; ASTRA's evidence covers 12–14 and the `022D89A8` selector map. ASTRA's
> [EXP-077](../../_experiments/EXP-077-arena-initializer-address-width.md) executed the initializer with
> backing above 2 GiB and 4 GiB and it keeps full 64-bit pointers in the arena record — so **the
> initializer imposes no low ceiling; the 32-bit assumption lives in the block links and the encoder**
> (`0036BC60`, `0020E620`). ~~Where the CRT heap actually places 256 MiB in a running process is not
> observed, so whether those links are safe in the shipped game stays open.~~ *Observed in two states
> (2026-09-12, below):* every enabled backing lay below 2 GiB at the title menu and after one ordinary load;
> that is placement at those instants, not a guarantee for every session or later state.
>
> **Live placement and the arena-7 exception ([EXP-079](../../_experiments/EXP-079-arena-live-placement.md), ASTRA; primary bytes re-read by
> FABLE 2026-09-12).** One unmodified process, read-only: base `0`, identity map, selected arena 2. Backings
> (`+0x08`) at `65F60040`–`7C5D3040`; loading The Stepping enabled arena 14 at `6610EF40` and moved arena 11
> from `7C5D3040` to `7C5D2040` (no trace names the cause). FABLE's reading of the same records:
> - **Arena 7's record is the initializer's untouched initial state for 256 slots** — `+0x20` = backing
>   + `0x40`, `+0x28` + `0x100`, `+0x30` = `+0x40` = backing + `0x1900` (no slot ever issued), `+0x38` = `+0x10`
>   = `+0x90` = `+0x98` = backing + `0x2900` (one free block, never split), `+0x48` = 0, `+0x5C` = `0x2FFD700`
>   = 48 MiB − `0x2900`. **But its backing bytes are not the initializer's**: they begin `EFX0010` and the
>   64 bytes at the first-block header are zero in all four samples. The static reason: `003B0660` requests
>   resource kind 10, index 0 **straight into arena 7's raw backing** (`003B06F8`–`003B070D`, destination
>   `[01FD4A30]`) and hands the same bytes to the EFX loader `003EDAD0` (`003B073F`–`003B0745`); `002FC860`
>   (kind 11 or 38, `002FC956`) and `003B2310` (kind 12, `003B23E3`–`003B23F5`) also pass that backing as a
>   request destination. So **arena 7 is registered by boot but used as a raw resource buffer that bypasses
>   the allocator**, which explains why its record never moved. Whether anything ever allocates from it
>   afterwards — which would now read a clobbered header — is not established (`SD-166`, SWE2-DATA, 2026-09-30). The three destination users
>   are the effect-file kinds — 10 (`c_all.efx`, `m_all.efx`), 11 / 38 (magic effects) and 12 (event effects) —
>   so the backing is the **effect-file load buffer**. ~~EFX's copy-or-borrow branch makes the buffer's lifetime
>   matter~~ *For kind 10 the EFX loader copies its chunk runs out* (template `+2` = 0; ~~borrowing is the EFB~~ borrowing is the EFB and type-3 contexts' mode, and the kind-12 context (type 7) does not run-collect at all — corrected 2026-09-12; 
>   loader's mode) ([the EFX page](../../17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md) §2).
> - **Arena 9 is enabled with `+0x90` = `+0x98` = 0** while `+0x10` names a first header: an empty free list,
>   consistent with a fully allocated arena; not traced.
> - **Zero-slot nested arenas 13 and 14** have `+0x30` / `+0x38` / `+0x40` null, as the initializer writes for a
>   zero count (`00369ECC`–`00369ED4`), while `+0x90` / `+0x98` are real headers; arena 13's moved from
>   `66128100` to `6612B000` between the states. So `+0x90` / `+0x98` are the free list's ends, equal to the
>   first header only before the first split — the type rows are corrected.
>
> **The fourth argument is a handle-slot count, not an alignment (corrected 2026-09-12,
> ASTRA-CONTRA-FABLE-ARENA-SLOT-COUNT; read by FABLE in the body).** `00369D30` sign-extends it into `rbp`
> (`00369D41`) and uses it only as a count of **16-byte records**: the record's `+0x30` is the table start,
> `+0x38` = start + 16 × count (`00369EB7`–`00369EBE`), `+0x40` the free-slot head, and the loop
> `00369EE5`–`00369F33` links the slots by 16-bit index (word `+0` next, word `+2` previous, `0xFFFF` = none,
> byte `+4` the arena id). Every region the initializer lays out is aligned to **64 bytes, hard-coded**
> (`and …, 0xFFFFFFC0`); nothing derives an alignment from the argument. Laid out inside `size`, in order: a
> dword bitmap and a qword array sized from the block's 64 KiB page count rounded up to 32 (`00369DDF`–`00369E23`,
> purposes not read here), the slot table, then the first free block. The slots are **handles to allocated
> blocks**: `0036AF20(id, header)` pops a free slot, moves it to the in-use list (head `+0x48`), stores the
> header pointer at slot `+8`, stores the slot's encoded reference at header `+0x20`, and returns **the slot
> address's low 32 bits OR 3** (`0036AFFC`–`0036B01B`). *It first checks the header:* when `header + 0x20` decodes
> to a slot marked in use, it returns that **existing** handle without touching the free list (`0036AF60`–
> `0036AF8B`; review ASTRA-CONTRA-FABLE-ARENA-CONSUMER-BOUNDS). Only a header with no live slot pops one; with
> ~~no free slot~~ no free slot *for such a header* it logs and returns 0, and its
> caller `0036C4B0` then frees the block (`0036C541`). `00369800(handle)` rejects values with the low two
> bits clear or below `0x100000`, masks with `0xFFFFFFFC` — which also clears the upper 32 bits — releases the
> slot (`0036A9C0`) and frees the block. So **the count bounds how many handle-held blocks an arena can have
> at once**, and a handle is an absolute address carried in 32 bits: **a third width condition**, besides the
> two stated on [the container sheet](../../25-EBP-Script-Container/Container/ebp2-container.md) §7 — handle-issued blocks need their arena's slot
> table below 4 GiB absolute. Which callers take handles rather than pointers (`0036B160`, `0036B980` reach
> `0036C4B0`) is not traced (`SD-167`, SWE2-DATA, 2026-09-30). The boot allocation of `size + count` bytes (tails `0x10` / `0x100` / `0x400`)
> is therefore **not** an alignment allowance: the initializer uses only `size`, and what the extra `count`
> bytes serve is not established (`SD-168`, SWE2-DATA, 2026-09-30).
>
> **Access to a handle-held block moves it out of a size-ordered tree (ASTRA's [lifetime evidence](../../02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md)
> §17–§18; FABLE re-read `0036B410`, `0036B4E0`, `003AB7C0`, `003AB8B0` and the append 2026-09-12).** Each arena
> record holds a **binary tree root at `+0x50`** (`0036B427`, `0036B457`); a block header carries encoded
> `+0x24` left, `+0x28` right, `+0x2C` parent links and is ordered by its payload length `+0x18` under a **signed**
> compare (`0036B50A`–`0036B50D`: a node whose key is ≤ the new key sends it right), with no balancing. Header byte
> `+0x15` mask `0x02` marks tree membership: tagged access `0036A000` checks that the slot's word `+6` still equals
> header `+0x1C`, and if the block is in the tree removes it (`0036C790`) and clears the mask before returning
> the payload `header + 0x40`; `0036D170` checks the same words and, when the mask is clear, re-inserts it
> (`0036B410`) and sets the mask. So **a handle-held block sits in its arena's size-ordered tree except while it
> is being accessed**. That is the shape of a set of relocatable blocks, and the EFX relocation front
> ([the EFX page](../../17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md)) is the consumer that expects moves, and SECTION-07 now connects and executes the actual tree selectors `0036AAD0`/`0036ABE0`
> and mover `0036A2A0`. Membership makes a block eligible for those moves, subject to mask `0x04`.
> This supersedes the earlier statement that no such tree walker had been read. The release front `003AB7C0` sends
> a tagged value to the handle release `00369800` and an untagged one to `003697F0`
> (`003AB7C5`–`003AB7DE`). The resource-storage allocator `003AB8B0` pushes selection (6, 6) and allocates
> **kind 0 as a raw block** (`0036A100`, full pointer) or **kind 1 as a handle** (`0036B160` → `0036C4B0`, a 32-bit
> value, `003AB8D5`–`003AB8E1`). One width detail for reconstruction: the storage append `0051EF90` passes
> `memcpy` a destination built in 32 bits — `low32(resolved base) + used` (`0051EFED`–`0051EFF8`) — so it is one
> more below-4 GiB condition on that storage's blocks; the growth copy `0051EEB0` uses full width.
>
> **The free routine and the 64 KiB buckets** ([lifetime evidence](../../02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md) §19; FABLE re-read `00369860`,
> `0036ACE0`, `0036B5F0` 2026-09-12). `00369860(payload)` is gated three ways before it reclaims anything: a header
> (`payload − 0x40`) without the `FF12` word takes a diagnostic path ending in an imported `exit(1)`; a **non-zero
> header word `+0x3E`** takes the "MCB broken" diagnostic and the same exit (`00369A80`); header byte `+0x14` mask 1
> clear is reported as already free and returns (`00369ABE`). Only then does it clear mask 1, debit the payload
> length from the counters indexed by header `+0x16` and `+0x17` (`00369B05`–`00369B1B`), clear metadata including
> `+0x3E` (`00369B4F`), coalesce with free physical neighbours or insert through the bucket searches. Those searches
> (`0036ACE0` / `0036AE00`) give the record's two initializer arrays their role: a block's **bucket is
> `(header − first header +0x10) >> 16`**, the qword array `+0x28` holds a representative free header per 64 KiB
> bucket and the dword bitmap `+0x20` one bit per bucket (`0036AD12`–`0036AD48`), refreshed by `0036B5F0`, which
> compares representatives by their **low 32 bits** (`0036B646`) — another 32-bit condition. For arena 7 (EXP-079) the
> zero bytes sit at the record's free-list head, so what they would affect is an **allocation** from that arena, whose
> handling of a zero header is not read here; the free gates check the freed block's own header.
>
> **`+0x3E` is a guard word, and the way that was settled was by failing to find a writer** (OPUS
> 2026-09-16). The gate above says a non-zero `+0x3E` is fatal; what it does not say is *what could
> make it non-zero*, and the field sat UNRESOLVED on that question. Two sweeps answer it in the
> negative. Every 16-bit access at displacement `0x3e` decoded from all **38,161** function bodies
> gives 92 hits, 36 of them in the arena manager; and because a dword at `+0x3c` or a qword at
> `+0x38` would set the word just as well, every access in the manager whose byte range *overlaps*
> `+0x3E..+0x3F` gives 68 more. Both sweeps carry the known sites as positive controls. **All 33
> stores to the header word store zero** — 30 settled by an immediate or an `xor`-self, three by
> hand (`0036C578`/`0036C587` take `bp` after `xor ebp, ebp` at `0036C4CC`; `0036B010` after
> `0036AF3D`) — and both reads are comparisons against zero. The only non-2-byte overlaps are three
> qword stores at `+0x38` in `00369C60` whose base is the **0xA8-byte arena descriptor**, not a
> block header, and two `lea …+0x3f` that are align-up arithmetic and dereference nothing.
>
> So a non-zero `+0x3E` is not a state the manager can produce, which is exactly why it is read as
> corruption. The word is the last two bytes of the `0x40` header, immediately before the payload
> and immediately after the undeclared `0x30`–`0x3D` region — which holds the NUL-terminated string
> that `0036A2A0` copies out of `+0x34` through an **unbounded** loop (`0036A320`–`0036A32C`).
> **Which overrun the guard is positioned to catch is not settled**: an over-long tag would reach
> it, and so would a payload underrun, and neither has been observed. Naming it `guardWord` records
> the discipline that was measured, not a mechanism that was not.
>
> **What the block links do once the backing is high (ASTRA's [EXP-078](../../_experiments/EXP-078-arena-allocation-link-width.md),
> consumed by FABLE 2026-09-12).** Original allocator bodies, run in isolation from EXP-077's sealed state with
> base `0` and no stubs in the allocation stage: with backing at `100010000` the **first** 64-byte allocation
> returns the correct high pointer, and the **second** faults writing to low memory — direction 0 at
> `0036CA8A` (store to `10290`), direction 1 at `0036CA75` (store to `10FF8C`) — while ~~the same cases at
> `40010000` and `80010000` complete~~ the low controls at `40010000` complete in both directions and the
> `80010000` case completes in direction 0; **no direction-1 case was run above 2 GiB** (corrected 2026-09-12). The failing fields are the block header's **neighbour links `+0x0C` /
> `+0x10`**, written 32-bit by the first allocation and followed by the unlinker `0036C9D0` on the second; FABLE
> read the stores in `0036C9D0` and they are as stated. With a byte copy of the backing mapped at `10000`,
> the second allocation returns the right high pointer but reads and writes the copy (four writes and one
> read), and the copy ends byte-identical. So a correct return value does not show a correct allocator:
> **it can operate on a different region**. The free-list links `+0x04` / `+0x08` and the handle reference at
> header `+0x20` use the same encoder and were not the path exercised. Not established: where the running
> game's CRT heap places the backing, the base's lifetime, other sizes, and any consequence in the shipped
> game — a clean final mirror is not evidence of corruption or of its absence there. `BW-2`.

The one place the game looks at the machine's memory at all is `GlobalMemoryStatusEx`, called from
just two functions (`0020C610`, `00792F10`). ~~Whatever it does with the answer, it is not used to
size a pool, because there is no pool to size.~~ *Withdrawn 2026-09-12:* the reason is false — the game runs
fifteen arena records with fixed boot sizes (above) — and whether either reader influences any size is not
established; it needs its own reading of `0020C610` and `00792F10`.

### The arena selection stack — how a caller borrows an arena (2026-09-13, FABLE)

*Corrected 2026-09-13 after SWE2-AUDIT-SEM's shadow audit (AUDITSEM-CONTRA-FABLE-ARENA-STACK, defects D1–D6).
The census and the stack mechanics were verified exactly. The tag, the initializer, the map, the byte-stack edge cases
and the allocator's depth gate are rewritten below.*

The allocation wrappers never take an arena argument. **`0036A100` passes `[022D89BC]` to the arena allocator
`0036BC60`** (`0036A113`); its retry at `0036A12E` passes the same global to the second allocator `0036BFE0` (`0036A149`).
`0036A1A0` does the same. A caller that wants its block from a
particular arena therefore **pushes a selection, allocates, and pops** — and that pattern is one of the most
used in the engine: **109 functions push through `0036C1D0` (135 call sites) and every one of them also pops
through `0036C140`** (111 functions, 153 sites, 19 of them tail jumps), from the resource loaders, effects,
text and actor code alike.

| operation | body | effect |
|---|---|---|
| push `0036C1D0(arena, category)` | `lea r9,[rsp]` / `mov r9,[r9+4]` / `sub r9,5`, then tail-jump to `0036C1F0` with stack index 0 (`0036C1D0`–`0036C1DF`). The return address is at `[rsp]`, so the qword at `[rsp+4]` **straddles** two slots: its low dword is the return address's high dword, and its high dword is residue from the caller's frame. ~~the caller's call-site address~~ The stored value, minus 5, identifies no call site. | a saved "tag" with no meaning and no consumer (below) |
| `0036C1F0(arena, category, stack, tag)` | depth `[022D89C0 + stack×4]`; **depth ≥ 31 spins forever** (`0036C20B`–`0036C211`). Saves the current state as a 16-byte record at `022D89D0 + (stack×32 + depth)×16`: `+0` u16 the active arena `022D89BC`, `+2` u8 the category `022D8E18`, `+3` u8 `022D8E28`, `+8` the tag `022D8E20` (`0036C213`–`0036C252`). Depth + 1. Then installs the new category (`0036C265`), the tag (`0036C26B`) and **the active arena through the map `022D89A8[arena]`**. The id is sign-extended (`0036C262`) and indexes the 15-byte map with **no bounds check** (`0036C272`–`0036C27F`). | ~~the requested id is not the arena index; the map translates it~~ **In the retail image the map translates nothing.** Its only writers are two identity fills, `00369DA0` in the initializer and `0036A290` in `0036A280`, so `map[id] == id` for ids 0–14. An id of 15 or more reads past the map into `022D89B7` and beyond. |
| pop `0036C140()` | depth of stack 0 − 1, **spinning forever if it was not positive** (`0036C146`–`0036C150`); restores all four fields from the record (`0036C167`–`0036C18D`) | the previous selection is back |
| byte push `0036C1A0(value)` / pop `0036C110()` | A second, 32-deep stack of the byte `022D8E1C` at `022D8DD0`, depth `022D89C8` (`0036C1A7`–`0036C1C9`, `0036C116`–`0036C12F`). ~~the pop simply returns when the depth is already negative~~ **The failure behaviour differs from the main stack.** A push at depth ≥ 31 returns without saving or installing anything (`0036C1AB`): the new byte is silently dropped. A pop returns unchanged only when the depth is negative (`0036C118`). At depth 0 it decrements to −1 and installs `022D8DD0[−1]` = `022D8DCF`, the last byte of the unused stack-1 records (`0036C11A`–`0036C12F`). | 18 functions, each using both |

**What the saved fields do.** The active arena is the wrappers' first argument. **The category byte is stamped into
the header of the blocks the two wrappers and `0036B160` return.** Each copies `022D8E18` to `block − 0x3E`:
`0036A15F` in `0036A100`, `0036A206` in `0036A1A0`, `0036B1CA` in `0036B160`. So such a block records which scope
allocated it. ~~every block's header~~ The other direct callers of `0036BC60` stamp nothing at that offset:
`0036A2A0`, `0036CB00`, and the retry allocator `0036BFE0`, whose result the wrappers stamp themselves. Whether
`0036A2A0` and `0036CB00` produce blocks that carry this header is not traced.

`022D8E1C` is the arena allocator's fallback where a free-list record supplies no byte `+0x16` (`0036BD19`, `0036BD21`,
`0036BD44`, `0036BD4F`). `022D8E28` is compared in `0036A490` (`0036A4F6`). **The tag `022D8E20` is saved and restored
and read by nothing.** The first scan here covered rip-relative operands only. SWE2-AUDIT-SEM's census then covered
rip-relative, image-base-indexed, immediate-built-pointer and data-qword forms and found no consumer of `022D8E20`
(`REVIEW-arena-selection-stack.md` in the auditor's work directory).

**The initializer `00369D30(arena, …)`.** It returns at once for an arena above 14 (`00369D47`). **Only when no arena has
been initialized yet** (the init mask `022D89B8` is zero, `00369D6E`), it:
- sets the active arena `022D89BC` to its argument;
- identity-fills the map;
- zeroes `022D8E28`, both stack depths (a qword store at `022D89C0`), the byte-stack depth (a qword store at `022D89C8`),
  `022D8E1C`, the tag `022D8E20` and `022D8E10`;
- sets the category `022D8E18` to `0xFF` (`00369D73`–`00369DC5`; `r8d` is cleared at `00369D57` before the stores).

~~sets the category to `0xFF`, the tag, `022D8E1C` and `022D8E28` to its argument~~ Every call then ORs `1 << arena`
into the mask (`00369DCC`–`00369DE7`), so a later arena's initialization leaves the stack state alone.

**Only stack 0 is used.** `0036C1F0` is general over a stack index, but its only caller is `0036C1D0`, which passes 0,
and the pop hard-codes stack 0. The depth array has two dwords (`022D89C0`, `022D89C4`), and the record array
`022D89D0` up to `022D8DD0` (exclusive) is `0x400` bytes: **exactly two stacks** of 32 × 16. The game drives one.

**The allocator will not run unselected.** `0036BC60` spins forever when its third argument `r8` is zero **and** the
stack-0 depth is zero (`0036BC79`–`0036BC87`). `r8` is zero at five of its six direct call sites: both wrappers
(`0036A11C`, `0036A1C6`), `0036B160` (`0036B17E`), `0036CB00` (`0036CF04`) and `0036BFE0` (`0036C0A4`). `0036A2A0`
passes `rbx` (`0036A3B5`) and passes the gate whenever that is non-zero. So an allocation through the wrappers requires at
least one pushed selection. **The push / allocate / pop discipline is enforced by a hang**, not only by convention.

**Scope discipline, and its exception.** Push and pop are always paired inside one function except in **two effect
constructors reached through the jump table at `0043EBF0`**, `0052A130` and `0052ADF0`, which pop **only on their
allocation-failure branch** (`0052A302` after a failed `0036A190` at `0052A2F1`; `0052AFE4` after `0052AFD3`). The
matching push lies upstream of the dispatcher and is not traced here; on success the selection stays pushed past
their return. **Both overflow and underflow of the main stack hang the thread** rather than fail, so a mismatched pop is
a freeze. ~~, not a crash.~~ **A bad arena id is a crash instead.** For an active arena above 14, `0036BC60` sets its
record pointer to 0 (`0036BCA1`–`0036BCC3`) and writes `byte [0 + 2] = 1` (`0036BCC5`). The identity map passes any
push id of 0–14 through unchanged. Which ids the 135 push sites pass is not censused here.

### The C runtime is not in the game folder

None of `ucrtbase.dll`, `api-ms-win-crt-*.dll`, `VCRUNTIME140.dll` or `MSVCP140.dll` ships in the
game's `x64` directory. They resolve from the system. This is why the game's `malloc`, its
`memcpy`, and its `sinf` and `sqrtf` are **properties of the player's Windows install, not of the
game build**. Two players on the same game version can be running measurably different allocator
and maths code.

### Two allocator classes, both EASTL

The C++ side of the engine is built on **EASTL**, Electronic Arts' STL replacement, and the binary
carries genuine MSVC RTTI for two allocator classes:

* `.?AVallocator@eastl@@` — vtable at `008F6500`
* `.?AVallocator_memory_log@eastl@@` — vtable at `00902720`

Both vtables are six slots and have the same shape, which is EASTL's allocator interface:

| slot | `eastl::allocator` (`008F6500`) | `eastl::allocator_memory_log` (`00902720`) | what it is |
|---:|---|---|---|
| 0 | `0016D680` | `0016D680` | destructor — `mov rax, rcx; ret`, returns `this`, frees nothing |
| 1 | `0016D6B0` | `001EDF10` | `allocate(n, alignment, offset, flags)` |
| 2 | `0016D6B0` | `001EDF80` | `allocate(n, flags)` |
| 3 | `0016D6C0` | `001EDFE0` | `deallocate(p, n)` |
| 4 | `0016D690` | `0016D690` | `get_name()` — returns the string `"EASTL"` at `01CDAE78` |
| 5 | `0016D6A0` | `0016D6A0` | an empty `ret 0` — the universal folded stub; see §4 before naming it |

The two classes differ in exactly one thing that matters: **alignment**.

`eastl::allocator` is the plain one. Both of its allocate overloads compiled to identical bodies
and the linker folded them into one function, `0016D6B0`, which is two instructions:

```
0016D6B0  mov  rcx, rdx                 ; arg1 (the size) becomes arg0
0016D6B3  jmp  qword ptr [rip+0x755486] ; -> ucrtbase!malloc
```

so it is `malloc(n)` with **no alignment guarantee beyond `malloc`'s own**, and its `deallocate`
is `free(p)`. The alignment, offset and flags arguments are silently discarded.

`eastl::allocator_memory_log` is the one that honours alignment. Its `allocate(n, flags)` is
`_aligned_malloc(n, 16)`; its `allocate(n, alignment, …)` passes the caller's alignment straight
through; its `deallocate` is a null-guarded `_aligned_free`. **This distinction is a live hazard
for a modder**: memory from `allocator_memory_log` must be released with `_aligned_free` and
memory from `allocator` with `free`, and the two are not interchangeable — `_aligned_malloc`
stores a back-pointer in front of the block it hands out, so passing one of its pointers to plain
`free` corrupts the heap.

### The same three operations also exist without the object

Alongside the virtual spellings there is a non-virtual set that does the identical work, reached
by direct `call` rather than through a vtable. These carry the overwhelming majority of the
traffic:

```
0017D260   or   r9d, -1                 ; flags  = -1
           xor  r8d, r8d                ; offset = 0
           jmp  0019C580                ; -> _aligned_malloc(size, alignment)

00584740   or   r9d, -1
           xor  r8d, r8d
           lea  edx, [r9 + 0x11]        ; alignment = -1 + 0x11 = 16
           jmp  0019C580

00584730   test rcx, rcx
           jne  0019C570                ; -> _aligned_free(p)
           ret                          ; null pointer: do nothing
```

`lea edx,[r9+0x11]` is worth reading twice — it is the compiler materialising the constant **16**
out of the `-1` it already has in `r9d`, which is why the alignment is easy to miss on a first
pass. All three tail-jump; none of them has a stack frame.

`00584730` — five instructions, ten bytes, "free it if it isn't null" — is called directly by
**2,309 distinct functions**, which makes it one of the most-called functions in the entire
binary. It is the engine's universal delete.

### The linker's forwarder chains, and why call counts look wrong

MSVC did not emit one thunk per import; it emitted chains of them, and a naïve census walks off
the end. `free` is the clearest case:

```
00809950  free   jmp 00210EB0            (E9 rel32)
00210EB0  free   jmp 0019C590            (E9 rel32)
0019C590  free   jmp qword [rip+…]       (48 FF 25 -> IAT free)
```

Three hops before the import. A census that counts only `call qword ptr [rip+slot]` — the
instruction people expect an import call to be — reports **`sqrtf` 0 sites, `memset` 0 sites,
`memcpy` 0 sites**, which are all plainly false. The transitive figures are in §4, and the
instrument correction is recorded in `COVERAGE.md`.

### The memory log that logs nothing

`allocator_memory_log`'s three methods all begin with the same lazy initialiser:

```c
if (g_log == NULL) {
    g_log = malloc(0x20);
    if (g_log) {
        *(u32*)(g_log + 0x00) = 0x02000000;   //  33,554,432 = 32 MiB
        *(u32*)(g_log + 0x04) = 0x00200000;   //   2,097,152 =  2 MiB
        *(u64*)(g_log + 0x10) = 0;
        *(u32*)(g_log + 0x18) = 0;
    }
}
```

The global is `01F82E48`. A displacement census over the whole `.text` section finds **exactly
three** references to it — and they are these three functions, each of which only tests it for
null and stores the pointer back. **No code anywhere loads that pointer and reads the fields.**
The 32 MiB figure and the 2 MiB figure are written once, on the first allocation of the session,
and never consulted again; the two counters stay at zero forever. In the retail build the memory
log is **inert** — the name is the only thing left of it.

*Method, and its blind spot.* The census scans every four-byte window in `.text`, treats it as a
RIP-relative displacement, and reports the ones that land on `01F82E48`. It cannot follow a
pointer copied into a register in one function and dereferenced in another. Here that does not
weaken the claim, because all three sites that touch the global were read in full and none of them
lets the pointer escape. Positive control: the same census, on the same run, found the single
reference to the `"EASTL"` name string, the single reference to the `allocator_memory_log` vtable,
and 38 references to `malloc`'s IAT slot — it demonstrably finds references of exactly this shape.

### Where gameplay records actually come from — and it is not this

The interesting result is a negative. Sort the callers of the three engine entry points by
`PrimaryOwner`:

| entry point | distinct callers | who they are |
|---|---:|---|
| `0017D260` allocate(n, align) | 228 | 158 generic native routines, 39 Phyre, 9 Runtime, 10 Boundary, 3 Presentation, 3 Resource, 1 Core scheduling, 1 Input |
| `00584740` allocate(n) → align 16 | 29 | Phyre 4, Boundary 4, Resource 3, Audio 3, Input 3, Platform 1, Application 1, rest generic |
| `00584730` free | 2,309 | Phyre 1,515, Runtime 304, generic 301, C++ lifecycle 49, Input 39, Resource 23, Presentation 3, Platform 3 |

> *Re-derived at GN161 2026-09-14: the caller sets are unchanged (228 / 29 / 2,309); three callers
> that were untagged when this table was written now carry `CodeDomain` tags (`001C22A0` →
> `Boundary.Audio.BufferAlloc`, `005DF890` → `Boundary.Audio.ProcessLoop`, `005DD890` →
> `Runtime.Container.Teardown`). The "generic" totals are coincidentally unchanged — other callers that were untagged
> acquired `NativeRoutine` labels across the same GN158→GN161 span, offsetting the three that left
> for `Boundary`/`Runtime`.*

**Not one Combat, Combat-Formula, Movement, Party, Actor, Spawn, Gambit, Status, Items or
Script-VM owner appears in any of the three lists.** Battle and field code does not call the C++
heap.

It does not need to, because its records are carved out of blocks obtained once, at manager
initialisation, and then sub-allocated by hand. `ActorStorage_AllocateAndInitializeRecords`
(`002679F0`) is the worked example, and its size arithmetic is in §4: it computes one total, takes
one block through the actor manager's own function pointer at `+0x88`, `memset`s the whole thing
to zero, writes the record count at `+0x00`, and then hands out interior pointers on a 16-byte
stride. Every actor record for that manager lives inside that one allocation for the lifetime of
the zone.

That is the fact a modder needs before touching anything: **an actor record is not a heap block.
It has no header, it cannot be freed individually, and its address is `poolBase` plus the sum of
the aligned record sizes ahead of it.** Writing past the end of one record writes into the next
actor.

### Failure is not handled *(answered: see the overview's 2026-09-28 and 2026-09-30 corrections - the arena retries, and some callers test for null; 2026-10-02, OPUS)*

~~`_set_new_mode` is imported and **never called**, so the CRT's new-handler mode stays at its~~
~~default of 0~~ *(Corrected 2026-09-30, SWE2-DATA: it is called once, as `_set_new_mode(0)`, by the first C++ initializer `00808D5C` through the import thunk `00862046`; the argument comes from the folded `return 0` stub (`pf_mem_checks.py` M1d). The shape is MSVC's stock `pre_cpp_initialization` — set the unhandled-exception filter, then `_set_new_mode(_get_startup_new_mode())` with the default stub returning 0 — toolchain startup, not a game decision (SWE2-AUDIT-SEM batch-4 review §2). So the new-handler mode is 0 by an explicit call)*: `malloc` returns `NULL` on failure rather than invoking a handler. The EXE imports
no `operator new` and no `operator delete` — every allocation route read for this document goes to
`malloc` or `_aligned_malloc` directly.

What happens next is up to the caller~~, and the callers mostly do not look~~ *(corrected 2026-09-30, SWE2-DATA: no census of which callers look has been made, `SD-165`)*. In
`ActorStorage_AllocateAndInitializeRecords` the returned pointer goes straight into `memset` with
no null test. ~~A failed actor-pool allocation therefore writes zeros from address 0 and the process~~
~~dies immediately with an access violation and no message — which is exactly the failure described~~
~~in §1.~~ *(Corrected 2026-09-30, SWE2-DATA: §1's crash narrative was struck on 2026-09-28 as never observed. The missing null test is a code fact; whether a null ever reaches it depends on the arena's retry and compaction (§1), and what the player sees has not been observed.)*

The STL side is different: `std::bad_alloc` is raised through `MSVCP140!_Xbad_alloc` at 23 sites
in 14 functions *(anchored 2026-09-30, SWE2-DATA: 23 call/jmp sites through the import slot, all inside 14 listed functions, `pf_mem_checks.py` M1)*. Those are `std::` containers, not engine containers, and 14 functions is a small
corner of a 38,161-function binary.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0016D680` | `eastl::allocator::~allocator` | 4 B | `mov rax,rcx; ret` — slot 0 of **both** allocator vtables |
| `0016D690` | `eastl::allocator::get_name` | 8 B | returns the `"EASTL"` string; slot 4 of both vtables |
| `0016D6A0` | `_guard_check_icall` | 3 B | `C2 00 00` = `ret 0`; the CFG check function named by the PE load config, **and** the stub every empty function folded onto; sixth qword of both allocator vtables — see §4 and **B-2/a** |
| `0016D6B0` | `eastl::allocator::allocate` | 10 B | `malloc(n)`; occupies **slots 1 and 2** of `008F6500` |
| `0016D6C0` | `eastl::allocator::deallocate` | 8 B | `free(p)` |
| `001EDF00` | `allocator_memory_log` constructor | 14 B | installs vtable `00902720`; 230 direct callers |
| `001EDF10` | `allocator_memory_log::allocate` | 100 B | `_aligned_malloc(n, alignment)` |
| `001EDF80` | `allocator_memory_log::allocate` | 90 B | `_aligned_malloc(n, 16)` |
| `001EDFE0` | `allocator_memory_log::deallocate` | 96 B | null-guarded `_aligned_free` |
| `0019C580` | aligned-malloc adapter | 9 B | `mov edx,edx; jmp _aligned_malloc` — drops offset and flags |
| `0019C570` | `_aligned_free` import thunk | 7 B | `48 FF 25` to the IAT |
| `0017D260` | engine `allocate(n, align)` | 12 B | 228 direct callers |
| `00584740` | engine `allocate(n)` | 16 B | alignment 16 via `lea edx,[r9+0x11]`; 29 callers |
| `00584730` | engine `free(p)` | 10 B | **2,309 direct callers** |
| `00809950` | `free` forwarder, hop 1 | 5 B | `E9` to `00210EB0`; 474 callers |
| `00210EB0` | `free` forwarder, hop 2 | 5 B | `E9` to `0019C590`; 240 callers |
| `0019C590` | `free` import thunk, hop 3 | 7 B | `48 FF 25` to the IAT |
| `0085E730` | `malloc` import thunk | 7 B | `48 FF 25` to the IAT |
| `002679F0` | `ActorStorage_AllocateAndInitializeRecords` | 436 B | the worked gameplay-pool example; formula in §4 |
| `0026CE60` | `ActorSystem_InitializeManagerRuntime` | 1332 B | sole caller of `002679F0` |
| `0020C610` | memory-status reader | 157 B | one of the two `GlobalMemoryStatusEx` sites |
| `00792F10` | memory-status reader | 306 B | the other |
| `00679A50` | audio stream buffer setup | 408 B | reads the `.data` allocator pair; 8 MiB ring plus `channels × 48000 × 4` |

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `008F6500` | `eastl::allocator::vftable` | vtable, 6 slots | table in §2 |
| `00902720` | `eastl::allocator_memory_log::vftable` | vtable, 6 slots | table in §2 |
| `01CED8C0` | `allocator_memory_log` COL | RTTI complete-object locator | names `.?AVallocator_memory_log@eastl@@` |
| `01D52540` | `allocator@eastl` COL | RTTI complete-object locator | names `.?AVallocator@eastl@@` |
| `01F480E8` | type descriptor | RTTI `type_info` | `.?AVallocator_memory_log@eastl@@` |
| `01F7E2F0` | type descriptor | RTTI `type_info` | `.?AVallocator@eastl@@` |
| `01CDAE78` | allocator name | `char[6]` | the string `"EASTL"` — the only reader is `0016D690` |
| `01F82E48` | memory-log record pointer | `void*` global | lazily created 0x20-byte record; layout in §4; **no reader** |
| `01F2EA70` | ~~intrusive list sentinel~~ **ordered keyed-tree header** | 6 self-pointing qwords | root at `+0x18`; elements linked through **element `+0x08`** and ordered on a key at element `+0x20`; empty at rest (see `UQ-326`) |
| `01F2EAA0` | ~~count~~ **terminator pad** *(corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 281)* | `u64` | initialised `2`. Its one reader, `00677030`, adds it to the string length before allocating (`006770A2`–`006770AC`) and zeroes that many bytes after the copy (`006770D5`–`006770E1`): a two-byte zero terminator, not a count. Declared in the type store as `StringTerminatorPad01F2EAA0` |
| `01F2EAA8` | injected allocate hook | function pointer | holds `00584740` — **`_aligned_malloc(size, 0x10)`**; read by `00679A50`, `0067A480` only |
| `01F2EAB0` | injected free hook | function pointer | holds `00584730` — **null-guarded `_aligned_free`**; same two readers |
| `008C2B40` | IAT slot | `void*` | `api-ms-win-crt-heap-l1-1-0!malloc` |
| `008C2B48` | IAT slot | `void*` | `!free` |
| `008C2B60` | IAT slot | `void*` | `!_aligned_malloc` |
| `008C2B70` | IAT slot | `void*` | `!_aligned_free` |

The eight heap IAT slots are contiguous from `008C2B40` to `008C2B78` in import-name-table order:
`malloc`, `free`, `_msize`, `realloc`, `_aligned_malloc`, `calloc`, `_aligned_free`,
`_set_new_mode`. That contiguity is what confirms the slot-to-symbol mapping: the descriptor
declares eight names and the eight slots sit in eight consecutive qwords.

## 4. Data structures and formulas

### The memory-log record

```struct EastlMemoryLogRecord base=record size=0x20
+0x00  u32   budgetBytes      written 0x02000000 (32 MiB); never read
+0x04  u32   blockBytes       written 0x00200000 (2 MiB); never read
+0x08  u32   unwritten0       not written by the initialiser
+0x0C  u32   unwritten1       not written by the initialiser
+0x10  u64   totalBytes       written 0; never read, never incremented
+0x18  u32   liveCount        written 0; never read, never incremented
+0x1C  u32   unwritten2       not written by the initialiser
```

`+0x08`, `+0x0C` and `+0x1C` are **UNACCOUNTED**. The initialiser writes `+0x00`, `+0x04`, a qword
at `+0x10` and a dword at `+0x18`, and leaves the rest as whatever `malloc(0x20)` returned.
Nothing reads any of it, so their meaning is not recoverable from this build.

### The alignment arithmetic

The two engine entry points differ only in how the alignment argument is produced:

```c
// 00584740 -- allocate(size)
_aligned_malloc(size, 16);          // 16 materialised as lea edx,[r9+0x11] with r9 == -1

// 0017D260 -- allocate(size, alignment)
_aligned_malloc(size, alignment);   // caller's alignment; offset and flags discarded

// 00584730 -- free(p)
if (p != NULL) _aligned_free(p);
```

`_aligned_malloc` requires its alignment to be a power of two; it is the caller's job to ensure
that, and neither adapter checks.

### The actor-pool size formula

This is the arithmetic that decides how much memory one zone's actors occupy. From the complete
body of `002679F0`, with `M` the actor manager and `L` the record-descriptor table base it reaches
through `M->aUnknown_000_007`:

```c
kinds  = *(u16*)(L + *(int*)(L + 0x14));        // number of record kinds
n      = M->nActorRecordCount;                  // total records

// per-kind storage, each record rounded UP to a 16-byte multiple
payload = 0;
for (k = 0; k < kinds; k++) {
    u16 recordSize = recordSizeTable[k];        // stride 4, from DAT_01E0C32A
    u16 count      = countArray[k];             // stride 2, at L + *(int*)(L + 0x14) + 2
    payload += ((recordSize + 15) >> 4) * count * 16;
}

// the pointer array, rounded up to 16 and then doubled
header  = (n * 8 + 0x17) & 0xFFFFFFF0;
prefix  = header * 2;

total   = prefix + payload;
```

`((x + 15) >> 4) * 16` is `x` rounded up to the next multiple of 16 — the same result as
`(x + 15) & ~15`, written the way the compiler emitted it. `n * 8 + 0x17` is `n` pointers of 8
bytes, plus 8 for the count word at `+0x00`, plus 15 for the rounding, before the `& ~15`.

The block is then laid out as:

```
pool + 0x00                     u32   record count (n)
pool + 0x08                     ptr[] record pointers, one per record
pool + header                   -->   M->field_0x1F0 points here
pool + prefix                   ...   the record payloads, 16-byte stride
```

and every record's byte at `+3` is packed with its kind:

```c
record[3] = (record[3] & 0xE0) | (indexWithinKind & 0x1F);
record[3] = (indexWithinKind & 0x1F) | (kindId << 5);
```

so the low 5 bits are an index within the kind and the top 3 bits are the kind id — a packed byte
with room for **32 records per kind and 8 kinds**. The first of those two lines is dead: the
second overwrites the whole byte. It is left in the shipped binary and is recorded here because a
modder single-stepping the loop will see both writes and should not read meaning into the first.

The block itself is obtained through the manager's own hook, and the result is not checked:

```c
pool = (*(void*(**)(int))(M + 0x88))(total);   // call qword ptr [R15+0x88], at 00267A79
memset(pool, 0, total);                        // <-- no null test on `pool`
```

### The import census, corrected

| measure | counting only `FF 15 [rip+slot]` | counting the transitive chains |
|---|---:|---:|
| import slots reached | 417 / 538 | **495 / 538** |
| total call sites | 3,543 | **7,707** |
| `sqrtf` | 0 | **566** |
| `memset` | 0 | **830** |
| `memcpy` | 0 | **632** |
| `free` | 37 | **860** |
| `malloc` | 30 | **78** |

The transitive walk resolves **206 functions** in `.text` that are nothing but a route to an
import: `E9 rel32` to another such function, or `FF 25` / `48 FF 25` to an IAT slot, to a depth of
up to three hops.

### The folded empty function, and why it cannot be named from a vtable

`0016D6A0` is three bytes — `C2 00 00`, `ret 0` — followed by `int3` padding. It has ~~**2,479~~
~~incoming calls**~~ **2,528 incoming `call` sites and 340 `jmp` sites, from 2,480 functions** *(corrected 2026-10-02, OPUS: direct edges over the current function extents; 2,479 is close to the function count, not the call count)*, more than any other function in the binary, and it turns up under several
different names. All of them are describing the same three bytes.

It has one identity that is genuinely established, and it comes from the PE itself rather than
from any body. The image's load-configuration directory (`01CEBE40`, `Size` = 148) declares:

```
GuardCFCheckFunctionPointer     = 008C31C0   ->  holds 0016D6A0   (ret 0)
GuardCFDispatchFunctionPointer  = 008C31C8   ->  holds 00896270   (jmp rax)
GuardCFFunctionTable            = 0
GuardCFFunctionCount            = 0
GuardFlags                      = 0x00000100  (IMAGE_GUARD_CF_INSTRUMENTED only)
```

So `0016D6A0` **is** the Control Flow Guard check function, by the binary's own declaration — and
CFG is inert in this build: the check returns immediately, the dispatch is an unchecked `jmp rax`,
and there is no valid-target table at all (`GuardCFFunctionTable = 0`, and `GuardFlags` carries
`CF_INSTRUMENTED` without `CF_FUNCTION_TABLE_PRESENT`). For a modder that is load-bearing:
**indirect calls in this build can be redirected without CFG rejecting the target.** This
corroborates the image-hardening document from a second direction — that document read the bodies,
this reads the load config, and they agree.

The second thing that is true of these three bytes is that identical-COMDAT folding merged every
empty function in the program onto them. `ret 0` is what an empty `__cdecl`-shaped function
compiles to, so an empty destructor, an empty setter and the CFG check are byte-identical and the
linker keeps one copy.

**That is exactly why a vtable slot cannot name it.** `0016D6A0` occupies the sixth qword of both
allocator vtables. What that proves is that *the sixth virtual of each allocator class is empty* —
not which function it is. EASTL's allocator interface puts `set_name(const char*)` in that
position and an allocator that does not record a name would compile it to nothing, which makes
`set_name` a reasonable reading of the *slot*; it is a tier-6 inference from the library's shape,
and the **body carries no identity of its own**. Written down as a name in a table it would look
like a finding, and it is not one.

**This sharpens ~~open~~ question B-2/a** ~~rather than closing it~~ *(superseded 2026-09-26, FABLE, Claude Opus 5.5: B-2/a was closed on 2026-09-07 in the negative, on exactly this reasoning)*. B-2/a asks which empty destructor
the linker folded onto `0016D6A0`, and the framing assumes there is a hidden identity to recover.
There is not one identity — there are many, and the population is "everything in the program whose
body is `ret 0`". Two members can be named from evidence and neither is named by the body: the CFG
check, named by the load config; and at least one genuine empty destructor, proven independently in
the exception-funclet document by `Unwind@0089dd0e` passing `0016D6A0` as an **array-element
destructor**, which a CFG check cannot be. The source-level destructors remain unrecoverable
from this image, and no amount of counting call sites or reading vtable slots will recover them.
That is the answer B-2/a should carry: **not "we have not found it yet" but "the information was
destroyed at link time, and here is the one member that survived because something outside the
code section still points at it."**

## 5. Call chain

```
engine subsystem needs a buffer
  -> 0017D260  allocate(n, align)        (228 callers)     -+
  -> 00584740  allocate(n) [align 16]    (29 callers)       +-> 0019C580 -> IAT -> ucrtbase!_aligned_malloc
  -> 001EDF10 / 001EDF80  (virtual, via vtable 00902720)   -+

  -> 0016D6B0  eastl::allocator::allocate (virtual, via vtable 008F6500)
                                                            \-> IAT -> ucrtbase!malloc

engine subsystem releases a buffer
  -> 00584730  free(p)                   (2,309 callers)   --> 0019C570 -> IAT -> ucrtbase!_aligned_free
  -> 001EDFE0  deallocate (virtual)                        -/
  -> 0016D6C0  eastl::allocator::deallocate                 --> 00210EB0 -> 0019C590 -> IAT -> ucrtbase!free
```

**Upstream (who causes this):** PhyreEngine reflection and object lifecycle dominates — 1,515 of
the 2,309 `00584730` callers carry a `Phyre.*` CodeDomain. Resource, Audio, Input and Presentation
appear in small numbers. Zone load and teardown is what drives the volume.

**Downstream (what this causes):** `ucrtbase.dll`'s heap, which sits on the Windows process heap.
Nothing inside `FFXII_TZA.exe` is downstream of the allocator; it is a leaf.

**The gameplay chain is a different chain and ~~does not join this one~~ joins this one only at boot, where its arenas take their backing from `malloc`:** *(corrected 2026-10-02, OPUS: `0036D240` is `jmp 0085E730`, the `malloc` stub, called nine times by `0022A0B0`)*

```
ActorSystem_InitializeManagerRuntime (0026CE60)
  -> ActorStorage_AllocateAndInitializeRecords (002679F0)
     -> (*M->hook_0x88)(total)          <-- ONE call, per manager, per zone
        -> memset(pool, 0, total)
           -> ActorStorage_InitializeRecord, once per record, on interior pointers
```

**Do not confuse with:** `BattleUnit_AllocateSlotAndBindActor` (`00234480`),
`BattleActionSnapshot_AllocateSlot` (`0030DFA0`) and `BattleAction_AllocatePresentationSlot`
(`0030D070`) are named "Allocate" and allocate **no memory**. They claim an index in a table that
already exists. Slot allocation and memory allocation are different mechanisms in this engine and
the names do not distinguish them.

Also do not confuse the three-hop `free` forwarder chain (`00809950` → `00210EB0` → `0019C590`)
with three different functions. They are one operation, and all three carry the name `free`.

## 6. Modding notes

- **Best intervention point.** To redirect *engine* allocation, patch `0017D260` and `00584740`
  (allocate) together with `00584730` (free). Those three cover the non-virtual majority. To
  redirect everything you must also patch the two vtables at `008F6500` and `00902720` — they are
  in `.rdata` and read-only at runtime, so that needs a page-protection change. Patching the IAT
  slots at `008C2B40` / `008C2B60` / `008C2B48` / `008C2B70` is the single cheapest hook and
  catches every route at once, including the CRT's own internal use.
- **Never mix the two families.** `_aligned_malloc` puts a back-pointer immediately before the
  block it returns. A pointer from `00584740` or `0017D260` **must** go to `_aligned_free`, and a
  pointer from `0016D6B0` **must** go to `free`. Swapping them corrupts the heap silently and
  crashes somewhere else, later, in unrelated code.
- **`_aligned_malloc` requires a power-of-two alignment** and neither adapter validates it.
  Passing a non-power-of-two through `0017D260` fails the allocation and returns `NULL`, which the
  caller will not check.
- **Regenerates itself:** ~~nothing here. There is no free list, no pool and no bookkeeping in the~~
  ~~game to keep consistent — the heap state lives entirely inside `ucrtbase.dll`.~~ *(Corrected 2026-09-30, SWE2-DATA: true only of the direct CRT-heap route. The arena allocator keeps its own bookkeeping: free-list ends `+0x90`/`+0x98`, handle slots, per-tag usage counters and a 64 KiB page table (the arena sections below), and its compaction moves tagged blocks (SECTION-07). A replacement allocator has to keep all of that consistent.)*
- **Breaks if:** you free an actor record. Records are interior pointers into one block; only the
  block base returned by the manager's `+0x88` hook is a valid free target. It also breaks if a
  replacement allocator returns a pointer with less than 16-byte alignment — the engine assumes 16
  throughout.
- **The memory log is not a hook point.** `01F82E48` looks like an accounting record and is not
  one; writing a smaller budget there changes nothing, because nothing reads `01F82E48`.
- **Multiplayer / XIIOnline:** allocation is entirely local derived state — no address, pool
  offset or record index in this system is authoritative world state, and none of it is meaningful
  to send. Note the corollary for this project's own detour rules: `00584730` and `0017D260` are
  called from inside frame-critical paths, so the standing "no heap allocation inside a native
  detour" rule is not merely stylistic here — a detour that allocates is re-entering the same
  allocator the engine may already be inside.
- **Mod compatibility:** the record-size table at `DAT_01E0C32A` drives the pool formula in §4. A
  mod that enlarges a record kind changes `total` and every interior offset after it. Two mods
  that both edit that table will not compose.

## 7. What is not known

- [x] What writes `ActorManager + 0x88`, the function pointer through which every actor pool is
      allocated. A `.text` scan for `lea rXX,[rip+fn]` immediately followed by
      `mov [rXX+0x88], rXX` finds four sites, none of them on this object, so it is installed by
      some other instruction form or copied from a template. Until it is found, the claim
      "gameplay records do not come from the EASTL heap" rests on the caller census, not on
      reading the hook.
      **Answered 2026-09-14 (FABLE): the bind writes it, and all three hooks allocate from the engine arena.**
      `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` sets `r12` to `00267930` at `0026C8E3` and replaces it with its
      third argument when that is non-null (`cmovne r12, r8`, `0026C8FA`). It stores `r12` into the bound slot's `+0x88`
      at `0026CAE6`, about 110 instructions later, which is why a "`lea` immediately followed by the store" scan could not
      see it. Its one caller, `ActorResource_OnDefinitionPayloadLoaded` `0032F850`, passes one of three hooks:
      `00267C20` (`0032F923`), `00267BB0` (`0032F945`) or `00267930` (`0032F95A`). Each is preceded by an arena
      selection `0036C1D0` (arena 5 or a per-kind choice from `0036B200`). All three hooks run the same sequence:
      `0036C1D0` select, `0036C750("..\..\katano\ateldecode.c")`, `0036A100` allocate, `0036C660` tag (with the constant
      `0x1676` in `00267930`), `0036C140` restore. So the pool comes from the `0036A100` arena, and the claim above now
      rests on the hook itself.
- [x] **UQ-325.** What `+0x08`, `+0x0C` and `+0x1C` of the memory-log record were for.
      ***Closed 2026-09-21 (FABLE) as unanswerable from this build — the substance was already
      above, and only this row had not caught up.*** §*The memory log that logs nothing* establishes
      every step the question needs: `allocator_memory_log`'s **three** methods each run the same
      lazy initialiser, which writes `+0x00`, `+0x04`, the qword at `+0x10` and the dword at `+0x18`
      and nothing else; the displacement census finds **exactly three** references to `01F82E48`,
      all three were read in full, and **none lets the pointer escape**, so no code can reach the
      record to write the other three fields or to read any of them. They therefore hold whatever
      `malloc(0x20)` left there, for the life of the process.
      **So the answer is that this build cannot have one**, and that is a result rather than a gap:
      *no further reading of this image will recover the meaning*, because the fields are never
      written by the only code that can see them. Recovering it would need a build of the same EASTL
      interface — the same bar §`UQ-327` sets for the sixth virtual.
      *(Re-checked against the image on 2026-09-21 before closing: a `ripscan` of `01F82E48` returns
      six entries, which are these three sites counted once per read and once per write.)*
- [x] ~~Whether `eastl::allocator` (the `malloc` one, vtable `008F6500`) is ever actually
      instantiated at runtime, or is only linked in. Its constructor was not located.~~ **Answered 2026-09-14 (FABLE),
      statically: it is instantiated, inline.** There is no standalone constructor. Five functions load the vtable with a
      RIP-relative `lea` (`tools/ripscan.py`), and four of them immediately store it as an object's vptr:
      - `001A2130` at `001A21E6` → `[obj + 0xE0]`. This is the `0x520`-byte map-art context built on first use by
        `001A98B0` ([game application](../../00-Engine-Core-Runtime/Application-Root/game-application.md)).
      - `001A9940` at `001A99DC` → the global object at `01F811B8`. It is the `phyremaps.txt` remap-table accessor
        ([ta lists](../../02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md)), with
        three callers.
      - `001E1670` at `001E1719` → `[obj + 0x70]` (one caller, `001A655C`).
      - `00676BD0` at `00676C62` → the global at `02D3ECD8` (callers `0063B1DA`, `00677D15`).

      The fifth, `006CC330` (`006CC344` → `[rcx + 0x18]`), has no direct caller. The image also holds two qword copies of
      the address; where they sit was not traced. These are static reachability through the map-art and remap-table
      paths, not a runtime observation.
- [x] **UQ-326.** What the intrusive list at `01F2EA70` links, and ~~which subsystem owns the object that
      carries the injected allocator pair at `01F2EAA8` / `01F2EAB0`~~.
      ***The allocator half is answered 2026-09-21 (FABLE); the list half is not.***

      **The sweep splits the object cleanly.** Every rip-relative reference into
      `01F2EA70`–`01F2EAB8` — 48 of them across nine functions — is either one of the six
      self-pointer resets of `+0x00`..`+0x28`, or one of **exactly two readers of the hook pair**:
      `00679A50` and `0067A480`.

      **Both readers hand the pair to the same generic pool initialiser.** `00679A50` loads the free
      hook into `rax` and the allocate hook into `r9`, puts the free hook in the fifth-argument slot
      and calls `006CC5A0(rsi+0x150, 0x800000, seconds << 13, alloc, free)` (`00679B63`–`00679B93`);
      `0067A480` does it twice more with a `0x2000000` budget (`0067A800`–`0067A84C`). So
      `006CC5A0(target, budget, count, alloc, free)` is a **sized-pool initialiser that takes its
      allocator as an argument**, and this pair is what gets passed.

      ***And the caller names itself in arithmetic, not in a tag.*** Eleven bytes after that first
      call, `00679B98` does `imul ebx, ebx, 0xBB80` and `shl rbx, 2`, then calls the **allocate hook
      directly**. `0xBB80` is **48,000**, so the block is ~~`seconds × 48 kHz × 4 bytes` — 16-bit~~
      ~~stereo~~ `channels × 48,000 × 4 bytes`, one second of 4-byte samples per channel *(corrected 2026-10-02, OPUS: `ebx` is `[rsi+0x324]`, loaded at `00679A50+0x10D`; `+0x320` is a libvorbis `vorbis_info` set up by `00880AF0` and read by `008800C0`, whose `008800C0+0x74` compares the `vorbis` header tag, so `+0x324` is `channels`; §1's table row says the same)*. *That is what identifies the consumer as audio streaming*; the ledger tags on those two
      bodies agree, but they are not what the claim rests on.

      **The pair is the CRT aligned heap, not the engine arena this page is otherwise about.**
      `00584740` is `or r9d, -1` / `xor r8d, r8d` / `lea edx, [r9+0x11]` / `jmp 0019C580`, so it calls
      the import at `008C2B60` with **alignment `0x10`**; `00584730` is `test rcx, rcx` /
      `jne _aligned_free` / `ret`. *Both identities are prior art* — the table above and
      [the Phyre cluster contract](../../22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md)
      already name them — and I re-resolved `008C2B60` from the PE import directory rather than
      trusting the row: `_aligned_malloc`, `api-ms-win-crt-heap-l1-1-0.dll`. So a subsystem is
      configured onto the **CRT aligned heap at 16-byte alignment**, with 8 MiB and 32 MiB budgets,
      while the gameplay records §4 follows come from the engine arena.

      ***And the list half, after the sweep's own blind spot was allowed for.*** The rip sweep finds
      no insertion because **the container is passed by pointer**: `00676450` does
      `lea rbx, [01F2EA70]` (`00676575`) and then calls `006750C0(container, key)` and, only if that
      returns null, `0067F700(container, element)` (`0067657F`–`00676596`) — with a **duplicate
      rejected as error `0x12`**, and the pair bracketed by `0080929C` / `005CD820`, so registration
      is **locked**.

      **The lookup identifies the structure, and it is not a list.** `006750C0` walks from the
      container's `+0x18`, and at `0067510A` converts a node pointer to its element with
      **`lea rbx, [rax - 8]`** — so the intrusive node sits at **element `+0x08`**. It then compares
      the candidate's `+0x20` against the sought `+0x20` through `00675EF0` (`00675129`–`00675143`)
      and uses the **sign** to pick one of two child links, `[rbx + rax*8 + 8]` (`0067514C`–
      `00675152`). Two children chosen by a comparison is an **ordered binary tree**; and `00675EF0`
      compares `dword[a]` against `dword[b]` first and only then continues, which is a **length-first
      key comparison**. ***So the row above calling this an "intrusive list sentinel" understates it***
      — it is the empty state of an ordered, keyed tree, and that row is corrected.

      ~~**What is still not established** is what the elements *are*: `00676450` receives both the
      element and the key as arguments, so naming the population needs its callers, which I did not
      trace.~~ **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): the tree is Phyre's process-wide registry of
      named `PAssetReference` objects, keyed by name.** *(The sentence it replaces is wrong in one detail
      too: `00676450` takes a whole instance list, not an element and a key.)*
      - **Both insert routes are `PClassDescriptor<PAssetReference>` methods.**
        - Slot 14 (vtables `00D6BB00` / `00D6BB88`, the adapter `00674B50` → `00676450`) registers every
          instance in an instance list. The count is `[list + 0x70]`, and the stride is the class size
          `[[list + 0x50] + 0x38]`.
        - Slot 10 (`00674BE0` → `006753A0` → `00677BA0`) registers one object.
      - **What registration does to each object:**
        1. It takes the tagged name pointer at `+0x30`, with bit 0 cleared; a null name returns `0x15`.
        2. It resets the node at `+0x08`.
        3. It stores the key, the engine's UTF-8 string hash of the name with seed `0x7B5`, at `+0x20`, and the name at
           `+0x28`. The slot-14 route also stores the list's `[list + 0x48]` at `+0x48`.
        4. It takes the lock `02D3E880` and builds the tree on first use: magic static `02D3EC9C`,
           destructor `008B1C00` via `atexit`.
        5. `006750C0` looks the key up. **A hit returns `0x12`**, a duplicate name; otherwise `0067F700`
           inserts it.
      - **Correction to the paragraph above.** `00675EF0` compares the **hash** first: the dword at `+0x20`,
        `00675EFA`–`00675F1C`, the string hash. Only then does it compare the names. It is not a
        length-first comparison.
      - **The reader.**
        - `00676BD0` finds an entry by name: the hash, then `memcmp`.
        - `00677CE0` uses it to resolve an import, and on a miss prints *"Failed to find asset %s of type
          %s, using fallback"* (`00D6C448`).
        - `00677CE0` is reached from `0063DA50`, the by-name asset fetch that game code calls from four places.
        - `00676A70` walks the same tree from its root; it has no direct caller and no stored pointer.
      - **So a named asset becomes findable by name once its cluster's `PAssetReference` instances are
        registered**, and two clusters exporting one name collide with `0x12`. **Not read:** whether
        entries are removed when a cluster unloads.

      **Not claimed:** how often either pool is built, or that the code constants are the sizes
      a real session uses.
- [x] **UQ-327.** Whether the sixth virtual of the two EASTL allocator classes is `set_name`. The slot is ~~*(NO ADMISSIBLE SOURCE, reviewed and signed 2026-09-26 by OPUS; see the register row UQ-327.)*~~ *OUT OF EVIDENCE BOUNDARY, 2026-09-27 (FABLE, Claude Opus 5.5): FRONTIER's batch-K Extension 2026-09-27f classes an identifier name by its carrier, the unshipped source / `FF12X64.pdb`; OPUS's signature carries. See the register row UQ-327.*
      proven; the identity is a tier-6 inference from EASTL's interface shape and the body is the
      universal folded stub, which carries no identity. Deciding it needs an EASTL build with the
      same interface, not more work on this image.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Eight heap imports, all from `api-ms-win-crt-heap-l1-1-0` | PE import directory parsed from the shipping EXE; slots verified contiguous `008C2B40`–`008C2B78` against the thunk bodies that jump to them | 1 |
| No `VirtualAlloc` / `HeapAlloc` / `HeapCreate` / `MapViewOfFile` | complete enumeration of all 538 import symbols, not a filtered search | 1 |
| The CRT is not app-local | directory listing of the shipping `x64` folder — no `ucrtbase.dll`, no `api-ms-win-crt-*`, no `MSVCP140` / `VCRUNTIME140` | 1 |
| Two EASTL allocator classes and their vtables | MSVC RTTI complete-object locators `01CED8C0` / `01D52540` → type descriptors `01F480E8` / `01F7E2F0`; vtable extents read to their terminating zero qword | 4 + 1 |
| Slot semantics (`allocate` / `deallocate` / `get_name`) | complete exact-current bodies of all ten distinct vtable targets | 1 |
| `allocator` = `malloc`, `allocator_memory_log` = `_aligned_malloc(·,16)` | complete bodies of `0016D6B0`, `0016D6C0`, `001EDF10`, `001EDF80`, `001EDFE0` with IAT targets resolved | 1 |
| The `"EASTL"` name string | string at `01CDAE78`; single reader `0016D690` | 2 |
| `00584730` has 2,309 distinct callers | freshly regenerated `edges.tsv` from this session's own project import, cross-checked against a raw `E8 rel32` scan of `.text` | 11 + 1 |
| Transitive import census 495/538, 7,707 sites | fixed-point walk over `E9` / `FF 25` / `48 FF 25` forwarders, then every `E8` and `FF 15` site in `.text` | 1 |
| The memory-log record has no reader | four-byte displacement census of the whole `.text` for `01F82E48`; three hits, all read in full; positive controls stated in §2 | 1 |
| Actor-pool size formula | complete exact-current body of `002679F0` | 1 |
| The pool is taken through `M + 0x88` | `002679F0` body; indirect call `call qword ptr [R15+0x88]` at `00267A79` | 1 |
| `pool` is not null-checked before `memset` | `002679F0` body | 1 |
| ~~`_set_new_mode` never called~~ `_set_new_mode` called once, with 0, at startup *(corrected 2026-09-30, SWE2-DATA)* | ~~transitive census, 0 sites~~ [`pf_mem_checks.py`](../../_index/candidates/dd-data-4-0930/pf_mem_checks.py) M1d | 1 |
| Gameplay owners absent from allocator callers | caller sets from the fresh call graph, grouped by `GFZ.V120.PrimaryOwner.*` tag | 11 |
| Four `sqrtss` in the whole image | REX-aware byte-pattern scan of `.text`; all four confirmed by disassembling the containing instruction | 1 |
| `0016D6A0` is the CFG check, and CFG is inert | PE load-configuration directory at `01CEBE40` read directly from the authorized EXE: check pointer `008C31C0` → `0016D6A0`, dispatch `008C31C8` → `00896270` (`jmp rax`), function table 0, count 0, `GuardFlags` `0x00000100` | 1 |

**Superseded readings:**

- *During this session*, a first pass counting only `call qword ptr [rip+slot]` concluded that
  **`sinf`, `cosf`, `sqrtf`, `powf` and every other transcendental had zero call sites**, and that
  the game therefore carried its own maths library. That was wrong. `memset` and `memcpy` also
  scored zero on the same instrument, which is what exposed it: MSVC reaches those imports through
  `E9` / `FF 25` forwarder chains up to three hops long. The corrected figures are in §4. The
  reading was reachable because the `FF 15` form is what an import call is *expected* to look
  like, and because the census's own headline — "417 of 538 slots reached" — sounds like a
  near-complete answer rather than a two-thirds one. Recorded in `COVERAGE.md`.
- *Corrected before first publication, after a peer session's `check_consistency` run found
  `0016D6A0` carrying three different names across five citations.* This document had it as
  a bare `ret` (`C3`) and named the vtable slot `set_name` in a table, as though that were
  established. Both were wrong in kind: the body is `C2 00 00` (`ret 0`), and a slot position
  cannot name a folded stub — it can only show that the slot's function is empty. The load-config
  derivation in §4 was re-run independently here and reproduces the peer's reading exactly
  (`GuardCFCheckFunctionPointer = 008C31C0` → `0016D6A0`, table 0, count 0, flags `0x00000100`).
  The reading was reachable because the two allocator vtables really do both carry the address at
  slot 5, which is a strong structural signal — and it is a signal about the *slot*, not about the
  *body*.
- **No claim in this document rests on `.pdata`, `.xdata`, unwind records, EH maps or
  `_IMAGE_RUNTIME_FUNCTION_ENTRY`.** Function extents come from the GZF's function manager and
  every body cited was read.


## The arena allocator's own data structure — [`EXP-123`](../../_experiments/EXP-123-alloc-core-exec.md), folded in 2026-09-19 (OPUS)

This page has described `0036BC60` as *"the game's own arena allocator: fifteen heaps as `0xA8`-byte
records"* since it was written. That is the **descriptor table**. `EXP-123` executed the allocator
and recovered **what is inside an arena**, which is the part a reconstruction actually needs.

> **Evidence class.** Isolated original-machine-code execution, re-read from the bytes here before
> adoption. It establishes what the body computes for planted inputs. **It does not establish which
> allocations the game makes**, and nothing below should be read as a claim about live heap state.

### Two link pairs — but `+0x90`/`+0x98` are ONE list's ends

**`EXP-123` reads `+0x90` and `+0x98` as the roots of two separate lists. They are not, and this
page already had it right:** they are the **head and tail of a single doubly-linked free list**.
The two search arms settle it, because they walk the same list from opposite ends:

```
0036BCEA  mov rax, qword ptr [rbx + 0x98]     ; the TAIL
0036BCF3  mov rcx, qword ptr [rbx + 0x90]     ; the HEAD
0036BCFA  test ebp, ebp
0036BCFC  jne  0036BD2C
          ; arg4 == 0 : forward from the HEAD
0036BD03  cmp  dword ptr [rcx + 0x18], r14d   ; size key >= request?
0036BD09  mov  ecx, dword ptr [rcx + 8]       ;   ... else advance by +8      <- NEXT
0036BD0C  call 0020E600                       ;   decode the BASE-encoded link
0036BD17  jne  0036BD03
          ; arg4 != 0 : backward from the TAIL
0036BD31  cmp  dword ptr [rax + 0x18], r14d   ; the SAME predicate
0036BD37  mov  ecx, dword ptr [rax + 4]       ;   ... else advance by +4      <- PREV
0036BD3A  call 0020E600
0036BD42  jne  0036BD31
```

**One list, `+0x08` forward and `+0x04` back, first-fit from the head or last-fit from the tail —
which is exactly what this page said before `EXP-123` ran.** The carve-time fixups at
`0036BDE4`–`0036BE27` are consistent with either model, which is presumably how the two-list
reading survived: a node that was the head re-heads `+0x90`, a node that was the tail re-tails
`+0x98`, and a remainder that replaces the node in place takes both.

**A second link pair does exist**, and the coalescer is where it is used — `0036B210` decodes
`[rdx+4]`, `[rbx+4]`, `[rbx+8]` **and `[rdi+0xC]`** through `0020E600` in one body. So `+0x0C` and
`+0x10` are real links, and `EXP-123`'s reading of them as physical adjacency fits a coalescer's
need to reach a block's memory neighbours without searching. ~~**What is NOT established is where
that second list is rooted** — not at `+0x90`/`+0x98`, which are spoken for. Recorded as open
below rather than assigned a root.~~ The second pair is a physical-order chain rooted at the descriptor's `+0x10`, the first block header. Only the
arena initializer writes that field, the chain's two ends are encoded nulls, and its links are written only by the
arena's header fill, its insert-after / insert-before pair and its unlinker; the dump walker starts at `+0x10` *(answered 2026-10-02, FABLE, static; addresses and controls in [`mempage-residue-fable-1002`](../../_index/candidates/mempage-residue-fable-1002/README.md) item 2)*.

> **Every link is `BASE`-encoded** — ~~`d[link] = ptr − arena`~~ `d[link] = (u32)ptr − (u32)base`, `base` the qword at `01F83530`, not the arena *(corrected 2026-10-02, OPUS: `0020E620` is `sub ecx, [01F83530]` and `0020E600+0x2` adds the qword back; no other instruction references `01F83530`, which lies in zero-filled `.data`)*, decoded through
> `ImageAddress_ResolveRuntimePointer` (`0020E600`) on every single hop above, and encoded by its
> inverse `RuntimePointer_EncodeImageAddress` (`0020E620`). **The roots are raw qword pointers and
> the links are 32-bit offsets**, and that asymmetry is real: `0036BDE4` compares `+0x90` against a
> pointer with no decode. A reimplementation that makes the two representations uniform breaks.

### The block header is `0x40` bytes

| offset | width | what |
|---|---|---|
| `+0x03` | 1 | allocation kind |
| `+0x04`, `+0x08` | 4, 4 | free-list links (`BASE`-encoded) |
| `+0x0C`, `+0x10` | 4, 4 | adjacency links (`BASE`-encoded) |
| `+0x14` | 1 | flags — bit 0 set at `0036BE7E`, cleared at `0036BE9B`/`0036BF70` |
| `+0x15` | 1 | flags — `or` at `0036BE67` |
| `+0x16` | 1 | **tag**, written at `0036BE8D`, read at `0036BD57` |
| `+0x18` | 4 | **size key**; the block's extent is `key + 0x40` (`0036BD03`, `0036BD31`, `0036BDA9`) |
| `+0x3E` | 2 | ~~**mark word**~~ guard word, written as zero at `0036BE91`, `0036BEA5`, `0036BF74` *(corrected 2026-10-02, OPUS: the stored `r13w` is zeroed at `0036BC60+0x222`; the mark byte is header `+0x02`)* |

**The magics are real and they are a pair:** `0xFF12` for a live block and `0xFF99` for an unlinked
one. `0xFF12` appears at five sites across the family — `003698BC`, `0036A4A8`, `0036C675`,
`0036C701`, `0036CB3F` — and `0xFF99` at exactly one, `0036CA92` in `0036C9D0`. **One producer of
"unlinked" against five checkers of "live"** is worth knowing before anyone calls a validation site
redundant.

> ~~**The header is NOT being added to `_types/` yet, and that is deliberate.**~~ *(answered: see "What this settled in `_types`" below - `ImageAddressArenaBlockHeader`, 2026-09-20; 2026-10-02, OPUS)* Nine of its
> sixty-four bytes are accounted for above. Writing a type row set now would mean inventing
> `unobservedSpan` rows over `+0x00`–`+0x02`, `+0x19`–`+0x3D` and `+0x3F` — **fifty-odd bytes of
> gap consumed to make the layout look complete**, which is the one thing the store's rules forbid.
> It goes in when the gaps are read, not when the named fields are.

### Carving, and the two modes are a single tail

The fourth argument selects which end of a free block is handed out:

```
0036BDB2  test ebp, ebp                 ; arg4
0036BDB4  jne  0036BDC5
          ; arg4 == 0 -> FRONT
0036BDB9  mov  rsi, rdi                 ;   result  = node
0036BDC0  add  rbp, rdi                 ;   remainder = node + 0x40 + size
0036BDC3  jmp  0036BDD9
          ; arg4 != 0 -> TAIL
0036BDC8  mov  rsi, r13                 ;   result  = node + key - size
0036BDCE  mov  rbp, rdi                 ;   remainder = node
0036BDD9  sub  r13d, r14d               ; rem = key - size - 0x40  (both modes)
0036BDDC  sub  r13d, 0x40
```

Both modes converge before the remainder is computed, and **`0036B210` coalesces eagerly after
every split**, through the shared tail at `0036BF1C`. There is no deferred-merge pass to model.

### The rest of the descriptor

- **A page table at `q[desc+0x28]`** holding the lowest-addressed head per 64 KiB, with a companion
  bitmap at `q[desc+0x20]`; the page slot is a **signed** 16-bit floor, so a negative slot is
  representable and the sign is load-bearing.
- **Per-tag usage counters** at `d[desc+0x68 + tag*4]`, and a sequence counter `w[desc+0x60]`
  incremented per operation.
- **Where the `+0x0C`/`+0x10` link pair is rooted.** The pair exists and the coalescer uses it; `+0x90`/`+0x98` are the free list's ends and cannot also be its roots. ~~**Open.**~~ *(Answered by reconciliation 2026-09-30, SWE2-DATA: the release path below uses them as the physical neighbour links, phys-prev `+0x0C` and phys-next `+0x10`. They chain blocks by address and have no root.)*
- **The corruption path is a hard stop.** A non-zero `w[+0x3E]` where zero is required routes to
  `0036A570`, calls ~~through the hook cell `q[008C2D80]`~~ the CRT's `exit(1)` through its import slot `008C2D80`, and executes `int3` *(corrected 2026-10-02, OPUS: `008C2D80` is the `api-ms-win-crt-runtime` import `exit`; `00369860+0x214` sets `ecx = 1` and `00369860+0x219` calls it)*. **It does not return
  an error** — a reconstruction that returns `NULL` there is not reproducing this allocator.

*(OPUS 2026-09-19, on `REQ-OPUS-ALLOC-CORE-FINDINGS` from SWE2-ORACLE. Header offsets, both magics, the
carve modes and the 887-byte body size re-derived from the image before adoption — and **one finding
refuted in the process**: the two-list reading of `+0x90`/`+0x98`, which the search arms disprove. The
`_types` deferral is stated above with its reason.)*


## The front door and the kind table — [`EXP-122`](../../_experiments/EXP-122-alloc-dispatch-exec.md), folded in 2026-09-19 (OPUS)

### `022D89BC` is the arena id AND the allocation kind — one dword, one table

This page calls `[022D89BC]` *"the selected arena"*; `EXP-122` calls the same dword *"the
allocation kind"*. **Both are right and it is worth saying so once**, because two names for one
value is how a reconstruction ends up with two fields:

```
0036A113  mov    ecx, dword ptr [022D89BC]    ; -> arg 1 of 0036BC60, the arena
0036C013  movsxd rcx, dword ptr [022D89BC]    ; -> index of the 0xA8 descriptor, the kind
```

**The fifteen `0xA8` records at `022D7FD0` are per-kind arenas.** The same record carries the
allocator state this page documents (`+0x20` bitmap, `+0x28` page table, `+0x60` sequence,
`+0x68` tag counters, `+0x90`/`+0x98` free-list ends) **and** the creation fields `EXP-122` found:
~~`+0x50` pool pointer~~ `+0x50` the root of the block-header tree, `+0xA0` per-kind constructor, live marks at `+0x02`/`+0x62` *(corrected 2026-10-02, OPUS: `0036B410+0x47` stores the first node at `+0x50` when the tree is empty and `0036AAD0+0x40` starts a size-keyed descent there, children at `+0x24` and `+0x28`)*. One record, two
jobs — selecting a heap and selecting a constructor are the same choice.

### An out-of-range kind is a null-page dereference, not an error

```
0036C01A  cmp  ecx, 0xe
0036C01D  ja   0036C02B
0036C01F  imul rdx, rcx, 0xa8
0036C026  add  rdx, r14                   ; + table base
0036C029  jmp  0036C02D
0036C02B  xor  edx, edx                   ; OUT OF RANGE -> descriptor = 0
0036C02D  mov  rax, qword ptr [rdx + 0xa0]  ; ... and then dereference [0xA0]
```

**The bound is checked and the failure path is worse than no check**: it substitutes a null
descriptor and immediately reads through it. There is no error return. This is the same idiom as
the render pool's `arg == -1` path, which substitutes `rcx = 0` and dereferences `[rcx+0x400]`
(`EXP-109`) — **twice now, a bound in this codebase selects a null base rather than refusing.**
A reconstruction must not "improve" it into an error return without saying so.

### The front door's header fill

`0036A100` is `0036BC60`, then `0036BFE0` on failure, then three header writes:

```
0036A124  xor   esi, esi                       ; before BOTH arms
0036A156  movzx eax, byte ptr [022D8E18]
0036A15F  mov   byte ptr [rbx - 0x3e], al      ; the mark byte, from the global 022D8E18
0036A15D  xor   ecx, ecx
0036A162  call  0020E620                       ; encode(0) = -low32(arena)
0036A167  mov   dword ptr [rbx - 0x10], eax
0036A16D  mov   word ptr [rbx - 2], si         ; ALWAYS 0 - esi is cleared at 0036A124
```

`w[obj-2]` is a **constant clear**, not a value: `esi` is `xor`-cleared before either allocator is
called and never reloaded. And `d[obj-0x10]` is `BASE`-encoded *zero*, which is `−low32(arena)` —
a link field pre-set to "points at the arena origin" rather than to null.

> *`EXP-122` describes the mark byte as coming from the staged tag. It comes from a different
> global, `022D8E18` — a neighbour of the `022D8E1C` ~~failure code that `0036BC60` returns~~ byte that `0036BC60` stores as the block's counter index when no free-list record supplies `+0x16` *(corrected 2026-10-02, OPUS: the four reads below load it into the local that `0036BC60+0xF7` otherwise fills from `byte [r8+0x16]`; nothing returns it)*
> (`0036BD19`, `0036BD21`, `0036BD44`, `0036BD4F`). Named by address here rather than by relation.*

### The retry is livelock-shaped

`0036BFE0` re-reads the staged kind on every pass and re-invokes the constructor; it leaves only on
a successful allocation or on "no work reported". **With a static kind and a failing allocator it
spins forever** — the same `jmp $` convention this page already records for `0036BC60`'s
unselected-arena spin. It is a bound to model, not a poll to imitate. The enable mask `022D89B8` is
`bt`-tested twice on the way in (`0036BFF8`, `0036C04F`), and the two failures differ: the entry
test hard-stops, the pool-gate test merely skips the check.

*(OPUS 2026-09-19, on `REQ-OPUS-ALLOC-DISPATCH-FINDINGS` from SWE2-ORACLE. The request routed this
to `CONTRACT-render-record-pool-lifecycle`; it is the allocator front door and belongs here, beside
`EXP-123`. Every quoted sequence re-read from the image.)*


## The selection queue itself — [`EXP-121`](../../_experiments/EXP-121-exp109-queue-tails-exec.md), folded in 2026-09-19 (OPUS)

This page already records the **push / allocate / pop** pattern and counts it — *"109 functions push
through `0036C1D0` and every one of them also pops through `0036C140`"*. `EXP-121` executed both
ends, and **the pop is what produces the staged dword the allocator reads.**

### The pop writes `022D89BC` — the loop closes

```
0036C140  mov   eax, dword ptr [022D89C0]    ; the per-lane COUNT array
0036C146  test  eax, eax
0036C148  jg    0036C152
0036C150  jmp   0036C150                     ; EMPTY -> hard spin
0036C152  dec   eax
0036C154  lea   rdx, [022D89D0]              ; the lane ENTRY blocks
0036C161  mov   dword ptr [022D89C0], eax    ; commit the new count
0036C167  movzx eax, word ptr [rdx + rcx*8]  ; the popped entry's first word
0036C16B  mov   dword ptr [022D89BC], eax    ; -> THE STAGED ARENA/KIND
```

**`022D89BC` — the dword the front-door section above shows being read as both the arena id and the
allocation kind — is written here, by the ~~pop~~ push, and restored by the pop.** *(corrected 2026-10-02, OPUS: `0036C1F0+0x8F` and `0036C140+0x2B`, below)* So the full path is: a caller pushes a selection
onto a lane, ~~the pop stages it into `022D89BC`~~ the push installs `map[id]` into `022D89BC` *(corrected 2026-10-02, OPUS: `0036C1F0+0x8F` stores the mapped id into `022D89BC`; the pop `0036C140+0x2B` writes back the saved previous one)*, and `0036A100`/`0036BC60`/`0036BFE0` read it as the
arena to allocate from and the kind to construct. The three sections on this page are one
mechanism.

### The queue is one region, sliced by count

**A dword count array at `022D89C0`** (4 bytes per lane) and **32-entry lane blocks at `022D89D0`**
(16 bytes per entry — `rcx = eax*2` then `[rdx + rcx*8]`). The pop takes lane 0's top; the push
targets any lane using that lane's own count.

### Both ends hard-spin

`jmp $` at `0036C150` (pop from empty) and `0036C211` (push to full). **Neither re-reads the count**
— they are not polls and there is no other thread to satisfy them. **The caller must guarantee
space**, exactly as `0036BC60` requires a selected arena, and this page's `jmp $` convention covers
all three.

**The push stages its own arguments** into the same dwords the pop fills, so `0036C1D0`'s
caller-stack `r9` becomes the *next* staged qword — a pipeline register rather than a parameter.

### Two corrections from the same pass

- **The 2D table base is `02EC3EE0`.** `002DF960` decodes it unambiguously as
  `lea rax, [rip + 0x2be456c]`, and the first static read had `02EB3EE0` — **off by exactly
  `0x100000`**. *That figure never reached a published page; it is corrected here so it cannot.*
  The leaf is a `0x1388`-row 2D dword table.
- **`0032E400`'s rounding is fallback-only.** The primary pointer-table path returns the raw dword
  and **`ret`s at `0032E430`, before the rounding block**. A model that rounds on both paths
  diverges on five of `EXP-121`'s functional cases — which is how it was caught.
- **`00512EF0` returns an ADDRESS**, `CLRT+0x200`, the residue of its pointer-walk `lea` — not a
  status code. A caller testing it for zero is testing a pointer.

*(OPUS 2026-09-19, on `REQ-OPUS-EXP109-QUEUE-TAILS-FINDINGS` from SWE2-ORACLE. The pop sequence and
the 2D base re-read from the image; the `022D89BC` join to the front-door section is new here.)*

## 9. Related

- [`../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`](../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md)
  — the same `0016D6A0`, read from the bodies rather than from the load config, and the fixed
  image base that makes every address here usable directly.
- [`../Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md`](../Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md)
  — the deleting-destructor idiom that calls `00584730`, and the `ContainerAllocator` population.
- [`../Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`](../Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md)
  — ~~open~~ question **B-2/a** (closed 2026-09-07 in the negative), which §4 of this document ~~partially answers~~ argues.
- [`../Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md`](../Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md)
  — the same forwarder mechanism, counted for internal calls rather than for imports.
- [`../Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md`](../Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md)
  — the other lazily-created global of this kind, and what happens when one is interrupted.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

The import claims were checked by **parsing the PE import directory itself**, not by disassembly —
independent of `functions.tsv` and of any call-graph, which is what a claim about *what the image
imports* deserves.

| claim | measured |
|---|---|
| **538** import symbols | **538**, across 30 DLLs |
| **eight** heap imports from `api-ms-win-crt-heap-l1-1-0`, slots contiguous `008C2B40`–`008C2B78` | **8** — `malloc`, `free`, `_msize`, `realloc`, `_aligned_malloc`, `calloc`, `_aligned_free`, `_set_new_mode` — at `008C2B40`…`008C2B78`, **contiguous at 8 bytes** |
| **no** `VirtualAlloc` / `HeapAlloc` / `HeapCreate` / `MapViewOfFile` | **none**, over all 538. Every imported symbol containing "alloc" is: `GlobalAlloc`, `LocalAlloc`, the CRT eight, and two C++ `std` symbols |
| `00584730` has **2,309** distinct callers | **2,309** |
| the memory-log record `01F82E48` — **three hits** | **three sites**, in `001EDF10`, `001EDF80`, `001EDFE0` |

### The 2,309 needed a tail jump, and the three hits needed sites

**Counting only `call` gives 2,308.** The 2,309th reaches `00584730` by a **tail `jmp`** — from
`0069ECD0`. A caller census that ignores tail jumps loses exactly one here, and the page's figure is
the one that counts it. *A tail jump is a call in every sense a caller census cares about.*

**Counting instructions at `01F82E48` gives six.** They are **three `cmp qword [rip], 0` and three
`mov qword [rip], rax`**, one pair per function — so three *sites*, as the page says. And the
distinction matters for the claim itself: the three `cmp`s are **the writers testing their own slot
before filling it**, not consumers reading the value. **The record `01F82E48` has no reader outside its own
writers**, which is precisely what "no reader" asserts.

*(A detector that treats a memory first-operand as a store calls all six writes; `cmp` is not a
write.)*

**Not claimed:** `_set_new_mode` is **imported** — it is the eighth heap slot — and this pass confirms
only that. The separate claim that it is *never called* is about call sites and was not re-run here. *(Checked 2026-09-30, SWE2-DATA: the claim was wrong, see "Failure is not handled" and `pf_mem_checks.py` M1d.)*

## `0036A2A0` read — it is not an allocator, and `022D8E10` is an array (OPUS, 2026-09-14)

This page says: *"The other direct callers of `0036BC60` stamp nothing at that offset: `0036A2A0`,
`0036CB00`, and the retry allocator `0036BFE0` … Whether `0036A2A0` and `0036CB00` produce blocks
that carry this header is **not traced**."* That sentence is the whole of `AC-5`'s evidence for
`0036A2A0` being unclassifiable, and it was the last CONTESTED body in the residual census — classified at GN162 as `Runtime.MemoryAllocator.RecordClone`, so the census is closed and the sentence above is what `AC-5` rested on, not what is true now.

**Read from the shipping executable at the authority hash `73461D08…9721F8`, image base `0x120000`;
every address below is decoded from the bytes.** All 495 bytes of `0036A2A0`, and the comparison
sites in `0036A100`, `00369860` and `0036C5D0`.

### Historical header-clone interpretation; source movement clarified by SECTION-07

`0036A100` obtains one — `0036BC60(arena, size, 0, 0)` and the result is `rax`:

```
0036A113  mov   ecx, dword [022D89BC]     ; the active arena
0036A11F  call  0036BC60                  ; -> rax = block
0036A156  movzx eax, byte [022D8E18]      ; the current category
0036A15F  mov   byte [rbx - 0x3e], al     ; stamped into the block header
```

`0036A2A0` passes one **in**, and throws the return value away:

```
0036A3AC  movzx ecx, byte [r12 + 1]       ; arena, from its context argument
0036A3B5  mov   r8, rbx                   ; <- the DESTINATION RECORD, third argument
0036A3B8  mov   edx, r13d                 ; size, taken from the SOURCE record's +0x18
0036A3BB  call  0036BC60
0036A3C0  movzx eax, byte [rsp + 0x34]    ; rax overwritten at once - the result is unused
```

**`r8` is `0` in the stamping wrappers and a record pointer here.** So `0036A2A0` is a **record
clone**: it copies `+0x02`, `+0x03`, `+0x14`–`+0x17`, `+0x1E`, `+0x30` and a NUL-terminated string at
`+0x34` from source to destination, re-encodes the image pointer at `+0x20` through `0020E600` /
`0020E620`, zeroes `word [dest + 0x3E]` twice, and calls `0036BC60` for its effect on the record it
was given. **SECTION-07 correction:** these are metadata transfers inside actual allocated-payload relocation,
not a detached clone with no block. The same original function updates the stable slot, releases the
old source at `0036A397`, copies its payload at `0036A3A7`, and allocates the chosen destination
header at `0036A3BB`. The return of that last call is unused because the destination is already
known. Historical metadata/count observations remain scoped; the current mechanism is below.

### And the same body shows `022D8E10` is an indexed array

```
0036A37D  movzx eax, byte  [rbp + 0x17]   ; a CATEGORY byte on the record
0036A381  lea   rcx, [022D8E10]
0036A388  lea   rcx, [rcx + rax*4]
0036A38E  mov   eax, dword [rbp + 0x18]   ; the record's size
0036A391  add   dword [rcx], eax
```

Three independent sites agree, and none of them is this one:

| site | what it does |
|---|---|
| `00369B1B`–`00369B34` | `byte [rbx+0x17]`, **skips when it is 0**, then `sub dword [022D8E10 + i*4], [rbx+0x18]` |
| `0036A381`–`0036A391` | `add dword [022D8E10 + i*4], [rbp+0x18]` |
| `0036C5F9`–`0036C610` | reads the old category, and **moves the amount**: `sub [022D8E10 + old*4]`, `add [022D8E10 + new*4]` |

**`022D8E10` is a per-category dword accounting array, stride 4, amount `[rec+0x18]`, index
`[rec+0x17]`, with index 0 meaning "not accounted".** This page models `022D8E10`–`022D8E2F` as
separate named scalars and does not mention an array anywhere.

### RULING — `022D8E10`..`022D8F10` is THREE objects, not one (FABLE, 2026-09-22)

Asked on `OPUS-REQ-FABLE-WHAT-IS-THE-022D8E10-BLOCK`: the writable-state sweep found 33 cells, 49
bodies, 54 writes and 102 reads in the `0x100` bytes below the EE/VU0 register bank, looking
heterogeneous, and OPUS would not name fields on a guess. **It is heterogeneous because it is three
objects with disjoint writers, disjoint entry points and disjoint lifetimes.**

| region | what it is | who writes it |
|---|---|---|
| `+0x00`..`+0x20` | **the per-category allocation accounting array** — *already named on this page* | the allocator sites `00369B1B`, `0036A381`, `0036C5F9` |
| `+0x20`..`+0x34` | three cells zeroed once, at boot | `0036D260`, whose only caller is `0022A0B0` |
| `+0x40`..`+0xD0` | **one display-geometry object**, initialised as a unit | `0036D280`, which tail-calls `0036D2F0` |

**Region 1 needs no new work and the request's description of it is the superseded model.** The
request calls `+0x00`..`+0x20` *"a `0xFF` constant and a pointer"*; the subsection above this one
establishes it is an **~~8-element~~ dword array at stride 4 *(corrected 2026-10-02, OPUS: `00369D30+0x7D` writes `0xFF` into `022D8E18`, a different field, so the array cannot run to eight; the closure below finds two elements on every identified path)*, indexed by `[rec+0x17]` and amounted by
`[rec+0x18]`** — OPUS's own finding of 2026-09-14, on three independent sites, and its closing
sentence is that this page *"models `022D8E10`–`022D8E2F` as separate named scalars and does not
mention an array anywhere"*. **That is exactly the shape a fresh displacement sweep re-discovers as
unrelated scalars.**

**Region 3 is one object because one routine initialises all of it and the second half has no other
caller.** `0036D280` writes `+0x98` = 0, `+0x9C` = `0x200`, `+0xA0` = `0x200`, `+0xA4` = `0x1C0`,
`+0xCC` = 1, `+0xD0` = 1, and then **tail-jumps to `0036D2F0`** (`0036D2E6`), which is the `movaps`
staging writer for `+0x40`..`+0x98`. `0036D2F0` has **exactly one caller**, that tail-jump. *So the
SSE staging area and the scalar group are not two findings that happen to be adjacent; they are one
initialisation, and a type row should cover both or neither.*

#### The `+0x98` group, measured — and the two `0x200`s are NOT the same kind of field (FABLE, 2026-09-22)

The fields hold what the hint suspected, and now by measurement rather than by coincidence:
`+0x9C` = **512**, `+0xA0` = **512**, `+0xA4` = **448**, written as literals by the one initialiser.
**A read census separates them, which is the part a write census could not do:**

| field | value at init | reads | bodies |
|---|---:|---:|---:|
| `+0x9C` | 512 | 26 | **17** |
| `+0xA4` | 448 | 25 | **15** |
| `+0xA0` | 512 | **1** | **1** |
| `+0x98` | 0 | 4 | 4 |

**`+0x9C` and `+0xA4` are a live pair — 512 by 448, consumed together across fifteen-odd bodies.
`+0xA0` is not part of that pair at all**: its single reader is `0036D2F0`, the very routine the
initialiser tail-calls, so it is a **one-shot parameter handed from the init to the staging step and
never consulted again.** *Two cells holding the same number are not the same kind of field, and the
reader census is what shows it.*

**And the PS2/GS reading now has a measurement under it, not just the 512×448 coincidence.**
`00244200` — the group's heaviest consumer, itself called from exactly one place — computes
`[+0x9C] >> 6`, which is `512 / 64 = 8`, **the GS `FBW` encoding, where buffer width is carried in
units of 64 pixels**; it packs that value twice into a 64-bit word beside the constant `0x333C`, and
multiplies `[+0x98] × [+0xA4] × [+0x9C]` before shifting right by 6 as well. It then calls
`0039D0C0`, a `Presentation` body **also called by `EffectCapture_ProcessCaptureDraw`**. *A `>> 6` on
a width, a 512×448 pair and a draw-path consumer are three independent things all pointing the same
way.* *(Anchored 2026-09-30, SWE2-DATA: `00244224`–`0024427B` and its one caller, `pf_mem_checks.py` M2, M3.)*

> **What is ruled, and what is not.** Ruled: three objects; region 3 is one unit; `+0x9C`/`+0xA4` are
> a width/height pair and `+0xA0` is an init parameter; the `>> 6` is a divide-by-64 on a width.
> **Not ruled: which GS register, if any, each field corresponds to.** `+0x9C` and `+0xA0` both hold
> 512 at init and nothing read here distinguishes a frame-buffer width from a display width by
> meaning — only by consumption. **The literals `0x1C0` and `0x200` that `00244200` passes to
> `0039D0C0` are its OWN immediates and are not read from this block**, so they corroborate the
> geometry and are not evidence about these cells. Naming the registers needs the `0039D0C0` side,
> which is `Presentation`'s and is not read here (`SD-169`, SWE2-DATA, 2026-09-30).

### What that collides with, stated as the open question it is

Element **2** of that array is `022D8E18` — the current-category byte the three wrappers stamp into
block headers. Element 3 is `022D8E1C`, the fallback byte; elements 4–5 are the tag `022D8E20`.
**Nothing at any of the three accounting sites bounds the index.**

So exactly one of these is true, and the bytes above do not settle which:

1. the category value is always 0 or 1, the array is the two dword halves of the qword the
   initializer writes at `022D8E10` (`00369DC5`), and the named scalars are untouched; or
2. a category of 2 or more exists, and the accounting array writes through three named scalars.

**One thing sharpens it and is not a proof.** The initializer sets the current category to `0xFF`
— `00369DAD  mov dword [022D8E18], 0xFF` — and a block allocated while that stands is stamped
`0xFF`, which as an index reaches `022D920C`, far outside anything this page names. Whether
`0036BC60` can return a block before a category is pushed is **not read here**, and without that the
`0xFF` path is a shape, not a finding.

Raised as `OPUS-CONTRA-ARENA-ACCOUNTING-ARRAY` rather than written into the page's model, because a
region this page describes as five scalars and three other functions treat as an array is a
disagreement about a **type**, and the reading above establishes the array, not the bound.

*(Read by OPUS 2026-09-14 from the shipping bytes. This supersedes the "not traced" sentence for
`0036A2A0` only: it is a record clone, and `AC-5`'s CONTESTED verdict on it falls with the premise.
`0036CB00` is untouched by this and remains unread.)*

### Narrowing the array question, and the measurement that did NOT settle it (OPUS, 2026-09-14)

The section above left one question: can the accounting index reach 2? The obvious way to answer it
is to bound the **category**, so every caller of the selection push was disassembled and the literal
it passes in `edx` taken — 136 call sites into `0036C1D0` / `0036C1F0`, 121 of them with a literal in
the preceding twelve instructions.

| category literal | sites | | category literal | sites |
|---:|---:|---|---:|---:|
| 3 | 1 | | 10 | **48** |
| 4 | 1 | | 11 | 2 |
| **5** | **46** | | 12 | 6 |
| 6 | 10 | | 15 | 1 |
| 8 | 1 | | 16 | 1 |
| 9 | 3 | | 18 | 1 |

**No site passes 0, 1 or 2.** The fifteen remaining sites compute their category rather than writing
a literal and are listed in the tool output; they are not assumed either way.

**That bounds the current-category byte and it does NOT bound the array index**, and the difference
matters enough to state rather than elide. If `[rec+0x17]` were the category, indices 3–18 would put
the array at `022D8E1C`–`022D8E5B`, straight through `022D8E1C`, `022D8E20` and `022D8E28`. Two things
say it is not:

- **`00369B1F  test al, al` / `je`** — the accounting **skips index 0**, so 0 is in that byte's range.
  It is not in the category's: the pushes start at 3 and the initializer's value is `0xFF`.
- **The initializer writes a STRUCT, not an array.** `00369D30` covers exactly `022D8E10`–`022D8E2B`
  with mixed widths — `qword [022D8E10]`, `dword [022D8E18] = 0xFF`, `dword [022D8E1C]`,
  `qword [022D8E20]`, `dword [022D8E28]`. A nineteen-element dword array would be cleared uniformly,
  and this is not that.

So `[rec+0x17]` is **a different field from the allocator's category**, on records the accounting
sites reach differently — `0036C5D0` gets its record through `mov rdx, qword [rdx + 8]` off a masked
pointer, not from a block header. **`OPUS-CONTRA-ARENA-ACCOUNTING-ARRAY` stands, narrowed to one
question: what is `[rec+0x17]`'s range?** The category measurement above does not answer it, and
saying so is the point of recording it here rather than quietly dropping a measurement that pointed
the wrong way.

*(Measured by OPUS 2026-09-14 from the shipping bytes. The category range 3–18 is a finding in its
own right — the block-header stamp at `block - 0x3E` carries those values, plus `0xFF` before any
push — and is the first time that byte's range has been bounded.)*

### `OPUS-CONTRA-ARENA-ACCOUNTING-ARRAY` closed — the array is two elements, and the page was right (OPUS, 2026-09-14)

The narrowing above left one question: what is `[rec+0x17]`'s range? `0036C5D0` answers it directly,
because that function **takes the new index as an argument** and compares it against the record's
current one (`0036C5FD  cmp eax, r8d`). So the callers give the range.

| callee | call sites | literal `edx` | computed |
|---|---:|---|---:|
| `0036C5D0` | 5 | **1** at two sites | 3 |
| `0036C620` | 2 | **1** at one site | 1 |
| `00369860` | 7 | **0** at all seven | 0 |

**Every literal is 0 or 1.** And the four computed sites forward a caller's parameter rather than
deriving a wide value — `FUN_003AB910` is the clearest: `test cl, 3` / `setne r8b` / `cmp r8d, 1`,
then `jmp 0036C5D0` when it is 1 and `jmp 0036C620` when it is not. ~~**A boolean dispatch.**~~ The boolean only picks the helper; the index rides in `edx` unchanged *(qualified 2026-10-02, OPUS - see the qualification below)*.

### So the accounting "array" is the two dword halves of the qword at `022D8E10`

Index 0 is skipped at `00369B1F` (`test al, al` / `je`), index 1 writes `022D8E14`, and the
initializer's `qword [022D8E10] = 0` at `00369DC5` zeroes both at once — which is exactly why the
initializer writes a qword there and dwords elsewhere. **`022D8E18` is element 2 and is never
reached.** ~~The current-category byte is safe, `022D8E1C`, `022D8E20` and `022D8E28` are safe, and
**this page's scalar model stands.**~~ That holds for the literal call sites *(qualified 2026-10-02, OPUS - see the qualification below)*.

The category pushed onto the selection stack (3–18, measured above) and `[rec+0x17]` (0 or 1) are
**different value spaces**, which is what the narrowing suspected and could not yet show.

*(Closed by OPUS 2026-09-14 from the shipping bytes. I raised this contradiction, measured it three
ways, and it resolved in favour of the document I raised it against. The residual uncertainty is the
four forwarding sites: each passes a caller's parameter, and none of their callers was read. That is
a smaller claim than the one this section started with, and it is stated rather than closed over.)*

### The closure qualified: the forwarding path carries a nibble, not a boolean (OPUS, 2026-10-02)

*On ASTRA's accounting-dispatch-index (`_experiments/evidence/accounting-dispatch-index/`), re-read at the bytes
(control: `_index/candidates/opus-accounting-qualify-1002/accounting_check.py`).* The closure above called `003AB910` a
boolean dispatch. It is not.
- The boolean in `r8` (`test cl, 3` / `setne r8b`) only picks the helper for the storage representation: `0036C5D0`
  or `0036C620`.
- The new index rides in `edx`, which `003AB910` never writes.
- `0036C5D0` replaces `r8` at once (`movsxd r8, edx`, `0036C5D0`), and `0036C620` sign-extends `edx` the same way.
  Both debit `022D8E10 + old * 4`, credit `022D8E10 + new * 4`, and store the low byte at `+0x17`, with no 0/1
  bound.

`003AB910` has one caller: the instance factory `0041F340`. It forwards CharacterRenderRecord `+0x0C1`, read with
`movsx` (`0041F515`, `0041F525`). Both known writers of `+0x0C1`, `002E28E0` and `002E3110`, store a source byte's
upper nibble (`shr edx, 4`), so on those paths the index is 0..15. It is 0 or 1 exactly when the source byte is below
`0x20`.

**So the closure holds for the literal call sites, and is open for this one path.** If a source byte at or above
`0x20` reaches the factory, the credit lands at `022D8E18` or beyond, on the struct fields the initializer writes.
*(That remaining question is registered as a runtime residue — `NR-1` in
[`_index/OPEN-QUESTIONS.md`](../../_index/OPEN-QUESTIONS.md), 2026-10-02.)*
~~Whether the shipped game ever supplies such a byte, and whether other writers of `+0x0C1` exist, is not established
statically.~~ No other writer of `+0x0C1` with a proven render-record receiver exists: an image-wide sweep of stores of every width
that cover the byte finds only the two known writers, and the defaults reset zeroes it. The source byte's upper nibble has one setter, and all 27 of its call sites pass 0 or 1, so the index is 0 or 1 on every identified path *(answered 2026-10-02, FABLE, static; addresses and controls in [`mempage-residue-fable-1002`](../../_index/candidates/mempage-residue-fable-1002/README.md) item 3)*. ~~Still open, static: the object type behind the `+0xC0` pointer in twelve bodies whose wider stores land on these offsets (no receiver is proven).~~ None of those twelve bodies reaches an actor record: in ten the `+0xC0` belongs to a UI widget (a child or owner widget, a manager slot, an image-registration entry or a private buffer), in one to an audio submix voice (a per-channel buffer), and in one the "pointer" is a stack argument of an audio filter method, so none can change the source byte and the index stays 0 or 1 *(answered 2026-10-02, FABLE, static; [record](../../_index/candidates/c0-receiver-fable-1002/README.md))*. The stored fields' own record is the type store's CharacterRenderRecord `+0x0C1` row (`b83439b6c`).

## The `0036CB00` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`0036CB00` (1,353 B) is a free-block realloc path on the `022D89xx` heap
state: `byte[rdx+3]` → `r12d` → `022D89BC` (`0036CB30`–`0036CB57`),
`word[rdx]` and `word[rdx+0x3E]` checks (`0036CB4E`/`0036CB76`),
`0036A570` ×2 with indirect `call qword[008C2D80]` (`0036CB6F`/
`0036CB99`), the `"ReallocIlligalAddress(free block):%p from %p"` assert
through `0017D2E0` (`0036CBA6`–`0036CBB2`), `dword[rdx+0x18]` vs `esi`
(`0036CBBE`), `0020E600` (`0036CBD6`), then members `0036C380` /
`0036C290` (`0036CBFC`/`0036CC0C`) on the way to `0036D02C` /
`0036D024`.

| member | role | interior |
| --- | --- | --- |
| `0036A240` (63 B) | block-link + id copy — `[rcx+8] = rdx` (`0036A25A`), `0020E620` → `dword[rbx+0x20]` (`0036A25E`–`0036A263`), `word[rbx+0x1C]` → `word[rdi+6]` and `word[rbx+0x3E]` (`0036A266`–`0036A270`)~~, byte store at `022D89A8` (`0036A282`–`0036A290`)~~ *(corrected 2026-10-02, OPUS: the body ends at `0036A240+0x3E`; the `022D89A8` store loop is `0036A280`, the identity-map fill)* | [`0036A266`](../../_index/ADDRESS-INDEX.md) |
| `0036C290` (228 B) | block metadata fill — `word[rcx+0x60]`, `byte[rcx+1]`, `dword[rdx+0x18]` (`0036C2A4`–`0036C2BA`), `0036A490` (`0036C2CB`), `word[rsi+0x3E] = ax` (`0036C2D7`), `[rdi+0x18] = ebp` (`0036C2DE`) | [`0036C2D7`](../../_index/ADDRESS-INDEX.md) |
| `0036C380` (289 B) | three-field resolve — `byte[rcx+1]` (`0036C3A1`), `dword[r8+4]` / `[r8+8]` / `[r8+0x18]` each through `0020E600` (`0036C3B2`–`0036C3C3`) | [`0036C3B7`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0036A570`, `0017D2E0`, `0020E600`,
`0020E620`, `0036A490`. The `ReallocIlligalAddress` assert fires on a
free-block address reaching realloc — the heap's own guard, kept verbatim
(misspelling and all) because the string is diagnostic evidence.

## Interior citations — three allocation hubs (2026-09-17, SWE2-EC7)

- **`0017D260`** — §3's `allocate(n, align)`, already quoted above. Interior verified:
  [`0017D264`](../../_index/ADDRESS-INDEX.md) is `xor r8d, r8d` — the offset arg forced to 0 between
  `or r9d, -1` (flags) and the tail `jmp 0019C580` (`_aligned_malloc` IAT thunk, import
  `008C2B60`). 12 B, 88 frontier callers at census.
- **`00210EC0`** — the `malloc` spelling of the same forwarder: `or r8d, -1; xor edx, edx;
  jmp 0085E730`, where `0085E730` is the `malloc` IAT thunk (`008C2B40`). Interior verified at
  [`00210EC4`](../../_index/ADDRESS-INDEX.md) — `xor edx, edx`. The extra registers are dead under
  the two-arg CRT signature; the body is `malloc(n)` with no alignment promise, consistent with
  §"the imports": no `operator new` is imported, so `new`-sized callers come here. 11 B, 81
  frontier callers.
- **`001EDF00`** — the `eastl::allocator_memory_log` ctor, already named in §5's table. Interior
  verified: [`001EDF07`](../../_index/ADDRESS-INDEX.md) is `mov qword ptr [rcx], rax` — the vtable
  `00902720` store; the full 14 B is install-vtable, `mov rax, rcx`, `ret`. 104 frontier callers.

~~NOT claimed: `00210EC0`'s caller-visible contract beyond `malloc(n)` — whether a caller relies on
the dead-arg form is not established.~~ `00210EC0`'s contract is `malloc(n)`: none of its 258 raw sites in 181 functions, nor its one table install, prepares or reads the second argument *(answered 2026-10-02, FABLE, static; addresses and controls in [`mempage-residue-fable-1002`](../../_index/candidates/mempage-residue-fable-1002/README.md) item 4)*.

## Interior citation — frontier hub `0036C750` (2026-09-18, SWE2-EC7)

`0036C750` — 57 B, 7 A-measured callers; the basename helper. Interior verified: an inline
`strlen` (`0036C757`–`0036C763`), then a backward scan from the terminator for `0x5C` or
`0x2F` at [`0036C773`](../../_index/ADDRESS-INDEX.md)–`0036C77B`, returning the first byte after the separator —
or the string start when none exists. Both separator conventions accepted; no allocation, no
copy.


## Interior citation — frontier hubs `0019C580`, `00584740` (2026-09-18, SWE2-EC7)

`0019C580` — 9 B, 10 callers; the `_aligned_malloc` import thunk this page's asm quote
already names. Interior verified: `mov edx, edx` (the 64-bit arg widen) then
`jmp qword [008C2B60]` at [`0019C582`](../../_index/ADDRESS-INDEX.md) — an IAT slot, so the
"every allocation route goes to `_aligned_malloc`" claim holds literally: this is the only
code between callers and the import.

`00584740` — 16 B, 29 callers; the `allocate(n) → align 16` adapter the `001A11B0`
boot-alloc exception uses. Interior verified: `edx` is forced to `0x10`
(`or r9d,-1; xor r8d,r8d; lea edx,[r9+0x11]` = `0x10` at
[`00584740`–`00584747`](../../_index/ADDRESS-INDEX.md)) and the tail is `jmp 0019C580` at
[`0058474B`](../../_index/ADDRESS-INDEX.md) — a 16-byte-aligned `malloc` shim.


### Interior citation — frontier hub `0036A570` (2026-09-18, SWE2-EC7)

`0036A570` — 729 B, 8 callers: the heap-usage line formatter. `bt` tests bit
`ecx` of `022D89B8` at [`0036A597`](../../_index/ADDRESS-INDEX.md) to decide
whether the arena is live; `ecx <= 0xE` indexes the 0xA8-stride `022D7FD0`
arena table. It then selects among `"M2/U"`, `"M /U"`, `"M2/l"`, `"M2/L"`,
`"M /l"`, `"M /L"` and `"FREE"` format strings by occupancy, runs the
`0020E600` stride-picker five times for the size fields, and emits through
`0036A850` + `00808C40` (vsnprintf-family). The debug overlay's per-arena
status row.
## SWE2-EC7-40 update (2026-09-19) - `0036A850`

`0036A850` (367 B) is a memory-family body - `01F44830`, `"FREE"`/`"M /L"`/`"M /U"`/`"M /l"`/`"M2/L"`/`"M2/U"`/`"M2/l"` strings, `0020E600` quadruple plus a self-call and `00808C40`. Interior anchor `0036A953` (an `0020E600` call).

## SWE2-EC7-42 update (2026-09-19) - `00792F10`

`00792F10` (306 B) is the memory-status reader the page names - `008C2118`/`008C21B8`/`008C2220`/`008C2270` imports, `005CC8A0`/`007A3810`/`005CD0A0`/`00808C40`. Interior anchor `00792F68` (a `005CC8A0` call).

## SWE2-EC7-43 update (2026-09-19) - `0036AE00`

`0036AE00` (287 B) is an allocator body - `0020E600`/`00861EC0` pair pattern. Interior anchor `0036AE24` (a `0020E600` call).

## SWE2-EC7-44 update (2026-09-19) - `0036A9C0`

`0036A9C0` (260 B) is a body - `0036C790` single call. Interior anchor `0036AA9B` (the `0036C790` call).


## SWE2-EC7-66 update (2026-09-19) - `00369C60`

`00369C60` (133 B) is the `00369C60(6, 1)` arena-descriptor body - `0036AAD0`/`0036ABE0` plus `022D7FD0`/`022D89B8`. Interior anchor `00369CAE` (a `0036AAD0` call).


## SWE2-EC7-71 update (2026-09-19) - `00369800` tagged-source release measured

Measured on `authored-reference-lifetime-evidence.md` (PARTIAL -
non-bearing); mirrored here where the page already describes the arm.

`00369800` (85 B) measured - the page's tagged-source arm is exact:
`ecx` must carry a low tag bit (`cl & 3`) and a value `>= 0x100000`; it
aligns `ecx & ~3`, reads the owner at `[src+8]` first, runs
`0036A9C0(src)`, and when the owner is non-NULL tails
`00369860(owner + 0x40, 0)` - the release the untagged sibling
`003697F0` pairs with.
Interior anchor `00369828` (the `0036A9C0` call).


## The release path — [`EXP-126`](../../_experiments/EXP-126-alloc-free-path-exec.md), folded in 2026-09-20 (OPUS)

`00369860(payload, aux)` is the allocator's free/release path. §2 above
already describes it as "gated three ways"; EXP-126 executed it, and the
gates are **six**, ordered, and three of them are diagnostics that
**return normally** rather than aborts. That distinction is the contract:
a caller cannot tell a refused free from a completed one by the return
value, because both return.

### The gate/abort taxonomy (OPUS)

The header is `payload - 0x40` (`003698C1 lea rbx,[rcx - 0x40]`), so
every offset below is a field of `ImageAddressArenaBlockHeader`.

| order | gate | on failure | reaches the reclaim? |
|---|---|---|---|
| 1 | `rcx == 0` | returns 0 | no |
| 2 | `rcx & 3` | emits `"%p might be MHANDLE from %p"`, **returns** | no |
| 3 | `w[hdr+0x00] != 0xFF12` (`magic`) | bad-magic abort: dumps `0xB0` header bytes then `0xD0` aux bytes, emits `CannotFreeIlligalAdrs`, `A570(kind,0xB,-1)`, hook, `int3` | no |
| 4 | `w[hdr+0x3E] != 0` (`guardWord`) | `"MCB Broken"`, same abort tail | no |
| 5 | `!(b[hdr+0x14] & 1)` (`allocFlags`) | emits `"TkFreeMain:Allready Free:%p from %p"` and **returns** | no |
| 6 | `b[hdr+0x03] >= 0xF` (`arenaId`) | `rdi = 0`, then `mov byte ptr [rdi+2],1` **faults at address 2** | no |

Gates 2 and 5 are the ones that matter to a caller: **freeing a free
block is a diagnostic, not a crash**, byte-verified. Gate 6 is not a
check that reports — it is fail-closed by construction, taking the null
record and writing through it, the same trap shape `0036C5A0` uses at
`0036C5BF` for an out-of-range id.

Gate 4 is recorded here because EXP-126 describes the matching clear as
`d[+0x3E] = 0`. It is a **word**: `00369B4F` is `6689733e`,
`mov word ptr [rbx + 0x3e], si`. A dword there would write two bytes past
the `0x40` header into the payload, which would have been an extent
violation on a type whose extent is settled. It is not one.

### Phys-first splice, and the stale-link guard is the contract (OPUS)

Reclaim clears the header (`b[+0x02] = 0xFF`, `b[+0x14] &= ~1`,
`b[+0x17]`, `w[+0x1E]`, `b[+0x34]` zeroed, `d[+0x30] = encode(0)`,
`w[+0x3E] = 0`) and then splices the block back in, **physical
neighbours first**:

1. phys-prev `BASE(d[+0x0C])` free → `B670(pp, rbx)`;
2. else phys-next `BASE(d[+0x10])` free → `B730(pn, rbx)`;
3. else by position against the descriptor bound `q[desc+0x18]`:
   below → `AE00` first with `ACE0` fallback, at-or-above → `ACE0`
   first with `AE00` fallback.

**Every lookup result is then re-checked against the free-list links
`BASE(d[+0x04])` / `BASE(d[+0x08])`, and if the found block already
equals that link no splice runs at all.** This is the part worth
stating as a contract rather than a step: the find-free pair may return
a block that is already the neighbour in the list, and the path is
required to notice. Then `B210` coalesces and `B5F0` updates the
page-head table.

### The counter decrements — and the mirror is not where it looks (OPUS)

The free debits **two different counters**, and they do not have the
same partner on the allocation side.

- **Per-arena.** `lea rcx,[rdi + rax*4]` (`00369B11`) with `rax` =
  `b[hdr+0x16]` `arenaCounterIndex`, then
  `sub dword ptr [rcx + 0x68], eax` (`00369B18`), subtracting
  `d[hdr+0x18]` `payloadLength`. The target is
  `ImageAddressArenaRecord +0x68`, now declared as `arenaCounters`,
  `uint32[9]`. **Its mirroring adds are in the carve `0036BC60`
  (`0036BFAD`) and in `0036D050` (`0036D126`)** — not in `0036A2A0`.
- **Global category.** `lea rcx,[rip->022D8E10]`, `lea rcx,[rcx+rax*4]`,
  `sub dword ptr [rcx], eax` (`00369B34`), with `rax` =
  `b[hdr+0x17]` `categoryCounterIndex` and `test al,al` first, so index
  0 means *absent*. **This** is the table `0036A2A0` bumps, at
  `0036A391`.

So the alloc/free mirror holds on the global category counters and is
carried by the carve, not the adopt, for the per-arena ones.

`arenaCounters` is **nine** elements because the initialiser zero-clears
exactly `0x68..0x8C` at `00369FAD-00369FC0` — four qwords and a dword,
36 bytes, `r8` zeroed at `00369E7B`. Containment against `+0x90`
`freeListHead` would have allowed ten. The measurement is taken; the
ceiling is not. Nothing range-checks `+0x16` against nine.

### What this settled in `_types` (OPUS)

The record side was censusable for the first time here (see the note in
[`COVERAGE-DIMENSIONS`](../../_index/COVERAGE-DIMENSIONS.md)), and the
release path supplied the header side directly:

- `ImageAddressArenaBlockHeader` — `+0x03 arenaId` (the cross-link to
  `ImageAddressArenaRecord`'s own `count=15`), `+0x1E word1E`,
  `+0x30 encodedRef30` (a fifth encoded reference, proven by the
  `0020E620` **encoder** call at `00369B44`, not by its width),
  `+0x34 byte34`. ~~Nine bytes at `+0x35` stay unobserved.~~ `+0x34`–`+0x3A` hold a 7-character name and `+0x3B` its NUL; `+0x3C`–`+0x3D` stay unobserved *(corrected 2026-10-02, OPUS: `0036C660+0x30` calls `strncpy` through `008C2F70` for 7 bytes at header `+0x34`, and `0036C660+0x36` stores the NUL at `+0x3B`)*.
- `ImageAddressArenaRecord` — twelve rows out of four spans, and
  `tailQword00A0`'s citation corrected: it had cited `0036C5C1`, which
  is `0036C5A0`'s out-of-bounds null-write trap and not an access to
  any record.

What none of this establishes is what the cleared fields *mean*. Six of
the new rows say "NOT UNDERSTOOD" in as many words: cleared on free is
where the evidence stops, and a field that is zeroed is not thereby
explained.

## SWE2-EC7-93 update (2026-09-20) - `0036ABE0` + `0036AAD0` measured

`0036ABE0` (243 B) is the first-match ring walk `00369C60` calls:
`[rcx+0x90]` chains nodes whose `[rdi+0x10]` resolves via `0020E600`;
a resolved record passing `+0x15 & 6 == 2` with `+0x14 & 1` clear
makes the `[r14+0x50]` ring walk `+0x24`/`+0x28`-resolved pointers,
comparing `+0x18` against `[rdi+0x18]` and preferring `+0x15` bit-2
members, until `0036A2A0` runs on the winner - returns 1 on apply, 0
on exhaust.
Interior anchor `0036AC10` (the loop-head `0020E600` call).

`0036AAD0` (261 B) is the counted sibling: the same ring walk and
the same `0036A2A0` apply, but every match increments `r15d` and
`r12d` decides whether the outer `+0x90` chain is walked once or to
exhaustion - returns the match count.
Interior anchor `0036AB60` (the `0036A2A0` apply).

## SWE2-EC7-111 update (2026-09-20) - `001A5A80` measured

`001A5A80` (114 B) is the
8-byte-element aligned
deallocate `001A2D10`,
`001A4D20`, `001A5B30` and
the CRT pair `00897140` /
`0089D7A0` run - the
`002099D0` convention:
`r8 * 8 >= 0x1000` sends the
block down the aligned path,
which validates `rdx & 0x1F
== 0`, recovers the raw block
base from `qword[rdx - 8]`,
and bounds the decoration
delta to `8..0x27` before the
`00210EB0` tail frees the
base. Every guard failure
dies on the `008C2DA8` fault
IAT.
Interior anchor `001A5AB6`
(the `[rdx - 8]` block-base
recovery).

`001A1990` (112 B) is the
SSO-aware two-string ordering
probe `001A6F10` and the
`00675xxx`/`00676xxx` callers
run: each side's `qword[+0x18]
>= 0x10` selects inline
buffer vs heap pointer, the
`+0x10` sizes bound a
`00861ED2` memcmp on the
shorter length, a nonzero
answer folds to its sign bit,
and equal prefixes answer the
size comparison - any length
mismatch is nonzero, only
equal sizes answer 0.
Interior anchor `001A19CB`
(the memcmp call).

## SWE2-EC7-112 update (2026-09-20) - `0016D6B0` measured

`0016D6B0` (10 B) is the IAT
thunk `001E1670` and
`008666B0` run: `rcx = rdx`
then `jmp qword[008C2B40]` -
the second argument becomes
the first and control passes
straight to the import. A
two-byte-wrapper's worth of
adapter, nothing more.
Interior anchor `0016D6B3`
(the `008C2B40` tail).

## SWE2-EC7-118 update (2026-09-21) - `0067ADD0` measured

`0067ADD0` (89 B) is the
copy-assign `001C22A0` runs:
the `+0x10` length moves
over, `0067B100` ensures
capacity for `btr([rdx],
31)`, and `00861EBA` copies
the source's `[+8]` bytes
into `[rbx + 8]` when both
exist.
Interior anchor `0067AE0D`
(the `00861EBA` call).

## SWE2-EC7-119 update (2026-09-21) - the UTF-8 hash and the keyed find measured

`00677350` (244 B) is the
UTF-8-aware string hash
`00676450`, `00676BD0` and
`00677BA0` call: lead bytes
0xC0-0xF8 select 1-5
continuation bytes, the
lead's payload comes off a
`6 - len` mask and each
continuation folds six bits
in, then the accumulator
steps `acc*0x21 + (cp &
0x1F)` per codepoint,
seeded by `edx`.
Interior anchor `0067742A`
(the `imul 0x21` fold).

`00674F60` (348 B) is the
ordered-map find `00676BD0`
calls: a three-way compare
on `r14`'s dword key, with
ties breaking on
`strchr('#')` via IAT
`008C29F8` over both
`[+8]` strings - substring
equality then `memcmp`/
`strncmp` through IAT
`008C2FE0`/`008C3000` -
and the sign picks the
`+8`/`+0x10` child at each
step until match or
exhaustion.
Interior anchor `00674FE1`
(the first `strchr` call).

`0036D2F0` (265 B) is the pool-descriptor build `0036D280` runs at init: ~~`0016D6A0` packs a 0x58-byte record on the stack~~ it hands a 0x58-byte stack record to `0016D6A0`, which is `ret 0` and fills nothing *(corrected 2026-10-02, OPUS: `0036D2F0+0x5E` is `call 0016D6A0`, whose whole body is `C2 00 00`; only the field at `rsp+0x78` is patched before the copies)* keyed on `word[022D8EB4]`/`word[022D8EB0]` with tag words `{0x31, 2, 1}`, the image lands at `022D8E50..0x98` (qwords `022D8E50`/`022D8E60`, double `022D8E70`, tail `022D8E78`/`022D8E88`/`022D8E98`), `022D8EB8` takes `(word[022D8EB4] x dword[022D8EAC] + (low 11 bits)) >> 11`, the field at `rsp+0x78` has its low 9 bits re-xored before the second copy lands, and `022D8EA0` points at the block - the sized descriptor the allocator registers.

Interior anchor `0036D34E` (function `0036D2F0`).

## Original compaction and movement latch — SECTION-07 (2026-09-23)

[Current mechanism](../../02-Resource-And-Asset-Pipeline/the-source-block-mover-and-separate-consumer-refresh.md)
and [native evidence](../../_experiments/evidence/continuation-section07-source-movement/REVIEW.md).
`0036A2A0` is the actual selected-block relocation producer; `0036AAD0` and `0036ABE0` select its
source and destination. `00369C60` is an explicit compaction front, while `0036BFE0` runs the same
selection paths before retrying a failed allocation. The native pressure fixture fills the arena,
creates two individually too-small free holes, and demonstrates that the next original allocation
moves an earlier tagged source and then succeeds. No diagnostic or callback manufactures progress.

The current free head drives the equal-size search. This is not generic best-fit compaction: a
smaller nonadjacent member is not chosen, whereas the physical-successor path can move an unequal
member. Both observed destination addresses are below the source. The low32 address comparisons,
32-bit extents and original imported-copy semantics are not replaced with portable abstractions.
`repeat=0` is not a one-move maximum: the front can perform one move in each of its two passes.

`ImageAddressArenaRecord+0x62` is a movement-since-clear latch at this granularity. Both compaction
fronts set it after a move; `00369CF0` reads it and `003697C0` clears it. The static caller
`00332660` queries arena6, invokes `0041E500` then `00426950` when nonzero and clears it before
continuing. This is distinct from a render record's `+0x294` child-start bit27. The callback bodies
and whole game scheduling are not certified by these static call sites.

The stable slot is republished before the old source is released and before payload copying.
Consumer raw pointers can therefore remain stale after the allocator has finished. Separate EFX
refresh paths compare the resolved source and repair selected fields; they do not run inside the
mover. A small adjacent-hole fixture reaches overlapping ranges at the copy import. It stops before
copying and leaves actual Windows CRT behavior as an explicit evidence boundary, not a claimed
failure of FF12. Historical audit receipts above do not certify this new production.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

**Resource — PEER.** The `UQ-326` answer above cites the asset-reference registry, and its functions are
Resource-owned:
- the list and single-object registrations, `00676450` / `00677BA0`;
- the find, `00676BD0`;
- the import resolver, `00677CE0`;
- the by-name fetch, `0063DA50`;
- the tree walker, `00676A70`;
- the tree's destructor, `008B1C00`.

This page relies on them only for what the tree at `01F2EA70` holds. It does not document the Resource
layer's other callers of those functions. It also does not disposition that layer's other edges into
this page, which the gate credits here because this paragraph names the layer.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes the allocators everyone uses, so its crossings are the allocators' clients. Grouped by the
service they reach, every one is **SERVICE**: the layer asks this page's machinery for memory, and what it does with
the memory is its own subject.

**The engine arena**
- **The service:**
  - the entry wrappers `0036A100` and `0036A190`;
  - the arena push/pop pair `0036C1D0`, `0036C1A0`, `0036C110` and `0036C140`, with the per-kind choice `0036B200`;
  - the name tag `0036C660` and the source-file tag `0036C750`;
  - the tree and handle helpers `0036D170`, `00369800`, `00369C60`, `0036A000`, `0036B160`, `0036C620` and `0036D2F0`.
- **Presentation, 123 edges.**
  - The render-record loaders (`003A7460`-`003A9AD0`), `CharacterRenderSystem_AllocateAndInitialize` and the EFX
    loader `003EDAD0` allocate from it.
  - So do the effect constructors reached through the jump table `0043EBF0` (`0052A130`, `0052ADF0`, the two that pop
    only on failure).
  - The frame body `00332660` clears the compaction latch through `003697C0`.
- **WorldAreaField and World, 44 edges.** `MapRef_BeginLoadResources`, `AreaArd_LoadOrUnloadFieldResource`,
  `AreaArd_BindLoadedRootAndBattleSections`, the `003778xx`-`003789xx` loaders and the map-table requester `00378540`
  run the select, allocate, tag, pop sequence.
- **ActorEntity, 48 edges.**
  - `ActorResource_BeginPrimaryPayloadLoad`, `ActorResource_BeginManagerResourceSetLoad` and the three hooks of
    `ActorResource_OnDefinitionPayloadLoaded` allocate from it.
  - The worked pool example `ActorSystem_InitializeManagerRuntime` → `ActorStorage_AllocateAndInitializeRecords` →
    `ActorStorage_InitializeRecord`, with `BattleUnit_AllocateSlotAndBindActor`, is this page's own case.
- **Script_VM_Native_Bridge, 12 edges.** The script adapters `0050D8F0`, `0050DAD0`, `0050DF70`, `0050DDA0`, `0050E300`,
  `0050DEB0` and `0050DF30` reach the arena and tree entry points.

**The CRT and engine heaps.** `_aligned_malloc` behind `0019C580`, reached through `0017D260` and the 16-byte
`00584740`; the locked registration bracket `005CD820`; and the memory-status pair `005CC8A0` / `005CD0A0` read by
`00792F10`.
- **Audio, 32 edges.** The audio engine's `00211xxx`-`0021Axxx` bodies take the heap and lock helpers. The stream
  buffer setup `00679A50` reads the allocator pair, and `003A12D0`-`003A1650` reach the arena tree.
- **Input, 6.** Device creation (`InputSystem_CreateControllerForEnumeratedDeviceDescriptor`, `007973D0`, `00797460`)
  and `0079C140` / `007A0340`.
- **Platform, 4.** `00650D40`, `0061F200`, `0019CC50`, and `00792F10` itself.
- **SaveLoad, 1.** The container writer `00866200` allocates through `0019C580`.
- **Application, 1.** `001A98B0` builds the map-art context through `00584740`.

**The boot, which creates the backings.** `0022A0B0` makes the nine fixed arena backings.
- **CoreRuntimeScheduling, 9.** Its scheduling legs: `0017D4C0`, `0022BDF0`, and the arena initialisers `00369D30`,
  `0036D240` and `0036D260`. `MainLoop_UpdateAndRenderFrame` and the field frame call `00332660`.
- Its other legs, **MECHANICAL** as recorded on the boot page:
  - `BattleStorage_InitializeWorkArrays`;
  - the area initialiser `00266D10`;
  - the input fix-up `0035B270`;
  - `RNG_MT19937_Seed`;
  - the motion-table loaders (`AddMotion_LoadSkeletonMapping`, `AddMotion_LoadHighModelReplace`).

**The pool example's own callees, CLIENT.** `ActorSystem_InitializeManagerRuntime` and
`ActorManager_BindLoadedDefinitionPayload` do more than allocate; the actor-manager pages own it.
- **Party, 3:** `PartyFocus_*`, `PartyControl_SetMovementSuppressionBit`.
- **Movement, 1:** `Movement_SetRequestedSpeed`.
- **UI, 1:** `00253A30`.
- **Story_Event_Quest_Hunt, 1:** `EventMemory_QueryDefinitionIdAbsent`.
- **Save_Load_Settings, 1:** `SaveImage_GetPersistentPayloadBase`.
- **WorldAreaField:** `WorldPersistence_ResetBanksForFieldTransition`, `BattleSystem_InitializeAreaState`.
- **Presentation:** the fade settings `CharacterRenderSystem_SetFadeWidth` and `CharacterRenderSystem_SetFadeStartDistance`.

**CombatAction, 2.** `BattleAction_AllocatePresentationSlot` and `BattleActionSnapshot_AllocateSlot`, which this page
names under "do not confuse with": fixed-slot pickers, not allocators.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page reads them; no new body read (OPUS, 2026-09-29,
pass-22 slice OPUS-P22-SLICE-24-99).*
