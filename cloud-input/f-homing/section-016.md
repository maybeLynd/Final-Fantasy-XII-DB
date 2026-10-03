# F homing pack: `25-EBP-Script-Container/Sections/section-016.md`

Generated 2026-10-02 22:28 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 00264CA0 (56 B, extent 00264CA0-00264CD8)

Documented callee on this page: `003DFAC0`

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
