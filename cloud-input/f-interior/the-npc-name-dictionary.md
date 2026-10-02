# F-interior pack: `04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md`

Generated 2026-10-02 10:27 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-npc-name-dictionary.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 001DA220 (102 B, extent 001DA220-001DA286)

Page context: "d-helper fan-in; no AI relationship to the dictionary.  **Resource — SERVICE (SWE2-EC7-163, 49 edges).** The dictionary's table helpers are consulted by the Resource loaders: '00265270' is called by '001DA220'/ '001DA970' there, and '002DF780' calls '001D6B40'/'001D6D90' (+45 more of the same shape). Mechanical fan-in; no shared ownership.  ## The '00379D20' exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)  '00379D20' "

```
001DA220  push     rdi
001DA222  sub      rsp, 0x20
001DA226  mov      rdi, rcx
001DA229  call     0x1d6b20  ; -> 001D6B20 fn
001DA22E  test     eax, eax
001DA230  je       0x1da280  ; -> 001DA280
001DA232  call     0x1d6b90  ; -> 001D6B90 fn
001DA237  test     eax, eax
001DA239  jne      0x1da280  ; -> 001DA280
001DA23B  call     0x265270  ; -> 00265270 fn
001DA240  test     ax, ax
001DA243  jne      0x1da280  ; -> 001DA280
001DA245  xor      eax, eax
001DA247  mov      qword ptr [rsp + 0x30], rbx
001DA24C  lea      rcx, [rdi + 0xf0]
001DA253  mov      word ptr [rdi + 0xe8], ax
001DA25A  call     0x5cd4f0  ; -> 005CD4F0 fn
001DA25F  mov      rcx, rdi
001DA262  call     0x1d9930  ; -> 001D9930 fn
001DA267  lea      rcx, [rdi + 0xf0]
001DA26E  call     0x5cd820  ; -> 005CD820 fn
001DA273  mov      rcx, rdi
001DA276  call     0x1d9ec0  ; -> 001D9EC0 fn
001DA27B  mov      rbx, qword ptr [rsp + 0x30]
001DA280  add      rsp, 0x20
001DA284  pop      rdi
001DA285  ret      
```

## 001DA970 (100 B, extent 001DA970-001DA9D4)

Page context: "-in; no AI relationship to the dictionary.  **Resource — SERVICE (SWE2-EC7-163, 49 edges).** The dictionary's table helpers are consulted by the Resource loaders: '00265270' is called by '001DA220'/ '001DA970' there, and '002DF780' calls '001D6B40'/'001D6D90' (+45 more of the same shape). Mechanical fan-in; no shared ownership.  ## The '00379D20' exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)  '00379D20' (~36 B) — '0"

```
001DA970  push     rdi
001DA972  sub      rsp, 0x20
001DA976  mov      rdi, rcx
001DA979  call     0x1d6b20  ; -> 001D6B20 fn
001DA97E  test     eax, eax
001DA980  je       0x1da9ce  ; -> 001DA9CE
001DA982  call     0x265270  ; -> 00265270 fn
001DA987  test     ax, ax
001DA98A  jle      0x1da9ce  ; -> 001DA9CE
001DA98C  cmp      ax, word ptr [rdi + 0xe8]
001DA993  je       0x1da9ce  ; -> 001DA9CE
001DA995  lea      rcx, [rdi + 0xf0]
001DA99C  mov      qword ptr [rsp + 0x30], rbx
001DA9A1  mov      word ptr [rdi + 0xe8], ax
001DA9A8  call     0x5cd4f0  ; -> 005CD4F0 fn
001DA9AD  mov      rcx, rdi
001DA9B0  call     0x1d9930  ; -> 001D9930 fn
001DA9B5  lea      rcx, [rdi + 0xf0]
001DA9BC  call     0x5cd820  ; -> 005CD820 fn
001DA9C1  mov      rcx, rdi
001DA9C4  call     0x1d9ec0  ; -> 001D9EC0 fn
001DA9C9  mov      rbx, qword ptr [rsp + 0x30]
001DA9CE  add      rsp, 0x20
001DA9D2  pop      rdi
001DA9D3  ret      
```

## 00275F10 (231 B, extent 00275F10-00275FF7)

Page context: "EC7-103 update (2026-09-20) - '002747B0' measured  '002747B0' (137 B) is the '0xD8'-keyed lookup pair '002B7590', '002BA700', '003CB650' and '00552250' call: a nonnull 'rcx' runs '00245000' with the '00275F10' formatter and a stack out-record; a null 'rcx' instead runs '00244F50' with the same '0xD8' size and '00275F10' target - the present-versus-fetch split the name-dictionary arms share. Interior anchor '002747FA' (the '00245000' cal"

```
00275F10  sub      rsp, 0x48
00275F14  mov      rax, qword ptr [rip + 0x1cce915]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00275F1B  xor      rax, rsp
00275F1E  mov      qword ptr [rsp + 0x38], rax
00275F23  mov      r8, rcx
00275F26  mov      ecx, dword ptr [rdx]
00275F28  sub      ecx, 1
00275F2B  je       0x275fc1  ; -> 00275FC1
00275F31  sub      ecx, 0xf
00275F34  je       0x275f98  ; -> 00275F98
00275F36  cmp      ecx, 2
00275F39  je       0x275f55  ; -> 00275F55
00275F3B  mov      rcx, r8
00275F3E  call     0x5c5230  ; -> 005C5230 fn
00275F43  mov      rcx, qword ptr [rsp + 0x38]
00275F48  xor      rcx, rsp
00275F4B  call     0x808c40  ; -> 00808C40 fn
00275F50  add      rsp, 0x48
00275F54  ret      
00275F55  mov      rcx, qword ptr [r8 + 0xc0]
00275F5C  xorps    xmm0, xmm0
00275F5F  mov      eax, dword ptr [r8 + 0xc8]
00275F66  mov      dword ptr [rsp + 0x20], eax
00275F6A  movdqu   xmmword ptr [rsp + 0x28], xmm0
00275F70  test     rcx, rcx
00275F73  je       0x275fe3  ; -> 00275FE3
00275F75  mov      rax, qword ptr [rcx]
00275F78  test     rax, rax
00275F7B  je       0x275fe3  ; -> 00275FE3
00275F7D  lea      rdx, [rsp + 0x20]
00275F82  call     rax
00275F84  xor      eax, eax
00275F86  mov      rcx, qword ptr [rsp + 0x38]
00275F8B  xor      rcx, rsp
00275F8E  call     0x808c40  ; -> 00808C40 fn
00275F93  add      rsp, 0x48
00275F97  ret      
00275F98  movsxd   rax, dword ptr [r8 + 0xcc]
00275F9F  cmp      qword ptr [rdx + 8], rax
00275FA3  jne      0x275fe3  ; -> 00275FE3
00275FA5  mov      rcx, r8
00275FA8  call     0x244f00  ; -> 00244F00 fn
00275FAD  xor      eax, eax
00275FAF  mov      rcx, qword ptr [rsp + 0x38]
00275FB4  xor      rcx, rsp
00275FB7  call     0x808c40  ; -> 00808C40 fn
00275FBC  add      rsp, 0x48
00275FC0  ret      
00275FC1  mov      rcx, qword ptr [rdx + 8]
00275FC5  mov      eax, dword ptr [rcx + 8]
00275FC8  mov      dword ptr [r8 + 0xc8], eax
00275FCF  mov      eax, dword ptr [rcx + 0xc]
00275FD2  mov      dword ptr [r8 + 0xcc], eax
00275FD9  mov      rax, qword ptr [rcx]
00275FDC  mov      qword ptr [r8 + 0xc0], rax
00275FE3  xor      eax, eax
00275FE5  mov      rcx, qword ptr [rsp + 0x38]
00275FEA  xor      rcx, rsp
00275FED  call     0x808c40  ; -> 00808C40 fn
00275FF2  add      rsp, 0x48
00275FF6  ret      
```

## 00521290 (70 B, extent 00521290-005212D6)

Page context: "1', '0053B730', 'mov word [r13 + r15*2 + 0x100]' — an indexed array element whose base 'r13' is the function's second argument, which the auditor traces to the FCP character parameter block fed from '00521290' records), '001294D0' (base loaded from '[rbp+0x18]'), '002D14E0' (an allocation result, beside a store to '+0xEA'), '003A8020' and '003A8290' (Presentation, beside '+0xE8' / '+0xF0' and a call to '004FF080'), '004FF080' (clears '+"

```
00521290  mov      r9, qword ptr [rip + 0x27871b9]  ; -> 02CA8450
00521297  xor      r8d, r8d
0052129A  mov      edx, r8d
0052129D  mov      rax, r9
005212A0  mov      r10d, 0xffff
005212A6  cmp      word ptr [rax], r10w
005212AA  je       0x5212b1  ; -> 005212B1
005212AC  cmp      dword ptr [rax + 4], ecx
005212AF  je       0x5212c7  ; -> 005212C7
005212B1  inc      r8d
005212B4  inc      rdx
005212B7  add      rax, 0x30
005212BB  cmp      rdx, 0x100
005212C2  jl       0x5212a6  ; -> 005212A6
005212C4  xor      eax, eax
005212C6  ret      
005212C7  movsxd   rax, r8d
005212CA  lea      rax, [rax + rax*2]
005212CE  shl      rax, 4
005212D2  add      rax, r9
005212D5  ret      
```
