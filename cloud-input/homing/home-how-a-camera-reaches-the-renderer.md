# Homing pack: `17-Presentation-Rendering/Scripted-Camera/how-a-camera-reaches-the-renderer.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-how-a-camera-reaches-the-renderer.json`.

Bodies: 7. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00185E50 (351 B, extent 00185E50-00185FAF)

Entered from (direct sites whose caller this page cites): `00182310` + 0x23 (jmp; `00182310` is cited on this page)
Other direct sites: none

Host context: "EC7-53 update (2026-09-19) - '003CBD60'  '003CBD60' (571 B) is the camera matrix rebuild the page describes - '00380190'/'00380650'/'003CBCA0' plus Movement helpers '00202B70'/'00202D50'/'00202E10', '00182310', '00D22740' rdata (the page note 'itself was not read' is now read). Interior anchor '003CBE17' (a '00380190' call).   ## SWE2-EC7-53 update (2026-09-19) - '00233230'  '00233230' (524 B) is a Movement-owned helper the camera page "

```
00185E50  push     rbx
00185E52  sub      rsp, 0x90
00185E59  mov      rbx, rdx
00185E5C  call     0x18a620  ; -> 0018A620 fn
00185E61  test     rax, rax
00185E64  je       0x185fa6  ; -> 00185FA6
00185E6A  call     0x18a620  ; -> 0018A620 fn
00185E6F  cmp      byte ptr [rax], 0
00185E72  je       0x185fa6  ; -> 00185FA6
00185E78  call     0x18a620  ; -> 0018A620 fn
00185E7D  cmp      qword ptr [rax + 0xc0], 0
00185E85  je       0x185fa6  ; -> 00185FA6
00185E8B  movaps   xmmword ptr [rsp + 0x80], xmm6
00185E93  movaps   xmmword ptr [rsp + 0x70], xmm7
00185E98  movaps   xmmword ptr [rsp + 0x60], xmm8
00185E9E  movaps   xmmword ptr [rsp + 0x50], xmm9
00185EA4  movaps   xmmword ptr [rsp + 0x40], xmm10
00185EAA  movaps   xmmword ptr [rsp + 0x30], xmm11
00185EB0  movaps   xmmword ptr [rsp + 0x20], xmm12
00185EB6  call     0x18a620  ; -> 0018A620 fn
00185EBB  movss    xmm9, dword ptr [rip + 0x1b65edc]  ; -> 01CEBDA0 [u32 0x80000000]
00185EC4  mov      rcx, qword ptr [rax + 0xc0]
00185ECB  xor      eax, eax
00185ECD  movss    xmm6, dword ptr [rcx + 0x10]
00185ED2  movss    xmm7, dword ptr [rcx + 0x14]
00185ED7  xorps    xmm6, xmm9
00185EDB  movss    xmm10, dword ptr [rcx + 0x20]
00185EE1  xorps    xmm7, xmm9
00185EE5  movss    xmm11, dword ptr [rcx + 0x24]
00185EEB  xorps    xmm10, xmm9
00185EEF  movss    xmm0, dword ptr [rcx + 0xc]
00185EF4  xorps    xmm11, xmm9
00185EF8  movss    xmm1, dword ptr [rcx + 0x1c]
00185EFD  xorps    xmm0, xmm9
00185F01  movss    xmm3, dword ptr [rcx]
00185F05  xorps    xmm1, xmm9
00185F09  movss    xmm4, dword ptr [rcx + 4]
00185F0E  xorps    xmm3, xmm9
00185F12  movss    xmm8, dword ptr [rcx + 0x18]
00185F18  xorps    xmm4, xmm9
00185F1C  movss    xmm12, dword ptr [rcx + 0x28]
00185F22  movss    xmm2, dword ptr [rcx + 0x2c]
00185F27  movss    xmm5, dword ptr [rcx + 8]
00185F2C  movaps   xmm9, xmmword ptr [rsp + 0x50]
00185F32  movss    dword ptr [rbx + 0x20], xmm6
00185F37  movaps   xmm6, xmmword ptr [rsp + 0x80]
00185F3F  movss    dword ptr [rbx + 0x24], xmm7
00185F44  movaps   xmm7, xmmword ptr [rsp + 0x70]
00185F49  movss    dword ptr [rbx + 0x30], xmm10
00185F4F  movaps   xmm10, xmmword ptr [rsp + 0x40]
00185F55  movss    dword ptr [rbx + 0x34], xmm11
00185F5B  movaps   xmm11, xmmword ptr [rsp + 0x30]
00185F61  movss    dword ptr [rbx + 0x28], xmm8
00185F67  movaps   xmm8, xmmword ptr [rsp + 0x60]
00185F6D  movss    dword ptr [rbx + 0x38], xmm12
00185F73  movaps   xmm12, xmmword ptr [rsp + 0x20]
00185F79  movss    dword ptr [rbx], xmm0
00185F7D  movss    dword ptr [rbx + 4], xmm1
00185F82  movss    dword ptr [rbx + 8], xmm2
00185F87  movss    dword ptr [rbx + 0x10], xmm3
00185F8C  movss    dword ptr [rbx + 0x14], xmm4
00185F91  movss    dword ptr [rbx + 0x18], xmm5
00185F96  mov      dword ptr [rbx + 0xc], eax
00185F99  mov      dword ptr [rbx + 0x1c], eax
00185F9C  mov      dword ptr [rbx + 0x2c], eax
00185F9F  mov      dword ptr [rbx + 0x3c], 0x3f800000
00185FA6  add      rsp, 0x90
00185FAD  pop      rbx
00185FAE  ret      
```

## 00217610 (383 B, extent 00217610-0021778F)

Entered from (direct sites whose caller this page cites): `00202D50` + 0x0 (jmp; `00202D50` is cited on this page)
Other direct sites: none

Host context: "56650' call).  ## SWE2-EC7-53 update (2026-09-19) - '003CBD60'  '003CBD60' (571 B) is the camera matrix rebuild the page describes - '00380190'/'00380650'/'003CBCA0' plus Movement helpers '00202B70'/'00202D50'/'00202E10', '00182310', '00D22740' rdata (the page note 'itself was not read' is now read). Interior anchor '003CBE17' (a '00380190' call).   ## SWE2-EC7-53 update (2026-09-19) - '00233230'  '00233230' (524 B) is a Movement-owned "

```
00217610  mov      r11, rsp
00217613  sub      rsp, 0x88
0021761A  movss    xmm5, dword ptr [rip + 0x1ad477e]  ; -> 01CEBDA0 [u32 0x80000000]
00217622  xor      eax, eax
00217624  movaps   xmmword ptr [rsp + 0x70], xmm6
00217629  movaps   xmmword ptr [rsp + 0x60], xmm7
0021762E  movaps   xmmword ptr [r11 - 0x38], xmm8
00217633  movups   xmm8, xmmword ptr [rdx + 0x30]
00217638  movaps   xmmword ptr [r11 - 0x48], xmm9
0021763D  movaps   xmmword ptr [r11 - 0x58], xmm10
00217642  movaps   xmm2, xmm8
00217646  movaps   xmmword ptr [r11 - 0x68], xmm11
0021764B  movaps   xmm6, xmm8
0021764F  movups   xmm11, xmmword ptr [rdx + 0x20]
00217654  movaps   xmmword ptr [r11 - 0x78], xmm12
00217659  movups   xmm12, xmmword ptr [rdx + 0x10]
0021765E  movaps   xmmword ptr [rsp], xmm13
00217663  movaps   xmm3, xmm11
00217667  movups   xmm13, xmmword ptr [rdx]
0021766B  shufps   xmm2, xmm8, 0x55
00217670  movaps   xmm7, xmm12
00217674  shufps   xmm6, xmm8, 0xaa
00217679  movaps   xmm0, xmm13
0021767D  mulss    xmm0, xmm8
00217682  movaps   xmm10, xmm13
00217686  shufps   xmm10, xmm13, 0x55
0021768B  movaps   xmm9, xmm13
0021768F  shufps   xmm9, xmm13, 0xaa
00217694  movaps   xmm1, xmm10
00217698  mulss    xmm1, xmm2
0021769C  movaps   xmm4, xmm12
002176A0  shufps   xmm7, xmm12, 0x55
002176A5  shufps   xmm4, xmm12, 0xaa
002176AA  addss    xmm1, xmm0
002176AE  shufps   xmm3, xmm11, 0x55
002176B3  movaps   xmm0, xmm9
002176B7  mulss    xmm0, xmm6
002176BB  addss    xmm1, xmm0
002176BF  movaps   xmm0, xmm12
002176C3  mulss    xmm0, xmm8
002176C8  xorps    xmm1, xmm5
002176CB  movss    dword ptr [rcx + 0x30], xmm1
002176D0  movaps   xmm1, xmm7
002176D3  mulss    xmm1, xmm2
002176D7  addss    xmm1, xmm0
002176DB  movaps   xmm0, xmm4
002176DE  mulss    xmm0, xmm6
002176E2  addss    xmm1, xmm0
002176E6  movaps   xmm0, xmm11
002176EA  mulss    xmm0, xmm8
002176EF  movaps   xmm8, xmmword ptr [r11 - 0x38]
002176F4  xorps    xmm1, xmm5
002176F7  movss    dword ptr [rcx + 0x34], xmm1
002176FC  movaps   xmm1, xmm3
002176FF  mulss    xmm1, xmm2
00217703  movaps   xmm2, xmm11
00217707  shufps   xmm2, xmm11, 0xaa
0021770C  addss    xmm1, xmm0
00217710  movaps   xmm0, xmm2
00217713  mulss    xmm0, xmm6
00217717  movaps   xmm6, xmmword ptr [rsp + 0x70]
0021771C  addss    xmm1, xmm0
00217720  xorps    xmm1, xmm5
00217723  movss    dword ptr [rcx + 0x38], xmm1
00217728  movss    dword ptr [rcx], xmm13
0021772D  movaps   xmm13, xmmword ptr [rsp]
00217732  movss    dword ptr [rcx + 4], xmm12
00217738  movaps   xmm12, xmmword ptr [r11 - 0x78]
0021773D  movss    dword ptr [rcx + 8], xmm11
00217743  movaps   xmm11, xmmword ptr [r11 - 0x68]
00217748  movss    dword ptr [rcx + 0x10], xmm10
0021774E  movaps   xmm10, xmmword ptr [r11 - 0x58]
00217753  movss    dword ptr [rcx + 0x14], xmm7
00217758  movaps   xmm7, xmmword ptr [rsp + 0x60]
0021775D  movss    dword ptr [rcx + 0x18], xmm3
00217762  movss    dword ptr [rcx + 0x20], xmm9
00217768  movaps   xmm9, xmmword ptr [r11 - 0x48]
0021776D  movss    dword ptr [rcx + 0x24], xmm4
00217772  movss    dword ptr [rcx + 0x28], xmm2
00217777  mov      dword ptr [rcx + 0xc], eax
0021777A  mov      dword ptr [rcx + 0x1c], eax
0021777D  mov      dword ptr [rcx + 0x2c], eax
00217780  mov      dword ptr [rcx + 0x3c], 0x3f800000
00217787  add      rsp, 0x88
0021778E  ret      
```

## 0028F6A0 (80 B, extent 0028F6A0-0028F6F0)

Entered from (direct sites whose caller this page cites): `0022A770` + 0x2E0 (call; `0022A770` is cited on this page)
Other direct sites: `002E2340` + 0x4 (call)

Host context: "plies, so the real figure is at or below that and is > **conditional, not fixed**. > > **And "per frame" is not established at all**: '00314370' is reached from several call sites (the > field frame '0022A770' at three and 'MainLoop_UpdateAndRenderFrame' at two, per the character > transform contract), so the number of invocations in a frame is a scheduling fact nobody has > measured. **A per-slot conditional quantity was being reported"

```
0028F6A0  sub      rsp, 0x28
0028F6A4  mov      rcx, qword ptr [rip + 0x1e0c7d5]  ; -> 0209BE80
0028F6AB  test     rcx, rcx
0028F6AE  jne      0x28f6b7  ; -> 0028F6B7
0028F6B0  xor      eax, eax
0028F6B2  add      rsp, 0x28
0028F6B6  ret      
0028F6B7  test     dword ptr [rcx + 0x10f68], 0x2000
0028F6C1  jne      0x28f6b0  ; -> 0028F6B0
0028F6C3  add      rcx, 0xab30
0028F6CA  call     0x273a20  ; -> 00273A20 fn
0028F6CF  test     eax, eax
0028F6D1  je       0x28f6b0  ; -> 0028F6B0
0028F6D3  mov      rax, qword ptr [rip + 0x1e0c7a6]  ; -> 0209BE80
0028F6DA  movzx    ecx, byte ptr [rax + 0x10f68]
0028F6E1  and      cl, 0x10
0028F6E4  neg      cl
0028F6E6  sbb      eax, eax
0028F6E8  add      eax, 2
0028F6EB  add      rsp, 0x28
0028F6EF  ret      
```

## 002E4E00 (78 B, extent 002E4E00-002E4E4E)

Entered from (direct sites whose caller this page cites): `00357F00` + 0x115 (call; `00357F00` is cited on this page)
Other direct sites: none

Host context: "l the start '003DD230'; '00349ED0' and '0034A370' call the stop '003DD320'; '0034B100' calls the clear '003DCF60'; '0034C7E0' calls '00358320', which returns the current draw index as a signed byte; '00357F00' calls '003DA190', a 3-byte function that returns its argument; and 20 script bodies call the slot accessor '00263FF0', among them '0033F7F0', '00342490', '0034E460', '003574B0' and '0050D0C0'. Scripts start, stop and clear shakes "

```
002E4E00  test     rcx, rcx
002E4E03  je       0x2e4e4a  ; -> 002E4E4A
002E4E05  mov      rax, qword ptr [rcx + 0xc0]
002E4E0C  test     rax, rax
002E4E0F  je       0x2e4e4a  ; -> 002E4E4A
002E4E11  cmp      dword ptr [rax], -1
002E4E14  je       0x2e4e4a  ; -> 002E4E4A
002E4E16  movzx    ecx, word ptr [rax]
002E4E19  cmp      cx, -1
002E4E1D  jne      0x2e4e28  ; -> 002E4E28
002E4E1F  movss    xmm0, dword ptr [rip + 0x1a06e75]  ; -> 01CEBC9C [f32 -1]
002E4E27  ret      
002E4E28  movsx    rax, cx
002E4E2C  imul     rcx, rax, 0x740
002E4E33  add      rcx, qword ptr [rip + 0x1fe20ee]  ; -> 022C6F28
002E4E3A  je       0x2e4e1f  ; -> 002E4E1F
002E4E3C  cmp      dword ptr [rcx + 0x284], 0
002E4E43  je       0x2e4e1f  ; -> 002E4E1F
002E4E45  jmp      0x423380  ; -> 00423380 fn
002E4E4A  xorps    xmm0, xmm0
002E4E4D  ret      
```

## 002E71C0 (208 B, extent 002E71C0-002E7290)

Entered from (direct sites whose caller this page cites): `00357F00` + 0x7A (call; `00357F00` is cited on this page); `00357F00` + 0x104 (call; `00357F00` is cited on this page); `00357F00` + 0x13E (call; `00357F00` is cited on this page)
Other direct sites: none

Host context: "l the start '003DD230'; '00349ED0' and '0034A370' call the stop '003DD320'; '0034B100' calls the clear '003DCF60'; '0034C7E0' calls '00358320', which returns the current draw index as a signed byte; '00357F00' calls '003DA190', a 3-byte function that returns its argument; and 20 script bodies call the slot accessor '00263FF0', among them '0033F7F0', '00342490', '0034E460', '003574B0' and '0050D0C0'. Scripts start, stop and clear shakes " / "l the start '003DD230'; '00349ED0' and '0034A370' call the stop '003DD320'; '0034B100' calls the clear '003DCF60'; '0034C7E0' calls '00358320', which returns the current draw index as a signed byte; '00357F00' calls '003DA190', a 3-byte function that returns its argument; and 20 script bodies call the slot accessor '00263FF0', among them '0033F7F0', '00342490', '0034E460', '003574B0' and '0050D0C0'. Scripts start, stop and clear shakes "

```
002E71C0  mov      qword ptr [rsp + 8], rbx
002E71C5  mov      qword ptr [rsp + 0x10], rsi
002E71CA  push     rdi
002E71CB  sub      rsp, 0x20
002E71CF  xor      ebx, ebx
002E71D1  mov      rsi, rcx
002E71D4  test     rcx, rcx
002E71D7  je       0x2e7229  ; -> 002E7229
002E71D9  mov      rax, qword ptr [rcx + 0xc0]
002E71E0  test     rax, rax
002E71E3  je       0x2e7229  ; -> 002E7229
002E71E5  cmp      dword ptr [rax], -1
002E71E8  je       0x2e7229  ; -> 002E7229
002E71EA  movzx    ecx, word ptr [rax]
002E71ED  cmp      cx, -1
002E71F1  jne      0x2e71f7  ; -> 002E71F7
002E71F3  mov      edi, ebx
002E71F5  jmp      0x2e722e  ; -> 002E722E
002E71F7  movsx    rax, cx
002E71FB  imul     rcx, rax, 0x740
002E7202  add      rcx, qword ptr [rip + 0x1fdfd1f]  ; -> 022C6F28
002E7209  jne      0x2e720f  ; -> 002E720F
002E720B  mov      edi, ebx
002E720D  jmp      0x2e722e  ; -> 002E722E
002E720F  cmp      dword ptr [rcx + 0x284], ebx
002E7215  jne      0x2e721b  ; -> 002E721B
002E7217  mov      edi, ebx
002E7219  jmp      0x2e722e  ; -> 002E722E
002E721B  mov      edx, 3
002E7220  call     0x41e690  ; -> 0041E690 fn
002E7225  mov      edi, eax
002E7227  jmp      0x2e722e  ; -> 002E722E
002E7229  mov      edi, 1
002E722E  test     rsi, rsi
002E7231  je       0x2e7277  ; -> 002E7277
002E7233  mov      rax, qword ptr [rsi + 0xc0]
002E723A  test     rax, rax
002E723D  je       0x2e7277  ; -> 002E7277
002E723F  cmp      dword ptr [rax], -1
002E7242  je       0x2e7277  ; -> 002E7277
002E7244  movzx    ecx, word ptr [rax]
002E7247  cmp      cx, -1
002E724B  je       0x2e727c  ; -> 002E727C
002E724D  movsx    rax, cx
002E7251  imul     rcx, rax, 0x740
002E7258  add      rcx, qword ptr [rip + 0x1fdfcc9]  ; -> 022C6F28
002E725F  je       0x2e727c  ; -> 002E727C
002E7261  cmp      dword ptr [rcx + 0x284], ebx
002E7267  je       0x2e727c  ; -> 002E727C
002E7269  mov      edx, 4
002E726E  call     0x41e690  ; -> 0041E690 fn
002E7273  mov      ebx, eax
002E7275  jmp      0x2e727c  ; -> 002E727C
002E7277  mov      ebx, 1
002E727C  mov      rsi, qword ptr [rsp + 0x38]
002E7281  or       ebx, edi
002E7283  mov      eax, ebx
002E7285  mov      rbx, qword ptr [rsp + 0x30]
002E728A  add      rsp, 0x20
002E728E  pop      rdi
002E728F  ret      
```

## 003600C0 (11 B, extent 003600C0-003600CB)

Entered from (direct sites whose caller this page cites): `002498B0` + 0x356 (call; `002498B0` is cited on this page)
Other direct sites: none

Host context: " matrix rebuild also uses, not a camera crossing.  **Input — OUT-OF-SCOPE and CLIENT (12 edges).** The field frame '0022A770' calls '0017DE60', 'InputGameplay_RebuildFrameSnapshotFromChannelHistory' '002498B0', '00250180', '0035AE30', '0035AF20', 'InputControl_SetOneShotFrameCallback' '0035E9A0', '0035FF90', 'InputGameplay_RebuildRemappedTransitionMaskState' '0036FDF0', 'InputGameplay_GetRemappedHistoryMask04' '0036FF70' and 'InputGamep"

```
003600C0  movaps   xmm0, xmmword ptr [rip + 0x1f6b5f9]  ; -> 022CB6C0
003600C7  movups   xmmword ptr [rcx], xmm0
003600CA  ret      
```

## 003A7AE0 (112 B, extent 003A7AE0-003A7B50)

Entered from (direct sites whose caller this page cites): `003ED8A0` + 0x167 (call; `003ED8A0` is cited on this page)
Other direct sites: none

Host context: "veView' ('00259820') | the active view behind the pointer '020972F0' | '0x14' | | '00259970' (17 B), called by the frame body before its second draw | the static default view '02097B80' | '0x14' | | '003ED8A0', in the effect-file data parse | the effect's camera at '02096D30' | '0x64' |  ## 3. Choosing - the first stage of '003820C0'  The camera update (2,125 B; one caller, a five-byte-call wrapper just below the graphics sync routines)"

```
003A7AE0  mov      qword ptr [rsp + 8], rbx
003A7AE5  mov      qword ptr [rsp + 0x10], rbp
003A7AEA  mov      qword ptr [rsp + 0x18], rsi
003A7AEF  push     rdi
003A7AF0  sub      rsp, 0x20
003A7AF4  movzx    esi, byte ptr [rcx + 1]
003A7AF8  mov      rdi, rcx
003A7AFB  movzx    ecx, byte ptr [rcx]
003A7AFE  movsxd   rbp, edx
003A7B01  call     0x3a78a0  ; -> 003A78A0 fn
003A7B06  test     rax, rax
003A7B09  je       0x3a7b39  ; -> 003A7B39
003A7B0B  movzx    edx, sil
003A7B0F  mov      rcx, rax
003A7B12  call     0x334000  ; -> 00334000 fn
003A7B17  test     rax, rax
003A7B1A  je       0x3a7b39  ; -> 003A7B39
003A7B1C  mov      ecx, dword ptr [rdi + 4]
003A7B1F  lea      rdx, [rdi + 8]
003A7B23  mov      dword ptr [rax], ecx
003A7B25  lea      rcx, [rax + 4]
003A7B29  movzx    r8d, byte ptr [rax + 2]
003A7B2E  call     0x861eba  ; -> 00861EBA fn
003A7B33  lea      rax, [rdi + rbp]
003A7B37  jmp      0x3a7b3b  ; -> 003A7B3B
003A7B39  xor      eax, eax
003A7B3B  mov      rbx, qword ptr [rsp + 0x30]
003A7B40  mov      rbp, qword ptr [rsp + 0x38]
003A7B45  mov      rsi, qword ptr [rsp + 0x40]
003A7B4A  add      rsp, 0x20
003A7B4E  pop      rdi
003A7B4F  ret      
```
