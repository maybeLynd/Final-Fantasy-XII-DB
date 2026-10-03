# F homing pack (FABLE): `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`

Generated 2026-10-03 06:31 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 0063BBC0 (49 B, extent 0063BBC0-0063BBF1)

Documented callee on this page: `00630340`

```
0063BBC0  sub      rsp, 0x28
0063BBC4  mov      rcx, qword ptr [rcx + 0x30]
0063BBC8  mov      rax, qword ptr [rcx]
0063BBCB  call     qword ptr [rax + 8]
0063BBCE  test     rax, rax
0063BBD1  je       0x63bbe8  ; -> 0063BBE8
0063BBD3  test     byte ptr [rax + 0xfc], 1
0063BBDA  je       0x63bbe8  ; -> 0063BBE8
0063BBDC  lea      rax, [rip + 0x26bc99d]  ; -> 02CF8580
0063BBE3  add      rsp, 0x28
0063BBE7  ret      
0063BBE8  add      rsp, 0x28
0063BBEC  jmp      0x630340  ; -> 00630340 fn
```

## 006ABEC0 (201 B, extent 006ABEC0-006ABF89)

Documented callee on this page: `005A7B50`

```
006ABEC0  push     rbx
006ABEC2  sub      rsp, 0x20
006ABEC6  mov      rbx, qword ptr [rcx]
006ABEC9  test     rbx, rbx
006ABECC  je       0x6abf2c  ; -> 006ABF2C
006ABECE  mov      r8, qword ptr [rcx + 8]
006ABED2  mov      rax, r8
006ABED5  test     r8, r8
006ABED8  je       0x6abeef  ; -> 006ABEEF
006ABEDA  lea      rcx, [rip + 0x27945cf]  ; -> 02E404B0
006ABEE1  cmp      rax, rcx
006ABEE4  je       0x6abf27  ; -> 006ABF27
006ABEE6  mov      rax, qword ptr [rax + 0x78]
006ABEEA  test     rax, rax
006ABEED  jne      0x6abee1  ; -> 006ABEE1
006ABEEF  xor      ecx, ecx
006ABEF1  test     rcx, rcx
006ABEF4  jne      0x6abf1d  ; -> 006ABF1D
006ABEF6  lea      rdx, [rip + 0x69e55b]  ; -> 00D4A458 [str "getLocalToWorldMatrix"]
006ABEFD  mov      rcx, r8
006ABF00  call     0x5a7b50  ; -> 005A7B50 fn
006ABF05  test     rax, rax
006ABF08  je       0x6abf2c  ; -> 006ABF2C
006ABF0A  mov      rdx, rbx
006ABF0D  mov      rcx, rax
006ABF10  call     0x6ab600  ; -> 006AB600 fn
006ABF15  test     rax, rax
006ABF18  je       0x6abf2c  ; -> 006ABF2C
006ABF1A  mov      rcx, rax
006ABF1D  add      rsp, 0x20
006ABF21  pop      rbx
006ABF22  jmp      0x6abf40  ; -> 006ABF40
006ABF27  mov      rcx, rbx
006ABF2A  jmp      0x6abef1  ; -> 006ABEF1
006ABF2C  xor      eax, eax
006ABF2E  add      rsp, 0x20
006ABF32  pop      rbx
006ABF33  ret      
006ABF34  int3     
006ABF35  int3     
006ABF36  int3     
006ABF37  int3     
006ABF38  int3     
006ABF39  int3     
006ABF3A  int3     
006ABF3B  int3     
006ABF3C  int3     
006ABF3D  int3     
006ABF3E  int3     
006ABF3F  int3     
006ABF40  mov      rdx, qword ptr [rip + 0x1882c11]  ; -> 01F2EB58 [u64 0x0000000001F2EB40]
006ABF47  lea      r9, [rip + 0x1882bf2]  ; -> 01F2EB40
006ABF4E  xor      r8d, r8d
006ABF51  cmp      rdx, r9
006ABF54  je       0x6abf7a  ; -> 006ABF7A
006ABF56  mov      rax, qword ptr [rdx + 0x18]
006ABF5A  cmp      rax, rcx
006ABF5D  jbe      0x6abf66  ; -> 006ABF66
006ABF5F  mov      eax, 1
006ABF64  jmp      0x6abf6d  ; -> 006ABF6D
006ABF66  jae      0x6abf7d  ; -> 006ABF7D
006ABF68  mov      eax, 0xffffffff
006ABF6D  shr      rax, 0x1f
006ABF71  mov      rdx, qword ptr [rdx + rax*8]
006ABF75  cmp      rdx, r9
006ABF78  jne      0x6abf56  ; -> 006ABF56
006ABF7A  mov      rdx, r8
006ABF7D  test     rdx, rdx
006ABF80  lea      rax, [rdx + 0x20]
006ABF84  cmove    rax, r8
```
