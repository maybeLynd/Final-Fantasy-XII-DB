# Consumer-check record — GI-8 to GI-11 answers and the effect-element corrections (FABLE, Claude Opus 5.5, 2026-09-29)

affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/the-element-types-00-0a.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/an-effect-element-frame-by-frame.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/the-element-types-60-74.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/the-element-types-80-97.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md`
affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md` (rows GI-8, GI-9, GI-10, GI-11)

Every correction below strikes the old words on its page and puts the corrected statement beside them, dated and
attributed. The consumers were found by grepping the database (`*.md` / `*.tsv`, without `_experiments/`, retained
copies, `AUDIT-LOG.md`, `_inbox/`, `ADDRESS-INDEX.md` and the derived `knowledge.sqlite`) for each address, offset and
phrase.

## The corrections and their consumers

**1. The authored-type census undercounted.** The dispatch page §2.8 said: "3,698 files, 31,635 `0xA00` records, 53
distinct values, 32,639 `0x800` chunks; of the 53, 42 have main arms and 11 sub-range; three types authored exactly
once". That walk read every `.efb` as one chunk stream, but an `.efb` holds EFX blobs, and the walk never saw the 531
EFX streams embedded in `.cm` / `.mpk` files. The earlier "11" list also named 14 types. Walking every stream gives
55 types, 48,868 records and 53,351 `0x800` chunks; 40 types are main-range and 15 sub-range, and only `0x8B` is
authored once.
- the dispatch page §2.8: corrected here (old figures struck and kept beside the new ones);
- `members/effect-type-authored-usage.tsv` and `effect_type_usage.py`: kept unchanged as the superseded snapshot; the page
  link now points to `type_census.tsv` / `type_census.py`;
- the containers page, its 2026-09-16 update ("every … `0xA00` element definition (31,635) and `0x800` sub-record (32,639)
  decoded"): corrected here;
- the kind-`0x54` mesh page §0 table: a caveat added here, numbers kept as a lower bound. **Routed to SWE2-DATA** (owner
  of `census_mesh54.py`): re-walk the kind-`0x54` records over the `.efb` blobs and the 531 embedded streams, using the same
  stream bound (EFX header `+0xC`) and chunk walk as `type_census.py`, and replace the page's figures;
- register row UQ-204, whose history cell says "53 distinct types over 31,635 chunks / 3,698 files". **Routed to the
  register owner**, exact text to append after its history: `(Census superseded 2026-09-29, FABLE GI-8: 55 distinct
  types in 48,868 0xA00 records over every EFX stream; the .efb blobs and 531 streams embedded in .cm / .mpk files were
  missed; see effect-element-type-dispatch.md section 2.8.)`
- the UQ-204 record under `_index/candidates/uq204-element-type-emits/`: carries no census figure, so it agrees and is unchanged.

**2. The step (`002F3BC0`) is the element's birth, not a per-frame step.**
- the dispatch page (line 28, §2.1, the key-address row): corrected here;
- the 40-42 page's "(the per-type per-frame math)": corrected here, in the struck paragraph;
- `members/effect-type-methods.tsv` (header "step 002F3BC0") and `_index/candidates/ov41-efx-children-fable/README.md`
  ("the step `002F3BC0`"): neutral wording; they agree and are unchanged;
- other pages matching "per-frame step" (`game-application.md`, `the-movement-and-secondary-context-censuses.md`,
  `06-Movement-And-Navigation/README.md`, `the-map-screens-and-their-shared-map-data.md`,
  `the-character-render-record-array.md`, `what-happens-between-two-frames.md`, `ms-map-screens-fable/*`,
  `CONTRADICTIONS.tsv`): none mentions an effect element or `002F3BC0`; unchanged.

**3. `00454890` was listed as a `0x80`–`0x97` tail.** It is neither a function nor an instruction start; the missing
tail is `00452C70`.
- the 80-97 page: corrected here. No other consumer (`knowledge.sqlite` regenerates).

**4. `0054C6B0` / `0054E040` were listed as the `0x73` / `0x74` tails.** They are birth-only piece generators; the update
tails are `0052E270` → `0054C440` and `0052F400` → `0054DD30`.
- the 60-74 page: corrected here;
- `loader-bound-bin-families.md` (lines 651 / 655) names the births as their callers, so it agrees and is unchanged;
- `procedural-stream-consumers.tsv`, `unlisted-body-admissions.tsv` and `actor-storage-record-flag-bit-writes.tsv` hold
  mechanical rows with no role claimed; unchanged.

**5. `0045F600` was called `0x67`'s tail, and `0024DDD0` a "config-indexed double lookup".** `0045F600` is the birth gate
(caster/target body separation); `0024DDD0` returns the owner and target actors.
- the 60-74 page: corrected here;
- `loader-bound-bin-families.md` (line 481, and §`0024DDD0` at line 636): agrees and is unchanged. Optional
  **routing** to that page's owner, line 521: after "`0045F600` (1788 B) is a bin-family element body", add
  ` - the birth gate of 0x67 / 0x6B: a body-separation test between the effect's owner and target (FABLE GI-10,
  2026-09-29, the-element-types-60-74.md)`;
- the character-render-record access tables (four `.tsv`): access rows only; unchanged.

**6. Setup arms `0053A5D0` / `0053A6F0` / `0053A790` / `0053A840` were labelled `0x65` / `0x66` / `0x67` / `0x68`.** They
belong to `0x67` / `0xA0` / `0xA1` / `0xA2`.
- the 60-74 page (four paragraphs) and the dispatch page ("Six more `005004C0` creation arms …"): both corrected here.

**7. Cluster and step statements on the 80-97 page.** Five statements are corrected there: the `0x8A` step is really
`0x89`'s; the clusters omitted `0x86` / `0x87` and `0x97`; `0020E610` replaces `0020E600` rather than adding a call; there
are six selector walks, not four; and `00458010` is its own function. The billboard wording also goes. All are
corrected here; a grep found no other consumer.

**8. `0xD0` "the payload is the seventh method … not per-frame"; `0x40`'s seventh method "on `+0x244`/`+0x24C`".** The
seventh method is the release/restore; the per-frame payload is `00465690`, driven by the registry walker. `0x40`
releases two different handles.
- the 40-42 page: corrected here;
- `intentionally-ownerless-functions-and-shared-scratch.md` line 697 (the same target switch): agrees and is unchanged;
- `CONTRACT-script-to-native-bridge.md` 446, `verbs-that-only-wait-and-verbs-that-do-nothing.md` 365,
  `the-actor-manager-record-field-map.md` 470 / 697, `the-field-runtime-pass.md` 592 and `CONTRACT-gambit-walk.md` 576
  are caller lists with no role claimed; unchanged.

**9. `EFX0009` "ships in no file at all".** It ships once, embedded in `alc1007.mpk`; `EFX0008` ships seven times.
- the containers page §5 (table and blockquote): corrected here;
- the same page's §6b table and item (c) count `.efx` files, which is true as stated; unchanged;
- `fef-and-motion-entries.md` line 207 (the loader accepts all three): agrees and is unchanged.

Additions that settle earlier "not read" notes, with nothing wrong in the old text: the frame-by-frame page's three
notes (`0x08`'s corner colours, the round-up to a multiple, `0x0A`'s random value), which are struck and settled with
a pointer.

## Regression

`gi_effects_checks.py` (this folder; output `gi_effects_checks.out`) re-derives each corrected fact from the shipping
image and fails on the old reading:

| correction | check |
|---|---|
| 1 | K18 reads the census data (`Effect-File-Formats/members/type_census.tsv`); the census itself, `members/type_census.py`, adds C1–C7, including C3 (the old walk reproduces the old table exactly) and C7 (the version magics, for correction 9) |
| 2 | K1 and K13 |
| 3 | K2 |
| 4 | K3 |
| 5 | K4 |
| 6 | K14 |
| 7 | K10 and K15 |
| 8 | K5, K6, K7 |
| additions | K8, K9, K11, K12, K16, K17 |

Result: K1 to K18 pass, FAILS 0. Before publication the script was run with `GI_EFFECTS_MEMBERS` pointed at the staged
copies of the new member files, because K18 reads a file this publish adds. `type_census.py` reported C1 to C7 pass,
FAILS 0.

run: gi_effects_checks.py at 6facc53bc (HEAD when it ran), K1 to K18 pass, FAILS 0 (output: gi_effects_checks.out)

The follow-up `followup_gi9.py` adds `d0_selector_census.py` to this folder (output `d0_selector_census.out`). Its R1 fails unless the 0xD0 blend block is authored with selectors 0 and 1 only (45 definitions); P1 and P2 are its positive controls. It ran with GI_EFFECTS_MEMBERS set to the staged members copy, because the embedded-stream list is added by this publish.

run: d0_selector_census.py at ed127d443 (HEAD when it ran), P1, P2 and R1 pass, 3 checks, FAILS 0 (output: d0_selector_census.out)

The follow-up `followup_gi10.py` adds `gi10_cores_check.py` and `gi10names.py` to this folder, each with its output (`gi10names.tsv` is the name table). The first re-derives the four simulation cores, and the translated VU1 program 004D40E0 that reads the six per-layer 0x71 values, from the image in 139 instruction-level checks. The draft readings it corrects (the 0x71 particle burst, the cloth solver, `00542740` building the edge geometry) were never published, so they have no consumers. The second joins action rows to magic-effect files; its positive controls are the name-bank entries Cure / Blindna / Vox / Belias / Zodiark. Both were re-run before this line and their outputs are unchanged. They read two scratch files outside the publish: `disw.py` (gi10names) and `gi-scratch/effects/type_census_files.tsv`.

run: gi10_cores_check.py at ed127d443 (HEAD when it ran), 139 checks pass, FAILS 0 (output: gi10_cores_check.out)

run: gi10names.py at ed127d443 (HEAD when it ran), 18 checks pass, FAILS 0 (output: gi10names.out)
