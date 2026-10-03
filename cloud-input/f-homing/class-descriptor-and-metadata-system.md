# F homing pack: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`

Generated 2026-10-02 21:16 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 11. No bearing page cites them and no documented function calls them directly.

## 00164100 (119 B, extent 00164100-00164177)

Documented callee on this page: `00632780`

```
00164100  sub      rsp, 0x28
00164104  xor      r8d, r8d
00164107  lea      rdx, [rip + 0x2b94162]  ; -> 02CF8270
0016410E  lea      rcx, [rip + 0x2b9496b]  ; -> 02CF8A80
00164115  call     0x632780  ; -> 00632780 fn
0016411A  mov      eax, dword ptr [rip + 0x2b94a5c]  ; -> 02CF8B7C
00164120  lea      rcx, [rip + 0x2b94cf9]  ; -> 02CF8E20
00164127  mov      qword ptr [rip + 0x2b94a12], rcx  ; -> 02CF8B40
0016412E  or       eax, 2
00164131  lea      rcx, [rip + 0x2b94d08]  ; -> 02CF8E40
00164138  and      eax, 0xfffffffd
0016413B  mov      qword ptr [rip + 0x2b94a06], rcx  ; -> 02CF8B48
00164142  or       eax, 8
00164145  lea      rcx, [rip + 0x2b94d14]  ; -> 02CF8E60
0016414C  mov      dword ptr [rip + 0x2b94a2a], eax  ; -> 02CF8B7C
00164152  mov      qword ptr [rip + 0x2b949f7], rcx  ; -> 02CF8B50
00164159  lea      rcx, [rip + 0xbf2bb0]  ; -> 00D56D10
00164160  mov      qword ptr [rip + 0x2b94919], rcx  ; -> 02CF8A80
00164167  lea      rcx, [rip + 0x74b002]  ; -> 008AF170
0016416E  add      rsp, 0x28
00164172  jmp      0x808b90  ; -> 00808B90 fn
```

## 00212600 (258 B, extent 00212600-00212702)

Documented callee on this page: `00212050`

```
00212600  push     rbp
00212602  sub      rsp, 0x20
00212606  movzx    eax, byte ptr [rcx + 0x28]
0021260A  mov      rbp, rcx
0021260D  test     al, al
0021260F  je       0x2126fa  ; -> 002126FA
00212615  mov      qword ptr [rsp + 0x30], rbx
0021261A  mov      qword ptr [rsp + 0x38], rsi
0021261F  mov      qword ptr [rsp + 0x40], rdi
00212624  lea      rdi, [rcx + 0x58]
00212628  nop      dword ptr [rax + rax]
00212630  lea      rcx, [rbp + 0x30]
00212634  call     0x5cd4f0  ; -> 005CD4F0 fn
00212639  mov      rbx, qword ptr [rdi]
0021263C  lea      rcx, [rbp + 0x30]
00212640  call     0x5cd820  ; -> 005CD820 fn
00212645  cmp      rbx, rdi
00212648  jne      0x212659  ; -> 00212659
0021264A  mov      ecx, 1
0021264F  call     0x5ccb80  ; -> 005CCB80 fn
00212654  jmp      0x2126df  ; -> 002126DF
00212659  lea      rcx, [rbp + 0x30]
0021265D  call     0x5cd4f0  ; -> 005CD4F0 fn
00212662  mov      rax, qword ptr [rdi]
00212665  xor      ecx, ecx
00212667  cmp      rax, rdi
0021266A  je       0x212689  ; -> 00212689
0021266C  nop      dword ptr [rax]
00212670  mov      rax, qword ptr [rax]
00212673  inc      rcx
00212676  cmp      rax, rdi
00212679  jne      0x212670  ; -> 00212670
0021267B  test     ecx, ecx
0021267D  je       0x212689  ; -> 00212689
0021267F  mov      rax, qword ptr [rbp + 0x60]
00212683  mov      rbx, qword ptr [rax + 0x10]
00212687  jmp      0x21268b  ; -> 0021268B
00212689  xor      ebx, ebx
0021268B  lea      rcx, [rbp + 0x30]
0021268F  call     0x5cd820  ; -> 005CD820 fn
00212694  test     rbx, rbx
00212697  je       0x2126df  ; -> 002126DF
00212699  mov      rdx, rbx
0021269C  mov      rcx, rbp
0021269F  call     0x212050  ; -> 00212050 fn
002126A4  lea      rcx, [rbp + 0x30]
002126A8  call     0x5cd4f0  ; -> 005CD4F0 fn
002126AD  mov      rdx, qword ptr [rdi + 8]
002126B1  mov      r8d, 0x18
002126B7  mov      rcx, qword ptr [rdx + 8]
002126BB  mov      rax, qword ptr [rdx]
002126BE  mov      qword ptr [rcx], rax
002126C1  mov      rcx, qword ptr [rdx]
002126C4  mov      rax, qword ptr [rdx + 8]
002126C8  mov      qword ptr [rcx + 8], rax
002126CC  lea      rcx, [rdi + 0x10]
002126D0  mov      rax, qword ptr [rcx]
002126D3  call     qword ptr [rax + 0x18]
002126D6  lea      rcx, [rbp + 0x30]
002126DA  call     0x5cd820  ; -> 005CD820 fn
002126DF  movzx    eax, byte ptr [rbp + 0x28]
002126E3  test     al, al
002126E5  jne      0x212630  ; -> 00212630
002126EB  mov      rdi, qword ptr [rsp + 0x40]
002126F0  mov      rsi, qword ptr [rsp + 0x38]
002126F5  mov      rbx, qword ptr [rsp + 0x30]
002126FA  xor      eax, eax
002126FC  add      rsp, 0x20
00212700  pop      rbp
00212701  ret      
```

## 005D1500 (39 B, extent 005D1500-005D1527)

Documented callee on this page: `00639450`

```
005D1500  sub      rsp, 0x28
005D1504  lea      rcx, [rip + 0x26e86f5]  ; -> 02CB9C00
005D150B  call     0x6388c0  ; -> 006388C0 fn
005D1510  or       dword ptr [rip + 0x26e87e5], 0x20  ; -> 02CB9CFC
005D1517  lea      rcx, [rip + 0x26e86e2]  ; -> 02CB9C00
005D151E  add      rsp, 0x28
005D1522  jmp      0x639450  ; -> 00639450 fn
```

## 005D7060 (39 B, extent 005D7060-005D7087)

Documented callee on this page: `00639450`

```
005D7060  sub      rsp, 0x28
005D7064  lea      rcx, [rip + 0x26e0c35]  ; -> 02CB7CA0
005D706B  call     0x6388c0  ; -> 006388C0 fn
005D7070  or       dword ptr [rip + 0x26e0d25], 0x20  ; -> 02CB7D9C
005D7077  lea      rcx, [rip + 0x26e0c22]  ; -> 02CB7CA0
005D707E  add      rsp, 0x28
005D7082  jmp      0x639450  ; -> 00639450 fn
```

## 0060F2D0 (116 B, extent 0060F2D0-0060F344)

Documented callee on this page: `00639850`

```
0060F2D0  mov      qword ptr [rsp + 8], rbx
0060F2D5  mov      qword ptr [rsp + 0x10], rbp
0060F2DA  mov      qword ptr [rsp + 0x18], rsi
0060F2DF  push     rdi
0060F2E0  sub      rsp, 0x20
0060F2E4  mov      ebx, r8d
0060F2E7  lea      rdi, [rcx + 8]
0060F2EB  mov      rsi, rdx
0060F2EE  mov      rbp, rcx
0060F2F1  call     0x630180  ; -> 00630180 fn
0060F2F6  mov      rcx, rax
0060F2F9  mov      r9, qword ptr [rax]
0060F2FC  call     qword ptr [r9 + 8]
0060F300  cmp      rsi, rdi
0060F303  jne      0x60f31f  ; -> 0060F31F
0060F305  cmp      ebx, 1
0060F308  jne      0x60f31f  ; -> 0060F31F
0060F30A  test     rax, rax
0060F30D  je       0x60f31f  ; -> 0060F31F
0060F30F  mov      r8d, ebx
0060F312  mov      rdx, rdi
0060F315  mov      rcx, rax
0060F318  call     0x639850  ; -> 00639850 fn
0060F31D  jmp      0x60f32d  ; -> 0060F32D
0060F31F  mov      r8d, ebx
0060F322  mov      rdx, rsi
0060F325  mov      rcx, rbp
0060F328  call     0x6c7d00  ; -> 006C7D00 fn
0060F32D  mov      rbx, qword ptr [rsp + 0x30]
0060F332  xor      eax, eax
0060F334  mov      rbp, qword ptr [rsp + 0x38]
0060F339  mov      rsi, qword ptr [rsp + 0x40]
0060F33E  add      rsp, 0x20
0060F342  pop      rdi
0060F343  ret      
```

## 0063AA50 (123 B, extent 0063AA50-0063AACB)

Documented callee on this page: `0063C910`

```
0063AA50  mov      qword ptr [rsp + 8], rbx
0063AA55  mov      qword ptr [rsp + 0x10], rsi
0063AA5A  push     rdi
0063AA5B  sub      rsp, 0x30
0063AA5F  test     byte ptr [r8 + 0xfc], 8
0063AA67  mov      rdi, r8
0063AA6A  mov      rsi, rdx
0063AA6D  je       0x63aa88  ; -> 0063AA88
0063AA6F  mov      r8, qword ptr [r8 + 0x30]
0063AA73  lea      rdx, [rip + 0x71dcd6]  ; -> 00D58750
0063AA7A  mov      ecx, 1
0063AA7F  call     0x5cdaa0  ; -> 005CDAA0 fn
0063AA84  xor      ebx, ebx
0063AA86  jmp      0x63aab1  ; -> 0063AAB1
0063AA88  mov      edx, dword ptr [rdi + 0x38]
0063AA8B  xor      ebx, ebx
0063AA8D  mov      r9, rdi
0063AA90  mov      dword ptr [rsp + 0x20], ebx
0063AA94  lea      r8d, [rbx + 1]
0063AA98  call     0x639510  ; -> 00639510 fn
0063AA9D  test     rax, rax
0063AAA0  je       0x63aab1  ; -> 0063AAB1
0063AAA2  mov      rbx, qword ptr [rax + 0x58]
0063AAA6  mov      rcx, rdi
0063AAA9  mov      rdx, rbx
0063AAAC  call     0x63c910  ; -> 0063C910 fn
0063AAB1  mov      qword ptr [rsi], rbx
0063AAB4  mov      rax, rsi
0063AAB7  mov      rbx, qword ptr [rsp + 0x40]
0063AABC  mov      qword ptr [rsi + 8], rdi
0063AAC0  mov      rsi, qword ptr [rsp + 0x48]
0063AAC5  add      rsp, 0x30
0063AAC9  pop      rdi
0063AACA  ret      
```

## 006777D0 (120 B, extent 006777D0-00677848)

Documented callee on this page: `006372A0`

```
006777D0  sub      rsp, 0x38
006777D4  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006777DD  mov      ecx, dword ptr [rip + 0x2837559]  ; -> 02EAED3C
006777E3  mov      rax, qword ptr gs:[0x58]
006777EC  mov      edx, 4
006777F1  mov      rcx, qword ptr [rax + rcx*8]
006777F5  mov      eax, dword ptr [rdx + rcx]
006777F8  cmp      dword ptr [rip + 0x26c74fa], eax  ; -> 02D3ECF8
006777FE  jle      0x67783c  ; -> 0067783C
00677800  lea      rcx, [rip + 0x26c74f1]  ; -> 02D3ECF8
00677807  call     0x8092fc  ; -> 008092FC fn
0067780C  cmp      dword ptr [rip + 0x26c74e5], -1  ; -> 02D3ECF8
00677813  jne      0x67783c  ; -> 0067783C
00677815  call     0x6372a0  ; -> 006372A0 fn
0067781A  or       rax, 1
0067781E  mov      qword ptr [rip + 0x26c74c3], rax  ; -> 02D3ECE8
00677825  mov      qword ptr [rip + 0x26c74c0], 0  ; -> 02D3ECF0
00677830  lea      rcx, [rip + 0x26c74c1]  ; -> 02D3ECF8
00677837  call     0x80929c  ; -> 0080929C fn
0067783C  lea      rax, [rip + 0x26c74a5]  ; -> 02D3ECE8
00677843  add      rsp, 0x38
00677847  ret      
```

## 0068D700 (80 B, extent 0068D700-0068D750)

Documented callee on this page: `006372A0`

```
0068D700  mov      qword ptr [rsp + 0x10], rdx
0068D705  push     rbx
0068D706  sub      rsp, 0x30
0068D70A  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0068D713  mov      rbx, rdx
0068D716  mov      qword ptr [rsp + 0x50], rdx
0068D71B  test     rdx, rdx
0068D71E  je       0x68d748  ; -> 0068D748
0068D720  mov      qword ptr [rdx], 0
0068D727  call     0x6372a0  ; -> 006372A0 fn
0068D72C  mov      qword ptr [rbx + 8], rax
0068D730  mov      qword ptr [rbx + 0x10], 0
0068D738  call     0x6372a0  ; -> 006372A0 fn
0068D73D  mov      qword ptr [rbx + 0x18], rax
0068D741  mov      dword ptr [rbx + 0x20], 0
0068D748  mov      al, 1
0068D74A  add      rsp, 0x30
0068D74E  pop      rbx
0068D74F  ret      
```

## 006AF4F0 (112 B, extent 006AF4F0-006AF560)

Documented callee on this page: `006372A0`

```
006AF4F0  push     rbx
006AF4F2  sub      rsp, 0x20
006AF4F6  mov      rbx, rdx
006AF4F9  test     r8, r8
006AF4FC  je       0x6af537  ; -> 006AF537
006AF4FE  mov      r9, qword ptr [rcx + 0x20]
006AF502  mov      ecx, dword ptr [rcx + 0x18]
006AF505  btr      ecx, 0x1f
006AF509  shl      rcx, 4
006AF50D  add      rcx, r9
006AF510  cmp      r9, rcx
006AF513  jae      0x6af537  ; -> 006AF537
006AF515  mov      rax, qword ptr [r9 + 8]
006AF519  test     rax, rax
006AF51C  je       0x6af52e  ; -> 006AF52E
006AF51E  nop      
006AF520  cmp      rax, r8
006AF523  je       0x6af550  ; -> 006AF550
006AF525  mov      rax, qword ptr [rax + 0x78]
006AF529  test     rax, rax
006AF52C  jne      0x6af520  ; -> 006AF520
006AF52E  add      r9, 0x10
006AF532  cmp      r9, rcx
006AF535  jb       0x6af515  ; -> 006AF515
006AF537  mov      qword ptr [rdx], 0
006AF53E  call     0x6372a0  ; -> 006372A0 fn
006AF543  mov      qword ptr [rbx + 8], rax
006AF547  mov      rax, rbx
006AF54A  add      rsp, 0x20
006AF54E  pop      rbx
006AF54F  ret      
006AF550  movups   xmm0, xmmword ptr [r9]
006AF554  mov      rax, rbx
006AF557  movups   xmmword ptr [rdx], xmm0
006AF55A  add      rsp, 0x20
006AF55E  pop      rbx
006AF55F  ret      
```

## 006CEE50 (79 B, extent 006CEE50-006CEE9F)

Documented callee on this page: `006372B0`

```
006CEE50  push     rdi
006CEE52  sub      rsp, 0x40
006CEE56  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006CEE5F  mov      qword ptr [rsp + 0x50], rbx
006CEE64  mov      rbx, rdx
006CEE67  mov      rdi, rcx
006CEE6A  call     0x6372b0  ; -> 006372B0 fn
006CEE6F  mov      qword ptr [rsp + 0x30], rax
006CEE74  lea      rax, [rip + 0x65e495]  ; -> 00D2D310
006CEE7B  mov      qword ptr [rsp + 0x28], rax
006CEE80  mov      rax, qword ptr [rdi]
006CEE83  lea      r8, [rsp + 0x28]
006CEE88  mov      rdx, rbx
006CEE8B  mov      rcx, rdi
006CEE8E  call     qword ptr [rax + 0x78]
006CEE91  nop      
006CEE92  mov      al, 1
006CEE94  mov      rbx, qword ptr [rsp + 0x50]
006CEE99  add      rsp, 0x40
006CEE9D  pop      rdi
006CEE9E  ret      
```

## 006D9E30 (79 B, extent 006D9E30-006D9E7F)

Documented callee on this page: `006372B0`

```
006D9E30  push     rdi
006D9E32  sub      rsp, 0x40
006D9E36  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006D9E3F  mov      qword ptr [rsp + 0x50], rbx
006D9E44  mov      rbx, rdx
006D9E47  mov      rdi, rcx
006D9E4A  call     0x6372b0  ; -> 006372B0 fn
006D9E4F  mov      qword ptr [rsp + 0x30], rax
006D9E54  lea      rax, [rip + 0x6534b5]  ; -> 00D2D310
006D9E5B  mov      qword ptr [rsp + 0x28], rax
006D9E60  mov      rax, qword ptr [rdi]
006D9E63  lea      r8, [rsp + 0x28]
006D9E68  mov      rdx, rbx
006D9E6B  mov      rcx, rdi
006D9E6E  call     qword ptr [rax + 0x78]
006D9E71  nop      
006D9E72  mov      al, 1
006D9E74  mov      rbx, qword ptr [rsp + 0x50]
006D9E79  add      rsp, 0x40
006D9E7D  pop      rdi
006D9E7E  ret      
```
