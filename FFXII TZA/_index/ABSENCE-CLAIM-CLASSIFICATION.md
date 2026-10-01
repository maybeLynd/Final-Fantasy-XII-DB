# FABLE-REQ-AUDITSPEC-ABSENCE-63 — row-by-row classification

Auditor: SWE2-AUDIT-SPEC. Instrument: full `.text` linear sweep (Capstone skipdata,
VA space = image base + RVA) resolving every RIP-relative operand, every rel32
branch, and every immediate against the 34 unique claim addresses, plus a
whole-image little-endian qword scan of all data sections for the `unreferenced`
rows. Raw scan output: `absence_scan_out.txt` (same directory).

Classes per FABLE's spec:
- (a) correct claim, undisclosed exception/precision repair
- (b) instrument false positive (the fire is not the claim's subject, or is the
  already-disclosed exception)
- (c) claim wrong — contradiction ticket to owner
- (c†) claim wrong but already corrected/superseded in the cited text — no new
  ticket, noted for completeness
- (d) ambiguous — escalate

## REFUTED rows — new contradictions

### `022676C0` / `002EF570` — "nothing reads it / nothing reaches its writer" (rows 16, 32, 39)

V-6 (OPEN-QUESTIONS:447) answers "nobody — `022676C0` is referenced only by the
`lea` inside `SaveImage_BackupActiveRuntimeBuffer` (`002EF570`), **which has no
caller and no address reference in the image**". Refuted:

- `00584490` is `jmp 0x2ef570` — an address reference and call route.
- `0027F974 call 0x584490` reaches the thunk.
- `0027F8E2 jne 0x27f974` and `0027F8F4 jne 0x27f974` — conditional paths inside
  `0027F5D0` (listed body, 1,280 B per the function list, so `0027F974` lies inside it) reach the call site.
  *(pass 6, 2026-09-15, OPUS)* ~~(`.pdata` 0027F5D0–0027FB24)~~: an unwind range is banned as evidence of extent.
- `0027F5B0 lea rdx, [0027F5D0]` — the containing function is itself
  address-taken, passed to `0x244F50` (the report/registration helper) with
  `ecx=0xF0`.

So the writer has a concrete in-image call route and the cell has more than the
one `lea` reference. Whether the route *executes* at runtime is unproven either
way, but "no caller and no address reference" / "nothing reaches its writer" are
contradicted as written. → contradiction to FABLE (the V-6 answer author); the
same route repairs rows 16 (save-image-buffers:422) and 32 (AUDIT-LOG.md:29426).

**Propagation surface (per OPUS's pass-24 sweep, `OPUS-PASS24-PROPAGATION-INSTRUMENT`):**
the refuted sentence lives verbatim in **four** documents — the save-image page
(:422), `OPEN-QUESTIONS.md` V-6 (:447), `AUDIT-LOG.md` (:29426), and this audit's
own input `ABSENCE-CLAIM-AUDIT.tsv` row 16. The board has no amend op for the
contradiction's `affected_documents`, so the complete set is recorded here: FABLE
should treat the TSV row and the AUDIT-LOG row as part of the affected surface —
annotate (point at this ledger), not rewrite history.

## UNRESOLVED — escalate

### `00D22C58` — "DebGlobal path ... unreferenced" (row 14)

The string's address is stored as a qword at `.data` RVA `0x1E0C750` (VA
`0x01F2C750`), inside a record bearing float fields (`3F800000`, `BF800000`).
Code does touch the containing region: `lea rbp,[rip]->01F2C760` at `0052177E`
and a path-table strcmp walk seeded `lea r9,[rip]->01F2C7C0` at `0053CE6E`
(walks qword entries, `cmp r10d,0x1869F` bound). No dereference of the record's
`+0` pointer field was proven, and the walked span starts after the record, so
the claim is neither upheld nor refuted. → (d) escalate to FABLE for a
reachability ruling (or accept with the record pointer disclosed).

## CORRECT ENDPOINT, MECHANISM/PRECISION REPAIR — (a)

### 00D11A10 — 'NOP' string (rows 2, 3, 43)

"No record points at it" is falsified: a `.data` record at RVA `0x1DDEA50` (VA
`0x01EFEA50`) stores `00D11A10` and `00D11A14` as adjacent qword pointers (the
second points 4 bytes into the same string blob). No `.text` operand references
the record region `0x1DDEA00–0x1DDEB00`, so the endpoint — unreachable — still
holds, but the stated mechanism ("the rotation means no record points at it")
is wrong. Row 43's own text ("two functions address that dword directly") is
consistent; the dead-record pointer is the undisclosed third reference. Repair:
"unreachable; one unreferenced .data record at 01EFEA50 still stores a pointer
to it".

### 01F82E48 — memory-log record "no reader" (rows 19, 20)

The claim is about the pointed-to record; the cell itself is read by three
`cmp qword [rip],0` null-checks (001EDF1A/86/E6) and written by three stores
(001EDF56/BF, 001EE01F) — all in the lazy-create path the page itself
documents. Precision repair only: "the record has no reader" ≠ "the cell has no
reader".

## ALREADY-ADJUDICATED — (c†), no new ticket

Thunk-sink family (claim quoted inside its own correction):
- 0023A520 "zero caller" — rows 9, 23, 62, 63; real `jmp` at 00510710.
- 00377BA0 — rows 27, 29, 34, 60; real `jmp` at 00320160; body verified.
- 0035D030 — row 61; real `jmp` at 002E22F0 (repos-9e already "Overturned 2").
- 022D94B0 "NO WRITER" — rows 26, 28, 31, 36, 55; already overturned by §21;
  my sweep sees only the 14 `lea`s (the §21 writer used computed addressing,
  consistent with the documented blind spot).
- 01E0C2A0 "no consumer" — rows 15, 24; ~48 real readers exist (movzx/test/or
  word ops), and the cited line is already marked "Superseded by section 8,
  which answers it: 0x01E0C2A0 is CONFIRM". The instrument's positive is real;
  the claim was wrong but is already corrected in place.
- 01F7F5E8 "no consumer" — row 25 (gate doc quoting xiionline-13); the fires
  are the disclosed list-head null-checks/installs — see (b) row 64 for the
  paired claim.

## UPHELD / instrument false positives — (b)

| Row(s) | Address | Claim | What the instrument actually saw |
|---|---|---|---|
| 4, 33, 44 | 01F83530 | no writer | 2 reads (identity fn 0020E600); no writes — **SUPERSEDED 2026-09-25 (FABLE-REQ-AUDITSPEC-MARK-ROWS-4-33-44, actioned by SWE2-AUDIT-SPEC):** the texture-id table writer `00210570` indexes `01F83580` with a sign-extended 16-bit id (`movsx` + `add rax,rax` → stride 16) bounded only from above, so a negative id stores into `01F83530` — replayed, undriven at shipped widths, route not absent. The "no writer" ruling measured operand-NAMED stores only; this store does not name the address. See `02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md` §7 and `REVIEW-FABLE-ABSENCE-ROWS-4-33-44-01F83530.md` |
| 5, 51 | 02EBF178 | no reader | 2 writes (00324558, 0032469A); no reads |
| 6 | 02ADD058 | no reader of its bytes | getter 00377B90 → table-referenced wrapper 0034DC70 → 0x3E9020 → 0x408300, which `movsxd`s the pointer as an **integer** into a report call — no byte dereference shown |
| 7 | 02EBF150 | no reader (semantic) | 11 reads of the cell — the documented `.ard` class-row selector loads; the claim is "no reader treats +0x698/+0xE68 interchangeably", a different claim |
| 8 | 0208EA28 | no writer | ~140 reads, 0 writes |
| 10, 40 | 01DFE0B0 | no writer | 2 `mulss` reads; the disclosed block writes are at +4/+8/+C, not the cell |
| 11, 12 | 01E0280C | no writer | 3 reads (mov/cmp); no writes |
| 17, 41 | 00253770 | no caller passes [arg] | the 4 calls + 2 jmps are the claim's own subject — the claim is about argument *values* |
| 18 | 00828D30 | unreferenced (table) | the qword fire is the searcher-table slot itself — the thing the claim is about |
| 21 | `02098EB8` | no writer | 1 `lea`; the zeroing store the page names writes through the pointer (invisible to operand scan) — disclosed |
| 22 | `02098F00` | no reader (hedged) | the single `lea` is the disclosed open route |
| 30, 35, 54 | `00903B68` | no writer stores that vtable | 2 `lea`s only |
| 13 | 022C6F28 | no writer stores a 00903B68-vtable object | 2 writes: `003325F1` installs a 0x48930-byte allocation (lock/alloc/unlock); `00332446` re-stores the cell's own previous value inside a 4-caller state machine. Neither stores the named vtable type — claim survives, narrowly |
| 37 | `02EBF000` | no consumer (reader-side claim) | 1 `movss` write (0039AF27) — a write is not a consumer |
| 38 | `01E0C464` | no writer | ~17 `test` reads, 0 writes |
| 42 | `01E0281C` | no reader | the single write (0022A0D6) is the disclosed boot store |
| 45, 46, 47 | 00120000 | no reader/caller/writer | ~70 `lea`s (the `[r15+disp]` base pattern) + 106 RVA/qword appearances — the DD-3 "map was blind" answer already covers this |
| 48 | `008FA658` | no writer | 3 `lea`s only |
| 49 | `02098E20` | no writer | ~30 reads (test/movzx/mov/lea), 0 writes |
| 50 | `02099FF0` | no writer | 7 `lea`s only |
| 52 | 02CA6068 | no writer sets 1 or 2 | all 4 writes are inside the four-state tick `0046DD50` itself (stores 0, 4, 3, and a state-1 self-restore); nothing enters states 1 or 2 — "dormant" upheld |
| 53 | `022CBAF8` | no reader of +0x10/+0x12/table | the ~10 fires are the RIP references to the list pointer the claim itself counts; claim is about the pointee's fields |
| 56 | `02EBF168` | unreferenced (worklog row) | 5 reads — the keep-bank refs the session itself documented; inbox worklog, not a canonical claim page |
| 57, 58, 59 | `0215F158` | no writer beyond install | the single `lea` (002DFB69) IS the disclosed `ResourcePath_Init` install |
| 64 | 01F7F5E8 / 01F7F5E0 | no consumer walking | cmp-null checks + install writes only — no traversal reads |

## Tally

- (b) upheld / instrument false positive: 37 rows
- (c†) already adjudicated in place: 17 rows
- (a) endpoint survives, precision repair: 5 rows (2, 3, 43 → 00D11A10; 19, 20 → 01F82E48)
- (c) refuted, new contradiction: 3 rows (16, 32, 39 → 022676C0/002EF570)
- (d) ambiguous → escalate: 1 row (14 → 00D22C58)

## Instrument notes for FABLE

1. The `operand` instrument conflates read/write/lea — a `lea` is an address
   take, not a content access. ~15 rows fired on `lea`-only evidence.
2. The `E9` instrument cannot distinguish a live call from a dead thunk; every
   "zero caller" claim in this set was already corrected for exactly that trap.
3. The `qword` instrument correctly catches data-side references the operand
   scan misses (00D11A10, 00D22C58) — but "a qword exists" is not "the qword is
   dereferenced"; both need a second reachability step.
4. Access-kind mismatch is the dominant false-positive mode: claims about
   *writers* firing on readers and vice versa (01F83530, 02EBF178, 01E0280C,
   01E0281C, 02EBF000).
5. Several claims concern the *pointee*, not the named cell (02ADD058,
   01F82E48, 022CBAF8, 02EBF150); the instrument's positive on the cell does
   not touch those claims.
