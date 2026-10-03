# Homing pack: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-five-small-bin-tables.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0029D4D0 (114 B, extent 0029D4D0-0029D542)

Entered from (direct sites whose caller this page cites): `0029E110` + 0x203 (call; `0029E110` is cited on this page)
Other direct sites: none

Host context: "' and the signal index. '0029E330(sceneId)' builds that legend and '0029DDF0' copies it into the HUD object '[0209C498]+0x158' at '+0xD0' only when it differs; its callers are the menus ('00295D20', '0029E110', '002B7B80', '002BAF80', '002D5EB0', '005789D0'). **The mask encoding is the engine's own input-snapshot button word**: '0029DBE0(key)' returns section 0's mask for a key below '0x100', or for '0x100 + n' the mask of signal n's bu"

```
0029D4D0  sub      rsp, 0x28
0029D4D4  mov      rcx, qword ptr [rip + 0x1dfefbd]  ; -> 0209C498
0029D4DB  lea      r8, [rip + 0x6e]  ; -> 0029D550
0029D4E2  add      rcx, 0x160
0029D4E9  xor      r9d, r9d
0029D4EC  mov      edx, 0x148
0029D4F1  call     0x245000  ; -> 00245000 fn
0029D4F6  mov      rcx, qword ptr [rip + 0x1dfef9b]  ; -> 0209C498
0029D4FD  lea      r8, [rip + 0x4c]  ; -> 0029D550
0029D504  add      rcx, 0x2a8
0029D50B  xor      r9d, r9d
0029D50E  mov      edx, 0x148
0029D513  call     0x245000  ; -> 00245000 fn
0029D518  mov      rcx, qword ptr [rip + 0x1dfef79]  ; -> 0209C498
0029D51F  lea      rdx, [rcx + 0x160]
0029D526  call     0x244960  ; -> 00244960 fn
0029D52B  mov      rcx, qword ptr [rip + 0x1dfef66]  ; -> 0209C498
0029D532  lea      rdx, [rcx + 0x2a8]
0029D539  add      rsp, 0x28
0029D53D  jmp      0x244960  ; -> 00244960 fn
```
