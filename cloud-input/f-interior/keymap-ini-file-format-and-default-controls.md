# F-interior pack: `15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md`

Generated 2026-10-02 23:37 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/keymap-ini-file-format-and-default-controls.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

## 00198670 (24 B, extent 00198670-00198688)

Page context: "r_PollAndBuildControlState' polls the first when bit 1 of the manager byte '+0x3A' is set ('001970C8') and the second when bit 0 or bit 2 is ('001970F8'). Those bits are toggled by six tiny setters ('00198670' sets bit 2, '00198710' clears bit 1, and so on), each marking '+0x3B' dirty, reached through the wrappers '00182CD0'–'00182DA0' from the system-stop registry paths '00225CD0' / '00225EB0' / '00227680', the main loop, the save-load"

```
00198670  movsx    edx, byte ptr [rcx + 0x3a]
00198674  mov      eax, edx
00198676  shr      eax, 2
00198679  test     al, 1
0019867B  jne      0x198687  ; -> 00198687
0019867D  or       dl, 4
00198680  mov      byte ptr [rcx + 0x3b], 1
00198684  mov      byte ptr [rcx + 0x3a], dl
00198687  ret      
```

## 001D8520 (120 B, extent 001D8520-001D8598)

Page context: "the pass list '00187950'): after the save-busy branch it tests '00229DF0()' — the byte '02064AD2', this page's 'g_fastModeEnabled' — and the per-frame byte '+0x68' ('001D72B5'–'001D72C2'), then runs '001D8520', which raises the alpha by 0.5 per frame (1.0 when the present interval '00184950()' is 2), lifts it to a 63.0 floor ('00900380') from below and holds it at 255.0 ('008C5B40') from above — '+0x64' receives −6 at the top and +6 at "

```
001D8520  push     rbx
001D8522  sub      rsp, 0x20
001D8526  mov      rbx, rcx
001D8529  call     0x184950  ; -> 00184950 fn
001D852E  cmp      eax, 2
001D8531  jne      0x1d853d  ; -> 001D853D
001D8533  movss    xmm0, dword ptr [rip + 0x1b1366d]  ; -> 01CEBBA8 [f32 1]
001D853B  jmp      0x1d8545  ; -> 001D8545
001D853D  movss    xmm0, dword ptr [rip + 0x1b1362b]  ; -> 01CEBB70 [f32 0.5]
001D8545  movss    xmm2, dword ptr [rip + 0x6ed5f3]  ; -> 008C5B40 [f32 255]
001D854D  movaps   xmm1, xmm0
001D8550  addss    xmm1, dword ptr [rbx + 0x60]
001D8555  comiss   xmm1, xmm2
001D8558  movss    dword ptr [rbx + 0x60], xmm1
001D855D  jb       0x1d8575  ; -> 001D8575
001D855F  subss    xmm2, xmm0
001D8563  mov      dword ptr [rbx + 0x64], 0xc0c00000
001D856A  movss    dword ptr [rbx + 0x60], xmm2
001D856F  add      rsp, 0x20
001D8573  pop      rbx
001D8574  ret      
001D8575  movss    xmm2, dword ptr [rip + 0x727e03]  ; -> 00900380 [f32 63]
001D857D  comiss   xmm2, xmm1
001D8580  jb       0x1d8592  ; -> 001D8592
001D8582  addss    xmm0, xmm2
001D8586  mov      dword ptr [rbx + 0x64], 0x40c00000
001D858D  movss    dword ptr [rbx + 0x60], xmm0
001D8592  add      rsp, 0x20
001D8596  pop      rbx
001D8597  ret      
```

## 0024B0C0 (50 B, extent 0024B0C0-0024B0F2)

Page context: "001D8150' zeroes the record and sets '+0x6C = 1.0'. '001D7150' fills it from the record table '[0209AC30] + 0xA0' ('0027E9D0') through 'ImageAddress_ResolveRuntimePointer' '0020E600', '002A0060' and '0024B0C0': a first icon set at '+0x10' .. '+0x28' and '+0x70' .. '+0x80', and a second set at '+0x30' .. '+0x38' with three sprite records '+0x48', '+0x50', '+0x58'. **'001D85C0(n)' arms the second icon:** '+0x40' (the sprite to draw) becom"

```
0024B0C0  mov      r9, qword ptr [rcx + 0x20]
0024B0C4  add      r9, 0x30
0024B0C8  mov      eax, edx
0024B0CA  shr      rax, 8
0024B0CE  movzx    ecx, word ptr [r9 + rax*2 + 0x14]
0024B0D4  movzx    eax, dl
0024B0D7  add      ecx, eax
0024B0D9  movsxd   rax, r8d
0024B0DC  movzx    edx, word ptr [r9 + rcx*2 + 0x14]
0024B0E2  movzx    ecx, word ptr [r9 + 0x10]
0024B0E7  add      rdx, rax
0024B0EA  add      rcx, r9
0024B0ED  lea      rax, [rcx + rdx*8]
0024B0F1  ret      
```

## 00797EE0 (61 B, extent 00797EE0-00797F1D)

Page context: "ding in this image. A second, unrelated 128-byte table precedes it at '01F3DA30': ASCII character → keymap code ('A' or 'a' → 28, '1' → 54, 'Esc' → 64, space → 80), used by the injected-key handlers '00797EE0' / '00797F20' / '00797F60'. Static: the poll body and the two tables read from the image.* - [x] **The 11–26 band is ANSWERED 2026-09-08: the sixteen pad buttons, and the "conflicting       values" are ALIASES.** 'PInputChannelSema"

```
00797EE0  test     rcx, rcx
00797EE3  je       0x797f1a  ; -> 00797F1A
00797EE5  test     rdx, rdx
00797EE8  je       0x797f1a  ; -> 00797F1A
00797EEA  mov      rax, qword ptr [rcx + 0xdf8]
00797EF1  mov      rcx, qword ptr [rax + 0x118]
00797EF8  test     rcx, rcx
00797EFB  je       0x797f1a  ; -> 00797F1A
00797EFD  movsx    rax, byte ptr [rdx]
00797F01  lea      rdx, [rip + 0x17a5b28]  ; -> 01F3DA30
00797F08  and      eax, 0x7f
00797F0B  movzx    eax, byte ptr [rax + rdx]
00797F0F  sub      rax, 0x1c
00797F13  mov      eax, eax
00797F15  mov      byte ptr [rax + rcx + 0x30], 1
00797F1A  xor      eax, eax
00797F1C  ret      
```

## 00797F20 (61 B, extent 00797F20-00797F5D)

Page context: "image. A second, unrelated 128-byte table precedes it at '01F3DA30': ASCII character → keymap code ('A' or 'a' → 28, '1' → 54, 'Esc' → 64, space → 80), used by the injected-key handlers '00797EE0' / '00797F20' / '00797F60'. Static: the poll body and the two tables read from the image.* - [x] **The 11–26 band is ANSWERED 2026-09-08: the sixteen pad buttons, and the "conflicting       values" are ALIASES.** 'PInputChannelSemantic' registe"

```
00797F20  test     rcx, rcx
00797F23  je       0x797f5a  ; -> 00797F5A
00797F25  test     rdx, rdx
00797F28  je       0x797f5a  ; -> 00797F5A
00797F2A  mov      rax, qword ptr [rcx + 0xdf8]
00797F31  mov      rcx, qword ptr [rax + 0x118]
00797F38  test     rcx, rcx
00797F3B  je       0x797f5a  ; -> 00797F5A
00797F3D  movsx    rax, byte ptr [rdx]
00797F41  lea      rdx, [rip + 0x17a5ae8]  ; -> 01F3DA30
00797F48  and      eax, 0x7f
00797F4B  movzx    eax, byte ptr [rax + rdx]
00797F4F  sub      rax, 0x1c
00797F53  mov      eax, eax
00797F55  mov      byte ptr [rax + rcx + 0x30], 0
00797F5A  xor      eax, eax
00797F5C  ret      
```
