# F-interior pack: `17-Presentation-Rendering/Character-Render-Records/how-a-character-fades-the-ten-channels.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/how-a-character-fades-the-ten-channels.json`.

Functions: 19. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ; inbox mentions: SWE2-EC7.md). OPUS read these before packing.

## 002915C0 (389 B, extent 002915C0-00291745)

Page context: "r the audit still reported for this page.*  **UI - MECHANICAL (24 edges).** Sixteen UI bodies call '00202C90', the 7-byte copy of one 16-byte vector that the '+0x2E0' hand-off tails into (among them '002915C0', '002C7660', '003F26F0', '003F9720' and '005528C0', and 11 more); seven call '00203170', the 44-byte store of a 4x4 identity matrix ('00247AE0', '002D2600', '002D28E0', '00368010', '003C5500', '003F26F0' and '003F2A70'); and '0024"

```
002915C0  push     rbp
002915C2  push     rsi
002915C3  push     rdi
002915C4  push     r14
002915C6  sub      rsp, 0x48
002915CA  mov      rax, qword ptr [rip + 0x1cb325f]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002915D1  xor      rax, rsp
002915D4  mov      qword ptr [rsp + 0x30], rax
002915D9  mov      rax, qword ptr [rcx + 0x10f20]
002915E0  mov      edi, r9d
002915E3  mov      rbp, r8
002915E6  mov      r14d, edx
002915E9  mov      rsi, rcx
002915EC  test     rax, rax
002915EF  je       0x291609  ; -> 00291609
002915F1  cmp      dword ptr [rax + 0x980], edi
002915F7  je       0x29172e  ; -> 0029172E
002915FD  mov      rax, qword ptr [rax + 0x9b0]
00291604  test     rax, rax
00291607  jne      0x2915f1  ; -> 002915F1
00291609  mov      rdx, qword ptr [rip + 0x1e0a870]  ; -> 0209BE80
00291610  mov      r8d, 0x9d0
00291616  xor      ecx, ecx
00291618  mov      qword ptr [rsp + 0x40], rbx
0029161D  mov      rdx, qword ptr [rdx + 0x10fc0]
00291624  call     0x273a30  ; -> 00273A30 fn
00291629  mov      rbx, rax
0029162C  test     rax, rax
0029162F  je       0x291729  ; -> 00291729
00291635  mov      edx, 0x9d0
0029163A  mov      rcx, rax
0029163D  call     0x275550  ; -> 00275550 fn
00291642  mov      edx, 0x9d0
00291647  mov      rcx, rbx
0029164A  call     0x275550  ; -> 00275550 fn
0029164F  lea      rcx, [rbx + 0x960]
00291656  test     rbp, rbp
00291659  je       0x291665  ; -> 00291665
0029165B  mov      rdx, rbp
0029165E  call     0x202c90  ; -> 00202C90 fn
00291663  jmp      0x291679  ; -> 00291679
00291665  or       byte ptr [rbx + 0x991], 2
0029166C  mov      edx, edi
0029166E  mov      dword ptr [rbx + 0x980], edi
00291674  call     0x2713e0  ; -> 002713E0 fn
00291679  cmp      dword ptr [rsp + 0x90], 0
00291681  mov      byte ptr [rbx + 0x990], r14b
00291688  je       0x291691  ; -> 00291691
0029168A  or       byte ptr [rbx + 0x991], 4
00291691  movss    xmm0, dword ptr [rsp + 0x98]
0029169A  movss    dword ptr [rbx + 0x9a8], xmm0
002916A2  cmp      qword ptr [rsi + 0x10f50], 0
002916AA  jne      0x2916bf  ; -> 002916BF
002916AC  mov      rcx, qword ptr [rip + 0x1b7ab2d]  ; -> 01E0C1E0 [u64 0x00000000009152A0]
002916B3  call     0x24a5a0  ; -> 0024A5A0 fn
002916B8  mov      qword ptr [rsi + 0x10f50], rax
002916BF  mov      r8, qword ptr [rsi + 0x10f50]
002916C6  mov      qword ptr [rbx + 0x988], r8
002916CD  mov      rcx, qword ptr [r8 + 0x20]
002916D1  mov      r8, qword ptr [r8 + 0x30]
002916D5  add      rcx, 0x30
002916D9  movzx    eax, word ptr [rcx + 0x14]
002916DD  movzx    edx, word ptr [rcx + rax*2 + 0x14]
002916E2  movzx    eax, word ptr [rcx + 0x10]
002916E6  add      rcx, rax
002916E9  lea      rdx, [rcx + rdx*8]
002916ED  lea      rcx, [rsp + 0x20]
002916F2  call     0x271140  ; -> 00271140 fn
002916F7  lea      rdx, [rsp + 0x20]
002916FC  mov      rcx, rbx
002916FF  call     0x3f2600  ; -> 003F2600 fn
00291704  mov      eax, 1
00291709  mov      rdx, rbx
0029170C  mov      word ptr [rbx + 0x9c0], ax
00291713  mov      rcx, qword ptr [rsi + 0x10f20]
0029171A  call     0x3f2580  ; -> 003F2580 fn
0029171F  mov      qword ptr [rsi + 0x10f20], rax
00291726  mov      rax, rbx
00291729  mov      rbx, qword ptr [rsp + 0x40]
0029172E  mov      rcx, qword ptr [rsp + 0x30]
00291733  xor      rcx, rsp
00291736  call     0x808c40  ; -> 00808C40 fn
0029173B  add      rsp, 0x48
0029173F  pop      r14
00291741  pop      rdi
00291742  pop      rsi
00291743  pop      rbp
00291744  ret      
```

## 002E84B0 (72 B, extent 002E84B0-002E84F8)

Page context: "notes and was > not applied.  Channels 6-9 are reached from the script verbs **'rgbatrans'** ('03B2', five arguments) and **'puppetrgbatrans'** ('0535', six) through the two actor-service forwarders '002E84B0' and '002E8500', each of which tail-jumps into '00428C40'. The names are the game's own.  ## 4. Who reads them  **'CharacterRenderRecord_EvaluateQ12PresentationChannel' - '003E48E0'** '(record, selector)' (604 B). Its body is four "

```
002E84B0  movaps   xmm4, xmm1
002E84B3  test     rcx, rcx
002E84B6  je       0x2e84f7  ; -> 002E84F7
002E84B8  mov      rax, qword ptr [rcx + 0xc0]
002E84BF  test     rax, rax
002E84C2  je       0x2e84f7  ; -> 002E84F7
002E84C4  cmp      dword ptr [rax], -1
002E84C7  je       0x2e84f7  ; -> 002E84F7
002E84C9  movzx    ecx, word ptr [rax]
002E84CC  cmp      cx, -1
002E84D0  je       0x2e84f7  ; -> 002E84F7
002E84D2  movsx    rax, cx
002E84D6  imul     rcx, rax, 0x740
002E84DD  add      rcx, qword ptr [rip + 0x1fdea44]  ; -> 022C6F28
002E84E4  je       0x2e84f7  ; -> 002E84F7
002E84E6  cmp      dword ptr [rcx + 0x284], 0
002E84ED  je       0x2e84f7  ; -> 002E84F7
002E84EF  movaps   xmm1, xmm4
002E84F2  jmp      0x428c40  ; -> 00428C40 fn
002E84F7  ret      
```

## 002E8500 (60 B, extent 002E8500-002E853C)

Page context: " not applied.  Channels 6-9 are reached from the script verbs **'rgbatrans'** ('03B2', five arguments) and **'puppetrgbatrans'** ('0535', six) through the two actor-service forwarders '002E84B0' and '002E8500', each of which tail-jumps into '00428C40'. The names are the game's own.  ## 4. Who reads them  **'CharacterRenderRecord_EvaluateQ12PresentationChannel' - '003E48E0'** '(record, selector)' (604 B). Its body is four copies of the f"

```
002E8500  movaps   xmm4, xmm1
002E8503  test     rcx, rcx
002E8506  je       0x2e853b  ; -> 002E853B
002E8508  cmp      dword ptr [rcx], -1
002E850B  je       0x2e853b  ; -> 002E853B
002E850D  movzx    eax, word ptr [rcx]
002E8510  cmp      ax, -1
002E8514  je       0x2e853b  ; -> 002E853B
002E8516  movsx    rax, ax
002E851A  imul     rcx, rax, 0x740
002E8521  add      rcx, qword ptr [rip + 0x1fdea00]  ; -> 022C6F28
002E8528  je       0x2e853b  ; -> 002E853B
002E852A  cmp      dword ptr [rcx + 0x284], 0
002E8531  je       0x2e853b  ; -> 002E853B
002E8533  movaps   xmm1, xmm4
002E8536  jmp      0x428c40  ; -> 00428C40 fn
002E853B  ret      
```

## 002EBBB0 (50 B, extent 002EBBB0-002EBBE2)

Page context: "EQ-FABLE-PHOOK-BIT0-WHO-READS-IT').** An image-wide sweep of the displacement '0x48818' finds ten bodies touching the word. Bit 0 is *set and cleared* by the distance-cull enable family ('002E8CC0', '002EBBB0', '002EBBF0') and the initialiser, and **read by this routine alone** - three tests. This routine's one caller '0042D7A0' has no call site: it is the per-record callback of the distance-fade *system phase* (taken by 'lea' at '00426"

```
002EBBB0  movzx    eax, byte ptr [rip + 0x1e7419f]  ; -> 0215FD56
002EBBB7  test     ecx, ecx
002EBBB9  je       0x2ebbbf  ; -> 002EBBBF
002EBBBB  and      al, 0xfe
002EBBBD  jmp      0x2ebbc1  ; -> 002EBBC1
002EBBBF  or       al, 1
002EBBC1  mov      byte ptr [rip + 0x1e7418f], al  ; -> 0215FD56
002EBBC7  test     al, al
002EBBC9  mov      rax, qword ptr [rip + 0x1fdb358]  ; -> 022C6F28
002EBBD0  jne      0x2ebbda  ; -> 002EBBDA
002EBBD2  or       dword ptr [rax + 0x48818], 1
002EBBD9  ret      
002EBBDA  and      dword ptr [rax + 0x48818], 0xfffffffe
002EBBE1  ret      
```

## 002EBBF0 (64 B, extent 002EBBF0-002EBC30)

Page context: "OK-BIT0-WHO-READS-IT').** An image-wide sweep of the displacement '0x48818' finds ten bodies touching the word. Bit 0 is *set and cleared* by the distance-cull enable family ('002E8CC0', '002EBBB0', '002EBBF0') and the initialiser, and **read by this routine alone** - three tests. This routine's one caller '0042D7A0' has no call site: it is the per-record callback of the distance-fade *system phase* (taken by 'lea' at '0042650E'). *Read"

```
002EBBF0  movzx    eax, byte ptr [rip + 0x1e7415f]  ; -> 0215FD56
002EBBF7  mov      r8d, 1
002EBBFD  shl      r8d, cl
002EBC00  test     edx, edx
002EBC02  je       0x2ebc0c  ; -> 002EBC0C
002EBC04  not      r8b
002EBC07  and      al, r8b
002EBC0A  jmp      0x2ebc0f  ; -> 002EBC0F
002EBC0C  or       al, r8b
002EBC0F  mov      byte ptr [rip + 0x1e74141], al  ; -> 0215FD56
002EBC15  test     al, al
002EBC17  mov      rax, qword ptr [rip + 0x1fdb30a]  ; -> 022C6F28
002EBC1E  jne      0x2ebc28  ; -> 002EBC28
002EBC20  or       dword ptr [rax + 0x48818], 1
002EBC27  ret      
002EBC28  and      dword ptr [rax + 0x48818], 0xfffffffe
002EBC2F  ret      
```

## 00348700 (42 B, extent 00348700-0034872A)

Page context: "o numbers | '00348B00' | pops the **range**, then the **distance**, and writes both live: the distance to '+0x4881C', the range to '+0x48824' | | 'setcharclipdefaultdistance' ('0x33E'), one number | '00348700' | stores it as the **default** distance ('021641F4') *and* as the live one | | 'setcharclipdefaultfaderange' ('0x33F'), one number | '003497D0' | the same for the range (default at '021641F8') | | 'setcharclipdefaultdistance', two"

```
00348700  sub      rsp, 0x38
00348704  mov      rcx, r9
00348707  movaps   xmmword ptr [rsp + 0x20], xmm6
0034870C  call     0x267db0  ; -> 00267DB0 fn
00348711  movaps   xmm6, xmm0
00348714  call     0x2eda70  ; -> 002EDA70 fn
00348719  movaps   xmm0, xmm6
0034871C  movaps   xmm6, xmmword ptr [rsp + 0x20]
00348721  add      rsp, 0x38
00348725  jmp      0x26a460  ; -> 0026A460 fn
```

## 00348B00 (56 B, extent 00348B00-00348B38)

Page context: "f the two distances (added 2026-09-19; four verb handlers and their setters read whole).**  | verb (call id) | handler | what it does | |---|---|---| | 'setcharclipdistance' ('0x327'), two numbers | '00348B00' | pops the **range**, then the **distance**, and writes both live: the distance to '+0x4881C', the range to '+0x48824' | | 'setcharclipdefaultdistance' ('0x33E'), one number | '00348700' | stores it as the **default** distance ('0"

```
00348B00  push     rbx
00348B02  sub      rsp, 0x30
00348B06  mov      rcx, r9
00348B09  movaps   xmmword ptr [rsp + 0x20], xmm6
00348B0E  mov      rbx, r9
00348B11  call     0x267db0  ; -> 00267DB0 fn
00348B16  mov      rcx, rbx
00348B19  movaps   xmm6, xmm0
00348B1C  call     0x267db0  ; -> 00267DB0 fn
00348B21  call     0x26a460  ; -> 0026A460 fn
00348B26  movaps   xmm0, xmm6
00348B29  movaps   xmm6, xmmword ptr [rsp + 0x20]
00348B2E  add      rsp, 0x30
00348B32  pop      rbx
00348B33  jmp      0x2e83a0  ; -> 002E83A0 fn
```

## 00348F20 (85 B, extent 00348F20-00348F75)

Page context: "d* as the live one | | 'setcharclipdefaultfaderange' ('0x33F'), one number | '003497D0' | the same for the range (default at '021641F8') | | 'setcharclipdefaultdistance', two-number form ('0x340') | '00348F20' | both defaults and both live values |  The system starts at **34.0 and 4.0**. In the 1,114 decompiled scripts the two-number verb is called with (22, 3) 103 times, (27, 3) 15, (28, 2) 13, (20, 3) 6, (50, 2) 5, and 15 times with '"

```
00348F20  push     rbx
00348F22  sub      rsp, 0x40
00348F26  movaps   xmmword ptr [rsp + 0x30], xmm6
00348F2B  mov      rcx, r9
00348F2E  movaps   xmmword ptr [rsp + 0x20], xmm7
00348F33  mov      rbx, r9
00348F36  call     0x267db0  ; -> 00267DB0 fn
00348F3B  mov      rcx, rbx
00348F3E  movaps   xmm7, xmm0
00348F41  call     0x267db0  ; -> 00267DB0 fn
00348F46  movaps   xmm6, xmm0
00348F49  call     0x2eda70  ; -> 002EDA70 fn
00348F4E  movaps   xmm0, xmm7
00348F51  call     0x2eda80  ; -> 002EDA80 fn
00348F56  movaps   xmm0, xmm6
00348F59  call     0x26a460  ; -> 0026A460 fn
00348F5E  movaps   xmm0, xmm7
00348F61  movaps   xmm6, xmmword ptr [rsp + 0x30]
00348F66  movaps   xmm7, xmmword ptr [rsp + 0x20]
00348F6B  add      rsp, 0x40
00348F6F  pop      rbx
00348F70  jmp      0x2e83a0  ; -> 002E83A0 fn
```

## 003497D0 (42 B, extent 003497D0-003497FA)

Page context: "| 'setcharclipdefaultdistance' ('0x33E'), one number | '00348700' | stores it as the **default** distance ('021641F4') *and* as the live one | | 'setcharclipdefaultfaderange' ('0x33F'), one number | '003497D0' | the same for the range (default at '021641F8') | | 'setcharclipdefaultdistance', two-number form ('0x340') | '00348F20' | both defaults and both live values |  The system starts at **34.0 and 4.0**. In the 1,114 decompiled scrip"

```
003497D0  sub      rsp, 0x38
003497D4  mov      rcx, r9
003497D7  movaps   xmmword ptr [rsp + 0x20], xmm6
003497DC  call     0x267db0  ; -> 00267DB0 fn
003497E1  movaps   xmm6, xmm0
003497E4  call     0x2eda80  ; -> 002EDA80 fn
003497E9  movaps   xmm0, xmm6
003497EC  movaps   xmm6, xmmword ptr [rsp + 0x20]
003497F1  add      rsp, 0x38
003497F5  jmp      0x2e83a0  ; -> 002E83A0 fn
```

## 00373160 (534 B, extent 00373160-00373376)

Page context: "d before their tails - the stack-table probe's pose publish on the render record.  Interior anchor '00370FF6' (function '00370FA0').  '003737C0' (160 B) is the tag-index search '00370FA0'/'00372800'/'00373160' call on 'dword[rcx+0xA0]''s handle table: two '0020E600' decodes fetch the table (null exits '0xFFFF'), then 'dword[+0xC]' entries iterate - each slot resolves through '00409270' + '00409250' and the first entry whose 'word' tag e"

```
00373160  push     rbp
00373162  push     r13
00373164  push     r15
00373166  sub      rsp, 0x40
0037316A  mov      rbp, rcx
0037316D  mov      r13d, r8d
00373170  mov      ecx, dword ptr [rcx + 0xa0]
00373176  mov      r15, rdx
00373179  call     0x20e600  ; -> 0020E600 fn
0037317E  test     rax, rax
00373181  je       0x37336c  ; -> 0037336C
00373187  mov      ecx, dword ptr [rbp + 0x84]
0037318D  mov      qword ptr [rsp + 0x38], rsi
00373192  mov      qword ptr [rsp + 0x30], rdi
00373197  mov      qword ptr [rsp + 0x28], r12
0037319C  mov      qword ptr [rsp + 0x20], r14
003731A1  call     0x20e600  ; -> 0020E600 fn
003731A6  mov      ecx, dword ptr [rbp + 0x84]
003731AC  mov      r12, rax
003731AF  call     0x20e600  ; -> 0020E600 fn
003731B4  movsx    rcx, word ptr [rbp + 0x88]
003731BC  imul     r14, rcx, 0x290
003731C3  mov      ecx, dword ptr [rbp + 0xa0]
003731C9  add      r14, rax
003731CC  call     0x20e600  ; -> 0020E600 fn
003731D1  mov      ecx, dword ptr [r15 + 0x84]
003731D8  mov      rdi, rax
003731DB  mov      qword ptr [rsp + 0x60], rax
003731E0  call     0x20e600  ; -> 0020E600 fn
003731E5  mov      ecx, dword ptr [r15 + 4]
003731E9  mov      dword ptr [rbp + 8], ecx
003731EC  mov      qword ptr [rsp + 0x78], rax
003731F1  cmp      r13d, -1
003731F5  je       0x3731fe  ; -> 003731FE
003731F7  mov      word ptr [rbp + 0x14], r13w
003731FC  jmp      0x373205  ; -> 00373205
003731FE  mov      eax, dword ptr [rbp + 4]
00373201  mov      dword ptr [r15 + 0x10], eax
00373205  xor      esi, esi
00373207  cmp      si, word ptr [rbp + 0x8a]
0037320E  jge      0x373358  ; -> 00373358
00373214  mov      qword ptr [rsp + 0x68], rbx
00373219  nop      dword ptr [rax]
00373220  movsx    rax, word ptr [r14]
00373224  mov      rcx, rdi
00373227  imul     rbx, rax, 0x290
0037322E  add      rbx, r12
00373231  movsx    edx, word ptr [rbx + 0x27e]
00373238  call     0x409270  ; -> 00409270 fn
0037323D  movzx    ecx, word ptr [rbx + 0x270]
00373244  mov      word ptr [rbx + 0x28e], cx
0037324B  cmp      r13d, -1
0037324F  jne      0x37333e  ; -> 0037333E
00373255  test     dword ptr [rax + 4], 0x100
0037325C  je       0x37333e  ; -> 0037333E
00373262  mov      rcx, rax
00373265  call     0x409250  ; -> 00409250 fn
0037326A  cmp      dword ptr [r15 + 0x9c], 2
00373272  movzx    edx, ax
00373275  je       0x37327c  ; -> 0037327C
00373277  or       eax, r13d
0037327A  jmp      0x373284  ; -> 00373284
0037327C  mov      rcx, r15
0037327F  call     0x3737c0  ; -> 003737C0 fn
00373284  movsx    rdi, ax
00373288  cmp      edi, -1
0037328B  je       0x373339  ; -> 00373339
00373291  movzx    edx, di
00373294  mov      rcx, r15
00373297  call     0x3725a0  ; -> 003725A0 fn
0037329C  test     eax, eax
0037329E  je       0x373339  ; -> 00373339
003732A4  mov      rax, rdi
003732A7  movzx    eax, word ptr [rbx + 0x270]
003732AE  imul     rdi, rdi, 0x290
003732B5  add      rdi, qword ptr [rsp + 0x78]
003732BA  cmp      ax, -1
003732BE  je       0x3732ef  ; -> 003732EF
003732C0  movsx    rax, ax
003732C4  imul     rcx, rax, 0x290
003732CB  cmp      word ptr [rcx + r12 + 0x28e], -1
003732D5  jne      0x3732ef  ; -> 003732EF
003732D7  or       eax, 0xffffffff
003732DA  mov      word ptr [rbx + 0x270], ax
003732E1  movzx    eax, word ptr [rdi + 0x270]
003732E8  mov      word ptr [rbx + 0x276], ax
003732EF  mov      rcx, rbx
003732F2  call     0x20e620  ; -> 0020E620 fn
003732F7  mov      dword ptr [rdi + 0x278], eax
003732FD  lea      rdx, [rdi + 0xc0]
00373304  movzx    eax, word ptr [rbx + 0x27e]
0037330B  lea      rcx, [rbx + 0xc0]
00373312  mov      word ptr [rdi + 0x27c], ax
00373319  call     0x46d100  ; -> 0046D100 fn
0037331E  lea      rdx, [rdi + 0x150]
00373325  lea      rcx, [rbx + 0x150]
0037332C  call     0x46d100  ; -> 0046D100 fn
00373331  or       word ptr [rbx + 0x280], 2
00373339  mov      rdi, qword ptr [rsp + 0x60]
0037333E  movsx    eax, word ptr [rbp + 0x8a]
00373345  inc      esi
00373347  add      r14, 2
0037334B  cmp      esi, eax
0037334D  jl       0x373220  ; -> 00373220
00373353  mov      rbx, qword ptr [rsp + 0x68]
00373358  mov      r12, qword ptr [rsp + 0x28]
0037335D  mov      rdi, qword ptr [rsp + 0x30]
00373362  mov      rsi, qword ptr [rsp + 0x38]
00373367  mov      r14, qword ptr [rsp + 0x20]
0037336C  add      rsp, 0x40
00373370  pop      r15
00373372  pop      r13
00373374  pop      rbp
00373375  ret      
```

## 003AFD50 (37 B, extent 003AFD50-003AFD75)

Page context: "'s '+0x274' instead when bit 2 of '+0xC0' is up -    the second a value from the record times '+0x278'. The handle at '+0x118' indexes the 32-entry '0x70'-stride table at    '02B3F570' the same way: '003AFD50' (37 B) stores the same scalar at '+8', and '003AFD80' (73 B) is given a vector    built from the record's scale '+0x160', its second scale '+0x260'..'+0x268' and '+0x278', of which it keeps the    middle component at '+0x10' and i"

```
003AFD50  movzx    edx, cl
003AFD53  imul     rax, rdx, 0x70
003AFD57  lea      rdx, [rip + 0x278f812]  ; -> 02B3F570
003AFD5E  add      rax, rdx
003AFD61  xor      edx, edx
003AFD63  cmp      dword ptr [rax + 4], ecx
003AFD66  cmovne   rax, rdx
003AFD6A  test     rax, rax
003AFD6D  je       0x3afd74  ; -> 003AFD74
003AFD6F  movss    dword ptr [rax + 8], xmm1
003AFD74  ret      
```

## 003AFD80 (73 B, extent 003AFD80-003AFDC9)

Page context: "he second a value from the record times '+0x278'. The handle at '+0x118' indexes the 32-entry '0x70'-stride table at    '02B3F570' the same way: '003AFD50' (37 B) stores the same scalar at '+8', and '003AFD80' (73 B) is given a vector    built from the record's scale '+0x160', its second scale '+0x260'..'+0x268' and '+0x278', of which it keeps the    middle component at '+0x10' and its reciprocal at '+0x14', only when that component has"

```
003AFD80  movzx    r8d, cl
003AFD84  imul     rax, r8, 0x70
003AFD88  lea      r8, [rip + 0x278f7e1]  ; -> 02B3F570
003AFD8F  add      rax, r8
003AFD92  xor      r8d, r8d
003AFD95  cmp      dword ptr [rax + 4], ecx
003AFD98  cmovne   rax, r8
003AFD9C  test     rax, rax
003AFD9F  je       0x3afdc8  ; -> 003AFDC8
003AFDA1  movss    xmm1, dword ptr [rdx + 4]
003AFDA6  movss    xmm0, dword ptr [rax + 0x10]
003AFDAB  ucomiss  xmm0, xmm1
003AFDAE  jp       0x3afdb2  ; -> 003AFDB2
003AFDB0  je       0x3afdc8  ; -> 003AFDC8
003AFDB2  movss    xmm0, dword ptr [rip + 0x193bdee]  ; -> 01CEBBA8 [f32 1]
003AFDBA  divss    xmm0, xmm1
003AFDBE  movss    dword ptr [rax + 0x10], xmm1
003AFDC3  movss    dword ptr [rax + 0x14], xmm0
003AFDC8  ret      
```

## 003B6BB0 (28 B, extent 003B6BB0-003B6BCC)

Page context: "ide objects get a scalar.** The handle at '+0x114' indexes a table of '0xE0'-byte entries    behind the pointer '02B40528' by its low byte, the entry's '+0x10' holding the full handle as a check:    '003B6BB0' (28 B) stores the entry's '+0x2C' and '003B6BD0' (28 B) its '+0x44'. The first receives *composite    scalar with the view factor as multiplier x alpha* - or the record's '+0x274' instead when bit 2 of '+0xC0' is up -    the secon"

```
003B6BB0  movzx    edx, cl
003B6BB3  imul     rax, rdx, 0xe0
003B6BBA  add      rax, qword ptr [rip + 0x2789967]  ; -> 02B40528
003B6BC1  cmp      dword ptr [rax + 0x10], ecx
003B6BC4  jne      0x3b6bcb  ; -> 003B6BCB
003B6BC6  movss    dword ptr [rax + 0x2c], xmm1
003B6BCB  ret      
```

## 003B6BD0 (28 B, extent 003B6BD0-003B6BEC)

Page context: "' indexes a table of '0xE0'-byte entries    behind the pointer '02B40528' by its low byte, the entry's '+0x10' holding the full handle as a check:    '003B6BB0' (28 B) stores the entry's '+0x2C' and '003B6BD0' (28 B) its '+0x44'. The first receives *composite    scalar with the view factor as multiplier x alpha* - or the record's '+0x274' instead when bit 2 of '+0xC0' is up -    the second a value from the record times '+0x278'. The han"

```
003B6BD0  movzx    edx, cl
003B6BD3  imul     rax, rdx, 0xe0
003B6BDA  add      rax, qword ptr [rip + 0x2789947]  ; -> 02B40528
003B6BE1  cmp      dword ptr [rax + 0x10], ecx
003B6BE4  jne      0x3b6beb  ; -> 003B6BEB
003B6BE6  movss    dword ptr [rax + 0x44], xmm1
003B6BEB  ret      
```

## 003E4780 (59 B, extent 003E4780-003E47BB)

Page context: "t, so **an attached piece inherits its owner's fade**. 'ComputeCompositePresentationScalar' ('003E4730') turns that word into the float '(+0x4B4 / 4096) * [+0x22C] * [+0x2EC] / 255', and its sibling '003E4780' takes the last factor from its caller instead of '+0x2EC'.  **'CharacterRenderRecord_BuildPresentationChannelVector4' - '003E51F0'** '(record, float out[4])' (701 B) is the evaluator inlined in a loop over selectors 6, 7, 8 and 9,"

```
003E4780  movsx    eax, word ptr [rcx + 0x4b4]
003E4787  movss    xmm0, dword ptr [rcx + 0x22c]
003E478F  cvtps2pd xmm0, xmm0
003E4792  movd     xmm2, eax
003E4796  cvtdq2pd xmm2, xmm2
003E479A  cvtss2sd xmm1, xmm1
003E479E  mulsd    xmm2, qword ptr [rip + 0x92d01a]  ; -> 00D117C0 [f64 0.000244140625]
003E47A6  mulsd    xmm2, xmm0
003E47AA  mulsd    xmm2, xmm1
003E47AE  mulsd    xmm2, qword ptr [rip + 0x92d012]  ; -> 00D117C8 [f64 0.003921568859]
003E47B6  cvtpd2ps xmm0, xmm2
003E47BA  ret      
```

## 0041FBF0 (135 B, extent 0041FBF0-0041FC77)

Page context: "ancestor, ~~and the flag handed over with it says whether the whole chain is also unculled.~~  **Corrected 2026-09-19 (FABLE): bit 5 has no live source, so that second flag is always 0.** The setter '0041FBF0' (135 B, read whole) is called only by the propagation '00429D40' (271 B, read whole) and its descendant callback '0042DE50' (59 B): the value is **bit 2 of the requested-state word '+0x304'**, applied to the record, its child and "

```
0041FBF0  mov      qword ptr [rsp + 8], rbx
0041FBF5  mov      qword ptr [rsp + 0x10], rsi
0041FBFA  push     rdi
0041FBFB  sub      rsp, 0x20
0041FBFF  mov      edi, dword ptr [rcx + 0x18]
0041FC02  mov      esi, edx
0041FC04  mov      rbx, rcx
0041FC07  cmp      edi, -1
0041FC0A  je       0x41fc29  ; -> 0041FC29
0041FC0C  mov      ecx, dword ptr [rcx + 0x10]
0041FC0F  call     0x20e600  ; -> 0020E600 fn
0041FC14  mov      rcx, qword ptr [rax + 0xd98]
0041FC1B  cmp      edi, -1
0041FC1E  je       0x41fc29  ; -> 0041FC29
0041FC20  mov      edx, edi
0041FC22  call     0x2ed570  ; -> 002ED570 fn
0041FC27  jmp      0x41fc2b  ; -> 0041FC2B
0041FC29  xor      eax, eax
0041FC2B  cmp      esi, 1
0041FC2E  jne      0x41fc49  ; -> 0041FC49
0041FC30  or       dword ptr [rbx + 0x284], 0x20
0041FC37  test     rax, rax
0041FC3A  je       0x41fc3f  ; -> 0041FC3F
0041FC3C  or       dword ptr [rax], 4
0041FC3F  mov      rcx, rbx
0041FC42  call     0x422f80  ; -> 00422F80 fn
0041FC47  jmp      0x41fc60  ; -> 0041FC60
0041FC49  and      dword ptr [rbx + 0x284], 0xffffffdf
0041FC50  test     rax, rax
0041FC53  je       0x41fc58  ; -> 0041FC58
0041FC55  and      dword ptr [rax], 0xfffffffb
0041FC58  mov      rcx, rbx
0041FC5B  call     0x422f30  ; -> 00422F30 fn
0041FC60  mov      rcx, rbx
0041FC63  mov      rbx, qword ptr [rsp + 0x30]
0041FC68  mov      rsi, qword ptr [rsp + 0x38]
0041FC6D  add      rsp, 0x20
0041FC71  pop      rdi
0041FC72  jmp      0x421030  ; -> 00421030 fn
```

## 00420F90 (29 B, extent 00420F90-00420FAD)

Page context: "**: '00421010' (29 B, read whole) is called by this page's fade-and-cull routine with 1 when none of the cull bits 0, 1 and 3 of '+0xD3' is up and with 0 otherwise. **Bit 4 is "display requested"**: '00420F90' (29 B, read whole) is called by the dirty-state pass, on dirty bit 4 of '+0x290', with bit 1 of the requested-state word '+0x304'. Both setters tail-jump into the chain step '00421030', so bit 6 is re-derived at once. **Bit 5** ha"

```
00420F90  cmp      edx, 1
00420F93  jne      0x420fa1  ; -> 00420FA1
00420F95  or       dword ptr [rcx + 0x284], 0x10
00420F9C  jmp      0x421030  ; -> 00421030 fn
00420FA1  and      dword ptr [rcx + 0x284], 0xffffffef
00420FA8  jmp      0x421030  ; -> 00421030 fn
```

## 004293C0 (67 B, extent 004293C0-00429403)

Page context: "('+0xD3' and '0x0B') are up, '0.0' over 1 frame | | 1 | '+0x4C8' | '0042E1F0', '0042F880'; *and, added 2026-09-19,* authored presentation command '0x23' ('00520180', 47 B) through a second forwarder '004293C0' (67 B) | **attached-piece visibility.** '0042E1F0' sets it to '0.0' at once when the owner's flag '0x08000000' of '+0x284' is up or the owner's '+0xCC' low twelve bits equal '0x35'; otherwise to '1.0' at once, or a ramp to '0.0' o"

```
004293C0  cmp      r9d, 1
004293C4  jle      0x3e5d00  ; -> 003E5D00 fn
004293CA  cmp      dword ptr [rsp + 0x28], 1
004293CF  jne      0x4293f9  ; -> 004293F9
004293D1  movzx    eax, word ptr [rcx + 8]
004293D5  cmp      ax, -1
004293D9  je       0x429402  ; -> 00429402
004293DB  movsx    rax, ax
004293DF  imul     rcx, rax, 0x740
004293E6  xor      eax, eax
004293E8  add      rcx, qword ptr [rip + 0x1e9db39]  ; -> 022C6F28
004293EF  cmp      dword ptr [rcx + 0x284], eax
004293F5  cmove    rcx, rax
004293F9  test     rcx, rcx
004293FC  jne      0x3e5d60  ; -> 003E5D60 fn
00429402  ret      
```

## 0042DE50 (59 B, extent 0042DE50-0042DE8B)

Page context: "): bit 5 has no live source, so that second flag is always 0.** The setter '0041FBF0' (135 B, read whole) is called only by the propagation '00429D40' (271 B, read whole) and its descendant callback '0042DE50' (59 B): the value is **bit 2 of the requested-state word '+0x304'**, applied to the record, its child and their descendants. '00429D40' runs only under **dirty bit 5 of '+0x290'**. Neither end is alive in this image: of the instru"

```
0042DE50  mov      qword ptr [rsp + 8], rbx
0042DE55  push     rdi
0042DE56  sub      rsp, 0x20
0042DE5A  mov      rdi, rdx
0042DE5D  mov      rbx, rcx
0042DE60  mov      rdx, qword ptr [rdx + 8]
0042DE64  call     0x426220  ; -> 00426220 fn
0042DE69  test     eax, eax
0042DE6B  jne      0x42de80  ; -> 0042DE80
0042DE6D  mov      edx, dword ptr [rdi + 0x38]
0042DE70  mov      rcx, rbx
0042DE73  call     0x41fbf0  ; -> 0041FBF0 fn
0042DE78  mov      rcx, rbx
0042DE7B  call     0x421030  ; -> 00421030 fn
0042DE80  mov      rbx, qword ptr [rsp + 0x30]
0042DE85  add      rsp, 0x20
0042DE89  pop      rdi
0042DE8A  ret      
```
