# F-interior pack: `22-Middleware-PhyreEngine/the-camera-state-snapshot.md`

Generated 2026-10-03 03:15 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-camera-state-snapshot.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: cd6bd7f58	SWE2-DATA consolidated publish: progress-report cluster (generation store, R3 semantics, DB_GOAL, me; 2e935e586	SWE2-DATA: published answers incorporated - section 18's binding-record cells corrected (SD-122 / SD). OPUS read these before packing.

## 00216720 (2200 B, extent 00216720-00216FB8)

Page context: " vtable ('+0x30').  **The resolvers and the helper.** - The first source is a global block — '02AEEB20', the inverse of the head matrix at '02AEDD30'   ('003820C0' → '0024E180' stores the '00202D60'/'00216720' inverse there). Its resolver is one   'lea rax, [rip+..]; ret'. - The two trailing dwords are floats — '02AEEBA0' / '02AEEBA4', the camera's two distances taken through the   '02B40470' matrix to post-transform depth, pulled 3 uni"

```
00216720  mov      rax, rsp
00216723  sub      rsp, 0xe8
0021672A  movss    xmm1, dword ptr [rdx + 0x1c]
0021672F  movss    xmm0, dword ptr [rdx + 0x3c]
00216734  movss    xmm4, dword ptr [rdx + 0x28]
00216739  movss    xmm2, dword ptr [rdx + 0x24]
0021673E  movaps   xmm3, xmm4
00216741  mulss    xmm3, xmm0
00216745  movaps   xmmword ptr [rax - 0x18], xmm6
00216749  movss    xmm6, dword ptr [rdx + 0x18]
0021674E  movaps   xmmword ptr [rax - 0x28], xmm7
00216752  movaps   xmm7, xmm1
00216755  movaps   xmmword ptr [rax - 0x38], xmm8
0021675A  movss    xmm8, dword ptr [rdx + 0x2c]
00216760  movaps   xmmword ptr [rax - 0x48], xmm9
00216765  movss    xmm9, dword ptr [rdx + 0x38]
0021676B  movaps   xmmword ptr [rax - 0x58], xmm10
00216770  movaps   xmm5, xmm9
00216774  movaps   xmmword ptr [rax - 0x68], xmm11
00216779  movaps   xmm10, xmm6
0021677D  movss    xmm11, dword ptr [rdx + 0xc]
00216783  mulss    xmm10, xmm0
00216788  movaps   xmmword ptr [rax - 0x78], xmm12
0021678D  movss    xmm12, dword ptr [rdx + 8]
00216793  movaps   xmmword ptr [rsp + 0x60], xmm13
00216799  movaps   xmmword ptr [rsp + 0x50], xmm14
0021679F  movaps   xmmword ptr [rsp + 0x40], xmm15
002167A5  movaps   xmm13, xmm6
002167A9  movaps   xmm14, xmm1
002167AD  mulss    xmm5, xmm8
002167B2  movss    xmm15, dword ptr [rdx + 0x34]
002167B8  movaps   xmm6, xmm11
002167BC  mulss    xmm14, xmm4
002167C1  movaps   xmm4, xmm12
002167C5  mulss    xmm4, xmm0
002167C9  movss    xmm0, dword ptr [rdx + 0x14]
002167CE  mulss    xmm0, xmm3
002167D2  mulss    xmm6, xmm9
002167D7  mulss    xmm7, xmm9
002167DC  movss    xmm9, dword ptr [rdx + 8]
002167E2  mulss    xmm9, xmm1
002167E7  movaps   xmm1, xmm2
002167EA  mulss    xmm1, xmm7
002167EE  mulss    xmm2, xmm10
002167F3  addss    xmm1, xmm0
002167F7  mulss    xmm13, xmm8
002167FC  mulss    xmm12, xmm8
00216801  movaps   xmm8, xmm11
00216805  mulss    xmm8, dword ptr [rdx + 0x28]
0021680B  mulss    xmm11, dword ptr [rdx + 0x18]
00216811  movss    dword ptr [rsp + 4], xmm1
00216817  movaps   xmm1, xmm15
0021681B  movss    xmm0, dword ptr [rsp + 4]
00216821  mulss    xmm1, xmm13
00216826  addss    xmm0, xmm1
0021682A  movaps   xmm1, xmm15
0021682E  mulss    xmm1, xmm14
00216833  movss    dword ptr [rsp + 4], xmm0
00216839  movss    xmm0, dword ptr [rdx + 0x14]
0021683E  mulss    xmm0, xmm5
00216842  addss    xmm2, xmm0
00216846  movss    xmm0, dword ptr [rsp + 4]
0021684C  addss    xmm2, xmm1
00216850  subss    xmm0, xmm2
00216854  movss    xmm2, dword ptr [rdx + 0x24]
00216859  movaps   xmm1, xmm2
0021685C  mulss    xmm2, xmm6
00216860  mulss    xmm1, xmm4
00216864  movss    dword ptr [rsp + 4], xmm0
0021686A  movss    xmm0, dword ptr [rdx + 4]
0021686F  mulss    xmm0, xmm5
00216873  addss    xmm1, xmm0
00216877  movss    dword ptr [rsp], xmm1
0021687C  movaps   xmm1, xmm15
00216880  movss    xmm0, dword ptr [rsp]
00216885  mulss    xmm1, xmm8
0021688A  addss    xmm0, xmm1
0021688E  movaps   xmm1, xmm15
00216892  mulss    xmm1, xmm12
00216897  movss    dword ptr [rsp], xmm0
0021689C  movss    xmm0, dword ptr [rdx + 4]
002168A1  mulss    xmm0, xmm3
002168A5  addss    xmm2, xmm0
002168A9  addss    xmm2, xmm1
002168AD  movss    xmm0, dword ptr [rsp]
002168B2  subss    xmm0, xmm2
002168B6  movss    xmm2, dword ptr [rdx + 0x14]
002168BB  movaps   xmm1, xmm2
002168BE  mulss    xmm2, xmm4
002168C2  mulss    xmm1, xmm6
002168C6  movss    dword ptr [rsp], xmm0
002168CB  movss    xmm0, dword ptr [rdx + 4]
002168D0  mulss    xmm0, xmm10
002168D5  addss    xmm1, xmm0
002168D9  movss    dword ptr [rsp + 8], xmm1
002168DF  movaps   xmm1, xmm15
002168E3  movss    xmm0, dword ptr [rsp + 8]
002168E9  mulss    xmm1, xmm9
002168EE  addss    xmm0, xmm1
002168F2  movaps   xmm1, xmm15
002168F6  mulss    xmm1, xmm11
002168FB  movss    dword ptr [rsp + 8], xmm0
00216901  movss    xmm0, dword ptr [rdx + 4]
00216906  mulss    xmm0, xmm7
0021690A  addss    xmm2, xmm0
0021690E  movss    xmm0, dword ptr [rsp + 8]
00216914  addss    xmm2, xmm1
00216918  subss    xmm0, xmm2
0021691C  movss    xmm2, dword ptr [rdx + 0x14]
00216921  movaps   xmm1, xmm2
00216924  mulss    xmm2, xmm8
00216929  mulss    xmm1, xmm12
0021692E  movss    dword ptr [rsp + 8], xmm0
00216934  movss    xmm0, dword ptr [rdx + 4]
00216939  mulss    xmm0, xmm14
0021693E  addss    xmm1, xmm0
00216942  movss    dword ptr [rsp + 0xc], xmm1
00216948  movss    xmm0, dword ptr [rsp + 0xc]
0021694E  movss    xmm1, dword ptr [rdx + 0x24]
00216953  mulss    xmm1, xmm11
00216958  addss    xmm0, xmm1
0021695C  movss    xmm1, dword ptr [rdx + 0x24]
00216961  mulss    xmm1, xmm9
00216966  movss    dword ptr [rsp + 0xc], xmm0
0021696C  movss    xmm0, dword ptr [rdx + 4]
00216971  mulss    xmm0, xmm13
00216976  addss    xmm2, xmm0
0021697A  movss    xmm0, dword ptr [rsp + 0xc]
00216980  addss    xmm2, xmm1
00216984  subss    xmm0, xmm2
00216988  movss    xmm2, dword ptr [rdx + 0x20]
0021698D  movaps   xmm1, xmm2
00216990  mulss    xmm2, xmm7
00216994  mulss    xmm1, xmm10
00216999  movss    dword ptr [rsp + 0xc], xmm0
0021699F  movss    xmm0, dword ptr [rdx + 0x10]
002169A4  mulss    xmm0, xmm5
002169A8  addss    xmm1, xmm0
002169AC  movss    dword ptr [rsp + 0x10], xmm1
002169B2  movss    xmm0, dword ptr [rsp + 0x10]
002169B8  movss    xmm1, dword ptr [rdx + 0x30]
002169BD  mulss    xmm1, xmm14
002169C2  addss    xmm0, xmm1
002169C6  movss    xmm1, dword ptr [rdx + 0x30]
002169CB  mulss    xmm1, xmm13
002169D0  movss    dword ptr [rsp + 0x10], xmm0
002169D6  movss    xmm0, dword ptr [rdx + 0x10]
002169DB  mulss    xmm0, xmm3
002169DF  addss    xmm2, xmm0
002169E3  movss    xmm0, dword ptr [rsp + 0x10]
002169E9  addss    xmm2, xmm1
002169ED  subss    xmm0, xmm2
002169F1  movss    xmm2, dword ptr [rdx + 0x20]
002169F6  movaps   xmm1, xmm2
002169F9  mulss    xmm1, xmm6
002169FD  movss    dword ptr [rsp + 0x10], xmm0
00216A03  movss    xmm0, dword ptr [rdx]
00216A07  mulss    xmm0, xmm3
00216A0B  movss    xmm3, dword ptr [rdx + 0x30]
00216A10  addss    xmm1, xmm0
00216A14  movss    dword ptr [rsp + 0x14], xmm1
00216A1A  movaps   xmm1, xmm3
00216A1D  movss    xmm0, dword ptr [rsp + 0x14]
00216A23  mulss    xmm1, xmm12
00216A28  addss    xmm0, xmm1
00216A2C  mulss    xmm2, xmm4
00216A30  movaps   xmm1, xmm3
00216A33  mulss    xmm1, xmm8
00216A38  movss    dword ptr [rsp + 0x14], xmm0
00216A3E  movss    xmm0, dword ptr [rdx]
00216A42  mulss    xmm0, xmm5
00216A46  movss    xmm5, dword ptr [rdx + 0x10]
00216A4B  movaps   xmm3, xmm5
00216A4E  addss    xmm2, xmm0
00216A52  mulss    xmm3, xmm4
00216A56  movss    xmm4, dword ptr [rdx]
00216A5A  movss    xmm0, dword ptr [rsp + 0x14]
00216A60  addss    xmm2, xmm1
00216A64  subss    xmm0, xmm2
00216A68  movaps   xmm2, xmm5
00216A6B  mulss    xmm2, xmm6
00216A6F  movss    dword ptr [rsp + 0x14], xmm0
00216A75  movaps   xmm0, xmm4
00216A78  mulss    xmm0, xmm7
00216A7C  movss    xmm7, dword ptr [rdx + 0x30]
00216A81  movaps   xmm1, xmm7
00216A84  movaps   xmm6, xmm7
00216A87  addss    xmm3, xmm0
00216A8B  mulss    xmm1, xmm11
00216A90  movaps   xmm0, xmm4
00216A93  mulss    xmm0, xmm10
00216A98  movss    xmm10, dword ptr [rdx]
00216A9D  addss    xmm3, xmm1
00216AA1  movaps   xmm1, xmm7
00216AA4  addss    xmm2, xmm0
00216AA8  mulss    xmm1, xmm9
00216AAD  movaps   xmm0, xmm4
00216AB0  mulss    xmm0, xmm13
00216AB5  movaps   xmm13, xmm10
00216AB9  addss    xmm2, xmm1
00216ABD  subss    xmm3, xmm2
00216AC1  movaps   xmm2, xmm5
00216AC4  mulss    xmm2, xmm12
00216AC9  movss    dword ptr [rsp + 0x30], xmm3
00216ACF  movaps   xmm3, xmm5
00216AD2  mulss    xmm3, xmm8
00216AD7  movaps   xmm5, xmm7
00216ADA  movss    xmm8, dword ptr [rdx + 0x20]
00216AE0  movaps   xmm1, xmm8
00216AE4  mulss    xmm1, xmm9
00216AE9  addss    xmm3, xmm0
00216AED  movaps   xmm0, xmm4
00216AF0  movaps   xmm9, xmm8
00216AF4  mulss    xmm0, xmm14
00216AF9  movaps   xmm14, xmm8
00216AFD  addss    xmm3, xmm1
00216B01  mulss    xmm4, xmm15
00216B06  movaps   xmm1, xmm8
00216B0A  addss    xmm2, xmm0
00216B0E  movss    xmm0, dword ptr [rdx + 0x24]
00216B13  mulss    xmm1, xmm11
00216B18  mulss    xmm5, xmm0
00216B1C  addss    xmm2, xmm1
00216B20  mulss    xmm13, xmm0
00216B25  movss    xmm1, dword ptr [rdx + 0x14]
00216B2A  mulss    xmm6, xmm1
00216B2E  subss    xmm3, xmm2
00216B32  mulss    xmm14, xmm1
00216B37  movss    xmm2, dword ptr [rdx + 0x10]
00216B3C  movaps   xmm11, xmm2
00216B40  movaps   xmm12, xmm2
00216B44  movss    xmm2, dword ptr [rdx + 4]
00216B49  movss    dword ptr [rsp + 0x34], xmm3
00216B4F  movaps   xmm3, xmm8
00216B53  movaps   xmm8, xmm10
00216B57  mulss    xmm3, xmm15
00216B5C  movss    xmm10, dword ptr [rdx + 0x10]
00216B62  mulss    xmm8, xmm1
00216B67  movaps   xmm1, xmm6
00216B6A  mulss    xmm1, dword ptr [rdx + 0x2c]
00216B6F  mulss    xmm11, xmm15
00216B74  mulss    xmm12, xmm0
00216B79  mulss    xmm7, xmm2
00216B7D  mulss    xmm9, xmm2
00216B82  mulss    xmm10, xmm2
00216B87  movss    xmm15, dword ptr [rdx + 0x3c]
00216B8D  movss    xmm2, dword ptr [rdx + 0x1c]
00216B92  movaps   xmm0, xmm2
00216B95  mulss    xmm2, xmm5
00216B99  mulss    xmm0, xmm3
00216B9D  addss    xmm1, xmm0
00216BA1  movss    dword ptr [rsp + 0x18], xmm1
00216BA7  movaps   xmm1, xmm12
00216BAB  movss    xmm0, dword ptr [rsp + 0x18]
00216BB1  mulss    xmm1, xmm15
00216BB6  addss    xmm0, xmm1
00216BBA  movaps   xmm1, xmm14
00216BBE  mulss    xmm1, xmm15
00216BC3  movss    dword ptr [rsp + 0x18], xmm0
00216BC9  movaps   xmm0, xmm11
00216BCD  mulss    xmm0, dword ptr [rdx + 0x2c]
00216BD2  addss    xmm2, xmm0
00216BD6  movss    xmm0, dword ptr [rsp + 0x18]
00216BDC  addss    xmm2, xmm1
00216BE0  movaps   xmm1, xmm9
00216BE4  mulss    xmm1, xmm15
00216BE9  subss    xmm0, xmm2
00216BED  movss    xmm2, dword ptr [rdx + 0xc]
00216BF2  mulss    xmm2, xmm5
00216BF6  movss    dword ptr [rsp + 0x18], xmm0
00216BFC  movaps   xmm0, xmm4
00216BFF  mulss    xmm0, dword ptr [rdx + 0x2c]
00216C04  addss    xmm2, xmm0
00216C08  movss    xmm0, dword ptr [rdx + 0xc]
00216C0D  mulss    xmm0, xmm3
00216C11  addss    xmm2, xmm1
00216C15  movaps   xmm1, xmm13
00216C19  mulss    xmm1, xmm15
00216C1E  movss    dword ptr [rsp + 0x20], xmm2
00216C24  movaps   xmm2, xmm7
00216C27  mulss    xmm2, dword ptr [rdx + 0x2c]
00216C2C  addss    xmm2, xmm0
00216C30  movss    xmm0, dword ptr [rsp + 0x20]
00216C36  addss    xmm2, xmm1
00216C3A  movaps   xmm1, xmm7
00216C3D  mulss    xmm1, dword ptr [rdx + 0x1c]
00216C42  subss    xmm0, xmm2
00216C46  movss    xmm2, dword ptr [rdx + 0xc]
00216C4B  movss    dword ptr [rsp + 0x20], xmm0
00216C51  movaps   xmm0, xmm2
00216C54  mulss    xmm0, xmm11
00216C59  mulss    xmm2, xmm6
00216C5D  addss    xmm1, xmm0
00216C61  movss    dword ptr [rsp + 0x1c], xmm1
00216C67  movaps   xmm1, xmm8
00216C6B  movss    xmm0, dword ptr [rsp + 0x1c]
00216C71  mulss    xmm1, xmm15
00216C76  addss    xmm0, xmm1
00216C7A  movaps   xmm1, xmm10
00216C7E  mulss    xmm1, xmm15
00216C83  movss    dword ptr [rsp + 0x1c], xmm0
00216C89  movaps   xmm0, xmm4
00216C8C  mulss    xmm0, dword ptr [rdx + 0x1c]
00216C91  addss    xmm2, xmm0
00216C95  movss    xmm0, dword ptr [rsp + 0x1c]
00216C9B  addss    xmm2, xmm1
00216C9F  movaps   xmm1, xmm10
00216CA3  mulss    xmm1, dword ptr [rdx + 0x2c]
00216CA8  subss    xmm0, xmm2
00216CAC  movss    xmm2, dword ptr [rdx + 0xc]
00216CB1  mulss    xmm2, xmm14
00216CB6  movss    dword ptr [rsp + 0x1c], xmm0
00216CBC  movaps   xmm0, xmm13
00216CC0  mulss    xmm0, dword ptr [rdx + 0x1c]
00216CC5  addss    xmm2, xmm0
00216CC9  movss    xmm0, dword ptr [rdx + 0xc]
00216CCE  mulss    xmm0, xmm12
00216CD3  addss    xmm2, xmm1
00216CD7  movss    dword ptr [rsp + 0x24], xmm2
00216CDD  movaps   xmm2, xmm9
00216CE1  mulss    xmm2, dword ptr [rdx + 0x1c]
00216CE6  movss    xmm1, dword ptr [rsp + 0x24]
00216CEC  addss    xmm2, xmm0
00216CF0  movaps   xmm0, xmm8
00216CF4  mulss    xmm0, dword ptr [rdx + 0x2c]
00216CF9  addss    xmm2, xmm0
00216CFD  movss    xmm15, dword ptr [rdx + 0x38]
00216D03  subss    xmm1, xmm2
00216D07  movaps   xmm2, xmm14
00216D0B  movaps   xmm0, xmm11
00216D0F  mulss    xmm0, dword ptr [rdx + 0x28]
00216D14  mulss    xmm2, xmm15
00216D19  movss    dword ptr [rsp + 0x24], xmm1
00216D1F  addss    xmm2, xmm0
00216D23  movss    xmm0, dword ptr [rdx + 0x18]
00216D28  movaps   xmm1, xmm0
00216D2B  mulss    xmm0, xmm3
00216D2F  mulss    xmm1, xmm5
00216D33  addss    xmm2, xmm1
00216D37  movaps   xmm1, xmm6
00216D3A  mulss    xmm1, dword ptr [rdx + 0x28]
00216D3F  movss    dword ptr [rsp + 0x28], xmm2
00216D45  movaps   xmm2, xmm12
00216D49  mulss    xmm2, xmm15
00216D4E  addss    xmm2, xmm0
00216D52  movss    xmm0, dword ptr [rsp + 0x28]
00216D58  addss    xmm2, xmm1
00216D5C  movaps   xmm1, xmm7
00216D5F  subss    xmm0, xmm2
00216D63  movaps   xmm2, xmm13
00216D67  mulss    xmm2, xmm15
00216D6C  movss    dword ptr [rsp + 0x28], xmm0
00216D72  movss    xmm0, dword ptr [rdx + 8]
00216D77  mulss    xmm0, xmm3
00216D7B  movss    xmm3, dword ptr [rdx + 0x28]
00216D80  mulss    xmm1, xmm3
00216D84  addss    xmm2, xmm0
00216D88  movaps   xmm0, xmm4
00216D8B  mulss    xmm0, xmm3
00216D8F  addss    xmm2, xmm1
00216D93  movss    xmm1, dword ptr [rdx + 8]
00216D98  mulss    xmm1, xmm5
00216D9C  movaps   xmm5, xmm10
00216DA0  mulss    xmm5, xmm15
00216DA5  movss    dword ptr [rsp + 0x2c], xmm2
00216DAB  movaps   xmm2, xmm9
00216DAF  mulss    xmm2, xmm15
00216DB4  mulss    xmm10, xmm3
00216DB9  addss    xmm2, xmm0
00216DBD  movss    xmm0, dword ptr [rsp + 0x2c]
00216DC3  addss    xmm2, xmm1
00216DC7  movaps   xmm1, xmm8
00216DCB  mulss    xmm1, xmm15
00216DD0  mulss    xmm8, xmm3
00216DD5  movss    xmm3, dword ptr [rsp]
00216DDA  subss    xmm0, xmm2
00216DDE  movss    xmm2, dword ptr [rdx + 0x18]
00216DE3  mulss    xmm7, xmm2
00216DE7  mulss    xmm4, xmm2
00216DEB  movss    dword ptr [rsp + 0x2c], xmm0
00216DF1  mulss    xmm13, xmm2
00216DF6  addss    xmm5, xmm4
00216DFA  mulss    xmm9, xmm2
00216DFF  movss    xmm4, dword ptr [rdx + 8]
00216E04  addss    xmm13, xmm10
00216E09  movss    xmm2, dword ptr [rsp + 4]
00216E0F  movaps   xmm0, xmm4
00216E12  mulss    xmm0, xmm6
00216E16  movaps   xmm6, xmm4
00216E19  mulss    xmm6, xmm12
00216E1E  addss    xmm5, xmm0
00216E22  movaps   xmm0, xmm4
00216E25  mulss    xmm0, xmm11
00216E2A  addss    xmm6, xmm8
00216E2F  mulss    xmm4, xmm14
00216E34  addss    xmm1, xmm0
00216E38  movss    xmm0, dword ptr [rdx]
00216E3C  mulss    xmm0, xmm2
00216E40  addss    xmm6, xmm9
00216E45  addss    xmm13, xmm4
00216E4A  addss    xmm1, xmm7
00216E4E  movss    xmm7, dword ptr [rdx + 0x10]
00216E53  mulss    xmm7, xmm3
00216E57  subss    xmm6, xmm13
00216E5C  subss    xmm5, xmm1
00216E60  addss    xmm7, xmm0
00216E64  movss    dword ptr [rsp + 0x38], xmm5
00216E6A  movss    xmm0, dword ptr [rdx + 0x20]
00216E6F  xorps    xmm1, xmm1
00216E72  movss    xmm4, dword ptr [rsp + 8]
00216E78  movss    xmm5, dword ptr [rsp + 0xc]
00216E7E  mulss    xmm0, xmm4
00216E82  addss    xmm7, xmm0
00216E86  movss    xmm0, dword ptr [rdx + 0x30]
00216E8B  mulss    xmm0, xmm5
00216E8F  addss    xmm7, xmm0
00216E93  ucomiss  xmm7, xmm1
00216E96  jp       0x216e9a  ; -> 00216E9A
00216E98  je       0x216ea6  ; -> 00216EA6
00216E9A  movss    xmm1, dword ptr [rip + 0x1ad4d06]  ; -> 01CEBBA8 [f32 1]
00216EA2  divss    xmm1, xmm7
00216EA6  movss    xmm0, dword ptr [rsp + 0x10]
00216EAC  lea      r11, [rsp + 0xe8]
00216EB4  movaps   xmm7, xmmword ptr [r11 - 0x28]
00216EB9  movaps   xmm8, xmmword ptr [r11 - 0x38]
00216EBE  movaps   xmm9, xmmword ptr [r11 - 0x48]
00216EC3  movaps   xmm10, xmmword ptr [r11 - 0x58]
00216EC8  movaps   xmm11, xmmword ptr [r11 - 0x68]
00216ECD  movaps   xmm12, xmmword ptr [r11 - 0x78]
00216ED2  movaps   xmm13, xmmword ptr [rsp + 0x60]
00216ED8  movaps   xmm14, xmmword ptr [rsp + 0x50]
00216EDE  movaps   xmm15, xmmword ptr [rsp + 0x40]
00216EE4  mulss    xmm0, xmm1
00216EE8  mulss    xmm2, xmm1
00216EEC  mulss    xmm3, xmm1
00216EF0  movss    dword ptr [rcx], xmm2
00216EF4  movss    xmm2, dword ptr [rsp + 0x30]
00216EFA  movss    dword ptr [rcx + 4], xmm3
00216EFF  mulss    xmm2, xmm1
00216F03  mulss    xmm4, xmm1
00216F07  mulss    xmm5, xmm1
00216F0B  movss    dword ptr [rcx + 8], xmm4
00216F10  mulss    xmm6, xmm1
00216F14  movss    dword ptr [rcx + 0xc], xmm5
00216F19  movss    dword ptr [rcx + 0x10], xmm0
00216F1E  movss    xmm0, dword ptr [rsp + 0x14]
00216F24  mulss    xmm0, xmm1
00216F28  movss    dword ptr [rcx + 0x14], xmm0
00216F2D  movss    xmm0, dword ptr [rsp + 0x34]
00216F33  mulss    xmm0, xmm1
00216F37  movss    dword ptr [rcx + 0x18], xmm2
00216F3C  movss    xmm2, dword ptr [rsp + 0x38]
00216F42  movss    dword ptr [rcx + 0x1c], xmm0
00216F47  movss    xmm0, dword ptr [rsp + 0x18]
00216F4D  mulss    xmm0, xmm1
00216F51  mulss    xmm2, xmm1
00216F55  movss    dword ptr [rcx + 0x20], xmm0
00216F5A  movss    xmm0, dword ptr [rsp + 0x20]
00216F60  mulss    xmm0, xmm1
00216F64  movss    dword ptr [rcx + 0x24], xmm0
00216F69  movss    xmm0, dword ptr [rsp + 0x1c]
00216F6F  mulss    xmm0, xmm1
00216F73  movss    dword ptr [rcx + 0x28], xmm0
00216F78  movss    xmm0, dword ptr [rsp + 0x24]
00216F7E  mulss    xmm0, xmm1
00216F82  movss    dword ptr [rcx + 0x2c], xmm0
00216F87  movss    xmm0, dword ptr [rsp + 0x28]
00216F8D  mulss    xmm0, xmm1
00216F91  movss    dword ptr [rcx + 0x30], xmm0
00216F96  movss    xmm0, dword ptr [rsp + 0x2c]
00216F9C  mulss    xmm0, xmm1
00216FA0  movss    dword ptr [rcx + 0x34], xmm0
00216FA5  movss    dword ptr [rcx + 0x38], xmm2
00216FAA  movss    dword ptr [rcx + 0x3c], xmm6
00216FAF  movaps   xmm6, xmmword ptr [r11 - 0x18]
00216FB4  mov      rsp, r11
00216FB7  ret      
```
