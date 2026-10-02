# FABLE review: ASTRA ov42-sequence-queue-source

- **Packet:** [ov42-sequence-queue-source README](../../../_experiments/evidence/ov42-sequence-queue-source/README.md)
- **Producer commit:** `0c4215736`. The manifest sha256 begins `59f6be899f03c3b6` and equals the committed manifest.
  All 58 members hash as listed. The packet's source range `00306760` .. + 0x38F and its 936-byte physical body
  (sha256 `11d908d011ff...`, with the 24 table bytes at + 0x390) equal the certified image's bytes.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every claim re-derives at the bytes: the five-record extent and its
  code / NOP / table split, the DEC + unsigned-bound dispatch, kind 4 as the only arm reaching the store, RDI = entry
  RDX, the 32-bit subtraction, the two descriptor loads, the zero-extended WORD divisor, the unsigned 32-bit `div`,
  the 16-bit FFFF test, the `- 0xD0` and the DWORD store. There is no divisor test. An emulation of the original
  routine agrees on every case tried. The narrowings add side facts and the one raw direct caller. None of them
  contradicts the packet, and none settles kind-to-row consistency.

## Method

[rv_seqq.py](rv_seqq.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is copied
unchanged from the filecache-route2-commit-key review (sha256 `69f9bc40be32abcc32b1`). It does not import or run
ASTRA's `prove.py`, `prove_owner_reload_order.py`, `capture*.py`, `extent.py`, `control.py`,
`validate-title-source-annotations.py`, freeze or publication scripts, or `reg_tracking.py`. It works as follows:

- It checks the image sha256 (`73461d0896204b1c259c`). It follows `00306760`'s `.pdata` records and checks that
  they tile the physical extent. It decodes the 911 code bytes linearly and exactly, and it checks that the NOP and
  the six DWORDs after the one `ret` are never reached as code and are what the dispatch load addresses.
- It re-reads the dispatch head, resolves the six table cells and walks the local CFG from each arm entry.
- It takes register-write censuses (RDI, RDX, RAX, RCX, R14), a compare census of the kind-4 arm, the operand widths
  of every load and store on the arm, and dominance of the subtraction and the `div` over the store.
- It emulates the **original** routine (unicorn). Every direct callee is stubbed by a code hook that returns at
  once with a scripted RAX; those callees are the only code not run from the image. The runs are: the whole
  routine from its entry with the kind cell 0..7; the kind-4 arm alone over 24 candidate rows, 10 edge cases and
  60 random rows; a descriptor repointed during the lookup call; and a zero stride.
- It runs a raw `E8`/`E9` rel32 and `0F 8x` census over `.text` for direct references to the routine, the kind-4
  entry and the store. It reads the one caller's call site and the register it passes as RDX (narrowing 6).
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is
  rechecked after all controls.

Raw output: [rv_seqq.out](rv_seqq.out).

## Re-derived (58 checks, 58 PASS, 0 FAIL; 17 controls among them)

### Extent

| Claim | Result |
|---|---|
| Five chained records, 936 physical bytes | PASS: the root `00306760` .. + 0x10 and four CHAININFO records + 0x10 .. + 0x62, + 0x62 .. + 0x33A, + 0x33A .. + 0x356 and + 0x356 .. + 0x3A8 tile the extent exactly, each resolving to the root. int3 padding follows to the next root `00306B10`. |
| 911 code bytes, one NOP, six DWORDs | PASS: + 0 .. + 0x38F decodes exactly and ends with the one `ret` (+ 0x38E). + 0x38F is a single `90` that nothing falls into or branches to. + 0x390 .. + 0x3A8 are the 24 bytes the dispatch load addresses. The local CFG is closed: one `ret`, one indirect `jmp rax` (+ 0x79), and no branch leaves the code. |

### Dispatch

| Claim | Result |
|---|---|
| DEC / unsigned bound / image-base indexed load | PASS: + 0x4A loads DWORD `022C215C` (4 bytes). Then come `dec eax` (+ 0x50), `cmp eax, 5` (+ 0x57), `ja` + 0x33A (+ 0x5A, unsigned), `cdqe`, R14 = the image base by a rip-relative `lea` (+ 0x67), `mov eax, dword ptr [r14 + rax*4 + 0x1E6AF0]` (+ 0x6E; image base + 0x1E6AF0 = `00306760` + 0x390), `add rax, r14` and `jmp rax`. Between the load and the jump nothing else writes RAX or R14. |
| The six entries | PASS: kind 1 → + 0x1D1, kind 2 → + 0x2DD, kind 3 → + 0x7B, kind 4 → + 0xE8, kind 5 → + 0x298, kind 6 → + 0x32E. All are instruction boundaries. |
| Only kind 4 reaches `00306760` + 0x174 | PASS: of the six arm entries, only + 0xE8 reaches the store in the local CFG. Neither the entry's direct CFG nor the `ja` default + 0x33A reaches it. No direct branch from outside the arm lands in + 0xE8 .. + 0x174, and kind 3's arm ends in `jmp` + 0x335 (+ 0xE3), so it does not fall into kind 4. Emulated: with the kind cell set to 0..7, the queue `022C2178` is written in the kind-4 run only, once, by a 4-byte store at + 0x174. Kinds 0 and 7 call no arm callee. Every run returns with RBX, RSI, RDI and R14 restored. |

### The value

| Claim | Result |
|---|---|
| Entry RDX is kept in RDI | PASS: the RDI home save is at + 0x10 and `mov rdi, rdx` at + 0x15, with no RDX write before it. RDI is written only at + 0x15, at + 0xBC (kind 3's `sub`), at + 0x147 (kind 4's `sub`) and by the reload at + 0x348. Nothing writes it on the kind-4 arm before + 0x147. The callees in between preserve it only under the Win64 ABI, which is a premise. |
| `D = (low32(row) - low32(base)) mod 2^32` | PASS: + 0x138 loads QWORD `02EBF138`, + 0x13F takes DWORD `+0xC` into ECX, + 0x142 calls `0020E600`, and + 0x147 is `sub edi, eax` (`2B F8`, 32-bit). Emulated: a row with different upper 32 bits gives the same queue, and a row below the base wraps as unsigned. |
| `S = u16(second context + 8)`; unsigned 32-bit `div` | PASS: + 0x149 `xor edx, edx`, + 0x14B a second QWORD load of `02EBF138`, + 0x152 `movzx ecx, word ptr [rax + 8]` (2 bytes), + 0x156 `mov eax, edi`, and + 0x158 `div ecx` (`F7 F1`). Emulated: stride FFFF is taken as 65535. |
| Two loads; key from the first, divisor from the second | PASS: the lookup call lies between the two loads (+ 0x138, + 0x14B). Emulated: when the lookup stub repoints `02EBF138` during the call, the key is the first descriptor's `+0xC` (1D74) and the divisor the second's `+8` (30). The queue is 60 * 520 / 30 - 208 = 832. |
| No zero-divisor guard | PASS: from the arm entry to the `div`, the only compares are the two `+0x695` / `+0x696` byte tests (+ 0x11E, + 0x122). Their branches rejoin at + 0x138, before both loads. There is no branch between the lookup call and the `div`, nothing writes ECX between the WORD load and the `div`, and EDX is written only by the `xor`. Emulated: a zero WORD raises #DE (interrupt 0) at + 0x158, and the queue is not written. That is a source prediction, not an observed fault. |
| Low-16 FFFF test, `- 0xD0`, DWORD store | PASS: + 0x15D `mov edx, 0xffff`, + 0x162 `cmp ax, dx` (`66 3B C2`, 16-bit), `je` + 0x171 → `or eax, 0xffffffff`; else `movzx eax, ax`, `sub eax, 0xd0` (+ 0x16A) and `jmp` + 0x174. + 0x174 is a 4-byte store to `022C2178` and the routine's only write to it. Nothing writes EAX between the `div` and the compare. The subtraction and the `div` both dominate the store from the arm entry. |
| 511 / 534 → 303 / 326 with a coherent stride-60 row | PASS (emulated): with row = base + 60 * id, each of 511..534 queues id - 208 = 303..326. Ten edge cases and 60 random 64-bit rows, bases and strides 1..FFFF all equal the packet's formula. |

### Packet integrity

PASS. The manifest sha256 begins `59f6be899f03c3b6` and equals the manifest at `0c4215736`, and all 58 members match.
The README keeps open: kind-to-row/caller/owner consistency, S > 0 as a precondition, the arithmetic as no native
run, descriptor initialization, and whole OV-42.

## Controls (17, each must FAIL a named check on a privately patched image; all did)

A null control also runs first: an unchanged private copy passes all 33 image checks.

1. The kind-4 table cell → kind 3's arm. Fails the table check and the emulated kind sweep.
2. The kind-1 table cell → kind 4's arm. Fails the table check and the emulated sweep (two kinds write the queue).
3. `dec eax` → `inc eax` (+ 0x50). Fails the dispatch-head check and the emulated sweep.
4. `ja` → `jg` (+ 0x5A, a signed bound). Fails the dispatch-head check and the emulated sweep.
5. `mov rdi, rdx` → `mov rdi, rcx` (+ 0x15). Fails the RDI check and the emulated row-3 case.
6. `sub edi, eax` → `sub edi, ecx` (+ 0x147). Fails the first-descriptor check and the emulated value checks.
7. The key DWORD `+0xC` → `+0x10` (+ 0x13F). Fails the first-descriptor check and the emulated key checks.
8. The second load `02EBF138` → `02EBF140` (+ 0x14B). Fails the second-descriptor and two-load checks.
9. The stride WORD → BYTE (+ 0x152). Fails the second-descriptor check and the emulated edge and random cases.
10. `div ecx` → `idiv ecx` (+ 0x158). Fails the second-descriptor check and the emulated random and zero cases.
11. `mov eax, edi` → `test ecx, ecx` (+ 0x156, a divisor test). Fails the second-descriptor, two-load and compare-census checks.
12. `cmp ax, dx` → `cmp eax, edx` + NOP (+ 0x162). Fails the remap check and the emulated edge cases.
13. `sub eax, 0xd0` → `0xd1` (+ 0x16A). Fails the remap check and the emulated value checks.
14. `or eax, 0xffffffff` → `or eax, 0` (+ 0x171). Fails the remap check and the emulated edge cases.
15. `movzx eax, ax` → `movzx eax, al` (+ 0x167). Fails the remap check and the emulated candidate and edge cases.
16. The store target `022C2178` → `022C217C` (+ 0x174). Fails the store check and the emulated sweep.
17. `je` + 0x171 → `jne` (+ 0x165). Fails the remap check and the emulated value checks.

After all controls, the exe on disk still hashes to `73461d0896204b1c259c`. The packet's four CLI refusals and six
derive countermodels were not repeated; these 17 image patches replace them for this review.

## Narrowings

1. **The dispatch's default.** Kind = DWORD `022C215C`, and table cell `kind - 1` is used. Kind 0 and every kind
   above 6 (including a negative DWORD) take `ja` to `00306760` + 0x33A, the shared tail. That path runs no arm and
   writes no queue. The kind-4 cell is `00306760` + 0x39C.
2. **The remap is not injective, and FFFFFFFF has two sources.** The FFFF test reads the low 16 bits of a 32-bit
   quotient, so quotients alias modulo 65536 (`1FFFF` → FFFFFFFF, `10005` → FFFFFF35, emulated). w = `0xCF` also
   stores FFFFFFFF, the same DWORD as the sentinel. Every w below `0xD0` stores FFFFFF30..FFFFFFFF. This matches the
   page's existing "only `0xCF` and FFFF read as unavailable".
3. **Kind 3 inverts the same row.** Its arm (+ 0xAD .. + 0xCD) makes the same two descriptor loads, the same 32-bit
   `sub` and the same unsigned `div`. It then passes the full 32-bit quotient as EDX to `0030EC00` (+ 0xD4), with no
   FFFF test and no `- 0xD0`. It never reaches the queue.
4. **Other writes on the kind-4 arm and the tail.** After the store, the arm writes the unit's DWORD `+8` (loaded at
   + 0x15A) to `022C218C` (+ 0x185). That is the unit value the queue reader returns through RCX. The arm also
   writes DWORD 0 to `022C21B4` (+ 0x17C), then copies the unit's `+0x77C` count of QWORDs, taken from `+0x780` at
   stride 0x10, to `022C21B8` + 8*i. It counts them in `022C21B4`, with no bound against the destination. Every
   path to the `ret` passes + 0x37F, which stores DWORD 5 to `022C2160`.
5. **The entry reads the row before the dispatch.** + 0x32 compares BYTE `[rdx + 0x1C]` with 8 on every call, so
   RDX must be readable at `+0x1C` whatever the kind is. When that byte is 8, `003098D0` and `003299B0` run before
   the dispatch (+ 0x38, + 0x45). The callee `00861EC0` is an `FF 25` import thunk for `memset`, as the packet
   says.
6. **The one raw direct caller (a reviewer observation, not a packet claim).** The raw census gives `00306760`
   one direct reference: `00304850` + 0x6FD, in phase case 9 (+ 0x66E) of that routine's 13-way switch. The call
   passes RDX = R15 and RCX = RDI, and only when `test dword ptr [r15 + 0xc], 0x40000000` finds row bit 30 set.
   - R15 is formed before the switch. R13 = WORD `[rsi + 0x64]`, and the routine exits when it is above `0x21E`
     (+ 0x8E / + 0x92). Then R15 = `0020E600`(first `02EBF138` + 0xC) (+ 0xCF), plus WORD (second load + 8) * R13W,
     added with `add r15d, ecx` (+ 0xE4, 32-bit). A null descriptor or a null lookup gives R15 = R14 (+ 0xE9),
     whose value is not read here.
   - No R15 write lies on any path from a case entry to the call.
   - So, if the descriptor and the lookup return are unchanged between the caller's loads and the callee's, the
     kind-4 quotient is that WORD exactly (stride * word < 2^32), and the queue holds word - `0xD0`. That ties this
     caller's row to its own word. It does not tie it to the kind published in `022C215C`. No local exclusion of
     511..534 follows. Indirect callers are not covered.
   - ASTRA's later packet `ov42-kind-row-coherence` (`d83287255`) names this `00304850` → `00306760` row carrier as
     its next discriminator. That packet is not reviewed here.
7. **The `.pdata` chain is nested.** The extent record shows each CHAININFO record chaining to the record before
   it, and each resolves to the root. This review checks the resolution to the root, not the nesting.

## Limits (kept as the packet states them)

This review supports conditional static facts, plus emulation of the original bytes on synthetic state. The
following remain open and are not awarded:

- kind-to-row, caller and owner consistency: a normal kind-4 call's row is not shown to belong to the usual
  Quickening range, and there is no local row exclusion;
- the writers and persistence of the kind cell `022C215C`;
- descriptor initialization and the stability of the two loads (`02EBF138` lies in `.data`'s virtual tail), and
  S > 0, which is a precondition;
- the native effects of `00306D90`, `memset`, `0030D720`, `0030D550` and `0020E600`;
- natural queue consumption, command execution, lifetime and reuse, and whole OV-42.

The 303 / 326 values are arithmetic on supplied coherent rows, not native runs. Valid, readable, stable row,
unit, descriptor and frame accesses, the normal Win64 ABI and preserved nonvolatile registers are premises.

run: `rv_seqq.py` at HEAD d8dd3408b (58 checks, 58 PASS, 0 FAIL, 17 controls; output identical to [`rv_seqq.out`](rv_seqq.out))
