# Homing pack: `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`

Generated 2026-10-03 12:43 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h12-ui-layout-parameters-and-editor-schema.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003689E0 (97 B, extent 003689E0-00368A41)

Entered from (direct sites whose caller this page cites): `002D45C0` + 0x76 (call; `002D45C0` is cited on this page)
Other direct sites: none

Host context: "02A3960' ('P', MessageWin, 1,159 B — '005C5230' first at '002A399B', '002DD7E0'/'002DC290'/'002D8BB0' ×2); '002C59D0' (1,187 B — '002432B0' first call at ['002C5A23'](../../_index/ADDRESS-INDEX.md), '002D45C0'/'002C5EC0' ×4 + '002D02A0' ×3 + '002D47C0' ×2); '00558FB0' ('P', BlackBand, 1,332 B — '01F44830' at ['00558FBB'](../../_index/ADDRESS-INDEX.md), '0024A5A0' ×14 + '002493D0' ×4 dense reader); '005565E0' ('P', LicenseBoard, 1,031 B "

```
003689E0  cmp      word ptr [rip + 0x1f63448], 0  ; -> 022CBE30
003689E8  je       0x368a40  ; -> 00368A40
003689EA  test     ecx, ecx
003689EC  je       0x3689f8  ; -> 003689F8
003689EE  mov      ecx, 8
003689F3  jmp      0x3688e0  ; -> 003688E0 fn
003689F8  movzx    eax, byte ptr [rip + 0x1f63488]  ; -> 022CBE87
003689FF  test     al, al
00368A01  je       0x368a24  ; -> 00368A24
00368A03  cmp      al, 1
00368A05  je       0x368a0e  ; -> 00368A0E
00368A07  sub      al, 2
00368A09  cmp      al, 1
00368A0B  ja       0x368a2d  ; -> 00368A2D
00368A0D  ret      
00368A0E  movsx    eax, word ptr [rip + 0x1f63475]  ; -> 022CBE8A
00368A15  movsx    ecx, word ptr [rip + 0x1f6346c]  ; -> 022CBE88
00368A1C  shl      eax, 3
00368A1F  cdq      
00368A20  idiv     ecx
00368A22  jmp      0x368a26  ; -> 00368A26
00368A24  xor      eax, eax
00368A26  mov      word ptr [rip + 0x1f6345d], ax  ; -> 022CBE8A
00368A2D  mov      eax, 8
00368A32  mov      byte ptr [rip + 0x1f6344e], 2  ; -> 022CBE87
00368A39  mov      word ptr [rip + 0x1f63448], ax  ; -> 022CBE88
00368A40  ret      
```
