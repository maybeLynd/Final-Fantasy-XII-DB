# Homing pack: `99-Unresolved-Residual/Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-painting-a-line-of-text-into-a-render-target.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001FDF10 (85 B, extent 001FDF10-001FDF65)

Entered from (direct sites whose caller this page cites): `001B58E0` + 0x109 (call; `001B58E0` is cited on this page)
Other direct sites: `001B6230` + 0x24 (call)

Host context: "1; 2026-10-02, OPUS)*; that is a staging state, not a claim about the code.  *(Pass 22 adjacency, 2026-09-14: the paint path crosses out through shared helpers — '001E9A20' is called by **resource** '001B58E0', '001E8070' calls **audio** '00225690', and '002134A0' is called by **actor** '00234480' (3 edges). The paint pass is reached from resource-loading and actor contexts through shared accessors; adjacency, not ownership.)*  *(Pass 2"

```
001FDF10  mov      qword ptr [rsp + 8], rbx
001FDF15  push     rdi
001FDF16  sub      rsp, 0x30
001FDF1A  xor      eax, eax
001FDF1C  mov      rdi, rdx
001FDF1F  mov      qword ptr [rdx], rax
001FDF22  mov      rbx, rcx
001FDF25  mov      qword ptr [rdx + 8], rax
001FDF29  mov      qword ptr [rdx + 0x10], rax
001FDF2D  lea      rdx, [rcx + 0xf8]
001FDF34  lea      rcx, [rdi + 0x18]
001FDF38  mov      dword ptr [rsp + 0x20], eax
001FDF3C  call     0x1edf00  ; -> 001EDF00 fn
001FDF41  mov      r8, qword ptr [rbx + 0xe8]
001FDF48  mov      rcx, rdi
001FDF4B  mov      rdx, qword ptr [rbx + 0xe0]
001FDF52  call     0x1a4bf0  ; -> 001A4BF0 fn
001FDF57  mov      rbx, qword ptr [rsp + 0x40]
001FDF5C  mov      rax, rdi
001FDF5F  add      rsp, 0x30
001FDF63  pop      rdi
001FDF64  ret      
```
