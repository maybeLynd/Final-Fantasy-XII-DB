# FABLE review: ASTRA ov42-caller-row-preconditions

- **Packet:** [ov42-caller-row-preconditions README](../../../_experiments/evidence/ov42-caller-row-preconditions/README.md)
  (board request `ASTRA-REQ-FABLE-OV42-CALLER-ROW-1002`).
- **Producer commit:** `103aa3123`. The manifest sha256 begins `5a49e70f7d355aa7` and equals the committed manifest.
  All 55 members hash as listed. The 9 source ranges of `current-row-source-01/02.json` and `helper-source-01.json`
  hash to the certified image's bytes, and their instruction records concatenate to them. `helper-extents-01.json`
  equals the image's `.pdata` records for `00305430` (517 B) and `0030D160` (1004 B). The retained copies are
  byte-identical to their sources (`git ls-tree` + `cat-file`): `current-row-source-01/02.json` to `fd45553c7`'s
  `autoattack-commit-exception/retained/` members, and `carrier-manifest.json`, `carrier-result-01.json` and
  `action_data_us.st2e` to `c40b24340`'s `summon-kind-row-carrier` members. The st2e is also the byte-identical slice
  of the shipped US `battle_pack.bin` at offset 78352 (the game extract on D:).
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every byte-level claim re-derives:
  - the latched carriers: the target builder gets the getter's AX zero-extended, the sequence gets R15 built from
    the entry WORD `+0x714`, and the helper gets that latched WORD, with its EAX overwritten untested;
  - the builder's own row, built from its own descriptor and lookup reads;
  - the phase-8/9 entries (`+ 0x663`, `+ 0x66E`, 161 and 158 instructions visited), and no readiness or
    acquisition call reachable from them;
  - the helper's two unsigned 16-bit bounds and its 278..542 arm, and for 511..534 under the US-table binding:
    two lookups, no own non-stack write, return 0;
  - the bit-6 positive control.

  An emulation of the original routine from its entry (phases 6, 8 and 9), of the helper and of the builder's prefix
  agrees on every case tried. The narrowings bound what "entry snapshot" and "not rerun" mean, state when the two
  carriers agree, and show that the builder's indirect call is not virtual. None of them contradicts the packet, and
  none settles natural pairing.

## Method

[rv_callerrow.py](rv_callerrow.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). The
reader is copied unchanged from the kind-row review (sha256 `69f9bc40be32abcc32b1`). The script does not import or
run any of ASTRA's scripts: `prove.py`, `prove_owner_reload_order.py`, `run.py`, `control.py`, `capture-helpers.py`,
`capture-index-path.py`, `prepare-helper-extents.py` and `validate-title-source-annotations.py` are all left alone,
and so is `reg_tracking.py`. It works as follows:

- **Reading the code.**
  - It checks the image sha256 (`73461d0896204b1c259c`).
  - It follows the battle-action routine `00304850`'s seven chained `.pdata` records. It decodes the routine's 2034
    code bytes exactly, reads the 13 DWORD phase entries after the code, and re-reads the entry latch, the entry
    guard, the R15 formula and the case-8/9 argument transfers. Operand widths come from the instruction bytes, and
    register-write censuses run on the local CFG.
  - It computes reach and dominance from the phase entries, both with the switch resolved to one entry from the
    routine's entry and from the case entries themselves.
  - It decodes the builder `0030D160` (nine chained records) and the helper `00305430` (one record) exactly.
  - It reads the retained US table directly.
- **Emulation.** It emulates the **original** bytes with unicorn:
  - `00304850` from its entry, with every callee stubbed by a code hook. A stub returns at once with a scripted
    RAX and clobbers RCX, RDX and R8-R11. The cookie check preserves RAX, as its body does.
  - `00305430` from its entry, with `0020E600` bound to the US table (it returns table + key) and its other five
    callees stubbed.
  - `0030D160` from its entry to its first call after the row is formed.
  - The runs: phases 6, 8 and 9 with W = 511; W = 0..542 at phase 9; the entry guard at `0x21F` and `0x21E`; a null
    descriptor; a builder stub that rewrites `+0x714`; four helper return values; the helper on 511..534 and on
    all of 278..542; a bit-6 table copy; null descriptor and null first lookup; lookup returns with upper bits set.
- **Census.** It takes a raw `E8`/`E9` rel32 and `0F 8x` census for `00304850`, `0030D160`, `00305430`, `00306760`
  and the builder's two indirect targets. It also takes a census of the routine's rip-relative accesses to
  `022C2150` .. `022C2180`.
- **Controls.** Each control patches a private in-memory copy of the image, or a private copy of the table. The exe
  on disk is never written, and its sha256 is rechecked after all controls.

Raw output: [rv_callerrow.out](rv_callerrow.out).

## Re-derived (68 checks, 68 PASS, 0 FAIL; 15 controls among them)

### The routine and its phase switch

| Claim | Result |
|---|---|
| Complete 2034-byte caller through its one `ret` | PASS: seven records tile `00304850` .. + 0x828 (the root, then six CHAININFO records resolving to it). + 0 .. + 0x7F2 decodes exactly. The one `ret` is the last instruction (+ 0x7F1). A 2-byte NOP and 13 DWORDs (+ 0x7F4 .. + 0x828) follow; they are data. |
| The 52-byte phase switch | PASS: + 0xEC reads BYTE `[rsi + 4]` = unit + 0x6B4, `cmp eax, 0xc` / `ja` + 0x7B6, and + 0x10A `jmp rcx` is the body's only indirect jump. The 13 entries land on instruction boundaries: entry 6 = + 0x555, 7 = + 0x5DC, **8 = + 0x663, 9 = + 0x66E** (the packet's two dispatch targets). |
| Entry latch of `unit+0x714` | PASS: + 0x3D `movzx r13d, word ptr [rsi + 0x64]` (2 B; RSI = unit + 0x6B0 from + 0x2F). R13 is written only there, by `sub r13w, ax` (+ 0x6B5, *after* the helper call) and by the restore. RDI = unit, RSI and R12 are written once each and restored. |
| R15 = zeroextend32(second lookup + ID * WORD(third descriptor + 8)) | PASS: three QWORD loads of `02EBF138` (+ 0x98, + 0xC0, + 0xD2); lookups + 0xB6, + 0xCA; + 0xCF `mov r15, rax`; + 0xDD `movzx eax, r13w`; + 0xE1 `imul ecx, eax`; + 0xE4 `add r15d, ecx` (`44 03 F9`, 32-bit, zero-extends). A null descriptor or a null first lookup gives R15 = R14 = 0 (+ 0xE9). |

### The phase-8/9 entries

| Claim | Result |
|---|---|
| Visited 161 / 158 | PASS: from the routine entry with the switch resolved to entry 8 or 9, the local CFG reaches 161 or 158 instructions. From the case entries alone it reaches 97 and 94. Both case reaches stay at + 0x663 and above. |
| No earlier slot readiness or acquisition | PASS: neither reach contains the readiness call `0030CA80` (+ 0x5EE, case 7) or the acquire call `0030CFB0` (+ 0x5D4, case 6). Emulated: the phase-8 and phase-9 runs call neither. |
| Builder dominates the sequence | PASS: from both entries the builder call (+ 0x692) and the helper call (+ 0x69E) dominate the sequence call (+ 0x6FD). R15 is not written on either reach before + 0x6FD. |

### The carriers

| Claim | Result |
|---|---|
| Target builder gets the getter's AX in EDX | PASS: + 0x675 RCX = QWORD `[rdi + 0x698]`, + 0x67C `call 00387090`, + 0x681 R8D = unit DWORD + 0x710, + 0x685 R9 = unit + 0x778, + 0x68C `movzx edx, ax`, + 0x692 `call 0030D160`. Between the two calls RAX is not written and RDX is written only by the `movzx`. Emulated: a getter return with upper bits set reaches the builder as its AX alone. |
| The builder latches DX and builds its own row | PASS: `0030D160` + 0x27 `movzx edi, dx` is its only RDX read before its first call. It forms RSI from three loads of `02EBF138` (+ 0x3B, + 0x66, + 0x78), lookups + 0x5C and + 0x70, `imul` + 0x86 and the 32-bit `add esi, ecx` + 0x89. Before + 0x21 `mov r15, r9` its only R15 access is the `push r15` save. Emulated: RSI = the row of DX for three different incoming R15 values. |
| The sequence gets R15 | PASS: + 0x6F7 `mov rdx, r15`, + 0x6FA `mov rcx, rdi`, + 0x6FD `call 00306760`. Emulated: for W = 0..542, the sequence gets the row of W whenever that row has bit 30 of `+0x0C`. The builder always gets the getter's word. |
| The helper gets the latched WORD; its EAX is overwritten untested | PASS: + 0x697 `movzx edx, r13w`, + 0x69E `call 00305430`. The next instruction, + 0x6A3 `movabs rax` (bit 46), writes RAX without reading RAX or the flags. Emulated: helper returns of 0, 1, -1 and 2^64 - 1 give identical later calls, arguments, writes and return. When the builder stub rewrites `+0x714`, the helper and the sequence still get the entry word. |
| No owner or kind re-check | PASS: the routine's rip-relative accesses to `022C2150` .. `022C2180` are two. One is the one-shot flag test of `022C2158` (+ 0x4F9, not on the phase-8/9 reach). The other is the state read of `022C2160` (+ 0x71C, after the sequence call). Nothing reads the kind `022C215C` or the owner `022C2168`. |

### The helper `00305430`

| Claim | Result |
|---|---|
| 517 bytes, complete decoding | PASS: one record, `00305430` .. + 0x205. It decodes exactly and has four rets (+ 0xE5, + 0x147, + 0x1D8, + 0x204). |
| Unsigned 16-bit bounds enter the 278..542 arm | PASS: + 0x1D `movzx edi, dx`; + 0x23 `cmp dx, ax` (`66 3B D0`) against `0x115`, `ja` + 0x148; + 0x150 `sub ax, cx` (DI - `0x116`) and + 0x158 `cmp ax, cx` against `0x108`, then `ja` + 0x1D9. |
| Bit 6 clear: two lookups, no own non-stack writes, return 0 | PASS: the arm reads the descriptor (loaded at + 0xF, not rewritten on the `ja` path) and makes lookups + 0x166 and + 0x17A. It forms a 32-bit row (+ 0x190 `add ebx, eax`) and tests bit 6 of row byte `+0x2C` (+ 0x192). `je` + 0x1D9 then `cmp di, 0x113` / `jne` + 0x1F3 leads to `xor eax, eax` / ret. `0x113` is outside 278..542, so no further call. The arm writes nothing but its stack. Emulated for 511..534 (EDX upper half set): RAX = 0, exactly two `0020E600` calls, no write outside the stack. |
| The US rows 511..534 have bit 6 clear | PASS: st2e count 543, stride 60, data at + 0x20. Rows 511..534 have `+0x2C` = 0, bit 30 of `+0x0C` set and `+0x1E` = 7. The 24 cases in `result-01.json` equal this reading and the emulation. |
| A supplied bit-6 row reaches `00311F70` | PASS (emulated, private table copy): row 511 with bit 6 set gives `0031B7E0`, then `00311F70` with RCX = unit, RDX = the owner and R8D = 1, then return 0. |

### The builder's opaque boundaries

PASS: `0030D160` makes 22 calls, and they are exactly the packet's 22 `builder_opaque_boundaries`. One of them is the
indirect `call rax` (+ 0x22D); see narrowing 5.

### Census

PASS: raw direct references, `E8`/`E9` and `0F 8x`:

- `00304850` has one, `00307BE0` + 0x39.
- `0030D160`, `00305430` and `00306760` have one each, all from `00304850` (+ 0x692, + 0x69E, + 0x6FD).

The census does not cover indirect callers.

### Packet integrity

PASS: the manifest, the members, the ranges, the extents, the lineage and the st2e provenance (see the header). The
README keeps natural pairing, initialization and opaque helper interference open, and forbids closing OV-42 or
inferring natural impossibility.

## Controls (15, each must FAIL a named check on a privately patched image or table; all did)

A null control runs first: an unchanged private copy passes all 40 image checks.

1. Caller + 0x68C `movzx edx, ax` → `mov edx, eax` + NOP. Fails the builder-transfer check and the emulated carriers.
2. Caller + 0x697 `movzx edx, r13w` → `movzx edx, ax` + NOP. Fails the helper check and the emulated carriers.
3. Caller + 0x6F7 `mov rdx, r15` → `mov rdx, r14`. Fails the sequence-leg check and the emulated carriers.
4. Caller + 0x6A3 `movabs` → `test eax, eax` / `jne` + 0x7BA (the helper's return tested). Fails the ignored-return check and the emulated runs.
5. Caller latch WORD `[rsi + 0x64]` → `[rsi + 0x66]`. Fails the latch check and the emulated carriers.
6. Caller phase entry 9 → + 0x5DC (case 7, which calls `0030CA80`). Fails the table check and the emulated runs.
7. Caller entry guard `ja` → `jae`. Fails the guard check, the sweep and the emulated guard.
8. Caller `cmp r13w, 0x21` → `0x22` (the D0..F1 skip widened). Fails the sequence-leg check and the sweep.
9. Caller + 0xE4 `add r15d, ecx` → `add r15d, eax` (row = base + id). Fails the R15 check and the emulated carriers.
10. Builder + 0x27 `movzx edi, dx` → `mov edi, r8d`. Fails the latch check and the emulated builder row.
11. Builder + 0x21 `mov r15, r9` → `mov r9, r15` (the caller's R15 read). Fails the R15 check and the emulated builder.
12. Helper + 0x196 `je` → `jne` (bit 6 inverted). Fails the arm check and the emulated stock and arm checks.
13. Helper + 0x1E1 `jne` → `je`. Fails the emulated stock, arm and null checks.
14. Helper arm base `0x116` → `0x200`. Fails the bounds check and the emulated stock and arm checks.
15. Table copy: row 520's `+0x2C` bit 6 set. Fails the table check and the emulated stock check.

After all controls, the exe on disk still hashes to `73461d0896204b1c259c`. The packet's four CLI refusals and four
source/resource controls were not repeated. These 15 replace them for this review.

## Narrowings

1. **"Entry snapshot" means this invocation's entry, and it is guarded.** Every invocation of the routine latches
   `+0x714` and builds R15 *before* its phase switch. No snapshot carries over from an earlier invocation. An entry
   word above 542 returns -1 before the switch (+ 0x8E `cmp r13w, bx` with `0x21E`, unsigned `ja`; emulated). So the
   terminal phase runs only for latched words 0..542, which include 511..534. With a null descriptor or a null first
   lookup, R15 is 0, and the first row test (+ 0x6D2) reads address 0xC. That is a source prediction (emulated).
2. **"Not rerun" holds only for invocations that enter at case 8 or 9.** Case 6 ends in `inc` (+ 0x5D9) and falls
   into case 7. Case 7 keeps `0030CA80`'s EAX in EBX and leaves when EBX is 0 or unit bit 12 is set. Otherwise it
   falls into case 8 (+ 0x660 → + 0x663). The emulated case-6 run makes these calls, in order:
   - the getter, then `0030CFB0` with R8 = the first getter word;
   - `0030CA80`, then `00319420`;
   - the getter again, then the terminal calls, with the builder getting the *second* getter word.

   So the acquisition, the readiness call and the terminal phase can share one invocation, with two separate getter
   reads.
3. **When the two carriers agree.** The builder's word is the getter's return. That is O2's `+0x714`, or record WORD
   `+0x10` when the word is `0x9F` and a record was selected (effective-id review). The sequence's word is this unit's
   `+0x714` at entry. They name the same row only if all of these hold:
   - O2 is this unit;
   - the word is unchanged between the entry and the case-9 getter call (case 8's `00319420` and, on a fall-through,
     cases 6 and 7 run in between);
   - the word is not `0x9F` with a record selected.

   None of these is established. The two rows also come from separate descriptor reads: three loads and two lookups
   at the routine's entry, and three loads and two lookups in the builder.
4. **Rows are 32-bit pointers in all three bodies.** The routine (+ 0xE4), the builder (+ 0x89) and the helper
   (+ 0x190) all add the base's low 32 bits with a 32-bit `add`, which zero-extends. The table must lie below 4 GB
   for these rows to address it. Emulated: lookup returns with upper bits 5 or 7 still address the low-32 row. The
   helper's arm has no null guard either. A null descriptor, or a null first lookup, reads address 0x2C (emulated).
   That is a source prediction, not an observed fault.
5. **The builder's indirect call is not virtual.** + 0x22D `call rax` has two fixed targets, both `.pdata` roots:
   - `0030BB10`, from the `lea` at + 0x21C;
   - `0030BCB0`, from RBP, set by the `lea`s at + 0x1C6 and + 0x2C7. RBP's other writes (+ 0x327, + 0x3B4) do not
     reach + 0x22D.

   The pick is bit 2 of the row's WORD `+0x36` (+ 0x214 `test al, 4`, + 0x226 `cmovne`). The call is skipped when
   bit 3 is set. Neither body is read here. Other raw direct callers: `0030BB10` has 1, `0030BCB0` has 5.
6. **Which stock rows reach the helper's effect call.** In 278..542, bit 6 of `+0x2C` is set only on US rows 325,
   326, 416, 417, 436 and 455. Emulated over all 265 arm ids: those reach the owner lookup `0031B7E0`, and then
   `00311F70(unit, owner, 1)`, except 455 (`0x1C7`), which returns 0 after the lookup. On the bit-6 path the helper
   returns -1 when the owner lookup is null. The routine ignores that return as well. So "no own writes" for
   511..534 is a property of those table bytes under the binding premise, not of the helper alone.
7. **The routine reads row bit 30 three times.** The reads are at + 0x6D2, + 0x6ED and + 0x712. The first sits
   before `00305640`, the second after it, and the third after the sequence. A callee that changed the row's bit 30
   would change the path. Nothing here reads whether one does.

## What stays OPEN (kept as the packet states them)

This review supports conditional static facts, plus emulation of the original bytes on synthetic state and the
retained US table. The following remain open and are not awarded:

- **natural pairing** of the classifier's row (`0030CBE0`'s slot word, kind-row review) with this routine's entry
  `+0x714`. That includes the writers of `+0x714` and of the phase byte `+0x6B4`, and whether a natural invocation
  enters at case 8 or 9 or falls through from 6 or 7;
- the global kind and owner persistence between the classifier and the queue dispatch (kind-row review);
- the getter's owner O2 being this unit, and the initialized descriptor and table binding. The stable US binding,
  the table below 4 GB and a positive stride are premises;
- the native effects of every stubbed callee between the row construction and the sequence: the getter, the
  builder's 22 calls (and its two indirect targets), the helper's lookups and its effect call, `00319420`, the
  preview `00303830` and the cost helper `00305640` (see the companion review of `ov42-terminal-resource-helper`);
- normal gameplay reachability, timing, lifetime and whole OV-42. No natural-impossibility claim is made for 511..534.

Valid, readable, stable unit, row, descriptor and frame accesses, the normal Win64 ABI and preserved nonvolatile
registers are premises. All emulated values come from supplied states, not native runs.

run: `rv_callerrow.py` at HEAD c7e2bb2a1 (68 checks, 68 PASS, 0 FAIL, 15 controls; output identical to [`rv_callerrow.out`](rv_callerrow.out))
