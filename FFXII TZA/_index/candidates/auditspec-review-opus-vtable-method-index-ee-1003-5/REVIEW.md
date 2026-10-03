# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-vtable-method-index-ee-1003-5)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · at HEAD `f54822cb280713ac81cf91fc9ddb3756b11bbcea` · Task: `OPUS-REQ-AUDITSPEC-OPUS-VTABLE-METHOD-INDEX-EE-1003-5-9C3ED` · Package: `_index/candidates/opus-vtable-method-index-ee-1003-5/` · Page: `00-Engine-Core-Runtime/Object-Model/vtable-method-index.md` (block "... cloud-drafted, opus-vtable-method-index-ee-1003-5)", committed in 51ad88762; page unchanged from there to HEAD)

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 30 rows hold clause by clause against the certified image. Two optional precision notes are given below. Neither blocks.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` printed `VERIFY 30 functions, 150 anchors`, `ALREADY` and `FAILS 0`, and exited 0. The output matches the committed `interior_applier.out`. All 30 texts appear on the page verbatim.
- `rows.json` has 30 rows and 150 anchors. The README reports rejected 0, skipped 0 and missing 240.
- Applier control: a scratch copy of the unmodified applier was run on a mutated `rows.json`.
  - Mutations: `00684860`'s first anchor relabelled `nop`, `007B9770`'s last anchor moved to the entry, and a pipe added to `008588A0`.
  - Result: exactly those three `VERIFY FAIL` lines, `FAILS 3`, exit 1, and the page untouched.
- Pattern rows: none. All 30 sentences differ in form, so every row was read by hand. The ten GPU-device wrappers share an idiom (log gates, error line, log strings), but each was checked against its own stack slots and constants.
- Image: `rvlib.Img` (sha-checked, base 0x00120000, section-aware). Every body was decoded to its true end, which is the larger of the stated size and the chained `.pdata` extent. In `007B93E0`, `007B9770` and `007E32E0` the extent adds one `int3` after a trailing `call 00809728` stub, and each row names that stub.
- RTTI: 28 of 30 match the appendix's class and slot, each with one vtable hit.
  - `007B93E0` and `007B9770` are slots 1 and 5 of `ExternalSourceVoice`'s secondary vtable (COL offset 8), as the appendix says.
  - `00684860` and `00841010` are not appendix methods. They have no `.rdata` qword and are named on the page only at their entries.

### SWE2-AUDIT-SPEC: the 30 rows (read by hand, to the end of each body)

The ten `GPUInterfaceDevice` wrappers are exact: `00725C80`, `00725E40`, `00725FF0`, `007261B0`, `00726550`, `00726700`, `007268C0` and `00726A70`, plus `00725AA0` and `00726360` in package -6. In each one the following were checked against the stack slots derived from the prologue:
- every log argument and its order;
- the `jb 1` log gates (`01F3BA80` with `01F3BA90` or `02EA0B40`);
- the callee's argument list;
- the error-log constant and the line number.

Further rows:
- `00684860` exact. The pass count is reset at `00684908`. Each later walk does `inc`, then `test 0x3FF`. The wrap path restarts with `jmp 006848B0`.
- `00808240` exact. The reviewer read this row in full.
  - `00802310(rcx, r8)` is called first; a negative result is returned.
  - The cursor's slot `+0x10` is 0, or the comparison against `00802820(slot +8 result, [cursor+8])` (signed `jle`), returns 0.
  - The binary search runs from `movsxd [b+0x10]` to `movsxd [[rcx+8]+0xA8]` over `[[rcx+8]+0xA0]`. Each key is `00802DA0`'s result, sign-extended when negative, else `[e+0x28]`. A non-negative key is multiplied by `[[[e]+0x78]+0x28]`. The search ends at the first entry greater than `rdx` (`jg`).
  - The first step back is unconditional. `00802100(entry, rcx, rdx)` is stored at `[r8]` after each step. The only bound is `cmp rbx, start` after a step, which stores `rcx+0x90`. When the search position is the start index, or the range is empty, the walk therefore goes below the start, as the row says.
- `007B93E0`, `007B9770` and `007E32E0` exact. The ring slot is a signed remainder of 32. The `div` is unsigned 64-bit. Newline, terminator and `00809728` are handled as stated.
- The other 17 rows are exact: `00725340`, `00769470`, `0077DED0`, `00787080`, `00787930`, `007C61F0`, `007D9070`, `007DC340`, `008373D0`, `00841010`, `00841D30`, `00847D00`, `0084A0C0`, `00855660`, `008557F0`, `00857CD0` and `008588A0`.
  - Every clause holds, including NaN and unordered paths (`jp` / `jb` / `ucomiss`), signed against unsigned jumps, re-read bounds and null tests.
  - Constants read in the image: `01CEBBA8` = 1.0, `008F30F8` = 0.2, `0090035C` = 0.08, `01CEBC08` = 2.0, `00D10FA8` = 2000.0 and `00D841C0` = 2^-23. `01CEBD80` is the double sign-clear mask.
  - `00861FAA` is a `jmp [IAT]` thunk to `expf` (IAT cell `008C2CA0`).
- Anchors: all 150 are strictly inside their bodies and decode as recorded. Each anchor does what its row says.

*Optional precision notes (non-blocking):*
- `007D9070`, "else (NaN included) keeps the byte at 1": the body stores 1 (`007D909C mov byte [rcx+0x38],1`, and the same in each arm) whatever non-zero value the byte held. "Sets the byte to 1" would be exact.
- `00855660` and `008557F0`: the grow path also stores the new capacity (`[rcx+0x128]` = `esi` at `0085576B` / `00855908`). The parenthetical does not name that store. The row does not claim the list is complete, so this is precision only.

### SWE2-AUDIT-SPEC: engine_explained crediting (ruling opus-ee-rulings-1003 section 2, FRONTIER 1e64e4042)

Measured at HEAD with `progress.py`'s own helpers: `index_only_headings`, `strip_index_only`, `evidence_bearing`, `family_rule_inputs`, `cite_credits` and `doc_credits`.
- The appendix is the only `ee_index_only` heading, and stripping it removes the appendix. This block is its own `##` section outside it.
- The page is evidence-bearing. The in-scope family overlap with the 30 rows is 0.
- **All 30 credit engine_explained, and only through this block.**
  - Without the block, the stripped page credits 0 of the 30, and no other page credits any of them.
  - Every crediting cite is a row's interior anchor.
  - Bodies are 151–438 B, so no small-body allowance applies.
  - `check_dispositions.evaluate` puts all 30 in `a_set` and `explained_set`, and none in `frontier_set`.

### SWE2-AUDIT-SPEC: the scoped-row ruling (auditspec-ruling-scoped-ee-row-1003, at HEAD)

No row opens with `Scope:` or carries `scoped row: set-exact`. With `scoped_out` (condition 5), `doc_credits` puts all 30 in the plain set and 0 in the scoped set. These are full exact rows, so the ruling adds no condition here.

- Limits: static evidence only. The cloud draft and OPUS's re-read are not independent review; this record is. Of this package, 29 rows were read in a forked context of the same reviewer (FABLE). The reviewer then re-read `00808240` in full and confirmed it. The scratch scripts and dumps (`rd.py`, `p5.txt`) are not committed.
