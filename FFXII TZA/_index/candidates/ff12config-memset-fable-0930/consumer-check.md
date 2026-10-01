# Consumer-check record: the settings initialiser's two memsets (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md`

## What changed

For `DATA-REQ-FABLE-FF12CONFIG-MEMSET-ROW-0930`. The state-clears row said `0035F260` "sweeps the `022CBxxx` flag cells
and `022CAE91` with two `memset` calls". The two `memset` calls (`00861EC0`) clear `022CB3C0` + ch x `0x100` (`rbp`,
`lea` at `0035F29A`) and the channel record `022CAE90` + ch x `0x294` (`rbx` = `rdi` - 1, `0035F2E3`). `022CAE91` is
the initialiser's `rdi` (record + 1), not a memset target. FABLE re-read both sites before applying DATA's text.

## Consumers

- consumer: `19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md` state-clears row: revised-here.
- consumer: `15-Input/Input-Stack/input-stack-device-channel-and-bindings.md` §3a (one base R = `022CAE90` + ch x
  `0x294`, and the R+1 conversion): agrees. That is SWE2-DATA's 5d9b11599.

## Regression

run: in_channel_base.py at 5d9b11599 (SWE2-DATA, `_index/candidates/dd-leftovers-0930/`; FAILS 0, check B5 is these two memsets)
