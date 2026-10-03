# F homing pack: `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md`

Generated 2026-10-02 21:45 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 5. No bearing page cites them and no documented function calls them directly.

## 002ECDC0 (63 B, extent 002ECDC0-002ECDFF)

Documented callee on this page: `002E8FD0`

```
002ECDC0  cmp      byte ptr [rcx + 0x18], 1
002ECDC4  je       0x2ecdfe  ; -> 002ECDFE
002ECDC6  movzx    eax, byte ptr [rcx + 3]
002ECDCA  and      al, 0xe0
002ECDCC  cmp      al, 0x60
002ECDCE  jne      0x2ecdfe  ; -> 002ECDFE
002ECDD0  mov      rax, qword ptr [rcx + 0xc0]
002ECDD7  test     rax, rax
002ECDDA  je       0x2ecdef  ; -> 002ECDEF
002ECDDC  and      byte ptr [rax + 0x70], 0xfe
002ECDE0  add      rax, 0x60
002ECDE4  and      dl, 1
002ECDE7  or       byte ptr [rax + 0x10], dl
002ECDEA  jmp      0x2e8fd0  ; -> 002E8FD0 fn
002ECDEF  and      byte ptr [rax + 0x10], 0xfe
002ECDF3  and      dl, 1
002ECDF6  or       byte ptr [rax + 0x10], dl
002ECDF9  jmp      0x2e8fd0  ; -> 002E8FD0 fn
002ECDFE  ret      
```

## 002ECE00 (63 B, extent 002ECE00-002ECE3F)

Documented callee on this page: `002E8FD0`

```
002ECE00  cmp      byte ptr [rcx + 0x18], 1
002ECE04  je       0x2ece3e  ; -> 002ECE3E
002ECE06  movzx    eax, byte ptr [rcx + 3]
002ECE0A  and      al, 0xe0
002ECE0C  cmp      al, 0x60
002ECE0E  jne      0x2ece3e  ; -> 002ECE3E
002ECE10  mov      rax, qword ptr [rcx + 0xc0]
002ECE17  test     rax, rax
002ECE1A  je       0x2ece2f  ; -> 002ECE2F
002ECE1C  and      byte ptr [rax + 0x40], 0xfe
002ECE20  add      rax, 0x30
002ECE24  and      dl, 1
002ECE27  or       byte ptr [rax + 0x10], dl
002ECE2A  jmp      0x2e8fd0  ; -> 002E8FD0 fn
002ECE2F  and      byte ptr [rax + 0x10], 0xfe
002ECE33  and      dl, 1
002ECE36  or       byte ptr [rax + 0x10], dl
002ECE39  jmp      0x2e8fd0  ; -> 002E8FD0 fn
002ECE3E  ret      
```

## 0034DF40 (81 B, extent 0034DF40-0034DF91)

Documented callee on this page: `002E8060`

```
0034DF40  mov      qword ptr [rsp + 8], rbx
0034DF45  push     rdi
0034DF46  sub      rsp, 0x20
0034DF4A  xor      ebx, ebx
0034DF4C  nop      dword ptr [rax]
0034DF50  mov      ecx, ebx
0034DF52  call     0x263750  ; -> 00263750 fn
0034DF57  mov      rdi, rax
0034DF5A  test     rax, rax
0034DF5D  je       0x34df7f  ; -> 0034DF7F
0034DF5F  mov      rcx, rax
0034DF62  call     0x263f40  ; -> 00263F40 fn
0034DF67  mov      rcx, rax
0034DF6A  call     0x2e8060  ; -> 002E8060 fn
0034DF6F  mov      rcx, rdi
0034DF72  call     0x263f40  ; -> 00263F40 fn
0034DF77  mov      rcx, rax
0034DF7A  call     0x2eb430  ; -> 002EB430 fn
0034DF7F  inc      ebx
0034DF81  cmp      ebx, 4
0034DF84  jl       0x34df50  ; -> 0034DF50
0034DF86  mov      rbx, qword ptr [rsp + 0x30]
0034DF8B  add      rsp, 0x20
0034DF8F  pop      rdi
0034DF90  ret      
```

## 0034F5A0 (211 B, extent 0034F5A0-0034F673)

Documented callee on this page: `0031B510`

```
0034F5A0  mov      qword ptr [rsp + 0x10], rbx
0034F5A5  push     rbp
0034F5A6  push     rsi
0034F5A7  push     rdi
0034F5A8  sub      rsp, 0x60
0034F5AC  mov      rax, qword ptr [rip + 0x1bf527d]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0034F5B3  xor      rax, rsp
0034F5B6  mov      qword ptr [rsp + 0x50], rax
0034F5BB  mov      rsi, r9
0034F5BE  mov      rbx, rcx
0034F5C1  call     0x2640c0  ; -> 002640C0 fn
0034F5C6  mov      rbp, rax
0034F5C9  mov      edi, 3
0034F5CE  nop      
0034F5D0  mov      rcx, rsi
0034F5D3  call     0x267e10  ; -> 00267E10 fn
0034F5D8  mov      r8d, eax
0034F5DB  mov      rdx, rbx
0034F5DE  mov      rcx, rbp
0034F5E1  call     0x2650b0  ; -> 002650B0 fn
0034F5E6  mov      qword ptr [rsp + rdi*8 + 0x30], rax
0034F5EB  sub      rdi, 1
0034F5EF  jns      0x34f5d0  ; -> 0034F5D0
0034F5F1  mov      edi, 4
0034F5F6  lea      rcx, [rsp + 0x20]
0034F5FB  mov      edx, edi
0034F5FD  call     0x31b510  ; -> 0031B510 fn
0034F602  movsxd   r8, eax
0034F605  cmp      r8d, edi
0034F608  jge      0x34f61f  ; -> 0034F61F
0034F60A  sub      edi, r8d
0034F60D  movsxd   rcx, edi
0034F610  or       rax, 0xffffffffffffffff
0034F614  lea      rdi, [rsp + 0x20]
0034F619  lea      rdi, [rdi + r8*4]
0034F61D  rep stosd dword ptr [rdi], eax
0034F61F  mov      edi, dword ptr [rsp + 0x20]
0034F623  mov      rcx, rbx
0034F626  mov      rdx, qword ptr [rsp + 0x30]
0034F62B  mov      rax, qword ptr [rsp + 0x38]
0034F630  mov      dword ptr [rdx], edi
0034F632  mov      edx, dword ptr [rsp + 0x24]
0034F636  mov      dword ptr [rax], edx
0034F638  mov      edx, dword ptr [rsp + 0x28]
0034F63C  mov      rax, qword ptr [rsp + 0x40]
0034F641  mov      dword ptr [rax], edx
0034F643  mov      edx, dword ptr [rsp + 0x2c]
0034F647  mov      rax, qword ptr [rsp + 0x48]
0034F64C  mov      dword ptr [rax], edx
0034F64E  mov      edx, r8d
0034F651  call     0x26b4e0  ; -> 0026B4E0 fn
0034F656  mov      rcx, qword ptr [rsp + 0x50]
0034F65B  xor      rcx, rsp
0034F65E  call     0x808c40  ; -> 00808C40 fn
0034F663  mov      rbx, qword ptr [rsp + 0x88]
0034F66B  add      rsp, 0x60
0034F66F  pop      rdi
0034F670  pop      rsi
0034F671  pop      rbp
0034F672  ret      
```

## 003599A0 (137 B, extent 003599A0-00359A29)

Documented callee on this page: `002E9600`

```
003599A0  mov      qword ptr [rsp + 0x18], rbx
003599A5  push     rdi
003599A6  push     r14
003599A8  push     r15
003599AA  sub      rsp, 0x20
003599AE  xor      ebx, ebx
003599B0  mov      qword ptr [rsp + 0x48], rsi
003599B5  mov      r14d, ecx
003599B8  mov      r15, rdx
003599BB  mov      rsi, rdx
003599BE  mov      rdi, rdx
003599C1  test     ecx, ecx
003599C3  jle      0x3599fc  ; -> 003599FC
003599C5  mov      qword ptr [rsp + 0x40], rbp
003599CA  mov      ebp, r14d
003599CD  nop      dword ptr [rax]
003599D0  mov      rcx, qword ptr [rdi]
003599D3  test     rcx, rcx
003599D6  je       0x3599ed  ; -> 003599ED
003599D8  call     0x2e9600  ; -> 002E9600 fn
003599DD  test     eax, eax
003599DF  je       0x3599ed  ; -> 003599ED
003599E1  mov      rax, qword ptr [rdi]
003599E4  mov      qword ptr [rsi], rax
003599E7  add      rsi, 8
003599EB  inc      ebx
003599ED  add      rdi, 8
003599F1  sub      rbp, 1
003599F5  jne      0x3599d0  ; -> 003599D0
003599F7  mov      rbp, qword ptr [rsp + 0x40]
003599FC  mov      rsi, qword ptr [rsp + 0x48]
00359A01  cmp      ebx, r14d
00359A04  jge      0x359a18  ; -> 00359A18
00359A06  sub      r14d, ebx
00359A09  movsxd   rdx, ebx
00359A0C  movsxd   rcx, r14d
00359A0F  xor      eax, eax
00359A11  lea      rdi, [r15 + rdx*8]
00359A15  rep stosq qword ptr [rdi], rax
00359A18  mov      eax, ebx
00359A1A  mov      rbx, qword ptr [rsp + 0x50]
00359A1F  add      rsp, 0x20
00359A23  pop      r15
00359A25  pop      r14
00359A27  pop      rdi
00359A28  ret      
```
