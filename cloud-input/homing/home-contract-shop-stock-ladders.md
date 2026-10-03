# Homing pack: `12-Items-Equipment-Shops-License/CONTRACT-shop-stock-ladders.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-shop-stock-ladders.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003931E0 (62 B, extent 003931E0-0039321E)

Entered from (direct sites whose caller this page cites): `00578450` + 0x2FF (call; `00578450` is cited on this page)
Other direct sites: `0056FEF0` + 0x9A (call); `0056FEF0` + 0xBD (call)

Host context: ", plus '00316480''s calls into '0046B180'/'0046B1A0' — touches that layer's bodies; the ladder itself stays shop-owned.  **Presentation — MECHANICAL (SWE2-EC7-169, 1 edge).** '0046B1A0' is called by '00578450' of that layer — one fan-in edge.  **Save_Load_Settings — MECHANICAL (SWE2-EC7-169, 4 edges).** '0046B180'/'0046B1A0'/ '0046B240' call '002EF2B0' of that layer, and '00315390' is called by '00583D60' — shared-helper fan-in both way"

```
003931E0  xor      r9d, r9d
003931E3  mov      rax, rcx
003931E6  test     rcx, rcx
003931E9  jne      0x3931f0  ; -> 003931F0
003931EB  mov      eax, r9d
003931EE  jmp      0x3931fb  ; -> 003931FB
003931F0  mov      rax, qword ptr [rax + 0x60]
003931F4  movsxd   rcx, edx
003931F7  mov      rax, qword ptr [rax + rcx*8]
003931FB  mov      ecx, dword ptr [rax + 8]
003931FE  and      cl, 0x3c
00393201  cmp      cl, 4
00393204  jne      0x39321d  ; -> 0039321D
00393206  mov      rax, qword ptr [rax + 0x18]
0039320A  test     rax, rax
0039320D  je       0x39321a  ; -> 0039321A
0039320F  mov      rax, qword ptr [rax + 0x60]
00393213  movsxd   rcx, r8d
00393216  mov      r9, qword ptr [rax + rcx*8]
0039321A  mov      rax, r9
0039321D  ret      
```
