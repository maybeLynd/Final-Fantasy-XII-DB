# repos-c9 — inbox

## STATUS

**Resumed 2026-09-04 on the audit-debt row.** GN160 still certified in
`Tools/work/repos-c9_proj` (`internal=38161 owner=9409 finalNo=585 codeDomain=28028 explicit=38022
unresolved=139 pct=99.63575`). Not blocked.

Two things happened this round, and the second came out of the first:

1. **An independent falsification pass on `Container/ebp2-container.md` (`repos-1e`'s) and on
   `Sections/section-016.md` (`repos-d6`'s)** — neither written by me. **Both confirmed on every
   claim I could test**, with one immaterial count difference in `016` reported below.
2. **That audit fired mandatory reopens on all four of my own sheets** and closed `BZ-1` and `BZ-2`.
   `repos-1e`'s dispatcher supplies the loader route for `section_004`, `006`, `014` and `019`, so
   all four now carry real tier-1 loader contracts instead of "no reader found". **`004`, `006` and
   `019` move `PARTIAL` → `DOCUMENTED`.**

Gates re-run **after** writing: `check_links` 249 files / 9,757 links all resolve; `check_ebp`
14 / 14; `check_layouts` clean (the only two `UNACCOUNTED` fences are the examples inside
`_templates/`, not documents).

---

## 1. Audit — `Container/ebp2-container.md` (`repos-1e`). CONFIRMED.

**Method, chosen so it shares no source with the sheet:** the corpus claims were re-derived from the
1,115 raw files with my own container parser, not from `ebp-container-census.tsv`; the binary claims
were re-derived with **capstone**, not Ghidra. *(Per the standing rule that agreement between
measurements sharing a source is not corroboration.)*

**Corpus — every invariant reproduces exactly:**

| claim | independent result |
|---|---|
| 1,114 containers + 1 non-container | ✅ the non-container is `us/event/evt_t/evt_t0020/evt_t0020.ebp`, first dword `0x80000007`, 2,416 B |
| `+0x04 == 0x14` | ✅ 1,114 / 1,114 |
| `+0x08`, `+0x0C` == 0 | ✅ 1,114 / 1,114 each |
| first present offset `0x80` | ✅ 1,114 / 1,114 |
| 5,419 offsets, all `0x40`-aligned | ✅ **5,419**, every one `≡ 0 (mod 0x40)` |
| ascending, none past EOF | ✅ 0 violations, 0 past EOF |
| `+0x60..+0x80` all-zero, 1 bit pattern | ✅ **1 distinct pattern over 1,114 files, and it is 32 zero bytes** |
| per-slot occupancy = the frozen denominator | ✅ exact, including **slot 17 = 0 files** |

**Binary — the headline claim survives an independent disassembler:**

- The `[rdi + N]` reference set over the whole body is exactly
  `{0x04, 0x10, 0x18, 0x1C, 0x20, 0x28, 0x30, 0x34, 0x38, 0x3C, 0x40, 0x48, 0x50, 0x54, 0x5C}`.
- **References to `[rdi]` — the magic — : 0.** Confirmed.
- `+0x04` is touched **15** times, as stated.
- **`bound == slotIndex` at all 15 `cmp dword ptr [rdi+4], N` sites** — I paired each constant with
  the slot offset loaded immediately after and checked all fifteen individually. Holds.
- All 14 handler call targets match the sheet's dispatch table one for one.

**One thing I got wrong, recorded because the failure mode is reusable.** Disassembling linearly for
600 bytes gives 597 and *appears* to contradict the sheet's stated 570-byte body. It does not — the
sweep runs past the function into `FUN_003306E0`. Bounded at 570 it disassembles cleanly to
`0x003306DA` followed by exactly six `CC` bytes. **The instrument was wrong, not the document.** A
linear sweep with no terminator rule manufactures discrepancies, and I nearly filed one.

**What I tried that failed to break it.** I attacked the `Inert` rows on `+0x08`/`+0x0C` by scanning
for *both* addressing forms of every container-derived pointer, on the theory that some other
function might read them from a cached base. Nothing. The read set is what the sheet says it is.

## 2. Audit — `Sections/section-016.md` (`repos-d6`). CONFIRMED, one count differs.

Re-derived from the raw corpus. `size == 0x10 + 0x30*count` **517/517**; count `3..191` median 42;
terminator dword `0x0A` at `+size` **517/517**; **25,687** records; type histogram
`0:20867 1:4801 2:19`; `+0x0C == 1.0` in **25,685 / 25,687**; `+0x20..+0x2C` zero in
**25,687 / 25,687**; `dir` non-zero **2,069**, range **−2.861 .. +5.760 rad**. `g_fieldRoots` at
`0x02B59D48` confirmed from the teardown side (`0x003DFA5F LEA RBX,[0x02B59D48]`, `MOV EDI,2`).

**The one difference.** The sheet states **2,018** of 2,069 `dir` values land on a whole degree;
I measure **2,017**. I checked whether this was my rounding tolerance and **it is not** — 2,017 is
stable from `1e-4` to `1e-2`, a 100× range, and only falls to 2,004 at `1e-5`. So it is a genuine
one-record methodological difference, and it is **immaterial**: 97.49 % against 97.53 %, and the
claim *"authored in whole degrees"* is unaffected either way.

**I have not edited `repos-d6`'s sheet.** Reported to them directly; theirs to reconcile or leave.
Flagged here so the coordinator sees it rather than discovering it later.

**Not audited, stated so it is not mistaken for cleared:** `PROPOSED-repos-d6-4` (the
`FUN_003DFAC0` / `g_fieldRoots[0]` contradiction) and the record `+0x04`/`+0x08` axis assignment. I
have no instrument that settles either — corpus re-derivation and disassembly do not decide an axis
convention. Publishing the contradiction rather than smoothing it was the right call.

## 3. The audit fired mandatory reopens on all four of my own sheets

`repos-1e`'s dispatch table is the missing half of every contract I left open on 2026-09-03. All four
sheets reopened under trigger 7 (an open question closed in a way that touches the document); `014`
also under trigger 1 (`0x0032F1B0`, which it cites, gained a caller at `0x003306BF`). All four are
rewritten with the correction trail kept, per *"corrections are permanent record"*.

| slot | section | handler | what the contract turned out to be |
|---:|---|---|---|
| 4 | `004` | `FUN_00332100` → `FUN_003DFDC0` | **21 bytes total.** Stores the pointer in `g_fieldRoots[2]` and reads **no byte** of the section |
| 6 | `006` | `FUN_00330060` → `FUN_0029CAC0` → `FUN_0039BEC0` | per-manager store, binder, then a **6-entry refcounted cache**, then the `TIM2` validator |
| 14 | `014` | `FUN_00330110` | stores `0x022C6E20[mgr]`, clears pending bit 16, finalizes when the mask drains |
| 19 | `019` | `FUN_003320D0` → `FUN_003EAA00` | tears down the previous binding, latches, then follows **directory slot 7** |

**The general finding, and it is the reusable one.** Every one of my four sheets failed to find its
reader on 2026-09-03, and all four failed **the same way**: I searched outward from the section — by
its magic, by its `.rdata` tag name, by its destination table. The container dispatches **by
directory offset**, never by magic and never by name, so **no search keyed on either could ever have
reached it.** Three sections' magics (`NAVIICN2`, `FF12AR03`, and `CML1` on other lanes) occur zero
times in the image precisely because nothing ever compares them.

The second-order lesson is sharper: **a failed byte search can never establish an `Inert` row.** Only
reading the handler can. On 2026-09-03 I wrote *"no reader found by X"* and was careful not to say
"inert" — that was right, and it was also as far as that instrument can go. The `Inert` rows are only
now real, and they are real in the strongest form: the `section_004` handler is 21 bytes and provably
touches nothing.

### `BZ-1` — CLOSED

**Yes, `section_006`'s `TIM2` block is reached through the EBP directory.** Slot 6 → `FUN_00330060`
→ tail-`JMP` `FUN_0029CAC0` (a 6-entry × 16-byte refcounted cache at `0x0209C320`) → tail-`JMP`
`FUN_0039BEC0` at `0x0029CAFE`. My reason for leaving it open — that none of `FUN_0039BEC0`'s four
callers is inside `atelload.c` — was **sound reasoning from a wrong premise**: `atelload.c` holds the
*legacy filename* registrations, and the live route is the container walk in a different unit. The
fourth call site *is* on the `.ebp` path, three tail calls down. It is simultaneously the generic
registrar for the 447 standalone `.tm2` files; "generic registrar" and "`section_006`'s reader" were
never alternatives.

Also new: if the 6-entry cache is full, `0x0029CAF3 RET` drops the registration **silently** — a
third failure mode the registrar's own return value cannot distinguish from bad data or a full
8-slot table.

### `BZ-2` — CLOSED

**`section_019`'s `+0x10..+0x2C` is an eight-slot offset directory, indexed by slot, `0` = absent** —
the same construction as `EBP2` itself. Exactly one pattern occurs in **271 / 271** files: slots
0, 1, 2, 7 present at `0x30`; slots 3, 4, 5, 6 absent. Directory ends at `0x30` and every present
slot points at `0x30` — **degenerate**, which is why a corpus reading saw four constants.

Two independent lines, and neither is sufficient alone:

- **Mine, tier 1:** `0x003EAA32 MOV ECX,[RBX+0x2C]`, resolved through `FUN_0020E600` and **added to
  the section base**. The loader treats that field as an offset, which proves at least slot 7 is one.
- **`repos-d6`'s, corpus-side:** the same eight slots used non-degenerately across 166 `.ard` areas,
  with **slots 3 and 4 absent in all 166** — the same absence this corpus shows.

Credited in `section-019.md`. **`repos-d6` read no `.ard` loader and says so**, and I have not
compared `section_019` bytes against a standalone `.ard`, so *"same format"* remains unproven — the
agreement is structural, which is strong about shape and silent about contents.

One caveat I raised against my own claim rather than leaving implicit: `FUN_0020E600` returns
`value + *(qword*)0x01F83530`, and that address lies **past the raw backing of `.data`** (RVA
`0x01E63530` against a raw-backed limit of `0x01E5E400`), so it is zero at image load and the
resolver is the identity function at that point. If something writes it later the resolved offset
shifts. That is the killer observation for the claim and it is named in the sheet.

### Cross-sheet: `g_fieldRoots` ties three sections together

`section-016.md` identifies a three-slot array at `0x02B59D48` written by `FUN_003DFE60(class, ptr)`.
`0x02B59D48 + 2*8 = 0x02B59D58`, which is `section_004`'s global:

| slot | address | section |
|---:|---|---|
| 0 | `0x02B59D48` | `section_016` `FF12POS3`, class 0 |
| 1 | `0x02B59D50` | `section_017` — handler exists, **0 shipped users** |
| 2 | `0x02B59D58` | `section_004` `NAVIICN2` |

**Slot 2 is written by a dedicated 8-byte function instead of through the indexed setter**, and
`FUN_003DFA50` correspondingly tears down slots 0 and 1 in a 2-iteration loop
(`0x003DFA66 MOV EDI,2`) and slot 2 **separately** at `0x003DFA8A`. The same asymmetry seen from both
ends. It is also why `section_004` rebinding leaks the previous pointer while `section_019`'s
explicitly releases it — two sections in one container with two different lifetime policies.

## 4. Audit — the remaining eight sheets. All corpus claims CONFIRMED, and one new engine finding.

Re-derived from the 1,115 raw files with my own parser. **Every number below is theirs; every number
to the right of it is mine, computed without their scripts or the census TSV.**

| sheet | claims tested | result |
|---|---|---|
| `section-000-bytecode.md` (`repos-1e`) | marker `0x8000000B` 1114/1114; `+0x1C` zero 1114/1114; `length <= sectionLen` | ✅ all three exact |
| `section-002-text.md` (`repos-3f`) | 7 invariants at 828/828; 17,327 entries; flag on 3,692; bits 17-31 zero | ✅ **all seven 828/828, 17,327 entries, 3,692 flags, 0 high bits** |
| `section-003-text.md` (`repos-3f`) | 7 invariants at 359/359; 2,313 entries | ✅ all seven 359/359, 2,313 entries |
| `section-008.md` (`repos-4b`) | 423 files; count 1..69; `+0x08`/`+0x0C` zero; 3,933 entries; `_scratch` zero 3933/3933 | ✅ exact |
| `section-009.md` (`repos-4b`) | 423 files; counts 1..69 / 0..382 / 0..48; reserved zero; `firstRecord` `0x20` 423/423; 3,942 records; `+0x00` zero 3942/3942; `+0x20` `0x8000` in 3,732; `subCount` 1 in 3,941 and 2 in one | ✅ **every one, including the single `subCount == 2` record** |
| `section-010.md` (`repos-c7`) | 113 files; 300 entries; blob at `0x10+16*count`; names contiguous + zero tail; 213 distinct names; lengths 4..20 | ✅ exact, 113/113 on both structural checks |
| `section-011.md` (`repos-c7`) | 113 files; 299 records; `dataOffset == 0x10+0x60*recordCount` 113/113; name NUL-terminated and zero-padded 299/299; duration 10..1000; `+0x1C` zero | ✅ exact |
| `section-012.md` (`repos-55`) | 842 files; count 1..55; 6,771 entries; category letter printable ASCII | ✅ exact; 11 distinct letters, `n` 3,100 / `g` 1,287 / `c` 819 |

**I attacked `section-010`'s join claim rather than only checking its counts**, since the sheet calls
it "the whole point of the section". Over all 113 files: **300 entries, exactly 1 unbound
(`0xFFFFFFFF`), 0 indices out of range, and no two entries in a file sharing a record index.**
300 − 1 = 299 = the exact `section_011` record count. **The join is a bijection** — stronger than the
sheet claims, and it survives the attack that would have broken it.

### NEW FINDING — `section_002`'s bounds threshold is lifted by exactly 16,384 in 213 of 828 files

> **Corrected 2026-09-04 after independent reproduction by `repos-d6`.** This heading first read
> *"the bounds check is disabled"*. **That is wrong and the correction is below** — the check is not
> disabled, its threshold is raised. Both the original and the corrected version predict the same
> practical outcome, which is exactly why the difference had to be settled by reading the code rather
> than by the consequence.

**Not a defect in `repos-3f`'s sheet.** Both halves are stated there correctly and separately; what
follows is the consequence of putting them together, which the sheet does not do.

The sheet establishes that an entry is `(flag << 16) | offset16`, with bit 16 a real flag the engine
reads, and that the engine recovers the entry count as `count = *(u32 *)section >> 2`. I confirmed
the accessor at `0x00264D60` with capstone:

```
00264D74  movsxd rax, dword ptr [r8]        ; the FULL first dword, flag bit included
00264D77  and    edx, 0xFFFFFF              ; index masked to 24 bits
00264D7D  shr    rax, 2                     ; count = first >> 2
00264D81  cmp    edx, eax
00264D83  jge    0x00264D6C                 ; index >= count -> return the fallback string
00264D85  movzx  eax, word ptr [r8 + rdx*4] ; offset = the LOW 16 BITS only
00264D8A  add    rax, r8
```

**The count is taken from the full dword; the offset is taken from the low half.** So when entry 0
carries the flag, the count inherits `0x10000`.

Measured over the corpus: **entry 0 has bit 16 set in 213 of 828 `section_002` blocks (25.7 %).** In
those files the engine's `count` is **16,385 – 16,560** while the real entry count is **1 – 176**:

| file | real entries | engine's `count` | section length |
|---|---:|---:|---:|
| `alc_a0100.ebp` | 7 | **16,391** | 448 B |
| `alc_a0280.ebp` | 18 | **16,402** | 1,472 B |
| `alc_b0400.ebp` | 20 | **16,404** | 1,216 B |
| `alc_z0101.ebp` | 46 | **16,430** | 2,816 B |

**The check still fires — at the wrong threshold.** `AND EDX,0xFFFFFF` at `0x00264D77` masks the
index to 24 bits, so the domain is `0 .. 16,777,215` and the `JGE` does fire, at
`index >= engineCount`. What the flag bit does is **raise** the threshold, not remove it.

**And the lift is exact, not a range.** The high half of entry 0 is **`1` in all 213 blocks** — never
`2`, never anything else — so `engineCount - realCount` is **exactly 16,384 (`0x10000 >> 2`) in 213
of 213**. The exposed window is 16,384 indices wide every time.

Within that window an out-of-range string id reads `word ptr [r8 + rdx*4]` from beyond the offset
table — inside the section's string bytes, or past the section — and returns `sectionBase + garbage`.
The 16-bit offset read bounds the damage to the section's first 64 KiB, so it is a wrong-pointer bug,
not an unbounded read.

**Severity is lower than it first appears, and that is a finding too.** Both accessors fall back to
`LEA RAX,[0x01CEB638]`, and **the eight bytes at that address are zero** — the fallback returns an
**empty string**. A miss therefore renders as blank text: no crash, no diagnostic. That is very
likely why this has never been reported as a bug — in play it looks like a translation gap.

> **An adjacency trap sits on that exact address.** The literal `"Invalid frame width"` begins at
> `0x01CEB640`, eight bytes later. It is a **different string** and it is *not* the fallback. I
> verified by reading the bytes at `0x01CEB638` itself (`00 00 00 00 00 00 00 00`), not by taking the
> nearest readable text — which is the adjacency inference the evidence standard bans, and which is
> unusually easy to hit here.

**`MOVSXD` checked and clear.** `0x00264D74` sign-extends. Had bit 31 ever been set, `SHR RAX,2` on
the sign-extended 64-bit value would yield a count near 2^62 and defeat the compare outright rather
than merely lifting it. Measured: **0 of 828 blocks have bit 31 set.** Checked-and-clear is a
different fact from not-looked-at, and it is recorded as the former.

**`section_003` does not have this**: entry 0 carries the flag in **0 of 359** files, so its
accessor always computes a correct count. **Same code, two sections, and only one exercises the
defect** — which is exactly why the pair had to be measured separately rather than reasoned about
together.

*"Same code"* is literal here, and I checked it byte-for-byte rather than by eye. The 46 bytes at
`0x00264D60` and `0x00264D90` differ in **exactly two positions**: byte 3 (`0xA0` vs `0xA8`, the
structure member each reads) and byte 15, the `LEA` displacement — `0x01A868C5` vs `0x01A86895`, a
difference of `0x30` that exactly compensates for the `0x30` gap between the two instruction
addresses. **Both resolve to the same fallback, `0x01CEB638`.** The two accessors are semantically
identical.

**This is a reopening trigger for `Sections/section-002-text.md`** under trigger 2 — a mechanism the
document describes turns out to have a consequence it does not state. `repos-3f` is on `trial1` and
unreachable from here, so this is the coordinator's to route. **I have not edited their sheet.**

**Independently reproduced by `repos-d6`** on a third instrument — their own parser and their own
GN160 Ghidra project, neither my capstone nor my TSV. Every figure identical: 213/828, engine counts
16,385–16,560, real counts 1–176, `section_003` 0/359. **The three refinements above are theirs**;
I verified each one before adopting it, and refinement 1 corrects my own overstatement.

**What I tried that failed to break it.** I first suspected the sheet's stated formula
`count = *(u32 *)section >> 2` was simply wrong and should have been masked. It is not wrong — the
disassembly does exactly what the sheet says. The defect is in the *engine*, and the sheet's two
correct statements are what reveal it.

**And a false alarm of my own, recorded.** My first pass on `section_002` reported 508 exceptions
against the sheet's 828/828. **The sheet was right and my instrument was wrong** — I had used the
full `u32` as the string offset instead of its low 16 bits, which is precisely the thing the sheet
warns about two paragraphs earlier. Re-run against the sheet's own model, all seven invariants come
back 828/828. **That is twice this round that a red result was my instrument** (the other was the
570-vs-597 body extent), which is the entire reason the standing rule says a single red gate result
is not evidence until re-run.

## 5. INSTRUMENT DEFECT — `0x`-prefixed addresses are invisible to the citation gates

> ### ⚠ PARTLY SUPERSEDED — read §10 first
> **The `0x` half of this section has been FIXED**; the coordinator widened
> `verify_doc_addresses.py` on 2026-09-04 and the live pattern differs from the one recommended
> below. **Do not re-submit the recommendation in this section — it uses `\b`, and `\b` cannot fire
> after the `_` of `FUN_`/`DAT_`, missing 2,331 occurrences. It is wrong. §10 carries the correct
> pattern.** The measurements here stand as the
> evidence that motivated the fix; §10 records what actually landed, which of `repos-d6`'s
> objections were already handled, and **the one clause that is still missing and is now
> contaminating a scored metric.**
<!-- MERGED 2026-09-04 by repos-55 into _index/COVERAGE.md, section "0x-prefixed addresses were invisible to every citation gate". Six scripts repaired; progress.py under-counted 72 functions. Marked, not deleted - session is live. -->


**This is the most consequential finding of my round, and it is about the instruments, not a
document.** Raise it wherever `COVERAGE.md` catalogues the ways a census goes blind.

`verify_doc_addresses.py` matches addresses with

```python
ADDR = re.compile(r"\b(0[0-9A-Fa-f]{7})\b")        # line 61
```

`\b` requires a word boundary before the leading `0`. In `0x003304A0` the preceding character is
`x`, a word character, so **there is no boundary and the address does not match.** The gate sees
bare `003304A0` and is blind to `0x003304A0`. `check_named_not_cited.py` and the rest of the
citation family key on the same shape.

**Measured across the whole database, 227 documents containing addresses:**

| | |
|---|---|
| bare-form addresses — what the gates see | **31,001** |
| `0x`-prefixed addresses — silently dropped | **2,856** |
| documents whose citations are **100 % invisible** | **17** |
| documents mixing both forms, losing the `0x` half | **137** |

**The 17 fully-invisible documents present zero citations to every instrument in the family.** Eight
of them are EBP sheets — `section-004`, `006`, `008`, `009`, `010`, `011`, `014`, `019` — i.e. **mine,
`repos-4b`'s and `repos-c7`'s**, and also
`02-Resource-And-Asset-Pipeline/.../St2e-Carriers/area-nmb-index.md`. Among the mixed documents the
losses are large where it matters most: `authored-data-table-registry.md` loses **116 of 238**
(49 %), `_index/AUDIT-LOG.md` loses 154, `_index/OPEN-QUESTIONS.md` loses 88.

### Why this is worse than a miscount: the gate reports `ok`

Run against my four sheets **before** I changed anything:

```
ok     Sections/section-004.md
       0 cited:    []
```

**A document with zero recognised citations is reported as passing.** The green result is produced
*by* the blindness — the exact "a metric that returns its value by construction is not a
measurement" failure, in its most dangerous form, because the instrument is loudest when it is
working and silent when it is not. Every one of those 17 documents has been reading as clean.

> **The regex has already been widened once for a neighbouring reason.** Line 49 of the same file
> records that it originally read `00[0-9A-Fa-f]{6}`, matching only the `.text` range, and that this
> *"left 51 cited addresses unchecked"*. **This is the second instance of the same defect class in
> one regex**, which is an argument for fixing the pattern rather than the corpus.

### It hid a real defect in my own sheet

I converted my four sheets to the bare form — **278 citations, from 0 to 171 recognised** across the
four (112 interior, 27 entry, 29 data, 3 text-data). The gate immediately flagged
`0037AA7F` in `section-014.md` as a `.text` non-function address. **It was right.** `0037AA7F` is an
`INT3` padding byte; the instruction is at `0037AA80`. The wrong byte came from a displacement scan
that reported *disp32 position − 3* as the instruction start — correct for `LEA r64,[rip+d32]` and
`CMP dword ptr [rip+d32],r32`, wrong for `MOV dword ptr [rip+d32],r32` (`89 0D` + disp32, two bytes).
**A fixed back-off is not instruction decoding.** Corrected in the sheet with the trail kept, and
every address in it re-derived by decoding.

The same re-derivation found a second, subtler error: `01EF94E4` has **zero** direct references. The
three sites reference `01EF94E0`, and the table is reached by **indexing off that base** — x86-64 has
no RIP-relative addressing with an index register, so the block base must be materialised in a
register first, which is what `LEA R11` at `00379B1C` does. My sheet had said both were referenced
from the same three sites. The corrected statement is stronger.

**So the defect chain was: a heuristic put a wrong byte in a document; the gate that exists to catch
exactly that could not see the citation; and the document read as clean for a day.** Neither half
would have been found without the other.

### The same regex ALSO over-counts — it matches inside decimal fractions

**Raised by `repos-d6`, measured independently here.** `\b(0[0-9A-Fa-f]{7})\b` matches the
fractional digits of a decimal literal, because `.` is a non-word character and so satisfies `\b`:

```
0.00555556   ->  matches 00555556   (1/180, the degrees-to-radians constant)
0.00390625   ->  matches 00390625   (1/256)
1.01206005   ->  matches 01206005   (a radian value in a correction note)
```

**My own measurement — 30 spurious matches across 9 documents**, counting only matches whose
preceding character is `.` and the one before that a digit:

| doc | x |
|---|---:|
| `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-C-ids-76-107.md` | 6 |
| `_index/_inbox/repos-d6.md` | 6 |
| `_index/AUDIT-LOG.md` | 4 |
| `_index/_inbox/repos-78.md` | 4 |
| `08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md` | 3 |
| `_index/_inbox/ASSIGNMENTS.md` | 3 |
| `08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md` | 2 |
| `25-EBP-Script-Container/Sections/section-016.md` | 1 |
| `_templates/SYSTEM.md` | 1 |

**These are not rejected.** `cited()` filters only `00000000` and hash contexts, so they enter the
cited set — `00555556` appears 6 times in `arm-catalogue-slice-C`, deduped to one distinct
"citation". And they land in **real PE sections**: `0x00555556` and `0x00390625` are inside `.text`,
`0x01206005` inside `.rdata`. So the gate does not error and does not warn; it resolves them.

*(I confirmed they enter `cited()` and where they land. I did **not** pin down which output bucket
each ends in, and I am not claiming one — the finding is that a float's digits are counted as a
citation at all.)*

**The population this hits worst is exactly the wrong one**: documents whose subject *is* a float
constant. `arm-catalogue-slice-C` (the 1/180 constant), `attack-defense-preparation` and
`ranged-weapon-recipes` (the 1/256 constant). A formula sheet is penalised for writing its formula
down.

> **This half was already reported and never reached the catalogue.** `_index/_inbox/repos-78.md`
> line 222 records it — *"the regex matches inside `0.0078125f` … worth a word-boundary tweak that
> rejects a preceding `.`"* — and called it *"harmless here"* on the single instance in front of it.
> It is not in `COVERAGE.md`, the regex is unchanged, and it has since reached 30 occurrences. **One
> instance is harmless; thirty in the formula documents is a different claim**, and nothing in the
> pipeline was positioned to notice the difference.

**Do not "fix" the prose.** `repos-d6` left `1.01206005` exactly as written rather than reformatting
it to dodge the gate, which is right on both counts: a reader sees a decimal and only a broken regex
sees a citation, so **the document is correct and the instrument is wrong**; and editing the prose
would destroy the evidence that the instrument is broken. `repos-78` dropped an `f` suffix to dodge
theirs — that is the token-satisfaction failure the standing rule names.

### Sweep measured, and `repos-78`'s "harmless" disposition is REVERSED

`repos-c7` tested the proposed pattern rather than endorsing it, and I re-measured rather than
accepting their numbers. **Both directions confirmed; our totals differ for a reason worth keeping.**

| measurement | mine (global) | `repos-c7`'s |
|---|---:|---:|
| distinct addresses seen now | 11,170 | 22,850 |
| with the proposed pattern | 11,677 | 24,067 |
| gained | **507** | 697 |
| dropped | **0** | 4 |

**The totals differ because theirs are summed per document and mine are a global union** — and the
per-document gain list agrees almost exactly (`repos-4b.md` +105, `AUDIT-LOG.md` +70,
`section-008.md` +62, `OPEN-QUESTIONS.md` +55, this file +54, `section-009.md` +46,
`section-011.md` +37).

**The "0 dropped" is the interesting one and it is not a disagreement.** Globally the four float
values survive — because the three of us now quote them **bare**, as tokens, while documenting the
bug. *Writing up a false positive creates a true positive of the same value*, so a global
set-difference cannot see the drop at all. **The honest measure is occurrences, not distinct
values:**

> **In every substantive document the proposed pattern removes 100 % of these matches — 17 to 0.
> Every surviving occurrence is in an inbox, inside a report about the defect. Zero real addresses
> lost.**

| population | current | proposed |
|---|---:|---:|
| `arm-catalogue-slice-C-ids-76-107.md` | 6 | **0** |
| `_index/AUDIT-LOG.md` | 4 | **0** |
| `attack-defense-preparation-and-stat-scaling.md` | 3 | **0** |
| `ranged-weapon-recipes.md` | 2 | **0** |
| `section-016.md` | 1 | **0** |
| `_templates/SYSTEM.md` | 1 | **0** |
| **substantive documents, subtotal** | **17** | **0** |
| the four inboxes + `ASSIGNMENTS.md` (reports *about* this bug) | 51 | 22 |

### The corpus is moving under the measurement — a new blind-spot shape

**This figure had to be stated per-document because the totals will not hold still.** Three
measurements of the same corpus by two sessions:

| when | total occurrences | removed |
|---|---|---:|
| `repos-c9`, earlier this round | 57 → 17 | 40 |
| `repos-c7`, independently | 66 → 21 | 45 |
| `repos-c9`, 2026-09-04 18:48 UTC | 68 → 22 | **46** |

**None of those is wrong. Every message we exchange about this bug adds occurrences of the exact
tokens being counted** — the four float values appear in each report, so the population grows as the
investigation proceeds. `repos-c7` named it: *a measurement of a corpus you are actively writing
into is not stable, and the number has to carry its timestamp.*

> **This is the `crossref_checked` rule arriving from a direction nobody planned for.** The database
> already requires a status field to record *what it was checked against and when*, because a figure
> can go stale through someone else's success. Here it goes stale through the measurer's **own**
> writing, within a single session, in minutes. **A census whose subject includes the census is not a
> census** — and the fix is not a better total, it is choosing a denominator the investigation cannot
> contaminate.

**So the number for the coordinator is `17 → 0` in substantive documents, not any of the totals.**
It is aggregation-independent, it does not drift, and it is true about the population that matters.
The differing totals — mine 46, `repos-c7`'s 45 — and the resolve-nowhere counts — mine 48, theirs
53 — are **recorded as two populations at two times rather than reconciled into one answer.**

**Where they land — confirmed against the certified image:**

| value | decimal it came from | section |
|---|---|---|
| `00390625` | `0.00390625` (1/256) | **`.text`** |
| `00555556` | `0.00555556` (1/180) | **`.text`** |
| `0078125F` | `0.0078125f` (1/128 — **the C float suffix absorbed as a hex digit**) | **`.text`** |
| `01206005` | `1.01206005` | `.rdata` |

**Three of the four resolve into the code section.** So a gate reporting `ok` was in part reporting
that a damage divisor is a valid `.text` address, and being checked as a code citation.

> ### The disposition on the record is wrong and should be reversed
>
> `repos-78` called this *"harmless here"*. **On the single instance in front of them it was, and
> across the corpus it is not.** It bites hardest exactly where the writing standard is most
> insistent — *"write out every formula with its real constants"* — so **the documents that follow
> the standard most faithfully are the ones the gate lies about most**: `arm-catalogue-slice-C`
> (1/180), `attack-defense-preparation` and `ranged-weapon-recipes` (1/256).
>
> Saying this plainly matters because *"harmless"* is on the record, and a later session will find
> that word and stop looking. **One instance is a curiosity; 40 occurrences concentrated in the
> formula documents is a defect.** The catalogue is what lets the fortieth occurrence argue with the
> first, and a finding that stays in an inbox has no denominator.

**Of the 507 gained values, 48 resolve into no PE section at all.** Those are not a regression —
an address that resolves nowhere is precisely what the gate exists to report, and they have been
invisible. **Expect them as genuine findings on the first sweep**, not as noise.

### Ordering — and it is a precondition, not tidiness

`repos-c7` has folded my §7 argument into `PROPOSED-repos-c7-9` as a fourth item, and the ordering is
now explicit:

> **convention, then pattern, then sweep.**

Any other order manufactures a batch of false findings against documents that are correct. Convert or
widen first and **every correction trail in all 137 mixed documents becomes visible simultaneously
with no convention to absorb it** — including the one in `section-014.md` §4, which is already live.

### Why the guard must be two characters, not one — measured

The obvious simpler guard is `(?<!\.)` — *reject a match preceded by a period.* **It is wrong,
and it is wrong expensively.** `repos-d6` flagged that it would break something; their stated reason
(an address ending a sentence) does not hold — I tested it, and both guards handle
`ends the sentence. 003304A0 follows` identically, because a lookbehind only looks backward.

**The real reason is address ranges.** This database writes extents as `LO..HI`, and the second
address is immediately preceded by a period:

```
02CB7FD0..02CB8438      00266E42..00266E7B      003D8E50..003D8FF1
022D8F00..022D9500      01DFE000..01DFE160      0x007CF6C3..0x007CF6D1
```

Measured across the corpus, the one-character guard loses citations the two-character guard keeps —
and **the count drifts for the same reason §5's totals do** (we are writing ranges while counting
them), so the stable statement is the *shape*, not the number:

| measurement | lost | preceding two characters |
|---|---:|---|
| `repos-c9`, earlier | 29 | `..` in 29 of 29 |
| `repos-d6`, all 252 documents | 36 | `..` in 36 of 36 |
| `repos-c9`, full population, later | **41** | **`..` in 41 of 41** |

> **In every measurement, by both sessions, 100 % of the losses are preceded by `..`** — the upper
> bound of an `LO..HI` address range. Not one is anything else. That is the drift-proof form of the
> claim, and it is the one to carry.

`repos-d6` classifies 2 of theirs as decompiler pseudo-symbols (`uRam...01df09c8`) rather than
ranges, which is a fair split — those are arguably not citations the document asserts at all. **The
rest are body extents**, which is precisely the claim class `audit_crossrefs.py` re-checks as
`BODY DRIFT`: a guard that silently dropped every upper bound would blind that check to exactly the
half of an extent that goes stale.

**The counter-case was tested and does not exist.** `repos-d6`'s original worry — an address ending a
sentence — has **70 occurrences** of the form `. <address>` in the corpus, and **the one-character
guard keeps every one**, because a lookbehind sees the space, never the period. Both of us measured
70.

**The two-character lookbehind separates the two cases precisely**, and this is the whole reason it
is written that way:

| context | two chars before the match | verdict |
|---|---|---|
| `0.00555556` | `0` `.` — digit then period | **rejected** — a decimal fraction |
| `02CB7FD0..02CB8438` | `.` `.` — period then period | **kept** — a range end-point |

So the guard is not "reject after a period", it is **"reject after a digit-then-period"**, and the
distinction is worth 29 real citations. *(Correcting `repos-d6`'s justification, not their
conclusion — they were right that the naive form breaks something.)*

### Recommendation, for the coordinator

**One regex, both directions** — accept an optional `0x`, and reject a match whose preceding
character is a `.` that itself follows a digit:

```python
ADDR = re.compile(r"(?<![0-9]\.)(?:\b|0x)(0[0-9A-Fa-f]{7})\b")
```

**Normalising the corpus fixes neither half.** It cannot fix the float direction at all — those are
not addresses to normalise — and it makes the under-count direction worse before it makes it better
(see the correction-trail problem in §7).

and re-run the citation family across all 227 documents, because **2,856 citations have never once
been checked** and some of them will be wrong in the way mine was. I have converted only my own four
sheets, which is the conservative move and does not pre-empt the decision; the other 13 invisible
documents and the 137 mixed ones are not mine to touch. `repos-c7` and `repos-d6` have been told
directly; `repos-4b` and `repos-3f` are on `trial1` and unreachable from here.

**Do not treat the conversion as the fix.** Normalising the corpus makes today's documents visible
and leaves the trap armed for the next author who writes `0x`, which is the more natural form and is
what 137 documents already reach for.

## 6. Audit round 2 — `.ard` reader body (`repos-1e`). CONFIRMED on every instruction. One scoring defect.

Same method: capstone against the certified image, my own parser against the corpus. Never the
author's instrument.

### Everything load-bearing reproduces

| claim | independent result |
|---|---|
| binder `003EA710` reads exactly `+0x10 +0x14 +0x18 +0x24 +0x28 +0x2C` | ✅ **exact**, 73 instructions / 267 bytes |
| **zero references to `[rbp+0]`** — the `FF12AR03` magic is never validated | ✅ **0**, confirmed |
| every cited read site | ✅ `003EA73B`, `003EA743`, `003EA751`, `003EA7AD`, `003EA7BA`, `003EA7D6`, `003EA7E3`, `003EA789`, `003EA796` — all nine exact |
| `+0x1C` and `+0x20` never read | ✅ absent from the read set — and they are the two slots `repos-d6` measured absent in 166/166. **Corpus and instruction stream agree on which two.** |
| five registry slots via `0023A160` | ✅ **all five exact.** Resolved the `LEA`s myself: `0023A1B7`→`02EBF150`, `0023A1A8`→`02EBF168`, `0023A196`→`02EBF120`, `0023A187`→`02EBF148`, `0023A178`→`02EBF140` |
| category constants 0,1,2,3,4 at the five call sites | ✅ `003EA765 XOR ECX,ECX`, `003EA772 MOV ECX,1`, `003EA77F MOV ECX,2`, `003EA7CC MOV ECX,3`, `003EA7F5 MOV ECX,4` |
| path resolver `002DF980`, table-of-tables `0215F000` | ✅ `LEA R8,[rip+0x1E7F676]` from `002DF98A` resolves to `0215F000` exactly; namespace 21 is `+0xA8` |
| `archive_formats: ard` | ✅ `check_assets` `[x]`, no collision. **Legitimately claimed** — no other `.ard` sheet exists |

**The warning in §4 about the branch order is correct and worth repeating**: `0023A160` is a
`sub ecx,1` chain, so the cases appear in the reverse of source order and reading the printed order
gives the wrong slot for every category. I resolved each `LEA` independently and got their mapping.

### The one defect: the frontmatter withholds five declarations on a false premise

The sheet's frontmatter says:

> `# registry_slots are DELIBERATELY NOT declared here — all five already have owners; see §4.`

**No document declares any of the five.** Every `registry_slots:` block in the database, exhaustively:

| declared slot | declaring document |
|---|---|
| `0x02EBF0C0` | `13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md` |
| `0x02EBF0F8` | `12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md` |
| `0x02EBF138` | `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md` |
| `0x02EBF160` | `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` |
| `0x02EBF190` | `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md` |

That is the whole of `registry_explained`'s 5 / 63 numerator, and **`02EBF120`, `02EBF140`,
`02EBF148`, `02EBF150` and `02EBF168` are not among them.**

`repos-1e` used *"owns"* in the prose sense, and §8 names the documents it meant. Those documents do
describe the slots substantively — `the-encoded-id-class-registry.md` line 110 gives `02EBF120` as
*"a unit-definition table"* with its readers, line 112 the same for `02EBF150`;
`which-gambit-set-fires-and-how-a-command-switches-it.md` line 132 gives `02EBF168` as *"the
order-set directory"*. **But not one of them carries a `registry_slots:` block.**

The scoring rule is explicit that this is the distinction that counts — `COVERAGE.md` line 1675:

> *"`0x02EBF138` is mentioned in ten documents and explained in one. **A mention is not an
> explanation**, and a declared claim has an owner."*

**So `registry_explained` under-counts by five slots — it would double, 5 / 63 → 10 / 63.** The work
is done and written; the declaration is missing because a correct sheet deferred to owners that the
metric does not recognise as owners.

**Not mine to fix, and deliberately so.** One owner per slot, and I did not read
`BattleUnit_ApplyUnitDefinition` or the gambit path. This is a routing decision: either the four
prose documents declare their slots, or `repos-1e`'s sheet declares the five it established from the
instruction stream — which is the reading that most literally meets the bar *"declare it only where
your document establishes what the slot holds"*. **The wrong outcome is the current one, where five
slots are explained in prose by four documents and counted by none.**

### A cross-sheet result the two documents produce only together

`.ard` header slot 7 (`+0x2C`) → `FUN_003DCF00` → **`0x02B58178`**.
`section_019` slot 7 (`+0x2C`) → `FUN_003DCF10` → **`0x02B58180`**.

Both handlers are eight bytes, both are a single `MOV [rip+disp],RCX`, and the two globals are
**adjacent, 8 bytes apart**. So the same directory slot in the same format lands in two neighbouring
entries depending on which carrier delivered it — the `.ard` file or the `.ebp` container's slot 19.
`my section-019.md` cited `FUN_003DCF10` without naming its global; that is now named.

**And the two readers of one format differ in reach**: the `.ard` binder consumes six directory
slots and fills five registry categories; the `section_019` handler consumes **slot 7 only**. That is
consistent with the corpus — `section_019` has slots 5 and 6 absent in 271/271, so two of the five
categories would have nothing to bind — but it is the *readers* that differ, not just the data, and
neither sheet could have said so alone.

## 7. Supporting `repos-c7`'s `PROPOSED-repos-c7-9` — correction trails vs the citation sweep

`repos-c7` raises a consequence of my §5 recommendation that I should have seen and did not:
**every honest correction trail becomes a gate finding the moment the regex can see it.** A
was/is table naming a superseded address is indistinguishable, to any citation checker, from a claim.

**I already have a live instance.** `section-014.md` names `0037AA7F` in its correction record *as
the wrong value*, and `verify_doc_addresses.py` flags it on every run. I dispositioned it in-sheet —
a table in §4 saying what each of the three flagged addresses is and why it is not an error — but a
disposition is a per-document workaround, and the sweep will hit this across 227 documents in a
project that has been correcting citations all week.

**I support the convention landing before the sweep, not after.** Note also that this cuts against
converting the corpus: normalising addresses to bare form would make every correction trail in all
137 mixed documents visible at once, with no convention in place to absorb them.

`repos-c7`'s reasoning for **not** converting their sheets is better than my reasoning for
converting mine. They ran my check without changing their documents and got the safety benefit
without spending the coordinator's decision — and it found two real defects in `section-010.md`,
both from the same displacement-scan class as mine (`0032F073` → `0032F06F`, `0033163F` → `0033163B`),
including a document that **described one instruction two ways** in §3 and §4. My conversion was the
more invasive move and I would not repeat it before the decision is made.

## 8. A third silent-failure instance, found by making one of my own

While writing §5 I wrote a literal **backspace** into this file eight times: a `\b` in a regex,
passed through a shell heredoc that processed the escape. `check_source_hygiene.py` caught it, and
its own message is the best statement of the theme this whole round has been circling:

> *"A backspace inside a regex literal is not a syntax error: the pattern silently matches nothing,
> forever."*

**That is the same failure shape as the citation gate itself.** A broken pattern does not raise; it
returns an empty result that is indistinguishable from a clean one. My §5 recommendation, delivered
in a corrupted form, would have read as a valid regex and matched nothing — I would have recommended
a fix that silently disabled the gate I was trying to repair.

Fixed here and in my `ASSIGNMENTS.md` row (1 occurrence). **Both regexes in §5 are now correct and
were tested before being written down**:

| input | current regex | proposed regex |
|---|---|---|
| `0.00555556` | `00555556` ← spurious | *no match* |
| `1.01206005` | `01206005` ← spurious | *no match* |
| `0x003304A0` | *no match* ← missed | `003304A0` |
| `003304A0` | `003304A0` | `003304A0` |

### One left — and it is a corrupted tier-1 evidence anchor, not a hygiene nit

`check_source_hygiene.py` across all 254 documents now reports exactly one remaining occurrence:

```
Database/FFXII TZA/_index/_inbox/repos-1e.md
    line 690    BEL        `..\..\katano<BEL>telload.c`
```

**The `\a` of `\atelload.c` was consumed as an escape**, leaving a BEL byte where the `a` should be.
Same class as mine, different escape. It matters more than a stray byte usually would, because that
string is **tier-1 evidence** — it is the loader's own source filename, it is cited as such in
`repos-1e`'s work and in three of my sheets, and the corrupted form is what a future session would
grep for and fail to find.

**Why this is more than a stray byte.** That string is the **assertion-filename anchor for the whole
EBP/ATEL loader translation unit** — the thing that identifies `0x0032F520`-`0x00331E9F` as one
source file, which is how the container's dispatcher was found at all. It is cited in
`repos-d6`'s `section-016.md` (at `00D10958`), in three of my sheets, and in `repos-1e`'s own `.ard`
work. **A future session greps for it, gets nothing, and concludes the anchor is wrong or the address
stale** — distrusting good evidence because of a mangled escape in a handoff document. That is the
failure mode, and it is why this belongs in the report rather than in a hygiene footnote.
*(Framing owed to `repos-d6`, who pushed back on my first wording.)*

**The binary is fine; only the inbox text is corrupt.** `repos-d6` re-checked the string at
`00D10958` in the image and it is intact with a NUL either side, and my own `.rdata` dump of
`00D10900`-`00D10A0C` earlier this round read it correctly. So nothing downstream is wrong — the
anchor is good and one handoff copy of it is not.

`repos-1e` is on `trial1` and unreachable from `trial2`, and an inbox belongs to its session, so I
have not touched it; **the coordinator is the only route.** **My own four sheets and `section-014`'s
`atelload.c` citations were checked and are clean** — they were written with a file tool rather than
through a shell heredoc, which is the actual difference.

> **Generalise past the instance:** *any evidence string containing a backslash is unsafe through a
> shell or a non-raw literal*, and this database's evidence strings are largely **Windows paths**.
> `atelload.c` is simply the one quoted most often. `repos-c7`'s mitigation is the right shape — their
> append script **asserts the string survives before it writes**, which is a check at the point of
> writing rather than a warning to be careful, i.e. the rule in the tooling instead of in a note.

> **Generalisable, and cheap:** any Windows path or regex written through a shell heredoc is at risk,
> and `\a \b \f  \n \r \t \v` are all live escapes. `..\..\katano\atelload.c` contains `\a`;
> a regex containing `\b` is the other common case. **Write them with a file tool, or verify with
> `check_source_hygiene.py` before reporting.** The gate exists and is cheap; I ran it only because I
> was already running the post-write gates I owed.

## 9. Audit — `section-008.md` and `section-009.md` (`repos-4b`). The last of the row's debt.

Both were `PARTIAL` / `audit.passes: 0`. Corpus side was confirmed in §4; this is the **loader
contract** pass, using `repos-c7`'s stricter test — *not* "is this address in `.text`" but **"is this
an instruction boundary"**, established by decoding forward from the function entry.

### `section-008.md` — CONFIRMED, 23 of 23 citations exact

`CAMCTL_OnLoaded` (`0032FA10`, 40 instructions / 164 B) and `CML1_ResolveNames` (`003DA1F0`,
51 instructions / **205 B — the stated size, exact**). **Every cited address is an instruction
boundary and every instruction is what the sheet says it is.** A sample of the load-bearing ones:

| cited | instruction | sheet's claim |
|---|---|---|
| `0032FA2E` | `AND ECX,0xF` | slot = low 4 bits ✅ |
| `0032FA3B` | `MOV [R14+RCX*8+0x21A6D80],RDX` | `g_cmlBlob = 0x022C6D80[slot]` ✅ (`0x21A6D80 + 0x120000`) |
| `0032FA4F` | `CMP qword ptr [RAX+0xE0],0` | tests the `CAM7` blob ✅ |
| `0032FA6C` | `BTR RBX,8` | clears pending bit 8 ✅ |
| `003DA253` | `MOV EAX,dword ptr [R14+4]` | `count = blob[+0x04]` ✅ |
| `003DA270` | `MOVSXD RDI,dword ptr [RBX]` | name offset, **and it is signed** ✅ |
| `003DA28A` | `CALL 0x256530` | `CAM7_FindCameraByName` ✅ |

**This is the cleanest sheet I have audited this round**, and the reason is visible in the result:
its addresses came from a disassembler throughout.

### `section-009.md` — the conclusions are right; **8 of the anchors are wrong**

`CAM7_Load` (`002561C0`) is **498 bytes, exactly as stated**, and the magic check is exact:
`002561C8 CMP dword ptr [RCX],0x374D4143` ✅. **Both `Inert` claims are confirmed** — over the whole
body, header `+0x10/+0x14/+0x18` appear in no read set, and the record base `RBX` is read at
`+0x00 +0x04 +0x08 +0x24 +0x26 +0x28` but **never at `+0x20` or `+0x22`**.

**Every field the sheet says is read IS read. But the field table's `Read by` column points at
neighbouring instructions rather than the reading ones:**

| field | sheet cites | what is actually there | the real instruction |
|---|---|---|---|
| `+0x04` cameraCount | `002561D6` | `XOR EAX,EAX` — the **rejection** path, not a read | *(the `JE` at `002561D4` takes the match path; `002561D6` is `return 0`)* |
| `+0x1C` firstRecord | `0025624B` | **not an instruction boundary at all** | **`0025624D MOV EBX,dword ptr [RAX+0x1C]`** |
| rec name `strncpy` | `00256276` | `ADD RCX,[R12+RSI+0x10]` | **`0025627B CALL qword ptr [rip+0x66CCEF]`**, with `R8D=0x18` set at `00256270` |
| rec `+0x24` | `00256289` | `MOV RCX,[R12+RSI+0x10]` | **`00256281 MOVZX EAX,word ptr [RBX+0x24]`** |
| rec `+0x26` | `0025629A` | `MOV RCX,[R12+RSI+0x10]` | **`00256296 MOVZX EAX,word ptr [RBX+0x26]`** |
| `+0x08` countB | `002562EF` | `TEST RAX,RAX` | **`002562F4 MOV EBP,dword ptr [RAX+8]`** |
| `+0x0C` countC | `00256342` | `TEST RAX,RAX` | **`00256347 MOV ESI,dword ptr [RAX+0xC]`** |

`0025629F` is a boundary and is `MOV word ptr [RCX+RBP-0xE],AX` — the **store** of the `+0x26` value,
so citing it under a column headed *"Read by"* is at best the wrong half of the operation.

**The offsets are not consistent** — −2, +5, +8, +4, −5, −5 — so this is **not** the displacement-scan
class that produced my own `0037AA7F` and `repos-c7`'s two. A fixed back-off leaves a fixed error.
This looks like addresses transcribed from a decompiler view, where a C line maps to a span of
instructions and any address in the span looks equally right.

**Same author, same round, and `section-008` is perfect** — which is the diagnostic. The difference
is not care, it is which instrument the addresses came from.

**Why it matters even though every conclusion survives**: the project's own standard is that *an
instruction anchor is what distinguishes a read from a mention for every instrument this project
has.* An anchor pointing at the adjacent instruction defeats `verify_doc_addresses.py`,
`audit_crossrefs.py`'s `BODY DRIFT` check, and any future re-derivation — silently, because the
address still resolves and still lands inside the right function. **The claims are sound and the
evidence trail does not lead to them.**

`repos-4b` is on `trial1` and unreachable from `trial2`. **I have not edited their sheet**; the
corrected addresses above are exactly what they need and this is the coordinator's to route.
`section-009.md` should reopen for the anchors, not for its findings.

> **Both sheets are also among the 17 documents whose citations are 100 % invisible** (§5), which is
> why none of this surfaced earlier: `section-008.md` presents 62 addresses to the gates and
> `section-009.md` 46, and both currently present **zero**. The `009` defect has been sitting behind
> a gate that could not see it.

## 10. UPDATE 2026-09-04 — the fix landed, then changed again. CORRECTED.

**`verify_doc_addresses.py` has been widened**, credited in its own comment to this session. The `0x`
blind spot in §5 is **fixed** and that recommendation is superseded.

### CORRECTION — the first version of this section was measured against a stale file

**What was believed** (this section, written earlier today): that the landed pattern was
`(?<![0-9A-Fa-fx])(?:0x)?(0[0-9A-Fa-f]{7})(?![0-9A-Fa-f])`, that it still matched decimal fractions,
and that `0.00555556` / `0.00390625` / `0.0078125f` were being credited as **interior** citations of
`00555400` / `00390390` / `00781240` — three functions cited nowhere else, sitting in
`engine_explained`'s numerator.

**What is now believed:** all of that was true of the file I read, and **the file changed underneath
me.** `verify_doc_addresses.py` has `mtime 2026-09-04 13:59:03` and the live pattern carries a `.`
inside the lookbehind class:

```
ADDR = re.compile(r"(?<![0-9A-Fa-fx.])(?:0x)?(0[0-9A-Fa-f]{7})(?![0-9A-Fa-f])")
```

**What proved it:** re-reading the file and re-running every case. Under the live pattern
`0.00555556`, `0.00390625`, `1.01206005` and `0.0078125f` all yield **nothing**, and I confirmed the
consequence directly — `00555556` and `00390625` are **no longer in the cited set** of
`arm-catalogue-slice-C` or `attack-defense-preparation`.

> **So the `engine_explained` contamination retires itself.** Those three functions are no longer
> credited. **The finding is dead and I am recording it rather than deleting it**, because it was
> true of a real program state and the reasoning that produced it is what found the live defect
> below.

**Why the earlier reading was reachable:** I read the pattern, ran the gate, and reported — over a
window that spanned the edit. **This is the same drift that has been chasing every measurement
tonight, applied to the instrument instead of the corpus.** A figure that goes stale through the
measurer's own writing (§5) and a figure that goes stale through someone else's edit are the same
defect; I had written up the first and then walked into the second. *A tool's behaviour needs its
timestamp exactly as much as a corpus measurement does.*

### The live defect: the one-character guard fixes floats and breaks ranges

`(?<![0-9A-Fa-fx.])` rejects **any** match preceded by a period. It cannot tell `0.` from `..`, so it
is precisely the one-character guard this report argued against before it existed.

| input | live pattern | the two-character form |
|---|---|---|
| `0x003304A0` | `003304A0` ✅ | `003304A0` ✅ |
| `0.00555556` | *(none)* ✅ | *(none)* ✅ |
| `02CB7FD0..02CB8438` | **`02CB7FD0` only** ❌ | both ✅ |
| `0x007CF6C3..0x007CF6D1` | **`007CF6C3` only** ❌ | both ✅ |

**Measured against the current file: the live pattern loses 51 occurrences, 24 distinct addresses,
across 15 documents — and the preceding two characters are `..` in 51 of 51.** Not one is anything
else. *(`repos-d6` measures 43 occurrences / **24 distinct** — the distinct count matches exactly and
the occurrence count drifts, as everything has tonight.)*

**Every one is the upper bound of an `LO..HI` address range** — `003D8E50..003D8FF1`,
`022D8F00..022D9500`, `01DFE000..01DFE160`, `00266E42..00266E7B`, `02CB7FD0..02CB8438`,
`0x007CF6C3..0x007CF6D1`.

> **A range's upper bound is how this project states a body extent**, which is exactly the claim
> class `audit_crossrefs.py` re-checks as `BODY DRIFT`. **The half being silently dropped right now
> is the half that goes stale.**

### The remaining recommendation — it has flipped

Not *"add float rejection"*. **Restore the range bounds**, with the two-character guard that keeps all
three properties at once:

```
ADDR = re.compile(r"(?<![0-9]\.)(?<![0-9A-Fa-fx])(?:0x)?(0[0-9A-Fa-f]{7})(?![0-9A-Fa-f])")
```

**Verified over the whole database, and the team has converged on one pattern.** `repos-c7` reached
the same fix independently with the two lookbehinds in the opposite order; lookbehinds at the same
position commute, and I measured the **symmetric difference over every `.md` as exactly 0** — the two
are the same pattern. Against the live one it **recovers 60 occurrences (26 distinct) and loses 0**.
*(`repos-c7` measures 58 recovered; same drift, and "loses 0" is identical in both.)*

| case | live | recommended |
|---|---:|---:|
| `0x003304A0` / `003304A0` | 1 / 1 | 1 / 1 |
| **`FUN_002DF9A0`** | **1** | **1** |
| **`DAT_02b59d48`** | **1** | **1** |
| `0.00555556` / `0.0078125f` | 0 / 0 | 0 / 0 |
| `02CB7FD0..02CB8438` | **1** | **2** |
| `` `0x0037DB10`..`0x0037DB25` `` | 2 | 2 |

> ### DO NOT use the `\b` variant — it misses 2,331 occurrences
>
> The form recommended in §5, `(?<![0-9]\.)(?:\b|0x)(0[0-9A-Fa-f]{7})\b`, is **wrong and must not be
> submitted**. `_` is a **word character**, so `\b` never fires before the digits in `FUN_002DF9A0` or
> `DAT_02b59d48` — **the dominant citation form in this database.** Measured: the `\b` variant finds
> 34,745 occurrences against the recommended form's 37,076, **missing 2,331**. Repairing a
> 51-occurrence range regression at a cost of 2,331 `FUN_`/`DAT_` citations is a far worse trade than
> the defect it fixes. *(Cause found by `repos-c7`, relayed by `repos-d6`, verified here.)*

**A correction to the narrowing that reached me:** it was relayed that the range loss hits *bare*
ranges only because `0x`-prefixed ones survive. **That is not the discriminator — backticks are.**

| spelling | live |
|---|---:|
| `02CB7FD0..02CB8438` | loses the upper bound |
| `0x0037DB10..0x0037DB25` | **also loses it** |
| `` `02CB7FD0`..`02CB8438` `` | survives |
| `` `0x0037DB10`..`0x0037DB25` `` | survives |

A backtick immediately before the digits satisfies the lookbehind; a `.` does not. So the loss hits
**un-backticked ranges**, with or without `0x` — and all 60 recovered occurrences are preceded by
`..`, confirming the shape.

**The regression is also silent rather than loud**, because `main()` returns 0 unconditionally: it
**under-counts**, which is the same failure class as the original `0x` blindness, not a noisier one.

### A separate live defect: the docstring claims an exit code the code deliberately does not produce

Line 16 of `verify_doc_addresses.py` states *"Exit code 1 if any cited address fails to resolve."*
`main()` ends `return 0` unconditionally (line 235), and it exits 0 across every document.

#### CORRECTION — my "report, not a gate" framing was too strong, and so was my count

**What I wrote earlier:** that the script *"is a REPORT, not a GATE, it cannot go red"*, that it has
no adverse path, and that it is **"1 of 11"** checkers with no failing state.

**What is now established, after reading the body rather than grepping it:**

1. **The `return 0` is deliberate, and the reason is three lines above it** (216–217):
   > `# a .text address that is neither a function nor interior is worth a human look,`
   > `# but jump tables legitimately live there -- report, do not fail.`

   **There IS an adverse path** — `text-data` raises a per-document `REVIEW` line (218–222). A jump
   table after a function legitimately lives in `.text`, so failing on it would make the gate
   *wrong*, not stricter. **So the docstring is the defect, not the design.** *"The code contradicts
   its docstring"* and *"the code lacks a capability its docstring claims"* call for **opposite**
   repairs, and only reading the body separates them. *(Correction owed to `repos-c7` via
   `repos-d6`; verified here.)*

2. **My "1 of 11" was wrong** — it came from a whole-file `grep` for non-zero returns over a
   hand-picked subset, which counts helper returns as exit paths. Re-measured with an AST, scoped to
   each script's `main()`, over **all 47 scripts in the kit that have one**:

   | | |
   |---|---|
   | provably cannot return non-zero | **5** — `verify_doc_addresses`, `audit_inbox_backlog`, `gen_address_index`, `fas2_export`, `watch_team` |
   | of those, **advertising an exit code** in the docstring | **1 — `verify_doc_addresses.py`, line 16** |

   *(`repos-d6` reports 2 of 25 on a different scoping; the counts differ and the conclusion does
   not.)* **The precise statement is: it is the only script in the kit that advertises an exit code
   it cannot produce.** That is a one-line docstring fix, not a redesign.

   > **Both of us produced a broken version of this measurement before a working one** — `repos-d6`'s
   > first two attempts counted a helper returning a dict as an exit path and reported *"0 of 25
   > cannot fail"*, **a clean sweep from a check that could not fail.** Mine over-counted in the same
   > direction. The measurement of "which checks can fail" is itself easy to write so that it cannot.

#### The real gap that survives: `unwind-BANNED` is reported globally and names no document

The documented *report-do-not-fail* rationale covers **`text-data` only**. Counting every line each
bucket appears on:

| bucket | lines | per-document output? |
|---|---|---|
| `text-data` | 149, 171, **218**, 231 | **yes** — `review = b.get("text-data", [])` → a `REVIEW` line naming the document |
| **`unwind-BANNED`** | **176, 231 only** | **NO** — the append, and the global summary loop. Nothing else. |

**`unwind-BANNED` is the banned-evidence rule wired into the instrument, and it is the one bucket
with no per-document line.** A full sweep prints `3  unwind-BANNED` and **names no document**.
`repos-d6` had to write a separate scan to find them:

```
00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md                   03000000
24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/…                02F98000
99-Unresolved-Residual/the-unresolved-158.md                              02FAE428
```

`.pdata`/`.xdata` as evidence is the project's most absolute prohibition — it cost a prior branch
**182 classifications**. **Whether those three are violations or legitimate citations *of* the ban is
unsettled and neither of us has settled it**; the instrument defect is that **nobody can tell without
writing a new scan.** Give `unwind-BANNED` the same per-document `REVIEW` treatment `text-data`
already has, and the question answers itself on the next run.

### `repos-d6`'s other objection, checked and already handled

Their proposed "third clause" — classify out-of-range values as non-addresses — **is already
implemented.** Line 169 buckets them as `literal`, *"not an address at all (quoted bytes)"*, and
**111 are counted database-wide**. My own count of newly-admitted out-of-range values is **194
occurrences / 53 distinct** against their 140 / 66, and the largest single value is
**`0x00120000`, the image base, at 80 occurrences**, which they did not list. All bucketed `literal`,
all harmless.

## 11. NEW ROW 2026-09-05 — `registry_explained`. The per-slot binder is found.

**Row taken** after clearing audit debt: `registry_explained` is COMPLETION-PLAN §6 item 3, *"the
highest value per unit of work in the plan"*, and no session was on it. It had also **moved 5 → 9 /
63 while I was writing** — `repos-1e` declared the four `.ard` slots after my §6 routing finding, so
that finding is banked. `02EBF168` remains explained-in-prose and declared by nobody.

### This closes an open question in `authored-data-table-registry.md`

That document, §8c, records: *"nothing read shows the binding cadence per slot"*, and its line 473
observes each slot has **many reads plus exactly one `LEA` — address taken once, by "the binder"** —
without identifying which function that is. Its §8d reads a binder *"partially"*, and the one it
reads is the **area-data** binder (`repos-1e`'s `.ard` path, `0023A160`).

**It is a different function.** The `LEA` that takes each slot's address once is in
**`FUN_00236C30`, 176 instructions / 1,037 bytes**, and it binds **36 slots in one pass** from a
single blob.

### The mechanism

```
rax = [0208E680]                       ; the "STATIC" authored-data blob
lea  rcx, [02EBF0xx]                   ; the registry slot -- this is the one LEA per slot
movsxd rdx, dword ptr [rax + N]        ; a u32 field at a FIXED offset in the blob
call FUN_003845F0                      ; bind(slot, field)
```

**Every slot is bound from a fixed `u32` field of one blob**, so the registry is that blob's own
header directory resolved into runtime pointers. Three shapes occur: `FUN_003845F0` (33 slots),
`FUN_003846F0` with an extra `r8d = 0` (2 slots — 43 and 45), and **one direct store with no binder
at all** (slot 47, `00236C74`, taking `[rcx+4]` before the blob pointer is even loaded).

Five further sites in the same function pass a blob field to a function **without** a registry slot
(`+0x20`→`00238880`, `+0x38`→`00238160`, `+0x3C`→`00237FC0`, `+0x40`→`003847B0`,
`+0xa0`→`00238660`), so the blob header carries more fields than the registry has slots.

### The complete slot ↔ blob-field directory, 36 slots

Derived by disassembling the whole body with capstone and pairing each `lea [slot]` with the
`movsxd` immediately before its `call`. Blob fields run `+0x04` … `+0x118`.

| slot | address | STATIC field | bound by | site |
|---:|---|---|---|---|
| 0 | `02EBF008` | `+0x118` | `003845F0` | `00237010` |
| 1 | `02EBF010` | `+0x114` | `003845F0` | `00236FF6` |
| 2 | `02EBF018` | `+0xc` | `003845F0` | `00236C7F` |
| 3 | `02EBF020` | `+0x70` | `003845F0` | `00236DFC` |
| 4 | `02EBF028` | `+0xf0` | `003845F0` | `00236FBC` |
| 5 | `02EBF030` | `+0xf4` | `003845F0` | `00236FA2` |
| 6 | `02EBF038` | `+0x34` | `003845F0` | `00236D5C` |
| 7 | `02EBF040` | `+0xec` | `003845F0` | `00236F88` |
| 8 | `02EBF048` | `+0xac` | `003845F0` | `00236F54` |
| 9 | `02EBF050` | `+0xa8` | `003845F0` | `00236F3A` |
| 10 | `02EBF058` | `+0xe8` | `003845F0` | `00236F6E` |
| 11 | `02EBF060` | `+0x74` | `003845F0` | `00236E13` |
| 12 | `02EBF068` | `+0x9c` | `003845F0` | `00236F0E` |
| 13 | `02EBF070` | `+0x98` | `003845F0` | `00236EF4` |
| 14 | `02EBF078` | `+0x94` | `003845F0` | `00236EDA` |
| 15 | `02EBF080` | `+0x90` | `003845F0` | `00236EC0` |
| 16 | `02EBF088` | `+0x8c` | `003845F0` | `00236EA6` |
| 17 | `02EBF090` | `+0x88` | `003845F0` | `00236E8C` |
| 18 | `02EBF098` | `+0x84` | `003845F0` | `00236E72` |
| 19 | `02EBF0A0` | `+0x80` | `003845F0` | `00236E58` |
| 20 | `02EBF0A8` | `+0x14` | `003845F0` | `00236CA9` |
| 21 | `02EBF0B0` | `+0x18` | `003845F0` | `00236CC0` |
| 22 | `02EBF0B8` | `+0x10` | `003845F0` | `00236C92` |
| 23 | `02EBF0C0` | `+0x1c` | `003845F0` | `00236CD7` |
| 24 | `02EBF0C8` | `+0x6c` | `003845F0` | `00236DE5` |
| 27 | `02EBF0E0` | `+0x24` | `003845F0` | `00236CFD` |
| 28 | `02EBF0E8` | `+0x7c` | `003845F0` | `00236E41` |
| 29 | `02EBF0F0` | `+0x78` | `003845F0` | `00236E2A` |
| 31 | `02EBF100` | `+0x4c` | `003845F0` | `00236DCE` |
| 32 | `02EBF108` | `+0x28` | `003845F0` | `00236D14` |
| 33 | `02EBF110` | `+0x30` | `003845F0` | `00236D45` |
| 36 | `02EBF128` | `+0x48` | `003845F0` | `00236DB7` |
| 37 | `02EBF130` | `+0x44` | `003845F0` | `00236DA0` |
| 43 | `02EBF160` | `+0x2c` | `003846F0` | `00236D2B` |
| 45 | `02EBF170` | `+0xf8` | `003846F0` | `00236FD6` |
| 47 | `02EBF180` | `+4` | `direct store` | `00236C74` |

**Cross-check against the two slots whose meaning was already known independently:**

| slot | address | this table says | already documented as |
|---:|---|---|---|
| 23 | `02EBF0C0` | `STATIC+0x1C` | loot / enemy chain (`loot-drops-and-enemy-chain.md`) |
| 43 | `02EBF160` | `STATIC+0x2C`, via the `FUN_003846F0` variant | the gambit order-set directory (`gambit-evaluation-and-enmity.md`) |

Both fall where the table predicts, and slot 43 is one of only two using the variant binder — which
is a **shape** agreement, not just an address agreement.

### Where the blob comes from — partially established, and one reading falsified

`0208E680` has exactly **one writer**: `002369B4`, inside `FUN_002368D0`. That function allocates the
battle work areas — `count * 0xF50` tagged `"BtlWork"`, and two `0x9400` blocks tagged
`btlKeepCharWork1` / `btlKeepCharWork2` — then **frees and nulls `0208E680`** and issues

```
002369BB  LEA R8, [009146A8]      ; "STATIC"
002369C2  MOV ECX, 0x13
002369C7  LEA RDX, [00238850]     ; the completion callback
002369CE  CALL FUN_003843F0
```

So the blob is requested under the tag **`"STATIC"`** and installed by the callback at `00238850`.

> **A reading I tried and killed.** `ECX = 0x13 = 19` looks like a resource *namespace*, which would
> make this the same `(namespace, index)` mechanism `.ard` uses at namespace 21. I built the
> namespace → path-table map from `FUN_002DF9A0` (41 namespaces, each a `lea` immediately before its
> `mov [0215F000 + ns*8]`) and read namespace 19's table at `01E94B50`. **It contains NPC model
> paths** — `PS2Data\obj_finish\in\npc\n10\n1059\n1059.cm` and siblings — which does not fit a
> single static authored-data blob. **So `0x13` is not established as a namespace here**, and the
> `"STATIC"` tag is passed separately as `R8`. Recorded as a dead reading rather than left implicit.

### What I am NOT declaring, and why

**No `registry_slots` declarations from this work.** The bar is *"declare it only where your document
establishes what the slot holds"*, and what I have established is **where each slot is bound from**,
not what its table contains. `STATIC+0x88` is a provenance, not a meaning. Declaring 36 slots on a
binding would be precisely the count-match error the `st2e` sheet caught itself making on `AY-6`.

**What it does buy** is that any future reader of one slot now knows exactly which blob field to
follow, and the two independently-documented slots landing where the table predicts is real
corroboration for the other 34.

### Routing — this belongs in an existing document, not a new one

`authored-data-table-registry.md` owns this subject, declares `02EBF138` / `02EBF190`, and carries
the open question this closes. **I have not edited it**, and I am not writing a competing sheet — a
second registry document is exactly the collision that produced the duplicate `.nmb` sheet earlier in
this round. Its frontmatter is also stale (`verified_against: gzf 2ed8affb…` = **GN158**;
`last_reviewed: 2026-09-02`), so it needs a reopen for provenance regardless. **Coordinator's to
merge or to assign back to me.**

## 12. A fourth escape-mangling instance — and this one the hygiene gate CANNOT catch

Writing §11 I mangled the same class of string a fourth time, and it is the variant that matters
most, because **`check_source_hygiene.py` is structurally unable to detect it.**

The Windows path `PS2Data\obj_finish\in\npc\n10\n1059\n1059.cm` contains `\n` **four times**. Through a shell heredoc
those became **four real newline characters**, silently splitting the path across five lines
inside a code span.

> **The gate scans for stray control bytes and skips `\t`, `\n`, `\r` — because those
> are legitimate content.** So `\a` → BEL and `\b` → BACKSPACE are caught (both were,
> earlier tonight), and **`\n` → newline is invisible to it, in exactly the file type where a
> newline is meaningful.** A path corrupted this way reads as a formatting glitch, not as damage.

**The escapes divide into two classes, and only one is covered:**

| escape | becomes | `check_source_hygiene` sees it? |
|---|---|---|
| `\a` `\b` `\f` `\v` `\0` | BEL, BACKSPACE, FF, VT, NUL | **yes** — flagged |
| **`\n` `\r` `\t`** | **newline, CR, tab** | **NO — legitimate content, skipped by design** |

This database's evidence strings are **Windows paths**, and `\n` is common in them —
`\npc`, `\n10`, any directory or file beginning with `n`. `..\..\katano\atelload.c`
was caught because `\a` happens to fall in the covered class; **`\npc` would not have been.**

> **This section demonstrated its own subject.** The first version of it was written through a
> heredoc and arrived with NUL, BEL, VT and FF in the escape table — caught by the gate — **and
> with its `\n`, `\r` and `\t` cells silently converted to real whitespace, which the
> gate passed as clean.** Both halves of the finding, produced by the finding.

**What actually protects against it:** `repos-c7`'s shape — an assertion at the point of writing
that the string survives — or building the text from character codes rather than literals, which is
how this section is now written. **Not the gate.** I found it by re-reading my own rendered output,
which is the check that has caught every one of these tonight.

## 13. NEW ROW 2026-09-05 — the 09-03 audit backlog. First pass: instruction-boundary sweep.

**Row taken from the rewritten board.** The backlog is defined as `last_reviewed: 2026-09-03` with
`audit.passes: 0`, excluding my own four. The board says **31**; I measure **30** — one was audited
between the board being written and my run (`repos-4b` is working `section-012`/`010`/`011`). *Same
drift as everything else this round: the population moves while it is being measured, so the figure
carries its timestamp — 2026-09-05.*

### The instrument

**Not** *"is this address in `.text`"* — that passes anything in an 8 MB section. The test is
**"is this address an instruction boundary"**, established by decoding forward from the containing
function's entry (from `functions.tsv`) and requiring the citation to land on an instruction start.
*(Instrument shape owed to `repos-c7`, who applied it to their own sheets after my `0037AA7F`
correction.)* Script: `Tools/work/repos-c9/boundary.py`, run over all 30 in one pass.

**Result: 1,309 distinct citations checked, 9 not a boundary, across 6 documents.**

### Disposition — silence is not disposition, so all nine

**Five are not defects:**

| citation | document | why it is fine |
|---|---|---|
| `002AE32F` | `the-text-control-code-language.md` | a **body extent** — the sheet says *"the body ends at `002AE32F` (`002AE32C jmp` is its last instruction)"*. One-past-the-end, same class as `003306DA` in my own `section-014` |
| `003590C3` | `active-party-reserve-…` | **the document already dispositions it** — *"a false positive in the same run (`003590C3`, a float read mid-instruction)"*. My checker independently rediscovered a known, recorded false positive, which is a good sign for the checker |
| `0032F073`, `0033163F` | `section-010.md` | **a correction trail.** `repos-c7` fixed both and kept the superseded values in a was/is table. This is `PROPOSED-repos-c7-9` live in the corpus — a citation checker cannot tell "cited as a claim" from "cited as a value that was wrong" |
| `002561CA` | `section-009.md` | defensible — it is where the **bytes** `CAM7` live, inside the `CMP` at `002561C8`. Citing a byte location is not citing an instruction |

**Four are real, in three documents. None is mine.**

**1. `what-the-console-tunes.md` — a quoted disassembly listing with a wrong address.**

```
the sheet says      0016242A  E9 60 67 6A 00   jmp  atexit
the binary has      0016242B  E9 60 67 6A 00   jmp  0x00808B90
```

**The five bytes match exactly; the address is one low.** `0016242A` is the last byte of the
preceding `ADD RSP,0x28` (`4883c428` at `00162427`). The listing's content is right and its anchor
is not — which is the failure mode that survives every check except this one.

**2. `the-widget-constructor-and-object-sizes.md` — both "globals" are wrong, in two different ways.**
The sheet's §7 asks: *"What the two globals at `0024665F` and `00246753` gate."*

- `0024665F` is the **imm8 byte** of `00246659 CMP dword ptr [rip + 0x1E48F00], 0`. The global that
  instruction tests is **`0208F560`** (`00246660 + 0x1E48F00`), which is the address the question
  should carry.
- `00246753` **is** an instruction boundary — and it is `CALL 0x00314960`, **not a global at all.**

So it passed the boundary test and is still mis-described. **A boundary check is necessary and not
sufficient**: a citation can be a valid instruction address and still be the wrong *kind* of thing.
The question itself is sound — there *is* a gate there — but neither anchor points at it.

**3. `section-009.md` — a fifth wrong anchor, on top of the eight in §9.**
The sheet says *"`cameraCount == 0` with `slot < 5` returns **1** at `0x002561E4`"*. `002561E4` is
mid-instruction (`002561E0 MOV qword ptr [RSP+0x50],RBX` spans it). And the nearby return is
`002561D6 XOR EAX,EAX` / `002561DF RET`, which returns **0**, not 1 — the magic-mismatch path I
identified in §9. **So both the anchor and the value need re-deriving.** `repos-4b` is on `trial1`
and unreachable; this joins the eight already reported.

### What the sweep says about the backlog as a whole

**1,300 of 1,309 citations land exactly.** The nine exceptions cluster in a way that matches the
instrument split found in §9: every real defect is in a document whose addresses came from a
**decompiler view or a hand-transcribed listing**, and none is in one whose addresses came from a
disassembler. `choosing-the-render-target-for-a-text-run.md` is **71 / 71 exact** — the cleanest in
the set.

**This is a first pass, not a finished audit.** A boundary check tests whether an anchor points at an
instruction; it does not test whether the instruction says what the sheet claims. That is the second
pass, and it is where §9's `section-009` result came from — the anchors were checkable, the *claims*
needed the read.

## 14. Backlog pass 2 — do the claims match the instructions?

Pass 1 asked whether an anchor points at an instruction. **Pass 2 asks whether that instruction says
what the document says it says.** Instrument: `Tools/work/repos-c9/claimcheck.py` — it extracts
`(address, claimed-mnemonic)` pairs from prose and compares against a disassembly of the containing
function.

**Result over the 30 backlog documents: 340 checkable claims, 339 correct, 1 real defect.**

### The defect — a hand-transcribed listing whose third row is wrong

`19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md`
carries this block:

```asm
00233C4D  cmp dword ptr [rax], 0x5071901
00233C53  je  0x233C5E                     ; matched -> proceed
00233C55  jmp 0x237DF0                     ; otherwise -> the reinitialise path
```

The binary has:

```
00233C4D  cmp dword ptr [rax], 0x5071901    <- correct
00233C53  je  0x233c5e                      <- correct
00233C55  add rsp, 0x28                     <- the document skips this instruction
00233C59  jmp 0x237df0                      <- the jmp is HERE, four bytes later
```

**The claim is right and the transcription is not.** *"Matched → proceed, otherwise → the
reinitialise path"* is exactly what the code does; the sheet omits the stack teardown and gives the
`jmp` the address of the `add`. Nothing downstream of the claim changes — which is precisely why it
survived until something compared the row against the bytes.

**This is the second instance of the class in this backlog**, after `what-the-console-tunes.md`'s
`0016242A` (§13), and both behave the same way: **a quoted listing whose content is right and whose
addresses are off.** Neither document is mine; both are `trial1`-authored and unreachable from here.

### Everything else survived, and the near-misses were my instrument

The first version of this check reported **9 mismatches**. Every one of the eight I discarded was a
defect in the extractor, not in a document, and both classes are worth writing down because anyone
building this check will hit them:

1. **The English word "and" matches the `AND` instruction.** Case-insensitively, *"`001C3D50` and
   `001C7940` are the same two functions"* parses as *"an `AND` instruction at `001C3D50`"*. Three
   false reports in one document came from that sentence alone; `or`, `not`, `call` and `add` are the
   same hazard. **Fixed by requiring an operand to follow the mnemonic.**
2. **A document may anchor a SEQUENCE to its first address.** `the-field-runtime-pass.md` writes
   *"`lea rdi, [→02098E10]`, `imul rbx, r14, 0x288` at `0025D9EF`"* — and it is **correct**: its own
   listing shows `lea` at `0025D9EF` and `imul` at `0025D9F6`. Taking the *last* mnemonic before
   "at" manufactures a mismatch against the first instruction. Same for
   `the-encoded-id-class-registry.md` (`lea` / `cmp` / `ja` at `00322C5A`) and `section-008.md`
   (`cmp` / `jbe` at `00330593`–`00330597`, where the sheet gives the **range** and is right).

**I re-ran and hand-checked every one before discarding it**, because an instrument whose output
becomes a defect claim about someone else's document must under-report rather than over-report. The
9 → 2 → 1 sequence is the instrument being corrected, not the documents improving.

### Backlog audit, both passes combined

| pass | checked | flagged | real defects |
|---|---:|---:|---:|
| 1 — is the anchor an instruction boundary? | 1,309 citations | 9 | **4**, in 3 documents |
| 2 — does the instruction match the claim? | 340 claims | 9 → 1 after correcting the instrument | **1**, in 1 document |

**Five real defects across four documents, out of thirty audited — and not one of them changes a
conclusion.** Every defect is an *anchor*: a wrong address, a mis-typed listing row, a global that is
really an imm8 byte. That is a consistent picture of this backlog: **the readings are sound and the
citation layer is where the errors live** — which is exactly the layer every downstream instrument
depends on and no human reader checks.

## 15. The remaining owing documents — 2026-09-06

The 09-03 backlog is closed (§13–§14). Re-censused what is still owing: **6 documents** with
`audit.passes: 0`, excluding my own four and the 30 already done — three 09-02 stragglers and three
landed today. **Also checked and clean: 0 documents claim a pass without naming a program state**,
so the board's *"a pass is not a counter bump"* rule is holding across all 193 documents.

Both instruments run over all six: **421 citations checked for instruction-boundary, 97
`(address, mnemonic)` claims checked against the binary.** Three flags, all dispositioned.

### The defect — a third listing anchored to the function entry

`18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md` carries:

```
002DF220  cmp  ecx, -1        -> return 0
```

The binary at `002DF220` is the **prologue** — `MOV qword ptr [RSP+8],RBX` — and the compare is at
**`002DF236`**:

```
002DF220  mov  qword ptr [rsp + 8], rbx     <- the entry
002DF236  cmp  ecx, -1                      <- the compare the sheet describes
002DF239  je   0x2df244
```

**The claim is right** — the function does refuse `-1` — and the anchor is the function entry rather
than the instruction. **Third instance of this exact class in my audit**, after
`what-the-console-tunes.md` (`0016242A`) and `version-stamps-and-what-loading-normalises.md`
(`00233C55`).

> **Three documents, three different authors, one failure mode: a hand-written listing whose first
> column is the function entry or a neighbouring byte rather than the instruction's own address.**
> It never changes a conclusion and it defeats every re-derivation, which is why it survives. **This
> is a writing-standard gap, not three unrelated slips** — worth a line wherever listings are
> specified, because the fix is mechanical: paste addresses from the disassembler, never type them.

### Two flags that are NOT defects — and are good practice

`tim2-images-and-the-seven-slot-registry.md` cites `001F43DA` and `002561CA`, neither an instruction
boundary. **Both are deliberate.** The sheet's §6 argues that `TIM2` appears 0 times in `.text`
because the check is a `memcmp` against `.rdata`, and it backs that with **positive controls** —
pointing at where *other* magics genuinely do appear as compare immediates:

| citation | the instruction containing it | what it proves |
|---|---|---|
| `001F43DA` | `001F43D7 CMP dword ptr [RBP+0x50],0x4B5952` — the `SRYK`/VBF magic | the scan can find a magic when one is there |
| `002561CA` | `002561C8 CMP dword ptr [RCX],0x374D4143` — `CAM7` | same, second control |

**Citing the byte offset of a magic inside its own compare instruction is the correct citation**, and
the evidence standard *requires* positive controls on an absence claim. A boundary checker cannot
tell this from an error; a reader can. **Recorded so the next sweep does not re-flag them.**

### Cross-document check — `tim2` against my own `section-006`

The new sheet and `Sections/section-006.md` describe the same registry from opposite ends, so a
disagreement would reopen both. **They agree on every point of contact:** `FUN_0039BEC0` is the gate,
the table is at `0x02AEE810`, the scan runs `1 .. 7` so **index 0 is never used**, and the `+0x40`
low-nibble gate is real.

**And I can supply the half the sheet says it lacks.** It states plainly *"No file was opened, and §5
says what that leaves unmeasured."* I opened 67 — every `section_006` TIM2 block in the `.ebp`
corpus — and the measurements it is missing are:

| the sheet's gate | my corpus result |
|---|---|
| the 4-byte `memcmp` against `TIM2` | passes **67 / 67** |
| the low-nibble gate on `+0x40` | `(u32 & 0xF) == 1` in **67 / 67** |
| version byte | `4` in 66 / 67 — **one file carries `0xD8`**, and `FUN_0039BEC0` never reads the field, so the engine cannot see it |
| `format` byte | `0` in 67 / 67, which is what puts the picture header at `+0x10` |

**Its §3 contract is confirmed against real files.** This is corroboration from a different
population, not agreement between two readings of the same instructions — the sheet reads the loader,
I read the data.

### Status of the six

| document | boundary | claims | verdict |
|---|---|---|---|
| `spawn-placement-height-and-authored-tunables.md` | 139, 0 bad | 53, 0 bad | **clean** |
| `how-a-sound-request-becomes-a-voice.md` | 207, 0 bad | 25, **1 bad** | one anchor defect, above |
| `animation-channel-binding-and-transform-composition.md` | 36, 0 bad | 0 pairs | **clean**; almost all citations are outside `.text`, so this pass says little about it |
| `chse-character-se-tables.md` | 2, 0 bad | 0 pairs | too few citations to test — noted, not cleared |
| `lmap-menumap-location-graph.md` | 2, 0 bad | 0 pairs | same |
| `tim2-images-and-the-seven-slot-registry.md` | 33, 2 flagged | 19, 0 bad | **clean** — both flags are positive controls; §3 confirmed against 67 files |

**`chse` and `lmap` are not cleared by this pass and I am saying so rather than counting them.** Two
citations apiece is below what either instrument can speak to, and the three sheets that landed today
may fall under `repos-1e`'s *as-it-lands* remit — flagged rather than collided with.

## 16. `st2e` row layouts — COLLISION, and the handover. 2026-09-06

**I took this row believing it orphaned and I was wrong.** Row 2's status cell was blank when I read
it and `repos-4b` had explicitly stopped the same decode, so "unclaimed" was a reasonable reading of
the board — but `repos-3f` edited their cell to *"NOW WORKING MY ACTUAL ROW: the four `st2e` row
layouts"* in the interval, with progress already banked. **`repos-c7` caught it and told me.**

**I have deleted the sheet I wrote** (`St2e-Carriers/st2e-row-layouts-and-the-area-join.md`, no
inbound links, `check_links` clean after removal) rather than leave a second row-layout document in
the folder that already produced one duplicate-sheet collision this round. **`repos-3f` owns the row.
Everything below is theirs to use or discard.**

### What `repos-3f` already has, and it is stronger than mine

`slot 2 +0x00` is a **bounds-checked index into slot 0**, named from a reader —
`BattleUnit_ApplyUnitDefinition` `0x0023A570`, the `u16` load at `0x0023A6B4`, bounded against slot
0's count at `0x0023A6B9`. **That is tier 1 and my corpus result is tier 4.** Where we overlap they
win, and my numbers corroborate rather than compete: I measure the same column at **138/138 areas
with `max == count-1`, mean unused headroom 0.00, and every slot-0 row referenced in every area** —
independently, from the files, with no knowledge of the reader.

### What is additive — two more index columns nobody has

Same instrument, same 166 areas, 3,838 rows:

| column | indexes | areas populated | `max == count-1` | mean slack | out of range |
|---|---|---:|---:|---:|---:|
| `+0x00` | slot 0 | 138 | 138 / 138 | 0.00 | 0 | *(theirs, from the reader)* |
| **`+0x22`** | **slot 5** | 140 | **140 / 140** | **0.00** | **0** |
| **`+0x24`** | **slot 6** | 120 | **120 / 120** | **0.00** | **0** |

**Every target row is referenced in every area, for all three — zero unreferenced rows anywhere.**
Multiplicity differs and is the informative part:

| column | injective areas | duplicates | slot-2 rows vs target |
|---|---:|---:|---|
| `+0x00` → slot 0 | 81 | 57 | equal 81, more 57, **fewer 0** |
| `+0x22` → slot 5 | **137** | 3 | equal 137, more 3, **fewer 0** |
| `+0x24` → slot 6 | 22 | 98 | equal 22, more 98, **fewer 0** |

**Slot 2 never has fewer rows than any table it points at, in any relation, in any area** — it is the
spine and slots 0/5/6 are satellites. `+0x22` → slot 5 is a **bijection in 137 of 140 areas**.

> **This explains `repos-4b`'s `.nmb` result.** They found `.nmb`'s entry count matches **slot 2**
> 166/166 and falsified it against 0/5/6. Slot 2 being the spine is *why*: it is the table with one
> row per thing. Two unrelated instruments — their count join, my index tracking — land on the same
> table.

### The noise floor, measured before believing any of it

*"In range in all 166 areas"* is not evidence. A column whose maximum is 2 is in range for any table
with three rows. I ran the weak test over **every column against every target**: it passes 1–5
columns per pair. Then the tracking test separates them, and `+0x24` is the clean demonstration —
**in range for all four tables, and tight only against slot 6** (120/120 vs 22/120, slack 0.00 vs
2.5–3.7). An in-range hit that does not track is a coincidence with 120 chances to be one.

Two candidates that survived the weak test and **failed** tracking, so there is **no self-index**:
`+0x12` (1/35 tight, slack 7.40) and `+0x1A` (1/4, slack 3.75).

### Also measured, and free to take

Dead-byte topology over all 3,838 rows — the strongest thing a corpus can say about a record:

| slot | record | bytes zero in **every** row | live |
|---:|---:|---:|---:|
| 0 | 84 | **43** | 41 |
| 2 | 88 | **27** | 61 |
| 5 | 56 | **32** | 24 |
| 6 | 56 | **40** | 16 |

**Slots 5 and 6 share a record size and a similar dead-byte topology** — both 56 bytes, both with a
long zero run ending at `+0x1F`. Suggestive of one layout used twice.

> **CORRECTED 2026-09-06, and settled by `repos-c7`.** The sentence above first read *"all live bytes
> in the tail from `+0x20`"*. **That is wrong for slot 5**, whose `+0x00`–`+0x03` are live; only slot
> 6's zero run starts as early as `+0x02`. The correct statement is that **slot 6 is zero from `+0x02`
> to `+0x1F` and slot 5 from `+0x04` to `+0x1F`** — I compressed two different runs into one phrase.
> `repos-c7` caught it by noticing that a consumer reads `+0x02`/`+0x03` from both tables, which my
> wording said could not happen.
>
> **And it is no longer a lead.** `repos-c7` reads `0x002FEF30` and finds *one function reading both
> tables through identical displacements* — the same offset list, in the same instruction pairs, one
> multiplied and one added. **One layout used twice, decided by a reader**, which is the bar my
> corpus reading could not reach.

### The reconciliation, and it answers a question neither of us could answer alone

`repos-c7` reports a conditional stat pair: `+0x02`/`+0x03` of both tables, gated by **bit 1 of
`spine[+0x15]`**, in `growth[off] * K + base[off] + rec[field]`. My census said those bytes were
dead. **Both were right about different tables**, measured over all 166 areas:

| | slot 5 (the additive base) | slot 6 (the growth coefficient) |
|---|---|---|
| `+0x02` non-zero | **84 of 1,119 rows** (5 distinct, max 25) | **0 of 619** |
| `+0x03` non-zero | **84 of 1,119 rows** (3 distinct, max 10) | **0 of 619** |

**So the gated pair is real, and its growth term is dead in every shipped area.** When bit 1 enables
it, the stat evaluates to `0 * K + base + rec` — **a flat authored value with no level scaling**,
because the coefficient it would be multiplied by is zero in all 619 growth rows. That is a fact a
modder can act on and neither a corpus pass nor a consumer read could have produced by itself.

**The flag tracks the data strongly but is not a bijection:**

| `spine[+0x15]` bit 1 | slot-5 row has a live `+0x02`/`+0x03` | spine rows |
|---|---|---:|
| set | **yes** | **83** |
| set | no | 43 |
| clear | yes | **2** |
| clear | no | 1,018 |

**Bit 1 clear predicts a dead pair in 1,018 of 1,020 rows (99.8 %); bit 1 set predicts a live one in
83 of 126 (66 %).** The two exceptions are explained by slot 5 being shared — one slot-5 row is
reachable from both a flagged and an unflagged spine row, so a live row can sit under a clear flag
without contradiction. **The 43 flagged-but-dead rows are not explained** and are the open end of
this: either the flag enables a pair the area chose not to author, or bit 1 carries a second meaning.

`spine[+0x15]` overall: bit 0 set in **1,120 of 1,146** rows, bit 1 in **126**. Values observed:
`0`×24, `1`×701, `3`×92, `5`×5, `9`×4, `13`×12, `16`×2, `17`×263, `19`×34, `21`×9.

Full per-byte census (distinct counts and ranges for every offset of all four records):
`Tools/work/repos-c9/st2e_census.txt` and `fences.txt`. Scripts: `st2e_rows.py`, `st2e_ids.py`,
`st2e_join.py`, `st2e_dense.py`.

### Carried, not verified by me

`repos-c7` reports — and `repos-1e` found independently — that **the board's own "already
established" block is wrong**: `0x002FEF30` reads **seven** registry slots, not four, and only the
*first* lookup is indexed by the record byte. **I have not re-derived that** and am recording it as
their finding, not mine.

## 17. The spine flag byte `+0x15` — bit 2's consumer found, bit 4's not

`repos-c7` established that `0x002FEF30` loads `[spine+0x15]` **once**, tests bits 0 and 1, and drops
the register 92 bytes later — so my `17`/`19`/`21` value cluster (bit 4 set) is consumed somewhere
else, and their function cannot explain it. They asked for that to be narrowed rather than answered.
**Here is the narrowing, and one bit is now attributed.**

### The corpus first — what each bit is worth

`spine[+0x15]` over all **1,146** slot-2 rows. Observed values: `0`×24, `1`×701, `3`×92, `5`×5,
`9`×4, `13`×12, `16`×2, `17`×263, `19`×34, `21`×9.

| bit | rows set | share |
|---:|---:|---:|
| 0 | 1,120 | 97.7 % |
| 1 | 126 | 11.0 % |
| **2** | **26** | 2.3 % |
| 3 | 16 | 1.4 % |
| **4** | **308** | **26.9 %** |
| 5, 6, 7 | **0** | — |

**The top three bits are never set in any shipped row** — the byte carries five bits, not eight.
Bit 4 is the second-commonest and had no known consumer, which is why it was worth chasing.

### Bit 2 is read by `BattleUnit_ApplyUnitDefinition`

```
0023AA0F  test   byte ptr [rsi + 0x15], 4        ; bit 2
0023AA13  jne    0x0023AA2F                      ; set -> skip the clear
0023AA1D  movabs rax, 0xFFFFF7FFFFFFFFFF         ; ~(1 << 43)
0023AA27  and    qword ptr [rdi], rax            ; clear bit 43 of the unit record
0023AA2A  jmp    0x0023ABCA
```

**Bit 2 CLEAR clears bit 43 of the qword at `[rdi]`; bit 2 SET leaves it alone.** The polarity is the
same shape `repos-c7` found for bits 0 and 1 — the flag *suppresses a default*, it does not enable a
feature. It is set in only **26 of 1,146** rows, so the default path is overwhelmingly the common one.

### Bit 4 — not tested by anything that reads the spine, and the global search is NOT decisive

Scoped to the four functions the registry document names as readers of slot `0x02EBF120`, the search
is **complete**: every memory access whose extent covers byte `+0x15` — including wider loads at
`+0x10`, `+0x12` and `+0x14` that would carry the byte along with it — is **11 accesses**, and only
two are byte-wide reads of `+0x15` itself:

| function | accesses covering `+0x15` | byte-wide tests of it |
|---|---:|---|
| `BattleUnit_ApplyUnitDefinition` `0023A570` | 3 | `0023AA0F`, bit 2 |
| `BattleStats_InitializeDefinitionRecord` `0023AC80` | 2 | none |
| `BattleEncodedId_IsValidForClass` `00322C50` | **0** | none |
| `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` | 6 | `002FF325`, bits 0 and 1 |

**No test of bit 4 in any of them.**

> **And I am not turning that into "bit 4 is tested nowhere".** A global scan of `.text` finds the
> only bit-tests against a `[reg+0x15]` byte operand are for bit 1 and bit 2 — but **a byte can be
> reached by a wider load**, and there are **~19,000 memory accesses at `+0x10`/`+0x12`/`+0x14` whose
> extent covers `+0x15`.** That is not a search, it is a population. **The negative is only valid
> inside the four-function scope where I could enumerate every access**, and outside it the method
> genuinely cannot see. Three of the eleven in-scope accesses *are* wider loads at `+0x14`
> (`0023AEEE`, `002FF2E0`, `002FF0CD`) and they are on `rbp`/`rdi`, which I have not shown to be the
> spine row — `rdi` in `0x002FEF30` is the 456-byte definition record, a different structure.

**So bit 4's consumer is outside the known reader set**, and finding it needs the spine pointer
traced to further callers rather than another scan of the same four functions.

### And the 43 flagged-but-dead rows are narrowed, not closed

`repos-c7` enumerated bit 1's effects and showed the flag is dead 92 bytes after it loads, with both
effects accounted for: **bit set → the growth pair applies and the equipment branch for that stat is
switched off; bit clear → no growth pair, equipment contributes instead.** *Either/or, not
suppression* — which the existing sheet had as "also suppresses".

That leaves my 43 rows as: **bit 1 set, so equipment is switched off for that stat, and the pair that
should replace it has a zero base.** Those rows take **neither source**. Either an area authored a
pair it did not fill, or bit 1 has a second meaning in a consumer that is not `0x002FEF30`. **It is a
narrowing and I am publishing it as one.**

## OPEN-QUESTIONS

- **`BZ-1` — CLOSE.** Resolved above; `Sections/section-006.md` §3 carries it.
- **`BZ-2` — CLOSE.** Resolved above; `Sections/section-019.md` §2 and §3 carry it.
- **`PROPOSED-c9-6`** — `FUN_0037aa90`'s `slot == 0` branch sets `|= 0x20` on every light record,
  but the dispatcher **skips slot 14 entirely for manager 0** (`0x0033066B TEST EBX,EBX ; JE`). On
  the `EBP2` route that branch never runs. It is reachable only if `FUN_003775D0` (site
  `0x003776A6`) passes 0, and that caller is unread. **Not claimed dead** — shown unreachable by the
  one route established.
- **`PROPOSED-c9-7`** — does anything write `0x01F83530` at runtime? It is zero at image load
  (past `.data`'s raw backing), which makes `FUN_0020E600` an identity function and `section_019`'s
  slot-7 resolution a no-op offset. A runtime write would change the resolved address for every
  `.ard`-family read. Static analysis has not found a writer; this is a **tier-10 question**.
- **`PROPOSED-c9-8`** — `section_017` has a live handler (`FUN_00332110` → `FUN_003DFE60(1, ptr)`)
  and **0 users in 1,115 `us` files**, independently confirmed here. `ebp_explained`'s denominator is
  13 censused section types; slot 17 is a **14th dispatchable slot with no shipped data**. Not a
  defect in the denominator — the census measures files and the dispatcher measures code — but the
  two populations differ by one and that should be stated where the denominator is defined, not left
  to be rediscovered.

## MANIFEST-ROWS

None. Every function I read this round already carries a `CodeDomain`, and nothing I found
contradicts one. `FUN_0037AA90`'s `Actor.ResourceAuxiliaryTable` is confirmed by the dispatcher
route rather than challenged by it.

## AUDIT-LOG

**2026-09-04 — `repos-c9`, independent falsification passes, program state GN160
`fa0db293…d2f708` (unchanged).**

- `Container/ebp2-container.md` — **audited, CONFIRMED.** Corpus re-derived from 1,115 raw files with
  an independent parser; binary re-derived with capstone rather than Ghidra. Read set, zero `[rdi]`
  references, `bound == slotIndex` at all 15 sites, and all 14 handler targets confirmed. One false
  discrepancy raised by my own linear-sweep method and withdrawn; the document was right.
- `Sections/section-016.md` — **audited, CONFIRMED** on all corpus invariants and on `g_fieldRoots`.
  One immaterial count difference (2,017 vs 2,018 whole-degree `dir` values, shown not to be a
  tolerance artifact) reported to the author, sheet not edited.
- `Sections/section-004.md`, `-006.md`, `-014.md`, `-019.md` — **REOPENED and re-closed**,
  `reopened_count: 1`, `audit.passes: 2`, `last_pass_state:
  GN160-repos-c9-falsification-2-after-reopen`. `004`/`006`/`019` `PARTIAL` → `DOCUMENTED` on real
  tier-1 contracts. Correction trails kept in each; nothing silently rewritten.
- **Structural:** no shared `_index/*.md` edited. The only edits outside my own four sheets are my
  own `status` cell in `ASSIGNMENTS.md` §1 row 6 and this file.

**Not audited, and named so the gap is visible:** `section-000-bytecode.md`, `-002-text.md`,
`-003-text.md`, `-008.md`, `-009.md`, `-010.md`, `-011.md`, `-012.md`. Eight of the ten sheets I did
not write are still unattacked, and `008`/`009` still carry `audit.passes: 0`. That is the remaining
audit debt on this row.

## CALL-CHAINS / ADDRESS-INDEX

```
ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources  0x003304A0
  slot 4  0x0033064B -> FUN_00332100 0x00332100 -> FUN_003DFDC0 0x003DFDC0 -> g_fieldRoots[2] 0x02B59D58
  slot 6  0x00330565 -> FUN_00330060 0x00330060 -> 0x022C6CF0[mgr]
                                                -> FUN_0026C860
                                                -> FUN_0029CAC0 0x0029CAC0 (cache 0x0209C320)
                                                -> FUN_0039BEC0 0x0039BEC0 (registry 0x02AEE810)
  slot 14 0x0033068A -> FUN_00330110 0x00330110 -> 0x022C6E20[mgr], mask 0x022C6E48[mgr] bit 16
  slot 19 0x00330666 -> FUN_003320D0 0x003320D0 -> FUN_003EAA00 0x003EAA00 -> latch 0x02B5E0C8
                                                                          -> FUN_0020E600 0x0020E600
                                                                          -> FUN_003DCF10
  tail    0x003306BF -> ActorResource_FinalizeManagerRuntimeAfterLoads 0x0032F1B0
                          0x0032F1C9 LEA RDI,[0x022C6E20]
                          0x0032F1F9 -> FUN_0037AA90 0x0037AA90   (validates 'LGT2')
```

New addresses this round: `0x00332100`, `0x003DFDC0`, `0x00330060`, `0x0029CAC0`, `0x0209C320`,
`0x003320D0`, `0x003EAA00`, `0x02B5E0C8`, `0x0020E600`, `0x01F83530`, `0x02B59D58` (`g_fieldRoots[2]`),
`0x003DFA50`.
