# F homing pack: `25-EBP-Script-Container/Sections/section-002-text.md`

Generated 2026-10-02 22:28 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 00357820 (133 B, extent 00357820-003578A5)

Documented callee on this page: `002E1E40`

```
00357820  mov      qword ptr [rsp + 8], rbx
00357825  mov      qword ptr [rsp + 0x10], rbp
0035782A  mov      qword ptr [rsp + 0x18], rsi
0035782F  mov      qword ptr [rsp + 0x20], rdi
00357834  push     r14
00357836  sub      rsp, 0x20
0035783A  mov      rcx, r9
0035783D  mov      rdi, r9
00357840  mov      r14, r8
00357843  call     0x267e10  ; -> 00267E10 fn
00357848  mov      rcx, rdi
0035784B  mov      ebp, eax
0035784D  call     0x267e10  ; -> 00267E10 fn
00357852  mov      rcx, rdi
00357855  mov      esi, eax
00357857  call     0x267e10  ; -> 00267E10 fn
0035785C  mov      rcx, rdi
0035785F  mov      ebx, eax
00357861  call     0x267e10  ; -> 00267E10 fn
00357866  mov      edi, eax
00357868  mov      dword ptr [r14], eax
0035786B  xor      eax, eax
0035786D  movzx    ecx, bl
00357870  test     esi, esi
00357872  mov      edx, esi
00357874  cmove    ecx, eax
00357877  mov      byte ptr [r14 + 0xd], cl
0035787B  mov      ecx, edi
0035787D  call     0x2e1e40  ; -> 002E1E40 fn
00357882  mov      edx, ebp
00357884  mov      ecx, edi
00357886  mov      rbx, qword ptr [rsp + 0x30]
0035788B  mov      rbp, qword ptr [rsp + 0x38]
00357890  mov      rsi, qword ptr [rsp + 0x40]
00357895  mov      rdi, qword ptr [rsp + 0x48]
0035789A  add      rsp, 0x20
0035789E  pop      r14
003578A0  jmp      0x2e1e70  ; -> 002E1E70 fn
```
