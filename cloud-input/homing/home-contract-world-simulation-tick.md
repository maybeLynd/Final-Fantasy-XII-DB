# Homing pack: `00-Engine-Core-Runtime/Battle-Frame/CONTRACT-world-simulation-tick.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-world-simulation-tick.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002DEF20 (17 B, extent 002DEF20-002DEF31)

Entered from (direct sites whose caller this page cites): `00332C40` + 0x320 (call; `00332C40` is cited on this page)
Other direct sites: none

Host context: " '0024ED80' is also called from '0024B9B0' in UI - a shared utility callee, nothing more.  **Audio — SERVICE.** '00332750' (named on this page as the marker executor's caller side) calls Audio-owned '00332C40' for its '0x30'-stride marker probes, and shared '001EDDA0'/'00314020' entries carry Audio call traffic ('003B99D0', '002DEBA0', '00362850') - the tick borrows Audio helpers through the executor, no audio state lives here.   '00322"

```
002DEF20  xor      r8d, r8d
002DEF23  mov      r9d, edx
002DEF26  mov      edx, ecx
002DEF28  lea      ecx, [r8 + 1]
002DEF2C  jmp      0x1dbd60  ; -> 001DBD60 fn
```

## 002DF1A0 (56 B, extent 002DF1A0-002DF1D8)

Entered from (direct sites whose caller this page cites): `003B99D0` + 0x2EE (call; `003B99D0` is cited on this page)
Other direct sites: `0034D470` + 0x44 (jmp)

Host context: "332750' (named on this page as the marker executor's caller side) calls Audio-owned '00332C40' for its '0x30'-stride marker probes, and shared '001EDDA0'/'00314020' entries carry Audio call traffic ('003B99D0', '002DEBA0', '00362850') - the tick borrows Audio helpers through the executor, no audio state lives here.   '003229E0' (150 B) is the gated instantiate-helper '003A3E30''s arm runs (the ActorEntity/CombatAction borrowing noted in"

```
002DF1A0  sub      rsp, 0x38
002DF1A4  test     edx, edx
002DF1A6  jne      0x2df1bd  ; -> 002DF1BD
002DF1A8  mov      r9d, r8d
002DF1AB  mov      edx, ecx
002DF1AD  xor      r8d, r8d
002DF1B0  lea      ecx, [r8 + 1]
002DF1B4  add      rsp, 0x38
002DF1B8  jmp      0x1dbf00  ; -> 001DBF00 fn
002DF1BD  mov      dword ptr [rsp + 0x20], r8d
002DF1C2  mov      r9d, edx
002DF1C5  xor      r8d, r8d
002DF1C8  mov      edx, ecx
002DF1CA  lea      ecx, [r8 + 1]
002DF1CE  call     0x1dbfa0  ; -> 001DBFA0 fn
002DF1D3  add      rsp, 0x38
002DF1D7  ret      
```
