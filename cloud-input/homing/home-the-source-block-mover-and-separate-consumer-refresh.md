# Homing pack: `02-Resource-And-Asset-Pipeline/the-source-block-mover-and-separate-consumer-refresh.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-source-block-mover-and-separate-consumer-refresh.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00420860 (35 B, extent 00420860-00420883)

Entered from (direct sites whose caller this page cites): `00427DE0` + 0xD7 (call; `00427DE0` is cited on this page)
Other direct sites: none

Host context: "x304[31:27]':  - '003E6AA0' replaces the previous five-bit index and preserves the low 27 bits. It is one coalesced   request, not a FIFO. The issuer itself does not enforce the later index bound. - '00427DE0' skips delivery and keeps the bit when 'record+0x288 == -1'. - Otherwise it calls '003B3C00' and clears the bit regardless of success. A stale full ticket,   invalid index, or failed start is not automatically retried by retaining "

```
00420860  sub      rsp, 0x38
00420864  movss    xmm0, dword ptr [rip + 0x18cb33c]  ; -> 01CEBBA8 [f32 1]
0042086C  add      rcx, 0x210
00420873  movss    dword ptr [rsp + 0x20], xmm0
00420879  call     0x6c0520  ; -> 006C0520 fn
0042087E  add      rsp, 0x38
00420882  ret      
```

## 004209F0 (22 B, extent 004209F0-00420A06)

Entered from (direct sites whose caller this page cites): `00427DE0` + 0xA2 (call; `00427DE0` is cited on this page)
Other direct sites: none

Host context: "x304[31:27]':  - '003E6AA0' replaces the previous five-bit index and preserves the low 27 bits. It is one coalesced   request, not a FIFO. The issuer itself does not enforce the later index bound. - '00427DE0' skips delivery and keeps the bit when 'record+0x288 == -1'. - Otherwise it calls '003B3C00' and clears the bit regardless of success. A stale full ticket,   invalid index, or failed start is not automatically retried by retaining "

```
004209F0  or       dword ptr [rcx + 0x284], 0x200
004209FA  add      rcx, 0x180
00420A01  jmp      0x46d100  ; -> 0046D100 fn
```
