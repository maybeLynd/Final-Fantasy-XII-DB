# SD-23: the two limits closed. Slot 39 decides whether a sound finishes when its last child ends; `007F0820` is `DynamicSound`'s (OPUS, 2026-09-30)

Register row SD-23 asks what the `Sound` family's capability slots 38 (`+0x130`) and 39 (`+0x138`) mean to their
callers. It sits on [sound-variant-selection.md](../../../18-Audio/Sound-Selection/sound-variant-selection.md), §2.

**Where it stood.** The earlier record [`sd23-sound-slots-38-39-0930`](../sd23-sound-slots-38-39-0930/README.md)
(`acb04148d`) read what each class answers and what the twelve boolean `+0x130` callers and the one Sound-family
`+0x138` caller do with the answer. It left two limits:

- what state 7 of the tick `007BF0A0` is;
- which class `007F0820` is. It calls a float-returning slot 38.

This record is static, from the certified image. The checker is `sd23b_check.py` (output `sd23b_check.out`,
`FAILS 0`).

## The answer (OPUS)

**State 7 is the terminal state (S1–S3).**

- **S1.** The tick `007BF0A0` skips a sound in state 0, 1 or 7.
- **S2.** Each tick it first drops dead children from the list at `+0x400` (count `+0x4C`). Then, when the sound is
  outside states 2–4 and has no child left:
  - state 6 (stopping) always becomes 7;
  - any other state becomes 7 only when slot 39 answers true.
- **S3.** The only other writer of state 7 is the start step `007BD120`, on a start that completes at once
  (`007BD13F`) or fails (`007BD16D`, returning −1). Nothing in the audio range compares the state with 7, except the
  tick's own skip.

**So slot 39 answers "does this sound finish when its last child ends".** Every class says yes except `CycleSound`.
Its false answer keeps a cycle sound alive with no children, outside the stop path. Slot 38, from the earlier record,
answers "does this sound delegate to a chosen child instead of playing a record of its own", which only
`VariationSound` does.

**`007F0820` is `SQEX::Sd::Lay::DynamicSound`'s (D1).**

- Its one caller, `007F1670`, is slot 10 of the vtable RTTI names `SQEX::Sd::Lay::DynamicSound`.
- In that class, slot 38 is `movss xmm0, [rcx + 0xE8]`, a float field, and slot 37 is the float `+0xE4`. That is why
  its `+0x130` calls compare floats: they are another hierarchy's slot 38, not the `Sound` family's capability.
- Its slot 39 is the shared `mov al, 1`.

## Limits (OPUS)

- **Static.** What the `DynamicSound` floats at `+0xE4` / `+0xE8` hold is not read here. `007F0820` compares
  `+0xE8` against a computed length (`sqrtps` at `007F0A17`). That fits [the spatial-audio page](../../../18-Audio/the-spatial-audio-object-model.md)'s
  reading of `DynamicSound` as distance-evaluated and gated on an audible range, but which field is the range is not
  claimed here.
- **Shipped data.** The earlier record's limit stands: no `CycleSound` is built from shipped data (§12), so its false
  slot-39 answer has no shipped effect.
