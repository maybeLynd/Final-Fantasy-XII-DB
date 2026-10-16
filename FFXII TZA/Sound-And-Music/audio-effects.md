---
title: "Audio effects: the filters, reverbs, compressor, flanger, pitch shifter and frequency shifter the sound driver can run on a voice or a bus"
kind: "system"
category: "Sound and music"
addresses: "007D1500, 007D1C80, 007D9770, 007D9C60, 007DA2E0, 007DACF0, 007D8BE0, 007D3CB0"
---

## What the player sees

- Every sound passes through a low-pass filter that can muffle it.
- A music voice can carry a pitch shifter that changes the pitch without changing the speed; no shipped music
  asks for one.
- The final mix has no reverb, compressor or equaliser: the shipped configuration gives the one master bus no effects.

## How it works

### The effect classes

An effect is a `SQEX::Sd::Driver` object with two vtables: its own, and the `ICoreEffect` interface at `+08`<sub>h</sub>.
Slot 1 of its own vtable returns its type, the number a bus record names ([Sound engine configuration](sound-engine-config.md)):

| Type | Class | Vtable | Built by | Block body |
|---:|---|---|---|---|
| 0 | `EmptyEffect` | | `007AC4F0` itself, `18`<sub>h</sub> bytes | |
| 1 | `SurroundReverb` | `01CB7528` | `007D2150` | `007D3CB0` |
| 2 | `Compressor` | `01CB7710` | `007D85E0` | `007D8BE0` |
| 3 | `Filter` | `01CB7078` | `007D0AC0` | `007D1500` |
| 4 | `SideChainInput` | `01CB7698` | `007D80E0` | `007D82E0` |
| 5 | `SimpleFilter` | `01CB77A8` | `007D9530` | `007D9770` |
| 6 | `Flanger` | `01CB7828` | `007D99E0` | `007D9C60` |
| 7 | `GranularPitchShift` | `01CB78A8` | `007DA0A0` | `007DA2E0` |
| 8 | `HilbertFilter` | `01CB7920` | `007DAAB0` | `007DACF0` |
| 10 | `BuildReverb` | `01CB7998` | `007DAFF0` | `007DB8D0` |

The type slots are `007BD590` (1), `007E3260` (2), `007D14C0` (3), `007D82A0` (4), `007D9730` (5), `007D9C20` (6),
`007DA2A0` (7), `007DACB0` (8) and `007DB8C0` (10). Byte `+10`<sub>h</sub> is a bypass flag that interface slot 1 `007ACD20` reads.

### Running an effect

Slot 3 of the interface runs the effect on one block. It passes the buffer as both input and output, so every effect
works in place, with the frame count at `+08`<sub>h</sub> and the channel count at `+0C`<sub>h</sub> of its argument (`007D14D0`,
`007DACC0`). Each thunk hands its body the effect's state block: `007D14D0` (Filter), `007D3C90` (SurroundReverb),
`007D8BB0` (Compressor), `007D82B0` (SideChainInput), `007D9740` (SimpleFilter), `007D9C30` (Flanger), `007DA2B0`
(GranularPitchShift) and `007DACC0` (HilbertFilter).

The bodies of the filter, the one-pole filter, the flanger, the compressor and the reverb work on eight interleaved
floats per frame, one per output channel; the pitch shifter and the frequency shifter loop over the given channel count.

Other slots of an effect's own vtable, where they were read:

| Slot | Does | Read in |
|---:|---|---|
| `2` | sets a parameter by id, with a ramp time | `007D1840` (Filter), `007D8E40` (Compressor) |
| `3` | reads a parameter back | `007DA1C0` (`600`<sub>h</sub>, `601`<sub>h</sub>), `007DAC30` (`700`<sub>h</sub>) |
| `5` | advances the parameter ramps and recomputes when one moved | `007D1A10` (Filter), `007DA970` (GranularPitchShift) |
| `6` | re-applies the four filter parameters; a null argument returns -1 | `007D1970` (Filter) |
| `8` | recomputes the coefficients from the current ramp values | `007D1C80`, `007D9200`, `007D98F0`, `007D9EA0`, `007DAA00`, `007DAF70` |

### Sine and cosine

`007B8C80` (sine) and `007B8BA0` (cosine) are the polynomial approximations every effect uses. Both reduce the angle
to -pi..pi by rounding `x / 2pi` (`0.15915494` at `00D22590`), fold it into -pi/2..pi/2, and evaluate:

```python
y2 = y * y
sin = y * (1 + y2*(-0.16666667 + y2*(0.008333331 + y2*(-0.00019840874 + y2*(0.0000027525562 - y2*0.000000023889859)))))
cos = s * (1 + y2*(-0.5 + y2*(0.041666638 + y2*(-0.0013888378 + y2*(0.000024760495 - y2*0.00000026051615)))))
```

`s` is -1 when the cosine's fold crossed pi/2 and 1 otherwise; the constants sit at `01CB5194`-`01CB51B0`,
`009159F4` and `01CEBB70`.

### The filter

`Filter` is a biquad, run by `007D1500` in direct form 1 on each of the eight channels, with its coefficients at
`+D0`<sub>h</sub> and its histories after them:

```python
y = b0*x + b1*x1 + b2*x2 - a1*y1 - a2*y2
```

`007D1840` takes four parameters. `200`<sub>h</sub> ramps the frequency, with curve 5 when it falls and 4 when it rises; `201`<sub>h</sub>
ramps the reciprocal of Q, a value of 0 counting as 1; `202`<sub>h</sub> ramps the gain; `203`<sub>h</sub> changes the shape. With a time above 0,
`007D16C0` ramps the old shape towards a neutral setting over half the time, and `007D1A10` then switches the shape and
ramps from neutral to the stored values. A time of 0 recomputes at once.

`007D0AC0` builds it as shape 1 at 2,000 Hz, 1/Q 1.414 and gain 1.0, with pass-through coefficients, and stores
`1 / device rate` at `01F41D18`. `007D1C80` turns the frequency into `w = f * 2pi * [01F41D18]` and fills the five
coefficients by shape:

| Shape | Kind | Coefficients |
|---:|---|---|
| `0` | pass | `b0` 1, the rest 0 |
| `1` | low-pass | `007D1080` |
| `2` | high-pass | `007D0EA0` |
| `3` | band-pass | `007D0DD0` |
| `4` | notch | `007D1280` |
| `5` | low shelf | `007D1140`, using the gain |
| `6` | high shelf | `007D0F60`, using the gain |
| `7` | peaking | `007D1330`, using the gain |
| `8` | all-pass | `007D0D30` |

Each coefficient function stores `a1, a2, b0, b1, b2` in that order, from `alpha = sin(w) * 0.5 * (1/Q)`. All but the
all-pass divide by `(1 + alpha) / 0.9999`, so their poles sit just inside the unit circle:

| Function | `b0` | `b1` | `b2` | `a1` | `a2` |
|---|---|---|---|---|---|
| `007D1080` | `(1 - cos w) / 2` | `1 - cos w` | `(1 - cos w) / 2` | `-2 cos w` | `1 - alpha` |
| `007D0EA0` | `(1 + cos w) / 2` | `-(1 + cos w)` | `(1 + cos w) / 2` | `-2 cos w` | `1 - alpha` |
| `007D0DD0` | `alpha` | 0 | `-alpha` | `-2 cos w` | `1 - alpha` |
| `007D1280` | 1 | `-2 cos w` | 1 | `-2 cos w` | `1 - alpha` |
| `007D1330` | `1 + alpha * A` | `-2 cos w` | `1 - alpha * A` | `-2 cos w` | `1 - alpha / A` |
| `007D0D30` | `1 - alpha` | `-2 cos w` | `1 + alpha` | `-2 cos w` | `1 - alpha` |

`A` is the gain; the peaking filter divides by `1 + alpha / A` instead. The shelves `007D1140` and `007D0F60` use the
same `A` with `2 * sqrt(A) * alpha`. The bodies receive `w` and the ramped values from `007D1C80`.

### The one-pole filter

`SimpleFilter` is the low-pass every voice carries as effect 0 ([Sound engine](sound-engine.md)). `007D9770` runs it on
each of the eight channels:

```python
y = b * x + a * y1
```

`007D98F0` sets `a` (`+50`<sub>h</sub>) and `b` (`+54`<sub>h</sub>) from the frequency ramp and the mode `+48`<sub>h</sub>, with `w = f * 2pi *
[01F41D20]`:

| Mode | `a` | `b` |
|---:|---|---|
| `0` | 0 | 1 |
| `1` | `exp(-w)` | `1 - a` |
| `2` | `exp(w - pi)` | `1 - a` |

`007D9530` builds it in mode 0 at 2,000 Hz. It stores `1 / device rate` at `01F41D20`, half the rate at `01F41D24`,
that half divided by 2,400 at `01F41D28`, and minus the base-10 logarithm of their ratio at `01F41D2C`. `007D9600`
puts back the base vtables of the voice's embedded filter when the voice is torn down (`007EA32E`).

### The flanger

`Flanger` mixes each frame with a copy read from a 2,048-frame eight-channel ring (`+130`<sub>h</sub>, write index `+10130`<sub>h</sub>).
`007D9C60` reads the copy at:

```python
read = write - delay + sin(phase) * depth          ; wrapped into 0..2047
out  = dry * x + wet * ring[read]
phase += step                                       ; 5.1415925 is subtracted once it passes pi
```

The subtracted constant at `01CB7898` is not 2pi, so the sweep is not a whole sine (`007D9D6D`-`007D9D78`).
`007D9EA0` fills the values from five ramps:

| Value | From | Note |
|---|---|---|
| delay `+110`<sub>h</sub> | ramp 1 | whole frames, at most 1,023 |
| depth `+124`<sub>h</sub> | ramp 2 | times the delay |
| step `+120`<sub>h</sub> | ramp 3 | `rate * 2pi / device rate` |
| dry `+114`<sub>h</sub> | ramp 4 | built at 1.0 |
| wet `+118`<sub>h</sub> | ramp 5 | |

### The pitch shifter

`GranularPitchShift` changes pitch with two read heads moving through a 14,400-frame ring (`+98`<sub>h</sub>, write index
`+70898`<sub>h</sub>). `007DA2E0` advances a grain clock by its step each frame and wraps it at 1:

1. When the clock passes 0.25 the first head restarts, and at 0.75 the second: its delay starts at `(pitch - 1)`
   grain lengths when the pitch is above 1, and at 0 otherwise.
2. Each frame each head's delay grows by `1 - pitch` frames, so a pitch below 1 falls behind the input.
3. Each head reads its delay with linear interpolation, and the output is `w * head2 + (1 - w) * head1`, with
   `w = (sin(2pi * clock) + 1) / 2`.

`007DAA00` takes the pitch (parameter `600`<sub>h</sub>, built at 1.0) into `+78`<sub>h</sub> and the grain rate (`601`<sub>h</sub>, built at
10.0) as rate over the device rate into `+7C`<sub>h</sub>; `007DA1C0` reads either back. A music voice gets one
([Interactive music](interactive-music.md)).

`007EA850(voice, on)` switches a voice's shifter: it looks for an effect of type 7 among effects 1 onward
(`+108`<sub>h</sub>, count `+74`<sub>h</sub>) and works on effect 1. When switching on a bypassed shifter it first sets `600`<sub>h</sub> to 1.0,
and it then stores the opposite of `on` in the bypass flag. It returns -1 for an ended voice or when no effect matches.

### The frequency shifter

`HilbertFilter` shifts every frequency by a fixed number of hertz. `007DACF0` runs an eight-tap Hilbert filter on
each channel's history and mixes it with the input four frames back:

```python
h   = -0.2122*x[n-1] - 0.6366*x[n-3] + 0.6366*x[n-5] + 0.2122*x[n-7]
out = cos(phase) * x[n-4] - sin(phase) * h
phase += 2pi * f / device rate                 ; wrapped at 2pi
```

The taps are `+-2/pi` and `+-2/(3pi)`, which `007DAAB0` stores at `+58`<sub>h</sub>-`+70`<sub>h</sub>. The shift `f` is parameter
`700`<sub>h</sub>, built at 1 Hz; `007DAF70` turns it into the step `+4C`<sub>h</sub>, and `007DAC30` reads it back.

### The compressor

`Compressor` (`007D85E0`) takes eight parameters through `007D8E40`:

| Id | Value | Stored as |
|---|---|---|
| `100`<sub>h</sub> | threshold in dB, built at -6 | `10^(dB/20)`, by `exp(x * 0.115129255)` |
| `101`<sub>h</sub> | slope | as given |
| `102`<sub>h</sub>, `103`<sub>h</sub> | input and output gain in dB | `10^(dB/20)` |
| `104`<sub>h</sub>, `105`<sub>h</sub> | attack and release in ms | seconds |
| `106`<sub>h</sub>, `107`<sub>h</sub> | the bus and the effect index of a side-chain input | whole numbers |

`007D9200` turns them into its block: threshold `+148`<sub>h</sub>, slope `+14C`<sub>h</sub>, gains `+150`<sub>h</sub> and `+154`<sub>h</sub>, attack
`exp(-2 / (attack * rate))` at `+158`<sub>h</sub> and release `exp(-1 / (release * rate))` at `+15C`<sub>h</sub>. The rate `+138`<sub>h</sub> is
the builder's argument. It looks the side chain up (`007AC3E0`) and keeps it at `+168`<sub>h</sub> only when its type is 4.

`007D8BE0` works on each channel with an eight-value gain state, built at 1.0:

```python
d = |side-chain sample|, or |x| without a side chain
g = (d + min((slope - 1) * (d * inGain - threshold), 0)) / d     ; 1.0 when the sum is 0 or less
state = g + (g < state ? attack : release) * (state - g)
out = x * outGain * state                                          ; times inGain without a side chain
```

The zero and one vectors it compares with live at `02EAE040`-`02EAE07F`, which the builder fills (`007D8794`-`007D87A9`).
`007D8210` gives a side-chain input's buffer, and `007D89A0` puts back the base vtables and frees the gain state.

### The side-chain input

`SideChainInput` is a pass-through effect that keeps a copy for a compressor to listen to. `007D82E0` copies the
block into its buffer (`+48`<sub>h</sub>, sized by `007AECD0` at build) and to the output, then scales every sample in the
buffer by `+54`<sub>h</sub> and adds `+58`<sub>h</sub>.

### The surround reverb

`SurroundReverb` keeps its state block at `+7D0`<sub>h</sub>, and `007D3CB0` runs it once per frame:

1. It writes the input frame into a 24,000-frame eight-channel history (`+10`<sub>h</sub> of the block; wrap at `007D5682`).
2. For each output channel (count `+0C`<sub>h</sub>), it sums 19 taps of that history, each with its own delay and gain. The
   byte table `01CB73E0` picks one of two delay sets per channel (`007D482F`).
3. It reads 16 delay lines, damps each with a one-pole filter, and mixes them with a 16-point Hadamard transform after
   scaling each line (`007D3B80`, called at `007D4D98`).
4. It writes the mixed lines back, each with a share of the new signal scaled by `0.125` (`00D90640`) and a per-line
   gain.
5. It runs the output through three filter stages, `007D3200` twice and `007D33B0` (`007D54A7`-`007D54EF`).
6. It moves every line's position on, wrapping each at its length, and moves on four further rings.

The rings are 16,384, 1,024, 2,048 and 2,048 frames long, the last three read 367, 512 and 1,179 frames back
(`007D55A3`-`007D563E`). `007D33B0` is one frame of an eight-channel direct-form-1 biquad; `007D3200` is the same
frame with both feedback terms taken from the input history (`y = b0*x + (b1 - a1)*x1 + (b2 - a2)*x2`). With their
flags set, both flush tiny values by adding and subtracting 1.0.

`007D6CD0` recomputes the reverb's ten equaliser biquads, `A0`<sub>h</sub> bytes apart from `+BF0`<sub>h</sub>, from parameter ramps
`30`<sub>h</sub> bytes apart from `+230`<sub>h</sub>. They are a high-pass, three peaking filters and a low-pass, then a low shelf, three
peaking filters and a high shelf (`007D0EA0`, `007D1330`, `007D1080`, `007D1140`, `007D0F60`). The builder calls it
(`007D2DE1`), as do slots 5 and 6.

`007D1EE0` zeroes the filter histories of the block the builder hands it (`007D29C3`). `007D2F00` frees the reverb's
buffers and per-channel tap tables and puts back the base vtables; `007D31B0` calls it before freeing the object.

### The build reverb

`BuildReverb` runs its own body in slot 3 of its interface (`007DB8D0`). `007DB650` frees its buffers at `+18`<sub>h</sub>,
`+28`<sub>h</sub>, `+30`<sub>h</sub>, six at `+280`<sub>h</sub> and two at `+400`<sub>h</sub>, `40`<sub>h</sub> bytes apart, and `+480`<sub>h</sub>, and puts back the base vtables.

## Shipped data

The shipped `bus ` chunk has one bus with no effects ([Sound engine configuration](sound-engine-config.md)). A raw
scan of the code section for calls and address loads of every builder above finds them only in the bus builder `007AC4F0` (`007AC8F6`-`007ACA48`),
except three that a voice builds for itself:

| Builder | Other caller | When |
|---|---|---|
| `007D9530` `SimpleFilter` | `007EA003` | every voice, as effect 0 |
| `007D99E0` `Flanger` | `007ED01F` | a sound effect of type 6 |
| `007DA0A0` `GranularPitchShift` | `007ED1B6` | a music voice whose header is not version 0 and sets bit 0 of `+0A`<sub>h</sub>, built bypassed (`+10`<sub>h</sub> = 1) until `007EA850` switches it on; all 116 shipped musics are version 11 with that bit clear |

So the reverbs, the compressor, the side-chain input, the biquad filter, the pitch shifter and the frequency shifter
are not built by the shipped game.

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
