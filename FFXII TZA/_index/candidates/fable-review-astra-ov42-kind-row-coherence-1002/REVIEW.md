# FABLE review: ASTRA ov42-kind-row-coherence

- **Packet:** [ov42-kind-row-coherence README](../../../_experiments/evidence/ov42-kind-row-coherence/README.md)
- **Producer commit:** `d83287255`. The manifest sha256 begins `dfea4a7f12fe6ab3` and equals the committed manifest.
  All 48 members hash as listed. The packet's ranges hash to the certified image's bytes: the new suffix
  `00306C5B` .. `00306CEC` (145 B, its 37 instruction records concatenate to it), the retained prefix `00306BD0` ..
  `00306C5B` (139 B) and the retained queue range `00306760` .. + 0x38F. The 440-byte physical body (sha256
  `27683107a3bb...`), the seven DWORDs and the 128 selector bytes in `data-01.json`, the `.pdata` records in
  `extent-01.json` and the seven arms in `result-02.json` all equal this review's own reading.
  `retained-prefix-01.json` is byte-identical to `318e510c`'s `special-admission-raw-01.json`.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every claim re-derives at the bytes: the three-record extent and its
  code / DWORD / selector split, the full unsigned 32-bit quotient, the two descriptor loads, the zero-extended WORD
  divisor, the absence of any narrowing before the 32-bit `add eax, -0x94` / unsigned `cmp eax, 0x7f` guard, kind 4
  exactly for q = 208..225, the queue's separate low-16 narrowing, the conditional invariant, both countermodels, and
  the unused `0032FC30` return. An emulation of the original classifier and of the queue's kind-4 arm agrees on
  every case tried. The narrowings add side facts, the kind cell's direct writers and the one direct caller. None
  contradicts the packet's conditional result, and none settles natural kind-to-row consistency.

## Method

[rv_kindrow.py](rv_kindrow.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is
copied unchanged from the sequence-queue review (sha256 `69f9bc40be32abcc32b1`). It does not import or run ASTRA's
`prove.py`, `prove_owner_reload_order.py`, `history-prove-before-retained-path-fix.py`, `capture*.py`, `extent.py`,
`control.py`, `validate-title-source-annotations.py`, freeze or publication scripts, or `reg_tracking.py`. It works as
follows:

- It checks the image sha256 (`73461d0896204b1c259c`). It follows `00306BD0`'s `.pdata` records and checks that
  they tile the physical extent. It decodes the 284 code bytes linearly and exactly, and checks that the 28 DWORD
  bytes and 128 selector bytes after the last `ret` are never branched to and are exactly what the two indexed loads
  address.
- It re-reads the quotient and the guard with operand widths taken from the instruction bytes, and takes register-
  write censuses (RSI, RAX, RBX, RCX, RDX) between the row's entry, the `div`, the guard and the jump.
- It resolves the seven DWORDs and, from each target, follows the local CFG to the kind store to find the last EBX
  writer. It enumerates all 128 selector bytes into the full q → kind map.
- It reads the return use of `0032FC30` as a def-use question (who reads RAX or the flags before RAX is next
  written), and it decodes the next callee `0032ED70`.
- It emulates the **original** classifier from its entry (unicorn). `0032F6E0`, `00309230`, `0032FC30` and
  `0020E600` are stubbed by a code hook that returns at once with a scripted RAX; those four are the only code not
  run from the image (`0032ED70` runs from the image). The runs are: one fully inspected call; q = 0..512; 15
  full-32 edge cases; 200 random 64-bit rows, lookup returns and strides; a descriptor repointed during the lookup
  call; a zero stride; five entry-gate cases; and five `0032FC30` return values. It emulates the queue's kind-4 arm
  `00306760` + 0xE8 .. + 0x17A as the sequence-queue review did, for the consistency and countermodel checks.
- It runs a raw `E8`/`E9` rel32 and `0F 8x` census over `.text` for `00306BD0` and its caller `0030CE10`, a disp32
  census and a pointer-value scan for `00306BD0`, and a disp32 census (rip-relative and image-base-relative, decoded
  from each hit's `.pdata` record) of every instruction whose access covers the kind cell `022C215C`, and of the
  owner cell `022C2168`.
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is
  rechecked after all controls.

Raw output: [rv_kindrow.out](rv_kindrow.out).

## Re-derived (75 checks, 75 PASS, 0 FAIL; 18 controls among them)

### Extent

| Claim | Result |
|---|---|
| Three chained records, 440 physical bytes | PASS: the root `00306BD0` .. + 0x35 and two CHAININFO records + 0x35 .. + 0x6D and + 0x6D .. + 0x1B8 tile the extent exactly, each resolving to the root. int3 padding follows to the next root `00306D90`. |
| 284 code bytes ending at the RET at `00306CEB` | PASS: + 0 .. + 0x11C decodes exactly. Its last instruction is the `ret` at + 0x11B (`00306CEB`). There are three rets (+ 0x2B, + 0x6C, + 0x11B). The local CFG is closed: one indirect `jmp rcx` (+ 0xD7), no tail jump, no branch into + 0x11C .. + 0x1B8. |
| Seven DWORDs `00306CEC` .. `00306D08`, 128 selector bytes `00306D08` .. + 0x80 | PASS: the loads are `movzx eax, byte ptr [rdx + rax + 0x1e6d08]` (1 B) and `mov ecx, dword ptr [rdx + rax*4 + 0x1e6cec]` (4 B), with RDX = the image base `0x120000` from a rip-relative `lea` (+ 0xBE); image base + 0x1E6D08 = `00306D08`, + 0x1E6CEC = `00306CEC`. Nothing writes RDX between the `lea` and the `jmp`. |

### The quotient (claim 2)

| Claim | Result |
|---|---|
| The row is the entry RDX | PASS: `mov rsi, rdx` (+ 0x10), with no RDX write before it. RSI is written only there, by the two early-return restores (+ 0x21, + 0x62, which do not reach + 0xA1), by `sub esi, eax` (+ 0xA1) and by the final restore (+ 0x101). The five calls before + 0xA1 preserve RSI only under the Win64 ABI. |
| `D = (low32(row) - low32(base)) mod 2^32` | PASS: + 0x92 loads QWORD `02EBF138`, + 0x99 takes DWORD `+0xC` into ECX, + 0x9C calls `0020E600`, and + 0xA1 is `sub esi, eax` (`2B F0`, 32-bit). Emulated: upper 32 bits of the row or of the lookup return change nothing; a row 60 below the base wraps to q = 71582787. |
| Divisor = zero-extended `u16(second load + 8)`; unsigned 32-bit `div` | PASS: + 0xA3 `xor edx, edx`, + 0xA5 a second QWORD load of `02EBF138`, + 0xAC `movzx ecx, word ptr [rax + 8]` (2 B), + 0xB0 `mov eax, esi`, + 0xB2 `div ecx` (`F7 F1`). Emulated: stride FFFF is 65535. |
| Two separate loads; key from the first, divisor from the second | PASS: they are the body's only two loads of `02EBF138`, with the lookup call between. Emulated: when the lookup stub repoints the cell, the key is the first descriptor's `+0xC` (1D74) and the divisor the second's `+8` (30), so 60 * 104 / 30 = 208 publishes kind 4 where the first descriptor's stride would give q = 104 and kind 7. |
| No divisor guard | PASS: no `cmp`, `test` or jcc from + 0x8B to the `div`. Nothing writes ECX between the WORD load and the `div`. EDX is written only by the `xor`. Emulated: a zero WORD raises #DE at + 0xB2 and the kind cell is not written. That is a source prediction, not an observed fault. |
| No narrowing of q before the guard | PASS: the instruction after the `div` is + 0xB4 `add eax, 0xffffff6c` (`05 6C FF FF FF`: 32-bit, no `66` prefix), then + 0xB9 `cmp eax, 0x7f` (`83 F8 7F`, 32-bit) and + 0xBC `ja` + 0xFC (`77`, unsigned). Between the `div` and the `ja`, only the `add` writes RAX. |

### The kinds (claim 3)

| Claim | Result |
|---|---|
| Selector bytes and DWORD targets | PASS: all 128 selector bytes are in 0..6. The seven DWORDs resolve to instruction boundaries: sel 0 → + 0xEE, 1 → + 0xF5, 2 → + 0x101, 3 → + 0xE7, 4 → + 0xD9, 5 → + 0xE0, 6 → + 0xFC. |
| Published kind per target | PASS: following each target to the store + 0x10B, the last EBX writer gives sel 0 → 5, 1 → 6, 3 → 4, 4 → 1, 5 → 2, 6 → 7. Sel 2's target is + 0x101 itself, with no EBX writer: the published value is EBX's initial `mov ebx, 3` (+ 0x3A) (narrowing 1). The `ja` default + 0xFC publishes 7. These equal `result-02.json`'s seven arms. |
| The full map | PASS: for q = 0x94 + x, x = 0..127: **148 → 5; 149 → 6; 150..181 → 7; 182..207 → 3; 208..225 → 4; 226..261 → 7; 262..274 → 1; 275 → 2.** Since q ↦ (q - 0x94) mod 2^32 is a bijection, exactly q = 148..275 pass the unsigned guard; every other 32-bit q, including 0..147, publishes 7. **Kind 4 is published exactly for q = 208..225.** |
| Emulated | PASS: q = 0..512 (stride 60, with in-stride remainders) publishes the derived kind every time, and kind 4 exactly for 208..225. 15 edge cases (65744 = `0x100D0`, `0x10000` + 225, `0x10094`, 147, 0, FFFFFFFF, `0x80000000` + 210, upper row/lookup bits, a row below the base, stride FFFF and 8000, 148, 275, 276) and 200 random rows / lookup returns / strides all agree with map(((low32(row) - low32(base)) mod 2^32) // stride). Over q = 0 .. 0x2FFFF only 208..225 map to kind 4. |
| The kind store and the return | PASS: + 0x10B `mov dword ptr [rip + ...], ebx` to `022C215C` (4 B) is the body's only write to it. With the table edges added, every path from the entry to it passes the `div`. It is followed by EAX = 1 and the last `ret`; the two other rets return EAX = 0 and never reach the store. Emulated: one 4-byte store, kind 4 for q = 210, return 1, RBX/RSI/RDI restored. |

### The queue and the conditional invariant (claim 4)

| Claim | Result |
|---|---|
| The queue narrows its own quotient | PASS (re-read): `00306760` + 0x147 `sub edi, eax`, + 0x152 `movzx ecx, word ptr [rax + 8]`, + 0x158 `div ecx`, + 0x162 `cmp ax, dx` (`66 3B C2`), + 0x167 `movzx eax, ax`, + 0x16A `sub eax, 0xd0`, + 0x174 DWORD store to `022C2178`. This agrees with the sequence-queue review. |
| Kind 4 + equal quotients ⇒ queue 0..17, 511..534 excluded | PASS: kind 4 ⇒ q ∈ 208..225 < 65536, so the low 16 bits are q, never FFFF, and the queue holds q - 208 = 0..17. Emulated on the original queue arm: each of 208..225 stores q - 208. The queue values of ids 511..534 are 303..326, disjoint from 0..17. |
| Countermodel 1 (classifier q 208, queue q 511) | PASS: q 208 maps to kind 4; the emulated queue arm stores 303 (`12F`) for q 511. |
| Countermodel 2 (q 65744) | PASS: 65744 = `0x100D0` maps to kind 7 (the full value is outside 148..275); the emulated queue arm narrows it to 208 and stores 0. The low-16 formula likewise maps `0x100D0`..`0x100E1` and `0x200D0`..`0x200E1` to 0..17, while the classifier publishes kind 7 for all of them. |

### Return use of `0032FC30` (claim 5)

| Claim | Result |
|---|---|
| Not tested before `0032ED70`; RAX killed, then overwritten | PASS: after `call 0032FC30` (+ 0x86) come `mov ecx, ebx` (+ 0x8B), `call 0032ED70` (+ 0x8D) and `mov rax, qword ptr [02EBF138]` (+ 0x92), which writes RAX without reading it. Nothing between reads RAX or the flags, and nothing branches. The callee `0032ED70` (no `.pdata`, a 16-byte leaf) begins `movsxd rax, ecx`, so it overwrites RAX itself (narrowing 4). Emulated: `0032FC30` returning 0, 1, FFFFFFFF, 2^63 or 2^64 - 1 gives identical kinds, returns, writes and `0032ED70` effect for q 207, 208, 225 and 226. |
| The other returns are used | PASS: `0032F6E0`'s EAX is tested (+ 0x57) and `00309230`'s EAX becomes `0032FC30`'s EDX (+ 0x82). |

### Census (claim 6)

| Claim | Result |
|---|---|
| Direct callers of `00306BD0` | PASS: exactly one raw direct reference, the call at `0030CF0D` = `0030CE10` + 0xFD. No direct reference reaches the kind-4 arm + 0xE7, the store or the `div`. No disp32 instruction forms its address, its 8-byte VA does not occur in the file, and its RVA DWORD occurs only in `.pdata` and at the two CHAININFO footers in `.rdata` (`01D74FAC`, `01D74FC0`). |
| The caller passes its own arguments | PASS: `0030CE10` keeps its entry RCX in RSI (+ 0xA) and RDX in RBP (+ 0xD), rewrites neither before + 0xF7 `mov rdx, rbp` / + 0xFA `mov rcx, rsi` / + 0xFD `call`, and on a nonzero return sets bit 29 of QWORD `[rsi]`. `0030CE10` itself has one raw direct caller, `0030CBE0` + 0x1B9 (`0030CD99`). |
| Kind-cell accesses | PASS (narrowing 5): five instructions. |

### Packet integrity

PASS. The manifest sha256 begins `dfea4a7f12fe6ab3` and equals the manifest at `d83287255`, and all 48 members
match. The README keeps open natural caller consistency and the equalities for normal callers, lists what is not
established, and forbids a natural impossibility claim. ASTRA's later addendum (`19e732aa6`) also holds at the
bytes: the 145-byte suffix is already a range of `autoattack-commit-exception/retained/current-row-source-01.json`
with the same sha256 (narrowing 7).

## Controls (18, each must FAIL a named check on a privately patched image; all did)

A null control also runs first: an unchanged private copy passes all 37 image checks.

1. Guard narrowed to 16 bits (+ 0xB4 .. + 0xBC become `add ax, 0xff6c` / `cmp ax, 0x7f`, the `ja` kept). Fails the guard and no-narrowing checks and the emulated full-32 edge cases.
2. `ja` → `jg` (+ 0xBC, a signed guard). Fails the guard check, the emulated sweep and the edge cases.
3. Bias `-0x94` → `-0x93` (+ 0xB5). Fails the guard check, the emulated sweep and the edge cases.
4. The kind-4 arm publishes 7 (+ 0xE8). Fails the per-target, map and emulated checks.
5. Selector byte x = 60 (q 208) `03` → `06`. Fails the map, the emulated sweep and the edge cases.
6. Selector byte x = 59 (q 207) `02` → `03`. Fails the map, the emulated sweep and the invariant.
7. Selector byte x = 100 → `07`, outside the seven DWORDs. Fails the selector-range, map and sweep checks.
8. The DWORD for selector 3 → the kind-7 arm. Fails the target, per-target, map and emulated checks.
9. `mov rsi, rdx` → `mov rsi, rcx` (+ 0x10, the owner as the row). Fails the RSI check and the emulated checks.
10. `sub esi, eax` → `sub esi, ecx` (+ 0xA1). Fails the first-descriptor check and the emulated checks.
11. Divisor WORD → BYTE (+ 0xAC). Fails the second-descriptor check, the edge cases and the zero-stride case.
12. `div ecx` → `idiv ecx` (+ 0xB2). Fails the second-descriptor check, the edge cases and the zero-stride case.
13. The second load `02EBF138` → `02EBF140` (+ 0xA5). Fails the second-descriptor and two-load checks and the emulated checks.
14. The kind store target `022C215C` → `022C2160` (+ 0x10B). Fails the store check and the emulated checks.
15. `mov ecx, ebx` → `mov ecx, eax` (+ 0x8B, `0032FC30`'s return used as `0032ED70`'s argument). Fails the return-use check and the emulated checks.
16. `je` + 0x35 → `jne` (+ 0x18, the entry gate inverted). Fails the emulated run, argument and sweep checks.
17. Queue `movzx eax, ax` → `mov eax, eax` + NOP (`00306760` + 0x167, no low-16 narrowing). Fails the queue re-read and countermodel 2.
18. Queue `sub eax, 0xd0` → `0xd1` (`00306760` + 0x16A). Fails the queue re-read, the invariant and countermodel 1.

After all controls, the exe on disk still hashes to `73461d0896204b1c259c`. The packet's CLI refusals and six source
countermodels were not repeated; these 18 image patches replace them for this review.

## Narrowings

1. **Kind 3 has no arm.** Selector 2's DWORD points at + 0x101, the store's own prologue. The published 3 is the
   `mov ebx, 3` at + 0x3A: the group number the routine also passes to `0032F6E0`, `0032FC30` and `0032ED70`. It
   survives five calls only because the Win64 ABI preserves RBX. `result-02.json`'s "selector 2 → `0x306cd1` → kind
   3" is right, but that target is not an arm. Kind 4 has its own `mov ebx, 4` (+ 0xE7), so the kind-4 band does
   not depend on this.
2. **Kind 7 is not "outside the band".** Within 148..275, kind 7 also covers 150..181 and 226..261. Every quotient
   that reaches the guard publishes some kind 1..7; the cell is never left unchanged after the `div`. The mode-ladder
   page's kind row says "**7** every other id in the range (and any id above `0x113`)". The bytes add the ids below
   `0x94`: q = 0..147 wrap above `0x7F` and publish 7 too. That page is led by the Database prefix; this is noted,
   not corrected, here. The page also says the kind comes "from the action id". It comes from the row quotient, which
   equals an action id only for a row on that descriptor's stride grid.
3. **The kind-publishing path has preconditions.** The entry reads state `022C2160`: 0 continues; 1 continues only
   when the entry RCX equals the QWORD owner in `022C2168`; anything else returns 0 with no call and no write. The
   routine then stores state 1 and the owner (its RCX), calls `0032F6E0(3)`, and returns 0 if that is nonzero (state
   1 and the owner stay written; the kind is untouched). Otherwise it stores state 2, then computes and publishes
   the kind and returns 1. A zero stride faults (#DE, emulated) after state 2 and the owner are written and before
   the kind. The owner compare tests the unit, not the row.
4. **`0032ED70` overwrites RAX itself.** It is a 16-byte leaf without `.pdata`: `movsxd rax, ecx`, `lea rcx,
   [022C6E48]`, `or qword ptr [rcx + rax*8], 1`, `ret`. With ECX = 3 it sets bit 0 of QWORD `022C6E60` and returns
   RAX = 3. So "the latter call kills RAX" holds at the bytes, not only by ABI convention. This is caller-side
   return use; nothing here certifies `0032FC30`'s native effects.
5. **The kind cell's direct writers.** The census of rip-relative and image-base-relative disp32 accesses that
   cover `022C215C` finds five instructions:
   - writes: the classifier's DWORD store (`00306BD0` + 0x10B); a QWORD store of 0 at `00306570` + 0x31, which
     clears kind and state together and is followed by a QWORD 0 to the owner `022C2168` (+ 0x38); and a QWORD
     store of RSI = 0 at `003065D0` + 0x13F (RSI zeroed at + 0x5B, which dominates the store; RSI is written
     nowhere else but the restore), likewise followed by the owner clear (+ 0x146);
   - reads: `003065D0` + 0x63 (the finisher's kind dispatch) and `00306760` + 0x4A (the queue routine's dispatch).

   So within this census only the classifier writes a nonzero kind. Two hits outside any `.pdata` record
   (`00306562`, `00306BA4`) decode to accesses of `022C2158` and `022C2160`, not the kind. The census does not cover
   register-based or aliased writes, block copies or fills, or indirect writers, so persistence is not closed. The
   same census gives `00306760` no access to the owner cell `022C2168`: the queue routine does not compare its unit
   with the recorded owner.
6. **The two rows come from two call chains.** The classifier has one raw direct caller, `0030CE10` + 0xFD, which
   passes its own entry RDX unchanged as the row and its entry RCX as the owner. `0030CE10` has one raw direct
   caller, `0030CBE0` + 0x1B9. The queue routine's one raw direct caller is `00304850` + 0x6FD, which builds its
   row in R15 from its own WORD and the descriptor (sequence-queue review, narrowing 6). So the packet's
   equal-quotient premise relates rows built in two separate routines, at two separate times, from two separate
   descriptor reads. No stored or formed pointer to `00306BD0` exists outside unwind metadata, but computed indirect
   calls are not excluded.
7. **"Newly captured" is qualified by ASTRA's own addendum.** The README says only the missing 145-byte suffix was
   newly captured. ASTRA's addendum `19e732aa6` says the suffix was already retained. This review confirms the
   byte-identical range in `autoattack-commit-exception/retained/current-row-source-01.json`. The conditional
   result is unaffected.

## What stays OPEN (kept as the packet states them)

This review supports conditional static facts, plus emulation of the original bytes on synthetic state. The
following remain open and are not awarded:

- **natural kind-to-row, caller and owner consistency.** That a normal kind-4 queue call carries the same quotient
  the classifier classified is not shown. The rows come from different routines (narrowing 6), and the owner compare
  is not row equality. This review makes no natural-impossibility claim for 511..534.
- the kind's persistence between the classifier and the queue routine's dispatch beyond the direct census
  (narrowing 5), and re-entry between them;
- descriptor initialization, and the stability of `02EBF138` between each pair of loads and across calls
  (`02EBF138` lies in `.data`'s virtual tail); S > 0 is a precondition;
- the native effects of `0032F6E0`, `00309230`, `0032FC30` and `0020E600`, and so the success of the request,
  presentation or scheduling;
- natural queue consumption, command execution, lifetime and reuse, and whole OV-42.

ASTRA's later packet `summon-kind-row-carrier` (`c40b24340`) addresses the `00304850` → `00306760` row carrier. It is
not reviewed here.

The 303 and 0 countermodel values are arithmetic on supplied states, run through the original bytes in emulation,
not native runs. Valid, readable, stable row, descriptor and frame accesses, the normal Win64 ABI and preserved
nonvolatile registers are premises.

run: `rv_kindrow.py` at HEAD 36d76cacb (75 checks, 75 PASS, 0 FAIL, 18 controls; output identical to [`rv_kindrow.out`](rv_kindrow.out))
