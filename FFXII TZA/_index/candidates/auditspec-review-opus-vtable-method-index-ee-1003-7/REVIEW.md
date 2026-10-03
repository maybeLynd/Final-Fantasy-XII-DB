# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-vtable-method-index-ee-1003-7)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · at HEAD `f54822cb280713ac81cf91fc9ddb3756b11bbcea` · Task: `OPUS-REQ-AUDITSPEC-OPUS-VTABLE-METHOD-INDEX-EE-1003-7-DA9A6` · Package: `_index/candidates/opus-vtable-method-index-ee-1003-7/` · Page: `00-Engine-Core-Runtime/Object-Model/vtable-method-index.md` (block "... cloud-drafted, opus-vtable-method-index-ee-1003-7)", committed in 51ad88762; page unchanged from there to HEAD)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

11 of the 12 rows hold exactly. One row, `00785C90`, puts an unconditional store inside a conditional clause. A one-clause rewording fixes it; the exact text is below. The anchors and the crediting are not affected.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`: `VERIFY 12 functions, 60 anchors`, `ALREADY`, `FAILS 0`, exit 0. This is identical to the committed `interior_applier.out`. All 12 texts appear on the page verbatim.
- `rows.json`: 12 rows, 60 anchors. README: rejected 0, skipped 0, missing 48.
- Applier control: a scratch copy of the unmodified applier was run on a mutated `rows.json`:
  - `00785C90`'s first anchor relabelled `nop`;
  - `00835000`'s last anchor moved to the entry;
  - a pipe added to `00857970`.

  It reported exactly those three `VERIFY FAIL` lines and `FAILS 3`, exited 1, and left the page untouched.
- Pattern rows: none. Every row was read by hand.
- Image: `rvlib.Img` (sha-checked, base 0x00120000, section-aware). Every body was decoded to its true end. For all 12 bodies the stated size equals the chained `.pdata` extent.
- RTTI: 12 of 12 match the appendix's class and slot, each with one vtable hit and COL offset 0.

### SWE2-AUDIT-SPEC: the 12 rows (read by hand, to the end of each body)

Constants read in the image: `01CEBB70` = 0.5, `0x3FB4FDF4` = 1.414, `01CEBD80` = double abs mask, `01CCD4E4` = -1e18, `01CEBDA0` = float sign mask, `01CEBBA8` = 1.0, `01CEBB60` = 0.0001, `008F30E8` = 0.05.

- `00785C90`: **one clause is misplaced.** The reviewer read this row in full. All the other clauses hold:
  - When both `a` and `b` are non-null, the body calls `a`'s slot `+0x38` with `&t`, calls `t`'s `+0x10` if it is non-null, and drops `b`.
  - It releases `+0x110` / `+0x118` / `+0x120`.
  - It sets dword `+0x14` to 2 and calls `00784810`, or sets it to 1 and calls `00784D70`. It then calls `0078A970` and sets `f` from bits 0x20 and 0x40 of `+0x58`.
  - It calls `0078AB60`. It stores `a` at `+0x110` even when `a` is null. It stores `b` at `+0x38` only inside the `b`-non-null branch.
  - The `+0x14 != 2` branch includes the `a`-slot `+0x38` call with no null test, and the `+0x70` 1/2 copies.
  - The `f`-bit-1 tail is `007853F0`, then own slot `+0x48`(0, `rcx`). On a negative `r` it logs with the gates `jb 1` on `01F3BA80` / `01F3BA90`, calls own slot `+8`, then logs with the gates on `01F3BA80` / `02EA0B40`. The strings are `00DACF20` / `00DACF70` / `00DACFC0` / `00DACFF0` and the lines 0xFE4 / 0xFF6.
  - The sixth argument is at `[rsp+0x68]` after three pushes and `sub 0x20`, which is entry+0x30.
  
  The defect is in the clause about the sixth-argument store. The row places "stores the sixth-argument dword at `+0x28`, AND ~0x300 if bit `0x800` of dword `+0x24` (re-read) is set" inside "if `f` has bit `0x1`: … ; returns `r`, else 0". In the body that store runs on every path. It is at `00785E9C`–`00785EB1`, and that point is reached from the `f`-clear branch (`test bpl,bl` / `je 00785E9C`) as well as from the non-negative `r` exit.
  
  A pre-store at `00785D7B`/`00785D81` (`bt ebx,0xb` / `and [rdi+0x28],0xFFFFFCFF`) can never fire, because `f` is at most 3. The row leaves it out, which is harmless.
- `007861A0` exact. The `_Xlength_error` test fires exactly at count = 0x7FF..FE: a larger count wraps, so "equals" is right. The import at `008C2618` is confirmed.
- `00790160` exact. The sixth and seventh arguments are at entry+0x30 and +0x38. The three 32-entry arrays are at `rsp+0x130`, `+0x30` and `+0xB0`. The bounds are unsigned and are not checked against 32, as stated.
- `007A1A50` exact. The eight exact-match cases on `B+0x20` are right.
- `007D1A10` exact. "Keeping it 1" means the body stores 1. That is a wording nuance only (see the note).
- `00834D50` exact. The three calls land on z, y, x in call order.
- `00835000` and `00847980` exact.
- `00848960` exact. The predecessor search loops with no -1 stop, as the row says.
- `00848C30` exact. The "stack byte" is the low byte of the `rcx` home slot, reused as a pointer.
- `0084A740` exact. The lane test covers x/y/z only. A 32-bit `or` drops lane 3.
- `00857970` exact. The result object also gets a zero qword at `+0x50` and a zero dword at `+0x68`. The row's field list leaves these out, but the list does not claim to be complete.
- Anchors: all 60 sit strictly inside their bodies and decode as recorded. Each anchor does what its row says.

### SWE2-AUDIT-SPEC: required narrowing (exact text)

`00785C90`: replace the ending "; stores the sixth-argument dword at `+0x28`, AND ~0x300 if bit `0x800` of dword `+0x24` (re-read) is set; returns `r`, else 0" with "; then, on every path, stores the sixth-argument dword at `+0x28`, AND ~0x300 if bit `0x800` of dword `+0x24` (re-read) is set, and returns `r` when `f` has bit `0x1`, else 0".

After the edit, re-run the applier. It re-renders this record's block, and the anchors are unchanged.

*Optional precision note (non-blocking):* `007D1A10`'s "else keeping it 1 (NaN included)" describes a store of 1. The byte is set to 1 whatever non-zero value it held, so "else setting it to 1" would be exact.

### SWE2-AUDIT-SPEC: engine_explained crediting (ruling opus-ee-rulings-1003 section 2, FRONTIER 1e64e4042)

Measured at HEAD with `progress.py`'s own helpers (`index_only_headings`, `strip_index_only`, `evidence_bearing`, `family_rule_inputs`, `cite_credits`, `doc_credits`):
- The appendix is the only `ee_index_only` heading, and stripping it removes the appendix. This block is its own `##` section outside it.
- The page is evidence-bearing, and the overlap with in-scope families is 0.
- **All 12 rows credit engine_explained, and only through this block.**
  - Without the block, the stripped page credits 0 of the 12, and no other page credits any of them.
  - Every crediting cite is a row's interior anchor.
  - The bodies are 575–659 B.
  - `check_dispositions.evaluate`: 12 of 12 are in `a_set` and `explained_set`, and 0 are in `frontier_set`.
- The narrowing changes text only, so the crediting is unaffected.

### SWE2-AUDIT-SPEC: the scoped-row ruling (auditspec-ruling-scoped-ee-row-1003, at HEAD)

No row opens with `Scope:` or carries `scoped row: set-exact`. With `scoped_out`, `doc_credits` puts all 12 in the plain set and 0 in the scoped set. These are full exact rows, so the ruling sets no condition here.

- Limits: static evidence only. The cloud draft and OPUS's re-read are not independent review; this record is. Eleven rows were read in a forked context of the same reviewer (FABLE). The reviewer re-read `00785C90` in full and confirmed the defect. The scratch scripts and dumps (`rd.py`, `dump7_7.txt`, `c7.txt`) are not committed.
