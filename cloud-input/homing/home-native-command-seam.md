# Homing pack: `07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`

Generated 2026-10-02 22:54 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-native-command-seam.json`.

Bodies: 6. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0026AB60 (58 B, extent 0026AB60-0026AB9A)

Entered from (direct sites whose caller this page cites): `00355A00` + 0x1C6 (call; `00355A00` is cited on this page)
Other direct sites: `00352500` + 0x20 (jmp)

Host context: "nit_RunPeriodicCombatMaintenance', and another calls 'BattleStats_ChangeStatusAndProcessSideEffects'.  **Party — CLIENT (SWE2-EC7-158, 25 edges).** Batch-123's '0026B4A0' names '00351F40'/'00355540'/'00355A00'/'00238BF0', and the seam's own '0026D6D0' is called by the party layer's '00358B40'/'00359200'/'00359250'/'003592C0' — the party side consults the seam's helpers, fan-in only.  - **CombatFormula — SERVICE (3 edges).** 'BattleUnit_"

```
0026AB60  movzx    edx, byte ptr [rcx + 3]
0026AB64  movss    xmm0, dword ptr [rip + 0x688578]  ; -> 008F30E4 [f32 0.01]
0026AB6C  shr      edx, 5
0026AB6F  maxss    xmm0, xmm1
0026AB73  sub      edx, 1
0026AB76  je       0x26ab8d  ; -> 0026AB8D
0026AB78  cmp      edx, 2
0026AB7B  jne      0x26ab99  ; -> 0026AB99
0026AB7D  mov      rax, qword ptr [rcx + 0xb8]
0026AB84  movss    dword ptr [rax + 0xfc], xmm0
0026AB8C  ret      
0026AB8D  mov      rax, qword ptr [rcx + 0xb8]
0026AB94  movss    dword ptr [rax + 0x70], xmm0
0026AB99  ret      
```

## 0026B480 (29 B, extent 0026B480-0026B49D)

Entered from (direct sites whose caller this page cites): `00355A00` + 0x64 (call; `00355A00` is cited on this page)
Other direct sites: `00349960` + 0x8 (jmp)

Host context: "nit_RunPeriodicCombatMaintenance', and another calls 'BattleStats_ChangeStatusAndProcessSideEffects'.  **Party — CLIENT (SWE2-EC7-158, 25 edges).** Batch-123's '0026B4A0' names '00351F40'/'00355540'/'00355A00'/'00238BF0', and the seam's own '0026D6D0' is called by the party layer's '00358B40'/'00359200'/'00359250'/'003592C0' — the party side consults the seam's helpers, fan-in only.  - **CombatFormula — SERVICE (3 edges).** 'BattleUnit_"

```
0026B480  movzx    r8d, byte ptr [rcx + 3]
0026B485  shr      r8d, 5
0026B489  cmp      r8d, 1
0026B48D  jne      0x26b49c  ; -> 0026B49C
0026B48F  and      byte ptr [rcx + 0xd], 0xf7
0026B493  and      dl, r8b
0026B496  shl      dl, 3
0026B499  or       byte ptr [rcx + 0xd], dl
0026B49C  ret      
```

## 0026BB00 (66 B, extent 0026BB00-0026BB42)

Entered from (direct sites whose caller this page cites): `00355A00` + 0x159 (call; `00355A00` is cited on this page)
Other direct sites: none

Host context: "nit_RunPeriodicCombatMaintenance', and another calls 'BattleStats_ChangeStatusAndProcessSideEffects'.  **Party — CLIENT (SWE2-EC7-158, 25 edges).** Batch-123's '0026B4A0' names '00351F40'/'00355540'/'00355A00'/'00238BF0', and the seam's own '0026D6D0' is called by the party layer's '00358B40'/'00359200'/'00359250'/'003592C0' — the party side consults the seam's helpers, fan-in only.  - **CombatFormula — SERVICE (3 edges).** 'BattleUnit_"

```
0026BB00  movzx    edx, byte ptr [rcx + 3]
0026BB04  shr      edx, 5
0026BB07  sub      edx, 1
0026BB0A  je       0x26bb2b  ; -> 0026BB2B
0026BB0C  cmp      edx, 2
0026BB0F  jne      0x26bb41  ; -> 0026BB41
0026BB11  mov      rax, qword ptr [rcx + 0xb8]
0026BB18  subss    xmm3, dword ptr [rax + 8]
0026BB1D  subss    xmm2, dword ptr [rax + 4]
0026BB22  subss    xmm1, dword ptr [rax]
0026BB26  jmp      0x26ba70  ; -> 0026BA70 fn
0026BB2B  mov      rax, qword ptr [rcx + 0xb8]
0026BB32  movss    dword ptr [rax + 0x10], xmm1
0026BB37  movss    dword ptr [rax + 0x14], xmm2
0026BB3C  movss    dword ptr [rax + 0x18], xmm3
0026BB41  ret      
```

## 0026BDD0 (35 B, extent 0026BDD0-0026BDF3)

Entered from (direct sites whose caller this page cites): `00355A00` + 0x1AC (call; `00355A00` is cited on this page)
Other direct sites: none

Host context: "nit_RunPeriodicCombatMaintenance', and another calls 'BattleStats_ChangeStatusAndProcessSideEffects'.  **Party — CLIENT (SWE2-EC7-158, 25 edges).** Batch-123's '0026B4A0' names '00351F40'/'00355540'/'00355A00'/'00238BF0', and the seam's own '0026D6D0' is called by the party layer's '00358B40'/'00359200'/'00359250'/'003592C0' — the party side consults the seam's helpers, fan-in only.  - **CombatFormula — SERVICE (3 edges).** 'BattleUnit_"

```
0026BDD0  movzx    edx, byte ptr [rcx + 3]
0026BDD4  shr      edx, 5
0026BDD7  cmp      edx, 1
0026BDDA  jne      0x26bdf2  ; -> 0026BDF2
0026BDDC  mov      rax, qword ptr [rcx + 0xb8]
0026BDE3  movss    dword ptr [rax + 0x20], xmm1
0026BDE8  movss    dword ptr [rax + 0x24], xmm2
0026BDED  movss    dword ptr [rax + 0x28], xmm3
0026BDF2  ret      
```

## 0026BFF0 (113 B, extent 0026BFF0-0026C061)

Entered from (direct sites whose caller this page cites): `00355A00` + 0x11B (call; `00355A00` is cited on this page)
Other direct sites: `00351E00` + 0x40 (jmp); `00352810` + 0x53 (call); `00352C00` + 0x36 (call)

Host context: "nit_RunPeriodicCombatMaintenance', and another calls 'BattleStats_ChangeStatusAndProcessSideEffects'.  **Party — CLIENT (SWE2-EC7-158, 25 edges).** Batch-123's '0026B4A0' names '00351F40'/'00355540'/'00355A00'/'00238BF0', and the seam's own '0026D6D0' is called by the party layer's '00358B40'/'00359200'/'00359250'/'003592C0' — the party side consults the seam's helpers, fan-in only.  - **CombatFormula — SERVICE (3 edges).** 'BattleUnit_"

```
0026BFF0  movzx    edx, byte ptr [rcx + 3]
0026BFF4  xorps    xmm0, xmm0
0026BFF7  cvtss2sd xmm0, xmm1
0026BFFB  shr      edx, 5
0026BFFE  andps    xmm0, xmmword ptr [rip + 0x1a7fd7b]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
0026C005  cvtpd2ps xmm1, xmm0
0026C009  xorps    xmm0, xmm0
0026C00C  cvtss2sd xmm0, xmm2
0026C010  andps    xmm0, xmmword ptr [rip + 0x1a7fd69]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
0026C017  cvtpd2ps xmm4, xmm0
0026C01B  sub      edx, 1
0026C01E  je       0x26c02d  ; -> 0026C02D
0026C020  cmp      edx, 2
0026C023  jne      0x26c060  ; -> 0026C060
0026C025  movaps   xmm2, xmm4
0026C028  jmp      0x26bf60  ; -> 0026BF60 fn
0026C02D  mov      rax, qword ptr [rcx + 0xb8]
0026C034  or       byte ptr [rax + 0x5d], 2
0026C038  movss    xmm0, dword ptr [rax + 0x40]
0026C03D  comiss   xmm0, xmm1
0026C040  movss    dword ptr [rax + 0x30], xmm1
0026C045  movss    dword ptr [rax + 0x34], xmm4
0026C04A  jbe      0x26c051  ; -> 0026C051
0026C04C  movss    dword ptr [rax + 0x40], xmm1
0026C051  movss    xmm0, dword ptr [rax + 0x44]
0026C056  comiss   xmm0, xmm4
0026C059  jbe      0x26c060  ; -> 0026C060
0026C05B  movss    dword ptr [rax + 0x44], xmm4
0026C060  ret      
```

## 003DF790 (27 B, extent 003DF790-003DF7AB)

Entered from (direct sites whose caller this page cites): `00355A00` + 0xB6 (call; `00355A00` is cited on this page)
Other direct sites: none

Host context: "nit_RunPeriodicCombatMaintenance', and another calls 'BattleStats_ChangeStatusAndProcessSideEffects'.  **Party — CLIENT (SWE2-EC7-158, 25 edges).** Batch-123's '0026B4A0' names '00351F40'/'00355540'/'00355A00'/'00238BF0', and the seam's own '0026D6D0' is called by the party layer's '00358B40'/'00359200'/'00359250'/'003592C0' — the party side consults the seam's helpers, fan-in only.  - **CombatFormula — SERVICE (3 edges).** 'BattleUnit_"

```
003DF790  test     ecx, ecx
003DF792  je       0x3df7a5  ; -> 003DF7A5
003DF794  cmp      ecx, 1
003DF797  je       0x3df79f  ; -> 003DF79F
003DF799  mov      eax, 1
003DF79E  ret      
003DF79F  mov      eax, 2
003DF7A4  ret      
003DF7A5  mov      eax, 3
003DF7AA  ret      
```
