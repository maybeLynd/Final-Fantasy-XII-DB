# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-vtable-method-index-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-VTABLE-METHOD-INDEX-EE-1003-06258` · Package: `_index/candidates/opus-vtable-method-index-ee-1003/` · Page: `00-Engine-Core-Runtime/Object-Model/vtable-method-index.md` (block committed in b0c7c5a57)

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 40 rows hold clause by clause against the certified image. No narrowing is required. One optional precision note (row `007DA970`, the unordered case) is given below. It does not block.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 40 functions, 160 anchors`, `ALREADY`, `FAILS 0` (exit 0). This matches the committed `interior_applier.out`. The page's working copy carries a peer's uncommitted 87-line append *after* this block (`git diff`: one hunk at +5269, insertions only). The block is the one committed in b0c7c5a57, and `ALREADY` confirms it renders `rows.json` byte for byte.
- `rows.json`: 40 rows, 160 anchors; rejected 0, skipped 0, missing 274, corrections 2 (`00786110`, `007DA970`). These match the README.
- Image: `rvlib.Img` (sha256 73461d08…, base 0x00120000), full bodies decoded with capstone (size from the page's size column, equal to the `.pdata` extent for every row). Every rip target's section was resolved: the statics, guards, TLS index, `01F3BA68` and `02EAF39C` are `.data` (mutable), and the rows treat them as loaded or stored cells, never as constants. `008C20B8` / `008C20C0` are `.rdata` IAT cells, and their import-name entries read `EnterCriticalSection` / `LeaveCriticalSection`.

### SWE2-AUDIT-SPEC: the 32 thread-safe-static rows (mechanical, with a control)

Rows `005C3C10` `005C3DB0` `005C4020` `005C40B0` `005C4250` `005C4360` `005C4770` `005C4800` `005C4890` `005C4920` `005C4A40` `005C4AD0` `005C4B60` `00603DB0` `00603FE0` `00604100` `00604190` `0063B660` `0063B6F0` `0063B800` `006AC860` `006AC8F0` `006AC980` `006AF450` `006B2680` `006B2710` `006B27A0` `006B2830` `006B28C0` `006B5B30` `006C03A0` `0079CB60` share one sentence form. A reviewer-written checker (independent of `interior_ingest.py`, scratch only) parsed each sentence and derived every value from the bytes:
- layout: static S, the qwords S / S+8 / S+0x10, and the guard = S+0x18;
- the TLS epoch read: `mov ecx, dword [02EAED3C]`, `gs:[0x58]`, `mov edx, 4`, `mov eax, [rdx+rcx]`;
- exactly one `cmp dword [guard], eax`, with polarity checked: either `jle` skip with the init path as fallthrough, or `jg` to the init path. Both shapes occur. The init path is entered when the guard is greater than the epoch (signed). The row says "compared with" and makes no claim about direction, so this is correct;
- the first call is `008092FC` and the last is `0080929C`, each with `lea rcx, [guard]`, with `cmp dword [guard], -1` / `jne` between them;
- the value stored to each qword, traced through `rax`: a `lea` address or a call return, with or without `or rax, 1`. The third qword is a literal 0;
- every `ret` is preceded by `lea rax, [S]`, and nothing in the body writes any other rip cell.

Result: **32 / 32 OK**. Control: three swapped values were injected into the sentences (a wrong second address, a wrong callee `00630180` -> `006301F0`, and a dropped `OR 1` on a call return). The checker flagged exactly those 3 rows, so it is sensitive to a swapped value. Spot-read by hand: `005C3C10` (jle shape), `005C4020` (jg shape, two addresses), `006B2680` (call-return OR 1).

### SWE2-AUDIT-SPEC: the 8 bespoke rows (read by hand)

- `0077E020` exact. `00727440(rcx)`, then `js` -> `0077E09A`, which is past the `mov eax, 0x80004005`, so the callee's own negative result is returned. `0076BE10(qword [rcx+0x238], rcx+0xCC)`, then `js` -> 0x80004005. `movsxd` count `[rcx+0xDC]` with `jle` (signed); `rdx` = qword `[rcx+0x4B8]` + 0xA0, step 0x108, entry = qword `[rdx]`, `cmp dword [rax+0x44], 0` / `je` -> 0x80004005 at the first zero. Falling out of the loop returns 0.
- `00780BB0` exact. Slot +8 of qword `[rcx+0x38]` is called with no null test, then qword `[rcx+0x90]` is set to 0. A 4-iteration loop (`edi` = 4) over `[rcx+0x48]`..`[rcx+0x60]` and then `[rcx+0x98]`: each non-null pointer gets slot +8 and is nulled. The body ends with `jmp 00727410` with `rcx` = this.
- `00786110` exact, including OPUS's rewording. The null `[rcx+0xF0]` path returns 0. Slot +0x50 is called with `edx` = `esi` 0..9 (`cmp esi, 9` / `jle`, ten calls), and `cmovs ebx, eax` keeps the last negative result. The qword is re-read; when it is non-null, the body calls `006DA8A0(qword [01F3BA68], ptr-8)` and zeroes it. It returns `ebx`.
- `007DA970` holds, with the polarity right for ordered values: `comiss sum, limit` / `jb` -> store 1; fallthrough (not below) -> store the limit, byte 0. The sum is stored before the compare (`007DA997`). Each slot +0x40 call sits inside its byte branch. The second half uses `xmm6` (the saved `xmm1`) with `[+0x58]`/`[+0x5C]`/`[+0x68]`. It returns 0. *Optional precision note (non-blocking):* `jb` is also taken when the compare is unordered (a NaN sum or limit), and that path stores 1, while the sentence's "not below" could be read as covering NaN. The README states this; the row does not. If OPUS wants the row exact for NaN, the wording is: "and, when that sum is not below float `[rcx+0x2C]` (comiss, ordered), stores float `[rcx+0x2C]` there and stores 0 to the byte, otherwise (below or unordered) stores 1 to the byte".
- `007DFA70` exact. `EnterCriticalSection(rcx+8)` through `[008C20B8]`, then byte `[rcx+0x70]` = 1. The count call `007AECE0()` is made before the loop and again after every copy (`cmp esi, eax` / `jl`, signed). Qword `[rcx+0x68]` is reloaded on every step, with dword-for-dword copies to `rdx`. Then `LeaveCriticalSection` through `[008C20C0]`, and it returns 0.
- `00848880` exact. Signed bound dword `[rcx+0xC]`, re-read every step. Entry = qword `[rcx+0x18]` + i*0x20, passed as `rdx` to `rdx`-object slot +8. On `al` != 0, `rcx`-object slot +0x10 is called with (`[e]`, `[e+8]`, original `r8` in `r9`), then `dec dword [02EAF39C]` and `jmp` to the bound test without `inc ebx` / `add rsi`. On false the index advances.
- `0084A6B0` exact. `mov eax, [+0x5C]` / `add eax, [+0x1C]` / `jne` -> exit. `00841010` is called on `rcx+8` and `rcx+0x48`, then come the eleven stores at the stated offsets, widths and values (word `+0xDD` = 0x100, the qword pair `+0xB0`/`+0xBC` = 1, dword `+0xB8` = 0xA, none overlapping).
- `00858560` exact. `movaps` 16 bytes from `[rdx]`, `movdqa` to `[rcx+0x140]`. Signed bound dword `[rcx+0x124]`, re-read every step. Object = qword `[qword [rcx+0x130] + i*8]`. The body skips when dword `+0xF4` is 2 or 5, or when `test byte [+0x230], 1` is nonzero; otherwise it calls `00854110(object, rdx)`.
- Anchors: all 160 are strictly inside their bodies and decode to the recorded mnemonics (applier `FAILS 0`, confirmed by reading the listings above). Each anchor is an instruction that does what its row says, for example the `cmovs`, `addss`, `dec` and `movdqa` anchors.

### SWE2-AUDIT-SPEC: vtable and slot claims (RTTI)

For each of the 40 functions, every 8-aligned `.rdata` qword equal to its VA was found. The scan then walked back to the qword after a valid complete-object locator (signature 1, pSelf = its own RVA) and read the type descriptor name. **40 / 40 match the appendix's class and slot**, and every COL offset is 0. For example: `005C3C10` is slot 4 of the vtable at `00D34D28` (`PMethodCallerConcrete<PAnimatableComponent,float,unsigned int>`), `0077E020` is slot 2 of `CDepthOfField` (`00DABD60`), `00786110` is slot 11 of `IGPUSurface`, `007DA970` is slot 5 of `GranularPitchShift`, `007DFA70` is slot 3 of `CoreMasterVoice`, `00848880` is slot 11 of `btHashedOverlappingPairCache`, `0084A6B0` is slot 11 of `btDbvtBroadphase` (`.?AU`), and `00858560` is slot 16 of `btDiscreteDynamicsWorld`. Each function has exactly one vtable hit. `00780BB0` also has a second `.rdata` qword at `01DBB920`. It is not a vtable: no COL precedes it, and its neighbours are `FFFFFFFF`-keyed pairs in an EH/state-map table. Ownership therefore stays unambiguous.

### SWE2-AUDIT-SPEC: engine_explained crediting (ruling opus-ee-rulings-1003 section 2, FRONTIER 1e64e4042)

These were measured with `progress.py`'s own helpers (`index_only_headings`, `strip_index_only`, `evidence_bearing`, `family_rule_inputs`, `cite_credits`), with no reimplementation:
- The page declares `ee_index_only: ["Appendix — the 4,275 unambiguously-owned vtable methods"]`. The heading exists, and stripping it removes the appendix. The package's block is a separate `##` section, outside the index-only heading.
- The page is evidence-bearing. It declares no in-scope accepted family that contains any of the 40 (`family_rule_inputs` overlap 0), so the base rule applies.
- **All 40 credit engine_explained, and they credit only through this block.** The page with the block removed credits 0 of the 40. No other page credits any of them. Every crediting citation in the block is one of the row's interior anchors, not an entry cite. All 40 bodies are 128-134 B, so their appendix entry cites never earned the under-128 allowance, before or after the ruling.
- **The package is consistent with the ruling.** The ruling denies credit to index rows that give only an address and a classification. These rows state what each body does and anchor interior instructions; that is the "re-earning it honestly" route the ruling describes. The package claims no credit from the appendix. Its README claims that the 40 "now measure A", and `check_dispositions.evaluate` confirms this: 40 of the 40 are in `a_set` and `explained_set`, none in `frontier_set`.
- The 32 template rows are not "explained-once family" rows under ruling section 1. Each row restates the whole shape with its own static, guard, values and anchors, and the page declares no family over them. Their per-member values were in any case derived from the image here, with a swapped-value control (above).

- Limits: static evidence only. The cloud draft and OPUS's re-read are not independent review; this record is. The reviewer's scripts live in a private scratch folder and are not committed.
