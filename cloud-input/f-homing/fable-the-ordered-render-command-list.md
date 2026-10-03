# F homing pack (FABLE): `17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 30. No bearing page cites them and no documented function calls them directly.

## 001A1850 (208 B, extent 001A1850-001A1920)

Documented callee on this page: `001F4950`

```
001A1850  push     rdi
001A1852  sub      rsp, 0x30
001A1856  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001A185F  mov      qword ptr [rsp + 0x40], rbx
001A1864  mov      qword ptr [rsp + 0x48], rsi
001A1869  mov      rsi, rdx
001A186C  mov      rbx, rcx
001A186F  call     0x189120  ; -> 00189120 fn
001A1874  test     rax, rax
001A1877  je       0x1a18e0  ; -> 001A18E0
001A1879  mov      edx, 0x28
001A187E  mov      rcx, qword ptr [rip + 0x1dddc3b]  ; -> 01F7F4C0
001A1885  call     0x1a1470  ; -> 001A1470 fn
001A188A  mov      rbx, rax
001A188D  mov      qword ptr [rsp + 0x50], rax
001A1892  xor      edi, edi
001A1894  mov      ecx, edi
001A1896  test     rax, rax
001A1899  setne    cl
001A189C  call     0x16d6a0  ; -> 0016D6A0 fn
001A18A1  mov      qword ptr [rsp + 0x58], rbx
001A18A6  test     rbx, rbx
001A18A9  je       0x1a18bc  ; -> 001A18BC
001A18AB  xor      r8d, r8d
001A18AE  mov      rdx, rsi
001A18B1  mov      rcx, rbx
001A18B4  call     0x1f4950  ; -> 001F4950 fn
001A18B9  mov      rdi, rax
001A18BC  mov      rdx, rbx
001A18BF  mov      rcx, qword ptr [rip + 0x1dddbfa]  ; -> 01F7F4C0
001A18C6  call     0x16d6a0  ; -> 0016D6A0 fn
001A18CB  call     0x189120  ; -> 00189120 fn
001A18D0  mov      r8, qword ptr [rdi]
001A18D3  mov      rdx, qword ptr [rax + 8]
001A18D7  mov      rcx, rdi
001A18DA  call     qword ptr [r8 + 8]
001A18DE  jmp      0x1a1910  ; -> 001A1910
001A18E0  xor      edi, edi
001A18E2  mov      ecx, edi
001A18E4  test     rsi, rsi
001A18E7  setne    cl
001A18EA  call     0x16d6a0  ; -> 0016D6A0 fn
001A18EF  cmp      qword ptr [rbx + 8], rdi
001A18F3  setne    dil
001A18F7  mov      ecx, edi
001A18F9  call     0x16d6a0  ; -> 0016D6A0 fn
001A18FE  mov      rcx, qword ptr [rbx + 8]
001A1902  mov      rax, qword ptr [rcx]
001A1905  mov      r8d, 0x40
001A190B  mov      rdx, rsi
001A190E  call     qword ptr [rax]
001A1910  mov      rbx, qword ptr [rsp + 0x40]
001A1915  mov      rsi, qword ptr [rsp + 0x48]
001A191A  add      rsp, 0x30
001A191E  pop      rdi
001A191F  ret      
```

## 001B27E0 (525 B, extent 001B27E0-001B29ED)

Documented callee on this page: `00186A90`

```
001B27E0  mov      rax, rsp
001B27E3  push     rdi
001B27E4  sub      rsp, 0xa0
001B27EB  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001B27F4  mov      qword ptr [rax + 8], rbx
001B27F8  mov      qword ptr [rax + 0x10], rsi
001B27FC  movaps   xmmword ptr [rax - 0x18], xmm6
001B2800  movaps   xmmword ptr [rax - 0x28], xmm7
001B2804  movaps   xmmword ptr [rax - 0x38], xmm8
001B2809  movaps   xmmword ptr [rax - 0x48], xmm9
001B280E  movaps   xmmword ptr [rax - 0x58], xmm10
001B2813  movaps   xmmword ptr [rax - 0x68], xmm11
001B2818  movaps   xmmword ptr [rax - 0x78], xmm12
001B281D  mov      rsi, rdx
001B2820  mov      rdi, rcx
001B2823  add      rcx, 0x218
001B282A  call     0x5cd4f0  ; -> 005CD4F0 fn
001B282F  lea      rax, [rdi + 0xe4]
001B2836  movups   xmm0, xmmword ptr [rax]
001B2839  movups   xmmword ptr [rsi], xmm0
001B283C  movups   xmm1, xmmword ptr [rax + 0x10]
001B2840  movups   xmmword ptr [rsi + 0x10], xmm1
001B2844  movups   xmm0, xmmword ptr [rax + 0x20]
001B2848  movups   xmmword ptr [rsi + 0x20], xmm0
001B284C  movups   xmm1, xmmword ptr [rax + 0x30]
001B2850  movups   xmmword ptr [rsi + 0x30], xmm1
001B2854  movups   xmm0, xmmword ptr [rax + 0x40]
001B2858  movups   xmmword ptr [rsi + 0x40], xmm0
001B285C  movups   xmm1, xmmword ptr [rax + 0x50]
001B2860  movups   xmmword ptr [rsi + 0x50], xmm1
001B2864  movups   xmm0, xmmword ptr [rax + 0x60]
001B2868  movups   xmmword ptr [rsi + 0x60], xmm0
001B286C  lea      r8, [rsi + 0x80]
001B2873  movups   xmm0, xmmword ptr [rax + 0x70]
001B2877  movups   xmmword ptr [r8 - 0x10], xmm0
001B287C  lea      rax, [rax + 0x80]
001B2883  movups   xmm1, xmmword ptr [rax]
001B2886  movups   xmmword ptr [r8], xmm1
001B288A  movups   xmm0, xmmword ptr [rax + 0x10]
001B288E  movups   xmmword ptr [r8 + 0x10], xmm0
001B2893  movups   xmm1, xmmword ptr [rax + 0x20]
001B2897  movups   xmmword ptr [r8 + 0x20], xmm1
001B289C  movups   xmm0, xmmword ptr [rax + 0x30]
001B28A0  movups   xmmword ptr [r8 + 0x30], xmm0
001B28A5  movups   xmm1, xmmword ptr [rax + 0x40]
001B28A9  movups   xmmword ptr [r8 + 0x40], xmm1
001B28AE  movups   xmm0, xmmword ptr [rax + 0x50]
001B28B2  movups   xmmword ptr [r8 + 0x50], xmm0
001B28B7  lea      rcx, [rdi + 0x218]
001B28BE  call     0x5cd820  ; -> 005CD820 fn
001B28C3  nop      
001B28C4  cmp      qword ptr [rdi + 0x1c8], 0
001B28CC  je       0x1b29b5  ; -> 001B29B5
001B28D2  lea      rbx, [rsi + 0x18]
001B28D6  mov      edi, 8
001B28DB  xor      esi, esi
001B28DD  movsd    xmm10, qword ptr [rip + 0x1b3949a]  ; -> 01CEBD80 [u64 0x7FFFFFFFFFFFFFFF]
001B28E6  movss    xmm11, dword ptr [rip + 0x1b39281]  ; -> 01CEBB70 [f32 0.5]
001B28EF  movss    xmm12, dword ptr [rip + 0x745888]  ; -> 008F8180 [f32 10]
001B28F8  movss    xmm9, dword ptr [rip + 0x1b392a7]  ; -> 01CEBBA8 [f32 1]
001B2901  xorps    xmm8, xmm8
001B2905  cmp      dword ptr [rbx - 0x18], esi
001B2908  je       0x1b29a7  ; -> 001B29A7
001B290E  movss    xmm0, dword ptr [rbx - 0xc]
001B2913  subss    xmm0, dword ptr [rbx - 0x10]
001B2918  cvtps2pd xmm1, xmm0
001B291B  andps    xmm1, xmm10
001B291F  cvtpd2ps xmm6, xmm1
001B2923  call     0x189120  ; -> 00189120 fn
001B2928  mov      rcx, rax
001B292B  call     0x186aa0  ; -> 00186AA0 fn
001B2930  mov      eax, eax
001B2932  xorps    xmm7, xmm7
001B2935  cvtsi2ss xmm7, rax
001B293A  mulss    xmm7, xmm6
001B293E  mulss    xmm7, xmm11
001B2943  movss    xmm0, dword ptr [rbx - 8]
001B2948  subss    xmm0, dword ptr [rbx - 0x14]
001B294D  cvtps2pd xmm1, xmm0
001B2950  andps    xmm1, xmm10
001B2954  cvtpd2ps xmm6, xmm1
001B2958  call     0x189120  ; -> 00189120 fn
001B295D  mov      rcx, rax
001B2960  call     0x186a90  ; -> 00186A90 fn
001B2965  mov      eax, eax
001B2967  xorps    xmm1, xmm1
001B296A  cvtsi2ss xmm1, rax
001B296F  mulss    xmm1, xmm6
001B2973  mulss    xmm1, xmm11
001B2978  mulss    xmm1, xmm7
001B297C  comiss   xmm1, xmm12
001B2980  jbe      0x1b29a5  ; -> 001B29A5
001B2982  movaps   xmm0, xmm1
001B2985  mulss    xmm0, dword ptr [rbx]
001B2989  divss    xmm0, xmm1
001B298D  movss    dword ptr [rbx], xmm0
001B2991  comiss   xmm0, xmm9
001B2995  jbe      0x1b299f  ; -> 001B299F
001B2997  mov      dword ptr [rbx], 0x3f800000
001B299D  jmp      0x1b29a7  ; -> 001B29A7
001B299F  comiss   xmm8, xmm0
001B29A3  jbe      0x1b29a7  ; -> 001B29A7
001B29A5  mov      dword ptr [rbx], esi
001B29A7  add      rbx, 0x1c
001B29AB  sub      rdi, 1
001B29AF  jne      0x1b2905  ; -> 001B2905
001B29B5  lea      r11, [rsp + 0xa0]
001B29BD  mov      rbx, qword ptr [r11 + 0x10]
001B29C1  mov      rsi, qword ptr [r11 + 0x18]
001B29C5  movaps   xmm6, xmmword ptr [r11 - 0x10]
001B29CA  movaps   xmm7, xmmword ptr [r11 - 0x20]
001B29CF  movaps   xmm8, xmmword ptr [r11 - 0x30]
001B29D4  movaps   xmm9, xmmword ptr [r11 - 0x40]
001B29D9  movaps   xmm10, xmmword ptr [r11 - 0x50]
001B29DE  movaps   xmm11, xmmword ptr [r11 - 0x60]
001B29E3  movaps   xmm12, xmmword ptr [r11 - 0x70]
001B29E8  mov      rsp, r11
001B29EB  pop      rdi
001B29EC  ret      
```

## 001E2250 (928 B, extent 001E2250-001E25F0)

Documented callee on this page: `00212C50`

```
001E2250  mov      qword ptr [rsp + 8], rbx
001E2255  mov      qword ptr [rsp + 0x10], rbp
001E225A  mov      qword ptr [rsp + 0x18], rsi
001E225F  mov      qword ptr [rsp + 0x20], rdi
001E2264  push     r12
001E2266  push     r14
001E2268  push     r15
001E226A  sub      rsp, 0x40
001E226E  mov      r10, qword ptr [rcx + 0x10]
001E2272  mov      rdi, rdx
001E2275  mov      ebx, r8d
001E2278  movabs   r12, 0x2aaaaaaaaaaaaaab
001E2282  mov      r8, qword ptr [rcx + 8]
001E2286  mov      rax, r12
001E2289  sub      r10, r8
001E228C  mov      rbp, r9
001E228F  imul     r10
001E2292  mov      rsi, rcx
001E2295  sar      rdx, 2
001E2299  mov      rax, rdx
001E229C  shr      rax, 0x3f
001E22A0  add      rdx, rax
001E22A3  cmp      ebx, edx
001E22A5  ja       0x1e2442  ; -> 001E2442
001E22AB  test     ebx, ebx
001E22AD  je       0x1e25d1  ; -> 001E25D1
001E22B3  mov      rcx, qword ptr [r9 + 8]
001E22B7  lea      r10, [rip + 0x71ee1a]  ; -> 009010D8
001E22BE  mov      rbp, qword ptr [rsi + 8]
001E22C2  sub      r8, rdi
001E22C5  mov      rax, r12
001E22C8  mov      qword ptr [rsp + 0x28], rcx
001E22CD  movzx    ecx, byte ptr [r9 + 0x10]
001E22D2  imul     r8
001E22D5  mov      byte ptr [rsp + 0x30], cl
001E22D9  mov      r14, rdx
001E22DC  mov      qword ptr [rsp + 0x20], r10
001E22E1  sar      r14, 2
001E22E5  mov      rax, r14
001E22E8  shr      rax, 0x3f
001E22EC  add      r14, rax
001E22EF  cmp      ebx, r14d
001E22F2  jae      0x1e23a3  ; -> 001E23A3
001E22F8  lea      rax, [rbx + rbx*2]
001E22FC  mov      r15d, ebx
001E22FF  lea      r14, [rax*8]
001E2307  mov      rbx, rbp
001E230A  sub      rbx, r14
001E230D  mov      r8, rbp
001E2310  mov      rcx, rbx
001E2313  mov      rdx, rbp
001E2316  call     0x1e1440  ; -> 001E1440 fn
001E231B  add      qword ptr [rsi + 8], r14
001E231F  cmp      rbx, rdi
001E2322  je       0x1e235d  ; -> 001E235D
001E2324  lea      rcx, [r14 + 0x10]
001E2328  mov      rdx, 0xfffffffffffffff8
001E232F  add      rcx, rbx
001E2332  sub      rdx, r14
001E2335  imul     r8, r15, -0x18
001E2339  nop      dword ptr [rax]
001E2340  mov      rax, qword ptr [rdx + rcx - 0x18]
001E2345  lea      rcx, [rcx - 0x18]
001E2349  mov      qword ptr [rcx - 8], rax
001E234D  sub      rbx, 0x18
001E2351  movzx    eax, byte ptr [r8 + rcx]
001E2356  mov      byte ptr [rcx], al
001E2358  cmp      rbx, rdi
001E235B  jne      0x1e2340  ; -> 001E2340
001E235D  lea      rdx, [r14 + rdi]
001E2361  cmp      rdi, rdx
001E2364  je       0x1e2433  ; -> 001E2433
001E236A  movzx    r8d, byte ptr [rsp + 0x30]
001E2370  lea      rcx, [rdi + 0x10]
001E2374  mov      r9, qword ptr [rsp + 0x28]
001E2379  nop      dword ptr [rax]
001E2380  mov      qword ptr [rcx - 8], r9
001E2384  mov      byte ptr [rcx], r8b
001E2387  lea      rcx, [rcx + 0x18]
001E238B  lea      rax, [rcx - 0x10]
001E238F  cmp      rax, rdx
001E2392  jne      0x1e2380  ; -> 001E2380
001E2394  lea      rcx, [rsp + 0x20]
001E2399  call     0x212c50  ; -> 00212C50 fn
001E239E  jmp      0x1e25d1  ; -> 001E25D1
001E23A3  sub      ebx, r14d
001E23A6  mov      rax, rbp
001E23A9  mov      edx, ebx
001E23AB  je       0x1e23d9  ; -> 001E23D9
001E23AD  lea      r9, [rip + 0x71ed04]  ; -> 009010B8
001E23B4  test     rax, rax
001E23B7  je       0x1e23d0  ; -> 001E23D0
001E23B9  mov      qword ptr [rax], r9
001E23BC  mov      rcx, qword ptr [rsp + 0x28]
001E23C1  mov      qword ptr [rax + 8], rcx
001E23C5  movzx    ecx, byte ptr [rsp + 0x30]
001E23CA  mov      byte ptr [rax + 0x10], cl
001E23CD  mov      qword ptr [rax], r10
001E23D0  add      rax, 0x18
001E23D4  add      edx, -1
001E23D7  jne      0x1e23b4  ; -> 001E23B4
001E23D9  lea      rcx, [rbx + rbx*2]
001E23DD  mov      rdx, rbp
001E23E0  shl      rcx, 3
001E23E4  add      qword ptr [rsi + 8], rcx
001E23E8  mov      rcx, rdi
001E23EB  mov      r8, qword ptr [rsi + 8]
001E23EF  call     0x1e1440  ; -> 001E1440 fn
001E23F4  mov      eax, r14d
001E23F7  lea      rcx, [rax + rax*2]
001E23FB  shl      rcx, 3
001E23FF  add      qword ptr [rsi + 8], rcx
001E2403  cmp      rdi, rbp
001E2406  je       0x1e2433  ; -> 001E2433
001E2408  movzx    edx, byte ptr [rsp + 0x30]
001E240D  lea      rcx, [rdi + 0x10]
001E2411  mov      r8, qword ptr [rsp + 0x28]
001E2416  nop      word ptr [rax + rax]
001E2420  mov      qword ptr [rcx - 8], r8
001E2424  mov      byte ptr [rcx], dl
001E2426  lea      rcx, [rcx + 0x18]
001E242A  lea      rax, [rcx - 0x10]
001E242E  cmp      rax, rbp
001E2431  jne      0x1e2420  ; -> 001E2420
001E2433  lea      rcx, [rsp + 0x20]
001E2438  call     0x212c50  ; -> 00212C50 fn
001E243D  jmp      0x1e25d1  ; -> 001E25D1
001E2442  sub      r8, qword ptr [rcx]
001E2445  mov      rax, r12
001E2448  imul     r8
001E244B  sar      rdx, 2
001E244F  mov      rax, rdx
001E2452  shr      rax, 0x3f
001E2456  add      rdx, rax
001E2459  lea      eax, [rdx + rdx]
001E245C  test     edx, edx
001E245E  jne      0x1e2465  ; -> 001E2465
001E2460  mov      eax, 1
001E2465  lea      r14d, [rdx + rbx]
001E2469  cmp      eax, r14d
001E246C  cmova    r14d, eax
001E2470  test     r14d, r14d
001E2473  je       0x1e2491  ; -> 001E2491
001E2475  mov      r9, qword ptr [rcx + 0x18]
001E2479  lea      rdx, [r14 + r14*2]
001E247D  add      rcx, 0x18
001E2481  shl      rdx, 3
001E2485  xor      r8d, r8d
001E2488  call     qword ptr [r9 + 0x10]
001E248C  mov      r15, rax
001E248F  jmp      0x1e2494  ; -> 001E2494
001E2491  xor      r15d, r15d
001E2494  mov      rcx, qword ptr [rsi]
001E2497  lea      r10, [rip + 0x71ec3a]  ; -> 009010D8
001E249E  lea      r9, [rip + 0x71ec13]  ; -> 009010B8
001E24A5  mov      rax, r15
001E24A8  cmp      rcx, rdi
001E24AB  je       0x1e24d7  ; -> 001E24D7
001E24AD  nop      dword ptr [rax]
001E24B0  test     rax, rax
001E24B3  je       0x1e24ca  ; -> 001E24CA
001E24B5  mov      qword ptr [rax], r9
001E24B8  mov      rdx, qword ptr [rcx + 8]
001E24BC  mov      qword ptr [rax + 8], rdx
001E24C0  movzx    edx, byte ptr [rcx + 0x10]
001E24C4  mov      byte ptr [rax + 0x10], dl
001E24C7  mov      qword ptr [rax], r10
001E24CA  add      rcx, 0x18
001E24CE  add      rax, 0x18
001E24D2  cmp      rcx, rdi
001E24D5  jne      0x1e24b0  ; -> 001E24B0
001E24D7  mov      r8d, ebx
001E24DA  mov      rcx, rax
001E24DD  test     ebx, ebx
001E24DF  je       0x1e2505  ; -> 001E2505
001E24E1  test     rcx, rcx
001E24E4  je       0x1e24fb  ; -> 001E24FB
001E24E6  mov      qword ptr [rcx], r9
001E24E9  mov      rdx, qword ptr [rbp + 8]
001E24ED  mov      qword ptr [rcx + 8], rdx
001E24F1  movzx    edx, byte ptr [rbp + 0x10]
001E24F5  mov      byte ptr [rcx + 0x10], dl
001E24F8  mov      qword ptr [rcx], r10
001E24FB  add      rcx, 0x18
001E24FF  add      r8d, -1
001E2503  jne      0x1e24e1  ; -> 001E24E1
001E2505  mov      rcx, qword ptr [rsi + 8]
001E2509  lea      r8, [rbx + rbx*2]
001E250D  lea      r11, [r8*8]
001E2515  lea      rbx, [r11 + rax]
001E2519  cmp      rdi, rcx
001E251C  je       0x1e2562  ; -> 001E2562
001E251E  mov      rdx, rbx
001E2521  lea      r8, [rdi + 0x10]
001E2525  sub      rdx, r11
001E2528  sub      rdx, rax
001E252B  add      r8, rdx
001E252E  sub      r11, rdi
001E2531  lea      rdx, [r11 + rax]
001E2535  test     rbx, rbx
001E2538  je       0x1e2551  ; -> 001E2551
001E253A  mov      qword ptr [rbx], r9
001E253D  mov      rax, qword ptr [r8 - 8]
001E2541  mov      qword ptr [rdx + r8 - 8], rax
001E2546  movzx    eax, byte ptr [r8]
001E254A  mov      byte ptr [rdx + r8], al
001E254E  mov      qword ptr [rbx], r10
001E2551  add      r8, 0x18
001E2555  add      rbx, 0x18
001E2559  lea      rax, [r8 - 0x10]
001E255D  cmp      rax, rcx
001E2560  jne      0x1e2535  ; -> 001E2535
001E2562  mov      rbp, qword ptr [rsi + 8]
001E2566  mov      rdi, qword ptr [rsi]
001E2569  cmp      rdi, rbp
001E256C  jae      0x1e2583  ; -> 001E2583
001E256E  nop      
001E2570  mov      rax, qword ptr [rdi]
001E2573  xor      edx, edx
001E2575  mov      rcx, rdi
001E2578  call     qword ptr [rax]
001E257A  add      rdi, 0x18
001E257E  cmp      rdi, rbp
001E2581  jb       0x1e2570  ; -> 001E2570
001E2583  mov      r10, qword ptr [rsi]
001E2586  test     r10, r10
001E2589  je       0x1e25be  ; -> 001E25BE
001E258B  mov      r8, qword ptr [rsi + 0x10]
001E258F  lea      rcx, [rsi + 0x18]
001E2593  mov      r9, qword ptr [rcx]
001E2596  sub      r8, r10
001E2599  mov      rax, r12
001E259C  imul     r8
001E259F  sar      rdx, 2
001E25A3  mov      rax, rdx
001E25A6  shr      rax, 0x3f
001E25AA  add      rax, rdx
001E25AD  mov      rdx, r10
001E25B0  mov      eax, eax
001E25B2  lea      r8, [rax + rax*2]
001E25B6  shl      r8, 3
001E25BA  call     qword ptr [r9 + 0x18]
001E25BE  lea      rcx, [r14 + r14*2]
001E25C2  mov      qword ptr [rsi], r15
001E25C5  lea      rax, [r15 + rcx*8]
001E25C9  mov      qword ptr [rsi + 8], rbx
001E25CD  mov      qword ptr [rsi + 0x10], rax
001E25D1  mov      rbx, qword ptr [rsp + 0x60]
001E25D6  mov      rbp, qword ptr [rsp + 0x68]
001E25DB  mov      rsi, qword ptr [rsp + 0x70]
001E25E0  mov      rdi, qword ptr [rsp + 0x78]
001E25E5  add      rsp, 0x40
001E25E9  pop      r15
001E25EB  pop      r14
001E25ED  pop      r12
001E25EF  ret      
```

## 001F2F50 (31 B, extent 001F2F50-001F2F6F)

Documented callee on this page: `00193D50`

```
001F2F50  push     rbx
001F2F52  sub      rsp, 0x20
001F2F56  mov      rbx, rcx
001F2F59  call     0x193d50  ; -> 00193D50 fn
001F2F5E  movzx    edx, byte ptr [rbx + 0x18]
001F2F62  mov      rcx, rax
001F2F65  add      rsp, 0x20
001F2F69  pop      rbx
001F2F6A  jmp      0x194240  ; -> 00194240 fn
```

## 00213040 (65 B, extent 00213040-00213081)

Documented callee on this page: `005FEFD0`

```
00213040  push     rbx
00213042  sub      rsp, 0x20
00213046  mov      rbx, rdx
00213049  mov      edx, 2
0021304E  mov      rcx, rbx
00213051  call     0x600a60  ; -> 00600A60 fn
00213056  call     0x189120  ; -> 00189120 fn
0021305B  mov      rcx, rax
0021305E  call     0x1893c0  ; -> 001893C0 fn
00213063  cmp      byte ptr [rip + 0x1dc0a56], 0  ; -> 01FD3AC0
0021306A  je       0x21307b  ; -> 0021307B
0021306C  xor      edx, edx
0021306E  mov      rcx, rbx
00213071  add      rsp, 0x20
00213075  pop      rbx
00213076  jmp      0x5fefd0  ; -> 005FEFD0 fn
0021307B  add      rsp, 0x20
0021307F  pop      rbx
00213080  ret      
```

## 002228A0 (381 B, extent 002228A0-00222A1D)

Documented callee on this page: `00221D10`

```
002228A0  mov      qword ptr [rsp + 8], rbx
002228A5  mov      qword ptr [rsp + 0x10], rbp
002228AA  push     rsi
002228AB  push     rdi
002228AC  push     r14
002228AE  sub      rsp, 0x50
002228B2  movaps   xmmword ptr [rsp + 0x30], xmm7
002228B7  mov      rbp, rcx
002228BA  movd     xmm7, r9d
002228BF  add      rcx, 0x38
002228C3  cvtdq2ps xmm7, xmm7
002228C6  mov      esi, r8d
002228C9  divss    xmm7, dword ptr [rip + 0x6d4483]  ; -> 008F6D54 [f32 60]
002228D1  call     0x7a7010  ; -> 007A7010 fn
002228D6  mov      ebx, eax
002228D8  call     0x210b30  ; -> 00210B30 fn
002228DD  xor      ecx, ecx
002228DF  mov      r14d, dword ptr [rax + 0x30]
002228E3  cmp      r14d, 2
002228E7  setbe    cl
002228EA  call     0x16d6a0  ; -> 0016D6A0 fn
002228EF  xor      ecx, ecx
002228F1  cmp      qword ptr [rbp + 0x48], rcx
002228F5  setne    cl
002228F8  call     0x16d6a0  ; -> 0016D6A0 fn
002228FD  test     ebx, ebx
002228FF  je       0x222924  ; -> 00222924
00222901  sub      ebx, 2
00222904  je       0x222a05  ; -> 00222A05
0022290A  cmp      ebx, 1
0022290D  jne      0x222950  ; -> 00222950
0022290F  or       r8d, 0xffffffff
00222913  lea      rcx, [rbp + 0x38]
00222917  xorps    xmm1, xmm1
0022291A  call     0x7a7a20  ; -> 007A7A20 fn
0022291F  jmp      0x222a05  ; -> 00222A05
00222924  mov      rcx, rbp
00222927  call     0x221d10  ; -> 00221D10 fn
0022292C  mov      dword ptr [rsp + 0x28], 0
00222934  lea      rdx, [rbp + 0x38]
00222938  xor      r9d, r9d
0022293B  mov      qword ptr [rsp + 0x20], 0
00222944  xor      r8d, r8d
00222947  lea      rcx, [rax + 8]
0022294B  call     0x7a86e0  ; -> 007A86E0 fn
00222950  call     0x221710  ; -> 00221710 fn
00222955  mov      edx, dword ptr [rbp + 0x50]
00222958  mov      rcx, rax
0022295B  call     0x221100  ; -> 00221100 fn
00222960  test     esi, esi
00222962  jle      0x22299f  ; -> 0022299F
00222964  movss    xmm2, dword ptr [rip + 0x1ac923c]  ; -> 01CEBBA8 [f32 1]
0022296C  lea      rdx, [rsp + 0x88]
00222974  dec      si
00222977  mov      word ptr [rsp + 0x8a], 0
00222981  mov      r9d, r14d
00222984  mov      word ptr [rsp + 0x88], si
0022298C  lea      rcx, [rbp + 0x38]
00222990  mov      dword ptr [rsp + 0x20], 0
00222998  call     0x7a92c0  ; -> 007A92C0 fn
0022299D  jmp      0x222a05  ; -> 00222A05
0022299F  test     al, al
002229A1  je       0x2229ea  ; -> 002229EA
002229A3  movaps   xmmword ptr [rsp + 0x40], xmm6
002229A8  call     0x221710  ; -> 00221710 fn
002229AD  mov      edx, dword ptr [rbp + 0x50]
002229B0  mov      rcx, rax
002229B3  call     0x220da0  ; -> 00220DA0 fn
002229B8  movaps   xmm6, xmm0
002229BB  call     0x221710  ; -> 00221710 fn
002229C0  mov      edx, dword ptr [rbp + 0x50]
002229C3  mov      rcx, rax
002229C6  call     0x221280  ; -> 00221280 fn
002229CB  movaps   xmm3, xmm7
002229CE  movss    dword ptr [rsp + 0x20], xmm6
002229D4  xor      r8d, r8d
002229D7  lea      rcx, [rbp + 0x38]
002229DB  mov      edx, r14d
002229DE  call     0x7a93a0  ; -> 007A93A0 fn
002229E3  movaps   xmm6, xmmword ptr [rsp + 0x40]
002229E8  jmp      0x222a05  ; -> 00222A05
002229EA  xorps    xmm0, xmm0
002229ED  lea      rcx, [rbp + 0x38]
002229F1  movaps   xmm3, xmm7
002229F4  movss    dword ptr [rsp + 0x20], xmm0
002229FA  xor      r8d, r8d
002229FD  mov      edx, r14d
00222A00  call     0x7a93a0  ; -> 007A93A0 fn
00222A05  mov      rbx, qword ptr [rsp + 0x70]
00222A0A  mov      rbp, qword ptr [rsp + 0x78]
00222A0F  movaps   xmm7, xmmword ptr [rsp + 0x30]
00222A14  add      rsp, 0x50
00222A18  pop      r14
00222A1A  pop      rdi
00222A1B  pop      rsi
00222A1C  ret      
```

## 00223030 (35 B, extent 00223030-00223053)

Documented callee on this page: `00223190`

```
00223030  sub      rsp, 0x48
00223034  mov      qword ptr [rsp + 0x30], r9
00223039  xor      r9d, r9d
0022303C  mov      byte ptr [rsp + 0x28], 1
00223041  mov      dword ptr [rsp + 0x20], 0
00223049  call     0x223190  ; -> 00223190 fn
0022304E  add      rsp, 0x48
00223052  ret      
```

## 00224900 (91 B, extent 00224900-0022495B)

Documented callee on this page: `00221E60`

```
00224900  mov      qword ptr [rsp + 8], rbx
00224905  push     rdi
00224906  sub      rsp, 0x20
0022490A  mov      edi, r9d
0022490D  test     edx, edx
0022490F  je       0x224918  ; -> 00224918
00224911  call     0x221ed0  ; -> 00221ED0 fn
00224916  jmp      0x224920  ; -> 00224920
00224918  mov      edx, r8d
0022491B  call     0x221e60  ; -> 00221E60 fn
00224920  mov      rbx, rax
00224923  test     rax, rax
00224926  je       0x22494e  ; -> 0022494E
00224928  mov      rcx, rax
0022492B  call     0x225680  ; -> 00225680 fn
00224930  test     eax, eax
00224932  je       0x22494e  ; -> 0022494E
00224934  xor      r8d, r8d
00224937  mov      edx, edi
00224939  mov      rcx, rbx
0022493C  call     0x2257e0  ; -> 002257E0 fn
00224941  mov      al, 1
00224943  mov      rbx, qword ptr [rsp + 0x30]
00224948  add      rsp, 0x20
0022494C  pop      rdi
0022494D  ret      
0022494E  xor      al, al
00224950  mov      rbx, qword ptr [rsp + 0x30]
00224955  add      rsp, 0x20
00224959  pop      rdi
0022495A  ret      
```

## 00224960 (106 B, extent 00224960-002249CA)

Documented callee on this page: `00221E60`

```
00224960  mov      qword ptr [rsp + 8], rbx
00224965  push     rdi
00224966  sub      rsp, 0x20
0022496A  mov      edi, r9d
0022496D  test     edx, edx
0022496F  je       0x224978  ; -> 00224978
00224971  call     0x221ed0  ; -> 00221ED0 fn
00224976  jmp      0x224980  ; -> 00224980
00224978  mov      edx, r8d
0022497B  call     0x221e60  ; -> 00221E60 fn
00224980  mov      rbx, rax
00224983  test     rax, rax
00224986  je       0x2249bd  ; -> 002249BD
00224988  mov      rcx, rax
0022498B  call     0x225680  ; -> 00225680 fn
00224990  test     eax, eax
00224992  je       0x2249bd  ; -> 002249BD
00224994  movd     xmm1, edi
00224998  lea      rcx, [rbx + 8]
0022499C  cvtdq2ps xmm1, xmm1
0022499F  or       r8d, 0xffffffff
002249A3  divss    xmm1, dword ptr [rip + 0x6d23a9]  ; -> 008F6D54 [f32 60]
002249AB  call     0x7a84a0  ; -> 007A84A0 fn
002249B0  mov      al, 1
002249B2  mov      rbx, qword ptr [rsp + 0x30]
002249B7  add      rsp, 0x20
002249BB  pop      rdi
002249BC  ret      
002249BD  xor      al, al
002249BF  mov      rbx, qword ptr [rsp + 0x30]
002249C4  add      rsp, 0x20
002249C8  pop      rdi
002249C9  ret      
```

## 002249D0 (93 B, extent 002249D0-00224A2D)

Documented callee on this page: `00221E60`

```
002249D0  mov      qword ptr [rsp + 8], rbx
002249D5  push     rdi
002249D6  sub      rsp, 0x20
002249DA  mov      edi, r9d
002249DD  test     edx, edx
002249DF  je       0x2249e8  ; -> 002249E8
002249E1  call     0x221ed0  ; -> 00221ED0 fn
002249E6  jmp      0x2249f0  ; -> 002249F0
002249E8  mov      edx, r8d
002249EB  call     0x221e60  ; -> 00221E60 fn
002249F0  mov      rbx, rax
002249F3  test     rax, rax
002249F6  je       0x224a20  ; -> 00224A20
002249F8  mov      rcx, rax
002249FB  call     0x225680  ; -> 00225680 fn
00224A00  test     eax, eax
00224A02  je       0x224a20  ; -> 00224A20
00224A04  mov      edx, dword ptr [rsp + 0x50]
00224A08  mov      r8d, edi
00224A0B  mov      rcx, rbx
00224A0E  call     0x2257e0  ; -> 002257E0 fn
00224A13  mov      al, 1
00224A15  mov      rbx, qword ptr [rsp + 0x30]
00224A1A  add      rsp, 0x20
00224A1E  pop      rdi
00224A1F  ret      
00224A20  xor      al, al
00224A22  mov      rbx, qword ptr [rsp + 0x30]
00224A27  add      rsp, 0x20
00224A2B  pop      rdi
00224A2C  ret      
```

## 00225400 (52 B, extent 00225400-00225434)

Documented callee on this page: `00221E60`

```
00225400  mov      qword ptr [rsp + 8], rbx
00225405  push     rdi
00225406  sub      rsp, 0x20
0022540A  xor      edx, edx
0022540C  mov      ebx, r9d
0022540F  mov      edi, r8d
00225412  call     0x221e60  ; -> 00221E60 fn
00225417  test     rax, rax
0022541A  je       0x225429  ; -> 00225429
0022541C  mov      r8d, edi
0022541F  mov      edx, ebx
00225421  mov      rcx, rax
00225424  call     0x2257e0  ; -> 002257E0 fn
00225429  mov      rbx, qword ptr [rsp + 0x30]
0022542E  add      rsp, 0x20
00225432  pop      rdi
00225433  ret      
```

## 00314B80 (37 B, extent 00314B80-00314BA5)

Documented callee on this page: `002EF2B0`

```
00314B80  push     rbx
00314B82  sub      rsp, 0x20
00314B86  mov      ebx, ecx
00314B88  call     0x2ef2b0  ; -> 002EF2B0 fn
00314B8D  and      byte ptr [rax + 0x1062], 0xfe
00314B94  test     ebx, ebx
00314B96  setne    cl
00314B99  or       byte ptr [rax + 0x1062], cl
00314B9F  add      rsp, 0x20
00314BA3  pop      rbx
00314BA4  ret      
```

## 00314BE0 (84 B, extent 00314BE0-00314C34)

Documented callee on this page: `002EF2B0`

```
00314BE0  push     rbx
00314BE2  sub      rsp, 0x20
00314BE6  mov      ebx, ecx
00314BE8  test     ecx, ecx
00314BEA  jg       0x314c0a  ; -> 00314C0A
00314BEC  call     0x2ef2b0  ; -> 002EF2B0 fn
00314BF1  and      byte ptr [rax + 0x1062], 0x7f
00314BF8  call     0x2ef2b0  ; -> 002EF2B0 fn
00314BFD  and      byte ptr [rax + 0x1063], 0xcf
00314C04  add      rsp, 0x20
00314C08  pop      rbx
00314C09  ret      
00314C0A  call     0x2ef2b0  ; -> 002EF2B0 fn
00314C0F  or       byte ptr [rax + 0x1062], 0x80
00314C16  call     0x2ef2b0  ; -> 002EF2B0 fn
00314C1B  and      bl, 3
00314C1E  shl      bl, 4
00314C21  and      byte ptr [rax + 0x1063], 0xcf
00314C28  or       byte ptr [rax + 0x1063], bl
00314C2E  add      rsp, 0x20
00314C32  pop      rbx
00314C33  ret      
```

## 00314C40 (35 B, extent 00314C40-00314C63)

Documented callee on this page: `002EF2B0`

```
00314C40  push     rbx
00314C42  sub      rsp, 0x20
00314C46  mov      ebx, ecx
00314C48  call     0x2ef2b0  ; -> 002EF2B0 fn
00314C4D  and      bl, 3
00314C50  and      byte ptr [rax + 0x1063], 0xfc
00314C57  or       byte ptr [rax + 0x1063], bl
00314C5D  add      rsp, 0x20
00314C61  pop      rbx
00314C62  ret      
```

## 00314CD0 (39 B, extent 00314CD0-00314CF7)

Documented callee on this page: `002EF2B0`

```
00314CD0  push     rbx
00314CD2  sub      rsp, 0x20
00314CD6  mov      ebx, ecx
00314CD8  call     0x2ef2b0  ; -> 002EF2B0 fn
00314CDD  and      byte ptr [rax + 0x1062], 0xfd
00314CE4  test     ebx, ebx
00314CE6  setne    cl
00314CE9  add      cl, cl
00314CEB  or       byte ptr [rax + 0x1062], cl
00314CF1  add      rsp, 0x20
00314CF5  pop      rbx
00314CF6  ret      
```

## 0032A860 (23 B, extent 0032A860-0032A877)

Documented callee on this page: `00309FB0`

```
0032A860  sub      rsp, 0x28
0032A864  xor      edx, edx
0032A866  call     0x309fb0  ; -> 00309FB0 fn
0032A86B  xor      ecx, ecx
0032A86D  test     eax, eax
0032A86F  cmovs    eax, ecx
0032A872  add      rsp, 0x28
0032A876  ret      
```

## 00341460 (62 B, extent 00341460-0034149E)

Documented callee on this page: `00267E10`

```
00341460  mov      qword ptr [rsp + 8], rbx
00341465  push     rdi
00341466  sub      rsp, 0x20
0034146A  mov      rcx, r9
0034146D  mov      rbx, r9
00341470  call     0x267e10  ; -> 00267E10 fn
00341475  mov      rcx, rbx
00341478  mov      edi, eax
0034147A  call     0x267e10  ; -> 00267E10 fn
0034147F  mov      ecx, edi
00341481  mov      ebx, eax
00341483  call     0x363b20  ; -> 00363B20 fn
00341488  mov      edx, ebx
0034148A  mov      ecx, 1
0034148F  mov      rbx, qword ptr [rsp + 0x30]
00341494  add      rsp, 0x20
00341498  pop      rdi
00341499  jmp      0x3631a0  ; -> 003631A0 fn
```

## 003417C0 (41 B, extent 003417C0-003417E9)

Documented callee on this page: `00267E10`

```
003417C0  push     rbx
003417C2  sub      rsp, 0x20
003417C6  mov      rcx, r9
003417C9  call     0x267e10  ; -> 00267E10 fn
003417CE  or       ecx, 0xffffffff
003417D1  mov      ebx, eax
003417D3  call     0x363b20  ; -> 00363B20 fn
003417D8  mov      edx, ebx
003417DA  mov      ecx, 1
003417DF  add      rsp, 0x20
003417E3  pop      rbx
003417E4  jmp      0x3631a0  ; -> 003631A0 fn
```

## 00342010 (45 B, extent 00342010-0034203D)

Documented callee on this page: `00267E10`

```
00342010  push     rbx
00342012  sub      rsp, 0x20
00342016  mov      rcx, r9
00342019  mov      rbx, rdx
0034201C  call     0x267e10  ; -> 00267E10 fn
00342021  cmp      byte ptr [rbx + 0x15], 3
00342025  mov      ecx, eax
00342027  jne      0x342033  ; -> 00342033
00342029  add      rsp, 0x20
0034202D  pop      rbx
0034202E  jmp      0x36e1a0  ; -> 0036E1A0 fn
00342033  add      rsp, 0x20
00342037  pop      rbx
00342038  jmp      0x36e160  ; -> 0036E160 fn
```

## 00343080 (55 B, extent 00343080-003430B7)

Documented callee on this page: `00267E10`

```
00343080  mov      qword ptr [rsp + 8], rbx
00343085  push     rdi
00343086  sub      rsp, 0x20
0034308A  mov      rcx, r9
0034308D  mov      rbx, rdx
00343090  call     0x267e10  ; -> 00267E10 fn
00343095  mov      rcx, rbx
00343098  mov      edi, eax
0034309A  call     0x2638c0  ; -> 002638C0 fn
0034309F  test     eax, eax
003430A1  je       0x3430ac  ; -> 003430AC
003430A3  mov      edx, edi
003430A5  mov      ecx, eax
003430A7  call     0x2eaea0  ; -> 002EAEA0 fn
003430AC  mov      rbx, qword ptr [rsp + 0x30]
003430B1  add      rsp, 0x20
003430B5  pop      rdi
003430B6  ret      
```

## 003437A0 (105 B, extent 003437A0-00343809)

Documented callee on this page: `00267E10`

```
003437A0  mov      qword ptr [rsp + 8], rbx
003437A5  mov      qword ptr [rsp + 0x10], rbp
003437AA  mov      qword ptr [rsp + 0x18], rsi
003437AF  mov      qword ptr [rsp + 0x20], rdi
003437B4  push     r14
003437B6  sub      rsp, 0x20
003437BA  mov      rbp, rcx
003437BD  mov      rdi, r9
003437C0  mov      rcx, r9
003437C3  mov      r14, r8
003437C6  mov      rsi, rdx
003437C9  call     0x267e10  ; -> 00267E10 fn
003437CE  mov      r9, rdi
003437D1  mov      r8, r14
003437D4  mov      rdx, rsi
003437D7  mov      rcx, rbp
003437DA  mov      ebx, eax
003437DC  call     0x342770  ; -> 00342770 fn
003437E1  and      byte ptr [r14 + 3], 0xbf
003437E6  mov      dword ptr [r14 + 0xc], ebx
003437EA  mov      rbx, qword ptr [rsp + 0x30]
003437EF  mov      rbp, qword ptr [rsp + 0x38]
003437F4  mov      rsi, qword ptr [rsp + 0x40]
003437F9  mov      rdi, qword ptr [rsp + 0x48]
003437FE  add      rsp, 0x20
00343802  pop      r14
00343804  jmp      0x25d5d0  ; -> 0025D5D0 fn
```

## 00344290 (51 B, extent 00344290-003442C3)

Documented callee on this page: `00267E10`

```
00344290  sub      rsp, 0x28
00344294  mov      rcx, r9
00344297  call     0x267e10  ; -> 00267E10 fn
0034429C  mov      edx, 1
003442A1  mov      ecx, eax
003442A3  mov      r8d, edx
003442A6  call     0x359ca0  ; -> 00359CA0 fn
003442AB  test     rax, rax
003442AE  je       0x3442be  ; -> 003442BE
003442B0  xor      edx, edx
003442B2  mov      rcx, rax
003442B5  add      rsp, 0x28
003442B9  jmp      0x26ae90  ; -> 0026AE90 fn
003442BE  add      rsp, 0x28
003442C2  ret      
```

## 00346750 (35 B, extent 00346750-00346773)

Documented callee on this page: `00267E10`

```
00346750  push     rbx
00346752  sub      rsp, 0x20
00346756  mov      rcx, r9
00346759  call     0x267e10  ; -> 00267E10 fn
0034675E  mov      ecx, eax
00346760  mov      ebx, eax
00346762  call     0x16d6a0  ; -> 0016D6A0 fn
00346767  mov      ecx, ebx
00346769  add      rsp, 0x20
0034676D  pop      rbx
0034676E  jmp      0x3eb6c0  ; -> 003EB6C0 fn
```

## 00347D90 (53 B, extent 00347D90-00347DC5)

Documented callee on this page: `00267E10`

```
00347D90  mov      qword ptr [rsp + 8], rbx
00347D95  push     rdi
00347D96  sub      rsp, 0x20
00347D9A  mov      rcx, r9
00347D9D  mov      rdi, rdx
00347DA0  call     0x267e10  ; -> 00267E10 fn
00347DA5  mov      edx, eax
00347DA7  mov      rcx, rdi
00347DAA  mov      ebx, eax
00347DAC  call     0x2e8c10  ; -> 002E8C10 fn
00347DB1  mov      edx, ebx
00347DB3  mov      rcx, rdi
00347DB6  mov      rbx, qword ptr [rsp + 0x30]
00347DBB  add      rsp, 0x20
00347DBF  pop      rdi
00347DC0  jmp      0x2ed200  ; -> 002ED200 fn
```

## 00349080 (101 B, extent 00349080-003490E5)

Documented callee on this page: `002640E0`

```
00349080  mov      qword ptr [rsp + 8], rbx
00349085  mov      qword ptr [rsp + 0x10], rbp
0034908A  mov      qword ptr [rsp + 0x18], rsi
0034908F  push     rdi
00349090  sub      rsp, 0x20
00349094  mov      rsi, rcx
00349097  mov      rbx, r9
0034909A  mov      rcx, rdx
0034909D  mov      rdi, r8
003490A0  mov      rbp, rdx
003490A3  call     0x2640e0  ; -> 002640E0 fn
003490A8  movaps   xmm1, xmm0
003490AB  mov      rcx, rbx
003490AE  call     0x267f60  ; -> 00267F60 fn
003490B3  mov      r9, rbx
003490B6  mov      r8, rdi
003490B9  mov      rdx, rbp
003490BC  mov      rcx, rsi
003490BF  call     0x357980  ; -> 00357980 fn
003490C4  mov      edx, 2
003490C9  mov      rcx, rbp
003490CC  mov      rbx, qword ptr [rsp + 0x30]
003490D1  mov      rbp, qword ptr [rsp + 0x38]
003490D6  mov      rsi, qword ptr [rsp + 0x40]
003490DB  add      rsp, 0x20
003490DF  pop      rdi
003490E0  jmp      0x26c120  ; -> 0026C120 fn
```

## 00349150 (48 B, extent 00349150-00349180)

Documented callee on this page: `00265200`

```
00349150  push     rbx
00349152  sub      rsp, 0x20
00349156  mov      rbx, rcx
00349159  mov      rcx, r9
0034915C  call     0x267e10  ; -> 00267E10 fn
00349161  mov      ecx, eax
00349163  call     0x264010  ; -> 00264010 fn
00349168  mov      rcx, rax
0034916B  call     0x265200  ; -> 00265200 fn
00349170  movaps   xmm1, xmm0
00349173  mov      rcx, rbx
00349176  add      rsp, 0x20
0034917A  pop      rbx
0034917B  jmp      0x26b4c0  ; -> 0026B4C0 fn
```

## 00349D90 (117 B, extent 00349D90-00349E05)

Documented callee on this page: `002640E0`

```
00349D90  mov      qword ptr [rsp + 8], rbx
00349D95  mov      qword ptr [rsp + 0x10], rbp
00349D9A  mov      qword ptr [rsp + 0x18], rsi
00349D9F  push     rdi
00349DA0  sub      rsp, 0x20
00349DA4  mov      rsi, rcx
00349DA7  mov      rbx, r9
00349DAA  mov      rcx, rdx
00349DAD  mov      rdi, r8
00349DB0  mov      rbp, rdx
00349DB3  call     0x2640e0  ; -> 002640E0 fn
00349DB8  movaps   xmm1, xmm0
00349DBB  mov      rcx, rbx
00349DBE  call     0x267f60  ; -> 00267F60 fn
00349DC3  mov      r9, rbx
00349DC6  mov      r8, rdi
00349DC9  mov      rdx, rbp
00349DCC  mov      rcx, rsi
00349DCF  call     0x357980  ; -> 00357980 fn
00349DD4  mov      rcx, rbp
00349DD7  call     0x263f40  ; -> 00263F40 fn
00349DDC  mov      rcx, rax
00349DDF  call     0x2eb430  ; -> 002EB430 fn
00349DE4  mov      edx, 2
00349DE9  mov      rcx, rbp
00349DEC  mov      rbx, qword ptr [rsp + 0x30]
00349DF1  mov      rbp, qword ptr [rsp + 0x38]
00349DF6  mov      rsi, qword ptr [rsp + 0x40]
00349DFB  add      rsp, 0x20
00349DFF  pop      rdi
00349E00  jmp      0x26c120  ; -> 0026C120 fn
```

## 003513B0 (57 B, extent 003513B0-003513E9)

Documented callee on this page: `00267E10`

```
003513B0  mov      qword ptr [rsp + 8], rbx
003513B5  push     rdi
003513B6  sub      rsp, 0x20
003513BA  mov      rcx, r9
003513BD  mov      rbx, r9
003513C0  call     0x267e10  ; -> 00267E10 fn
003513C5  mov      rcx, rbx
003513C8  mov      edi, eax
003513CA  call     0x267e10  ; -> 00267E10 fn
003513CF  mov      ecx, edi
003513D1  mov      ebx, eax
003513D3  call     0x379980  ; -> 00379980 fn
003513D8  mov      ecx, ebx
003513DA  mov      rbx, qword ptr [rsp + 0x30]
003513DF  add      rsp, 0x20
003513E3  pop      rdi
003513E4  jmp      0x379990  ; -> 00379990 fn
```

## 005D8E40 (103 B, extent 005D8E40-005D8EA7)

Documented callee on this page: `00615C90`

```
005D8E40  push     rdi
005D8E42  sub      rsp, 0x30
005D8E46  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005D8E4F  mov      qword ptr [rsp + 0x40], rbx
005D8E54  mov      rdi, rdx
005D8E57  xor      r9d, r9d
005D8E5A  lea      r8, [rip + 0x26de83f]  ; -> 02CB76A0
005D8E61  lea      edx, [r9 + 1]
005D8E65  call     0x6394e0  ; -> 006394E0 fn
005D8E6A  test     rax, rax
005D8E6D  jne      0x5d8e76  ; -> 005D8E76
005D8E6F  mov      qword ptr [rsp + 0x50], rax
005D8E74  jmp      0x5d8e84  ; -> 005D8E84
005D8E76  mov      rbx, qword ptr [rax + 0x60]
005D8E7A  mov      qword ptr [rsp + 0x50], rbx
005D8E7F  test     rbx, rbx
005D8E82  jne      0x5d8e88  ; -> 005D8E88
005D8E84  xor      eax, eax
005D8E86  jmp      0x5d8e9c  ; -> 005D8E9C
005D8E88  mov      qword ptr [rsp + 0x58], rbx
005D8E8D  mov      rdx, rdi
005D8E90  mov      rcx, rbx
005D8E93  call     0x615c90  ; -> 00615C90 fn
005D8E98  nop      
005D8E99  mov      rax, rbx
005D8E9C  mov      rbx, qword ptr [rsp + 0x40]
005D8EA1  add      rsp, 0x30
005D8EA5  pop      rdi
005D8EA6  ret      
```

## 00863350 (94 B, extent 00863350-008633AE)

Documented callee on this page: `00809950`

```
00863350  mov      qword ptr [rsp + 8], rbx
00863355  push     rdi
00863356  sub      rsp, 0x20
0086335A  lea      rax, [rip + 0x146c70f]  ; -> 01CCFA70
00863361  mov      rbx, rcx
00863364  mov      qword ptr [rcx], rax
00863367  mov      edi, edx
00863369  mov      rcx, qword ptr [rcx + 8]
0086336D  test     rcx, rcx
00863370  je       0x86338d  ; -> 0086338D
00863372  xor      edx, edx
00863374  call     qword ptr [rip + 0x5f086]  ; -> 008C2400 [u64 0x0000000001CCF75E]
0086337A  mov      rcx, qword ptr [rbx + 8]
0086337E  call     qword ptr [rip + 0x5f05c]  ; -> 008C23E0 [u64 0x0000000001CCC076]
00863384  xor      eax, eax
00863386  mov      qword ptr [rbx + 8], rax
0086338A  mov      dword ptr [rbx + 0x10], eax
0086338D  test     dil, 1
00863391  je       0x8633a0  ; -> 008633A0
00863393  mov      edx, 0x18
00863398  mov      rcx, rbx
0086339B  call     0x809950  ; -> 00809950 fn
008633A0  mov      rax, rbx
008633A3  mov      rbx, qword ptr [rsp + 0x30]
008633A8  add      rsp, 0x20
008633AC  pop      rdi
008633AD  ret      
```
