# F homing pack (FABLE): `03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 31. No bearing page cites them and no documented function calls them directly.

## 0026FEC0 (140 B, extent 0026FEC0-0026FF4C)

Documented callee on this page: `0024F680`

```
0026FEC0  push     rdi
0026FEC2  sub      rsp, 0x3e0
0026FEC9  mov      rax, qword ptr [rip + 0x1cd4960]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0026FED0  xor      rax, rsp
0026FED3  mov      qword ptr [rsp + 0x3d0], rax
0026FEDB  mov      edi, edx
0026FEDD  cmp      ecx, 0x40
0026FEE0  jl       0x26fee6  ; -> 0026FEE6
0026FEE2  xor      eax, eax
0026FEE4  jmp      0x26ff33  ; -> 0026FF33
0026FEE6  mov      word ptr [rsp + 0x24], cx
0026FEEB  lea      rcx, [rsp + 0x20]
0026FEF0  mov      byte ptr [rsp + 0x20], 2
0026FEF5  call     0x24f680  ; -> 0024F680 fn
0026FEFA  test     rax, rax
0026FEFD  je       0x26fee2  ; -> 0026FEE2
0026FEFF  mov      qword ptr [rsp + 0x400], rbx
0026FF07  mov      rbx, qword ptr [rax + 0x130]
0026FF0E  test     rbx, rbx
0026FF11  jne      0x26ff17  ; -> 0026FF17
0026FF13  xor      eax, eax
0026FF15  jmp      0x26ff2b  ; -> 0026FF2B
0026FF17  mov      rcx, rax
0026FF1A  call     0x24ed80  ; -> 0024ED80 fn
0026FF1F  movzx    edx, dil
0026FF23  mov      rcx, rbx
0026FF26  call     0x3333f0  ; -> 003333F0 fn
0026FF2B  mov      rbx, qword ptr [rsp + 0x400]
0026FF33  mov      rcx, qword ptr [rsp + 0x3d0]
0026FF3B  xor      rcx, rsp
0026FF3E  call     0x808c40  ; -> 00808C40 fn
0026FF43  add      rsp, 0x3e0
0026FF4A  pop      rdi
0026FF4B  ret      
```

## 002899A0 (107 B, extent 002899A0-00289A0B)

Documented callee on this page: `00244F50`

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

## 002A1D40 (114 B, extent 002A1D40-002A1DB2)

Documented callee on this page: `00244F50`

```
002A1D40  sub      rsp, 0x68
002A1D44  mov      rax, qword ptr [rip + 0x1ca2ae5]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002A1D4B  xor      rax, rsp
002A1D4E  mov      qword ptr [rsp + 0x50], rax
002A1D53  cmp      qword ptr [rip + 0x1dfa76d], 0  ; -> 0209C4C8
002A1D5B  jne      0x2a1da0  ; -> 002A1DA0
002A1D5D  xor      edx, edx
002A1D5F  mov      dword ptr [rsp + 0x2c], ecx
002A1D63  mov      qword ptr [rsp + 0x20], rdx
002A1D68  lea      rax, [rsp + 0x20]
002A1D6D  mov      dword ptr [rsp + 0x38], edx
002A1D71  lea      r8, [rsp + 0x38]
002A1D76  mov      qword ptr [rsp + 0x48], rdx
002A1D7B  mov      ecx, 0xf8
002A1D80  lea      rdx, [rip + 0x229]  ; -> 002A1FB0
002A1D87  mov      dword ptr [rsp + 0x28], 0x30000
002A1D8F  mov      word ptr [rsp + 0x30], 2
002A1D96  mov      qword ptr [rsp + 0x40], rax
002A1D9B  call     0x244f50  ; -> 00244F50 fn
002A1DA0  mov      rcx, qword ptr [rsp + 0x50]
002A1DA5  xor      rcx, rsp
002A1DA8  call     0x808c40  ; -> 00808C40 fn
002A1DAD  add      rsp, 0x68
002A1DB1  ret      
```

## 002A1EB0 (112 B, extent 002A1EB0-002A1F20)

Documented callee on this page: `00244F50`

```
002A1EB0  sub      rsp, 0x68
002A1EB4  mov      rax, qword ptr [rip + 0x1ca2975]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002A1EBB  xor      rax, rsp
002A1EBE  mov      qword ptr [rsp + 0x50], rax
002A1EC3  cmp      qword ptr [rip + 0x1dfa5fd], 0  ; -> 0209C4C8
002A1ECB  jne      0x2a1f0e  ; -> 002A1F0E
002A1ECD  xor      edx, edx
002A1ECF  mov      dword ptr [rsp + 0x2c], ecx
002A1ED3  mov      qword ptr [rsp + 0x20], rdx
002A1ED8  lea      rax, [rsp + 0x20]
002A1EDD  mov      word ptr [rsp + 0x30], dx
002A1EE2  lea      r8, [rsp + 0x38]
002A1EE7  mov      dword ptr [rsp + 0x38], edx
002A1EEB  mov      ecx, 0xf8
002A1EF0  mov      qword ptr [rsp + 0x48], rdx
002A1EF5  lea      rdx, [rip + 0xb4]  ; -> 002A1FB0
002A1EFC  mov      dword ptr [rsp + 0x28], 0x30000
002A1F04  mov      qword ptr [rsp + 0x40], rax
002A1F09  call     0x244f50  ; -> 00244F50 fn
002A1F0E  mov      rcx, qword ptr [rsp + 0x50]
002A1F13  xor      rcx, rsp
002A1F16  call     0x808c40  ; -> 00808C40 fn
002A1F1B  add      rsp, 0x68
002A1F1F  ret      
```

## 002A7E20 (114 B, extent 002A7E20-002A7E92)

Documented callee on this page: `00244F50`

```
002A7E20  sub      rsp, 0x68
002A7E24  mov      rax, qword ptr [rip + 0x1c9ca05]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002A7E2B  xor      rax, rsp
002A7E2E  mov      qword ptr [rsp + 0x50], rax
002A7E33  cmp      qword ptr [rip + 0x1df468d], 0  ; -> 0209C4C8
002A7E3B  jne      0x2a7e80  ; -> 002A7E80
002A7E3D  xor      edx, edx
002A7E3F  mov      dword ptr [rsp + 0x2c], ecx
002A7E43  mov      qword ptr [rsp + 0x20], rdx
002A7E48  lea      rax, [rsp + 0x20]
002A7E4D  mov      dword ptr [rsp + 0x38], edx
002A7E51  lea      r8, [rsp + 0x38]
002A7E56  mov      qword ptr [rsp + 0x48], rdx
002A7E5B  mov      ecx, 0xf8
002A7E60  lea      rdx, [rip - 0x5eb7]  ; -> 002A1FB0
002A7E67  mov      dword ptr [rsp + 0x28], 0x30000
002A7E6F  mov      word ptr [rsp + 0x30], 1
002A7E76  mov      qword ptr [rsp + 0x40], rax
002A7E7B  call     0x244f50  ; -> 00244F50 fn
002A7E80  mov      rcx, qword ptr [rsp + 0x50]
002A7E85  xor      rcx, rsp
002A7E88  call     0x808c40  ; -> 00808C40 fn
002A7E8D  add      rsp, 0x68
002A7E91  ret      
```

## 002D7840 (97 B, extent 002D7840-002D78A1)

Documented callee on this page: `00244F50`

```
002D7840  sub      rsp, 0x28
002D7844  mov      rax, qword ptr [rip + 0x1dc33e5]  ; -> 0209AC30
002D784B  cmp      qword ptr [rax + 0x3b8], 0
002D7853  jne      0x2d787a  ; -> 002D787A
002D7855  cmp      qword ptr [rax + 0xe0], 0
002D785D  jne      0x2d787a  ; -> 002D787A
002D785F  xor      r8d, r8d
002D7862  lea      rdx, [rip - 0x989]  ; -> 002D6EE0
002D7869  mov      ecx, 0xc0
002D786E  call     0x244f50  ; -> 00244F50 fn
002D7873  mov      rax, qword ptr [rip + 0x1dc33b6]  ; -> 0209AC30
002D787A  cmp      qword ptr [rax + 0xf0], 0
002D7882  jne      0x2d789c  ; -> 002D789C
002D7884  xor      r8d, r8d
002D7887  lea      rdx, [rip - 0xbee]  ; -> 002D6CA0
002D788E  mov      ecx, 0x188
002D7893  add      rsp, 0x28
002D7897  jmp      0x244f50  ; -> 00244F50 fn
002D789C  add      rsp, 0x28
002D78A0  ret      
```

## 00341F50 (55 B, extent 00341F50-00341F87)

Documented callee on this page: `00267310`

```
00341F50  push     rbx
00341F52  sub      rsp, 0x20
00341F56  movzx    ecx, byte ptr [rdx + 0x15]
00341F5A  mov      rbx, r8
00341F5D  call     0x267310  ; -> 00267310 fn
00341F62  test     eax, eax
00341F64  jne      0x341f7f  ; -> 00341F7F
00341F66  mov      edx, dword ptr [rbx + 4]
00341F69  mov      ecx, dword ptr [rbx]
00341F6B  call     0x3e92a0  ; -> 003E92A0 fn
00341F70  xor      ecx, ecx
00341F72  test     eax, eax
00341F74  setne    cl
00341F77  mov      eax, ecx
00341F79  add      rsp, 0x20
00341F7D  pop      rbx
00341F7E  ret      
00341F7F  xor      eax, eax
00341F81  add      rsp, 0x20
00341F85  pop      rbx
00341F86  ret      
```

## 003428C0 (55 B, extent 003428C0-003428F7)

Documented callee on this page: `00267310`

```
003428C0  push     rbx
003428C2  sub      rsp, 0x20
003428C6  movzx    ecx, byte ptr [rdx + 0x15]
003428CA  mov      rbx, r8
003428CD  call     0x267310  ; -> 00267310 fn
003428D2  test     eax, eax
003428D4  jne      0x3428ef  ; -> 003428EF
003428D6  mov      edx, dword ptr [rbx + 4]
003428D9  mov      ecx, dword ptr [rbx]
003428DB  call     0x3e9250  ; -> 003E9250 fn
003428E0  xor      ecx, ecx
003428E2  test     eax, eax
003428E4  setne    cl
003428E7  mov      eax, ecx
003428E9  add      rsp, 0x20
003428ED  pop      rbx
003428EE  ret      
003428EF  xor      eax, eax
003428F1  add      rsp, 0x20
003428F5  pop      rbx
003428F6  ret      
```

## 003435C0 (67 B, extent 003435C0-00343603)

Documented callee on this page: `00267310`

```
003435C0  push     rbx
003435C2  sub      rsp, 0x20
003435C6  mov      rcx, rdx
003435C9  mov      rbx, rdx
003435CC  call     0x265290  ; -> 00265290 fn
003435D1  test     eax, eax
003435D3  je       0x3435f9  ; -> 003435F9
003435D5  mov      rcx, rbx
003435D8  call     0x2ea780  ; -> 002EA780 fn
003435DD  test     eax, eax
003435DF  je       0x3435f9  ; -> 003435F9
003435E1  movzx    ecx, byte ptr [rbx + 0x15]
003435E5  call     0x267310  ; -> 00267310 fn
003435EA  xor      ecx, ecx
003435EC  test     eax, eax
003435EE  sete     cl
003435F1  mov      eax, ecx
003435F3  add      rsp, 0x20
003435F7  pop      rbx
003435F8  ret      
003435F9  xor      ecx, ecx
003435FB  mov      eax, ecx
003435FD  add      rsp, 0x20
00343601  pop      rbx
00343602  ret      
```

## 003436B0 (87 B, extent 003436B0-00343707)

Documented callee on this page: `00473680`

```
003436B0  mov      qword ptr [rsp + 8], rbx
003436B5  push     rdi
003436B6  sub      rsp, 0x20
003436BA  mov      ecx, dword ptr [r8]
003436BD  mov      rbx, rdx
003436C0  call     0x473620  ; -> 00473620 fn
003436C5  movzx    ecx, byte ptr [rbx + 0x15]
003436C9  mov      edi, eax
003436CB  call     0x267310  ; -> 00267310 fn
003436D0  test     eax, eax
003436D2  je       0x3436dd  ; -> 003436DD
003436D4  movzx    ecx, byte ptr [rbx + 0x15]
003436D8  call     0x473680  ; -> 00473680 fn
003436DD  movzx    ecx, byte ptr [rbx + 0x15]
003436E1  call     0x267310  ; -> 00267310 fn
003436E6  test     eax, eax
003436E8  jne      0x3436fa  ; -> 003436FA
003436EA  test     edi, edi
003436EC  setne    al
003436EF  mov      rbx, qword ptr [rsp + 0x30]
003436F4  add      rsp, 0x20
003436F8  pop      rdi
003436F9  ret      
003436FA  xor      eax, eax
003436FC  mov      rbx, qword ptr [rsp + 0x30]
00343701  add      rsp, 0x20
00343705  pop      rdi
00343706  ret      
```

## 00343F10 (37 B, extent 00343F10-00343F35)

Documented callee on this page: `00267310`

```
00343F10  sub      rsp, 0x28
00343F14  movzx    ecx, byte ptr [rdx + 0x15]
00343F18  call     0x267310  ; -> 00267310 fn
00343F1D  xor      ecx, ecx
00343F1F  test     eax, eax
00343F21  jne      0x343f2c  ; -> 00343F2C
00343F23  add      rsp, 0x28
00343F27  jmp      0x3ddf90  ; -> 003DDF90 fn
00343F2C  add      rsp, 0x28
00343F30  jmp      0x3ddc50  ; -> 003DDC50 fn
```

## 00344340 (68 B, extent 00344340-00344384)

Documented callee on this page: `00267310`

```
00344340  mov      qword ptr [rsp + 8], rbx
00344345  push     rdi
00344346  sub      rsp, 0x20
0034434A  mov      rcx, r9
0034434D  mov      rbx, rdx
00344350  call     0x267e10  ; -> 00267E10 fn
00344355  movzx    ecx, byte ptr [rbx + 0x15]
00344359  mov      edi, eax
0034435B  call     0x267310  ; -> 00267310 fn
00344360  mov      ecx, edi
00344362  test     eax, eax
00344364  jne      0x344375  ; -> 00344375
00344366  mov      rbx, qword ptr [rsp + 0x30]
0034436B  add      rsp, 0x20
0034436F  pop      rdi
00344370  jmp      0x3ddf90  ; -> 003DDF90 fn
00344375  mov      rbx, qword ptr [rsp + 0x30]
0034437A  add      rsp, 0x20
0034437E  pop      rdi
0034437F  jmp      0x3ddc50  ; -> 003DDC50 fn
```

## 00345930 (135 B, extent 00345930-003459B7)

Documented callee on this page: `00267310`

```
00345930  mov      qword ptr [rsp + 8], rbx
00345935  mov      qword ptr [rsp + 0x10], rbp
0034593A  mov      qword ptr [rsp + 0x18], rsi
0034593F  push     rdi
00345940  push     r14
00345942  push     r15
00345944  sub      rsp, 0x20
00345948  mov      r14, rcx
0034594B  mov      rdi, rdx
0034594E  mov      rcx, r9
00345951  call     0x267e10  ; -> 00267E10 fn
00345956  mov      ebx, eax
00345958  call     0x2640c0  ; -> 002640C0 fn
0034595D  movzx    ecx, byte ptr [rdi + 0x15]
00345961  mov      ebp, ebx
00345963  sar      ebx, 0x18
00345966  mov      r15, rax
00345969  movzx    ebx, bl
0034596C  and      ebp, 0xffffff
00345972  sub      ebx, 4
00345975  xor      esi, esi
00345977  call     0x267310  ; -> 00267310 fn
0034597C  test     eax, eax
0034597E  jne      0x345995  ; -> 00345995
00345980  cmp      ebx, 7
00345983  ja       0x345995  ; -> 00345995
00345985  mov      ecx, dword ptr [r15 + 0x28]
00345989  mov      r8d, ebp
0034598C  mov      edx, ebx
0034598E  call     0x3df200  ; -> 003DF200 fn
00345993  mov      esi, eax
00345995  mov      edx, esi
00345997  mov      rcx, r14
0034599A  mov      rbx, qword ptr [rsp + 0x40]
0034599F  mov      rbp, qword ptr [rsp + 0x48]
003459A4  mov      rsi, qword ptr [rsp + 0x50]
003459A9  add      rsp, 0x20
003459AD  pop      r15
003459AF  pop      r14
003459B1  pop      rdi
003459B2  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 003486A0 (89 B, extent 003486A0-003486F9)

Documented callee on this page: `00466DD0`

```
003486A0  mov      qword ptr [rsp + 8], rbx
003486A5  push     rdi
003486A6  sub      rsp, 0x20
003486AA  movzx    ecx, byte ptr [rdx + 0x15]
003486AE  mov      rbx, rdx
003486B1  mov      edi, dword ptr [r8]
003486B4  call     0x267310  ; -> 00267310 fn
003486B9  test     eax, eax
003486BB  je       0x3486c2  ; -> 003486C2
003486BD  call     0x466dd0  ; -> 00466DD0 fn
003486C2  mov      ecx, edi
003486C4  call     0x4735e0  ; -> 004735E0 fn
003486C9  test     eax, eax
003486CB  jne      0x3486dc  ; -> 003486DC
003486CD  xor      ecx, ecx
003486CF  mov      eax, ecx
003486D1  mov      rbx, qword ptr [rsp + 0x30]
003486D6  add      rsp, 0x20
003486DA  pop      rdi
003486DB  ret      
003486DC  movzx    ecx, byte ptr [rbx + 0x15]
003486E0  call     0x267310  ; -> 00267310 fn
003486E5  mov      rbx, qword ptr [rsp + 0x30]
003486EA  xor      ecx, ecx
003486EC  test     eax, eax
003486EE  sete     cl
003486F1  mov      eax, ecx
003486F3  add      rsp, 0x20
003486F7  pop      rdi
003486F8  ret      
```

## 0034A600 (50 B, extent 0034A600-0034A632)

Documented callee on this page: `00267310`

```
0034A600  sub      rsp, 0x28
0034A604  movzx    ecx, byte ptr [rdx + 0x15]
0034A608  call     0x267310  ; -> 00267310 fn
0034A60D  test     eax, eax
0034A60F  je       0x34a61f  ; -> 0034A61F
0034A611  call     0x256500  ; -> 00256500 fn
0034A616  xor      ecx, ecx
0034A618  mov      eax, ecx
0034A61A  add      rsp, 0x28
0034A61E  ret      
0034A61F  call     0x2564b0  ; -> 002564B0 fn
0034A624  xor      ecx, ecx
0034A626  test     eax, eax
0034A628  sete     cl
0034A62B  mov      eax, ecx
0034A62D  add      rsp, 0x28
0034A631  ret      
```

## 0034AB50 (145 B, extent 0034AB50-0034ABE1)

Documented callee on this page: `00267310`

```
0034AB50  mov      qword ptr [rsp + 8], rbx
0034AB55  mov      qword ptr [rsp + 0x10], rbp
0034AB5A  mov      qword ptr [rsp + 0x18], rsi
0034AB5F  push     rdi
0034AB60  sub      rsp, 0x40
0034AB64  mov      rcx, r9
0034AB67  movaps   xmmword ptr [rsp + 0x30], xmm6
0034AB6C  mov      rbx, r9
0034AB6F  mov      rsi, rdx
0034AB72  call     0x267e10  ; -> 00267E10 fn
0034AB77  movd     xmm6, eax
0034AB7B  cvtdq2ps xmm6, xmm6
0034AB7E  call     0x2640c0  ; -> 002640C0 fn
0034AB83  mov      rcx, rbx
0034AB86  mov      rbp, rax
0034AB89  call     0x267e10  ; -> 00267E10 fn
0034AB8E  movzx    ecx, byte ptr [rsi + 0x15]
0034AB92  mov      ebx, eax
0034AB94  mov      edi, eax
0034AB96  shr      ebx, 0x18
0034AB99  sub      ebx, 0x10
0034AB9C  and      edi, 0xffffff
0034ABA2  call     0x267310  ; -> 00267310 fn
0034ABA7  test     eax, eax
0034ABA9  jne      0x34abc7  ; -> 0034ABC7
0034ABAB  cmp      ebx, 0xf
0034ABAE  ja       0x34abc7  ; -> 0034ABC7
0034ABB0  mov      edx, dword ptr [rbp + 0x28]
0034ABB3  mov      r9d, edi
0034ABB6  mov      r8d, ebx
0034ABB9  movss    dword ptr [rsp + 0x20], xmm6
0034ABBF  mov      rcx, rsi
0034ABC2  call     0x3dd8d0  ; -> 003DD8D0 fn
0034ABC7  mov      rbx, qword ptr [rsp + 0x50]
0034ABCC  mov      rbp, qword ptr [rsp + 0x58]
0034ABD1  mov      rsi, qword ptr [rsp + 0x60]
0034ABD6  movaps   xmm6, xmmword ptr [rsp + 0x30]
0034ABDB  add      rsp, 0x40
0034ABDF  pop      rdi
0034ABE0  ret      
```

## 0034B3C0 (50 B, extent 0034B3C0-0034B3F2)

Documented callee on this page: `00267310`

```
0034B3C0  sub      rsp, 0x28
0034B3C4  movzx    ecx, byte ptr [rdx + 0x15]
0034B3C8  call     0x267310  ; -> 00267310 fn
0034B3CD  test     eax, eax
0034B3CF  jne      0x34b3e4  ; -> 0034B3E4
0034B3D1  call     0x379f10  ; -> 00379F10 fn
0034B3D6  xor      ecx, ecx
0034B3D8  test     eax, eax
0034B3DA  setne    cl
0034B3DD  mov      eax, ecx
0034B3DF  add      rsp, 0x28
0034B3E3  ret      
0034B3E4  call     0x379f40  ; -> 00379F40 fn
0034B3E9  xor      ecx, ecx
0034B3EB  mov      eax, ecx
0034B3ED  add      rsp, 0x28
0034B3F1  ret      
```

## 00350700 (176 B, extent 00350700-003507B0)

Documented callee on this page: `00267310`

```
00350700  mov      qword ptr [rsp + 8], rbx
00350705  mov      qword ptr [rsp + 0x10], rbp
0035070A  mov      qword ptr [rsp + 0x18], rsi
0035070F  push     rdi
00350710  push     r12
00350712  push     r13
00350714  push     r14
00350716  push     r15
00350718  sub      rsp, 0x30
0035071C  mov      r14, rcx
0035071F  mov      rbx, r9
00350722  mov      rcx, r9
00350725  mov      rdi, rdx
00350728  call     0x267e10  ; -> 00267E10 fn
0035072D  mov      rcx, rbx
00350730  mov      r15d, eax
00350733  call     0x267e10  ; -> 00267E10 fn
00350738  mov      rcx, rbx
0035073B  mov      r12d, eax
0035073E  call     0x267e10  ; -> 00267E10 fn
00350743  mov      ebx, eax
00350745  call     0x2640c0  ; -> 002640C0 fn
0035074A  movzx    ecx, byte ptr [rdi + 0x15]
0035074E  mov      ebp, ebx
00350750  sar      ebx, 0x18
00350753  mov      r13, rax
00350756  movzx    ebx, bl
00350759  and      ebp, 0xffffff
0035075F  sub      ebx, 4
00350762  xor      esi, esi
00350764  call     0x267310  ; -> 00267310 fn
00350769  test     eax, eax
0035076B  jne      0x35078a  ; -> 0035078A
0035076D  cmp      ebx, 7
00350770  ja       0x35078a  ; -> 0035078A
00350772  mov      ecx, dword ptr [r13 + 0x28]
00350776  mov      r9d, r12d
00350779  mov      r8d, ebp
0035077C  mov      dword ptr [rsp + 0x20], r15d
00350781  mov      edx, ebx
00350783  call     0x3df130  ; -> 003DF130 fn
00350788  mov      esi, eax
0035078A  mov      edx, esi
0035078C  mov      rcx, r14
0035078F  mov      rbx, qword ptr [rsp + 0x60]
00350794  mov      rbp, qword ptr [rsp + 0x68]
00350799  mov      rsi, qword ptr [rsp + 0x70]
0035079E  add      rsp, 0x30
003507A2  pop      r15
003507A4  pop      r14
003507A6  pop      r13
003507A8  pop      r12
003507AA  pop      rdi
003507AB  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 003549D0 (65 B, extent 003549D0-00354A11)

Documented callee on this page: `00267310`

```
003549D0  push     rbx
003549D2  sub      rsp, 0x20
003549D6  mov      rbx, rcx
003549D9  movzx    ecx, byte ptr [rdx + 0x15]
003549DD  call     0x267310  ; -> 00267310 fn
003549E2  test     eax, eax
003549E4  je       0x3549fa  ; -> 003549FA
003549E6  call     0x3604c0  ; -> 003604C0 fn
003549EB  mov      edx, eax
003549ED  mov      rcx, rbx
003549F0  add      rsp, 0x20
003549F4  pop      rbx
003549F5  jmp      0x26b4e0  ; -> 0026B4E0 fn
003549FA  or       ecx, 0xffffffff
003549FD  call     0x2debe0  ; -> 002DEBE0 fn
00354A02  mov      edx, eax
00354A04  mov      rcx, rbx
00354A07  add      rsp, 0x20
00354A0B  pop      rbx
00354A0C  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00355160 (61 B, extent 00355160-0035519D)

Documented callee on this page: `00267310`

```
00355160  push     rbx
00355162  sub      rsp, 0x20
00355166  mov      ecx, dword ptr [r8]
00355169  mov      rbx, rdx
0035516C  test     ecx, ecx
0035516E  jne      0x355178  ; -> 00355178
00355170  xor      eax, eax
00355172  add      rsp, 0x20
00355176  pop      rbx
00355177  ret      
00355178  mov      edx, dword ptr [r8 + 4]
0035517C  call     0x36dfc0  ; -> 0036DFC0 fn
00355181  test     eax, eax
00355183  jne      0x355170  ; -> 00355170
00355185  movzx    ecx, byte ptr [rbx + 0x15]
00355189  call     0x267310  ; -> 00267310 fn
0035518E  xor      ecx, ecx
00355190  test     eax, eax
00355192  sete     cl
00355195  mov      eax, ecx
00355197  add      rsp, 0x20
0035519B  pop      rbx
0035519C  ret      
```

## 0035C0D0 (46 B, extent 0035C0D0-0035C0FE)

Documented callee on this page: `00244F50`

```
0035C0D0  sub      rsp, 0x28
0035C0D4  cmp      qword ptr [rip + 0x1f6c304], 0  ; -> 022C83E0
0035C0DC  jne      0x35c0f9  ; -> 0035C0F9
0035C0DE  xor      r8d, r8d
0035C0E1  lea      rdx, [rip + 0x78]  ; -> 0035C160
0035C0E8  mov      ecx, 0xf8
0035C0ED  call     0x244f50  ; -> 00244F50 fn
0035C0F2  mov      qword ptr [rip + 0x1f6c2e7], rax  ; -> 022C83E0
0035C0F9  add      rsp, 0x28
0035C0FD  ret      
```

## 0035DAF0 (357 B, extent 0035DAF0-0035DC55)

Documented callee on this page: `00247950`

```
0035DAF0  mov      qword ptr [rsp + 0x10], rbx
0035DAF5  mov      qword ptr [rsp + 0x18], rsi
0035DAFA  push     rdi
0035DAFB  sub      rsp, 0x20
0035DAFF  mov      rbx, rcx
0035DB02  mov      ecx, dword ptr [rdx]
0035DB04  sub      ecx, 1
0035DB07  je       0x35dc05  ; -> 0035DC05
0035DB0D  sub      ecx, 1
0035DB10  je       0x35db49  ; -> 0035DB49
0035DB12  cmp      ecx, 0x10
0035DB15  je       0x35db2e  ; -> 0035DB2E
0035DB17  mov      rcx, rbx
0035DB1A  mov      rbx, qword ptr [rsp + 0x38]
0035DB1F  mov      rsi, qword ptr [rsp + 0x40]
0035DB24  add      rsp, 0x20
0035DB28  pop      rdi
0035DB29  jmp      0x5c5230  ; -> 005C5230 fn
0035DB2E  xor      edi, edi
0035DB30  mov      qword ptr [rip + 0x1f6a871], rdi  ; -> 022C83A8
0035DB37  xor      eax, eax
0035DB39  mov      rbx, qword ptr [rsp + 0x38]
0035DB3E  mov      rsi, qword ptr [rsp + 0x40]
0035DB43  add      rsp, 0x20
0035DB47  pop      rdi
0035DB48  ret      
0035DB49  mov      rax, qword ptr [rip + 0x1f6a528]  ; -> 022C8078
0035DB50  test     rax, rax
0035DB53  je       0x35dc43  ; -> 0035DC43
0035DB59  mov      esi, dword ptr [rip + 0x1f6a50d]  ; -> 022C806C
0035DB5F  mov      ecx, dword ptr [rbx + 0xc4]
0035DB65  mov      edi, dword ptr [rax + 8]
0035DB68  cmp      esi, ecx
0035DB6A  je       0x35db9f  ; -> 0035DB9F
0035DB6C  test     ecx, ecx
0035DB6E  je       0x35db75  ; -> 0035DB75
0035DB70  call     0x290940  ; -> 00290940 fn
0035DB75  mov      dword ptr [rbx + 0xc4], esi
0035DB7B  mov      dword ptr [rbx + 0xc8], edi
0035DB81  test     esi, esi
0035DB83  je       0x35dc43  ; -> 0035DC43
0035DB89  test     edi, edi
0035DB8B  jne      0x35dbb9  ; -> 0035DBB9
0035DB8D  xor      eax, eax
0035DB8F  mov      rbx, qword ptr [rsp + 0x38]
0035DB94  mov      rsi, qword ptr [rsp + 0x40]
0035DB99  add      rsp, 0x20
0035DB9D  pop      rdi
0035DB9E  ret      
0035DB9F  cmp      edi, dword ptr [rbx + 0xc8]
0035DBA5  je       0x35dc43  ; -> 0035DC43
0035DBAB  mov      dword ptr [rbx + 0xc8], edi
0035DBB1  test     edi, edi
0035DBB3  je       0x35dbec  ; -> 0035DBEC
0035DBB5  cmp      esi, edi
0035DBB7  je       0x35dbec  ; -> 0035DBEC
0035DBB9  lea      rdx, [rsp + 0x30]
0035DBBE  mov      ecx, edi
0035DBC0  call     0x320ca0  ; -> 00320CA0 fn
0035DBC5  cmp      eax, 1
0035DBC8  jne      0x35dbec  ; -> 0035DBEC
0035DBCA  test     byte ptr [rsp + 0x30], 3
0035DBCF  jne      0x35dbec  ; -> 0035DBEC
0035DBD1  mov      edx, edi
0035DBD3  mov      ecx, esi
0035DBD5  call     0x290300  ; -> 00290300 fn
0035DBDA  xor      eax, eax
0035DBDC  mov      rbx, qword ptr [rsp + 0x38]
0035DBE1  mov      rsi, qword ptr [rsp + 0x40]
0035DBE6  add      rsp, 0x20
0035DBEA  pop      rdi
0035DBEB  ret      
0035DBEC  mov      ecx, esi
0035DBEE  call     0x290940  ; -> 00290940 fn
0035DBF3  xor      eax, eax
0035DBF5  mov      rbx, qword ptr [rsp + 0x38]
0035DBFA  mov      rsi, qword ptr [rsp + 0x40]
0035DBFF  add      rsp, 0x20
0035DC03  pop      rdi
0035DC04  ret      
0035DC05  mov      eax, dword ptr [rip + 0x1aae5d1]  ; -> 01E0C1DC [u32 0x000001C0]
0035DC0B  xor      edi, edi
0035DC0D  mov      ecx, dword ptr [rip + 0x1aae5c5]  ; -> 01E0C1D8 [u32 0x00000200]
0035DC13  test     rbx, rbx
0035DC16  je       0x35dc2c  ; -> 0035DC2C
0035DC18  mov      dword ptr [rbx + 0x98], edi
0035DC1E  mov      word ptr [rbx + 0x9c], cx
0035DC25  mov      word ptr [rbx + 0x9e], ax
0035DC2C  xor      edx, edx
0035DC2E  mov      rcx, rbx
0035DC31  call     0x247950  ; -> 00247950 fn
0035DC36  mov      qword ptr [rbx + 0xc0], rdi
0035DC3D  mov      dword ptr [rbx + 0xc8], edi
0035DC43  mov      rbx, qword ptr [rsp + 0x38]
0035DC48  xor      eax, eax
0035DC4A  mov      rsi, qword ptr [rsp + 0x40]
0035DC4F  add      rsp, 0x20
0035DC53  pop      rdi
0035DC54  ret      
```

## 0035DC60 (46 B, extent 0035DC60-0035DC8E)

Documented callee on this page: `00244F50`

```
0035DC60  sub      rsp, 0x28
0035DC64  cmp      qword ptr [rip + 0x1f6a73c], 0  ; -> 022C83A8
0035DC6C  jne      0x35dc89  ; -> 0035DC89
0035DC6E  xor      r8d, r8d
0035DC71  lea      rdx, [rip - 0x188]  ; -> 0035DAF0
0035DC78  mov      ecx, 0xd0
0035DC7D  call     0x244f50  ; -> 00244F50 fn
0035DC82  mov      qword ptr [rip + 0x1f6a71f], rax  ; -> 022C83A8
0035DC89  add      rsp, 0x28
0035DC8D  ret      
```

## 003DF360 (122 B, extent 003DF360-003DF3DA)

Documented callee on this page: `002DF070`

```
003DF360  cmp      edx, 7
003DF363  ja       0x3df3d9  ; -> 003DF3D9
003DF365  mov      qword ptr [rsp + 0x10], rbx
003DF36A  push     rdi
003DF36B  sub      rsp, 0x20
003DF36F  movsxd   rax, edx
003DF372  mov      rdi, r9
003DF375  mov      qword ptr [rsp + 0x30], rsi
003DF37A  mov      rbx, r8
003DF37D  movsxd   rcx, ecx
003DF380  lea      rcx, [rax + rcx*8]
003DF384  imul     rsi, rcx, 0x38
003DF388  lea      rax, [rip + 0x2779fd1]  ; -> 02B59360
003DF38F  add      rsi, rax
003DF392  je       0x3df3ca  ; -> 003DF3CA
003DF394  test     rbx, rbx
003DF397  je       0x3df3ca  ; -> 003DF3CA
003DF399  mov      qword ptr [rsi + 8], rbx
003DF39D  test     r9, r9
003DF3A0  jne      0x3df3a9  ; -> 003DF3A9
003DF3A2  mov      edi, dword ptr [r8 + 0xc]
003DF3A6  add      rdi, rbx
003DF3A9  or       ecx, 0xffffffff
003DF3AC  call     0x2dee90  ; -> 002DEE90 fn
003DF3B1  mov      edx, dword ptr [rbx + 8]
003DF3B4  mov      rcx, rdi
003DF3B7  call     0x2df070  ; -> 002DF070 fn
003DF3BC  or       ecx, 0xffffffff
003DF3BF  mov      dword ptr [rsi], eax
003DF3C1  call     0x2dee90  ; -> 002DEE90 fn
003DF3C6  mov      byte ptr [rsi + 0x10], 4
003DF3CA  mov      rsi, qword ptr [rsp + 0x30]
003DF3CF  mov      rbx, qword ptr [rsp + 0x38]
003DF3D4  add      rsp, 0x20
003DF3D8  pop      rdi
003DF3D9  ret      
```

## 003E8BF0 (81 B, extent 003E8BF0-003E8C41)

Documented callee on this page: `003E8C50`

```
003E8BF0  sub      rsp, 0x28
003E8BF4  mov      r10, qword ptr [rip + 0x2774485]  ; -> 02B5D080
003E8BFB  test     r10, r10
003E8BFE  je       0x3e8c3c  ; -> 003E8C3C
003E8C00  mov      qword ptr [rsp + 0x30], rbx
003E8C05  mov      qword ptr [rsp + 0x20], rdi
003E8C0A  call     0x3e8230  ; -> 003E8230 fn
003E8C0F  movzx    ebx, word ptr [r10 + 0xe]
003E8C14  mov      rdi, rax
003E8C17  add      rbx, r10
003E8C1A  test     rax, rax
003E8C1D  je       0x3e8c32  ; -> 003E8C32
003E8C1F  call     0x265920  ; -> 00265920 fn
003E8C24  mov      r8d, eax
003E8C27  mov      rdx, rbx
003E8C2A  mov      rcx, rdi
003E8C2D  call     0x3e8c50  ; -> 003E8C50 fn
003E8C32  mov      rbx, qword ptr [rsp + 0x30]
003E8C37  mov      rdi, qword ptr [rsp + 0x20]
003E8C3C  add      rsp, 0x28
003E8C40  ret      
```

## 004051B0 (31 B, extent 004051B0-004051CF)

Documented callee on this page: `00244F50`

```
004051B0  cmp      qword ptr [rip + 0x275dbd0], 0  ; -> 02B62D88
004051B8  jne      0x4051ce  ; -> 004051CE
004051BA  xor      r8d, r8d
004051BD  lea      rdx, [rip + 0x189c]  ; -> 00406A60
004051C4  mov      ecx, 0xf0
004051C9  jmp      0x244f50  ; -> 00244F50 fn
004051CE  ret      
```

## 00467B30 (34 B, extent 00467B30-00467B52)

Documented callee on this page: `003EC8A0`

```
00467B30  push     rbx
00467B32  sub      rsp, 0x20
00467B36  mov      rax, qword ptr [rcx + 0x10]
00467B3A  mov      rbx, rcx
00467B3D  test     rax, rax
00467B40  je       0x467b44  ; -> 00467B44
00467B42  call     rax
00467B44  lea      rcx, [rbx + 8]
00467B48  add      rsp, 0x20
00467B4C  pop      rbx
00467B4D  jmp      0x3ec8a0  ; -> 003EC8A0 fn
```

## 00473640 (61 B, extent 00473640-0047367D)

Documented callee on this page: `0026FE50`

```
00473640  mov      qword ptr [rsp + 8], rbx
00473645  push     rdi
00473646  sub      rsp, 0x20
0047364A  mov      edi, r8d
0047364D  mov      ebx, ecx
0047364F  test     edx, edx
00473651  je       0x47366e  ; -> 0047366E
00473653  call     0x265920  ; -> 00265920 fn
00473658  mov      r8d, edi
0047365B  mov      edx, eax
0047365D  mov      ecx, ebx
0047365F  mov      rbx, qword ptr [rsp + 0x30]
00473664  add      rsp, 0x20
00473668  pop      rdi
00473669  jmp      0x26fad0  ; -> 0026FAD0 fn
0047366E  mov      rbx, qword ptr [rsp + 0x30]
00473673  add      rsp, 0x20
00473677  pop      rdi
00473678  jmp      0x26fe50  ; -> 0026FE50 fn
```

## 00474070 (140 B, extent 00474070-004740FC)

Documented callee on this page: `00244F50`

```
00474070  sub      rsp, 0x58
00474074  mov      rax, qword ptr [rip + 0x1ad07b5]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0047407B  xor      rax, rsp
0047407E  mov      qword ptr [rsp + 0x48], rax
00474083  mov      eax, dword ptr [rsp + 0x80]
0047408A  mov      dword ptr [rsp + 0x44], eax
0047408E  lea      rax, [rsp + 0x38]
00474093  mov      qword ptr [rsp + 0x30], rax
00474098  mov      rax, qword ptr [rsp + 0x88]
004740A0  mov      dword ptr [rsp + 0x38], edx
004740A4  lea      rdx, [rip + 0x55]  ; -> 00474100
004740AB  mov      dword ptr [rsp + 0x3c], r8d
004740B0  lea      r8, [rsp + 0x20]
004740B5  mov      qword ptr [rsp + 0x28], rcx
004740BA  mov      ecx, 0x1d8
004740BF  mov      qword ptr [rip + 0x2832bb2], rax  ; -> 02CA6C78
004740C6  mov      dword ptr [rsp + 0x40], r9d
004740CB  mov      dword ptr [rsp + 0x20], 0
004740D3  call     0x244f50  ; -> 00244F50 fn
004740D8  mov      qword ptr [rip + 0x2832ba1], rax  ; -> 02CA6C80
004740DF  mov      qword ptr [rip + 0x2832b8e], 0  ; -> 02CA6C78
004740EA  mov      rcx, qword ptr [rsp + 0x48]
004740EF  xor      rcx, rsp
004740F2  call     0x808c40  ; -> 00808C40 fn
004740F7  add      rsp, 0x58
004740FB  ret      
```

## 00536140 (66 B, extent 00536140-00536182)

Documented callee on this page: `003EC8A0`

```
00536140  mov      qword ptr [rsp + 0x10], rdx
00536145  push     rbx
00536146  sub      rsp, 0x20
0053614A  mov      rbx, qword ptr [rdx + 8]
0053614E  mov      rdx, qword ptr [rdx]
00536151  mov      qword ptr [rbx], rdx
00536154  mov      qword ptr [rdx + 8], rbx
00536158  dec      dword ptr [rcx + 0x14]
0053615B  mov      rax, qword ptr [rcx + 0x18]
0053615F  test     rax, rax
00536162  je       0x53616f  ; -> 0053616F
00536164  mov      rcx, qword ptr [rsp + 0x38]
00536169  add      rcx, 0x10
0053616D  call     rax
0053616F  lea      rcx, [rsp + 0x38]
00536174  call     0x3ec8a0  ; -> 003EC8A0 fn
00536179  mov      rax, rbx
0053617C  add      rsp, 0x20
00536180  pop      rbx
00536181  ret      
```

## 0053EB30 (60 B, extent 0053EB30-0053EB6C)

Documented callee on this page: `00244F00`

```
0053EB30  sub      rsp, 0x28
0053EB34  cmp      qword ptr [rip + 0x2769f3c], 0  ; -> 02CA8A78
0053EB3C  jne      0x53eb52  ; -> 0053EB52
0053EB3E  xor      r8d, r8d
0053EB41  lea      rdx, [rip + 0x358]  ; -> 0053EEA0
0053EB48  mov      ecx, 0xc8
0053EB4D  call     0x244f50  ; -> 00244F50 fn
0053EB52  mov      rcx, qword ptr [rip + 0x2769f27]  ; -> 02CA8A80
0053EB59  test     rcx, rcx
0053EB5C  je       0x53eb67  ; -> 0053EB67
0053EB5E  add      rsp, 0x28
0053EB62  jmp      0x244f00  ; -> 00244F00 fn
0053EB67  add      rsp, 0x28
0053EB6B  ret      
```
