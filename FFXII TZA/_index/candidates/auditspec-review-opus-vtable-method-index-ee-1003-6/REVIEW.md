# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-vtable-method-index-ee-1003-6)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · at HEAD `f54822cb280713ac81cf91fc9ddb3756b11bbcea` · Task: `OPUS-REQ-AUDITSPEC-OPUS-VTABLE-METHOD-INDEX-EE-1003-6-F0B86` · Package: `_index/candidates/opus-vtable-method-index-ee-1003-6/` · Page: `00-Engine-Core-Runtime/Object-Model/vtable-method-index.md` (block "... cloud-drafted, opus-vtable-method-index-ee-1003-6)", committed in 51ad88762; page unchanged from there to HEAD)

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 16 rows hold clause by clause against the certified image. One optional precision note is given below; it does not block.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply` and printed `VERIFY 16 functions, 80 anchors`, `ALREADY`, `FAILS 0`, exit 0. This is identical to the committed `interior_applier.out`, and all 16 texts are on the page verbatim.
- `rows.json` holds 16 rows and 80 anchors. The README states rejected 0, skipped 0, missing 44.
- Applier control: a scratch copy of the unmodified applier was run on a mutated `rows.json`.
  - Mutations: `00655F10`'s first anchor relabelled `nop`, `007DD040`'s last anchor moved to the entry, and a pipe added to `008521C0`.
  - Result: exactly those three `VERIFY FAIL` lines, `FAILS 3`, exit 1, and the page untouched.
- Pattern rows: none. Every row was read by hand.
- Image: `rvlib.Img` (sha-checked, base 0x00120000, section-aware). Every body was decoded to its true end, taking the larger of the stated size and the chained `.pdata` extent.
  - `007D1C80`: `.pdata` adds 37 bytes, a `nop` and then the body's jump table.
  - `007DE120`: `.pdata` adds 2 bytes, the second `00809728` stub.
  - `00692080` and `007DC4A0` are leaf bodies with no `.pdata`, and both end at `ret`.
- RTTI: 12 of 16 rows match the appendix's class and slot, each with one vtable hit.
  - `007DD040` is slot 1 of `HCAMixerVoice`'s secondary vtable (COL offset 8), as the appendix says.
  - `00655F10`, `00692080`, `0073BB50` and `008521C0` are not appendix methods. They have no `.rdata` qword and are named on the page only at their entries.

### SWE2-AUDIT-SPEC: the 16 rows (read by hand, to the end of each body)

- `007D1C80` exact. Its jump table sits at image base + `0x6B1EB0` and has nine entries, which map exactly to the arms the row describes:

  | Case | Target | What the arm does |
  |---|---|---|
  | 0 | `007D1CFE` | store-and-zero arm |
  | 1-4 | `007D1D28` / `007D1D52` / `007D1D7C` / `007D1DA6` | tail-call `007D1080` / `007D0EA0` / `007D0DD0` / `007D1280` |
  | 5-7 | `007D1DD0` / `007D1E0C` / `007D1E48` | tail-call `007D1140` / `007D0F60` / `007D1330` |
  | 8 | `007D1E84` | `call 007D0D30`, then return |
- `0083DE00` exact. The constant picked by `[o+0xF4]` is:
  - 1 -> `00D11570`
  - 2 -> `008C5F90`
  - 3 -> `01CCE8B0`
  - 5 -> `00D63910`
  - 4 or any other value -> `008C5F80`
- `008521C0` exact. The compares are ordered, so a NaN distance does not count.
- `007DE120` exact. When `SetThreadPriority` fails, the body repeats from `GetLastError` with no -1 store.
- `00725AA0` and `00726360` (GPU-device wrappers) exact. The log gates, line numbers, strings and callee argument lists all match the derived stack slots.
- `00655F10`, `00692080`, `0073BB50`, `007D9EA0`, `007DC4A0`, `007DD040`, `00832E90`, `008330A0`, `00833830` and `00833FB0` exact, clause by clause, including signed versus unsigned bounds, NaN paths and null tests.
- Anchors: all 80 are strictly inside their bodies and decode as recorded. Each anchor does what its row says.

*Optional precision note (non-blocking).* `007DC4A0` says "else (NaN included) keeps the byte at 1", but the body stores 1 (`007DC4DA`, and the same in each arm), whatever non-zero value the byte held. "Sets the byte to 1" would be exact.

### SWE2-AUDIT-SPEC: engine_explained crediting (ruling opus-ee-rulings-1003 section 2, FRONTIER 1e64e4042)

Measured at HEAD with `progress.py`'s own helpers: `index_only_headings`, `strip_index_only`, `evidence_bearing`, `family_rule_inputs`, `cite_credits` and `doc_credits`.
- The appendix is the only `ee_index_only` heading, and stripping it removes the appendix. This block is its own `##` section outside it.
- The page is evidence-bearing, and the in-scope family overlap is 0.
- **All 16 rows credit engine_explained, and only through this block.**
  - Without the block, the stripped page credits 0 of the 16, and no other page credits any of them.
  - Every crediting cite is a row's interior anchor.
  - Bodies are 449-573 B, so the small-body allowance never applies.
  - `check_dispositions.evaluate` puts 16 of 16 in `a_set` and `explained_set`, and 0 in `frontier_set`.

### SWE2-AUDIT-SPEC: the scoped-row ruling (auditspec-ruling-scoped-ee-row-1003, at HEAD)

No row opens with `Scope:` or carries `scoped row: set-exact`. `doc_credits` with `scoped_out` (condition 5) puts all 16 in the plain set, with 0 scoped. These are full exact rows, so the ruling sets no condition here.

- Limits: static evidence only. The cloud draft and OPUS's re-read are not independent review; this record is. The rows were read in a forked context of the same reviewer (FABLE). The scratch scripts and dumps (`rd.py`, `p6.txt`) are not committed.
