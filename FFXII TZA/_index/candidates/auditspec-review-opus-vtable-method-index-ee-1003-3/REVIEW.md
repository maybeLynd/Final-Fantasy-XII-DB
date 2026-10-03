# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-vtable-method-index-ee-1003-3)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · at HEAD `f54822cb280713ac81cf91fc9ddb3756b11bbcea` · Task: `OPUS-REQ-AUDITSPEC-OPUS-VTABLE-METHOD-INDEX-EE-1003-3-01D23` · Package: `_index/candidates/opus-vtable-method-index-ee-1003-3/` · Page: `00-Engine-Core-Runtime/Object-Model/vtable-method-index.md` (block "... cloud-drafted, opus-vtable-method-index-ee-1003-3)", committed in 51ad88762; page unchanged from there to HEAD)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

54 of the 60 rows hold exactly. Six rows need a one-phrase rewording. None of the six rewordings changes what a row anchors or what it credits.
- `00627750` misstates a call's arguments.
- Five record-copy rows list incomplete "not copied" gaps.

The exact replacement text is given below.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply`: `VERIFY 60 functions, 293 anchors`, `ALREADY`, `FAILS 0`, exit 0. This is identical to the committed `interior_applier.out`. The applier is byte-identical to the first package's, and all 60 texts are on the page verbatim.
- `rows.json`: 60 rows, 293 anchors. README: rejected 0, skipped 0, missing 210.
- Applier control: a scratch copy of the unmodified applier ran on a mutated `rows.json`:
  - `005C1E70`'s first anchor was re-labelled `nop`.
  - `007A9820`'s last anchor was moved onto the entry.
  - A pipe was added to `00858A00`'s text.

  The applier printed exactly those three `VERIFY FAIL` lines and `FAILS 3`, exited 1, and left the page untouched.
- Image: `rvlib.Img` (sha-checked, base 0x00120000, section-aware). Every body was decoded to its true end, which is the larger of the stated size and the chained `.pdata` extent.
  - `007DEEF0` and `007E8890`: the `.pdata` adds one `int3` after the trailing `call 00809728` stub, and both stubs were read.
  - `00842040` is a leaf with no `.pdata` and ends at `ret`.
- RTTI: 57 of 60 match the appendix's class and slot, each with one vtable hit.
  - `007DEEF0` sits in `WASAPIDevice`'s secondary vtable (COL offset 16, slot 6), as the appendix says.
  - `005DC0E0`, `00627750` and `00637650` are not appendix methods. No `.rdata` qword holds them; the page names them only at their entry outside the appendix.
  - `00781B70` and `007DA1C0` each have one extra `.rdata` qword (`01DC1FA0`, `01D5D110`). Neither is preceded by a COL, and both sit among `FFFFFFFF`-keyed EH state pairs, so they are not vtables. Ownership stays unambiguous.

### SWE2-AUDIT-SPEC: pattern rows (mechanical, with controls)

A shape checker normalises each body: rip and call targets, memory displacements and `edx` immediates are abstracted, while test, compare and return immediates stay literal. Each body must equal a hand-read exemplar. The checker then regenerates the row's sentence from the member's own bytes and requires character equality.

- **5 vector-deleting-destructor rows**: `007A9820` `007AB120` `007BAA30` `007C1290` `007DC8B0`.
  - There are two layouts, each with its own exemplar read by hand to every `ret`: 0x30-byte elements (`007A9820`: `lea [r8+r8*2]`, `shl 4`) and 0x18-byte elements (`007AB120`: `lea [rcx+rax*8]`).
  - The element size comes from the backward store stride. The base vtable comes from the two `lea`s. The heap size is `count*k+8` on the array path and `k` on the scalar path.
  - **Result: 5 / 5 OK.**
- **4 list-to-array rows**: `005C38B0` `00603770` `0062DBD0` `006709D0`.
  - The exemplar is `005C38B0`, read by hand. It walks `[node+8]`, uses `cmp ebx,[rdx]`, and calls `0017D260(count*8, 8)`. A null result returns 0xD, and a non-null one is zero-filled by `rep stosq`. The bit-31 test (`shr 0x1f` / `not` / `test 1`) means "clear". The body then calls `00584730`, stores the count dword, and runs the fill loop.
  - **Result: 4 / 4 OK** (the head static and the next offset are read per member).
- Controls (text): `007C1290`'s `count*0x30+8` was changed to `count*0x18+8`. The checker refused it, along with the controls planted in the other packages' groups.
- **5 record-copy rows**: `0068C260` `0068CBE0` `0068D370` `0068DD80` `0068E940`.
  - Their normalised bodies are identical. The store map read from `0068C260`'s bytes is: byte `+8`; dwords `+0xC`, `+0x10`; qword `+0x18`; dwords `+0x20`..`+0x58`; dword `+0x60`; qword `+0x68`; dwords `+0x70`..`+0x78`; qword `+0x80`. Each is copied from the same offset of the callee's record.
  - The positive lists in the five rows are exact. The gap list is not (see the narrowing).

### SWE2-AUDIT-SPEC: the one-off rows (read by hand, to the end of each body)

- `005C1E70`, `005C1F20`, `005C2100`, `0066FC50` are exact. Each passes (`rdx`, -1, 0) to `00811470` and (`rdx`, -2) to `00811130`, then gets the object from its own getter (`005BCD20` / `005BCD20` / `005BDDC0` / `0066E7D0`).
  - A null object returns `rax` = 0.
  - Otherwise the body calls slot `+8` with (o, `esi`). A non-null result calls `00684080(rdx, result, <static>)` with the static `02CAD440` / `02CADC50` / `02CAD840` / `02CB6B80`. A null result calls `0080F420(rdx,1)` and `00810620(rdx)`.
  - The body returns 1.
- `005DC0E0` exact. `00808FE4` is called with (rcx+8, 0x18, 8, `005DC1B0`, `0016D6A0`). The stores are in order `+0xF0`, `+0xE8`, `+0xF8`, qword `+0xFC` = 0x400000, `+0xF4`, then dword `+0x100` = 0x100000. The final state is therefore bytes `+0xE8`..`+0xFB` = 0, `+0xFC` = 0x400000 and `+0x100` = 0x100000, as stated.
- `00627750`: the control flow and every store hold. **The call clause is wrong.** At `0062778D` the body calls `0061CF20` with `rcx` and with `edx` still holding its own incoming `edx`. `edx` is unmodified since entry (`mov ebp,edx`; `cmp edx,[rbx]`). `0061CF20` reads it: it returns null for 0, the inline slot `rcx+8` for 1, and else `0017D260(edx*0x28, 8)` with the entries zeroed. The row writes the call as `0061CF20(rcx)`.
- `00637650` exact. The guard `02CF950C` is checked with `jg` into the init path, between `008092FC` and `0080929C`.
  - The stores are `01F2E5A0` = `00D311B0` and three qwords = `01F2E5A8`.
  - Dword `01F2E5C0` and qword `01F2E5C8` are 0. `01F2E5D0` = `00D58BF0` ("PUInt32"). `01F2E5D8` / `01F2E5DC` = 4. `01F2E5E0` / `01F2E5E8` = 0.
  - The body then calls `00808B90(008AFE50)`.
- `0068C260`, `0068CBE0`, `0068D370`, `0068DD80`, `0068E940`: the callee (`00699B30` / `006998F0` / `00699290` / `00699050` / `00698E10`) and the positive copy list are exact. The "not copied" parenthetical is incomplete (see the narrowing).
- `00722060` exact. It runs a two-iteration loop over `+0xF0` / `+0xF8`:
  - When `[obj+8]` is non-null, it calls `006DA8A0([01F3BA68], [obj+8]-8)` and zeroes the qword.
  - It then calls `006DA8A0(obj)` and zeroes the slot.
  - It calls `00720220` and then `00727450`, and returns via `cmovs`.
- `00724C10` exact. `mov eax, dword` zero-extends before the 64-bit `cvtsi2ss`. The six floats are packed at `rsp+0x20`. Slot `+0x160` is called with `edx` = 1.
- `00724CD0` exact. The slot is `+0x2F8`, called with (`&dword 1`, `rsp+0x28`). `00D99774` = 0.49999. The four stores use `addss` + `cvttss2si` in the order `[0x28]`, `[0x2C]`, `[0x30]`, `[0x34]` -> `+0`..`+0xC`. `[0x38]` and `[0x3C]` go to `+0x10` / `+0x14`.
- `00725760` exact. `bt edx,0x1c` gates the first part. Its loop over `t+0x130` is bounded by unsigned `jb`, re-read each pass, with a null skip. The `+0x1A8` call carries (`[t+0x170]`, `edx&3`, `xmm3`, fifth-argument byte).
- `007258C0` exact. `00861EC0` is called twice (0x80 and 0x100). The slot `+0x90` arguments are (0, 0x20, `rsp+0xB0`, `rsp+0x30`, `rsp+0x30`).
- `007259D0` exact. The two log gates are `jb 1`, with line 0x1FD6. A null `ib` returns 0x8000FFFF. The three slot calls carry the stated arguments, and `[rcx+0x30]` is re-read for each.
- `00726C30` and `00726D00` exact. The fifth and sixth arguments are at entry+0x28 and +0x30. A null result returns 0x80004005 after the error logs.
- `00726E30` exact. `edx-3 <= 3` is unsigned. The flag bits are 0x4000 -> 1, bit 16 -> 2, 0x20 -> bits 28 and 17, `cl` sign -> bit 29, 0x40 -> bit 30, and bit 15 -> bit 19. The bitmap `0x8280049` over `r8d-0x48` gives exactly 0x48, 0x4B, 0x4E, 0x5B, 0x5D and 0x63, plus 0x1D. `0071A600` sets bit 18.
- `00781B70` exact. It does `sub [o+8],1` / `jne`, followed by slot `+0x20` and `006DA8A0`, zeroing both slots. The zero stores also include dwords `+0x38` / `+0x44`, which the stated qword zeroes already cover.
- `00785EE0` exact. Dword `+0x28` ends 0 on every path; both `cmovne` select 0. Byte `+0x58` bits 0x20 and 0x40 give 1 and 2 in `+0x24`. Slot `+0x38` is called on `rdx` with `rcx+0x38`.
- `00786D00` exact. The allocation is `006DA880([01F3BA68], n*8+8, 00DAD4A0, 0x6E1, 0)`. Without a null test before the loop, the store goes to `[[rcx+0xF0] + 8i]`, which is re-read each step; the loop bound is unsigned `jb`.
- `00789C00` exact. The loop is `k` = 1..len-1 (signed). It reads `rdx[len-k]` and writes `data[k]`, re-reading length and data pointer after each write. Byte 0 is untouched.
- `0078F9F0` exact. The count is `sar 3` of the span, compared unsigned (`jb`). The function returns `i+1`, or 0 via `or -1` / `inc`.
- `007AE740` exact. The list is walked with `next` read before each slot `+0` call (`edx` = 1). The zeroes are as stated, and the size is 0x20.
- `007CA370` exact. The guard uses `jb 3` (unsigned) and bit 3 of byte `+0xA`. `xmm1` is unchanged before the first call. The fifth-argument float is at entry+0x28.
- `007D1970`, `007D9B70`, `007D9DF0`, `007DA1C0`, `007DAA00` exact. The keys and records are as stated, and every ramp uses `ucomiss` / `jne`, so an unordered compare takes the end path. `008C5B2C` = 0.001.
- `007D98F0` exact. The constants are `01CEBC78` = 2π, `01CEBC50` = π, and `01CEBDA0` = the float sign mask. `00861FAA` is the `expf` thunk. `01F41D20` is in `.data` and holds 2.0833e-05 in the file. A whole-image sweep finds a writer at `007D959C` (`movss [01F41D20], xmm1`), so "stored to elsewhere at run time" holds.
- `007DC970` exact. It is the buffer destructor shape, with vtables `01CB7B10` / `01CB7B00` and size 0x30.
- `007DEEF0` and `007E8890` exact. The `0019C5D0` calls, the newline and terminator handling, `OutputDebugStringA` (IAT `008C2120`) and `007A5570(0/2, buffer)` are as stated. The trailing `00809728` stub past the stated size was read. *Optional precision note:* the terminator bound is `movsxd` + unsigned `jae`, so a negative index also calls `00809728`. "(unsigned)" would make that exact.
- `007F1220` exact. The fifth argument is at entry+0x28. `[r8+0x18]` 0 / 1 selects the stores, and any other value stores nothing. The result is returned on every path.
- `007F1EC0` exact. `00D11570` = (1,1,1,0), `00D560A0` = 3.0 ×4 and `00D22600` = 0.5 ×4. The scale is `0.5 r (3 - s r r)` applied to the vector, and lane 3 is restored from `+0x10C`.
- `007F24F0` exact. The copy list is as stated. The loop runs to the re-read count (signed), copying 12-byte sources to 16-byte destinations, with the fourth dword = 1.0.
- `00832DD0` exact. Entries are walked from the last to the first at stride 0x60. Inside the match branch, `+0x68` is incremented a second time. `008332A0` gets (`rcx+0x18`, i, re-read count - 1). The final tail call is `jmp [rax+0x78]`.
- `00833A60` exact. It uses two `cdq` / `idiv` signed remainders. The scaled xyz goes to `[r8]` and `[r9]` with w = 0.
- `00834C70` exact. `0x55555556` gives signed mod 3. `008FCC84` = 0.04 and `01CCD6F8` = 1/12. The output order is `[r8]` = (c1+c2)k, `+4` = (c0+c2)k, `+8` = (c0+c1)k.
- `00837E20` exact. Results a, b, c land in `xmm7`, `xmm6`, `xmm0`, giving `[r8]` = (x-c, y-b, z-a, 0) and `[r9]` with sums.
- `00842040` exact. Each of the three points uses `comiss` / `jbe`, so only a greater (ordered) dot replaces `+0x60` and copies the point to `+0x10`.
- `00847C00` exact. The index logic picks the first on ties. The row is `[rcx + (i+5)*16]`, and the function returns `rdx`.
- `00848270` exact. It does `inc [02EAF398]` and swaps by signed `jle`. The key is (larger<<16)|smaller, mixed by the shift / `not` / add / xor chain, masked by `[rcx+0x10]-1`, and bounded by signed `jge [rcx+0x3C]`. Chains follow `[rcx+0x48]` / `[rcx+0x68]` until -1 over 0x20-byte records.
- `0084A5D0` exact. Both `008497D0` calls pass (base, root, `rdx`, `r8`, `r9+0x10`, `r9+0x20`, float `[r9+0x2C]`, 5th, 6th, `&saved r9`). The fifth and sixth arguments are at entry+0x28 and +0x30.
- `00855A50` exact. The count is read once via `movsxd`. The "both in {2,5}" test is as stated. The final call is the tail jump `jmp [rax+0x10]` with `rdx` = `rcx`.
- `00857C10` exact. Each call carries the step in `xmm1` where stated, and all ten calls and stores appear in the stated order.
- `00858A00` exact. Both loops re-read their bound (signed). The tests are bit 0x2 of byte `+0x104`, and `+0xF4` not in {2, 5}.
- Anchors: all 293 are strictly inside their bodies and decode as recorded, and each does what its row says.

### SWE2-AUDIT-SPEC: required narrowing (exact text)

1. `00627750`: replace "`n` = `0061CF20(rcx)`" with "`n` = `0061CF20(rcx, edx)`". The callee sizes and places the new storage by that count (`0061CF20`: 0 -> null, 1 -> the inline slot `rcx+8`, more -> `0017D260(edx*0x28, 8)` with zeroed entries).
2. `0068C260`, `0068CBE0`, `0068D370`, `0068DD80`, `0068E940`: replace "(bytes `+0` to `+7`, `+9` to `+0xB` and dwords `+0x5C` / `+0x64` are not copied)" with "(bytes `+0` to `+7`, `+9` to `+0xB` and dwords `+0x14`, `+0x5C`, `+0x64` and `+0x7C` are not copied)". The store map has no write to `+0x14`..`+0x17` or to `+0x7C`..`+0x7F`. The current list reads as the complement, but it omits these two dwords.

After the rewording, re-run the applier; it re-renders this record's block (`REWRITTEN`), and the anchors are unchanged.

### SWE2-AUDIT-SPEC: engine_explained crediting (ruling opus-ee-rulings-1003 section 2, FRONTIER 1e64e4042)

Measured with `progress.py`'s own helpers at HEAD (`index_only_headings`, `strip_index_only`, `evidence_bearing`, `family_rule_inputs`, `cite_credits`, `doc_credits`):
- `ee_index_only` names the appendix heading, and stripping it removes the appendix. This block is its own `##` section, outside it.
- The page is evidence-bearing. The in-scope family overlap with the 60 is 0, so the base rule applies.
- **All 60 credit engine_explained, and only through this block.**
  - Without the block, the stripped page credits 0 of the 60, and no other page credits any of them.
  - Every crediting cite in the block is a row's interior anchor.
  - Bodies are 151-222 B, so no small-body allowance applies.
  - `check_dispositions.evaluate` puts all 60 in `a_set` and `explained_set`, and none in `frontier_set`.
- The narrowing above changes sentence text only. It does not change an anchor, so the crediting is unaffected.

### SWE2-AUDIT-SPEC: the scoped-row ruling (auditspec-ruling-scoped-ee-row-1003, at HEAD)

No row opens with `Scope:`, and none carries `scoped row: set-exact`. `doc_credits` with `scoped_out` (condition 5) places all 60 in the plain set, with 0 scoped. These are full exact rows, so the ruling sets no condition here.

- Limits: static evidence only. The cloud draft and OPUS's re-read are not independent review; this record is. The reviewer's checkers (shape-group checker with text and byte controls, applier control, store-map extraction, cell-writer sweep, RTTI walk, crediting script) are in a private scratch folder and are not committed.
