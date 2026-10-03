# Homing pack: `24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-what-the-game-asks-windows-for.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00159520 (95 B, extent 00159520-0015957F)

Entered from (direct sites whose caller this page cites): `0015B820` + 0x35 (call; `0015B820` is cited on this page)
Other direct sites: `0015B550` + 0x5D (call)

Host context: "s on 'rdx''s alternate name.  Interior anchor '00159605' (function '001595F0').  '0015B440' (265 B) is the wide path join the enumeration layer calls to glue a directory and a leaf name ('0015B5F0', '0015B820'): two 'repne scasw' lengths, an 'ebp = 1' separator flag only when the left part does not already end in '\' and the right part does not begin with one, '(len1 + sep + len2) * 2 + pad' sized allocation through IAT '008C2348', then"

```
00159520  sub      rsp, 8
00159524  mov      rdx, rcx
00159527  test     rcx, rcx
0015952A  je       0x15956e  ; -> 0015956E
0015952C  mov      qword ptr [rsp], rdi
00159530  or       rcx, 0xffffffffffffffff
00159534  xor      eax, eax
00159536  mov      rdi, rdx
00159539  xor      r8d, r8d
0015953C  repne scasw ax, word ptr [rdi]
0015953F  mov      rdi, qword ptr [rsp]
00159543  not      rcx
00159546  sub      rcx, 1
0015954A  je       0x15956e  ; -> 0015956E
0015954C  nop      dword ptr [rax]
00159550  movzx    eax, word ptr [rdx]
00159553  cmp      ax, 0x5c
00159557  je       0x159575  ; -> 00159575
00159559  cmp      ax, 0x2f
0015955D  je       0x159575  ; -> 00159575
0015955F  inc      r8d
00159562  add      rdx, 2
00159566  mov      eax, r8d
00159569  cmp      rax, rcx
0015956C  jb       0x159550  ; -> 00159550
0015956E  xor      eax, eax
00159570  add      rsp, 8
00159574  ret      
00159575  mov      eax, 1
0015957A  add      rsp, 8
0015957E  ret      
```

## 00159580 (109 B, extent 00159580-001595ED)

Entered from (direct sites whose caller this page cites): `0015B820` + 0x24C (call; `0015B820` is cited on this page)
Other direct sites: none

Host context: "s on 'rdx''s alternate name.  Interior anchor '00159605' (function '001595F0').  '0015B440' (265 B) is the wide path join the enumeration layer calls to glue a directory and a leaf name ('0015B5F0', '0015B820'): two 'repne scasw' lengths, an 'ebp = 1' separator flag only when the left part does not already end in '\' and the right part does not begin with one, '(len1 + sep + len2) * 2 + pad' sized allocation through IAT '008C2348', then"

```
00159580  mov      qword ptr [rsp + 8], rbx
00159585  push     rdi
00159586  sub      rsp, 0x20
0015958A  xor      ecx, ecx
0015958C  call     qword ptr [rip + 0x768dc6]  ; -> 008C2358 [u64 0x0000000001CCC724]
00159592  xor      edx, edx
00159594  xor      ecx, ecx
00159596  call     qword ptr [rip + 0x768db4]  ; -> 008C2350 [u64 0x0000000001CCC70E]
0015959C  mov      ecx, 0x40
001595A1  mov      edx, eax
001595A3  mov      edi, eax
001595A5  add      rdx, rdx
001595A8  call     qword ptr [rip + 0x768d9a]  ; -> 008C2348 [u64 0x0000000001CCC700]
001595AE  mov      rbx, rax
001595B1  test     rax, rax
001595B4  je       0x1595e2  ; -> 001595E2
001595B6  mov      edx, edi
001595B8  mov      rcx, rax
001595BB  call     qword ptr [rip + 0x768d8f]  ; -> 008C2350 [u64 0x0000000001CCC70E]
001595C1  test     eax, eax
001595C3  je       0x1595d7  ; -> 001595D7
001595C5  cmp      edi, eax
001595C7  jb       0x1595d7  ; -> 001595D7
001595C9  mov      rax, rbx
001595CC  mov      rbx, qword ptr [rsp + 0x30]
001595D1  add      rsp, 0x20
001595D5  pop      rdi
001595D6  ret      
001595D7  mov      rcx, rbx
001595DA  call     qword ptr [rip + 0x768c18]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
001595E0  xor      eax, eax
001595E2  mov      rbx, qword ptr [rsp + 0x30]
001595E7  add      rsp, 0x20
001595EB  pop      rdi
001595EC  ret      
```

## 0015B550 (146 B, extent 0015B550-0015B5E2)

Entered from (direct sites whose caller this page cites): `0015BB30` + 0xB5 (call; `0015BB30` is cited on this page)
Other direct sites: none

Host context: "E0'/'001599D0' copy both halves into the fresh buffer - a manual PathCombineW.  Interior anchor '0015B4D5' (function '0015B440').  '0015A240' (235 B) is the lazy OS-build cache '0015B110'/'0015B820'/'0015BB30' consult: if 'dword[02EAECE0]' is zero it calls '0015A0E0' with 'rcx = 0xFFFFFFFF80000002' (HKEY_LOCAL_MACHINE) against 'SOFTWARE\Microsoft\Windows NT\CurrentVersion' / 'CurrentBuildNumber' ('01CC6CA0'/'01CC6D00'), and only when th"

```
0015B550  mov      qword ptr [rsp + 8], rbx
0015B555  push     rdi
0015B556  sub      rsp, 0x20
0015B55A  mov      edi, edx
0015B55C  mov      rbx, rcx
0015B55F  test     rcx, rcx
0015B562  je       0x15b5aa  ; -> 0015B5AA
0015B564  movzx    eax, word ptr [rcx]
0015B567  cmp      ax, 0x5c
0015B56B  je       0x15b596  ; -> 0015B596
0015B56D  cmp      ax, 0x2f
0015B571  je       0x15b596  ; -> 0015B596
0015B573  movzx    ecx, ax
0015B576  call     0x861f92  ; -> 00861F92 fn
0015B57B  test     eax, eax
0015B57D  je       0x15b5aa  ; -> 0015B5AA
0015B57F  cmp      word ptr [rbx + 2], 0x3a
0015B584  jne      0x15b5aa  ; -> 0015B5AA
0015B586  movzx    eax, word ptr [rbx + 4]
0015B58A  cmp      ax, 0x5c
0015B58E  je       0x15b596  ; -> 0015B596
0015B590  cmp      ax, 0x2f
0015B594  jne      0x15b5aa  ; -> 0015B5AA
0015B596  mov      edx, edi
0015B598  mov      rcx, rbx
0015B59B  mov      rbx, qword ptr [rsp + 0x30]
0015B5A0  add      rsp, 0x20
0015B5A4  pop      rdi
0015B5A5  jmp      0x15b070  ; -> 0015B070 fn
0015B5AA  mov      rcx, rbx
0015B5AD  call     0x159520  ; -> 00159520 fn
0015B5B2  test     eax, eax
0015B5B4  jne      0x15b5ca  ; -> 0015B5CA
0015B5B6  mov      edx, edi
0015B5B8  mov      rcx, rbx
0015B5BB  mov      rbx, qword ptr [rsp + 0x30]
0015B5C0  add      rsp, 0x20
0015B5C4  pop      rdi
0015B5C5  jmp      0x159aa0  ; -> 00159AA0 fn
0015B5CA  mov      ecx, 0x7e
0015B5CF  call     qword ptr [rip + 0x766d83]  ; -> 008C2358 [u64 0x0000000001CCC724]
0015B5D5  mov      rbx, qword ptr [rsp + 0x30]
0015B5DA  xor      eax, eax
0015B5DC  add      rsp, 0x20
0015B5E0  pop      rdi
0015B5E1  ret      
```
