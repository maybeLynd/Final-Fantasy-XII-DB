---
system: The unresolved 158
category: 99-Unresolved-Residual
status: DOCUMENTED
owner_layer: none — this document exists to describe what has no owner
evidence_tier: 3
level: L1
readiness: CLASSIFIED
confidence: HIGH
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `001C2980`, `0020ED30`, `0023EFC0`, `0024B9B0`, `00256CA0`, `0028AAA0` and 17 more, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range - re-run the additivity test at each checkpoint
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  coverage_dump: verify/coverage.tsv @ 2026-09-02 01:23
last_reviewed: 2026-09-08
audit:
  passes: 2
  last_pass: 2026-09-02
  last_pass_state: five-largest-read-structure-derived-twin-account-corrected
  crossref_clean: true
  reopened_count: 3
---

# The unresolved 158

> Of 38,161 functions, **158 have no owner, no final-no, and no code domain.** They are not
> leftovers or stubs — **every single one is large**, the median is 828 bytes, and the biggest is
> 7,489. What survived classification is the hard part.

**One system has now been recovered out of this residual** and moved into the database proper:
[numeric formatting and character mapping](../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md).
Section 1 said *"somewhere in these 158 functions is behaviour a player experiences every session,
and this database cannot yet say which behaviour."* It can now name one: **every number the game
draws.**

**This document was originally about absence.** As of 2026-09-02 that is no longer entirely true:
**the five largest have been read** (section 9), and the set has been characterised structurally —
it is not 158 scattered singletons but **14 connected clusters plus 109 singletons**, and **~~15~~
~~functions have no caller at all~~** *(answered: see §7, NARROWED 2026-09-16: thirteen of the 139 have no incoming edge, and edges are not reach; 2026-10-02, OPUS)*, which is itself the best available explanation of why they
resisted classification.

> **Ledger status, 2026-09-14 (GN161).** The 109 ~~singletons~~ bodies of `residual-109-classification.tsv` *(corrected 2026-10-02, OPUS: the batch's rows include cluster members `002A4830`, `002A4430`, `002AF960` and `00256CA0`, so they are 109 of the 139, not the singletons)* are **no longer
> unresolved**: batch `R109` applied the body-read CodeDomain classification of
> `residual-109-classification.tsv` (65 ENTRY-MENTION + 44 UNTOUCHED rows, AUDIT-SEM
> accept-with-narrowing). The certified ledger now reads `unresolved=30`,
> `pct=99.92139`. This page remains the historical record of the residual's structure and
> of how it was read; the live count is `GfzEnv.ps1` and `COVERAGE.md`.

## 1. What the player sees

Nothing, and that is the point — but not for the usual reason.

These are not tiny helpers or dead code. They are among the **largest functions in the game**, so
whatever they do, they do a lot of it. Somewhere in these 158 functions is behaviour a player
experiences every session, and this database cannot yet say which behaviour.

That is the honest state of the work: 99.6% of the executable is classified, and the remaining
0.4% is disproportionately substantial code.

## 2. What the residual actually is

### The ledger

```
V121_COVERAGE  internal=38161  owner=9409  finalNo=585  codeDomain=28009
               overlap=0  explicit=38003  unresolved=158  pct=99.58596
```

A function is **explicit** if it has at least one of: a `PrimaryOwner`, a `finalNo` disposition, or
a `CodeDomain`. Cross-layer overlap is 0. **Unresolved means none of the three.**

### Size — the whole story

| Bucket | Count |
|---|---:|
| under 128 B | **0** |
| 128–511 B | 25 |
| 512 B and over | 133 |

```
n = 158    min = 310 B    median = 828 B    max = 7,489 B
total = 180,134 bytes = 2.25% of .text
```

**There is not one small function in the set, and not one thunk.** That is not what a leftover pile
looks like. Small functions are easy to classify — a 12-byte adapter or a 6-byte getter has an
obvious mechanical shape, which is exactly how the `NativeLeaf` / `NativeAdapter` families were
assigned. Large functions with mixed control flow, many callees and no distinguishing string resist
every mechanical test at once.

**The residual is a difficulty gradient, not a remainder.**

### Distribution

The 158 are scattered over **37 distinct 64 KB pages** from `0x0018xxxx` to ~~`0x004Fxxxx`~~ `0x005Dxxxx` *(corrected 2026-10-02, OPUS: recount of `residual_addrs.txt.GN158`: 37 pages, the last member in page `0x005D`, 33 members at or above `0x0050xxxx`)*. They are
not one unclassified module — they are spread thinly through the whole text section, with the
heaviest single page holding ~~9~~ 13 *(corrected 2026-10-02, OPUS: pages `0x002A` and `0x0057` hold 13 each, same recount)*.

### The largest

| Address | Size |
|---|---:|
| `002AC5F0` | 7,489 B |
| `004EDB50` | 7,440 B |
| `004F5360` | 7,440 B |
| `002A0440` | 5,301 B |
| `002F0280` | 5,130 B |
| `001E8580` | 3,572 B |
| `003649A0` | 3,020 B |
| `002B8EE0` | 2,865 B |

**`004EDB50` and `004F5360` are byte-for-byte the same length**, 7,440, and sit 0x7810 apart.
They are *not* clones: they are the same routine specialised to a different slot base. A hash-based
dedup would never have paired them, since the reflection document already proved clones do not share
a body hash.

**The earlier account of the difference was wrong in two ways and is corrected in section 8b.** It
said "~23 index constants shifted by exactly +2". The true figure is **42** single-byte `+2`
differences, and the shift is **not uniform**: two further constants shift `0x0A -> 0x45`, a delta
of **+59**. The byte *total* (1,228) was right; its classification was not.

## 3. Key addresses

The complete list is
[`Database/Tools/evidence/GM160_CURRENT160_ADDRS.txt`](../../Tools/evidence/GM160_CURRENT160_ADDRS.txt)
— **160 entries, one per line, and now tracked in git.**

> **This citation was changed on 2026-09-08, and the reason matters.** It previously named
> `Database/Tools/work/verify/residual_addrs.txt` *“(158 entries)”*. **That file now holds
> 139.** `work/` is gitignored, so the list is mutable and unversioned, and it was regenerated
> twice after this document quoted it. The document was not wrong when it was written; it had
> no way to stay right. See §11 and
> [the research-provenance index](../_index/RESEARCH-PROVENANCE.md) §3.

| Address | Size | Read? |
|---|---:|---|
| `002AC5F0` | 7,489 B | **yes — 2026-09-02** |
| `004EDB50` / `004F5360` | 7,440 B each | **yes — 2026-09-02, both** |
| `002A0440` | 5,301 B | **yes — 2026-09-02** |
| `002F0280` | 5,130 B | **yes — 2026-09-02** |
| `001E8580` | 3,572 B | **yes — 2026-09-03**, [painting-a-line-of-text-into-a-render-target](Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md) |
| *(152 more)* | 310–3,020 B | no |

**~~Eight of 158 have been read~~** ~~(section 9). The other 150 have not.~~ *(answered: see §7: "Every member now has a reading"; 2026-10-02, OPUS)*

**A doubt was raised against this document's "no caller" claim about `002AAE40` and it has been withdrawn.** The
live analysis program reports a **zero-byte body** for `002AAE40` and returns **no callees** for it,
while the function decompiles in full with fifteen direct calls — so it looked as though the
*"purest example … no caller"* (`002AAE40`) characterisation might be describing an empty body.

**It is not.** The snapshot call graph this document's analysis actually used has the edges:
`edges.tsv` records `002AAE40` with **16 outgoing and 0 incoming**, against controls like `002AC5F0`
(44 out, 7 in). **The absent callers are a real property of the function, independently of the live
program's state.** The claim stands as written.

> **What does not survive is the live program as a source.** Sampled 15 residuals: **8 have
> `body_start == body_end`** — `002AAE40`, `004EDB50`, `004F5360`, `002B8EE0`, `002F0280`,
> `0020AC30`, `001D72F0`, `001C2980` — while `edges.tsv` carries their edges normally.
> **Use `Tools/work/graph/edges.tsv` for any call-graph question about a residual; do not use
> `get_function_callees`.** See
> [drawing-a-line-character-by-character](Glyph-Run-Rendering/drawing-a-line-character-by-character.md) §5.

**`001E8580` was reached from the pair frontier, not from this table** — it shares one field
displacement (`+0x2348`) with `001E8070`, itself a residual at survey date (line 13 of `residual_addrs.txt`; classified GN161 `Presentation.Text.GlyphQuadVertexEmissionAndLineBoundsAccumulation`),
named in the glyph-run document by the string `fontclut_%d` and never opened. **Reading the pair
closed two residuals at once**, and neither was chosen for its size — `001E8070` is 1,293 bytes and
would not have been reached by working down this table for a long time.

**Ledger rows for both are authored and staged** at
`Tools/work/pending/repos55_text_target_pre.tsv` (domains `Presentation.Text.*`). They are **not
applied**: `Apply-GfzBatch.ps1` asserts the project is unlocked, and the project is currently open
to the analysis server. **Until they are applied the ledger still counts both as unresolved**, so
`ledger_resolved` will read 154 and not 152.

## 4. Data structures and formulas

```
explicit(f)    = hasOwner(f) OR hasFinalNo(f) OR hasCodeDomain(f)
unresolved(f)  = NOT explicit(f)

pct = 100 * explicit / internal = 100 * 38003 / 38161 = 99.58596%
```

**Completion target:**

```
done  iff  unresolved == 0  AND  every explicit function has a real document
```

The second clause is the larger job. ~11,800 functions carry a generic shape class
(`NativeRoutine.*`, `NativeLeaf.*`, `NativeInline.*`) which accounts for a function without
explaining it — see the evidence standard.

## 5. Call chain

Not applicable, and stating why matters: a call chain for these functions cannot be written without
reading them. The call graph *does* record their edges, so a future pass can start from callers —
that is the recommended attack in §6, not a claim about behaviour.

## 6. How to close this category

In the order a future pass should try them:

1. **Read one of the 7,440-byte twins** (`004EDB50`, `004F5360`). Section 8b proved they differ only
   by a +2 index shift, so one read explains both.
2. **Read the largest first.** `002AC5F0` at 7,489 bytes was the single biggest unclassified
   function in the game — residual when surveyed, classified at GN162 as
   `UI.Text.ControlCodeInterpreter`.
3. **Use callers, not the body.** Every residual function has edges in `graph/edges.tsv`. A
   function called only from Audio-owned code is not thereby Audio-owned — the evidence standard
   bans that inference — but it *is* a strong hint about where to look for authored strings.
4. **Check for authored strings first.** `string_xref.py` mapping RIP-relative LEAs to functions
   named 237 functions in an earlier pass at essentially zero cost.
5. **Expect no cheap wins.** These 158 survived every mechanical classifier the GFZ applied across
   121 versions. Each will likely need a body read.

## 7. What is not known

- [x] **UQ-378.** What any of the 158 functions do. **AC-1 — this is the category.** Nine have now been *(closed — the register row is WITHDRAWN.)*
      *described* (shape, callers, callees, state touched) but none *explained* in player terms.
- [x] What the 13-function cluster is. **`UQ-383` — PARTIALLY ANSWERED 2026-09-02, see §11.**
      *(Re-labelled 2026-09-15 (FABLE): this bullet and the census note at §"Two consequences" below both
      said `AC-6`, and they are different questions. The register's `AC-6` row is the census one, so
      this bullet had no row of its own; it is now `UQ-383`. The `AC-6` row itself is untouched —
      whether the label should be retired is the register owner's call, filed as
      `FABLE-NOTICE-OPUS-AC6-IS-TWO-QUESTIONS`.)* The
      libxml2 hypothesis was killed. The text/number hypothesis was killed and then **reinstated on
      decisive evidence**; four of thirteen functions are read and the result is documented as
      [`16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`](../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md).
      **Nine functions remain.** The Audio question is answered: both doors are **object message
      handlers** entering from their per-frame update case, and `0209C4D0` is an **8-slot ~~actor~~
      ~~registry~~ message-window registry** *(corrected 2026-10-02, OPUS: §11's correction, slots filled by `002A6190`+0x6B..+0xAE)* whose readers are named `InputGameplay_GetActorStateAwareRemappedMask*`. The
      cluster therefore holds actor update logic *as well as* text layout, and how those relate is
      the remaining question.
      ***ANSWERED 2026-09-18 (FABLE) — the cluster is the message and selection window's text engine, and the two Audio doors are that window's per-frame draw and its animation.** Every member now has a reading: six on 2026-09-03, five more placed on 2026-09-15, and the two doors read today. `002A4830` (1,701 B) **draws the window's rows**: for each of the `+0x3C2` records of the `0x28`-byte array at `0209C700` (the store's `TextLayoutRecord`) it copies the window's `+0xD0` draw block to the stack, scales the window's RGBA bytes `+0x90`..`+0x93` by the fade words `+0x58` / `+0x5A` (`imul`, `sar 7`; `002A4954`..`002A49B8`), takes the record's fields — `+0x08` to state `+0x60`, `+0x18` into flag `0x800`, `+0x1C` to `+0x54`, `+0x20` to `+0xA6` — lays the row at the pen y accumulated from each record's `+0x24` row height (`002A4A0D`, `002A4A12`), and draws its `+0x22` runs through `002B2930` / `002B2880` (`002A4A21`..`002A4A62`); the row whose index equals `+0x3C0` is the **cursor row** and takes the special arm at `002A4A67` (its `+0x10` text is what `0209C980` publishes). `002A4430` (1,020 B) is the **open / close / scroll animation** path: it tests the window word `+0xB0` for `0x20000000`, `0x40000000` and `0x100000`, steps with the timing constants `01E0CDAC` / `01E0CDB0` / `01E0CDB4` / `01E0CDBC` / `01E0CDC0` through `00244070` / `002B2D60` / `00368360`, and fills the line scratch `0209C630`. `002A6190`'s case 4 chooses between them by the flag bits §5 names. The four-field group is the window's list state, named by its writers: **`+0x3BE`** (word) the scroll offset `002A5020` returns (stored at `002A5E50` and `002A599B`, copied to `0209C61C` on every cursor move, `002A6132`); **`+0x3C0`** the cursor row — `002A5F40` moves it down or up on the input bits, bounded by `+0x3C1 − 1` (`002A60B6`..`002A6102`), and `002A5CC0` resets it to the last row (`002A5E2C`..`002A5E31`); **`+0x3C1`** the row total, `002A5CC0` summing each record's `+0x22` over the `+0x3C2` records plus one (`002A5DF3`..`002A5E1C`); **`+0x3C2`** the record count (`002A3250` increments it per added record, `002A2720` and `002A2C00` zero it, `00241D40` fixes it at 4); and **`+0x3C5`** the input-wait flag (`0x80` by `002A3730`, 0 by `002A38C0`, read by the four `InputGameplay_GetA*` getters and `002A6190`). So in player terms: a text window with selectable rows — the choice lists and menus built from text records — redrawn every frame with its fade and its highlighted cursor row, scrolled by the offset, animated open and closed, and moved by the pad. Static: the two door bodies, the field-group sweep (every access at `+0x3BE`..`+0x3C5`), the record array's uses.*
- [x] ~~What `DAT_01E0CE08` is.~~ **ANSWERED 2026-09-02** — not authored data. It has exactly two
      references, a `MOV` write and a `LEA`, **both inside `002AC5F0` itself**. It is that
      function's private scratch global, not a shared table.
- [x] ~~What a 16-byte record in the `0x02064E30` bank is.~~ **AC-7** — the twins walk it and hand each
      *Identified 2026-09-13 (FABLE), box left for the ledger mirror:* the bank is the emulated **VU1 memory** (1,024
      16-byte cells) of [the VIF1 / VU1 layer](../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md). The twins are
      microprogram code, and their leaf `004EF860` hands a pointer into VU memory to the GS callback, which is XGKICK-shaped
      (not yet proved).
      record to a callback (§11). Identifying one record identifies both 7,440-byte functions.
- [x] Whether they share any common property beyond size. *(Marker normalised 2026-09-30 (FABLE, [record](../_index/candidates/qid-marker-truth-fable-0930/README.md)): AC-2 is ANSWERED 2026-09-26.)* **AC-2 — PARTIALLY ANSWERED
      2026-09-02.** Two real shared properties found: (a) the set is **connected**, forming 14
      clusters plus 109 singletons, with one cluster of 13 functions holding 21,162 B — 11.7% of
      the residual in a single component; (b) ~~**15 have no caller at all**~~ **some have no
      incoming call edge**, so they carry no call-graph context for a classifier to use.

      > **NARROWED 2026-09-16 (FABLE), on two counts, and the wording is the load-bearing one.**
      > *"No caller **at all**"* reads as unreachable, and this page says otherwise about a member
      > of the set. Its own §7 cell phrases it correctly for `002F0280` — *"0 — no caller **in the
      > graph** … reached only indirectly"* — while **`AC-4`, answered on this page on 2026-09-14,
      > establishes `00565E00` as reachable from a player-visible action**, and `00565E00` is one of
      > them. **The claim this measurement supports is about incoming edges, not about reach.**
      >
      > **And the number re-measures as thirteen.** Over the **139** residual addresses in this
      > page's three companion tables, against the **current** `edges.tsv`, thirteen have no
      > incoming edge: `0020AC30`, `0023F8B0`, `0028B860`, `002A86A0`, `002D66D0`, `002F0280`, `003FAF10` (interior read 2026-09-17, SWE2-FRONTIER: 1,226 B — `0035D480` first at [`003FAFC1`](../_index/ADDRESS-INDEX.md), `003FB8F0`/`002D8D10`/`00861F74` ×2), `003FDFE0`, `00565E00`, `00566680`, `0056E140`, `0056F810`, `005771F0`. That is a **second measurement with its population named**,
      > not a claim that two of the fifteen acquired callers — the 2026-09-02 population cannot be
      > reconstructed from here, so the members are listed instead, so anyone can repeat it.
      >
      > **What is not disputed is that the absent edges are real.** This page refused an earlier
      > doubt about `002AAE40` and was right to, and **that refusal is carefully worded about edges
      > and claims nothing about reachability.** This narrowing agrees with it.
- [x] ~~Whether `004EDB50` and `004F5360` are clones.~~ **AC-3 ANSWERED — not clones.** Same
      routine, different slot base. **The original account was corrected on 2026-09-02**: 42
      single-byte `+2` shifts (not ~23) and two `+59` shifts (not "exactly +2"). All 1,228
      differing bytes are now accounted for exactly — see section 8b.
- [x] ~~Whether any is reachable from a player-visible action. **AC-4.**~~ **Answered 2026-09-14 (FABLE): yes.**
      `00565E00` (1,914 B) was one of the thirty functions listed as unresolved in the certified
      GN161 ledger (`verify_GFZ_PARENT/residual_addrs.txt`) — residual when surveyed; classified at
      GN162 as `UI.Widget.OnceRegisteredCommandBandProcedure`. It is the message handler of the
      **inventory category list**.
      - Its only registrar `00565DD0` is called only by the menu state machine `00281ED0`, for menu request `0x4B8`.
      - Its kind-1 arm builds one row per item category the party holds.
      - Source: [the 512-byte widget page](../16-UI/Widget-Object-Model/a-512-byte-widget-that-registers-itself-once.md)
        §7, EJ-1 and UQ-181.
      - So opening that menu page runs a residual function. Whether the other 29 are player-reachable is not claimed.
- [x] ~~**UQ-379.** Why the GFZ's own mechanical classifiers failed on all 158. **AC-5 — would say something
      about the classifier, not just the functions.**~~ **ANSWERED 2026-09-14 (OPUS)** — and it does say
      something about the classifier: §*AC-5 / UQ-379* below runs the counterfactual this document said
      had not been run. Against classified bodies **of the residual's own size**, the residual is not
      short of any classifier input — same incoming call context, **more** outgoing, and 2,838 of the
      2,858 same-size bodies carried no symbol either. No graph signal separates them, so the failure
      is a property of the decision rule, which is not in this repository.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 158 unresolved of 38,161 | `verify/coverage.tsv`, the certified coverage dump | 3 |
| The explicit/unresolved definition and 0 overlap | same dump's header line | 3 |
| Size distribution, median 828 B, max 7,489 B | joining `residual_addrs.txt` against `graph/functions.tsv` | 1 |
| No function under 128 bytes, no thunks | same join | 1 |
| 2.25% of `.text` | 180,134 residual bytes over `.text` virtual size `0x7A0800` | 1 |
| Spread over 37 pages | address census of the 158 | 1 |
| Two functions of identical 7,440-byte size | same census | 1 |

### A stale export, caught by disagreeing with itself

Deriving the unresolved set independently from `graph/functions.tsv` produced **160**, not 158 —
a strict superset containing `002F7380` and `00313A00`. Both genuinely have no owner, no finalNo
and no CodeDomain **in that file**.

The resolution is timestamps:

```
graph/functions.tsv          2026-09-02 01:09
verify/coverage.tsv          2026-09-02 01:23
verify/residual_addrs.txt    2026-09-02 01:23
```

**The function dump is 14 minutes older than the coverage dump.** Those two functions were
classified in between. Both files are internally consistent — `38003 + 158 = 38161` and
`38001 + 160 = 38161` — they simply describe program states 14 minutes apart.

**The ledger is correct and current; my derivation was reading an older export.**

Two consequences, both recorded rather than assumed away:

- The authoritative residual is `verify/coverage.tsv` and `residual_addrs.txt`, not a fresh
  derivation from `functions.tsv`.
- **Every census in this database taken from `graph/functions.tsv`** — family counts, caller
  counts, owner tallies — reflects the **01:09** state. Bulk classification counts are very
  unlikely to have shifted materially in 14 minutes, but the provenance is now on record so any
  figure can be re-derived against a fresher dump. Tracked as **AC-6**.

### Why this document is tier 3

Its central facts come from a GFZ coverage dump, which is tier 3. The size, distribution and
address statistics computed on top of that are tier 1 arithmetic over exported data — but they
describe the *set*, not the *functions*. Nothing here is tier 1 about any function's behaviour,
because no body was read.

A document about unresolved code that claimed to explain the code would be self-refuting.

## 8b. Reopened 2026-09-02 - AC-3 answered: not clones, near-twins

The two 7,440-byte functions `004EDB50` and `004F5360` were compared byte for byte. **They are not
clones.** They are two instantiations of the same routine, differing by a systematic constant.

```
address delta = 0x7810
differing bytes = 1,228 of 7,440  (16.51%)
```

Every differing byte is accounted for:

| Kind | Bytes | Detail |
|---|---:|---|
| rel32 displacements shifted by exactly `0x7810` | ~~~1,186~~ 1,184 | 395+ groups, all the same delta *(corrected 2026-10-02, OPUS: byte diff of the twins: 1,228 differing bytes, 1,184 of them in 395 rel32 fields, 44 single bytes)* |
| small immediates, **exactly +2** in B | 42 | ~23 distinct constants |
| a differing constant `0x0A` -> `0x45` | 2 | at `+0xCF2` and `+0x1AAB` |

The immediates form a clean contiguous run:

```
0x1F->0x21   0x24->0x26   0x29->0x2B   0x2A->0x2C   0x2B->0x2D   0x2C->0x2E
0x2D->0x2F   0x2E->0x30   0x2F->0x31   0x30->0x32   0x31->0x33   0x32->0x34
0x33->0x35   0x34->0x36   0x35->0x37   0x36->0x38   0x37->0x39   0x38->0x3A
0x39->0x3B   0x3A->0x3C   0x3B->0x3D   0x3E->0x40   0x3F->0x41
```

Seen in context these are index and displacement constants:

```
A:  8d 41 3e     lea eax,[rcx+0x3E]        B:  8d 41 40     lea eax,[rcx+0x40]
A:  83 c1 1f     add ecx,0x1F              B:  83 c1 21     add ecx,0x21
A:  8d 47 30     lea eax,[rdi+0x30]        B:  8d 47 32     lea eax,[rdi+0x32]
```

**The same code, indexing a structure whose fields sit 2 bytes further along.** That is a template
instantiation or a hand-specialised variant, not a linker-folded duplicate - and it is a more
interesting answer than the "clones" hypothesis this started from.

**Consequence for the residual:** reading one of the two effectively explains both, since the only
semantic difference is a +2 index shift. That still leaves 157 to go.

### A second narrow-test false negative

The first pass reported "1,184 of 1,228 explained" and left 44 bytes unaccounted. Four of those
were the function's **tail `jmp`**:

```
A tail:  5f 5d 5b e9 00 00 00 00      pop rdi; pop rbp; pop rbx; jmp +0
B tail:  5f 5d 5b e9 f0 87 ff ff      pop rdi; pop rbp; pop rbx; jmp -0x7810
```

That is the same `0x7810` delta - the scan missed it because the sliding window ran
`range(N-4)`, which excludes the final valid 4-byte offset at `N-4`. **An off-by-one in the test,
not a property of the code.**

This is the second time in this database that a **too-narrow test produced a confident false
negative** - the first being a byte check that looked for `0xC3` and missed `C2 00 00` (`ret imm16`).
Both were caught only because a residue refused to explain itself. The lesson is recorded here
rather than silently fixed: when a test leaves a small unexplained remainder, suspect the test
before concluding something about the code.

## 9. Related

- [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md) — the explicit/unresolved definitions and the ban on caller-ownership inference
- [`../_index/COVERAGE.md`](../_index/COVERAGE.md) — the ledger this document explains
- [`../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md) — why clone detection by body hash fails, relevant to AC-3
- [`../24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`](../24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md) — the `.text` size this residual is measured against

## 8b. The twins, re-derived at byte level (corrected 2026-09-02)

The two 7,440-byte functions were re-diffed directly against the authorized EXE, because section 2
made a **quantitative** claim ("~23 index constants shifted by exactly +2", "all 1,228 differing
bytes accounted for") and a quantitative claim can be tested exactly.

**The byte total was right. The classification of those bytes was wrong.**

| Category | Runs | Bytes | What it is |
|---|---:|---:|---|
| multi-byte runs | 395 | 1,184 | RIP-relative displacement fields |
| single byte, `+2` | 42 | 42 | index constants |
| single byte, `0x0A -> 0x45` | 2 | 2 | index constants, **delta +59** |
| **total** | **439** | **1,228** | matches the observed diff exactly |

### The displacements prove the specialisation is positional

The two functions sit exactly `0x7810` apart. Every RIP-relative displacement in `004F5360` that
targets the same global must therefore be `0x7810` **smaller**. The observed byte deltas are
precisely that, with borrow propagation:

```
0x7810 = 30736      low byte 0x10 -> delta -16   (x395)
                    next byte 0x78 -> delta -120  (x372)
                    borrows        -> delta -1    (x394)  and -121 (x23)
```

`395 + 394 + 372 + 23 = 1184`, plus `42 + 2 = 44` index bytes, is `1228` — **a complete account with
nothing left over**. The 395 displacement runs are the two functions pointing at the *same* data.

### They operate on identical state

Decompiled, the two reference **exactly the same 59 globals** spanning `0x02064B04`–`0x02064E3C`.
**No global is unique to either.** Both call exactly one function, the same 219-byte leaf
`004EF860`. Each has exactly one caller, and both callers are classified
`Boundary.Presentation.SingleOwnerReferencedSupport` — 22,073 B and 24,541 B respectively.

At C level the difference is 92 changed lines out of 879 (**94.77% identical**), and apart from the
function's own name **every single difference is a numeric constant** — there is no structural
divergence at all. The constants are used as `(index + K) * 0x10`, a **16-byte stride**.

### What this does and does not establish

**Established:** one generated routine, emitted twice, specialised to slot bases two apart, reading
and writing one shared ~824-byte state block through 16-byte-strided indexing.

**Not established:** what the slots are. The 16-byte stride and the constant `255.0f` present in
both are *consistent with* four-float vector registers, but this document does not assert that. The
test that would settle it is reading the shared leaf `004EF860` (219 B) and the two giant callers.

**Why the `+59` pair matters.** Under a pure "+2 specialisation" the two sites at file offsets
`+0x0CF2` and `+0x1AAB` should also have shifted by 2. They jump `0x0A -> 0x45` instead. Those two
sites reference something that is **not** part of the regularly-shifted bank, and they are therefore
the most informative two bytes in either function.

## 9. The first five read (2026-09-02)

Facts only. None of these is *explained* yet; describing a function's shape is not saying what a
player experiences, and this section does not pretend otherwise.

| Address | Size | Signature | Callers | Distinctive |
|---|---:|---|---|---|
| `002AC5F0` | 7,489 B | `(undefined8*, longlong*, float*, byte*)` | 7 — 3 unresolved at survey date, 2 `Runtime.RealFunctionPointerOrVtableMember` | calls `RenderCommand_SubmitCurrentBufferAndSwap`; 107 anonymous calls; constants cluster at `0x10C8`–`0x1102`, i.e. fields of one large object. Residual when surveyed — classified at GN162 as `UI.Text.ControlCodeInterpreter` |
| `004EDB50` | 7,440 B | `void (code*, undefined8)` | 1 — `Boundary.Presentation.SingleOwnerReferencedSupport` (22,073 B) | see 8b |
| `004F5360` | 7,440 B | `void (code*, undefined8)` | 1 — `Boundary.Presentation.SingleOwnerReferencedSupport` (24,541 B) | see 8b |
| `002A0440` | 5,301 B | `(longlong*, undefined4*, uint, uint, short*, int, int)` | 2 — **both `Presentation.Rendering.ShaderMaterial`** | 34 anonymous calls; constants `0x1000000`, `0x431`, and three 64-bit values `0x30AA400000000006` / `...0008` / `...8006`. Interior read 2026-09-17 (SWE2-FRONTIER): `00181560` first at [`002A04BD`](../_index/ADDRESS-INDEX.md), `002A1900` ×20 dominating, `00181890`/`00181330` ×3 |
| `002F0280` | 5,130 B | `void (code*, undefined8)` | **0 — no caller in the graph** | calls `sqrtf`; reached only indirectly |

Three of the five take a **`code *` first parameter** — a callback or dispatch entry. That is a
shape the GFZ's mechanical classifiers handle poorly, because such a function's behaviour is
determined by a pointer supplied at runtime.

## 10. The residual has structure (2026-09-02)

This is the most useful new fact in this document, and it replaces the earlier assumption that the
158 are independent leftovers.

### It is connected

Treating the 158 as a graph in which an edge exists when one unresolved function calls another:

```
14 clusters of 2 or more      109 singletons
largest cluster: 13 functions, 21,162 bytes = 11.7% of the entire residual
```

The largest cluster is `002A4430 002A4830 002AAE40 002ABB20 002ABF70 002AC5F0 002AE610 002AF340 …`
— and it contains `002AC5F0`, the single biggest unclassified function in the game. **Reading that
cluster would explain 13 of the 158 at once**, which is a far better return than any singleton.
(`002AC5F0` has since been classified at GN162 as `UI.Text.ControlCodeInterpreter`.)

**Six of the thirteen are now read** (2026-09-03): `002AC5F0`, `002AAE40`, `002B2150`, `002ABB20`,
`002ABF70` and `002AF340` — see
[measuring text by drawing it with the output off](measuring-text-by-drawing-it-with-the-output-off.md).
**The component's cause is now known**: the measure pass, the draw pass and the control-code
interpreter are **the same character walk under different settings of two globals**, so they call
each other by construction. ~~The remaining seven are `002A4830`, `002AE610`, `002AF960`,
`002A4430`, `00573BE0`, `002B5390` and `002B2DF0`.~~

**Corrected 2026-09-15 (FABLE): the list above is stale, and the page that overtook it is this
page's own consequence.** Five of the seven now carry a role, four of them stated on
[`numeric-formatting-and-character-mapping.md`](../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md),
which was written *because* this cluster was opened:

| was "remaining" | now |
|---|---|
| `002AE610` | **number → digits → glyph advances** — converts an integer by repeated subtraction of powers of ten, from the table at `00916520` |
| `002B2DF0` | **a 7-bit-masked walk of a NUL-terminated buffer** with two float accumulators |
| `002AF960` | **the slot-2 dispatcher**, not a drawer — `movsx rax, byte [rbx+0xA3]` / `lea r9, [rax+rax*2]` / `call [rdi + r9*8 + 0x7F64D0]`, the kind byte selecting through `009164D0` |
| `00573BE0` · `002B5390` | the reachability chain — `00573BE0` → `002B5390` → `002B2150` reaches the hub at depth 3, which is what falsified the dispatch page's §6b unreachability claim |
| `002A4830` · `002A4430` | **the true remainder.** Their *entry* is documented — both are reached from `002A6190`'s case 4 — and their bodies are not read end to end |

**So the honest remainder is two, not seven**, and they are the two Audio doors.

**Both read, 2026-09-15 (FABLE) — the two Audio doors, characterised rather than closed.**

`002A4830` (1,701 B) opens on a **four-field group of its first argument**, three of them new and the
fourth already documented: `movsx esi, word [rcx + 0x3BE]`, `movsx eax, byte [r14 + 0x3C0]`,
`movzx r9d, byte [rcx + 0x3C2]`, and `+0x3C5`, the sub-step opt-in. **`+0x3C2` is a loop count** —
`test r9d, r9d / jle` skips the whole body — and `+0x3C0` is compared against the loop's index both
directly and as `(x - 1)`, so it bounds the walk. The body walks an array **through the image-base
idiom this database has been chasing all month**:

```asm
002A4926  lea  rdx, [rip - 0x18492D]              ; = 00120000
002A4A30  lea  r13, [rip - 0x184A37]              ; = 00120000
002A4A40  mov  rax, qword ptr [r13 + r15*8 + 0x1F7C700]   ; 0209C700 + r15*8
002A4A21  cmp  r12w, word  ptr [rdx + r15*8 + 0x1F7C722]  ; 0209C722 + r15*8
```

**Neither `0209C700` nor `0209C722` appears anywhere in the instruction stream** — both are
`00120000 + displacement`, which is why a `[reg + disp]` census does not see this array at all. Two
accesses share the index `r15` and the scale 8 at displacements `0x22` apart; **whether that is one
record array or two parallel arrays is not established and is not claimed.** The band is
`.data` BSS, so the array is runtime-filled, not authored — which is consistent with `0209C4D0`
two hundred bytes below it being the **live** message-window registry.

> **Resolved 2026-09-17 (SWE2-STRUCT): ONE record array, stride `0x28`.** The index is not `r15`
> but `r8d`: `movsxd rax, r8d` / `lea r15, [rax + rax*4]` at `002A4959`/`002A4963` makes
> `r15*8 = index*0x28`, so `0209C700/08/10/18/1C/20/22/24` are the fields of a 0x28-byte
> record — three pointers, three dwords, a byte and a u16 bound — not two parallel arrays.
> The element count is `byte[window+0x3C2]`; the element whose index equals `byte[+0x3C0]`
> gets its `+0x10` published to `0209C980`, and `0209C630` is a ~0x80-byte "line being drawn"
> scratch block the body fills with `movups`. Declared in the store as **`TextLayoutRecord`**
> (`ARRAY 0x0209C700 stride=0x28`) and the window objects as **`MessageWindowRecord`**
> (`SLOTPTR 0x0209C4D0 stride=0x8 count=8`) — `FABLE-REQ-…-REGISTRIES-HAS-NO-TYPE-ROW`.

`002A4430` (1,020 B) takes `lea rbx, [rcx + 0xD0]` and reads `+0xB0` eight times, and touches
**five consecutive globals** `01E0CDAC`, `01E0CDB0`, `01E0CDB4`, `01E0CDBC`, `01E0CDC0` — and
`01E0CDC0` is one of the three globals `002B2DF0` touches, so the two share state.

**Both doors call `002AF960`**, the slot-2 dispatcher, which is what makes them doors rather than
members. **What neither is yet:** explained in player terms. The shapes are read; what the array at
`0209C700` holds, and what the `+0x3BE`–`+0x3C2` group means, are not established here.

> **Recorded because it is the useful part.** I re-derived `002AE610`'s power-of-ten table from the
> bytes before noticing that `numeric-formatting-and-character-mapping.md` already names
> `00916520` as *"the power-of-ten table"* and `002AE610` as *"number → digits → glyph advances"* —
> **published by me.** The cluster page kept a worklist; the consequence page answered it; and
> nothing carried the answer back. That is the drift a *"what remains"* list attracts: it is written
> once and read as current forever.

Next largest clusters:

| Functions | Bytes | Members | read |
|---:|---:|---|---|
| 5 | 7,030 | `00245170` `002455A0` `00245E60` `002DA2D0` `002DA7C0` | **all five, 2026-09-03** |
| 3 | 6,775 | `002B8EE0` `002BCB00` `002DBDD0` | **all three, 2026-09-03** |
| 4 | 4,853 | `002DC290` `002DC7F0` `00392A10` `00392CE0` | **all four, 2026-09-03** |
| 3 | 3,464 | `00256960` `00256CA0` `00258350` | **all three, 2026-09-12** — [the scripted camera player](../17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md): the `CAM7` command interpreter and its two path-follow interpolation kinds; tags staged in `Tools/work/pending/fable_cam7_residual_pre.tsv`, not applied |

**Cluster 3 is closed and the clustering held.** All three members are documented:
[the blinking icon and its atlas](the-blinking-icon-and-its-atlas.md),
[drawing one coloured rectangle](drawing-one-coloured-rectangle.md), and
[the second icon drawer and what it adds](the-second-icon-drawer-and-what-it-adds.md).
**Both drawers call the primitive, twice each** — so the cluster was a real call cluster, and it was
grouped by the call graph **before any member had been opened.**

> **And the two drawers turned out to be one routine written twice**, differing in six measured
> ways. **That is the residual set's second specialisation pair**, after `004EDB50` / `004F5360` in
> §8b *(both members of that pair are now classified — `Presentation.LegacyPS2.VU1BankUpload` at
> GN161)* — so **two of the fourteen clusters are duplications**, which is worth knowing before
> estimating how much distinct behaviour the remaining 147 contain.

**Cluster 4 is closed too** — [the nine-patch window frame](the-nine-patch-window-frame.md). All
four members are one mechanism: a resizable box drawn as nine rectangles with a gradient sampled
across the whole window. **~~`00392A10` is one of the fifteen no-caller residuals~~** *(answered: see §"What would settle the cluster", UPDATED 2026-09-16: `00392A00` is `cmp word [rcx+0x58], 0` then `jne 00392A10` at `00392A00`+0x5, and `00392A00` has four callers; 2026-10-02, OPUS)* and its own
fallback `00392CE0` has exactly one caller, so **the pair was invisible from either end.**

**Cluster 5 is closed too** — [the widget tree draw pass](the-widget-tree-draw-pass.md)
and [the widget background and its atlas sets](the-widget-background-and-its-atlas-sets.md). Its root
`00245E60` is the recursive draw of the whole UI and **calls itself**; `00392A10` in cluster 4 and
`00245E60` here are both no-caller residuals reached only through tables.

> **Three clusters read, three clusterings held.** In both cases the call-graph grouping was made
> **before any member had been opened**, and reading them confirmed it. **That is the strongest
> support this section's structural claims have**, and it is worth more than the cluster counts
> themselves.

**41 of the caller-edges into unresolved functions come from other unresolved functions**, which is
why the set survived classification as a group rather than one at a time.

### Fifteen have no caller at all

**15 of the 158 have zero incoming call edges.** They are reached only indirectly — through a
vtable, a function pointer, or a jump table. This is the single best answer available to **AC-5**
("why did the mechanical classifiers fail?"): a classifier that reasons from call context has *no
call context to reason from* for these. Among them are `002F0280` (5,130 B) and `002AAE40`
(2,440 B).

### Where the rest are embedded

Caller CodeDomains for the whole residual (a hint for reading order, **not** an ownership claim —
caller-to-callee ownership inheritance is banned as proof in this database):

| Callers | CodeDomain of the caller |
|---:|---|
| 48 | `NativeRoutine.AcyclicDirectCall.ExtendedBounded` |
| 41 | **another unresolved function** |
| 26 | `NativeRoutine.BoundedLoop.DirectCallOnly` |
| 18 | `NativeRoutine.BoundedLoop.Extended.DirectCallOnly` |
| 16 | `Boundary.Audio.NativeSupport` |
| 14 | `NativeRoutine.AcyclicDirectCall.Bounded.Conditional` |
| 8 | `Presentation.UI.InputConsumerStateMachine` |
| 6 | `Runtime.ImageAddressMemoryStructure` |
| 5 | `Boundary.SaveLoad.NativeSupport` |
| 4 | `Presentation.Rendering.ShaderMaterial`, `Boundary.StoryEvent.NativeSupport`, `Runtime.RealFunctionPointerOrVtableMember` |

Most callers carry only a **generic shape class**, not a subsystem — so the residual is mostly
embedded in code that is itself only shape-classified. That is consistent with §4's warning that
~11,800 functions carry a shape class which accounts for a function without explaining it.

## 11. The 13-function cluster, opened (2026-09-02)

The cluster identified in §10 as the best target was attacked. It is **not** identified yet, but it
is no longer shapeless, and two hypotheses were killed — which is most of what an opening pass is
for.

### Anatomy

```
                002ABF70 (577)          002A4430 (1020)   002A4830 (1701)
                    |                        \               /
                002ABB20 (918)                 002AF960 (1117)
                    |                               |
                002AF340 (1563) ---------------.    |
                                                \   |
   002AAE40 (2440, NO CALLER AT ALL) ---------.  \  |
                                               \  \ |
                        002AC5F0 (7489) <====> 002B2150 (861)   <- mutual recursion
                            |       \                ^
                            |        `-> 002B2DF0 (598)
                            v                        |
                        002AE610 (1281)     002B5390 (747) <- 00573BE0 (850)
```

`002B2150` is the **hub**: six of the twelve other members call it, and it and `002AC5F0` call each
other. Five members are entered from classified code and are the cluster's doors:

| Door | Entered from |
|---|---|
| `002AC5F0` | `Runtime.RealFunctionPointerOrVtableMember` x2, plus two shape-classed routines |
| `002AF340` | five shape-classed routines |
| `002AE610` | **`Presentation.Rendering.ShaderMaterial`** |
| `002A4430`, `002A4830` | **`Boundary.Audio.NativeSupport`** (both from `002A6190`) |
| `00573BE0` | **`Boundary.Audio.NativeSupport`** (`005742D0`) |
| `002AAE40` | ~~**nothing — no caller at all**~~ **CORRECTED 2026-09-02** — no *caller*, but a base-relocation-certified function pointer at `00916518`. See the §11 entry |

### External interface (fact)

Everything the cluster calls outside itself that carries a name:

| Callee | Meaning |
|---|---|
| `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`, Presentation) | from `002AC5F0` — it submits render work |
| `ImageAddress_ResolveRuntimePointer` / `RuntimePointer_EncodeImageAddress` | it resolves and encodes **authored-data pointers** |
| `Boundary.StoryEvent.NativeSupport` x2 | from `002AC5F0` |
| `memcmp`, `memcpy`, a `strchr`-shaped byte scan | buffer work |

Being entered from **Audio**, **ShaderMaterial** and **vtable dispatch**, while calling
**Presentation** submit and **StoryEvent** support, makes this a cross-subsystem service rather than
one subsystem's internals. That is consistent with it having no single owner — which is a *reason*
it is unresolved, not an excuse for leaving it so.

### Two hypotheses killed

**Killed: libxml2.** A member calls `002B39A0`, which the GFZ names `xmlStrchr` and domains
`ThirdParty.XML.Libxml2`. With mutual recursion, `memcmp`/`memcpy` and vtable entry, a
recursive-descent XML parser was a good guess. It is wrong. `string_xref.py` found **zero**
references from the cluster to any XML string, and a raw byte scan of the EXE shows the binary
contains **no `CDATA`, no `DOCTYPE`, no `libxml` literal** at all (`xmlns` appears 11 times,
`<?xml` once). `xmlStrchr` is a signature-derived name for a generic `strchr`; calling it proves
byte scanning, not XML.

**The zero was positive-controlled before being believed** — patterns `PhyreObject` and `sead`
through the same tool returned 162 strings and 13 references. This database has been burned once by
trusting an unverified zero, and the rule adopted then was applied here.

**Killed, then REINSTATED on decisive evidence: text and number layout.**

> **This subsection records a wrong kill.** The hypothesis was rejected below on 2026-09-02 and
> then re-established the same day by reading `002AE610`. Both readings are kept, because the
> reason the kill was wrong is more useful than the conclusion.

**What reinstated it.** `002AE610` (1,281 B), which `002AC5F0` calls twice, contains an
unambiguous text-measurement loop:

```c
advance = *(ushort *)(glyphTable + (*p - 0x20) * 2);   // advance width, table based at ' '
...
p = p + 1;                                              // per character
*param_3 = fVar21 + *param_3;                           // accumulate a float pen position
```

and it *produces* the characters it measures by decomposing an integer against a **power-of-ten
table** read directly from `.rdata`:

```
00916520:  1  10  100  1000  10000  100000  1000000  10000000  100000000
```

**Why the kill was wrong.** The observation it rested on — that `002AC5F0`'s `byte *param_4` is
written and never read — is *correct*, and is still recorded below. The error was **generalising
from one parameter of one function to the character of the whole cluster**. The character loop was
never in `002AC5F0`; it is in the function `002AC5F0` calls. A negative about one function is not a
negative about its callees.

This is now documented as its own system:
[`16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`](../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md)
— **the first system recovered out of this residual**, and a player-facing one: it is the machinery
behind every number the game draws, and the reason counting digits do not jitter (the advance width
of `'0'` is hoisted out of the loop and used for all digits).

### The original kill, preserved

**Killed: text layout and drawing.** `002B2150` and `002B2DF0` take `(object, byte*, float*, ...)`
and `002B2DF0` genuinely walks a byte stream — see below — so "measure and draw a string, output
width and height" was the natural reading, and `002AC5F0`'s two `StoryEvent` callees supported it.

It does not survive reading `002AC5F0`'s own body. Its fourth parameter, which Ghidra types
`byte *param_4`, is **written and never read**:

```c
param_4[0] = 0;  param_4[1] = 0;  param_4[2] = 0;  param_4[3] = 0;   // at 5 sites
param_4[0] = 1;  param_4[1] = 0;  param_4[2] = 0;  param_4[3] = 0;   // at 4 sites
```

It is a **four-byte output status block**, not an input string. The big function does not consume
text at all, so the cluster is not a text pipeline hanging off it. **A `byte *` in a decompiled
signature is a type guess, not evidence of a string** — recorded here because the same trap will
recur across the remaining 153.

### What the bodies actually establish

Facts, no interpretation:

- **`002B2DF0`** (598 B) copies a **208-byte block** (26 x 8) from its first argument to the stack,
  then loops N times over a byte buffer: `v = *p & 0x7f; p++`, tests `v` against a bitmask taken
  from the copied block, scans forward for a NUL to get a length, and if `v` indexes inside it,
  **reads and then writes** `p[v]`. It zeroes two floats through `param_3` and accumulates into
  them, returning a third float. So: a **7-bit-indexed, in-place mutation of a NUL-terminated
  buffer, producing two accumulated floats**.
- **`002ABF70`** (577 B) is a per-tick state machine: `switch (*(uint *)(obj + 0xB0) & 0xFF)` over
  labels **0, 1, 2, 3, 4, 5, 7** (~~seven, no `default`~~ eight table entries, mode 6 and any value above 7 going to the epilogue *(corrected 2026-10-02, OPUS: `cmp eax, 7` / `ja` at `002ABF70`+0x15 and the eight table dwords its +0x22 load indexes, entry 6 = `002ABF70`+0x23B)*) — *corrected 2026-09-02, see §12*;
  accumulates `obj[0x9B] += obj[0x9C]`; fires when `obj[0x9C] == 0x1E` (30) or
  `obj[0x9B] > 0x1D` (29); clamps a `short` at **32000**. Thresholds of 29/30 on an accumulator are
  the shape of a **frame counter**, though nothing here proves the unit is frames.
- **`002AC5F0`** (7,489 B) writes the 4-byte status block above, calls `002AE610` twice — once with
  its own locals and once with a global at `DAT_01E0CE08` — and submits render work.

### `004EF860`, the leaf shared by both twins — read

The 219-byte function that both 7,440-byte twins call, and the cheapest thing in §10's attack
order:

```c
void FUN_004ef860(code *param_1, undefined8 param_2)
{
    i = DAT_02064DD0 << 4;                       // 16-byte stride
    DAT_02064C60..C6C = record at (&DAT_02064E30 + i);   // publish current record
    j = DAT_02064DB0 << 4;
    *(uint *)(&DAT_02064E30 + j) = DAT_02064DB8 + 0x8000;
    ... copy the record ...
    (*param_1)(&DAT_02064E30 + j, param_2, 0);   // <- the callback, given the record
    DAT_02064DB0 = DAT_02064B0C + DAT_02064DB4;
}
```

**This settles what the twins' `code *` parameter is for.** It is a **visitor callback invoked once
per 16-byte record**, over a bank based at `DAT_02064E30` — inside the same
`0x02064B04`-`0x02064E3C` state block the twins share. The twins are therefore **record-emitting
walkers**, and their `+2` slot specialisation (§8b) is a specialisation of *which bank position they
walk*. The constants `0x168` (360) and `0x2A8` (680) appear as additive wrap terms, and
`DAT_02064DB8 + 0x8000` flips the top bit of a 16-bit field.

This does not say what a record *is*. It does say the twins are traversal, not computation, which
is why 7,440 bytes of them contain almost no arithmetic.

### The Audio doors, opened — the premise was wrong

The cluster's two `Boundary.Audio.NativeSupport` entries were the most interesting loose thread:
why would audio code reach text layout? **It does not.** Both callers are **object message
handlers** sharing the signature `undefined8 f(longlong object, undefined4 *message)` and
switching on `*message`:

| Handler | Enters the cluster from |
|---|---|
| `002A6190` | **case 4** — its per-frame update (9 labels: 1, 2, 3, 4, 10, 12, 15, 18, 21) |
| `005742D0` | case 1 (construction) and case 10 (7 labels: 1, 3, 10, 12, 14, 15, 18) |

`002A6190` case 4 selects between two cluster functions by flag bits:

```c
flags = *(uint *)(object + 1000);
if (((flags >> 0xB & 1) == 0) && ((flags >> 0xD & 1) == 0)) {
    if ((flags & 0x700) == 0)  002A4430(...);          // update path A
    else                       002A4830(object, ...);  // update path B
}
```

**So `002A4430` and `002A4830` are two alternative per-frame update paths for one object type**, and
the "Audio" label describes the handler's boundary rather than the work it dispatches to.

### `0209C4D0` is an 8-slot actor registry

`002A6190` case 1 walks eight slots for the first free one, claims it, and stores the index in the
object at `+0x3B8`:

```c
do {
    if ((&DAT_0209C4D0)[i] == 0) {
        (&DAT_0209C4D0)[i] = object;
        *(char *)(object + 0x3B8) = (char)i;
        ...
    }
    i = i + 1;
} while (i < 8);
```

A reference census on that array names it, because **four of its readers already carry GFZ working
names**:

```
InputGameplay_GetActorStateAwareRemappedMask04   (002A28E0)
InputGameplay_GetActorStateAwareRemappedMask08   (002A2940)
InputGameplay_GetActorStateAwareRemappedMask0C   (002A29A0)
InputGameplay_GetActorStateAwareRemappedMask10   (002A2A00)
```

Each reads **slot 0** (`LEA` the base, then `MOV RAX, [RCX]`), while six further functions scan the
array with `CMP dword ptr [base + index*8], reg`. An array of at most eight entries, whose readers
compute **actor-state-aware input remapping**, is ~~an **actor registry**~~ the live **message-window registry** *(corrected 2026-10-02, OPUS: the slots are filled by the message handler `002A6190`, case 1 (`002A6190`+0x6B..+0xAE), whose same object draws a nine-patch frame through `00392A00` (+0x15E) and text through the font painter (+0x202); the four readers' bodies return the confirm-button mask while a window waits, and *actor* rests only on their GFZ working names — §"It is connected", `MessageWindowRecord`)*.

**This revises the cluster's identity.** It is not only text and number layout — that is one role
inside it. It also holds **per-frame update logic for a registered actor type**. How the two roles
connect is not established, and guessing at it is what this document exists to avoid.

### What would settle the cluster

1. `002AE610` (1,281 B) — called twice by `002AC5F0`, once with the global `DAT_01E0CE08`. That
   global is authored data; identifying it identifies the payload.
2. `002AAE40` (2,440 B) — ~~**attempted 2026-09-02, dead end.**~~ **REFUTED 2026-09-02, and this
   entry was the category's flagship example.** It has three data references *in the Ghidra
   database*, and all three are exception-handling metadata: one `.pdata` `RUNTIME_FUNCTION` entry
   at `02FAE428` and two `.rdata` ~~scope-table RVA pairs~~ **chained `RUNTIME_FUNCTION` records** at
   `01D702C0`/`01D702D0`, each holding the begin/end pair `0x18AE40`/`0x18AF28` (RVAs;
   `+0x120000` = `002AAE40`). That much stands.
   *Label corrected 2026-09-15 (FABLE); the conclusion is untouched and the use was always right.*
   **They are not scope tables.** Each is preceded by an `UNWIND_INFO` header carrying
   `UNW_FLAG_CHAININFO` (`flags & 4`), and for such a block a 12-byte `RUNTIME_FUNCTION` follows the
   unwind codes — here `{Begin=002AAE40, End=002AAF28, UnwindInfo=01D7026C}`. So the class is
   `_IMAGE_RUNTIME_FUNCTION_ENTRY`, **item six of the ban by name**, rather than item four. The
   distinction matters only because chained records live in `.rdata`, **below** `.pdata` — so a guard
   written as *"every `DATA` xref above the start of `.pdata` is unwind data"* does not reach them,
   which is how the same structure is still read as a dispatch table elsewhere in this database.

   **What does not stand is the conclusion drawn from it** — *"this function has no admissible
   reference of any kind — no caller [`002AAE40`], no vtable, no dispatch table … the purest example in the
   database of why a call-context classifier cannot touch these."*

   **It has one.** `00916518` in `.rdata` holds the qword `0x00000000002AAE40`, and that slot
   carries a **base relocation**, so it is a genuine absolute function pointer rather than a
   coincidental integer — tier-8 evidence, squarely admissible. Re-read from the certified program
   to confirm: `00916518` → `40 ae 2a 00 00 00 00 00`.

   **The slot is absent from the reference dump entirely.** `DumpUnresolvedIncomingDataRefContexts`
   reports the references *Ghidra holds*, and Ghidra holds none from a data slot never typed as a
   pointer. Same cause as the retracted "no strings" zero: **an instrument that can only return what
   the database was told, asked a question about the image.**

   Locality is deliberately **not** offered as evidence: the slot sits 8 bytes before the
   power-of-ten table at `00916520`, and address adjacency is banned. The independent identification
   of `002AAE40` as font drawing rests on the tier-2 `"display : draw Font"` scope-close, unchanged.

   **The rhetorical point of this entry survives with a different subject.** ~~A full re-census of all~~
   ~~158 (below) finds **156 have an admissible incoming reference**. Exactly two do not, and neither~~
   ~~is `002AAE40`:~~

   > **UPDATED 2026-09-16 (OPUS), answering `FABLE-CONTRA-OPUS-THE-NINE-PATCH-RENDERER-IS-REACHABLE`.**
   > **The count is now 158 of 158, and the entry has no exceptions left.** Both were closed by the
   > same kind of finding — a route the census did not enumerate — and both are re-verified here rather
   > than carried over:
   >
   > | body | the route that closes it |
   > |---|---|
   > | `0020AC30` | `0032FD64` → `001EC660` (a thunk) → `jmp` → `0020AC30`; a graph census loses the path at the thunk |
   > | `00392A10` | `00392A00`, a listed 12-byte guard stub, `jne` (`0F 85`) into the body; the stub has four ordinary callers |
   >
   > **FABLE's question is one short and the page is the reason:** it asks whether *157 of 158, one
   > honest exception* becomes 158 of 158. The sentence above counted **two** exceptions, and the
   > first had already been corrected in place. So the stale figure was 156, not 157, and the answer
   > is **158 of 158**.
   >
   > **What does not change:** both bodies keep their entries, their sizes and their reason for being
   > in the residual — being *reachable* is not being *classified*, and neither carries a `CodeDomain`
   > yet. The residual is 158 bodies either way.

   The two that were the exceptions:

   - ~~`0020AC30` (572 B) — no incoming evidence~~ **CORRECTED: `0020AC30` IS REACHABLE**, from
     `ActorResource_BeginManagerResourceSetLoad` through `thunk_FUN_0020ac30` (`001EC660`). A graph
     census loses the path at the thunk; a byte decode does not. It also has strong outgoing
     evidence: it references
     authored strings directly (`.json`, `spc_`, `sum_`) and one call deeper reaches
     `JsonData/CutScenes/`, `mDofFocusDistance` and a `plan_master\…\event\` regex.
   - `00392A10` (707 B) — ~~**no caller, no code reference, no data slot, and absent from the depth-1
     string result.** It is the only function in the residual with neither incoming nor outgoing
     evidence, and it has never been mentioned anywhere in this database.~~

     > **REFUTED 2026-09-16 (FABLE) — a caller exists, and it is a conditional jump.** `00392A10` is
     > entered by `00392A05` `jne 00392A10` (`0F 85 05 00 00 00`) from the **listed twelve-byte
     > function `00392A00`** — `cmp word [rcx+0x58], 0` / `jne` / `ret` — which is itself **called
     > four times by ordinary `E8` calls** (`002A62EE`, `002C0967`, `002C0E5E`, `00574056`; the
     > middle two in `UI`-owned bodies). **The censuses that reported zero searched calls, stored
     > pointers and data slots**; a `0F 8x rel32` relative branch is none of those. So this is
     > **not** the only function with neither incoming nor outgoing evidence, and the line above is
     > struck rather than rewritten so the shape of the error stays visible. The full account,
     > including what the dedicated page got right, is on
     > [the box renderer](Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md).

   **`00392A10` is the purest example this section was reaching for.** The claim was sound; the
   subject was chosen from a census that could not see the evidence it was asserting the absence of.

   **And the slot has a structure around it.** `00916518` is **index 11 of a 12-entry sparse table
   at `009164C0`** — re-read from the certified program:

   ```
   009164C0  002A9980  002A8C50  002A9F00  002A9980     idx 0-3
   009164E0  002A8C50  002AA800  00000000  00000000     idx 4-7
   00916500  00000000  00000000  00000000  002AAE40     idx 8-11
   00916520  00000001  0000000A  ...                    the power-of-ten table begins
   ```

   **Seven populated slots, five distinct targets, five NULL holes**, and three `.text` sites take
   the table address: `002ABEFD` and `002ABF4D` (both to `009164C8`) and `002B393C` (to `009164C0`).

   So `002AAE40` has a **structural identity** — entry 11 of a dispatch table shared with five named
   functions, reached from three named sites — **without any claim about what it does.** The
   power-of-ten table beginning at `00916520` is recorded as a **layout fact only**: adjacency is
   banned and is not offered as evidence of purpose, however suggestive the neighbourhood is.

   **The lead is also bounded.** Of the 158, **exactly one** has a relocation-certified `.rdata`
   pointer. The other 157 have none — a single admissible lead, not a class of them.
3. The 208-byte block consumed by `002B2DF0` — 26 quadwords is a specific, findable shape.

### Revised attack order

1. **The 13-function cluster around `002AC5F0`** — best return per read, and it contains the
   largest unclassified function in the game.
2. **`004EF860`** (219 B), the leaf shared by both twins — smallest function that would explain
   two 7,440-byte ones, and cheap.
3. **The two `+59` bytes** at `004EDB50+0x0CF2` and `+0x1AAB`.
4. **`002A0440`**, whose only two callers are both `Presentation.Rendering.ShaderMaterial` — the
   most specifically-placed of the large residual functions.
5. The 15 caller-less functions **last**: with no call context they are the hardest, and they are
   hardest for exactly the reason the classifiers failed on them.

### Method note

The unresolved set here is read from `verify/residual_addrs.txt`, never recomputed. Recomputing it
from `graph/functions.tsv` during this pass produced **133**, because the derivation treated any
`tags` value as a CodeDomain assignment — but tags such as `ContextAuditV108` and
`V102_InputCategoryParse` are audit and parse markers, **not** the third explicit layer. Only a
`GFZ.V121.CodeDomain.*` tag counts. This is the *second* time a fresh derivation of this set has
disagreed with the ledger and been the party in error (§8 records the first, a 14-minute-stale
export giving 160). **The ledger has been right both times.**

## 12. Switch-label sweep 2026-09-02 — and a same-day repeat of a fresh mistake

The `gambit-evaluation-and-enmity.md` pass found that a decompiled `switch` can be miscounted
because Ghidra prints `default:` in **source order**, sometimes mid-list. That was recorded as a new
blind-spot class, and every switch claim in the database was then swept against the binary.

**The sweep's first casualty was this document, and the claim was hours old.**

| Claim | Written | Actual labels | |
|---|---|---|---|
| `002ABF70` switches over "cases 0, 1, 2 and 4" | 2026-09-02, this session | **0, 1, 2, 3, 4, 5, 7** | wrong |
| `002A6190` "case 1 registers, case 4 updates" | same | 1, 2, 3, 4, 10, 12, 15, 18, 21 | true but partial |
| `005742D0` "case 1 and case 10" | same | 1, 3, 10, 12, 14, 15, 18 | true but partial |

**The cause was not the `default:` trap.** It was simpler and worse: the case set was read off a
**35-line excerpt** of the body, printed to keep context small, and reported as if it were the whole
switch. Cases 3, 5 and 7 were below the cut.

`0`, `1` and `4` appeared as *stacked fall-through labels* in the visible region, which made the
excerpt look like a complete listing — a switch that opens `case 2:` … `case 0:` `case 1:`
`case 4:` reads as though the author has already seen the interesting structure.

**The rule this breaks was already written, one pass earlier, and was too narrow.** The evidence
standard said *"never report a **disagreement** computed from truncated output."* That was framed
around contradicting a document. The same defect produces a **positive** claim just as easily, and
did so within the hour. The rule is widened to: **never characterise a function from a truncated
excerpt at all** — if a claim is about a whole construct, the whole construct must be in view.

**What survived the sweep.**
[`../16-UI/Request-Router/ui-request-router.md`](../16-UI/Request-Router/ui-request-router.md)
makes a switch claim about `00254B50` and handles it correctly: it enumerates the six labels it
recovered (`1`, `3`, `4`, `5`, `0xC`, `0x18`), states that the *set* is not fully enumerated, and
claims **only the bound**. Re-decompiled, the labels are exactly `1, 3, 4, 5, 12, 24` — the document
is right, and right about the limits of its own evidence. (What the sweep then *added* on the router
page — "six live request ids, not twenty-four" — was wrong in a different way: the `default` arm is
the generic scheduler, not a rejection, so the label count never bounded the vocabulary; struck on
that page 2026-09-11 with EXP-067. Counting labels correctly and reading `default` are two claims.)

That comparison is the useful part of this sweep. Two documents made a claim about the same kind of
object on the same day; the one that **stated what its evidence did not cover** is the one that
survived.

## 13. A cross-check that found nothing, and a correction that was almost published

### The residual is unreachable by every identification route opened this session

Three new bulk-identification routes came online on 2026-09-02 — the
[vtable method index](../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md) (4,275 methods
tied to one class each) and three string cross-reference families (`Phyre::`, `[sead]`, PPFX). Each
named hundreds or thousands of previously anonymous functions. **Run against the residual, all three
return nothing:**

```
residual functions appearing in a vtable, uniquely owned : 0 / 158
residual functions appearing in ANY vtable, even folded  : 0 / 158
residual functions emitting a Phyre:: accessor string    : 0 / 158
residual functions emitting a [sead] string              : 0 / 158
residual functions emitting a PPFX string                : 0 / 158
```

**This is a structural fact about the residual, not a null result.** These 158 functions contain **no
virtual method of any RTTI-bearing class** and emit **none** of the three authored string families
that named 5,000+ functions elsewhere. Whatever they are, they are neither polymorphic class methods
nor diagnostic-carrying middleware — which is consistent with, and independent of, the existing
finding that 96 % of their incoming references are banned exception metadata *(answered: see the category README, QUALIFIED 2026-09-02: the figure describes the reference dump, not the image; 2026-10-02, OPUS)*.

**It also bounds the effort saved:** the cheapest high-yield techniques available have now been tried
against this set and eliminated. The tail really is complete-body reading, one function at a time.

### The correction that was almost published

A three-way census over `Tools/work/graph/functions.tsv` — no `owner`, no `final_no_owner`, no
`CodeDomain` — returns **160**, not 158. The columns reproduce the ledger's own `owner=9409` and
`finalNo=585` exactly, and a tag census confirms `GFZ.V121.CodeDomain` on exactly **28,007**
functions against the ledger's `28,009`. Every route pointed the same way: *the ledger is over by
two.*

**It is not. The two extra are `00313A00` and `002F7380` — and this category's own README already
records both**, resolved and persistence-certified at the GN checkpoint of 2026-09-02, each given a
`CodeDomain` and a documenting category. The evidence list is even named
`GM160_CURRENT160_ADDRS.txt`: **the residual was 160, two were closed, 158 remain.**

> **`Tools/work/graph/functions.tsv` is stale with respect to those two applied GN rows.** The dump
> does not carry the two `CodeDomain` assignments the certified ledger holds. **158 is correct;
> the dump is behind by exactly the two rows this category closed.**

**The lesson is not "check the ledger" — it is that the discrepancy was already explained in the
README of the very category being audited.** Four independent measurements agreeing did not make the
conclusion right, because all four were drawn from the same stale artifact. **Agreement between
measurements that share a source is not corroboration.**

**Practical consequence for anyone re-running this:** a census over `functions.tsv` will return 160
and be wrong by construction. Use `Tools/work/verify/residual_addrs.txt` (158), or apply the two GN
rows to the dump first.

---

## Supersession notice — 2026-09-07, session `xiionline-61`

**This document is correct for the checkpoint it names, and superseded by two later ones.** Its
`verified_against` block says **GN158** (`2ed8affb…` / snapshot `46f02e26…`), and that is exactly
what it was written against. **The stamp is not being touched.**

**The residual is now 139, not 158.** GN159 classified 4 out and GN160 classified 15 more — the
Presentation text/glyph/primitive/widget batch `R55TEXT`. The nineteen that left, enumerated by
diffing the two certified residual lists:

```
001E8070 001E8580 00245170 002455A0 00245E60 002AAE40 002B8EE0 002BCB00 002DA2D0 002DA7C0
002DBDD0 002DC290 002DC7F0 00364530 003649A0 00366110 00392A10 00392CE0 0053E0B0
```

**All nineteen are in this category's own glyph / widget / nine-patch / icon cluster**, which is the
expected shape — they are the functions the `99-Unresolved-Residual/` documents read and described
well enough for the ledger to classify them. **This document's census, cluster analysis and page
spread are therefore historical figures**, true of GN158, and any count in it (`158`, `37 pages`,
`14 clusters plus 109 singletons`, `n = 158 min 310 B median 828 B max 7,489 B`) must be read with
that date attached.

**What is *not* superseded:** every structural finding about the functions themselves. The binary did
not change — the embedded authorized EXE is `73461d08…` at both checkpoints — so what these functions
*do* is unaffected. Only their ownership status moved.

A successor census against GN160's 139 has **not** been run here. Until it is, cite this document for
mechanism and cite the current ledger for counts.

**A third checkpoint, 2026-09-15 (OPUS): the residual is now 30, not 139.** GN161 is GN160 plus
batch R109 — the 109 unopened rows of `residual-109-classification.tsv`, body-read and classified
by SWE2-FRONTIER with an AUDIT-SEM accept-with-narrowing pass. **Verified here from the artefacts
rather than from the checkpoint's own prose**: the batch file's entry column holds exactly **109**
distinct addresses, the current residual list holds **30**, the two sets are **disjoint**, and their
union is **exactly 139** — GN160's declared figure. All 109 resolve in `functions.tsv` and all 109
are classified there now. Every one of GN161's six ledger figures reproduces from `functions.tsv`
independently: internal 38,161, owner 9,409, finalNo 585, codeDomain 28,137, explicit 38,131,
unresolved 30. **`internal`, `owner` and `finalNo` are unchanged from GN160**, which is what makes
the delta additive rather than a reclassification.

*Found because a checker missed it.* `Tools/work/OPUS/check_stale_absence_after_gn161.py` looks for
absence language on lines that cite one of the 109, and found **no stale claim about any of them** —
the fleet had already propagated GN161 into every page that names one. It could not find this
sentence, because **a count claim cites no address at all**. The check is worth keeping and its
blind spot is worth stating: it protects functions, not figures.

**And what kind of work the 30 are, which that checkpoint did not say: all thirty are DESCRIBED.**
[`residual-30-GN161.tsv`](residual-30-GN161.tsv)'s `band` column classifies each row by the rule in
§2 — `DESCRIBED` (a passage says what it does and none refuses), `CONTESTED` (described somewhere and
refused somewhere), `UNREAD` (nothing says what it does). The split is **30 DESCRIBED, 0 CONTESTED,
0 UNREAD**, across 38,478 bytes.

> **So the remaining distance to `unresolved = 0` contains no research.** That file's own header
> already states the consequence — *"a DESCRIBED row needs tagging in the GZF and re-certification,
> not documentation"* (EVIDENCE-STANDARD addendum 2026-09-13t) — and the band column now says it
> applies to **every** remaining row, not most of them. The database side of this metric is done;
> what is left is a checkpoint operation.

**§6's closure order is written for the 158 and should not be read as advice for these 30.** It tells
a future pass to read the 7,440-byte twins, read the largest body first, and *"expect no cheap wins
… each will likely need a body read"*. That was true of the population it was written for. It is not
true of the 30: they are described already, and a body read would re-derive what a passage on some
page already says.

*Verified 2026-09-15 (OPUS), and the census is CURRENT rather than assumed current:* the 30 addresses
in `residual-30-GN161.tsv` and the 30 in the certified `residual_addrs.txt` are the **same set** — no
row in one and absent from the other, in either direction — and every row's `size` matches
`functions.tsv` exactly, 0 disagreements. `progress.py` also raises **none** of its provenance
warnings against this pair: the residual file lists 30, the certified header says `unresolved=30`,
and not one of the 30 is already tagged in the dump, which is the state that would silently inflate
the figure.

## 11. Reopened 2026-09-08 — the worklist has shrunk by 21 and the frontier has not moved

Three snapshots of this population survive. They are **strictly nested**, verified as sets:

| file | entries | written | tracked? |
|---|---:|---|---|
| `Tools/evidence/GM160_CURRENT160_ADDRS.txt` | **160** | 2026-09-02 00:06 | **yes, as of 2026-09-08** |
| `Tools/work/verify/residual_addrs.txt.GN158` | 158 | 2026-09-02 20:47 | no — gitignored |
| `Tools/work/verify/residual_addrs.txt` | **139** | 2026-09-03 19:44 | no — gitignored |

`139 ⊂ 158 ⊂ 160`, with no element outside the chain. **The 158 this document is named for was
the middle snapshot**, and §8's reconciliation of 158-against-160 as *“two program states 14
minutes apart”* survives intact — it just now has a third state a day later.

### The undocumented remainder is the same set in all three

Crossing each list against every address any database document cites:

```
uncited(160) == uncited(158) == uncited(139)        112 functions, the SAME 112
```

Not the same count — **the same set**. So the entire `160 → 139` shrink came from functions the
database had already written about: **all 21 that left are cited**, and they are one
recognisable cluster.

| left the worklist | B | where it was already documented |
|---|---:|---|
| `001E8580` | 3,572 | [painting a line of text into a render target](Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md) |
| `003649A0` | 3,020 | [how a line of text becomes glyph quads](Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md) |
| `002B8EE0` | 2,865 | [drawing one coloured rectangle](drawing-one-coloured-rectangle.md), [the blinking icon](the-blinking-icon-and-its-atlas.md) |
| `002BCB00` | 2,703 | the same two, plus [the second icon drawer](the-second-icon-drawer-and-what-it-adds.md) |
| `002AAE40` | 2,440 | [measuring text by drawing it with the output off](measuring-text-by-drawing-it-with-the-output-off.md) |
| `00313A00` | 289 | [the largest unclassified functions](Largest-Unclassified-Code/the-largest-unclassified-functions.md) |
| *15 more* | 589–2,232 | all cited, all in the same glyph-run / icon / rectangle neighbourhood |

> **Documentation led classification, and the residual count followed it.** This document's §6
> *“How to close this category”* said to expect no cheap wins from mechanical classifiers. The
> measurement is stronger than that: over three classification passes, **a mechanical classifier
> resolved nothing this database had not already read.**
>
> The corollary is the useful half. **The 112 will not shrink on their own.** They survived all
> three passes untouched and nothing about them will change until somebody reads one.

### What the 112 are

All authored: **none generated, none an EH funclet, and all 112 with no owner** when surveyed —
`00565E00` has since been classified at GN162 as `UI.Widget.OnceRegisteredCommandBandProcedure`.
Largest first:
`0028BB50` 2,387 B · `00565E00` 1,914 B · `00275570` 1,835 B · `0020F3E0` 1,779 B ·
`003BED70` 1,720 B · `0028AAA0` 1,692 B. **`DT-1`.**

### What this section does not claim

- **That the classifier could not have resolved the 112.** It says only that across three
  passes it did not. No classifier configuration was compared, and no counterfactual was run.
- **That “cited” means “understood”.** A function is cited when any document names its address.
  §3's *“eight of 158 have been read”* is the honest reading count and is unchanged by this
  section.
- **That 160 is the true original size.** It is the largest surviving snapshot. Whether an
  earlier and larger one existed is not established — `work/` keeps no history.

## 14. Cross-reference 2026-09-13 (FABLE) — 50 of the 139 are now cited elsewhere, 22 inside their bodies

> **Restated 2026-09-13 after SWE2-AUDIT-SEM's review (AUDITSEM-CONTRA-FABLE-RESIDUAL-XREF).** The figures below are a
> snapshot; re-run the script rather than quote them. At commit time the regenerated TSV says **55 of 139 cited, 23
> interior, 84 uncited**. Three changes produce that. The menu effect registry page cites `00572920` / `005734C0` /
> `00573690` (+3). The lmap page §10 cites `003BDDE0` / `003BDFF0` / `003C1A20` (+3). This folder's `README.md` is now
> excluded as the ledger's own index (−1, `00402000`, whose only citation there is the dump audit's bitmask note). The
> auditor's genuine extra cite, `0023F06E` inside `0023EFC0`, is in that README, so the exclusion covers it too.
> **Citation-form limit:** the script reads only backticked bare 8-hex addresses. `0x`-prefixed, unbackticked, `FUN_`-style
> and name-only citations are not measured. The auditor's broad sweep found two false positives in those forms (a
> range bound, a rip displacement), so widening the regex is not a free improvement.

The residual is 139 today (`Tools/work/verify/residual_addrs.txt`), not 158. `residual_crossref.py` (beside this page) finds
every citation of a residual function on any page outside this one and the unowned-code census, and writes
`residual-crossref.tsv` with one row per function:
- ~~**50 of 139**~~ **55 of 139** (restated) are cited by at least one other page;
- ~~**22**~~ **23** have a citation strictly inside the body — the measure `check_dispositions.py` uses for an individual explanation;
- the other ~~28~~ 32 are entry-only mentions.

Identities established after this page was written, by page:
- **The AC-7 twins `004EDB50` / `004F5360` and `002F0280` belong to the PS2 VIF1 / VU1 layer.** `002F0280` is a
  VU1 microprogram installed by an MPG packet. The twins work on VU state (VU memory `02064E30`) and their 219-byte leaf
  `004EF860` hands a pointer into VU memory to the GS callback
  ([the VIF1 / VU1 layer](../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md)). That answers AC-7's
  record identity; the XGKICK equivalence is still open.
- **`0020F3E0` is the GS translator's PACKED-register dispatcher** (20 GS registers honoured, 60 ignored), and **`0020ED30`
  selects draw state for its batch flush** (same page, §2.1b).
- **`0024B9B0`** is one of the callers of the transform-matrix writer `0024C060`
  ([the two transform primitives](../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md)).

The frontier ledger `coverage.tsv` is a frozen export, so these citations do not change the `ledger_resolved` figure until
that ledger is regenerated. What they change is the worklist: the ~~89~~ 84 residual functions no page cites are the real AC-1
backlog. ~~They are listed in the TSV with an empty `pages` column.~~ *(answered: see the member TSV now holds the 30 of GN161, each `interior_cited=yes` and none with an empty `pages` column; 2026-10-02, OPUS)*

## Interior citations — entry-only-large pass (2026-09-14, SWE2-FRONTIER)

This page named the following bodies only at their entries. Each interior address below was read
in the shipping image and is cited so the entry is no longer the page's only anchor into the body.
The notes describe what the instruction does; they are not yet claims of each body's full role.

| body | interior cite | what is there |
|---|---|---|
| `002A0440` | `002A060E` | `movups [022D8F30], xmm2` then `xmm0`/`xmm1`/`xmm0` — a 64-byte record copy from `[r13]`/`[+0x10]`/`[+0x20]`/`[+0x30]` into `022D8F30`–`022D8F6F`, not a zeroing |
| `0028BB50` | `0028BE4E` | `call 0028CF80`, the fourth of five distinct leaf calls after three `00203170`/`002754E0` pairs |
| `002455A0` | `002455E4` | `mov rax, qword ptr [rip+…]` — loads the pointer cached at `0208EA98` before the `002DAxxx` call chain |
| `002A6190` | `002A6464` | `mov dword ptr [rip+…], …` — writes `01E0CDC8`/`01E0CDCC`, the state dwords the case-4 message arm drives |
| `00565E00` | `00565F65` | `mov eax, dword ptr [rip+…]` — reads `01E0C3B0` mid-loop; body alternates `002CD3C0`/`00252D10` call pairs |
| `00275570` | `00275BDB` | `call 00202B10` inside a `shl rcx,4` loop indexing a 16-byte record bank at `[rbp+0x410]` |
| `0020F3E0` | `0020F49A` | `mov byte ptr [rip+…], 1` — sets `01FC3603` in the pending-batch flush arm of the GS dispatcher |
| `003BED70` | `003BEE16` | `call 003BF430` — the nibble-keyed entry fetch inside the two-phase `02B457E0` block scanner |
| `002A4830` | `002A4B18` | `movss dword ptr [rip+…], …` — writes `0209C634`; four calls to `0017F880` bracket it |
| `0028AAA0` | `0028ABB8` | `call sinf` between `00273880` and `003F0040` — a transform/easing path, not a leaf |
| `0024B9B0` | `0024BBE4` | `call 0024C060` — the transform-matrix writer this page already documents |
| `00245E60` | `002460A4` | `movss dword ptr [rip+…], …` — writes `0208ED00`/`0208ED04`, a float pair set after the `00398xxx` calls |
| `0020ED30` | `0020EDAE` | `cmove rbx, qword ptr [rip+…]` — conditional pick between the `01FC3588`/`01FC3590` state blocks |
| `002AE610` | `002AE7DC` | `movss xmm8, dword ptr [rip+…]` — reads `0209CC68`, the glyph pen-advance global the char-loop page documents |
| `005742D0` | `00574427` | `call RuntimePointer_EncodeImageAddress` inside the construction arm of this message handler |

**Movement-layer adjacency, accounted.** Three cited members reach or are reached by Movement:
`00202B10` and `00203170` are the shared workbench vector helpers whose `0033xxxx` locomotion-family
callers are documented on [the two transform primitives](../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md)
(16 and 19 Movement callers respectively); `00258350` — the CAM7 path-follow member — calls
`00230B60`, and `002F7380` is called by `0026E290`, both Movement-layer bodies. Residual census
membership is about ownership, not adjacency; these edges say the unresolved set is used by
locomotion code, not that Movement owns them.

## `0024B580` read — the one residual whose entry nothing names (2026-09-14, OPUS; classified at GN162 as `Runtime.DeferredQueue.KindDispatchDrain`)

**It is a deferred-work queue drain.** Read from the shipping executable at the authority hash,
image base `0x120000`; every address below is decoded from the bytes, and the jump table is decoded
rather than inferred.

### The queue, and a second reading that agrees

`0024B586` loads `[02092170]` into `rbx` and `0024B58D` immediately **stores 0 back into it** — the
whole pending list is detached in two instructions before anything is walked. The walk advances
through `node + 0x348`, loaded at the top of each iteration (`0024B5C3`) and moved into `rbx` at
the bottom (`0024B6A3`), so `+0x348` is the next link.

**`02092170` has exactly nine references across four functions**, and the shape corroborates the
reading from a direction that does not depend on it:

| function | sites | shape |
|---|---|---|
| `0024B1F0` | read `0024B1F5`, write `0024B218`, write `0024B22E` | read-then-write — a push |
| **`0024B580`** | read `0024B586`, write `0024B58D`, write `0024B60B` | **detach, and one arm re-queues** |
| `0024C3C0` | read `0024C423`, write `0024C44D` | read-then-write |
| `0024C970` | write `0024CAC0` | write only |

### The dispatch is nine arms and five destinations, decoded from the table

`0024B5C0` reads a **kind byte at `node + 0x00`**, decrements it, and refuses anything above 8
(`cmp eax, 8` / `ja`). `rsi` is the image base — `lea rsi, [rip - 0x12b5ad]` at `0024B5A6` resolves
to `00120000` — so `mov ecx, [rsi + rax*4 + 0x12b6c4]` indexes a table at **`0024B6C4`**, the four
bytes after this function's `ret`, and `add rcx, rsi` turns each entry into an address.

| byte at `+0x00` | target | what the arm does |
|---:|---|---|
| 1 | `0024B5E9` | `002FC010(node)`; **if it returns 0, re-queue** — zero `+0x348` and `+0x350`, store `node` back into `[02092170]`, and skip the tail entirely |
| 2, 3, 8 | `0024B629` | straight to the common tail, no per-kind call |
| 4 | `0024B621` | `003B2930(node)` |
| 5, 6, 9 | `0024B5DF` | `003B0220(node)` |
| 7 | `0024B617` | `003B15C0(node)` |
| 0, or above 9 | *(the `ja`)* | falls into the tail |

**Kind 1 is the only arm that can put a node back**, and it is conditional on `002FC010`.

### The common tail publishes three sub-objects and appends to a bounded array

    02F97348 = node
    02EBEF98 = node + 0x120   then call 003A81E0
    02EBEFB0 = node + 0x130   then call 003A72E0
    02EBEF88 = node + 0x1B8   then call 003A8D70      <- 0024B65D
    if node + 0x380 is non-null:
        count = u16 [0209216A]
        if count >= 0x100 -> call 00182CA0            <- the bound is 256, not a wrap
        else               -> [02091950 + count*8] = that pointer;  ++[0209216A]
    call 003697F0(node)

`0024B65D` is the `02EBEF88` store, and it is **the single instruction any page in this corpus
cites** — [the effect-element type dispatch](../17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md)
§ lists it among eleven writers of that global. That page names an instruction; it does not name
this function.

### What this does NOT establish

**Structure, not meaning.** What the nine kinds *are*, what the three published sub-objects are
for, what `002FC010`'s return value means, and what any of `003B0220` / `003B15C0` / `003B2930` /
`003A81E0` / `003A72E0` / `003A8D70` / `003697F0` / `00182CA0` do are **not read here and are not
claimed**. The names `queue`, `drain`, `push` and `publish` above describe the instruction shapes —
a head detached and restored, a list walked by a link field, a bounded array appended to — and not
an authored purpose.

**And a reading is not a classification.** `0024B580` is residual because it carries no
`GFZ.V121.CodeDomain` tag, and prose does not give a function one. `unresolved` is unmoved by this
section. What it removes is the reason `OPUS-REQ-SWE2-EC7-RESIDUAL-BODY-READ-30` singled this
address out: it was the one with no page to start from, and it now has this. (*Closed at GN162*:
the body now carries `GFZ.V121.CodeDomain.Runtime.DeferredQueue.KindDispatchDrain` — the tag this
paragraph said prose could not confer.)

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — SERVICE.** Cited functions call small core helpers (27 and 7 bytes twice each, and 40 and 93 bytes).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — CLIENT.** `FUN_00313db0`, owned by that layer, calls `00313A00` on this page. That caller is a 360-byte drain of a **64-entry ring at `022BEDA4`** - head `byte[022BEDA0]`, tail `byte[022BEDA1]`, both wrapping with `& 0x3F` - which resolves each queued handle, clears bit 12 and sets bit 13 of its `qword[+0]`, and then tests the `+0x3C`/`+0x64` pair; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — SERVICE.** `00313DB0` on this page calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15`, owned by that layer. What it reaches is a 105-byte ladder over one flags word - `dword[[02EBF190] + 0x5B04]` - where bit 3 answers **5**, bit 2 answers **4**, the shared permission bit answers **3**, and the rest fall through in order; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — CLIENT (2 edges, one fan-in).** All 2 edges are Resource bodies reaching `0024C970` on this page. `FUN_0024f240` is the worked example - it is a 384-byte load in an `0x88`-byte frame with a stack cookie: it opens a file and does nothing at all when the open fails. The crossing is **one shared subject with 2 callers on that layer**, not 2 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

## What a citation has to say before it can carry a CodeDomain — OPUS ruling, 2026-09-15

`OPUS-REQ-SWE2-EC7-RESIDUAL-BODY-READ-30` asks, of each remaining residual, *"does the prose that
already cites its interior establish a CodeDomain, or is the citation shallower than it looks?"* That
is a reading question, so it needs a rule before it needs thirty readings.

**The first rule I tried was wrong and is worth recording.** I measured which folders cite each of
the thirty, reasoning that a function documented inside exactly one layer's folder has an owner the
corpus already asserts. Sixteen came back single-folder. Three worked cases killed it:

| function | folders | what the prose actually says | establishes it? |
|---|---|---|---|
| `002ABF70` | 16-UI only | the page carries a section headed **"`002ABF70` opened"**: 122 instructions, ends `ret` at `002AC1B0`, no `jmp` leaves the extent, an **eight-mode jump table** on the low byte of `dword[rcx+0xB0]` with the table in `.text` after the `ret` | **yes** |
| `0036A2A0` | 24-Compiler-And-CRT-Runtime only | *"whether `0036A2A0` … produces blocks that carry this header is **not traced**"* | **no** — the page names it precisely to say it did not follow it |
| `00402000` | 12-Items… only, one document, one line | *"`00402000(rows, mapDesc)` builds the array both readers walk"* | **yes** — a prototype and a position in a named pipeline |

One folder and one line settles `00402000`; one folder and a whole page leaves `0036A2A0` open. **The
test is the sentence, not the shelf.**

### The rule

A citation establishes a CodeDomain when it **says what the function does** — a prototype, a verb
about named state, or a position in a named pipeline. It does not when it only **names** the
function, and it explicitly does not when the prose records that the function was not followed.
Citations inside a page's pass-22 crossing section never establish ownership at all: those name the
**far end** of an edge, which is the same population R6 excludes from being a subject.

### The triage, and its error rate

`Tools/work/OPUS/residual_citation_depth.py` bands every citing line ROLE / DISCLAIMED / BARE and
reports **22 of the 30 classifiable from what exists, 8 needing the body read**. That list is a
worklist, not a verdict, and the two cases above are exactly why:

- **False negative.** `002ABF70` lands in "needs the body read" because the line carrying its address
  says *"at its entry only"* — a `DISCLAIMED` phrase that the page uses to describe the state it was
  in **before** the section that opens it. The function is fully read on that page. **Move it to
  classifiable.**
- **False positive.** `0036A2A0` lands in classifiable on one `ROLE` line that is a list of addresses
  with their interiors, while the page's own sentence about it says *"not traced"*. **Move it to
  needs-read.**

So the honest split is **22 classifiable and 8 to read**, with one swapped in each direction and the
tool's failure mode known: it bands lines, and a page's claim about a function is not always on the
line that carries its address.

### The eight that need a reading

`001D72F0`, `001D7A20`, `0020F3E0`, `0024B580`, `002BA310`, `002C3D70`, `00566680`, and `0036A2A0`
by the correction above. `0024B580` is the hardest of them: it is cited by **no document outside this
folder and the indexes at all**, so there is no prose to lean on in either direction.

*(Ruling by OPUS 2026-09-15 for SWE2-EC7. The classification itself remains theirs; this settles what
the evidence has to look like, not what any particular answer is.)*

### Correction to the triage above: 29 of the 30, not 22 — and the rule did not change (OPUS, 2026-09-14)

The ruling above stands. **Its worklist does not.** It reported *"22 of the 30 classifiable from what
exists, 8 needing the body read"*, and named the tool's failure mode in the same breath — *"it bands
lines, and a page's claim about a function is not always on the line that carries its address"*. That
correction was applied to two cases. Applied to all eight, **seven of them are described already.**

| | old triage | re-tested |
|---|---:|---:|
| described — a passage says what it does | 22 | **29** |
| contested — described somewhere, refused somewhere | — | **1** |
| **needs the body read** | **8** | **0** |

### Four defects, one per miss, each with the passage that exposed it

1. **The residual folder was skipped entirely.** `Tools/work/OPUS/residual_citation_depth.py` drops
   any path whose top segment is `99-Unresolved-Residual` — *this folder*, where residual bodies are
   written up. `0024B580` therefore came back with **zero citing lines**, not BARE but absent, while
   the section four headings above this one opens with **"It is a deferred-work queue drain."** The
   exclusion was meant to stop the survey pages counting as owners; it also hid the only readings.
2. **The role vocabulary was verbs only.** The corpus states a role as a **noun phrase** at least as
   often, in table cells and headings where a verb would be redundant: *"the item-sort bar"*
   (`00566680`), *"child-widget create+attach"* (`002BA310`), *"round-robin channel picker"*
   (`002C3D70`). None contains a listed verb. All three say exactly what the function is.
3. **`handles` was not in the list.** `0020F3E0` is cited as *"`0020F3E0` handles one PACKED GIF
   packet. For each register slot:"* — as plain a role sentence as this database contains.
4. **Prose hard-wraps and the tool bands lines.** `001D72F0` and `001D7A20` are named at the end of
   one line and described at the start of the next: *"...the two render passes `001D72F0` (from the
   render pass list `00187950` through `001D7280`) and `001D7A20` (from the slot-4 pump through
   `001D8AB0`) / **return at once while it is set**"*.

### And the replacement's own two failures, found before its number was quoted

Widening from one line to five immediately manufactured the opposite error, twice:

- **`002C3D70` came back classifiable on the worklist itself** — the line listing all eight addresses,
  with role words from the surrounding sentences dragged in by the window. A line enumerating three or
  more residual addresses is a **list**; it describes none of them, and is now excluded.
- **`002C3D70` then came back as REFUSED**, because the table row above its own in
  [`the-two-transform-primitives.md`](../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md)
  ends *"Track variant, not read deeper"* — about a different function. **A table row is
  self-contained and the window must not cross it.** Widening context is right for wrapped prose and
  meaningless in a table.

### The control

The ruling above was the old tool **plus two hand corrections, one in each direction**: `002ABF70`
moved in, `0036A2A0` moved out. `check_residual_depth.py` reports 29 described and **`0036A2A0`
alone as contested** — it **reproduces both hand corrections unaided**, from the passages, with
neither address special-cased. A rewrite that empties the expensive queue is worth distrusting on its
own; one that also lands on the single judgement a person had to make by hand can be checked.

### What this changes for `unresolved = 0`

The expensive queue is **empty**. Every one of the 30 except `0036A2A0` has a passage naming what it
does, so the whole remaining cost of the gate's first precondition is **checkpoint work — tagging in
the GZF and re-certifying — not reading**. That is exactly what addendum 2026-09-13t said the number
meant, and the worklist had drifted back to reading anyway.

`0036A2A0` is contested rather than unread: the allocator page names it precisely to say *"whether
`0036A2A0` … produces blocks that carry this header is **not traced**"*. One body.

*(OPUS, 2026-09-14, correcting the OPUS ruling above. The rule is unchanged — only its application.
The heading above carries `2026-09-15`, a day that had not happened when it was written; see
EVIDENCE-STANDARD addendum bn. It is left as written because it is a section identifier.)*

## AC-5 / UQ-379 — the counterfactual this document said had not been run (OPUS, 2026-09-14)

§*"Fifteen have no caller at all"* offers **"the single best answer available to `AC-5`"**: a
classifier reasoning from call context has none to reason from. The same document then says plainly
what it did not do — *"No classifier configuration was compared, and **no counterfactual was
run**."* Fifteen of 158 is 9.5 %, so that answer covered a tenth of the question.

**The counterfactual is run here, and it refutes the standing answer for the thirty that survive.**

### The method, and the control that makes it mean anything

A mechanical classifier has few inputs: a real symbol, an owner record, incoming call context,
outgoing calls into already-classified bodies, thunk shape, size. Each is measured on the residual
and on the classified population from `graph/functions.tsv` and `edges.tsv`.

**Compared against ALL 28,137 classified bodies the residual looks obviously different — and that
comparison is worthless.** The classified population has a **median body of 60 bytes**; it is
dominated by ~11,800 generic shape classes and 3,887 EH funclets. A 937-byte function calls more
things than a 60-byte one for reasons that have nothing to do with classification. So the cohort is
**every classified body in the residual's own size band, 324–7,489 B — 2,858 of them.**

| signal | residual (30) | same-size classified (2,858) | all classified (28,137) |
|---|---:|---:|---:|
| a real symbol, not `FUN_xxxxxxxx` | **0.0 %** | **0.7 %** | 16.8 % |
| at least one INCOMING call edge | 80.0 % | **83.4 %** | 47.3 % |
| at least one OUTGOING call edge | 100.0 % | 89.7 % | 80.2 % |
| **5 or more outgoing call edges** | **86.7 %** | **51.2 %** | 10.0 % |
| a thunk | 0.0 % | 0.0 % | 2.9 % |
| median body | 937 B | 597 B | 60 B |

### Both candidate causes fail

- **It is not the missing symbol.** Every residual is `FUN_xxxxxxxx` by construction — and so were
  **2,838 of the 2,858** same-size bodies that the classifier tagged anyway. The name is not what
  separated them.
- **It is not missing call context.** Incoming edges: **80.0 % against 83.4 %** — the same. Outgoing:
  the residual has **more**. Matched one at a time, within ±20 % of each body's own size,
  **22 of the 30 have more outgoing call edges than the median classified body of their size**, and
  every one of the thirty sits in a cohort of 28 to 1,812 same-size peers that were classified.

### The positive control, because this is a negative result

The same measurement **does** separate the residual from the classified population as a whole —
symbol 0.0 % against 16.8 %, callers 80 % against 47 %. **The instrument detects a difference when
one exists.** Against the size-matched cohort it detects none, and where it detects one at all it
points the wrong way: the residual is *better* connected than the bodies that were classified.

### What that leaves, said without inventing a cause

**No signal available in the call graph separates a residual body from a classified body of its own
size.** The failure is therefore not explained by anything this repository holds; it is a property
of the classifier's own decision rule, which lives in the GFZ pipeline and not here. That is the
answer — a bounded negative, not a shrug — and it supersedes the fifteen-no-callers explanation,
which remains true of those fifteen and false as an account of the class.

**The practical half.** §*"How to close this category"* said to expect no cheap wins from mechanical
classifiers, and §*"the 112 will not shrink on their own"* said they survived three passes untouched.
**Both stand, and this strengthens them**: the bodies are not deficient in classifier inputs, so a
fourth pass with the same inputs has no reason to behave differently. What moves them is the tagging
pass on the ~~29~~ 30 DESCRIBED bodies *(corrected 2026-10-02, OPUS: the member TSV's `band` column reads `DESCRIBED` on all 30 rows, `0036A2A0` included — the split stated in §"what kind of work the 30 are")* in
[`residual-30-GN161.tsv`](residual-30-GN161.tsv), which uses prose rather than signals.

*(Measured by OPUS 2026-09-14 over `graph/functions.tsv` and `edges.tsv` at the current generation,
so the finding is about the **30 that survive**, not the historical 158. The fifteen-no-callers
figure was about the 158 and is not contradicted for those fifteen.)*


## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

Every citation on this page is a census entry of unresolved or unowned code, so each layer below arrives with those bodies' ordinary call graphs. None of them is a claim this page makes.

**The weight of the neighbourhood is a pointer, not a classification.** 351 of the 374 edges are Presentation (224) or UI (127). The shared leaves `00203170`, `00181560`, `00181330` and `00181890` alone serve dozens of render and menu bodies, so the residue sits mostly in the render and menu paths (tier 2, from callers only).

**ActorEntity — MECHANICAL, 3 edges.** `00203170` is called by `003F1E90`; `0028BB50` calls `002713E0`; `002FC010` calls `ActorTimeline_DispatchEventToBattleUnit` (`002EB740`).

**Audio — MECHANICAL, 3 edges.** `00187950` calls `00182E80`; `001E8070` calls `00225690`; `00241D40` calls `00249CA0`.

**Input — MECHANICAL, 11 edges.** `00368360` calls `001E0A10`, `001E0E30`, `001E0E50`; `00254B50` is called by `InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`), `002E09A0`; `InputGameplay_GetActorStateAwareRemappedMask04` (`002A28E0`) calls `InputGameplay_GetRemappedHistoryMask04` (`0036FF70`); `InputGameplay_GetActorStateAwareRemappedMask08` (`002A2940`) calls `InputGameplay_GetRemappedHistoryMask08` (`0036FFC0`); `InputGameplay_GetActorStateAwareRemappedMask0C` (`002A29A0`) calls `InputGameplay_GetRemappedHistoryMask0C` (`0036FFD0`); `InputGameplay_GetActorStateAwareRemappedMask10` (`002A2A00`) calls `InputGameplay_GetRemappedHistoryMask10` (`0036FFE0`); `002A38C0` is called by `002E09A0`; `002A9980` calls `001E0A10`.

**Presentation — MECHANICAL, 224 edges.** `00203170` is called by `00245E60`, `00258350`, `002B7B80`, `002DB080` and 26 more; `00181560` is called by `0022FFE0`, `00274CB0`, `0028D980`, `002AFDC0` and 21 more; `00181330` is called by `00274CB0`, `002AFDC0`, `002DB080`, `002DBDD0` and 16 more; `00181890` is called by `0022FFE0`, `00274CB0`, `0028D980`, `002D9DB0` and 16 more; `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`) is called by `0024A710`, `002B0280`, `002DB080`, `002DC290` and 12 more; `0024B9B0` calls `003A7050`, `003A7300`, `003A74F0`, `003A7EE0` and 1 more; `00182CA0` is called by `0024F4D0`, `002512B0`, `002D81D0`, `003AAA50`; `00202B10` is called by `Skeleton_ComposeFinalPose` (`00373860`), `003C81B0`, `003F0610`, `003F6370`; `00258350` calls `00256960`, `00256CA0`, `003CC000`, `003CC970`; `003F0040` is called by `0028D460`, `003FAB60`, `003FB3E0`, `003FBA80`; `001D7A20` calls `001B03D0`, `001B06D0`, `001D8790`; `00245E60` calls `00245170`, `002455A0`, `00245E60`; `002D8D10` is called by `002D2DB0`, `003C29A0`, `00405C20`; `002DA7C0` is called by `00245170`, `002455A0`, `002D6990`; `002F7380` calls `00467AA0`, `00467B00`, `00467B10`; `003649A0` calls `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`), `RenderCommand_FinalizeSubpacket` (`003A2020`), `RenderCommand_BeginSubpacket` (`003A2090`); `0017F880` is called by `002AAE40`, `002B0280`; `00187950` calls `00187550`, `0018B100`; `001D7280` calls `001D72F0`, `001D7DD0`; `001D72F0` calls `001B03D0`, `001B06D0`; `001D8AB0` calls `001D7A20`, `001D8700`; `00230B60` is called by `00258350`, `003CC970`; `00241D40` calls `002DBDD0`, `002DC290`; `002455A0` calls `002DA2D0`, `002DA7C0`; `0028AAA0` calls `003F0040`, `003F1290`; `002A0440` is called by `0029E840`, `0029ED50`; `002B2150` is called by `002AAE40`, `002B0280`; `002B8EE0` calls `002DBDD0`, `00403BC0`; `002BCB00` calls `002DBDD0`, `00403BC0`; `002DBDD0` is called by `002B8EE0`, `002BCB00`; `00392A10` calls `002DC7F0`, `00392CE0`; `003A81E0` is called by `0024F4D0`, `003A74F0`; `003BED70` is called by `002B7B80`, `002BAF80`; `004EF860` is called by `004EDB50`, `004F5360`; `00181330` calls `001B03D0`; `001D7280` is called by `00187950`; `0020AC30` calls `001C5750`; `00245170` calls `002DA7C0`; `00245170` is called by `00245E60`; `002455A0` is called by `00245E60`; `00245E60` is called by `00245E60`; `0024C060` calls `0057A1F0`; `00256960` is called by `00258350`; `00256CA0` is called by `00258350`; `0026E290` calls `002F7380`; `002754E0` is called by `005621A0`; `002A86A0` calls `002B0280`; `002A9F00` is called by `002B0280`; `002AC5F0` calls `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`); `002AC5F0` is called by `002AAE40`; `002AE610` is called by `002B0280`; `002AF960` calls `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`); `xmlStrchr` (`002B39A0`) is called by `00578450`; `002BA310` is called by `002BAF80`; `002D8D10` calls `002DB080`; `002DA2D0` is called by `002455A0`; `002DC290` calls `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`); `002DC290` is called by `00392CE0`; `002DC7F0` is called by `00392A10`; `002FC010` calls `0024F410`; `0035D480` is called by `0028D460`; `00364530` calls `00366110`; `003649A0` is called by `0053E0B0`; `00366110` is called by `00364530`; `00392CE0` calls `002DC290`; `00392CE0` is called by `00392A10`; `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`) calls `GraphicsCommand_PublishCompletedBatchState100` (`0036F360`); `003B15C0` calls `0024F410`; `0053E0B0` calls `003649A0`; `00572920` calls `003B2D80`; `005734C0` calls `003B2D80`; `00573690` calls `003B2D80`.

**Script_VM_Native_Bridge — MECHANICAL, 1 edge.** `00203170` is called by `00356160`.

**StoryEvent — MECHANICAL, 1 edge.** `0020AC30` calls `0020A800`.

**UI — MECHANICAL, 127 edges.** `00281ED0` calls `0028E790`, `00291D70`, `00291D80`, `002C2280` and 4 more; `00203170` is called by `00247AE0`, `002D2600`, `002D28E0`, `00368010` and 3 more; `00254B50` calls `00280A00`, `0028F970`, `0035D080`, `0035D660` and 3 more; `00368360` is called by `0029A0A0`, `002A4430`, `002C3560`, `002C4460` and 2 more; `0017F880` is called by `002A4830`, `002AC5F0`, `002AE610`, `002AF960`; `00202B10` is called by `002C7B10`, `002C84E0`, `003FC170`, `005512B0`; `002CD3C0` is called by `00281AE0`, `002C2320`, `002D70F0`, `00565E00`; `003F0040` is called by `0028AAA0`, `0028B140`, `002C7B10`, `002C84E0`; `00181890` is called by `002A0440`, `002D8D40`, `002D9380`; `00252D10` is called by `002C4720`, `00564780`, `00565E00`; `00273880` is called by `0028AAA0`, `002BF0E0`, `002BFD20`; `002A8C50` calls `002ABF70`, `002AC5F0`, `002B2150`; `002B2150` is called by `002AC5F0`, `002AF340`, `002AF960`; `00565E00` calls `002814E0`, `00291D80`, `002C9BF0`; `00244070` is called by `002A4430`, `002A86A0`; `002A2720` is called by `0035D0E0`, `0035D280`; `002A6190` calls `002A4430`, `002A4830`; `002A9F00` is called by `002AC5F0`, `002AE610`; `002AAE40` calls `002AC5F0`, `002B2150`; `002AC5F0` calls `002AE610`, `002B2150`; `002AC5F0` is called by `002AF340`, `002B2150`; `002AF340` calls `002AC5F0`, `002B2150`; `002AF960` is called by `002A4430`, `002A4830`; `00392A00` is called by `002C0870`, `002C0BE0`; `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`) is called by `002AC5F0`, `002AF960`; `00566680` calls `00291D70`, `00291D80`; `00181330` is called by `002A0440`; `00181560` is called by `002A0440`; `00245E60` calls `002435C0`; `0024C060` is called by `0024B9B0`; `00254B50` is called by `00254B40`; `00273880` calls `0035BB20`; `002754E0` is called by `003F6BB0`; `00281ED0` is called by `00280DE0`; `0028AAA0` calls `00273880`; `002A1900` is called by `002A0440`; `002A4430` calls `002AF960`; `002A4830` calls `002AF960`; `002A9F00` calls `002AC5F0`; `002ABB20` calls `002AF340`; `002ABB20` is called by `002ABF70`; `002ABF70` calls `002ABB20`; `002AE610` is called by `002AC5F0`; `002AF340` is called by `002ABB20`; `002AF960` calls `002B2150`; `002B2150` calls `002AC5F0`; `002B2880` is called by `002A4830`; `002B2930` is called by `002A4830`; `002B2D60` is called by `002A4430`; `002B2DF0` calls `002B2150`; `002B2DF0` is called by `002AC5F0`; `002B5390` calls `002B2150`; `002BA310` calls `00402000`; `002D8D10` is called by `003FAF10`; `002FC010` is called by `0024B9B0`; `0035D480` is called by `003FAF10`; `00368360` calls `00368010`; `003B0220` is called by `0024B9B0`; `003B15C0` is called by `0024B9B0`; `003B2930` is called by `0024B9B0`; `003C1A20` is called by `003BE3A0`; `003FAF10` calls `0029F6E0`; `003FB8F0` is called by `003FAF10`; `003FDFE0` calls `003FDAD0`; `00402000` is called by `002BA310`; `00565DD0` is called by `00281ED0`; `0056F810` calls `00291D80`.

**WorldAreaField — MECHANICAL, 4 edges.** `002DC290` is called by `0057FB00`; `00313A00` calls `FieldData_GetActiveFieldRecordBit15` (`00377C20`); `00313A00` is called by `BattleSystem_RunFieldFrameOrchestrator` (`00234590`); `005742D0` calls `00576A50`.

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*
