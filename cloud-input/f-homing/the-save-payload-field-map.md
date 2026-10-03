# F homing pack: `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md`

Generated 2026-10-02 21:44 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 6. No bearing page cites them and no documented function calls them directly.

## 00264A40 (78 B, extent 00264A40-00264A8E)

Documented callee on this page: `002649B0`

```
00264A40  cmp      ecx, 8
00264A43  ja       0x264a8b  ; -> 00264A8B
00264A45  movsxd   rax, ecx
00264A48  lea      r8, [rip - 0x144a4f]  ; -> 00120000 (image base)
00264A4F  mov      ecx, dword ptr [r8 + rax*4 + 0x144a90]  ; image base + 0x144a90 = 00264A90
00264A57  add      rcx, r8
00264A5A  jmp      rcx
00264A5C  mov      ecx, 2
00264A61  jmp      0x2649b0  ; -> 002649B0 fn
00264A66  mov      ecx, 3
00264A6B  jmp      0x2649b0  ; -> 002649B0 fn
00264A70  mov      ecx, 4
00264A75  jmp      0x2649b0  ; -> 002649B0 fn
00264A7A  xor      ecx, ecx
00264A7C  jmp      0x2649b0  ; -> 002649B0 fn
00264A81  mov      ecx, 1
00264A86  jmp      0x2649b0  ; -> 002649B0 fn
00264A8B  xor      eax, eax
00264A8D  ret      
```

## 002E23E0 (27 B, extent 002E23E0-002E23FB)

Documented callee on this page: `00254E00`

```
002E23E0  sub      rsp, 0x28
002E23E4  mov      r9d, edx
002E23E7  call     0x2e13c0  ; -> 002E13C0 fn
002E23EC  mov      ecx, eax
002E23EE  movzx    edx, r9b
002E23F2  add      rsp, 0x28
002E23F6  jmp      0x254e00  ; -> 00254E00 fn
```

## 00344D30 (65 B, extent 00344D30-00344D71)

Documented callee on this page: `003137E0`

```
00344D30  mov      qword ptr [rsp + 8], rbx
00344D35  push     rdi
00344D36  sub      rsp, 0x20
00344D3A  mov      rdi, r9
00344D3D  call     0x3137e0  ; -> 003137E0 fn
00344D42  mov      edx, eax
00344D44  mov      rcx, rdi
00344D47  call     0x267f90  ; -> 00267F90 fn
00344D4C  mov      rcx, rdi
00344D4F  call     0x267e10  ; -> 00267E10 fn
00344D54  mov      rcx, rdi
00344D57  mov      ebx, eax
00344D59  call     0x267e10  ; -> 00267E10 fn
00344D5E  mov      edx, ebx
00344D60  mov      ecx, eax
00344D62  mov      rbx, qword ptr [rsp + 0x30]
00344D67  add      rsp, 0x20
00344D6B  pop      rdi
00344D6C  jmp      0x36e6f0  ; -> 0036E6F0 fn
```

## 0034A590 (52 B, extent 0034A590-0034A5C4)

Documented callee on this page: `003137E0`

```
0034A590  mov      qword ptr [rsp + 8], rbx
0034A595  push     rdi
0034A596  sub      rsp, 0x20
0034A59A  mov      rdi, rcx
0034A59D  or       ebx, 0xffffffff
0034A5A0  call     0x37c8f0  ; -> 0037C8F0 fn
0034A5A5  test     eax, eax
0034A5A7  je       0x34a5b0  ; -> 0034A5B0
0034A5A9  call     0x3137e0  ; -> 003137E0 fn
0034A5AE  mov      ebx, eax
0034A5B0  mov      edx, ebx
0034A5B2  mov      rcx, rdi
0034A5B5  mov      rbx, qword ptr [rsp + 0x30]
0034A5BA  add      rsp, 0x20
0034A5BE  pop      rdi
0034A5BF  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00356E10 (270 B, extent 00356E10-00356F1E)

Documented callee on this page: `003148B0`

```
00356E10  mov      qword ptr [rsp + 8], rbx
00356E15  push     rbp
00356E16  push     rsi
00356E17  push     rdi
00356E18  sub      rsp, 0x60
00356E1C  movaps   xmmword ptr [rsp + 0x50], xmm6
00356E21  movaps   xmmword ptr [rsp + 0x40], xmm7
00356E26  mov      rax, qword ptr [rip + 0x1beda03]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00356E2D  xor      rax, rsp
00356E30  mov      qword ptr [rsp + 0x30], rax
00356E35  mov      rsi, rcx
00356E38  mov      rbx, r9
00356E3B  mov      rcx, r9
00356E3E  mov      rbp, r8
00356E41  mov      rdi, rdx
00356E44  call     0x267e10  ; -> 00267E10 fn
00356E49  test     eax, eax
00356E4B  jns      0x356e52  ; -> 00356E52
00356E4D  call     0x3148b0  ; -> 003148B0 fn
00356E52  lea      rdx, [rsp + 0x20]
00356E57  mov      ecx, eax
00356E59  call     0x377ab0  ; -> 00377AB0 fn
00356E5E  movss    xmm1, dword ptr [rsp + 0x20]
00356E64  mov      rcx, rbx
00356E67  call     0x267f60  ; -> 00267F60 fn
00356E6C  movss    xmm1, dword ptr [rsp + 0x24]
00356E72  mov      rcx, rbx
00356E75  call     0x267f60  ; -> 00267F60 fn
00356E7A  movss    xmm1, dword ptr [rsp + 0x28]
00356E80  mov      rcx, rbx
00356E83  call     0x267f60  ; -> 00267F60 fn
00356E88  mov      rcx, rbx
00356E8B  call     0x267db0  ; -> 00267DB0 fn
00356E90  mov      rcx, rbx
00356E93  movaps   xmm6, xmm0
00356E96  call     0x267db0  ; -> 00267DB0 fn
00356E9B  mov      rcx, rbx
00356E9E  movaps   xmm7, xmm0
00356EA1  call     0x267db0  ; -> 00267DB0 fn
00356EA6  cmp      byte ptr [rdi + 0x10], 0
00356EAA  movaps   xmm3, xmm6
00356EAD  movaps   xmm2, xmm7
00356EB0  movaps   xmm1, xmm0
00356EB3  mov      rcx, rdi
00356EB6  je       0x356ebf  ; -> 00356EBF
00356EB8  call     0x26b0c0  ; -> 0026B0C0 fn
00356EBD  jmp      0x356ec4  ; -> 00356EC4
00356EBF  call     0x26af80  ; -> 0026AF80 fn
00356EC4  xor      edx, edx
00356EC6  mov      rcx, rdi
00356EC9  call     0x26ae90  ; -> 0026AE90 fn
00356ECE  movss    xmm1, dword ptr [rsp + 0x2c]
00356ED4  mov      rcx, rbx
00356ED7  call     0x267f60  ; -> 00267F60 fn
00356EDC  xor      edx, edx
00356EDE  mov      rcx, rbx
00356EE1  call     0x267f90  ; -> 00267F90 fn
00356EE6  mov      r9, rbx
00356EE9  mov      r8, rbp
00356EEC  mov      rdx, rdi
00356EEF  mov      rcx, rsi
00356EF2  call     0x34d1b0  ; -> 0034D1B0 fn
00356EF7  mov      rcx, qword ptr [rsp + 0x30]
00356EFC  xor      rcx, rsp
00356EFF  call     0x808c40  ; -> 00808C40 fn
00356F04  mov      rbx, qword ptr [rsp + 0x80]
00356F0C  movaps   xmm6, xmmword ptr [rsp + 0x50]
00356F11  movaps   xmm7, xmmword ptr [rsp + 0x40]
00356F16  add      rsp, 0x60
00356F1A  pop      rdi
00356F1B  pop      rsi
00356F1C  pop      rbp
00356F1D  ret      
```

## 00574160 (360 B, extent 00574160-005742C8)

Documented callee on this page: `002AB870`

```
00574160  mov      r11, rsp
00574163  push     rsi
00574164  push     rdi
00574165  sub      rsp, 0x58
00574169  mov      rax, qword ptr [rip + 0x19d06c0]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00574170  xor      rax, rsp
00574173  mov      qword ptr [rsp + 0x38], rax
00574178  cmp      qword ptr [rcx + 0xf8], 0
00574180  mov      rsi, rcx
00574183  mov      rax, qword ptr [rdx + 0x10]
00574187  mov      rdi, qword ptr [rax]
0057418A  je       0x574290  ; -> 00574290
00574190  mov      qword ptr [r11 + 0x18], rbx
00574194  mov      qword ptr [r11 - 0x18], rbp
00574198  xor      ebp, ebp
0057419A  movsxd   rdx, r9d
0057419D  mov      qword ptr [r11 - 0x20], r14
005741A1  mov      qword ptr [r11 - 0x28], r15
005741A5  lea      rax, [rdx + 0x41e]
005741AC  add      rdx, rdx
005741AF  add      rax, rax
005741B2  mov      r8d, dword ptr [rcx + rdx*8 + 0x41e8]
005741BA  mov      r14, qword ptr [rcx + rax*8]
005741BE  movzx    ebx, word ptr [rcx + rdx*8 + 0x41ec]
005741C6  movzx    r15d, byte ptr [rcx + rdx*8 + 0x41ef]
005741CF  cmp      r8d, 0x80808080
005741D6  je       0x5741fd  ; -> 005741FD
005741D8  lea      rdx, [r11 - 0x40]
005741DC  lea      ecx, [rbp + 0x10]
005741DF  call     0x2ab870  ; -> 002AB870 fn
005741E4  movsxd   rbp, eax
005741E7  lea      rcx, [rsi + 0x4120]
005741EE  mov      r8, rbp
005741F1  lea      rdx, [rsp + 0x28]
005741F6  call     0x861eba  ; -> 00861EBA fn
005741FB  dec      ebp
005741FD  movsxd   r10, ebp
00574200  lea      rcx, [rsi + 0x4120]
00574207  mov      r8d, 0x7f
0057420D  mov      r9d, 0x80
00574213  sub      r8d, ebp
00574216  sub      r9, r10
00574219  cmp      rbx, r9
0057421C  mov      rdx, r14
0057421F  cmovb    r8d, ebx
00574223  add      rcx, r10
00574226  mov      ebx, r8d
00574229  call     0x861eba  ; -> 00861EBA fn
0057422E  mov      r14, qword ptr [rsp + 0x48]
00574233  lea      eax, [rbx + rbp]
00574236  mov      rbp, qword ptr [rsp + 0x50]
0057423B  mov      rbx, qword ptr [rsp + 0x80]
00574243  mov      byte ptr [rax + rsi + 0x4120], 0
0057424B  add      rsi, 0x4120
00574252  test     r15b, r15b
00574255  mov      r15, qword ptr [rsp + 0x40]
0057425A  je       0x574297  ; -> 00574297
0057425C  lea      r8, [rsp + 0x24]
00574261  mov      rcx, rdi
00574264  lea      rdx, [rsp + 0x20]
00574269  call     0x29fe20  ; -> 0029FE20 fn
0057426E  movzx    eax, word ptr [rdi + 0x10]
00574272  add      ax, word ptr [rdi + 0xc]
00574276  sub      ax, word ptr [rsp + 0x20]
0057427B  sub      ax, 4
0057427F  mov      word ptr [rdi + 0xa], ax
00574283  movzx    eax, byte ptr [rdi + 0x2d]
00574287  and      al, 0xd7
00574289  or       al, 0x10
0057428B  mov      byte ptr [rdi + 0x2d], al
0057428E  jmp      0x57429b  ; -> 0057429B
00574290  lea      rsi, [rip + 0x17773a1]  ; -> 01CEB638
00574297  and      byte ptr [rdi + 0x2d], 0xc7
0057429B  call     0x5766b0  ; -> 005766B0 fn
005742A0  mov      rcx, rax
005742A3  mov      qword ptr [rdi + 0x18], rsi
005742A7  call     0x20e620  ; -> 0020E620 fn
005742AC  mov      dword ptr [rdi + 0x20], eax
005742AF  mov      eax, 1
005742B4  mov      rcx, qword ptr [rsp + 0x38]
005742B9  xor      rcx, rsp
005742BC  call     0x808c40  ; -> 00808C40 fn
005742C1  add      rsp, 0x58
005742C5  pop      rdi
005742C6  pop      rsi
005742C7  ret      
```
