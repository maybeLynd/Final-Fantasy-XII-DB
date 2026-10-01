# Access direction repair — evidence (OPUS, 2026-09-24)

Goal priority 1: *"The audited access index contains 238 reversed read/write labels."* This
directory is the measurement behind the repair. Evidence class: **NATIVE/STATIC** (shipping image
`73461D08…21F8`, decoded twice by independent decoders). Nothing here is live or replayed.

## What was wrong, measured

`field-access-index.tsv` (F-6, published at `37ba899ea`) has **exactly 238 rows with a reversed
direction** — `field-access-index-238-reversed.tsv`:

| rows | instruction | published | correct | cause |
|---:|---|---|---|---|
| 198 | `movups xmmword ptr [m], xmm` | `r` | `w` | capstone 5.0.7 flags the STORE form's memory operand READ |
| 40 | `test byte/word ptr [m], reg` | `w` | `r` | capstone gives the operand NO flag; `op_kind` fell back to "operand 0 is written" |

Both are in `reg_tracking.op_kind`, the kit's one shared classifier. The whole-image control
(`gfz-scripts/opkind_vs_iced.py`, iced-x86 1.21 as the second decoder, loaded from a scratch path — not a
kit dependency) found the full defect class, `opkind-vs-iced-before.tsv`:

| memory operands | disagreeing | classes |
|---:|---:|---|
| 728,535 | 23,260 | movups 13,816 st→r · nop 8,663 · test 477 →w · movq 206 · lock cmpxchg 30 (rw→r) · movhps 27 · movd 13 · movhpd/movlpd 12 · prefetch 5 · vmov* 6 · setcc 5 |

and the register side that decides **receiver overwrite** (`gfz-scripts/regwrites_vs_iced.py`, 1,775,860
instructions): 1,269 disagreements — `lock cmpxchg` never killed `rax` (30, the dangerous
direction: accesses credited to an object the register no longer holds), `cdq`/`cqo` killed `rax`
(1,031) and `test eax, imm` killed `rax` (208).

## The repair

* `reg_tracking.op_kind` consults SDM-grounded mnemonic tables first (compares read, atomic
  exchanges read-modify-write, pure moves write operand 0 and read elsewhere, lea/nop/prefetch
  touch nothing); capstone flags only after; an operand with no flag is `?`, never a guess.
* `reg_tracking.written` corrects cmpxchg / cmpxchg8b/16b / cdq/cqo/cwd / test.
* **After: 0 / 728,535 and 0 / 1,775,860 disagreements.**
* `test_reg_tracking.py` pins positive (13 store forms), negative (10 read forms incl. the three
  unflagged `test` shapes), RMW (6), LEA/nop/prefetch, string-op and receiver-overwrite controls.
  **Run against the pre-repair module it fails 20 subtests; after, 12/12 pass.**
* Eight OPUS producers that hand-rolled `"w" if operand 0 else "r"` now call `op_kind`, and
  `gen_static_census.py` no longer truncates the refs file's kind (it turned `addr` into `r` and
  `rw` into `r`). Regenerating `mt19937-state-accesses.tsv` with the repaired producer is
  **byte-identical** to the relabelled committed file.

## Effect

* **Field-access index, HEAD inputs, same producer, only the classifier changed**
  (`field-access-index-flips-on-head-inputs.tsv`): 20,150 rows → 20,150 rows, **240 flipped**
  (200 movups `r→w`, 40 test `w→r`), zero added, zero lost, 34 types. The index file itself is
  NOT regenerated here — it is FRONTIER's F-6 artifact and a peer has uncommitted edits in its
  producer; routed.
* **The published index is not reproducible from its committed inputs**: the pre-repair producer on
  HEAD `types.tsv`/`fields.tsv` gives 226 types / 20,150 rows against the published 228 / 20,011
  (5 types differ: AchievementState, ImageBackedStateBlock, IndexedExternalSourceRequest,
  PApplication, VmValueStack). Cause NOT established; routed to FRONTIER as a provenance question.
* **Per-type access artifacts**: `gfz-scripts/relabel_access_kinds.py` re-decodes each row's own site (no
  row added or dropped; a row whose instruction text does not match its site is left and
  reported). 80 artifacts, 23,257 rows unchanged, **297 changed**, 4 MISMATCH (all in
  `spawn-group-ledger-accesses.tsv`, sites and instructions swapped pairwise — STRUCT).
  **Applied to the 18 OPUS-owned artifacts only: 195 cells** (`relabel-opus-applied.tsv`, every
  preimage kept; a second pass changes 0). Peer-owned artifacts get exact patches:
  `relabel-patch-for-{SWE2-AUDIT-SPEC,SWE2-STRUCT,FABLE}.tsv`.
* **Register kills in the F-6 producer.** `gen_route_seeded_census.py` calls capstone's
  `regs_access()` directly, not `reg_tracking.written`, so it still carries the three kill
  defects. Measured by running it on HEAD inputs with `regs_access` wrapped to apply the same
  three corrections (1,884 applications: cdq 1,155, test 725, cmpxchg 4): **0 rows gained, 0
  lost.** Inert for this producer on this domain; it is NOT a statement about
  `receiver_flow_census.py` or `census_receiver_fixpoint.py`, which also call `regs_access()`
  and were not measured.
* **Writer sets** (`writer-set-changes.tsv`): 84 (artifact, disp) pairs change writer status —
  79 gain their FIRST writer, 5 lose their ONLY one (it was a `cmp`/`test`).
* **`rip_data_refs.tsv` → `global_refs`** (DATA's producer, `rip-data-refs-vs-iced.tsv`): of
  164,489 rows, **4,040 stores are recorded `read`** (movups 4,013, movq 26, setns 1) and **19
  `lock cmpxchg` are `read`**; 1,100 RMW are `write` (right for a writer query, class lost); 68
  `test` are `other`. Every "writer of a global" query misses those 4,059 sites. Routed.
* **Published text that rested on the labels** (`fields-zero-written-contradicted.tsv`): 50
  `fields.tsv` rows say "N access(es), 0 written" while a corrected source shows a writing site.
  **13 of them are this defect** (21 sites, all `movups` stores: BattleMenuPanelWidget3010 ×11,
  MapScreenContainer +0x190/+0x1A0, WidgetSingleton02CA99C0 +0x108). **37 are NOT** — the index
  already had a plain `mov` writer there, so the text is older than the index. Both routed to the
  `fields.tsv` claim holder; neither is edited here.
* **One declared lifetime claim is refuted by the image.** CharacterRenderObject `+0x644`
  (`simd0644`) says *"allocated unzeroed, never cleared, never written individually"*. Vtable
  slot 9, `001F9A80`: `mov rbx, rcx` at `001F9A8D`; `call 00189120` (a two-instruction global
  getter, `rbx` preserved); `cmp byte ptr [rax+0x1c], 0` at `001F9AFF`; `je` → `001F9B12
  movups xmmword ptr [rbx+0x644], xmm0`, else `001F9B05 movups [rbx+0x654]`. The field is
  written, conditionally, by the object's own method. `character-render-object.md` already lists
  `+0x644, +0x654 slot 9`; only the `fields.tsv` evidence is wrong.

## What is NOT claimed

A direction label is width-and-direction evidence only. Nothing here promotes a meaning, and a
field gaining a writer says nothing about what it holds. The whole-image counts are over the
bodies listed in `work/graph/functions.tsv` (≤ 0x20000 bytes each); unlisted code is outside the
measured domain, so "0 disagreements" is a statement about that domain only.

## Addendum 2026-09-25 (OPUS, block 222): the fields.tsv rows are corrected

**All 50 `fields.tsv` rows are corrected by an appended note** (the original text is kept). They are
listed in `fields-zero-written-contradicted.tsv`, and every one is OPUS-authored text. Each of the 67
cited sites was re-decoded with the repaired `reg_tracking.op_kind`, and all 67 are stores (`w`):

- **55** store at exactly the field's displacement.
- **12** reach it through a derived base that the field-access index tracks. They are marked
  "receiver-tracked, not re-derived here".

The `CharacterRenderObject +0x644` LIFETIME note is corrected in part:

- **Withdrawn:** "never written individually / never read". Slot 9 `001F9A80` stores the field
  conditionally at `001F9B12`.
- **Stands:** "allocated unzeroed, no memset".

**Still routed:** DATA's `global_refs` direction (4,059 sites) and `gen_array_census` onto
`op_kind`; AUDIT-SPEC's five-census relabel and its review of this repair.
