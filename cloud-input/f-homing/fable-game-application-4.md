# F homing pack (FABLE): `00-Engine-Core-Runtime/Application-Root/game-application.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 16. No bearing page cites them and no documented function calls them directly.

## 006AF910 (82 B, extent 006AF910-006AF962)

Documented callee on this page: `00584730`

```
006AF910  push     rbx
006AF912  sub      rsp, 0x30
006AF916  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006AF91F  mov      rbx, rdx
006AF922  lea      r8, [rdx + 0x18]
006AF926  mov      rcx, qword ptr [r8]
006AF929  mov      rax, qword ptr [r8 + 8]
006AF92D  mov      qword ptr [rcx + 8], rax
006AF931  mov      qword ptr [rax], rcx
006AF934  mov      qword ptr [r8], r8
006AF937  mov      qword ptr [r8 + 8], r8
006AF93B  mov      rcx, qword ptr [rdx + 0x28]
006AF93F  test     rcx, rcx
006AF942  je       0x6af952  ; -> 006AF952
006AF944  mov      eax, ecx
006AF946  not      al
006AF948  test     al, 1
006AF94A  je       0x6af952  ; -> 006AF952
006AF94C  call     0x584730  ; -> 00584730 fn
006AF951  nop      
006AF952  mov      rcx, rbx
006AF955  call     0x6aaa50  ; -> 006AAA50 fn
006AF95A  mov      al, 1
006AF95C  add      rsp, 0x30
006AF960  pop      rbx
006AF961  ret      
```

## 006BC540 (134 B, extent 006BC540-006BC5C6)

Documented callee on this page: `0017D260`

```
006BC540  mov      qword ptr [rsp + 0x10], rsi
006BC545  push     rdi
006BC546  sub      rsp, 0x20
006BC54A  mov      esi, ecx
006BC54C  mov      rdi, rdx
006BC54F  test     ecx, ecx
006BC551  je       0x6bc5b9  ; -> 006BC5B9
006BC553  lea      rcx, [rsi + rsi*2]
006BC557  mov      qword ptr [rsp + 0x30], rbx
006BC55C  shl      rcx, 3
006BC560  mov      edx, 8
006BC565  mov      ebx, esi
006BC567  call     0x17d260  ; -> 0017D260 fn
006BC56C  mov      rdx, rax
006BC56F  test     rax, rax
006BC572  je       0x6bc5a9  ; -> 006BC5A9
006BC574  mov      rcx, rax
006BC577  test     esi, esi
006BC579  je       0x6bc5a9  ; -> 006BC5A9
006BC57B  nop      dword ptr [rax + rax]
006BC580  mov      rax, rcx
006BC583  add      rcx, 0x18
006BC587  test     rax, rax
006BC58A  je       0x6bc5a0  ; -> 006BC5A0
006BC58C  movups   xmm0, xmmword ptr [rdi]
006BC58F  movups   xmmword ptr [rax], xmm0
006BC592  movsd    xmm1, qword ptr [rdi + 0x10]
006BC597  add      rdi, 0x18
006BC59B  movsd    qword ptr [rax + 0x10], xmm1
006BC5A0  sub      rbx, 1
006BC5A4  jne      0x6bc580  ; -> 006BC580
006BC5A6  mov      rax, rdx
006BC5A9  mov      rbx, qword ptr [rsp + 0x30]
006BC5AE  mov      rsi, qword ptr [rsp + 0x38]
006BC5B3  add      rsp, 0x20
006BC5B7  pop      rdi
006BC5B8  ret      
006BC5B9  xor      eax, eax
006BC5BB  mov      rsi, qword ptr [rsp + 0x38]
006BC5C0  add      rsp, 0x20
006BC5C4  pop      rdi
006BC5C5  ret      
```

## 006C0B50 (71 B, extent 006C0B50-006C0B97)

Documented callee on this page: `00584730`

```
006C0B50  push     rbx
006C0B52  sub      rsp, 0x30
006C0B56  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006C0B5F  mov      rbx, rdx
006C0B62  lea      rcx, [rdx + 0x58]
006C0B66  call     0x6167c0  ; -> 006167C0 fn
006C0B6B  nop      
006C0B6C  mov      eax, dword ptr [rbx + 0x10]
006C0B6F  shr      eax, 0x1f
006C0B72  not      al
006C0B74  test     al, 1
006C0B76  je       0x6c0b86  ; -> 006C0B86
006C0B78  mov      rcx, qword ptr [rbx + 0x18]
006C0B7C  test     rcx, rcx
006C0B7F  je       0x6c0b86  ; -> 006C0B86
006C0B81  call     0x584730  ; -> 00584730 fn
006C0B86  xor      eax, eax
006C0B88  mov      qword ptr [rbx + 0x18], rax
006C0B8C  mov      dword ptr [rbx + 0x10], eax
006C0B8F  mov      al, 1
006C0B91  add      rsp, 0x30
006C0B95  pop      rbx
006C0B96  ret      
```

## 006C4B70 (82 B, extent 006C4B70-006C4BC2)

Documented callee on this page: `00584730`

```
006C4B70  push     rbx
006C4B72  sub      rsp, 0x30
006C4B76  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006C4B7F  mov      rbx, rdx
006C4B82  lea      rcx, [rdx + 0x50]
006C4B86  call     0x6c5200  ; -> 006C5200 fn
006C4B8B  nop      
006C4B8C  mov      ecx, dword ptr [rbx + 0x20]
006C4B8F  mov      eax, ecx
006C4B91  shr      eax, 0x1f
006C4B94  not      al
006C4B96  test     al, 1
006C4B98  je       0x6c4bb1  ; -> 006C4BB1
006C4B9A  btr      ecx, 0x1f
006C4B9E  cmp      ecx, 1
006C4BA1  jbe      0x6c4bb1  ; -> 006C4BB1
006C4BA3  mov      rcx, qword ptr [rbx + 0x28]
006C4BA7  test     rcx, rcx
006C4BAA  je       0x6c4bb1  ; -> 006C4BB1
006C4BAC  call     0x584730  ; -> 00584730 fn
006C4BB1  xor      eax, eax
006C4BB3  mov      qword ptr [rbx + 0x28], rax
006C4BB7  mov      dword ptr [rbx + 0x20], eax
006C4BBA  mov      al, 1
006C4BBC  add      rsp, 0x30
006C4BC0  pop      rbx
006C4BC1  ret      
```

## 006C52D0 (69 B, extent 006C52D0-006C5315)

Documented callee on this page: `00584730`

```
006C52D0  push     rbx
006C52D2  sub      rsp, 0x30
006C52D6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006C52DF  mov      rbx, rcx
006C52E2  mov      ecx, dword ptr [rcx]
006C52E4  mov      eax, ecx
006C52E6  shr      eax, 0x1f
006C52E9  not      al
006C52EB  test     al, 1
006C52ED  je       0x6c5307  ; -> 006C5307
006C52EF  btr      ecx, 0x1f
006C52F3  cmp      ecx, 1
006C52F6  jbe      0x6c5307  ; -> 006C5307
006C52F8  mov      rcx, qword ptr [rbx + 8]
006C52FC  test     rcx, rcx
006C52FF  je       0x6c5307  ; -> 006C5307
006C5301  call     0x584730  ; -> 00584730 fn
006C5306  nop      
006C5307  xor      eax, eax
006C5309  mov      dword ptr [rbx], eax
006C530B  mov      qword ptr [rbx + 8], rax
006C530F  add      rsp, 0x30
006C5313  pop      rbx
006C5314  ret      
```

## 006C7D00 (178 B, extent 006C7D00-006C7DB2)

Documented callee on this page: `00584730`

```
006C7D00  mov      qword ptr [rsp + 0x18], rbx
006C7D05  push     rdi
006C7D06  sub      rsp, 0x20
006C7D0A  mov      rdi, rdx
006C7D0D  mov      rbx, rcx
006C7D10  test     r8d, r8d
006C7D13  jns      0x6c7d25  ; -> 006C7D25
006C7D15  mov      eax, 5
006C7D1A  mov      rbx, qword ptr [rsp + 0x40]
006C7D1F  add      rsp, 0x20
006C7D23  pop      rdi
006C7D24  ret      
006C7D25  mov      eax, dword ptr [rcx]
006C7D27  btr      eax, 0x1f
006C7D2B  mov      qword ptr [rsp + 0x30], rsi
006C7D30  mov      qword ptr [rsp + 0x38], r14
006C7D35  cmp      eax, 1
006C7D38  jbe      0x6c7d40  ; -> 006C7D40
006C7D3A  mov      rcx, qword ptr [rcx + 8]
006C7D3E  jmp      0x6c7d4c  ; -> 006C7D4C
006C7D40  test     eax, eax
006C7D42  je       0x6c7d4a  ; -> 006C7D4A
006C7D44  add      rcx, 8
006C7D48  jmp      0x6c7d4c  ; -> 006C7D4C
006C7D4A  xor      ecx, ecx
006C7D4C  mov      esi, r8d
006C7D4F  bts      esi, 0x1f
006C7D53  cmp      r8d, 1
006C7D57  jne      0x6c7d6e  ; -> 006C7D6E
006C7D59  lea      rdx, [rbx + 8]
006C7D5D  test     rdx, rdx
006C7D60  je       0x6c7d66  ; -> 006C7D66
006C7D62  mov      eax, dword ptr [rdi]
006C7D64  mov      dword ptr [rdx], eax
006C7D66  mov      rdi, rdx
006C7D69  mov      esi, 1
006C7D6E  lea      r14, [rbx + 8]
006C7D72  cmp      rcx, rdi
006C7D75  je       0x6c7d91  ; -> 006C7D91
006C7D77  cmp      rcx, r14
006C7D7A  je       0x6c7d91  ; -> 006C7D91
006C7D7C  mov      eax, dword ptr [rbx]
006C7D7E  shr      eax, 0x1f
006C7D81  not      al
006C7D83  test     al, 1
006C7D85  je       0x6c7d91  ; -> 006C7D91
006C7D87  test     rcx, rcx
006C7D8A  je       0x6c7d91  ; -> 006C7D91
006C7D8C  call     0x584730  ; -> 00584730 fn
006C7D91  cmp      rdi, r14
006C7D94  je       0x6c7d99  ; -> 006C7D99
006C7D96  mov      qword ptr [r14], rdi
006C7D99  mov      r14, qword ptr [rsp + 0x38]
006C7D9E  xor      eax, eax
006C7DA0  mov      dword ptr [rbx], esi
006C7DA2  mov      rsi, qword ptr [rsp + 0x30]
006C7DA7  mov      rbx, qword ptr [rsp + 0x40]
006C7DAC  add      rsp, 0x20
006C7DB0  pop      rdi
006C7DB1  ret      
```

## 006C8870 (33 B, extent 006C8870-006C8891)

Documented callee on this page: `0016D6A0`

```
006C8870  lea      rax, [rip + 0x6be0e9]  ; -> 00D86960
006C8877  mov      qword ptr [rcx], rax
006C887A  lea      rax, [rip + 0x6be24f]  ; -> 00D86AD0
006C8881  mov      qword ptr [rcx + 8], rax
006C8885  add      rcx, 0x880
006C888C  jmp      0x16d6a0  ; -> 0016D6A0 fn
```

## 006CC490 (94 B, extent 006CC490-006CC4EE)

Documented callee on this page: `00809054`

```
006CC490  push     rdi
006CC492  sub      rsp, 0x30
006CC496  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006CC49F  mov      qword ptr [rsp + 0x40], rbx
006CC4A4  mov      ebx, edx
006CC4A6  mov      rdi, rcx
006CC4A9  lea      rax, [rip + 0x6bd5d0]  ; -> 00D89A80
006CC4B0  mov      qword ptr [rcx], rax
006CC4B3  add      rcx, 0x60
006CC4B7  lea      r9, [rip - 0xae]  ; -> 006CC410
006CC4BE  mov      edx, 0x20
006CC4C3  lea      r8d, [rdx - 0x1e]
006CC4C7  call     0x809054  ; -> 00809054 fn
006CC4CC  nop      
006CC4CD  test     bl, 1
006CC4D0  je       0x6cc4e0  ; -> 006CC4E0
006CC4D2  mov      edx, 0xa8
006CC4D7  mov      rcx, rdi
006CC4DA  call     0x809950  ; -> 00809950 fn
006CC4DF  nop      
006CC4E0  mov      rax, rdi
006CC4E3  mov      rbx, qword ptr [rsp + 0x40]
006CC4E8  add      rsp, 0x30
006CC4EC  pop      rdi
006CC4ED  ret      
```

## 006CDD30 (80 B, extent 006CDD30-006CDD80)

Documented callee on this page: `00584730`

```
006CDD30  push     rbx
006CDD32  sub      rsp, 0x30
006CDD36  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006CDD3F  mov      rbx, rdx
006CDD42  mov      rcx, qword ptr [rdx + 0x40]
006CDD46  test     rcx, rcx
006CDD49  je       0x6cdd59  ; -> 006CDD59
006CDD4B  mov      eax, ecx
006CDD4D  not      al
006CDD4F  test     al, 1
006CDD51  je       0x6cdd59  ; -> 006CDD59
006CDD53  call     0x584730  ; -> 00584730 fn
006CDD58  nop      
006CDD59  mov      rcx, qword ptr [rbx + 0x28]
006CDD5D  test     rcx, rcx
006CDD60  je       0x6cdd70  ; -> 006CDD70
006CDD62  mov      eax, ecx
006CDD64  not      al
006CDD66  test     al, 1
006CDD68  je       0x6cdd70  ; -> 006CDD70
006CDD6A  call     0x584730  ; -> 00584730 fn
006CDD6F  nop      
006CDD70  mov      rcx, rbx
006CDD73  call     0x6aaa50  ; -> 006AAA50 fn
006CDD78  mov      al, 1
006CDD7A  add      rsp, 0x30
006CDD7E  pop      rbx
006CDD7F  ret      
```

## 006D7380 (674 B, extent 006D7380-006D7622)

Documented callee on this page: `00861EBA`

```
006D7380  sub      rsp, 0x58
006D7384  mov      rax, rcx
006D7387  test     edx, edx
006D7389  je       0x6d761d  ; -> 006D761D
006D738F  movss    xmm3, dword ptr [rcx]
006D7393  xor      r10d, r10d
006D7396  xorps    xmm0, xmm0
006D7399  mov      r11d, r10d
006D739C  ucomiss  xmm3, xmm0
006D739F  jp       0x6d73b0  ; -> 006D73B0
006D73A1  jne      0x6d73b0  ; -> 006D73B0
006D73A3  mov      rcx, qword ptr [rsp + 0x30]
006D73A8  movss    xmm3, dword ptr [rsp + 0x20]
006D73AE  jmp      0x6d73c4  ; -> 006D73C4
006D73B0  mov      rcx, qword ptr [r8]
006D73B3  mov      r11d, 1
006D73B9  mov      qword ptr [rsp + 0x30], rcx
006D73BE  movss    dword ptr [rsp + 0x20], xmm3
006D73C4  movss    xmm1, dword ptr [rax + 4]
006D73C9  ucomiss  xmm1, xmm0
006D73CC  jp       0x6d73d0  ; -> 006D73D0
006D73CE  je       0x6d73f0  ; -> 006D73F0
006D73D0  mov      rax, qword ptr [r8 + 8]
006D73D4  mov      ecx, r11d
006D73D7  inc      r11d
006D73DA  movss    dword ptr [rsp + rcx*4 + 0x20], xmm1
006D73E0  movss    xmm3, dword ptr [rsp + 0x20]
006D73E6  mov      qword ptr [rsp + rcx*8 + 0x30], rax
006D73EB  mov      rcx, qword ptr [rsp + 0x30]
006D73F0  shufps   xmm3, xmm3, 0
006D73F4  lea      r8d, [rdx + rdx]
006D73F8  sub      r11d, 1
006D73FC  je       0x6d7547  ; -> 006D7547
006D7402  sub      r11d, 1
006D7406  je       0x6d7507  ; -> 006D7507
006D740C  sub      r11d, 1
006D7410  je       0x6d74a9  ; -> 006D74A9
006D7416  cmp      r11d, 1
006D741A  je       0x6d742e  ; -> 006D742E
006D741C  mov      rcx, qword ptr [r9]
006D741F  xor      edx, edx
006D7421  shl      r8, 2
006D7425  add      rsp, 0x58
006D7429  jmp      0x861ec0  ; -> 00861EC0 fn
006D742E  mov      rax, qword ptr [r9]
006D7431  mov      r9, qword ptr [rsp + 0x48]
006D7436  mov      rdx, qword ptr [rsp + 0x38]
006D743B  sub      r9, rcx
006D743E  mov      r10, qword ptr [rsp + 0x40]
006D7443  sub      rdx, rcx
006D7446  movss    xmm4, dword ptr [rsp + 0x2c]
006D744C  sub      r10, rcx
006D744F  movss    xmm5, dword ptr [rsp + 0x28]
006D7455  movaps   xmmword ptr [rsp + 0x40], xmm6
006D745A  movss    xmm6, dword ptr [rsp + 0x24]
006D7460  movaps   xmm0, xmm3
006D7463  movaps   xmm2, xmm6
006D7466  mulss    xmm2, dword ptr [rdx + rcx]
006D746B  movaps   xmm1, xmm5
006D746E  mulss    xmm0, dword ptr [rcx]
006D7472  mulss    xmm1, dword ptr [r10 + rcx]
006D7478  addss    xmm2, xmm0
006D747C  movaps   xmm0, xmm4
006D747F  mulss    xmm0, dword ptr [r9 + rcx]
006D7485  add      rcx, 4
006D7489  addss    xmm2, xmm1
006D748D  addss    xmm2, xmm0
006D7491  movss    dword ptr [rax], xmm2
006D7495  add      rax, 4
006D7499  add      r8d, -1
006D749D  jne      0x6d7460  ; -> 006D7460
006D749F  movaps   xmm6, xmmword ptr [rsp + 0x40]
006D74A4  add      rsp, 0x58
006D74A8  ret      
006D74A9  mov      rax, qword ptr [rsp + 0x40]
006D74AE  mov      rdx, qword ptr [r9]
006D74B1  sub      rcx, rax
006D74B4  mov      r9, qword ptr [rsp + 0x38]
006D74B9  movss    xmm4, dword ptr [rsp + 0x28]
006D74BF  sub      r9, rax
006D74C2  movss    xmm5, dword ptr [rsp + 0x24]
006D74C8  nop      dword ptr [rax + rax]
006D74D0  movaps   xmm2, xmm5
006D74D3  movaps   xmm0, xmm3
006D74D6  mulss    xmm2, dword ptr [rax + r9]
006D74DC  movaps   xmm1, xmm4
006D74DF  mulss    xmm0, dword ptr [rax + rcx]
006D74E4  mulss    xmm1, dword ptr [rax]
006D74E8  add      rax, 4
006D74EC  addss    xmm2, xmm0
006D74F0  addss    xmm2, xmm1
006D74F4  movss    dword ptr [rdx], xmm2
006D74F8  add      rdx, 4
006D74FC  add      r8d, -1
006D7500  jne      0x6d74d0  ; -> 006D74D0
006D7502  add      rsp, 0x58
006D7506  ret      
006D7507  mov      rax, qword ptr [r9]
006D750A  mov      rdx, qword ptr [rsp + 0x38]
006D750F  movss    xmm2, dword ptr [rsp + 0x24]
006D7515  sub      rdx, rax
006D7518  sub      rcx, rax
006D751B  nop      dword ptr [rax + rax]
006D7520  movaps   xmm1, xmm2
006D7523  movaps   xmm0, xmm3
006D7526  mulss    xmm1, dword ptr [rdx + rax]
006D752B  mulss    xmm0, dword ptr [rcx + rax]
006D7530  addss    xmm1, xmm0
006D7534  movss    dword ptr [rax], xmm1
006D7538  add      rax, 4
006D753C  add      r8d, -1
006D7540  jne      0x6d7520  ; -> 006D7520
006D7542  add      rsp, 0x58
006D7546  ret      
006D7547  ucomiss  xmm3, dword ptr [rip + 0x161465a]  ; -> 01CEBBA8 [f32 1]
006D754E  movaps   xmm1, xmm3
006D7551  shufps   xmm1, xmm1, 0
006D7555  jp       0x6d756c  ; -> 006D756C
006D7557  jne      0x6d756c  ; -> 006D756C
006D7559  mov      rdx, rcx
006D755C  shl      r8, 2
006D7560  mov      rcx, qword ptr [r9]
006D7563  add      rsp, 0x58
006D7567  jmp      0x861eba  ; -> 00861EBA fn
006D756C  mov      rdx, qword ptr [r9]
006D756F  test     r8d, r8d
006D7572  je       0x6d761d  ; -> 006D761D
006D7578  cmp      r8d, 8
006D757C  jb       0x6d75b5  ; -> 006D75B5
006D757E  mov      eax, r8d
006D7581  and      eax, 0xfffffff8
006D7584  nop      dword ptr [rax]
006D7588  nop      dword ptr [rax + rax]
006D7590  movups   xmm0, xmmword ptr [rcx]
006D7593  add      r10d, 8
006D7597  mulps    xmm0, xmm1
006D759A  movups   xmmword ptr [rdx], xmm0
006D759D  movups   xmm0, xmmword ptr [rcx + 0x10]
006D75A1  add      rcx, 0x20
006D75A5  mulps    xmm0, xmm1
006D75A8  movups   xmmword ptr [rdx + 0x10], xmm0
006D75AC  add      rdx, 0x20
006D75B0  cmp      r10d, eax
006D75B3  jb       0x6d7590  ; -> 006D7590
006D75B5  cmp      r10d, r8d
006D75B8  jae      0x6d761d  ; -> 006D761D
006D75BA  mov      eax, r8d
006D75BD  sub      eax, r10d
006D75C0  cmp      eax, 4
006D75C3  jb       0x6d75f7  ; -> 006D75F7
006D75C5  mov      eax, r8d
006D75C8  sub      eax, r10d
006D75CB  sub      eax, 4
006D75CE  shr      eax, 2
006D75D1  inc      eax
006D75D3  mov      r9d, eax
006D75D6  lea      r10d, [r10 + rax*4]
006D75DA  nop      word ptr [rax + rax]
006D75E0  movups   xmm0, xmmword ptr [rcx]
006D75E3  add      rcx, 0x10
006D75E7  mulps    xmm0, xmm3
006D75EA  movups   xmmword ptr [rdx], xmm0
006D75ED  add      rdx, 0x10
006D75F1  sub      r9, 1
006D75F5  jne      0x6d75e0  ; -> 006D75E0
006D75F7  cmp      r10d, r8d
006D75FA  jae      0x6d761d  ; -> 006D761D
006D75FC  sub      rdx, rcx
006D75FF  sub      r8d, r10d
006D7602  mov      eax, r8d
006D7605  lea      rcx, [rcx + 4]
006D7609  movaps   xmm0, xmm3
006D760C  mulss    xmm0, dword ptr [rcx - 4]
006D7611  movss    dword ptr [rdx + rcx - 4], xmm0
006D7617  sub      rax, 1
006D761B  jne      0x6d7605  ; -> 006D7605
006D761D  add      rsp, 0x58
006D7621  ret      
```

## 006D7630 (674 B, extent 006D7630-006D78D2)

Documented callee on this page: `00861EBA`

```
006D7630  sub      rsp, 0x58
006D7634  mov      rax, rcx
006D7637  test     edx, edx
006D7639  je       0x6d78cd  ; -> 006D78CD
006D763F  movss    xmm3, dword ptr [rcx]
006D7643  xor      r10d, r10d
006D7646  xorps    xmm0, xmm0
006D7649  mov      r11d, r10d
006D764C  ucomiss  xmm3, xmm0
006D764F  jp       0x6d7660  ; -> 006D7660
006D7651  jne      0x6d7660  ; -> 006D7660
006D7653  mov      rcx, qword ptr [rsp + 0x30]
006D7658  movss    xmm3, dword ptr [rsp + 0x20]
006D765E  jmp      0x6d7674  ; -> 006D7674
006D7660  mov      rcx, qword ptr [r8]
006D7663  mov      r11d, 1
006D7669  mov      qword ptr [rsp + 0x30], rcx
006D766E  movss    dword ptr [rsp + 0x20], xmm3
006D7674  movss    xmm1, dword ptr [rax + 4]
006D7679  ucomiss  xmm1, xmm0
006D767C  jp       0x6d7680  ; -> 006D7680
006D767E  je       0x6d76a0  ; -> 006D76A0
006D7680  mov      rax, qword ptr [r8 + 8]
006D7684  mov      ecx, r11d
006D7687  inc      r11d
006D768A  movss    dword ptr [rsp + rcx*4 + 0x20], xmm1
006D7690  movss    xmm3, dword ptr [rsp + 0x20]
006D7696  mov      qword ptr [rsp + rcx*8 + 0x30], rax
006D769B  mov      rcx, qword ptr [rsp + 0x30]
006D76A0  shufps   xmm3, xmm3, 0
006D76A4  lea      r8d, [rdx + rdx*2]
006D76A8  sub      r11d, 1
006D76AC  je       0x6d77f7  ; -> 006D77F7
006D76B2  sub      r11d, 1
006D76B6  je       0x6d77b7  ; -> 006D77B7
006D76BC  sub      r11d, 1
006D76C0  je       0x6d7759  ; -> 006D7759
006D76C6  cmp      r11d, 1
006D76CA  je       0x6d76de  ; -> 006D76DE
006D76CC  mov      rcx, qword ptr [r9]
006D76CF  xor      edx, edx
006D76D1  shl      r8, 2
006D76D5  add      rsp, 0x58
006D76D9  jmp      0x861ec0  ; -> 00861EC0 fn
006D76DE  mov      rax, qword ptr [r9]
006D76E1  mov      r9, qword ptr [rsp + 0x48]
006D76E6  mov      rdx, qword ptr [rsp + 0x38]
006D76EB  sub      r9, rcx
006D76EE  mov      r10, qword ptr [rsp + 0x40]
006D76F3  sub      rdx, rcx
006D76F6  movss    xmm4, dword ptr [rsp + 0x2c]
006D76FC  sub      r10, rcx
006D76FF  movss    xmm5, dword ptr [rsp + 0x28]
006D7705  movaps   xmmword ptr [rsp + 0x40], xmm6
006D770A  movss    xmm6, dword ptr [rsp + 0x24]
006D7710  movaps   xmm0, xmm3
006D7713  movaps   xmm2, xmm6
006D7716  mulss    xmm2, dword ptr [rdx + rcx]
006D771B  movaps   xmm1, xmm5
006D771E  mulss    xmm0, dword ptr [rcx]
006D7722  mulss    xmm1, dword ptr [r10 + rcx]
006D7728  addss    xmm2, xmm0
006D772C  movaps   xmm0, xmm4
006D772F  mulss    xmm0, dword ptr [r9 + rcx]
006D7735  add      rcx, 4
006D7739  addss    xmm2, xmm1
006D773D  addss    xmm2, xmm0
006D7741  movss    dword ptr [rax], xmm2
006D7745  add      rax, 4
006D7749  add      r8d, -1
006D774D  jne      0x6d7710  ; -> 006D7710
006D774F  movaps   xmm6, xmmword ptr [rsp + 0x40]
006D7754  add      rsp, 0x58
006D7758  ret      
006D7759  mov      rax, qword ptr [rsp + 0x40]
006D775E  mov      rdx, qword ptr [r9]
006D7761  sub      rcx, rax
006D7764  mov      r9, qword ptr [rsp + 0x38]
006D7769  movss    xmm4, dword ptr [rsp + 0x28]
006D776F  sub      r9, rax
006D7772  movss    xmm5, dword ptr [rsp + 0x24]
006D7778  nop      dword ptr [rax + rax]
006D7780  movaps   xmm2, xmm5
006D7783  movaps   xmm0, xmm3
006D7786  mulss    xmm2, dword ptr [rax + r9]
006D778C  movaps   xmm1, xmm4
006D778F  mulss    xmm0, dword ptr [rax + rcx]
006D7794  mulss    xmm1, dword ptr [rax]
006D7798  add      rax, 4
006D779C  addss    xmm2, xmm0
006D77A0  addss    xmm2, xmm1
006D77A4  movss    dword ptr [rdx], xmm2
006D77A8  add      rdx, 4
006D77AC  add      r8d, -1
006D77B0  jne      0x6d7780  ; -> 006D7780
006D77B2  add      rsp, 0x58
006D77B6  ret      
006D77B7  mov      rax, qword ptr [r9]
006D77BA  mov      rdx, qword ptr [rsp + 0x38]
006D77BF  movss    xmm2, dword ptr [rsp + 0x24]
006D77C5  sub      rdx, rax
006D77C8  sub      rcx, rax
006D77CB  nop      dword ptr [rax + rax]
006D77D0  movaps   xmm1, xmm2
006D77D3  movaps   xmm0, xmm3
006D77D6  mulss    xmm1, dword ptr [rdx + rax]
006D77DB  mulss    xmm0, dword ptr [rcx + rax]
006D77E0  addss    xmm1, xmm0
006D77E4  movss    dword ptr [rax], xmm1
006D77E8  add      rax, 4
006D77EC  add      r8d, -1
006D77F0  jne      0x6d77d0  ; -> 006D77D0
006D77F2  add      rsp, 0x58
006D77F6  ret      
006D77F7  ucomiss  xmm3, dword ptr [rip + 0x16143aa]  ; -> 01CEBBA8 [f32 1]
006D77FE  movaps   xmm1, xmm3
006D7801  shufps   xmm1, xmm1, 0
006D7805  jp       0x6d781c  ; -> 006D781C
006D7807  jne      0x6d781c  ; -> 006D781C
006D7809  mov      rdx, rcx
006D780C  shl      r8, 2
006D7810  mov      rcx, qword ptr [r9]
006D7813  add      rsp, 0x58
006D7817  jmp      0x861eba  ; -> 00861EBA fn
006D781C  mov      rdx, qword ptr [r9]
006D781F  test     r8d, r8d
006D7822  je       0x6d78cd  ; -> 006D78CD
006D7828  cmp      r8d, 8
006D782C  jb       0x6d7865  ; -> 006D7865
006D782E  mov      eax, r8d
006D7831  and      eax, 0xfffffff8
006D7834  nop      dword ptr [rax]
006D7838  nop      dword ptr [rax + rax]
006D7840  movups   xmm0, xmmword ptr [rcx]
006D7843  add      r10d, 8
006D7847  mulps    xmm0, xmm1
006D784A  movups   xmmword ptr [rdx], xmm0
006D784D  movups   xmm0, xmmword ptr [rcx + 0x10]
006D7851  add      rcx, 0x20
006D7855  mulps    xmm0, xmm1
006D7858  movups   xmmword ptr [rdx + 0x10], xmm0
006D785C  add      rdx, 0x20
006D7860  cmp      r10d, eax
006D7863  jb       0x6d7840  ; -> 006D7840
006D7865  cmp      r10d, r8d
006D7868  jae      0x6d78cd  ; -> 006D78CD
006D786A  mov      eax, r8d
006D786D  sub      eax, r10d
006D7870  cmp      eax, 4
006D7873  jb       0x6d78a7  ; -> 006D78A7
006D7875  mov      eax, r8d
006D7878  sub      eax, r10d
006D787B  sub      eax, 4
006D787E  shr      eax, 2
006D7881  inc      eax
006D7883  mov      r9d, eax
006D7886  lea      r10d, [r10 + rax*4]
006D788A  nop      word ptr [rax + rax]
006D7890  movups   xmm0, xmmword ptr [rcx]
006D7893  add      rcx, 0x10
006D7897  mulps    xmm0, xmm3
006D789A  movups   xmmword ptr [rdx], xmm0
006D789D  add      rdx, 0x10
006D78A1  sub      r9, 1
006D78A5  jne      0x6d7890  ; -> 006D7890
006D78A7  cmp      r10d, r8d
006D78AA  jae      0x6d78cd  ; -> 006D78CD
006D78AC  sub      rdx, rcx
006D78AF  sub      r8d, r10d
006D78B2  mov      eax, r8d
006D78B5  lea      rcx, [rcx + 4]
006D78B9  movaps   xmm0, xmm3
006D78BC  mulss    xmm0, dword ptr [rcx - 4]
006D78C1  movss    dword ptr [rdx + rcx - 4], xmm0
006D78C7  sub      rax, 1
006D78CB  jne      0x6d78b5  ; -> 006D78B5
006D78CD  add      rsp, 0x58
006D78D1  ret      
```

## 006D78E0 (690 B, extent 006D78E0-006D7B92)

Documented callee on this page: `00861EBA`

```
006D78E0  sub      rsp, 0x58
006D78E4  mov      rax, rcx
006D78E7  test     edx, edx
006D78E9  je       0x6d7b8d  ; -> 006D7B8D
006D78EF  movss    xmm3, dword ptr [rcx]
006D78F3  xor      r10d, r10d
006D78F6  xorps    xmm0, xmm0
006D78F9  mov      r11d, r10d
006D78FC  ucomiss  xmm3, xmm0
006D78FF  jp       0x6d7910  ; -> 006D7910
006D7901  jne      0x6d7910  ; -> 006D7910
006D7903  mov      rcx, qword ptr [rsp + 0x30]
006D7908  movss    xmm3, dword ptr [rsp + 0x20]
006D790E  jmp      0x6d7924  ; -> 006D7924
006D7910  mov      rcx, qword ptr [r8]
006D7913  mov      r11d, 1
006D7919  mov      qword ptr [rsp + 0x30], rcx
006D791E  movss    dword ptr [rsp + 0x20], xmm3
006D7924  movss    xmm1, dword ptr [rax + 4]
006D7929  ucomiss  xmm1, xmm0
006D792C  jp       0x6d7930  ; -> 006D7930
006D792E  je       0x6d7950  ; -> 006D7950
006D7930  mov      rax, qword ptr [r8 + 8]
006D7934  mov      ecx, r11d
006D7937  inc      r11d
006D793A  movss    dword ptr [rsp + rcx*4 + 0x20], xmm1
006D7940  movss    xmm3, dword ptr [rsp + 0x20]
006D7946  mov      qword ptr [rsp + rcx*8 + 0x30], rax
006D794B  mov      rcx, qword ptr [rsp + 0x30]
006D7950  shufps   xmm3, xmm3, 0
006D7954  lea      r8d, [rdx*4]
006D795C  sub      r11d, 1
006D7960  je       0x6d7ab7  ; -> 006D7AB7
006D7966  sub      r11d, 1
006D796A  je       0x6d7a77  ; -> 006D7A77
006D7970  sub      r11d, 1
006D7974  je       0x6d7a19  ; -> 006D7A19
006D797A  cmp      r11d, 1
006D797E  je       0x6d7992  ; -> 006D7992
006D7980  mov      rcx, qword ptr [r9]
006D7983  xor      edx, edx
006D7985  shl      r8, 2
006D7989  add      rsp, 0x58
006D798D  jmp      0x861ec0  ; -> 00861EC0 fn
006D7992  mov      rax, qword ptr [r9]
006D7995  mov      r9, qword ptr [rsp + 0x48]
006D799A  mov      rdx, qword ptr [rsp + 0x38]
006D799F  sub      r9, rcx
006D79A2  mov      r10, qword ptr [rsp + 0x40]
006D79A7  sub      rdx, rcx
006D79AA  movss    xmm4, dword ptr [rsp + 0x2c]
006D79B0  sub      r10, rcx
006D79B3  movss    xmm5, dword ptr [rsp + 0x28]
006D79B9  movaps   xmmword ptr [rsp + 0x40], xmm6
006D79BE  movss    xmm6, dword ptr [rsp + 0x24]
006D79C4  nop      dword ptr [rax]
006D79C8  nop      dword ptr [rax + rax]
006D79D0  movaps   xmm0, xmm3
006D79D3  movaps   xmm2, xmm6
006D79D6  mulss    xmm2, dword ptr [rdx + rcx]
006D79DB  movaps   xmm1, xmm5
006D79DE  mulss    xmm0, dword ptr [rcx]
006D79E2  mulss    xmm1, dword ptr [r10 + rcx]
006D79E8  addss    xmm2, xmm0
006D79EC  movaps   xmm0, xmm4
006D79EF  mulss    xmm0, dword ptr [r9 + rcx]
006D79F5  add      rcx, 4
006D79F9  addss    xmm2, xmm1
006D79FD  addss    xmm2, xmm0
006D7A01  movss    dword ptr [rax], xmm2
006D7A05  add      rax, 4
006D7A09  add      r8d, -1
006D7A0D  jne      0x6d79d0  ; -> 006D79D0
006D7A0F  movaps   xmm6, xmmword ptr [rsp + 0x40]
006D7A14  add      rsp, 0x58
006D7A18  ret      
006D7A19  mov      rax, qword ptr [rsp + 0x40]
006D7A1E  mov      rdx, qword ptr [r9]
006D7A21  sub      rcx, rax
006D7A24  mov      r9, qword ptr [rsp + 0x38]
006D7A29  movss    xmm4, dword ptr [rsp + 0x28]
006D7A2F  sub      r9, rax
006D7A32  movss    xmm5, dword ptr [rsp + 0x24]
006D7A38  nop      dword ptr [rax + rax]
006D7A40  movaps   xmm2, xmm5
006D7A43  movaps   xmm0, xmm3
006D7A46  mulss    xmm2, dword ptr [rax + r9]
006D7A4C  movaps   xmm1, xmm4
006D7A4F  mulss    xmm0, dword ptr [rax + rcx]
006D7A54  mulss    xmm1, dword ptr [rax]
006D7A58  add      rax, 4
006D7A5C  addss    xmm2, xmm0
006D7A60  addss    xmm2, xmm1
006D7A64  movss    dword ptr [rdx], xmm2
006D7A68  add      rdx, 4
006D7A6C  add      r8d, -1
006D7A70  jne      0x6d7a40  ; -> 006D7A40
006D7A72  add      rsp, 0x58
006D7A76  ret      
006D7A77  mov      rax, qword ptr [r9]
006D7A7A  mov      rdx, qword ptr [rsp + 0x38]
006D7A7F  movss    xmm2, dword ptr [rsp + 0x24]
006D7A85  sub      rdx, rax
006D7A88  sub      rcx, rax
006D7A8B  nop      dword ptr [rax + rax]
006D7A90  movaps   xmm1, xmm2
006D7A93  movaps   xmm0, xmm3
006D7A96  mulss    xmm1, dword ptr [rdx + rax]
006D7A9B  mulss    xmm0, dword ptr [rcx + rax]
006D7AA0  addss    xmm1, xmm0
006D7AA4  movss    dword ptr [rax], xmm1
006D7AA8  add      rax, 4
006D7AAC  add      r8d, -1
006D7AB0  jne      0x6d7a90  ; -> 006D7A90
006D7AB2  add      rsp, 0x58
006D7AB6  ret      
006D7AB7  ucomiss  xmm3, dword ptr [rip + 0x16140ea]  ; -> 01CEBBA8 [f32 1]
006D7ABE  movaps   xmm1, xmm3
006D7AC1  shufps   xmm1, xmm1, 0
006D7AC5  jp       0x6d7adc  ; -> 006D7ADC
006D7AC7  jne      0x6d7adc  ; -> 006D7ADC
006D7AC9  mov      rdx, rcx
006D7ACC  shl      r8, 2
006D7AD0  mov      rcx, qword ptr [r9]
006D7AD3  add      rsp, 0x58
006D7AD7  jmp      0x861eba  ; -> 00861EBA fn
006D7ADC  mov      rdx, qword ptr [r9]
006D7ADF  test     r8d, r8d
006D7AE2  je       0x6d7b8d  ; -> 006D7B8D
006D7AE8  cmp      r8d, 8
006D7AEC  jb       0x6d7b25  ; -> 006D7B25
006D7AEE  mov      eax, r8d
006D7AF1  and      eax, 0xfffffff8
006D7AF4  nop      dword ptr [rax]
006D7AF8  nop      dword ptr [rax + rax]
006D7B00  movups   xmm0, xmmword ptr [rcx]
006D7B03  add      r10d, 8
006D7B07  mulps    xmm0, xmm1
006D7B0A  movups   xmmword ptr [rdx], xmm0
006D7B0D  movups   xmm0, xmmword ptr [rcx + 0x10]
006D7B11  add      rcx, 0x20
006D7B15  mulps    xmm0, xmm1
006D7B18  movups   xmmword ptr [rdx + 0x10], xmm0
006D7B1C  add      rdx, 0x20
006D7B20  cmp      r10d, eax
006D7B23  jb       0x6d7b00  ; -> 006D7B00
006D7B25  cmp      r10d, r8d
006D7B28  jae      0x6d7b8d  ; -> 006D7B8D
006D7B2A  mov      eax, r8d
006D7B2D  sub      eax, r10d
006D7B30  cmp      eax, 4
006D7B33  jb       0x6d7b67  ; -> 006D7B67
006D7B35  mov      eax, r8d
006D7B38  sub      eax, r10d
006D7B3B  sub      eax, 4
006D7B3E  shr      eax, 2
006D7B41  inc      eax
006D7B43  mov      r9d, eax
006D7B46  lea      r10d, [r10 + rax*4]
006D7B4A  nop      word ptr [rax + rax]
006D7B50  movups   xmm0, xmmword ptr [rcx]
006D7B53  add      rcx, 0x10
006D7B57  mulps    xmm0, xmm3
006D7B5A  movups   xmmword ptr [rdx], xmm0
006D7B5D  add      rdx, 0x10
006D7B61  sub      r9, 1
006D7B65  jne      0x6d7b50  ; -> 006D7B50
006D7B67  cmp      r10d, r8d
006D7B6A  jae      0x6d7b8d  ; -> 006D7B8D
006D7B6C  sub      rdx, rcx
006D7B6F  sub      r8d, r10d
006D7B72  mov      eax, r8d
006D7B75  lea      rcx, [rcx + 4]
006D7B79  movaps   xmm0, xmm3
006D7B7C  mulss    xmm0, dword ptr [rcx - 4]
006D7B81  movss    dword ptr [rdx + rcx - 4], xmm0
006D7B87  sub      rax, 1
006D7B8B  jne      0x6d7b75  ; -> 006D7B75
006D7B8D  add      rsp, 0x58
006D7B91  ret      
```

## 006D7BA0 (756 B, extent 006D7BA0-006D7E94)

Documented callee on this page: `00861EBA`

```
006D7BA0  test     edx, edx
006D7BA2  je       0x6d7e93  ; -> 006D7E93
006D7BA8  mov      qword ptr [rsp + 8], rbx
006D7BAD  push     rbp
006D7BAE  mov      rbp, rsp
006D7BB1  sub      rsp, 0x60
006D7BB5  mov      rax, qword ptr [rip + 0x186cc74]  ; -> 01F44830 [u64 0x00002B992DDFA232]
006D7BBC  xor      rax, rsp
006D7BBF  mov      qword ptr [rbp - 0x18], rax
006D7BC3  movss    xmm3, dword ptr [rcx]
006D7BC7  xor      r10d, r10d
006D7BCA  xorps    xmm0, xmm0
006D7BCD  mov      r11, r9
006D7BD0  ucomiss  xmm3, xmm0
006D7BD3  mov      rbx, rcx
006D7BD6  mov      r9d, r10d
006D7BD9  jp       0x6d7be8  ; -> 006D7BE8
006D7BDB  jne      0x6d7be8  ; -> 006D7BE8
006D7BDD  mov      rcx, qword ptr [rbp - 0x30]
006D7BE1  movss    xmm3, dword ptr [rbp - 0x40]
006D7BE6  jmp      0x6d7bfa  ; -> 006D7BFA
006D7BE8  mov      rcx, qword ptr [r8]
006D7BEB  mov      r9d, 1
006D7BF1  mov      qword ptr [rbp - 0x30], rcx
006D7BF5  movss    dword ptr [rbp - 0x40], xmm3
006D7BFA  movss    xmm1, dword ptr [rbx + 4]
006D7BFF  ucomiss  xmm1, xmm0
006D7C02  jp       0x6d7c06  ; -> 006D7C06
006D7C04  je       0x6d7c24  ; -> 006D7C24
006D7C06  mov      rax, qword ptr [r8 + 8]
006D7C0A  mov      ecx, r9d
006D7C0D  inc      r9d
006D7C10  movss    dword ptr [rbp + rcx*4 - 0x40], xmm1
006D7C16  movss    xmm3, dword ptr [rbp - 0x40]
006D7C1B  mov      qword ptr [rbp + rcx*8 - 0x30], rax
006D7C20  mov      rcx, qword ptr [rbp - 0x30]
006D7C24  movss    xmm1, dword ptr [rbx + 8]
006D7C29  ucomiss  xmm1, xmm0
006D7C2C  jp       0x6d7c30  ; -> 006D7C30
006D7C2E  je       0x6d7c4e  ; -> 006D7C4E
006D7C30  mov      rax, qword ptr [r8 + 0x10]
006D7C34  mov      ecx, r9d
006D7C37  inc      r9d
006D7C3A  movss    dword ptr [rbp + rcx*4 - 0x40], xmm1
006D7C40  movss    xmm3, dword ptr [rbp - 0x40]
006D7C45  mov      qword ptr [rbp + rcx*8 - 0x30], rax
006D7C4A  mov      rcx, qword ptr [rbp - 0x30]
006D7C4E  shufps   xmm3, xmm3, 0
006D7C52  lea      r8d, [rdx + rdx]
006D7C56  sub      r9d, 1
006D7C5A  je       0x6d7da7  ; -> 006D7DA7
006D7C60  sub      r9d, 1
006D7C64  je       0x6d7d67  ; -> 006D7D67
006D7C6A  sub      r9d, 1
006D7C6E  je       0x6d7d09  ; -> 006D7D09
006D7C74  cmp      r9d, 1
006D7C78  je       0x6d7c8d  ; -> 006D7C8D
006D7C7A  mov      rcx, qword ptr [r11]
006D7C7D  xor      edx, edx
006D7C7F  shl      r8, 2
006D7C83  call     0x861ec0  ; -> 00861EC0 fn
006D7C88  jmp      0x6d7e7d  ; -> 006D7E7D
006D7C8D  mov      rdx, qword ptr [rbp - 0x28]
006D7C91  mov      r9, qword ptr [rbp - 0x18]
006D7C95  sub      rdx, rcx
006D7C98  mov      r10, qword ptr [rbp - 0x20]
006D7C9C  sub      r9, rcx
006D7C9F  mov      rax, qword ptr [r11]
006D7CA2  sub      r10, rcx
006D7CA5  movss    xmm4, dword ptr [rbp - 0x34]
006D7CAA  movss    xmm5, dword ptr [rbp - 0x38]
006D7CAF  movaps   xmmword ptr [rsp + 0x50], xmm6
006D7CB4  movss    xmm6, dword ptr [rbp - 0x3c]
006D7CB9  nop      dword ptr [rax]
006D7CC0  movaps   xmm0, xmm3
006D7CC3  movaps   xmm2, xmm6
006D7CC6  mulss    xmm2, dword ptr [rdx + rcx]
006D7CCB  movaps   xmm1, xmm5
006D7CCE  mulss    xmm0, dword ptr [rcx]
006D7CD2  mulss    xmm1, dword ptr [r10 + rcx]
006D7CD8  addss    xmm2, xmm0
006D7CDC  movaps   xmm0, xmm4
006D7CDF  mulss    xmm0, dword ptr [r9 + rcx]
006D7CE5  add      rcx, 4
006D7CE9  addss    xmm2, xmm1
006D7CED  addss    xmm2, xmm0
006D7CF1  movss    dword ptr [rax], xmm2
006D7CF5  add      rax, 4
006D7CF9  add      r8d, -1
006D7CFD  jne      0x6d7cc0  ; -> 006D7CC0
006D7CFF  movaps   xmm6, xmmword ptr [rsp + 0x50]
006D7D04  jmp      0x6d7e7d  ; -> 006D7E7D
006D7D09  mov      rax, qword ptr [rbp - 0x20]
006D7D0D  mov      r9, qword ptr [rbp - 0x28]
006D7D11  sub      rcx, rax
006D7D14  mov      rdx, qword ptr [r11]
006D7D17  sub      r9, rax
006D7D1A  movss    xmm4, dword ptr [rbp - 0x38]
006D7D1F  movss    xmm5, dword ptr [rbp - 0x3c]
006D7D24  nop      dword ptr [rax]
006D7D28  nop      dword ptr [rax + rax]
006D7D30  movaps   xmm2, xmm3
006D7D33  movaps   xmm0, xmm5
006D7D36  mulss    xmm2, dword ptr [rax + rcx]
006D7D3B  movaps   xmm1, xmm4
006D7D3E  mulss    xmm0, dword ptr [rax + r9]
006D7D44  mulss    xmm1, dword ptr [rax]
006D7D48  add      rax, 4
006D7D4C  addss    xmm2, xmm0
006D7D50  addss    xmm2, xmm1
006D7D54  movss    dword ptr [rdx], xmm2
006D7D58  add      rdx, 4
006D7D5C  add      r8d, -1
006D7D60  jne      0x6d7d30  ; -> 006D7D30
006D7D62  jmp      0x6d7e7d  ; -> 006D7E7D
006D7D67  mov      rax, qword ptr [r11]
006D7D6A  mov      rdx, qword ptr [rbp - 0x28]
006D7D6E  movss    xmm2, dword ptr [rbp - 0x3c]
006D7D73  sub      rdx, rax
006D7D76  sub      rcx, rax
006D7D79  nop      dword ptr [rax]
006D7D80  movaps   xmm1, xmm3
006D7D83  movaps   xmm0, xmm2
006D7D86  mulss    xmm1, dword ptr [rcx + rax]
006D7D8B  mulss    xmm0, dword ptr [rdx + rax]
006D7D90  addss    xmm1, xmm0
006D7D94  movss    dword ptr [rax], xmm1
006D7D98  add      rax, 4
006D7D9C  add      r8d, -1
006D7DA0  jne      0x6d7d80  ; -> 006D7D80
006D7DA2  jmp      0x6d7e7d  ; -> 006D7E7D
006D7DA7  ucomiss  xmm3, dword ptr [rip + 0x1613dfa]  ; -> 01CEBBA8 [f32 1]
006D7DAE  movaps   xmm1, xmm3
006D7DB1  shufps   xmm1, xmm1, 0
006D7DB5  jp       0x6d7dcd  ; -> 006D7DCD
006D7DB7  jne      0x6d7dcd  ; -> 006D7DCD
006D7DB9  mov      rdx, rcx
006D7DBC  shl      r8, 2
006D7DC0  mov      rcx, qword ptr [r11]
006D7DC3  call     0x861eba  ; -> 00861EBA fn
006D7DC8  jmp      0x6d7e7d  ; -> 006D7E7D
006D7DCD  mov      rdx, qword ptr [r11]
006D7DD0  test     r8d, r8d
006D7DD3  je       0x6d7e7d  ; -> 006D7E7D
006D7DD9  cmp      r8d, 8
006D7DDD  jb       0x6d7e15  ; -> 006D7E15
006D7DDF  mov      eax, r8d
006D7DE2  and      eax, 0xfffffff8
006D7DE5  nop      word ptr [rax + rax]
006D7DF0  movups   xmm0, xmmword ptr [rcx]
006D7DF3  add      r10d, 8
006D7DF7  mulps    xmm0, xmm1
006D7DFA  movups   xmmword ptr [rdx], xmm0
006D7DFD  movups   xmm0, xmmword ptr [rcx + 0x10]
006D7E01  add      rcx, 0x20
006D7E05  mulps    xmm0, xmm1
006D7E08  movups   xmmword ptr [rdx + 0x10], xmm0
006D7E0C  add      rdx, 0x20
006D7E10  cmp      r10d, eax
006D7E13  jb       0x6d7df0  ; -> 006D7DF0
006D7E15  cmp      r10d, r8d
006D7E18  jae      0x6d7e7d  ; -> 006D7E7D
006D7E1A  mov      eax, r8d
006D7E1D  sub      eax, r10d
006D7E20  cmp      eax, 4
006D7E23  jb       0x6d7e57  ; -> 006D7E57
006D7E25  mov      eax, r8d
006D7E28  sub      eax, r10d
006D7E2B  sub      eax, 4
006D7E2E  shr      eax, 2
006D7E31  inc      eax
006D7E33  mov      r9d, eax
006D7E36  lea      r10d, [r10 + rax*4]
006D7E3A  nop      word ptr [rax + rax]
006D7E40  movups   xmm0, xmmword ptr [rcx]
006D7E43  add      rcx, 0x10
006D7E47  mulps    xmm0, xmm3
006D7E4A  movups   xmmword ptr [rdx], xmm0
006D7E4D  add      rdx, 0x10
006D7E51  sub      r9, 1
006D7E55  jne      0x6d7e40  ; -> 006D7E40
006D7E57  cmp      r10d, r8d
006D7E5A  jae      0x6d7e7d  ; -> 006D7E7D
006D7E5C  sub      rdx, rcx
006D7E5F  sub      r8d, r10d
006D7E62  mov      eax, r8d
006D7E65  lea      rcx, [rcx + 4]
006D7E69  movaps   xmm0, xmm3
006D7E6C  mulss    xmm0, dword ptr [rcx - 4]
006D7E71  movss    dword ptr [rdx + rcx - 4], xmm0
006D7E77  sub      rax, 1
006D7E7B  jne      0x6d7e65  ; -> 006D7E65
006D7E7D  mov      rcx, qword ptr [rbp - 0x18]
006D7E81  xor      rcx, rsp
006D7E84  call     0x808c40  ; -> 00808C40 fn
006D7E89  mov      rbx, qword ptr [rsp + 0x70]
006D7E8E  add      rsp, 0x60
006D7E92  pop      rbp
006D7E93  ret      
```

## 006D7EA0 (756 B, extent 006D7EA0-006D8194)

Documented callee on this page: `00861EBA`

```
006D7EA0  test     edx, edx
006D7EA2  je       0x6d8193  ; -> 006D8193
006D7EA8  mov      qword ptr [rsp + 8], rbx
006D7EAD  push     rbp
006D7EAE  mov      rbp, rsp
006D7EB1  sub      rsp, 0x60
006D7EB5  mov      rax, qword ptr [rip + 0x186c974]  ; -> 01F44830 [u64 0x00002B992DDFA232]
006D7EBC  xor      rax, rsp
006D7EBF  mov      qword ptr [rbp - 0x18], rax
006D7EC3  movss    xmm3, dword ptr [rcx]
006D7EC7  xor      r10d, r10d
006D7ECA  xorps    xmm0, xmm0
006D7ECD  mov      r11, r9
006D7ED0  ucomiss  xmm3, xmm0
006D7ED3  mov      rbx, rcx
006D7ED6  mov      r9d, r10d
006D7ED9  jp       0x6d7ee8  ; -> 006D7EE8
006D7EDB  jne      0x6d7ee8  ; -> 006D7EE8
006D7EDD  mov      rcx, qword ptr [rbp - 0x30]
006D7EE1  movss    xmm3, dword ptr [rbp - 0x40]
006D7EE6  jmp      0x6d7efa  ; -> 006D7EFA
006D7EE8  mov      rcx, qword ptr [r8]
006D7EEB  mov      r9d, 1
006D7EF1  mov      qword ptr [rbp - 0x30], rcx
006D7EF5  movss    dword ptr [rbp - 0x40], xmm3
006D7EFA  movss    xmm1, dword ptr [rbx + 4]
006D7EFF  ucomiss  xmm1, xmm0
006D7F02  jp       0x6d7f06  ; -> 006D7F06
006D7F04  je       0x6d7f24  ; -> 006D7F24
006D7F06  mov      rax, qword ptr [r8 + 8]
006D7F0A  mov      ecx, r9d
006D7F0D  inc      r9d
006D7F10  movss    dword ptr [rbp + rcx*4 - 0x40], xmm1
006D7F16  movss    xmm3, dword ptr [rbp - 0x40]
006D7F1B  mov      qword ptr [rbp + rcx*8 - 0x30], rax
006D7F20  mov      rcx, qword ptr [rbp - 0x30]
006D7F24  movss    xmm1, dword ptr [rbx + 8]
006D7F29  ucomiss  xmm1, xmm0
006D7F2C  jp       0x6d7f30  ; -> 006D7F30
006D7F2E  je       0x6d7f4e  ; -> 006D7F4E
006D7F30  mov      rax, qword ptr [r8 + 0x10]
006D7F34  mov      ecx, r9d
006D7F37  inc      r9d
006D7F3A  movss    dword ptr [rbp + rcx*4 - 0x40], xmm1
006D7F40  movss    xmm3, dword ptr [rbp - 0x40]
006D7F45  mov      qword ptr [rbp + rcx*8 - 0x30], rax
006D7F4A  mov      rcx, qword ptr [rbp - 0x30]
006D7F4E  shufps   xmm3, xmm3, 0
006D7F52  lea      r8d, [rdx + rdx*2]
006D7F56  sub      r9d, 1
006D7F5A  je       0x6d80a7  ; -> 006D80A7
006D7F60  sub      r9d, 1
006D7F64  je       0x6d8067  ; -> 006D8067
006D7F6A  sub      r9d, 1
006D7F6E  je       0x6d8009  ; -> 006D8009
006D7F74  cmp      r9d, 1
006D7F78  je       0x6d7f8d  ; -> 006D7F8D
006D7F7A  mov      rcx, qword ptr [r11]
006D7F7D  xor      edx, edx
006D7F7F  shl      r8, 2
006D7F83  call     0x861ec0  ; -> 00861EC0 fn
006D7F88  jmp      0x6d817d  ; -> 006D817D
006D7F8D  mov      rdx, qword ptr [rbp - 0x28]
006D7F91  mov      r9, qword ptr [rbp - 0x18]
006D7F95  sub      rdx, rcx
006D7F98  mov      r10, qword ptr [rbp - 0x20]
006D7F9C  sub      r9, rcx
006D7F9F  mov      rax, qword ptr [r11]
006D7FA2  sub      r10, rcx
006D7FA5  movss    xmm4, dword ptr [rbp - 0x34]
006D7FAA  movss    xmm5, dword ptr [rbp - 0x38]
006D7FAF  movaps   xmmword ptr [rsp + 0x50], xmm6
006D7FB4  movss    xmm6, dword ptr [rbp - 0x3c]
006D7FB9  nop      dword ptr [rax]
006D7FC0  movaps   xmm0, xmm3
006D7FC3  movaps   xmm2, xmm6
006D7FC6  mulss    xmm2, dword ptr [rdx + rcx]
006D7FCB  movaps   xmm1, xmm5
006D7FCE  mulss    xmm0, dword ptr [rcx]
006D7FD2  mulss    xmm1, dword ptr [r10 + rcx]
006D7FD8  addss    xmm2, xmm0
006D7FDC  movaps   xmm0, xmm4
006D7FDF  mulss    xmm0, dword ptr [r9 + rcx]
006D7FE5  add      rcx, 4
006D7FE9  addss    xmm2, xmm1
006D7FED  addss    xmm2, xmm0
006D7FF1  movss    dword ptr [rax], xmm2
006D7FF5  add      rax, 4
006D7FF9  add      r8d, -1
006D7FFD  jne      0x6d7fc0  ; -> 006D7FC0
006D7FFF  movaps   xmm6, xmmword ptr [rsp + 0x50]
006D8004  jmp      0x6d817d  ; -> 006D817D
006D8009  mov      rax, qword ptr [rbp - 0x20]
006D800D  mov      r9, qword ptr [rbp - 0x28]
006D8011  sub      rcx, rax
006D8014  mov      rdx, qword ptr [r11]
006D8017  sub      r9, rax
006D801A  movss    xmm4, dword ptr [rbp - 0x38]
006D801F  movss    xmm5, dword ptr [rbp - 0x3c]
006D8024  nop      dword ptr [rax]
006D8028  nop      dword ptr [rax + rax]
006D8030  movaps   xmm2, xmm3
006D8033  movaps   xmm0, xmm5
006D8036  mulss    xmm2, dword ptr [rax + rcx]
006D803B  movaps   xmm1, xmm4
006D803E  mulss    xmm0, dword ptr [rax + r9]
006D8044  mulss    xmm1, dword ptr [rax]
006D8048  add      rax, 4
006D804C  addss    xmm2, xmm0
006D8050  addss    xmm2, xmm1
006D8054  movss    dword ptr [rdx], xmm2
006D8058  add      rdx, 4
006D805C  add      r8d, -1
006D8060  jne      0x6d8030  ; -> 006D8030
006D8062  jmp      0x6d817d  ; -> 006D817D
006D8067  mov      rax, qword ptr [r11]
006D806A  mov      rdx, qword ptr [rbp - 0x28]
006D806E  movss    xmm2, dword ptr [rbp - 0x3c]
006D8073  sub      rdx, rax
006D8076  sub      rcx, rax
006D8079  nop      dword ptr [rax]
006D8080  movaps   xmm1, xmm3
006D8083  movaps   xmm0, xmm2
006D8086  mulss    xmm1, dword ptr [rcx + rax]
006D808B  mulss    xmm0, dword ptr [rdx + rax]
006D8090  addss    xmm1, xmm0
006D8094  movss    dword ptr [rax], xmm1
006D8098  add      rax, 4
006D809C  add      r8d, -1
006D80A0  jne      0x6d8080  ; -> 006D8080
006D80A2  jmp      0x6d817d  ; -> 006D817D
006D80A7  ucomiss  xmm3, dword ptr [rip + 0x1613afa]  ; -> 01CEBBA8 [f32 1]
006D80AE  movaps   xmm1, xmm3
006D80B1  shufps   xmm1, xmm1, 0
006D80B5  jp       0x6d80cd  ; -> 006D80CD
006D80B7  jne      0x6d80cd  ; -> 006D80CD
006D80B9  mov      rdx, rcx
006D80BC  shl      r8, 2
006D80C0  mov      rcx, qword ptr [r11]
006D80C3  call     0x861eba  ; -> 00861EBA fn
006D80C8  jmp      0x6d817d  ; -> 006D817D
006D80CD  mov      rdx, qword ptr [r11]
006D80D0  test     r8d, r8d
006D80D3  je       0x6d817d  ; -> 006D817D
006D80D9  cmp      r8d, 8
006D80DD  jb       0x6d8115  ; -> 006D8115
006D80DF  mov      eax, r8d
006D80E2  and      eax, 0xfffffff8
006D80E5  nop      word ptr [rax + rax]
006D80F0  movups   xmm0, xmmword ptr [rcx]
006D80F3  add      r10d, 8
006D80F7  mulps    xmm0, xmm1
006D80FA  movups   xmmword ptr [rdx], xmm0
006D80FD  movups   xmm0, xmmword ptr [rcx + 0x10]
006D8101  add      rcx, 0x20
006D8105  mulps    xmm0, xmm1
006D8108  movups   xmmword ptr [rdx + 0x10], xmm0
006D810C  add      rdx, 0x20
006D8110  cmp      r10d, eax
006D8113  jb       0x6d80f0  ; -> 006D80F0
006D8115  cmp      r10d, r8d
006D8118  jae      0x6d817d  ; -> 006D817D
006D811A  mov      eax, r8d
006D811D  sub      eax, r10d
006D8120  cmp      eax, 4
006D8123  jb       0x6d8157  ; -> 006D8157
006D8125  mov      eax, r8d
006D8128  sub      eax, r10d
006D812B  sub      eax, 4
006D812E  shr      eax, 2
006D8131  inc      eax
006D8133  mov      r9d, eax
006D8136  lea      r10d, [r10 + rax*4]
006D813A  nop      word ptr [rax + rax]
006D8140  movups   xmm0, xmmword ptr [rcx]
006D8143  add      rcx, 0x10
006D8147  mulps    xmm0, xmm3
006D814A  movups   xmmword ptr [rdx], xmm0
006D814D  add      rdx, 0x10
006D8151  sub      r9, 1
006D8155  jne      0x6d8140  ; -> 006D8140
006D8157  cmp      r10d, r8d
006D815A  jae      0x6d817d  ; -> 006D817D
006D815C  sub      rdx, rcx
006D815F  sub      r8d, r10d
006D8162  mov      eax, r8d
006D8165  lea      rcx, [rcx + 4]
006D8169  movaps   xmm0, xmm3
006D816C  mulss    xmm0, dword ptr [rcx - 4]
006D8171  movss    dword ptr [rdx + rcx - 4], xmm0
006D8177  sub      rax, 1
006D817B  jne      0x6d8165  ; -> 006D8165
006D817D  mov      rcx, qword ptr [rbp - 0x18]
006D8181  xor      rcx, rsp
006D8184  call     0x808c40  ; -> 00808C40 fn
006D8189  mov      rbx, qword ptr [rsp + 0x70]
006D818E  add      rsp, 0x60
006D8192  pop      rbp
006D8193  ret      
```

## 006D81A0 (756 B, extent 006D81A0-006D8494)

Documented callee on this page: `00861EBA`

```
006D81A0  test     edx, edx
006D81A2  je       0x6d8493  ; -> 006D8493
006D81A8  mov      qword ptr [rsp + 8], rbx
006D81AD  push     rbp
006D81AE  mov      rbp, rsp
006D81B1  sub      rsp, 0x60
006D81B5  mov      rax, qword ptr [rip + 0x186c674]  ; -> 01F44830 [u64 0x00002B992DDFA232]
006D81BC  xor      rax, rsp
006D81BF  mov      qword ptr [rbp - 0x18], rax
006D81C3  movss    xmm3, dword ptr [rcx]
006D81C7  xor      r10d, r10d
006D81CA  xorps    xmm0, xmm0
006D81CD  mov      r11, r9
006D81D0  ucomiss  xmm3, xmm0
006D81D3  mov      rbx, rcx
006D81D6  mov      r9d, r10d
006D81D9  jp       0x6d81e8  ; -> 006D81E8
006D81DB  jne      0x6d81e8  ; -> 006D81E8
006D81DD  mov      rcx, qword ptr [rbp - 0x30]
006D81E1  movss    xmm3, dword ptr [rbp - 0x40]
006D81E6  jmp      0x6d81fa  ; -> 006D81FA
006D81E8  mov      rcx, qword ptr [r8]
006D81EB  mov      r9d, 1
006D81F1  mov      qword ptr [rbp - 0x30], rcx
006D81F5  movss    dword ptr [rbp - 0x40], xmm3
006D81FA  movss    xmm1, dword ptr [rbx + 4]
006D81FF  ucomiss  xmm1, xmm0
006D8202  jp       0x6d8206  ; -> 006D8206
006D8204  je       0x6d8224  ; -> 006D8224
006D8206  mov      rax, qword ptr [r8 + 8]
006D820A  mov      ecx, r9d
006D820D  inc      r9d
006D8210  movss    dword ptr [rbp + rcx*4 - 0x40], xmm1
006D8216  movss    xmm3, dword ptr [rbp - 0x40]
006D821B  mov      qword ptr [rbp + rcx*8 - 0x30], rax
006D8220  mov      rcx, qword ptr [rbp - 0x30]
006D8224  movss    xmm1, dword ptr [rbx + 8]
006D8229  ucomiss  xmm1, xmm0
006D822C  jp       0x6d8230  ; -> 006D8230
006D822E  je       0x6d824e  ; -> 006D824E
006D8230  mov      rax, qword ptr [r8 + 0x10]
006D8234  mov      ecx, r9d
006D8237  inc      r9d
006D823A  movss    dword ptr [rbp + rcx*4 - 0x40], xmm1
006D8240  movss    xmm3, dword ptr [rbp - 0x40]
006D8245  mov      qword ptr [rbp + rcx*8 - 0x30], rax
006D824A  mov      rcx, qword ptr [rbp - 0x30]
006D824E  shufps   xmm3, xmm3, 0
006D8252  lea      r8d, [rdx*4]
006D825A  sub      r9d, 1
006D825E  je       0x6d83a7  ; -> 006D83A7
006D8264  sub      r9d, 1
006D8268  je       0x6d8367  ; -> 006D8367
006D826E  sub      r9d, 1
006D8272  je       0x6d8309  ; -> 006D8309
006D8278  cmp      r9d, 1
006D827C  je       0x6d8291  ; -> 006D8291
006D827E  mov      rcx, qword ptr [r11]
006D8281  xor      edx, edx
006D8283  shl      r8, 2
006D8287  call     0x861ec0  ; -> 00861EC0 fn
006D828C  jmp      0x6d847d  ; -> 006D847D
006D8291  mov      rdx, qword ptr [rbp - 0x28]
006D8295  mov      r9, qword ptr [rbp - 0x18]
006D8299  sub      rdx, rcx
006D829C  mov      r10, qword ptr [rbp - 0x20]
006D82A0  sub      r9, rcx
006D82A3  mov      rax, qword ptr [r11]
006D82A6  sub      r10, rcx
006D82A9  movss    xmm4, dword ptr [rbp - 0x34]
006D82AE  movss    xmm5, dword ptr [rbp - 0x38]
006D82B3  movaps   xmmword ptr [rsp + 0x50], xmm6
006D82B8  movss    xmm6, dword ptr [rbp - 0x3c]
006D82BD  nop      dword ptr [rax]
006D82C0  movaps   xmm0, xmm3
006D82C3  movaps   xmm2, xmm6
006D82C6  mulss    xmm2, dword ptr [rdx + rcx]
006D82CB  movaps   xmm1, xmm5
006D82CE  mulss    xmm0, dword ptr [rcx]
006D82D2  mulss    xmm1, dword ptr [r10 + rcx]
006D82D8  addss    xmm2, xmm0
006D82DC  movaps   xmm0, xmm4
006D82DF  mulss    xmm0, dword ptr [r9 + rcx]
006D82E5  add      rcx, 4
006D82E9  addss    xmm2, xmm1
006D82ED  addss    xmm2, xmm0
006D82F1  movss    dword ptr [rax], xmm2
006D82F5  add      rax, 4
006D82F9  add      r8d, -1
006D82FD  jne      0x6d82c0  ; -> 006D82C0
006D82FF  movaps   xmm6, xmmword ptr [rsp + 0x50]
006D8304  jmp      0x6d847d  ; -> 006D847D
006D8309  mov      rax, qword ptr [rbp - 0x20]
006D830D  mov      r9, qword ptr [rbp - 0x28]
006D8311  sub      rcx, rax
006D8314  mov      rdx, qword ptr [r11]
006D8317  sub      r9, rax
006D831A  movss    xmm4, dword ptr [rbp - 0x38]
006D831F  movss    xmm5, dword ptr [rbp - 0x3c]
006D8324  nop      dword ptr [rax]
006D8328  nop      dword ptr [rax + rax]
006D8330  movaps   xmm2, xmm3
006D8333  movaps   xmm0, xmm5
006D8336  mulss    xmm2, dword ptr [rax + rcx]
006D833B  movaps   xmm1, xmm4
006D833E  mulss    xmm0, dword ptr [rax + r9]
006D8344  mulss    xmm1, dword ptr [rax]
006D8348  add      rax, 4
006D834C  addss    xmm2, xmm0
006D8350  addss    xmm2, xmm1
006D8354  movss    dword ptr [rdx], xmm2
006D8358  add      rdx, 4
006D835C  add      r8d, -1
006D8360  jne      0x6d8330  ; -> 006D8330
006D8362  jmp      0x6d847d  ; -> 006D847D
006D8367  mov      rax, qword ptr [r11]
006D836A  mov      rdx, qword ptr [rbp - 0x28]
006D836E  movss    xmm2, dword ptr [rbp - 0x3c]
006D8373  sub      rdx, rax
006D8376  sub      rcx, rax
006D8379  nop      dword ptr [rax]
006D8380  movaps   xmm1, xmm3
006D8383  movaps   xmm0, xmm2
006D8386  mulss    xmm1, dword ptr [rcx + rax]
006D838B  mulss    xmm0, dword ptr [rdx + rax]
006D8390  addss    xmm1, xmm0
006D8394  movss    dword ptr [rax], xmm1
006D8398  add      rax, 4
006D839C  add      r8d, -1
006D83A0  jne      0x6d8380  ; -> 006D8380
006D83A2  jmp      0x6d847d  ; -> 006D847D
006D83A7  ucomiss  xmm3, dword ptr [rip + 0x16137fa]  ; -> 01CEBBA8 [f32 1]
006D83AE  movaps   xmm1, xmm3
006D83B1  shufps   xmm1, xmm1, 0
006D83B5  jp       0x6d83cd  ; -> 006D83CD
006D83B7  jne      0x6d83cd  ; -> 006D83CD
006D83B9  mov      rdx, rcx
006D83BC  shl      r8, 2
006D83C0  mov      rcx, qword ptr [r11]
006D83C3  call     0x861eba  ; -> 00861EBA fn
006D83C8  jmp      0x6d847d  ; -> 006D847D
006D83CD  mov      rdx, qword ptr [r11]
006D83D0  test     r8d, r8d
006D83D3  je       0x6d847d  ; -> 006D847D
006D83D9  cmp      r8d, 8
006D83DD  jb       0x6d8415  ; -> 006D8415
006D83DF  mov      eax, r8d
006D83E2  and      eax, 0xfffffff8
006D83E5  nop      word ptr [rax + rax]
006D83F0  movups   xmm0, xmmword ptr [rcx]
006D83F3  add      r10d, 8
006D83F7  mulps    xmm0, xmm1
006D83FA  movups   xmmword ptr [rdx], xmm0
006D83FD  movups   xmm0, xmmword ptr [rcx + 0x10]
006D8401  add      rcx, 0x20
006D8405  mulps    xmm0, xmm1
006D8408  movups   xmmword ptr [rdx + 0x10], xmm0
006D840C  add      rdx, 0x20
006D8410  cmp      r10d, eax
006D8413  jb       0x6d83f0  ; -> 006D83F0
006D8415  cmp      r10d, r8d
006D8418  jae      0x6d847d  ; -> 006D847D
006D841A  mov      eax, r8d
006D841D  sub      eax, r10d
006D8420  cmp      eax, 4
006D8423  jb       0x6d8457  ; -> 006D8457
006D8425  mov      eax, r8d
006D8428  sub      eax, r10d
006D842B  sub      eax, 4
006D842E  shr      eax, 2
006D8431  inc      eax
006D8433  mov      r9d, eax
006D8436  lea      r10d, [r10 + rax*4]
006D843A  nop      word ptr [rax + rax]
006D8440  movups   xmm0, xmmword ptr [rcx]
006D8443  add      rcx, 0x10
006D8447  mulps    xmm0, xmm3
006D844A  movups   xmmword ptr [rdx], xmm0
006D844D  add      rdx, 0x10
006D8451  sub      r9, 1
006D8455  jne      0x6d8440  ; -> 006D8440
006D8457  cmp      r10d, r8d
006D845A  jae      0x6d847d  ; -> 006D847D
006D845C  sub      rdx, rcx
006D845F  sub      r8d, r10d
006D8462  mov      eax, r8d
006D8465  lea      rcx, [rcx + 4]
006D8469  movaps   xmm0, xmm3
006D846C  mulss    xmm0, dword ptr [rcx - 4]
006D8471  movss    dword ptr [rdx + rcx - 4], xmm0
006D8477  sub      rax, 1
006D847B  jne      0x6d8465  ; -> 006D8465
006D847D  mov      rcx, qword ptr [rbp - 0x18]
006D8481  xor      rcx, rsp
006D8484  call     0x808c40  ; -> 00808C40 fn
006D8489  mov      rbx, qword ptr [rsp + 0x70]
006D848E  add      rsp, 0x60
006D8492  pop      rbp
006D8493  ret      
```

## 006D84A0 (807 B, extent 006D84A0-006D87C7)

Documented callee on this page: `00861EBA`

```
006D84A0  test     edx, edx
006D84A2  je       0x6d87c6  ; -> 006D87C6
006D84A8  mov      qword ptr [rsp + 8], rbx
006D84AD  push     rbp
006D84AE  mov      rbp, rsp
006D84B1  sub      rsp, 0x70
006D84B5  mov      rax, qword ptr [rip + 0x186c374]  ; -> 01F44830 [u64 0x00002B992DDFA232]
006D84BC  xor      rax, rsp
006D84BF  mov      qword ptr [rbp - 0x20], rax
006D84C3  movss    xmm3, dword ptr [rcx]
006D84C7  xor      r10d, r10d
006D84CA  xorps    xmm0, xmm0
006D84CD  mov      r11, r9
006D84D0  ucomiss  xmm3, xmm0
006D84D3  mov      rbx, rcx
006D84D6  mov      r9d, r10d
006D84D9  jp       0x6d84e8  ; -> 006D84E8
006D84DB  jne      0x6d84e8  ; -> 006D84E8
006D84DD  mov      rcx, qword ptr [rbp - 0x40]
006D84E1  movss    xmm3, dword ptr [rbp - 0x50]
006D84E6  jmp      0x6d84fa  ; -> 006D84FA
006D84E8  mov      rcx, qword ptr [r8]
006D84EB  mov      r9d, 1
006D84F1  mov      qword ptr [rbp - 0x40], rcx
006D84F5  movss    dword ptr [rbp - 0x50], xmm3
006D84FA  movss    xmm1, dword ptr [rbx + 4]
006D84FF  ucomiss  xmm1, xmm0
006D8502  jp       0x6d8506  ; -> 006D8506
006D8504  je       0x6d8524  ; -> 006D8524
006D8506  mov      rax, qword ptr [r8 + 8]
006D850A  mov      ecx, r9d
006D850D  inc      r9d
006D8510  movss    dword ptr [rbp + rcx*4 - 0x50], xmm1
006D8516  movss    xmm3, dword ptr [rbp - 0x50]
006D851B  mov      qword ptr [rbp + rcx*8 - 0x40], rax
006D8520  mov      rcx, qword ptr [rbp - 0x40]
006D8524  movss    xmm1, dword ptr [rbx + 8]
006D8529  ucomiss  xmm1, xmm0
006D852C  jp       0x6d8530  ; -> 006D8530
006D852E  je       0x6d854e  ; -> 006D854E
006D8530  mov      rax, qword ptr [r8 + 0x10]
006D8534  mov      ecx, r9d
006D8537  inc      r9d
006D853A  movss    dword ptr [rbp + rcx*4 - 0x50], xmm1
006D8540  movss    xmm3, dword ptr [rbp - 0x50]
006D8545  mov      qword ptr [rbp + rcx*8 - 0x40], rax
006D854A  mov      rcx, qword ptr [rbp - 0x40]
006D854E  movss    xmm1, dword ptr [rbx + 0xc]
006D8553  ucomiss  xmm1, xmm0
006D8556  jp       0x6d855a  ; -> 006D855A
006D8558  je       0x6d8578  ; -> 006D8578
006D855A  mov      rax, qword ptr [r8 + 0x18]
006D855E  mov      ecx, r9d
006D8561  inc      r9d
006D8564  movss    dword ptr [rbp + rcx*4 - 0x50], xmm1
006D856A  movss    xmm3, dword ptr [rbp - 0x50]
006D856F  mov      qword ptr [rbp + rcx*8 - 0x40], rax
006D8574  mov      rcx, qword ptr [rbp - 0x40]
006D8578  shufps   xmm3, xmm3, 0
006D857C  lea      r8d, [rdx + rdx]
006D8580  sub      r9d, 1
006D8584  je       0x6d86d7  ; -> 006D86D7
006D858A  sub      r9d, 1
006D858E  je       0x6d8697  ; -> 006D8697
006D8594  sub      r9d, 1
006D8598  je       0x6d8639  ; -> 006D8639
006D859E  cmp      r9d, 1
006D85A2  je       0x6d85b7  ; -> 006D85B7
006D85A4  mov      rcx, qword ptr [r11]
006D85A7  xor      edx, edx
006D85A9  shl      r8, 2
006D85AD  call     0x861ec0  ; -> 00861EC0 fn
006D85B2  jmp      0x6d87ad  ; -> 006D87AD
006D85B7  mov      rdx, qword ptr [rbp - 0x38]
006D85BB  mov      r9, qword ptr [rbp - 0x28]
006D85BF  sub      rdx, rcx
006D85C2  mov      r10, qword ptr [rbp - 0x30]
006D85C6  sub      r9, rcx
006D85C9  mov      rax, qword ptr [r11]
006D85CC  sub      r10, rcx
006D85CF  movss    xmm4, dword ptr [rbp - 0x44]
006D85D4  movss    xmm5, dword ptr [rbp - 0x48]
006D85D9  movaps   xmmword ptr [rsp + 0x60], xmm6
006D85DE  movss    xmm6, dword ptr [rbp - 0x4c]
006D85E3  nop      dword ptr [rax]
006D85E7  nop      word ptr [rax + rax]
006D85F0  movaps   xmm0, xmm3
006D85F3  movaps   xmm2, xmm6
006D85F6  mulss    xmm2, dword ptr [rdx + rcx]
006D85FB  movaps   xmm1, xmm5
006D85FE  mulss    xmm0, dword ptr [rcx]
006D8602  mulss    xmm1, dword ptr [r10 + rcx]
006D8608  addss    xmm2, xmm0
006D860C  movaps   xmm0, xmm4
006D860F  mulss    xmm0, dword ptr [r9 + rcx]
006D8615  add      rcx, 4
006D8619  addss    xmm2, xmm1
006D861D  addss    xmm2, xmm0
006D8621  movss    dword ptr [rax], xmm2
006D8625  add      rax, 4
006D8629  add      r8d, -1
006D862D  jne      0x6d85f0  ; -> 006D85F0
006D862F  movaps   xmm6, xmmword ptr [rsp + 0x60]
006D8634  jmp      0x6d87ad  ; -> 006D87AD
006D8639  mov      rax, qword ptr [rbp - 0x30]
006D863D  mov      r9, qword ptr [rbp - 0x38]
006D8641  sub      rcx, rax
006D8644  mov      rdx, qword ptr [r11]
006D8647  sub      r9, rax
006D864A  movss    xmm4, dword ptr [rbp - 0x48]
006D864F  movss    xmm5, dword ptr [rbp - 0x4c]
006D8654  nop      dword ptr [rax]
006D8658  nop      dword ptr [rax + rax]
006D8660  movaps   xmm2, xmm3
006D8663  movaps   xmm0, xmm5
006D8666  mulss    xmm2, dword ptr [rcx + rax]
006D866B  movaps   xmm1, xmm4
006D866E  mulss    xmm0, dword ptr [r9 + rax]
006D8674  mulss    xmm1, dword ptr [rax]
006D8678  add      rax, 4
006D867C  addss    xmm2, xmm0
006D8680  addss    xmm2, xmm1
006D8684  movss    dword ptr [rdx], xmm2
006D8688  add      rdx, 4
006D868C  add      r8d, -1
006D8690  jne      0x6d8660  ; -> 006D8660
006D8692  jmp      0x6d87ad  ; -> 006D87AD
006D8697  mov      rax, qword ptr [r11]
006D869A  mov      rdx, qword ptr [rbp - 0x38]
006D869E  movss    xmm2, dword ptr [rbp - 0x4c]
006D86A3  sub      rdx, rax
006D86A6  sub      rcx, rax
006D86A9  nop      dword ptr [rax]
006D86B0  movaps   xmm1, xmm3
006D86B3  movaps   xmm0, xmm2
006D86B6  mulss    xmm1, dword ptr [rcx + rax]
006D86BB  mulss    xmm0, dword ptr [rdx + rax]
006D86C0  addss    xmm1, xmm0
006D86C4  movss    dword ptr [rax], xmm1
006D86C8  add      rax, 4
006D86CC  add      r8d, -1
006D86D0  jne      0x6d86b0  ; -> 006D86B0
006D86D2  jmp      0x6d87ad  ; -> 006D87AD
006D86D7  ucomiss  xmm3, dword ptr [rip + 0x16134ca]  ; -> 01CEBBA8 [f32 1]
006D86DE  movaps   xmm1, xmm3
006D86E1  shufps   xmm1, xmm1, 0
006D86E5  jp       0x6d86fd  ; -> 006D86FD
006D86E7  jne      0x6d86fd  ; -> 006D86FD
006D86E9  mov      rdx, rcx
006D86EC  shl      r8, 2
006D86F0  mov      rcx, qword ptr [r11]
006D86F3  call     0x861eba  ; -> 00861EBA fn
006D86F8  jmp      0x6d87ad  ; -> 006D87AD
006D86FD  mov      rdx, qword ptr [r11]
006D8700  test     r8d, r8d
006D8703  je       0x6d87ad  ; -> 006D87AD
006D8709  cmp      r8d, 8
006D870D  jb       0x6d8745  ; -> 006D8745
006D870F  mov      eax, r8d
006D8712  and      eax, 0xfffffff8
006D8715  nop      word ptr [rax + rax]
006D8720  movups   xmm0, xmmword ptr [rcx]
006D8723  add      r10d, 8
006D8727  mulps    xmm0, xmm1
006D872A  movups   xmmword ptr [rdx], xmm0
006D872D  movups   xmm0, xmmword ptr [rcx + 0x10]
006D8731  add      rcx, 0x20
006D8735  mulps    xmm0, xmm1
006D8738  movups   xmmword ptr [rdx + 0x10], xmm0
006D873C  add      rdx, 0x20
006D8740  cmp      r10d, eax
006D8743  jb       0x6d8720  ; -> 006D8720
006D8745  cmp      r10d, r8d
006D8748  jae      0x6d87ad  ; -> 006D87AD
006D874A  mov      eax, r8d
006D874D  sub      eax, r10d
006D8750  cmp      eax, 4
006D8753  jb       0x6d8787  ; -> 006D8787
006D8755  mov      eax, r8d
006D8758  sub      eax, r10d
006D875B  sub      eax, 4
006D875E  shr      eax, 2
006D8761  inc      eax
006D8763  mov      r9d, eax
006D8766  lea      r10d, [r10 + rax*4]
006D876A  nop      word ptr [rax + rax]
006D8770  movups   xmm0, xmmword ptr [rcx]
006D8773  add      rcx, 0x10
006D8777  mulps    xmm0, xmm3
006D877A  movups   xmmword ptr [rdx], xmm0
006D877D  add      rdx, 0x10
006D8781  sub      r9, 1
006D8785  jne      0x6d8770  ; -> 006D8770
006D8787  cmp      r10d, r8d
006D878A  jae      0x6d87ad  ; -> 006D87AD
006D878C  sub      rdx, rcx
006D878F  sub      r8d, r10d
006D8792  mov      eax, r8d
006D8795  lea      rcx, [rcx + 4]
006D8799  movaps   xmm0, xmm3
006D879C  mulss    xmm0, dword ptr [rcx - 4]
006D87A1  movss    dword ptr [rdx + rcx - 4], xmm0
006D87A7  sub      rax, 1
006D87AB  jne      0x6d8795  ; -> 006D8795
006D87AD  mov      rcx, qword ptr [rbp - 0x20]
006D87B1  xor      rcx, rsp
006D87B4  call     0x808c40  ; -> 00808C40 fn
006D87B9  mov      rbx, qword ptr [rsp + 0x80]
006D87C1  add      rsp, 0x70
006D87C5  pop      rbp
006D87C6  ret      
```
