# Homing pack: `06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-contract-heading-speed-to-position-delta.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002E9BE0 (26 B, extent 002E9BE0-002E9BFA)

Entered from (direct sites whose caller this page cites): `003B73B0` + 0x49 (call; `003B73B0` is cited on this page)
Other direct sites: `003B7440` + 0x78 (call); `003B7510` + 0x72 (call)

Host context: "S-18's first  ## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)  - **ActorEntity - CLIENT (8 edges).** '00265020' is also called by bodies filed to ActorEntity: '00236300', '0037B4D0', '003B73B0' - shared machinery across the layer boundary, no shared ownership. - **Audio - CLIENT (1 edge).** '00265020' is also called by bodies filed to audio: '00362850' - shared machinery across the layer boundary, no shared ownership. - "

```
002E9BE0  test     rcx, rcx
002E9BE3  je       0x2e9bf6  ; -> 002E9BF6
002E9BE5  mov      rax, qword ptr [rcx + 0xc0]
002E9BEC  test     rax, rax
002E9BEF  je       0x2e9bf6  ; -> 002E9BF6
002E9BF1  movsx    eax, byte ptr [rax + 0x13]
002E9BF5  ret      
002E9BF6  or       eax, 0xffffffff
002E9BF9  ret      
```
