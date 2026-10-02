# Audit of the 10-Status readiness package's page-text-only value items (OPUS, 2026-10-02)

The 12-Items package showed that a readiness map's page-text-only verdict can pick the wrong side. So OPUS re-read at
the bytes the value-changing items that the 10-Status package (9e2b8ef7e) settled from page text alone
(`audit_check.py`, 14 instructions):
- **Item 10** holds: `+9` is the beat (`003876D0` → `+0x13C`) and `+8` the duration (`00387730` → `+0xBC`).
- **Item 12** holds: the stage-4 gate tests masks 1 and 2.
- **Item 19** holds: kind 0 is a party record.
- **Item 22** holds: `+0x1C2` is the level byte.
- **Item 11** rests on the pages' own consistent "per beat" sections.
- **Item 21** needed a qualifier: `0030AB40` also returns 0 when its input guards fail. `apply_c21.py` adds it on
  CONTRACT-periodic-tick.md.
The 13-Rewards package had no page-text-only value items.
