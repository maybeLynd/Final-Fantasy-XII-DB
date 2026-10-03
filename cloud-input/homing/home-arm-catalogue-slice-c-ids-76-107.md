# Homing pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-C-ids-76-107.md`

Generated 2026-10-03 00:35 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-arm-catalogue-slice-c-ids-76-107.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001C1C80 (151 B, extent 001C1C80-001C1D17)

Entered from (direct sites whose caller this page cites): `001C2D50` + 0x34 (call; `001C2D50` is cited on this page)
Other direct sites: `001C2790` + 0x5B (call); `001C2790` + 0x118 (call)

Host context: "s 2.0 ('01CEBC08'); otherwise returns without writing | Interior anchor '001C2D18'; Interior anchor '001C2D26'; Interior anchor '001C2D2E'; Interior anchor '001C2D3F'; Interior anchor '001C2D47' | | '001C2D50' | 83 B | '001C2980' + 0x23C | when qword 'rcx+8' is below qword 'rcx+0x10' (unsigned), advances '+8' by 0x230 and, when the old value is non-null, calls '001C2D50' + 0x34 with it in 'rcx' and the incoming 'rdx'; otherwise tail-jum"

```
001C1C80  push     rbx
001C1C82  sub      rsp, 0x20
001C1C86  mov      eax, dword ptr [rdx]
001C1C88  lea      r8, [rdx + 8]
001C1C8C  mov      dword ptr [rcx], eax
001C1C8E  mov      rbx, rcx
001C1C91  mov      eax, dword ptr [rdx + 4]
001C1C94  mov      dword ptr [rcx + 4], eax
001C1C97  lea      rax, [rcx + 8]
001C1C9B  mov      ecx, 2
001C1CA0  lea      rax, [rax + 0x80]
001C1CA7  movups   xmm0, xmmword ptr [r8]
001C1CAB  lea      r8, [r8 + 0x80]
001C1CB2  movups   xmmword ptr [rax - 0x80], xmm0
001C1CB6  movups   xmm1, xmmword ptr [r8 - 0x70]
001C1CBB  movups   xmmword ptr [rax - 0x70], xmm1
001C1CBF  movups   xmm0, xmmword ptr [r8 - 0x60]
001C1CC4  movups   xmmword ptr [rax - 0x60], xmm0
001C1CC8  movups   xmm1, xmmword ptr [r8 - 0x50]
001C1CCD  movups   xmmword ptr [rax - 0x50], xmm1
001C1CD1  movups   xmm0, xmmword ptr [r8 - 0x40]
001C1CD6  movups   xmmword ptr [rax - 0x40], xmm0
001C1CDA  movups   xmm1, xmmword ptr [r8 - 0x30]
001C1CDF  movups   xmmword ptr [rax - 0x30], xmm1
001C1CE3  movups   xmm0, xmmword ptr [r8 - 0x20]
001C1CE8  movups   xmmword ptr [rax - 0x20], xmm0
001C1CEC  movups   xmm1, xmmword ptr [r8 - 0x10]
001C1CF1  movups   xmmword ptr [rax - 0x10], xmm1
001C1CF5  sub      rcx, 1
001C1CF9  jne      0x1c1ca0  ; -> 001C1CA0
001C1CFB  add      rdx, 0x108
001C1D02  lea      rcx, [rbx + 0x108]
001C1D09  call     0x1c1e70  ; -> 001C1E70 fn
001C1D0E  mov      rax, rbx
001C1D11  add      rsp, 0x20
001C1D15  pop      rbx
001C1D16  ret      
```

## 001C2790 (484 B, extent 001C2790-001C2974)

Entered from (direct sites whose caller this page cites): `001C2D50` + 0x49 (jmp; `001C2D50` is cited on this page)
Other direct sites: none

Host context: "s 2.0 ('01CEBC08'); otherwise returns without writing | Interior anchor '001C2D18'; Interior anchor '001C2D26'; Interior anchor '001C2D2E'; Interior anchor '001C2D3F'; Interior anchor '001C2D47' | | '001C2D50' | 83 B | '001C2980' + 0x23C | when qword 'rcx+8' is below qword 'rcx+0x10' (unsigned), advances '+8' by 0x230 and, when the old value is non-null, calls '001C2D50' + 0x34 with it in 'rcx' and the incoming 'rdx'; otherwise tail-jum"

```
001C2790  mov      rax, rsp
001C2793  mov      qword ptr [rax + 8], rcx
001C2797  push     rsi
001C2798  push     rdi
001C2799  push     r12
001C279B  push     r14
001C279D  push     r15
001C279F  sub      rsp, 0x40
001C27A3  mov      qword ptr [rax - 0x38], 0xfffffffffffffffe
001C27AB  mov      qword ptr [rax + 0x10], rbx
001C27AF  mov      qword ptr [rax + 0x18], rbp
001C27B3  mov      rdi, r8
001C27B6  mov      rbp, rdx
001C27B9  mov      rsi, rcx
001C27BC  mov      rcx, qword ptr [rcx + 8]
001C27C0  cmp      rcx, qword ptr [rsi + 0x10]
001C27C4  je       0x1c281c  ; -> 001C281C
001C27C6  cmp      r8, rdx
001C27C9  jb       0x1c27d7  ; -> 001C27D7
001C27CB  cmp      r8, rcx
001C27CE  jae      0x1c27d7  ; -> 001C27D7
001C27D0  add      rdi, 0x230
001C27D7  mov      qword ptr [rsp + 0x88], rcx
001C27DF  test     rcx, rcx
001C27E2  je       0x1c27f1  ; -> 001C27F1
001C27E4  lea      rdx, [rcx - 0x230]
001C27EB  call     0x1c1c80  ; -> 001C1C80 fn
001C27F0  nop      
001C27F1  mov      r8, qword ptr [rsi + 8]
001C27F5  lea      rdx, [r8 - 0x230]
001C27FC  mov      rcx, rbp
001C27FF  call     0x1c1a60  ; -> 001C1A60 fn
001C2804  mov      rdx, rdi
001C2807  mov      rcx, rbp
001C280A  call     0x1c2230  ; -> 001C2230 fn
001C280F  add      qword ptr [rsi + 8], 0x230
001C2817  jmp      0x1c295a  ; -> 001C295A
001C281C  sub      rcx, qword ptr [rsi]
001C281F  movabs   r12, 0xea0ea0ea0ea0ea1
001C2829  mov      rax, r12
001C282C  imul     rcx
001C282F  sar      rdx, 5
001C2833  mov      rax, rdx
001C2836  shr      rax, 0x3f
001C283A  add      rdx, rax
001C283D  test     edx, edx
001C283F  je       0x1c284f  ; -> 001C284F
001C2841  lea      r14d, [rdx + rdx]
001C2845  test     r14d, r14d
001C2848  jne      0x1c2855  ; -> 001C2855
001C284A  xor      r15d, r15d
001C284D  jmp      0x1c286f  ; -> 001C286F
001C284F  mov      r14d, 1
001C2855  mov      eax, r14d
001C2858  imul     rdx, rax, 0x230
001C285F  lea      rcx, [rsi + 0x18]
001C2863  mov      rax, qword ptr [rcx]
001C2866  xor      r8d, r8d
001C2869  call     qword ptr [rax + 0x10]
001C286C  mov      r15, rax
001C286F  movzx    eax, byte ptr [rsp + 0x70]
001C2874  mov      byte ptr [rsp + 0x20], al
001C2878  mov      r9, r15
001C287B  mov      r8, rbp
001C287E  mov      rdx, qword ptr [rsi]
001C2881  lea      rcx, [rsp + 0x70]
001C2886  call     0x1c1b00  ; -> 001C1B00 fn
001C288B  mov      rbx, qword ptr [rsp + 0x70]
001C2890  mov      qword ptr [rsp + 0x70], rbx
001C2895  mov      qword ptr [rsp + 0x88], rbx
001C289D  test     rbx, rbx
001C28A0  je       0x1c28ae  ; -> 001C28AE
001C28A2  mov      rdx, rdi
001C28A5  mov      rcx, rbx
001C28A8  call     0x1c1c80  ; -> 001C1C80 fn
001C28AD  nop      
001C28AE  lea      r9, [rbx + 0x230]
001C28B5  mov      qword ptr [rsp + 0x70], r9
001C28BA  movzx    eax, byte ptr [rsp + 0x70]
001C28BF  mov      byte ptr [rsp + 0x20], al
001C28C3  mov      r8, qword ptr [rsi + 8]
001C28C7  mov      rdx, rbp
001C28CA  lea      rcx, [rsp + 0x70]
001C28CF  call     0x1c1b00  ; -> 001C1B00 fn
001C28D4  mov      rbx, qword ptr [rsp + 0x70]
001C28D9  mov      qword ptr [rsp + 0x70], rbx
001C28DE  mov      rbp, qword ptr [rsi + 8]
001C28E2  mov      rdi, qword ptr [rsi]
001C28E5  cmp      rdi, rbp
001C28E8  jae      0x1c2908  ; -> 001C2908
001C28EA  nop      word ptr [rax + rax]
001C28F0  lea      rcx, [rdi + 0x108]
001C28F7  call     0x1ea180  ; -> 001EA180 fn
001C28FC  add      rdi, 0x230
001C2903  cmp      rdi, rbp
001C2906  jb       0x1c28f0  ; -> 001C28F0
001C2908  mov      r10, qword ptr [rsi]
001C290B  test     r10, r10
001C290E  je       0x1c2942  ; -> 001C2942
001C2910  lea      rcx, [rsi + 0x18]
001C2914  mov      r9, qword ptr [rcx]
001C2917  mov      r8, qword ptr [rsi + 0x10]
001C291B  sub      r8, r10
001C291E  mov      rax, r12
001C2921  imul     r8
001C2924  sar      rdx, 5
001C2928  mov      rax, rdx
001C292B  shr      rax, 0x3f
001C292F  add      rax, rdx
001C2932  mov      eax, eax
001C2934  imul     r8, rax, 0x230
001C293B  mov      rdx, r10
001C293E  call     qword ptr [r9 + 0x18]
001C2942  mov      qword ptr [rsi], r15
001C2945  mov      qword ptr [rsi + 8], rbx
001C2949  mov      eax, r14d
001C294C  imul     rcx, rax, 0x230
001C2953  add      rcx, r15
001C2956  mov      qword ptr [rsi + 0x10], rcx
001C295A  mov      rbx, qword ptr [rsp + 0x78]
001C295F  mov      rbp, qword ptr [rsp + 0x80]
001C2967  add      rsp, 0x40
001C296B  pop      r15
001C296D  pop      r14
001C296F  pop      r12
001C2971  pop      rdi
001C2972  pop      rsi
001C2973  ret      
```
