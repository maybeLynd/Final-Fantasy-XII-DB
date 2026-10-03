# Homing pack: `06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-movement-body-pool-and-the-separation-pass.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00263910 (40 B, extent 00263910-00263938)

Entered from (direct sites whose caller this page cites): `002E6000` + 0x4B (call; `002E6000` is cited on this page)
Other direct sites: none

Host context: "lator reset '003DA9F0' ('003DA9F2').         A scan of every write at displacements '+0xF5'–'+0x104' in the body module ('003D9000'–'003DC000'), the pair resolver and the movement update ('002E3000'–'002E6000') finds these three, the resolver's two 4-byte float stores at '+0x100', and three 4-byte stores to '+0xF8' of the movement context (a different structure).       - **The whole image has no other candidate.** There are 115 function"

```
00263910  mov      rax, qword ptr [rcx + 0xc0]
00263917  xorps    xmm1, xmm1
0026391A  test     rax, rax
0026391D  je       0x263934  ; -> 00263934
0026391F  movss    xmm0, dword ptr [rax + 0x140]
00263927  addss    xmm0, xmm1
0026392B  addss    xmm0, dword ptr [rax + 0x144]
00263933  ret      
00263934  movaps   xmm0, xmm1
00263937  ret      
```
