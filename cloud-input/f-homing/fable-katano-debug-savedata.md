# F homing pack (FABLE): `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/katano-debug-savedata.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 5. No bearing page cites them and no documented function calls them directly.

## 001C1C00 (128 B, extent 001C1C00-001C1C80)

Documented callee on this page: `001C19A0`

```
001C1C00  mov      qword ptr [rsp + 8], rbx
001C1C05  mov      qword ptr [rsp + 0x10], rbp
001C1C0A  mov      qword ptr [rsp + 0x18], rsi
001C1C0F  mov      qword ptr [rsp + 0x20], rdi
001C1C14  push     r14
001C1C16  sub      rsp, 0x20
001C1C1A  xor      edi, edi
001C1C1C  mov      r14, rcx
001C1C1F  mov      dword ptr [rcx], edi
001C1C21  mov      ebx, edi
001C1C23  mov      esi, dword ptr [rdx]
001C1C25  mov      rbp, qword ptr [rdx + 8]
001C1C29  and      esi, 0x7fffffff
001C1C2F  jbe      0x1c1c55  ; -> 001C1C55
001C1C31  mov      ecx, esi
001C1C33  lea      edx, [rdi + 8]
001C1C36  shl      rcx, 3
001C1C3A  call     0x17d260  ; -> 0017D260 fn
001C1C3F  mov      rbx, rax
001C1C42  test     rax, rax
001C1C45  je       0x1c1c55  ; -> 001C1C55
001C1C47  mov      r8d, esi
001C1C4A  mov      rdx, rbp
001C1C4D  mov      rcx, rax
001C1C50  call     0x1c19a0  ; -> 001C19A0 fn
001C1C55  mov      rbp, qword ptr [rsp + 0x38]
001C1C5A  test     rbx, rbx
001C1C5D  mov      qword ptr [r14 + 8], rbx
001C1C61  mov      rax, r14
001C1C64  mov      rbx, qword ptr [rsp + 0x30]
001C1C69  cmovne   edi, esi
001C1C6C  mov      rsi, qword ptr [rsp + 0x40]
001C1C71  mov      dword ptr [r14], edi
001C1C74  mov      rdi, qword ptr [rsp + 0x48]
001C1C79  add      rsp, 0x20
001C1C7D  pop      r14
001C1C7F  ret      
```

## 001C1E70 (417 B, extent 001C1E70-001C2011)

Documented callee on this page: `001C26B0`

```
001C1E70  mov      qword ptr [rsp + 8], rcx
001C1E75  push     rdi
001C1E76  sub      rsp, 0x30
001C1E7A  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001C1E83  mov      qword ptr [rsp + 0x48], rbx
001C1E88  mov      rbx, rdx
001C1E8B  mov      rdi, rcx
001C1E8E  movups   xmm0, xmmword ptr [rdx]
001C1E91  movups   xmmword ptr [rcx], xmm0
001C1E94  mov      rax, qword ptr [rdx + 0x10]
001C1E98  mov      qword ptr [rcx + 0x10], rax
001C1E9C  mov      rax, qword ptr [rdx + 0x18]
001C1EA0  mov      qword ptr [rcx + 0x18], rax
001C1EA4  mov      rax, qword ptr [rdx + 0x20]
001C1EA8  mov      qword ptr [rcx + 0x20], rax
001C1EAC  add      rdx, 0x28
001C1EB0  add      rcx, 0x28
001C1EB4  call     0x1c1c00  ; -> 001C1C00 fn
001C1EB9  nop      
001C1EBA  movzx    eax, byte ptr [rbx + 0x38]
001C1EBE  and      eax, 1
001C1EC1  mov      rcx, qword ptr [rbx + 0x38]
001C1EC5  sub      rcx, rax
001C1EC8  call     0x1c26b0  ; -> 001C26B0 fn
001C1ECD  mov      qword ptr [rdi + 0x38], rax
001C1ED1  lea      rdx, [rbx + 0x40]
001C1ED5  lea      rcx, [rdi + 0x40]
001C1ED9  call     0x67acf0  ; -> 0067ACF0 fn
001C1EDE  movups   xmm0, xmmword ptr [rbx + 0x58]
001C1EE2  movups   xmmword ptr [rdi + 0x58], xmm0
001C1EE6  movups   xmm0, xmmword ptr [rbx + 0x68]
001C1EEA  movups   xmmword ptr [rdi + 0x68], xmm0
001C1EEE  movups   xmm0, xmmword ptr [rbx + 0x78]
001C1EF2  movups   xmmword ptr [rdi + 0x78], xmm0
001C1EF6  movups   xmm0, xmmword ptr [rbx + 0x88]
001C1EFD  movups   xmmword ptr [rdi + 0x88], xmm0
001C1F04  movups   xmm0, xmmword ptr [rbx + 0x98]
001C1F0B  movups   xmmword ptr [rdi + 0x98], xmm0
001C1F12  movups   xmm0, xmmword ptr [rbx + 0xa8]
001C1F19  movups   xmmword ptr [rdi + 0xa8], xmm0
001C1F20  movups   xmm0, xmmword ptr [rbx + 0xb8]
001C1F27  movups   xmmword ptr [rdi + 0xb8], xmm0
001C1F2E  movups   xmm0, xmmword ptr [rbx + 0xc8]
001C1F35  movups   xmmword ptr [rdi + 0xc8], xmm0
001C1F3C  movups   xmm0, xmmword ptr [rbx + 0xd8]
001C1F43  movups   xmmword ptr [rdi + 0xd8], xmm0
001C1F4A  movzx    eax, byte ptr [rbx + 0xe8]
001C1F51  mov      byte ptr [rdi + 0xe8], al
001C1F57  movzx    eax, byte ptr [rbx + 0xe9]
001C1F5E  mov      byte ptr [rdi + 0xe9], al
001C1F64  movzx    eax, byte ptr [rbx + 0xea]
001C1F6B  mov      byte ptr [rdi + 0xea], al
001C1F71  mov      eax, dword ptr [rbx + 0xec]
001C1F77  mov      dword ptr [rdi + 0xec], eax
001C1F7D  mov      eax, dword ptr [rbx + 0xf0]
001C1F83  mov      dword ptr [rdi + 0xf0], eax
001C1F89  mov      eax, dword ptr [rbx + 0xf4]
001C1F8F  mov      dword ptr [rdi + 0xf4], eax
001C1F95  mov      eax, dword ptr [rbx + 0xf8]
001C1F9B  mov      dword ptr [rdi + 0xf8], eax
001C1FA1  mov      eax, dword ptr [rbx + 0xfc]
001C1FA7  mov      dword ptr [rdi + 0xfc], eax
001C1FAD  movups   xmm0, xmmword ptr [rbx + 0x100]
001C1FB4  movups   xmmword ptr [rdi + 0x100], xmm0
001C1FBB  mov      eax, dword ptr [rbx + 0x110]
001C1FC1  mov      dword ptr [rdi + 0x110], eax
001C1FC7  mov      eax, dword ptr [rbx + 0x114]
001C1FCD  mov      dword ptr [rdi + 0x114], eax
001C1FD3  mov      eax, dword ptr [rbx + 0x118]
001C1FD9  mov      dword ptr [rdi + 0x118], eax
001C1FDF  mov      eax, dword ptr [rbx + 0x11c]
001C1FE5  mov      dword ptr [rdi + 0x11c], eax
001C1FEB  mov      eax, dword ptr [rbx + 0x120]
001C1FF1  mov      dword ptr [rdi + 0x120], eax
001C1FF7  mov      eax, dword ptr [rbx + 0x124]
001C1FFD  mov      dword ptr [rdi + 0x124], eax
001C2003  mov      rax, rdi
001C2006  mov      rbx, qword ptr [rsp + 0x48]
001C200B  add      rsp, 0x30
001C200F  pop      rdi
001C2010  ret      
```

## 0063AD30 (94 B, extent 0063AD30-0063AD8E)

Documented callee on this page: `001C2720`

```
0063AD30  push     rbx
0063AD32  sub      rsp, 0x30
0063AD36  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0063AD3F  mov      rbx, rdx
0063AD42  mov      ecx, dword ptr [rdx]
0063AD44  mov      eax, ecx
0063AD46  shr      eax, 0x1f
0063AD49  not      al
0063AD4B  test     al, 1
0063AD4D  je       0x63ad7e  ; -> 0063AD7E
0063AD4F  btr      ecx, 0x1f
0063AD53  cmp      ecx, 1
0063AD56  jbe      0x63ad65  ; -> 0063AD65
0063AD58  mov      edx, ecx
0063AD5A  mov      rcx, qword ptr [rbx + 8]
0063AD5E  call     0x1c2720  ; -> 001C2720 fn
0063AD63  jmp      0x63ad7e  ; -> 0063AD7E
0063AD65  jne      0x63ad7e  ; -> 0063AD7E
0063AD67  mov      rcx, qword ptr [rdx + 8]
0063AD6B  test     rcx, rcx
0063AD6E  je       0x63ad7e  ; -> 0063AD7E
0063AD70  mov      eax, ecx
0063AD72  not      al
0063AD74  test     al, 1
0063AD76  je       0x63ad7e  ; -> 0063AD7E
0063AD78  call     0x584730  ; -> 00584730 fn
0063AD7D  nop      
0063AD7E  xor      eax, eax
0063AD80  mov      qword ptr [rbx + 8], rax
0063AD84  mov      dword ptr [rbx], eax
0063AD86  mov      al, 1
0063AD88  add      rsp, 0x30
0063AD8C  pop      rbx
0063AD8D  ret      
```

## 0063DCA0 (131 B, extent 0063DCA0-0063DD23)

Documented callee on this page: `001C2720`

```
0063DCA0  push     rdi
0063DCA2  sub      rsp, 0x30
0063DCA6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0063DCAF  mov      qword ptr [rsp + 0x40], rbx
0063DCB4  mov      qword ptr [rsp + 0x48], rbp
0063DCB9  mov      qword ptr [rsp + 0x50], rsi
0063DCBE  mov      ebp, r8d
0063DCC1  mov      rsi, rdx
0063DCC4  mov      rbx, rcx
0063DCC7  lea      rdi, [rcx + 8]
0063DCCB  cmp      r9, rdx
0063DCCE  je       0x63dd04  ; -> 0063DD04
0063DCD0  cmp      r9, rdi
0063DCD3  jne      0x63dced  ; -> 0063DCED
0063DCD5  mov      rcx, qword ptr [r9]
0063DCD8  test     rcx, rcx
0063DCDB  je       0x63dceb  ; -> 0063DCEB
0063DCDD  mov      eax, ecx
0063DCDF  not      al
0063DCE1  test     al, 1
0063DCE3  je       0x63dceb  ; -> 0063DCEB
0063DCE5  call     0x584730  ; -> 00584730 fn
0063DCEA  nop      
0063DCEB  jmp      0x63dd04  ; -> 0063DD04
0063DCED  mov      eax, dword ptr [rcx]
0063DCEF  shr      eax, 0x1f
0063DCF2  not      al
0063DCF4  test     al, 1
0063DCF6  je       0x63dd04  ; -> 0063DD04
0063DCF8  mov      edx, dword ptr [rsp + 0x60]
0063DCFC  mov      rcx, r9
0063DCFF  call     0x1c2720  ; -> 001C2720 fn
0063DD04  mov      dword ptr [rbx], ebp
0063DD06  cmp      rsi, rdi
0063DD09  je       0x63dd0e  ; -> 0063DD0E
0063DD0B  mov      qword ptr [rdi], rsi
0063DD0E  mov      rbx, qword ptr [rsp + 0x40]
0063DD13  mov      rbp, qword ptr [rsp + 0x48]
0063DD18  mov      rsi, qword ptr [rsp + 0x50]
0063DD1D  add      rsp, 0x30
0063DD21  pop      rdi
0063DD22  ret      
```

## 0063DE10 (205 B, extent 0063DE10-0063DEDD)

Documented callee on this page: `001C26B0`

```
0063DE10  push     rsi
0063DE12  push     rdi
0063DE13  push     r14
0063DE15  sub      rsp, 0x40
0063DE19  mov      qword ptr [rsp + 0x30], 0xfffffffffffffffe
0063DE22  mov      qword ptr [rsp + 0x60], rbx
0063DE27  mov      qword ptr [rsp + 0x68], rbp
0063DE2C  mov      eax, r8d
0063DE2F  mov      r14, rdx
0063DE32  mov      rsi, rcx
0063DE35  test     r8d, r8d
0063DE38  jns      0x63de44  ; -> 0063DE44
0063DE3A  mov      eax, 5
0063DE3F  jmp      0x63deca  ; -> 0063DECA
0063DE44  mov      edi, dword ptr [rcx]
0063DE46  btr      edi, 0x1f
0063DE4A  cmp      edi, 1
0063DE4D  jbe      0x63de55  ; -> 0063DE55
0063DE4F  mov      rbp, qword ptr [rcx + 8]
0063DE53  jmp      0x63de61  ; -> 0063DE61
0063DE55  test     edi, edi
0063DE57  je       0x63de5f  ; -> 0063DE5F
0063DE59  lea      rbp, [rcx + 8]
0063DE5D  jmp      0x63de61  ; -> 0063DE61
0063DE5F  xor      ebp, ebp
0063DE61  bts      r8d, 0x1f
0063DE66  cmp      eax, 1
0063DE69  jne      0x63deb6  ; -> 0063DEB6
0063DE6B  lea      rbx, [rcx + 8]
0063DE6F  mov      qword ptr [rsp + 0x78], rbx
0063DE74  cmp      edi, eax
0063DE76  jne      0x63de8e  ; -> 0063DE8E
0063DE78  mov      rcx, qword ptr [rbx]
0063DE7B  test     rcx, rcx
0063DE7E  je       0x63de8e  ; -> 0063DE8E
0063DE80  mov      eax, ecx
0063DE82  not      al
0063DE84  test     al, 1
0063DE86  je       0x63de8e  ; -> 0063DE8E
0063DE88  call     0x584730  ; -> 00584730 fn
0063DE8D  nop      
0063DE8E  mov      qword ptr [rsp + 0x38], rbx
0063DE93  test     rbx, rbx
0063DE96  je       0x63dead  ; -> 0063DEAD
0063DE98  movzx    eax, byte ptr [r14]
0063DE9C  and      eax, 1
0063DE9F  mov      rcx, qword ptr [r14]
0063DEA2  sub      rcx, rax
0063DEA5  call     0x1c26b0  ; -> 001C26B0 fn
0063DEAA  mov      qword ptr [rbx], rax
0063DEAD  mov      r14, rbx
0063DEB0  mov      r8d, 1
0063DEB6  mov      dword ptr [rsp + 0x20], edi
0063DEBA  mov      r9, rbp
0063DEBD  mov      rdx, r14
0063DEC0  mov      rcx, rsi
0063DEC3  call     0x63dca0  ; -> 0063DCA0 fn
0063DEC8  xor      eax, eax
0063DECA  mov      rbx, qword ptr [rsp + 0x60]
0063DECF  mov      rbp, qword ptr [rsp + 0x68]
0063DED4  add      rsp, 0x40
0063DED8  pop      r14
0063DEDA  pop      rdi
0063DEDB  pop      rsi
0063DEDC  ret      
```
