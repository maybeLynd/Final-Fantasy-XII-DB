# DD residue closure, batch 21: the shop table and spawn placement (SWE2-STRUCT for OPUS, 2026-10-01)

Request: OPUS's DD residue closure, batch 21. Board task `SWE2STRUCT-DD-B21-1001` (research, added and claimed at board
revisions 44403 and 44404). The batch was run by a Claude session in the SWE2-STRUCT lane, started by OPUS, with no
subagents and no commits. OPUS publishes.

Both pages pass `documented_rule.py` (READY and READY-WITH-POINTER) but still carried prose residue without a register
id. Both were clean at HEAD when the batch started (`git status --short` empty) and both are pure CRLF. The edits are
additive notes only: nothing is struck, so this batch has no `consumer-check.md`. Every line keeps its CRLF ending
(`git diff --numstat`: shop 5/5, spawn 9/7; the spawn page's two extra lines are one new blockquote paragraph). The
edit script is `Database/Tools/work/SWE2-STRUCT/b21/apply_b21.py` (idempotent, every anchor matches once). No status line,
front matter or register row was touched.

The sentences were found with `grep -n -i` for *not read, unread, unresolved, not yet, not established, still open, stay
open, remains open, unknown, unnamed, not settled, not traced, not known, live-only, not shown, not proven, not
decoded*, and a wider pass for *does not establish, routed, pending, remain required, outstanding, remain separate,
still need, not proved, not replayed, not excluded*. Text inside `~~strikes~~` and lines that already carry a later
answer note were set aside. Line numbers are those of the pages at the start of the batch.

## Dispositions: the shop table (SWE2-STRUCT for OPUS)

Legend: **(a) STALE** = answered elsewhere, so a dated pointer was added. **(b) ANSWERED** = settled statically here
and answered in place. **(c) LIMIT** = a bound on a claim, now marked as a stated limit. **BOUNDARY** = another page
owns it. **carried** = struck, or already carrying its answer.

| line | sentence | disposition |
|---|---|---|
| 338 | UQ-133's answer: "native writes of the counter are not censused" | **(c) LIMIT**: the answer rests on the script census; UQ-133 is ANSWERED with that limit |
| 384–388 | "What this does not establish: which screen the widget is" | **(b) ANSWERED** (M1–M6): `002BA310`'s only caller is the location map's page procedure `002BAF80`, at `002BB836` in its confirm-on-marker arm; `002BD8C0` and `002BA530` are reached only from `002BA310`, and `002B9C70` only from `002BD8C0`. The widget is the `0x3E0`-byte child page the location map opens on a kind-0 marker |
| 384–385 | "… and what the ten categories and the type codes at word `+0x8` are" | **BOUNDARY**, stated: the map screens page's, which SWE2-CONTRACT is editing now. Not a question this page asks |
| 480 | "The `in`/`kr` copies were not decoded" | **(b) ANSWERED** (V1–V7): all nine `battle_pack.bin` packs hold the same shop table |
| 797 | "What stays open is whether message 26's layout write can land on a list … That is GR-14" | **(a) STALE**: GR-14 ANSWERED (no) |
| 899–905 | "which kinds each family actually uses is **not** established here … Registered as GR-15" | **(a) STALE**: GR-15 ANSWERED |
| 287 | the heading "7. What is not known" | carried: a template heading; every box below it is ticked (G3). The heading is not edited, so its anchor is kept |
| 336, 629, 775–776, 783–785, 796, 858–860, 991 | the vendor's place, the half-price rule, the selector route, the object's identity, the `+0xC0` pairing, the second word, the counter | carried: DD batch 11 notes and FABLE's 2026-09-30 corrections |
| 318, 692 | the predicates; "*Still not read:*" | carried (struck, with corrections) |
| 736 | "left unnamed" | carried: it quotes a retracted statement inside its own amendment |

**GR-13 / GR-14 / GR-15 and their consumer items.** All three rows are ANSWERED in the register (G1). OPUS's record
`gr13-15-shop-list-widget-0930` routed six page contradictions to FABLE. The page carries all six as dated corrections
naming "statement 1" to "statement 6" (G2), applied by FABLE's `shop-page-corrections-fable-0930`. Section 7 has no open
box (G3), and the GR-14 and GR-15 boxes carry their answers (G4). So the page no longer waits on these consumer items.
What is left from that record is its status line, which still says the three questions "stay open". That is OPUS's
re-status (below).

**Proposed register rows: none.** The one open item, the marker categories, is the map page's.

## Dispositions: spawn placement and retirement (SWE2-STRUCT for OPUS)

### Sections 1 to 11 (SWE2-STRUCT for OPUS)

| line | sentence | disposition |
|---|---|---|
| 482 | `0023A520` "*(unnamed)* spawn tunable reset" | **(a) STALE**: L-10 names it as the handler of verb `0x3053` `btlAtelSetupActorStart`, through the thunk `00510710` (A1–A3). Note added in the cell |
| 729–730 | "Actual same-frame activation/retirement requires caller scheduling … not established by these inequalities alone" | **(c) LIMIT**: the note claims the inequality, not the frame schedule |
| 768–775 | L-13: "Still open: the complete ordering …"; "Current-to-old session reuse and nonzero persistence/respawn remain open" | carried: FABLE reconciled both on 2026-09-30 (the static half answered; L-13 SUPERSEDED). The live-only residue has no carrier (R2, R3), so a pointer was added and it is proposed below as **row P1** |
| 1513–1514 | "Not established here: what that word actually holds in ordinary play — still live-only; whether any caller of `00235720` reliably leaves a particular value at that address" | first half **(a) STALE**: L-12 SUPERSEDED under the runtime rule (one read, deliberately not queued). Second half **(b) ANSWERED** (W1–W7): no caller leaves a value there |
| 1530–1533 | "those consumer changes remain open until their owners agree" | **(a) STALE**: FABLE's 2026-09-30 reconciliation below it; both review requests DONE (R5). Rechecked today: the gambit page's "copies them back" still stands (C1), so it stays routed to that page's owner |
| 1555 | "L-12 and L-13 are open above"; `crossref_clean` false | carried (reconciled). The graph audit is not prose residue: see "The graph audit" below |
| 1042, 1144, 1432, 1469 | "available and unread" (history of a correction); the ledger's "158 unresolved"; "Y is not read" (a code fact); "L-12 remains open" | carried: not residue, or already reconciled |

### Sections 12 to 29, ASTRA's dated packages (SWE2-STRUCT for OPUS)

FABLE's 2026-09-30 note under section 12's heading covers these sections as a block. This batch itemizes them and adds
one dated paragraph under that note. Four kinds of line occur:

- **L-12 / L-13 "remains open"** lines carry FABLE's inline reconciliation. They are carried.
- **"Review / propagation remains pending"** lines name reviews that are all DONE. The 30 review requests on these
  sections are DONE (R5), and no open board item names the page except this batch's task (R4: 104 items name it).
- **Live delivery, timing and chronology on an actual load** is L-13's live-only residue. It is proposed as **row P1**.
- **"Not established here" / "not proved" / "remain separate"** lines are stated limits of each package. Each bounds
  what that package read, as FABLE's note says. They are not questions this page asks.

| line | kind | disposition |
|---|---|---|
| 1574, 1653, 1700, 1718–1719, 1810, 1874–1877, 1985–1988, 2088–2092, 2169–2174, 2319–2322, 2434, 2533, 2681, 2800, 3165, 3314, 3443, 3486, 3535–3536 | L-12 / L-13 open | carried (FABLE's inline reconciliation) |
| 1813–1815, 1988, 2236, 2322, 2531, 2681, 2800, 2972, 3160, 3310, 3444, 3537–3538 | review or propagation pending | **(a) STALE**: R4, R5 (the matching requests: MANAGER-QUEUE, FIELD-PREP, WIDGET-ROOTS, WIDGET-GENERATION, LOAD-CLOSE, LOAD-MATERIALIZATION, LOAD-SUCCESS, STORAGE-COMPLETION, SAVE-CONTAINER, OLD-SAVE-CONVERSION, OLD-SAVE-LIVE-REVIEW, all DONE) |
| 1822, 1885, 1995, 2064–2066, 2099, 2158, 2269, 2355, 2594, 2918, 2973, 2976, 3162, 3521, 3536–3537 | the actual load's delivery order, timing and chronology; current-to-old session reuse; non-zero banks | L-13's live-only residue: **row P1** (runtime) |
| 1856–1858 | "Their actual script invocation and those gates' meanings are not established here" | **(b) ANSWERED in part** (E1–E3): the adapters are the script verbs `eventplay` (`0x00EB`, `00354E80`) and `eventplay_ec` (`0x00EC`, `00354B20`). Which scripts call them, and what the two gates mean, is marked **(c) LIMIT** |
| 2309–2310 | "The sort helper's full implementation is not read here" | **(b) ANSWERED** (S1–S7): the order does not depend on it |
| 1606 | the metadata wrappers' "downstream effects are not established here" | carried: FABLE's note (FO-1 ANSWERED, the battle runtime mode ladder) |
| 1940, 1954, 2025 | the authored group values; F-3 "pending its owner's integration"; the PC-2 review | carried: FABLE's notes (map_ref.bin; F-3 ANSWERED 2026-09-13; PC-2 ANSWERED) |
| 3081 | "The transformation helper … and complete container contract remain open" | **(a) STALE** for the helper and the contract: section 26 traces the recipe, and both SAVE-CONTAINER reviews are DONE. Allocation failure and short reads: **(c) LIMIT** |
| 1801, 1845, 1853, 1861, 1958, 1977, 2010, 2061, 2234, 2265, 2416, 2485, 2520, 2952, 3007, 3139, 3157, 3181, 3391, 3532 | unread callee effects, not executed, not replayed, survival through re-entrant callbacks, input-receipt comparison | **(c) LIMIT**: package bounds (FABLE's note, now itemized) |
| 2334 | "the chain left open by section 19" | carried: section 20 is the continuation |
| 2913, 2923, 3266 | "Its return is not checked"; "an unknown callee"; "Decode does not read its output-length pointer" | carried: code facts, not residue |

## The answers, in player terms (SWE2-STRUCT for OPUS)

- **Every language sells the same things (V1–V7).** The shop table is identical in all nine language packs: the same
  57 shops, 267 stock lists and 2,512 item references, entry for entry. The packs differ as files and the table sits at
  a different offset in each, but what a vendor stocks and when it unlocks does not depend on the game's language.
- **The shop names you see on the area map come from one list (M1–M6).** When you confirm a plain marker on the
  location map (the area map with jump icons), the map opens a small list page. That page names each marker. For a
  shop marker, it reads the shop's name from this page's table. No other screen builds that list.
- **Whether an automatic spawn takes its first good spot is decided by leftover memory (W1–W7).** The automatic spawn
  selector compares a candidate against a value on the stack that nothing in the spawn path writes. Its only caller is
  the script command `btlAtelDecideEntryPointAuto`, and that command writes nothing there either. So the value is
  whatever earlier work left in that memory, which depends on what the zone script ran before. It cannot be predicted
  from the code. Measuring it needs a live read (L-12).
- **Menu children are drawn in priority order, ties in creation order (S1–S7).** When a menu re-sorts its children,
  the highest priority (the word at `+0x44`) comes first. Children with equal priority keep the order they were
  created in. This holds whatever sorting routine is used, because the comparison never calls two children equal.
- **Playing a cut-scene event can release the field's actor hold (E1–E3).** The two script commands that release the
  pending latch for managers 1 to 3 are `eventplay` and `eventplay_ec`.

## Receipts (SWE2-STRUCT for OPUS)

Static work on the certified shipping image (`73461d08…`) through `retool.py`: its v4 extents, its reference cache,
its `.data` qword scan and capstone. The data is the installed `FFXII_TZA.vbf` (the nine
`ps2data/image/ff12/test_battle/<lang>/binaryfile/battle_pack.bin` packs), read by the checker's own SRYK reader. The
register and the board are read only.

| script | result |
|---|---|
| [`b21_checks.py`](b21_checks.py) ([`b21_checks.out`](b21_checks.out)) | V1–V7, M1–M6, G1–G4, A1–A3, W1–W7, S1–S7, E1–E3, R1–R5, C1, N1: **78 PASS, FAILS 0** |
| `documented_rule.py` ([`documented_rule.out`](documented_rule.out)) | shop `READY`, spawn `READY-WITH-POINTER` (L-12, L-13 SUPERSEDED, pointers present), `TALLY READY=1 READY-WITH-POINTER=1 of 2`, FAILS 0 |

run: b21_checks.py at 362571e7c (FAILS 0)

Controls and blind spots:
- **V is a decoded comparison, not a byte comparison.** Each pack is walked through the three header levels (tags
  `0x64`, `0x164`, `0x264`) with section-relative offsets. *Positive control:* the `us` pack gives the page's own figures,
  and row 24 sits at `+0x1338` with 39 entries and name `0x1F9` (V3). *Discrimination controls:* the nine files have nine
  different hashes (V5), the table sits at different offsets (V6), and flipping one id bit in one list changes the digest
  (V7). Only the `us` table's meaning (names, gates) is the page's. This check shows the other eight are equal to it.
- **M uses the reference cache.** *Control:* the same index returns all eight callers of the shared sort `00249CE0`, so
  a single caller is not an artefact of a truncated list. Indirect calls through a register are outside any caller
  index. `002BA310` has no `.data` slot and no rip reference, so no table or `lea` can reach it.
- **W rests on two frame layouts and one sweep.** The adapter's whole pre-call body is pinned (W3). The callee's
  prologue fixes the slot at 0xBC below the adapter's stack pointer (W4, W5). *Control:* the `rsp`-relative sweep sees
  the writes to `+0x30` and `+0x38` (W7). The claim is that no live frame owns the word at the call. What it holds is
  the live question, closed under the runtime rule as L-12.
- **S assumes `00249CE0` sorts correctly.** It is the shared sort with eight call sites. The partition loop is pinned
  in the usual sense (negative means "first", S6), but the whole routine is not proven correct. The order claim holds
  for any correct sort, because the comparator is a strict total order (S2, S3).
- **E names the verbs from the dispatch table.** No script census of `eventplay` / `eventplay_ec` calls was run.

## Proposed register row (SWE2-STRUCT for OPUS)

One id-less row, for OPUS. The disposition is runtime. FABLE's 2026-09-30 record (`dd-content-fable-0930`) noted that an
OPEN row would conflict with the runtime SUPERSEDED rule. So the proposal is either a row that is closed as SUPERSEDED
under the runtime rule *with* a named carrier, or adding the item to a runtime carrier's row list. Which of the two is
OPUS's call.

| proposed | question | disposition | evidence and carrier |
|---|---|---|---|
| P1 | **L-13's live-only residue.** On a slot-0 field-transition autosave load with non-zero keep banks: in which order do the load controller's and the area controller's message 18 arrive, and does the requeued area init's rotation then bring the same enemies back (current-to-old session reuse, non-zero persistence and respawn)? | **runtime**: not settleable statically, because the order depends on the live widget tree and on the destroy path taken | Static half answered: L-13 SUPERSEDED 2026-09-27 (`l13-bank-writers`). The named carrier `FABLE-REQ-ASTRA-L13-BANKS` closed on 2026-09-13, before the ruling, on EXP-080 with both banks zero (R3). `FRONTIER-RT-RUNTIME-SURROGATE` lists seven other rows (R2). Proposed carrier: add P1 to `FRONTIER-RT-RUNTIME-SURROGATE`, or a new ASTRA live request |

No other row is proposed. L-12's live word is already a register row, closed under the runtime rule and deliberately
not queued.

## The graph audit (SWE2-STRUCT for OPUS)

The spawn page's status line keeps REOPENED "until the amended citation surface has a fresh graph audit
(`crossref_clean` false)". That is FABLE's 2026-09-20 resume note (`_inbox/FABLE.md`, "what still holds
`spawn-placement-and-retirement.md` at REOPENED beyond L-12/L-13 is `crossref_clean: false`, which needs a fresh graph
audit rather than semantics"). It means a new `audit_crossrefs.py` report for the page with no findings, newer than the
page. `check_crossref_clean.py` then accepts `audit.crossref_clean: true` in the front matter. It is not prose residue
and not a register question. No board item carries it: R4 finds no open item naming the page except this batch's
task. This batch did not run `audit_crossrefs.py`, because a run regenerates the shared `pass22-tripwires.tsv`. Today's
notes add citations (`0050F520`, `01F28510`, `00244610`, `00249CE0`, `00354E80`, `00354B20`, `00510710`), so any audit
must run after this publish.

## Proposed status lines (SWE2-STRUCT for OPUS)

The status words are OPUS's. These texts keep the current words until the owner read.

- **Shop page:** `PARTIAL — GR-13, GR-14 and GR-15 are answered (OPUS 9c71391a8: one row layout with the price at entry +0x10; a shop list never receives message 26; the list kinds per widget family) and the body carries all six consumer corrections (FABLE, shop-page-corrections-fable-0930); the shop table, the gate and the listing are read whole, and the table is identical in all nine language packs (DD batch 21). Answered: UQ-132 (the 57 names), UQ-133 (the vendor is first usable at 3,100), the rank counters (FG-1), no purchase path re-checks a gate; no prose residue without an answer, a pointer or a stated limit (DD batches 11 and 21, swe2struct-ddres-b21-1001, 78 PASS, FAILS 0); documented_rule READY`.
  With that, the page has no open residue, and DOCUMENTED is OPUS's call.
- **Spawn page:** `REOPENED — ASTRA's independent falsification (§11) is integrated; its two rows are closed as L-12 SUPERSEDED (2026-09-26) and L-13 SUPERSEDED (2026-09-27), and every residue sentence in §§1-29 is answered, pointed or a stated limit (DD batch 21, swe2struct-ddres-b21-1001: the L-12 word has no static source, the child sort is a total order, the latch adapters are eventplay / eventplay_ec); L-13's live-only residue is proposed as one runtime row with a carrier; the status word stays REOPENED until a fresh graph audit (crossref_clean false) and the owner read`.
  The page's last blocker is the graph audit, not prose.

## For OPUS: routed, not edited (SWE2-STRUCT for OPUS)

- **The gambit page's restore sentence.** `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` (its "Threat is
  written to the save file" bullet) still says `SpawnKeep_RestorePersistenceBank` "copies them back", meaning both
  banks. The restore copies bank 2 only. FABLE routed this on 2026-09-30, and it is still unedited (C1).
- **The map page owns the marker categories.** "What the ten categories and the type codes at word `+0x8` are" stays
  open on the shop page as a boundary. SWE2-CONTRACT is editing the map screens page now, so nothing was written there.
- **Row P1 needs a carrier** (above).
