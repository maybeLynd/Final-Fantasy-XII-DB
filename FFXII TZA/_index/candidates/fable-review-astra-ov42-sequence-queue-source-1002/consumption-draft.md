# Consumption draft: ov42-sequence-queue-source (FABLE, 2026-10-02)

*Links inside proposed page text are shown as `page-relative link:` paths, because they resolve from the target page, not from this folder.*

This draft is for FABLE to apply. Nothing in it has been applied yet. Its scope is the accepted claims of
[REVIEW.md](REVIEW.md), with the review's narrowings, at the stated limits. It was drafted against the availability
page at `d9bc7155d` ("FABLE: actor 25's talk-gate bits ..."). The repository HEAD was `d8dd3408b` when the draft was
written, and the page was unchanged since `d9bc7155d`. The page has CRLF line endings. If
`git log -1 --format=%s -- <page>` no longer names that commit, re-read the page before applying.

The request: replace the unread `003068D4` local producer leg with the exact kind-4 dispatch and the low-32 quotient
/ low-16 queue formula. OPUS owns the widths, the two-descriptor reads and the positive-divisor precondition. FABLE
keeps the kind-row / owner / caller consistency unresolved and does not treat it as normal candidate admission.
Edits 1-4 do that on the availability page. The OPUS preconditions are routed with suggested text.

## Candidate pages and who leads them

The lead counts come from `git log --format=%s -- <page> | cut -d: -f1 | sort | uniq -c`.

| Page | What it says | Commit subjects by prefix | Lead | Action |
|---|---|---|---|---|
| availability page (`07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`) | special-sequence limits: "`003068D4`, the `00387090` effective-id leg ... not covered"; the queue-remap bullet cites `003068CA`; "`00306760`'s six-way dispatch (`003067AA`) switches on the kind `022C215C`" | FABLE 8, OPUS 2, pass22 1, batch 26 1, batch 19 1 | **FABLE** | edits 1-4 (below) |
| type store `_types/fields.tsv` (`AuthoredTableHeader` `+0x08` recordStride, `+0x0C` recordArrayRef) | stride "read at runtime" with multiply readers; no divide reader, no positive-stride note | OPUS 519, SWE2-STRUCT 52, types 34, Types 8, db 7 | **OPUS** | **route to OPUS** (suggested text below) |
| registry page (`02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`) | the shared header: `+0x08` u16 row stride, `+0x0C` RVA via `ImageAddress_ResolveRuntimePointer` | OPUS 13, FABLE 9, Database 7, SWE2-CONTRACT 3, FRONTIER 3 | OPUS | optional OPUS placement for the same text |
| mode-ladder page (`00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md`), "The `00306760` exclusive subtree" | "`00306760` `BattleAction_UpdateSpecialPresentationSequence` (293 B)" | Database 10, OPUS 4, FRONTIER 4, SWE2-CONTRACT 2, FABLE 2 | Database | **disagrees** with the extent (911 code bytes, 936 physical). Noted below; outside this package |

The regressions for edits 1-4 are `rv_seqq.py`'s dispatch-head, table, reach, RDI, first- and second-descriptor,
two-load, remap and store checks, with controls 1-17.

## Edit 1 (FABLE page): the special-sequence limits no longer exclude `003068D4`

Subsection: "FABLE 2026-10-02: which action rows the special-sequence path could turn into a rejected request
(OV-42)". Section: **Limits kept**, the fourth bullet.

OLD (as at `d9bc7155d`):

```
- `003068D4`, the `00387090` effective-id leg and the other callers of these functions are not covered.
```

NEW:

```
- ~~`003068D4`,~~ the `00387090` effective-id leg and the other callers of these functions are not covered.
  *(narrowed 2026-10-02, FABLE: the queue store `00306760` + 0x174 is now read - the special-sequence
  queue-writer subsection below)*
```

If the effective-id draft's edit 1 lands first, the OLD is instead:

```
- `003068D4`, ~~the `00387090` effective-id leg~~ and the other callers of these functions are not covered.
  *(narrowed 2026-10-02, FABLE: the effective-id leg is now read where the standard-action route hands its
  word to the acquire wrapper - the effective-id subsection below)*
```

and the NEW strikes the first token too, then adds the second note:

```
- ~~`003068D4`,~~ ~~the `00387090` effective-id leg~~ and the other callers of these functions are not covered.
  *(narrowed 2026-10-02, FABLE: the effective-id leg is now read where the standard-action route hands its
  word to the acquire wrapper - the effective-id subsection below)* *(narrowed 2026-10-02, FABLE: the queue
  store `00306760` + 0x174 is now read - the special-sequence queue-writer subsection below)*
```

The struck token is the page's own text. `003068D4` is an interior address; the new note uses the
`00306760` + 0x174 form.

## Edit 2 (FABLE page): qualify the `003068CA` cite in the queue-remap bullet

Same subsection, **What does not exclude 511..534**, the queue-remap bullet, its first line.

OLD:

```
  - The queue remap. The queue cell `022C2178` holds `word - 0xD0` (`0030DBDA`, `0030DC7B`, `003068CA`) or -1, and
```

NEW:

```
  - The queue remap. The queue cell `022C2178` holds `word - 0xD0` (`0030DBDA`, `0030DC7B`, `003068CA`) or -1
    *(qualified 2026-10-02, FABLE: at `003068CA` = `00306760` + 0x16A the word is the low 16 bits of a row
    quotient that the routine computes, not a stored word; the special-sequence queue-writer subsection below)*, and
```

## Edit 3 (FABLE page): the dispatch sentence points at the new subsection

Same subsection, the paragraph after **The request needs two gates open**, its last line.

OLD:

```
  `00306760`'s six-way dispatch (`003067AA`) switches on the kind `022C215C`, not on `+0x1E`.
```

NEW:

```
  `00306760`'s six-way dispatch (`003067AA`) switches on the kind `022C215C`, not on `+0x1E`. Only its kind-4 arm
  writes the queue (FABLE 2026-10-02, the special-sequence queue-writer subsection below).
```

`003067AA` is the page's own interior cite (`00306760` + 0x4A); it is left as it stands.

## Edit 4 (FABLE page): new subsection at the end of the page

Append it after the page's current last line, with one blank line between. At `d9bc7155d` that line is
"- Whole OV-42 stays OPEN." (the slot-allocator subsection's limits). If the effective-id subsection has been
appended first, append after its last line instead.

```
### FABLE 2026-10-02: what the special-sequence queue store writes (OV-42)

*From ASTRA's packet [`ov42-sequence-queue-source`] (page-relative link: `../../_experiments/evidence/ov42-sequence-queue-source/README.md`)
(`0c4215736`), reviewed by FABLE ACCEPT-WITH-NARROWING
([record] (page-relative link: `../../_index/candidates/fable-review-astra-ov42-sequence-queue-source-1002/REVIEW.md`), 58 checks, 0 FAIL,
17 controls). Static, plus an emulation of the original bytes on synthetic rows, descriptors and lookup returns.*

- **The routine `00306760` (five chained `.pdata` records, 936 bytes).** Its 911 code bytes end at its one `ret`
  (`00306760` + 0x38E). A NOP and six DWORD jump entries follow (+ 0x390 .. + 0x3A8). They are data, not code.
- **The dispatch.** It loads the kind DWORD `022C215C` (+ 0x4A), subtracts 1 and compares the result unsigned with
  5. Kinds 1..6 jump through the six entries. Kind 0 and every kind above 6 (unsigned) go straight to the shared tail. Only the
  kind-4 arm (+ 0xE8) reaches the queue store (+ 0x174). In the emulation of the whole routine with the kind cell
  set to 0..7, only the kind-4 run writes `022C2178`.
- **The value.** The routine keeps its incoming RDX, the row pointer, in RDI. The kind-4 arm then works as follows.
  - It loads `02EBF138` and passes its DWORD `+0xC` to `0020E600`. It subtracts the returned EAX from EDI, a 32-bit
    subtraction: D = (low32(row) - low32(base)) mod 2^32.
  - It loads `02EBF138` again and divides D by the WORD `+8`, zero-extended, with an unsigned 32-bit `div`
    (+ 0x158). The quotient is q.
  - It compares q's low 16 bits, w, with FFFF. If w is FFFF it stores FFFFFFFF. Otherwise it stores
    (w - 0xD0) mod 2^32 to `022C2178` (+ 0x16A, + 0x174). The store is a DWORD.
  - For a row formed as base + 60 * id, ids 511..534 queue as 303..326 (emulated). These are arithmetic results,
    not native runs.
  - Quotients alias modulo 65536 before the test. w = `0xCF` also stores FFFFFFFF.
- **Two loads, no guard.** The descriptor is loaded twice, and the lookup call comes between the loads. The key comes
  from the first load and the divisor from the second. In the emulation, repointing the cell during the call changes
  only the divisor. Nothing tests the divisor before the `div`. A zero WORD faults (#DE in the emulation); that is a
  source prediction, not an observed fault.
- **The arm's other writes.** After the store, the arm writes the unit's DWORD `+8` to `022C218C`, the value the
  queue reader returns with the queue (subsection above). Every return of the routine stores 5 to `022C2160`.
- **Kind 3** computes the same full 32-bit quotient. It passes it to another callee, not to the queue.
- **The caller.** The raw `E8`/`E9` census gives the routine one direct caller. That caller is in the same
  battle-action routine as the acquire wrapper's second caller (slot-allocator subsection), and it calls only when
  row bit 30 (`+0x0C`) is set. Indirect callers are not covered.

So the local producer leg has a single bound: the kind. Whatever row the caller passes, kind 4 queues that row's
quotient through the remap. Nothing in this routine tests the row's id or category. Excluding 511..534 on this leg
needs the kind-to-row, caller and owner consistency: the kind in `022C215C` must refer to the same row this call
passes. That consistency is not established.

**Limits kept.** These limits are ASTRA's and FABLE's.

- Kind-to-row, caller and owner consistency stays OPEN. A normal kind-4 call is not shown to carry a row in the
  usual Quickening range. The kind cell's writers and persistence are not read. ASTRA's later packet
  `ov42-kind-row-coherence` (`d83287255`) bears on this and is not yet reviewed.
- The two descriptor loads are not shown to read the same, initialized descriptor. A positive WORD `+8` is a
  precondition.
- The arm's five earlier callees (four helpers and a `memset`) are opaque. The Win64 ABI, which preserves RDI and
  RBX, and valid, readable, stable row, unit and descriptor state are premises.
- No natural kind-4 call, queue consumption, command execution or rejection is observed.
- Whole OV-42 stays OPEN.
```

### Citations and the neighbour gate

Edits 2-4 cite two functions: `00306760` and `0020E600`. Both are already cited on the page at `d9bc7155d`, so
neither is new. The other 8-digit tokens are the data cells `022C215C`, `022C2178`, `022C218C`, `022C2160` and
`02EBF138`. All five are already on the page, and none is `.text`. Every interior `.text` address in the new text is
written as `00306760` + 0xNN. The page's own `003068D4`, `003068CA` and `003067AA` tokens are kept, struck or
qualified, never added.

These functions are **named by role** and not by address, so that no new caller edges are imported:

- the one direct caller, `00304850` (+ 0x6FD), named "the same battle-action routine as the acquire wrapper's
  second caller". The page already names that routine by role. Its ledger name is
  `BattleUnit_AdvanceStandardActionState`;
- kind 3's callee `0030EC00` ("another callee");
- the arm's opaque callees `00306D90`, `0030D720`, `0030D550` and the `memset` import thunk `00861EC0` ("four
  helpers and a `memset`").

Their addresses are in the review record.

The neighbour pre-check (`xlayer.py`) was **not** run for this draft. The machine was short of memory and this
task's instructions forbade it. Before publishing, FABLE should run `xlayer.py --only 00306760,0020E600` (and the
full-page edge diff) on a staged copy of the page.

## Route to OPUS: the type store, inverse reader and positive-stride precondition

The packet assigns OPUS the exact pointer and width preconditions, the divisor, the two-descriptor reads and the
queue ABI. OPUS leads the type store: `_types/fields.tsv` has OPUS 519 commit subjects. OPUS also leads the registry
page, by OPUS 13 to FABLE 9. Placement is OPUS's choice. Suggested text:

```
- AuthoredTableHeader inverse reader (FABLE review of ASTRA `ov42-sequence-queue-source`, 2026-10-02,
  _index/candidates/fable-review-astra-ov42-sequence-queue-source-1002/REVIEW.md):
  - 00306760 + 0x138 .. + 0x158 (kind-4 arm; kind 3's arm + 0xAD .. + 0xCD is the same) inverts a row pointer:
    D = (low32(row) - low32(0020E600(header +0x0C))) mod 2^32 (`sub edi, eax`, 32-bit), then an UNSIGNED
    32-bit `div` by the zero-extended u16 header +0x08 (EDX zeroed first).
  - TWO separate QWORD loads of 02EBF138 with the lookup call between them: +0x0C from the first, +0x08 from
    the second. Equality and stability are not established.
  - PRECONDITION: recordStride > 0. There is no zero test between the WORD load and the `div`; a zero stride
    is a #DE in emulation (a source prediction, not an observed fault).
  - Kind 4 then narrows the quotient to its low 16 bits: FFFF -> queue DWORD FFFFFFFF, else (w - 0xD0) mod 2^32,
    stored as a DWORD to 022C2178 (00306760 + 0x174). Kind 3 passes the full 32-bit quotient on as EDX.
- recordStride (+0x08) reader list: add 00306760 + 0x152 and + 0xC7 (divide, not multiply).
- recordArrayRef (+0x0C) reader list: add 00306760 + 0x13F and + 0xB4.
```

## Noted, outside this package: the mode-ladder extent

The mode-ladder page's "The `00306760` exclusive subtree" gives `00306760` as "(293 B)". The image's `.pdata` gives
five chained records over 936 bytes, of which 911 are code (this review's extent checks). The page is led by the
Database prefix (Database 10, OPUS 4, FRONTIER 4). The correction belongs to a later package with its own
correction record. It is not proposed here.

## Optional: register row OV-42 (FABLE, at publish time)

Append this to the OV-42 status cell and keep its current text:

```
2026-10-02 (FABLE): the special-sequence queue store 00306760 + 0x174 is read - only dispatch kind 4 reaches it,
and it queues the low-16 row quotient (low32 row - lookup base, unsigned div by the second descriptor's u16 +8)
as FFFFFFFF or w - 0xD0; no local row exclusion (ASTRA ov42-sequence-queue-source, FABLE review
ACCEPT-WITH-NARROWING). Kind-to-row/caller/owner consistency stays OPEN.
```

Escape any literal `|` before writing it into the row.

- consumer: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md` OV-42 subsections - revised-here (edits 1-4)

affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

run: `rv_seqq.py` at HEAD d8dd3408b (58 checks, 58 PASS, 0 FAIL, 17 controls)
