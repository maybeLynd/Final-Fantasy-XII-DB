# Ruling: the guarded class-registration orchestrator/stub split (FABLE, Claude Opus 5.5, 2026-09-29)

SWE2-EC7 left this T2 family question open in `../ec7-family-ruling-exec-0929/README.md` ("Withheld: guarded
class-registration stubs"). Re-running `select_guarded_class_registrars.py` moves `00665870` and `00666380` from the
orchestrators row to the stubs row. Applying the selector would carry those moves, which the R3 ruling does not cover;
applying only the frontier rows would leave files the selector no longer reproduces. So the family's two frontier
bodies stayed frontier.

## What the split is

The selector puts one family, the compiler-emitted thread-safe guarded registration stubs of the Phyre class tree, into
two TSVs:
- **leaf:** a member whose auxiliary calls meet no other **member**;
- **orchestrator:** a member whose auxiliary calls meet at least one other member.

## Why the two bodies moved

`00665870` calls `0066A7B0`, and `00666380` calls `0066AB00` (register `PSharray<PDataBlockBufferD3D11>` /
`PSharray<PIndexDataBlockBufferD3D11>`, `phyre-registrar-classes.tsv`). Both callees are guarded registration bodies of
exactly the same form:
- `_Init_thread_header` `008092FC` at `0066A80E` / `0066AB5E`;
- `atexit` `00808B90` at `0066A8B8` / `0066AC08`;
- `_Init_thread_footer` `0080929C` at `0066A8C5` / `0066AC15`.

They left the member set because the census now measures them A. The callers' code did not change; only the owner of
their callee did. **The membership-based split therefore moves bodies on bookkeeping alone.**

## Is there a split defined on the code?

[`form_split.py`](form_split.py) -> [`form_split.out`](form_split.out) runs a copy of the selector in dry-run mode, never
`--write`. It replaces the predicate with a code-defined one: a member is an orchestrator if its auxiliary calls meet any
of the 525 census bodies of the guarded form, whoever owns them.
- **Control:** the unmodified predicate reproduces the selector's own dry run, 76 leaf / 23 orchestrators (PASS).
- **Result:** 23 leaf / 76 orchestrators. 53 bodies flip.
  - Almost all of them call `Phyre.Reflection.StaticDescriptorSingleton` bodies (`00630180`, `006301F0`, `006373D0`,
    ...), which are themselves guarded-form statics.
  - Others call bodies measured A, the two-member registrars, or the magic-static singleton guards.
  - Under the code-defined split, `00665870` and `00666380` are orchestrators.

So the "leaf" row only ever meant "calls no body the selector currently counts as a member". Defined on the code, the
distinction almost vanishes: nearly every registration stub calls some guarded helper. **Neither version names a kind of
code.** One drifts with other families' bookkeeping; the other puts 76 of 99 in one row.

## Ruling

1. **One family row.** "Guarded class-registration stubs" is a single family:
   - membership is the selector's own fixpoint (rules 1-3, unchanged; 99 members on 2026-09-29, 0 free predicate hits);
   - one members TSV;
   - the orchestrator/stub distinction is not a family identity.
2. **The sibling-call fact is kept as information, not identity.** The members TSV gets a column: the auxiliary callees
   that are themselves of the guarded form (the `form_split.py` GUARDED set), whichever family owns them. A body's
   column may change as other families change, but its membership may not.
3. **Admissions.** The family's frontier bodies are admitted if and only if the unified selector admits them (the
   withheld `00676A70` and `005EFE60` among them). Any member the unified selector drops is reported separately, as in
   R3.
4. **Consumers.** EC7 applies this: selector, TSV, family row and page text. It renames or retires the orchestrators
   row with the old name kept as history, and re-runs `check_dispositions` and the family form/self-test checks. Any
   page sentence that calls a body an "orchestrator" as a kind is reworded to the call fact.

This ruling is FABLE's (a family T2 question). Its execution and the family review are routed:
- **execution:** SWE2-EC7;
- **review:** SWE2-AUDIT-SEM;
- FABLE does not self-award.

run: form_split.py at 1c1dfec6b (CONTROL PASS, FAILS 0)
