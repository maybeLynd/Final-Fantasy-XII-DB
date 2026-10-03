# F homing pack (FABLE): `00-Engine-Core-Runtime/Application-Root/game-application.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 6. No bearing page cites them and no documented function calls them directly.

## 006A7800 (82 B, extent 006A7800-006A7852)

Documented callee on this page: `00584730`

```
006A7800  push     rbx
006A7802  sub      rsp, 0x20
006A7806  mov      rbx, rcx
006A7809  test     dl, 1
006A780C  je       0x6a7819  ; -> 006A7819
006A780E  mov      eax, 5
006A7813  add      rsp, 0x20
006A7817  pop      rbx
006A7818  ret      
006A7819  mov      qword ptr [rsp + 0x30], rdi
006A781E  test     rdx, rdx
006A7821  je       0x6a7829  ; -> 006A7829
006A7823  lea      rdi, [rdx + 1]
006A7827  jmp      0x6a782b  ; -> 006A782B
006A7829  xor      edi, edi
006A782B  mov      rcx, qword ptr [rcx]
006A782E  test     rcx, rcx
006A7831  je       0x6a7842  ; -> 006A7842
006A7833  movzx    edx, cl
006A7836  not      dl
006A7838  test     dl, 1
006A783B  je       0x6a7842  ; -> 006A7842
006A783D  call     0x584730  ; -> 00584730 fn
006A7842  mov      qword ptr [rbx], rdi
006A7845  xor      eax, eax
006A7847  mov      rdi, qword ptr [rsp + 0x30]
006A784C  add      rsp, 0x20
006A7850  pop      rbx
006A7851  ret      
```

## 006A7940 (72 B, extent 006A7940-006A7988)

Documented callee on this page: `00584730`

```
006A7940  push     rbx
006A7942  sub      rsp, 0x30
006A7946  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006A794F  mov      rbx, rdx
006A7952  mov      ecx, dword ptr [rdx + 8]
006A7955  mov      eax, ecx
006A7957  shr      eax, 0x1f
006A795A  not      al
006A795C  test     al, 1
006A795E  je       0x6a7977  ; -> 006A7977
006A7960  btr      ecx, 0x1f
006A7964  cmp      ecx, 1
006A7967  jbe      0x6a7977  ; -> 006A7977
006A7969  mov      rcx, qword ptr [rdx + 0x10]
006A796D  test     rcx, rcx
006A7970  je       0x6a7977  ; -> 006A7977
006A7972  call     0x584730  ; -> 00584730 fn
006A7977  xor      eax, eax
006A7979  mov      qword ptr [rbx + 0x10], rax
006A797D  mov      dword ptr [rbx + 8], eax
006A7980  mov      al, 1
006A7982  add      rsp, 0x30
006A7986  pop      rbx
006A7987  ret      
```

## 006AB600 (120 B, extent 006AB600-006AB678)

Documented callee on this page: `00808C40`

```
006AB600  mov      r11, rsp
006AB603  mov      qword ptr [r11 + 0x10], rdx
006AB607  mov      qword ptr [r11 + 0x18], r8
006AB60B  mov      qword ptr [r11 + 0x20], r9
006AB60F  push     rbx
006AB610  sub      rsp, 0x60
006AB614  mov      rax, qword ptr [rip + 0x1899215]  ; -> 01F44830 [u64 0x00002B992DDFA232]
006AB61B  xor      rax, rsp
006AB61E  mov      qword ptr [rsp + 0x58], rax
006AB623  mov      rcx, qword ptr [rcx + 0x28]
006AB627  lea      rax, [r11 - 0x30]
006AB62B  neg      eax
006AB62D  lea      rbx, [r11 - 0x30]
006AB631  and      eax, 0xf
006AB634  add      rbx, rax
006AB637  lea      rax, [r11 + 0x18]
006AB63B  mov      qword ptr [r11 - 0x38], rax
006AB63F  test     rcx, rcx
006AB642  je       0x6ab661  ; -> 006AB661
006AB644  mov      r10, qword ptr [rcx]
006AB647  lea      rax, [r11 - 0x38]
006AB64B  lea      r8, [rip + 0x2794e5e]  ; -> 02E404B0
006AB652  mov      qword ptr [r11 - 0x48], rax
006AB656  or       r8, 1
006AB65A  mov      r9, rbx
006AB65D  call     qword ptr [r10 + 0x10]
006AB661  mov      rax, qword ptr [rbx + 8]
006AB665  mov      rcx, qword ptr [rsp + 0x58]
006AB66A  xor      rcx, rsp
006AB66D  call     0x808c40  ; -> 00808C40 fn
006AB672  add      rsp, 0x60
006AB676  pop      rbx
006AB677  ret      
```

## 006AC770 (111 B, extent 006AC770-006AC7DF)

Documented callee on this page: `0080929C`

```
006AC770  sub      rsp, 0x28
006AC774  mov      rax, qword ptr gs:[0x58]
006AC77D  mov      ecx, dword ptr [rip + 0x28025b9]  ; -> 02EAED3C
006AC783  mov      edx, 4
006AC788  mov      rcx, qword ptr [rax + rcx*8]
006AC78C  mov      eax, dword ptr [rdx + rcx]
006AC78F  cmp      dword ptr [rip + 0x27a281b], eax  ; -> 02E4EFB0
006AC795  jg       0x6ac7a3  ; -> 006AC7A3
006AC797  lea      rax, [rip + 0x27a2802]  ; -> 02E4EFA0
006AC79E  add      rsp, 0x28
006AC7A2  ret      
006AC7A3  lea      rcx, [rip + 0x27a2806]  ; -> 02E4EFB0
006AC7AA  call     0x8092fc  ; -> 008092FC fn
006AC7AF  cmp      dword ptr [rip + 0x27a27fa], -1  ; -> 02E4EFB0
006AC7B6  jne      0x6ac797  ; -> 006AC797
006AC7B8  lea      rax, [rip + 0x27a1c71]  ; -> 02E4E430
006AC7BF  mov      qword ptr [rip + 0x27a27de], 0  ; -> 02E4EFA8
006AC7CA  lea      rcx, [rip + 0x27a27df]  ; -> 02E4EFB0
006AC7D1  mov      qword ptr [rip + 0x27a27c8], rax  ; -> 02E4EFA0
006AC7D8  call     0x80929c  ; -> 0080929C fn
006AC7DD  jmp      0x6ac797  ; -> 006AC797
```

## 006ADC20 (69 B, extent 006ADC20-006ADC65)

Documented callee on this page: `00584730`

```
006ADC20  push     rbx
006ADC22  sub      rsp, 0x30
006ADC26  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006ADC2F  mov      rbx, rdx
006ADC32  mov      eax, dword ptr [rdx + 0x18]
006ADC35  shr      eax, 0x1f
006ADC38  not      al
006ADC3A  test     al, 1
006ADC3C  je       0x6adc4c  ; -> 006ADC4C
006ADC3E  mov      rcx, qword ptr [rdx + 0x20]
006ADC42  test     rcx, rcx
006ADC45  je       0x6adc4c  ; -> 006ADC4C
006ADC47  call     0x584730  ; -> 00584730 fn
006ADC4C  xor      eax, eax
006ADC4E  mov      qword ptr [rbx + 0x20], rax
006ADC52  mov      dword ptr [rbx + 0x18], eax
006ADC55  mov      rcx, rbx
006ADC58  call     0x6aaa50  ; -> 006AAA50 fn
006ADC5D  mov      al, 1
006ADC5F  add      rsp, 0x30
006ADC63  pop      rbx
006ADC64  ret      
```

## 006AF760 (87 B, extent 006AF760-006AF7B7)

Documented callee on this page: `00584730`

```
006AF760  mov      qword ptr [rsp + 8], rbx
006AF765  mov      qword ptr [rsp + 0x10], rsi
006AF76A  push     rdi
006AF76B  sub      rsp, 0x20
006AF76F  mov      ebx, r8d
006AF772  mov      rsi, rdx
006AF775  mov      rdi, rcx
006AF778  test     r8d, r8d
006AF77B  js       0x6af7a5  ; -> 006AF7A5
006AF77D  mov      rcx, qword ptr [rcx + 8]
006AF781  mov      eax, dword ptr [rdi]
006AF783  cmp      rcx, rdx
006AF786  je       0x6af79b  ; -> 006AF79B
006AF788  shr      eax, 0x1f
006AF78B  not      al
006AF78D  test     al, 1
006AF78F  je       0x6af79b  ; -> 006AF79B
006AF791  test     rcx, rcx
006AF794  je       0x6af79b  ; -> 006AF79B
006AF796  call     0x584730  ; -> 00584730 fn
006AF79B  bts      ebx, 0x1f
006AF79F  mov      qword ptr [rdi + 8], rsi
006AF7A3  mov      dword ptr [rdi], ebx
006AF7A5  mov      rbx, qword ptr [rsp + 0x30]
006AF7AA  xor      eax, eax
006AF7AC  mov      rsi, qword ptr [rsp + 0x38]
006AF7B1  add      rsp, 0x20
006AF7B5  pop      rdi
006AF7B6  ret      
```
