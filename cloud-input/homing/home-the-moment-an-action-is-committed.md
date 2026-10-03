# Homing pack: `07-Combat-Action/the-moment-an-action-is-committed.md`

Generated 2026-10-02 22:54 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-moment-an-action-is-committed.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00310D30 (94 B, extent 00310D30-00310D8E)

Entered from (direct sites whose caller this page cites): `00310920` + 0x147 (call; `00310920` is cited on this page)
Other direct sites: none

Host context: "etClassNibble' '00263C20'; 'BattleLocomotion_DecodeOrderGoal' '00312730', '00336710', '00337A50' and '00338140' call 'BattleUnit_ResolveByFocusHandle' '0031B7E0'; '0025B470', '0026C3E0', '002E28E0', '00310920' and '00313670' call '00377C20'. In the other direction the standard action state 'BattleUnit_AdvanceStandardActionState' '00304850' calls 'BattleLocomotion_SetApproachAndReferenceTargets' '00319110', 'BattleUnit_UpdateCombatNaviga"

```
00310D30  mov      qword ptr [rsp + 8], rbx
00310D35  push     rdi
00310D36  sub      rsp, 0x30
00310D3A  movaps   xmmword ptr [rsp + 0x20], xmm6
00310D3F  mov      rdi, rcx
00310D42  movaps   xmm6, xmm1
00310D45  call     0x327270  ; -> 00327270 fn
00310D4A  mov      rbx, rax
00310D4D  test     rax, rax
00310D50  je       0x310d7e  ; -> 00310D7E
00310D52  movss    xmm3, dword ptr [rdi + 8]
00310D57  mov      rcx, rax
00310D5A  movss    xmm2, dword ptr [rdi + 4]
00310D5F  movss    xmm1, dword ptr [rdi]
00310D63  call     0x26b0c0  ; -> 0026B0C0 fn
00310D68  movaps   xmm1, xmm6
00310D6B  mov      rcx, rbx
00310D6E  call     0x26a0d0  ; -> 0026A0D0 fn
00310D73  movaps   xmm1, xmm6
00310D76  mov      rcx, rbx
00310D79  call     0x26b620  ; -> 0026B620 fn
00310D7E  mov      rbx, qword ptr [rsp + 0x40]
00310D83  movaps   xmm6, xmmword ptr [rsp + 0x20]
00310D88  add      rsp, 0x30
00310D8C  pop      rdi
00310D8D  ret      
```
