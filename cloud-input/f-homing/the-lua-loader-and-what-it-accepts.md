# F homing pack: `23-Third-Party-Libraries/Lua-Core/the-lua-loader-and-what-it-accepts.md`

Generated 2026-10-02 22:29 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 0063C450 (68 B, extent 0063C450-0063C494)

Documented callee on this page: `008113D0`

```
0063C450  mov      qword ptr [rsp + 8], rbx
0063C455  mov      qword ptr [rsp + 0x10], rsi
0063C45A  push     rdi
0063C45B  sub      rsp, 0x20
0063C45F  mov      rdi, rdx
0063C462  mov      rsi, r8
0063C465  mov      rcx, rdi
0063C468  or       edx, 0xffffffff
0063C46B  call     0x8113d0  ; -> 008113D0 fn
0063C470  test     eax, eax
0063C472  mov      edx, 0xfffffffe
0063C477  mov      rcx, rdi
0063C47A  setne    bl
0063C47D  call     0x811130  ; -> 00811130 fn
0063C482  mov      byte ptr [rsi], bl
0063C484  mov      rbx, qword ptr [rsp + 0x30]
0063C489  mov      rsi, qword ptr [rsp + 0x38]
0063C48E  add      rsp, 0x20
0063C492  pop      rdi
0063C493  ret      
```
