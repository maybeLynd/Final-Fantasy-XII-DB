# Homing pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-H-ids-236-267.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-arm-catalogue-slice-h-ids-236-267.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00183260 (28 B, extent 00183260-0018327C)

Entered from (direct sites whose caller this page cites): `0079C140` + 0x37D (call; `0079C140` is cited on this page)
Other direct sites: none

Host context: "odies '002DEBA0', '001DBB00'). Substantive edges include '001CD0E0' calls '002DEBA0'; '001D1660' calls '001DBB00'; '001D1660' calls '002DEBA0'. - **Input — CLIENT (1 edge).** 1 inbound (Input bodies '0079C140' call page-cited '00182DE0'). Substantive edges include '00182DE0' is called by '0079C140'. - **PlatformOnlineAchievements — SERVICE (1 edge).** 1 outbound (page-cited '001CD0E0' call PlatformOnlineAchievements bodies '003166F0'). "

```
00183260  sub      rsp, 0x28
00183264  call     0x189120  ; -> 00189120 fn
00183269  test     rax, rax
0018326C  je       0x183277  ; -> 00183277
0018326E  call     0x189120  ; -> 00189120 fn
00183273  mov      byte ptr [rax + 2], 1
00183277  add      rsp, 0x28
0018327B  ret      
```
