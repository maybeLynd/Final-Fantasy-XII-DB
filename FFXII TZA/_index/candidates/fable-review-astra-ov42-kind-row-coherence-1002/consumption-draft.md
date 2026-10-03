# Consumption draft: ov42-kind-row-coherence (FABLE, 2026-10-02)

*Paths in this draft are plain backticked text. When FABLE applies the edits, it turns the packet and record paths in
the proposed page text into page-relative links in the page's usual style.*

This draft is for FABLE to apply. Nothing in it has been applied yet. Its scope is the accepted claims of
`_index/candidates/fable-review-astra-ov42-kind-row-coherence-1002/REVIEW.md`, with the review's seven narrowings, at
the stated limits. It was drafted against the availability page at `b128c3a2c` ("FABLE: both standard and
special-sequence routes hand the slot allocator an unbounded word ..."). That commit contains the 2026-10-02 FABLE
subsections, which earlier sat uncommitted in the working tree. The repository HEAD was `36d76cacb` when the draft was
written, and the page had no working-tree changes. The page has CRLF line endings. If
`git log -1 --format=%s -- <page>` no longer names `b128c3a2c`, re-read the page before applying.

The request asks FABLE to incorporate the full-32 classifier band versus the low-16 queue distinction and the exact
conditional band, and to leave natural kind-to-row, caller and owner consistency OPEN. Edits 1-3 do that on the
availability page. OPUS owns the exact quotient, width and descriptor preconditions and the return-use distinction;
those are routed with suggested text.

## Candidate pages and who leads them

The lead counts come from `git log --format=%s -- <page> | cut -d: -f1 | sort | uniq -c`.

| Page | What it says | Commit subjects by prefix | Lead | Action |
|---|---|---|---|---|
| availability page (`Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`) | queue-writer subsection limits: "The kind cell's writers and persistence are not read. ASTRA's later packet `ov42-kind-row-coherence` (`d83287255`) bears on this and is not yet reviewed." | FABLE 9, OPUS 2, the rest 1 each | **FABLE** | edits 1-3 (below) |
| type store `_types/fields.tsv` (`AuthoredTableHeader` `+0x08` recordStride, `+0x0C` recordArrayRef) | the sequence-queue route added the queue arm's divide readers | OPUS leads (see the sequence-queue draft) | **OPUS** | **route to OPUS** (suggested text below) |
| mode-ladder page (`Database/FFXII TZA/00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md`), the `022C215C` row of the special-sequence table | "the kind - from the action id through a 128-byte table ... **7** every other id in the range (and any id above `0x113`)" | Database 10, OPUS 4, FRONTIER 4, SWE2-CONTRACT 2, FABLE 2 | Database | **agrees** on every kind in 148..275. It leaves out that q below `0x94` also publishes 7, and the kind comes from a row quotient, not the id itself. Noted below; no edit proposed |

The regressions for edits 1-3 are `rv_kindrow.py`'s guard, per-target, map, store, entry-gate, return-use, queue
re-read and census checks, plus its emulated sweep, invariant and countermodel checks, with controls 1-18.

## Edit 1 (FABLE page): the queue-writer limits no longer leave the packet unreviewed

Subsection: "FABLE 2026-10-02: what the special-sequence queue store writes (OV-42)". Section: **Limits kept**, the
first bullet.

OLD (as at `b128c3a2c`):

```
- Kind-to-row, caller and owner consistency stays OPEN. A normal kind-4 call is not shown to carry a row in the
  usual Quickening range. The kind cell's writers and persistence are not read. ASTRA's later packet
  `ov42-kind-row-coherence` (`d83287255`) bears on this and is not yet reviewed.
```

NEW:

```
- Kind-to-row, caller and owner consistency stays OPEN. A normal kind-4 call is not shown to carry a row in the
  usual Quickening range. ~~The kind cell's writers and persistence are not read.~~ ASTRA's later packet
  `ov42-kind-row-coherence` (`d83287255`) bears on this ~~and is not yet reviewed~~. *(narrowed 2026-10-02, FABLE:
  the packet is reviewed, and the kind cell's direct writers are now counted; its persistence is still not closed -
  the kind-band subsection below)*
```

The struck phrases are the page's own text.

## Edit 2 (FABLE page): the dispatch sentence names where the kind comes from

Subsection: "FABLE 2026-10-02: which action rows the special-sequence path could turn into a rejected request
(OV-42)". The paragraph after **The request needs two gates open**, its last two lines.

OLD:

```
  `00306760`'s six-way dispatch (`003067AA`) switches on the kind `022C215C`, not on `+0x1E`. Only its kind-4 arm
  writes the queue (FABLE 2026-10-02, the special-sequence queue-writer subsection below).
```

NEW:

```
  `00306760`'s six-way dispatch (`003067AA`) switches on the kind `022C215C`, not on `+0x1E`. Only its kind-4 arm
  writes the queue (FABLE 2026-10-02, the special-sequence queue-writer subsection below). When both gates are
  open, `00306BD0` publishes that kind from its own full 32-bit row quotient (FABLE 2026-10-02, the kind-band
  subsection below).
```

## Edit 3 (FABLE page): new subsection at the end of the page

Append it after the page's current last line, with one blank line between. At `b128c3a2c` that line is
"- Whole OV-42 stays OPEN." (the queue-writer subsection's limits).

```
### FABLE 2026-10-02: which quotients publish kind 4, and what that binds in the queue (OV-42)

*From ASTRA's packet `ov42-kind-row-coherence` (`_experiments/evidence/ov42-kind-row-coherence/README.md`,
`d83287255`; method addendum `19e732aa6`), reviewed by FABLE ACCEPT-WITH-NARROWING (record
`_index/candidates/fable-review-astra-ov42-kind-row-coherence-1002/REVIEW.md`, 75 checks, 0 FAIL, 18 controls).
Static, plus an emulation of the original classifier and of the queue's kind-4 arm on synthetic rows, descriptors
and stubbed callees.*

- **The classifier `00306BD0` (three chained `.pdata` records, 440 bytes).** Its 284 code bytes end at its last
  `ret` (`00306BD0` + 0x11B). Seven DWORD jump entries (+ 0x11C) and 128 selector bytes (+ 0x138) follow. They are
  data, not code.
- **When it publishes.** Only past the two gates above. It then records its RCX as the owner in `022C2168`, sets
  `022C2160` to 2, computes the kind, stores it as a DWORD to `022C215C` and returns 1. The owner compare tests the
  unit, not the row.
- **The quotient is full 32-bit.** The row is the classifier's incoming RDX. It computes
  q = ((low32(row) - low32(base)) mod 2^32) / u16 stride with an unsigned 32-bit `div`. The key comes from the
  first load of `02EBF138` and the stride from a second load after the lookup call; there is no zero test. This is
  the same shape as the queue arm (subsection above). The full EAX then goes through `add eax, -0x94` and an
  unsigned `cmp eax, 0x7f`. Nothing narrows q to a WORD first.
- **The kinds.** For q = 148..275 a selector byte picks one of seven entries: 148 -> 5, 149 -> 6, 150..181 -> 7,
  182..207 -> 3, 208..225 -> 4, 226..261 -> 7, 262..274 -> 1, 275 -> 2. Every other 32-bit q, including 0..147,
  publishes 7. **Kind 4 is published exactly for q = 208..225.** Kind 3 has no arm of its own: it is the 3 that
  the routine loads into EBX at its start, and it survives five calls only by the Win64 ABI.
- **The full-32 / low-16 split.** The queue arm narrows its own quotient to 16 bits before its FFFF test and its
  `- 0xD0`; the classifier does not. So q = 65744 (`0x100D0`) publishes kind 7, while the queue arm would read it
  as 208 and queue 0 (emulated).
- **The `0032FC30` result is unused.** On the publishing path nothing reads that call's RAX or flags. The next
  call is a 16-byte leaf whose first instruction overwrites RAX, and the descriptor load after it writes RAX again.
  This concerns return use only. It does not show the request's native effect or success.
- **The kind cell's direct writers.** In a census of rip-relative and image-base-relative accesses, only the
  classifier writes a nonzero kind. Two end-of-sequence routines zero kind and state together with one 8-byte
  store each, then clear the owner. The two readers are the queue routine's dispatch and the finisher's kind
  dispatch. The queue routine never reads the owner cell. Register-based, aliased and indirect writes are not
  covered.
- **The two rows come from different routines.** The classifier's one direct caller is `0030CE10`, which passes its
  own incoming row unchanged; `0030CE10`'s one direct caller is `0030CBE0` (first subsection). The queue routine's
  one direct caller builds its row separately (queue-writer subsection). Indirect callers are not covered.

**The conditional invariant.** Suppose the queue routine's dispatch still reads the kind 4 that this classifier
published, and the queue arm's quotient equals the classifier's. Then q is 208..225, its low 16 bits are q, and the
queue DWORD is q - 208 = 0..17. Ids 511..534, which queue as 303..326, are then excluded on this leg. Equal row
low32, equal base low32 and equal positive strides are enough. Equal quotients alone are also enough, so pointer
identity is not needed. Neither equality is established for a normal call. Two supplied states mark the limits:
a kind-4 publication at q 208 followed by a queue quotient of 511 queues 303, and q 65744 publishes kind 7 but
queues 0. Both are arithmetic run through the original bytes in emulation, not native runs.

**Limits kept.** These limits are ASTRA's and FABLE's.

- Natural kind-to-row, caller and owner consistency stays OPEN. The two quotients come from rows built in
  different routines, at different times, from separate descriptor reads. No natural-impossibility claim is made
  for 511..534.
- The kind's persistence between the classifier and the queue dispatch is closed only for direct writes. Re-entry
  between the two is not read.
- The descriptor's initialization and its stability between each pair of loads and across calls are premises. So is
  a positive stride: a zero WORD faults after state 2 and the owner are written (a source prediction).
- The native effects of `0032F6E0`, `00309230`, `0032FC30` and `0020E600` are not read. The Win64 ABI, which
  preserves RSI and RBX, and valid, readable, stable row and descriptor state are premises.
- ASTRA's later packet `summon-kind-row-carrier` (`c40b24340`), on the queue routine's row carrier, is not yet
  reviewed.
- Whole OV-42 stays OPEN.
```

### Citations and the neighbour gate

The new text cites eight functions: `00306BD0`, `00306760`, `0030CE10`, `0030CBE0`, `0032FC30`, `0032F6E0`,
`00309230` and `0020E600`. All of them are already cited on the page at `b128c3a2c`, so none is new. The other
8-digit tokens are the data cells `022C215C`, `022C2160`, `022C2168` and `02EBF138`, all already on the page, and none
of them is `.text`. Every interior `.text` address in the new text is written as `00306BD0` + 0xNN.

These are **named by role** and not by address, so that no new caller edges are imported:

- the leaf `0032ED70` ("a 16-byte leaf");
- the two zeroing routines `00306570` (the owner-singleton release) and `003065D0` (the field-frame finisher)
  ("two end-of-sequence routines", "the finisher's kind dispatch");
- the queue routine's direct caller `00304850` ("the queue routine's one direct caller").

Their addresses are in the review record.

The neighbour pre-check (`xlayer.py`) was **not** run for this draft. Before publishing, FABLE should run
`xlayer.py --only 00306BD0,0030CE10,0030CBE0,0032FC30,0032F6E0,00309230,0020E600,00306760` (and the full-page edge
diff) on a staged copy of the page.

## Route to OPUS: quotient, widths, descriptor preconditions and return use

The packet assigns OPUS the exact quotient, width and descriptor preconditions and the return-use distinction.
Placement is OPUS's choice. Suggested text:

```
- AuthoredTableHeader inverse reader, third site (FABLE review of ASTRA `ov42-kind-row-coherence`, 2026-10-02,
  _index/candidates/fable-review-astra-ov42-kind-row-coherence-1002/REVIEW.md):
  - 00306BD0 + 0x92 .. + 0xB2 inverts its incoming RDX row: D = (low32(row) - low32(0020E600(header +0x0C)))
    mod 2^32 (`sub esi, eax`, 32-bit), then an UNSIGNED 32-bit `div` by the zero-extended u16 header +0x08 (EDX
    zeroed first). TWO separate QWORD loads of 02EBF138 with the lookup call between: +0x0C from the first, +0x08
    from the second.
  - PRECONDITION: recordStride > 0; no zero test before the `div` (#DE in emulation, a source prediction).
  - The FULL 32-bit quotient goes through `add eax, -0x94` / unsigned `cmp eax, 0x7f` / 128-byte selector at
    00306D08 / seven DWORDs at 00306CEC; kind 4 exactly for q 208..225, every q outside 148..275 -> kind 7.
    Contrast 00306760's kind-4 arm, which narrows its own quotient to 16 bits (`cmp ax, dx`, `movzx eax, ax`).
- recordStride (+0x08) reader list: add 00306BD0 + 0xAC (divide).
- recordArrayRef (+0x0C) reader list: add 00306BD0 + 0x99.
- Return use at 00306BD0 + 0x86: 0032FC30's RAX/flags are never read; 0032ED70 (16-byte leaf, no .pdata,
  `movsxd rax, ecx` / `or qword ptr [022C6E48 + rax*8], 1`) overwrites RAX, then + 0x92 overwrites it again.
  0032F6E0's return is tested (+ 0x57); 00309230's return is 0032FC30's EDX (+ 0x82).
```

## Noted, outside this package: the mode-ladder kind row

The mode-ladder page's `022C215C` row agrees with the bytes on every kind in `0x94`..`0x113`. Two omissions remain:

- Ids below `0x94` also publish 7, because the unsigned guard wraps them above `0x7F`.
- The kind comes from the classifier's row quotient. That quotient equals an action id only for a row on the
  descriptor's stride grid.

The page is led by the Database prefix (Database 10, OPUS 4, FRONTIER 4). A qualification belongs to a later package
with its own correction record. It is not proposed here.

## Optional: register row OV-42 (FABLE, at publish time)

Append this to the OV-42 status cell and keep its current text:

```
2026-10-02 (FABLE): the classifier 00306BD0 publishes kind 4 exactly for full unsigned 32-bit row quotients
208..225 (no narrowing before its guard), while the queue arm narrows its own quotient to 16 bits; IF the queue
dispatch still sees that kind 4 AND its quotient equals the classifier's, the queue DWORD is 0..17 and 511..534 are
excluded (ASTRA ov42-kind-row-coherence, FABLE review ACCEPT-WITH-NARROWING). Natural kind-to-row/caller/owner
consistency stays OPEN.
```

Escape any literal `|` before writing it into the row.

- consumer: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md` OV-42 subsections - revised-here (edits 1-3)

affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

run: `rv_kindrow.py` at HEAD 36d76cacb (75 checks, 75 PASS, 0 FAIL, 18 controls)
