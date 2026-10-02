# FABLE review: ASTRA filecache-read-zero-view

- **Packet:** [filecache-read-zero-view README](../../../_experiments/evidence/filecache-read-zero-view/README.md)
- **Producer commit:** `4a818c6d3`. The manifest sha256 begins `43e05ee2e8590e06` and equals the committed manifest.
  All 55 members hash as listed. The packet's two range hashes (Read, and the retained IsOpen) equal the certified
  image's bytes. The retained IsOpen manifest is byte-identical to `filecache-open-sentinel`'s committed manifest
  (`7479a4f8…`), which FABLE reviews alongside this one ([review](../fable-review-astra-filecache-open-sentinel-1002/REVIEW.md),
  ACCEPT). `metadata-correction-01.json` is present.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT.** Every claim re-derives at the bytes:
  - the 92-byte body and its five paths;
  - the full-width buffer and handle tests, the low-32 size guard and the signed cache guard;
  - the full zero returned on both no-call arms;
  - the import's identity, and the stack count that replaces the API return.

  The reviewer adds three facts that the packet leaves implicit: the count slot is pre-zeroed, the fifth argument is
  zero, and rdx and r8 are forwarded untouched. They do not change any claim.

## Method

[rv_read.py](rv_read.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is copied
unchanged from the route2-commit-key review (sha256 `69f9bc40be32abcc32b1`). It also uses the reviewer's own Unicorn
2.1.4 sandbox, which runs the shipped bytes over a private copy of the image's sections. Every callee and every
import (through the IAT) is a recording stub. The stubs and their premises are described in the zero-handle review.
The script does not import ASTRA's `prove.py`, its capture drivers, its freeze or publication scripts, or
`reg_tracking.py`. It works as follows:

- It checks the image sha256 (`73461d0896204b1c259c`) and decodes two bodies completely.
  - Read `0059D4B0` is checked against its `.pdata` record.
  - The retained IsOpen `0059D920` has no record. It is bounded by int3 bytes before and after it.
- It enumerates every entry → ret path.
- It takes each guard's width and signedness from capstone's operand detail and the REX prefix.
- It resolves the import from the PE import directory.
- It does frame arithmetic for the count slot and the stack-passed fifth argument.
- In the sandbox, every arm runs with values that would expose a width or sign error, and the ReadFile stub is run
  both writing and not writing the count.
- It runs the zero view twice. The first is the bare witness. The second is the stream built by constructor →
  resolver → route-1 hit → NULL allocation. Each is read with sizes 0 and 0x100.
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is
  rechecked after all controls.

Raw output: [rv_read.out](rv_read.out).

## Re-derived (34 checks, 34 PASS, 0 FAIL; 8 controls among them)

| Claim | Result |
|---|---|
| Read `0059D4B0` + 0x5C (92 B) | PASS: it decodes exactly, and exactly one `.pdata` record covers it. It has three `ret`s (+ 0x19, + 0x48, + 0x5B), no tail branch and exactly five entry → ret paths, which are the packet's five classes. |
| A non-zero `+0x30` calls `002150E0` first | PASS: + 0x4 `mov rax, qword ptr [rcx + 0x30]` (8 B), `test rax, rax`, `je`. On the non-zero arm, rcx = the buffer and `002150E0` is the first and only call; its RAX is returned. |
| A zero buffer with `R8D` = 0 makes no call and returns a full RAX of 0 | PASS: + 0x1E `test r8d, r8d` / `je` goes to the final `ret`. On both no-call paths the only rax writer is the + 0x4 qword load, which loaded the zero. |
| `R8D` is a low-32 guard only | PASS: the test is `test r8d, r8d` (REX 0x45, not 0x4D). In the sandbox, a size of `0x100000000` with a bound handle makes no call and returns 0. |
| `R8D` ≠ 0, `+0x28` = -1, signed `+0x40` ≤ 0 → no call, a full RAX of 0 | PASS: + 0x23 `mov r10, qword ptr [rcx + 0x28]` / `cmp r10, -1` (64-bit) / `je`. Then + 0x49 `mov rcx, qword ptr [rcx + 0x40]` / `test rcx, rcx` / `jle`, which is a signed test. |
| A positive `+0x40` calls `001D6CA0` | PASS: rcx = the `+0x40` value. In the sandbox, `0x77` and `0xFFFFFFFF` call it. -1, 0 and `0x8000000000000000` do not. |
| IAT `008C2140` = `KERNEL32!ReadFile` | PASS: + 0x3A is `call [rip+…]` through `008C2140`, which the import directory names `KERNEL32.dll!ReadFile`. That is the static declaration only. |
| `EAX` is replaced by a stack DWORD count after the call | PASS: + 0x40 `mov eax, dword ptr [rsp + 0x40]` (4 B, zero-extending) directly follows the call. In the sandbox, a stub that writes 0x0C and returns BOOL 1 gives RAX = 0x0C. |
| The witness: IsOpen accepts -1 / 0 / 0, and Read supplies nothing | PASS: IsOpen returns AL 1. Read with sizes 0 and 0x100 returns a full RAX of 0, with no call and no stream write. |
| The composed zero view | PASS: the stream built by constructor → resolver → route-1 hit → NULL allocation gives the same result: IsOpen AL 1, and Read returns 0 with no call for sizes 0 and 0x100. |
| Read writes nothing outside its own stack | PASS: every memory write is rsp-based. |

The eleven sandbox arm cases cover:
- a buffer, including one only in the high half;
- size 0, and a size only in the high half with a bound handle;
- a handle, including `0xFFFFFFFF`;
- a positive cache value, including `0xFFFFFFFF`;
- cache values 0, -1 and `0x8000000000000000`.

Each gives the derived call list and full RAX, with no stream write.

## Additions (implicit in the packet; they do not change any claim)

- **The count slot is pre-zeroed.** On the zero-buffer arm, + 0x1A stores EAX, which is 0 there, into `[rsp+40h]`.
  With the 38h frame, that is entry SP+8, the caller's home slot for rcx. ReadFile's `lpNumberOfBytesRead` points
  there. So a ReadFile that writes no count makes Read return 0. The sandbox confirms this with a stub that writes
  nothing and returns 0.
- **The fifth argument is 0.** `lpOverlapped` (`[rsp+20h]`) is RAX, which is 0 on this arm.
- **rdx and r8 pass through unchanged.** No instruction in the body writes them, so `002150E0`, ReadFile and
  `001D6CA0` all receive the caller's destination and full size register. ReadFile reads only `r8d`.

## Controls (8, each must FAIL a named check on a privately patched image; all did)

A null control runs first: an unchanged private copy, with the sha check off, passes all 19 image checks.

1. + 0x1E `test r8d, r8d` → `test r8, r8`. Fails the size-guard check and the arm sandbox (the high-half size with a
   handle now reads).
2. + 0x4 `mov rax, [rcx+30h]` → `mov eax, [rcx+30h]; nop`. Fails the buffer check and the arm sandbox.
3. + 0x50 `jle` → `jl`. Fails the cache-arm check, the arm sandbox and the witness.
4. + 0x40 `mov eax, [rsp+40h]` → four nops. Fails the replacement check, the arm sandbox and the ReadFile-argument
   run.
5. + 0x3A: the call moved to IAT slot + 8 (`SetEndOfFile`). Fails the import check, the arm sandbox and the
   ReadFile-argument run.
6. + 0x1A `mov [rsp+40h], eax` → four nops. Fails the pre-zero check and the ReadFile-argument run, because junk on
   the stack is then returned.
7. + 0x27 `cmp r10, -1` → `cmp r10d, -1`. Fails the handle-width check and the arm sandbox.
8. Retained IsOpen + 0xE: `-1` → `0`. Fails the IsOpen shape check, the witness and the composed run.

After all controls the exe on disk still hashes to `73461d0896204b1c259c`. The packet's three CLI refusals and four
decoded-record controls were not repeated. These eight replace them for this review.

## Limits (kept as the packet states them)

This review supports conditional static facts only. Its premises:
- a valid, readable record and a private frame;
- normal execution.

The sandbox stubs model `002150E0`, `001D6CA0` and ReadFile. They do not establish them. The following remain open
and are not awarded:
- the helpers' and the API's native effects, error and partial-count semantics, and the live DLL binding;
- an actual caller, natural allocation failure, a read fault, a leak, and scheduling;
- what the engine does after a 0-byte Read.

Consumption: see the combined draft in
[fable-review-astra-filecache-close-zero-sentinel-1002/consumption-draft.md](../fable-review-astra-filecache-close-zero-sentinel-1002/consumption-draft.md).

run: `rv_read.py` at c0bf8acd5 (34 checks, 34 PASS, 0 FAIL, 8 controls; output identical to [`rv_read.out`](rv_read.out); capstone 5.0.7, unicorn 2.1.4)
