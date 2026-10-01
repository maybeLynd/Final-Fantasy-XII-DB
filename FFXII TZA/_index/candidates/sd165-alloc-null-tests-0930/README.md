# SD-165: which callers of the arena allocator test its result for null (OPUS, 2026-09-30)

Register row SD-165 was registered by SWE2-DATA ([where-the-games-memory-comes-from.md](../../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md)
sections 1 and 2). It asks which callers of the arena allocator test its result for null. Three cases are read on the
page, and no census exists.

This record is static. The checker is `sd165_nulltests.py` (output `sd165_nulltests.out`, `FAILS 0`). The per-site
result is in `sd165-sites.tsv` (206 rows: entry, caller, site, class).

## Method

The census covers every call site of the four entry points callers use:
- the raw-block wrappers `0036A100`, `0036A190` and `0036A1A0`;
- the handle path `0036B160`.

~~The retry allocator `0036BFE0` is reached only through these and the allocator's own helpers.~~ *(False: see the repaired answer - `0036A230` and the realloc `0036CAD0` also reach it.)*

The returned value is followed from the instruction after the call: the register it is in and its copies, including
callee-saved registers across calls, for up to 24 instructions. Each site is classed by what comes first:

- **TESTED:** a `test` / `cmp … 0` of the value before any dereference. The caller checks for null.
- **DEREF:** a memory access through the value before any test. The caller uses it unchecked.
- **PASSED / STORED / RETURNED:** the value becomes a call argument, is written to memory, or is returned, with no
  test and no dereference in the window. The check, if any, happens elsewhere.
- **UNCLEAR:** the value is lost without any of these.

**Controls (C1).**
- `002E678F` stores the handle and then tests it: TESTED.
- `0024A2B9` keeps the pointer in `rbp` across a call and writes through it with `movups [rbp + …]`, untested: DEREF.

## The repaired answer (OPUS, 2026-10-01, on SWE2-AUDIT-SPEC's REJECT)

SWE2-AUDIT-SPEC's [review](../auditspec-review-sd165-0930/REVIEW.md) (`e1a2c0f05`) REJECTED the first census. Its entry list missed `0036A230` (47 sites)
and the realloc `0036CAD0` (2), and it counted the two thunk `jmp`s into `0036A1A0` as sites. Its classifier had five
defects: a register was not killed by a partial-width or memory write, `lea` and `nop` read as dereferences, an in-body
`jmp` read as RETURNED, and a stack spill read as STORED. **`sd165_nulltests_v2.py`** (output `sd165_nulltests_v2.out`,
**`FAILS 0`**, per-site `sd165-sites-v2.tsv`) repairs all of these:
- the method is the docstring's;
- one control per defect (dK `0025623B`, dL `005033B1`, dJ `003EA03C`, dS `00259E27`, dN `002562FE`), plus the
  original two controls and a `0036A230` site;
- the entry census is checked at 110 / 81 / 47 / 13 / 2 = 253.

`0036A1A0` is the body the two thunks share (`0036A195`, `0036A232`), not an entry. `0036BFE0` is reached through all
five entries, not "only through these" four.

| entry | sites | TESTED | DEREF (unchecked use) | PASSED | STORED | RETURNED | UNCLEAR |
|---|---:|---:|---:|---:|---:|---:|---:|
| `0036A100` | 110 | 5 | 30 | 36 | 32 | 7 | 0 |
| `0036A190` | 81 | 42 | 2 | 25 | 9 | 1 | 2 |
| `0036A230` | 47 | 47 | 0 | 0 | 0 | 0 | 0 |
| `0036B160` (handles) | 13 | 4 | 0 | 2 | 6 | 1 | 0 |
| `0036CAD0` (realloc) | 2 | 0 | 0 | 1 | 1 | 0 | 0 |
| **all** | **253** | **98** | **32** | **64** | **48** | **9** | **2** |

- **98 sites check** the result before use, including all 47 on `0036A230`.
- **32 sites dereference it unchecked**, 30 of them on `0036A100`. A failed allocation there faults. The list is in
  the TSV.
- **121 sites hand the value on** (passed, stored or returned) before either. Whether a null is checked there depends on
  the callee or a later reader, which is not traced.

The reviewer's own classifier, a different implementation, agrees on 252 of 253 sites. The difference is `0050EF2C`
(realloc): `mov edx, eax` hands the result, truncated to 32 bits, as the second argument of the tail jump to
`0026B4E0`. This record classes it PASSED and the reviewer RETURNED; nothing returns `rax` to the caller there. The
reviewer reads `0032E80E` as DEREF by hand, and this classifier agrees.

**For modding:** raising allocation pressure is safe only if the arenas' reclaim succeeds. The 32 unchecked
dereferences would fault on a null block.

## The first answer, REJECTED (OPUS, kept struck)

| entry | sites | TESTED | DEREF (unchecked use) | PASSED | STORED | RETURNED | UNCLEAR |
|---|---:|---:|---:|---:|---:|---:|---:|
| `0036A100` | 110 | 5 | 15 | 50 | 31 | 9 | 0 |
| `0036A190` | 81 | 41 | 2 | 21 | 12 | 2 | 3 |
| `0036A1A0` | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| `0036B160` (handles) | 13 | 4 | 0 | 2 | 6 | 1 | 0 |
| **all** | **206** | **50** | **17** | **73** | **49** | **12** | **5** |

~~- **50 sites check** the result before use. Most are on `0036A190`, which half its callers test.~~
~~- **17 sites dereference it unchecked** (15 on `0036A100`). A failed allocation there faults. The list is in the TSV.~~
~~- **134 sites hand the value on** (passed, stored or returned) before either. Whether a null is checked there depends~~
~~  on the callee or a later reader, which is not traced.~~

~~**For modding:** raising allocation pressure is safe only if the arenas' reclaim succeeds. The 17 unchecked~~
~~dereferences would fault on a null block.~~

*(The table above is the rejected first census: superseded by the repaired one.)*

## Limits (OPUS)

- **The window.** The 24-instruction window follows an unconditional `jmp` inside the caller's body but not conditional branches. A test on another path, or after the window, is not seen.
- **Handed-on values.** Whether a check happens after the value is passed or stored is not traced.
- ~~**`0036A1A0`'s two sites** were not classified.~~ They are the thunks' jumps, not sites (repaired).
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
