# F homing pack (FABLE): `00-Engine-Core-Runtime/Application-Root/game-application.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 16. No bearing page cites them and no documented function calls them directly.

## 006D87D0 (807 B, extent 006D87D0-006D8AF7)

Documented callee on this page: `00861EBA`

```
006D87D0  test     edx, edx
006D87D2  je       0x6d8af6  ; -> 006D8AF6
006D87D8  mov      qword ptr [rsp + 8], rbx
006D87DD  push     rbp
006D87DE  mov      rbp, rsp
006D87E1  sub      rsp, 0x70
006D87E5  mov      rax, qword ptr [rip + 0x186c044]  ; -> 01F44830 [u64 0x00002B992DDFA232]
006D87EC  xor      rax, rsp
006D87EF  mov      qword ptr [rbp - 0x20], rax
006D87F3  movss    xmm3, dword ptr [rcx]
006D87F7  xor      r10d, r10d
006D87FA  xorps    xmm0, xmm0
006D87FD  mov      r11, r9
006D8800  ucomiss  xmm3, xmm0
006D8803  mov      rbx, rcx
006D8806  mov      r9d, r10d
006D8809  jp       0x6d8818  ; -> 006D8818
006D880B  jne      0x6d8818  ; -> 006D8818
006D880D  mov      rcx, qword ptr [rbp - 0x40]
006D8811  movss    xmm3, dword ptr [rbp - 0x50]
006D8816  jmp      0x6d882a  ; -> 006D882A
006D8818  mov      rcx, qword ptr [r8]
006D881B  mov      r9d, 1
006D8821  mov      qword ptr [rbp - 0x40], rcx
006D8825  movss    dword ptr [rbp - 0x50], xmm3
006D882A  movss    xmm1, dword ptr [rbx + 4]
006D882F  ucomiss  xmm1, xmm0
006D8832  jp       0x6d8836  ; -> 006D8836
006D8834  je       0x6d8854  ; -> 006D8854
006D8836  mov      rax, qword ptr [r8 + 8]
006D883A  mov      ecx, r9d
006D883D  inc      r9d
006D8840  movss    dword ptr [rbp + rcx*4 - 0x50], xmm1
006D8846  movss    xmm3, dword ptr [rbp - 0x50]
006D884B  mov      qword ptr [rbp + rcx*8 - 0x40], rax
006D8850  mov      rcx, qword ptr [rbp - 0x40]
006D8854  movss    xmm1, dword ptr [rbx + 8]
006D8859  ucomiss  xmm1, xmm0
006D885C  jp       0x6d8860  ; -> 006D8860
006D885E  je       0x6d887e  ; -> 006D887E
006D8860  mov      rax, qword ptr [r8 + 0x10]
006D8864  mov      ecx, r9d
006D8867  inc      r9d
006D886A  movss    dword ptr [rbp + rcx*4 - 0x50], xmm1
006D8870  movss    xmm3, dword ptr [rbp - 0x50]
006D8875  mov      qword ptr [rbp + rcx*8 - 0x40], rax
006D887A  mov      rcx, qword ptr [rbp - 0x40]
006D887E  movss    xmm1, dword ptr [rbx + 0xc]
006D8883  ucomiss  xmm1, xmm0
006D8886  jp       0x6d888a  ; -> 006D888A
006D8888  je       0x6d88a8  ; -> 006D88A8
006D888A  mov      rax, qword ptr [r8 + 0x18]
006D888E  mov      ecx, r9d
006D8891  inc      r9d
006D8894  movss    dword ptr [rbp + rcx*4 - 0x50], xmm1
006D889A  movss    xmm3, dword ptr [rbp - 0x50]
006D889F  mov      qword ptr [rbp + rcx*8 - 0x40], rax
006D88A4  mov      rcx, qword ptr [rbp - 0x40]
006D88A8  shufps   xmm3, xmm3, 0
006D88AC  lea      r8d, [rdx + rdx*2]
006D88B0  sub      r9d, 1
006D88B4  je       0x6d8a07  ; -> 006D8A07
006D88BA  sub      r9d, 1
006D88BE  je       0x6d89c7  ; -> 006D89C7
006D88C4  sub      r9d, 1
006D88C8  je       0x6d8969  ; -> 006D8969
006D88CE  cmp      r9d, 1
006D88D2  je       0x6d88e7  ; -> 006D88E7
006D88D4  mov      rcx, qword ptr [r11]
006D88D7  xor      edx, edx
006D88D9  shl      r8, 2
006D88DD  call     0x861ec0  ; -> 00861EC0 fn
006D88E2  jmp      0x6d8add  ; -> 006D8ADD
006D88E7  mov      rdx, qword ptr [rbp - 0x38]
006D88EB  mov      r9, qword ptr [rbp - 0x28]
006D88EF  sub      rdx, rcx
006D88F2  mov      r10, qword ptr [rbp - 0x30]
006D88F6  sub      r9, rcx
006D88F9  mov      rax, qword ptr [r11]
006D88FC  sub      r10, rcx
006D88FF  movss    xmm4, dword ptr [rbp - 0x44]
006D8904  movss    xmm5, dword ptr [rbp - 0x48]
006D8909  movaps   xmmword ptr [rsp + 0x60], xmm6
006D890E  movss    xmm6, dword ptr [rbp - 0x4c]
006D8913  nop      dword ptr [rax]
006D8917  nop      word ptr [rax + rax]
006D8920  movaps   xmm0, xmm3
006D8923  movaps   xmm2, xmm6
006D8926  mulss    xmm2, dword ptr [rdx + rcx]
006D892B  movaps   xmm1, xmm5
006D892E  mulss    xmm0, dword ptr [rcx]
006D8932  mulss    xmm1, dword ptr [r10 + rcx]
006D8938  addss    xmm2, xmm0
006D893C  movaps   xmm0, xmm4
006D893F  mulss    xmm0, dword ptr [r9 + rcx]
006D8945  add      rcx, 4
006D8949  addss    xmm2, xmm1
006D894D  addss    xmm2, xmm0
006D8951  movss    dword ptr [rax], xmm2
006D8955  add      rax, 4
006D8959  add      r8d, -1
006D895D  jne      0x6d8920  ; -> 006D8920
006D895F  movaps   xmm6, xmmword ptr [rsp + 0x60]
006D8964  jmp      0x6d8add  ; -> 006D8ADD
006D8969  mov      rax, qword ptr [rbp - 0x30]
006D896D  mov      r9, qword ptr [rbp - 0x38]
006D8971  sub      rcx, rax
006D8974  mov      rdx, qword ptr [r11]
006D8977  sub      r9, rax
006D897A  movss    xmm4, dword ptr [rbp - 0x48]
006D897F  movss    xmm5, dword ptr [rbp - 0x4c]
006D8984  nop      dword ptr [rax]
006D8988  nop      dword ptr [rax + rax]
006D8990  movaps   xmm2, xmm3
006D8993  movaps   xmm0, xmm5
006D8996  mulss    xmm2, dword ptr [rcx + rax]
006D899B  movaps   xmm1, xmm4
006D899E  mulss    xmm0, dword ptr [r9 + rax]
006D89A4  mulss    xmm1, dword ptr [rax]
006D89A8  add      rax, 4
006D89AC  addss    xmm2, xmm0
006D89B0  addss    xmm2, xmm1
006D89B4  movss    dword ptr [rdx], xmm2
006D89B8  add      rdx, 4
006D89BC  add      r8d, -1
006D89C0  jne      0x6d8990  ; -> 006D8990
006D89C2  jmp      0x6d8add  ; -> 006D8ADD
006D89C7  mov      rax, qword ptr [r11]
006D89CA  mov      rdx, qword ptr [rbp - 0x38]
006D89CE  movss    xmm2, dword ptr [rbp - 0x4c]
006D89D3  sub      rdx, rax
006D89D6  sub      rcx, rax
006D89D9  nop      dword ptr [rax]
006D89E0  movaps   xmm1, xmm3
006D89E3  movaps   xmm0, xmm2
006D89E6  mulss    xmm1, dword ptr [rcx + rax]
006D89EB  mulss    xmm0, dword ptr [rdx + rax]
006D89F0  addss    xmm1, xmm0
006D89F4  movss    dword ptr [rax], xmm1
006D89F8  add      rax, 4
006D89FC  add      r8d, -1
006D8A00  jne      0x6d89e0  ; -> 006D89E0
006D8A02  jmp      0x6d8add  ; -> 006D8ADD
006D8A07  ucomiss  xmm3, dword ptr [rip + 0x161319a]  ; -> 01CEBBA8 [f32 1]
006D8A0E  movaps   xmm1, xmm3
006D8A11  shufps   xmm1, xmm1, 0
006D8A15  jp       0x6d8a2d  ; -> 006D8A2D
006D8A17  jne      0x6d8a2d  ; -> 006D8A2D
006D8A19  mov      rdx, rcx
006D8A1C  shl      r8, 2
006D8A20  mov      rcx, qword ptr [r11]
006D8A23  call     0x861eba  ; -> 00861EBA fn
006D8A28  jmp      0x6d8add  ; -> 006D8ADD
006D8A2D  mov      rdx, qword ptr [r11]
006D8A30  test     r8d, r8d
006D8A33  je       0x6d8add  ; -> 006D8ADD
006D8A39  cmp      r8d, 8
006D8A3D  jb       0x6d8a75  ; -> 006D8A75
006D8A3F  mov      eax, r8d
006D8A42  and      eax, 0xfffffff8
006D8A45  nop      word ptr [rax + rax]
006D8A50  movups   xmm0, xmmword ptr [rcx]
006D8A53  add      r10d, 8
006D8A57  mulps    xmm0, xmm1
006D8A5A  movups   xmmword ptr [rdx], xmm0
006D8A5D  movups   xmm0, xmmword ptr [rcx + 0x10]
006D8A61  add      rcx, 0x20
006D8A65  mulps    xmm0, xmm1
006D8A68  movups   xmmword ptr [rdx + 0x10], xmm0
006D8A6C  add      rdx, 0x20
006D8A70  cmp      r10d, eax
006D8A73  jb       0x6d8a50  ; -> 006D8A50
006D8A75  cmp      r10d, r8d
006D8A78  jae      0x6d8add  ; -> 006D8ADD
006D8A7A  mov      eax, r8d
006D8A7D  sub      eax, r10d
006D8A80  cmp      eax, 4
006D8A83  jb       0x6d8ab7  ; -> 006D8AB7
006D8A85  mov      eax, r8d
006D8A88  sub      eax, r10d
006D8A8B  sub      eax, 4
006D8A8E  shr      eax, 2
006D8A91  inc      eax
006D8A93  mov      r9d, eax
006D8A96  lea      r10d, [r10 + rax*4]
006D8A9A  nop      word ptr [rax + rax]
006D8AA0  movups   xmm0, xmmword ptr [rcx]
006D8AA3  add      rcx, 0x10
006D8AA7  mulps    xmm0, xmm3
006D8AAA  movups   xmmword ptr [rdx], xmm0
006D8AAD  add      rdx, 0x10
006D8AB1  sub      r9, 1
006D8AB5  jne      0x6d8aa0  ; -> 006D8AA0
006D8AB7  cmp      r10d, r8d
006D8ABA  jae      0x6d8add  ; -> 006D8ADD
006D8ABC  sub      rdx, rcx
006D8ABF  sub      r8d, r10d
006D8AC2  mov      eax, r8d
006D8AC5  lea      rcx, [rcx + 4]
006D8AC9  movaps   xmm0, xmm3
006D8ACC  mulss    xmm0, dword ptr [rcx - 4]
006D8AD1  movss    dword ptr [rdx + rcx - 4], xmm0
006D8AD7  sub      rax, 1
006D8ADB  jne      0x6d8ac5  ; -> 006D8AC5
006D8ADD  mov      rcx, qword ptr [rbp - 0x20]
006D8AE1  xor      rcx, rsp
006D8AE4  call     0x808c40  ; -> 00808C40 fn
006D8AE9  mov      rbx, qword ptr [rsp + 0x80]
006D8AF1  add      rsp, 0x70
006D8AF5  pop      rbp
006D8AF6  ret      
```

## 006D8B00 (807 B, extent 006D8B00-006D8E27)

Documented callee on this page: `00861EBA`

```
006D8B00  test     edx, edx
006D8B02  je       0x6d8e26  ; -> 006D8E26
006D8B08  mov      qword ptr [rsp + 8], rbx
006D8B0D  push     rbp
006D8B0E  mov      rbp, rsp
006D8B11  sub      rsp, 0x70
006D8B15  mov      rax, qword ptr [rip + 0x186bd14]  ; -> 01F44830 [u64 0x00002B992DDFA232]
006D8B1C  xor      rax, rsp
006D8B1F  mov      qword ptr [rbp - 0x20], rax
006D8B23  movss    xmm3, dword ptr [rcx]
006D8B27  xor      r10d, r10d
006D8B2A  xorps    xmm0, xmm0
006D8B2D  mov      r11, r9
006D8B30  ucomiss  xmm3, xmm0
006D8B33  mov      rbx, rcx
006D8B36  mov      r9d, r10d
006D8B39  jp       0x6d8b48  ; -> 006D8B48
006D8B3B  jne      0x6d8b48  ; -> 006D8B48
006D8B3D  mov      rcx, qword ptr [rbp - 0x40]
006D8B41  movss    xmm3, dword ptr [rbp - 0x50]
006D8B46  jmp      0x6d8b5a  ; -> 006D8B5A
006D8B48  mov      rcx, qword ptr [r8]
006D8B4B  mov      r9d, 1
006D8B51  mov      qword ptr [rbp - 0x40], rcx
006D8B55  movss    dword ptr [rbp - 0x50], xmm3
006D8B5A  movss    xmm1, dword ptr [rbx + 4]
006D8B5F  ucomiss  xmm1, xmm0
006D8B62  jp       0x6d8b66  ; -> 006D8B66
006D8B64  je       0x6d8b84  ; -> 006D8B84
006D8B66  mov      rax, qword ptr [r8 + 8]
006D8B6A  mov      ecx, r9d
006D8B6D  inc      r9d
006D8B70  movss    dword ptr [rbp + rcx*4 - 0x50], xmm1
006D8B76  movss    xmm3, dword ptr [rbp - 0x50]
006D8B7B  mov      qword ptr [rbp + rcx*8 - 0x40], rax
006D8B80  mov      rcx, qword ptr [rbp - 0x40]
006D8B84  movss    xmm1, dword ptr [rbx + 8]
006D8B89  ucomiss  xmm1, xmm0
006D8B8C  jp       0x6d8b90  ; -> 006D8B90
006D8B8E  je       0x6d8bae  ; -> 006D8BAE
006D8B90  mov      rax, qword ptr [r8 + 0x10]
006D8B94  mov      ecx, r9d
006D8B97  inc      r9d
006D8B9A  movss    dword ptr [rbp + rcx*4 - 0x50], xmm1
006D8BA0  movss    xmm3, dword ptr [rbp - 0x50]
006D8BA5  mov      qword ptr [rbp + rcx*8 - 0x40], rax
006D8BAA  mov      rcx, qword ptr [rbp - 0x40]
006D8BAE  movss    xmm1, dword ptr [rbx + 0xc]
006D8BB3  ucomiss  xmm1, xmm0
006D8BB6  jp       0x6d8bba  ; -> 006D8BBA
006D8BB8  je       0x6d8bd8  ; -> 006D8BD8
006D8BBA  mov      rax, qword ptr [r8 + 0x18]
006D8BBE  mov      ecx, r9d
006D8BC1  inc      r9d
006D8BC4  movss    dword ptr [rbp + rcx*4 - 0x50], xmm1
006D8BCA  movss    xmm3, dword ptr [rbp - 0x50]
006D8BCF  mov      qword ptr [rbp + rcx*8 - 0x40], rax
006D8BD4  mov      rcx, qword ptr [rbp - 0x40]
006D8BD8  shufps   xmm3, xmm3, 0
006D8BDC  lea      r8d, [rdx*4]
006D8BE4  sub      r9d, 1
006D8BE8  je       0x6d8d37  ; -> 006D8D37
006D8BEE  sub      r9d, 1
006D8BF2  je       0x6d8cf7  ; -> 006D8CF7
006D8BF8  sub      r9d, 1
006D8BFC  je       0x6d8c99  ; -> 006D8C99
006D8C02  cmp      r9d, 1
006D8C06  je       0x6d8c1b  ; -> 006D8C1B
006D8C08  mov      rcx, qword ptr [r11]
006D8C0B  xor      edx, edx
006D8C0D  shl      r8, 2
006D8C11  call     0x861ec0  ; -> 00861EC0 fn
006D8C16  jmp      0x6d8e0d  ; -> 006D8E0D
006D8C1B  mov      rdx, qword ptr [rbp - 0x38]
006D8C1F  mov      r9, qword ptr [rbp - 0x28]
006D8C23  sub      rdx, rcx
006D8C26  mov      r10, qword ptr [rbp - 0x30]
006D8C2A  sub      r9, rcx
006D8C2D  mov      rax, qword ptr [r11]
006D8C30  sub      r10, rcx
006D8C33  movss    xmm4, dword ptr [rbp - 0x44]
006D8C38  movss    xmm5, dword ptr [rbp - 0x48]
006D8C3D  movaps   xmmword ptr [rsp + 0x60], xmm6
006D8C42  movss    xmm6, dword ptr [rbp - 0x4c]
006D8C47  nop      word ptr [rax + rax]
006D8C50  movaps   xmm0, xmm3
006D8C53  movaps   xmm2, xmm6
006D8C56  mulss    xmm2, dword ptr [rdx + rcx]
006D8C5B  movaps   xmm1, xmm5
006D8C5E  mulss    xmm0, dword ptr [rcx]
006D8C62  mulss    xmm1, dword ptr [r10 + rcx]
006D8C68  addss    xmm2, xmm0
006D8C6C  movaps   xmm0, xmm4
006D8C6F  mulss    xmm0, dword ptr [r9 + rcx]
006D8C75  add      rcx, 4
006D8C79  addss    xmm2, xmm1
006D8C7D  addss    xmm2, xmm0
006D8C81  movss    dword ptr [rax], xmm2
006D8C85  add      rax, 4
006D8C89  add      r8d, -1
006D8C8D  jne      0x6d8c50  ; -> 006D8C50
006D8C8F  movaps   xmm6, xmmword ptr [rsp + 0x60]
006D8C94  jmp      0x6d8e0d  ; -> 006D8E0D
006D8C99  mov      rax, qword ptr [rbp - 0x30]
006D8C9D  mov      r9, qword ptr [rbp - 0x38]
006D8CA1  sub      rcx, rax
006D8CA4  mov      rdx, qword ptr [r11]
006D8CA7  sub      r9, rax
006D8CAA  movss    xmm4, dword ptr [rbp - 0x48]
006D8CAF  movss    xmm5, dword ptr [rbp - 0x4c]
006D8CB4  nop      dword ptr [rax]
006D8CB8  nop      dword ptr [rax + rax]
006D8CC0  movaps   xmm2, xmm3
006D8CC3  movaps   xmm0, xmm5
006D8CC6  mulss    xmm2, dword ptr [rcx + rax]
006D8CCB  movaps   xmm1, xmm4
006D8CCE  mulss    xmm0, dword ptr [r9 + rax]
006D8CD4  mulss    xmm1, dword ptr [rax]
006D8CD8  add      rax, 4
006D8CDC  addss    xmm2, xmm0
006D8CE0  addss    xmm2, xmm1
006D8CE4  movss    dword ptr [rdx], xmm2
006D8CE8  add      rdx, 4
006D8CEC  add      r8d, -1
006D8CF0  jne      0x6d8cc0  ; -> 006D8CC0
006D8CF2  jmp      0x6d8e0d  ; -> 006D8E0D
006D8CF7  mov      rax, qword ptr [r11]
006D8CFA  mov      rdx, qword ptr [rbp - 0x38]
006D8CFE  movss    xmm2, dword ptr [rbp - 0x4c]
006D8D03  sub      rdx, rax
006D8D06  sub      rcx, rax
006D8D09  nop      dword ptr [rax]
006D8D10  movaps   xmm1, xmm3
006D8D13  movaps   xmm0, xmm2
006D8D16  mulss    xmm1, dword ptr [rcx + rax]
006D8D1B  mulss    xmm0, dword ptr [rdx + rax]
006D8D20  addss    xmm1, xmm0
006D8D24  movss    dword ptr [rax], xmm1
006D8D28  add      rax, 4
006D8D2C  add      r8d, -1
006D8D30  jne      0x6d8d10  ; -> 006D8D10
006D8D32  jmp      0x6d8e0d  ; -> 006D8E0D
006D8D37  ucomiss  xmm3, dword ptr [rip + 0x1612e6a]  ; -> 01CEBBA8 [f32 1]
006D8D3E  movaps   xmm1, xmm3
006D8D41  shufps   xmm1, xmm1, 0
006D8D45  jp       0x6d8d5d  ; -> 006D8D5D
006D8D47  jne      0x6d8d5d  ; -> 006D8D5D
006D8D49  mov      rdx, rcx
006D8D4C  shl      r8, 2
006D8D50  mov      rcx, qword ptr [r11]
006D8D53  call     0x861eba  ; -> 00861EBA fn
006D8D58  jmp      0x6d8e0d  ; -> 006D8E0D
006D8D5D  mov      rdx, qword ptr [r11]
006D8D60  test     r8d, r8d
006D8D63  je       0x6d8e0d  ; -> 006D8E0D
006D8D69  cmp      r8d, 8
006D8D6D  jb       0x6d8da5  ; -> 006D8DA5
006D8D6F  mov      eax, r8d
006D8D72  and      eax, 0xfffffff8
006D8D75  nop      word ptr [rax + rax]
006D8D80  movups   xmm0, xmmword ptr [rcx]
006D8D83  add      r10d, 8
006D8D87  mulps    xmm0, xmm1
006D8D8A  movups   xmmword ptr [rdx], xmm0
006D8D8D  movups   xmm0, xmmword ptr [rcx + 0x10]
006D8D91  add      rcx, 0x20
006D8D95  mulps    xmm0, xmm1
006D8D98  movups   xmmword ptr [rdx + 0x10], xmm0
006D8D9C  add      rdx, 0x20
006D8DA0  cmp      r10d, eax
006D8DA3  jb       0x6d8d80  ; -> 006D8D80
006D8DA5  cmp      r10d, r8d
006D8DA8  jae      0x6d8e0d  ; -> 006D8E0D
006D8DAA  mov      eax, r8d
006D8DAD  sub      eax, r10d
006D8DB0  cmp      eax, 4
006D8DB3  jb       0x6d8de7  ; -> 006D8DE7
006D8DB5  mov      eax, r8d
006D8DB8  sub      eax, r10d
006D8DBB  sub      eax, 4
006D8DBE  shr      eax, 2
006D8DC1  inc      eax
006D8DC3  mov      r9d, eax
006D8DC6  lea      r10d, [r10 + rax*4]
006D8DCA  nop      word ptr [rax + rax]
006D8DD0  movups   xmm0, xmmword ptr [rcx]
006D8DD3  add      rcx, 0x10
006D8DD7  mulps    xmm0, xmm3
006D8DDA  movups   xmmword ptr [rdx], xmm0
006D8DDD  add      rdx, 0x10
006D8DE1  sub      r9, 1
006D8DE5  jne      0x6d8dd0  ; -> 006D8DD0
006D8DE7  cmp      r10d, r8d
006D8DEA  jae      0x6d8e0d  ; -> 006D8E0D
006D8DEC  sub      rdx, rcx
006D8DEF  sub      r8d, r10d
006D8DF2  mov      eax, r8d
006D8DF5  lea      rcx, [rcx + 4]
006D8DF9  movaps   xmm0, xmm3
006D8DFC  mulss    xmm0, dword ptr [rcx - 4]
006D8E01  movss    dword ptr [rdx + rcx - 4], xmm0
006D8E07  sub      rax, 1
006D8E0B  jne      0x6d8df5  ; -> 006D8DF5
006D8E0D  mov      rcx, qword ptr [rbp - 0x20]
006D8E11  xor      rcx, rsp
006D8E14  call     0x808c40  ; -> 00808C40 fn
006D8E19  mov      rbx, qword ptr [rsp + 0x80]
006D8E21  add      rsp, 0x70
006D8E25  pop      rbp
006D8E26  ret      
```

## 00793490 (71 B, extent 00793490-007934D7)

Documented callee on this page: `00584730`

```
00793490  push     rbx
00793492  sub      rsp, 0x30
00793496  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0079349F  mov      rbx, rcx
007934A2  mov      ecx, dword ptr [rcx + 8]
007934A5  mov      eax, ecx
007934A7  shr      eax, 0x1f
007934AA  not      al
007934AC  test     al, 1
007934AE  je       0x7934c8  ; -> 007934C8
007934B0  btr      ecx, 0x1f
007934B4  cmp      ecx, 1
007934B7  jbe      0x7934c8  ; -> 007934C8
007934B9  mov      rcx, qword ptr [rbx + 0x10]
007934BD  test     rcx, rcx
007934C0  je       0x7934c8  ; -> 007934C8
007934C2  call     0x584730  ; -> 00584730 fn
007934C7  nop      
007934C8  xor      eax, eax
007934CA  mov      qword ptr [rbx + 0x10], rax
007934CE  mov      dword ptr [rbx + 8], eax
007934D1  add      rsp, 0x30
007934D5  pop      rbx
007934D6  ret      
```

## 00795800 (510 B, extent 00795800-007959FE)

Documented callee on this page: `005CDAA0`

```
00795800  mov      qword ptr [rsp + 8], rbx
00795805  push     rdi
00795806  sub      rsp, 0x20
0079580A  mov      rbx, rdx
0079580D  test     rcx, rcx
00795810  je       0x7959cd  ; -> 007959CD
00795816  test     rdx, rdx
00795819  je       0x7959cd  ; -> 007959CD
0079581F  mov      rax, qword ptr [rcx + 0xdf8]
00795826  mov      rdi, qword ptr [rax + 0x88]
0079582D  test     rdi, rdi
00795830  je       0x7959cd  ; -> 007959CD
00795836  lea      rdx, [rip + 0x130223]  ; -> 008C5A60 [str "Circle"]
0079583D  mov      rcx, rbx
00795840  call     qword ptr [rip + 0x12d7ba]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795846  test     eax, eax
00795848  jne      0x795860  ; -> 00795860
0079584A  mov      eax, 0x32
0079584F  mov      byte ptr [rax + rdi], 1
00795853  xor      eax, eax
00795855  mov      rbx, qword ptr [rsp + 0x30]
0079585A  add      rsp, 0x20
0079585E  pop      rdi
0079585F  ret      
00795860  lea      rdx, [rip + 0x130201]  ; -> 008C5A68 [str "Cross"]
00795867  mov      rcx, rbx
0079586A  call     qword ptr [rip + 0x12d790]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795870  test     eax, eax
00795872  jne      0x79588a  ; -> 0079588A
00795874  mov      eax, 0x31
00795879  mov      byte ptr [rax + rdi], 1
0079587D  xor      eax, eax
0079587F  mov      rbx, qword ptr [rsp + 0x30]
00795884  add      rsp, 0x20
00795888  pop      rdi
00795889  ret      
0079588A  lea      rdx, [rip + 0x151cfb7]  ; -> 01CB2848 [str "Triangle"]
00795891  mov      rcx, rbx
00795894  call     qword ptr [rip + 0x12d766]  ; -> 008C3000 [u64 0x0000000001CCEF78]
0079589A  test     eax, eax
0079589C  jne      0x7958b4  ; -> 007958B4
0079589E  mov      eax, 0x33
007958A3  mov      byte ptr [rax + rdi], 1
007958A7  xor      eax, eax
007958A9  mov      rbx, qword ptr [rsp + 0x30]
007958AE  add      rsp, 0x20
007958B2  pop      rdi
007958B3  ret      
007958B4  lea      rdx, [rip + 0x151cf99]  ; -> 01CB2854 [str "Square"]
007958BB  mov      rcx, rbx
007958BE  call     qword ptr [rip + 0x12d73c]  ; -> 008C3000 [u64 0x0000000001CCEF78]
007958C4  test     eax, eax
007958C6  jne      0x7958de  ; -> 007958DE
007958C8  mov      eax, 0x30
007958CD  mov      byte ptr [rax + rdi], 1
007958D1  xor      eax, eax
007958D3  mov      rbx, qword ptr [rsp + 0x30]
007958D8  add      rsp, 0x20
007958DC  pop      rdi
007958DD  ret      
007958DE  lea      rdx, [rip + 0x151cf77]  ; -> 01CB285C [str "Start"]
007958E5  mov      rcx, rbx
007958E8  call     qword ptr [rip + 0x12d712]  ; -> 008C3000 [u64 0x0000000001CCEF78]
007958EE  test     eax, eax
007958F0  jne      0x795908  ; -> 00795908
007958F2  mov      eax, 0x39
007958F7  mov      byte ptr [rax + rdi], 1
007958FB  xor      eax, eax
007958FD  mov      rbx, qword ptr [rsp + 0x30]
00795902  add      rsp, 0x20
00795906  pop      rdi
00795907  ret      
00795908  lea      rdx, [rip + 0x151cf55]  ; -> 01CB2864 [str "Select"]
0079590F  mov      rcx, rbx
00795912  call     qword ptr [rip + 0x12d6e8]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795918  test     eax, eax
0079591A  jne      0x795932  ; -> 00795932
0079591C  mov      eax, 0x38
00795921  mov      byte ptr [rax + rdi], 1
00795925  xor      eax, eax
00795927  mov      rbx, qword ptr [rsp + 0x30]
0079592C  add      rsp, 0x20
00795930  pop      rdi
00795931  ret      
00795932  lea      rdx, [rip + 0x151cf33]  ; -> 01CB286C
00795939  mov      rcx, rbx
0079593C  call     qword ptr [rip + 0x12d6be]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795942  test     eax, eax
00795944  jne      0x79595c  ; -> 0079595C
00795946  mov      eax, 0x3c
0079594B  mov      byte ptr [rax + rdi], 1
0079594F  xor      eax, eax
00795951  mov      rbx, qword ptr [rsp + 0x30]
00795956  add      rsp, 0x20
0079595A  pop      rdi
0079595B  ret      
0079595C  lea      rdx, [rip + 0x151cf0d]  ; -> 01CB2870 [str "Down"]
00795963  mov      rcx, rbx
00795966  call     qword ptr [rip + 0x12d694]  ; -> 008C3000 [u64 0x0000000001CCEF78]
0079596C  test     eax, eax
0079596E  jne      0x795986  ; -> 00795986
00795970  mov      eax, 0x3e
00795975  mov      byte ptr [rax + rdi], 1
00795979  xor      eax, eax
0079597B  mov      rbx, qword ptr [rsp + 0x30]
00795980  add      rsp, 0x20
00795984  pop      rdi
00795985  ret      
00795986  lea      rdx, [rip + 0x151ceeb]  ; -> 01CB2878 [str "Left"]
0079598D  mov      rcx, rbx
00795990  call     qword ptr [rip + 0x12d66a]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795996  test     eax, eax
00795998  jne      0x7959b0  ; -> 007959B0
0079599A  mov      eax, 0x3f
0079599F  mov      byte ptr [rax + rdi], 1
007959A3  xor      eax, eax
007959A5  mov      rbx, qword ptr [rsp + 0x30]
007959AA  add      rsp, 0x20
007959AE  pop      rdi
007959AF  ret      
007959B0  lea      rdx, [rip + 0x151cec9]  ; -> 01CB2880 [str "Right"]
007959B7  mov      rcx, rbx
007959BA  call     qword ptr [rip + 0x12d640]  ; -> 008C3000 [u64 0x0000000001CCEF78]
007959C0  test     eax, eax
007959C2  jne      0x7959da  ; -> 007959DA
007959C4  mov      eax, 0x3d
007959C9  mov      byte ptr [rax + rdi], 1
007959CD  xor      eax, eax
007959CF  mov      rbx, qword ptr [rsp + 0x30]
007959D4  add      rsp, 0x20
007959D8  pop      rdi
007959D9  ret      
007959DA  mov      r8, rbx
007959DD  lea      rdx, [rip + 0x151cea4]  ; -> 01CB2888
007959E4  mov      ecx, 2
007959E9  call     0x5cdaa0  ; -> 005CDAA0 fn
007959EE  mov      rbx, qword ptr [rsp + 0x30]
007959F3  mov      eax, 5
007959F8  add      rsp, 0x20
007959FC  pop      rdi
007959FD  ret      
```

## 00795A00 (510 B, extent 00795A00-00795BFE)

Documented callee on this page: `005CDAA0`

```
00795A00  mov      qword ptr [rsp + 8], rbx
00795A05  push     rdi
00795A06  sub      rsp, 0x20
00795A0A  mov      rbx, rdx
00795A0D  test     rcx, rcx
00795A10  je       0x795bcd  ; -> 00795BCD
00795A16  test     rdx, rdx
00795A19  je       0x795bcd  ; -> 00795BCD
00795A1F  mov      rax, qword ptr [rcx + 0xdf8]
00795A26  mov      rdi, qword ptr [rax + 0x88]
00795A2D  test     rdi, rdi
00795A30  je       0x795bcd  ; -> 00795BCD
00795A36  lea      rdx, [rip + 0x130023]  ; -> 008C5A60 [str "Circle"]
00795A3D  mov      rcx, rbx
00795A40  call     qword ptr [rip + 0x12d5ba]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795A46  test     eax, eax
00795A48  jne      0x795a60  ; -> 00795A60
00795A4A  mov      eax, 0x32
00795A4F  mov      byte ptr [rax + rdi], 0
00795A53  xor      eax, eax
00795A55  mov      rbx, qword ptr [rsp + 0x30]
00795A5A  add      rsp, 0x20
00795A5E  pop      rdi
00795A5F  ret      
00795A60  lea      rdx, [rip + 0x130001]  ; -> 008C5A68 [str "Cross"]
00795A67  mov      rcx, rbx
00795A6A  call     qword ptr [rip + 0x12d590]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795A70  test     eax, eax
00795A72  jne      0x795a8a  ; -> 00795A8A
00795A74  mov      eax, 0x31
00795A79  mov      byte ptr [rax + rdi], 0
00795A7D  xor      eax, eax
00795A7F  mov      rbx, qword ptr [rsp + 0x30]
00795A84  add      rsp, 0x20
00795A88  pop      rdi
00795A89  ret      
00795A8A  lea      rdx, [rip + 0x151cdb7]  ; -> 01CB2848 [str "Triangle"]
00795A91  mov      rcx, rbx
00795A94  call     qword ptr [rip + 0x12d566]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795A9A  test     eax, eax
00795A9C  jne      0x795ab4  ; -> 00795AB4
00795A9E  mov      eax, 0x33
00795AA3  mov      byte ptr [rax + rdi], 0
00795AA7  xor      eax, eax
00795AA9  mov      rbx, qword ptr [rsp + 0x30]
00795AAE  add      rsp, 0x20
00795AB2  pop      rdi
00795AB3  ret      
00795AB4  lea      rdx, [rip + 0x151cd99]  ; -> 01CB2854 [str "Square"]
00795ABB  mov      rcx, rbx
00795ABE  call     qword ptr [rip + 0x12d53c]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795AC4  test     eax, eax
00795AC6  jne      0x795ade  ; -> 00795ADE
00795AC8  mov      eax, 0x30
00795ACD  mov      byte ptr [rax + rdi], 0
00795AD1  xor      eax, eax
00795AD3  mov      rbx, qword ptr [rsp + 0x30]
00795AD8  add      rsp, 0x20
00795ADC  pop      rdi
00795ADD  ret      
00795ADE  lea      rdx, [rip + 0x151cd77]  ; -> 01CB285C [str "Start"]
00795AE5  mov      rcx, rbx
00795AE8  call     qword ptr [rip + 0x12d512]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795AEE  test     eax, eax
00795AF0  jne      0x795b08  ; -> 00795B08
00795AF2  mov      eax, 0x39
00795AF7  mov      byte ptr [rax + rdi], 0
00795AFB  xor      eax, eax
00795AFD  mov      rbx, qword ptr [rsp + 0x30]
00795B02  add      rsp, 0x20
00795B06  pop      rdi
00795B07  ret      
00795B08  lea      rdx, [rip + 0x151cd55]  ; -> 01CB2864 [str "Select"]
00795B0F  mov      rcx, rbx
00795B12  call     qword ptr [rip + 0x12d4e8]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795B18  test     eax, eax
00795B1A  jne      0x795b32  ; -> 00795B32
00795B1C  mov      eax, 0x38
00795B21  mov      byte ptr [rax + rdi], 0
00795B25  xor      eax, eax
00795B27  mov      rbx, qword ptr [rsp + 0x30]
00795B2C  add      rsp, 0x20
00795B30  pop      rdi
00795B31  ret      
00795B32  lea      rdx, [rip + 0x151cd33]  ; -> 01CB286C
00795B39  mov      rcx, rbx
00795B3C  call     qword ptr [rip + 0x12d4be]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795B42  test     eax, eax
00795B44  jne      0x795b5c  ; -> 00795B5C
00795B46  mov      eax, 0x3c
00795B4B  mov      byte ptr [rax + rdi], 0
00795B4F  xor      eax, eax
00795B51  mov      rbx, qword ptr [rsp + 0x30]
00795B56  add      rsp, 0x20
00795B5A  pop      rdi
00795B5B  ret      
00795B5C  lea      rdx, [rip + 0x151cd0d]  ; -> 01CB2870 [str "Down"]
00795B63  mov      rcx, rbx
00795B66  call     qword ptr [rip + 0x12d494]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795B6C  test     eax, eax
00795B6E  jne      0x795b86  ; -> 00795B86
00795B70  mov      eax, 0x3e
00795B75  mov      byte ptr [rax + rdi], 0
00795B79  xor      eax, eax
00795B7B  mov      rbx, qword ptr [rsp + 0x30]
00795B80  add      rsp, 0x20
00795B84  pop      rdi
00795B85  ret      
00795B86  lea      rdx, [rip + 0x151cceb]  ; -> 01CB2878 [str "Left"]
00795B8D  mov      rcx, rbx
00795B90  call     qword ptr [rip + 0x12d46a]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795B96  test     eax, eax
00795B98  jne      0x795bb0  ; -> 00795BB0
00795B9A  mov      eax, 0x3f
00795B9F  mov      byte ptr [rax + rdi], 0
00795BA3  xor      eax, eax
00795BA5  mov      rbx, qword ptr [rsp + 0x30]
00795BAA  add      rsp, 0x20
00795BAE  pop      rdi
00795BAF  ret      
00795BB0  lea      rdx, [rip + 0x151ccc9]  ; -> 01CB2880 [str "Right"]
00795BB7  mov      rcx, rbx
00795BBA  call     qword ptr [rip + 0x12d440]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795BC0  test     eax, eax
00795BC2  jne      0x795bda  ; -> 00795BDA
00795BC4  mov      eax, 0x3d
00795BC9  mov      byte ptr [rax + rdi], 0
00795BCD  xor      eax, eax
00795BCF  mov      rbx, qword ptr [rsp + 0x30]
00795BD4  add      rsp, 0x20
00795BD8  pop      rdi
00795BD9  ret      
00795BDA  mov      r8, rbx
00795BDD  lea      rdx, [rip + 0x151cca4]  ; -> 01CB2888
00795BE4  mov      ecx, 2
00795BE9  call     0x5cdaa0  ; -> 005CDAA0 fn
00795BEE  mov      rbx, qword ptr [rsp + 0x30]
00795BF3  mov      eax, 5
00795BF8  add      rsp, 0x20
00795BFC  pop      rdi
00795BFD  ret      
```

## 00795C00 (439 B, extent 00795C00-00795DB7)

Documented callee on this page: `005CDAA0`

```
00795C00  mov      qword ptr [rsp + 8], rbx
00795C05  mov      qword ptr [rsp + 0x10], rsi
00795C0A  push     rdi
00795C0B  sub      rsp, 0x20
00795C0F  mov      rbx, rdx
00795C12  mov      rdi, rcx
00795C15  test     rcx, rcx
00795C18  je       0x795d7c  ; -> 00795D7C
00795C1E  test     rdx, rdx
00795C21  je       0x795d7c  ; -> 00795D7C
00795C27  mov      rax, qword ptr [rcx + 0xdf8]
00795C2E  mov      rsi, qword ptr [rax + 0x88]
00795C35  test     rsi, rsi
00795C38  je       0x795d5d  ; -> 00795D5D
00795C3E  lea      rdx, [rip + 0x12fe1b]  ; -> 008C5A60 [str "Circle"]
00795C45  mov      rcx, rbx
00795C48  call     qword ptr [rip + 0x12d3b2]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795C4E  test     eax, eax
00795C50  jne      0x795c5c  ; -> 00795C5C
00795C52  mov      eax, 0x32
00795C57  jmp      0x795d59  ; -> 00795D59
00795C5C  lea      rdx, [rip + 0x12fe05]  ; -> 008C5A68 [str "Cross"]
00795C63  mov      rcx, rbx
00795C66  call     qword ptr [rip + 0x12d394]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795C6C  test     eax, eax
00795C6E  jne      0x795c7a  ; -> 00795C7A
00795C70  mov      eax, 0x31
00795C75  jmp      0x795d59  ; -> 00795D59
00795C7A  lea      rdx, [rip + 0x151cbc7]  ; -> 01CB2848 [str "Triangle"]
00795C81  mov      rcx, rbx
00795C84  call     qword ptr [rip + 0x12d376]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795C8A  test     eax, eax
00795C8C  jne      0x795c98  ; -> 00795C98
00795C8E  mov      eax, 0x33
00795C93  jmp      0x795d59  ; -> 00795D59
00795C98  lea      rdx, [rip + 0x151cbb5]  ; -> 01CB2854 [str "Square"]
00795C9F  mov      rcx, rbx
00795CA2  call     qword ptr [rip + 0x12d358]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795CA8  test     eax, eax
00795CAA  jne      0x795cb6  ; -> 00795CB6
00795CAC  mov      eax, 0x30
00795CB1  jmp      0x795d59  ; -> 00795D59
00795CB6  lea      rdx, [rip + 0x151cb9f]  ; -> 01CB285C [str "Start"]
00795CBD  mov      rcx, rbx
00795CC0  call     qword ptr [rip + 0x12d33a]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795CC6  test     eax, eax
00795CC8  jne      0x795cd4  ; -> 00795CD4
00795CCA  mov      eax, 0x39
00795CCF  jmp      0x795d59  ; -> 00795D59
00795CD4  lea      rdx, [rip + 0x151cb89]  ; -> 01CB2864 [str "Select"]
00795CDB  mov      rcx, rbx
00795CDE  call     qword ptr [rip + 0x12d31c]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795CE4  test     eax, eax
00795CE6  jne      0x795cef  ; -> 00795CEF
00795CE8  mov      eax, 0x38
00795CED  jmp      0x795d59  ; -> 00795D59
00795CEF  lea      rdx, [rip + 0x151cb76]  ; -> 01CB286C
00795CF6  mov      rcx, rbx
00795CF9  call     qword ptr [rip + 0x12d301]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795CFF  test     eax, eax
00795D01  jne      0x795d0a  ; -> 00795D0A
00795D03  mov      eax, 0x3c
00795D08  jmp      0x795d59  ; -> 00795D59
00795D0A  lea      rdx, [rip + 0x151cb5f]  ; -> 01CB2870 [str "Down"]
00795D11  mov      rcx, rbx
00795D14  call     qword ptr [rip + 0x12d2e6]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795D1A  test     eax, eax
00795D1C  jne      0x795d25  ; -> 00795D25
00795D1E  mov      eax, 0x3e
00795D23  jmp      0x795d59  ; -> 00795D59
00795D25  lea      rdx, [rip + 0x151cb4c]  ; -> 01CB2878 [str "Left"]
00795D2C  mov      rcx, rbx
00795D2F  call     qword ptr [rip + 0x12d2cb]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795D35  test     eax, eax
00795D37  jne      0x795d40  ; -> 00795D40
00795D39  mov      eax, 0x3f
00795D3E  jmp      0x795d59  ; -> 00795D59
00795D40  lea      rdx, [rip + 0x151cb39]  ; -> 01CB2880 [str "Right"]
00795D47  mov      rcx, rbx
00795D4A  call     qword ptr [rip + 0x12d2b0]  ; -> 008C3000 [u64 0x0000000001CCEF78]
00795D50  test     eax, eax
00795D52  jne      0x795d8e  ; -> 00795D8E
00795D54  mov      eax, 0x3d
00795D59  mov      byte ptr [rax + rsi], 1
00795D5D  mov      rax, qword ptr [rdi]
00795D60  mov      rcx, rdi
00795D63  call     qword ptr [rax + 0x38]
00795D66  test     eax, eax
00795D68  jne      0x795d7e  ; -> 00795D7E
00795D6A  xor      r8d, r8d
00795D6D  mov      rdx, rbx
00795D70  mov      rcx, rdi
00795D73  call     0x7a08f0  ; -> 007A08F0 fn
00795D78  test     eax, eax
00795D7A  jne      0x795d7e  ; -> 00795D7E
00795D7C  xor      eax, eax
00795D7E  mov      rbx, qword ptr [rsp + 0x30]
00795D83  mov      rsi, qword ptr [rsp + 0x38]
00795D88  add      rsp, 0x20
00795D8C  pop      rdi
00795D8D  ret      
00795D8E  mov      r8, rbx
00795D91  lea      rdx, [rip + 0x151caf0]  ; -> 01CB2888
00795D98  mov      ecx, 2
00795D9D  call     0x5cdaa0  ; -> 005CDAA0 fn
00795DA2  mov      rbx, qword ptr [rsp + 0x30]
00795DA7  mov      eax, 5
00795DAC  mov      rsi, qword ptr [rsp + 0x38]
00795DB1  add      rsp, 0x20
00795DB5  pop      rdi
00795DB6  ret      
```

## 00796280 (139 B, extent 00796280-0079630B)

Documented callee on this page: `00808C40`

```
00796280  sub      rsp, 0x48
00796284  mov      rax, qword ptr [rip + 0x17ae5a5]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0079628B  xor      rax, rsp
0079628E  mov      qword ptr [rsp + 0x38], rax
00796293  mov      eax, dword ptr [rcx + 0x18]
00796296  mov      r9, rdx
00796299  test     al, 3
0079629B  je       0x7962f4  ; -> 007962F4
0079629D  mov      dword ptr [rsp + 0x28], eax
007962A1  lea      r8, [rsp + 0x20]
007962A6  mov      rax, qword ptr [rdx]
007962A9  mov      rcx, r9
007962AC  mov      edx, 4
007962B1  mov      dword ptr [rsp + 0x20], 0x18
007962B9  mov      dword ptr [rsp + 0x24], 0x10
007962C1  mov      dword ptr [rsp + 0x2c], 2
007962C9  mov      dword ptr [rsp + 0x30], 0xffffff01
007962D1  mov      dword ptr [rsp + 0x34], 0xff
007962D9  call     qword ptr [rax + 0x30]
007962DC  test     eax, eax
007962DE  jns      0x7962f4  ; -> 007962F4
007962E0  xor      eax, eax
007962E2  mov      rcx, qword ptr [rsp + 0x38]
007962E7  xor      rcx, rsp
007962EA  call     0x808c40  ; -> 00808C40 fn
007962EF  add      rsp, 0x48
007962F3  ret      
007962F4  mov      eax, 1
007962F9  mov      rcx, qword ptr [rsp + 0x38]
007962FE  xor      rcx, rsp
00796301  call     0x808c40  ; -> 00808C40 fn
00796306  add      rsp, 0x48
0079630A  ret      
```

## 007963C0 (203 B, extent 007963C0-0079648B)

Documented callee on this page: `00808F10`

```
007963C0  push     rbp
007963C2  sub      rsp, 0x40
007963C6  lea      rbp, [rsp + 0x30]
007963CB  mov      qword ptr [rbp + 0x20], rbx
007963CF  mov      qword ptr [rbp + 0x28], rdi
007963D3  mov      rax, qword ptr [rip + 0x17ae456]  ; -> 01F44830 [u64 0x00002B992DDFA232]
007963DA  xor      rax, rbp
007963DD  mov      qword ptr [rbp], rax
007963E1  mov      rdi, rcx
007963E4  or       r8, 0xffffffffffffffff
007963E8  nop      dword ptr [rax + rax]
007963F0  inc      r8
007963F3  cmp      byte ptr [rdx + r8], 0
007963F8  jne      0x7963f0  ; -> 007963F0
007963FA  inc      r8
007963FD  lea      rax, [r8 + 0xf]
00796401  cmp      rax, r8
00796404  ja       0x796410  ; -> 00796410
00796406  movabs   rax, 0xffffffffffffff0
00796410  and      rax, 0xfffffffffffffff0
00796414  call     0x808f10  ; -> 00808F10 fn
00796419  sub      rsp, rax
0079641C  lea      rbx, [rsp + 0x30]
00796421  mov      rcx, rbx
00796424  call     0x861eba  ; -> 00861EBA fn
00796429  cmp      byte ptr [rbx], 0
0079642C  mov      rax, rbx
0079642F  je       0x796447  ; -> 00796447
00796431  movzx    ecx, byte ptr [rax + 1]
00796435  lea      rax, [rax + 1]
00796439  cmp      cl, 0x2c
0079643C  je       0x796444  ; -> 00796444
0079643E  test     cl, cl
00796440  jne      0x796431  ; -> 00796431
00796442  jmp      0x796447  ; -> 00796447
00796444  mov      byte ptr [rax], 0
00796447  movss    xmm3, dword ptr [rdi + 0x60]
0079644C  lea      rdx, [rip + 0x151c3dd]  ; -> 01CB2830
00796453  mov      eax, dword ptr [rdi + 0x64]
00796456  mov      r8, rbx
00796459  cvtps2pd xmm3, xmm3
0079645C  mov      ecx, 2
00796461  mov      dword ptr [rsp + 0x20], eax
00796465  movq     r9, xmm3
0079646A  call     0x5cdaa0  ; -> 005CDAA0 fn
0079646F  xor      eax, eax
00796471  mov      rcx, qword ptr [rbp]
00796475  xor      rcx, rbp
00796478  call     0x808c40  ; -> 00808C40 fn
0079647D  mov      rbx, qword ptr [rbp + 0x20]
00796481  mov      rdi, qword ptr [rbp + 0x28]
00796485  lea      rsp, [rbp + 0x10]
00796489  pop      rbp
0079648A  ret      
```

## 00798EB0 (193 B, extent 00798EB0-00798F71)

Documented callee on this page: `00808C40`

```
00798EB0  push     rbx
00798EB2  push     rsi
00798EB3  push     rdi
00798EB4  sub      rsp, 0x50
00798EB8  mov      rax, qword ptr [rip + 0x17ab971]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00798EBF  xor      rax, rsp
00798EC2  mov      qword ptr [rsp + 0x40], rax
00798EC7  mov      rsi, r8
00798ECA  mov      rbx, rdx
00798ECD  mov      edi, ecx
00798ECF  cmp      ecx, 5
00798ED2  jne      0x798f47  ; -> 00798F47
00798ED4  cmp      rdx, qword ptr [rip + 0x270c36d]  ; -> 02EA5248
00798EDB  je       0x798f47  ; -> 00798F47
00798EDD  lea      rdx, [rsp + 0x30]
00798EE2  mov      rcx, rbx
00798EE5  call     qword ptr [rip + 0x1299e5]  ; -> 008C28D0 [u64 0x0000000001CCCA6C]
00798EEB  mov      eax, dword ptr [rip + 0x17a4b2f]  ; -> 01F3DA20 [u32 0x00000438]
00798EF1  mov      r10d, dword ptr [rsp + 0x3c]
00798EF6  cdq      
00798EF7  sub      r10d, dword ptr [rsp + 0x34]
00798EFC  sub      eax, edx
00798EFE  mov      r9d, dword ptr [rsp + 0x38]
00798F03  sub      r9d, dword ptr [rsp + 0x30]
00798F08  sar      eax, 1
00798F0A  mov      r8d, eax
00798F0D  mov      dword ptr [rsp + 0x28], 1
00798F15  mov      eax, r10d
00798F18  mov      dword ptr [rsp + 0x20], r10d
00798F1D  cdq      
00798F1E  sub      eax, edx
00798F20  sar      eax, 1
00798F22  sub      r8d, eax
00798F25  mov      eax, dword ptr [rip + 0x17a4af1]  ; -> 01F3DA1C [u32 0x00000780]
00798F2B  cdq      
00798F2C  sub      eax, edx
00798F2E  sar      eax, 1
00798F30  mov      ecx, eax
00798F32  mov      eax, r9d
00798F35  cdq      
00798F36  sub      eax, edx
00798F38  sar      eax, 1
00798F3A  sub      ecx, eax
00798F3C  mov      edx, ecx
00798F3E  mov      rcx, rbx
00798F41  call     qword ptr [rip + 0x1299d9]  ; -> 008C2920 [u64 0x0000000001CCC9BA]
00798F47  mov      rcx, qword ptr [rip + 0x270c30a]  ; -> 02EA5258
00798F4E  mov      r9, rsi
00798F51  mov      r8, rbx
00798F54  mov      edx, edi
00798F56  call     qword ptr [rip + 0x1298ec]  ; -> 008C2848 [u64 0x0000000001CCCB94]
00798F5C  mov      rcx, qword ptr [rsp + 0x40]
00798F61  xor      rcx, rsp
00798F64  call     0x808c40  ; -> 00808C40 fn
00798F69  add      rsp, 0x50
00798F6D  pop      rdi
00798F6E  pop      rsi
00798F6F  pop      rbx
00798F70  ret      
```

## 00799C90 (308 B, extent 00799C90-00799DC4)

Documented callee on this page: `0017D260`

```
00799C90  mov      qword ptr [rsp + 8], rbx
00799C95  mov      qword ptr [rsp + 0x10], rbp
00799C9A  mov      qword ptr [rsp + 0x18], rsi
00799C9F  mov      qword ptr [rsp + 0x20], rdi
00799CA4  push     r12
00799CA6  push     r14
00799CA8  push     r15
00799CAA  sub      rsp, 0x20
00799CAE  mov      edi, dword ptr [rcx]
00799CB0  mov      r12, rdx
00799CB3  btr      edi, 0x1f
00799CB7  mov      r14, rcx
00799CBA  lea      ebp, [rdi + 1]
00799CBD  cmp      edi, 1
00799CC0  jbe      0x799cc8  ; -> 00799CC8
00799CC2  mov      rbx, qword ptr [rcx + 8]
00799CC6  jmp      0x799cd4  ; -> 00799CD4
00799CC8  test     edi, edi
00799CCA  je       0x799cd2  ; -> 00799CD2
00799CCC  lea      rbx, [rcx + 8]
00799CD0  jmp      0x799cd4  ; -> 00799CD4
00799CD2  xor      ebx, ebx
00799CD4  lea      r15, [rcx + 8]
00799CD8  mov      rsi, r15
00799CDB  cmp      ebp, 1
00799CDE  jbe      0x799d00  ; -> 00799D00
00799CE0  mov      ecx, ebp
00799CE2  mov      edx, 4
00799CE7  shl      rcx, 6
00799CEB  call     0x17d260  ; -> 0017D260 fn
00799CF0  mov      rsi, rax
00799CF3  test     rax, rax
00799CF6  jne      0x799d00  ; -> 00799D00
00799CF8  lea      eax, [rsi + 0xd]
00799CFB  jmp      0x799da5  ; -> 00799DA5
00799D00  mov      rdx, rbx
00799D03  mov      rcx, rsi
00799D06  test     edi, edi
00799D08  je       0x799d44  ; -> 00799D44
00799D0A  mov      r8d, edi
00799D0D  nop      dword ptr [rax]
00799D10  mov      rax, rcx
00799D13  add      rcx, 0x40
00799D17  test     rax, rax
00799D1A  je       0x799d3e  ; -> 00799D3E
00799D1C  movups   xmm0, xmmword ptr [rdx]
00799D1F  movups   xmmword ptr [rax], xmm0
00799D22  movups   xmm1, xmmword ptr [rdx + 0x10]
00799D26  movups   xmmword ptr [rax + 0x10], xmm1
00799D2A  movups   xmm0, xmmword ptr [rdx + 0x20]
00799D2E  movups   xmmword ptr [rax + 0x20], xmm0
00799D32  movups   xmm1, xmmword ptr [rdx + 0x30]
00799D36  add      rdx, 0x40
00799D3A  movups   xmmword ptr [rax + 0x30], xmm1
00799D3E  sub      r8, 1
00799D42  jne      0x799d10  ; -> 00799D10
00799D44  mov      ecx, edi
00799D46  shl      rcx, 6
00799D4A  add      rcx, rsi
00799D4D  je       0x799d75  ; -> 00799D75
00799D4F  movups   xmm0, xmmword ptr [r12]
00799D54  movups   xmmword ptr [rcx], xmm0
00799D57  movups   xmm1, xmmword ptr [r12 + 0x10]
00799D5D  movups   xmmword ptr [rcx + 0x10], xmm1
00799D61  movups   xmm0, xmmword ptr [r12 + 0x20]
00799D67  movups   xmmword ptr [rcx + 0x20], xmm0
00799D6B  movups   xmm1, xmmword ptr [r12 + 0x30]
00799D71  movups   xmmword ptr [rcx + 0x30], xmm1
00799D75  cmp      rbx, rsi
00799D78  je       0x799d98  ; -> 00799D98
00799D7A  cmp      rbx, r15
00799D7D  je       0x799d98  ; -> 00799D98
00799D7F  mov      eax, dword ptr [r14]
00799D82  shr      eax, 0x1f
00799D85  not      al
00799D87  test     al, 1
00799D89  je       0x799d98  ; -> 00799D98
00799D8B  test     rbx, rbx
00799D8E  je       0x799d98  ; -> 00799D98
00799D90  mov      rcx, rbx
00799D93  call     0x584730  ; -> 00584730 fn
00799D98  cmp      rsi, r15
00799D9B  je       0x799da0  ; -> 00799DA0
00799D9D  mov      qword ptr [r15], rsi
00799DA0  mov      dword ptr [r14], ebp
00799DA3  xor      eax, eax
00799DA5  mov      rbx, qword ptr [rsp + 0x40]
00799DAA  mov      rbp, qword ptr [rsp + 0x48]
00799DAF  mov      rsi, qword ptr [rsp + 0x50]
00799DB4  mov      rdi, qword ptr [rsp + 0x58]
00799DB9  add      rsp, 0x20
00799DBD  pop      r15
00799DBF  pop      r14
00799DC1  pop      r12
00799DC3  ret      
```

## 0079A550 (154 B, extent 0079A550-0079A5EA)

Documented callee on this page: `00808C40`

```
0079A550  sub      rsp, 0x88
0079A557  mov      rax, qword ptr [rip + 0x17aa2d2]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0079A55E  xor      rax, rsp
0079A561  mov      qword ptr [rsp + 0x70], rax
0079A566  mov      rax, qword ptr [rsp + 0xb0]
0079A56E  add      rcx, 8
0079A572  mov      dword ptr [rdx + 0xc], 0x3f800000
0079A579  movss    xmm1, dword ptr [r8 + 4]
0079A57F  mov      dword ptr [r8 + 0xc], 0x3f800000
0079A587  movups   xmm0, xmmword ptr [rdx]
0079A58A  lea      rdx, [rsp + 0x20]
0079A58F  movss    dword ptr [rsp + 0x34], xmm1
0079A595  movss    xmm1, dword ptr [rip + 0x155160b]  ; -> 01CEBBA8 [f32 1]
0079A59D  movaps   xmmword ptr [rsp + 0x20], xmm0
0079A5A2  movss    xmm0, dword ptr [r8]
0079A5A7  movss    dword ptr [rsp + 0x30], xmm0
0079A5AD  movss    xmm0, dword ptr [r8 + 8]
0079A5B3  movss    dword ptr [rsp + 0x38], xmm0
0079A5B9  movups   xmm0, xmmword ptr [r9]
0079A5BD  movss    dword ptr [rsp + 0x3c], xmm1
0079A5C3  movaps   xmmword ptr [rsp + 0x40], xmm0
0079A5C8  movups   xmm0, xmmword ptr [rax]
0079A5CB  movaps   xmmword ptr [rsp + 0x50], xmm0
0079A5D0  call     0x799c90  ; -> 00799C90 fn
0079A5D5  mov      rcx, qword ptr [rsp + 0x70]
0079A5DA  xor      rcx, rsp
0079A5DD  call     0x808c40  ; -> 00808C40 fn
0079A5E2  add      rsp, 0x88
0079A5E9  ret      
```

## 007A08F0 (400 B, extent 007A08F0-007A0A80)

Documented callee on this page: `005CDAA0`

```
007A08F0  mov      qword ptr [rsp + 8], rbx
007A08F5  mov      qword ptr [rsp + 0x10], rsi
007A08FA  push     rdi
007A08FB  sub      rsp, 0x20
007A08FF  movzx    esi, r8b
007A0903  mov      rbx, rdx
007A0906  test     rcx, rcx
007A0909  je       0x7a0a45  ; -> 007A0A45
007A090F  mov      rax, qword ptr [rcx + 0xdf8]
007A0916  mov      rdi, qword ptr [rax + 0x88]
007A091D  test     rdi, rdi
007A0920  je       0x7a0a45  ; -> 007A0A45
007A0926  lea      rdx, [rip + 0x125133]  ; -> 008C5A60 [str "Circle"]
007A092D  mov      rcx, rbx
007A0930  call     qword ptr [rip + 0x1226ca]  ; -> 008C3000 [u64 0x0000000001CCEF78]
007A0936  test     eax, eax
007A0938  jne      0x7a0944  ; -> 007A0944
007A093A  mov      eax, 0x32
007A093F  jmp      0x7a0a41  ; -> 007A0A41
007A0944  lea      rdx, [rip + 0x12511d]  ; -> 008C5A68 [str "Cross"]
007A094B  mov      rcx, rbx
007A094E  call     qword ptr [rip + 0x1226ac]  ; -> 008C3000 [u64 0x0000000001CCEF78]
007A0954  test     eax, eax
007A0956  jne      0x7a0962  ; -> 007A0962
007A0958  mov      eax, 0x31
007A095D  jmp      0x7a0a41  ; -> 007A0A41
007A0962  lea      rdx, [rip + 0x1511edf]  ; -> 01CB2848 [str "Triangle"]
007A0969  mov      rcx, rbx
007A096C  call     qword ptr [rip + 0x12268e]  ; -> 008C3000 [u64 0x0000000001CCEF78]
007A0972  test     eax, eax
007A0974  jne      0x7a0980  ; -> 007A0980
007A0976  mov      eax, 0x33
007A097B  jmp      0x7a0a41  ; -> 007A0A41
007A0980  lea      rdx, [rip + 0x1511ecd]  ; -> 01CB2854 [str "Square"]
007A0987  mov      rcx, rbx
007A098A  call     qword ptr [rip + 0x122670]  ; -> 008C3000 [u64 0x0000000001CCEF78]
007A0990  test     eax, eax
007A0992  jne      0x7a099e  ; -> 007A099E
007A0994  mov      eax, 0x30
007A0999  jmp      0x7a0a41  ; -> 007A0A41
007A099E  lea      rdx, [rip + 0x1511eb7]  ; -> 01CB285C [str "Start"]
007A09A5  mov      rcx, rbx
007A09A8  call     qword ptr [rip + 0x122652]  ; -> 008C3000 [u64 0x0000000001CCEF78]
007A09AE  test     eax, eax
007A09B0  jne      0x7a09bc  ; -> 007A09BC
007A09B2  mov      eax, 0x39
007A09B7  jmp      0x7a0a41  ; -> 007A0A41
007A09BC  lea      rdx, [rip + 0x1511ea1]  ; -> 01CB2864 [str "Select"]
007A09C3  mov      rcx, rbx
007A09C6  call     qword ptr [rip + 0x122634]  ; -> 008C3000 [u64 0x0000000001CCEF78]
007A09CC  test     eax, eax
007A09CE  jne      0x7a09d7  ; -> 007A09D7
007A09D0  mov      eax, 0x38
007A09D5  jmp      0x7a0a41  ; -> 007A0A41
007A09D7  lea      rdx, [rip + 0x1511e8e]  ; -> 01CB286C
007A09DE  mov      rcx, rbx
007A09E1  call     qword ptr [rip + 0x122619]  ; -> 008C3000 [u64 0x0000000001CCEF78]
007A09E7  test     eax, eax
007A09E9  jne      0x7a09f2  ; -> 007A09F2
007A09EB  mov      eax, 0x3c
007A09F0  jmp      0x7a0a41  ; -> 007A0A41
007A09F2  lea      rdx, [rip + 0x1511e77]  ; -> 01CB2870 [str "Down"]
007A09F9  mov      rcx, rbx
007A09FC  call     qword ptr [rip + 0x1225fe]  ; -> 008C3000 [u64 0x0000000001CCEF78]
007A0A02  test     eax, eax
007A0A04  jne      0x7a0a0d  ; -> 007A0A0D
007A0A06  mov      eax, 0x3e
007A0A0B  jmp      0x7a0a41  ; -> 007A0A41
007A0A0D  lea      rdx, [rip + 0x1511e64]  ; -> 01CB2878 [str "Left"]
007A0A14  mov      rcx, rbx
007A0A17  call     qword ptr [rip + 0x1225e3]  ; -> 008C3000 [u64 0x0000000001CCEF78]
007A0A1D  test     eax, eax
007A0A1F  jne      0x7a0a28  ; -> 007A0A28
007A0A21  mov      eax, 0x3f
007A0A26  jmp      0x7a0a41  ; -> 007A0A41
007A0A28  lea      rdx, [rip + 0x1511e51]  ; -> 01CB2880 [str "Right"]
007A0A2F  mov      rcx, rbx
007A0A32  call     qword ptr [rip + 0x1225c8]  ; -> 008C3000 [u64 0x0000000001CCEF78]
007A0A38  test     eax, eax
007A0A3A  jne      0x7a0a57  ; -> 007A0A57
007A0A3C  mov      eax, 0x3d
007A0A41  mov      byte ptr [rax + rdi], sil
007A0A45  xor      eax, eax
007A0A47  mov      rbx, qword ptr [rsp + 0x30]
007A0A4C  mov      rsi, qword ptr [rsp + 0x38]
007A0A51  add      rsp, 0x20
007A0A55  pop      rdi
007A0A56  ret      
007A0A57  mov      r8, rbx
007A0A5A  lea      rdx, [rip + 0x1511e27]  ; -> 01CB2888
007A0A61  mov      ecx, 2
007A0A66  call     0x5cdaa0  ; -> 005CDAA0 fn
007A0A6B  mov      rbx, qword ptr [rsp + 0x30]
007A0A70  mov      eax, 5
007A0A75  mov      rsi, qword ptr [rsp + 0x38]
007A0A7A  add      rsp, 0x20
007A0A7E  pop      rdi
007A0A7F  ret      
```

## 008633B0 (94 B, extent 008633B0-0086340E)

Documented callee on this page: `00809950`

```
008633B0  mov      qword ptr [rsp + 8], rbx
008633B5  push     rdi
008633B6  sub      rsp, 0x20
008633BA  lea      rax, [rip + 0x146c6af]  ; -> 01CCFA70
008633C1  mov      rbx, rcx
008633C4  mov      qword ptr [rcx], rax
008633C7  mov      edi, edx
008633C9  mov      rcx, qword ptr [rcx + 8]
008633CD  test     rcx, rcx
008633D0  je       0x8633ed  ; -> 008633ED
008633D2  xor      edx, edx
008633D4  call     qword ptr [rip + 0x5f026]  ; -> 008C2400 [u64 0x0000000001CCF75E]
008633DA  mov      rcx, qword ptr [rbx + 8]
008633DE  call     qword ptr [rip + 0x5effc]  ; -> 008C23E0 [u64 0x0000000001CCC076]
008633E4  xor      eax, eax
008633E6  mov      qword ptr [rbx + 8], rax
008633EA  mov      dword ptr [rbx + 0x10], eax
008633ED  test     dil, 1
008633F1  je       0x863400  ; -> 00863400
008633F3  mov      edx, 0x28
008633F8  mov      rcx, rbx
008633FB  call     0x809950  ; -> 00809950 fn
00863400  mov      rax, rbx
00863403  mov      rbx, qword ptr [rsp + 0x30]
00863408  add      rsp, 0x20
0086340C  pop      rdi
0086340D  ret      
```

## 00874490 (84 B, extent 00874490-008744E4)

Documented callee on this page: `00625ED0`

```
00874490  push     rdi
00874492  sub      rsp, 0x30
00874496  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0087449F  mov      qword ptr [rsp + 0x40], rbx
008744A4  mov      rdi, rcx
008744A7  add      rcx, 0x188
008744AE  call     0x625ed0  ; -> 00625ED0 fn
008744B3  nop      
008744B4  test     al, al
008744B6  je       0x8744c5  ; -> 008744C5
008744B8  lea      rcx, [rdi + 0x188]
008744BF  call     0x62b890  ; -> 0062B890 fn
008744C4  nop      
008744C5  lea      rcx, [rdi + 0x188]
008744CC  call     0x5ddb00  ; -> 005DDB00 fn
008744D1  nop      
008744D2  mov      rcx, rdi
008744D5  mov      rbx, qword ptr [rsp + 0x40]
008744DA  add      rsp, 0x30
008744DE  pop      rdi
008744DF  jmp      0x5de250  ; -> 005DE250 fn
```

## 00879B00 (115 B, extent 00879B00-00879B73)

Documented callee on this page: `00584730`

```
00879B00  mov      qword ptr [rsp + 8], rbx
00879B05  mov      qword ptr [rsp + 0x10], rbp
00879B0A  mov      qword ptr [rsp + 0x18], rsi
00879B0F  push     rdi
00879B10  sub      rsp, 0x20
00879B14  mov      edi, dword ptr [rdx]
00879B16  mov      rsi, rdx
00879B19  mov      rdx, qword ptr [rdx + 8]
00879B1D  mov      rbx, rcx
00879B20  btr      edi, 0x1f
00879B24  mov      ecx, edi
00879B26  call     0x6bc4c0  ; -> 006BC4C0 fn
00879B2B  mov      rcx, qword ptr [rbx + 8]
00879B2F  mov      rbp, rax
00879B32  cmp      rcx, rax
00879B35  je       0x879b4d  ; -> 00879B4D
00879B37  mov      edx, dword ptr [rbx]
00879B39  shr      edx, 0x1f
00879B3C  not      dl
00879B3E  test     dl, 1
00879B41  je       0x879b4d  ; -> 00879B4D
00879B43  test     rcx, rcx
00879B46  je       0x879b4d  ; -> 00879B4D
00879B48  call     0x584730  ; -> 00584730 fn
00879B4D  mov      qword ptr [rbx + 8], rbp
00879B51  mov      rbp, qword ptr [rsp + 0x38]
00879B56  mov      dword ptr [rbx], edi
00879B58  mov      rax, qword ptr [rsi + 0x10]
00879B5C  mov      rsi, qword ptr [rsp + 0x40]
00879B61  mov      qword ptr [rbx + 0x10], rax
00879B65  mov      rax, rbx
00879B68  mov      rbx, qword ptr [rsp + 0x30]
00879B6D  add      rsp, 0x20
00879B71  pop      rdi
00879B72  ret      
```

## 0087A830 (136 B, extent 0087A830-0087A8B8)

Documented callee on this page: `00584730`

```
0087A830  push     rdi
0087A832  sub      rsp, 0x30
0087A836  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0087A83F  mov      qword ptr [rsp + 0x40], rbx
0087A844  mov      rbx, rcx
0087A847  mov      eax, dword ptr [rcx + 0x20]
0087A84A  shr      eax, 0x1f
0087A84D  not      al
0087A84F  test     al, 1
0087A851  je       0x87a862  ; -> 0087A862
0087A853  mov      rcx, qword ptr [rcx + 0x28]
0087A857  test     rcx, rcx
0087A85A  je       0x87a862  ; -> 0087A862
0087A85C  call     0x584730  ; -> 00584730 fn
0087A861  nop      
0087A862  xor      edi, edi
0087A864  mov      qword ptr [rbx + 0x28], rdi
0087A868  mov      dword ptr [rbx + 0x20], edi
0087A86B  mov      eax, dword ptr [rbx + 0x10]
0087A86E  shr      eax, 0x1f
0087A871  not      al
0087A873  test     al, 1
0087A875  je       0x87a886  ; -> 0087A886
0087A877  mov      rcx, qword ptr [rbx + 0x18]
0087A87B  test     rcx, rcx
0087A87E  je       0x87a886  ; -> 0087A886
0087A880  call     0x584730  ; -> 00584730 fn
0087A885  nop      
0087A886  mov      qword ptr [rbx + 0x18], rdi
0087A88A  mov      dword ptr [rbx + 0x10], edi
0087A88D  mov      eax, dword ptr [rbx]
0087A88F  shr      eax, 0x1f
0087A892  not      al
0087A894  test     al, 1
0087A896  je       0x87a8a7  ; -> 0087A8A7
0087A898  mov      rcx, qword ptr [rbx + 8]
0087A89C  test     rcx, rcx
0087A89F  je       0x87a8a7  ; -> 0087A8A7
0087A8A1  call     0x584730  ; -> 00584730 fn
0087A8A6  nop      
0087A8A7  mov      qword ptr [rbx + 8], rdi
0087A8AB  mov      dword ptr [rbx], edi
0087A8AD  mov      rbx, qword ptr [rsp + 0x40]
0087A8B2  add      rsp, 0x30
0087A8B6  pop      rdi
0087A8B7  ret      
```
