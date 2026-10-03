# F homing pack (FABLE): `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 32. No bearing page cites them and no documented function calls them directly.

## 005CC4E0 (133 B, extent 005CC4E0-005CC565)

Documented callee on this page: `005A6670`

```
005CC4E0  mov      qword ptr [rsp + 0x18], rbx
005CC4E5  push     rsi
005CC4E6  sub      rsp, 0x20
005CC4EA  mov      rbx, r9
005CC4ED  mov      rsi, r8
005CC4F0  mov      r9, rdx
005CC4F3  mov      r8, rcx
005CC4F6  test     rdx, rdx
005CC4F9  je       0x5cc558  ; -> 005CC558
005CC4FB  mov      rax, qword ptr [rsp + 0x50]
005CC500  mov      rcx, r9
005CC503  mov      qword ptr [rsp + 0x30], rdi
005CC508  add      qword ptr [rax], 8
005CC50C  mov      rax, qword ptr [rax]
005CC50F  mov      edx, dword ptr [rax - 8]
005CC512  call     qword ptr [r8 + 8]
005CC516  mov      edi, eax
005CC518  test     rbx, rbx
005CC51B  je       0x5cc546  ; -> 005CC546
005CC51D  call     0x5a6670  ; -> 005A6670 fn
005CC522  cmp      rsi, rax
005CC525  jne      0x5cc546  ; -> 005CC546
005CC527  mov      dword ptr [rbx + 8], edi
005CC52A  mov      eax, 1
005CC52F  mov      rdi, qword ptr [rsp + 0x30]
005CC534  mov      qword ptr [rbx], 0
005CC53B  mov      rbx, qword ptr [rsp + 0x40]
005CC540  add      rsp, 0x20
005CC544  pop      rsi
005CC545  ret      
005CC546  xor      eax, eax
005CC548  mov      rdi, qword ptr [rsp + 0x30]
005CC54D  mov      rbx, qword ptr [rsp + 0x40]
005CC552  add      rsp, 0x20
005CC556  pop      rsi
005CC557  ret      
005CC558  xor      eax, eax
005CC55A  mov      rbx, qword ptr [rsp + 0x40]
005CC55F  add      rsp, 0x20
005CC563  pop      rsi
005CC564  ret      
```

## 005FFB10 (114 B, extent 005FFB10-005FFB82)

Documented callee on this page: `005F86B0`

```
005FFB10  mov      qword ptr [rsp + 8], rbx
005FFB15  mov      qword ptr [rsp + 0x10], rbp
005FFB1A  mov      qword ptr [rsp + 0x18], rsi
005FFB1F  push     rdi
005FFB20  sub      rsp, 0x20
005FFB24  mov      rdi, rcx
005FFB27  mov      rbx, rdx
005FFB2A  mov      rcx, rdx
005FFB2D  call     0x683b10  ; -> 00683B10 fn
005FFB32  xor      r8d, r8d
005FFB35  or       edx, 0xffffffff
005FFB38  mov      rcx, rbx
005FFB3B  mov      rsi, rax
005FFB3E  call     0x811470  ; -> 00811470 fn
005FFB43  mov      edx, 0xfffffffe
005FFB48  mov      rcx, rbx
005FFB4B  mov      rbp, rax
005FFB4E  call     0x811130  ; -> 00811130 fn
005FFB53  mov      rcx, rbx
005FFB56  call     0x5f86b0  ; -> 005F86B0 fn
005FFB5B  test     rax, rax
005FFB5E  je       0x5ffb6b  ; -> 005FFB6B
005FFB60  mov      r8, rsi
005FFB63  mov      edx, ebp
005FFB65  mov      rcx, rax
005FFB68  call     qword ptr [rdi + 8]
005FFB6B  mov      rbx, qword ptr [rsp + 0x30]
005FFB70  xor      eax, eax
005FFB72  mov      rbp, qword ptr [rsp + 0x38]
005FFB77  mov      rsi, qword ptr [rsp + 0x40]
005FFB7C  add      rsp, 0x20
005FFB80  pop      rdi
005FFB81  ret      
```

## 0063C220 (69 B, extent 0063C220-0063C265)

Documented callee on this page: `00811470`

```
0063C220  mov      qword ptr [rsp + 8], rbx
0063C225  mov      qword ptr [rsp + 0x10], rsi
0063C22A  push     rdi
0063C22B  sub      rsp, 0x20
0063C22F  mov      rdi, rdx
0063C232  mov      rsi, r8
0063C235  mov      rcx, rdi
0063C238  xor      r8d, r8d
0063C23B  or       edx, 0xffffffff
0063C23E  call     0x811470  ; -> 00811470 fn
0063C243  mov      edx, 0xfffffffe
0063C248  mov      rcx, rdi
0063C24B  mov      rbx, rax
0063C24E  call     0x811130  ; -> 00811130 fn
0063C253  mov      byte ptr [rsi], bl
0063C255  mov      rbx, qword ptr [rsp + 0x30]
0063C25A  mov      rsi, qword ptr [rsp + 0x38]
0063C25F  add      rsp, 0x20
0063C263  pop      rdi
0063C264  ret      
```

## 0063C270 (70 B, extent 0063C270-0063C2B6)

Documented callee on this page: `00811470`

```
0063C270  mov      qword ptr [rsp + 8], rbx
0063C275  mov      qword ptr [rsp + 0x10], rsi
0063C27A  push     rdi
0063C27B  sub      rsp, 0x20
0063C27F  mov      rdi, rdx
0063C282  mov      rsi, r8
0063C285  mov      rcx, rdi
0063C288  xor      r8d, r8d
0063C28B  or       edx, 0xffffffff
0063C28E  call     0x811470  ; -> 00811470 fn
0063C293  mov      edx, 0xfffffffe
0063C298  mov      rcx, rdi
0063C29B  mov      rbx, rax
0063C29E  call     0x811130  ; -> 00811130 fn
0063C2A3  mov      word ptr [rsi], bx
0063C2A6  mov      rbx, qword ptr [rsp + 0x30]
0063C2AB  mov      rsi, qword ptr [rsp + 0x38]
0063C2B0  add      rsp, 0x20
0063C2B4  pop      rdi
0063C2B5  ret      
```

## 0063C2C0 (69 B, extent 0063C2C0-0063C305)

Documented callee on this page: `00811470`

```
0063C2C0  mov      qword ptr [rsp + 8], rbx
0063C2C5  mov      qword ptr [rsp + 0x10], rsi
0063C2CA  push     rdi
0063C2CB  sub      rsp, 0x20
0063C2CF  mov      rdi, rdx
0063C2D2  mov      rsi, r8
0063C2D5  mov      rcx, rdi
0063C2D8  xor      r8d, r8d
0063C2DB  or       edx, 0xffffffff
0063C2DE  call     0x811470  ; -> 00811470 fn
0063C2E3  mov      edx, 0xfffffffe
0063C2E8  mov      rcx, rdi
0063C2EB  mov      rbx, rax
0063C2EE  call     0x811130  ; -> 00811130 fn
0063C2F3  mov      dword ptr [rsi], ebx
0063C2F5  mov      rbx, qword ptr [rsp + 0x30]
0063C2FA  mov      rsi, qword ptr [rsp + 0x38]
0063C2FF  add      rsp, 0x20
0063C303  pop      rdi
0063C304  ret      
```

## 0063C3B0 (77 B, extent 0063C3B0-0063C3FD)

Documented callee on this page: `00811470`

```
0063C3B0  mov      qword ptr [rsp + 8], rbx
0063C3B5  push     rdi
0063C3B6  sub      rsp, 0x30
0063C3BA  mov      rbx, rdx
0063C3BD  mov      rdi, r8
0063C3C0  mov      rcx, rbx
0063C3C3  xor      r8d, r8d
0063C3C6  or       edx, 0xffffffff
0063C3C9  call     0x811470  ; -> 00811470 fn
0063C3CE  mov      edx, 0xfffffffe
0063C3D3  mov      qword ptr [rsp + 0x20], rax
0063C3D8  mov      rcx, rbx
0063C3DB  mov      qword ptr [rsp + 0x28], 0
0063C3E4  call     0x811130  ; -> 00811130 fn
0063C3E9  movaps   xmm0, xmmword ptr [rsp + 0x20]
0063C3EE  mov      rbx, qword ptr [rsp + 0x40]
0063C3F3  movdqa   xmmword ptr [rdi], xmm0
0063C3F7  add      rsp, 0x30
0063C3FB  pop      rdi
0063C3FC  ret      
```

## 0063C400 (70 B, extent 0063C400-0063C446)

Documented callee on this page: `00811470`

```
0063C400  mov      qword ptr [rsp + 8], rbx
0063C405  mov      qword ptr [rsp + 0x10], rsi
0063C40A  push     rdi
0063C40B  sub      rsp, 0x20
0063C40F  mov      rdi, rdx
0063C412  mov      rsi, r8
0063C415  mov      rcx, rdi
0063C418  xor      r8d, r8d
0063C41B  or       edx, 0xffffffff
0063C41E  call     0x811470  ; -> 00811470 fn
0063C423  mov      edx, 0xfffffffe
0063C428  mov      rcx, rdi
0063C42B  mov      rbx, rax
0063C42E  call     0x811130  ; -> 00811130 fn
0063C433  mov      qword ptr [rsi], rbx
0063C436  mov      rbx, qword ptr [rsp + 0x30]
0063C43B  mov      rsi, qword ptr [rsp + 0x38]
0063C440  add      rsp, 0x20
0063C444  pop      rdi
0063C445  ret      
```

## 0063D200 (51 B, extent 0063D200-0063D233)

Documented callee on this page: `0080F420`

```
0063D200  mov      qword ptr [rsp + 8], rbx
0063D205  push     rdi
0063D206  sub      rsp, 0x20
0063D20A  mov      rdi, rdx
0063D20D  mov      rbx, r8
0063D210  mov      rcx, rdi
0063D213  mov      edx, 1
0063D218  call     0x80f420  ; -> 0080F420 fn
0063D21D  movss    xmm1, dword ptr [rbx]
0063D221  mov      rcx, rdi
0063D224  mov      rbx, qword ptr [rsp + 0x30]
0063D229  add      rsp, 0x20
0063D22D  pop      rdi
0063D22E  jmp      0x810640  ; -> 00810640 fn
```

## 0063D240 (55 B, extent 0063D240-0063D277)

Documented callee on this page: `0080F420`

```
0063D240  mov      qword ptr [rsp + 8], rbx
0063D245  push     rdi
0063D246  sub      rsp, 0x20
0063D24A  mov      rdi, rdx
0063D24D  mov      rbx, r8
0063D250  mov      rcx, rdi
0063D253  mov      edx, 1
0063D258  call     0x80f420  ; -> 0080F420 fn
0063D25D  movsd    xmm1, qword ptr [rbx]
0063D261  mov      rcx, rdi
0063D264  cvtpd2ps xmm1, xmm1
0063D268  mov      rbx, qword ptr [rsp + 0x30]
0063D26D  add      rsp, 0x20
0063D271  pop      rdi
0063D272  jmp      0x810640  ; -> 00810640 fn
```

## 006A76E0 (89 B, extent 006A76E0-006A7739)

Documented callee on this page: `006A75B0`

```
006A76E0  mov      qword ptr [rsp + 8], rbx
006A76E5  push     rdi
006A76E6  sub      rsp, 0x20
006A76EA  mov      rbx, rcx
006A76ED  mov      rdi, rdx
006A76F0  mov      rcx, rdx
006A76F3  call     0x6a75b0  ; -> 006A75B0 fn
006A76F8  test     rax, rax
006A76FB  je       0x6a772e  ; -> 006A772E
006A76FD  mov      rcx, rax
006A7700  call     qword ptr [rbx + 8]
006A7703  mov      edx, 1
006A7708  mov      rcx, rdi
006A770B  mov      rbx, rax
006A770E  call     0x80f420  ; -> 0080F420 fn
006A7713  mov      rdx, rbx
006A7716  mov      rcx, rdi
006A7719  call     0x810660  ; -> 00810660 fn
006A771E  mov      eax, 1
006A7723  mov      rbx, qword ptr [rsp + 0x30]
006A7728  add      rsp, 0x20
006A772C  pop      rdi
006A772D  ret      
006A772E  mov      rbx, qword ptr [rsp + 0x30]
006A7733  add      rsp, 0x20
006A7737  pop      rdi
006A7738  ret      
```

## 006A8D90 (92 B, extent 006A8D90-006A8DEC)

Documented callee on this page: `006A8B60`

```
006A8D90  mov      qword ptr [rsp + 8], rbx
006A8D95  mov      qword ptr [rsp + 0x10], rsi
006A8D9A  push     rdi
006A8D9B  sub      rsp, 0x20
006A8D9F  mov      rbx, rdx
006A8DA2  mov      rdi, rcx
006A8DA5  mov      rcx, rbx
006A8DA8  or       edx, 0xffffffff
006A8DAB  call     0x8113d0  ; -> 008113D0 fn
006A8DB0  test     eax, eax
006A8DB2  mov      edx, 0xfffffffe
006A8DB7  mov      rcx, rbx
006A8DBA  setne    sil
006A8DBE  call     0x811130  ; -> 00811130 fn
006A8DC3  mov      rcx, rbx
006A8DC6  call     0x6a8b60  ; -> 006A8B60 fn
006A8DCB  test     rax, rax
006A8DCE  je       0x6a8dda  ; -> 006A8DDA
006A8DD0  movzx    edx, sil
006A8DD4  mov      rcx, rax
006A8DD7  call     qword ptr [rdi + 8]
006A8DDA  mov      rbx, qword ptr [rsp + 0x30]
006A8DDF  xor      eax, eax
006A8DE1  mov      rsi, qword ptr [rsp + 0x38]
006A8DE6  add      rsp, 0x20
006A8DEA  pop      rdi
006A8DEB  ret      
```

## 006A8DF0 (88 B, extent 006A8DF0-006A8E48)

Documented callee on this page: `006A8B60`

```
006A8DF0  mov      qword ptr [rsp + 8], rbx
006A8DF5  push     rdi
006A8DF6  sub      rsp, 0x20
006A8DFA  mov      rbx, rcx
006A8DFD  mov      rdi, rdx
006A8E00  mov      rcx, rdx
006A8E03  call     0x6a8b60  ; -> 006A8B60 fn
006A8E08  test     rax, rax
006A8E0B  je       0x6a8e3d  ; -> 006A8E3D
006A8E0D  mov      rcx, rax
006A8E10  call     qword ptr [rbx + 8]
006A8E13  mov      edx, 1
006A8E18  mov      rcx, rdi
006A8E1B  movzx    ebx, al
006A8E1E  call     0x80f420  ; -> 0080F420 fn
006A8E23  mov      edx, ebx
006A8E25  mov      rcx, rdi
006A8E28  call     0x810450  ; -> 00810450 fn
006A8E2D  mov      eax, 1
006A8E32  mov      rbx, qword ptr [rsp + 0x30]
006A8E37  add      rsp, 0x20
006A8E3B  pop      rdi
006A8E3C  ret      
006A8E3D  mov      rbx, qword ptr [rsp + 0x30]
006A8E42  add      rsp, 0x20
006A8E46  pop      rdi
006A8E47  ret      
```

## 006A8E50 (117 B, extent 006A8E50-006A8EC5)

Documented callee on this page: `006A8B60`

```
006A8E50  mov      qword ptr [rsp + 8], rbx
006A8E55  mov      qword ptr [rsp + 0x10], rsi
006A8E5A  push     rdi
006A8E5B  sub      rsp, 0x20
006A8E5F  mov      rbx, rcx
006A8E62  mov      rdi, rdx
006A8E65  mov      rcx, rdx
006A8E68  call     0x683b50  ; -> 00683B50 fn
006A8E6D  mov      rcx, rdi
006A8E70  mov      rsi, rax
006A8E73  call     0x6a8b60  ; -> 006A8B60 fn
006A8E78  test     rax, rax
006A8E7B  je       0x6a8eb5  ; -> 006A8EB5
006A8E7D  mov      rdx, rsi
006A8E80  mov      rcx, rax
006A8E83  call     qword ptr [rbx + 8]
006A8E86  mov      edx, 1
006A8E8B  mov      rcx, rdi
006A8E8E  movzx    ebx, al
006A8E91  call     0x80f420  ; -> 0080F420 fn
006A8E96  mov      edx, ebx
006A8E98  mov      rcx, rdi
006A8E9B  call     0x810450  ; -> 00810450 fn
006A8EA0  mov      eax, 1
006A8EA5  mov      rbx, qword ptr [rsp + 0x30]
006A8EAA  mov      rsi, qword ptr [rsp + 0x38]
006A8EAF  add      rsp, 0x20
006A8EB3  pop      rdi
006A8EB4  ret      
006A8EB5  mov      rbx, qword ptr [rsp + 0x30]
006A8EBA  mov      rsi, qword ptr [rsp + 0x38]
006A8EBF  add      rsp, 0x20
006A8EC3  pop      rdi
006A8EC4  ret      
```

## 006AB030 (89 B, extent 006AB030-006AB089)

Documented callee on this page: `006AAF00`

```
006AB030  mov      qword ptr [rsp + 8], rbx
006AB035  push     rdi
006AB036  sub      rsp, 0x20
006AB03A  mov      rdi, rcx
006AB03D  mov      rbx, rdx
006AB040  mov      rcx, rdx
006AB043  call     0x6aaf00  ; -> 006AAF00 fn
006AB048  test     rax, rax
006AB04B  je       0x6ab07e  ; -> 006AB07E
006AB04D  mov      rcx, rax
006AB050  call     qword ptr [rdi + 8]
006AB053  test     rax, rax
006AB056  je       0x6ab05c  ; -> 006AB05C
006AB058  add      rax, 0x30
006AB05C  lea      r8, [rip + 0x264d40d]  ; -> 02CF8470
006AB063  mov      rdx, rax
006AB066  mov      rcx, rbx
006AB069  call     0x684080  ; -> 00684080 fn
006AB06E  mov      eax, 1
006AB073  mov      rbx, qword ptr [rsp + 0x30]
006AB078  add      rsp, 0x20
006AB07C  pop      rdi
006AB07D  ret      
006AB07E  mov      rbx, qword ptr [rsp + 0x30]
006AB083  add      rsp, 0x20
006AB087  pop      rdi
006AB088  ret      
```

## 006ACF30 (81 B, extent 006ACF30-006ACF81)

Documented callee on this page: `006AD250`

```
006ACF30  mov      qword ptr [rsp + 8], rbx
006ACF35  push     rdi
006ACF36  sub      rsp, 0x20
006ACF3A  mov      rcx, rdx
006ACF3D  mov      rdi, r8
006ACF40  call     0x6ad250  ; -> 006AD250 fn
006ACF45  mov      rbx, rax
006ACF48  test     rax, rax
006ACF4B  je       0x6acf53  ; -> 006ACF53
006ACF4D  lea      rdx, [rax + 8]
006ACF51  jmp      0x6acf55  ; -> 006ACF55
006ACF53  xor      edx, edx
006ACF55  lea      rcx, [rdi + 8]
006ACF59  call     0x18a4a0  ; -> 0018A4A0 fn
006ACF5E  mov      eax, dword ptr [rbx + 0xc8]
006ACF64  mov      dword ptr [rdi + 0xc8], eax
006ACF6A  mov      eax, dword ptr [rbx + 0xd0]
006ACF70  mov      rbx, qword ptr [rsp + 0x30]
006ACF75  mov      dword ptr [rdi + 0xd0], eax
006ACF7B  add      rsp, 0x20
006ACF7F  pop      rdi
006ACF80  ret      
```

## 006AD7A0 (93 B, extent 006AD7A0-006AD7FD)

Documented callee on this page: `006AD9D0`

```
006AD7A0  mov      qword ptr [rsp + 8], rbx
006AD7A5  push     rdi
006AD7A6  sub      rsp, 0x20
006AD7AA  mov      rcx, rdx
006AD7AD  mov      rdi, r8
006AD7B0  call     0x6ad9d0  ; -> 006AD9D0 fn
006AD7B5  mov      rbx, rax
006AD7B8  test     rax, rax
006AD7BB  je       0x6ad7c3  ; -> 006AD7C3
006AD7BD  lea      rdx, [rax + 8]
006AD7C1  jmp      0x6ad7c5  ; -> 006AD7C5
006AD7C3  xor      edx, edx
006AD7C5  lea      rcx, [rdi + 8]
006AD7C9  call     0x18a4a0  ; -> 0018A4A0 fn
006AD7CE  mov      eax, dword ptr [rbx + 0xc8]
006AD7D4  mov      dword ptr [rdi + 0xc8], eax
006AD7DA  mov      eax, dword ptr [rbx + 0xd0]
006AD7E0  mov      dword ptr [rdi + 0xd0], eax
006AD7E6  mov      eax, dword ptr [rbx + 0xd4]
006AD7EC  mov      rbx, qword ptr [rsp + 0x30]
006AD7F1  mov      dword ptr [rdi + 0xd4], eax
006AD7F7  add      rsp, 0x20
006AD7FB  pop      rdi
006AD7FC  ret      
```

## 006AF060 (86 B, extent 006AF060-006AF0B6)

Documented callee on this page: `006AEE00`

```
006AF060  mov      qword ptr [rsp + 8], rbx
006AF065  push     rdi
006AF066  sub      rsp, 0x20
006AF06A  mov      rbx, rcx
006AF06D  mov      rdi, rdx
006AF070  mov      rcx, rdx
006AF073  call     0x6aee00  ; -> 006AEE00 fn
006AF078  test     rax, rax
006AF07B  je       0x6af0ab  ; -> 006AF0AB
006AF07D  mov      rcx, rax
006AF080  call     qword ptr [rbx + 8]
006AF083  xor      ecx, ecx
006AF085  mov      rbx, rax
006AF088  call     0x6ae780  ; -> 006AE780 fn
006AF08D  mov      r8, rax
006AF090  mov      rdx, rbx
006AF093  mov      rcx, rdi
006AF096  call     0x684080  ; -> 00684080 fn
006AF09B  mov      eax, 1
006AF0A0  mov      rbx, qword ptr [rsp + 0x30]
006AF0A5  add      rsp, 0x20
006AF0A9  pop      rdi
006AF0AA  ret      
006AF0AB  mov      rbx, qword ptr [rsp + 0x30]
006AF0B0  add      rsp, 0x20
006AF0B4  pop      rdi
006AF0B5  ret      
```

## 006B38C0 (102 B, extent 006B38C0-006B3926)

Documented callee on this page: `006B3780`

```
006B38C0  mov      qword ptr [rsp + 8], rbx
006B38C5  mov      qword ptr [rsp + 0x10], rsi
006B38CA  push     rdi
006B38CB  sub      rsp, 0x20
006B38CF  mov      rdi, rcx
006B38D2  mov      rbx, rdx
006B38D5  mov      rcx, rdx
006B38D8  call     0x683bf0  ; -> 00683BF0 fn
006B38DD  mov      rcx, rbx
006B38E0  mov      rsi, rax
006B38E3  call     0x6b3780  ; -> 006B3780 fn
006B38E8  test     rax, rax
006B38EB  je       0x6b3916  ; -> 006B3916
006B38ED  mov      rdx, rsi
006B38F0  mov      rcx, rax
006B38F3  call     qword ptr [rdi + 8]
006B38F6  mov      rdx, rax
006B38F9  mov      rcx, rbx
006B38FC  call     0x6b3610  ; -> 006B3610 fn
006B3901  mov      eax, 1
006B3906  mov      rbx, qword ptr [rsp + 0x30]
006B390B  mov      rsi, qword ptr [rsp + 0x38]
006B3910  add      rsp, 0x20
006B3914  pop      rdi
006B3915  ret      
006B3916  mov      rbx, qword ptr [rsp + 0x30]
006B391B  mov      rsi, qword ptr [rsp + 0x38]
006B3920  add      rsp, 0x20
006B3924  pop      rdi
006B3925  ret      
```

## 006B5310 (77 B, extent 006B5310-006B535D)

Documented callee on this page: `006B5170`

```
006B5310  mov      qword ptr [rsp + 8], rbx
006B5315  push     rdi
006B5316  sub      rsp, 0x20
006B531A  mov      rdi, rcx
006B531D  mov      rbx, rdx
006B5320  mov      rcx, rdx
006B5323  call     0x6b5170  ; -> 006B5170 fn
006B5328  test     rax, rax
006B532B  je       0x6b5352  ; -> 006B5352
006B532D  movsxd   rcx, dword ptr [rdi + 0x10]
006B5331  add      rcx, rax
006B5334  call     qword ptr [rdi + 8]
006B5337  mov      rdx, rax
006B533A  mov      rcx, rbx
006B533D  call     0x684130  ; -> 00684130 fn
006B5342  mov      eax, 1
006B5347  mov      rbx, qword ptr [rsp + 0x30]
006B534C  add      rsp, 0x20
006B5350  pop      rdi
006B5351  ret      
006B5352  mov      rbx, qword ptr [rsp + 0x30]
006B5357  add      rsp, 0x20
006B535B  pop      rdi
006B535C  ret      
```

## 006B5360 (84 B, extent 006B5360-006B53B4)

Documented callee on this page: `006B5170`

```
006B5360  mov      qword ptr [rsp + 8], rbx
006B5365  push     rdi
006B5366  sub      rsp, 0x20
006B536A  mov      rdi, rcx
006B536D  mov      rbx, rdx
006B5370  mov      rcx, rdx
006B5373  call     0x6b5170  ; -> 006B5170 fn
006B5378  test     rax, rax
006B537B  je       0x6b53a9  ; -> 006B53A9
006B537D  movsxd   rcx, dword ptr [rdi + 0x10]
006B5381  add      rcx, rax
006B5384  call     qword ptr [rdi + 8]
006B5387  lea      r8, [rip + 0x27982a2]  ; -> 02E4D630
006B538E  mov      rcx, rbx
006B5391  mov      rdx, rax
006B5394  call     0x684080  ; -> 00684080 fn
006B5399  mov      eax, 1
006B539E  mov      rbx, qword ptr [rsp + 0x30]
006B53A3  add      rsp, 0x20
006B53A7  pop      rdi
006B53A8  ret      
006B53A9  mov      rbx, qword ptr [rsp + 0x30]
006B53AE  add      rsp, 0x20
006B53B2  pop      rdi
006B53B3  ret      
```

## 006B5460 (124 B, extent 006B5460-006B54DC)

Documented callee on this page: `006B5170`

```
006B5460  mov      qword ptr [rsp + 8], rbx
006B5465  push     rdi
006B5466  sub      rsp, 0x20
006B546A  mov      rdi, rcx
006B546D  mov      rbx, rdx
006B5470  mov      rcx, rdx
006B5473  call     0x6b5170  ; -> 006B5170 fn
006B5478  test     rax, rax
006B547B  je       0x6b54d1  ; -> 006B54D1
006B547D  movsxd   rcx, dword ptr [rdi + 0x10]
006B5481  add      rcx, rax
006B5484  call     qword ptr [rdi + 8]
006B5487  mov      rcx, rbx
006B548A  test     rax, rax
006B548D  je       0x6b54af  ; -> 006B54AF
006B548F  lea      rdx, [rax + 8]
006B5493  lea      r8, [rip + 0x279c436]  ; -> 02E518D0
006B549A  call     0x684080  ; -> 00684080 fn
006B549F  mov      eax, 1
006B54A4  mov      rbx, qword ptr [rsp + 0x30]
006B54A9  add      rsp, 0x20
006B54AD  pop      rdi
006B54AE  ret      
006B54AF  mov      edx, 1
006B54B4  call     0x80f420  ; -> 0080F420 fn
006B54B9  mov      rcx, rbx
006B54BC  call     0x810620  ; -> 00810620 fn
006B54C1  mov      eax, 1
006B54C6  mov      rbx, qword ptr [rsp + 0x30]
006B54CB  add      rsp, 0x20
006B54CF  pop      rdi
006B54D0  ret      
006B54D1  mov      rbx, qword ptr [rsp + 0x30]
006B54D6  add      rsp, 0x20
006B54DA  pop      rdi
006B54DB  ret      
```

## 006B54E0 (123 B, extent 006B54E0-006B555B)

Documented callee on this page: `006B5170`

```
006B54E0  mov      qword ptr [rsp + 8], rbx
006B54E5  push     rdi
006B54E6  sub      rsp, 0x20
006B54EA  mov      rdi, rcx
006B54ED  mov      rbx, rdx
006B54F0  mov      rcx, rdx
006B54F3  call     0x6b5170  ; -> 006B5170 fn
006B54F8  test     rax, rax
006B54FB  je       0x6b5550  ; -> 006B5550
006B54FD  movsxd   rcx, dword ptr [rdi + 0x10]
006B5501  add      rcx, rax
006B5504  call     qword ptr [rdi + 8]
006B5507  mov      rcx, rbx
006B550A  test     rax, rax
006B550D  je       0x6b552e  ; -> 006B552E
006B550F  lea      r8, [rip + 0x278af9a]  ; -> 02E404B0
006B5516  mov      rdx, rax
006B5519  call     0x684080  ; -> 00684080 fn
006B551E  mov      eax, 1
006B5523  mov      rbx, qword ptr [rsp + 0x30]
006B5528  add      rsp, 0x20
006B552C  pop      rdi
006B552D  ret      
006B552E  mov      edx, 1
006B5533  call     0x80f420  ; -> 0080F420 fn
006B5538  mov      rcx, rbx
006B553B  call     0x810620  ; -> 00810620 fn
006B5540  mov      eax, 1
006B5545  mov      rbx, qword ptr [rsp + 0x30]
006B554A  add      rsp, 0x20
006B554E  pop      rdi
006B554F  ret      
006B5550  mov      rbx, qword ptr [rsp + 0x30]
006B5555  add      rsp, 0x20
006B5559  pop      rdi
006B555A  ret      
```

## 006B5560 (40 B, extent 006B5560-006B5588)

Documented callee on this page: `006B5170`

```
006B5560  push     rbx
006B5562  sub      rsp, 0x20
006B5566  mov      rbx, rcx
006B5569  mov      rcx, rdx
006B556C  call     0x6b5170  ; -> 006B5170 fn
006B5571  test     rax, rax
006B5574  je       0x6b5580  ; -> 006B5580
006B5576  movsxd   rcx, dword ptr [rbx + 0x10]
006B557A  add      rcx, rax
006B557D  call     qword ptr [rbx + 8]
006B5580  xor      eax, eax
006B5582  add      rsp, 0x20
006B5586  pop      rbx
006B5587  ret      
```

## 006BFDE0 (91 B, extent 006BFDE0-006BFE3B)

Documented callee on this page: `006BFB10`

```
006BFDE0  mov      qword ptr [rsp + 8], rbx
006BFDE5  push     rdi
006BFDE6  sub      rsp, 0x30
006BFDEA  mov      rbx, rdx
006BFDED  movaps   xmmword ptr [rsp + 0x20], xmm6
006BFDF2  mov      rdi, rcx
006BFDF5  xor      r8d, r8d
006BFDF8  mov      rcx, rbx
006BFDFB  or       edx, 0xffffffff
006BFDFE  call     0x811640  ; -> 00811640 fn
006BFE03  mov      edx, 0xfffffffe
006BFE08  mov      rcx, rbx
006BFE0B  movaps   xmm6, xmm0
006BFE0E  call     0x811130  ; -> 00811130 fn
006BFE13  mov      rcx, rbx
006BFE16  call     0x6bfb10  ; -> 006BFB10 fn
006BFE1B  test     rax, rax
006BFE1E  je       0x6bfe29  ; -> 006BFE29
006BFE20  movaps   xmm1, xmm6
006BFE23  mov      rcx, rax
006BFE26  call     qword ptr [rdi + 8]
006BFE29  mov      rbx, qword ptr [rsp + 0x40]
006BFE2E  xor      eax, eax
006BFE30  movaps   xmm6, xmmword ptr [rsp + 0x20]
006BFE35  add      rsp, 0x30
006BFE39  pop      rdi
006BFE3A  ret      
```

## 006C4AC0 (78 B, extent 006C4AC0-006C4B0E)

Documented callee on this page: `006C6D60`

```
006C4AC0  mov      qword ptr [rsp + 8], rbx
006C4AC5  push     rdi
006C4AC6  sub      rsp, 0x20
006C4ACA  mov      rcx, rdx
006C4ACD  mov      rdi, r8
006C4AD0  call     0x6c6d60  ; -> 006C6D60 fn
006C4AD5  mov      rbx, rax
006C4AD8  mov      rcx, qword ptr [rax]
006C4ADB  lea      rdx, [rax + 8]
006C4ADF  mov      qword ptr [rdi], rcx
006C4AE2  lea      rcx, [rdi + 8]
006C4AE6  call     0x646c00  ; -> 00646C00 fn
006C4AEB  mov      ecx, dword ptr [rbx + 0x18]
006C4AEE  lea      rdx, [rbx + 0x20]
006C4AF2  mov      dword ptr [rdi + 0x18], ecx
006C4AF5  mov      ecx, dword ptr [rbx + 0x1c]
006C4AF8  mov      dword ptr [rdi + 0x1c], ecx
006C4AFB  lea      rcx, [rdi + 0x20]
006C4AFF  mov      rbx, qword ptr [rsp + 0x30]
006C4B04  add      rsp, 0x20
006C4B08  pop      rdi
006C4B09  jmp      0x6c54d0  ; -> 006C54D0 fn
```

## 006C7580 (92 B, extent 006C7580-006C75DC)

Documented callee on this page: `006C70E0`

```
006C7580  mov      qword ptr [rsp + 8], rbx
006C7585  mov      qword ptr [rsp + 0x10], rsi
006C758A  push     rdi
006C758B  sub      rsp, 0x20
006C758F  mov      rbx, rdx
006C7592  mov      rdi, rcx
006C7595  mov      rcx, rbx
006C7598  or       edx, 0xffffffff
006C759B  call     0x8113d0  ; -> 008113D0 fn
006C75A0  test     eax, eax
006C75A2  mov      edx, 0xfffffffe
006C75A7  mov      rcx, rbx
006C75AA  setne    sil
006C75AE  call     0x811130  ; -> 00811130 fn
006C75B3  mov      rcx, rbx
006C75B6  call     0x6c70e0  ; -> 006C70E0 fn
006C75BB  test     rax, rax
006C75BE  je       0x6c75ca  ; -> 006C75CA
006C75C0  movzx    edx, sil
006C75C4  mov      rcx, rax
006C75C7  call     qword ptr [rdi + 8]
006C75CA  mov      rbx, qword ptr [rsp + 0x30]
006C75CF  xor      eax, eax
006C75D1  mov      rsi, qword ptr [rsp + 0x38]
006C75D6  add      rsp, 0x20
006C75DA  pop      rdi
006C75DB  ret      
```

## 007913D0 (61 B, extent 007913D0-0079140D)

Documented callee on this page: `00796760`

```
007913D0  mov      qword ptr [rsp + 8], rbx
007913D5  push     rdi
007913D6  sub      rsp, 0x20
007913DA  mov      rcx, rdx
007913DD  mov      rdi, r8
007913E0  call     0x796760  ; -> 00796760 fn
007913E5  mov      rbx, rax
007913E8  mov      rcx, qword ptr [rax]
007913EB  lea      rdx, [rax + 8]
007913EF  mov      qword ptr [rdi], rcx
007913F2  lea      rcx, [rdi + 8]
007913F6  call     0x7938f0  ; -> 007938F0 fn
007913FB  movzx    eax, byte ptr [rbx + 0x50]
007913FF  mov      rbx, qword ptr [rsp + 0x30]
00791404  mov      byte ptr [rdi + 0x50], al
00791407  add      rsp, 0x20
0079140B  pop      rdi
0079140C  ret      
```

## 0079A770 (89 B, extent 0079A770-0079A7C9)

Documented callee on this page: `00796960`

```
0079A770  mov      qword ptr [rsp + 8], rbx
0079A775  push     rdi
0079A776  sub      rsp, 0x20
0079A77A  mov      rbx, rcx
0079A77D  mov      rdi, rdx
0079A780  mov      rcx, rdx
0079A783  call     0x796960  ; -> 00796960 fn
0079A788  test     rax, rax
0079A78B  je       0x79a7be  ; -> 0079A7BE
0079A78D  mov      rcx, rax
0079A790  call     qword ptr [rbx + 8]
0079A793  mov      edx, 1
0079A798  mov      rcx, rdi
0079A79B  movsxd   rbx, eax
0079A79E  call     0x80f420  ; -> 0080F420 fn
0079A7A3  mov      rdx, rbx
0079A7A6  mov      rcx, rdi
0079A7A9  call     0x810580  ; -> 00810580 fn
0079A7AE  mov      eax, 1
0079A7B3  mov      rbx, qword ptr [rsp + 0x30]
0079A7B8  add      rsp, 0x20
0079A7BC  pop      rdi
0079A7BD  ret      
0079A7BE  mov      rbx, qword ptr [rsp + 0x30]
0079A7C3  add      rsp, 0x20
0079A7C7  pop      rdi
0079A7C8  ret      
```

## 0079A8B0 (103 B, extent 0079A8B0-0079A917)

Documented callee on this page: `00796960`

```
0079A8B0  mov      qword ptr [rsp + 8], rbx
0079A8B5  push     rdi
0079A8B6  sub      rsp, 0x30
0079A8BA  mov      rdi, rcx
0079A8BD  mov      rbx, rdx
0079A8C0  mov      rcx, rdx
0079A8C3  call     0x796960  ; -> 00796960 fn
0079A8C8  test     rax, rax
0079A8CB  je       0x79a90c  ; -> 0079A90C
0079A8CD  mov      rcx, rax
0079A8D0  movaps   xmmword ptr [rsp + 0x20], xmm6
0079A8D5  call     qword ptr [rdi + 8]
0079A8D8  mov      edx, 1
0079A8DD  mov      rcx, rbx
0079A8E0  movaps   xmm6, xmm0
0079A8E3  call     0x80f420  ; -> 0080F420 fn
0079A8E8  xorps    xmm1, xmm1
0079A8EB  mov      rcx, rbx
0079A8EE  cvtsd2ss xmm1, xmm6
0079A8F2  call     0x810640  ; -> 00810640 fn
0079A8F7  movaps   xmm6, xmmword ptr [rsp + 0x20]
0079A8FC  mov      eax, 1
0079A901  mov      rbx, qword ptr [rsp + 0x40]
0079A906  add      rsp, 0x30
0079A90A  pop      rdi
0079A90B  ret      
0079A90C  mov      rbx, qword ptr [rsp + 0x40]
0079A911  add      rsp, 0x30
0079A915  pop      rdi
0079A916  ret      
```

## 0079AB20 (91 B, extent 0079AB20-0079AB7B)

Documented callee on this page: `00796A90`

```
0079AB20  mov      qword ptr [rsp + 8], rbx
0079AB25  push     rdi
0079AB26  sub      rsp, 0x20
0079AB2A  mov      rbx, rcx
0079AB2D  mov      rdi, rdx
0079AB30  mov      rcx, rdx
0079AB33  call     0x796a90  ; -> 00796A90 fn
0079AB38  test     rax, rax
0079AB3B  je       0x79ab70  ; -> 0079AB70
0079AB3D  movsxd   rcx, dword ptr [rbx + 0x10]
0079AB41  add      rcx, rax
0079AB44  call     qword ptr [rbx + 8]
0079AB47  mov      edx, 1
0079AB4C  mov      rcx, rdi
0079AB4F  mov      ebx, eax
0079AB51  call     0x80f420  ; -> 0080F420 fn
0079AB56  mov      edx, ebx
0079AB58  mov      rcx, rdi
0079AB5B  call     0x810580  ; -> 00810580 fn
0079AB60  mov      eax, 1
0079AB65  mov      rbx, qword ptr [rsp + 0x30]
0079AB6A  add      rsp, 0x20
0079AB6E  pop      rdi
0079AB6F  ret      
0079AB70  mov      rbx, qword ptr [rsp + 0x30]
0079AB75  add      rsp, 0x20
0079AB79  pop      rdi
0079AB7A  ret      
```

## 0079AB80 (103 B, extent 0079AB80-0079ABE7)

Documented callee on this page: `00796A90`

```
0079AB80  mov      qword ptr [rsp + 8], rbx
0079AB85  push     rdi
0079AB86  sub      rsp, 0x30
0079AB8A  mov      rdi, rcx
0079AB8D  mov      rbx, rdx
0079AB90  mov      rcx, rdx
0079AB93  call     0x796a90  ; -> 00796A90 fn
0079AB98  test     rax, rax
0079AB9B  je       0x79abdc  ; -> 0079ABDC
0079AB9D  movsxd   rcx, dword ptr [rdi + 0x10]
0079ABA1  add      rcx, rax
0079ABA4  movaps   xmmword ptr [rsp + 0x20], xmm6
0079ABA9  call     qword ptr [rdi + 8]
0079ABAC  mov      edx, 1
0079ABB1  mov      rcx, rbx
0079ABB4  movaps   xmm6, xmm0
0079ABB7  call     0x80f420  ; -> 0080F420 fn
0079ABBC  movaps   xmm1, xmm6
0079ABBF  mov      rcx, rbx
0079ABC2  call     0x810640  ; -> 00810640 fn
0079ABC7  movaps   xmm6, xmmword ptr [rsp + 0x20]
0079ABCC  mov      eax, 1
0079ABD1  mov      rbx, qword ptr [rsp + 0x40]
0079ABD6  add      rsp, 0x30
0079ABDA  pop      rdi
0079ABDB  ret      
0079ABDC  mov      rbx, qword ptr [rsp + 0x40]
0079ABE1  add      rsp, 0x30
0079ABE5  pop      rdi
0079ABE6  ret      
```

## 0079ABF0 (36 B, extent 0079ABF0-0079AC14)

Documented callee on this page: `00796BC0`

```
0079ABF0  push     rbx
0079ABF2  sub      rsp, 0x20
0079ABF6  mov      rbx, rcx
0079ABF9  mov      rcx, rdx
0079ABFC  call     0x796bc0  ; -> 00796BC0 fn
0079AC01  test     rax, rax
0079AC04  je       0x79ac0c  ; -> 0079AC0C
0079AC06  mov      rcx, rax
0079AC09  call     qword ptr [rbx + 8]
0079AC0C  xor      eax, eax
0079AC0E  add      rsp, 0x20
0079AC12  pop      rbx
0079AC13  ret      
```
