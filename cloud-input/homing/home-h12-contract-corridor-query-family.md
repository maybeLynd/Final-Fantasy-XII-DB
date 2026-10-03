# Homing pack: `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md`

Generated 2026-10-03 12:43 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h12-contract-corridor-query-family.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00264CE0 (56 B, extent 00264CE0-00264D18)

Entered from (direct sites whose caller this page cites): `0033F7F0` + 0x21 (call; `0033F7F0` is cited on this page)
Other direct sites: none

Host context: "02EF640' - shared machinery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (26 edges).** '00263FF0' is also called by bodies filed to script VM / native bridge: '0033F7F0', '00342490', '00342A30' - shared machinery across the layer boundary, no shared ownership. - **Spawn_Encounter_Lifecycle - CLIENT (30 edges).** '00236820', '0031B760' are also called by bodies filed to spawn/encounter lifecycle: '"

```
00264CE0  test     rcx, rcx
00264CE3  je       0x264d10  ; -> 00264D10
00264CE5  mov      rax, qword ptr [rcx]
00264CE8  test     rax, rax
00264CEB  je       0x264d10  ; -> 00264D10
00264CED  cmp      edx, -1
00264CF0  jne      0x264cf6  ; -> 00264CF6
00264CF2  movsx    edx, word ptr [rax + 0x52]
00264CF6  cmp      edx, -2
00264CF9  jne      0x264cff  ; -> 00264CFF
00264CFB  movsx    edx, word ptr [rax + 0x78]
00264CFF  cmp      edx, -3
00264D02  jne      0x264d08  ; -> 00264D08
00264D04  movsx    edx, word ptr [rax + 0x7a]
00264D08  test     edx, edx
00264D0A  jns      0x264d10  ; -> 00264D10
00264D0C  movsx    edx, word ptr [rax + 0x52]
00264D10  xor      eax, eax
00264D12  test     edx, edx
00264D14  cmovns   eax, edx
00264D17  ret      
```
