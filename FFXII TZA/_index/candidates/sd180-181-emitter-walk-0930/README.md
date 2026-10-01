# SD-180 / SD-181: the sound-emitter walk after its shape dispatch, and its base (OPUS, 2026-09-30)

Register rows SD-180 and SD-181 were registered by SWE2-DATA (DD owner read batch 5, `b92561451`) on
[clamping-a-point-into-a-volume.md](../../../06-Movement-And-Navigation/clamping-a-point-into-a-volume.md) Call chain.

This record is static. The checker is `sd180_walk.py` (output `sd180_walk.out`, `FAILS 0`).

**Most of both answers is already on record.**
[the-map-ctrl-pack.md](../../../03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md) §2.3 decodes the records the walk
reads: the SP1 sound-emitter block, map-pack slot 16. There, `+0x38` is the attenuation argument to `00361810`'s
volume math, `+0x54` / `+0x58` are the class-0/1 extents, and `003638B0` starts or refreshes the record's voice. This
record re-checks that reading on the bytes and adds what the walk returns.

## SD-180: what the walk does after the clamp (OPUS)

- **W1: the three floats.** After the shape dispatch, `003631B0` hands the clamped point to `00361810`, together
  with the record's `+0x38` (all classes) and `+0x54` / `+0x58` (classes 0 and 1). The segment-chain class 2 passes 0
  and a constant in their place and adds `00362230`'s own float result.
- **W2: when the running value changes.** Next comes `003638B0(record, …, r9 = the running value)`. Its result
  replaces the running value **only when `00361810` returned exactly 0.0** (`ucomiss xmm6, xmm7` / `jp` / `jne`).
- **W3: what `003638B0` returns.** It returns the record's signed byte `+0x1A` when that byte is ≥ 0, and in that
  case skips the voice start. Otherwise it returns the value it was given.
- **W4: what the walk returns.** The walk returns the running value it started with (its caller's `r9d`). That value
  is replaced by the `+0x1A` byte of each record that meets W2 and W3. The driver `00362850` threads the value through
  two walks (the listener-grid cell's list, then the default list) and dispatches it as
  `002DF410(1, 0xB4, value)`, remembering it at `022CBA80`. That is the map-ctrl page's "dispatch the result via
  `002DF410(1, 0xB4, idx)`".

## SD-181: which shipped file carries the records (OPUS)

- **B1:** `022CBAF0` has three writers:
  - the boot initialiser zeroes it (`00362F70`, from `00266D10`);
  - unload zeroes it (`00363730`, from `00378230`);
  - `003635C0(rcx)` sets it. Its one caller, `003775D0`, passes `[02ADD060]` when bit 7 of the to-bind word
    `02ADD0F0` is set.

  `02ADD060` is **the map pack's slot 16, the `SP1` sound-emitter block** (map-ctrl page's slot table and §2.3). So
  the records come from each area's map-ctrl pack, and 456 shipped packs carry one.

## Limits (OPUS)

- **What `002DF410`'s parameter `0xB4` means to the sound layer is not read.** The walk's result is a small index
  taken from a record's `+0x1A` byte. The map-ctrl page calls `+0x1A` a runtime field; whether shipped records set it,
  and what the `0xB4` channel does with the index, is left open.
- **`00361810`'s float result is not named here.** Its volume math is on the map-ctrl page. This record only uses the
  fact that the walk tests it against exactly 0.0.
