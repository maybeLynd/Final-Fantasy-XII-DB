# Homing pack: `15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-capability-inhibition-policy.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002E1630 (43 B, extent 002E1630-002E165B)

Entered from (direct sites whose caller this page cites): `002628B0` + 0x391 (call; `002628B0` is cited on this page)
Other direct sites: `00345E20` + 0xF (call)

Host context: "'0x139203' (bits 0, 1, 9, 12, 13,       16, 17, 20) that '002E1CD0(on, row)' sets or clears wholesale on **rows 0, 3 and 6** from the       field-entry, area-unload and notify functions ('00268D10', '002628B0', '00263050', '0026C3E0',       '0026C5D0', '00263660', '002678C0', '0025C830', '0025D580') and four menu handlers       ('00344C60', '00345140', '003456E0', '003464D0') — the script side's block set. *Readers:*       over all 25 c"

```
002E1630  sub      rsp, 0x28
002E1634  call     0x290180  ; -> 00290180 fn
002E1639  test     eax, eax
002E163B  je       0x2e1653  ; -> 002E1653
002E163D  sub      eax, 1
002E1640  je       0x2e164c  ; -> 002E164C
002E1642  cmp      eax, 1
002E1645  jne      0x2e164c  ; -> 002E164C
002E1647  add      rsp, 0x28
002E164B  ret      
002E164C  xor      eax, eax
002E164E  add      rsp, 0x28
002E1652  ret      
002E1653  or       eax, 0xffffffff
002E1656  add      rsp, 0x28
002E165A  ret      
```

## 002E2300 (9 B, extent 002E2300-002E2309)

Entered from (direct sites whose caller this page cites): `002628B0` + 0x105 (call; `002628B0` is cited on this page)
Other direct sites: `003406E0` + 0x12 (jmp)

Host context: "'0x139203' (bits 0, 1, 9, 12, 13,       16, 17, 20) that '002E1CD0(on, row)' sets or clears wholesale on **rows 0, 3 and 6** from the       field-entry, area-unload and notify functions ('00268D10', '002628B0', '00263050', '0026C3E0',       '0026C5D0', '00263660', '002678C0', '0025C830', '0025D580') and four menu handlers       ('00344C60', '00345140', '003456E0', '003464D0') — the script side's block set. *Readers:*       over all 25 c"

```
002E2300  mov      edx, ecx
002E2302  xor      ecx, ecx
002E2304  jmp      0x16d6a0  ; -> 0016D6A0 fn
```

## 003DF7B0 (89 B, extent 003DF7B0-003DF809)

Entered from (direct sites whose caller this page cites): `002628B0` + 0x133 (call; `002628B0` is cited on this page)
Other direct sites: `003546C0` + 0x1D (jmp); `00354B00` + 0x1A (jmp)

Host context: "'0x139203' (bits 0, 1, 9, 12, 13,       16, 17, 20) that '002E1CD0(on, row)' sets or clears wholesale on **rows 0, 3 and 6** from the       field-entry, area-unload and notify functions ('00268D10', '002628B0', '00263050', '0026C3E0',       '0026C5D0', '00263660', '002678C0', '0025C830', '0025D580') and four menu handlers       ('00344C60', '00345140', '003456E0', '003464D0') — the script side's block set. *Readers:*       over all 25 c"

```
003DF7B0  sub      rsp, 0x28
003DF7B4  mov      eax, dword ptr [rip + 0x277a55e]  ; -> 02B59D18
003DF7BA  test     edx, edx
003DF7BC  je       0x3df7c3  ; -> 003DF7C3
003DF7BE  btr      eax, ecx
003DF7C1  jmp      0x3df7c6  ; -> 003DF7C6
003DF7C3  bts      eax, ecx
003DF7C6  mov      dword ptr [rip + 0x277a54c], eax  ; -> 02B59D18
003DF7CC  test     eax, eax
003DF7CE  jne      0x3df7d9  ; -> 003DF7D9
003DF7D0  add      rsp, 0x28
003DF7D4  jmp      0x3df810  ; -> 003DF810 fn
003DF7D9  xor      r9d, r9d
003DF7DC  xor      r8d, r8d
003DF7DF  xor      edx, edx
003DF7E1  xor      ecx, ecx
003DF7E3  call     0x29cab0  ; -> 0029CAB0 fn
003DF7E8  xor      eax, eax
003DF7EA  mov      qword ptr [rip + 0x277a50f], rax  ; -> 02B59D00
003DF7F1  mov      qword ptr [rip + 0x277a510], rax  ; -> 02B59D08
003DF7F8  mov      dword ptr [rip + 0x277a512], eax  ; -> 02B59D10
003DF7FE  mov      dword ptr [rip + 0x277a510], eax  ; -> 02B59D14
003DF804  add      rsp, 0x28
003DF808  ret      
```
