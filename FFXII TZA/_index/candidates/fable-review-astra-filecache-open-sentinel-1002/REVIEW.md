# FABLE review: ASTRA filecache-open-sentinel

- **Packet:** [filecache-open-sentinel README](../../../_experiments/evidence/filecache-open-sentinel/README.md)
- **Producer commit:** `446a56af9`. The manifest sha256 begins `7479a4f8d544249b` and equals the committed manifest.
  All 48 members hash as listed. The packet's seven captured and parent range hashes equal the certified image's
  bytes, and they include IsOpen, the constructor and the resolver. The two parent manifests are:
  - `filecache-source-key-initialization` (`d5cc7655…`), which FABLE reviewed as ACCEPT-WITH-NARROWING;
  - `filecache-zero-handle-return` (`93e2351f…`), the same committed manifest FABLE reviews alongside this one
    ([review](../fable-review-astra-filecache-zero-handle-return-1002/REVIEW.md), ACCEPT-WITH-NARROWING).
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT.** Every claim re-derives at the bytes:
  - the 27-byte predicate's formula, its full 64-bit compares and its AL-only result;
  - the counterexample `+0x28` = -1, `+0x30` = 0, `+0x40` = 0 → AL 1;
  - the constructor's sentinel writes and the resolver's store into the stream's `+0x40`;
  - the conditional composition, which runs end to end in the reviewer's sandbox.

  Nothing needs narrowing. Two clarifications are given below. They come from the companion zero-handle review
  and do not change any claim.

## Method

[rv_open.py](rv_open.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is copied
unchanged from the route2-commit-key review (sha256 `69f9bc40be32abcc32b1`). It also uses the reviewer's own sandbox:
Unicorn 2.1.4 runs the shipped bytes over a private copy of the image's sections, and every callee and import is a
recording stub that returns a chosen RAX and puts junk in the volatile registers. The sandbox and its stubs are
described in the zero-handle review. The script does not import ASTRA's `prove.py`, its capture drivers, its freeze or
publication scripts, or `reg_tracking.py`. It works as follows:

- It checks the image sha256 (`73461d0896204b1c259c`) and decodes three bodies completely.
  - IsOpen `0059D920` has no `.pdata` record. It is bounded by int3 bytes before its entry and after its last `ret`,
    and by its closed CFG.
  - The constructor `00597970` and the resolver `0059EE90` are each checked against their `.pdata` record.
- It checks IsOpen's exact instruction text, its operand widths and its rax writers.
- It runs IsOpen in the sandbox over a grid of 64 cases. Each of `+0x28`, `+0x30` and `+0x40` takes four values,
  chosen so that a dword compare, a zero-for-all-ones sentinel or a flipped branch would give a different answer. RAX
  starts as junk, so a full-register write would show.
- It takes a census of the constructor's and the resolver's writes to the three fields, before and after the
  resolver call and on every path to the lookup.
- It runs the composition from the constructor itself: a null path, then a path resolved through a route-1 hit whose
  16-byte allocation returns NULL, then the same path with a real allocation.
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is
  rechecked after all controls.

Raw output: [rv_open.out](rv_open.out).

## Re-derived (32 checks, 32 PASS, 0 FAIL; 8 controls among them)

### IsOpen

| Claim | Result |
|---|---|
| `0059D920` + 0x1B (27 B), ten instructions, no calls and no object writes | PASS: it decodes exactly and has no `.pdata` record, with int3 before and after. It has two `ret`s (+ 0x17 and + 0x1A), no call and no memory write. |
| `AL = !(q28 == -1 && q30 == 0 && q40 == -1)` | PASS: the text is exactly `cmp q[+28h], -1` / `jne` / `cmp q[+30h], 0` / `jne` / `cmp q[+40h], -1` / `jne` / `xor al, al` / `ret` / `mov al, 1` / `ret`. Every `jne` goes to the `mov al, 1`. |
| Full 64-bit fields | PASS: all three compares have an 8-byte memory operand and a REX.W prefix, with sign-extended immediates -1, 0 and -1. |
| Only AL is assigned | PASS: the only rax writers are `xor al, al` (+ 0x15) and `mov al, 1` (+ 0x18). |
| Eight equality classes, false only for the all-sentinel one | PASS in the sandbox: in all 64 cases AL equals the formula, and only one case is false. Bits 8–63 of RAX are never touched, and there is no call or write. |
| Counterexample `-1 / 0 / 0` | PASS: the run goes through + 0x13's `jne` to `mov al, 1`, and AL = 1. |

### Constructor and resolver

| Claim | Result |
|---|---|
| `00597970` initialises `+0x28` = -1, `+0x30` = 0, `+0x40` = -1 | PASS: before the resolver call it writes `+0x28` = -1 (8 B), `+0x20` = 0 (4), `+0x30` = rbp = 0 (8), `+0x40` = -1 (8), `+0x48` = 0 (4) and `+0x38` = the selector byte. ebp is `xor ebp, ebp`. |
| It passes `this + 0x20` to the resolver | PASS: `add rcx, 0x20` and `mov r8b, 1`. The call happens only for a non-null path (`test rdx, rdx` / `je`). |
| No later constructor write to the backing fields | PASS: after the call, its writes go to `+8`, `+0`, `+0x10`, `+0x1C` and `+0x18`, none of them in `+0x28`..`+0x47`. |
| The constructor returns its object; the status is separate | PASS: the first instruction after the call overwrites rax, and + 0x99 is `mov rax, rdi`. |
| The resolver's `[r15+20h]` store is the stream's `+0x40` | PASS: r15 = `this + 0x20`. The resolver writes through r15 only at `+0`/4, `+0x10`/8, `+0x18`/1 and `+0x20`/8, which are the stream's `+0x20`, `+0x30`, `+0x38` and `+0x40`. It never writes the stream's `+0x28`. |
| No prefix write to the other fields | PASS: on every entry → lookup-call path (94 instructions), the only r15 write is the forced selector byte (`0059EE90` + 0x61). |
| The post-zero slice | PASS: after a non-negative result, the only r15 write is the size (`0059EE90` + 0x166). The route-2 buffer store (`0059EE90` + 0x307) is unreachable. |

### Composition (sandbox)

| Run | Result |
|---|---|
| Constructed with a null path | PASS: the stream is -1 / 0 / -1, and IsOpen returns AL 0. |
| Path → route-1 hit → NULL allocation | PASS: the constructor returns `this`, the stream is -1 / 0 / 0, and IsOpen returns AL 1. |
| Path → route-1 hit → real allocation | PASS: `+0x40` = the block, and IsOpen returns AL 1. The predicate gives the same answer for a null view and a real one. |

## Controls (8, each must FAIL a named check on a privately patched image; all did)

A null control runs first: an unchanged private copy, with the sha check off, passes all 17 image checks.

1. IsOpen + 0x0: the `-1` immediate → `0`. Fails the text, width and grid checks.
2. IsOpen + 0x0: the qword compare → a dword compare + nop. Five checks fail, the first listed being the decode,
   text and width checks.
3. IsOpen + 0x15: `xor al, al` → `xor eax, eax`. Fails the text and AL-only checks and the grid's upper-bits test.
4. IsOpen + 0x13: `jne` → `je`. Fails the text, grid and witness checks.
5. IsOpen + 0xE: the compare moved to `+0x48`. Fails the text, width and grid checks.
6. Constructor + 0x2B: the `+0x40` init moved to `+0x48`. Fails the init census and the null-path run.
7. Constructor + 0x24: the `+0x30` init moved to `+0x38`. Fails the init census, the null-path run and the composed
   run.
8. Resolver + 0x15A: `[r15+20h]` → `[r15+28h]`. Fails the r15 census and the composed run.

After all controls the exe on disk still hashes to `73461d0896204b1c259c`. The packet's three CLI refusals and four
synthetic decoded-record controls were not repeated. These eight replace them for this review.

## Clarifications (from the companion zero-handle review; no claim changes)

- **The composition needs a non-null path, the route-1 gates and a cache hit.** The constructor skips the resolver
  for a null path. That path leaves -1 / 0 / -1, which IsOpen rejects.
- **The zero view still has a size.** The resolver copies the hit entry's size into the stream's `+0x20` before
  returning status 0.

## Limits (kept as the packet states them)

This review supports conditional static facts only. Its premises:
- valid records and private frames, with no aliasing;
- normal returns under the native Win64 ABI;
- a successful cookie check;
- no opaque field interference.

The sandbox stubs stand in for those premises. They do not prove them. The following remain open and are not
awarded:
- that a shipped caller naturally reaches a NULL allocation, or calls IsOpen afterwards;
- every writer of the fields, their lifetime, ownership, reuse, scheduling and atomicity;
- native failure frequency, and the later consequences of a getter or read beyond what the read-zero-view and
  close-zero-sentinel reviews derive.

Consumption: see the combined draft in
[fable-review-astra-filecache-close-zero-sentinel-1002/consumption-draft.md](../fable-review-astra-filecache-close-zero-sentinel-1002/consumption-draft.md).

run: `rv_open.py` at c0bf8acd5 (32 checks, 32 PASS, 0 FAIL, 8 controls; output identical to [`rv_open.out`](rv_open.out); capstone 5.0.7, unicorn 2.1.4)
