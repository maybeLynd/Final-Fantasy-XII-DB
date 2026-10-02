# F-interior pack: `16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`

Generated 2026-10-02 18:33 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/dyngeo-instance-family.json`.

Functions: 6. Each is cited on the page only at its entry and is still in the F frontier.

## 001EE650 (362 B, extent 001EE650-001EE7BA)

Page context: "ery across the layer boundary, no shared ownership.  ## SWE2-EC7-34 update (2026-09-19) - '00215440'  '00215440' (845 B) is the dyngeo instance setup - cookie frame, '001EE7C0'/'002155D5'/'002154C2'/'001EE650' plus '00861EBA'. Interior anchor '00215483' (an '001EE7C0' call).  ## SWE2-EC7-38 update (2026-09-19) - '00213B40'  '00213B40' (460 B) is 'Final''s own slot-6 body the page names - '00900384'/'008C5B5C'/'008C5B48', '001B1620' pair"

```
001EE650  mov      qword ptr [rsp + 8], rbx
001EE655  mov      qword ptr [rsp + 0x10], rsi
001EE65A  mov      qword ptr [rsp + 0x18], rdi
001EE65F  mov      edx, ecx
001EE661  lea      rdi, [rip + 0x7140e8]  ; -> 00902750
001EE668  shr      edx, 2
001EE66B  mov      r11d, ecx
001EE66E  and      edx, 3
001EE671  and      r11d, 3
001EE675  mov      r9, rcx
001EE678  mov      esi, 0x10
001EE67D  lea      eax, [r11 + r11*2]
001EE681  add      edx, eax
001EE683  mov      eax, ecx
001EE685  shr      eax, 4
001EE688  and      eax, 3
001EE68B  lea      edx, [rdx + rdx*2]
001EE68E  add      edx, eax
001EE690  mov      eax, ecx
001EE692  mov      rcx, qword ptr [rsp + 0x28]
001EE697  shr      eax, 6
001EE69A  and      eax, 3
001EE69D  lea      ebx, [rdx + rdx*2]
001EE6A0  add      ebx, eax
001EE6A2  lea      rdx, [rcx + 4]
001EE6A6  mov      r10d, ebx
001EE6A9  add      r10, r10
001EE6AC  mov      eax, dword ptr [rdi + r10*8 + 4]
001EE6B1  mov      dword ptr [rcx + 8], eax
001EE6B4  mov      r8d, dword ptr [rdi + r10*8 + 8]
001EE6B9  mov      dword ptr [rcx], r8d
001EE6BC  mov      eax, dword ptr [rdi + r10*8 + 0xc]
001EE6C1  mov      dword ptr [rdx], eax
001EE6C3  cmp      r8d, 6
001EE6C7  jne      0x1ee6d1  ; -> 001EE6D1
001EE6C9  mov      dword ptr [rcx], 0x11
001EE6CF  jmp      0x1ee6f9  ; -> 001EE6F9
001EE6D1  cmp      r8d, 7
001EE6D5  jne      0x1ee6df  ; -> 001EE6DF
001EE6D7  mov      dword ptr [rcx], 0x12
001EE6DD  jmp      0x1ee6f9  ; -> 001EE6F9
001EE6DF  cmp      r8d, 2
001EE6E3  jne      0x1ee6ed  ; -> 001EE6ED
001EE6E5  mov      dword ptr [rcx], 0xf
001EE6EB  jmp      0x1ee6f9  ; -> 001EE6F9
001EE6ED  cmp      r8d, 3
001EE6F1  mov      eax, r8d
001EE6F4  cmove    eax, esi
001EE6F7  mov      dword ptr [rcx], eax
001EE6F9  mov      r8d, dword ptr [rdx]
001EE6FC  cmp      r8d, 6
001EE700  jne      0x1ee70a  ; -> 001EE70A
001EE702  mov      dword ptr [rdx], 0x11
001EE708  jmp      0x1ee732  ; -> 001EE732
001EE70A  cmp      r8d, 7
001EE70E  jne      0x1ee718  ; -> 001EE718
001EE710  mov      dword ptr [rdx], 0x12
001EE716  jmp      0x1ee732  ; -> 001EE732
001EE718  cmp      r8d, 2
001EE71C  jne      0x1ee726  ; -> 001EE726
001EE71E  mov      dword ptr [rdx], 0xf
001EE724  jmp      0x1ee732  ; -> 001EE732
001EE726  cmp      r8d, 3
001EE72A  mov      eax, r8d
001EE72D  cmove    eax, esi
001EE730  mov      dword ptr [rdx], eax
001EE732  cmp      dword ptr [rdi + r10*8], 1
001EE737  jne      0x1ee749  ; -> 001EE749
001EE739  test     r11d, r11d
001EE73C  mov      rax, rcx
001EE73F  cmovne   rax, rdx
001EE743  mov      dword ptr [rax], 1
001EE749  cmp      byte ptr [rsp + 0x30], 0
001EE74E  mov      eax, dword ptr [rdi + r10*8]
001EE752  mov      dword ptr [rcx + 0x1c], eax
001EE755  je       0x1ee767  ; -> 001EE767
001EE757  cmp      ebx, 0xa
001EE75A  mov      r8d, 5
001EE760  cmove    eax, r8d
001EE764  mov      dword ptr [rcx + 0x1c], eax
001EE767  mov      eax, dword ptr [rcx + 0x1c]
001EE76A  xor      r8d, r8d
001EE76D  sub      eax, 3
001EE770  test     eax, 0xfffffffd
001EE775  jne      0x1ee780  ; -> 001EE780
001EE777  mov      dword ptr [rcx], 1
001EE77D  mov      dword ptr [rdx], r8d
001EE780  mov      rbx, qword ptr [rsp + 8]
001EE785  mov      rsi, qword ptr [rsp + 0x10]
001EE78A  mov      rdi, qword ptr [rsp + 0x18]
001EE78F  shr      r9, 0x20
001EE793  movzx    eax, r9b
001EE797  mov      dword ptr [rcx + 0x18], r8d
001EE79B  movd     xmm0, eax
001EE79F  cvtdq2ps xmm0, xmm0
001EE7A2  divss    xmm0, dword ptr [rip + 0x6d7396]  ; -> 008C5B40 [f32 255]
001EE7AA  movss    dword ptr [rcx + 0xc], xmm0
001EE7AF  movss    dword ptr [rcx + 0x10], xmm0
001EE7B4  movss    dword ptr [rcx + 0x14], xmm0
001EE7B9  ret      
```

## 00214710 (144 B, extent 00214710-002147A0)

Page context: " - **Byte zero: draw in place.** The flush constructs the one 'Final' object ('0x170' bytes) and pushes no         render target. It copies its 4×4 matrix at '+0xE30' into the object through slot 3 ('00214710', which         fills '+0x11C'–'+0x158'). 'Final''s own slot 6 ('00213B40') then applies that matrix to every vertex on         the CPU, with a divide by w, before the GS-to-device mapping that the shared slot 6 ('00213D10') also d"

```
00214710  mov      eax, dword ptr [rdx]
00214712  mov      dword ptr [rcx + 0x11c], eax
00214718  mov      eax, dword ptr [rdx + 4]
0021471B  mov      dword ptr [rcx + 0x120], eax
00214721  mov      eax, dword ptr [rdx + 8]
00214724  mov      dword ptr [rcx + 0x124], eax
0021472A  mov      eax, dword ptr [rdx + 0xc]
0021472D  mov      dword ptr [rcx + 0x128], eax
00214733  mov      eax, dword ptr [rdx + 0x10]
00214736  mov      dword ptr [rcx + 0x12c], eax
0021473C  mov      eax, dword ptr [rdx + 0x14]
0021473F  mov      dword ptr [rcx + 0x130], eax
00214745  mov      eax, dword ptr [rdx + 0x18]
00214748  mov      dword ptr [rcx + 0x134], eax
0021474E  mov      eax, dword ptr [rdx + 0x1c]
00214751  mov      dword ptr [rcx + 0x138], eax
00214757  mov      eax, dword ptr [rdx + 0x20]
0021475A  mov      dword ptr [rcx + 0x13c], eax
00214760  mov      eax, dword ptr [rdx + 0x24]
00214763  mov      dword ptr [rcx + 0x140], eax
00214769  mov      eax, dword ptr [rdx + 0x28]
0021476C  mov      dword ptr [rcx + 0x144], eax
00214772  mov      eax, dword ptr [rdx + 0x2c]
00214775  mov      dword ptr [rcx + 0x148], eax
0021477B  mov      eax, dword ptr [rdx + 0x30]
0021477E  mov      dword ptr [rcx + 0x14c], eax
00214784  mov      eax, dword ptr [rdx + 0x34]
00214787  mov      dword ptr [rcx + 0x150], eax
0021478D  mov      eax, dword ptr [rdx + 0x38]
00214790  mov      dword ptr [rcx + 0x154], eax
00214796  mov      eax, dword ptr [rdx + 0x3c]
00214799  mov      dword ptr [rcx + 0x158], eax
0021479F  ret      
```

## 00215A30 (109 B, extent 00215A30-00215A9D)

Page context: "ss | slot | address | size | |---|---:|---|---:| | 'DynGeoTextureInstance' | 1, 5, 6, 19 | '001FB8E0', '001FBA50', '001FB990', '001FBB10' | 161/192/191/45 | | 'DynGeoUIInstance' | 5, 6 | '00215AA0', '00215A30' | 105/109 | | 'DynGeo3DInstance' | 5, 6 | '001FBBE0' (thunk), '001FBBB0' | 5/39 | | 'DynGeoFontTextInstance' | 1 | '00213140' | 644 |  ## 4. Data structures and formulas  **The pool's identity rows**, read out of the image rather "

```
00215A30  movsxd   rax, dword ptr [rcx + 0x1c0]
00215A37  mov      r11, rdx
00215A3A  mov      r8, qword ptr [rcx + 0x18]
00215A3E  mov      r10, rcx
00215A41  lea      r9, [rax + rax*2]
00215A45  mov      eax, dword ptr [rdx]
00215A47  add      r9, r9
00215A4A  mov      dword ptr [r8 + r9*8], eax
00215A4E  movsxd   rax, dword ptr [rcx + 0x1c0]
00215A55  mov      r8, qword ptr [rcx + 0x18]
00215A59  lea      r9, [rax + rax*2]
00215A5D  mov      eax, dword ptr [rdx + 4]
00215A60  add      r9, r9
00215A63  mov      dword ptr [r8 + r9*8 + 4], eax
00215A68  movsxd   rax, dword ptr [rcx + 0x1c0]
00215A6F  mov      rcx, qword ptr [rcx + 0x18]
00215A73  lea      rdx, [rax + rax*2]
00215A77  mov      eax, dword ptr [r11 + 8]
00215A7B  add      rdx, rdx
00215A7E  mov      dword ptr [rcx + rdx*8 + 8], eax
00215A82  movsxd   rax, dword ptr [r10 + 0x1c0]
00215A89  mov      rcx, qword ptr [r10 + 0x18]
00215A8D  lea      rdx, [rax + rax*2]
00215A91  mov      eax, dword ptr [r11 + 0xc]
00215A95  add      rdx, rdx
00215A98  mov      dword ptr [rcx + rdx*8 + 0xc], eax
00215A9C  ret      
```

## 006CA760 (41 B, extent 006CA760-006CA789)

Page context: "its that class's primary         vtable '00D86960' (the Gi page's leading candidate, §13b):          | slot | '00D86960' implementation | fits the call here |         |---|---|---|         | 0 / 1 | '006CA760' ~~begins a batch and~~ *returns the fixed staging area (682 vertices) and* publishes '+0xB8' *(corrected 2026-09-26 (FABLE, Claude Opus 5.5): batching is slot 4's job; the Gi page 'BG-6')*; '006CB5E0' returns '+0xB8' | the memcpy "

```
006CA760  mov      eax, dword ptr [rcx + 0x18860]
006CA766  imul     rdx, rax, 0x7fe0
006CA76D  lea      rax, [rcx + 0x10880]
006CA774  mov      dword ptr [rcx + 0x18860], 0
006CA77E  add      rax, rdx
006CA781  mov      qword ptr [rcx + 0xb8], rax
006CA788  ret      
```

## 006CAC30 (15 B, extent 006CAC30-006CAC3F)

Page context: " 'Final''s identity matrix |         | 8 | '006CAEB0' stores a texture and its sampler arguments | the layer texture bind |         | 15 | '006CAB80', below | the 'Shadow' constants |         | 35 | '006CAC30' stores 'dl' at '+0x851' and 'r8w' at '+0x852' | slot 11's boolean and mode |        - **Slot 15 '006CAB80(1, 6, 7, 6, 7, x)'** passes its first five arguments to '00627FF0' on the '+0x208' state         object. That function zeroe"

```
006CAC30  mov      byte ptr [rcx + 0x851], dl
006CAC36  mov      word ptr [rcx + 0x852], r8w
006CAC3E  ret      
```

## 006CAF40 (105 B, extent 006CAF40-006CAFA9)

Page context: "atching is slot 4's job; the Gi page 'BG-6')*; '006CB5E0' returns '+0xB8' | the memcpy destination |         | 4 | '006C8C50(type, buffer, count)' → '006DA5A0' | the draw with 2 or 3 |         | 6 | '006CAF40' copies 16 dwords to '+0x10' and sets dirty '+0x208F3' | 'Final''s identity matrix |         | 8 | '006CAEB0' stores a texture and its sampler arguments | the layer texture bind |         | 15 | '006CAB80', below | the 'Shadow' con"

```
006CAF40  mov      eax, dword ptr [rdx]
006CAF42  mov      dword ptr [rcx + 0x10], eax
006CAF45  mov      eax, dword ptr [rdx + 4]
006CAF48  mov      dword ptr [rcx + 0x14], eax
006CAF4B  mov      eax, dword ptr [rdx + 8]
006CAF4E  mov      dword ptr [rcx + 0x18], eax
006CAF51  mov      eax, dword ptr [rdx + 0xc]
006CAF54  mov      dword ptr [rcx + 0x1c], eax
006CAF57  mov      eax, dword ptr [rdx + 0x10]
006CAF5A  mov      dword ptr [rcx + 0x20], eax
006CAF5D  mov      eax, dword ptr [rdx + 0x14]
006CAF60  mov      dword ptr [rcx + 0x24], eax
006CAF63  mov      eax, dword ptr [rdx + 0x18]
006CAF66  mov      dword ptr [rcx + 0x28], eax
006CAF69  mov      eax, dword ptr [rdx + 0x1c]
006CAF6C  mov      dword ptr [rcx + 0x2c], eax
006CAF6F  mov      eax, dword ptr [rdx + 0x20]
006CAF72  mov      dword ptr [rcx + 0x30], eax
006CAF75  mov      eax, dword ptr [rdx + 0x24]
006CAF78  mov      dword ptr [rcx + 0x34], eax
006CAF7B  mov      eax, dword ptr [rdx + 0x28]
006CAF7E  mov      dword ptr [rcx + 0x38], eax
006CAF81  mov      eax, dword ptr [rdx + 0x2c]
006CAF84  mov      dword ptr [rcx + 0x3c], eax
006CAF87  mov      eax, dword ptr [rdx + 0x30]
006CAF8A  mov      dword ptr [rcx + 0x40], eax
006CAF8D  mov      eax, dword ptr [rdx + 0x34]
006CAF90  mov      dword ptr [rcx + 0x44], eax
006CAF93  mov      eax, dword ptr [rdx + 0x38]
006CAF96  mov      dword ptr [rcx + 0x48], eax
006CAF99  mov      eax, dword ptr [rdx + 0x3c]
006CAF9C  mov      dword ptr [rcx + 0x4c], eax
006CAF9F  xor      eax, eax
006CAFA1  mov      byte ptr [rcx + 0x208f3], 1
006CAFA8  ret      
```
