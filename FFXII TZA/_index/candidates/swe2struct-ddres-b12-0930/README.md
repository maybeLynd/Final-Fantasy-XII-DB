# DD residue closure, batch 12: the render-record residue, the FCP block, the table registry (SWE2-STRUCT for OPUS, 2026-09-30)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`, batch 12 (brief: `Tools/work/OPUS/lane_brief_dd_b12.md`). A Claude
session in the SWE2-STRUCT lane, started by OPUS, ran this batch. It used no subagents, no board operations and no
commits. Page 1 of the brief was done by OPUS and is skipped. Page 2 was partly done by OPUS
(`opus-render-record-residue-0930`), so only its remaining items are worked here.

| page | git state when the batch started | edited here |
|---|---|---|
| `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md` | **modified, uncommitted**: OPUS's two notes from `opus-render-record-residue-0930` | at first **no**, because the rules forbid editing a page with someone else's uncommitted change. OPUS committed its notes during the batch (`5f3b94f75`), and the page was then clean. Notes N1 and N2 were applied after that, notes only (numstat 9 / 2) |
| `17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md` | clean (LF) | yes: notes only, no strike (`git diff --numstat` 23 / 6) |
| `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md` | clean (LF) | yes: notes, and three corrections with strikes, so this record has a [`consumer-check.md`](consumer-check.md) (numstat 86 / 22) |

All three pages are still all-LF (0 CRLF). No status word was moved. The proposed status lines are at the end.

The sentences were found with `grep -n -i` for *not read, unread, not yet, not established, still open, remains open,
unknown, not settled, not proven, UNRESOLVED, not followed, residue, what remains, is open, not decoded, not known,
not checked, highest-value*. The line numbers below are HEAD's.

## Dispositions (SWE2-STRUCT for OPUS)

**Legend.** **STALE**: the item is already answered, so a dated pointer note was added. **BOUNDARY**: another page owns
the fact, so a pointer was added. **RESIDUE**: the item is open and in scope; it was answered here, or a row is
proposed. **carried**: the line already names its answer, so it was not edited.

### the-character-render-record-array.md: STALE 0, BOUNDARY 0, RESIDUE 2 (both answered, notes applied) (SWE2-STRUCT for OPUS)

| line | sentence | disposition |
|---|---|---|
| 4 (status) | "UQ-196 … UQ-197 … are open" | STALE. Both are SUPERSEDED as duplicates, of BT-2 and BT-3. The proposed line is at the end |
| 683, 706–707 | "the semantic names of the three special bones" | **RESIDUE, answered** (SB1–SB9). The image has no names, so the bones are given roles by consumer. Note **N1** applied |
| 615–623 | "`+0x414` stays `UNRESOLVED` on meaning … the only door left open" | **RESIDUE, answered** (F1–F5). `+0x414` is write-only on PC: it has no reader on any followed route, the door included. Note **N2** applied |

### fcp-character-parameter-block.md: STALE 6, BOUNDARY 0, RESIDUE 3 (2 answered, 1 proposed row) (SWE2-STRUCT for OPUS)

| line | sentence | disposition |
|---|---|---|
| 4 (status) | "UQ-217 … UQ-218 … are open; UQ-220 is narrowed" | STALE: UQ-217 is SUPERSEDED (a duplicate of FW-1, which is ANSWERED), and UQ-218 / UQ-220 are ANSWERED. The proposed line is at the end |
| 187 (the `+0x36`–`+0x3E` cell) | "the three model-declared special bones … that the render-record page names" | **RESIDUE, answered**: the roles were added in the cell (SB1–SB9) |
| 291 | "several of slots 87–98 hold non-numeric bit patterns" | STALE: slots 83–98 are the bone table (the §2 correction of 2026-09-18). Note added |
| 367 | "The `@FOR`, `@FDM`, `@FTE`, `@FCT`, `@FEF` and motion-entry readers stay unread here." | STALE: the UQ-218 answer on line 368, plus the `@FTE`/`@FCT` page for the two it does not name. Note added |
| 392 | "the readers of section 8's copy, which stay with `UQ-218`" | **RESIDUE**: UQ-218's answer does not cover them, so no row carries them. **Proposed row P1** below, with the lead C3. Note added |
| 476–477 | "The three computed-id sites … nothing establishes what they pass." | STALE: UQ-219's answer, pinned by C2. Note added |
| 554 | "0041F010 repeats the same section-3 reads (skimmed, not read whole, so not cited)" | **RESIDUE, answered** (C1): it was read whole. Note added |
| 584 | "What a record holds was not read." (section 8) | STALE in part: the 2026-09-21 Section 8 extension decodes the record. The runtime remainder goes to P1. Note added |
| 598 | "sections 2 and 6, which still have none by this wider sweep" | STALE: the 2026-09-21 inventory gives `003E4B40` and `003E5C0E`. Note added |
| 186, 263, 366, 373–374, 391, 394, 479, 593, 648, 721 | the tag-scan inert cell; "partly"; UQ-218 / UQ-220 question text; "the rig page's own unknowns"; the UQ-221 question; "Not claimed"; "What the objects are" (answered in the next sentence); section 5's and section 10's "no reader" | carried. These are answered in the same box or sentence, are boundaries that already point to their owners, or state an instrument's bound |

### authored-data-table-registry.md: STALE 13, BOUNDARY 4, RESIDUE 5 (all answered) (SWE2-STRUCT for OPUS)

| line | sentence | disposition |
|---|---|---|
| 4 (status) | "the contents of the other 26 slots (UQ-80) are open" | STALE: UQ-80 is SUPERSEDED (class-1 ruling). The proposed line is at the end |
| 344–348 | "Settling that completely needs a base-plus-index scan … which is `AG-9`" | STALE: AG-4 answers it, and R3 shows there is no such path. The register's AG-9 is something else. Note added |
| 361 | `003845F0` "not read" | STALE: read whole as AG-12, §8d. Note added |
| 363 | `00384160` "not read" | BOUNDARY: read on the navigation-mesh and map-ctrl-pack pages. Note added |
| 364 | `ImageAddress_ResolveRuntimePointer` "not read" | STALE: read whole on this page. Note added |
| 415–416 | "the highest-value unread targets" | STALE: AG-1. Note added |
| 417–418 | "Three slots are unreferenced … or reached by a path this scan cannot see" | STALE: AG-4. Note added |
| 530–536 | "passed … together with a **data-driven index** … So any slot … can be bound through that path" | **RESIDUE, answered and corrected** (R3). The value is slot 0's descriptor, and the binder writes only the slot it is handed. **Struck**, with a note |
| 589 | "not proven. It is recorded as **AG-5**" | STALE: AG-5 is answered NO. Note added |
| 896 | "**AG-2 stays open**" | STALE: AG-2 is ANSWERED (2026-09-26). Note added |
| 910–912 | "that every slot is an area-data section descriptor at all … the second read as settled" | STALE: AG-11, AG-5 and AG-2 settle it. Note added |
| 1281–1282 | "why the bias is five … The record's remaining `0x50` bytes are unread." | BOUNDARY: the encoded-id class registry page owns the nibble records, and its `00309EC0` read settles nibble 15. Note added |
| 1400 | "`unk0A` … not established" | **RESIDUE, answered** (R1). It is the high half of `st2e` `recordSize`: 0 in all 333 headers and read by nothing. Note added after the fence; the fence itself was not edited |
| 1582–1583 | "the 84/88/56/56 record layouts are not" | BOUNDARY: the `.ard` loader page §7 and its CC-7 section. Note added |
| 1603–1606 | "the link from `[rdi+4]` back to a *named enemy* unestablished" | STALE: the section above it and CB-11 answer it. Note added |
| 1755 | "`0x02EBF168` … is not read here" | BOUNDARY: the `.ard` loader page §7a (CC-5). Note added |
| 1798 | "open residue tracked as `CB-11`" | STALE: CB-11 is ANSWERED. Note added |
| 1945–1948 | "whose callers — the loader of the per-model motion index — are unread" | STALE: CC-10, with the callers pinned by R4. Note added |
| 1970–1979, 1996 | "`00238260` passes `3` in that word … completion markers, not pointers … marks the completion"; the cell "the slots hold scalar values" | **RESIDUE, answered and corrected** (R2). The word is the buffer's address. **Struck** in three places and in the cell, with notes |
| 2020–2027 | "**Live tension, recorded rather than resolved** … Either the slots also receive real pointers …" | **RESIDUE, answered** (R2): the first branch holds. Note added |
| 2046 | "Whether the field can be `−1` is not established here" | STALE: AG-4's answer reads both writers. Note added; the note also points to the BSS correction |
| 2049–2051 | "It could also still be *written* through the registrar's base-plus-index binder path …" | **RESIDUE, answered** (R3). Note added |
| 535–544, 900, 1210–1212, 1534–1538, 1885, 2062, 2159–2172 | AG-4's "what remains" (answered at 501); AG-11 (answered in the same block); UQ-80's "Still open" (narrowed at 1213); "What is NOT established" (answered in the next section); the census's own scope; the tier-2 Audio crossing; the type-store shells question (store convention under UQ-80's class-1 ruling) | carried |

## The answers (SWE2-STRUCT for OPUS)

**The three special bones (SB1–SB9).** `003E5AD0(record, id)` reads the record's `@FCP` payload (`+0x400`). Ids below
`0x20` go through section 1's bone table. `0x104`, `0x105` and `0x106` return payload words `+0x3A`, `+0x3C` and `+0x3E`,
and any other id returns `0xFFFF`. The comparisons are on raw immediates, and the image gives the ids no name, so they
are named here by what consumes them:

- **`0x104` (`+0x3A`) is the body bone.** It has four consumers:
  - **The shadow.** The pool-A entry takes it as anchor A (`+0x3C`). The shadow LOD `003B5980` measures the bone's height,
    and the shadow draw `003B62D0` anchors on it.
  - **Lights.** `0042E7F0` → `004221F0` publishes its matrix at the model instance's `+0xF0`. The gather `003ABD50`
    evaluates a light against that matrix when the light's `+5` bits 1-3 are set, and against the record's own matrix
    otherwise.
  - **The rig.** The hit-flinch / Immobilize apply `00471230` and the Float-bob apply `004717E0` add their vector to this
    bone's pose translation (`+0x260` of its `0x290`-byte pose record).
  - **The chain** described below.
- **`0x105` (`+0x3C`) has no id consumer.** No call site passes it: the two variable-id callers are bounded below `0x100`
  and `0xFF` (SB2). It is read only as the chain's second link. 284 of the 326 weapons declare it instead of `+0x3A`.
- **`0x106` (`+0x3E`) is the shadow's anchor B** (`+0x3E`), the second bone `003B62D0` blends to. Authored command class
  `0x09` (`00417F40` → `003B5CE0`, choice in `+0xA8`) switches between A and B. It is bone 0, the root, in all 1,066 blocks.
- **The chain.** `00421CD0`, `003E4CB0` and the focus-point frame `003E5FA0` take the first of the three words that is not
  `0xFFFF`. The gate `byte[payload] >= 3` always passes, because the byte is 4 in all 1,066 blocks. Note for the brief:
  `00421CD0` returns 0, not `0xFFFF`, when all three are absent.
  - Its result goes to the model object's `+0xB6`. That field's one reader is `0053D780`, which hands the bone's matrix
    to the draw setup `004FD4B0`.
  - The draw setup copies the matrix's translation into the draw packet (`+0x160`) and into `02EBA4A0`. Only the
    `@FTE`/`@FCT` packet builder `0053AB50` reads that global.
- **Who declares what.** `+0x3A` is declared by every chara (17), summon (26) and treasure (17), by 253 of 254 monsters
  and by 173 of 174 NPCs. `+0x3C` alone is declared by 284 weapons, 16 gadgets and 1 monster. 121 of the 132 `high`
  models declare neither, so for them the chain lands on the root.

**`+0x414` (F1–F5).** It has two writers. The reset `0041F730` stores `1/6`, and the promoter `00428710` copies in tail
`+0x28`, which is itself a constant: `1/6` is written by `004269A0` and `0042ED30`, and only the promoter reads it.
**Nothing reads `+0x414` on any route the census follows.** Measured with `structflow`:

- **The array routes.** It started from all 639 references to the array global (375 functions, call depth 3, 845
  functions walked). Every other hit is a loop-induction alias, whose base register carries 232 or more offsets.
- **The escape routes.** It then seeded all 12 sites where the record pointer escapes, adding 176 seeds (1,238 functions
  walked):
  - the published copies `02EBB740` / `02EBB750`;
  - the model instance's `+0xF8` back-pointer;
  - the `+0x2E0` holders;
  - the status-push blocks;
  - the five out-parameters.
- **Width.** No access of 16 bytes or more covers the field.
- **Control.** The same census finds the known `+0x408` read `002EDC14` and the light gather's `+0x5EC` read
  `003ABDF3`. The second is reachable only through the `+0xF8` escape.

So the field is write-only on PC. The page's 2026-09-15 retraction of "fade step" was right. Its door, "a reader that
folds an array offset into the displacement or works from a biased base pointer", is the case `structflow` models, and
nothing comes through it.

**The registry's board slots (R2).** The `3` that `00238260` passes is `00384420`'s fourth argument. `00384420` spends it
on `0036C1D0` before the allocation replaces `rbx`. The request descriptor's `+8` word is therefore the buffer's low
dword (`003844B9`). The request queue carries that word to the callbacks' `ecx`, and the setter stores it,
sign-extended. So `0x02EBF1A0 + 8k` holds the address of the loaded `board_{k+1}.bin`. `0055BFF0` reads it as the `licd`
header, and all 48 shipped boards carry 24 × 24 there.

**The registry's binder (R3).** `003845F0(slot, desc)` writes only `[slot]`. Its 42 call sites pass 41 distinct
rip-relative slot addresses, and none is `0x02EBF198`. The one other site, `00238640`, indexes `0x02F973C0`. The
"data-driven index" at `00237010` is slot 0's descriptor.

**Header `+0x0A` (R1).** It is 0 in all 333 `st2e` headers of the nine `battle_pack.bin`. The census from 1,818 table-slot
loads (254 functions) finds no access covering it. The only exception is a dword at `+8` on `0x02EBF158`, a slot with
its own `{u16 stride, u16 count, u32 rows}` header at `+4`.

**0041F010 (C1)** is described in the page note. **The computed ids (C2)** are one `cmov` between two constants and two
pass-throughs.

## In player terms (SWE2-STRUCT for OPUS)

- **One bone carries the body.** When a character flinches from a hit, shakes under Immobilize or bobs under Float,
  the engine moves one model-declared bone. The shadow tracks that same bone and fades as it rises. Lights authored to
  follow the body are lit from it. Weapons, which have no body bone, name a substitute that only the draw and the focus
  point use. A modder who changes `+0x3A` in a model's `@FCP` moves all of this at once.
- **The `1/6` beside each character's render record does nothing on PC.** It is copied in at every promotion and never
  read.
- **The job-board slots are real pointers to the loaded boards.** They are not "done" flags. The licence-board screen
  reads each board's width, height and squares straight through them.

## The two notes applied to page 2 (SWE2-STRUCT for OPUS)

- **N1**, after "the semantic names of the three special bones." in section 13: the roles above, with SB1-SB9 cited.
  It sits before OPUS's UQ-191 note on the same line.
- **N2**, after "…that is the only door left open." in section 12: the F1-F5 census, its control, and the constant source
  tail `+0x28`. "UNRESOLVED on meaning" is left in place and not struck. The note answers it, and the status word is
  OPUS's.

## Proposed register row, id-less, for SWE2-DATA (SWE2-STRUCT for OPUS)

- **P1.**
  - *Question:* who reads the runtime copy of `@FCP` section 8, and what do they do with it? The copy is made in the
    28 blocks that carry the section: `0x10 + n x 0x1D0` bytes are `memcpy`'d at `0041F5CE` / `0041F5D9` into the
    model's aux region, the offset is kept at render record `+0x300`, and the lazy pool init `0051D220` follows the copy.
  - *Source:* `fcp-character-parameter-block.md`, the UQ-220 box ("the readers of section 8's copy") and section 3's
    "What a record holds was not read".
  - *Lead (C3):* the four `+0x300` accessors, with their callers:
    - `003E6680`, from `00425DC0`, which tail-jumps `0051CDE0`;
    - `003E66D0`, from `00425E10`;
    - `003E6710`, from `0041FCF0` and `00520140`;
    - `003E6D40`, from `0042CBF0`, `0042D050`, `00421280` and `004213E0`.
  - *Why not answered here:* the copy's readers are a `0051Cxxx` family outside this batch's pages.

Nothing is marked runtime-only.

## Routed, not edited (SWE2-STRUCT for OPUS)

- **The R2 correction contradicts three other places.** These are routed to OPUS, and their owners correct them:
  - `02-Resource-And-Asset-Pipeline/the-resource-request-queue.md` lines 305–308: "hand `3` in that word … the slots are
    completion markers";
  - `12-Items-Equipment-Shops-License/license-board-grid-format.md` lines 154–156: "a generated setter marks each
    completion (the bytes live in the loader's resource block, not in the slot)". The page's own 2026-09-13 correction
    on line 174 already follows the slot pointer.
  - `_index/EVIDENCE-STANDARD.md` line 4429: "a **data-driven index**, so any slot is reachable unnamed" (R3).
- `_index/AUDIT-LOG.md` and `_index/_inbox/FABLE.md` are historical and were left as they are. FABLE.md line 4791
  already calls the twelve "loaded-resource pointers".
- AG-4's own answer leaves a remainder: the data range of the byte `0055CD40` copies into `+0x558`. It was not
  re-examined here.

## Receipts (SWE2-STRUCT for OPUS)

| script | result |
|---|---|
| [`b12_struct.py`](b12_struct.py) ([`b12_struct.out`](b12_struct.out)) | SB1–SB9, F1–F5, C1–C3, R1–R4: **149 PASS, FAILS 0** |
| `documented_rule.py` ([`documented_rule.out`](documented_rule.out)) | `TALLY NEEDS-POINTER=3 of 3`, FAILS 0. The status lines are not edited, so the P pointers are still missing: UQ-196, UQ-197 and UQ-198; UQ-217; UQ-80 |

**Inputs.** The work is static, on the certified image `73461d08…`, through `retool.py` and `structflow.py`. The data is
the installed `FFXII_TZA.vbf`: 1,066 `.cm`, nine `battle_pack.bin` and 48 `board_N.bin`.

**Positive controls.**
- SB3: the census finds the selector's own reads.
- SB9: the per-word totals reproduce the FCP page's falsification-pass figures, 628/426/12 and 762/301/3.
- F4: the known `+0x408` and `+0x5EC` readers are found.
- R1: the `0x02EBF158` dword reads are found and attributed.
- R2: the `licd` width and height.

**Blind spots.**
- `structflow` does not see indirect-call targets (listed in its output), code outside the function extents, or taint
  through non-stack memory other than the seeded escapes.
- The 32-bit pointer round trip in R2 assumes a sub-2 GiB arena (BW-2).
- The bone roles are by consumer. What an artist called the bones is not in the image.

## Proposed status lines (SWE2-STRUCT for OPUS; the status word stays OPUS's)

Each line names every disposed row with its disposition word, which is condition P.

- **the-character-render-record-array.md:** `status: <word> — the rest of the 0x740 record (UQ-196) is SUPERSEDED as a duplicate of BT-2, itself SUPERSEDED 2026-09-27 under FRONTIER's class-1 ruling (fields.tsv tiles all 1,856 bytes; the DISCOVERED spans are the static-FIELDS work); the rest of the 0x130 tail (UQ-197) is SUPERSEDED as a duplicate of BT-3, answered 2026-09-26; pool exhaustion (UQ-198) is SUPERSEDED as a duplicate of BT-5, answered 2026-09-18 (160 records, 160 slots, one per promotion; an exhausted allocation would store handle 0 and every consumer guards on it); the subtype meanings (BT-4) answered 2026-09-27 (each is the motion slot it plays: revive, c_turbo, active, deact); BT-6 answered 2026-09-17 with its premise corrected; the three special bones' roles and +0x414 (write-only on PC) answered 2026-09-30 (swe2struct-ddres-b12-0930)`
- **fcp-character-parameter-block.md:** `status: <word> — what each slot means (UQ-217) is SUPERSEDED as a duplicate of FW-1, answered 2026-09-26 (every cached tunable has a reader; the unaddressed slots have none in the image); the other @Fx entries (UQ-218) answered 2026-09-30 (SWE2-DATA pass 18); the payload sections (UQ-220) answered 2026-09-26 (section 2 is the rig, 3 the attachment table, 6 dead, 18 and 21-24 absent); the one-slot-behind default table (UQ-219) and the section-1 pairs (UQ-221) answered 2026-09-18; prose residue: the readers of the section-8 runtime copy, row proposed 2026-09-30 (swe2struct-ddres-b12-0930 P1)`. The page keeps that residue until SWE2-DATA registers P1.
- **authored-data-table-registry.md:** `status: <word> — the contents of the other 26 slots (UQ-80) are SUPERSEDED 2026-09-27 under FRONTIER's class-1 ruling (uq80_coverage.py: 15 of 23 tables fully mapped, the 60-byte residue carried by the static-FIELDS work); the identity of all 64 slots (AG-2) answered 2026-09-26 (ag2-slot-identity.tsv); whether same-slot classes differ elsewhere (UQ-81) answered 2026-09-25 (they do, in the query-record filler); the board-request slots corrected 2026-09-30 (they hold the loaded boards' addresses; swe2struct-ddres-b12-0930 R2)`
