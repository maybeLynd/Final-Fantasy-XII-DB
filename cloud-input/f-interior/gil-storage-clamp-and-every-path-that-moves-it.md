# F-interior pack: `13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/gil-storage-clamp-and-every-path-that-moves-it.json`.

Functions: 20. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ). OPUS read these before packing.

## 0017F9E0 (44 B, extent 0017F9E0-0017FA0C)

Page context: "9C3F0' ('0032E400'/'003EFCD0'/'0032E620'), '003EFCD0' (alloc triple '0036C1D0'/'0036A100'/'0036C140') | state cells the binder primes — the '022CBExx' band reuses the deque-alloc family | | leaves | '0017F9E0' ('001B5FB0'), '00229E30' ('01E02818'), '002494A0' ('02090790'/'02090910'), '0024A660' ('0208F580'), '00272470', '002800F0' ('0209AC60'), '0029CE40' ('00229E30'/'00229E40'/'0017F9E0'/'0039BB30'/'002B3550'/'00364950' — a small fan-o"

```
0017F9E0  mov      qword ptr [rsp + 8], rbx
0017F9E5  push     rdi
0017F9E6  sub      rsp, 0x20
0017F9EA  movzx    ebx, dl
0017F9ED  mov      edi, ecx
0017F9EF  call     0x1b5fb0  ; -> 001B5FB0 fn
0017F9F4  mov      rcx, rax
0017F9F7  movzx    r8d, bl
0017F9FB  mov      edx, edi
0017F9FD  mov      rbx, qword ptr [rsp + 0x30]
0017FA02  add      rsp, 0x20
0017FA06  pop      rdi
0017FA07  jmp      0x1b44a0  ; -> 001B44A0 fn
```

## 0020CB50 (334 B, extent 0020CB50-0020CC9E)

Page context: " calls '003165C0', '00863280' and '008632B0', and '00316440' calls '00863280' and '008632B0'; the counter-object getter '0020CE00' is called only by '00863240', '00863280' and '008632B0', which call '0020CB50', '0020CCA0' and '0020CE60'; '008632B0' is also called by '00315E90'; the verbs '0034C9A0' and '00352250' call '00863240' and '008632B0'. The setter feeds the gil meter, the achievement checks read the header '+0x0C' walked-distanc"

```
0020CB50  mov      qword ptr [rsp + 0x10], rbx
0020CB55  mov      qword ptr [rsp + 0x18], rbp
0020CB5A  push     rdi
0020CB5B  sub      rsp, 0x20
0020CB5F  xor      ebp, ebp
0020CB61  lea      rax, [rip + 0x6f972c]  ; -> 00906294
0020CB68  mov      rdi, rcx
0020CB6B  mov      ebx, ebp
0020CB6D  lea      rcx, [rip + 0x6f9774]  ; -> 009062E8
0020CB74  cmp      edx, dword ptr [rax - 4]
0020CB77  jne      0x20cb7e  ; -> 0020CB7E
0020CB79  cmp      r8d, dword ptr [rax]
0020CB7C  je       0x20cb99  ; -> 0020CB99
0020CB7E  inc      ebx
0020CB80  add      rax, 0xc
0020CB84  cmp      rax, rcx
0020CB87  jl       0x20cb74  ; -> 0020CB74
0020CB89  mov      rbx, qword ptr [rsp + 0x38]
0020CB8E  mov      rbp, qword ptr [rsp + 0x40]
0020CB93  add      rsp, 0x20
0020CB97  pop      rdi
0020CB98  ret      
0020CB99  movsxd   rax, ebx
0020CB9C  mov      qword ptr [rsp + 0x30], rsi
0020CBA1  lea      rcx, [rax + rax*2]
0020CBA5  lea      rax, [rip + 0x6f96ec]  ; -> 00906298
0020CBAC  movsxd   rax, dword ptr [rax + rcx*4]
0020CBB0  imul     rcx, rax, 0x198
0020CBB7  add      rcx, qword ptr [rdi + 8]
0020CBBB  cmp      byte ptr [rcx + 0x190], bpl
0020CBC2  jne      0x20cc0c  ; -> 0020CC0C
0020CBC4  mov      rsi, qword ptr [rcx + 8]
0020CBC8  mov      byte ptr [rcx + 0x190], 1
0020CBCF  mov      dword ptr [rcx + 0x194], ebp
0020CBD5  cmp      byte ptr [rdi + 0x18], bpl
0020CBD9  je       0x20cc0c  ; -> 0020CC0C
0020CBDB  lea      rcx, [rip + 0x1bf14ee]  ; -> 01DFE0D0
0020CBE2  call     qword ptr [rip + 0x6b65a8]  ; -> 008C3190 [u64 0x0000000001CCBFA6]
0020CBE8  mov      rdx, rsi
0020CBEB  mov      rcx, qword ptr [rax + 0x28]
0020CBEF  mov      rax, qword ptr [rcx]
0020CBF2  call     qword ptr [rax + 0x38]
0020CBF5  lea      rcx, [rip + 0x1bf14d4]  ; -> 01DFE0D0
0020CBFC  call     qword ptr [rip + 0x6b658e]  ; -> 008C3190 [u64 0x0000000001CCBFA6]
0020CC02  mov      rcx, qword ptr [rax + 0x28]
0020CC06  mov      rax, qword ptr [rcx]
0020CC09  call     qword ptr [rax + 0x50]
0020CC0C  cmp      ebx, 6
0020CC0F  jne      0x20cc89  ; -> 0020CC89
0020CC11  mov      ebx, 0x3168
0020CC16  nop      word ptr [rax + rax]
0020CC20  mov      rax, qword ptr [rdi + 8]
0020CC24  cmp      byte ptr [rbx + rax + 0x190], bpl
0020CC2C  jne      0x20cc79  ; -> 0020CC79
0020CC2E  mov      rsi, qword ptr [rbx + rax + 8]
0020CC33  mov      byte ptr [rbx + rax + 0x190], 1
0020CC3B  mov      dword ptr [rbx + rax + 0x194], ebp
0020CC42  cmp      byte ptr [rdi + 0x18], bpl
0020CC46  je       0x20cc79  ; -> 0020CC79
0020CC48  lea      rcx, [rip + 0x1bf1481]  ; -> 01DFE0D0
0020CC4F  call     qword ptr [rip + 0x6b653b]  ; -> 008C3190 [u64 0x0000000001CCBFA6]
0020CC55  mov      rdx, rsi
0020CC58  mov      rcx, qword ptr [rax + 0x28]
0020CC5C  mov      rax, qword ptr [rcx]
0020CC5F  call     qword ptr [rax + 0x38]
0020CC62  lea      rcx, [rip + 0x1bf1467]  ; -> 01DFE0D0
0020CC69  call     qword ptr [rip + 0x6b6521]  ; -> 008C3190 [u64 0x0000000001CCBFA6]
0020CC6F  mov      rcx, qword ptr [rax + 0x28]
0020CC73  mov      rax, qword ptr [rcx]
0020CC76  call     qword ptr [rax + 0x50]
0020CC79  add      rbx, 0x198
0020CC80  cmp      rbx, 0x3c90
0020CC87  jl       0x20cc20  ; -> 0020CC20
0020CC89  mov      rsi, qword ptr [rsp + 0x30]
0020CC8E  mov      rbx, qword ptr [rsp + 0x38]
0020CC93  mov      rbp, qword ptr [rsp + 0x40]
0020CC98  add      rsp, 0x20
0020CC9C  pop      rdi
0020CC9D  ret      
```

## 0020CCA0 (23 B, extent 0020CCA0-0020CCB7)

Page context: "65C0', '00863280' and '008632B0', and '00316440' calls '00863280' and '008632B0'; the counter-object getter '0020CE00' is called only by '00863240', '00863280' and '008632B0', which call '0020CB50', '0020CCA0' and '0020CE60'; '008632B0' is also called by '00315E90'; the verbs '0034C9A0' and '00352250' call '00863240' and '008632B0'. The setter feeds the gil meter, the achievement checks read the header '+0x0C' walked-distance mirror (§1"

```
0020CCA0  movsxd   rax, edx
0020CCA3  imul     rdx, rax, 0x198
0020CCAA  mov      rax, qword ptr [rcx + 8]
0020CCAE  movzx    eax, byte ptr [rdx + rax + 0x190]
0020CCB6  ret      
```

## 002494A0 (65 B, extent 002494A0-002494E1)

Page context: "D0' (alloc triple '0036C1D0'/'0036A100'/'0036C140') | state cells the binder primes — the '022CBExx' band reuses the deque-alloc family | | leaves | '0017F9E0' ('001B5FB0'), '00229E30' ('01E02818'), '002494A0' ('02090790'/'02090910'), '0024A660' ('0208F580'), '00272470', '002800F0' ('0209AC60'), '0029CE40' ('00229E30'/'00229E40'/'0017F9E0'/'0039BB30'/'002B3550'/'00364950' — a small fan-out), '002DD4A0', '003C5E40' ('02B45A00'), '003CA2B"

```
002494A0  sub      rsp, 0x28
002494A4  cmp      qword ptr [rip + 0x1e460cc], 0  ; -> 0208F578
002494AC  jne      0x2494c9  ; -> 002494C9
002494AE  lea      rcx, [rip + 0x1e4745b]  ; -> 02090910
002494B5  xor      edx, edx
002494B7  mov      r8d, 0x780
002494BD  mov      qword ptr [rip + 0x1e460b4], rcx  ; -> 0208F578
002494C4  call     0x861ec0  ; -> 00861EC0 fn
002494C9  xor      edx, edx
002494CB  lea      rcx, [rip + 0x1e472be]  ; -> 02090790
002494D2  mov      r8d, 0x180
002494D8  add      rsp, 0x28
002494DC  jmp      0x861ec0  ; -> 00861EC0 fn
```

## 0024A660 (20 B, extent 0024A660-0024A674)

Page context: "00'/'0036C140') | state cells the binder primes — the '022CBExx' band reuses the deque-alloc family | | leaves | '0017F9E0' ('001B5FB0'), '00229E30' ('01E02818'), '002494A0' ('02090790'/'02090910'), '0024A660' ('0208F580'), '00272470', '002800F0' ('0209AC60'), '0029CE40' ('00229E30'/'00229E40'/'0017F9E0'/'0039BB30'/'002B3550'/'00364950' — a small fan-out), '002DD4A0', '003C5E40' ('02B45A00'), '003CA2B0' ('00244F00', '02B47758'), '003F30"

```
0024A660  xor      edx, edx
0024A662  lea      rcx, [rip + 0x1e44f17]  ; -> 0208F580
0024A669  mov      r8d, 0x1208
0024A66F  jmp      0x861ec0  ; -> 00861EC0 fn
```

## 00272470 (42 B, extent 00272470-0027249A)

Page context: "274840' ×2 + eight more, table '00290DF0'), '0028F8B0' (190 B — '0028F2F0' + '002B9FD0'/'00271420'/'00291750'/'00296260'/'00296240'/'004FE3C0'/'00244F00'), '00290430', '00291750' (144 B — '00271420'/'00272470'/'0028A080'/'0028CA30'/'002BE450'/'002BE0A0'/'003FA760'), '00274840' ('002446E0'/'002473B0'/'002482E0'), '002A79E0' ('0209C510'), '002B3550' ('008620A0'/'00254A10'/'0024ABC0', '0209D490'), '002BE450' ('00245000'/'00246AC0', table '"

```
00272470  xor      eax, eax
00272472  add      edx, ecx
00272474  mov      qword ptr [rcx], rax
00272477  mov      qword ptr [rcx + 0x10], rax
0027247B  mov      qword ptr [rcx + 0x18], rdx
0027247F  mov      eax, ecx
00272481  add      rax, 0x30
00272485  mov      edx, eax
00272487  mov      qword ptr [rcx + 0x20], rax
0027248B  and      edx, 0xf
0027248E  je       0x272499  ; -> 00272499
00272490  sub      eax, edx
00272492  add      eax, 0x10
00272495  mov      qword ptr [rcx + 0x20], rax
00272499  ret      
```

## 00274840 (40 B, extent 00274840-00274868)

Page context: "–'5C') | the '0x7E00'-byte pool the party page describes; the five-×-five call shape is five parallel sub-pool inits | | '0209BE80' block family | '0028F2F0' (629 B — '00273B40' ×4 + '003697F0' ×3 + '00274840' ×2 + eight more, table '00290DF0'), '0028F8B0' (190 B — '0028F2F0' + '002B9FD0'/'00271420'/'00291750'/'00296260'/'00296240'/'004FE3C0'/'00244F00'), '00290430', '00291750' (144 B — '00271420'/'00272470'/'0028A080'/'0028CA30'/'002BE"

```
00274840  test     rcx, rcx
00274843  je       0x274867  ; -> 00274867
00274845  push     rbx
00274846  sub      rsp, 0x20
0027484A  mov      rbx, rcx
0027484D  call     0x2446e0  ; -> 002446E0 fn
00274852  mov      rcx, rbx
00274855  call     0x2473b0  ; -> 002473B0 fn
0027485A  mov      rcx, rbx
0027485D  call     0x2482e0  ; -> 002482E0 fn
00274862  add      rsp, 0x20
00274866  pop      rbx
00274867  ret      
```

## 002800F0 (38 B, extent 002800F0-00280116)

Page context: "der primes — the '022CBExx' band reuses the deque-alloc family | | leaves | '0017F9E0' ('001B5FB0'), '00229E30' ('01E02818'), '002494A0' ('02090790'/'02090910'), '0024A660' ('0208F580'), '00272470', '002800F0' ('0209AC60'), '0029CE40' ('00229E30'/'00229E40'/'0017F9E0'/'0039BB30'/'002B3550'/'00364950' — a small fan-out), '002DD4A0', '003C5E40' ('02B45A00'), '003CA2B0' ('00244F00', '02B47758'), '003F30A0' ('call rdi' thunk), '003FA760' ('"

```
002800F0  cmp      qword ptr [rip + 0x1e1ab38], 0  ; -> 0209AC30
002800F8  jne      0x280115  ; -> 00280115
002800FA  lea      rcx, [rip + 0x1e1ab5f]  ; -> 0209AC60
00280101  xor      edx, edx
00280103  mov      r8d, 0xe00
00280109  mov      qword ptr [rip + 0x1e1ab20], rcx  ; -> 0209AC30
00280110  jmp      0x861ec0  ; -> 00861EC0 fn
00280115  ret      
```

## 00290430 (19 B, extent 00290430-00290443)

Page context: "629 B — '00273B40' ×4 + '003697F0' ×3 + '00274840' ×2 + eight more, table '00290DF0'), '0028F8B0' (190 B — '0028F2F0' + '002B9FD0'/'00271420'/'00291750'/'00296260'/'00296240'/'004FE3C0'/'00244F00'), '00290430', '00291750' (144 B — '00271420'/'00272470'/'0028A080'/'0028CA30'/'002BE450'/'002BE0A0'/'003FA760'), '00274840' ('002446E0'/'002473B0'/'002482E0'), '002A79E0' ('0209C510'), '002B3550' ('008620A0'/'00254A10'/'0024ABC0', '0209D490'),"

```
00290430  mov      rax, qword ptr [rip + 0x1e0ba49]  ; -> 0209BE80
00290437  test     rax, rax
0029043A  je       0x290442  ; -> 00290442
0029043C  mov      dword ptr [rax + 0xaa44], ecx
00290442  ret      
```

## 00290DF0 (28 B, extent 00290DF0-00290E0C)

Page context: "e party page describes; the five-×-five call shape is five parallel sub-pool inits | | '0209BE80' block family | '0028F2F0' (629 B — '00273B40' ×4 + '003697F0' ×3 + '00274840' ×2 + eight more, table '00290DF0'), '0028F8B0' (190 B — '0028F2F0' + '002B9FD0'/'00271420'/'00291750'/'00296260'/'00296240'/'004FE3C0'/'00244F00'), '00290430', '00291750' (144 B — '00271420'/'00272470'/'0028A080'/'0028CA30'/'002BE450'/'002BE0A0'/'003FA760'), '0027"

```
00290DF0  test     rcx, rcx
00290DF3  je       0x290e0b  ; -> 00290E0B
00290DF5  mov      rdx, rcx
00290DF8  mov      rcx, qword ptr [rip + 0x1e0b081]  ; -> 0209BE80
00290DFF  mov      rcx, qword ptr [rcx + 0x10fc0]
00290E06  jmp      0x273b40  ; -> 00273B40 fn
00290E0B  ret      
```

## 002BE490 (88 B, extent 002BE490-002BE4E8)

Page context: "0'/'002BE0A0'/'003FA760'), '00274840' ('002446E0'/'002473B0'/'002482E0'), '002A79E0' ('0209C510'), '002B3550' ('008620A0'/'00254A10'/'0024ABC0', '0209D490'), '002BE450' ('00245000'/'00246AC0', table '002BE490') | the second '0209BE80' accessor family in this census (the '002778C0' battle-menu subtree has its own band) — here serving the binder's UI-facing side | | '022Cxxxx'/'022CAxxx' cells | '0035C560' (68 B — '0028F8B0'/'00253480'/'0"

```
002BE490  push     rbx
002BE492  sub      rsp, 0x20
002BE496  cmp      dword ptr [rdx], 2
002BE499  mov      rbx, rcx
002BE49C  je       0x2be4a8  ; -> 002BE4A8
002BE49E  add      rsp, 0x20
002BE4A2  pop      rbx
002BE4A3  jmp      0x5c5230  ; -> 005C5230 fn
002BE4A8  mov      ecx, dword ptr [rcx + 0xb4]
002BE4AE  call     0x1edec0  ; -> 001EDEC0 fn
002BE4B3  test     eax, eax
002BE4B5  je       0x2be4d4  ; -> 002BE4D4
002BE4B7  movzx    edx, word ptr [rbx + 0x10f8]
002BE4BE  mov      rcx, rbx
002BE4C1  call     0x2bf4f0  ; -> 002BF4F0 fn
002BE4C6  cmp      eax, 1
002BE4C9  jne      0x2be4d4  ; -> 002BE4D4
002BE4CB  xor      eax, eax
002BE4CD  mov      word ptr [rbx + 0x10f8], ax
002BE4D4  lea      rcx, [rbx + 0xac0]
002BE4DB  call     0x2be290  ; -> 002BE290 fn
002BE4E0  xor      eax, eax
002BE4E2  add      rsp, 0x20
002BE4E6  pop      rbx
002BE4E7  ret      
```

## 00300500 (28 B, extent 00300500-0030051C)

Page context: " '003112F0' 'BattleFormula_ApplyTargetResult' | CombatFormula | gil changed by an action's result on a target | | '003004B0' 'GameState_AddGilClampedAndNotify' | Rewards | a relative-add wrapper | | '00300500' 'GameState_SetGilClampedNonnegative' | Rewards | an absolute-set wrapper | | '003F4AA0' | Rewards | reward-bundle record applier (§13a); sole feeder '00290130', ~~statically orphaned~~ **reached from script verb '037C questresultw"

```
00300500  push     rbx
00300502  sub      rsp, 0x20
00300506  xor      ebx, ebx
00300508  test     ecx, ecx
0030050A  cmovns   ebx, ecx
0030050D  mov      ecx, ebx
0030050F  call     0x254ee0  ; -> 00254EE0 fn
00300514  mov      eax, ebx
00300516  add      rsp, 0x20
0030051A  pop      rbx
0030051B  ret      
```

## 0034C9A0 (50 B, extent 0034C9A0-0034C9D2)

Page context: "'0020CE00()' (singleton '01F84450'), which has exactly three callers — '00863240'/'00863280'/'008632B0' — and every body calling that accessor family ('00315FDA', '003162E0', '00316440', '00316A63', '0034C9A0', '00352250') is disjoint from all ~~21~~ 22 bodies calling 'GameState_GetGil' or its thunk *(corrected 2026-10-02, OPUS: 19 direct and 3 through '00309BF0', §4's census and CONTRACT-gil-storage-and-movement.md GL-5)*. Metered tota"

```
0034C9A0  push     rbx
0034C9A2  sub      rsp, 0x20
0034C9A6  mov      rcx, r9
0034C9A9  call     0x267e10  ; -> 00267E10 fn
0034C9AE  mov      ebx, eax
0034C9B0  call     0x2640c0  ; -> 002640C0 fn
0034C9B5  mov      ecx, dword ptr [rax + 0x28]
0034C9B8  call     0x32f240  ; -> 0032F240 fn
0034C9BD  mov      edx, ebx
0034C9BF  mov      ecx, eax
0034C9C1  call     0x863240  ; -> 00863240 fn
0034C9C6  mov      ecx, ebx
0034C9C8  add      rsp, 0x20
0034C9CC  pop      rbx
0034C9CD  jmp      0x26b750  ; -> 0026B750 fn
```

## 0035C560 (68 B, extent 0035C560-0035C5A4)

Page context: " '002BE490') | the second '0209BE80' accessor family in this census (the '002778C0' battle-menu subtree has its own band) — here serving the binder's UI-facing side | | '022Cxxxx'/'022CAxxx' cells | '0035C560' (68 B — '0028F8B0'/'00253480'/'00290430'/'003C5E40', '022C8060'), '0035FF60' ('022CAE95'), '00364950' ('003658F0', '022CBBB0'), '003658F0' ('0032E400'/'004745D0'/'0032E620', '022CBE00'), '00365DD0' ('004745D0', '022CBE00'), '00368"

```
0035C560  sub      rsp, 0x28
0035C564  xor      edx, edx
0035C566  lea      rcx, [rip + 0x1f6baf3]  ; -> 022C8060
0035C56D  mov      r8d, 0x23c8
0035C573  call     0x861ec0  ; -> 00861EC0 fn
0035C578  or       dword ptr [rip + 0x1f6be69], 0x20  ; -> 022C83E8
0035C57F  call     0x28f8b0  ; -> 0028F8B0 fn
0035C584  call     0x253480  ; -> 00253480 fn
0035C589  mov      ecx, 1
0035C58E  call     0x290430  ; -> 00290430 fn
0035C593  call     0x3c5e40  ; -> 003C5E40 fn
0035C598  mov      qword ptr [rip + 0x1f6be19], rax  ; -> 022C83B8
0035C59F  add      rsp, 0x28
0035C5A3  ret      
```

## 00365DD0 (115 B, extent 00365DD0-00365E43)

Page context: " '0035C560' (68 B — '0028F8B0'/'00253480'/'00290430'/'003C5E40', '022C8060'), '0035FF60' ('022CAE95'), '00364950' ('003658F0', '022CBBB0'), '003658F0' ('0032E400'/'004745D0'/'0032E620', '022CBE00'), '00365DD0' ('004745D0', '022CBE00'), '00368270' ('022CBE30'), '0039BB30' ('02AEE810'), '0039C3F0' ('0032E400'/'003EFCD0'/'0032E620'), '003EFCD0' (alloc triple '0036C1D0'/'0036A100'/'0036C140') | state cells the binder primes — the '022CBExx'"

```
00365DD0  sub      rsp, 0x28
00365DD4  mov      ecx, 0xa00
00365DD9  call     0x4745d0  ; -> 004745D0 fn
00365DDE  mov      r8d, 0x40
00365DE4  xor      r9d, r9d
00365DE7  lea      rcx, [rax + 0x28]
00365DEB  nop      dword ptr [rax + rax]
00365DF0  lea      rdx, [rcx - 0x50]
00365DF4  mov      qword ptr [rcx - 0x20], rcx
00365DF8  mov      qword ptr [rcx - 0x28], rdx
00365DFC  mov      dword ptr [rcx - 0x18], 0xff0000
00365E03  mov      qword ptr [rcx - 8], r9
00365E07  mov      qword ptr [rcx - 0x10], r9
00365E0B  add      rcx, 0x28
00365E0F  sub      r8, 1
00365E13  jne      0x365df0  ; -> 00365DF0
00365E15  mov      rcx, qword ptr [rip + 0x1f65fe4]  ; -> 022CBE00
00365E1C  mov      qword ptr [rcx + 0x220], rax
00365E23  mov      qword ptr [rcx + 0x228], rax
00365E2A  mov      qword ptr [rax], r9
00365E2D  add      rax, 0x9d8
00365E33  mov      qword ptr [rcx + 0x230], rax
00365E3A  mov      qword ptr [rax + 8], r9
00365E3E  add      rsp, 0x28
00365E42  ret      
```

## 0039BB30 (33 B, extent 0039BB30-0039BB51)

Page context: "', '022C8060'), '0035FF60' ('022CAE95'), '00364950' ('003658F0', '022CBBB0'), '003658F0' ('0032E400'/'004745D0'/'0032E620', '022CBE00'), '00365DD0' ('004745D0', '022CBE00'), '00368270' ('022CBE30'), '0039BB30' ('02AEE810'), '0039C3F0' ('0032E400'/'003EFCD0'/'0032E620'), '003EFCD0' (alloc triple '0036C1D0'/'0036A100'/'0036C140') | state cells the binder primes — the '022CBExx' band reuses the deque-alloc family | | leaves | '0017F9E0' ('"

```
0039BB30  sub      rsp, 0x28
0039BB34  xor      edx, edx
0039BB36  lea      rcx, [rip + 0x2752cd3]  ; -> 02AEE810
0039BB3D  mov      r8d, 0xf0
0039BB43  call     0x861ec0  ; -> 00861EC0 fn
0039BB48  add      rsp, 0x28
0039BB4C  jmp      0x39c3f0  ; -> 0039C3F0 fn
```

## 003F30A0 (48 B, extent 003F30A0-003F30D0)

Page context: ", '002800F0' ('0209AC60'), '0029CE40' ('00229E30'/'00229E40'/'0017F9E0'/'0039BB30'/'002B3550'/'00364950' — a small fan-out), '002DD4A0', '003C5E40' ('02B45A00'), '003CA2B0' ('00244F00', '02B47758'), '003F30A0' ('call rdi' thunk), '003FA760' ('00275550'), '008620A0' | small reads and thunks |  The shape matches the binder's role: one pool allocator, the '0209BE80' block family, and two dozen cell writes — a save-slot bind is a publish st"

```
003F30A0  test     rcx, rcx
003F30A3  je       0x3f30cf  ; -> 003F30CF
003F30A5  push     rdi
003F30A6  sub      rsp, 0x20
003F30AA  mov      rdi, rdx
003F30AD  mov      qword ptr [rsp + 0x30], rbx
003F30B2  mov      rbx, qword ptr [rcx + 0x70]
003F30B6  test     rdi, rdi
003F30B9  je       0x3f30bd  ; -> 003F30BD
003F30BB  call     rdi
003F30BD  mov      rcx, rbx
003F30C0  test     rbx, rbx
003F30C3  jne      0x3f30b2  ; -> 003F30B2
003F30C5  mov      rbx, qword ptr [rsp + 0x30]
003F30CA  add      rsp, 0x20
003F30CE  pop      rdi
003F30CF  ret      
```

## 003F4BD0 (92 B, extent 003F4BD0-003F4C2C)

Page context: "24' and tail-jumping to '003F4C30') fetches the bundle — '003F4C30' resolves a keyed record through '0030AAC0'/'0030AEA0' into the gil amount plus the two item lists — then '003F4AA0' applies it and '003F4BD0' posts message '0x100' through '00244F50' with the record's key. ~~'00290130' itself has **zero routes of every form**: no 'call'/'jmp' edge, no 'lea' or immediate materialisation, no qword slot in any data section, and the only RV"

```
003F4BD0  mov      r11, rsp
003F4BD3  sub      rsp, 0x68
003F4BD7  mov      rax, qword ptr [rip + 0x1b4fc52]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003F4BDE  xor      rax, rsp
003F4BE1  mov      qword ptr [rsp + 0x50], rax
003F4BE6  xor      r8d, r8d
003F4BE9  mov      qword ptr [r11 - 0x40], rdx
003F4BED  mov      byte ptr [r11 - 0x48], r8b
003F4BF1  lea      rax, [r11 - 0x48]
003F4BF5  mov      dword ptr [rsp + 0x30], ecx
003F4BF9  lea      rdx, [rip + 0x270]  ; -> 003F4E70
003F4C00  mov      dword ptr [r11 - 0x30], r8d
003F4C04  mov      ecx, 0x100
003F4C09  mov      qword ptr [r11 - 0x20], r8
003F4C0D  lea      r8, [r11 - 0x30]
003F4C11  mov      qword ptr [r11 - 0x28], rax
003F4C15  call     0x244f50  ; -> 00244F50 fn
003F4C1A  mov      rcx, qword ptr [rsp + 0x50]
003F4C1F  xor      rcx, rsp
003F4C22  call     0x808c40  ; -> 00808C40 fn
003F4C27  add      rsp, 0x68
003F4C2B  ret      
```

## 003FA760 (35 B, extent 003FA760-003FA783)

Page context: "(190 B — '0028F2F0' + '002B9FD0'/'00271420'/'00291750'/'00296260'/'00296240'/'004FE3C0'/'00244F00'), '00290430', '00291750' (144 B — '00271420'/'00272470'/'0028A080'/'0028CA30'/'002BE450'/'002BE0A0'/'003FA760'), '00274840' ('002446E0'/'002473B0'/'002482E0'), '002A79E0' ('0209C510'), '002B3550' ('008620A0'/'00254A10'/'0024ABC0', '0209D490'), '002BE450' ('00245000'/'00246AC0', table '002BE490') | the second '0209BE80' accessor family in t"

```
003FA760  push     rbx
003FA762  sub      rsp, 0x20
003FA766  mov      edx, 0x26c0
003FA76B  mov      rbx, rcx
003FA76E  call     0x275550  ; -> 00275550 fn
003FA773  or       eax, 0xffffffff
003FA776  mov      word ptr [rbx + 0x249a], ax
003FA77D  add      rsp, 0x20
003FA781  pop      rbx
003FA782  ret      
```

## 00863240 (53 B, extent 00863240-00863275)

Page context: "s bounds §10's last question: **no consumer reconciles the meter against the balance.** The meter's counter records live behind '0020CE00()' (singleton '01F84450'), which has exactly three callers — '00863240'/'00863280'/'008632B0' — and every body calling that accessor family ('00315FDA', '003162E0', '00316440', '00316A63', '0034C9A0', '00352250') is disjoint from all ~~21~~ 22 bodies calling 'GameState_GetGil' or its thunk *(corrected"

```
00863240  mov      qword ptr [rsp + 8], rbx
00863245  push     rdi
00863246  sub      rsp, 0x20
0086324A  mov      ebx, edx
0086324C  mov      edi, ecx
0086324E  call     0x20ce00  ; -> 0020CE00 fn
00863253  test     rax, rax
00863256  je       0x86326a  ; -> 0086326A
00863258  call     0x20ce00  ; -> 0020CE00 fn
0086325D  mov      rcx, rax
00863260  mov      r8d, ebx
00863263  mov      edx, edi
00863265  call     0x20cb50  ; -> 0020CB50 fn
0086326A  mov      rbx, qword ptr [rsp + 0x30]
0086326F  add      rsp, 0x20
00863273  pop      rdi
00863274  ret      
```
