# F-interior pack: `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md`

Generated 2026-10-02 18:33 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-map-screens-and-their-shared-map-data.json`.

Functions: 13. Each is cited on the page only at its entry and is still in the F frontier.

## 00254E70 (11 B, extent 00254E70-00254E7B)

Page context: ", in it, the map-data widget | '00253A30' (from 'ActorSystem_InitializeManagerRuntime', '0026D374'), '00251F40' (from '00254A90', which 'ActorManager_RunFieldRuntimePass' calls, and from '00255330', '00254E70', '00255020') | | '003CB410' | destroys the field-time container ('00245020', clears '02B47760') | '00253A30', '0028E790', '002BA040', '00281ED0' |  ### 2.5 The map-data widget and its family  The widget itself is documented with i"

```
00254E70  mov      ecx, dword ptr [rip + 0x1e3d972]  ; -> 020927E8
00254E76  jmp      0x251f40  ; -> 00251F40 fn
```

## 00255020 (20 B, extent 00255020-00255034)

Page context: " map-data widget | '00253A30' (from 'ActorSystem_InitializeManagerRuntime', '0026D374'), '00251F40' (from '00254A90', which 'ActorManager_RunFieldRuntimePass' calls, and from '00255330', '00254E70', '00255020') | | '003CB410' | destroys the field-time container ('00245020', clears '02B47760') | '00253A30', '0028E790', '002BA040', '00281ED0' |  ### 2.5 The map-data widget and its family  The widget itself is documented with its file form"

```
00255020  mov      ecx, dword ptr [rip + 0x1e3d7c2]  ; -> 020927E8
00255026  xor      ecx, 1
00255029  mov      dword ptr [rip + 0x1e3d7b9], ecx  ; -> 020927E8
0025502F  jmp      0x251f40  ; -> 00251F40 fn
```

## 0028E660 (33 B, extent 0028E660-0028E681)

Page context: "02B6249') | 'InputGameplay_ArbitrateDigitalInputAndModalState' '00253C70' ('00253DE2') | | '0028E630(x)' | location map '002B9D30(0, 6)', '002B9FE0(x)', then '002BA040' | '002804E0' ('002805C3') | | '0028E660(x)' | location map '002B9D30(x, 5)', '002BA020', '002BA000', then '002BA040' | the fullscreen procedure '0027F5D0' ('0027F6AF', '0027F9EC') | | '0028E690(req)' | 'req.u16[0]' 0 or 3: nothing ('0028E6AB'–'0028E6B8'); 1: location map"

```
0028E660  sub      rsp, 0x28
0028E664  mov      edx, 5
0028E669  call     0x2b9d30  ; -> 002B9D30 fn
0028E66E  call     0x2ba020  ; -> 002BA020 fn
0028E673  call     0x2ba000  ; -> 002BA000 fn
0028E678  add      rsp, 0x28
0028E67C  jmp      0x2ba040  ; -> 002BA040 fn
```

## 002B7540 (66 B, extent 002B7540-002B7582)

Page context: "            ([the widget contract](../Widget-Object-Model/CONTRACT-widget-object.md) §16). The release enters the              continuation the container's arm 1 stored at '+8' ('002BA6B0' location, '002B7540' track), which clears              the global ('0209E5F0' / '0209E5C0').           4. When the sibling object ('0209E5F8' / '0209E5C8') and the shared cursor singleton '02B62D78' are also gone,              the continuation copies "

```
002B7540  sub      rsp, 0x28
002B7544  cmp      qword ptr [rip + 0x1de707c], 0  ; -> 0209E5C8
002B754C  mov      qword ptr [rip + 0x1de7069], 0  ; -> 0209E5C0
002B7557  jne      0x2b757d  ; -> 002B757D
002B7559  call     0x402220  ; -> 00402220 fn
002B755E  test     rax, rax
002B7561  jne      0x2b757d  ; -> 002B757D
002B7563  lea      rcx, [rip + 0x1de7066]  ; -> 0209E5D0
002B756A  call     0x285f00  ; -> 00285F00 fn
002B756F  mov      ecx, 0x4ea
002B7574  add      rsp, 0x28
002B7578  jmp      0x2814e0  ; -> 002814E0 fn
002B757D  add      rsp, 0x28
002B7581  ret      
```

## 002BA240 (204 B, extent 002BA240-002BA30C)

Page context: "| | map-data widget | '0x278' | '02B457E0' | '003BC4E0' | — | '003BC450', called by '002BA040' ('002BA15C') and '003CB440' ('003CB4CC') |  All three containers also install the small child procedure '002BA240'. Its only three references are one 'lea' in each container procedure.  ### 2.3 The container class: two page slots and a flip  A container keeps two '0xBC10'-byte page slots at '+0x1B0' and '+0x1B0 + 0xBC10'. Bit 2 of the word at "

```
002BA240  sub      rsp, 0x48
002BA244  mov      rax, qword ptr [rip + 0x1c8a5e5]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002BA24B  xor      rax, rsp
002BA24E  mov      qword ptr [rsp + 0x38], rax
002BA253  mov      r8d, dword ptr [rdx]
002BA256  sub      r8d, 1
002BA25A  je       0x2ba2f8  ; -> 002BA2F8
002BA260  sub      r8d, 0xd
002BA264  je       0x2ba2d1  ; -> 002BA2D1
002BA266  sub      r8d, 2
002BA26A  je       0x2ba2b8  ; -> 002BA2B8
002BA26C  cmp      r8d, 2
002BA270  je       0x2ba289  ; -> 002BA289
002BA272  call     0x5c5230  ; -> 005C5230 fn
002BA277  mov      rcx, qword ptr [rsp + 0x38]
002BA27C  xor      rcx, rsp
002BA27F  call     0x808c40  ; -> 00808C40 fn
002BA284  add      rsp, 0x48
002BA288  ret      
002BA289  xorps    xmm0, xmm0
002BA28C  mov      dword ptr [rsp + 0x20], 0x20
002BA294  lea      rdx, [rsp + 0x20]
002BA299  movdqu   xmmword ptr [rsp + 0x28], xmm0
002BA29F  call     0x275440  ; -> 00275440 fn
002BA2A4  xor      eax, eax
002BA2A6  mov      rcx, qword ptr [rsp + 0x38]
002BA2AB  xor      rcx, rsp
002BA2AE  call     0x808c40  ; -> 00808C40 fn
002BA2B3  add      rsp, 0x48
002BA2B7  ret      
002BA2B8  call     0x245020  ; -> 00245020 fn
002BA2BD  xor      eax, eax
002BA2BF  mov      rcx, qword ptr [rsp + 0x38]
002BA2C4  xor      rcx, rsp
002BA2C7  call     0x808c40  ; -> 00808C40 fn
002BA2CC  add      rsp, 0x48
002BA2D0  ret      
002BA2D1  mov      qword ptr [rsp + 0x40], rbx
002BA2D6  call     0x249580  ; -> 00249580 fn
002BA2DB  mov      edx, 2
002BA2E0  mov      rcx, rax
002BA2E3  mov      rbx, rax
002BA2E6  call     0x3c2100  ; -> 003C2100 fn
002BA2EB  mov      rcx, rbx
002BA2EE  call     0x249410  ; -> 00249410 fn
002BA2F3  mov      rbx, qword ptr [rsp + 0x40]
002BA2F8  xor      eax, eax
002BA2FA  mov      rcx, qword ptr [rsp + 0x38]
002BA2FF  xor      rcx, rsp
002BA302  call     0x808c40  ; -> 00808C40 fn
002BA307  add      rsp, 0x48
002BA30B  ret      
```

## 002BA6B0 (66 B, extent 002BA6B0-002BA6F2)

Page context: "s the widget defers              ([the widget contract](../Widget-Object-Model/CONTRACT-widget-object.md) §16). The release enters the              continuation the container's arm 1 stored at '+8' ('002BA6B0' location, '002B7540' track), which clears              the global ('0209E5F0' / '0209E5C0').           4. When the sibling object ('0209E5F8' / '0209E5C8') and the shared cursor singleton '02B62D78' are also gone,              the"

```
002BA6B0  sub      rsp, 0x28
002BA6B4  cmp      qword ptr [rip + 0x1de3f3c], 0  ; -> 0209E5F8
002BA6BC  mov      qword ptr [rip + 0x1de3f29], 0  ; -> 0209E5F0
002BA6C7  jne      0x2ba6ed  ; -> 002BA6ED
002BA6C9  call     0x402220  ; -> 00402220 fn
002BA6CE  test     rax, rax
002BA6D1  jne      0x2ba6ed  ; -> 002BA6ED
002BA6D3  lea      rcx, [rip + 0x1de3f2e]  ; -> 0209E608
002BA6DA  call     0x285f00  ; -> 00285F00 fn
002BA6DF  mov      ecx, 0x417
002BA6E4  add      rsp, 0x28
002BA6E8  jmp      0x2814e0  ; -> 002814E0 fn
002BA6ED  add      rsp, 0x28
002BA6F1  ret      
```

## 0035F0F0 (22 B, extent 0035F0F0-0035F106)

Page context: "E0', '002D1870', '002D3900', '002D3A50', '002D3BA0' and '00368360' call the input layer's wrappers and mask tests ('001E0A10', '001E0E30', '001E0E50', '001E0F20', '00250130', '00250200', '002D66A0', '0035F0F0', '0035F110'), and the input body '00291D90' calls the image-slot release '0024A680'. The map pages read the pad through the input layer's manager singleton and mask tests, and the input arbiter is what opens the track map; most of"

```
0035F0F0  movsxd   rax, ecx
0035F0F3  imul     rcx, rax, 0x294
0035F0FA  lea      rax, [rip + 0x1f6bd93]  ; -> 022CAE94
0035F101  movzx    eax, byte ptr [rcx + rax]
0035F105  ret      
```

## 00368860 (62 B, extent 00368860-0036889E)

Page context: "nput dispatcher" is exact: it reads the '+0xE0'/'+0xE4' flag words, runs the '(flags & 0xF000) - 1' six-arm jump table at '02ED4310' ('00120000' + '0x1B4310'), each arm pairing '002D4A40'/'002D1870'/'00368860' with escalating 'edi' op codes, and carries the '+0x10B'/'+0x10C' repeat throttle against '0208F574', the '+0xE4' bit-13 commit, and helpers '002D0A20'/'002D1B10'/'002D1DB0'/'002D2D40'/'002D4330'/'002445C0'/ '0035F110'. Interior a"

```
00368860  add      ecx, 2
00368863  test     byte ptr [rip + 0x1f635c8], 0x10  ; -> 022CBE32
0036886A  je       0x36889d  ; -> 0036889D
0036886C  cmp      ecx, -1
0036886F  mov      word ptr [rip + 0x1f635c9], 0x406  ; -> 022CBE41
00368878  mov      eax, 2
0036887D  mov      byte ptr [rip + 0x1f635bf], 0x1e  ; -> 022CBE43
00368884  cmove    ecx, eax
00368887  mov      byte ptr [rip + 0x1f635af], 1  ; -> 022CBE3D
0036888E  xor      eax, eax
00368890  mov      byte ptr [rip + 0x1f635aa], cl  ; -> 022CBE40
00368896  mov      word ptr [rip + 0x1f635a1], ax  ; -> 022CBE3E
0036889D  ret      
```

## 00402BF0 (52 B, extent 00402BF0-00402C24)

Page context: " bit 3 is set ('002B74C3'..'002B74EB'), builds the page's entry list from the scratch through '00402D20(page +0xB140, scratch, n)' into '+0xBBC0', and, when the page's mode word '+0xBBE0' is 6, runs '00402BF0' over the list ('002B7508'..'002B7519'): the marker list for the page's map. '00402250(outX, outY, field, kind, arg5)' resolves the field's '+0x1C' word through the cached-record search '003BE2D0', passes the record to '003DFB50(re"

```
00402BF0  test     rcx, rcx
00402BF3  je       0x402c23  ; -> 00402C23
00402BF5  mov      eax, 0x80
00402BFA  mov      edx, 0xfff9
00402BFF  nop      
00402C00  cmp      byte ptr [rcx + 2], 1
00402C04  jne      0x402c1a  ; -> 00402C1A
00402C06  and      word ptr [rcx + 0x4e], dx
00402C0A  or       word ptr [rcx + 0x4e], 9
00402C0F  mov      dword ptr [rcx + 0x38], 0x3f800000
00402C16  mov      word ptr [rcx + 0x4c], ax
00402C1A  mov      rcx, qword ptr [rcx + 0x60]
00402C1E  test     rcx, rcx
00402C21  jne      0x402c00  ; -> 00402C00
00402C23  ret      
```

## 00510950 (30 B, extent 00510950-0051096E)

Page context: ", while the save screens reuse the same widget and resource-scope helpers and the save header reads the same map state.  **Script_VM_Native_Bridge — CLIENT (12 edges).** '00356160' calls '00203170'; '00510950' and '00510990' call '00247780'; '00357450' and '0050CDE0' call '00264F90', and '0033F310' and '00357450' call '003148F0'; '0033FD40' calls '002EFD20'; '0034E0B0' (the script query of the primary flag bank) calls '0032A8A0'; '0050D"

```
00510950  sub      rsp, 0x28
00510954  call     0x280120  ; -> 00280120 fn
00510959  test     eax, eax
0051095B  jne      0x510969  ; -> 00510969
0051095D  lea      ecx, [rax + 1]
00510960  add      rsp, 0x28
00510964  jmp      0x247780  ; -> 00247780 fn
00510969  add      rsp, 0x28
0051096D  ret      
```

## 00510990 (29 B, extent 00510990-005109AD)

Page context: "e screens reuse the same widget and resource-scope helpers and the save header reads the same map state.  **Script_VM_Native_Bridge — CLIENT (12 edges).** '00356160' calls '00203170'; '00510950' and '00510990' call '00247780'; '00357450' and '0050CDE0' call '00264F90', and '0033F310' and '00357450' call '003148F0'; '0033FD40' calls '002EFD20'; '0034E0B0' (the script query of the primary flag bank) calls '0032A8A0'; '0050D8F0' calls '003"

```
00510990  sub      rsp, 0x28
00510994  call     0x280120  ; -> 00280120 fn
00510999  test     eax, eax
0051099B  jne      0x5109a8  ; -> 005109A8
0051099D  xor      ecx, ecx
0051099F  add      rsp, 0x28
005109A3  jmp      0x247780  ; -> 00247780 fn
005109A8  add      rsp, 0x28
005109AC  ret      
```

## 00552230 (21 B, extent 00552230-00552245)

Page context: "552258' | | '005528C0' | 4521 | 28C0 | the page proc (0xA020, 42 ids to 17 arms) — installs the panes, ~~owns '02CA8F38'~~ reads '02CA8F38', which only the installer '00550400' ('00550400+0x55') and '00552230' ('00552230+0x5') write *(corrected 2026-10-02, OPUS)* | '005528DC' | | '00553AE0' | 202 | 3AE0 | MapName/RegionText pane (0x1C0, ids 1/4): id 1 sets '+0x98'=0 / '+0x9C'=0x7800438 + '00247570' name; id 4 draws via '002D8910'/'002D8"

```
00552230  mov      ecx, 0x418
00552235  mov      qword ptr [rip + 0x2756cf8], 0  ; -> 02CA8F38
00552240  jmp      0x2814e0  ; -> 002814E0 fn
```

## 0057FB00 (887 B, extent 0057FB00-0057FE77)

Page context: "77700', '00377750', '00377780', '00377BA0', '00377C20', '00377C70', '003C0450' and '00576A50'; '00264F90' and '00265270' by 'WorldTransition_StageFieldTransition' '003145E0', '003778B0', '003C0450', '0057FB00', '001EDCD0' and '003EAA70'; '002EFD20' by 'WorldTransition_RequestFieldTransition' '00314440'; the string lookup '0036A100' by '00267930', '003319D0' and 'AreaArd_LoadOrUnloadFieldResource' '003EA820'; and the members '001EC560', "

```
0057FB00  mov      qword ptr [rsp + 0x20], rbx
0057FB05  push     rbp
0057FB06  push     rsi
0057FB07  push     rdi
0057FB08  push     r12
0057FB0A  push     r13
0057FB0C  push     r14
0057FB0E  push     r15
0057FB10  sub      rsp, 0x60
0057FB14  mov      rax, qword ptr [rip + 0x19c4d15]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0057FB1B  xor      rax, rsp
0057FB1E  mov      qword ptr [rsp + 0x50], rax
0057FB23  or       r12d, 0xffffffff
0057FB27  mov      r15, r8
0057FB2A  test     byte ptr [r8 + 0x57], 1
0057FB2F  mov      r9, rdx
0057FB32  mov      rbx, rcx
0057FB35  lea      r14d, [r12 + 3]
0057FB3A  je       0x57fb94  ; -> 0057FB94
0057FB3C  mov      rcx, qword ptr [rcx + 8]
0057FB40  lea      r8, [rsp + 0x40]
0057FB45  mov      dword ptr [rsp + 0x30], 0x20002
0057FB4D  lea      rdx, [rsp + 0x30]
0057FB52  movzx    eax, word ptr [rcx + 8]
0057FB56  sub      ax, 4
0057FB5A  mov      word ptr [rsp + 0x34], ax
0057FB5F  movzx    eax, word ptr [rcx + 0xa]
0057FB63  mov      rcx, r9
0057FB66  sub      ax, 4
0057FB6A  mov      dword ptr [rsp + 0x4c], 0x4816224a
0057FB72  mov      word ptr [rsp + 0x36], ax
0057FB77  mov      dword ptr [rsp + 0x48], 0x4816224a
0057FB7F  mov      dword ptr [rsp + 0x44], 0x4816224a
0057FB87  mov      dword ptr [rsp + 0x40], 0x4816224a
0057FB8F  call     0x2dc290  ; -> 002DC290 fn
0057FB94  mov      edx, 1
0057FB99  mov      rcx, rbx
0057FB9C  call     0x393190  ; -> 00393190 fn
0057FBA1  mov      rax, qword ptr [rbx + 0x10]
0057FBA5  lea      r9, [rip + 0x7a4300]  ; -> 00D23EAC
0057FBAC  mov      rcx, qword ptr [rax + 0xd8]
0057FBB3  and      dword ptr [rcx + 8], 0xfffffffe
0057FBB7  mov      rax, qword ptr [rbx + 0x10]
0057FBBB  mov      rcx, qword ptr [rax + 0xb0]
0057FBC2  and      dword ptr [rcx + 8], 0xfffffffe
0057FBC6  xor      r13d, r13d
0057FBC9  mov      r8d, r13d
0057FBCC  nop      dword ptr [rax]
0057FBD0  movzx    ecx, byte ptr [r9]
0057FBD4  lea      r9, [r9 + 1]
0057FBD8  mov      rax, qword ptr [rbx + 0x10]
0057FBDC  inc      r8d
0057FBDF  mov      rdx, qword ptr [rax + rcx*8]
0057FBE3  or       dword ptr [rdx + 8], 1
0057FBE7  cmp      r8d, 7
0057FBEB  jb       0x57fbd0  ; -> 0057FBD0
0057FBED  mov      rax, qword ptr [rbx + 0x10]
0057FBF1  mov      rcx, qword ptr [rax + 0xd0]
0057FBF8  and      dword ptr [rcx + 8], 0xfffffffe
0057FBFC  test     byte ptr [r15 + 0x57], 4
0057FC01  je       0x57fc12  ; -> 0057FC12
0057FC03  mov      rax, qword ptr [rbx + 0x10]
0057FC07  mov      rcx, qword ptr [rax + 0xd8]
0057FC0E  or       dword ptr [rcx + 8], 1
0057FC12  test     byte ptr [r15 + 0x57], 1
0057FC17  mov      ecx, dword ptr [r15 + 0x4c]
0057FC1B  mov      esi, ecx
0057FC1D  je       0x57fce5  ; -> 0057FCE5
0057FC23  mov      eax, dword ptr [r15 + 0x80]
0057FC2A  test     eax, eax
0057FC2C  cmove    eax, ecx
0057FC2F  mov      dword ptr [rsp + 0x30], eax
0057FC33  call     0x377b60  ; -> 00377B60 fn
0057FC38  mov      rcx, qword ptr [rbx + 0x10]
0057FC3C  mov      rdi, qword ptr [rcx + 0xb8]
0057FC43  xor      ecx, ecx
0057FC45  mov      qword ptr [rdi + 0x18], rax
0057FC49  call     0x20e620  ; -> 0020E620 fn
0057FC4E  or       dword ptr [rdi + 8], 1
0057FC52  lea      r8, [rsp + 0x3c]
0057FC57  lea      rdx, [rsp + 0x38]
0057FC5C  mov      dword ptr [rdi + 0x20], eax
0057FC5F  mov      rcx, rdi
0057FC62  call     0x29fe20  ; -> 0029FE20 fn
0057FC67  mov      rax, qword ptr [rbx + 0x10]
0057FC6B  movsx    esi, word ptr [rdi + 0xc]
0057FC6F  movsx    ebp, word ptr [rdi + 0xe]
0057FC73  mov      rcx, qword ptr [rax + 0xc8]
0057FC7A  sub      si, word ptr [rcx + 0x10]
0057FC7E  or       dword ptr [rcx + 8], 1
0057FC82  mov      word ptr [rcx + 0xc], si
0057FC86  mov      ecx, dword ptr [r15 + 0x4c]
0057FC8A  call     0x3778b0  ; -> 003778B0 fn
0057FC8F  mov      rcx, qword ptr [rbx + 0x10]
0057FC93  mov      rdi, rax
0057FC96  mov      r14, qword ptr [rcx + 0xc0]
0057FC9D  mov      rcx, r14
0057FCA0  sub      si, word ptr [r14 + 0x10]
0057FCA5  mov      word ptr [r14 + 0xc], si
0057FCAA  mov      word ptr [r14 + 0xe], bp
0057FCAF  call     0x29fb50  ; -> 0029FB50 fn
0057FCB4  mov      rcx, qword ptr [r14]
0057FCB7  or       dword ptr [r14 + 8], 1
0057FCBC  movzx    edx, word ptr [rcx + 4]
0057FCC0  xor      ecx, ecx
0057FCC2  sub      dx, word ptr [rsp + 0x38]
0057FCC7  mov      word ptr [r14 + 0xc], dx
0057FCCC  mov      qword ptr [r14 + 0x18], rdi
0057FCD0  call     0x20e620  ; -> 0020E620 fn
0057FCD5  mov      esi, dword ptr [rsp + 0x30]
0057FCD9  mov      dword ptr [r14 + 0x20], eax
0057FCDD  mov      r14d, 2
0057FCE3  jmp      0x57fd12  ; -> 0057FD12
0057FCE5  mov      rax, qword ptr [rbx + 0x10]
0057FCE9  mov      rcx, qword ptr [rax + 0xc0]
0057FCF0  and      dword ptr [rcx + 8], 0xfffffffe
0057FCF4  mov      rax, qword ptr [rbx + 0x10]
0057FCF8  mov      rcx, qword ptr [rax + 0xc8]
0057FCFF  and      dword ptr [rcx + 8], 0xfffffffe
0057FD03  mov      rax, qword ptr [rbx + 0x10]
0057FD07  mov      rcx, qword ptr [rax + 0xb8]
0057FD0E  and      dword ptr [rcx + 8], 0xfffffffe
0057FD12  mov      ecx, esi
0057FD14  call     0x3778b0  ; -> 003778B0 fn
0057FD19  mov      rbp, rax
0057FD1C  call     0x264150  ; -> 00264150 fn
0057FD21  test     eax, eax
0057FD23  je       0x57fd69  ; -> 0057FD69
0057FD25  mov      ecx, esi
0057FD27  call     0x264f90  ; -> 00264F90 fn
0057FD2C  cmp      eax, 7
0057FD2F  je       0x57fd58  ; -> 0057FD58
0057FD31  cmp      eax, 0x16
0057FD34  je       0x57fd50  ; -> 0057FD50
0057FD36  cmp      eax, 0x19
0057FD39  je       0x57fd48  ; -> 0057FD48
0057FD3B  cmp      eax, 0x1d
0057FD3E  jne      0x57fd69  ; -> 0057FD69
0057FD40  mov      r12d, 0x7ed
0057FD46  jmp      0x57fd5e  ; -> 0057FD5E
0057FD48  mov      r12d, 0x7ee
0057FD4E  jmp      0x57fd5e  ; -> 0057FD5E
0057FD50  mov      r12d, 0x7eb
0057FD56  jmp      0x57fd5e  ; -> 0057FD5E
0057FD58  mov      r12d, 0x7ec
0057FD5E  mov      ecx, r12d
0057FD61  call     0x2f9860  ; -> 002F9860 fn
0057FD66  mov      rbp, rax
0057FD69  mov      rax, qword ptr [rbx + 0x10]
0057FD6D  xor      ecx, ecx
0057FD6F  mov      rdi, qword ptr [rax + 0x90]
0057FD76  mov      qword ptr [rdi + 0x18], rbp
0057FD7A  call     0x20e620  ; -> 0020E620 fn
0057FD7F  mov      dword ptr [rdi + 0x20], eax
0057FD82  mov      rax, qword ptr [rbx + 0x10]
0057FD86  mov      rcx, qword ptr [rax + 0xa0]
0057FD8D  and      dword ptr [rcx + 8], 0xfffffffe
0057FD91  mov      ecx, esi
0057FD93  call     0x377b60  ; -> 00377B60 fn
0057FD98  mov      rcx, qword ptr [rbx + 0x10]
0057FD9C  mov      rdi, qword ptr [rcx + 0x98]
0057FDA3  xor      ecx, ecx
0057FDA5  mov      qword ptr [rdi + 0x18], rax
0057FDA9  call     0x20e620  ; -> 0020E620 fn
0057FDAE  mov      dword ptr [rdi + 0x20], eax
0057FDB1  cmp      r12d, -1
0057FDB5  je       0x57fdbf  ; -> 0057FDBF
0057FDB7  mov      esi, r13d
0057FDBA  mov      edi, r13d
0057FDBD  jmp      0x57fdf9  ; -> 0057FDF9
0057FDBF  movzx    eax, word ptr [r15 + 0x18]
0057FDC4  mov      ecx, 0x3e8
0057FDC9  mov      edi, 0x3b
0057FDCE  cmp      ax, cx
0057FDD1  jb       0x57fddb  ; -> 0057FDDB
0057FDD3  lea      r13d, [rcx - 1]
0057FDD7  mov      esi, edi
0057FDD9  jmp      0x57fdf9  ; -> 0057FDF9
0057FDDB  movzx    r13d, ax
0057FDDF  movzx    eax, byte ptr [r15 + 0x1a]
0057FDE4  movzx    esi, al
0057FDE7  cmp      al, 0x3c
0057FDE9  jb       0x57fded  ; -> 0057FDED
0057FDEB  mov      esi, edi
0057FDED  movzx    eax, byte ptr [r15 + 0x1b]
0057FDF2  cmp      al, 0x3c
0057FDF4  jae      0x57fdf9  ; -> 0057FDF9
0057FDF6  movzx    edi, al
0057FDF9  mov      r9d, 3
0057FDFF  mov      dword ptr [rsp + 0x20], r13d
0057FE04  mov      r8d, r9d
0057FE07  mov      edx, 8
0057FE0C  mov      rcx, rbx
0057FE0F  call     0x393160  ; -> 00393160 fn
0057FE14  mov      rax, qword ptr [rbx + 0x10]
0057FE18  mov      r9d, 1
0057FE1E  mov      r8d, r14d
0057FE21  mov      dword ptr [rsp + 0x20], esi
0057FE25  mov      rcx, rbx
0057FE28  mov      rdx, qword ptr [rax + 0x38]
0057FE2C  and      dword ptr [rdx + 8], 0xfffffffe
0057FE30  lea      edx, [r9 + 0xa]
0057FE34  call     0x393160  ; -> 00393160 fn
0057FE39  mov      r9d, 1
0057FE3F  mov      dword ptr [rsp + 0x20], edi
0057FE43  mov      r8d, r14d
0057FE46  mov      rcx, rbx
0057FE49  lea      edx, [r9 + 0xc]
0057FE4D  call     0x393160  ; -> 00393160 fn
0057FE52  mov      rcx, qword ptr [rsp + 0x50]
0057FE57  xor      rcx, rsp
0057FE5A  call     0x808c40  ; -> 00808C40 fn
0057FE5F  mov      rbx, qword ptr [rsp + 0xb8]
0057FE67  add      rsp, 0x60
0057FE6B  pop      r15
0057FE6D  pop      r14
0057FE6F  pop      r13
0057FE71  pop      r12
0057FE73  pop      rdi
0057FE74  pop      rsi
0057FE75  pop      rbp
0057FE76  ret      
```
