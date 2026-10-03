# Homing pack: `12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-item-id-encoding-and-equipment-compatibility.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00264CA0 (56 B, extent 00264CA0-00264CD8)

Entered from (direct sites whose caller this page cites): `003DFDD0` + 0x4C (call; `003DFDD0` is cited on this page)
Other direct sites: `00352C80` + 0x2B (call); `003532D0` + 0x2B (call)

Host context: "very anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*  | function | size | entered from | what the body does | interior anchors | |---|---|---|---|---| | '003DFDD0' | 104 B | '003DFBE0' + 0x2F | zeroes the two qwords at 'r8'; when 'ecx - 1' is above 7 (unsigned) it goes straight to the return, otherwise it dispatches on 'ecx' through an indexed table: 1 and 2 reach a call ('003DFDD0' + 0x35) "

```
00264CA0  sub      rsp, 0x28
00264CA4  mov      r8d, edx
00264CA7  cmp      ecx, 6
00264CAA  je       0x264ccf  ; -> 00264CCF
00264CAC  cmp      ecx, 9
00264CAF  je       0x264ccf  ; -> 00264CCF
00264CB1  call     0x264e40  ; -> 00264E40 fn
00264CB6  test     eax, eax
00264CB8  js       0x264cc8  ; -> 00264CC8
00264CBA  mov      edx, r8d
00264CBD  mov      ecx, eax
00264CBF  add      rsp, 0x28
00264CC3  jmp      0x2649b0  ; -> 002649B0 fn
00264CC8  xor      eax, eax
00264CCA  add      rsp, 0x28
00264CCE  ret      
00264CCF  add      rsp, 0x28
00264CD3  jmp      0x3dfac0  ; -> 003DFAC0 fn
```
