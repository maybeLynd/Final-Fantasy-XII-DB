# FABLE review: ASTRA render-clear-callee-footprints

- **Packet:** [render-clear-callee-footprints README](../../../_experiments/evidence/render-clear-callee-footprints/README.md)
  (board `ASTRA-REQ-FABLE-RENDER-CLEAR-CALLEE-FOOTPRINTS-1002`)
- **Producer commit:** `621dbd2cc`. The manifest sha256 begins `c3e8141dc7fafc01` and all 61 members hash as listed.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** The narrowing is about wording only. Every footprint, carrier, count and the
  conditional ID/active result re-derives at the bytes.

## Method

[rv_clear.py](rv_clear.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It does not import
ASTRA's `prove.py` or the shared role adapter. It works as follows:

- A small step emulator runs `0041F730` from entry to its `ret`, instruction by instruction, and follows each call into
  the helper bodies.
- The record pointer is symbolic (R+offset). The stack is symbolic.
- Constants come from the image: the 1.0f at `01CEBBA8`, the 64-byte source at `01F204E0` and the multiplier at
  `00915258`.
- The memset import (`00861EC0`) is the only modelled callee. The model fills `[rcx, rcx+r8)` with `dl` and clobbers
  the volatile registers. This model is the packet's library/ABI premise.

Every memory write is logged with its site. Footprints, call carriers, counts and the final bytes of WORD +0 and DWORD
+284h therefore all follow from the image. Raw output: [rv_clear.out](rv_clear.out).

## Re-derived (42 checks, 42 PASS, 0 FAIL)

| Claim | Result |
|---|---|
| Caller `0041F730..0041FBE8` is complete | PASS: exact decode, and one `.pdata` record tiles it |
| The seven direct calls are 41F754→memset, 41F95F/41F97A→`006C0520`, 41F990/41F99C→`0046D110`, 41FAFA→`003E5D00`, 41FB5A→`003E37E0` | PASS: exactly these seven, no others |
| The five helper bodies are complete and total 124 bytes; `00861EC0` is the memset thunk | PASS: each decodes exactly, has no call and ends in `ret` or `jmp` |
| `006C0520` targets 210h..220h and 220h..230h, with the fifth scalar from callee stack +28h | PASS: rcx = R+210h, then R+220h; four 4-byte `movss` stores per call |
| `0046D110` → `00202C70` targets 180h..1C0h and 1C0h..200h; it is a copy from `01F204E0`, not a zero fill | PASS: four 16-byte `movups` per call; the source is `01F204E0` |
| `003E5D00` writes 4C0h..510h, 8 bytes per index; EDI is reset from ESI = 0 at 41F9C0; the indices are 0..9 | PASS: emulated edx sequence is 0..9; WORD/DWORD/WORD per index |
| `003E37E0` uses EDX = 0, R8D = 50h and tail-jumps to the fill over 580h..5D0h | PASS: the fill model is reached with (R+580h, 0, 50h) |
| 125 direct non-stack w/rw sites in the caller, LEA excluded | PASS: 125 |
| 47 composed helper writes | PASS: 47 (8 + 8 + 30 + 1) |
| All footprints lie inside 740h | PASS |
| After the 740h fill, exactly one ID0 write (41F795 `WORD [rbx] = bp`) | PASS: full-width intersection |
| No write overlaps DWORD +284h at full width | PASS |
| On return, ID0 = FFFFh and +284h = 0 (under the premises) | PASS: the emulated final bytes are FFFFh and 0 |

### Things this review proves beyond the packet

- The four leaf helpers write none of rbx, rbp, rsi, rdi or xmm6. This is checked from their bytes. Of the callees
  here, only memset (the call at 41F754) depends on the ABI register-preservation premise.
- Values the packet left unsampled:
  - All eight `006C0520` stores write 1.0f. xmm6 is loaded from `01CEBBA8`.
  - The bytes at `01F204E0` in the file image form a 4x4 identity matrix. That address is in the writable `.data`
    section, so the copied values hold only under the packet's "readable constant inputs" premise.
  - Under the emulator's float model, `003E5D00` stores the WORD 4096 at each index. The packet makes no arithmetic
    claim, and this review awards none.

## Controls (9, each must FAIL a named check on a privately patched image; all did)

1. First `006C0520` receiver moved to R+27Ch. The helper span then overlaps +284h. Fails the carrier, footprint and +284h
   checks.
2. 41F771 store moved from +2 to +0. Fails "exactly one ID0 write".
3. 41FA2A DWORD store moved from +288h to +286h. Fails the full-width +284h overlap check and the final-value check.
4. QWORD store of zero at 41F843 moved to +280h. Fails the overlap check while the final value stays 0. This shows the
   overlap test uses the access width, not the start offset or the stored value.
5. Loop bound 10 changed to 80. Fails the index sequence, the 47 count and the `003E5D00` footprint.
6. `003E37E0` fill size 50h changed to 60h. Fails the footprint check.
7. 41F9C0 `mov edi, esi` NOPed. Fails the index checks: the stale FFFFh index escapes the record.
8. memset size 740h changed to 280h. Fails the +284h result.
9. `0046D110` source moved by 40h. Fails the source check.

The packet's own controls (four synthetic and five CLI refusals) were not rerun. These nine are this review's
replacements.

## Narrowing (wording)

- The board summary says "16B scalar stores 210..230". The stores are **four 4-byte scalar (`movss`) stores, 16 bytes per
  call**. The README table ("Four scalar stores, 16 bytes each") can be read the same wrong way. Consumers should write
  "four 4-byte stores per call, 16 bytes per call".

## Scope (kept as the packet states it)

This review supports a conditional, static source result only. It does not award:

- native memset behaviour, beyond the model above;
- caller validity;
- full all-writer closure of +0 or +284h;
- atomicity, reentrancy, lifetime or scheduling;
- live values of `01F204E0`.

The packet's wording respects these limits apart from the narrowing above. The parent slot packet (`aac0489ac`) has its own
review and is not re-reviewed here.

run: rv_clear.py at 80da775cb
