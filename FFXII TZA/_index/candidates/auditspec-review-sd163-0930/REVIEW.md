# SWE2-AUDIT-SPEC review of SteamController_PollState (OPUS, e5e8d6013): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
[sd163-steamcontroller-poll-0930](../sd163-steamcontroller-poll-0930/README.md) at e5e8d6013, measured at HEAD
17a959c94 (the first worker's re-run was at HEAD 3cae47364; the package is unchanged between them). Static,
certified image, plus the Steamworks DLLs that ship next to it.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD163-0930 | `_index/candidates/sd163-steamcontroller-poll-0930/` | `e5e8d6013` | ACCEPT-WITH-NARROWING |

**Re-run.** `sd163_poll.py` -> [rerun_sd163_poll.out](rerun_sd163_poll.out): identical to the committed `.out`
(ignoring CR), P1-P5 PASS, `FAILS 0`. Package dir clean after re-run: yes (`git status --porcelain` on it prints
nothing).

**Re-derived independently** ([sd163_indep.py](sd163_indep.py) / [sd163_indep.out](sd163_indep.out); full decode
[dump_poll_lin.out](dump_poll_lin.out) over the .pdata extent `[007A1CD0, 007A2134)`).
- Calls through the interface `[02EA9508]`: `+0x18` x1, `+0x48` x16, `+0x60` x4, `+0x88` x1. Every `+0x48` and
  `+0x60` call passes the controller handle `[02EA95A0]` in r8 and an action handle cell in r9.
- **The button-list end.** The 16 digital calls use 16 distinct cells, `02EA9510` to `02EA9588`, contiguous qwords.
  The analog calls use `02EA9590` (twice) and `02EA9598` (twice). The two sets do not overlap. The fill loop in
  `00792B70` agrees: `GetDigitalActionHandle` results go to `[rdi+rbp+0x2D89510 displacement]` with rbp = 0x120000
  for rdi < 0x80 (16 qwords, last `02EA9588`), and the analog handles go to `[rbx+rbp+0x2D89590 displacement]` for
  rbx < 0x10 ([dump_792b70.out](dump_792b70.out)). So the README's "qwords `02EA9510`…`02EA9590`" gives the wrong last
  cell. The right one is `02EA9588`.
- Each digital call's `movzx ecx, byte [rax]` goes to one byte of `+0x43C`..`+0x44B` (all 16, one each). The analog
  calls read `[rax+4]` (x) and `[rax+8]` (y). x is scaled by the constant `00915A00` = 256.0 and stored to `+0x414`
  (`02EA9590`) and `+0x418` (`02EA9598`). y is scaled by `01CB3CF8` = -256.0 and stored to `+0x420` and `+0x424`.
- `+0x88` arguments: rdx = `[02EA95A0]`, r8d = byte `+0x98` x 0x100, r9d = byte `+0x99` x 0x100. My tracker's `r9`
  column for that row is stale: `movzx r9d` overwrites r9.
- The gate: `jle` on a count <= 0 and a compare of the first returned handle `[rsp+0x50]` with `[02EA95A0]`, else
  the disconnect arm (log `01CB3928`, clear `+0xA9` only if it was set). `+0xA9` is set once after the connect log.
- `007A15A0` walks the ring at `this+0x18`. For a node with a state pointer `+0x38`: `+0x31` = 1 on a 0->1 edge,
  `+0x32` = 1 on a 1->0 edge, then `+0x30` = the new state. Otherwise, with `+0x40` set, it calls `0079A5F0`.
- **Which button each byte is** ([sd163_names.py](sd163_names.py) / [sd163_names.out](sd163_names.out)). The name
  table at `01F40210` names the cells `Up, Down, Left, Right, Circle, Cross, Square, Triangle, L1, L2, L3, R1, R2,
  R3, Start, Select` in order. Mapped through the stores, `+0x43C`..`+0x44B` are Square, Cross, Circle, Triangle, L1,
  R1, L2, R2, Select, Start, L3, R3, Up, Right, Down, Left. That is the XInput poll's PlayStation order in
  [dm2-code27](../dm2-code27/README.md) D3. This answers the README's first limit.

**Method names: verified, not only an identification.** No SDK header was searched on disk. The game folder ships
`steam_api64.dll` (x64), which the exe imports. It carries the same interface version the exe asks for,
`SteamController005`, and its flat-API exports `SteamAPI_ISteamController_<Method>` each call through one vtable
slot ([sdk_vtable.py](sdk_vtable.py) / [sdk_vtable.out](sdk_vtable.out)). The slots include
`0x18` GetConnectedControllers, `0x48` GetDigitalActionData, `0x60` GetAnalogActionData and `0x88`
TriggerVibration. As a control, the slots `00792B70` uses fit the same list: `0x28` GetActionSetHandle on the
string "Global", `0x30` ActivateActionSet, `0x40` GetDigitalActionHandle and `0x58` GetAnalogActionHandle. The
bundled `CSteamworks.dll` is 32-bit, and my scanner does not decode its register-indirect calls. It was not needed.

**Controls.** Defect: a handle list that overlaps or is off by one cell. The instrument is sensitive to it: it lists
each call's r9 cell, so an overlap would show as a shared cell. It found `02EA9590` on analog calls only. The name
table is a second, independent source for the 16/2 split (loop bounds 0x80 / 0x10). Defect: a wrong method name.
Control: the `00792B70` slot uses have to fit their names (a string argument goes to a handle lookup), and they do.

**Citations checked.** P1-P5's cited addresses match the bytes. "Already on record" (dm2-code27 D3: the Steam poll
stores exactly 16 bytes `+0x43C`..`+0x44B`) matches the decode.

**Runtime routing.** None needed; nothing in the claim is live-only.

**Correction wording.** In the README P2, replace "(qwords `02EA9510`…`02EA9590`)" with "(qwords `02EA9510`…
`02EA9588`)". In the opening paragraph, replace "That naming is an identification matched to the call shapes, not a
symbol." with "The slot names are confirmed against the shipped `steam_api64.dll` (`SteamController005`): its flat
exports `SteamAPI_ISteamController_*` call through the same slots (SWE2-AUDIT-SPEC review 2026-09-30)." Optional:
replace the first Limit with the byte order above (Square … Left, the XInput order), and the second with the
`007A15A0` edge rule.
