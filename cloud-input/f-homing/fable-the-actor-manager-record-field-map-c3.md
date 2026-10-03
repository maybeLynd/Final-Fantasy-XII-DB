# F homing pack (FABLE): `04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md`

Generated 2026-10-03 06:31 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 003E9480 (80 B, extent 003E9480-003E94D0)

Documented callee on this page: `002E1040`

```
003E9480  mov      qword ptr [rsp + 8], rbx
003E9485  push     rdi
003E9486  sub      rsp, 0x20
003E948A  mov      ebx, r8d
003E948D  movsxd   rdi, edx
003E9490  call     0x2e1040  ; -> 002E1040 fn
003E9495  mov      r9, qword ptr [rax]
003E9498  test     r9, r9
003E949B  je       0x3e94c5  ; -> 003E94C5
003E949D  movzx    eax, word ptr [rax + 0x54]
003E94A1  cmp      edi, eax
003E94A3  jge      0x3e94c5  ; -> 003E94C5
003E94A5  cmp      byte ptr [r9 + 0x3f3], 0
003E94AD  jl       0x3e94c5  ; -> 003E94C5
003E94AF  mov      rax, qword ptr [r9 + 0x3f8]
003E94B6  lea      rcx, [rdi + rdi*2]
003E94BA  shl      bl, 4
003E94BD  shl      rcx, 5
003E94C1  mov      byte ptr [rcx + rax + 0xd], bl
003E94C5  mov      rbx, qword ptr [rsp + 0x30]
003E94CA  add      rsp, 0x20
003E94CE  pop      rdi
003E94CF  ret      
```

## 003E94D0 (85 B, extent 003E94D0-003E9525)

Documented callee on this page: `002E1040`

```
003E94D0  mov      qword ptr [rsp + 8], rbx
003E94D5  push     rdi
003E94D6  sub      rsp, 0x30
003E94DA  mov      rbx, r8
003E94DD  mov      edi, edx
003E94DF  call     0x2e1040  ; -> 002E1040 fn
003E94E4  mov      rcx, qword ptr [rax]
003E94E7  test     rcx, rcx
003E94EA  je       0x3e951a  ; -> 003E951A
003E94EC  movzx    eax, word ptr [rax + 0x54]
003E94F0  cmp      edi, eax
003E94F2  jge      0x3e951a  ; -> 003E951A
003E94F4  movd     xmm0, dword ptr [rbx + 8]
003E94F9  mov      r8, rbx
003E94FC  mov      r9d, dword ptr [rbx + 4]
003E9500  mov      edx, edi
003E9502  cvtdq2ps xmm0, xmm0
003E9505  divss    xmm0, dword ptr [rip + 0x1a14baf]  ; -> 01DFE0BC [f32 1]
003E950D  cvttss2si eax, xmm0
003E9511  mov      dword ptr [rsp + 0x20], eax
003E9515  call     0x2a2650  ; -> 002A2650 fn
003E951A  mov      rbx, qword ptr [rsp + 0x40]
003E951F  add      rsp, 0x30
003E9523  pop      rdi
003E9524  ret      
```
