---
title: "Script variables: the six storage classes behind PUSHV and POPV, where each lives and how long it lasts"
kind: "system"
category: "Scripts and script commands"
addresses: "00262440, 00267FC0, 00267E60, 00268100, 0026D530, 002650B0, 00264E30, 0026C8C0, 0026CE60, 0026DB30, 00268320, 0025D8E0, 00269A20, 0032F240, 02099DF0, 02099FF0, 0209AC10"
---

## What the player sees

Whether a chest has been opened, which line a townsperson says next, how far a quest has come:
every such fact a script remembers is a variable. Some are kept inside the save file and follow
the player forever, some live only while the current area's scripts are loaded, and two shared
banks are wiped on an area change or when the player leaves a group of areas. Which of those a
script author chose decides what the game forgets.

## How it works

### The descriptor

A script image carries a table of 8-byte variable records, bound into the manager slot at
`+0x78` by `0026C8C0` from the image header's `+0x28`. The opcodes `PUSHV`, `POPV`, `PUSHDBG` and
`PUSHP` carry a 16-bit variable index, and the resolver `00262440(slot, actor, stack, index,
out)` reads the record's first dword at `table + 4 + index × 8`:

```
bits  0..23  offset into the class's home
bits 24..26  class: 0 global, 1 file, 2 local, 3 msp, 4 scratch1, 5 scratch2, 7 array
bit  27      float: the value is pushed with tag 2 instead of tag 1
bits 28..31  width: 0 u8, 1 s8, 2 u16, 3 s16, 4 s32, 5 f32
```

For classes 0 to 5 the address is the class's base plus the offset. For class 7 the offset
names an array header in the image: the element descriptor at `+0`, the dimension count at `+4`
(u16) and the dimensions from `+8`.

The resolver pops one index per dimension from the value
stack, last dimension first, clamps each into `0 … dim − 1` (a negative index reads element 0, a
large one the last element), multiplies the dimensions out row-major into one flat index, and
then resolves the element descriptor's class as above. The flat index is returned separately and
the caller scales it by the element width.

The resolver fills a `0x30`-byte record for its caller: `+0` the constant 6, `+4` the kind (1 int,
2 float, from bit 27), `+0xA` the variable index, `+0xC` the descriptor, `+0x10` the base address
plus offset, `+0x18` the element descriptor and `+0x1C` the flat index.

### The six homes

| Class | Base pointer in the slot | Set by | What it is |
|---|---|---|---|
| 0 `global` | `+0x48` | the binder `0026C8C0`, from `002EF2B0()` | the save payload: offsets `0` to `0xCF4` of the persistent save image |
| 1 `file` | `+0x40` | `0026CE60`, `image + [image + 0x38]`, when the binder left it null | an area inside the loaded script image |
| 2 `local` | the callback `+0x98` = `00264E30` | the binder | `[slot + 0x50] + [[actor + 0x40] + 0x1C]`: the actor's own slice of the image's `+0x48` region |
| 3 msp | `image + [image + 0x40]` | inline | the image's msp area; no shipped script declares a variable here |
| 4 `scratch1` | `+0x58` = `02099DF0` | the binder | a 512-byte static bank |
| 5 `scratch2` | `+0x60` = `02099FF0` | the binder | a 512-byte static bank that rides the save image |

A class-6 descriptor has no case in either resolver and falls to base 0, the bare offset as an
address; no shipped script declares one.

`PUSHV` (`00267FC0`) loads the element by width (`u8` and `s8` at `base + i`, 16-bit widths at
`base + 2i`, 32-bit at `base + 4i`), zero- or sign-extending, and pushes it with the kind's tag;
the kind byte it stores beside the value is the record's `+0`, 6. `POPV` (`00267E60`) pops the
top by the kind (a float operand to an int variable is truncated with `cvttss2si`, an int to a
float variable converted with `cvtdq2ps`) and stores it through `0026D530`.

`PUSHV` refuses at
stack depth 63 like every other push; `POPV` on an empty stack stores 0 to an int variable
silently and, for a float variable, calls `008620C0` first; a missing array index reads as 0.

### The store saturates by width

`0026D530` clamps before it writes: `u8` into 0 to 255, `s8` into −128 to 127, `u16` into 0 to
65,535, `s32` and `f32` copied as the raw dword, widths 6 and 7 not stored at all. The `s16` arm
clamps into −32,767 to +32,768 and stores the low word, so a script that stores 32,768 reads back
−32,768 and one that stores −32,768 reads back −32,767. A float at or above 2³¹ truncates to
`0x80000000` first, which the `u8` arm then clamps to 0.

### References

`PUSHP` (`00268100`) pushes a reference instead of a value: the element offset plus the flat
index scaled by the width, the class bits kept, and the width nibble forced to 7, tagged int; the
kind byte beside that stack entry is the element's width nibble, so a verb can read the width
from the entry as well.

Width 7 is outside the 0 to 5 every loader accepts, so the reference cannot be read as a value by
mistake. A native verb that takes an out-reference decodes it with `002650B0`, which adds the
24-bit offset to the same six bases (class 2 through the callback, classes 6 and 7 to base 0) and
writes the result there.

### Lifetimes of the two banks

`0026DB30`, run on every field transition, zeroes `scratch1` unconditionally. It then compares
the persistence group word (`+6` of the map-reference row at `[02099D88] + [header + 4] +
field × 8`) of the previous field (`00314870`) with the current one (`003148F0`): when they differ
it zeroes `scratch2` and, unless the payload's `+0x1062` has bit 5, runs `003149E0`; it also
zeroes `scratch2` when the transition options (`003148D0`) have bit 3.

So `scratch2` lives as long
as the player stays inside one group of fields, and `0025D8E0` / `00269A20` copy its 512 bytes
into and out of the save image, so it also survives a save: the copy out runs from the save-image
writer `00229B40` and from `00584580`, the copy back from `00584210` and `005843E0` under the save
controller `00582860`. The boot `00266D10` zeroes both banks, and the teardown `002695A0` (from
`002628B0`) zeroes `scratch1` together with the four party pointers at `0209A1F0` and the sixteen
tagged pointers at `0209A210`.

`00268320` is the other reset: it zeroes `scratch1` always, zeroes `scratch2` only when the load
flag `0209AC10` is 0 and `01E0C3EC` is set, and marks the payload's `+0x1061` when the flag is 0.
The save controller sets the flag to 1 at `00582E98`, the script verb `0x05BF` (start `00355E80`)
clears it through `00287D00`, and the verb `0x05BE` (start `00355940`) reads it through
`00286000`; in the shipped scripts only the Trial Mode
director uses the pair, to skip its entry sequences once after a load.

`global` variables are bytes of the save payload and are saved and loaded with it; `file` and
`local` variables live in the script image and are gone when the area's scripts unload. `POPV`
also looks up a notification id (`0032F240`, tables `022C6D18` and `022C6D28` by slot index) when
the slot index is 1 to 3 and the class is 0, and discards it: nothing is notified on that path.

## Layouts

```
descriptor table  [slot+0x78]: u32 count, then u64 per variable (dword 0 = the descriptor above)
array header      image + offset: u32 element descriptor, u16 dimension count, u16, u32 dim[n]
resolver record   +0 u8 6, +4 u16 kind, +8 u16 actor ordinal, +0xA u16 index, +0xC u32 descriptor, +0x10 u64 base+offset,
                  +0x18 u32 element descriptor, +0x1C u32 flat index, +0x20 u32 value (POPV)
reference (PUSHP) (offset + index*width) | class << 24 | 0x70000000, tag 1
slot pointers     +0 image, +0x40 file, +0x48 global (save payload), +0x50 local region, +0x58 scratch1,
                  +0x60 scratch2, +0x68 int pool, +0x70 float pool, +0x78 descriptors, +0x80 tags, +0x98 local callback
banks             02099DF0 scratch1 (0x200), 02099FF0 scratch2 (0x200)
```

## Shipped data

| Fact | Value |
|---|---|
| descriptors in the 1,114 decoded scripts | 43,466: global 9,448, file 9,995, local 15,766, scratch1 2,292, scratch2 2,343, array 3,622, msp 0 ([script-variables-by-script.tsv](script-variables-by-script.tsv)) |
| save-payload offsets a script declares | 620, `0x0` to `0xCF4`; one offset shared by 575 scripts ([script-variables-global-offsets.tsv](script-variables-global-offsets.tsv), [script-variables-global-by-script.tsv](script-variables-global-by-script.tsv)) |
| global arrays | 34 ([script-variables-global-arrays.tsv](script-variables-global-arrays.tsv)) |
| bank size | 512 bytes each |
| resolver callers | 4: `PUSHV`, `POPV`, `PUSHP`, `PUSHDBG` |

## Operations

Per variable opcode: resolve, then load and push or pop and store. Per field transition:
`0026DB30`. Per save: `0025D8E0` copies `scratch2` out; per load: `00269A20` copies it back and the
controller sets `0209AC10`.

## State

The save payload bytes `0` to `0xCF4`, the script image's file and local areas, and the two banks.

## Modding notes

- A `global` is a save-payload byte; the offsets table says which bytes the shipped scripts
  already use, and the region is written to the save file verbatim.
- `scratch2` survives saves and area changes within a persistence group; `scratch1` dies on any
  area change; `file` and `local` die with the script image.
- An out-of-range array index is clamped, not refused.
- A value stored through an `s16` variable wraps at 32,768, one step beyond the usual range.

## Related

- [Script interpreter](script-interpreter.md): the opcodes and the value stack.
- [Verb dispatch](verb-dispatch.md): how a verb receives a reference.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): the payload the globals live in.
