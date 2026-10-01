# Image-base two-level switches — 64 functions whose dispatch tables no ordinary sweep can see

**OPUS, 2026-09-16.** Generated from `embedded_exe.bin` sha256 `73461d08…21f8`, image base `0x00120000`.

## The idiom

```
lea   rX, [rip - D]                     computes EXACTLY 00120000, the image base
movzx eax, byte ptr [rX + rax + I]      index byte table
mov   ecx, dword ptr [rX + rax*4 + C]   case RVA table
add   rcx, rX
jmp   rcx
```

The tables are reached as **base + displacement and never materialised as an address**, so no
`E8`/`E9`/`LEA`/pointer sweep sees a reference to them. This is the class FABLE's `imagebase`
absence instrument exists for, and the reason `UQ-156` could call two 4.8 KB handlers *unparsed*.

## The control, built in rather than bolted on

A function is listed only when **every** clause holds:

- the `lea` computes **exactly** the image base — not *a plausible constant*;
- **every** decoded arm lands inside the owning function's declared body;
- the `ja` default target is itself one of those arms.

**52 candidates were rejected**, and their reasons are counted rather than dropped silently:

| reason | count |
|---|---:|
| switch shape incomplete | 47 |
| `ja` target not among the arms | 3 |
| arms outside the body | 1 |
| `lea` is not an instruction boundary | 1 |

**Not asserted:** that the tables lie outside the body. That is true of `002B7B80` by accident and
**false** of `002BAF80`, whose case table sits inside its declared extent.

## What is incomplete, stated rather than hidden

The id **bias** is read from the range check where the shape allows it (`lea eax,[rdx-1]`,
`add eax,-0x12`, `add eax,-0x40`) and is **unread for 32 of the 64**. For those rows the id
**range size** is known and the id **values** are not.

A first version printed `ids 1..N` for every row. That is false for most of them, and
spot-checking `005FD5F0` (bias `0x12`, a 52-byte predicate returning 1 or 0) and `003A92D0`
(bias `0x40`) is what caught it. **A range size is not an id range**, in the same way a store
width is not a field width.

## The scan

923 sites in `.text` compute exactly the image base with a REX.W `lea`; they sit in **641**
functions of the census; **64** carry a fully verified two-level switch.

> **CORRECTED 2026-09-16 (OPUS), same day.** The first version of this note printed the heading
> *"VERIFIED … 64"* over a table of **22 rows**, because the generating script displayed only its
> top 22 and I pasted its output. A reader met a count and a table that did not agree, with
> nothing reconciling them. **All 64 verified rows are listed below.**
>
> The same limit had already propagated: the register cross-reference in the next section reads
> this table, and over 22 rows it reported **3** OPEN rows where the true answer over all 64 is
> **5**. *A tool that reads another tool's **display** inherits its display limits* — the same
> class as a regex that read the wrong commit because a note capitalised a word.

```
VERIFIED image-base two-level switches: 64
entry      name                            bytes id range         arms handled
0082D130   FUN_0082d130                      349 0x3B..0x11D        12      12
001D0190   FUN_001d0190                      251 0x01..0xDE          6      12  Presentation
002F3910   FUN_002f3910                      284 bias unread        48      47
002F3BC0   FUN_002f3bc0                      711 bias unread        48      47
0043F450   FUN_0043f450                     9092 bias unread        48      47  Presentation
002F4020   FUN_002f4020                      864 bias unread        47      46
005FD5F0   FUN_005fd5f0                       52 0x12..0xE2          2      26
0082CCC0   FUN_0082ccc0                      391 0x7B..0x121         9       8
00798FF0   FUN_00798ff0                     1941 0x01..0xA5         12      13
002F31C0   FUN_002f31c0                      233 0x40..0xD1          7       6
003A92D0   FUN_003a92d0                      128 0x40..0xD1          2       7  Presentation
00325260   BattleUnit_HandleActionTimelin   1215 bias unread        11      11  CombatAction
00500C00   FUN_00500c00                     1259 bias unread         8       7  Presentation
00306BD0   BattleAction_InitializeGlobalS    284 bias unread         7      60  CombatAction
00520800   FUN_00520800                      811 bias unread         9       8
002FDDA0   BattleUnit_ExecuteDirectStateC   1937 0x40D2..0x4148      6      96  CombatAction
00209530   FUN_00209530                      432 0x0A..0x7D         10      12
0043EAB0   FUN_0043eab0                      136 0x42..0xAB         19      18
0043EBF0   FUN_0043ebf0                      136 0x42..0xAB         19      18
0043ED30   FUN_0043ed30                      133 0x42..0xAB         19      18
004FF440   FUN_004ff440                     3553 0x42..0xAB         19      18  Presentation
00538910   FUN_00538910                      138 0x42..0xAB         19      18
0043E9C0   FUN_0043e9c0                       89 0x42..0xA3         10       9
004FF360   FUN_004ff360                      109 0x42..0xA3          2       9  Presentation
0024E4B0   FUN_0024e4b0                      308 bias unread         4      28
00713820   FUN_00713820                      120 0x1D..0x63          8       7
00301AD0   AiOrder_EvaluateTargetSelector   6963 bias unread        31      59  CombatAI
002B49F0   FUN_002b49f0                     2022 0x2B..0x6E          8       7
0071B550   FUN_0071b550                      149 0x01..0x41         14      64
00322280   FUN_00322280                       66 0x200A..0x2048      2      10
003250F0   BattleUnit_HandleReactionAnima    279 0x2002..0x203C      7      14
008162F0   FUN_008162f0                     1087 0x41..0x78          7      16
002FE660   FUN_002fe660                      282 bias unread         5       6  CombatAction
00276D30   FUN_00276d30                     2849 bias unread        11      10  UI
002ED6F0   FUN_002ed6f0                      356 0x43..0x77         13      12
002085B0   FUN_002085b0                      120 0x44..0x77          2       7
00279E20   FUN_00279e20                     3006 bias unread        22      21  UI
00312B40   FUN_00312b40                      582 bias unread        11      25
002778C0   BattleMenu_UpdateCommandSelect   9374 bias unread        14      14  UI
003CB650   FUN_003cb650                      924 bias unread        14      13  UI
002B7590   FUN_002b7590                     1417 bias unread        13      12
002BA700   FUN_002ba700                     2077 bias unread        13      12
002B7B80   FUN_002b7b80                     4847 0x01..0x2A         16      17
002BAF80   FUN_002baf80                     4810 0x01..0x2A         16      17
005528C0   FUN_005528c0                     4521 bias unread        17      17  UI
00552250   FUN_00552250                     1543 bias unread        13      12  UI
002B6DB0   FUN_002b6db0                     1033 bias unread        10       9
002BC3E0   FUN_002bc3e0                     1422 bias unread        10       9
00729870   FUN_00729870                      109 0x14..0x38          2       8
00553F40   FUN_00553f40                      817 bias unread        11      10  UI
00240750   FUN_00240750                       88 0x04..0x26          5      14
0031EB20   BattleMenu_BuildCommandEntryLi   4182 0x01..0x23         11      34  UI
00819C90   FUN_00819c90                      150 bias unread        10       9
0081AE20   FUN_0081ae20                      348 bias unread         8       9
003CAB00   FUN_003cab00                      693 bias unread         7       6  UI
0029BE50   FUN_0029be50                     1663 bias unread         8       7
00299090   FUN_00299090                     1040 bias unread         7       6  UI
008229F0   FUN_008229f0                      401 0x06..0x22          6      17
00254B50   FUN_00254b50                      263 0x01..0x18          6       6  UI
0023B530   FUN_0023b530                      402 0x01..0x17          5      18
0023B6F0   FUN_0023b6f0                     1031 bias unread         3      12
0027C3D0   BattleMenu_ClassifySelectedEnt    717 bias unread         6      13  UI
0081FCA0   FUN_0081fca0                      331 bias unread         5       4
002805D0   FUN_002805d0                      127 bias unread         3       7  UI

rows whose id bias could not be read (reported, not guessed): 32 of 64

rejected candidates, by reason (a rejection is a report, not a silence):
   switch shape incomplete              47
   ja target not among the arms         3
   arms outside the body                1
   lea is not an instruction boundary   1

```

## Which OPEN register rows name one of these

Converting the inventory into routing: these rows name a function whose dispatch is now
mechanically decodable. **None of them is answered by that alone** — a decoded switch gives
the id space and the arms, not the meaning.

```
OPEN rows naming a decodable switch function: 5

  line 1018   BI-11      00325260
    What the **`Runtime.PackedIdBucketRegistry` family** holds. Ten functions using the 32-bit top-nibble scheme cluster in `0024Cxxx`-`0024Fxxx`, and the

  line 1705   CG-6       002F4020
    **Where are the GIF command buffers consumed?** *Reframed from `PROPOSED-xiionline-13-1`, which did not close.* **The producer side is fully mapped; t

  line 2092   EE-12      003250F0, 00325260
    **Whether `003250F0` (`BattleUnit_HandleReactionAnimationEvent`), `00325090` and `00325260` (`BattleUnit_HandleActionTimelineEvent`, 1,215 B) ever exe

  line 2120   EH-4       003250F0
    **What any flag bit means.** Eleven bytes are read-modify-written with exact masks (`&0x7F`, `&0xDF`, `&0xFE`, `&0x8F`, `&0x3C`, `\|0xF0`, `&0xFFFFDEF

  line 2929   UQ-156     002B7B80, 002BAF80
    What each page draws, and the message protocol of the `0xBC08` pages (`002B7B80` and `002BAF80` are "unparsed" in the handler census). [the-map-screen

```

**`EE-12` cannot be closed this way and is not being offered as closeable.** Its remaining
half asks whether those handlers *ever execute*, which is a runtime question; a static parse
of their dispatch says nothing about it.

