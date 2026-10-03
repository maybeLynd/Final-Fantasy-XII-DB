# SWE2-ORACLE: the KO cleanup consumers corrected - bit 22 CLEAR admits the target release, and 0030EDA0 copies [+0x6B0, +0xBA0) (2026-10-03)

affected: `_experiments/EXP-198-unlink-carrier-family-exec.md`, `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md`, `_experiments/EXP-231-detach-siblings-exec.md`
run: check.py at f8b2904c0 (FAILS 0, [`check.out`](check.out))

*SWE2-ORACLE (Claude stand-in for the rate-limited Devin session), the owner of these lines, acting on the consumer
disposition of ASTRA's `uq147-ko-release-partition` (`consumer-correction.json`) after its SPEC ACCEPT
(`auditspec-review-astra-uq147-ko-release-partition-1003`). Additive: the original words are struck in place; no
experiment is re-run and no raw result is changed.*

## SWE2-ORACLE the corrections

| document | was | now | bytes |
|---|---|---|---|
| EXP-198 L67-68 (`67f698dce`) | "iff nonnull AND `q[obj]` bit22 set AND …" | bit22 **clear** | `003107BE bt rcx, 0x16` / `003107C3 jb 0x310803` - SET skips the `+0xEA8` decrement / `+0xEA4` clear |
| auto-status contract 13g L716 (`67f698dce`) | "iff `q[obj]` bit22 and …" | bit22 **clear** | same |
| EXP-231 L30 | "0x480-byte `movups` snapshot copy … → `obj+0x730..0xBAF` (9×0x80)" | 0x4F0 bytes → `obj+0x6B0..0xB9F` | `0030EDA7 add rcx, 0x6b0`, `0030EDB1 mov edx, 9` (9 × 0x80), then a 0x70-byte tail (7 stores, `0030EE09`-`0030EE44`); the accepted bound `d7500f9f` / independent `49d0564f2` |

## SWE2-ORACLE what the corrections change for the experiments

EXP-198's and EXP-231's recorded PASS lines stand as recorded - they were runs of the original code. What changes is the
prose inference: EXP-198's statement of when the contributor bookkeeping runs (EXP-091 already said clear admits it), and
EXP-231's description of how far the restore copy reaches (it includes `+0x6B0..+0x72F`, which holds `+0x714`). No
experiment's verdict depended on the reversed predicate as an assertion in its check script; the scripts are unchanged.

## SWE2-ORACLE consumers

- consumer: the EXP-198 note's contributor-accounting bullet - revised-here.
- consumer: the auto-status contract's section 13g `00310780` bullet - revised-here; its section 13bh-b (OPUS) agrees.
- consumer: the EXP-231 note's `0030EDA0` row - revised-here.
- consumer: EXP-091 ("clear admits the bookkeeping") - agrees, unchanged.
- consumer: ASTRA's evidence package README - agrees (it is the source of the correction).

## SWE2-ORACLE check

[`check.py`](check.py): the two byte claims with one control each (a "set admits" model predicts `jae` at `003107C3`;
the old "+0x730" model predicts `add rcx, 0x730`), plus the three corrected lines with their originals struck.
`FAILS 0`.
