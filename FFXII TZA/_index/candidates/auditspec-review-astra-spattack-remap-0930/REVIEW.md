# SWE2-AUDIT-SPEC review of ASTRA's special-action word remap (spattack-native-word-remap at 1f6569546): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Producer:
ASTRA. Reviewed: commit `1f6569546`, packet
[`spattack-native-word-remap/`](../../../_experiments/evidence/spattack-native-word-remap/README.md) (37-member
manifest; checker `prove-spattack-word-roundtrip.py`, controls `prerequisite-controls/`). Measured at HEAD `9b6c5bc93`.
Static, certified image (sha256 `73461d089620…21f8` asserted by every script below). The render-executor half of the
same commit, and the earlier class20 / bit30 / FST reviews, are out of scope.

| request | record | commit | verdict |
|---|---|---|---|
| ASTRA-REQ-SPEC-SPATTACK-REMAP-0930 | `_index/candidates/auditspec-review-astra-spattack-remap-0930/` | `1f6569546` | ACCEPT |

The board row was already DONE `verdict:ACCEPT` with no tracked record. This is the tracked record. It was done again
from the image and does not rely on that checkpoint. The verdict is the same: **ACCEPT**. Four precision points follow;
none of them changes a claim.

**Re-run.** Summary in [rerun_summary.txt](rerun_summary.txt).
- The checker, run to a fresh [rerun_result.json](rerun_result.json), is **byte-identical** to
  `spattack-word-roundtrip-result-01.json`.
- `exercise-spattack-prerequisites.py` was run into a scratch directory outside the repo. The positive exits 0 with a
  result. `missing_wrapper_completion`, `failed_upstream_role` and `missing_required_input` each exit 1 with no result.
  The positive result differs from the committed one only in `driver_sha256`, because the adapted checker has a
  different path literal.
- All seven capture drivers were re-run to scratch outputs. Each is **identical** to its committed raw JSON.
- All 37 manifest members match their bytes and sha256. The `reg_tracking.py` pin (`5fcc6484…`) equals the current
  kit file.
- FAILS 0. Package dir clean after the re-runs: yes for git (`git status --porcelain` is empty). One side effect:
  re-running the capture drivers **created** the gitignored
  `spattack-native-word-remap/__pycache__/capture-index-path.cpython-314.pyc`. It is not tracked, and I did not remove it.

**Re-derived independently** ([sp_indep.py](sp_indep.py) / [sp_indep.out](sp_indep.out), pefile + capstone, own
scans; 130 PASS, FAILS 0).
- *Producer subtraction.* `0030DB70` stores to the dword `022C2178` only at `0030DC98`, and two paths reach that store:
  - **Record path.** It runs when `002FFCF0` returns 0 and the word is not F2/F3/F4; those three leave through
    `00300BC0` and return 1 without the store. It computes `movzx eax,cx` / `sub eax,0xd0` at `0030DBDA`, and
    `or eax,-1` when the word is FFFF.
  - **NULL-record path.** It computes `lea eax,[rbx-0xd0]` at `0030DC7B`, or -1.

  A third encoder, `003068D4` in `003067C2..00306A9A`, does the same (`sub eax,0xd0` at `003068CA`, FFFF → -1).
- *Reader.* `00309C00` has `cmp eax,-1` / `jne`. On -1 it returns 0. Otherwise it stores to `[rdx]`, then
  `00309C22` re-arms the cell to -1 and it returns 1. It has no `.pdata` row, and neither does `0030D720`, the other
  -1 writer (`0030D722`).
- *Adapter.* `00348870` pops two integers. The **first** goes to EDX, the second to ECX. `0030EEA0` does
  `mov ebx,edx` / `cmp edx,-1` / `je` → `mov ebx,0xffff`; otherwise `add bx,ax` with ax = 0xD0, a 16-bit add. Then
  `movzx r8d,bx` → `call 0030CFB0`. Before that call there are two exits: a NULL from `0031B7E0` returns -1, and
  `[022C2170] != 4` returns -2. `0030CFB0` takes `movzx ebx,r8w`. `0030D070` stores the word at `0030D14F`
  (`mov word [rcx+0x1c], r10w`).
- *Arithmetic.* My own model of those instructions, run over all 65536 words for each of the three encoders, gives
  the same result every time:
  - Only CF and FFFF are reader-unavailable.
  - No available word changes on decode.
  - With the reader ignored, the composed round trip changes only CF, into FFFF.
  - 511..534 queue as 303..326 and decode unchanged.
  - Word 0 queues -208, which is not -1, so it passes and decodes back to 0.
- *Writer set by direct reference.* An image-wide sweep for any operand that **overlaps** the cell, in rip-relative,
  image-base-relative and absolute form, finds exactly 5 instructions:
  - `003068D4` (w), `00309C00` (r), `00309C22` (w -1), `0030D722` (w -1), `0030DC98` (w);
  - no stored VA64 or RVA32 of the cell anywhere.

  Two base pointers are formed at `022C2170`, at `0030D832` and `00313267`. Their uses index at `+0x22` and above
  and do not reach the cell for a non-negative index. The index signs are not bounded here. So this is a
  direct-reference census, not an alias closure, which matches the packet's own limit.
- *Callers.* `00309C00` has two E8 callers, `0034838A` (inside `00348330`) and `002D6175`, and no jcc caller.
  `0030EEA0` has one caller, `00348893`. `0030CFB0` has two: `00304E24`, fed by `00387090` →
  `movzx r8d,ax`, and `0030EF00`. `00348870` and `00348330` are stored as VA64 in `.data` (`01EF2A80` /
  `01EF2A60`).

**Precision** (non-blocking; the packet's claims stay true):
1. The CF / FFFF collision is a property of every direct writer, not only `0030DB70`'s ordinary branch. The NULL-record
   branch and `003068D4` encode the same way.
2. The reader **consumes** the value: `00309C22` writes -1 after a successful read. A second caller, `002D6175`,
   calls it with stack out-pointers outside the script path, so it can drain the cell before the script reads it.
   This lives inside the packet's "unchanged transfer / natural queue state" premise.
3. `00348870` passes the first of **two** popped integers as the id. `0030EEA0` can also return early (-1 / -2) before
   the remapped word reaches `0030CFB0`. That is covered by the stated "readiness OPEN".
4. `0030CFB0`'s own `(id-0xD0) <= 0x21` test (`0030D025`) is the likely source of the refuted "0..33" hypothesis. It
   applies only under flag `0x40000000`, where it chooses the `022C2158` bit-2 once path. That belongs to the
   separate bit30 review, not to this remap.

**Controls.** [rv_controls.py](rv_controls.py) / [rv_controls.out](rv_controls.out): the packet checker, unchanged
except for the same W/ROOT literal the packet's exercise script uses.
- A mnemonic-only change (`0030EEB2` add → sub) is refused by the witness table.
- A self-consistent byte change (`0030DBDA` imm D0 → CF, with the span sha rebuilt) is refused by the image
  comparison ("original span differs").
- So the checker really reads the image, and the witness and byte layers are both sensitive.
- **The failed01 defect.** The real failed capture `invalid-output-writer-01/inner-capture.json` has no `00309C00`
  span.
  - Fed as-is, it is refused ("capture invocation incomplete/changed").
  - With `wrapper_complete: true` and the current driver hash added, it is **accepted** (exit 0).

  So the checker trusts the flag and the driver hash; the leaf fix lives in the capture driver's pre-capture
  `{309c00, 309c22}` check. No semantic claim depends on writer02, because the reader bytes come from the
  queue-reader capture, which is why this is non-blocking. It does mean `missing_wrapper_completion` tests the
  flag, not the missing leaf. The package's three prerequisite controls are sensitive to the defects they name.

**Citations checked.**
- The README's anchors `0030DB70`/`0030DC98`, `00309C00`, `00348870`, `0030EEA0`, `0030CFB0` (R8w), `0030D070`
  (slot+1C), `00387090` (9F / actor+714), and `0030D722`/`0030D758` in `0030D720` were each opened; each supports its
  sentence.
- The failed01 history is preserved as described: STATUS INVALID_WRAPPER_CONTROL, and the driver diff is exactly the
  leaf check plus `wrapper_complete`.

**Runtime routing.** The packet routes nothing live. Its next step (`002FFCF0` and the committed producers' authored
input domain) is static. The unchanged-transfer premise (script variable written through `[rdx]` at `00309C13`, later
popped by `00267E10`) is also **statically settleable** by reading the interpreter's store and pop path. Only natural
selection and queue state need authored data or a run.

**Correction wording.** None needed. Optional sentence for ASTRA's README, after "FFFF itself also means unavailable":
> The same encoding is used by the NULL-record branch (`0030DC7B`) and by `003068D4`. `00309C00` consumes the cell
> (re-arms -1 at `00309C22`) and has a second caller, `002D6175`, outside the script path.

**Limits kept** (as ASTRA states them): the interpreter transfer is a premise. Producer admission, command / AI /
authored selection, natural queue and actor state, metadata / IO / owner submission, indirect aliases and the whole of
OV-42 / OV-21 stay OPEN. The 65536 calculations are static arithmetic, not code executions.
