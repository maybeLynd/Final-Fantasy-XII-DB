# F-interior pack: `19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md`

Generated 2026-10-02 18:33 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/game-settings-ini-and-runtime-config.json`.

Functions: 7. Each is cited on the page only at its entry and is still in the F frontier.

## 0017ECB0 (10 B, extent 0017ECB0-0017ECBA)

Page context: "(mode, 1, 3)' in '01F3DA18' ('00798E90'; getter '00184950', eight callers that add it to per-frame accumulators such as '0208F570') and posts it to the render thread through a command whose callback '0017ECB0' copies it to '01DF08F8'. The render side '006234A0' reads it back ('0017ECE0') and calls **'IDXGISwapChain::Present(interval, flags)'** through the swap chain at '+0x118' of its device object (vtable slot 8, '+0x40' — 'Present''s "

```
0017ECB0  mov      eax, dword ptr [rcx + 0x10]
0017ECB3  mov      dword ptr [rip + 0x1c71c3f], eax  ; -> 01DF08F8 [u32 0x00000002]
0017ECB9  ret      
```

## 001DA090 (92 B, extent 001DA090-001DA0EC)

Page context: "er viewer page](../../16-UI/Handbook/the-handbooks-monster-viewer.md).   - **'001DADA0()' is the FileCache singleton '[01F82CF0]', and '+0x88' is its "map jump pending" byte.**     It is set only by '001DA090', which logs '"[FileCache] OnMapJumpBefore (%d)"' ('009006E8'), records     the previous and next field ids at '+0x80' / '+0x7C', and hands them to '0020C1A0'. '001DA090' is     reached only through '001D6C40', from 'WorldTransitio"

```
001DA090  test     edx, edx
001DA092  js       0x1da0eb  ; -> 001DA0EB
001DA094  mov      qword ptr [rsp + 8], rbx
001DA099  push     rdi
001DA09A  sub      rsp, 0x20
001DA09E  mov      eax, dword ptr [rcx + 0x7c]
001DA0A1  mov      ebx, edx
001DA0A3  mov      byte ptr [rcx + 0x88], 1
001DA0AA  mov      rdi, rcx
001DA0AD  cmp      eax, edx
001DA0AF  je       0x1da0e1  ; -> 001DA0E1
001DA0B1  mov      dword ptr [rcx + 0x80], eax
001DA0B7  mov      dword ptr [rcx + 0x7c], edx
001DA0BA  call     0x20c700  ; -> 0020C700 fn
001DA0BF  mov      edx, dword ptr [rdi + 0x80]
001DA0C5  mov      rcx, rax
001DA0C8  mov      r8d, ebx
001DA0CB  call     0x20c1a0  ; -> 0020C1A0 fn
001DA0D0  mov      r8d, ebx
001DA0D3  lea      rdx, [rip + 0x72660e]  ; -> 009006E8
001DA0DA  xor      ecx, ecx
001DA0DC  call     0x5cdaa0  ; -> 005CDAA0 fn
001DA0E1  mov      rbx, qword ptr [rsp + 0x30]
001DA0E6  add      rsp, 0x20
001DA0EA  pop      rdi
001DA0EB  ret      
```

## 001DF760 (110 B, extent 001DF760-001DF7CE)

Page context: "parser, not a table fill — see note below), '001DDC40' (430 B, 8 more indirect calls), '001DED50' (wires '001DE5D0' + '001DF240' + '001DFD40'), '001DF240' ('01DFDA10'/'01DFDB60'/'01DFDCB0' triples), '001DF760' (5 indirect calls) | '001DED50' installs the object's method/interface table; '001DE5D0' is one of the methods *being* installed | | input-binding readers | '0020C730' (263 B, '0020CCC0' + '008C3180'/'00906360' consts), '0020CCC0'"

```
001DF760  sub      rsp, 0x28
001DF764  mov      r9, rdx
001DF767  or       rax, 0xffffffffffffffff
001DF76B  xor      edx, edx
001DF76D  div      r8
001DF770  cmp      r9, rax
001DF773  jbe      0x1df77c  ; -> 001DF77C
001DF775  call     qword ptr [rip + 0x6e362d]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001DF77B  int3     
001DF77C  imul     r9, r8
001DF780  cmp      r9, 0x1000
001DF787  jb       0x1df7c5  ; -> 001DF7C5
001DF789  test     cl, 0x1f
001DF78C  je       0x1df795  ; -> 001DF795
001DF78E  call     qword ptr [rip + 0x6e3614]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001DF794  int3     
001DF795  mov      rax, qword ptr [rcx - 8]
001DF799  cmp      rax, rcx
001DF79C  jb       0x1df7a5  ; -> 001DF7A5
001DF79E  call     qword ptr [rip + 0x6e3604]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001DF7A4  int3     
001DF7A5  sub      rcx, rax
001DF7A8  cmp      rcx, 8
001DF7AC  jae      0x1df7b5  ; -> 001DF7B5
001DF7AE  call     qword ptr [rip + 0x6e35f4]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001DF7B4  int3     
001DF7B5  cmp      rcx, 0x27
001DF7B9  jbe      0x1df7c2  ; -> 001DF7C2
001DF7BB  call     qword ptr [rip + 0x6e35e7]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001DF7C1  int3     
001DF7C2  mov      rcx, rax
001DF7C5  add      rsp, 0x28
001DF7C9  jmp      0x210eb0  ; -> 00210EB0 fn
```

## 001ED0D0 (94 B, extent 001ED0D0-001ED12E)

Page context: "'m1266', 'm1222', 'm1223', 'm1151', 'm1267' | '1' | '0' | | '001ED020(name)' | '00418880' | progress '0x15AE' + state 1 + 'g0111'; progress '0x15E0' + state 15 + 'c1006' | '0.5' / '−1.0' | '0.0' | | '001ED0D0(name, id)' | '00416FB0' | outside a cutscene: 'hc1006' with 'id == 0x57' | '0.0' | '0.5' | | '001ED1E0()' | '004717E0' | progress '0x14B7' + state 4 | '1' | '0' | | '001ED240(…, f)' | '00418880' | progress '0xD70', '0x15AE', '0x15E"

```
001ED0D0  mov      qword ptr [rsp + 8], rbx
001ED0D5  push     rdi
001ED0D6  sub      rsp, 0x20
001ED0DA  cmp      dword ptr [rip + 0x1d95d57], 0  ; -> 01F82E38
001ED0E1  movzx    ebx, dx
001ED0E4  mov      rdi, rcx
001ED0E7  je       0x1ed11b  ; -> 001ED11B
001ED0E9  call     0x1ec560  ; -> 001EC560 fn
001ED0EE  test     eax, eax
001ED0F0  jne      0x1ed11b  ; -> 001ED11B
001ED0F2  lea      rdx, [rip + 0x7154f3]  ; -> 009025EC [str "hc1006"]
001ED0F9  mov      rcx, rdi
001ED0FC  call     qword ptr [rip + 0x6d5906]  ; -> 008C2A08 [u64 0x0000000001CCEBD2]
001ED102  test     rax, rax
001ED105  je       0x1ed11b  ; -> 001ED11B
001ED107  cmp      bx, 0x57
001ED10B  jne      0x1ed11b  ; -> 001ED11B
001ED10D  xorps    xmm0, xmm0
001ED110  mov      rbx, qword ptr [rsp + 0x30]
001ED115  add      rsp, 0x20
001ED119  pop      rdi
001ED11A  ret      
001ED11B  movss    xmm0, dword ptr [rip + 0x1afea4d]  ; -> 01CEBB70 [f32 0.5]
001ED123  mov      rbx, qword ptr [rsp + 0x30]
001ED128  add      rsp, 0x20
001ED12C  pop      rdi
001ED12D  ret      
```

## 001ED1E0 (86 B, extent 001ED1E0-001ED236)

Page context: "x15AE' + state 1 + 'g0111'; progress '0x15E0' + state 15 + 'c1006' | '0.5' / '−1.0' | '0.0' | | '001ED0D0(name, id)' | '00416FB0' | outside a cutscene: 'hc1006' with 'id == 0x57' | '0.0' | '0.5' | | '001ED1E0()' | '004717E0' | progress '0x14B7' + state 4 | '1' | '0' | | '001ED240(…, f)' | '00418880' | progress '0xD70', '0x15AE', '0x15E0' … with 'g0999', 'c1019', 'c1004', 'c1005', 'n1018', 'n1210', 'c1021', 'c1006', 'mrm_g0100', 'bds_f01"

```
001ED1E0  sub      rsp, 0x28
001ED1E4  cmp      dword ptr [rip + 0x1d95c4d], 0  ; -> 01F82E38
001ED1EB  je       0x1ed22f  ; -> 001ED22F
001ED1ED  call     0x1ec560  ; -> 001EC560 fn
001ED1F2  test     eax, eax
001ED1F4  je       0x1ed22f  ; -> 001ED22F
001ED1F6  call     0x265270  ; -> 00265270 fn
001ED1FB  movsx    edx, ax
001ED1FE  movsxd   rax, dword ptr [rip + 0x1c11207]  ; -> 01DFE40C [u32 0xFFFFFFFF]
001ED205  cmp      eax, 4
001ED208  ja       0x1ed216  ; -> 001ED216
001ED20A  lea      rcx, [rip + 0x1d9609f]  ; -> 01F832B0
001ED211  mov      ecx, dword ptr [rcx + rax*4]
001ED214  jmp      0x1ed218  ; -> 001ED218
001ED216  xor      ecx, ecx
001ED218  cmp      edx, 0x14b7
001ED21E  jne      0x1ed22f  ; -> 001ED22F
001ED220  cmp      ecx, 4
001ED223  jne      0x1ed22f  ; -> 001ED22F
001ED225  mov      eax, 1
001ED22A  add      rsp, 0x28
001ED22E  ret      
001ED22F  xor      eax, eax
001ED231  add      rsp, 0x28
001ED235  ret      
```

## 0020C1A0 (16 B, extent 0020C1A0-0020C1B0)

Page context: "p pending" byte.**     It is set only by '001DA090', which logs '"[FileCache] OnMapJumpBefore (%d)"' ('009006E8'), records     the previous and next field ids at '+0x80' / '+0x7C', and hands them to '0020C1A0'. '001DA090' is     reached only through '001D6C40', from 'WorldTransition_RequestFieldTransition' ('00314508') and     'WorldTransition_RequeueCurrentFieldForRestore' ('003145CF').   - It is cleared only by the 7-byte '001DA080' ("

```
0020C1A0  mov      dword ptr [rcx + 0x84], edx
0020C1A6  mov      al, 1
0020C1A8  mov      dword ptr [rcx + 0x80], r8d
0020C1AF  ret      
```

## 008B9040 (28 B, extent 008B9040-008B905C)

Page context: "'006253D0' (the display-adapter enumeration) uses: the '02EAEA98' bit-0 once-guard double-checks around 'lock' refcount '02EAEA128', installs vtable '01CC6B60' at '02EAEA68'/'02EAEA70' and registers '008B9040' teardown via '00808B90', then '00158F60()' runs under the guard with counter '02EAEA138' - returns that call's result  Interior anchor '001593A6' (function '00159340').  '001EDCD0' (203 B) is the gated whitelist test '0040ACF0' ru"

```
008B9040  lea      rax, [rip + 0x140db19]  ; -> 01CC6B60
008B9047  lea      rcx, [rip + 0x25f5a22]  ; -> 02EAEA70
008B904E  mov      qword ptr [rip + 0x25f5a13], rax  ; -> 02EAEA68
008B9055  jmp      qword ptr [rip + 0x9074]  ; -> 008C20D0 [u64 0x0000000001CCC110]
```
