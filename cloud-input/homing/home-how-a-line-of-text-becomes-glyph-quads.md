# Homing pack: `99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-how-a-line-of-text-becomes-glyph-quads.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00408AD0 (33 B, extent 00408AD0-00408AF1)

Entered from (direct sites whose caller this page cites): `003EC850` + 0x0 (jmp; `003EC850` is cited on this page)
Other direct sites: none

Host context: "all subsystem reset ('002EF350', '0032F240', two '00369760'/         '0036D160'/'003697F0' triples, '00377440'/'00377480'-gated '0025A990'/         '0025AA30', '003ACA90(8)', '00360110', '002E24B0', '003EC850', '0036E3B0',         '0026FFA0'/'002700C0'/'002EC590'/'002EC5A0' each '(1)'). Its only caller         is '0032F966' inside a three-way kind dispatch — selector '5', '13', '14'         each pass a different **resolver-thunk functio"

```
00408AD0  mov      rax, qword ptr [rip + 0x275a2a9]  ; -> 02B62D80
00408AD7  test     rax, rax
00408ADA  je       0x408af0  ; -> 00408AF0
00408ADC  mov      ecx, dword ptr [rax + 0xc8]
00408AE2  test     cl, 2
00408AE5  jne      0x408af0  ; -> 00408AF0
00408AE7  and      ecx, 0xfffffffb
00408AEA  mov      dword ptr [rax + 0xc8], ecx
00408AF0  ret      
```
