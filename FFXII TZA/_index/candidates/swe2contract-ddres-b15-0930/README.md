# DD residue closure, batch 15: the nine id-less rows of batch 13, answered statically (SWE2-CONTRACT for OPUS, 2026-09-30)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`, batch 15. A Claude session ran the batch in the SWE2-CONTRACT lane,
started by OPUS. It used no subagents, no board tasks and no commits.

Batch 13 (`../swe2contract-ddres-b13-0930/README.md`, "Proposed id-less rows") proposed nine rows, P1–P9. **All nine
are answered statically here, so none of them needs a register row.** Each answer is written in place on its page with
a dated note, and each page has a new section holding the answers:

1. `16-UI/Request-Router/ui-request-router.md`: P1–P4, §7c
2. `16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`: P5–P7, §15b
3. `02-Resource-And-Asset-Pipeline/the-resource-request-queue.md`: P8–P9, §7c

All three pages were clean at HEAD before the edit (`git status --short` empty) and are LF-only. Each line keeps its LF
ending (`git diff --numstat`: router 60/4, number formatting 52/0, queue 41/2; the removed lines are the six rewritten in
place: three strikes and three appended notes). No status word was moved. Three statements are corrected under a strike with a
*Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 15)* note; see [`consumer-check.md`](consumer-check.md).

Legend, as in batch 13: **RESIDUE, answered** = open and in scope, answered here. **STALE** = another page had already
answered part of it. **BOUNDARY** = another page owns the fact. **corrected** = the page's own sentence was wrong.

## The nine answers (SWE2-CONTRACT for OPUS)

| # | disposition | answer | checks |
|---|---|---|---|
| P1 | RESIDUE, answered (with STALE: the resource ids were read by rc22-34) | `00D11C88` = kind-7 id `0x39` `gameover_c.tm2`; `00D11CA0` = id `0x38` `gameover.mrp`. The image is a 1024 × 256 8-bit TIM2, identical in all nine full-size language folders, and reads *GAME OVER*. The layout has one text slot, with string id −1 (none). The request-11 row's "wording unread" is corrected | G1–G6 |
| P2 | RESIDUE, answered by role; one page sentence corrected | No shipped file names flag `0x5E` (Primary bit 94). It is the airship-trip flag: set by the five aerodrome scripts right before `mapjump(124/125)` (the airship fields `asp_a01` / `asp_a02`) and by `rsn_z02`'s init; released by `asp_a02` and `rsn_z02`; tested by no script. While it is set, Triangle posts request 2 with `global_flag[2]`, or **1** when that is 0 (the page said 0), and so opens the airship-route page | F1–F5 |
| P3 | RESIDUE, answered by role | Bit 12 = "this session was loaded through load mode 3, the title's Trial Mode route" (FV-1). Its only live source is the controller's mode-3 test via `02089344` bit 0 and `00233C10`. The script arms `0x308D` / `0x308F` are unused by shipped scripts, and the restore clears it. Readers: image B, the restore flag, and three field-menu request paths that it blocks | B1–B4 |
| P4 | RESIDUE, answered | Yes. `00314440` replaces target 0 with field `0xC` (`ttl_a01`, the title) while the debug byte `02B62DB9` is 0, and the reset's 0 is that byte's only store. Field 0's own path is the bare test map `tst_a01` | T1–T4 |
| P5 | RESIDUE, answered | Byte 1 = argument selector (the formatter draws only for `0x7F`, the state's own number); byte 2 low nibble = field width (state `+0xA1`, low digits kept, padded); bit 6 unread; bit 5 = pad `'0'` or space; bit 4 = the font's second character map (a separate digit set, two-byte codes `0x3010`–`0x3910` in `us`) | D1–D8 |
| P6 | RESIDUE, answered | Bit 31 marks the Latin glyphs. In `us` / `it`: single-byte codes `0x20`–`0x8E`, `0x93`–`0x94`, `0x98`–`0xB6` (letters, accented letters, digits, ASCII punctuation); clear on a few marks, the `0xB7`–`0xFF` symbol and second-letter blocks and every two-byte glyph. In `kr` / `cn` / `ch` / `in` it is a minority Latin block. The 2.3-scaled gap goes before a Latin glyph that follows a non-Latin one | E1–E4 |
| P7 | RESIDUE, answered | The two arms only copy `+8` / `+0xC` into a local pen for `002A9F00`, which reads `+0` / `+4`; no reader anywhere on the text path. Padding | H1–H5 |
| P8 | RESIDUE, answered (with STALE: command 7's delete was on the manual-save page); one page sentence corrected | `003BB790` dispatches on the command word `02B40E1C` (0–9): 0 `003BAC90`, 1 `003BA7B0`, 2 `003BAEB0`, 3/4/5 none (idle), 6 `003BA990`, 7 `003BA5F0` (delete the named file), 8 `003BA720` (does the slot's save fit the free blocks), 9 `003BA680`. `02B40E14` is the handler's step, `02B40E18` the result class | S1–S4 |
| P9 | RESIDUE, answered | No. All sixteen raw-path request sites discard the id, so no shipped code can cancel a kind-`0xFF` request even once. The double free is latent in the API only | C1–C5 |

## The answers, in player terms (SWE2-CONTRACT for OPUS)

- **The game-over screen** is the words *GAME OVER* in red-glowing capitals. It is one picture, the same in every
  language, and no line of text is drawn under it.
- **During an airship trip, Triangle opens the route page** instead of the location map. The aerodromes raise a flag
  as the airship leaves, and the airship field drops it on arrival.
- **A Trial Mode session** (the title's second load route) keeps its own spawn-keep image, cannot open the field
  menus that bit 12 blocks, and arms the restore of the real save for the next ordinary load.
- **A save that fails the header check** sends the player back to the title screen.
- **Number codes in text** say which value to print, how many digits, whether to pad with zeros and which digit style.
- **Text spacing:** a small extra gap opens where a line passes from symbols or two-byte characters into Latin letters.
- **The save list** uses command 8 to learn which slots have room, and command 7 removes a slot's old file.
- **The loader's double-free hazard** cannot be reached by the game itself; only a mod that kept a raw-path id and
  cancelled it twice could hit it.

## What the evidence rests on, and its limits (SWE2-CONTRACT for OPUS)

- **P1's two words** rest on a visual reading of the decoded image (`gameover_c_us.png`, written by the checker). The
  checker pins the files, the ids, the layout, the two ink groups and the four-glyph first group, but not the letters.
  No text id or string exists to pin them against.
- **P6's group names** (dashes, guillemets, quote marks, arrows, the second letter set) rest on `glyphs_us_20_FF.png`.
  The checker writes it with the record decode `x` = bits 0–9 and `y` = bits 10–19, and its visual control is that the
  render reads A–Z, a–z in code order. The code ranges themselves are pinned.
- **P2's role** rests on the decompiled `us` corpus (`Tools/work/FABLE/pub140-scratch/corpus/us`, gitignored). The
  other languages' scripts were not scanned. Native setters with a computed id (`00329E60` through `0032ABE0`) are not
  followed; the literal-id native setters and the new-game list are.
- **P9's register-flow check** treats any call as overwriting `rax`, and follows only direct jumps inside the function.
  The 36 `0032E620` callers with a computed kind are not proven never to pass `0xFF`; doing so would be a different
  defect (`0032E902`).
- **Displacement censuses** (`02B62DB9`, `02089344`, `02B40E1C`, the slot table, the id counter) do not see a store
  through a rebased pointer or a block copy.

## Receipts (SWE2-CONTRACT for OPUS)

Static work on the certified shipping image (`73461d08…`) through `retool.py`; the game extract
`D:/FFXII_TZA_extract` (menu images and layouts of all ten language folders, the font packs, `mapjumpgroupinit.bin`);
the kind-7 path helper `../rc22-34-resource-readers-0930/kind7.py`; the decompiled `us` scripts.

| script | result |
|---|---|
| `b15_checks.py` (`b15_checks.out`) | G1–G6, F1–F5, B1–B4, T1–T4, D1–D8, E1–E4, H1–H5, S1–S4, C1–C5, Z1–Z2: 311 PASS, FAILS 0 |
| `documented_rule.py` (`documented_rule.out`) | `TALLY PARTIAL=2 READY=1 of 3`, FAILS 0 |

Positive controls in the checker: kind-7 id `0x3A` → `title.mrp`; the mrp walker finds real string ids in
`save_load.mrp`; the operand bank is imported at offset 0 by every script that imports it; kind-5 paths `0x132`
(`rbn_a18`) and `0x483` (`tri_a01`); the digit glyphs share one advance (AC-10) and `I` is narrower than `W`; the
register flow finds `0032E620`'s use of the id and `0032E7C0`'s return; the neighbouring verb `0x308C` has 854 calls.

## documented_rule verdicts, and why the number page now reads PARTIAL (SWE2-CONTRACT for OPUS)

- **ui-request-router.md: READY** (UQ-162, UQ-163 answered; no box, no live id).
- **the-resource-request-queue.md: PARTIAL**, as after batch 13: OV-19 and OV-33 are PARTLY ANSWERED, and their
  runtime remainder is the page's live-scheduling bound. This batch changes nothing there.
- **numeric-formatting-and-character-mapping.md: PARTIAL, boxes=1.** The box is the pre-existing `- [~]` at line 328
  (*Why Audio enters this cluster*, "ANSWERED IN PART 2026-09-02"). FABLE's 2026-09-30 rule change (`02d59b826`, after
  batch 13) counts `[~]` as residue. The box is at HEAD and outside the nine rows. Batch 13 had carried it. It was not
  ticked here, because ticking it would be a status move; it is left for OPUS's owner read.

## Proposed status lines (SWE2-CONTRACT for OPUS)

No status word is moved; these are for OPUS's owner read.

- **ui-request-router.md** (current line unchanged), add: `rows P1–P4 answered 2026-09-30 (SWE2-CONTRACT for OPUS, DD
  batch 15, §7c): the game-over wording (the image GAME OVER), flag 0x5E (the airship-trip flag; a zero operand word
  posts 1), bit 12 (the Trial Mode session), field 0 (the title); open only as runtime-only items`.
- **numeric-formatting-and-character-mapping.md**, add: `rows P5–P7 answered 2026-09-30 (DD batch 15, §15b): the
  .  and - payload, bit 31's Latin class, the pen's unread +8 / +0xC; open only as two runtime-only items and the
  partial Audio box (line 328)`.
- **the-resource-request-queue.md**, add: `rows P8–P9 answered 2026-09-30 (DD batch 15, §7c): the storage machine's
  command map and handlers 7 and 8; no shipped path cancels a raw-path request; open only as the runtime-only items`.

## Routed, not edited (SWE2-CONTRACT for OPUS)

- **OPEN-QUESTIONS.md EX-2** says request 0x0B's wording is unread; P1 answers it. **FZ-18** calls `003BB790` "the
  ten-substate machine over `02B40E10` / `02B40E14`"; P8 corrects that. **PKG-GP-HP-LETHAL** lists the game-over
  wording as a gap. All three are in `consumer-check.md`. No register row was added or changed.
- **Not proposed as rows:** nothing. No question needed a runtime or NO ADMISSIBLE SOURCE row. The two answers by role
  (P2's flag name and P3's bit name) are cases with no authored name at all: the scripts carry the id as a literal and
  the three verbs are unnamed.
