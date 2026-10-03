# Consumption draft: ov42-caller-row-preconditions (FABLE, 2026-10-02)

*Paths in this draft are plain backticked text. When FABLE applies the edits, it turns the packet and record paths in
the proposed page text into page-relative links in the page's usual style.*

This draft is for FABLE to apply. Nothing in it has been applied yet. Its scope is the accepted claims of
`_index/candidates/fable-review-astra-ov42-caller-row-preconditions-1002/REVIEW.md`, with that review's seven
narrowings, at the stated limits.

**Drafted against:** the availability page at `1c4c5820f`, its last commit ("FABLE: the kind-4 classifier publishes
kind 4 exactly for full 32-bit row quotients 208..225 ..."). That commit includes the OV-42 subsections committed
tonight at `b128c3a2c` and `1c4c5820f`. The repository HEAD was `c7e2bb2a1` when the draft was written, and the
page had no working-tree changes. The page has CRLF line endings. Its last line is "- Whole OV-42 stays OPEN.", the
last line of the kind-band subsection. If `git log -1 --format=%h -- <page>` no longer prints `1c4c5820f`, re-read
the page before applying.

**Order within tonight's package:**

1. Apply this draft first.
2. Then apply the companion draft `_index/candidates/fable-review-astra-ov42-terminal-resource-helper-1002/consumption-draft.md`.
   Its subsection follows this one.
3. A sibling draft, `_index/candidates/fable-review-astra-ov42-caller-quotient-bound-1002/consumption-draft.md`, also
   appends a subsection about the same routine's latch, guard and row. If both are applied, keep that subsection for
   the latch, guard, row and bound, and shorten this subsection's first bullet to the one sentence marked below.

## What the request asks, and the answer

The request asks whether the terminal phase re-establishes the prior classifier row and owner, or uses distinct
current carriers.

**Answer:** it uses distinct current carriers.

- The terminal phase never reads the kind or owner cells.
- The sequence receives a row rebuilt at the top of the invocation from the unit's own `+0x714`.
- The target builder receives the effective-id getter's word and builds its own row.
- Under the stock-table binding, the helper between them makes no own writes for 511..534.

Edits 1-4 incorporate this. Natural pairing stays OPEN. OPUS owns the widths and the ABI/table-binding
preconditions, and those are routed below with suggested text.

## Candidate pages and who leads them

The lead counts come from `git log --format=%s -- <page> | cut -d: -f1 | sort | uniq -c`.

| Page | Bearing | Lead | Action |
|---|---|---|---|
| availability page (`Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`) | effective-id subsection names "a different callee" for the later getter call; kind-band subsection says the queue caller "builds its row separately" and leaves `summon-kind-row-carrier` unreviewed | FABLE 10, OPUS 2, others 1 each | **FABLE**: edits 1-4 |
| type store `_types/fields.tsv` (`AuthoredTableHeader` `+0x08` recordStride, `+0x0C` recordArrayRef) | three new multiply sites, 32-bit row pointers, null and stride preconditions | OPUS | **route to OPUS** (below) |
| battle-unit field map (`Database/FFXII TZA/04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`) | `+0x714` is latched at the top of the battle-action routine and bounded there by 542 | Database 28, FABLE 12, SWE2-EC7 9, OPUS 7 | noted only; no edit proposed here |

The regressions for edits 1-4 are these checks in `rv_callerrow.py`, with controls 1-15:

- the latch, guard, R15, reach, fall-through, builder-transfer, helper, sequence-leg and owner/kind-census checks;
- the builder and helper checks;
- the table check;
- the emulated carriers, phase 6/8/9, latch, ignored-return, sweep, guard, stock, arm and positive-control runs.

## Edit 1 (FABLE page): the getter's later caller is the target builder

Subsection: "FABLE 2026-10-02: where the standard-action route's slot word comes from (OV-42)". The bullet
**Other direct callers**.

OLD (as at `1c4c5820f`):

```
- **Other direct callers (raw `E8`/`E9` census).** The getter has three. One is this call. One is in a later case
  of the same routine, where its AX goes to EDX for a different callee. One is in the unit display-record builder.
  Only the first is read for the transfer. Indirect callers are not covered.
```

NEW:

```
- **Other direct callers (raw `E8`/`E9` census).** The getter has three. One is this call. One is in a later case
  of the same routine, where its AX goes to EDX for a different callee *(qualified 2026-10-02, FABLE: that callee
  is the routine's target builder, in case 9; the terminal-phase subsection below)*. One is in the unit
  display-record builder. Only the first is read for the transfer. Indirect callers are not covered.
```

## Edit 2 (FABLE page): where the queue caller's row comes from

Subsection: "FABLE 2026-10-02: which quotients publish kind 4, and what that binds in the queue (OV-42)". The bullet
**The two rows come from different routines**.

OLD:

```
- **The two rows come from different routines.** The classifier's one direct caller is `0030CE10`, which passes its
  own incoming row unchanged; `0030CE10`'s one direct caller is `0030CBE0` (first subsection). The queue routine's
  one direct caller builds its row separately (queue-writer subsection). Indirect callers are not covered.
```

NEW:

```
- **The two rows come from different routines.** The classifier's one direct caller is `0030CE10`, which passes its
  own incoming row unchanged; `0030CE10`'s one direct caller is `0030CBE0` (first subsection). The queue routine's
  one direct caller builds its row separately (queue-writer subsection), at the top of each of its invocations,
  from its unit's WORD `+0x714` (FABLE 2026-10-02, the terminal-phase subsection below). Indirect callers are not
  covered.
```

## Edit 3 (FABLE page): the row-carrier limit

Same subsection, **Limits kept**, the bullet before the last.

OLD:

```
- ASTRA's later packet `summon-kind-row-carrier` (`c40b24340`), on the queue routine's row carrier, is not yet
  reviewed.
```

NEW:

```
- ASTRA's later packet `summon-kind-row-carrier` (`c40b24340`), on the queue routine's row carrier, is not yet
  reviewed. *(narrowed 2026-10-02, FABLE: the row carrier itself is now read, from ASTRA's
  `ov42-caller-row-preconditions`, which reuses that packet's switch and table evidence - the terminal-phase
  subsection below; `summon-kind-row-carrier` as a packet stays unreviewed)*
```

## Edit 4 (FABLE page): new subsection at the end of the page

Append it after the page's current last line, with one blank line between. At `1c4c5820f` that line is "- Whole OV-42
stays OPEN." (the kind-band subsection's limits). If the sibling quotient-bound subsection has already been
appended, append after its last line, which reads the same.

```
### FABLE 2026-10-02: what the terminal phase hands the target builder and the special sequence (OV-42)

*From ASTRA's packet `ov42-caller-row-preconditions` (`_experiments/evidence/ov42-caller-row-preconditions/README.md`,
`103aa3123`), reviewed by FABLE ACCEPT-WITH-NARROWING (record
`_index/candidates/fable-review-astra-ov42-caller-row-preconditions-1002/REVIEW.md`, 68 checks, 0 FAIL, 15 controls).
Static, plus an emulation of the original bytes on synthetic units, the retained US action table and stubbed
callees.*

The routine is the battle-action routine of the effective-id subsection above, with its 13-way switch on the unit's
phase byte `+0x6B4`. The routine, its target builder and its small helper are named by role here; their addresses
are in the record.

- **One row per invocation, latched at the top.** Before its phase switch, every invocation copies the unit's WORD
  `+0x714` into a register and returns -1 when that word is above 542 (an unsigned 16-bit compare). From the same
  word it builds the sequence row: the low 32 bits of `0020E600`'s second result plus the word times the WORD
  stride, from three reads of `02EBF138`. Neither the word nor the row is reloaded later in the invocation. A null
  descriptor or a null first lookup leaves the row 0, with no guard. A later row test then reads address 0xC; that
  is a source prediction.
- **Case 9, the terminal phase.** Case 8 makes one call and falls into it. Case 9 runs in this order:
  - it calls `00387090` with the unit's `+0x698`;
  - it hands the returned AX, zero-extended, to the target builder;
  - it hands the latched word to the helper, and overwrites the helper's return without testing it;
  - for a word outside D0..F1 it calls a preview routine and then, if the row has bit 30 of `+0x0C`, `00305640` (next
    subsection);
  - if bit 30 is set at a second test, `00306760` receives the latched row.

  The builder latches its word and builds its own row from its own three descriptor reads and two lookups. It never
  reads the routine's row.
- **Two carriers, agreeing only under premises.** The builder works from the getter's word, and the sequence from the
  unit's own word at entry. They name the same row only when all three of these hold:
  - the getter's owner O2 is this unit;
  - its `+0x714` is unchanged between the routine's entry and the case-9 getter call;
  - the word is not `0x9F` with a record selected. In that case the getter returns the record's WORD `+0x10`; see
    the effective-id subsection.

  None of these is established, and the two rows come from separate descriptor reads.
- **Nothing here re-checks the classifier.** The routine has no access to the kind `022C215C` or the owner `022C2168`.
  It reads the state `022C2160` only after the sequence call. The row's bit 30 is read three times: before
  `00305640`, after it, and after the sequence.
- **What "not rerun" covers.** An invocation that enters at case 8 or 9 reaches neither the readiness call of case 7
  nor the acquire wrapper `0030CFB0` of case 6. Cases 6 and 7 fall through into 8 and 9, though. An invocation that
  enters at case 6 calls the getter twice: once for the acquisition word and once for the builder (emulated).
- **The helper on 511..534.** For words 278..542 the helper builds the row as a 32-bit pointer and tests bit 6 of row
  byte `+0x2C`. In the retained US table that bit is clear on every one of 511..534. Under a stable binding to that
  table, the helper therefore makes only its two lookups, writes nothing outside its stack and returns 0, for all 24
  words (emulated). In 278..542 the bit is set only on rows 325, 326, 416, 417, 436 and 455. Those rows reach an
  owner lookup and, except 455, an effect call. A supplied bit-6 row reaches the effect call too.
- **The builder's indirect call** has two fixed local targets. Bit 2 of the row's WORD `+0x36` picks between them, so
  it is not a virtual dispatch. Neither target is read, and neither is any of the builder's other 21 calls.

So the terminal phase does not re-establish the classifier's row or owner. It rebuilds its rows from current
carriers: the unit's `+0x714` at entry for the sequence, and the getter's word for the builder. For the queue leg
to exclude 511..534 through the kind, the classifier's row and this routine's entry word must agree, and that is an
earlier lifecycle obligation. It is not established.

**Limits kept.** These limits are ASTRA's and FABLE's.

- Natural pairing of the classifier's slot word (`0030CBE0`) and this routine's entry `+0x714` stays OPEN. So do the
  writers of `+0x714` and of the phase byte, and whether a natural invocation enters at case 8 or 9 or falls through
  from 6 or 7.
- Kind and owner persistence beyond the direct census (kind-band subsection) stays OPEN.
- The descriptor and table binding, its initialization and its stability across the calls are premises. So are
  table addresses below 4 GB (all three bodies form 32-bit row pointers) and a positive stride.
- The native effects of the getter, the builder's 22 calls, the helper's lookups and effect call, the case-8 call
  and the preview are not read. `00305640`'s own body is read in the next subsection; its callees are not. The
  Win64 ABI, which preserves the latched registers, is a premise.
- These are local normal-return CFG facts and emulation on supplied states. They are not native runs or natural
  reachability.
- No natural-impossibility claim is made for 511..534.
- Whole OV-42 stays OPEN.
```

**If the sibling quotient-bound subsection is applied in the same package**, replace this subsection's first bullet
with this one sentence:

```
- **One row per invocation, latched at the top** (the queue-caller subsection above): neither the word nor the row
  is reloaded later in the invocation.
```

### Citations and the neighbour gate

The new text cites these 8-digit tokens, and every one is already on the page at `1c4c5820f`, so none is new:

- functions: `0020E600`, `00387090`, `0030CFB0`, `00305640`, `00306760` and `0030CBE0`;
- data cells: `02EBF138`, `022C215C`, `022C2168` and `022C2160`, none of them `.text`.

Edits 1-3 add no new address.

These are **named by role** and not by address, so that no new caller edges are imported:

- the battle-action routine `00304850`;
- its target builder `0030D160`;
- the helper `00305430`;
- the readiness call `0030CA80`;
- the case-8 call `00319420`;
- the preview `00303830`;
- the helper's owner lookup and its effect call `00311F70`;
- the builder's two indirect targets.

Their addresses are in the review record. No jump-table or other `.text` data address is written; the phase table
is "its 13-way switch".

The neighbour pre-check (`xlayer.py`) was **not** run for this draft. Before publishing, FABLE should run `xlayer.py
--only 0020E600,00387090,0030CFB0,00305640,00306760,0030CBE0` (and the full-page edge diff) on a staged copy of the
page.

## Route to OPUS: widths, ABI and table-binding preconditions

The board request assigns OPUS the exact widths and the ABI/table-binding preconditions. Placement is OPUS's choice.
Suggested text:

```
- AuthoredTableHeader forward readers (multiply), from FABLE's review of ASTRA `ov42-caller-row-preconditions`
  (2026-10-02, _index/candidates/fable-review-astra-ov42-caller-row-preconditions-1002/REVIEW.md):
  - 00304850 + 0xB3 / + 0xC7 (+0x0C key into 0020E600), + 0xD9 (+0x08 stride), + 0xE1 `imul ecx, eax`,
    + 0xE4 `add r15d, ecx`: the row is zeroextend32(low32(second lookup) + id * stride), id = the entry WORD
    unit+0x714 latched at + 0x3D. The row is used as a pointer (`test dword ptr [r15 + 0xc]`), so the table must lie
    below 4 GB. A null descriptor or null first lookup gives row 0, with no guard.
  - 0030D160 + 0x59 / + 0x6D (key), + 0x7F (stride), + 0x86 / + 0x89 (32-bit add into RSI); the word is its
    incoming DX (+ 0x27).
  - 00305430 + 0x31 / + 0x46, + 0x79 / + 0x8E, + 0x162 / + 0x177 (key) and + 0x58, + 0xA0, + 0x186 (stride), three
    32-bit row builds; no null guard on the descriptor or the first lookup (a null reads address 0x2C).
- 00304850 entry guard: `cmp r13w, bx` with 0x21E, unsigned `ja` -> return -1 before the phase switch (+ 0x8E,
  + 0x92). 00305430 bounds: unsigned 16-bit `cmp dx, 0x115` and `(di - 0x116) <= 0x108` for the 278..542 arm.
- Return use: 00305430's EAX is overwritten untested at 00304850 + 0x6A3; 0030D160's EAX is not read by the
  routine (+ 0x697 rewrites EDX, + 0x69B RCX, + 0x6A3 RAX).
- 0030D160 + 0x22D `call rax`: two fixed targets, 0030BB10 (`lea` + 0x21C) and 0030BCB0 (RBP, `lea` + 0x1C6 /
  + 0x2C7), picked by bit 2 of row WORD +0x36 (skipped when bit 3 is set).
```

## Noted, outside this package

- The battle-unit field map's `+0x714` row could say that the battle-action routine latches the field at the top of
  each invocation and refuses values above 542 there. That page is led by the Database prefix, so this is noted and
  not proposed.
- SPEC reviews the exact packet per its README. This review does not replace that.

- consumer: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md` OV-42 subsections - revised-here (edits 1-4)

affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

run: `rv_callerrow.py` at HEAD c7e2bb2a1 (68 checks, 68 PASS, 0 FAIL, 15 controls)
