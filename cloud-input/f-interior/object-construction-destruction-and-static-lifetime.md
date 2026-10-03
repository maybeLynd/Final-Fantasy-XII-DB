# F-interior pack: `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/object-construction-destruction-and-static-lifetime.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

## 00199320 (99 B, extent 00199320-00199383)

Page context: "e CRT-import calls | '0019BB11' / '00197B91' | | 4 | '0019BD80' | '00197E10' | get-area walk on '+0x38'/'+0x50'/'+0x68'/'+0x70'/'+0x80' buffer pointers | '0019BDEC' / '00197E8F' | | 6 | '0019C490' | '00199320' | put/get pointer recompute on '+0x20'/'+0x30'/'+0x38'/'+0x50' | '0019C49D' / '00199320' | | 7 | '0019C130' | '00198FC0' | the big drain routine (861/864 B): mirror of slot 3's shape, '00195670' | '0019C196' / '0019902A' | | 10 | "

```
00199320  push     rbx
00199322  sub      rsp, 0x20
00199326  mov      rax, qword ptr [rcx + 0x38]
0019932A  mov      rbx, rcx
0019932D  mov      rcx, qword ptr [rax]
00199330  test     rcx, rcx
00199333  je       0x19934e  ; -> 0019934E
00199335  mov      rdx, qword ptr [rbx + 0x50]
00199339  movsxd   r8, dword ptr [rdx]
0019933C  lea      rdx, [rcx + r8*2]
00199340  cmp      rcx, rdx
00199343  jae      0x19934e  ; -> 0019934E
00199345  movzx    eax, word ptr [rcx]
00199348  add      rsp, 0x20
0019934C  pop      rbx
0019934D  ret      
0019934E  mov      rax, qword ptr [rbx]
00199351  mov      rcx, rbx
00199354  mov      qword ptr [rsp + 0x30], rdi
00199359  call     qword ptr [rax + 0x38]
0019935C  movzx    edi, ax
0019935F  mov      eax, 0xffff
00199364  cmp      ax, di
00199367  je       0x199378  ; -> 00199378
00199369  mov      rax, qword ptr [rbx]
0019936C  movzx    edx, di
0019936F  mov      rcx, rbx
00199372  call     qword ptr [rax + 0x20]
00199375  movzx    eax, di
00199378  mov      rdi, qword ptr [rsp + 0x30]
0019937D  add      rsp, 0x20
00199381  pop      rbx
00199382  ret      
```

## 001E0F40 (36 B, extent 001E0F40-001E0F64)

Page context: "s, 1; Script_VM_Native_Bridge, 1; WorldAreaField, 1;   RNG_Random_Selection, 1 — MECHANICAL.** Each is one more caller of a shared lifetime helper:   - the destructor '001993B0', from '0017D670' and '001E0F40';   - the serialisers, from '0079FB10';   - '00873FE0' / '00874080';   - '001BDAC0', from the frame step;   - '001DF8C0', from 'GameSettingConfig_SerializeText';   - '00660570', from '00510740';   - '00378540', from 'WorldAreaField"

```
001E0F40  sub      rsp, 0x28
001E0F44  call     0x198790  ; -> 00198790 fn
001E0F49  test     rax, rax
001E0F4C  je       0x1e0f5f  ; -> 001E0F5F
001E0F4E  call     0x198790  ; -> 00198790 fn
001E0F53  mov      rcx, rax
001E0F56  add      rsp, 0x28
001E0F5A  jmp      0x1993b0  ; -> 001993B0 fn
001E0F5F  add      rsp, 0x28
001E0F63  ret      
```

## 00660570 (4 B, extent 00660570-00660574)

Page context: "er than a sample does. Taking each site's neighbours across **all 28**:  | slot | value | in how many | |---|---|---| | '−2' | '0062EFD0' | **28 / 28** | | '−1' | '0062F080' | **28 / 28** | | '+3' | '00660570' | **28 / 28** | | '+4' | '005C5230' | 25 / 28 | | '+1' | '0063FC60' | 16 / 28 | | '−4', '−3', '+2' | *(all different)* | 1 / 28 |  **Three slots hold the same function in every one of the 28 tables while the slots either side of t"

```
00660570  or       eax, 0xffffffff
00660573  ret      
```
