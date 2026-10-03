# F homing pack (FABLE): `15-Input/Input-Stack/input-stack-device-channel-and-bindings.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 5. No bearing page cites them and no documented function calls them directly.

## 00343C60 (96 B, extent 00343C60-00343CC0)

Documented callee on this page: `00361200`

```
00343C60  mov      qword ptr [rsp + 8], rbx
00343C65  push     rdi
00343C66  sub      rsp, 0x20
00343C6A  mov      rcx, r9
00343C6D  mov      rdi, rdx
00343C70  call     0x267e10  ; -> 00267E10 fn
00343C75  movzx    ecx, byte ptr [rdi + 0x15]
00343C79  mov      ebx, eax
00343C7B  call     0x267310  ; -> 00267310 fn
00343C80  xor      ecx, ecx
00343C82  mov      edx, 1
00343C87  test     eax, eax
00343C89  mov      r8d, edx
00343C8C  cmovne   ebx, ecx
00343C8F  mov      ecx, ebx
00343C91  call     0x361200  ; -> 00361200 fn
00343C96  call     0x25d5d0  ; -> 0025D5D0 fn
00343C9B  movzx    ecx, byte ptr [rdi + 0x15]
00343C9F  call     0x267310  ; -> 00267310 fn
00343CA4  test     eax, eax
00343CA6  je       0x343cb5  ; -> 00343CB5
00343CA8  xor      r8d, r8d
00343CAB  xor      edx, edx
00343CAD  or       ecx, 0xffffffff
00343CB0  call     0x360960  ; -> 00360960 fn
00343CB5  mov      rbx, qword ptr [rsp + 0x30]
00343CBA  add      rsp, 0x20
00343CBE  pop      rdi
00343CBF  ret      
```

## 005DCD10 (138 B, extent 005DCD10-005DCD9A)

Documented callee on this page: `00662EA0`

```
005DCD10  push     rdi
005DCD12  sub      rsp, 0x30
005DCD16  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005DCD1F  mov      qword ptr [rsp + 0x40], rbx
005DCD24  mov      qword ptr [rsp + 0x48], rbp
005DCD29  mov      qword ptr [rsp + 0x50], rsi
005DCD2E  mov      rbx, rcx
005DCD31  mov      edx, dword ptr [rcx]
005DCD33  mov      eax, edx
005DCD35  shr      eax, 0x1f
005DCD38  not      al
005DCD3A  test     al, 1
005DCD3C  je       0x5dcd7d  ; -> 005DCD7D
005DCD3E  btr      edx, 0x1f
005DCD42  mov      rbp, qword ptr [rcx + 8]
005DCD46  test     rbp, rbp
005DCD49  je       0x5dcd7d  ; -> 005DCD7D
005DCD4B  test     edx, edx
005DCD4D  je       0x5dcd6a  ; -> 005DCD6A
005DCD4F  mov      rdi, rbp
005DCD52  mov      esi, edx
005DCD54  mov      rcx, rdi
005DCD57  call     0x662ea0  ; -> 00662EA0 fn
005DCD5C  nop      
005DCD5D  add      rdi, 0x88
005DCD64  sub      rsi, 1
005DCD68  jne      0x5dcd54  ; -> 005DCD54
005DCD6A  mov      rcx, rbp
005DCD6D  call     0x584730  ; -> 00584730 fn
005DCD72  nop      
005DCD73  xor      eax, eax
005DCD75  mov      qword ptr [rbx + 8], rax
005DCD79  mov      dword ptr [rbx], eax
005DCD7B  jmp      0x5dcd85  ; -> 005DCD85
005DCD7D  xor      eax, eax
005DCD7F  mov      dword ptr [rcx], eax
005DCD81  mov      qword ptr [rcx + 8], rax
005DCD85  mov      rbx, qword ptr [rsp + 0x40]
005DCD8A  mov      rbp, qword ptr [rsp + 0x48]
005DCD8F  mov      rsi, qword ptr [rsp + 0x50]
005DCD94  add      rsp, 0x30
005DCD98  pop      rdi
005DCD99  ret      
```

## 005DE1D0 (64 B, extent 005DE1D0-005DE210)

Documented callee on this page: `0060B750`

```
005DE1D0  push     rbx
005DE1D2  sub      rsp, 0x30
005DE1D6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005DE1DF  mov      rbx, rcx
005DE1E2  mov      rcx, qword ptr [rcx]
005DE1E5  test     rcx, rcx
005DE1E8  je       0x5de1fb  ; -> 005DE1FB
005DE1EA  lea      rdx, [rbx + 8]
005DE1EE  mov      r8, rcx
005DE1F1  mov      rcx, qword ptr [rcx + 0x28]
005DE1F5  call     0x60b750  ; -> 0060B750 fn
005DE1FA  nop      
005DE1FB  mov      qword ptr [rbx], 0
005DE202  lea      rcx, [rbx + 8]
005DE206  add      rsp, 0x30
005DE20A  pop      rbx
005DE20B  jmp      0x16d6a0  ; -> 0016D6A0 fn
```

## 00670790 (119 B, extent 00670790-00670807)

Documented callee on this page: `006224E0`

```
00670790  mov      r9, qword ptr [rsp + 0x38]
00670795  xor      ecx, ecx
00670797  mov      r11, rdx
0067079A  test     r9, r9
0067079D  je       0x6707a5  ; -> 006707A5
0067079F  mov      ecx, dword ptr [r9 + 8]
006707A3  jmp      0x6707d9  ; -> 006707D9
006707A5  mov      r10, qword ptr [rsp + 0x30]
006707AA  mov      edx, ecx
006707AC  mov      r8d, dword ptr [r10]
006707AF  and      r8d, 0x7fffffff
006707B6  jbe      0x6707d9  ; -> 006707D9
006707B8  mov      r10, qword ptr [r10 + 8]
006707BC  nop      dword ptr [rax]
006707C0  mov      eax, edx
006707C2  imul     rcx, rax, 0x88
006707C9  mov      ecx, dword ptr [rcx + r10 + 4]
006707CE  test     ecx, ecx
006707D0  jne      0x6707d9  ; -> 006707D9
006707D2  inc      edx
006707D4  cmp      edx, r8d
006707D7  jb       0x6707c0  ; -> 006707C0
006707D9  mov      rax, qword ptr [rsp + 0x28]
006707DE  mov      edx, dword ptr [rax + 0x18]
006707E1  test     r9, r9
006707E4  je       0x6707f9  ; -> 006707F9
006707E6  mov      eax, dword ptr [rsp + 0x40]
006707EA  mov      r8d, ecx
006707ED  mov      rcx, r11
006707F0  mov      dword ptr [rsp + 0x28], eax
006707F4  jmp      0x6224e0  ; -> 006224E0 fn
006707F9  mov      r9d, ecx
006707FC  xor      r8d, r8d
006707FF  mov      rcx, r11
00670802  jmp      0x622350  ; -> 00622350 fn
```

## 00670810 (131 B, extent 00670810-00670893)

Documented callee on this page: `00622450`

```
00670810  mov      r9, qword ptr [rsp + 0x38]
00670815  xor      ecx, ecx
00670817  mov      r11, rdx
0067081A  test     r9, r9
0067081D  je       0x670825  ; -> 00670825
0067081F  mov      ecx, dword ptr [r9 + 8]
00670823  jmp      0x670859  ; -> 00670859
00670825  mov      r10, qword ptr [rsp + 0x30]
0067082A  mov      eax, ecx
0067082C  mov      r8d, dword ptr [r10]
0067082F  and      r8d, 0x7fffffff
00670836  jbe      0x670859  ; -> 00670859
00670838  mov      r10, qword ptr [r10 + 8]
0067083C  nop      dword ptr [rax]
00670840  mov      ecx, eax
00670842  imul     rdx, rcx, 0x88
00670849  mov      ecx, dword ptr [rdx + r10 + 4]
0067084E  test     ecx, ecx
00670850  jne      0x670859  ; -> 00670859
00670852  inc      eax
00670854  cmp      eax, r8d
00670857  jb       0x670840  ; -> 00670840
00670859  mov      rax, qword ptr [rsp + 0x28]
0067085E  mov      edx, dword ptr [rax + 0x18]
00670861  mov      eax, dword ptr [rsp + 0x48]
00670865  test     r9, r9
00670868  je       0x670881  ; -> 00670881
0067086A  mov      dword ptr [rsp + 0x30], eax
0067086E  mov      r8d, ecx
00670871  mov      eax, dword ptr [rsp + 0x40]
00670875  mov      rcx, r11
00670878  mov      dword ptr [rsp + 0x28], eax
0067087C  jmp      0x6226d0  ; -> 006226D0 fn
00670881  mov      r9d, ecx
00670884  mov      dword ptr [rsp + 0x28], eax
00670888  mov      rcx, r11
0067088B  xor      r8d, r8d
0067088E  jmp      0x622450  ; -> 00622450 fn
```
