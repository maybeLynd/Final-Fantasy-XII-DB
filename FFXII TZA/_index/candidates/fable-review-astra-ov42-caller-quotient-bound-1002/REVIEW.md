# FABLE review: ASTRA ov42-caller-quotient-bound

- **Packet:** [ov42-caller-quotient-bound README](../../../_experiments/evidence/ov42-caller-quotient-bound/README.md)
- **Producer commit:** `c51d5af60`. The manifest's sha256 equals the committed manifest, and all 37 members hash as
  listed. The four retained copies (three from `ov42-caller-row-preconditions` at `103aa3123`, one from
  `ov42-sequence-queue-source` at `0c4215736`) are byte-identical to their committed sources.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every byte claim re-derives at the bytes, and the bound holds through the
  original instructions in emulation. The latch, the unsigned 542 guard, the 32-bit row construction, the R15 carrier
  into the queue call and the queue arm's arithmetic all check out. The narrowings add four facts the packet does not
  state. None contradicts it, and none settles whether a normal call has equal bases and strides.

## Method

[rv_qbound.py](rv_qbound.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is copied
unchanged from the kind-row review (sha256 `69f9bc40be32abcc32b1`). It does not import or run ASTRA's `prove.py`,
`prove_owner_reload_order.py`, `run.py`, `control.py` or validation scripts, or the shared role adapter.

- It checks the image sha256, the manifest and its members, and the retained lineage (`git show` of each source).
- It decodes the queue routine's direct caller (`00304850`) over its `.pdata` chain. The switch's jump table is
  resolved and its edges are added to the CFG.
- It asserts each instruction of the latch, the guard and the row construction. Reaching definitions of R13, R14 and
  R15 are computed over that CFG.
- It re-asserts the queue routine's kind-4 arm, which FABLE reviewed independently in
  [ov42-sequence-queue-source](../fable-review-astra-ov42-sequence-queue-source-1002/REVIEW.md).
- It emulates (unicorn) the **original** caller construction (`+ 0xC0` .. `+ 0xE7`, the lookup stubbed), feeding the
  **original** queue arm (`00306760` + 0x138 .. the store at + 0x174, the lookup stubbed). The runs are:
  - every id 0..542 at 9 strides and 5 bases;
  - 400 random cases;
  - the packet's four boundary checks and its three supplied-state countermodels.
- It checks the integer invariant arithmetically over all 543 ids and 65,535 strides.
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is rechecked.

Raw output: [rv_qbound.out](rv_qbound.out). 67 checks, 67 PASS, 0 FAIL, 9 of them controls.

## Re-derived

| claim | result |
|---|---|
| The caller latches unsigned WORD unit `+0x714` as i | PASS: `+ 0x3D` `movzx r13d, word ptr [rsi + 0x64]` with RSI = RCX + 0x6B0 (`+ 0x2F`). The only R13 definition reaching the guard and the row's `movzx eax, r13w` is this latch |
| It rejects i > 542 | PASS: `+ 0x8E` `cmp r13w, bx` (EBX = 0x21E from `+ 0x58`), then `+ 0x92` unsigned `ja` to the rejecting exit. The guard dominates the queue call over the CFG including the switch edges |
| R = low32(Bc + i·Sc) | PASS: `+ 0xCF` `mov r15, rax` (the second lookup's result), `+ 0xD9` `movzx ecx, word ptr [rax + 8]` (stride), `+ 0xDD` `movzx eax, r13w`, `+ 0xE1` `imul ecx, eax` (32-bit), `+ 0xE4` `add r15d, ecx`. The 32-bit `add` zero-extends, so R15's upper half is 0 |
| R15 carries R to the queue call | PASS: the definitions reaching `+ 0x6F7` `mov rdx, r15` / `+ 0x6FD` `call 00306760` are exactly `+ 0xE4` and the null-row `+ 0xE9` `mov r15, r14` (R14 = 0 from `+ 0x2C`). The five other R15 writes are `mov r15, qword ptr [rsp + 0x108]` restores on exit paths |
| The queue arm: D = (low32(R) − low32(Bq)) mod 2^32, unsigned `div` by the u16 stride, 16-bit FFFF test, `− 0xD0`, DWORD store | PASS (re-asserted at `00306760` + 0x147 .. + 0x174) |
| Equal bases and strides give q = i, so the stored DWORD is i − 0xD0 | PASS: emulated for every id 0..542 × 9 strides × 5 bases (24,435 cases) and 400 random cases. i·S ≤ 542 × 65535 = 35,519,970 < 2^32 |
| Domain 0..334 and FFFFFF30..FFFFFFFF; 511..534 excluded | PASS (emulated over all 543 ids) |
| i = 207 stores FFFFFFFF by subtraction, not through the FFFF branch | PASS |
| The three supplied-state countermodels give 511, 512, 512 | PASS, through the original bytes |
| The four boundary checks | PASS, through the original bytes |

Controls (each fails at least one check): signed guard (`ja` → `jg`); latch BYTE; 64-bit row `add`; stride BYTE;
`imul` → `add`; queue call RDX from R14; queue `− 0xD1`; queue `idiv`. The null control passes.

## Narrowings

1. **The row is a 32-bit value used as a pointer.** `+ 0xE4` `add r15d, ecx` zero-extends, and the caller then
   dereferences R15 (`test dword ptr [r15 + 0xc], 0x40000000` at `+ 0x6D2` and `+ 0x6ED`). The packet's "valid
   non-NULL current-row construction" premise therefore includes the row lying below 4 GiB.
2. **The descriptor cell is read three times before the switch.** `+ 0x98` tests it for null before the first lookup,
   `+ 0xC0` supplies the second lookup's key, and `+ 0xD2` supplies the stride. Two more loads sit in switch arms. The
   lookup call lies between the key and stride loads, as in the queue arm.
3. **Two routes reach the queue call.** For i − 0xD0 ≤ 0x21 unsigned (ids 208..241) the caller jumps straight to the
   bit-30 test before the call. Other ids first run `00303830` and then, when bit 30 of `[r15 + 0xC]` is set,
   `00305640(rdi, r15, 1)`, and test bit 30 again. Both helpers run with R15 as their RDX and are not read here.
4. **The null row.** When the descriptor cell is null or the first lookup returns 0, the row is 0 (`+ 0xE9`). The
   bit-30 test at `+ 0x6ED` dominates the queue call, so a null row reaches the call only after reading address
   0xC (a source prediction: that read faults).

## What stays OPEN

- Whether a normal call has equal construction and queue bases (low32) and equal positive strides. The two reads
  are separated by at least `00303830`, `00305640` (on the second route) and the queue routine's own callees.
- Descriptor and resource stability across those calls; the table binding's writers and lifetime. ASTRA's
  `ov42-action-table-binding` (`ca2dd6483`) bears on this and is reviewed separately.
- Kind-4 dispatch itself, natural admission of any row, and the native effects of the helpers.
- No natural-impossibility claim is made for 511..534. Whole OV-42 stays OPEN.
