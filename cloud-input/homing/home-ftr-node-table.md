# Homing pack: `17-Presentation-Rendering/Model-And-Motion-Formats/ftr-node-table.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-ftr-node-table.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 004775E0 (39 B, extent 004775E0-00477607)

Entered from (direct sites whose caller this page cites): `004213E0` + 0xF1 (call; `004213E0` is cited on this page)
Other direct sites: none

Host context: "(../Character-Render-Records/the-rig-of-seventeen-controllers.md): '003703A0', '00370E20', '00372710', '003B8260', '003E6DF0', '003E6F90', '003E7040', '00417F40', '0041D220', '0041D560', '0041DD40', '004213E0', '004215A0', '00421B00', '00422940', '00427320', '0042BDE0', '0042BED0', '0042C410', '0042C8F0', '0042D8B0', '0042DCD0', '0042DD90', '0042E690', '005201B0', '00520320' and '00520E90'.  **Which bones carry attachments (B1–B2).** No"

```
004775E0  lea      rax, [rip + 0x282f6b9]  ; -> 02CA6CA0
004775E7  movzx    r8d, cl
004775EB  shl      r8, 6
004775EF  add      r8, rax
004775F2  xor      eax, eax
004775F4  cmp      dword ptr [r8 + 4], ecx
004775F8  cmovne   r8, rax
004775FC  test     r8, r8
004775FF  je       0x477606  ; -> 00477606
00477601  mov      word ptr [r8 + 2], dx
00477606  ret      
```
