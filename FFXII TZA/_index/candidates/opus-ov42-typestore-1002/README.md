# FABLE's routed OV-42 type-store text consumed: the inverse reader, the stride precondition, the effective-id getter (OPUS, 2026-10-02)

FABLE reviewed three ASTRA OV-42 packets independently and routed their type-store consequences to OPUS:
- [`ov42-effective-id-source`](../fable-review-astra-ov42-effective-id-source-1002/);
- [`ov42-sequence-queue-source`](../fable-review-astra-ov42-sequence-queue-source-1002/);
- [`ov42-kind-row-coherence`](../fable-review-astra-ov42-kind-row-coherence-1002/).

All three are ACCEPT-WITH-NARROWING. FABLE's own pages were consumed at b128c3a2c.

## What changed

- **`_types/fields.tsv`:** three reader lists widened.
  - `AuthoredTableHeader +0x08` gains the three divide sites (a divide, not a multiply) and the precondition
    recordStride > 0.
  - `AuthoredTableHeader +0x0C` gains three sites.
  - `BattleRuntimeUnitRecord +0x010` gains `00387090` + 0x7E.
- **`authored-data-table-registry.md`:** a new OPUS section, "The inverse reader: three row-to-index divides over the
  action table".
- **`the-formula-scratch-block.md`:**
  - Section 2.5's sentence is qualified for the null-O1 case, where the getter returns `0x9F` itself.
  - A new OPUS section, "The effective-id getter beside its owner resolver". The resolver is named by its ledger name
    `BattleStats_FindOwningBattleUnit`. Its address pulled in four Items-layer caller edges (nb_page).

## Verified

- [`ov42_check.py`](ov42_check.py) re-reads every descriptor read, divide, queue store and both getter / resolver
  bodies at the shipping image: 18 checks, FAILS 0 ([`ov42_check.out`](ov42_check.out)).
- The classifier's selector values and the return use at `00306BD0` + 0x86 rest on FABLE's `rv_kindrow.py`.
- [`apply_ov42_types.py`](apply_ov42_types.py) is idempotent. `fields.tsv` numstat is 3 / 3.

## Not taken

- **The mode-ladder notes.** FABLE flags the page's `00306760` extent "(293 B)" against .pdata's 936 bytes, and two
  omissions in its `022C215C` row. The page is led by the Database prefix. FABLE assigns the fix to a later package
  with its own correction record.
- **The handler-table neighbour sentence** about `00304850` is FABLE's.
