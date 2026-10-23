---
title: "PS2 CPU emulation: the in-memory PS2 register set that translated assembly runs on"
kind: "system"
category: "Engine core"
addresses: "0x0036D990, 0x0022CB90, 0x0036D9E0, 0x0036D930, 0x0036D8E0, 0x0036DD80, 0x0036DD90, 0x0036DDA0, 0x00398F90, 0x00397910, 0x003970A0, 0x0025A8E0, 0x0024AD00, 0x00363FD0, 0x0026EE00, 0x0022A0B0, 0x0017D6E0, 0x003D2B60, 0x003CD840"
---

## What the player sees

Nothing directly. Every particle that is placed, every bone that is multiplied through a matrix,
every vertex that is projected for the old PlayStation 2 style effects, and the search for the
sound source nearest the listener all pass through this code. On the PlayStation 2 that work was
hand-written assembly for the console's vector unit and its 128-bit integer instructions. The
remaster did not rewrite those routines.

It translated them instruction by instruction into x64, and the registers the instructions named
became ordinary globals. The game boots with the log line
`PS2 Assembly emulation initilization completed! ***`.

## How it works

### The register bank

The registers live in one block of zero-initialised data at `0x022D8F08`, plus the constant
register `vf00` at `0x01EF93F0`, which holds `(0, 0, 0, 1)` in the image. Nothing in the block
has an image value; the start-up routine, the clear and the re-assert write `vf00`'s constant
again. Each general-purpose register is a 16-byte cell, as on the Emotion Engine, and each vector
register is four floats.

The translation keeps the MIPS register conventions, which is what identifies the block. Register
0 at `0x022D8F10` is `$zero`: 45 functions read it 444 times and nothing writes it, and loop exits
compare the counter against it (`0x0024AD00` ends its vertex loop on `t0 == $zero` at `0x0024AF0A`).

The caller-saved temporaries `t0` to `t7` carry almost all the traffic; the argument registers
`a0`/`a1` and the return registers `v0`/`v1` are next; the callee-saved `s` registers, `a2`,
`a3`, `k0`, `k1`, `gp`, `sp`, `fp` and `ra` have no reference at all (one dword inside `s3`'s
cell, `0x022D904C`, is read once by `0x0051D310`, which uses the scratch dwords below the same way).

| register | address | functions | writes | reads |
|---|---|---|---|---|
| `$zero` | `0x022D8F10` | 45 | 0 | 444 |
| `at` | `0x022D8F20` | 1 (`0x00362230`) | 1 | 1 |
| `v0` | `0x022D8F30` | 29 | 108 | 50 |
| `v1` | `0x022D8F40` | 10 | 24 | 19 |
| `a0`, `a1` | `0x022D8F50`, `0x022D8F60` | 9 each | 15 each | 15 each |
| `t0` | `0x022D8F90` | 64 | 653 | 478 |
| `t1` | `0x022D8FA0` | 46 | 929 | 334 |
| `t2` | `0x022D8FB0` | 41 | 321 | 592 |
| `t3` | `0x022D8FC0` | 27 | 166 | 179 |
| `t4` | `0x022D8FD0` | 20 | 195 | 142 |
| `t5` | `0x022D8FE0` | 13 | 76 | 58 |
| `t6`, `t7` | `0x022D8FF0`, `0x022D9000` | 7 each | 144, 56 | 71, 28 |
| `t8`, `t9` | `0x022D9090`, `0x022D90A0` | 3 each | 7 each | 9 each |

`HI` at `0x022D9110` and `LO` at `0x022D9120` are written by ten functions at fifteen sites each: the
multiply in `0x0026EE00` (`0x0026F0E6`, `0x0026F0EC`) and the family `0x00506A40`, `0x00506B40`, `0x00507120`,
`0x00507490`, `0x005080A0`, `0x00508C90`, `0x00509BB0`, `0x0050A100` and `0x00545650`.

A halfword multiply forms the eight signed products of the matching 16-bit halfwords of its two 16-byte
operands and keeps them in `LO` and `HI`, one 32-bit word each. `0x00506A40` shows the order
(`0x00506A70`-`0x00506B2E`), and `0x0026EE00` uses the same one (`0x0026F0E0`-`0x0026F1D2`):

| Word | `LO` (`0x022D9120`) | `HI` (`0x022D9110`) |
|---|---|---|
| 0 | halfword 0 | halfword 2 |
| 1 | halfword 1 | halfword 3 |
| 2 | halfword 4 | halfword 6 |
| 3 | halfword 5 | halfword 7 |

`0x0026EE00` then copies the low halfwords of words 1 and 3 of `LO` and `HI` into halfwords 1, 3, 5 and 7 of
`v0` (`0x0026F24F`-`0x0026F280`). No instruction reads word 2 of either register (see Project notes).

The vector unit's registers follow. `0x022D9130` is the 24-bit `CLIP` flag: `0x0025A8E0` shifts it
left by six and sets one bit per comparison of x, y and z against `+|w|` and `-|w|` (`0x0025A8EE`
to `0x0025A96A`), which is the `VCLIP` instruction, and two more translated bodies do the same inline
(`0x003623C0` at `0x00362611` to `0x00362662`, `0x00521450` at `0x00521966` to `0x00521A86`). All three mirror
the new word to `0x022D9478`, and the only readers are those three and `0x0025C830` (`0x0025CEFA`),
which tests the bits after calling `0x0025A8E0` four times.

`0x0025C830` is the box test of class-1 trigger records that files the `touch` and `touchon`
script requests ([script requests](../Scripts-And-Script-Commands/script-requests.md)).

`0x003623C0` and the segment chain `0x00362230` (with its helper `0x00363FD0`) are point clamps of the
map-sound emitter shapes, called from the emitter walk `0x003631B0`
([geometry primitives](../Movement-And-Pathfinding/geometry-primitives.md),
[map sounds](../Sound-And-Music/map-sounds.md)).

`0x022D9198` is `Q`, the divide and square-root result: 55 functions write it at 85 sites, always
from a division (`0x0024AEC0` stores `vf00.w / w`, `0x003640CE` stores `vf00.w / |d|²`). `0x022D91A0`
is `ACC`, the accumulator the multiply-add forms read: 83 functions write it, 544 stores and 356
loads.

`0x022D91B0` to `0x022D939F` are the vector registers `vf01` to `vf31`, 16 bytes apart, so register n
sits at `0x022D91A0 + 16n`; `vf00` is the constant `(0, 0, 0, 1)` at `0x01EF93F0`, read by 132
functions and written only by the start-up `0x0036D990`, the clear `0x0036D9E0` and the re-assert
`0x0036DD80`.

Which registers a routine uses is its own choice, as on the real unit: `0x00398F90` keeps its matrix
in `vf01` to `vf04`, `0x0024AD00` keeps its matrix in `vf20` to `vf23`. The rows `vf01` to `vf04`
are busy (72, 76, 68 and 55 functions), and `vf20` and `vf21` at `0x022D92E0` and `0x022D92F0` are
the busiest of all (124 and 128 functions).

### Start-up, clear and the flag helpers

The boot routine `0x0022A0B0` ([startup constants](startup-constants.md)) calls `0x0036D990` at
`0x0022A125` and `0x0022CB90` at `0x0022A12A`. `0x0036D990` stores `vf00 = (0, 0, 0, 1)` and logs
`Sizeof 64 bit int = 8` and the completion line through `0x0017D280`.

`0x0022CB90` is the vector unit 1 side: it zeroes the 16 KB data memory `0x02064E30`, the words
`0x02064E1C`, `0x02064E28`, `0x02064E2C`, `0x02088E30` to `0x02088E38`, `0x01E02830` and `0x01E02838`, sets
`0x01E0283C` to 1.0, and logs the same two lines
([the VIF1 / VU1 layer](ps2-vif1-vu1-emulation.md)). The
restart loop `0x0017D6E0` calls `0x0022CB90` again at `0x0017D723` on every pass.

`0x0036D9E0` re-stores `vf00` and zeroes the forty rows `0x022D91B0` to `0x022D942F` with eighty 8-byte
stores.
Its two callers are the model update entries `0x003DFFE0` and `0x003E00C0`, which run it before the
translated per-model routines `0x0040EE70`, `0x0040F390`, `0x0040D890`, `0x0040ACF0` and `0x0040B180`. Rows
`0x022D93A0` to `0x022D942F` have no other reference, so the live vector registers end at `vf31`.

`0x0036DD80` re-stores `(0, 0, 0, 1)` into `vf00` from the image constant and has 90 callers; a
translated body calls it after every store that used `vf00` as an operand, before the constant
is read again (`0x0025C830` does so four times, `0x00363FD0` three). `0x0036DD90` and `0x0036DDA0`
set bits `0x80` and `0x40` of the byte `0x022D9470` (twelve callers each, `0x00361FF5`, `0x0040ADAE`,
`0x003A29A5` and their siblings); nothing reads that byte.

### Register save and restore

`0x0036D930(count, &cell1, &cell2, …)` takes the count in `ecx` and one cell address per further
argument, read back from the caller's home slots; it copies each 16-byte cell into the value
stack `0x02EC0800`, records the address at `0x02EC0A00` and stores `count` into the depth word
`0x022D8F08`.
`0x0036D8E0` copies the cells back from the stack in order and zeroes the depth. A translated body
saves the register its caller still needs and restores it on the way out. Nine functions do so, and
each pairs one save with one restore:

| function | save site | register | restore site |
|---|---|---|---|
| `0x0026EE00` | `0x0026EE2C` | `v0` (`0x0026EE17`) | `0x0026F413` |
| `0x003AFDD0` | `0x003AFDEC` | `v0` | `0x003AFFAB` |
| `0x003D8E50` | `0x003D8E78` | `v0` | `0x003D8FE2` |
| `0x0042FDB0` | `0x004300F9` | `v0` and `v1` (`0x004300E0`, `0x004300EC`, count 2) | `0x0043035E` |
| `0x00431D30` | `0x00431D4C` | `v0` | `0x00431F0A` |
| `0x00462260` | `0x0046227C` | `v0` | `0x0046242E` |
| `0x0044BAC0` | `0x0044C43E` | `t0` | `0x0044C4C3` |
| `0x002F1CE0` | `0x002F1CF5` | `t0` (`0x002F1CE9`) | `0x002F1D7D` |
| `0x002F1D90` | `0x002F1DAC` | `t0` | `0x002F1E9B` |

Four of the restores (`0x0026F413`, `0x003AFFAB`, `0x00431F0A`, `0x0046242E`) are tail jumps. The depth
word is read only by the pair, and the stack holds at most the two cells of `0x0042FDB0`.

### The three shared routines

Most C code that needs the vector unit's matrix reaches it through three small routines.

`0x00398F90(in, out)`, 74 functions at 102 sites, transforms one point through the matrix in `vf01`
to `vf04`. It
copies `in` to `vf22` (`0x022D9300`), forms `ACC = x·vf01 + y·vf02 + z·vf03`, then
`vf23 = vf04·vf00.w + ACC` (`0x022D9310`), and stores `vf23` into `t0` (`0x022D8F90`) and into `out`.
The point's own fourth component is copied and never used: `w` is `vf00.w = 1`, so the routine
transforms positions, not directions, and there is no divide. The matrix is row-major with the
translation in row `vf04`.

`0x00397910(a, b, out)`, 82 functions at 129 sites, multiplies two 4×4 matrices. It copies both
inputs to its stack
(`0x00397977` to `0x003979DE`) before any store, so `out` may alias either input, and then writes
`out[i][j] = Σk b[i][k] · a[k][j]`, row by row, with the loop at `0x00397A10` to `0x00397AED` producing
one column of all four rows per pass. The result is `b × a`, not `a × b`, and the routine returns
`out`. It touches no register of the bank.

`0x003970A0(out)`, 30 callers, copies the 64 bytes of `vf01` to `vf04` into `out`.

### Two translated bodies read as examples

`0x0024AD00(out, matrix, verts, count)` (callers `0x00249080`, `0x00249110`, `0x003C6420`) is a vertex
projection. It loads the matrix into `vf20` to `vf23`, the count into `t0`, and for each vertex:
`vf24 = vert`; `ACC = x·vf20 + y·vf21 + z·vf22`; `w' = vf23.w·w + ACC.w`; `Q = vf00.w / w'`;
`vf25 = (vf23·w + ACC) · Q`; `vf26 = int(vf25 · 16)`, stored to `out`. The 16 is the Graphics
Synthesizer's 12.4 fixed-point vertex format. The loop decrements `t0` and ends when it equals
`$zero`.

`0x0026EE00(out, a, b)` saves `v0`, reads `$zero` as a 16-byte operand at `0x0026EE34`, forms signed
16-bit lane products through `t0` to `t3` with each product split into `LO` and `HI`, writes the
packed result through `out`, and tail-jumps to the restore. It is the only user of `HI`/`LO`
outside the `0x00506A40` family.

### What the bank is not

`0x022D9138`, inside the block, is the enable word of a random-number stream and belongs to
[random number generators](../Random-Numbers/random-number-generators.md). The dwords
`0x022D9144` to `0x022D916C` are scalar scratch for eleven translated bodies (`0x003AC110`, `0x003B4310`,
`0x003B5D40`, `0x005131C0`, `0x00515DA0`, `0x00515FE0`, `0x0051D310`, `0x0053DB50`, `0x0042CBF0`, `0x00395050`,
`0x003954E0`) and stand for no named register; `0x022D9134` is written by four of them and read by
none; `0x022D9450` to `0x022D945F` is written by `0x002487A0` and `0x00248A90` (all four lanes, three times each) and
read by nothing.

## Layouts

```
0x022D8F08  u32        save depth (0x0036D930 / 0x0036D8E0)
0x022D8F10  16 B × 32  GPR[0..31]: $zero at +0, v0 at 0x022D8F30, t0 at 0x022D8F90 (see table)
0x022D9110  16 B       HI
0x022D9120  16 B       LO
0x022D9130  u32        CLIP (24 bits used); 0x022D9478 u32 its mirror
0x022D9138  u32        RNG stream enable (not a register)
0x022D9144..0x022D916C   scalar scratch of eleven bodies
0x022D9198  f32        Q
0x022D91A0  f32[4]     ACC
0x022D91B0  f32[4] × 31  vf01..vf31 at 0x022D91A0 + 16n
0x022D93A0..0x022D942F   cleared by 0x0036D9E0, otherwise unreferenced
0x022D9470  u8         flag byte: 0x80 by 0x0036DD90, 0x40 by 0x0036DDA0; never read
0x01EF93F0  f32[4]     vf00 = (0, 0, 0, 1); image constant copied by 0x0036DD80
0x02EC0800  16 B × n   saved register values; 0x02EC0A00 the saved addresses
```

## Shipped data

| Fact | Value |
|---|---|
| functions referencing the block or `vf00` | 273 (251 the block, 22 only `vf00`), in [ps2-cpu-emulation-functions.tsv](ps2-cpu-emulation-functions.tsv) |
| of those, using general-purpose registers | 99 (27 only those) |
| using vector registers, `ACC`, `Q` or `CLIP` | 217 (145 only those); 72 use both sets |
| heaviest bodies by bank references | `0x003D2B60` 1,625; `0x003CD840` 749; `0x00413C80` 474; `0x0040B780` 433; `0x00411650` 428; `0x00533B20` 405; `0x00548A00` 402 |
| `vf00` writers / readers | 3 / 132 |
| `Q` writers | 55 functions, 85 sites |
| `ACC` writers / readers | 83 / 46 functions |
| save / restore pairs | 9; registers `v0` ×6, `t0` ×3, `v1` once |

The table lists every function with the register groups it touches (`depth`, `GPR`, `HILO`,
`CLIP`, `Q`, `ACC`, `rows`, `misc`, `tail`, `vf00`) and its write, read and address-only
reference counts.

## Operations

At boot: `0x0036D990`, then `0x0022CB90`. Before each model update that uses the translated per-model
routines: `0x0036D9E0`. In every translated body: loads and stores on the cells above, `0x0036DD80`
before a read of `vf00` that follows a `vf00 - vf00` store, `0x0036D930` on entry and `0x0036D8E0` on
exit when a register must survive. From C code: `0x00398F90`, `0x00397910` and `0x003970A0`.

## State

The block `0x022D8F08` to `0x022D947B`, `vf00` at `0x01EF93F0`, and the save stack at `0x02EC0800` /
`0x02EC0A00`. Every value is whatever the last body left there; no routine owns a register between
calls, and a value that survives is one nobody overwrote.

### The shift-amount register

`0x022D8F0C`, between the save depth and `$zero`, is the Emotion Engine's shift-amount register `SA`. Before each
call of `0x00501820`, `0x00502280` stores `((signed byte) sil ^ 2) << 4` there (`0x00502670`, `0x005027C1`).
`0x00501820` is `QFSRV`: it shifts the 256-bit pair of its two source registers right by `SA` bits into its
result (`0x00501822`-`0x00501939`). A shift of 0 copies the low source, and 64 joins the high half of the low
source to the low half of the high source.

### The loop counter

`0x022D94A0`, past the block's end, is the 64-bit loop counter of the translated loops. A body stores its
remaining count near the end of each pass and runs the pass again while the counter is not 0. It compares it
either with `$zero` (11 sites) or with the immediate 0. `0x00394E50` stores it at `0x00395011` and compares it at
`0x0039502A`. Its row in the table below lists every function that stores or compares it.

### Lanes, scratch and the rows past vf31

The register table above names each register by its first byte. Translated bodies also address bytes,
halfwords and words inside a register, for example the byte lanes of `t2` that `0x00446050` stores. Each such
address has its own row in [ps2-cpu-emulation-state.tsv](ps2-cpu-emulation-state.tsv):

- the byte, halfword and word lanes of `t2` to `t7` (`0x022D8FB1` to `0x022D900E`);
- the top byte of `CLIP`, `0x022D9133`, which each `VCLIP` step clears after its shift;
- the scalar scratch dwords `0x022D9148` to `0x022D9168`, with what each body stores in them;
- lanes y and w of `ACC` and the lanes of `vf01` to `vf31` that are named by their own address;
- the 8-byte words of the rows `0x022D93A0` to `0x022D942F`, which only the clear `0x0036D9E0` writes;
- the four lanes of the cell `0x022D9450` to `0x022D945F`, which only `0x002487A0` and `0x00248A90` write.

An access counts for a row when its bytes include the row's address. A 16-byte register store therefore
appears in the row of every lane it covers, and a lane loop over a register appears in every lane's row.

The table also has a row for each of these addresses:

- the byte, halfword and word lanes of `t0` and `t1` (`0x022D8F91` to `0x022D8FAF`), the word lanes of `v0`
  (`0x022D8F34` to `0x022D8F3C`), the word lanes of `t2` (`0x022D8FB4` to `0x022D8FBC`) and the halfword lanes of `t3`
  (`0x022D8FC2` to `0x022D8FCE`). The save `0x0036D930` reads every lane of `v0` and `t0` (`0x0036D974`) and the
  restore `0x0036D8E0` writes them back (`0x0036D90F`), through the cell addresses of the table of saves above;
- words 1 to 3 of `HI` (`0x022D9114` to `0x022D911C`) and of `LO` (`0x022D9124` to `0x022D912C`);
- lanes y and z of `vf00` (`0x01EF93F4`, `0x01EF93F8`), which every store keeps at 0;
- the scratch dword `0x022D9158`, which `0x0051D310` and `0x0053DB50` store;
- lane z of `ACC` (`0x022D91A8`) and 44 further lanes of `vf01` to `vf31`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| each row of [ps2-cpu-emulation-state.tsv](ps2-cpu-emulation-state.tsv), one per address | the row's `type` | the row's `start`: 0 from the zero-filled tail of `.data`, or 0 in the image for `vf00`'s lanes y and z | the row's `meaning` | the row's `set_by` | the row's `read_by` |

## Modding notes

- `0x00398F90` writes its result to `vf23` and `t0` as well as `out`; a replacement that only fills
  `out` starves any translated body that reads the registers afterwards.
- `0x00397910` is `b × a`. Swapping the operands gives a different matrix that still looks like a
  transform.
- A matrix loaded into `vf01` to `vf04` is overwritten by the next routine that uses those rows;
  copy it out with `0x003970A0` first.
- `$zero` is never written. A hook that stores into `0x022D8F10` changes every loop that ends on it.

## Related

- [Startup constants](startup-constants.md): the boot sequence that initialises the layer.
- [The VIF1 / VU1 layer](ps2-vif1-vu1-emulation.md): the
  second vector unit, with its own data memory at `0x02064E30`.
- [Random number generators](../Random-Numbers/random-number-generators.md): the stream
  word at `0x022D9138`.
