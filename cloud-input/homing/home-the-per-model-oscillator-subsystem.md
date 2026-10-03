# Homing pack: `17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-per-model-oscillator-subsystem.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002E4150 (377 B, extent 002E4150-002E42C9)

Entered from (direct sites whose caller this page cites): `00267D40` + 0x3C (call; `00267D40` is cited on this page)
Other direct sites: `0034E6D0` + 0x35 (jmp)

Host context: "03777A0' / '003777B0'); - **a one-deep save and restore** - '002EAB40' saves the current preset, direction and tilt (through '0040AAB0') and   sets calm; '002EAA60' restores them. Both are driven by '00267D40', a requester mask in '02099DA6' that the verbs   'denybonephysicalall' ('0x3D5', handler '0034C550', bit 0) and 'denybonephysicalall_3ea' ('0x3EA') set and clear:   while any requester denies bone physics, the wind is calm.  The t"

```
002E4150  mov      qword ptr [rsp + 8], rbx
002E4155  mov      qword ptr [rsp + 0x10], rbp
002E415A  mov      qword ptr [rsp + 0x18], rsi
002E415F  mov      qword ptr [rsp + 0x20], rdi
002E4164  push     r12
002E4166  push     r14
002E4168  push     r15
002E416A  sub      rsp, 0x20
002E416E  mov      r15d, edx
002E4171  mov      r12d, ecx
002E4174  xor      r14d, r14d
002E4177  mov      ecx, r14d
002E417A  call     0x263ff0  ; -> 00263FF0 fn
002E417F  mov      rbp, rax
002E4182  test     byte ptr [rax + 0x10], 1
002E4186  je       0x2e429d  ; -> 002E429D
002E418C  movzx    edi, word ptr [rax + 0x1de]
002E4193  movzx    esi, word ptr [rax + 0x1d6]
002E419A  add      esi, edi
002E419C  test     r12d, r12d
002E419F  je       0x2e425a  ; -> 002E425A
002E41A5  cmp      r12d, 1
002E41A9  jne      0x2e429d  ; -> 002E429D
002E41AF  cmp      edi, esi
002E41B1  jae      0x2e429d  ; -> 002E429D
002E41B7  nop      word ptr [rax + rax]
002E41C0  mov      edx, edi
002E41C2  mov      rcx, rbp
002E41C5  call     0x358940  ; -> 00358940 fn
002E41CA  mov      rdx, rax
002E41CD  test     r14d, r14d
002E41D0  jne      0x2e41e5  ; -> 002E41E5
002E41D2  movzx    ecx, byte ptr [rax + 3]
002E41D6  xor      r8d, r8d
002E41D9  and      cl, 0x1f
002E41DC  cmp      cl, 6
002E41DF  setne    r8b
002E41E3  jmp      0x2e41eb  ; -> 002E41EB
002E41E5  mov      r8d, 1
002E41EB  xor      eax, eax
002E41ED  test     r15d, r15d
002E41F0  cmovne   eax, r8d
002E41F4  test     eax, eax
002E41F6  je       0x2e424e  ; -> 002E424E
002E41F8  cmp      byte ptr [rdx + 0x18], 1
002E41FC  je       0x2e424e  ; -> 002E424E
002E41FE  mov      rax, qword ptr [rdx + 0xc0]
002E4205  test     rax, rax
002E4208  je       0x2e424e  ; -> 002E424E
002E420A  cmp      dword ptr [rax], -1
002E420D  je       0x2e424e  ; -> 002E424E
002E420F  movzx    ecx, word ptr [rax]
002E4212  cmp      cx, -1
002E4216  jne      0x2e421c  ; -> 002E421C
002E4218  xor      eax, eax
002E421A  jmp      0x2e4246  ; -> 002E4246
002E421C  movsx    rax, cx
002E4220  imul     rcx, rax, 0x740
002E4227  add      rcx, qword ptr [rip + 0x1fe2cfa]  ; -> 022C6F28
002E422E  jne      0x2e4234  ; -> 002E4234
002E4230  xor      eax, eax
002E4232  jmp      0x2e4246  ; -> 002E4246
002E4234  cmp      dword ptr [rcx + 0x284], 0
002E423B  jne      0x2e4241  ; -> 002E4241
002E423D  xor      eax, eax
002E423F  jmp      0x2e4246  ; -> 002E4246
002E4241  call     0x3e6da0  ; -> 003E6DA0 fn
002E4246  mov      rcx, rax
002E4249  call     0x3e0860  ; -> 003E0860 fn
002E424E  inc      edi
002E4250  cmp      edi, esi
002E4252  jl       0x2e41c0  ; -> 002E41C0
002E4258  jmp      0x2e429d  ; -> 002E429D
002E425A  cmp      edi, esi
002E425C  jae      0x2e429d  ; -> 002E429D
002E425E  nop      
002E4260  mov      edx, edi
002E4262  mov      rcx, rbp
002E4265  call     0x358940  ; -> 00358940 fn
002E426A  test     rax, rax
002E426D  je       0x2e4297  ; -> 002E4297
002E426F  mov      rbx, qword ptr [rax + 0xc0]
002E4276  test     rbx, rbx
002E4279  je       0x2e4297  ; -> 002E4297
002E427B  cmp      dword ptr [rbx], -1
002E427E  je       0x2e4297  ; -> 002E4297
002E4280  test     r15d, r15d
002E4283  je       0x2e4293  ; -> 002E4293
002E4285  cmp      byte ptr [rbx + 0x11], 0x80
002E4289  jb       0x2e4293  ; -> 002E4293
002E428B  movzx    ecx, word ptr [rbx]
002E428E  call     0x426520  ; -> 00426520 fn
002E4293  and      byte ptr [rbx + 0x11], 0x7f
002E4297  inc      edi
002E4299  cmp      edi, esi
002E429B  jl       0x2e4260  ; -> 002E4260
002E429D  inc      r14d
002E42A0  cmp      r14d, 3
002E42A4  jl       0x2e4177  ; -> 002E4177
002E42AA  mov      rbx, qword ptr [rsp + 0x40]
002E42AF  mov      rbp, qword ptr [rsp + 0x48]
002E42B4  mov      rsi, qword ptr [rsp + 0x50]
002E42B9  mov      rdi, qword ptr [rsp + 0x58]
002E42BE  add      rsp, 0x20
002E42C2  pop      r15
002E42C4  pop      r14
002E42C6  pop      r12
002E42C8  ret      
```
