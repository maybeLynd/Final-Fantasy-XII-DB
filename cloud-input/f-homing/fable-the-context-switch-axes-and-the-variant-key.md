# F homing pack (FABLE): `22-Middleware-PhyreEngine/Shader-Variant-Selection/the-context-switch-axes-and-the-variant-key.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 6. No bearing page cites them and no documented function calls them directly.

## 001670A0 (66 B, extent 001670A0-001670E2)

Documented callee on this page: `006B8D20`

```
001670A0  sub      rsp, 0x28
001670A4  lea      rcx, [rip + 0x1dc7b45]  ; -> 01F2EBF0
001670AB  call     0x6b8d20  ; -> 006B8D20 fn
001670B0  test     eax, eax
001670B2  jne      0x1670c4  ; -> 001670C4
001670B4  inc      dword ptr [rip + 0x2ceb226]  ; -> 02E522E0
001670BA  mov      dword ptr [rip + 0x1dc7b4c], 1  ; -> 01F2EC10 [u32 0x00000000]
001670C4  lea      rax, [rip + 0xc19e2d]  ; -> 00D80EF8
001670CB  lea      rcx, [rip + 0x74e7de]  ; -> 008B58B0
001670D2  mov      qword ptr [rip + 0x1dc7b17], rax  ; -> 01F2EBF0 [u64 0x0000000000D80EA8]
001670D9  add      rsp, 0x28
001670DD  jmp      0x808b90  ; -> 00808B90 fn
```

## 001670F0 (67 B, extent 001670F0-00167133)

Documented callee on this page: `006B8D20`

```
001670F0  sub      rsp, 0x28
001670F4  lea      rcx, [rip + 0x1dc7acd]  ; -> 01F2EBC8
001670FB  call     0x6b8d20  ; -> 006B8D20 fn
00167100  test     eax, eax
00167102  jne      0x167115  ; -> 00167115
00167104  add      dword ptr [rip + 0x2ceb1d5], 3  ; -> 02E522E0
0016710B  mov      dword ptr [rip + 0x1dc7ad3], 3  ; -> 01F2EBE8 [u32 0x00000000]
00167115  lea      rax, [rip + 0xc19db4]  ; -> 00D80ED0
0016711C  lea      rcx, [rip + 0x74e80d]  ; -> 008B5930
00167123  mov      qword ptr [rip + 0x1dc7a9e], rax  ; -> 01F2EBC8 [u64 0x0000000000D80EA8]
0016712A  add      rsp, 0x28
0016712E  jmp      0x808b90  ; -> 00808B90 fn
```

## 00167140 (73 B, extent 00167140-00167189)

Documented callee on this page: `006B8D20`

```
00167140  sub      rsp, 0x28
00167144  lea      rcx, [rip + 0x1dc7b95]  ; -> 01F2ECE0
0016714B  call     0x6b8d20  ; -> 006B8D20 fn
00167150  test     eax, eax
00167152  jne      0x167164  ; -> 00167164
00167154  inc      dword ptr [rip + 0x2ceb186]  ; -> 02E522E0
0016715A  mov      dword ptr [rip + 0x1dc7b9c], 1  ; -> 01F2ED00 [u32 0x00000000]
00167164  lea      rax, [rip + 0xc19e7d]  ; -> 00D80FE8
0016716B  mov      byte ptr [rip + 0x1dc7b92], 0  ; -> 01F2ED04 [u8 0x01]
00167172  lea      rcx, [rip + 0x74e837]  ; -> 008B59B0
00167179  mov      qword ptr [rip + 0x1dc7b60], rax  ; -> 01F2ECE0 [u64 0x0000000000D80EA8]
00167180  add      rsp, 0x28
00167184  jmp      0x808b90  ; -> 00808B90 fn
```

## 00167190 (66 B, extent 00167190-001671D2)

Documented callee on this page: `006B8D20`

```
00167190  sub      rsp, 0x28
00167194  lea      rcx, [rip + 0x1dc7af5]  ; -> 01F2EC90
0016719B  call     0x6b8d20  ; -> 006B8D20 fn
001671A0  test     eax, eax
001671A2  jne      0x1671b4  ; -> 001671B4
001671A4  inc      dword ptr [rip + 0x2ceb136]  ; -> 02E522E0
001671AA  mov      dword ptr [rip + 0x1dc7afc], 1  ; -> 01F2ECB0 [u32 0x00000000]
001671B4  lea      rax, [rip + 0xc19ddd]  ; -> 00D80F98
001671BB  lea      rcx, [rip + 0x74e86e]  ; -> 008B5A30
001671C2  mov      qword ptr [rip + 0x1dc7ac7], rax  ; -> 01F2EC90 [u64 0x0000000000D80EA8]
001671C9  add      rsp, 0x28
001671CD  jmp      0x808b90  ; -> 00808B90 fn
```

## 001671E0 (66 B, extent 001671E0-00167222)

Documented callee on this page: `006B8D20`

```
001671E0  sub      rsp, 0x28
001671E4  lea      rcx, [rip + 0x1dc7a55]  ; -> 01F2EC40
001671EB  call     0x6b8d20  ; -> 006B8D20 fn
001671F0  test     eax, eax
001671F2  jne      0x167204  ; -> 00167204
001671F4  inc      dword ptr [rip + 0x2ceb0e6]  ; -> 02E522E0
001671FA  mov      dword ptr [rip + 0x1dc7a5c], 1  ; -> 01F2EC60 [u32 0x00000000]
00167204  lea      rax, [rip + 0xc19d3d]  ; -> 00D80F48
0016720B  lea      rcx, [rip + 0x74e89e]  ; -> 008B5AB0
00167212  mov      qword ptr [rip + 0x1dc7a27], rax  ; -> 01F2EC40 [u64 0x0000000000D80EA8]
00167219  add      rsp, 0x28
0016721D  jmp      0x808b90  ; -> 00808B90 fn
```

## 00167230 (66 B, extent 00167230-00167272)

Documented callee on this page: `006B8D20`

```
00167230  sub      rsp, 0x28
00167234  lea      rcx, [rip + 0x1dc7a2d]  ; -> 01F2EC68
0016723B  call     0x6b8d20  ; -> 006B8D20 fn
00167240  test     eax, eax
00167242  jne      0x167254  ; -> 00167254
00167244  inc      dword ptr [rip + 0x2ceb096]  ; -> 02E522E0
0016724A  mov      dword ptr [rip + 0x1dc7a34], 1  ; -> 01F2EC88 [u32 0x00000000]
00167254  lea      rax, [rip + 0xc19d15]  ; -> 00D80F70
0016725B  lea      rcx, [rip + 0x74e8ce]  ; -> 008B5B30
00167262  mov      qword ptr [rip + 0x1dc79ff], rax  ; -> 01F2EC68 [u64 0x0000000000D80EA8]
00167269  add      rsp, 0x28
0016726D  jmp      0x808b90  ; -> 00808B90 fn
```
