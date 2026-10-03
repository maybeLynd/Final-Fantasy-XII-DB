# F-interior pack: `15-Input/Modal-Toggles/r2-force-fight-toggle.md`

Generated 2026-10-02 20:44 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/r2-force-fight-toggle.json`.

Functions: 6. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: cd6bd7f58	SWE2-DATA consolidated publish: progress-report cluster (generation store, R3 semantics, DB_GOAL, me; d0fd168a2	SWE2-DATA: batch-5 review corrections (clamping page's .data vf00 cell restored, SD-190 gate on the ; inbox mentions: FABLE.md, repos-2d.md). OPUS read these before packing.

## 0028E5F0 (59 B, extent 0028E5F0-0028E62B)

Page context: "sets the counter; '00366940' resets the counter; '003667B0(n)' sets or clears bit 7; '003669D0' (UI) returns '0' / '1' / '2' for off / arming / engaged and has seven readers ('00253C70', '00273950', '0028E5F0', '002C64C0', '0035D660', '003C87B0', '003C8B70') — the 'FLEEING' label's driver ~~is among them or behind the flag, not read here~~ (**FM-1**). *(Corrected 2026-09-30, SWE2-DATA: FM-1 was answered on 2026-09-25 in §7 — the label i"

```
0028E5F0  sub      rsp, 0x28
0028E5F4  call     0x3669d0  ; -> 003669D0 fn
0028E5F9  xor      r9d, r9d
0028E5FC  dec      eax
0028E5FE  mov      r8d, r9d
0028E601  cmp      eax, 1
0028E604  mov      ecx, 2
0028E609  setbe    r8b
0028E60D  test     r8d, r8d
0028E610  cmovne   ecx, r9d
0028E614  lea      edx, [r8 + r8]
0028E618  call     0x35c880  ; -> 0035C880 fn
0028E61D  call     0x366990  ; -> 00366990 fn
0028E622  add      rsp, 0x28
0028E626  jmp      0x2970c0  ; -> 002970C0 fn
```

## 00354EF0 (38 B, extent 00354EF0-00354F16)

Page context: "ytes.** '003603D0' sets '+0xA'; it is reached through a 5-byte thunk in the script-verb range. '003603E0' sets '+0xB'; its callers are the UI request router's destination-'0xC' route, '00280140' and '00354EF0'.       - **Per-frame check.** '00360120', run by the field frame and mode 5, checks the block. While '+0' is 0 and either request byte is set, it runs '003601D0', the screen-fade page's skip-family handler. That handler stops soun"

```
00354EF0  sub      rsp, 0x28
00354EF4  call     0x363560  ; -> 00363560 fn
00354EF9  call     0x360d70  ; -> 00360D70 fn
00354EFE  call     0x2dee70  ; -> 002DEE70 fn
00354F03  mov      ecx, 2
00354F08  call     0x249ca0  ; -> 00249CA0 fn
00354F0D  add      rsp, 0x28
00354F11  jmp      0x3603e0  ; -> 003603E0 fn
```

## 0035C880 (17 B, extent 0035C880-0035C891)

Page context: "FieldData_GetActiveFieldRecordBit15' | 78 B | the area pin *(ledger name)* | | '00366870' / '003667E0' | repeating-sound acquire / release | 196 / 135 B | driven by the toggle state | | '0035C6F0' / '0035C880' | mode-register read / masked write | 7 / 17 B | '022C83EC' | | '0035BC50' | battle-menu list build | 1,014 B | runs only when register bit 0 is clear | | '00266D10' | field/area initialisation | 1,185 B | sets both enable bytes |"

```
0035C880  not      ecx
0035C882  and      ecx, dword ptr [rip + 0x1f6bb64]  ; -> 022C83EC
0035C888  or       ecx, edx
0035C88A  mov      dword ptr [rip + 0x1f6bb5c], ecx  ; -> 022C83EC
0035C890  ret      
```

## 003667B0 (42 B, extent 003667B0-003667DA)

Page context: "driver remain unmeasured ('FM-1').  The word's other clients: '00366960(n)' sets the engaged state directly (counter = threshold, word = '0x25') or resets the counter; '00366940' resets the counter; '003667B0(n)' sets or clears bit 7; '003669D0' (UI) returns '0' / '1' / '2' for off / arming / engaged and has seven readers ('00253C70', '00273950', '0028E5F0', '002C64C0', '0035D660', '003C87B0', '003C8B70') — the 'FLEEING' label's driver "

```
003667B0  movzx    eax, word ptr [rip + 0x1f65663]  ; -> 022CBE1A
003667B7  mov      edx, 0xff7f
003667BC  and      ax, dx
003667BF  mov      word ptr [rip + 0x1f65654], ax  ; -> 022CBE1A
003667C6  test     ecx, ecx
003667C8  je       0x3667d9  ; -> 003667D9
003667CA  mov      ecx, 0x80
003667CF  or       ax, cx
003667D2  mov      word ptr [rip + 0x1f65641], ax  ; -> 022CBE1A
003667D9  ret      
```

## 003667E0 (135 B, extent 003667E0-00366867)

Page context: "ced off */ apply: if (DAT_020927CC == 1) { state = 0; flag = 1; } /* ... register transitions on DAT_022C83EC bits 2-3 ... */ if (FUN_003603B0() == 0 && FUN_003603C0() == 0) {     if (state == 0) FUN_003667E0();            /* release the repeating sound */     else            FUN_00366870();            /* acquire bank-local sound index 0x52, advance counter */ } FUN_00252C80(state, flag); '''  So the toggle is overridden by **capability"

```
003667E0  sub      rsp, 0x28
003667E4  call     0x35c6f0  ; -> 0035C6F0 fn
003667E9  test     al, 1
003667EB  jne      0x366862  ; -> 00366862
003667ED  test     byte ptr [rip + 0x1f65626], 4  ; -> 022CBE1A
003667F4  je       0x366812  ; -> 00366812
003667F6  call     0x265680  ; -> 00265680 fn
003667FB  test     eax, eax
003667FD  je       0x366812  ; -> 00366812
003667FF  test     byte ptr [rip + 0x1f65614], 0x40  ; -> 022CBE1A
00366806  jne      0x366812  ; -> 00366812
00366808  mov      ecx, 0x2a
0036680D  call     0x249c60  ; -> 00249C60 fn
00366812  test     byte ptr [rip + 0x1f65601], 0x10  ; -> 022CBE1A
00366819  je       0x366848  ; -> 00366848
0036681B  mov      ecx, dword ptr [rip + 0x1f655fb]  ; -> 022CBE1C
00366821  call     0x2dee80  ; -> 002DEE80 fn
00366826  test     eax, eax
00366828  je       0x366837  ; -> 00366837
0036682A  mov      ecx, dword ptr [rip + 0x1f655ec]  ; -> 022CBE1C
00366830  xor      edx, edx
00366832  call     0x2df0f0  ; -> 002DF0F0 fn
00366837  movzx    eax, word ptr [rip + 0x1f655dc]  ; -> 022CBE1A
0036683E  mov      ecx, 0xffef
00366843  and      ax, cx
00366846  jmp      0x36684f  ; -> 0036684F
00366848  movzx    eax, word ptr [rip + 0x1f655cb]  ; -> 022CBE1A
0036684F  mov      ecx, 0xff92
00366854  and      ax, cx
00366857  or       ax, 2
0036685B  mov      word ptr [rip + 0x1f655b8], ax  ; -> 022CBE1A
00366862  add      rsp, 0x28
00366866  ret      
```

## 00366960 (43 B, extent 00366960-0036698B)

Page context: " bits, not the counter. That is the progression §2g predicts, at sample precision; instruction ordering inside the frame and the label's driver remain unmeasured ('FM-1').  The word's other clients: '00366960(n)' sets the engaged state directly (counter = threshold, word = '0x25') or resets the counter; '00366940' resets the counter; '003667B0(n)' sets or clears bit 7; '003669D0' (UI) returns '0' / '1' / '2' for off / arming / engaged a"

```
00366960  test     ecx, ecx
00366962  je       0x36697f  ; -> 0036697F
00366964  movzx    eax, word ptr [rip + 0x1f6549d]  ; -> 022CBE08
0036696B  mov      word ptr [rip + 0x1f654a6], ax  ; -> 022CBE18
00366972  mov      eax, 0x25
00366977  mov      word ptr [rip + 0x1f6549c], ax  ; -> 022CBE1A
0036697E  ret      
0036697F  mov      qword ptr [rip + 0x1f6548e], 0  ; -> 022CBE18
0036698A  ret      
```
