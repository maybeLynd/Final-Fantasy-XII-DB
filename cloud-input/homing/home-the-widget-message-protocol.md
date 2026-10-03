# Homing pack: `16-UI/Widget-Object-Model/the-widget-message-protocol.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-widget-message-protocol.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00297E10 (88 B, extent 00297E10-00297E68)

Entered from (direct sites whose caller this page cites): `0029A0A0` + 0x4C5 (call; `0029A0A0` is cited on this page)
Other direct sites: none

Host context: "already sent '{1}' by the time '00276650' sends '{29}'; construct says "you exist", 29 says "the fields are now set".  **Message 30 is narrowed, not named — its senders do not agree.** Of its three, '0029A0A0' sends it to **another object** ('qword[rbp + 0x120]', a delegate) and **consumes the return** ('0029A19C call rax' / 'test eax, eax' / 'je'), while '002778C0' sends a **16-byte constant argument block** ('movdqa xmm0, [00915BC0]',"

```
00297E10  push     rbx
00297E12  sub      rsp, 0x20
00297E16  mov      ebx, edx
00297E18  cmp      edx, dword ptr [rcx + 0xe0]
00297E1E  jne      0x297e31  ; -> 00297E31
00297E20  cmp      r8d, dword ptr [rcx + 0xe8]
00297E27  jne      0x297e31  ; -> 00297E31
00297E29  xor      eax, eax
00297E2B  add      rsp, 0x20
00297E2F  pop      rbx
00297E30  ret      
00297E31  mov      rax, qword ptr [rcx + 0x60]
00297E35  mov      qword ptr [rsp + 0x30], rdi
00297E3A  mov      rdi, qword ptr [rax + 0x30]
00297E3E  mov      rcx, rdi
00297E41  cmp      r8d, ebx
00297E44  jle      0x297e49  ; -> 00297E49
00297E46  mov      edx, r8d
00297E49  call     0x29f4b0  ; -> 0029F4B0 fn
00297E4E  mov      edx, ebx
00297E50  mov      rcx, rdi
00297E53  call     0x225580  ; -> 00225580 fn
00297E58  mov      rdi, qword ptr [rsp + 0x30]
00297E5D  mov      eax, 1
00297E62  add      rsp, 0x20
00297E66  pop      rbx
00297E67  ret      
```

## 00297F60 (115 B, extent 00297F60-00297FD3)

Entered from (direct sites whose caller this page cites): `0029A0A0` + 0x529 (call; `0029A0A0` is cited on this page)
Other direct sites: none

Host context: "already sent '{1}' by the time '00276650' sends '{29}'; construct says "you exist", 29 says "the fields are now set".  **Message 30 is narrowed, not named — its senders do not agree.** Of its three, '0029A0A0' sends it to **another object** ('qword[rbp + 0x120]', a delegate) and **consumes the return** ('0029A19C call rax' / 'test eax, eax' / 'je'), while '002778C0' sends a **16-byte constant argument block** ('movdqa xmm0, [00915BC0]',"

```
00297F60  mov      qword ptr [rsp + 8], rbx
00297F65  mov      qword ptr [rsp + 0x10], rsi
00297F6A  push     rdi
00297F6B  sub      rsp, 0x20
00297F6F  mov      rbx, r8
00297F72  mov      edi, edx
00297F74  mov      rsi, rcx
00297F77  cmp      dword ptr [rcx + 0xec], edx
00297F7D  je       0x297fc3  ; -> 00297FC3
00297F7F  mov      ecx, edx
00297F81  call     0x296600  ; -> 00296600 fn
00297F86  mov      rdx, qword ptr [rsi + 0x60]
00297F8A  test     rax, rax
00297F8D  mov      r9, rax
00297F90  cmove    r9, rbx
00297F94  mov      rcx, qword ptr [rdx + 0xe0]
00297F9B  mov      rax, qword ptr [rcx + 0x18]
00297F9F  test     rax, rax
00297FA2  jne      0x297fa8  ; -> 00297FA8
00297FA4  xor      ebx, ebx
00297FA6  jmp      0x297faf  ; -> 00297FAF
00297FA8  mov      rax, qword ptr [rax + 0x60]
00297FAC  mov      rbx, qword ptr [rax]
00297FAF  xor      ecx, ecx
00297FB1  mov      qword ptr [rbx + 0x18], r9
00297FB5  call     0x20e620  ; -> 0020E620 fn
00297FBA  mov      dword ptr [rbx + 0x20], eax
00297FBD  mov      dword ptr [rsi + 0xec], edi
00297FC3  mov      rbx, qword ptr [rsp + 0x30]
00297FC8  mov      rsi, qword ptr [rsp + 0x38]
00297FCD  add      rsp, 0x20
00297FD1  pop      rdi
00297FD2  ret      
```

## 003FCDE0 (245 B, extent 003FCDE0-003FCED5)

Entered from (direct sites whose caller this page cites): `003FCD20` + 0xA2 (call; `003FCD20` is cited on this page)
Other direct sites: none

Host context: "' (the '+0x28' bit-0 test).  '003FCCC0' (83 B) is the 0xC0-record builder the message-protocol callers run: under a stack cookie it packs 'ecx'/'edx' into a stack descriptor and calls '00244F50(0xC0, 003FCD20, &desc)' so the '003FCD20' callback constructs the record. Interior anchor '003FCCFC' (the '00244F50' builder call).  ## SWE2-EC7-99 update (2026-09-20) - '002D4D60' + '002D1820' + '002CF8B0' + '002CD470' measured  '002D4D60' (423 "

```
003FCDE0  mov      qword ptr [rsp + 0x10], rbx
003FCDE5  mov      qword ptr [rsp + 0x18], rbp
003FCDEA  push     rsi
003FCDEB  push     rdi
003FCDEC  push     r12
003FCDEE  push     r14
003FCDF0  push     r15
003FCDF2  sub      rsp, 0x20
003FCDF6  mov      rsi, rcx
003FCDF9  test     rcx, rcx
003FCDFC  jne      0x3fce02  ; -> 003FCE02
003FCDFE  xor      ebx, ebx
003FCE00  jmp      0x3fce0a  ; -> 003FCE0A
003FCE02  mov      rax, qword ptr [rcx + 0x60]
003FCE06  mov      rbx, qword ptr [rax + 0x28]
003FCE0A  mov      rbx, qword ptr [rbx + 0x18]
003FCE0E  xor      edi, edi
003FCE10  mov      rbx, qword ptr [rbx + 0x98]
003FCE17  mov      qword ptr [rsp + 0x50], rbx
003FCE1C  nop      dword ptr [rax]
003FCE20  test     rsi, rsi
003FCE23  jne      0x3fce29  ; -> 003FCE29
003FCE25  xor      ecx, ecx
003FCE27  jmp      0x3fce31  ; -> 003FCE31
003FCE29  mov      rax, qword ptr [rsi + 0x60]
003FCE2D  mov      rcx, qword ptr [rdi + rax]
003FCE31  mov      rcx, qword ptr [rcx + 0x18]
003FCE35  xor      edx, edx
003FCE37  call     0x247870  ; -> 00247870 fn
003FCE3C  add      rdi, 8
003FCE40  cmp      rdi, 0x28
003FCE44  jle      0x3fce20  ; -> 003FCE20
003FCE46  movzx    r15d, word ptr [rsp + 0x54]
003FCE4C  lea      r12, [rip + 0x91524d]  ; -> 00D120A0
003FCE53  movzx    r14d, word ptr [rsp + 0x50]
003FCE59  xor      ebp, ebp
003FCE5B  nop      dword ptr [rax + rax]
003FCE60  mov      ecx, ebp
003FCE62  call     0x282df0  ; -> 00282DF0 fn
003FCE67  mov      rcx, rax
003FCE6A  mov      rdi, rax
003FCE6D  call     0x282fa0  ; -> 00282FA0 fn
003FCE72  test     eax, eax
003FCE74  je       0x3fceb7  ; -> 003FCEB7
003FCE76  test     rsi, rsi
003FCE79  jne      0x3fce7f  ; -> 003FCE7F
003FCE7B  xor      edi, edi
003FCE7D  jmp      0x3fce90  ; -> 003FCE90
003FCE7F  movsx    rax, word ptr [rdi + 0x60]
003FCE84  movsxd   rcx, dword ptr [r12 + rax*4]
003FCE88  mov      rax, qword ptr [rsi + 0x60]
003FCE8C  mov      rdi, qword ptr [rax + rcx*8]
003FCE90  mov      rdi, qword ptr [rdi + 0x18]
003FCE94  mov      edx, 1
003FCE99  mov      rcx, rdi
003FCE9C  call     0x247870  ; -> 00247870 fn
003FCEA1  add      r14w, r15w
003FCEA5  mov      qword ptr [rdi + 0x98], rbx
003FCEAC  mov      word ptr [rsp + 0x50], r14w
003FCEB2  mov      rbx, qword ptr [rsp + 0x50]
003FCEB7  inc      ebp
003FCEB9  cmp      ebp, 9
003FCEBC  jl       0x3fce60  ; -> 003FCE60
003FCEBE  mov      rbx, qword ptr [rsp + 0x58]
003FCEC3  mov      rbp, qword ptr [rsp + 0x60]
003FCEC8  add      rsp, 0x20
003FCECC  pop      r15
003FCECE  pop      r14
003FCED0  pop      r12
003FCED2  pop      rdi
003FCED3  pop      rsi
003FCED4  ret      
```
