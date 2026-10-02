# Consumption draft: actor-directory-kind-proof (FABLE, 2026-10-02)

*Links inside proposed page text are shown as `page-relative link:` paths, because they resolve from the target page, not from this folder.*

This draft is for FABLE to apply. Nothing here has been applied. Its scope is the accepted claims of
[REVIEW.md](REVIEW.md), with the review's six narrowings, at the stated limits. It was drafted against HEAD
`e828e3f50`, which does not touch the target page. The target page has CRLF line endings.

## Candidate pages and who leads them

The lead counts come from `git log --format=%s -- <page> | cut -d: -f1 | sort | uniq -c`.

| Page | What it says now | Commit subjects by prefix | Lead | Action |
|---|---|---|---|---|
| `_index/candidates/ov16-motion-functions-fable-0930/README.md` (found by `grep -rl asp_a03`) | §4 "What stays open", first bullet: the count-prefix/carve link for actor 25 is "the one link not read in the bytes"; §3 C4b calls "record ordinal = directory index" an inference | FABLE 1 | **FABLE** | edit 1 (required), edit 2 (optional) |
| `04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md` | §7b: the descriptor's two counts, and the subflag index is the group | OPUS 6 | OPUS | **route to OPUS** (the packet assigns the ordinal/category/descriptor and preset-point qualifications to OPUS); suggested text below |

This draft does not edit `_index/OPEN-QUESTIONS.md`. The OV-16 row does not state the carve premise, and its timing
gap is unchanged.

## Edit 1 (FABLE page, required): replace the unread premise in §4

File: `Database/FFXII TZA/_index/candidates/ov16-motion-functions-fable-0930/README.md`. Section: "## 4. Verdict",
"What stays open, kept separate:", first bullet (lines 173-177 at HEAD).

OLD:

```
- **Static inference, not read here:** that this actor's record gets `+0x1C` bits 16/17 at birth. The initialiser sets
  them for sequences 5, 6 and 7 (`actor-storage-record-flags1c-initial-values.tsv`, `0x00030004` for 6). The record's
  sequence is the carve-loop class `k` (`the-record-behind-every-actor.md`, EH-1, `00267AFA`–`00267B13`). That `k`
  equals the directory `scriptType` (6 here) through the header `+0x14` per-type counts is the one link not read in the
  bytes. Even without it, `attack_02`'s `reqenable(17)` sets bit 17 explicitly.
```

NEW:

```
- **Read in the bytes and the data (2026-10-02), replacing the inference that stood here:** this actor's record gets
  `+0x1C` bits 16 and 17 from its initialiser, and what selects them is the actor's ordinal, not its `scriptType`
  label. *(From ASTRA's `actor-directory-kind-proof` (`317ebd1b8`), reviewed by FABLE ACCEPT-WITH-NARROWING:
  [record] (page-relative link: `../fable-review-astra-actor-directory-kind-proof-1002/REVIEW.md`), 69 checks, 0 FAIL, 16 controls.)*
  - **The ordinal.** In the US `asp_a03.ebp`, the header `+0x14` table has 8 rows with counts 9, 11, 0, 0, 0, 4, 72,
    0 (sum 96, the directory count). All nine language copies have the same counts.
    - The record allocator carves the rows in order and publishes one pool pointer per record. So ordinal i
      belongs to row k exactly when sum(counts[:k]) <= i < sum(counts[:k+1]).
    - Row 6 spans ordinals 24..95, so actor 25 is in row 6.
    - The carve stamps the record's `+3` with `0x66`: row 6 in the low five bits, and the native table's kind 3 in
      the upper three.
  - **The binding.** The initialiser `00266530` receives the same pool and ordinal.
    - It selects `pool[1 + 25]` (`00266530` + 0x3A).
    - It binds the record's `+0x40` to directory entry 25 (`00266530` + 0x204). That entry is at section offset
      `0xD2A4` = `[+0x18]` + 4 + 48 × 25. The stride is 48 because the descriptor's WORD `+0` is 11.
    - Entry 25 is `ラバナ_通常_NPC01`. This also puts §3 C4b's "record ordinal = directory index" in the bytes for
      this actor.
  - **The preset.** The preset leaf that the initialiser calls switches on `+3 & 0x1F`, which is the row.
    - Rows 5 and 6 store DWORD `0x00030004` into `+0x1C`. That is bits 16 (`talkhold`) and 17 (`talkterm`),
      exactly the masks `00268EA0` tests.
    - The six later direct `+0x1C` writes in `00266530` (two ORs and four ANDs) all keep bits 16 and 17.
  - **The label is not the selector.** The directory WORD `+4` (`scriptType`) is 6 here, and it equals the
    count-prefix row for all 96 entries.
    - No instruction on the allocator, initialiser or preset path reads it.
    - A copy of the map with entry 25's label changed to 7 still gives row 6 and `0x00030004`.
    - The kind bits never reach the preset either, and row 5 gets the same `0x00030004`.
  - **Gate, not filing.** The initialiser does not file `talkhold` / `talkterm` itself. It clears `+0x0B` bit 3, and
    its two `00268EA0` calls test that bit. Bits 16 and 17 are therefore a gate for a later filer run, such as
    `0026CE60`'s, `reqenable`'s or `REQCHG`'s.
  - **Still open, not read:**
    - what the initialiser's later callees and its tail do to `+0x1C` (the review emulated them as bare returns);
    - the record's final live flags;
    - natural scene setup, including which caller first runs `00268EA0` for this actor.

    The manager count covering ordinal 25 (96 here) is a premise. Whatever the birth state, `attack_02`'s
    `reqenable(17)` still sets bit 17 explicitly.
```

The second bullet of "What stays open" ("**The live fact (the interleaving) for OV-16's motion route** ...") stays
unchanged. It is the natural wait, cancel, reentry and receipt timing gap that this packet does not answer.

## Edit 2 (FABLE page, optional): qualify C4b in §3

Same file, §3 controls table, row C4b.

OLD:

```
| C4b | 441 of 450 resolved targets are named `talkhold*` / `talkterm*`. This checks the reading "record ordinal = directory index", which is an **inference**. The 9 others are `rbn_a01`'s `catrine_talk_term` (×9 language copies) on slot 17. |
```

NEW:

```
| C4b | 441 of 450 resolved targets are named `talkhold*` / `talkterm*`. This checks the reading "record ordinal = directory index", which is an **inference** here. *(For `asp_a03` actor 25 it is now read in the bytes: the initialiser binds `pool[1 + i]` to directory entry i; see §4, 2026-10-02.)* The 9 others are `rbn_a01`'s `catrine_talk_term` (×9 language copies) on slot 17. |
```

## Citations

The NEW text cites `00266530`, `00268EA0` and `0026CE60`, which the page already cites (§1). Interior addresses are
written `00266530` + 0x3A and `00266530` + 0x204.

These are **named by role, not by address**, because the page does not cite them:

- the record allocator (`002679F0`);
- the preset leaf (`00266BD0`; its `0x00030004` store is at `00266BD0` + 0x42);
- the pre-preset leaf (`00266AD0`);
- the initialiser's tail target (`003DB280`).

Their addresses are in the review record. The old text's bare interior range `00267AFA`–`00267B13` is removed with
the bullet it sat in. The file name `actor-storage-record-flags1c-initial-values.tsv` is dropped too: the preset
point is now read in the bytes.

The page is a candidate record with no `owner_layer` front matter, so no neighbour pre-check was run.

## Route to OPUS: `04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md`

Suggested text for §7b, or wherever OPUS keeps the ordinal and category qualifications:

```
- Ordinal, row and preset (FABLE review of ASTRA `actor-directory-kind-proof`, 2026-10-02):
  - The allocator `002679F0` publishes `pool[1 + ordinal]` row by row, so ordinal i is in row k exactly when
    sum(counts[:k]) <= i < sum(counts[:k+1]). The counts are the u16 entries after the group count at
    descriptor + s32 [desc+0x14].
  - Nothing bounds the published ordinals by N = manager +0x20; N covering sum(counts) is a precondition.
  - The initializer `00266530` binds record +0x40 = desc + s32 [desc+0x18] + 4 + 48*i (32*i when WORD [desc+0] < 8).
  - The preset leaf `00266BD0` switches on the GROUP (record +3 & 0x1F), not on the kind:
    - groups 5 and 6 store 0x00030004 (group 5 also sets +0x14 bit 7);
    - group 7 stores 0x00034C85 and sets +0x14 bit 7;
    - group 0 stores 0, groups 1-2 store 0x38, groups 3-4 store 0x40.
  - The initializer clears +0x0B bit 3 before its two `00268EA0` call sites, so it never files talkhold / talkterm
    itself unless a callee sets that bit.
  - The directory WORD +4 (scriptType) is read nowhere on this path.
```

- consumer: `ov16-motion-functions-fable-0930/README.md` §4 - revised-here (edit 1; edit 2 optional)
- consumer: `CONTRACT-actor-record-pool-and-region-map.md` - routed-to OPUS (ordinal / group / preset qualifications)
- consumer: the register row OV-16 - agrees (timing gap unchanged)

affected: `Database/FFXII TZA/_index/candidates/ov16-motion-functions-fable-0930/README.md`

run: `rv_actordir.py` at HEAD e828e3f50 (69 checks, 69 PASS, 0 FAIL, 16 controls)
