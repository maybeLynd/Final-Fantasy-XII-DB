# F-interior pack: `16-UI/the-selection-the-menu-publishes.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-selection-the-menu-publishes.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 66f4ecd88	FABLE: SD-125 answered - +0x2FF0 bit 0x4000 means the battle command dispatcher's open window is the; f3e4846dc	FABLE for SWE2-DATA: SD-124 answered - the command menu's handle names a class-2 (battle-menu map) p). OPUS read these before packing.

## 00203030 (77 B, extent 00203030-0020307D)

Page context: "d, rcx + 0x10)' and '002EA0E0(found, rcx)'; combines the vectors at '+0' and '+0x10' with '00203080' and, when '002703F0' of the result is at least 1.0 ('01CEBBA8'), passes it through '00202DE0' and '00203030', otherwise copies it to '022D9240' and '022D9260', 1.0 to '022D925C' and three stack floats to '022D9250'-'022D9258'; after '00202B10' adds (2.0 minus floats '+0x820' and '+0x824') times 0.75 plus 1.5 to its y ('01CEBC08', '00901B"

```
00203030  sub      rsp, 0x18
00203034  movaps   xmm0, xmm2
00203037  movaps   xmm1, xmm2
0020303A  mulss    xmm0, dword ptr [rdx]
0020303E  mulss    xmm1, dword ptr [rdx + 4]
00203043  movss    dword ptr [rsp], xmm0
00203048  movaps   xmm0, xmm2
0020304B  mulss    xmm0, dword ptr [rdx + 8]
00203050  mulss    xmm2, dword ptr [rdx + 0xc]
00203055  movss    dword ptr [rsp + 4], xmm1
0020305B  movss    dword ptr [rsp + 8], xmm0
00203061  movss    dword ptr [rsp + 0xc], xmm2
00203067  movups   xmm0, xmmword ptr [rsp]
0020306B  movups   xmmword ptr [rcx], xmm0
0020306E  movss    xmm1, dword ptr [rdx + 0xc]
00203073  movss    dword ptr [rcx + 0xc], xmm1
00203078  add      rsp, 0x18
0020307C  ret      
```
