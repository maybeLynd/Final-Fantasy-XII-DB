# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-vtable-method-index-ee-1003-2)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · at HEAD `f54822cb280713ac81cf91fc9ddb3756b11bbcea` · Task: `OPUS-REQ-AUDITSPEC-OPUS-VTABLE-METHOD-INDEX-EE-1003-2-29A22` · Package: `_index/candidates/opus-vtable-method-index-ee-1003-2/` · Page: `00-Engine-Core-Runtime/Object-Model/vtable-method-index.md` (block "Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-vtable-method-index-ee-1003-2)", committed in 51ad88762; page unchanged from there to HEAD)

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 80 rows hold clause by clause against the certified image. No row needs narrowing.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply`: `VERIFY 80 functions, 347 anchors`, `ALREADY`, `FAILS 0`, exit 0. Identical to the committed `interior_applier.out`. The applier is byte-identical to the first package's. The page block renders `rows.json` byte for byte, and all 80 row texts appear on the page verbatim.
- `rows.json`: 80 rows, 347 anchors, 80 distinct functions. README: rejected 0, skipped 0, missing 190.
- Applier control (planted defect): an unmodified scratch copy of this package's applier (only its DB root pinned) was run on a scratch `rows.json` carrying three mutations: `005C4140`'s first anchor re-labelled `nop`, `00725830`'s last anchor moved onto the entry, and a pipe added to `0087FCF0`'s sentence. It printed exactly three `VERIFY FAIL` lines for those rows and `FAILS 3`, exited 1, and left the page untouched (mtime unchanged, `git status` clean).
- Image: `rvlib.Img` (sha-checked shipping `FFXII_TZA.exe`, base 0x00120000, section-aware offsets). Every body was decoded from its entry to its true end, the larger of the stated size and the chained `.pdata` extent.
  - 78 bodies: the stated size equals the `.pdata` extent.
  - `007252A0` is a leaf with no `.pdata`. It ends at `ret` `00725330`, followed by `int3` padding.
  - `007895F0`: the chained `.pdata` runs 9 bytes past the stated 148 B. That tail is the epilogue (`add rsp`, `pop rdi`, `ret`), and the body was read through it.
- RTTI: for each function, every 8-aligned `.rdata` qword equal to its VA was walked back to a complete-object locator. 78 of 80 match the appendix's class and slot, each with exactly one vtable hit and COL offset 0.
  - `0072F7D0` and `0084CA50` are not appendix methods. They have no `.rdata` qword at all. The page names each only at its entry, outside the appendix: `0072F7D0` in the entry-only-large interior table (line 2812) and `0084CA50` in a slot row (line 2803).

### SWE2-AUDIT-SPEC: pattern rows (mechanical, with controls)

Reviewer-written checkers, kept in scratch and independent of `interior_ingest.py`, check 57 rows in three forms.

- **36 thread-safe-static rows**: `005C4140` `005C49B0` `00603850` `006038F0` `00603990` `00603A30` `00603AD0` `00603B70` `00603C10` `00604070` `00604320` `00653950` `006539E0` `00653A70` `00670B30` `00670C60` `00679070` `0067F140` `0067F1D0` `006A2DD0` `006A3060` `006A30F0` `006A8FA0` `006A90B0` `006AD4F0` `006AF340` `006B5810` `006B5AA0` `006B5BC0` `006C01C0` `006C0430` `006C76D0` `0079C8C0` `0079C9D0` `00873AD0` `00873B60`. The first review's checker was generalised to any static size and any number of qwords, then parsed each sentence and derived every value from the bytes:
  - Layout: the static `S`, qwords at `S+8k`, the guard at `S` + size. Twenty-nine statics are 0x18 B with 3 qwords; seven are 0x20 B with 4 qwords.
  - The TLS epoch read: dword `02EAED3C`, `gs:[0x58]`, `edx` = 4, then `[rdx+rcx]`.
  - Exactly one `cmp [guard], eax`. All 36 use `jle` with the init path as the fallthrough.
  - `lea rcx,[guard]` before both `008092FC` and `0080929C`, with `cmp [guard],-1` / `jne` between them.
  - Each qword's stored value traced through `rax` (a `lea` address or a call return, with or without `OR 1`). The last qword is a literal 0.
  - No other rip write and no other non-stack write. Every `ret` is preceded by `lea rax,[S]`. Anchors decode as recorded.
  - All statics, guards and values are `.data` cells.
  - **Result: 36 / 36 OK.**
  - Control: five sentence mutations were planted:
    - a wrong callee (`0062FF50` -> `0062FF60`);
    - a dropped `OR 1` on an address;
    - the closing call swapped for the opening one;
    - the guard shifted by +8;
    - an `OR 1` added to a bare call return.
  - The checker flagged exactly those five rows. An anchor re-labelled from `cmp` was also refused.
- **16 deleting-destructor rows**: `007A98E0` `007AB080` `007AE600` `007AE6A0` `007B1420` `007B2B30` `007B4D60` `007B54B0` `007B5C50` `007B61C0` `007B7110` `007B7F30` `007BA990` `007BB8B0` `007BBE50` `007C1530`.
- **5 callback-table rows**: `006B3120` `006B31B0` `006B3240` `006B32D0` `006B3360`.
- A shape checker covers both of these forms:
  - Each body is normalised: rip targets, direct call targets, memory displacements and `edx` immediates are abstracted; bit-test, compare and return immediates stay literal; branch targets are made entry-relative. Each body must equal a hand-read exemplar (`007A98E0` and `006B3120`, both read by hand to the `ret`).
  - The sentence is then regenerated from the member's own bytes: vtable, buffer offset, slot, `00210EB0`, zeroed qword range and dword, base vtable, `007AD450` / `0016D6A0` and size, or the compared callee for the callback rows. The regenerated sentence must equal the row character for character.
  - **Result: 21 / 21 OK.** Both destructor layouts occur: buffer `+0x10` with dword `+0xC` (14 rows), and buffer `+8` with dword `+0x2C` (`007AB080`, `007BA990`).
  - Text controls: `007B54B0` was given dword `+0x2C`, and `006B3240`'s "returns 1" became "returns 0". Both were refused.
  - Byte controls on a patched image: `007B54B0`'s `test dil,4` was made `test dil,2`, and `006B3240`'s `mov eax,1` was made `mov eax,2`. Both were refused.

### SWE2-AUDIT-SPEC: the 23 one-off rows (read by hand, to the end of each body)

- `00724940` exact. The 0x28-byte copy is done with two `movups` to `02EA1960` / `02EA1970` and a `movsd` to `02EA1980`. `00724830` is called with the incoming registers. The swap is guarded by `rdx`, `[rdx+0x18]` and `!= [rcx+0x30]`. The old object's `+0x10` call sits behind its own null test (`0072499A`). The `+8` call is made on the new object. The return is `cmovs` of `00723440`'s result.
- `00724DB0` exact. The stack rectangle is (x, y, x+w, y+h); slot `+0x168` is called with `edx` = 1. On the null path, own slots `+0x80` and `+0x90` are called with `rsp+0x20`. The return is 0, with the cookie checked.
- `007252A0` exact. `jl` is signed, so `edx` >= 0x14 returns 0x80070057. The indexed dword store covers 0..0x13; a negative `edx` takes the ten qword stores `+0xA1C`..`+0xA64`.
- `00725830` exact. Byte order is 2, 1, 0, 3 into `rsp+0x30..0x3C`. `00D11104` = 0.0039215689 (1/255). `r9` holds the vtable at the call. The fifth argument is entry+0x28.
- `0072F7D0` exact. Both log gates are unsigned `jb 1`. The line numbers are 0x13E5 / 0x13E9, and the strings at `00DA5A88` / `00DA5AD0` / `00D9F030` / `00D9F060` are as described.
- `00783A10` exact. `r9b` is read from `[rsp+0x38]` after `push`+`sub 0x20` (entry+0x10), a slot the body never writes. The shift is `sar 5`. The three zeroes are inside the non-null branch. `00809950(rcx, 0x20)` runs on bit 0x1.
- `00785FD0` exact. The `+0x20` call passes the fifth-argument byte at `[rsp+0x20]` and returns early on `js`. Slot `+0x180` is called on `[[rcx+0x18]+0x30]`, which is null when `+0x18` is null, with (`[rcx+0x38]`, `n`, 0, `rdx`, `b*[rcx+0xB8]`, 0).
- `007895F0` exact. `cmp eax,2` / `jge` is signed. State 5 stores to `rdx` when it is non-null. The `+0x50` loop runs while the result is 1, `js` returns the result, slot `+0x28` gets `edx` = 0, and the function returns 0. The epilogue past the stated size was read.
- `007C6C70` exact. `jb 3` is unsigned. `01CEBBA8` = 1.0. The loop is three iterations at stride 0x40 from `+0x150`, followed by `+0x5B0` / `+0x5B4` / `+0x5B8`.
- `007D1430` exact. The key chain is 0x200 -> `+0x38`, 0x201 -> 1.0 / `+0x68`, 0x202 -> `+0x98`, 0x203 -> `cvtdq2ps [rcx+0x18]`, and any other key returns -1.
- `007D8180` exact. The vtables are `01CB7698` at `+0` and `01CB76E8` at `+8`. `007AD450([rcx+0x48])` is called with no null test. The base vtables are `01CB7058` / `01CB4658` / `01CB4680`, and the size is 0x60.
- `007D9690` exact. `ucomiss` / `jne` sends an unordered compare to the `+0x24` path, as stated. 0x401 writes and returns -1.
- `007DD510` exact. The imports at `008C2198` / `008C2330` / `008C20E0` are read from the IAT as SetEvent / ResumeThread / WaitForSingleObject. The `ResumeThread` loop reloads `[rbx+0x10]`. The size is 0x48.
- `007DF9B0` exact. It is a two-iteration loop over `+0x60` / `+0x68` with a null skip and no nulling. `DeleteCriticalSection` is IAT `008C20D0`. The size is 0x78.
- `007E0070` exact. `EnterCriticalSection` / `LeaveCriticalSection` are `008C20B8` / `008C20C0`. Byte `+0xC8` is set to 1. Qword `[rcx+0xC0]` is reloaded on every step, and `007AECE0` is re-called after every copy (`jl`, signed).
- `007E0880` exact. `test [rcx+0x80], 0xFFFFFFFB` is the "no bit other than 0x4" test. The index is `cols*j + i`, with `cols` re-read inside the inner loop.
- `007E25A0` exact. This is the mirror copy, from `[rdx + 4*idx]` into `[rcx+0x10C + 4*idx]`.
- `0083F7B0` exact. `jp` sends an unordered compare to the non-zero path. The `+8` call is on `[rcx+0xC8]` with `rdx` = `[o+0xC8]`. All eight `0083E7E0` arguments match the stack slots. The return is `al` = 1.
- `0084A220` exact. The `00841530` target follows from `[node+0x58]` == 2. The unlink handles both the prev and next sides, with the head at `[rcx+0x88+8*movsxd]`. Slot `+0x18` is called with (node, `r8`), then `0085E710(node)`, then byte `+0xDE` = 1.
- `0084CA50` exact. The qword store at `+0x14` writes float 1.0 there and 0 at `+0x18`. The fifth argument is at entry+0x28. All other stores are as stated.
- `00857E70` exact. Bound and array are re-read every step (`jl`, signed), and `test byte [+0xE8],3` selects the objects. The three calls carry `xmm1` (and `r8` = obj+0x50 for the third).
- `008581E0` exact. The search is a linear scan with a signed bound. The swap writes `entry[i]` = `entry[last]` and `entry[last]` = old `entry[i]`, then `dec [rcx+0x104]`. `00853B20` is called once and tail-jumped once.
- `0087FCF0` exact. The counter writes `+0xEC` only when `test byte +0xE8,3` is zero. `+0xF0` = -1 and `+0x110` = 1.0 are set on all. The tail call is `jmp 0087FB60` with (`rcx`, old `r8`, old `rdx`).
- Anchors: all 347 are strictly inside their bodies and decode as recorded (applier). On the listings, each anchor is an instruction that does what its row says.

### SWE2-AUDIT-SPEC: engine_explained crediting (ruling opus-ee-rulings-1003 section 2, FRONTIER 1e64e4042)

This was measured with `progress.py`'s own helpers at HEAD (`index_only_headings`, `strip_index_only`, `evidence_bearing`, `family_rule_inputs`, `cite_credits`, `doc_credits`), with no reimplementation:
- The page declares `ee_index_only: ["Appendix — the 4,275 unambiguously-owned vtable methods"]`. Stripping it removes the appendix. This package's block is its own `##` section, present in the stripped text, and outside the index-only heading.
- The page is evidence-bearing. No page declares an in-scope accepted family containing any of the 80 (`family_rule_inputs` overlap 0), so the base rule applies.
- **All 80 credit engine_explained, and only through this block.**
  - The stripped page with this block removed credits 0 of the 80, and no other page credits any of them.
  - Every crediting citation inside the block is one of the row's interior anchors, never an entry cite.
  - No body is under 128 B (134-151 B), so no appendix entry cite ever earned the small-body allowance.
  - `check_dispositions.evaluate` places all 80 in `a_set` and `explained_set`, and none in `frontier_set`. The README's "all 80 now measure A" is confirmed.
- The package is consistent with the ruling. It claims no credit from the appendix. Its rows state what each body does and anchor interior instructions, which is the route the ruling leaves open.
- The template rows are not "explained-once family" rows under ruling section 1. Each row restates the whole shape with its own values and anchors, and the page declares no family over them.

### SWE2-AUDIT-SPEC: the scoped-row ruling (auditspec-ruling-scoped-ee-row-1003, at HEAD)

The ruling's five conditions bind only rows that open with `Scope:` and carry the marker `scoped row: set-exact`. None of the 80 rows does, and the marker is absent from the page. `doc_credits` with `scoped_out` (condition 5, `progress.py` at HEAD) places all 80 in the plain set: template 0, scoped 0. These are full exact rows, not scoped rows, so the ruling sets no further condition here.

- Limits: static evidence only. The cloud draft and OPUS's re-read are not independent review; this record is. The reviewer's checkers (generalised thread-safe-static checker, shape-group checker with text and byte controls, applier control, RTTI walk, crediting script) live in a private scratch folder and are not committed.
