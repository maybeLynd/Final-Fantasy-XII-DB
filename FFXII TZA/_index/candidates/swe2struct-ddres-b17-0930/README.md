# DD residue closure, batch 17: the widget message protocol's body (SWE2-STRUCT for OPUS, 2026-10-01)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`, batch 17. The batch was run by a Claude session in the
SWE2-STRUCT lane, started by OPUS, with no subagents, no board tasks and no commits.

The page is `16-UI/Widget-Object-Model/the-widget-message-protocol.md` (LF only, 2,421 lines at the start). It was
clean when the batch started (`git status --short` empty) and was not changed in git while the batch ran.
SWE2-CONTRACT's batch 10 had answered the status line's residue (W1–W4). The body still carried sentences such as
"stay open", "not read" and "unnamed" with no register id.

The sentences were found with `grep -n -i` for *not read, unread, unresolved, not yet, not established, still open,
stay open, remains open, unknown, unnamed, not settled, not traced*. A wider pass added *gets no name, narrowed, not
named, no sender* and the section 7 ordering item. Text inside `~~strikes~~` and lines that already carry a later
answer note were set aside. No status word was moved: OPUS re-statuses after its owner read.

The edits are added notes, four strikes with corrections, and one new section at the end. The page stays LF only.
`git diff --numstat` gives 155 lines added and 5 removed; the 5 removed lines are the four struck statements (one
spans two lines), each kept verbatim under its strike.

## Dispositions (SWE2-STRUCT for OPUS)

Legend: **STALE** = already answered, so a dated pointer note was added. **BOUNDARY** = another page owns the fact,
so a pointer with a link was added. **RESIDUE** = open and in scope, answered here with checks. **carried** = the line
already has its answer or is struck, so it was not edited.

Line numbers are those of the page at the start of the batch.

### Grep set: STALE 9, BOUNDARY 2, RESIDUE 5 (all answered) (SWE2-STRUCT for OPUS)

| line | sentence | disposition |
|---|---|---|
| 38 | "honest about the ones it could not read" | STALE: no handler is left unread (DD batch 10, W1–W3). Check P7 |
| 436 | "The three individual meanings stay open and are recorded as such" | **BOUNDARY**: each screen's page reads its id. 285 is the dialog reply (licence-board widgets section 8a, GI-3), 289 is the gambit list's destroy notice to its editor child (gambit screens), and 287 is `002C9EB0`'s code message, read for the Config screen in its section 7.1. Checks P1–P3 |
| 468 / 477 | the section 5 heading "what is honestly unknown"; "Naming 1, 2, 15 and 18 … is DL-1" | STALE: all four are named in section 9, and DL-1 was answered on 2026-09-25. The heading was not edited, so its anchor is kept. Checks P6, P8 |
| 581 | "20 application senders not read" (id 16, section 9 table) | **RESIDUE, answered and corrected** (C1–C5). The 20 include the three framework senders, so the application senders are 17. Their receivers and payloads are tabled in the new section. Struck, with the two cells that repeat the count (section 4 id 16; the section 8 box) |
| 612 | "released instead of messaged — a branch the page had not read" | STALE: the bullet below reads it, and section 2a's replay observes it. Check P6 |
| 717 / 736 | "Not established here." / which snapshot readers run after the walk | STALE pointer: FABLE's static pass is done (`fable-astra-live-facts-0930`, `snap_order.py`). The remainder is run-time object state and stays under its own request id, `FABLE-REQ-ASTRA-WHERE-THE-SNAPSHOT-READERS-SIT-RELATIVE-TO-THE-ARBITER`. Check P5 |
| 836 | "fourteen ids DL-1 still listed as unnamed" | STALE: that was the 2026-09-20 count, and DL-1 has since been answered. Check P8 |
| 867–868 | "Whether any of the sixteen curve kinds does that was not read — 00248F40 is not read here" | **RESIDUE, answered** (E1–E4): no curve kind can do it (below) |
| 907 | `002B6DB0` "(same band, not read whole)" | **RESIDUE, answered and corrected** (S1–S4): struck, and the cell now lists what the arm writes. A note was added below the table |
| 984 | "what the flag distinguishes is not read" | **RESIDUE, answered** (F1–F3): 1 = the focus came back by the teardown pop, 0 = the widget took the focus by a push |
| 1089–1092 | "What is NOT established is the link … the one thing still open on message 26" | **RESIDUE, answered** (L1–L9): the two are the same object (below) |
| 1148 | "where the count is raised is unresolved and 26 keeps its narrowed status" | STALE: answered by the paragraph headed "Found" above it, and 26 was named on 2026-09-25. Check P6 |
| 1153 | "The receiver rdi is not resolved here, so 53 stays unnamed." | STALE: section 9e names 53 from its sender and both receivers. Check P6 |
| 1208 | "what 00393460 and its siblings do natively is not read here" | **BOUNDARY**: the typed-list page, section 7c (`dataface_c` through `002493D0` → `0024A4E0`; kind 7 id 111 through `00249320`). Check P4 |
| 1265 | "DL-1 stays open for the three" | STALE: all three are answered just below it on 2026-09-25. Checks P6, P8 |
| 1567 | "the bit's own author is not traced here" (`+0x40` bit `0x20`) | STALE: the page's own "Kept, then reclaimed" section reads it. Pinned here: B1–B3 |
| 4 (status), 117/122–125, 1036, 1111/1115, 1308, 1332, 1353, 1393, 1465 | the status line, the 24 UNPARSED table, "receivers still unread", the clip-suspension "still not found", the struck 26 note, "nothing remains unnamed", DL-1 superseded, DL-3 answered within its paragraph, and the falsification pass's scope | carried |
| 155–169, 520, 1256–1262 | struck UNRESOLVED or "remain unnamed" text | carried (struck) |

### Wider pass: STALE 5 (SWE2-STRUCT for OPUS)

| line | sentence | disposition |
|---|---|---|
| 526 | "Anything about ordering. Nothing here establishes when a message is sent" | STALE: section 9 covers when each message is sent, and DL-3 (answered 2026-09-13). Check P6 |
| 918–923 | "Message 30 is narrowed, not named … 30 gets no name" | STALE: 30 was dispositioned as application-defined in section 10 on 2026-09-25 |
| 925–929 | "Message 11 has no sender either instrument can see" | STALE: section 10 names the sender, `002481C0` (tail `jmp`, `.rdata` `{11}`) |
| 1006 | "26 is narrowed, not named" | STALE: named in section 10 on 2026-09-25, with the last receivers read in DD batch 10 (W4) |
| 1372–1384 | "For DL-1's remaining 11, the concrete next instrument …" | STALE: the same answer in section 10 |

**Proposed rows: none.** Every residue sentence was either stale, owned by another page, or answered statically. The
one run-time item, the snapshot-reader order, already has its request id.

## The answers, in player terms (SWE2-STRUCT for OPUS)

- **A menu slide always lands, whatever its easing curve (E1–E4).** The easing function `00248F40` returns exactly
  `1.0` as soon as the elapsed time reaches the duration. It does this before it looks at which of the sixteen curve
  kinds it was given, so no curve can leave a position tween re-sending its "stepped" message forever. The only way
  the snap test (unsigned) and the easing test (signed) can disagree is a scaled elapsed of 2^31 ticks or more. That
  happens when a start tick sits less than one duration ahead of the clock, which clears once the clock passes it. It
  also happens when the first frame that runs the channel is 2^31 scaled ticks or more after the start (about 24.8
  days at rate 1.0). The rate cannot be zero or negative: `00229E70` replaces such a value with `1.0`.
- **A window learns how it got the focus (F1–F3).** Message 8 carries 1 when the focus has come back because the
  window above closed (the teardown pop `002448D0`), and 0 when the window has just taken the focus (the push
  `002470D0`). These are the only two senders.
- **A map page's "fields changed" notice keeps its cursor in view (S1–S4).** `002B6DB0` is the track map page's
  shared command procedure, not a separate widget. When the page opens (message 14), it sets the zoom to 100, the
  metric pair and the viewport, and then tells the page "29: re-read your fields". The page hands 29 back to the same
  procedure, which rebuilds the 24-pixel cursor box and moves the cursor inside it.
- **Grid cells land where their owner places them (L1–L9).** When a screen builds its layout, a kind-8 row creates
  a grid list and makes the screen its delegate. The screen points its own `+0xD8` at that list, and the list's
  `+0xD8` back at the screen. Before each cell is placed, the list asks its owner (message 26). The owner writes the
  cell origin into the list, and the list reads it straight back. This is how the licence-screen lists slide their
  cells into place.
- **"Load finished" (16) is a shared notice (C1–C5).** The framework sends `{16, 0, 0}` when a resource batch
  completes. Seventeen functions in the game's screens reuse the id for their own completion notices, some with a
  code: 1, 8, 9 or 10 from the `0037xxxx` senders around the `[02AED490]` object and `00577180`, or a caller's code through `003BC3E0` /
  `005770A0`. The earlier "20 application senders" counted the framework's three: the scan's core band ended at
  `00249000`, just below them.
- **Bit 5 of a widget's flags marks "under a root" (B1–B3).** The root procedure sets it, attach copies it down the
  tree, and teardown keeps such a widget for the next reconcile instead of freeing it at once.

## Receipts (SWE2-STRUCT for OPUS)

Static work on the certified shipping image (`73461d08…`) through `retool.py`: its v4 extents, its reference cache
and its capstone. No archive data was needed.

| script | result |
|---|---|
| [`b17_checks.py`](b17_checks.py) ([`b17_checks.out`](b17_checks.out)) | E1–E4, F1–F3, S1–S4, L1–L9, C1–C5, B1–B3, P1–P8: **125 PASS, FAILS 0** (run: b17_checks.py at 95cf8c42f (FAILS 0)) |
| `documented_rule.py` ([`documented_rule.out`](documented_rule.out)) | `READY`, `TALLY READY=1 of 1`, FAILS 0 |
| [`consumer-check.md`](consumer-check.md) | the four strikes on this page; two consumers are routed, not edited |

Controls and blind spots:
- **C1 is the census control.** The re-implemented `widget_messages.py --senders` scan reproduces section 8's 163
  sites and 49 ids before its id-16 counts are used. It has the original's blind spots: a record whose id is written
  from a register, a non-`rdx` record, and a send by a direct call or a tail `jmp`.
- **E is read, not executed.** The early return is a single compare at the function's entry, ahead of the only read
  of the kind, so all sixteen kinds take the same path once `duration <= elapsed`.
- **L rests on two link pins, not on matching offsets.** `002432B0` keeps its owner argument in `r13`, which is
  written once (L6). The receivers copy the row's `+0x18` pointer, the very field `0029F930` stored the list in (L5,
  L7, L9). The loop needs the copied row to be a kind-8 grid row, and that comes from each screen's layout data, which
  is not walked here.
- **F names the flag from its two senders.** Which message-8 receivers act on the difference is a receiver census
  that this batch did not run.
- **S** decodes `002B6DB0`'s table and reads the id-14 and id-29 arms only. Its other arms (1, 2, 3, 10, 15, 36, 39)
  are listed, not read.
- **C5** gives each application sender's receiver and payload. What a non-zero code means is each receiving screen's.

## For OPUS: proposed status line and routed items (SWE2-STRUCT for OPUS)

- **Proposed status line** (the status word is OPUS's; this text keeps `PARTIAL` until the owner read):
  `PARTIAL — the status line's residue answered in DD batch 10 (SWE2-CONTRACT, W1-W4) and the body's in DD batch 17 (SWE2-STRUCT, swe2struct-ddres-b17-0930, 125 PASS, FAILS 0): no handler unread, every id of the 56-id recount named or dispositioned (section 10), the high band's meanings read on their screens' pages, and no residue sentence left without an answer, a pointer or a request id; documented_rule READY (was — the residue this line named is answered in place (SWE2-CONTRACT DD batch 10) …)`.
  With that, the page has no open prose residue, and DOCUMENTED is OPUS's call.
- **Routed, not edited:**
  - `widget-message-handlers.tsv` has no row for `002B6DB0`. Like `003EE420` (batch 10), it is a base procedure that
    another procedure calls with its own self and message. Its ids are 1, 2, 3, 10, 14, 15, 29, 36 and 39 (S1). The
    TSV's `002985C0` note from batch 10 is also still pending.
  - `the-widget-constructor-and-object-sizes.md`'s residual row calls `002B6DB0`'s jump table "not decoded". S1
    decodes it.
- **Bounds outside the grep set, not edited:**
  - section 9a's "What this does not claim" (the channel-2 float, the second dword of `{17, 1}` and `{23, 1}`);
  - section 9d's "What is still not shown, and is not a static question" (one widget taking 3 and 26 in one frame);
  - the residual placement row "`0028B860` … jump table present, not decoded";
  - section 9's "Whether initialisation completes with valid storage is not observed".

  Each is a stated scope bound or a run-time question, not a register question the page asks.
