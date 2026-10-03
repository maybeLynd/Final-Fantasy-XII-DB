# F-interior pack: `06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md`

Generated 2026-10-02 12:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/how-the-engine-chooses-3d-or-flat-movement.json`.

Functions: 16. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 058c93e21	SWE2-AUDIT-SPEC: promotion sweep - 29 pages DOCUMENTED -> AUDITED; 06c849caf	SWE2-DATA: restate batches 0930E and GR - SD-3, SD-23, SD-166, SD-181..SD-184, SD-190, SD-191, SD-19; inbox mentions: FABLE.md, repos-46.md, repos-d2.md). OPUS read these before packing.

## 00262870 (57 B, extent 00262870-002628A9)

Page context: " party apart and put it back.       - '02B40530' (A): the initialiser '003B6ED0' and the 7-byte setter '003B7E10', whose callers are all engine code (§10:         '0024B6F0', '0024C6B0', '0024C870', '00262870', '003B8670').       - '02B40534' (B), from a full RIP-relative census with eight store sites in eight functions (the register's "nine"         was not reproduced): the initialiser (1), the setter '003B7E00' (argument; one caller, "

```
00262870  sub      rsp, 0x28
00262874  xor      ecx, ecx
00262876  call     0x2eda90  ; -> 002EDA90 fn
0026287B  or       ecx, 0xffffffff
0026287E  call     0x363b20  ; -> 00363B20 fn
00262883  xor      edx, edx
00262885  xor      ecx, ecx
00262887  call     0x3631a0  ; -> 003631A0 fn
0026288C  call     0x358420  ; -> 00358420 fn
00262891  mov      ecx, 1
00262896  call     0x3b7e10  ; -> 003B7E10 fn
0026289B  mov      ecx, 1
002628A0  add      rsp, 0x28
002628A4  jmp      0x3b7e00  ; -> 003B7E00 fn
```

## 0026ACE0 (32 B, extent 0026ACE0-0026AD00)

Page context: "' / '002E5278'), bit 3 is set at initialisation ('00265E06'), bit 4 is the ambient         fetch flag ('0026AD40' ← verbs 'setambient' / 'fetchambient' / 'resetambient'), bit 5 is         written by '0026ACE0' (← '003B7B00', '003B7F40'), bit 7 by '0026AF40' (← '002E28E0', read by         '00264EA0'). - [x] ~~What controller '+0x14F' bit 0 and '+0x138' are. They gate the flat path; their own meaning is       unread.~~ **'BV-2' ANSWERED 2"

```
0026ACE0  mov      rax, qword ptr [rcx + 0xc0]
0026ACE7  test     rax, rax
0026ACEA  je       0x26acff  ; -> 0026ACFF
0026ACEC  and      byte ptr [rax + 0x151], 0xdf
0026ACF3  and      dl, 1
0026ACF6  shl      dl, 5
0026ACF9  or       byte ptr [rax + 0x151], dl
0026ACFF  ret      
```

## 0026AD40 (32 B, extent 0026AD40-0026AD60)

Page context: "its of '+0x151' are not the 3-D pair: bit 2 is "moved this frame" ('002E5180',         '002E51BD' / '002E5278'), bit 3 is set at initialisation ('00265E06'), bit 4 is the ambient         fetch flag ('0026AD40' ← verbs 'setambient' / 'fetchambient' / 'resetambient'), bit 5 is         written by '0026ACE0' (← '003B7B00', '003B7F40'), bit 7 by '0026AF40' (← '002E28E0', read by         '00264EA0'). - [x] ~~What controller '+0x14F' bit 0 and"

```
0026AD40  mov      rax, qword ptr [rcx + 0xc0]
0026AD47  test     rax, rax
0026AD4A  je       0x26ad5f  ; -> 0026AD5F
0026AD4C  and      byte ptr [rax + 0x151], 0xef
0026AD53  and      dl, 1
0026AD56  shl      dl, 4
0026AD59  or       byte ptr [rax + 0x151], dl
0026AD5F  ret      
```

## 0026AF40 (36 B, extent 0026AF40-0026AF64)

Page context: "('00265E06'), bit 4 is the ambient         fetch flag ('0026AD40' ← verbs 'setambient' / 'fetchambient' / 'resetambient'), bit 5 is         written by '0026ACE0' (← '003B7B00', '003B7F40'), bit 7 by '0026AF40' (← '002E28E0', read by         '00264EA0'). - [x] ~~What controller '+0x14F' bit 0 and '+0x138' are. They gate the flat path; their own meaning is       unread.~~ **'BV-2' ANSWERED 2026-09-12 (FABLE): bit 0 is "this actor is attac"

```
0026AF40  mov      r8, qword ptr [rcx + 0xc0]
0026AF47  test     r8, r8
0026AF4A  je       0x26af63  ; -> 0026AF63
0026AF4C  and      byte ptr [r8 + 0x151], 0x7f
0026AF54  test     edx, edx
0026AF56  setne    al
0026AF59  shl      al, 7
0026AF5C  or       byte ptr [r8 + 0x151], al
0026AF63  ret      
```

## 002E9B40 (26 B, extent 002E9B40-002E9B5A)

Page context: "e' ('0034CB60'), '0483' / '02E0' 'setforcefight' / 'setforcerelax' through         their tick '00357F00', and '02E1' / '0484' 'clearforcerelax' / 'clearforcefight' ('00343290');         read back by '002E9B40' and, ORed with "controller '+0x12' ≥ 0x10", by '002EA2A0' /         '002EABF0'. The shipped scripts call 'setforcefight(-1)' 2,106 times and 'setforcerelax(0|1)'         2,174 times; 'setfightmode' never.       - **bit 2 — attach "

```
002E9B40  mov      rax, qword ptr [rcx + 0xc0]
002E9B47  test     rax, rax
002E9B4A  je       0x2e9b59  ; -> 002E9B59
002E9B4C  movzx    eax, byte ptr [rax + 0x14f]
002E9B53  shr      eax, 1
002E9B55  and      eax, 1
002E9B58  ret      
002E9B59  ret      
```

## 002EA2A0 (120 B, extent 002EA2A0-002EA318)

Page context: "cerelax' through         their tick '00357F00', and '02E1' / '0484' 'clearforcerelax' / 'clearforcefight' ('00343290');         read back by '002E9B40' and, ORed with "controller '+0x12' ≥ 0x10", by '002EA2A0' /         '002EABF0'. The shipped scripts call 'setforcefight(-1)' 2,106 times and 'setforcerelax(0|1)'         2,174 times; 'setfightmode' never.       - **bit 2 — attach offsets present.** '0026A140(actor, slot, ptr)' ('0026A163"

```
002EA2A0  test     rcx, rcx
002EA2A3  je       0x2ea317  ; -> 002EA317
002EA2A5  push     rbx
002EA2A6  sub      rsp, 0x20
002EA2AA  mov      rax, qword ptr [rcx + 0xc0]
002EA2B1  mov      rbx, rcx
002EA2B4  test     rax, rax
002EA2B7  je       0x2ea312  ; -> 002EA312
002EA2B9  cmp      dword ptr [rax], -1
002EA2BC  je       0x2ea312  ; -> 002EA312
002EA2BE  movzx    edx, byte ptr [rax + 0x14f]
002EA2C5  mov      ecx, 1
002EA2CA  shr      edx, 1
002EA2CC  and      edx, 1
002EA2CF  cmp      byte ptr [rax + 0x12], 0x10
002EA2D3  cmovge   edx, ecx
002EA2D6  cmp      dword ptr [rax], -1
002EA2D9  je       0x2ea306  ; -> 002EA306
002EA2DB  movzx    ecx, word ptr [rax]
002EA2DE  cmp      cx, -1
002EA2E2  je       0x2ea306  ; -> 002EA306
002EA2E4  movsx    rax, cx
002EA2E8  imul     rcx, rax, 0x740
002EA2EF  add      rcx, qword ptr [rip + 0x1fdcc32]  ; -> 022C6F28
002EA2F6  je       0x2ea306  ; -> 002EA306
002EA2F8  cmp      dword ptr [rcx + 0x284], 0
002EA2FF  je       0x2ea306  ; -> 002EA306
002EA301  call     0x426c90  ; -> 00426C90 fn
002EA306  movzx    edx, word ptr [rbx]
002EA309  movzx    ecx, byte ptr [rbx + 0x15]
002EA30D  call     0x263a30  ; -> 00263A30 fn
002EA312  add      rsp, 0x20
002EA316  pop      rbx
002EA317  ret      
```

## 002EABF0 (145 B, extent 002EABF0-002EAC81)

Page context: "    their tick '00357F00', and '02E1' / '0484' 'clearforcerelax' / 'clearforcefight' ('00343290');         read back by '002E9B40' and, ORed with "controller '+0x12' ≥ 0x10", by '002EA2A0' /         '002EABF0'. The shipped scripts call 'setforcefight(-1)' 2,106 times and 'setforcerelax(0|1)'         2,174 times; 'setfightmode' never.       - **bit 2 — attach offsets present.** '0026A140(actor, slot, ptr)' ('0026A163') is verb '01C8'    "

```
002EABF0  mov      r8, rcx
002EABF3  test     rcx, rcx
002EABF6  je       0x2eac80  ; -> 002EAC80
002EABFC  mov      rax, qword ptr [rcx + 0xc0]
002EAC03  test     rax, rax
002EAC06  je       0x2eac80  ; -> 002EAC80
002EAC08  cmp      dword ptr [rax], -1
002EAC0B  je       0x2eac80  ; -> 002EAC80
002EAC0D  movzx    edx, byte ptr [rax + 0x14f]
002EAC14  mov      ecx, 1
002EAC19  shr      edx, 1
002EAC1B  and      edx, 1
002EAC1E  cmp      byte ptr [rax + 0x12], 0x10
002EAC22  cmovge   edx, ecx
002EAC25  movzx    ecx, word ptr [rax]
002EAC28  cmp      cx, -1
002EAC2C  je       0x2eac72  ; -> 002EAC72
002EAC2E  movsx    rax, cx
002EAC32  imul     rcx, rax, 0x740
002EAC39  add      rcx, qword ptr [rip + 0x1fdc2e8]  ; -> 022C6F28
002EAC40  je       0x2eac72  ; -> 002EAC72
002EAC42  cmp      dword ptr [rcx + 0x284], 0
002EAC49  je       0x2eac72  ; -> 002EAC72
002EAC4B  test     edx, edx
002EAC4D  je       0x2eac6b  ; -> 002EAC6B
002EAC4F  and      byte ptr [rcx + 0x40b], 0xfd
002EAC56  or       byte ptr [rcx + 0x40b], 1
002EAC5D  movzx    edx, word ptr [r8]
002EAC61  movzx    ecx, byte ptr [r8 + 0x15]
002EAC66  jmp      0x263a30  ; -> 00263A30 fn
002EAC6B  and      byte ptr [rcx + 0x40b], 0xfc
002EAC72  movzx    edx, word ptr [r8]
002EAC76  movzx    ecx, byte ptr [r8 + 0x15]
002EAC7B  jmp      0x263a30  ; -> 00263A30 fn
002EAC80  ret      
```

## 003410C0 (120 B, extent 003410C0-00341138)

Page context: "e layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (97 edges).** '0025A5F0', '00262F50' are also called by bodies filed to script VM / native bridge: '003B7BB0', '003B7C60', '003410C0' - shared machinery across the layer boundary, no shared ownership. - **Spawn_Encounter_Lifecycle - CLIENT (4 edges).** '00265020', '00265200' are also called by bodies filed to spawn/encounter lifecycle: '00234AF0', '00234DA0', '0"

```
003410C0  mov      qword ptr [rsp + 8], rbx
003410C5  push     rdi
003410C6  sub      rsp, 0x50
003410CA  mov      rax, qword ptr [rip + 0x1c0375f]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003410D1  xor      rax, rsp
003410D4  mov      qword ptr [rsp + 0x40], rax
003410D9  mov      rcx, r9
003410DC  mov      rdi, rdx
003410DF  call     0x267e10  ; -> 00267E10 fn
003410E4  mov      edx, 4
003410E9  movsxd   rbx, eax
003410EC  lea      rcx, [rsp + 0x20]
003410F1  call     0x31b680  ; -> 0031B680 fn
003410F6  cmp      ebx, eax
003410F8  jge      0x341120  ; -> 00341120
003410FA  mov      rbx, qword ptr [rsp + rbx*8 + 0x20]
003410FF  test     rbx, rbx
00341102  je       0x341120  ; -> 00341120
00341104  mov      rdx, rbx
00341107  mov      rcx, rdi
0034110A  call     0x262f50  ; -> 00262F50 fn
0034110F  test     eax, eax
00341111  je       0x341120  ; -> 00341120
00341113  mov      edx, 1
00341118  mov      rcx, rbx
0034111B  call     0x35ae10  ; -> 0035AE10 fn
00341120  mov      rcx, qword ptr [rsp + 0x40]
00341125  xor      rcx, rsp
00341128  call     0x808c40  ; -> 00808C40 fn
0034112D  mov      rbx, qword ptr [rsp + 0x60]
00341132  add      rsp, 0x50
00341136  pop      rdi
00341137  ret      
```

## 00343290 (141 B, extent 00343290-0034331D)

Page context: " verbs         '01A7' 'setfightmode' ('0034CB60'), '0483' / '02E0' 'setforcefight' / 'setforcerelax' through         their tick '00357F00', and '02E1' / '0484' 'clearforcerelax' / 'clearforcefight' ('00343290');         read back by '002E9B40' and, ORed with "controller '+0x12' ≥ 0x10", by '002EA2A0' /         '002EABF0'. The shipped scripts call 'setforcefight(-1)' 2,106 times and 'setforcerelax(0|1)'         2,174 times; 'setfightmode"

```
00343290  mov      qword ptr [rsp + 8], rbx
00343295  mov      qword ptr [rsp + 0x10], rsi
0034329A  push     rdi
0034329B  sub      rsp, 0x20
0034329F  mov      rcx, rdx
003432A2  mov      rbx, rdx
003432A5  call     0x263f10  ; -> 00263F10 fn
003432AA  mov      rcx, rbx
003432AD  mov      rsi, rax
003432B0  call     0x263f40  ; -> 00263F40 fn
003432B5  mov      rcx, rax
003432B8  mov      rbx, rax
003432BB  call     0x2e9b40  ; -> 002E9B40 fn
003432C0  mov      rcx, rsi
003432C3  call     0x30bfb0  ; -> 0030BFB0 fn
003432C8  xor      edi, edi
003432CA  mov      rcx, rbx
003432CD  test     eax, eax
003432CF  setne    dil
003432D3  xor      r8d, r8d
003432D6  xor      edx, edx
003432D8  call     0x26a770  ; -> 0026A770 fn
003432DD  xorps    xmm1, xmm1
003432E0  mov      rcx, rbx
003432E3  call     0x2e5bc0  ; -> 002E5BC0 fn
003432E8  mov      rcx, rbx
003432EB  test     edi, edi
003432ED  je       0x3432f9  ; -> 003432F9
003432EF  mov      edx, 1
003432F4  mov      r8d, edx
003432F7  jmp      0x3432ff  ; -> 003432FF
003432F9  xor      edx, edx
003432FB  lea      r8d, [rdx + 1]
003432FF  call     0x2ecf10  ; -> 002ECF10 fn
00343304  mov      edx, edi
00343306  mov      rcx, rsi
00343309  mov      rbx, qword ptr [rsp + 0x30]
0034330E  mov      rsi, qword ptr [rsp + 0x38]
00343313  add      rsp, 0x20
00343317  pop      rdi
00343318  jmp      0x2e8540  ; -> 002E8540 fn
```

## 0034CC00 (82 B, extent 0034CC00-0034CC52)

Page context: "th a single writer, '0026AD60(actor, on)'         ('0026AD69'–'0026AD7E'): 'on' → bit 1 set and bit 2 clear, 'off' → bit 1 clear and bit 2 set.         Its callers are verb '007B' **'usemapid(n)'** ('0034CC00', then a re-read of the world position),         verb '040D' **'partyusemapid(n)'** ('0033FD60', per party member, then '002E5DF0') and the battle         console verb '301D' 'btlAtelSetCtrlCharPosToOrigin' ('0050F560'). The corpus"

```
0034CC00  push     rbx
0034CC02  sub      rsp, 0x30
0034CC06  mov      rcx, r9
0034CC09  mov      rbx, rdx
0034CC0C  call     0x267e10  ; -> 00267E10 fn
0034CC11  mov      edx, eax
0034CC13  mov      rcx, rbx
0034CC16  call     0x26ad60  ; -> 0026AD60 fn
0034CC1B  lea      r9, [rsp + 0x20]
0034CC20  mov      rcx, rbx
0034CC23  lea      r8, [rsp + 0x24]
0034CC28  lea      rdx, [rsp + 0x28]
0034CC2D  call     0x265020  ; -> 00265020 fn
0034CC32  movss    xmm3, dword ptr [rsp + 0x20]
0034CC38  mov      rcx, rbx
0034CC3B  movss    xmm2, dword ptr [rsp + 0x24]
0034CC41  movss    xmm1, dword ptr [rsp + 0x28]
0034CC47  call     0x2e5df0  ; -> 002E5DF0 fn
0034CC4C  add      rsp, 0x30
0034CC50  pop      rbx
0034CC51  ret      
```

## 00355D20 (103 B, extent 00355D20-00355D87)

Page context: "orcerelax(0|1)'         2,174 times; 'setfightmode' never.       - **bit 2 — attach offsets present.** '0026A140(actor, slot, ptr)' ('0026A163') is verb '01C8'         **'attachinfo(slot, &vec3)'** ('00355D20'): it stores a pointer to a script-owned float triple         in slot 0 / 1 / 2 = controller '+0x120' / '+0x128' / '+0x130' (position / rotation / scale         offset). When set, 'attach' uses '0042F3B0' to write the three offsets"

```
00355D20  mov      qword ptr [rsp + 8], rbx
00355D25  mov      qword ptr [rsp + 0x10], rbp
00355D2A  mov      qword ptr [rsp + 0x18], rsi
00355D2F  push     rdi
00355D30  sub      rsp, 0x20
00355D34  mov      rsi, r9
00355D37  mov      rbp, rdx
00355D3A  mov      rdi, rcx
00355D3D  call     0x2640c0  ; -> 002640C0 fn
00355D42  mov      rcx, rsi
00355D45  mov      rbx, rax
00355D48  call     0x267e10  ; -> 00267E10 fn
00355D4D  mov      r8d, eax
00355D50  mov      rdx, rdi
00355D53  mov      rcx, rbx
00355D56  call     0x2650b0  ; -> 002650B0 fn
00355D5B  mov      rcx, rsi
00355D5E  mov      rbx, rax
00355D61  call     0x267e10  ; -> 00267E10 fn
00355D66  mov      r8, rbx
00355D69  mov      edx, eax
00355D6B  mov      rcx, rbp
00355D6E  mov      rbx, qword ptr [rsp + 0x30]
00355D73  mov      rbp, qword ptr [rsp + 0x38]
00355D78  mov      rsi, qword ptr [rsp + 0x40]
00355D7D  add      rsp, 0x20
00355D81  pop      rdi
00355D82  jmp      0x26a140  ; -> 0026A140 fn
```

## 00357F00 (414 B, extent 00357F00-0035809E)

Page context: "t stance.** '002E8540(actor, on)' ('002E854C'–'002E855B'), reached from verbs         '01A7' 'setfightmode' ('0034CB60'), '0483' / '02E0' 'setforcefight' / 'setforcerelax' through         their tick '00357F00', and '02E1' / '0484' 'clearforcerelax' / 'clearforcefight' ('00343290');         read back by '002E9B40' and, ORed with "controller '+0x12' ≥ 0x10", by '002EA2A0' /         '002EABF0'. The shipped scripts call 'setforcefight(-1)' "

```
00357F00  mov      qword ptr [rsp + 8], rbx
00357F05  mov      qword ptr [rsp + 0x10], rsi
00357F0A  push     rdi
00357F0B  sub      rsp, 0x30
00357F0F  mov      rcx, rdx
00357F12  mov      rsi, r8
00357F15  mov      rdi, rdx
00357F18  call     0x263f10  ; -> 00263F10 fn
00357F1D  mov      rcx, rdi
00357F20  mov      rbx, rax
00357F23  call     0x263f40  ; -> 00263F40 fn
00357F28  mov      rcx, rbx
00357F2B  mov      rdi, rax
00357F2E  call     0x2ea6a0  ; -> 002EA6A0 fn
00357F33  test     eax, eax
00357F35  jne      0x357f47  ; -> 00357F47
00357F37  mov      rbx, qword ptr [rsp + 0x40]
00357F3C  mov      rsi, qword ptr [rsp + 0x48]
00357F41  add      rsp, 0x30
00357F45  pop      rdi
00357F46  ret      
00357F47  movsx    rax, word ptr [rsi]
00357F4B  cmp      eax, 5
00357F4E  ja       0x358085  ; -> 00358085
00357F54  lea      rdx, [rip - 0x237f5b]  ; -> 00120000 (image base)
00357F5B  mov      ecx, dword ptr [rdx + rax*4 + 0x2380a0]  ; image base + 0x2380a0 = 003580A0
00357F62  add      rcx, rdx
00357F65  jmp      rcx
00357F67  mov      ebx, 1
00357F6C  mov      word ptr [rsi], bx
00357F6F  mov      eax, 2
00357F74  mov      word ptr [rsi], ax
00357F77  mov      rcx, rdi
00357F7A  call     0x2e71c0  ; -> 002E71C0 fn
00357F7F  test     eax, eax
00357F81  jne      0x358085  ; -> 00358085
00357F87  mov      eax, 3
00357F8C  jmp      0x358082  ; -> 00358082
00357F91  mov      rcx, rdi
00357F94  call     0x2e9b40  ; -> 002E9B40 fn
00357F99  cmp      byte ptr [rsi + 2], 0
00357F9D  mov      dword ptr [rsi + 8], eax
00357FA0  je       0x357fd2  ; -> 00357FD2
00357FA2  xorps    xmm1, xmm1
00357FA5  mov      rcx, rdi
00357FA8  call     0x2e5bc0  ; -> 002E5BC0 fn
00357FAD  mov      ecx, 4
00357FB2  xor      edx, edx
00357FB4  mov      word ptr [rsi], cx
00357FB7  lea      r8d, [rcx - 3]
00357FBB  mov      rcx, rdi
00357FBE  call     0x2ecf10  ; -> 002ECF10 fn
00357FC3  xor      edx, edx
00357FC5  mov      rcx, rdi
00357FC8  call     0x2e8540  ; -> 002E8540 fn
00357FCD  jmp      0x358085  ; -> 00358085
00357FD2  mov      ecx, 4
00357FD7  mov      ebx, 1
00357FDC  mov      word ptr [rsi], cx
00357FDF  mov      r8d, ebx
00357FE2  mov      rcx, rdi
00357FE5  mov      edx, ebx
00357FE7  call     0x2ecf10  ; -> 002ECF10 fn
00357FEC  mov      edx, ebx
00357FEE  mov      rcx, rdi
00357FF1  call     0x2e8540  ; -> 002E8540 fn
00357FF6  jmp      0x358085  ; -> 00358085
00357FFB  cmp      byte ptr [rsi + 2], 0
00357FFF  mov      rcx, rdi
00358002  je       0x35803e  ; -> 0035803E
00358004  call     0x2e71c0  ; -> 002E71C0 fn
00358009  test     eax, eax
0035800B  je       0x358047  ; -> 00358047
0035800D  mov      rcx, rdi
00358010  movaps   xmmword ptr [rsp + 0x20], xmm6
00358015  call     0x2e4e00  ; -> 002E4E00 fn
0035801A  mov      ecx, 0x10
0035801F  movaps   xmm6, xmm0
00358022  call     0x3da190  ; -> 003DA190 fn
00358027  movd     xmm1, eax
0035802B  cvtdq2ps xmm1, xmm1
0035802E  comiss   xmm6, xmm1
00358031  movaps   xmm6, xmmword ptr [rsp + 0x20]
00358036  jb       0x358085  ; -> 00358085
00358038  mov      byte ptr [rsi + 3], 1
0035803C  jmp      0x358047  ; -> 00358047
0035803E  call     0x2e71c0  ; -> 002E71C0 fn
00358043  test     eax, eax
00358045  jne      0x358085  ; -> 00358085
00358047  mov      eax, 5
0035804C  mov      word ptr [rsi], ax
0035804F  cmp      dword ptr [rsi + 4], 0
00358053  je       0x35807d  ; -> 0035807D
00358055  cmp      byte ptr [rsi + 3], 0
00358059  xorps    xmm3, xmm3
0035805C  je       0x35806f  ; -> 0035806F
0035805E  mov      ecx, 4
00358063  call     0x3da190  ; -> 003DA190 fn
00358068  movd     xmm3, eax
0035806C  cvtdq2ps xmm3, xmm3
0035806F  mov      r8d, dword ptr [rsi + 0xc]
00358073  xor      edx, edx
00358075  mov      rcx, rdi
00358078  call     0x3ddb40  ; -> 003DDB40 fn
0035807D  mov      eax, 7
00358082  mov      word ptr [rsi], ax
00358085  mov      rbx, qword ptr [rsp + 0x40]
0035808A  xor      eax, eax
0035808C  cmp      word ptr [rsi], 7
00358090  mov      rsi, qword ptr [rsp + 0x48]
00358095  setne    al
00358098  add      rsp, 0x30
0035809C  pop      rdi
0035809D  ret      
```

## 0036D840 (79 B, extent 0036D840-0036D88F)

Page context: "4' **at its head** and then walks the actor list:  '''asm 003B7E4C  mov  dword ptr [rip -> 02B40534], ebx     ; ebx = 0, clear the gate 003B7E52  lea  ecx, [rbx + 1]      call 0025A5F0           call 0036D840           cmp  dword ptr [02EBCC60], ebx            ; actor count           mov  ecx, dword ptr [02EBCBE0]           call 003588B0                             ; ActorHandle_ResolveRegistryEntryByPackedId           call 00265020    "

```
0036D840  mov      qword ptr [rsp + 8], rbx
0036D845  push     rdi
0036D846  sub      rsp, 0x20
0036D84A  mov      ebx, dword ptr [rip + 0x2b532d4]  ; -> 02EC0B24
0036D850  mov      edi, dword ptr [rip + 0x2b532d2]  ; -> 02EC0B28
0036D856  test     ecx, ecx
0036D858  je       0x36d862  ; -> 0036D862
0036D85A  or       ebx, 0xc
0036D85D  or       edi, 0xc
0036D860  jmp      0x36d868  ; -> 0036D868
0036D862  and      ebx, 0xfffffff3
0036D865  and      edi, 0xfffffff3
0036D868  movzx    ecx, bx
0036D86B  call     0x2547c0  ; -> 002547C0 fn
0036D870  movzx    ecx, di
0036D873  call     0x254840  ; -> 00254840 fn
0036D878  mov      dword ptr [rip + 0x2b532a6], ebx  ; -> 02EC0B24
0036D87E  mov      rbx, qword ptr [rsp + 0x30]
0036D883  mov      dword ptr [rip + 0x2b5329f], edi  ; -> 02EC0B28
0036D889  add      rsp, 0x20
0036D88D  pop      rdi
0036D88E  ret      
```

## 003B70B0 (122 B, extent 003B70B0-003B712A)

Page context: "ared machinery across the layer boundary, no shared ownership. - **Presentation - CLIENT (72 edges).** '0024C6B0', '0024C870', '00263F40' are also called by bodies filed to presentation: '003A7360', '003B70B0', '003A4290' - shared machinery across the layer boundary, no shared ownership. - **Resource - SERVICE (4 edges).** '0042F6C0', '0042F880' reach bodies filed to resource: '002ED570', '004780B0' - shared machinery across the layer b"

```
003B70B0  mov      qword ptr [rsp + 0x18], rbx
003B70B5  push     rbp
003B70B6  sub      rsp, 0x20
003B70BA  xor      ebx, ebx
003B70BC  mov      ebp, ecx
003B70BE  cmp      dword ptr [rip + 0x2b05afc], ebx  ; -> 02EBCBC0
003B70C4  jle      0x3b711f  ; -> 003B711F
003B70C6  mov      qword ptr [rsp + 0x30], rsi
003B70CB  mov      qword ptr [rsp + 0x38], rdi
003B70D0  lea      rdi, [rip + 0x2b059e9]  ; -> 02EBCAC0
003B70D7  mov      rcx, qword ptr [rdi]
003B70DA  call     0x263f40  ; -> 00263F40 fn
003B70DF  mov      rcx, rax
003B70E2  mov      rsi, rax
003B70E5  call     0x2e97b0  ; -> 002E97B0 fn
003B70EA  test     rax, rax
003B70ED  je       0x3b7107  ; -> 003B7107
003B70EF  and      byte ptr [rax + 0x10], 0xfd
003B70F3  movzx    ecx, bpl
003B70F7  and      cl, 1
003B70FA  add      cl, cl
003B70FC  or       byte ptr [rax + 0x10], cl
003B70FF  mov      rcx, rsi
003B7102  call     0x2e8fd0  ; -> 002E8FD0 fn
003B7107  inc      ebx
003B7109  add      rdi, 8
003B710D  cmp      ebx, dword ptr [rip + 0x2b05aad]  ; -> 02EBCBC0
003B7113  jl       0x3b70d7  ; -> 003B70D7
003B7115  mov      rdi, qword ptr [rsp + 0x38]
003B711A  mov      rsi, qword ptr [rsp + 0x30]
003B711F  mov      rbx, qword ptr [rsp + 0x40]
003B7124  add      rsp, 0x20
003B7128  pop      rbp
003B7129  ret      
```

## 003B7B00 (171 B, extent 003B7B00-003B7BAB)

Page context: "), bit 3 is set at initialisation ('00265E06'), bit 4 is the ambient         fetch flag ('0026AD40' ← verbs 'setambient' / 'fetchambient' / 'resetambient'), bit 5 is         written by '0026ACE0' (← '003B7B00', '003B7F40'), bit 7 by '0026AF40' (← '002E28E0', read by         '00264EA0'). - [x] ~~What controller '+0x14F' bit 0 and '+0x138' are. They gate the flat path; their own meaning is       unread.~~ **'BV-2' ANSWERED 2026-09-12 (FAB"

```
003B7B00  test     rcx, rcx
003B7B03  je       0x3b7baa  ; -> 003B7BAA
003B7B09  push     rbx
003B7B0A  sub      rsp, 0x20
003B7B0E  mov      rbx, rcx
003B7B11  mov      qword ptr [rsp + 0x30], rdi
003B7B16  call     0x263f40  ; -> 00263F40 fn
003B7B1B  mov      rcx, rbx
003B7B1E  mov      rdi, rax
003B7B21  call     0x359b80  ; -> 00359B80 fn
003B7B26  mov      rbx, rax
003B7B29  test     rax, rax
003B7B2C  je       0x3b7ba0  ; -> 003B7BA0
003B7B2E  movss    xmm1, dword ptr [rax + 0x34]
003B7B33  mov      rcx, rdi
003B7B36  call     0x26a0d0  ; -> 0026A0D0 fn
003B7B3B  movss    xmm1, dword ptr [rbx + 0x24]
003B7B40  mov      rcx, rdi
003B7B43  call     0x26b620  ; -> 0026B620 fn
003B7B48  movss    xmm1, dword ptr [rbx + 0x34]
003B7B4D  mov      rcx, rdi
003B7B50  call     0x26a0d0  ; -> 0026A0D0 fn
003B7B55  movss    xmm3, dword ptr [rbx + 8]
003B7B5A  mov      rcx, rdi
003B7B5D  movss    xmm2, dword ptr [rbx + 4]
003B7B62  movss    xmm1, dword ptr [rbx]
003B7B66  call     0x26b0c0  ; -> 0026B0C0 fn
003B7B6B  movss    xmm3, dword ptr [rbx + 0x18]
003B7B70  mov      rcx, rdi
003B7B73  movss    xmm2, dword ptr [rbx + 0x14]
003B7B78  movss    xmm1, dword ptr [rbx + 0x10]
003B7B7D  call     0x26b720  ; -> 0026B720 fn
003B7B82  xor      edx, edx
003B7B84  mov      rcx, rdi
003B7B87  call     0x26ace0  ; -> 0026ACE0 fn
003B7B8C  movsx    edx, byte ptr [rbx + 0x64]
003B7B90  mov      rcx, rdi
003B7B93  call     0x2ec680  ; -> 002EC680 fn
003B7B98  mov      rcx, rdi
003B7B9B  call     0x2e4a40  ; -> 002E4A40 fn
003B7BA0  mov      rdi, qword ptr [rsp + 0x30]
003B7BA5  add      rsp, 0x20
003B7BA9  pop      rbx
003B7BAA  ret      
```

## 0050F560 (59 B, extent 0050F560-0050F59B)

Page context: "re-read of the world position),         verb '040D' **'partyusemapid(n)'** ('0033FD60', per party member, then '002E5DF0') and the battle         console verb '301D' 'btlAtelSetCtrlCharPosToOrigin' ('0050F560'). The corpus calls 'usemapid'         8,210 times (6,016 × '0', 2,194 × '1') and 'partyusemapid' 459 times (448 × '1'). Bit 2 is also         set by the teardown '002E3AF0' ('002E3BE4') and cleared by the presentation builder '002"

```
0050F560  push     rbx
0050F562  sub      rsp, 0x20
0050F566  call     0x327150  ; -> 00327150 fn
0050F56B  mov      rbx, rax
0050F56E  test     rax, rax
0050F571  je       0x50f595  ; -> 0050F595
0050F573  mov      rcx, qword ptr [rax + 0x10]
0050F577  xor      edx, edx
0050F579  call     0x26ad60  ; -> 0026AD60 fn
0050F57E  mov      rcx, qword ptr [rbx + 0x10]
0050F582  xorps    xmm3, xmm3
0050F585  xorps    xmm2, xmm2
0050F588  xorps    xmm1, xmm1
0050F58B  add      rsp, 0x20
0050F58F  pop      rbx
0050F590  jmp      0x26b0c0  ; -> 0026B0C0 fn
0050F595  add      rsp, 0x20
0050F599  pop      rbx
0050F59A  ret      
```
