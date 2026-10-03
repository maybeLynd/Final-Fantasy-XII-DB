# Homing pack: `00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md`

Generated 2026-10-03 08:08 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-battle-runtime-mode-ladder.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00422E40 (11 B, extent 00422E40-00422E4B)

Entered from (direct sites whose caller this page cites): `0042DF10` + 0x92 (jmp; `0042DF10` is cited on this page)
Other direct sites: none

Host context: "nterior anchor '002970DF' (function '002970C0').  '00429F70' (223 B) is the recursive record walk '00427DE0' runs over the '022C6F28' '0x740'-stride table: from 'rcx''s u16 head index ('-1' ends) it '0042DF10'-visits each record into a stack out-pair, then recurses through '0042EF90' on the '+8' and '+0xA' u16 links - a depth-first sweep of the chain with the caller's '+0x308' float carried in the out record  Interior anchor '00429FD0' "

```
00422E40  mov      r8d, 1
00422E46  jmp      0x424870  ; -> 00424870 fn
```
