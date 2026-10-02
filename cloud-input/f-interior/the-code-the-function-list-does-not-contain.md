# F-interior pack: `99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-code-the-function-list-does-not-contain.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 4e32dd8df	FABLE: GI-1..GI-11 and GI-13 answered (GI-12 already at 6facc53bc) - UI screens, dialogs, save/load,; inbox mentions: REVIEW-POLICY.md, SWE2-AUDIT-SPEC.md). OPUS read these before packing.

## 001274D0 (193 B, extent 001274D0-00127591)

Page context: "unction list is a reference-derived census**, to within **356 bodies by admissible routes** ~~eight bodies~~. Eight carry no reference by any route at all, and five of those sit in this same window: '001274D0', '00129870', '0012A290', '0012B980' and '00147B00', two of them tagged 'DCT8x8'. So the tool did find a handful of these assembly bodies by some other route and missed the rest. **The shortfall is explained without any appeal to t"

```
001274D0  sub      rsp, 0x20
001274D4  movdqu   xmmword ptr [rsp], xmm6
001274D9  movdqu   xmmword ptr [rsp + 0x10], xmm7
001274DF  lea      r10, [rcx + rdx*2]
001274E3  movdqu   xmm0, xmmword ptr [rcx]
001274E7  movdqu   xmm1, xmmword ptr [rcx + 0x10]
001274EC  movdqu   xmm2, xmmword ptr [rcx + rdx]
001274F1  movdqu   xmm3, xmmword ptr [rcx + rdx + 0x10]
001274F7  movdqu   xmm4, xmmword ptr [r10]
001274FC  movdqu   xmm5, xmmword ptr [r10 + 0x10]
00127502  movdqu   xmm6, xmmword ptr [r10 + rdx]
00127508  movdqu   xmm7, xmmword ptr [r10 + rdx + 0x10]
0012750F  lea      rcx, [rcx + rdx*4]
00127513  lea      r10, [r8 + r9*2]
00127517  movdqa   xmmword ptr [r8], xmm0
0012751C  movdqa   xmmword ptr [r8 + 0x10], xmm1
00127522  movdqa   xmmword ptr [r8 + r9], xmm2
00127528  movdqa   xmmword ptr [r8 + r9 + 0x10], xmm3
0012752F  movdqa   xmmword ptr [r10], xmm4
00127534  movdqa   xmmword ptr [r10 + 0x10], xmm5
0012753A  movdqa   xmmword ptr [r10 + r9], xmm6
00127540  movdqa   xmmword ptr [r10 + r9 + 0x10], xmm7
00127547  lea      r8, [r8 + r9*4]
0012754B  sub      dword ptr [rsp + 0x48], 4
00127550  cmp      dword ptr [rsp + 0x48], 4
00127555  jge      0x1274df  ; -> 001274DF
00127557  cmp      dword ptr [rsp + 0x48], 0
0012755C  je       0x127581  ; -> 00127581
0012755E  movdqu   xmm0, xmmword ptr [rcx]
00127562  movdqu   xmm1, xmmword ptr [rcx + 0x10]
00127567  lea      rcx, [rcx + rdx]
0012756B  movdqa   xmmword ptr [r8], xmm0
00127570  movdqa   xmmword ptr [r8 + 0x10], xmm1
00127576  lea      r8, [r8 + r9]
0012757A  sub      dword ptr [rsp + 0x48], 1
0012757F  jne      0x12755e  ; -> 0012755E
00127581  movdqu   xmm7, xmmword ptr [rsp + 0x10]
00127587  movdqu   xmm6, xmmword ptr [rsp]
0012758C  add      rsp, 0x20
00127590  ret      
```

## 00129870 (885 B, extent 00129870-00129BE5)

Page context: " is a reference-derived census**, to within **356 bodies by admissible routes** ~~eight bodies~~. Eight carry no reference by any route at all, and five of those sit in this same window: '001274D0', '00129870', '0012A290', '0012B980' and '00147B00', two of them tagged 'DCT8x8'. So the tool did find a handful of these assembly bodies by some other route and missed the rest. **The shortfall is explained without any appeal to the tool's in"

```
00129870  sub      rsp, 0x20
00129874  movdqu   xmmword ptr [rsp], xmm6
00129879  movdqu   xmmword ptr [rsp + 0x10], xmm7
0012987F  movdqa   xmm0, xmmword ptr [rcx]
00129883  lddqu    xmm5, xmmword ptr [r8]
00129888  lddqu    xmm6, xmmword ptr [r8 + 1]
0012988E  lddqu    xmm7, xmmword ptr [r8 + 2]
00129894  psadbw   xmm5, xmm0
00129898  psadbw   xmm6, xmm0
0012989C  psadbw   xmm7, xmm0
001298A0  movdqa   xmm0, xmmword ptr [rcx + rdx]
001298A5  lddqu    xmm1, xmmword ptr [r8 + r9]
001298AB  lddqu    xmm2, xmmword ptr [r8 + r9 + 1]
001298B2  lddqu    xmm3, xmmword ptr [r8 + r9 + 2]
001298B9  lea      rcx, [rcx + rdx*2]
001298BD  lea      r8, [r8 + r9*2]
001298C1  psadbw   xmm1, xmm0
001298C5  psadbw   xmm2, xmm0
001298C9  psadbw   xmm3, xmm0
001298CD  paddw    xmm5, xmm1
001298D1  paddw    xmm6, xmm2
001298D5  paddw    xmm7, xmm3
001298D9  movdqa   xmm0, xmmword ptr [rcx]
001298DD  lddqu    xmm1, xmmword ptr [r8]
001298E2  lddqu    xmm2, xmmword ptr [r8 + 1]
001298E8  lddqu    xmm3, xmmword ptr [r8 + 2]
001298EE  psadbw   xmm1, xmm0
001298F2  psadbw   xmm2, xmm0
001298F6  psadbw   xmm3, xmm0
001298FA  paddw    xmm5, xmm1
001298FE  paddw    xmm6, xmm2
00129902  paddw    xmm7, xmm3
00129906  movdqa   xmm0, xmmword ptr [rcx + rdx]
0012990B  lddqu    xmm1, xmmword ptr [r8 + r9]
00129911  lddqu    xmm2, xmmword ptr [r8 + r9 + 1]
00129918  lddqu    xmm3, xmmword ptr [r8 + r9 + 2]
0012991F  lea      rcx, [rcx + rdx*2]
00129923  lea      r8, [r8 + r9*2]
00129927  psadbw   xmm1, xmm0
0012992B  psadbw   xmm2, xmm0
0012992F  psadbw   xmm3, xmm0
00129933  paddw    xmm5, xmm1
00129937  paddw    xmm6, xmm2
0012993B  paddw    xmm7, xmm3
0012993F  movdqa   xmm0, xmmword ptr [rcx]
00129943  lddqu    xmm1, xmmword ptr [r8]
00129948  lddqu    xmm2, xmmword ptr [r8 + 1]
0012994E  lddqu    xmm3, xmmword ptr [r8 + 2]
00129954  psadbw   xmm1, xmm0
00129958  psadbw   xmm2, xmm0
0012995C  psadbw   xmm3, xmm0
00129960  paddw    xmm5, xmm1
00129964  paddw    xmm6, xmm2
00129968  paddw    xmm7, xmm3
0012996C  movdqa   xmm0, xmmword ptr [rcx + rdx]
00129971  lddqu    xmm1, xmmword ptr [r8 + r9]
00129977  lddqu    xmm2, xmmword ptr [r8 + r9 + 1]
0012997E  lddqu    xmm3, xmmword ptr [r8 + r9 + 2]
00129985  lea      rcx, [rcx + rdx*2]
00129989  lea      r8, [r8 + r9*2]
0012998D  psadbw   xmm1, xmm0
00129991  psadbw   xmm2, xmm0
00129995  psadbw   xmm3, xmm0
00129999  paddw    xmm5, xmm1
0012999D  paddw    xmm6, xmm2
001299A1  paddw    xmm7, xmm3
001299A5  movdqa   xmm0, xmmword ptr [rcx]
001299A9  lddqu    xmm1, xmmword ptr [r8]
001299AE  lddqu    xmm2, xmmword ptr [r8 + 1]
001299B4  lddqu    xmm3, xmmword ptr [r8 + 2]
001299BA  psadbw   xmm1, xmm0
001299BE  psadbw   xmm2, xmm0
001299C2  psadbw   xmm3, xmm0
001299C6  paddw    xmm5, xmm1
001299CA  paddw    xmm6, xmm2
001299CE  paddw    xmm7, xmm3
001299D2  movdqa   xmm0, xmmword ptr [rcx + rdx]
001299D7  lddqu    xmm1, xmmword ptr [r8 + r9]
001299DD  lddqu    xmm2, xmmword ptr [r8 + r9 + 1]
001299E4  lddqu    xmm3, xmmword ptr [r8 + r9 + 2]
001299EB  lea      rcx, [rcx + rdx*2]
001299EF  lea      r8, [r8 + r9*2]
001299F3  psadbw   xmm1, xmm0
001299F7  psadbw   xmm2, xmm0
001299FB  psadbw   xmm3, xmm0
001299FF  paddw    xmm5, xmm1
00129A03  paddw    xmm6, xmm2
00129A07  paddw    xmm7, xmm3
00129A0B  movdqa   xmm0, xmmword ptr [rcx]
00129A0F  lddqu    xmm1, xmmword ptr [r8]
00129A14  lddqu    xmm2, xmmword ptr [r8 + 1]
00129A1A  lddqu    xmm3, xmmword ptr [r8 + 2]
00129A20  psadbw   xmm1, xmm0
00129A24  psadbw   xmm2, xmm0
00129A28  psadbw   xmm3, xmm0
00129A2C  paddw    xmm5, xmm1
00129A30  paddw    xmm6, xmm2
00129A34  paddw    xmm7, xmm3
00129A38  movdqa   xmm0, xmmword ptr [rcx + rdx]
00129A3D  lddqu    xmm1, xmmword ptr [r8 + r9]
00129A43  lddqu    xmm2, xmmword ptr [r8 + r9 + 1]
00129A4A  lddqu    xmm3, xmmword ptr [r8 + r9 + 2]
00129A51  lea      rcx, [rcx + rdx*2]
00129A55  lea      r8, [r8 + r9*2]
00129A59  psadbw   xmm1, xmm0
00129A5D  psadbw   xmm2, xmm0
00129A61  psadbw   xmm3, xmm0
00129A65  paddw    xmm5, xmm1
00129A69  paddw    xmm6, xmm2
00129A6D  paddw    xmm7, xmm3
00129A71  movdqa   xmm0, xmmword ptr [rcx]
00129A75  lddqu    xmm1, xmmword ptr [r8]
00129A7A  lddqu    xmm2, xmmword ptr [r8 + 1]
00129A80  lddqu    xmm3, xmmword ptr [r8 + 2]
00129A86  psadbw   xmm1, xmm0
00129A8A  psadbw   xmm2, xmm0
00129A8E  psadbw   xmm3, xmm0
00129A92  paddw    xmm5, xmm1
00129A96  paddw    xmm6, xmm2
00129A9A  paddw    xmm7, xmm3
00129A9E  movdqa   xmm0, xmmword ptr [rcx + rdx]
00129AA3  lddqu    xmm1, xmmword ptr [r8 + r9]
00129AA9  lddqu    xmm2, xmmword ptr [r8 + r9 + 1]
00129AB0  lddqu    xmm3, xmmword ptr [r8 + r9 + 2]
00129AB7  lea      rcx, [rcx + rdx*2]
00129ABB  lea      r8, [r8 + r9*2]
00129ABF  psadbw   xmm1, xmm0
00129AC3  psadbw   xmm2, xmm0
00129AC7  psadbw   xmm3, xmm0
00129ACB  paddw    xmm5, xmm1
00129ACF  paddw    xmm6, xmm2
00129AD3  paddw    xmm7, xmm3
00129AD7  movdqa   xmm0, xmmword ptr [rcx]
00129ADB  lddqu    xmm1, xmmword ptr [r8]
00129AE0  lddqu    xmm2, xmmword ptr [r8 + 1]
00129AE6  lddqu    xmm3, xmmword ptr [r8 + 2]
00129AEC  psadbw   xmm1, xmm0
00129AF0  psadbw   xmm2, xmm0
00129AF4  psadbw   xmm3, xmm0
00129AF8  paddw    xmm5, xmm1
00129AFC  paddw    xmm6, xmm2
00129B00  paddw    xmm7, xmm3
00129B04  movdqa   xmm0, xmmword ptr [rcx + rdx]
00129B09  lddqu    xmm1, xmmword ptr [r8 + r9]
00129B0F  lddqu    xmm2, xmmword ptr [r8 + r9 + 1]
00129B16  lddqu    xmm3, xmmword ptr [r8 + r9 + 2]
00129B1D  lea      rcx, [rcx + rdx*2]
00129B21  lea      r8, [r8 + r9*2]
00129B25  psadbw   xmm1, xmm0
00129B29  psadbw   xmm2, xmm0
00129B2D  psadbw   xmm3, xmm0
00129B31  paddw    xmm5, xmm1
00129B35  paddw    xmm6, xmm2
00129B39  paddw    xmm7, xmm3
00129B3D  movdqa   xmm0, xmmword ptr [rcx]
00129B41  lddqu    xmm1, xmmword ptr [r8]
00129B46  lddqu    xmm2, xmmword ptr [r8 + 1]
00129B4C  lddqu    xmm3, xmmword ptr [r8 + 2]
00129B52  psadbw   xmm1, xmm0
00129B56  psadbw   xmm2, xmm0
00129B5A  psadbw   xmm3, xmm0
00129B5E  paddw    xmm5, xmm1
00129B62  paddw    xmm6, xmm2
00129B66  paddw    xmm7, xmm3
00129B6A  movdqa   xmm0, xmmword ptr [rcx + rdx]
00129B6F  lddqu    xmm1, xmmword ptr [r8 + r9]
00129B75  lddqu    xmm2, xmmword ptr [r8 + r9 + 1]
00129B7C  lddqu    xmm3, xmmword ptr [r8 + r9 + 2]
00129B83  psadbw   xmm1, xmm0
00129B87  psadbw   xmm2, xmm0
00129B8B  psadbw   xmm3, xmm0
00129B8F  paddw    xmm5, xmm1
00129B93  paddw    xmm6, xmm2
00129B97  paddw    xmm7, xmm3
00129B9B  mov      rcx, qword ptr [rsp + 0x48]
00129BA0  movq     xmm0, xmm5
00129BA4  psrldq   xmm5, 8
00129BA9  paddw    xmm0, xmm5
00129BAD  movd     dword ptr [rcx], xmm0
00129BB1  movq     xmm0, xmm6
00129BB5  psrldq   xmm6, 8
00129BBA  paddw    xmm0, xmm6
00129BBE  movd     dword ptr [rcx + 4], xmm0
00129BC3  movq     xmm0, xmm7
00129BC7  psrldq   xmm7, 8
00129BCC  paddw    xmm0, xmm7
00129BD0  movd     dword ptr [rcx + 8], xmm0
00129BD5  movdqu   xmm7, xmmword ptr [rsp + 0x10]
00129BDB  movdqu   xmm6, xmmword ptr [rsp]
00129BE0  add      rsp, 0x20
00129BE4  ret      
```

## 0012A290 (636 B, extent 0012A290-0012A50C)

Page context: "ag | |---|---|---| | '0012C02C' +31,508 | '0012B980' | 'Math.Transform.DCT8x8.FixedPointInverseAddClampPix' | | '00133BBF' +81,729 | '00133B40' | 'Media.ImageProcessing.SIMD' | | '0012A50C' +5,236 | '0012A290' | 'NativeInline.AcyclicControlFlow.ExtendedBounded' | | '0014C4E6' +50,778 | '0014C221' | 'NativeInline.AcyclicControlFlow.ExtendedBounded' |  The code reads the same way: 'pmullw' / 'paddw' / 'psraw 4' / 'packuswb' / 'pavgb' / 'p"

```
0012A290  sub      rsp, 0x48
0012A294  movaps   xmmword ptr [rsp + 0x50], xmm6
0012A299  movaps   xmmword ptr [rsp + 0x60], xmm7
0012A29E  movaps   xmmword ptr [rsp + 0x20], xmm8
0012A2A4  movaps   xmmword ptr [rsp + 0x30], xmm9
0012A2AA  lea      r9, [rdx + rdx]
0012A2AE  lea      r10, [rdx*4]
0012A2B6  movdqa   xmm0, xmmword ptr [rcx]
0012A2BA  movdqa   xmm1, xmmword ptr [rcx + r9]
0012A2C0  lea      rcx, [rcx + r10]
0012A2C4  movdqa   xmm2, xmmword ptr [rcx]
0012A2C8  movdqa   xmm3, xmmword ptr [rcx + r9]
0012A2CE  lea      rcx, [rcx + r10]
0012A2D2  movdqa   xmm4, xmmword ptr [rcx]
0012A2D6  movdqa   xmm5, xmmword ptr [rcx + r9]
0012A2DC  lea      rcx, [rcx + r10]
0012A2E0  movdqa   xmm6, xmmword ptr [rcx]
0012A2E4  movdqa   xmm7, xmmword ptr [rcx + r9]
0012A2EA  movdqa   xmm8, xmm0
0012A2EF  psubw    xmm8, xmm1
0012A2F4  movdqa   xmm9, xmm2
0012A2F9  psubw    xmm9, xmm3
0012A2FE  paddw    xmm0, xmm1
0012A302  paddw    xmm2, xmm3
0012A306  movdqa   xmm1, xmm4
0012A30A  psubw    xmm1, xmm5
0012A30E  movdqa   xmm3, xmm6
0012A312  psubw    xmm3, xmm7
0012A316  paddw    xmm4, xmm5
0012A31A  paddw    xmm6, xmm7
0012A31E  movdqa   xmm5, xmm0
0012A322  psubw    xmm5, xmm2
0012A326  movdqa   xmm7, xmm8
0012A32B  psubw    xmm7, xmm9
0012A330  paddw    xmm0, xmm2
0012A334  paddw    xmm8, xmm9
0012A339  movdqa   xmm2, xmm4
0012A33D  psubw    xmm2, xmm6
0012A341  movdqa   xmm9, xmm1
0012A346  psubw    xmm9, xmm3
0012A34B  paddw    xmm4, xmm6
0012A34F  paddw    xmm1, xmm3
0012A353  movdqa   xmm6, xmm0
0012A357  psubw    xmm6, xmm4
0012A35B  movdqa   xmm3, xmm8
0012A360  psubw    xmm3, xmm1
0012A364  paddw    xmm0, xmm4
0012A368  paddw    xmm8, xmm1
0012A36D  movdqa   xmm4, xmm5
0012A371  psubw    xmm4, xmm2
0012A375  movdqa   xmm1, xmm7
0012A379  psubw    xmm1, xmm9
0012A37E  paddw    xmm5, xmm2
0012A382  paddw    xmm7, xmm9
0012A387  movdqa   xmm9, xmm0
0012A38C  punpckhwd xmm9, xmm8
0012A391  punpcklwd xmm0, xmm8
0012A396  movdqa   xmm8, xmm5
0012A39B  punpckhwd xmm8, xmm7
0012A3A0  punpcklwd xmm5, xmm7
0012A3A4  movdqa   xmm7, xmm6
0012A3A8  punpckhwd xmm7, xmm3
0012A3AC  punpcklwd xmm6, xmm3
0012A3B0  movdqa   xmm3, xmm4
0012A3B4  punpckhwd xmm3, xmm1
0012A3B8  punpcklwd xmm4, xmm1
0012A3BC  movdqa   xmm1, xmm0
0012A3C0  punpckhdq xmm1, xmm5
0012A3C4  punpckldq xmm0, xmm5
0012A3C8  movdqa   xmm5, xmm9
0012A3CD  punpckhdq xmm5, xmm8
0012A3D2  punpckldq xmm9, xmm8
0012A3D7  movdqa   xmm8, xmm6
0012A3DC  punpckhdq xmm8, xmm4
0012A3E1  punpckldq xmm6, xmm4
0012A3E5  movdqa   xmm4, xmm7
0012A3E9  punpckhdq xmm4, xmm3
0012A3ED  punpckldq xmm7, xmm3
0012A3F1  movdqa   xmm3, xmm0
0012A3F5  punpckhqdq xmm3, xmm6
0012A3F9  punpcklqdq xmm0, xmm6
0012A3FD  movdqa   xmm6, xmm1
0012A401  punpckhqdq xmm6, xmm8
0012A406  punpcklqdq xmm1, xmm8
0012A40B  movdqa   xmm8, xmm9
0012A410  punpckhqdq xmm8, xmm7
0012A415  punpcklqdq xmm9, xmm7
0012A41A  movdqa   xmm7, xmm5
0012A41E  punpckhqdq xmm7, xmm4
0012A422  punpcklqdq xmm5, xmm4
0012A426  movdqa   xmm2, xmm0
0012A42A  psubw    xmm2, xmm3
0012A42E  movdqa   xmm4, xmm1
0012A432  psubw    xmm4, xmm6
0012A436  paddw    xmm0, xmm3
0012A43A  paddw    xmm1, xmm6
0012A43E  movdqa   xmm3, xmm9
0012A443  psubw    xmm3, xmm8
0012A448  movdqa   xmm6, xmm5
0012A44C  psubw    xmm6, xmm7
0012A450  paddw    xmm9, xmm8
0012A455  paddw    xmm5, xmm7
0012A459  movdqa   xmm8, xmm0
0012A45E  psubw    xmm8, xmm1
0012A463  movdqa   xmm7, xmm2
0012A467  psubw    xmm7, xmm4
0012A46B  paddw    xmm0, xmm1
0012A46F  paddw    xmm2, xmm4
0012A473  movdqa   xmm1, xmm9
0012A478  psubw    xmm1, xmm5
0012A47C  movdqa   xmm4, xmm3
0012A480  psubw    xmm4, xmm6
0012A484  paddw    xmm9, xmm5
0012A489  paddw    xmm3, xmm6
0012A48D  movdqa   xmm5, xmm0
0012A491  psubw    xmm5, xmm9
0012A496  movdqa   xmm6, xmm2
0012A49A  psubw    xmm6, xmm3
0012A49E  paddw    xmm0, xmm9
0012A4A3  paddw    xmm2, xmm3
0012A4A7  movdqa   xmm9, xmm8
0012A4AC  psubw    xmm9, xmm1
0012A4B1  movdqa   xmm3, xmm7
0012A4B5  psubw    xmm3, xmm4
0012A4B9  paddw    xmm8, xmm1
0012A4BE  paddw    xmm7, xmm4
0012A4C2  movdqa   xmmword ptr [r8], xmm0
0012A4C7  movdqa   xmmword ptr [r8 + 0x10], xmm2
0012A4CD  movdqa   xmmword ptr [r8 + 0x20], xmm8
0012A4D3  movdqa   xmmword ptr [r8 + 0x30], xmm7
0012A4D9  movdqa   xmmword ptr [r8 + 0x40], xmm5
0012A4DF  movdqa   xmmword ptr [r8 + 0x50], xmm6
0012A4E5  movdqa   xmmword ptr [r8 + 0x60], xmm9
0012A4EB  movdqa   xmmword ptr [r8 + 0x70], xmm3
0012A4F1  movaps   xmm9, xmmword ptr [rsp + 0x30]
0012A4F7  movaps   xmm8, xmmword ptr [rsp + 0x20]
0012A4FD  add      rsp, 0x48
0012A501  movaps   xmm7, xmmword ptr [rsp + 0x18]
0012A506  movaps   xmm6, xmmword ptr [rsp + 8]
0012A50B  ret      
```

## 0026A420 (111 B, extent 0026A420-0026A48F)

Page context: "'00229DF0' / '00229E70', and '0057FE80' asks '001EDEC0'.  **Movement, Presentation, Platform and PlatformOnlineAchievements — MECHANICAL, seven edges.** - '002ED6A0' is called by the movement bodies '0026A420' / '002E4A40' and calls '0026E530'. - The generic indexed dword store '001DF340' is called by the console dispatcher '001D1660', the platform init   '001DD170' and the online init '007A0C60'. - '004232D0' is called by '00426560'.  "

```
0026A420  movzx    eax, byte ptr [rcx + 3]
0026A424  and      al, 0xe0
0026A426  cmp      al, 0x60
0026A428  je       0x2e5b00  ; -> 002E5B00 fn
0026A42E  ret      
0026A42F  int3     
0026A430  test     edx, edx
0026A432  setne    r8b
0026A436  and      byte ptr [rcx + 8], 0xf7
0026A43A  and      byte ptr [rcx + 9], 0xbf
0026A43E  and      r8b, 1
0026A442  movzx    eax, r8b
0026A446  shl      r8b, 6
0026A44A  or       byte ptr [rcx + 9], r8b
0026A44E  shl      al, 3
0026A451  or       byte ptr [rcx + 8], al
0026A454  ret      
0026A455  int3     
0026A456  int3     
0026A457  int3     
0026A458  int3     
0026A459  int3     
0026A45A  int3     
0026A45B  int3     
0026A45C  int3     
0026A45D  int3     
0026A45E  int3     
0026A45F  int3     
0026A460  jmp      0x2ebc30  ; -> 002EBC30 fn
0026A465  int3     
0026A466  int3     
0026A467  int3     
0026A468  int3     
0026A469  int3     
0026A46A  int3     
0026A46B  int3     
0026A46C  int3     
0026A46D  int3     
0026A46E  int3     
0026A46F  int3     
0026A470  jmp      0x2ebbb0  ; -> 002EBBB0 fn
0026A475  int3     
0026A476  int3     
0026A477  int3     
0026A478  int3     
0026A479  int3     
0026A47A  int3     
0026A47B  int3     
0026A47C  int3     
0026A47D  int3     
0026A47E  int3     
0026A47F  int3     
0026A480  mov      qword ptr [rip + 0x1e2f8e9], rcx  ; -> 02099D70
0026A487  ret      
0026A488  int3     
0026A489  int3     
0026A48A  int3     
0026A48B  int3     
0026A48C  int3     
0026A48D  int3     
0026A48E  int3     
```
