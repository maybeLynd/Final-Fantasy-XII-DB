# F homing pack (FABLE): `00-Engine-Core-Runtime/Application-Root/game-application.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 20. No bearing page cites them and no documented function calls them directly.

## 005AA160 (102 B, extent 005AA160-005AA1C6)

Documented callee on this page: `00584730`

```
005AA160  push     rdi
005AA162  sub      rsp, 0x30
005AA166  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005AA16F  mov      qword ptr [rsp + 0x40], rbx
005AA174  mov      rbx, rcx
005AA177  mov      eax, dword ptr [rcx + 0x10]
005AA17A  shr      eax, 0x1f
005AA17D  not      al
005AA17F  test     al, 1
005AA181  je       0x5aa192  ; -> 005AA192
005AA183  mov      rcx, qword ptr [rcx + 0x18]
005AA187  test     rcx, rcx
005AA18A  je       0x5aa192  ; -> 005AA192
005AA18C  call     0x584730  ; -> 00584730 fn
005AA191  nop      
005AA192  xor      edi, edi
005AA194  mov      qword ptr [rbx + 0x18], rdi
005AA198  mov      dword ptr [rbx + 0x10], edi
005AA19B  mov      eax, dword ptr [rbx]
005AA19D  shr      eax, 0x1f
005AA1A0  not      al
005AA1A2  test     al, 1
005AA1A4  je       0x5aa1b5  ; -> 005AA1B5
005AA1A6  mov      rcx, qword ptr [rbx + 8]
005AA1AA  test     rcx, rcx
005AA1AD  je       0x5aa1b5  ; -> 005AA1B5
005AA1AF  call     0x584730  ; -> 00584730 fn
005AA1B4  nop      
005AA1B5  mov      qword ptr [rbx + 8], rdi
005AA1B9  mov      dword ptr [rbx], edi
005AA1BB  mov      rbx, qword ptr [rsp + 0x40]
005AA1C0  add      rsp, 0x30
005AA1C4  pop      rdi
005AA1C5  ret      
```

## 005AA280 (63 B, extent 005AA280-005AA2BF)

Documented callee on this page: `00809054`

```
005AA280  push     rbx
005AA282  sub      rsp, 0x30
005AA286  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005AA28F  mov      rcx, qword ptr [rcx]
005AA292  test     rcx, rcx
005AA295  je       0x5aa2b9  ; -> 005AA2B9
005AA297  lea      rbx, [rcx - 8]
005AA29B  lea      r9, [rip + 0x4e]  ; -> 005AA2F0
005AA2A2  mov      r8, qword ptr [rbx]
005AA2A5  mov      edx, 0x138
005AA2AA  call     0x809054  ; -> 00809054 fn
005AA2AF  nop      
005AA2B0  mov      rcx, rbx
005AA2B3  call     0x584730  ; -> 00584730 fn
005AA2B8  nop      
005AA2B9  add      rsp, 0x30
005AA2BD  pop      rbx
005AA2BE  ret      
```

## 005AA2F0 (174 B, extent 005AA2F0-005AA39E)

Documented callee on this page: `00584730`

```
005AA2F0  push     rdi
005AA2F2  sub      rsp, 0x30
005AA2F6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005AA2FF  mov      qword ptr [rsp + 0x40], rbx
005AA304  mov      rbx, rcx
005AA307  mov      eax, dword ptr [rcx + 0x120]
005AA30D  shr      eax, 0x1f
005AA310  not      al
005AA312  test     al, 1
005AA314  je       0x5aa328  ; -> 005AA328
005AA316  mov      rcx, qword ptr [rcx + 0x128]
005AA31D  test     rcx, rcx
005AA320  je       0x5aa328  ; -> 005AA328
005AA322  call     0x584730  ; -> 00584730 fn
005AA327  nop      
005AA328  xor      edi, edi
005AA32A  mov      qword ptr [rbx + 0x128], rdi
005AA331  mov      dword ptr [rbx + 0x120], edi
005AA337  mov      eax, dword ptr [rbx + 0x110]
005AA33D  shr      eax, 0x1f
005AA340  not      al
005AA342  test     al, 1
005AA344  je       0x5aa358  ; -> 005AA358
005AA346  mov      rcx, qword ptr [rbx + 0x118]
005AA34D  test     rcx, rcx
005AA350  je       0x5aa358  ; -> 005AA358
005AA352  call     0x584730  ; -> 00584730 fn
005AA357  nop      
005AA358  mov      qword ptr [rbx + 0x118], rdi
005AA35F  mov      dword ptr [rbx + 0x110], edi
005AA365  mov      eax, dword ptr [rbx + 0x100]
005AA36B  shr      eax, 0x1f
005AA36E  not      al
005AA370  test     al, 1
005AA372  je       0x5aa386  ; -> 005AA386
005AA374  mov      rcx, qword ptr [rbx + 0x108]
005AA37B  test     rcx, rcx
005AA37E  je       0x5aa386  ; -> 005AA386
005AA380  call     0x584730  ; -> 00584730 fn
005AA385  nop      
005AA386  mov      qword ptr [rbx + 0x108], rdi
005AA38D  mov      dword ptr [rbx + 0x100], edi
005AA393  mov      rbx, qword ptr [rsp + 0x40]
005AA398  add      rsp, 0x30
005AA39C  pop      rdi
005AA39D  ret      
```

## 005AA3C0 (138 B, extent 005AA3C0-005AA44A)

Documented callee on this page: `0017D260`

```
005AA3C0  mov      qword ptr [rsp + 8], rbx
005AA3C5  mov      qword ptr [rsp + 0x10], rbp
005AA3CA  mov      qword ptr [rsp + 0x18], rsi
005AA3CF  push     rdi
005AA3D0  sub      rsp, 0x20
005AA3D4  mov      esi, dword ptr [rdx]
005AA3D6  mov      rbx, rcx
005AA3D9  mov      rbp, qword ptr [rdx + 8]
005AA3DD  mov      edi, 0
005AA3E2  and      esi, 0x7fffffff
005AA3E8  jbe      0x5aa40e  ; -> 005AA40E
005AA3EA  mov      ecx, esi
005AA3EC  lea      edx, [rdi + 4]
005AA3EF  shl      rcx, 2
005AA3F3  call     0x17d260  ; -> 0017D260 fn
005AA3F8  mov      rdi, rax
005AA3FB  test     rax, rax
005AA3FE  je       0x5aa40e  ; -> 005AA40E
005AA400  mov      r8d, esi
005AA403  mov      rdx, rbp
005AA406  mov      rcx, rax
005AA409  call     0x5a5b40  ; -> 005A5B40 fn
005AA40E  mov      rcx, qword ptr [rbx + 8]
005AA412  cmp      rcx, rdi
005AA415  je       0x5aa42c  ; -> 005AA42C
005AA417  mov      eax, dword ptr [rbx]
005AA419  shr      eax, 0x1f
005AA41C  not      al
005AA41E  test     al, 1
005AA420  je       0x5aa42c  ; -> 005AA42C
005AA422  test     rcx, rcx
005AA425  je       0x5aa42c  ; -> 005AA42C
005AA427  call     0x584730  ; -> 00584730 fn
005AA42C  mov      rbp, qword ptr [rsp + 0x38]
005AA431  mov      rax, rbx
005AA434  mov      dword ptr [rbx], esi
005AA436  mov      rsi, qword ptr [rsp + 0x40]
005AA43B  mov      qword ptr [rbx + 8], rdi
005AA43F  mov      rbx, qword ptr [rsp + 0x30]
005AA444  add      rsp, 0x20
005AA448  pop      rdi
005AA449  ret      
```

## 005AD1B0 (124 B, extent 005AD1B0-005AD22C)

Documented callee on this page: `0017D260`

```
005AD1B0  mov      qword ptr [rsp + 0x10], rbx
005AD1B5  push     rsi
005AD1B6  sub      rsp, 0x20
005AD1BA  mov      esi, ecx
005AD1BC  mov      rbx, rdx
005AD1BF  test     ecx, ecx
005AD1C1  je       0x5ad21f  ; -> 005AD21F
005AD1C3  mov      qword ptr [rsp + 0x30], rdi
005AD1C8  lea      rcx, [rsi*8]
005AD1D0  mov      edx, 4
005AD1D5  mov      edi, esi
005AD1D7  call     0x17d260  ; -> 0017D260 fn
005AD1DC  mov      r8, rax
005AD1DF  test     rax, rax
005AD1E2  je       0x5ad20f  ; -> 005AD20F
005AD1E4  mov      rcx, rax
005AD1E7  test     esi, esi
005AD1E9  je       0x5ad20f  ; -> 005AD20F
005AD1EB  nop      dword ptr [rax + rax]
005AD1F0  mov      rdx, rcx
005AD1F3  add      rcx, 8
005AD1F7  test     rdx, rdx
005AD1FA  je       0x5ad206  ; -> 005AD206
005AD1FC  mov      rax, qword ptr [rbx]
005AD1FF  add      rbx, 8
005AD203  mov      qword ptr [rdx], rax
005AD206  sub      rdi, 1
005AD20A  jne      0x5ad1f0  ; -> 005AD1F0
005AD20C  mov      rax, r8
005AD20F  mov      rdi, qword ptr [rsp + 0x30]
005AD214  mov      rbx, qword ptr [rsp + 0x38]
005AD219  add      rsp, 0x20
005AD21D  pop      rsi
005AD21E  ret      
005AD21F  xor      eax, eax
005AD221  mov      rbx, qword ptr [rsp + 0x38]
005AD226  add      rsp, 0x20
005AD22A  pop      rsi
005AD22B  ret      
```

## 005B7E80 (101 B, extent 005B7E80-005B7EE5)

Documented callee on this page: `00584730`

```
005B7E80  test     rcx, rcx
005B7E83  je       0x5b7ee4  ; -> 005B7EE4
005B7E85  push     rbp
005B7E86  sub      rsp, 0x20
005B7E8A  mov      rbp, rcx
005B7E8D  test     edx, edx
005B7E8F  je       0x5b7ed7  ; -> 005B7ED7
005B7E91  mov      qword ptr [rsp + 0x30], rbx
005B7E96  mov      rbx, rcx
005B7E99  mov      qword ptr [rsp + 0x38], rsi
005B7E9E  mov      qword ptr [rsp + 0x40], rdi
005B7EA3  mov      rdi, rcx
005B7EA6  mov      esi, edx
005B7EA8  nop      dword ptr [rax + rax]
005B7EB0  mov      rax, qword ptr [rbx]
005B7EB3  xor      edx, edx
005B7EB5  mov      rcx, rdi
005B7EB8  call     qword ptr [rax]
005B7EBA  add      rdi, 0x20
005B7EBE  lea      rbx, [rbx + 0x20]
005B7EC2  sub      rsi, 1
005B7EC6  jne      0x5b7eb0  ; -> 005B7EB0
005B7EC8  mov      rdi, qword ptr [rsp + 0x40]
005B7ECD  mov      rsi, qword ptr [rsp + 0x38]
005B7ED2  mov      rbx, qword ptr [rsp + 0x30]
005B7ED7  mov      rcx, rbp
005B7EDA  call     0x584730  ; -> 00584730 fn
005B7EDF  add      rsp, 0x20
005B7EE3  pop      rbp
005B7EE4  ret      
```

## 005B7EF0 (101 B, extent 005B7EF0-005B7F55)

Documented callee on this page: `00584730`

```
005B7EF0  test     rcx, rcx
005B7EF3  je       0x5b7f54  ; -> 005B7F54
005B7EF5  push     rbp
005B7EF6  sub      rsp, 0x20
005B7EFA  mov      rbp, rcx
005B7EFD  test     edx, edx
005B7EFF  je       0x5b7f47  ; -> 005B7F47
005B7F01  mov      qword ptr [rsp + 0x30], rbx
005B7F06  mov      rbx, rcx
005B7F09  mov      qword ptr [rsp + 0x38], rsi
005B7F0E  mov      qword ptr [rsp + 0x40], rdi
005B7F13  mov      rdi, rcx
005B7F16  mov      esi, edx
005B7F18  nop      dword ptr [rax + rax]
005B7F20  mov      rax, qword ptr [rbx]
005B7F23  xor      edx, edx
005B7F25  mov      rcx, rdi
005B7F28  call     qword ptr [rax]
005B7F2A  add      rdi, 0x10
005B7F2E  lea      rbx, [rbx + 0x10]
005B7F32  sub      rsi, 1
005B7F36  jne      0x5b7f20  ; -> 005B7F20
005B7F38  mov      rdi, qword ptr [rsp + 0x40]
005B7F3D  mov      rsi, qword ptr [rsp + 0x38]
005B7F42  mov      rbx, qword ptr [rsp + 0x30]
005B7F47  mov      rcx, rbp
005B7F4A  call     0x584730  ; -> 00584730 fn
005B7F4F  add      rsp, 0x20
005B7F53  pop      rbp
005B7F54  ret      
```

## 005B7F60 (101 B, extent 005B7F60-005B7FC5)

Documented callee on this page: `00584730`

```
005B7F60  test     rcx, rcx
005B7F63  je       0x5b7fc4  ; -> 005B7FC4
005B7F65  push     rbp
005B7F66  sub      rsp, 0x20
005B7F6A  mov      rbp, rcx
005B7F6D  test     edx, edx
005B7F6F  je       0x5b7fb7  ; -> 005B7FB7
005B7F71  mov      qword ptr [rsp + 0x30], rbx
005B7F76  mov      rbx, rcx
005B7F79  mov      qword ptr [rsp + 0x38], rsi
005B7F7E  mov      qword ptr [rsp + 0x40], rdi
005B7F83  mov      rdi, rcx
005B7F86  mov      esi, edx
005B7F88  nop      dword ptr [rax + rax]
005B7F90  mov      rax, qword ptr [rbx]
005B7F93  xor      edx, edx
005B7F95  mov      rcx, rdi
005B7F98  call     qword ptr [rax]
005B7F9A  add      rdi, 0x18
005B7F9E  lea      rbx, [rbx + 0x18]
005B7FA2  sub      rsi, 1
005B7FA6  jne      0x5b7f90  ; -> 005B7F90
005B7FA8  mov      rdi, qword ptr [rsp + 0x40]
005B7FAD  mov      rsi, qword ptr [rsp + 0x38]
005B7FB2  mov      rbx, qword ptr [rsp + 0x30]
005B7FB7  mov      rcx, rbp
005B7FBA  call     0x584730  ; -> 00584730 fn
005B7FBF  add      rsp, 0x20
005B7FC3  pop      rbp
005B7FC4  ret      
```

## 005CD960 (91 B, extent 005CD960-005CD9BB)

Documented callee on this page: `005CDA30`

```
005CD960  sub      rsp, 0x28
005CD964  mov      rax, qword ptr gs:[0x58]
005CD96D  mov      ecx, dword ptr [rip + 0x28e13c9]  ; -> 02EAED3C
005CD973  mov      edx, 4
005CD978  mov      rcx, qword ptr [rax + rcx*8]
005CD97C  mov      eax, dword ptr [rdx + rcx]
005CD97F  cmp      dword ptr [rip + 0x26e87d3], eax  ; -> 02CB6158
005CD985  jg       0x5cd98c  ; -> 005CD98C
005CD987  add      rsp, 0x28
005CD98B  ret      
005CD98C  lea      rcx, [rip + 0x26e87c5]  ; -> 02CB6158
005CD993  call     0x8092fc  ; -> 008092FC fn
005CD998  cmp      dword ptr [rip + 0x26e87b9], -1  ; -> 02CB6158
005CD99F  jne      0x5cd987  ; -> 005CD987
005CD9A1  call     0x5cda30  ; -> 005CDA30 fn
005CD9A6  lea      rcx, [rip + 0x26e87ab]  ; -> 02CB6158
005CD9AD  mov      qword ptr [rip + 0x26e879c], rax  ; -> 02CB6150
005CD9B4  call     0x80929c  ; -> 0080929C fn
005CD9B9  jmp      0x5cd987  ; -> 005CD987
```

## 005CEBA0 (72 B, extent 005CEBA0-005CEBE8)

Documented callee on this page: `00584730`

```
005CEBA0  push     rbx
005CEBA2  sub      rsp, 0x30
005CEBA6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005CEBAF  mov      rbx, rdx
005CEBB2  mov      ecx, dword ptr [rdx + 0x38]
005CEBB5  mov      eax, ecx
005CEBB7  shr      eax, 0x1f
005CEBBA  not      al
005CEBBC  test     al, 1
005CEBBE  je       0x5cebd7  ; -> 005CEBD7
005CEBC0  btr      ecx, 0x1f
005CEBC4  cmp      ecx, 1
005CEBC7  jbe      0x5cebd7  ; -> 005CEBD7
005CEBC9  mov      rcx, qword ptr [rdx + 0x40]
005CEBCD  test     rcx, rcx
005CEBD0  je       0x5cebd7  ; -> 005CEBD7
005CEBD2  call     0x584730  ; -> 00584730 fn
005CEBD7  xor      eax, eax
005CEBD9  mov      qword ptr [rbx + 0x40], rax
005CEBDD  mov      dword ptr [rbx + 0x38], eax
005CEBE0  mov      al, 1
005CEBE2  add      rsp, 0x30
005CEBE6  pop      rbx
005CEBE7  ret      
```

## 005D2470 (71 B, extent 005D2470-005D24B7)

Documented callee on this page: `00584730`

```
005D2470  push     rbx
005D2472  sub      rsp, 0x30
005D2476  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005D247F  mov      rbx, rdx
005D2482  mov      rcx, qword ptr [rdx + 8]
005D2486  test     rcx, rcx
005D2489  je       0x5d2499  ; -> 005D2499
005D248B  mov      eax, ecx
005D248D  not      al
005D248F  test     al, 1
005D2491  je       0x5d2499  ; -> 005D2499
005D2493  call     0x584730  ; -> 00584730 fn
005D2498  nop      
005D2499  mov      rcx, qword ptr [rbx]
005D249C  test     rcx, rcx
005D249F  je       0x5d24af  ; -> 005D24AF
005D24A1  mov      eax, ecx
005D24A3  not      al
005D24A5  test     al, 1
005D24A7  je       0x5d24af  ; -> 005D24AF
005D24A9  call     0x584730  ; -> 00584730 fn
005D24AE  nop      
005D24AF  mov      al, 1
005D24B1  add      rsp, 0x30
005D24B5  pop      rbx
005D24B6  ret      
```

## 005D7720 (66 B, extent 005D7720-005D7762)

Documented callee on this page: `005CCB80`

```
005D7720  push     rbx
005D7722  sub      rsp, 0x30
005D7726  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005D772F  mov      rbx, rdx
005D7732  mov      eax, dword ptr [rdx + 4]
005D7735  test     eax, eax
005D7737  jle      0x5d7751  ; -> 005D7751
005D7739  nop      dword ptr [rax]
005D7740  mov      ecx, 1
005D7745  call     0x5ccb80  ; -> 005CCB80 fn
005D774A  mov      eax, dword ptr [rbx + 4]
005D774D  test     eax, eax
005D774F  jg       0x5d7740  ; -> 005D7740
005D7751  mov      rcx, rbx
005D7754  call     0x6164b0  ; -> 006164B0 fn
005D7759  nop      
005D775A  mov      al, 1
005D775C  add      rsp, 0x30
005D7760  pop      rbx
005D7761  ret      
```

## 005DE310 (63 B, extent 005DE310-005DE34F)

Documented callee on this page: `006108C0`

```
005DE310  push     rbx
005DE312  sub      rsp, 0x30
005DE316  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005DE31F  mov      rbx, rcx
005DE322  cmp      byte ptr [rcx + 8], 0
005DE326  je       0x5de33a  ; -> 005DE33A
005DE328  lea      rdx, [rip + 0x76d021]  ; -> 00D4B350
005DE32F  mov      ecx, 3
005DE334  call     0x5cdaa0  ; -> 005CDAA0 fn
005DE339  nop      
005DE33A  mov      rcx, qword ptr [rbx + 0x20]
005DE33E  test     rcx, rcx
005DE341  je       0x5de349  ; -> 005DE349
005DE343  call     0x6108c0  ; -> 006108C0 fn
005DE348  nop      
005DE349  add      rsp, 0x30
005DE34D  pop      rbx
005DE34E  ret      
```

## 005DE390 (63 B, extent 005DE390-005DE3CF)

Documented callee on this page: `006108C0`

```
005DE390  push     rbx
005DE392  sub      rsp, 0x30
005DE396  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005DE39F  mov      rbx, rcx
005DE3A2  cmp      byte ptr [rcx + 8], 0
005DE3A6  je       0x5de3ba  ; -> 005DE3BA
005DE3A8  lea      rdx, [rip + 0x76cfa1]  ; -> 00D4B350
005DE3AF  mov      ecx, 3
005DE3B4  call     0x5cdaa0  ; -> 005CDAA0 fn
005DE3B9  nop      
005DE3BA  mov      rcx, qword ptr [rbx + 0x20]
005DE3BE  test     rcx, rcx
005DE3C1  je       0x5de3c9  ; -> 005DE3C9
005DE3C3  call     0x6108c0  ; -> 006108C0 fn
005DE3C8  nop      
005DE3C9  add      rsp, 0x30
005DE3CD  pop      rbx
005DE3CE  ret      
```

## 005F0470 (173 B, extent 005F0470-005F051D)

Documented callee on this page: `00584730`

```
005F0470  test     rcx, rcx
005F0473  je       0x5f051c  ; -> 005F051C
005F0479  push     rdi
005F047A  sub      rsp, 0x30
005F047E  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005F0487  mov      qword ptr [rsp + 0x40], rbx
005F048C  mov      qword ptr [rsp + 0x48], rsi
005F0491  mov      rsi, rcx
005F0494  test     edx, edx
005F0496  je       0x5f0505  ; -> 005F0505
005F0498  lea      rbx, [rcx + 0x10]
005F049C  mov      edi, edx
005F049E  nop      
005F04A0  mov      rcx, qword ptr [rbx + 8]
005F04A4  test     rcx, rcx
005F04A7  je       0x5f04b7  ; -> 005F04B7
005F04A9  mov      eax, ecx
005F04AB  not      al
005F04AD  test     al, 1
005F04AF  je       0x5f04b7  ; -> 005F04B7
005F04B1  call     0x584730  ; -> 00584730 fn
005F04B6  nop      
005F04B7  mov      rcx, qword ptr [rbx]
005F04BA  test     rcx, rcx
005F04BD  je       0x5f04cd  ; -> 005F04CD
005F04BF  mov      eax, ecx
005F04C1  not      al
005F04C3  test     al, 1
005F04C5  je       0x5f04cd  ; -> 005F04CD
005F04C7  call     0x584730  ; -> 00584730 fn
005F04CC  nop      
005F04CD  mov      rcx, qword ptr [rbx - 8]
005F04D1  test     rcx, rcx
005F04D4  je       0x5f04e4  ; -> 005F04E4
005F04D6  mov      eax, ecx
005F04D8  not      al
005F04DA  test     al, 1
005F04DC  je       0x5f04e4  ; -> 005F04E4
005F04DE  call     0x584730  ; -> 00584730 fn
005F04E3  nop      
005F04E4  mov      rcx, qword ptr [rbx - 0x10]
005F04E8  test     rcx, rcx
005F04EB  je       0x5f04fb  ; -> 005F04FB
005F04ED  mov      eax, ecx
005F04EF  not      al
005F04F1  test     al, 1
005F04F3  je       0x5f04fb  ; -> 005F04FB
005F04F5  call     0x584730  ; -> 00584730 fn
005F04FA  nop      
005F04FB  add      rbx, 0x30
005F04FF  sub      rdi, 1
005F0503  jne      0x5f04a0  ; -> 005F04A0
005F0505  mov      rcx, rsi
005F0508  call     0x584730  ; -> 00584730 fn
005F050D  mov      rbx, qword ptr [rsp + 0x40]
005F0512  mov      rsi, qword ptr [rsp + 0x48]
005F0517  add      rsp, 0x30
005F051B  pop      rdi
005F051C  ret      
```

## 0060C340 (162 B, extent 0060C340-0060C3E2)

Documented callee on this page: `0017D260`

```
0060C340  mov      qword ptr [rsp + 0x10], rbx
0060C345  mov      qword ptr [rsp + 0x18], rbp
0060C34A  mov      qword ptr [rsp + 0x20], rsi
0060C34F  push     r14
0060C351  sub      rsp, 0x20
0060C355  mov      rsi, rcx
0060C358  mov      ebx, edx
0060C35A  cmp      edx, dword ptr [rcx]
0060C35C  je       0x60c3bf  ; -> 0060C3BF
0060C35E  xor      ebp, ebp
0060C360  test     edx, edx
0060C362  je       0x60c3d7  ; -> 0060C3D7
0060C364  mov      r14d, ebx
0060C367  lea      edx, [rbp + 8]
0060C36A  shl      r14, 3
0060C36E  mov      rcx, r14
0060C371  call     0x17d260  ; -> 0017D260 fn
0060C376  mov      rbp, rax
0060C379  test     rax, rax
0060C37C  je       0x60c3d7  ; -> 0060C3D7
0060C37E  test     ebx, ebx
0060C380  je       0x60c39b  ; -> 0060C39B
0060C382  mov      qword ptr [rsp + 0x30], rdi
0060C387  mov      rdi, rax
0060C38A  shr      r14, 3
0060C38E  xor      eax, eax
0060C390  mov      rcx, r14
0060C393  rep stosq qword ptr [rdi], rax
0060C396  mov      rdi, qword ptr [rsp + 0x30]
0060C39B  mov      rcx, qword ptr [rsi + 8]
0060C39F  cmp      rcx, rbp
0060C3A2  je       0x60c3b9  ; -> 0060C3B9
0060C3A4  mov      eax, dword ptr [rsi]
0060C3A6  shr      eax, 0x1f
0060C3A9  not      al
0060C3AB  test     al, 1
0060C3AD  je       0x60c3b9  ; -> 0060C3B9
0060C3AF  test     rcx, rcx
0060C3B2  je       0x60c3b9  ; -> 0060C3B9
0060C3B4  call     0x584730  ; -> 00584730 fn
0060C3B9  mov      qword ptr [rsi + 8], rbp
0060C3BD  mov      dword ptr [rsi], ebx
0060C3BF  xor      eax, eax
0060C3C1  mov      rbx, qword ptr [rsp + 0x38]
0060C3C6  mov      rbp, qword ptr [rsp + 0x40]
0060C3CB  mov      rsi, qword ptr [rsp + 0x48]
0060C3D0  add      rsp, 0x20
0060C3D4  pop      r14
0060C3D6  ret      
0060C3D7  test     ebx, ebx
0060C3D9  je       0x60c39b  ; -> 0060C39B
0060C3DB  mov      eax, 0xd
0060C3E0  jmp      0x60c3c1  ; -> 0060C3C1
```

## 0060C3F0 (135 B, extent 0060C3F0-0060C477)

Documented callee on this page: `00584730`

```
0060C3F0  mov      qword ptr [rsp + 8], rbx
0060C3F5  mov      qword ptr [rsp + 0x10], rsi
0060C3FA  push     rdi
0060C3FB  sub      rsp, 0x20
0060C3FF  mov      r8d, dword ptr [rcx]
0060C402  mov      edi, edx
0060C404  btr      r8d, 0x1f
0060C409  mov      rbx, rcx
0060C40C  cmp      edx, dword ptr [rcx]
0060C40E  je       0x60c465  ; -> 0060C465
0060C410  cmp      edx, r8d
0060C413  cmovb    r8d, edx
0060C417  mov      rdx, qword ptr [rcx + 8]
0060C41B  mov      ecx, edi
0060C41D  call     0x5e3040  ; -> 005E3040 fn
0060C422  mov      rsi, rax
0060C425  test     rax, rax
0060C428  jne      0x60c441  ; -> 0060C441
0060C42A  test     edi, edi
0060C42C  je       0x60c441  ; -> 0060C441
0060C42E  lea      eax, [rsi + 0xd]
0060C431  mov      rbx, qword ptr [rsp + 0x30]
0060C436  mov      rsi, qword ptr [rsp + 0x38]
0060C43B  add      rsp, 0x20
0060C43F  pop      rdi
0060C440  ret      
0060C441  mov      rcx, qword ptr [rbx + 8]
0060C445  cmp      rcx, rsi
0060C448  je       0x60c45f  ; -> 0060C45F
0060C44A  mov      eax, dword ptr [rbx]
0060C44C  shr      eax, 0x1f
0060C44F  not      al
0060C451  test     al, 1
0060C453  je       0x60c45f  ; -> 0060C45F
0060C455  test     rcx, rcx
0060C458  je       0x60c45f  ; -> 0060C45F
0060C45A  call     0x584730  ; -> 00584730 fn
0060C45F  mov      qword ptr [rbx + 8], rsi
0060C463  mov      dword ptr [rbx], edi
0060C465  mov      rbx, qword ptr [rsp + 0x30]
0060C46A  xor      eax, eax
0060C46C  mov      rsi, qword ptr [rsp + 0x38]
0060C471  add      rsp, 0x20
0060C475  pop      rdi
0060C476  ret      
```

## 0060F400 (124 B, extent 0060F400-0060F47C)

Documented callee on this page: `00584730`

```
0060F400  mov      qword ptr [rsp + 8], rbx
0060F405  mov      qword ptr [rsp + 0x10], rsi
0060F40A  push     rdi
0060F40B  sub      rsp, 0x20
0060F40F  mov      rax, qword ptr [rcx + 0x18]
0060F413  mov      edi, r9d
0060F416  mov      ecx, dword ptr [rcx + 0x48]
0060F419  mov      rsi, r8
0060F41C  sub      ecx, dword ptr [rax + 0xf4]
0060F422  movsxd   rbx, ecx
0060F425  add      rbx, rdx
0060F428  test     r9d, r9d
0060F42B  jns      0x60f442  ; -> 0060F442
0060F42D  mov      eax, 5
0060F432  mov      rbx, qword ptr [rsp + 0x30]
0060F437  mov      rsi, qword ptr [rsp + 0x38]
0060F43C  add      rsp, 0x20
0060F440  pop      rdi
0060F441  ret      
0060F442  mov      rcx, qword ptr [rbx + 8]
0060F446  mov      eax, dword ptr [rbx]
0060F448  cmp      rcx, rsi
0060F44B  je       0x60f460  ; -> 0060F460
0060F44D  shr      eax, 0x1f
0060F450  not      al
0060F452  test     al, 1
0060F454  je       0x60f460  ; -> 0060F460
0060F456  test     rcx, rcx
0060F459  je       0x60f460  ; -> 0060F460
0060F45B  call     0x584730  ; -> 00584730 fn
0060F460  bts      edi, 0x1f
0060F464  mov      qword ptr [rbx + 8], rsi
0060F468  mov      rsi, qword ptr [rsp + 0x38]
0060F46D  xor      eax, eax
0060F46F  mov      dword ptr [rbx], edi
0060F471  mov      rbx, qword ptr [rsp + 0x30]
0060F476  add      rsp, 0x20
0060F47A  pop      rdi
0060F47B  ret      
```

## 00610AE0 (102 B, extent 00610AE0-00610B46)

Documented callee on this page: `005CDAA0`

```
00610AE0  mov      qword ptr [rsp + 0x10], rsi
00610AE5  push     rdi
00610AE6  sub      rsp, 0x30
00610AEA  mov      rdi, rdx
00610AED  mov      rsi, rcx
00610AF0  test     rdx, rdx
00610AF3  je       0x610b39  ; -> 00610B39
00610AF5  mov      rax, qword ptr [rsp + 0x60]
00610AFA  lea      rdx, [rip + 0x73dc4f]  ; -> 00D4E750
00610B01  mov      qword ptr [rsp + 0x40], rbx
00610B06  mov      ecx, 1
00610B0B  add      qword ptr [rax], 8
00610B0F  mov      rax, qword ptr [rax]
00610B12  mov      rbx, qword ptr [rax - 8]
00610B16  call     0x5cdaa0  ; -> 005CDAA0 fn
00610B1B  movups   xmm0, xmmword ptr [rsp + 0x20]
00610B20  lea      r8, [rsp + 0x20]
00610B25  mov      rdx, rbx
00610B28  mov      rcx, rdi
00610B2B  movdqa   xmmword ptr [rsp + 0x20], xmm0
00610B31  call     qword ptr [rsi + 8]
00610B34  mov      rbx, qword ptr [rsp + 0x40]
00610B39  xor      eax, eax
00610B3B  mov      rsi, qword ptr [rsp + 0x48]
00610B40  add      rsp, 0x30
00610B44  pop      rdi
00610B45  ret      
```

## 006155B0 (355 B, extent 006155B0-00615713)

Documented callee on this page: `005FD050`

```
006155B0  mov      qword ptr [rsp + 8], rbx
006155B5  mov      qword ptr [rsp + 0x10], rsi
006155BA  push     rdi
006155BB  sub      rsp, 0x20
006155BF  mov      rbx, r8
006155C2  mov      qword ptr [rcx + 0x400], rdx
006155C9  xor      edx, edx
006155CB  mov      r8d, 0x400
006155D1  mov      rdi, r9
006155D4  mov      rsi, rcx
006155D7  call     0x861ec0  ; -> 00861EC0 fn
006155DC  lea      rcx, [rsi + 0x408]
006155E3  xor      edx, edx
006155E5  mov      r8d, 0x80
006155EB  mov      qword ptr [rcx + 0x80], rbx
006155F2  call     0x861ec0  ; -> 00861EC0 fn
006155F7  xor      eax, eax
006155F9  mov      qword ptr [rsi + 0x4d0], rdi
00615600  mov      qword ptr [rsi + 0x490], rax
00615607  lea      rcx, [rsi + 0x4d8]
0061560E  mov      qword ptr [rsi + 0x498], rax
00615615  xor      edx, edx
00615617  mov      qword ptr [rsi + 0x4a0], rax
0061561E  mov      r8d, 0x400
00615624  mov      qword ptr [rsi + 0x4a8], rax
0061562B  mov      qword ptr [rsi + 0x4b0], rax
00615632  mov      qword ptr [rsi + 0x4b8], rax
00615639  mov      qword ptr [rsi + 0x4c0], rax
00615640  mov      qword ptr [rsi + 0x4c8], rax
00615647  call     0x861ec0  ; -> 00861EC0 fn
0061564C  lea      rdi, [rsi + 0x8e0]
00615653  mov      qword ptr [rsi + 0x8d8], 0x80
0061565E  mov      rcx, rdi
00615661  xor      edx, edx
00615663  mov      r8d, 0x80
00615669  xor      ebx, ebx
0061566B  call     0x861ec0  ; -> 00861EC0 fn
00615670  mov      qword ptr [rdi + 0x80], 0x10
0061567B  xor      eax, eax
0061567D  mov      qword ptr [rsi + 0x968], rax
00615684  mov      qword ptr [rsi + 0x970], rax
0061568B  mov      qword ptr [rsi + 0x978], rax
00615692  mov      qword ptr [rsi + 0x980], rax
00615699  mov      qword ptr [rsi + 0x988], rax
006156A0  mov      qword ptr [rsi + 0x990], rax
006156A7  mov      qword ptr [rsi + 0x998], rax
006156AE  mov      qword ptr [rsi + 0x9a0], rax
006156B5  mov      qword ptr [rsi + 0x9a8], 8
006156C0  call     0x5fd050  ; -> 005FD050 fn
006156C5  mov      rcx, qword ptr [rax + 0x1840]
006156CC  nop      dword ptr [rax]
006156D0  mov      eax, dword ptr [rdi + 0x80]
006156D6  cmp      ebx, eax
006156D8  cmovl    eax, ebx
006156DB  mov      dword ptr [rdi + 0x80], eax
006156E1  mov      eax, dword ptr [rdi + 0x84]
006156E7  cmp      ebx, eax
006156E9  cmovg    eax, ebx
006156EC  mov      dword ptr [rdi + 0x84], eax
006156F2  movsxd   rax, ebx
006156F5  inc      ebx
006156F7  mov      qword ptr [rdi + rax*8], rcx
006156FB  cmp      ebx, 0x10
006156FE  jb       0x6156d0  ; -> 006156D0
00615700  mov      rbx, qword ptr [rsp + 0x30]
00615705  mov      rax, rsi
00615708  mov      rsi, qword ptr [rsp + 0x38]
0061570D  add      rsp, 0x20
00615711  pop      rdi
00615712  ret      
```
