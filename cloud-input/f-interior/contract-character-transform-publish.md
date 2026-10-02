# F-interior pack: `17-Presentation-Rendering/CONTRACT-character-transform-publish.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-character-transform-publish.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

## 0034A3F0 (37 B, extent 0034A3F0-0034A415)

Page context: "zero floor instead of a byte being read. Interior anchor '0036EC3D' (the 'dec word [rax+0x16]').  ## SWE2-EC7-98 update (2026-09-20) - '002E49B0' measured  '002E49B0' (83 B) is the type-0x60 publish '0034A3F0', '0034A860', '0037B4D0' and '0037CF00' call: 'byte[rcx+3] & 0xE0 == 0x60' admits, 'rdx = [rcx+0xC0]' then '[+0x138]' must be non-null, 'r8' defaults to 'rdx+0x30' while 'rdx+0x50' is the second argument to '0026E530', and the call"

```
0034A3F0  push     rbx
0034A3F2  sub      rsp, 0x20
0034A3F6  mov      rbx, rdx
0034A3F9  mov      edx, 1
0034A3FE  mov      rcx, rbx
0034A401  call     0x26ad40  ; -> 0026AD40 fn
0034A406  xor      edx, edx
0034A408  mov      rcx, rbx
0034A40B  add      rsp, 0x20
0034A40F  pop      rbx
0034A410  jmp      0x2e49b0  ; -> 002E49B0 fn
```

## 0034A860 (137 B, extent 0034A860-0034A8E9)

Page context: "nstead of a byte being read. Interior anchor '0036EC3D' (the 'dec word [rax+0x16]').  ## SWE2-EC7-98 update (2026-09-20) - '002E49B0' measured  '002E49B0' (83 B) is the type-0x60 publish '0034A3F0', '0034A860', '0037B4D0' and '0037CF00' call: 'byte[rcx+3] & 0xE0 == 0x60' admits, 'rdx = [rcx+0xC0]' then '[+0x138]' must be non-null, 'r8' defaults to 'rdx+0x30' while 'rdx+0x50' is the second argument to '0026E530', and the call's result bi"

```
0034A860  mov      qword ptr [rsp + 8], rbx
0034A865  push     rdi
0034A866  sub      rsp, 0x40
0034A86A  mov      rax, qword ptr [rip + 0x1bf9fbf]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0034A871  xor      rax, rsp
0034A874  mov      qword ptr [rsp + 0x30], rax
0034A879  movss    xmm0, dword ptr [rip + 0x19a1327]  ; -> 01CEBBA8 [f32 1]
0034A881  mov      rcx, r9
0034A884  movss    dword ptr [rsp + 0x2c], xmm0
0034A88A  mov      rbx, r9
0034A88D  mov      rdi, rdx
0034A890  call     0x267db0  ; -> 00267DB0 fn
0034A895  mov      rcx, rbx
0034A898  movss    dword ptr [rsp + 0x28], xmm0
0034A89E  call     0x267db0  ; -> 00267DB0 fn
0034A8A3  mov      rcx, rbx
0034A8A6  movss    dword ptr [rsp + 0x24], xmm0
0034A8AC  call     0x267db0  ; -> 00267DB0 fn
0034A8B1  mov      edx, 1
0034A8B6  movss    dword ptr [rsp + 0x20], xmm0
0034A8BC  mov      rcx, rdi
0034A8BF  call     0x26ad40  ; -> 0026AD40 fn
0034A8C4  lea      rdx, [rsp + 0x20]
0034A8C9  mov      rcx, rdi
0034A8CC  call     0x2e49b0  ; -> 002E49B0 fn
0034A8D1  mov      rcx, qword ptr [rsp + 0x30]
0034A8D6  xor      rcx, rsp
0034A8D9  call     0x808c40  ; -> 00808C40 fn
0034A8DE  mov      rbx, qword ptr [rsp + 0x50]
0034A8E3  add      rsp, 0x40
0034A8E7  pop      rdi
0034A8E8  ret      
```
