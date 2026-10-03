# Homing pack: `16-UI/License-Board-View/the-license-board-grid-build-and-its-change-sweep.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-license-board-grid-build-and-its-change-sweep.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002286B0 (64 B, extent 002286B0-002286F0)

Entered from (direct sites whose caller this page cites): `002470D0` + 0x2F (jmp; `002470D0` is cited on this page)
Other direct sites: none

Host context: "rd create '00561390' runs: a null '[+0xC8]' is '00244F50(0x580, 0055CD40, &ctx{this})'-created, stored into '[0209AC30]+0x320' as well as '[+0xC8]', registered through '00246AD0(0208EA28, obj)', and '002470D0''d — the '0x580'-byte '0055CD40' view record is the board object the whole '0055xxxx' cluster serves.  Interior anchor '0055C6EA' (function '0055C690').  '0055A810' (140 B) is the per-slot child ensure-create '00561390' runs: 'this"

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
