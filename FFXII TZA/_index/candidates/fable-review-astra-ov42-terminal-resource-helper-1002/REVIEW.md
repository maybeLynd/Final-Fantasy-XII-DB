# FABLE review: ASTRA ov42-terminal-resource-helper

- **Packet:** [ov42-terminal-resource-helper README](../../../_experiments/evidence/ov42-terminal-resource-helper/README.md)
  (board request `ASTRA-REQ-FABLE-OV42-TERMINAL-HELPER-1002`). It builds on the caller packet
  `ov42-caller-row-preconditions` (`103aa3123`), which FABLE reviewed alongside it:
  [REVIEW](../fable-review-astra-ov42-caller-row-preconditions-1002/REVIEW.md).
- **Producer commit:** `d66234298`. The manifest sha256 begins `11d379a0daaf905a` and equals the committed manifest.
  All 70 members hash as listed. The packet's records match the certified image:
  - `source-01.json` (one range, `00305640` .. + 0x189) hashes to the image's bytes, and its instruction records
    concatenate to them.
  - `extents-01.json` (complete) equals the image's `.pdata` record and bytes (393 B).
  - `caller-source-01.json` is byte-identical to `103aa3123`'s `current-row-source-01.json` (`git ls-tree` +
    `cat-file`).
  - `result-02.json`'s two own writes, ten callee boundaries and 65744 countermodel equal this review's reading.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING** for the source claims, as follows.
  - **Re-derived at the bytes:** the first unsigned 32-bit quotient in EDI; the low-16 cost inputs to `00309110` and
    `00308FF0`; the type-10 counter leg, which rereads the binding and passes the full recomputed quotient with
    ECX 13; the mode 16 + (R8D != 0), with R8D = 1 from the terminal call; the early NULL-unit branch, which gates
    only the `+0xE58` / `+0xDC8` resets; the later unguarded `+0x698` and WORD `+0x28` reads; exactly two own
    non-stack stores; the gil request's low-32 subtraction and signed non-negative pick.
  - **Emulation:** an emulation of the original helper agrees on every case tried.
  - **Not re-run:** the producer-prerequisite repair. Its recorded artifacts were inspected and agree with the README
    (see Packet integrity). Its acceptance is SPEC's.
  - **The main narrowing:** on this call site, under the packet's own equal-binding premise, the shipped tables never
    route a type-10 row here. So the low-16 / full-32 split is real at the bytes but needs an off-premise row to show.

## Method

[rv_termres.py](rv_termres.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). The reader
is copied unchanged from the kind-row review (sha256 `69f9bc40be32abcc32b1`). The script does not import or run any
of ASTRA's scripts: `prove.py`, `prove-before-prerequisite-hardening.py`, `prove_owner_reload_order.py`, `run.py`,
`control.py`, `capture.py`, `capture_prerequisites.py`, `capture-index-path.py`, `prepare-extents.py`,
`qualify-binding.py` and `validate-title-source-annotations.py` are all left alone, and so is `reg_tracking.py`. It
works as follows:

- **Reading the code.**
  - It checks the image sha256 (`73461d0896204b1c259c`).
  - It decodes `00305640` (one `.pdata` record, 393 B) exactly. It re-reads every claim with operand widths taken
    from the instruction bytes and register-write censuses on the local CFG.
  - It re-reads the terminal call in `00304850` and the store that the preceding preview call makes to `+0xE54`.
  - It reads the retained US table (from `103aa3123`), and all nine shipped language tables from the game extract
    on D:.
- **Emulation.** It emulates the **original** `00305640` from its entry with unicorn. Its nine callees are stubbed
  by a code hook, which returns at once with a scripted RAX and clobbers RCX, RDX and R8-R11. The runs:
  - the 65744 discriminator;
  - 200 random strides, quotients and lookup upper halves;
  - six R8 values;
  - three stats-argument cases and six gil cases;
  - the reset gate, a NULL unit, a NULL record and eight row types;
  - the descriptor repointed during `00316440` and during the first lookup;
  - every bit-30 US row outside D0..F1.
- **Census.** It takes a raw `E8`/`E9` and `0F 8x` census of `00305640`'s direct callers and reads the R8 each one
  passes.
- **Producer-repair artifacts.** These are read as recorded: exit codes, flags and stderr. They are not re-run.
- **Controls.** Each control patches a private in-memory copy of the image, or a private copy of the table. The exe
  on disk is never written, and its sha256 is rechecked after all controls.

Raw output: [rv_termres.out](rv_termres.out).

## Re-derived (55 checks, 55 PASS, 0 FAIL; 13 controls among them)

### The helper and its call

| Claim | Result |
|---|---|
| Complete 393-byte original `00305640` .. + 0x189 | PASS: one `.pdata` record, int3 padding to the next root. The body decodes exactly and has one `ret` (+ 0x188, the last instruction). There is no tail jump, no indirect branch and no branch out. Ten direct calls. |
| The terminal invocation supplies unit RCX, current-row RDX and R8D 1 | PASS: `00304850` + 0x6DC `mov r8d, 1`, + 0x6E2 `mov rdx, r15`, + 0x6E5 `mov rcx, rdi`, + 0x6E8 call. It is reached only past + 0x6BE (entry word outside D0..F1) and the row bit-30 test at + 0x6D2. The sequence call + 0x6FD follows only after a second bit-30 test (+ 0x6ED). |
| Entry carriers | PASS: RBP = RCX (+ 0x25), R12D = R8D (+ 0x28), R14 = RDX (+ 0x2B). Each is written nowhere else except R14's counter-leg `sub` (+ 0x130) and the restores. |

### The two ID inputs

| Claim | Result |
|---|---|
| First row quotient: unsigned 32-bit, latched in EDI | PASS: + 0x1E QWORD `[02EBF138]`, then + 0x2E DWORD `+0xC` with no test between (no null guard), + 0x31 `call 0020E600`, + 0x36 a second load of `02EBF138`, + 0x45 `sub r11d, eax` (32-bit), + 0x4B `movzx r10d, word ptr [r9 + 8]` (2 B), + 0x50 `div r10d` (`41 F7 F2`, EDX zeroed at + 0x3D, no zero test), + 0x53 `mov edi, eax`. |
| `00309110` and `00308FF0` get `movzx edx, di` | PASS: + 0x81 and + 0x8C, with RCX = RBP. EDI is not written between + 0x53 and + 0x8C, and both null-test outcomes reach + 0x81. Emulated over 200 random cases: both get q mod 65536. |
| Type 10 rereads the binding and passes the full 32-bit quotient to `00253770` with ECX 13 | PASS: + 0x11C `call 00316440`, + 0x121 and + 0x135 two more loads of `02EBF138`, + 0x12B `call 0020E600`, + 0x130 `sub r14d, eax`, + 0x143 `div ecx` (`F7 F1`), + 0x145 ECX = 13, + 0x14A `mov edx, eax` (`8B D0`, no 16-bit narrowing), + 0x165 call. Emulated over 200 random cases: the counter gets q. |
| 65744 → cost 208, counter 65744 | PASS (emulated, stride 1): `00309110` and `00308FF0` get EDX 208, and `00253770` gets ECX 13 and EDX 65744. This is arithmetic run through the original bytes, not a native call. |
| The two descriptor reads are independent | PASS (emulated): repointing `02EBF138` during `00316440` to a stride-30 descriptor leaves the cost input at 511 and makes the counter input 1022. Repointing it during the first lookup makes the first quotient divide by the second descriptor's stride (cost input 1022). |

### Mode, stats, gil and NULL

| Claim | Result |
|---|---|
| Mode 16 + (R8D != 0) to `00300CE0` and `00300BC0` | PASS: R15D = 0 (+ 0x42) until the `cmovns`; + 0xA0 ESI = R15D; + 0xA3 `test r12d, r12d`; + 0xA8 `setne sil` (the `mov edi, eax` between them writes no flags); + 0xB0 and + 0xC0 `lea r8d, [rsi + 0x10]`, with ESI not written between. Emulated: R8 = 0, 1, 2, 2^31, 2^32 - 1 and 2^32 give 16, 17, 17, 17, 17 and 16 (narrowing 2). |
| Stats arguments | PASS: `00300CE0` gets RCX = QWORD unit `+0x698` (the record) and EDX = -(`00309110`'s EAX). `00300BC0` gets the record reloaded and EDX = -(sign-extended WORD record `+0x28` × `00308FF0`'s EAX), in 32 bits. Emulated with -2 × 3, -32768 × 3 and 5 × (2^32 - 1). |
| Gil request: low-32 subtraction, signed non-negative pick | PASS: + 0xD2 EBX = DWORD unit `+0xE54`, negated; `call 00253690`; + 0xDF `lea edx, [rax + rbx]` (32-bit); + 0xE4 `cmovns r15d, edx`; + 0xEB `call 00254EE0` with ECX = R15D. Emulated: 100 - 30 → 70; 30 - 100 → 0; 5 - 5 → 0 (narrowing 5). |
| The early NULL-unit check gates only the reset | PASS: the one test of RBP is + 0x55 (`je` + 0x81). Every path from the entry to the ret passes + 0x99, which reads `[rbp + 0x698]` with no test. The record is not null-tested before + 0xC4 reads WORD `+0x28`. Emulated: a NULL unit calls `00309110` and `00308FF0`, then reads address 0x698. A NULL record reads 0x28 after `00300CE0`. These are source predictions. |
| The own non-stack stores are the conditional `+0xE58` / `+0xDC8` resets | PASS: the body's only non-stack memory writes are + 0x73 DWORD `[rbp + 0xe58]` := R15D (0) and + 0x7A WORD `[rbp + 0xdc8]` := `0xFFFF`. Emulated: with record byte `+5` = 0 these are the only writes outside the stack. With `+5` = 1 there are none (narrowing 4). |
| The type switch | PASS: with a non-null record and record byte `+5` = 0, the row byte `+0x1E` (read through the entry RDX) selects the final call. Emulated: 0 → (0, 1), 1 → (1, 1), 2 → (2, 1), 10 → (13, q); 3, 7, 9 and 255 make no final call. |

### Census

PASS: `00305640` has four raw direct callers (`E8`/`E9` and `0F 8x`). Indirect callers are not covered.

| Caller | R8 before the call |
|---|---|
| `00304850` + 0x6E8 (the terminal call) | `mov r8d, 1` |
| `00307300` + 0xB9 | `xor r8d, r8d` |
| `00313120` + 0x197 | `mov r8d, 1` |
| `003191B0` + 0x107 | `mov r8d, 1` |

### The table and the preview store

- PASS: the retained US table's type-10 rows are 226..241. All of them lie inside D0..F1 (208..241). Rows 511..534
  have type 7.
- PASS: all nine shipped language tables in the game extract (us, ch, cn, de, es, fr, in, it, kr) have the same
  type-10 rows, and type 7 with bit 30 on 511..534.
- PASS: the preview call just before this one (`00304850` + 0x6CD → `00303830`) stores a DWORD to `[r14 + 0xe54]`
  at `00303830` + 0x124, inside `00303830`'s `.pdata` chain. That R14 is the unit is not re-derived here.

### Packet integrity

- PASS: the manifest and its members, the source range, the extent, the lineage and result-02 (see the header).
- PASS, as recorded artifacts (not re-run): with extent `complete` false, the old helper producer exited 0 with
  `producer_complete` true, and the current one exited 1 ("required complete current extent artifact"). The same
  holds for the old binding producer and the new qualification. The other three helper cases exited 1.
  `binding-qualified-01.json` is complete, has base `ca2dd6483` and two VERIFIED checks.
- PASS: the README keeps broader consequences, initialization, callbacks, aliasing and ownership OPEN, and makes no
  whole-OV closure.

## Controls (13, each must FAIL a named check on a privately patched image or table; all did)

A null control runs first: an unchanged private copy passes all 28 image checks.

1. + 0x81 `movzx edx, di` → `mov edx, edi` + NOP. Fails the cost-input check, the 65744 run and the random sweep.
2. + 0x8C, the same. Fails the same three.
3. + 0x145 counter input narrowed (`movzx edx, ax`). Fails the counter-leg check, the 65744 run and the random sweep.
4. + 0xA8 `setne` → `sete`. Fails the mode check and the emulated mode.
5. + 0x28 `mov r12d, r8d` → `mov r12d, r9d` (the mode from the wrong argument). Fails the carrier check and the emulated mode.
6. + 0x58 the NULL-unit `je` → NOPs. Fails the cost-input check and the emulated NULL case.
7. + 0x6C byte `+5` `jne` → `je`. Fails the emulated own-writes check.
8. The reset target `+0xE58` → `+0xE5C`. Fails the own-writes check and its emulation.
9. `cmp ecx, 8` → `cmp ecx, 7` (type 9 takes the counter leg). Fails the type-switch check, the 65744 run and the random sweep.
10. `cmovns` → `cmovs`. Fails the gil check and its emulation.
11. The counter leg's second descriptor load `02EBF138` → `02EBF140`. Fails the counter-leg check and the emulated quotient checks.
12. The caller's `mov r8d, 1` → `mov r8d, 0`. Fails the terminal-call check.
13. Table copy: row 511 type 7 → 10. Fails the table check and the US-table emulation.

After all controls, the exe on disk still hashes to `73461d0896204b1c259c`. The packet's five artifact refusals and
four source controls were not repeated. These 13 replace them for this review.

## Narrowings

1. **On this call site the counter leg needs an off-premise row.** In all nine shipped tables the type-10 rows are
   226..241, all inside D0..F1. The terminal phase routes entry words in D0..F1 around this helper (+ 0x6BE). Under
   the equal-binding premise, row = base + stride × entry word, so the helper is never called with a type-10 row.
   Emulated with the US table: none of the 53 bit-30 rows outside D0..F1 makes any final call. Those rows are 148,
   149, 183..207 (odd ids), 262..275 and 511..534, with types 5 (13 rows), 7 (24), 9 (13) and 255 (3).
   - For 511..534 (type 7) the helper makes no `00253770` call at all.
   - So the cost/counter disagreement (q mod 65536 against q) shows only when the row and the entry word disagree,
     or the table is modified. The packet calls its 65744 case mathematical; this places it off-premise for this
     call site.
2. **The mode at the other callers.** Of the four raw direct callers, three pass R8D = 1 (mode 17). The fourth,
   `00307300` + 0xB9, passes 0 (mode 16). Only the low 32 bits of R8 are tested, so R8 = 2^32 gives 16 (emulated).
   "Nonzero negative 32-bit values normalize to 17" holds; the raw flag is not forwarded.
3. **More NULL preconditions than the unit's.**
   - The first descriptor load has no null test before its `+0xC` read (+ 0x1E / + 0x2E).
   - Neither `div` tests its WORD stride. A zero stride faults (#DE). This is a source prediction from the bytes and
     was not emulated here.
   - The record (`+0x698`, reloaded at + 0x99 and + 0xB9) is not null-tested before WORD `+0x28` is read (emulated:
     address 0x28).

   So whole-helper NULL safety fails on the unit, the record and the descriptor alike.
4. **The reset has three gates, not one.** The `+0xE58` := 0 and `+0xDC8` := `0xFFFF` stores need a non-null unit,
   a non-null record *and* record byte `+5` = 0 (+ 0x58, + 0x64, + 0x6C). With byte `+5` nonzero the helper writes
   nothing outside its stack and makes no final call (emulated). The battle-unit field map names `+0xE58` the
   reserved gil cost and `+0xDC8` the reserved consumed item (`0xFFFF` = none). Those names are the field map's;
   this review re-derived the stores only.
5. **The gil pick wraps.** The subtraction is 32-bit, and `cmovns` tests the wrapped sign. Emulated cases:
   - 2^31 - 1 minus (-1) gives 0 (the wrapped result is negative);
   - 2^31 + 5 minus 10 gives 2^31 - 5 (a "negative" gil value wraps positive).

   `+0xE54` is the value that the preceding preview call stores at `00303830` + 0x124. The field map calls it the
   preview's gil amount.
6. **The helper writes nothing that the queue routine's row depends on, but it does not protect that row either.**
   Its own stores are only the two unit resets. It writes neither `02EBF138` nor the table. The routine's sequence
   row R15 was latched before this call and is not reloaded. `00306760` divides that row by the descriptor it reads
   *afterwards* (sequence-queue review). So any descriptor or table rebinding by one of the nine callees would change
   the queue's quotient. ASTRA's plan asks this question (H1 against H2), and it stays open here.

## What stays OPEN (kept as the packet states them)

This review supports conditional static facts, plus emulation of the original bytes on synthetic state and the
retained US table. The following remain open and are not awarded:

- the native effects of `00309110`, `00308FF0`, `00300CE0`, `00300BC0`, `00253690`, `00254EE0`, `00316440`,
  `00253770` and `0020E600`. In particular, whether any of them rebinds `02EBF138`, mutates the table or arena, or
  schedules a callback in the window before the special sequence (narrowing 6);
- the table and arena initialization and binding, and the equal-binding premise itself (the caller review's
  narrowing 3);
- natural reachability of this call site and of the counter leg, action consequences, aliasing, ownership, lifetime
  and whole OV-42;
- the producer-prerequisite repair and the binding qualification as gates. They were inspected, not re-run, and
  their acceptance is SPEC's.

Valid, readable, stable unit, record, row, descriptor and frame accesses, the normal Win64 ABI and preserved
nonvolatile registers are premises. All emulated values come from supplied states, not native runs.

run: `rv_termres.py` at HEAD c7e2bb2a1 (55 checks, 55 PASS, 0 FAIL, 13 controls; output identical to [`rv_termres.out`](rv_termres.out))
