# F homing pack (FABLE): `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-the-battle-party.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 0034B4B0 (237 B, extent 0034B4B0-0034B59D)

Documented callee on this page: `00320800`

```
0034B4B0  mov      qword ptr [rsp + 0x10], rbx
0034B4B5  push     rbp
0034B4B6  push     rsi
0034B4B7  push     rdi
0034B4B8  sub      rsp, 0x70
0034B4BC  mov      rax, qword ptr [rip + 0x1bf936d]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0034B4C3  xor      rax, rsp
0034B4C6  mov      qword ptr [rsp + 0x68], rax
0034B4CB  mov      rsi, r9
0034B4CE  mov      rbx, rcx
0034B4D1  call     0x2640c0  ; -> 002640C0 fn
0034B4D6  mov      rbp, rax
0034B4D9  mov      edi, 5
0034B4DE  nop      
0034B4E0  mov      rcx, rsi
0034B4E3  call     0x267e10  ; -> 00267E10 fn
0034B4E8  mov      r8d, eax
0034B4EB  mov      rdx, rbx
0034B4EE  mov      rcx, rbp
0034B4F1  call     0x2650b0  ; -> 002650B0 fn
0034B4F6  mov      qword ptr [rsp + rdi*8 + 0x38], rax
0034B4FB  sub      rdi, 1
0034B4FF  jns      0x34b4e0  ; -> 0034B4E0
0034B501  mov      edi, 6
0034B506  lea      rcx, [rsp + 0x20]
0034B50B  mov      edx, edi
0034B50D  call     0x320800  ; -> 00320800 fn
0034B512  mov      edx, eax
0034B514  xor      eax, eax
0034B516  test     edx, edx
0034B518  cmovs    edx, eax
0034B51B  cmp      edx, edi
0034B51D  jge      0x34b536  ; -> 0034B536
0034B51F  sub      edi, edx
0034B521  movsxd   rax, edx
0034B524  movsxd   rcx, edi
0034B527  lea      rdi, [rsp + 0x20]
0034B52C  lea      rdi, [rdi + rax*4]
0034B530  or       rax, 0xffffffffffffffff
0034B534  rep stosd dword ptr [rdi], eax
0034B536  mov      ecx, dword ptr [rsp + 0x20]
0034B53A  mov      rax, qword ptr [rsp + 0x38]
0034B53F  mov      dword ptr [rax], ecx
0034B541  mov      rcx, rbx
0034B544  mov      edi, dword ptr [rsp + 0x24]
0034B548  mov      rax, qword ptr [rsp + 0x40]
0034B54D  mov      dword ptr [rax], edi
0034B54F  mov      edi, dword ptr [rsp + 0x28]
0034B553  mov      rax, qword ptr [rsp + 0x48]
0034B558  mov      dword ptr [rax], edi
0034B55A  mov      edi, dword ptr [rsp + 0x2c]
0034B55E  mov      rax, qword ptr [rsp + 0x50]
0034B563  mov      dword ptr [rax], edi
0034B565  mov      edi, dword ptr [rsp + 0x30]
0034B569  mov      rax, qword ptr [rsp + 0x58]
0034B56E  mov      dword ptr [rax], edi
0034B570  mov      rax, qword ptr [rsp + 0x60]
0034B575  mov      edi, dword ptr [rsp + 0x34]
0034B579  mov      dword ptr [rax], edi
0034B57B  call     0x26b4e0  ; -> 0026B4E0 fn
0034B580  mov      rcx, qword ptr [rsp + 0x68]
0034B585  xor      rcx, rsp
0034B588  call     0x808c40  ; -> 00808C40 fn
0034B58D  mov      rbx, qword ptr [rsp + 0x98]
0034B595  add      rsp, 0x70
0034B599  pop      rdi
0034B59A  pop      rsi
0034B59B  pop      rbp
0034B59C  ret      
```
