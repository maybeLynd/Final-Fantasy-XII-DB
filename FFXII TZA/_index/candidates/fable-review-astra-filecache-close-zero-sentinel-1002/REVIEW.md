# FABLE review: ASTRA filecache-close-zero-sentinel

- **Packet:** [filecache-close-zero-sentinel README](../../../_experiments/evidence/filecache-close-zero-sentinel/README.md)
- **Producer commit:** `a30d4772a`. The manifest sha256 begins `460bdc9fcf554fb3` and equals the committed manifest.
  All 54 members hash as listed. The packet's two range hashes (Close, and the retained IsOpen) equal the certified
  image's bytes. The retained IsOpen manifest is byte-identical to `filecache-open-sentinel`'s committed manifest
  (`7479a4f8…`), which FABLE reviews alongside this one ([review](../fable-review-astra-filecache-open-sentinel-1002/REVIEW.md),
  ACCEPT).
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT.** Every claim re-derives at the bytes:
  - the 64-byte body and its two guards: the buffer guard tests for zero, and the cache guard is a signed ≤ 0 test;
  - the full-qword clear and reset;
  - the single `mov al, 1` that every return passes through;
  - the zero-view witness, where Close returns AL 1 with no call and no write and IsOpen still returns AL 1.

  The reviewer goes one step further than the packet. It states exactly when a true Close is followed by a false
  IsOpen. This widens the packet's refutation and does not narrow anything in it.

## Method

[rv_close.py](rv_close.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is copied
unchanged from the route2-commit-key review (sha256 `69f9bc40be32abcc32b1`). It also uses the reviewer's own Unicorn
2.1.4 sandbox, which runs the shipped bytes over a private copy of the image's sections. Every callee and import is a
recording stub. The stubs and their premises are described in the zero-handle review. The script does not import
ASTRA's `prove.py`, its capture drivers, its freeze or publication scripts, or `reg_tracking.py`. It works as follows:

- It checks the image sha256 (`73461d0896204b1c259c`) and decodes two bodies completely.
  - Close `0059BD40` is checked against its `.pdata` record.
  - The retained IsOpen `0059D920` has no record. It is bounded by int3 bytes before and after it.
- It enumerates the four entry → ret paths with their calls and stores.
- It takes the guards' width and signedness from capstone's operand detail.
- It checks that `mov al, 1` dominates the ret.
- In the sandbox it runs Close and then IsOpen:
  - on the witness;
  - on the four buffer × cache partitions;
  - on a 96-case grid: `+0x28` takes 4 values, `+0x30` takes 3, and `+0x40` takes 8, among them `0x8000000000000000`,
    `0x8000000000000001` and `0xFFFFFFFF`;
  - on the composed zero view, built by constructor → resolver → route-1 hit → NULL allocation.
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is
  rechecked after all controls.

Raw output: [rv_close.out](rv_close.out).

## Re-derived (28 checks, 28 PASS, 0 FAIL; 8 controls among them)

| Claim | Result |
|---|---|
| Close `0059BD40` + 0x40 (64 B) | PASS: it decodes exactly, and exactly one `.pdata` record covers it. Its one `ret` is the last instruction (+ 0x3F), and it has no tail branch. |
| A non-zero `+0x30` calls `002150D0`, then zeroes `+0x30` | PASS: + 0x9 `mov rcx, qword ptr [rcx + 0x30]` (8 B), `test`, `je`. Then + 0x12 calls `002150D0` with rcx = the buffer, and + 0x17 `mov qword ptr [rbx + 0x30], 0` (8 B). |
| A signed `+0x40` ≤ 0 skips both `001D6AA0` and the reset | PASS: + 0x1F `mov rdx, qword ptr [rbx + 0x40]` (8 B), `test rdx, rdx`, + 0x26 `jle`. TEST clears OF, so JLE is ZF or SF, which is a signed ≤ 0 test. |
| A positive value reads the dword `+0x48` key, calls `001D6AA0` and writes `+0x40` = -1 | PASS: + 0x28 `mov ecx, dword ptr [rbx + 0x48]` (4 B), + 0x2B call, + 0x30 `mov qword ptr [rbx + 0x40], -1` (8 B). |
| Four partitions with exactly their calls and stores | PASS: exactly four paths, whose (call, store) sequences are: none; `002150D0`, `+0x30`; `001D6AA0`, `+0x40`; and all four in that order. The sandbox runs each partition and gets the same calls, stores and arguments. |
| Every normal return assigns AL = 1 and nothing more | PASS: the only rax writer is `mov al, 1` (+ 0x38), and it dominates the ret. In the sandbox, bits 8–63 of RAX are whatever they were on entry, or what the last helper returned. |
| Close never accesses `+0x28` | PASS: no instruction reads or writes it. |
| The witness `-1 / 0 / 0` | PASS: Close returns AL 1, with no call and no object write, and the three fields are unchanged. The retained IsOpen then returns AL 1. |
| A universal "Close true ⇒ IsOpen false" is refuted | PASS. The grid states the exact rule (see the addition below). |
| The composed zero view | PASS: Close returns AL 1, with no call and no write, and IsOpen stays at AL 1. A real view (non-NULL allocation) closes through `001D6AA0`, and IsOpen then returns AL 0. |

## Addition: when a true Close is followed by a false IsOpen

Close leaves `+0x28` alone. It always ends with `+0x30` = 0, and it sets `+0x40` = -1 only when `+0x40` was
signed-positive. So the IsOpen that follows is false **exactly when `+0x28` was already -1 and `+0x40` was positive
or already -1**.

The sandbox grid matches this rule in all 96 cases. In 84 of the 96, Close returned AL 1 and IsOpen still returned
AL 1.

Two consequences:
- **A handle-backed stream is never made "closed" by this body.** Any `+0x28` other than -1 survives every arm.
  This is broader than the packet's "a non-sentinel `+0x28` with the same no-helper guard", which is one case of
  it.
- **`001D6AA0` also receives the cache value.** At its call rdx is still the `+0x40` value, because rdx has a single
  writer at + 0x1F. The call therefore gets ecx = the `+0x48` key and rdx = the `+0x40` value.

## Controls (8, each must FAIL a named check on a privately patched image; all did)

A null control runs first: an unchanged private copy, with the sha check off, passes all 14 image checks.

1. + 0x26 `jle` → `jl`. Fails the guard check, the witness (0 now resets) and the grid.
2. + 0x26 `jle` → `je`. Fails the guard check, the partitions (a negative value now resets) and the grid.
3. + 0x30: the qword reset → a dword reset + nop. Fails the reset check, the partitions and the grid.
4. + 0x10 `je` retargeted to + 0x38, so skipping the release also skips the reset. Fails the buffer-arm check, the
   path-shape check and the partitions.
5. + 0x17: the clear moved from `+0x30` to `+0x28`. Fails the buffer-arm check, the path-shape check and the
   no-`+0x28` check.
6. + 0x38 `mov al, 1` → `xor al, al`. Fails the AL check, the witness and the partitions.
7. + 0x1F `mov rdx, [rbx+40h]` → `mov edx, [rbx+40h]; nop`. Fails the guard check, the partitions and the grid.
8. Retained IsOpen + 0xE: `-1` → `0`. Fails the IsOpen shape check, the witness and the grid.

After all controls the exe on disk still hashes to `73461d0896204b1c259c`. The packet's three CLI refusals and four
decoded-record controls were not repeated. These eight replace them for this review. The packet's own history is
also kept: Control01 was invalid and was corrected by Control02.

## Limits (kept as the packet states them)

The zero no-helper arm needs no opaque effect. The other arms rest on these premises:
- a normal ABI and normal returns;
- `002150D0` and `001D6AA0` not writing the object;
- no aliasing and no interference.

All arms need a readable, valid record. The sandbox stubs stand in for those premises. They do not establish them.
The following remain open and are not awarded:
- what the two helpers release, and whether anything leaks;
- natural allocation failure, and actual callers, including the prefetch loop's `Close`;
- later effects on Read beyond the read-zero-view review;
- every writer, resource cardinality, ownership, reuse, lifetime and scheduling.

This review does not say a Win32 handle is leaked. It says only that this body never touches `+0x28`.

Consumption: the combined draft for all four packets is [consumption-draft.md](consumption-draft.md).

run: `rv_close.py` at c0bf8acd5 (28 checks, 28 PASS, 0 FAIL, 8 controls; output identical to [`rv_close.out`](rv_close.out); capstone 5.0.7, unicorn 2.1.4)
