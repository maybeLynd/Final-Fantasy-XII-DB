# Homing pack: `16-UI/Request-Router/ui-request-router.md`

Generated 2026-10-03 00:35 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-ui-request-router.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002D5060 (67 B, extent 002D5060-002D50A3)

Entered from (direct sites whose caller this page cites): `00290740` + 0x1A (call; `00290740` is cited on this page)
Other direct sites: none

Host context: "F5F0' + 0x45 with qword '0209BE80' '+0xAB30' in 'rcx' | Interior anchor '0028F5FB'; Interior anchor '0028F607'; Interior anchor '0028F61A'; Interior anchor '0028F621'; Interior anchor '0028F635' | | '00290740' | 50 B | '002D5EB0' + 0x6A0 | when qword '0209BE80' is non-null and its qword '+0x10FB8' is 0, stores the result of '00290740' + 0x1A to qword '+0x10FB8' of qword '0209BE80'; otherwise returns without a write | Interior anchor '00"

```
002D5060  push     rbx
002D5062  sub      rsp, 0x20
002D5066  mov      eax, dword ptr [rip + 0x1b37170]  ; -> 01E0C1DC [u32 0x000001C0]
002D506C  mov      r8d, 1
002D5072  cdq      
002D5073  sub      eax, edx
002D5075  sar      eax, 1
002D5077  mov      r9d, eax
002D507A  mov      eax, dword ptr [rip + 0x1b37158]  ; -> 01E0C1D8 [u32 0x00000200]
002D5080  cdq      
002D5081  sub      eax, edx
002D5083  mov      edx, r9d
002D5086  sar      eax, 1
002D5088  mov      ecx, eax
002D508A  call     0x2899a0  ; -> 002899A0 fn
002D508F  mov      rcx, rax
002D5092  mov      rbx, rax
002D5095  call     0x246ac0  ; -> 00246AC0 fn
002D509A  mov      rax, rbx
002D509D  add      rsp, 0x20
002D50A1  pop      rbx
002D50A2  ret      
```

## 002F8B90 (25 B, extent 002F8B90-002F8BA9)

Entered from (direct sites whose caller this page cites): `00309E40` + 0x18 (call; `00309E40` is cited on this page)
Other direct sites: none

Host context: "d 'o+0x18' and '002D54B0' + 0x37(0) to dword 'o+0x20' | Interior anchor '002D54C1'; Interior anchor '002D54D2'; Interior anchor '002D54DC'; Interior anchor '002D54E3'; Interior anchor '002D54EC' | | '00309E40' | 42 B | '002D5EB0' + 0x80 | calls '00309E40' + 0x18 with float '022C2184' in 'xmm0' and float '022C2188' minus float '022C2184' in 'xmm1', and stores the float result to '022C2188' | Interior anchor '00309E44'; Interior anchor '0"

```
002F8B90  mulss    xmm1, dword ptr [rip + 0x19f2fd8]  ; -> 01CEBB70 [f32 0.5]
002F8B98  addss    xmm1, xmm0
002F8B9C  movss    xmm0, dword ptr [rip + 0x19f30cc]  ; -> 01CEBC70 [f32 4]
002F8BA4  minss    xmm0, xmm1
002F8BA8  ret      
```
