# Homing pack: `15-Input/how-a-gamepad-becomes-a-controller-object.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-how-a-gamepad-becomes-a-controller-object.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00797460 (547 B, extent 00797460-00797683)

Entered from (direct sites whose caller this page cites): `00796230` + 0x3C (call; `00796230` is cited on this page); `00798A40` + 0x28 (call; `00798A40` is cited on this page)
Other direct sites: none

Host context: "r:Input evidence_tier: 1 verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: the DirectInput initialiser 00797910, the two enumeration callbacks 00796230 and 00798A40, the per-device     body 00797690, the controller base constructor 00792940 and its three derived constructors 00792CB0, 00792AB0 and     00792B70 disassembled from the authority image and read whole, 2026-09-19; the t" / "nce_tier: 1 verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: the DirectInput initialiser 00797910, the two enumeration callbacks 00796230 and 00798A40, the per-device     body 00797690, the controller base constructor 00792940 and its three derived constructors 00792CB0, 00792AB0 and     00792B70 disassembled from the authority image and read whole, 2026-09-19; the three log stri"

```
00797460  push     rdi
00797462  sub      rsp, 0x30
00797466  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0079746F  mov      qword ptr [rsp + 0x50], rbx
00797474  mov      r10, rcx
00797477  xor      ebx, ebx
00797479  mov      r9, qword ptr [rip + 0x270e438]  ; -> 02EA58B8
00797480  test     r9, r9
00797483  je       0x7975d6  ; -> 007975D6
00797489  lea      r8, [r9 + 0x30]
0079748D  cmp      qword ptr [r8 + 0x10], r9
00797491  jne      0x7974b4  ; -> 007974B4
00797493  mov      rdx, qword ptr [r8]
00797496  mov      rax, qword ptr [r8 + 8]
0079749A  mov      qword ptr [rdx + 8], rax
0079749E  mov      qword ptr [rax], rdx
007974A1  mov      qword ptr [r8], r8
007974A4  mov      qword ptr [r8 + 8], r8
007974A8  mov      qword ptr [r8 + 0x10], rbx
007974AC  mov      qword ptr [r8 + 0x38], rbx
007974B0  mov      qword ptr [r8 + 0x40], rbx
007974B4  lea      rdx, [r8 + 0x48]
007974B8  cmp      qword ptr [rdx + 0x10], r9
007974BC  jne      0x7974df  ; -> 007974DF
007974BE  mov      rcx, qword ptr [rdx]
007974C1  mov      rax, qword ptr [rdx + 8]
007974C5  mov      qword ptr [rcx + 8], rax
007974C9  mov      qword ptr [rax], rcx
007974CC  mov      qword ptr [rdx], rdx
007974CF  mov      qword ptr [rdx + 8], rdx
007974D3  mov      qword ptr [rdx + 0x10], rbx
007974D7  mov      qword ptr [rdx + 0x38], rbx
007974DB  mov      qword ptr [rdx + 0x40], rbx
007974DF  lea      rdx, [r8 + 0x90]
007974E6  cmp      qword ptr [rdx + 0x10], r9
007974EA  jne      0x79750d  ; -> 0079750D
007974EC  mov      rcx, qword ptr [rdx]
007974EF  mov      rax, qword ptr [rdx + 8]
007974F3  mov      qword ptr [rcx + 8], rax
007974F7  mov      qword ptr [rax], rcx
007974FA  mov      qword ptr [rdx], rdx
007974FD  mov      qword ptr [rdx + 8], rdx
00797501  mov      qword ptr [rdx + 0x10], rbx
00797505  mov      qword ptr [rdx + 0x38], rbx
00797509  mov      qword ptr [rdx + 0x40], rbx
0079750D  lea      rdx, [r8 + 0xd8]
00797514  cmp      qword ptr [rdx + 0x10], r9
00797518  jne      0x79753b  ; -> 0079753B
0079751A  mov      rcx, qword ptr [rdx]
0079751D  mov      rax, qword ptr [rdx + 8]
00797521  mov      qword ptr [rcx + 8], rax
00797525  mov      qword ptr [rax], rcx
00797528  mov      qword ptr [rdx], rdx
0079752B  mov      qword ptr [rdx + 8], rdx
0079752F  mov      qword ptr [rdx + 0x10], rbx
00797533  mov      qword ptr [rdx + 0x38], rbx
00797537  mov      qword ptr [rdx + 0x40], rbx
0079753B  lea      rdx, [r8 + 0x120]
00797542  cmp      qword ptr [rdx + 0x10], r9
00797546  jne      0x797569  ; -> 00797569
00797548  mov      rcx, qword ptr [rdx]
0079754B  mov      rax, qword ptr [rdx + 8]
0079754F  mov      qword ptr [rcx + 8], rax
00797553  mov      qword ptr [rax], rcx
00797556  mov      qword ptr [rdx], rdx
00797559  mov      qword ptr [rdx + 8], rdx
0079755D  mov      qword ptr [rdx + 0x10], rbx
00797561  mov      qword ptr [rdx + 0x38], rbx
00797565  mov      qword ptr [rdx + 0x40], rbx
00797569  add      r8, 0x168
00797570  cmp      qword ptr [r8 + 0x10], r9
00797574  jne      0x797597  ; -> 00797597
00797576  mov      rcx, qword ptr [r8]
00797579  mov      rax, qword ptr [r8 + 8]
0079757D  mov      qword ptr [rcx + 8], rax
00797581  mov      qword ptr [rax], rcx
00797584  mov      qword ptr [r8], r8
00797587  mov      qword ptr [r8 + 8], r8
0079758B  mov      qword ptr [r8 + 0x10], rbx
0079758F  mov      qword ptr [r8 + 0x38], rbx
00797593  mov      qword ptr [r8 + 0x40], rbx
00797597  lea      rdx, [r9 + 8]
0079759B  mov      rcx, qword ptr [rdx]
0079759E  mov      rax, qword ptr [rdx + 8]
007975A2  mov      qword ptr [rcx + 8], rax
007975A6  mov      qword ptr [rax], rcx
007975A9  mov      qword ptr [rdx], rdx
007975AC  mov      qword ptr [rdx + 8], rdx
007975B0  mov      rax, qword ptr [rip + 0x17a8c49]  ; -> 01F40200 [u64 0x0000000001F401F8]
007975B7  lea      rcx, [rip + 0x17a8c3a]  ; -> 01F401F8
007975BE  mov      qword ptr [rdx], rcx
007975C1  mov      qword ptr [rdx + 8], rax
007975C5  mov      qword ptr [rax], rdx
007975C8  mov      qword ptr [rip + 0x17a8c31], rdx  ; -> 01F40200 [u64 0x0000000001F401F8]
007975CF  mov      byte ptr [rip + 0x270dda4], 1  ; -> 02EA537A
007975D6  mov      rcx, qword ptr [rip + 0x270dd93]  ; -> 02EA5370
007975DD  mov      rax, qword ptr [rcx]
007975E0  lea      rdx, [r10 + 4]
007975E4  xor      r9d, r9d
007975E7  lea      r8, [rsp + 0x40]
007975EC  call     qword ptr [rax + 0x18]
007975EF  test     eax, eax
007975F1  js       0x797678  ; -> 00797678
007975F7  mov      rcx, qword ptr [rsp + 0x40]
007975FC  mov      rax, qword ptr [rcx]
007975FF  lea      rdx, [rip + 0x152fb2a]  ; -> 01CC7130
00797606  call     qword ptr [rax + 0x58]
00797609  test     eax, eax
0079760B  js       0x797678  ; -> 00797678
0079760D  mov      rcx, qword ptr [rsp + 0x40]
00797612  mov      rax, qword ptr [rcx]
00797615  mov      r8d, 6
0079761B  mov      rdx, qword ptr [rip + 0x270dc26]  ; -> 02EA5248
00797622  call     qword ptr [rax + 0x68]
00797625  cmp      eax, 0x80004001
0079762A  je       0x797678  ; -> 00797678
0079762C  mov      rcx, qword ptr [rsp + 0x40]
00797631  mov      rax, qword ptr [rcx]
00797634  call     qword ptr [rax + 0x38]
00797637  mov      ecx, 0x10
0079763C  call     0x584740  ; -> 00584740 fn
00797641  mov      rdi, rax
00797644  mov      byte ptr [rax], bl
00797646  mov      rcx, qword ptr [rsp + 0x40]
0079764B  mov      qword ptr [rax + 8], rcx
0079764F  mov      ecx, 0x1f8
00797654  call     0x584740  ; -> 00584740 fn
00797659  mov      qword ptr [rsp + 0x48], rax
0079765E  test     rax, rax
00797661  je       0x797671  ; -> 00797671
00797663  mov      rdx, rdi
00797666  mov      rcx, rax
00797669  call     0x792870  ; -> 00792870 fn
0079766E  mov      rbx, rax
00797671  mov      qword ptr [rip + 0x270e240], rbx  ; -> 02EA58B8
00797678  mov      rbx, qword ptr [rsp + 0x50]
0079767D  add      rsp, 0x30
00797681  pop      rdi
00797682  ret      
```
