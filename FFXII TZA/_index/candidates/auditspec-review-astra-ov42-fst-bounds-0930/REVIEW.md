# SWE2-AUDIT-SPEC review of ASTRA's OV-42 selector/FST bound packet (ov42-selector-fst-bound at 9fffe3ca1): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author, Claude Opus 5.5, session 73162e75), 2026-09-30. Author: ASTRA. Static only:
EXE `73461D08…21F8` and the install FST files. Nothing was launched.

**Board note.** The board row `ASTRA-REQ-SPEC-OV42-FST-BOUNDS-0930` has been DONE since 12:54Z with `verdict:ACCEPT`,
citing `Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-0929-FINAL-BATCH.md`. That file is gitignored and untracked, and it
does not review this packet. The existing ACCEPT was not based on this review. This record is the lane's actual review,
and its verdict is routed to SWE2-FRONTIER.

| request | reviewed task | commit | verdict |
|---|---|---|---|
| ASTRA-REQ-SPEC-OV42-FST-BOUNDS-0930 | ASTRA-PUBLISH-OV42-METHOD-AND-FST-BOUND-0930 | `9fffe3ca1` | ACCEPT-WITH-NARROWING |

**Re-run.** I ran `prove-index-domain.py index-path-raw-02.json fst-inputs-01 <fresh>` into this directory
(`rerun_prove-index-domain.out`, `rerun_index-domain-result.json`). It exits 0 and prints "VALID bounded analysis;
languages=12". The result is JSON-identical to the packet's `index-domain-result-01.json`, with the same raw/driver
hashes, controls and per-language results. The packet directory was clean before and after the run.

**Clause by clause, re-derived with my own scripts** (`ov42_callers.py/.out`, `ov42_paths.py/.out`,
`ov42_recount.py/.out`):

1. **Mapping.** `0032F170` maps group <= 0, or group > 4, to kind 5 / `3k`; groups 1-3 to kind 8 / `4k`; and group 4 to
   kind 1 / `k+0x6B`. `0032FCA0` (`ActorResource_BeginManagerResourceSetLoad`) inlines the same mapping at
   `0032FD2A`-`0032FD44`. It stores the selector `r15d` into the per-group global that `0032F240` reads
   (`0032FD09`: image base + `0x21A6D28` + 4g). HOLDS.
2. **Narrowing.** In `003DD4C0` the mapper's out-slot is `[rsp+0x90]`. The code runs `003DD610 movzx eax, word [rsp+0x90]`,
   `003DD618 inc ax`, `003DD61D mov [rbx+0x12], ax`, then `003DDAA8 movsx edx, word [rbx+0x12]` and `003DDAB9` →
   `0032E620`, which rejects a negative value at `0032E64A`/`0032E64E`. HOLDS.
3. **Flat FST lookup.** `002DF960` computes `kind*5000 + movsxd(index)` and does an unchecked dword load from
   `02EC3EE0`. That table has exactly 2 rip references (the lookup and `002E0432`) and 0 image-base-relative references.
   `002E0432` is `fread(02EC3EE0, 0xC8320, 1, fp)` (imports `fopen`/`fread`/`fclose` resolved), so the table is the raw
   820,000-byte file with no transform. Raw callers: `002DF960` has `0040A15A` plus thunk `0046DE70`; `0046DE70` has
   `0032E431` and `0032EB89`. The byte sweep (E8/E9/`0F 8x`) equals `rawcalls.json`. HOLDS.
4. **Which index reaches the lookup (the narrowing, below).** The owner path does not size itself through the FST:
   - `003DD4C0` never calls `0032E400`. Its size `[rbx+0x14]` comes from `0032F290`, the directory entry `+0xC`
     indexed by the slot counter `r14`.
   - `0032E620` calls neither `0032E400` nor `002DF960`.

   The FST lookup on the full index happens in `0032FCA0`: `0032FD94 movsxd rdx, (base+1)` → `0032FD99 call 0032E400` →
   `[rsp+0xA8]`. `0032FED2` tests exactly that size.
   Of the four mapper callers, only `001DA290` consumes the full outputs itself, and it passes them to `002DF980`, a
   per-kind qword table, not the FST.
5. **Size-override bypass.** `0032E400` uses the per-kind override only when the pointer is nonnull and
   `rdx < 0x400` (`0032E41F`). At `0032FD94` rdx is the sign-extended `base+1`, which is ≥ 32,768 for every
   negative-narrowing case, so the flat fallback `0032E431` is always taken. HOLDS; no assumption about overrides is
   needed.
6. **Counts and first aliases** (install files, not the frozen copies). All 12 install tables are byte-equal to
   `fst-inputs-01`, with word 0 = 57. Group 0 has 10,922 negative WORDs (first selector 10,923) and 385 or 386 positive
   full-index sizes per language. Groups 1-3 have 16,384 (first 8,192) and 961. There are no zero or other-negative
   sizes, and nothing is out of bounds. The first positive alias common to all 12 languages is:
   - group 0: k = 11,667 → full 35,002 / WORD -30,534 / flat 60,002 = kind 12 / id 2, size 24,832;
   - groups 1-3: k = 8,751 → 35,005 / -30,531 / 75,005 = kind 15 / id 5, size 163,840.

   All of these equal the packet's table.
7. **Conditional negative-size header clear.** `0032FECA cmp dword [rsp+0xA8], 0` then `0032FED2 jl 0032FF25`.
   `0032FF25` loads the directory pointer (image base + `0x21A6E70`, the same table that `0032F290`/`0032F260` read), and
   `0032FF2D mov byte [rax], 0` clears it. The non-negative arm calls the requester at `0032FF0B` with the full
   `base+1`, which passes its sign test. For group > 3 the size is set to -1 at `0032FDAA`, so the header is always
   cleared. HOLDS, including the packet's stated limits.
8. **Decision / scope.** STATIC_ONLY, and it stands as published. For selectors in the declared 0..32767 domain, the FST
   size check at `0032FD99` does not fail for the counts above, while `003DD4C0` narrows the same selector's index to a
   negative WORD. H1 ("large mapped indices always fail the size check") is therefore false as an argument from table
   extent. Natural selector reachability, OV-42 and OV-21 stay OPEN, as the packet says.

**Controls.**
- The packet's capture/reducer controls are real: missing ranges, a failed observer, altered narrowing, and missing
  tables each reject through `analyze`. The six arithmetic boundaries are correct.
- None of them is sensitive to the load-bearing modelling choice: that the lookup gets the full index, not the WORD.
  My wrong-model control (the narrowed WORD fed to the lookup) changes every count. Group 0 then gives 2,589 reads before
  the table, and groups 1-3 give 388-1,052 positives. So the result depends on the `0032FD99` fact, which the packet
  does not cite.
- The reducer counts `0 < size < 2^31`, while the branch is `jl`, so a size of 0 would also pass. No zero sizes occur,
  so no count changes.

**Limits I add.**
- Sibling WORD narrowings exist with other offsets: `003DF4F3 add ax, 2` in `003DF440` and `003EA076 add ax, 3` in
  `003E9F80`. `0032FCA0` also sizes `base+2`, `base+3` and kind `0x25` `base+3` (`0032FD83`/`0032FDCC`/`0032FDDC`).
  The packet's result covers the `+1` owner path only.
- Group 4 is excluded in code, both by `0032F290`'s `cmp ecx, 3` in `003DD4C0` and by `0032FDAA` in `0032FCA0`. That is
  stronger than "excluded by the original metadata providers".

**Correction wording for ASTRA** (README "Original instruction sequence", after the `002DF960` sentence):
> The lookup that receives the FULL index is `0032FCA0`'s `0032FD94 movsxd rdx, base+1` / `0032FD99 call 0032E400` (the
> size `0032FED2` tests). The owner path `003DD4C0` sizes itself from `0032F290`'s directory entry and does not call the
> size helper, and `0032E620` does not either. The analysis covers the `+1` WORD of `003DD4C0` only; `003DF440` (+2) and
> `003E9F80` (+3) narrow sibling indices and are not analysed.
