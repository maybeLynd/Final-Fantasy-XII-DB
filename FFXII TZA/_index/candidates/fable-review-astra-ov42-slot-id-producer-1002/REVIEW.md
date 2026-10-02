# FABLE review: ASTRA ov42-slot-id-producer

- **Packet:** [ov42-slot-id-producer README](../../../_experiments/evidence/ov42-slot-id-producer/README.md)
- **Producer commit:** `0ada51452`. The manifest sha256 begins `0bc1d6929da2afbf` and equals the committed manifest.
  All 45 members hash as listed. The packet's three retained/captured range hashes equal the certified image's bytes:
  the allocator `0030D070` + 0xE5, the wrapper prefix `0030CFB0` .. + 0xA6 and the new suffix `0030CFB0` + 0xA6 ..
  + 0xB9.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every carrier, store, width, compare, scan bound, return and gate claim
  re-derives at the bytes, and a concrete emulation of the two original bodies agrees on every case tried. The
  narrowings correct one size label in the request, add a one-way side effect of the flag gate and a missing null
  guard on the row read, and pin the direct-caller census. None of them contradicts the packet.

## Method

[rv_slots.py](rv_slots.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is copied
unchanged from the filecache-route2-commit-key review (sha256 `69f9bc40be32abcc32b1`). It does not import or run
ASTRA's `prove.py`, `control.py`, capture drivers, freeze or publication scripts, or `reg_tracking.py`. It works as
follows:

- It checks the image sha256 (`73461d0896204b1c259c`) and decodes both bodies completely. Each one is checked
  against the image's own `.pdata` (one record each), and its local CFG is checked closed.
- It takes register-write and register-read censuses for the action WORD (DX, R10), the identity (ECX, R11), the scan
  index (R8B), the slot base (RDI) and the wrapper's saved carriers (RBX, RSI, RDI).
- It lists every memory write of both bodies with base, displacement and width.
- It does its own finite reading of the scan index: the values R8B can hold at the loop head, and which arms they make
  dead.
- It emulates the **original** two bodies (unicorn) over synthetic slot arrays and synthetic action rows, recording
  every memory write. Only the address resolver `0020E600` runs besides them. The cases:
  - the first free slot at each position 0..31;
  - all 32 slots occupied;
  - the 24 candidate words 511..534, FFFF, D0, F1 and 0;
  - each wrapper gate.
- It runs a raw `E8`/`E9` rel32 and `0F 8x` census over `.text` for direct references to both bodies.
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is rechecked
  after all controls.

Raw output: [rv_slots.out](rv_slots.out).

## Re-derived (53 checks, 53 PASS, 0 FAIL; 13 controls among them)

### Bodies

| Claim | Result |
|---|---|
| Allocator `0030D070`, 229 B | PASS: it decodes exactly, and one `.pdata` record covers it exactly. It has three rets: the full-array return `0030D070` + 0x51, the dead sign arm + 0x5E, and the success return + 0xE4 (the last instruction). It has no call, no tail and no indirect jump. |
| Acquire wrapper `0030CFB0` | PASS, at **185 B**: one `.pdata` record, one ret (the last instruction). The 166 B retained prefix ends at `0030CFB0` + 0xA6; the 19 B suffix is + 0xA6 .. + 0xB9. Its only calls are `0020E600` (twice) and `0030D070`. See narrowing 1. |

### The allocator

| Claim | Result |
|---|---|
| The identity is ECX | PASS: `mov r11d, ecx` (`0030D070` + 0x5). R11 has no other writer, and its one reader is the DWORD store `[rcx + 0x20]` (+ 0xDB). |
| The incoming DX only zero-extends into R10D and is the final WORD store | PASS: `movzx r10d, dx` (+ 0x14) is the only read of the incoming RDX, which is next written at + 0x82. R10 has one writer and one reader, `mov word ptr [rcx + 0x1c], r10w` (+ 0xDF). That store is the instruction before the final ret. |
| No action-range or category test | PASS: the seven compares and tests read only R8B, the marker WORD with CX, and RAX (the list-tail test). None reads R10, RDX or R11. |
| Slots are `022C17B0` + 48*i | PASS: RDI = `022C17B0` (+ 0x8), written only there and at the three restores. All three pointer formations are `lea [rax + rax*2]`, `shl 4`, `add rdi`. |
| WORD `+0x1C` == FFFF selects | PASS: ECX = 0xFFFF (+ 0xF), with no RCX write inside the scan. The WORD compare is `cmp word ptr [r9 + 0x1c], cx` (+ 0x3A), then `je` to the found arm. |
| Scan 0 → 31, stop at 32 | PASS: `xor r8b, r8b` (+ 0x18), `inc r8b` (+ 0x41), `cmp r8b, 0x20` / `jl` (+ 0x44 / + 0x48). R8 has no other writer. The reviewer's own reading gives exactly 0..31 at the loop head. The null-record arm (+ 0x37), the sign arm (+ 0x57) and both "> 31" arms (+ 0x76, + 0x7C) are therefore dead. |
| Success writes | PASS: the census lists the entry home slot, slot +0 and +8 (links), the list head `022BE978` or the old tail's +0, the tail `022BEB88`, then DWORD 1 at +0x18/+0x14/+0x10, DWORD +0x20, and WORD +0x1C. The success path returns EAX = `movzx r8b` (+ 0xC2). The link block always runs: its `je` (+ 0x8D) tests the ZF of `add rdx, rdi`, and no slot address is 0. |
| Full array: AL = FF, no own non-frame write | PASS: no write is reachable from + 0x4A (`mov al, 0xff`). In the emulation, all 32 occupied gives AL = FF and no non-frame write. RAX was FF in that run (the last index's `movsx` plus `mov al`); the arm promises AL only. |
| 511..534 are not excluded when a free slot exists | PASS (emulated): each of 511..534, FFFF, D0, F1 and 0 (with RDX's upper bits set) is stored unchanged in the first free slot, and the next free slot stays free. For each first-free position k = 0..31, EAX = k. The only non-frame writes are slot k's seven fields and the head/tail cells. |
| FFFF is copied and the marker stays free | PASS (emulated): after a FFFF word, slot 7's +0x1C still reads FFFF while +0x10/+0x14/+0x18, +0x20 and the links were written. |
| `0030D070`'s direct callers | PASS: the raw census finds one direct reference, the call at `0030CFB0` + 0xA1. See narrowing 4. |

### The wrapper

| Claim | Result |
|---|---|
| Input R8W → BX → EDX; identity ESI → ECX | PASS: `movzx ebx, r8w` (+ 0x13), `mov esi, edx` (+ 0x17), `mov rdi, rcx` (+ 0x19). Each is written only there and at its restore. `movzx edx, bx` (+ 0x9C), `mov ecx, esi` (+ 0x9F), `call 0030D070` (+ 0xA1). |
| After the call, AL → unit+4 | PASS: `mov byte ptr [rdi + 4], al` (+ 0xA6) directly follows the call. |
| The WORD store is the allocator's, not the wrapper's | PASS: the wrapper's own writes are two home slots, `022C2158` (DWORD) and unit+4 (byte). None is at +0x1C, and none goes into the slot array. |
| An existing non-FF unit+4 skips | PASS: `cmp byte ptr [rcx + 4], 0xff` (+ 0xF) / `jne` to the epilogue. The call and the unit+4 store are unreachable from there. Emulated: unit+4 = 5 returns with no non-frame write. |
| The bit-30 row gate and the `022C2158` bit-1 gate | PASS: bit 30 clear goes straight to the call. With bit 30 set, `ax = BX - 0xD0` is tested `cmp ax, 0x21` / `ja`. Inside D0..F1, `022C2160 - 5 <= 1` allocates. Otherwise bit 1 of `022C2158` set skips without the call, and clear sets it (+ 0x93 / + 0x96), then allocates. Emulated: 511 allocates with the flag clear and sets it; 511 with the flag set leaves unit+4 FF and writes no slot; D5 with the flag set allocates only while `022C2160` is 5 (not 4). |
| 511..534 reach the flag gate, not the exception | PASS: their WORD differences from D0 are 303..326, all above 0x21. |
| Bit-30-clear rows, emulated | PASS: each of 511..534 lands in the free slot with the identity, AL becomes unit+4, and `022C2158` is untouched. |
| Word FFFF through the wrapper | PASS (emulated): unit+4 = 3, while slot 3's marker still reads FFFF. |

### Manifest

PASS. The manifest sha256 begins `0bc1d6929da2afbf`, it equals the manifest at `0ada51452`, and all 45 members match.

## Controls (13, each must FAIL a named check on a privately patched image; all did)

A null control also runs first: an unchanged private copy, with the sha check off, passes all 33 image checks.

1. Marker `0xFFFF` → `0xFFFE` (`0030D070` + 0xF). Fails the marker check and the emulated selection and storage
   checks.
2. Scan bound 0x20 → 0x1F. Fails the scan-index check and the emulated first-free check.
3. Scan stride `shl r9, 4` → `shl r9, 5`. Fails the slot-base check and the emulated checks.
4. `inc r8b` → `dec r8b`. Fails the scan-index check. The emulation then leaves its mapped memory.
5. The WORD store `r10w` → `r11w`. Fails the R10 and R11 censuses and the emulated storage check.
6. The identity store `r11d` → `r10d`. Fails both censuses and the emulated checks.
7. `movzx r10d, dx` → `movzx r10d, cx`. Fails the DX check and the emulated storage checks.
8. The full-arm restore → `mov [rcx], rdi`, a non-frame write on the full path. Fails the write census and the
   slot-base census. The emulation faults.
9. `movzx edx, bx` → `movzx edx, si`. Fails the call check and the emulated wrapper checks.
10. The unit+4 store → unit+5. Fails the call, write-census and suffix checks.
11. `movzx ebx, r8w` → `nop; movzx ebx, dx`. Fails the carrier check and the emulated wrapper checks.
12. Flag test bit 1 → bit 2. Fails the flag-gate check and the emulated gate checks.
13. The unit+4 byte store → `mov dword [rdi+0x1c], eax`, so the wrapper writes +0x1C (the attribution this review
    corrects on the availability page). Fails "0030CFB0's own writes ... none at +0x1C" and the call check.

After all controls, the exe on disk still hashes to `73461d0896204b1c259c`. The packet's three CLI refusals and seven
source mutations were not repeated. These 13 replace them for this review.

## Narrowings

1. **The wrapper is 185 B, not 166 B.** 166 B is the prefix the packet reused, and the closed body adds a 19 B suffix.
   The battle-unit field map's exclusive-subtree table labels `0030CFB0` "~229 B". That is the allocator's size
   (routed in the consumption draft).
2. **The flag gate is one-way inside the wrapper.** For a bit-30 row outside the D0..F1 exception, the wrapper sets
   bit 1 of `022C2158` *before* it calls the allocator, and nothing in the wrapper clears it. When the array is full,
   the allocator returns FF, unit+4 becomes FF, and the flag stays set (emulated). Later bit-30 rows outside the
   exception are then skipped until some other writer clears the bit. That writer is not read here.
3. **The row read has no null guard.** The wrapper takes the row descriptor from `[02EBF138]`. If that pointer is
   null, or the first `0020E600` resolve returns null, it sets RCX = 0 and still executes
   `test dword ptr [rcx + 0xc], 0x40000000`. That is a read of address 0xC (a fault), not a skip. The row pointer is
   a zero-extended 32-bit sum, `low32(WORD [desc+8] * BX + low32(resolve))`. The packet's premise "readable stable
   resolved rows" covers both points. The availability page already notes that `02EBF138` is 0 at load.
4. **Direct callers, raw census.** `0030D070`'s only direct reference is `0030CFB0` + 0xA1. `0030CFB0` has two:
   `00304850` + 0x5D4 (in its chained fragment that starts at + 0x520) and the script adapter `0030EEA0` + 0x60.
   Indirect callers are not covered.
5. **Return width.** The success return is the full EAX = slot index (0..31). The full arm defines only AL. The
   wrapper consumes only AL. Index FF can never be a success.

## Limits (kept as the packet states them)

This review supports conditional static facts, plus emulation of the original bytes on synthetic state. The following
remain open and are not awarded:

- which upstream command, AI or authored-VM producer supplies 511..534 or FFFF;
- current descriptor or row identity, and the pool's initialization, ownership and reuse. The slot array is in the
  `.data` virtual tail, so it is zero at load and gets its FFFF markers from the pool reset, which is not read here;
- the consequence of a FFFF allocation: a linked slot that still reads free could be selected and linked again;
- normal control or command reachability, action execution and actual rejection;
- whole OV-42.

Valid, stable, disjoint slot, list and frame storage, and the normal native ABI, are premises.

run: `rv_slots.py` at HEAD e828e3f50 (53 checks, 53 PASS, 0 FAIL, 13 controls; output identical to [`rv_slots.out`](rv_slots.out))
