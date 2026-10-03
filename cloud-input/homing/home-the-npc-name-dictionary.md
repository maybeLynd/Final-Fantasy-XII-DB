# Homing pack: `04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-npc-name-dictionary.json`.

Bodies: 8. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0017F0B0 (15 B, extent 0017F0B0-0017F0BF)

Entered from (direct sites whose caller this page cites): `0053AB50` + 0x2CA (call; `0053AB50` is cited on this page); `0053AB50` + 0x2DC (call; `0053AB50` is cited on this page)
Other direct sites: none

Host context: "ex/ADDRESS-INDEX.md), read back at '0055BF1D'; '00282DF0' first call at '0055BAE0', then '00365B30'/'002F9860'/'002DD7E0'/'002DB080'), and three PhyreEngine objects in '0063xxxx'. Eight are untyped: '0053AB50' twice ('0053B701', '0053B730', 'mov word [r13 + r15*2 + 0x100]' — an indexed array element whose base 'r13' is the function's second argument, which the auditor traces to the FCP character parameter block fed from '00521290' recor" / "ex/ADDRESS-INDEX.md), read back at '0055BF1D'; '00282DF0' first call at '0055BAE0', then '00365B30'/'002F9860'/'002DD7E0'/'002DB080'), and three PhyreEngine objects in '0063xxxx'. Eight are untyped: '0053AB50' twice ('0053B701', '0053B730', 'mov word [r13 + r15*2 + 0x100]' — an indexed array element whose base 'r13' is the function's second argument, which the auditor traces to the FCP character parameter block fed from '00521290' recor"

```
0017F0B0  test     rcx, rcx
0017F0B3  je       0x17f0be  ; -> 0017F0BE
0017F0B5  mov      rax, qword ptr [rcx]
0017F0B8  xor      edx, edx
0017F0BA  jmp      qword ptr [rax + 8]
0017F0BE  ret      
```

## 0017F200 (16 B, extent 0017F200-0017F210)

Entered from (direct sites whose caller this page cites): `0053AB50` + 0x4A1 (call; `0053AB50` is cited on this page)
Other direct sites: none

Host context: "ex/ADDRESS-INDEX.md), read back at '0055BF1D'; '00282DF0' first call at '0055BAE0', then '00365B30'/'002F9860'/'002DD7E0'/'002DB080'), and three PhyreEngine objects in '0063xxxx'. Eight are untyped: '0053AB50' twice ('0053B701', '0053B730', 'mov word [r13 + r15*2 + 0x100]' — an indexed array element whose base 'r13' is the function's second argument, which the auditor traces to the FCP character parameter block fed from '00521290' recor"

```
0017F200  test     rcx, rcx
0017F203  je       0x17f20f  ; -> 0017F20F
0017F205  mov      r8, qword ptr [rcx]
0017F208  jmp      qword ptr [r8 + 0xc0]
0017F20F  ret      
```

## 0017F210 (16 B, extent 0017F210-0017F220)

Entered from (direct sites whose caller this page cites): `0053AB50` + 0x242D (call; `0053AB50` is cited on this page)
Other direct sites: none

Host context: "ex/ADDRESS-INDEX.md), read back at '0055BF1D'; '00282DF0' first call at '0055BAE0', then '00365B30'/'002F9860'/'002DD7E0'/'002DB080'), and three PhyreEngine objects in '0063xxxx'. Eight are untyped: '0053AB50' twice ('0053B701', '0053B730', 'mov word [r13 + r15*2 + 0x100]' — an indexed array element whose base 'r13' is the function's second argument, which the auditor traces to the FCP character parameter block fed from '00521290' recor"

```
0017F210  test     rcx, rcx
0017F213  je       0x17f21f  ; -> 0017F21F
0017F215  mov      r10, qword ptr [rcx]
0017F218  jmp      qword ptr [r10 + 0x80]
0017F21F  ret      
```

## 0017F220 (21 B, extent 0017F220-0017F235)

Entered from (direct sites whose caller this page cites): `0053AB50` + 0x41D (call; `0053AB50` is cited on this page)
Other direct sites: none

Host context: "ex/ADDRESS-INDEX.md), read back at '0055BF1D'; '00282DF0' first call at '0055BAE0', then '00365B30'/'002F9860'/'002DD7E0'/'002DB080'), and three PhyreEngine objects in '0063xxxx'. Eight are untyped: '0053AB50' twice ('0053B701', '0053B730', 'mov word [r13 + r15*2 + 0x100]' — an indexed array element whose base 'r13' is the function's second argument, which the auditor traces to the FCP character parameter block fed from '00521290' recor"

```
0017F220  test     rcx, rcx
0017F223  je       0x17f234  ; -> 0017F234
0017F225  mov      rax, qword ptr [rcx]
0017F228  test     edx, edx
0017F22A  setne    dl
0017F22D  jmp      qword ptr [rax + 0xa8]
0017F234  ret      
```

## 00182870 (70 B, extent 00182870-001828B6)

Entered from (direct sites whose caller this page cites): `00382BF0` + 0xCC (call; `00382BF0` is cited on this page); `00382BF0` + 0xF6 (call; `00382BF0` is cited on this page)
Other direct sites: none

Host context: "0'; then the '00254380'/'00264F90'/'00315DC0'/'00380170'/'0046B180'/'0046B240'/'00473BB0' chain iterates 'cx' - the dictionary's armed-table walk.  Interior anchor '003C0A4A' (function '003C0A00').  '00382BF0' (285 B) is the '02AEDFA0'-gated position publisher '0053AB50' calls: 'dword[02AEDFA0] != ecx' exits; 'word[02AEDFA0]' resolves 'sx x 0x740 + 022C6F28' (a '-1', a null base, or 'dword[+0x284] == 0' fails into '00182870(0, -1.0f, 0)" / "0'; then the '00254380'/'00264F90'/'00315DC0'/'00380170'/'0046B180'/'0046B240'/'00473BB0' chain iterates 'cx' - the dictionary's armed-table walk.  Interior anchor '003C0A4A' (function '003C0A00').  '00382BF0' (285 B) is the '02AEDFA0'-gated position publisher '0053AB50' calls: 'dword[02AEDFA0] != ecx' exits; 'word[02AEDFA0]' resolves 'sx x 0x740 + 022C6F28' (a '-1', a null base, or 'dword[+0x284] == 0' fails into '00182870(0, -1.0f, 0)"

```
00182870  mov      qword ptr [rsp + 8], rbx
00182875  push     rdi
00182876  sub      rsp, 0x30
0018287A  movaps   xmmword ptr [rsp + 0x20], xmm6
0018287F  mov      rbx, r8
00182882  movaps   xmm6, xmm1
00182885  mov      edi, ecx
00182887  call     0x193d50  ; -> 00193D50 fn
0018288C  test     rax, rax
0018288F  je       0x1828a6  ; -> 001828A6
00182891  call     0x193d50  ; -> 00193D50 fn
00182896  mov      rcx, rax
00182899  mov      r9, rbx
0018289C  movaps   xmm2, xmm6
0018289F  mov      edx, edi
001828A1  call     0x194490  ; -> 00194490 fn
001828A6  mov      rbx, qword ptr [rsp + 0x40]
001828AB  movaps   xmm6, xmmword ptr [rsp + 0x20]
001828B0  add      rsp, 0x30
001828B4  pop      rdi
001828B5  ret      
```

## 002BA1B0 (64 B, extent 002BA1B0-002BA1F0)

Entered from (direct sites whose caller this page cites): `002BA700` + 0x2F1 (call; `002BA700` is cited on this page); `002BA700` + 0x35C (call; `002BA700` is cited on this page)
Other direct sites: none

Host context: " and payloads dropped. Interior anchor '00521337' (the '+0x1C' flag clear).  ## SWE2-EC7-103 update (2026-09-20) - '002747B0' measured  '002747B0' (137 B) is the '0xD8'-keyed lookup pair '002B7590', '002BA700', '003CB650' and '00552250' call: a nonnull 'rcx' runs '00245000' with the '00275F10' formatter and a stack out-record; a null 'rcx' instead runs '00244F50' with the same '0xD8' size and '00275F10' target - the present-versus-fetch" / " and payloads dropped. Interior anchor '00521337' (the '+0x1C' flag clear).  ## SWE2-EC7-103 update (2026-09-20) - '002747B0' measured  '002747B0' (137 B) is the '0xD8'-keyed lookup pair '002B7590', '002BA700', '003CB650' and '00552250' call: a nonnull 'rcx' runs '00245000' with the '00275F10' formatter and a stack out-record; a null 'rcx' instead runs '00244F50' with the same '0xD8' size and '00275F10' target - the present-versus-fetch"

```
002BA1B0  push     rbx
002BA1B2  sub      rsp, 0x20
002BA1B6  mov      ebx, ecx
002BA1B8  mov      ecx, 0x80
002BA1BD  call     0x2c9430  ; -> 002C9430 fn
002BA1C2  add      eax, ebx
002BA1C4  je       0x2ba1e0  ; -> 002BA1E0
002BA1C6  mov      ecx, 0x81
002BA1CB  call     0x2c9430  ; -> 002C9430 fn
002BA1D0  mov      ecx, eax
002BA1D2  mov      eax, dword ptr [rip + 0x1b52004]  ; -> 01E0C1DC [u32 0x000001C0]
002BA1D8  sub      eax, ecx
002BA1DA  add      rsp, 0x20
002BA1DE  pop      rbx
002BA1DF  ret      
002BA1E0  mov      eax, dword ptr [rip + 0x1b51ff6]  ; -> 01E0C1DC [u32 0x000001C0]
002BA1E6  xor      ecx, ecx
002BA1E8  sub      eax, ecx
002BA1EA  add      rsp, 0x20
002BA1EE  pop      rbx
002BA1EF  ret      
```

## 00370BB0 (26 B, extent 00370BB0-00370BCA)

Entered from (direct sites whose caller this page cites): `0041BEE0` + 0x14A (call; `0041BEE0` is cited on this page)
Other direct sites: none

Host context: "y's own name. **The other 16-bit writers of '+0x102' are not actor records:** '003AAA50' writes a stack local ('rbp = rsp − 0x198', '003AAA57'), '0041B550' a mask object handed in 'rcx' (called from '0041BEE0', which also ORs bits into the same word at '0041B5FA'), and '00552250' / '005528C0' counters of UI objects built by the widget factory. Residue: the same classification for the 16-bit writers of '+0x100' beside '00269F20'. *Residu"

```
00370BB0  mov      eax, dword ptr [rcx + 0x9c]
00370BB6  test     eax, eax
00370BB8  je       0x370bc4  ; -> 00370BC4
00370BBA  cmp      eax, 2
00370BBD  jne      0x370bc9  ; -> 00370BC9
00370BBF  jmp      0x370cd0  ; -> 00370CD0 fn
00370BC4  jmp      0x370bd0  ; -> 00370BD0 fn
00370BC9  ret      
```

## 003E41F0 (71 B, extent 003E41F0-003E4237)

Entered from (direct sites whose caller this page cites): `0053AB50` + 0x427 (call; `0053AB50` is cited on this page)
Other direct sites: none

Host context: "ex/ADDRESS-INDEX.md), read back at '0055BF1D'; '00282DF0' first call at '0055BAE0', then '00365B30'/'002F9860'/'002DD7E0'/'002DB080'), and three PhyreEngine objects in '0063xxxx'. Eight are untyped: '0053AB50' twice ('0053B701', '0053B730', 'mov word [r13 + r15*2 + 0x100]' — an indexed array element whose base 'r13' is the function's second argument, which the auditor traces to the FCP character parameter block fed from '00521290' recor"

```
003E41F0  mov      r8, qword ptr [rip + 0x1ee2d31]  ; -> 022C6F28
003E41F7  xor      r9d, r9d
003E41FA  nop      word ptr [rax + rax]
003E4200  cmp      cx, -1
003E4204  je       0x3e4233  ; -> 003E4233
003E4206  movsx    rax, cx
003E420A  imul     rax, rax, 0x740
003E4211  add      rax, r8
003E4214  cmp      dword ptr [rax + 0x284], r9d
003E421B  cmove    rax, r9
003E421F  test     rax, rax
003E4222  je       0x3e4233  ; -> 003E4233
003E4224  movzx    edx, word ptr [rax + 6]
003E4228  cmp      dx, -1
003E422C  je       0x3e4233  ; -> 003E4233
003E422E  movzx    ecx, dx
003E4231  jmp      0x3e4200  ; -> 003E4200
003E4233  movzx    eax, cx
003E4236  ret      
```
