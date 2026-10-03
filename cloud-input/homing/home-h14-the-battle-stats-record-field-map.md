# Homing pack: `08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-the-battle-stats-record-field-map.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0031A910 (30 B, extent 0031A910-0031A92E)

Entered from (direct sites whose caller this page cites): `002FDDA0` + 0x343 (call; `002FDDA0` is cited on this page)
Other direct sites: `00344610` + 0x19 (jmp)

Host context: "'+0x26' ('002FF245'), with the Magick Power modifier at '+0x0A' ([where a stat number comes from](../where-a-stat-number-comes-from.md), 'CB-5') | 4 / 4 | 'BattleUnit_ExecuteDirectStateCommandOrder' '002FDDA0' ('002FE156'); '0030C470' ('0030C500'); 'BattleFormula_ApplyTargetResult' '003112F0' ('003118BB'); +1 more | 'BattleUnit_ExecuteDirectStateCommandOrder' '002FDDA0' ('002FE132'); 'BattleAction_UpdateSpecialPresentationSequence' '003"

```
0031A910  push     rbx
0031A912  sub      rsp, 0x20
0031A916  mov      edx, 1
0031A91B  mov      ebx, ecx
0031A91D  call     0x469c00  ; -> 00469C00 fn
0031A922  or       dword ptr [rip + 0x1fa8824], ebx  ; -> 022C314C
0031A928  add      rsp, 0x20
0031A92C  pop      rbx
0031A92D  ret      
```
