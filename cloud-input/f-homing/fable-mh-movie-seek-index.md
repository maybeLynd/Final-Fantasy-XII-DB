# F homing pack (FABLE): `17-Presentation-Rendering/Movie-Containers/mh-movie-seek-index.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 3. No bearing page cites them and no documented function calls them directly.

## 00211B60 (82 B, extent 00211B60-00211BB2)

Documented callee on this page: `00211AC0`

```
00211B60  push     rdi
00211B62  sub      rsp, 0x30
00211B66  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00211B6F  mov      qword ptr [rsp + 0x40], rbx
00211B74  mov      edi, edx
00211B76  mov      rbx, rcx
00211B79  call     0x211ac0  ; -> 00211AC0 fn
00211B7E  nop      
00211B7F  test     dil, 1
00211B83  je       0x211ba4  ; -> 00211BA4
00211B85  test     dil, 4
00211B89  jne      0x211b96  ; -> 00211B96
00211B8B  mov      rcx, rbx
00211B8E  call     0x584730  ; -> 00584730 fn
00211B93  nop      
00211B94  jmp      0x211ba4  ; -> 00211BA4
00211B96  mov      edx, 0x158
00211B9B  mov      rcx, rbx
00211B9E  call     0x16d6a0  ; -> 0016D6A0 fn
00211BA3  nop      
00211BA4  mov      rax, rbx
00211BA7  mov      rbx, qword ptr [rsp + 0x40]
00211BAC  add      rsp, 0x30
00211BB0  pop      rdi
00211BB1  ret      
```

## 006792C0 (82 B, extent 006792C0-00679312)

Documented callee on this page: `005CD700`

```
006792C0  push     rdi
006792C2  sub      rsp, 0x30
006792C6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006792CF  mov      qword ptr [rsp + 0x40], rbx
006792D4  mov      rdi, rcx
006792D7  lea      rax, [rip + 0x6f3ab2]  ; -> 00D6CD90
006792DE  mov      qword ptr [rcx], rax
006792E1  add      rcx, 0x48
006792E5  call     0x5cd700  ; -> 005CD700 fn
006792EA  nop      
006792EB  mov      byte ptr [rdi + 0x50], 0
006792EF  lea      rcx, [rdi + 0x30]
006792F3  call     0x5cd700  ; -> 005CD700 fn
006792F8  nop      
006792F9  mov      byte ptr [rdi + 0x38], 0
006792FD  lea      rax, [rip + 0x6f3a74]  ; -> 00D6CD78
00679304  mov      qword ptr [rdi], rax
00679307  mov      rbx, qword ptr [rsp + 0x40]
0067930C  add      rsp, 0x30
00679310  pop      rdi
00679311  ret      
```

## 00679330 (117 B, extent 00679330-006793A5)

Documented callee on this page: `005CD700`

```
00679330  push     rdi
00679332  sub      rsp, 0x30
00679336  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0067933F  mov      qword ptr [rsp + 0x40], rbx
00679344  mov      qword ptr [rsp + 0x48], rsi
00679349  mov      edi, edx
0067934B  mov      rsi, rcx
0067934E  lea      rax, [rip + 0x6f3a3b]  ; -> 00D6CD90
00679355  mov      qword ptr [rcx], rax
00679358  add      rcx, 0x48
0067935C  call     0x5cd700  ; -> 005CD700 fn
00679361  nop      
00679362  mov      byte ptr [rsi + 0x50], 0
00679366  lea      rcx, [rsi + 0x30]
0067936A  call     0x5cd700  ; -> 005CD700 fn
0067936F  nop      
00679370  mov      byte ptr [rsi + 0x38], 0
00679374  lea      rax, [rip + 0x6f39fd]  ; -> 00D6CD78
0067937B  mov      qword ptr [rsi], rax
0067937E  test     dil, 1
00679382  je       0x679392  ; -> 00679392
00679384  mov      edx, 0x60
00679389  mov      rcx, rsi
0067938C  call     0x809950  ; -> 00809950 fn
00679391  nop      
00679392  mov      rax, rsi
00679395  mov      rbx, qword ptr [rsp + 0x40]
0067939A  mov      rsi, qword ptr [rsp + 0x48]
0067939F  add      rsp, 0x30
006793A3  pop      rdi
006793A4  ret      
```
