# SWE2-AUDIT-SEM re-score: S-31 types PARTIAL -> MET, L2 NOT MET -> MET

SWE2-AUDIT-SEM (Claude stand-in for the rate-limited Devin session) · 2026-10-03 · Closes the S-31 residual of `auditsem-types-rescore-2-1003` and part 2b of `AUDITSEM-REQ-AUDITSPEC-CENSUS2-BLINDSPOT-AND-RULES-1003`

## SWE2-AUDIT-SEM what changed

- **The rule.** OPUS ruled on rule (b) in `51ad88762` (record `opus-s31-licence-node-1003`): a contract section belongs
  in the types denominator by content, whatever its heading. S-31's §8a.2 therefore counts, and S-31 was correctly
  PARTIAL.
- **The declaration.** In the same commit OPUS declared the five node-table fields §8a.2 names on
  `LicenseNodeRecord`:
  - `+0x004` lpCost uint8;
  - `+0x005` category uint8;
  - `+0x006` squareKind uint8;
  - `+0x007` startMask uint8;
  - `+0x008` ids u16[8].
- The previous re-score's cell said "MET when the five fields are declared". That condition now holds.

## SWE2-AUDIT-SEM checks

- I re-read two of OPUS's evidence sites at the bytes:
  - `003239C3 movzx ecx, byte [rcx+4]`, then `neg ecx` against dword `+0x190`: the LP cost subtracted from the
    character's licence points.
  - `0023AE61`-`0023AE68 mov edx, 1` / `shl edx, cl` / `test byte [r8+7], dl`: the start mask tested one bit per slot.
- `+0x000`..`+0x003` stays an exact-extent unobserved span. The contract names nothing there, so rule (a) and its
  condition (FABLE, `auditspec-rules-review-exact-extent-1003`) do not apply.
- The shared reader `l2_verdict_table.py` reads S-31 as **MET** after the edit, with no malformed rows. The L2 count is
  **33 of 52**.
- The edit is column-precise (`Tools/work/SWE2-AUDIT-SEM/standin1003/apply_s31.py`). Only text that is really in each
  cell is struck, and the new verdict follows it. The edit touches the types, L2 and binding-gap cells.

## SWE2-AUDIT-SEM advisory

The type's instance column still describes 360 records in `license_data.bin`, where the contract says the game loads
361. This is a quality note on the instance description, not a declaration gap. It is routed to the type store's owner
as a note and does not block MET.

## SWE2-AUDIT-SEM limits

Static only. Rules (a) and (b) are now both settled: (a) by FABLE, (b) by OPUS.
