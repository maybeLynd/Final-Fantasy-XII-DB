# F-interior pack: `99-Unresolved-Residual/Glyph-Run-Rendering/choosing-the-render-target-for-a-text-run.md`

Generated 2026-10-03 03:15 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/choosing-the-render-target-for-a-text-run.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: repos-78.md, repos-c9.md). OPUS read these before packing.

## 003655F0 (108 B, extent 003655F0-0036565C)

Page context: "quester '00365810' with a computed id ('003658D4'); the mode-2 chooser '0017FD00' is called only by the message-window family ('00364530', which passes 11 plus a window byte, '003647E0', '003649A0', '003655F0'), so in mode 2 'a' enumerates the message-window kinds, 11 upward, and the packed '(index << 5) + a' key is *window kind under slot*. The modes 0 and 1 chooser '0017FD30(a, flag, key)' has eight callers, all in the glyph-run famil"

```
003655F0  push     rbx
003655F2  sub      rsp, 0x20
003655F6  mov      rax, qword ptr [rip + 0x1f66803]  ; -> 022CBE00
003655FD  movsxd   rdx, ecx
00365600  mov      r8, qword ptr [rax + rdx*8 + 0x10]
00365605  xor      eax, eax
00365607  mov      edx, dword ptr [r8 + 4]
0036560B  lea      rbx, [r8 + 0x10]
0036560F  test     edx, edx
00365611  jle      0x365623  ; -> 00365623
00365613  cmp      word ptr [rbx], 0x30
00365617  je       0x36562b  ; -> 0036562B
00365619  inc      eax
0036561B  add      rbx, 0xc
0036561F  cmp      eax, edx
00365621  jl       0x365613  ; -> 00365613
00365623  xor      eax, eax
00365625  add      rsp, 0x20
00365629  pop      rbx
0036562A  ret      
0036562B  add      ecx, 0xb
0036562E  call     0x17fd00  ; -> 0017FD00 fn
00365633  movzx    ecx, word ptr [rbx]
00365636  call     0x17f8c0  ; -> 0017F8C0 fn
0036563B  test     rax, rax
0036563E  je       0x365652  ; -> 00365652
00365640  mov      ecx, dword ptr [rax + 0x1c]
00365643  call     0x17f9c0  ; -> 0017F9C0 fn
00365648  cvttss2si eax, xmm0
0036564C  add      rsp, 0x20
00365650  pop      rbx
00365651  ret      
00365652  movzx    eax, byte ptr [rbx + 4]
00365656  add      rsp, 0x20
0036565A  pop      rbx
0036565B  ret      
```
