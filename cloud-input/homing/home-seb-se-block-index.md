# Homing pack: `18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-seb-se-block-index.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00212970 (127 B, extent 00212970-002129EF)

Entered from (direct sites whose caller this page cites): `002129F0` + 0x9 (call; `002129F0` is cited on this page)
Other direct sites: none

Host context: "68750', '00378030', '003EA820' (+2 more) - shared machinery across the layer boundary, no shared ownership. ## SWE2-EC7-44 update (2026-09-19) - '0021B430'  '0021B430' (268 B) is a body - '0016D6A0'/'002129F0'/'00212A70'/'00223AD0' plus 'call [rax+0x18]'/'[rax+0x30]' vcalls. Interior anchor '0021B45D' (an '0016D6A0' call).   ## SWE2-EC7-65 update (2026-09-19) - '002ED950'  '002ED950' (134 B) is a call-free CHSE-candidate jump-table leaf"

```
00212970  mov      eax, dword ptr [rip + 0x1dc0d3a]  ; -> 01FD36B0
00212976  lea      r9, [rip + 0x1dc0d43]  ; -> 01FD36C0
0021297D  inc      eax
0021297F  lea      r10, [rip + 0x1dc113a]  ; -> 01FD3AC0
00212986  and      eax, 0x7fffffff
0021298B  mov      r8, rcx
0021298E  mov      ecx, 1
00212993  cmove    eax, ecx
00212996  mov      dword ptr [rip + 0x1dc0d14], eax  ; -> 01FD36B0
0021299C  mov      dword ptr [r8], eax
0021299F  mov      rax, qword ptr [rip + 0x1befe2a]  ; -> 01E027D0 [u64 0x0000000001FD36C0]
002129A6  mov      ecx, dword ptr [rax]
002129A8  test     ecx, ecx
002129AA  je       0x2129ca  ; -> 002129CA
002129AC  add      rax, 8
002129B0  mov      rcx, r9
002129B3  cmp      rax, r10
002129B6  cmovb    rcx, rax
002129BA  cmp      rcx, qword ptr [rip + 0x1befe0f]  ; -> 01E027D0 [u64 0x0000000001FD36C0]
002129C1  mov      rax, rcx
002129C4  jne      0x2129a6  ; -> 002129A6
002129C6  or       eax, 0xffffffff
002129C9  ret      
002129CA  mov      ecx, dword ptr [r8]
002129CD  mov      dword ptr [rax], ecx
002129CF  lea      rcx, [rax + 8]
002129D3  mov      dword ptr [rax + 4], edx
002129D6  cmp      rcx, r10
002129D9  mov      rdx, r9
002129DC  cmovb    rdx, rcx
002129E0  sub      rax, r9
002129E3  sar      rax, 3
002129E7  mov      qword ptr [rip + 0x1befde2], rdx  ; -> 01E027D0 [u64 0x0000000001FD36C0]
002129EE  ret      
```
