# F homing pack (FABLE): `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 14. No bearing page cites them and no documented function calls them directly.

## 002E3E90 (108 B, extent 002E3E90-002E3EFC)

Documented callee on this page: `002EAEB0`

```
002E3E90  mov      rax, qword ptr [rip + 0x1e7bec1]  ; -> 0215FD58
002E3E97  test     rax, rax
002E3E9A  je       0x2e3eae  ; -> 002E3EAE
002E3E9C  nop      dword ptr [rax]
002E3EA0  cmp      dword ptr [rax + 0x14], ecx
002E3EA3  je       0x2e3ecf  ; -> 002E3ECF
002E3EA5  mov      rax, qword ptr [rax + 8]
002E3EA9  test     rax, rax
002E3EAC  jne      0x2e3ea0  ; -> 002E3EA0
002E3EAE  mov      rax, qword ptr [rip + 0x1e7bec3]  ; -> 0215FD78
002E3EB5  test     rax, rax
002E3EB8  je       0x2e3efb  ; -> 002E3EFB
002E3EBA  nop      word ptr [rax + rax]
002E3EC0  cmp      dword ptr [rax + 0x14], ecx
002E3EC3  je       0x2e3ecf  ; -> 002E3ECF
002E3EC5  mov      rax, qword ptr [rax + 8]
002E3EC9  test     rax, rax
002E3ECC  jne      0x2e3ec0  ; -> 002E3EC0
002E3ECE  ret      
002E3ECF  test     rax, rax
002E3ED2  je       0x2e3efb  ; -> 002E3EFB
002E3ED4  movzx    edx, byte ptr [rax + 0x19]
002E3ED8  mov      ecx, edx
002E3EDA  shr      ecx, 4
002E3EDD  and      ecx, 1
002E3EE0  jne      0x2e3efb  ; -> 002E3EFB
002E3EE2  cmp      word ptr [rax + 0x1c], cx
002E3EE6  jg       0x2e3efb  ; -> 002E3EFB
002E3EE8  test     dl, 3
002E3EEB  jne      0x2e3ef5  ; -> 002E3EF5
002E3EED  mov      rcx, rax
002E3EF0  jmp      0x2eaeb0  ; -> 002EAEB0 fn
002E3EF5  xor      ecx, ecx
002E3EF7  mov      word ptr [rax + 0x1c], cx
002E3EFB  ret      
```

## 00344550 (98 B, extent 00344550-003445B2)

Documented callee on this page: `002E3110`

```
00344550  mov      qword ptr [rsp + 8], rbx
00344555  push     rdi
00344556  sub      rsp, 0x30
0034455A  cmp      byte ptr [r8 + 8], 0
0034455F  mov      rbx, r8
00344562  mov      rdi, rdx
00344565  je       0x3445a7  ; -> 003445A7
00344567  cmp      dword ptr [r8], 0
0034456B  jl       0x3445a7  ; -> 003445A7
0034456D  movsx    edx, byte ptr [r8 + 9]
00344572  mov      rcx, rdi
00344575  add      edx, 4
00344578  mov      r8d, 1
0034457E  call     0x2ebc90  ; -> 002EBC90 fn
00344583  mov      ecx, dword ptr [rbx + 4]
00344586  call     0x2e97c0  ; -> 002E97C0 fn
0034458B  movsx    r8d, byte ptr [rbx + 9]
00344590  mov      r9, rax
00344593  mov      eax, dword ptr [rbx + 0xc]
00344596  mov      edx, 3
0034459B  mov      rcx, rdi
0034459E  mov      dword ptr [rsp + 0x20], eax
003445A2  call     0x2e3110  ; -> 002E3110 fn
003445A7  mov      rbx, qword ptr [rsp + 0x40]
003445AC  add      rsp, 0x30
003445B0  pop      rdi
003445B1  ret      
```

## 00345A60 (91 B, extent 00345A60-00345ABB)

Documented callee on this page: `002E3110`

```
00345A60  mov      qword ptr [rsp + 8], rbx
00345A65  push     rdi
00345A66  sub      rsp, 0x30
00345A6A  cmp      byte ptr [r8 + 8], 0
00345A6F  mov      rbx, r8
00345A72  mov      rdi, rdx
00345A75  je       0x345ab0  ; -> 00345AB0
00345A77  cmp      dword ptr [r8], 0
00345A7B  jl       0x345ab0  ; -> 00345AB0
00345A7D  mov      edx, 3
00345A82  mov      rcx, rdi
00345A85  lea      r8d, [rdx - 2]
00345A89  call     0x2ebc90  ; -> 002EBC90 fn
00345A8E  mov      ecx, dword ptr [rbx + 4]
00345A91  call     0x2e97c0  ; -> 002E97C0 fn
00345A96  xor      r8d, r8d
00345A99  mov      dword ptr [rsp + 0x20], 0
00345AA1  mov      r9, rax
00345AA4  mov      rcx, rdi
00345AA7  lea      edx, [r8 + 2]
00345AAB  call     0x2e3110  ; -> 002E3110 fn
00345AB0  mov      rbx, qword ptr [rsp + 0x40]
00345AB5  add      rsp, 0x30
00345AB9  pop      rdi
00345ABA  ret      
```

## 00345F60 (69 B, extent 00345F60-00345FA5)

Documented callee on this page: `002EA6A0`

```
00345F60  mov      qword ptr [rsp + 8], rbx
00345F65  push     rdi
00345F66  sub      rsp, 0x20
00345F6A  mov      rcx, r9
00345F6D  mov      rdi, r8
00345F70  call     0x267e10  ; -> 00267E10 fn
00345F75  mov      edx, 1
00345F7A  mov      ecx, eax
00345F7C  mov      r8d, edx
00345F7F  call     0x359ca0  ; -> 00359CA0 fn
00345F84  mov      rcx, rax
00345F87  mov      rbx, rax
00345F8A  call     0x2ea6a0  ; -> 002EA6A0 fn
00345F8F  xor      ecx, ecx
00345F91  test     eax, eax
00345F93  cmove    rbx, rcx
00345F97  mov      qword ptr [rdi], rbx
00345F9A  mov      rbx, qword ptr [rsp + 0x30]
00345F9F  add      rsp, 0x20
00345FA3  pop      rdi
00345FA4  ret      
```

## 003463F0 (97 B, extent 003463F0-00346451)

Documented callee on this page: `002E97C0`

```
003463F0  push     rbp
003463F2  sub      rsp, 0x30
003463F6  cmp      byte ptr [r8 + 5], 0
003463FB  mov      rbp, r8
003463FE  je       0x34644b  ; -> 0034644B
00346400  mov      ecx, dword ptr [r8 + 8]
00346404  mov      qword ptr [rsp + 0x40], rbx
00346409  movsx    ebx, word ptr [r8 + 2]
0034640E  mov      qword ptr [rsp + 0x48], rsi
00346413  movsx    esi, byte ptr [r8 + 4]
00346418  mov      qword ptr [rsp + 0x50], rdi
0034641D  movsx    edi, word ptr [r8]
00346421  call     0x2e97c0  ; -> 002E97C0 fn
00346426  movsx    ecx, byte ptr [rbp + 6]
0034642A  mov      rdx, rax
0034642D  mov      r9d, edi
00346430  mov      dword ptr [rsp + 0x20], ebx
00346434  mov      r8d, esi
00346437  call     0x3eb190  ; -> 003EB190 fn
0034643C  mov      rdi, qword ptr [rsp + 0x50]
00346441  mov      rsi, qword ptr [rsp + 0x48]
00346446  mov      rbx, qword ptr [rsp + 0x40]
0034644B  add      rsp, 0x30
0034644F  pop      rbp
00346450  ret      
```

## 00354990 (57 B, extent 00354990-003549C9)

Documented callee on this page: `002EBD60`

```
00354990  mov      qword ptr [rsp + 8], rbx
00354995  push     rdi
00354996  sub      rsp, 0x20
0035499A  mov      rcx, r9
0035499D  mov      rdi, r9
003549A0  call     0x267e10  ; -> 00267E10 fn
003549A5  mov      rcx, rdi
003549A8  mov      ebx, eax
003549AA  call     0x267e10  ; -> 00267E10 fn
003549AF  mov      ecx, eax
003549B1  call     0x2e9a60  ; -> 002E9A60 fn
003549B6  mov      edx, ebx
003549B8  mov      ecx, eax
003549BA  mov      rbx, qword ptr [rsp + 0x30]
003549BF  add      rsp, 0x20
003549C3  pop      rdi
003549C4  jmp      0x2ebd60  ; -> 002EBD60 fn
```

## 00354A40 (140 B, extent 00354A40-00354ACC)

Documented callee on this page: `002E97C0`

```
00354A40  mov      qword ptr [rsp + 8], rbx
00354A45  mov      qword ptr [rsp + 0x10], rsi
00354A4A  push     rdi
00354A4B  sub      rsp, 0x20
00354A4F  mov      ecx, dword ptr [r8]
00354A52  mov      rdi, r8
00354A55  mov      rsi, rdx
00354A58  mov      ebx, 1
00354A5D  test     ecx, ecx
00354A5F  je       0x354ab8  ; -> 00354AB8
00354A61  call     0x2e97c0  ; -> 002E97C0 fn
00354A66  test     rax, rax
00354A69  jne      0x354a93  ; -> 00354A93
00354A6B  movzx    edx, byte ptr [rsi + 0x15]
00354A6F  mov      ecx, dword ptr [rdi + 4]
00354A72  call     0x2eae20  ; -> 002EAE20 fn
00354A77  mov      rcx, rax
00354A7A  call     0x2e9810  ; -> 002E9810 fn
00354A7F  mov      dword ptr [rdi], eax
00354A81  mov      eax, ebx
00354A83  mov      rbx, qword ptr [rsp + 0x30]
00354A88  mov      rsi, qword ptr [rsp + 0x38]
00354A8D  add      rsp, 0x20
00354A91  pop      rdi
00354A92  ret      
00354A93  mov      rcx, rax
00354A96  call     0x2e4c20  ; -> 002E4C20 fn
00354A9B  test     eax, eax
00354A9D  jne      0x354ab8  ; -> 00354AB8
00354A9F  mov      ecx, ebx
00354AA1  call     0x314d40  ; -> 00314D40 fn
00354AA6  mov      eax, ebx
00354AA8  mov      rbx, qword ptr [rsp + 0x30]
00354AAD  mov      rsi, qword ptr [rsp + 0x38]
00354AB2  add      rsp, 0x20
00354AB6  pop      rdi
00354AB7  ret      
00354AB8  mov      rsi, qword ptr [rsp + 0x38]
00354ABD  xor      ebx, ebx
00354ABF  mov      eax, ebx
00354AC1  mov      rbx, qword ptr [rsp + 0x30]
00354AC6  add      rsp, 0x20
00354ACA  pop      rdi
00354ACB  ret      
```

## 003EB200 (79 B, extent 003EB200-003EB24F)

Documented callee on this page: `002EAE20`

```
003EB200  mov      qword ptr [rsp + 8], rbx
003EB205  mov      qword ptr [rsp + 0x10], rsi
003EB20A  push     rdi
003EB20B  sub      rsp, 0x30
003EB20F  mov      eax, edx
003EB211  mov      esi, ecx
003EB213  mov      ecx, eax
003EB215  xor      edx, edx
003EB217  mov      ebx, r9d
003EB21A  mov      edi, r8d
003EB21D  call     0x2eae20  ; -> 002EAE20 fn
003EB222  test     rax, rax
003EB225  je       0x3eb23f  ; -> 003EB23F
003EB227  mov      edx, dword ptr [rsp + 0x60]
003EB22B  mov      r9d, ebx
003EB22E  mov      dword ptr [rsp + 0x20], edx
003EB232  mov      r8d, edi
003EB235  mov      rdx, rax
003EB238  mov      ecx, esi
003EB23A  call     0x3eb190  ; -> 003EB190 fn
003EB23F  mov      rbx, qword ptr [rsp + 0x40]
003EB244  mov      rsi, qword ptr [rsp + 0x48]
003EB249  add      rsp, 0x30
003EB24D  pop      rdi
003EB24E  ret      
```

## 0050CB00 (48 B, extent 0050CB00-0050CB30)

Documented callee on this page: `002E4C20`

```
0050CB00  sub      rsp, 0x28
0050CB04  cmp      dword ptr [r8], 0
0050CB08  jl       0x50cb29  ; -> 0050CB29
0050CB0A  mov      rcx, qword ptr [r8 + 8]
0050CB0E  call     0x2e4c20  ; -> 002E4C20 fn
0050CB13  test     eax, eax
0050CB15  jne      0x50cb29  ; -> 0050CB29
0050CB17  lea      ecx, [rax + 1]
0050CB1A  call     0x314d40  ; -> 00314D40 fn
0050CB1F  mov      eax, 1
0050CB24  add      rsp, 0x28
0050CB28  ret      
0050CB29  xor      eax, eax
0050CB2B  add      rsp, 0x28
0050CB2F  ret      
```

## 0050CE70 (77 B, extent 0050CE70-0050CEBD)

Documented callee on this page: `002E9C00`

```
0050CE70  mov      qword ptr [rsp + 8], rbx
0050CE75  mov      qword ptr [rsp + 0x10], rsi
0050CE7A  push     rdi
0050CE7B  sub      rsp, 0x20
0050CE7F  mov      rsi, rcx
0050CE82  mov      rdi, rdx
0050CE85  mov      rcx, r9
0050CE88  call     0x267e10  ; -> 00267E10 fn
0050CE8D  mov      rcx, rdi
0050CE90  mov      ebx, eax
0050CE92  call     0x2e9c00  ; -> 002E9C00 fn
0050CE97  mov      r8d, eax
0050CE9A  mov      edx, ebx
0050CE9C  mov      rcx, rdi
0050CE9F  call     0x3dccf0  ; -> 003DCCF0 fn
0050CEA4  mov      edx, eax
0050CEA6  mov      rcx, rsi
0050CEA9  mov      rbx, qword ptr [rsp + 0x30]
0050CEAE  mov      rsi, qword ptr [rsp + 0x38]
0050CEB3  add      rsp, 0x20
0050CEB7  pop      rdi
0050CEB8  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0050D710 (109 B, extent 0050D710-0050D77D)

Documented callee on this page: `002E4C30`

```
0050D710  mov      qword ptr [rsp + 8], rbx
0050D715  push     rdi
0050D716  sub      rsp, 0x20
0050D71A  mov      rcx, rdx
0050D71D  mov      rbx, r8
0050D720  mov      rdi, rdx
0050D723  call     0x2e97b0  ; -> 002E97B0 fn
0050D728  mov      rbx, qword ptr [rbx + 8]
0050D72C  mov      rcx, rbx
0050D72F  call     0x2e4c20  ; -> 002E4C20 fn
0050D734  test     eax, eax
0050D736  je       0x50d763  ; -> 0050D763
0050D738  mov      rcx, rdi
0050D73B  call     0x2e9c00  ; -> 002E9C00 fn
0050D740  mov      edx, eax
0050D742  mov      rcx, rbx
0050D745  call     0x2e4c30  ; -> 002E4C30 fn
0050D74A  test     eax, eax
0050D74C  je       0x50d763  ; -> 0050D763
0050D74E  mov      rcx, rdi
0050D751  call     0x2eac90  ; -> 002EAC90 fn
0050D756  xor      eax, eax
0050D758  mov      rbx, qword ptr [rsp + 0x30]
0050D75D  add      rsp, 0x20
0050D761  pop      rdi
0050D762  ret      
0050D763  mov      ecx, 1
0050D768  call     0x314d40  ; -> 00314D40 fn
0050D76D  mov      rbx, qword ptr [rsp + 0x30]
0050D772  mov      eax, 1
0050D777  add      rsp, 0x20
0050D77B  pop      rdi
0050D77C  ret      
```

## 0050D860 (133 B, extent 0050D860-0050D8E5)

Documented callee on this page: `002EA6A0`

```
0050D860  mov      qword ptr [rsp + 8], rbx
0050D865  mov      qword ptr [rsp + 0x10], rsi
0050D86A  push     rdi
0050D86B  sub      rsp, 0x20
0050D86F  mov      rbx, r9
0050D872  mov      rdi, rdx
0050D875  call     0x2640c0  ; -> 002640C0 fn
0050D87A  mov      rcx, rbx
0050D87D  mov      rsi, rax
0050D880  call     0x267e10  ; -> 00267E10 fn
0050D885  test     eax, eax
0050D887  jns      0x50d88c  ; -> 0050D88C
0050D889  movzx    eax, word ptr [rdi]
0050D88C  mov      edx, eax
0050D88E  mov      rcx, rsi
0050D891  call     0x358940  ; -> 00358940 fn
0050D896  mov      rbx, rax
0050D899  test     rax, rax
0050D89C  je       0x50d8d5  ; -> 0050D8D5
0050D89E  movzx    ecx, byte ptr [rax + 3]
0050D8A2  and      cl, 0xe0
0050D8A5  cmp      cl, 0x60
0050D8A8  jne      0x50d8d5  ; -> 0050D8D5
0050D8AA  mov      rcx, rax
0050D8AD  call     0x2ea6a0  ; -> 002EA6A0 fn
0050D8B2  test     eax, eax
0050D8B4  je       0x50d8d5  ; -> 0050D8D5
0050D8B6  mov      rax, qword ptr [rbx + 0xc0]
0050D8BD  test     rax, rax
0050D8C0  je       0x50d8d5  ; -> 0050D8D5
0050D8C2  movsx    edx, byte ptr [rax + 0x14c]
0050D8C9  lea      rcx, [rip + 0x81513c]  ; -> 00D22A0C
0050D8D0  call     0x17d280  ; -> 0017D280 fn
0050D8D5  mov      rbx, qword ptr [rsp + 0x30]
0050D8DA  mov      rsi, qword ptr [rsp + 0x38]
0050D8DF  add      rsp, 0x20
0050D8E3  pop      rdi
0050D8E4  ret      
```

## 0050DB80 (80 B, extent 0050DB80-0050DBD0)

Documented callee on this page: `002EA6A0`

```
0050DB80  mov      qword ptr [rsp + 8], rbx
0050DB85  mov      qword ptr [rsp + 0x10], rsi
0050DB8A  push     rdi
0050DB8B  sub      rsp, 0x20
0050DB8F  mov      rdi, r9
0050DB92  mov      rsi, rcx
0050DB95  call     0x2640c0  ; -> 002640C0 fn
0050DB9A  mov      rcx, rdi
0050DB9D  mov      rbx, rax
0050DBA0  call     0x267e10  ; -> 00267E10 fn
0050DBA5  mov      edx, eax
0050DBA7  mov      rcx, rbx
0050DBAA  call     0x358940  ; -> 00358940 fn
0050DBAF  mov      rcx, rax
0050DBB2  call     0x2ea6a0  ; -> 002EA6A0 fn
0050DBB7  mov      edx, eax
0050DBB9  mov      rcx, rsi
0050DBBC  mov      rbx, qword ptr [rsp + 0x30]
0050DBC1  mov      rsi, qword ptr [rsp + 0x38]
0050DBC6  add      rsp, 0x20
0050DBCA  pop      rdi
0050DBCB  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0050E150 (135 B, extent 0050E150-0050E1D7)

Documented callee on this page: `002EAE20`

```
0050E150  mov      qword ptr [rsp + 8], rbx
0050E155  mov      qword ptr [rsp + 0x10], rbp
0050E15A  mov      qword ptr [rsp + 0x18], rsi
0050E15F  mov      qword ptr [rsp + 0x20], rdi
0050E164  push     r14
0050E166  sub      rsp, 0x20
0050E16A  mov      rcx, r9
0050E16D  mov      rbx, r9
0050E170  mov      r14, r8
0050E173  mov      rbp, rdx
0050E176  call     0x267e10  ; -> 00267E10 fn
0050E17B  mov      rcx, rbx
0050E17E  mov      esi, eax
0050E180  call     0x267e10  ; -> 00267E10 fn
0050E185  mov      rcx, rbx
0050E188  mov      edi, eax
0050E18A  call     0x267e10  ; -> 00267E10 fn
0050E18F  mov      ecx, eax
0050E191  call     0x2e9a60  ; -> 002E9A60 fn
0050E196  mov      edx, eax
0050E198  lea      rcx, [rip + 0x814871]  ; -> 00D22A10
0050E19F  mov      ebx, eax
0050E1A1  call     0x17d280  ; -> 0017D280 fn
0050E1A6  mov      dword ptr [r14 + 4], esi
0050E1AA  mov      ecx, ebx
0050E1AC  mov      dword ptr [r14], edi
0050E1AF  movzx    edx, byte ptr [rbp + 0x15]
0050E1B3  call     0x2eae20  ; -> 002EAE20 fn
0050E1B8  mov      rbx, qword ptr [rsp + 0x30]
0050E1BD  mov      rbp, qword ptr [rsp + 0x38]
0050E1C2  mov      rsi, qword ptr [rsp + 0x40]
0050E1C7  mov      rdi, qword ptr [rsp + 0x48]
0050E1CC  mov      qword ptr [r14 + 8], rax
0050E1D0  add      rsp, 0x20
0050E1D4  pop      r14
0050E1D6  ret      
```
