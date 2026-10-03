# Homing pack: `14-Story-Event-Quest-Hunt/persistent-flag-banks.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-persistent-flag-banks.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003EB200 (79 B, extent 003EB200-003EB24F)

Entered from (direct sites whose caller this page cites): `003EC5B0` + 0x2D (call; `003EC5B0` is cited on this page)
Other direct sites: none

Host context: " anchor '0033CC39'; Interior anchor '0033CC49' | [world-loot-pickups-the-ten-slot-pool-and-the-despawn](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) | | '003EC5B0' | 56 B | '002FB560' + 0x33 | calls '003EC5B0' + 0x8 with the incoming 'ecx' and returns its value when non-zero; otherwise returns 0 when dword '02B5EC94' is zero or 'ecx' is above 15 (unsigned), and else calls + 0x2D with ('ecx',"

```
003EB200  mov      qword ptr [rsp + 8], rbx
003EB205  mov      qword ptr [rsp + 0x10], rsi
003EB20A  push     rdi
003EB20B  sub      rsp, 0x30
003EB20F  mov      eax, edx
003EB211  mov      esi, ecx
003EB213  mov      ecx, eax
003EB215  xor      edx, edx
003EB217  mov      ebx, r9d
003EB21A  mov      edi, r8d
003EB21D  call     0x2eae20  ; -> 002EAE20 fn
003EB222  test     rax, rax
003EB225  je       0x3eb23f  ; -> 003EB23F
003EB227  mov      edx, dword ptr [rsp + 0x60]
003EB22B  mov      r9d, ebx
003EB22E  mov      dword ptr [rsp + 0x20], edx
003EB232  mov      r8d, edi
003EB235  mov      rdx, rax
003EB238  mov      ecx, esi
003EB23A  call     0x3eb190  ; -> 003EB190 fn
003EB23F  mov      rbx, qword ptr [rsp + 0x40]
003EB244  mov      rsi, qword ptr [rsp + 0x48]
003EB249  add      rsp, 0x30
003EB24D  pop      rdi
003EB24E  ret      
```

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

## 003EB910 (37 B, extent 003EB910-003EB935)

Entered from (direct sites whose caller this page cites): `003EC770` + 0x44 (jmp; `003EC770` is cited on this page)
Other direct sites: `003471B0` + 0x75 (jmp); `0050E4A0` + 0x65 (jmp)

Host context: " anchor '003EC74C'; Interior anchor '003EC764' | [world-loot-pickups-the-ten-slot-pool-and-the-despawn](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) | | '003EC770' | 73 B | '002FB560' + 0x12A | keeps the incoming floats 'xmm1', 'xmm2' and 'xmm3' across a call to '003EC770' + 0x1E made with the incoming arguments, then tail-jumps (+ 0x44) with 'rcx' = the sign-extended dword that call returne"

```
003EB910  sub      rsp, 0x38
003EB914  test     rcx, rcx
003EB917  je       0x3eb930  ; -> 003EB930
003EB919  cmp      dword ptr [rcx + 0x10], 0
003EB91D  jl       0x3eb930  ; -> 003EB930
003EB91F  movzx    ecx, word ptr [rcx + 0x10]
003EB923  mov      dword ptr [rsp + 0x20], 1
003EB92B  call     0x3ec260  ; -> 003EC260 fn
003EB930  add      rsp, 0x38
003EB934  ret      
```
