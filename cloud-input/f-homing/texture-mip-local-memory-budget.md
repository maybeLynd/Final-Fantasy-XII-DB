# F homing pack: `17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md`

Generated 2026-10-02 21:56 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 3. No bearing page cites them and no documented function calls them directly.

## 008641B0 (92 B, extent 008641B0-0086420C)

Documented callee on this page: `002D7FA0`

```
008641B0  push     rbx
008641B2  sub      rsp, 0x20
008641B6  mov      eax, dword ptr [rcx + 0x50]
008641B9  mov      rbx, rcx
008641BC  and      eax, 0x3fff
008641C1  cmp      eax, 0xe00
008641C6  jne      0x8641d8  ; -> 008641D8
008641C8  xor      eax, eax
008641CA  cmp      dword ptr [rip + 0x265fcfc], eax  ; -> 02EC3ECC
008641D0  setne    al
008641D3  add      eax, 0xdff
008641D8  movzx    ecx, ax
008641DB  call     0x2d7fa0  ; -> 002D7FA0 fn
008641E0  mov      rcx, qword ptr [rax]
008641E3  mov      qword ptr [rbx + 0x20], rcx
008641E7  mov      rcx, qword ptr [rbx + 0x50]
008641EB  call     0x2d7ee0  ; -> 002D7EE0 fn
008641F0  mov      rcx, qword ptr [rax]
008641F3  mov      qword ptr [rbx + 0x28], rcx
008641F7  mov      rcx, qword ptr [rbx + 0x50]
008641FB  call     0x2d7ee0  ; -> 002D7EE0 fn
00864200  mov      ecx, dword ptr [rax + 8]
00864203  mov      dword ptr [rbx + 0x30], ecx
00864206  add      rsp, 0x20
0086420A  pop      rbx
0086420B  ret      
```

## 00864750 (110 B, extent 00864750-008647BE)

Documented callee on this page: `002D7FA0`

```
00864750  push     rbx
00864752  sub      rsp, 0x20
00864756  mov      eax, dword ptr [rcx + 0xc8]
0086475C  mov      rbx, rcx
0086475F  and      eax, 0x3fff
00864764  cmp      eax, 0xe00
00864769  jne      0x86477b  ; -> 0086477B
0086476B  xor      eax, eax
0086476D  cmp      dword ptr [rip + 0x265f759], eax  ; -> 02EC3ECC
00864773  setne    al
00864776  add      eax, 0xdff
0086477B  movzx    ecx, ax
0086477E  call     0x2d7fa0  ; -> 002D7FA0 fn
00864783  mov      rcx, qword ptr [rax]
00864786  mov      qword ptr [rbx + 0xa0], rcx
0086478D  mov      rcx, qword ptr [rbx + 0xc8]
00864794  call     0x2d7ee0  ; -> 002D7EE0 fn
00864799  mov      rcx, qword ptr [rax]
0086479C  mov      qword ptr [rbx + 0xa8], rcx
008647A3  mov      rcx, qword ptr [rbx + 0xc8]
008647AA  call     0x2d7ee0  ; -> 002D7EE0 fn
008647AF  mov      ecx, dword ptr [rax + 8]
008647B2  mov      dword ptr [rbx + 0xb0], ecx
008647B8  add      rsp, 0x20
008647BC  pop      rbx
008647BD  ret      
```

## 00864CA0 (110 B, extent 00864CA0-00864D0E)

Documented callee on this page: `002D7FA0`

```
00864CA0  push     rbx
00864CA2  sub      rsp, 0x20
00864CA6  mov      eax, dword ptr [rcx + 0xf8]
00864CAC  mov      rbx, rcx
00864CAF  and      eax, 0x3fff
00864CB4  cmp      eax, 0xe00
00864CB9  jne      0x864ccb  ; -> 00864CCB
00864CBB  xor      eax, eax
00864CBD  cmp      dword ptr [rip + 0x265f209], eax  ; -> 02EC3ECC
00864CC3  setne    al
00864CC6  add      eax, 0xdff
00864CCB  movzx    ecx, ax
00864CCE  call     0x2d7fa0  ; -> 002D7FA0 fn
00864CD3  mov      rcx, qword ptr [rax]
00864CD6  mov      qword ptr [rbx + 0xd0], rcx
00864CDD  mov      rcx, qword ptr [rbx + 0xf8]
00864CE4  call     0x2d7ee0  ; -> 002D7EE0 fn
00864CE9  mov      rcx, qword ptr [rax]
00864CEC  mov      qword ptr [rbx + 0xd8], rcx
00864CF3  mov      rcx, qword ptr [rbx + 0xf8]
00864CFA  call     0x2d7ee0  ; -> 002D7EE0 fn
00864CFF  mov      ecx, dword ptr [rax + 8]
00864D02  mov      dword ptr [rbx + 0xe0], ecx
00864D08  add      rsp, 0x20
00864D0C  pop      rbx
00864D0D  ret      
```
