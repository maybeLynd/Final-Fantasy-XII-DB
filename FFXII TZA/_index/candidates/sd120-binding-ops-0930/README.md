# SD-120: the eight `0050xxxx` binding operations are palette (CLUT) animation effects (SWE2-ORACLE, 2026-09-30)

Register row SD-120 asks what each of the eight `0050xxxx` binding operations does. The row points at
[the-largest-unclassified-functions.md](../../../99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md)
sections 7, 16, 18 and 19. Both byte-opcode dispatchers, `003CCF20` and `003CD2C0`, map opcodes 1 to 8 to the same
eight bodies (`dd-data-3-0930/ui_bi17_dispatch.py`).

The checker is `sd120_ops.py`. Its output is `sd120_ops.out`, which ends `FAILS 0` (33 checks). It uses two
instruments:

- **Static.** `txt(addr)` compares the exact capstone mnemonic and operands at every cited site, and `ripref(addr)`
  resolves a rip-relative target.
- **Execution.** `sd120_emu.py` runs the shipped bodies in Unicorn on controlled memory: the image's own BSS buffers and
  a scratch record page. Two calls are bridged. The VCRUNTIME140 `memcpy` thunk `00861EBA` is performed in Python. The
  stack probe `__chkstk` `00808F10` is returned without running (it only touches guard pages). Everything else is the
  shipped code.

Each M-check runs a Python model against the native result over seeded random trials. **The model is the claim and the
native run is the control.** The instrument is not vacuous. While this record was being built, two first-draft models
failed against the native code and were corrected from the code:

- op7 on unmasked lanes: 159 of 300 trials failed;
- op1 mode 2 with negative shifts: 10 of 400 trials failed.

## What the machine works on (SWE2-ORACLE)

**The working buffer is a colour lookup table (CLUT), measured.** Checks K1 and K2:

- `003CD840(src, buf, n)` unpacks `n` = 1, 16 or 256 RGBA8 entries into `buf`. Each entry becomes 16 bytes, four s32
  lanes of `byte << 8` (8.8 fixed point). A 256-entry table is read in the PS2 CSM1 order, where entries 8–15 and
  16–23 swap in every 32.
- `003D2B60(buf, dst, n)` packs the entries back. Each lane is shifted right by 8, clamped to 0..255 and written in the
  same order. Nothing past `n` entries is touched.
- Lane `c` is byte `c` of the RGBA8 dword. **Reading the lanes as R, G, B, A is an interpretation.** It rests on the
  PS2 CLUT byte order and on op5's BT.601 weights landing on lanes 0, 1 and 2.

**Per binding entry**, the dispatcher runs three steps (D3):

1. `003CD840(entry +8 → 02B477A0, n = entry word +2)`;
2. the entry's operation list;
3. `003D2B60(02B477A0 → entry +0x10, n)`.

**So a binding is: a source palette, the operations that animate it this frame, and a destination palette.** Linking
this to the GFZ-named "render-model subresource-variant bindings" (§19) is the page's reading, not a new
measurement.

### Arguments the dispatchers pass (D1, D2, D5, D6)

| caller | working buffer | ops 1, 2, 3, 5, 6, 7 | ops 4, 8 |
|---|---|---|---|
| `003CCF20` (the timed pass over the work list) | `02B477A0` | `(rcx = buffer, rdx = record)` | `(rcx = buffer, rdx = second CLUT, r8 = record)`; second CLUT decoded into `02B487A0` (op 4) / `02B497A0` (op 8) |
| `003CD2C0` (one binding, by handle, at once) | `02B4A7A0` | the same | second CLUT into `02B4B7A0` / `02B4C7A0` |
| `00431B10` (the expression evaluator) | `02CA4EE0` | builds a record on its stack from a 16-byte authored item: kinds 1, 2, 3, 5, 6, 7 → ops 1, 2, 3, 5, 6, 7 | kind 4 returns 0; op 8 absent |

**The second CLUT for ops 4 and 8** (D2):

- Record `+0x20` is a handle into the 32 × 64-byte handle table `02B47790`, generation-checked at `+4`.
- That entry's `+0x10` is its destination palette. It is used raw, or through `0036B130` when entry `+1 & 0x3F`.
- It is decoded with the entry's own word `+2`.

**Interpretation:** ops 4 and 8 blend toward *another binding's* current palette.

### The record fields every operation reads (D4, P0)

The record is the 80-byte pool entry.

| field | meaning | evidence |
|---|---|---|
| `+0x00` byte | opcode 1–8 | `003CD0E6` |
| `+0x03` byte | lane mask, bits 0–3 → lanes 0–3 | each op's `sbb` masks; P0 |
| `+0x08` word | lifetime. When elapsed passes it, the record is released inline and unlinked | `003CD003`, `003CD028` |
| `+0x0A` word | start delay. Counted down by the dispatcher's `dt` argument (`r14`); the overshoot seeds `+0x34` | `003CCFD9`, `003CCFEA` |
| `+0x0E` word | time divisor: `t = +0x36 / +0x0E` when non-zero | P0 |
| `+0x10` word, `+0x15` byte | loop length; loop mode 0 wraps, 1 ping-pongs | `003CD085`–`003CD0D9` |
| `+0x12` word, `+0x14` byte | entry count and first entry: the range `[+0x14, +0x14 + +0x12)` | P0 |
| `+0x34` word | elapsed time | `003CCFF5` |
| `+0x36` word | local time after the loop, the operations' `t` | D4 |
| `+0x20`…`+0x2A` | per-operation operands (below) | P1–P8 |
| `+0x28` qword | op 8: the curve pointer | `0050718F` |

## The eight operations (SWE2-ORACLE)

`t` is the local time from above. "Masked" means the lanes selected by `+0x03`. Every sum saturates to s32. Products
are the PS2 `PMULTH` form: the signed low halfword of each lane, as the translated code computes it.

| op | body | operands | what it does (M-check, exact) | callees by role |
|---|---|---|---|---|
| **1** | `0050AC20` (6,192 B) | `+0x20` s16 speed, `+0x22` mode | **Permute the range** by shift `s = t·speed`. Mode 0 rotates cyclically (mod n). Mode 1 shifts with edge clamping. Mode 2 mirrors (period 2n; see Q3). Mode 3 and up is a no-op. Only masked lanes move. **Palette cycling.** (M1) | `00808F10` `__chkstk`, a 4 KB stack frame; `00861EBA` `memcpy`, the range via a stack copy; `00808C40` cookie check |
| **2** | `00506B40` (1,501 B) | `+0x20..+0x26` 4 × s16 `v`, `+0x28` cap on `t`, `+0x2A` mode | Mode 0: **add `v·t` colour units** (`t` ≤ 255): a linear additive tint ramp. Mode 1: **add `(c·v/128)·t`**: a proportional brightness ramp. (M2) | `00506A40`, the 8-lane s16 product (`PMULTH`), mode 0 |
| **3** | `005080A0` (3,048 B) | `+0x20` RGBA8 colour, `+0x24` duration, `+0x26` mode | **Fade the range to one colour.** Mode 1 cross-fades with weight `(t<<8)/dur`, then copies at `t ≥ dur`. Mode 0 steps each lane `t` colour units toward it, then copies at `t ≥ 255`. (M3) | none (call-free) |
| **4** | `0050A100` (2,842 B) | second CLUT, `+0x24` duration, `+0x26` mode | **Fade the range to another palette**, entry by entry. The same two modes as op 3. (M4) | none; the dispatcher's `0036B130` → `003CD840` supply the target |
| **5** | `00509BB0` (1,345 B) | `+0x20` duration | **Desaturate** lanes 0–2 toward `Y = (77·R + 150·G + 29·B)/256` (BT.601 weights, `00D22850`). The partial weight is the byte `(t<<8)/dur`, then it copies `Y` at `t ≥ dur`. Lane 3 is untouched. (M5) | none |
| **6** | `00507490` (3,074 B) | `+0x20..+0x22` colour, halfword `+0x23` strength `G` (`0x80` = 1.0), `+0x24` duration | **Tint** lanes 0–2 toward the colour: `F = 2·col·G + (A>>7)·(0x80 − G)`, which is `A + (G/128)(col·256 − A)`. Then cross-fade `A → F` over `dur`. (M6) | `00808C40` cookie check |
| **7** | `00508C90` (3,861 B) | `+0x20` colour, `+0x24` s16 speed, `+0x26` ramp width | **Sweep the colour through the range.** The head is at `p = t·speed` entries. Behind it, a linear ramp `+0x26` entries wide (weights `k·256/width`, float) leads into full colour. Positive speed sweeps up from `+0x14`, negative speed sweeps down from the end. At `|p| − width ≥ n` the whole range is the colour. (M7) | none |
| **8** | `00507120` (867 B) | second CLUT, qword `+0x28` curve | **Cross-fade the range to another palette** with weight `(int)(256·curve(t))`. (M8) | `0053DB50`, the curve evaluator (K3) |

**`0053DB50` (K3).** It takes 16-byte keys `(time, value, in-tangent +8, out-tangent +0xC)`, with the count at `+4`
and the keys from `+0x10`. It clamps outside the keys and bisects inside them. It then interpolates as a **cubic
Hermite**, with the tangents scaled by the key interval. The maximum error against that formula is 2e-6. Keys at
(0, 0) and (10, 1) give 0.15625 at t = 2.5, not the linear 0.25.

**Taken together (interpretation):** colour cycling, fades to a colour or to another palette, additive and
proportional tints, desaturation, tinting and wipe-sweeps. These are the classic palette-animation effects, applied to a
render-model's CLUT per frame.

## Native quirks the models reproduce (SWE2-ORACLE)

These describe measured behaviour. None of them is a claim about intent.

- **Q1, op 7 writes below the buffer.** On negative speed the start index is `n − (+0x14) − |p|`: `005096BF` subtracts
  the start byte where the positive arm adds it. With a non-zero start byte, a sweep whose `|p|` exceeds `n − start`
  writes entries **below `02B477A0`**. The 56-byte machine state `02B47770..02B477A0` sits there (§19). This happened
  in 14 of the 300 M7 trials, and the model reproduces them exactly.
  - **Reachability is narrowed.** `00431B10` zero-extends the speed byte, so the expression path never goes negative
    (X3). Whether any dispatcher-path record carries a negative speed with a non-zero start byte is not surveyed.
- **Op 7's ramp also moves unmasked lanes.** The per-entry weight vector is built from an unmasked step (`022D92F0`,
  saved before the `pand` at `005091CD`). The colour is masked, so an unmasked lane in the ramp is pulled toward 0. In
  the full-colour part, unmasked lanes are kept.
- **Q2, op 6's strength overlaps the duration.** The strength halfword `+0x23` has, as its high byte, the low byte of
  the duration word `+0x24`. `00431B10` kind 5 writes duration 100, so `G` = `0x64xx`, about 200 × the `0x80` unit. The
  visible result after `003D2B60`'s clamp is not evaluated here. Whether authored dispatcher records avoid the overlap
  is not surveyed.
- **Q3, op 1 mode 2 is asymmetric.** A negative shift in `(−2n, −n]` mirrors without doubling the edge entry. Positive
  shifts double it. So `−7` and `+5` (n = 6) give different permutations.

## What stays narrowed (SWE2-ORACLE)

- **Who fills the operands of a dispatcher-path record.** The allocator `003CCC20` copies 48 bytes from its caller
  (X1). Its callers are `00504D30` (`RenderModelInstance_EnsureSubresourceVariantBinding`) and `00468160`. They were not
  read, so the authored values of `+0x20..+0x2F` per opcode, and the curve tables for op 8, are not characterised.
- **Other parts not read:**
  - the allocator's `+0x0C != 0` arm (RNG state `022D9138`);
  - `004314E0`, the expression path's time source;
  - the entry fields `+0x01` bit 7 / `0x40` and `+0x38`, beyond what the dispatcher tests;
  - the `00181DD0` gate.
- **The mode-0 time scales are measured only at the operation's input.** A step per frame is `t` colour units, and op 2
  adds `v·t`. How the authored `+0x0E` divisor makes that per-frame or per-second is not measured.

## Contradictions with published text (reported to OPUS, not edited) (SWE2-ORACLE)

1. [the-largest-unclassified-functions.md](../../../99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md)
   §18 makes three statements the code contradicts:
   - It says "32-byte payload". **`003CCC20` copies 48 bytes** (`003CCC8E`/`003CCC93`), and the operations read
     operands at `+0x20..+0x2A` (X1).
   - It says `+0x34` is "bounds-checked by dispatch against something unidentified". **It is the elapsed-time counter
     compared with the lifetime `+0x08`** (D4).
   - It says record `+0x38` / `+0x40` are pointers whose "writers were not found", and handle-entry `+0x28` / `+0x30`
     are "written only". **They are the operation list:** head and tail in the entry, next and prev in the record.
     `003CCC20` links a record in, `003CCF20` unlinks it, and both dispatchers read `+0x28` (X2). This bears on
     SD-122.
2. [the-world-tick-and-the-field-frame.md](../../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
   has three EC-7 one-liners the code contradicts:
   - Line 2589 calls `0050A100` "the flag-pack scan … a call-free jump-threaded packer". **It is op 4, a palette
     cross-fade** (M4).
   - Line 2597 says `00507120` "runs the per-item step" through `0053DB50`. **`0053DB50` is called once per call for
     the blend weight**; the per-item loop is the translated `PMULTH` blend (M8).
   - Line 2621 says `0053DB50` does "a linear probe" and "bisects the 8-byte pairs". **The keys are 16 bytes**
     (`add rcx, rcx` + `[r9 + rcx*8]`) and the interpolation is cubic Hermite (K3).
3. [how-an-authored-number-gets-its-randomness.md](../../../02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md)
   line 556 calls the six `0050xxxx` bodies reached from `00431B10` a "formatter". **They are CLUT operations** on
   `02CA4EE0`, which `00431B10` decodes and `003A9C10` then consumes (D6). What `003A9C10` does was not read.

## Files (SWE2-ORACLE)

- `sd120_ops.py` / `sd120_ops.out`: the checker (33 checks, `FAILS 0`, about 10 s).
- `sd120_emu.py`: the Unicorn harness. It needs `unicorn` 2.x and `pefile`, plus the image at
  `Database/Tools/work/exe/FFXII_TZA.exe`.
