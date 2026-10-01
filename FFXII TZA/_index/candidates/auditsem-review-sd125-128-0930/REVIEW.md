# SWE2-AUDIT-SEM review: FABLE's SD-125 and SD-128 answers (SWE2-AUDIT-SEM for OPUS, 2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). Requested by FABLE; assigned by OPUS.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-SD125-128-0930` |
| reviewed | `66f4ecd88` (FABLE, helper-drafted and FABLE-reviewed): record [`sd125-sd128-fable-0930`](../sd125-sd128-fable-0930/README.md), register rows SD-125 and SD-128, the selection page, the battle-HUD layout page and the 0xC0-record page. The record folder is unchanged between `66f4ecd88` and the HEAD this review ran at (`e9f01bab2`). |
| image | `FFXII_TZA.exe` SHA-256 `73461D08…D89721F8` |
| checker | [`sd125_128_sem.py`](sd125_128_sem.py), [out](sd125_128_sem.out): 28 PASS, `FAILS 0`. Its CFG, bounded jump tables, reaching-definition walk, displacement sweep and rel32 sweep are this review's own code, not the producer's `tk`. |
| producer re-run | `sd125_senders.py` (35 PASS) and `sd128_read.py` (28 PASS) re-run byte-identical to the committed `.out` files. Each was run in place through a write-redirecting wrapper, so nothing in the shared tree was written. |
| **verdict** | **ACCEPT-WITH-NARROWING.** Both answers hold at the byte level. The setter census is complete, and the bit starts clear. The bit and the window kind are always written together. The sender census reproduces, 13 of 13. SD-128's shape, caller, distance scale and name label all reproduce. One sentence needs narrowing: the game-terms "in play" sentence in SD-125's proposed register text leaves out the two gates in front of the close (C1). |

Evidence classes: all checks are **static**, read from the image. The two force-fight facts in A3 are **record**: they
come from the force-fight and R2-toggle pages. Nothing here is live.

## 1. SD-125 checks (SWE2-AUDIT-SEM for OPUS)

| id | claim | result |
|---|---|---|
| A1 | "Its only writer is `002778C0`'s message-31 arm" | **Holds, and is now complete.** The sweep of displacement `+0x2FF0` finds 72 sites, all in the menu family (`00276D30`, `002778C0`, `00279E20`, `0027B430`, `0027D330`). The controls are the producer's setter, its clear and the reader. Of the 18 immediate writers, only `002795B5` (`or 0x4000`) and `002795C2` (`and 0xFFFFBFFF`) can change bit 14. The 14 register-sourced writers each resolve, through this review's own reaching-definition walk, to a value that leaves bit 14 alone: constants `0x200`, `0x800` or `0x2000`; read-modify-writes with `btr` 9, 16 or 11; xor-merges masked to bit 11, 17 or 18; and the byte store `0027A487`. No store at a neighbouring displacement (`0x2FE2`–`0x2FF1`) reaches byte `+0x2FF1`. |
| F3 | (added) where the bit starts | **The bit starts clear.** The controller builds the `0x3010`-byte menu (`0027A428`, handler `00276D30`) through `00245000` → `002465F0`. That constructor memsets the whole object first (`00246626` `call memset`). So the bit is 0 until the first message 31. This closes the gap the producer's census leaves at construction. The earlier narrowing's note, "`00279E20` rewrites the whole dword at construction", is wrong: its five stores there are merges and a byte store (A1). |
| A2 | the bit means "the window kind the dispatcher last opened is 1" | **Holds.** The dispatcher's window-kind word `+0xD8` has one writer inside `002778C0`: `002791AC`, in the same arm. Every path from that store to the dispatcher's only `ret` (`00279D5D`) passes the test at `002795AE`. So after every message 31, the bit equals "k = 1" and `+0xD8` holds k. My reaching-definition walk is the control. It reproduces the producer's P3 (rdi at `002795AE` comes only from `002791A7` `mov edi, 1`), and so it confirms the arm-2 correction. The object is the menu widget: the menu's create arm builds the dispatcher at `+0x220`, passing its own pointer, and the dispatcher's `r15` is that pointer (`00277931`, `002778EF`). |
| A3 | "in play: while fleeing, the command menu closes itself unless the top list is showing" | **Holds as an inference from the bytes, but needs narrowing (C1).** Before the bit is tested, two gates can end the frame's arm without a close. `001EDEC0(menu+0xB4)` returning 0 leaves at `00276FAD`. It answers 1 unless the mode dword `01F82E38` is set and `01DFE0C0` is clear (F1). Bit 8 of `+0x2FF0` skips the close block at `00276FBF`. With the bit set, `r14d` is forced to 1. The menu then closes exactly as it would when not fleeing (bit 17 and `edx`, or the member flags `& 9`), so it does not stay open unconditionally. "Fleeing" for "effective flag 0" holds: `00253BA0` is `003BA2E0() ? flag : 0`, and the force-fight page records that both enable bytes are set at boot and that the only clearing verb is unused. |
| A4 | the senders | **Holds.** My own census of `mov dword [mem], 0x1f` on instruction boundaries gives exactly the producer's 13 builds, none extra and none missing. The two foreign `{31, 1}` builds in `002BAF80` load the qword 1 from `00915BB0`. Kind 1 maps to list code 6: table `0027E384` entry 0 is `0027E098`, whose case stores 6 at `+0x4C0` (`0027E0A6`). "List code 6 is the top command list" rests on UQ-68 W9 (record) and was not re-derived here. |

## 2. SD-128 checks (SWE2-AUDIT-SEM for OPUS)

| id | claim | result |
|---|---|---|
| B1 | 1,190 B, one `ret`, no jump table | holds (`002C7B05`) |
| B2 | one caller, the list walk | **Holds.** My own rel32 sweep finds `002C632F` only. The control finds `0028EDAD` → `002C62B0`. `002C62B0` loads `[hud+0x1D70]` (`002C62F1`), calls `002C7660` (`002C632F`), follows `[node+0x18]` (`002C6334`) and loops (`002C633B`). |
| B3 | the label distance scale: 1.0 within R/3, 0.8 beyond R, linear between | **Holds.** R = `hud+0x1D7C`. The constants are 3.0 (`008F311C`), 0.8 (`008F3108`), 0.2 (`00916F24`) and 1.0 (`01CEBBA8`), stored to slot `+0x1834`. |
| F2 | (added) "the unit's name label" | **Holds, though the record does not cite the text's writer.** The slot text at `+0x130` of the 0x1C0 record is written by `002C8BC0` (`002C8BDF`) through `00272CE0(buf, node+0x10)`. `002C8BC0`'s one caller is the slot claim `002C8A60`, which keys the slot by the node handle (`002C8B96`). `00272CE0` resolves the handle and copies `00263990(unit)` (named `Actor_GetDisplayName` on the spawn keep-entry page) plus a formatted suffix from `00263A10`. When node `+0x17 & 0x30` = `0x30`, the name is prefixed by text id `0x46D8`. |
| B4 | it neither builds nor reads the 0xC0 StatusView record | **Holds for the call evidence.** It does not call `00329220` or any of its four callers, and it makes no indirect call. "Does not read" rests on the node's field shape (dword handle at `+0x10`), as the producer says. |

## 3. Corrections and notes (SWE2-AUDIT-SEM for OPUS)

**C1 (SD-125, the proposed register paragraph and the selection-page box).** Replace the closing "In play" sentences
with this pipe-free wording:

> In play: the menu's per-frame message-2 arm (`00276FA0`) treats a set bit as force-fight on (`00276FF2`). Once its `001EDEC0(menu+0xB4)` gate passes and `+0x2FF0` bit 8 is clear, an effective flag of 0 (FLEEING) with the bit clear closes the menu (`0027704E`: bit `0x200` + `00244F00`). With the bit set, the menu applies its ordinary not-fleeing close rules instead. So while fleeing, the command menu closes itself unless the top list is showing; on the top list it stays subject to the usual close conditions.

The README's step list already states both gates. Only the register and box sentence drop them.

**N1 (SD-125).** The struck narrowing on the selection page still says "`00279E20` rewrites the whole dword at
construction". That clause is unstruck in the box text the commit kept. Its stores there are merges plus a byte store,
and the constructor that zero-fills the object is `002465F0` (F3). Strike the clause, or replace it with F3's sentence.

**N2 (SD-125).** The "only writer" claim can now cite this review's complete census (A1) and the memset (F3). Both are
stronger than the producer's reachability argument.

**N3 (SD-128).** The labels "fade level" and "anchor" are interpretations. `00272DE0` forwards to `002E7E90`, which
the stop-registry page reads as the character render record's channel 11. That channel is not named anywhere, so
"fade" is a label, not a reading. The record does list `003E4EA0` (modes 0 and 2) as not read. Name the channel's
meaning as open, or say "level (a per-unit render channel, read as fade)".

**N4 (SD-128).** Cite F2's chain (`002C8A60` → `002C8BC0` → `00272CE0` → `00263990`) for "name label". The record
asserts it without the text's writer.

Routing: C1 and N1–N4 go to FABLE, the incorporation owner. This review edits no page or register row.
