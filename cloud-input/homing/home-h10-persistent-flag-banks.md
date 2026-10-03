# Homing pack: `14-Story-Event-Quest-Hunt/persistent-flag-banks.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-persistent-flag-banks.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003EB700 (23 B, extent 003EB700-003EB717)

Entered from (direct sites whose caller this page cites): `003EC720` + 0x1E (call; `003EC720` is cited on this page); `003EC770` + 0x1E (call; `003EC770` is cited on this page)
Other direct sites: `00340890` + 0x2A (call); `00340D00` + 0x4E (call); `003412B0` + 0x63 (call); `00346B80` + 0x4E (call); `003471B0` + 0x4E (call); `00351250` + 0x2C (call); `003518C0` + 0x4E (call)

Host context: " anchor '003EC5D4'; Interior anchor '003EC5DD' | [world-loot-pickups-the-ten-slot-pool-and-the-despawn](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) | | '003EC720' | 73 B | '002FB560' + 0x79 | keeps the incoming floats 'xmm1', 'xmm2' and 'xmm3' across a call to '003EC720' + 0x1E made with the incoming arguments, then tail-jumps (+ 0x44) with 'rcx' = the sign-extended dword that call returned" / " anchor '003EC74C'; Interior anchor '003EC764' | [world-loot-pickups-the-ten-slot-pool-and-the-despawn](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) | | '003EC770' | 73 B | '002FB560' + 0x12A | keeps the incoming floats 'xmm1', 'xmm2' and 'xmm3' across a call to '003EC770' + 0x1E made with the incoming arguments, then tail-jumps (+ 0x44) with 'rcx' = the sign-extended dword that call returne"

```
003EB700  cmp      ecx, 0x1f
003EB703  ja       0x3eb714  ; -> 003EB714
003EB705  movsxd   rax, ecx
003EB708  lea      rcx, [rip + 0x2773311]  ; -> 02B5EA20
003EB70F  mov      rax, qword ptr [rcx + rax*8]
003EB713  ret      
003EB714  xor      eax, eax
003EB716  ret      
```
