# Homing pack: `07-Combat-Action/Action-Dispatch/battle-action-handler-table.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-battle-action-handler-table.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0031A8C0 (29 B, extent 0031A8C0-0031A8DD)

Entered from (direct sites whose caller this page cites): `002FDDA0` + 0x36F (call; `002FDDA0` is cited on this page)
Other direct sites: `00344980` + 0x19 (jmp)

Host context: "d-availability-and-reason-codes.md), which is the *player-facing* availability test; this is the AI-facing one.  ## 3. The handlers  | count | address | name | size | |---:|---|---|---:| | **249** | '002FDDA0' | 'BattleUnit_ExecuteDirectStateCommandOrder' | 1,937 B | | 57 | '002FDA60' | 'caseD_4000' — **the goal-following handler** (read whole 2026-09-12, FABLE: phase byte '+0x6B4', goal from 'BattleLocomotion_DecodeOrderGoal', ends on "

```
0031A8C0  push     rbx
0031A8C2  sub      rsp, 0x20
0031A8C6  xor      edx, edx
0031A8C8  mov      ebx, ecx
0031A8CA  call     0x469c00  ; -> 00469C00 fn
0031A8CF  not      ebx
0031A8D1  and      dword ptr [rip + 0x1fa8875], ebx  ; -> 022C314C
0031A8D7  add      rsp, 0x20
0031A8DB  pop      rbx
0031A8DC  ret      
```
