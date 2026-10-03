# Homing pack: `10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-status-write-and-its-side-effects.json`.

Bodies: 6. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002C7620 (60 B, extent 002C7620-002C765C)

Entered from (direct sites whose caller this page cites): `002C6F70` + 0x126 (call; `002C6F70` is cited on this page)
Other direct sites: none

Host context: "-Entity/Unit-Display-Record/the-record-00329220-builds.md) at '+0x66 + s' ('00329500'–'00329539'), and two lookalike readers, '0031FC70' (actor → 32 bytes of 'count − 1', '0xFE' elsewhere; called by '002C6F70') and '00320CF0(slotIndex, s)' (the raw count for a present status 2 / 6, else '−1'; called by '00470780' / '00470B70'), read nothing else from the arrays. The default count 11 therefore shows as **10**; the count steps down every "

```
002C7620  mov      r8, rcx
002C7623  cmp      rdx, rcx
002C7626  jne      0x2c762c  ; -> 002C762C
002C7628  mov      r8, qword ptr [rcx + 0x18]
002C762C  mov      rcx, qword ptr [rdx + 0x20]
002C7630  test     rcx, rcx
002C7633  je       0x2c763d  ; -> 002C763D
002C7635  mov      rax, qword ptr [rdx + 0x18]
002C7639  mov      qword ptr [rcx + 0x18], rax
002C763D  mov      rax, qword ptr [rdx + 0x18]
002C7641  test     rax, rax
002C7644  je       0x2c764e  ; -> 002C764E
002C7646  mov      rcx, qword ptr [rdx + 0x20]
002C764A  mov      qword ptr [rax + 0x20], rcx
002C764E  xor      eax, eax
002C7650  mov      qword ptr [rdx + 0x18], rax
002C7654  mov      qword ptr [rdx + 0x20], rax
002C7658  mov      rax, r8
002C765B  ret      
```

## 002EA1E0 (79 B, extent 002EA1E0-002EA22F)

Entered from (direct sites whose caller this page cites): `002C6F70` + 0xD2 (call; `002C6F70` is cited on this page)
Other direct sites: none

Host context: "-Entity/Unit-Display-Record/the-record-00329220-builds.md) at '+0x66 + s' ('00329500'–'00329539'), and two lookalike readers, '0031FC70' (actor → 32 bytes of 'count − 1', '0xFE' elsewhere; called by '002C6F70') and '00320CF0(slotIndex, s)' (the raw count for a present status 2 / 6, else '−1'; called by '00470780' / '00470B70'), read nothing else from the arrays. The default count 11 therefore shows as **10**; the count steps down every "

```
002EA1E0  test     rcx, rcx
002EA1E3  je       0x2ea229  ; -> 002EA229
002EA1E5  mov      rax, qword ptr [rcx + 0xc0]
002EA1EC  test     rax, rax
002EA1EF  je       0x2ea229  ; -> 002EA229
002EA1F1  cmp      dword ptr [rax], -1
002EA1F4  je       0x2ea229  ; -> 002EA229
002EA1F6  movzx    ecx, word ptr [rax]
002EA1F9  cmp      cx, -1
002EA1FD  jne      0x2ea202  ; -> 002EA202
002EA1FF  xor      eax, eax
002EA201  ret      
002EA202  movsx    rax, cx
002EA206  imul     rcx, rax, 0x740
002EA20D  add      rcx, qword ptr [rip + 0x1fdcd14]  ; -> 022C6F28
002EA214  je       0x2ea1ff  ; -> 002EA1FF
002EA216  mov      eax, dword ptr [rcx + 0x284]
002EA21C  test     eax, eax
002EA21E  je       0x2ea1ff  ; -> 002EA1FF
002EA220  shr      eax, 3
002EA223  not      eax
002EA225  and      eax, 1
002EA228  ret      
002EA229  mov      eax, 1
002EA22E  ret      
```

## 00322950 (67 B, extent 00322950-00322993)

Entered from (direct sites whose caller this page cites): `002C7660` + 0x1AD (call; `002C7660` is cited on this page)
Other direct sites: none

Host context: "unction.  - **UI — MECHANICAL (SWE2-EC7-170, 74 edges).** '0028A090''s emit helpers   '00202C90', '002B3400', '00270550', '003588B0', '00203080' and '00271AB0' are   shared by UI bodies ('002915C0', '002C7660', '0028AAA0', '0027AD70',   +70 more) — the command-record constructor and the measure/transform   primitives' fan-in, not a UI relationship to the status write. Edge list   from 'edges.tsv' 2026-09-22.  ## Cross-subsystem neighbou"

```
00322950  sub      rsp, 0x28
00322954  test     byte ptr [rip + 0x1d669e5], 0x10  ; -> 02089340
0032295B  je       0x32298c  ; -> 0032298C
0032295D  call     0x3588b0  ; -> 003588B0 fn
00322962  test     rax, rax
00322965  je       0x32298c  ; -> 0032298C
00322967  mov      rcx, rax
0032296A  call     0x263e30  ; -> 00263E30 fn
0032296F  test     rax, rax
00322972  je       0x32298c  ; -> 0032298C
00322974  xor      edx, edx
00322976  mov      rcx, rax
00322979  call     0x321770  ; -> 00321770 fn
0032297E  xor      ecx, ecx
00322980  test     eax, eax
00322982  sete     cl
00322985  mov      eax, ecx
00322987  add      rsp, 0x28
0032298B  ret      
0032298C  xor      eax, eax
0032298E  add      rsp, 0x28
00322992  ret      
```

## 0035D570 (45 B, extent 0035D570-0035D59D)

Entered from (direct sites whose caller this page cites): `002C6F70` + 0xF1 (call; `002C6F70` is cited on this page)
Other direct sites: none

Host context: "-Entity/Unit-Display-Record/the-record-00329220-builds.md) at '+0x66 + s' ('00329500'–'00329539'), and two lookalike readers, '0031FC70' (actor → 32 bytes of 'count − 1', '0xFE' elsewhere; called by '002C6F70') and '00320CF0(slotIndex, s)' (the raw count for a present status 2 / 6, else '−1'; called by '00470780' / '00470B70'), read nothing else from the arrays. The default count 11 therefore shows as **10**; the count steps down every "

```
0035D570  mov      r8d, dword ptr [rip + 0x1f6ae79]  ; -> 022C83F0
0035D577  xor      edx, edx
0035D579  test     r8d, r8d
0035D57C  jle      0x35d594  ; -> 0035D594
0035D57E  lea      rax, [rip + 0x1f6ae73]  ; -> 022C83F8
0035D585  cmp      dword ptr [rax], ecx
0035D587  je       0x35d597  ; -> 0035D597
0035D589  inc      edx
0035D58B  add      rax, 4
0035D58F  cmp      edx, r8d
0035D592  jl       0x35d585  ; -> 0035D585
0035D594  xor      eax, eax
0035D596  ret      
0035D597  mov      eax, 1
0035D59C  ret      
```

## 003F19D0 (131 B, extent 003F19D0-003F1A53)

Entered from (direct sites whose caller this page cites): `003F0170` + 0xB1 (call; `003F0170` is cited on this page)
Other direct sites: none

Host context: "twice plus '00271720', formats into 'rsp+0x70'/'rsp+0x90' ('0x80' buffer) via '003F12D0'/'003F1220', sets '+0x88' bit '0', submits through '00289A10' with the caller's 'xmm0' in 'xmm3', and runs the '003F0170' teardown  Interior anchor '0028EEA9' (function '0028EE10').  '003F12D0' (9 B) is the record clear '0028EAB0' and '0028EE10' run before formatting: 'qword [rcx] = 0', 'dword [rcx+0x18] = 0' - two fields and out, the '0x20'-byte mes"

```
003F19D0  xor      eax, eax
003F19D2  mov      r8, rcx
003F19D5  mov      qword ptr [rdx + 0xb0], rax
003F19DC  mov      qword ptr [rdx + 0xb8], rax
003F19E3  mov      qword ptr [rdx + 0xc0], rax
003F19EA  test     rcx, rcx
003F19ED  jne      0x3f19f3  ; -> 003F19F3
003F19EF  mov      rax, rdx
003F19F2  ret      
003F19F3  movss    xmm1, dword ptr [rdx + 0xc8]
003F19FB  mov      rax, r8
003F19FE  nop      
003F1A00  movss    xmm0, dword ptr [rax + 0xc8]
003F1A08  comiss   xmm0, xmm1
003F1A0B  jbe      0x3f1a1e  ; -> 003F1A1E
003F1A0D  mov      rcx, qword ptr [rax + 0xb8]
003F1A14  test     rcx, rcx
003F1A17  je       0x3f1a2f  ; -> 003F1A2F
003F1A19  mov      rax, rcx
003F1A1C  jmp      0x3f1a00  ; -> 003F1A00
003F1A1E  mov      rcx, qword ptr [rax + 0xb0]
003F1A25  test     rcx, rcx
003F1A28  je       0x3f1a41  ; -> 003F1A41
003F1A2A  mov      rax, rcx
003F1A2D  jmp      0x3f1a00  ; -> 003F1A00
003F1A2F  mov      qword ptr [rax + 0xb8], rdx
003F1A36  mov      qword ptr [rdx + 0xc0], rax
003F1A3D  mov      rax, r8
003F1A40  ret      
003F1A41  mov      qword ptr [rax + 0xb0], rdx
003F1A48  mov      qword ptr [rdx + 0xc0], rax
003F1A4F  mov      rax, r8
003F1A52  ret      
```

## 003F2580 (65 B, extent 003F2580-003F25C1)

Entered from (direct sites whose caller this page cites): `002915C0` + 0x15A (call; `002915C0` is cited on this page)
Other direct sites: none

Host context: "ted status function.  - **UI — MECHANICAL (SWE2-EC7-170, 74 edges).** '0028A090''s emit helpers   '00202C90', '002B3400', '00270550', '003588B0', '00203080' and '00271AB0' are   shared by UI bodies ('002915C0', '002C7660', '0028AAA0', '0027AD70',   +70 more) — the command-record constructor and the measure/transform   primitives' fan-in, not a UI relationship to the status write. Edge list   from 'edges.tsv' 2026-09-22.  ## Cross-subsys"

```
003F2580  mov      r8, rcx
003F2583  test     rcx, rcx
003F2586  jne      0x3f258c  ; -> 003F258C
003F2588  mov      rax, rdx
003F258B  ret      
003F258C  mov      rax, qword ptr [rcx + 0x9b0]
003F2593  test     rax, rax
003F2596  je       0x3f25af  ; -> 003F25AF
003F2598  nop      dword ptr [rax + rax]
003F25A0  mov      rcx, rax
003F25A3  mov      rax, qword ptr [rax + 0x9b0]
003F25AA  test     rax, rax
003F25AD  jne      0x3f25a0  ; -> 003F25A0
003F25AF  mov      qword ptr [rcx + 0x9b0], rdx
003F25B6  mov      rax, r8
003F25B9  mov      qword ptr [rdx + 0x9b8], rcx
003F25C0  ret      
```
