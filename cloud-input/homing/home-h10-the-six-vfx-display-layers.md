# Homing pack: `17-Presentation-Rendering/Effect-File-Formats/the-six-vfx-display-layers.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-the-six-vfx-display-layers.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001823E0 (38 B, extent 001823E0-00182406)

Entered from (direct sites whose caller this page cites): `001B2530` + 0x3A (call; `001B2530` is cited on this page); `001B2600` + 0x21 (jmp; `001B2600` is cited on this page)
Other direct sites: none

Host context: "258FE3', '00258FF1', '00258FFF' |  ## Cross-subsystem neighbours  None named: every routine this body calls is described by role, and none is cited by address.  **Core runtime scheduling - CLIENT.** '001B2530', the tail target of the forwarder '00862C10' now named on this page, calls '0017D980' in that layer's census. The VFX-layer bodies consult the scheduler through that forwarder; they do not own it. MECHANICAL accounting (SWE2-EC7, " / "oes not depend on that caller.  ## SWE2-EC7-71 update (2026-09-19) - '00862C30' + '00862C10' singleton forwarders measured  '00862C30' (12 B) loads the '01F7F4D8' singleton into 'rcx' and tail-jumps '001B2600' - the no-arg forwarder.  '00862C10' (17 B) is the arg-swapping sibling: '001B2530(global, edx, ecx)' - the singleton prepended, the two caller args reversed. Interior anchors '00862C37' (the 'jmp 001B2600' tail) and '00862C1C' (th"

```
001823E0  push     rbx
001823E2  sub      rsp, 0x20
001823E6  mov      ebx, ecx
001823E8  mov      dword ptr [rip + 0x1dfd146], 0  ; -> 01F7F538
001823F2  call     0x18ca40  ; -> 0018CA40 fn
001823F7  mov      rcx, rax
001823FA  mov      edx, ebx
001823FC  add      rsp, 0x20
00182400  pop      rbx
00182401  jmp      0x18bdd0  ; -> 0018BDD0 fn
```
