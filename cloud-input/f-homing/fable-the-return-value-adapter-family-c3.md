# F homing pack (FABLE): `24-Compiler-And-CRT-Runtime/Generated-Adapters/the-return-value-adapter-family.md`

Generated 2026-10-03 06:31 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 006B2A60 (120 B, extent 006B2A60-006B2AD8)

Documented callee on this page: `00683B10`

```
006B2A60  push     rbx
006B2A62  sub      rsp, 0x20
006B2A66  mov      rcx, rdx
006B2A69  mov      rbx, r8
006B2A6C  call     0x683b10  ; -> 00683B10 fn
006B2A71  mov      rdx, rax
006B2A74  mov      ecx, dword ptr [rax]
006B2A76  mov      dword ptr [rbx], ecx
006B2A78  mov      ecx, dword ptr [rax + 4]
006B2A7B  mov      dword ptr [rbx + 4], ecx
006B2A7E  mov      ecx, dword ptr [rax + 8]
006B2A81  mov      dword ptr [rbx + 8], ecx
006B2A84  mov      ecx, dword ptr [rax + 0xc]
006B2A87  mov      dword ptr [rbx + 0xc], ecx
006B2A8A  mov      ecx, dword ptr [rax + 0x10]
006B2A8D  mov      dword ptr [rbx + 0x10], ecx
006B2A90  mov      ecx, dword ptr [rax + 0x14]
006B2A93  mov      dword ptr [rbx + 0x14], ecx
006B2A96  mov      eax, dword ptr [rax + 0x18]
006B2A99  mov      dword ptr [rbx + 0x18], eax
006B2A9C  mov      eax, dword ptr [rdx + 0x1c]
006B2A9F  mov      dword ptr [rbx + 0x1c], eax
006B2AA2  mov      eax, dword ptr [rdx + 0x20]
006B2AA5  mov      dword ptr [rbx + 0x20], eax
006B2AA8  mov      eax, dword ptr [rdx + 0x24]
006B2AAB  mov      dword ptr [rbx + 0x24], eax
006B2AAE  mov      eax, dword ptr [rdx + 0x28]
006B2AB1  mov      dword ptr [rbx + 0x28], eax
006B2AB4  mov      eax, dword ptr [rdx + 0x2c]
006B2AB7  mov      dword ptr [rbx + 0x2c], eax
006B2ABA  mov      eax, dword ptr [rdx + 0x30]
006B2ABD  mov      dword ptr [rbx + 0x30], eax
006B2AC0  mov      eax, dword ptr [rdx + 0x34]
006B2AC3  mov      dword ptr [rbx + 0x34], eax
006B2AC6  mov      eax, dword ptr [rdx + 0x38]
006B2AC9  mov      dword ptr [rbx + 0x38], eax
006B2ACC  mov      eax, dword ptr [rdx + 0x3c]
006B2ACF  mov      dword ptr [rbx + 0x3c], eax
006B2AD2  add      rsp, 0x20
006B2AD6  pop      rbx
006B2AD7  ret      
```
