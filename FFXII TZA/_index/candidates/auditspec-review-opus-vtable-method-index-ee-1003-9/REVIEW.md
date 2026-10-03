# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-vtable-method-index-ee-1003-9)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · at HEAD `f54822cb280713ac81cf91fc9ddb3756b11bbcea` · Task: `OPUS-REQ-AUDITSPEC-OPUS-VTABLE-METHOD-INDEX-EE-1003-9-9DAE0` · Package: `_index/candidates/opus-vtable-method-index-ee-1003-9/` · Page: `00-Engine-Core-Runtime/Object-Model/vtable-method-index.md` (block "... cloud-drafted, opus-vtable-method-index-ee-1003-9)", committed in 51ad88762; page unchanged from there to HEAD)

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 11 rows hold clause by clause against the certified image. No narrowing is required.

## SWE2-AUDIT-SPEC checks

- I re-ran `interior_applier.py` fresh without `--apply`. It printed `VERIFY 11 functions, 55 anchors`, `ALREADY` and `FAILS 0`, and exited 0. This is identical to the committed `interior_applier.out`. All 11 texts are on the page verbatim.
- `rows.json` holds 11 rows and 55 anchors. The README states rejected 1, skipped 1 and missing 48. The rejected and skipped drafts are not in `rows.json` and are not on the page.
- Applier control: I ran a scratch copy of the unmodified applier on a mutated `rows.json`:
  - `005DF890`'s first anchor relabelled `nop`;
  - `007D9200`'s last anchor moved to the entry;
  - a pipe added to `008473A0`.

  It reported exactly those three `VERIFY FAIL` lines and `FAILS 3`, exited 1, and left the page untouched.
- Pattern rows: none. Every row was read by hand. Two mechanical extractions support the hand reading: the 32 (key, value) pairs of `007D5F50`, and the direct-call census of `00608A40`.
- Image: `rvlib.Img` (sha-checked, base 0x00120000, section-aware). Every body was decoded to its true end. For all 11 bodies the stated size equals the chained `.pdata` extent.
- RTTI: 10 of the 11 match the appendix's class and slot, each with exactly one vtable hit. The `btOptimizedBvh::build` local classes `NodeTriangleCallback` / `QuantizedNodeTriangleCallback` match by their decorated names. `005DF890` is not an appendix method: it has no `.rdata` qword, and the page names it only at its entry (line 2779).

### SWE2-AUDIT-SPEC: the 11 rows (read by hand, to the end of each body)

Constants and thunks were confirmed in the image:
- `01CEBC78` = 2π and `00915624` = -2π.
- `01CEBC9C` = -1.0.
- `008C5F80` = (1,0,0,0).
- `01CCD870` / `01CCD880` = ±1e18 ×3, then 0.
- `01CCE8AC` = 1e18.
- `009002B0` = 0.002, `009002EC` = -0.001, and `008F3148` = -2.0.
- Thunks: `00861F14` is `sqrtf`, `00861EFC` `asinf`, `00861F02` `atan2f`, `00861F0E` `sinf`, `00861F08` `cosf`, and `00861FAA` `expf`.

Per row:
- `005DF890` exact. 3×0x80 + 0x10 = 0x190 bytes, and all eight k groups match.
- `00608A40` exact. The mechanical census counts 105 direct calls:
  - 39 to `006388C0` / `00639450`;
  - 5 `f()` calls;
  - 4 tail-gate calls;
  - 57 plain calls, the first to `005E6E70` and the last to `005E67C0`. None of them sets up an argument register.

  The 17 statics, their order, and both `OR` stores match.
- `0062E1C0` exact. The y/z rotation stack matrix is exactly the rows (1,0,0,0), (0,C,S,0), (0,-S,C,0) and (0,0,0,1).
- `0062E5A0` exact. The angle-wrap loops and the 2^27 claim are right. Above 2^27 the float spacing is 16, so adding 2π rounds back to the same value. The row-1 terms are right; they include multiplications by 0 that vanish for finite values.
- `007D5F50` exact. All 32 (key, value) pairs were extracted mechanically and match the list. This includes k = 0x1C re-using `+0x58`, and `+0x68` never being read.
- `007D9200` exact. "0.0 or NaN" follows the `ucomiss` / `jne` flag behaviour.
- `00832930` exact.
- `008355B0` exact. `w` at `rbp-0x2D` is confirmed never written.
- `00846C20` exact. Node bytes `+0x2C`–`+0x3F` are confirmed unwritten.
- `00846F70` exact.
- `008473A0` exact. The row index is (eax+5)×16 = 0x50 + 16×row.
- Anchors: all 55 are strictly inside their bodies and decode as recorded. Each anchor is an instruction that does what its row says.

### SWE2-AUDIT-SPEC: engine_explained crediting (ruling opus-ee-rulings-1003 section 2, FRONTIER 1e64e4042)

Measured at HEAD with `progress.py`'s own helpers (`index_only_headings`, `strip_index_only`, `evidence_bearing`, `family_rule_inputs`, `cite_credits` and `doc_credits`):
- The appendix is the only `ee_index_only` heading, and stripping it removes the appendix. This block is its own `##` section, outside it.
- The page is evidence-bearing, and its in-scope family overlap is 0.
- **All 11 credit engine_explained, and only through this block.**
  - The stripped page with the block removed credits 0 of the 11, and no other page credits any of them.
  - Every crediting cite is a row's interior anchor.
  - The bodies are 789–985 B.
  - `check_dispositions.evaluate` puts 11 of 11 in `a_set` and `explained_set`, and 0 in `frontier_set`.

### SWE2-AUDIT-SPEC: the scoped-row ruling (auditspec-ruling-scoped-ee-row-1003, at HEAD)

No row opens with `Scope:` or carries `scoped row: set-exact`. `doc_credits` with `scoped_out` puts all 11 in the plain set and 0 in the scoped set. These are full exact rows, not scoped rows, so the ruling sets no condition here. This holds even though these are the batch's largest bodies, because each row states its whole body, not a set.

- Limits: static evidence only. The cloud draft and OPUS's re-read are not independent review; this record is. The rows were read in a forked context of the same reviewer (FABLE). The scratch scripts and dumps (`rd.py`, `k7.py`, `dump7_9.txt`) are not committed.
