# FABLE review: ASTRA filecache-route2-commit-key

- **Packet:** [filecache-route2-commit-key README](../../../_experiments/evidence/filecache-route2-commit-key/README.md)
- **Producer commit:** `81cbc06f0`. The manifest sha256 begins `f3365d0eb049fb0c` and equals the committed manifest.
  All 99 members hash as listed. The packet's seven captured and retained range hashes (`source-01.json` plus the
  two retained source maps) equal the certified image's bytes. They include all five bodies reviewed here.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every carrier, frame, store, branch and byte-total claim re-derives at the
  bytes: 1491 new bytes over three complete bodies, plus 119 retained bytes. The empty-key composition holds under
  the premises listed below. The narrowings add two insertion gates, an alias window and a .pdata clarification that
  the packet leaves out. They do not contradict anything the packet states.

## Method

[rv_route2.py](rv_route2.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is
copied unchanged from the insert-key-admission review (sha256 `69f9bc40be32abcc32b1`). It does not import ASTRA's `prove.py`,
its capture drivers, its freeze or publication scripts, or the shared role adapter `reg_tracking.py`. It works as
follows:

- It checks the image sha256 (`73461d0896204b1c259c`) and decodes the five bodies completely.
  - Four bodies are checked against the image's own `.pdata`.
  - The hash leaf `00674A00` has no record. It is bounded by its closed CFG, its single final `ret`, and int3
    padding before it and after it.
- It builds a local CFG from direct branches for each body.
- For each key or out-key carrier, it takes a register-write census and does exact frame arithmetic for each
  stack-passed argument.
- It runs dominance and "every path except one edge" checks for the out-key store and for the hash's `btr`.
- It takes a census of every write that could reach source-record+28h between the lookup and the commit read.
- It runs its own finite abstract interpretation of the resolver's arm byte r12b. Each state is
  (pc, r12b in {0, 1, unknown}, lookup seen). Every other branch is taken both ways, and callees are assumed to keep
  r12 (Win64 nonvolatile ABI).
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is
  rechecked after all controls.

Raw output: [rv_route2.out](rv_route2.out).

## Re-derived (72 checks, 72 PASS, 0 FAIL; 13 controls among them)

### Bodies and totals (claim 5)

| Claim | Result |
|---|---|
| Resolver `0059EE90` + 0x36C (876 B), commit `0059A9B0` + 0x125 (293 B), lookup `0020C1B0` + 0x142 (322 B): 1491 B | PASS: each decodes exactly and exactly one `.pdata` record covers each. The resolver's record runs through the epilogue and its only `ret` (59F1FB, the last instruction). See narrowing 4. |
| Retained wrapper `001D6D20` + 0x4F (79 B) and hash `00674A00` + 0x28 (40 B): 119 B | PASS: the wrapper has one `.pdata` record. The hash has none; it is bounded by int3 at `00674A00` - 1 and 8 int3 bytes after its `ret`. |
| Local CFGs closed | PASS: there is no tail or out-of-body branch. Four bodies have a single `ret` as their last instruction. `0059A9B0` has two: the early 59A9F4 and the last 59AAD4. |
| Captured bytes | PASS: the hashes of all seven packet ranges equal the image. The control check set leaves this check out. |

### Claim 1: record+28h to `001D6A20`

| Claim | Result |
|---|---|
| 59F1B0 loads the DWORD record+28h into EDX | PASS: `mov edx, dword ptr [r15 + 0x28]` (4 B), then rcx = r15 and `call 0059A9B0`. r15 = incoming rcx (59EEC4), with no other writer except the epilogue pop. |
| The load is armed by r12b | PASS: 59F1AB `test r12b, r12b` / 59F1AE `je` skips the load and the call |
| `0059A9B0` saves the key in ESI | PASS: 59A9C3 `mov esi, edx` comes before 59A9CA `setne dl` and has no earlier rdx write. rsi has only that writer plus the two epilogue restores. 59A9C3 dominates 59AAA4, and no rsi writer lies on any path between them (56 instructions). |
| ECX = ESI at the insertion call | PASS: 59AAA2 `mov ecx, esi`, then 59AAA4 `call 001D6A20`. No value-changing operation writes rsi anywhere in the body. |
| Size, selector and pointer are separate arguments | PASS: r8d = edi = record+0 (59A9C5), r9d = sign-extended byte record+18h (59AA93), rdx = `lea [rsp+50h]`, the slot holding the `001D6BB0` result |

ESI survives eight callees between 59A9C3 and 59AAA4, and only the Win64 nonvolatile ABI keeps it. They are
`001D6BB0`, `002150E0`, `001D6CA0`, `005CDAA0`, `002150D0`, and the imports ReadFile, SetEndOfFile and CloseHandle.

### Claim 2: the lookup's out-key

| Claim | Result |
|---|---|
| The out-key is the fifth argument, record+28h | PASS: at 59EFD7 `lea r9, [r15 + 0x28]`, with no r9 write before 59EFE5 `call 001D6D20`. 1D6D34 `mov rbx, r9` and 1D6D47 `mov [rsp+20h], rbx`, with a frame of 38h, place it at the callee's entry SP+28h. In `001D6D20`, rbx has no other writer and all memory writes are to its own stack. |
| `0020C1B0` holds it in R14 | PASS: five pushes + `sub rsp, 150h` give a frame of 178h. 20C1EE `mov r14, [rsp+1A0h]` reads entry SP+28h. r14 has only that writer plus the epilogue pop, and it is used only as a memory base. |
| Nonempty key: hash, then a fresh store before hit/miss | PASS: 20C228 `call 00674A00` is followed directly by 20C22D `mov dword ptr [r14], eax`, the only write through r14. 20C22D dominates both the hit (20C284) and the miss (20C2BE). Every entry → ret path passes it, except one that takes the 20C21D → 20C2C7 edge. |
| The hash clears bit 31 on every exit | PASS: `00674A00` = seed 1505h, `imul eax, eax, 21h` + the sign-extended byte, then 674A23 `btr eax, 1Fh`, then `ret`. It has one exit. The btr dominates it, and eax is not written between them. There is no call and no memory write. The stored key is in 0 to 2^31 - 1. |
| Empty key: no hash, no out-key write, return −1 | PASS: 20C218 `cmp byte [rsp+40h], 0` (the first byte of the memset buffer that `0020C440` fills) leads to 20C21D `je 20C2C7`. 20C2C7 is `or rax, -1`. Nothing reachable from it writes through r14, calls the hash or rewrites rax. Its only call is `00808C40`, whose returning path writes no rax. |

### Claim 3: composition

| Claim | Result |
|---|---|
| A commit needs a negative lookup result | PASS: 59EFF1 `js`. From 59EFF3 (non-negative result), 59F1B0 is unreachable. |
| An armed commit has passed the lookup | PASS: r12b's only writers are 59EED6 `xor`, 59EFC4 `mov r12b, 1` and 59EFCE `setne`, plus the pop. In the reviewer's own interpretation, the single state at 59F1B7 has r12b = 1 and lookup-seen. |
| The resolver never writes record+28h | PASS: across the whole body, writes through r15 are +0/4, +10h/8, +18h/1 and +20h/8. The +20h QWORD ends at +27h. On the 142 instructions between the lookup's return and 59F1B0, r15 is used only as a memory base, so no callee there receives a record pointer. |
| `0059A9B0` writes no record+28h before 1D6A20 | PASS: rbx-based writes are +0, +8 and +10h. In any case, the key is already in ESI at entry. |

**The rule as re-derived.** Assume these premises:

- (a) r15 is a valid record, and record+28h..2Bh does not overlap any of these:
  - the resolver's frame and its three alloca buffers;
  - the local at `[rbp]`;
  - the frames of `001D6D20` and `0020C1B0`.
- (b) Every callee returns normally and keeps r12, r14, r15, rbx and rsi (Win64 ABI).
- (c) No opaque callee writes record+28h through state it already holds, such as globals. Locally, none is passed a
  record pointer. The opaque callees are:
  - `0020C700`, `00861EC0`, `0020C440` and `00808C40` in the lookup;
  - `00808F10`, `00599250`, `0017D2E0`, `0019B1F0`, `0019AEE0` and `00215280` after it.
- (d) No concurrent writer exists.

Under those premises, suppose the 59EFE5 lookup takes the empty arm, and both `0019AEE0` and `001D6BB0` return
non-null with r12b armed. Then the key that 59AAA4 passes to `001D6A20` is the DWORD that record+28h held when
59EFE5 was called. It is not a freshly computed hash. With the same no-interference premise for the callees before
59EFE5, it is also the value at resolver entry, because the resolver never writes that field.

### Claim 4: the 606 states

| Claim | Result |
|---|---|
| The packet frames the 606 as analysis states, not executions | PASS: the README says "These are not606 executions…", and result-02's `arm_flag_proof.limits` says "no concrete path length, native execution, archive feasibility or all-caller proof". |

The reviewer's own interpretation reaches 774 states in its own encoding, against the same bound of 1596
(266 × 6). The count depends on the encoding, so the two numbers differ. Neither 606 nor 774 is counted as an
execution anywhere in this review.

### Claim 6: the manifest

PASS. The manifest sha256 begins `f3365d0eb049fb0c`, and all 99 members match.

The retained hash capture's status file has only `exit` and `driver`. It has no terminal flag and no driver hash.
Result-02 labels it `LEGACY_INCOMPLETE_INVOCATION_RECEIPT`. This review keeps that limit: no capture or invocation
credit is given for it. The hash body's bytes were re-read here from the shipping image.

## Controls (13, each must FAIL a named check on a privately patched image; all did)

A null control also runs first: an unchanged private copy, with the sha check off, passes all 52 image checks. The
packet-bytes, README and manifest checks are kept out of the control check set.

1. 674A23 `btr eax, 1Fh` → four nops. Fails the hash-shape check and the "btr dominates the ret" check.
2. 674A0A empty-string `je` retargeted past the btr to the `ret`. Fails "btr dominates the ret".
3. 20C1EE out-key carrier `[rsp+1A0h]` → `[rsp+1A8h]`. Fails the fifth-argument check.
4. 20C22D `mov [r14], eax` → `nop; mov [rsi], eax`. Fails "writes through r14 exactly once".
5. 20C21D empty-key `je` retargeted to 20C22D, which moves the early return after the store. Fails the empty-test
   check and the store-dominance check.
6. 59F1B0 load `[r15+28h]` → `[r15+2Ch]`. Fails the 59F1B0 check.
7. 59AAA2 `mov ecx, esi` → `mov ecx, edi`. Fails the ECX = ESI check.
8. 59AA47 `mov r8d, esi` → `mov esi, r8d`, so `0059A9B0` overwrites ESI before the call. Fails the rsi census and
   the path check.
9. 1D6D47 fifth-argument store `[rsp+20h]` → `[rsp+28h]`. Fails the `001D6D20` mapping.
10. 59EFD7 `lea r9, [r15+28h]` → `[r15+2Ch]`. Fails the call-site check.
11. 59EED6 `xor r12b, r12b` → `mov r12b, 1`. The reviewer's interpretation then finds 2 commit states, one without
    the lookup.
12. 59EFEA `mov [r15+20h], rax` → `[r15+28h]`. Fails "no write overlaps record+28h" and the r15 write census.
13. 1D6D34 `mov rbx, r9` → `mov rbx, r8`. Fails the `001D6D20` mapping.

After all controls, the exe on disk still hashes to `73461d0896204b1c259c`. The packet's six controls-01 CLI refusals and two
publication-guard calls were not repeated. These 13 replace them for this review.

## Narrowings

1. **The insertion has two more gates, and only one of them is stated.**
   - The resolver commits only if `0019AEE0` returns non-null (59F19E). The packet's "successful archive fill"
     covers this gate.
   - `0059A9B0` returns −1 at 59A9F4 without calling `001D6A20` when `001D6BB0` returns null (59A9DF). The packet
     does not state this gate.

   So an armed 59F1B7 call is not yet an insertion.
2. **"Empty" means only that the buffer's first byte is still 0.** The empty arm is taken whenever byte 0 of the
   memset buffer is still 0 after `0020C440`. That happens on any normalizer exit that writes nothing as well as on
   a genuinely empty normalized name. Which inputs produce it belongs to the normalizer's own packet, not this one.
3. **The nonempty key is re-read through memory.** After the fresh store, `0020C1B0` reads the out-key back through
   r14 three times: the tree compares at 20C252 and 20C273, and the `0020C300` argument at 20C2A2. These reads
   follow the lock call `005CD4F0`. Even the nonempty hit/miss decision therefore uses the memory value, which is
   the fresh hash only under the same non-alias / no-interference premise.
4. **.pdata wording.** The image's exception directory has a single record for the resolver, with flags 3. It
   covers `0059EE90` + 0x36C, including the epilogue from 59F1E2 to the `ret` at 59F1FB. No record in the image ends
   at 59F1E2. The packet's "beyond its prepared .pdata fragment" therefore describes its own preparation input, not
   the image. The byte total is unaffected.
5. **The hash detail.** The 33-multiplicative hash adds each byte sign-extended (`movsx`), with seed 1505h. It has
   one exit, so "all exits pass BTR" means that one exit. The range 0 to 2^31 - 1 is unaffected.
6. **Callees that hold the key.** ESI survives eight callees, three of them imports, and only by ABI. The key is
   also passed as r8d to the `005CDAA0` message at 59AA47 on the size-mismatch path. It is passed by value there, so ESI itself still depends only on the ABI.

## Limits (kept as the packet states them)

This review supports conditional static facts only, under premises (a) to (d) above. The following remain open and
are not awarded:

- a natural shipped-game request that normalizes empty;
- an empty-normalized request that then hits the archive;
- a natural high-bit cache key. The 31-bit domain applies to the fresh nonempty key only and is not a universal
  insertion-domain claim;
- the initial value of source-record+28h, the record's lifetime and reuse;
- all callers, including indirect or external ones, and actual archive feasibility;
- native callback, allocator and import effects, and concurrency.

The retained hash capture stays incomplete, with no capture credit.

run: `rv_route2.py` at f348f2f1d (72 checks, 72 PASS, 0 FAIL, 13 controls; output identical to [`rv_route2.out`](rv_route2.out))
