# F-interior pack: `22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/embedded-lua-and-phyre-object-bindings.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 6075e3017	SWE2-FRONTIER for FABLE: pass-22 unattributed appends - the other 11 PUBLISHABLE pages (batch 2, 21/; inbox mentions: SWE2-EC7.md). OPUS read these before packing.

## 00685FB0 (83 B, extent 00685FB0-00686003)

Page context: "teardown, and the remaining fifteen are all inside the       > scripting module itself — '00680950' ×2, '00681F30' ×6, '006836B0', '00683DC0',       > '00683F70', '00685810', '006858C0', '006859E0', '00685FB0'. *This is the enumeration       > behind 'DA-1''s stated bound (“the descriptor's other references are all inside the       > scripting module itself”), and the two that look like exceptions are the CRT's own       > teardown rath"

```
00685FB0  mov      qword ptr [rsp + 8], rbx
00685FB5  push     rdi
00685FB6  sub      rsp, 0x20
00685FBA  mov      rbx, r9
00685FBD  mov      rdi, r8
00685FC0  call     qword ptr [rcx + 8]
00685FC3  mov      rcx, rax
00685FC6  test     rbx, rbx
00685FC9  je       0x685ff6  ; -> 00685FF6
00685FCB  lea      rax, [rip + 0x27bb39e]  ; -> 02E41370
00685FD2  or       rax, 1
00685FD6  cmp      rdi, rax
00685FD9  jne      0x685ff6  ; -> 00685FF6
00685FDB  mov      qword ptr [rbx], 0
00685FE2  mov      eax, 1
00685FE7  mov      qword ptr [rbx + 8], rcx
00685FEB  mov      rbx, qword ptr [rsp + 0x30]
00685FF0  add      rsp, 0x20
00685FF4  pop      rdi
00685FF5  ret      
00685FF6  xor      eax, eax
00685FF8  mov      rbx, qword ptr [rsp + 0x30]
00685FFD  add      rsp, 0x20
00686001  pop      rdi
00686002  ret      
```
