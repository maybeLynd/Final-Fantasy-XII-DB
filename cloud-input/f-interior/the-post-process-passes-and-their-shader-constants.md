# F-interior pack: `22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-post-process-passes-and-their-shader-constants.json`.

Functions: 12. Each is cited on the page only at its entry and is still in the F frontier.

## 00167050 (66 B, extent 00167050-00167092)

Page context: "ight, not a tail of stubs. The string body this   page left unnamed is '001F5D70' (2,924 B, the 'EASTL vector' one).   - **18 of the 48 are the 'PContextSwitch' family** — eight static installers at '00167050'–'00167280',     the constructor, the base destructor and eight deleting destructors, 1,222 B — read end to end in     [the context-switch axes and the shader-variant key](../Shader-Variant-Selection/the-context-switch-axes-and-the"

```
00167050  sub      rsp, 0x28
00167054  lea      rcx, [rip + 0x1dc7bbd]  ; -> 01F2EC18
0016705B  call     0x6b8d20  ; -> 006B8D20 fn
00167060  test     eax, eax
00167062  jne      0x167074  ; -> 00167074
00167064  inc      dword ptr [rip + 0x2ceb276]  ; -> 02E522E0
0016706A  mov      dword ptr [rip + 0x1dc7bc4], 1  ; -> 01F2EC38 [u32 0x00000000]
00167074  lea      rax, [rip + 0xc19ea5]  ; -> 00D80F20
0016707B  lea      rcx, [rip + 0x74e7ae]  ; -> 008B5830
00167082  mov      qword ptr [rip + 0x1dc7b8f], rax  ; -> 01F2EC18 [u64 0x0000000000D80EA8]
00167089  add      rsp, 0x28
0016708D  jmp      0x808b90  ; -> 00808B90 fn
```

## 00167280 (66 B, extent 00167280-001672C2)

Page context: " tail of stubs. The string body this   page left unnamed is '001F5D70' (2,924 B, the 'EASTL vector' one).   - **18 of the 48 are the 'PContextSwitch' family** — eight static installers at '00167050'–'00167280',     the constructor, the base destructor and eight deleting destructors, 1,222 B — read end to end in     [the context-switch axes and the shader-variant key](../Shader-Variant-Selection/the-context-switch-axes-and-the-variant-ke"

```
00167280  sub      rsp, 0x28
00167284  lea      rcx, [rip + 0x1dc7a2d]  ; -> 01F2ECB8
0016728B  call     0x6b8d20  ; -> 006B8D20 fn
00167290  test     eax, eax
00167292  jne      0x1672a4  ; -> 001672A4
00167294  inc      dword ptr [rip + 0x2ceb046]  ; -> 02E522E0
0016729A  mov      dword ptr [rip + 0x1dc7a34], 1  ; -> 01F2ECD8 [u32 0x00000000]
001672A4  lea      rax, [rip + 0xc19d15]  ; -> 00D80FC0
001672AB  lea      rcx, [rip + 0x74e8fe]  ; -> 008B5BB0
001672B2  mov      qword ptr [rip + 0x1dc79ff], rax  ; -> 01F2ECB8 [u64 0x0000000000D80EA8]
001672B9  add      rsp, 0x28
001672BD  jmp      0x808b90  ; -> 00808B90 fn
```

## 00182E50 (44 B, extent 00182E50-00182E7C)

Page context: "ior anchor '00654FFD' (a '00600120' call).  ## SWE2-EC7-41 update (2026-09-19) - '00186B80'  '00186B80' (332 B) is a post-process body - '0060F6B0' triple/'0060D190'/'005FEFD0'/'00600A60'/'00182F50'/'00182E50'. Interior anchor '00186C01' (a '0060F6B0' call).  ## SWE2-EC7-42 update (2026-09-19) - '00639510'  '00639510' (319 B) is a post-process body - '00D586A0'/'00D586F0', '005CDAA0' pair/'006394B0'/'00633120'/'00639750'/'00639780'/'006"

```
00182E50  sub      rsp, 0x28
00182E54  call     0x1ddab0  ; -> 001DDAB0 fn
00182E59  test     rax, rax
00182E5C  je       0x182e6f  ; -> 00182E6F
00182E5E  call     0x1ddab0  ; -> 001DDAB0 fn
00182E63  mov      rcx, rax
00182E66  add      rsp, 0x28
00182E6A  jmp      0x1dd110  ; -> 001DD110 fn
00182E6F  movss    xmm0, dword ptr [rip + 0x742cc1]  ; -> 008C5B38 [f32 1.777778]
00182E77  add      rsp, 0x28
00182E7B  ret      
```

## 0019EE50 (167 B, extent 0019EE50-0019EEF7)

Page context: "the layer boundary, no shared ownership. - **Resource - CLIENT and SERVICE (86 edges).** '00193D50', '0019CE20', '001AD440', '0020B5F0' (+14 more) are called by bodies filed to Resource: '0019EAA0', '0019EE50', '001A0CF0', '001A0E50' (+25 more); '0018D160', '0019CB20', '001F5D70', '00597970' (+6 more) reach bodies filed to Resource: '001D6AA0', '0020B5F0', '002150D0', '002DF980' (+12 more) - shared machinery across the layer boundary, n"

```
0019EE50  mov      qword ptr [rsp + 0x10], rbx
0019EE55  push     rsi
0019EE56  sub      rsp, 0x20
0019EE5A  mov      rax, qword ptr [rcx + 0x108]
0019EE61  xor      esi, esi
0019EE63  sub      rax, qword ptr [rcx + 0x100]
0019EE6A  mov      rbx, rcx
0019EE6D  sar      rax, 3
0019EE71  test     eax, eax
0019EE73  je       0x19eee5  ; -> 0019EEE5
0019EE75  mov      qword ptr [rsp + 0x30], rdi
0019EE7A  nop      word ptr [rax + rax]
0019EE80  mov      rax, qword ptr [rbx + 0x100]
0019EE87  lea      rdi, [rsi*8]
0019EE8F  mov      rcx, qword ptr [rax + rdi]
0019EE93  mov      rcx, qword ptr [rcx + 0x108]
0019EE9A  call     0x63da50  ; -> 0063DA50 fn
0019EE9F  mov      rax, qword ptr [rbx + 0x100]
0019EEA6  mov      rcx, qword ptr [rax + rdi]
0019EEAA  mov      rcx, qword ptr [rcx + 0x108]
0019EEB1  call     0x63b010  ; -> 0063B010 fn
0019EEB6  mov      rax, qword ptr [rbx + 0x108]
0019EEBD  inc      esi
0019EEBF  sub      rax, qword ptr [rbx + 0x100]
0019EEC6  sar      rax, 3
0019EECA  cmp      esi, eax
0019EECC  jb       0x19ee80  ; -> 0019EE80
0019EECE  mov      byte ptr [rbx + 0x128], 1
0019EED5  mov      rdi, qword ptr [rsp + 0x30]
0019EEDA  mov      rbx, qword ptr [rsp + 0x38]
0019EEDF  add      rsp, 0x20
0019EEE3  pop      rsi
0019EEE4  ret      
0019EEE5  mov      byte ptr [rcx + 0x128], 1
0019EEEC  mov      rbx, qword ptr [rsp + 0x38]
0019EEF1  add      rsp, 0x20
0019EEF5  pop      rsi
0019EEF6  ret      
```

## 001D6AA0 (53 B, extent 001D6AA0-001D6AD5)

Page context: "(+14 more) are called by bodies filed to Resource: '0019EAA0', '0019EE50', '001A0CF0', '001A0E50' (+25 more); '0018D160', '0019CB20', '001F5D70', '00597970' (+6 more) reach bodies filed to Resource: '001D6AA0', '0020B5F0', '002150D0', '002DF980' (+12 more) - shared machinery across the layer boundary, no shared ownership. - **UI - CLIENT (6 edges).** '0018CD90', '0018F8F0', '001EE8E0', '005FEFD0' (+2 more) are called by bodies filed to "

```
001D6AA0  mov      qword ptr [rsp + 8], rbx
001D6AA5  push     rdi
001D6AA6  sub      rsp, 0x20
001D6AAA  mov      rbx, rdx
001D6AAD  mov      edi, ecx
001D6AAF  call     0x20c700  ; -> 0020C700 fn
001D6AB4  mov      rcx, rax
001D6AB7  mov      r8, rbx
001D6ABA  mov      edx, edi
001D6ABC  call     0x20b9a0  ; -> 0020B9A0 fn
001D6AC1  mov      rbx, qword ptr [rsp + 0x30]
001D6AC6  xor      ecx, ecx
001D6AC8  test     al, al
001D6ACA  setne    cl
001D6ACD  mov      eax, ecx
001D6ACF  add      rsp, 0x20
001D6AD3  pop      rdi
001D6AD4  ret      
```

## 001F39B0 (38 B, extent 001F39B0-001F39D6)

Page context: "DA0'.   - **What gates this pass.** '0018FE00' is called earlier in the same frame step, '001F3090' ('001F3114'), gated only by     the global byte '01DFE0C4' (1 in the image; writers '001F2870' and '001F39B0'). With 'SMAA_1x' it therefore runs     **in addition to** SMAA, and with 'FXAA' it runs beside ~~a plain copy~~ **Phyre's FXAA worker ('CON-198')**.   - **What is left.** The pass may still be an FXAA-style filter, but the setting"

```
001F39B0  push     rbx
001F39B2  sub      rsp, 0x20
001F39B6  mov      rbx, rcx
001F39B9  call     0x193d50  ; -> 00193D50 fn
001F39BE  mov      edx, dword ptr [rbx + 0x18]
001F39C1  mov      rcx, rax
001F39C4  call     0x1f9a60  ; -> 001F9A60 fn
001F39C9  mov      byte ptr [rip + 0x1c0a6f4], 1  ; -> 01DFE0C4 [u8 0x01]
001F39D0  add      rsp, 0x20
001F39D4  pop      rbx
001F39D5  ret      
```

## 005CE850 (89 B, extent 005CE850-005CE8A9)

Page context: "    ('02E58CA0', '02E59BB8') unlinking 'this+0x10' — the same unlink-on-destroy shape as the       context-switch family's own destructor.     - **Two lookups through the engine's keyed container.** '005CE850' (89 B) and '005D6E00' (74 B)       both call '0063BC00' on the same global '02E58060' and then convert the returned node to its       element with 'add rax, -8' — the node-to-element '−8' idiom the class-descriptor and CRT-heap   "

```
005CE850  push     rbx
005CE852  sub      rsp, 0x20
005CE856  lea      rcx, [rip + 0x2889803]  ; -> 02E58060
005CE85D  mov      rbx, rdx
005CE860  call     0x63bc00  ; -> 0063BC00 fn
005CE865  test     rax, rax
005CE868  je       0x5ce8a1  ; -> 005CE8A1
005CE86A  add      rax, -8
005CE86E  je       0x5ce8a1  ; -> 005CE8A1
005CE870  test     rbx, rbx
005CE873  je       0x5ce899  ; -> 005CE899
005CE875  lea      rcx, [rip + 0x77b034]  ; -> 00D498B0
005CE87C  mov      qword ptr [rbx], rcx
005CE87F  xor      ecx, ecx
005CE881  mov      qword ptr [rbx + 8], rax
005CE885  lea      rax, [rip + 0x77b044]  ; -> 00D498D0
005CE88C  mov      qword ptr [rbx], rax
005CE88F  mov      dword ptr [rbx + 0x10], ecx
005CE892  mov      dword ptr [rbx + 0x18], ecx
005CE895  mov      qword ptr [rbx + 0x20], rcx
005CE899  mov      al, 1
005CE89B  add      rsp, 0x20
005CE89F  pop      rbx
005CE8A0  ret      
005CE8A1  xor      al, al
005CE8A3  add      rsp, 0x20
005CE8A7  pop      rbx
005CE8A8  ret      
```

## 005D6E00 (74 B, extent 005D6E00-005D6E4A)

Page context: "9BB8') unlinking 'this+0x10' — the same unlink-on-destroy shape as the       context-switch family's own destructor.     - **Two lookups through the engine's keyed container.** '005CE850' (89 B) and '005D6E00' (74 B)       both call '0063BC00' on the same global '02E58060' and then convert the returned node to its       element with 'add rax, -8' — the node-to-element '−8' idiom the class-descriptor and CRT-heap       containers use.   "

```
005D6E00  push     rbx
005D6E02  sub      rsp, 0x20
005D6E06  lea      rcx, [rip + 0x2881253]  ; -> 02E58060
005D6E0D  mov      rbx, rdx
005D6E10  call     0x63bc00  ; -> 0063BC00 fn
005D6E15  test     rax, rax
005D6E18  je       0x5d6e42  ; -> 005D6E42
005D6E1A  add      rax, -8
005D6E1E  je       0x5d6e42  ; -> 005D6E42
005D6E20  test     rbx, rbx
005D6E23  je       0x5d6e3a  ; -> 005D6E3A
005D6E25  lea      rcx, [rip + 0x772a84]  ; -> 00D498B0
005D6E2C  mov      qword ptr [rbx], rcx
005D6E2F  mov      qword ptr [rbx + 8], rax
005D6E33  mov      dword ptr [rbx + 0x10], 0
005D6E3A  mov      al, 1
005D6E3C  add      rsp, 0x20
005D6E40  pop      rbx
005D6E41  ret      
005D6E42  xor      al, al
005D6E44  add      rsp, 0x20
005D6E48  pop      rbx
005D6E49  ret      
```

## 005DBF60 (25 B, extent 005DBF60-005DBF79)

Page context: "elper and the seven vtable-slot members — 1,946 B, under 9 % of the 48 by weight —     are two small class families and their loops:     - **A two-class pair with its constructors and destructors.** '005DBF60' (25 B) installs the       vtable '00D498B0', takes one argument at '+0x08' and zeroes '+0x10'; '005DC0B0' (40 B) is the       derived form, installing '00D498B0' then '00D498D0' and zeroing out to '+0x20'. '005E2AA0'       (66 B) "

```
005DBF60  lea      rax, [rip + 0x76d949]  ; -> 00D498B0
005DBF67  mov      qword ptr [rcx], rax
005DBF6A  mov      rax, rcx
005DBF6D  mov      qword ptr [rcx + 8], rdx
005DBF71  mov      dword ptr [rcx + 0x10], 0
005DBF78  ret      
```

## 005DDD60 (79 B, extent 005DDD60-005DDDAF)

Page context: "ne byte-by-byte compare   ('r8 = r10 - rax', '[rax]' vs '[rax+r8]') and returns **'0x12'** on a duplicate; otherwise   'mov [r11+8],rbx; mov [02CBF998],r11' — a front push — and returns **'0'**. - **'005DDD60' UNREGISTER** (79 B) — 'rax = head', 'r8 = &02CBF998' so the head case needs no   special path, 'r9 = rcx+8'; compares *addresses* of next fields, then 'mov rcx,[rax+8];   mov [r8],rcx; mov [rax+8],0'.  **The sixty teardown wrapper"

```
005DDD60  mov      rax, qword ptr [rip + 0x26e1c31]  ; -> 02CBF998
005DDD67  lea      r8, [rip + 0x26e1c2a]  ; -> 02CBF998
005DDD6E  test     rax, rax
005DDD71  je       0x5dddae  ; -> 005DDDAE
005DDD73  lea      r9, [rcx + 8]
005DDD77  xor      r10d, r10d
005DDD7A  nop      word ptr [rax + rax]
005DDD80  test     rax, rax
005DDD83  lea      rcx, [rax + 8]
005DDD87  cmove    rcx, r10
005DDD8B  cmp      rcx, r9
005DDD8E  je       0x5ddd9e  ; -> 005DDD9E
005DDD90  lea      r8, [rax + 8]
005DDD94  mov      rax, qword ptr [rax + 8]
005DDD98  test     rax, rax
005DDD9B  jne      0x5ddd80  ; -> 005DDD80
005DDD9D  ret      
005DDD9E  test     rax, rax
005DDDA1  je       0x5dddae  ; -> 005DDDAE
005DDDA3  mov      rcx, qword ptr [rax + 8]
005DDDA7  mov      qword ptr [r8], rcx
005DDDAA  mov      qword ptr [rax + 8], r10
005DDDAE  ret      
```

## 0061CFA0 (130 B, extent 0061CFA0-0061D022)

Page context: "lass-descriptor and CRT-heap       containers use.     - **Array and count loops.** '00613770' (133 B) and '0061C250' (93 B) walk stride-'0x58' and       stride-'0x10' arrays under a guarded helper; '0061CFA0' (130 B) is a count loop over 'this+8';       '005DC2F0' (267 B) is an array constructor over 'eh_vector_constructor_iterator'; '0060E9C0'       (411 B) allocates, frees and rebuilds a container and returns 0.     - **The shared he"

```
0061CFA0  push     rbx
0061CFA2  sub      rsp, 0x20
0061CFA6  mov      ebx, edx
0061CFA8  lea      r8, [rcx + 8]
0061CFAC  test     edx, edx
0061CFAE  jne      0x61cfb8  ; -> 0061CFB8
0061CFB0  xor      eax, eax
0061CFB2  add      rsp, 0x20
0061CFB6  pop      rbx
0061CFB7  ret      
0061CFB8  cmp      ebx, 1
0061CFBB  jbe      0x61cfd1  ; -> 0061CFD1
0061CFBD  mov      rcx, rbx
0061CFC0  mov      edx, 8
0061CFC5  shl      rcx, 6
0061CFC9  call     0x17d260  ; -> 0017D260 fn
0061CFCE  mov      r8, rax
0061CFD1  test     r8, r8
0061CFD4  je       0x61d019  ; -> 0061D019
0061CFD6  test     ebx, ebx
0061CFD8  je       0x61d019  ; -> 0061D019
0061CFDA  lea      rcx, [r8 + 0x10]
0061CFDE  mov      rdx, rbx
0061CFE1  xor      r9d, r9d
0061CFE4  lea      r10, [rip + 0x73736d]  ; -> 00D54358
0061CFEB  nop      dword ptr [rax + rax]
0061CFF0  lea      rax, [rcx - 0x10]
0061CFF4  test     rax, rax
0061CFF7  je       0x61d00f  ; -> 0061D00F
0061CFF9  mov      qword ptr [rax], r9
0061CFFC  mov      qword ptr [rcx - 8], r9
0061D000  mov      qword ptr [rcx], r9
0061D003  mov      qword ptr [rcx + 8], r9
0061D007  mov      dword ptr [rcx + 0x10], r9d
0061D00B  mov      qword ptr [rcx + 0x18], r10
0061D00F  add      rcx, 0x40
0061D013  sub      rdx, 1
0061D017  jne      0x61cff0  ; -> 0061CFF0
0061D019  mov      rax, r8
0061D01C  add      rsp, 0x20
0061D020  pop      rbx
0061D021  ret      
```

## 00659A90 (391 B, extent 00659A90-00659C17)

Page context: "l 48. What it can still ask is which of them have been read     **instruction by instruction** rather than characterised — and that is 18 (the context-switch     family) plus '001B76E0', '00652940', '00659A90' and the four selector and predicate bodies. The     eleven workers were read as a population by their call structure, '001E2AF0' and the seventeen     above by shape and a partial decode. *A body identified from its shape is not a"

```
00659A90  mov      r11, rsp
00659A93  push     r14
00659A95  sub      rsp, 0x70
00659A99  mov      qword ptr [r11 - 0x48], 0xfffffffffffffffe
00659AA1  mov      qword ptr [r11 + 8], rbx
00659AA5  mov      qword ptr [r11 + 0x10], rsi
00659AA9  mov      qword ptr [r11 + 0x18], rdi
00659AAD  mov      rbx, r8
00659AB0  mov      rdi, rdx
00659AB3  mov      rsi, rcx
00659AB6  mov      rdx, qword ptr [rcx + 0x58]
00659ABA  lea      r14, [rip + 0x26dac57]  ; -> 02D34718
00659AC1  test     rdx, rdx
00659AC4  je       0x659aef  ; -> 00659AEF
00659AC6  mov      qword ptr [r11 - 0x40], 0x42
00659ACE  mov      qword ptr [r11 - 0x30], r9
00659AD2  mov      qword ptr [r11 - 0x38], r14
00659AD6  mov      rax, qword ptr [rcx + 0x10]
00659ADA  lea      r8, [r11 - 0x40]
00659ADE  mov      rcx, qword ptr [rax + 8]
00659AE2  call     0x1b81b0  ; -> 001B81B0 fn
00659AE7  test     eax, eax
00659AE9  jne      0x659c00  ; -> 00659C00
00659AEF  mov      rax, qword ptr [rsp + 0xa0]
00659AF7  test     rax, rax
00659AFA  je       0x659b32  ; -> 00659B32
00659AFC  mov      rdx, qword ptr [rsi + 0x60]
00659B00  test     rdx, rdx
00659B03  je       0x659b32  ; -> 00659B32
00659B05  mov      qword ptr [rsp + 0x38], 0x42
00659B0E  mov      qword ptr [rsp + 0x48], rax
00659B13  mov      qword ptr [rsp + 0x40], r14
00659B18  mov      rax, qword ptr [rsi + 0x10]
00659B1C  lea      r8, [rsp + 0x38]
00659B21  mov      rcx, qword ptr [rax + 8]
00659B25  call     0x1b81b0  ; -> 001B81B0 fn
00659B2A  test     eax, eax
00659B2C  jne      0x659c00  ; -> 00659C00
00659B32  xor      r8d, r8d
00659B35  mov      rdx, rbx
00659B38  lea      rcx, [rsp + 0x50]
00659B3D  call     0x5dc190  ; -> 005DC190 fn
00659B42  nop      
00659B43  test     rbx, rbx
00659B46  je       0x659b55  ; -> 00659B55
00659B48  mov      eax, dword ptr [rbx + 0xc]
00659B4B  shr      eax, 1
00659B4D  test     al, 1
00659B4F  je       0x659b55  ; -> 00659B55
00659B51  mov      cl, 1
00659B53  jmp      0x659b57  ; -> 00659B57
00659B55  xor      cl, cl
00659B57  lea      rdx, [rip + 0x26de4a2]  ; -> 02D38000
00659B5E  lea      rax, [rip + 0x26de47b]  ; -> 02D37FE0
00659B65  test     cl, cl
00659B67  cmovne   rax, rdx
00659B6B  mov      qword ptr [rdi + 0x80], rax
00659B72  xor      r8d, r8d
00659B75  lea      rdx, [rsp + 0x50]
00659B7A  mov      rcx, rdi
00659B7D  call     0x60d4f0  ; -> 0060D4F0 fn
00659B82  mov      ebx, eax
00659B84  test     eax, eax
00659B86  jne      0x659bf4  ; -> 00659BF4
00659B88  xor      edx, edx
00659B8A  mov      rcx, rdi
00659B8D  call     0x60db50  ; -> 0060DB50 fn
00659B92  mov      ebx, eax
00659B94  test     eax, eax
00659B96  jne      0x659bf4  ; -> 00659BF4
00659B98  xor      edx, edx
00659B9A  mov      rcx, rdi
00659B9D  call     0x5fefd0  ; -> 005FEFD0 fn
00659BA2  mov      ebx, eax
00659BA4  test     eax, eax
00659BA6  jne      0x659bf4  ; -> 00659BF4
00659BA8  lea      rax, [rip + 0x26d0e9]  ; -> 008C6C98
00659BAF  mov      qword ptr [rsp + 0x38], rax
00659BB4  lea      rax, [rsi + 0x30]
00659BB8  mov      qword ptr [rsp + 0x40], rax
00659BBD  mov      byte ptr [rsp + 0x28], bl
00659BC1  mov      eax, dword ptr [rdi + 0x220]
00659BC7  mov      dword ptr [rsp + 0x20], eax
00659BCB  xor      r9d, r9d
00659BCE  lea      r8, [rsp + 0x38]
00659BD3  mov      rdx, qword ptr [rip + 0x26dab36]  ; -> 02D34710
00659BDA  mov      rcx, rdi
00659BDD  call     0x60b980  ; -> 0060B980 fn
00659BE2  mov      ebx, eax
00659BE4  test     eax, eax
00659BE6  jne      0x659bf4  ; -> 00659BF4
00659BE8  xor      edx, edx
00659BEA  mov      rcx, rdi
00659BED  call     0x600a60  ; -> 00600A60 fn
00659BF2  mov      ebx, eax
00659BF4  lea      rcx, [rsp + 0x50]
00659BF9  call     0x16d6a0  ; -> 0016D6A0 fn
00659BFE  mov      eax, ebx
00659C00  lea      r11, [rsp + 0x70]
00659C05  mov      rbx, qword ptr [r11 + 0x10]
00659C09  mov      rsi, qword ptr [r11 + 0x18]
00659C0D  mov      rdi, qword ptr [r11 + 0x20]
00659C11  mov      rsp, r11
00659C14  pop      r14
00659C16  ret      
```
