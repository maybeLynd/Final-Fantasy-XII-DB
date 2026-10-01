# WC-1 residue: `eps ` preset-block field meanings (static read, 2026-09-27)

Everything here is STATIC(code): read from the shipping exe (`FFXII_TZA.exe`, base 0x120000). Nothing ran.
Row-level evidence is in `fields.tsv`. `build_fields.py` reads the shipped-value column from
`D:/FFXII_TZA_extract/ps2data/sound/sead.win.config`. `controls.py` prints the controls in `controls.out`.

## Method

1. **Vtables.** For each ctor, I took the first `lea rax,[rip+X]; mov [rcx],rax` as the primary vtable and
   named it through the COL at vtable-8. Then I checked that slot +0x08 returns the classId. Slot +0x30 is
   the applier. Every applier has the same shape: for each field it calls `vft[+0x10] = setParam(id, value, fade)`,
   then (except BuildReverb) `vft[+0x40]`, which is the commit/recompute call.
2. **setParam.** Each setParam routes a paramId to a `SQEX::Sd::DynamicValue<2>` member (vtable 01CB7068, 0x30 B:
   `+8` start, `+0xC` target, `+0x10` elapsed, `+0x14` duration, `+0x1C` curve, `+0x20` active) through
   `007CA560(dv, target, fadeSeconds, curve, 0)`. Some ids go to a plain int member instead. Any clamp or
   unit conversion happens at this step.
3. **Consumers.** Slot +0x40 (commit) and, for BuildReverb, the ICoreEffect process function read the current
   ramp value, either through `007A9E00` or the inlined `start + curve(elapsed/duration)*(target-start)`. They
   turn it into DSP state. I then followed that state into the per-block process function: the secondary
   vtable (object offset 8) slot 3, a thunk that passes `obj+K` as the state pointer. Slot +0x28 (update)
   only advances the ramps and calls commit.
4. **Math helpers.** I named these from their bodies and the import list: 861FAA expf, 861F6E powf, 861FC2 log10f,
   861EBA memcpy. 007B8BA0 is cos and 007B8C80 is sin; the builders use them in the RBJ biquad pattern.
5. **Coverage.** For every DV that a preset field feeds, I swept the class's own functions (ctor, dtor,
   getParam, update, commit, EQ recompute, process) for a read of its `+0x14` duration or `+0xC` target.

Per-class entry points (classId: applier / setParam / commit / process):

| id | class | applier | setParam | commit (vft+0x40) | process |
|---|---|---|---|---|---|
| 1 | SurroundReverb | 007D5F50 | 007D5BD0 (53-arm table 007D5E70) | 007D76E0 + EQ 007D6CD0 | 007D3CB0 (state obj+0x7D0) |
| 2 | Compressor | 007D8F70 | 007D8E40 (table 007D8F44) | 007D9200 | 007D8BE0 (state obj+0x148) |
| 3 | Filter | 007D1970 | 007D1840, type 007D16C0 | 007D1C80 (table 007D1EB0) | 007D1500 (state obj+0xD0) |
| 4 | SideChainInput | 007D8540 | 007D8500 | 007D8580 | 007D82E0 (state obj+0x48) |
| 5 | SimpleFilter | 007D9870 | 007D97F0 | 007D98F0 | 007D9770 (state obj+0x50) |
| 7 | GranularPitchShift | 007DA900 | 007DA8A0 | 007DAA00 | 007DA2E0 (state obj+0x78) |
| 10 | BuildReverb | 007DC340 | 007DC1F0 (table 007DC318) | none (8-slot vtable) | 007DB8D0 (this = obj+8) |

## Results (determined = the code gives the float a role; counts cover the stride's slots)

- **SurroundReverb (32 slots).**
  - Roles determined for 27 slots: wet, dry, FDN input gain, size, RT60 (ms), HF damping, diffusion, ER level,
    late level, pre-delay (ms), ER pattern selector, and 5 EQ bands × {freq, 1/Q} plus 3 peak gains.
  - The 5 band **type ints are ignored** (setParam cases 0xC/0x10/0x14/0x18/0x1C are the no-op epilogue). The bands
    are hardwired as HP, peak, peak, peak, LP. The shipped type codes `{2,7,7,7,1}` match those designs in Filter's
    own numbering (1 LP 007D1080, 2 HP 007D0EA0, 7 peaking 007D1330), which is an independent consistency check.
  - The applier has a copy-paste slip: paramId 0x1C re-reads `+0x58` (007D61ED), so **`+0x68` is never read**.
    This is moot because 0x1C is a no-op.
  - Band 1 and band 5 gain slots (`+0x34`, `+0x74`) are ramped but never consumed.
  - **`+0x7C` (id 0xB → DV obj+0x138) has no DSP consumer.** Only getParam echoes it. Role not determined.
  - Medium confidence: `+0x1C`/`+0x20` (ER vs late level) and `+0x00` (FDN input gain). The 7956-B process
    function was read only around their uses.
- **Compressor (8 slots): 8 determined.** Threshold dB, slope = 1/ratio, input gain dB, make-up dB, attack ms,
  release ms, side-chain bus index, side-chain slot. The shipped preset is all zero: threshold 0 dB, slope 0,
  instant attack and release. That makes it a **0 dBFS brick-wall limiter**, which is a plausible default.
- **Filter (4 slots): 4 determined.** Type selector (0 identity … 8 all-pass), cutoff Hz, Q (stored as 1/Q), and
  shelf/peak A. The shipped type is 0, the identity biquad, so the shipped 2000 / 0.707 / 1.0 have no effect.
- **SideChainInput (4 slots): 1 determined** (capture gain). `+4..+0xC` are never read by its applier.
- **SimpleFilter (4 slots): 2 determined** (mode int, cutoff Hz clamped to [fs/4800, fs/2]). Mode 2's filter shape
  is not determined. `+8/+0xC` are unread.
- **GranularPitchShift (4 slots): 2 determined** (pitch ratio, grain rate Hz). `+8/+0xC` are unread.
- **BuildReverb (8 slots): 8 determined.**
  - Fields: master scale (0..1; composite, medium confidence), dry, wet, early level, late level, pre-delay (s),
    RT60 (s), damping cutoff (Hz).
  - The section's **flag byte (`sec+5`) is a field-count/version gate** in 007DC340. With flag 0 only `+0x00` is
    read and the rest take defaults (1, 1, 1, 0.2, 0.08, 2.0). `+0x1C` needs flag ≥ 2. The shipped flag is 2, so
    all 8 are read. The shipped values equal the applier defaults exactly.
- **classId 9 (stride 0x10):** no class. Arm 9 of the bus-insert table 0x68CCF0 jumps to 007ACA78, the skip path,
  so no applier exists. Role not determined.

## Shipped-file finding: classes 5 and 7 overrun into the next section

Section starts are 0x3A0 (class 5), 0x3B0 (class 6), 0x3C0 (class 7) and 0x3D0 (class 8). Both class 5 and class 7
have `presetCnt=1` and a code stride of 0x10, but their sections are header-only (16 B). So `007ADDC0` returns a
preset block that **is the following class's section header**:

- **SimpleFilter** would receive mode = 0x00100601 (1050113). Commit then leaves the coefficients unchanged.
  Cutoff = 1.4e-45, clamped up to fs/4800.
- **GranularPitchShift** would receive ratio ≈ 1.5e-39 and grain rate 1.4e-45 Hz.

The stride table is confirmed from the code: 01CB49A0 = {0,0x80,0x20,0x10}, 01CB4990 = {0x10,0x10,0,0x10}, and the
literals {0,0x10,0x20} at 007ADE0C–007ADE22. So this is a data/tool mismatch, not a misread of the strides.
It is dormant: the page records that the shipped `bus ` builds no inserts.

A related quirk: Flanger (6) and HilbertFilter (8) have stride 0, but their vft+0x30 is the *same function* as
SimpleFilter's (007D9870) and GranularPitchShift's (007DA900). That is identical-code folding. With stride 0 they
would also read `+0/+4` of whatever follows their header. Out of scope; noted only.

## Controls (controls.out)

- **(a)** For all seven classes, the ctor-installed vtable's COL gives the page's class name, and slot +0x08
  returns the page's classId. This covers SurroundReverb, Compressor, Filter, SideChainInput, SimpleFilter,
  GranularPitchShift and BuildReverb. The bus-insert jump table 0x68CCF0 arms 0–10 resolve to the page's ctors,
  with arm 9 as the skip.
- **(b) Known answers:**
  - Compressor's dB constant 01CB7780 = 0.1151293 = ln10/20 exactly, so expf(x·k) is dB→linear. The −6 dB ctor
    default gives 0.501.
  - Filter's shipped 2000 Hz × 2π × (1/fs cell 01F41D18) = 0.26180 rad = 2π·2000/48000.
  - The Filter Q 0.707 is inverted to 1.414, which is exactly SurroundReverb's shipped per-band value. Both classes
    feed the same RBJ builders, so both mean Q = 0.707.
  - SurroundReverb's damping constant 01CB7598 = ln10/4 exactly, which is Jot's absorptive-filter formula. RT 500
    with the ms delay table gives 10^(−3·len/T), a −60 dB decay after T ms.
  - BuildReverb RT60 2.0 s over comb delays 0.050–0.078 s gives gains 0.84–0.76. Its pre-delay 0.08 s = 3840
    samples, which fits inside the 0.11·fs buffer and under the 0.1 s clamp.
- **(c) Sample rate.** The runtime fs is `[02EAD348]`, written at 007AF064 from the init descriptor. The .data
  *initial images* of the derived cells all encode 48 kHz: 1/fs = 2.0833e-5, fs/2 = 24000, fs/4800 = 10.
  Where I give sample counts, they assume 48 kHz.

## Limits

- No live run. Every role comes from the arithmetic and data flow. The names "ER level" and "late level" for
  SurroundReverb `+0x1C`/`+0x20`, and "FDN input gain" for `+0x00`, rest on partial reads of the 7956-B process
  function (007D3CB0) around the use sites cited. Treat them as medium confidence.
- The "slope = 1/ratio" name for Compressor `+0x04` follows from the static curve. The code never stores a ratio.
- Filter type 6 (007D0F60) and SimpleFilter mode 2 are not classified.
- The page's `008F5F50` "param descriptor" citation is MSVC FuncInfo, as the brief said. No parameter-name strings
  were used or needed; every role above comes from code.
- Coverage sweeps were limited to each class's own functions. The effect objects are reached only through their
  vtables, but a direct outside read of a member was not ruled out image-wide.
