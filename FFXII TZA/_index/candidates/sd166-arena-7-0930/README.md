# SD-166: nothing selects arena 7 for an allocation after boot (OPUS, 2026-09-30)

Register row SD-166 was registered by SWE2-DATA (DD owner read batch 4, `4415dba48`) on
[where-the-games-memory-comes-from.md](../../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md)
section 2. It asks whether anything allocates from arena 7 after boot, once arena 7's backing has been used as the
effect-file load buffer.

- **Earlier narrowing:** `sd164-167-arena-allocator-0930`, `1f1defd7d`. It showed that no constant push site selects 7,
  but it left 47 variable sites open.
- **Evidence here, two kinds:**
  - **Static,** from the certified image.
  - **A census of the shipped scripts** (S1), which decodes every `.ebp` with FABLE's decoder through
    `script_verb_census.py`.
- **Checker:** `sd166_check.py` (output `sd166_check.out`, `FAILS 0`; the census run is kept as `sd166-verbs.out` and
  `sd166-verbs.tsv`).
- **New kit tool:** `Database/Tools/analysis-kit/gfz-scripts/regval.py`. It is a backward value-set resolver for a
  register at an instruction:
  - it walks the function's CFG with branch pins and follows arguments into the callers;
  - any register write it does not model yields "unresolved";
  - it carries its own self-test (P0).

## The answer (OPUS)

**No code path in the shipped game selects arena 7 for an allocation. Heap 7 is initialised at boot and never chosen
afterwards.** ~~The only way to reach it is a script calling one of two debug verbs, and no shipped script does.~~ The only way to reach it is a script calling one of four class-2 debug verbs, and no shipped script calls any of
them: `debug_tkmalloc` 0x2003 and `debug_tkmallochandle` 0x2008 (handlers `0050DA30` / `0050DBD0`, which jump into
the push functions), and `debug_tkmalloc_4` 0x2004 and `debug_tkmallochandle_9` 0x2009, whose handlers are the push
functions `0050D8F0` / `0050DAD0` themselves (class-2 table `01F26720`, slots `01F267C0` / `01F26860`). *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd166-0930/REVIEW.md))*

- **A1: every allocation takes its arena from one dword.**
  - The arena allocator `0036BFE0` receives the arena in `ecx`, and spins unless that heap's mask bit is set.
  - Its four callers `0036A100`, `0036A1A0`, `0036B160` and `0036D050` all load that `ecx` from the active-arena
    dword `022D89BC`.
- **A2: the push is an identity.**
  - The push `0036C1F0` stores `byte [022D89A8 + arg]` into `022D89BC`.
  - `00369D30` and `0036A280` fill that byte table with `table[i] = i` for i < 15.
  - `0036C272` is the only instruction in executable code that indexes it, found by a raw search for its displacement.
  - So a pushed argument is the arena.
- **A3: the 135 push sites.**
  - `regval.py` resolves each site's argument to the values below (value: sites):
    `{2: 12, 3: 12, 4: 6, 5: 24, 6: 34, 8: 44, 9: 2, 10: 1, 11: 1, 12: 1, 13: 4, 14: 4}`. **No site can pass 7.**
  - Five sites keep a non-constant term; A4 closes each.
- **A4: the five.**

  | push site | where its argument comes from | arena |
  |---|---|---|
  | `00384420` | the return of `008478A0`, which is `mov eax, 3; ret` | 3 |
  | `00249210` | a dword its callers read: the table `00D23658`, walked twice by `003934F0` (`{2,1}`, `{2,2}`); the stack struct built with `+0 = 2` by `005632C0`; and the three map-screen handlers `002B7B80`, `002BAF80`, `003CB4F0` (`003C1F00` only reads it) | 2 |
  | `003E9AA0` | `setexpandvoicememory` (`0x395`, handler `0034D080`): the script's second pop; a negative value selects 6 (`cmovns`) | the script's value, or 6 |
  | `0050D8F0` | `debug_tkmalloc` (`0x2003`, handler `0050DA30`) and itself the handler of `debug_tkmalloc_4` (`0x2004`): a script integer | the script's value |
  | `0050DAD0` | `debug_tkmallochandle` (`0x2008`, handler `0050DBD0`) and itself the handler of `debug_tkmallochandle_9` (`0x2009`): a script integer | the script's value |

  *(The `0050D8F0` / `0050DAD0` rows narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd166-0930/REVIEW.md): the class-2 table `01F26720` holds the push functions themselves as the handlers of 0x2004 / 0x2009, slots `01F267C0` / `01F26860`, both DIR64-relocated. `sd166_check.py` A4 tests direct callers only and S1 censuses 0x2003 / 0x2008 only; the four-id census is the review's `census_debugverbs.out`.)*

- **S1: what the shipped scripts pass.**
  - ~~`debug_tkmalloc` and `debug_tkmallochandle` are **never called**.~~ `debug_tkmalloc`, `debug_tkmalloc_4`, `debug_tkmallochandle` and `debug_tkmallochandle_9` (0x2003,
    0x2004, 0x2008, 0x2009) are never called. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd166-0930/REVIEW.md))*
  - `setexpandvoicememory` is called 18 times, in `byu_z9900` and `rrp_z9900` across the nine language copies. Its
    arena argument is always `PUSHII 0xFFFF`.
  - The interpreter's handler for opcode `0x4F` (PUSHII) is `0026186D movsx edx, bx`, so the value is **−1**, and
    `003E9AA0` selects **arena 6**.
- **W1: the other writers of `022D89BC`.** Five functions write it:
  - **the first heap init** (`00369D30`), only while the heap mask is 0. The boot initialiser `0022A0B0` inits heaps 2,
    3, 4, 5, 6 and then 7 in straight-line calls, so 7 is never the first. The other initialisers pass 11, 12, 13 and
    14.
  - **the push** (`0036C1F0`);
  - **the pop** (`0036C140`), which restores a pushed record;
  - **four error stores**, two in `00369860` and two in `0036CB00`. Each sets the failing block's own arena, calls the
    dump `0036A570` and an exit import, and ends in `int3`.

So after boot, `022D89BC` holds 2 or a pushed value, and a pushed value is never 7.

**For the page:** arena 7's backing is used only as the raw effect-file load buffer (the four request-destination bodies
in [authored-reference-lifetime-evidence.md](../../../02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md)
section 13). The heap header that sits over that memory is never consulted again. **For modding:** a script that calls
~~`debug_tkmalloc(7, ...)`~~ any of the four debug verbs with 7 would allocate over a live load buffer. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd166-0930/REVIEW.md))*

## Limits (OPUS)

- **The walk sees direct call edges only.** An indirect caller of a pass-through helper, a tail jump into the middle of
  a body, or a stack-passed arena argument is outside it. Every argument chain in A3 ended at a constant or at one of
  the five closed in A4.
- **Which initialiser runs first is not traced.** W1 rests on the fact that no first-init candidate is 7, not on boot
  order.
- **Static and census only.** No execution, and no live session.
