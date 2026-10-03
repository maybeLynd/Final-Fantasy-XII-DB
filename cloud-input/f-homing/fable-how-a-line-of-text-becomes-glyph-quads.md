# F homing pack (FABLE): `99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 17. No bearing page cites them and no documented function calls them directly.

## 00290FF0 (18 B, extent 00290FF0-00291002)

Documented callee on this page: `003F7F50`

```
00290FF0  cmp      dword ptr [rdx], 4
00290FF3  jne      0x290ffd  ; -> 00290FFD
00290FF5  mov      rax, qword ptr [rcx + 0x38]
00290FF9  mov      byte ptr [rax + 0x5c], 4
00290FFD  jmp      0x3f7f50  ; -> 003F7F50 fn
```

## 002D5690 (409 B, extent 002D5690-002D5829)

Documented callee on this page: `002D8910`

```
002D5690  push     rdi
002D5692  sub      rsp, 0x30
002D5696  mov      rdi, rcx
002D5699  mov      ecx, dword ptr [rdx]
002D569B  sub      ecx, 1
002D569E  je       0x2d5745  ; -> 002D5745
002D56A4  sub      ecx, 1
002D56A7  je       0x2d5704  ; -> 002D5704
002D56A9  sub      ecx, 2
002D56AC  je       0x2d56d6  ; -> 002D56D6
002D56AE  cmp      ecx, 0xe
002D56B1  je       0x2d56c0  ; -> 002D56C0
002D56B3  mov      rcx, rdi
002D56B6  add      rsp, 0x30
002D56BA  pop      rdi
002D56BB  jmp      0x5c5230  ; -> 005C5230 fn
002D56C0  mov      rax, qword ptr [rdi + 0xd8]
002D56C7  mov      qword ptr [rax], 0
002D56CE  xor      eax, eax
002D56D0  add      rsp, 0x30
002D56D4  pop      rdi
002D56D5  ret      
002D56D6  mov      r9, qword ptr [rdi + 0xc0]
002D56DD  mov      r8d, dword ptr [rdi + 0xd0]
002D56E4  mov      edx, dword ptr [rdi + 0xcc]
002D56EA  mov      rcx, qword ptr [rdi + 0x38]
002D56EE  mov      qword ptr [rsp + 0x20], 0
002D56F7  call     0x2d8910  ; -> 002D8910 fn
002D56FC  xor      eax, eax
002D56FE  add      rsp, 0x30
002D5702  pop      rdi
002D5703  ret      
002D5704  mov      ecx, dword ptr [rdi + 0xb4]
002D570A  call     0x1edec0  ; -> 001EDEC0 fn
002D570F  test     eax, eax
002D5711  je       0x2d5821  ; -> 002D5821
002D5717  mov      eax, dword ptr [rdi + 0xc8]
002D571D  test     eax, eax
002D571F  je       0x2d5821  ; -> 002D5821
002D5725  dec      eax
002D5727  mov      dword ptr [rdi + 0xc8], eax
002D572D  test     eax, eax
002D572F  jg       0x2d5821  ; -> 002D5821
002D5735  mov      rcx, rdi
002D5738  call     0x244f00  ; -> 00244F00 fn
002D573D  xor      eax, eax
002D573F  add      rsp, 0x30
002D5743  pop      rdi
002D5744  ret      
002D5745  mov      rcx, qword ptr [rdx + 8]
002D5749  mov      qword ptr [rsp + 0x50], rbx
002D574E  mov      rax, qword ptr [rcx]
002D5751  mov      qword ptr [rdi + 0xc0], rax
002D5758  mov      eax, dword ptr [rcx + 8]
002D575B  mov      dword ptr [rdi + 0xc8], eax
002D5761  mov      rax, qword ptr [rcx + 0x10]
002D5765  mov      ecx, 3
002D576A  mov      qword ptr [rdi + 0xd8], rax
002D5771  call     0x2735e0  ; -> 002735E0 fn
002D5776  mov      rdx, rax
002D5779  mov      rcx, rdi
002D577C  call     0x247570  ; -> 00247570 fn
002D5781  mov      rax, qword ptr [rip + 0x1dc54a8]  ; -> 0209AC30
002D5788  lea      rcx, [rdi + 0x50]
002D578C  mov      r9, rdi
002D578F  xor      r8d, r8d
002D5792  mov      rdx, qword ptr [rax + 0x18]
002D5796  call     0x2432b0  ; -> 002432B0 fn
002D579B  mov      rbx, rax
002D579E  movzx    r9d, word ptr [rax + 0xa]
002D57A3  movzx    r8d, word ptr [rax + 8]
002D57A8  movsx    edx, word ptr [rax + 6]
002D57AC  movzx    ecx, word ptr [rax + 4]
002D57B0  mov      word ptr [rdi + 0x98], cx
002D57B7  xor      ecx, ecx
002D57B9  mov      word ptr [rdi + 0x9a], dx
002D57C0  mov      rdx, qword ptr [rdi + 0xc0]
002D57C7  mov      word ptr [rdi + 0x9c], r8w
002D57CF  lea      r8, [rsp + 0x40]
002D57D4  mov      word ptr [rdi + 0x9e], r9w
002D57DC  lea      r9, [rsp + 0x48]
002D57E1  call     0x2b3050  ; -> 002B3050 fn
002D57E6  movzx    eax, word ptr [rbx + 8]
002D57EA  movzx    ecx, word ptr [rsp + 0x40]
002D57EF  sub      eax, ecx
002D57F1  xor      ecx, ecx
002D57F3  cdq      
002D57F4  sub      eax, edx
002D57F6  sar      eax, 1
002D57F8  mov      dword ptr [rdi + 0xcc], eax
002D57FE  mov      rax, qword ptr [rdi + 0x60]
002D5802  mov      rbx, qword ptr [rax]
002D5805  mov      qword ptr [rbx + 0x18], 0
002D580D  call     0x20e620  ; -> 0020E620 fn
002D5812  mov      dword ptr [rbx + 0x20], eax
002D5815  and      dword ptr [rdi + 0x40], 0xffffff7f
002D581C  mov      rbx, qword ptr [rsp + 0x50]
002D5821  xor      eax, eax
002D5823  add      rsp, 0x30
002D5827  pop      rdi
002D5828  ret      
```

## 002E08C0 (117 B, extent 002E08C0-002E0935)

Documented callee on this page: `002A2720`

```
002E08C0  push     rbx
002E08C2  sub      rsp, 0x20
002E08C6  mov      eax, 7
002E08CB  test     ecx, ecx
002E08CD  jns      0x2e091c  ; -> 002E091C
002E08CF  xor      ecx, ecx
002E08D1  cmp      ecx, eax
002E08D3  cmovg    ecx, eax
002E08D6  movsxd   rax, ecx
002E08D9  imul     rbx, rax, 0x68
002E08DD  lea      rax, [rip + 0x1e7e91c]  ; -> 0215F200
002E08E4  add      rbx, rax
002E08E7  mov      rcx, qword ptr [rbx]
002E08EA  test     rcx, rcx
002E08ED  je       0x2e0929  ; -> 002E0929
002E08EF  call     0x2a2720  ; -> 002A2720 fn
002E08F4  cmp      byte ptr [rbx + 0x40], 0xff
002E08F8  mov      dword ptr [rbx + 8], 6
002E08FF  jne      0x2e090d  ; -> 002E090D
002E0901  movzx    ecx, byte ptr [rip + 0x1e7e8ae]  ; -> 0215F1B6
002E0908  call     0x2f1c50  ; -> 002F1C50 fn
002E090D  mov      eax, 1
002E0912  mov      byte ptr [rbx + 0x40], 0xfe
002E0916  add      rsp, 0x20
002E091A  pop      rbx
002E091B  ret      
002E091C  cmp      ecx, eax
002E091E  cmovg    ecx, eax
002E0921  test     ecx, ecx
002E0923  jns      0x2e08d1  ; -> 002E08D1
002E0925  xor      ecx, ecx
002E0927  jmp      0x2e08d6  ; -> 002E08D6
002E0929  xor      eax, eax
002E092B  mov      byte ptr [rbx + 0x40], 0xfe
002E092F  add      rsp, 0x20
002E0933  pop      rbx
002E0934  ret      
```

## 00352A50 (60 B, extent 00352A50-00352A8C)

Documented callee on this page: `00264D60`

```
00352A50  mov      qword ptr [rsp + 8], rbx
00352A55  push     rdi
00352A56  sub      rsp, 0x20
00352A5A  mov      rbx, r9
00352A5D  call     0x2640c0  ; -> 002640C0 fn
00352A62  mov      rcx, rbx
00352A65  mov      rdi, rax
00352A68  call     0x267e10  ; -> 00267E10 fn
00352A6D  mov      edx, eax
00352A6F  mov      rcx, rdi
00352A72  call     0x264d60  ; -> 00264D60 fn
00352A77  mov      rdx, rax
00352A7A  mov      rcx, rdi
00352A7D  mov      rbx, qword ptr [rsp + 0x30]
00352A82  add      rsp, 0x20
00352A86  pop      rdi
00352A87  jmp      0x3e8f50  ; -> 003E8F50 fn
```

## 00352EC0 (60 B, extent 00352EC0-00352EFC)

Documented callee on this page: `00264D60`

```
00352EC0  mov      qword ptr [rsp + 8], rbx
00352EC5  push     rdi
00352EC6  sub      rsp, 0x20
00352ECA  mov      rbx, r9
00352ECD  call     0x2640c0  ; -> 002640C0 fn
00352ED2  mov      rcx, rbx
00352ED5  mov      rdi, rax
00352ED8  call     0x267e10  ; -> 00267E10 fn
00352EDD  mov      edx, eax
00352EDF  mov      rcx, rdi
00352EE2  call     0x264d60  ; -> 00264D60 fn
00352EE7  mov      rdx, rax
00352EEA  mov      rcx, rdi
00352EED  mov      rbx, qword ptr [rsp + 0x30]
00352EF2  add      rsp, 0x20
00352EF6  pop      rdi
00352EF7  jmp      0x3e8fc0  ; -> 003E8FC0 fn
```

## 003534F0 (60 B, extent 003534F0-0035352C)

Documented callee on this page: `00264D60`

```
003534F0  mov      qword ptr [rsp + 8], rbx
003534F5  push     rdi
003534F6  sub      rsp, 0x20
003534FA  mov      rbx, r9
003534FD  call     0x2640c0  ; -> 002640C0 fn
00353502  mov      rcx, rbx
00353505  mov      rdi, rax
00353508  call     0x267e10  ; -> 00267E10 fn
0035350D  mov      edx, eax
0035350F  mov      rcx, rdi
00353512  call     0x264d60  ; -> 00264D60 fn
00353517  mov      rdx, rax
0035351A  mov      rcx, rdi
0035351D  mov      rbx, qword ptr [rsp + 0x30]
00353522  add      rsp, 0x20
00353526  pop      rdi
00353527  jmp      0x3e9000  ; -> 003E9000 fn
```

## 00354C50 (29 B, extent 00354C50-00354C6D)

Documented callee on this page: `002EC590`

```
00354C50  sub      rsp, 0x28
00354C54  xor      ecx, ecx
00354C56  call     0x3633b0  ; -> 003633B0 fn
00354C5B  xor      ecx, ecx
00354C5D  call     0x3634a0  ; -> 003634A0 fn
00354C62  xor      ecx, ecx
00354C64  add      rsp, 0x28
00354C68  jmp      0x2ec590  ; -> 002EC590 fn
```

## 00355060 (38 B, extent 00355060-00355086)

Documented callee on this page: `002EC590`

```
00355060  sub      rsp, 0x28
00355064  mov      ecx, 1
00355069  call     0x3633b0  ; -> 003633B0 fn
0035506E  mov      ecx, 1
00355073  call     0x3634a0  ; -> 003634A0 fn
00355078  mov      ecx, 1
0035507D  add      rsp, 0x28
00355081  jmp      0x2ec590  ; -> 002EC590 fn
```

## 003555F0 (142 B, extent 003555F0-0035567E)

Documented callee on this page: `00264D60`

```
003555F0  mov      qword ptr [rsp + 8], rbx
003555F5  mov      qword ptr [rsp + 0x10], rbp
003555FA  mov      qword ptr [rsp + 0x18], rsi
003555FF  mov      qword ptr [rsp + 0x20], rdi
00355604  push     r14
00355606  sub      rsp, 0x30
0035560A  mov      rcx, r9
0035560D  mov      rdi, r9
00355610  mov      r14, rdx
00355613  call     0x267e10  ; -> 00267E10 fn
00355618  mov      rcx, rdi
0035561B  mov      ebx, eax
0035561D  call     0x267e10  ; -> 00267E10 fn
00355622  mov      ebp, eax
00355624  call     0x2640c0  ; -> 002640C0 fn
00355629  mov      edx, ebx
0035562B  mov      rcx, rax
0035562E  mov      rsi, rax
00355631  call     0x264d60  ; -> 00264D60 fn
00355636  xor      edi, edi
00355638  mov      rcx, r14
0035563B  cmp      dword ptr [rsi + 0x28], edi
0035563E  mov      rbx, rax
00355641  setne    dil
00355645  call     0x3589b0  ; -> 003589B0 fn
0035564A  mov      r9, qword ptr [rsi + 0xb0]
00355651  lea      edx, [rdi + 4]
00355654  mov      ecx, eax
00355656  mov      qword ptr [rsp + 0x20], rbx
0035565B  mov      r8d, ebp
0035565E  call     0x3df760  ; -> 003DF760 fn
00355663  mov      rbx, qword ptr [rsp + 0x40]
00355668  mov      rbp, qword ptr [rsp + 0x48]
0035566D  mov      rsi, qword ptr [rsp + 0x50]
00355672  mov      rdi, qword ptr [rsp + 0x58]
00355677  add      rsp, 0x30
0035567B  pop      r14
0035567D  ret      
```

## 003F8510 (289 B, extent 003F8510-003F8631)

Documented callee on this page: `002D8910`

```
003F8510  mov      qword ptr [rsp + 0x10], rbx
003F8515  mov      qword ptr [rsp + 0x18], rsi
003F851A  push     rdi
003F851B  sub      rsp, 0x30
003F851F  mov      rbx, rcx
003F8522  mov      rdi, rdx
003F8525  mov      ecx, dword ptr [rdx]
003F8527  sub      ecx, 1
003F852A  je       0x3f8601  ; -> 003F8601
003F8530  cmp      ecx, 3
003F8533  je       0x3f854c  ; -> 003F854C
003F8535  mov      rcx, rbx
003F8538  mov      rbx, qword ptr [rsp + 0x48]
003F853D  mov      rsi, qword ptr [rsp + 0x50]
003F8542  add      rsp, 0x30
003F8546  pop      rdi
003F8547  jmp      0x5c5230  ; -> 005C5230 fn
003F854C  mov      rax, qword ptr [rbx + 0x98]
003F8553  lea      rdx, [rbx + 0x98]
003F855A  mov      r8, qword ptr [rbx + 0xd8]
003F8561  lea      rcx, [rsp + 0x40]
003F8566  mov      rsi, qword ptr [rbx + 0x38]
003F856A  mov      qword ptr [rsp + 0x40], rax
003F856F  call     0x249ee0  ; -> 00249EE0 fn
003F8574  test     eax, eax
003F8576  je       0x3f861f  ; -> 003F861F
003F857C  movzx    eax, word ptr [rbx + 0x9a]
003F8583  lea      rdx, [rsp + 0x40]
003F8588  sub      word ptr [rsp + 0x42], ax
003F858D  mov      rcx, rsi
003F8590  movzx    eax, word ptr [rbx + 0x98]
003F8597  sub      word ptr [rsp + 0x40], ax
003F859C  call     0x2dd2f0  ; -> 002DD2F0 fn
003F85A1  mov      dword ptr [rsi + 0x60], 0x3f400000
003F85A8  xor      edi, edi
003F85AA  mov      byte ptr [rsi + 0x65], 0
003F85AE  xor      r8d, r8d
003F85B1  mov      r9, qword ptr [rbx + 0xc0]
003F85B8  mov      rcx, rsi
003F85BB  mov      edx, dword ptr [rbx + 0xd0]
003F85C1  mov      qword ptr [rsp + 0x20], rdi
003F85C6  call     0x2d8910  ; -> 002D8910 fn
003F85CB  mov      byte ptr [rsi + 0x65], 0xfe
003F85CF  xor      r8d, r8d
003F85D2  mov      edx, dword ptr [rbx + 0xd0]
003F85D8  mov      rcx, rsi
003F85DB  mov      r9, qword ptr [rbx + 0xc8]
003F85E2  add      edx, 0x10
003F85E5  mov      qword ptr [rsp + 0x20], rdi
003F85EA  call     0x2d8910  ; -> 002D8910 fn
003F85EF  xor      eax, eax
003F85F1  mov      rbx, qword ptr [rsp + 0x48]
003F85F6  mov      rsi, qword ptr [rsp + 0x50]
003F85FB  add      rsp, 0x30
003F85FF  pop      rdi
003F8600  ret      
003F8601  mov      ecx, 6
003F8606  call     0x2735e0  ; -> 002735E0 fn
003F860B  mov      rdx, rax
003F860E  mov      rcx, rbx
003F8611  call     0x247570  ; -> 00247570 fn
003F8616  mov      eax, dword ptr [rdi + 8]
003F8619  mov      dword ptr [rbx + 0xe0], eax
003F861F  mov      rbx, qword ptr [rsp + 0x48]
003F8624  xor      eax, eax
003F8626  mov      rsi, qword ptr [rsp + 0x50]
003F862B  add      rsp, 0x30
003F862F  pop      rdi
003F8630  ret      
```

## 004085B0 (140 B, extent 004085B0-0040863C)

Documented callee on this page: `00407450`

```
004085B0  mov      rax, qword ptr [rip + 0x275a7c9]  ; -> 02B62D80
004085B7  mov      edx, ecx
004085B9  test     rax, rax
004085BC  je       0x4085da  ; -> 004085DA
004085BE  mov      rcx, qword ptr [rax + 0xc0]
004085C5  test     rcx, rcx
004085C8  je       0x4085da  ; -> 004085DA
004085CA  xor      r8d, r8d
004085CD  cmp      byte ptr [rcx + 0xc0], r8b
004085D4  cmovne   rcx, r8
004085D8  jmp      0x4085e0  ; -> 004085E0
004085DA  xor      r8d, r8d
004085DD  mov      ecx, r8d
004085E0  test     rax, rax
004085E3  je       0x4085ee  ; -> 004085EE
004085E5  test     byte ptr [rax + 0xc8], 2
004085EC  jne      0x40863b  ; -> 0040863B
004085EE  test     rcx, rcx
004085F1  je       0x40863b  ; -> 0040863B
004085F3  mov      dword ptr [rcx + 0x118], r8d
004085FA  movzx    r8d, byte ptr [rcx + 0xc0]
00408602  mov      dword ptr [rcx + 0xe4], edx
00408608  test     r8d, r8d
0040860B  je       0x408636  ; -> 00408636
0040860D  sub      r8d, 1
00408611  je       0x408631  ; -> 00408631
00408613  cmp      r8d, 2
00408617  jne      0x40863b  ; -> 0040863B
00408619  mov      eax, dword ptr [rcx + 0xe0]
0040861F  cmp      edx, eax
00408621  jle      0x408625  ; -> 00408625
00408623  sub      edx, eax
00408625  mov      rcx, qword ptr [rcx + 0xd0]
0040862C  jmp      0x225580  ; -> 00225580 fn
00408631  jmp      0x407720  ; -> 00407720 fn
00408636  jmp      0x407450  ; -> 00407450 fn
0040863B  ret      
```

## 00408640 (177 B, extent 00408640-004086F1)

Documented callee on this page: `003937C0`

```
00408640  mov      qword ptr [rsp + 0x10], rbx
00408645  mov      qword ptr [rsp + 0x18], rbp
0040864A  push     rsi
0040864B  sub      rsp, 0x20
0040864F  mov      rax, qword ptr [rip + 0x275a72a]  ; -> 02B62D80
00408656  mov      rsi, rdx
00408659  mov      rbp, rcx
0040865C  test     rax, rax
0040865F  je       0x40867d  ; -> 0040867D
00408661  mov      rbx, qword ptr [rax + 0xc0]
00408668  test     rbx, rbx
0040866B  je       0x40867d  ; -> 0040867D
0040866D  xor      r8d, r8d
00408670  cmp      byte ptr [rbx + 0xc0], r8b
00408677  cmovne   rbx, r8
0040867B  jmp      0x408683  ; -> 00408683
0040867D  xor      r8d, r8d
00408680  mov      ebx, r8d
00408683  test     rax, rax
00408686  je       0x408691  ; -> 00408691
00408688  test     byte ptr [rax + 0xc8], 2
0040868F  jne      0x4086e1  ; -> 004086E1
00408691  test     rbx, rbx
00408694  je       0x4086e1  ; -> 004086E1
00408696  mov      rcx, qword ptr [rbx + 0xc8]
0040869D  test     rcx, rcx
004086A0  je       0x4086e1  ; -> 004086E1
004086A2  xor      edx, edx
004086A4  mov      qword ptr [rsp + 0x30], rdi
004086A9  call     0x394690  ; -> 00394690 fn
004086AE  mov      rdi, rax
004086B1  test     rax, rax
004086B4  je       0x4086dc  ; -> 004086DC
004086B6  add      rbx, 0x170
004086BD  mov      r8, rsi
004086C0  mov      rcx, rbx
004086C3  mov      edx, 0x80
004086C8  call     0x3937c0  ; -> 003937C0 fn
004086CD  mov      rcx, rbp
004086D0  mov      qword ptr [rdi + 0x18], rbx
004086D4  call     0x20e620  ; -> 0020E620 fn
004086D9  mov      dword ptr [rdi + 0x20], eax
004086DC  mov      rdi, qword ptr [rsp + 0x30]
004086E1  mov      rbx, qword ptr [rsp + 0x38]
004086E6  mov      rbp, qword ptr [rsp + 0x40]
004086EB  add      rsp, 0x20
004086EF  pop      rsi
004086F0  ret      
```

## 00408700 (116 B, extent 00408700-00408774)

Documented callee on this page: `003937C0`

```
00408700  mov      qword ptr [rsp + 8], rbx
00408705  push     rdi
00408706  sub      rsp, 0x20
0040870A  mov      rax, qword ptr [rip + 0x275a66f]  ; -> 02B62D80
00408711  mov      rdi, rcx
00408714  test     rax, rax
00408717  je       0x408735  ; -> 00408735
00408719  mov      rbx, qword ptr [rax + 0xc0]
00408720  test     rbx, rbx
00408723  je       0x408735  ; -> 00408735
00408725  xor      r8d, r8d
00408728  cmp      byte ptr [rbx + 0xc0], r8b
0040872F  cmovne   rbx, r8
00408733  jmp      0x40873b  ; -> 0040873B
00408735  xor      r8d, r8d
00408738  mov      ebx, r8d
0040873B  test     rax, rax
0040873E  je       0x408749  ; -> 00408749
00408740  test     byte ptr [rax + 0xc8], 2
00408747  jne      0x408769  ; -> 00408769
00408749  test     rbx, rbx
0040874C  je       0x408769  ; -> 00408769
0040874E  mov      r8, rdx
00408751  lea      rcx, [rbx + 0x1f0]
00408758  mov      edx, 0x80
0040875D  call     0x3937c0  ; -> 003937C0 fn
00408762  mov      qword ptr [rbx + 0x270], rdi
00408769  mov      rbx, qword ptr [rsp + 0x30]
0040876E  add      rsp, 0x20
00408772  pop      rdi
00408773  ret      
```

## 004088D0 (141 B, extent 004088D0-0040895D)

Documented callee on this page: `00407450`

```
004088D0  mov      rax, qword ptr [rip + 0x275a4a9]  ; -> 02B62D80
004088D7  mov      r8d, ecx
004088DA  test     rax, rax
004088DD  je       0x4088fa  ; -> 004088FA
004088DF  mov      rcx, qword ptr [rax + 0xc0]
004088E6  test     rcx, rcx
004088E9  je       0x4088fa  ; -> 004088FA
004088EB  xor      edx, edx
004088ED  cmp      byte ptr [rcx + 0xc0], 1
004088F4  cmovne   rcx, rdx
004088F8  jmp      0x4088fe  ; -> 004088FE
004088FA  xor      edx, edx
004088FC  mov      ecx, edx
004088FE  test     rax, rax
00408901  je       0x40890c  ; -> 0040890C
00408903  test     byte ptr [rax + 0xc8], 2
0040890A  jne      0x40895c  ; -> 0040895C
0040890C  test     rcx, rcx
0040890F  je       0x40895c  ; -> 0040895C
00408911  mov      dword ptr [rcx + 0x118], edx
00408917  imul     edx, r8d, 0x3c
0040891B  movzx    r8d, byte ptr [rcx + 0xc0]
00408923  mov      dword ptr [rcx + 0xe4], edx
00408929  test     r8d, r8d
0040892C  je       0x408957  ; -> 00408957
0040892E  sub      r8d, 1
00408932  je       0x408952  ; -> 00408952
00408934  cmp      r8d, 2
00408938  jne      0x40895c  ; -> 0040895C
0040893A  mov      eax, dword ptr [rcx + 0xe0]
00408940  cmp      edx, eax
00408942  jle      0x408946  ; -> 00408946
00408944  sub      edx, eax
00408946  mov      rcx, qword ptr [rcx + 0xd0]
0040894D  jmp      0x225580  ; -> 00225580 fn
00408952  jmp      0x407720  ; -> 00407720 fn
00408957  jmp      0x407450  ; -> 00407450 fn
0040895C  ret      
```

## 00408960 (177 B, extent 00408960-00408A11)

Documented callee on this page: `003937C0`

```
00408960  mov      qword ptr [rsp + 0x10], rbx
00408965  mov      qword ptr [rsp + 0x18], rbp
0040896A  push     rsi
0040896B  sub      rsp, 0x20
0040896F  mov      rax, qword ptr [rip + 0x275a40a]  ; -> 02B62D80
00408976  mov      rsi, rdx
00408979  mov      rbp, rcx
0040897C  test     rax, rax
0040897F  je       0x40899d  ; -> 0040899D
00408981  mov      rbx, qword ptr [rax + 0xc0]
00408988  test     rbx, rbx
0040898B  je       0x40899d  ; -> 0040899D
0040898D  xor      r8d, r8d
00408990  cmp      byte ptr [rbx + 0xc0], 1
00408997  cmovne   rbx, r8
0040899B  jmp      0x4089a3  ; -> 004089A3
0040899D  xor      r8d, r8d
004089A0  mov      ebx, r8d
004089A3  test     rax, rax
004089A6  je       0x4089b1  ; -> 004089B1
004089A8  test     byte ptr [rax + 0xc8], 2
004089AF  jne      0x408a01  ; -> 00408A01
004089B1  test     rbx, rbx
004089B4  je       0x408a01  ; -> 00408A01
004089B6  mov      rcx, qword ptr [rbx + 0xc8]
004089BD  test     rcx, rcx
004089C0  je       0x408a01  ; -> 00408A01
004089C2  xor      edx, edx
004089C4  mov      qword ptr [rsp + 0x30], rdi
004089C9  call     0x394690  ; -> 00394690 fn
004089CE  mov      rdi, rax
004089D1  test     rax, rax
004089D4  je       0x4089fc  ; -> 004089FC
004089D6  add      rbx, 0x174
004089DD  mov      r8, rsi
004089E0  mov      rcx, rbx
004089E3  mov      edx, 0x80
004089E8  call     0x3937c0  ; -> 003937C0 fn
004089ED  mov      rcx, rbp
004089F0  mov      qword ptr [rdi + 0x18], rbx
004089F4  call     0x20e620  ; -> 0020E620 fn
004089F9  mov      dword ptr [rdi + 0x20], eax
004089FC  mov      rdi, qword ptr [rsp + 0x30]
00408A01  mov      rbx, qword ptr [rsp + 0x38]
00408A06  mov      rbp, qword ptr [rsp + 0x40]
00408A0B  add      rsp, 0x20
00408A0F  pop      rsi
00408A10  ret      
```

## 00578310 (310 B, extent 00578310-00578446)

Documented callee on this page: `002B39A0`

```
00578310  mov      qword ptr [rsp + 8], rbx
00578315  mov      qword ptr [rsp + 0x10], rbp
0057831A  mov      qword ptr [rsp + 0x18], rsi
0057831F  mov      qword ptr [rsp + 0x20], rdi
00578324  push     r14
00578326  sub      rsp, 0x20
0057832A  movzx    r8d, byte ptr [rcx + 0xf8]
00578332  xor      ebx, ebx
00578334  movsxd   rdi, r9d
00578337  mov      rbp, rdx
0057833A  mov      rsi, rcx
0057833D  lea      r14d, [rbx + 1]
00578341  test     r8d, r8d
00578344  jne      0x5783bf  ; -> 005783BF
00578346  movzx    r8d, byte ptr [rcx + 0xf4]
0057834E  mov      r9d, ebx
00578351  mov      edx, ebx
00578353  mov      ecx, ebx
00578355  test     r8, r8
00578358  je       0x578376  ; -> 00578376
0057835A  nop      word ptr [rax + rax]
00578360  movzx    eax, byte ptr [rsi + rcx + 0xe8]
00578368  cmp      edi, eax
0057836A  je       0x578376  ; -> 00578376
0057836C  inc      edx
0057836E  inc      rcx
00578371  cmp      rcx, r8
00578374  jl       0x578360  ; -> 00578360
00578376  cmp      edx, r8d
00578379  jge      0x57839e  ; -> 0057839E
0057837B  lea      eax, [r8 - 1]
0057837F  cmp      edx, eax
00578381  jne      0x578398  ; -> 00578398
00578383  mov      rax, qword ptr [rsi + 0xd0]
0057838A  movzx    ecx, word ptr [rax]
0057838D  call     0x46b1a0  ; -> 0046B1A0 fn
00578392  test     eax, eax
00578394  cmove    ebx, r14d
00578398  mov      r9d, ebx
0057839B  xor      r9d, r14d
0057839E  mov      rax, qword ptr [rbp + 0x10]
005783A2  mov      rcx, qword ptr [rax + 0x10]
005783A6  and      dword ptr [rcx + 8], 0xfffffffe
005783AA  or       dword ptr [rcx + 8], ebx
005783AD  mov      rbx, r14
005783B0  mov      rax, qword ptr [rbp + 0x10]
005783B4  mov      rcx, qword ptr [rax]
005783B7  and      dword ptr [rcx + 8], 0xfffffffe
005783BB  or       dword ptr [rcx + 8], r9d
005783BF  mov      rdi, qword ptr [rsi + rdi*8 + 0x100]
005783C7  mov      dl, 2
005783C9  mov      rax, qword ptr [rbp + 0x10]
005783CD  mov      rcx, rdi
005783D0  mov      rsi, qword ptr [rsi + 0xe0]
005783D7  mov      rbp, qword ptr [rax + rbx*8]
005783DB  call     0x2b39a0  ; -> 002B39A0 fn
005783E0  mov      rbx, rax
005783E3  test     rax, rax
005783E6  je       0x578414  ; -> 00578414
005783E8  sub      ebx, edi
005783EA  cmp      ebx, 0x80
005783F0  jb       0x5783f9  ; -> 005783F9
005783F2  mov      ebx, 0x7f
005783F7  jmp      0x5783fd  ; -> 005783FD
005783F9  test     ebx, ebx
005783FB  je       0x57840b  ; -> 0057840B
005783FD  mov      r8d, ebx
00578400  mov      rdx, rdi
00578403  mov      rcx, rsi
00578406  call     0x861eba  ; -> 00861EBA fn
0057840B  mov      ecx, ebx
0057840D  mov      rdi, rsi
00578410  mov      byte ptr [rcx + rsi], 0
00578414  call     0x37eb70  ; -> 0037EB70 fn
00578419  mov      rcx, rax
0057841C  mov      qword ptr [rbp + 0x18], rdi
00578420  call     0x20e620  ; -> 0020E620 fn
00578425  mov      rbx, qword ptr [rsp + 0x30]
0057842A  mov      rsi, qword ptr [rsp + 0x40]
0057842F  mov      rdi, qword ptr [rsp + 0x48]
00578434  mov      dword ptr [rbp + 0x20], eax
00578437  mov      eax, r14d
0057843A  mov      rbp, qword ptr [rsp + 0x38]
0057843F  add      rsp, 0x20
00578443  pop      r14
00578445  ret      
```

## 0057C3E0 (151 B, extent 0057C3E0-0057C477)

Documented callee on this page: `002D8910`

```
0057C3E0  mov      qword ptr [rsp + 0x10], rbx
0057C3E5  push     rdi
0057C3E6  sub      rsp, 0x30
0057C3EA  cmp      byte ptr [rcx + 0x636], 0
0057C3F1  mov      rdi, rdx
0057C3F4  mov      rbx, rcx
0057C3F7  je       0x57c46c  ; -> 0057C46C
0057C3F9  mov      qword ptr [rsp + 0x40], rsi
0057C3FE  movsxd   rsi, r8d
0057C401  mov      rcx, rsi
0057C404  add      rcx, rcx
0057C407  movzx    eax, word ptr [rbx + rcx*8 + 0x5b8]
0057C40F  cmp      word ptr [rbx + 0x638], ax
0057C416  jne      0x57c41f  ; -> 0057C41F
0057C418  mov      ecx, 6
0057C41D  jmp      0x57c42e  ; -> 0057C42E
0057C41F  test     byte ptr [rbx + rcx*8 + 0x5bc], 1
0057C427  jne      0x57c439  ; -> 0057C439
0057C429  mov      ecx, 2
0057C42E  call     0x2dd7e0  ; -> 002DD7E0 fn
0057C433  mov      dword ptr [rdi + 0x90], eax
0057C439  lea      r9, [rsi + 0x5b]
0057C43D  mov      qword ptr [rsp + 0x20], 0
0057C446  add      r9, r9
0057C449  xor      r8d, r8d
0057C44C  xor      edx, edx
0057C44E  mov      rcx, rdi
0057C451  mov      r9, qword ptr [rbx + r9*8]
0057C455  call     0x2d8910  ; -> 002D8910 fn
0057C45A  xor      ecx, ecx
0057C45C  call     0x2dd7e0  ; -> 002DD7E0 fn
0057C461  mov      rsi, qword ptr [rsp + 0x40]
0057C466  mov      dword ptr [rdi + 0x90], eax
0057C46C  mov      rbx, qword ptr [rsp + 0x48]
0057C471  add      rsp, 0x30
0057C475  pop      rdi
0057C476  ret      
```
