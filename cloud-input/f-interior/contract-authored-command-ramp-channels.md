# F-interior pack: `17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/contract-authored-command-ramp-channels.json`.

Functions: 16. Each is cited on the page only at its entry and is still in the F frontier.

## 001DC2E0 (78 B, extent 001DC2E0-001DC32E)

Page context: "n full" is cheap here.)*  ## SWE2-EC7-27 update (2026-09-18) — '002DF660' sequence-stamped forward  '002DF660' (30 B) reads 'dword[0215EFDC]', increments and republishes the counter, then tail-jumps '001DC2E0' passing the pre-increment value in 'ecx' — the sequence stamp the '003B8670' ramp caller attaches to each forwarded command. Interior anchor '002DF673' (the counter store).  ## SWE2-EC7-34 update (2026-09-19) - '00332C40'  '00332C"

```
001DC2E0  mov      qword ptr [rsp + 8], rbx
001DC2E5  mov      qword ptr [rsp + 0x10], rbp
001DC2EA  mov      qword ptr [rsp + 0x18], rsi
001DC2EF  push     rdi
001DC2F0  sub      rsp, 0x30
001DC2F4  mov      ebx, r9d
001DC2F7  mov      rdi, r8
001DC2FA  mov      esi, edx
001DC2FC  mov      rbp, rcx
001DC2FF  call     0x210b30  ; -> 00210B30 fn
001DC304  mov      rcx, rax
001DC307  mov      dword ptr [rsp + 0x20], ebx
001DC30B  mov      r9, rdi
001DC30E  mov      r8d, esi
001DC311  mov      rdx, rbp
001DC314  call     0x211270  ; -> 00211270 fn
001DC319  mov      rbx, qword ptr [rsp + 0x40]
001DC31E  mov      rbp, qword ptr [rsp + 0x48]
001DC323  mov      rsi, qword ptr [rsp + 0x50]
001DC328  add      rsp, 0x30
001DC32C  pop      rdi
001DC32D  ret      
```

## 001EB7B0 (79 B, extent 001EB7B0-001EB7FF)

Page context: " the **handbook monster    viewer's model-open flag** — '001EB9C0' sets it after the staged loader accepts the request    (handle kept at '+0x130', keyed by '001C6320()' at '+0x120'), and '001EB940'/'001EB7B0' clear it    while closing the slot through '002EEB20' — the singleton '01F82E18' is the viewer object itself    ([the handbook's monster viewer](../16-UI/Handbook/the-handbooks-monster-viewer.md); verified by    re-reading the cto"

```
001EB7B0  push     rbx
001EB7B2  sub      rsp, 0x20
001EB7B6  mov      rbx, rcx
001EB7B9  mov      dword ptr [rcx + 0x11c], edx
001EB7BF  mov      ecx, dword ptr [rcx + 0x130]
001EB7C5  cmp      ecx, -1
001EB7C8  je       0x1eb7f2  ; -> 001EB7F2
001EB7CA  mov      byte ptr [rbx + 0x118], 0
001EB7D1  call     0x2eeb20  ; -> 002EEB20 fn
001EB7D6  mov      qword ptr [rbx + 0x130], 0xffffffffffffffff
001EB7E1  mov      dword ptr [rbx + 0x120], 0xffffffff
001EB7EB  mov      byte ptr [rbx + 0x26e], 0
001EB7F2  mov      rcx, rbx
001EB7F5  add      rsp, 0x20
001EB7F9  pop      rbx
001EB7FA  jmp      0x1eb9c0  ; -> 001EB9C0 fn
```

## 002EE3E0 (70 B, extent 002EE3E0-002EE426)

Page context: "against 'byte[r8+2]', and 'r10d' is added on the way out - the channel value's fetch half, call-free.  Interior anchor '0041B4A2' (function '0041B460').  '0041C410' (666 B) is the rebuild dispatcher '002EE3E0', '00422EB0' and 'PresentationEntry_RebuildAndFastForwardToTime' '0041D820' itself call: two '00229EA0' mode reads against '+0x6E0', flag bits 1/0x17/0x12 at '+0xC', '003E7D10(3)', '+0xC0' bit 0x40, the '+0x340' float, mode '02CA83"

```
002EE3E0  sub      rsp, 0x28
002EE3E4  movsx    ecx, cx
002EE3E7  call     0x3ec580  ; -> 003EC580 fn
002EE3EC  test     rax, rax
002EE3EF  je       0x2ee421  ; -> 002EE421
002EE3F1  mov      rcx, rax
002EE3F4  mov      qword ptr [rsp + 0x20], rbx
002EE3F9  call     0x422d50  ; -> 00422D50 fn
002EE3FE  mov      rbx, rax
002EE401  test     rax, rax
002EE404  je       0x2ee41c  ; -> 002EE41C
002EE406  and      dword ptr [rax + 0xc], 0xff7fffff
002EE40D  mov      rcx, rax
002EE410  call     0x41c410  ; -> 0041C410 fn
002EE415  or       dword ptr [rbx + 0xc], 0x800000
002EE41C  mov      rbx, qword ptr [rsp + 0x20]
002EE421  add      rsp, 0x28
002EE425  ret      
```

## 00345010 (70 B, extent 00345010-00345056)

Page context: "'.  The tick order is 'the-world-tick-and-the-field-frame''s.  **Script_VM_Native_Bridge — CLIENT, eight edges.** Script handlers reach bodies this page cites: - the audio fade leaf '002DEDE0', from '00345010', '00350EC0' and '0050E960'; - the mode read '00229EA0', from '00354D00'; - the kind-3 read '00264670', from '00343520'; - the close-full-menu predicate '002E05C0', from '0050D1E0'; - '00360710' (a '0024D9C0' caller), from '0034ECF"

```
00345010  push     rbx
00345012  sub      rsp, 0x20
00345016  mov      rcx, r9
00345019  mov      rbx, rdx
0034501C  call     0x267e10  ; -> 00267E10 fn
00345021  test     eax, eax
00345023  jns      0x34502a  ; -> 0034502A
00345025  call     0x2dec00  ; -> 002DEC00 fn
0034502A  mov      ecx, eax
0034502C  call     0x2dede0  ; -> 002DEDE0 fn
00345031  movzx    ecx, byte ptr [rbx + 0x15]
00345035  call     0x267310  ; -> 00267310 fn
0034503A  test     eax, eax
0034503C  je       0x345050  ; -> 00345050
0034503E  xor      r8d, r8d
00345041  xor      edx, edx
00345043  or       ecx, 0xffffffff
00345046  add      rsp, 0x20
0034504A  pop      rbx
0034504B  jmp      0x360960  ; -> 00360960 fn
00345050  add      rsp, 0x20
00345054  pop      rbx
00345055  ret      
```

## 00350EC0 (107 B, extent 00350EC0-00350F2B)

Page context: " order is 'the-world-tick-and-the-field-frame''s.  **Script_VM_Native_Bridge — CLIENT, eight edges.** Script handlers reach bodies this page cites: - the audio fade leaf '002DEDE0', from '00345010', '00350EC0' and '0050E960'; - the mode read '00229EA0', from '00354D00'; - the kind-3 read '00264670', from '00343520'; - the close-full-menu predicate '002E05C0', from '0050D1E0'; - '00360710' (a '0024D9C0' caller), from '0034ECF0'; - '003A1"

```
00350EC0  mov      qword ptr [rsp + 8], rbx
00350EC5  push     rdi
00350EC6  sub      rsp, 0x20
00350ECA  xor      ebx, ebx
00350ECC  mov      rdi, r8
00350ECF  cmp      dword ptr [r8], ebx
00350ED2  jge      0x350ee1  ; -> 00350EE1
00350ED4  xor      eax, eax
00350ED6  mov      rbx, qword ptr [rsp + 0x30]
00350EDB  add      rsp, 0x20
00350EDF  pop      rdi
00350EE0  ret      
00350EE1  movzx    ecx, byte ptr [rdx + 0x15]
00350EE5  call     0x267310  ; -> 00267310 fn
00350EEA  mov      ecx, dword ptr [rdi]
00350EEC  test     eax, eax
00350EEE  je       0x350f0f  ; -> 00350F0F
00350EF0  call     0x2dede0  ; -> 002DEDE0 fn
00350EF5  xor      r8d, r8d
00350EF8  xor      edx, edx
00350EFA  or       ecx, 0xffffffff
00350EFD  call     0x360960  ; -> 00360960 fn
00350F02  mov      eax, ebx
00350F04  mov      rbx, qword ptr [rsp + 0x30]
00350F09  add      rsp, 0x20
00350F0D  pop      rdi
00350F0E  ret      
00350F0F  call     0x2ded60  ; -> 002DED60 fn
00350F14  test     eax, eax
00350F16  mov      ecx, 1
00350F1B  cmovne   ebx, ecx
00350F1E  mov      eax, ebx
00350F20  mov      rbx, qword ptr [rsp + 0x30]
00350F25  add      rsp, 0x20
00350F29  pop      rdi
00350F2A  ret      
```

## 003AFD50 (37 B, extent 003AFD50-003AFD75)

Page context: "e address or to either    writer, no 'lea' of the header base '02B3F550' at all, and all nine 'lea 02B3F570' walkers —    '003AF340'/'003AFB30'/'003AFBE0'/'003AFC10'/'003AFC30'/'003AFC80'/'003AFD00'/'003AFD50'/'003AFD80' —    read slot-positive offsets only. Best-fit reading: the V2 pool's own enable flag, driven in    lockstep with the V1 hide gate '02B40524' (4→1 shown, 6→0 hidden) — **published but consumed by    nothing in '.text'**"

```
003AFD50  movzx    edx, cl
003AFD53  imul     rax, rdx, 0x70
003AFD57  lea      rdx, [rip + 0x278f812]  ; -> 02B3F570
003AFD5E  add      rax, rdx
003AFD61  xor      edx, edx
003AFD63  cmp      dword ptr [rax + 4], ecx
003AFD66  cmovne   rax, rdx
003AFD6A  test     rax, rax
003AFD6D  je       0x3afd74  ; -> 003AFD74
003AFD6F  movss    dword ptr [rax + 8], xmm1
003AFD74  ret      
```

## 003AFD80 (73 B, extent 003AFD80-003AFDC9)

Page context: "r to either    writer, no 'lea' of the header base '02B3F550' at all, and all nine 'lea 02B3F570' walkers —    '003AF340'/'003AFB30'/'003AFBE0'/'003AFC10'/'003AFC30'/'003AFC80'/'003AFD00'/'003AFD50'/'003AFD80' —    read slot-positive offsets only. Best-fit reading: the V2 pool's own enable flag, driven in    lockstep with the V1 hide gate '02B40524' (4→1 shown, 6→0 hidden) — **published but consumed by    nothing in '.text'**; its consu"

```
003AFD80  movzx    r8d, cl
003AFD84  imul     rax, r8, 0x70
003AFD88  lea      r8, [rip + 0x278f7e1]  ; -> 02B3F570
003AFD8F  add      rax, r8
003AFD92  xor      r8d, r8d
003AFD95  cmp      dword ptr [rax + 4], ecx
003AFD98  cmovne   rax, r8
003AFD9C  test     rax, rax
003AFD9F  je       0x3afdc8  ; -> 003AFDC8
003AFDA1  movss    xmm1, dword ptr [rdx + 4]
003AFDA6  movss    xmm0, dword ptr [rax + 0x10]
003AFDAB  ucomiss  xmm0, xmm1
003AFDAE  jp       0x3afdb2  ; -> 003AFDB2
003AFDB0  je       0x3afdc8  ; -> 003AFDC8
003AFDB2  movss    xmm0, dword ptr [rip + 0x193bdee]  ; -> 01CEBBA8 [f32 1]
003AFDBA  divss    xmm0, xmm1
003AFDBE  movss    dword ptr [rax + 0x10], xmm1
003AFDC3  movss    dword ptr [rax + 0x14], xmm0
003AFDC8  ret      
```

## 003B6A10 (119 B, extent 003B6A10-003B6A87)

Page context: "ines / 0 mismatches, mutants killed (SWE2-CONTRACT, 2026-09-13, a27b5cc5) confidence: PROVEN implements: 17-Presentation-Rendering/README.md entries: ["003B5890", "003B6890", "003B6950", "003B69B0", "003B6A10", "003B6A90"] verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: address-resolution verification 2026-09-14 (OPUS) - 96 addresses cited - 16 data, 42 entry, 36 interior, 2 tex"

```
003B6A10  movzx    r9d, cl
003B6A14  imul     r10, r9, 0xe0
003B6A1B  add      r10, qword ptr [rip + 0x2789b06]  ; -> 02B40528
003B6A22  cmp      dword ptr [r10 + 0x10], ecx
003B6A26  jne      0x3b6a86  ; -> 003B6A86
003B6A28  test     dl, dl
003B6A2A  je       0x3b6a72  ; -> 003B6A72
003B6A2C  movss    xmm2, dword ptr [rip + 0x1935174]  ; -> 01CEBBA8 [f32 1]
003B6A34  movzx    eax, dl
003B6A37  mov      byte ptr [r10 + 2], dl
003B6A3B  movd     xmm0, eax
003B6A3F  cvtdq2ps xmm0, xmm0
003B6A42  divss    xmm2, xmm0
003B6A46  movss    xmm0, dword ptr [r8]
003B6A4B  subss    xmm0, dword ptr [r10 + 0x58]
003B6A51  mulss    xmm0, xmm2
003B6A55  movss    dword ptr [r10 + 0x68], xmm0
003B6A5B  movss    xmm1, dword ptr [r8 + 4]
003B6A61  subss    xmm1, dword ptr [r10 + 0x5c]
003B6A67  mulss    xmm1, xmm2
003B6A6B  movss    dword ptr [r10 + 0x6c], xmm1
003B6A71  ret      
003B6A72  mov      byte ptr [r10 + 2], 0
003B6A77  mov      eax, dword ptr [r8]
003B6A7A  mov      dword ptr [r10 + 0x58], eax
003B6A7E  mov      eax, dword ptr [r8 + 4]
003B6A82  mov      dword ptr [r10 + 0x5c], eax
003B6A86  ret      
```

## 003B6A90 (117 B, extent 003B6A90-003B6B05)

Page context: "matches, mutants killed (SWE2-CONTRACT, 2026-09-13, a27b5cc5) confidence: PROVEN implements: 17-Presentation-Rendering/README.md entries: ["003B5890", "003B6890", "003B6950", "003B69B0", "003B6A10", "003B6A90"] verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: address-resolution verification 2026-09-14 (OPUS) - 96 addresses cited - 16 data, 42 entry, 36 interior, 2 text-data, ever"

```
003B6A90  movzx    r9d, cl
003B6A94  imul     r10, r9, 0xe0
003B6A9B  add      r10, qword ptr [rip + 0x2789a86]  ; -> 02B40528
003B6AA2  cmp      dword ptr [r10 + 0x10], ecx
003B6AA6  jne      0x3b6b04  ; -> 003B6B04
003B6AA8  test     dl, dl
003B6AAA  je       0x3b6af1  ; -> 003B6AF1
003B6AAC  movss    xmm2, dword ptr [rip + 0x19350f4]  ; -> 01CEBBA8 [f32 1]
003B6AB4  movzx    eax, dl
003B6AB7  mov      byte ptr [r10], dl
003B6ABA  movd     xmm0, eax
003B6ABE  cvtdq2ps xmm0, xmm0
003B6AC1  divss    xmm2, xmm0
003B6AC5  movss    xmm0, dword ptr [r8]
003B6ACA  subss    xmm0, dword ptr [r10 + 0x50]
003B6AD0  mulss    xmm0, xmm2
003B6AD4  movss    dword ptr [r10 + 0x60], xmm0
003B6ADA  movss    xmm1, dword ptr [r8 + 4]
003B6AE0  subss    xmm1, dword ptr [r10 + 0x54]
003B6AE6  mulss    xmm1, xmm2
003B6AEA  movss    dword ptr [r10 + 0x64], xmm1
003B6AF0  ret      
003B6AF1  mov      byte ptr [r10], 0
003B6AF5  mov      eax, dword ptr [r8]
003B6AF8  mov      dword ptr [r10 + 0x50], eax
003B6AFC  mov      eax, dword ptr [r8 + 4]
003B6B00  mov      dword ptr [r10 + 0x54], eax
003B6B04  ret      
```

## 003B6BB0 (28 B, extent 003B6BB0-003B6BCC)

Page context: "uted-state cache; '+0x08'/'+0x0C'/'+0x14'/'+0x18'/'+0x20'–'+0x28'/'+0x2C' are the    scalar/vec3 fields '003B62D0' multiplies into the out record (leaf setters '003B6B10',    '003B6B30', '003B6B80', '003B6BB0'). **'+0x30'/'+0x34' reader censused to the boundary    2026-09-20 — there is none.** Every accessor resolves the record itself from    '[02B40528]' via the '(cl=slot, ecx=serial)' + 'imul 0xE0' pattern, so the 21-body    census is"

```
003B6BB0  movzx    edx, cl
003B6BB3  imul     rax, rdx, 0xe0
003B6BBA  add      rax, qword ptr [rip + 0x2789967]  ; -> 02B40528
003B6BC1  cmp      dword ptr [rax + 0x10], ecx
003B6BC4  jne      0x3b6bcb  ; -> 003B6BCB
003B6BC6  movss    dword ptr [rax + 0x2c], xmm1
003B6BCB  ret      
```

## 003B6BD0 (28 B, extent 003B6BD0-003B6BEC)

Page context: "re writing new ones — its reader is unfound);    '+0x38'/'+0x3A' are the current/previous blend selectors ('003B5CE0' shifts '+0x38'→'+0x3A');    '+0x44'/'+0x48'/'+0x4C' are UV scale/offset (setters '003B6BD0', '003B5CE0'); '+0x80'–'+0x94'    is the cross-fade B-set; '+0xA0'–'+0xB8' is a '+0x40'-flag-mode snapshot buffer ('003B5E20');    '+0xBC' is an extra rotation offset (setter '003B6B60'); '+0xC0'–'+0xD4' is '003B62D0''s    computed"

```
003B6BD0  movzx    edx, cl
003B6BD3  imul     rax, rdx, 0xe0
003B6BDA  add      rax, qword ptr [rip + 0x2789947]  ; -> 02B40528
003B6BE1  cmp      dword ptr [rax + 0x10], ecx
003B6BE4  jne      0x3b6beb  ; -> 003B6BEB
003B6BE6  movss    dword ptr [rax + 0x44], xmm1
003B6BEB  ret      
```

## 003B6BF0 (43 B, extent 003B6BF0-003B6C1B)

Page context: " before '003B62D0' builds its output ('003B620A'–'003B6224'; '003B62D0' interior read 2026-09-17, SWE2-FRONTIER: 1,301 B — '00421FF0' ×2 first at ['003B634F'](../_index/ADDRESS-INDEX.md), '0046FAE0'/'003B6BF0'/'00264670'). The advance '003B5890' tests only bit 0,         so hidden shadows keep ramping. - [x] **Who drives channel '+0x43'.** No authored-command class in the '00417xxx' family writes it.       *Answered on the page 2026-09-"

```
003B6BF0  cmp      cx, -1
003B6BF4  jne      0x3b6bf9  ; -> 003B6BF9
003B6BF6  xor      eax, eax
003B6BF8  ret      
003B6BF9  movsx    rax, cx
003B6BFD  imul     rcx, rax, 0x740
003B6C04  add      rcx, qword ptr [rip + 0x1f1031d]  ; -> 022C6F28
003B6C0B  je       0x3b6bf6  ; -> 003B6BF6
003B6C0D  cmp      dword ptr [rcx + 0x284], 0
003B6C14  je       0x3b6bf6  ; -> 003B6BF6
003B6C16  jmp      0x3e6f70  ; -> 003E6F70 fn
```

## 00422EB0 (117 B, extent 00422EB0-00422F25)

Page context: "e[r8+2]', and 'r10d' is added on the way out - the channel value's fetch half, call-free.  Interior anchor '0041B4A2' (function '0041B460').  '0041C410' (666 B) is the rebuild dispatcher '002EE3E0', '00422EB0' and 'PresentationEntry_RebuildAndFastForwardToTime' '0041D820' itself call: two '00229EA0' mode reads against '+0x6E0', flag bits 1/0x17/0x12 at '+0xC', '003E7D10(3)', '+0xC0' bit 0x40, the '+0x340' float, mode '02CA83F4' with '+0"

```
00422EB0  mov      qword ptr [rsp + 8], rbx
00422EB5  mov      qword ptr [rsp + 0x10], rsi
00422EBA  push     rdi
00422EBB  sub      rsp, 0x20
00422EBF  mov      edi, dword ptr [rcx + 0xc4]
00422EC5  xor      ebx, ebx
00422EC7  mov      esi, ebx
00422EC9  cmp      edi, -1
00422ECC  je       0x422f0e  ; -> 00422F0E
00422ECE  mov      ecx, dword ptr [rcx + 0x10]
00422ED1  call     0x20e600  ; -> 0020E600 fn
00422ED6  mov      edx, edi
00422ED8  mov      rcx, qword ptr [rax + 0xda8]
00422EDF  call     0x51b9e0  ; -> 0051B9E0 fn
00422EE4  mov      rcx, rax
00422EE7  mov      rdi, rax
00422EEA  call     0x41ca70  ; -> 0041CA70 fn
00422EEF  cmp      qword ptr [rdi + 0x368], rbx
00422EF6  je       0x422f0e  ; -> 00422F0E
00422EF8  test     dword ptr [rdi + 0xc], 0x100
00422EFF  jne      0x422f0e  ; -> 00422F0E
00422F01  mov      rcx, rdi
00422F04  call     0x41c410  ; -> 0041C410 fn
00422F09  mov      esi, 1
00422F0E  test     esi, esi
00422F10  mov      rsi, qword ptr [rsp + 0x38]
00422F15  setne    bl
00422F18  mov      eax, ebx
00422F1A  mov      rbx, qword ptr [rsp + 0x30]
00422F1F  add      rsp, 0x20
00422F23  pop      rdi
00422F24  ret      
```

## 0046D8E0 (54 B, extent 0046D8E0-0046D916)

Page context: "+0x58'/'+0x88'. Interior anchor '003B5E5B' (the first snapshot store).   ## SWE2-EC7-53 update (2026-09-19) - '00409300'  '00409300' (451 B) is a ramp-channel body - '0046D110'/'0046D380'/'0046D560'/'0046D8E0'/'0046D920'/'00808C40'. Interior anchor '0040941B' (a '0046D560' call).  ## SWE2-EC7-54 update (2026-09-19) - '0046D560'  '0046D560' (464 B) is a call-free '01F004E0' table evaluator - 'divss' normalize by '01CEBC78', '00D10820' sc"

```
0046D8E0  movss    xmm2, dword ptr [rcx + 0x3c]
0046D8E5  movaps   xmm0, xmm2
0046D8E8  movaps   xmm1, xmm2
0046D8EB  mulss    xmm0, dword ptr [rdx]
0046D8EF  movss    dword ptr [rcx + 0x30], xmm0
0046D8F4  movaps   xmm0, xmm2
0046D8F7  mulss    xmm1, dword ptr [rdx + 4]
0046D8FC  movss    dword ptr [rcx + 0x34], xmm1
0046D901  mulss    xmm0, dword ptr [rdx + 8]
0046D906  movss    dword ptr [rcx + 0x38], xmm0
0046D90B  mulss    xmm2, dword ptr [rdx + 0xc]
0046D910  movss    dword ptr [rcx + 0x3c], xmm2
0046D915  ret      
```

## 0046D920 (41 B, extent 0046D920-0046D949)

Page context: "88'. Interior anchor '003B5E5B' (the first snapshot store).   ## SWE2-EC7-53 update (2026-09-19) - '00409300'  '00409300' (451 B) is a ramp-channel body - '0046D110'/'0046D380'/'0046D560'/'0046D8E0'/'0046D920'/'00808C40'. Interior anchor '0040941B' (a '0046D560' call).  ## SWE2-EC7-54 update (2026-09-19) - '0046D560'  '0046D560' (464 B) is a call-free '01F004E0' table evaluator - 'divss' normalize by '01CEBC78', '00D10820' scale, 'cvtts"

```
0046D920  movss    xmm2, dword ptr [rcx + 0x3c]
0046D925  movaps   xmm0, xmm2
0046D928  movaps   xmm1, xmm2
0046D92B  mulss    xmm0, dword ptr [rdx]
0046D92F  movss    dword ptr [rcx + 0x30], xmm0
0046D934  mulss    xmm1, dword ptr [rdx + 4]
0046D939  movss    dword ptr [rcx + 0x34], xmm1
0046D93E  mulss    xmm2, dword ptr [rdx + 8]
0046D943  movss    dword ptr [rcx + 0x38], xmm2
0046D948  ret      
```

## 0046FB40 (100 B, extent 0046FB40-0046FBA4)

Page context: "nterior anchor '0041C564' (function '0041C410').  '0042F030' (349 B) is the ramp tick '00426090' calls: '02CA48F8' global - '[rbx - 0x1C]' decrements while '[rbx - 0x14] + [rbx - 0x18]' accumulates, '0046FB40' is poked per step, 'xmm7' seeded from '00D12470' - the channel ramp's per-frame accumulator.  Interior anchor '0042F09A' (function '0042F030').  '003AFD00' (44 B) is the low-nibble write '00421280'/'00426340' call: 'cl x 0x70' ind"

```
0046FB40  mov      r9d, dword ptr [rip + 0x1ab09e9]  ; -> 01F20530 [u32 0x00000032]
0046FB47  xor      r8d, r8d
0046FB4A  xorps    xmm1, xmm1
0046FB4D  mov      r10, rdx
0046FB50  lea      ecx, [r9 - 1]
0046FB54  mov      eax, ecx
0046FB56  cvtsi2ss xmm1, rax
0046FB5B  mulss    xmm1, xmm0
0046FB5F  cvttss2si eax, xmm1
0046FB63  test     eax, eax
0046FB65  cmovns   r8d, eax
0046FB69  cmp      r8d, ecx
0046FB6C  jbe      0x46fb72  ; -> 0046FB72
0046FB6E  lea      r8d, [r9 - 1]
0046FB72  lea      edx, [r8 + r8*2]
0046FB76  lea      r8, [rip + 0x1ab09c3]  ; -> 01F20540
0046FB7D  movsxd   rax, edx
0046FB80  mov      eax, dword ptr [r8 + rax*4]
0046FB84  mov      dword ptr [r10], eax
0046FB87  lea      eax, [rdx + 1]
0046FB8A  movsxd   rcx, eax
0046FB8D  mov      eax, dword ptr [r8 + rcx*4]
0046FB91  mov      dword ptr [r10 + 4], eax
0046FB95  lea      eax, [rdx + 2]
0046FB98  movsxd   rcx, eax
0046FB9B  mov      eax, dword ptr [r8 + rcx*4]
0046FB9F  mov      dword ptr [r10 + 8], eax
0046FBA3  ret      
```
