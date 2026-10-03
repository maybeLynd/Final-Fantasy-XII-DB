# Homing pack: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-how-the-ard-loader-binds-area-battle-data.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0031A8C0 (29 B, extent 0031A8C0-0031A8DD)

Entered from (direct sites whose caller this page cites): `002FDDA0` + 0x36F (call; `002FDDA0` is cited on this page)
Other direct sites: `00344980` + 0x19 (jmp)

Host context: "ffinityState' '002FEF30', 'BattleEncodedId_IsValidForClass' '00322C50' | | '0x02EBF168' | 'BattleUnit_SelectAiOrderSetVariantFromAuthoredUnit' '00239040', 'BattleUnit_ExecuteDirectStateCommandOrder' '002FDDA0', 'BattleUnit_ApplyUnitDefinition' '0023A570' |  ### What this sheet declares, and the one it does not  Four of the five are declared in this document's 'registry_slots'. **What each declaration claims is narrow and checkable:**  >"

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
