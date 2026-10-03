# F homing pack: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md`

Generated 2026-10-02 21:56 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 3. No bearing page cites them and no documented function calls them directly.

## 00393950 (83 B, extent 00393950-003939A3)

Documented callee on this page: `00393240`

```
00393950  mov      qword ptr [rsp + 8], rbx
00393955  push     rdi
00393956  sub      rsp, 0x20
0039395A  movsxd   rbx, r9d
0039395D  mov      rdi, rdx
00393960  call     0x264150  ; -> 00264150 fn
00393965  test     eax, eax
00393967  je       0x39397c  ; -> 0039397C
00393969  mov      rcx, qword ptr [rdi + 0x10]
0039396D  xor      edx, edx
0039396F  test     ebx, ebx
00393971  sete     dl
00393974  mov      rcx, qword ptr [rcx]
00393977  call     0x393240  ; -> 00393240 fn
0039397C  mov      rax, qword ptr [rdi + 0x10]
00393980  mov      rdx, qword ptr [rax]
00393983  mov      rax, qword ptr [rdx + 0x20]
00393987  movzx    ecx, byte ptr [rax + rbx*8 + 7]
0039398C  mov      eax, 1
00393991  mov      word ptr [rdx + 0xa], bx
00393995  mov      rbx, qword ptr [rsp + 0x30]
0039399A  mov      byte ptr [rdx + 0x39], cl
0039399D  add      rsp, 0x20
003939A1  pop      rdi
003939A2  ret      
```

## 00510E40 (232 B, extent 00510E40-00510F28)

Documented callee on this page: `0055FB20`

```
00510E40  push     rbp
00510E42  push     r15
00510E44  sub      rsp, 0x38
00510E48  mov      rbp, r9
00510E4B  mov      r15, rcx
00510E4E  call     0x280120  ; -> 00280120 fn
00510E53  test     eax, eax
00510E55  jne      0x510f20  ; -> 00510F20
00510E5B  mov      qword ptr [rsp + 0x50], rbx
00510E60  mov      qword ptr [rsp + 0x58], rsi
00510E65  mov      qword ptr [rsp + 0x60], rdi
00510E6A  mov      qword ptr [rsp + 0x30], r14
00510E6F  call     0x2640c0  ; -> 002640C0 fn
00510E74  mov      rcx, rbp
00510E77  mov      rbx, rax
00510E7A  call     0x267e10  ; -> 00267E10 fn
00510E7F  mov      r8d, eax
00510E82  mov      rdx, r15
00510E85  mov      rcx, rbx
00510E88  call     0x2650b0  ; -> 002650B0 fn
00510E8D  mov      rcx, rbp
00510E90  mov      r14, rax
00510E93  call     0x267e10  ; -> 00267E10 fn
00510E98  mov      r8d, eax
00510E9B  mov      rdx, r15
00510E9E  mov      rcx, rbx
00510EA1  call     0x2650b0  ; -> 002650B0 fn
00510EA6  mov      rcx, rbp
00510EA9  mov      rsi, rax
00510EAC  call     0x267e10  ; -> 00267E10 fn
00510EB1  mov      r8d, eax
00510EB4  mov      rdx, r15
00510EB7  mov      rcx, rbx
00510EBA  call     0x2650b0  ; -> 002650B0 fn
00510EBF  mov      rcx, rbp
00510EC2  mov      rdi, rax
00510EC5  call     0x267e10  ; -> 00267E10 fn
00510ECA  mov      r8d, eax
00510ECD  mov      rdx, r15
00510ED0  mov      rcx, rbx
00510ED3  call     0x2650b0  ; -> 002650B0 fn
00510ED8  mov      rcx, rbp
00510EDB  mov      rbx, rax
00510EDE  call     0x267e10  ; -> 00267E10 fn
00510EE3  lea      rdx, [rsp + 0x20]
00510EE8  mov      ecx, eax
00510EEA  call     0x55fb20  ; -> 0055FB20 fn
00510EEF  movsx    ecx, word ptr [rsp + 0x20]
00510EF4  mov      dword ptr [rbx], ecx
00510EF6  movsx    eax, word ptr [rsp + 0x22]
00510EFB  mov      rbx, qword ptr [rsp + 0x50]
00510F00  mov      dword ptr [rdi], eax
00510F02  movsx    eax, word ptr [rsp + 0x24]
00510F07  mov      rdi, qword ptr [rsp + 0x60]
00510F0C  mov      dword ptr [rsi], eax
00510F0E  movsx    eax, word ptr [rsp + 0x26]
00510F13  mov      rsi, qword ptr [rsp + 0x58]
00510F18  mov      dword ptr [r14], eax
00510F1B  mov      r14, qword ptr [rsp + 0x30]
00510F20  add      rsp, 0x38
00510F24  pop      r15
00510F26  pop      rbp
00510F27  ret      
```

## 0056CF10 (660 B, extent 0056CF10-0056D1A4)

Documented callee on this page: `00393240`

```
0056CF10  push     rbp
0056CF12  push     r15
0056CF14  sub      rsp, 0x48
0056CF18  mov      rax, qword ptr [rcx + 0xc8]
0056CF1F  mov      rbp, rdx
0056CF22  mov      r10, rcx
0056CF25  test     rax, rax
0056CF28  je       0x56d12c  ; -> 0056D12C
0056CF2E  mov      r8d, dword ptr [rcx + 0xe4]
0056CF35  mov      qword ptr [rsp + 0x60], rbx
0056CF3A  mov      ebx, dword ptr [rsp + 0x30]
0056CF3E  mov      qword ptr [rsp + 0x68], rsi
0056CF43  mov      qword ptr [rsp + 0x70], rdi
0056CF48  mov      qword ptr [rsp + 0x78], r12
0056CF4D  xor      r12d, r12d
0056CF50  mov      qword ptr [rsp + 0x40], r14
0056CF55  movsxd   r14, r9d
0056CF58  shl      r14, 5
0056CF5C  add      r14, rax
0056CF5F  mov      eax, r8d
0056CF62  xor      eax, ebx
0056CF64  and      eax, 3
0056CF67  xor      ebx, eax
0056CF69  test     r8b, 2
0056CF6D  je       0x56cfac  ; -> 0056CFAC
0056CF6F  mov      rcx, qword ptr [rcx + 0xc0]
0056CF76  movsx    eax, word ptr [rcx + 0xf2]
0056CF7D  movsx    edx, word ptr [rcx + 0xf4]
0056CF84  add      edx, eax
0056CF86  movzx    eax, byte ptr [rcx + 0xec]
0056CF8D  imul     edx, eax
0056CF90  movsx    eax, byte ptr [rcx + 0xee]
0056CF97  add      edx, eax
0056CF99  movsx    eax, byte ptr [rcx + 0xed]
0056CFA0  add      edx, eax
0056CFA2  lea      eax, [r12 + 4]
0056CFA7  cmp      edx, r9d
0056CFAA  je       0x56cfaf  ; -> 0056CFAF
0056CFAC  mov      eax, r12d
0056CFAF  and      ebx, 0xfffffffb
0056CFB2  or       ebx, eax
0056CFB4  movzx    eax, word ptr [r10 + 0xdc]
0056CFBC  mov      word ptr [rsp + 0x34], ax
0056CFC1  mov      eax, 0x63
0056CFC6  mov      word ptr [rsp + 0x36], ax
0056CFCB  mov      dword ptr [rsp + 0x30], ebx
0056CFCF  call     0x253690  ; -> 00253690 fn
0056CFD4  mov      dword ptr [rsp + 0x38], eax
0056CFD8  mov      edx, eax
0056CFDA  mov      r15d, 1
0056CFE0  test     bl, 2
0056CFE3  je       0x56cfee  ; -> 0056CFEE
0056CFE5  shr      ebx, 1
0056CFE7  not      ebx
0056CFE9  and      ebx, 2
0056CFEC  jmp      0x56d049  ; -> 0056D049
0056CFEE  test     r15b, bl
0056CFF1  je       0x56d01a  ; -> 0056D01A
0056CFF3  cmp      dword ptr [r14 + 0x10], 0x80000000
0056CFFB  mov      eax, 8
0056D000  movsx    edx, word ptr [r14 + 0xc]
0056D005  cmovb    eax, r12d
0056D009  mov      ecx, eax
0056D00B  cmp      edx, -1
0056D00E  je       0x56d040  ; -> 0056D040
0056D010  or       ecx, 2
0056D013  test     edx, edx
0056D015  cmovne   ecx, eax
0056D018  jmp      0x56d040  ; -> 0056D040
0056D01A  cmp      word ptr [r14 + 0xe], 0x63
0056D020  mov      ecx, r12d
0056D023  mov      eax, dword ptr [r14 + 0x10]
0056D027  cmovae   ecx, r15d
0056D02B  btr      eax, 0x1f
0056D02F  cmp      eax, edx
0056D031  jbe      0x56d040  ; -> 0056D040
0056D033  or       ecx, 4
0056D036  nop      word ptr [rax + rax]
0056D040  test     ecx, ecx
0056D042  mov      ebx, r12d
0056D045  cmovne   ebx, r15d
0056D049  mov      edi, r12d
0056D04C  lea      rsi, [rip + 0x7b65b5]  ; -> 00D23608
0056D053  movsxd   rax, dword ptr [rsi]
0056D056  mov      edx, ebx
0056D058  mov      rcx, qword ptr [rbp + 0x10]
0056D05C  mov      rcx, qword ptr [rcx + rax*8]
0056D060  call     0x393240  ; -> 00393240 fn
0056D065  inc      edi
0056D067  lea      rsi, [rsi + 4]
0056D06B  cmp      edi, 4
0056D06E  jb       0x56d053  ; -> 0056D053
0056D070  mov      rax, qword ptr [rbp + 0x10]
0056D074  mov      ecx, r12d
0056D077  cmp      byte ptr [r14 + 0xa], 0xff
0056D07C  setne    cl
0056D07F  mov      r8, qword ptr [rax]
0056D082  mov      eax, dword ptr [r8 + 8]
0056D086  and      eax, 0xfffffffe
0056D089  or       ecx, eax
0056D08B  mov      rax, qword ptr [r8 + 0x20]
0056D08F  mov      dword ptr [r8 + 8], ecx
0056D093  movzx    edx, byte ptr [r14 + 0xa]
0056D098  movzx    ecx, byte ptr [rax + rdx*8 + 7]
0056D09D  mov      byte ptr [r8 + 0x39], cl
0056D0A1  xor      ecx, ecx
0056D0A3  mov      word ptr [r8 + 0xa], dx
0056D0A8  mov      rax, qword ptr [rbp + 0x10]
0056D0AC  mov      rbx, qword ptr [rax + 8]
0056D0B0  mov      rax, qword ptr [r14]
0056D0B3  mov      qword ptr [rbx + 0x18], rax
0056D0B7  call     0x20e620  ; -> 0020E620 fn
0056D0BC  mov      dword ptr [rbx + 0x20], eax
0056D0BF  xor      r8d, r8d
0056D0C2  mov      rcx, qword ptr [rbp + 0x10]
0056D0C6  xor      edx, edx
0056D0C8  mov      r9d, dword ptr [r14 + 0x10]
0056D0CC  btr      r9d, 0x1f
0056D0D1  mov      qword ptr [rsp + 0x28], r12
0056D0D6  mov      dword ptr [rsp + 0x20], r12d
0056D0DB  mov      rcx, qword ptr [rcx + 0x18]
0056D0DF  call     0x29ff60  ; -> 0029FF60 fn
0056D0E4  mov      rcx, qword ptr [rbp + 0x10]
0056D0E8  mov      rcx, qword ptr [rcx + 0x18]
0056D0EC  call     0x29fb50  ; -> 0029FB50 fn
0056D0F1  lea      r9, [rip + 0x7b6428]  ; -> 00D23520
0056D0F8  mov      rdx, rbp
0056D0FB  lea      r8, [rsp + 0x30]
0056D100  mov      rcx, r14
0056D103  call     0x56da80  ; -> 0056DA80 fn
0056D108  mov      r14, qword ptr [rsp + 0x40]
0056D10D  mov      eax, r15d
0056D110  mov      r12, qword ptr [rsp + 0x78]
0056D115  mov      rdi, qword ptr [rsp + 0x70]
0056D11A  mov      rsi, qword ptr [rsp + 0x68]
0056D11F  mov      rbx, qword ptr [rsp + 0x60]
0056D124  add      rsp, 0x48
0056D128  pop      r15
0056D12A  pop      rbp
0056D12B  ret      
0056D12C  mov      rax, qword ptr [rdx + 0x10]
0056D130  mov      rcx, qword ptr [rax]
0056D133  and      dword ptr [rcx + 8], 0xfffffffe
0056D137  mov      rax, qword ptr [rdx + 0x10]
0056D13B  mov      rcx, qword ptr [rax + 8]
0056D13F  and      dword ptr [rcx + 8], 0xfffffffe
0056D143  mov      rax, qword ptr [rdx + 0x10]
0056D147  mov      rcx, qword ptr [rax + 0x18]
0056D14B  and      dword ptr [rcx + 8], 0xfffffffe
0056D14F  mov      rax, qword ptr [rdx + 0x10]
0056D153  mov      rcx, qword ptr [rax + 0x20]
0056D157  and      dword ptr [rcx + 8], 0xfffffffe
0056D15B  mov      rax, qword ptr [rdx + 0x10]
0056D15F  mov      rcx, qword ptr [rax + 0x10]
0056D163  and      dword ptr [rcx + 8], 0xfffffffe
0056D167  mov      rax, qword ptr [rdx + 0x10]
0056D16B  mov      rcx, qword ptr [rax + 0x40]
0056D16F  and      dword ptr [rcx + 8], 0xfffffffe
0056D173  mov      rax, qword ptr [rdx + 0x10]
0056D177  mov      rcx, qword ptr [rax + 0x28]
0056D17B  and      dword ptr [rcx + 8], 0xfffffffe
0056D17F  mov      rax, qword ptr [rdx + 0x10]
0056D183  mov      rcx, qword ptr [rax + 0x30]
0056D187  and      dword ptr [rcx + 8], 0xfffffffe
0056D18B  mov      rax, qword ptr [rdx + 0x10]
0056D18F  mov      rcx, qword ptr [rax + 0x38]
0056D193  mov      eax, 1
0056D198  and      dword ptr [rcx + 8], 0xfffffffe
0056D19C  add      rsp, 0x48
0056D1A0  pop      r15
0056D1A2  pop      rbp
0056D1A3  ret      
```
