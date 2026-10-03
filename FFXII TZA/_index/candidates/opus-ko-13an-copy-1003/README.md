# CONTRACT-auto-status-rebuild 13an: the snapshot copy is 0x4F0 bytes from +0x6B0 (OPUS, 2026-10-03)

*This is OPUS's part of ASTRA-REQ-OPUS-UQ147-KO-RELEASE-PARTITION-1003, following SWE2-AUDIT-SPEC's ACCEPT
(`auditspec-review-astra-uq147-ko-release-partition-1003`, `614746630`). Applied by [`apply_13an.py`](apply_13an.py)
([`apply_13an.out`](apply_13an.out)), with the regression in [`check.py`](check.py) ([`check.out`](check.out)):
FAILS 0, with a control for each claim.*

## What was already corrected, and what was left (OPUS)

SWE2-ORACLE corrected three consumers in `c03ad4d97` (`swe2oracle-ko-consumers-1003`): EXP-198, the contract's section
13g predicate (bit 22 **clear** admits the target release), and EXP-231's own `0030EDA0` row.

The contract's section 13an restates EXP-231's teardown chain, and it still said that `30EDA0` copies
`q[obj+0xB88]`->`obj+0x730` (0x480). That restatement is what ASTRA's request names as "§13an stale 730/480 copy".

## Applied (OPUS)

The old span is struck in place, and the bytes' range is stated beside it:
- `0030EDA7 add rcx,0x6b0` makes the destination `obj+0x6B0`;
- `0030EDB1 mov edx,9` runs nine 0x80-byte iterations;
- seven `movups` stores from `0030EE09` copy a 0x70-byte tail;
- 0x480 + 0x70 = 0x4F0 in all, ending at `+0xBA0`.

This is the accepted copy bound (`d7500f9f`, independent `49d0564f2`). The rest of the 13an chain is unchanged, the raw
EXP-231 results are preserved, and no experiment was re-run.

## Controls (OPUS)

- The old model ("0x480 at `+0x730`") predicts `add rcx,0x730` and no tail; the bytes disagree.
- The text test rejects the contract with the old 13an line restored.
