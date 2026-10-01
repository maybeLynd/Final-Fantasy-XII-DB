# Consumer-check record: battle-unit bit 46's clear is conditional, and the bit-30 arm never clears it (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`
affected: `Database/FFXII TZA/04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`
affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`

## What changed

The native command seam's phase-10 row said the non-bit-30 actions "clear bit 46", without a condition. The clear at
`00304F9F`–`00304FA9` runs only once `animationEventFlags` `+0x690` holds bits 1 and 3 (`00304F91`–`00304F9A`). The
bit-30 arm (`00304F62`–`00304F8C`) never clears the bit. The seam row gains that clause, as a narrowing with nothing
struck. The field map gains the bit-46 row, and the register gains FF-6 for the clear that is still unknown. Evidence:
[`README.md`](README.md).

## Consumers

- consumer: `07-Combat-Action/Command-And-Action-Seam/native-command-seam.md` phase-10 row: revised-here (narrowing clause).
- consumer: `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` register-mask table and §7: revised-here (row 46, box FF-6).
- consumer: `15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md` §10 ("bit 46 forces all-suppressed when
  reached", `0023B0D4`–`0023B0E9`): agrees. The test is on the party leader's flag qword (`0023B0E6`).
- consumer: request `DATA-REQ-FABLE-BATTLEUNIT-BIT46-0930` (SWE2-DATA's suggested row): revised-here. The row is published
  with the conditional clear and FF-6, rather than the suggested "phase 10 clears it".
- consumer: `_index/OPEN-QUESTIONS.md` section FF: revised-here (FF-6 added, OPEN, static).

## Regression

run: bit46_writers.py at 0fcf9349e (FAILS 0; control C0: the three page-cited sites are found)
run: bit46_regindex.py at 0fcf9349e (FAILS 0; control: the synthetic register-index shift is found)
