---
system: Where the game's memory comes from
category: 24-Compiler-And-CRT-Runtime
status: REOPENED
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
> Windows DLL the game does not ship — through exactly **six** doors. The game never creates a
> heap of its own, never reserves a pool up front, and never checks whether the memory it just
> asked for actually arrived.

## 1. What the player sees

Watch FFXII in Task Manager while you play. The memory figure is not flat. It climbs as you walk
into Rabanastre, climbs again when the Bazaar crowd streams in, drops back when you leave for the
Estersand, climbs hard on a summon cinematic. The game is asking Windows for memory and giving it
back, continuously, all the way through a session — it does not grab one big block at startup and
live inside it the way a console game does.

That has two consequences a player can actually feel.

**The game's appetite is set by what is on screen, not by a setting.** There is no memory slider
in the options, and no texture budget that the game enforces on itself. It loads what the zone
asks for. On a machine with plenty of RAM this is invisible. On a machine that is short of it,
Windows starts paging, and the symptom is the one everybody knows: the game keeps running at a
normal frame rate right up until a zone transition, and then the loading screen takes ten times as
long as it did an hour ago.

**When memory genuinely runs out, FFXII does not tell you.** There is no out-of-memory message in
this game, and no graceful fallback. The code that builds a zone's actors asks for its block, gets
nothing back, and then writes to it anyway. The result is an instant close to desktop with no
dialog — the classic "it just disappeared" report. It is not a corrupted save and it is not a bad
install; it is the engine trusting an allocation that failed.

This also explains something modders run into immediately. Because the game leans on the C runtime
that *Windows* supplies rather than one it ships in its own folder, two machines running the same
copy of FFXII are not running the same allocator code. A memory bug that reproduces on one PC and
not on another, with identical game files, is behaving exactly as designed.

## 2. Native mechanism

### One heap, six doors

`FFXII_TZA.exe` imports **538 symbols across 30 DLLs**. Of those, exactly **eight** are heap
functions, and all eight come from `api-ms-win-crt-heap-l1-1-0.dll` — the API-set stub that
forwards to `ucrtbase.dll`, the Universal C Runtime that ships with Windows. Six of the eight are
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
| `_set_new_mode` | **0** | — |

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
> buffer) come from it, and `0036C660` tags a block's header with a 7-character name. Where the
> arena's backing is obtained — through the CRT imports listed here or otherwise — is not established
> on this page (ASTRA's EXP-077 / EXP-078). "There is no pool to size" is withdrawn for the resource
> path.
>
> **Where the backing comes from (2026-09-12, ASTRA's supplement re-read by FABLE).** At boot,
