# F-interior pack: `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md`

Generated 2026-10-03 02:32 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-save-payload-field-map.json`.

Functions: 7. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: cd6bd7f58	SWE2-DATA consolidated publish: progress-report cluster (generation store, R3 semantics, DB_GOAL, me; d0fd168a2	SWE2-DATA: batch-5 review corrections (clamping page's .data vf00 cell restored, SD-190 gate on the ; inbox mentions: FABLE.md, SWE2-STRUCT.md). OPUS read these before packing.

## 00249080 (140 B, extent 00249080-0024910C)

Page context: " kinds to '003096F0(r14w, r15w)' or '0020E600' - the loadout's class-pair resolver.  Interior anchor '00309527' (function '00309480').  '0024AD00' (577 B) is the call-free accumulate '003C6420' (and '00249080'/'00249110') call: 'rdx''s 64-byte block publishes to '022D92E0'..'022D9310', 'rcx'/'r8'/'rax' land in '022D8F90'/'022D8FA0'/'022D8FB0', then the 'r9d'-counted loop runs 'shufps'/'mulps'/'mulss' over 'r8''s 0x10-stride rows - the p"

```
00249080  mov      qword ptr [rsp + 8], rbx
00249085  push     rdi
00249086  sub      rsp, 0x30
0024908A  movsxd   rbx, r9d
0024908D  mov      rdi, rcx
00249090  mov      r9d, ebx
00249093  call     0x24ad00  ; -> 0024AD00 fn
00249098  test     rbx, rbx
0024909B  jle      0x249101  ; -> 00249101
0024909D  movaps   xmmword ptr [rsp + 0x20], xmm6
002490A2  nop      dword ptr [rax]
002490A6  nop      word ptr [rax + rax]
002490B0  movd     xmm6, dword ptr [rip + 0x1bc3120]  ; -> 01E0C1D8 [u32 0x00000200]
002490B8  cvtdq2ps xmm6, xmm6
002490BB  call     0x183280  ; -> 00183280 fn
002490C0  mov      eax, dword ptr [rdi]
002490C2  lea      rdi, [rdi + 0x10]
002490C6  sub      eax, 0x8000
002490CB  sar      eax, 4
002490CE  divss    xmm6, xmm0
002490D2  cvttss2si ecx, xmm6
002490D6  sar      ecx, 1
002490D8  add      eax, ecx
002490DA  mov      ecx, dword ptr [rdi - 0xc]
002490DD  mov      dword ptr [rdi - 0x10], eax
002490E0  sub      ecx, 0x8000
002490E6  mov      eax, dword ptr [rip + 0x1bc30f0]  ; -> 01E0C1DC [u32 0x000001C0]
002490EC  sar      ecx, 4
002490EF  sar      eax, 1
002490F1  add      ecx, eax
002490F3  mov      dword ptr [rdi - 0xc], ecx
002490F6  sub      rbx, 1
002490FA  jne      0x2490b0  ; -> 002490B0
002490FC  movaps   xmm6, xmmword ptr [rsp + 0x20]
00249101  mov      rbx, qword ptr [rsp + 0x40]
00249106  add      rsp, 0x30
0024910A  pop      rdi
0024910B  ret      
```

## 00264870 (118 B, extent 00264870-002648E6)

Page context: " the '00264xxx' family's index root.  Interior anchor '00264B06' (function '00264AE0').  '00264920' (137 B) is the record packer '002648F0''s tail calls (the settings arm '003F9720' reaches it too): '00264870' looks the record up, '0037C860'/'0037C8F0' pick 'word[+8]'/'+6'/'+4', then five '0032A8A0' byte-stores fill 'rdi' ('+2', '+0', '+1', '+3') and 'word[+0xA]' lands at 'word[+4]' - the 6-byte payload assembler.  Interior anchor '0026"

```
00264870  push     rdi
00264872  sub      rsp, 0x20
00264876  test     byte ptr [rip + 0x1e345a3], 1  ; -> 02098E20
0026487D  movsxd   rdi, ecx
00264880  je       0x2648de  ; -> 002648DE
00264882  mov      qword ptr [rsp + 0x30], rbx
00264887  mov      rbx, qword ptr [rip + 0x1e34582]  ; -> 02098E10
0026488E  test     rbx, rbx
00264891  je       0x2648d1  ; -> 002648D1
00264893  mov      ecx, dword ptr [rbx + 0x8c]
00264899  call     0x20e600  ; -> 0020E600 fn
0026489E  test     rax, rax
002648A1  je       0x2648d1  ; -> 002648D1
002648A3  mov      ecx, dword ptr [rbx + 0x8c]
002648A9  call     0x20e600  ; -> 0020E600 fn
002648AE  movsxd   rcx, eax
002648B1  add      rcx, rbx
002648B4  cmp      edi, dword ptr [rcx]
002648B6  jge      0x2648d1  ; -> 002648D1
002648B8  mov      rbx, qword ptr [rsp + 0x30]
002648BD  mov      rax, rdi
002648C0  shl      rax, 4
002648C4  add      rax, 4
002648C8  add      rax, rcx
002648CB  add      rsp, 0x20
002648CF  pop      rdi
002648D0  ret      
002648D1  xor      eax, eax
002648D3  mov      rbx, qword ptr [rsp + 0x30]
002648D8  add      rsp, 0x20
002648DC  pop      rdi
002648DD  ret      
002648DE  xor      eax, eax
002648E0  add      rsp, 0x20
002648E4  pop      rdi
002648E5  ret      
```

## 0026ABA0 (38 B, extent 0026ABA0-0026ABC6)

Page context: "e global '02098E58' — at '0026CAF8'–'0026CAFD'; reached only through that pointer by three accessors bounded at '0x100' with a 2-byte stride and gated by '02098E20' bit 0: '00264640' (get, 'movzx'), '0026ABA0' (set), '0026B730' (element 0); the reader 'AiTargetSelector_ResolveOperandValue' ('00321190') sign-extends the element ('003211EC'). What the 256 entries mean is not established (OPUS: a stride-4 scan of the region finds nothing e"

```
0026ABA0  cmp      ecx, 0x100
0026ABA6  jge      0x26abc5  ; -> 0026ABC5
0026ABA8  test     byte ptr [rip + 0x1e2e271], 1  ; -> 02098E20
0026ABAF  je       0x26abc5  ; -> 0026ABC5
0026ABB1  mov      r8, qword ptr [rip + 0x1e2e2a0]  ; -> 02098E58
0026ABB8  test     r8, r8
0026ABBB  je       0x26abc5  ; -> 0026ABC5
0026ABBD  movsxd   rax, ecx
0026ABC0  mov      word ptr [r8 + rax*2], dx
0026ABC5  ret      
```

## 002E13C0 (102 B, extent 002E13C0-002E1426)

Page context: "8 gives 4; 6, 7 and every value above 8 (unsigned compare) return 0 without the call | '00264A43', '00264A4F', '00264A61', '00264A7C', '00264A8B' | | '002E23E0' | 27 B | copies 'edx' to 'r9d', calls '002E13C0' with the incoming registers, then tail-jumps to '00254E00' with that result as 'ecx' and the low byte of 'r9' ('movzx edx, r9b' after the call) as 'edx' | '002E23E4', '002E23E7', '002E23EE', '002E23F6' | | '00344D30' | 65 B | keep"

```
002E13C0  mov      edx, 0x1d
002E13C5  cmp      ecx, 9
002E13C8  ja       0x2e1423  ; -> 002E1423
002E13CA  movsxd   rax, ecx
002E13CD  lea      r8, [rip - 0x1c13d4]  ; -> 00120000 (image base)
002E13D4  mov      ecx, dword ptr [r8 + rax*4 + 0x1c1428]  ; image base + 0x1c1428 = 002E1428
002E13DC  add      rcx, r8
002E13DF  jmp      rcx
002E13E1  xor      edx, edx
002E13E3  mov      eax, edx
002E13E5  ret      
002E13E6  mov      edx, 1
002E13EB  mov      eax, edx
002E13ED  ret      
002E13EE  mov      edx, 9
002E13F3  mov      eax, edx
002E13F5  ret      
002E13F6  mov      edx, 0x12
002E13FB  mov      eax, edx
002E13FD  ret      
002E13FE  mov      edx, 0x13
002E1403  mov      eax, edx
002E1405  ret      
002E1406  mov      edx, 0x14
002E140B  mov      eax, edx
002E140D  ret      
002E140E  mov      edx, 0x15
002E1413  mov      eax, edx
002E1415  ret      
002E1416  mov      edx, 0x16
002E141B  mov      eax, edx
002E141D  ret      
002E141E  mov      edx, 0x1e
002E1423  mov      eax, edx
002E1425  ret      
```

## 003F6FD0 (41 B, extent 003F6FD0-003F6FF9)

Page context: "-call '0209BE80'-manager battery — '003F8EA0', '003F8A90', '004FE3C0', tail '0028A080' | ['0028FA87'](../../_index/ADDRESS-INDEX.md) | | '002908C0' (117 B) | mode-3 conditional — '0209BE80' manager, '003F6FD0' fires only when '[rbx+0x2F0] == 3' ('00290909') | ['00290909'](../../_index/ADDRESS-INDEX.md) | | '00290BE0' (29 B) | conditional inner refresh — '0209BE80' nonnull and '[+0x10F10]' nonnull → '003F5030' ('00290BF6') | ['00290BEC']"

```
003F6FD0  movzx    eax, word ptr [rcx + 0x2f0]
003F6FD7  mov      edx, 0xfffb
003F6FDC  test     dx, ax
003F6FDF  je       0x3f6ff8  ; -> 003F6FF8
003F6FE1  cmp      ax, 1
003F6FE5  mov      eax, 4
003F6FEA  je       0x3f6ff1  ; -> 003F6FF1
003F6FEC  mov      eax, 3
003F6FF1  mov      word ptr [rcx + 0x2f0], ax
003F6FF8  ret      
```

## 00473B90 (29 B, extent 00473B90-00473BAD)

Page context: "600' share the fan-in — the interface layer consults this page's functions, not a shared responsibility.  **Script_VM_Native_Bridge — CLIENT (SWE2-EC7-157, 113 edges).** Batch-122's '0037E8D0' names '00473B90'/'002F9920'/'0037EF70'/'0037EFC0', and the map's helpers ('00236740'/'00236760'/'00203170') are reached by '0050F3F0'/'0050F540'/'00356160' on that layer — shared fan-in, no second owner. - **PlatformOnlineAchievements - CLIENT and"

```
00473B90  mov      rdx, qword ptr [rip + 0x28330c9]  ; -> 02CA6C60
00473B97  cmp      dword ptr [rdx + 4], ecx
00473B9A  jle      0x473ba9  ; -> 00473BA9
00473B9C  movsxd   rax, ecx
00473B9F  mov      eax, dword ptr [rdx + rax*4 + 8]
00473BA3  and      eax, 0x1fff
00473BA8  ret      
00473BA9  or       eax, 0xffffffff
00473BAC  ret      
```

## 00862930 (71 B, extent 00862930-00862977)

Page context: "n '003C81B0').  '003C29A0' (1208 B) is the fetch-and-format helper '003C4070' runs: '[rdx]' nonzero gates, '0035D320' x3 fetches, '003588B0' x2, '00272DE0', '0035D3D0', '00265020' x2, '00202B70' x2, '00862930', '00265200' x2, '002D8D10' x2 and '00861F0E' - the save/map draw's preparation body.  Interior anchor '003C29D7' (function '003C29A0').  '00403640' (809 B) is the map reader '00403970' calls: '00808F10', '00404230', '00861F0E' x2,"

```
00862930  movss    xmm0, dword ptr [rdx]
00862934  movss    xmm2, dword ptr [rip + 0x1489348]  ; -> 01CEBC84 [f32 16]
0086293C  mulss    xmm0, xmm2
00862940  cvttss2si eax, xmm0
00862944  mov      dword ptr [rcx], eax
00862946  movss    xmm0, dword ptr [rdx + 4]
0086294B  mulss    xmm0, xmm2
0086294F  cvttss2si eax, xmm0
00862953  mov      dword ptr [rcx + 4], eax
00862956  movss    xmm1, dword ptr [rdx + 8]
0086295B  mulss    xmm1, xmm2
0086295F  cvttss2si eax, xmm1
00862963  mov      dword ptr [rcx + 8], eax
00862966  movss    xmm0, dword ptr [rdx + 0xc]
0086296B  mulss    xmm0, xmm2
0086296F  cvttss2si eax, xmm0
00862973  mov      dword ptr [rcx + 0xc], eax
00862976  ret      
```
