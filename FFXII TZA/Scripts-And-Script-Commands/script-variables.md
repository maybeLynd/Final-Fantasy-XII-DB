---
title: "Script variables: the six storage classes behind PUSHV and POPV, where each lives and how long it lasts"
kind: "system"
category: "Scripts and script commands"
addresses: "0x00262440, 0x00267FC0, 0x00267E60, 0x00268100, 0x0026D530, 0x002650B0, 0x00264E30, 0x0026C8C0, 0x0026CE60, 0x0026DB30, 0x00268320, 0x0025D8E0, 0x00269A20, 0x0032F240, 0x02099DF0, 0x02099FF0, 0x0209AC10"
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
`+0x78` by `0x0026C8C0` from the image header's `+0x28`. The opcodes `PUSHV`, `POPV`, `PUSHDBG` and
`PUSHP` carry a 16-bit variable index, and the resolver `0x00262440(slot, actor, stack, index,
out)` reads the record's first dword at `table + 4 + index × 8`:

```
mask 0x00FFFFFF  offset into the class's home
mask 0x07000000  class: 0 global, 1 file, 2 local, 3 msp, 4 scratch1, 5 scratch2, 7 array
bit  0x08000000  float: the value is pushed with tag 2 instead of tag 1
mask 0xF0000000  width: 0 u8, 1 s8, 2 u16, 3 s16, 4 s32, 5 f32
```

For classes 0 to 5 the address is the class's base plus the offset. For class 7 the offset
names an array header in the image: the element descriptor at `+0`, the dimension count at `+4`
(u16) and the dimensions from `+8`.

The resolver pops one index per dimension from the value
stack, last dimension `d[n − 1]` first, and folds them row-major with `stride = 1`, then for
`k = n − 1 … 0`: `i = min(max(pop(), 0), d[k] − 1); flat += i × stride; stride ×= d[k]`
(`0x002624D2`-`0x00262537`), so a negative index reads element 0 and a large one the last element.
An empty stack gives the index 0 (`0x002624D8`), and an entry whose tag is neither 1 nor 2 calls `0x008620C0` and
gives 0 as well (`0x002624F3`-`0x002624FB`).

It then resolves the element descriptor's class as above; an element class of 6 or 7 has no case and falls to
base 0, the bare offset as an address (`0x00262552`-`0x00262555`). The flat index is returned separately and
the caller scales it by the element width.

The resolver fills a `0x30`-byte record for its caller: `+0` the constant 6, `+4` the kind (1 int,
2 float, from bit `0x8000000` of the element descriptor), `+8` the actor's `u16` at `+0` (`0x00262676`-`0x0026267A`),
`+0xA` the variable index, `+0xC` the descriptor, `+0x10` the base address
plus offset, `+0x18` the element descriptor (the descriptor itself for classes 0 to 6) and `+0x1C` the flat index.
It returns the element's class in `eax` (`0x00262665`), which `POPV` tests.

### The six homes

| Class | Base pointer in the slot | Set by | What it is |
|---|---|---|---|
| 0 `global` | `+0x48` | the binder `0x0026C8C0`, from `0x002EF2B0()` | the save payload: offsets `0` to `0xCF4` of the persistent save image |
| 1 `file` | `+0x40` | `0x0026CE60`, `image + [image + 0x38]`, when the binder left it null | an area inside the loaded script image |
| 2 `local` | the callback `+0x98` = `0x00264E30` | the binder | `[slot + 0x50] + [[actor + 0x40] + 0x1C]`: the actor's own slice of the image's `+0x48` region |
| 3 msp | `image + [image + 0x40]` | inline | the image's msp area; no shipped script declares a variable here |
| 4 `scratch1` | `+0x58` = `0x02099DF0` | the binder | a 512-byte static bank |
| 5 `scratch2` | `+0x60` = `0x02099FF0` | the binder | a 512-byte static bank that rides the save image |

A class-6 descriptor has no case in either resolver and falls to base 0, the bare offset as an
address; no shipped script declares one.

`PUSHV` (`0x00267FC0`) loads the element by width (`u8` and `s8` at `base + i`, 16-bit widths at
`base + 2i`, 32-bit at `base + 4i`), zero- or sign-extending, and pushes it with the kind's tag;
the kind byte it stores beside the value is the record's `+0`, 6. A width nibble above 5 has no load case
(`0x00267FE4`-`0x00267FE7`): `PUSHV` loads nothing and pushes whatever its stack frame holds in the value dword.

`POPV` (`0x00267E60`) pops the
top by the kind (a float operand to an int variable is truncated with `cvttss2si`, an int to a
float variable converted with `cvtdq2ps`) and stores it through `0x0026D530`. It pops the value after the
resolver has popped any array indices (`0x00267E7F`), so a script pushes the value first and the indices on top.

`PUSHV` refuses at
stack depth 63 like every other push; `POPV` on an empty stack stores 0 to an int variable
silently and, for a float variable, calls `0x008620C0` first; a missing array index reads as 0.
A top entry whose tag is neither 1 nor 2 is the other way round: an int variable gets 0 after `0x008620C0`
(`0x00267F0E`-`0x00267F13`), a float variable 0.0 silently (`0x00267EB6`, `0x00267EE7`).

### The store saturates by width

`0x0026D530` clamps before it writes: `u8` into 0 to 255, `s8` into −128 to 127, `u16` into 0 to
65,535, `s32` and `f32` copied as the raw dword, widths 6 to 15 not stored at all (`0x0026D542`-`0x0026D545`).
The `s16` arm clamps into −32,767 to +32,768 and stores the low word, so a script that stores 32,768 reads back
−32,768 and one that stores −32,768 reads back −32,767. A float at or above 2³¹ truncates to
`0x80000000` first, which the `u8` arm then clamps to 0.

### References

`PUSHP` (`0x00268100`) pushes a reference instead of a value: the element offset plus the flat
index scaled by the width (2 for widths 2 and 3, 4 for 4 and 5, 1 for any other, `0x00268124`-`0x00268146`), the
class bits kept, the float bit `0x8000000` dropped and the width nibble forced to 7 (`0x00268155`-`0x0026816C`),
tagged int; the kind byte beside that stack entry is the element's width nibble, so a verb can read the width
from the entry as well. At stack depth 63 it pushes nothing (`0x00268173`).

Width 7 is outside the 0 to 5 every loader accepts, so the reference cannot be read as a value by
mistake. A native verb that takes an out-reference decodes it with `0x002650B0`, which adds the
24-bit offset to the same six bases (class 2 through the callback, classes 6 and 7 to base 0) and
writes the result there.

### Lifetimes of the two banks

`0x0026DB30`, run on every field transition, first clears the dword `0x02099D44` (`0x0026DB3C`), runs the
field-transition reset `0x003590E0`, zeroes the four party pointers at `0x0209A1F0` (`0x0026DB52`, `0x0026DB5A`), sets
camera record 0's mode to 2 (`0x0025A500(0, 2)`, `0x0026DB62`), clears the menu request at `0x0215F1A0` (`0x002E15D0`)
and sets the `disposeentry` state `0x022C8010` to 0 (`0x0035A240`). Then it zeroes `scratch1` unconditionally
(`0x0026DB80`).

It then compares
the persistence group word (`+6` of the map-reference row at `[0x02099D88] + [header + 4] +
field × 8`) of the previous field (`0x00314870`) with the current one (`0x003148F0`); each reads as 0 while
`[0x02099D88]` or `[0x02099D90]` is null (`0x0026DB91`-`0x0026DB9D`, `0x0026DBC6`-`0x0026DBD2`), so no change is seen then.
When they differ it zeroes `scratch2` (`0x0026DC11`) and, unless the payload's `+0x1062` has bit `0x20`, runs
`0x003149E0` before that (`0x0026DBF4`-`0x0026DBFD`); it also zeroes `scratch2` when the transition options
(`0x003148D0`) have bit `0x8` (`0x0026DC1B`-`0x0026DC2E`).

So `scratch2` lives as long
as the player stays inside one group of fields, and `0x0025D8E0` / `0x00269A20` copy its 512 bytes
into and out of the save image, so it also survives a save: the copy out runs from the save-image
writer `0x00229B40` and from `0x00584580`, the copy back from `0x00584210` and `0x005843E0` under the save
controller `0x00582860`. The boot `0x00266D10` zeroes both banks, and the teardown `0x002695A0` (from
`0x002628B0`) zeroes `scratch1` together with the four party pointers at `0x0209A1F0` and the sixteen
tagged pointers at `0x0209A210`.

`0x00268320` is the other reset: it zeroes `scratch1` always, zeroes `scratch2` only when the load
flag `0x0209AC10` is 0 and `0x01E0C3EC` is set, and marks the payload's `+0x1061` when the flag is 0.
The save controller sets the flag to 1 at `0x00582E98`, the script verb `0x05BF` (start `0x00355E80`)
clears it through `0x00287D00`, and the verb `0x05BE` (start `0x00355940`) reads it through
`0x00286000`; in the shipped scripts only the Trial Mode
director uses the pair, to skip its entry sequences once after a load.

`global` variables are bytes of the save payload and are saved and loaded with it; `file` and
`local` variables live in the script image and are gone when the area's scripts unload. `POPV`
also looks up a notification id (`0x0032F240`, tables `0x022C6D18` and `0x022C6D28` by slot index) when
the slot index is 1 to 3 and the class is 0, and discards it: nothing is notified on that path.

## Layouts

Descriptor table [slot+`0x78`]:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count |  |
| `+0x04` | `...` | variables | then u64 per variable (dword 0 = the descriptor above) |

Array header (image + offset):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` |  | element descriptor |
| `+0x04` | `u16` |  | dimension count |
| `+0x06` | `u16` | word06 |  |
| `+0x08` | `...` | dim | u32 dim[n] |

Resolver record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | kind00 | 6, stored by the resolver (`0x00262667`) |
| `+0x04` | `u16` | kind |  |
| `+0x08` | `u16` |  | actor ordinal |
| `+0x0A` | `u16` | index |  |
| `+0x0C` | `u32` | descriptor |  |
| `+0x10` | `u64` | base+offset |  |
| `+0x18` | `u32` |  | element descriptor |
| `+0x1C` | `u32` |  | flat index |
| `+0x20` | `u32` | value | POPV |

```
reference (PUSHP) (offset + index*width) | class << 24 | 0x70000000, tag 1
```

Slot pointers:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | image |  |
| `+0x40` | `void*` | file |  |
| `+0x48` | `void*` | global | save payload |
| `+0x50` | `void*` |  | local region |
| `+0x58` | `void*` | scratch1 |  |
| `+0x60` | `void*` | scratch2 |  |
| `+0x68` | `void*` |  | int pool |
| `+0x70` | `void*` |  | float pool |
| `+0x78` | `void*` | descriptors |  |
| `+0x80` | `void*` | tags |  |
| `+0x98` | `void*` |  | local callback |

Banks:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x02099DF0` | `...` | scratch1 | `0x200` |
| `0x02099FF0` | `...` | scratch2 | `0x200` |

## Shipped data

| Fact | Value |
|---|---|
| descriptors in the 1,114 decoded scripts | 43,466: global 9,448, file 9,995, local 15,766, scratch1 2,292, scratch2 2,343, array 3,622, msp 0 ([script-variables-by-script.tsv](script-variables-by-script.tsv)) |
| save-payload offsets a script declares | 620, `0x0` to `0xCF4`; one offset shared by 575 scripts ([script-variables-global-offsets.tsv](script-variables-global-offsets.tsv), [script-variables-global-by-script.tsv](script-variables-global-by-script.tsv)) |
| global arrays | 34 ([script-variables-global-arrays.tsv](script-variables-global-arrays.tsv)) |
| variables whose tests gate script steps | 562 of the 620 offsets, in 4,230 rows, one per variable and script ([script-variables-global-gates.tsv](script-variables-global-gates.tsv)) |
| variable values and what each leads to | 3,355 rows for all 620 offsets ([script-variables-global-values.tsv](script-variables-global-values.tsv)) |
| variables that gate no step | 58, with the reason for each ([script-variables-global-nogate.tsv](script-variables-global-nogate.tsv)) |
| bank size | 512 bytes each |
| resolver callers | 4: `PUSHV`, `POPV`, `PUSHP`, `PUSHDBG` |

### What each global variable is for

[`script-variables-global-meanings.tsv`](script-variables-global-meanings.tsv) has one row for each of the 624
save-payload offsets. It is counted over the 1,114 decompiled `us` scripts and the three controller scripts
`bin/evctrl`, `bin/mapctrl` and `bin/btlctrl`, which ship in the `in` and `ch` trees only. A row gives the variable's role, one
sentence on what the scripts use it for, and its values: those the scripts write, test, switch on or mask. It also
gives the kinds of steps its tests choose, and the scripts that use it.

| role | variables | how the scripts use it |
|---|---|---|
| story counter and global flags | 1 | `0x0`, `global_flag[256]`: element 0 is the story counter |
| map-set position | 4 | `getmapdestposbyindex` fills them with a map exit's destination: the angle at `0x900`, then x, y and z at `0x904`, `0x908` and `0x90C` |
| weather slot | 1 | walk exits store `getweatherslot()` in it before the map jump |
| conversation counter | 17 | a talk function adds 1 to it and switches or tests on it |
| battle word | 15 | a map's foe setup (`setup.map` or `setup.battle`) tests it |
| control bit word | 57 | bit tests and bit writes make up at least half of its uses |
| area state | 328 | its other uses lie in the maps of one area (one three-letter map prefix, such as `rbn`) |
| game-wide state | 172 | its other uses lie in more than one area |
| debug display | 16 | the debug display (`sysDVAR`) or a developer menu of the controller scripts is all that uses it |
| declared | 13 | no statement of the story scripts reads or writes it; 12 of them appear in the developer test scripts |

The gates column counts the steps under each test of the variable by kind: map exits, floors and walls, items and gil,
scenes, messages, requests, stores, map models, battles, music and sound, screen and camera, and actors. A step under
several tests counts once for each variable it tests. Bits are written as values (`0x4` for `& 4`).

Two developer menus can also fill every byte `0x000` to `0xFFF` of the global area with 255 or 0: the field debug
menu's second convenience menu, answers 12 and 13 (`bin/mapctrl` lines 2792 to 2802), and the Battle Plan Menu's
event control, answer 6 (`bin/btlctrl` lines 1494 to 1510).

The scenario-flag menus of `bin/evctrl`,
`bin/btlctrl` and `bin/mapctrl` store the answer to a menu question in the story counter (`bin/evctrl` line
1338, `bin/btlctrl` line 3291, `bin/mapctrl` line 2850). Where the pages say that a value is written, or
never written, by the story scripts, or that something happens once in story play, these menus and the
developer event scripts (the evt_t scripts) can still write other values.

### What each global variable gates

[`script-variables-global-gates.tsv`](script-variables-global-gates.tsv) joins the global variables to the script
steps their tests choose. It has 4,230 rows, one for each variable and each script whose steps it gates, keyed by
`payload_offset` and `script`, and covers 562 of the 620 offsets. The joins are counted over the 1,114 decompiled `us`
scripts and `ttl_a01_e3`, which ships in the `cn` and `kr` trees only.

- A step is gated by a variable when a part of the condition on its row in an area step table (the `*-script-steps`
  tables of `14-Story-Event-Quest-Hunt/Areas`) names the variable, by the name its script declares for that offset, at
  any width and through any element.
- The steps of the 26 shared templates in [`shared-zone-script-steps.tsv`](../Story-Events-And-Hunts/shared-zone-script-steps.tsv) count for every script that carries the
  template.
- The spawn functions `fn_entry`, `fn_spawn` and `fn_respawn` have no step rows. For them a placement in
  [`enemy-placement-conditions.tsv`](../Enemy-Spawning/enemy-placement-conditions.tsv) whose test cells name the variable counts as a gated step, which gives 75 rows for
  49 variables.
- All 33,539 places where these scripts test a global variable lie in a script that has a gates row for that variable,
  so a variable has no gates row exactly when no script tests it.

### What each value means

[`script-variables-global-values.tsv`](script-variables-global-values.tsv) says, for every value a script tests or
writes, what happens when the variable holds it. It has 3,355 rows for all 620 offsets, keyed by `payload_offset`,
`element` and `value`, and the `source` column says what a row rests on:

| source | rows | what the row gives |
|---|---|---|
| gated steps | 2,343 | a value some step's condition tests: each form of the test, and for each form the place, the actor and function, and what every gated step does |
| written value | 544 | a value a script stores that no condition names: the stores, and the tested forms the value meets or fails |
| counter rule | 23 | a counter: the stores that add 1, and the rule by which its value chooses steps, read at the scripts |
| no gated step | 445 | a variable that gates no step: each value written to it, with the reason no step depends on it |

The table is one file. Offset `0x0` (`global_flag[256]`) alone holds 362 rows, 333 of them for
element 0, the story counter.

### Variables that gate no step

[`script-variables-global-nogate.tsv`](script-variables-global-nogate.tsv) has one row for each of the 58 offsets that
no step condition and no placement test names, keyed by `payload_offset`. None of the 58 is tested.

- The reason in each row comes from every use of the variable's bytes in the 1,114 `us` scripts and `ttl_a01_e3`,
  under every name and width any script declares for them.
- Each use is a store, a test, a copy into another variable, an argument to a verb, or the debug display call
  `sysDVAR`.
- The opcode behind `sysDVAR` calls the debug hook `0x0016D6A0`, which is a bare `ret 0` in the shipped game
  ([Script interpreter](script-interpreter.md)), so a variable whose only use is `sysDVAR` is never shown.

The reasons:

| reason | offsets | what the scripts do with the variable |
|---|---|---|
| `written only` | 31 | store values in it, and nothing reads them |
| `read only as a verb argument` | 10 | pass it to a verb, which reads or fills it |
| `debug display only` | 8 | name it only in `sysDVAR` |
| `copied` | 6 | copy it into another variable, whose own rows say what that one gates |
| `read only as a verb argument; copied` | 2 | both of the above |
| `declared, no use` | 1 | declare its bytes, and never store, test, read or pass them |

### Columns of script-variables-global-gates.tsv

| column | what it holds |
|---|---|
| `payload_offset` | the variable's offset in the save payload |
| `name` | the name the script declares for the offset, in that script |
| `script` | the zone or event script |
| `step_table` | the step table that holds the script's steps, or [`enemy-placement-conditions.tsv`](../Enemy-Spawning/enemy-placement-conditions.tsv) for placement rows |
| `elements` | the array elements whose tests gate steps: `-` for a scalar, an index, or `any` when the index is itself a variable |
| `steps` | how many different steps (actor, function and step) the variable gates in the script |
| `kinds` | the gated steps by what they do: messages, map exits, floors and walls, items and gil, scenes, requests, stores, map models, battles, music and sound, screen and camera, actors, spawns, control (the tests and loops themselves), other |
| `gated` | the gated steps, as `actor.function steps` ranges, each led by its element in brackets; a step of a shared template reads `actor (shared template id)`, and a placement reads `function.placement` with the `row` numbers of the placement table |
| `same_code` | the actors of the script that run the same code as another actor, whose steps the step table lists once under that actor |

### Columns of script-variables-global-values.tsv

| column | what it holds |
|---|---|
| `payload_offset` | the variable's offset in the save payload |
| `tool_name` | the names scripts declare for the offset, as in [`script-variables-global-offsets.tsv`](script-variables-global-offsets.tsv), joined by `/` |
| `element` | the array element, `-` for a scalar, or `any` when the index is itself a variable |
| `value` | the value: a number; `bit` and a mask for a bit test; `a to b` for a range case; `any other value` for a switch default; `compared with` another variable; `computed` for a test inside an expression with no number to name; `each pass` for a counter rule; `-` for a variable with no written value |
| `condition_forms` | each form of the test that picks the value, with its number of steps; `within:` gives a condition part that tests several things at once, in full |
| `leads_to` | for each form, after `When`: the place and script, the actor (by its in-game name where it has one) and function, and what each gated step does, with its step numbers; message steps quote the full `us` text in double quotes, except a few texts that hold double quotes of their own, which the row names by line and leaves to the step table's `quoted_lines`; verbs with no plain reading are written as their call, `verb(arguments)` |
| `steps` | what the row rests on: for gated steps, the step table, script, actor and function, and step ranges; for a written value or a counter rule, the stores, by script, actor, function and line of the decompiled script counted from 1; for a variable with no gated step, the nogate table |
| `source` | gated steps, written value, counter rule or no gated step (above) |

### Columns of script-variables-global-nogate.tsv

| column | what it holds |
|---|---|
| `payload_offset` | the variable's offset in the save payload |
| `tool_name` | the names scripts declare for the offset, joined by `/` |
| `reason` | why no step depends on it (the reasons above) |
| `census` | the bytes searched and the uses found, by kind |
| `read_by` | what reads it, in words: the verbs and arguments it is passed to, and for a copy, the variable it goes into and the steps that variable gates |
| `values_written` | every value the scripts store in it |
| `scripts` | the scripts that use it: their count and names, then, where developer test scripts also use it, "developer scripts" with their count and names |
| `sites` | how many uses read it (copies, verb arguments and references passed to verbs), not counting stores and `sysDVAR` |

### Columns of script-variables-by-script.tsv

| column | what it holds |
|---|---|
| `class3` | the script's descriptors of class 3, the image's msp area: 0 on all 1,114 rows; with the other class columns it adds up to `descriptors` on every row |

### Columns of script-variables-global-offsets.tsv

One row per save-payload offset a script declares, 620 rows.

| column | what it holds |
|---|---|
| `tool_type` | the C type declared with the offset's name: `u_char` (281 offsets), `char` (15), `int` (5), `float` (5), `short` (4) or `u_short` (2); empty on the 308 offsets that carry no name |
| `scalar_declarations` | how many scalar declarations (not arrays) name the offset across the 1,114 scripts; 0 on the 33 offsets that are declared only as arrays |
| `scalar_scripts` | how many scripts hold those declarations; equal to `scalar_declarations` on all 620 rows, so no script declares an offset twice |
| `scalar_widths` | the widths of those declarations with the number of each, for example `u8=3` or `s16=513`; empty where `scalar_declarations` is 0 |

### Columns of script-variables-global-by-script.tsv

One row per offset with a scalar declaration, 587 rows.

| column | what it holds |
|---|---|
| `scripts_declaring` | how many scripts declare a scalar at the offset with that `width`; the number of names in `scripts` on every row, and the same as `scalar_scripts` in script-variables-global-offsets.tsv |

### Columns of script-variables-global-arrays.tsv

| column | what it holds |
|---|---|
| `dims` | the number of elements the array is declared with, 1 to 256; `bytes` is `dims` times the element width on all 34 rows |
| `scripts_declaring` | how many scripts declare the array, 1 to 193; the number of names in `scripts` on every row |

### Columns of script-variables-global-meanings.tsv

| column | what it holds |
|---|---|
| `meaning` | one or more sentences on what the scripts use the variable for, written from its uses: who writes it, what its tests choose, or that only the debug display or the developer test scripts name it |

## Operations

Per variable opcode: resolve, then load and push or pop and store. Per field transition:
`0x0026DB30`. Per save: `0x0025D8E0` copies `scratch2` out; per load: `0x00269A20` copies it back and the
controller sets `0x0209AC10`.

## State

The save payload bytes `0` to `0xCF5` (the last declared offset, `0xCF4`, is a 16-bit variable), the script
image's file and local areas, and the two banks.

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
