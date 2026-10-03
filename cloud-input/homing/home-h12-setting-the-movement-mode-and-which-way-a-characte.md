# Homing pack: `06-Movement-And-Navigation/Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md`

Generated 2026-10-03 12:43 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h12-setting-the-movement-mode-and-which-way-a-characte.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002E5B90 (35 B, extent 002E5B90-002E5BB3)

Entered from (direct sites whose caller this page cites): `0026AC70` + 0x5C (jmp; `0026AC70` is cited on this page)
Other direct sites: none

Host context: "re the switch it reads 'turn_step' ('00264750' → '002E4BC0' → '+0x58') and, **when any mode is active, floors it at '0x3C0EFA35' = π/360 = 0.5° per frame** ('002E5806'–'002E5821', through the setter '0026AC70').  | mode | what the integrator does each frame | set by | |---:|---|---| | 0 | nothing | the teardown callers (§7) | | 1 | 'heading += +0x3C', wrapped, through 'Actor_SetFacingHeading_Variant0' ('002E5A9E'–'002E5AED') — **a const"

```
002E5B90  test     rcx, rcx
002E5B93  je       0x2e5bb2  ; -> 002E5BB2
002E5B95  cmp      qword ptr [rcx + 0xc0], 0
002E5B9D  je       0x2e5bb2  ; -> 002E5BB2
002E5B9F  mov      rax, qword ptr [rcx + 0xb8]
002E5BA6  mov      rcx, qword ptr [rax + 0xf0]
002E5BAD  movss    dword ptr [rcx + 0x58], xmm1
002E5BB2  ret      
```
