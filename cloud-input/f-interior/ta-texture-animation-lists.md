# F-interior pack: `02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/ta-texture-animation-lists.json`.

Functions: 17. Each is cited on the page only at its entry and is still in the F frontier.

## 00180830 (60 B, extent 00180830-0018086C)

Page context: "180650' (108 B — '001A9930' ×2 + '001A94C0'/'001E3E80'/'001E3FF0'/'001A4FE0', '[rax+8]' virtual), '00180730' ('001A9930' + '001A9B70'), '001807F0' ('001A9930' + '001E62E0' — the entry 'TA-1' names), '00180830', '00180900' ('001AA240'), '001809A0' ('0018CA40' ×2), '001806C0' ('00189120'), '001803F0' ('001E4B00'), '001A4FE0' ('001AB570'), '001A94C0' ('001A2E50'), '001A9B70' ('001E5790'), '001AA240' ('001E69A0') | the '001A9930' resolve + "

```
00180830  mov      qword ptr [rsp + 8], rbx
00180835  mov      qword ptr [rsp + 0x10], rsi
0018083A  push     rdi
0018083B  sub      rsp, 0x20
0018083F  mov      ebx, r8d
00180842  mov      edi, edx
00180844  mov      rsi, rcx
00180847  call     0x1a9930  ; -> 001A9930 fn
0018084C  mov      rcx, rax
0018084F  mov      r9d, ebx
00180852  mov      r8d, edi
00180855  mov      rdx, rsi
00180858  mov      rbx, qword ptr [rsp + 0x30]
0018085D  mov      rsi, qword ptr [rsp + 0x38]
00180862  add      rsp, 0x20
00180866  pop      rdi
00180867  jmp      0x1a9dd0  ; -> 001A9DD0 fn
```

## 00180900 (115 B, extent 00180900-00180973)

Page context: " B — '001A9930' ×2 + '001A94C0'/'001E3E80'/'001E3FF0'/'001A4FE0', '[rax+8]' virtual), '00180730' ('001A9930' + '001A9B70'), '001807F0' ('001A9930' + '001E62E0' — the entry 'TA-1' names), '00180830', '00180900' ('001AA240'), '001809A0' ('0018CA40' ×2), '001806C0' ('00189120'), '001803F0' ('001E4B00'), '001A4FE0' ('001AB570'), '001A94C0' ('001A2E50'), '001A9B70' ('001E5790'), '001AA240' ('001E69A0') | the '001A9930' resolve + '001Exxxx' f"

```
00180900  mov      qword ptr [rsp + 8], rbx
00180905  mov      qword ptr [rsp + 0x10], rbp
0018090A  mov      qword ptr [rsp + 0x18], rsi
0018090F  push     rdi
00180910  sub      rsp, 0x40
00180914  mov      ebx, r9d
00180917  movzx    edi, r8b
0018091B  movzx    esi, dl
0018091E  mov      rbp, rcx
00180921  call     0x1a9930  ; -> 001A9930 fn
00180926  movss    xmm0, dword ptr [rsp + 0x70]
0018092C  mov      rcx, rax
0018092F  movzx    eax, byte ptr [rsp + 0x80]
00180937  movzx    r9d, dil
0018093B  mov      byte ptr [rsp + 0x38], al
0018093F  movzx    r8d, sil
00180943  movzx    eax, byte ptr [rsp + 0x78]
00180948  mov      rdx, rbp
0018094B  mov      byte ptr [rsp + 0x30], al
0018094F  movss    dword ptr [rsp + 0x28], xmm0
00180955  mov      dword ptr [rsp + 0x20], ebx
00180959  call     0x1aa240  ; -> 001AA240 fn
0018095E  mov      rbx, qword ptr [rsp + 0x50]
00180963  mov      rbp, qword ptr [rsp + 0x58]
00180968  mov      rsi, qword ptr [rsp + 0x60]
0018096D  add      rsp, 0x40
00180971  pop      rdi
00180972  ret      
```

## 001809A0 (52 B, extent 001809A0-001809D4)

Page context: "A94C0'/'001E3E80'/'001E3FF0'/'001A4FE0', '[rax+8]' virtual), '00180730' ('001A9930' + '001A9B70'), '001807F0' ('001A9930' + '001E62E0' — the entry 'TA-1' names), '00180830', '00180900' ('001AA240'), '001809A0' ('0018CA40' ×2), '001806C0' ('00189120'), '001803F0' ('001E4B00'), '001A4FE0' ('001AB570'), '001A94C0' ('001A2E50'), '001A9B70' ('001E5790'), '001AA240' ('001E69A0') | the '001A9930' resolve + '001Exxxx' fetch chain the pass walks"

```
001809A0  sub      rsp, 0x28
001809A4  cmp      byte ptr [rip + 0x1dfeb62], 0  ; -> 01F7F50D
001809AB  jne      0x1809cf  ; -> 001809CF
001809AD  call     0x18ca40  ; -> 0018CA40 fn
001809B2  test     rax, rax
001809B5  je       0x1809cf  ; -> 001809CF
001809B7  mov      byte ptr [rip + 0x1dfeb4f], 1  ; -> 01F7F50D
001809BE  call     0x18ca40  ; -> 0018CA40 fn
001809C3  mov      rcx, rax
001809C6  add      rsp, 0x28
001809CA  jmp      0x18c3c0  ; -> 0018C3C0 fn
001809CF  add      rsp, 0x28
001809D3  ret      
```

## 001A1920 (98 B, extent 001A1920-001A1982)

Page context: "lel list walks — same machinery instantiated for two record types | | container iterators | '001A3220', '001A3380', '001A34F0', '001A4390' (161–358 B, '0016D840'/'0016D720' + '[rax+0x10]' indirect), '001A1920', '001A20A0' ('02CBBD00'), '001A4D20', '001A5150', '001A6F10', '001A7850' | string/refcount helpers ('0016Dxxx') wrapped around container-vtable calls | | master populate | '001A7F10' (3,194 B — '001A2F70' ×12, 26 rip-indirect call"

```
001A1920  push     rbx
001A1922  sub      rsp, 0x30
001A1926  cmp      byte ptr [r8], 0
001A192A  mov      rax, r8
001A192D  mov      r9, rdx
001A1930  mov      dword ptr [rsp + 0x20], 0
001A1938  mov      rbx, rcx
001A193B  jne      0x1a1942  ; -> 001A1942
001A193D  xor      r8d, r8d
001A1940  jmp      0x1a1950  ; -> 001A1950
001A1942  or       r8, 0xffffffffffffffff
001A1946  inc      r8
001A1949  cmp      byte ptr [rax + r8], 0
001A194E  jne      0x1a1946  ; -> 001A1946
001A1950  mov      rdx, rax
001A1953  mov      rcx, r9
001A1956  call     0x1a5150  ; -> 001A5150 fn
001A195B  mov      qword ptr [rbx + 0x18], 0xf
001A1963  mov      rdx, rax
001A1966  mov      qword ptr [rbx + 0x10], 0
001A196E  mov      rcx, rbx
001A1971  mov      byte ptr [rbx], 0
001A1974  call     0x1a4c90  ; -> 001A4C90 fn
001A1979  mov      rax, rbx
001A197C  add      rsp, 0x30
001A1980  pop      rbx
001A1981  ret      
```

## 001A4FE0 (70 B, extent 001A4FE0-001A5026)

Page context: "4, 'TA-1'). All signature-swept 2026-09-15 ('bshape.py'):  | cluster | members | role | |---|---|---| | resource-handle helpers | '00180650' (108 B — '001A9930' ×2 + '001A94C0'/'001E3E80'/'001E3FF0'/'001A4FE0', '[rax+8]' virtual), '00180730' ('001A9930' + '001A9B70'), '001807F0' ('001A9930' + '001E62E0' — the entry 'TA-1' names), '00180830', '00180900' ('001AA240'), '001809A0' ('0018CA40' ×2), '001806C0' ('00189120'), '001803F0' ('001E4"

```
001A4FE0  test     rdx, rdx
001A4FE3  je       0x1a5025  ; -> 001A5025
001A4FE5  mov      qword ptr [rsp + 0x10], rdx
001A4FEA  sub      rsp, 0x28
001A4FEE  add      rcx, 0x90
001A4FF5  mov      r8, rdx
001A4FF8  mov      rdx, qword ptr [rcx + 8]
001A4FFC  cmp      rdx, qword ptr [rcx + 0x10]
001A5000  jae      0x1a5017  ; -> 001A5017
001A5002  lea      rax, [rdx + 8]
001A5006  mov      qword ptr [rcx + 8], rax
001A500A  test     rdx, rdx
001A500D  je       0x1a5021  ; -> 001A5021
001A500F  mov      qword ptr [rdx], r8
001A5012  add      rsp, 0x28
001A5016  ret      
001A5017  lea      r8, [rsp + 0x38]
001A501C  call     0x1ab570  ; -> 001AB570 fn
001A5021  add      rsp, 0x28
001A5025  ret      
```

## 001A7460 (52 B, extent 001A7460-001A7494)

Page context: ", 'glf0100_ya_tento04' ("tent"), 'var0100_m_hansya01_' ("reflection"). Each '.ta' file names one such texture and its frames. Without a map's '.ta', the renderer finds no frame set for that texture ('001A7460' returns null) and nothing swaps it; the base picture still draws.  ## 2. The layout  The file is text: **entries separated by CRLF**, each a logical asset path.  ''' /GameData/D3D11/ArtData/map/glf01/glf0102/tex/glf0100_ya_tento04"

```
001A7460  movzx    eax, byte ptr [rcx + 0x140]
001A7467  test     al, al
001A7469  je       0x1a7491  ; -> 001A7491
001A746B  mov      rax, qword ptr [rcx + 0x120]
001A7472  mov      r8, qword ptr [rcx + 0x128]
001A7479  cmp      rax, r8
001A747C  je       0x1a7491  ; -> 001A7491
001A747E  nop      
001A7480  mov      rcx, qword ptr [rax]
001A7483  cmp      qword ptr [rcx], rdx
001A7486  je       0x1a7493  ; -> 001A7493
001A7488  add      rax, 0x20
001A748C  cmp      rax, r8
001A748F  jne      0x1a7480  ; -> 001A7480
001A7491  xor      eax, eax
001A7493  ret      
```

## 001A9DD0 (64 B, extent 001A9DD0-001A9E10)

Page context: "7A70'/'00467A90' ('02CA5FF4'/'F8'), '00467B60' (71 B — rip-indirect + '008C2BD8'/'00901988'/'00D12518'/'01CEBD80'/'02AED570'), '00468070' | the draw-side emit the pass feeds | | leaves | '00180870', '001A9DD0', '001E3E80', '001E3FF0', '001E4B00' | five 7–17 B thunks |  'TA-1''s answer lives here in embryo: '001E5790' is the clock source ('01CEBDA0' — the same global the fps exceptions read) and '001E62E0' owns '001A7460'. What selects t"

```
001A9DD0  sub      r9d, 1
001A9DD4  je       0x1a9e04  ; -> 001A9E04
001A9DD6  sub      r9d, 1
001A9DDA  je       0x1a9df8  ; -> 001A9DF8
001A9DDC  cmp      r9d, 1
001A9DE0  je       0x1a9dec  ; -> 001A9DEC
001A9DE2  xor      eax, eax
001A9DE4  mov      qword ptr [rdx + 0xd0], rax
001A9DEB  ret      
001A9DEC  mov      qword ptr [rdx + 0xd0], 1
001A9DF7  ret      
001A9DF8  mov      qword ptr [rdx + 0xd0], 2
001A9E03  ret      
001A9E04  mov      qword ptr [rdx + 0xd0], 3
001A9E0F  ret      
```

## 001AA240 (120 B, extent 001AA240-001AA2B8)

Page context: "30' ×2 + '001A94C0'/'001E3E80'/'001E3FF0'/'001A4FE0', '[rax+8]' virtual), '00180730' ('001A9930' + '001A9B70'), '001807F0' ('001A9930' + '001E62E0' — the entry 'TA-1' names), '00180830', '00180900' ('001AA240'), '001809A0' ('0018CA40' ×2), '001806C0' ('00189120'), '001803F0' ('001E4B00'), '001A4FE0' ('001AB570'), '001A94C0' ('001A2E50'), '001A9B70' ('001E5790'), '001AA240' ('001E69A0') | the '001A9930' resolve + '001Exxxx' fetch chain t"

```
001AA240  push     rbx
001AA242  sub      rsp, 0x40
001AA246  mov      ecx, dword ptr [rsp + 0x70]
001AA24A  movzx    r10d, r9b
001AA24E  movzx    r11d, r8b
001AA252  mov      rbx, rdx
001AA255  test     ecx, ecx
001AA257  je       0x1aa27b  ; -> 001AA27B
001AA259  sub      ecx, 2
001AA25C  je       0x1aa273  ; -> 001AA273
001AA25E  cmp      ecx, 1
001AA261  je       0x1aa26b  ; -> 001AA26B
001AA263  mov      r9d, 1
001AA269  jmp      0x1aa27e  ; -> 001AA27E
001AA26B  mov      r9d, 3
001AA271  jmp      0x1aa27e  ; -> 001AA27E
001AA273  mov      r9d, 2
001AA279  jmp      0x1aa27e  ; -> 001AA27E
001AA27B  xor      r9d, r9d
001AA27E  movzx    eax, byte ptr [rsp + 0x88]
001AA286  movzx    r8d, r10b
001AA28A  movss    xmm0, dword ptr [rsp + 0x78]
001AA290  movzx    edx, r11b
001AA294  mov      byte ptr [rsp + 0x30], al
001AA298  mov      rcx, rbx
001AA29B  movzx    eax, byte ptr [rsp + 0x80]
001AA2A3  mov      byte ptr [rsp + 0x28], al
001AA2A7  movss    dword ptr [rsp + 0x20], xmm0
001AA2AD  call     0x1e69a0  ; -> 001E69A0 fn
001AA2B2  add      rsp, 0x40
001AA2B6  pop      rbx
001AA2B7  ret      
```

## 001AA4F0 (125 B, extent 001AA4F0-001AA56D)

Page context: "ter '[rcx]' advance to 'rdx' bound. Interior anchor '001A7665' (the '[rax+0x78]' chain advance).    ## SWE2-EC7-63 update (2026-09-19) - '001AB8A0'  '001AB8A0' (488 B) is a TA-list body - '0019D8D0'/'001AA4F0'/'001AA630'/'001AAF80'/'001AB350' plus two vcalls. Interior anchor '001AB906' (a '0019D8D0' call).    ## SWE2-EC7-63 update (2026-09-19) - '001E1490'  '001E1490' (144 B) is a call-free '0x80'-stride 'movups' record copier - 4-itera"

```
001AA4F0  mov      qword ptr [rsp + 8], rbx
001AA4F5  mov      qword ptr [rsp + 0x10], rsi
001AA4FA  push     rdi
001AA4FB  sub      rsp, 0x20
001AA4FF  mov      rbx, r8
001AA502  mov      rdi, rdx
001AA505  mov      rsi, rcx
001AA508  cmp      rdx, rcx
001AA50B  je       0x1aa55a  ; -> 001AA55A
001AA50D  nop      dword ptr [rax]
001AA510  movzx    eax, byte ptr [rdi - 0x30]
001AA514  add      rdi, -0x30
001AA518  add      rbx, -0x30
001AA51C  lea      rdx, [rdi + 8]
001AA520  mov      byte ptr [rbx], al
001AA522  lea      rcx, [rbx + 8]
001AA526  movzx    eax, byte ptr [rdi + 1]
001AA52A  mov      byte ptr [rbx + 1], al
001AA52D  movzx    eax, byte ptr [rdi + 2]
001AA531  mov      byte ptr [rbx + 2], al
001AA534  movzx    eax, byte ptr [rdi + 3]
001AA538  mov      byte ptr [rbx + 3], al
001AA53B  movzx    eax, byte ptr [rdi + 4]
001AA53F  mov      byte ptr [rbx + 4], al
001AA542  movzx    eax, byte ptr [rdi + 5]
001AA546  mov      byte ptr [rbx + 5], al
001AA549  call     0x19ddd0  ; -> 0019DDD0 fn
001AA54E  movzx    eax, byte ptr [rdi + 0x28]
001AA552  mov      byte ptr [rbx + 0x28], al
001AA555  cmp      rdi, rsi
001AA558  jne      0x1aa510  ; -> 001AA510
001AA55A  mov      rsi, qword ptr [rsp + 0x38]
001AA55F  mov      rax, rbx
001AA562  mov      rbx, qword ptr [rsp + 0x30]
001AA567  add      rsp, 0x20
001AA56B  pop      rdi
001AA56C  ret      
```

## 001AB350 (115 B, extent 001AB350-001AB3C3)

Page context: "d. Interior anchor '001A7665' (the '[rax+0x78]' chain advance).    ## SWE2-EC7-63 update (2026-09-19) - '001AB8A0'  '001AB8A0' (488 B) is a TA-list body - '0019D8D0'/'001AA4F0'/'001AA630'/'001AAF80'/'001AB350' plus two vcalls. Interior anchor '001AB906' (a '0019D8D0' call).    ## SWE2-EC7-63 update (2026-09-19) - '001E1490'  '001E1490' (144 B) is a call-free '0x80'-stride 'movups' record copier - 4-iteration unroll. Interior anchor '001"

```
001AB350  cmp      rdx, r8
001AB353  jae      0x1ab3c2  ; -> 001AB3C2
001AB355  push     rdi
001AB356  sub      rsp, 0x30
001AB35A  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001AB363  mov      qword ptr [rsp + 0x40], rbx
001AB368  lea      rbx, [rdx + 8]
001AB36C  sub      r8, rdx
001AB36F  dec      r8
001AB372  movabs   rax, 0xaaaaaaaaaaaaaaab
001AB37C  mul      r8
001AB37F  mov      rdi, rdx
001AB382  shr      rdi, 5
001AB386  inc      rdi
001AB389  nop      dword ptr [rax]
001AB390  mov      rdx, qword ptr [rbx]
001AB393  test     rdx, rdx
001AB396  je       0x1ab3ae  ; -> 001AB3AE
001AB398  lea      rcx, [rbx + 0x18]
001AB39C  mov      rax, qword ptr [rcx]
001AB39F  mov      r8, qword ptr [rcx - 8]
001AB3A3  sub      r8, rdx
001AB3A6  and      r8, 0xfffffffffffffff8
001AB3AA  call     qword ptr [rax + 0x18]
001AB3AD  nop      
001AB3AE  add      rbx, 0x30
001AB3B2  sub      rdi, 1
001AB3B6  jne      0x1ab390  ; -> 001AB390
001AB3B8  mov      rbx, qword ptr [rsp + 0x40]
001AB3BD  add      rsp, 0x30
001AB3C1  pop      rdi
001AB3C2  ret      
```

## 001ABC80 (89 B, extent 001ABC80-001ABCD9)

Page context: "; interior verified 2026-09-17, SWE2-FRONTIER — '001E1370' first at ['001E1EF1'](../../_index/ADDRESS-INDEX.md)), '001E3F70', '001E5290', '001E55C0'/'001E6110' (462 B twins → '001E6040'), '001AC480'/'001ABC80'/'001ABCE0'/'001AD6E0'/'001AD7B0' | element ops behind the iterators — '001E1DD0''s '[r9]' pair is the same callback idiom as the SEAD container family ('00210760' subtree) |  Not established: which of the two dispatcher twins serv"

```
001ABC80  test     r8d, r8d
001ABC83  js       0x1abcd8  ; -> 001ABCD8
001ABC85  mov      qword ptr [rsp + 0x10], rsi
001ABC8A  push     rdi
001ABC8B  sub      rsp, 0x20
001ABC8F  mov      rsi, rdx
001ABC92  mov      qword ptr [rsp + 0x30], rbx
001ABC97  mov      edx, r8d
001ABC9A  mov      edi, r9d
001ABC9D  call     0x1ac810  ; -> 001AC810 fn
001ABCA2  mov      r9d, dword ptr [rsp + 0x50]
001ABCA7  mov      r8d, edi
001ABCAA  mov      rdx, rsi
001ABCAD  mov      rcx, rax
001ABCB0  mov      rbx, rax
001ABCB3  call     0x1ad7b0  ; -> 001AD7B0 fn
001ABCB8  mov      rax, qword ptr [rbx]
001ABCBB  lea      ecx, [rdi*2 - 2]
001ABCC2  mov      rbx, qword ptr [rsp + 0x30]
001ABCC7  mov      rsi, qword ptr [rsp + 0x38]
001ABCCC  movsxd   rdx, ecx
001ABCCF  mov      byte ptr [rdx + rax], 1
001ABCD3  add      rsp, 0x20
001ABCD7  pop      rdi
001ABCD8  ret      
```

## 001ABCE0 (89 B, extent 001ABCE0-001ABD39)

Page context: "verified 2026-09-17, SWE2-FRONTIER — '001E1370' first at ['001E1EF1'](../../_index/ADDRESS-INDEX.md)), '001E3F70', '001E5290', '001E55C0'/'001E6110' (462 B twins → '001E6040'), '001AC480'/'001ABC80'/'001ABCE0'/'001AD6E0'/'001AD7B0' | element ops behind the iterators — '001E1DD0''s '[r9]' pair is the same callback idiom as the SEAD container family ('00210760' subtree) |  Not established: which of the two dispatcher twins serves '.ta' ve"

```
001ABCE0  test     r8d, r8d
001ABCE3  js       0x1abd38  ; -> 001ABD38
001ABCE5  mov      qword ptr [rsp + 0x10], rsi
001ABCEA  push     rdi
001ABCEB  sub      rsp, 0x20
001ABCEF  mov      rsi, rdx
001ABCF2  mov      qword ptr [rsp + 0x30], rbx
001ABCF7  mov      edx, r8d
001ABCFA  mov      edi, r9d
001ABCFD  call     0x1ac810  ; -> 001AC810 fn
001ABD02  mov      r9d, dword ptr [rsp + 0x50]
001ABD07  mov      r8d, edi
001ABD0A  mov      rdx, rsi
001ABD0D  mov      rcx, rax
001ABD10  mov      rbx, rax
001ABD13  call     0x1ad6e0  ; -> 001AD6E0 fn
001ABD18  mov      rax, qword ptr [rbx]
001ABD1B  lea      ecx, [rdi*2 - 1]
001ABD22  mov      rbx, qword ptr [rsp + 0x30]
001ABD27  mov      rsi, qword ptr [rsp + 0x38]
001ABD2C  movsxd   rdx, ecx
001ABD2F  mov      byte ptr [rdx + rax], 1
001ABD33  add      rsp, 0x20
001ABD37  pop      rdi
001ABD38  ret      
```

## 001AC480 (34 B, extent 001AC480-001AC4A2)

Page context: "llback pair; interior verified 2026-09-17, SWE2-FRONTIER — '001E1370' first at ['001E1EF1'](../../_index/ADDRESS-INDEX.md)), '001E3F70', '001E5290', '001E55C0'/'001E6110' (462 B twins → '001E6040'), '001AC480'/'001ABC80'/'001ABCE0'/'001AD6E0'/'001AD7B0' | element ops behind the iterators — '001E1DD0''s '[r9]' pair is the same callback idiom as the SEAD container family ('00210760' subtree) |  Not established: which of the two dispatcher"

```
001AC480  push     rbx
001AC482  sub      rsp, 0x20
001AC486  lea      rdx, [rcx + 0x16c]
001AC48D  mov      rbx, rcx
001AC490  call     0x1ad130  ; -> 001AD130 fn
001AC495  mov      byte ptr [rbx + 0x250], 1
001AC49C  add      rsp, 0x20
001AC4A0  pop      rbx
001AC4A1  ret      
```

## 003ABD20 (39 B, extent 003ABD20-003ABD47)

Page context: "ock read and the resolver the open question covers | | emit/scratch | '0018C3C0' (144 B — '0085E730' + '001F1D30' + '001AB570' + '0018B4E0', the same shape as the '0022B0B0' four-sibling pass arms), '003ABD20' ('02B3F508'), '00467A70'/'00467A90' ('02CA5FF4'/'F8'), '00467B60' (71 B — rip-indirect + '008C2BD8'/'00901988'/'00D12518'/'01CEBD80'/'02AED570'), '00468070' | the draw-side emit the pass feeds | | leaves | '00180870', '001A9DD0', "

```
003ABD20  mov      rax, qword ptr [rip + 0x27937e1]  ; -> 02B3F508
003ABD27  test     rax, rax
003ABD2A  je       0x3abd3f  ; -> 003ABD3F
003ABD2C  nop      dword ptr [rax]
003ABD30  cmp      byte ptr [rax + 0x23], 5
003ABD34  je       0x3abd42  ; -> 003ABD42
003ABD36  mov      rax, qword ptr [rax + 0x10]
003ABD3A  test     rax, rax
003ABD3D  jne      0x3abd30  ; -> 003ABD30
003ABD3F  xor      eax, eax
003ABD41  ret      
003ABD42  add      rax, 0x20
003ABD46  ret      
```

## 00467A70 (27 B, extent 00467A70-00467A8B)

Page context: " the open question covers | | emit/scratch | '0018C3C0' (144 B — '0085E730' + '001F1D30' + '001AB570' + '0018B4E0', the same shape as the '0022B0B0' four-sibling pass arms), '003ABD20' ('02B3F508'), '00467A70'/'00467A90' ('02CA5FF4'/'F8'), '00467B60' (71 B — rip-indirect + '008C2BD8'/'00901988'/'00D12518'/'01CEBD80'/'02AED570'), '00468070' | the draw-side emit the pass feeds | | leaves | '00180870', '001A9DD0', '001E3E80', '001E3FF0', '"

```
00467A70  mov      eax, dword ptr [rip + 0x283e57e]  ; -> 02CA5FF4
00467A76  mov      dword ptr [rip + 0x283e57c], eax  ; -> 02CA5FF8
00467A7C  xor      eax, eax
00467A7E  mov      dword ptr [rip + 0x283e578], eax  ; -> 02CA5FFC
00467A84  mov      dword ptr [rip + 0x283e576], eax  ; -> 02CA6000
00467A8A  ret      
```

## 00467B60 (71 B, extent 00467B60-00467BA7)

Page context: "h | '0018C3C0' (144 B — '0085E730' + '001F1D30' + '001AB570' + '0018B4E0', the same shape as the '0022B0B0' four-sibling pass arms), '003ABD20' ('02B3F508'), '00467A70'/'00467A90' ('02CA5FF4'/'F8'), '00467B60' (71 B — rip-indirect + '008C2BD8'/'00901988'/'00D12518'/'01CEBD80'/'02AED570'), '00468070' | the draw-side emit the pass feeds | | leaves | '00180870', '001A9DD0', '001E3E80', '001E3FF0', '001E4B00' | five 7–17 B thunks |  'TA-1''"

```
00467B60  sub      rsp, 0x28
00467B64  movss    xmm0, dword ptr [rip + 0x499e1c]  ; -> 00901988 [f32 20]
00467B6C  subss    xmm0, dword ptr [rip + 0x26859fc]  ; -> 02AED570
00467B74  cvtps2pd xmm1, xmm0
00467B77  andps    xmm1, xmmword ptr [rip + 0x1884202]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
00467B7E  cvtpd2ps xmm0, xmm1
00467B82  call     qword ptr [rip + 0x45b050]  ; -> 008C2BD8 [u64 0x0000000001CCF074]
00467B88  mulss    xmm0, dword ptr [rip + 0x8aa988]  ; -> 00D12518 [f32 -16]
00467B90  cvttss2si eax, xmm0
00467B94  movsxd   rcx, eax
00467B97  shl      rcx, 0x20
00467B9B  mov      qword ptr [rip + 0x2a53b26], rcx  ; -> 02EBB6C8
00467BA2  add      rsp, 0x28
00467BA6  ret      
```

## 00468070 (84 B, extent 00468070-004680C4)

Page context: "s the '0022B0B0' four-sibling pass arms), '003ABD20' ('02B3F508'), '00467A70'/'00467A90' ('02CA5FF4'/'F8'), '00467B60' (71 B — rip-indirect + '008C2BD8'/'00901988'/'00D12518'/'01CEBD80'/'02AED570'), '00468070' | the draw-side emit the pass feeds | | leaves | '00180870', '001A9DD0', '001E3E80', '001E3FF0', '001E4B00' | five 7–17 B thunks |  'TA-1''s answer lives here in embryo: '001E5790' is the clock source ('01CEBDA0' — the same global"

```
00468070  mov      r9, qword ptr [rcx + 8]
00468074  or       r8d, 0x6c010000
0046807B  lea      rax, [r9 + 0x30]
0046807F  mov      qword ptr [rcx + 8], rax
00468083  xor      eax, eax
00468085  mov      qword ptr [r9 + 8], rax
00468089  mov      qword ptr [r9], 0x10000002
00468090  mov      dword ptr [r9 + 0x10], eax
00468094  mov      dword ptr [r9 + 0x14], 0x10000000
0046809C  mov      dword ptr [r9 + 0x18], 0x1000404
004680A4  mov      dword ptr [r9 + 0x1c], r8d
004680A8  mov      eax, dword ptr [rdx]
004680AA  mov      dword ptr [r9 + 0x20], eax
004680AE  mov      eax, dword ptr [rdx + 4]
004680B1  mov      dword ptr [r9 + 0x24], eax
004680B5  mov      eax, dword ptr [rdx + 8]
004680B8  mov      dword ptr [r9 + 0x28], eax
004680BC  mov      eax, dword ptr [rdx + 0xc]
004680BF  mov      dword ptr [r9 + 0x2c], eax
004680C3  ret      
```
