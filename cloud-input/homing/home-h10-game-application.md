# Homing pack: `00-Engine-Core-Runtime/Application-Root/game-application.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-game-application.json`.

Bodies: 16. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0019D050 (165 B, extent 0019D050-0019D0F5)

Entered from (direct sites whose caller this page cites): `0019ED80` + 0x88 (call; `0019ED80` is cited on this page)
Other direct sites: none

Host context: "cookie from qword '01F44830' is checked by '00808C40' | Interior anchor '0019ECA0'; Interior anchor '0019ECB3'; Interior anchor '0019ED11'; Interior anchor '0019ED43'; Interior anchor '0019ED56' | | '0019ED80' | 208 B | computes 'n' = (qword '[rcx+8]' minus qword '[rcx]') / 0x118 (signed); when 'edx' is above 'n' (unsigned, 32-bit) zeroes a 0x118-byte local with '00861EC0(local, 0, 0x118)' and calls '0019ED80'+0x6E('rcx', old qword '[rc"

```
0019D050  mov      r11, r8
0019D053  mov      r10, rcx
0019D056  cmp      rcx, rdx
0019D059  je       0x19d0f1  ; -> 0019D0F1
0019D05F  nop      
0019D060  mov      r9, r11
0019D063  mov      rax, r10
0019D066  mov      r8d, 2
0019D06C  nop      dword ptr [rax]
0019D070  lea      r9, [r9 + 0x80]
0019D077  movups   xmm0, xmmword ptr [rax]
0019D07A  lea      rax, [rax + 0x80]
0019D081  movups   xmmword ptr [r9 - 0x80], xmm0
0019D086  movups   xmm1, xmmword ptr [rax - 0x70]
0019D08A  movups   xmmword ptr [r9 - 0x70], xmm1
0019D08F  movups   xmm0, xmmword ptr [rax - 0x60]
0019D093  movups   xmmword ptr [r9 - 0x60], xmm0
0019D098  movups   xmm1, xmmword ptr [rax - 0x50]
0019D09C  movups   xmmword ptr [r9 - 0x50], xmm1
0019D0A1  movups   xmm0, xmmword ptr [rax - 0x40]
0019D0A5  movups   xmmword ptr [r9 - 0x40], xmm0
0019D0AA  movups   xmm1, xmmword ptr [rax - 0x30]
0019D0AE  movups   xmmword ptr [r9 - 0x30], xmm1
0019D0B3  movups   xmm0, xmmword ptr [rax - 0x20]
0019D0B7  movups   xmmword ptr [r9 - 0x20], xmm0
0019D0BC  movups   xmm1, xmmword ptr [rax - 0x10]
0019D0C0  movups   xmmword ptr [r9 - 0x10], xmm1
0019D0C5  sub      r8, 1
0019D0C9  jne      0x19d070  ; -> 0019D070
0019D0CB  movups   xmm0, xmmword ptr [rax]
0019D0CE  add      r11, 0x118
0019D0D5  add      r10, 0x118
0019D0DC  movups   xmmword ptr [r9], xmm0
0019D0E0  mov      rcx, qword ptr [rax + 0x10]
0019D0E4  mov      qword ptr [r9 + 0x10], rcx
0019D0E8  cmp      r10, rdx
0019D0EB  jne      0x19d060  ; -> 0019D060
0019D0F1  mov      rax, r11
0019D0F4  ret      
```

## 0019E2C0 (1139 B, extent 0019E2C0-0019E733)

Entered from (direct sites whose caller this page cites): `0019ED80` + 0x6E (call; `0019ED80` is cited on this page)
Other direct sites: none

Host context: "cookie from qword '01F44830' is checked by '00808C40' | Interior anchor '0019ECA0'; Interior anchor '0019ECB3'; Interior anchor '0019ED11'; Interior anchor '0019ED43'; Interior anchor '0019ED56' | | '0019ED80' | 208 B | computes 'n' = (qword '[rcx+8]' minus qword '[rcx]') / 0x118 (signed); when 'edx' is above 'n' (unsigned, 32-bit) zeroes a 0x118-byte local with '00861EC0(local, 0, 0x118)' and calls '0019ED80'+0x6E('rcx', old qword '[rc"

```
0019E2C0  mov      qword ptr [rsp + 0x10], rbx
0019E2C5  mov      qword ptr [rsp + 0x20], rbp
0019E2CA  push     rsi
0019E2CB  push     rdi
0019E2CC  push     r12
0019E2CE  push     r14
0019E2D0  push     r15
0019E2D2  sub      rsp, 0x150
0019E2D9  mov      rdi, qword ptr [rcx + 8]
0019E2DD  mov      rbp, rdx
0019E2E0  mov      rdx, qword ptr [rcx + 0x10]
0019E2E4  movabs   r12, 0xea0ea0ea0ea0ea1
0019E2EE  sub      rdx, rdi
0019E2F1  mov      r15d, r8d
0019E2F4  mov      rax, r12
0019E2F7  mov      rbx, r9
0019E2FA  imul     rdx
0019E2FD  mov      r14, rcx
0019E300  sar      rdx, 4
0019E304  mov      rax, rdx
0019E307  shr      rax, 0x3f
0019E30B  add      rdx, rax
0019E30E  cmp      r8d, edx
0019E311  ja       0x19e602  ; -> 0019E602
0019E317  test     r8d, r8d
0019E31A  je       0x19e717  ; -> 0019E717
0019E320  lea      rdx, [rsp + 0x30]
0019E325  mov      ecx, 2
0019E32A  nop      word ptr [rax + rax]
0019E330  lea      rdx, [rdx + 0x80]
0019E337  movups   xmm0, xmmword ptr [rbx]
0019E33A  movups   xmm1, xmmword ptr [rbx + 0x10]
0019E33E  lea      rbx, [rbx + 0x80]
0019E345  movups   xmmword ptr [rdx - 0x80], xmm0
0019E349  movups   xmm0, xmmword ptr [rbx - 0x60]
0019E34D  movups   xmmword ptr [rdx - 0x70], xmm1
0019E351  movups   xmm1, xmmword ptr [rbx - 0x50]
0019E355  movups   xmmword ptr [rdx - 0x60], xmm0
0019E359  movups   xmm0, xmmword ptr [rbx - 0x40]
0019E35D  movups   xmmword ptr [rdx - 0x50], xmm1
0019E361  movups   xmm1, xmmword ptr [rbx - 0x30]
0019E365  movups   xmmword ptr [rdx - 0x40], xmm0
0019E369  movups   xmm0, xmmword ptr [rbx - 0x20]
0019E36D  movups   xmmword ptr [rdx - 0x30], xmm1
0019E371  movups   xmm1, xmmword ptr [rbx - 0x10]
0019E375  movups   xmmword ptr [rdx - 0x20], xmm0
0019E379  movups   xmmword ptr [rdx - 0x10], xmm1
0019E37D  sub      rcx, 1
0019E381  jne      0x19e330  ; -> 0019E330
0019E383  mov      rcx, qword ptr [rbx + 0x10]
0019E387  mov      rax, r12
0019E38A  movups   xmm0, xmmword ptr [rbx]
0019E38D  movups   xmmword ptr [rdx], xmm0
0019E390  mov      qword ptr [rdx + 0x10], rcx
0019E394  mov      rcx, rdi
0019E397  sub      rcx, rbp
0019E39A  imul     rcx
0019E39D  mov      rbx, rdx
0019E3A0  sar      rbx, 4
0019E3A4  mov      rax, rbx
0019E3A7  shr      rax, 0x3f
0019E3AB  add      rbx, rax
0019E3AE  cmp      r15d, ebx
0019E3B1  jae      0x19e492  ; -> 0019E492
0019E3B7  movzx    eax, byte ptr [rsp + 0x190]
0019E3BF  lea      rcx, [rsp + 0x180]
0019E3C7  imul     rsi, r15, 0x118
0019E3CE  mov      rbx, rdi
0019E3D1  mov      byte ptr [rsp + 0x20], al
0019E3D5  sub      rbx, rsi
0019E3D8  mov      r9, rdi
0019E3DB  mov      rdx, rbx
0019E3DE  mov      r8, rdi
0019E3E1  call     0x19d350  ; -> 0019D350 fn
0019E3E6  add      qword ptr [r14 + 8], rsi
0019E3EA  mov      r8, rdi
0019E3ED  mov      rdx, rbx
0019E3F0  mov      rcx, rbp
0019E3F3  call     0x19cfa0  ; -> 0019CFA0 fn
0019E3F8  lea      r8, [rsi + rbp]
0019E3FC  cmp      rbp, r8
0019E3FF  je       0x19e717  ; -> 0019E717
0019E405  nop      word ptr [rax + rax]
0019E410  mov      rcx, rbp
0019E413  lea      rax, [rsp + 0x30]
0019E418  mov      edx, 2
0019E41D  nop      dword ptr [rax]
0019E420  lea      rcx, [rcx + 0x80]
0019E427  movups   xmm0, xmmword ptr [rax]
0019E42A  movups   xmm1, xmmword ptr [rax + 0x10]
0019E42E  lea      rax, [rax + 0x80]
0019E435  movups   xmmword ptr [rcx - 0x80], xmm0
0019E439  movups   xmm0, xmmword ptr [rax - 0x60]
0019E43D  movups   xmmword ptr [rcx - 0x70], xmm1
0019E441  movups   xmm1, xmmword ptr [rax - 0x50]
0019E445  movups   xmmword ptr [rcx - 0x60], xmm0
0019E449  movups   xmm0, xmmword ptr [rax - 0x40]
0019E44D  movups   xmmword ptr [rcx - 0x50], xmm1
0019E451  movups   xmm1, xmmword ptr [rax - 0x30]
0019E455  movups   xmmword ptr [rcx - 0x40], xmm0
0019E459  movups   xmm0, xmmword ptr [rax - 0x20]
0019E45D  movups   xmmword ptr [rcx - 0x30], xmm1
0019E461  movups   xmm1, xmmword ptr [rax - 0x10]
0019E465  movups   xmmword ptr [rcx - 0x20], xmm0
0019E469  movups   xmmword ptr [rcx - 0x10], xmm1
0019E46D  sub      rdx, 1
0019E471  jne      0x19e420  ; -> 0019E420
0019E473  movups   xmm0, xmmword ptr [rax]
0019E476  mov      rax, qword ptr [rax + 0x10]
0019E47A  add      rbp, 0x118
0019E481  movups   xmmword ptr [rcx], xmm0
0019E484  mov      qword ptr [rcx + 0x10], rax
0019E488  cmp      rbp, r8
0019E48B  jne      0x19e410  ; -> 0019E410
0019E48D  jmp      0x19e717  ; -> 0019E717
0019E492  sub      r15d, ebx
0019E495  mov      rax, rdi
0019E498  mov      r9d, r15d
0019E49B  je       0x19e531  ; -> 0019E531
0019E4A1  test     rax, rax
0019E4A4  je       0x19e521  ; -> 0019E521
0019E4A6  mov      rdx, rax
0019E4A9  lea      rcx, [rsp + 0x30]
0019E4AE  mov      r8d, 2
0019E4B4  nop      dword ptr [rax]
0019E4B8  nop      dword ptr [rax + rax]
0019E4C0  lea      rdx, [rdx + 0x80]
0019E4C7  movups   xmm0, xmmword ptr [rcx]
0019E4CA  movups   xmm1, xmmword ptr [rcx + 0x10]
0019E4CE  lea      rcx, [rcx + 0x80]
0019E4D5  movups   xmmword ptr [rdx - 0x80], xmm0
0019E4D9  movups   xmm0, xmmword ptr [rcx - 0x60]
0019E4DD  movups   xmmword ptr [rdx - 0x70], xmm1
0019E4E1  movups   xmm1, xmmword ptr [rcx - 0x50]
0019E4E5  movups   xmmword ptr [rdx - 0x60], xmm0
0019E4E9  movups   xmm0, xmmword ptr [rcx - 0x40]
0019E4ED  movups   xmmword ptr [rdx - 0x50], xmm1
0019E4F1  movups   xmm1, xmmword ptr [rcx - 0x30]
0019E4F5  movups   xmmword ptr [rdx - 0x40], xmm0
0019E4F9  movups   xmm0, xmmword ptr [rcx - 0x20]
0019E4FD  movups   xmmword ptr [rdx - 0x30], xmm1
0019E501  movups   xmm1, xmmword ptr [rcx - 0x10]
0019E505  movups   xmmword ptr [rdx - 0x20], xmm0
0019E509  movups   xmmword ptr [rdx - 0x10], xmm1
0019E50D  sub      r8, 1
0019E511  jne      0x19e4c0  ; -> 0019E4C0
0019E513  movups   xmm0, xmmword ptr [rcx]
0019E516  mov      rcx, qword ptr [rcx + 0x10]
0019E51A  movups   xmmword ptr [rdx], xmm0
0019E51D  mov      qword ptr [rdx + 0x10], rcx
0019E521  add      rax, 0x118
0019E527  add      r9d, -1
0019E52B  jne      0x19e4a1  ; -> 0019E4A1
0019E531  mov      eax, r15d
0019E534  lea      rcx, [rsp + 0x180]
0019E53C  imul     r9, rax, 0x118
0019E543  movzx    eax, byte ptr [rsp + 0x190]
0019E54B  mov      r8, rdi
0019E54E  add      r9, qword ptr [r14 + 8]
0019E552  mov      rdx, rbp
0019E555  mov      qword ptr [r14 + 8], r9
0019E559  mov      byte ptr [rsp + 0x20], al
0019E55D  call     0x19d350  ; -> 0019D350 fn
0019E562  mov      eax, ebx
0019E564  imul     rcx, rax, 0x118
0019E56B  add      qword ptr [r14 + 8], rcx
0019E56F  cmp      rbp, rdi
0019E572  je       0x19e717  ; -> 0019E717
0019E578  nop      dword ptr [rax + rax]
0019E580  mov      rdx, rbp
0019E583  lea      rax, [rsp + 0x30]
0019E588  mov      ecx, 2
0019E58D  nop      dword ptr [rax]
0019E590  lea      rdx, [rdx + 0x80]
0019E597  movups   xmm0, xmmword ptr [rax]
0019E59A  movups   xmm1, xmmword ptr [rax + 0x10]
0019E59E  lea      rax, [rax + 0x80]
0019E5A5  movups   xmmword ptr [rdx - 0x80], xmm0
0019E5A9  movups   xmm0, xmmword ptr [rax - 0x60]
0019E5AD  movups   xmmword ptr [rdx - 0x70], xmm1
0019E5B1  movups   xmm1, xmmword ptr [rax - 0x50]
0019E5B5  movups   xmmword ptr [rdx - 0x60], xmm0
0019E5B9  movups   xmm0, xmmword ptr [rax - 0x40]
0019E5BD  movups   xmmword ptr [rdx - 0x50], xmm1
0019E5C1  movups   xmm1, xmmword ptr [rax - 0x30]
0019E5C5  movups   xmmword ptr [rdx - 0x40], xmm0
0019E5C9  movups   xmm0, xmmword ptr [rax - 0x20]
0019E5CD  movups   xmmword ptr [rdx - 0x30], xmm1
0019E5D1  movups   xmm1, xmmword ptr [rax - 0x10]
0019E5D5  movups   xmmword ptr [rdx - 0x20], xmm0
0019E5D9  movups   xmmword ptr [rdx - 0x10], xmm1
0019E5DD  sub      rcx, 1
0019E5E1  jne      0x19e590  ; -> 0019E590
0019E5E3  movups   xmm0, xmmword ptr [rax]
0019E5E6  mov      rcx, qword ptr [rax + 0x10]
0019E5EA  add      rbp, 0x118
0019E5F1  movups   xmmword ptr [rdx], xmm0
0019E5F4  mov      qword ptr [rdx + 0x10], rcx
0019E5F8  cmp      rbp, rdi
0019E5FB  jne      0x19e580  ; -> 0019E580
0019E5FD  jmp      0x19e717  ; -> 0019E717
0019E602  sub      rdi, qword ptr [rcx]
0019E605  mov      rax, r12
0019E608  imul     rdi
0019E60B  sar      rdx, 4
0019E60F  mov      rax, rdx
0019E612  shr      rax, 0x3f
0019E616  add      rdx, rax
0019E619  lea      eax, [rdx + rdx]
0019E61C  test     edx, edx
0019E61E  jne      0x19e625  ; -> 0019E625
0019E620  mov      eax, 1
0019E625  lea      edi, [rdx + r15]
0019E629  cmp      eax, edi
0019E62B  cmova    edi, eax
0019E62E  test     edi, edi
0019E630  je       0x19e64f  ; -> 0019E64F
0019E632  mov      r9, qword ptr [rcx + 0x18]
0019E636  add      rcx, 0x18
0019E63A  mov      eax, edi
0019E63C  xor      r8d, r8d
0019E63F  imul     rdx, rax, 0x118
0019E646  call     qword ptr [r9 + 0x10]
0019E64A  mov      rsi, rax
0019E64D  jmp      0x19e651  ; -> 0019E651
0019E64F  xor      esi, esi
0019E651  movzx    eax, byte ptr [rsp + 0x190]
0019E659  lea      rcx, [rsp + 0x180]
0019E661  mov      rdx, qword ptr [r14]
0019E664  mov      r9, rsi
0019E667  mov      r8, rbp
0019E66A  mov      byte ptr [rsp + 0x20], al
0019E66E  call     0x19d350  ; -> 0019D350 fn
0019E673  movzx    r9d, byte ptr [rsp + 0x190]
0019E67C  mov      r8, rbx
0019E67F  mov      rcx, qword ptr [rsp + 0x180]
0019E687  mov      edx, r15d
0019E68A  call     0x19d510  ; -> 0019D510 fn
0019E68F  movzx    eax, byte ptr [rsp + 0x190]
0019E697  lea      rcx, [rsp + 0x180]
0019E69F  mov      r8, qword ptr [r14 + 8]
0019E6A3  mov      rdx, rbp
0019E6A6  imul     r9, r15, 0x118
0019E6AD  mov      byte ptr [rsp + 0x20], al
0019E6B1  add      r9, qword ptr [rsp + 0x180]
0019E6B9  call     0x19d350  ; -> 0019D350 fn
0019E6BE  mov      r10, qword ptr [r14]
0019E6C1  test     r10, r10
0019E6C4  je       0x19e6f8  ; -> 0019E6F8
0019E6C6  mov      r8, qword ptr [r14 + 0x10]
0019E6CA  lea      rcx, [r14 + 0x18]
0019E6CE  mov      r9, qword ptr [rcx]
0019E6D1  sub      r8, r10
0019E6D4  mov      rax, r12
0019E6D7  imul     r8
0019E6DA  sar      rdx, 4
0019E6DE  mov      rax, rdx
0019E6E1  shr      rax, 0x3f
0019E6E5  add      rax, rdx
0019E6E8  mov      rdx, r10
0019E6EB  mov      eax, eax
0019E6ED  imul     r8, rax, 0x118
0019E6F4  call     qword ptr [r9 + 0x18]
0019E6F8  mov      rax, qword ptr [rsp + 0x180]
0019E700  mov      qword ptr [r14 + 8], rax
0019E704  mov      eax, edi
0019E706  imul     rcx, rax, 0x118
0019E70D  mov      qword ptr [r14], rsi
0019E710  add      rcx, rsi
0019E713  mov      qword ptr [r14 + 0x10], rcx
0019E717  lea      r11, [rsp + 0x150]
0019E71F  mov      rbx, qword ptr [r11 + 0x38]
0019E723  mov      rbp, qword ptr [r11 + 0x48]
0019E727  mov      rsp, r11
0019E72A  pop      r15
0019E72C  pop      r14
0019E72E  pop      r12
0019E730  pop      rdi
0019E731  pop      rsi
0019E732  ret      
```

## 0019EA20 (114 B, extent 0019EA20-0019EA92)

Entered from (direct sites whose caller this page cites): `0019EC40` + 0x116 (call; `0019EC40` is cited on this page)
Other direct sites: none

Host context: " with 'r' the result of the call at '0019E740' + 0x50 | Interior anchor '0019E750'; Interior anchor '0019E76B'; Interior anchor '0019E77A'; Interior anchor '0019E789'; Interior anchor '0019E79B' | | '0019EC40' | 320 B | computes 'n' = (qword '[rcx+8]' minus qword '[rcx]') / 0x130 (signed); when 'edx' is at most 'n' (unsigned, 32-bit) calls '0019EC40'+0x116('rcx', qword '[rcx]' + 'edx'*0x130); otherwise zeroes a 0x130-byte local with '00"

```
0019EA20  mov      qword ptr [rsp + 8], rbx
0019EA25  mov      qword ptr [rsp + 0x10], rsi
0019EA2A  push     rdi
0019EA2B  sub      rsp, 0x20
0019EA2F  mov      rbx, r8
0019EA32  mov      rsi, rdx
0019EA35  mov      r8, rdx
0019EA38  mov      rdi, rcx
0019EA3B  mov      rdx, qword ptr [rcx + 8]
0019EA3F  mov      rcx, rbx
0019EA42  call     0x19cef0  ; -> 0019CEF0 fn
0019EA47  mov      r8, qword ptr [rdi + 8]
0019EA4B  mov      rdx, rax
0019EA4E  mov      rcx, rdi
0019EA51  call     0x19df90  ; -> 0019DF90 fn
0019EA56  sub      rbx, rsi
0019EA59  movabs   rax, 0xf9435e50d79435e5
0019EA63  imul     rbx
0019EA66  mov      rbx, qword ptr [rsp + 0x30]
0019EA6B  sar      rdx, 3
0019EA6F  mov      rax, rdx
0019EA72  shr      rax, 0x3f
0019EA76  add      rdx, rax
0019EA79  imul     rax, rdx, 0x130
0019EA80  add      qword ptr [rdi + 8], rax
0019EA84  mov      rax, rsi
0019EA87  mov      rsi, qword ptr [rsp + 0x38]
0019EA8C  add      rsp, 0x20
0019EA90  pop      rdi
0019EA91  ret      
```

## 001A49C0 (394 B, extent 001A49C0-001A4B4A)

Entered from (direct sites whose caller this page cites): `008B1B10` + 0x1B (call; `008B1B10` is cited on this page)
Other direct sites: `008A69A0` + 0x1B (call)

Host context: "58]'-keyed once-init blocks ('008092FC'/'0080929C' on '02D3ECE0' and '02D3EC9C') lazily build the '02D3ECB0' tree - self-linked head, allocator vtable '008F6500' at '02D3ECD8', '00808B90'-registered '008B1B10'/'008B1C00' atexit teardowns - and the second guards the one-time '00677030' registration of '"/GameData/D3D11/ArtData/shared/idmaps.txt"' into '02D3ECA8'; the lookup builds its key with '001A5630', walks the tree under the '02D3E8"

```
001A49C0  test     rdx, rdx
001A49C3  je       0x1a4b49  ; -> 001A4B49
001A49C9  mov      qword ptr [rsp + 8], rcx
001A49CE  push     rsi
001A49CF  sub      rsp, 0x20
001A49D3  mov      qword ptr [rsp + 0x38], rbx
001A49D8  mov      rsi, rdx
001A49DB  mov      qword ptr [rsp + 0x40], rbp
001A49E0  mov      rax, rcx
001A49E3  mov      qword ptr [rsp + 0x48], rdi
001A49E8  nop      dword ptr [rax + rax]
001A49F0  mov      rdx, qword ptr [rsi]
001A49F3  mov      rcx, rax
001A49F6  call     0x1a49c0  ; -> 001A49C0 fn
001A49FB  mov      rbp, qword ptr [rsi + 8]
001A49FF  lea      rdi, [rsi + 0x20]
001A4A03  mov      rax, qword ptr [rdi + 0x38]
001A4A07  lea      rbx, [rdi + 0x20]
001A4A0B  cmp      rax, 0x10
001A4A0F  jb       0x1a4a54  ; -> 001A4A54
001A4A11  mov      rcx, qword ptr [rbx]
001A4A14  inc      rax
001A4A17  cmp      rax, 0x1000
001A4A1D  jb       0x1a4a4f  ; -> 001A4A4F
001A4A1F  test     cl, 0x1f
001A4A22  jne      0x1a4b12  ; -> 001A4B12
001A4A28  mov      rax, qword ptr [rcx - 8]
001A4A2C  cmp      rax, rcx
001A4A2F  jae      0x1a4b0b  ; -> 001A4B0B
001A4A35  sub      rcx, rax
001A4A38  cmp      rcx, 8
001A4A3C  jb       0x1a4b04  ; -> 001A4B04
001A4A42  cmp      rcx, 0x27
001A4A46  ja       0x1a4afd  ; -> 001A4AFD
001A4A4C  mov      rcx, rax
001A4A4F  call     0x210eb0  ; -> 00210EB0 fn
001A4A54  mov      qword ptr [rbx + 0x18], 0xf
001A4A5C  cmp      qword ptr [rbx + 0x18], 0x10
001A4A61  mov      qword ptr [rbx + 0x10], 0
001A4A69  jb       0x1a4a6e  ; -> 001A4A6E
001A4A6B  mov      rbx, qword ptr [rbx]
001A4A6E  mov      byte ptr [rbx], 0
001A4A71  mov      rax, qword ptr [rdi + 0x18]
001A4A75  cmp      rax, 0x10
001A4A79  jb       0x1a4ab6  ; -> 001A4AB6
001A4A7B  mov      rcx, qword ptr [rdi]
001A4A7E  inc      rax
001A4A81  cmp      rax, 0x1000
001A4A87  jb       0x1a4ab1  ; -> 001A4AB1
001A4A89  test     cl, 0x1f
001A4A8C  jne      0x1a4b2e  ; -> 001A4B2E
001A4A92  mov      rax, qword ptr [rcx - 8]
001A4A96  cmp      rax, rcx
001A4A99  jae      0x1a4b27  ; -> 001A4B27
001A4A9F  sub      rcx, rax
001A4AA2  cmp      rcx, 8
001A4AA6  jb       0x1a4b20  ; -> 001A4B20
001A4AA8  cmp      rcx, 0x27
001A4AAC  ja       0x1a4b19  ; -> 001A4B19
001A4AAE  mov      rcx, rax
001A4AB1  call     0x210eb0  ; -> 00210EB0 fn
001A4AB6  mov      qword ptr [rdi + 0x18], 0xf
001A4ABE  cmp      qword ptr [rdi + 0x18], 0x10
001A4AC3  mov      qword ptr [rdi + 0x10], 0
001A4ACB  jb       0x1a4ad0  ; -> 001A4AD0
001A4ACD  mov      rdi, qword ptr [rdi]
001A4AD0  mov      rcx, qword ptr [rsp + 0x30]
001A4AD5  mov      r8d, 0x60
001A4ADB  add      rcx, 0x30
001A4ADF  mov      byte ptr [rdi], 0
001A4AE2  mov      rdx, rsi
001A4AE5  mov      rax, qword ptr [rcx]
001A4AE8  call     qword ptr [rax + 0x18]
001A4AEB  mov      rsi, rbp
001A4AEE  test     rbp, rbp
001A4AF1  je       0x1a4b35  ; -> 001A4B35
001A4AF3  mov      rax, qword ptr [rsp + 0x30]
001A4AF8  jmp      0x1a49f0  ; -> 001A49F0
001A4AFD  call     qword ptr [rip + 0x71e2a5]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B03  int3     
001A4B04  call     qword ptr [rip + 0x71e29e]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B0A  int3     
001A4B0B  call     qword ptr [rip + 0x71e297]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B11  int3     
001A4B12  call     qword ptr [rip + 0x71e290]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B18  int3     
001A4B19  call     qword ptr [rip + 0x71e289]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B1F  int3     
001A4B20  call     qword ptr [rip + 0x71e282]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B26  int3     
001A4B27  call     qword ptr [rip + 0x71e27b]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B2D  int3     
001A4B2E  call     qword ptr [rip + 0x71e274]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B34  int3     
001A4B35  mov      rbp, qword ptr [rsp + 0x40]
001A4B3A  mov      rbx, qword ptr [rsp + 0x38]
001A4B3F  mov      rdi, qword ptr [rsp + 0x48]
001A4B44  add      rsp, 0x20
001A4B48  pop      rsi
001A4B49  ret      
```

## 001AAE70 (102 B, extent 001AAE70-001AAED6)

Entered from (direct sites whose caller this page cites): `001AD490` + 0x1E (call; `001AD490` is cited on this page)
Other direct sites: none

Host context: " '001AB570(rcx+8, end, pointer to 0)'); returns 'rcx' | Interior anchor '001AAC8E'; Interior anchor '001AAC9A'; Interior anchor '001AACB9'; Interior anchor '001AACD9'; Interior anchor '001AACE2' | | '001AD490' | 55 B | returns at once when 'rcx' is null; otherwise calls '001AD490'+0x16 and '001AD490'+0x1E with 'rcx', then '00809950(rcx, 0x48)' | Interior anchor '001AD493'; Interior anchor '001AD4A6'; Interior anchor '001AD4AE'; Interior"

```
001AAE70  push     rbx
001AAE72  sub      rsp, 0x30
001AAE76  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001AAE7F  mov      rbx, rcx
001AAE82  mov      r8, qword ptr [rcx + 8]
001AAE86  mov      rdx, qword ptr [rcx]
001AAE89  call     0x1ab350  ; -> 001AB350 fn
001AAE8E  nop      
001AAE8F  mov      r10, qword ptr [rbx]
001AAE92  test     r10, r10
001AAE95  je       0x1aaed0  ; -> 001AAED0
001AAE97  lea      rcx, [rbx + 0x18]
001AAE9B  mov      r9, qword ptr [rcx]
001AAE9E  mov      r8, qword ptr [rbx + 0x10]
001AAEA2  sub      r8, r10
001AAEA5  movabs   rax, 0x2aaaaaaaaaaaaaab
001AAEAF  imul     r8
001AAEB2  sar      rdx, 3
001AAEB6  mov      rax, rdx
001AAEB9  shr      rax, 0x3f
001AAEBD  add      rdx, rax
001AAEC0  lea      r8, [rdx + rdx*2]
001AAEC4  shl      r8, 4
001AAEC8  mov      rdx, r10
001AAECB  call     qword ptr [r9 + 0x18]
001AAECF  nop      
001AAED0  add      rsp, 0x30
001AAED4  pop      rbx
001AAED5  ret      
```

## 001ABD40 (229 B, extent 001ABD40-001ABE25)

Entered from (direct sites whose caller this page cites): `001AD490` + 0x16 (call; `001AD490` is cited on this page)
Other direct sites: none

Host context: " '001AB570(rcx+8, end, pointer to 0)'); returns 'rcx' | Interior anchor '001AAC8E'; Interior anchor '001AAC9A'; Interior anchor '001AACB9'; Interior anchor '001AACD9'; Interior anchor '001AACE2' | | '001AD490' | 55 B | returns at once when 'rcx' is null; otherwise calls '001AD490'+0x16 and '001AD490'+0x1E with 'rcx', then '00809950(rcx, 0x48)' | Interior anchor '001AD493'; Interior anchor '001AD4A6'; Interior anchor '001AD4AE'; Interior"

```
001ABD40  push     rdi
001ABD42  sub      rsp, 0x30
001ABD46  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001ABD4F  mov      qword ptr [rsp + 0x40], rbx
001ABD54  mov      qword ptr [rsp + 0x48], rsi
001ABD59  mov      rdi, rcx
001ABD5C  xor      r8d, r8d
001ABD5F  mov      rdx, qword ptr [rcx + 8]
001ABD63  sub      rdx, qword ptr [rcx]
001ABD66  movabs   r9, 0x2aaaaaaaaaaaaaab
001ABD70  mov      rax, r9
001ABD73  imul     rdx
001ABD76  sar      rdx, 3
001ABD7A  mov      rax, rdx
001ABD7D  shr      rax, 0x3f
001ABD81  add      rdx, rax
001ABD84  test     edx, edx
001ABD86  je       0x1abdcc  ; -> 001ABDCC
001ABD88  nop      dword ptr [rax + rax]
001ABD90  lea      rax, [r8 + r8*2]
001ABD94  shl      rax, 4
001ABD98  add      rax, qword ptr [rdi]
001ABD9B  cmp      byte ptr [rax + 0x28], 0
001ABD9F  je       0x1abda9  ; -> 001ABDA9
001ABDA1  mov      rcx, qword ptr [rax + 8]
001ABDA5  mov      qword ptr [rax + 0x10], rcx
001ABDA9  inc      r8d
001ABDAC  mov      rcx, qword ptr [rdi + 8]
001ABDB0  sub      rcx, qword ptr [rdi]
001ABDB3  mov      rax, r9
001ABDB6  imul     rcx
001ABDB9  sar      rdx, 3
001ABDBD  mov      rax, rdx
001ABDC0  shr      rax, 0x3f
001ABDC4  add      rdx, rax
001ABDC7  cmp      r8d, edx
001ABDCA  jb       0x1abd90  ; -> 001ABD90
001ABDCC  mov      rsi, qword ptr [rdi + 8]
001ABDD0  mov      rbx, qword ptr [rdi]
001ABDD3  cmp      rbx, rsi
001ABDD6  jae      0x1abe11  ; -> 001ABE11
001ABDD8  nop      dword ptr [rax + rax]
001ABDE0  mov      rdx, qword ptr [rbx + 8]
001ABDE4  test     rdx, rdx
001ABDE7  je       0x1abdff  ; -> 001ABDFF
001ABDE9  lea      rcx, [rbx + 0x20]
001ABDED  mov      rax, qword ptr [rcx]
001ABDF0  mov      r8, qword ptr [rcx - 8]
001ABDF4  sub      r8, rdx
001ABDF7  and      r8, 0xfffffffffffffff8
001ABDFB  call     qword ptr [rax + 0x18]
001ABDFE  nop      
001ABDFF  add      rbx, 0x30
001ABE03  cmp      rbx, rsi
001ABE06  jb       0x1abde0  ; -> 001ABDE0
001ABE08  mov      rax, qword ptr [rdi]
001ABE0B  mov      qword ptr [rdi + 8], rax
001ABE0F  jmp      0x1abe15  ; -> 001ABE15
001ABE11  mov      qword ptr [rdi + 8], rbx
001ABE15  mov      rbx, qword ptr [rsp + 0x40]
001ABE1A  mov      rsi, qword ptr [rsp + 0x48]
001ABE1F  add      rsp, 0x30
001ABE23  pop      rdi
001ABE24  ret      
```

## 001AD0C0 (112 B, extent 001AD0C0-001AD130)

Entered from (direct sites whose caller this page cites): `001AA840` + 0x9A (call; `001AA840` is cited on this page)
Other direct sites: none

Host context: "roes qword '+0x500', byte '+0x508' and dword '+0x510' | Interior anchor '001A6CF9'; Interior anchor '001A6CFF'; Interior anchor '001A6D27'; Interior anchor '001A6D41'; Interior anchor '001A6D5F' | | '001AA840' | 411 B | zeroes qwords 'rcx+0'/'+8'/'+0x10', calls '001EDF00(rcx+0x18, "EASTL vector" 008C5F58)' and stores qword 0 at '+0x28', qword 1 at '+0x30', dword 0 at '+0x38', dword 1 at '+0x3c', byte 1 at '+0x40', dword 0 at '+0x44' and"

```
001AD0C0  push     rdi
001AD0C2  sub      rsp, 0x30
001AD0C6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001AD0CF  mov      qword ptr [rsp + 0x48], rbx
001AD0D4  mov      rdi, rdx
001AD0D7  mov      rbx, qword ptr [rcx + 8]
001AD0DB  cmp      rbx, qword ptr [rcx + 0x10]
001AD0DF  jae      0x1ad11a  ; -> 001AD11A
001AD0E1  mov      qword ptr [rsp + 0x40], rbx
001AD0E6  lea      rax, [rbx + 0x30]
001AD0EA  mov      qword ptr [rcx + 8], rax
001AD0EE  mov      qword ptr [rsp + 0x50], rbx
001AD0F3  test     rbx, rbx
001AD0F6  je       0x1ad118  ; -> 001AD118
001AD0F8  mov      eax, dword ptr [rdx]
001AD0FA  mov      dword ptr [rbx], eax
001AD0FC  movzx    eax, word ptr [rdx + 4]
001AD100  mov      word ptr [rbx + 4], ax
001AD104  add      rdx, 8
001AD108  lea      rcx, [rbx + 8]
001AD10C  call     0x19d8d0  ; -> 0019D8D0 fn
001AD111  movzx    eax, byte ptr [rdi + 0x28]
001AD115  mov      byte ptr [rbx + 0x28], al
001AD118  jmp      0x1ad125  ; -> 001AD125
001AD11A  mov      r8, rdi
001AD11D  mov      rdx, rbx
001AD120  call     0x1ab8a0  ; -> 001AB8A0 fn
001AD125  mov      rbx, qword ptr [rsp + 0x48]
001AD12A  add      rsp, 0x30
001AD12E  pop      rdi
001AD12F  ret      
```

## 001B1A20 (228 B, extent 001B1A20-001B1B04)

Entered from (direct sites whose caller this page cites): `001AE010` + 0x4A (call; `001AE010` is cited on this page)
Other direct sites: none

Host context: " calls '001AD490'+0x16 and '001AD490'+0x1E with 'rcx', then '00809950(rcx, 0x48)' | Interior anchor '001AD493'; Interior anchor '001AD4A6'; Interior anchor '001AD4AE'; Interior anchor '001AD4BC' | | '001AE010' | 94 B | zeroes qwords 'rcx+0x38'/'+0x40'/'+0x48', calls '001EDF00(rcx+0x50, "EASTL vector" 008C5F58)' and '001AE010'+0x4A('rcx+0x38', 0x400); returns 'rcx' | Interior anchor '001AE036'; Interior anchor '001AE04C'; Interior anchor"

```
001B1A20  mov      qword ptr [rsp + 0x10], rbx
001B1A25  mov      qword ptr [rsp + 0x18], rbp
001B1A2A  push     rdi
001B1A2B  sub      rsp, 0x20
001B1A2F  mov      r8, qword ptr [rcx]
001B1A32  movabs   rbp, 0x2aaaaaaaaaaaaaab
001B1A3C  mov      r9, qword ptr [rcx + 0x10]
001B1A40  mov      rax, rbp
001B1A43  mov      edi, edx
001B1A45  sub      r9, r8
001B1A48  imul     r9
001B1A4B  mov      rbx, rcx
001B1A4E  sar      rdx, 3
001B1A52  mov      rax, rdx
001B1A55  shr      rax, 0x3f
001B1A59  add      rdx, rax
001B1A5C  cmp      edi, edx
001B1A5E  jbe      0x1b1af4  ; -> 001B1AF4
001B1A64  mov      r9, qword ptr [rcx + 8]
001B1A68  mov      edx, edi
001B1A6A  mov      qword ptr [rsp + 0x30], rsi
001B1A6F  call     0x1ad860  ; -> 001AD860 fn
001B1A74  mov      r10, qword ptr [rbx]
001B1A77  mov      rsi, rax
001B1A7A  test     r10, r10
001B1A7D  je       0x1b1ab3  ; -> 001B1AB3
001B1A7F  mov      r8, qword ptr [rbx + 0x10]
001B1A83  lea      rcx, [rbx + 0x18]
001B1A87  mov      r9, qword ptr [rcx]
001B1A8A  sub      r8, r10
001B1A8D  mov      rax, rbp
001B1A90  imul     r8
001B1A93  sar      rdx, 3
001B1A97  mov      r8, rdx
001B1A9A  shr      r8, 0x3f
001B1A9E  add      r8, rdx
001B1AA1  mov      rdx, r10
001B1AA4  mov      r8d, r8d
001B1AA7  lea      r8, [r8 + r8*2]
001B1AAB  shl      r8, 4
001B1AAF  call     qword ptr [r9 + 0x18]
001B1AB3  mov      rcx, qword ptr [rbx + 8]
001B1AB7  mov      rax, rbp
001B1ABA  sub      rcx, qword ptr [rbx]
001B1ABD  imul     rcx
001B1AC0  lea      rcx, [rdi + rdi*2]
001B1AC4  mov      qword ptr [rbx], rsi
001B1AC7  sar      rdx, 3
001B1ACB  mov      rax, rdx
001B1ACE  shl      rcx, 4
001B1AD2  shr      rax, 0x3f
001B1AD6  add      rdx, rax
001B1AD9  lea      rax, [rdx + rdx*2]
001B1ADD  shl      rax, 4
001B1AE1  add      rax, rsi
001B1AE4  add      rcx, rsi
001B1AE7  mov      qword ptr [rbx + 8], rax
001B1AEB  mov      rsi, qword ptr [rsp + 0x30]
001B1AF0  mov      qword ptr [rbx + 0x10], rcx
001B1AF4  mov      rbx, qword ptr [rsp + 0x38]
001B1AF9  mov      rbp, qword ptr [rsp + 0x40]
001B1AFE  add      rsp, 0x20
001B1B02  pop      rdi
001B1B03  ret      
```

## 001D6250 (117 B, extent 001D6250-001D62C5)

Entered from (direct sites whose caller this page cites): `001D5FD0` + 0x29 (jmp; `001D5FD0` is cited on this page)
Other direct sites: none

Host context: "E0' returned a non-zero 'al', else the incoming 'rcx' | Interior anchor '001C5540'; Interior anchor '001C5548'; Interior anchor '001C5557'; Interior anchor '001C555B'; Interior anchor '001C5568' | | '001D5FD0' | 46 B | calls '0016D6A0(1 when qword 01F82C80 is non-null, else 0)', then tail-jumps to '001D5FD0'+0x29 with 'rcx' = qword '01F82C80' and 'rdx' = the incoming 'rcx' | Interior anchor '001D5FE2'; Interior anchor '001D5FE5'; Interi"

```
001D6250  push     rbx
001D6252  sub      rsp, 0x20
001D6256  movsxd   rax, dword ptr [rcx + 0x20]
001D625A  mov      rbx, rcx
001D625D  cmp      eax, 0x80
001D6262  jge      0x1d62bf  ; -> 001D62BF
001D6264  movsxd   rdx, dword ptr [rip + 0x1dab5c9]  ; -> 01F81834
001D626B  shl      rdx, 7
001D626F  add      rdx, rax
001D6272  mov      qword ptr [rsp + 0x30], rdi
001D6277  lea      rdi, [rip - 0xb627e]  ; -> 00120000 (image base)
001D627E  mov      rdx, qword ptr [rdi + rdx*8 + 0x1e61880]  ; image base + 0x1e61880 = 01F81880
001D6286  test     rdx, rdx
001D6289  je       0x1d62b7  ; -> 001D62B7
001D628B  mov      rcx, qword ptr [rip + 0x1dab5ae]  ; -> 01F81840
001D6292  mov      rax, qword ptr [rcx]
001D6295  call     qword ptr [rax + 0xe0]
001D629B  movsxd   rax, dword ptr [rip + 0x1dab592]  ; -> 01F81834
001D62A2  cmp      dword ptr [rdi + rax*4 + 0x1e61850], 0  ; image base + 0x1e61850 = 01F81850
001D62AA  jne      0x1d62b7  ; -> 001D62B7
001D62AC  mov      dword ptr [rdi + rax*4 + 0x1e61850], 1  ; image base + 0x1e61850 = 01F81850
001D62B7  inc      dword ptr [rbx + 0x20]
001D62BA  mov      rdi, qword ptr [rsp + 0x30]
001D62BF  add      rsp, 0x20
001D62C3  pop      rbx
001D62C4  ret      
```

## 001FB830 (15 B, extent 001FB830-001FB83F)

Entered from (direct sites whose caller this page cites): `001F16C0` + 0x6E (jmp; `001F16C0` is cited on this page)
Other direct sites: none

Host context: "'/'+0x48'/'+0x54'/'+0x5C'/'+0x68'/ '+0x70' - the default transform/colour record. Interior anchor '0062DD2E' (the first '1.0f' store).  ## SWE2-EC7-77 update (2026-09-20) - '00220760' + '001A5810' + '001F16C0' lifecycle helpers measured  '00220760' (119 B) is the '[rcx+0x18]'-head chain drain: each link runs '001AF2B0(rcx, [link])' then the '+0x18' vtable slot of the '[rcx+0x30]' object with 'r8d = 0x30'; the head is then reset - '[rcx+"

```
001FB830  mov      rdx, qword ptr [rcx]
001FB833  mov      rcx, qword ptr [rip + 0x1d83c96]  ; -> 01F7F4D0
001FB83A  jmp      0x1a1850  ; -> 001A1850 fn
```

## 0026B790 (98 B, extent 0026B790-0026B7F2)

Entered from (direct sites whose caller this page cites): `00342D80` + 0x41 (jmp; `00342D80` is cited on this page)
Other direct sites: `00343570` + 0x3F (jmp)

Host context: "hor '002D7C92'; Interior anchor '002D7C9C' | | '002E2310' | 12 B | tail-jumps to '0016D6A0' with 'ecx' = 1 and 'edx' = the incoming 'ecx' | Interior anchor '002E2312'; Interior anchor '002E2317' | | '00342D80' | 70 B | calls '00267E10(r9)' and then '005C5230(byte [rdx+0x15], that result)'; when '005C5230' returns non-zero calls '0016D6A0' (no arguments loaded), otherwise skips it; then tail-jumps through '00342D80+0x41' with (byte '[rdx"

```
0026B790  movsxd   rax, ecx
0026B793  mov      r10d, r8d
0026B796  imul     r9, rax, 0x288
0026B79D  lea      rax, [rip + 0x1e2d66c]  ; -> 02098E10
0026B7A4  add      r9, rax
0026B7A7  test     edx, edx
0026B7A9  jns      0x26b7af  ; -> 0026B7AF
0026B7AB  xor      edx, edx
0026B7AD  jmp      0x26b7b9  ; -> 0026B7B9
0026B7AF  mov      eax, 0x1ff
0026B7B4  cmp      edx, eax
0026B7B6  cmovg    edx, eax
0026B7B9  mov      eax, edx
0026B7BB  cdq      
0026B7BC  and      edx, 0x1f
0026B7BF  add      eax, edx
0026B7C1  mov      r8d, eax
0026B7C4  and      eax, 0x1f
0026B7C7  sub      eax, edx
0026B7C9  sar      r8d, 5
0026B7CD  mov      ecx, eax
0026B7CF  mov      edx, 1
0026B7D4  shl      edx, cl
0026B7D6  movsxd   rax, r8d
0026B7D9  test     r10d, r10d
0026B7DC  je       0x26b7e7  ; -> 0026B7E7
0026B7DE  or       dword ptr [r9 + rax*4 + 0x244], edx
0026B7E6  ret      
0026B7E7  not      edx
0026B7E9  and      dword ptr [r9 + rax*4 + 0x244], edx
0026B7F1  ret      
```

## 0046DE80 (345 B, extent 0046DE80-0046DFD9)

Entered from (direct sites whose caller this page cites): `0046E050` + 0x4F (call; `0046E050` is cited on this page)
Other direct sites: none

Host context: "d' when that qword is non-null, and returns otherwise | Interior anchor '0040730C'; Interior anchor '00407315'; Interior anchor '00407346'; Interior anchor '0040736F'; Interior anchor '004073A1' | | '0046E050' | 129 B | returns when 'ecx' is 2 or more (signed); otherwise takes the 0xa0-byte record at '02CA6070' + 0xa0*'ecx', calls '00861EC0(record, 0, 0xa0)', stores dword '+4' = the result of '0046E050+0x4F(edx, r8d)', qword '+0x10' = '"

```
0046DE80  mov      qword ptr [rsp + 8], rbx
0046DE85  mov      qword ptr [rsp + 0x10], rsi
0046DE8A  mov      qword ptr [rsp + 0x18], rdi
0046DE8F  mov      rbx, qword ptr [rip + 0x2a4c672]  ; -> 02EBA508
0046DE96  movsxd   rsi, edx
0046DE99  movsxd   rdi, ecx
0046DE9C  test     rbx, rbx
0046DE9F  jne      0x46deb3  ; -> 0046DEB3
0046DEA1  xor      eax, eax
0046DEA3  mov      rbx, qword ptr [rsp + 8]
0046DEA8  mov      rsi, qword ptr [rsp + 0x10]
0046DEAD  mov      rdi, qword ptr [rsp + 0x18]
0046DEB2  ret      
0046DEB3  movzx    eax, byte ptr [rbx + 4]
0046DEB7  cmp      edi, eax
0046DEB9  jg       0x46dea1  ; -> 0046DEA1
0046DEBB  lea      eax, [rdi + rdi*4]
0046DEBE  add      eax, eax
0046DEC0  movsxd   rdx, eax
0046DEC3  add      rdx, rbx
0046DEC6  movzx    ecx, byte ptr [rdx + 0x19]
0046DECA  movzx    eax, byte ptr [rdx + 0x18]
0046DECE  shl      ecx, 8
0046DED1  or       ecx, eax
0046DED3  cmp      esi, ecx
0046DED5  jge      0x46dea1  ; -> 0046DEA1
0046DED7  movzx    r9d, byte ptr [rdx + 0x10]
0046DEDC  movzx    r10d, byte ptr [rdx + 0x13]
0046DEE1  movzx    eax, byte ptr [rdx + 0x12]
0046DEE5  shl      r10d, 8
0046DEE9  or       r10d, eax
0046DEEC  movzx    eax, byte ptr [rdx + 0x11]
0046DEF0  shl      r10d, 8
0046DEF4  or       r10d, eax
0046DEF7  mov      eax, esi
0046DEF9  cdq      
0046DEFA  shl      r10d, 8
0046DEFE  and      edx, 0xf
0046DF01  movsxd   r8, r10d
0046DF04  or       r8, r9
0046DF07  add      eax, edx
0046DF09  sar      eax, 4
0046DF0C  mov      r11d, eax
0046DF0F  shl      r11d, 4
0046DF13  movsxd   r11, r11d
0046DF16  lea      ecx, [rax + rax*2]
0046DF19  movsxd   rdx, ecx
0046DF1C  add      r8, rdx
0046DF1F  movsxd   rcx, r10d
0046DF22  or       rcx, r9
0046DF25  mov      r10, rsi
0046DF28  add      rcx, rdx
0046DF2B  movzx    eax, byte ptr [r8 + rbx]
0046DF30  movzx    r9d, byte ptr [rcx + rbx + 2]
0046DF36  movzx    ecx, byte ptr [r8 + rbx + 1]
0046DF3C  shl      r9d, 8
0046DF40  or       r9d, ecx
0046DF43  shl      r9d, 8
0046DF47  or       r9d, eax
0046DF4A  shr      r9d, 2
0046DF4E  cmp      r11, rsi
0046DF51  jge      0x46dfc0  ; -> 0046DFC0
0046DF53  lea      rax, [rdi + rdi*4]
0046DF57  sub      r10, r11
0046DF5A  movzx    edx, byte ptr [rbx + rax*2 + 0x17]
0046DF5F  lea      rcx, [rbx + rax*2]
0046DF63  movzx    eax, byte ptr [rbx + rax*2 + 0x16]
0046DF68  shl      edx, 8
0046DF6B  or       edx, eax
0046DF6D  movzx    eax, byte ptr [rcx + 0x15]
0046DF71  shl      edx, 8
0046DF74  or       edx, eax
0046DF76  lea      rax, [rdi + rdi*4]
0046DF7A  movzx    eax, byte ptr [rbx + rax*2 + 0x14]
0046DF7F  shl      edx, 8
0046DF82  movsxd   rdx, edx
0046DF85  or       rax, rdx
0046DF88  add      rax, rbx
0046DF8B  xor      edx, edx
0046DF8D  lea      rcx, [rax + r11*4]
0046DF91  mov      eax, dword ptr [rcx]
0046DF93  test     al, 1
0046DF95  jne      0x46dfa0  ; -> 0046DFA0
0046DF97  shr      eax, 1
0046DF99  and      eax, 0x1fff
0046DF9E  jmp      0x46dfb3  ; -> 0046DFB3
0046DFA0  shr      eax, 2
0046DFA3  cmp      eax, 0x3fffffff
0046DFA8  cmove    eax, edx
0046DFAB  add      eax, 0x7ff
0046DFB0  shr      eax, 0xb
0046DFB3  add      rcx, 4
0046DFB7  add      r9d, eax
0046DFBA  sub      r10, 1
0046DFBE  jne      0x46df91  ; -> 0046DF91
0046DFC0  mov      eax, dword ptr [rip + 0x2a4c53a]  ; -> 02EBA500
0046DFC6  mov      rbx, qword ptr [rsp + 8]
0046DFCB  add      eax, r9d
0046DFCE  mov      rsi, qword ptr [rsp + 0x10]
0046DFD3  mov      rdi, qword ptr [rsp + 0x18]
0046DFD8  ret      
```

## 00561280 (119 B, extent 00561280-005612F7)

Entered from (direct sites whose caller this page cites): `002D7BF0` + 0x57 (call; `002D7BF0` is cited on this page)
Other direct sites: none

Host context: "ame cookie (qword '01F44830' XOR 'rsp') to '00808C40' | Interior anchor '002D7A06'; Interior anchor '002D7A22'; Interior anchor '002D7A29'; Interior anchor '002D7A6D'; Interior anchor '002D7A77' | | '002D7BF0' | 183 B | keeps 'r8d'; takes the qword pointer at '0209AC30' and uses its qword '+0xd8', or its qword '+0x100' when that is null, and when the chosen object is non-null stores its dwords '+0xcc' = 3, '+0xc4' = 8 and '+0xc8' = 'r8d"

```
00561280  push     rbx
00561282  sub      rsp, 0x20
00561286  mov      rax, qword ptr [rip + 0x1b399a3]  ; -> 0209AC30
0056128D  mov      rbx, qword ptr [rax + 0x320]
00561294  test     rbx, rbx
00561297  je       0x5612d9  ; -> 005612D9
00561299  test     ecx, ecx
0056129B  jne      0x5612bb  ; -> 005612BB
0056129D  test     byte ptr [rbx + 0x570], 2
005612A4  jne      0x5612d9  ; -> 005612D9
005612A6  mov      rcx, rbx
005612A9  call     0x55a1f0  ; -> 0055A1F0 fn
005612AE  or       dword ptr [rbx + 0x570], 2
005612B5  add      rsp, 0x20
005612B9  pop      rbx
005612BA  ret      
005612BB  test     byte ptr [rbx + 0x570], 2
005612C2  je       0x5612d9  ; -> 005612D9
005612C4  mov      rcx, rbx
005612C7  call     0x559800  ; -> 00559800 fn
005612CC  and      dword ptr [rbx + 0x570], 0xfffffffd
005612D3  add      rsp, 0x20
005612D7  pop      rbx
005612D8  ret      
005612D9  mov      edx, 3
005612DE  lea      ecx, [rdx - 2]
005612E1  call     0x2d7580  ; -> 002D7580 fn
005612E6  mov      edx, 3
005612EB  xor      ecx, ecx
005612ED  add      rsp, 0x20
005612F1  pop      rbx
005612F2  jmp      0x2d7580  ; -> 002D7580 fn
```

## 00616210 (58 B, extent 00616210-0061624A)

Entered from (direct sites whose caller this page cites): `00163760` + 0x43 (call; `00163760` is cited on this page); `00163D60` + 0x2F (call; `00163D60` is cited on this page)
Other direct sites: `00163110` + 0x46 (call); `00163170` + 0x46 (call); `001631D0` + 0x46 (call); `00163230` + 0x46 (call); `00163290` + 0x38 (call); `001632E0` + 0x38 (call); `00163330` + 0x38 (call); `00163380` + 0x38 (call); `001633D0` + 0x44 (call); `00163430` + 0x44 (call); `00163490` + 0x44 (call); `001634F0` + 0x44 (call); `00163550` + 0x38 (call); `001635A0` + 0x38 (call); `001635F0` + 0x38 (call); `00163640` + 0x46 (call); `001636A0` + 0x46 (call); `00163700` + 0x46 (call); `001637C0` + 0x46 (call); `00163820` + 0x46 (call); `00163880` + 0x46 (call); `001638E0` + 0x46 (call); `00163940` + 0x46 (call); `001639A0` + 0x46 (call); `00163A00` + 0x46 (call); `00163A60` + 0x46 (call); `00163AC0` + 0x46 (call); `00163B20` + 0x46 (call); `00163B80` + 0x46 (call); `00163BE0` + 0x46 (call); `00163C40` + 0x46 (call); `00163CA0` + 0x46 (call); `00163D00` + 0x46 (call)

Host context: "d '02CB757C', then tail-jumps to '00808B90(008AB0B0)' | Interior anchor '001615CB'; Interior anchor '001615D7'; Interior anchor '001615EC'; Interior anchor '001615FF'; Interior anchor '00161609' | | '00163760' | 88 B | calls the function at site '00163760' + 0x43 with ('02CF72C0', '00D560D8', 0, 0x1F8) and stack arguments 0, 0x3D, 0x3D, 0x3D, 0x3D, then tail-jumps to '00808B90(008AEF70)' | Interior anchor '0016378A'; Interior anchor '00" / "tack arguments 0, 0x3D, 0x3D, 0x3D, 0x3D, then tail-jumps to '00808B90(008AEF70)' | Interior anchor '0016378A'; Interior anchor '0016379B'; Interior anchor '001637A3'; Interior anchor '001637B3' | | '00163D60' | 68 B | calls the function at site '00163D60' + 0x2F with ('02CF7A30', "UNKNOWN" ('00D26D00'), 0x33, 0) and five zero stack arguments, then tail-jumps to '00808B90(008AF070)' | Interior anchor '00163D66'; Interior anchor '00163D8"

```
00616210  push     rbx
00616212  sub      rsp, 0x20
00616216  mov      rbx, rcx
00616219  call     0x62cd40  ; -> 0062CD40 fn
0061621E  mov      eax, dword ptr [rsp + 0x50]
00616222  mov      dword ptr [rbx + 0x20], eax
00616225  mov      eax, dword ptr [rsp + 0x58]
00616229  mov      dword ptr [rbx + 0x24], eax
0061622C  mov      eax, dword ptr [rsp + 0x60]
00616230  mov      dword ptr [rbx + 0x28], eax
00616233  mov      eax, dword ptr [rsp + 0x68]
00616237  mov      dword ptr [rbx + 0x2c], eax
0061623A  mov      eax, dword ptr [rsp + 0x70]
0061623E  mov      dword ptr [rbx + 0x30], eax
00616241  mov      rax, rbx
00616244  add      rsp, 0x20
00616248  pop      rbx
00616249  ret      
```

## 0061C920 (1292 B, extent 0061C920-0061CE2C)

Entered from (direct sites whose caller this page cites): `00671E80` + 0x68 (call; `00671E80` is cited on this page)
Other direct sites: none

Host context: "ress '00D68DE0' at qword '+0x28'; returns the pointer | Interior anchor '0066F68E'; Interior anchor '0066F69B'; Interior anchor '0066F6AA'; Interior anchor '0066F6D9'; Interior anchor '0066F6EB' | | '00671E80' | 342 B | stores 0 at qword '[r9]' and dword '[fifth (stack) arg]'; with n = dword '[eighth]' AND '0x7fffffff' and A = qword 'eighth+8' (stride '0x88'), when n is non-zero calls '00671E80'+0x68('rdx', 0, A, n, ninth) and returns i"

```
0061C920  push     rbx
0061C922  push     rbp
0061C923  push     rsi
0061C924  push     rdi
0061C925  push     r12
0061C927  push     r13
0061C929  push     r14
0061C92B  sub      rsp, 0x30
0061C92F  mov      r13, rcx
0061C932  mov      ebx, r9d
0061C935  test     edx, edx
0061C937  mov      ecx, 0x708
0061C93C  mov      r12d, 0x760
0061C942  mov      rsi, r8
0061C945  cmove    r12d, ecx
0061C949  mov      ebp, edx
0061C94B  xor      r10d, r10d
0061C94E  add      r12, r13
0061C951  mov      edi, r10d
0061C954  mov      r11d, r10d
0061C957  cmp      r9d, 8
0061C95B  jb       0x61ca86  ; -> 0061CA86
0061C961  movaps   xmmword ptr [rsp + 0x20], xmm6
0061C966  mov      r14d, ebx
0061C969  movdqa   xmm6, xmmword ptr [rip + 0x73970f]  ; -> 00D56080 [u32x4 0x0000000F, 0x0000000F, 0x0000000F, 0x0000000F]
0061C971  xorps    xmm4, xmm4
0061C974  movaps   xmmword ptr [rsp + 0x10], xmm7
0061C979  and      r14d, 0xfffffff8
0061C97D  movdqa   xmm7, xmmword ptr [rip + 0x73972b]  ; -> 00D560B0 [u32x4 0xFFFFFFF0, 0xFFFFFFF0, 0xFFFFFFF0, 0xFFFFFFF0]
0061C985  movdqa   xmm5, xmm4
0061C989  mov      edi, 2
0061C98E  nop      
0061C990  lea      ecx, [rdi + 1]
0061C993  mov      eax, edi
0061C995  imul     r8, rcx, 0x88
0061C99C  imul     rdx, rax, 0x88
0061C9A3  movd     xmm1, dword ptr [r8 + rsi + 0x78]
0061C9AA  lea      ecx, [rdi - 1]
0061C9AD  mov      r9d, r11d
0061C9B0  imul     rax, rcx, 0x88
0061C9B7  movd     xmm0, dword ptr [rdx + rsi + 0x78]
0061C9BD  imul     rcx, r9, 0x88
0061C9C4  movd     xmm2, dword ptr [rax + rsi + 0x78]
0061C9CA  punpckldq xmm2, xmm1
0061C9CE  add      r11d, 8
0061C9D2  movd     xmm3, dword ptr [rcx + rsi + 0x78]
0061C9D8  lea      ecx, [rdi + 5]
0061C9DB  punpckldq xmm3, xmm0
0061C9DF  punpckldq xmm3, xmm2
0061C9E3  paddd    xmm3, xmm6
0061C9E7  pand     xmm3, xmm7
0061C9EB  paddd    xmm3, xmm4
0061C9EF  movdqa   xmm4, xmm3
0061C9F3  imul     r9, rcx, 0x88
0061C9FA  lea      ecx, [rdi + 4]
0061C9FD  imul     r8, rcx, 0x88
0061CA04  movd     xmm1, dword ptr [r9 + rsi + 0x78]
0061CA0B  lea      ecx, [rdi + 3]
0061CA0E  imul     rdx, rcx, 0x88
0061CA15  movd     xmm0, dword ptr [r8 + rsi + 0x78]
0061CA1C  lea      ecx, [rdi + 2]
0061CA1F  add      edi, 8
0061CA22  imul     rax, rcx, 0x88
0061CA29  movd     xmm2, dword ptr [rdx + rsi + 0x78]
0061CA2F  punpckldq xmm2, xmm1
0061CA33  movd     xmm3, dword ptr [rax + rsi + 0x78]
0061CA39  punpckldq xmm3, xmm0
0061CA3D  punpckldq xmm3, xmm2
0061CA41  paddd    xmm3, xmm6
0061CA45  pand     xmm3, xmm7
0061CA49  paddd    xmm3, xmm5
0061CA4D  movdqa   xmm5, xmm3
0061CA51  cmp      r11d, r14d
0061CA54  jb       0x61c990  ; -> 0061C990
0061CA5A  movaps   xmm7, xmmword ptr [rsp + 0x10]
0061CA5F  paddd    xmm4, xmm3
0061CA63  movaps   xmm6, xmmword ptr [rsp + 0x20]
0061CA68  movdqa   xmm0, xmm4
0061CA6C  psrldq   xmm0, 8
0061CA71  paddd    xmm4, xmm0
0061CA75  movdqa   xmm0, xmm4
0061CA79  psrldq   xmm0, 4
0061CA7E  paddd    xmm4, xmm0
0061CA82  movd     edi, xmm4
0061CA86  mov      r8d, r10d
0061CA89  mov      r9d, r10d
0061CA8C  cmp      r11d, ebx
0061CA8F  jae      0x61cb1c  ; -> 0061CB1C
0061CA95  mov      eax, ebx
0061CA97  sub      eax, r11d
0061CA9A  cmp      eax, 2
0061CA9D  jb       0x61cafb  ; -> 0061CAFB
0061CA9F  mov      eax, r11d
0061CAA2  lea      rdx, [rsi + 0x100]
0061CAA9  imul     rcx, rax, 0x88
0061CAB0  mov      eax, ebx
0061CAB2  sub      eax, r11d
0061CAB5  add      rdx, rcx
0061CAB8  sub      eax, 2
0061CABB  shr      eax, 1
0061CABD  inc      eax
0061CABF  mov      ecx, eax
0061CAC1  lea      r11d, [r11 + rax*2]
0061CAC5  nop      word ptr [rax + rax]
0061CAD0  mov      eax, dword ptr [rdx - 0x88]
0061CAD6  lea      rdx, [rdx + 0x110]
0061CADD  add      eax, 0xf
0061CAE0  and      eax, 0xfffffff0
0061CAE3  add      r8d, eax
0061CAE6  mov      eax, dword ptr [rdx - 0x110]
0061CAEC  add      eax, 0xf
0061CAEF  and      eax, 0xfffffff0
0061CAF2  add      r9d, eax
0061CAF5  sub      rcx, 1
0061CAF9  jne      0x61cad0  ; -> 0061CAD0
0061CAFB  cmp      r11d, ebx
0061CAFE  jae      0x61cb16  ; -> 0061CB16
0061CB00  mov      eax, r11d
0061CB03  imul     rcx, rax, 0x88
0061CB0A  mov      eax, dword ptr [rcx + rsi + 0x78]
0061CB0E  add      eax, 0xf
0061CB11  and      eax, 0xfffffff0
0061CB14  add      edi, eax
0061CB16  lea      eax, [r9 + r8]
0061CB1A  add      edi, eax
0061CB1C  mov      r8, qword ptr [rsp + 0x90]
0061CB24  mov      qword ptr [rsp + 0x80], r15
0061CB2C  test     r8, r8
0061CB2F  je       0x61cb3f  ; -> 0061CB3F
0061CB31  mov      r15d, dword ptr [r8 + 0x70]
0061CB35  add      r15d, 0xf
0061CB39  and      r15d, 0xfffffff0
0061CB3D  jmp      0x61cb42  ; -> 0061CB42
0061CB3F  mov      r15d, r10d
0061CB42  mov      r14d, dword ptr [r13 + 0x6f0]
0061CB49  lea      rax, [r14 + 8]
0061CB4D  mov      r9d, dword ptr [r12 + rax*4]
0061CB51  lea      rax, [r12 + rax*4]
0061CB55  mov      qword ptr [rsp + 0x70], rax
0061CB5A  lea      rax, [r14 + 0xa]
0061CB5E  mov      r11d, dword ptr [r12 + rax*4]
0061CB62  lea      rax, [r12 + rax*4]
0061CB66  mov      qword ptr [rsp], rax
0061CB6A  lea      eax, [r9 + rdi]
0061CB6E  mov      dword ptr [rsp + 0x78], r11d
0061CB73  cmp      eax, dword ptr [r12 + 0x30]
0061CB78  ja       0x61ce10  ; -> 0061CE10
0061CB7E  lea      eax, [r11 + r15]
0061CB82  mov      dword ptr [rsp + 0x88], eax
0061CB89  cmp      eax, dword ptr [r12 + 0x34]
0061CB8E  ja       0x61ce10  ; -> 0061CE10
0061CB94  mov      rdi, qword ptr [r12 + r14*8]
0061CB98  mov      r12, qword ptr [r12 + r14*8 + 0x10]
0061CB9D  mov      qword ptr [rsp + 0x90], r12
0061CBA5  cmp      ebp, 1
0061CBA8  je       0x61cca6  ; -> 0061CCA6
0061CBAE  mov      r12, qword ptr [r13 + r14*8 + 0x740]
0061CBB6  mov      ebp, 4
0061CBBB  mov      r14, qword ptr [r13 + r14*8 + 0x750]
0061CBC3  test     ebx, ebx
0061CBC5  je       0x61cc3a  ; -> 0061CC3A
0061CBC7  lea      rdx, [rsi + 0x28]
0061CBCB  mov      rsi, rbx
0061CBCE  nop      
0061CBD0  mov      ebx, dword ptr [rdx + 0x50]
0061CBD3  test     ebx, ebx
0061CBD5  je       0x61cc28  ; -> 0061CC28
0061CBD7  mov      eax, dword ptr [rdx - 8]
0061CBDA  btr      eax, 0x1f
0061CBDE  cmp      eax, 1
0061CBE1  jbe      0x61cbe8  ; -> 0061CBE8
0061CBE3  mov      r11, qword ptr [rdx]
0061CBE6  jmp      0x61cbf1  ; -> 0061CBF1
0061CBE8  test     eax, eax
0061CBEA  mov      r11, r10
0061CBED  cmovne   r11, rdx
0061CBF1  mov      eax, dword ptr [rdx - 0x10]
0061CBF4  lea      rcx, [rax + rax*8]
0061CBF8  mov      qword ptr [r11 + rcx*8], rdi
0061CBFC  test     rdi, rdi
0061CBFF  je       0x61cc05  ; -> 0061CC05
0061CC01  or       dword ptr [rdx + 0x4c], 1
0061CC05  mov      dword ptr [rdx + 0x48], r9d
0061CC09  mov      eax, r9d
0061CC0C  add      rax, r12
0061CC0F  mov      dword ptr [rdx + 0x50], ebx
0061CC12  mov      qword ptr [rdx + 0x58], rax
0061CC16  mov      eax, ebp
0061CC18  cmovne   eax, r10d
0061CC1C  mov      byte ptr [rdx - 0xc], al
0061CC1F  lea      eax, [rbx + 0xf]
0061CC22  and      eax, 0xfffffff0
0061CC25  add      r9d, eax
0061CC28  add      rdx, 0x88
0061CC2F  sub      rsi, 1
0061CC33  jne      0x61cbd0  ; -> 0061CBD0
0061CC35  mov      r11d, dword ptr [rsp + 0x78]
0061CC3A  test     r15d, r15d
0061CC3D  je       0x61cdfd  ; -> 0061CDFD
0061CC43  mov      eax, dword ptr [r8 + 0x18]
0061CC47  btr      eax, 0x1f
0061CC4B  cmp      eax, 1
0061CC4E  jbe      0x61cc56  ; -> 0061CC56
0061CC50  mov      rdx, qword ptr [r8 + 0x20]
0061CC54  jmp      0x61cc61  ; -> 0061CC61
0061CC56  lea      rdx, [r8 + 0x20]
0061CC5A  test     eax, eax
0061CC5C  jne      0x61cc61  ; -> 0061CC61
0061CC5E  mov      rdx, r10
0061CC61  mov      eax, dword ptr [r8 + 0x10]
0061CC65  lea      rcx, [rax + rax*8]
0061CC69  mov      rax, qword ptr [rsp + 0x90]
0061CC71  mov      qword ptr [rdx + rcx*8], rax
0061CC75  test     rax, rax
0061CC78  je       0x61cc7f  ; -> 0061CC7F
0061CC7A  or       dword ptr [r8 + 0x6c], 1
0061CC7F  mov      eax, r11d
0061CC82  add      rax, r14
0061CC85  mov      dword ptr [r8 + 0x68], r11d
0061CC89  mov      r11d, dword ptr [rsp + 0x88]
0061CC91  cmovne   ebp, r10d
0061CC95  mov      dword ptr [r8 + 0x70], r15d
0061CC99  mov      byte ptr [r8 + 0xe], bpl
0061CC9D  mov      qword ptr [r8 + 0x78], rax
0061CCA1  jmp      0x61cdfd  ; -> 0061CDFD
0061CCA6  test     ebx, ebx
0061CCA8  je       0x61cd6e  ; -> 0061CD6E
0061CCAE  lea      rax, [rsi + 0x28]
0061CCB2  mov      r12, rbx
0061CCB5  nop      word ptr [rax + rax]
0061CCC0  mov      ebx, dword ptr [rax + 0x50]
0061CCC3  mov      rsi, r10
0061CCC6  mov      ebp, dword ptr [rax - 0x10]
0061CCC9  test     ebx, ebx
0061CCCB  je       0x61cd23  ; -> 0061CD23
0061CCCD  mov      ecx, dword ptr [rax - 8]
0061CCD0  btr      ecx, 0x1f
0061CCD4  cmp      ecx, 1
0061CCD7  jbe      0x61ccde  ; -> 0061CCDE
0061CCD9  mov      r11, qword ptr [rax]
0061CCDC  jmp      0x61cce7  ; -> 0061CCE7
0061CCDE  test     ecx, ecx
0061CCE0  mov      r11, r10
0061CCE3  cmovne   r11, rax
0061CCE7  lea      rdx, [rbp*8]
0061CCEF  add      rdx, rbp
0061CCF2  mov      qword ptr [r11 + rdx*8], rdi
0061CCF6  test     rdi, rdi
0061CCF9  je       0x61ccff  ; -> 0061CCFF
0061CCFB  or       dword ptr [rax + 0x4c], 1
0061CCFF  mov      dword ptr [rax + 0x48], r9d
0061CD03  lea      ecx, [rbx + 0xf]
0061CD06  and      ecx, 0xfffffff0
0061CD09  mov      dword ptr [rax + 0x50], ebx
0061CD0C  mov      qword ptr [rax + 0x58], 1
0061CD14  add      r9d, ecx
0061CD17  mov      byte ptr [rax - 0xc], sil
0061CD1B  mov      rsi, qword ptr [r13 + r14*8 + 0x798]
0061CD23  mov      ecx, dword ptr [rax - 8]
0061CD26  btr      ecx, 0x1f
0061CD2A  cmp      ecx, 1
0061CD2D  jbe      0x61cd34  ; -> 0061CD34
0061CD2F  mov      r11, qword ptr [rax]
0061CD32  jmp      0x61cd3d  ; -> 0061CD3D
0061CD34  test     ecx, ecx
0061CD36  mov      r11, r10
0061CD39  cmovne   r11, rax
0061CD3D  lea      rdx, [rbp*8]
0061CD45  add      rdx, rbp
0061CD48  mov      qword ptr [r11 + rdx*8 + 0x10], rsi
0061CD4D  or       dword ptr [rax + 0x4c], 1
0061CD51  add      rax, 0x88
0061CD57  sub      r12, 1
0061CD5B  jne      0x61ccc0  ; -> 0061CCC0
0061CD61  mov      r11d, dword ptr [rsp + 0x78]
0061CD66  mov      r12, qword ptr [rsp + 0x90]
0061CD6E  test     r8, r8
0061CD71  je       0x61cdfd  ; -> 0061CDFD
0061CD77  mov      ebx, dword ptr [r8 + 0x10]
0061CD7B  mov      rdx, r10
0061CD7E  test     r15d, r15d
0061CD81  je       0x61cdd4  ; -> 0061CDD4
0061CD83  mov      eax, dword ptr [r8 + 0x18]
0061CD87  btr      eax, 0x1f
0061CD8B  cmp      eax, 1
0061CD8E  jbe      0x61cd96  ; -> 0061CD96
0061CD90  mov      rdx, qword ptr [r8 + 0x20]
0061CD94  jmp      0x61cd9e  ; -> 0061CD9E
0061CD96  test     eax, eax
0061CD98  je       0x61cd9e  ; -> 0061CD9E
0061CD9A  lea      rdx, [r8 + 0x20]
0061CD9E  lea      rcx, [rbx + rbx*8]
0061CDA2  mov      qword ptr [rdx + rcx*8], r12
0061CDA6  test     r12, r12
0061CDA9  je       0x61cdb0  ; -> 0061CDB0
0061CDAB  or       dword ptr [r8 + 0x6c], 1
0061CDB0  mov      dword ptr [r8 + 0x68], r11d
0061CDB4  mov      r11d, dword ptr [rsp + 0x88]
0061CDBC  mov      dword ptr [r8 + 0x70], r15d
0061CDC0  mov      qword ptr [r8 + 0x78], 1
0061CDC8  mov      byte ptr [r8 + 0xe], r10b
0061CDCC  mov      rdx, qword ptr [r13 + r14*8 + 0x7a8]
0061CDD4  mov      eax, dword ptr [r8 + 0x18]
0061CDD8  btr      eax, 0x1f
0061CDDC  cmp      eax, 1
0061CDDF  jbe      0x61cde7  ; -> 0061CDE7
0061CDE1  mov      r10, qword ptr [r8 + 0x20]
0061CDE5  jmp      0x61cdef  ; -> 0061CDEF
0061CDE7  test     eax, eax
0061CDE9  je       0x61cdef  ; -> 0061CDEF
0061CDEB  lea      r10, [r8 + 0x20]
0061CDEF  lea      rcx, [rbx + rbx*8]
0061CDF3  mov      qword ptr [r10 + rcx*8 + 0x10], rdx
0061CDF8  or       dword ptr [r8 + 0x6c], 1
0061CDFD  mov      rax, qword ptr [rsp + 0x70]
0061CE02  mov      dword ptr [rax], r9d
0061CE05  mov      rax, qword ptr [rsp]
0061CE09  mov      dword ptr [rax], r11d
0061CE0C  xor      eax, eax
0061CE0E  jmp      0x61ce15  ; -> 0061CE15
0061CE10  mov      eax, 0xd
0061CE15  mov      r15, qword ptr [rsp + 0x80]
0061CE1D  add      rsp, 0x30
0061CE21  pop      r14
0061CE23  pop      r13
0061CE25  pop      r12
0061CE27  pop      rdi
0061CE28  pop      rsi
0061CE29  pop      rbp
0061CE2A  pop      rbx
0061CE2B  ret      
```

## 00662A50 (37 B, extent 00662A50-00662A75)

Entered from (direct sites whose caller this page cites): `00169450` + 0x16 (call; `00169450` is cited on this page)
Other direct sites: `006BB350` + 0x31 (call)

Host context: "d '02EA094C', then tail-jumps to '00808B90(008B78B0)' | Interior anchor '001688FB'; Interior anchor '00168907'; Interior anchor '0016891E'; Interior anchor '00168932'; Interior anchor '0016893C' | | '00169450' | 136 B | calls the function at site '00169450' + 0x16 with '02EA5850', stores the pointer '01CB3950' at qword '02EA5850' and zeroes qwords '02EA5888' and '02EA5890'; when qword '02EA5878' is not '02EA5888', bit 31 of dword '02EA5"

```
00662A50  lea      rax, [rip + 0x706399]  ; -> 00D68DF0
00662A57  mov      qword ptr [rcx], rax
00662A5A  xor      eax, eax
00662A5C  mov      qword ptr [rcx + 8], rax
00662A60  mov      dword ptr [rcx + 0x10], eax
00662A63  mov      qword ptr [rcx + 0x18], rax
00662A67  mov      dword ptr [rcx + 0x20], eax
00662A6A  mov      qword ptr [rcx + 0x28], rax
00662A6E  mov      dword ptr [rcx + 0x30], eax
00662A71  mov      rax, rcx
00662A74  ret      
```
