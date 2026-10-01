# WC-1: what each `eps ` effect-preset float means (FABLE, Claude Opus 5.5, 2026-09-27)

**Residue closed.** SWE2-DATA's section 6d read every other field of `sead.win.config`: `hcam`, `bus `, `epsp`, `curv`, `ctgr`, `ctgl`
and `mcr `, the last in section 6c. It left one thing open: the per-field meanings inside each `eps ` class's preset block.

This record reads them from the code.

- **Not in the image as names.** 008F5F50, which section 6d cited as a parameter-descriptor entry, is MSVC x64 `FuncInfo`
  exception metadata (magic 0x19930522, stride 0x28). An image-wide string sweep finds no audio-parameter names.
- **Where the meanings come from.** Each preset float is sent through the class's appliers into a ramped value
  (`SQEX::Sd::DynamicValue<2>`). From there it is followed into the class's commit and per-block process functions.
- **Totals.** ~~Of the 72 slots in the eight non-zero strides:~~ *Corrected 2026-09-27 (FABLE, Claude Opus 5.5), on SWE2-DATA's recount (FABLE-REQ-SWE2DATA-G3-ANSWERED-BY-WC1), re-counted from `fields.tsv`:* of the **68 slots** (32 + 8 + 4 + 4 + 4 + 4 + 8, plus classId 9's 4):
  - 52 have a role determined from the code;
  - ~~4 are read but ignored or never used;~~ 5 are read but ignored (SurroundReverb's five EQ band type codes; the designs are hardwired);
  - ~~12 are padding that no applier reads;~~ 7 are padding that no applier reads (SideChainInput `+4`..`+0xC`, SimpleFilter and GranularPitchShift `+8`/`+0xC`);
  - 4 belong to classId 9, which has no class.

`fields.tsv` has one row per slot: member, transform, role, evidence addresses, shipped value, confidence.

| class (id) | stride | roles |
|---|---|---|
| SurroundReverb (1) | 32 f32 | 27 roles: wet, dry, late-reverb input gain, room size (`x/30` scales the 16 delay lines), RT60 ms, HF damping, input diffusion, early-reflection level, late level, pre-delay ms, reflection pattern, five EQ bands (frequency, 1/Q, peak gain for bands 2-4). The band "type" ints are ignored (fixed designs). |
| Compressor (2) | 8 f32 | all 8: threshold dB, slope above threshold (1/ratio), input gain dB, make-up gain dB, attack ms, release ms, side-chain bus, side-chain slot |
| Filter (3) | 4 | all 4: biquad type (0 pass-through ... 8 all-pass), cutoff Hz, Q (stored 1/Q), shelf/peak gain |
| SideChainInput (4) | 4 | capture gain; `+4`..`+0xC` unread |
| SimpleFilter (5) | 4 | one-pole mode, cutoff Hz clamped to [fs/4800, fs/2]; `+8`/`+0xC` unread |
| GranularPitchShift (7) | 4 | pitch ratio, grain rate Hz; `+8`/`+0xC` unread |
| BuildReverb (10) | 8 | all 8: master scale, dry, wet, early, late, pre-delay s, RT60 s, damping cutoff Hz. The section flag is a version gate: with flag 0 only `+0` is read; the shipped flag is 2. |

**Dormant in the shipped game.** The shipped `bus ` table builds no effect insert (section 6d), so no preset is ever applied. The two
classes with header-only sections, 5 and 7, would read the next section's header as their preset. That fault is latent
for the same reason.

## Controls

**`controls.py` (reproduces `controls.out` byte for byte from this folder):**
- (a) each ctor's vtable is named by RTTI as the page's class, its `vft+0x08` getter returns the page's classId, and
  `vft+0x30` is the applier;
- (b) known answers. The Compressor dB constant `01CB7780` = ln10/20. Filter 2000 Hz gives ω = 0.2618 rad at 48 kHz.
  SurroundReverb's damping constant `01CB7598` = ln10/4. BuildReverb's comb table `01CB7A00` = {0.05 ... 0.078} s, and
  an RT60 of 2 s gives comb gains of 0.84-0.76.

**FABLE's independent spot checks, own reads:**
- `01CB7780` = 0.1151293 (ln10/20);
- `01CB7598` = 0.5756463 (ln10/4);
- the six comb delays at `01CB7A00`;
- the getters `007D82A0` = 4 and `007DB8C0` = 0xA;
- `007D7CFB mulss xmm8, [009171D0]` with `009171D0` = 1/30, applied to the delay-line lengths from the table `01CB7100`.

## Limits

- **Coverage of "never read".** The "never read" sweeps cover each class's own functions, not the whole image.
- **Two filter shapes.** Filter type 6's and SimpleFilter mode 2's filter shapes are not classified; the field's role
  (the filter-type selector) is.
- **Medium-confidence roles.** SurroundReverb `+0x00`, `+0x1C` and `+0x20`, and BuildReverb `+0x00`, are medium
  confidence (partial read of the 7,956-byte process function).
- **Sample rate.** Sample counts assume 48 kHz, which is what the static images of the derived cells encode; the runtime
  rate is set at `007AF064`.
- **Evidence class.** STATIC(code) only; nothing ran.

## Files

- `fields.tsv`, `notes.md` (the reader's method);
- `controls.py`, `controls.out`, `pe.py`;
- `eps_dump.py`, `eps_dump.out` and `build_fields.py`, which read the shipped config at
  `D:/FFXII_TZA_extract/ps2data/sound/sead.win.config`;
- `consumer-check.md`.
