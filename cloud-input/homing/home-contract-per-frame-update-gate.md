# Homing pack: `00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-per-frame-update-gate.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001BC010 (371 B, extent 001BC010-001BC183)

Entered from (direct sites whose caller this page cites): `0017F040` + 0x21 (jmp; `0017F040` is cited on this page)
Other direct sites: none

Host context: " '[rcx+0x24]' it takes 32 rounds of '002EAFA0(record, i)'; three '003A0F80' decrements walk '[rcx+0x30..0x38]', '[rcx+0x10]' frees through '00369800' when nonzero and is zeroed, '[rcx+0x14]' goes to '0017F040', then the node unlinks from the '0215FD60'/'0215FD88' doubly-linked list, re-links at the head under a bumped '+0x24' generation with '+0x18'/'+0x26'/'+0x14' cleared - the detach-and-recycle the gate's object pool performs.  Inter"

```
001BC010  mov      qword ptr [rsp + 0x18], rbx
001BC015  mov      qword ptr [rsp + 0x20], rbp
001BC01A  push     rsi
001BC01B  sub      rsp, 0x20
001BC01F  mov      r8, qword ptr [rcx + 0xc8]
001BC026  mov      ebx, edx
001BC028  lea      rdx, [rcx + 0xb8]
001BC02F  mov      rsi, rcx
001BC032  mov      rax, rdx
001BC035  test     r8, r8
001BC038  je       0x1bc057  ; -> 001BC057
001BC03A  nop      word ptr [rax + rax]
001BC040  cmp      dword ptr [r8 + 0x20], ebx
001BC044  jl       0x1bc04f  ; -> 001BC04F
001BC046  mov      rax, r8
001BC049  mov      r8, qword ptr [r8 + 8]
001BC04D  jmp      0x1bc052  ; -> 001BC052
001BC04F  mov      r8, qword ptr [r8]
001BC052  test     r8, r8
001BC055  jne      0x1bc040  ; -> 001BC040
001BC057  cmp      rax, rdx
001BC05A  je       0x1bc061  ; -> 001BC061
001BC05C  cmp      ebx, dword ptr [rax + 0x20]
001BC05F  jge      0x1bc064  ; -> 001BC064
001BC061  mov      rax, rdx
001BC064  lea      rbp, [rcx + 0xb8]
001BC06B  cmp      rax, rbp
001BC06E  je       0x1bc0d0  ; -> 001BC0D0
001BC070  mov      rcx, qword ptr [rax + 0x28]
001BC074  sub      dword ptr [rcx + 0x48], 1
001BC078  jne      0x1bc0d0  ; -> 001BC0D0
001BC07A  xor      r8d, r8d
001BC07D  mov      qword ptr [rsp + 0x38], rdi
001BC082  lea      rdi, [rsi + 0x1a8]
001BC089  mov      dword ptr [rsp + 0x30], ebx
001BC08D  mov      rax, qword ptr [rdi + 0x10]
001BC091  lea      rcx, [rdi + 0x10]
001BC095  mov      dword ptr [rsp + 0x34], 4
001BC09D  lea      edx, [r8 + 0x18]
001BC0A1  call     qword ptr [rax + 0x10]
001BC0A4  lea      rdx, [rax + 0x10]
001BC0A8  test     rdx, rdx
001BC0AB  je       0x1bc0b5  ; -> 001BC0B5
001BC0AD  mov      rcx, qword ptr [rsp + 0x30]
001BC0B2  mov      qword ptr [rdx], rcx
001BC0B5  mov      qword ptr [rax], rdi
001BC0B8  mov      rcx, qword ptr [rdi + 8]
001BC0BC  mov      qword ptr [rax + 8], rcx
001BC0C0  mov      rcx, qword ptr [rdi + 8]
001BC0C4  mov      qword ptr [rcx], rax
001BC0C7  mov      qword ptr [rdi + 8], rax
001BC0CB  mov      rdi, qword ptr [rsp + 0x38]
001BC0D0  test     ebx, ebx
001BC0D2  js       0x1bc173  ; -> 001BC173
001BC0D8  mov      rax, qword ptr [rsi + 0xc8]
001BC0DF  lea      r8, [rsi + 0xb8]
001BC0E6  mov      edx, 0xfffffffe
001BC0EB  mov      rcx, r8
001BC0EE  sub      edx, ebx
001BC0F0  test     rax, rax
001BC0F3  je       0x1bc10b  ; -> 001BC10B
001BC0F5  cmp      dword ptr [rax + 0x20], edx
001BC0F8  jl       0x1bc103  ; -> 001BC103
001BC0FA  mov      rcx, rax
001BC0FD  mov      rax, qword ptr [rax + 8]
001BC101  jmp      0x1bc106  ; -> 001BC106
001BC103  mov      rax, qword ptr [rax]
001BC106  test     rax, rax
001BC109  jne      0x1bc0f5  ; -> 001BC0F5
001BC10B  cmp      rcx, r8
001BC10E  je       0x1bc115  ; -> 001BC115
001BC110  cmp      edx, dword ptr [rcx + 0x20]
001BC113  jge      0x1bc118  ; -> 001BC118
001BC115  mov      rcx, r8
001BC118  cmp      rcx, rbp
001BC11B  je       0x1bc173  ; -> 001BC173
001BC11D  mov      rax, qword ptr [rcx + 0x28]
001BC121  sub      dword ptr [rax + 0x48], 1
001BC125  jne      0x1bc173  ; -> 001BC173
001BC127  xor      r8d, r8d
001BC12A  mov      dword ptr [rsp + 0x30], edx
001BC12E  lea      rbx, [rsi + 0x1a8]
001BC135  mov      dword ptr [rsp + 0x34], 4
001BC13D  mov      rax, qword ptr [rbx + 0x10]
001BC141  lea      rcx, [rbx + 0x10]
001BC145  lea      edx, [r8 + 0x18]
001BC149  call     qword ptr [rax + 0x10]
001BC14C  lea      rdx, [rax + 0x10]
001BC150  test     rdx, rdx
001BC153  je       0x1bc15d  ; -> 001BC15D
001BC155  mov      rcx, qword ptr [rsp + 0x30]
001BC15A  mov      qword ptr [rdx], rcx
001BC15D  mov      qword ptr [rax], rbx
001BC160  mov      rcx, qword ptr [rbx + 8]
001BC164  mov      qword ptr [rax + 8], rcx
001BC168  mov      rcx, qword ptr [rbx + 8]
001BC16C  mov      qword ptr [rcx], rax
001BC16F  mov      qword ptr [rbx + 8], rax
001BC173  mov      rbx, qword ptr [rsp + 0x40]
001BC178  mov      rbp, qword ptr [rsp + 0x48]
001BC17D  add      rsp, 0x20
001BC181  pop      rsi
001BC182  ret      
```

## 003F65C0 (196 B, extent 003F65C0-003F6684)

Entered from (direct sites whose caller this page cites): `003F62D0` + 0x1A (call; `003F62D0` is cited on this page)
Other direct sites: none

Host context: " through '003F6370', compares against 1.0, scales '01DFE0B4' by '0xF' iterations and the '008C5F6C'/'008F30F8'/'009002BC'/'009159F8'/'00901988' constants, clamps via '0028E9F0', and finishes through '003F62D0' - the parameterized fade/speed curve one gate arm advances each tick.  Interior anchor '003F5F45' (function '003F5CB0').  ## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; AUDIT-SPEC batch 4)  *Each body below was hom"

```
003F65C0  mov      qword ptr [rcx + 0x18], 0xe
003F65C8  mov      r9, rcx
003F65CB  movabs   rax, 0x1000000000000002
003F65D5  mov      qword ptr [rcx + 0x10], rax
003F65D9  xor      eax, eax
003F65DB  mov      qword ptr [rcx + 0x20], 0x5b
003F65E3  mov      qword ptr [rcx + 0x28], rax
003F65E7  mov      qword ptr [rcx + 0x30], 0x5c
003F65EF  mov      qword ptr [rcx + 0x38], rax
003F65F3  movabs   rax, 0x3000000000008000
003F65FD  mov      qword ptr [r9 + 0x48], 0x412
003F6605  lea      ecx, [rdx*4 + 2]
003F660C  or       rcx, rax
003F660F  lea      eax, [rdx + 5]
003F6612  mov      qword ptr [r9 + 0x40], rcx
003F6616  shl      eax, 0x10
003F6619  or       eax, 0x6c008000
003F661E  mov      dword ptr [r9], 0x10000000
003F6625  mov      dword ptr [r9 + 0xc], eax
003F6629  mov      dword ptr [r9 + 4], 0x10000000
003F6631  mov      dword ptr [r9 + 8], 0x10000000
003F6639  mov      dword ptr [r9 + 0x50], 0x42fe0000
003F6641  mov      dword ptr [r9 + 0x54], 0x42fe0000
003F6649  mov      dword ptr [r9 + 0x58], 0x42fe0000
003F6651  mov      dword ptr [r9 + 0x5c], edx
003F6655  mov      eax, edx
003F6657  add      rax, 6
003F665B  shl      rax, 4
003F665F  add      rax, r9
003F6662  mov      dword ptr [rax], 0x10000000
003F6668  mov      dword ptr [rax + 4], 0x17000000
003F666F  mov      dword ptr [rax + 8], 0x10000000
003F6676  mov      dword ptr [rax + 0xc], 0x10000000
003F667D  sub      eax, r9d
003F6680  add      eax, 0x10
003F6683  ret      
```

## 003F6A10 (288 B, extent 003F6A10-003F6B30)

Entered from (direct sites whose caller this page cites): `003F62D0` + 0x88 (call; `003F62D0` is cited on this page)
Other direct sites: none

Host context: " through '003F6370', compares against 1.0, scales '01DFE0B4' by '0xF' iterations and the '008C5F6C'/'008F30F8'/'009002BC'/'009159F8'/'00901988' constants, clamps via '0028E9F0', and finishes through '003F62D0' - the parameterized fade/speed curve one gate arm advances each tick.  Interior anchor '003F5F45' (function '003F5CB0').  ## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; AUDIT-SPEC batch 4)  *Each body below was hom"

```
003F6A10  mov      qword ptr [rsp + 8], rbx
003F6A15  push     rdi
003F6A16  sub      rsp, 0x20
003F6A1A  mov      edx, dword ptr [rcx + 0x5c]
003F6A1D  xor      edi, edi
003F6A1F  movss    xmm0, dword ptr [rip + 0x18f5181]  ; -> 01CEBBA8 [f32 1]
003F6A27  mov      r9, rcx
003F6A2A  subss    xmm0, xmm1
003F6A2E  mov      r8d, edi
003F6A31  movd     xmm4, edx
003F6A35  cvtdq2ps xmm4, xmm4
003F6A38  mulss    xmm0, xmm4
003F6A3C  cvttss2si r11, xmm0
003F6A41  movaps   xmm0, xmm4
003F6A44  mulss    xmm4, dword ptr [rsp + 0x50]
003F6A4A  mulss    xmm0, xmm2
003F6A4E  movaps   xmm2, xmm3
003F6A51  mulss    xmm3, dword ptr [rip + 0x50ffeb]  ; -> 00906A44 [f32 127]
003F6A59  mulss    xmm2, dword ptr [rip + 0x4fc6d3]  ; -> 008F3134 [f32 100]
003F6A61  cvttss2si rbx, xmm4
003F6A66  mulss    xmm2, dword ptr [rsp + 0x50]
003F6A6C  xorps    xmm4, xmm4
003F6A6F  mov      eax, ebx
003F6A71  movss    dword ptr [rcx + 0x50], xmm3
003F6A76  cvttss2si r10, xmm0
003F6A7B  movss    dword ptr [rcx + 0x54], xmm3
003F6A80  sub      eax, r10d
003F6A83  movss    dword ptr [rcx + 0x58], xmm3
003F6A88  cvtsi2ss xmm4, rax
003F6A8D  test     edx, edx
003F6A8F  je       0x3f6af2  ; -> 003F6AF2
003F6A91  mov      edx, r10d
003F6A94  neg      edx
003F6A96  cmp      r8d, r11d
003F6A99  jbe      0x3f6ade  ; -> 003F6ADE
003F6A9B  cmp      r8d, r10d
003F6A9E  ja       0x3f6aaf  ; -> 003F6AAF
003F6AA0  mov      eax, r8d
003F6AA3  add      rax, rax
003F6AA6  movss    dword ptr [r9 + rax*8 + 0x6c], xmm2
003F6AAD  jmp      0x3f6ae9  ; -> 003F6AE9
003F6AAF  cmp      r8d, ebx
003F6AB2  ja       0x3f6ade  ; -> 003F6ADE
003F6AB4  lea      ecx, [rdx + r8]
003F6AB8  mov      eax, r8d
003F6ABB  xorps    xmm0, xmm0
003F6ABE  movaps   xmm1, xmm4
003F6AC1  cvtsi2ss xmm0, rcx
003F6AC6  add      rax, rax
003F6AC9  subss    xmm1, xmm0
003F6ACD  divss    xmm1, xmm4
003F6AD1  mulss    xmm1, xmm2
003F6AD5  movss    dword ptr [r9 + rax*8 + 0x6c], xmm1
003F6ADC  jmp      0x3f6ae9  ; -> 003F6AE9
003F6ADE  mov      eax, r8d
003F6AE1  add      rax, rax
003F6AE4  mov      dword ptr [r9 + rax*8 + 0x6c], edi
003F6AE9  inc      r8d
003F6AEC  cmp      r8d, dword ptr [r9 + 0x5c]
003F6AF0  jb       0x3f6a96  ; -> 003F6A96
003F6AF2  mov      eax, dword ptr [r9 + 0x5c]
003F6AF6  mov      rbx, qword ptr [rsp + 0x58]
003F6AFB  dec      eax
003F6AFD  movsxd   rcx, eax
003F6B00  add      rcx, rcx
003F6B03  mov      edx, r11d
003F6B06  add      rdx, 6
003F6B0A  shl      rdx, 4
003F6B0E  add      rdx, r9
003F6B11  mov      dword ptr [r9 + rcx*8 + 0x6c], edi
003F6B16  mov      rcx, rbx
003F6B19  call     0x202c90  ; -> 00202C90 fn
003F6B1E  mov      dword ptr [rbx + 0xc], 0x3f800000
003F6B25  mov      rbx, qword ptr [rsp + 0x30]
003F6B2A  add      rsp, 0x20
003F6B2E  pop      rdi
003F6B2F  ret      
```
