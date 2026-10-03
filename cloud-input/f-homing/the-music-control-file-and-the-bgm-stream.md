# F homing pack: `18-Audio/the-music-control-file-and-the-bgm-stream.md`

Generated 2026-10-02 22:03 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 00224890 (111 B, extent 00224890-002248FF)

Documented callee on this page: `00221ED0`

```
00224890  push     rdi
00224892  sub      rsp, 0x20
00224896  mov      rdi, r8
00224899  test     edx, edx
0022489B  je       0x2248ec  ; -> 002248EC
0022489D  mov      qword ptr [rsp + 0x30], rbx
002248A2  call     0x221ed0  ; -> 00221ED0 fn
002248A7  mov      rbx, rax
002248AA  test     rax, rax
002248AD  je       0x2248df  ; -> 002248DF
002248AF  mov      rcx, rax
002248B2  call     0x225680  ; -> 00225680 fn
002248B7  test     eax, eax
002248B9  je       0x2248df  ; -> 002248DF
002248BB  movss    xmm3, dword ptr [rdi + 8]
002248C0  lea      rcx, [rbx + 8]
002248C4  movss    xmm2, dword ptr [rdi + 4]
002248C9  movss    xmm1, dword ptr [rdi]
002248CD  call     0x7a77f0  ; -> 007A77F0 fn
002248D2  mov      rbx, qword ptr [rsp + 0x30]
002248D7  mov      al, 1
002248D9  add      rsp, 0x20
002248DD  pop      rdi
002248DE  ret      
002248DF  xor      al, al
002248E1  mov      rbx, qword ptr [rsp + 0x30]
002248E6  add      rsp, 0x20
002248EA  pop      rdi
002248EB  ret      
002248EC  mov      dword ptr [0], 0
002248F7  mov      al, 1
002248F9  add      rsp, 0x20
002248FD  pop      rdi
002248FE  ret      
```

## 0050CEC0 (43 B, extent 0050CEC0-0050CEEB)

Documented callee on this page: `0035E810`

```
0050CEC0  sub      rsp, 0x28
0050CEC4  call     0x35e810  ; -> 0035E810 fn
0050CEC9  mov      rdx, rax
0050CECC  lea      rcx, [rip + 0x815a95]  ; -> 00D22968
0050CED3  call     0x17d280  ; -> 0017D280 fn
0050CED8  mov      ecx, 1
0050CEDD  call     0x16d6a0  ; -> 0016D6A0 fn
0050CEE2  add      rsp, 0x28
0050CEE6  jmp      0x16d6a0  ; -> 0016D6A0 fn
```
