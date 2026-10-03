# Homing pack: `12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md`

Generated 2026-10-03 08:08 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-item-id-encoding-and-equipment-compatibility.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00264E40 (58 B, extent 00264E40-00264E7A)

Entered from (direct sites whose caller this page cites): `00264CA0` + 0x11 (call; `00264CA0` is cited on this page)
Other direct sites: none

Host context: "very anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*  | function | size | entered from | what the body does | interior anchors | |---|---|---|---|---| | '00264CA0' | 56 B | '003DFDD0' + 0x4C | when 'ecx' is 6 or 9, tail-jumps to '00264CA0' + 0x33 with 'ecx' and 'edx' unchanged; otherwise calls '00264CA0' + 0x11 with 'ecx' and 'edx', returns 0 when its result is negative (signed), and else ta"

```
00264E40  cmp      ecx, 8
00264E43  ja       0x264e76  ; -> 00264E76
00264E45  movsxd   rax, ecx
00264E48  lea      rdx, [rip - 0x144e4f]  ; -> 00120000 (image base)
00264E4F  mov      ecx, dword ptr [rdx + rax*4 + 0x144e7c]  ; image base + 0x144e7c = 00264E7C
00264E56  add      rcx, rdx
00264E59  jmp      rcx
00264E5B  mov      eax, 2
00264E60  ret      
00264E61  mov      eax, 3
00264E66  ret      
00264E67  mov      eax, 4
00264E6C  ret      
00264E6D  xor      eax, eax
00264E6F  ret      
00264E70  mov      eax, 1
00264E75  ret      
00264E76  or       eax, 0xffffffff
00264E79  ret      
```
