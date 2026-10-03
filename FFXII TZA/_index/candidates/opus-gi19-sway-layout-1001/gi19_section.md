
## GI-19: the sway section's layout and the chain's objects (OPUS, 2026-10-01)

Static, from the shipping image: a read-only reader pass, byte-checked by OPUS (control `gi19_check.py` in
`_index/candidates/opus-gi19-sway-layout-1001/`).

**Where the record comes from.** The oscillator record is controller 0 of the rig, so it is authored data: a
sub-block of the model's `@FCP` section 2 ([the rig](../../../17-Presentation-Rendering/Character-Render-Records/the-rig-of-seventeen-controllers.md)
§2). The rig's slot initialiser `003E1C50` calls `0040EEA0(rig, S)`, where S is the sway section, rig base plus its
slot-0 offset (`003E1D9A`). `0040EEA0` is a relocation pass. Every offset field is turned into an encoded pointer
relative to S (`0020E600`, `lea ecx, [S + rax]`, `0020E620`), so every relocated target lies inside the sway section.

| record | stride | authored layout (offsets relocated by `0040EEA0`) |
|---|---|---|
| header S | - | `+0x00` → the entry array, `+0x04` u8 entry count |
| entry E | `0x30` | `+0x00` u8 count of A; `+0x03`..`+0x07` u8 counts of C, D, F, G, H; `+0x08` → A; `+0x0C` → C (`0x20`); `+0x10` → D (`0x40`); `+0x14` → F (`0x50`); `+0x18` → G (`0x50`); `+0x1C` → H (`0x60`); `+0x20` f32 blend t; `+0x24` → I (`0x40`), `+0x28` u8 its count |
| A | `0x40` | `+0x03` u8 count of B; `+0x04` → B; `+0x20`, `+0x28`, `+0x2C` → further records |
| B | `0x50` | `+0x00` u16 bone index (`0xFFFF` skips); `+0x04` → optional; `+0x08` → optional record holding two vec4s; `+0x10` vec4 |

Three header fields are **not** authored. `003E1C50` writes them after the relocation:
- S `+0x08` is set to the encoded address of the rig's own slot `+0x78` (`003E1D9F`–`003E1DB5`);
- S `+0x0C` is set to the encoded address of the rig's `+0x7C`, the parent's bone array;
- S `+0x5C` is set to the encoded address of the rig's `+0x70`, the render record.

The rig's `+0x78` holds `encode(00421D20(render record))`, written at `003E1CC3`. `00421D20` resolves the render
record's resource entry (owner `+0x10`, table `+0xD98`, key `+0x18`) and returns that entry's `+0x84`: the skeleton's
`0x290`-stride bone array.

**So the chain's objects are named.**
- The record's `+0x08` resolves to **the rig's own field `+0x78`**, a slot rather than an object. Its `+0x00` is the
  encoded bone array. A rebind can rewrite the slot (`003E3CA0` rewrites `+0x70`..`+0x7C`) without touching the
  authored section.
- The entry's `+0x08` resolves to **the authored A array** (`0x40`-byte records, entry `+0x00` of them).
- Each A's `+0x04` resolves to **the authored B array** (`0x50`-byte link records). Each B record holds its bone index
  at `+0x00`.

`0040DBB0` runs with `r14` = S and `r13` = the entry. Per bone it indexes the bone array with B's index × `0x290`
(`0040DDB5` / `0040DDC5`). The "second 4×4" it loads into VU rows 5–8 is that **bone row's** `+0x150`–`+0x180`.

**Not established here:**
- the names of the authored records beyond A and B (C, D, F, G, H, I, and the targets of A `+0x20`/`+0x28`/`+0x2C`
  and B `+0x04`/`+0x08`), which the heavy stages `0040FF30`, `00411650` and `00413C80` read;
- whether the resource entry that supplies the bones is always the one that carries this rig (likely, not shown);
- `0040EEA0`'s second host `0054A9C0`.
