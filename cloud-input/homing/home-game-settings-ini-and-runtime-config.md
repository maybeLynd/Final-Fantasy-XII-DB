# Homing pack: `19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md`

Generated 2026-10-03 08:08 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-game-settings-ini-and-runtime-config.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001E0B00 (144 B, extent 001E0B00-001E0B90)

Entered from (direct sites whose caller this page cites): `0023CAF0` + 0x3F (call; `0023CAF0` is cited on this page)
Other direct sites: none

Host context: "jumps at '001F3A00+0x44' with (the incoming 'rdx', 3) | Interior anchor '001F3A09'; Interior anchor '001F3A1B'; Interior anchor '001F3A28'; Interior anchor '001F3A32'; Interior anchor '001F3A44' | | '0023CAF0' | 412 B | with P0..P4 the qwords at '+0', '+8', '+0x10', '+0x18', '+0x20' of qword 'rdx+0x10', i the sign-extended 'r9d', set/clear meaning OR 1/AND 0xfffffffe on a Pk's dword '+8', and S(x) storing the result of the function call"

```
001E0B00  mov      qword ptr [rsp + 8], rbx
001E0B05  mov      qword ptr [rsp + 0x10], rsi
001E0B0A  push     rdi
001E0B0B  sub      rsp, 0x20
001E0B0F  mov      edi, ecx
001E0B11  mov      esi, 0x46e1
001E0B16  xor      ecx, ecx
001E0B18  xor      ebx, ebx
001E0B1A  call     qword ptr [rip + 0x6e1e98]  ; -> 008C29B8 [u64 0x0000000001CCC826]
001E0B20  and      eax, 0xfff
001E0B25  cmp      eax, 0x40c
001E0B2A  jne      0x1e0b33  ; -> 001E0B33
001E0B2C  mov      ebx, 1
001E0B31  jmp      0x1e0b40  ; -> 001E0B40
001E0B33  cmp      eax, 0x407
001E0B38  mov      ecx, 2
001E0B3D  cmove    ebx, ecx
001E0B40  sub      ebx, 1
001E0B43  je       0x1e0b51  ; -> 001E0B51
001E0B45  cmp      ebx, 1
001E0B48  jne      0x1e0b56  ; -> 001E0B56
001E0B4A  mov      esi, 0x47b1
001E0B4F  jmp      0x1e0b56  ; -> 001E0B56
001E0B51  mov      esi, 0x4749
001E0B56  cmp      edi, 0x1c
001E0B59  jl       0x1e0b70  ; -> 001E0B70
001E0B5B  lea      eax, [rdi - 0x1c]
001E0B5E  add      eax, esi
001E0B60  mov      rbx, qword ptr [rsp + 0x30]
001E0B65  mov      rsi, qword ptr [rsp + 0x38]
001E0B6A  add      rsp, 0x20
001E0B6E  pop      rdi
001E0B6F  ret      
001E0B70  lea      eax, [rdi + 0x46dd]
001E0B76  cmp      edi, 1
001E0B79  jge      0x1e0b80  ; -> 001E0B80
001E0B7B  mov      eax, 0x46dc
001E0B80  mov      rbx, qword ptr [rsp + 0x30]
001E0B85  mov      rsi, qword ptr [rsp + 0x38]
001E0B8A  add      rsp, 0x20
001E0B8E  pop      rdi
001E0B8F  ret      
```

## 003B7A30 (117 B, extent 003B7A30-003B7AA5)

Entered from (direct sites whose caller this page cites): `00348DA0` + 0x15 (jmp; `00348DA0` is cited on this page)
Other direct sites: none

Host context: " | | '00348A70' | 26 B | tail-jumps at '00348A70+0x15' with 'rcx' = '00263FF0(3)' | Interior anchor '00348A74'; Interior anchor '00348A79'; Interior anchor '00348A7E'; Interior anchor '00348A85' | | '00348DA0' | 26 B | tail-jumps at '00348DA0+0x15' with 'rcx' = '00263FF0(3)' | Interior anchor '00348DA4'; Interior anchor '00348DA9'; Interior anchor '00348DAE'; Interior anchor '00348DB5' | | '00357170' | 36 B | calls '00263FF0(0)', then t"

```
003B7A30  push     rbx
003B7A32  sub      rsp, 0x20
003B7A36  mov      rcx, qword ptr [rip + 0x2b0522b]  ; -> 02EBCC68
003B7A3D  test     rcx, rcx
003B7A40  je       0x3b7a54  ; -> 003B7A54
003B7A42  call     0x263f40  ; -> 00263F40 fn
003B7A47  mov      edx, 1
003B7A4C  mov      rcx, rax
003B7A4F  call     0x2693d0  ; -> 002693D0 fn
003B7A54  mov      eax, dword ptr [rip + 0x2b05166]  ; -> 02EBCBC0
003B7A5A  xor      ebx, ebx
003B7A5C  test     eax, eax
003B7A5E  jle      0x3b7a9f  ; -> 003B7A9F
003B7A60  mov      qword ptr [rsp + 0x30], rdi
003B7A65  lea      rdi, [rip + 0x2b05054]  ; -> 02EBCAC0
003B7A6C  nop      dword ptr [rax]
003B7A70  mov      rcx, qword ptr [rdi]
003B7A73  test     rcx, rcx
003B7A76  je       0x3b7a90  ; -> 003B7A90
003B7A78  call     0x263f40  ; -> 00263F40 fn
003B7A7D  mov      edx, 1
003B7A82  mov      rcx, rax
003B7A85  call     0x2693d0  ; -> 002693D0 fn
003B7A8A  mov      eax, dword ptr [rip + 0x2b05130]  ; -> 02EBCBC0
003B7A90  inc      ebx
003B7A92  add      rdi, 8
003B7A96  cmp      ebx, eax
003B7A98  jl       0x3b7a70  ; -> 003B7A70
003B7A9A  mov      rdi, qword ptr [rsp + 0x30]
003B7A9F  add      rsp, 0x20
003B7AA3  pop      rbx
003B7AA4  ret      
```

## 003B7AB0 (78 B, extent 003B7AB0-003B7AFE)

Entered from (direct sites whose caller this page cites): `003484A0` + 0x15 (jmp; `003484A0` is cited on this page)
Other direct sites: none

Host context: "mps at '002D5590+0x1D' with 'rcx' and 'rdx' unchanged | Interior anchor '002D55AD'; Interior anchor '002D55B8'; Interior anchor '002D55D5'; Interior anchor '002D55F3'; Interior anchor '002D564D' | | '003484A0' | 26 B | tail-jumps at '003484A0+0x15' with 'rcx' = '00263FF0(3)' | Interior anchor '003484A4'; Interior anchor '003484A9'; Interior anchor '003484AE'; Interior anchor '003484B5' | | '00348A70' | 26 B | tail-jumps at '00348A70+0x1"

```
003B7AB0  push     rbx
003B7AB2  sub      rsp, 0x20
003B7AB6  xor      ebx, ebx
003B7AB8  cmp      dword ptr [rip + 0x2b04fe2], ebx  ; -> 02EBCAA0
003B7ABE  jle      0x3b7af8  ; -> 003B7AF8
003B7AC0  mov      qword ptr [rsp + 0x30], rdi
003B7AC5  lea      rdi, [rip + 0x2b04fb4]  ; -> 02EBCA80
003B7ACC  nop      dword ptr [rax]
003B7AD0  mov      rcx, qword ptr [rdi]
003B7AD3  call     0x263f40  ; -> 00263F40 fn
003B7AD8  mov      edx, 1
003B7ADD  mov      rcx, rax
003B7AE0  call     0x2693d0  ; -> 002693D0 fn
003B7AE5  inc      ebx
003B7AE7  lea      rdi, [rdi + 8]
003B7AEB  cmp      ebx, dword ptr [rip + 0x2b04faf]  ; -> 02EBCAA0
003B7AF1  jl       0x3b7ad0  ; -> 003B7AD0
003B7AF3  mov      rdi, qword ptr [rsp + 0x30]
003B7AF8  add      rsp, 0x20
003B7AFC  pop      rbx
003B7AFD  ret      
```
