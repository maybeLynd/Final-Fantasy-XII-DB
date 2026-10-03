# Homing pack: `05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-when-a-group-is-wiped-and-when-it-comes-back.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003DCB90 (43 B, extent 003DCB90-003DCBBB)

Entered from (direct sites whose caller this page cites): `00427320` + 0x32F (call; `00427320` is cited on this page)
Other direct sites: `00325B30` + 0x0 (jmp); `0050CEF0` + 0x13 (call)

Host context: " presentation dispatch actually does is different from what a "handler" name suggests: > '003299B0' writes the event to actor-work '+0xF0' ('002EB04D', via '002EB030'), and '002EB0D0' > passes it to '00427320' on the '0x740'-stride animation object at '*(022C6F28)' — **the animation > layer consumes the event; no native handler is called with it.** If the animation layer ever > calls back into '003250F0', it does so through a pointer th"

```
003DCB90  test     ecx, ecx
003DCB92  jns      0x3dcb9a  ; -> 003DCB9A
003DCB94  mov      eax, 3
003DCB99  ret      
003DCB9A  je       0x3dcbb8  ; -> 003DCBB8
003DCB9C  mov      eax, ecx
003DCB9E  lea      rdx, [rip + 0x277b3cb]  ; -> 02B57F70
003DCBA5  and      eax, 0xf
003DCBA8  lea      rax, [rax + rax*4]
003DCBAC  cmp      dword ptr [rdx + rax*4 + 8], ecx
003DCBB0  jne      0x3dcbb8  ; -> 003DCBB8
003DCBB2  movzx    eax, byte ptr [rdx + rax*4 + 6]
003DCBB7  ret      
003DCBB8  xor      eax, eax
003DCBBA  ret      
```
