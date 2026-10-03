# FABLE review: ASTRA ov42-mode17-query-boundaries

- **Packet:** the publication `ov42-mode17-query-boundaries` (board request `ASTRA-REQ-FABLE-OV42-MODE17-QUERY-1002`).
  The record path the request names, `_experiments/evidence/ov42-mode17-query-boundaries/README.md`, does not exist.
  The publication's evidence is two folders, both first committed in `7b4e2b92c`:
  [ov42-resource-mutator-mode17](../../../_experiments/evidence/ov42-resource-mutator-mode17/README.md) and
  [ov42-resource-eligibility-domain](../../../_experiments/evidence/ov42-resource-eligibility-domain/README.md).
  This review covers both.
- **Producer commit:** `7b4e2b92c`. The mutator manifest sha256 begins `6db69c8e1cae5b05` (32 members). The
  eligibility manifest sha256 begins `9f78042a995e6cdd` (91 members). Each equals its manifest committed at
  `7b4e2b92c`, and every member hashes as listed. Every source range in both folders hashes to the certified image's
  bytes, and its instruction records concatenate to them. The ranges are the two modifiers `00300CE0` and `00300BC0`,
  the queries `0030B770` and `0030B7F0`, the getter `0017D470`, the accessor `001D50D0` and the constructor
  `001CCB20`. Every extents file equals the image's physical bytes, sizes and `.pdata` records.
  `retained-constructor-source-01.json` is byte-identical to `30754ad4b`'s `special-override-constructor-raw-01.json`.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every claim re-derives at the bytes. The global query's upper WORD is
  always 0. The unit query's upper WORD comes from two separate getter reads of `+0xC20`. It is 0..3 in general
  and 0..2 when both reads see one value. The modifier's flag decoding, the entry-leg bypass, the call order
  (notification attempt, then both queries, then the veto, then the store, then the accumulator clear) and the
  secondary modifier's store before its follow-up call all hold. So do the accessor's lazy NULL path and the
  constructor's own zero store, followed by seven opaque calls. An emulation of the original queries, getter and
  accessor, and of both modifiers with their outside callees stubbed, agrees on every case tried. The narrowings
  correct the record path. They add that the veto can act only on the late leg, name who passes mode 17, record a
  second root initializer on the startup path, and add a low-WORD link to the special-sequence state.

## Method

[rv_mode17q.py](rv_mode17q.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is
copied unchanged from the kind-row review (sha256 `69f9bc40be32abcc`). It does not import or run ASTRA's `prove.py`,
`prove_owner_reload_order.py`, `prove-before-*.py`, `qualify-singleton*.py`, `capture*.py`, `prepare-*.py`,
`control.py`, `run.py`, `validate-title-source-annotations.py`, or `reg_tracking.py`. It works as follows:

- It checks the image sha256 (`73461d0896204b1c259c`). It checks the `.pdata` extents and the exact linear decode of
  the eight bodies, including the twin accessor `001D5090`.
- It reads the instructions. The read covers the two queries' complete store lists, the unit query's upper-WORD arms,
  the getter's DWORD read, the accessor's two paths, the constructor's `+0xC20` store and the calls after it, the
  primary modifier's flag decoding, both query legs, the vetoes and the store order, and the secondary modifier's
  store before its call.
- It emulates (unicorn) the **original** global query, unit query, getter and accessor, with nothing stubbed on the
  initialized path. The global query runs over every combination of its six mask bits and the flag byte's bit 0, at
  eight stack alignments, on a stack filled with 0xFF (1024 runs). The unit query runs over 3456 states. Further runs
  cover two different C20 reads, the lazy path, a NULL allocation and a constructor whose return differs from the
  allocation.
- It emulates the **original** primary and secondary modifiers with the queries run from the image and their outside
  callees stubbed (owner lookup `0031B860`, the two publishers `003283D0` and `0028F1F0`, the accumulator clear
  `002FA540`, the secondary or its follow-up `0030E060`, and `00210EC0`/`001CCB20`). It runs modes 17, 16, 1 and 0x91,
  negative and positive deltas, a NULL owner, and the intervention case with `0030B770` replaced by a stub.
- It runs a raw `E8`/`E9` rel32 and `0F 8x` census for the bodies, and a disp32 census (rip-relative and
  image-base-relative, decoded from each hit's `.pdata` record) of the singleton root `01F81428`.
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is
  rechecked after all controls.

Raw output: [rv_mode17q.out](rv_mode17q.out).

## Re-derived (65 checks, 65 PASS, 0 FAIL; 18 controls among them)

### The global query `0030B770` (119 B)

| Claim | Result |
|---|---|
| Initial DWORD 0, only low-WORD stores, no calls | PASS: its stores are exactly `mov dword ptr [rbp], 0` (+ 0x15) and five `mov word ptr [rbp], ax`. RBP = (RSP + 0x40) & ~0x3F is set once, and it returns DWORD `[rbp]`. It makes no call. |
| Upper WORD always 0; low mask 0..31 | PASS, emulated: in 1024 runs the upper WORD is 0 every time, and the low WORD equals the bit map from DWORD `02089340` (mask 0x3080, bits 10, 9 and 11) and bit 0 of byte `022C2158`. The stack was filled with 0xFF, so a missing zeroing store would show. |

### The unit query `0030B7F0` (226 B), the getter and the accessor

| Claim | Result |
|---|---|
| Eligibility before the getters | PASS: a NULL unit (+ 0x14) or DWORD bit 4 clear (+ 0x1D / + 0x21) returns the zeroed DWORD before either call. Emulated: an ineligible unit reads `+0xC20` zero times. |
| Upper bit 0 = first read 1, current stats nonNULL, stats byte +5 = 0; upper bit 1 = second read 2 | PASS: `cmp eax, 1` (+ 0x98), `[unit + 0x698]` nonNULL, its byte +5 = 0, then `or bx, 1`. `cmp eax, 2` (+ 0xCB), then `or bx, ax`. Its only stores are to its own result DWORD, and its upper WORD is written only at + 0xBA and + 0xD3. Emulated over 3456 states: the result equals the formula every time. |
| Two independent reads; 0..3, and 0..2 for one value | PASS: the only calls are two calls of `0017D470` (+ 0x93, + 0xC6). The getter is `call 001D50D0` / `mov eax, dword ptr [rax + 0xc20]` (4 B). Emulated: with one value in `+0xC20`, the upper WORD is only ever 0, 1 or 2, and the DWORD is read exactly twice. When the value changes between the calls, first 1 / second 2 gives 3. The packet's four conditional-control rows reproduce as 1, 2, 3, 0. |
| The modifier passes EDX 0 | PASS: `xor edx, edx` at `00300CE0` + 0x6B and + 0x102 precede both unit-query calls. The arm that needs a nonzero EDX (`bt r8d, 0x1e` / `test edx, edx` / `or cx, 2`) is a low-WORD arm. |
| Accessor: fast path call-free and store-free; lazy NULL path | PASS: a nonNULL root goes straight to the epilogue. That path's only store is to the stack (+ 0x4). A NULL root leads to `mov ecx, 0x10e8`, `call 00210EC0`, `call 001CCB20` on a nonNULL allocation, and a store of RAX to `01F81428` (+ 0x36). Emulated: one allocation and one constructor call, after which the second getter call takes the fast path. A NULL allocation stores the root as 0 and makes no constructor call, and the getter then reads address 0xC20 (an emulated fault, a source prediction). The root receives the constructor's RAX even when it differs from the allocation. |
| Constructor's own `+0xC20` store is intermediate | PASS: + 0x22 `mov rdi, rcx`, + 0x25 `xor ebp, ebp`, and neither is rewritten before + 0x12B `mov dword ptr [rdi + 0xc20], ebp`, the body's only store that covers `+0xC20`. Calls between them preserve RBP only by the Win64 ABI. Seven calls follow, equal to `qualified-result-02`'s list. |

### The modifiers

| Claim | Result |
|---|---|
| Mode 17 flag roles | PASS: bit 0 skips the entry leg (+ 0x64), inverted bit 4 gates `003283D0` (+ 0xDA), and inverted bit 7 gates `0028F1F0` (+ 0xF3). Emulated: mode 1 calls `003283D0`, mode 0x91 does not call `0028F1F0`, and mode 17 calls `0028F1F0` but never `003283D0`. |
| Negative delta: notification attempt, then both queries, then veto, then store | PASS. Emulated mode 17, delta -10, C20 0: owner lookup, then `0028F1F0` with ECX = owner DWORD 8, EDX = 50, R8D = 40, R9D = 1, then `0030B770`, `0030B7F0`, the `+0x4C` store of 40 and `002FA540`. C20 1 (stats byte +5 = 0) or C20 2 stops the store and the `002FA540` call after the notification attempt, and MP stays 50. The store (+ 0x120) is reachable from + 0xFD only through both late tests. |
| The global partition is an intervention | PASS: emulated with `0030B770` **replaced** by a stub returning 0x10000, the store is vetoed. The same stub returning 0x1F does not veto. The shipping body never returns the former (first table). |
| Private frame | PASS, emulated: in the whole mode-17 run the only write to the modifier's RDX home slot is its own save of the global result (+ 0x104). Nothing the unit query runs overwrites it before the WORD test (+ 0x110). |
| Secondary: WORD +6 before `0030E060` with the full flags | PASS: + 0xAA `mov word ptr [rdi + 6], cx` dominates + 0xB4 `call 0030E060`, whose EDX is the full R14D. Emulated mode 17: the store of 15, then the call with (stats, 0x11), and no query. |

### Packet integrity

PASS. Both manifests equal their committed versions, and all 32 + 91 members match. The eligibility README keeps
natural initialization, ownership/lifetime and concurrent/alias mutation as explicit premises, and says the
correction "does not promise that the whole operation has no effects". The mutator README says the `28F1F0` call
attempt is not visible presentation and that the own-write veto is not a whole-call no-write claim. The mutator
`result-02`'s three cases agree with the emulation. Its first-upper case agrees only with `0030B770` replaced.

## Controls (18, each must FAIL a named check on a privately patched image; all did)

A null control also runs first: an unchanged private copy passes all 31 image checks.

1. The global query's zeroing store writes 0x10000. Fails the store-list, the 1024-run sweep and the mode-17 order checks.
2. The zeroing store removed (7-byte NOP). Fails the store-list check and the sweep (0xFF stack).
3. A WORD store widened to a DWORD (+ 0x40). Fails the store-list check.
4. `cmp eax, 2` -> `cmp eax, 1` (unit query + 0xCB). Fails the arm, grid, two-read and modifier checks.
5. `cmp eax, 1` -> `cmp eax, 2` (+ 0x98). Fails the arm, grid (an upper 3 from one value) and two-read checks.
6. The byte +5 test removed (+ 0xAF). Fails the arm, grid and no-veto checks.
7. The getter's field `+0xC20` -> `+0xC24`. Fails the getter, grid and read-count checks.
8. The accessor's fast-path `jne` inverted. Fails the grid, read-count and two-read checks.
9. The accessor's fast path retargeted to the root store. Fails the accessor, read-count and lazy-path checks.
10. The late global-upper veto removed (modifier + 0x116). Fails the late-leg check and the intervention run.
11. The late unit-upper veto removed (+ 0x11E). Fails the late-leg check and the veto runs.
12. The bit-0 bypass removed (+ 0x64). Fails the flag check and the mode-17 order and veto runs.
13. `jns` -> `jmp` (+ 0xFB, the late leg never runs). Fails the late-leg check and the veto runs.
14. `xor edx, edx` -> `mov edx, ebx` (+ 0x102). Fails the EDX-0 check and the mode-16 run.
15. The secondary's WORD +6 store removed. Fails the secondary check and its emulation.
16. The secondary's follow-up EDX -> ESI (+ 0xAE). Fails the secondary check and its emulation.
17. The constructor's `+0xC20` store -> `+0xC24`. Fails the constructor check.
18. The constructor's `xor ebp, ebp` -> `mov ebp, ebx`. Fails the constructor check.

After all controls, the exe on disk still hashes to `73461d0896204b1c259c`. The packets' source controls and CLI
refusals (three base, four qualifier, three CLI in the eligibility folder, three in the mutator folder) were not
repeated. These 18 image patches replace them for this review.

## Narrowings

1. **The named record does not exist; the evidence is two folders from one commit.** The request names
   `ov42-mode17-query-boundaries/README.md`. The publication instead committed `ov42-resource-mutator-mode17` and
   `ov42-resource-eligibility-domain`, both first in `7b4e2b92c`. The eligibility README's "frozen mode17 package"
   (named by an 8-digit prefix of `6db69c8e1cae5b05`) is the mutator folder's manifest hash, not an earlier commit. The "additive correction" and the package
   it corrects landed in the same commit. Consumers should cite the two folders.
2. **The C20 veto can act only on the late leg.** The entry leg (bit 0 clear) tests the queries' **low** WORDs
   (`test bx, bx`, `test ax, ax`), which do not depend on `+0xC20`. Only a negative delta reaches the late leg,
   which tests the upper WORDs. A positive delta consults neither query in mode 17. So the console's Invincible
   setting can stop only an MP decrease, and only after the notification attempt.
3. **Who passes mode 17.** The consume path `00305640` + 0xB4 calls the primary modifier with R8D = 0x10 + (R12D !=
   0), which is mode 16 or 17, and with EDX = minus the cost. Its + 0xCD call to the secondary passes the same R8D. For
   this caller bit 4 is always set (no `003283D0`) and bit 7 always clear (`0028F1F0` is attempted for a nonNULL
   owner). In mode 16 the entry leg runs both queries before the notification (emulated). The primary modifier has
   six raw direct callers, and the other five callers' flags are not read here.
4. **The root has a second NULL-path initializer on the startup path.** In the disp32 census the root `01F81428` is
   stored by exactly two instructions: the accessor's + 0x36 and its twin `001D5090` + 0x34. Each store is skipped
   when the root is nonNULL, so no instruction in the census replaces a nonNULL root. The twin's one raw direct
   caller is the ensure stub `001C1940`, which the game-application page lists in the startup manager-init burst
   ("`001C1940` -> `[01F81268]` (ctor `001D5090`)"). The packet's initialized-root premise therefore has a named
   startup route. This review does not read whether that route precedes every query, nor any free, aliased or
   indirect root write.
5. **The unit query's low WORD reads the special-sequence state.** Low bit 3 (value 8) is set when the unit's byte +4
   bit 5 is set and `022C2160` is not 5 or 6 (`add eax, -5` / `cmp eax, 1` / `jbe`). This is a low-WORD bit. It can
   matter only at the entry leg (mode 16), never for the late upper-WORD veto. It is noted because `022C2160` is the
   OV-42 special-sequence state.

## What stays OPEN (kept as the packet states them)

This review supports static facts and emulation of the original bytes on supplied state. The following remain open
and are not awarded:

- natural initialization timing of the root, and the absence of other root or `+0xC20` writers during a query (the
  console's arm 14 is the known writer, and it wraps at 3; no image-wide `+0xC20` writer census was run);
- the effects of `0028F1F0`, `003283D0`, `002FA540`, `0030E060` and the constructor's later calls, and so any
  visible presentation of a vetoed decrease;
- whether any normal play state reaches mode 17 with a negative delta and Invincible 1 or 2;
- concurrency, ownership and lifetime, the table binding, and whole OV-42.

The upper 3 is a two-read model, not an observed change of the setting. The intervention case is a substituted
callee, not shipping behaviour. Valid storage, the Win64 ABI and private frames are premises.

run: `rv_mode17q.py` at HEAD c2fc944fe (65 checks, 65 PASS, 0 FAIL, 18 controls; output identical to [`rv_mode17q.out`](rv_mode17q.out))
