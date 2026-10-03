# Homing pack: `23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-eastl-strings-containers-and-the-logging-allocator.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001A3F10 (404 B, extent 001A3F10-001A40A4)

Entered from (direct sites whose caller this page cites): `001A6A20` + 0xF8 (call; `001A6A20` is cited on this page); `001A6A20` + 0x225 (call; `001A6A20` is cited on this page)
Other direct sites: none

Host context: "allers on that layer**, not 2 separate relationships. Edge count from 'edges.tsv'. Read from the shipping bytes 2026-09-14 (OPUS).  **Resource — CLIENT (SWE2-EC7, batch 167, 1 edge).** The batch-167 '001A6A20' runtime 'basic_string' build is called by that layer's '001A9A30' - a Resource body constructing the '"start"' literal string through the shared '001EDF00' allocator attach; the crossing is that call, not a Resource responsibility" / "allers on that layer**, not 2 separate relationships. Edge count from 'edges.tsv'. Read from the shipping bytes 2026-09-14 (OPUS).  **Resource — CLIENT (SWE2-EC7, batch 167, 1 edge).** The batch-167 '001A6A20' runtime 'basic_string' build is called by that layer's '001A9A30' - a Resource body constructing the '"start"' literal string through the shared '001EDF00' allocator attach; the crossing is that call, not a Resource responsibility"

```
001A3F10  mov      qword ptr [rsp + 8], rbx
001A3F15  mov      qword ptr [rsp + 0x10], rbp
001A3F1A  mov      qword ptr [rsp + 0x18], rsi
001A3F1F  push     rdi
001A3F20  push     r12
001A3F22  push     r13
001A3F24  push     r14
001A3F26  push     r15
001A3F28  sub      rsp, 0x20
001A3F2C  mov      rbx, qword ptr [rcx + 0x18]
001A3F30  lea      rsi, [rcx + 8]
001A3F34  xor      ebp, ebp
001A3F36  mov      r12, r8
001A3F39  mov      r15, rdx
001A3F3C  mov      r14, rcx
001A3F3F  mov      rdi, rsi
001A3F42  mov      al, 1
001A3F44  test     rbx, rbx
001A3F47  je       0x1a3faf  ; -> 001A3FAF
001A3F49  mov      r13, qword ptr [r8]
001A3F4C  mov      rsi, qword ptr [r8 + 8]
001A3F50  sub      rsi, r13
001A3F53  nop      dword ptr [rax]
001A3F57  nop      word ptr [rax + rax]
001A3F60  mov      rdx, qword ptr [rbx + 0x20]
001A3F64  mov      r8, rsi
001A3F67  mov      rdi, qword ptr [rbx + 0x28]
001A3F6B  mov      rcx, r13
001A3F6E  sub      rdi, rdx
001A3F71  cmp      rdi, rsi
001A3F74  cmovl    r8, rdi
001A3F78  call     0x861ed2  ; -> 00861ED2 fn
001A3F7D  test     eax, eax
001A3F7F  jne      0x1a3f93  ; -> 001A3F93
001A3F81  cmp      rsi, rdi
001A3F84  jge      0x1a3f8b  ; -> 001A3F8B
001A3F86  or       eax, 0xffffffff
001A3F89  jmp      0x1a3f93  ; -> 001A3F93
001A3F8B  cmp      rsi, rdi
001A3F8E  mov      eax, ebp
001A3F90  setg     al
001A3F93  shr      eax, 0x1f
001A3F96  mov      rdi, rbx
001A3F99  test     al, al
001A3F9B  je       0x1a3fa3  ; -> 001A3FA3
001A3F9D  mov      rbx, qword ptr [rbx + 8]
001A3FA1  jmp      0x1a3fa6  ; -> 001A3FA6
001A3FA3  mov      rbx, qword ptr [rbx]
001A3FA6  test     rbx, rbx
001A3FA9  jne      0x1a3f60  ; -> 001A3F60
001A3FAB  lea      rsi, [r14 + 8]
001A3FAF  mov      r13, rdi
001A3FB2  test     al, al
001A3FB4  je       0x1a3fc7  ; -> 001A3FC7
001A3FB6  cmp      rdi, qword ptr [r14 + 0x10]
001A3FBA  je       0x1a4008  ; -> 001A4008
001A3FBC  mov      rcx, rdi
001A3FBF  call     0x16d720  ; -> 0016D720 fn
001A3FC4  mov      rdi, rax
001A3FC7  mov      rdx, qword ptr [r12]
001A3FCB  mov      rcx, qword ptr [rdi + 0x20]
001A3FCF  mov      rbx, qword ptr [rdi + 0x28]
001A3FD3  mov      rsi, qword ptr [r12 + 8]
001A3FD8  sub      rbx, rcx
001A3FDB  sub      rsi, rdx
001A3FDE  mov      r8, rbx
001A3FE1  cmp      rsi, rbx
001A3FE4  cmovl    r8, rsi
001A3FE8  call     0x861ed2  ; -> 00861ED2 fn
001A3FED  test     eax, eax
001A3FEF  jne      0x1a3ffd  ; -> 001A3FFD
001A3FF1  cmp      rbx, rsi
001A3FF4  jl       0x1a4038  ; -> 001A4038
001A3FF6  mov      eax, ebp
001A3FF8  setg     al
001A3FFB  test     eax, eax
001A3FFD  js       0x1a4038  ; -> 001A4038
001A3FFF  mov      qword ptr [r15], rdi
001A4002  mov      byte ptr [r15 + 8], bpl
001A4006  jmp      0x1a4084  ; -> 001A4084
001A4008  cmp      rdi, rsi
001A400B  je       0x1a4025  ; -> 001A4025
001A400D  lea      r8, [rdi + 0x20]
001A4011  mov      rdx, r12
001A4014  mov      rcx, r14
001A4017  call     0x1a3100  ; -> 001A3100 fn
001A401C  test     al, al
001A401E  jne      0x1a4025  ; -> 001A4025
001A4020  mov      ebp, 1
001A4025  mov      rdx, r12
001A4028  mov      rcx, r14
001A402B  call     0x1a3190  ; -> 001A3190 fn
001A4030  mov      r8, rsi
001A4033  mov      rdx, rdi
001A4036  jmp      0x1a406a  ; -> 001A406A
001A4038  lea      rdi, [r14 + 8]
001A403C  cmp      r13, rdi
001A403F  je       0x1a4059  ; -> 001A4059
001A4041  lea      r8, [r13 + 0x20]
001A4045  mov      rdx, r12
001A4048  mov      rcx, r14
001A404B  call     0x1a3100  ; -> 001A3100 fn
001A4050  test     al, al
001A4052  jne      0x1a4059  ; -> 001A4059
001A4054  mov      ebp, 1
001A4059  mov      rdx, r12
001A405C  mov      rcx, r14
001A405F  call     0x1a3190  ; -> 001A3190 fn
001A4064  mov      r8, rdi
001A4067  mov      rdx, r13
001A406A  mov      r9d, ebp
001A406D  mov      rcx, rax
001A4070  mov      rbx, rax
001A4073  call     0x16d840  ; -> 0016D840 fn
001A4078  inc      dword ptr [r14 + 0x28]
001A407C  mov      byte ptr [r15 + 8], 1
001A4081  mov      qword ptr [r15], rbx
001A4084  mov      rbx, qword ptr [rsp + 0x50]
001A4089  mov      rax, r15
001A408C  mov      rbp, qword ptr [rsp + 0x58]
001A4091  mov      rsi, qword ptr [rsp + 0x60]
001A4096  add      rsp, 0x20
001A409A  pop      r15
001A409C  pop      r14
001A409E  pop      r13
001A40A0  pop      r12
001A40A2  pop      rdi
001A40A3  ret      
```

## 001BC950 (126 B, extent 001BC950-001BC9CE)

Entered from (direct sites whose caller this page cites): `001BD1B0` + 0xA0 (call; `001BD1B0` is cited on this page); `001BD1B0` + 0x12D (call; `001BD1B0` is cited on this page)
Other direct sites: `001BD040` + 0xB9 (call); `001BD040` + 0x123 (call); `001BD340` + 0x75 (call)

Host context: "rd[node+0x20]' against '*rdx' ('cmp'/'cmov' lower-bound step), attaches the '008F3CC0' '\"EASTL list\"' allocator via '001EDF00' when no node owns the key, then splices a new node through '001BC8C0'/'001BD1B0' - the ordered-key insert-or-find the EASTL families share.  Interior anchor '001BCEA2' (function '001BCE30').  ## Per-member rows: the static string object each EASTL basic_string<char> initialiser builds (OPUS, 2026-10-03)  The f" / "rd[node+0x20]' against '*rdx' ('cmp'/'cmov' lower-bound step), attaches the '008F3CC0' '\"EASTL list\"' allocator via '001EDF00' when no node owns the key, then splices a new node through '001BC8C0'/'001BD1B0' - the ordered-key insert-or-find the EASTL families share.  Interior anchor '001BCEA2' (function '001BCE30').  ## Per-member rows: the static string object each EASTL basic_string<char> initialiser builds (OPUS, 2026-10-03)  The f"

```
001BC950  mov      qword ptr [rsp + 8], rcx
001BC955  push     rdi
001BC956  sub      rsp, 0x40
001BC95A  mov      qword ptr [rsp + 0x30], 0xfffffffffffffffe
001BC963  mov      qword ptr [rsp + 0x58], rbx
001BC968  mov      qword ptr [rsp + 0x60], rsi
001BC96D  mov      rsi, rcx
001BC970  mov      rax, qword ptr [rdx]
001BC973  mov      qword ptr [rcx], rax
001BC976  lea      rbx, [rdx + 8]
001BC97A  lea      rdi, [rcx + 8]
001BC97E  mov      qword ptr [rsp + 0x50], rdi
001BC983  xor      eax, eax
001BC985  mov      qword ptr [rdi], rax
001BC988  mov      qword ptr [rdi + 8], rax
001BC98C  lea      rdx, [rbx + 0x10]
001BC990  lea      rcx, [rdi + 0x10]
001BC994  call     0x1edf00  ; -> 001EDF00 fn
001BC999  mov      qword ptr [rdi], rdi
001BC99C  mov      qword ptr [rdi + 8], rdi
001BC9A0  movzx    eax, byte ptr [rsp + 0x50]
001BC9A5  mov      byte ptr [rsp + 0x20], al
001BC9A9  mov      r9, rbx
001BC9AC  mov      r8, qword ptr [rbx]
001BC9AF  mov      rdx, rdi
001BC9B2  mov      rcx, rdi
001BC9B5  call     0x1bc8c0  ; -> 001BC8C0 fn
001BC9BA  nop      
001BC9BB  mov      rax, rsi
001BC9BE  mov      rbx, qword ptr [rsp + 0x58]
001BC9C3  mov      rsi, qword ptr [rsp + 0x60]
001BC9C8  add      rsp, 0x40
001BC9CC  pop      rdi
001BC9CD  ret      
```

## 001BD340 (167 B, extent 001BD340-001BD3E7)

Entered from (direct sites whose caller this page cites): `001BD1B0` + 0xD0 (call; `001BD1B0` is cited on this page)
Other direct sites: none

Host context: "rd[node+0x20]' against '*rdx' ('cmp'/'cmov' lower-bound step), attaches the '008F3CC0' '\"EASTL list\"' allocator via '001EDF00' when no node owns the key, then splices a new node through '001BC8C0'/'001BD1B0' - the ordered-key insert-or-find the EASTL families share.  Interior anchor '001BCEA2' (function '001BCE30').  ## Per-member rows: the static string object each EASTL basic_string<char> initialiser builds (OPUS, 2026-10-03)  The f"

```
001BD340  push     rbp
001BD342  push     rsi
001BD343  push     rdi
001BD344  push     r14
001BD346  push     r15
001BD348  sub      rsp, 0x30
001BD34C  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001BD355  mov      qword ptr [rsp + 0x70], rbx
001BD35A  mov      rbp, r9
001BD35D  mov      rdi, r8
001BD360  mov      r15, rdx
001BD363  mov      rbx, rcx
001BD366  cmp      byte ptr [rsp + 0x80], 0
001BD36E  jne      0x1bd389  ; -> 001BD389
001BD370  lea      rax, [rcx + 8]
001BD374  cmp      r8, rax
001BD377  je       0x1bd389  ; -> 001BD389
001BD379  mov      rax, qword ptr [r8 + 0x20]
001BD37D  cmp      qword ptr [r9], rax
001BD380  jb       0x1bd389  ; -> 001BD389
001BD382  mov      esi, 1
001BD387  jmp      0x1bd38b  ; -> 001BD38B
001BD389  xor      esi, esi
001BD38B  add      rcx, 0x30
001BD38F  mov      rax, qword ptr [rcx]
001BD392  xor      r8d, r8d
001BD395  lea      edx, [r8 + 0x40]
001BD399  call     qword ptr [rax + 0x10]
001BD39C  mov      r14, rax
001BD39F  mov      qword ptr [rsp + 0x60], rax
001BD3A4  lea      rcx, [rax + 0x20]
001BD3A8  mov      qword ptr [rsp + 0x68], rcx
001BD3AD  test     rcx, rcx
001BD3B0  je       0x1bd3bb  ; -> 001BD3BB
001BD3B2  mov      rdx, rbp
001BD3B5  call     0x1bc950  ; -> 001BC950 fn
001BD3BA  nop      
001BD3BB  lea      r8, [rbx + 8]
001BD3BF  mov      r9d, esi
001BD3C2  mov      rdx, rdi
001BD3C5  mov      rcx, r14
001BD3C8  call     0x16d840  ; -> 0016D840 fn
001BD3CD  inc      dword ptr [rbx + 0x28]
001BD3D0  mov      qword ptr [r15], r14
001BD3D3  mov      rax, r15
001BD3D6  mov      rbx, qword ptr [rsp + 0x70]
001BD3DB  add      rsp, 0x30
001BD3DF  pop      r15
001BD3E1  pop      r14
001BD3E3  pop      rdi
001BD3E4  pop      rsi
001BD3E5  pop      rbp
001BD3E6  ret      
```
