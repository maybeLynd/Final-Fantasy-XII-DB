# F-interior pack: `17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md`

Generated 2026-10-02 12:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/add-motion-skeleton-and-high-model-tables.json`.

Functions: 13. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: bafa49c9f	SWE2-DATA: bucket member formats declared - 53 .bin + 5 .dat members, every entry assigned, each cla; inbox mentions: FABLE.md, SWE2-AUDIT-SPEC.md). OPUS read these before packing.

## 001F6E00 (77 B, extent 001F6E00-001F6E4D)

Page context: "B) is the record-list compare '0017EF60' calls: '([rdx+0x38] - [rdx+0x30]) >> 3' and the same on 'r8' gate empty lists, then the first elements' '[0] -> [0] -> +0x30'/'+0x48' fields are compared and '001F6E00' runs twice - the motion table's element-wise equality walk.  Interior anchor '001BD6E0' (function '001BD630').  '0036F0F0' (318 B) is the four-slot allocator '003466A0'/'0037B4D0' call on the '021B9AE0' table (4 records x 24 B, 'w"

```
001F6E00  xor      edx, edx
001F6E02  or       r8, 0xffffffffffffffff
001F6E06  inc      r8
001F6E09  cmp      byte ptr [rcx + r8], dl
001F6E0D  jne      0x1f6e06  ; -> 001F6E06
001F6E0F  cmp      byte ptr [rcx], 0x5f
001F6E12  je       0x1f6e4a  ; -> 001F6E4A
001F6E14  mov      r10, rcx
001F6E17  neg      r10
001F6E1A  nop      word ptr [rax + rax]
001F6E20  lea      rax, [r10 + rcx]
001F6E24  cmp      rax, r8
001F6E27  jae      0x1f6e4a  ; -> 001F6E4A
001F6E29  movzx    r9d, byte ptr [rcx]
001F6E2D  lea      eax, [r9 - 0x30]
001F6E31  cmp      al, 9
001F6E33  ja       0x1f6e42  ; -> 001F6E42
001F6E35  lea      edx, [rdx + rdx*4]
001F6E38  movsx    eax, r9b
001F6E3C  lea      edx, [rdx - 0x18]
001F6E3F  lea      edx, [rax + rdx*2]
001F6E42  inc      rcx
001F6E45  cmp      byte ptr [rcx], 0x5f
001F6E48  jne      0x1f6e20  ; -> 001F6E20
001F6E4A  mov      eax, edx
001F6E4C  ret      
```

## 00263F80 (35 B, extent 00263F80-00263FA3)

Page context: " Fran in all four - binds 'c:3' with 'bindp2' ('bindp2_d4' in dgl_g0102), and also 'bindh's 'C:22' directly (k = 2, no mapping state). The argument is a pool value '0x3000000 + k' that '002E9A60' -> '00263F80' resolves to entry k of the EBP's section 12, the manifest. Control ['c22_bind.py'](../../_index/candidates/hm1-parent-writer/c22_bind.py).*   - *LIP FLAP 2026-09-27 (OPUS):* the '+0x304' bit 6 that the k = 4 bind sets on the unit'"

```
00263F80  mov      r8, qword ptr [rcx + 0x100]
00263F87  and      edx, 0xffffff
00263F8D  test     r8, r8
00263F90  je       0x263fa0  ; -> 00263FA0
00263F92  cmp      edx, dword ptr [r8]
00263F95  jge      0x263f9d  ; -> 00263F9D
00263F97  mov      eax, dword ptr [r8 + rdx*4 + 4]
00263F9C  ret      
00263F9D  xor      eax, eax
00263F9F  ret      
00263FA0  mov      eax, edx
00263FA2  ret      
```

## 002E3A60 (134 B, extent 002E3A60-002E3AE6)

Page context: "(216 B) is a motion-table body - '003AB7F0'/'0051F6B0'. Interior anchor '0051F7C1' (a '003AB7F0' call).   ## SWE2-EC7-56 update (2026-09-19) - '002E3C20'  '002E3C20' (212 B) is a motion-table body - '002E3A60'/'002E42D0'. Interior anchor '002E3C8F' (a '002E3A60' call).  ## SWE2-EC7-62 update (2026-09-19) - '003721E0'  '003721E0' (150 B) is an add-motion body - '0020E620' single call. Interior anchor '00372201' (a '0020E620' call).   ## "

```
002E3A60  mov      qword ptr [rsp + 8], rbx
002E3A65  mov      qword ptr [rsp + 0x10], rsi
002E3A6A  push     rdi
002E3A6B  sub      rsp, 0x20
002E3A6F  xor      esi, esi
002E3A71  mov      rbx, rcx
002E3A74  mov      edi, esi
002E3A76  test     rcx, rcx
002E3A79  je       0x2e3ad4  ; -> 002E3AD4
002E3A7B  cmp      dword ptr [rcx], -1
002E3A7E  je       0x2e3ab6  ; -> 002E3AB6
002E3A80  test     edx, edx
002E3A82  je       0x2e3a9b  ; -> 002E3A9B
002E3A84  movzx    ecx, word ptr [rcx]
002E3A87  call     0x42f250  ; -> 0042F250 fn
002E3A8C  movzx    eax, byte ptr [rbx + 0x11]
002E3A90  or       byte ptr [rbx + 0x10], 0xb
002E3A94  and      al, 0x9f
002E3A96  or       al, 6
002E3A98  mov      byte ptr [rbx + 0x11], al
002E3A9B  mov      ecx, dword ptr [rbx]
002E3A9D  call     0x2ed470  ; -> 002ED470 fn
002E3AA2  mov      ecx, dword ptr [rbx + 4]
002E3AA5  call     0x2eb810  ; -> 002EB810 fn
002E3AAA  mov      qword ptr [rbx], 0xffffffffffffffff
002E3AB1  mov      edi, 1
002E3AB6  and      byte ptr [rbx + 0x10], 0xf
002E3ABA  xor      r8d, r8d
002E3ABD  xor      edx, edx
002E3ABF  mov      dword ptr [rbx], 0xffffffff
002E3AC5  mov      rcx, rbx
002E3AC8  mov      qword ptr [rbx + 8], rsi
002E3ACC  call     0x269d60  ; -> 00269D60 fn
002E3AD1  mov      dword ptr [rbx + 0x20], esi
002E3AD4  mov      rbx, qword ptr [rsp + 0x30]
002E3AD9  mov      eax, edi
002E3ADB  mov      rsi, qword ptr [rsp + 0x38]
002E3AE0  add      rsp, 0x20
002E3AE4  pop      rdi
002E3AE5  ret      
```

## 003466A0 (71 B, extent 003466A0-003466E7)

Page context: "0x48' fields are compared and '001F6E00' runs twice - the motion table's element-wise equality walk.  Interior anchor '001BD6E0' (function '001BD630').  '0036F0F0' (318 B) is the four-slot allocator '003466A0'/'0037B4D0' call on the '021B9AE0' table (4 records x 24 B, 'word[+0x16]' refcount): '0036F240' resolves 'edx'; a hit bumps '+0x16', clears 'byte[+3]', and returns '(sbyte[+2]<<4) | sbyte[+1]'; a miss scans the four slots for 'word"

```
003466A0  mov      qword ptr [rsp + 8], rbx
003466A5  push     rdi
003466A6  sub      rsp, 0x20
003466AA  mov      rcx, r9
003466AD  mov      rbx, rdx
003466B0  call     0x267e10  ; -> 00267E10 fn
003466B5  movzx    ecx, byte ptr [rbx + 0x20]
003466B9  mov      edi, eax
003466BB  test     cl, cl
003466BD  js       0x3466c7  ; -> 003466C7
003466BF  movsx    ecx, cl
003466C2  call     0x36ec10  ; -> 0036EC10 fn
003466C7  mov      edx, edi
003466C9  xor      ecx, ecx
003466CB  call     0x36f0f0  ; -> 0036F0F0 fn
003466D0  mov      ecx, 1
003466D5  mov      byte ptr [rbx + 0x20], al
003466D8  mov      rbx, qword ptr [rsp + 0x30]
003466DD  add      rsp, 0x20
003466E1  pop      rdi
003466E2  jmp      0x314d40  ; -> 00314D40 fn
```

## 0036EAB0 (192 B, extent 0036EAB0-0036EB70)

Page context: "s '(sbyte[+2]<<4) | sbyte[+1]' into 'esi'; 'eax>0' runs '0036C1D0(6)', '0036B160' -> 'dword[+0xC]', 'byte[0]=1', 'byte[+3]=0', '0036C140'/'0036A0B0', then '0032E620' registers the record against the '0036EAB0' vtable with 'r9d'=the first slot, 'edx'=the '+0x14' word - a 'eax<=0' leaves 'dword[+4]=0xFFFF'; a second '0032E400(0x27)' tail follows - the init half the four-slot issuer defers to.  Interior anchor '0036EDF7' (function '0036ED5"

```
0036EAB0  mov      qword ptr [rsp + 8], rbx
0036EAB5  mov      qword ptr [rsp + 0x10], rsi
0036EABA  mov      qword ptr [rsp + 0x18], rdi
0036EABF  push     r14
0036EAC1  sub      rsp, 0x30
0036EAC5  cmp      ecx, -1
0036EAC8  jne      0x36eacf  ; -> 0036EACF
0036EACA  xor      r14d, r14d
0036EACD  jmp      0x36eaf6  ; -> 0036EAF6
0036EACF  mov      eax, ecx
0036EAD1  and      eax, 0xf
0036EAD4  test     cl, 0xf0
0036EAD7  lea      rcx, [rax + rax*2]
0036EADB  lea      rax, [rip - 0x24eae2]  ; -> 00120000 (image base)
0036EAE2  lea      r14, [rax + 0x21b9ae0]  ; image base + 0x21b9ae0 = 022D9AE0
0036EAE9  jne      0x36eaf2  ; -> 0036EAF2
0036EAEB  lea      r14, [rax + 0x21b9ab0]  ; image base + 0x21b9ab0 = 022D9AB0
0036EAF2  lea      r14, [r14 + rcx*8]
0036EAF6  mov      ecx, dword ptr [r14 + 0xc]
0036EAFA  call     0x36a0b0  ; -> 0036A0B0 fn
0036EAFF  movsx    edi, byte ptr [r14 + 1]
0036EB04  mov      rcx, rax
0036EB07  movzx    ebx, byte ptr [r14 + 2]
0036EB0C  mov      rsi, rax
0036EB0F  call     0x36c100  ; -> 0036C100 fn
0036EB14  movsx    edx, word ptr [r14 + 0x14]
0036EB19  lea      ecx, [rdi + 2]
0036EB1C  test     bl, bl
0036EB1E  mov      dword ptr [rsp + 0x20], 1
0036EB26  mov      r9d, eax
0036EB29  mov      r8, rsi
0036EB2C  cmove    ecx, edi
0036EB2F  call     0x2df450  ; -> 002DF450 fn
0036EB34  mov      dword ptr [r14 + 4], eax
0036EB38  test     eax, eax
0036EB3A  je       0x36eb45  ; -> 0036EB45
0036EB3C  cmp      dword ptr [r14 + 8], 0
0036EB41  je       0x36eb5a  ; -> 0036EB5A
0036EB43  jmp      0x36eb56  ; -> 0036EB56
0036EB45  mov      ecx, dword ptr [r14 + 0xc]
0036EB49  call     0x369800  ; -> 00369800 fn
0036EB4E  mov      dword ptr [r14 + 0xc], 0
0036EB56  mov      byte ptr [r14], 3
0036EB5A  mov      rbx, qword ptr [rsp + 0x40]
0036EB5F  mov      rsi, qword ptr [rsp + 0x48]
0036EB64  mov      rdi, qword ptr [rsp + 0x50]
0036EB69  add      rsp, 0x30
0036EB6D  pop      r14
0036EB6F  ret      
```

## 0036F050 (145 B, extent 0036F050-0036F0E1)

Page context: "s the '002DF440'/'00369800'/'0036ED50' init tail - the skeleton-adjacent slot issuer the bind body uses.  Interior anchor '0036F118' (function '0036F0F0').  '0036ED50' (342 B) is the record composer '0036F050'/'0036F0F0' call: '0032E400(0x21, sword[rcx+0x14])' issues the first slot and packs '(sbyte[+2]<<4) | sbyte[+1]' into 'esi'; 'eax>0' runs '0036C1D0(6)', '0036B160' -> 'dword[+0xC]', 'byte[0]=1', 'byte[+3]=0', '0036C140'/'0036A0B0',"

```
0036F050  mov      qword ptr [rsp + 8], rbx
0036F055  push     rdi
0036F056  sub      rsp, 0x20
0036F05A  cmp      byte ptr [rip + 0x1f6aadf], 2  ; -> 022D9B40
0036F061  jne      0x36f096  ; -> 0036F096
0036F063  xor      ecx, ecx
0036F065  mov      byte ptr [rip + 0x1f6aad4], 1  ; -> 022D9B40
0036F06C  call     0x2df420  ; -> 002DF420 fn
0036F071  lea      rbx, [rip + 0x1f6aa38]  ; -> 022D9AB0
0036F078  lea      rdi, [rip + 0x1f6aa61]  ; -> 022D9AE0
0036F07F  nop      
0036F080  cmp      byte ptr [rbx], 3
0036F083  jne      0x36f08d  ; -> 0036F08D
0036F085  mov      rcx, rbx
0036F088  call     0x36ed50  ; -> 0036ED50 fn
0036F08D  add      rbx, 0x18
0036F091  cmp      rbx, rdi
0036F094  jl       0x36f080  ; -> 0036F080
0036F096  cmp      byte ptr [rip + 0x1f6aaa4], 2  ; -> 022D9B41
0036F09D  jne      0x36f0d6  ; -> 0036F0D6
0036F09F  mov      ecx, 1
0036F0A4  mov      byte ptr [rip + 0x1f6aa96], 1  ; -> 022D9B41
0036F0AB  call     0x2df420  ; -> 002DF420 fn
0036F0B0  lea      rbx, [rip + 0x1f6aa29]  ; -> 022D9AE0
0036F0B7  lea      rdi, [rip + 0x1f6aa82]  ; -> 022D9B40
0036F0BE  nop      
0036F0C0  cmp      byte ptr [rbx], 3
0036F0C3  jne      0x36f0cd  ; -> 0036F0CD
0036F0C5  mov      rcx, rbx
0036F0C8  call     0x36ed50  ; -> 0036ED50 fn
0036F0CD  add      rbx, 0x18
0036F0D1  cmp      rbx, rdi
0036F0D4  jl       0x36f0c0  ; -> 0036F0C0
0036F0D6  mov      rbx, qword ptr [rsp + 0x30]
0036F0DB  add      rsp, 0x20
0036F0DF  pop      rdi
0036F0E0  ret      
```

## 0036F240 (128 B, extent 0036F240-0036F2C0)

Page context: "walk.  Interior anchor '001BD6E0' (function '001BD630').  '0036F0F0' (318 B) is the four-slot allocator '003466A0'/'0037B4D0' call on the '021B9AE0' table (4 records x 24 B, 'word[+0x16]' refcount): '0036F240' resolves 'edx'; a hit bumps '+0x16', clears 'byte[+3]', and returns '(sbyte[+2]<<4) | sbyte[+1]'; a miss scans the four slots for 'word[+0x16]==0' then runs the '002DF440'/'00369800'/'0036ED50' init tail - the skeleton-adjacent sl"

```
0036F240  lea      r10, [rip - 0x24f247]  ; -> 00120000 (image base)
0036F247  mov      r9d, edx
0036F24A  test     ecx, ecx
0036F24C  je       0x36f282  ; -> 0036F282
0036F24E  xor      r8d, r8d
0036F251  movsxd   rax, r8d
0036F254  lea      rdx, [r10 + 0x21b9ae0]  ; image base + 0x21b9ae0 = 022D9AE0
0036F25B  lea      rcx, [rax + rax*2]
0036F25F  cmp      byte ptr [rdx + rcx*8], 0
0036F263  lea      rdx, [rdx + rcx*8]
0036F267  je       0x36f272  ; -> 0036F272
0036F269  movsx    eax, word ptr [rdx + 0x14]
0036F26D  cmp      eax, r9d
0036F270  je       0x36f27e  ; -> 0036F27E
0036F272  inc      r8d
0036F275  cmp      r8d, 4
0036F279  jl       0x36f251  ; -> 0036F251
0036F27B  xor      eax, eax
0036F27D  ret      
0036F27E  mov      rax, rdx
0036F281  ret      
0036F282  xor      edx, edx
0036F284  nop      dword ptr [rax]
0036F288  nop      dword ptr [rax + rax]
0036F290  movsxd   rax, edx
0036F293  lea      r8, [r10 + 0x21b9ab0]  ; image base + 0x21b9ab0 = 022D9AB0
0036F29A  lea      rcx, [rax + rax*2]
0036F29E  cmp      byte ptr [r8 + rcx*8], 0
0036F2A3  lea      r8, [r8 + rcx*8]
0036F2A7  je       0x36f2b3  ; -> 0036F2B3
0036F2A9  movsx    eax, word ptr [r8 + 0x14]
0036F2AE  cmp      eax, r9d
0036F2B1  je       0x36f2bc  ; -> 0036F2BC
0036F2B3  inc      edx
0036F2B5  cmp      edx, 2
0036F2B8  jge      0x36f27b  ; -> 0036F27B
0036F2BA  jmp      0x36f290  ; -> 0036F290
0036F2BC  mov      rax, r8
0036F2BF  ret      
```

## 004719B0 (54 B, extent 004719B0-004719E6)

Page context: "ord-indexed slots reach the 0x740-stride table at '022C6F28' only while its '+0x284' sentinel is nonzero, and nested structures recurse through the type-dispatched relocators '00421D20', '00512A90', '004719B0', '0051A380', '0051B850', '005161D0' and '0040EEA0' - clearing the field to a fresh '0020E620(0)' offset when the sub-record is absent. Called from '003713C0' on the motion-table load path.  Interior anchor '003E1D9A' (function '00"

```
004719B0  mov      qword ptr [rsp + 8], rbx
004719B5  push     rdi
004719B6  sub      rsp, 0x20
004719BA  mov      rdi, rcx
004719BD  mov      rbx, rdx
004719C0  mov      ecx, dword ptr [rdx]
004719C2  call     0x20e600  ; -> 0020E600 fn
004719C7  lea      ecx, [rbx + rax]
004719CA  call     0x20e620  ; -> 0020E620 fn
004719CF  mov      rcx, rbx
004719D2  mov      dword ptr [rbx], eax
004719D4  call     0x20e620  ; -> 0020E620 fn
004719D9  mov      rbx, qword ptr [rsp + 0x30]
004719DE  mov      dword ptr [rdi], eax
004719E0  add      rsp, 0x20
004719E4  pop      rdi
004719E5  ret      
```

## 00512A90 (56 B, extent 00512A90-00512AC8)

Page context: "0020E620', word-indexed slots reach the 0x740-stride table at '022C6F28' only while its '+0x284' sentinel is nonzero, and nested structures recurse through the type-dispatched relocators '00421D20', '00512A90', '004719B0', '0051A380', '0051B850', '005161D0' and '0040EEA0' - clearing the field to a fresh '0020E620(0)' offset when the sub-record is absent. Called from '003713C0' on the motion-table load path.  Interior anchor '003E1D9A' ("

```
00512A90  mov      qword ptr [rsp + 8], rbx
00512A95  push     rdi
00512A96  sub      rsp, 0x20
00512A9A  mov      rdi, rcx
00512A9D  mov      rbx, rdx
00512AA0  mov      ecx, dword ptr [rdx + 0x30]
00512AA3  call     0x20e600  ; -> 0020E600 fn
00512AA8  lea      ecx, [rbx + rax]
00512AAB  call     0x20e620  ; -> 0020E620 fn
00512AB0  mov      rcx, rbx
00512AB3  mov      dword ptr [rbx + 0x30], eax
00512AB6  call     0x20e620  ; -> 0020E620 fn
00512ABB  mov      rbx, qword ptr [rsp + 0x30]
00512AC0  mov      dword ptr [rdi], eax
00512AC2  add      rsp, 0x20
00512AC6  pop      rdi
00512AC7  ret      
```

## 005161D0 (43 B, extent 005161D0-005161FB)

Page context: "ride table at '022C6F28' only while its '+0x284' sentinel is nonzero, and nested structures recurse through the type-dispatched relocators '00421D20', '00512A90', '004719B0', '0051A380', '0051B850', '005161D0' and '0040EEA0' - clearing the field to a fresh '0020E620(0)' offset when the sub-record is absent. Called from '003713C0' on the motion-table load path.  Interior anchor '003E1D9A' (function '003E1C50').  '00421D20' (70 B) is the "

```
005161D0  mov      qword ptr [rsp + 8], rbx
005161D5  push     rdi
005161D6  sub      rsp, 0x20
005161DA  mov      rdi, rcx
005161DD  mov      ebx, edx
005161DF  mov      ecx, dword ptr [rcx]
005161E1  call     0x20e600  ; -> 0020E600 fn
005161E6  lea      ecx, [rbx + rax]
005161E9  call     0x20e620  ; -> 0020E620 fn
005161EE  mov      rbx, qword ptr [rsp + 0x30]
005161F3  mov      dword ptr [rdi], eax
005161F5  add      rsp, 0x20
005161F9  pop      rdi
005161FA  ret      
```

## 0051A380 (56 B, extent 0051A380-0051A3B8)

Page context: "slots reach the 0x740-stride table at '022C6F28' only while its '+0x284' sentinel is nonzero, and nested structures recurse through the type-dispatched relocators '00421D20', '00512A90', '004719B0', '0051A380', '0051B850', '005161D0' and '0040EEA0' - clearing the field to a fresh '0020E620(0)' offset when the sub-record is absent. Called from '003713C0' on the motion-table load path.  Interior anchor '003E1D9A' (function '003E1C50').  '"

```
0051A380  mov      qword ptr [rsp + 8], rbx
0051A385  push     rdi
0051A386  sub      rsp, 0x20
0051A38A  mov      rdi, rcx
0051A38D  mov      rbx, rdx
0051A390  mov      ecx, dword ptr [rdx + 0x10]
0051A393  call     0x20e600  ; -> 0020E600 fn
0051A398  lea      ecx, [rbx + rax]
0051A39B  call     0x20e620  ; -> 0020E620 fn
0051A3A0  mov      rcx, rbx
0051A3A3  mov      dword ptr [rbx + 0x10], eax
0051A3A6  call     0x20e620  ; -> 0020E620 fn
0051A3AB  mov      rbx, qword ptr [rsp + 0x30]
0051A3B0  mov      dword ptr [rdi], eax
0051A3B2  add      rsp, 0x20
0051A3B6  pop      rdi
0051A3B7  ret      
```

## 0051B850 (25 B, extent 0051B850-0051B869)

Page context: "the 0x740-stride table at '022C6F28' only while its '+0x284' sentinel is nonzero, and nested structures recurse through the type-dispatched relocators '00421D20', '00512A90', '004719B0', '0051A380', '0051B850', '005161D0' and '0040EEA0' - clearing the field to a fresh '0020E620(0)' offset when the sub-record is absent. Called from '003713C0' on the motion-table load path.  Interior anchor '003E1D9A' (function '003E1C50').  '00421D20' (7"

```
0051B850  push     rbx
0051B852  sub      rsp, 0x20
0051B856  mov      rbx, rcx
0051B859  mov      rcx, rdx
0051B85C  call     0x20e620  ; -> 0020E620 fn
0051B861  mov      dword ptr [rbx], eax
0051B863  add      rsp, 0x20
0051B867  pop      rbx
0051B868  ret      
```

## 00537260 (9 B, extent 00537260-00537269)

Page context: "F0' (a '002ED570' call).  ## SWE2-EC7-53 update (2026-09-19) - '0046E6F0'  '0046E6F0' (444 B) is a motion-table body the handlers page lists as a '00520010' caller - '00520010'/'00537170'/'00537180'/'00537260'/'002ED570'/'0020E600'/'003AB7F0', '[rsi+0x60]'-list walk under '[rsi+0x40]' count. Interior anchor '0046E719' (a '00520010' call).  ## SWE2-EC7-54 update (2026-09-19) - '0051FBB0'  '0051FBB0' (307 B) is a motion-table body - '003A"

```
00537260  mov      r8d, dword ptr [rcx + 0x20]
00537264  jmp      0x51ef90  ; -> 0051EF90 fn
```
