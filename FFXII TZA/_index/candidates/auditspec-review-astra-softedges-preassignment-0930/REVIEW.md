# SWE2-AUDIT-SPEC review of ASTRA's PhyreText preclear/cleanup proof (phyretext-preassignment-cleanup at 451897b9d): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75), 2026-09-30. Static only, on image
`73461D08…21F8`. No native or live run. The field (`5bbbe5528`), member (`7a524fda9`) and key (`a50f9dea4`)
acceptances stay separate.

| request | reviewed task | commit | verdict |
|---|---|---|---|
| ASTRA-REQ-SPEC-SOFTEDGES-PREASSIGNMENT-0930 | ASTRA-PUBLISH-SOFTEDGES-PREASSIGNMENT-0930 | `451897b9d` | ACCEPT |

**Verdict in one line.** Every clause of the conditional proof re-derives from the bytes. The reducer's refusal controls
are sensitive, and this review added a positive twin and four mutations of its own. There is one precision note about
where the preclear value's zero comes from; it is optional wording and does not change the result.

**Clause by clause** (from [`pa_indep.out`](pa_indep.out), [`pa_indep2.out`](pa_indep2.out), [`pa_r13_flow.out`](pa_r13_flow.out), [`pa_pdata.out`](pa_pdata.out)):
- *`006372A0` arg6 → descriptor +0x78; `006373D0` arg2 → +0x70.* `006372A0` is the 8-byte leaf `lea rax, [02CF8270]; ret`.
  `006373D0` returns `01F2E330` on its normal path (`006373F7`); a thread-safe-static init path (`008092FC`) sits in
  front of it, and its lazy-init effects are correctly left unproved. In `005EEB20`: `005EEB95 mov rbx, rax` (the
  `006372A0` result) goes to `[rsp+0x28]` = callee arg6, and `005EEBA4 mov rdx, rax` (the `006373D0` result) = arg2.
  Then `005EEBC3 call 00632D80`, which does `00632DD1 mov rax, [rsp+0x30]` (arg6) / `00632DD6 mov [rcx+0x70], rdx` /
  `00632DDA mov [rcx+0x78], rax`. **The corrected attribution holds.** The named descriptor is `rcx` =
  `02CEA460` (`005EEB61`); arg7 = `r15d` = 0 is stored to F0 (`00632E4F`), and `00632E62` zeroes F4/F8.
- *Leaf boundaries.* `00632D80`..`00632E71` (`ret` at `00632E70`, `int3` from `00632E71`), `0063E410`..`0063E487`
  (`ret` at `0063E486`) and the 8-byte `006372A0`. None of the three has a `.pdata` entry; I checked 35,713 entries.
  `0063E410` has exactly 3 raw E8/E9/jcc callers (`00632F2F`, `006391FA`, `0063D60F`), and `rawcalls.json` agrees.
- *Root exclusion.* `0063E410` zeroes F4, then walks `rax` = self → `[rax+0x78]`, adding each F0 until `rax` ==
  `r9` = `02CF8270` (`0063E425`/`0063E430`). With own F0 = 0 and the parent still the root, it adds 0 and stops
  **before** reading the root's F0, so F4 = 0. As the packet says, this is not a later-writer or rebind invariance claim.
- *The modular identity.* `0059CC76 mov ecx, [r14+0x48]` / `0059CC7E sub ecx, [[r14+0x18]+0xF4]` /
  `0059CC84 movsxd rdx, ecx` / `0059CC8C add rdx, [rsp+0x38]`. So the preclear address is object +
  sext32((off − F4) mod 2^32). With off = 8, sext32((8 − F4) mod 2^32) = 8 exactly when (8 − F4) ≡ 8 (mod 2^32),
  which is exactly when the F4 dword is 0. This is exact, with no sign-extension edge, because 8 is inside the positive
  int32 range. A 140,000-value grid plus the int32 boundary values finds 0 counterexamples.
- *`0059CD14` preclear, then `0060EFE0` NULL read.* The callback path: `0059CD1D mov rdx, [rsp+0x38]` (the same
  supplied object) → `0059CD25 call [rax+0x40]` → `0060F3D0` (it moves `rdx`/`r8`/`r9d` into `rcx`/`rdx`/`r8d` and does
  `jmp rax` with rax = `[rcx+0x70]`, see [`pa_60f3d0.out`](pa_60f3d0.out)) → `0060F280` (its only rip reference is the `lea` at `005EEDEF` in the registrar) → `call 0060EFE0`.
  That reads `[rcx+8]` at `0060F012`. So the preclear slot and the read slot are the same `object+8` exactly when F4 = 0.
- *Preclear value.* A must-be-zero dataflow over all 508 instructions of `0059C700` (none unreached; the control state
  right after `0059CB2A` is TOP) gives **r13 = 0 at `0059CD14` on every path**, assuming callees preserve r13 (Win64
  ABI). See the precision note.
- *Cleanup.* A NULL source means old == new, so the cleanup is skipped (`0060F019`). With a non-NULL source, bit 31 of
  the old count set (borrowed) skips it (`0060F01F`..`0060F026`). With bit 31 clear (owned), the code calls
  `005F03A0(NULL, count & 0x7FFFFFFF)`, whose `test rcx, rcx` / `je 005F0407` goes straight to `ret`. The setter then
  stores the pointer and `count | 0x80000000` (`0060F031`..`0060F040`). None of this can release the overwritten old pointer.
- *Negative boundary.* `0060EFF8 test r8d, r8d` / `jns` / `mov eax, 5` / `ret` runs before `[rcx+8]` is read or any
  store, and `0060F289 xor eax, eax` makes `0060F280` return 0. The preclear therefore stands, the count is unchanged and
  the callback returns 0, under the stated premises.

**Re-run.** `reduce-softedges-preassignment-cleanup.py` was run to a fresh output
([`rerun_reduce.out`](rerun_reduce.out), [`rerun_result.json`](rerun_result.json)). All 111 of 111 leaf fields are
equal to `softedges-preassignment-cleanup-result-02.json`, and the packet stayed clean.

**Controls** ([`pa_controls.py`](pa_controls.py) / [`pa_controls.out`](pa_controls.out), on copies of result-02's
`source_pins` in this directory):
- The unmutated copy succeeds (`baseline`). ASTRA's own positive run used the canonical packet rather than its copies,
  so this closes that gap: the copy set is complete.
- ASTRA's three refusals reproduce: `missing-parent-getter`, `false-parent-store` at `0x632dda` and
  `false-borrowed-flag` at `0x60f01f`.
- My four mutations are each refused at the exact pc: `jns`→`js` at `0060EFFB`, `movsxd`→`mov` at `0059CC84`,
  `cmp rax, r9`→`r8` at `0063E430`, and the `0059CC38` zeroing changed to `or`. The reducer pins what its conclusions
  rest on.
- The procedural `checked_run` controls (failed-with-output, zero-exit-without-output, stale output) are wrapper
  fixtures (`python -c pass`). They were read, not re-run, because they write into immutable paths.

**Precision note (optional wording for ASTRA).** Not every path reaches `0059CD14` through `0059CC38`:
`0059CB1C jmp 0059CC3B` enters one instruction after it. On that edge r13 is still the function's zero register from
`0059C73F xor r13d, r13d`, so the conclusion holds. Suggested README text: "r13 is zero at `59CD14` on every path —
from `59CC38`, or from `59C73F` via `59CB1C→59CC3B`". Suggested reducer pin: `need(patch, 0x59c73f, 'xor', 'r13d, r13d')`,
if that span is added to the capture.

**Limits kept.** No natural initialization, no rebind history, no successful load, no non-NULL cleanup behaviour, no
alias or leak claim, and no completeness of constructor, caller or writer, exactly as the request's contract forbids.

This verdict is the reviewer's; the incorporation owner decides consumption.
