# F homing pack (FABLE): `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 20. No bearing page cites them and no documented function calls them directly.

## 002697A0 (50 B, extent 002697A0-002697D2)

Documented callee on this page: `003DB420`

```
002697A0  push     rbx
002697A2  sub      rsp, 0x20
002697A6  mov      edx, 1
002697AB  mov      rbx, rcx
002697AE  lea      r8d, [rdx + 2]
002697B2  call     0x3db420  ; -> 003DB420 fn
002697B7  xor      edx, edx
002697B9  mov      rcx, rbx
002697BC  lea      r8d, [rdx + 3]
002697C0  call     0x3db420  ; -> 003DB420 fn
002697C5  mov      rcx, rbx
002697C8  add      rsp, 0x20
002697CC  pop      rbx
002697CD  jmp      0x269640  ; -> 00269640 fn
```

## 0033F190 (32 B, extent 0033F190-0033F1B0)

Documented callee on this page: `0026C120`

```
0033F190  push     rbx
0033F192  sub      rsp, 0x20
0033F196  mov      rbx, rdx
0033F199  call     0x357980  ; -> 00357980 fn
0033F19E  mov      edx, 2
0033F1A3  mov      rcx, rbx
0033F1A6  add      rsp, 0x20
0033F1AA  pop      rbx
0033F1AB  jmp      0x26c120  ; -> 0026C120 fn
```

## 0033FF00 (62 B, extent 0033FF00-0033FF3E)

Documented callee on this page: `0026B4E0`

```
0033FF00  push     rbx
0033FF02  sub      rsp, 0x20
0033FF06  mov      rbx, rcx
0033FF09  mov      rcx, r9
0033FF0C  call     0x267e10  ; -> 00267E10 fn
0033FF11  mov      edx, 1
0033FF16  mov      ecx, eax
0033FF18  mov      r8d, edx
0033FF1B  call     0x359ca0  ; -> 00359CA0 fn
0033FF20  mov      rcx, rax
0033FF23  xor      eax, eax
0033FF25  test     rcx, rcx
0033FF28  je       0x33ff2f  ; -> 0033FF2F
0033FF2A  call     0x233dc0  ; -> 00233DC0 fn
0033FF2F  mov      edx, eax
0033FF31  mov      rcx, rbx
0033FF34  add      rsp, 0x20
0033FF38  pop      rbx
0033FF39  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 003400E0 (196 B, extent 003400E0-003401A4)

Documented callee on this page: `002640C0`

```
003400E0  mov      qword ptr [rsp + 8], rbx
003400E5  mov      qword ptr [rsp + 0x10], rbp
003400EA  push     rsi
003400EB  push     rdi
003400EC  push     r14
003400EE  sub      rsp, 0x50
003400F2  mov      rax, qword ptr [rip + 0x1c04737]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003400F9  xor      rax, rsp
003400FC  mov      qword ptr [rsp + 0x40], rax
00340101  mov      rbx, r9
00340104  call     0x2640c0  ; -> 002640C0 fn
00340109  mov      rcx, rbx
0034010C  mov      r14, rax
0034010F  call     0x267e10  ; -> 00267E10 fn
00340114  mov      rcx, rbx
00340117  mov      dword ptr [rsp + 0x3c], eax
0034011B  call     0x267e10  ; -> 00267E10 fn
00340120  mov      rcx, rbx
00340123  mov      dword ptr [rsp + 0x38], eax
00340127  call     0x267e10  ; -> 00267E10 fn
0034012C  mov      rcx, rbx
0034012F  mov      dword ptr [rsp + 0x34], eax
00340133  call     0x267e10  ; -> 00267E10 fn
00340138  mov      rcx, rbx
0034013B  mov      dword ptr [rsp + 0x30], eax
0034013F  call     0x267e10  ; -> 00267E10 fn
00340144  mov      rcx, rbx
00340147  mov      ebp, eax
00340149  call     0x267e10  ; -> 00267E10 fn
0034014E  mov      rcx, rbx
00340151  mov      esi, eax
00340153  call     0x267e10  ; -> 00267E10 fn
00340158  mov      rcx, rbx
0034015B  mov      edi, eax
0034015D  call     0x267e10  ; -> 00267E10 fn
00340162  lea      rdx, [rsp + 0x30]
00340167  mov      ecx, eax
00340169  mov      ebx, eax
0034016B  call     0x3e9440  ; -> 003E9440 fn
00340170  mov      r9d, esi
00340173  mov      dword ptr [rsp + 0x20], ebp
00340177  mov      r8d, edi
0034017A  mov      edx, ebx
0034017C  mov      rcx, r14
0034017F  call     0x3e9320  ; -> 003E9320 fn
00340184  mov      rcx, qword ptr [rsp + 0x40]
00340189  xor      rcx, rsp
0034018C  call     0x808c40  ; -> 00808C40 fn
00340191  mov      rbx, qword ptr [rsp + 0x70]
00340196  mov      rbp, qword ptr [rsp + 0x78]
0034019B  add      rsp, 0x50
0034019F  pop      r14
003401A1  pop      rdi
003401A2  pop      rsi
003401A3  ret      
```

## 00340340 (61 B, extent 00340340-0034037D)

Documented callee on this page: `0026B4E0`

```
00340340  push     rbx
00340342  sub      rsp, 0x20
00340346  mov      rbx, rcx
00340349  mov      rcx, r9
0034034C  call     0x267e10  ; -> 00267E10 fn
00340351  xor      r8d, r8d
00340354  mov      ecx, eax
00340356  lea      edx, [r8 + 1]
0034035A  call     0x359ca0  ; -> 00359CA0 fn
0034035F  mov      rcx, rax
00340362  xor      eax, eax
00340364  test     rcx, rcx
00340367  je       0x34036e  ; -> 0034036E
00340369  call     0x233dc0  ; -> 00233DC0 fn
0034036E  mov      edx, eax
00340370  mov      rcx, rbx
00340373  add      rsp, 0x20
00340377  pop      rbx
00340378  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 003405C0 (122 B, extent 003405C0-0034063A)

Documented callee on this page: `002640C0`

```
003405C0  mov      qword ptr [rsp + 8], rbx
003405C5  mov      qword ptr [rsp + 0x10], rbp
003405CA  mov      qword ptr [rsp + 0x18], rsi
003405CF  mov      qword ptr [rsp + 0x20], rdi
003405D4  push     r14
003405D6  sub      rsp, 0x30
003405DA  mov      rbp, r9
003405DD  call     0x2640c0  ; -> 002640C0 fn
003405E2  mov      rcx, rbp
003405E5  mov      r14, rax
003405E8  call     0x267e10  ; -> 00267E10 fn
003405ED  mov      rcx, rbp
003405F0  mov      esi, eax
003405F2  call     0x267e10  ; -> 00267E10 fn
003405F7  mov      rcx, rbp
003405FA  mov      edi, eax
003405FC  call     0x267e10  ; -> 00267E10 fn
00340601  mov      rcx, rbp
00340604  mov      ebx, eax
00340606  call     0x267e10  ; -> 00267E10 fn
0034060B  mov      r9d, edi
0034060E  mov      dword ptr [rsp + 0x20], esi
00340612  mov      r8d, ebx
00340615  mov      edx, eax
00340617  mov      rcx, r14
0034061A  call     0x3e9320  ; -> 003E9320 fn
0034061F  mov      rbx, qword ptr [rsp + 0x40]
00340624  mov      rbp, qword ptr [rsp + 0x48]
00340629  mov      rsi, qword ptr [rsp + 0x50]
0034062E  mov      rdi, qword ptr [rsp + 0x58]
00340633  add      rsp, 0x30
00340637  pop      r14
00340639  ret      
```

## 00340810 (95 B, extent 00340810-0034086F)

Documented callee on this page: `00267DB0`

```
00340810  mov      qword ptr [rsp + 8], rbx
00340815  push     rdi
00340816  sub      rsp, 0x30
0034081A  mov      rcx, r9
0034081D  movaps   xmmword ptr [rsp + 0x20], xmm6
00340822  mov      rbx, r9
00340825  mov      rdi, rdx
00340828  call     0x267db0  ; -> 00267DB0 fn
0034082D  mov      rcx, rbx
00340830  movaps   xmm6, xmm0
00340833  call     0x267db0  ; -> 00267DB0 fn
00340838  xorps    xmm1, xmm1
0034083B  comiss   xmm6, xmm1
0034083E  jb       0x34084a  ; -> 0034084A
00340840  movaps   xmm1, xmm0
00340843  maxss    xmm1, xmm6
00340847  movaps   xmm6, xmm1
0034084A  movaps   xmm1, xmm0
0034084D  mov      rcx, rdi
00340850  call     0x2ec970  ; -> 002EC970 fn
00340855  movaps   xmm1, xmm6
00340858  mov      rcx, rdi
0034085B  mov      rbx, qword ptr [rsp + 0x40]
00340860  movaps   xmm6, xmmword ptr [rsp + 0x20]
00340865  add      rsp, 0x30
00340869  pop      rdi
0034086A  jmp      0x2ec8b0  ; -> 002EC8B0 fn
```

## 00340890 (148 B, extent 00340890-00340924)

Documented callee on this page: `00267F90`

```
00340890  mov      qword ptr [rsp + 8], rbx
00340895  push     rdi
00340896  sub      rsp, 0x20
0034089A  mov      rcx, r9
0034089D  mov      rbx, r9
003408A0  call     0x267e10  ; -> 00267E10 fn
003408A5  mov      rcx, rbx
003408A8  mov      edi, eax
003408AA  call     0x267e10  ; -> 00267E10 fn
003408AF  mov      ecx, eax
003408B1  mov      ebx, eax
003408B3  call     0x16d6a0  ; -> 0016D6A0 fn
003408B8  mov      ecx, ebx
003408BA  call     0x3eb700  ; -> 003EB700 fn
003408BF  movsxd   rbx, eax
003408C2  mov      edx, edi
003408C4  mov      rcx, rbx
003408C7  call     0x3eb960  ; -> 003EB960 fn
003408CC  mov      edx, edi
003408CE  mov      rcx, rbx
003408D1  mov      rbx, qword ptr [rsp + 0x30]
003408D6  add      rsp, 0x20
003408DA  pop      rdi
003408DB  jmp      0x3eb8c0  ; -> 003EB8C0 fn
003408E0  mov      qword ptr [rsp + 8], rbx
003408E5  mov      qword ptr [rsp + 0x10], rbp
003408EA  mov      qword ptr [rsp + 0x18], rsi
003408EF  push     rdi
003408F0  sub      rsp, 0x20
003408F4  mov      rsi, rdx
003408F7  mov      rbp, rcx
003408FA  xor      edx, edx
003408FC  mov      rcx, r9
003408FF  mov      rbx, r9
00340902  mov      rdi, r8
00340905  call     0x267f90  ; -> 00267F90 fn
0034090A  xor      edx, edx
0034090C  mov      rcx, rbx
0034090F  call     0x267f90  ; -> 00267F90 fn
00340914  mov      r9, rbx
00340917  mov      r8, rdi
0034091A  mov      rdx, rsi
0034091D  mov      rcx, rbp
```

## 003412B0 (167 B, extent 003412B0-00341357)

Documented callee on this page: `00267DB0`

```
003412B0  push     rbx
003412B2  sub      rsp, 0x50
003412B6  mov      rax, qword ptr [rip + 0x1c03573]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003412BD  xor      rax, rsp
003412C0  mov      qword ptr [rsp + 0x40], rax
003412C5  movss    xmm0, dword ptr [rip + 0x19aa8db]  ; -> 01CEBBA8 [f32 1]
003412CD  mov      rcx, r9
003412D0  movss    dword ptr [rsp + 0x2c], xmm0
003412D6  mov      rbx, r9
003412D9  call     0x267db0  ; -> 00267DB0 fn
003412DE  mov      rcx, rbx
003412E1  movss    dword ptr [rsp + 0x28], xmm0
003412E7  call     0x267db0  ; -> 00267DB0 fn
003412EC  mov      rcx, rbx
003412EF  movss    dword ptr [rsp + 0x24], xmm0
003412F5  call     0x267db0  ; -> 00267DB0 fn
003412FA  mov      rcx, rbx
003412FD  movss    dword ptr [rsp + 0x20], xmm0
00341303  call     0x267e10  ; -> 00267E10 fn
00341308  mov      ecx, eax
0034130A  mov      ebx, eax
0034130C  call     0x16d6a0  ; -> 0016D6A0 fn
00341311  mov      ecx, ebx
00341313  call     0x3eb700  ; -> 003EB700 fn
00341318  lea      rdx, [rsp + 0x30]
0034131D  mov      rbx, rax
00341320  lea      rcx, [rsp + 0x20]
00341325  call     0x2e70d0  ; -> 002E70D0 fn
0034132A  movss    xmm3, dword ptr [rsp + 0x38]
00341330  movss    xmm2, dword ptr [rsp + 0x34]
00341336  movss    xmm1, dword ptr [rsp + 0x30]
0034133C  movsxd   rcx, ebx
0034133F  call     0x3eb860  ; -> 003EB860 fn
00341344  mov      rcx, qword ptr [rsp + 0x40]
00341349  xor      rcx, rsp
0034134C  call     0x808c40  ; -> 00808C40 fn
00341351  add      rsp, 0x50
00341355  pop      rbx
00341356  ret      
```

## 00341E60 (119 B, extent 00341E60-00341ED7)

Documented callee on this page: `0026B4E0`

```
00341E60  mov      qword ptr [rsp + 0x10], rbx
00341E65  push     rdi
00341E66  sub      rsp, 0x50
00341E6A  mov      rax, qword ptr [rip + 0x1c029bf]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00341E71  xor      rax, rsp
00341E74  mov      qword ptr [rsp + 0x40], rax
00341E79  mov      rdi, rcx
00341E7C  mov      edx, 4
00341E81  lea      rcx, [rsp + 0x20]
00341E86  call     0x31b670  ; -> 0031B670 fn
00341E8B  lea      rdx, [rsp + 0x20]
00341E90  mov      ecx, eax
00341E92  call     0x3599a0  ; -> 003599A0 fn
00341E97  mov      edx, 4
00341E9C  lea      rcx, [rsp + 0x20]
00341EA1  mov      ebx, eax
00341EA3  call     0x31b680  ; -> 0031B680 fn
00341EA8  lea      rdx, [rsp + 0x20]
00341EAD  mov      ecx, eax
00341EAF  call     0x3599a0  ; -> 003599A0 fn
00341EB4  mov      rcx, rdi
00341EB7  lea      edx, [rax + rbx]
00341EBA  call     0x26b4e0  ; -> 0026B4E0 fn
00341EBF  mov      rcx, qword ptr [rsp + 0x40]
00341EC4  xor      rcx, rsp
00341EC7  call     0x808c40  ; -> 00808C40 fn
00341ECC  mov      rbx, qword ptr [rsp + 0x68]
00341ED1  add      rsp, 0x50
00341ED5  pop      rdi
00341ED6  ret      
```

## 00342280 (149 B, extent 00342280-00342315)

Documented callee on this page: `0026B4E0`

```
00342280  mov      qword ptr [rsp + 0x10], rbx
00342285  mov      qword ptr [rsp + 0x18], rsi
0034228A  push     rdi
0034228B  sub      rsp, 0x50
0034228F  mov      rax, qword ptr [rip + 0x1c0259a]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00342296  xor      rax, rsp
00342299  mov      qword ptr [rsp + 0x40], rax
0034229E  mov      rsi, rcx
003422A1  mov      rcx, r9
003422A4  call     0x267e10  ; -> 00267E10 fn
003422A9  mov      edx, 4
003422AE  lea      rcx, [rsp + 0x20]
003422B3  mov      edi, eax
003422B5  call     0x31b670  ; -> 0031B670 fn
003422BA  mov      ebx, eax
003422BC  test     edi, edi
003422BE  je       0x3422ce  ; -> 003422CE
003422C0  lea      rdx, [rsp + 0x20]
003422C5  mov      ecx, eax
003422C7  call     0x3599a0  ; -> 003599A0 fn
003422CC  mov      ebx, eax
003422CE  mov      edx, 4
003422D3  lea      rcx, [rsp + 0x20]
003422D8  call     0x31b680  ; -> 0031B680 fn
003422DD  test     edi, edi
003422DF  je       0x3422ed  ; -> 003422ED
003422E1  lea      rdx, [rsp + 0x20]
003422E6  mov      ecx, eax
003422E8  call     0x3599a0  ; -> 003599A0 fn
003422ED  lea      edx, [rax + rbx]
003422F0  mov      rcx, rsi
003422F3  call     0x26b4e0  ; -> 0026B4E0 fn
003422F8  mov      rcx, qword ptr [rsp + 0x40]
003422FD  xor      rcx, rsp
00342300  call     0x808c40  ; -> 00808C40 fn
00342305  mov      rbx, qword ptr [rsp + 0x68]
0034230A  mov      rsi, qword ptr [rsp + 0x70]
0034230F  add      rsp, 0x50
00342313  pop      rdi
00342314  ret      
```

## 003426F0 (118 B, extent 003426F0-00342766)

Documented callee on this page: `0026B4E0`

```
003426F0  mov      qword ptr [rsp + 0x10], rbx
003426F5  push     rdi
003426F6  sub      rsp, 0x50
003426FA  mov      rax, qword ptr [rip + 0x1c0212f]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00342701  xor      rax, rsp
00342704  mov      qword ptr [rsp + 0x40], rax
00342709  mov      rdi, rcx
0034270C  mov      edx, 4
00342711  lea      rcx, [rsp + 0x20]
00342716  call     0x31b670  ; -> 0031B670 fn
0034271B  lea      rdx, [rsp + 0x20]
00342720  mov      ecx, eax
00342722  call     0x3599a0  ; -> 003599A0 fn
00342727  mov      edx, 4
0034272C  lea      rcx, [rsp + 0x20]
00342731  mov      ebx, eax
00342733  call     0x31b680  ; -> 0031B680 fn
00342738  lea      rdx, [rsp + 0x20]
0034273D  mov      ecx, eax
0034273F  call     0x3599a0  ; -> 003599A0 fn
00342744  mov      edx, ebx
00342746  mov      rcx, rdi
00342749  call     0x26b4e0  ; -> 0026B4E0 fn
0034274E  mov      rcx, qword ptr [rsp + 0x40]
00342753  xor      rcx, rsp
00342756  call     0x808c40  ; -> 00808C40 fn
0034275B  mov      rbx, qword ptr [rsp + 0x68]
00342760  add      rsp, 0x50
00342764  pop      rdi
00342765  ret      
```

## 00342BF0 (148 B, extent 00342BF0-00342C84)

Documented callee on this page: `0026B4E0`

```
00342BF0  mov      qword ptr [rsp + 0x10], rbx
00342BF5  mov      qword ptr [rsp + 0x18], rsi
00342BFA  push     rdi
00342BFB  sub      rsp, 0x50
00342BFF  mov      rax, qword ptr [rip + 0x1c01c2a]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00342C06  xor      rax, rsp
00342C09  mov      qword ptr [rsp + 0x40], rax
00342C0E  mov      rsi, rcx
00342C11  mov      rcx, r9
00342C14  call     0x267e10  ; -> 00267E10 fn
00342C19  mov      edx, 4
00342C1E  lea      rcx, [rsp + 0x20]
00342C23  mov      edi, eax
00342C25  call     0x31b670  ; -> 0031B670 fn
00342C2A  mov      ebx, eax
00342C2C  test     edi, edi
00342C2E  je       0x342c3e  ; -> 00342C3E
00342C30  lea      rdx, [rsp + 0x20]
00342C35  mov      ecx, eax
00342C37  call     0x3599a0  ; -> 003599A0 fn
00342C3C  mov      ebx, eax
00342C3E  mov      edx, 4
00342C43  lea      rcx, [rsp + 0x20]
00342C48  call     0x31b680  ; -> 0031B680 fn
00342C4D  test     edi, edi
00342C4F  je       0x342c5d  ; -> 00342C5D
00342C51  lea      rdx, [rsp + 0x20]
00342C56  mov      ecx, eax
00342C58  call     0x3599a0  ; -> 003599A0 fn
00342C5D  mov      edx, ebx
00342C5F  mov      rcx, rsi
00342C62  call     0x26b4e0  ; -> 0026B4E0 fn
00342C67  mov      rcx, qword ptr [rsp + 0x40]
00342C6C  xor      rcx, rsp
00342C6F  call     0x808c40  ; -> 00808C40 fn
00342C74  mov      rbx, qword ptr [rsp + 0x68]
00342C79  mov      rsi, qword ptr [rsp + 0x70]
00342C7E  add      rsp, 0x50
00342C82  pop      rdi
00342C83  ret      
```

## 003430C0 (107 B, extent 003430C0-0034312B)

Documented callee on this page: `0026B4E0`

```
003430C0  push     rbx
003430C2  sub      rsp, 0x50
003430C6  mov      rax, qword ptr [rip + 0x1c01763]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003430CD  xor      rax, rsp
003430D0  mov      qword ptr [rsp + 0x40], rax
003430D5  mov      rbx, rcx
003430D8  mov      edx, 4
003430DD  lea      rcx, [rsp + 0x20]
003430E2  call     0x31b670  ; -> 0031B670 fn
003430E7  lea      rdx, [rsp + 0x20]
003430EC  mov      ecx, eax
003430EE  call     0x3599a0  ; -> 003599A0 fn
003430F3  mov      edx, 4
003430F8  lea      rcx, [rsp + 0x20]
003430FD  call     0x31b680  ; -> 0031B680 fn
00343102  lea      rdx, [rsp + 0x20]
00343107  mov      ecx, eax
00343109  call     0x3599a0  ; -> 003599A0 fn
0034310E  mov      edx, eax
00343110  mov      rcx, rbx
00343113  call     0x26b4e0  ; -> 0026B4E0 fn
00343118  mov      rcx, qword ptr [rsp + 0x40]
0034311D  xor      rcx, rsp
00343120  call     0x808c40  ; -> 00808C40 fn
00343125  add      rsp, 0x50
00343129  pop      rbx
0034312A  ret      
```

## 003433E0 (134 B, extent 003433E0-00343466)

Documented callee on this page: `0026B4E0`

```
003433E0  mov      qword ptr [rsp + 0x10], rbx
003433E5  push     rdi
003433E6  sub      rsp, 0x50
003433EA  mov      rax, qword ptr [rip + 0x1c0143f]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003433F1  xor      rax, rsp
003433F4  mov      qword ptr [rsp + 0x40], rax
003433F9  mov      rdi, rcx
003433FC  mov      rcx, r9
003433FF  call     0x267e10  ; -> 00267E10 fn
00343404  mov      edx, 4
00343409  lea      rcx, [rsp + 0x20]
0034340E  mov      ebx, eax
00343410  call     0x31b670  ; -> 0031B670 fn
00343415  test     ebx, ebx
00343417  je       0x343425  ; -> 00343425
00343419  lea      rdx, [rsp + 0x20]
0034341E  mov      ecx, eax
00343420  call     0x3599a0  ; -> 003599A0 fn
00343425  mov      edx, 4
0034342A  lea      rcx, [rsp + 0x20]
0034342F  call     0x31b680  ; -> 0031B680 fn
00343434  test     ebx, ebx
00343436  je       0x343444  ; -> 00343444
00343438  lea      rdx, [rsp + 0x20]
0034343D  mov      ecx, eax
0034343F  call     0x3599a0  ; -> 003599A0 fn
00343444  mov      edx, eax
00343446  mov      rcx, rdi
00343449  call     0x26b4e0  ; -> 0026B4E0 fn
0034344E  mov      rcx, qword ptr [rsp + 0x40]
00343453  xor      rcx, rsp
00343456  call     0x808c40  ; -> 00808C40 fn
0034345B  mov      rbx, qword ptr [rsp + 0x68]
00343460  add      rsp, 0x50
00343464  pop      rdi
00343465  ret      
```

## 00344000 (74 B, extent 00344000-0034404A)

Documented callee on this page: `002650B0`

```
00344000  mov      qword ptr [rsp + 8], rbx
00344005  mov      qword ptr [rsp + 0x10], rsi
0034400A  push     rdi
0034400B  sub      rsp, 0x20
0034400F  mov      rdi, r9
00344012  mov      rsi, rcx
00344015  call     0x2640c0  ; -> 002640C0 fn
0034401A  mov      rcx, rdi
0034401D  mov      rbx, rax
00344020  call     0x267e10  ; -> 00267E10 fn
00344025  mov      r8d, eax
00344028  mov      rdx, rsi
0034402B  mov      rcx, rbx
0034402E  call     0x2650b0  ; -> 002650B0 fn
00344033  mov      rcx, rax
00344036  mov      rbx, qword ptr [rsp + 0x30]
0034403B  mov      rsi, qword ptr [rsp + 0x38]
00344040  add      rsp, 0x20
00344044  pop      rdi
00344045  jmp      0x3ebe70  ; -> 003EBE70 fn
```

## 003449A0 (114 B, extent 003449A0-00344A12)

Documented callee on this page: `0026B4E0`

```
003449A0  mov      qword ptr [rsp + 8], rbx
003449A5  mov      qword ptr [rsp + 0x10], rbp
003449AA  mov      qword ptr [rsp + 0x18], rsi
003449AF  push     rdi
003449B0  sub      rsp, 0x20
003449B4  mov      rbp, rcx
003449B7  mov      rdi, r9
003449BA  mov      rcx, r9
003449BD  call     0x267e10  ; -> 00267E10 fn
003449C2  mov      rcx, rdi
003449C5  mov      ebx, eax
003449C7  call     0x267e10  ; -> 00267E10 fn
003449CC  mov      rcx, rdi
003449CF  mov      esi, eax
003449D1  call     0x267e10  ; -> 00267E10 fn
003449D6  mov      edi, eax
003449D8  test     ebx, ebx
003449DA  je       0x3449eb  ; -> 003449EB
003449DC  mov      r8d, 1
003449E2  mov      edx, esi
003449E4  mov      ecx, eax
003449E6  call     0x2e2540  ; -> 002E2540 fn
003449EB  mov      edx, esi
003449ED  mov      ecx, edi
003449EF  call     0x32a810  ; -> 0032A810 fn
003449F4  mov      edx, eax
003449F6  mov      rcx, rbp
003449F9  mov      rbx, qword ptr [rsp + 0x30]
003449FE  mov      rbp, qword ptr [rsp + 0x38]
00344A03  mov      rsi, qword ptr [rsp + 0x40]
00344A08  add      rsp, 0x20
00344A0C  pop      rdi
00344A0D  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00344EC0 (56 B, extent 00344EC0-00344EF8)

Documented callee on this page: `0026B4E0`

```
00344EC0  push     rbx
00344EC2  sub      rsp, 0x20
00344EC6  mov      rbx, rcx
00344EC9  mov      rcx, r9
00344ECC  call     0x267e10  ; -> 00267E10 fn
00344ED1  mov      ecx, eax
00344ED3  call     0x35a140  ; -> 0035A140 fn
00344ED8  mov      ecx, eax
00344EDA  call     0x31a900  ; -> 0031A900 fn
00344EDF  test     eax, eax
00344EE1  mov      ecx, 1
00344EE6  cmovne   eax, ecx
00344EE9  mov      rcx, rbx
00344EEC  mov      edx, eax
00344EEE  add      rsp, 0x20
00344EF2  pop      rbx
00344EF3  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00345080 (127 B, extent 00345080-003450FF)

Documented callee on this page: `00267F90`

```
00345080  mov      qword ptr [rsp + 8], rbx
00345085  mov      qword ptr [rsp + 0x10], rbp
0034508A  mov      qword ptr [rsp + 0x18], rsi
0034508F  push     rdi
00345090  sub      rsp, 0x20
00345094  mov      rbp, rcx
00345097  mov      edx, 1
0034509C  mov      rcx, r9
0034509F  mov      rdi, r9
003450A2  call     0x267f90  ; -> 00267F90 fn
003450A7  mov      rcx, rdi
003450AA  call     0x267e10  ; -> 00267E10 fn
003450AF  mov      rcx, rdi
003450B2  mov      ebx, eax
003450B4  call     0x267e10  ; -> 00267E10 fn
003450B9  mov      rcx, rdi
003450BC  mov      esi, eax
003450BE  call     0x267e10  ; -> 00267E10 fn
003450C3  mov      edi, eax
003450C5  test     ebx, ebx
003450C7  je       0x3450d8  ; -> 003450D8
003450C9  mov      r8d, 1
003450CF  mov      edx, esi
003450D1  mov      ecx, eax
003450D3  call     0x2e2540  ; -> 002E2540 fn
003450D8  mov      edx, esi
003450DA  mov      ecx, edi
003450DC  call     0x32a810  ; -> 0032A810 fn
003450E1  mov      edx, eax
003450E3  mov      rcx, rbp
003450E6  mov      rbx, qword ptr [rsp + 0x30]
003450EB  mov      rbp, qword ptr [rsp + 0x38]
003450F0  mov      rsi, qword ptr [rsp + 0x40]
003450F5  add      rsp, 0x20
003450F9  pop      rdi
003450FA  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00346680 (28 B, extent 00346680-0034669C)

Documented callee on this page: `002640C0`

```
00346680  sub      rsp, 0x28
00346684  mov      dword ptr [r8], 0
0034668B  call     0x2640c0  ; -> 002640C0 fn
00346690  mov      rcx, rax
00346693  add      rsp, 0x28
00346697  jmp      0x26b8a0  ; -> 0026B8A0 fn
```
