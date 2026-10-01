# DD prose-residue closure, batch 20: the map screens and the request router (SWE2-CONTRACT for OPUS, 2026-10-01)

Request: OPUS, DD prose-residue closure batch 20. A Claude session ran the batch in the SWE2-CONTRACT lane, started by
OPUS, with no subagents and no commits. Board task `SWE2CONTRACT-DD-B20-1001` (kind research): added at revision
44400, claimed at 44402.

Both pages already pass `documented_rule.py` (READY), but they still carried prose residue with no register id, which
blocks OPUS's owner re-status:

1. `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md` (1,338 lines, CRLF on every line).
2. `16-UI/Request-Router/ui-request-router.md` (961 lines, LF on every line).

**Search.** The residue sentences were found with
`grep -n -i -E "not read|unread|not yet|not established|still open|remains open|unknown|not settled|not traced"`.
A second pass added `not identified|not proven|stays open|not found|not located|not claimed|unproven|not named|not known|does not read|not followed|probably|runtime-only|by inference|inferred`.
Struck text was skipped, and so were lines that already carry an answer note. Each remaining sentence was read in
context.

**Edits.** Both pages were clean at HEAD before the edit. `git diff --numstat` gives 23 / 23 for the map page and 9 / 9
for the router page. Each removed line is one that was rewritten in place: the original text is kept and a dated note
is inserted at the end of the sentence. Every added line keeps its page's line ending (`b20_checks.py` Z4), and the
line counts equal HEAD's (Z5). The edits are made by
`Database/Tools/work/SWE2-CONTRACT/b20_edit_pages.py`, which is idempotent (a second run applies 0 edits).

**Two statements are struck**, both on the map page and both about `003BC160`: the section 4 row (line 333) and the
interior citation (line 1294). See [`consumer-check.md`](consumer-check.md). No status word was moved, and no
register row was edited.

Legend:

- **RESIDUE, answered**: open and in scope, and answered here from the shipping image.
- **STALE**: already answered elsewhere on the page or in the register. The sentence gets a dated pointer.
- **LIMIT**: a bound on a claim, not an open question. The sentence is marked as a stated limit.
- **ROW**: a genuine open question that the image cannot settle. It is proposed below as an id-less register row.
- **already noted**: the sentence already carries a later answer or disposition, so it was left alone.

## Answers first (SWE2-CONTRACT for OPUS)

In player terms first, then the evidence. Every item is pinned by `b20_checks.py` (37 checks, FAILS 0).

1. **The track map always opens on the first marker in its list.** Following a link on the location map opens the next
   map on the marker the link names. The track map tests the same container word, `+0x179DE`, but nothing on the track
   side ever writes it.
   - The container comes from the widget factory `00244F50` (`002B63A0`). The factory hands every new object to
     `002465F0`, which clears all `0x179E0` bytes with `memset` (`00246626`; the IAT slot `008C2A60` imports
     `VCRUNTIME140!memset`) before it installs the procedure (A1-A4).
   - Image-wide, the only stores at `+0x179DC`-`+0x179DF` are the location page's two (`002BB921`, `002BB928`) (A5).
     The control is that the same census reproduces the page's 109 sites and 49 stores at `+0x179D2` (A5c).
2. **The track map is closed from four places, and the arm-10 close is not one of them.** `002B6260` has five direct
   call sites (B1-B4):
   - the input arbitration `00253C70` at `00253C92`, taken on every call while the byte `02092750` is not 3, and at
     `00253EA4`;
   - the request reset `00252DE0`, whose first call it is; the only caller of that reset is the area unload `002628B0`;
   - `002B6140`, which releases a ready page through `00247870` and then tail-jumps into it, called from `00251F40`,
     `00254AC0` and `00255330`;
   - the arm-10 close `002B8325`, which the page already shows to be dead.

   Every path returns at once when no track container exists.
3. **The highlighted marker is the current marker.** Both marker walkers compare each node with the page's current
   marker `+0xBBC8`. That node is drawn with message 37's latched byte `+0xBBE4`, and every other node with −1 (D1-D2;
   the stack offsets are checked against each walker's frame).
4. **What separates the two icon drawers.** The bodies are 2,865 B and 2,703 B, and they make the same calls apart
   from the ones below (C1-C5).

   | | track drawer `002B8EE0` | location drawer `002BCB00` |
   |---|---|---|
   | clipping | sets the scissor directly through `00249FD0`, four times | goes through the offset-apply `002DD2F0` three times (it runs `00249EE0`, then `00249FD0`), plus one direct `00249EE0` call |
   | colour and scale | tints with `TrackMapColorR/G/B/A` | scales its icons by `BaseMapJumpIconScale` |
   | icon offset | `ExtraTrackMapJumpIconOffsetX/Y` | `ExtraLocaMapJumpIconOffsetX/Y` |
   | placement | the 512 × 448 screen, `002B6B50`, `01E0CE54` and `00900384`, plus one more `002D8530` call | none of these |
   | unnamed floats | `01E0CE78` and `01E0CE7C`, which have no layout key, read as integers | none |

   Both drawers call the same three scans: `003BC160`, `003BDCD0` and `003BDB30`.
5. **What `003BC160` looks for, corrected.** It is a scan with three gates. It walks row 0 of the chunk at `02CA6C68`,
   which is the quest-menu `QHD0` chunk. The hit is the first entry whose kind is 1 **and whose bit is set**. That bit
   comes from the entry's first bitfield, at `003BC260`'s result divided by 5. The hit passes its word `+4` to
   `003C0380`, and the scan stores **a dword at `02B457D8`**, whether the hit is past entry 0 (E1-E7).
   - The page said `[+0x34]==0` and `02B457DC` in section 4, and "byte `02B457D9`" in its interior citation. Both are
     struck.
   - Nothing references `02B457D9`-`02B457DF` at all. The only writers of `02B457D8` are `003BC247` and `002BAD7F`
     (E5).

**The router page needed no new reading.** Batches 13 and 15 answered its static residue. This batch adds pointers
and marks the stated limits. Two items remain that only the running game can settle, and both are proposed below as
register rows Q1 and Q2. It also reads two bodies in passing (F1-F2): `00290450` and `00428F30`.

## Tally (SWE2-CONTRACT for OPUS)

| page | RESIDUE, answered | STALE, pointer added | LIMIT | ROW | already noted | not residue |
|---|---:|---:|---:|---:|---:|---:|
| the-map-screens-and-their-shared-map-data.md | 6 (M5, M8, M9, M15, M17, M22) | 15 | 1 (M6) | 0 | 4 | 4 |
| ui-request-router.md | 0 (two bodies read in passing, R3) | 3 (R1, R3, R5) | 2 (R2, R9) | 4 sentences (R4, R6-R8) to 2 rows (Q1, Q2) | 8 | 4 groups |

Each sentence is counted once, by its main disposition; the tables give the mixed cases (M7, M15, M20, R1, R3, R7,
R8). Line numbers are those after the edit. They are unchanged from HEAD, because notes are added in place.

### Map page (SWE2-CONTRACT for OPUS)

| # | line | sentence | disposition | source | checks |
|---|---|---|---|---|---|
| M1 | 31-32 | lede: "Not read: what each page draws, who drives the field-time preloader (§2.6), and the role of most members." | STALE | UQ-156 ANSWERED 2026-09-26; MS-4 ANSWERED 2026-09-30; §4 | P1 |
| M2 | 46 | "What each screen draws is not read (§7)." | STALE | UQ-156 | P1 |
| M3 | 143-144 | "the half of `UQ-156` that stays open." | STALE | UQ-156 | P1 |
| M4 | 208 | "`003C21B0` (a tail call to `003C2210` on the widget, not read)" | STALE | §4 row `003C2210` (releases both slots) | P2 |
| M5 | 333 | §4 row `003BC160`: "`[+0x34]`==0, writes `02B457DC`" | RESIDUE, answered, with a correction (struck) | this record | E3-E5, Z2 |
| M6 | 812-813 | "What `word[+0x44]` holds at run time is not read." | LIMIT | the word is in the loaded resource's header (`[[+0x130]+8]+0x20`), which makes it file data; no claim on the page rests on its value | - |
| M7 | 819-820 | "*Still unread:* what the two drawers ... put on screen, element by element, and arms 1, 2, 10 and 14 beyond their callees." | STALE for the arms (read 2026-09-26 below); RESIDUE, answered for the drawers (M9); LIMIT for a draw-call-by-draw-call account | the narrowings below; this record | C1-C5 |
| M8 | 823-824 | "it is probably the highlighted marker." | RESIDUE, answered | this record | D1-D2 |
| M9 | 834-835 | "How the two drawers differ inside is not read." | RESIDUE, answered (a census of callees and globals) | this record | C1-C5 |
| M10 | 836 | "*Still unread:* arms 1, 2, 10 and 14 beyond their callees." | STALE | narrowings of 2026-09-26 | - |
| M11 | 853-855 | "*Not established:* what `00254560`'s case 1 tests, and ... bit 11 ... arms 1, 2 and 14 remain." | STALE | the location arm-10 reading (`00254560(1)` is 1); MS-1 | P1 |
| M12 | 881 | "*Still unread:* the location map's arm 10, and arm 14 on both pages." | STALE | narrowings of 2026-09-26 | - |
| M13 | 974 | "Not traced here: who re-opens the page after the link's close, and who clears `+0x179DE`." | STALE | the next narrowing (bits 7 and 9; never cleared) | - |
| M14 | 995-996 | "*Still open on UQ-156:* bits 9–11, the reopen after a link, and what each page draws" | STALE | MS-1, the next narrowing, UQ-156 | P1 |
| M15 | 1017-1018 | "Which of those fire is not traced here." | RESIDUE, answered (the callers and their guards); LIMIT (which one closes a given map in play) | this record | B1-B5 |
| M16 | 1036-1037 | "*Still open on UQ-156:* ... `003C1DF0` and `003BD890` ... who clears `+0x179DE`." | STALE | the next narrowing | - |
| M17 | 1053-1054 | "initial contents, which this page does not read (the allocation's zeroing is not traced)." | RESIDUE, answered | this record | A1-A5c |
| M18 | 1055-1056 | "*Still open on UQ-156:* ... the container's lifetime (who destroys `0209E5F0`)." | STALE | the lifetime narrowing | - |
| M19 | 1076-1077 | "*Still open:* what the track map's own drawing adds ..., and the location container's lifetime." | STALE | the next narrowing | - |
| M20 | 1146-1149 | UQ-157 box: "What the values *mean* is one hop further and is not claimed." | STALE for kinds 1, 2, 3 and 7 (router §7, §7b R5); LIMIT for kind 6 and the dword | router page | P1, P2 |
| M21 | 1210-1211 | falsification pass 1: "**Not attacked, and not claimed:** what each page draws, the field-time preloader's driver, and the role of most members" | STALE | UQ-156, MS-4, §4 | P1 |
| M22 | 1294-1295 | `003BC160` citation: "sets byte `02B457D9`"; "What the predicate scans for stays open with the page's boxes." | RESIDUE, answered, with a correction (struck) | this record | E1-E7, Z2 |
| - | 747 | "what the four large arms draw is the residue" (2026-09-18 narrowing) | already noted | the UQ-156 box: ANSWERED 2026-09-26 | - |
| - | 935 | "~~*Not established:* ... bits 9, 10 and 11~~" | already noted | MS-1 | - |
| - | 1116 | "~~which ancestors can be released is not read here.~~" | already noted | MS-3 | - |
| - | 242 | "~~Whether each gate id ... was not checked.~~" | already noted | checked 2026-09-18 | - |
| - | 801 | "(the controlled character, by inference)" | not residue (a labelled inference) | the selection builder `0035BC50` is read on the battle-mode ladder; the page does not claim more | - |
| - | 804 | "~~that meaning is inferred~~" | not residue (struck, corrected 2026-09-26) | - | - |
| - | 1067 | "A record that is not yet listed" | not residue | a description of the merge | - |
| - | 4 | front-matter status: "MS-4 open" | not residue (front matter) | stale against MS-4 ANSWERED; the proposed status line replaces it; front matter is not edited here | - |

### Router page (SWE2-CONTRACT for OPUS)

| # | line | sentence | disposition | source | checks |
|---|---|---|---|---|---|
| R1 | 36-37 | "What is still not read is the game-over screen's wording (request 11) and the `spattack` window's title (request 12)" | STALE for the game-over wording (§7c P1); ROW Q1 for the title | §7c P1; Q1 | P2 |
| R2 | 193-194 | "how long the word stays set is runtime-only" | LIMIT | §7b R1: set by `00252B46`, cleared by `00252D90` or `00252DE0`; the frames between them depend on the player | - |
| R3 | 215-216 | "(the bodies of `0035BC50`, `0028FD70`, `00290450`, `00290500` and `00428F30` are not read there)" | STALE for `0035BC50`, `0028FD70` and `00290500` (the battle-mode ladder); RESIDUE, answered in passing for `00290450` and `00428F30` (their shapes); LIMIT (no claim rests on their insides) | ladder page; this record | F1-F3 |
| R4 | 335-344 | "The widget's procedure at message 15 and the delivery order are runtime-only." | ROW Q2 | Q2 | - |
| R5 | 487-488 | "Which screens 2, 15, 17, 18, 19 and 22 open is not named by these arms." | STALE | the narrowings below (2026-09-18, 2026-09-25); §7b R7 | P2 |
| R6 | 519 | "Runtime-only: the name needs the screen seen." | ROW Q1 | Q1 | - |
| R7 | 536-543 | "whether the `spattack` window is the Quickening screen ... and any live observation, are runtime-only." | ROW Q1 for the Quickening question; LIMIT for "any live observation" (a statement of the evidence's scope) | Q1 | - |
| R8 | 617-620 | §7b "**Runtime-only**" paragraph | ROW Q1 and Q2; LIMIT for the request word's duration and the number of parses per frame; the observation of 15, 18 and 19 is a scope statement (no native producer, §7b R13) | Q1, Q2 | P2 |
| R9 | 883-885 | "How many parses a frame runs depends on the windows on screen and is runtime-only." | LIMIT | - | - |
| - | 88 | table row 18: "what kind 7 changes is not read" | already noted | §7b R5 (batch 13) | - |
| - | 303-305 | "**Not established:** that nothing else writes `+0x598` ..." | already noted | batch 13 (R9, L-13) and batch 15 (§7c P3) notes on the same paragraph | - |
| - | 335-338 | "**Not established:** ... what the native callees ... do, and whether field `0` is the title." | already noted | the callee pointers and §7c P4; the runtime half is R4 | - |
| - | 469 | "*Not established:* what the menu handler makes of `0x21` ..., and the authored name of flag `0x5E`." | already noted | §7b R7, §7c P2 | - |
| - | 495 | "What kind 7 changes inside the map is not read." | already noted | §7b R5 | - |
| - | 538 | "**Not established:** the aerodrome names ...; what kind 7 changes; which native path ... issues 15, 18 or 19" | already noted | the batch-13 note: R6, R5, the producer census | - |
| - | 808 | UQ-163 box: "... is unknown." | already noted | UQ-163 ANSWERED 2026-09-17 | - |
| - | 867 | "**Not established by this join:** what `002AF340` returns ... and what `00916548` contains." | already noted | batch-13 pointer (EXP-208; the text-control contract) | - |
| - | 12 | front matter "unresolved fall" | not residue (front matter, provenance) | - | - |
| - | 83, 93, 365 | table cells "~~on-screen wording unread~~", "~~unread~~" | not residue (struck and corrected by batches 13 and 15) | - | - |
| - | 164, 182, 205, 717, 837 | struck "unread" / "not followed" / "not established" | not residue (struck, with answers) | - | - |
| - | 943, 951 | "No caller was traced" (the 2026-09-16 heading) | not residue (narrates the earlier state of a finding) | - | - |

## Proposed id-less rows (SWE2-CONTRACT for OPUS)

For SWE2-DATA, the register's owner. This batch does not edit the register.

| # | question | static floor (what the image already says) | disposition |
|---|---|---|---|
| Q1 | What the `spattack` window (request 12) shows on screen, its title and wording, and whether it is the Quickening screen | It is opened only by ScriptVM verb `0x2A8` through `002E1AE0`, and only `plan_master/us/event/spc_z/spc_z0000/spc_z0000.ebp` calls that verb. The router's arm `0028E970` builds a `0x760`-byte widget at `0209BE80 + 0x10FB0`. Its procedure `002D5EB0` looks up text only through `002D5170`, and the four ids there (`0x4669`, `0x466A`, `0x466C`, `0x46B4`) are control-code templates, not a title (§7b R12) | runtime: see the window while the `spc_z0000` event runs. NO ADMISSIBLE SOURCE statically, because no string in the image names it |
| Q2 | After a load, the order in which the save/load controller's message 18 and the area controller's message 2 are delivered, and whether the fullscreen widget still has procedure `0027F5D0` and context `+0x100` when message 15 arrives | The three load outcomes separate by bits 8-10, not by the menu closing (router §2); the callees are read on other pages | runtime: a trace of one autosave load and one manual-slot load |

A note for OPUS's owner read: if either row is registered OPEN, `documented_rule.py` will read the router page as
PARTIAL until the row closes. Registered with a disposition the rule accepts (for example OUT OF EVIDENCE BOUNDARY for
the static database, with the page stating the limit), the page reads READY-WITH-POINTER.

The map page has no proposed row: every remaining sentence there is answered, a pointer, or a stated limit.

## What the evidence rests on, and its limits (SWE2-CONTRACT for OPUS)

- **A5's census** reads every instruction in the extent set with a memory displacement in `0x179DC`-`0x179DF`. It
  does not see a block copy or a store through a rebased pointer (the same limit as the router's §7b R9). The control
  is the page's own `0x179D2` figures (109 / 49).
- **C1-C2 compare the multisets of callees and rip-referenced globals.** They are not a data-flow comparison. Two
  identical calls fed different arguments count as the same, so the differences listed are a floor. The names of
  `00249FD0` (the scissor setter) and `002DD2F0` (the offset-apply) come from the widget-protocol page and the
  coloured-rectangle page; C5 re-derives only the call order inside `002DD2F0`.
- **E1-E7 give `003BC160`'s structure, not its player meaning.** The `QHD0` identity of row 0 comes from the
  quest-menu detail page. What `003BC260`'s index denotes, and so which quest stage a set bit marks, is not claimed.
- **B3's guard** describes only the `00253C92` call. The guards on the `00253EA4` path (the byte compared with 1, or
  set to 1 at `00253E94`) are cited and not interpreted.
- Static only. Nothing is executed and nothing is live.

## Receipts (SWE2-CONTRACT for OPUS)

The work is static, on the certified shipping image (`73461d08…`), through `retool.py` and the image's import table
(`pefile`). It also uses the register `_index/OPEN-QUESTIONS.md`, the key-slot table, and git for the line counts at
HEAD.

| script | result |
|---|---|
| `b20_checks.py` (`b20_checks.out`) | A1-A5c, B1-B5, C1-C5, D1-D2, E1-E7, F1-F3, P1-P3, Z1-Z5: 37 PASS, FAILS 0 |
| `documented_rule.py` (`documented_rule.out`) | both pages `READY`, `TALLY READY=2 of 2`, FAILS 0 |
| `Database/Tools/work/SWE2-CONTRACT/b20_edit_pages.py` | 32 edits; a second run applies 0 (idempotent) |

run: _index/candidates/swe2contract-ddres-b20-1001/b20_checks.py at 61d916f19 (FAILS 0)

The checker's positive controls:

- A4: `0028CA30`'s known 0x80-byte clear goes through the same `memset` thunk.
- A5c: the displacement census reproduces the page's 109 / 49 at `0x179D2`.
- B5: `callers()` finds `002B6220`'s known caller.
- C3: the key table loads 226 keys and names the nine key globals.
- E5: the rip census finds `003BC247` itself.

## documented_rule verdict (SWE2-CONTRACT for OPUS)

- **map page:** `READY`, `kinds=MS-1,MS-2,MS-3,MS-4,UQ-156,UQ-158:answered`, `boxes=0 live=-`
- **router page:** `READY`, `kinds=UQ-162,UQ-163:answered`, `boxes=0 live=-`

Both pages were READY before the edit and stay READY after it. The rule reads boxes and register ids, not prose. This
batch closes the prose that the rule cannot see.

## Proposed status lines (SWE2-CONTRACT for OPUS)

No status word is moved here. These lines are for OPUS's owner read:

- **map page:** `status: DOCUMENTED — UQ-156 answered 2026-09-26 (the 0xBC08 protocol arm by arm, the four things each
  page draws, the containers' lifetime); UQ-157 answered 2026-09-15; UQ-158 answered 2026-09-17; MS-1, MS-2 and MS-3
  answered 2026-09-29 (FABLE); MS-4 answered 2026-09-30 (SWE2-STRUCT for OPUS, d526b865b); prose residue closed
  2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 20): the track container's zeroing, the track closer's callers, the
  marker walkers' substitution, the two drawers' differences and 003BC160's scan read from the image, and 003BC160's
  test and store corrected (consumer-check)`
- **router page:** `status: DOCUMENTED — UQ-162 answered 2026-09-25 (every request id has an identity or a ruling; 12
  is the spattack window); UQ-163 answered 2026-09-17; C-1 and C-2 closed and C-3 and C-4 answered 2026-09-12; prose
  residue closed 2026-09-30 (DD batches 13 and 15) and 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 20); the two
  runtime-only items are register rows <Q1 id> (the spattack window's wording) and <Q2 id> (message order after a
  load)`

On the router page, DOCUMENTED holds once SWE2-DATA has registered Q1 and Q2 with dispositions the rule accepts; until
then the line should keep PARTIAL. On the map page, the front matter's `last_reviewed` (2026-09-13) and
`crossref_clean: false` are audit fields, not prose residue, and this batch did not touch them.

## Routed, not edited (SWE2-CONTRACT for OPUS)

- **OPEN-QUESTIONS.md:** proposed rows Q1 and Q2 go to SWE2-DATA (the register's owner).
- **99-Unresolved-Residual/the-blinking-icon-and-its-atlas.md,** the SWE2-EC7-29 update: its hit test `rec[+0x14] == 0`
  contradicts the bytes (E3). Routed to SWE2-EC7 with the replacement in [`consumer-check.md`](consumer-check.md).
- **`_index/knowledge.sqlite`** still holds the old `02B457D9` text. It is derived and goes to OPUS for regeneration.
