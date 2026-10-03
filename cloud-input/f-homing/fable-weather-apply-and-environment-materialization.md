# F homing pack (FABLE): `03-World-Area-Field/Weather/weather-apply-and-environment-materialization.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 003EBE70 (171 B, extent 003EBE70-003EBF1B)

Documented callee on this page: `0036C660`

```
003EBE70  sub      rsp, 0x28
003EBE74  mov      qword ptr [rip + 0x2772de5], rcx  ; -> 02B5EC60
003EBE7B  test     rcx, rcx
003EBE7E  je       0x3ebf16  ; -> 003EBF16
003EBE84  mov      rcx, qword ptr [rip + 0x2772ddd]  ; -> 02B5EC68
003EBE8B  test     rcx, rcx
003EBE8E  je       0x3ebea0  ; -> 003EBEA0
003EBE90  call     0x3697f0  ; -> 003697F0 fn
003EBE95  mov      qword ptr [rip + 0x2772dc8], 0  ; -> 02B5EC68
003EBEA0  mov      edx, 5
003EBEA5  mov      ecx, edx
003EBEA7  call     0x36c1d0  ; -> 0036C1D0 fn
003EBEAC  mov      ecx, 0x100
003EBEB1  call     0x36a190  ; -> 0036A190 fn
003EBEB6  mov      qword ptr [rip + 0x2772dab], rax  ; -> 02B5EC68
003EBEBD  test     rax, rax
003EBEC0  je       0x3ebed7  ; -> 003EBED7
003EBEC2  mov      r8d, 0x100
003EBEC8  lea      rdx, [rip + 0x925951]  ; -> 00D11820 [str "VOICEWK"]
003EBECF  mov      rcx, rax
003EBED2  call     0x36c660  ; -> 0036C660 fn
003EBED7  call     0x36c140  ; -> 0036C140 fn
003EBEDC  mov      rcx, qword ptr [rip + 0x2772d7d]  ; -> 02B5EC60
003EBEE3  xor      eax, eax
003EBEE5  mov      qword ptr [rip + 0x2772d84], rax  ; -> 02B5EC70
003EBEEC  mov      qword ptr [rip + 0x2772d85], rax  ; -> 02B5EC78
003EBEF3  mov      qword ptr [rip + 0x2772d86], rax  ; -> 02B5EC80
003EBEFA  mov      qword ptr [rip + 0x2772d87], rax  ; -> 02B5EC88
003EBF01  test     rcx, rcx
003EBF04  je       0x3ebf16  ; -> 003EBF16
003EBF06  lea      rdx, [rip + 0x2772d63]  ; -> 02B5EC70
003EBF0D  add      rsp, 0x28
003EBF11  jmp      0x321ea0  ; -> 00321EA0 fn
003EBF16  add      rsp, 0x28
003EBF1A  ret      
```
