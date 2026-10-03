# Homing pack: `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-ui-layout-parameters-and-editor-schema.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00251D20 (36 B, extent 00251D20-00251D44)

Entered from (direct sites whose caller this page cites): `003EEEC0` + 0x106 (call; `003EEEC0` is cited on this page)
Other direct sites: none

Host context: "hor '002A03BC' (the proportional-path '002D8D40' call).  ## SWE2-EC7-106 update (2026-09-20) - '00251D90' measured  '00251D90' (105 B) is the conditional one-shot register '002289D0', '0027FB70' and '003EEEC0' call: only when '020927F0' is null does it build a stack descriptor - 'word = cx', 'dword = edx', 'dword = r8d', a count out-slot and a '0x10'-byte buffer pointer - and runs '00244F50(0x140, 002509D0, &desc)'; a live record skips "

```
00251D20  mov      rax, qword ptr [rip + 0x1e40ac9]  ; -> 020927F0
00251D27  test     rax, rax
00251D2A  je       0x251d43  ; -> 00251D43
00251D2C  test     byte ptr [rax + 0xe8], 1
00251D33  je       0x251d3d  ; -> 00251D3D
00251D35  movsx    eax, word ptr [rax + 0xe6]
00251D3C  ret      
00251D3D  mov      eax, 2
00251D42  ret      
00251D43  ret      
```

## 00270880 (48 B, extent 00270880-002708B0)

Entered from (direct sites whose caller this page cites): `0028D260` + 0x1AC (call; `0028D260` is cited on this page); `0028D460` + 0x31D (call; `0028D460` is cited on this page)
Other direct sites: none

Host context: "and '+0xD8' ('0039BB60'), then '0017FA70' and '00473B50'/'00473B60' - the layout record's release sweep.  Interior anchor '0037F87D' (function '0037F860').  '0028CB90' (381 B) is the interval lookup '0028D260'/'0028D460' call: an 'r8d'-bounded bisect over word pairs at 'rbx' - 'word[rbx + 6] > r9d' descends left, 'word[rbx + 0xE] <= r9d' ascends right - then '00861F0E' twice and '002752E0' - the layout's range search.  Interior anchor '" / " P | | 'ScrollMark…' | 2 | '002CEB40', '002D1750' | | 'SilhouettePos…' | 2 | '002CF440' P | | 'SystemWindow…' | 2 | '002A4170' | | 'TalkingMessage…' | 2 | '002A2C00' | | '2DSideCursorCenterX…' | 1 | '0028D460' | | '2DSideCursorCenterY…' | 1 | '0028D460' | | 'BaseMap…' | 1 | '002BCB00' | | 'BattleMenu…' | 1 | '00276D30' P | | 'BlackBand…' | 1 | '0027EE80', '0027EED0', '0027EF00', '0027EF50', '002804E0', '002814E0', '00281ED0', '002BA700'"

```
00270880  movaps   xmm0, xmm2
00270883  movaps   xmm1, xmm2
00270886  mulss    xmm0, dword ptr [rdx]
0027088A  movss    dword ptr [rcx], xmm0
0027088E  movaps   xmm0, xmm2
00270891  mulss    xmm1, dword ptr [rdx + 4]
00270896  movss    dword ptr [rcx + 4], xmm1
0027089B  mulss    xmm0, dword ptr [rdx + 8]
002708A0  movss    dword ptr [rcx + 8], xmm0
002708A5  mulss    xmm2, dword ptr [rdx + 0xc]
002708AA  movss    dword ptr [rcx + 0xc], xmm2
002708AF  ret      
```

## 002C5660 (137 B, extent 002C5660-002C56E9)

Entered from (direct sites whose caller this page cites): `002C59D0` + 0xEF (call; `002C59D0` is cited on this page)
Other direct sites: none

Host context: "CD', inside the   '002B3120'→'002B3050'→'00474100' text-layout path), '002D4930' ('FontBaseHeight'→'r9d',   'sub r9d, edx', '002D4961' — shared by the action list, battle command, nobu-message and   '002C59D0'-family callers), '002D5EB0' P (the 'NaSPArt' signal widget, installed by '002D5030':   'OffsetY' 'sub'ed, 'OffsetX'→'ecx' → '0029E770', '002D6117'/'002D611D' — the same call the map and   item screens use), '00291D80' P (tail-jump"

```
002C5660  push     rbx
002C5662  push     rbp
002C5663  push     rdi
002C5664  sub      rsp, 0x20
002C5668  xor      ebp, ebp
002C566A  mov      edi, ebp
002C566C  mov      ebx, ebp
002C566E  nop      
002C5670  mov      ecx, ebx
002C5672  call     0x282df0  ; -> 00282DF0 fn
002C5677  cmp      word ptr [rax + 0x60], bp
002C567B  jl       0x2c5680  ; -> 002C5680
002C567D  or       edi, dword ptr [rax + 0x44]
002C5680  inc      ebx
002C5682  cmp      ebx, 9
002C5685  jl       0x2c5670  ; -> 002C5670
002C5687  test     edi, edi
002C5689  je       0x2c56de  ; -> 002C56DE
002C568B  mov      ebx, 1
002C5690  mov      qword ptr [rsp + 0x50], rsi
002C5695  rol      ebx, 0
002C5698  mov      esi, ebp
002C569A  nop      word ptr [rax + rax]
002C56A0  test     edi, ebx
002C56A2  je       0x2c56d0  ; -> 002C56D0
002C56A4  mov      edx, esi
002C56A6  mov      ecx, 0x1a
002C56AB  call     0x35d330  ; -> 0035D330 fn
002C56B0  lea      r9, [rsp + 0x48]
002C56B5  xor      ecx, ecx
002C56B7  lea      r8, [rsp + 0x40]
002C56BC  mov      rdx, qword ptr [rax + 0x10]
002C56C0  call     0x2b3050  ; -> 002B3050 fn
002C56C5  cmp      word ptr [rsp + 0x40], bp
002C56CA  cmovg    bp, word ptr [rsp + 0x40]
002C56D0  inc      esi
002C56D2  rol      ebx, 1
002C56D4  cmp      esi, 0x20
002C56D7  jl       0x2c56a0  ; -> 002C56A0
002C56D9  mov      rsi, qword ptr [rsp + 0x50]
002C56DE  movsx    eax, bp
002C56E1  add      rsp, 0x20
002C56E5  pop      rdi
002C56E6  pop      rbp
002C56E7  pop      rbx
002C56E8  ret      
```

## 00404D40 (44 B, extent 00404D40-00404D6C)

Entered from (direct sites whose caller this page cites): `00405310` + 0x302 (call; `00405310` is cited on this page)
Other direct sites: none

Host context: " x2, '00249C60', '002C3B90' walk the entries into 'r15d' - the layout family's counted list pass.  Interior anchor '002C3071' (function '002C2F90').  '00405C20' (1162 B) is the flag-gated gauge draw '00405310' runs: '[rcx+0x130]' bit 8 and 'test 0x40' gate the modes, '[rcx+0xD0]'/'[rcx+0xE4]' feed the state, '0029E840' x2 binds the shader material, '0035D460', '002DAF30', '002D9DB0', '002DAC70' x2 and '002D8D10' x2 run the textured-quad"

```
00404D40  mov      rax, qword ptr [rip + 0x275e041]  ; -> 02B62D88
00404D47  test     rax, rax
00404D4A  je       0x404d69  ; -> 00404D69
00404D4C  mov      rdx, qword ptr [rax + 0xc0]
00404D53  test     rdx, rdx
00404D56  je       0x404d69  ; -> 00404D69
00404D58  cmp      ecx, 2
00404D5B  jge      0x404d69  ; -> 00404D69
00404D5D  movsxd   rax, ecx
00404D60  mov      rax, qword ptr [rdx + rax*8 + 0xc8]
00404D68  ret      
00404D69  xor      eax, eax
00404D6B  ret      
```
