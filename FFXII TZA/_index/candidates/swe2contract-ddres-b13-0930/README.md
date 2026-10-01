# DD residue closure, batch 13: the request router, number formatting and the request queue (SWE2-CONTRACT for OPUS, 2026-09-30)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`, batch 13 (brief `Tools/work/OPUS/lane_brief_dd_b13.md`). A
Claude session ran the batch in the SWE2-CONTRACT lane, started by OPUS. It used no subagents, no board tasks and no
commits.

All three pages were clean at HEAD (`git status --short` empty), LF-only and unchanged by peers during the batch:

1. `16-UI/Request-Router/ui-request-router.md`
2. `16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`
3. `02-Resource-And-Asset-Pipeline/the-resource-request-queue.md`

The sentences were found with `grep -n -i` for *not read, unread, not yet, not established, still open, remains open,
unknown, not settled, not proven, not followed, not traced, not decoded, not named, stays open, is open, what remains*.
Lines already struck, or already carrying a later answer, are marked carried. No status word was moved. The residue
clauses of pages 2 and 3 now say what is answered, and the old text is kept after "was —". Every correction keeps the
removed text under a strike with a *Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13)* note; see
[`consumer-check.md`](consumer-check.md). Each line keeps its LF ending (`git diff --numstat`: 141/18, 102/18, 42/4).
Line numbers below are those at HEAD before the batch.

Legend: **STALE** = already answered, so a dated note or strike points to the answer. **BOUNDARY** = another page owns
the fact. **RESIDUE** = open and in scope; it is answered here, proposed as a row, or marked runtime-only. **carried** =
the line already holds its answer.

## Dispositions (SWE2-CONTRACT for OPUS)

### ui-request-router.md: STALE 7, BOUNDARY 2, RESIDUE 14 (SWE2-CONTRACT for OPUS)

| line | sentence | disposition |
|---|---|---|
| 33 | "several request IDs have no recovered player-facing name" | STALE: UQ-162 answered 2026-09-25; note names the two screens still unread |
| 80 | request 11 "on-screen wording unread" | RESIDUE: the widget family looks up no text id (R4); proposed row P1 |
| 82, 87 | 14 and 21 "**name open**" | STALE (two rows): C-1 / C-2, unused request numbers |
| 85, 457 | "what kind 7 changes is not read" | **RESIDUE, answered (R5)**: nothing inside the map tests 7, so it draws like kind 1; closing it ends the request as 2 and 3 do |
| 90 | request 24: "builds the battle-menu selection state (`0035BC50`) — the reserve-swap prompt"; "on-screen wording unread" | **RESIDUE, answered and corrected (R2, R3)**: text `0x86F`, then request 2 on close; `0035BC50` is request 3's arm (struck) |
| 179 | "who clears the word is unread" | **RESIDUE, answered (R1)**, struck: `00252D90` and the reset `00252DE0` |
| 187 | "how long ... and who clears it, stay outside" | RESIDUE: who = R1; how long is runtime-only |
| 198 | "Which screen reads those two fields is not followed here." | **RESIDUE, answered (R8)**, struck: `00290CF0` → `00276650`, the `0x61F0` battle menu (line 64 had named the result) |
| 204–205 | "its callees ... are unread, and so is what it shows" | **RESIDUE, answered (R2, R3)**, struck; the callee bodies are not claimed |
| 290–292 | `+0x598`; bit 12; bank 2 | RESIDUE: `+0x598` answered (R9); bank 2 STALE (L-13's 2026-09-21 observation); bit 12's writers read (R10), meaning proposed row P3 |
| 315–317 | callees, delivery order, field 0; "`L-13` stays open for that" | L-13 STALE (SUPERSEDED, struck); callees BOUNDARY (title-asset page, SetSaveData page, layout page); order runtime-only; field 0 proposed row P4 |
| 336 | key address `0035D6B0`: "unread" | **RESIDUE, answered (R2)**, struck |
| 398 | "Requests 14 and 21 have no proven identity" | STALE: C-1 / C-2 |
| 439–440 | `0x21` versus a non-zero operand word; flag `0x5E`'s name | **RESIDUE, answered (R7)**: `0x21` opens the location map; flag name proposed row P2 |
| 453 | "request 7's producer is still to be found" | STALE: the 2026-09-25 answer in the same item |
| 477–478 | the `spattack` window's name | RESIDUE, runtime-only: its procedure looks up only control-code templates (R12) |
| 495–497 | aerodrome names; kind 7; native path for 15 / 18 / 19; Quickening; live | **RESIDUE**: names answered (R6), kind 7 (R5), native path STALE by the 2026-09-25 census (R13); the rest runtime-only |
| 547 | "which this page has not read" | STALE: §2 reads `00280A00` (struck) |
| 696–697 | `002AF340`'s return; `00916548` | BOUNDARY: CONTRACT-auto-status-rebuild §13q and the text-control contract |
| 706 | "How often the stepper itself is called per frame was not traced." | RESIDUE: one call site (R11); per-frame count runtime-only |
| 764 | `00249410` "(body not read here)" | BOUNDARY: the handbook image-bundle page reads it |
| 772 | "The allocation half is still open" | STALE: UQ-163 answered 2026-09-17 |
| 529–531, 637, 666 | the switch-label caution; UQ-163 "unknown"; mode 2 | carried |

### numeric-formatting-and-character-mapping.md: STALE 17, BOUNDARY 3, RESIDUE 13 (SWE2-CONTRACT for OPUS)

| line | sentence | disposition |
|---|---|---|
| 4 (status) | "on-screen column parity and the written fields' meanings (UQ-173) are open" | STALE: AC-10 answered 2026-09-17, UQ-173 answered 2026-09-26; residue clause rewritten |
| 36–39 | "Four of the thirteen ... boundaries ... not yet drawn" | STALE: UQ-383 |
| 212 | `+0xA6` "what it means is not read" | **RESIDUE, answered (N1)**: the glyph sheet's font slot; 7 is the alternate sheet |
| 213 | `+0xB8` "what it selects is not read" | **RESIDUE, answered (N2)**: the glyph run's pixel-test word (code `0x47`) |
| 215 | "**`UQ-164` is `PARTIAL`, not answered.** What the block is *called* is still unknown," | STALE: UQ-164 CLOSED (struck) |
| 305 | "`002A9F00`, which is unread" | STALE: §14, AC-9 (struck) |
| 308–309 | "Only 4 of the cluster's 13 functions are read" | STALE: UQ-383 |
| 425 | why the sub-step opt-in governs the windows' confirm | RESIDUE, runtime-only (purpose) |
| 549–550 | `003FFC60`'s fields "*mean*" | RESIDUE: consumers named (the `.` and `-` escapes); proposed row P5 |
| 577 | descriptor layout "transcribed, not decoded, on the glyph-run page" | BOUNDARY: the glyph-run pages |
| 586 | "fixed pitch per call, set by the caller" | RESIDUE, qualified (N3): true of the formatter only |
| 591 | AC-10's "one pitch per line or ... per character" | **RESIDUE, answered (N3)**: per character |
| 885 | "any kind's subject except 3" | BOUNDARY: the text-element dispatch-table page |
| 894 | `[owner + 0xC0]` the shared dialog's list child? | **RESIDUE, answered (N4)**: yes, `002D14E0`'s list widget on both |
| 898 | "Whether that re-stamps the same state ... was not traced" | **RESIDUE, answered (N5)**: a fresh stack state |
| 934 | "The row stays open because the cluster has other doors" | STALE: UQ-166 answered |
| 1005 | "(2,304 B, unread)" | STALE: §14 (struck) |
| 1121 | "The largest thing this function calls is also unread" | STALE: §12, UQ-170, UQ-177 |
| 1162–1163, 1185–1186, 1191, 1207 | UQ-168's "row stays open", "polarity ... not established", "placed but not named", "not named" | STALE (four lines): UQ-168 answered 2026-09-18 in the same item |
| 1266, 1271 | "what was not read"; "1,658 instructions were surveyed, not decoded" | STALE (two lines): the dispatch is mapped, UQ-170 / UQ-177 |
| 1286 | pen `+8` and `+0xC` "are not named here" | RESIDUE: proposed row P7 |
| 1423–1425 | `+0xAE` "Still not named"; six fields untouched | STALE: answered 2026-09-25 / 26 in the same item |
| 1441 | `+0x9E`'s three `002B3xxx` readers "not read here" | **RESIDUE, answered (N6)** |
| 1445–1446 | "the unit ... and who reads `+0x8E`" | STALE: answered 2026-09-26 |
| 1617–1622 | "whether callers pass each drawn character ... not traced"; "not settled here" | **RESIDUE, answered (N3)** |
| 1644 | "though what it gates was not followed" | STALE: the 2026-09-14 answer below it |
| 1675 | "Which glyphs carry bit 31 ... was not identified." | RESIDUE: proposed row P6 |
| 1710 | UQ-176's "what those two command-word fields are" | BOUNDARY: the glyph-run pages |
| 1724 | why 1920-unit strips | RESIDUE, runtime-only |
| 329, 482, 502, 557, 590, 1476, 1496, 1558, 1574, 1708 | struck items and stated answers | carried |

### the-resource-request-queue.md: STALE 2, BOUNDARY 2, RESIDUE 1 (answered) (SWE2-CONTRACT for OPUS)

| line | sentence | disposition |
|---|---|---|
| 4 (status) | "deeper services, live scheduling, path/callback lifetime and complete authored reachability remain separately bounded" | **RESIDUE, answered (Q1–Q2)**: each item's bound is named (table below and the page's new §7b); residue clause rewritten |
| 571–573 | the arena above 2 GB; the crash values' page alignment | STALE (the 2026-09-20 trace); the alignment half runtime-only (EO-3's live remainder) |
| 600 | the `malloc` tail "stays open on that page" | BOUNDARY: what-the-engine-fixes-at-boot.md |
| 611 | "Which `malloc` call creates the arena buffer was not traced" | STALE: traced 2026-09-20 (`0022A1E1`) |
| 673 | "What each of the ten substates does is not decoded." | BOUNDARY: five of seven handlers are read on the save pages; the other two and the substate map are proposed row P8 |
| 75, 177, 295, 540, 644 | DG-6; `+0`'s purpose; results 2 / 3; EO-3 "open"; the byte count | carried |

**The four bounds of page 3's status clause:**

| item | bound | left |
|---|---|---|
| deeper services | §8 of the page (FZ-14, FZ-18, FZ-19, the dormant tick); the save pages for the storage handlers; OV-19 and OV-33 (PARTLY ANSWERED); SECTION-02 review Q4 | service issuance and loading-state timing, runtime-only (`FABLE-REQ-ASTRA-RT-REMAINDERS-0929`); P8 |
| live scheduling | SECTION-02 review Q3; the page's §1 | runtime-only, the same carrier |
| path / callback lifetime | EO-3 SUPERSEDED (`FABLE-REQ-ASTRA-EO3-PATH-POINTER`); Q1 for the copy's frees; DD batch 6 Z2 (no part callback); OV-36 ANSWERED (single delivery) | P9 |
| complete authored reachability | DD batch 6 Z2 and A0–A6; the chunk gate `003EB0D0` on the music-control page §3 | which requests run during an active stream, runtime-only |

None of the four is unbounded.

## The answers, in player terms (SWE2-CONTRACT for OPUS)

- **When the whole active party falls but reserves remain**, the game shows *"All members of the party have fallen.
  Reform the party with one or more reserve members."* and then opens the Party Menu so the player can swap them in.
  When only the leader is lost, the same widget's request-3 path uses *"Select a new party leader."*
- **Request 18 is the field menu's world map as a stand-alone screen.** It looks the same as the menu's own map, but
  closing it returns to the game rather than to the menu.
- **The airship legs** run between Rabanastre, Nalbina Fortress, Archades, Bhujerba and Balfonheim Port, seven pairs
  in both directions (routes 1–14).
- **The default Triangle-path parameter `0x21` opens the location map.** Request 2 with parameter 0 opens the menu
  widget instead.
- **Ordinary text is spaced glyph by glyph; numbers are spaced evenly.** The general glyph loop re-derives the advance
  from each glyph, and the number formatter derives it once from `'0'`.
- **A text reveal starts behind by its lag bound**, and the glyph run carries a pixel-test word per path.
- **The loader frees a path request's copy once on every normal path.** A second cancel of the same in-flight raw-path
  request would free it again, a latent double free that the shipped callers do not take directly.

## Proposed register rows, id-less, for SWE2-DATA (SWE2-CONTRACT for OPUS)

| # | page | question |
|---|---|---|
| P1 | ui-request-router.md | What the game-over screen shows: which shipped resources the descriptors `00D11C88` and `00D11CA0` name (loaded by `003EF830` through `00393460` and `003933F0`), and what words they draw. The widget family looks up no text id |
| P2 | ui-request-router.md | The authored name, or the setting script, of scenario flag `0x5E`, which `00253C70` tests through `0032A8A0` to choose request 2's operand-word parameter |
| P3 | ui-request-router.md | What state bit 12 of the battle-system flag dword `[02EBF190] + 4` denotes. Writers: `00233C10` at `00233C6E`, `00239960` at `00239A35`, and `0023A390` (callers `0050F500`, the handler of verb `0x308D`, and `00584210`). It selects SpawnKeep image B in the persistence-pair capture and restore |
| P4 | ui-request-router.md | Whether field id 0, the target the area controller requests after an invalid save header (`00280140`, bit 8 with target 0), is the title screen |
| P5 | numeric-formatting-and-character-mapping.md | What the five outputs of `003FFC60` mean in the `.` and `-` escapes: byte 1's 7-bit field, byte 2's clamped 4-bit field and its three flags, as the number formatter `002AE610` uses them after `002AE760` |
| P6 | numeric-formatting-and-character-mapping.md | Which glyphs of the shipped fonts set bit 31 of their 8-byte glyph record (`002AA117`–`002AA16C`), which decides where the class-change gap is inserted |
| P7 | numeric-formatting-and-character-mapping.md | What the pen components `+8` and `+0xC` carry in `002AC5F0`'s `0x0E` and `*` arms, which copy them into locals at `002AC8A4` / `002AC8BD` and `002AD690` / `002AD69B`. UQ-165 found them unread on `002AE610`'s path |
| P8 | the-resource-request-queue.md | What the save-storage machine's handlers `003BA5F0` and `003BA720` do, and which of `003BB790`'s ten substates reaches each of its seven handlers |
| P9 | the-resource-request-queue.md | Can a kind-`0xFF` request id be cancelled twice while in state 4, so that `0032E590` frees its path copy a second time (`0032E5CB`, before the state test at `0032E5D0`)? Its direct callers are `002FC3C0`, `003B1310`, `003B1710` and `003B18E0`; the raw-path users are `003306E0`, `003319D0` and `00377DC0` |

No cell holds a literal pipe.

## Runtime-only (SWE2-CONTRACT for OPUS)

- **Router:** how long a request word stays set; the delivery order of the save controller's message 18 against the
  area controller's message 2, and whether the fullscreen widget is still in place when message 15 arrives; how many
  parses a frame runs; the `spattack` window's name, and whether it is the Quickening screen (no string names it); any
  live observation of requests 15, 18 or 19.
- **Number formatting:** why the sub-step opt-in governs the windows' confirm (the coupling is static, its purpose is
  not); which limit the 1920-unit render strip serves.
- **Queue:** service issuance, completion and loading-state timing (OV-19 / OV-33, already carried by
  `FABLE-REQ-ASTRA-RT-REMAINDERS-0929`); which requests run during an active BGM stream; the page alignment of the
  three EO-3 crash values (`FABLE-REQ-ASTRA-EO3-PATH-POINTER`).

## Proposed status lines (SWE2-CONTRACT for OPUS)

No status word is moved; these are for OPUS's owner read.

- **ui-request-router.md** (current line unchanged): `PARTIAL — UQ-162 answered 2026-09-25 (…unchanged…); the state
  block's owner (UQ-163 …) answered 2026-09-17; residue read 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13, §7b):
  request 24's text and Party Menu hand-off, request 18's close, the word's clearer, the airship legs, request 2's
  parameter; open only as proposed rows P1–P4 (game-over wording, flag 0x5E, bit 12, field 0) and runtime-only items`.
- **numeric-formatting-and-character-mapping.md** (residue clause rewritten in place): `PARTIAL — on-screen column
  parity (AC-10 …) and the written fields' meanings (UQ-173 …) are answered …; …`, plus, for OPUS to add: `residue read
  2026-09-30 (DD batch 13, §15): +0xA6, +0xB8, per-glyph spacing; open only as proposed rows P5–P7 and two runtime-only
  items`.
- **the-resource-request-queue.md** (residue clause rewritten in place): the four outside items are named with their
  bounds (EO-3, OV-19 / OV-33, OV-36, DD batch 6, the music-control page) and the path copy's lifetime is read (§7b);
  open as proposed rows P8–P9 and the runtime-only items.

## Receipts (SWE2-CONTRACT for OPUS)

Static work on the certified shipping image (`73461d08…`) through `retool.py`, the US text files of the game extract
resolved by the method of `_index/candidates/gi-0929-dialogs/gi13_saveload_states.py`, and the shipped
`myoshiok/us/worldmap/menumap_world.bin` with `test_battle/us/binaryfile/menu_mapname.bin`.

| script | result |
|---|---|
| `b13_checks.py` (`b13_checks.out`) | R1–R14, N1–N7, Q1–Q2: 239 PASS, FAILS 0 |
| `documented_rule.py` (`documented_rule.out`) | `TALLY PARTIAL=1 READY=2 of 3`, FAILS 0 |

Controls and blind spots:
- **Text:** the resolver reproduces `0x87E` "Save complete." (gi13's control), `0x82E` (UQ-299's control) and `0xC03`
  (this page's own help-line reading) before it is trusted on `0x86E` / `0x86F`.
- **World map:** node 1 reproduces `decode_menumap.out.txt`'s "60100 Rabanastre", and the link table reproduces the
  page's fourteen routes and the self-link at node 22.
- **R5** finds the `cmp eax, 7` at `002817B3` with the same instruction scan that finds no compare of the kind fields
  with 7. Scans see displacement operands only; a kind read through another addressing form would escape.
- **R9 and Q1** are displacement censuses (`+0x598`, `+0x24`). A store through a rebased pointer or a block copy is
  outside them, and Q1's free census is limited to the slot code `0032E000`–`0032ED00`.
- **N2:** that `0x3001` and `0x30000` are particular pixel tests rests on the glyph-run page's reading of code `0x47`
  and its PS2 register correspondence, which that page calls corroboration. The checker pins only where the word goes.
- **Q1** is call-level for the cancel's reachability; it does not follow ids through memory (P9).

## Effect on the documented rule, and things left untouched (SWE2-CONTRACT for OPUS)

- **The queue page now reads PARTIAL under `documented_rule.py`** (it read READY before the batch). The brief asked for
  the four bounds to be named, and two of them are OV-19 and OV-33. Both are PARTLY ANSWERED: their static parts are
  closed, and the runtime remainder stays OPEN under FRONTIER's 2026-09-29 runtime rule. The rule's check L counts any
  live id in the body. This is the honest reading, since the page's live-scheduling item is exactly that open remainder.
  Whether that remainder belongs to the service pages rather than this one is OPUS's call; the ids were not hidden to
  keep the page READY.
- **Routed, not edited:** `the-world-tick-and-the-field-frame.md` (stage 3 / 18) repeats the request-24 reading this
  batch corrects. Register AC-9's "fixed pitch per call, set by the callers" holds for the formatter only. Both are in
  `consumer-check.md`.
- **Not touched:** `CONTRACT-resource-request-queue.md` §14 lists the same four items; the file is dirty with another
  party's edits (as in batch 6). No register row was added or changed.
