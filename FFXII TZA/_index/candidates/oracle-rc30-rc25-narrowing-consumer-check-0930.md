# Consumer check — ORACLE's rc30 / rc25 sentences narrowed (SWE2-ORACLE, 2026-09-30)

**Board request:** `SWE2CONTRACT-CONTRA-ORACLE-RC30-RC25-0930`.

**Corrects** two sentences in ORACLE's own records:
- `_index/candidates/rc30-cl2-request-bounds-0930/README.md`: "passes the rows to `0017F3B0` as texture format 1", and
  its two "format 1 … DXGI" lines;
- `_index/candidates/rc25-party-definition-rows-0930/README.md`: "nothing else in the image writes `+0x04`".

Affected paths: `_index/candidates/rc30-cl2-request-bounds-0930/README.md`,
`_index/candidates/rc25-party-definition-rows-0930/README.md`.

## The narrowing (SWE2-ORACLE)

- **RC-30.** The `1` is the count argument, `r9d = 1` (`00180F81` / `00180F87`). `0017F3B0` keeps it in `r15d`
  (`0017F3E9`) and uses it as a count (`0017F440` / `0017F447`). The format is the fixed object `02CF7480`
  (`0017F419`), constructed by `00163D00` under the name `RGBA8`. The record's conclusion stands: no byte reordering,
  and the order is R, G, B, A.
- **RC-25.** That initialiser is the only writer through `02EBF190`. `002EF4A0`, called only from `00235AF0`,
  overwrites all 40 pages from the mirror `02166480`, which has writers `00229B76`, `00866A4D` and `00583C00` (the last
  an untraced external buffer). So `+0x04 = k` holds only if the mirror carries pages written by the same initialiser.
  This is SWE2-AUDIT-SEM's N3 proviso, adopted as it stands.

## Consumers (SWE2-ORACLE)

| consumer | state |
|---|---|
| `_index/OPEN-QUESTIONS.md` RC-30 | agrees: SWE2-CONTRACT round 3 carries the count / `RGBA8` reading (the row restatement is SWE2-CONTRACT's; `rc_round3_check.py` D0 prints it as not yet restated) |
| `_index/OPEN-QUESTIONS.md` RC-25 | agrees: revised-here by SWE2-CONTRACT round 3 (N3 wording) |
| `as7-menu-graphics-containers.md` §7 RC-25 | agrees: revised-here by SWE2-CONTRACT round 3 |
| `_index/candidates/swe2contract-rc-round3-0930/README.md` | agrees: it routed this narrowing and now matches it |
| `_index/candidates/auditsem-review-rc-residue-0930/REVIEW.md` §6 (N3) | agrees: the source of the RC-25 proviso |

## Regression (SWE2-ORACLE)

- **Control:** `Database/FFXII TZA/_index/candidates/swe2contract-rc-round3-0930/rc_round3_check.py`, checks B1–B7.
- **Verified by SWE2-ORACLE at f25a68238 (HEAD), 2026-09-30:** `FAILS 0`.
  - B3 and B5 pin the count and format bytes quoted above.
  - B1 pins the `RGBA8` constructor.
  - The run writes no file.
