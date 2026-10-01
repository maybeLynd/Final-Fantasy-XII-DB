# Audit-spec review: OPUS pass-7 tier assignments (71141fdc0)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: commit `71141fdc0`
Board task: `OPUS-REQ-AUDITSPEC-PASS7-TIERS-0930`

## Verdict: ACCEPT

## What was checked

- **Tier vocabulary** (EVIDENCE-STANDARD): tier 1 = complete exact-current
  function body; tier 2 = authored/runtime strings tied to the body or its
  data; tier 10 = runtime evidence.
- **`CONTRACT-experience-and-licence-award.md`** — 8 rows:
  - 7 rows rest on original-body reads (`002F8C34..002F8D24`,
    `002F8BDE` vs `002F90C0..002F9173`, `+0x34`/`+0x2F` loads, `002F8CD8`/
    `002F8CE2`, `002367A0`, `0023A965..0023A9FB` + `0020E600`,
    `003124B4..0031251D`) plus named native controls/mutants — **tier 1 earned**.
  - The "Cached reward pointers" row rests on parsing EXP-081's captured raw
    spans — runtime-captured data → **tier 10 correctly assigned**, not tier 1
    (the claim's support is a live capture, even though the parse is static).
- **`phyre-class-instance-sizes-and-alignments.md`** — 6 rows:
  - four rows are pure body/scan claims (registrar fields `00632D80`/
    `00632C90`, `+0x30` name readers `006388C0`/`PObjectAccessor`, six list
    heads, destructor operands) → **tier 1 earned**.
  - the sizes↔classes row is a body read joined to class-name `lea` strings →
    **1, 2 correct**.
  - the Phyre-own-names row is string-located (179 NUL-terminated leaf names)
    → **tier 2 correct**.
- `check_tier_presence` effect: MISSING 0, untiered rows 0 as claimed by the
  commit message (spot-consistent with the tables now present).

## Narrowing / notes

None required.
