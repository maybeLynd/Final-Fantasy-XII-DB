# F-interior pack: `03-World-Area-Field/Weather/weather-probability-and-transition-roll.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/weather-probability-and-transition-roll.json`.

Functions: 6. Each is cited on the page only at its entry and is still in the F frontier.

## 00234D40 (91 B, extent 00234D40-00234D9B)

Page context: "1' commits  Interior anchor '00400134' (function '004000E0').  '00400AC0' (559 B) is the per-slot processor '004000E0' calls for each '0x20'-stride row: '[rcx]' bit '0x40000' bypasses the '003588B0'/'00234D40' count query ('r9d' stays 1), the '*rdi' '+0x28'-chain is scanned for 'dword[+4] == [rbp+4]', a hit clears flag bit 2 (re-arming bit '0x4' when 'r9d == 2') or splices the node beside the 'esi'-indexed cursor with '00400650' unlink/"

```
00234D40  sub      rsp, 0x28
00234D44  call     0x31b760  ; -> 0031B760 fn
00234D49  test     rax, rax
00234D4C  jne      0x234d55  ; -> 00234D55
00234D4E  xor      eax, eax
00234D50  add      rsp, 0x28
00234D54  ret      
00234D55  test     byte ptr [rax], 0x10
00234D58  je       0x234d4e  ; -> 00234D4E
00234D5A  mov      rcx, qword ptr [rax + 0x698]
00234D61  test     rcx, rcx
00234D64  je       0x234d8d  ; -> 00234D8D
00234D66  mov      eax, dword ptr [rcx + 0x64]
00234D69  or       eax, dword ptr [rcx + 0x3c]
00234D6C  test     eax, 0x80000003
00234D71  je       0x234d7c  ; -> 00234D7C
00234D73  call     0x313f60  ; -> 00313F60 fn
00234D78  test     eax, eax
00234D7A  je       0x234d8d  ; -> 00234D8D
00234D7C  mov      eax, 1
00234D81  neg      eax
00234D83  sbb      eax, eax
00234D85  add      eax, 2
00234D88  add      rsp, 0x28
00234D8C  ret      
00234D8D  xor      eax, eax
00234D8F  neg      eax
00234D91  sbb      eax, eax
00234D93  add      eax, 2
00234D96  add      rsp, 0x28
00234D9A  ret      
```

## 00263AA0 (14 B, extent 00263AA0-00263AAE)

Page context: "510' counts and '0035D500' returns the '02B45A80'-family table, then per row 'dword[r13+i*4]' -> '0035D4F0', '0031FE10' gates, '00265020' triple-outputs, the '02064AB0' vector stores into 'rdi', and '00263AA0'/'00263AB0'/'00263AC0'/'00263C20'/'00265200'/'00320C60'/'0037C860'/'003FFFF0'/'004000E0'/'00400550'/'00808C40' run the emit - the index table's per-row collect, whose far-end callers are CombatFormula- and Rewards-side crossings (n"

```
00263AA0  test     byte ptr [rcx + 0xf], 0x40
00263AA4  je       0x263aab  ; -> 00263AAB
00263AA6  movsx    eax, byte ptr [rcx + 0x21]
00263AAA  ret      
00263AAB  xor      eax, eax
00263AAD  ret      
```

## 00263AB0 (14 B, extent 00263AB0-00263ABE)

Page context: " and '0035D500' returns the '02B45A80'-family table, then per row 'dword[r13+i*4]' -> '0035D4F0', '0031FE10' gates, '00265020' triple-outputs, the '02064AB0' vector stores into 'rdi', and '00263AA0'/'00263AB0'/'00263AC0'/'00263C20'/'00265200'/'00320C60'/'0037C860'/'003FFFF0'/'004000E0'/'00400550'/'00808C40' run the emit - the index table's per-row collect, whose far-end callers are CombatFormula- and Rewards-side crossings (named at sub"

```
00263AB0  test     byte ptr [rcx + 0xf], 0x40
00263AB4  je       0x263abb  ; -> 00263ABB
00263AB6  movsx    eax, byte ptr [rcx + 0x22]
00263ABA  ret      
00263ABB  xor      eax, eax
00263ABD  ret      
```

## 00263AC0 (118 B, extent 00263AC0-00263B36)

Page context: "500' returns the '02B45A80'-family table, then per row 'dword[r13+i*4]' -> '0035D4F0', '0031FE10' gates, '00265020' triple-outputs, the '02064AB0' vector stores into 'rdi', and '00263AA0'/'00263AB0'/'00263AC0'/'00263C20'/'00265200'/'00320C60'/'0037C860'/'003FFFF0'/'004000E0'/'00400550'/'00808C40' run the emit - the index table's per-row collect, whose far-end callers are CombatFormula- and Rewards-side crossings (named at subsystem leve"

```
00263AC0  push     rdi
00263AC2  sub      rsp, 0x20
00263AC6  mov      rdi, rcx
00263AC9  test     rcx, rcx
00263ACC  je       0x263b2e  ; -> 00263B2E
00263ACE  mov      qword ptr [rsp + 0x30], rbx
00263AD3  movzx    ebx, byte ptr [rcx + 0xf]
00263AD7  cmp      ebx, 2
00263ADA  jne      0x263b21  ; -> 00263B21
00263ADC  lea      rax, [rip + 0x1e3532d]  ; -> 02098E10
00263AE3  mov      qword ptr [rsp + 0x38], rsi
00263AE8  mov      rsi, qword ptr [rip + 0x1e36281]  ; -> 02099D70
00263AEF  mov      qword ptr [rip + 0x1e3627a], rax  ; -> 02099D70
00263AF6  call     0x3590d0  ; -> 003590D0 fn
00263AFB  test     eax, eax
00263AFD  je       0x263b08  ; -> 00263B08
00263AFF  mov      ecx, eax
00263B01  call     0x3588b0  ; -> 003588B0 fn
00263B06  jmp      0x263b0a  ; -> 00263B0A
00263B08  xor      eax, eax
00263B0A  cmp      rdi, rax
00263B0D  mov      qword ptr [rip + 0x1e3625c], rsi  ; -> 02099D70
00263B14  mov      rsi, qword ptr [rsp + 0x38]
00263B19  mov      ecx, 1
00263B1E  cmove    ebx, ecx
00263B21  mov      eax, ebx
00263B23  mov      rbx, qword ptr [rsp + 0x30]
00263B28  add      rsp, 0x20
00263B2C  pop      rdi
00263B2D  ret      
00263B2E  xor      eax, eax
00263B30  add      rsp, 0x20
00263B34  pop      rdi
00263B35  ret      
```

## 00400550 (132 B, extent 00400550-004005D4)

Page context: "035D4F0', '0031FE10' gates, '00265020' triple-outputs, the '02064AB0' vector stores into 'rdi', and '00263AA0'/'00263AB0'/'00263AC0'/'00263C20'/'00265200'/'00320C60'/'0037C860'/'003FFFF0'/'004000E0'/'00400550'/'00808C40' run the emit - the index table's per-row collect, whose far-end callers are CombatFormula- and Rewards-side crossings (named at subsystem level, not by address).  Interior anchor '003C515F' (function '003C5130').  '0040"

```
00400550  test     edx, edx
00400552  jne      0x4005d3  ; -> 004005D3
00400554  push     rbx
00400555  sub      rsp, 0x30
00400559  mov      edx, 5
0040055E  mov      qword ptr [rsp + 0x40], rdi
00400563  xor      edi, edi
00400565  xor      r9d, r9d
00400568  mov      dword ptr [rsp + 0x28], edi
0040056C  mov      r8d, edx
0040056F  mov      dword ptr [rsp + 0x20], edi
00400573  mov      rbx, rcx
00400576  call     0x400cf0  ; -> 00400CF0 fn
0040057B  xor      r9d, r9d
0040057E  mov      dword ptr [rsp + 0x28], edi
00400582  lea      edx, [rdi + 8]
00400585  mov      dword ptr [rsp + 0x20], eax
00400589  lea      r8d, [rdi + 5]
0040058D  mov      rcx, rbx
00400590  call     0x400cf0  ; -> 00400CF0 fn
00400595  xor      r9d, r9d
00400598  mov      dword ptr [rsp + 0x28], edi
0040059C  lea      edx, [rdi + 3]
0040059F  mov      dword ptr [rsp + 0x20], eax
004005A3  lea      r8d, [rdi + 6]
004005A7  mov      rcx, rbx
004005AA  call     0x400cf0  ; -> 00400CF0 fn
004005AF  xor      r9d, r9d
004005B2  mov      dword ptr [rsp + 0x28], edi
004005B6  lea      edx, [rdi + 4]
004005B9  mov      dword ptr [rsp + 0x20], eax
004005BD  lea      r8d, [rdi + 7]
004005C1  mov      rcx, rbx
004005C4  call     0x400cf0  ; -> 00400CF0 fn
004005C9  mov      rdi, qword ptr [rsp + 0x40]
004005CE  add      rsp, 0x30
004005D2  pop      rbx
004005D3  ret      
```

## 00400650 (69 B, extent 00400650-00400695)

Page context: "'r9d' stays 1), the '*rdi' '+0x28'-chain is scanned for 'dword[+4] == [rbp+4]', a hit clears flag bit 2 (re-arming bit '0x4' when 'r9d == 2') or splices the node beside the 'esi'-indexed cursor with '00400650' unlink/relink; a miss runs the '+0x1411' modulo-0x40 round-robin to pick a free '+0x10'-block slot ('+0x20' bit 0 clear), '00275550' reclaims it, the node links at '[rdi+8]' tail with '+0x1412' bump and '+0x22 = 0x80', '[rbp]'/'[r"

```
00400650  mov      r8, rcx
00400653  cmp      rcx, rdx
00400656  jne      0x40065c  ; -> 0040065C
00400658  mov      r8, qword ptr [rdx + 0x28]
0040065C  mov      rcx, qword ptr [rdx + 0x30]
00400660  test     rcx, rcx
00400663  je       0x40066d  ; -> 0040066D
00400665  mov      rax, qword ptr [rdx + 0x28]
00400669  mov      qword ptr [rcx + 0x28], rax
0040066D  mov      rax, qword ptr [rdx + 0x28]
00400671  test     rax, rax
00400674  je       0x40067e  ; -> 0040067E
00400676  mov      rcx, qword ptr [rdx + 0x30]
0040067A  mov      qword ptr [rax + 0x30], rcx
0040067E  mov      eax, 0xfffe
00400683  and      word ptr [rdx + 0x20], ax
00400687  xor      eax, eax
00400689  mov      qword ptr [rdx + 0x30], rax
0040068D  mov      qword ptr [rdx + 0x28], rax
00400691  mov      rax, r8
00400694  ret      
```
