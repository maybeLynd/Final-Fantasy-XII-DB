# SWE2-AUDIT-SPEC review of SD-165 (sd165-alloc-null-tests-0930, OPUS, e87a83339): REJECT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed: OPUS's
`e87a83339`, the [README](../sd165-alloc-null-tests-0930/README.md), `sd165_nulltests.py` and `sd165-sites.tsv`. First
half measured at HEAD `9b6c5bc93`, resumed and finished at HEAD `b58c633f7`. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD165-0930 | sd165-alloc-null-tests-0930 | `e87a83339` | REJECT (incomplete site list; classifier defects move 20 of the 204 real sites) |

**Re-run.**
- `sd165_nulltests.py` rewrites `sd165-sites.tsv` next to itself. The committed TSV's mtime (14:04) is after the commit
  (08:38), so someone else has already re-run it in place; git shows no content change.
- I ran an unmodified copy, [rerun_copy_sd165_nulltests.py](rerun_copy_sd165_nulltests.py), from this folder.
  [rerun_sd165_nulltests.out](rerun_sd165_nulltests.out) and [rerun_sd165-sites.tsv](rerun_sd165-sites.tsv) are
  identical to the committed files (CR ignored). C1 and C2 PASS, `FAILS 0`.
- The package dir is clean.

**Re-derived independently** ([sd165_indep.py](sd165_indep.py) / [.out](sd165_indep.out), per-site
[sd165_indep-sites.tsv](sd165_indep-sites.tsv)). Tools: arena_ix only (raw E8/E9/jcc, DIR64, rva32, capstone
`regs_access`).
- **The site list is incomplete, and it counts two thunk jumps as call sites.**
  - `0036A1A0` has no callers. Its only 2 raw references are the `jmp`s of two thunks: `0036A190`
    (`mov edx, 1; jmp`) at `0036A195`, and **`0036A230`** (`xor edx, edx; jmp`) at `0036A232`. The TSV's two
    `0036A1A0` rows, both UNCLEAR, are exactly those jumps.
  - `0036A230` itself has **47 call sites**, all in `0043F450`. None is in the census. My classifier finds all 47 TESTED;
    the first, `0043F58E`, is followed by `test rax, rax; je`.
  - The realloc `0036CAD0` -> `0036D050` also reaches `0036BFE0` when its pointer is null. It has 2 game-code sites
    (`00251E5D`, `0050EF2C`), also not in the census. So the README's "`0036BFE0` is reached only through these and
    the allocator's own helpers" is false.
  - No entry has DIR64 slots, jcc callers, or rva32 hits outside `.pdata`.
  - Real allocation call sites: 110 + 81 + 47 + 13 + 2 = **253**. The package has 206, 2 of which are not sites.
- **The four suspected classify() defects, counted on the package's own logic.** I re-implemented `classify()` over the
  same bytes. It reproduces the TSV on 206/206 rows, which is the control that the instrumentation is the package's
  logic. For each row it records what decided the class:
  - **dK kill set** (3: `0025623B`, `00502DB9`, `005033B1`). A register overwritten through its 32-bit alias or from
    memory stays "live".
    - e.g. `0025623B`: the value is stored to `[r12+rbx+0x10]`, then `mov rax, [r12+rbx+8]` loads a different slot, and
      `[rax+0x1c]` is classed DEREF.
  - **dL `lea` read as a dereference** (5: `0024B290`, `0024B3C0`, `0024F28C`, `005033B1`, `005033C4`).
    - e.g. `005033B1`: `movzx eax, word ptr [rdi+0x38]` then `lea ecx, [rax+rax*8]`, which is arithmetic on a
      different value.
  - **dJ jump inside the function read as RETURNED** (4: `002492C5`, `003AB8DC`, `003EA03C`, `005043A0`).
    - e.g. `003EA03C`: `jmp 0x3ea048` leads to `test rax, rax; jne`, so the site is TESTED.
    - `002492C5` and `005043A0` jump to a store.
  - **dS stack spill counted as STORED** (3: `00259E27`, `00360CDB`, `00379EBC`).
    - e.g. `00259E27`: `mov [rsp+0x38], ebx`, and then the struct at `rsp+0x30` is passed.
  - **dN, a fifth defect: multi-byte `nop` padding read as a dereference** (6: `002562FE`, `00256351`, `0032E80E`,
    `00502CF8`, `00502E33`, `00503375`). `nop dword ptr [rax]` matches `\[rax( |\])`.
    - At `002562FE` and `0032E80E` the true class is still DEREF, but for other reasons: a reload in the loop, and a
      copy loop through `rdx = rax - rbx`.
  - Together: **20 distinct rows** (`005033B1` has two), none of them covered by the README's limits.
- **My classifier** has the same 24-instruction linear window. It kills on any write, treats `lea` as a derived
  pointer, ignores `nop`, follows unconditional jumps inside the function, keeps spills and reloads (stack and
  store-reload) live, and allows 32-bit copies.
  - On the 204 real sites the two share, it changes 30 classes and leaves 174 alone.
  - The largest shift is **PASSED -> DEREF, 14 sites** (`003A9F7D`..`003AA59F`). The value is passed, then the window
    reaches `jmp 0x3aa10e` inside the function, and the target writes through it untested (`003AA135 mov [rbx+4], eax`).
  - STORED -> DEREF is 5 (store and reload, e.g. `0037DAE8`, `003332D1`). DEREF -> STORED is 3 (dK/dL). DEREF -> PASSED
    is 1 (`0032E80E`; by hand it is a DEREF, so my classifier is wrong there).
  - Totals over all 253 sites: TESTED 98, DEREF 32 (33 with `0032E80E` read by hand), PASSED 63, STORED 48,
    RETURNED 10, UNCLEAR 2.
  - The README's headline figures (50 TESTED, 17 unchecked DEREF, 134 handed on) do not survive: the checked count
    nearly doubles and the unchecked-dereference count roughly doubles.

**Controls.**
- The package's C1 sites (`002E678F` TESTED, `0024A2B9` DEREF) are classed the same by both classifiers. Neither is
  sensitive to any of dK/dL/dJ/dS/dN, so C1 could not have caught them.
- C2 counts the rows against retool's caller lists of the same four entries. It is blind to a missing entry and to a
  "site" that is a thunk's `jmp`.
- I hand-read each defect on a named site from the bytes: `0025623B`, `005033B1`, `003EA03C`, `002492C5`, `002562FE`,
  `0032E80E`, `00259E27`, `003A9F7D` + `003AA10E..003AA157`, `0037DAE8`, `003332D1` and `0043F58E`.

**Citations checked.** `002E678F` and `0024A2B9` say what C1 says. The README's method sentence "`0036BFE0` is reached
only through these and the allocator's own helpers" is false: see `0036A230` and `0036CAD0` above.

**Runtime routing.** None. This is a static census question.

**Correction wording (what the producer repairs).**
1. **Entry list.** Census the real sites of `0036A100` (110), `0036A190` (81), `0036A230` (47), `0036B160` (13) and the
   realloc `0036CAD0` (2). Describe `0036A1A0` as the body the two thunks share (`0036A195`, `0036A232`), not as an
   entry with 2 sites. Replace the "reached only through these" sentence.
2. **Classifier.**
   - Kill a live register on any write, whatever the alias width, and on a memory load.
   - Do not class `lea` or `nop` as dereferences.
   - Follow, or at least do not class as RETURNED, a `jmp` whose target is in the same function.
   - Class a `[rsp+k]` store as a spill and keep tracking the reload.
   - Add one control site per defect (e.g. `0025623B`, `005033B1`, `003EA03C`, `002562FE`, `00259E27`), so a
     regression fails.
3. **Answer.** Rebuild the table from the repaired run. For reference, my classifier gives TESTED 98, DEREF 32 (+1 by
   hand), PASSED 63, STORED 48, RETURNED 10, UNCLEAR 2 over 253 sites. The 47 `0036A230` sites are all TESTED.
   Restate "17 sites dereference it unchecked" and the modding line from the repaired numbers.
