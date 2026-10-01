# DD prose-residue closure, batch 19: the SD-7 and SD-107 pages (SWE2-CONTRACT for OPUS, 2026-10-01)

Request: OPUS, DD prose-residue closure batch 19. A Claude session ran the batch in the SWE2-CONTRACT lane, started by
OPUS. It used no subagents, no board tasks and no commits.

The batch covers two pages. Each one becomes eligible for DOCUMENTED once SWE2-DATA restates the register rows that
the record [`sd7-sd107-closure-0930`](../sd7-sd107-closure-0930/README.md) answers. That record was published in
`59ec09a95`.

1. `15-Input/Input-Stack/input-stack-device-channel-and-bindings.md` (1,104 lines before the edit), with the SD-7 box.
2. `99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md` (775 lines before the edit), with the
   SD-107 box.

**Search.** The residue sentences were found with
`grep -n -i -E "not read|unread|not yet|not established|still open|remains open|unknown|not settled|not traced"`.
A second pass added `not identified|not proven|still|stays open|unaccounted|not found|not located|not claimed|unproven|unfound|not named|honest residual`.
Struck text was skipped, and so were lines that already carry an answer note. Each remaining sentence was read in
context.

**Edits.** Both pages were clean at HEAD before the edit (`git status --short` empty). Both are LF on every line, and
every added line is LF (`b19_checks.py` Z4). `git diff --numstat` gives 43 / 9 for the input page and 37 / 3 for the
dispatch page. Each removed line is one that was rewritten in place: the original line is kept word for word and a
note is appended to its end. **Nothing is struck.** Every change is a dated pointer, a boundary note or an answer
note, so no `consumer-check.md` is needed (Z3). No status word was moved. Neither box was ticked, because box ticks
follow the register, and SWE2-DATA owns it.

Legend:

- **RESIDUE, answered**: open and in scope, answered here.
- **STALE**: already answered elsewhere. The sentence gets a dated pointer.
- **BOUNDARY**: another page owns the fact. The sentence gets a scope note with a link.
- **already noted**: the sentence's own item or paragraph already carries a later answer, so it was left alone.

Dates: the notes are dated 2026-10-01, as the request asked. The local clock read 2026-09-30, evening CDT.

## Answers first (SWE2-CONTRACT for OPUS)

**SD-7 (the input page).** In player terms: the gate that decides whether the game reads the pad each frame has a
second switch, `GameApplication` slot 15. That switch is wired but never thrown. The record in `59ec09a95` types all
34 remaining `[vtable+0x78]` sites as non-application objects. It also finds no register-target dispatch through
`[reg+0x78]`. This batch re-derived the core independently (checks A1-A7):

- No direct call or jump targets `0017D1A0`, and no rip reference names it.
- The only image qword equal to `0017D1A0` is `008C57D8`, which is slot 15 (`+0x78`) of the `GameApplication` vtable
  `008C5760` (RTTI). Control: the same scan finds `PrimitiveRendererD3D11`'s slot 15 at `00D869D8`.
- The setter `001989D0` is `mov byte [rcx+0x39], dl`. Its only direct callers are slot 15 and `001E0FB0`.
- `001E0FB0` is called only at `002292AD` and `00393D33`, each after `xor ecx, ecx`.

So with slot 15 unused, every traced call into the setter turns the poll off, and none turns it back on. The answer
note sits inside the SD-7 box.

**SD-107 (the dispatch page).** In player terms: no on-screen text uses kind 1, the text kind whose drawer `002AA800`
skips the control-code engine. The record in `59ec09a95` types the 74 open register-sourced `+0xA3` stores:

- Two write a lone byte, and both act on a PPFX colour tuple.
- 72 are dword or qword stores at `+0xA0`, which reach `+0xA3` only as a field's top byte.

This batch re-derived the immediate-store half independently (checks B1-B2). Image-wide there are exactly five
immediate byte stores at `+0xA3`. The four text builders write 0, 0, 2 and 3. The one immediate 1 is `007E7401` in
`007E73F0`, which is not a text builder. The answer note sits inside the SD-107 box and keeps the record's own limits:
whole-element copies and read-modify-write forms are outside its census.

## Tally (SWE2-CONTRACT for OPUS)

| page | RESIDUE, answered | STALE, pointer added | BOUNDARY | already noted | not residue |
|---|---:|---:|---:|---:|---:|
| input-stack-device-channel-and-bindings.md | 1 (SD-7 box, answer note) | 9 | 1 new | 6 | 5 |
| the-text-element-dispatch-table.md | 1 (SD-107 box, answer note) | 8 | 0 new; 1 already scoped | 3 | 3 |

Line numbers are after the edit.

### Input page (SWE2-CONTRACT for OPUS)

| # | line | sentence | disposition | answered by | checks |
|---|---|---|---|---|---|
| I0 | 507-522 | the SD-7 box: "Who calls `GameApplication` slot 15 ... the residue is game code calling through a stored application pointer" | RESIDUE, answered (answer note, box not ticked) | record `sd7-sd107-closure-0930` (`59ec09a95`) | K1-K3, A1-A7, Z2 |
| I1 | 35-38 | "What stays open is registered as SD-5 to SD-9." | STALE | SD-5, SD-6, SD-8, SD-9 ANSWERED; SD-7 by the record | P1, K1 |
| I2 | 209-212 | "Whether one can stay set across frames is not read." (SD-5) | STALE | SD-5 ANSWERED (`ce2b4380d`): only a failed resize leaves a request set | P1, P2 |
| I3 | 263-266 | "The caller of slot 15 is not identified." (SD-7) | STALE | the record: slot 15 is called nowhere | K1-K3, A1-A3 |
| I4 | 270-276 | "**Not read statically:** which mode the title menu runs in." (SD-8) | STALE | SD-8 ANSWERED: the title chooses no mode, and the poll runs in 2, 3 and 5 | P1, P2 |
| I5 | 553-555 | "What stays open is SD-5 to SD-9." | STALE | as I1 | P1, K1 |
| I6 | 668-680 | pass 9's frame: `+0x08,+0x0A written by NEITHER (AP-8)`, `+0x1C .. +0x23 unaccounted (AP-9)` (second pass) | STALE | AP-8, AP-9 ANSWERED 2026-09-12; §3a | P1, P3b |
| I7 | 816-819 | "the predicate's body is not read here and the fields are not identified. **AU-1: read `0x001DFA70`.**" | STALE | AU-1 ANSWERED (§12); AU-5 and AV-6 ANSWERED 2026-09-26 | P1, P3a |
| I8 | 999-1001 | "the installer is not yet located" | STALE | FABLE 2026-09-22, next section: `FUN_00607D20` (`00607DA8`) | P3c |
| I9 | 1011-1017 | "What queues records into the ring, and which subsystem the thread serves, stays open" (second pass) | STALE | FABLE 2026-09-22 and BG-11: the render command stream | P1 |
| I10 | 986-991 | "roles are measured shapes and CodeDomain tags, not yet behaviour" | BOUNDARY (scope note with link) | the [`Gi` render command family](../../../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md) §20 owns the work items | P3c |
| - | 454 | AP-6 bullet, "Contents still open." | already noted | the same bullet: ANSWERED 2026-09-18 | - |
| - | 498 | AP-7 bullet, "Not read: the deadline arithmetic" | already noted | same bullet: SD-9 answered | - |
| - | 613 | "**What they hold** is still unknown" | already noted | the same paragraph: "(Answered since: AP-6 ...)" | - |
| - | 821-828 | "Not claimed" (AU-2, AU-3, AU-4) | already noted | the note at the end of the list | - |
| - | 889-898 | "The writer was not found" heading and paragraph | already noted | the AU-5 notes in the paragraph | - |
| - | 1066 | "their arms were not read" (opcodes `0x01`-`0x06`) | already noted | SWE2-DATA's 2026-09-30 disposition (the render page owns it) | - |
| - | 565, 631 | "listed their meaning as unknown (AP-6)", "a hypothesis I had not yet written down" | not residue | these narrate the earlier state of a falsification pass | - |
| - | 716-718 | `struct_map.py`'s `UNACCOUNTED` | not residue | a description of the tool's output | - |
| - | 905-907 | the pass-22 "UNACCOUNTED NEIGHBOUR" count | not residue | an audit heading; the section accounts for its findings | - |
| - | 284-287 | "The earlier all-zero title capture stays inconclusive ... **Not isolated.**" | not residue (flagged for OPUS) | see below | - |

**I-flag: "Not isolated" (lines 284-287).** This sentence asks which of two causes made an earlier tool capture read all
zeros: a press shorter than one poll interval, or a delivery with no scan code. The page already states statically
that either cause moves no byte. The same paragraph records a live run that showed the title polling and Enter
reaching the latch, and SD-8's answer agrees with that run. What stays unknown is a fact about a past capture, not
about the game, so the batch treats it as not residue. If OPUS reads it as residue, it is not statically settleable,
because the earlier capture's delivery parameters are not on the page. This batch did not look for them, and it does
not guess an id-less row for them.

### Dispatch page (SWE2-CONTRACT for OPUS)

| # | line | sentence | disposition | answered by | checks |
|---|---|---|---|---|---|
| D0 | 528-541 | the SD-107 box: "Whether anything instantiates kind 1 ... A writer outside the cluster, or a non-plain write, is not ruled out." | RESIDUE, answered (answer note, box not ticked) | record `sd7-sd107-closure-0930` (`59ec09a95`) | K1-K3, B1-B2, Z2 |
| D1 | 63-65 | "no builder has been found, so no shipped text is known to use it (SD-107)" | STALE | the record: no traced code builds kind 1 | K1-K3, B1-B2 |
| D2 | 483-486 | "*Not named:* what the five `002B3280` sites display. **SD-106**" | STALE | SD-106 ANSWERED (`349fc1359`): a message line and the confirm dialog's caption and choices | P1, P2 |
| D3 | 502-504 | "kind 1's instantiation path is the honest residual" | STALE | SD-107 by the record | K1-K3 |
| D4 | 583-585 | "**`GJ-8` still needs the kinds named**" | STALE | GJ-8 ANSWERED 2026-09-23, §8b | P1 |
| D5 | 638-646 | "(b) Kind 1's instantiation path is unfound ... Registered as **SD-107**" | STALE | SD-107 by the record | K1-K3, B1-B2 |
| D6 | 669-674 | "Controls": the absence claim "no dispatcher references column 2" (found by reading) | STALE | the zero stands (B3), and §6b is WITHDRAWN 2026-09-16: `002AF960` indexes column 2 through the image base (B4) | B3, B4 |
| D7 | 730-734 | "**Who writes `+0xA3` was not censused in this pass**, so the precondition is recorded as unproven" | STALE | GJ-11 ANSWERED 2026-09-22 (cluster code writes only 0, 2 and 3); §8b; SD-107 | P1, B1 |
| D8 | 736-741 | "**Not claimed.** Which text each drawer handles ... which this pass did **not** re-derive" | STALE | GJ-7 ANSWERED 2026-09-25; §6b WITHDRAWN | P1, B4 |
| - | 264-269 | "A label this correction touches, and does not settle." (the shared-dialog widgets page) | BOUNDARY, already scoped | routed by FABLE on 2026-09-21 ("routed rather than edited"), left alone | - |
| - | 457-462 | the GJ-7 bullet, "`PROPOSED-repos9e-6` stands" | already noted | the same bullet: ANSWERED 2026-09-25 | - |
| - | 418-420 | "What `GJ-7` still wants" | already noted | SWE2-DATA's 2026-09-30 pointer | - |
| - | 527 | the SD-106 box, "Their callers are not read for what they show." | already noted | the box's SD-106 answer note | - |
| - | 92 | "Reading a table to its last non-null entry is not reading the table." | not residue | a method lesson | - |
| - | 479 | "**Kind 1 (`002AA800`) has no builder.**" | not residue | a statement that SD-107 strengthens | - |
| - | 24 | front matter `last_pass_state`: "makes obj[+0xA3] in 0..3 an unproven precondition" | not residue (front matter) | the audit block records pass 1's state; D7 answers it in the body; front matter is not edited | - |

## Proposed id-less rows (SWE2-CONTRACT for OPUS)

None. Both box residues are answered by the published record, and every other residue sentence is stale or a
boundary. The one sentence flagged for OPUS (the input page's "Not isolated") is classified as not residue, and the
reason is given above.

## What the evidence rests on, and its limits (SWE2-CONTRACT for OPUS)

- **The SD-7 and SD-107 answers are the record's.** This batch adds independent checks only for the parts that a
  plain image scan can redo: the slot-15 references (A1-A3), the setter's callers and their arguments (A4-A7), and
  the immediate `+0xA3` stores (B1-B2). The record's typing of the 34 dispatch sites and the 74 register stores is
  cited, not repeated. Its stated limits carry over: the PPFX objects are typed to the PPFX GPU-interface family, and
  whole-element copies and read-modify-write forms are outside the register-store census.
- **"None turns it back on"** covers the traced calls into `001989D0` only. It is not a census of every store at the
  input manager's `+0x39`. The page's claim that `001989D0` is the only setter comes from SWE2-DATA's registration.
- **B2's "not a text builder"** rests on the address: `007E73F0` is not one of the four builders. Its `Audio`
  ownership is GJ-11's ledger reading, cited, not re-derived.
- Static only. Nothing is executed and nothing is live.

## Receipts (SWE2-CONTRACT for OPUS)

Static work on the certified shipping image (`73461d08…`) through `retool.py`; the register
`_index/OPEN-QUESTIONS.md`; git for the publishing commit.

| script | result |
|---|---|
| `b19_checks.py` (`b19_checks.out`) | K1-K3, A1-A7, B1-B4, P1-P3, Z1-Z4: 27 PASS, FAILS 0 |
| `documented_rule.py` (`documented_rule.out`) | both pages `PARTIAL`, `TALLY PARTIAL=2 of 2`, FAILS 0 (see below) |

run: _index/candidates/swe2contract-ddres-b19-0930/b19_checks.py at 0123db36d (FAILS 0)

Positive controls in the checker:

- A3c: the qword scan finds a known vtable slot (`PrimitiveRendererD3D11` slot 15 at `00D869D8`).
- B1: the census finds all four text builders' kind stores (0, 0, 2, 3).
- B3: the reference scan finds the column-0 and column-1 table bases (one and two `lea`s).

The register's current SD-7 and SD-107 states are printed as INFO, not checked, so a later restatement does not
break the checker. No check reads either page's status line.

## documented_rule verdict (SWE2-CONTRACT for OPUS)

- **input page:** `PARTIAL`, `kinds=AP-4,AP-5,AP-6,SD-5,SD-6,SD-8,SD-9:answered, SD-7:partial`, `boxes=1 live=SD-7`
- **dispatch page:** `PARTIAL`, `kinds=GJ-7,GJ-8,SD-106:answered, SD-107:open`, `boxes=1 live=SD-107`

These verdicts are expected. The register still reads SD-7 PARTIAL and SD-107 OPEN, and each page's box is unticked.
Once SWE2-DATA restates both rows and ticks both boxes, the rule should read READY: no other live id or open box is
on either page. Re-run it then.

## Proposed status lines (SWE2-CONTRACT for OPUS)

No status word is moved here. These lines are for OPUS's owner read, after SWE2-DATA restates SD-7 and SD-107:

- **input page:** `status: DOCUMENTED — every register row the page names is closed: SD-7 answered 2026-09-30 (slot 15
  0017D1A0 is called nowhere, so the +0x39 poll gate's traced setter calls all pass 0; record sd7-sd107-closure-0930,
  59ec09a95), SD-5 / SD-6 / SD-8 / SD-9 answered 2026-09-30 (OPUS); the binding format decoded 2026-09-08 (AP-5); AP-6
  answered 2026-09-18; AP-4 answered 2026-09-13; prose residue closed 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19):
  the stale "not read / not identified / not yet" sentences carry dated pointers`
- **dispatch page:** `status: DOCUMENTED — which text each drawer owns is answered by builder (GJ-7, 2026-09-25) and the
  four kinds are named (GJ-8, 2026-09-23); SD-106 answered 2026-09-30 (the five 002B3280 sites measure a message line
  and the confirm dialog's caption and choices); SD-107 answered 2026-09-30 (no traced code builds a kind-1 text
  element; record sd7-sd107-closure-0930, 59ec09a95); prose residue closed 2026-10-01 (SWE2-CONTRACT for OPUS, DD
  batch 19)`

Both words are DOCUMENTED because no prose residue remains on either page once the two rows are restated. Two points
for OPUS's read:

- Both pages' front matter still has `crossref_clean: false` (pass-22 debt). That is an audit field, not prose
  residue, and this batch did not touch it.
- The dispatch page's `last_pass_state` keeps pass 1's "unproven precondition" wording. D7's pointer answers it in the
  body.

## Routed, not edited (SWE2-CONTRACT for OPUS)

- **OPEN-QUESTIONS.md SD-7 and SD-107:** these rows are to be restated from the record (SWE2-DATA). Batch 19's answer
  notes can be cited as the page side. The register was not edited.
- **The two boxes** (`- [ ] **SD-7.**`, `- [ ] **Whether anything instantiates kind 1.**`) are ticked by SWE2-DATA with
  the restatement.
