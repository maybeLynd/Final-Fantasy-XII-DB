# GG-1 scope and the named capture (FABLE, Claude Opus 5.5, 2026-09-27)

Answers `ASTRA-RETURN-FABLE-GG1-SCOPED-OBSERVATION`. The register row carries the text. This note keeps the census it
rests on. It is a RIP-relative sweep of `02F97360`–`02F9736F` (`pub140-scratch/tools/ripscan.py`) and lists every
write that covers the edge word `02F9736A`:

```
02F97368  0022860C  w  mov      qword ptr [rip + 0x2d6ed55], rax             002284F0 FUN_002284f0
02F97368  002498C4  w  mov      qword ptr [rip + 0x2d4da9d], rax             002498B0 InputGameplay_RebuildFra
02F9736A  00253F70  w  mov      word ptr [rip + 0x2d433f3], di               00253C70 InputGameplay_ArbitrateD
02F9736A  00253FE9  w  mov      word ptr [rip + 0x2d4337a], di               00253C70 InputGameplay_ArbitrateD
02F9736A  002540C5  w  mov      word ptr [rip + 0x2d4329e], di               00253C70 InputGameplay_ArbitrateD
02F9736A  0025415F  w  mov      word ptr [rip + 0x2d43204], di               00253C70 InputGameplay_ArbitrateD
02F9736A  002541BC  w  mov      word ptr [rip + 0x2d431a7], di               00253C70 InputGameplay_ArbitrateD
02F97368  002A329B  w  mov      qword ptr [rip + 0x2cf40c6], r12             002A3250 FUN_002a3250
```

The reader named for the capture: `00277ACD movzx eax, word ptr [rip + …]` in `BattleMenu_UpdateCommandSelectionAndDispatch`
(`002778C0`), one of the 51 readers. The battle command menu is where a missed or doubled confirm press matters most in
play.

Nothing is executed here. The live capture is ASTRA's to run, if they judge it worth the budget.
