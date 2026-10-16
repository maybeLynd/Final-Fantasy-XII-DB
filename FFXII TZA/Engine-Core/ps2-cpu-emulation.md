---
title: "PS2 CPU emulation: the in-memory PS2 register set that translated assembly runs on"
kind: "system"
category: "Engine core"
addresses: "0036D990, 0022CB90, 0036D9E0, 0036D930, 0036D8E0, 0036DD80, 0036DD90, 0036DDA0, 00398F90, 00397910, 003970A0, 0025A8E0, 0024AD00, 00363FD0, 0026EE00, 0022A0B0, 0017D6E0, 003D2B60, 003CD840"
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

The registers live in one block of zero-initialised data at `022D8F08`, plus the constant
register `vf00` at `01EF93F0`, which holds `(0, 0, 0, 1)` in the image. Nothing in the block
has an image value; the start-up routine, the clear and the re-assert write `vf00`'s constant
again. Each general-purpose register is a 16-byte cell, as on the Emotion Engine, and each vector
register is four floats.

The translation keeps the MIPS register conventions, which is what identifies the block. Register
0 at `022D8F10` is `$zero`: 45 functions read it 444 times and nothing writes it, and loop exits
compare the counter against it (`0024AD00` ends its vertex loop on `t0 == $zero` at `0024AF0A`).

The caller-saved temporaries `t0` to `t7` carry almost all the traffic; the argument registers
`a0`/`a1` and the return registers `v0`/`v1` are next; the callee-saved `s` registers, `a2`,
`a3`, `k0`, `k1`, `gp`, `sp`, `fp` and `ra` have no reference at all (one dword inside `s3`'s
cell, `022D904C`, is read once by `0051D310`, which uses the scratch dwords below the same way).

| register | address | functions | writes | reads |
|---|---|---|---|---|
| `$zero` | `022D8F10` | 45 | 0 | 444 |
| `at` | `022D8F20` | 1 (`00362230`) | 1 | 1 |
| `v0` | `022D8F30` | 29 | 108 | 50 |
| `v1` | `022D8F40` | 10 | 24 | 19 |
| `a0`, `a1` | `022D8F50`, `022D8F60` | 9 each | 15 each | 15 each |
| `t0` | `022D8F90` | 64 | 653 | 478 |
| `t1` | `022D8FA0` | 46 | 929 | 334 |
| `t2` | `022D8FB0` | 41 | 321 | 592 |
| `t3` | `022D8FC0` | 27 | 166 | 179 |
| `t4` | `022D8FD0` | 20 | 195 | 142 |
| `t5` | `022D8FE0` | 13 | 76 | 58 |
| `t6`, `t7` | `022D8FF0`, `022D9000` | 7 each | 144, 56 | 71, 28 |
| `t8`, `t9` | `022D9090`, `022D90A0` | 3 each | 7 each | 9 each |

`HI` at `022D9110` and `LO` at `022D9120` are written by ten functions at fifteen sites each: the
multiply in `0026EE00` (`0026F0E6`, `0026F0EC`) and the family `00506A40`, `00506B40`, `00507120`,
`00507490`, `005080A0`, `00508C90`, `00509BB0`, `0050A100` and `00545650`.

The vector unit's registers follow. `022D9130` is the 24-bit `CLIP` flag: `0025A8E0` shifts it
left by six and sets one bit per comparison of x, y and z against `+|w|` and `-|w|` (`0025A8EE`
to `0025A96A`), which is the `VCLIP` instruction, and two more translated bodies do the same inline
(`003623C0` at `00362611` to `00362662`, `00521450` at `00521966` to `00521A86`). All three mirror
the new word to `022D9478`, and the only readers are those three and `0025C830` (`0025CEFA`),
which tests the bits after calling `0025A8E0` four times.

`022D9198` is `Q`, the divide and square-root result: 55 functions write it at 85 sites, always
from a division (`0024AEC0` stores `vf00.w / w`, `003640CE` stores `vf00.w / |d|²`). `022D91A0`
is `ACC`, the accumulator the multiply-add forms read: 83 functions write it, 544 stores and 356
loads.

`022D91B0` to `022D939F` are the vector registers `vf01` to `vf31`, 16 bytes apart, so register n
sits at `022D91A0 + 16n`; `vf00` is the constant `(0, 0, 0, 1)` at `01EF93F0`, read by 132
functions and written only by the start-up `0036D990`, the clear `0036D9E0` and the re-assert
`0036DD80`.

Which registers a routine uses is its own choice, as on the real unit: `00398F90` keeps its matrix
in `vf01` to `vf04`, `0024AD00` keeps its matrix in `vf20` to `vf23`. The rows `vf01` to `vf04`
are busy (72, 76, 68 and 55 functions), and `vf20` and `vf21` at `022D92E0` and `022D92F0` are
the busiest of all (124 and 128 functions).

### Start-up, clear and the flag helpers

The boot routine `0022A0B0` ([startup constants](startup-constants.md)) calls `0036D990` at
`0022A125` and `0022CB90` at `0022A12A`. `0036D990` stores `vf00 = (0, 0, 0, 1)` and logs
`Sizeof 64 bit int = 8` and the completion line through `0017D280`.

`0022CB90` is the vector unit 1 side: it zeroes the 16 KB data memory `02064E30`, the words
`02064E1C`, `02064E28`, `02064E2C`, `02088E30` to `02088E38`, `01E02830` and `01E02838`, sets
`01E0283C` to 1.0, and logs the same two lines
([the VIF1 / VU1 layer](ps2-vif1-vu1-emulation.md)). The
restart loop `0017D6E0` calls `0022CB90` again at `0017D723` on every pass.

`0036D9E0` re-stores `vf00` and zeroes the forty rows `022D91B0` to `022D942F` with eighty 8-byte
stores.
Its two callers are the model update entries `003DFFE0` and `003E00C0`, which run it before the
translated per-model routines `0040EE70`, `0040F390`, `0040D890`, `0040ACF0` and `0040B180`. Rows
`022D93A0` to `022D942F` have no other reference, so the live vector registers end at `vf31`.

`0036DD80` re-stores `(0, 0, 0, 1)` into `vf00` from the image constant and has 90 callers; a
translated body calls it after every store that used `vf00` as an operand, before the constant
is read again (`0025C830` does so four times, `00363FD0` three). `0036DD90` and `0036DDA0`
set bits `0x80` and `0x40` of the byte `022D9470` (twelve callers each, `00361FF5`, `0040ADAE`,
`003A29A5` and their siblings); nothing reads that byte.

### Register save and restore

`0036D930(count, &cell1, &cell2, …)` takes the count in `ecx` and one cell address per further
argument, read back from the caller's home slots; it copies each 16-byte cell into the value
stack `02EC0800`, records the address at `02EC0A00` and stores `count` into the depth word
`022D8F08`.
`0036D8E0` copies the cells back from the stack in order and zeroes the depth. A translated body
saves the register its caller still needs and restores it on the way out. Nine functions do so, and
each pairs one save with one restore:

| function | save site | register | restore site |
|---|---|---|---|
| `0026EE00` | `0026EE2C` | `v0` (`0026EE17`) | `0026F413` |
| `003AFDD0` | `003AFDEC` | `v0` | `003AFFAB` |
| `003D8E50` | `003D8E78` | `v0` | `003D8FE2` |
| `0042FDB0` | `004300F9` | `v0` and `v1` (`004300E0`, `004300EC`, count 2) | `0043035E` |
| `00431D30` | `00431D4C` | `v0` | `00431F0A` |
| `00462260` | `0046227C` | `v0` | `0046242E` |
| `0044BAC0` | `0044C43E` | `t0` | `0044C4C3` |
| `002F1CE0` | `002F1CF5` | `t0` (`002F1CE9`) | `002F1D7D` |
| `002F1D90` | `002F1DAC` | `t0` | `002F1E9B` |

Four of the restores (`0026F413`, `003AFFAB`, `00431F0A`, `0046242E`) are tail jumps. The depth
word is read only by the pair, and the stack holds at most the two cells of `0042FDB0`.

### The three shared routines

Most C code that needs the vector unit's matrix reaches it through three small routines.

`00398F90(in, out)`, 74 functions at 102 sites, transforms one point through the matrix in `vf01`
to `vf04`. It
copies `in` to `vf22` (`022D9300`), forms `ACC = x·vf01 + y·vf02 + z·vf03`, then
`vf23 = vf04·vf00.w + ACC` (`022D9310`), and stores `vf23` into `t0` (`022D8F90`) and into `out`.
The point's own fourth component is copied and never used: `w` is `vf00.w = 1`, so the routine
transforms positions, not directions, and there is no divide. The matrix is row-major with the
translation in row `vf04`.

`00397910(a, b, out)`, 82 functions at 129 sites, multiplies two 4×4 matrices. It copies both
inputs to its stack
(`00397977` to `003979DE`) before any store, so `out` may alias either input, and then writes
`out[i][j] = Σk b[i][k] · a[k][j]`, row by row, with the loop at `00397A10` to `00397AED` producing
one column of all four rows per pass. The result is `b × a`, not `a × b`, and the routine returns
`out`. It touches no register of the bank.

`003970A0(out)`, 30 callers, copies the 64 bytes of `vf01` to `vf04` into `out`.

### Two translated bodies read as examples

`0024AD00(out, matrix, verts, count)` (callers `00249080`, `00249110`, `003C6420`) is a vertex
projection. It loads the matrix into `vf20` to `vf23`, the count into `t0`, and for each vertex:
`vf24 = vert`; `ACC = x·vf20 + y·vf21 + z·vf22`; `w' = vf23.w·w + ACC.w`; `Q = vf00.w / w'`;
`vf25 = (vf23·w + ACC) · Q`; `vf26 = int(vf25 · 16)`, stored to `out`. The 16 is the Graphics
Synthesizer's 12.4 fixed-point vertex format. The loop decrements `t0` and ends when it equals
`$zero`.

`0026EE00(out, a, b)` saves `v0`, reads `$zero` as a 16-byte operand at `0026EE34`, forms signed
16-bit lane products through `t0` to `t3` with each product split into `LO` and `HI`, writes the
packed result through `out`, and tail-jumps to the restore. It is the only user of `HI`/`LO`
outside the `00506A40` family.

### What the bank is not

`022D9138`, inside the block, is the enable word of a random-number stream and belongs to
[random number generators](../Random-Numbers/random-number-generators.md). The dwords
`022D9144` to `022D916C` are scalar scratch for eleven translated bodies (`003AC110`, `003B4310`,
`003B5D40`, `005131C0`, `00515DA0`, `00515FE0`, `0051D310`, `0053DB50`, `0042CBF0`, `00395050`,
`003954E0`) and stand for no named register; `022D9134` is written by four of them and read by
none; `022D9450` to `022D9457` is written by `002487A0` and `00248A90` and read by nothing.

## Layouts

```
022D8F08  u32        save depth (0036D930 / 0036D8E0)
022D8F10  16 B × 32  GPR[0..31]: $zero at +0, v0 at 022D8F30, t0 at 022D8F90 (see table)
022D9110  16 B       HI
022D9120  16 B       LO
022D9130  u32        CLIP (24 bits used); 022D9478 u32 its mirror
022D9138  u32        RNG stream enable (not a register)
022D9144..022D916C   scalar scratch of eleven bodies
022D9198  f32        Q
022D91A0  f32[4]     ACC
022D91B0  f32[4] × 31  vf01..vf31 at 022D91A0 + 16n
022D93A0..022D942F   cleared by 0036D9E0, otherwise unreferenced
022D9470  u8         flag byte: 0x80 by 0036DD90, 0x40 by 0036DDA0; never read
01EF93F0  f32[4]     vf00 = (0, 0, 0, 1); image constant copied by 0036DD80
02EC0800  16 B × n   saved register values; 02EC0A00 the saved addresses
```

## Shipped data

| Fact | Value |
|---|---|
| functions referencing the block or `vf00` | 273 (251 the block, 22 only `vf00`), in [ps2-cpu-emulation-functions.tsv](ps2-cpu-emulation-functions.tsv) |
| of those, using general-purpose registers | 99 (27 only those) |
| using vector registers, `ACC`, `Q` or `CLIP` | 217 (145 only those); 72 use both sets |
| heaviest bodies by bank references | `003D2B60` 1,625; `003CD840` 749; `00413C80` 474; `0040B780` 433; `00411650` 428; `00533B20` 405; `00548A00` 402 |
| `vf00` writers / readers | 3 / 132 |
| `Q` writers | 55 functions, 85 sites |
| `ACC` writers / readers | 83 / 46 functions |
| save / restore pairs | 9; registers `v0` ×6, `t0` ×3, `v1` once |

The table lists every function with the register groups it touches (`depth`, `GPR`, `HILO`,
`CLIP`, `Q`, `ACC`, `rows`, `misc`, `tail`, `vf00`) and its write, read and address-only
reference counts.

## Operations

At boot: `0036D990`, then `0022CB90`. Before each model update that uses the translated per-model
routines: `0036D9E0`. In every translated body: loads and stores on the cells above, `0036DD80`
before a read of `vf00` that follows a `vf00 - vf00` store, `0036D930` on entry and `0036D8E0` on
exit when a register must survive. From C code: `00398F90`, `00397910` and `003970A0`.

## State

The block `022D8F08` to `022D947B`, `vf00` at `01EF93F0`, and the save stack at `02EC0800` /
`02EC0A00`. Every value is whatever the last body left there; no routine owns a register between
calls, and a value that survives is one nobody overwrote.

## Modding notes

- `00398F90` writes its result to `vf23` and `t0` as well as `out`; a replacement that only fills
  `out` starves any translated body that reads the registers afterwards.
- `00397910` is `b × a`. Swapping the operands gives a different matrix that still looks like a
  transform.
- A matrix loaded into `vf01` to `vf04` is overwritten by the next routine that uses those rows;
  copy it out with `003970A0` first.
- `$zero` is never written. A hook that stores into `022D8F10` changes every loop that ends on it.

## Related

- [Startup constants](startup-constants.md): the boot sequence that initialises the layer.
- [The VIF1 / VU1 layer](ps2-vif1-vu1-emulation.md): the
  second vector unit, with its own data memory at `02064E30`.
- [Random number generators](../Random-Numbers/random-number-generators.md): the stream
  word at `022D9138`.
