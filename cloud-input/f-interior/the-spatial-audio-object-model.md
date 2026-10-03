# F-interior pack: `18-Audio/the-spatial-audio-object-model.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-spatial-audio-object-model.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

## 001A7600 (41 B, extent 001A7600-001A7629)

Page context: "0320' measured  '00180320' (70 B) is the flag-forwarding poke '002F4520' and '002F5550' run: a live '001A9930()' object is required, then 'byte[00189120() + 0x1C]' is read as a boolean and passed to '001A7600(obj, flag, ecx)' as the middle argument - the second singleton's flag byte gates the first's call. Interior anchor '0018035B' (the '001A7600' tail). "

```
001A7600  mov      r9, qword ptr [rcx + 0x88]
001A7607  test     r9, r9
001A760A  je       0x1a7626  ; -> 001A7626
001A760C  test     r8d, r8d
001A760F  js       0x1a7626  ; -> 001A7626
001A7611  cmp      r8d, dword ptr [rcx + 0x20]
001A7615  jge      0x1a7626  ; -> 001A7626
001A7617  movsxd   r8, r8d
001A761A  movsxd   rcx, edx
001A761D  lea      rax, [rcx + r8*2]
001A7621  mov      rax, qword ptr [r9 + rax*8]
001A7625  ret      
001A7626  xor      eax, eax
001A7628  ret      
```

## 001DBE00 (58 B, extent 001DBE00-001DBE3A)

Page context: "te (2026-09-19) - '002DEFA0' + '002DEF40' gated audio tails measured  '002DEFA0' (104 B) is the '003603C0'-gated two-call chain: the gate failing returns 0; otherwise '002DE800(rsi, rdi)' runs, then '001DBE00' tails with 'ecx = !(ecx >> 31)', 'edx = ecx & 0x7FFFFFFF', 'r8 = 0215E710' - the sign-bit split the audio bodies share. Interior anchor '002DEFD8' (the '002DE800' call).  '002DEF40' (95 B) is the sibling repack: same '003603C0' ga"

```
001DBE00  mov      qword ptr [rsp + 8], rbx
001DBE05  mov      qword ptr [rsp + 0x10], rsi
001DBE0A  push     rdi
001DBE0B  sub      rsp, 0x20
001DBE0F  mov      rbx, r8
001DBE12  mov      edi, edx
001DBE14  mov      esi, ecx
001DBE16  call     0x210b30  ; -> 00210B30 fn
001DBE1B  mov      rcx, rax
001DBE1E  mov      r9, rbx
001DBE21  mov      r8d, edi
001DBE24  mov      edx, esi
001DBE26  mov      rbx, qword ptr [rsp + 0x30]
001DBE2B  mov      rsi, qword ptr [rsp + 0x38]
001DBE30  add      rsp, 0x20
001DBE34  pop      rdi
001DBE35  jmp      0x210be0  ; -> 00210BE0 fn
```

## 00223EB0 (35 B, extent 00223EB0-00223ED3)

Page context: "' and vertices   '+0x28' at 16 bytes each ('00221A7B'–'00221AA4'). The descriptor reaches the builder as   'AudioBank_StartVoice''s sixth argument (null through the wrapper '00224540'; supplied by   '00223EB0' ← '0021B200') or '00224E40''s fourth (← '0021C760' ← '00211200'); the stream side   passes null. **No instruction in the image stores the kind 5 as an immediate**, so polygon   descriptors are copied from data or assembled through"

```
00223EB0  sub      rsp, 0x48
00223EB4  mov      qword ptr [rsp + 0x30], r9
00223EB9  xor      r9d, r9d
00223EBC  mov      byte ptr [rsp + 0x28], 1
00223EC1  mov      dword ptr [rsp + 0x20], 0
00223EC9  call     0x224570  ; -> 00224570 fn
00223ECE  add      rsp, 0x48
00223ED2  ret      
```

## 0026E5D0 (31 B, extent 0026E5D0-0026E5EF)

Page context: "70', '00230790' are also called by bodies filed to movement: '00230790', '00338490', '0022EF20' (+18 more); '002F5550', '002330D0', '002F4520' reach bodies filed to movement: '0026E5F0', '00233050', '0026E5D0' (+1 more) - shared machinery across the layer boundary, no shared ownership. - **Presentation - CLIENT and SERVICE (376 edges).** '00398F90', '002ED570', '00398030' are also called by bodies filed to presentation/rendering: '0046C"

```
0026E5D0  cmp      qword ptr [rip + 0x1e2c098], 0  ; -> 0209A670
0026E5D8  je       0x26e5ec  ; -> 0026E5EC
0026E5DA  mov      rax, qword ptr [rip + 0x1e2c0df]  ; -> 0209A6C0
0026E5E1  not      rax
0026E5E4  and      rax, qword ptr [rip + 0x1e2c0dd]  ; -> 0209A6C8
0026E5EB  ret      
0026E5EC  xor      eax, eax
0026E5EE  ret      
```

## 0041C970 (42 B, extent 0041C970-0041C99A)

Page context: "2D9300'; the '00397B50' family's sibling. Interior anchor '0039AC1E' (the '022D9300' store).  ## SWE2-EC7-41 update (2026-09-19) - '003E5B30'  '003E5B30' (338 B) is a spatial-audio body - '00422D50'/'0041C970'/'003E6DA0'. Interior anchor '003E5B4D' (a '00422D50' call).  ## SWE2-EC7-48 update (2026-09-19) - '00224E40'  '00224E40' (203 B) is the descriptor-forwarding audio body - '00221940'/'00221D60'/'00222050'/'00224C40'/'00225580'/'002"

```
0041C970  movsx    r9d, word ptr [rcx + 0x28]
0041C975  lea      rax, [rcx + 0x30]
0041C979  xor      r8d, r8d
0041C97C  test     r9d, r9d
0041C97F  jle      0x41c997  ; -> 0041C997
0041C981  cmp      dword ptr [rax + 0x80], edx
0041C987  je       0x41c999  ; -> 0041C999
0041C989  inc      r8d
0041C98C  add      rax, 0xa0
0041C992  cmp      r8d, r9d
0041C995  jl       0x41c981  ; -> 0041C981
0041C997  xor      eax, eax
0041C999  ret      
```
