# Homing pack: `08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md`

Generated 2026-10-03 12:43 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h12-the-count-clock-and-bank-recipes.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002286B0 (64 B, extent 002286B0-002286F0)

Entered from (direct sites whose caller this page cites): `002470D0` + 0x2F (jmp; `002470D0` is cited on this page)
Other direct sites: none

Host context: " − threshold[0] ≥ threshold[1]') and the UI ('00281AE0',   '0057B890' — interior read 2026-09-17, SWE2-FRONTIER: 1,107 B — '002497E0' first at ['0057B906'](../../_index/ADDRESS-INDEX.md), '00291D80'/'002470D0' ×3 + '002CA110'/'00285F20' ×2, '002CF940').  ### 2.6 Recipe 61 — the gil throw (action '0xB5')  The only recipe whose cost is computed at **preview** and charged at **consume**. Its preview list is slot 18 ('00388D50') and its com"

```
002286B0  push     rbx
002286B2  sub      rsp, 0x20
002286B6  mov      rax, qword ptr [rip + 0x1dac28b]  ; -> 01FD4948
002286BD  mov      rbx, rcx
002286C0  test     rax, rax
002286C3  je       0x2286ea  ; -> 002286EA
002286C5  test     rcx, rcx
002286C8  je       0x2286e3  ; -> 002286E3
002286CA  mov      r8, qword ptr [rcx]
002286CD  test     r8, r8
002286D0  je       0x2286e3  ; -> 002286E3
002286D2  lea      rdx, [rip + 0x6e0487]  ; -> 00908B60
002286D9  call     r8
002286DC  mov      rax, qword ptr [rip + 0x1dac265]  ; -> 01FD4948
002286E3  mov      qword ptr [rax + 0xc8], rbx
002286EA  add      rsp, 0x20
002286EE  pop      rbx
002286EF  ret      
```
