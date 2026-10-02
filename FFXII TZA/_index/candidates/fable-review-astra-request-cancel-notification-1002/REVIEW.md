# FABLE review: ASTRA request-cancel-notification

- **Packet:** [request-cancel-notification README](../../../_experiments/evidence/request-cancel-notification/README.md)
- **Producer commit:** `011e013c7`. The manifest sha256 begins `8a463282899676c2`. It equals the manifest at the
  producer commit (`git show 011e013c7:…/manifest.json`), and all 62 members hash as listed. The packet's 11 captured
  and retained range hashes equal the certified image's bytes. They cover all 11 bodies reviewed here. The packet's
  `retained/manifest.json` is byte-identical to the parent packet `notification-retirement-order`'s manifest.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every carrier, range, mode, selection, multiplicity, return-value and
  extent claim re-derives at the bytes: 426 new bytes over three complete bodies, plus 1041 retained bytes over
  eight. The central claim also re-derives: a mode-4 cancel can reach the end-notification attempt without any
  interpreter call. The narrowings tie "removes the first nonzero entry" to the channel head. They state the
  selection rule and the NULL-actor whole-verb hazard, and they correct the `.pdata` reading. None of them
  contradicts the packet's notification clause, which is already scoped to a valid head entry.

## Method

[rv_cancel.py](rv_cancel.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). The reader
is copied unchanged from the filecache-route2-commit-key review (sha256 `69f9bc40be32abcc32b1`). The review does
not import ASTRA's `prove.py`, `capture.py`, `unwind-fragment.py` or `control.py`, or the shared role adapter
`reg_tracking.py`. It works as follows:

- It checks the image sha256 (`73461d0896204b1c259c`) and decodes the three new bodies and the eight retained bodies
  completely.
  - Bodies with a `.pdata` record are checked against the image's own `.pdata`, with CHAININFO records followed.
  - Leaves without a record (`00263FF0`, `003DB550`, `003DB650`, `003DC1B0`) are bounded by a closed local CFG that
    ends in `ret`, and by int3 padding or the next record after them.
- It builds a local CFG from direct branches for each body.
- It takes register-write censuses for every carrier (rbx, rdi, rbp, r12, r14, r15).
- It checks flag producers between each `test`/`cmp` and the `cmov` or `jcc` that consumes it.
- It runs a premise-driven path walker through the retained removal `003DB2A0`. Every conditional branch on the
  path must have an explicit premise.
- It computes reverse reaching definitions for EAX at every `ret` of `003DB420`, with a call counted as an rax
  definition. It also checks that the removal's own EAX is dead in the recycler.
- It computes the call closure in front of the notification attempt.
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is
  rechecked after all controls.

Raw output: [rv_cancel.out](rv_cancel.out).

## Re-derived (85 checks, 85 PASS, 0 FAIL; 14 controls among them)

### Extents and totals

| Claim | Result |
|---|---|
| `00352980` + 0x2E (46 B), `00353660` + 0x4C (76 B), `003DB420` + 0x130 (304 B): 426 B | PASS. Each decodes exactly. One record covers each carrier. For the recycler, see the next row. |
| `003DB420`'s first `.pdata` record is 28 B | PASS: `003DB420` + 0x1C, flags 0. It ends before the first out-of-fragment branch target (`003DB420` + 0x125) and before the removal call (`003DB420` + 0xE6). See narrowing 4. |
| The complete body is 304 B | PASS. Six records tile it exactly: the primary record plus five CHAININFO records. Records `+0x1C`, `+0x11E` and `+0x125` chain directly to `003DB420`. Records `+0x71` and `+0xFF` chain to the `+0x1C` record. Every chain resolves to `003DB420` in at most 2 hops. |
| Local CFGs | PASS. `003DB420` has no tail or out-of-body branch, and its two rets are `+0x11D` and `+0x12F` (the last instruction). Each carrier ends in a single tail `jmp 003DB6E0` and has no `ret`. |
| Retained bodies: 1041 B over 8 | PASS. `003DBCF0` is tiled by 3 chained records. The others have one record each or are closed leaves. |

### Native carriers

| Claim | Result |
|---|---|
| `00352980` passes the popped channel and mode 4 | PASS. rbx = incoming rdx (the receiver), and the `00267E10` result goes to edx. `00352980` + 0x11 sets `mov r8d, 4` and rcx = rbx before the call `003DB420`. Afterwards rcx = rbx again and the body tail-jumps to `003DB6E0`. The recycler's EAX is never read. |
| `00353660` passes first pop + 1 and resolves the second pop | PASS. The first pop goes to edi (rdi has no other writer except the epilogue pop). The second pop goes to `00264010` (`00353660` + 0x21). `00353660` + 0x2C is `lea edx, [rdi + 1]`, followed by r8d = 4. rcx = rbx = the resolved actor at the `003DB420` call. The body then tail-jumps to `003DB6E0` with the same pointer. |
| The pop helper | PASS. `00267E10` returns 0 on an empty stack. With type byte 1 it returns the DWORD. With type 2 it returns `cvttss2si` of the float. Any other type calls `008620C0(1)` and returns 0. |

### Recycler `003DB420`

| Claim | Result |
|---|---|
| Range: channels from `byte actor+88h - 1` down to `max(0, signed edx)` | PASS. `xor eax, eax` / `test edx, edx` / `cmovns eax, edx` (`003DB420` + 0x2F), with no flag producer between. The start is `movsxd rbp, (r9 - 1)`, where r9 = byte actor+88h. Both range compares are signed 64-bit: `jl` at `+0x6B` and `jge` at `+0xF3`. rbp is written only at `+0x61`, by the decrement at `+0xED` and by the restore. The narrowing `r9d = eax + 1` applies to mode 3 only (`jne` at `+0x4A`). |
| Gated by the initial active-bit snapshot | PASS. r12d = WORD actor+6 (`+0x37`). r12 is never rewritten in the body except by the restore. Each channel is tested with `test r12d, edi` (`+0x89`). The mask is `1 rol cl`, with cl = the low byte of (count − 1), followed by `ror edi, 1` per channel. |
| Mode 4 normalises the filter to zero | PASS. `xor r14d, r14d`, `cmp r8d, 4`, then `cmovne r14d, r8d` (`+0x64`). Only `lea` and `movsxd` lie between them. r14 has no other writer. Before the compare, r8 is written only on the mode-3 arm. |
| The first nonzero `+11h` is selected; states 1, 2 and 3 all qualify | PASS. The head is BYTE [actor + channel + 94h] (`+0x80`), and FF skips the channel. The state is BYTE entry+11h with stride 14h (`+0xA4`). `test r9d, r9d` / `jne` (`+0xAD`) selects any nonzero value. A zero state follows the entry's +0 link (`+0xB3`). Under mode 4, the path from the nonzero arm to the call `003DB2A0` (`+0xE6`) is exactly six instructions and reads no r9. See narrowing 2. |
| At most one entry per channel, then the channel is decremented | PASS. The call's only successor is `+0xEB`. From the nonzero arm, no path re-enters the walk head `+0x90` without passing `dec rbp` (`+0xED`). The walk's only back edge comes from the zero-state arm. |
| EAX 1 on all normal paths | PASS by reverse reaching definitions. EAX at ret `+0x11D` comes from {`+0xFA`, `+0x11E`}, and EAX at ret `+0x12F` comes from {`+0x125`}. All three are `mov eax, 1`. They map to loop exit, empty range and NULL actor. The removal's EAX is dead: every path from the call writes rax before reading it. These definitions equal `result-01.json`'s. |

### Retained removal and post (the notification clause)

| Claim | Result |
|---|---|
| A valid head, a mode-3 descriptor and a non-8000h requester reach `003DC0D0` independently of `+11h` | PASS. The premise walker fixes nine branches: index ≠ FF, actor non-null, `+10h` ≠ 4, `+2` ≥ 0, head ≠ FF, head = index, `+6` ≠ 8000h and `+10h` = 3. It then reaches the call `003DC0D0` at `003DB2A0` + 0xDD in 43 instructions. The path reads entry `+12h`, `+10h`, `+2` and `+6` and the head byte, and never reads `+11h`. Its only earlier call is the unhook `003DC1B0`, which clears `+11h` (`003DC1B0` + 0x83 dominates its ret). |
| Flags ≥ 2 cross `00263050` | PASS. The flags test (`003DB2A0` + 0xE6) and the `00263050` call (`+0xF2`) come after the attempt. See note A. |
| Removal EAX is the entry's flags bit 0 | PASS. It is BYTE `+12h` & 1 (`+0x4A`, `+0x162`), and r14 has no other writer. |
| The attempt is the `003DBCF0` call inside the post | PASS. `003DC0D0` resolves (dword `+8`, word `+6`) through `003587C0`. A NULL result (`+0x18`) skips the `003DBCF0` call at `003DC0D0` + 0x52. `003587C0` returns NULL for a null table, a negative ordinal or an ordinal ≥ count. |
| No target interpreter call | PASS. The call closure in front of `003DC0D0` + 0x52 is exactly {`003DB420`, `003DB2A0`, `003DC1B0`, `003DC0D0`, `003587C0`, `00263FF0`}. It has no `0025E4C0` and no indirect call, and every callee below it is a leaf. The recycler has no call before `+0xE6`. |

## Controls (14, each must FAIL a named check on a privately patched image; all did)

A null control also runs first: an unchanged private copy, with the sha check off, passes all 60 image checks. The
manifest, packet-file and README checks are kept out of the control check set.

1. `cmovne r14d, r8d` → `mov r14d, r8d` (mode 4 is no longer normalised). Fails the mode-filter check.
2. `cmovns` → `cmovs`. Fails the `max(0, signed)` check.
3. Range `jl` → `jb`. Fails the signed-compare check.
4. State `jne` → `je`, so a zero state is selected. Fails the selection check.
5. `ror edi, 1` → `jmp` to the walk head, so the same channel is walked again after a removal. 4 checks fail,
   including once-per-channel.
6. Loop-exit `mov eax, 1` → `mov eax, 0`. Fails the reaching-definitions check.
7. The snapshot reads WORD actor+4 instead of actor+6. Fails the snapshot check.
8. Removal `jne` before the post → `jmp`, so the post is skipped. Fails the premise path (4 checks).
9. The descriptor test reads `+11h` instead of `+10h`. Fails the premise path and the no-`+11h` check.
10. `003DC0D0`'s resolver call is retargeted to `0025E4C0`. Fails the post check and the interpreter-free closure.
11. The removal's `mov edx, esi` → `mov edx, eax`, which makes it a real list walk. Fails the non-head-search check.
12. `00352980` passes mode 3. Fails the carrier check.
13. `00353660` passes no +1. Fails the carrier check.
14. The primary `.pdata` record's end is moved from `+0x1C` to `+0x20`. Fails the tiling and first-record checks.

After all controls, the exe on disk still hashes to `73461d0896204b1c259c`. The packet's four CLI refusals and six
static mutations were not repeated. These 14 replace them for this review.

## Narrowings

1. **The recycler removes only a channel head.** The packet says mode 4 "removes the first nonzero entry". The bytes
   show something narrower: the recycler *passes* that entry to `003DB2A0`. The removal's search loop
   (`003DB2A0` + 0x86, `mov edx, esi`) reloads the same index on every turn, and `003DB550` is pure. Unless the
   index is already the head of the channel named by its own `+2` byte, one of the following happens with stable
   memory:
   - if the entry's +0 link equals its own index, the entry is removed;
   - if the link is FF, the removal returns without removing anything (`+0x15D`);
   - otherwise the loop never exits.

   When every linked entry has a nonzero `+11h`, the first nonzero entry *is* the head, and the packet's statement
   holds. A cancel does not reach past a zero-state head.
2. **"States 1/2/3 eligible" means "any nonzero `+11h` byte".** Mode 4 tests the byte for nonzero only. The walk is
   bounded by BYTE actor+89h (a signed compare, so at most that count + 2 list positions are examined).
3. **The NULL-actor return 1 is not a safe whole-verb path.** The recycler returns 1 for a NULL actor. Both carriers
   then tail-jump to `003DB6E0` with the same rcx, and `003DB6E0` + 0x6 reads byte [rcx + 63h] with no prior test.
   For `00353660` that pointer is `00264010`'s result, which can be NULL (`00264010` + 0x2E). This is a static
   reading; no fault was observed.
4. **`.pdata` does bound the 304 B body once chains are followed.** "The first `.pdata` entry covers only 28 bytes"
   is exact for the primary record. The image then tiles the rest with five CHAININFO records that resolve to
   `003DB420`. The extent lesson should read "never use the primary record alone", not "`.pdata` does not give the
   extent". The byte total is unaffected.
5. **The two-argument bound is 32-bit, and a missing argument recycles from channel 0.** `lea edx, [rdi + 1]`
   (`00353660` + 0x2C) wraps a first pop of 7FFFFFFFh to a negative bound, which `cmovns` clamps to 0. The pop
   returns 0 on an empty stack or an unexpected type, and truncates a float. Either way the range starts at channel
   0, so every active channel is recycled.

**Note A (scope, not a narrowing).** The notification attempt comes before the flags test. The packet's "flags 0/1"
premise is needed only for the no-opaque composition past the attempt (the `00263050` call and the relink). It is
not needed for the attempt itself.

## Limits (kept as the packet states them)

This review supports conditional static facts only, under these premises: valid, stable and disjoint
actor/entry/frame storage; normal ABI and returns; no concurrent writer. The following remain open and are not
awarded:

- that an authored scene cancels a mode-3 entry, and the natural cancel/interleaving timing;
- whether the notification is admitted (capacity), delivered or consumed;
- same-key re-entry, entry ownership and reuse, and actor lifetime;
- the tail scheduler `003DB6E0`, `00263050` (flags ≥ 2), the pop helper's `008620C0` error path, and `00264010`'s
  resolver callees (`00358940`, `003590D0`, `003588B0`), none of which were read;
- channels whose index mod 32 is 16 to 31 never pass the WORD snapshot test. That follows from the bytes, but there
  is no authored-data census here of channel counts above 16.

run: `rv_cancel.py` at c0bf8acd5 (85 checks, 85 PASS, 0 FAIL, 14 controls; output identical to
[`rv_cancel.out`](rv_cancel.out))
