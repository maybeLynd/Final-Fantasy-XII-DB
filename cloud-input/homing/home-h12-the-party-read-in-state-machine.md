# Homing pack: `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md`

Generated 2026-10-03 12:43 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h12-the-party-read-in-state-machine.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003B5470 (78 B, extent 003B5470-003B54BE)

Entered from (direct sites whose caller this page cites): `00359B10` + 0x5F (jmp; `00359B10` is cited on this page)
Other direct sites: none

Host context: "riant1', 'Actor_SetDesiredMovementHeading', '002E4A40', '002E8060', '002EB030', **'Actor_SetPresentationVisibilityEnabled'** (shown again), 'BattleUnit_ActivateAppliedDefinitionRuntime', '00263560', '00359B10', '002DEB90' | 23 ('0037C0EB') | | 23 | done: returns 1 ('0037C0EE') | — |  **The entries it loads live in the 128 × 64-byte table at '0215FDA0'** ([how a script names a thing in the world](../how-a-script-names-a-thing-in-the-worl"

```
003B5470  mov      qword ptr [rsp + 8], rbx
003B5475  push     rdi
003B5476  sub      rsp, 0x20
003B547A  cmp      byte ptr [rip + 0x278b091], 0  ; -> 02B40512
003B5481  mov      edi, edx
003B5483  mov      ebx, ecx
003B5485  je       0x3b549a  ; -> 003B549A
003B5487  mov      ecx, 1
003B548C  call     0x2ea030  ; -> 002EA030 fn
003B5491  mov      edx, eax
003B5493  mov      ecx, edi
003B5495  call     0x3b4b60  ; -> 003B4B60 fn
003B549A  cmp      byte ptr [rip + 0x278b069], 0  ; -> 02B4050A
003B54A1  je       0x3b54b3  ; -> 003B54B3
003B54A3  xor      ecx, ecx
003B54A5  call     0x2ea030  ; -> 002EA030 fn
003B54AA  mov      edx, eax
003B54AC  mov      ecx, ebx
003B54AE  call     0x3b4b60  ; -> 003B4B60 fn
003B54B3  mov      rbx, qword ptr [rsp + 0x30]
003B54B8  add      rsp, 0x20
003B54BC  pop      rdi
003B54BD  ret      
```
