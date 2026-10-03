# F homing pack: `22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`

Generated 2026-10-02 21:16 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 34. No bearing page cites them and no documented function calls them directly.

## 005A0C50 (93 B, extent 005A0C50-005A0CAD)

Documented callee on this page: `00630260`

```
005A0C50  mov      qword ptr [rsp + 8], rbx
005A0C55  push     rdi
005A0C56  sub      rsp, 0x30
005A0C5A  movaps   xmmword ptr [rsp + 0x20], xmm6
005A0C5F  mov      rbx, r9
005A0C62  mov      rdi, r8
005A0C65  call     qword ptr [rcx + 8]
005A0C68  movaps   xmm6, xmm0
005A0C6B  test     rbx, rbx
005A0C6E  je       0x5a0c9b  ; -> 005A0C9B
005A0C70  call     0x630260  ; -> 00630260 fn
005A0C75  cmp      rdi, rax
005A0C78  jne      0x5a0c9b  ; -> 005A0C9B
005A0C7A  movsd    qword ptr [rbx + 8], xmm6
005A0C7F  mov      eax, 1
005A0C84  mov      qword ptr [rbx], 0
005A0C8B  mov      rbx, qword ptr [rsp + 0x40]
005A0C90  movaps   xmm6, xmmword ptr [rsp + 0x20]
005A0C95  add      rsp, 0x30
005A0C99  pop      rdi
005A0C9A  ret      
005A0C9B  mov      rbx, qword ptr [rsp + 0x40]
005A0CA0  xor      eax, eax
005A0CA2  movaps   xmm6, xmmword ptr [rsp + 0x20]
005A0CA7  add      rsp, 0x30
005A0CAB  pop      rdi
005A0CAC  ret      
```

## 005C80F0 (49 B, extent 005C80F0-005C8121)

Documented callee on this page: `00810580`

```
005C80F0  mov      qword ptr [rsp + 8], rbx
005C80F5  push     rdi
005C80F6  sub      rsp, 0x20
005C80FA  mov      rdi, rdx
005C80FD  mov      rbx, r8
005C8100  mov      rcx, rdi
005C8103  mov      edx, 1
005C8108  call     0x80f420  ; -> 0080F420 fn
005C810D  mov      edx, dword ptr [rbx]
005C810F  mov      rcx, rdi
005C8112  mov      rbx, qword ptr [rsp + 0x30]
005C8117  add      rsp, 0x20
005C811B  pop      rdi
005C811C  jmp      0x810580  ; -> 00810580 fn
```

## 005CBCC0 (93 B, extent 005CBCC0-005CBD1D)

Documented callee on this page: `006301F0`

```
005CBCC0  mov      qword ptr [rsp + 8], rbx
005CBCC5  push     rdi
005CBCC6  sub      rsp, 0x30
005CBCCA  movaps   xmmword ptr [rsp + 0x20], xmm6
005CBCCF  mov      rbx, r9
005CBCD2  mov      rdi, r8
005CBCD5  call     qword ptr [rcx + 8]
005CBCD8  movaps   xmm6, xmm0
005CBCDB  test     rbx, rbx
005CBCDE  je       0x5cbd0b  ; -> 005CBD0B
005CBCE0  call     0x6301f0  ; -> 006301F0 fn
005CBCE5  cmp      rdi, rax
005CBCE8  jne      0x5cbd0b  ; -> 005CBD0B
005CBCEA  movss    dword ptr [rbx + 8], xmm6
005CBCEF  mov      eax, 1
005CBCF4  mov      qword ptr [rbx], 0
005CBCFB  mov      rbx, qword ptr [rsp + 0x40]
005CBD00  movaps   xmm6, xmmword ptr [rsp + 0x20]
005CBD05  add      rsp, 0x30
005CBD09  pop      rdi
005CBD0A  ret      
005CBD0B  mov      rbx, qword ptr [rsp + 0x40]
005CBD10  xor      eax, eax
005CBD12  movaps   xmm6, xmmword ptr [rsp + 0x20]
005CBD17  add      rsp, 0x30
005CBD1B  pop      rdi
005CBD1C  ret      
```

## 005CBD20 (126 B, extent 005CBD20-005CBD9E)

Documented callee on this page: `006301F0`

```
005CBD20  mov      qword ptr [rsp + 8], rbx
005CBD25  push     rdi
005CBD26  sub      rsp, 0x30
005CBD2A  mov      rbx, r9
005CBD2D  mov      r9, rcx
005CBD30  mov      rdi, r8
005CBD33  test     rdx, rdx
005CBD36  je       0x5cbd91  ; -> 005CBD91
005CBD38  movsxd   rax, dword ptr [rcx + 0x10]
005CBD3C  lea      rcx, [rdx - 8]
005CBD40  add      rcx, rax
005CBD43  movaps   xmmword ptr [rsp + 0x20], xmm6
005CBD48  call     qword ptr [r9 + 8]
005CBD4C  movaps   xmm6, xmm0
005CBD4F  test     rbx, rbx
005CBD52  je       0x5cbd7f  ; -> 005CBD7F
005CBD54  call     0x6301f0  ; -> 006301F0 fn
005CBD59  cmp      rdi, rax
005CBD5C  jne      0x5cbd7f  ; -> 005CBD7F
005CBD5E  movss    dword ptr [rbx + 8], xmm6
005CBD63  mov      eax, 1
005CBD68  movaps   xmm6, xmmword ptr [rsp + 0x20]
005CBD6D  mov      qword ptr [rbx], 0
005CBD74  mov      rbx, qword ptr [rsp + 0x40]
005CBD79  add      rsp, 0x30
005CBD7D  pop      rdi
005CBD7E  ret      
005CBD7F  xor      eax, eax
005CBD81  movaps   xmm6, xmmword ptr [rsp + 0x20]
005CBD86  mov      rbx, qword ptr [rsp + 0x40]
005CBD8B  add      rsp, 0x30
005CBD8F  pop      rdi
005CBD90  ret      
005CBD91  xor      eax, eax
005CBD93  mov      rbx, qword ptr [rsp + 0x40]
005CBD98  add      rsp, 0x30
005CBD9C  pop      rdi
005CBD9D  ret      
```

## 005CC1F0 (125 B, extent 005CC1F0-005CC26D)

Documented callee on this page: `00630490`

```
005CC1F0  mov      qword ptr [rsp + 0x18], rbx
005CC1F5  push     rsi
005CC1F6  sub      rsp, 0x20
005CC1FA  mov      rbx, r9
005CC1FD  mov      r9, rcx
005CC200  mov      rsi, r8
005CC203  test     rdx, rdx
005CC206  je       0x5cc260  ; -> 005CC260
005CC208  movsxd   rax, dword ptr [rcx + 0x10]
005CC20C  lea      rcx, [rdx - 8]
005CC210  add      rcx, rax
005CC213  mov      qword ptr [rsp + 0x30], rdi
005CC218  call     qword ptr [r9 + 8]
005CC21C  movzx    edi, al
005CC21F  test     rbx, rbx
005CC222  je       0x5cc24e  ; -> 005CC24E
005CC224  call     0x630490  ; -> 00630490 fn
005CC229  cmp      rsi, rax
005CC22C  jne      0x5cc24e  ; -> 005CC24E
005CC22E  mov      byte ptr [rbx + 8], dil
005CC232  mov      eax, 1
005CC237  mov      rdi, qword ptr [rsp + 0x30]
005CC23C  mov      qword ptr [rbx], 0
005CC243  mov      rbx, qword ptr [rsp + 0x40]
005CC248  add      rsp, 0x20
005CC24C  pop      rsi
005CC24D  ret      
005CC24E  xor      eax, eax
005CC250  mov      rdi, qword ptr [rsp + 0x30]
005CC255  mov      rbx, qword ptr [rsp + 0x40]
005CC25A  add      rsp, 0x20
005CC25E  pop      rsi
005CC25F  ret      
005CC260  xor      eax, eax
005CC262  mov      rbx, qword ptr [rsp + 0x40]
005CC267  add      rsp, 0x20
005CC26B  pop      rsi
005CC26C  ret      
```

## 005CC360 (114 B, extent 005CC360-005CC3D2)

Documented callee on this page: `00630180`

```
005CC360  mov      qword ptr [rsp + 0x18], rbx
005CC365  push     rsi
005CC366  sub      rsp, 0x20
005CC36A  mov      rbx, r9
005CC36D  mov      rsi, r8
005CC370  mov      rax, rcx
005CC373  test     rdx, rdx
005CC376  je       0x5cc3c5  ; -> 005CC3C5
005CC378  mov      rcx, rdx
005CC37B  mov      qword ptr [rsp + 0x30], rdi
005CC380  call     qword ptr [rax + 8]
005CC383  mov      edi, eax
005CC385  test     rbx, rbx
005CC388  je       0x5cc3b3  ; -> 005CC3B3
005CC38A  call     0x630180  ; -> 00630180 fn
005CC38F  cmp      rsi, rax
005CC392  jne      0x5cc3b3  ; -> 005CC3B3
005CC394  mov      dword ptr [rbx + 8], edi
005CC397  mov      eax, 1
005CC39C  mov      rdi, qword ptr [rsp + 0x30]
005CC3A1  mov      qword ptr [rbx], 0
005CC3A8  mov      rbx, qword ptr [rsp + 0x40]
005CC3AD  add      rsp, 0x20
005CC3B1  pop      rsi
005CC3B2  ret      
005CC3B3  xor      eax, eax
005CC3B5  mov      rdi, qword ptr [rsp + 0x30]
005CC3BA  mov      rbx, qword ptr [rsp + 0x40]
005CC3BF  add      rsp, 0x20
005CC3C3  pop      rsi
005CC3C4  ret      
005CC3C5  xor      eax, eax
005CC3C7  mov      rbx, qword ptr [rsp + 0x40]
005CC3CC  add      rsp, 0x20
005CC3D0  pop      rsi
005CC3D1  ret      
```

## 005FE350 (1298 B, extent 005FE350-005FE862)

Documented callee on this page: `00630030`

```
005FE350  push     rbx
005FE352  push     r14
005FE354  sub      rsp, 0x48
005FE358  mov      rax, qword ptr [rdx]
005FE35B  mov      r14, rcx
005FE35E  mov      rcx, rdx
005FE361  mov      rbx, rdx
005FE364  call     qword ptr [rax + 0x18]
005FE367  test     al, al
005FE369  jne      0x5fe85a  ; -> 005FE85A
005FE36F  mov      rdx, qword ptr [r14 + 0x18]
005FE373  mov      rcx, qword ptr [rbx + 8]
005FE377  mov      qword ptr [rsp + 0x70], rdi
005FE37C  mov      edi, dword ptr [r14 + 0x10]
005FE380  mov      qword ptr [rsp + 0x38], r13
005FE385  call     0x5d8eb0  ; -> 005D8EB0 fn
005FE38A  mov      r13, rax
005FE38D  and      edi, 0x7fffffff
005FE393  je       0x5fe850  ; -> 005FE850
005FE399  mov      qword ptr [rsp + 0x60], rbp
005FE39E  lea      r8, [rip - 0x4de3a5]  ; -> 00120000 (image base)
005FE3A5  mov      qword ptr [rsp + 0x68], rsi
005FE3AA  xor      r10d, r10d
005FE3AD  mov      qword ptr [rsp + 0x40], r12
005FE3B2  mov      qword ptr [rsp + 0x30], r15
005FE3B7  mov      r15d, r10d
005FE3BA  mov      r12d, edi
005FE3BD  nop      dword ptr [rax]
005FE3C0  mov      rbp, qword ptr [r14 + 0x18]
005FE3C4  add      rbp, r15
005FE3C7  movzx    ecx, word ptr [rbp + 0x12]
005FE3CB  movzx    edx, word ptr [rbp + 0x10]
005FE3CF  and      ecx, 0x1fff
005FE3D5  add      ecx, edx
005FE3D7  cmp      ecx, dword ptr [r14]
005FE3DA  jbe      0x5fe3e1  ; -> 005FE3E1
005FE3DC  mov      rdi, r10
005FE3DF  jmp      0x5fe3f2  ; -> 005FE3F2
005FE3E1  cmp      dx, 4
005FE3E5  jae      0x5fe3ec  ; -> 005FE3EC
005FE3E7  mov      rdi, r10
005FE3EA  jmp      0x5fe3f2  ; -> 005FE3F2
005FE3EC  movzx    edi, dx
005FE3EF  add      rdi, r14
005FE3F2  movzx    eax, byte ptr [rbp + 2]
005FE3F6  mov      rsi, rdi
005FE3F9  test     r13, r13
005FE3FC  je       0x5fe40d  ; -> 005FE40D
005FE3FE  movzx    esi, word ptr [r15 + r13 + 0x10]
005FE404  add      rsi, r14
005FE407  movzx    edi, dx
005FE40A  add      rdi, r14
005FE40D  cmp      eax, 0x42
005FE410  jne      0x5fe43a  ; -> 005FE43A
005FE412  mov      rax, qword ptr [rbx]
005FE415  lea      r9, [rip + 0x26bbae4]  ; -> 02CB9F00
005FE41C  mov      qword ptr [rsp + 0x28], rsi
005FE421  mov      r8d, 1
005FE427  mov      rdx, rdi
005FE42A  mov      dword ptr [rsp + 0x20], r10d
005FE42F  mov      rcx, rbx
005FE432  call     qword ptr [rax + 0x10]
005FE435  jmp      0x5fe821  ; -> 005FE821
005FE43A  cmp      eax, 0x43
005FE43D  jne      0x5fe467  ; -> 005FE467
005FE43F  mov      rax, qword ptr [rbx]
005FE442  lea      r9, [rip + 0x26bbbb7]  ; -> 02CBA000
005FE449  mov      qword ptr [rsp + 0x28], rsi
005FE44E  mov      r8d, 1
005FE454  mov      rdx, rdi
005FE457  mov      dword ptr [rsp + 0x20], r10d
005FE45C  mov      rcx, rbx
005FE45F  call     qword ptr [rax + 0x10]
005FE462  jmp      0x5fe821  ; -> 005FE821
005FE467  cmp      eax, 0x44
005FE46A  jne      0x5fe494  ; -> 005FE494
005FE46C  mov      rax, qword ptr [rbx]
005FE46F  lea      r9, [rip + 0x26bbc8a]  ; -> 02CBA100
005FE476  mov      qword ptr [rsp + 0x28], rsi
005FE47B  mov      r8d, 1
005FE481  mov      rdx, rdi
005FE484  mov      dword ptr [rsp + 0x20], r10d
005FE489  mov      rcx, rbx
005FE48C  call     qword ptr [rax + 0x10]
005FE48F  jmp      0x5fe821  ; -> 005FE821
005FE494  cmp      eax, 0x47
005FE497  jne      0x5fe4c1  ; -> 005FE4C1
005FE499  mov      rax, qword ptr [rbx]
005FE49C  lea      r9, [rip + 0x26bbd5d]  ; -> 02CBA200
005FE4A3  mov      qword ptr [rsp + 0x28], rsi
005FE4A8  mov      r8d, 1
005FE4AE  mov      rdx, rdi
005FE4B1  mov      dword ptr [rsp + 0x20], r10d
005FE4B6  mov      rcx, rbx
005FE4B9  call     qword ptr [rax + 0x10]
005FE4BC  jmp      0x5fe821  ; -> 005FE821
005FE4C1  cmp      eax, 0x48
005FE4C4  jne      0x5fe4ee  ; -> 005FE4EE
005FE4C6  mov      rax, qword ptr [rbx]
005FE4C9  lea      r9, [rip + 0x26bbe30]  ; -> 02CBA300
005FE4D0  mov      qword ptr [rsp + 0x28], rsi
005FE4D5  mov      r8d, 1
005FE4DB  mov      rdx, rdi
005FE4DE  mov      dword ptr [rsp + 0x20], r10d
005FE4E3  mov      rcx, rbx
005FE4E6  call     qword ptr [rax + 0x10]
005FE4E9  jmp      0x5fe821  ; -> 005FE821
005FE4EE  cmp      eax, 0x49
005FE4F1  jne      0x5fe51b  ; -> 005FE51B
005FE4F3  mov      rax, qword ptr [rbx]
005FE4F6  lea      r9, [rip + 0x26bbf03]  ; -> 02CBA400
005FE4FD  mov      qword ptr [rsp + 0x28], rsi
005FE502  mov      r8d, 1
005FE508  mov      rdx, rdi
005FE50B  mov      dword ptr [rsp + 0x20], r10d
005FE510  mov      rcx, rbx
005FE513  call     qword ptr [rax + 0x10]
005FE516  jmp      0x5fe821  ; -> 005FE821
005FE51B  cmp      eax, 0x4b
005FE51E  jne      0x5fe548  ; -> 005FE548
005FE520  mov      rax, qword ptr [rbx]
005FE523  lea      r9, [rip + 0x26bbfd6]  ; -> 02CBA500
005FE52A  mov      qword ptr [rsp + 0x28], rsi
005FE52F  mov      r8d, 1
005FE535  mov      rdx, rdi
005FE538  mov      dword ptr [rsp + 0x20], r10d
005FE53D  mov      rcx, rbx
005FE540  call     qword ptr [rax + 0x10]
005FE543  jmp      0x5fe821  ; -> 005FE821
005FE548  cmp      eax, 0x4c
005FE54B  jne      0x5fe575  ; -> 005FE575
005FE54D  mov      rax, qword ptr [rbx]
005FE550  lea      r9, [rip + 0x26bc0a9]  ; -> 02CBA600
005FE557  mov      qword ptr [rsp + 0x28], rsi
005FE55C  mov      r8d, 1
005FE562  mov      rdx, rdi
005FE565  mov      dword ptr [rsp + 0x20], r10d
005FE56A  mov      rcx, rbx
005FE56D  call     qword ptr [rax + 0x10]
005FE570  jmp      0x5fe821  ; -> 005FE821
005FE575  cmp      eax, 0x4a
005FE578  jne      0x5fe5a2  ; -> 005FE5A2
005FE57A  mov      rax, qword ptr [rbx]
005FE57D  lea      r9, [rip + 0x26bb87c]  ; -> 02CB9E00
005FE584  mov      qword ptr [rsp + 0x28], rsi
005FE589  mov      r8d, 1
005FE58F  mov      rdx, rdi
005FE592  mov      dword ptr [rsp + 0x20], r10d
005FE597  mov      rcx, rbx
005FE59A  call     qword ptr [rax + 0x10]
005FE59D  jmp      0x5fe821  ; -> 005FE821
005FE5A2  cmp      eax, 0x4d
005FE5A5  jne      0x5fe5cf  ; -> 005FE5CF
005FE5A7  mov      rax, qword ptr [rbx]
005FE5AA  lea      r9, [rip + 0x26bc34f]  ; -> 02CBA900
005FE5B1  mov      qword ptr [rsp + 0x28], rsi
005FE5B6  mov      r8d, 1
005FE5BC  mov      rdx, rdi
005FE5BF  mov      dword ptr [rsp + 0x20], r10d
005FE5C4  mov      rcx, rbx
005FE5C7  call     qword ptr [rax + 0x10]
005FE5CA  jmp      0x5fe821  ; -> 005FE821
005FE5CF  cmp      eax, 0x4e
005FE5D2  jne      0x5fe5fc  ; -> 005FE5FC
005FE5D4  mov      rax, qword ptr [rbx]
005FE5D7  lea      r9, [rip + 0x26bc422]  ; -> 02CBAA00
005FE5DE  mov      qword ptr [rsp + 0x28], rsi
005FE5E3  mov      r8d, 1
005FE5E9  mov      rdx, rdi
005FE5EC  mov      dword ptr [rsp + 0x20], r10d
005FE5F1  mov      rcx, rbx
005FE5F4  call     qword ptr [rax + 0x10]
005FE5F7  jmp      0x5fe821  ; -> 005FE821
005FE5FC  cmp      eax, 0x4f
005FE5FF  jne      0x5fe629  ; -> 005FE629
005FE601  mov      rax, qword ptr [rbx]
005FE604  lea      r9, [rip + 0x26bc0f5]  ; -> 02CBA700
005FE60B  mov      qword ptr [rsp + 0x28], rsi
005FE610  mov      r8d, 1
005FE616  mov      rdx, rdi
005FE619  mov      dword ptr [rsp + 0x20], r10d
005FE61E  mov      rcx, rbx
005FE621  call     qword ptr [rax + 0x10]
005FE624  jmp      0x5fe821  ; -> 005FE821
005FE629  cmp      eax, 0x50
005FE62C  jne      0x5fe656  ; -> 005FE656
005FE62E  mov      rax, qword ptr [rbx]
005FE631  lea      r9, [rip + 0x26bc1c8]  ; -> 02CBA800
005FE638  mov      qword ptr [rsp + 0x28], rsi
005FE63D  mov      r8d, 1
005FE643  mov      rdx, rdi
005FE646  mov      dword ptr [rsp + 0x20], r10d
005FE64B  mov      rcx, rbx
005FE64E  call     qword ptr [rax + 0x10]
005FE651  jmp      0x5fe821  ; -> 005FE821
005FE656  movzx    eax, byte ptr [rbp + 3]
005FE65A  mov      r9, r10
005FE65D  mov      edx, r10d
005FE660  cmp      eax, 0x32
005FE663  ja       0x5fe7d2  ; -> 005FE7D2
005FE669  mov      ecx, dword ptr [r8 + rax*4 + 0x4de864]  ; image base + 0x4de864 = 005FE864
005FE671  add      rcx, r8
005FE674  jmp      rcx
005FE676  call     0x6301f0  ; -> 006301F0 fn
005FE67B  mov      edx, 1
005FE680  jmp      0x5fe7cc  ; -> 005FE7CC
005FE685  call     0x6301f0  ; -> 006301F0 fn
005FE68A  mov      edx, 2
005FE68F  jmp      0x5fe7cc  ; -> 005FE7CC
005FE694  call     0x6301f0  ; -> 006301F0 fn
005FE699  mov      edx, 3
005FE69E  jmp      0x5fe7cc  ; -> 005FE7CC
005FE6A3  call     0x6301f0  ; -> 006301F0 fn
005FE6A8  jmp      0x5fe7c7  ; -> 005FE7C7
005FE6AD  call     0x630180  ; -> 00630180 fn
005FE6B2  mov      edx, 1
005FE6B7  jmp      0x5fe7cc  ; -> 005FE7CC
005FE6BC  call     0x630180  ; -> 00630180 fn
005FE6C1  mov      edx, 2
005FE6C6  jmp      0x5fe7cc  ; -> 005FE7CC
005FE6CB  call     0x630180  ; -> 00630180 fn
005FE6D0  mov      edx, 3
005FE6D5  jmp      0x5fe7cc  ; -> 005FE7CC
005FE6DA  call     0x630180  ; -> 00630180 fn
005FE6DF  jmp      0x5fe7c7  ; -> 005FE7C7
005FE6E4  call     0x630030  ; -> 00630030 fn
005FE6E9  mov      edx, 1
005FE6EE  jmp      0x5fe7cc  ; -> 005FE7CC
005FE6F3  call     0x630030  ; -> 00630030 fn
005FE6F8  mov      edx, 2
005FE6FD  jmp      0x5fe7cc  ; -> 005FE7CC
005FE702  call     0x630030  ; -> 00630030 fn
005FE707  mov      edx, 3
005FE70C  jmp      0x5fe7cc  ; -> 005FE7CC
005FE711  call     0x630030  ; -> 00630030 fn
005FE716  jmp      0x5fe7c7  ; -> 005FE7C7
005FE71B  call     0x6300a0  ; -> 006300A0 fn
005FE720  mov      edx, 1
005FE725  jmp      0x5fe7cc  ; -> 005FE7CC
005FE72A  call     0x6300a0  ; -> 006300A0 fn
005FE72F  mov      edx, 2
005FE734  jmp      0x5fe7cc  ; -> 005FE7CC
005FE739  call     0x6300a0  ; -> 006300A0 fn
005FE73E  mov      edx, 3
005FE743  jmp      0x5fe7cc  ; -> 005FE7CC
005FE748  call     0x62ffc0  ; -> 0062FFC0 fn
005FE74D  mov      edx, 1
005FE752  jmp      0x5fe7cc  ; -> 005FE7CC
005FE754  call     0x62ffc0  ; -> 0062FFC0 fn
005FE759  mov      edx, 2
005FE75E  jmp      0x5fe7cc  ; -> 005FE7CC
005FE760  call     0x62ffc0  ; -> 0062FFC0 fn
005FE765  mov      edx, 3
005FE76A  jmp      0x5fe7cc  ; -> 005FE7CC
005FE76C  call     0x62ffc0  ; -> 0062FFC0 fn
005FE771  jmp      0x5fe7c7  ; -> 005FE7C7
005FE773  call     0x630110  ; -> 00630110 fn
005FE778  mov      edx, 1
005FE77D  jmp      0x5fe7cc  ; -> 005FE7CC
005FE77F  call     0x630110  ; -> 00630110 fn
005FE784  mov      edx, 2
005FE789  jmp      0x5fe7cc  ; -> 005FE7CC
005FE78B  call     0x630110  ; -> 00630110 fn
005FE790  mov      edx, 3
005FE795  jmp      0x5fe7cc  ; -> 005FE7CC
005FE797  call     0x630110  ; -> 00630110 fn
005FE79C  jmp      0x5fe7c7  ; -> 005FE7C7
005FE79E  call     0x62ff50  ; -> 0062FF50 fn
005FE7A3  mov      edx, 1
005FE7A8  jmp      0x5fe7cc  ; -> 005FE7CC
005FE7AA  call     0x6301f0  ; -> 006301F0 fn
005FE7AF  mov      edx, 0xc
005FE7B4  jmp      0x5fe7cc  ; -> 005FE7CC
005FE7B6  call     0x6301f0  ; -> 006301F0 fn
005FE7BB  mov      edx, 0x10
005FE7C0  jmp      0x5fe7cc  ; -> 005FE7CC
005FE7C2  call     0x6300a0  ; -> 006300A0 fn
005FE7C7  mov      edx, 4
005FE7CC  xor      r10d, r10d
005FE7CF  mov      r9, rax
005FE7D2  movzx    r8d, word ptr [rbp]
005FE7D7  test     r8d, r8d
005FE7DA  je       0x5fe7e2  ; -> 005FE7E2
005FE7DC  imul     r8d, edx
005FE7E0  jmp      0x5fe7e5  ; -> 005FE7E5
005FE7E2  mov      r8d, edx
005FE7E5  test     r9, r9
005FE7E8  je       0x5fe802  ; -> 005FE802
005FE7EA  mov      rax, qword ptr [rbx]
005FE7ED  mov      rdx, rdi
005FE7F0  mov      qword ptr [rsp + 0x28], rsi
005FE7F5  mov      rcx, rbx
005FE7F8  mov      dword ptr [rsp + 0x20], r10d
005FE7FD  call     qword ptr [rax + 0x10]
005FE800  jmp      0x5fe821  ; -> 005FE821
005FE802  movzx    eax, byte ptr [rbp + 8]
005FE806  lea      rdx, [rip + 0x74be7b]  ; -> 00D4A688
005FE80D  mov      r8, qword ptr [rbp + 8]
005FE811  and      eax, 1
005FE814  sub      r8, rax
005FE817  mov      ecx, 1
005FE81C  call     0x5cdaa0  ; -> 005CDAA0 fn
005FE821  add      r15, 0x18
005FE825  lea      r8, [rip - 0x4de82c]  ; -> 00120000 (image base)
005FE82C  mov      r10d, 0
005FE832  sub      r12, 1
005FE836  jne      0x5fe3c0  ; -> 005FE3C0
005FE83C  mov      r15, qword ptr [rsp + 0x30]
005FE841  mov      r12, qword ptr [rsp + 0x40]
005FE846  mov      rsi, qword ptr [rsp + 0x68]
005FE84B  mov      rbp, qword ptr [rsp + 0x60]
005FE850  mov      rdi, qword ptr [rsp + 0x70]
005FE855  mov      r13, qword ptr [rsp + 0x38]
005FE85A  add      rsp, 0x48
005FE85E  pop      r14
005FE860  pop      rbx
005FE861  ret      
```

## 0062FB40 (31 B, extent 0062FB40-0062FB5F)

Documented callee on this page: `00684080`

```
0062FB40  xor      ecx, ecx
0062FB42  mov      rax, rdx
0062FB45  test     r8, r8
0062FB48  lea      rdx, [r8 + 0x30]
0062FB4C  lea      r8, [rip + 0x26c8a2d]  ; -> 02CF8580
0062FB53  cmove    rdx, rcx
0062FB57  mov      rcx, rax
0062FB5A  jmp      0x684080  ; -> 00684080 fn
```

## 0063A110 (51 B, extent 0063A110-0063A143)

Documented callee on this page: `00684080`

```
0063A110  push     rbx
0063A112  sub      rsp, 0x20
0063A116  mov      rbx, rdx
0063A119  call     qword ptr [rcx + 8]
0063A11C  test     rax, rax
0063A11F  je       0x63a127  ; -> 0063A127
0063A121  lea      rdx, [rax + 0x10]
0063A125  jmp      0x63a129  ; -> 0063A129
0063A127  xor      edx, edx
0063A129  lea      r8, [rip + 0x26be850]  ; -> 02CF8980
0063A130  mov      rcx, rbx
0063A133  call     0x684080  ; -> 00684080 fn
0063A138  mov      eax, 1
0063A13D  add      rsp, 0x20
0063A141  pop      rbx
0063A142  ret      
```

## 0063D0C0 (51 B, extent 0063D0C0-0063D0F3)

Documented callee on this page: `00810580`

```
0063D0C0  mov      qword ptr [rsp + 8], rbx
0063D0C5  push     rdi
0063D0C6  sub      rsp, 0x20
0063D0CA  mov      rdi, rdx
0063D0CD  mov      rbx, r8
0063D0D0  mov      rcx, rdi
0063D0D3  mov      edx, 1
0063D0D8  call     0x80f420  ; -> 0080F420 fn
0063D0DD  movsx    rdx, byte ptr [rbx]
0063D0E1  mov      rcx, rdi
0063D0E4  mov      rbx, qword ptr [rsp + 0x30]
0063D0E9  add      rsp, 0x20
0063D0ED  pop      rdi
0063D0EE  jmp      0x810580  ; -> 00810580 fn
```

## 0063D100 (50 B, extent 0063D100-0063D132)

Documented callee on this page: `00810580`

```
0063D100  mov      qword ptr [rsp + 8], rbx
0063D105  push     rdi
0063D106  sub      rsp, 0x20
0063D10A  mov      rdi, rdx
0063D10D  mov      rbx, r8
0063D110  mov      rcx, rdi
0063D113  mov      edx, 1
0063D118  call     0x80f420  ; -> 0080F420 fn
0063D11D  movzx    edx, byte ptr [rbx]
0063D120  mov      rcx, rdi
0063D123  mov      rbx, qword ptr [rsp + 0x30]
0063D128  add      rsp, 0x20
0063D12C  pop      rdi
0063D12D  jmp      0x810580  ; -> 00810580 fn
```

## 0063D140 (51 B, extent 0063D140-0063D173)

Documented callee on this page: `00810580`

```
0063D140  mov      qword ptr [rsp + 8], rbx
0063D145  push     rdi
0063D146  sub      rsp, 0x20
0063D14A  mov      rdi, rdx
0063D14D  mov      rbx, r8
0063D150  mov      rcx, rdi
0063D153  mov      edx, 1
0063D158  call     0x80f420  ; -> 0080F420 fn
0063D15D  movsx    rdx, word ptr [rbx]
0063D161  mov      rcx, rdi
0063D164  mov      rbx, qword ptr [rsp + 0x30]
0063D169  add      rsp, 0x20
0063D16D  pop      rdi
0063D16E  jmp      0x810580  ; -> 00810580 fn
```

## 0063D180 (50 B, extent 0063D180-0063D1B2)

Documented callee on this page: `00810580`

```
0063D180  mov      qword ptr [rsp + 8], rbx
0063D185  push     rdi
0063D186  sub      rsp, 0x20
0063D18A  mov      rdi, rdx
0063D18D  mov      rbx, r8
0063D190  mov      rcx, rdi
0063D193  mov      edx, 1
0063D198  call     0x80f420  ; -> 0080F420 fn
0063D19D  movzx    edx, word ptr [rbx]
0063D1A0  mov      rcx, rdi
0063D1A3  mov      rbx, qword ptr [rsp + 0x30]
0063D1A8  add      rsp, 0x20
0063D1AC  pop      rdi
0063D1AD  jmp      0x810580  ; -> 00810580 fn
```

## 0063D1C0 (50 B, extent 0063D1C0-0063D1F2)

Documented callee on this page: `00810580`

```
0063D1C0  mov      qword ptr [rsp + 8], rbx
0063D1C5  push     rdi
0063D1C6  sub      rsp, 0x20
0063D1CA  mov      rdi, rdx
0063D1CD  mov      rbx, r8
0063D1D0  mov      rcx, rdi
0063D1D3  mov      edx, 1
0063D1D8  call     0x80f420  ; -> 0080F420 fn
0063D1DD  movsxd   rdx, dword ptr [rbx]
0063D1E0  mov      rcx, rdi
0063D1E3  mov      rbx, qword ptr [rsp + 0x30]
0063D1E8  add      rsp, 0x20
0063D1EC  pop      rdi
0063D1ED  jmp      0x810580  ; -> 00810580 fn
```

## 0063D280 (50 B, extent 0063D280-0063D2B2)

Documented callee on this page: `00810580`

```
0063D280  mov      qword ptr [rsp + 8], rbx
0063D285  push     rdi
0063D286  sub      rsp, 0x20
0063D28A  mov      rdi, rdx
0063D28D  mov      rbx, r8
0063D290  mov      rcx, rdi
0063D293  mov      edx, 1
0063D298  call     0x80f420  ; -> 0080F420 fn
0063D29D  mov      rdx, qword ptr [rbx]
0063D2A0  mov      rcx, rdi
0063D2A3  mov      rbx, qword ptr [rsp + 0x30]
0063D2A8  add      rsp, 0x20
0063D2AC  pop      rdi
0063D2AD  jmp      0x810580  ; -> 00810580 fn
```

## 0063D2C0 (50 B, extent 0063D2C0-0063D2F2)

Documented callee on this page: `0080F420`

```
0063D2C0  mov      qword ptr [rsp + 8], rbx
0063D2C5  push     rdi
0063D2C6  sub      rsp, 0x20
0063D2CA  mov      rdi, rdx
0063D2CD  mov      rbx, r8
0063D2D0  mov      rcx, rdi
0063D2D3  mov      edx, 1
0063D2D8  call     0x80f420  ; -> 0080F420 fn
0063D2DD  movzx    edx, byte ptr [rbx]
0063D2E0  mov      rcx, rdi
0063D2E3  mov      rbx, qword ptr [rsp + 0x30]
0063D2E8  add      rsp, 0x20
0063D2EC  pop      rdi
0063D2ED  jmp      0x810450  ; -> 00810450 fn
```

## 00677850 (120 B, extent 00677850-006778C8)

Documented callee on this page: `0062FF50`

```
00677850  sub      rsp, 0x38
00677854  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0067785D  mov      ecx, dword ptr [rip + 0x28374d9]  ; -> 02EAED3C
00677863  mov      rax, qword ptr gs:[0x58]
0067786C  mov      edx, 4
00677871  mov      rcx, qword ptr [rax + rcx*8]
00677875  mov      eax, dword ptr [rdx + rcx]
00677878  cmp      dword ptr [rip + 0x26c7492], eax  ; -> 02D3ED10
0067787E  jle      0x6778bc  ; -> 006778BC
00677880  lea      rcx, [rip + 0x26c7489]  ; -> 02D3ED10
00677887  call     0x8092fc  ; -> 008092FC fn
0067788C  cmp      dword ptr [rip + 0x26c747d], -1  ; -> 02D3ED10
00677893  jne      0x6778bc  ; -> 006778BC
00677895  call     0x62ff50  ; -> 0062FF50 fn
0067789A  or       rax, 1
0067789E  mov      qword ptr [rip + 0x26c745b], rax  ; -> 02D3ED00
006778A5  mov      qword ptr [rip + 0x26c7458], 0  ; -> 02D3ED08
006778B0  lea      rcx, [rip + 0x26c7459]  ; -> 02D3ED10
006778B7  call     0x80929c  ; -> 0080929C fn
006778BC  lea      rax, [rip + 0x26c743d]  ; -> 02D3ED00
006778C3  add      rsp, 0x38
006778C7  ret      
```

## 00683A40 (145 B, extent 00683A40-00683AD1)

Documented callee on this page: `00810580`

```
00683A40  mov      qword ptr [rsp + 0x10], rbx
00683A45  mov      qword ptr [rsp + 0x18], rbp
00683A4A  mov      qword ptr [rsp + 0x20], rsi
00683A4F  push     r14
00683A51  sub      rsp, 0x20
00683A55  mov      r14d, edx
00683A58  mov      rsi, r9
00683A5B  xor      edx, edx
00683A5D  mov      rbp, r8
00683A60  mov      rbx, rcx
00683A63  call     0x8119f0  ; -> 008119F0 fn
00683A68  cmp      eax, 5
00683A6B  jne      0x683abb  ; -> 00683ABB
00683A6D  test     r14d, r14d
00683A70  je       0x683abb  ; -> 00683ABB
00683A72  mov      qword ptr [rsp + 0x30], rdi
00683A77  mov      edi, 1
00683A7C  nop      dword ptr [rax]
00683A80  mov      rdx, rdi
00683A83  mov      rcx, rbx
00683A86  call     0x810580  ; -> 00810580 fn
00683A8B  mov      edx, 0xfffffffe
00683A90  mov      rcx, rbx
00683A93  call     0x80fc70  ; -> 0080FC70 fn
00683A98  mov      rax, qword ptr [rsi]
00683A9B  mov      r8, rbp
00683A9E  mov      rdx, rbx
00683AA1  mov      rcx, rsi
00683AA4  call     qword ptr [rax + 0x18]
00683AA7  mov      eax, dword ptr [rsi + 0x38]
00683AAA  inc      rdi
00683AAD  add      rbp, rax
00683AB0  sub      r14, 1
00683AB4  jne      0x683a80  ; -> 00683A80
00683AB6  mov      rdi, qword ptr [rsp + 0x30]
00683ABB  mov      rbx, qword ptr [rsp + 0x38]
00683AC0  mov      rbp, qword ptr [rsp + 0x40]
00683AC5  mov      rsi, qword ptr [rsp + 0x48]
00683ACA  add      rsp, 0x20
00683ACE  pop      r14
00683AD0  ret      
```

## 00683FF0 (139 B, extent 00683FF0-0068407B)

Documented callee on this page: `00810580`

```
00683FF0  mov      qword ptr [rsp + 0x18], rbx
00683FF5  push     rbp
00683FF6  push     rsi
00683FF7  push     r14
00683FF9  sub      rsp, 0x20
00683FFD  mov      rsi, r8
00684000  mov      ebp, edx
00684002  xor      r8d, r8d
00684005  mov      r14, r9
00684008  mov      rbx, rcx
0068400B  call     0x80f740  ; -> 0080F740 fn
00684010  test     ebp, ebp
00684012  je       0x68406d  ; -> 0068406D
00684014  mov      qword ptr [rsp + 0x40], rdi
00684019  mov      edi, 1
0068401E  mov      qword ptr [rsp + 0x48], r15
00684023  mov      r15d, dword ptr [r14 + 0x38]
00684027  nop      word ptr [rax + rax]
00684030  mov      rdx, rdi
00684033  mov      rcx, rbx
00684036  call     0x810580  ; -> 00810580 fn
0068403B  mov      rax, qword ptr [r14]
0068403E  mov      r8, rsi
00684041  mov      rdx, rbx
00684044  mov      rcx, r14
00684047  call     qword ptr [rax + 0x20]
0068404A  mov      edx, 0xfffffffd
0068404F  mov      rcx, rbx
00684052  call     0x811090  ; -> 00811090 fn
00684057  inc      rdi
0068405A  add      rsi, r15
0068405D  sub      rbp, 1
00684061  jne      0x684030  ; -> 00684030
00684063  mov      r15, qword ptr [rsp + 0x48]
00684068  mov      rdi, qword ptr [rsp + 0x40]
0068406D  mov      rbx, qword ptr [rsp + 0x50]
00684072  add      rsp, 0x20
00684076  pop      r14
00684078  pop      rsi
00684079  pop      rbp
0068407A  ret      
```

## 006841F0 (143 B, extent 006841F0-0068427F)

Documented callee on this page: `00810580`

```
006841F0  mov      qword ptr [rsp + 0x10], rbx
006841F5  mov      qword ptr [rsp + 0x18], rbp
006841FA  mov      qword ptr [rsp + 0x20], rsi
006841FF  push     r14
00684201  sub      rsp, 0x20
00684205  mov      rsi, r8
00684208  mov      ebp, edx
0068420A  xor      r8d, r8d
0068420D  mov      r14, r9
00684210  mov      rbx, rcx
00684213  call     0x80f740  ; -> 0080F740 fn
00684218  test     ebp, ebp
0068421A  je       0x684269  ; -> 00684269
0068421C  mov      qword ptr [rsp + 0x30], rdi
00684221  mov      edi, 1
00684226  nop      word ptr [rax + rax]
00684230  mov      rdx, rdi
00684233  mov      rcx, rbx
00684236  call     0x810580  ; -> 00810580 fn
0068423B  mov      rax, qword ptr [r14]
0068423E  mov      r8, rsi
00684241  mov      rdx, rbx
00684244  mov      rcx, r14
00684247  call     qword ptr [rax + 0x30]
0068424A  mov      edx, 0xfffffffd
0068424F  mov      rcx, rbx
00684252  call     0x811090  ; -> 00811090 fn
00684257  inc      rdi
0068425A  add      rsi, 8
0068425E  sub      rbp, 1
00684262  jne      0x684230  ; -> 00684230
00684264  mov      rdi, qword ptr [rsp + 0x30]
00684269  mov      rbx, qword ptr [rsp + 0x38]
0068426E  mov      rbp, qword ptr [rsp + 0x40]
00684273  mov      rsi, qword ptr [rsp + 0x48]
00684278  add      rsp, 0x20
0068427C  pop      r14
0068427E  ret      
```

## 006843D0 (123 B, extent 006843D0-0068444B)

Documented callee on this page: `00810240`

```
006843D0  mov      qword ptr [rsp + 8], rbx
006843D5  mov      qword ptr [rsp + 0x10], rsi
006843DA  push     rdi
006843DB  sub      rsp, 0x20
006843DF  mov      rsi, rdx
006843E2  mov      rdi, rcx
006843E5  mov      edx, 0x10
006843EA  call     0x810240  ; -> 00810240 fn
006843EF  mov      rbx, rax
006843F2  test     rax, rax
006843F5  je       0x68443b  ; -> 0068443B
006843F7  lea      r8, [rip + 0x6ebd56]  ; -> 00D70154 [str "Vector"]
006843FE  mov      edx, 0xfff0b9d8
00684403  mov      rcx, rdi
00684406  call     0x80fa50  ; -> 0080FA50 fn
0068440B  mov      edx, 0xfffffffe
00684410  mov      rcx, rdi
00684413  call     0x810f60  ; -> 00810F60 fn
00684418  movss    xmm0, dword ptr [rsi]
0068441C  movss    xmm1, dword ptr [rsi + 4]
00684421  movss    xmm2, dword ptr [rsi + 8]
00684426  movss    dword ptr [rbx], xmm0
0068442A  movss    dword ptr [rbx + 4], xmm1
0068442F  movss    dword ptr [rbx + 8], xmm2
00684434  mov      dword ptr [rbx + 0xc], 0
0068443B  mov      rbx, qword ptr [rsp + 0x30]
00684440  mov      rsi, qword ptr [rsp + 0x38]
00684445  add      rsp, 0x20
00684449  pop      rdi
0068444A  ret      
```

## 00684A80 (34 B, extent 00684A80-00684AA2)

Documented callee on this page: `00683DC0`

```
00684A80  push     rbx
00684A82  sub      rsp, 0x20
00684A86  mov      rbx, rdx
00684A89  call     qword ptr [rcx + 8]
00684A8C  mov      rdx, rax
00684A8F  mov      rcx, rbx
00684A92  call     0x683dc0  ; -> 00683DC0 fn
00684A97  mov      eax, 1
00684A9C  add      rsp, 0x20
00684AA0  pop      rbx
00684AA1  ret      
```

## 006A6780 (117 B, extent 006A6780-006A67F5)

Documented callee on this page: `006301F0`

```
006A6780  mov      qword ptr [rsp + 8], rbx
006A6785  push     rdi
006A6786  sub      rsp, 0x30
006A678A  mov      rbx, r9
006A678D  mov      rdi, r8
006A6790  mov      rax, rcx
006A6793  test     rdx, rdx
006A6796  je       0x6a67e8  ; -> 006A67E8
006A6798  mov      rcx, rdx
006A679B  movaps   xmmword ptr [rsp + 0x20], xmm6
006A67A0  call     qword ptr [rax + 8]
006A67A3  movaps   xmm6, xmm0
006A67A6  test     rbx, rbx
006A67A9  je       0x6a67d6  ; -> 006A67D6
006A67AB  call     0x6301f0  ; -> 006301F0 fn
006A67B0  cmp      rdi, rax
006A67B3  jne      0x6a67d6  ; -> 006A67D6
006A67B5  movss    dword ptr [rbx + 8], xmm6
006A67BA  mov      eax, 1
006A67BF  movaps   xmm6, xmmword ptr [rsp + 0x20]
006A67C4  mov      qword ptr [rbx], 0
006A67CB  mov      rbx, qword ptr [rsp + 0x40]
006A67D0  add      rsp, 0x30
006A67D4  pop      rdi
006A67D5  ret      
006A67D6  xor      eax, eax
006A67D8  movaps   xmm6, xmmword ptr [rsp + 0x20]
006A67DD  mov      rbx, qword ptr [rsp + 0x40]
006A67E2  add      rsp, 0x30
006A67E6  pop      rdi
006A67E7  ret      
006A67E8  xor      eax, eax
006A67EA  mov      rbx, qword ptr [rsp + 0x40]
006A67EF  add      rsp, 0x30
006A67F3  pop      rdi
006A67F4  ret      
```

## 006A6970 (116 B, extent 006A6970-006A69E4)

Documented callee on this page: `00630490`

```
006A6970  mov      qword ptr [rsp + 0x18], rbx
006A6975  push     rsi
006A6976  sub      rsp, 0x20
006A697A  mov      rbx, r9
006A697D  mov      rsi, r8
006A6980  mov      rax, rcx
006A6983  test     rdx, rdx
006A6986  je       0x6a69d7  ; -> 006A69D7
006A6988  mov      rcx, rdx
006A698B  mov      qword ptr [rsp + 0x30], rdi
006A6990  call     qword ptr [rax + 8]
006A6993  movzx    edi, al
006A6996  test     rbx, rbx
006A6999  je       0x6a69c5  ; -> 006A69C5
006A699B  call     0x630490  ; -> 00630490 fn
006A69A0  cmp      rsi, rax
006A69A3  jne      0x6a69c5  ; -> 006A69C5
006A69A5  mov      byte ptr [rbx + 8], dil
006A69A9  mov      eax, 1
006A69AE  mov      rdi, qword ptr [rsp + 0x30]
006A69B3  mov      qword ptr [rbx], 0
006A69BA  mov      rbx, qword ptr [rsp + 0x40]
006A69BF  add      rsp, 0x20
006A69C3  pop      rsi
006A69C4  ret      
006A69C5  xor      eax, eax
006A69C7  mov      rdi, qword ptr [rsp + 0x30]
006A69CC  mov      rbx, qword ptr [rsp + 0x40]
006A69D1  add      rsp, 0x20
006A69D5  pop      rsi
006A69D6  ret      
006A69D7  xor      eax, eax
006A69D9  mov      rbx, qword ptr [rsp + 0x40]
006A69DE  add      rsp, 0x20
006A69E2  pop      rsi
006A69E3  ret      
```

## 006A7860 (120 B, extent 006A7860-006A78D8)

Documented callee on this page: `0062FF50`

```
006A7860  mov      qword ptr [rsp + 0x18], rbx
006A7865  push     rsi
006A7866  sub      rsp, 0x20
006A786A  mov      rbx, r9
006A786D  mov      rsi, r8
006A7870  mov      rax, rcx
006A7873  test     rdx, rdx
006A7876  je       0x6a78cb  ; -> 006A78CB
006A7878  mov      rcx, rdx
006A787B  mov      qword ptr [rsp + 0x30], rdi
006A7880  call     qword ptr [rax + 8]
006A7883  mov      rdi, rax
006A7886  test     rbx, rbx
006A7889  je       0x6a78b9  ; -> 006A78B9
006A788B  call     0x62ff50  ; -> 0062FF50 fn
006A7890  or       rax, 1
006A7894  cmp      rsi, rax
006A7897  jne      0x6a78b9  ; -> 006A78B9
006A7899  mov      qword ptr [rbx + 8], rdi
006A789D  mov      eax, 1
006A78A2  mov      rdi, qword ptr [rsp + 0x30]
006A78A7  mov      qword ptr [rbx], 0
006A78AE  mov      rbx, qword ptr [rsp + 0x40]
006A78B3  add      rsp, 0x20
006A78B7  pop      rsi
006A78B8  ret      
006A78B9  xor      eax, eax
006A78BB  mov      rdi, qword ptr [rsp + 0x30]
006A78C0  mov      rbx, qword ptr [rsp + 0x40]
006A78C5  add      rsp, 0x20
006A78C9  pop      rsi
006A78CA  ret      
006A78CB  xor      eax, eax
006A78CD  mov      rbx, qword ptr [rsp + 0x40]
006A78D2  add      rsp, 0x20
006A78D6  pop      rsi
006A78D7  ret      
```

## 006A9D10 (57 B, extent 006A9D10-006A9D49)

Documented callee on this page: `00810620`

```
006A9D10  push     rbx
006A9D12  sub      rsp, 0x20
006A9D16  mov      rbx, rdx
006A9D19  mov      rdx, qword ptr [r8]
006A9D1C  mov      rcx, rbx
006A9D1F  test     rdx, rdx
006A9D22  je       0x6a9d32  ; -> 006A9D32
006A9D24  mov      r8, qword ptr [r8 + 8]
006A9D28  add      rsp, 0x20
006A9D2C  pop      rbx
006A9D2D  jmp      0x684080  ; -> 00684080 fn
006A9D32  mov      edx, 1
006A9D37  call     0x80f420  ; -> 0080F420 fn
006A9D3C  mov      rcx, rbx
006A9D3F  add      rsp, 0x20
006A9D43  pop      rbx
006A9D44  jmp      0x810620  ; -> 00810620 fn
```

## 006B0110 (120 B, extent 006B0110-006B0188)

Documented callee on this page: `0062FF50`

```
006B0110  sub      rsp, 0x38
006B0114  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006B011D  mov      ecx, dword ptr [rip + 0x27fec19]  ; -> 02EAED3C
006B0123  mov      rax, qword ptr gs:[0x58]
006B012C  mov      edx, 4
006B0131  mov      rcx, qword ptr [rax + rcx*8]
006B0135  mov      eax, dword ptr [rdx + rcx]
006B0138  cmp      dword ptr [rip + 0x279ffea], eax  ; -> 02E50128
006B013E  jle      0x6b017c  ; -> 006B017C
006B0140  lea      rcx, [rip + 0x279ffe1]  ; -> 02E50128
006B0147  call     0x8092fc  ; -> 008092FC fn
006B014C  cmp      dword ptr [rip + 0x279ffd5], -1  ; -> 02E50128
006B0153  jne      0x6b017c  ; -> 006B017C
006B0155  call     0x62ff50  ; -> 0062FF50 fn
006B015A  or       rax, 1
006B015E  mov      qword ptr [rip + 0x279ffb3], rax  ; -> 02E50118
006B0165  mov      qword ptr [rip + 0x279ffb0], 0  ; -> 02E50120
006B0170  lea      rcx, [rip + 0x279ffb1]  ; -> 02E50128
006B0177  call     0x80929c  ; -> 0080929C fn
006B017C  lea      rax, [rip + 0x279ff95]  ; -> 02E50118
006B0183  add      rsp, 0x38
006B0187  ret      
```

## 006B3A40 (78 B, extent 006B3A40-006B3A8E)

Documented callee on this page: `00810620`

```
006B3A40  mov      qword ptr [rsp + 8], rbx
006B3A45  push     rdi
006B3A46  sub      rsp, 0x20
006B3A4A  mov      rdi, qword ptr [r8]
006B3A4D  mov      rbx, rdx
006B3A50  call     0x6b33f0  ; -> 006B33F0 fn
006B3A55  mov      rcx, rbx
006B3A58  test     rdi, rdi
006B3A5B  je       0x6b3a72  ; -> 006B3A72
006B3A5D  mov      r8, rax
006B3A60  mov      rdx, rdi
006B3A63  mov      rbx, qword ptr [rsp + 0x30]
006B3A68  add      rsp, 0x20
006B3A6C  pop      rdi
006B3A6D  jmp      0x6b3610  ; -> 006B3610 fn
006B3A72  mov      edx, 1
006B3A77  call     0x80f420  ; -> 0080F420 fn
006B3A7C  mov      rcx, rbx
006B3A7F  mov      rbx, qword ptr [rsp + 0x30]
006B3A84  add      rsp, 0x20
006B3A88  pop      rdi
006B3A89  jmp      0x810620  ; -> 00810620 fn
```

## 006DA380 (206 B, extent 006DA380-006DA44E)

Documented callee on this page: `0062FFC0`

```
006DA380  mov      qword ptr [rsp + 8], rbx
006DA385  mov      qword ptr [rsp + 0x10], rsi
006DA38A  mov      qword ptr [rsp + 0x18], rdi
006DA38F  push     r14
006DA391  sub      rsp, 0x30
006DA395  mov      r14, rdx
006DA398  mov      rbx, rcx
006DA39B  call     0x6b08a0  ; -> 006B08A0 fn
006DA3A0  mov      r8d, dword ptr [rbx]
006DA3A3  lea      rdx, [rbx + 0x30]
006DA3A7  mov      r10, qword ptr [r14]
006DA3AA  add      r8d, 3
006DA3AE  shr      r8d, 2
006DA3B2  mov      r9, rax
006DA3B5  mov      rcx, r14
006DA3B8  mov      dword ptr [rsp + 0x20], 0
006DA3C0  call     qword ptr [r10 + 8]
006DA3C4  call     0x6b0b20  ; -> 006B0B20 fn
006DA3C9  mov      edx, dword ptr [rbx]
006DA3CB  mov      r9, rax
006DA3CE  mov      r10, qword ptr [r14]
006DA3D1  add      edx, 3
006DA3D4  mov      r8d, dword ptr [rbx + 4]
006DA3D8  mov      rcx, r14
006DA3DB  shr      rdx, 2
006DA3DF  shl      rdx, 6
006DA3E3  add      rdx, 0x30
006DA3E7  mov      dword ptr [rsp + 0x20], 0
006DA3EF  add      rdx, rbx
006DA3F2  call     qword ptr [r10 + 8]
006DA3F6  mov      ecx, dword ptr [rbx]
006DA3F8  mov      edi, dword ptr [rbx + 4]
006DA3FB  add      ecx, 3
006DA3FE  mov      esi, dword ptr [rbx + 8]
006DA401  add      rdi, 3
006DA405  shr      rcx, 2
006DA409  lea      rdi, [rdi + rcx*4]
006DA40D  shl      rdi, 4
006DA411  add      rdi, rbx
006DA414  mov      rbx, qword ptr [r14]
006DA417  call     0x62ffc0  ; -> 0062FFC0 fn
006DA41C  mov      r9, rax
006DA41F  mov      dword ptr [rsp + 0x20], 0
006DA427  lea      r8d, [rsi*4]
006DA42F  mov      rdx, rdi
006DA432  mov      rcx, r14
006DA435  call     qword ptr [rbx + 8]
006DA438  mov      rbx, qword ptr [rsp + 0x40]
006DA43D  mov      rsi, qword ptr [rsp + 0x48]
006DA442  mov      rdi, qword ptr [rsp + 0x50]
006DA447  add      rsp, 0x30
006DA44B  pop      r14
006DA44D  ret      
```

## 0079A6C0 (91 B, extent 0079A6C0-0079A71B)

Documented callee on this page: `00810620`

```
0079A6C0  push     rbx
0079A6C2  sub      rsp, 0x40
0079A6C6  mov      rax, rcx
0079A6C9  mov      rbx, rdx
0079A6CC  lea      rcx, [rsp + 0x30]
0079A6D1  call     qword ptr [rax + 8]
0079A6D4  mov      rcx, rbx
0079A6D7  movups   xmm0, xmmword ptr [rax]
0079A6DA  movq     rdx, xmm0
0079A6DF  movaps   xmmword ptr [rsp + 0x20], xmm0
0079A6E4  test     rdx, rdx
0079A6E7  je       0x79a6fe  ; -> 0079A6FE
0079A6E9  mov      r8, qword ptr [rsp + 0x28]
0079A6EE  call     0x684080  ; -> 00684080 fn
0079A6F3  mov      eax, 1
0079A6F8  add      rsp, 0x40
0079A6FC  pop      rbx
0079A6FD  ret      
0079A6FE  mov      edx, 1
0079A703  call     0x80f420  ; -> 0080F420 fn
0079A708  mov      rcx, rbx
0079A70B  call     0x810620  ; -> 00810620 fn
0079A710  mov      eax, 1
0079A715  add      rsp, 0x40
0079A719  pop      rbx
0079A71A  ret      
```

## 007A32C0 (115 B, extent 007A32C0-007A3333)

Documented callee on this page: `00630110`

```
007A32C0  mov      qword ptr [rsp + 0x18], rbx
007A32C5  push     rsi
007A32C6  sub      rsp, 0x20
007A32CA  mov      rbx, r9
007A32CD  mov      rsi, r8
007A32D0  mov      rax, rcx
007A32D3  test     rdx, rdx
007A32D6  je       0x7a3326  ; -> 007A3326
007A32D8  lea      rcx, [rdx - 8]
007A32DC  mov      qword ptr [rsp + 0x30], rdi
007A32E1  call     qword ptr [rax + 8]
007A32E4  mov      edi, eax
007A32E6  test     rbx, rbx
007A32E9  je       0x7a3314  ; -> 007A3314
007A32EB  call     0x630110  ; -> 00630110 fn
007A32F0  cmp      rsi, rax
007A32F3  jne      0x7a3314  ; -> 007A3314
007A32F5  mov      dword ptr [rbx + 8], edi
007A32F8  mov      eax, 1
007A32FD  mov      rdi, qword ptr [rsp + 0x30]
007A3302  mov      qword ptr [rbx], 0
007A3309  mov      rbx, qword ptr [rsp + 0x40]
007A330E  add      rsp, 0x20
007A3312  pop      rsi
007A3313  ret      
007A3314  xor      eax, eax
007A3316  mov      rdi, qword ptr [rsp + 0x30]
007A331B  mov      rbx, qword ptr [rsp + 0x40]
007A3320  add      rsp, 0x20
007A3324  pop      rsi
007A3325  ret      
007A3326  xor      eax, eax
007A3328  mov      rbx, qword ptr [rsp + 0x40]
007A332D  add      rsp, 0x20
007A3331  pop      rsi
007A3332  ret      
```

## 007A3340 (115 B, extent 007A3340-007A33B3)

Documented callee on this page: `00630180`

```
007A3340  mov      qword ptr [rsp + 0x18], rbx
007A3345  push     rsi
007A3346  sub      rsp, 0x20
007A334A  mov      rbx, r9
007A334D  mov      rsi, r8
007A3350  mov      rax, rcx
007A3353  test     rdx, rdx
007A3356  je       0x7a33a6  ; -> 007A33A6
007A3358  lea      rcx, [rdx - 8]
007A335C  mov      qword ptr [rsp + 0x30], rdi
007A3361  call     qword ptr [rax + 8]
007A3364  mov      edi, eax
007A3366  test     rbx, rbx
007A3369  je       0x7a3394  ; -> 007A3394
007A336B  call     0x630180  ; -> 00630180 fn
007A3370  cmp      rsi, rax
007A3373  jne      0x7a3394  ; -> 007A3394
007A3375  mov      dword ptr [rbx + 8], edi
007A3378  mov      eax, 1
007A337D  mov      rdi, qword ptr [rsp + 0x30]
007A3382  mov      qword ptr [rbx], 0
007A3389  mov      rbx, qword ptr [rsp + 0x40]
007A338E  add      rsp, 0x20
007A3392  pop      rsi
007A3393  ret      
007A3394  xor      eax, eax
007A3396  mov      rdi, qword ptr [rsp + 0x30]
007A339B  mov      rbx, qword ptr [rsp + 0x40]
007A33A0  add      rsp, 0x20
007A33A4  pop      rsi
007A33A5  ret      
007A33A6  xor      eax, eax
007A33A8  mov      rbx, qword ptr [rsp + 0x40]
007A33AD  add      rsp, 0x20
007A33B1  pop      rsi
007A33B2  ret      
```

## 007A3450 (118 B, extent 007A3450-007A34C6)

Documented callee on this page: `00630260`

```
007A3450  mov      qword ptr [rsp + 8], rbx
007A3455  push     rdi
007A3456  sub      rsp, 0x30
007A345A  mov      rbx, r9
007A345D  mov      rdi, r8
007A3460  mov      rax, rcx
007A3463  test     rdx, rdx
007A3466  je       0x7a34b9  ; -> 007A34B9
007A3468  lea      rcx, [rdx - 8]
007A346C  movaps   xmmword ptr [rsp + 0x20], xmm6
007A3471  call     qword ptr [rax + 8]
007A3474  movaps   xmm6, xmm0
007A3477  test     rbx, rbx
007A347A  je       0x7a34a7  ; -> 007A34A7
007A347C  call     0x630260  ; -> 00630260 fn
007A3481  cmp      rdi, rax
007A3484  jne      0x7a34a7  ; -> 007A34A7
007A3486  movsd    qword ptr [rbx + 8], xmm6
007A348B  mov      eax, 1
007A3490  movaps   xmm6, xmmword ptr [rsp + 0x20]
007A3495  mov      qword ptr [rbx], 0
007A349C  mov      rbx, qword ptr [rsp + 0x40]
007A34A1  add      rsp, 0x30
007A34A5  pop      rdi
007A34A6  ret      
007A34A7  xor      eax, eax
007A34A9  movaps   xmm6, xmmword ptr [rsp + 0x20]
007A34AE  mov      rbx, qword ptr [rsp + 0x40]
007A34B3  add      rsp, 0x30
007A34B7  pop      rdi
007A34B8  ret      
007A34B9  xor      eax, eax
007A34BB  mov      rbx, qword ptr [rsp + 0x40]
007A34C0  add      rsp, 0x30
007A34C4  pop      rdi
007A34C5  ret      
```

## 007A3630 (123 B, extent 007A3630-007A36AB)

Documented callee on this page: `00630180`

```
007A3630  mov      qword ptr [rsp + 0x18], rbx
007A3635  push     rsi
007A3636  sub      rsp, 0x20
007A363A  mov      rbx, r9
007A363D  mov      r9, rcx
007A3640  mov      rsi, r8
007A3643  test     rdx, rdx
007A3646  je       0x7a369e  ; -> 007A369E
007A3648  movsxd   rax, dword ptr [rcx + 0x10]
007A364C  lea      rcx, [rdx - 8]
007A3650  add      rcx, rax
007A3653  mov      qword ptr [rsp + 0x30], rdi
007A3658  call     qword ptr [r9 + 8]
007A365C  mov      edi, eax
007A365E  test     rbx, rbx
007A3661  je       0x7a368c  ; -> 007A368C
007A3663  call     0x630180  ; -> 00630180 fn
007A3668  cmp      rsi, rax
007A366B  jne      0x7a368c  ; -> 007A368C
007A366D  mov      dword ptr [rbx + 8], edi
007A3670  mov      eax, 1
007A3675  mov      rdi, qword ptr [rsp + 0x30]
007A367A  mov      qword ptr [rbx], 0
007A3681  mov      rbx, qword ptr [rsp + 0x40]
007A3686  add      rsp, 0x20
007A368A  pop      rsi
007A368B  ret      
007A368C  xor      eax, eax
007A368E  mov      rdi, qword ptr [rsp + 0x30]
007A3693  mov      rbx, qword ptr [rsp + 0x40]
007A3698  add      rsp, 0x20
007A369C  pop      rsi
007A369D  ret      
007A369E  xor      eax, eax
007A36A0  mov      rbx, qword ptr [rsp + 0x40]
007A36A5  add      rsp, 0x20
007A36A9  pop      rsi
007A36AA  ret      
```
