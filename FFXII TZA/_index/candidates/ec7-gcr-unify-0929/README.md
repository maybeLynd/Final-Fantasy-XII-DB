# Guarded class-registration stubs unified into one family, 2026-09-30 (SWE2-EC7)

This package executes FABLE's ruling [`fable-gcr-split-ruling-0929`](../fable-gcr-split-ruling-0929/README.md)
(`e862a1dae`) under request `FABLE-REQ-EC7-GCR-UNIFY-0929`. The ruling makes "guarded class-registration stubs" one
family. The old orchestrator/stub split becomes an information column. The family admits exactly the frontier bodies
that the unified selector admits, and any drops are reported separately.

## What changed

- **Selector.** `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/select_guarded_class_registrars.py`
  now writes one TSV, `guarded-class-registration-stubs.tsv`.
  - The membership fixpoint is unchanged: seeds, shared-machinery control, rules 1-3 and the census-wide
    self-bounding check.
  - A last column lists the auxiliary callees that are themselves of the guarded form. This is the ruling's `GUARDED`
    set: census bodies that call `_Init_thread_header`, `_Init_thread_footer` and `atexit`, whoever owns them.
  - The retired orchestrators file is still read as a seed source if present, and is never written.
- **Members.** `guarded-class-registration-orchestrators.tsv` is deleted, and its 25 members are in the unified file.
- **Rows** on `class-descriptor-and-metadata-system.md`.
  - The "guarded class-registration stubs" row goes from 72 to 99. Its note loses the "leaf bodies" wording and ends
    with a dated sentence naming the retired row "guarded class-registration orchestrators" as history.
  - The orchestrators row is removed.
- **Page wording.** Three body sentences used "orchestrator" as a kind of code, and each now states the call fact:
  - the decomposition summary ("76 leaves + 26 orchestrators");
  - "a dozen guarded orchestrators whose private aux targets...";
  - "`006343E0` ... is an orchestrator aux target".

## Membership: 97 -> 99, admitted 2, dropped 0

The unified selector's output (`selector-after-write.txt`) holds 99 members. That is every one of the 97 members of the
two old rows (72 + 25), plus the two frontier bodies withheld on 2026-09-29: `00676A70` (337 B) and `005EFE60` (839 B).
**It drops none.** Census predicate hits are 486, and there are 0 free twins. The information column is non-empty for
76 of the 99, against 525 guarded-form bodies in the census. This equals the form-based split in FABLE's
`form_split.out` (23 / 76), so the column reproduces the ruling's own measurement.

**Controls.**
- The unchanged committed selector's dry run (`selector-before-dry-run.txt`) gives the same 99 members, split 76 / 23,
  which is the ruling's control figure. So the edit changed only the output shape.
- On a **clean extract of HEAD `2c840bfe4`** the edited selector writes a byte-identical TSV
  (`selector-head-extract.txt`), so no member depends on a peer's uncommitted page.

## Gates

- `check_dispositions`: the row is accepted at 99, and the self-test passes all 13 cases.
- `check_family_forms`: 0 MISMATCH.
- `check_family_spans`: rc 0.
- `verify_doc_addresses` on the page: nothing to confirm.

**Not touched.** `_index/ADDRESS-INDEX.md` still names the retired TSV in its "table only" listings. It is generated,
and it updates on its generator's next run. `_index/PROGRAM-STATE.md` line ~6293 ("stubs x76 + orchestrators x28") is a
dated checkpoint in a history log, so it is left as written.

**Review:** T2, a family change. SWE2-AUDIT-SEM audits it, and the `reviews` field is set.
