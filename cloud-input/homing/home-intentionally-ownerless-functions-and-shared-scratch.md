# Homing pack: `00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md`

Generated 2026-10-03 09:39 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-intentionally-ownerless-functions-and-shared-scratch.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00311E90 (177 B, extent 00311E90-00311F41)

Entered from (direct sites whose caller this page cites): `00346EB0` + 0x6 (call; `00346EB0` is cited on this page)
Other direct sites: none

Host context: "rn is discarded), then tail-jumps '002ECF10(P, 1, 1)' | Interior anchor '003460C6'; Interior anchor '003460C9'; Interior anchor '003460D4'; Interior anchor '003460E1'; Interior anchor '003460E9' | | '00346EB0' | 57 B | calls the function at '00346EB0+0x6', then for 'ebx' = 0 to 3 calls the function at '00346EB0+0x12' with 'ecx' = 'ebx' and, when it returns non-null, calls '002ECF10(result, 1, 1)' | Interior anchor '00346EB6'; Interior a"

```
00311E90  mov      qword ptr [rsp + 8], rbx
00311E95  mov      qword ptr [rsp + 0x10], rbp
00311E9A  mov      qword ptr [rsp + 0x18], rsi
00311E9F  push     rdi
00311EA0  push     r14
00311EA2  push     r15
00311EA4  sub      rsp, 0x20
00311EA8  xor      ebx, ebx
00311EAA  lea      r15, [rip + 0x1faf8d7]  ; -> 022C1788
00311EB1  mov      r14d, ebx
00311EB4  mov      esi, ebx
00311EB6  mov      edi, ebx
00311EB8  mov      ecx, esi
00311EBA  call     0x31b810  ; -> 0031B810 fn
00311EBF  mov      rbp, rax
00311EC2  test     rax, rax
00311EC5  je       0x311efa  ; -> 00311EFA
00311EC7  mov      rax, qword ptr [rax + 0x698]
00311ECE  test     rax, rax
00311ED1  je       0x311efa  ; -> 00311EFA
00311ED3  mov      ecx, dword ptr [rax + 0x64]
00311ED6  or       ecx, dword ptr [rax + 0x3c]
00311ED9  test     ecx, 0x80000003
00311EDF  je       0x311eea  ; -> 00311EEA
00311EE1  call     0x377c20  ; -> 00377C20 fn
00311EE6  test     eax, eax
00311EE8  je       0x311efa  ; -> 00311EFA
00311EEA  cmp      rdi, 4
00311EEE  jge      0x311ef4  ; -> 00311EF4
00311EF0  mov      qword ptr [r15 + rdi*8], rbp
00311EF4  inc      r14d
00311EF7  inc      rdi
00311EFA  inc      esi
00311EFC  cmp      esi, 4
00311EFF  jl       0x311eb8  ; -> 00311EB8
00311F01  movsxd   rcx, r14d
00311F04  test     r14d, r14d
00311F07  jle      0x311f28  ; -> 00311F28
00311F09  nop      dword ptr [rax]
00311F10  mov      rax, qword ptr [r15 + rbx*8]
00311F14  test     rax, rax
00311F17  je       0x311f20  ; -> 00311F20
00311F19  or       dword ptr [rax + 4], 0x600
00311F20  inc      rbx
00311F23  cmp      rbx, rcx
00311F26  jl       0x311f10  ; -> 00311F10
00311F28  mov      rbx, qword ptr [rsp + 0x40]
00311F2D  mov      rbp, qword ptr [rsp + 0x48]
00311F32  mov      rsi, qword ptr [rsp + 0x50]
00311F37  add      rsp, 0x20
00311F3B  pop      r15
00311F3D  pop      r14
00311F3F  pop      rdi
00311F40  ret      
```

## 0041C770 (78 B, extent 0041C770-0041C7BE)

Entered from (direct sites whose caller this page cites): `00423380` + 0x39 (jmp; `00423380` is cited on this page)
Other direct sites: none

Host context: "= word 'rcx+0x10' zero-extended; otherwise it returns | Interior anchor '003EB943'; Interior anchor '003EB945'; Interior anchor '003EB949'; Interior anchor '003EB94B'; Interior anchor '003EB94F' | | '00423380' | 71 B | returns 0.0 in 'xmm0' when dword 'rcx+0xc4' is -1 or when '0051B9E0'(qword '+0xda8' of '0020E600(dword rcx+0x10)', dword 'rcx+0xc4') returns null; otherwise tail-jumps at '00423380+0x39' with 'rcx' = that result | Interio"

```
0041C770  movsx    r9, word ptr [rcx + 0x28]
0041C775  mov      r8d, 1
0041C77B  mov      r10, rcx
0041C77E  mov      eax, r8d
0041C781  cmp      r8, r9
0041C784  jge      0x41c7a7  ; -> 0041C7A7
0041C786  lea      rdx, [rcx + 0x165]
0041C78D  nop      dword ptr [rax]
0041C790  cmp      byte ptr [rdx], 1
0041C793  je       0x41c7ab  ; -> 0041C7AB
0041C795  inc      r8d
0041C798  inc      rax
0041C79B  add      rdx, 0xa0
0041C7A2  cmp      rax, r9
0041C7A5  jl       0x41c790  ; -> 0041C790
0041C7A7  xorps    xmm0, xmm0
0041C7AA  ret      
0041C7AB  movsxd   rax, r8d
0041C7AE  lea      rcx, [rax + rax*4]
0041C7B2  shl      rcx, 5
0041C7B6  movss    xmm0, dword ptr [rcx + r10 + 0x3c]
0041C7BD  ret      
```
