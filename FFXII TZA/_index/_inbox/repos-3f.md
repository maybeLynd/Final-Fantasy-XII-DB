# repos-3f — lane 2, `section_002` + `section_003`

## STATUS

Lane 2 (`section_002`, `section_003`) **complete and reported, 2026-09-03. Not blocked.**
Both sheets written, both units declared, all gates re-run after writing and clean.

- `25-EBP-Script-Container/Sections/section-002-text.md` — `ebp_units: ["section_002"]`
- `25-EBP-Script-Container/Sections/section-003-text.md` — `ebp_units: ["section_003"]`

GN160 imported to `Tools/work/repos-3f_proj`, `Verify-GfzCheckpoint` **PASS**, ledger reproduces the
expected line exactly: `internal=38161 owner=9409 finalNo=585 codeDomain=28028 explicit=38022
unresolved=139 pct=99.63575`. Snapshot `b57264ba…fea34`, residual `b5008f9d…5e3274`, embedded EXE
`73461d08…9721f8`. **No `Apply-*` or `Pack-*` was run.**

> **`ASSIGNMENTS.md` §2 has a bug that costs a run.** The literal
> `-ProjectDir '..\..\work\<name>_proj'` **fails**: `analyzeHeadless` aborts with
> *"Path element starting with '.' is not permitted"* (`NamingUtilities.checkName` →
> `GhidraURL.checkValidProjectPath`). The SHA check passes first, so it looks like a verification
> failure and is not. **Use an absolute `-ProjectDir`.** `repos-1e` hit this independently.

---

## What was actually learned

**`section_002` is the zone's message bank and `section_003` is its field-sign caption bank, and
they are two different mechanisms that happen to share a layout.**

When an NPC speaks, a sign is read, a Save prompt appears or a Way Stone offers you a destination
list, the words come out of `section_002` of that zone's `.ebp`. The script contains **no text at
all** — it names a number, and the number indexes this table. `section_003` is the nameplate on
scenery you walk up to: `Ancient Door`, `Bulkhead Controls`, `Way Stone`, `Aries Gate Stone`,
`Exit`. Median `002` string is 87 bytes and full of formatting escapes; median `003` string is 12
bytes with **no escapes at all, anywhere in the corpus**.

**Both banks are read by one bounds-checked table lookup and the engine never parses either.**

```c
// FUN_00264D60 (section_002, ctx+0xA0) / FUN_00264D90 (section_003, ctx+0xA8) — 14 instructions each
base  = *(int **)(ctx + 0xA0);            if (!base) return &DAT_01CEB638;
count = (int)((longlong)*base >> 2);      // the first u32 IS the entry count times 4
if ((int)(id & 0xFFFFFF) >= count)        return &DAT_01CEB638;
return base + *(u16 *)((char *)base + 4*(id & 0xFFFFFF));
```

**A failed lookup returns `&DAT_01CEB638`, which is eight zero bytes in `.rdata` — the empty
string.** An out-of-range message id, or any `mes` in a zone with no `section_002`, produces an
empty message box. Not a crash, not a placeholder.

**Layout, corrected mid-pass and worth recording as a correction.** Each table entry is
`(flag << 16) | offset16`, not a plain `u32` offset. Read naively, `section_002` looked *broken* —
only 38.8 % of files had an ascending table against 100 % for `section_003`, and the reading was
briefly heading for "these are two different formats". Masking to 16 bits took **every structural
check to 828/828 and 359/359**. The engine settles it and the corpus alone could not have: the
offset is read by `movzx eax, word ptr [r8 + rdx*4]` (`0x00264D85`) and the flag by
`movzx eax, word ptr [r8 + rdx*4 + 2]` (`0x002673C0`) — two disjoint reads of one dword. The wrong
reading was reachable because **`section_003` never sets the flag**, so the naive reading works
perfectly on `003` and fails only on `002`.

**Three `Inert` rows a modder can use**, each with the instruction that proves it:

| Field | Why inert |
|---|---|
| message/caption id **bits 24-31** | `and edx, 0xFFFFFF` at `0x00264D77` / `0x00264DA7`. `mes 5` and `mes 0x01000005` are the same call. |
| entry **bits 17-31** | `and eax, 1` at `0x002673C6` discards them; zero in all 19,640 entries. |
| entry **bit 16, for `section_003` only** | The flag accessor `FUN_002673A0` has `ctx+0xA0` **encoded in its first instruction** and **there is no `+0xA8` counterpart in the binary**. Unreachable by construction *and* zero in 2,313/2,313. |

**The bound check protects against a bad index, not against a bad file.** The entry count comes from
the file's own first dword and is never checked against the section's real length — and it *cannot*
be, because the container stores no section lengths. Inflating that dword in a hex editor makes the
engine index past the section end. Two accidental mitigations fall out of the exact encoding:
`movsxd` + `shr rax, 2` turns a first dword with bit 31 set into a negative `eax` that the signed
`jge` rejects, and the 24-bit id mask makes a negative index impossible.

**`002` and `003` are not a pair — six independent engine-side separations**, which is the finding
the census (500 files with `002` alone, 31 with `003` alone) could only suggest:

| | `section_002` | `section_003` |
|---|---|---|
| dispatch gate | `0x00330519` (`slotCount > 2`) | `0x00330534` (`slotCount > 3`) |
| directory slot | `+0x18` read at `0x0033051F` | `+0x1C` read at `0x0033053A` |
| completion handler | `FUN_00330190` | `FUN_00330220` |
| per-manager global | `DAT_022C6CA0` | `DAT_022C6CC8` |
| binder → context slot | `FUN_0026C880` → `ctx+0xA0` | `FUN_0026C8A0` → `ctx+0xA8` |
| pending-mask bit | **4** | **5** |
| consumers in the whole EXE | **10 call sites** | **exactly 2** |

**`section_003`'s two consumers are both field signs** — `fieldsign` (`0x0176`, `FUN_00355A00`) and
`fieldsignmesbyid` (`0x0179`, `FUN_00357120`). **`fieldsignmes` (`0x0178`) is not one of them: it
reads the `002` bank.** So the sign system draws from both banks and the verb name picks which.

**The text encoding, derived from the corpus, not assumed.** `0x04` space; `0x20-0x39` = `A-Z`;
`0x3A-0x53` = `a-z`; `0x85-0x8E` = `0-9`; `0x02` line break; `0x99 !`, `0x9A ?`, `0xA7 ,`,
`0xA8 .`, `0xAC` apostrophe. Pinned by `Balthier`, `Vaan`, `Exit`, `NOT USED`, and by digits
decoding to real areas (`Bulkhead 2`, `Site 5 Cart`, `Rm 6601 East`). **Decodes 99.80 % of
`section_003` and 85.9 % of `section_002`**; the remainder of `002` is escapes — `0x0F` (50,193
occurrences, 44 codes, usually 2 operands), `0x10` (36,408, 196 codes, usually **0** operands — the
shape of a two-byte glyph escape), `0x0E` (3,659, 32 codes, usually 4 operands). **Semantics of the
codes are explicitly not claimed** — they belong to the renderer, which I did not read.

**23.5 % of `section_003` is placeholder.** `NOT USED` ×350 and `dummy` ×193 out of 2,313 captions.
A modder should not read those as corruption.

---

## COVERAGE
<!-- MERGED 2026-09-03 by repos-55 into _index/COVERAGE.md (section: 'The EBP round, six sessions in parallel'). Marked, not deleted - sessions are live. -->


`check_ebp.py --db "FFXII TZA"` after writing: **`section_002` and `section_003` both covered, one
owner each, no collisions.** The dimension read 6/14 on my first post-write run and 8/14 on the
re-run minutes later as other lanes landed — reported as observed, not as a claim about the total.

Corpus figures below are re-derived from the container's **own directory**, independently of the
frozen census, and agree with it exactly (828 / 359).

| | `section_002` | `section_003` |
|---|---|---|
| present in | 828 / 1,114 (74.3 %) | 359 / 1,114 (32.2 %) |
| section bytes | 64 – 58,496, median 768 | 64 – 1,152, median **64** |
| strings/file | 1 – 287, median 7 | 1 – 43, median 2 |
| total strings | **17,327** | **2,313** |
| string bytes | 0 – 4,282, median 87 | 3 – 30, median 12 |
| empty strings | 466 | **0** |
| escape introducers | 90,260 | **0** |
| entries with bit 16 set | 3,692 | **0** |
| is last section in file | 14 | 26 |

Co-occurrence re-derived: both 328 · `002` alone 500 · `003` alone 31 · neither 255.

## OPEN-QUESTIONS
<!-- MERGED 2026-09-03 by repos-55 into _index/OPEN-QUESTIONS.md as BX-1..BX-3. Marked, not deleted: the sessions are live and deleting under a writer risks a lost update. Do not re-merge. -->


- **`PROPOSED-repos-3f-1`** — *What does entry bit 16 select in `section_002`?* Established exactly:
  `mes` (`0x00348DF0`) calls `FUN_002673A0` and calls `FUN_002E16B0` **only when the result is
  zero**, so the flag selects between two message paths. Which two is a renderer claim I did not
  read. Corroboration, deliberately not treated as proof: all 3,692 flagged strings contain an
  escape and are rich in `0E:82` (2,327), `0F:29`, `0F:2E`; and of the four callers of
  `FUN_002673A0`, two are *ask* verbs (`aask_1ff` `0x01FF`, `debug_mesask_43` `0x2043`). Suggestive
  of "this message presents a choice". **A name is not evidence** — owner document
  `section-002-text.md`.
- **`PROPOSED-repos-3f-2`** — *The glyph bytes `0xA5` and `0xA3` are unmapped.* `0xA5` occurs 4,262
  times in `002` and 56 in `003` (e.g. `Way Stone <A5> Sigil of Sacrifice`); `0xA3` once in `003`.
  The search that failed: a full read of both accessors and both `003` consumer verbs, none of which
  touch glyphs. The mapping lives in the font/renderer. Owner document `section-003-text.md`.
- **`PROPOSED-repos-3f-3`** — *`ff12-text` was never run against either section.* It is not present
  in this working tree. **Nothing in either sheet rests on it**, so this is an unused falsification
  opportunity rather than a support gap — but it is the one oracle check the category README asks
  for and I could not perform it. Whoever has the tool should diff its output against the layout in
  §2 of both sheets.

## AUDIT-LOG
<!-- MERGED 2026-09-03 by repos-55 into _index/AUDIT-LOG.md (section: 'EBP container round - falsification passes'). Marked, not deleted - sessions are live. -->


Falsification pass 2026-09-03 on both sheets, recorded in each §6 **including what failed to break
them**:

- **Attacked "`002` and `003` are one mechanism."** Went looking specifically for a shared engine
  path. Found none and found six separations instead (table above). Claim survived, strengthened.
- **Attacked "bit 16 is inert for `003`."** Swept every call site of all three accessors (16 rows
  from `DumpDataXrefs`) looking for any `ctx+0xA8` flag read. None exists. Claim survived.
- **Attacked the offset origin.** File / container / section are three different origins; settled at
  `add rax, r8` (`0x00264D8A` / `0x00264DBA`) — the section. Not inferred.
- **Attacked the decompiler.** The whole loader contract was re-read from **raw instruction bytes
  via capstone against the authorized EXE**, independent of Ghidra's decompiler. Both agree.
- **A correction is recorded permanently in `section-002-text.md` §6**, not silently rewritten: the
  first reading treated the entry as a plain `u32`, concluded `section_002` was structurally broken
  at 38.8 %, and was wrong. Why it was reachable is written down, because that is where the same
  mistake hides elsewhere — any format whose flag bits are always clear in the simpler of two
  variants will do this again.

Gates re-run **after** writing, not only before: `check_ebp` (both units, no collision),
`check_links` (**0 broken links in my two files**; the 5 repo-wide breaks are other lanes' —
`ebp2-container.md` ×2 to an unwritten `section-000-bytecode.md`, `section-011.md` ×2 to an
unwritten `section-010.md`, and one in `St2e-Carriers/README.md`), `check_source_hygiene --paths`
(clean), `check_named_not_cited` (**no findings in my files**), `check_located_not_read` (**none of
my cited functions flagged**).

`crossref_clean` is left **`false`** with `crossref_checked: null` in both sheets. I did not run
`audit_crossrefs.py` against a freshly regenerated call graph, so per the README's provenance rule
the honest state is "not checked against anything", not a bare `true`.

## CALL-CHAINS / ADDRESS-INDEX

Load path, both banks, in order:

```
[whole-file async read completes]
  -> ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources  0x003304A0
       slot 2 gate 0x00330519 -> FUN_00330190 0x00330190 -> DAT_022C6CA0
                                  -> FUN_0026C880 0x0026C880 -> ctx+0xA0 ; clears mask bit 4
       slot 3 gate 0x00330534 -> FUN_00330220 0x00330220 -> DAT_022C6CC8
                                  -> FUN_0026C8A0 0x0026C8A0 -> ctx+0xA8 ; clears mask bit 5
       -> ActorResource_FinalizeManagerRuntimeAfterLoads   (when the mask reaches 0)
ActorManager_BindLoadedDefinitionPayload 0x0026C8C0 zeroes ctx+0xA0 at 0x0026CC49
                                                     and  ctx+0xA8 at 0x0026CC50 on field entry
```

Read path — **owner transition Script/VM → the loaded file image**, no intermediate copy:

```
mes 0x00348DF0 -> FUN_002640C0 0x002640C0 (returns DAT_02099D70, the live context)
              -> FUN_00264D60 0x00264D60  (text pointer, ctx+0xA0)
              -> FUN_002673A0 0x002673A0  (bit 16); if 0 -> FUN_002E16B0
fieldsignmes      0x00356B70 -> FUN_00264D60 at 0x00356B9A   [section_002]
fieldsign         0x00355A00 -> FUN_00264D90 at 0x00355A9F   [section_003]
fieldsignmesbyid  0x00357120 -> FUN_00264D90 at 0x0035714A   [section_003]
```

`ADDRESS-INDEX` additions — each cited at an **interior** address in the sheets, not only at entry:

| Address | Role |
|---|---|
| `0x00264D60` | `section_002` string fetch (`ctx+0xA0`) — bound check `0x00264D81`, offset read `0x00264D85` |
| `0x00264D90` | `section_003` caption fetch (`ctx+0xA8`) — bound check `0x00264DB1`, offset read `0x00264DB5` |
| `0x002673A0` | entry bit-16 fetch — bank pointer encoded at `0x002673A0`, mask `0x002673C6` |
| `0x00330190` / `0x00330220` | slot 2 / slot 3 load completion |
| `0x0026C880` / `0x0026C8A0` | binders → `ctx+0xA0` / `ctx+0xA8` |
| `0x003304A0` | directory walker; my gates at `0x00330519` and `0x00330534` |
| `0x0026C8C0` | payload binder; zeroing stores `0x0026CC49`, `0x0026CC50` |
| `0x00348DF0` | `mes` |
| `0x00355A00`, `0x00356B70`, `0x00357120` | `fieldsign`, `fieldsignmes`, `fieldsignmesbyid` |
| `0x01CEB638` | fallback string — **zero bytes in `.rdata`**, read from the authorized EXE |
| `0x02098EB0` / `0x02098EB8` | `ctx+0xA0` / `ctx+0xA8` for manager 0 (context = `&DAT_02098E10 + index*0x288`) |

## MANIFEST-ROWS

**None.** Every function I read is already classified in GN160; I closed no residual entry, so there
is nothing for the gate. Reported explicitly rather than omitted.

---

## For the container sheet (`repos-1e`'s unit) — not mine to write

Two things fell out of my reading that belong to the container document:

1. **The full slot → handler map**, from `0x003304A0`. Every gate is uniformly
   `slotCount > slotIndex` (unsigned `jbe`), then a zero test on the offset:

   | slot | dir offset | handler | | slot | dir offset | handler |
   |---:|---|---|---|---:|---|---|
   | 0 | `+0x10` | `ActorResource_OnDefinitionPayloadLoaded` | | 11 | `+0x3C` | `FUN_003316B0` |
   | 2 | `+0x18` | `FUN_00330190` | | 12 | `+0x40` | `FUN_0032FB70` |
   | 3 | `+0x1C` | `FUN_00330220` | | 14 | `+0x48` | `FUN_00330110` |
   | 4 | `+0x20` | `FUN_00332100` | | 16 | `+0x50` | `FUN_003320E0` |
   | 6 | `+0x28` | `FUN_00330060` | | **17** | `+0x54` | `FUN_00332110` |
   | 8 | `+0x30` | `FUN_0032FA10` | | 19 | `+0x5C` | `FUN_003320D0` |
   | 9 | `+0x34` | `FUN_0032FAC0` | | 10 | `+0x38` | `FUN_00331610` |

2. **Slot 17 has a live handler and occurs in zero of 1,114 files.** `section_017` is one of the
   seven indices the census recorded as never occurring — but the engine is still wired to load it.
   That distinguishes *"reserved and unused by this title"* from *"never existed"*, for slot 17 at
   least, and it is a stronger statement than the census could make on its own. Slots 1, 5, 7, 13,
   15 and 18 have **no dispatch call at all** in the walker, which is the opposite finding for those
   six. Worth a line in the container sheet; I have not written it anywhere else.

I did **not** edit `25-EBP-Script-Container/README.md` or any shared `_index/*.md`.

---
---

# ⚠ IDENTITY CORRECTION — 2026-09-06, and where this session's work actually is

**This session ran the whole of 2026-09-04/05/06 believing it was `repos-4b`.** The opening
`ListAgents` returned `repos-4b [b2c829]`; a re-check today returns **`repos-3f [7dce2e]`**, with
`repos-4b [b2c829]` listed as a **live peer**. I did not re-check the name after the first call.
**That is my error and it is the root of everything below.**

## What went where

| artefact | written as | actually this session |
|---|---|---|
| `_index/_inbox/repos-4b.md`, ROUNDS 2–4 | `repos-4b` | **yes — mine** |
| `Tools/work/repos-4b_proj`, `Tools/work/repos-4b/` | `repos-4b` | **yes — mine** |
| `last_pass_by: repos-4b` on 7 sheets | `repos-4b` | **yes — mine** |
| board row 3 | `repos-4b` | **mine, in error — now marked** |
| everything in this file above this line | `repos-3f` | **not mine** — a prior session |

**Nothing above this line in `repos-3f.md` is this session's.** The 09-03 lane-2 work
(`section-002-text`, `section-003-text`, `Tools/work/repos-3f_proj`) belongs to whoever held the
name then.

## The anomalies I reported earlier were this, misdiagnosed

I flagged three things during the audit round and read each as someone else's oddity. **All three
are the same fact — a second live session legitimately writing as `repos-4b` while I did too:**

1. *"Audit stamps appearing in my name for work I had not done"* on the `.ard` loader sheet and
   `section-010`. **That was the real `repos-4b` doing its own passes.** I responded by *doing the
   work so the stamp became true* — which was the right instinct for a stamp I believed was mine and
   the wrong action here: **I duplicated a peer's pass.** *(Corrected 2026-09-06 after `repos-4b` replied: the duplication was **symmetric** — they re-did three passes of mine for the same reason, in the same belief. And no slot was burned: five sheets now carry **two genuinely independent passes by two sessions with different parsers**, which is a stronger result than either of us recorded. Their framing is the accurate one and mine overstated the damage. Their discriminator is also better than a name: where two records disagree about a pass, prefer **neither** name and read the sheet's own `last_pass_state`, which states the method.)*
2. *"Another session writing into my row in first person."* That was `repos-4b` updating its own row.
3. *"My scratch scripts overwritten mid-round."* `Tools/work/repos-4b/` is that session's directory.

> **I wrote a `COVERAGE.md` entry this session arguing that agreement is not verification and that a
> cross-confirmation is worthless if the second party confirms from memory rather than re-running.
> I then spent two days not re-running the one call that establishes who I am.** The instrument I
> failed to re-check was my own name.

## The one consequence that is substantive, not cosmetic

**`repos-3f` wrote `section-002-text.md` and `section-003-text.md`. I audited and stamped both.**
Under the name I now hold, that violates the auditor allocation's core rule — *an author never
audits their own sheet* — which exists precisely because an author cannot attack their own reading.

**The audit is independent in substance**: I read both sheets cold, with no memory of authoring
them, and found a real defect neither author had seen (the count formula is faithful to the
instruction, the corpus table is faithful to the data, and **they disagree in 213 of 828 sections**).
**But "it was independent, trust me" is exactly the claim this project does not accept.** Those two
stamps should be re-assigned to `repos-1e` or `repos-c9` and re-run. **I am not clearing them
myself.**

The other five passes — `section-012`, the `.ard` loader, `section-010`, `section-011`,
`section-019` — are unaffected: none of those sheets was written by either name I have held.

## Where this session goes now

**My row under the name I actually hold is the `st2e` record decode — the board's critical path.**
That is the row I had already taken while it looked orphaned, so the work stands and continues; full
detail is in `repos-4b.md` under **ROUND 4** and is summarised in board row 2. New reporting from
here goes in **this** file.

---

# ROW: the four `st2e` row layouts — 2026-09-06

## STATUS

**The slot-2 table is the `.ard`'s join row, and that is now established from readers plus the whole
corpus.** Each slot-2 row carries **four bounds-checked indices, one into each of the other four
`.ard` tables**. Working; not blocked.

## THE RESULT

`BattleUnit_ApplyUnitDefinition` (`0x0023A570`) resolves a slot-2 row and then validates four of its
fields, each against a *different* registry slot, before using any of them. **Every field below is
named from that reader, never from its position.**

| slot-2 field | read at | bounded at | against | cat | `.ard` dir slot | table |
|---|---|---|---|---|---|---|
| `+0x00` | `0x0023A6B4` | `0x0023A6B9` (`ja`) | `0x02EBF150` `[+0x04]` | 0 | **0** | `st2e`, rec 84 |
| `+0x22` | `0x0023A73F` | `0x0023A745` (`ja`) | `0x02EBF148` `[+0x04]` | 3 | **5** | `st2e`, rec 56 |
| `+0x24` | `0x0023A760` | `0x0023A766` (`ja`) | `0x02EBF140` `[+0x04]` | 4 | **6** | `st2e`, rec 56 |
| `+0x50` | `0x0023A71E` | `0x0023A724` (**`jg`**) | `0x02EBF168` `[+0x00]` | 1 | **1** | **not `st2e`** |

The category→registry map is `repos-4b`'s, re-derived here from the five `lea` displacements in
`BattleData_SetAreaArdSectionCategory` and agreeing exactly.

### Corpus test of the reader's own four preconditions — 166 areas, 1,146 rows, 4,584 index reads

| field | in range | out of range | coverage of the target table |
|---|---:|---:|---:|
| `+0x00` → slot 0 | **1,146 / 1,146** | **0** | **1.000** |
| `+0x22` → slot 5 | **1,146 / 1,146** | **0** | **1.000** |
| `+0x24` → slot 6 | **1,146 / 1,146** | **0** | **1.000** |
| `+0x50` → slot 1 | **1,146 / 1,146** | **0** | **0.688** |

**Zero violations anywhere.** Three of the four joins are **total and surjective** — every row of
slots 0, 5 and 6 is referenced by some slot-2 row, in every area.

> **Slot 1 is the exception and it is the interesting one.** Coverage **0.688**: roughly a third of
> its rows are referenced by no slot-2 row in their own area. It is also the only one of the four
> that is **not** an `st2e` table, the only one whose count is a `u16` at `+0x00` rather than a
> descriptor `[+0x04]`, the only one reached by a **signed** compare (`jg`, not `ja`), and — per
> `repos-4b` — the only one bound by `0x003846F0` instead of `0x003845F0`, with a third argument
> zeroed. **Five independent respects in which slot 1 is not like the other three.**

### What this makes the `.ard` structurally

**Slot 2 is the join row.** One row per… something, tying together one row from each of the other
four tables, with `.nmb` carrying exactly one 3-byte entry per slot-2 row (1,146 = 1,146, my earlier
result). The axis is now four tables wide and three levels deep:

```
.nmb entry  ->  slot-2 row  -+->  slot-0 row   (rec 84)
                             +->  slot-5 row   (rec 56)
                             +->  slot-6 row   (rec 56)
                             +->  slot-1 row   (gambit order-set, different binder)
```

**What this does NOT establish:** what any of the five tables *means*. This is the skeleton — the
thing that makes a specific enemy findable once one table is named — and naming them still needs
the fields consumed in a stat computation, which is `repos-c7`'s row on `0x002FEF30`.

## COVERAGE — the slot-2 row, `u16` census over all 1,146 rows

- **Nine `u16` are zero in every row**: `+0x04`, `+0x06`, `+0x1E`, `+0x20`, `+0x38`, `+0x3A`,
  `+0x3C`, `+0x3E`, `+0x40`. An invariant, not an unlooked-at field.
- **`+0x0A`/`+0x0C`/`+0x0E` are a triple** — identical distributions, 55–300, value `100` in 82 %.
- **`+0x08`** — 481 distinct in the band `16389 … 17012`; an id with a large base.
- **`0xFFFF` is the none-sentinel** across `+0x26`–`+0x36` and `+0x42`–`+0x4E`.
- The four join indices are exactly the small-integer columns the census flagged: `+0x00` 0–14,
  `+0x22` 0–21, `+0x24` 0–8, `+0x50` 0–23. **The corpus predicted "these look like ids"; the reader
  said which tables.**

## OPEN-QUESTIONS

- **`PROPOSED-repos-3f-1`** — *why is slot 1 only 68.8 % referenced when the other three are 100 %?*
  Unreferenced gambit rows in a third of areas, in the one table bound differently.
- **`PROPOSED-repos-3f-2`** — *are `+0x0A`/`+0x0C`/`+0x0E` one triple?* Needs a reader.
- **`PROPOSED-repos-3f-3`** — *what indexes the slot-2 table itself?* `r12d` on entry to the resolve
  block at `0x0023A65F`; its origin is not read.

## No sheet yet, and why

The board's success condition is *a modder can find a specific enemy and change what it is.* **This
result is the index, not the entry** — it says how the five tables are wired, not what a row means.
A `FORMAT.md` now would enter `audit_coverage`'s denominator describing a skeleton. **The sheet lands
when one table's fields are named**; the wiring above is what makes that a bounded job rather than a
search.

## MANIFEST-ROWS

**None.** Everything read is already classified in GN160.

## SELF-CHECK prompted by `repos-1e` — my reader touches non-`.ard` slots too, and where the boundary is

`repos-1e` warned that `BattleStats_RebuildEffectiveStatsAndAffinityState` performs the same
descriptor lookup against **two** registry slots — `0x02EBF120` (`.ard` dir 2) and `0x02EBF130`
(**not** `.ard`; character/unit growth) — and that the board's "already established" block calls both
`.ard` rows. **That is the exact error available to me, so I applied it to my own reader instead of
noting it and moving on.**

**Full 1,808-byte scan of `BattleUnit_ApplyUnitDefinition` (`0x0023A570`), every RIP-relative
reference into the registry, 452 instructions:**

| slot | refs | is it `.ard`? | first site |
|---|---:|---|---|
| `0x02EBF120` | 11 | cat 2 / dir 2 | `0x0023A64A` |
| `0x02EBF148` | 4 | cat 3 / dir 5 | `0x0023A72C` |
| `0x02EBF140` | 4 | cat 4 / dir 6 | `0x0023A74D` |
| `0x02EBF150` | 3 | cat 0 / dir 0 | `0x0023A6A1` |
| `0x02EBF168` | 2 | cat 1 / dir 1 | `0x0023A70B` |
| **`0x02EBF130`** | **8** | **NO** — the growth table `repos-1e` names | `0x0023AA66` |
| **`0x02EBF170`** | **4** | **NO** | `0x0023A860` |
| **`0x02EBF190`** | **1** | **NO** | `0x0023AAAA` |

**Eight registry slots, three of them outside the `.ard` family — including the same `0x02EBF130`
`repos-1e` found in the other function.** So the confusion is not local to one reader; **two
independent functions mix `.ard` and non-`.ard` descriptors with identical lookup code**, and
nothing in the instruction shape distinguishes them.

**The result above is unaffected, and now for a stated reason rather than by luck.** All four join
indices are bounded against slots I resolved individually — `0x02EBF150`, `0x02EBF148`,
`0x02EBF140`, `0x02EBF168` — and all four are `.ard`. **The four reads sit at
`0x0023A6B4`–`0x0023A768`; the first non-`.ard` slot appears at `0x0023A860`.** The safe region ends
there.

> **Recorded as a boundary, not a warning.** Anyone continuing this function past `0x0023A860` is
> reading growth definitions and two unidentified tables, and **the corpus will not object**, because
> those are real rows in real tables — just not the ones being decoded. That is what makes this class
> of error survive: it fails no check.

## `repos-1e`'s objection was right, and testing it produced the better finding

**Their objection:** for slots 0/5/6 the join index is bounded against an `st2e` descriptor's count —
a field whose meaning is established. For slot 1 it is bounded against **a bare `u16` at `+0x00`
that I assumed was a count.** If it is not a count, "1,146/1,146 in range" tests against an arbitrary
number and the 0.688 coverage measures nothing. **They were right to refuse the four-row table as
one finding.**

**So I tested the assumption instead of re-wording it — and slot 1 is the `.nmb` container format.**

| test, over all 166 areas | result |
|---|---|
| `+0x02 == 100` | **166 / 166** |
| `offsets[0] == 4 + 4·(count + 1)` | **166 / 166** |
| offsets ascending | **166 / 166** |
| `offsets[count] ≤ block extent` | **166 / 166** |
| every offset inside the block | **166 / 166** |

That is **exactly** the header and offset table documented in
[`area-nmb-index.md`](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md):
`{u16 count, u16 version = 100, u32 offsets[count+1]}`, first offset `4 + 4·(count+1)`. **The same
container ships as the standalone per-area `.nmb` file and as `.ard` directory slot 1** — one design
used twice, the same trick `CML1` plays across EBP slots 8 and 10.

**So the `u16` at `+0x00` is a count**, established by the container's own arithmetic rather than by
my assuming it: `offsets[0]` is a function of it in every area, and the offset table it heads is
well-formed on four further tests.

**The payload differs, which is why this is a container match and not a format match.** `.nmb`
entries are all 3 bytes; slot 1's are large and variable — 56 B in 165 areas, then 872, 800, 632,
1,256, 1,136, 920, 944. Entry heads are dominated by `01 00 00 00` (165 areas). **Same envelope,
different contents.**

### Four of the five slot-1 asymmetries collapse into one cause

Not `st2e`; count is a `u16` at `+0x00`; bound against `[+0x00]` not `[+0x04]`; and a different
binder (`0x003846F0`, `repos-4b`) — **all four are the same fact: it is not an `st2e` table, it is
an `.nmb`-format blob heap, and it needs a different binder because it is a different container.**

**The fifth does not collapse and is now the interesting one.** The **signed** compare — `jg` at
`0x0023A724` where the other three use `ja` — is unexplained. `repos-4b` reads it as the most
diagnostic of the five, on the grounds that a signed compare on an index is usually a different
author or era rather than a different intent. **I have not settled it.**

### Reporting corrected, per the objection

The four joins **must not** be reported as one finding, and are not any more:

- **Three joins into `st2e` tables — slots 0, 5, 6.** Index bounded against an established count
  field; **1,146/1,146 in range and coverage 1.000** — every row of every target referenced in every
  area. **This is the strong result.**
- **One join into an `.nmb`-format heap — slot 1.** The bound field is now established as a count
  (above), so "1,146/1,146 in range" stands. **Coverage 0.688 is a separate and weaker statement**:
  roughly a third of slot-1 entries are referenced by no slot-2 row in their own area, and **what an
  unreferenced entry means is not known.**

> **The objection improved the result twice over.** It separated a strong finding from a weak one,
> and testing the assumption it targeted turned an unknown table into a known container. **I would
> have reported the four joins as one row and been unable to say why slot 1 was different.**

## Slot 1, continued: `8 + 24k` verified, the header falsified, and the binder read

**`repos-1e`'s `8 + 24k` claim, re-derived with my own parser: 1,422 / 1,422**, `k = 2 … 125`,
lengths 56 … 3,008. Each slot-1 entry is an **8-byte entry header plus `k` records of 24 bytes**.
`24` is none of `84/88/56/56` — one more independent reason slot 1 is not an `st2e` table.

*(Their 1,422 counts **entries**; my earlier "56 B in 165 areas" counted **areas** containing a
56-byte entry — 160 by my parse, 162 areas having a slot-1 block at all. Different populations, not
a disagreement, and I should have said which I was counting.)*

### The entry header does not carry the record count — falsified, not declined

`repos-1e` declined to name the 8-byte header because its first two `u16` look like a count in some
entries `(1,0)×165` and plainly do not in others `(1282,1541)×18`. **Tested rather than left open:**

| test | result |
|---|---|
| `u16[0] == k` | **0 / 1,422** |
| any `u16` at `+0x00/02/04/06 == k` | **0 / 1,422** each |
| either `u32` at `+0x00/04 == k` | **0 / 1,422** each |

**No field of the header equals the record count, in any position, at either width.** That is a
stronger statement than "I would not name it", and it kills the reading their `(1,0)` sample
suggests.

**The header is eight small bytes, not four `u16`.** Every byte across all 1,422 entries lies in
`0 … 17`; byte 0 is never zero (`1 … 16`), bytes 1–7 may be. `repos-1e`'s "1282, 1541" are just byte
pairs — `02 05`, `05 06` — read as `u16`. **`corr(sum(bytes), k) = 0.9746` and no exact identity
holds**, which is precisely where I stopped: a 0.97 correlation with no closed form is the shape of
a relationship, not evidence for one, and going further would be naming a field from its numbers.

### The binder settles it — `FUN_003846F0` is a recursive offset-table rebaser

The reader `repos-4b` flagged as "the different binder, third argument zeroed" is 177 bytes and does
this:

```
00384704  call RuntimePointer_EncodeImageAddress   ; encode the block pointer
00384709  mov  [rdi], eax                          ; store it into the registry slot
00384727  movzx ebx, word ptr [rax]                ; THE u16 COUNT AT +0x00
00384746  lea  rbx, [r9 + 4]                       ; the offset table starts at +4
00384780  add  dword ptr [rbx], ebp                ; REBASE each offset in place
0038476B  call 0x3846f0                            ; ...or RECURSE, with r8d = depth-1
```

**Three things follow, and they are the point of this section:**

1. **A second, independent reader confirms the count field.** The binder reads the `u16` at `+0x00`
   at `0x00384727` and walks the table from `+4` — from the *bind* side, where the use side
   (`0x0023A724`) reads it as a bound. Two readers, one meaning.
2. **The offsets are rebased in place** (`0x00384780`), so the loaded block is not the file — the
   same behaviour the `.ard` sheet records for the fixed descriptors, now shown for this container.
3. **The zeroed third argument is a depth limit, not an incidental difference.** `r8d` is decremented
   into the recursive call at `0x0038475B`, and `test ecx,ecx / je` at `0x00384750` takes the
   non-recursive branch when it is zero. **`BattleData_SetAreaArdSectionCategory` passes `xor r8d,r8d`
   — depth 0 — so the `.ard`'s slot-1 block is rebased one level only.** The function is built for
   *nested* offset tables and the `.ard` uses it flat.

> **That closes `repos-4b`'s observation with a mechanism.** "Bound by a different binder with a
> third argument zeroed" is now "bound by a recursive rebaser told not to recurse", which is a
> different kind of fact.

**The signed `jg` at `0x0023A724` is still unexplained** and is now the *only* slot-1 asymmetry
without a cause. `repos-1e` is right that the tidy explanation of the other four should not be
allowed to pull it in: a container difference does not make an index signed.
