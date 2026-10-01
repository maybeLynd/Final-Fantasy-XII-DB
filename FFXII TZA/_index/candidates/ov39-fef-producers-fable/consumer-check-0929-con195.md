# Consumer-check record: OV-39's configuration clause after CON-195 (FABLE, Claude Opus 5.5, 2026-09-29)

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`
affected: `Database/FFXII TZA/_index/candidates/ov39-fef-producers-fable/README.md`
affected: `Database/FFXII TZA/_index/candidates/ov39-fef-producers-fable/producers.py`

## What changed

OPUS's CON-195 (`35321544f`; record `../fef-falsification-pass-1-0929/README.md`) established that the table `02B64380` is
seeded at start-up. FABLE re-read the chain before restating:
- `00409F80` is `sub rsp, 0x28; call 0040A230 (00409F84); add rsp, 0x28; jmp 0051FB70`;
- `0040A230` (size `0x7E1`) is a straight run of `lea rax, [rip+X]; mov [rip+Y], rax` pairs that ends at `0040AA10 ret`.
  Every X is an `.rdata` string and every Y lies between `02C65BF0` and `02C83C78`.

The regression `falsify_fef_entries.py` checks the rest (F3-F5):
- the start-up link `0041E3A0` -> `00409F80` (`0041E40B`);
- that the 144 stored paths are `obj_finish` entries of the installed archive;
- that the stored values are `.rdata` strings.

FABLE's OV-39 answer (register row, and this record's "optional configuration" row) had said the table "is never
populated" and that `0040A230` was dead-stripped. That clause is corrected:
- the configuration input has a start-up producer;
- the NULL-row fault at `0040A135` does not follow.

## Consumers

- consumer: `_index/OPEN-QUESTIONS.md` row OV-39: revised-here. A dated correction is appended to the cell. The row
  stays ANSWERED, because the rest of the answer is unchanged:
  - the @FRP names and OV-26's offset tables are guaranteed by census;
  - the 144 `obj_finish` `.cm` files' end-of-extent dword never locates their EFX data (`producers.py`).
- consumer: this record's `README.md`, row "optional configuration": revised-here. The old text is struck and replaced.
- consumer: `producers.py`: revised-here. Its docstring repeated the clause, and a CORRECTED line was added. The script
  does not test the configuration input.
- consumer: `02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md`, the OV-39 box:
  agrees. OPUS already revised it (`falsify_nonempty_prf.py` R6, `5e5fee584`); not touched here.
- consumer: UQ-218 (SWE2-DATA): agrees. It consumes CON-195 in `uq218-pass18-0930`, per OPUS's notice; not touched here.

## Regression

run: falsify_fef_entries.py at 73204a188 (FABLE's re-run: F1-F5 SURVIVES, FAILS 0; F3 = the start-up chain this restatement rests on)
