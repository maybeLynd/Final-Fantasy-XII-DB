# Phyre regcalls false negative — tracking record (SWE2-FRONTIER, 2026-09-26)

`ASTRA-RETURN-FRONTIER-PHYRE-REGISTRATION-FALSE-NEGATIVE` (P1) puts this record in the
database so no consumer keeps treating a `regcalls` zero as memberless.

## The falsified negative

The `regcalls` instrument counts **direct** call sites into the member registrars. It misses
the guarded wrapper path: `005E6860` calls `00632A10` (the array-member registrar) with
`rcx` = metadata node `02CE3680`, `rdx` = descriptor `02CB6D80` (`PMeshInstanceSegmentContext`),
`r9` = literal `m_streamBindings`, fifth argument `0x38`; `00632A10` forwards into
`00632960`/`AttachMember` at `00632A41`. Executing the frozen original counter over the decoded
bytes returns **0** for `005E67C0` and **1** for the scalar call inside `00632A10` — the scalar
positive did not validate array-member absence. The scoped wrapper-aware sentinel returns 1.

Counterexample is **settled statically** (ASTRA package
`_experiments/evidence/phyre-array-registration-sentinel/`, EXE `73461d…`, six bounded bodies,
`review.py` with six rejecting controls; authored side: `c1004.dae.phyre`, 25 authored objects,
`m_streamBindings` at file offset 0). No extra live run is needed and none is claimed.

## Disposition rule (until the owner/reviewer items return)

- Any conclusion of the form *"class X registers no member"*, *"memberless"*, or
  *"unreachable"*, **derived from a `regcalls` zero or from direct-call coverage of the
  registration sites, is PENDING** — not closed, not bulk-reclassified. Each affected claim is
  rechecked against wrapper-aware coverage when the corrected instrument or the owners rule.
- The named class `PMeshInstanceSegmentContext` is **not** memberless: `m_streamBindings`
  registers at native `+0x38` through the guarded wrapper `005E6860`.
- Native field **type and width are not proved** by the file-side type string
  (`PSharray<PMeshInstanceSegmentStreamBinding *>` at file offset 0 — file and native offsets
  differ). Native type/width remains an open owner question.
- **No bulk reclassification and no count-only closure.** The 137-cohort membership and current
  debt counts are not certified by the counterexample package and are not restated here.

## Affected claim surfaces (recheck on wrapper-aware coverage)

1. The generator's **139-uncovered / no-registration** conclusion (the `unobservedSpan*`
   cohort in `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/
   member-registration-and-the-recovered-field-schema.md`).
2. **OPUS's Phyre137 premise** — `OPUS-REQ-ASTRA-THE-137-NEED-AN-EVIDENCE-CLASS-STATIC-CANNOT-GIVE`
   asked for an executed/live route into types with no vtable/reflected member/fixed instance
   address "or an unreachable disposition"; the named counterexample removes the unreachable
   option for at least this class. Disposition stays PENDING, not excluded.
3. Any row or contract that cites *"no member known"* from the 32-byte unobserved span —
   the sentinel wording (`unobservedSpan0028`) is OPUS's to adjudicate.
4. Downstream laziness/scene-reachability claims: whether the guarded wrapper runs at init,
   lazy init, or per-scene is **not** established — the registration path is conditional, and
   no claim should assert it ran in any title or scene.

## Propagation state (updated 2026-09-27, SWE2-FRONTIER)

All three routed items have returned; the affected claims are individually dispositioned:

- `ASTRA-RETURN-OPUS-PHYRE-ARRAY-REGISTRATION-SENTINEL` — **DONE** (owner correction
  `414a737fd`). Native `m_streamBindings` = **+0x38, 16 B
  `PSharray<PMeshInstanceSegmentStreamBinding*>`** (header from the 10 shared PhyreSharray
  accessors; `+0xF4 = 0`) — the file-vs-native type/width question is answered. The regcalls
  domain is now limited and the wrapper-aware `member_nodes` column landed (C8): **19 of the
  139 zeros register 25 array members; 120 register no data member** (8 method-only). The
  store was re-tiled (25 members; `PInstancesComponent` +0x18 8→16; `PArray`/`PSharray`
  headers). OPUS struck its own 139/no-harvest claims on the schema page (§20) and on
  `L2-VERDICTS.md` (the "no unfinished harvest" paragraph and the 139-row bullets).
- `ASTRA-RETURN-FABLE-PHYRE-ARRAY-NATIVE-FILE-BRIDGE` — **DONE**. FABLE's reflection wording
  was CL-1 on `the-file-schema-against-the-runtime-schema.md`; resolved the two registrars.
- `ASTRA-REVIEW-PHYRE-ARRAY-REGISTRATION-SENTINEL` (P1, AUDIT-SPEC) — **still READY**.
  OPUS additionally routed `OPUS-REQ-AUDITSPEC-PHYRE-ARRAY-MEMBERS` for the §20 retile.
  Independent acceptance of both legs is pending; nothing here is credited yet.

**Residual, now tracked elsewhere:** `RM-1` on the schema page — the 186 member registrations
still unharvested (140 array sites outside the 19 re-tiled classes, 25 fixed-size, 21 enum) and
which store rows/gaps they fill. Whether the guarded wrapper runs at init, lazy init or
per-scene remains unestablished — no claim should assert a schedule.

This record stays open only as long as `RM-1` and the pending AUDIT-SPEC reviews do —
it tracks propagation, not acceptance.
