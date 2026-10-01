# T5 - REGFILE-REUSE: does any native store reach ActorStorageRecord +0x64..+0x83 between release and reuse?

FABLE reader, 2026-09-29. Static only. The request was read from TEAM.json (`FABLE-REQ-ASTRA-REGFILE-REUSE`, task 884). Sources read:
- interpreter page section 13;
- ASTRA's `_experiments/evidence/regfile-reuse-identity/README.md`;
- the record page's nineteenth pass (one initialiser caller);
- the respawn page, section 5 item 4;
- the RC-8 model `rc8_inverse.py`.

## Files
| file | what |
|---|---|
| `t5_regfile.py` -> `t5_regfile_h2.out`, `t5_regfile_h3.out` | the inverted census: `python t5_regfile.py 2` and `3` |
| `t5_basedefs.py` -> `t5_basedefs_h2.out`, `t5_basedefs_h3.out` | the backward slice of each surviving store's base register |
| `t5_argtypes.py` -> `t5_argtypes.out` | call-site typing of hop-3 survivors whose base is an entry argument |
| `bulkcalls.tsv` (from T3) | destination and size of every memset/memcpy/rep site |

## 1. The record, and how code reaches one
- **Type.** ActorStorageRecord. The register file is I0..I3 at +0x64..+0x70 and F0..F3 at +0x74..+0x80 (interpreter page, section 13).
- **Pool.** Each manager is `02098E10 + idx*0x288`, with at most five up to the value stack at `02099AC0`. The pool root is manager +0x08. It is allocated by `002679F0` through `[r15+0x88]` (`00267A79`), zeroed whole by `memset` at `00267A8B`, and installed at `0026CEB0`.
- **Pool layout:**
  - dword count at +0;
  - record-pointer table at +8 (`00267AF5`);
  - records carved after the table in per-class sizes from `01E0C328`: 0x2D0, 0x328, 0x330, 0x348, 0x3A8, 0x668 or 0x6E0 bytes, 16-aligned (`00267B16`..`00267B21`).
  - **There is no uniform stride.** ~~Manager +0x1F0 is the derived address of the first record, not the allocation root.~~ *(Narrowed 2026-09-30, FABLE, on SWE2-AUDIT-SEM's ACCEPT-WITH-NARROWING, `../auditsem-review-livefacts-0930/REVIEW.md` §6, N1:)* Manager +0x1F0 points to a per-record dword array between the pointer table and the records (`pool + align16(8n + 0x17)`, set at `00267AA8`; filled by `0046BAC0`); the records start at twice that offset.
- **Resolvers.**
  - `ActorManager_GetRecordByOrdinal` `00358940` returns `qword [pool + 8 + ordinal*8]` after a null and bounds check.
  - The interpreter receives the record in rdx from `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025E0CD`/`0025E0D3`) and keeps it in r15.

## 2. The inverted census
- **H0 = 162 functions:**
  - 75 callers of the getter (raw E8/E9 index);
  - 96 with a rip-relative reference into the manager array;
  - the one image-base-relative form `0026C8FE lea rdi,[r14+0x1f78e10]`;
  - the allocator, the initialisers and the release `002693D0`, with their callers.
- **Hops.** H2 adds two hops of direct callees (1,146 functions) and H3 three (1,643).
- **W.** Image-wide there are 1,443 listed functions with a non-rsp store (any width, any writing mnemonic) whose byte range overlaps +0x64..+0x83.
- **W and H2: 22 functions.** Every store's base was sliced back (`t5_basedefs_h2.out`). **Only the interpreter stores through the record itself.** The others:

| function | base, by its defining instruction | what it is |
|---|---|---|
| `0025E4C0` interpreter | r15 = the record argument (`0025E4D5`) | **the register file: control** |
| `002693D0` callees `002681E0`, `0026AE90`, `0026A870`, `0026A8E0`, `0026C070`, `0026C300`, `002EC3F0`; also `00265FF0`, `00265B60`, `0025B070` | loaded from `[rec+0xC0]`->`+0x138`, `[rec+0xB8]`->`+0xF0`, `[rbp+0xB8]`, `[rbx+0xC0]`, `[rbx+0xB8]` | movement and secondary context sub-objects |
| `00265A20`, `00329A80`, `00234200` | `00359B80` / `ActorWork_GetBattleUnitRaw` = `[rec+0x30]`; `[rbx+0x6A0]` | the battle unit and the spawn record |
| `0026C8C0` `ActorManager_BindLoadedDefinitionPayload` | rdi = `02098E10 + idx*0x288` (`0026C8FE`/`0026C90E`) | **the manager**, whose +0x60..+0x87 are block pointers |
| `00259620` -> `0032B8B0` | `lea rdi, 02098428` | static camera object |
| `0035BB70` -> `002A27F0` | rip-loaded global, `[rbx+0xC0]` | other objects |
| `00369860`, `00369D30` | allocator internals (`lea rcx,[rdi+rax*4]`, arena `rbx`) | allocator |
| `00375900`, `003A4290`, `00472820`, `00518E60` | indexed static table; rbp frame; render matrices (callers `003E0740`/`003E3D70`) | not records |

- **Hop 3 adds 26 functions.** They were typed by slice and by call-site argument (`t5_basedefs_h3.out`, `t5_argtypes.out`):
  - BattleStats via `[unit+0x698]` (`0030E360`);
  - BattleUnit (`0023A570`, `00300E40`);
  - UI widgets (`00244DD0`, callers in 0028xxxx through `[x+0xF8]`);
  - the camera (`00380B80`/`00380D30`/`003D99B0` from `00259B30`);
  - request-queue slots (`0032EC40` from `0032E070`);
  - render (`004FEAD0`, `00519A30`, `0051A320`);
  - stack frames, and static tables (`0033CA00`, `00375A20`).
  - **None is a record.** Two bases are typed only by the band of their callers, not proven: `003AB960`'s rdx and `0036BC60`'s rbx.
- **Bulk operations inside H2: 58 sites in 37 functions** (list in `t5_regfile_h2.out`, destinations in `bulkcalls.tsv`).
  - **Only one covers a record: the pool memset `00267A8B`** (control).
  - The others, all 58 checked against `bulkcalls.tsv`, resolve to:
    - static tables: the manager array reset `00266EFC` (0x288), 02099DF0/02099FF0, 02098360/camera bases in `00259B30`, 02097xxx, 022Cxxxx, 02B4xxxx/02B5xxxx, 02EBF9E0 (`003754DF`), 02EBCBE0, `[02AEE0A0]`/`[02AEE0A8]`;
    - stack frames (`0031478D`/`0031479F`/`003147B4`, `003B03B6`, `003B81F6`);
    - the battle unit (0xF50 at `002342CE`/`002344D2`);
    - the spawn-keep banks (`[0208E690]`, 0208D354 + 0x80);
    - the save image (`002EF2E8`, `005844E9`);
    - a fresh allocation (`0039267E`);
    - allocator internals (`00369F45`/`00369F5B`);
    - the record's own +0xC8..+0xEB in the initialiser (`002668B0`, 0x12 words);
    - manager +0x204 (`0026B898`);
    - a static 0x18-stride table (`003B07EF`, r14 = `lea 02EBEC00` at `003B078F`).
  - The one data-driven copy, `0026D3E0`'s memcpy at `0026D4D5`, needs its own row. It is the authored initial-value patcher that `0026CE60` calls at `0026D300`, after the allocation. **It never writes the record.** It fetches the record at `0026D45F`, but its destination modes (table `0026D510`) are:
    - manager +0x48 / +0x40 / +0x58 / +0x60 blocks;
    - `definition + [definition+0x40]`;
    - the mode-2 callback `00264E30` (installed at `0026CB76`), which returns `[manager+0x50] + [[rec+0x40]+0x1C]`, a separate block.

**Controls.**
- The interpreter's register stores `00261624`, `00261635`, `00261646`, `00261657`, `00261668`, `0026167B`, `0026168E` and `002616A1` are found in W and H2, and in W and H3.
- The pool memset `00267A8B` is found in the H2 bulk list.

## 3. Release and reuse
**Within one pool's lifetime**, a record is never re-initialised.
- `ActorStorage_InitializeRecord` `00266530` has exactly one caller, `00267B79`, inside the allocator. Raw E8/E9 index, re-read here; this agrees with the record page's nineteenth pass.
- The per-record release is `002693D0`. Its callers are `0025B070`, `00269530`, `0026C5D0`, `003B7A30`, `003B7AB0`, and tail jumps from `00354110`/`00354590`.
- It rewrites only `+0x18..+0x1B` (`00269500 mov dword [rbx+0x18], 0xFFFF0000`) and, through `00266AD0`, the region pointers at +0xA0..+0xC0.
- Its callees `00266AD0`, `002681E0`, `0026AE90`, `002E9560`, `002E4F40`, `0026C120`, `002EAC90`, `002EB430` and `002E4A40` are all in H1. Every store they make near +0x64..+0x83 goes through a loaded sub-object pointer.
- **So between a record's release and its next use in the same pool, nothing native writes +0x64..+0x83.**

**Across pool lifetimes**, the chain is:
1. Unload `002628B0`: `0025B070` releases the records.
2. `00262D9F` calls `003697F0` (allocator release), then `00262DA4` nulls manager +0x08.
3. Next load, `0026CE60`: `0026CEB0` -> `002679F0` -> allocate -> **`memset` `00267A8B` zeroes the whole block, including every record's +0x64..+0x83**.
4. `00266530` runs per record (`00266AD0`, `00266BD0`), then `0026D3E0` (never the record).
5. The first script instruction comes through `0025D9E0` -> `0025DF00` -> `0025E4C0`.

## Conclusion
**H1 holds statically for reuse within a pool:** no native store reaches +0x64..+0x83 between a record's release (`002693D0`) and the next occupant's first script instruction. Only the interpreter (`0026161C`..`00261734` handlers through r15) writes the range.

**The only clear is the allocation memset `00267A8B`.** It runs once per pool allocation, so a record in a newly allocated pool starts at zero. That clear belongs to manager load, not to a spawn.

Which case a given respawn is, is the identity question ASTRA's package raised, and this census does not decide it:
- same pool, same authored ordinal: registers survive;
- after a manager unload and reload: zero.

Also not established: whether a record can host a different logical actor within one pool. Records are carved per authored ordinal and no re-initialiser exists, but no rebinding census was run.

## Limits
- Record pointers reached only through stored copies are not followed beyond three hops from the getter, the manager array or the initialisers. Examples: the global `02099D80` that `0025E0BE` writes, and back-pointers in other objects.
- Only listed functions are covered.
- Base typing is a linear backward slice. Two hop-3 bases are typed by caller band only: `003AB960` rdx and `0036BC60` rbx.
- rsp-relative stores are excluded; rbp-based stores are kept and typed.
- The census says nothing about what live play does: which respawns reuse a pool and which reload it.
