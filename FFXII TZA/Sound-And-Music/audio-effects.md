[Home](../../README.md) / [Sound and music](README.md) / Audio effects

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Audio effects: the filters, reverbs, compressor, flanger, pitch shifter and frequency shifter the sound driver can run on a voice or a bus | system | Sound and music | The sound engine | The sound driver's effect classes: their type numbers, builders and per-block bodies, the polynomial sine and cosine they share, the biquad filter with its nine shapes and coefficient formulas, the one-pole filter every voice carries, the flanger, the granular pitch shifter a music voice can carry and its switch, the Hilbert frequency shifter, the compressor with its side-chain input, the surround reverb's delay network and equaliser, and which of them the shipped game builds. | 0x007D1500, 0x007D1C80, 0x007D9770, 0x007D9C60, 0x007DA2E0, 0x007DACF0, 0x007D8BE0, 0x007D3CB0 |

## What the player sees

- Every sound passes through a low-pass filter that can muffle it.
- A music voice can carry a pitch shifter that changes the pitch without changing the speed; no shipped music
  asks for one.
- The final mix has no reverb, compressor or equaliser: the shipped configuration gives the one master bus no effects.

## How it works

### The effect classes

An effect is a `SQEX::Sd::Driver` object with two vtables: its own, and the `ICoreEffect` interface at `+0x08`.
Slot 1 of its own vtable returns its type, the number a bus record names ([Sound engine configuration](sound-engine-config.md)):

| Type | Class | Vtable | Built by | Block body |
|---:|---|---|---|---|
| 0 | `EmptyEffect` | | `0x007AC4F0` itself, `0x18` bytes | |
| 1 | `SurroundReverb` | `0x01CB7528` | `0x007D2150` | `0x007D3CB0` |
| 2 | `Compressor` | `0x01CB7710` | `0x007D85E0` | `0x007D8BE0` |
| 3 | `Filter` | `0x01CB7078` | `0x007D0AC0` | `0x007D1500` |
| 4 | `SideChainInput` | `0x01CB7698` | `0x007D80E0` | `0x007D82E0` |
| 5 | `SimpleFilter` | `0x01CB77A8` | `0x007D9530` | `0x007D9770` |
| 6 | `Flanger` | `0x01CB7828` | `0x007D99E0` | `0x007D9C60` |
| 7 | `GranularPitchShift` | `0x01CB78A8` | `0x007DA0A0` | `0x007DA2E0` |
| 8 | `HilbertFilter` | `0x01CB7920` | `0x007DAAB0` | `0x007DACF0` |
| 10 | `BuildReverb` | `0x01CB7998` | `0x007DAFF0` | `0x007DB8D0` |

The type slots are `0x007BD590` (1), `0x007E3260` (2), `0x007D14C0` (3), `0x007D82A0` (4), `0x007D9730` (5), `0x007D9C20` (6),
`0x007DA2A0` (7), `0x007DACB0` (8) and `0x007DB8C0` (10). Byte `+0x10` is a bypass flag that interface slot 1 `0x007ACD20` reads.

### Running an effect

Slot 3 of the interface runs the effect on one block. It passes the buffer as both input and output, so every effect
works in place, with the frame count at `+0x08` and the channel count at `+0x0C` of its argument¹. Each thunk hands its body the effect's state block: `0x007D14D0` (Filter), `0x007D3C90` (SurroundReverb),
`0x007D8BB0` (Compressor), `0x007D82B0` (SideChainInput), `0x007D9740` (SimpleFilter), `0x007D9C30` (Flanger), `0x007DA2B0`
(GranularPitchShift) and `0x007DACC0` (HilbertFilter).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007D14D0`, `0x007DACC0` |

</details>

The bodies of the filter, the one-pole filter, the flanger, the compressor and the reverb work on eight interleaved
floats per frame, one per output channel; the pitch shifter and the frequency shifter loop over the given channel count.

Other slots of an effect's own vtable, where they were read:

| Slot | Does | Read in |
|---:|---|---|
| `2` | sets a parameter by id, with a ramp time | `0x007D1840` (Filter), `0x007D8E40` (Compressor) |
| `3` | reads a parameter back | `0x007DA1C0` (`0x600`, `0x601`), `0x007DAC30` (`0x700`) |
| `5` | advances the parameter ramps and recomputes when one moved | `0x007D1A10` (Filter), `0x007DA970` (GranularPitchShift) |
| `6` | re-applies the four filter parameters; a null argument returns -1 | `0x007D1970` (Filter) |
| `8` | recomputes the coefficients from the current ramp values | `0x007D1C80`, `0x007D9200`, `0x007D98F0`, `0x007D9EA0`, `0x007DAA00`, `0x007DAF70` |

### Sine and cosine

`0x007B8C80` (sine) and `0x007B8BA0` (cosine) are the polynomial approximations every effect uses. Both reduce the angle
to -pi..pi by rounding `x / 2pi` (`0.15915494` at `0x00D22590`), fold it into -pi/2..pi/2, and evaluate:

```python
y2 = y * y
sin = y * (1 + y2*(-0.16666667 + y2*(0.008333331 + y2*(-0.00019840874 + y2*(0.0000027525562 - y2*0.000000023889859)))))
cos = s * (1 + y2*(-0.5 + y2*(0.041666638 + y2*(-0.0013888378 + y2*(0.000024760495 - y2*0.00000026051615)))))
```

`s` is -1 when the cosine's fold crossed pi/2 and 1 otherwise; the constants sit at `0x01CB5194`-`0x01CB51B0`,
`0x009159F4` and `0x01CEBB70`.

### The filter

`Filter` is a biquad, run by `0x007D1500` in direct form 1 on each of the eight channels, with its coefficients at
`+0xD0` and its histories after them:

```python
y = b0*x + b1*x1 + b2*x2 - a1*y1 - a2*y2
```

`0x007D1840` takes four parameters. `0x200` ramps the frequency, with curve 5 when it falls and 4 when it rises; `0x201`
ramps the reciprocal of Q, a value of 0 counting as 1; `0x202` ramps the gain; `0x203` changes the shape. With a time above 0,
`0x007D16C0` ramps the old shape towards a neutral setting over half the time, and `0x007D1A10` then switches the shape and
ramps from neutral to the stored values. A time of 0 recomputes at once.

`0x007D0AC0` builds it as shape 1 at 2,000 Hz, 1/Q 1.414 and gain 1.0, with pass-through coefficients, and stores
`1 / device rate` at `0x01F41D18`. `0x007D1C80` turns the frequency into `w = f * 2pi * [0x01F41D18]` and fills the five
coefficients by shape:

| Shape | Kind | Coefficients |
|---:|---|---|
| `0` | pass | `b0` 1, the rest 0 |
| `1` | low-pass | `0x007D1080` |
| `2` | high-pass | `0x007D0EA0` |
| `3` | band-pass | `0x007D0DD0` |
| `4` | notch | `0x007D1280` |
| `5` | low shelf | `0x007D1140`, using the gain |
| `6` | high shelf | `0x007D0F60`, using the gain |
| `7` | peaking | `0x007D1330`, using the gain |
| `8` | all-pass | `0x007D0D30` |

Each coefficient function stores `a1, a2, b0, b1, b2` in that order, from `alpha = sin(w) * 0.5 * (1/Q)`. All but the
all-pass divide by `(1 + alpha) / 0.9999`, so their poles sit just inside the unit circle:

| Function | `b0` | `b1` | `b2` | `a1` | `a2` |
|---|---|---|---|---|---|
| `0x007D1080` | `(1 - cos w) / 2` | `1 - cos w` | `(1 - cos w) / 2` | `-2 cos w` | `1 - alpha` |
| `0x007D0EA0` | `(1 + cos w) / 2` | `-(1 + cos w)` | `(1 + cos w) / 2` | `-2 cos w` | `1 - alpha` |
| `0x007D0DD0` | `alpha` | 0 | `-alpha` | `-2 cos w` | `1 - alpha` |
| `0x007D1280` | 1 | `-2 cos w` | 1 | `-2 cos w` | `1 - alpha` |
| `0x007D1330` | `1 + alpha * A` | `-2 cos w` | `1 - alpha * A` | `-2 cos w` | `1 - alpha / A` |
| `0x007D0D30` | `1 - alpha` | `-2 cos w` | `1 + alpha` | `-2 cos w` | `1 - alpha` |

`A` is the gain; the peaking filter divides by `1 + alpha / A` instead. The shelves `0x007D1140` and `0x007D0F60` use the
same `A` with `2 * sqrt(A) * alpha`. The bodies receive `w` and the ramped values from `0x007D1C80`.

`0x007D1C80` reads the frequency ramp at `+0x38` the way `0x007A9E00` reads the 1/Q ramp `+0x68` and the gain ramp
`+0x98`: the target `+0x44` while the ramp time `+0x4C` is 0¹, otherwise
`+0x40 + (+0x44 - +0x40) * 0x007A9E50(+0x48 / +0x4C, curve +0x54)`². A shape above 8 leaves
the coefficients as they were³, and shape 0 stores `b0` = 1.0 and zeroes the other four⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007D1C9E` |
| ² | `0x007D1CA7`-`0x007D1CC9` |
| ³ | `0x007D1CE2`-`0x007D1CE5` |
| ⁴ | `0x007D1D00`-`0x007D1D11` |

</details>

### The one-pole filter

`SimpleFilter` is the low-pass every voice carries as effect 0 ([Sound engine](sound-engine.md)). `0x007D9770` runs it on
each of the eight channels:

```python
y = b * x + a * y1
```

`0x007D98F0` sets `a` (`+0x50`) and `b` (`+0x54`) from the frequency ramp and the mode `+0x48`, with `w = f * 2pi *
[0x01F41D20]`:

| Mode | `a` | `b` |
|---:|---|---|
| `0` | 0 | 1 |
| `1` | `exp(-w)` | `1 - a` |
| `2` | `exp(w - pi)` | `1 - a` |

`0x007D9530` builds it in mode 0 at 2,000 Hz. It stores `1 / device rate` at `0x01F41D20`, half the rate at `0x01F41D24`,
that half divided by 2,400 at `0x01F41D28`, and minus the base-10 logarithm of their ratio at `0x01F41D2C`. `0x007D9600`
puts back the base vtables of the voice's embedded filter when the voice is torn down¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007EA32E` |

</details>

### The flanger

`Flanger` mixes each frame with a copy read from a 2,048-frame eight-channel ring (`+0x130`, write index `+0x10130`).
`0x007D9C60` reads the copy at:

```python
read = write - delay + sin(phase) * depth          ; wrapped into 0..2047
out  = dry * x + wet * ring[read]
phase += step                                       ; 5.1415925 is subtracted once it passes pi
```

The subtracted constant at `0x01CB7898` is not 2pi, so the sweep is not a whole sine¹.
`0x007D9EA0` fills the values from five ramps:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007D9D6D`-`0x007D9D78` |

</details>

| Value | From | Note |
|---|---|---|
| delay `+0x110` | ramp 1 | whole frames, at most 1,023 |
| depth `+0x124` | ramp 2 | times the delay |
| step `+0x120` | ramp 3 | `rate * 2pi / device rate` |
| dry `+0x114` | ramp 4 | built at 1.0 |
| wet `+0x118` | ramp 5 | |

### The pitch shifter

`GranularPitchShift` changes pitch with two read heads moving through a 14,400-frame ring (`+0x98`, write index
`+0x70898`). `0x007DA2E0` advances a grain clock by its step each frame and wraps it at 1:

1. When the clock passes 0.25 the first head restarts, and at 0.75 the second: its delay starts at `(pitch - 1)`
   grain lengths when the pitch is above 1, and at 0 otherwise.
2. Each frame each head's delay grows by `1 - pitch` frames, so a pitch below 1 falls behind the input.
3. Each head reads its delay with linear interpolation, and the output is `w * head2 + (1 - w) * head1`, with
   `w = (sin(2pi * clock) + 1) / 2`.

`0x007DAA00` takes the pitch (parameter `0x600`, built at 1.0) into `+0x78` and the grain rate (`0x601`, built at
10.0) as rate over the device rate into `+0x7C`; `0x007DA1C0` reads either back. A music voice gets one
([Interactive music](interactive-music.md)).

`0x007EA850(voice, on)` switches a voice's shifter: it looks for an effect of type 7 among effects 1 onward
(`+0x108`, count `+0x74`) and works on effect 1. When switching on a bypassed shifter it first sets `0x600` to 1.0,
and it then stores the opposite of `on` in the bypass flag. It returns -1 for an ended voice or when no effect matches.

### The frequency shifter

`HilbertFilter` shifts every frequency by a fixed number of hertz. `0x007DACF0` runs an eight-tap Hilbert filter on
each channel's history and mixes it with the input four frames back:

```python
h   = -0.2122*x[n-1] - 0.6366*x[n-3] + 0.6366*x[n-5] + 0.2122*x[n-7]
out = cos(phase) * x[n-4] - sin(phase) * h
phase += 2pi * f / device rate                 ; wrapped at 2pi
```

The taps are `+-2/pi` and `+-2/(3pi)`, which `0x007DAAB0` stores at `+0x58`-`+0x70`. The shift `f` is parameter
`0x700`, built at 1 Hz; `0x007DAF70` turns it into the step `+0x4C`, and `0x007DAC30` reads it back.

### The compressor

`Compressor`¹ takes eight parameters through `0x007D8E40`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007D85E0` |

</details>

| Id | Value | Stored as |
|---|---|---|
| `0x100` | threshold in dB, built at -6 | `10^(dB/20)`, by `exp(x * 0.115129255)` |
| `0x101` | slope | as given |
| `0x102`, `0x103` | input and output gain in dB | `10^(dB/20)` |
| `0x104`, `0x105` | attack and release in ms | seconds |
| `0x106`, `0x107` | the bus and the effect index of a side-chain input | whole numbers |

`0x007D9200` turns them into its block: threshold `+0x148`, slope `+0x14C`, gains `+0x150` and `+0x154`, attack
`exp(-2 / (attack * rate))` at `+0x158` and release `exp(-1 / (release * rate))` at `+0x15C`. The rate `+0x138` is
the builder's argument. It looks the side chain up¹ and keeps it at `+0x168` only when its type is 4.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007AC3E0` |

</details>

`0x007D8BE0` works on each channel with an eight-value gain state, built at 1.0:

```python
d = |side-chain sample|, or |x| without a side chain
g = (d + min((slope - 1) * (d * inGain - threshold), 0)) / d     ; 1.0 when the sum is 0 or less
state = g + (g < state ? attack : release) * (state - g)
out = x * outGain * state                                          ; times inGain without a side chain
```

The zero and one vectors it compares with live at `0x02EAE040`-`0x02EAE07F`, which the builder fills¹.
`0x007D8210` gives a side-chain input's buffer, and `0x007D89A0` puts back the base vtables and frees the gain state.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007D8794`-`0x007D87A9` |

</details>

The state step works on `g + 1e-25`, the four floats at `0x01CB7790`¹, both in the attack or
release choice and in the step, and takes the same amount off the new state², so
`state = g + c * (state - g - 1e-25)` with `c` the attack or release. With a side chain the body reads its buffer
through `0x007D8210`³; without one it reads its own input and takes `outGain * inGain` as the
output gain, worked out once per block⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007D8D60`, `0x007D8D67` |
| ² | `0x007D8DAE`, `0x007D8DB2` |
| ³ | `0x007D8C8E` |
| ⁴ | `0x007D8C81` |

</details>

### The side-chain input

`SideChainInput` is a pass-through effect that keeps a copy for a compressor to listen to. `0x007D82E0` copies the
block into its buffer (`+0x48`, sized by `0x007AECD0` at build) and to the output, then scales every sample in the
buffer by `+0x54` and adds `+0x58`.

### The surround reverb

`SurroundReverb` keeps its state block at `+0x7D0`, and `0x007D3CB0` runs it once per frame:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | It writes the input frame into a 24,000-frame eight-channel history (`+0x10` of the block; wrap at `0x007D5682`). |   |
| 2 | For each output channel (count `+0x0C`), it sums 19 taps of that history, each with its own delay and gain. The byte table `0x01CB73E0` picks one of two delay sets per channel. | `0x007D482F` |
| 3 | It reads 16 delay lines, damps each with a one-pole filter, and mixes them with a 16-point Hadamard transform after scaling each line (`0x007D3B80`, called at `0x007D4D98`): line `i` times the state block's `[+0x418][i]`, then unnormalised butterflies `a + b`, `a - b` at strides 1, 2, 4 and 8. |   |
| 4 | It writes the mixed lines back: each sample `k` of line `i` becomes `mixed[i][k] + v[i] x s[k]`, `v[i] = [+0x410][i]` (the pointer `0x007D3D0E` reads is parked at `[rbp+0x18]` by `0x007D3D7E` and reloaded at `0x007D4DA8`), with the same eight samples `s` for every line. | `0x007D4DB2`-`0x007D4DF2` |
| 5 | `s = 0.125 x (p + a + r)` per sample (`[0x00D90640]`, `0x007D4CBC`-`0x007D4CC6`): `p` the quad pair formed at `0x007D4B6D` and `0x007D4B81`, `a` the output of the third allpass stage (coefficient `[+0x12C]`, `0x007D4C6A`, `0x007D4C7A`) and `r` the ring sample read at `0x007D4C9F`, added at `0x007D4CB0`. |   |
| 6 | It runs the output through three filter stages, `0x007D3200` twice and `0x007D33B0`. | `0x007D54A7`-`0x007D54EF` |
| 7 | It moves every line's position on, wrapping each at its length, and moves on four further rings. |   |

The rings are 16,384, 1,024, 2,048 and 2,048 frames long, the last three read 367, 512 and 1,179 frames back¹. `0x007D33B0` is one frame of an eight-channel direct-form-1 biquad; `0x007D3200` is the same
frame with both feedback terms taken from the input history (`y = b0*x + (b1 - a1)*x1 + (b2 - a2)*x2`). With their
flags set, both flush tiny values by adding and subtracting 1.0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007D55A3`-`0x007D563E` |

</details>

`0x007D6CD0` recomputes the reverb's ten equaliser biquads, `0xA0` bytes apart from `+0xBF0`, from parameter ramps
`0x30` bytes apart from `+0x230`. They are a high-pass, three peaking filters and a low-pass, then a low shelf, three
peaking filters and a high shelf¹. The builder calls it², as do slots 5 and 6.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007D0EA0`, `0x007D1330`, `0x007D1080`, `0x007D1140`, `0x007D0F60` |
| ² | `0x007D2DE1` |

</details>

`0x007D1EE0` zeroes the filter histories of the block the builder hands it¹. `0x007D2F00` frees the reverb's
buffers and per-channel tap tables and puts back the base vtables; `0x007D31B0` calls it before freeing the object.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007D29C3` |

</details>

### The build reverb

`BuildReverb` runs its own body in slot 3 of its interface¹. `0x007DB650` frees its buffers at `+0x18`,
`+0x28`, `+0x30`, six at `+0x280` and two at `+0x400`, `0x40` bytes apart, and `+0x480`, and puts back the base vtables.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007DB8D0` |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

The shipped `bus ` chunk has one bus with no effects ([Sound engine configuration](sound-engine-config.md)). Every
builder above is called, or has its address loaded, only in the bus builder `0x007AC4F0`¹,
except three that a voice builds for itself:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007AC8F6`-`0x007ACA48` |

</details>

| Builder | Other caller | When |
|---|---|---|
| `0x007D9530` `SimpleFilter` | `0x007EA003` | every voice, as effect 0 |
| `0x007D99E0` `Flanger` | `0x007ED01F` | a sound effect of type 6 |
| `0x007DA0A0` `GranularPitchShift` | `0x007ED1B6` | a music voice whose header is not version 0 and sets bit `0x1` of `+0x0A`, built bypassed (`+0x10` = 1) until `0x007EA850` switches it on; all 116 shipped musics are version 11 with that bit clear |

So the reverbs, the compressor, the side-chain input, the biquad filter, the pitch shifter and the frequency shifter
are not built by the shipped game.

</details>

## State

<details>
<summary>Show the state it keeps</summary>

All are 16-byte vectors of four `f32`, 0 in the file, that the builders fill each time an effect is built and the
run functions only read.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EADF00` | `f32[4]` | 0 | (1, 1, 1, 1): the weight of the vector parked at `[rbp+0x190]` in the first four samples of the pair the reverb stores at `[rsi+0xE0]` and adds into `p` (`0x007D4AFF`-`0x007D4B6D`) | `0x007D2150` (`0x007D29EF`) | `0x007D3CB0` (`0x007D4B06`) |
| `0x02EADF10` | `f32[4]` | 0 | (0, 0, 1, 1): the weight of the vector parked at `[rbp+0x1A0]` in the last four samples, stored at `[rsi+0xF0]`: its last two lanes are kept (`0x007D4B57`-`0x007D4B81`) | `0x007D2150` (`0x007D29F8`) | `0x007D3CB0` (`0x007D4B5E`) |
| `0x02EADF20` | `f32[4]` | 0 | (0, 0, 0, 0): the weight of the vector parked at `[rbp+0x1D0]` in the first four samples, so it drops out (`0x007D4B33`-`0x007D4B53`) | `0x007D2150` (`0x007D2A09`) | `0x007D3CB0` (`0x007D4B3B`) |
| `0x02EADF30` | `f32[4]` | 0 | (1, 1, 0, 0): the weight of the vector parked at `[rbp+0x1E0]` in the last four samples: its first two lanes are kept (`0x007D4B43`-`0x007D4B71`) | `0x007D2150` (`0x007D2A10`) | `0x007D3CB0` (`0x007D4B4B`) |
| `0x02EAE050` | `f32[4]` | 0 | the compressor's zero vector for channels 4-7, as `0x02EAE040` is for channels 0-3: the cap of `(slope - 1) x (d x inGain - threshold)` and the "sum is 0 or less" test (`0x007D8D12`, `0x007D8D30`) | `0x007D85E0` (`0x007D8794`) | `0x007D8BE0` (`0x007D8D12`, `0x007D8D30`) |
| `0x02EAE060` | `f32[4]` | 0 | the compressor's one vector for channels 0-3: the gain 1.0 put in where the sum is 0 or less (`0x007D8D41`) | `0x007D85E0` (`0x007D87A9`) | `0x007D8BE0` (`0x007D8D41`) |
| `0x02EAE070` | `f32[4]` | 0 | the same for channels 4-7 (`0x007D8D4B`) | `0x007D85E0` (`0x007D87A2`) | `0x007D8BE0` (`0x007D8D4B`) |

No other instruction reaches these vectors. The address `0x02EAE040` that `0x007D3CB0` takes at `0x007D4584` and `0x007D5672`
ends a loop over the vectors from `0x02EADF40`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007D4777`-`0x007D47BF` |

</details>

</details>

## Modding notes

- Giving a bus effect records in `sead.win.config` builds these effects on that bus; each record's type byte picks the
  class from the table above.
- A compressor that names a side chain finds it only when that effect has type 4; any other leaves it listening to its
  own input.
- The flanger's delay is capped at 1,023 frames, about 21 ms at 48 kHz.

## Related

- [Sound engine configuration](sound-engine-config.md) - the bus records, effect types and presets.
- [Sound engine](sound-engine.md) - the voice that runs its effects each block, and the voice controls that set them.
- [Interactive music](interactive-music.md) - how music switches its pitch shifter.
