
## GI-15: the per-site helpers read (OPUS, 2026-10-01)

Static, from the shipping image; a read-only reader pass, checked at the bytes by OPUS (control `gi15_check.py` in
`_index/candidates/opus-gi15-helpers-1001/`). One item per "not read" site above.

**`0x34`, the shadow object.** `003AFC10(h)` returns slot `02B3F570 + (h & 0xFF) * 0x70` when the slot's `+4` equals
`h`, else null. Arms `0x01`, `0x02`, `0x04`, `0x20` and `0x40` are linear ramps, each a count byte, a value and a rate:

| arm | count | value | rate |
|---|---|---|---|
| `0x01` | `+0x1C` | `+0x24` | `+0x2C` |
| `0x02` | `+0x1D` | `+0x28` | `+0x30` |
| `0x04` | `+0x1E` | `+0x34` | `+0x38` |
| `0x20` | `+0x54` | `+0x3C` | `+0x48` |
| `0x40` | `+0x55` | `+0x44` | `+0x4C` |

With `n = byte+3`, the float `dword[cmd + 4]` is always used. When `n <= 1` the value takes it at once and the count
becomes 0. Otherwise `rate = (float - value) / n` and `count = n`. `0x08` sets `+0x1F`'s low nibble to 2 (`byte+3`
non-zero) or 1. `0x10` sets its high nibble to `0x20` or `0x10`. The `0x80` arm switches on `byte+3`:
- 1: `+0x40 = float`;
- 2: `+0x58 |= 2` and word `+0x56` = `0x40`, `0x80` or `0x100` for a float up to 1.5, up to 2.5, or above;
- 4: `+0x58 |= 1` and `+0x50 = float`;
- other values: nothing.

The ramps are stepped by the tick `003AF460` / `003AFB30`
([CONTRACT-authored-command-ramp-channels.md](../../../17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md)). The allocator `003AF340`
sets `+0x1F = 0x11` and the three first values to 1.0. Across the pool `02B3F550`-`02B40370`, no function other than
the tick and the two resets reads these fields. **In static code the pool is write-only**, as `02B3F554` already is,
so what the values do on screen is not established here.

**`0x3F` / `0x48`, `00372800` and key 29.** `00372800` returns -1 unless the resource's `@FTR` entry is of kind 2
(`+0x9C`); otherwise it tail-jumps to `003737C0`. That search returns the first record whose key (`00409250`: word
`+8` when flags bit 30 is set, else link bits 0-11) equals the argument **and whose flags bit 8 is set**; otherwise it
returns `0xFFFF`. The block's `+0x14` is the **bone** the sway hangs on. `00520E90` hands it to `0040ABF0`, which
stores it at oscillator `+0x3C`, and the heavy stage `0040FF30` reads that bone's `0x290`-stride record, and its `+0x284` matrix handle, from `+0x3C`. `+0x16` is the
**preset**: `0040ABF0` stores it at `+0x3E`, and preset 0 skips the set-up. So name key 29 names a skeleton bone of
each model; which bone is per-model data. The corrected field sources:

| | `0x3F` (`00520510`) | `0x48` (`005205B0`) |
|---|---|---|
| `+0x14` bone | `word[cmd + 2]`, used directly (0 in every shipped command) | `00372800(resource, low word of dword[cmd + 0x10])` |
| `+0x16` preset | `word[cmd + 0x10] & 0xFFF` (4, 5 or 6 as authored) | `word[cmd + 2] & 0xFFF` (0 in 5,167 of 5,771) |
| `+0x18` flag | `word[cmd + 0x10] >> 15` | `word[cmd + 2] >> 15` |
| preset zeroed | when `word[cmd + 2]` is `0xFFFF` | when the lookup returns `0xFFFF` |

In both commands "no bone" forces preset 0, which leaves the sway off.

**`00423790`.** This is the reaction-eligibility predicate (`004274E4` is its one call). A non-zero third argument
(`word[rec + 0x3B4]`) whose kind nibble is 0 refuses. No pending record admits. Both ids are then normalised and
kind-tested. The result compares their priorities, `prio[arg & 0xFFF] <= prio[candidate & 0xFFF]`, in the byte map
**`01F00410`**. For `0x203D`, `prio` is 3.

**`004219C0`, the key, `00372760` and `0046E590`.** `004219C0(parent, key, child)` mirrors `004218A0`:
- `key == -1` sets `+0x284` bit 26 and `+0x2F2 = 1`.
- Otherwise `00372800(parent resource, key)` runs, retried once with key `0x1E`, and the bind aborts if both miss.
- It then binds through `0046E640`, the twin of `0046E590` that calls `00370390` instead of `00370180`.

The key is a bone: a C-string bone name for `004218A0` (compared by `00372760`) and a numeric `@FTR` key for
`004219C0`. `004215A0` passes no key for attach code `0x7FFF`, and a looked-up key for the others. `00372760` reads
the kind-0 layout (names at `+0x30`, stride `0x4C`) without testing `+0x9C`. Whether its by-name path ever matches on
the shipped kind-2 `@FTR` data is not established.

**`word[+0x2F2]`, `00373060` and `005048A0`.** `+0x2F2` is a 0/1 flag, set to 1 only by the no-key path of the two
binders. That path is attach code `0x7FFF`, the whole-skeleton bind. The bind still runs then, with bone -1.
`00373060` and `005048A0` are read whole on
[ftr-node-table.md](../../../17-Presentation-Rendering/Model-And-Motion-Formats/ftr-node-table.md) and
[fdm-and-for-entries.md](../../../17-Presentation-Rendering/Model-And-Motion-Formats/fdm-and-for-entries.md).

**`0x2A`, the pool, its gate and its table.** The pool is the camera-shake source pool of
[the-element-types-40-42-a0-ab-d0-d1.md](../../../17-Presentation-Rendering/Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md) (`0x42`). So the
command's three floats are its intensity, time rate and radius scale.
- `003D8300` checks the handle, decrements the live count `02B4D7A0`, clears `+4` and unlinks the slot.
- The gate `02B4D7A2` refuses kind-2 requests in `003D7FF0`. It is set by `003D8D60` (thunk `002EA880`) from the
  script verb `0x4A0` (`deny_char_camerashake`, handler `003517C0`), and cleared by the area unload `002628B0` and
  by init `003D8C30`.
- `003D8C30` fills `02B4E3D0` with four `.data` blocks, `01EFE3A0` / `01EFE520` / `01EFE6A0` / `01EFE820`. They are
  byte-identical: radius 25.0, duration 22.0. The kind-2 path clamps its index to 3 and uses block `+0x80` as the
  shake group.

**`0x16`, the sub-resource variant.** The variant is an `@FCT` palette binding
([fte-fct-texture-colour-tables.md](../../../17-Presentation-Rendering/Model-And-Motion-Formats/fte-fct-texture-colour-tables.md), `00504D30`).
`003E7210`'s table is the FCP block's section 5 (the word at `[record + 0x400] + 0x0A`). Each listed record takes the
palette resource id at its `+4`. The five authored indices are palette records of the 7 models whose FCP carries
section 5. Which palette each one is, is content.

**`0x09`, the tail.** `0041B650`, `00409190` and `003AB7F0` are read on
[fef-and-motion-entries.md](../../../17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md) and
[resource-section-addressing.md](../../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md). Past the loop,
`0041BEE0` sets the binding record:
- `+0x14 = 0`;
- `+0x16` = the `@FMN` entry's duration `word[+0x50]`;
- `+0x18` = the same, or 0 when the caller's byte `+0x96` bit 6 is set;
- `+0x1C = (duration - [01DFE0BC]) / duration`, or 0 for a zero duration.

It then calls `0041C260`. A resource index of -1 skips straight to that call.

**Ids 4 and 6.** `00325090` (id 6) never reads the command. For a unit with `+0x698` (and field bit 15 when the unit
is KO, Stone or X-Zone), it calls `00319E40`, which hands the target buffer's ids and the current action-stage handle
to `002EAD00`. Id 4's `00325260` maps the subtype (tables `0032574C` / `00325720`) to an arm:

| subtype | arm |
|---|---|
| 0 | `003191B0` per matching target |
| 2, 6 | the effect handle through `002EACD0`, `0026A430`, `0033CB10` |
| 3 | `003257D0(1)` |
| 4 | `002EB4A0`, then `+0x690 \|= 2` |
| 5 | `002FD0C0(handle, byte+3)` |
| 9 | unit `\|= 0x80000` |
| 7, 8 | nothing (`return 1`) |
| `0x80`-`0x83` (from 1) | `003257D0` with classes 2, 3 then `0xA`, 4, 5 |

`003257D0(class)` emits the reaction (`003176E0`) of every target entry whose code equals the class. The classes are
the evade / parry codes of the formula scratch block's §2.6. Subtype 1 therefore shows every evade and parry
reaction, and 3 the band-C evades.

**Not established here:** what the shadow pool's values do on screen; which bone key 29 or `0x1E` is in each model;
what subtypes 2/6, 4, 5 and 9 look like, and why 7 and 8 are authored at all; which palettes the 7 section-5 models
carry; whether `004218A0`'s by-name lookup matches on kind-2 data. All are content or live questions, not code.
