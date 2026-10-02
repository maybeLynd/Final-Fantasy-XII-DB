# F-interior pack: `12-Items-Equipment-Shops-License/CONTRACT-bazaar-unlock-and-purchase.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-bazaar-unlock-and-purchase.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: c9b951983	EC7 pass-22 debt: crossing-section dispositions - 527 pairs / 65 pages (FRONTIER-REQ-SWE2-EC7-PASS22). OPUS read these before packing.

## 00238640 (19 B, extent 00238640-00238653)

Page context: " '00273E30', '002BFD20', '0035D380' - shared machinery across the layer boundary, no shared ownership. - **World - CLIENT and SERVICE (3 edges).** '003845F0' is also called by bodies filed to World: '00238640' (Area), '003847B0' (Area); '00236C30' reaches bodies filed to World: '003847B0' (Area) - shared machinery across the layer boundary, no shared ownership. - **WorldAreaField - CLIENT and SERVICE (9 edges).** '00236C30' is also call"

```
00238640  movsxd   rax, ecx
00238643  lea      rcx, [rip + 0x2d5ed76]  ; -> 02F973C0
0023864A  lea      rcx, [rcx + rax*8]
0023864E  jmp      0x3845f0  ; -> 003845F0 fn
```

## 002524C0 (60 B, extent 002524C0-002524FC)

Page context: " (194 B) is the gil-commit step '0056D370' runs on a purchase: gated on '0209C4C8' live and '+0xF4'/'+0xC0 & 3' clear, it flags '+0xF3' when '+0xEC + ecx' would exceed '0x5F5E0FF' (99,999,999), then '002524C0' applies - success commits '+0xC4 = +0xEC', '+0xC8' = result, '+0xC0' = '(... & ~0x3E) | 1', '+0xCC = 0x15', '+0xD0' = tick '0208F570'; failure leaves '+0xF2 = 2'  Interior anchor '002A1E3B' (function '002A1DC0'). - **Input - CLIEN"

```
002524C0  mov      r9d, edx
002524C3  mov      r8d, ecx
002524C6  cmp      ecx, 0x5f5e0ff
002524CC  jle      0x2524d4  ; -> 002524D4
002524CE  mov      eax, 0x5f5e0ff
002524D3  ret      
002524D4  test     r8d, r8d
002524D7  jns      0x2524dc  ; -> 002524DC
002524D9  xor      eax, eax
002524DB  ret      
002524DC  lea      eax, [rcx + rdx]
002524DF  mov      edx, r8d
002524E2  test     eax, eax
002524E4  mov      eax, 0x5f5e0ff
002524E9  cmovns   edx, r9d
002524ED  sub      eax, r8d
002524F0  add      ecx, edx
002524F2  cmp      ecx, 0x5f5e0ff
002524F8  cmovle   eax, edx
002524FB  ret      
```

## 002535D0 (189 B, extent 002535D0-0025368D)

Page context: "ImageAddress_ResolveRuntimePointer'.  '00325F40' (239 B) is the recipe/class indirection '002FD150' runs: '00322C50' fetch gates the body; the '(esi, ebx)' pair picks between handlers '00252E60' and '002535D0'; a u16 id whose top nibble is 1 takes the '02EBF0F8' row-byte lookup '(id-0x1000)*[+8] + resolved[+0x9]'; other kinds '<=0xA' fetch through the '01EED1B0[kind*2]' pointer table - both paths converge on the row fetch  Interior anch"

```
002535D0  mov      qword ptr [rsp + 8], rbx
002535D5  mov      qword ptr [rsp + 0x10], rbp
002535DA  mov      qword ptr [rsp + 0x18], rsi
002535DF  mov      qword ptr [rsp + 0x20], rdi
002535E4  push     r14
002535E6  sub      rsp, 0x20
002535EA  xor      ebx, ebx
002535EC  mov      edi, edx
002535EE  mov      esi, ecx
002535F0  mov      eax, ecx
002535F2  cmp      ecx, 0xb
002535F5  jbe      0x253603  ; -> 00253603
002535F7  mov      ecx, 0x200
002535FC  call     0x16d6a0  ; -> 0016D6A0 fn
00253601  mov      eax, ebx
00253603  cdqe     
00253605  lea      rdx, [rip + 0x1e3f154]  ; -> 02092760
0025360C  lea      rbp, [rdx + rax*8]
00253610  mov      eax, esi
00253612  cmp      esi, 0xb
00253615  jbe      0x253623  ; -> 00253623
00253617  mov      ecx, 0x200
0025361C  call     0x16d6a0  ; -> 0016D6A0 fn
00253621  mov      eax, ebx
00253623  movsxd   rdx, eax
00253626  mov      rax, qword ptr [rip + 0x1e3f193]  ; -> 020927C0
0025362D  lea      r14, [rax + rdx*4]
00253631  test     rbp, rbp
00253634  je       0x253672  ; -> 00253672
00253636  mov      ecx, dword ptr [rbp + 4]
00253639  call     0x20e600  ; -> 0020E600 fn
0025363E  mov      edx, dword ptr [r14 + 0x47b8]
00253645  shr      edi, 0x10
00253648  test     edx, edx
0025364A  jle      0x253672  ; -> 00253672
0025364C  nop      dword ptr [rax]
00253650  movzx    ecx, word ptr [rax]
00253653  cmp      ecx, edi
00253655  je       0x253663  ; -> 00253663
00253657  inc      ebx
00253659  add      rax, 2
0025365D  cmp      ebx, edx
0025365F  jl       0x253650  ; -> 00253650
00253661  jmp      0x253672  ; -> 00253672
00253663  mov      ecx, 0xffff
00253668  mov      word ptr [rax], cx
0025366B  mov      ecx, esi
0025366D  call     0x2534c0  ; -> 002534C0 fn
00253672  mov      rbx, qword ptr [rsp + 0x30]
00253677  mov      rbp, qword ptr [rsp + 0x38]
0025367C  mov      rsi, qword ptr [rsp + 0x40]
00253681  mov      rdi, qword ptr [rsp + 0x48]
00253686  add      rsp, 0x20
0025368A  pop      r14
0025368C  ret      
```

## 0032AB50 (14 B, extent 0032AB50-0032AB5E)

Page context: "30B1D0', which is '0x50' into the body: past the prologue, past the gate and past the state-pointer setup. Corrected 2026-09-12 by execution | | script-set availability | '0030B570', reached through '0032AB50(good, bool)' | | zero a loot tally | '003008A0(loot, 0, absolute = 1, 3)' |  ## 3. Types  | | | |---|---| | the goods table | registry slot '02EBF058'; row index is **'id - 0xD000'** ('0030B1F4'), the category-13 base | | the good'"

```
0032AB50  mov      eax, edx
0032AB52  xor      edx, edx
0032AB54  test     eax, eax
0032AB56  setne    dl
0032AB59  jmp      0x30b570  ; -> 0030B570 fn
```
