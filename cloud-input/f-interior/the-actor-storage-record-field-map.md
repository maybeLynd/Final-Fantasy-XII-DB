# F-interior pack: `04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md`

Generated 2026-10-02 18:33 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-actor-storage-record-field-map.json`.

Functions: 6. Each is cited on the page only at its entry and is still in the F frontier.

## 002E6420 (179 B, extent 002E6420-002E64D3)

Page context: "ord returned (0 on a null resolve). Interior anchor '0031E7E1' (the '002367A0' call).  ## SWE2-EC7-98 update (2026-09-20) - '00428FE0' measured  '00428FE0' (60 B) is the flag-word update '002E3AF0', '002E6420' and '002E92F0' tail into: '[+0x304]' bit 4 is cleared then re-set iff 'edx != 0' (the 'neg'/'sbb'/'and 0x10' idiom), and '[+0x290]' takes '0x4000000' when 'edx != 0' and 'byte[+0x294] & 8' is clear, '0x8000000' otherwise - the pai"

```
002E6420  mov      qword ptr [rsp + 8], rbx
002E6425  mov      qword ptr [rsp + 0x10], rbp
002E642A  mov      qword ptr [rsp + 0x18], rsi
002E642F  push     rdi
002E6430  sub      rsp, 0x20
002E6434  xor      ebp, ebp
002E6436  mov      ecx, ebp
002E6438  call     0x263ff0  ; -> 00263FF0 fn
002E643D  mov      rdi, rax
002E6440  test     byte ptr [rax + 0x10], 1
002E6444  je       0x2e64b3  ; -> 002E64B3
002E6446  movzx    ebx, word ptr [rax + 0x1de]
002E644D  movzx    esi, word ptr [rax + 0x1d6]
002E6454  add      esi, ebx
002E6456  cmp      ebx, esi
002E6458  jae      0x2e64b3  ; -> 002E64B3
002E645A  nop      word ptr [rax + rax]
002E6460  mov      edx, ebx
002E6462  mov      rcx, rdi
002E6465  call     0x358940  ; -> 00358940 fn
002E646A  test     rax, rax
002E646D  je       0x2e64ad  ; -> 002E64AD
002E646F  mov      rax, qword ptr [rax + 0xc0]
002E6476  test     rax, rax
002E6479  je       0x2e64ad  ; -> 002E64AD
002E647B  cmp      dword ptr [rax], -1
002E647E  je       0x2e64ad  ; -> 002E64AD
002E6480  movzx    ecx, word ptr [rax]
002E6483  cmp      cx, -1
002E6487  je       0x2e64ad  ; -> 002E64AD
002E6489  movsx    rax, cx
002E648D  imul     rcx, rax, 0x740
002E6494  add      rcx, qword ptr [rip + 0x1fe0a8d]  ; -> 022C6F28
002E649B  je       0x2e64ad  ; -> 002E64AD
002E649D  cmp      dword ptr [rcx + 0x284], 0
002E64A4  je       0x2e64ad  ; -> 002E64AD
002E64A6  xor      edx, edx
002E64A8  call     0x428fe0  ; -> 00428FE0 fn
002E64AD  inc      ebx
002E64AF  cmp      ebx, esi
002E64B1  jl       0x2e6460  ; -> 002E6460
002E64B3  inc      ebp
002E64B5  cmp      ebp, 3
002E64B8  jl       0x2e6436  ; -> 002E6436
002E64BE  mov      rbx, qword ptr [rsp + 0x30]
002E64C3  mov      rbp, qword ptr [rsp + 0x38]
002E64C8  mov      rsi, qword ptr [rsp + 0x40]
002E64CD  add      rsp, 0x20
002E64D1  pop      rdi
002E64D2  ret      
```

## 002EA970 (86 B, extent 002EA970-002EA9C6)

Page context: "0' measured  '0026B500' (32 B) is the flag-bit writer '003B6CC0', '003B6D60', '003B7C60' and '003B7D30' call on a record's '+0x0D' byte: it clears bit 1 and ORs '(edx != 0) << 1' back in, then tails '002EA970' - the predicate-to-bit publish the storage arms share. Interior anchor '0026B509' (the bit clear).  ## SWE2-EC7-107 update (2026-09-20) - '00237F40' measured  '00237F40' (118 B) is the gated enumeration '0025C830' and '0026C3E0' r"

```
002EA970  mov      r8d, edx
002EA973  test     rcx, rcx
002EA976  je       0x2ea9c5  ; -> 002EA9C5
002EA978  mov      rax, qword ptr [rcx + 0xc0]
002EA97F  test     rax, rax
002EA982  je       0x2ea9c5  ; -> 002EA9C5
002EA984  cmp      dword ptr [rax], -1
002EA987  je       0x2ea9c5  ; -> 002EA9C5
002EA989  movzx    ecx, word ptr [rax]
002EA98C  cmp      cx, -1
002EA990  je       0x2ea9c5  ; -> 002EA9C5
002EA992  movsx    rax, cx
002EA996  imul     rcx, rax, 0x740
002EA99D  add      rcx, qword ptr [rip + 0x1fdc584]  ; -> 022C6F28
002EA9A4  je       0x2ea9c5  ; -> 002EA9C5
002EA9A6  cmp      dword ptr [rcx + 0x284], 0
002EA9AD  je       0x2ea9c5  ; -> 002EA9C5
002EA9AF  add      rcx, 0x550
002EA9B6  je       0x2ea9c5  ; -> 002EA9C5
002EA9B8  xor      edx, edx
002EA9BA  test     r8d, r8d
002EA9BD  sete     dl
002EA9C0  jmp      0x3af320  ; -> 003AF320 fn
002EA9C5  ret      
```

## 00340970 (118 B, extent 00340970-003409E6)

Page context: "4, 102 edges, one fan-in).** The math helpers this page's '003A1C90' cites ('00202E10' and family, the '0025Axxx'/'0025Bxxx'/'0025Dxxx' leaves) are called across the script VM / native bridge layer ('00340970', '00268850', '0025E4C0'…) — one shared helper set with a wide caller fan, not field-map plumbing.  *Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*  **Save_Load_Settings — S"

```
00340970  mov      qword ptr [rsp + 8], rbx
00340975  push     rdi
00340976  sub      rsp, 0x20
0034097A  mov      rbx, r9
0034097D  call     0x2640c0  ; -> 002640C0 fn
00340982  mov      rcx, rbx
00340985  mov      rdi, rax
00340988  call     0x267e10  ; -> 00267E10 fn
0034098D  mov      r8d, eax
00340990  xor      edx, edx
00340992  mov      rcx, rdi
00340995  mov      ebx, eax
00340997  call     0x25ae00  ; -> 0025AE00 fn
0034099C  mov      r8d, ebx
0034099F  mov      edx, 1
003409A4  mov      rcx, rdi
003409A7  call     0x25ae00  ; -> 0025AE00 fn
003409AC  mov      r8d, ebx
003409AF  mov      edx, 4
003409B4  mov      rcx, rdi
003409B7  call     0x25ae00  ; -> 0025AE00 fn
003409BC  mov      r8d, ebx
003409BF  mov      edx, 2
003409C4  mov      rcx, rdi
003409C7  call     0x25ae00  ; -> 0025AE00 fn
003409CC  mov      r8d, ebx
003409CF  mov      edx, 3
003409D4  mov      rcx, rdi
003409D7  mov      rbx, qword ptr [rsp + 0x30]
003409DC  add      rsp, 0x20
003409E0  pop      rdi
003409E1  jmp      0x25ae00  ; -> 0025AE00 fn
```

## 00358A00 (21 B, extent 00358A00-00358A15)

Page context: "pt-binds-to-an-actor-and-how-requests-are-scheduled.md); store row unnamed | 0 / 2 |  | 'ActorResource_AllocateAndSubmitEntry' '003DBCF0' ('003DBCFA' +1); 'ActorScriptResource_GetBytecodeOffsetById' '00358A00' ('00358A00') | | '+0x050' | 8 | void* | 'payloadSectionA' — **the script's jump table** '{u32 count; u32 offsetWithinScript[]}' ('image + resolve(entry.+0x14)', planted at '002667B9'; 'FUN_003589E0' indexes it with the 'JMP' famil"

```
00358A00  mov      r8, qword ptr [rcx + 0x48]
00358A04  cmp      edx, dword ptr [r8]
00358A07  jb       0x358a0c  ; -> 00358A0C
00358A09  xor      eax, eax
00358A0B  ret      
00358A0C  movsxd   rax, edx
00358A0F  mov      eax, dword ptr [r8 + rax*8 + 8]
00358A14  ret      
```

## 003B7D30 (70 B, extent 003B7D30-003B7D76)

Page context: "ms apply. Interior anchor '00429006' (the '0x4000000' or).  ## SWE2-EC7-104 update (2026-09-20) - '0026B500' measured  '0026B500' (32 B) is the flag-bit writer '003B6CC0', '003B6D60', '003B7C60' and '003B7D30' call on a record's '+0x0D' byte: it clears bit 1 and ORs '(edx != 0) << 1' back in, then tails '002EA970' - the predicate-to-bit publish the storage arms share. Interior anchor '0026B509' (the bit clear).  ## SWE2-EC7-107 update ("

```
003B7D30  push     rbx
003B7D32  sub      rsp, 0x20
003B7D36  xor      ebx, ebx
003B7D38  cmp      dword ptr [rip + 0x2b04d62], ebx  ; -> 02EBCAA0
003B7D3E  jle      0x3b7d70  ; -> 003B7D70
003B7D40  mov      qword ptr [rsp + 0x30], rdi
003B7D45  lea      rdi, [rip + 0x2b04d34]  ; -> 02EBCA80
003B7D4C  nop      dword ptr [rax]
003B7D50  mov      rcx, qword ptr [rdi]
003B7D53  mov      edx, 1
003B7D58  call     0x26b500  ; -> 0026B500 fn
003B7D5D  inc      ebx
003B7D5F  lea      rdi, [rdi + 8]
003B7D63  cmp      ebx, dword ptr [rip + 0x2b04d37]  ; -> 02EBCAA0
003B7D69  jl       0x3b7d50  ; -> 003B7D50
003B7D6B  mov      rdi, qword ptr [rsp + 0x30]
003B7D70  add      rsp, 0x20
003B7D74  pop      rbx
003B7D75  ret      
```

## 00420A10 (41 B, extent 00420A10-00420A39)

Page context: "adeStartDistance' plus the six 'CharacterRenderConfig_*' getters and setters — and '0025DF00' calls '003E68B0'/'003E6EF0'/ '003E6A70'; '002E5180' reaches 'CharacterRenderQuerySupport' '002E8000' and '00420A10'. Caller-side, 'ActorOverlapDrivenTransparencyFadeUpdate' '00256F60' calls '002EA6A0', 'BattleUnit_BroadcastPartyCombatTargetRelation' and 'PartyCombat_UpdateStanceState' call '0031B810', '00358940' fans in to four Presentation bod"

```
00420A10  cmp      dword ptr [rcx + 0xc4], -1
00420A17  je       0x420a2e  ; -> 00420A2E
00420A19  test     dword ptr [rcx + 0x304], 0x4000
00420A23  jne      0x420a2e  ; -> 00420A2E
00420A25  movss    dword ptr [rcx + 0x23c], xmm1
00420A2D  ret      
00420A2E  mov      dword ptr [rcx + 0x23c], 0
00420A38  ret      
```
