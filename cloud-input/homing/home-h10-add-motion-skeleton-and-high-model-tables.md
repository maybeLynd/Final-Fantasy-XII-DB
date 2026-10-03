# Homing pack: `17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-add-motion-skeleton-and-high-model-tables.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002EB810 (92 B, extent 002EB810-002EB86C)

Entered from (direct sites whose caller this page cites): `002E3A60` + 0x45 (call; `002E3A60` is cited on this page)
Other direct sites: `002E3110` + 0x1F9 (call)

Host context: "(216 B) is a motion-table body - '003AB7F0'/'0051F6B0'. Interior anchor '0051F7C1' (a '003AB7F0' call).   ## SWE2-EC7-56 update (2026-09-19) - '002E3C20'  '002E3C20' (212 B) is a motion-table body - '002E3A60'/'002E42D0'. Interior anchor '002E3C8F' (a '002E3A60' call).  ## SWE2-EC7-62 update (2026-09-19) - '003721E0'  '003721E0' (150 B) is an add-motion body - '0020E620' single call. Interior anchor '00372201' (a '0020E620' call).   ## "

```
002EB810  mov      rax, qword ptr [rip + 0x1e74541]  ; -> 0215FD58
002EB817  test     rax, rax
002EB81A  je       0x2eb82e  ; -> 002EB82E
002EB81C  nop      dword ptr [rax]
002EB820  cmp      dword ptr [rax + 0x14], ecx
002EB823  je       0x2eb84f  ; -> 002EB84F
002EB825  mov      rax, qword ptr [rax + 8]
002EB829  test     rax, rax
002EB82C  jne      0x2eb820  ; -> 002EB820
002EB82E  mov      rax, qword ptr [rip + 0x1e74543]  ; -> 0215FD78
002EB835  test     rax, rax
002EB838  je       0x2eb86b  ; -> 002EB86B
002EB83A  nop      word ptr [rax + rax]
002EB840  cmp      dword ptr [rax + 0x14], ecx
002EB843  je       0x2eb84f  ; -> 002EB84F
002EB845  mov      rax, qword ptr [rax + 8]
002EB849  test     rax, rax
002EB84C  jne      0x2eb840  ; -> 002EB840
002EB84E  ret      
002EB84F  test     rax, rax
002EB852  je       0x2eb86b  ; -> 002EB86B
002EB854  dec      word ptr [rax + 0x1c]
002EB858  cmp      word ptr [rax + 0x1c], 0
002EB85D  jg       0x2eb86b  ; -> 002EB86B
002EB85F  test     byte ptr [rax + 0x19], 3
002EB863  je       0x2eb86b  ; -> 002EB86B
002EB865  xor      ecx, ecx
002EB867  mov      word ptr [rax + 0x1c], cx
002EB86B  ret      
```
