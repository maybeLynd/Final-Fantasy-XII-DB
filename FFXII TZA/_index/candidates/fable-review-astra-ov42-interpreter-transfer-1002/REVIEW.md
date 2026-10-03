# FABLE review: ASTRA ov42-interpreter-transfer

- **Packet:** [ov42-interpreter-transfer README](../../../_experiments/evidence/ov42-interpreter-transfer/README.md)
- **Producer commit:** `76dfc5dc6`. The manifest's sha256 (`c665e817770ddcde`) equals the committed manifest, and all
  51 members hash as listed.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every byte claim re-derives at the bytes:
  - the raw DWORD store in the bridge leaf;
  - the first-resolved pointer as its RDX;
  - the reference getter's scope bits and 24-bit offset;
  - PUSHV's width/kind separation;
  - the pop's tag handling;
  - the native's pop order;
  - the decoder's −1 test and 16-bit `+ 0xD0`.

  An emulation of the original PUSHV, pop and decoder recovers every available queue word through u16, s16 and s32
  loads, and reproduces the packet's 511..534 table and float case. The narrowings add facts about the bridge's
  second consumer, the getter's default scopes, the decoder's mode gate and a discarded result. None contradicts the
  packet.

## Method

[rv_xfer.py](rv_xfer.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is copied
unchanged from the kind-row review (sha256 `69f9bc40be32abcc32b1`). It does not import or run ASTRA's `prove.py`,
`capture.py`, `control.py` or validation scripts, or the shared role adapter.

- It checks the image sha256, the manifest and its members.
- It asserts the instruction text of the bridge leaf `00309C00`, the native `00348330`, the reference getter
  `002650B0`, PUSHV `00267FC0` (with its six-entry jump table resolved), the pop `00267E10`, the native `00348870` and
  the decoder `0030EEA0`.
- It runs a raw `E8`/`E9` census of direct calls to the bridge leaf.
- It emulates (unicorn) the **original** PUSHV, pop and decoder. The resolver is stubbed to supply the record (kind,
  width, pointer, index), and the decoder's unit lookup and its callee are stubbed. The chain is: a raw DWORD in a
  variable, PUSHV at a given width and kind, pop, decoder.
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is rechecked.

Raw output: [rv_xfer.out](rv_xfer.out). 77 checks, 77 PASS, 0 FAIL, 9 of them controls.

## Re-derived

| claim | result |
|---|---|
| The bridge writes the queue value as a raw DWORD, bypassing the typed store | PASS: `00309C00` reads DWORD `022C2178`, returns 0 on −1, else `+ 0x13` `mov dword ptr [rdx], eax` when RDX is non-null |
| Two references are resolved by `002650B0` before the call; the first stays in RSI and becomes RDX | PASS: `00348330` pops (`+ 0x25`), resolves (`+ 0x33`), `mov rsi, rax`; pops, resolves (`+ 0x4C`); `+ 0x51` `mov rdx, rsi`, `+ 0x54` `mov rcx, rax`, `+ 0x5A` call. RSI is not written in between |
| The getter selects a scope from bits 24..26 and masks the offset to 24 bits; width and float fields do not select the store | PASS: `sar eax, 0x18` / `and eax, 7` / `cmp eax, 5`; all seven exits `and eax, 0xffffff`; no other test of the word |
| PUSHV: six widths (u8, s8, u16, s16, s32, f32) from bits 28..31, separate from the kind | PASS: `shr eax, 0x1c` / `cmp eax, 5`; the six jump entries resolve to the six loads in that order; kind = WORD `[rbp − 0x2C]` |
| Kind 1 tags the payload integer, kind 2 tags the same payload float | PASS: tag bytes 1 / 2, the payload DWORD (kind 1) or the same 32 bits via `movss` (kind 2) |
| Depth 0..62 before a push | PASS: both pushes test `cmp eax, 0x3f` / `jge` |
| Pop: tag 1 exact DWORD, tag 2 CVTTSS2SI, empty or negative depth 0, unknown tags the error call | PASS |
| `00348870`: first pop → EBX → EDX, second → ECX, then `0030EEA0` | PASS |
| Decoder: −1 → FFFF, else BX `+ 0xD0` (16-bit) | PASS |
| Low-16 invariant: an integer-tagged transfer with the same low 16 bits and ≠ −1 decodes back to w | PASS: emulated for all 65,534 available words (excluding CF, FFFF) × u16, s16, s32 loads |
| 511..534 through u8 / s8 decode to 255..278 | PASS (emulated) |
| Raw 303 (`0x12F`) loaded as f32, kind 2: CVTTSS2SI gives 0 and the decoder 208 | PASS (emulated; unicorn's default MXCSR) |

Controls (each fails at least one check):
- the bridge store as WORD;
- the bridge RDX from the second resolution;
- the getter's scope mask widened to 4 bits;
- PUSHV's u16 load made signed;
- the pop's CVTTSS2SI made rounding;
- the native's pop order swapped;
- the decoder's 16-bit add made 32-bit;
- the decoder's −1 compare changed.

The null control passes.

## Narrowings

1. **The bridge leaf does more than the store** (already on the availability page, from FABLE's queue-output-alias review). When RCX is non-null it also stores DWORD `022C218C` (the unit value the
   queue arm saved) through the second resolved pointer. It then resets the queue to −1 and returns 1. On a −1 queue
   it returns 0 and writes nothing.
2. **A second direct consumer** (also already on the page, there as "one other direct caller"). The raw census finds two direct calls of the bridge leaf. One is the script native
   (`00348330` + 0x5A). The other is inside the function rooted at `002D5EB0` (a chained record from `002D616B`), which
   passes two stack locals. That second consumer takes the queue without any script store and is not read here.
3. **Scopes 6 and 7 use base 0.** The getter's default exit adds the 24-bit offset to 0, so a reference word with bits
   24..26 = 6 or 7 points the raw DWORD at an absolute address below 16 MiB. Scope 2's base comes from a virtual call
   (`[ctx + 0x98]`).
4. **The decoder is gated.** It writes the decoded word to unit `+0x758` and calls `0030CFB0` only when `0031B7E0`
   returns a unit for the second pop and DWORD `022C2170` is 4. Otherwise it returns −1 or −2. `00348870` discards
   that result and tail-jumps to `00314D40(1)`.
5. **The f32 case uses the default MXCSR.** The emulation ran with unicorn's default MXCSR (exceptions masked). The
   packet's DAZ and rounding remarks are arithmetic, not runs.

## What stays OPEN

- The authored caller and the reference descriptors actually used: whether a script stores the bridge output through
  a u16/s16/s32 integer variable (recovering 511..534) or through u8/s8 or a float (not).
- A valid four-byte writable destination, the declared widths, nonaliasing and lifetime.
- Successful resolution, valid stack state, and the error handler's effects.
- The second consumer's use of the queue value, and the mode-4 gate's writers.
- Whole OV-42 stays OPEN.
