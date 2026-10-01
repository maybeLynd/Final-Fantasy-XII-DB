# Audit-spec review: OV-33 E2 — six FST cache keys collide with no archive name

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject:
`work/ASTRA/runtime-residue-method-retriage/ov33-e2-six-cache-keys-frozen-ready`
Board task: `ASTRA-REQ-SPEC-OV33-E2-SIX-CACHE-KEYS-0930`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-ov33-e2-six-cache-keys.py` →
  `NO_COLLISION_IN_COMPLETE_RETAINED_ARCHIVE_NAME_DOMAIN` — 6 selected paths,
  89,414 archive names, 0 candidate collisions, **positive detector valid**.
- **The 89,414 count cross-confirms an earlier independent check**: this lane
  re-ran ASTRA's `a17-vbf-archive-index-check.py` against the installed archive
  and the dashboard listing and found INDEX_MATCH at 89,414 entries (S78
  shadow review) — the domain the collision test runs over is the complete
  verified name table, not a sample.
- **Negative with a real control.** The run reports the positive detector valid
  (a forced-collision case is caught), so the 0-collision result is a true
  negative, not a broken comparison — satisfies the absent-evidence rule.
- **Scope.** The claim is bounded to the six retained FABLE FST-sized
  missing-kind-1 paths (US129/130/131, UK131/132, CN127, both edx modes)
  against the archive-name key domain; no availability/loader-behaviour claim.
  `674A00`'s 40B recurrence/normal-CFG was re-decoded through the shared
  adapter rather than re-derived by me; the collision claim itself, which is
  the verdict's load-bearing fact, does reproduce.

## Narrowing / notes

None required.
