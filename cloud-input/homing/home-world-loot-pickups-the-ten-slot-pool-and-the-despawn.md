# Homing pack: `13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md`

Generated 2026-10-02 22:54 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-world-loot-pickups-the-ten-slot-pool-and-the-despawn.json`.

Bodies: 6. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00231F20 (43 B, extent 00231F20-00231F4B)

Entered from (direct sites whose caller this page cites): `002FB560` + 0xA5 (call; `002FB560` is cited on this page)
Other direct sites: none

Host context: "ored id selector '00231900' and the record read '00231820', and the selector's helpers cited in the appended note ('00231890', '002324F0', '00233050') and their other callers, among them '0026E3C0', '002FB560', '003808A0' and '0022F430', are movement bodies; '0026A1D0' calls '00226BE0'; the time-base writer '001EDDC0' calls '00337A00', which re-derives two movement timing constants from the new frame-rate scalar. The remaining edges are"

```
00231F20  movsx    r9, r8w
00231F24  mov      r8, qword ptr [rcx + 0x10]
00231F28  shl      r9, 5
00231F2C  mov      eax, dword ptr [r9 + r8]
00231F30  mov      dword ptr [rdx], eax
00231F32  mov      eax, dword ptr [r9 + r8 + 4]
00231F37  mov      dword ptr [rdx + 4], eax
00231F3A  mov      eax, dword ptr [r9 + r8 + 8]
00231F3F  mov      dword ptr [rdx + 8], eax
00231F42  mov      eax, dword ptr [r9 + r8 + 0xc]
00231F47  mov      dword ptr [rdx + 0xc], eax
00231F4A  ret      
```

## 002E9BE0 (26 B, extent 002E9BE0-002E9BFA)

Entered from (direct sites whose caller this page cites): `003B73B0` + 0x49 (call; `003B73B0` is cited on this page)
Other direct sites: `003B7440` + 0x78 (call); `003B7510` + 0x72 (call)

Host context: " — 'BattleUnit_SnapshotWorldActorRuntimeState' ('00236300'), 'ActorManager_RunFieldRuntimePass' ('0025D9E0') and nine more readers of the focus handle '003590D0', the position readers '0037B4D0' and '003B73B0', the matrix and fill leaves' callers '003F1E90' and '00400AC0' — plus the actor lookups of the two bodies cited only as callers ('00226BE0' reaching 'ActorHandle_ResolveRegistryEntryByPackedId' '003588B0' and 'ActorManager_GetReco"

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

## 0033CBF0 (129 B, extent 0033CBF0-0033CC71)

Entered from (direct sites whose caller this page cites): `002FB560` + 0xFB (call; `002FB560` is cited on this page)
Other direct sites: none

Host context: "ored id selector '00231900' and the record read '00231820', and the selector's helpers cited in the appended note ('00231890', '002324F0', '00233050') and their other callers, among them '0026E3C0', '002FB560', '003808A0' and '0022F430', are movement bodies; '0026A1D0' calls '00226BE0'; the time-base writer '001EDDC0' calls '00337A00', which re-derives two movement timing constants from the new frame-rate scalar. The remaining edges are"

```
0033CBF0  mov      qword ptr [rsp + 0x20], rbx
0033CBF5  push     rdi
0033CBF6  sub      rsp, 0x80
0033CBFD  movaps   xmmword ptr [rsp + 0x70], xmm6
0033CC02  mov      rax, qword ptr [rip + 0x1c07c27]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0033CC09  xor      rax, rsp
0033CC0C  mov      qword ptr [rsp + 0x60], rax
0033CC11  mov      rdi, rcx
0033CC14  movaps   xmm6, xmm2
0033CC17  lea      rcx, [rsp + 0x20]
0033CC1C  mov      rbx, rdx
0033CC1F  call     0x203170  ; -> 00203170 fn
0033CC24  movaps   xmm0, xmm6
0033CC27  call     0x33cb70  ; -> 0033CB70 fn
0033CC2C  movaps   xmm2, xmm0
0033CC2F  lea      rdx, [rsp + 0x20]
0033CC34  lea      rcx, [rsp + 0x20]
0033CC39  call     0x202f00  ; -> 00202F00 fn
0033CC3E  mov      r8, rbx
0033CC41  lea      rdx, [rsp + 0x20]
0033CC46  mov      rcx, rdi
0033CC49  call     0x202b70  ; -> 00202B70 fn
0033CC4E  mov      rcx, qword ptr [rsp + 0x60]
0033CC53  xor      rcx, rsp
0033CC56  call     0x808c40  ; -> 00808C40 fn
0033CC5B  mov      rbx, qword ptr [rsp + 0xa8]
0033CC63  movaps   xmm6, xmmword ptr [rsp + 0x70]
0033CC68  add      rsp, 0x80
0033CC6F  pop      rdi
0033CC70  ret      
```

## 003EC5B0 (56 B, extent 003EC5B0-003EC5E8)

Entered from (direct sites whose caller this page cites): `002FB560` + 0x33 (call; `002FB560` is cited on this page)
Other direct sites: none

Host context: "ored id selector '00231900' and the record read '00231820', and the selector's helpers cited in the appended note ('00231890', '002324F0', '00233050') and their other callers, among them '0026E3C0', '002FB560', '003808A0' and '0022F430', are movement bodies; '0026A1D0' calls '00226BE0'; the time-base writer '001EDDC0' calls '00337A00', which re-derives two movement timing constants from the new frame-rate scalar. The remaining edges are"

```
003EC5B0  push     rbx
003EC5B2  sub      rsp, 0x30
003EC5B6  mov      ebx, ecx
003EC5B8  call     0x377c20  ; -> 00377C20 fn
003EC5BD  test     eax, eax
003EC5BF  jne      0x3ec5e2  ; -> 003EC5E2
003EC5C1  mov      edx, dword ptr [rip + 0x27726cd]  ; -> 02B5EC94
003EC5C7  test     edx, edx
003EC5C9  je       0x3ec5e2  ; -> 003EC5E2
003EC5CB  cmp      ebx, 0xf
003EC5CE  ja       0x3ec5e2  ; -> 003EC5E2
003EC5D0  lea      r9d, [rax + 1]
003EC5D4  mov      dword ptr [rsp + 0x20], eax
003EC5D8  xor      r8d, r8d
003EC5DB  mov      ecx, ebx
003EC5DD  call     0x3eb200  ; -> 003EB200 fn
003EC5E2  add      rsp, 0x30
003EC5E6  pop      rbx
003EC5E7  ret      
```

## 003EC720 (73 B, extent 003EC720-003EC769)

Entered from (direct sites whose caller this page cites): `002FB560` + 0x79 (call; `002FB560` is cited on this page)
Other direct sites: none

Host context: "ored id selector '00231900' and the record read '00231820', and the selector's helpers cited in the appended note ('00231890', '002324F0', '00233050') and their other callers, among them '0026E3C0', '002FB560', '003808A0' and '0022F430', are movement bodies; '0026A1D0' calls '00226BE0'; the time-base writer '001EDDC0' calls '00337A00', which re-derives two movement timing constants from the new frame-rate scalar. The remaining edges are"

```
003EC720  sub      rsp, 0x58
003EC724  movaps   xmmword ptr [rsp + 0x40], xmm6
003EC729  movaps   xmm6, xmm3
003EC72C  movaps   xmmword ptr [rsp + 0x30], xmm7
003EC731  movaps   xmm7, xmm2
003EC734  movaps   xmmword ptr [rsp + 0x20], xmm8
003EC73A  movaps   xmm8, xmm1
003EC73E  call     0x3eb700  ; -> 003EB700 fn
003EC743  movsxd   rcx, eax
003EC746  movaps   xmm3, xmm6
003EC749  movaps   xmm2, xmm7
003EC74C  movaps   xmm1, xmm8
003EC750  movaps   xmm6, xmmword ptr [rsp + 0x40]
003EC755  movaps   xmm7, xmmword ptr [rsp + 0x30]
003EC75A  movaps   xmm8, xmmword ptr [rsp + 0x20]
003EC760  add      rsp, 0x58
003EC764  jmp      0x3eb8e0  ; -> 003EB8E0 fn
```

## 003EC770 (73 B, extent 003EC770-003EC7B9)

Entered from (direct sites whose caller this page cites): `002FB560` + 0x12A (call; `002FB560` is cited on this page)
Other direct sites: none

Host context: "ored id selector '00231900' and the record read '00231820', and the selector's helpers cited in the appended note ('00231890', '002324F0', '00233050') and their other callers, among them '0026E3C0', '002FB560', '003808A0' and '0022F430', are movement bodies; '0026A1D0' calls '00226BE0'; the time-base writer '001EDDC0' calls '00337A00', which re-derives two movement timing constants from the new frame-rate scalar. The remaining edges are"

```
003EC770  sub      rsp, 0x58
003EC774  movaps   xmmword ptr [rsp + 0x40], xmm6
003EC779  movaps   xmm6, xmm3
003EC77C  movaps   xmmword ptr [rsp + 0x30], xmm7
003EC781  movaps   xmm7, xmm2
003EC784  movaps   xmmword ptr [rsp + 0x20], xmm8
003EC78A  movaps   xmm8, xmm1
003EC78E  call     0x3eb700  ; -> 003EB700 fn
003EC793  movsxd   rcx, eax
003EC796  movaps   xmm3, xmm6
003EC799  movaps   xmm2, xmm7
003EC79C  movaps   xmm1, xmm8
003EC7A0  movaps   xmm6, xmmword ptr [rsp + 0x40]
003EC7A5  movaps   xmm7, xmmword ptr [rsp + 0x30]
003EC7AA  movaps   xmm8, xmmword ptr [rsp + 0x20]
003EC7B0  add      rsp, 0x58
003EC7B4  jmp      0x3eb910  ; -> 003EB910 fn
```
