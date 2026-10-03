# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-vtable-method-index-ee-1003-4)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · at HEAD `f54822cb280713ac81cf91fc9ddb3756b11bbcea` · Task: `OPUS-REQ-AUDITSPEC-OPUS-VTABLE-METHOD-INDEX-EE-1003-4-91F99` · Package: `_index/candidates/opus-vtable-method-index-ee-1003-4/` · Page: `00-Engine-Core-Runtime/Object-Model/vtable-method-index.md` (block "... cloud-drafted, opus-vtable-method-index-ee-1003-4)", committed in 51ad88762; page unchanged from there to HEAD)

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 47 rows hold clause by clause against the certified image. One optional precision note is given below; it does not block.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 47 functions, 233 anchors`, `ALREADY` and `FAILS 0`, and exited 0. The output matches the committed `interior_applier.out`. All 47 texts are on the page verbatim.
- `rows.json` has 47 rows and 233 anchors. The README reports rejected 0, skipped 0, missing 223.
- Applier control: a scratch copy of the unmodified applier was run on a mutated `rows.json`.
  - Mutations: `006C0060`'s first anchor relabelled `nop`, `007D8F70`'s last anchor moved to the entry, and a pipe added to `0087FC00`'s text.
  - Result: exactly those three `VERIFY FAIL` lines, `FAILS 3`, exit 1, and the page untouched.
- Image: `rvlib.Img` (sha-checked, base 0x00120000, section-aware). Every body was decoded to its true end, the larger of the stated size and the chained `.pdata` extent. Bodies whose `.pdata` runs past the stated size:
  - `00719460` and `007E2AD0` end in one `int3`.
  - `007DF1F0` ends in the remainder of its third `call 00809728` stub plus `int3`. The stated 288 B ends inside that call.
  - In `007D8A70`, `007D8E40`, `007DB7A0` and `007DC1F0` the extra bytes are a `nop` followed by each body's own eight-entry jump table. Each table was read as data and every arm was followed.
- RTTI: 44 of 47 match the appendix's class and slot, each with one vtable hit.
  - `007DF1F0` is slot 8 of `WASAPIDevice`'s secondary vtable (COL offset 24), as the appendix says.
  - `00719460`, `0075E690` and `0075E7C0` are not appendix methods. They have no `.rdata` qword and are named on the page only at their entries outside the appendix.

### SWE2-AUDIT-SPEC: pattern rows (mechanical, with controls)

- **10 list-to-array rows**: `006C0060` `006C24C0` `006CD5B0` `006D6FF0` `006D9780` `006D9B70` `008761A0` `00876590` `008769A0` `00877160`.
  - The shape checker matches each normalised body against the hand-read exemplar `005C38B0` (package -3). The normalisation abstracts rip and call targets, displacements and `edx` immediates; test, compare and return immediates stay literal.
  - It then regenerates each sentence from the member's own bytes (head static, next offset `+8` or `+0x10`, `0017D260`, alignment, 0xD, `00584730`) and requires character equality.
  - **Result: 10 / 10 OK.** `006C0060` was also read by hand.
- Text controls: `006D9780`'s "node `+0x10`" was changed to "`+8`", and an anchor of `00876590` was relabelled. Both were refused.
- Byte control: on a patched image, `006C24C0`'s head rip displacement was moved by +8. The regenerated sentence no longer matched, and the row was refused.
- **2 matrix rows**, `007F10F0` and `007F1850`, were read by hand (below).

### SWE2-AUDIT-SPEC: the one-off rows (read by hand, to the end of each body)

- `00719460` exact.
  - `00715A00` is called as (incoming `rdx`, incoming `rcx`) on both empty paths. `007158B0` is called with (`rsp+0x30`, `[rcx+8]`, `[rcx]`+len, -1).
  - `00861EBA` is a `jmp [IAT]` thunk to `memcpy`. It is called with (data + signed `[rcx]`, `r8`, len).
  - The free is skipped for `02EA1720` and for null, and the function returns `rdx`.
- `007214A0` exact. "Changed across that call" compares `[rcx+0x28]` before and after `007273E0`. The first-use block stores `02EA1918`, four qwords at `01F3CB18` and nine at `02EA18C0`, and the `inc` is stored on every path. The `+0xA8` / `+0xB8` test is "both non-null -> 0".
- `007255E0` exact.
  - The range tests are `ja 0xF` and `jae 0x14` (unsigned).
  - When byte `01F3CBA9` is clear, the cache is reset to -1.
  - The early return 1 needs the byte set, `r9b` set and the cache equal.
  - The call condition is cache -1 OR a differing bit 0x3 OR a differing bit 0xC. `r9` = `rcx+0x460+8*state`.
  - The slot is `+0x50` for slots 0..0xF and `+0xD0` with slot-0x10 for 0x10..0x13. The cache is stored only when the byte is set.
- `0075CAD0` exact. The `+0x48` array has a null test and the `+0x40`-count array has none. The `+0x60` / `+0x80` pairs, the `+0x90` refcount pairs with `+0x70`, and the zeroes `+0x5C` / `+0xA4` are as stated. The body ends with `jmp 00727410`.
- `0075CC50` exact. Entries of `[rcx+0x48]` are null-tested, but the array itself is not. The `[rcx+0x50]` array is tested before its entries. Both arrays are freed as `-8`. The qword zeroes are `+0xA0`, `+0x3C` and `+0x58`, and the function returns with `cmovs`.
- `0075E690` and `0075E7C0` exact. Both walk the circular list from the sentinel's next (signed `jle` on `edx`, re-reading `[p+8]` per candidate).
  - The removal sequence is: slot `+0x20`(0), `006DA8A0(o)`, null `[p+8]`, free and null the payload, unlink both sides, `dec qword [rcx+0x40]`, then `00210EB0(node)`.
  - Iteration continues from the saved next, and the count is returned. `0075E7C0` loops once over its spilled `rdx`.
- `0075EC00` exact.
  - The first `sub [o+8],1` has no null test.
  - The "otherwise, when byte `[p]` is non-zero" loop repeats `sub`/`jne` until 0, then makes the two calls.
  - The sentinel is reset to self and `[rcx+0x40]` to 0. Every old node is freed with `00210EB0`, and the function returns with `cmovs`.
- `00780C70` exact. `00714560` is called after `007142F0`. The `[d+0x22248]` call comes before the re-tested free of `+0x80`. The zero list and the qword `+0xA8` = 2 are as stated.
- `007819F0` exact. Both slot `+0` calls are made with `rdx` = `[rcx+0x28]` and return on `js`. `+0x504` = 0x3E800000 (0.25). Over the 17-iteration loop, every pointer offset was mapped back to `+0x7C`, `+0x1D0`, `+0x214`, `+0x368`, `+0x3AC`, `+0x3F0`, `+0x434`, `+0x478`, `+0x4BC` (+4i) and `+0xC0` / `+0x258` (+16i).
- `00786410` exact. The cursor is spilled at `rsp+0x40` and re-read after each `007854D0`. The match flags give "any" when `rdx` is null or `r8d` is -1. `cmovs` keeps the last negative result. The walk stops when the cursor returns to the head.
- `00786DD0` exact. The `jbe 1` test is unsigned. The log gates are `01F3BA80` / `01F3BA8C`, the line is 0x71B, and the strings are `00DAD520` / `00DAD570`. The byte `+0xAC` and qword `+0xD8` clears sit inside the ">1" branch. The slot `+8` call and the nulling sit behind the null test, and the array is freed as `-8`.
- `007B1520` exact. Per element (reading the stride 0x30 backwards), the vtable `01CB4B08` is stored after `p` = `[element+0x10]` is read. The buffer release, the zeroes and the base `01CB4470` are as stated. The scalar path calls `007B14C0(rcx)` first.
- `007C6370` exact. The two-iteration loop applies the record test (`[rec]` >= 1 unsigned, bit 0x1 of `+0xA`) only to the second ramp, `+0x348`. The `+0x5E4` multiply uses the same test.
- `007D1840` exact.
  - 0x200 picks 5 vs 4 by `comiss` / `ja`; NaN gives 4.
  - 0x201 replaces a 0.0 or NaN value by 1.0 before `divss`.
  - 0x203 calls `007D16C0(rcx, cvttss2si, time)`.
  - The `ucomiss time` tail call runs for every `edx`.
- `007D8A70` exact. The jump table at `0x6B8B8C` + image base maps keys 0..7 to `007D8AA8`, `007D8ACF`, `007D8AE9`, `007D8AEF`, `007D8AF8`, `007D8B1D`, `007D8B42`, `007D8B5E`. Keys 0x102/0x103 share the `logf` arm. `00861F98` is a `jmp [IAT]` thunk to `logf`. `01CB7784` = 8.685889 and `008C5F78` = 1000.
- `007D8E40` exact. The table at `0x6B8F44` maps keys to `007D8E79`, `007D8EA8`, `007D8ECA`, `007D8EDD`, `007D8EF3`, `007D8F04`, `007D8F18`, `007D8F24`. `01CB7780` = 0.1151293. 0x106/0x107 store `cvttss2si` and call own `+0x40`. Keys out of range do nothing.
- `007D8F70` exact. The keys 0x100..0x107 and their values are as stated, followed by slot `+0x40` and a return of 0.
- `007DB7A0` exact. The table at `0x6BB89C` maps keys 0x1000..0x1007, in key order, to the arms for records `+0x490`..`+0x5E0`.
- `007DC0E0` exact. It makes eight `007CA560` calls with the stated targets (0, 1.0 ×3, 0.2, 0.08, 2.0, 2000), passing the incoming `xmm1` as time.
- `007DC1F0` exact. The table at `0x6BC318` maps keys to arms in the stated record order. The clamps use `comiss` / `jb` (below or NaN -> lower bound), then `minss` with 1.0, `008C5F6C` = 0.1 or `009146F8` = 20000. 0x1006 uses `maxss value,0`, so NaN -> 0.
- `007DF1F0` exact. Each of the three strings has its own newline and terminator handling and its own `00809728` stub. Any other `edx` returns 0.
- `007E2AD0` exact. `k` = 1/2 selects `007CFF90` / `007D07A0`, `al` == 0 returns -1, and otherwise the body stores `[rdx+0x20]` at `[rcx+0x50]` and returns `007D09B0(rcx, rdx)`. The default arm formats with `r9d` = `k` and returns -1.
- `007F10F0` and `007F1850` exact. The fifth and sixth arguments are at entry+0x28 and +0x30. The `unpcklps` packing gives (d60, d70, d80, d90) in order. The `007F0320` argument slots are as stated. The second store is `+0x120` and `+0x110` respectively, and the float argument is `+0x130` and `+0x120`.
- `007F1DD0` exact. The vector is `+0x100`, and `008F8180` = 10.0. The two 1.0 stores follow the call.
- `00832810` exact. The stack matrix rows are `008C5F80`, `008C5F90`, `008C5FB0` and 0, with `a` = `rsp+0x30` and `b` = `rsp+0x20`. `01CEBB70` = 0.5, `01CEBC08` = 2.0 and `009146E8` = 12.0. The output order matches.
- `00832CD0` exact. The `+0x40` / `+0x50` initial vectors are as stated. Per entry, slot `+8` is called on `[entry+0x40]` with (entry, lo, hi), and the per-component `comiss` / `jbe` means NaN changes nothing.
- `00835CE0` and `00837F00` exact. `01CCD4E0` = 2^-46 and `01CEBC9C` = -1.0. `00861F14` is the `sqrtf` thunk. `00835CE0`'s early return is `ucomiss` with `jp` going on.
- `008553F0` and `00855520` exact. Growth happens when count == capacity and the new capacity (2×count, or 1) exceeds capacity (signed). The copy skips per entry when `n` is null, and the free needs the owner byte. The final store is skipped at a null address. `00855520`'s `r8b` tail is as stated.
- `00857820` exact. Every test calls slot `+0x18` afresh. The loop runs from `n`-1 down (`js`). The final branch re-tests `w` and the slot `+0x58` result (non-zero) before the pointer-array loop.
- `0085C3E0` and `0085CDC0` exact. The stack arguments are at entry+0x28..+0x50, with widths dword, qword, dword, qword, qword, qword. The eighth argument is entry+0x40. Both return `xorps` 0.0.
- `0085DCE0` exact. The eighth argument is at entry+0x40. The pass count `[a+0x14]` is re-read each pass. The record is `[rcx+0x18]` + 0xC0k. `0085AC50` vs `0085A900` is chosen by bit 0x100 of `[a+0x3C]`.
- `0087FC00` exact. The root search halves the path: each visited entry's parent is replaced by its grandparent, and the cursor moves to that grandparent. The stores are `+0xEC` = root, entry `+4` = the array index, and `+0xF0` = -1. Flagged objects get -1 / -2.
- Anchors: all 233 are strictly inside their bodies and decode as recorded. Each one does what its row says.

*Optional precision note (non-blocking).* In `007DF1F0` and `007E2AD0`, "an index of 0x100 or more calls `00809728`" is implemented as `movsxd` plus an unsigned `jae`, so a negative index also calls the stub. Adding "(unsigned)" would make the clause exact for a negative `0019C5D0` result.

### SWE2-AUDIT-SPEC: engine_explained crediting (ruling opus-ee-rulings-1003 section 2, FRONTIER 1e64e4042)

Measured with `progress.py`'s own helpers at HEAD: `index_only_headings`, `strip_index_only`, `evidence_bearing`, `family_rule_inputs`, `cite_credits` and `doc_credits`.
- The appendix is the only `ee_index_only` heading, and stripping it removes the appendix. This block is its own `##` section outside it.
- The page is evidence-bearing. The in-scope family overlap with the 47 is 0.
- **All 47 credit engine_explained, and only through this block.**
  - Without the block, the stripped page credits 0 of the 47, and no other page credits any of them.
  - Every crediting cite is a row's interior anchor.
  - Bodies are 222–317 B, so the small-body allowance does not apply.
  - `check_dispositions.evaluate` puts 47 of 47 in `a_set` and `explained_set`, and 0 in `frontier_set`.

### SWE2-AUDIT-SPEC: the scoped-row ruling (auditspec-ruling-scoped-ee-row-1003, at HEAD)

No row opens with `Scope:`, and none carries `scoped row: set-exact`. With `scoped_out` (condition 5), `doc_credits` puts all 47 in the plain set and 0 in the scoped set. These are full exact rows, so the ruling sets no condition here.

- Limits: this is static evidence only. The cloud draft and OPUS's re-read are not independent review; this record is. The reviewer's checkers are in a private scratch folder and are not committed: the shape-group checker with its text and byte controls, the applier control, the jump-table reader, the RTTI walk and the crediting script.
