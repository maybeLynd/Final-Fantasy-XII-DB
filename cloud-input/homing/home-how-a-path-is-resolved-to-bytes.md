# Homing pack: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md`

Generated 2026-10-03 00:35 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-how-a-path-is-resolved-to-bytes.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0059FD10 (137 B, extent 0059FD10-0059FD99)

Entered from (direct sites whose caller this page cites): `0059FDA0` + 0x4 (jmp; `0059FDA0` is cited on this page)
Other direct sites: none

Host context: "d** - slot 1, then slot 3, then clears '+0x18' | | 5 | '0059D4B0' | **Read** - from the buffer, else 'ReadFile', else the '+0x40' backing; returns 0, calling nothing, when none applies (§5c) | | 6 | '0059FDA0' | **Seek** on the buffer backing |  **Slot 2 is twenty-seven bytes and settles what "open" means here.** It returns '!(+0x28 == -1 && +0x30 == 0 && +0x40 == -1)', comparing all three as full 64-bit values, and it sets only AL (RAX"

```
0059FD10  push     rbx
0059FD12  sub      rsp, 0x20
0059FD16  mov      rax, qword ptr [rcx + 0x10]
0059FD1A  mov      ebx, edx
0059FD1C  test     rax, rax
0059FD1F  je       0x59fd41  ; -> 0059FD41
0059FD21  mov      r8d, 1
0059FD27  mov      rcx, rax
0059FD2A  call     0x215220  ; -> 00215220 fn
0059FD2F  mov      r8d, eax
0059FD32  xor      eax, eax
0059FD34  cmp      r8d, -1
0059FD38  cmovne   eax, ebx
0059FD3B  add      rsp, 0x20
0059FD3F  pop      rbx
0059FD40  ret      
0059FD41  mov      rax, qword ptr [rcx + 8]
0059FD45  or       r8d, 0xffffffff
0059FD49  cmp      rax, -1
0059FD4D  je       0x59fd73  ; -> 0059FD73
0059FD4F  mov      r9d, 1
0059FD55  xor      r8d, r8d
0059FD58  mov      rcx, rax
0059FD5B  call     qword ptr [rip + 0x3223ef]  ; -> 008C2150 [u64 0x0000000001CCC23A]
0059FD61  mov      r8d, eax
0059FD64  xor      eax, eax
0059FD66  cmp      r8d, -1
0059FD6A  cmovne   eax, ebx
0059FD6D  add      rsp, 0x20
0059FD71  pop      rbx
0059FD72  ret      
0059FD73  mov      rcx, qword ptr [rcx + 0x20]
0059FD77  test     rcx, rcx
0059FD7A  jle      0x59fd8a  ; -> 0059FD8A
0059FD7C  mov      r8d, 1
0059FD82  call     0x1d6ce0  ; -> 001D6CE0 fn
0059FD87  mov      r8d, eax
0059FD8A  xor      eax, eax
0059FD8C  cmp      r8d, -1
0059FD90  cmovne   eax, ebx
0059FD93  add      rsp, 0x20
0059FD97  pop      rbx
0059FD98  ret      
```
