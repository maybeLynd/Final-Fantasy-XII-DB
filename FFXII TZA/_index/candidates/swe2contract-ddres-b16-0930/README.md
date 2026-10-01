# DD prose-residue closure, batch 16: the gambit page's residue sentences (SWE2-CONTRACT for OPUS, 2026-10-01)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`, batch 16. A Claude session ran the batch in the SWE2-CONTRACT lane,
started by OPUS. It used no subagents, no board tasks and no commits.

The batch covers one page, `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` (2,049 lines before the edit).
Every register row the page names is closed. About 25 sentences still said "not read / unread / not established /
still open / unknown" without an id. They were found with
`grep -n -i -E "not read|unread|not yet|not established|still open|remains open|unknown|not settled|not proven|not traced|no reader found"`,
and a second pass added `unproven|unidentified|\*\*not\*\*|leans no|OPEN`. Struck text was skipped. Each remaining
sentence was read in context.

The page was clean at HEAD before the edit (`git status --short` empty). It is CRLF on every line, and every edited
or added line keeps CRLF: `git diff --numstat` gives 20 / 12. The 12 removed lines are the 12 lines rewritten in
place: two corrections under a strike and ten pointer notes appended to the end of a line. The other 8 added lines
are three pointer paragraphs and one added note, each with its blank line. No status word was moved. The two
corrections carry a *Corrected 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16)* note; see
[`consumer-check.md`](consumer-check.md).

Legend: **RESIDUE, answered** = open and in scope, answered here. **STALE** = already answered elsewhere; it gets a
dated pointer. **BOUNDARY** = another page owns the fact. **already noted** = the sentence's own paragraph already
carries a later answer or scope note, so it was left alone.

Dates: the notes are dated 2026-10-01, as the request asked. The local clock read 2026-09-30, about 22:15 CDT, which
is 2026-10-01 UTC.

## Tally (SWE2-CONTRACT for OPUS)

| disposition | count | lines (after the edit) |
|---|---:|---|
| RESIDUE, answered (one question, two sentences, both corrected) | 2 | 467, 1217 |
| STALE, pointer added | 13 | 535, 628, 803 (heading, pointer at 805), 889, 896, 1227, 1317, 1417, 1499, 1628, 1803, 1858 (heading, pointer at 1860), 1951 (heading, pointer at 1953) |
| BOUNDARY | 0 new; 2 already scoped by FABLE on 2026-09-30, left alone | 1588 (`0x01DFE0B0`), 1989 (the options-screen list) |
| already noted, left alone | 3 | 372, 563, 1265 |
| not residue | 2 | 1761, 1766 |

The grep hits at 554, 727, 888, 1212, 1214, 1477, 1729 and 1880 are inside `~~strikes~~`. Line 1761 quotes the earlier
state, and the same sentence answers it. Line 1766 says section 2 "named but did not read" the rebuild, which the same
section then reads. Line 4, the status line, still names GR-9 as the page's one registered residue, but GR-9 is
ANSWERED (2026-09-30). That is a status move, left for OPUS (see the proposed status line).

## The residue: order-record flag bit `0x04` (SWE2-CONTRACT for OPUS)

| # | sentence (page, before the edit) | disposition | answer | checks |
|---|---|---|---|---|
| R1 | §7 Z-19 box (line 467): "… `0x400` / `0x1000` evaluator modes, `0x04` unread)" | RESIDUE, answered; **corrected** | `0x04` is read. While the unit's current order (`unit + 0x708`) carries it, `BattleUnit_CanAdvanceCombatNavigation` (`00325D90`) returns 0 at `00325DF4` / `00325DF8` → `00325DA5`. | N4–N6 |
| R2 | §8g table (line 1215), the `0x0004` row (256 records): "**no reader found** — the shifted test stops at entry 2" and "authored but unread" | RESIDUE, answered; **corrected** (the shifted-test half is true and kept) | The gate's only caller is `BattleUnit_UpdateCombatNavigationStep` (`00325BB0`, at `00325BD0`). On a 0 it calls `0033C9B0` on the locomotion block `unit + 0x80` and leaves (`00325BD5`–`00325BE1`). It skips the open path's route and step calls (`0030A130`, `00383620`, `00383670`, `003003F0`). So the order runs with **no combat navigation step**. The evaluator's chain test really does stop at entry 2 (`003016B5`). No player gambit carries the bit: all 256 condition rows' `+0xE` are 0. | N1–N7 |

**What the census shows.** The shipped data is the 166 `in` area files and, identically, the 166 `ch` files: 1,422
sets and 50,050 records. Bit `0x04` is on 256 records, and every bit count of the page's table is reproduced. The bit
is not a fourth chain bit: 200 of the 256 carry no chain bit, and 194 have only selector entry 0.

**How the reader was found.** The taint census seeds every qword load of `[reg + 0x708]` in the image (20 loads in 19
functions) and the record argument of the evaluator `003014C0`, the selector `00301AD0` and `BattleUnit_CommitAction`
`0030F760`. It finds exactly eleven accesses covering record `+4`, none with an unknown offset. The only bit-2 test
among them is `00325DF4 test byte ptr [rax + 4], 4`. The 2026-09-12 census did not list this reader.

**Added, not a strike.** The same census finds three sign tests of bit `0x8000` on the current order: `00308736`
(the combat frame, which skips its resume walk), `0030AF49` and `00328604`. No shipped record and none of the engine's
static order sets carry that bit, so the page's "never set" holds. Its reader column "—" does not, and an added note
under the table says so (N8).

**In player terms:** some enemy AI orders, 256 lines across the area files, are marked to be carried out without
combat movement. While such an order is the enemy's current one, the enemy takes no route or steering step. It acts
from where it stands. No gambit a player can set carries the mark.

## The stale sentences (SWE2-CONTRACT for OPUS)

| # | line (before the edit) | sentence | disposition | answered by | checks |
|---|---|---|---|---|---|
| S1 | 534–535 | "*what each of the twelve subgroups means in authored data is not read*" | STALE | UQ-121 (ANSWERED 2026-09-26, the next box); its residue GR-9 (ANSWERED 2026-09-30) | P1 |
| S2 | 626–628 | "`AiOrder_EvaluateTargetSelector` is 6,963 bytes and **unread**" | STALE (a superseded note sits below) | Z-1 (ANSWERED 2026-09-12), §8b | P1 |
| S3 | 803–810 | "What is still not read": the opcode numbering, "the comparison threshold path … only partly followed", "unidentified fields", "Z-1 is … not closed" | STALE | Z-1; the threshold is the entry's `+4` s16 word (`00301B1F`); the note at the end of the subsection names the fields | P1, P2 |
| S4 | 884–887 | "What is still not established: the unit" | STALE | Z-3 (ANSWERED): one second of maintained field frames | P1 |
| S5 | 891–894 | the 2× / 4× speed reading "is *not* proven … Recorded as **Z-10**" | STALE | Z-10 (CLOSED NO 2026-09-08): the frame-rate scalar | P1 |
| S6 | 1221–1223 | "Byte offsets are still not established" | STALE | Z-2 (ANSWERED 2026-09-17), §8l. The superseded note below it cites "the Z-2 box in §9", but the box is in §7; the pointer says so | P1 |
| S7 | 1312–1313 | "the action-id encoding has **not** been proven … recorded as **Z-16**" | STALE | Z-16 (ANSWERED 2026-09-17, yes): `00301830` decodes the `0x4000` band (`003018DD`–`003018FB`) | P1, P2 |
| S8 | 1412–1413 | "**Z-16 leans NO** … some other consumer could still decode a category" | STALE | Z-16 answered yes | P1 |
| S9 | 1493–1495 | "Whether any *other* mode is reachable from authored gambit data is **not established**" | STALE | Z-15, both halves (the notes below it and the register) | P1 |
| S10 | 1620–1624 | "has not read `FUN_0033F020` …, has not identified the configuration field at `+0x48`" | STALE | DH-1 (`FrameLimit`); `0033F020`'s seven targets include the six 60-fps table initialisers | P1, P3 |
| S11 | 1798–1799 | "which of the three members is the opcode is not proven here" | STALE (an answered note sits below) | Z-15 and Z-1 (the note at line 1805) | P1 |
| S12 | 1854 | heading "Z-19 advanced — three of the five unknown flag bits are one field" | STALE | Z-19; bit `0x04`'s reader is added by R2 | P1 |
| S13 | 1945 | heading "What is still open" (both boxes ticked) | STALE | DH-1, DH-2 | P1 |

## Proposed id-less rows (SWE2-CONTRACT for OPUS)

None. The one residue is answered statically, so nothing needs a runtime row or a NO ADMISSIBLE SOURCE row.

## What the evidence rests on, and its limits (SWE2-CONTRACT for OPUS)

- **The reader census is a may-taint over direct control flow** (`structflow.py`). It does not see indirect calls,
  record pointers kept in non-stack memory, or code outside retool's function extents. Its seeds are the current-order
  loads (`+0x708`) and the arguments of the three functions that take a record. `+0x738` is only compared, never
  dereferenced (`003015AD`). The walk's own record register is checked by a separate full-body scan (N5).
- **"Acts from where it stands"** describes only what the gate skips: the route and step calls of the navigation
  step. What `0033C9B0` itself does (it builds the solver context and resets avoidance, per the movement pages) and the
  on-screen result are not replayed here.
- **The player-gambit half** reads the us `battle_pack.bin` only. The rebuild copies row `+0xE` to record `+4` (Z-2).

## Receipts (SWE2-CONTRACT for OPUS)

Static work on the certified shipping image (`73461d08…`) through `retool.py` and `structflow.py`; the shipped archive
`D:/FFXII MP Mod/FFXII_TestClient1/FFXII_TZA.vbf` through `agent_flow/tools/vbfextract.py` (the 332 area files, the
us `battle_pack.bin`); the register `_index/OPEN-QUESTIONS.md`.

| script | result |
|---|---|
| `b16_checks.py` (`b16_checks.out`) | N1–N8, P1–P3, Z1–Z4: 89 PASS, FAILS 0 |
| `documented_rule.py` (`documented_rule.out`) | `READY 09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md … boxes=0 live=-`, `TALLY READY=1 of 1`, FAILS 0 |

run: _index/candidates/swe2contract-ddres-b16-0930/b16_checks.py at d526b865b (FAILS 0)

Positive controls in the checker:

- the census's 13 bit counts match the page's table, in two languages;
- the taint finds the seven Z-19 reader sites, each with its known mask (`0x2000`, `0x800`, `0x4000`, `0x200`,
  `0x100`, the chain load, the `0x1000` / `0x400` word);
- the walk's `0x40` / `0x80` tests are found;
- the condition rows' relation bytes are 137 / 68 / 51;
- the static records' flags match their pages (`01EEC298` and `01EEC3C0` `0x2000`);
- `0033F020` has seven targets.

## documented_rule verdict (SWE2-CONTRACT for OPUS)

**READY** (kinds GR-9, UQ-121, Z-16, Z-2 answered; no box, no live id). The page's status word is still PARTIAL, with
GR-9 named as open.

## Proposed status line (SWE2-CONTRACT for OPUS)

No status word is moved; this is for OPUS's owner read.

`status: DOCUMENTED — every register row the page names is closed (GR-9 answered 2026-09-30, UQ-121 2026-09-26, Z-2
and Z-16 2026-09-17, every other Z row closed); prose residue closed 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16):
order-flag bit 0x04 is read by the navigation gate 00325D90 (no combat navigation step while current), and the stale
"not read / not established" sentences carry dated pointers`

## Routed, not edited (SWE2-CONTRACT for OPUS)

- **OPEN-QUESTIONS.md Z-19**'s status cell says "`0x04` authored (256 records) but unread"; R1–R2 answer it. Routed to
  the row's owner.
- **CONTRACT-gambit-walk.md** §14 item 2 and its evidence row say `0x0004` has no reader. Routed to the contract's
  owner.
- **The movement page** (`battle-locomotion-steering-and-recovery.md`) does not describe the navigation step's
  opening gate. This batch's N6 is available to it.
- All four are in `consumer-check.md`. No register row was added or changed.
