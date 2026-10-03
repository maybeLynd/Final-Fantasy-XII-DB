# Homing pack: `15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md`

Generated 2026-10-02 22:54 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-keymap-ini-file-format-and-default-controls.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001941F0 (74 B, extent 001941F0-0019423A)

Entered from (direct sites whose caller this page cites): `00189CE0` + 0x1CF (call; `00189CE0` is cited on this page)
Other direct sites: none

Host context: "022A770' — platform-layer helpers the keymap parse path neighbours. Shared-helper exchange only.  **Presentation — MECHANICAL (SWE2-EC7-159, 107 edges).** '0017D6E0' calls Presentation-tagged bodies '00189CE0'/'001BC190'/'001BDAC0'/'001CCxxx' et al. — the binding pump's fan-in to shared presentation helpers. Not a keymap responsibility.  **Resource — MECHANICAL (SWE2-EC7-159, 14 edges).** '0017D4C0' calls '001A11B0'/'001DB1E0', '0017D6E"

```
001941F0  movups   xmm0, xmmword ptr [rdx]
001941F3  movups   xmmword ptr [rcx + 0x440], xmm0
001941FA  movups   xmm1, xmmword ptr [rdx + 0x10]
001941FE  movups   xmmword ptr [rcx + 0x450], xmm1
00194205  movups   xmm0, xmmword ptr [rdx + 0x20]
00194209  movups   xmmword ptr [rcx + 0x460], xmm0
00194210  movups   xmm1, xmmword ptr [rdx + 0x30]
00194214  movss    xmm0, dword ptr [rsp + 0x28]
0019421A  movups   xmmword ptr [rcx + 0x470], xmm1
00194221  movss    dword ptr [rcx + 0x480], xmm2
00194229  movss    dword ptr [rcx + 0x484], xmm3
00194231  movss    dword ptr [rcx + 0x488], xmm0
00194239  ret      
```

## 00194490 (43 B, extent 00194490-001944BB)

Entered from (direct sites whose caller this page cites): `00189CE0` + 0x405 (call; `00189CE0` is cited on this page)
Other direct sites: `00182870` + 0x31 (call)

Host context: "022A770' — platform-layer helpers the keymap parse path neighbours. Shared-helper exchange only.  **Presentation — MECHANICAL (SWE2-EC7-159, 107 edges).** '0017D6E0' calls Presentation-tagged bodies '00189CE0'/'001BC190'/'001BDAC0'/'001CCxxx' et al. — the binding pump's fan-in to shared presentation helpers. Not a keymap responsibility.  **Resource — MECHANICAL (SWE2-EC7-159, 14 edges).** '0017D4C0' calls '001A11B0'/'001DB1E0', '0017D6E"

```
00194490  movss    dword ptr [rcx + 0x128], xmm2
00194498  mov      dword ptr [rcx + 0x124], edx
0019449E  test     r9, r9
001944A1  je       0x1944ba  ; -> 001944BA
001944A3  movsd    xmm0, qword ptr [r9]
001944A8  movsd    qword ptr [rcx + 0x12c], xmm0
001944B0  mov      eax, dword ptr [r9 + 8]
001944B4  mov      dword ptr [rcx + 0x134], eax
001944BA  ret      
```

## 00285FE0 (26 B, extent 00285FE0-00285FFA)

Entered from (direct sites whose caller this page cites): `002B5C90` + 0x38 (call; `002B5C90` is cited on this page)
Other direct sites: none

Host context: "001E0BD0' 'InputConfig_GetBinding' as *"generic '(profile, group, slot)' getter, **10 call sites**"*. The graph gives 10 **distinct callers**; the instruction census gives **15 call sites**, because '002B5C90' calls it **six times** and the other nine call it once each.  Both numbers are right about different populations, and the document states the one it did not measure. This is the edge-count-versus-call-site confusion the evidence s"

```
00285FE0  sub      ecx, 1
00285FE3  je       0x285ff4  ; -> 00285FF4
00285FE5  cmp      ecx, 1
00285FE8  jne      0x285fee  ; -> 00285FEE
00285FEA  lea      eax, [rcx + 6]
00285FED  ret      
00285FEE  mov      eax, 9
00285FF3  ret      
00285FF4  mov      eax, 8
00285FF9  ret      
```

## 00314820 (18 B, extent 00314820-00314832)

Entered from (direct sites whose caller this page cites): `0022A770` + 0x1D8 (call; `0022A770` is cited on this page); `0022A770` + 0x4D6 (call; `0022A770` is cited on this page); `0022A770` + 0x661 (call; `0022A770` is cited on this page)
Other direct sites: none

Host context: "tead. The file's 'L2=' and 'R2=' lines are live; they simply take a different road.  #### 'Speed1', 'Speed2', 'Speed3' — the 1× / 2× / 4× game-speed toggles  '0017DEA0' is called from the main loop ('0022A770', under its own '"[PS2]fast mode"' / '"FAST MODE"' debug markers) and is a three-way edge-latched poll:  '''c if      (IsActive(GetBinding(0, 2, 0))) { if (!latch) { latch = 1; SetSpeedMode(1); } return 1; } else if (IsActive(GetBi" / "tead. The file's 'L2=' and 'R2=' lines are live; they simply take a different road.  #### 'Speed1', 'Speed2', 'Speed3' — the 1× / 2× / 4× game-speed toggles  '0017DEA0' is called from the main loop ('0022A770', under its own '"[PS2]fast mode"' / '"FAST MODE"' debug markers) and is a three-way edge-latched poll:  '''c if      (IsActive(GetBinding(0, 2, 0))) { if (!latch) { latch = 1; SetSpeedMode(1); } return 1; } else if (IsActive(GetBi"

```
00314820  sub      rsp, 0x28
00314824  call     0x377520  ; -> 00377520 fn
00314829  add      rsp, 0x28
0031482D  jmp      0x3b6c70  ; -> 003B6C70 fn
```
