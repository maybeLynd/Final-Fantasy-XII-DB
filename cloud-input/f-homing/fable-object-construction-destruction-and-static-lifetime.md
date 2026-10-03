# F homing pack (FABLE): `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 4. No bearing page cites them and no documented function calls them directly.

## 0019B2F0 (270 B, extent 0019B2F0-0019B3FE)

Documented callee on this page: `00808850`

```
0019B2F0  push     rdi
0019B2F2  sub      rsp, 0x40
0019B2F6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0019B2FF  mov      qword ptr [rsp + 0x60], rbx
0019B304  mov      qword ptr [rsp + 0x68], rsi
0019B309  mov      rsi, rcx
0019B30C  xor      edx, edx
0019B30E  lea      rcx, [rsp + 0x50]
0019B313  call     qword ptr [rip + 0x7272d7]  ; -> 008C25F0 [u64 0x0000000001CCCD2C]
0019B319  nop      
0019B31A  mov      rax, qword ptr [rip + 0x1de5e27]  ; -> 01F81148
0019B321  mov      qword ptr [rsp + 0x58], rax
0019B326  mov      rcx, qword ptr [rip + 0x72727b]  ; -> 008C25A8 [u64 0x0000000001CCDD74]
0019B32D  call     qword ptr [rip + 0x7272f5]  ; -> 008C2628 [u64 0x0000000001CCCE08]
0019B333  mov      rdi, rax
0019B336  mov      rax, qword ptr [rsi + 8]
0019B33A  cmp      rdi, qword ptr [rax + 0x18]
0019B33E  jae      0x19b353  ; -> 0019B353
0019B340  mov      rcx, qword ptr [rax + 0x10]
0019B344  mov      rbx, qword ptr [rcx + rdi*8]
0019B348  test     rbx, rbx
0019B34B  jne      0x19b3e1  ; -> 0019B3E1
0019B351  jmp      0x19b355  ; -> 0019B355
0019B353  xor      ebx, ebx
0019B355  cmp      byte ptr [rax + 0x24], 0
0019B359  je       0x19b36f  ; -> 0019B36F
0019B35B  call     qword ptr [rip + 0x7272cf]  ; -> 008C2630 [u64 0x0000000001CCCE26]
0019B361  cmp      rdi, qword ptr [rax + 0x18]
0019B365  jae      0x19b374  ; -> 0019B374
0019B367  mov      rax, qword ptr [rax + 0x10]
0019B36B  mov      rbx, qword ptr [rax + rdi*8]
0019B36F  test     rbx, rbx
0019B372  jne      0x19b3e1  ; -> 0019B3E1
0019B374  mov      rbx, qword ptr [rsp + 0x58]
0019B379  test     rbx, rbx
0019B37C  jne      0x19b3e1  ; -> 0019B3E1
0019B37E  mov      rdx, rsi
0019B381  lea      rcx, [rsp + 0x58]
0019B386  call     qword ptr [rip + 0x727404]  ; -> 008C2790 [u64 0x0000000001CCDA12]
0019B38C  cmp      rax, -1
0019B390  jne      0x19b3c3  ; -> 0019B3C3
0019B392  xor      eax, eax
0019B394  mov      qword ptr [rsp + 0x38], rax
0019B399  lea      rax, [rip + 0x758288]  ; -> 008F3628 [str "bad cast"]
0019B3A0  mov      qword ptr [rsp + 0x30], rax
0019B3A5  lea      rax, [rip + 0x75826c]  ; -> 008F3618
0019B3AC  mov      qword ptr [rsp + 0x28], rax
0019B3B1  lea      rdx, [rip + 0x1c4f6e8]  ; -> 01DEAAA0
0019B3B8  lea      rcx, [rsp + 0x28]
0019B3BD  call     0x861ecc  ; -> 00861ECC fn
0019B3C2  int3     
0019B3C3  mov      rbx, qword ptr [rsp + 0x58]
0019B3C8  mov      qword ptr [rip + 0x1de5d79], rbx  ; -> 01F81148
0019B3CF  mov      rax, qword ptr [rbx]
0019B3D2  mov      rcx, rbx
0019B3D5  call     qword ptr [rax + 8]
0019B3D8  mov      rcx, rbx
0019B3DB  call     0x808850  ; -> 00808850 fn
0019B3E0  nop      
0019B3E1  lea      rcx, [rsp + 0x50]
0019B3E6  call     qword ptr [rip + 0x72720c]  ; -> 008C25F8 [u64 0x0000000001CCCD48]
0019B3EC  mov      rax, rbx
0019B3EF  mov      rbx, qword ptr [rsp + 0x60]
0019B3F4  mov      rsi, qword ptr [rsp + 0x68]
0019B3F9  add      rsp, 0x40
0019B3FD  pop      rdi
```

## 001DE200 (116 B, extent 001DE200-001DE274)

Documented callee on this page: `001DF8C0`

```
001DE200  mov      qword ptr [rsp + 8], rbx
001DE205  push     rdi
001DE206  sub      rsp, 0x20
001DE20A  mov      rax, qword ptr [rcx - 0x88]
001DE211  mov      rdi, rcx
001DE214  movsxd   rdx, dword ptr [rax + 4]
001DE218  lea      rax, [rip + 0x722e71]  ; -> 00901090
001DE21F  mov      qword ptr [rdx + rcx - 0x88], rax
001DE227  mov      rax, qword ptr [rcx - 0x88]
001DE22E  movsxd   rdx, dword ptr [rax + 4]
001DE232  lea      rax, [rip + 0x722ce7]  ; -> 00900F20
001DE239  lea      r8d, [rdx - 0x88]
001DE240  mov      dword ptr [rdx + rcx - 0x8c], r8d
001DE248  mov      qword ptr [rcx - 0x80], rax
001DE24C  add      rcx, -0x80
001DE250  call     0x1df8c0  ; -> 001DF8C0 fn
001DE255  lea      rcx, [rdi - 0x80]
001DE259  call     qword ptr [rip + 0x6e4541]  ; -> 008C27A0 [u64 0x0000000001CCDA9C]
001DE25F  lea      rcx, [rdi - 0x78]
001DE263  mov      rbx, qword ptr [rsp + 0x30]
001DE268  add      rsp, 0x20
001DE26C  pop      rdi
001DE26D  jmp      qword ptr [rip + 0x6e435c]  ; -> 008C25D0 [u64 0x0000000001CCDC3C]
```

## 008A4BAB (23 B, extent 008A4BAB-008A4BC2)

Documented callee on this page: `00861ECC`

```
008A4BAB  mov      qword ptr [rsp + 0x10], rdx
008A4BB0  push     rbp
008A4BB1  sub      rsp, 0x20
008A4BB5  mov      rbp, rdx
008A4BB8  xor      edx, edx
008A4BBA  xor      ecx, ecx
008A4BBC  call     0x861ecc  ; -> 00861ECC fn
008A4BC1  nop      
```

## 008B90A0 (105 B, extent 008B90A0-008B9109)

Documented callee on this page: `0085E710`

```
008B90A0  push     rbp
008B90A2  sub      rsp, 0x50
008B90A6  mov      qword ptr [rsp + 0x40], 0xfffffffffffffffe
008B90AF  lea      rbp, [rsp + 0x40]
008B90B4  and      rbp, 0xffffffffffffffe0
008B90B8  lea      rax, [rip + 0x1416289]  ; -> 01CCF348
008B90BF  mov      qword ptr [rip + 0x25f633a], rax  ; -> 02EAF400
008B90C6  mov      rcx, qword ptr [rip + 0x25f6553]  ; -> 02EAF620
008B90CD  test     rcx, rcx
008B90D0  je       0x8b90e0  ; -> 008B90E0
008B90D2  cmp      byte ptr [rip + 0x25f654f], 0  ; -> 02EAF628
008B90D9  je       0x8b90e0  ; -> 008B90E0
008B90DB  call     0x85e710  ; -> 0085E710 fn
008B90E0  mov      byte ptr [rip + 0x25f6541], 1  ; -> 02EAF628
008B90E7  xor      eax, eax
008B90E9  mov      qword ptr [rip + 0x25f6530], rax  ; -> 02EAF620
008B90F0  mov      qword ptr [rip + 0x25f651d], rax  ; -> 02EAF614
008B90F7  lea      rcx, [rip + 0x25f6302]  ; -> 02EAF400
008B90FE  call     0x839fd0  ; -> 00839FD0 fn
008B9103  add      rsp, 0x50
008B9107  pop      rbp
008B9108  ret      
```
