# Homing pack: `16-UI/Request-Router/ui-request-router.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-ui-request-router.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002899A0 (107 B, extent 002899A0-00289A0B)

Entered from (direct sites whose caller this page cites): `002D5060` + 0x2A (call; `002D5060` is cited on this page)
Other direct sites: none

Host context: "very anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*  | function | size | entered from | what the body does | interior anchors | |---|---|---|---|---| | '002D5060' | 67 B | '00290740' + 0x1A | calls '002D5060' + 0x2A with dword '01E0C1D8' (0x200 in the image) halved in 'ecx', dword '01E0C1DC' (0x1C0 in the image) halved in both 'edx' and 'r9d', and 1 in 'r8d', each halving a signed division "

```
002899A0  push     rbx
002899A2  sub      rsp, 0x40
002899A6  mov      rax, qword ptr [rip + 0x1cbae83]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002899AD  xor      rax, rsp
002899B0  mov      qword ptr [rsp + 0x38], rax
002899B5  movsxd   rax, ecx
002899B8  mov      ebx, r8d
002899BB  mov      qword ptr [rsp + 0x28], rax
002899C0  lea      r8, [rsp + 0x20]
002899C5  movsxd   rax, edx
002899C8  mov      ecx, 0xd0
002899CD  lea      rdx, [rip + 0x1e8c]  ; -> 0028B860
002899D4  mov      qword ptr [rsp + 0x30], rax
002899D9  mov      dword ptr [rsp + 0x20], 0
002899E1  call     0x244f50  ; -> 00244F50 fn
002899E6  and      ebx, 1
002899E9  add      ebx, ebx
002899EB  and      dword ptr [rax + 0xc4], 0xfffffffd
002899F2  or       dword ptr [rax + 0xc4], ebx
002899F8  mov      rcx, qword ptr [rsp + 0x38]
002899FD  xor      rcx, rsp
00289A00  call     0x808c40  ; -> 00808C40 fn
00289A05  add      rsp, 0x40
00289A09  pop      rbx
00289A0A  ret      
```
