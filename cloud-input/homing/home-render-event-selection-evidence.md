# Homing pack: `17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-render-event-selection-evidence.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002E9860 (40 B, extent 002E9860-002E9888)

Entered from (direct sites whose caller this page cites): `003B0C50` + 0xD8 (call; `003B0C50` is cited on this page)
Other direct sites: none

Host context: " | '00520E70' | | 0x15 | '00520740' | 58 B — touches '+0x3D1' | '00520740' | | 0x16 | '00520BD0' | '0042B550'; flag pair '+0x3D2'/'+0x3D3', '+0x3F8' | '00520BF8' | | 0x18 | '00520C80' | '00421E20' + '003B0C50'; '+0x60'/'+0x90' fields | '00520C8A' | | 0x19 | '00520CE0' | 32 B — calls '0046CC70' | '00520CF4' | | 0x1A | '00520C10' | '00422D50' + '003E6340'; '+0x30'/'+0x370' | '00520C20' | | 0x1D | '00520D30' | '003E55B0','00477610','00428B"

```
002E9860  mov      rax, qword ptr [rcx + 0xc0]
002E9867  test     rax, rax
002E986A  je       0x2e9885  ; -> 002E9885
002E986C  mov      rax, qword ptr [rax + 0x138]
002E9873  test     rax, rax
002E9876  je       0x2e9885  ; -> 002E9885
002E9878  mov      eax, dword ptr [rax + 0x90]
002E987E  shr      eax, 3
002E9881  and      eax, 1
002E9884  ret      
002E9885  xor      eax, eax
002E9887  ret      
```

## 002E98C0 (37 B, extent 002E98C0-002E98E5)

Entered from (direct sites whose caller this page cites): `003B0C50` + 0xE4 (call; `003B0C50` is cited on this page)
Other direct sites: none

Host context: " | '00520E70' | | 0x15 | '00520740' | 58 B — touches '+0x3D1' | '00520740' | | 0x16 | '00520BD0' | '0042B550'; flag pair '+0x3D2'/'+0x3D3', '+0x3F8' | '00520BF8' | | 0x18 | '00520C80' | '00421E20' + '003B0C50'; '+0x60'/'+0x90' fields | '00520C8A' | | 0x19 | '00520CE0' | 32 B — calls '0046CC70' | '00520CF4' | | 0x1A | '00520C10' | '00422D50' + '003E6340'; '+0x30'/'+0x370' | '00520C20' | | 0x1D | '00520D30' | '003E55B0','00477610','00428B"

```
002E98C0  mov      rax, qword ptr [rcx + 0xc0]
002E98C7  test     rax, rax
002E98CA  je       0x2e98e1  ; -> 002E98E1
002E98CC  mov      rax, qword ptr [rax + 0x138]
002E98D3  test     rax, rax
002E98D6  je       0x2e98e1  ; -> 002E98E1
002E98D8  movss    xmm0, dword ptr [rax + 0xc0]
002E98E0  ret      
002E98E1  xorps    xmm0, xmm0
002E98E4  ret      
```
