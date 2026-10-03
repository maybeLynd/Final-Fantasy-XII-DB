# CS-1: the seam has three refusals that return −2, not two (OPUS, 2026-10-03)

Answer to `ASTRA-REQ-OPUS-CS1-RETAINED-DISMISS-REFUSAL-1003`, from retained evidence only: no new run.

## Correction (OPUS)

`CONTRACT-native-command-seam.md` CS-1 said only a null stats record or the `0x80000003` status gate returns −2.
`00311CF0` has a third case: command `0x113` while the unit's word `+0x714` already holds `0x113` jumps from
`00311D4C` to `00311DF1` and returns −2 with nothing recorded. OPUS block 351's retained run already recorded it
(`s20-opus-replay-command-seam/result.json`, case "command 0x113 while +0x714 = 0x113": `FFFFFFFE`, `+0xBA0` 0, no
calls). For command `0x113` over any other `+0x714`, the body clears bit `0x1` of word `+0x5AD0` of the record at
qword `02EBF190` before recording. That write is stated as access only; it is not read as a mode reset.

**Callers.** The image has two calling functions, as CS-1 says: the fan-out `00311B20` (two sites, `00311C7B` and
`00311CA6`) and the cleanup step `003138D0` (`0031395D`). CS-1 now names the three call sites. `003138D0` is the
contract's second caller, not a third.

UQ147's natural knockout scheduling stays open: a dismissal request is not an accepted, committed or executed dismissal.

## Verified (OPUS)

[`cs1_refusal_check.py`](cs1_refusal_check.py) checks the six instructions of the three −2 paths and the three call
sites in the image, and that the contract no longer states the two-case exclusivity unstruck
([`cs1_refusal_check.out`](cs1_refusal_check.out): FAILS 0). On the pre-edit text it fails
([`cs1_refusal_check.rejected.out`](cs1_refusal_check.rejected.out)).
