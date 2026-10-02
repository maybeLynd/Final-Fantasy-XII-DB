# F-interior pack: `00-Engine-Core-Runtime/CONTRACT-boot-fixups.md`

Generated 2026-10-02 18:33 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/contract-boot-fixups.json`.

Functions: 13. Each is cited on the page only at its entry and is still in the F frontier.

## 00259370 (35 B, extent 00259370-00259393)

Page context: "es the count, a nonpositive answer just clears '02098DF0', otherwise it arms the '0036C1D0(6, 5)'/'0036C1A0(3)'/'0036A190(count)'/'0036C110'/'0036C140' pool sequence and '0032E620'-spawns with entry '00259370' and the '{0, ebx}' stack packet  Interior anchor '00259DFE' (function '00259DF0').  '004DA3C0' (157 B) is one of the '0037E0F0' battery's static-record initializers: '00861EC0' zeroes '0x70' and '008631D0(rcx, 6)' lays the base, t"

```
00259370  mov      eax, ecx
00259372  mov      qword ptr [rip + 0x1e3fa77], rax  ; -> 02098DF0
00259379  test     ecx, ecx
0025937B  je       0x259392  ; -> 00259392
0025937D  cmp      dword ptr [rax + 4], 0
00259381  jle      0x259392  ; -> 00259392
00259383  mov      dword ptr [rip + 0x1e3fa6b], 0  ; -> 02098DF8
0025938D  jmp      0x259fe0  ; -> 00259FE0 fn
00259392  ret      
```

## 004C2160 (5292 B, extent 004C2160-004C360C)

Page context: "00'/'0x412412'/'0x457FA000' constants - a module record's init.  Interior anchor '004D3E37' (function '004D3E20').  '004C3610' (426 B) is a battery constructor '0037E0F0' calls: '008631E0' registers '004C2160', '008631D0(0x11)' fills '+0x10', then '+0x8' = 0x03000000, '+0xC' = 0x02000000, '+0x18' = 0x1000404, '+0x1C' = 0x6C0E0000, '+0x24' = 0x20204000, '+0x28' = 0x41, '+0x30'/'+0x34' = 0x457FA000 - a module record's init.  Interior anch"

```
004C2160  push     rbp
004C2162  push     rsi
004C2163  push     rdi
004C2164  sub      rsp, 0xe0
004C216B  movzx    eax, word ptr [rip + 0x1ba299a]  ; -> 02064B0C
004C2172  lea      rbp, [rip + 0x1ba2cb7]  ; -> 02064E30
004C2179  add      ax, 0xb
004C217D  movaps   xmmword ptr [rsp + 0xb0], xmm7
004C2185  mov      word ptr [rip + 0x1ba2c5c], ax  ; -> 02064DE8
004C218C  mov      rsi, rcx
004C218F  cwde     
004C2190  xor      r8d, r8d
004C2193  shl      eax, 4
004C2196  mov      rdi, rdx
004C2199  movsxd   rcx, eax
004C219C  add      rcx, rbp
004C219F  call     rsi
004C21A1  movsx    edx, word ptr [rip + 0x1ba2964]  ; -> 02064B0C
004C21A8  mov      eax, 0x80
004C21AD  movss    xmm7, dword ptr [rip + 0x194067b]  ; -> 01E02830 [u32 0x00000000]
004C21B5  add      eax, edx
004C21B7  mov      word ptr [rip + 0x1ba2bf2], ax  ; -> 02064DB0
004C21BE  mov      r8d, edx
004C21C1  inc      ax
004C21C4  mov      word ptr [rip + 0x1ba2bed], dx  ; -> 02064DB8
004C21CB  mov      word ptr [rip + 0x1ba2be2], ax  ; -> 02064DB4
004C21D2  lea      eax, [rdx + 2]
004C21D5  shl      eax, 4
004C21D8  movsxd   rcx, eax
004C21DB  lea      eax, [r8 + 1]
004C21DF  shl      eax, 4
004C21E2  mov      word ptr [rip + 0x1ba2be7], dx  ; -> 02064DD0
004C21E9  add      dx, 0x14
004C21ED  mov      word ptr [rip + 0x1ba2be4], dx  ; -> 02064DD8
004C21F4  movzx    r9d, word ptr [rcx + rbp]
004C21F9  movsxd   rcx, eax
004C21FC  lea      eax, [r8 + 3]
004C2200  shl      eax, 4
004C2203  mov      word ptr [rip + 0x1ba2bb1], r9w  ; -> 02064DBC
004C220B  mov      dword ptr [rip + 0x1ba28e7], 1  ; -> 02064AFC
004C2215  movups   xmm0, xmmword ptr [rcx + rbp]
004C2219  movsxd   rcx, eax
004C221C  lea      eax, [r8 + 4]
004C2220  shl      eax, 4
004C2223  movups   xmmword ptr [rip + 0x1ba2906], xmm0  ; -> 02064B30
004C222A  movups   xmm2, xmmword ptr [rcx + rbp]
004C222E  movsxd   rcx, eax
004C2231  lea      eax, [r8 + 5]
004C2235  shl      eax, 4
004C2238  movups   xmmword ptr [rip + 0x1ba2981], xmm2  ; -> 02064BC0
004C223F  movups   xmm1, xmmword ptr [rcx + rbp]
004C2243  movsxd   rcx, eax
004C2246  lea      eax, [r8 + 6]
004C224A  shl      eax, 4
004C224D  mulss    xmm2, xmm1
004C2251  movups   xmm0, xmmword ptr [rcx + rbp]
004C2255  movsxd   rcx, eax
004C2258  lea      eax, [r8 + 7]
004C225C  shl      eax, 4
004C225F  maxss    xmm2, xmm7
004C2263  movups   xmmword ptr [rip + 0x1ba2976], xmm0  ; -> 02064BE0
004C226A  movups   xmm0, xmmword ptr [rcx + rbp]
004C226E  movsxd   rcx, eax
004C2271  lea      eax, [r8 + 8]
004C2275  shl      eax, 4
004C2278  movups   xmmword ptr [rip + 0x1ba2971], xmm0  ; -> 02064BF0
004C227F  movups   xmm0, xmmword ptr [rcx + rbp]
004C2283  movsxd   rcx, eax
004C2286  lea      eax, [r8 + 9]
004C228A  shl      eax, 4
004C228D  movups   xmmword ptr [rip + 0x1ba2a4c], xmm0  ; -> 02064CE0
004C2294  movups   xmm0, xmmword ptr [rcx + rbp]
004C2298  movsxd   rcx, eax
004C229B  lea      eax, [r8 + 0xa]
004C229F  shl      eax, 4
004C22A2  movups   xmmword ptr [rip + 0x1ba2a47], xmm0  ; -> 02064CF0
004C22A9  movups   xmm0, xmmword ptr [rcx + rbp]
004C22AD  movsxd   rcx, eax
004C22B0  movups   xmmword ptr [rip + 0x1ba2919], xmm1  ; -> 02064BD0
004C22B7  movss    xmm1, dword ptr [rip + 0x1ba2905]  ; -> 02064BC4
004C22BF  movups   xmmword ptr [rip + 0x1ba2a3a], xmm0  ; -> 02064D00
004C22C6  movups   xmm0, xmmword ptr [rcx + rbp]
004C22CA  movss    dword ptr [rip + 0x1ba28ee], xmm2  ; -> 02064BC0
004C22D2  movups   xmmword ptr [rip + 0x1ba2a37], xmm0  ; -> 02064D10
004C22D9  movss    dword ptr [rip + 0x1940547], xmm1  ; -> 01E02828 [f32 1]
004C22E1  mov      eax, dword ptr [rip + 0x1940541]  ; -> 01E02828 [f32 1]
004C22E7  mov      ecx, eax
004C22E9  shr      ecx, 0x12
004C22EC  xor      ecx, eax
004C22EE  and      eax, 0x3fffff
004C22F3  or       eax, 0x1fc00000
004C22F8  shr      ecx, 4
004C22FB  add      eax, eax
004C22FD  and      ecx, 1
004C2300  or       ecx, eax
004C2302  mov      eax, ecx
004C2304  shr      eax, 0x12
004C2307  xor      eax, ecx
004C2309  and      ecx, 0x3fffff
004C230F  shr      eax, 4
004C2312  or       ecx, 0x1fc00000
004C2318  add      ecx, ecx
004C231A  and      eax, 1
004C231D  or       eax, ecx
004C231F  mov      ecx, eax
004C2321  shr      ecx, 0x12
004C2324  xor      ecx, eax
004C2326  and      eax, 0x3fffff
004C232B  or       eax, 0x1fc00000
004C2330  shr      ecx, 4
004C2333  add      eax, eax
004C2335  and      ecx, 1
004C2338  or       ecx, eax
004C233A  mov      edx, ecx
004C233C  shr      edx, 0x12
004C233F  xor      edx, ecx
004C2341  and      ecx, 0x3fffff
004C2347  shr      edx, 4
004C234A  or       ecx, 0x1fc00000
004C2350  and      edx, 1
004C2353  add      ecx, ecx
004C2355  or       edx, ecx
004C2357  mov      eax, edx
004C2359  shr      eax, 0x12
004C235C  xor      eax, edx
004C235E  and      edx, 0x3fffff
004C2364  shr      eax, 4
004C2367  or       edx, 0x1fc00000
004C236D  add      edx, edx
004C236F  and      eax, 1
004C2372  or       eax, edx
004C2374  mov      dword ptr [rip + 0x19404ae], eax  ; -> 01E02828 [f32 1]
004C237A  movss    xmm2, dword ptr [rip + 0x19404a6]  ; -> 01E02828 [f32 1]
004C2382  movss    dword ptr [rip + 0x1ba2926], xmm2  ; -> 02064CB0
004C238A  test     r9w, r9w
004C238E  jle      0x4c35f9  ; -> 004C35F9
004C2394  movss    xmm4, dword ptr [rip + 0x194049c]  ; -> 01E02838 [u32 0x00000000]
004C239C  movss    xmm5, dword ptr [rip + 0x1940490]  ; -> 01E02834 [u32 0x00000000]
004C23A4  mov      qword ptr [rsp + 0xd8], rbx
004C23AC  mov      qword ptr [rsp + 0xd0], r14
004C23B4  mov      r14d, 0xe0
004C23BA  movaps   xmmword ptr [rsp + 0xc0], xmm6
004C23C2  movaps   xmmword ptr [rsp + 0xa0], xmm8
004C23CB  movss    xmm8, dword ptr [rip + 0x18298c8]  ; -> 01CEBC9C [f32 -1]
004C23D4  movaps   xmmword ptr [rsp + 0x90], xmm9
004C23DD  movss    xmm9, dword ptr [rip + 0x1940456]  ; -> 01E0283C [f32 1]
004C23E6  movaps   xmmword ptr [rsp + 0x80], xmm10
004C23EF  movss    xmm10, dword ptr [rip + 0x84e4a8]  ; -> 00D108A0 [f32 1e-05]
004C23F8  movaps   xmmword ptr [rsp + 0x70], xmm11
004C23FE  movss    xmm11, dword ptr [rip + 0x43df59]  ; -> 00900360 [u32 0x7F7FFFFF]
004C2407  movaps   xmmword ptr [rsp + 0x60], xmm12
004C240D  movss    xmm12, dword ptr [rip + 0x1829862]  ; -> 01CEBC78 [f32 6.283185]
004C2416  movaps   xmmword ptr [rsp + 0x50], xmm13
004C241C  movss    xmm13, dword ptr [rip + 0x43f717]  ; -> 00901B3C [f32 1.5]
004C2425  movaps   xmmword ptr [rsp + 0x40], xmm14
004C242B  movaps   xmmword ptr [rsp + 0x30], xmm15
004C2431  movss    xmm15, dword ptr [rip + 0x182976e]  ; -> 01CEBBA8 [f32 1]
004C243A  nop      word ptr [rax + rax]
004C2440  addss    xmm4, xmm4
004C2444  mov      dword ptr [rip + 0x1ba26b6], 0x3727c5ac  ; -> 02064B04
004C244E  subss    xmm2, xmm9
004C2453  movaps   xmm3, xmm5
004C2456  addss    xmm3, xmm5
004C245A  movaps   xmm1, xmm9
004C245E  dec      r9w
004C2462  mov      word ptr [rip + 0x1ba2952], r9w  ; -> 02064DBC
004C246A  movss    dword ptr [rip + 0x1ba27d6], xmm4  ; -> 02064C48
004C2472  movaps   xmm4, xmm7
004C2475  movaps   xmm0, xmm2
004C2478  subss    xmm4, xmm10
004C247D  mulss    xmm0, dword ptr [rip + 0x1ba274f]  ; -> 02064BD4
004C2485  mulss    xmm2, dword ptr [rip + 0x1ba273f]  ; -> 02064BCC
004C248D  movss    dword ptr [rip + 0x1ba27bf], xmm0  ; -> 02064C54
004C2495  movaps   xmm0, xmm7
004C2498  mulss    xmm4, xmm3
004C249C  addss    xmm2, dword ptr [rip + 0x1ba2724]  ; -> 02064BC8
004C24A4  movss    dword ptr [rip + 0x1ba2798], xmm3  ; -> 02064C44
004C24AC  movss    dword ptr [rip + 0x1ba2810], xmm3  ; -> 02064CC4
004C24B4  addss    xmm0, xmm2
004C24B8  mulss    xmm1, xmm2
004C24BC  movaps   xmm2, xmm5
004C24BF  addss    xmm5, xmm10
004C24C4  addss    xmm2, xmm9
004C24C9  movss    dword ptr [rip + 0x1ba277b], xmm1  ; -> 02064C4C
004C24D1  movss    dword ptr [rip + 0x1ba2767], xmm0  ; -> 02064C40
004C24D9  movaps   xmm0, xmm7
004C24DC  addss    xmm0, xmm9
004C24E1  addss    xmm7, xmm1
004C24E5  mulss    xmm0, xmm7
004C24E9  mulss    xmm5, xmm7
004C24ED  addss    xmm4, xmm0
004C24F1  movss    dword ptr [rip + 0x1ba2627], xmm0  ; -> 02064B20
004C24F9  movaps   xmm0, xmm3
004C24FC  movss    dword ptr [rip + 0x1ba27bc], xmm7  ; -> 02064CC0
004C2504  mulss    xmm0, xmm2
004C2508  movss    dword ptr [rip + 0x1ba2614], xmm5  ; -> 02064B24
004C2510  movss    dword ptr [rip + 0x1ba27b8], xmm4  ; -> 02064CD0
004C2518  subss    xmm4, xmm7
004C251C  addss    xmm0, xmm5
004C2520  xorps    xmm7, xmm7
004C2523  ucomiss  xmm4, xmm7
004C2526  movss    dword ptr [rip + 0x1ba27a6], xmm0  ; -> 02064CD4
004C252E  subss    xmm0, xmm3
004C2532  movss    dword ptr [rip + 0x1ba2776], xmm4  ; -> 02064CB0
004C253A  movss    dword ptr [rip + 0x1ba2772], xmm0  ; -> 02064CB4
004C2542  jp       0x4c2546  ; -> 004C2546
004C2544  je       0x4c254d  ; -> 004C254D
004C2546  ucomiss  xmm0, xmm7
004C2549  jp       0x4c2562  ; -> 004C2562
004C254B  jne      0x4c2562  ; -> 004C2562
004C254D  call     0x22cc40  ; -> 0022CC40 fn
004C2552  movss    xmm0, dword ptr [rip + 0x1ba275a]  ; -> 02064CB4
004C255A  movss    xmm4, dword ptr [rip + 0x1ba274e]  ; -> 02064CB0
004C2562  comiss   xmm7, xmm4
004C2565  ja       0x4c256c  ; -> 004C256C
004C2567  comiss   xmm7, xmm0
004C256A  jbe      0x4c2571  ; -> 004C2571
004C256C  call     0x22cc30  ; -> 0022CC30 fn
004C2571  call     0x22cc20  ; -> 0022CC20 fn
004C2576  movss    xmm2, dword ptr [rip + 0x1ba2736]  ; -> 02064CB4
004C257E  movss    xmm0, dword ptr [rip + 0x1ba272a]  ; -> 02064CB0
004C2586  movss    xmm6, dword ptr [rip + 0x19402ae]  ; -> 01E0283C [f32 1]
004C258E  mulss    xmm0, xmm0
004C2592  movaps   xmm1, xmm6
004C2595  mulss    xmm2, xmm2
004C2599  mulss    xmm1, xmm0
004C259D  movaps   xmm0, xmm6
004C25A0  mulss    xmm0, xmm2
004C25A4  movss    dword ptr [rip + 0x1ba2708], xmm2  ; -> 02064CB4
004C25AC  movss    dword ptr [rip + 0x1ba2578], xmm1  ; -> 02064B2C
004C25B4  addss    xmm0, xmm1
004C25B8  movss    dword ptr [rip + 0x1ba26fc], xmm0  ; -> 02064CBC
004C25C0  cvtps2pd xmm0, xmm0
004C25C3  andps    xmm0, xmmword ptr [rip + 0x18297b6]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
004C25CA  cvtpd2ps xmm0, xmm0
004C25CE  call     0x861f14  ; -> 00861F14 fn
004C25D3  cmp      dword ptr [rip + 0x1ba2522], 0  ; -> 02064AFC
004C25DA  je       0x4c2683  ; -> 004C2683
004C25E0  mov      eax, dword ptr [rip + 0x1940242]  ; -> 01E02828 [f32 1]
004C25E6  mov      ecx, eax
004C25E8  shr      ecx, 0x12
004C25EB  xor      ecx, eax
004C25ED  and      eax, 0x3fffff
004C25F2  or       eax, 0x1fc00000
004C25F7  shr      ecx, 4
004C25FA  add      eax, eax
004C25FC  and      ecx, 1
004C25FF  or       ecx, eax
004C2601  mov      eax, ecx
004C2603  shr      eax, 0x12
004C2606  xor      eax, ecx
004C2608  and      ecx, 0x3fffff
004C260E  or       ecx, 0x1fc00000
004C2614  shr      eax, 4
004C2617  add      ecx, ecx
004C2619  and      eax, 1
004C261C  or       eax, ecx
004C261E  mov      ecx, eax
004C2620  shr      ecx, 0x12
004C2623  xor      ecx, eax
004C2625  and      eax, 0x3fffff
004C262A  or       eax, 0x1fc00000
004C262F  shr      ecx, 4
004C2632  add      eax, eax
004C2634  and      ecx, 1
004C2637  or       ecx, eax
004C2639  mov      edx, ecx
004C263B  shr      edx, 0x12
004C263E  xor      edx, ecx
004C2640  and      ecx, 0x3fffff
004C2646  shr      edx, 4
004C2649  or       ecx, 0x1fc00000
004C264F  and      edx, 1
004C2652  add      ecx, ecx
004C2654  or       edx, ecx
004C2656  mov      eax, edx
004C2658  shr      eax, 0x12
004C265B  xor      eax, edx
004C265D  and      edx, 0x3fffff
004C2663  or       edx, 0x1fc00000
004C2669  shr      eax, 4
004C266C  add      edx, edx
004C266E  and      eax, 1
004C2671  or       eax, edx
004C2673  mov      dword ptr [rip + 0x19401af], eax  ; -> 01E02828 [f32 1]
004C2679  movss    xmm1, dword ptr [rip + 0x19401a7]  ; -> 01E02828 [f32 1]
004C2681  jmp      0x4c2687  ; -> 004C2687
004C2683  movaps   xmm1, xmm15
004C2687  movss    xmm2, dword ptr [rip + 0x19401a1]  ; -> 01E02830 [u32 0x00000000]
004C268F  subss    xmm1, xmm6
004C2693  movaps   xmm3, xmm2
004C2696  mov      dword ptr [rip + 0x1ba2464], 0x3727c5ac  ; -> 02064B04
004C26A0  addss    xmm3, xmm0
004C26A4  movss    dword ptr [rip + 0x1ba2618], xmm1  ; -> 02064CC4
004C26AC  mulss    xmm1, dword ptr [rip + 0x1ba2528]  ; -> 02064BDC
004C26B4  ucomiss  xmm3, xmm7
004C26B7  movss    dword ptr [rip + 0x1ba260d], xmm1  ; -> 02064CCC
004C26BF  addss    xmm1, dword ptr [rip + 0x1ba2511]  ; -> 02064BD8
004C26C7  addss    xmm1, dword ptr [rip + 0x1ba2585]  ; -> 02064C54
004C26CF  movaps   xmm0, xmm1
004C26D2  movss    dword ptr [rip + 0x1ba25ee], xmm1  ; -> 02064CC8
004C26DA  addss    xmm0, dword ptr [rip + 0x1940156]  ; -> 01E02838 [u32 0x00000000]
004C26E2  movss    dword ptr [rip + 0x1ba254e], xmm0  ; -> 02064C38
004C26EA  jp       0x4c26f4  ; -> 004C26F4
004C26EC  jne      0x4c26f4  ; -> 004C26F4
004C26EE  movaps   xmm1, xmm11
004C26F2  jmp      0x4c26f8  ; -> 004C26F8
004C26F4  divss    xmm1, xmm3
004C26F8  addss    xmm2, xmm1
004C26FC  movss    dword ptr [rip + 0x1ba23fc], xmm1  ; -> 02064B00
004C2704  movss    dword ptr [rip + 0x1ba25b4], xmm2  ; -> 02064CC0
004C270C  mulss    xmm2, xmm10
004C2711  movss    dword ptr [rip + 0x1ba2507], xmm2  ; -> 02064C20
004C2719  mulss    xmm2, dword ptr [rip + 0x1ba249f]  ; -> 02064BC0
004C2721  movss    dword ptr [rip + 0x1ba2587], xmm2  ; -> 02064CB0
004C2729  call     0x5375f0  ; -> 005375F0 fn
004C272E  call     0x5376d0  ; -> 005376D0 fn
004C2733  movss    xmm2, dword ptr [rip + 0x19400f5]  ; -> 01E02830 [u32 0x00000000]
004C273B  movss    xmm1, dword ptr [rip + 0x19400f1]  ; -> 01E02834 [u32 0x00000000]
004C2743  movaps   xmm3, xmm2
004C2746  movss    xmm5, dword ptr [rip + 0x1ba2572]  ; -> 02064CC0
004C274E  movaps   xmm4, xmm1
004C2751  movss    xmm0, dword ptr [rip + 0x1ba256b]  ; -> 02064CC4
004C2759  addss    xmm3, xmm5
004C275D  mov      edx, dword ptr [rip + 0x1ba2399]  ; -> 02064AFC
004C2763  addss    xmm4, xmm0
004C2767  movss    dword ptr [rip + 0x1ba2501], xmm3  ; -> 02064C70
004C276F  movss    dword ptr [rip + 0x1ba24fd], xmm4  ; -> 02064C74
004C2777  test     edx, edx
004C2779  je       0x4c27a4  ; -> 004C27A4
004C277B  mov      eax, dword ptr [rip + 0x19400a7]  ; -> 01E02828 [f32 1]
004C2781  mov      ecx, eax
004C2783  shr      ecx, 0x12
004C2786  xor      ecx, eax
004C2788  and      eax, 0x3fffff
004C278D  or       eax, 0x1fc00000
004C2792  shr      ecx, 4
004C2795  add      eax, eax
004C2797  and      ecx, 1
004C279A  or       ecx, eax
004C279C  mov      dword ptr [rip + 0x1940086], ecx  ; -> 01E02828 [f32 1]
004C27A2  jmp      0x4c27aa  ; -> 004C27AA
004C27A4  mov      ecx, dword ptr [rip + 0x194007e]  ; -> 01E02828 [f32 1]
004C27AA  addss    xmm2, xmm0
004C27AE  movss    dword ptr [rip + 0x1ba24aa], xmm2  ; -> 02064C60
004C27B6  test     edx, edx
004C27B8  je       0x4c27db  ; -> 004C27DB
004C27BA  mov      eax, ecx
004C27BC  shr      ecx, 0x12
004C27BF  xor      ecx, eax
004C27C1  and      eax, 0x3fffff
004C27C6  or       eax, 0x1fc00000
004C27CB  shr      ecx, 4
004C27CE  add      eax, eax
004C27D0  and      ecx, 1
004C27D3  or       ecx, eax
004C27D5  mov      dword ptr [rip + 0x194004d], ecx  ; -> 01E02828 [f32 1]
004C27DB  addss    xmm1, xmm5
004C27DF  mulss    xmm1, xmm8
004C27E4  movss    dword ptr [rip + 0x1ba2478], xmm1  ; -> 02064C64
004C27EC  test     edx, edx
004C27EE  je       0x4c2811  ; -> 004C2811
004C27F0  mov      eax, ecx
004C27F2  shr      ecx, 0x12
004C27F5  xor      ecx, eax
004C27F7  and      eax, 0x3fffff
004C27FC  or       eax, 0x1fc00000
004C2801  shr      ecx, 4
004C2804  add      eax, eax
004C2806  and      ecx, 1
004C2809  or       ecx, eax
004C280B  mov      dword ptr [rip + 0x1940017], ecx  ; -> 01E02828 [f32 1]
004C2811  mulss    xmm2, dword ptr [rip + 0x1ba2427]  ; -> 02064C40
004C2819  mulss    xmm1, dword ptr [rip + 0x1ba241f]  ; -> 02064C40
004C2821  movss    dword ptr [rip + 0x1ba22f7], xmm2  ; -> 02064B20
004C2829  movss    dword ptr [rip + 0x1ba22f3], xmm1  ; -> 02064B24
004C2831  test     edx, edx
004C2833  je       0x4c2856  ; -> 004C2856
004C2835  mov      eax, ecx
004C2837  shr      ecx, 0x12
004C283A  xor      ecx, eax
004C283C  and      eax, 0x3fffff
004C2841  or       eax, 0x1fc00000
004C2846  shr      ecx, 4
004C2849  add      eax, eax
004C284B  and      ecx, 1
004C284E  or       ecx, eax
004C2850  mov      dword ptr [rip + 0x193ffd2], ecx  ; -> 01E02828 [f32 1]
004C2856  mulss    xmm3, dword ptr [rip + 0x1ba23e6]  ; -> 02064C44
004C285E  mulss    xmm4, dword ptr [rip + 0x1ba23de]  ; -> 02064C44
004C2866  addss    xmm3, xmm2
004C286A  addss    xmm4, xmm1
004C286E  movss    dword ptr [rip + 0x1ba23ca], xmm3  ; -> 02064C40
004C2876  movss    dword ptr [rip + 0x1ba23c6], xmm4  ; -> 02064C44
004C287E  test     edx, edx
004C2880  jne      0x4c2888  ; -> 004C2888
004C2882  movaps   xmm0, xmm15
004C2886  jmp      0x4c28b3  ; -> 004C28B3
004C2888  mov      eax, ecx
004C288A  shr      eax, 0x12
004C288D  xor      eax, ecx
004C288F  and      ecx, 0x3fffff
004C2895  or       ecx, 0x1fc00000
004C289B  shr      eax, 4
004C289E  add      ecx, ecx
004C28A0  and      eax, 1
004C28A3  or       eax, ecx
004C28A5  mov      dword ptr [rip + 0x193ff7d], eax  ; -> 01E02828 [f32 1]
004C28AB  movss    xmm0, dword ptr [rip + 0x193ff75]  ; -> 01E02828 [f32 1]
004C28B3  subss    xmm0, xmm13
004C28B8  mov      dword ptr [rip + 0x1ba2242], 0x40c90fdb  ; -> 02064B04
004C28C2  mulss    xmm0, xmm12
004C28C7  movss    dword ptr [rip + 0x1ba23e1], xmm0  ; -> 02064CB0
004C28CF  call     0x5376d0  ; -> 005376D0 fn
004C28D4  movss    xmm5, dword ptr [rip + 0x1ba23e4]  ; -> 02064CC0
004C28DC  movss    xmm4, dword ptr [rip + 0x193ff54]  ; -> 01E02838 [u32 0x00000000]
004C28E4  mov      edx, dword ptr [rip + 0x1ba2212]  ; -> 02064AFC
004C28EA  addss    xmm5, xmm4
004C28EE  movss    dword ptr [rip + 0x1ba2272], xmm5  ; -> 02064B68
004C28F6  test     edx, edx
004C28F8  je       0x4c2923  ; -> 004C2923
004C28FA  mov      eax, dword ptr [rip + 0x193ff28]  ; -> 01E02828 [f32 1]
004C2900  mov      ecx, eax
004C2902  shr      ecx, 0x12
004C2905  xor      ecx, eax
004C2907  and      eax, 0x3fffff
004C290C  or       eax, 0x1fc00000
004C2911  shr      ecx, 4
004C2914  add      eax, eax
004C2916  and      ecx, 1
004C2919  or       ecx, eax
004C291B  mov      dword ptr [rip + 0x193ff07], ecx  ; -> 01E02828 [f32 1]
004C2921  jmp      0x4c2929  ; -> 004C2929
004C2923  mov      ecx, dword ptr [rip + 0x193feff]  ; -> 01E02828 [f32 1]
004C2929  movss    xmm2, dword ptr [rip + 0x193ff03]  ; -> 01E02834 [u32 0x00000000]
004C2931  movaps   xmm3, xmm2
004C2934  addss    xmm3, dword ptr [rip + 0x1ba2388]  ; -> 02064CC4
004C293C  movss    dword ptr [rip + 0x1ba2220], xmm3  ; -> 02064B64
004C2944  test     edx, edx
004C2946  je       0x4c2969  ; -> 004C2969
004C2948  mov      eax, ecx
004C294A  shr      ecx, 0x12
004C294D  xor      ecx, eax
004C294F  and      eax, 0x3fffff
004C2954  or       eax, 0x1fc00000
004C2959  shr      ecx, 4
004C295C  add      eax, eax
004C295E  and      ecx, 1
004C2961  or       ecx, eax
004C2963  mov      dword ptr [rip + 0x193febf], ecx  ; -> 01E02828 [f32 1]
004C2969  movaps   xmm0, xmm2
004C296C  movaps   xmm1, xmm4
004C296F  addss    xmm0, xmm2
004C2973  addss    xmm1, xmm4
004C2977  movss    dword ptr [rip + 0x1ba21d5], xmm0  ; -> 02064B54
004C297F  movss    dword ptr [rip + 0x1ba21d1], xmm1  ; -> 02064B58
004C2987  test     edx, edx
004C2989  je       0x4c29ac  ; -> 004C29AC
004C298B  mov      eax, ecx
004C298D  shr      ecx, 0x12
004C2990  xor      ecx, eax
004C2992  and      eax, 0x3fffff
004C2997  or       eax, 0x1fc00000
004C299C  shr      ecx, 4
004C299F  add      eax, eax
004C29A1  and      ecx, 1
004C29A4  or       ecx, eax
004C29A6  mov      dword ptr [rip + 0x193fe7c], ecx  ; -> 01E02828 [f32 1]
004C29AC  movss    xmm1, dword ptr [rip + 0x193fe7c]  ; -> 01E02830 [u32 0x00000000]
004C29B4  movaps   xmm0, xmm1
004C29B7  addss    xmm0, dword ptr [rip + 0x193fe7d]  ; -> 01E0283C [f32 1]
004C29BF  movss    dword ptr [rip + 0x1ba2189], xmm0  ; -> 02064B50
004C29C7  test     edx, edx
004C29C9  je       0x4c29ec  ; -> 004C29EC
004C29CB  mov      eax, ecx
004C29CD  shr      ecx, 0x12
004C29D0  xor      ecx, eax
004C29D2  and      eax, 0x3fffff
004C29D7  or       eax, 0x1fc00000
004C29DC  shr      ecx, 4
004C29DF  add      eax, eax
004C29E1  and      ecx, 1
004C29E4  or       ecx, eax
004C29E6  mov      dword ptr [rip + 0x193fe3c], ecx  ; -> 01E02828 [f32 1]
004C29EC  addss    xmm1, xmm1
004C29F0  movss    dword ptr [rip + 0x1ba2178], xmm1  ; -> 02064B70
004C29F8  test     edx, edx
004C29FA  jne      0x4c2a02  ; -> 004C2A02
004C29FC  movaps   xmm0, xmm15
004C2A00  jmp      0x4c2a2d  ; -> 004C2A2D
004C2A02  mov      eax, ecx
004C2A04  shr      eax, 0x12
004C2A07  xor      eax, ecx
004C2A09  and      ecx, 0x3fffff
004C2A0F  or       ecx, 0x1fc00000
004C2A15  shr      eax, 4
004C2A18  add      ecx, ecx
004C2A1A  and      eax, 1
004C2A1D  or       eax, ecx
004C2A1F  mov      dword ptr [rip + 0x193fe03], eax  ; -> 01E02828 [f32 1]
004C2A25  movss    xmm0, dword ptr [rip + 0x193fdfb]  ; -> 01E02828 [f32 1]
004C2A2D  addss    xmm2, xmm5
004C2A31  movss    dword ptr [rip + 0x1ba2127], xmm1  ; -> 02064B60
004C2A39  subss    xmm0, xmm13
004C2A3E  mov      dword ptr [rip + 0x1ba20bc], 0x40c90fdb  ; -> 02064B04
004C2A48  addss    xmm3, xmm4
004C2A4C  mulss    xmm2, xmm8
004C2A51  mulss    xmm0, xmm12
004C2A56  movss    dword ptr [rip + 0x1ba2116], xmm2  ; -> 02064B74
004C2A5E  movss    dword ptr [rip + 0x1ba2112], xmm3  ; -> 02064B78
004C2A66  movss    dword ptr [rip + 0x1ba2242], xmm0  ; -> 02064CB0
004C2A6E  call     0x5376d0  ; -> 005376D0 fn
004C2A73  movss    xmm7, dword ptr [rip + 0x193fdb5]  ; -> 01E02830 [u32 0x00000000]
004C2A7B  movss    xmm0, dword ptr [rip + 0x193fdb5]  ; -> 01E02838 [u32 0x00000000]
004C2A83  movaps   xmm13, xmm7
004C2A87  movss    xmm3, dword ptr [rip + 0x1ba20c9]  ; -> 02064B58
004C2A8F  movaps   xmm12, xmm0
004C2A93  movss    xmm9, dword ptr [rip + 0x193fd98]  ; -> 01E02834 [u32 0x00000000]
004C2A9C  addss    xmm12, xmm0
004C2AA1  movss    xmm2, dword ptr [rip + 0x1ba20ab]  ; -> 02064B54
004C2AA9  movaps   xmm10, xmm9
004C2AAD  addss    xmm13, dword ptr [rip + 0x1ba220a]  ; -> 02064CC0
004C2AB6  movss    xmm14, dword ptr [rip + 0x1ba2205]  ; -> 02064CC4
004C2ABF  addss    xmm10, xmm9
004C2AC4  addss    xmm9, dword ptr [rip + 0x193fd6f]  ; -> 01E0283C [f32 1]
004C2ACD  mov      edx, dword ptr [rip + 0x1ba2029]  ; -> 02064AFC
004C2AD3  addss    xmm14, xmm0
004C2AD8  movss    dword ptr [rip + 0x1ba20b7], xmm12  ; -> 02064B98
004C2AE1  movaps   xmm11, xmm7
004C2AE5  addss    xmm11, xmm7
004C2AEA  movaps   xmm8, xmm13
004C2AEE  mulss    xmm13, dword ptr [rip + 0x18291a5]  ; -> 01CEBC9C [f32 -1]
004C2AF7  addss    xmm8, xmm0
004C2AFC  movss    xmm0, dword ptr [rip + 0x1ba204c]  ; -> 02064B50
004C2B04  addss    xmm7, xmm14
004C2B09  movss    dword ptr [rip + 0x1ba2096], xmm14  ; -> 02064BA8
004C2B12  movaps   xmm5, xmm10
004C2B16  mulss    xmm5, xmm0
004C2B1A  movaps   xmm1, xmm12
004C2B1E  mulss    xmm1, xmm2
004C2B22  movaps   xmm6, xmm8
004C2B26  mulss    xmm6, xmm0
004C2B2A  movaps   xmm4, xmm7
004C2B2D  mulss    xmm4, xmm0
004C2B31  movaps   xmm0, xmm11
004C2B35  mulss    xmm0, xmm2
004C2B39  addss    xmm6, xmm1
004C2B3D  movss    dword ptr [rip + 0x1ba203e], xmm10  ; -> 02064B84
004C2B46  movaps   xmm1, xmm3
004C2B49  mulss    xmm1, xmm10
004C2B4E  movss    dword ptr [rip + 0x1ba2039], xmm11  ; -> 02064B90
004C2B57  addss    xmm4, xmm0
004C2B5B  movss    dword ptr [rip + 0x1ba2030], xmm9  ; -> 02064B94
004C2B64  movaps   xmm0, xmm9
004C2B68  mulss    xmm0, xmm2
004C2B6C  movss    dword ptr [rip + 0x1ba200c], xmm7  ; -> 02064B80
004C2B74  movss    dword ptr [rip + 0x1ba200b], xmm8  ; -> 02064B88
004C2B7D  movss    dword ptr [rip + 0x1ba201e], xmm10  ; -> 02064BA4
004C2B86  addss    xmm5, xmm0
004C2B8A  movss    dword ptr [rip + 0x1ba200d], xmm13  ; -> 02064BA0
004C2B93  movaps   xmm0, xmm3
004C2B96  mulss    xmm3, xmm14
004C2B9B  mulss    xmm0, xmm13
004C2BA0  addss    xmm1, xmm5
004C2BA4  movaps   xmm5, xmm8
004C2BA8  addss    xmm3, xmm6
004C2BAC  addss    xmm0, xmm4
004C2BB0  movaps   xmm4, xmm7
004C2BB3  movss    dword ptr [rip + 0x1ba1f99], xmm1  ; -> 02064B54
004C2BBB  movss    dword ptr [rip + 0x1ba1f95], xmm3  ; -> 02064B58
004C2BC3  movaps   xmm3, xmm10
004C2BC7  movss    dword ptr [rip + 0x1ba1f81], xmm0  ; -> 02064B50
004C2BCF  movss    xmm0, dword ptr [rip + 0x1ba1f89]  ; -> 02064B60
004C2BD7  mulss    xmm4, xmm0
004C2BDB  mulss    xmm3, xmm0
004C2BDF  mulss    xmm5, xmm0
004C2BE3  test     edx, edx
004C2BE5  je       0x4c2c10  ; -> 004C2C10
004C2BE7  mov      eax, dword ptr [rip + 0x193fc3b]  ; -> 01E02828 [f32 1]
004C2BED  mov      ecx, eax
004C2BEF  shr      ecx, 0x12
004C2BF2  xor      ecx, eax
004C2BF4  and      eax, 0x3fffff
004C2BF9  or       eax, 0x1fc00000
004C2BFE  shr      ecx, 4
004C2C01  add      eax, eax
004C2C03  and      ecx, 1
004C2C06  or       ecx, eax
004C2C08  mov      dword ptr [rip + 0x193fc1a], ecx  ; -> 01E02828 [f32 1]
004C2C0E  jmp      0x4c2c16  ; -> 004C2C16
004C2C10  mov      ecx, dword ptr [rip + 0x193fc12]  ; -> 01E02828 [f32 1]
004C2C16  movss    xmm2, dword ptr [rip + 0x1ba1f46]  ; -> 02064B64
004C2C1E  movaps   xmm0, xmm11
004C2C22  mulss    xmm0, xmm2
004C2C26  movaps   xmm1, xmm12
004C2C2A  mulss    xmm1, xmm2
004C2C2E  addss    xmm4, xmm0
004C2C32  movaps   xmm0, xmm9
004C2C36  mulss    xmm0, xmm2
004C2C3A  addss    xmm5, xmm1
004C2C3E  addss    xmm3, xmm0
004C2C42  test     edx, edx
004C2C44  je       0x4c2c67  ; -> 004C2C67
004C2C46  mov      eax, ecx
004C2C48  shr      ecx, 0x12
004C2C4B  xor      ecx, eax
004C2C4D  and      eax, 0x3fffff
004C2C52  or       eax, 0x1fc00000
004C2C57  shr      ecx, 4
004C2C5A  add      eax, eax
004C2C5C  and      ecx, 1
004C2C5F  or       ecx, eax
004C2C61  mov      dword ptr [rip + 0x193fbc1], ecx  ; -> 01E02828 [f32 1]
004C2C67  movss    xmm2, dword ptr [rip + 0x1ba1ef9]  ; -> 02064B68
004C2C6F  movaps   xmm0, xmm13
004C2C73  mulss    xmm0, xmm2
004C2C77  movaps   xmm1, xmm14
004C2C7B  mulss    xmm1, xmm2
004C2C7F  addss    xmm0, xmm4
004C2C83  addss    xmm1, xmm5
004C2C87  movss    dword ptr [rip + 0x1ba1ed1], xmm0  ; -> 02064B60
004C2C8F  movaps   xmm0, xmm10
004C2C93  mulss    xmm0, xmm2
004C2C97  movss    dword ptr [rip + 0x1ba1ec9], xmm1  ; -> 02064B68
004C2C9F  addss    xmm0, xmm3
004C2CA3  movss    dword ptr [rip + 0x1ba1eb9], xmm0  ; -> 02064B64
004C2CAB  test     edx, edx
004C2CAD  je       0x4c2cd0  ; -> 004C2CD0
004C2CAF  mov      eax, ecx
004C2CB1  shr      ecx, 0x12
004C2CB4  xor      ecx, eax
004C2CB6  and      eax, 0x3fffff
004C2CBB  or       eax, 0x1fc00000
004C2CC0  shr      ecx, 4
004C2CC3  add      eax, eax
004C2CC5  and      ecx, 1
004C2CC8  or       ecx, eax
004C2CCA  mov      dword ptr [rip + 0x193fb58], ecx  ; -> 01E02828 [f32 1]
004C2CD0  movss    xmm0, dword ptr [rip + 0x1ba1e98]  ; -> 02064B70
004C2CD8  movaps   xmm3, xmm10
004C2CDC  mulss    xmm7, xmm0
004C2CE0  mulss    xmm3, xmm0
004C2CE4  mulss    xmm8, xmm0
004C2CE9  test     edx, edx
004C2CEB  je       0x4c2d0e  ; -> 004C2D0E
004C2CED  mov      eax, ecx
004C2CEF  shr      ecx, 0x12
004C2CF2  xor      ecx, eax
004C2CF4  and      eax, 0x3fffff
004C2CF9  or       eax, 0x1fc00000
004C2CFE  shr      ecx, 4
004C2D01  add      eax, eax
004C2D03  and      ecx, 1
004C2D06  or       ecx, eax
004C2D08  mov      dword ptr [rip + 0x193fb1a], ecx  ; -> 01E02828 [f32 1]
004C2D0E  movss    xmm0, dword ptr [rip + 0x1ba1e5e]  ; -> 02064B74
004C2D16  mulss    xmm11, xmm0
004C2D1B  mulss    xmm9, xmm0
004C2D20  mulss    xmm12, xmm0
004C2D25  addss    xmm7, xmm11
004C2D2A  addss    xmm3, xmm9
004C2D2F  addss    xmm8, xmm12
004C2D34  movss    dword ptr [rip + 0x1ba1de4], xmm7  ; -> 02064B20
004C2D3C  movss    dword ptr [rip + 0x1ba1de0], xmm3  ; -> 02064B24
004C2D44  movss    dword ptr [rip + 0x1ba1ddb], xmm8  ; -> 02064B28
004C2D4D  test     edx, edx
004C2D4F  je       0x4c2d7d  ; -> 004C2D7D
004C2D51  mov      eax, ecx
004C2D53  shr      eax, 0x12
004C2D56  xor      eax, ecx
004C2D58  and      ecx, 0x3fffff
004C2D5E  or       ecx, 0x1fc00000
004C2D64  shr      eax, 4
004C2D67  add      ecx, ecx
004C2D69  and      eax, 1
004C2D6C  or       eax, ecx
004C2D6E  mov      dword ptr [rip + 0x193fab4], eax  ; -> 01E02828 [f32 1]
004C2D74  movss    xmm15, dword ptr [rip + 0x193faab]  ; -> 01E02828 [f32 1]
004C2D7D  movss    xmm2, dword ptr [rip + 0x1ba1df3]  ; -> 02064B78
004C2D85  subss    xmm15, dword ptr [rip + 0x43edae]  ; -> 00901B3C [f32 1.5]
004C2D8E  movaps   xmm0, xmm2
004C2D91  mov      dword ptr [rip + 0x1ba1d69], 0x40c90fdb  ; -> 02064B04
004C2D9B  movaps   xmm1, xmm2
004C2D9E  mulss    xmm0, xmm13
004C2DA3  mulss    xmm1, xmm10
004C2DA8  mulss    xmm15, dword ptr [rip + 0x1828ec7]  ; -> 01CEBC78 [f32 6.283185]
004C2DB1  addss    xmm0, xmm7
004C2DB5  mulss    xmm2, xmm14
004C2DBA  addss    xmm1, xmm3
004C2DBE  movss    dword ptr [rip + 0x1ba1ee9], xmm15  ; -> 02064CB0
004C2DC7  movss    dword ptr [rip + 0x1ba1da1], xmm0  ; -> 02064B70
004C2DCF  addss    xmm2, xmm8
004C2DD4  movss    dword ptr [rip + 0x1ba1d98], xmm1  ; -> 02064B74
004C2DDC  movss    dword ptr [rip + 0x1ba1d94], xmm2  ; -> 02064B78
004C2DE4  call     0x5376d0  ; -> 005376D0 fn
004C2DE9  movss    xmm0, dword ptr [rip + 0x193fa43]  ; -> 01E02834 [u32 0x00000000]
004C2DF1  movss    xmm1, dword ptr [rip + 0x193fa37]  ; -> 01E02830 [u32 0x00000000]
004C2DF9  movaps   xmm6, xmm0
004C2DFC  movss    xmm2, dword ptr [rip + 0x193fa34]  ; -> 01E02838 [u32 0x00000000]
004C2E04  movaps   xmm14, xmm0
004C2E08  addss    xmm6, dword ptr [rip + 0x1ba1eb4]  ; -> 02064CC4
004C2E10  movss    xmm15, dword ptr [rip + 0x193fa23]  ; -> 01E0283C [f32 1]
004C2E19  addss    xmm14, xmm0
004C2E1E  movss    dword ptr [rsp + 0x20], xmm0
004C2E24  addss    xmm15, xmm2
004C2E29  movaps   xmm7, xmm1
004C2E2C  movss    dword ptr [rsp + 0x24], xmm2
004C2E32  addss    xmm7, dword ptr [rip + 0x1ba1e86]  ; -> 02064CC0
004C2E3A  movaps   xmm8, xmm2
004C2E3E  movss    dword ptr [rsp + 0x110], xmm6
004C2E47  addss    xmm8, xmm2
004C2E4C  movss    dword ptr [rip + 0x1ba1d40], xmm6  ; -> 02064B94
004C2E54  movss    xmm2, dword ptr [rip + 0x1ba1cf8]  ; -> 02064B54
004C2E5C  movaps   xmm13, xmm1
004C2E60  addss    xmm13, xmm1
004C2E65  movss    dword ptr [rip + 0x1ba1d36], xmm14  ; -> 02064BA4
004C2E6E  movaps   xmm10, xmm7
004C2E72  movss    dword ptr [rip + 0x1ba1d2d], xmm15  ; -> 02064BA8
004C2E7B  mulss    xmm7, dword ptr [rip + 0x1828e19]  ; -> 01CEBC9C [f32 -1]
004C2E83  addss    xmm10, xmm0
004C2E88  mov      dword ptr [rip + 0x1ba1c72], 0xbf800000  ; -> 02064B04
004C2E92  movss    xmm0, dword ptr [rip + 0x1ba1cb6]  ; -> 02064B50
004C2E9A  movaps   xmm9, xmm6
004C2E9E  addss    xmm9, xmm1
004C2EA3  movss    dword ptr [rip + 0x1ba1cdc], xmm8  ; -> 02064B88
004C2EAC  movaps   xmm5, xmm8
004C2EB0  movss    dword ptr [rip + 0x1ba1cdf], xmm8  ; -> 02064B98
004C2EB9  mulss    xmm5, xmm0
004C2EBD  movaps   xmm4, xmm10
004C2EC1  mulss    xmm4, xmm0
004C2EC5  movaps   xmm1, xmm8
004C2EC9  movaps   xmm3, xmm9
004C2ECD  mulss    xmm1, xmm2
004C2ED1  mulss    xmm3, xmm0
004C2ED5  movaps   xmm0, xmm7
004C2ED8  mulss    xmm0, xmm2
004C2EDC  addss    xmm5, xmm1
004C2EE0  movss    dword ptr [rip + 0x1ba1cb7], xmm13  ; -> 02064BA0
004C2EE9  movss    dword ptr [rip + 0x1ba1c92], xmm10  ; -> 02064B84
004C2EF2  addss    xmm3, xmm0
004C2EF6  movss    dword ptr [rip + 0x1ba1c81], xmm9  ; -> 02064B80
004C2EFF  movaps   xmm0, xmm6
004C2F02  movss    dword ptr [rsp + 0x100], xmm7
004C2F0B  mulss    xmm0, xmm2
004C2F0F  movss    dword ptr [rip + 0x1ba1c79], xmm7  ; -> 02064B90
004C2F17  addss    xmm4, xmm0
004C2F1B  movss    xmm0, dword ptr [rip + 0x1ba1c35]  ; -> 02064B58
004C2F23  movaps   xmm12, xmm0
004C2F27  movaps   xmm11, xmm0
004C2F2B  mulss    xmm12, xmm13
004C2F30  mulss    xmm11, xmm14
004C2F35  mulss    xmm0, xmm15
004C2F3A  addss    xmm12, xmm3
004C2F3F  addss    xmm11, xmm4
004C2F44  addss    xmm0, xmm5
004C2F48  movss    dword ptr [rip + 0x1ba1bff], xmm12  ; -> 02064B50
004C2F51  movss    dword ptr [rip + 0x1ba1bfa], xmm11  ; -> 02064B54
004C2F5A  movss    dword ptr [rsp + 0x118], xmm0
004C2F63  movss    dword ptr [rip + 0x1ba1bed], xmm0  ; -> 02064B58
004C2F6B  movss    xmm0, dword ptr [rip + 0x1ba1bed]  ; -> 02064B60
004C2F73  movaps   xmm1, xmm8
004C2F77  movss    xmm2, dword ptr [rip + 0x1ba1be5]  ; -> 02064B64
004C2F7F  movaps   xmm5, xmm8
004C2F83  mulss    xmm1, xmm2
004C2F87  movaps   xmm3, xmm9
004C2F8B  mulss    xmm3, xmm0
004C2F8F  movaps   xmm4, xmm10
004C2F93  mulss    xmm4, xmm0
004C2F97  mulss    xmm5, xmm0
004C2F9B  movaps   xmm0, xmm7
004C2F9E  mulss    xmm0, xmm2
004C2FA2  movaps   xmm7, xmm13
004C2FA6  addss    xmm5, xmm1
004C2FAA  movaps   xmm1, xmm8
004C2FAE  addss    xmm3, xmm0
004C2FB2  movaps   xmm0, xmm6
004C2FB5  mulss    xmm0, xmm2
004C2FB9  movaps   xmm6, xmm14
004C2FBD  movss    xmm2, dword ptr [rsp + 0x100]
004C2FC6  addss    xmm4, xmm0
004C2FCA  movss    xmm0, dword ptr [rip + 0x1ba1b96]  ; -> 02064B68
004C2FD2  mulss    xmm7, xmm0
004C2FD6  mulss    xmm6, xmm0
004C2FDA  addss    xmm7, xmm3
004C2FDE  movaps   xmm3, xmm15
004C2FE2  mulss    xmm3, xmm0
004C2FE6  movss    xmm0, dword ptr [rip + 0x1ba1b82]  ; -> 02064B70
004C2FEE  addss    xmm6, xmm4
004C2FF2  mulss    xmm1, xmm0
004C2FF6  mulss    xmm9, xmm0
004C2FFB  addss    xmm3, xmm5
004C2FFF  mulss    xmm10, xmm0
004C3004  movss    xmm0, dword ptr [rip + 0x1ba1b68]  ; -> 02064B74
004C300C  mulss    xmm2, xmm0
004C3010  mulss    xmm8, xmm0
004C3015  addss    xmm9, xmm2
004C301A  movss    dword ptr [rip + 0x1ba1b3e], xmm7  ; -> 02064B60
004C3022  movss    xmm2, dword ptr [rsp + 0x110]
004C302B  mulss    xmm2, xmm0
004C302F  addss    xmm1, xmm8
004C3034  movss    xmm8, dword ptr [rip + 0x1ba1b3b]  ; -> 02064B78
004C303D  movss    xmm0, dword ptr [rip + 0x1ba1bfb]  ; -> 02064C40
004C3045  movaps   xmm4, xmm8
004C3049  addss    xmm10, xmm2
004C304E  mulss    xmm4, xmm14
004C3053  movaps   xmm2, xmm8
004C3057  mulss    xmm12, xmm0
004C305C  mulss    xmm8, xmm15
004C3061  addss    xmm4, xmm10
004C3066  mulss    xmm2, xmm13
004C306B  addss    xmm8, xmm1
004C3070  mulss    xmm11, xmm0
004C3075  movss    xmm1, dword ptr [rsp + 0x118]
004C307E  addss    xmm2, xmm9
004C3083  mulss    xmm1, xmm0
004C3087  movss    xmm0, dword ptr [rip + 0x1ba1bb5]  ; -> 02064C44
004C308F  mulss    xmm7, xmm0
004C3093  movss    dword ptr [rip + 0x1ba1ad9], xmm4  ; -> 02064B74
004C309B  movss    dword ptr [rip + 0x1ba1ad4], xmm8  ; -> 02064B78
004C30A4  movss    dword ptr [rip + 0x1ba1ac4], xmm2  ; -> 02064B70
004C30AC  addss    xmm12, xmm7
004C30B1  movss    xmm7, dword ptr [rip + 0x193f777]  ; -> 01E02830 [u32 0x00000000]
004C30B9  movss    dword ptr [rip + 0x1ba1aa3], xmm6  ; -> 02064B64
004C30C1  mulss    xmm6, xmm0
004C30C5  movss    dword ptr [rip + 0x1ba1a9b], xmm3  ; -> 02064B68
004C30CD  mulss    xmm3, xmm0
004C30D1  movss    xmm0, dword ptr [rip + 0x1ba1b6f]  ; -> 02064C48
004C30D9  addss    xmm11, xmm6
004C30DE  mulss    xmm4, xmm0
004C30E2  mulss    xmm8, xmm0
004C30E7  addss    xmm1, xmm3
004C30EB  mulss    xmm2, xmm0
004C30EF  addss    xmm4, xmm11
004C30F4  addss    xmm8, xmm1
004C30F9  addss    xmm2, xmm12
004C30FE  addss    xmm4, dword ptr [rip + 0x1ba1ade]  ; -> 02064BE4
004C3106  addss    xmm8, dword ptr [rip + 0x1ba1ad9]  ; -> 02064BE8
004C310F  addss    xmm2, dword ptr [rip + 0x1ba1ac9]  ; -> 02064BE0
004C3117  movss    dword ptr [rip + 0x1ba1b95], xmm4  ; -> 02064CB4
004C311F  movss    dword ptr [rip + 0x1ba1b90], xmm8  ; -> 02064CB8
004C3128  movups   xmm0, xmmword ptr [rip + 0x1ba1bb1]  ; -> 02064CE0
004C312F  movss    xmm1, dword ptr [rip + 0x1ba1bc1]  ; -> 02064CF8
004C3137  movaps   xmm5, xmm2
004C313A  movss    xmm9, dword ptr [rip + 0x193f6f9]  ; -> 01E0283C [f32 1]
004C3143  movaps   xmm6, xmm7
004C3146  mulss    xmm1, xmm4
004C314A  addss    xmm6, xmm9
004C314F  shufps   xmm5, xmm5, 0
004C3153  mulps    xmm5, xmm0
004C3156  movss    xmm0, dword ptr [rip + 0x1ba1b92]  ; -> 02064CF0
004C315E  mulss    xmm0, xmm4
004C3162  movups   xmmword ptr [rip + 0x1ba19b7], xmm5  ; -> 02064B20
004C3169  movss    xmm2, dword ptr [rip + 0x1ba19b3]  ; -> 02064B24
004C3171  addss    xmm5, xmm0
004C3175  movss    xmm0, dword ptr [rip + 0x1ba1b77]  ; -> 02064CF4
004C317D  movss    xmm3, dword ptr [rip + 0x1ba19a3]  ; -> 02064B28
004C3185  mulss    xmm0, xmm4
004C3189  addss    xmm3, xmm1
004C318D  movss    xmm1, dword ptr [rip + 0x1ba1b6f]  ; -> 02064D04
004C3195  mulss    xmm1, xmm8
004C319A  addss    xmm2, xmm0
004C319E  movss    dword ptr [rip + 0x1ba1b16], xmm6  ; -> 02064CBC
004C31A6  movss    xmm0, dword ptr [rip + 0x1ba1b4e]  ; -> 02064CFC
004C31AE  mulss    xmm0, xmm4
004C31B2  movss    xmm4, dword ptr [rip + 0x1ba1972]  ; -> 02064B2C
004C31BA  addss    xmm2, xmm1
004C31BE  movss    xmm1, dword ptr [rip + 0x1ba1b46]  ; -> 02064D0C
004C31C6  addss    xmm4, xmm0
004C31CA  mulss    xmm1, xmm8
004C31CF  movss    xmm0, dword ptr [rip + 0x1ba1b29]  ; -> 02064D00
004C31D7  mulss    xmm0, xmm8
004C31DC  addss    xmm4, xmm1
004C31E0  movss    dword ptr [rip + 0x1ba193c], xmm2  ; -> 02064B24
004C31E8  movss    xmm1, dword ptr [rip + 0x1ba1b24]  ; -> 02064D14
004C31F0  addss    xmm5, xmm0
004C31F4  mulss    xmm1, xmm6
004C31F8  movss    xmm0, dword ptr [rip + 0x1ba1b08]  ; -> 02064D08
004C3200  mulss    xmm0, xmm8
004C3205  addss    xmm1, xmm2
004C3209  movss    dword ptr [rip + 0x1ba191b], xmm4  ; -> 02064B2C
004C3211  movss    dword ptr [rip + 0x1ba1907], xmm5  ; -> 02064B20
004C3219  addss    xmm3, xmm0
004C321D  movss    xmm0, dword ptr [rip + 0x1ba1aeb]  ; -> 02064D10
004C3225  mulss    xmm0, xmm6
004C3229  movss    dword ptr [rip + 0x1ba1a93], xmm1  ; -> 02064CC4
004C3231  movss    xmm1, dword ptr [rip + 0x1ba1ae3]  ; -> 02064D1C
004C3239  addss    xmm0, xmm5
004C323D  mulss    xmm1, xmm6
004C3241  movss    dword ptr [rip + 0x1ba18df], xmm3  ; -> 02064B28
004C3249  addss    xmm1, xmm4
004C324D  movss    dword ptr [rip + 0x1ba1a6b], xmm0  ; -> 02064CC0
004C3255  movss    xmm0, dword ptr [rip + 0x1ba1abb]  ; -> 02064D18
004C325D  mulss    xmm0, xmm6
004C3261  ucomiss  xmm1, dword ptr [rip + 0x43e71c]  ; -> 00901984 [u32 0x00000000]
004C3268  addss    xmm0, xmm3
004C326C  movss    dword ptr [rip + 0x1ba1a58], xmm1  ; -> 02064CCC
004C3274  movss    dword ptr [rip + 0x1ba1a4c], xmm0  ; -> 02064CC8
004C327C  jp       0x4c328f  ; -> 004C328F
004C327E  jne      0x4c328f  ; -> 004C328F
004C3280  movss    xmm11, dword ptr [rip + 0x43d0d7]  ; -> 00900360 [u32 0x7F7FFFFF]
004C3289  movaps   xmm0, xmm11
004C328D  jmp      0x4c32a0  ; -> 004C32A0
004C328F  movss    xmm11, dword ptr [rip + 0x43d0c8]  ; -> 00900360 [u32 0x7F7FFFFF]
004C3298  movaps   xmm0, xmm9
004C329C  divss    xmm0, xmm1
004C32A0  cmp      dword ptr [rip + 0x1ba1855], 0  ; -> 02064AFC
004C32A7  movss    dword ptr [rip + 0x1ba1851], xmm0  ; -> 02064B00
004C32AF  je       0x4c3361  ; -> 004C3361
004C32B5  mov      eax, dword ptr [rip + 0x193f56d]  ; -> 01E02828 [f32 1]
004C32BB  mov      ecx, eax
004C32BD  movss    xmm15, dword ptr [rip + 0x18288e2]  ; -> 01CEBBA8 [f32 1]
004C32C6  shr      ecx, 0x12
004C32C9  xor      ecx, eax
004C32CB  and      eax, 0x3fffff
004C32D0  or       eax, 0x1fc00000
004C32D5  shr      ecx, 4
004C32D8  add      eax, eax
004C32DA  and      ecx, 1
004C32DD  or       ecx, eax
004C32DF  mov      eax, ecx
004C32E1  shr      eax, 0x12
004C32E4  xor      eax, ecx
004C32E6  and      ecx, 0x3fffff
004C32EC  or       ecx, 0x1fc00000
004C32F2  shr      eax, 4
004C32F5  add      ecx, ecx
004C32F7  and      eax, 1
004C32FA  or       eax, ecx
004C32FC  mov      ecx, eax
004C32FE  shr      ecx, 0x12
004C3301  xor      ecx, eax
004C3303  and      eax, 0x3fffff
004C3308  or       eax, 0x1fc00000
004C330D  shr      ecx, 4
004C3310  add      eax, eax
004C3312  and      ecx, 1
004C3315  or       ecx, eax
004C3317  mov      edx, ecx
004C3319  shr      edx, 0x12
004C331C  xor      edx, ecx
004C331E  and      ecx, 0x3fffff
004C3324  shr      edx, 4
004C3327  or       ecx, 0x1fc00000
004C332D  and      edx, 1
004C3330  add      ecx, ecx
004C3332  or       edx, ecx
004C3334  mov      eax, edx
004C3336  shr      eax, 0x12
004C3339  xor      eax, edx
004C333B  and      edx, 0x3fffff
004C3341  or       edx, 0x1fc00000
004C3347  shr      eax, 4
004C334A  add      edx, edx
004C334C  and      eax, 1
004C334F  or       eax, edx
004C3351  mov      dword ptr [rip + 0x193f4d1], eax  ; -> 01E02828 [f32 1]
004C3357  movss    xmm2, dword ptr [rip + 0x193f4c9]  ; -> 01E02828 [f32 1]
004C335F  jmp      0x4c336e  ; -> 004C336E
004C3361  movss    xmm15, dword ptr [rip + 0x182883e]  ; -> 01CEBBA8 [f32 1]
004C336A  movaps   xmm2, xmm15
004C336E  movups   xmm1, xmmword ptr [rip + 0x1ba194b]  ; -> 02064CC0
004C3375  movss    xmm6, dword ptr [rip + 0x1ba17b3]  ; -> 02064B30
004C337D  shufps   xmm0, xmm0, 0
004C3381  mulps    xmm1, xmm0
004C3384  movss    dword ptr [rip + 0x1ba1924], xmm2  ; -> 02064CB0
004C338C  ucomiss  xmm6, xmm1
004C338F  jp       0x4c339b  ; -> 004C339B
004C3391  jne      0x4c339b  ; -> 004C339B
004C3393  mov      r9d, 1
004C3399  jmp      0x4c339e  ; -> 004C339E
004C339B  xor      r9d, r9d
004C339E  movss    xmm5, dword ptr [rip + 0x1ba178e]  ; -> 02064B34
004C33A6  movaps   xmm3, xmm1
004C33A9  shufps   xmm3, xmm1, 0x55
004C33AD  ucomiss  xmm5, xmm3
004C33B0  jp       0x4c33bc  ; -> 004C33BC
004C33B2  jne      0x4c33bc  ; -> 004C33BC
004C33B4  mov      r8d, 1
004C33BA  jmp      0x4c33bf  ; -> 004C33BF
004C33BC  xor      r8d, r8d
004C33BF  movss    xmm4, dword ptr [rip + 0x1ba1771]  ; -> 02064B38
004C33C7  movaps   xmm0, xmm1
004C33CA  shufps   xmm0, xmm1, 0xaa
004C33CE  ucomiss  xmm4, xmm0
004C33D1  jp       0x4c33dc  ; -> 004C33DC
004C33D3  jne      0x4c33dc  ; -> 004C33DC
004C33D5  mov      edx, 1
004C33DA  jmp      0x4c33de  ; -> 004C33DE
004C33DC  xor      edx, edx
004C33DE  xor      ecx, ecx
004C33E0  comiss   xmm1, xmm6
004C33E3  seta     cl
004C33E6  xor      eax, eax
004C33E8  add      cx, cx
004C33EB  comiss   xmm3, xmm5
004C33EE  seta     al
004C33F1  add      cx, ax
004C33F4  xor      eax, eax
004C33F6  add      cx, cx
004C33F9  comiss   xmm0, xmm4
004C33FC  seta     al
004C33FF  add      cx, ax
004C3402  shl      cx, 2
004C3406  add      cx, r9w
004C340A  add      cx, cx
004C340D  add      cx, r8w
004C3411  add      cx, cx
004C3414  add      cx, dx
004C3417  add      cx, cx
004C341A  ucomiss  xmm1, xmm7
004C341D  jp       0x4c3428  ; -> 004C3428
004C341F  jne      0x4c3428  ; -> 004C3428
004C3421  mov      ebx, 1
004C3426  jmp      0x4c342a  ; -> 004C342A
004C3428  xor      ebx, ebx
004C342A  movss    xmm5, dword ptr [rsp + 0x20]
004C3430  ucomiss  xmm3, xmm5
004C3433  jp       0x4c343f  ; -> 004C343F
004C3435  jne      0x4c343f  ; -> 004C343F
004C3437  mov      r11d, 1
004C343D  jmp      0x4c3442  ; -> 004C3442
004C343F  xor      r11d, r11d
004C3442  movss    xmm4, dword ptr [rsp + 0x24]
004C3448  ucomiss  xmm0, xmm4
004C344B  jp       0x4c3457  ; -> 004C3457
004C344D  jne      0x4c3457  ; -> 004C3457
004C344F  mov      r9d, 1
004C3455  jmp      0x4c345a  ; -> 004C345A
004C3457  xor      r9d, r9d
004C345A  movzx    r10d, word ptr [rip + 0x1ba16aa]  ; -> 02064B0C
004C3462  lea      edx, [r14 + r10]
004C3466  movzx    r8d, dx
004C346A  and      r8w, cx
004C346E  xor      ecx, ecx
004C3470  comiss   xmm7, xmm1
004C3473  mulps    xmm1, xmmword ptr [rip + 0x451f76]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004C347A  seta     cl
004C347D  xor      eax, eax
004C347F  add      cx, cx
004C3482  comiss   xmm5, xmm3
004C3485  cvttps2dq xmm3, xmm1
004C3489  seta     al
004C348C  add      cx, ax
004C348F  xor      eax, eax
004C3491  add      cx, cx
004C3494  comiss   xmm4, xmm0
004C3497  movups   xmmword ptr [rip + 0x1ba1822], xmm3  ; -> 02064CC0
004C349E  seta     al
004C34A1  add      cx, ax
004C34A4  shl      cx, 2
004C34A8  add      cx, bx
004C34AB  add      cx, cx
004C34AE  add      cx, r11w
004C34B2  add      cx, cx
004C34B5  add      cx, r9w
004C34B9  add      cx, cx
004C34BC  and      dx, cx
004C34BF  movsx    eax, dx
004C34C2  add      r8w, ax
004C34C6  mov      word ptr [rip + 0x1ba191b], dx  ; -> 02064DE8
004C34CD  mov      word ptr [rip + 0x1ba190f], r8w  ; -> 02064DE4
004C34D5  cmp      r8w, r10w
004C34D9  jne      0x4c3511  ; -> 004C3511
004C34DB  movsx    edx, word ptr [rip + 0x1ba18d2]  ; -> 02064DB4
004C34E2  movups   xmm0, xmmword ptr [rip + 0x1ba1707]  ; -> 02064BF0
004C34E9  mov      ecx, edx
004C34EB  add      dx, 2
004C34EF  shl      ecx, 4
004C34F2  inc      word ptr [rip + 0x1ba18bf]  ; -> 02064DB8
004C34F9  movsxd   rax, ecx
004C34FC  mov      word ptr [rip + 0x1ba18b1], dx  ; -> 02064DB4
004C3503  movups   xmmword ptr [rax + rbp], xmm0
004C3507  lea      eax, [rcx + 0x10]
004C350A  movsxd   rcx, eax
004C350D  movups   xmmword ptr [rcx + rbp], xmm3
004C3511  movzx    eax, word ptr [rip + 0x1ba18c0]  ; -> 02064DD8
004C3518  cmp      word ptr [rip + 0x1ba1899], ax  ; -> 02064DB8
004C351F  jne      0x4c355d  ; -> 004C355D
004C3521  mov      rdx, rdi
004C3524  mov      rcx, rsi
004C3527  call     0x4c4c40  ; -> 004C4C40 fn
004C352C  movzx    r10d, word ptr [rip + 0x1ba15d8]  ; -> 02064B0C
004C3534  movss    xmm4, dword ptr [rip + 0x193f2fc]  ; -> 01E02838 [u32 0x00000000]
004C353C  movss    xmm5, dword ptr [rip + 0x193f2f0]  ; -> 01E02834 [u32 0x00000000]
004C3544  movss    xmm2, dword ptr [rip + 0x1ba1764]  ; -> 02064CB0
004C354C  movss    xmm7, dword ptr [rip + 0x193f2dc]  ; -> 01E02830 [u32 0x00000000]
004C3554  movss    xmm9, dword ptr [rip + 0x193f2df]  ; -> 01E0283C [f32 1]
004C355D  movzx    r9d, word ptr [rip + 0x1ba1857]  ; -> 02064DBC
004C3565  movss    xmm8, dword ptr [rip + 0x182872e]  ; -> 01CEBC9C [f32 -1]
004C356E  movss    xmm10, dword ptr [rip + 0x84d329]  ; -> 00D108A0 [f32 1e-05]
004C3577  movss    xmm12, dword ptr [rip + 0x18286f8]  ; -> 01CEBC78 [f32 6.283185]
004C3580  movss    xmm13, dword ptr [rip + 0x43e5b3]  ; -> 00901B3C [f32 1.5]
004C3589  test     r9w, r9w
004C358D  jg       0x4c2440  ; -> 004C2440
004C3593  movaps   xmm15, xmmword ptr [rsp + 0x30]
004C3599  movaps   xmm14, xmmword ptr [rsp + 0x40]
004C359F  movaps   xmm13, xmmword ptr [rsp + 0x50]
004C35A5  movaps   xmm12, xmmword ptr [rsp + 0x60]
004C35AB  movaps   xmm11, xmmword ptr [rsp + 0x70]
004C35B1  movaps   xmm10, xmmword ptr [rsp + 0x80]
004C35BA  movaps   xmm9, xmmword ptr [rsp + 0x90]
004C35C3  movaps   xmm8, xmmword ptr [rsp + 0xa0]
004C35CC  movaps   xmm6, xmmword ptr [rsp + 0xc0]
004C35D4  mov      r14, qword ptr [rsp + 0xd0]
004C35DC  mov      rbx, qword ptr [rsp + 0xd8]
004C35E4  cmp      word ptr [rip + 0x1ba17cc], r10w  ; -> 02064DB8
004C35EC  je       0x4c35f9  ; -> 004C35F9
004C35EE  mov      rdx, rdi
004C35F1  mov      rcx, rsi
004C35F4  call     0x4c4c40  ; -> 004C4C40 fn
004C35F9  movaps   xmm7, xmmword ptr [rsp + 0xb0]
004C3601  add      rsp, 0xe0
004C3608  pop      rdi
004C3609  pop      rsi
004C360A  pop      rbp
004C360B  ret      
```

## 004C4D20 (3755 B, extent 004C4D20-004C5BCB)

Page context: "+0x1C' = 0x6C120000, '+0x20' = 0x8000 - a module record's init.  Interior anchor '004C6BC3' (function '004C6BB0').  '004C5BD0' (542 B) is a battery constructor '0037E0F0' calls: '008631E0' registers '004C4D20', '008631D0(0x14)' fills '+0x10', then constants - '+0xC' = 0x02000000, '+0x18' = 0x1000404, '+0x1C' = 0x6C110000, '+0x20' = 0x8000 - a module record's init.  Interior anchor '004C5BE3' (function '004C5BD0').  '004C7CF0' (524 B) is"

```
004C4D20  mov      rax, rsp
004C4D23  push     rbp
004C4D24  push     r14
004C4D26  sub      rsp, 0xc8
004C4D2D  mov      qword ptr [rax + 8], rbx
004C4D31  mov      r14, rcx
004C4D34  mov      qword ptr [rax + 0x18], rdi
004C4D38  xor      r8d, r8d
004C4D3B  mov      qword ptr [rax - 0x18], r15
004C4D3F  mov      rbp, rdx
004C4D42  movzx    eax, word ptr [rip + 0x1b9fdc3]  ; -> 02064B0C
004C4D49  lea      r15, [rip + 0x1ba00e0]  ; -> 02064E30
004C4D50  add      ax, 0xe
004C4D54  mov      word ptr [rip + 0x1ba008d], ax  ; -> 02064DE8
004C4D5B  cwde     
004C4D5C  shl      eax, 4
004C4D5F  movsxd   rcx, eax
004C4D62  add      rcx, r15
004C4D65  call     r14
004C4D68  movsx    r9d, word ptr [rip + 0x1b9fd9c]  ; -> 02064B0C
004C4D70  mov      word ptr [rip + 0x1ba0040], r9w  ; -> 02064DB8
004C4D78  mov      word ptr [rip + 0x1ba0050], r9w  ; -> 02064DD0
004C4D80  lea      eax, [r9 + 1]
004C4D84  shl      eax, 4
004C4D87  movsxd   rcx, eax
004C4D8A  lea      eax, [r9 + 3]
004C4D8E  shl      eax, 4
004C4D91  movups   xmm0, xmmword ptr [rcx + r15]
004C4D96  movsxd   rcx, eax
004C4D99  lea      eax, [r9 + 4]
004C4D9D  shl      eax, 4
004C4DA0  movups   xmmword ptr [rip + 0x1b9fd89], xmm0  ; -> 02064B30
004C4DA7  movups   xmm1, xmmword ptr [rcx + r15]
004C4DAC  movsxd   rcx, eax
004C4DAF  lea      eax, [r9 + 5]
004C4DB3  shl      eax, 4
004C4DB6  movups   xmmword ptr [rip + 0x1b9fe03], xmm1  ; -> 02064BC0
004C4DBD  movups   xmm2, xmmword ptr [rcx + r15]
004C4DC2  movsxd   rcx, eax
004C4DC5  lea      eax, [r9 + 6]
004C4DC9  shl      eax, 4
004C4DCC  mulss    xmm1, xmm2
004C4DD0  movups   xmm0, xmmword ptr [rcx + r15]
004C4DD5  movsxd   rcx, eax
004C4DD8  lea      eax, [r9 + 7]
004C4DDC  maxss    xmm1, dword ptr [rip + 0x193da4c]  ; -> 01E02830 [u32 0x00000000]
004C4DE4  shl      eax, 4
004C4DE7  movups   xmmword ptr [rip + 0x1b9fdf2], xmm0  ; -> 02064BE0
004C4DEE  movups   xmm0, xmmword ptr [rcx + r15]
004C4DF3  movsxd   rcx, eax
004C4DF6  lea      eax, [r9 + 8]
004C4DFA  shl      eax, 4
004C4DFD  movups   xmmword ptr [rip + 0x1b9fdec], xmm0  ; -> 02064BF0
004C4E04  movups   xmm0, xmmword ptr [rcx + r15]
004C4E09  movsxd   rcx, eax
004C4E0C  lea      eax, [r9 + 9]
004C4E10  shl      eax, 4
004C4E13  movups   xmmword ptr [rip + 0x1b9fdf6], xmm0  ; -> 02064C10
004C4E1A  movss    dword ptr [rip + 0x1b9fd9e], xmm1  ; -> 02064BC0
004C4E22  movups   xmm1, xmmword ptr [rcx + r15]
004C4E27  movsxd   rcx, eax
004C4E2A  mov      eax, 0x80
004C4E2F  add      eax, r9d
004C4E32  movups   xmmword ptr [rip + 0x1b9fde7], xmm1  ; -> 02064C20
004C4E39  mov      word ptr [rip + 0x1b9ff70], ax  ; -> 02064DB0
004C4E40  inc      ax
004C4E43  movups   xmm0, xmmword ptr [rcx + r15]
004C4E48  mov      word ptr [rip + 0x1b9ff65], ax  ; -> 02064DB4
004C4E4F  lea      eax, [r9 + 2]
004C4E53  shufps   xmm1, xmm1, 0x55
004C4E57  movups   xmmword ptr [rip + 0x1b9fdd2], xmm0  ; -> 02064C30
004C4E5E  shl      eax, 4
004C4E61  movss    xmm0, dword ptr [rip + 0x1b9fdb7]  ; -> 02064C20
004C4E69  addss    xmm0, xmm0
004C4E6D  movsxd   rdx, eax
004C4E70  movups   xmmword ptr [rip + 0x1b9fd59], xmm2  ; -> 02064BD0
004C4E77  shufps   xmm2, xmm2, 0x55
004C4E7B  subss    xmm1, xmm2
004C4E7F  movss    dword ptr [rip + 0x1b9fdb9], xmm0  ; -> 02064C40
004C4E87  movss    xmm0, dword ptr [rip + 0x1b9fd99]  ; -> 02064C28
004C4E8F  addss    xmm0, xmm0
004C4E93  movss    dword ptr [rip + 0x1b9fd89], xmm1  ; -> 02064C24
004C4E9B  addss    xmm1, xmm1
004C4E9F  movss    dword ptr [rip + 0x1b9fda1], xmm0  ; -> 02064C48
004C4EA7  movss    dword ptr [rip + 0x1b9fd95], xmm1  ; -> 02064C44
004C4EAF  movss    xmm2, dword ptr [rip + 0x193d981]  ; -> 01E02838 [u32 0x00000000]
004C4EB7  lea      eax, [r9 + 0x14]
004C4EBB  movzx    ebx, word ptr [rdx + r15]
004C4EC0  movaps   xmm1, xmm2
004C4EC3  mov      word ptr [rip + 0x1b9ff0e], ax  ; -> 02064DD8
004C4ECA  lea      eax, [r9 + 0xa]
004C4ECE  shl      eax, 4
004C4ED1  movsxd   rcx, eax
004C4ED4  lea      eax, [r9 + 0xb]
004C4ED8  shl      eax, 4
004C4EDB  mov      word ptr [rip + 0x1b9feda], bx  ; -> 02064DBC
004C4EE2  movups   xmm0, xmmword ptr [rcx + r15]
004C4EE7  movsxd   rcx, eax
004C4EEA  lea      eax, [r9 + 0xc]
004C4EEE  shl      eax, 4
004C4EF1  movups   xmmword ptr [rip + 0x1b9fde8], xmm0  ; -> 02064CE0
004C4EF8  movups   xmm0, xmmword ptr [rcx + r15]
004C4EFD  movsxd   rcx, eax
004C4F00  lea      eax, [r9 + 0xd]
004C4F04  shl      eax, 4
004C4F07  inc      r9w
004C4F0B  movups   xmmword ptr [rip + 0x1b9fdde], xmm0  ; -> 02064CF0
004C4F12  mov      word ptr [rip + 0x1b9feb2], r9w  ; -> 02064DCC
004C4F1A  movups   xmm0, xmmword ptr [rcx + r15]
004C4F1F  movsxd   rcx, eax
004C4F22  movzx    eax, word ptr [rdx + r15 + 4]
004C4F28  movups   xmmword ptr [rip + 0x1b9fdd1], xmm0  ; -> 02064D00
004C4F2F  and      ax, r9w
004C4F33  mov      word ptr [rip + 0x1b9fe8e], ax  ; -> 02064DC8
004C4F3A  movups   xmm0, xmmword ptr [rcx + r15]
004C4F3F  movups   xmmword ptr [rip + 0x1b9fdca], xmm0  ; -> 02064D10
004C4F46  movss    xmm0, dword ptr [rip + 0x193d8ee]  ; -> 01E0283C [f32 1]
004C4F4E  addss    xmm1, xmm0
004C4F52  movss    dword ptr [rip + 0x1b9fc0e], xmm1  ; -> 02064B68
004C4F5A  cmp      ax, r9w
004C4F5E  jne      0x4c4f6c  ; -> 004C4F6C
004C4F60  subss    xmm2, xmm0
004C4F64  movss    dword ptr [rip + 0x1b9fbfc], xmm2  ; -> 02064B68
004C4F6C  movss    xmm0, dword ptr [rip + 0x1b9fc50]  ; -> 02064BC4
004C4F74  movss    dword ptr [rip + 0x193d8ac], xmm0  ; -> 01E02828 [f32 1]
004C4F7C  mov      eax, dword ptr [rip + 0x193d8a6]  ; -> 01E02828 [f32 1]
004C4F82  mov      ecx, eax
004C4F84  shr      ecx, 0x12
004C4F87  xor      ecx, eax
004C4F89  mov      dword ptr [rip + 0x1b9fb69], 1  ; -> 02064AFC
004C4F93  and      eax, 0x3fffff
004C4F98  shr      ecx, 4
004C4F9B  or       eax, 0x1fc00000
004C4FA0  and      ecx, 1
004C4FA3  add      eax, eax
004C4FA5  or       ecx, eax
004C4FA7  mov      eax, ecx
004C4FA9  shr      eax, 0x12
004C4FAC  xor      eax, ecx
004C4FAE  and      ecx, 0x3fffff
004C4FB4  or       ecx, 0x1fc00000
004C4FBA  shr      eax, 4
004C4FBD  add      ecx, ecx
004C4FBF  and      eax, 1
004C4FC2  or       eax, ecx
004C4FC4  mov      ecx, eax
004C4FC6  shr      ecx, 0x12
004C4FC9  xor      ecx, eax
004C4FCB  and      eax, 0x3fffff
004C4FD0  or       eax, 0x1fc00000
004C4FD5  shr      ecx, 4
004C4FD8  add      eax, eax
004C4FDA  and      ecx, 1
004C4FDD  or       ecx, eax
004C4FDF  mov      eax, ecx
004C4FE1  shr      eax, 0x12
004C4FE4  xor      eax, ecx
004C4FE6  and      ecx, 0x3fffff
004C4FEC  or       ecx, 0x1fc00000
004C4FF2  shr      eax, 4
004C4FF5  add      ecx, ecx
004C4FF7  and      eax, 1
004C4FFA  or       eax, ecx
004C4FFC  mov      ecx, eax
004C4FFE  shr      ecx, 0x12
004C5001  xor      ecx, eax
004C5003  and      eax, 0x3fffff
004C5008  or       eax, 0x1fc00000
004C500D  shr      ecx, 4
004C5010  add      eax, eax
004C5012  and      ecx, 1
004C5015  or       ecx, eax
004C5017  mov      eax, ecx
004C5019  mov      dword ptr [rip + 0x193d809], ecx  ; -> 01E02828 [f32 1]
004C501F  movss    xmm1, dword ptr [rip + 0x193d801]  ; -> 01E02828 [f32 1]
004C5027  shr      eax, 0x12
004C502A  xor      eax, ecx
004C502C  and      ecx, 0x3fffff
004C5032  or       ecx, 0x1fc00000
004C5038  shr      eax, 4
004C503B  add      ecx, ecx
004C503D  and      eax, 1
004C5040  or       eax, ecx
004C5042  mov      ecx, eax
004C5044  shr      ecx, 0x12
004C5047  xor      ecx, eax
004C5049  and      eax, 0x3fffff
004C504E  or       eax, 0x1fc00000
004C5053  shr      ecx, 4
004C5056  add      eax, eax
004C5058  and      ecx, 1
004C505B  or       ecx, eax
004C505D  mov      eax, ecx
004C505F  shr      eax, 0x12
004C5062  xor      eax, ecx
004C5064  and      ecx, 0x3fffff
004C506A  or       ecx, 0x1fc00000
004C5070  shr      eax, 4
004C5073  add      ecx, ecx
004C5075  and      eax, 1
004C5078  or       eax, ecx
004C507A  mov      ecx, eax
004C507C  shr      ecx, 0x12
004C507F  xor      ecx, eax
004C5081  subss    xmm1, dword ptr [rip + 0x1b9fb87]  ; -> 02064C10
004C5089  and      eax, 0x3fffff
004C508E  shr      ecx, 4
004C5091  or       eax, 0x1fc00000
004C5096  and      ecx, 1
004C5099  add      eax, eax
004C509B  or       ecx, eax
004C509D  mov      edx, ecx
004C509F  movss    dword ptr [rip + 0x1b9fbd9], xmm1  ; -> 02064C80
004C50A7  shr      edx, 0x12
004C50AA  xor      edx, ecx
004C50AC  and      ecx, 0x3fffff
004C50B2  or       ecx, 0x1fc00000
004C50B8  shr      edx, 4
004C50BB  add      ecx, ecx
004C50BD  and      edx, 1
004C50C0  or       edx, ecx
004C50C2  mov      dword ptr [rip + 0x193d760], edx  ; -> 01E02828 [f32 1]
004C50C8  mov      eax, edx
004C50CA  movss    xmm0, dword ptr [rip + 0x193d756]  ; -> 01E02828 [f32 1]
004C50D2  shr      eax, 0x12
004C50D5  xor      eax, edx
004C50D7  movss    dword ptr [rip + 0x1b9fba5], xmm0  ; -> 02064C84
004C50DF  shr      eax, 4
004C50E2  and      edx, 0x3fffff
004C50E8  and      eax, 1
004C50EB  or       edx, 0x1fc00000
004C50F1  add      edx, edx
004C50F3  or       eax, edx
004C50F5  mov      ecx, eax
004C50F7  shr      ecx, 0x12
004C50FA  xor      ecx, eax
004C50FC  and      eax, 0x3fffff
004C5101  or       eax, 0x1fc00000
004C5106  shr      ecx, 4
004C5109  add      eax, eax
004C510B  and      ecx, 1
004C510E  or       ecx, eax
004C5110  mov      eax, ecx
004C5112  shr      eax, 0x12
004C5115  xor      eax, ecx
004C5117  and      ecx, 0x3fffff
004C511D  shr      eax, 4
004C5120  or       ecx, 0x1fc00000
004C5126  add      ecx, ecx
004C5128  and      eax, 1
004C512B  or       eax, ecx
004C512D  mov      ecx, eax
004C512F  shr      ecx, 0x12
004C5132  xor      ecx, eax
004C5134  and      eax, 0x3fffff
004C5139  or       eax, 0x1fc00000
004C513E  shr      ecx, 4
004C5141  add      eax, eax
004C5143  and      ecx, 1
004C5146  or       ecx, eax
004C5148  mov      eax, ecx
004C514A  shr      eax, 0x12
004C514D  xor      eax, ecx
004C514F  and      ecx, 0x3fffff
004C5155  shr      eax, 4
004C5158  or       ecx, 0x1fc00000
004C515E  add      ecx, ecx
004C5160  and      eax, 1
004C5163  or       eax, ecx
004C5165  mov      dword ptr [rip + 0x193d6bd], eax  ; -> 01E02828 [f32 1]
004C516B  movss    xmm0, dword ptr [rip + 0x193d6b5]  ; -> 01E02828 [f32 1]
004C5173  subss    xmm0, dword ptr [rip + 0x1b9fa9d]  ; -> 02064C18
004C517B  movss    dword ptr [rip + 0x1b9fb05], xmm0  ; -> 02064C88
004C5183  call     0x22cc20  ; -> 0022CC20 fn
004C5188  movzx    edi, word ptr [rip + 0x1b9fc2d]  ; -> 02064DBC
004C518F  dec      di
004C5192  mov      word ptr [rip + 0x1b9fc23], di  ; -> 02064DBC
004C5199  test     bx, bx
004C519C  jle      0x4c5b8d  ; -> 004C5B8D
004C51A2  mov      qword ptr [rsp + 0xe8], rsi
004C51AA  mov      qword ptr [rsp + 0xf8], r12
004C51B2  mov      r12d, 0xe0
004C51B8  movaps   xmmword ptr [rsp + 0xb0], xmm6
004C51C0  xorps    xmm6, xmm6
004C51C3  movaps   xmmword ptr [rsp + 0xa0], xmm7
004C51CB  movaps   xmmword ptr [rsp + 0x90], xmm8
004C51D4  movaps   xmmword ptr [rsp + 0x80], xmm9
004C51DD  movaps   xmmword ptr [rsp + 0x70], xmm10
004C51E3  movaps   xmmword ptr [rsp + 0x60], xmm11
004C51E9  movaps   xmmword ptr [rsp + 0x50], xmm12
004C51EF  movaps   xmmword ptr [rsp + 0x40], xmm13
004C51F5  movss    xmm13, dword ptr [rip + 0x18269aa]  ; -> 01CEBBA8 [f32 1]
004C51FE  movaps   xmmword ptr [rsp + 0x30], xmm14
004C5204  movaps   xmmword ptr [rsp + 0x20], xmm15
004C520A  nop      word ptr [rax + rax]
004C5210  movss    xmm8, dword ptr [rip + 0x193d623]  ; -> 01E0283C [f32 1]
004C5219  movss    xmm7, dword ptr [rip + 0x1b9fa5f]  ; -> 02064C80
004C5221  movss    xmm11, dword ptr [rip + 0x1b9fa5e]  ; -> 02064C88
004C522A  movaps   xmm1, xmm7
004C522D  movss    xmm12, dword ptr [rip + 0x1b9fa4e]  ; -> 02064C84
004C5236  movaps   xmm0, xmm11
004C523A  mulss    xmm0, xmm11
004C523F  subss    xmm12, xmm8
004C5244  mulss    xmm1, xmm7
004C5248  mulss    xmm0, xmm8
004C524D  mulss    xmm1, xmm8
004C5252  addss    xmm0, xmm1
004C5256  cvtps2pd xmm0, xmm0
004C5259  andps    xmm0, xmmword ptr [rip + 0x1826b20]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
004C5260  cvtpd2ps xmm0, xmm0
004C5264  call     0x861f14  ; -> 00861F14 fn
004C5269  ucomiss  xmm0, xmm6
004C526C  jp       0x4c527a  ; -> 004C527A
004C526E  jne      0x4c527a  ; -> 004C527A
004C5270  movss    xmm1, dword ptr [rip + 0x43b0e8]  ; -> 00900360 [u32 0x7F7FFFFF]
004C5278  jmp      0x4c5282  ; -> 004C5282
004C527A  movaps   xmm1, xmm8
004C527E  divss    xmm1, xmm0
004C5282  mov      esi, dword ptr [rip + 0x1b9f874]  ; -> 02064AFC
004C5288  test     esi, esi
004C528A  je       0x4c5331  ; -> 004C5331
004C5290  mov      eax, dword ptr [rip + 0x193d592]  ; -> 01E02828 [f32 1]
004C5296  mov      ecx, eax
004C5298  shr      ecx, 0x12
004C529B  xor      ecx, eax
004C529D  and      eax, 0x3fffff
004C52A2  or       eax, 0x1fc00000
004C52A7  shr      ecx, 4
004C52AA  add      eax, eax
004C52AC  and      ecx, 1
004C52AF  or       ecx, eax
004C52B1  mov      eax, ecx
004C52B3  shr      eax, 0x12
004C52B6  xor      eax, ecx
004C52B8  and      ecx, 0x3fffff
004C52BE  shr      eax, 4
004C52C1  or       ecx, 0x1fc00000
004C52C7  and      eax, 1
004C52CA  add      ecx, ecx
004C52CC  or       eax, ecx
004C52CE  mov      ecx, eax
004C52D0  shr      ecx, 0x12
004C52D3  xor      ecx, eax
004C52D5  and      eax, 0x3fffff
004C52DA  or       eax, 0x1fc00000
004C52DF  shr      ecx, 4
004C52E2  add      eax, eax
004C52E4  and      ecx, 1
004C52E7  or       ecx, eax
004C52E9  mov      eax, ecx
004C52EB  shr      eax, 0x12
004C52EE  xor      eax, ecx
004C52F0  and      ecx, 0x3fffff
004C52F6  shr      eax, 4
004C52F9  or       ecx, 0x1fc00000
004C52FF  and      eax, 1
004C5302  add      ecx, ecx
004C5304  or       eax, ecx
004C5306  mov      ebx, eax
004C5308  shr      ebx, 0x12
004C530B  xor      ebx, eax
004C530D  and      eax, 0x3fffff
004C5312  or       eax, 0x1fc00000
004C5317  shr      ebx, 4
004C531A  add      eax, eax
004C531C  and      ebx, 1
004C531F  or       ebx, eax
004C5321  mov      dword ptr [rip + 0x193d501], ebx  ; -> 01E02828 [f32 1]
004C5327  movss    xmm0, dword ptr [rip + 0x193d4f9]  ; -> 01E02828 [f32 1]
004C532F  jmp      0x4c533b  ; -> 004C533B
004C5331  mov      ebx, dword ptr [rip + 0x193d4f1]  ; -> 01E02828 [f32 1]
004C5337  movaps   xmm0, xmm13
004C533B  movss    xmm15, dword ptr [rip + 0x193d4f0]  ; -> 01E02834 [u32 0x00000000]
004C5344  subss    xmm0, xmm8
004C5349  movss    xmm14, dword ptr [rip + 0x193d4de]  ; -> 01E02830 [u32 0x00000000]
004C5352  movaps   xmm10, xmm15
004C5356  subss    xmm10, dword ptr [rip + 0x1b9f885]  ; -> 02064BE4
004C535F  mulss    xmm12, dword ptr [rip + 0x1b9f878]  ; -> 02064BE0
004C5368  mulss    xmm0, dword ptr [rip + 0x1b9f85c]  ; -> 02064BCC
004C5370  mulss    xmm7, xmm1
004C5374  addss    xmm0, dword ptr [rip + 0x1b9f84c]  ; -> 02064BC8
004C537C  mulss    xmm11, xmm1
004C5381  mulss    xmm7, xmm0
004C5385  mulss    xmm11, xmm0
004C538A  movaps   xmm0, xmm10
004C538E  mulss    xmm0, xmm10
004C5393  movaps   xmm6, xmm7
004C5396  addss    xmm6, xmm14
004C539B  movaps   xmm9, xmm11
004C539F  addss    xmm9, dword ptr [rip + 0x193d490]  ; -> 01E02838 [u32 0x00000000]
004C53A8  movss    dword ptr [rip + 0x1b9f924], xmm0  ; -> 02064CD4
004C53B0  mulss    xmm0, xmm8
004C53B5  movaps   xmm2, xmm6
004C53B8  mulss    xmm2, xmm6
004C53BC  movaps   xmm1, xmm9
004C53C0  mulss    xmm1, xmm9
004C53C5  mulss    xmm2, xmm8
004C53CA  movss    dword ptr [rip + 0x1b9f906], xmm1  ; -> 02064CD8
004C53D2  mulss    xmm1, xmm8
004C53D7  addss    xmm2, xmm0
004C53DB  addss    xmm1, xmm2
004C53DF  cvtps2pd xmm0, xmm1
004C53E2  movss    dword ptr [rip + 0x1b9f8f2], xmm1  ; -> 02064CDC
004C53EA  andps    xmm0, xmmword ptr [rip + 0x182698f]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
004C53F1  cvtpd2ps xmm0, xmm0
004C53F5  call     0x861f14  ; -> 00861F14 fn
004C53FA  xorps    xmm1, xmm1
004C53FD  ucomiss  xmm0, xmm1
004C5400  jp       0x4c540e  ; -> 004C540E
004C5402  jne      0x4c540e  ; -> 004C540E
004C5404  movss    xmm1, dword ptr [rip + 0x43af54]  ; -> 00900360 [u32 0x7F7FFFFF]
004C540C  jmp      0x4c5416  ; -> 004C5416
004C540E  movaps   xmm1, xmm8
004C5412  divss    xmm1, xmm0
004C5416  test     esi, esi
004C5418  je       0x4c54bb  ; -> 004C54BB
004C541E  mov      eax, ebx
004C5420  shr      eax, 0x12
004C5423  xor      eax, ebx
004C5425  and      ebx, 0x3fffff
004C542B  shr      eax, 4
004C542E  or       ebx, 0x1fc00000
004C5434  and      eax, 1
004C5437  add      ebx, ebx
004C5439  or       eax, ebx
004C543B  mov      ecx, eax
004C543D  shr      ecx, 0x12
004C5440  xor      ecx, eax
004C5442  and      eax, 0x3fffff
004C5447  shr      ecx, 4
004C544A  or       eax, 0x1fc00000
004C544F  and      ecx, 1
004C5452  add      eax, eax
004C5454  or       ecx, eax
004C5456  mov      eax, ecx
004C5458  shr      eax, 0x12
004C545B  xor      eax, ecx
004C545D  and      ecx, 0x3fffff
004C5463  or       ecx, 0x1fc00000
004C5469  shr      eax, 4
004C546C  add      ecx, ecx
004C546E  and      eax, 1
004C5471  or       eax, ecx
004C5473  mov      ecx, eax
004C5475  shr      ecx, 0x12
004C5478  xor      ecx, eax
004C547A  and      eax, 0x3fffff
004C547F  shr      ecx, 4
004C5482  or       eax, 0x1fc00000
004C5487  and      ecx, 1
004C548A  add      eax, eax
004C548C  or       ecx, eax
004C548E  mov      ebx, ecx
004C5490  shr      ebx, 0x12
004C5493  xor      ebx, ecx
004C5495  and      ecx, 0x3fffff
004C549B  or       ecx, 0x1fc00000
004C54A1  shr      ebx, 4
004C54A4  add      ecx, ecx
004C54A6  and      ebx, 1
004C54A9  or       ebx, ecx
004C54AB  mov      dword ptr [rip + 0x193d377], ebx  ; -> 01E02828 [f32 1]
004C54B1  movss    xmm0, dword ptr [rip + 0x193d36f]  ; -> 01E02828 [f32 1]
004C54B9  jmp      0x4c54bf  ; -> 004C54BF
004C54BB  movaps   xmm0, xmm13
004C54BF  subss    xmm0, xmm8
004C54C4  mulss    xmm6, xmm1
004C54C8  mulss    xmm9, xmm1
004C54CD  mulss    xmm10, xmm1
004C54D2  mulss    xmm0, dword ptr [rip + 0x1b9f702]  ; -> 02064BDC
004C54DA  movss    xmm1, dword ptr [rip + 0x1b9f6de]  ; -> 02064BC0
004C54E2  addss    xmm0, dword ptr [rip + 0x1b9f6ee]  ; -> 02064BD8
004C54EA  mulss    xmm6, xmm0
004C54EE  mulss    xmm9, xmm0
004C54F3  mulss    xmm6, dword ptr [rip + 0x1b9f66d]  ; -> 02064B68
004C54FB  mulss    xmm9, dword ptr [rip + 0x1b9f664]  ; -> 02064B68
004C5504  mulss    xmm10, xmm0
004C5509  movss    xmm0, dword ptr [rip + 0x1b9f72f]  ; -> 02064C40
004C5511  movss    dword ptr [rip + 0x1b9f777], xmm6  ; -> 02064C90
004C5519  mulss    xmm6, xmm1
004C551D  movss    dword ptr [rip + 0x1b9f772], xmm9  ; -> 02064C98
004C5526  mulss    xmm9, xmm1
004C552B  addss    xmm6, xmm7
004C552F  movss    dword ptr [rip + 0x1b9f75c], xmm10  ; -> 02064C94
004C5538  movss    xmm7, dword ptr [rip + 0x1b9f708]  ; -> 02064C48
004C5540  mulss    xmm10, xmm1
004C5545  addss    xmm9, xmm11
004C554A  mulss    xmm1, xmm1
004C554E  addss    xmm10, xmm12
004C5553  mulss    xmm0, xmm1
004C5557  movaps   xmm5, xmm1
004C555A  mulss    xmm5, dword ptr [rip + 0x1b9f6e2]  ; -> 02064C44
004C5562  addss    xmm0, xmm6
004C5566  mulss    xmm7, xmm1
004C556A  movss    dword ptr [rip + 0x1b9f75e], xmm1  ; -> 02064CD0
004C5572  addss    xmm5, xmm10
004C5577  addss    xmm7, xmm9
004C557C  movaps   xmm9, xmm14
004C5580  addss    xmm0, dword ptr [rip + 0x1b9f668]  ; -> 02064BF0
004C5588  addss    xmm9, xmm8
004C558D  addss    xmm5, dword ptr [rip + 0x1b9f65f]  ; -> 02064BF4
004C5595  addss    xmm7, dword ptr [rip + 0x1b9f65b]  ; -> 02064BF8
004C559D  movaps   xmm6, xmm0
004C55A0  movss    dword ptr [rip + 0x1b9f708], xmm0  ; -> 02064CB0
004C55A8  movups   xmm0, xmmword ptr [rip + 0x1b9f731]  ; -> 02064CE0
004C55AF  shufps   xmm6, xmm6, 0
004C55B3  movaps   xmm1, xmm5
004C55B6  mulss    xmm1, dword ptr [rip + 0x1b9f73a]  ; -> 02064CF8
004C55BE  mulps    xmm6, xmm0
004C55C1  movaps   xmm0, xmm5
004C55C4  mulss    xmm0, dword ptr [rip + 0x1b9f724]  ; -> 02064CF0
004C55CC  movss    dword ptr [rip + 0x1b9f6e0], xmm5  ; -> 02064CB4
004C55D4  movups   xmmword ptr [rip + 0x1b9f545], xmm6  ; -> 02064B20
004C55DB  movss    xmm2, dword ptr [rip + 0x1b9f541]  ; -> 02064B24
004C55E3  addss    xmm6, xmm0
004C55E7  movss    xmm3, dword ptr [rip + 0x1b9f539]  ; -> 02064B28
004C55EF  movaps   xmm0, xmm5
004C55F2  mulss    xmm0, dword ptr [rip + 0x1b9f6fa]  ; -> 02064CF4
004C55FA  addss    xmm3, xmm1
004C55FE  movss    xmm4, dword ptr [rip + 0x1b9f526]  ; -> 02064B2C
004C5606  movaps   xmm1, xmm7
004C5609  mulss    xmm1, dword ptr [rip + 0x1b9f6f3]  ; -> 02064D04
004C5611  mulss    xmm5, dword ptr [rip + 0x1b9f6e3]  ; -> 02064CFC
004C5619  addss    xmm2, xmm0
004C561D  movaps   xmm0, xmm7
004C5620  movss    dword ptr [rip + 0x1b9f690], xmm7  ; -> 02064CB8
004C5628  mulss    xmm0, dword ptr [rip + 0x1b9f6d0]  ; -> 02064D00
004C5630  addss    xmm4, xmm5
004C5634  movss    dword ptr [rip + 0x1b9f67f], xmm9  ; -> 02064CBC
004C563D  addss    xmm2, xmm1
004C5641  movaps   xmm1, xmm9
004C5645  mulss    xmm1, dword ptr [rip + 0x1b9f6c7]  ; -> 02064D14
004C564D  addss    xmm6, xmm0
004C5651  movaps   xmm0, xmm7
004C5654  mulss    xmm7, dword ptr [rip + 0x1b9f6b0]  ; -> 02064D0C
004C565C  mulss    xmm0, dword ptr [rip + 0x1b9f6a4]  ; -> 02064D08
004C5664  addss    xmm4, xmm7
004C5668  movss    dword ptr [rip + 0x1b9f4b0], xmm6  ; -> 02064B20
004C5670  movss    dword ptr [rip + 0x1b9f4ac], xmm2  ; -> 02064B24
004C5678  addss    xmm3, xmm0
004C567C  movaps   xmm0, xmm9
004C5680  mulss    xmm0, dword ptr [rip + 0x1b9f688]  ; -> 02064D10
004C5688  movss    dword ptr [rip + 0x1b9f49c], xmm4  ; -> 02064B2C
004C5690  addss    xmm0, xmm6
004C5694  movss    dword ptr [rip + 0x1b9f48c], xmm3  ; -> 02064B28
004C569C  movss    dword ptr [rip + 0x1b9f61c], xmm0  ; -> 02064CC0
004C56A4  movaps   xmm0, xmm9
004C56A8  addss    xmm1, xmm2
004C56AC  mulss    xmm0, dword ptr [rip + 0x1b9f664]  ; -> 02064D18
004C56B4  mulss    xmm9, dword ptr [rip + 0x1b9f65f]  ; -> 02064D1C
004C56BD  addss    xmm0, xmm3
004C56C1  movss    dword ptr [rip + 0x1b9f5fb], xmm1  ; -> 02064CC4
004C56C9  addss    xmm9, xmm4
004C56CE  movss    dword ptr [rip + 0x1b9f5f2], xmm0  ; -> 02064CC8
004C56D6  xorps    xmm0, xmm0
004C56D9  ucomiss  xmm9, xmm0
004C56DD  movss    dword ptr [rip + 0x1b9f5e6], xmm9  ; -> 02064CCC
004C56E6  jp       0x4c56f5  ; -> 004C56F5
004C56E8  jne      0x4c56f5  ; -> 004C56F5
004C56EA  movss    xmm8, dword ptr [rip + 0x43ac6d]  ; -> 00900360 [u32 0x7F7FFFFF]
004C56F3  jmp      0x4c56fa  ; -> 004C56FA
004C56F5  divss    xmm8, xmm9
004C56FA  movss    dword ptr [rip + 0x1b9f3fd], xmm8  ; -> 02064B00
004C5703  test     esi, esi
004C5705  je       0x4c58ee  ; -> 004C58EE
004C570B  mov      eax, ebx
004C570D  shr      eax, 0x12
004C5710  xor      eax, ebx
004C5712  and      ebx, 0x3fffff
004C5718  shr      eax, 4
004C571B  or       ebx, 0x1fc00000
004C5721  and      eax, 1
004C5724  add      ebx, ebx
004C5726  or       eax, ebx
004C5728  mov      ecx, eax
004C572A  shr      ecx, 0x12
004C572D  xor      ecx, eax
004C572F  and      eax, 0x3fffff
004C5734  shr      ecx, 4
004C5737  or       eax, 0x1fc00000
004C573C  and      ecx, 1
004C573F  add      eax, eax
004C5741  or       ecx, eax
004C5743  mov      eax, ecx
004C5745  shr      eax, 0x12
004C5748  xor      eax, ecx
004C574A  and      ecx, 0x3fffff
004C5750  or       ecx, 0x1fc00000
004C5756  shr      eax, 4
004C5759  add      ecx, ecx
004C575B  and      eax, 1
004C575E  or       eax, ecx
004C5760  mov      ecx, eax
004C5762  shr      ecx, 0x12
004C5765  xor      ecx, eax
004C5767  and      eax, 0x3fffff
004C576C  shr      ecx, 4
004C576F  or       eax, 0x1fc00000
004C5774  and      ecx, 1
004C5777  add      eax, eax
004C5779  or       ecx, eax
004C577B  mov      edx, ecx
004C577D  shr      edx, 0x12
004C5780  xor      edx, ecx
004C5782  and      ecx, 0x3fffff
004C5788  or       ecx, 0x1fc00000
004C578E  shr      edx, 4
004C5791  add      ecx, ecx
004C5793  and      edx, 1
004C5796  or       edx, ecx
004C5798  mov      eax, edx
004C579A  mov      dword ptr [rip + 0x193d088], edx  ; -> 01E02828 [f32 1]
004C57A0  movss    xmm3, dword ptr [rip + 0x193d080]  ; -> 01E02828 [f32 1]
004C57A8  shr      eax, 0x12
004C57AB  xor      eax, edx
004C57AD  movss    dword ptr [rip + 0x1b9f4cb], xmm3  ; -> 02064C80
004C57B5  shr      eax, 4
004C57B8  and      edx, 0x3fffff
004C57BE  and      eax, 1
004C57C1  or       edx, 0x1fc00000
004C57C7  add      edx, edx
004C57C9  or       eax, edx
004C57CB  mov      ecx, eax
004C57CD  shr      ecx, 0x12
004C57D0  xor      ecx, eax
004C57D2  and      eax, 0x3fffff
004C57D7  shr      ecx, 4
004C57DA  or       eax, 0x1fc00000
004C57DF  and      ecx, 1
004C57E2  add      eax, eax
004C57E4  or       ecx, eax
004C57E6  mov      eax, ecx
004C57E8  shr      eax, 0x12
004C57EB  xor      eax, ecx
004C57ED  and      ecx, 0x3fffff
004C57F3  or       ecx, 0x1fc00000
004C57F9  shr      eax, 4
004C57FC  add      ecx, ecx
004C57FE  and      eax, 1
004C5801  or       eax, ecx
004C5803  mov      ecx, eax
004C5805  shr      ecx, 0x12
004C5808  xor      ecx, eax
004C580A  shr      ecx, 4
004C580D  and      ecx, 1
004C5810  and      eax, 0x3fffff
004C5815  or       eax, 0x1fc00000
004C581A  add      eax, eax
004C581C  or       ecx, eax
004C581E  mov      edx, ecx
004C5820  shr      edx, 0x12
004C5823  xor      edx, ecx
004C5825  and      ecx, 0x3fffff
004C582B  or       ecx, 0x1fc00000
004C5831  shr      edx, 4
004C5834  add      ecx, ecx
004C5836  and      edx, 1
004C5839  or       edx, ecx
004C583B  mov      dword ptr [rip + 0x193cfe7], edx  ; -> 01E02828 [f32 1]
004C5841  mov      eax, edx
004C5843  movss    xmm0, dword ptr [rip + 0x193cfdd]  ; -> 01E02828 [f32 1]
004C584B  shr      eax, 0x12
004C584E  xor      eax, edx
004C5850  movss    dword ptr [rip + 0x1b9f42c], xmm0  ; -> 02064C84
004C5858  shr      eax, 4
004C585B  and      edx, 0x3fffff
004C5861  and      eax, 1
004C5864  or       edx, 0x1fc00000
004C586A  add      edx, edx
004C586C  or       eax, edx
004C586E  mov      ecx, eax
004C5870  shr      ecx, 0x12
004C5873  xor      ecx, eax
004C5875  and      eax, 0x3fffff
004C587A  or       eax, 0x1fc00000
004C587F  shr      ecx, 4
004C5882  add      eax, eax
004C5884  and      ecx, 1
004C5887  or       ecx, eax
004C5889  mov      eax, ecx
004C588B  shr      eax, 0x12
004C588E  xor      eax, ecx
004C5890  and      ecx, 0x3fffff
004C5896  or       ecx, 0x1fc00000
004C589C  shr      eax, 4
004C589F  add      ecx, ecx
004C58A1  and      eax, 1
004C58A4  or       eax, ecx
004C58A6  mov      ecx, eax
004C58A8  shr      ecx, 0x12
004C58AB  xor      ecx, eax
004C58AD  and      eax, 0x3fffff
004C58B2  or       eax, 0x1fc00000
004C58B7  shr      ecx, 4
004C58BA  add      eax, eax
004C58BC  and      ecx, 1
004C58BF  or       ecx, eax
004C58C1  mov      eax, ecx
004C58C3  shr      eax, 0x12
004C58C6  xor      eax, ecx
004C58C8  and      ecx, 0x3fffff
004C58CE  or       ecx, 0x1fc00000
004C58D4  shr      eax, 4
004C58D7  add      ecx, ecx
004C58D9  and      eax, 1
004C58DC  or       eax, ecx
004C58DE  mov      dword ptr [rip + 0x193cf44], eax  ; -> 01E02828 [f32 1]
004C58E4  movss    xmm4, dword ptr [rip + 0x193cf3c]  ; -> 01E02828 [f32 1]
004C58EC  jmp      0x4c5908  ; -> 004C5908
004C58EE  movaps   xmm3, xmm13
004C58F2  mov      dword ptr [rip + 0x1b9f388], 0x3f800000  ; -> 02064C84
004C58FC  movss    dword ptr [rip + 0x1b9f37c], xmm3  ; -> 02064C80
004C5904  movaps   xmm4, xmm13
004C5908  movups   xmm1, xmmword ptr [rip + 0x1b9f3b1]  ; -> 02064CC0
004C590F  movss    xmm7, dword ptr [rip + 0x1b9f219]  ; -> 02064B30
004C5917  movaps   xmm0, xmm8
004C591B  shufps   xmm0, xmm0, 0
004C591F  mulps    xmm1, xmm0
004C5922  movss    dword ptr [rip + 0x1b9f35e], xmm4  ; -> 02064C88
004C592A  ucomiss  xmm7, xmm1
004C592D  jp       0x4c5939  ; -> 004C5939
004C592F  jne      0x4c5939  ; -> 004C5939
004C5931  mov      r9d, 1
004C5937  jmp      0x4c593c  ; -> 004C593C
004C5939  xor      r9d, r9d
004C593C  movss    xmm6, dword ptr [rip + 0x1b9f1f0]  ; -> 02064B34
004C5944  movaps   xmm2, xmm1
004C5947  shufps   xmm2, xmm1, 0x55
004C594B  ucomiss  xmm6, xmm2
004C594E  jp       0x4c595a  ; -> 004C595A
004C5950  jne      0x4c595a  ; -> 004C595A
004C5952  mov      r8d, 1
004C5958  jmp      0x4c595d  ; -> 004C595D
004C595A  xor      r8d, r8d
004C595D  movss    xmm5, dword ptr [rip + 0x1b9f1d3]  ; -> 02064B38
004C5965  movaps   xmm0, xmm1
004C5968  shufps   xmm0, xmm1, 0xaa
004C596C  ucomiss  xmm5, xmm0
004C596F  jp       0x4c597a  ; -> 004C597A
004C5971  jne      0x4c597a  ; -> 004C597A
004C5973  mov      edx, 1
004C5978  jmp      0x4c597c  ; -> 004C597C
004C597A  xor      edx, edx
004C597C  xor      ecx, ecx
004C597E  comiss   xmm1, xmm7
004C5981  seta     cl
004C5984  xor      eax, eax
004C5986  add      cx, cx
004C5989  comiss   xmm2, xmm6
004C598C  seta     al
004C598F  add      cx, ax
004C5992  xor      eax, eax
004C5994  add      cx, cx
004C5997  comiss   xmm0, xmm5
004C599A  seta     al
004C599D  add      cx, ax
004C59A0  shl      cx, 2
004C59A4  add      cx, r9w
004C59A8  add      cx, cx
004C59AB  add      cx, r8w
004C59AF  add      cx, cx
004C59B2  add      cx, dx
004C59B5  add      cx, cx
004C59B8  ucomiss  xmm1, xmm14
004C59BC  jp       0x4c59c7  ; -> 004C59C7
004C59BE  jne      0x4c59c7  ; -> 004C59C7
004C59C0  mov      ebx, 1
004C59C5  jmp      0x4c59c9  ; -> 004C59C9
004C59C7  xor      ebx, ebx
004C59C9  ucomiss  xmm2, xmm15
004C59CD  jp       0x4c59d9  ; -> 004C59D9
004C59CF  jne      0x4c59d9  ; -> 004C59D9
004C59D1  mov      r11d, 1
004C59D7  jmp      0x4c59dc  ; -> 004C59DC
004C59D9  xor      r11d, r11d
004C59DC  movss    xmm5, dword ptr [rip + 0x193ce54]  ; -> 01E02838 [u32 0x00000000]
004C59E4  ucomiss  xmm0, xmm5
004C59E7  jp       0x4c59f3  ; -> 004C59F3
004C59E9  jne      0x4c59f3  ; -> 004C59F3
004C59EB  mov      r10d, 1
004C59F1  jmp      0x4c59f6  ; -> 004C59F6
004C59F3  xor      r10d, r10d
004C59F6  movzx    r9d, word ptr [rip + 0x1b9f10e]  ; -> 02064B0C
004C59FE  lea      edx, [r12 + r9]
004C5A02  movzx    r8d, dx
004C5A06  and      r8w, cx
004C5A0A  xor      ecx, ecx
004C5A0C  comiss   xmm14, xmm1
004C5A10  seta     cl
004C5A13  xor      eax, eax
004C5A15  add      cx, cx
004C5A18  comiss   xmm15, xmm2
004C5A1C  seta     al
004C5A1F  add      cx, ax
004C5A22  xor      eax, eax
004C5A24  add      cx, cx
004C5A27  comiss   xmm5, xmm0
004C5A2A  movaps   xmm0, xmmword ptr [rip + 0x44f9bf]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004C5A31  mulps    xmm0, xmm1
004C5A34  seta     al
004C5A37  add      cx, ax
004C5A3A  shl      cx, 2
004C5A3E  add      cx, bx
004C5A41  add      cx, cx
004C5A44  add      cx, r11w
004C5A48  add      cx, cx
004C5A4B  add      cx, r10w
004C5A4F  add      cx, cx
004C5A52  and      dx, cx
004C5A55  cvttps2dq xmm2, xmm0
004C5A59  movsx    eax, dx
004C5A5C  add      r8w, ax
004C5A60  mov      word ptr [rip + 0x1b9f381], dx  ; -> 02064DE8
004C5A67  mov      word ptr [rip + 0x1b9f375], r8w  ; -> 02064DE4
004C5A6F  movups   xmmword ptr [rip + 0x1b9f24a], xmm2  ; -> 02064CC0
004C5A76  cmp      r8w, r9w
004C5A7A  jne      0x4c5ac0  ; -> 004C5AC0
004C5A7C  movsx    edx, word ptr [rip + 0x1b9f331]  ; -> 02064DB4
004C5A83  movups   xmm0, xmmword ptr [rip + 0x1b9f1a6]  ; -> 02064C30
004C5A8A  mov      ecx, edx
004C5A8C  shl      ecx, 4
004C5A8F  movsxd   rax, ecx
004C5A92  movups   xmmword ptr [rax + r15], xmm0
004C5A97  lea      eax, [rcx + 0x10]
004C5A9A  movsxd   rcx, eax
004C5A9D  movzx    eax, word ptr [rip + 0x1b9f314]  ; -> 02064DB8
004C5AA4  inc      ax
004C5AA7  add      dx, 2
004C5AAB  mov      word ptr [rip + 0x1b9f306], ax  ; -> 02064DB8
004C5AB2  mov      word ptr [rip + 0x1b9f2fb], dx  ; -> 02064DB4
004C5AB9  movups   xmmword ptr [rcx + r15], xmm2
004C5ABE  jmp      0x4c5ac7  ; -> 004C5AC7
004C5AC0  movzx    eax, word ptr [rip + 0x1b9f2f1]  ; -> 02064DB8
004C5AC7  cmp      ax, word ptr [rip + 0x1b9f30a]  ; -> 02064DD8
004C5ACE  jne      0x4c5af2  ; -> 004C5AF2
004C5AD0  mov      rdx, rbp
004C5AD3  mov      rcx, r14
004C5AD6  call     0x4c4c40  ; -> 004C4C40 fn
004C5ADB  movss    xmm4, dword ptr [rip + 0x1b9f1a5]  ; -> 02064C88
004C5AE3  movss    xmm3, dword ptr [rip + 0x1b9f195]  ; -> 02064C80
004C5AEB  movzx    edi, word ptr [rip + 0x1b9f2ca]  ; -> 02064DBC
004C5AF2  subss    xmm3, dword ptr [rip + 0x1b9f116]  ; -> 02064C10
004C5AFA  subss    xmm4, dword ptr [rip + 0x1b9f116]  ; -> 02064C18
004C5B02  movzx    ebx, di
004C5B05  movss    dword ptr [rip + 0x1b9f173], xmm3  ; -> 02064C80
004C5B0D  movss    dword ptr [rip + 0x1b9f173], xmm4  ; -> 02064C88
004C5B15  call     0x22cc20  ; -> 0022CC20 fn
004C5B1A  movzx    edi, word ptr [rip + 0x1b9f29b]  ; -> 02064DBC
004C5B21  xorps    xmm6, xmm6
004C5B24  dec      di
004C5B27  mov      word ptr [rip + 0x1b9f28e], di  ; -> 02064DBC
004C5B2E  test     bx, bx
004C5B31  jg       0x4c5210  ; -> 004C5210
004C5B37  movaps   xmm15, xmmword ptr [rsp + 0x20]
004C5B3D  movaps   xmm14, xmmword ptr [rsp + 0x30]
004C5B43  movaps   xmm13, xmmword ptr [rsp + 0x40]
004C5B49  movaps   xmm12, xmmword ptr [rsp + 0x50]
004C5B4F  movaps   xmm11, xmmword ptr [rsp + 0x60]
004C5B55  movaps   xmm10, xmmword ptr [rsp + 0x70]
004C5B5B  movaps   xmm9, xmmword ptr [rsp + 0x80]
004C5B64  movaps   xmm8, xmmword ptr [rsp + 0x90]
004C5B6D  movaps   xmm7, xmmword ptr [rsp + 0xa0]
004C5B75  movaps   xmm6, xmmword ptr [rsp + 0xb0]
004C5B7D  mov      r12, qword ptr [rsp + 0xf8]
004C5B85  mov      rsi, qword ptr [rsp + 0xe8]
004C5B8D  movzx    eax, word ptr [rip + 0x1b9ef78]  ; -> 02064B0C
004C5B94  cmp      word ptr [rip + 0x1b9f21d], ax  ; -> 02064DB8
004C5B9B  mov      r15, qword ptr [rsp + 0xc0]
004C5BA3  mov      rdi, qword ptr [rsp + 0xf0]
004C5BAB  mov      rbx, qword ptr [rsp + 0xe0]
004C5BB3  je       0x4c5bc0  ; -> 004C5BC0
004C5BB5  mov      rdx, rbp
004C5BB8  mov      rcx, r14
004C5BBB  call     0x4c4c40  ; -> 004C4C40 fn
004C5BC0  add      rsp, 0xc8
004C5BC7  pop      r14
004C5BC9  pop      rbp
004C5BCA  ret      
```

## 004C5DF0 (3508 B, extent 004C5DF0-004C6BA4)

Page context: "8' colour lanes and '3F800000' scales - a module record's init.  Interior anchor '0047BB03' (function '0047BAF0').  '004C6BB0' (555 B) is a battery constructor '0037E0F0' calls: '008631E0' registers '004C5DF0', '008631D0(0x15)' fills '+0x10', then the same constant shape - '+0xC' = 0x02000000, '+0x18' = 0x1000404, '+0x1C' = 0x6C120000, '+0x20' = 0x8000 - a module record's init.  Interior anchor '004C6BC3' (function '004C6BB0').  '004C5B"

```
004C5DF0  mov      rax, rsp
004C5DF3  push     rbp
004C5DF4  push     rsi
004C5DF5  sub      rsp, 0xc8
004C5DFC  mov      qword ptr [rax + 8], rbx
004C5E00  mov      rbp, rcx
004C5E03  mov      qword ptr [rax + 0x10], rdi
004C5E07  xor      r8d, r8d
004C5E0A  mov      qword ptr [rax + 0x18], r14
004C5E0E  mov      rsi, rdx
004C5E11  movzx    eax, word ptr [rip + 0x1b9ecf4]  ; -> 02064B0C
004C5E18  lea      r14, [rip + 0x1b9f011]  ; -> 02064E30
004C5E1F  add      ax, 0xf
004C5E23  mov      word ptr [rip + 0x1b9efbe], ax  ; -> 02064DE8
004C5E2A  cwde     
004C5E2B  shl      eax, 4
004C5E2E  movsxd   rcx, eax
004C5E31  add      rcx, r14
004C5E34  call     rbp
004C5E36  movsx    edx, word ptr [rip + 0x1b9eccf]  ; -> 02064B0C
004C5E3D  mov      r8d, edx
004C5E40  mov      word ptr [rip + 0x1b9ef71], dx  ; -> 02064DB8
004C5E47  lea      eax, [rdx + 1]
004C5E4A  shl      eax, 4
004C5E4D  movsxd   rcx, eax
004C5E50  lea      eax, [rdx + 3]
004C5E53  shl      eax, 4
004C5E56  movups   xmm0, xmmword ptr [rcx + r14]
004C5E5B  movsxd   rcx, eax
004C5E5E  lea      eax, [rdx + 4]
004C5E61  shl      eax, 4
004C5E64  movups   xmmword ptr [rip + 0x1b9ecc5], xmm0  ; -> 02064B30
004C5E6B  movups   xmm2, xmmword ptr [rcx + r14]
004C5E70  movsxd   rcx, eax
004C5E73  lea      eax, [rdx + 5]
004C5E76  shl      eax, 4
004C5E79  movups   xmmword ptr [rip + 0x1b9ed40], xmm2  ; -> 02064BC0
004C5E80  movups   xmm3, xmmword ptr [rcx + r14]
004C5E85  movsxd   rcx, eax
004C5E88  lea      eax, [rdx + 6]
004C5E8B  shl      eax, 4
004C5E8E  mulss    xmm2, xmm3
004C5E92  movups   xmm0, xmmword ptr [rcx + r14]
004C5E97  movsxd   rcx, eax
004C5E9A  lea      eax, [rdx + 7]
004C5E9D  maxss    xmm2, dword ptr [rip + 0x193c98b]  ; -> 01E02830 [u32 0x00000000]
004C5EA5  shl      eax, 4
004C5EA8  movups   xmmword ptr [rip + 0x1b9ed31], xmm0  ; -> 02064BE0
004C5EAF  movups   xmm0, xmmword ptr [rcx + r14]
004C5EB4  movsxd   rcx, eax
004C5EB7  lea      eax, [rdx + 8]
004C5EBA  shl      eax, 4
004C5EBD  movups   xmmword ptr [rip + 0x1b9ed2c], xmm0  ; -> 02064BF0
004C5EC4  movups   xmm0, xmmword ptr [rcx + r14]
004C5EC9  movsxd   rcx, eax
004C5ECC  lea      eax, [rdx + 9]
004C5ECF  shl      eax, 4
004C5ED2  movups   xmmword ptr [rip + 0x1b9ed27], xmm0  ; -> 02064C00
004C5ED9  movups   xmm4, xmmword ptr [rcx + r14]
004C5EDE  movsxd   rcx, eax
004C5EE1  lea      eax, [rdx + 0xa]
004C5EE4  shl      eax, 4
004C5EE7  movups   xmmword ptr [rip + 0x1b9ece2], xmm3  ; -> 02064BD0
004C5EEE  movups   xmm1, xmmword ptr [rcx + r14]
004C5EF3  movsxd   rcx, eax
004C5EF6  mov      eax, 0x80
004C5EFB  add      eax, edx
004C5EFD  shufps   xmm3, xmm3, 0x55
004C5F01  movups   xmmword ptr [rip + 0x1b9ed18], xmm1  ; -> 02064C20
004C5F08  mov      word ptr [rip + 0x1b9eea1], ax  ; -> 02064DB0
004C5F0F  inc      ax
004C5F12  movups   xmm0, xmmword ptr [rcx + r14]
004C5F17  mov      word ptr [rip + 0x1b9ee96], ax  ; -> 02064DB4
004C5F1E  shufps   xmm1, xmm1, 0x55
004C5F22  movups   xmmword ptr [rip + 0x1b9ed07], xmm0  ; -> 02064C30
004C5F29  movss    xmm0, dword ptr [rip + 0x1b9ecef]  ; -> 02064C20
004C5F31  subss    xmm1, xmm3
004C5F35  addss    xmm0, xmm0
004C5F39  movss    dword ptr [rip + 0x1b9ec7f], xmm2  ; -> 02064BC0
004C5F41  movups   xmmword ptr [rip + 0x1b9ecc8], xmm4  ; -> 02064C10
004C5F48  movss    dword ptr [rip + 0x1b9ecd4], xmm1  ; -> 02064C24
004C5F50  addss    xmm1, xmm1
004C5F54  movss    dword ptr [rip + 0x1b9ece4], xmm0  ; -> 02064C40
004C5F5C  movss    xmm0, dword ptr [rip + 0x1b9ecc4]  ; -> 02064C28
004C5F64  movss    dword ptr [rip + 0x1b9ecd8], xmm1  ; -> 02064C44
004C5F6C  movss    xmm1, dword ptr [rip + 0x1b9ec50]  ; -> 02064BC4
004C5F74  addss    xmm0, xmm0
004C5F78  lea      eax, [rdx + 2]
004C5F7B  movss    dword ptr [rip + 0x193c8a5], xmm1  ; -> 01E02828 [f32 1]
004C5F83  shl      eax, 4
004C5F86  movsxd   rcx, eax
004C5F89  lea      eax, [r8 + 0xb]
004C5F8D  shl      eax, 4
004C5F90  movss    dword ptr [rip + 0x1b9ecb0], xmm0  ; -> 02064C48
004C5F98  mov      word ptr [rip + 0x1b9ee31], dx  ; -> 02064DD0
004C5F9F  add      dx, 0x14
004C5FA3  movzx    ebx, word ptr [rcx + r14]
004C5FA8  movsxd   rcx, eax
004C5FAB  lea      eax, [r8 + 0xc]
004C5FAF  shl      eax, 4
004C5FB2  mov      word ptr [rip + 0x1b9ee03], bx  ; -> 02064DBC
004C5FB9  mov      word ptr [rip + 0x1b9ee18], dx  ; -> 02064DD8
004C5FC0  movups   xmm0, xmmword ptr [rcx + r14]
004C5FC5  movsxd   rcx, eax
004C5FC8  lea      eax, [r8 + 0xd]
004C5FCC  shl      eax, 4
004C5FCF  movups   xmmword ptr [rip + 0x1b9ed0a], xmm0  ; -> 02064CE0
004C5FD6  mov      dword ptr [rip + 0x1b9eb1c], 1  ; -> 02064AFC
004C5FE0  movups   xmm0, xmmword ptr [rcx + r14]
004C5FE5  movsxd   rcx, eax
004C5FE8  lea      eax, [r8 + 0xe]
004C5FEC  shl      eax, 4
004C5FEF  movups   xmmword ptr [rip + 0x1b9ecfa], xmm0  ; -> 02064CF0
004C5FF6  movups   xmm0, xmmword ptr [rcx + r14]
004C5FFB  movsxd   rcx, eax
004C5FFE  mov      eax, dword ptr [rip + 0x193c824]  ; -> 01E02828 [f32 1]
004C6004  movups   xmmword ptr [rip + 0x1b9ecf5], xmm0  ; -> 02064D00
004C600B  movups   xmm0, xmmword ptr [rcx + r14]
004C6010  mov      ecx, eax
004C6012  shr      ecx, 0x12
004C6015  xor      ecx, eax
004C6017  and      eax, 0x3fffff
004C601C  or       eax, 0x1fc00000
004C6021  shr      ecx, 4
004C6024  add      eax, eax
004C6026  and      ecx, 1
004C6029  or       ecx, eax
004C602B  mov      eax, ecx
004C602D  shr      eax, 0x12
004C6030  xor      eax, ecx
004C6032  and      ecx, 0x3fffff
004C6038  or       ecx, 0x1fc00000
004C603E  shr      eax, 4
004C6041  add      ecx, ecx
004C6043  and      eax, 1
004C6046  or       eax, ecx
004C6048  mov      ecx, eax
004C604A  shr      ecx, 0x12
004C604D  xor      ecx, eax
004C604F  and      eax, 0x3fffff
004C6054  or       eax, 0x1fc00000
004C6059  shr      ecx, 4
004C605C  add      eax, eax
004C605E  and      ecx, 1
004C6061  or       ecx, eax
004C6063  mov      eax, ecx
004C6065  shr      eax, 0x12
004C6068  xor      eax, ecx
004C606A  and      ecx, 0x3fffff
004C6070  or       ecx, 0x1fc00000
004C6076  shr      eax, 4
004C6079  add      ecx, ecx
004C607B  and      eax, 1
004C607E  or       eax, ecx
004C6080  mov      ecx, eax
004C6082  shr      ecx, 0x12
004C6085  xor      ecx, eax
004C6087  and      eax, 0x3fffff
004C608C  or       eax, 0x1fc00000
004C6091  shr      ecx, 4
004C6094  add      eax, eax
004C6096  and      ecx, 1
004C6099  or       ecx, eax
004C609B  mov      dword ptr [rip + 0x193c787], ecx  ; -> 01E02828 [f32 1]
004C60A1  movss    xmm1, dword ptr [rip + 0x193c77f]  ; -> 01E02828 [f32 1]
004C60A9  movups   xmmword ptr [rip + 0x1b9ec60], xmm0  ; -> 02064D10
004C60B0  mov      eax, ecx
004C60B2  shr      eax, 0x12
004C60B5  xor      eax, ecx
004C60B7  and      ecx, 0x3fffff
004C60BD  or       ecx, 0x1fc00000
004C60C3  shr      eax, 4
004C60C6  add      ecx, ecx
004C60C8  and      eax, 1
004C60CB  or       eax, ecx
004C60CD  mov      ecx, eax
004C60CF  shr      ecx, 0x12
004C60D2  xor      ecx, eax
004C60D4  and      eax, 0x3fffff
004C60D9  shr      ecx, 4
004C60DC  or       eax, 0x1fc00000
004C60E1  and      ecx, 1
004C60E4  add      eax, eax
004C60E6  or       ecx, eax
004C60E8  mov      eax, ecx
004C60EA  shr      eax, 0x12
004C60ED  xor      eax, ecx
004C60EF  and      ecx, 0x3fffff
004C60F5  or       ecx, 0x1fc00000
004C60FB  shr      eax, 4
004C60FE  add      ecx, ecx
004C6100  and      eax, 1
004C6103  or       eax, ecx
004C6105  mov      ecx, eax
004C6107  shr      ecx, 0x12
004C610A  xor      ecx, eax
004C610C  and      eax, 0x3fffff
004C6111  shr      ecx, 4
004C6114  or       eax, 0x1fc00000
004C6119  and      ecx, 1
004C611C  add      eax, eax
004C611E  or       ecx, eax
004C6120  mov      edx, ecx
004C6122  shr      edx, 0x12
004C6125  xor      edx, ecx
004C6127  and      ecx, 0x3fffff
004C612D  or       ecx, 0x1fc00000
004C6133  shr      edx, 4
004C6136  add      ecx, ecx
004C6138  and      edx, 1
004C613B  or       edx, ecx
004C613D  mov      eax, edx
004C613F  mov      dword ptr [rip + 0x193c6e3], edx  ; -> 01E02828 [f32 1]
004C6145  movss    xmm0, dword ptr [rip + 0x193c6db]  ; -> 01E02828 [f32 1]
004C614D  shr      eax, 0x12
004C6150  xor      eax, edx
004C6152  movss    dword ptr [rip + 0x1b9eb2a], xmm0  ; -> 02064C84
004C615A  shr      eax, 4
004C615D  and      edx, 0x3fffff
004C6163  and      eax, 1
004C6166  or       edx, 0x1fc00000
004C616C  add      edx, edx
004C616E  or       eax, edx
004C6170  mov      ecx, eax
004C6172  shr      ecx, 0x12
004C6175  xor      ecx, eax
004C6177  and      eax, 0x3fffff
004C617C  shr      ecx, 4
004C617F  or       eax, 0x1fc00000
004C6184  and      ecx, 1
004C6187  add      eax, eax
004C6189  or       ecx, eax
004C618B  mov      eax, ecx
004C618D  shr      eax, 0x12
004C6190  xor      eax, ecx
004C6192  and      ecx, 0x3fffff
004C6198  or       ecx, 0x1fc00000
004C619E  shr      eax, 4
004C61A1  add      ecx, ecx
004C61A3  and      eax, 1
004C61A6  or       eax, ecx
004C61A8  mov      ecx, eax
004C61AA  shr      ecx, 0x12
004C61AD  xor      ecx, eax
004C61AF  shr      ecx, 4
004C61B2  and      ecx, 1
004C61B5  and      eax, 0x3fffff
004C61BA  or       eax, 0x1fc00000
004C61BF  subss    xmm1, xmm4
004C61C3  add      eax, eax
004C61C5  shufps   xmm4, xmm4, 0xaa
004C61C9  or       ecx, eax
004C61CB  mov      eax, ecx
004C61CD  shr      eax, 0x12
004C61D0  xor      eax, ecx
004C61D2  movss    dword ptr [rip + 0x1b9eaa6], xmm1  ; -> 02064C80
004C61DA  and      ecx, 0x3fffff
004C61E0  shr      eax, 4
004C61E3  or       ecx, 0x1fc00000
004C61E9  and      eax, 1
004C61EC  add      ecx, ecx
004C61EE  or       eax, ecx
004C61F0  mov      dword ptr [rip + 0x193c632], eax  ; -> 01E02828 [f32 1]
004C61F6  movss    xmm0, dword ptr [rip + 0x193c62a]  ; -> 01E02828 [f32 1]
004C61FE  subss    xmm0, xmm4
004C6202  movss    dword ptr [rip + 0x1b9ea7e], xmm0  ; -> 02064C88
004C620A  call     0x22cc20  ; -> 0022CC20 fn
004C620F  movzx    edi, word ptr [rip + 0x1b9eba6]  ; -> 02064DBC
004C6216  dec      di
004C6219  mov      word ptr [rip + 0x1b9eb9c], di  ; -> 02064DBC
004C6220  test     bx, bx
004C6223  jle      0x4c6b67  ; -> 004C6B67
004C6229  mov      qword ptr [rsp + 0xc0], r15
004C6231  mov      r15d, 0xe0
004C6237  movaps   xmmword ptr [rsp + 0xb0], xmm6
004C623F  movaps   xmmword ptr [rsp + 0xa0], xmm7
004C6247  movaps   xmmword ptr [rsp + 0x90], xmm8
004C6250  movaps   xmmword ptr [rsp + 0x80], xmm9
004C6259  movaps   xmmword ptr [rsp + 0x70], xmm10
004C625F  movss    xmm10, dword ptr [rip + 0x1825940]  ; -> 01CEBBA8 [f32 1]
004C6268  movaps   xmmword ptr [rsp + 0x60], xmm11
004C626E  movaps   xmmword ptr [rsp + 0x50], xmm12
004C6274  movss    xmm12, dword ptr [rip + 0x43a0e3]  ; -> 00900360 [u32 0x7F7FFFFF]
004C627D  movaps   xmmword ptr [rsp + 0x40], xmm13
004C6283  xorps    xmm13, xmm13
004C6287  movaps   xmmword ptr [rsp + 0x30], xmm14
004C628D  movsd    xmm14, qword ptr [rip + 0x1825aea]  ; -> 01CEBD80 [u64 0x7FFFFFFFFFFFFFFF]
004C6296  movaps   xmmword ptr [rsp + 0x20], xmm15
004C629C  movaps   xmm15, xmmword ptr [rip + 0x44f14c]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004C62A4  movss    xmm8, dword ptr [rip + 0x193c58f]  ; -> 01E0283C [f32 1]
004C62AD  movss    xmm6, dword ptr [rip + 0x1b9e9cb]  ; -> 02064C80
004C62B5  movss    xmm7, dword ptr [rip + 0x1b9e9cb]  ; -> 02064C88
004C62BD  movaps   xmm1, xmm6
004C62C0  movss    xmm9, dword ptr [rip + 0x1b9e9bb]  ; -> 02064C84
004C62C9  movaps   xmm0, xmm7
004C62CC  mulss    xmm0, xmm7
004C62D0  subss    xmm9, xmm8
004C62D5  mulss    xmm1, xmm6
004C62D9  mulss    xmm0, xmm8
004C62DE  mulss    xmm1, xmm8
004C62E3  addss    xmm0, xmm1
004C62E7  cvtps2pd xmm0, xmm0
004C62EA  andps    xmm0, xmm14
004C62EE  cvtpd2ps xmm0, xmm0
004C62F2  call     0x861f14  ; -> 00861F14 fn
004C62F7  ucomiss  xmm0, xmm13
004C62FB  jp       0x4c6305  ; -> 004C6305
004C62FD  jne      0x4c6305  ; -> 004C6305
004C62FF  movaps   xmm5, xmm12
004C6303  jmp      0x4c630d  ; -> 004C630D
004C6305  movaps   xmm5, xmm8
004C6309  divss    xmm5, xmm0
004C630D  mov      edx, dword ptr [rip + 0x1b9e7e9]  ; -> 02064AFC
004C6313  test     edx, edx
004C6315  je       0x4c63bc  ; -> 004C63BC
004C631B  mov      eax, dword ptr [rip + 0x193c507]  ; -> 01E02828 [f32 1]
004C6321  mov      ecx, eax
004C6323  shr      ecx, 0x12
004C6326  xor      ecx, eax
004C6328  and      eax, 0x3fffff
004C632D  or       eax, 0x1fc00000
004C6332  shr      ecx, 4
004C6335  add      eax, eax
004C6337  and      ecx, 1
004C633A  or       ecx, eax
004C633C  mov      eax, ecx
004C633E  shr      eax, 0x12
004C6341  xor      eax, ecx
004C6343  and      ecx, 0x3fffff
004C6349  or       ecx, 0x1fc00000
004C634F  shr      eax, 4
004C6352  add      ecx, ecx
004C6354  and      eax, 1
004C6357  or       eax, ecx
004C6359  mov      ecx, eax
004C635B  shr      ecx, 0x12
004C635E  xor      ecx, eax
004C6360  and      eax, 0x3fffff
004C6365  or       eax, 0x1fc00000
004C636A  shr      ecx, 4
004C636D  add      eax, eax
004C636F  and      ecx, 1
004C6372  or       ecx, eax
004C6374  mov      eax, ecx
004C6376  shr      eax, 0x12
004C6379  xor      eax, ecx
004C637B  and      ecx, 0x3fffff
004C6381  or       ecx, 0x1fc00000
004C6387  shr      eax, 4
004C638A  add      ecx, ecx
004C638C  and      eax, 1
004C638F  or       eax, ecx
004C6391  mov      ecx, eax
004C6393  shr      ecx, 0x12
004C6396  xor      ecx, eax
004C6398  and      eax, 0x3fffff
004C639D  or       eax, 0x1fc00000
004C63A2  shr      ecx, 4
004C63A5  add      eax, eax
004C63A7  and      ecx, 1
004C63AA  or       ecx, eax
004C63AC  mov      dword ptr [rip + 0x193c476], ecx  ; -> 01E02828 [f32 1]
004C63B2  movss    xmm1, dword ptr [rip + 0x193c46e]  ; -> 01E02828 [f32 1]
004C63BA  jmp      0x4c63c6  ; -> 004C63C6
004C63BC  mov      ecx, dword ptr [rip + 0x193c466]  ; -> 01E02828 [f32 1]
004C63C2  movaps   xmm1, xmm10
004C63C6  subss    xmm1, xmm8
004C63CB  test     edx, edx
004C63CD  je       0x4c63f0  ; -> 004C63F0
004C63CF  mov      eax, ecx
004C63D1  shr      ecx, 0x12
004C63D4  xor      ecx, eax
004C63D6  and      eax, 0x3fffff
004C63DB  or       eax, 0x1fc00000
004C63E0  shr      ecx, 4
004C63E3  add      eax, eax
004C63E5  and      ecx, 1
004C63E8  or       ecx, eax
004C63EA  mov      dword ptr [rip + 0x193c438], ecx  ; -> 01E02828 [f32 1]
004C63F0  mulss    xmm1, dword ptr [rip + 0x1b9e7d4]  ; -> 02064BCC
004C63F8  addss    xmm1, dword ptr [rip + 0x1b9e7c8]  ; -> 02064BC8
004C6400  test     edx, edx
004C6402  je       0x4c6488  ; -> 004C6488
004C6408  mov      eax, ecx
004C640A  shr      eax, 0x12
004C640D  xor      eax, ecx
004C640F  and      ecx, 0x3fffff
004C6415  or       ecx, 0x1fc00000
004C641B  shr      eax, 4
004C641E  add      ecx, ecx
004C6420  and      eax, 1
004C6423  or       eax, ecx
004C6425  mov      ecx, eax
004C6427  shr      ecx, 0x12
004C642A  xor      ecx, eax
004C642C  and      eax, 0x3fffff
004C6431  or       eax, 0x1fc00000
004C6436  shr      ecx, 4
004C6439  add      eax, eax
004C643B  and      ecx, 1
004C643E  or       ecx, eax
004C6440  mov      eax, ecx
004C6442  shr      eax, 0x12
004C6445  xor      eax, ecx
004C6447  and      ecx, 0x3fffff
004C644D  or       ecx, 0x1fc00000
004C6453  shr      eax, 4
004C6456  add      ecx, ecx
004C6458  and      eax, 1
004C645B  or       eax, ecx
004C645D  mov      ecx, eax
004C645F  shr      ecx, 0x12
004C6462  xor      ecx, eax
004C6464  and      eax, 0x3fffff
004C6469  or       eax, 0x1fc00000
004C646E  shr      ecx, 4
004C6471  add      eax, eax
004C6473  and      ecx, 1
004C6476  or       ecx, eax
004C6478  mov      dword ptr [rip + 0x193c3aa], ecx  ; -> 01E02828 [f32 1]
004C647E  movss    xmm2, dword ptr [rip + 0x193c3a2]  ; -> 01E02828 [f32 1]
004C6486  jmp      0x4c648c  ; -> 004C648C
004C6488  movaps   xmm2, xmm10
004C648C  mulss    xmm9, dword ptr [rip + 0x1b9e74b]  ; -> 02064BE0
004C6495  subss    xmm2, xmm8
004C649A  movss    xmm4, dword ptr [rip + 0x1b9e75e]  ; -> 02064C00
004C64A2  movss    xmm3, dword ptr [rip + 0x1b9e75e]  ; -> 02064C08
004C64AA  movss    xmm11, dword ptr [rip + 0x193c37d]  ; -> 01E02830 [u32 0x00000000]
004C64B3  mulss    xmm2, dword ptr [rip + 0x1b9e721]  ; -> 02064BDC
004C64BB  mulss    xmm6, xmm5
004C64BF  addss    xmm2, dword ptr [rip + 0x1b9e711]  ; -> 02064BD8
004C64C7  mulss    xmm7, xmm5
004C64CB  mulss    xmm6, xmm1
004C64CF  mulss    xmm7, xmm1
004C64D3  movaps   xmm0, xmm2
004C64D6  mulss    xmm0, dword ptr [rip + 0x1b9e726]  ; -> 02064C04
004C64DE  mulss    xmm4, xmm2
004C64E2  movss    dword ptr [rip + 0x1b9e7aa], xmm0  ; -> 02064C94
004C64EA  mulss    xmm3, xmm2
004C64EE  movss    xmm2, dword ptr [rip + 0x1b9e6ca]  ; -> 02064BC0
004C64F6  movaps   xmm1, xmm2
004C64F9  movss    dword ptr [rip + 0x1b9e78f], xmm4  ; -> 02064C90
004C6501  mulss    xmm1, xmm0
004C6505  movss    xmm0, dword ptr [rip + 0x1b9e733]  ; -> 02064C40
004C650D  mulss    xmm4, xmm2
004C6511  addss    xmm1, xmm9
004C6516  movss    dword ptr [rip + 0x1b9e77a], xmm3  ; -> 02064C98
004C651E  mulss    xmm3, xmm2
004C6522  movaps   xmm9, xmm11
004C6526  addss    xmm4, xmm6
004C652A  mulss    xmm2, xmm2
004C652E  addss    xmm3, xmm7
004C6532  movss    xmm7, dword ptr [rip + 0x1b9e70e]  ; -> 02064C48
004C653A  addss    xmm9, xmm8
004C653F  mulss    xmm0, xmm2
004C6543  movaps   xmm5, xmm2
004C6546  mulss    xmm5, dword ptr [rip + 0x1b9e6f6]  ; -> 02064C44
004C654E  addss    xmm0, xmm4
004C6552  mulss    xmm7, xmm2
004C6556  addss    xmm5, xmm1
004C655A  movss    dword ptr [rip + 0x1b9e76e], xmm2  ; -> 02064CD0
004C6562  movss    dword ptr [rip + 0x1b9e751], xmm9  ; -> 02064CBC
004C656B  addss    xmm7, xmm3
004C656F  addss    xmm0, dword ptr [rip + 0x1b9e679]  ; -> 02064BF0
004C6577  addss    xmm5, dword ptr [rip + 0x1b9e675]  ; -> 02064BF4
004C657F  addss    xmm7, dword ptr [rip + 0x1b9e671]  ; -> 02064BF8
004C6587  movaps   xmm6, xmm0
004C658A  movss    dword ptr [rip + 0x1b9e71e], xmm0  ; -> 02064CB0
004C6592  movups   xmm0, xmmword ptr [rip + 0x1b9e747]  ; -> 02064CE0
004C6599  shufps   xmm6, xmm6, 0
004C659D  movaps   xmm1, xmm5
004C65A0  mulss    xmm1, dword ptr [rip + 0x1b9e750]  ; -> 02064CF8
004C65A8  mulps    xmm6, xmm0
004C65AB  movaps   xmm0, xmm5
004C65AE  mulss    xmm0, dword ptr [rip + 0x1b9e73a]  ; -> 02064CF0
004C65B6  movss    dword ptr [rip + 0x1b9e6f6], xmm5  ; -> 02064CB4
004C65BE  movups   xmmword ptr [rip + 0x1b9e55b], xmm6  ; -> 02064B20
004C65C5  movss    xmm2, dword ptr [rip + 0x1b9e557]  ; -> 02064B24
004C65CD  addss    xmm6, xmm0
004C65D1  movss    xmm3, dword ptr [rip + 0x1b9e54f]  ; -> 02064B28
004C65D9  movaps   xmm0, xmm5
004C65DC  mulss    xmm0, dword ptr [rip + 0x1b9e710]  ; -> 02064CF4
004C65E4  addss    xmm3, xmm1
004C65E8  movss    xmm4, dword ptr [rip + 0x1b9e53c]  ; -> 02064B2C
004C65F0  movaps   xmm1, xmm7
004C65F3  mulss    xmm5, dword ptr [rip + 0x1b9e701]  ; -> 02064CFC
004C65FB  mulss    xmm1, dword ptr [rip + 0x1b9e701]  ; -> 02064D04
004C6603  addss    xmm2, xmm0
004C6607  movaps   xmm0, xmm7
004C660A  movss    dword ptr [rip + 0x1b9e6a6], xmm7  ; -> 02064CB8
004C6612  mulss    xmm0, dword ptr [rip + 0x1b9e6e6]  ; -> 02064D00
004C661A  addss    xmm4, xmm5
004C661E  addss    xmm2, xmm1
004C6622  addss    xmm6, xmm0
004C6626  movaps   xmm0, xmm7
004C6629  mulss    xmm0, dword ptr [rip + 0x1b9e6d7]  ; -> 02064D08
004C6631  mulss    xmm7, dword ptr [rip + 0x1b9e6d3]  ; -> 02064D0C
004C6639  addss    xmm3, xmm0
004C663D  movss    dword ptr [rip + 0x1b9e4db], xmm6  ; -> 02064B20
004C6645  movss    dword ptr [rip + 0x1b9e4d7], xmm2  ; -> 02064B24
004C664D  movaps   xmm0, xmm9
004C6651  addss    xmm4, xmm7
004C6655  movss    dword ptr [rip + 0x1b9e4cb], xmm3  ; -> 02064B28
004C665D  movss    dword ptr [rip + 0x1b9e4c7], xmm4  ; -> 02064B2C
004C6665  mulss    xmm0, dword ptr [rip + 0x1b9e6a3]  ; -> 02064D10
004C666D  movaps   xmm1, xmm9
004C6671  mulss    xmm1, dword ptr [rip + 0x1b9e69b]  ; -> 02064D14
004C6679  addss    xmm0, xmm6
004C667D  addss    xmm1, xmm2
004C6681  movss    dword ptr [rip + 0x1b9e637], xmm0  ; -> 02064CC0
004C6689  movaps   xmm0, xmm9
004C668D  mulss    xmm9, dword ptr [rip + 0x1b9e686]  ; -> 02064D1C
004C6696  mulss    xmm0, dword ptr [rip + 0x1b9e67a]  ; -> 02064D18
004C669E  addss    xmm9, xmm4
004C66A3  movss    dword ptr [rip + 0x1b9e619], xmm1  ; -> 02064CC4
004C66AB  addss    xmm0, xmm3
004C66AF  ucomiss  xmm9, xmm13
004C66B3  movss    dword ptr [rip + 0x1b9e60d], xmm0  ; -> 02064CC8
004C66BB  movss    dword ptr [rip + 0x1b9e608], xmm9  ; -> 02064CCC
004C66C4  jp       0x4c66d7  ; -> 004C66D7
004C66C6  jne      0x4c66d7  ; -> 004C66D7
004C66C8  movss    dword ptr [rip + 0x1b9e42f], xmm12  ; -> 02064B00
004C66D1  movaps   xmm8, xmm12
004C66D5  jmp      0x4c66e5  ; -> 004C66E5
004C66D7  divss    xmm8, xmm9
004C66DC  movss    dword ptr [rip + 0x1b9e41b], xmm8  ; -> 02064B00
004C66E5  test     edx, edx
004C66E7  je       0x4c68d0  ; -> 004C68D0
004C66ED  mov      eax, ecx
004C66EF  shr      eax, 0x12
004C66F2  xor      eax, ecx
004C66F4  and      ecx, 0x3fffff
004C66FA  or       ecx, 0x1fc00000
004C6700  shr      eax, 4
004C6703  add      ecx, ecx
004C6705  and      eax, 1
004C6708  or       eax, ecx
004C670A  mov      ecx, eax
004C670C  shr      ecx, 0x12
004C670F  xor      ecx, eax
004C6711  and      eax, 0x3fffff
004C6716  shr      ecx, 4
004C6719  or       eax, 0x1fc00000
004C671E  and      ecx, 1
004C6721  add      eax, eax
004C6723  or       ecx, eax
004C6725  mov      eax, ecx
004C6727  shr      eax, 0x12
004C672A  xor      eax, ecx
004C672C  and      ecx, 0x3fffff
004C6732  or       ecx, 0x1fc00000
004C6738  shr      eax, 4
004C673B  add      ecx, ecx
004C673D  and      eax, 1
004C6740  or       eax, ecx
004C6742  mov      ecx, eax
004C6744  shr      ecx, 0x12
004C6747  xor      ecx, eax
004C6749  and      eax, 0x3fffff
004C674E  shr      ecx, 4
004C6751  or       eax, 0x1fc00000
004C6756  and      ecx, 1
004C6759  add      eax, eax
004C675B  or       ecx, eax
004C675D  mov      edx, ecx
004C675F  shr      edx, 0x12
004C6762  xor      edx, ecx
004C6764  and      ecx, 0x3fffff
004C676A  or       ecx, 0x1fc00000
004C6770  shr      edx, 4
004C6773  add      ecx, ecx
004C6775  and      edx, 1
004C6778  or       edx, ecx
004C677A  mov      eax, edx
004C677C  mov      dword ptr [rip + 0x193c0a6], edx  ; -> 01E02828 [f32 1]
004C6782  movss    xmm2, dword ptr [rip + 0x193c09e]  ; -> 01E02828 [f32 1]
004C678A  shr      eax, 0x12
004C678D  xor      eax, edx
004C678F  movss    dword ptr [rip + 0x1b9e4e9], xmm2  ; -> 02064C80
004C6797  shr      eax, 4
004C679A  and      edx, 0x3fffff
004C67A0  and      eax, 1
004C67A3  or       edx, 0x1fc00000
004C67A9  add      edx, edx
004C67AB  or       eax, edx
004C67AD  mov      ecx, eax
004C67AF  shr      ecx, 0x12
004C67B2  xor      ecx, eax
004C67B4  and      eax, 0x3fffff
004C67B9  shr      ecx, 4
004C67BC  or       eax, 0x1fc00000
004C67C1  and      ecx, 1
004C67C4  add      eax, eax
004C67C6  or       ecx, eax
004C67C8  mov      eax, ecx
004C67CA  shr      eax, 0x12
004C67CD  xor      eax, ecx
004C67CF  and      ecx, 0x3fffff
004C67D5  or       ecx, 0x1fc00000
004C67DB  shr      eax, 4
004C67DE  add      ecx, ecx
004C67E0  and      eax, 1
004C67E3  or       eax, ecx
004C67E5  mov      ecx, eax
004C67E7  shr      ecx, 0x12
004C67EA  xor      ecx, eax
004C67EC  shr      ecx, 4
004C67EF  and      ecx, 1
004C67F2  and      eax, 0x3fffff
004C67F7  or       eax, 0x1fc00000
004C67FC  add      eax, eax
004C67FE  or       ecx, eax
004C6800  mov      edx, ecx
004C6802  shr      edx, 0x12
004C6805  xor      edx, ecx
004C6807  and      ecx, 0x3fffff
004C680D  or       ecx, 0x1fc00000
004C6813  shr      edx, 4
004C6816  add      ecx, ecx
004C6818  and      edx, 1
004C681B  or       edx, ecx
004C681D  mov      dword ptr [rip + 0x193c005], edx  ; -> 01E02828 [f32 1]
004C6823  mov      eax, edx
004C6825  movss    xmm0, dword ptr [rip + 0x193bffb]  ; -> 01E02828 [f32 1]
004C682D  shr      eax, 0x12
004C6830  xor      eax, edx
004C6832  movss    dword ptr [rip + 0x1b9e44a], xmm0  ; -> 02064C84
004C683A  shr      eax, 4
004C683D  and      edx, 0x3fffff
004C6843  and      eax, 1
004C6846  or       edx, 0x1fc00000
004C684C  add      edx, edx
004C684E  or       eax, edx
004C6850  mov      ecx, eax
004C6852  shr      ecx, 0x12
004C6855  xor      ecx, eax
004C6857  and      eax, 0x3fffff
004C685C  or       eax, 0x1fc00000
004C6861  shr      ecx, 4
004C6864  add      eax, eax
004C6866  and      ecx, 1
004C6869  or       ecx, eax
004C686B  mov      eax, ecx
004C686D  shr      eax, 0x12
004C6870  xor      eax, ecx
004C6872  and      ecx, 0x3fffff
004C6878  or       ecx, 0x1fc00000
004C687E  shr      eax, 4
004C6881  add      ecx, ecx
004C6883  and      eax, 1
004C6886  or       eax, ecx
004C6888  mov      ecx, eax
004C688A  shr      ecx, 0x12
004C688D  xor      ecx, eax
004C688F  and      eax, 0x3fffff
004C6894  or       eax, 0x1fc00000
004C6899  shr      ecx, 4
004C689C  add      eax, eax
004C689E  and      ecx, 1
004C68A1  or       ecx, eax
004C68A3  mov      eax, ecx
004C68A5  shr      eax, 0x12
004C68A8  xor      eax, ecx
004C68AA  and      ecx, 0x3fffff
004C68B0  or       ecx, 0x1fc00000
004C68B6  shr      eax, 4
004C68B9  add      ecx, ecx
004C68BB  and      eax, 1
004C68BE  or       eax, ecx
004C68C0  mov      dword ptr [rip + 0x193bf62], eax  ; -> 01E02828 [f32 1]
004C68C6  movss    xmm4, dword ptr [rip + 0x193bf5a]  ; -> 01E02828 [f32 1]
004C68CE  jmp      0x4c68ea  ; -> 004C68EA
004C68D0  movaps   xmm2, xmm10
004C68D4  mov      dword ptr [rip + 0x1b9e3a6], 0x3f800000  ; -> 02064C84
004C68DE  movss    dword ptr [rip + 0x1b9e39a], xmm2  ; -> 02064C80
004C68E6  movaps   xmm4, xmm10
004C68EA  movups   xmm1, xmmword ptr [rip + 0x1b9e3cf]  ; -> 02064CC0
004C68F1  movss    xmm7, dword ptr [rip + 0x1b9e237]  ; -> 02064B30
004C68F9  movaps   xmm0, xmm8
004C68FD  shufps   xmm0, xmm0, 0
004C6901  mulps    xmm1, xmm0
004C6904  movss    dword ptr [rip + 0x1b9e37c], xmm4  ; -> 02064C88
004C690C  ucomiss  xmm7, xmm1
004C690F  jp       0x4c691b  ; -> 004C691B
004C6911  jne      0x4c691b  ; -> 004C691B
004C6913  mov      r9d, 1
004C6919  jmp      0x4c691e  ; -> 004C691E
004C691B  xor      r9d, r9d
004C691E  movss    xmm6, dword ptr [rip + 0x1b9e20e]  ; -> 02064B34
004C6926  movaps   xmm0, xmm1
004C6929  shufps   xmm0, xmm1, 0x55
004C692D  ucomiss  xmm6, xmm0
004C6930  jp       0x4c693c  ; -> 004C693C
004C6932  jne      0x4c693c  ; -> 004C693C
004C6934  mov      r8d, 1
004C693A  jmp      0x4c693f  ; -> 004C693F
004C693C  xor      r8d, r8d
004C693F  movss    xmm5, dword ptr [rip + 0x1b9e1f1]  ; -> 02064B38
004C6947  movaps   xmm3, xmm1
004C694A  shufps   xmm3, xmm1, 0xaa
004C694E  ucomiss  xmm5, xmm3
004C6951  jp       0x4c695c  ; -> 004C695C
004C6953  jne      0x4c695c  ; -> 004C695C
004C6955  mov      edx, 1
004C695A  jmp      0x4c695e  ; -> 004C695E
004C695C  xor      edx, edx
004C695E  xor      ecx, ecx
004C6960  comiss   xmm1, xmm7
004C6963  seta     cl
004C6966  xor      eax, eax
004C6968  add      cx, cx
004C696B  comiss   xmm0, xmm6
004C696E  seta     al
004C6971  add      cx, ax
004C6974  xor      eax, eax
004C6976  add      cx, cx
004C6979  comiss   xmm3, xmm5
004C697C  seta     al
004C697F  add      cx, ax
004C6982  shl      cx, 2
004C6986  add      cx, r9w
004C698A  add      cx, cx
004C698D  add      cx, r8w
004C6991  add      cx, cx
004C6994  add      cx, dx
004C6997  add      cx, cx
004C699A  ucomiss  xmm1, xmm11
004C699E  jp       0x4c69a9  ; -> 004C69A9
004C69A0  jne      0x4c69a9  ; -> 004C69A9
004C69A2  mov      ebx, 1
004C69A7  jmp      0x4c69ab  ; -> 004C69AB
004C69A9  xor      ebx, ebx
004C69AB  movss    xmm6, dword ptr [rip + 0x193be81]  ; -> 01E02834 [u32 0x00000000]
004C69B3  ucomiss  xmm0, xmm6
004C69B6  jp       0x4c69c2  ; -> 004C69C2
004C69B8  jne      0x4c69c2  ; -> 004C69C2
004C69BA  mov      r11d, 1
004C69C0  jmp      0x4c69c5  ; -> 004C69C5
004C69C2  xor      r11d, r11d
004C69C5  movss    xmm5, dword ptr [rip + 0x193be6b]  ; -> 01E02838 [u32 0x00000000]
004C69CD  ucomiss  xmm3, xmm5
004C69D0  jp       0x4c69dc  ; -> 004C69DC
004C69D2  jne      0x4c69dc  ; -> 004C69DC
004C69D4  mov      r10d, 1
004C69DA  jmp      0x4c69df  ; -> 004C69DF
004C69DC  xor      r10d, r10d
004C69DF  movzx    r9d, word ptr [rip + 0x1b9e125]  ; -> 02064B0C
004C69E7  lea      edx, [r15 + r9]
004C69EB  movzx    r8d, dx
004C69EF  and      r8w, cx
004C69F3  xor      ecx, ecx
004C69F5  comiss   xmm11, xmm1
004C69F9  seta     cl
004C69FC  xor      eax, eax
004C69FE  add      cx, cx
004C6A01  comiss   xmm6, xmm0
004C6A04  movaps   xmm0, xmm15
004C6A08  mulps    xmm0, xmm1
004C6A0B  seta     al
004C6A0E  add      cx, ax
004C6A11  xor      eax, eax
004C6A13  add      cx, cx
004C6A16  comiss   xmm5, xmm3
004C6A19  cvttps2dq xmm3, xmm0
004C6A1D  seta     al
004C6A20  add      cx, ax
004C6A23  shl      cx, 2
004C6A27  add      cx, bx
004C6A2A  add      cx, cx
004C6A2D  add      cx, r11w
004C6A31  add      cx, cx
004C6A34  add      cx, r10w
004C6A38  add      cx, cx
004C6A3B  and      dx, cx
004C6A3E  movsx    eax, dx
004C6A41  add      r8w, ax
004C6A45  mov      word ptr [rip + 0x1b9e39c], dx  ; -> 02064DE8
004C6A4C  mov      word ptr [rip + 0x1b9e390], r8w  ; -> 02064DE4
004C6A54  movups   xmmword ptr [rip + 0x1b9e265], xmm3  ; -> 02064CC0
004C6A5B  cmp      r8w, r9w
004C6A5F  jne      0x4c6aa5  ; -> 004C6AA5
004C6A61  movsx    edx, word ptr [rip + 0x1b9e34c]  ; -> 02064DB4
004C6A68  movups   xmm0, xmmword ptr [rip + 0x1b9e1c1]  ; -> 02064C30
004C6A6F  mov      ecx, edx
004C6A71  shl      ecx, 4
004C6A74  movsxd   rax, ecx
004C6A77  movups   xmmword ptr [rax + r14], xmm0
004C6A7C  lea      eax, [rcx + 0x10]
004C6A7F  movsxd   rcx, eax
004C6A82  movzx    eax, word ptr [rip + 0x1b9e32f]  ; -> 02064DB8
004C6A89  inc      ax
004C6A8C  add      dx, 2
004C6A90  mov      word ptr [rip + 0x1b9e321], ax  ; -> 02064DB8
004C6A97  mov      word ptr [rip + 0x1b9e316], dx  ; -> 02064DB4
004C6A9E  movups   xmmword ptr [rcx + r14], xmm3
004C6AA3  jmp      0x4c6aac  ; -> 004C6AAC
004C6AA5  movzx    eax, word ptr [rip + 0x1b9e30c]  ; -> 02064DB8
004C6AAC  cmp      ax, word ptr [rip + 0x1b9e325]  ; -> 02064DD8
004C6AB3  jne      0x4c6ad7  ; -> 004C6AD7
004C6AB5  mov      rdx, rsi
004C6AB8  mov      rcx, rbp
004C6ABB  call     0x4c4c40  ; -> 004C4C40 fn
004C6AC0  movss    xmm4, dword ptr [rip + 0x1b9e1c0]  ; -> 02064C88
004C6AC8  movss    xmm2, dword ptr [rip + 0x1b9e1b0]  ; -> 02064C80
004C6AD0  movzx    edi, word ptr [rip + 0x1b9e2e5]  ; -> 02064DBC
004C6AD7  subss    xmm2, dword ptr [rip + 0x1b9e131]  ; -> 02064C10
004C6ADF  subss    xmm4, dword ptr [rip + 0x1b9e131]  ; -> 02064C18
004C6AE7  movzx    ebx, di
004C6AEA  movss    dword ptr [rip + 0x1b9e18e], xmm2  ; -> 02064C80
004C6AF2  movss    dword ptr [rip + 0x1b9e18e], xmm4  ; -> 02064C88
004C6AFA  call     0x22cc20  ; -> 0022CC20 fn
004C6AFF  movzx    edi, word ptr [rip + 0x1b9e2b6]  ; -> 02064DBC
004C6B06  dec      di
004C6B09  mov      word ptr [rip + 0x1b9e2ac], di  ; -> 02064DBC
004C6B10  test     bx, bx
004C6B13  jg       0x4c62a4  ; -> 004C62A4
004C6B19  movaps   xmm15, xmmword ptr [rsp + 0x20]
004C6B1F  movaps   xmm14, xmmword ptr [rsp + 0x30]
004C6B25  movaps   xmm13, xmmword ptr [rsp + 0x40]
004C6B2B  movaps   xmm12, xmmword ptr [rsp + 0x50]
004C6B31  movaps   xmm11, xmmword ptr [rsp + 0x60]
004C6B37  movaps   xmm10, xmmword ptr [rsp + 0x70]
004C6B3D  movaps   xmm9, xmmword ptr [rsp + 0x80]
004C6B46  movaps   xmm8, xmmword ptr [rsp + 0x90]
004C6B4F  movaps   xmm7, xmmword ptr [rsp + 0xa0]
004C6B57  movaps   xmm6, xmmword ptr [rsp + 0xb0]
004C6B5F  mov      r15, qword ptr [rsp + 0xc0]
004C6B67  movzx    eax, word ptr [rip + 0x1b9df9e]  ; -> 02064B0C
004C6B6E  cmp      word ptr [rip + 0x1b9e243], ax  ; -> 02064DB8
004C6B75  mov      r14, qword ptr [rsp + 0xf0]
004C6B7D  mov      rdi, qword ptr [rsp + 0xe8]
004C6B85  mov      rbx, qword ptr [rsp + 0xe0]
004C6B8D  je       0x4c6b9a  ; -> 004C6B9A
004C6B8F  mov      rdx, rsi
004C6B92  mov      rcx, rbp
004C6B95  call     0x4c4c40  ; -> 004C4C40 fn
004C6B9A  add      rsp, 0xc8
004C6BA1  pop      rsi
004C6BA2  pop      rbp
004C6BA3  ret      
```

## 004C6DE0 (3851 B, extent 004C6DE0-004C7CEB)

Page context: "+0x1C' = 0x6C110000, '+0x20' = 0x8000 - a module record's init.  Interior anchor '004C5BE3' (function '004C5BD0').  '004C7CF0' (524 B) is a battery constructor '0037E0F0' calls: '008631E0' registers '004C6DE0', '008631D0(0x14)' fills '+0x10', then the '0x02000000'/'0x1000404'/'0x6C110000'/'0x8000' head shared with '004C5BD0' - a module record's init.  Interior anchor '004C7D03' (function '004C7CF0').  '004DB060' (523 B) is the battery's"

```
004C6DE0  push     rbp
004C6DE2  push     r14
004C6DE4  push     r15
004C6DE6  sub      rsp, 0xc0
004C6DED  movzx    eax, word ptr [rip + 0x1b9dd18]  ; -> 02064B0C
004C6DF4  lea      r15, [rip + 0x1b9e035]  ; -> 02064E30
004C6DFB  add      ax, 0xe
004C6DFF  mov      r14, rcx
004C6E02  mov      word ptr [rip + 0x1b9dfdf], ax  ; -> 02064DE8
004C6E09  xor      r8d, r8d
004C6E0C  cwde     
004C6E0D  mov      rbp, rdx
004C6E10  shl      eax, 4
004C6E13  movsxd   rcx, eax
004C6E16  add      rcx, r15
004C6E19  call     r14
004C6E1C  movsx    edx, word ptr [rip + 0x1b9dce9]  ; -> 02064B0C
004C6E23  mov      r8d, edx
004C6E26  mov      word ptr [rip + 0x1b9df8b], dx  ; -> 02064DB8
004C6E2D  mov      word ptr [rip + 0x1b9df9c], dx  ; -> 02064DD0
004C6E34  lea      eax, [rdx + 1]
004C6E37  shl      eax, 4
004C6E3A  movsxd   rcx, eax
004C6E3D  lea      eax, [rdx + 3]
004C6E40  shl      eax, 4
004C6E43  movups   xmm0, xmmword ptr [rcx + r15]
004C6E48  movsxd   rcx, eax
004C6E4B  lea      eax, [rdx + 4]
004C6E4E  shl      eax, 4
004C6E51  movups   xmmword ptr [rip + 0x1b9dcd8], xmm0  ; -> 02064B30
004C6E58  movups   xmm2, xmmword ptr [rcx + r15]
004C6E5D  movsxd   rcx, eax
004C6E60  lea      eax, [rdx + 5]
004C6E63  shl      eax, 4
004C6E66  movups   xmmword ptr [rip + 0x1b9dd53], xmm2  ; -> 02064BC0
004C6E6D  movups   xmm3, xmmword ptr [rcx + r15]
004C6E72  movsxd   rcx, eax
004C6E75  lea      eax, [rdx + 6]
004C6E78  shl      eax, 4
004C6E7B  mulss    xmm2, xmm3
004C6E7F  movups   xmm0, xmmword ptr [rcx + r15]
004C6E84  movsxd   rcx, eax
004C6E87  lea      eax, [rdx + 7]
004C6E8A  maxss    xmm2, dword ptr [rip + 0x193b99e]  ; -> 01E02830 [u32 0x00000000]
004C6E92  shl      eax, 4
004C6E95  movups   xmmword ptr [rip + 0x1b9dd44], xmm0  ; -> 02064BE0
004C6E9C  movups   xmm0, xmmword ptr [rcx + r15]
004C6EA1  movsxd   rcx, eax
004C6EA4  lea      eax, [rdx + 8]
004C6EA7  shl      eax, 4
004C6EAA  movups   xmmword ptr [rip + 0x1b9dd3f], xmm0  ; -> 02064BF0
004C6EB1  movups   xmm0, xmmword ptr [rcx + r15]
004C6EB6  movsxd   rcx, eax
004C6EB9  lea      eax, [rdx + 9]
004C6EBC  shl      eax, 4
004C6EBF  movups   xmmword ptr [rip + 0x1b9dd3a], xmm0  ; -> 02064C00
004C6EC6  movups   xmm1, xmmword ptr [rcx + r15]
004C6ECB  movsxd   rcx, eax
004C6ECE  mov      eax, 0x80
004C6ED3  add      eax, edx
004C6ED5  movss    dword ptr [rip + 0x1b9dce3], xmm2  ; -> 02064BC0
004C6EDD  movups   xmmword ptr [rip + 0x1b9dd2c], xmm1  ; -> 02064C10
004C6EE4  mov      word ptr [rip + 0x1b9dec5], ax  ; -> 02064DB0
004C6EEB  inc      ax
004C6EEE  movups   xmm0, xmmword ptr [rcx + r15]
004C6EF3  mov      word ptr [rip + 0x1b9deba], ax  ; -> 02064DB4
004C6EFA  lea      eax, [rdx + 2]
004C6EFD  shufps   xmm1, xmm1, 0x55
004C6F01  movups   xmmword ptr [rip + 0x1b9dd18], xmm0  ; -> 02064C20
004C6F08  shl      eax, 4
004C6F0B  movss    xmm0, dword ptr [rip + 0x1b9dcfd]  ; -> 02064C10
004C6F13  addss    xmm0, xmm0
004C6F17  movsxd   rcx, eax
004C6F1A  movups   xmmword ptr [rip + 0x1b9dcaf], xmm3  ; -> 02064BD0
004C6F21  shufps   xmm3, xmm3, 0x55
004C6F25  movzx    r9d, word ptr [rcx + r15]
004C6F2A  subss    xmm1, xmm3
004C6F2E  movss    dword ptr [rip + 0x1b9dcfa], xmm0  ; -> 02064C30
004C6F36  movss    xmm0, dword ptr [rip + 0x1b9dcda]  ; -> 02064C18
004C6F3E  addss    xmm0, xmm0
004C6F42  mov      word ptr [rip + 0x1b9de72], r9w  ; -> 02064DBC
004C6F4A  movss    dword ptr [rip + 0x1b9dcc2], xmm1  ; -> 02064C14
004C6F52  addss    xmm1, xmm1
004C6F56  movss    dword ptr [rip + 0x1b9dcda], xmm0  ; -> 02064C38
004C6F5E  movss    dword ptr [rip + 0x1b9dcce], xmm1  ; -> 02064C34
004C6F66  movzx    ecx, word ptr [rcx + r15 + 4]
004C6F6C  lea      eax, [rdx + 1]
004C6F6F  and      ax, cx
004C6F72  movss    xmm1, dword ptr [rip + 0x1b9dc4a]  ; -> 02064BC4
004C6F7A  mov      word ptr [rip + 0x1b9de43], ax  ; -> 02064DC4
004C6F81  lea      eax, [rdx + 2]
004C6F84  and      ax, cx
004C6F87  mov      word ptr [rip + 0x1b9de32], cx  ; -> 02064DC0
004C6F8E  mov      word ptr [rip + 0x1b9de33], ax  ; -> 02064DC8
004C6F95  add      dx, 0x14
004C6F99  movss    dword ptr [rip + 0x193b887], xmm1  ; -> 01E02828 [f32 1]
004C6FA1  lea      eax, [r8 + 0xa]
004C6FA5  shl      eax, 4
004C6FA8  movsxd   rcx, eax
004C6FAB  lea      eax, [r8 + 0xb]
004C6FAF  shl      eax, 4
004C6FB2  mov      word ptr [rip + 0x1b9de1f], dx  ; -> 02064DD8
004C6FB9  mov      dword ptr [rip + 0x1b9db39], 1  ; -> 02064AFC
004C6FC3  movups   xmm0, xmmword ptr [rcx + r15]
004C6FC8  movsxd   rcx, eax
004C6FCB  lea      eax, [r8 + 0xc]
004C6FCF  shl      eax, 4
004C6FD2  movups   xmmword ptr [rip + 0x1b9dd07], xmm0  ; -> 02064CE0
004C6FD9  movups   xmm0, xmmword ptr [rcx + r15]
004C6FDE  movsxd   rcx, eax
004C6FE1  lea      eax, [r8 + 0xd]
004C6FE5  shl      eax, 4
004C6FE8  movups   xmmword ptr [rip + 0x1b9dd01], xmm0  ; -> 02064CF0
004C6FEF  movups   xmm0, xmmword ptr [rcx + r15]
004C6FF4  movsxd   rcx, eax
004C6FF7  mov      eax, dword ptr [rip + 0x193b82b]  ; -> 01E02828 [f32 1]
004C6FFD  movups   xmmword ptr [rip + 0x1b9dcfc], xmm0  ; -> 02064D00
004C7004  movups   xmm0, xmmword ptr [rcx + r15]
004C7009  mov      ecx, eax
004C700B  shr      ecx, 0x12
004C700E  xor      ecx, eax
004C7010  and      eax, 0x3fffff
004C7015  or       eax, 0x1fc00000
004C701A  shr      ecx, 4
004C701D  add      eax, eax
004C701F  and      ecx, 1
004C7022  or       ecx, eax
004C7024  mov      eax, ecx
004C7026  shr      eax, 0x12
004C7029  xor      eax, ecx
004C702B  and      ecx, 0x3fffff
004C7031  or       ecx, 0x1fc00000
004C7037  shr      eax, 4
004C703A  add      ecx, ecx
004C703C  and      eax, 1
004C703F  or       eax, ecx
004C7041  mov      ecx, eax
004C7043  shr      ecx, 0x12
004C7046  xor      ecx, eax
004C7048  and      eax, 0x3fffff
004C704D  or       eax, 0x1fc00000
004C7052  shr      ecx, 4
004C7055  add      eax, eax
004C7057  and      ecx, 1
004C705A  or       ecx, eax
004C705C  mov      eax, ecx
004C705E  shr      eax, 0x12
004C7061  xor      eax, ecx
004C7063  and      ecx, 0x3fffff
004C7069  or       ecx, 0x1fc00000
004C706F  shr      eax, 4
004C7072  add      ecx, ecx
004C7074  and      eax, 1
004C7077  or       eax, ecx
004C7079  mov      ecx, eax
004C707B  shr      ecx, 0x12
004C707E  xor      ecx, eax
004C7080  and      eax, 0x3fffff
004C7085  or       eax, 0x1fc00000
004C708A  shr      ecx, 4
004C708D  add      eax, eax
004C708F  and      ecx, 1
004C7092  or       ecx, eax
004C7094  mov      dword ptr [rip + 0x193b78e], ecx  ; -> 01E02828 [f32 1]
004C709A  movss    xmm2, dword ptr [rip + 0x193b786]  ; -> 01E02828 [f32 1]
004C70A2  movups   xmmword ptr [rip + 0x1b9dc67], xmm0  ; -> 02064D10
004C70A9  mov      eax, ecx
004C70AB  movss    dword ptr [rip + 0x1b9dbcd], xmm2  ; -> 02064C80
004C70B3  shr      eax, 0x12
004C70B6  xor      eax, ecx
004C70B8  and      ecx, 0x3fffff
004C70BE  or       ecx, 0x1fc00000
004C70C4  shr      eax, 4
004C70C7  add      ecx, ecx
004C70C9  and      eax, 1
004C70CC  or       eax, ecx
004C70CE  mov      ecx, eax
004C70D0  shr      ecx, 0x12
004C70D3  xor      ecx, eax
004C70D5  and      eax, 0x3fffff
004C70DA  shr      ecx, 4
004C70DD  or       eax, 0x1fc00000
004C70E2  and      ecx, 1
004C70E5  add      eax, eax
004C70E7  or       ecx, eax
004C70E9  mov      eax, ecx
004C70EB  shr      eax, 0x12
004C70EE  xor      eax, ecx
004C70F0  and      ecx, 0x3fffff
004C70F6  or       ecx, 0x1fc00000
004C70FC  shr      eax, 4
004C70FF  add      ecx, ecx
004C7101  and      eax, 1
004C7104  or       eax, ecx
004C7106  mov      ecx, eax
004C7108  shr      ecx, 0x12
004C710B  xor      ecx, eax
004C710D  and      eax, 0x3fffff
004C7112  shr      ecx, 4
004C7115  or       eax, 0x1fc00000
004C711A  and      ecx, 1
004C711D  add      eax, eax
004C711F  or       ecx, eax
004C7121  mov      edx, ecx
004C7123  shr      edx, 0x12
004C7126  xor      edx, ecx
004C7128  and      ecx, 0x3fffff
004C712E  or       ecx, 0x1fc00000
004C7134  shr      edx, 4
004C7137  add      ecx, ecx
004C7139  and      edx, 1
004C713C  or       edx, ecx
004C713E  mov      eax, edx
004C7140  mov      dword ptr [rip + 0x193b6e2], edx  ; -> 01E02828 [f32 1]
004C7146  movss    xmm3, dword ptr [rip + 0x193b6da]  ; -> 01E02828 [f32 1]
004C714E  shr      eax, 0x12
004C7151  xor      eax, edx
004C7153  movss    dword ptr [rip + 0x1b9db29], xmm3  ; -> 02064C84
004C715B  shr      eax, 4
004C715E  and      edx, 0x3fffff
004C7164  and      eax, 1
004C7167  or       edx, 0x1fc00000
004C716D  add      edx, edx
004C716F  or       eax, edx
004C7171  mov      ecx, eax
004C7173  shr      ecx, 0x12
004C7176  xor      ecx, eax
004C7178  and      eax, 0x3fffff
004C717D  shr      ecx, 4
004C7180  or       eax, 0x1fc00000
004C7185  and      ecx, 1
004C7188  add      eax, eax
004C718A  or       ecx, eax
004C718C  mov      eax, ecx
004C718E  shr      eax, 0x12
004C7191  xor      eax, ecx
004C7193  and      ecx, 0x3fffff
004C7199  or       ecx, 0x1fc00000
004C719F  shr      eax, 4
004C71A2  add      ecx, ecx
004C71A4  and      eax, 1
004C71A7  or       eax, ecx
004C71A9  mov      ecx, eax
004C71AB  shr      ecx, 0x12
004C71AE  xor      ecx, eax
004C71B0  shr      ecx, 4
004C71B3  and      ecx, 1
004C71B6  and      eax, 0x3fffff
004C71BB  or       eax, 0x1fc00000
004C71C0  add      eax, eax
004C71C2  or       ecx, eax
004C71C4  mov      eax, ecx
004C71C6  shr      eax, 0x12
004C71C9  xor      eax, ecx
004C71CB  and      ecx, 0x3fffff
004C71D1  shr      eax, 4
004C71D4  or       ecx, 0x1fc00000
004C71DA  add      ecx, ecx
004C71DC  and      eax, 1
004C71DF  or       eax, ecx
004C71E1  mov      dword ptr [rip + 0x193b641], eax  ; -> 01E02828 [f32 1]
004C71E7  movss    xmm5, dword ptr [rip + 0x193b639]  ; -> 01E02828 [f32 1]
004C71EF  movss    dword ptr [rip + 0x1b9da91], xmm5  ; -> 02064C88
004C71F7  test     r9w, r9w
004C71FB  jle      0x4c7cde  ; -> 004C7CDE
004C7201  mov      qword ptr [rsp + 0xe8], rsi
004C7209  mov      qword ptr [rsp + 0xf0], rdi
004C7211  mov      qword ptr [rsp + 0xf8], r12
004C7219  mov      r12d, 0xe0
004C721F  movaps   xmmword ptr [rsp + 0xb0], xmm6
004C7227  movaps   xmmword ptr [rsp + 0xa0], xmm7
004C722F  movaps   xmmword ptr [rsp + 0x90], xmm8
004C7238  movsd    xmm8, qword ptr [rip + 0x1824b3f]  ; -> 01CEBD80 [u64 0x7FFFFFFFFFFFFFFF]
004C7241  movaps   xmmword ptr [rsp + 0x80], xmm9
004C724A  movaps   xmmword ptr [rsp + 0x70], xmm10
004C7250  movaps   xmmword ptr [rsp + 0x60], xmm11
004C7256  xorps    xmm11, xmm11
004C725A  movaps   xmmword ptr [rsp + 0x50], xmm12
004C7260  movaps   xmmword ptr [rsp + 0x40], xmm13
004C7266  movss    xmm13, dword ptr [rip + 0x1824939]  ; -> 01CEBBA8 [f32 1]
004C726F  movaps   xmmword ptr [rsp + 0x30], xmm14
004C7275  movaps   xmmword ptr [rsp + 0x20], xmm15
004C727B  mov      qword ptr [rsp + 0xe0], rbx
004C7283  nop      dword ptr [rax]
004C7287  nop      word ptr [rax + rax]
004C7290  subss    xmm2, dword ptr [rip + 0x1b9d968]  ; -> 02064C00
004C7298  subss    xmm3, dword ptr [rip + 0x1b9d964]  ; -> 02064C04
004C72A0  subss    xmm5, dword ptr [rip + 0x1b9d960]  ; -> 02064C08
004C72A8  dec      r9w
004C72AC  mov      word ptr [rip + 0x1b9db08], r9w  ; -> 02064DBC
004C72B4  movss    dword ptr [rip + 0x1b9d9c4], xmm2  ; -> 02064C80
004C72BC  movss    dword ptr [rip + 0x1b9d9c0], xmm3  ; -> 02064C84
004C72C4  movss    dword ptr [rip + 0x1b9d9bc], xmm5  ; -> 02064C88
004C72CC  call     0x22cc20  ; -> 0022CC20 fn
004C72D1  movzx    edi, word ptr [rip + 0x1b9d834]  ; -> 02064B0C
004C72D8  cmp      word ptr [rip + 0x1b9dae9], di  ; -> 02064DC8
004C72DF  je       0x4c72f6  ; -> 004C72F6
004C72E1  movss    xmm0, dword ptr [rip + 0x1b9d99b]  ; -> 02064C84
004C72E9  cvtps2pd xmm0, xmm0
004C72EC  andps    xmm0, xmm8
004C72F0  cvtpd2ps xmm6, xmm0
004C72F4  jmp      0x4c72fe  ; -> 004C72FE
004C72F6  movss    xmm6, dword ptr [rip + 0x1b9d986]  ; -> 02064C84
004C72FE  movss    xmm9, dword ptr [rip + 0x193b535]  ; -> 01E0283C [f32 1]
004C7307  movaps   xmm0, xmm6
004C730A  movss    xmm7, dword ptr [rip + 0x1b9d96e]  ; -> 02064C80
004C7312  movss    xmm10, dword ptr [rip + 0x1b9d96d]  ; -> 02064C88
004C731B  movaps   xmm2, xmm7
004C731E  mulss    xmm0, xmm6
004C7322  movaps   xmm1, xmm10
004C7326  mulss    xmm1, xmm10
004C732B  mulss    xmm0, xmm9
004C7330  mulss    xmm2, xmm7
004C7334  mulss    xmm1, xmm9
004C7339  mulss    xmm2, xmm9
004C733E  addss    xmm2, xmm0
004C7342  addss    xmm1, xmm2
004C7346  cvtps2pd xmm0, xmm1
004C7349  andps    xmm0, xmm8
004C734D  cvtpd2ps xmm0, xmm0
004C7351  call     0x861f14  ; -> 00861F14 fn
004C7356  ucomiss  xmm0, xmm11
004C735A  jp       0x4c7368  ; -> 004C7368
004C735C  jne      0x4c7368  ; -> 004C7368
004C735E  movss    xmm3, dword ptr [rip + 0x438ffa]  ; -> 00900360 [u32 0x7F7FFFFF]
004C7366  jmp      0x4c7370  ; -> 004C7370
004C7368  movaps   xmm3, xmm9
004C736C  divss    xmm3, xmm0
004C7370  mov      esi, dword ptr [rip + 0x1b9d786]  ; -> 02064AFC
004C7376  test     esi, esi
004C7378  je       0x4c741f  ; -> 004C741F
004C737E  mov      eax, dword ptr [rip + 0x193b4a4]  ; -> 01E02828 [f32 1]
004C7384  mov      ecx, eax
004C7386  shr      ecx, 0x12
004C7389  xor      ecx, eax
004C738B  and      eax, 0x3fffff
004C7390  or       eax, 0x1fc00000
004C7395  shr      ecx, 4
004C7398  add      eax, eax
004C739A  and      ecx, 1
004C739D  or       ecx, eax
004C739F  mov      eax, ecx
004C73A1  shr      eax, 0x12
004C73A4  xor      eax, ecx
004C73A6  and      ecx, 0x3fffff
004C73AC  shr      eax, 4
004C73AF  or       ecx, 0x1fc00000
004C73B5  and      eax, 1
004C73B8  add      ecx, ecx
004C73BA  or       eax, ecx
004C73BC  mov      ecx, eax
004C73BE  shr      ecx, 0x12
004C73C1  xor      ecx, eax
004C73C3  and      eax, 0x3fffff
004C73C8  or       eax, 0x1fc00000
004C73CD  shr      ecx, 4
004C73D0  add      eax, eax
004C73D2  and      ecx, 1
004C73D5  or       ecx, eax
004C73D7  mov      eax, ecx
004C73D9  shr      eax, 0x12
004C73DC  xor      eax, ecx
004C73DE  and      ecx, 0x3fffff
004C73E4  shr      eax, 4
004C73E7  or       ecx, 0x1fc00000
004C73ED  and      eax, 1
004C73F0  add      ecx, ecx
004C73F2  or       eax, ecx
004C73F4  mov      ebx, eax
004C73F6  shr      ebx, 0x12
004C73F9  xor      ebx, eax
004C73FB  and      eax, 0x3fffff
004C7400  or       eax, 0x1fc00000
004C7405  shr      ebx, 4
004C7408  add      eax, eax
004C740A  and      ebx, 1
004C740D  or       ebx, eax
004C740F  mov      dword ptr [rip + 0x193b413], ebx  ; -> 01E02828 [f32 1]
004C7415  movss    xmm0, dword ptr [rip + 0x193b40b]  ; -> 01E02828 [f32 1]
004C741D  jmp      0x4c7429  ; -> 004C7429
004C741F  mov      ebx, dword ptr [rip + 0x193b403]  ; -> 01E02828 [f32 1]
004C7425  movaps   xmm0, xmm13
004C7429  subss    xmm0, xmm9
004C742E  test     esi, esi
004C7430  je       0x4c7453  ; -> 004C7453
004C7432  mov      eax, ebx
004C7434  shr      ebx, 0x12
004C7437  xor      ebx, eax
004C7439  and      eax, 0x3fffff
004C743E  or       eax, 0x1fc00000
004C7443  shr      ebx, 4
004C7446  add      eax, eax
004C7448  and      ebx, 1
004C744B  or       ebx, eax
004C744D  mov      dword ptr [rip + 0x193b3d5], ebx  ; -> 01E02828 [f32 1]
004C7453  movss    xmm2, dword ptr [rip + 0x1b9d771]  ; -> 02064BCC
004C745B  mulss    xmm2, xmm0
004C745F  addss    xmm2, dword ptr [rip + 0x1b9d761]  ; -> 02064BC8
004C7467  test     esi, esi
004C7469  je       0x4c74ef  ; -> 004C74EF
004C746F  mov      eax, ebx
004C7471  shr      eax, 0x12
004C7474  xor      eax, ebx
004C7476  and      ebx, 0x3fffff
004C747C  shr      eax, 4
004C747F  or       ebx, 0x1fc00000
004C7485  and      eax, 1
004C7488  add      ebx, ebx
004C748A  or       eax, ebx
004C748C  mov      ecx, eax
004C748E  shr      ecx, 0x12
004C7491  xor      ecx, eax
004C7493  and      eax, 0x3fffff
004C7498  or       eax, 0x1fc00000
004C749D  shr      ecx, 4
004C74A0  add      eax, eax
004C74A2  and      ecx, 1
004C74A5  or       ecx, eax
004C74A7  mov      eax, ecx
004C74A9  shr      eax, 0x12
004C74AC  xor      eax, ecx
004C74AE  and      ecx, 0x3fffff
004C74B4  shr      eax, 4
004C74B7  or       ecx, 0x1fc00000
004C74BD  and      eax, 1
004C74C0  add      ecx, ecx
004C74C2  or       eax, ecx
004C74C4  mov      ebx, eax
004C74C6  shr      ebx, 0x12
004C74C9  xor      ebx, eax
004C74CB  and      eax, 0x3fffff
004C74D0  or       eax, 0x1fc00000
004C74D5  shr      ebx, 4
004C74D8  add      eax, eax
004C74DA  and      ebx, 1
004C74DD  or       ebx, eax
004C74DF  mov      dword ptr [rip + 0x193b343], ebx  ; -> 01E02828 [f32 1]
004C74E5  movss    xmm1, dword ptr [rip + 0x193b33b]  ; -> 01E02828 [f32 1]
004C74ED  jmp      0x4c74f3  ; -> 004C74F3
004C74EF  movaps   xmm1, xmm13
004C74F3  cmp      word ptr [rip + 0x1b9d8ca], di  ; -> 02064DC4
004C74FA  subss    xmm1, xmm9
004C74FF  movss    xmm11, dword ptr [rip + 0x1b9d6b8]  ; -> 02064BC0
004C7508  movaps   xmm14, xmm2
004C750C  movss    xmm0, dword ptr [rip + 0x1b9d6c4]  ; -> 02064BD8
004C7514  movaps   xmm12, xmm11
004C7518  mulss    xmm7, xmm3
004C751C  mulss    xmm1, dword ptr [rip + 0x1b9d6b8]  ; -> 02064BDC
004C7524  mulss    xmm10, xmm3
004C7529  movaps   xmm8, xmm7
004C752D  addss    xmm0, xmm1
004C7531  movss    dword ptr [rip + 0x1b9d7a3], xmm1  ; -> 02064CDC
004C7539  movaps   xmm1, xmm3
004C753C  mulss    xmm8, xmm2
004C7541  mulss    xmm1, xmm6
004C7545  movaps   xmm15, xmm10
004C7549  movaps   xmm6, xmm2
004C754C  mulss    xmm15, xmm2
004C7551  mulss    xmm7, xmm0
004C7555  mulss    xmm10, xmm0
004C755A  mulss    xmm14, xmm1
004C755F  mulss    xmm1, xmm0
004C7563  movss    dword ptr [rip + 0x1b9d76d], xmm0  ; -> 02064CD8
004C756B  movss    xmm0, dword ptr [rip + 0x1b9d66d]  ; -> 02064BE0
004C7573  mulss    xmm7, xmm0
004C7577  mulss    xmm10, xmm0
004C757C  mulss    xmm1, xmm0
004C7580  mulss    xmm6, xmm9
004C7585  movss    dword ptr [rip + 0x1b9d703], xmm7  ; -> 02064C90
004C758D  movss    dword ptr [rip + 0x1b9d702], xmm10  ; -> 02064C98
004C7596  movss    dword ptr [rip + 0x1b9d6f6], xmm1  ; -> 02064C94
004C759E  mulss    xmm12, xmm1
004C75A3  movss    dword ptr [rip + 0x1b9d6f1], xmm6  ; -> 02064C9C
004C75AB  mulss    xmm7, xmm11
004C75B0  mulss    xmm10, xmm11
004C75B5  je       0x4c7655  ; -> 004C7655
004C75BB  movaps   xmm1, xmm10
004C75BF  movaps   xmm0, xmm12
004C75C3  mulss    xmm0, xmm12
004C75C8  movaps   xmm2, xmm7
004C75CB  mulss    xmm1, xmm10
004C75D0  movss    dword ptr [rip + 0x1b9d6fc], xmm0  ; -> 02064CD4
004C75D8  mulss    xmm0, xmm9
004C75DD  mulss    xmm2, xmm7
004C75E1  movss    dword ptr [rip + 0x1b9d6ef], xmm1  ; -> 02064CD8
004C75E9  mulss    xmm1, xmm9
004C75EE  mulss    xmm2, xmm9
004C75F3  addss    xmm2, xmm0
004C75F7  addss    xmm1, xmm2
004C75FB  cvtps2pd xmm0, xmm1
004C75FE  movss    dword ptr [rip + 0x1b9d6d6], xmm1  ; -> 02064CDC
004C7606  andps    xmm0, xmmword ptr [rip + 0x1824773]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
004C760D  cvtpd2ps xmm0, xmm0
004C7611  call     0x861f14  ; -> 00861F14 fn
004C7616  xorps    xmm1, xmm1
004C7619  ucomiss  xmm0, xmm1
004C761C  jp       0x4c762a  ; -> 004C762A
004C761E  jne      0x4c762a  ; -> 004C762A
004C7620  movss    xmm6, dword ptr [rip + 0x438d38]  ; -> 00900360 [u32 0x7F7FFFFF]
004C7628  jmp      0x4c762e  ; -> 004C762E
004C762A  divss    xmm6, xmm0
004C762E  movss    xmm0, dword ptr [rip + 0x193b1fa]  ; -> 01E02830 [u32 0x00000000]
004C7636  addss    xmm0, xmm6
004C763A  minss    xmm0, xmm9
004C763F  movss    dword ptr [rip + 0x1b9d689], xmm0  ; -> 02064CD0
004C7647  mulss    xmm7, xmm0
004C764B  mulss    xmm12, xmm0
004C7650  mulss    xmm10, xmm0
004C7655  movss    xmm0, dword ptr [rip + 0x1b9d5d3]  ; -> 02064C30
004C765D  addss    xmm7, xmm8
004C7662  movss    xmm8, dword ptr [rip + 0x1b9d5cd]  ; -> 02064C38
004C766B  addss    xmm12, xmm14
004C7670  mulss    xmm11, xmm11
004C7675  addss    xmm10, xmm15
004C767A  mulss    xmm0, xmm11
004C767F  movaps   xmm6, xmm11
004C7683  mulss    xmm6, dword ptr [rip + 0x1b9d5a9]  ; -> 02064C34
004C768B  movss    dword ptr [rip + 0x1b9d5dd], xmm0  ; -> 02064C70
004C7693  addss    xmm0, xmm7
004C7697  mulss    xmm8, xmm11
004C769C  movaps   xmm7, xmm9
004C76A0  mulss    xmm7, xmm9
004C76A5  movss    dword ptr [rip + 0x1b9d5c7], xmm6  ; -> 02064C74
004C76AD  addss    xmm6, xmm12
004C76B2  addss    xmm0, dword ptr [rip + 0x1b9d536]  ; -> 02064BF0
004C76BA  movss    dword ptr [rip + 0x1b9d5b5], xmm8  ; -> 02064C78
004C76C3  addss    xmm8, xmm10
004C76C8  movss    dword ptr [rip + 0x1b9d58f], xmm11  ; -> 02064C60
004C76D1  xorps    xmm11, xmm11
004C76D5  movss    dword ptr [rip + 0x1b9d5df], xmm7  ; -> 02064CBC
004C76DD  addss    xmm6, dword ptr [rip + 0x1b9d50f]  ; -> 02064BF4
004C76E5  movaps   xmm5, xmm0
004C76E8  movss    dword ptr [rip + 0x1b9d5c0], xmm0  ; -> 02064CB0
004C76F0  addss    xmm8, dword ptr [rip + 0x1b9d4ff]  ; -> 02064BF8
004C76F9  movups   xmm0, xmmword ptr [rip + 0x1b9d5e0]  ; -> 02064CE0
004C7700  shufps   xmm5, xmm5, 0
004C7704  movaps   xmm1, xmm6
004C7707  mulss    xmm1, dword ptr [rip + 0x1b9d5e9]  ; -> 02064CF8
004C770F  mulps    xmm5, xmm0
004C7712  movaps   xmm0, xmm6
004C7715  mulss    xmm0, dword ptr [rip + 0x1b9d5d3]  ; -> 02064CF0
004C771D  movss    dword ptr [rip + 0x1b9d58f], xmm6  ; -> 02064CB4
004C7725  movups   xmmword ptr [rip + 0x1b9d3f4], xmm5  ; -> 02064B20
004C772C  movss    xmm2, dword ptr [rip + 0x1b9d3f0]  ; -> 02064B24
004C7734  addss    xmm5, xmm0
004C7738  movss    xmm3, dword ptr [rip + 0x1b9d3e8]  ; -> 02064B28
004C7740  movaps   xmm0, xmm6
004C7743  mulss    xmm0, dword ptr [rip + 0x1b9d5a9]  ; -> 02064CF4
004C774B  addss    xmm3, xmm1
004C774F  movss    xmm4, dword ptr [rip + 0x1b9d3d5]  ; -> 02064B2C
004C7757  movaps   xmm1, xmm8
004C775B  mulss    xmm1, dword ptr [rip + 0x1b9d5a1]  ; -> 02064D04
004C7763  mulss    xmm6, dword ptr [rip + 0x1b9d591]  ; -> 02064CFC
004C776B  addss    xmm2, xmm0
004C776F  movaps   xmm0, xmm8
004C7773  movss    dword ptr [rip + 0x1b9d53c], xmm8  ; -> 02064CB8
004C777C  mulss    xmm0, dword ptr [rip + 0x1b9d57c]  ; -> 02064D00
004C7784  addss    xmm2, xmm1
004C7788  movss    xmm1, dword ptr [rip + 0x1b9d584]  ; -> 02064D14
004C7790  mulss    xmm1, xmm7
004C7794  addss    xmm4, xmm6
004C7798  addss    xmm5, xmm0
004C779C  movaps   xmm0, xmm8
004C77A0  mulss    xmm0, dword ptr [rip + 0x1b9d560]  ; -> 02064D08
004C77A8  mulss    xmm8, dword ptr [rip + 0x1b9d55b]  ; -> 02064D0C
004C77B1  addss    xmm1, xmm2
004C77B5  addss    xmm3, xmm0
004C77B9  movss    dword ptr [rip + 0x1b9d35f], xmm5  ; -> 02064B20
004C77C1  movss    xmm0, dword ptr [rip + 0x1b9d547]  ; -> 02064D10
004C77C9  mulss    xmm0, xmm7
004C77CD  addss    xmm4, xmm8
004C77D2  movss    dword ptr [rip + 0x1b9d4ea], xmm1  ; -> 02064CC4
004C77DA  movss    xmm1, dword ptr [rip + 0x1b9d53a]  ; -> 02064D1C
004C77E2  addss    xmm0, xmm5
004C77E6  mulss    xmm1, xmm7
004C77EA  movss    dword ptr [rip + 0x1b9d332], xmm2  ; -> 02064B24
004C77F2  movss    dword ptr [rip + 0x1b9d32e], xmm3  ; -> 02064B28
004C77FA  addss    xmm1, xmm4
004C77FE  movss    dword ptr [rip + 0x1b9d326], xmm4  ; -> 02064B2C
004C7806  movss    dword ptr [rip + 0x1b9d4b2], xmm0  ; -> 02064CC0
004C780E  movss    xmm0, dword ptr [rip + 0x1b9d502]  ; -> 02064D18
004C7816  mulss    xmm0, xmm7
004C781A  ucomiss  xmm1, xmm11
004C781E  addss    xmm0, xmm3
004C7822  movss    dword ptr [rip + 0x1b9d4a2], xmm1  ; -> 02064CCC
004C782A  movss    dword ptr [rip + 0x1b9d496], xmm0  ; -> 02064CC8
004C7832  jp       0x4c7841  ; -> 004C7841
004C7834  jne      0x4c7841  ; -> 004C7841
004C7836  movss    xmm9, dword ptr [rip + 0x438b21]  ; -> 00900360 [u32 0x7F7FFFFF]
004C783F  jmp      0x4c7846  ; -> 004C7846
004C7841  divss    xmm9, xmm1
004C7846  movss    dword ptr [rip + 0x1b9d2b1], xmm9  ; -> 02064B00
004C784F  test     esi, esi
004C7851  je       0x4c7a3a  ; -> 004C7A3A
004C7857  mov      eax, ebx
004C7859  shr      eax, 0x12
004C785C  xor      eax, ebx
004C785E  and      ebx, 0x3fffff
004C7864  shr      eax, 4
004C7867  or       ebx, 0x1fc00000
004C786D  and      eax, 1
004C7870  add      ebx, ebx
004C7872  or       eax, ebx
004C7874  mov      ecx, eax
004C7876  shr      ecx, 0x12
004C7879  xor      ecx, eax
004C787B  and      eax, 0x3fffff
004C7880  shr      ecx, 4
004C7883  or       eax, 0x1fc00000
004C7888  and      ecx, 1
004C788B  add      eax, eax
004C788D  or       ecx, eax
004C788F  mov      eax, ecx
004C7891  shr      eax, 0x12
004C7894  xor      eax, ecx
004C7896  and      ecx, 0x3fffff
004C789C  or       ecx, 0x1fc00000
004C78A2  shr      eax, 4
004C78A5  add      ecx, ecx
004C78A7  and      eax, 1
004C78AA  or       eax, ecx
004C78AC  mov      ecx, eax
004C78AE  shr      ecx, 0x12
004C78B1  xor      ecx, eax
004C78B3  and      eax, 0x3fffff
004C78B8  shr      ecx, 4
004C78BB  or       eax, 0x1fc00000
004C78C0  and      ecx, 1
004C78C3  add      eax, eax
004C78C5  or       ecx, eax
004C78C7  mov      edx, ecx
004C78C9  shr      edx, 0x12
004C78CC  xor      edx, ecx
004C78CE  and      ecx, 0x3fffff
004C78D4  or       ecx, 0x1fc00000
004C78DA  shr      edx, 4
004C78DD  add      ecx, ecx
004C78DF  and      edx, 1
004C78E2  or       edx, ecx
004C78E4  mov      eax, edx
004C78E6  mov      dword ptr [rip + 0x193af3c], edx  ; -> 01E02828 [f32 1]
004C78EC  movss    xmm2, dword ptr [rip + 0x193af34]  ; -> 01E02828 [f32 1]
004C78F4  shr      eax, 0x12
004C78F7  xor      eax, edx
004C78F9  movss    dword ptr [rip + 0x1b9d37f], xmm2  ; -> 02064C80
004C7901  shr      eax, 4
004C7904  and      edx, 0x3fffff
004C790A  and      eax, 1
004C790D  or       edx, 0x1fc00000
004C7913  add      edx, edx
004C7915  or       eax, edx
004C7917  mov      ecx, eax
004C7919  shr      ecx, 0x12
004C791C  xor      ecx, eax
004C791E  and      eax, 0x3fffff
004C7923  shr      ecx, 4
004C7926  or       eax, 0x1fc00000
004C792B  and      ecx, 1
004C792E  add      eax, eax
004C7930  or       ecx, eax
004C7932  mov      eax, ecx
004C7934  shr      eax, 0x12
004C7937  xor      eax, ecx
004C7939  and      ecx, 0x3fffff
004C793F  or       ecx, 0x1fc00000
004C7945  shr      eax, 4
004C7948  add      ecx, ecx
004C794A  and      eax, 1
004C794D  or       eax, ecx
004C794F  mov      ecx, eax
004C7951  shr      ecx, 0x12
004C7954  xor      ecx, eax
004C7956  shr      ecx, 4
004C7959  and      ecx, 1
004C795C  and      eax, 0x3fffff
004C7961  or       eax, 0x1fc00000
004C7966  add      eax, eax
004C7968  or       ecx, eax
004C796A  mov      edx, ecx
004C796C  shr      edx, 0x12
004C796F  xor      edx, ecx
004C7971  and      ecx, 0x3fffff
004C7977  or       ecx, 0x1fc00000
004C797D  shr      edx, 4
004C7980  add      ecx, ecx
004C7982  and      edx, 1
004C7985  or       edx, ecx
004C7987  mov      dword ptr [rip + 0x193ae9b], edx  ; -> 01E02828 [f32 1]
004C798D  mov      eax, edx
004C798F  movss    xmm3, dword ptr [rip + 0x193ae91]  ; -> 01E02828 [f32 1]
004C7997  shr      eax, 0x12
004C799A  xor      eax, edx
004C799C  movss    dword ptr [rip + 0x1b9d2e0], xmm3  ; -> 02064C84
004C79A4  shr      eax, 4
004C79A7  and      edx, 0x3fffff
004C79AD  and      eax, 1
004C79B0  or       edx, 0x1fc00000
004C79B6  add      edx, edx
004C79B8  or       eax, edx
004C79BA  mov      ecx, eax
004C79BC  shr      ecx, 0x12
004C79BF  xor      ecx, eax
004C79C1  and      eax, 0x3fffff
004C79C6  or       eax, 0x1fc00000
004C79CB  shr      ecx, 4
004C79CE  add      eax, eax
004C79D0  and      ecx, 1
004C79D3  or       ecx, eax
004C79D5  mov      eax, ecx
004C79D7  shr      eax, 0x12
004C79DA  xor      eax, ecx
004C79DC  and      ecx, 0x3fffff
004C79E2  or       ecx, 0x1fc00000
004C79E8  shr      eax, 4
004C79EB  add      ecx, ecx
004C79ED  and      eax, 1
004C79F0  or       eax, ecx
004C79F2  mov      ecx, eax
004C79F4  shr      ecx, 0x12
004C79F7  xor      ecx, eax
004C79F9  and      eax, 0x3fffff
004C79FE  or       eax, 0x1fc00000
004C7A03  shr      ecx, 4
004C7A06  add      eax, eax
004C7A08  and      ecx, 1
004C7A0B  or       ecx, eax
004C7A0D  mov      eax, ecx
004C7A0F  shr      eax, 0x12
004C7A12  xor      eax, ecx
004C7A14  and      ecx, 0x3fffff
004C7A1A  or       ecx, 0x1fc00000
004C7A20  shr      eax, 4
004C7A23  add      ecx, ecx
004C7A25  and      eax, 1
004C7A28  or       eax, ecx
004C7A2A  mov      dword ptr [rip + 0x193adf8], eax  ; -> 01E02828 [f32 1]
004C7A30  movss    xmm5, dword ptr [rip + 0x193adf0]  ; -> 01E02828 [f32 1]
004C7A38  jmp      0x4c7a56  ; -> 004C7A56
004C7A3A  movaps   xmm2, xmm13
004C7A3E  movaps   xmm3, xmm13
004C7A42  movss    dword ptr [rip + 0x1b9d236], xmm2  ; -> 02064C80
004C7A4A  movaps   xmm5, xmm13
004C7A4E  movss    dword ptr [rip + 0x1b9d22e], xmm3  ; -> 02064C84
004C7A56  movups   xmm1, xmmword ptr [rip + 0x1b9d263]  ; -> 02064CC0
004C7A5D  movss    xmm8, dword ptr [rip + 0x1b9d0ca]  ; -> 02064B30
004C7A66  movaps   xmm0, xmm9
004C7A6A  shufps   xmm0, xmm0, 0
004C7A6E  mulps    xmm1, xmm0
004C7A71  movss    dword ptr [rip + 0x1b9d20f], xmm5  ; -> 02064C88
004C7A79  ucomiss  xmm8, xmm1
004C7A7D  jp       0x4c7a89  ; -> 004C7A89
004C7A7F  jne      0x4c7a89  ; -> 004C7A89
004C7A81  mov      r9d, 1
004C7A87  jmp      0x4c7a8c  ; -> 004C7A8C
004C7A89  xor      r9d, r9d
004C7A8C  movss    xmm7, dword ptr [rip + 0x1b9d0a0]  ; -> 02064B34
004C7A94  movaps   xmm0, xmm1
004C7A97  shufps   xmm0, xmm1, 0x55
004C7A9B  ucomiss  xmm7, xmm0
004C7A9E  jp       0x4c7aaa  ; -> 004C7AAA
004C7AA0  jne      0x4c7aaa  ; -> 004C7AAA
004C7AA2  mov      r8d, 1
004C7AA8  jmp      0x4c7aad  ; -> 004C7AAD
004C7AAA  xor      r8d, r8d
004C7AAD  movss    xmm6, dword ptr [rip + 0x1b9d083]  ; -> 02064B38
004C7AB5  movaps   xmm4, xmm1
004C7AB8  shufps   xmm4, xmm1, 0xaa
004C7ABC  ucomiss  xmm6, xmm4
004C7ABF  jp       0x4c7aca  ; -> 004C7ACA
004C7AC1  jne      0x4c7aca  ; -> 004C7ACA
004C7AC3  mov      edx, 1
004C7AC8  jmp      0x4c7acc  ; -> 004C7ACC
004C7ACA  xor      edx, edx
004C7ACC  xor      ecx, ecx
004C7ACE  comiss   xmm1, xmm8
004C7AD2  seta     cl
004C7AD5  xor      eax, eax
004C7AD7  add      cx, cx
004C7ADA  comiss   xmm0, xmm7
004C7ADD  seta     al
004C7AE0  add      cx, ax
004C7AE3  xor      eax, eax
004C7AE5  add      cx, cx
004C7AE8  comiss   xmm4, xmm6
004C7AEB  movss    xmm6, dword ptr [rip + 0x193ad3d]  ; -> 01E02830 [u32 0x00000000]
004C7AF3  seta     al
004C7AF6  add      cx, ax
004C7AF9  shl      cx, 2
004C7AFD  add      cx, r9w
004C7B01  add      cx, cx
004C7B04  add      cx, r8w
004C7B08  add      cx, cx
004C7B0B  add      cx, dx
004C7B0E  add      cx, cx
004C7B11  ucomiss  xmm1, xmm6
004C7B14  jp       0x4c7b20  ; -> 004C7B20
004C7B16  jne      0x4c7b20  ; -> 004C7B20
004C7B18  mov      r11d, 1
004C7B1E  jmp      0x4c7b23  ; -> 004C7B23
004C7B20  xor      r11d, r11d
004C7B23  movss    xmm8, dword ptr [rip + 0x193ad08]  ; -> 01E02834 [u32 0x00000000]
004C7B2C  ucomiss  xmm0, xmm8
004C7B30  jp       0x4c7b3c  ; -> 004C7B3C
004C7B32  jne      0x4c7b3c  ; -> 004C7B3C
004C7B34  mov      r10d, 1
004C7B3A  jmp      0x4c7b3f  ; -> 004C7B3F
004C7B3C  xor      r10d, r10d
004C7B3F  movss    xmm7, dword ptr [rip + 0x193acf1]  ; -> 01E02838 [u32 0x00000000]
004C7B47  ucomiss  xmm4, xmm7
004C7B4A  jp       0x4c7b56  ; -> 004C7B56
004C7B4C  jne      0x4c7b56  ; -> 004C7B56
004C7B4E  mov      r9d, 1
004C7B54  jmp      0x4c7b59  ; -> 004C7B59
004C7B56  xor      r9d, r9d
004C7B59  lea      edx, [r12 + rdi]
004C7B5D  movzx    r8d, dx
004C7B61  and      r8w, cx
004C7B65  xor      ecx, ecx
004C7B67  comiss   xmm6, xmm1
004C7B6A  seta     cl
004C7B6D  xor      eax, eax
004C7B6F  add      cx, cx
004C7B72  comiss   xmm8, xmm0
004C7B76  movaps   xmm0, xmmword ptr [rip + 0x44d873]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004C7B7D  mulps    xmm0, xmm1
004C7B80  seta     al
004C7B83  add      cx, ax
004C7B86  xor      eax, eax
004C7B88  add      cx, cx
004C7B8B  comiss   xmm7, xmm4
004C7B8E  cvttps2dq xmm4, xmm0
004C7B92  seta     al
004C7B95  add      cx, ax
004C7B98  shl      cx, 2
004C7B9C  add      cx, r11w
004C7BA0  add      cx, cx
004C7BA3  add      cx, r10w
004C7BA7  add      cx, cx
004C7BAA  add      cx, r9w
004C7BAE  add      cx, cx
004C7BB1  and      dx, cx
004C7BB4  movsx    eax, dx
004C7BB7  add      r8w, ax
004C7BBB  mov      word ptr [rip + 0x1b9d226], dx  ; -> 02064DE8
004C7BC2  mov      word ptr [rip + 0x1b9d21a], r8w  ; -> 02064DE4
004C7BCA  movups   xmmword ptr [rip + 0x1b9d0ef], xmm4  ; -> 02064CC0
004C7BD1  cmp      r8w, di
004C7BD5  jne      0x4c7c0f  ; -> 004C7C0F
004C7BD7  movsx    edx, word ptr [rip + 0x1b9d1d6]  ; -> 02064DB4
004C7BDE  movups   xmm0, xmmword ptr [rip + 0x1b9d03b]  ; -> 02064C20
004C7BE5  inc      word ptr [rip + 0x1b9d1cc]  ; -> 02064DB8
004C7BEC  mov      ecx, edx
004C7BEE  shl      ecx, 4
004C7BF1  movsxd   rax, ecx
004C7BF4  add      dx, 2
004C7BF8  mov      word ptr [rip + 0x1b9d1b5], dx  ; -> 02064DB4
004C7BFF  movups   xmmword ptr [rax + r15], xmm0
004C7C04  lea      eax, [rcx + 0x10]
004C7C07  movsxd   rcx, eax
004C7C0A  movups   xmmword ptr [rcx + r15], xmm4
004C7C0F  movzx    eax, word ptr [rip + 0x1b9d1c2]  ; -> 02064DD8
004C7C16  cmp      word ptr [rip + 0x1b9d19b], ax  ; -> 02064DB8
004C7C1D  jne      0x4c7c49  ; -> 004C7C49
004C7C1F  mov      rdx, rbp
004C7C22  mov      rcx, r14
004C7C25  call     0x4c4c40  ; -> 004C4C40 fn
004C7C2A  movss    xmm5, dword ptr [rip + 0x1b9d056]  ; -> 02064C88
004C7C32  movss    xmm3, dword ptr [rip + 0x1b9d04a]  ; -> 02064C84
004C7C3A  movss    xmm2, dword ptr [rip + 0x1b9d03e]  ; -> 02064C80
004C7C42  movzx    edi, word ptr [rip + 0x1b9cec3]  ; -> 02064B0C
004C7C49  movzx    r9d, word ptr [rip + 0x1b9d16b]  ; -> 02064DBC
004C7C51  movsd    xmm8, qword ptr [rip + 0x1824126]  ; -> 01CEBD80 [u64 0x7FFFFFFFFFFFFFFF]
004C7C5A  test     r9w, r9w
004C7C5E  jg       0x4c7290  ; -> 004C7290
004C7C64  movaps   xmm15, xmmword ptr [rsp + 0x20]
004C7C6A  movaps   xmm14, xmmword ptr [rsp + 0x30]
004C7C70  movaps   xmm13, xmmword ptr [rsp + 0x40]
004C7C76  movaps   xmm12, xmmword ptr [rsp + 0x50]
004C7C7C  movaps   xmm11, xmmword ptr [rsp + 0x60]
004C7C82  movaps   xmm10, xmmword ptr [rsp + 0x70]
004C7C88  movaps   xmm9, xmmword ptr [rsp + 0x80]
004C7C91  movaps   xmm8, xmmword ptr [rsp + 0x90]
004C7C9A  movaps   xmm7, xmmword ptr [rsp + 0xa0]
004C7CA2  movaps   xmm6, xmmword ptr [rsp + 0xb0]
004C7CAA  mov      r12, qword ptr [rsp + 0xf8]
004C7CB2  mov      rsi, qword ptr [rsp + 0xe8]
004C7CBA  mov      rbx, qword ptr [rsp + 0xe0]
004C7CC2  cmp      word ptr [rip + 0x1b9d0ef], di  ; -> 02064DB8
004C7CC9  mov      rdi, qword ptr [rsp + 0xf0]
004C7CD1  je       0x4c7cde  ; -> 004C7CDE
004C7CD3  mov      rdx, rbp
004C7CD6  mov      rcx, r14
004C7CD9  call     0x4c4c40  ; -> 004C4C40 fn
004C7CDE  add      rsp, 0xc0
004C7CE5  pop      r15
004C7CE7  pop      r14
004C7CE9  pop      rbp
004C7CEA  ret      
```

## 004C8320 (28422 B, extent 004C8320-004CF226)

Page context: "onstant fill - a module record's init.  Interior anchor '004EC973' (function '004EC960').  '004C8080' (509 B) is a battery constructor '0037E0F0' calls: '00861EC0' zeroes first, '008631E0' registers '004C8320', '008631D0(0x27)' fills '+0x10', then '+0xC' = 0x02000000, '+0x18' = 0x1000404, '+0x1C' = 0x6C260000 - the largest field count of the family.  Interior anchor '004C8097' (function '004C8080').  '004DCA00' (507 B) is a battery cons"

```
004C8320  mov      r11, rsp
004C8323  push     rbx
004C8324  push     rbp
004C8325  push     rsi
004C8326  push     rdi
004C8327  push     r14
004C8329  push     r15
004C832B  sub      rsp, 0x288
004C8332  movaps   xmmword ptr [r11 - 0x48], xmm6
004C8337  movaps   xmmword ptr [r11 - 0x58], xmm7
004C833C  movaps   xmmword ptr [r11 - 0x68], xmm8
004C8341  movaps   xmmword ptr [r11 - 0x78], xmm9
004C8346  movaps   xmmword ptr [r11 - 0x88], xmm10
004C834E  movaps   xmmword ptr [r11 - 0x98], xmm11
004C8356  movaps   xmmword ptr [r11 - 0xa8], xmm12
004C835E  movaps   xmmword ptr [r11 - 0xb8], xmm13
004C8366  movaps   xmmword ptr [r11 - 0xc8], xmm14
004C836E  movaps   xmmword ptr [r11 - 0xd8], xmm15
004C8376  mov      rax, qword ptr [rip + 0x1a7c4b3]  ; -> 01F44830 [u64 0x00002B992DDFA232]
004C837D  xor      rax, rsp
004C8380  mov      qword ptr [rsp + 0x1d0], rax
004C8388  mov      r14, rdx
004C838B  mov      rbp, rcx
004C838E  test     r8d, r8d
004C8391  je       0x4cf0eb  ; -> 004CF0EB
004C8397  cmp      r8d, 1
004C839B  jne      0x4cb6dd  ; -> 004CB6DD
004C83A1  mov      qword ptr [r11 + 0x18], r12
004C83A5  mov      qword ptr [r11 - 0x38], r13
004C83A9  movsx    r13d, word ptr [rip + 0x1b9c75b]  ; -> 02064B0C
004C83B1  lea      rbx, [rip + 0x1b9ca78]  ; -> 02064E30
004C83B8  lea      eax, [r13 + 0x29]
004C83BC  shl      eax, 4
004C83BF  movsxd   r10, eax
004C83C2  lea      eax, [r13 + 7]
004C83C6  shl      eax, 4
004C83C9  movsxd   rcx, eax
004C83CC  lea      eax, [r13 + 8]
004C83D0  shl      eax, 4
004C83D3  movups   xmm7, xmmword ptr [r10 + rbx]
004C83D8  movups   xmm1, xmmword ptr [rcx + rbx]
004C83DC  movsxd   rcx, eax
004C83DF  lea      eax, [r13 + 9]
004C83E3  shl      eax, 4
004C83E6  movaps   xmm6, xmm7
004C83E9  movups   xmmword ptr [rip + 0x1b9c770], xmm1  ; -> 02064B60
004C83F0  movups   xmm2, xmmword ptr [rcx + rbx]
004C83F4  movsxd   rcx, eax
004C83F7  lea      eax, [r13 + 0xa]
004C83FB  shl      eax, 4
004C83FE  shufps   xmm6, xmm6, 0
004C8402  movaps   xmm10, xmm2
004C8406  mulps    xmm6, xmm1
004C8409  movaps   xmm9, xmm2
004C840D  movups   xmm11, xmmword ptr [rcx + rbx]
004C8412  movsxd   rcx, eax
004C8415  lea      eax, [r13 + 0x2a]
004C8419  shufps   xmm10, xmm2, 0xaa
004C841E  movaps   xmm1, xmm7
004C8421  shufps   xmm1, xmm7, 0x55
004C8425  movaps   xmm8, xmm11
004C8429  movups   xmmword ptr [rip + 0x1b9c6f0], xmm6  ; -> 02064B20
004C8430  shl      eax, 4
004C8433  movups   xmm0, xmmword ptr [rcx + rbx]
004C8437  movsxd   r9, eax
004C843A  lea      eax, [r13 + 0x2b]
004C843E  movss    xmm3, dword ptr [rip + 0x1b9c6de]  ; -> 02064B24
004C8446  movss    xmm4, dword ptr [rip + 0x1b9c6da]  ; -> 02064B28
004C844E  movss    xmm5, dword ptr [rip + 0x1b9c6d6]  ; -> 02064B2C
004C8456  movups   xmmword ptr [rsp + 0x110], xmm0
004C845E  shl      eax, 4
004C8461  movups   xmmword ptr [rip + 0x1b9c728], xmm0  ; -> 02064B90
004C8468  movsxd   r8, eax
004C846B  movups   xmm0, xmmword ptr [r9 + rbx]
004C8470  shufps   xmm9, xmm2, 0xff
004C8475  movups   xmmword ptr [rsp + 0x120], xmm0
004C847D  movups   xmmword ptr [rip + 0x1b9c74c], xmm0  ; -> 02064BD0
004C8484  movaps   xmm0, xmm2
004C8487  shufps   xmm8, xmm11, 0x55
004C848C  mulss    xmm0, xmm1
004C8490  movups   xmmword ptr [rsp + 0x130], xmm2
004C8498  addss    xmm6, xmm0
004C849C  movaps   xmmword ptr [rsp + 0x170], xmm10
004C84A5  movaps   xmm0, xmm2
004C84A8  movaps   xmmword ptr [rsp + 0x1a0], xmm9
004C84B1  shufps   xmm0, xmm2, 0x55
004C84B5  movaps   xmmword ptr [rsp + 0x160], xmm0
004C84BD  mulss    xmm0, xmm1
004C84C1  movups   xmmword ptr [rip + 0x1b9c6a8], xmm2  ; -> 02064B70
004C84C8  movaps   xmm2, xmm7
004C84CB  movaps   xmmword ptr [rsp + 0x1b0], xmm8
004C84D4  addss    xmm3, xmm0
004C84D8  shufps   xmm2, xmm7, 0xaa
004C84DC  movaps   xmm0, xmm10
004C84E0  mulss    xmm0, xmm1
004C84E4  movups   xmmword ptr [rip + 0x1b9c6d5], xmm7  ; -> 02064BC0
004C84EB  addss    xmm4, xmm0
004C84EF  movaps   xmm0, xmm9
004C84F3  mulss    xmm0, xmm1
004C84F7  movaps   xmm1, xmm2
004C84FA  mulss    xmm1, xmm8
004C84FF  addss    xmm5, xmm0
004C8503  movups   xmm0, xmmword ptr [r8 + rbx]
004C8508  movups   xmmword ptr [rip + 0x1b9c670], xmm11  ; -> 02064B80
004C8510  movups   xmmword ptr [rsp + 0xf0], xmm0
004C8518  movups   xmmword ptr [rip + 0x1b9c6c1], xmm0  ; -> 02064BE0
004C851F  movaps   xmm0, xmm2
004C8522  addss    xmm3, xmm1
004C8526  mulss    xmm0, xmm11
004C852B  addss    xmm6, xmm0
004C852F  movaps   xmm0, xmm2
004C8532  shufps   xmm7, xmm7, 0xff
004C8536  movaps   xmm1, xmm7
004C8539  lea      eax, [r13 + 0x2c]
004C853D  shl      eax, 4
004C8540  movaps   xmm15, xmm11
004C8544  shufps   xmm15, xmm11, 0xaa
004C8549  movaps   xmm14, xmm11
004C854D  mulss    xmm0, xmm15
004C8552  movsxd   rdx, eax
004C8555  lea      eax, [r13 + 0x28]
004C8559  shufps   xmm14, xmm11, 0xff
004C855E  mulss    xmm2, xmm14
004C8563  shl      eax, 4
004C8566  addss    xmm4, xmm0
004C856A  cdqe     
004C856C  movups   xmm0, xmmword ptr [rdx + rbx]
004C8570  mov      qword ptr [rsp + 0x1c0], rax
004C8578  addss    xmm5, xmm2
004C857C  movaps   xmmword ptr [rsp + 0x90], xmm15
004C8585  movups   xmm2, xmmword ptr [rsp + 0x110]
004C858D  movzx    r15d, word ptr [rax + rbx]
004C8592  movups   xmmword ptr [rsp + 0x100], xmm0
004C859A  movups   xmmword ptr [rip + 0x1b9c64f], xmm0  ; -> 02064BF0
004C85A1  movaps   xmm13, xmm2
004C85A5  movss    dword ptr [rip + 0x1b9c5e3], xmm2  ; -> 02064B90
004C85AD  shufps   xmm13, xmm2, 0x55
004C85B2  movaps   xmm12, xmm2
004C85B6  shufps   xmm12, xmm2, 0xaa
004C85BB  movaps   xmm11, xmm2
004C85BF  shufps   xmm11, xmm2, 0xff
004C85C4  movaps   xmm0, xmm7
004C85C7  mulss    xmm0, xmm2
004C85CB  mulss    xmm1, xmm13
004C85D0  addss    xmm0, xmm6
004C85D4  movss    dword ptr [rip + 0x1b9c5b7], xmm13  ; -> 02064B94
004C85DD  movss    dword ptr [rip + 0x1b9c5b2], xmm12  ; -> 02064B98
004C85E6  addss    xmm1, xmm3
004C85EA  movss    dword ptr [rip + 0x1b9c5a9], xmm11  ; -> 02064B9C
004C85F3  movaps   xmmword ptr [rsp + 0xa0], xmm14
004C85FC  movaps   xmmword ptr [rsp + 0xb0], xmm13
004C8605  movss    dword ptr [rip + 0x1b9c5b3], xmm0  ; -> 02064BC0
004C860D  movaps   xmm0, xmm7
004C8610  mulss    xmm0, xmm12
004C8615  movss    dword ptr [rip + 0x1b9c5a7], xmm1  ; -> 02064BC4
004C861D  movups   xmm1, xmmword ptr [rsp + 0x120]
004C8625  addss    xmm0, xmm4
004C8629  mulss    xmm7, xmm11
004C862E  movaps   xmm6, xmm1
004C8631  movaps   xmmword ptr [rsp + 0x40], xmm11
004C8637  shufps   xmm6, xmm6, 0
004C863B  movaps   xmm2, xmm1
004C863E  shufps   xmm2, xmm1, 0x55
004C8642  addss    xmm7, xmm5
004C8646  movss    dword ptr [rip + 0x1b9c57a], xmm0  ; -> 02064BC8
004C864E  movaps   xmm1, xmm10
004C8652  movups   xmm0, xmmword ptr [rip + 0x1b9c507]  ; -> 02064B60
004C8659  mulss    xmm1, xmm2
004C865D  mulps    xmm6, xmm0
004C8660  movss    xmm0, dword ptr [rsp + 0x130]
004C8669  mulss    xmm0, xmm2
004C866D  movups   xmmword ptr [rip + 0x1b9c4ac], xmm6  ; -> 02064B20
004C8674  movss    xmm3, dword ptr [rip + 0x1b9c4a8]  ; -> 02064B24
004C867C  addss    xmm6, xmm0
004C8680  movaps   xmm0, xmmword ptr [rsp + 0x160]
004C8688  movss    xmm5, dword ptr [rip + 0x1b9c49c]  ; -> 02064B2C
004C8690  movss    xmm4, dword ptr [rip + 0x1b9c490]  ; -> 02064B28
004C8698  mulss    xmm0, xmm2
004C869C  addss    xmm4, xmm1
004C86A0  movss    dword ptr [rip + 0x1b9c524], xmm7  ; -> 02064BCC
004C86A8  movups   xmm10, xmmword ptr [r11 - 0x198]
004C86B0  addss    xmm3, xmm0
004C86B4  movaps   xmmword ptr [rsp + 0x80], xmm12
004C86BD  movaps   xmm0, xmm9
004C86C1  mulss    xmm0, xmm2
004C86C5  movaps   xmm2, xmm10
004C86C9  shufps   xmm2, xmm10, 0xaa
004C86CE  addss    xmm5, xmm0
004C86D2  movaps   xmm0, xmm2
004C86D5  mulss    xmm0, dword ptr [rip + 0x1b9c4a3]  ; -> 02064B80
004C86DD  addss    xmm6, xmm0
004C86E1  movaps   xmm0, xmm2
004C86E4  shufps   xmm10, xmm10, 0xff
004C86E9  mulss    xmm0, xmm15
004C86EE  lea      eax, [r13 + 0xb]
004C86F2  shl      eax, 4
004C86F5  movaps   xmm1, xmm2
004C86F8  movsxd   rcx, eax
004C86FB  mulss    xmm1, xmm8
004C8700  lea      eax, [r13 + 0xc]
004C8704  shl      eax, 4
004C8707  addss    xmm4, xmm0
004C870B  mulss    xmm2, xmm14
004C8710  movss    xmm0, dword ptr [rsp + 0x110]
004C8719  addss    xmm3, xmm1
004C871D  mulss    xmm0, xmm10
004C8722  addss    xmm5, xmm2
004C8726  addss    xmm0, xmm6
004C872A  movss    dword ptr [rsp + 0x50], xmm0
004C8730  movss    dword ptr [rip + 0x1b9c498], xmm0  ; -> 02064BD0
004C8738  movaps   xmm0, xmm10
004C873C  mulss    xmm0, xmm13
004C8741  addss    xmm0, xmm3
004C8745  movss    dword ptr [rsp + 0x54], xmm0
004C874B  movss    dword ptr [rip + 0x1b9c481], xmm0  ; -> 02064BD4
004C8753  movaps   xmm0, xmm10
004C8757  mulss    xmm0, xmm12
004C875C  mulss    xmm10, xmm11
004C8761  addss    xmm0, xmm4
004C8765  addss    xmm10, xmm5
004C876A  movss    dword ptr [rsp + 0x58], xmm0
004C8770  movss    dword ptr [rip + 0x1b9c460], xmm0  ; -> 02064BD8
004C8778  movups   xmmword ptr [r11 - 0x198], xmm10
004C8780  movups   xmm3, xmmword ptr [rsp + 0xf0]
004C8788  movups   xmm0, xmmword ptr [rip + 0x1b9c3d1]  ; -> 02064B60
004C878F  movss    xmm1, dword ptr [rsp + 0x130]
004C8798  movaps   xmm6, xmm3
004C879B  movaps   xmm2, xmm3
004C879E  shufps   xmm6, xmm6, 0
004C87A2  mulps    xmm6, xmm0
004C87A5  movaps   xmm0, xmmword ptr [rsp + 0x160]
004C87AD  shufps   xmm2, xmm3, 0x55
004C87B1  mulss    xmm0, xmm2
004C87B5  mulss    xmm1, xmm2
004C87B9  movups   xmmword ptr [rip + 0x1b9c360], xmm6  ; -> 02064B20
004C87C0  movss    xmm3, dword ptr [rip + 0x1b9c35c]  ; -> 02064B24
004C87C8  addss    xmm6, xmm1
004C87CC  movss    xmm1, dword ptr [rsp + 0x170]
004C87D5  addss    xmm3, xmm0
004C87D9  movss    xmm5, dword ptr [rip + 0x1b9c34b]  ; -> 02064B2C
004C87E1  movaps   xmm0, xmm9
004C87E5  movss    xmm4, dword ptr [rip + 0x1b9c33b]  ; -> 02064B28
004C87ED  mulss    xmm0, xmm2
004C87F1  mulss    xmm1, xmm2
004C87F5  addss    xmm5, xmm0
004C87F9  movss    dword ptr [rip + 0x1b9c3da], xmm10  ; -> 02064BDC
004C8802  movups   xmm0, xmmword ptr [rsp + 0xf0]
004C880A  movups   xmm10, xmmword ptr [rcx + rbx]
004C880F  movsxd   rcx, eax
004C8812  lea      eax, [r13 + 0xd]
004C8816  movaps   xmm2, xmm0
004C8819  shl      eax, 4
004C881C  shufps   xmm2, xmm0, 0xaa
004C8820  addss    xmm4, xmm1
004C8824  movaps   xmm0, xmm2
004C8827  movaps   xmm1, xmm2
004C882A  mulss    xmm0, dword ptr [rip + 0x1b9c34e]  ; -> 02064B80
004C8832  movups   xmm7, xmmword ptr [rcx + rbx]
004C8836  movsxd   rcx, eax
004C8839  addss    xmm6, xmm0
004C883D  mulss    xmm1, xmm8
004C8842  movaps   xmm0, xmm2
004C8845  mulss    xmm2, xmm14
004C884A  movups   xmm9, xmmword ptr [rcx + rbx]
004C884F  mulss    xmm0, xmm15
004C8854  addss    xmm3, xmm1
004C8858  movups   xmmword ptr [rip + 0x1b9c410], xmm10  ; -> 02064C70
004C8860  movups   xmmword ptr [rsp + 0x180], xmm7
004C8868  movups   xmmword ptr [rip + 0x1b9c411], xmm7  ; -> 02064C80
004C886F  addss    xmm4, xmm0
004C8873  addss    xmm5, xmm2
004C8877  movups   xmmword ptr [r11 - 0x128], xmm9
004C887F  movups   xmm0, xmmword ptr [rsp + 0xf0]
004C8887  lea      eax, [r13 + 0xe]
004C888B  movss    xmm1, dword ptr [rsp + 0x110]
004C8894  movups   xmm8, xmmword ptr [r10 + rbx]
004C8899  shl      eax, 4
004C889C  shufps   xmm0, xmm0, 0xff
004C88A0  mulss    xmm1, xmm0
004C88A4  movsxd   rcx, eax
004C88A7  movups   xmmword ptr [rip + 0x1b9c3e1], xmm9  ; -> 02064C90
004C88AF  addss    xmm1, xmm6
004C88B3  movups   xmmword ptr [rip + 0x1b9c375], xmm8  ; -> 02064C30
004C88BB  movss    dword ptr [rsp + 0x5c], xmm1
004C88C1  movss    dword ptr [rip + 0x1b9c317], xmm1  ; -> 02064BE0
004C88C9  movaps   xmm1, xmm0
004C88CC  mulss    xmm1, xmm13
004C88D1  addss    xmm1, xmm3
004C88D5  movups   xmm3, xmmword ptr [rsp + 0x100]
004C88DD  movaps   xmm6, xmm3
004C88E0  movaps   xmm2, xmm3
004C88E3  movss    dword ptr [rsp + 0x60], xmm1
004C88E9  movss    dword ptr [rip + 0x1b9c2f3], xmm1  ; -> 02064BE4
004C88F1  movaps   xmm1, xmm0
004C88F4  mulss    xmm0, xmm11
004C88F9  mulss    xmm1, xmm12
004C88FE  addss    xmm0, xmm5
004C8902  shufps   xmm2, xmm3, 0x55
004C8906  shufps   xmm6, xmm6, 0
004C890A  addss    xmm1, xmm4
004C890E  movss    dword ptr [rip + 0x1b9c2d6], xmm0  ; -> 02064BEC
004C8916  movups   xmmword ptr [rsp + 0xf0], xmm0
004C891E  movups   xmm0, xmmword ptr [rcx + rbx]
004C8922  movss    dword ptr [rsp + 0x64], xmm1
004C8928  movups   xmmword ptr [rsp + 0x150], xmm0
004C8930  movups   xmm0, xmmword ptr [rip + 0x1b9c229]  ; -> 02064B60
004C8937  movss    dword ptr [rip + 0x1b9c2a9], xmm1  ; -> 02064BE8
004C893F  movss    xmm1, dword ptr [rsp + 0x130]
004C8948  mulps    xmm6, xmm0
004C894B  movss    xmm0, dword ptr [rsp + 0x160]
004C8954  mulss    xmm0, xmm2
004C8958  mulss    xmm1, xmm2
004C895C  movups   xmmword ptr [rip + 0x1b9c1bd], xmm6  ; -> 02064B20
004C8963  movss    xmm3, dword ptr [rip + 0x1b9c1b9]  ; -> 02064B24
004C896B  addss    xmm6, xmm1
004C896F  movss    xmm1, dword ptr [rsp + 0x170]
004C8978  addss    xmm3, xmm0
004C897C  movss    xmm0, dword ptr [rsp + 0x1a0]
004C8985  movss    xmm5, dword ptr [rip + 0x1b9c19f]  ; -> 02064B2C
004C898D  movss    xmm4, dword ptr [rip + 0x1b9c193]  ; -> 02064B28
004C8995  mulss    xmm0, xmm2
004C8999  mulss    xmm1, xmm2
004C899D  addss    xmm5, xmm0
004C89A1  movups   xmm0, xmmword ptr [r9 + rbx]
004C89A6  addss    xmm4, xmm1
004C89AA  movups   xmmword ptr [rsp + 0x140], xmm0
004C89B2  movups   xmmword ptr [rip + 0x1b9c287], xmm0  ; -> 02064C40
004C89B9  movups   xmm0, xmmword ptr [rsp + 0x100]
004C89C1  movaps   xmm2, xmm0
004C89C4  shufps   xmm2, xmm0, 0xaa
004C89C8  movaps   xmm0, xmm2
004C89CB  movaps   xmm1, xmm2
004C89CE  mulss    xmm0, dword ptr [rip + 0x1b9c1aa]  ; -> 02064B80
004C89D6  mulss    xmm1, dword ptr [rsp + 0x1b0]
004C89DF  addss    xmm6, xmm0
004C89E3  movaps   xmm0, xmm2
004C89E6  mulss    xmm0, xmm15
004C89EB  addss    xmm3, xmm1
004C89EF  mulss    xmm2, xmm14
004C89F4  movss    xmm1, dword ptr [rsp + 0x110]
004C89FD  addss    xmm4, xmm0
004C8A01  movups   xmm0, xmmword ptr [r8 + rbx]
004C8A06  addss    xmm5, xmm2
004C8A0A  movups   xmmword ptr [rsp + 0xd0], xmm0
004C8A12  movups   xmmword ptr [rip + 0x1b9c237], xmm0  ; -> 02064C50
004C8A19  movups   xmm0, xmmword ptr [rsp + 0x100]
004C8A21  shufps   xmm0, xmm0, 0xff
004C8A25  mulss    xmm1, xmm0
004C8A29  addss    xmm1, xmm6
004C8A2D  movss    dword ptr [rsp + 0x68], xmm1
004C8A33  movss    dword ptr [rip + 0x1b9c1b5], xmm1  ; -> 02064BF0
004C8A3B  movaps   xmm1, xmm0
004C8A3E  mulss    xmm1, xmm13
004C8A43  addss    xmm1, xmm3
004C8A47  movss    dword ptr [rip + 0x1b9c231], xmm7  ; -> 02064C80
004C8A4F  movaps   xmm15, xmm7
004C8A53  movaps   xmm14, xmm7
004C8A57  shufps   xmm15, xmm7, 0x55
004C8A5C  movaps   xmm13, xmm7
004C8A60  shufps   xmm14, xmm7, 0xaa
004C8A65  shufps   xmm13, xmm7, 0xff
004C8A6A  movss    dword ptr [rsp + 0x6c], xmm1
004C8A70  movss    dword ptr [rip + 0x1b9c17c], xmm1  ; -> 02064BF4
004C8A78  movaps   xmm1, xmm0
004C8A7B  mulss    xmm0, xmm11
004C8A80  mulss    xmm1, xmm12
004C8A85  movaps   xmm12, xmm9
004C8A89  addss    xmm0, xmm5
004C8A8D  shufps   xmm12, xmm9, 0x55
004C8A92  movaps   xmm5, xmm8
004C8A96  movss    dword ptr [rip + 0x1b9c1e5], xmm15  ; -> 02064C84
004C8A9F  addss    xmm1, xmm4
004C8AA3  shufps   xmm5, xmm5, 0
004C8AA7  mulps    xmm5, xmm10
004C8AAB  movaps   xmm10, xmm9
004C8AAF  movss    dword ptr [rip + 0x1b9c145], xmm0  ; -> 02064BFC
004C8AB7  movups   xmmword ptr [rsp + 0x100], xmm0
004C8ABF  movups   xmm0, xmmword ptr [rdx + rbx]
004C8AC3  movss    dword ptr [rsp + 0x70], xmm1
004C8AC9  movups   xmmword ptr [rsp + 0xe0], xmm0
004C8AD1  movups   xmmword ptr [rip + 0x1b9c188], xmm0  ; -> 02064C60
004C8AD8  movss    dword ptr [rip + 0x1b9c118], xmm1  ; -> 02064BF8
004C8AE0  movaps   xmm0, xmm7
004C8AE3  movups   xmmword ptr [rip + 0x1b9c036], xmm5  ; -> 02064B20
004C8AEA  movss    xmm2, dword ptr [rip + 0x1b9c032]  ; -> 02064B24
004C8AF2  movaps   xmm1, xmm8
004C8AF6  movss    xmm3, dword ptr [rip + 0x1b9c02a]  ; -> 02064B28
004C8AFE  movaps   xmm7, xmm9
004C8B02  movss    xmm4, dword ptr [rip + 0x1b9c022]  ; -> 02064B2C
004C8B0A  shufps   xmm1, xmm8, 0x55
004C8B0F  mulss    xmm0, xmm1
004C8B13  shufps   xmm10, xmm9, 0xaa
004C8B18  shufps   xmm7, xmm9, 0xff
004C8B1D  addss    xmm5, xmm0
004C8B21  movaps   xmm0, xmm15
004C8B25  mulss    xmm0, xmm1
004C8B29  addss    xmm2, xmm0
004C8B2D  movaps   xmm0, xmm14
004C8B31  mulss    xmm0, xmm1
004C8B35  addss    xmm3, xmm0
004C8B39  movaps   xmm0, xmm13
004C8B3D  mulss    xmm0, xmm1
004C8B41  movaps   xmm1, xmm8
004C8B45  shufps   xmm1, xmm8, 0xaa
004C8B4A  shufps   xmm8, xmm8, 0xff
004C8B4F  addss    xmm4, xmm0
004C8B53  movaps   xmm0, xmm9
004C8B57  mulss    xmm0, xmm1
004C8B5B  addss    xmm5, xmm0
004C8B5F  movaps   xmm0, xmm12
004C8B63  mulss    xmm0, xmm1
004C8B67  addss    xmm2, xmm0
004C8B6B  movaps   xmm0, xmm10
004C8B6F  mulss    xmm0, xmm1
004C8B73  mulss    xmm1, xmm7
004C8B77  addss    xmm3, xmm0
004C8B7B  addss    xmm4, xmm1
004C8B7F  movups   xmm1, xmmword ptr [rsp + 0x150]
004C8B87  movups   xmmword ptr [r11 - 0x1f8], xmm8
004C8B8F  movaps   xmm0, xmm1
004C8B92  movaps   xmm11, xmm1
004C8B96  mulss    xmm0, xmm8
004C8B9B  movaps   xmm9, xmm1
004C8B9F  shufps   xmm11, xmm1, 0x55
004C8BA4  shufps   xmm9, xmm1, 0xaa
004C8BA9  addss    xmm0, xmm5
004C8BAD  movss    dword ptr [rip + 0x1b9c07b], xmm0  ; -> 02064C30
004C8BB5  movaps   xmm0, xmm11
004C8BB9  mulss    xmm0, xmm8
004C8BBE  addss    xmm0, xmm2
004C8BC2  movss    dword ptr [rip + 0x1b9c06a], xmm0  ; -> 02064C34
004C8BCA  movaps   xmm0, xmm9
004C8BCE  mulss    xmm0, xmm8
004C8BD3  addss    xmm0, xmm3
004C8BD7  movss    dword ptr [rip + 0x1b9c059], xmm0  ; -> 02064C38
004C8BDF  movaps   xmm8, xmm1
004C8BE3  shufps   xmm8, xmm1, 0xff
004C8BE8  movups   xmm1, xmmword ptr [rsp + 0x140]
004C8BF0  movaps   xmm0, xmm8
004C8BF4  mulss    xmm0, dword ptr [rsp + 0xc0]
004C8BFD  movaps   xmm6, xmm1
004C8C00  movaps   xmm2, xmm1
004C8C03  shufps   xmm6, xmm6, 0
004C8C07  shufps   xmm2, xmm1, 0x55
004C8C0B  movaps   xmm1, xmm14
004C8C0F  addss    xmm0, xmm4
004C8C13  mulss    xmm1, xmm2
004C8C17  movss    dword ptr [rip + 0x1b9c01d], xmm0  ; -> 02064C3C
004C8C1F  movups   xmm0, xmmword ptr [rip + 0x1b9c04a]  ; -> 02064C70
004C8C26  mulps    xmm6, xmm0
004C8C29  movss    xmm0, dword ptr [rsp + 0x180]
004C8C32  mulss    xmm0, xmm2
004C8C36  movups   xmmword ptr [rip + 0x1b9bee3], xmm6  ; -> 02064B20
004C8C3D  movss    xmm3, dword ptr [rip + 0x1b9bedf]  ; -> 02064B24
004C8C45  addss    xmm6, xmm0
004C8C49  movss    xmm5, dword ptr [rip + 0x1b9bedb]  ; -> 02064B2C
004C8C51  movaps   xmm0, xmm15
004C8C55  movss    xmm4, dword ptr [rip + 0x1b9becb]  ; -> 02064B28
004C8C5D  mulss    xmm0, xmm2
004C8C61  addss    xmm4, xmm1
004C8C65  movss    xmm1, dword ptr [rsp + 0x190]
004C8C6E  addss    xmm3, xmm0
004C8C72  movaps   xmm0, xmm13
004C8C76  mulss    xmm0, xmm2
004C8C7A  addss    xmm5, xmm0
004C8C7E  movups   xmm0, xmmword ptr [rsp + 0x140]
004C8C86  movaps   xmm2, xmm0
004C8C89  shufps   xmm2, xmm0, 0xaa
004C8C8D  movaps   xmm0, xmm12
004C8C91  mulss    xmm0, xmm2
004C8C95  mulss    xmm1, xmm2
004C8C99  addss    xmm3, xmm0
004C8C9D  movups   xmm0, xmmword ptr [rsp + 0x150]
004C8CA5  addss    xmm6, xmm1
004C8CA9  movaps   xmm1, xmm10
004C8CAD  mulss    xmm1, xmm2
004C8CB1  mulss    xmm2, xmm7
004C8CB5  addss    xmm4, xmm1
004C8CB9  movaps   xmm1, xmm9
004C8CBD  addss    xmm5, xmm2
004C8CC1  movss    xmm2, dword ptr [rsp + 0x14c]
004C8CCA  mulss    xmm0, xmm2
004C8CCE  mulss    xmm1, xmm2
004C8CD2  addss    xmm0, xmm6
004C8CD6  addss    xmm1, xmm4
004C8CDA  movss    dword ptr [rip + 0x1b9bf5e], xmm0  ; -> 02064C40
004C8CE2  movaps   xmm0, xmm11
004C8CE6  mulss    xmm0, xmm2
004C8CEA  movss    dword ptr [rip + 0x1b9bf56], xmm1  ; -> 02064C48
004C8CF2  movups   xmm1, xmmword ptr [rsp + 0x180]
004C8CFA  addss    xmm0, xmm3
004C8CFE  movss    dword ptr [rip + 0x1b9bf3e], xmm0  ; -> 02064C44
004C8D06  movaps   xmm0, xmm8
004C8D0A  mulss    xmm0, xmm2
004C8D0E  addss    xmm0, xmm5
004C8D12  movups   xmm5, xmmword ptr [rsp + 0xd0]
004C8D1A  movaps   xmm4, xmm5
004C8D1D  movss    dword ptr [rip + 0x1b9bf27], xmm0  ; -> 02064C4C
004C8D25  movups   xmm0, xmmword ptr [rip + 0x1b9bf44]  ; -> 02064C70
004C8D2C  shufps   xmm4, xmm4, 0
004C8D30  mulps    xmm4, xmm0
004C8D33  movaps   xmm0, xmm5
004C8D36  shufps   xmm0, xmm5, 0x55
004C8D3A  mulss    xmm1, xmm0
004C8D3E  movups   xmmword ptr [rip + 0x1b9bddb], xmm4  ; -> 02064B20
004C8D45  movss    xmm2, dword ptr [rip + 0x1b9bddb]  ; -> 02064B28
004C8D4D  addss    xmm4, xmm1
004C8D51  movss    xmm1, dword ptr [rip + 0x1b9bdcb]  ; -> 02064B24
004C8D59  movss    xmm3, dword ptr [rip + 0x1b9bdcb]  ; -> 02064B2C
004C8D61  mulss    xmm15, xmm0
004C8D66  mulss    xmm14, xmm0
004C8D6B  mulss    xmm13, xmm0
004C8D70  addss    xmm1, xmm15
004C8D75  addss    xmm2, xmm14
004C8D7A  addss    xmm3, xmm13
004C8D7F  movups   xmm6, xmmword ptr [rsp + 0x190]
004C8D87  lea      eax, [r13 + 0x64]
004C8D8B  movzx    r12d, r13w
004C8D8F  movaps   xmm0, xmm5
004C8D92  shl      eax, 4
004C8D95  shufps   xmm0, xmm5, 0xaa
004C8D99  mulss    xmm6, xmm0
004C8D9D  movsxd   rcx, eax
004C8DA0  mulss    xmm12, xmm0
004C8DA5  mulss    xmm10, xmm0
004C8DAA  addss    xmm4, xmm6
004C8DAE  mulss    xmm0, xmm7
004C8DB2  addss    xmm1, xmm12
004C8DB7  movups   xmm7, xmmword ptr [rsp + 0xe0]
004C8DBF  shufps   xmm5, xmm5, 0xff
004C8DC3  addss    xmm2, xmm10
004C8DC8  addss    xmm3, xmm0
004C8DCC  mulss    xmm11, xmm5
004C8DD1  movups   xmm0, xmmword ptr [rcx + rbx]
004C8DD5  addss    xmm11, xmm1
004C8DDA  mulss    xmm8, xmm5
004C8DDF  mulss    xmm9, xmm5
004C8DE4  movaps   xmm6, xmm7
004C8DE7  movups   xmm1, xmmword ptr [rsp + 0x130]
004C8DEF  movups   xmmword ptr [rip + 0x1b9beba], xmm0  ; -> 02064CB0
004C8DF6  movups   xmm0, xmmword ptr [rsp + 0x150]
004C8DFE  addss    xmm8, xmm3
004C8E03  shufps   xmm6, xmm6, 0
004C8E07  mulss    xmm0, xmm5
004C8E0B  addss    xmm9, xmm2
004C8E10  movaps   xmm2, xmm7
004C8E13  movss    dword ptr [rip + 0x1b9be38], xmm11  ; -> 02064C54
004C8E1C  shufps   xmm2, xmm7, 0xaa
004C8E20  addss    xmm0, xmm4
004C8E24  movss    dword ptr [rip + 0x1b9be2f], xmm8  ; -> 02064C5C
004C8E2D  movss    dword ptr [rip + 0x1b9be22], xmm9  ; -> 02064C58
004C8E36  movss    dword ptr [rip + 0x1b9be12], xmm0  ; -> 02064C50
004C8E3E  movups   xmm0, xmmword ptr [rcx + rbx]
004C8E42  movups   xmmword ptr [rip + 0x1b9be77], xmm0  ; -> 02064CC0
004C8E49  movups   xmm0, xmmword ptr [rip + 0x1b9bd10]  ; -> 02064B60
004C8E50  mulps    xmm6, xmm0
004C8E53  movaps   xmm0, xmm7
004C8E56  shufps   xmm0, xmm7, 0x55
004C8E5A  mulss    xmm1, xmm0
004C8E5E  movups   xmmword ptr [rip + 0x1b9bcbb], xmm6  ; -> 02064B20
004C8E65  movss    xmm3, dword ptr [rip + 0x1b9bcb7]  ; -> 02064B24
004C8E6D  addss    xmm6, xmm1
004C8E71  movaps   xmm1, xmmword ptr [rsp + 0x160]
004C8E79  movss    xmm4, dword ptr [rip + 0x1b9bca7]  ; -> 02064B28
004C8E81  movss    xmm5, dword ptr [rip + 0x1b9bca3]  ; -> 02064B2C
004C8E89  mulss    xmm1, xmm0
004C8E8D  shufps   xmm7, xmm7, 0xff
004C8E91  addss    xmm3, xmm1
004C8E95  movaps   xmm1, xmmword ptr [rsp + 0x170]
004C8E9D  mulss    xmm1, xmm0
004C8EA1  addss    xmm4, xmm1
004C8EA5  movaps   xmm1, xmmword ptr [rsp + 0x1a0]
004C8EAD  mulss    xmm1, xmm0
004C8EB1  movaps   xmm0, xmm2
004C8EB4  mulss    xmm0, dword ptr [rip + 0x1b9bcc4]  ; -> 02064B80
004C8EBC  addss    xmm5, xmm1
004C8EC0  movaps   xmm1, xmm2
004C8EC3  mulss    xmm1, dword ptr [rsp + 0x1b0]
004C8ECC  addss    xmm6, xmm0
004C8ED0  movaps   xmm0, xmm2
004C8ED3  mulss    xmm0, dword ptr [rsp + 0x90]
004C8EDC  mulss    xmm2, dword ptr [rsp + 0xa0]
004C8EE5  addss    xmm3, xmm1
004C8EE9  addss    xmm4, xmm0
004C8EED  movaps   xmm1, xmm7
004C8EF0  movups   xmm0, xmmword ptr [rsp + 0x110]
004C8EF8  mulss    xmm1, dword ptr [rsp + 0x80]
004C8F01  addss    xmm5, xmm2
004C8F05  mulss    xmm0, xmm7
004C8F09  addss    xmm1, xmm4
004C8F0D  addss    xmm0, xmm6
004C8F11  movss    dword ptr [rip + 0x1b9bd47], xmm0  ; -> 02064C60
004C8F19  movaps   xmm0, xmm7
004C8F1C  mulss    xmm0, dword ptr [rsp + 0xb0]
004C8F25  addss    xmm0, xmm3
004C8F29  movss    dword ptr [rip + 0x1b9bd33], xmm0  ; -> 02064C64
004C8F31  movss    xmm9, dword ptr [rip + 0x1939902]  ; -> 01E0283C [f32 1]
004C8F3A  mov      eax, 0xe0
004C8F3F  mulss    xmm7, dword ptr [rsp + 0x40]
004C8F45  movaps   xmm14, xmm9
004C8F49  add      r13w, ax
004C8F4D  movss    xmm0, dword ptr [rip + 0x1b9bcd7]  ; -> 02064C2C
004C8F55  xorps    xmm10, xmm10
004C8F59  movss    xmm3, dword ptr [rip + 0x1b9bcc7]  ; -> 02064C28
004C8F61  movaps   xmm15, xmm0
004C8F65  movss    xmm4, dword ptr [rip + 0x1b9bcb7]  ; -> 02064C24
004C8F6D  addss    xmm7, xmm5
004C8F71  movss    xmm6, dword ptr [rip + 0x19398bb]  ; -> 01E02834 [u32 0x00000000]
004C8F79  movss    xmm13, dword ptr [rip + 0x19398ae]  ; -> 01E02830 [u32 0x00000000]
004C8F82  movss    dword ptr [rip + 0x1b9bcde], xmm1  ; -> 02064C68
004C8F8A  mulss    xmm14, xmm9
004C8F8F  movss    dword ptr [rip + 0x1b9bcd5], xmm7  ; -> 02064C6C
004C8F97  movss    xmm7, dword ptr [rip + 0x1939899]  ; -> 01E02838 [u32 0x00000000]
004C8F9F  movaps   xmm2, xmm7
004C8FA2  addss    xmm15, xmm7
004C8FA7  movaps   xmm8, xmm7
004C8FAB  addss    xmm2, xmm9
004C8FB0  subss    xmm8, xmm0
004C8FB5  movss    dword ptr [rsp + 0x24], xmm15
004C8FBC  movss    dword ptr [rsp + 0x30], xmm2
004C8FC2  movss    dword ptr [rsp + 0x28], xmm8
004C8FC9  nop      dword ptr [rax]
004C8FD0  movss    xmm11, dword ptr [rip + 0x1b9bcdb]  ; -> 02064CB4
004C8FD9  movaps   xmm1, xmm6
004C8FDC  addss    xmm1, dword ptr [rip + 0x1b9bcd8]  ; -> 02064CBC
004C8FE4  movss    xmm12, dword ptr [rip + 0x1b9bcd3]  ; -> 02064CC0
004C8FED  movaps   xmm0, xmm13
004C8FF1  addss    xmm0, dword ptr [rip + 0x1b9bcbf]  ; -> 02064CB8
004C8FF9  movss    dword ptr [rip + 0x1b9bcd7], xmm2  ; -> 02064CD8
004C9001  dec      r15w
004C9005  movss    dword ptr [rip + 0x1b9bcdb], xmm2  ; -> 02064CE8
004C900D  movss    dword ptr [rip + 0x1b9bcbf], xmm1  ; -> 02064CD4
004C9015  movaps   xmm1, xmm6
004C9018  addss    xmm1, dword ptr [rip + 0x1b9bcac]  ; -> 02064CCC
004C9020  movss    dword ptr [rip + 0x1b9bca8], xmm0  ; -> 02064CD0
004C9028  movaps   xmm0, xmm13
004C902C  addss    xmm0, dword ptr [rip + 0x1b9bc94]  ; -> 02064CC8
004C9034  mulss    xmm12, xmm3
004C9039  movsx    edi, r12w
004C903D  movss    dword ptr [rip + 0x1b9bc9f], xmm1  ; -> 02064CE4
004C9045  mulss    xmm11, xmm4
004C904A  movss    dword ptr [rip + 0x1b9bc8e], xmm0  ; -> 02064CE0
004C9052  lea      eax, [rdi + 0x28a]
004C9058  movups   xmm0, xmmword ptr [rip + 0x1b9bc71]  ; -> 02064CD0
004C905F  shl      eax, 4
004C9062  movsxd   rcx, eax
004C9065  movaps   xmm1, xmm11
004C9069  movss    dword ptr [rip + 0x1b9bc46], xmm15  ; -> 02064CB8
004C9072  lea      eax, [rdi + 0x2ee]
004C9078  movss    xmm15, dword ptr [rip + 0x1b9bc2f]  ; -> 02064CB0
004C9081  shl      eax, 4
004C9084  movups   xmmword ptr [rcx + rbx], xmm0
004C9088  movsxd   rcx, eax
004C908B  lea      eax, [rdi + 0x258]
004C9091  movups   xmm0, xmmword ptr [rip + 0x1b9bc48]  ; -> 02064CE0
004C9098  shl      eax, 4
004C909B  mulss    xmm15, xmm4
004C90A0  movsxd   rbp, eax
004C90A3  lea      eax, [rdi + 0x2bc]
004C90A9  movups   xmmword ptr [rcx + rbx], xmm0
004C90AD  shl      eax, 4
004C90B0  movss    xmm0, dword ptr [rsp + 0x24]
004C90B6  movaps   xmm2, xmm0
004C90B9  movss    dword ptr [rip + 0x1b9bc06], xmm8  ; -> 02064CC8
004C90C2  movss    xmm8, dword ptr [rip + 0x1b9bbf9]  ; -> 02064CC4
004C90CB  mulss    xmm2, xmm0
004C90CF  movsxd   r14, eax
004C90D2  mulss    xmm8, xmm3
004C90D7  movaps   xmm3, xmm15
004C90DB  mulss    xmm3, xmm15
004C90E0  mulss    xmm2, xmm9
004C90E5  mulss    xmm1, xmm11
004C90EA  mulss    xmm3, xmm9
004C90EF  mulss    xmm1, xmm9
004C90F4  movss    dword ptr [rip + 0x1b9bbbf], xmm14  ; -> 02064CBC
004C90FD  movss    dword ptr [rip + 0x1b9bbae], xmm11  ; -> 02064CB4
004C9106  addss    xmm3, xmm1
004C910A  movss    dword ptr [rip + 0x1b9bb9d], xmm15  ; -> 02064CB0
004C9113  movups   xmm0, xmmword ptr [rip + 0x1b9bb96]  ; -> 02064CB0
004C911A  movss    dword ptr [rip + 0x1b9bba9], xmm14  ; -> 02064CCC
004C9123  movups   xmmword ptr [rbx + rbp], xmm0
004C9127  addss    xmm2, xmm3
004C912B  movss    dword ptr [rip + 0x1b9bb90], xmm8  ; -> 02064CC4
004C9134  movss    dword ptr [rip + 0x1b9bb83], xmm12  ; -> 02064CC0
004C913D  movups   xmm0, xmmword ptr [rip + 0x1b9bb7c]  ; -> 02064CC0
004C9144  movups   xmmword ptr [r14 + rbx], xmm0
004C9149  cvtps2pd xmm0, xmm2
004C914C  andps    xmm0, xmmword ptr [rip + 0x1822c2d]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
004C9153  cvtpd2ps xmm0, xmm0
004C9157  call     0x861f14  ; -> 00861F14 fn
004C915C  ucomiss  xmm0, xmm10
004C9160  jp       0x4c916e  ; -> 004C916E
004C9162  jne      0x4c916e  ; -> 004C916E
004C9164  movss    xmm3, dword ptr [rip + 0x4371f4]  ; -> 00900360 [u32 0x7F7FFFFF]
004C916C  jmp      0x4c9176  ; -> 004C9176
004C916E  movaps   xmm3, xmm9
004C9172  divss    xmm3, xmm0
004C9176  movss    xmm4, dword ptr [rsp + 0x28]
004C917C  movaps   xmm1, xmm12
004C9180  mulss    xmm1, xmm12
004C9185  movaps   xmm2, xmm4
004C9188  movss    xmm12, dword ptr [rsp + 0x24]
004C918F  movaps   xmm0, xmm8
004C9193  mulss    xmm0, xmm8
004C9198  mulss    xmm2, xmm4
004C919C  mulss    xmm0, xmm9
004C91A1  mulss    xmm2, xmm9
004C91A6  mulss    xmm1, xmm9
004C91AB  mulss    xmm12, xmm3
004C91B0  addss    xmm1, xmm0
004C91B4  movaps   xmm0, xmm15
004C91B8  mulss    xmm0, xmm3
004C91BC  movss    dword ptr [rsp + 0x2c], xmm0
004C91C2  addss    xmm2, xmm1
004C91C6  movaps   xmm0, xmm11
004C91CA  mulss    xmm0, xmm3
004C91CE  movss    dword ptr [rsp + 0x20], xmm0
004C91D4  cvtps2pd xmm0, xmm2
004C91D7  andps    xmm0, xmmword ptr [rip + 0x1822ba2]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
004C91DE  cvtpd2ps xmm0, xmm0
004C91E2  call     0x861f14  ; -> 00861F14 fn
004C91E7  ucomiss  xmm0, xmm10
004C91EB  jp       0x4c91f9  ; -> 004C91F9
004C91ED  jne      0x4c91f9  ; -> 004C91F9
004C91EF  movss    xmm5, dword ptr [rip + 0x437169]  ; -> 00900360 [u32 0x7F7FFFFF]
004C91F7  jmp      0x4c9201  ; -> 004C9201
004C91F9  movaps   xmm5, xmm9
004C91FD  divss    xmm5, xmm0
004C9201  movss    xmm4, dword ptr [rsp + 0x20]
004C9207  movss    xmm1, dword ptr [rsp + 0x2c]
004C920D  movups   xmm0, xmmword ptr [rip + 0x1b9ba1c]  ; -> 02064C30
004C9214  shufps   xmm1, xmm1, 0
004C9218  mulps    xmm1, xmm0
004C921B  movaps   xmm0, xmm4
004C921E  mulss    xmm0, dword ptr [rip + 0x1b9ba1a]  ; -> 02064C40
004C9226  movups   xmmword ptr [rip + 0x1b9b8f3], xmm1  ; -> 02064B20
004C922D  addss    xmm1, xmm0
004C9231  movss    xmm2, dword ptr [rip + 0x1b9b8eb]  ; -> 02064B24
004C9239  movss    xmm3, dword ptr [rip + 0x1b9b8e7]  ; -> 02064B28
004C9241  movaps   xmm0, xmm4
004C9244  mulss    xmm0, dword ptr [rip + 0x1b9b9f8]  ; -> 02064C44
004C924C  mulss    xmm4, dword ptr [rip + 0x1b9b9f4]  ; -> 02064C48
004C9254  addss    xmm2, xmm0
004C9258  movaps   xmm0, xmm12
004C925C  mulss    xmm0, dword ptr [rip + 0x1b9b9ec]  ; -> 02064C50
004C9264  addss    xmm3, xmm4
004C9268  addss    xmm0, xmm1
004C926C  movaps   xmm1, xmm12
004C9270  mulss    xmm1, dword ptr [rip + 0x1b9b9dc]  ; -> 02064C54
004C9278  mulss    xmm12, dword ptr [rip + 0x1b9b9d7]  ; -> 02064C58
004C9281  movss    dword ptr [rip + 0x1b9b8b7], xmm0  ; -> 02064B40
004C9289  addss    xmm1, xmm2
004C928D  movss    xmm0, dword ptr [rip + 0x1b9ba2b]  ; -> 02064CC0
004C9295  mulss    xmm0, xmm5
004C9299  addss    xmm12, xmm3
004C929E  movss    dword ptr [rip + 0x1b9b89e], xmm1  ; -> 02064B44
004C92A6  movaps   xmm1, xmm11
004C92AA  mulss    xmm1, dword ptr [rsp + 0x58]
004C92B0  movss    dword ptr [rsp + 0x20], xmm0
004C92B6  movaps   xmm0, xmm8
004C92BA  mulss    xmm0, xmm5
004C92BE  movss    dword ptr [rip + 0x1b9b881], xmm12  ; -> 02064B48
004C92C7  movss    xmm12, dword ptr [rsp + 0x28]
004C92CE  movss    dword ptr [rsp + 0x2c], xmm0
004C92D4  movups   xmm0, xmmword ptr [rip + 0x1b9b8e5]  ; -> 02064BC0
004C92DB  mulss    xmm12, xmm5
004C92E0  movaps   xmm5, xmm15
004C92E4  movss    xmm15, dword ptr [rsp + 0x24]
004C92EB  shufps   xmm5, xmm5, 0
004C92EF  mulps    xmm5, xmm0
004C92F2  movaps   xmm0, xmm11
004C92F6  mulss    xmm0, dword ptr [rsp + 0x50]
004C92FC  movups   xmmword ptr [rip + 0x1b9b81d], xmm5  ; -> 02064B20
004C9303  movss    xmm2, dword ptr [rip + 0x1b9b819]  ; -> 02064B24
004C930B  addss    xmm5, xmm0
004C930F  movss    xmm3, dword ptr [rip + 0x1b9b811]  ; -> 02064B28
004C9317  movaps   xmm0, xmm11
004C931B  mulss    xmm0, dword ptr [rsp + 0x54]
004C9321  addss    xmm3, xmm1
004C9325  mulss    xmm11, dword ptr [rsp + 0x120]
004C932F  movaps   xmm1, xmm15
004C9333  mulss    xmm1, dword ptr [rsp + 0x60]
004C9339  addss    xmm2, xmm0
004C933D  movss    xmm4, dword ptr [rip + 0x1b9b7e7]  ; -> 02064B2C
004C9345  movaps   xmm0, xmm15
004C9349  mulss    xmm0, dword ptr [rsp + 0x5c]
004C934F  addss    xmm4, xmm11
004C9354  addss    xmm2, xmm1
004C9358  movaps   xmm1, xmm15
004C935C  mulss    xmm1, dword ptr [rsp + 0xf0]
004C9365  addss    xmm5, xmm0
004C9369  movaps   xmm0, xmm15
004C936D  mulss    xmm0, dword ptr [rsp + 0x64]
004C9373  addss    xmm4, xmm1
004C9377  movss    xmm1, dword ptr [rsp + 0x6c]
004C937D  mulss    xmm1, xmm14
004C9382  addss    xmm3, xmm0
004C9386  movss    xmm0, dword ptr [rsp + 0x68]
004C938C  mulss    xmm0, xmm14
004C9391  addss    xmm1, xmm2
004C9395  addss    xmm0, xmm5
004C9399  movss    dword ptr [rip + 0x1b9b913], xmm1  ; -> 02064CB4
004C93A1  movss    xmm1, dword ptr [rsp + 0x100]
004C93AA  movss    dword ptr [rip + 0x1b9b8fe], xmm0  ; -> 02064CB0
004C93B2  movss    xmm0, dword ptr [rsp + 0x70]
004C93B8  mulss    xmm0, xmm14
004C93BD  mulss    xmm1, xmm14
004C93C2  addss    xmm0, xmm3
004C93C6  movss    dword ptr [rip + 0x1b9b8ea], xmm0  ; -> 02064CB8
004C93CE  addss    xmm1, xmm4
004C93D2  ucomiss  xmm1, xmm10
004C93D6  movss    dword ptr [rip + 0x1b9b8de], xmm1  ; -> 02064CBC
004C93DE  jp       0x4c93ed  ; -> 004C93ED
004C93E0  jne      0x4c93ed  ; -> 004C93ED
004C93E2  movss    xmm11, dword ptr [rip + 0x436f75]  ; -> 00900360 [u32 0x7F7FFFFF]
004C93EB  jmp      0x4c93f6  ; -> 004C93F6
004C93ED  movaps   xmm11, xmm9
004C93F1  divss    xmm11, xmm1
004C93F6  movss    xmm4, dword ptr [rsp + 0x2c]
004C93FC  movups   xmm0, xmmword ptr [rip + 0x1b9b82d]  ; -> 02064C30
004C9403  movss    xmm1, dword ptr [rsp + 0x20]
004C9409  movss    xmm5, dword ptr [rip + 0x1b9b8af]  ; -> 02064CC0
004C9411  shufps   xmm1, xmm1, 0
004C9415  mulps    xmm1, xmm0
004C9418  movaps   xmm0, xmm4
004C941B  mulss    xmm0, dword ptr [rip + 0x1b9b81d]  ; -> 02064C40
004C9423  shufps   xmm5, xmm5, 0
004C9427  movups   xmmword ptr [rip + 0x1b9b6f2], xmm1  ; -> 02064B20
004C942E  addss    xmm1, xmm0
004C9432  movss    xmm2, dword ptr [rip + 0x1b9b6ea]  ; -> 02064B24
004C943A  movss    xmm3, dword ptr [rip + 0x1b9b6e6]  ; -> 02064B28
004C9442  movaps   xmm0, xmm4
004C9445  mulss    xmm0, dword ptr [rip + 0x1b9b7f7]  ; -> 02064C44
004C944D  mulss    xmm4, dword ptr [rip + 0x1b9b7f3]  ; -> 02064C48
004C9455  addss    xmm2, xmm0
004C9459  movaps   xmm0, xmm12
004C945D  mulss    xmm0, dword ptr [rip + 0x1b9b7eb]  ; -> 02064C50
004C9465  addss    xmm3, xmm4
004C9469  addss    xmm0, xmm1
004C946D  movaps   xmm1, xmm12
004C9471  mulss    xmm1, dword ptr [rip + 0x1b9b7db]  ; -> 02064C54
004C9479  mulss    xmm12, dword ptr [rip + 0x1b9b7d6]  ; -> 02064C58
004C9482  addss    xmm1, xmm2
004C9486  movss    dword ptr [rip + 0x1b9b6c2], xmm0  ; -> 02064B50
004C948E  movups   xmm0, xmmword ptr [rip + 0x1b9b72b]  ; -> 02064BC0
004C9495  addss    xmm12, xmm3
004C949A  mulps    xmm5, xmm0
004C949D  movaps   xmm0, xmm8
004C94A1  mulss    xmm0, dword ptr [rsp + 0x50]
004C94A7  movss    dword ptr [rip + 0x1b9b6a5], xmm1  ; -> 02064B54
004C94AF  movaps   xmm1, xmm8
004C94B3  mulss    xmm1, dword ptr [rsp + 0x58]
004C94B9  movups   xmmword ptr [rip + 0x1b9b660], xmm5  ; -> 02064B20
004C94C0  movss    xmm2, dword ptr [rip + 0x1b9b65c]  ; -> 02064B24
004C94C8  addss    xmm5, xmm0
004C94CC  movss    xmm4, dword ptr [rip + 0x1b9b658]  ; -> 02064B2C
004C94D4  movaps   xmm0, xmm8
004C94D8  mulss    xmm0, dword ptr [rsp + 0x54]
004C94DE  mulss    xmm8, dword ptr [rsp + 0x120]
004C94E8  movss    xmm3, dword ptr [rip + 0x1b9b638]  ; -> 02064B28
004C94F0  addss    xmm2, xmm0
004C94F4  addss    xmm3, xmm1
004C94F8  movss    dword ptr [rip + 0x1b9b657], xmm12  ; -> 02064B58
004C9501  addss    xmm4, xmm8
004C9506  movss    xmm8, dword ptr [rsp + 0x28]
004C950D  movaps   xmm0, xmm8
004C9511  movaps   xmm1, xmm8
004C9515  mulss    xmm0, dword ptr [rsp + 0x5c]
004C951B  mulss    xmm1, dword ptr [rsp + 0x60]
004C9521  addss    xmm5, xmm0
004C9525  movaps   xmm0, xmm8
004C9529  mulss    xmm0, dword ptr [rsp + 0x64]
004C952F  addss    xmm2, xmm1
004C9533  movaps   xmm1, xmm8
004C9537  mulss    xmm1, dword ptr [rsp + 0xf0]
004C9540  addss    xmm3, xmm0
004C9544  movss    xmm0, dword ptr [rsp + 0x68]
004C954A  mulss    xmm0, xmm14
004C954F  addss    xmm4, xmm1
004C9553  movss    xmm1, dword ptr [rsp + 0x6c]
004C9559  mulss    xmm1, xmm14
004C955E  addss    xmm0, xmm5
004C9562  addss    xmm1, xmm2
004C9566  movss    xmm2, dword ptr [rsp + 0x100]
004C956F  mulss    xmm2, xmm14
004C9574  movss    dword ptr [rip + 0x1b9b744], xmm0  ; -> 02064CC0
004C957C  movss    xmm0, dword ptr [rsp + 0x70]
004C9582  mulss    xmm0, xmm14
004C9587  addss    xmm2, xmm4
004C958B  movss    dword ptr [rip + 0x1b9b731], xmm1  ; -> 02064CC4
004C9593  movups   xmm1, xmmword ptr [rip + 0x1b9b716]  ; -> 02064CB0
004C959A  addss    xmm0, xmm3
004C959E  movss    dword ptr [rip + 0x1b9b726], xmm2  ; -> 02064CCC
004C95A6  movss    dword ptr [rip + 0x1b9b71a], xmm0  ; -> 02064CC8
004C95AE  movaps   xmm0, xmm11
004C95B2  shufps   xmm0, xmm0, 0
004C95B6  mulps    xmm1, xmm0
004C95B9  mulss    xmm11, xmm9
004C95BE  movups   xmmword ptr [rip + 0x1b9b6eb], xmm1  ; -> 02064CB0
004C95C5  ucomiss  xmm2, xmm10
004C95C9  movss    dword ptr [rip + 0x1b9b70a], xmm11  ; -> 02064CDC
004C95D2  jp       0x4c95e0  ; -> 004C95E0
004C95D4  jne      0x4c95e0  ; -> 004C95E0
004C95D6  movss    xmm1, dword ptr [rip + 0x436d82]  ; -> 00900360 [u32 0x7F7FFFFF]
004C95DE  jmp      0x4c95e8  ; -> 004C95E8
004C95E0  movaps   xmm1, xmm9
004C95E4  divss    xmm1, xmm2
004C95E8  movsd    xmm0, qword ptr [rip + 0x1b9b550]  ; -> 02064B40
004C95F0  lea      eax, [rdi + 0x1c2]
004C95F6  movups   xmm2, xmmword ptr [rip + 0x1b9b6c3]  ; -> 02064CC0
004C95FD  shl      eax, 4
004C9600  movss    xmm5, dword ptr [rip + 0x1b9b6a8]  ; -> 02064CB0
004C9608  movsxd   rcx, eax
004C960B  mov      eax, dword ptr [rip + 0x1b9b537]  ; -> 02064B48
004C9611  movss    dword ptr [rip + 0x1b9b4e7], xmm1  ; -> 02064B00
004C9619  movsd    qword ptr [rcx + rbx], xmm0
004C961E  movsd    xmm0, qword ptr [rip + 0x1b9b52a]  ; -> 02064B50
004C9626  mov      dword ptr [rcx + rbx + 8], eax
004C962A  lea      eax, [rdi + 0x226]
004C9630  shl      eax, 4
004C9633  movsxd   rcx, eax
004C9636  mov      eax, dword ptr [rip + 0x1b9b51c]  ; -> 02064B58
004C963C  movsd    qword ptr [rcx + rbx], xmm0
004C9641  movaps   xmm0, xmm1
004C9644  mov      dword ptr [rcx + rbx + 8], eax
004C9648  lea      eax, [rdi + 0x190]
004C964E  shl      eax, 4
004C9651  movsxd   r11, eax
004C9654  mov      eax, dword ptr [rip + 0x1b9b65e]  ; -> 02064CB8
004C965A  shufps   xmm0, xmm0, 0
004C965E  mulps    xmm2, xmm0
004C9661  movsd    xmm0, qword ptr [rip + 0x1b9b647]  ; -> 02064CB0
004C9669  movsd    qword ptr [r11 + rbx], xmm0
004C966F  mov      dword ptr [r11 + rbx + 8], eax
004C9674  lea      eax, [rdi + 0x1f4]
004C967A  shl      eax, 4
004C967D  movsxd   rsi, eax
004C9680  mov      eax, dword ptr [rip + 0x1b9b656]  ; -> 02064CDC
004C9686  movups   xmmword ptr [rip + 0x1b9b633], xmm2  ; -> 02064CC0
004C968D  movsd    qword ptr [rsi + rbx], xmm2
004C9692  psrldq   xmm2, 8
004C9697  movd     dword ptr [rsi + rbx + 8], xmm2
004C969D  movss    xmm2, dword ptr [rip + 0x1b9b48b]  ; -> 02064B30
004C96A5  ucomiss  xmm2, xmm5
004C96A8  mov      dword ptr [rbx + rbp + 0xc], eax
004C96AC  mulss    xmm1, xmm9
004C96B1  movss    dword ptr [rip + 0x1b9b633], xmm1  ; -> 02064CEC
004C96B9  mov      eax, dword ptr [rip + 0x1b9b62d]  ; -> 02064CEC
004C96BF  mov      dword ptr [rbx + r14 + 0xc], eax
004C96C4  jp       0x4c96d0  ; -> 004C96D0
004C96C6  jne      0x4c96d0  ; -> 004C96D0
004C96C8  mov      r9d, 1
004C96CE  jmp      0x4c96d3  ; -> 004C96D3
004C96D0  xor      r9d, r9d
004C96D3  movss    xmm1, dword ptr [rip + 0x1b9b5d9]  ; -> 02064CB4
004C96DB  movss    xmm11, dword ptr [rip + 0x1b9b450]  ; -> 02064B34
004C96E4  ucomiss  xmm11, xmm1
004C96E8  jp       0x4c96f3  ; -> 004C96F3
004C96EA  jne      0x4c96f3  ; -> 004C96F3
004C96EC  mov      edx, 1
004C96F1  jmp      0x4c96f5  ; -> 004C96F5
004C96F3  xor      edx, edx
004C96F5  movss    xmm0, dword ptr [rip + 0x1b9b5bb]  ; -> 02064CB8
004C96FD  movss    xmm12, dword ptr [rip + 0x1b9b432]  ; -> 02064B38
004C9706  ucomiss  xmm12, xmm0
004C970A  jp       0x4c9715  ; -> 004C9715
004C970C  jne      0x4c9715  ; -> 004C9715
004C970E  mov      ecx, 1
004C9713  jmp      0x4c9717  ; -> 004C9717
004C9715  xor      ecx, ecx
004C9717  movss    xmm4, dword ptr [rip + 0x1b9b5a1]  ; -> 02064CC0
004C971F  xor      r8d, r8d
004C9722  comiss   xmm5, xmm2
004C9725  seta     r8b
004C9729  xor      eax, eax
004C972B  add      r8w, r8w
004C972F  comiss   xmm1, xmm11
004C9733  seta     al
004C9736  add      r8w, ax
004C973A  xor      eax, eax
004C973C  add      r8w, r8w
004C9740  comiss   xmm0, xmm12
004C9744  seta     al
004C9747  add      r8w, ax
004C974B  shl      r8w, 2
004C9750  add      r8w, r9w
004C9754  add      r8w, r8w
004C9758  add      r8w, dx
004C975C  add      r8w, r8w
004C9760  add      r8w, cx
004C9764  add      r8w, r8w
004C9768  ucomiss  xmm2, xmm4
004C976B  mov      word ptr [rip + 0x1b9b39d], r8w  ; -> 02064B10
004C9773  jp       0x4c977f  ; -> 004C977F
004C9775  jne      0x4c977f  ; -> 004C977F
004C9777  mov      r10d, 1
004C977D  jmp      0x4c9782  ; -> 004C9782
004C977F  xor      r10d, r10d
004C9782  movss    xmm3, dword ptr [rip + 0x1b9b53a]  ; -> 02064CC4
004C978A  ucomiss  xmm11, xmm3
004C978E  jp       0x4c9799  ; -> 004C9799
004C9790  jne      0x4c9799  ; -> 004C9799
004C9792  mov      edx, 1
004C9797  jmp      0x4c979b  ; -> 004C979B
004C9799  xor      edx, edx
004C979B  movss    xmm2, dword ptr [rip + 0x1b9b525]  ; -> 02064CC8
004C97A3  ucomiss  xmm12, xmm2
004C97A7  jp       0x4c97b2  ; -> 004C97B2
004C97A9  jne      0x4c97b2  ; -> 004C97B2
004C97AB  mov      ecx, 1
004C97B0  jmp      0x4c97b4  ; -> 004C97B4
004C97B2  xor      ecx, ecx
004C97B4  xor      r9d, r9d
004C97B7  comiss   xmm4, dword ptr [rip + 0x1b9b372]  ; -> 02064B30
004C97BE  seta     r9b
004C97C2  xor      eax, eax
004C97C4  add      r9w, r9w
004C97C8  comiss   xmm3, xmm11
004C97CC  seta     al
004C97CF  add      r9w, ax
004C97D3  xor      eax, eax
004C97D5  add      r9w, r9w
004C97D9  comiss   xmm2, xmm12
004C97DD  seta     al
004C97E0  add      r9w, ax
004C97E4  shl      r9w, 2
004C97E9  add      r9w, r10w
004C97ED  add      r9w, r9w
004C97F1  add      r9w, dx
004C97F5  add      r9w, r9w
004C97F9  add      r9w, cx
004C97FD  add      r9w, r9w
004C9801  ucomiss  xmm5, xmm13
004C9805  mov      word ptr [rip + 0x1b9b305], r9w  ; -> 02064B12
004C980D  jp       0x4c9818  ; -> 004C9818
004C980F  jne      0x4c9818  ; -> 004C9818
004C9811  mov      ebp, 1
004C9816  jmp      0x4c981a  ; -> 004C981A
004C9818  xor      ebp, ebp
004C981A  ucomiss  xmm1, xmm6
004C981D  jp       0x4c9828  ; -> 004C9828
004C981F  jne      0x4c9828  ; -> 004C9828
004C9821  mov      edx, 1
004C9826  jmp      0x4c982a  ; -> 004C982A
004C9828  xor      edx, edx
004C982A  ucomiss  xmm0, xmm7
004C982D  jp       0x4c9838  ; -> 004C9838
004C982F  jne      0x4c9838  ; -> 004C9838
004C9831  mov      ecx, 1
004C9836  jmp      0x4c983a  ; -> 004C983A
004C9838  xor      ecx, ecx
004C983A  xor      r10d, r10d
004C983D  comiss   xmm13, xmm5
004C9841  seta     r10b
004C9845  xor      eax, eax
004C9847  add      r10w, r10w
004C984B  comiss   xmm6, xmm1
004C984E  seta     al
004C9851  add      r10w, ax
004C9855  xor      eax, eax
004C9857  add      r10w, r10w
004C985B  comiss   xmm7, xmm0
004C985E  seta     al
004C9861  add      r10w, ax
004C9865  shl      r10w, 2
004C986A  add      r10w, bp
004C986E  add      r10w, r10w
004C9872  add      r10w, dx
004C9876  add      r10w, r10w
004C987A  add      r10w, cx
004C987E  add      r10w, r10w
004C9882  ucomiss  xmm4, xmm13
004C9886  mov      word ptr [rip + 0x1b9b286], r10w  ; -> 02064B14
004C988E  jp       0x4c989a  ; -> 004C989A
004C9890  jne      0x4c989a  ; -> 004C989A
004C9892  mov      r14d, 1
004C9898  jmp      0x4c989d  ; -> 004C989D
004C989A  xor      r14d, r14d
004C989D  ucomiss  xmm3, xmm6
004C98A0  jp       0x4c98ab  ; -> 004C98AB
004C98A2  jne      0x4c98ab  ; -> 004C98AB
004C98A4  mov      ebp, 1
004C98A9  jmp      0x4c98ad  ; -> 004C98AD
004C98AB  xor      ebp, ebp
004C98AD  ucomiss  xmm2, xmm7
004C98B0  jp       0x4c98bb  ; -> 004C98BB
004C98B2  jne      0x4c98bb  ; -> 004C98BB
004C98B4  mov      ecx, 1
004C98B9  jmp      0x4c98bd  ; -> 004C98BD
004C98BB  xor      ecx, ecx
004C98BD  xor      edx, edx
004C98BF  comiss   xmm13, xmm4
004C98C3  movss    xmm4, dword ptr [rip + 0x1b9b359]  ; -> 02064C24
004C98CB  seta     dl
004C98CE  xor      eax, eax
004C98D0  add      dx, dx
004C98D3  comiss   xmm6, xmm3
004C98D6  movss    xmm3, dword ptr [rip + 0x1b9b34a]  ; -> 02064C28
004C98DE  seta     al
004C98E1  add      dx, ax
004C98E4  xor      eax, eax
004C98E6  add      dx, dx
004C98E9  comiss   xmm7, xmm2
004C98EC  movss    xmm2, dword ptr [rsp + 0x30]
004C98F2  seta     al
004C98F5  and      r10w, r13w
004C98F9  add      dx, ax
004C98FC  mov      word ptr [rip + 0x1b9b4e0], r10w  ; -> 02064DE4
004C9904  shl      dx, 2
004C9908  and      r8w, r13w
004C990C  add      dx, r14w
004C9910  movsx    eax, r10w
004C9914  or       r8w, ax
004C9918  add      dx, dx
004C991B  add      dx, bp
004C991E  and      r9w, r13w
004C9922  add      dx, dx
004C9925  inc      r12w
004C9929  add      dx, cx
004C992C  movzx    ecx, r13w
004C9930  add      dx, dx
004C9933  and      cx, dx
004C9936  mov      word ptr [rip + 0x1b9b1d9], dx  ; -> 02064B16
004C993D  movsx    eax, cx
004C9940  or       r9w, ax
004C9944  mov      word ptr [rip + 0x1b9b49d], cx  ; -> 02064DE8
004C994B  movzx    eax, r8w
004C994F  mov      dword ptr [r11 + rbx + 0xc], eax
004C9954  movzx    eax, r9w
004C9958  mov      dword ptr [rsi + rbx + 0xc], eax
004C995C  lea      eax, [rdi + 0x65]
004C995F  shl      eax, 4
004C9962  movsxd   rcx, eax
004C9965  movups   xmm0, xmmword ptr [rcx + rbx]
004C9969  movups   xmmword ptr [rip + 0x1b9b340], xmm0  ; -> 02064CB0
004C9970  movups   xmmword ptr [rip + 0x1b9b349], xmm0  ; -> 02064CC0
004C9977  test     r15w, r15w
004C997B  jg       0x4c8fd0  ; -> 004C8FD0
004C9981  movzx    eax, word ptr [rip + 0x1b9b184]  ; -> 02064B0C
004C9988  mov      r15d, 4
004C998E  movaps   xmm14, xmmword ptr [rip + 0x858d8a]  ; -> 00D22720 [f32x4 -1, -1, -1, -1]
004C9996  mov      word ptr [rip + 0x1b9b43b], ax  ; -> 02064DD8
004C999D  mov      word ptr [rip + 0x1b9b438], ax  ; -> 02064DDC
004C99A4  mov      word ptr [rip + 0x1b9b435], ax  ; -> 02064DE0
004C99AB  lea      r12d, [r15 + 4]
004C99AF  mov      rax, qword ptr [rsp + 0x1c0]
004C99B7  lea      r13d, [r15 + 0xc]
004C99BB  movzx    eax, word ptr [rax + rbx + 4]
004C99C0  movups   xmm0, xmmword ptr [rip + 0x1b9b269]  ; -> 02064C30
004C99C7  dec      ax
004C99CA  mov      dword ptr [rip + 0x1b9b130], 0xbf800000  ; -> 02064B04
004C99D4  addss    xmm7, xmm9
004C99D9  mulss    xmm6, xmm13
004C99DE  mov      word ptr [rip + 0x1b9b3ef], ax  ; -> 02064DD4
004C99E5  movsx    eax, word ptr [rip + 0x1b9b3ec]  ; -> 02064DD8
004C99EC  movaps   xmm5, xmm13
004C99F0  add      eax, 0x96
004C99F5  mulss    xmm5, xmm13
004C99FA  shl      eax, 4
004C99FD  movsxd   rcx, eax
004C9A00  movaps   xmm1, xmm6
004C9A03  mulss    xmm1, dword ptr [rip + 0x1b9b23d]  ; -> 02064C48
004C9A0B  shufps   xmm5, xmm5, 0
004C9A0F  movsx    eax, word ptr [rcx + rbx]
004C9A13  movsx    edx, word ptr [rcx + rbx + 4]
004C9A18  movsx    ecx, word ptr [rcx + rbx + 8]
004C9A1D  mulps    xmm5, xmm0
004C9A20  movaps   xmm0, xmm6
004C9A23  mov      word ptr [rip + 0x1b9b392], ax  ; -> 02064DBC
004C9A2A  add      eax, 0x190
004C9A2F  mulss    xmm0, dword ptr [rip + 0x1b9b209]  ; -> 02064C40
004C9A37  shl      eax, 4
004C9A3A  cdqe     
004C9A3C  movups   xmmword ptr [rip + 0x1b9b0dd], xmm5  ; -> 02064B20
004C9A43  mov      word ptr [rip + 0x1b9b376], dx  ; -> 02064DC0
004C9A4A  movss    xmm2, dword ptr [rip + 0x1b9b0d2]  ; -> 02064B24
004C9A52  addss    xmm5, xmm0
004C9A56  movss    xmm3, dword ptr [rip + 0x1b9b0ca]  ; -> 02064B28
004C9A5E  movaps   xmm0, xmm6
004C9A61  mulss    xmm0, dword ptr [rip + 0x1b9b1db]  ; -> 02064C44
004C9A69  addss    xmm3, xmm1
004C9A6D  mov      word ptr [rip + 0x1b9b350], cx  ; -> 02064DC4
004C9A74  movss    xmm4, dword ptr [rip + 0x1b9b0b0]  ; -> 02064B2C
004C9A7C  movaps   xmm1, xmm7
004C9A7F  mulss    xmm1, dword ptr [rip + 0x1b9b1cd]  ; -> 02064C54
004C9A87  mulss    xmm6, dword ptr [rip + 0x1b9b1bd]  ; -> 02064C4C
004C9A8F  addss    xmm2, xmm0
004C9A93  movaps   xmm0, xmm7
004C9A96  movss    dword ptr [rip + 0x1b9b08a], xmm3  ; -> 02064B28
004C9A9E  mulss    xmm0, dword ptr [rip + 0x1b9b1aa]  ; -> 02064C50
004C9AA6  addss    xmm4, xmm6
004C9AAA  movss    dword ptr [rip + 0x1b9b06e], xmm5  ; -> 02064B20
004C9AB2  addss    xmm1, xmm2
004C9AB6  movss    dword ptr [rip + 0x1b9b066], xmm2  ; -> 02064B24
004C9ABE  addss    xmm0, xmm5
004C9AC2  movss    dword ptr [rip + 0x1b9b062], xmm4  ; -> 02064B2C
004C9ACA  movss    dword ptr [rip + 0x1b9b072], xmm1  ; -> 02064B44
004C9AD2  movss    dword ptr [rip + 0x1b9b066], xmm0  ; -> 02064B40
004C9ADA  movaps   xmm0, xmm7
004C9ADD  mulss    xmm0, dword ptr [rip + 0x1b9b173]  ; -> 02064C58
004C9AE5  mulss    xmm7, dword ptr [rip + 0x1b9b16f]  ; -> 02064C5C
004C9AED  addss    xmm0, xmm3
004C9AF1  movups   xmm3, xmmword ptr [rax + rbx]
004C9AF5  lea      eax, [rdx + 0x190]
004C9AFB  shl      eax, 4
004C9AFE  addss    xmm7, xmm4
004C9B02  cdqe     
004C9B04  movss    dword ptr [rip + 0x1b9b03c], xmm0  ; -> 02064B48
004C9B0C  movups   xmmword ptr [rip + 0x1b9b18d], xmm3  ; -> 02064CA0
004C9B13  movups   xmm2, xmmword ptr [rax + rbx]
004C9B17  lea      eax, [rcx + 0x190]
004C9B1D  movss    dword ptr [rip + 0x1b9b027], xmm7  ; -> 02064B4C
004C9B25  movups   xmm1, xmmword ptr [rip + 0x1b9b014]  ; -> 02064B40
004C9B2C  shl      eax, 4
004C9B2F  cdqe     
004C9B31  mulps    xmm1, xmm14
004C9B35  movups   xmmword ptr [rip + 0x1b9b174], xmm2  ; -> 02064CB0
004C9B3C  movups   xmm0, xmmword ptr [rax + rbx]
004C9B40  movups   xmmword ptr [rip + 0x1b9b009], xmm1  ; -> 02064B50
004C9B47  movups   xmmword ptr [rip + 0x1b9b172], xmm0  ; -> 02064CC0
004C9B4E  movaps   xmm0, xmm2
004C9B51  movss    dword ptr [rip + 0x1b9b157], xmm2  ; -> 02064CB0
004C9B59  subss    xmm0, xmm3
004C9B5D  movaps   xmm1, xmm2
004C9B60  shufps   xmm1, xmm2, 0x55
004C9B64  shufps   xmm2, xmm2, 0xaa
004C9B68  movss    dword ptr [rip + 0x1b9b144], xmm1  ; -> 02064CB4
004C9B70  movss    dword ptr [rip + 0x1b9b140], xmm2  ; -> 02064CB8
004C9B78  movss    dword ptr [rip + 0x1b9b170], xmm0  ; -> 02064CF0
004C9B80  movaps   xmm0, xmm3
004C9B83  shufps   xmm0, xmm3, 0x55
004C9B87  shufps   xmm3, xmm3, 0xaa
004C9B8B  subss    xmm1, xmm0
004C9B8F  subss    xmm2, xmm3
004C9B93  movss    dword ptr [rip + 0x1b9b159], xmm1  ; -> 02064CF4
004C9B9B  movss    dword ptr [rip + 0x1b9b155], xmm2  ; -> 02064CF8
004C9BA3  call     0x22cc20  ; -> 0022CC20 fn
004C9BA8  movss    xmm0, dword ptr [rip + 0x1b9b0f0]  ; -> 02064CA0
004C9BB0  subss    xmm0, dword ptr [rip + 0x1b9b108]  ; -> 02064CC0
004C9BB8  movss    xmm1, dword ptr [rip + 0x1b9b0e4]  ; -> 02064CA4
004C9BC0  subss    xmm1, dword ptr [rip + 0x1b9b0fc]  ; -> 02064CC4
004C9BC8  movss    dword ptr [rip + 0x1b9b130], xmm0  ; -> 02064D00
004C9BD0  movss    xmm0, dword ptr [rip + 0x1b9b0d0]  ; -> 02064CA8
004C9BD8  subss    xmm0, dword ptr [rip + 0x1b9b0e8]  ; -> 02064CC8
004C9BE0  movss    dword ptr [rip + 0x1b9b11c], xmm1  ; -> 02064D04
004C9BE8  movss    dword ptr [rip + 0x1b9b118], xmm0  ; -> 02064D08
004C9BF0  call     0x22cc20  ; -> 0022CC20 fn
004C9BF5  movups   xmm4, xmmword ptr [rip + 0x1b9b0f4]  ; -> 02064CF0
004C9BFC  movss    xmm3, dword ptr [rip + 0x1b9b104]  ; -> 02064D08
004C9C04  movss    xmm1, dword ptr [rip + 0x1b9b0f8]  ; -> 02064D04
004C9C0C  movaps   xmm0, xmm4
004C9C0F  movss    xmm2, dword ptr [rip + 0x1b9b0e9]  ; -> 02064D00
004C9C17  movaps   xmm6, xmm1
004C9C1A  shufps   xmm0, xmm4, 0x55
004C9C1E  movaps   xmm5, xmm4
004C9C21  shufps   xmm5, xmm4, 0xaa
004C9C25  movaps   xmm7, xmm3
004C9C28  mulss    xmm7, xmm0
004C9C2C  movaps   xmm0, xmm4
004C9C2F  shufps   xmm0, xmm4, 0xaa
004C9C33  mulss    xmm1, xmm0
004C9C37  movaps   xmm0, xmm4
004C9C3A  mulss    xmm6, xmm4
004C9C3E  mulss    xmm5, xmm2
004C9C42  movss    dword ptr [rip + 0x1b9aed6], xmm7  ; -> 02064B20
004C9C4A  subss    xmm7, xmm1
004C9C4E  movups   xmmword ptr [rsp + 0x1b0], xmm4
004C9C56  shufps   xmm4, xmm4, 0x55
004C9C5A  mulss    xmm0, xmm3
004C9C5E  ucomiss  xmm7, xmm10
004C9C62  mulss    xmm2, xmm4
004C9C66  movss    dword ptr [rip + 0x1b9aeb6], xmm5  ; -> 02064B24
004C9C6E  subss    xmm5, xmm0
004C9C72  movss    dword ptr [rip + 0x1b9aeae], xmm6  ; -> 02064B28
004C9C7A  subss    xmm6, xmm2
004C9C7E  jp       0x4c9c8a  ; -> 004C9C8A
004C9C80  jne      0x4c9c8a  ; -> 004C9C8A
004C9C82  mov      r9d, 1
004C9C88  jmp      0x4c9c8d  ; -> 004C9C8D
004C9C8A  xor      r9d, r9d
004C9C8D  ucomiss  xmm5, xmm10
004C9C91  jp       0x4c9c9d  ; -> 004C9C9D
004C9C93  jne      0x4c9c9d  ; -> 004C9C9D
004C9C95  mov      r8d, 1
004C9C9B  jmp      0x4c9ca0  ; -> 004C9CA0
004C9C9D  xor      r8d, r8d
004C9CA0  ucomiss  xmm6, xmm10
004C9CA4  jp       0x4c9caf  ; -> 004C9CAF
004C9CA6  jne      0x4c9caf  ; -> 004C9CAF
004C9CA8  mov      ecx, 1
004C9CAD  jmp      0x4c9cb1  ; -> 004C9CB1
004C9CAF  xor      ecx, ecx
004C9CB1  movsx    ebp, word ptr [rip + 0x1b9b10c]  ; -> 02064DC4
004C9CB8  xor      edx, edx
004C9CBA  movsx    r10d, word ptr [rip + 0x1b9b11a]  ; -> 02064DDC
004C9CC2  mov      r14d, ebp
004C9CC5  movzx    r11d, word ptr [rip + 0x1b9ae3f]  ; -> 02064B0C
004C9CCD  movsx    edi, word ptr [rip + 0x1b9b0ec]  ; -> 02064DC0
004C9CD4  movups   xmm0, xmmword ptr [rip + 0x1b9ae65]  ; -> 02064B40
004C9CDB  comiss   xmm10, xmm6
004C9CDF  cmova    dx, r15w
004C9CE4  xor      eax, eax
004C9CE6  comiss   xmm10, xmm5
004C9CEA  cmova    ax, r12w
004C9CEF  add      dx, ax
004C9CF2  xor      eax, eax
004C9CF4  comiss   xmm10, xmm7
004C9CF8  cmova    ax, r13w
004C9CFD  add      dx, ax
004C9D00  lea      eax, [rdi + 0x190]
004C9D06  shl      eax, 4
004C9D09  add      dx, r9w
004C9D0D  cdqe     
004C9D0F  add      dx, dx
004C9D12  add      dx, r8w
004C9D16  lea      r8d, [r11 + 0x20]
004C9D1A  add      dx, dx
004C9D1D  add      dx, cx
004C9D20  movzx    esi, word ptr [rax + rbx + 0xc]
004C9D25  add      dx, dx
004C9D28  and      r8w, dx
004C9D2C  mov      word ptr [rip + 0x1b9addd], dx  ; -> 02064B10
004C9D33  lea      eax, [rbp + 0x190]
004C9D39  mov      word ptr [rip + 0x1b9b08c], si  ; -> 02064DCC
004C9D40  shl      eax, 4
004C9D43  movsxd   rcx, eax
004C9D46  lea      eax, [r10 + 0xfa]
004C9D4D  shl      eax, 4
004C9D50  mov      word ptr [rip + 0x1b9b070], r8w  ; -> 02064DC8
004C9D58  movzx    r9d, word ptr [rcx + rbx + 0xc]
004C9D5E  movsxd   rcx, eax
004C9D61  lea      eax, [r10 + 0xc8]
004C9D68  shl      eax, 4
004C9D6B  movsxd   rdx, eax
004C9D6E  mov      word ptr [rip + 0x1b9b05a], r9w  ; -> 02064DD0
004C9D76  movups   xmmword ptr [rcx + rbx], xmm0
004C9D7A  movzx    ecx, word ptr [rip + 0x1b9b03b]  ; -> 02064DBC
004C9D81  mov      dword ptr [rdx + rbx], ecx
004C9D84  cmp      r8w, r11w
004C9D88  jne      0x4c9dcd  ; -> 004C9DCD
004C9D8A  movsx    eax, cx
004C9D8D  add      eax, 0x190
004C9D92  movsx    ecx, si
004C9D95  shl      eax, 4
004C9D98  cdqe     
004C9D9A  movsx    eax, word ptr [rax + rbx + 0xc]
004C9D9F  or       ecx, eax
004C9DA1  movzx    eax, di
004C9DA4  mov      dword ptr [rdx + rbx + 4], eax
004C9DA8  or       r9w, cx
004C9DAC  movzx    eax, bp
004C9DAF  mov      dword ptr [rdx + rbx + 8], eax
004C9DB3  mov      word ptr [rip + 0x1b9b00d], r9w  ; -> 02064DC8
004C9DBB  cmp      r9w, r11w
004C9DBF  jne      0x4c9dcd  ; -> 004C9DCD
004C9DC1  inc      r10w
004C9DC5  mov      word ptr [rip + 0x1b9b00f], r10w  ; -> 02064DDC
004C9DCD  movsx    eax, word ptr [rip + 0x1b9b004]  ; -> 02064DD8
004C9DD4  add      eax, 0x96
004C9DD9  shl      eax, 4
004C9DDC  movsxd   rdx, eax
004C9DDF  lea      eax, [r14 + 0x1f4]
004C9DE6  shl      eax, 4
004C9DE9  movsxd   rcx, eax
004C9DEC  movsx    eax, word ptr [rdx + rbx + 4]
004C9DF1  movsx    r8d, word ptr [rdx + rbx]
004C9DF6  movups   xmm3, xmmword ptr [rcx + rbx]
004C9DFA  mov      word ptr [rip + 0x1b9afbf], ax  ; -> 02064DC0
004C9E01  add      eax, 0x1f4
004C9E06  shl      eax, 4
004C9E09  cdqe     
004C9E0B  movups   xmmword ptr [rip + 0x1b9ae8e], xmm3  ; -> 02064CA0
004C9E12  mov      word ptr [rip + 0x1b9afa2], r8w  ; -> 02064DBC
004C9E1A  movups   xmm2, xmmword ptr [rax + rbx]
004C9E1E  movzx    eax, word ptr [rdx + rbx + 8]
004C9E23  mov      word ptr [rip + 0x1b9af9a], ax  ; -> 02064DC4
004C9E2A  lea      eax, [r8 + 0x1f4]
004C9E31  movups   xmmword ptr [rip + 0x1b9ae78], xmm2  ; -> 02064CB0
004C9E38  shl      eax, 4
004C9E3B  movaps   xmm1, xmm2
004C9E3E  movss    dword ptr [rip + 0x1b9ae6a], xmm2  ; -> 02064CB0
004C9E46  shufps   xmm1, xmm2, 0x55
004C9E4A  cdqe     
004C9E4C  movss    dword ptr [rip + 0x1b9ae60], xmm1  ; -> 02064CB4
004C9E54  movups   xmm0, xmmword ptr [rax + rbx]
004C9E58  movups   xmmword ptr [rip + 0x1b9ae61], xmm0  ; -> 02064CC0
004C9E5F  movaps   xmm0, xmm2
004C9E62  shufps   xmm2, xmm2, 0xaa
004C9E66  subss    xmm0, xmm3
004C9E6A  movss    dword ptr [rip + 0x1b9ae46], xmm2  ; -> 02064CB8
004C9E72  movss    dword ptr [rip + 0x1b9ae76], xmm0  ; -> 02064CF0
004C9E7A  movaps   xmm0, xmm3
004C9E7D  shufps   xmm0, xmm3, 0x55
004C9E81  shufps   xmm3, xmm3, 0xaa
004C9E85  subss    xmm1, xmm0
004C9E89  subss    xmm2, xmm3
004C9E8D  movss    dword ptr [rip + 0x1b9ae5f], xmm1  ; -> 02064CF4
004C9E95  movss    dword ptr [rip + 0x1b9ae5b], xmm2  ; -> 02064CF8
004C9E9D  call     0x22cc20  ; -> 0022CC20 fn
004C9EA2  movss    xmm0, dword ptr [rip + 0x1b9adf6]  ; -> 02064CA0
004C9EAA  subss    xmm0, dword ptr [rip + 0x1b9ae0e]  ; -> 02064CC0
004C9EB2  movss    xmm1, dword ptr [rip + 0x1b9adea]  ; -> 02064CA4
004C9EBA  subss    xmm1, dword ptr [rip + 0x1b9ae02]  ; -> 02064CC4
004C9EC2  movss    dword ptr [rip + 0x1b9ae36], xmm0  ; -> 02064D00
004C9ECA  movss    xmm0, dword ptr [rip + 0x1b9add6]  ; -> 02064CA8
004C9ED2  subss    xmm0, dword ptr [rip + 0x1b9adee]  ; -> 02064CC8
004C9EDA  movss    dword ptr [rip + 0x1b9ae22], xmm1  ; -> 02064D04
004C9EE2  movss    dword ptr [rip + 0x1b9ae1e], xmm0  ; -> 02064D08
004C9EEA  call     0x22cc20  ; -> 0022CC20 fn
004C9EEF  movups   xmm4, xmmword ptr [rip + 0x1b9adfa]  ; -> 02064CF0
004C9EF6  movsx    r11d, word ptr [rip + 0x1b9aede]  ; -> 02064DDC
004C9EFE  movups   xmm0, xmmword ptr [rip + 0x1b9ac4b]  ; -> 02064B50
004C9F05  mov      ebp, r11d
004C9F08  movss    xmm1, dword ptr [rip + 0x1b9adf4]  ; -> 02064D04
004C9F10  movaps   xmm5, xmm4
004C9F13  movss    xmm3, dword ptr [rip + 0x1b9aded]  ; -> 02064D08
004C9F1B  lea      eax, [r11 + 0xfa]
004C9F22  movss    xmm2, dword ptr [rip + 0x1b9add6]  ; -> 02064D00
004C9F2A  movaps   xmm6, xmm1
004C9F2D  shl      eax, 4
004C9F30  movaps   xmm7, xmm3
004C9F33  movsxd   rcx, eax
004C9F36  shufps   xmm5, xmm4, 0xaa
004C9F3A  mulss    xmm5, xmm2
004C9F3E  movups   xmmword ptr [rcx + rbx], xmm0
004C9F42  movaps   xmm0, xmm4
004C9F45  mulss    xmm6, xmm4
004C9F49  shufps   xmm0, xmm4, 0x55
004C9F4D  mulss    xmm7, xmm0
004C9F51  movaps   xmm0, xmm4
004C9F54  shufps   xmm0, xmm4, 0xaa
004C9F58  mulss    xmm1, xmm0
004C9F5C  movss    dword ptr [rip + 0x1b9abbc], xmm7  ; -> 02064B20
004C9F64  movss    dword ptr [rip + 0x1b9abb8], xmm5  ; -> 02064B24
004C9F6C  subss    xmm7, xmm1
004C9F70  movss    dword ptr [rip + 0x1b9abb0], xmm6  ; -> 02064B28
004C9F78  movss    dword ptr [rip + 0x1b9ad78], xmm0  ; -> 02064CF8
004C9F80  movups   xmmword ptr [rsp + 0x1a0], xmm4
004C9F88  ucomiss  xmm7, xmm10
004C9F8C  movaps   xmm0, xmm4
004C9F8F  movss    dword ptr [rip + 0x1b9ad59], xmm4  ; -> 02064CF0
004C9F97  shufps   xmm4, xmm4, 0x55
004C9F9B  mulss    xmm2, xmm4
004C9F9F  mulss    xmm0, xmm3
004C9FA3  subss    xmm6, xmm2
004C9FA7  movss    dword ptr [rip + 0x1b9ad45], xmm4  ; -> 02064CF4
004C9FAF  subss    xmm5, xmm0
004C9FB3  jp       0x4c9fbf  ; -> 004C9FBF
004C9FB5  jne      0x4c9fbf  ; -> 004C9FBF
004C9FB7  mov      r9d, 1
004C9FBD  jmp      0x4c9fc2  ; -> 004C9FC2
004C9FBF  xor      r9d, r9d
004C9FC2  ucomiss  xmm5, xmm10
004C9FC6  jp       0x4c9fd2  ; -> 004C9FD2
004C9FC8  jne      0x4c9fd2  ; -> 004C9FD2
004C9FCA  mov      r8d, 1
004C9FD0  jmp      0x4c9fd5  ; -> 004C9FD5
004C9FD2  xor      r8d, r8d
004C9FD5  ucomiss  xmm6, xmm10
004C9FD9  jp       0x4c9fe4  ; -> 004C9FE4
004C9FDB  jne      0x4c9fe4  ; -> 004C9FE4
004C9FDD  mov      edx, 1
004C9FE2  jmp      0x4c9fe6  ; -> 004C9FE6
004C9FE4  xor      edx, edx
004C9FE6  movsx    r10d, word ptr [rip + 0x1b9add6]  ; -> 02064DC4
004C9FEE  xor      ecx, ecx
004C9FF0  movzx    edi, word ptr [rip + 0x1b9ab15]  ; -> 02064B0C
004C9FF7  comiss   xmm10, xmm6
004C9FFB  cmova    cx, r15w
004CA000  xor      eax, eax
004CA002  comiss   xmm10, xmm5
004CA006  cmova    ax, r12w
004CA00B  add      cx, ax
004CA00E  xor      eax, eax
004CA010  comiss   xmm10, xmm7
004CA014  cmova    ax, r13w
004CA019  add      cx, ax
004CA01C  add      cx, r9w
004CA020  movsx    r9d, word ptr [rip + 0x1b9ad98]  ; -> 02064DC0
004CA028  add      cx, cx
004CA02B  add      cx, r8w
004CA02F  add      cx, cx
004CA032  lea      eax, [r9 + 0x1f4]
004CA039  add      cx, dx
004CA03C  shl      eax, 4
004CA03F  add      cx, cx
004CA042  cdqe     
004CA044  add      r9w, 0x64
004CA049  mov      word ptr [rip + 0x1b9aac0], cx  ; -> 02064B10
004CA050  movzx    esi, word ptr [rax + rbx + 0xc]
004CA055  lea      eax, [r10 + 0x1f4]
004CA05C  shl      eax, 4
004CA05F  add      r10w, 0x64
004CA064  cdqe     
004CA066  mov      word ptr [rip + 0x1b9ad5f], si  ; -> 02064DCC
004CA06D  movzx    r8d, word ptr [rax + rbx + 0xc]
004CA073  lea      eax, [rdi + 0x20]
004CA076  and      ax, cx
004CA079  mov      word ptr [rip + 0x1b9ad4f], r8w  ; -> 02064DD0
004CA081  mov      word ptr [rip + 0x1b9ad40], ax  ; -> 02064DC8
004CA088  cmp      ax, di
004CA08B  jne      0x4ca0ed  ; -> 004CA0ED
004CA08D  movsx    edx, word ptr [rip + 0x1b9ad28]  ; -> 02064DBC
004CA094  movsx    ecx, si
004CA097  lea      eax, [rdx + 0x1f4]
004CA09D  add      dx, 0x64
004CA0A1  shl      eax, 4
004CA0A4  cdqe     
004CA0A6  movsx    eax, word ptr [rax + rbx + 0xc]
004CA0AB  or       ecx, eax
004CA0AD  lea      eax, [rbp + 0xc8]
004CA0B3  shl      eax, 4
004CA0B6  or       r8w, cx
004CA0BA  movsxd   rcx, eax
004CA0BD  movzx    eax, dx
004CA0C0  mov      word ptr [rip + 0x1b9ad00], r8w  ; -> 02064DC8
004CA0C8  mov      dword ptr [rcx + rbx], eax
004CA0CB  cmp      r8w, di
004CA0CF  jne      0x4ca0ed  ; -> 004CA0ED
004CA0D1  movzx    eax, r9w
004CA0D5  inc      r11w
004CA0D9  mov      dword ptr [rcx + rbx + 4], eax
004CA0DD  movzx    eax, r10w
004CA0E1  mov      dword ptr [rcx + rbx + 8], eax
004CA0E5  mov      word ptr [rip + 0x1b9acef], r11w  ; -> 02064DDC
004CA0ED  movsx    eax, word ptr [rip + 0x1b9ace4]  ; -> 02064DD8
004CA0F4  add      eax, 0x96
004CA0F9  shl      eax, 4
004CA0FC  movsxd   rdx, eax
004CA0FF  movzx    eax, word ptr [rdx + rbx + 0xc]
004CA104  mov      word ptr [rip + 0x1b9acb1], ax  ; -> 02064DBC
004CA10B  movzx    r8d, word ptr [rdx + rbx + 4]
004CA111  lea      ecx, [rdi + 1]
004CA114  and      cx, ax
004CA117  mov      word ptr [rip + 0x1b9aca5], r8w  ; -> 02064DC4
004CA11F  cmp      cx, di
004CA122  je       0x4ca896  ; -> 004CA896
004CA128  movsx    eax, word ptr [rdx + rbx]
004CA12C  mov      word ptr [rip + 0x1b9ac8d], ax  ; -> 02064DC0
004CA133  mov      edx, eax
004CA135  add      eax, 0x190
004CA13A  shl      eax, 4
004CA13D  movsxd   rcx, eax
004CA140  movsx    eax, r8w
004CA144  add      eax, 0x190
004CA149  shl      eax, 4
004CA14C  movups   xmm3, xmmword ptr [rcx + rbx]
004CA150  cdqe     
004CA152  movups   xmmword ptr [rip + 0x1b9ab47], xmm3  ; -> 02064CA0
004CA159  movups   xmm2, xmmword ptr [rax + rbx]
004CA15D  lea      eax, [rdx + 0x1f4]
004CA163  shl      eax, 4
004CA166  movups   xmmword ptr [rip + 0x1b9ab43], xmm2  ; -> 02064CB0
004CA16D  movsxd   rcx, eax
004CA170  movaps   xmm1, xmm2
004CA173  movss    dword ptr [rip + 0x1b9ab35], xmm2  ; -> 02064CB0
004CA17B  shufps   xmm1, xmm2, 0x55
004CA17F  movss    dword ptr [rip + 0x1b9ab2d], xmm1  ; -> 02064CB4
004CA187  movups   xmm0, xmmword ptr [rcx + rbx]
004CA18B  movups   xmmword ptr [rip + 0x1b9ab2e], xmm0  ; -> 02064CC0
004CA192  movaps   xmm0, xmm2
004CA195  shufps   xmm2, xmm2, 0xaa
004CA199  subss    xmm0, xmm3
004CA19D  movss    dword ptr [rip + 0x1b9ab13], xmm2  ; -> 02064CB8
004CA1A5  movss    dword ptr [rip + 0x1b9ab43], xmm0  ; -> 02064CF0
004CA1AD  movaps   xmm0, xmm3
004CA1B0  shufps   xmm0, xmm3, 0x55
004CA1B4  shufps   xmm3, xmm3, 0xaa
004CA1B8  subss    xmm1, xmm0
004CA1BC  subss    xmm2, xmm3
004CA1C0  movss    dword ptr [rip + 0x1b9ab2c], xmm1  ; -> 02064CF4
004CA1C8  movss    dword ptr [rip + 0x1b9ab28], xmm2  ; -> 02064CF8
004CA1D0  call     0x22cc20  ; -> 0022CC20 fn
004CA1D5  movss    xmm0, dword ptr [rip + 0x1b9aac3]  ; -> 02064CA0
004CA1DD  subss    xmm0, dword ptr [rip + 0x1b9aadb]  ; -> 02064CC0
004CA1E5  movss    xmm1, dword ptr [rip + 0x1b9aab7]  ; -> 02064CA4
004CA1ED  subss    xmm1, dword ptr [rip + 0x1b9aacf]  ; -> 02064CC4
004CA1F5  movss    dword ptr [rip + 0x1b9ab03], xmm0  ; -> 02064D00
004CA1FD  movss    xmm0, dword ptr [rip + 0x1b9aaa3]  ; -> 02064CA8
004CA205  subss    xmm0, dword ptr [rip + 0x1b9aabb]  ; -> 02064CC8
004CA20D  movss    dword ptr [rip + 0x1b9aaef], xmm1  ; -> 02064D04
004CA215  movss    dword ptr [rip + 0x1b9aaeb], xmm0  ; -> 02064D08
004CA21D  call     0x22cc20  ; -> 0022CC20 fn
004CA222  movups   xmm9, xmmword ptr [rip + 0x1b9aac6]  ; -> 02064CF0
004CA22A  movups   xmm4, xmmword ptr [rip + 0x1b9aacf]  ; -> 02064D00
004CA231  movss    xmm8, dword ptr [rip + 0x1b9aace]  ; -> 02064D08
004CA23A  movaps   xmm0, xmm9
004CA23E  movss    xmm7, dword ptr [rip + 0x1b9aaba]  ; -> 02064D00
004CA246  movaps   xmm13, xmm8
004CA24A  movss    xmm6, dword ptr [rip + 0x1b9aab2]  ; -> 02064D04
004CA252  movaps   xmm5, xmm9
004CA256  shufps   xmm0, xmm9, 0x55
004CA25B  movaps   xmm11, xmm9
004CA25F  mulss    xmm13, xmm0
004CA264  movaps   xmm2, xmm4
004CA267  shufps   xmm5, xmm9, 0xaa
004CA26C  movaps   xmm0, xmm4
004CA26F  shufps   xmm0, xmm4, 0x55
004CA273  movaps   xmm1, xmm5
004CA276  mulss    xmm1, xmm0
004CA27A  movaps   xmm12, xmm6
004CA27E  movaps   xmm0, xmm13
004CA282  shufps   xmm11, xmm9, 0xaa
004CA287  mulss    xmm11, xmm7
004CA28C  subss    xmm0, xmm1
004CA290  shufps   xmm2, xmm4, 0xaa
004CA294  mulss    xmm12, xmm9
004CA299  mulss    xmm2, xmm9
004CA29E  movss    dword ptr [rip + 0x1b9a89a], xmm0  ; -> 02064B40
004CA2A6  movaps   xmm0, xmm11
004CA2AA  movss    dword ptr [rip + 0x1b9a86d], xmm13  ; -> 02064B20
004CA2B3  subss    xmm0, xmm2
004CA2B7  movss    dword ptr [rip + 0x1b9a864], xmm11  ; -> 02064B24
004CA2C0  movss    dword ptr [rip + 0x1b9a85f], xmm12  ; -> 02064B28
004CA2C9  movss    dword ptr [rip + 0x1b9aa27], xmm5  ; -> 02064CF8
004CA2D1  movss    dword ptr [rip + 0x1b9aa16], xmm9  ; -> 02064CF0
004CA2DA  movups   xmmword ptr [rsp + 0x190], xmm9
004CA2E3  movups   xmmword ptr [rsp + 0x180], xmm4
004CA2EB  movaps   xmm3, xmm9
004CA2EF  movss    dword ptr [rip + 0x1b9a84d], xmm0  ; -> 02064B44
004CA2F7  shufps   xmm3, xmm9, 0x55
004CA2FC  movaps   xmm0, xmm12
004CA300  movaps   xmm1, xmm3
004CA303  mulss    xmm6, xmm5
004CA307  mulss    xmm1, xmm4
004CA30B  subss    xmm13, xmm6
004CA310  mulss    xmm9, xmm8
004CA315  subss    xmm0, xmm1
004CA319  mulss    xmm7, xmm3
004CA31D  movss    dword ptr [rip + 0x1b9a9cf], xmm3  ; -> 02064CF4
004CA325  subss    xmm11, xmm9
004CA32A  ucomiss  xmm13, xmm10
004CA32E  movss    dword ptr [rip + 0x1b9a812], xmm0  ; -> 02064B48
004CA336  subss    xmm12, xmm7
004CA33B  jp       0x4ca347  ; -> 004CA347
004CA33D  jne      0x4ca347  ; -> 004CA347
004CA33F  mov      r8d, 1
004CA345  jmp      0x4ca34a  ; -> 004CA34A
004CA347  xor      r8d, r8d
004CA34A  ucomiss  xmm11, xmm10
004CA34E  jp       0x4ca359  ; -> 004CA359
004CA350  jne      0x4ca359  ; -> 004CA359
004CA352  mov      edx, 1
004CA357  jmp      0x4ca35b  ; -> 004CA35B
004CA359  xor      edx, edx
004CA35B  ucomiss  xmm12, xmm10
004CA35F  jp       0x4ca36a  ; -> 004CA36A
004CA361  jne      0x4ca36a  ; -> 004CA36A
004CA363  mov      ecx, 1
004CA368  jmp      0x4ca36c  ; -> 004CA36C
004CA36A  xor      ecx, ecx
004CA36C  movzx    edi, word ptr [rip + 0x1b9a799]  ; -> 02064B0C
004CA373  xor      r9d, r9d
004CA376  comiss   xmm10, xmm12
004CA37A  cmova    r9w, r15w
004CA37F  xor      eax, eax
004CA381  comiss   xmm10, xmm11
004CA385  cmova    ax, r12w
004CA38A  add      r9w, ax
004CA38E  xor      eax, eax
004CA390  comiss   xmm10, xmm13
004CA394  cmova    ax, r13w
004CA399  add      r9w, ax
004CA39D  add      r9w, r8w
004CA3A1  movsx    r8d, word ptr [rip + 0x1b9aa17]  ; -> 02064DC0
004CA3A9  add      r9w, r9w
004CA3AD  add      r9w, dx
004CA3B1  lea      edx, [rdi + 0x20]
004CA3B4  add      r9w, r9w
004CA3B8  add      r9w, cx
004CA3BC  lea      eax, [r8 + 0x258]
004CA3C3  shl      eax, 4
004CA3C6  add      r9w, r9w
004CA3CA  movsxd   rcx, eax
004CA3CD  and      dx, r9w
004CA3D1  movsx    eax, word ptr [rip + 0x1b9a9ec]  ; -> 02064DC4
004CA3D8  add      eax, 0x258
004CA3DD  mov      word ptr [rip + 0x1b9a72b], r9w  ; -> 02064B10
004CA3E5  shl      eax, 4
004CA3E8  movups   xmm0, xmmword ptr [rcx + rbx]
004CA3EC  cdqe     
004CA3EE  mov      word ptr [rip + 0x1b9a9d3], dx  ; -> 02064DC8
004CA3F5  movups   xmmword ptr [rip + 0x1b9a8a4], xmm0  ; -> 02064CA0
004CA3FC  movups   xmm0, xmmword ptr [rax + rbx]
004CA400  lea      eax, [r8 + 0x2bc]
004CA407  shl      eax, 4
004CA40A  movsxd   rcx, eax
004CA40D  movups   xmmword ptr [rip + 0x1b9a89c], xmm0  ; -> 02064CB0
004CA414  movups   xmm0, xmmword ptr [rcx + rbx]
004CA418  movups   xmmword ptr [rip + 0x1b9a8a1], xmm0  ; -> 02064CC0
004CA41F  cmp      dx, di
004CA422  je       0x4ca896  ; -> 004CA896
004CA428  movss    xmm0, dword ptr [rip + 0x1b9a880]  ; -> 02064CB0
004CA430  subss    xmm0, dword ptr [rip + 0x1b9a868]  ; -> 02064CA0
004CA438  movss    xmm1, dword ptr [rip + 0x1b9a874]  ; -> 02064CB4
004CA440  subss    xmm1, dword ptr [rip + 0x1b9a85c]  ; -> 02064CA4
004CA448  movss    dword ptr [rip + 0x1b9a8a0], xmm0  ; -> 02064CF0
004CA450  movss    xmm0, dword ptr [rip + 0x1b9a860]  ; -> 02064CB8
004CA458  subss    xmm0, dword ptr [rip + 0x1b9a848]  ; -> 02064CA8
004CA460  movss    dword ptr [rip + 0x1b9a88c], xmm1  ; -> 02064CF4
004CA468  movss    dword ptr [rip + 0x1b9a888], xmm0  ; -> 02064CF8
004CA470  call     0x22cc20  ; -> 0022CC20 fn
004CA475  movss    xmm0, dword ptr [rip + 0x1b9a823]  ; -> 02064CA0
004CA47D  subss    xmm0, dword ptr [rip + 0x1b9a83b]  ; -> 02064CC0
004CA485  movsx    eax, word ptr [rip + 0x1b9a934]  ; -> 02064DC0
004CA48C  movss    xmm1, dword ptr [rip + 0x1b9a810]  ; -> 02064CA4
004CA494  add      eax, 0x190
004CA499  subss    xmm1, dword ptr [rip + 0x1b9a823]  ; -> 02064CC4
004CA4A1  shl      eax, 4
004CA4A4  movss    dword ptr [rip + 0x1b9a854], xmm0  ; -> 02064D00
004CA4AC  movss    xmm0, dword ptr [rip + 0x1b9a7f4]  ; -> 02064CA8
004CA4B4  subss    xmm0, dword ptr [rip + 0x1b9a80c]  ; -> 02064CC8
004CA4BC  cdqe     
004CA4BE  movss    dword ptr [rip + 0x1b9a83e], xmm1  ; -> 02064D04
004CA4C6  movzx    eax, word ptr [rax + rbx + 0xc]
004CA4CB  movss    dword ptr [rip + 0x1b9a835], xmm0  ; -> 02064D08
004CA4D3  mov      word ptr [rip + 0x1b9a8ee], ax  ; -> 02064DC8
004CA4DA  call     0x22cc20  ; -> 0022CC20 fn
004CA4DF  movups   xmm3, xmmword ptr [rip + 0x1b9a80a]  ; -> 02064CF0
004CA4E6  movsx    esi, word ptr [rip + 0x1b9a8d7]  ; -> 02064DC4
004CA4ED  movups   xmm2, xmmword ptr [rip + 0x1b9a80c]  ; -> 02064D00
004CA4F4  movsx    edx, word ptr [rip + 0x1b9a8cd]  ; -> 02064DC8
004CA4FB  mov      r8d, esi
004CA4FE  movss    xmm13, dword ptr [rip + 0x1b9a801]  ; -> 02064D08
004CA507  movaps   xmm0, xmm3
004CA50A  movsx    ebp, word ptr [rip + 0x1b9a8af]  ; -> 02064DC0
004CA511  lea      eax, [rsi + 0x190]
004CA517  movss    xmm12, dword ptr [rip + 0x1b9a7e4]  ; -> 02064D04
004CA520  movaps   xmm1, xmm3
004CA523  shufps   xmm0, xmm3, 0x55
004CA527  movaps   xmm11, xmm3
004CA52B  mulss    xmm13, xmm0
004CA530  movaps   xmm0, xmm2
004CA533  shl      eax, 4
004CA536  movsxd   rcx, eax
004CA539  lea      eax, [rbp + 0x1f4]
004CA53F  shufps   xmm1, xmm3, 0xaa
004CA543  shufps   xmm0, xmm2, 0x55
004CA547  shl      eax, 4
004CA54A  movzx    r9d, word ptr [rcx + rbx + 0xc]
004CA550  shufps   xmm11, xmm3, 0xaa
004CA555  or       r9w, dx
004CA559  mulss    xmm11, dword ptr [rip + 0x1b9a79e]  ; -> 02064D00
004CA562  cdqe     
004CA564  mulss    xmm12, xmm3
004CA569  movss    dword ptr [rip + 0x1b9a77f], xmm3  ; -> 02064CF0
004CA571  movsx    edx, word ptr [rax + rbx + 0xc]
004CA576  lea      eax, [rsi + 0x1f4]
004CA57C  movups   xmmword ptr [rsp + 0x170], xmm3
004CA584  shl      eax, 4
004CA587  movss    dword ptr [rip + 0x1b9a769], xmm1  ; -> 02064CF8
004CA58F  or       r9w, dx
004CA593  mulss    xmm1, xmm0
004CA597  movaps   xmm0, xmm2
004CA59A  movsxd   rcx, eax
004CA59D  shufps   xmm0, xmm2, 0xaa
004CA5A1  mulss    xmm0, xmm3
004CA5A5  mov      word ptr [rip + 0x1b9a81c], dx  ; -> 02064DC8
004CA5AC  movsx    r8d, word ptr [rcx + rbx + 0xc]
004CA5B2  shufps   xmm3, xmm3, 0x55
004CA5B6  movss    dword ptr [rip + 0x1b9a736], xmm3  ; -> 02064CF4
004CA5BE  mulss    xmm3, xmm2
004CA5C2  mov      word ptr [rip + 0x1b9a802], r8w  ; -> 02064DCC
004CA5CA  movss    dword ptr [rip + 0x1b9a54d], xmm13  ; -> 02064B20
004CA5D3  subss    xmm13, xmm1
004CA5D8  movss    dword ptr [rip + 0x1b9a543], xmm11  ; -> 02064B24
004CA5E1  subss    xmm11, xmm0
004CA5E6  movss    dword ptr [rip + 0x1b9a539], xmm12  ; -> 02064B28
004CA5EF  subss    xmm12, xmm3
004CA5F4  movups   xmmword ptr [rsp + 0x160], xmm2
004CA5FC  movss    dword ptr [rip + 0x1b9a53b], xmm13  ; -> 02064B40
004CA605  movss    dword ptr [rip + 0x1b9a536], xmm11  ; -> 02064B44
004CA60E  movss    dword ptr [rip + 0x1b9a531], xmm12  ; -> 02064B48
004CA617  movzx    edi, word ptr [rip + 0x1b9a4ee]  ; -> 02064B0C
004CA61E  or       r9w, r8w
004CA622  mov      word ptr [rip + 0x1b9a7a6], r9w  ; -> 02064DD0
004CA62A  cmp      r9w, di
004CA62E  jne      0x4ca896  ; -> 004CA896
004CA634  movss    xmm9, dword ptr [rip + 0x19381ff]  ; -> 01E0283C [f32 1]
004CA63D  lea      rcx, [rip + 0x1b9a4bc]  ; -> 02064B00
004CA644  movaps   xmm1, xmm13
004CA648  movaps   xmm0, xmm11
004CA64C  mulss    xmm1, xmm13
004CA651  movaps   xmm2, xmm12
004CA655  mulss    xmm2, xmm12
004CA65A  mulss    xmm1, xmm9
004CA65F  mulss    xmm0, xmm11
004CA664  mulss    xmm2, xmm9
004CA669  mulss    xmm0, xmm9
004CA66E  addss    xmm1, xmm0
004CA672  addss    xmm2, xmm1
004CA676  movaps   xmm1, xmm9
004CA67A  movss    dword ptr [rip + 0x1b9a4da], xmm2  ; -> 02064B5C
004CA682  call     0x4cf350  ; -> 004CF350 fn
004CA687  movss    xmm0, dword ptr [rip + 0x1b9a471]  ; -> 02064B00
004CA68F  lea      rcx, [rip + 0x1b9a46a]  ; -> 02064B00
004CA696  movaps   xmm8, xmm13
004CA69A  movaps   xmm7, xmm11
004CA69E  mulss    xmm8, xmm0
004CA6A3  movaps   xmm6, xmm12
004CA6A7  mulss    xmm6, xmm0
004CA6AB  mulss    xmm7, xmm0
004CA6AF  movaps   xmm1, xmm8
004CA6B3  mulss    xmm1, xmm8
004CA6B8  mulss    xmm13, xmm0
004CA6BD  mulss    xmm11, xmm0
004CA6C2  mulss    xmm12, xmm0
004CA6C7  movaps   xmm0, xmm7
004CA6CA  movss    dword ptr [rip + 0x1b9a4ce], xmm1  ; -> 02064BA0
004CA6D2  mulss    xmm0, xmm7
004CA6D6  mulss    xmm1, xmm9
004CA6DB  mulss    xmm6, xmm9
004CA6E0  movss    dword ptr [rip + 0x1b9a4bc], xmm0  ; -> 02064BA4
004CA6E8  mulss    xmm0, xmm9
004CA6ED  movaps   xmm2, xmm6
004CA6F0  mulss    xmm2, xmm6
004CA6F4  addss    xmm1, xmm0
004CA6F8  movss    dword ptr [rip + 0x1b9a4a8], xmm2  ; -> 02064BA8
004CA700  mulss    xmm2, xmm9
004CA705  addss    xmm2, xmm1
004CA709  movaps   xmm1, xmm9
004CA70D  movss    dword ptr [rip + 0x1b9a497], xmm2  ; -> 02064BAC
004CA715  call     0x4cf350  ; -> 004CF350 fn
004CA71A  movups   xmm0, xmmword ptr [rip + 0x1b9a50f]  ; -> 02064C30
004CA721  movaps   xmm1, xmm11
004CA725  movaps   xmm5, xmm13
004CA729  mulss    xmm1, dword ptr [rip + 0x1b9a517]  ; -> 02064C48
004CA731  shufps   xmm5, xmm5, 0
004CA735  mulps    xmm5, xmm0
004CA738  movaps   xmm0, xmm11
004CA73C  mulss    xmm0, dword ptr [rip + 0x1b9a4fc]  ; -> 02064C40
004CA744  movups   xmmword ptr [rip + 0x1b9a3d5], xmm5  ; -> 02064B20
004CA74B  movss    xmm2, dword ptr [rip + 0x1b9a3d1]  ; -> 02064B24
004CA753  addss    xmm5, xmm0
004CA757  movss    xmm3, dword ptr [rip + 0x1b9a3c9]  ; -> 02064B28
004CA75F  movaps   xmm0, xmm11
004CA763  mulss    xmm0, dword ptr [rip + 0x1b9a4d9]  ; -> 02064C44
004CA76B  addss    xmm3, xmm1
004CA76F  movss    xmm4, dword ptr [rip + 0x1b9a3b5]  ; -> 02064B2C
004CA777  movaps   xmm1, xmm12
004CA77B  mulss    xmm11, dword ptr [rip + 0x1b9a4c8]  ; -> 02064C4C
004CA784  mulss    xmm1, dword ptr [rip + 0x1b9a4c8]  ; -> 02064C54
004CA78C  addss    xmm2, xmm0
004CA790  movaps   xmm0, xmm12
004CA794  movss    dword ptr [rip + 0x1b9a384], xmm5  ; -> 02064B20
004CA79C  mulss    xmm0, dword ptr [rip + 0x1b9a4ac]  ; -> 02064C50
004CA7A4  addss    xmm4, xmm11
004CA7A9  addss    xmm1, xmm2
004CA7AD  movss    dword ptr [rip + 0x1b9a36f], xmm2  ; -> 02064B24
004CA7B5  movss    dword ptr [rip + 0x1b9a36b], xmm3  ; -> 02064B28
004CA7BD  addss    xmm0, xmm5
004CA7C1  movss    dword ptr [rip + 0x1b9a363], xmm4  ; -> 02064B2C
004CA7C9  movss    dword ptr [rip + 0x1b9a373], xmm1  ; -> 02064B44
004CA7D1  movss    dword ptr [rip + 0x1b9a367], xmm0  ; -> 02064B40
004CA7D9  movaps   xmm0, xmm12
004CA7DD  mulss    xmm0, dword ptr [rip + 0x1b9a473]  ; -> 02064C58
004CA7E5  mulss    xmm12, dword ptr [rip + 0x1b9a46e]  ; -> 02064C5C
004CA7EE  addss    xmm0, xmm3
004CA7F2  movss    dword ptr [rip + 0x1b9a34e], xmm0  ; -> 02064B48
004CA7FA  movsx    r8d, word ptr [rip + 0x1b9a5de]  ; -> 02064DE0
004CA802  addss    xmm12, xmm4
004CA807  movss    xmm0, dword ptr [rip + 0x1b9a2f1]  ; -> 02064B00
004CA80F  mulss    xmm8, xmm0
004CA814  mulss    xmm7, xmm0
004CA818  lea      eax, [r8 + 0x12c]
004CA81F  shl      eax, 4
004CA822  movsxd   rcx, eax
004CA825  mulss    xmm6, xmm0
004CA829  movzx    eax, bp
004CA82C  movss    dword ptr [rip + 0x1b9a317], xmm12  ; -> 02064B4C
004CA835  movups   xmm0, xmmword ptr [rip + 0x1b9a304]  ; -> 02064B40
004CA83C  mov      dword ptr [rcx + rbx], eax
004CA83F  movzx    eax, si
004CA842  mov      dword ptr [rbx + rcx + 4], eax
004CA846  lea      eax, [r8 + 0x15e]
004CA84D  shl      eax, 4
004CA850  movsxd   rcx, eax
004CA853  lea      eax, [r8 + 0x177]
004CA85A  shl      eax, 4
004CA85D  movss    dword ptr [rip + 0x1b9a2ea], xmm8  ; -> 02064B50
004CA866  inc      r8w
004CA86A  movss    dword ptr [rip + 0x1b9a2e2], xmm7  ; -> 02064B54
004CA872  movups   xmmword ptr [rcx + rbx], xmm0
004CA876  movsxd   rcx, eax
004CA879  movss    dword ptr [rip + 0x1b9a2d7], xmm6  ; -> 02064B58
004CA881  movups   xmm0, xmmword ptr [rip + 0x1b9a2c8]  ; -> 02064B50
004CA888  mov      word ptr [rip + 0x1b9a550], r8w  ; -> 02064DE0
004CA890  movups   xmmword ptr [rcx + rbx], xmm0
004CA894  jmp      0x4ca89f  ; -> 004CA89F
004CA896  movss    xmm9, dword ptr [rip + 0x1937f9d]  ; -> 01E0283C [f32 1]
004CA89F  movsx    eax, word ptr [rip + 0x1b9a532]  ; -> 02064DD8
004CA8A6  lea      ecx, [rdi + 2]
004CA8A9  and      cx, word ptr [rip + 0x1b9a50c]  ; -> 02064DBC
004CA8B0  add      eax, 0x96
004CA8B5  shl      eax, 4
004CA8B8  movsxd   rdx, eax
004CA8BB  movzx    r8d, word ptr [rdx + rbx + 8]
004CA8C1  mov      word ptr [rip + 0x1b9a4fb], r8w  ; -> 02064DC4
004CA8C9  cmp      cx, di
004CA8CC  je       0x4caf98  ; -> 004CAF98
004CA8D2  movsx    eax, word ptr [rdx + rbx + 4]
004CA8D7  mov      word ptr [rip + 0x1b9a4e2], ax  ; -> 02064DC0
004CA8DE  mov      edx, eax
004CA8E0  add      eax, 0x190
004CA8E5  shl      eax, 4
004CA8E8  movsxd   rcx, eax
004CA8EB  movsx    eax, r8w
004CA8EF  add      eax, 0x190
004CA8F4  shl      eax, 4
004CA8F7  movups   xmm3, xmmword ptr [rcx + rbx]
004CA8FB  cdqe     
004CA8FD  movups   xmmword ptr [rip + 0x1b9a39c], xmm3  ; -> 02064CA0
004CA904  movups   xmm2, xmmword ptr [rax + rbx]
004CA908  lea      eax, [rdx + 0x1f4]
004CA90E  shl      eax, 4
004CA911  movups   xmmword ptr [rip + 0x1b9a398], xmm2  ; -> 02064CB0
004CA918  movsxd   rcx, eax
004CA91B  movaps   xmm1, xmm2
004CA91E  movss    dword ptr [rip + 0x1b9a38a], xmm2  ; -> 02064CB0
004CA926  shufps   xmm1, xmm2, 0x55
004CA92A  movss    dword ptr [rip + 0x1b9a382], xmm1  ; -> 02064CB4
004CA932  movups   xmm0, xmmword ptr [rcx + rbx]
004CA936  movups   xmmword ptr [rip + 0x1b9a383], xmm0  ; -> 02064CC0
004CA93D  movaps   xmm0, xmm2
004CA940  shufps   xmm2, xmm2, 0xaa
004CA944  subss    xmm0, xmm3
004CA948  movss    dword ptr [rip + 0x1b9a368], xmm2  ; -> 02064CB8
004CA950  movss    dword ptr [rip + 0x1b9a398], xmm0  ; -> 02064CF0
004CA958  movaps   xmm0, xmm3
004CA95B  shufps   xmm0, xmm3, 0x55
004CA95F  shufps   xmm3, xmm3, 0xaa
004CA963  subss    xmm1, xmm0
004CA967  subss    xmm2, xmm3
004CA96B  movss    dword ptr [rip + 0x1b9a381], xmm1  ; -> 02064CF4
004CA973  movss    dword ptr [rip + 0x1b9a37d], xmm2  ; -> 02064CF8
004CA97B  call     0x22cc20  ; -> 0022CC20 fn
004CA980  movss    xmm0, dword ptr [rip + 0x1b9a318]  ; -> 02064CA0
004CA988  subss    xmm0, dword ptr [rip + 0x1b9a330]  ; -> 02064CC0
004CA990  movss    xmm1, dword ptr [rip + 0x1b9a30c]  ; -> 02064CA4
004CA998  subss    xmm1, dword ptr [rip + 0x1b9a324]  ; -> 02064CC4
004CA9A0  movss    dword ptr [rip + 0x1b9a358], xmm0  ; -> 02064D00
004CA9A8  movss    xmm0, dword ptr [rip + 0x1b9a2f8]  ; -> 02064CA8
004CA9B0  subss    xmm0, dword ptr [rip + 0x1b9a310]  ; -> 02064CC8
004CA9B8  movss    dword ptr [rip + 0x1b9a344], xmm1  ; -> 02064D04
004CA9C0  movss    dword ptr [rip + 0x1b9a340], xmm0  ; -> 02064D08
004CA9C8  call     0x22cc20  ; -> 0022CC20 fn
004CA9CD  movups   xmm6, xmmword ptr [rip + 0x1b9a31c]  ; -> 02064CF0
004CA9D4  movups   xmm2, xmmword ptr [rip + 0x1b9a325]  ; -> 02064D00
004CA9DB  movss    xmm5, dword ptr [rip + 0x1b9a321]  ; -> 02064D04
004CA9E3  movaps   xmm3, xmm6
004CA9E6  shufps   xmm3, xmm6, 0x55
004CA9EA  movaps   xmm1, xmm2
004CA9ED  mulss    xmm3, dword ptr [rip + 0x1b9a313]  ; -> 02064D08
004CA9F5  movaps   xmm0, xmm6
004CA9F8  shufps   xmm0, xmm6, 0xaa
004CA9FC  movaps   xmm4, xmm6
004CA9FF  shufps   xmm1, xmm2, 0x55
004CAA03  mulss    xmm1, xmm0
004CAA07  movss    dword ptr [rip + 0x1b9a2e9], xmm0  ; -> 02064CF8
004CAA0F  movaps   xmm0, xmm2
004CAA12  shufps   xmm4, xmm6, 0xaa
004CAA16  mulss    xmm4, dword ptr [rip + 0x1b9a2e2]  ; -> 02064D00
004CAA1E  mulss    xmm5, xmm6
004CAA22  movss    dword ptr [rip + 0x1b9a0f6], xmm3  ; -> 02064B20
004CAA2A  subss    xmm3, xmm1
004CAA2E  movaps   xmm1, xmm6
004CAA31  shufps   xmm0, xmm2, 0xaa
004CAA35  shufps   xmm1, xmm6, 0x55
004CAA39  movss    dword ptr [rip + 0x1b9a2b3], xmm1  ; -> 02064CF4
004CAA41  mulss    xmm1, xmm2
004CAA45  mulss    xmm0, xmm6
004CAA49  movss    dword ptr [rip + 0x1b9a0d3], xmm4  ; -> 02064B24
004CAA51  movss    dword ptr [rip + 0x1b9a0cf], xmm5  ; -> 02064B28
004CAA59  subss    xmm5, xmm1
004CAA5D  subss    xmm4, xmm0
004CAA61  movss    dword ptr [rip + 0x1b9a0d7], xmm3  ; -> 02064B40
004CAA69  movss    dword ptr [rip + 0x1b9a27f], xmm6  ; -> 02064CF0
004CAA71  movups   xmmword ptr [rsp + 0x150], xmm6
004CAA79  movss    dword ptr [rip + 0x1b9a0c7], xmm5  ; -> 02064B48
004CAA81  movss    dword ptr [rip + 0x1b9a0bb], xmm4  ; -> 02064B44
004CAA89  movups   xmmword ptr [rsp + 0x140], xmm2
004CAA91  lea      r8, [rsp + 0x40]
004CAA96  movdqa   xmmword ptr [rsp + 0x40], xmm6
004CAA9C  lea      rdx, [rip + 0x1b9a25d]  ; -> 02064D00
004CAAA3  lea      rcx, [rip + 0x1b9a066]  ; -> 02064B10
004CAAAA  call     0x4cf280  ; -> 004CF280 fn
004CAAAF  movsx    r8d, word ptr [rip + 0x1b9a309]  ; -> 02064DC0
004CAAB7  movzx    edi, word ptr [rip + 0x1b9a04e]  ; -> 02064B0C
004CAABE  lea      eax, [r8 + 0x258]
004CAAC5  shl      eax, 4
004CAAC8  lea      edx, [rdi + 0x20]
004CAACB  and      dx, word ptr [rip + 0x1b9a03e]  ; -> 02064B10
004CAAD2  movsxd   rcx, eax
004CAAD5  movsx    eax, word ptr [rip + 0x1b9a2e8]  ; -> 02064DC4
004CAADC  add      eax, 0x258
004CAAE1  mov      word ptr [rip + 0x1b9a2e0], dx  ; -> 02064DC8
004CAAE8  shl      eax, 4
004CAAEB  movups   xmm0, xmmword ptr [rcx + rbx]
004CAAEF  cdqe     
004CAAF1  movups   xmmword ptr [rip + 0x1b9a1a8], xmm0  ; -> 02064CA0
004CAAF8  movups   xmm0, xmmword ptr [rax + rbx]
004CAAFC  lea      eax, [r8 + 0x2bc]
004CAB03  shl      eax, 4
004CAB06  movsxd   rcx, eax
004CAB09  movups   xmmword ptr [rip + 0x1b9a1a0], xmm0  ; -> 02064CB0
004CAB10  movups   xmm0, xmmword ptr [rcx + rbx]
004CAB14  movups   xmmword ptr [rip + 0x1b9a1a5], xmm0  ; -> 02064CC0
004CAB1B  cmp      dx, di
004CAB1E  je       0x4caf8f  ; -> 004CAF8F
004CAB24  movss    xmm0, dword ptr [rip + 0x1b9a184]  ; -> 02064CB0
004CAB2C  subss    xmm0, dword ptr [rip + 0x1b9a16c]  ; -> 02064CA0
004CAB34  movss    xmm1, dword ptr [rip + 0x1b9a178]  ; -> 02064CB4
004CAB3C  subss    xmm1, dword ptr [rip + 0x1b9a160]  ; -> 02064CA4
004CAB44  movss    dword ptr [rip + 0x1b9a1a4], xmm0  ; -> 02064CF0
004CAB4C  movss    xmm0, dword ptr [rip + 0x1b9a164]  ; -> 02064CB8
004CAB54  subss    xmm0, dword ptr [rip + 0x1b9a14c]  ; -> 02064CA8
004CAB5C  movss    dword ptr [rip + 0x1b9a190], xmm1  ; -> 02064CF4
004CAB64  movss    dword ptr [rip + 0x1b9a18c], xmm0  ; -> 02064CF8
004CAB6C  call     0x22cc20  ; -> 0022CC20 fn
004CAB71  movss    xmm0, dword ptr [rip + 0x1b9a127]  ; -> 02064CA0
004CAB79  subss    xmm0, dword ptr [rip + 0x1b9a13f]  ; -> 02064CC0
004CAB81  movsx    eax, word ptr [rip + 0x1b9a238]  ; -> 02064DC0
004CAB88  movss    xmm1, dword ptr [rip + 0x1b9a114]  ; -> 02064CA4
004CAB90  add      eax, 0x190
004CAB95  subss    xmm1, dword ptr [rip + 0x1b9a127]  ; -> 02064CC4
004CAB9D  shl      eax, 4
004CABA0  movss    dword ptr [rip + 0x1b9a158], xmm0  ; -> 02064D00
004CABA8  movss    xmm0, dword ptr [rip + 0x1b9a0f8]  ; -> 02064CA8
004CABB0  subss    xmm0, dword ptr [rip + 0x1b9a110]  ; -> 02064CC8
004CABB8  cdqe     
004CABBA  movss    dword ptr [rip + 0x1b9a142], xmm1  ; -> 02064D04
004CABC2  movzx    eax, word ptr [rax + rbx + 0xc]
004CABC7  movss    dword ptr [rip + 0x1b9a139], xmm0  ; -> 02064D08
004CABCF  mov      word ptr [rip + 0x1b9a1f2], ax  ; -> 02064DC8
004CABD6  call     0x22cc20  ; -> 0022CC20 fn
004CABDB  movups   xmm3, xmmword ptr [rip + 0x1b9a10e]  ; -> 02064CF0
004CABE2  movsx    esi, word ptr [rip + 0x1b9a1db]  ; -> 02064DC4
004CABE9  movups   xmm2, xmmword ptr [rip + 0x1b9a110]  ; -> 02064D00
004CABF0  movsx    edx, word ptr [rip + 0x1b9a1d1]  ; -> 02064DC8
004CABF7  mov      r8d, esi
004CABFA  movsx    ebp, word ptr [rip + 0x1b9a1bf]  ; -> 02064DC0
004CAC01  movaps   xmm0, xmm3
004CAC04  movss    xmm12, dword ptr [rip + 0x1b9a0f7]  ; -> 02064D04
004CAC0D  lea      eax, [rsi + 0x190]
004CAC13  shl      eax, 4
004CAC16  movaps   xmm13, xmm3
004CAC1A  movsxd   rcx, eax
004CAC1D  movaps   xmm11, xmm3
004CAC21  shufps   xmm0, xmm3, 0xaa
004CAC25  lea      eax, [rbp + 0x1f4]
004CAC2B  shl      eax, 4
004CAC2E  movaps   xmm1, xmm2
004CAC31  shufps   xmm13, xmm3, 0x55
004CAC36  movzx    r9d, word ptr [rcx + rbx + 0xc]
004CAC3C  mulss    xmm13, dword ptr [rip + 0x1b9a0c3]  ; -> 02064D08
004CAC45  or       r9w, dx
004CAC49  cdqe     
004CAC4B  shufps   xmm11, xmm3, 0xaa
004CAC50  mulss    xmm11, dword ptr [rip + 0x1b9a0a7]  ; -> 02064D00
004CAC59  movsx    edx, word ptr [rax + rbx + 0xc]
004CAC5E  lea      eax, [rsi + 0x1f4]
004CAC64  mulss    xmm12, xmm3
004CAC69  or       r9w, dx
004CAC6D  shl      eax, 4
004CAC70  movss    dword ptr [rip + 0x1b9a080], xmm0  ; -> 02064CF8
004CAC78  movss    dword ptr [rip + 0x1b9a070], xmm3  ; -> 02064CF0
004CAC80  movups   xmmword ptr [rsp + 0x130], xmm3
004CAC88  movsxd   rcx, eax
004CAC8B  shufps   xmm1, xmm2, 0x55
004CAC8F  mulss    xmm1, xmm0
004CAC93  movaps   xmm0, xmm2
004CAC96  mov      word ptr [rip + 0x1b9a12b], dx  ; -> 02064DC8
004CAC9D  movsx    r8d, word ptr [rcx + rbx + 0xc]
004CACA3  shufps   xmm0, xmm2, 0xaa
004CACA7  or       r9w, r8w
004CACAB  mulss    xmm0, xmm3
004CACAF  mov      word ptr [rip + 0x1b9a115], r8w  ; -> 02064DCC
004CACB7  shufps   xmm3, xmm3, 0x55
004CACBB  movss    dword ptr [rip + 0x1b9a031], xmm3  ; -> 02064CF4
004CACC3  mulss    xmm3, xmm2
004CACC7  movss    dword ptr [rip + 0x1b99e50], xmm13  ; -> 02064B20
004CACD0  subss    xmm13, xmm1
004CACD5  movss    dword ptr [rip + 0x1b99e46], xmm11  ; -> 02064B24
004CACDE  subss    xmm11, xmm0
004CACE3  movss    dword ptr [rip + 0x1b99e3c], xmm12  ; -> 02064B28
004CACEC  subss    xmm12, xmm3
004CACF1  movups   xmmword ptr [rsp + 0x120], xmm2
004CACF9  movss    dword ptr [rip + 0x1b99e3e], xmm13  ; -> 02064B40
004CAD02  movss    dword ptr [rip + 0x1b99e39], xmm11  ; -> 02064B44
004CAD0B  movss    dword ptr [rip + 0x1b99e34], xmm12  ; -> 02064B48
004CAD14  movzx    edi, word ptr [rip + 0x1b99df1]  ; -> 02064B0C
004CAD1B  mov      word ptr [rip + 0x1b9a0ad], r9w  ; -> 02064DD0
004CAD23  cmp      r9w, di
004CAD27  jne      0x4caf8f  ; -> 004CAF8F
004CAD2D  movss    xmm9, dword ptr [rip + 0x1937b06]  ; -> 01E0283C [f32 1]
004CAD36  lea      rcx, [rip + 0x1b99dc3]  ; -> 02064B00
004CAD3D  movaps   xmm1, xmm13
004CAD41  movaps   xmm0, xmm11
004CAD45  mulss    xmm1, xmm13
004CAD4A  movaps   xmm2, xmm12
004CAD4E  mulss    xmm2, xmm12
004CAD53  mulss    xmm1, xmm9
004CAD58  mulss    xmm0, xmm11
004CAD5D  mulss    xmm2, xmm9
004CAD62  mulss    xmm0, xmm9
004CAD67  addss    xmm1, xmm0
004CAD6B  addss    xmm2, xmm1
004CAD6F  movaps   xmm1, xmm9
004CAD73  movss    dword ptr [rip + 0x1b99de1], xmm2  ; -> 02064B5C
004CAD7B  call     0x4cf350  ; -> 004CF350 fn
004CAD80  movss    xmm0, dword ptr [rip + 0x1b99d78]  ; -> 02064B00
004CAD88  lea      rcx, [rip + 0x1b99d71]  ; -> 02064B00
004CAD8F  movaps   xmm8, xmm13
004CAD93  movaps   xmm7, xmm11
004CAD97  mulss    xmm8, xmm0
004CAD9C  movaps   xmm6, xmm12
004CADA0  mulss    xmm6, xmm0
004CADA4  mulss    xmm7, xmm0
004CADA8  movaps   xmm1, xmm8
004CADAC  mulss    xmm1, xmm8
004CADB1  mulss    xmm13, xmm0
004CADB6  mulss    xmm11, xmm0
004CADBB  mulss    xmm12, xmm0
004CADC0  movaps   xmm0, xmm7
004CADC3  movss    dword ptr [rip + 0x1b99dd5], xmm1  ; -> 02064BA0
004CADCB  mulss    xmm0, xmm7
004CADCF  mulss    xmm1, xmm9
004CADD4  mulss    xmm6, xmm9
004CADD9  movss    dword ptr [rip + 0x1b99dc3], xmm0  ; -> 02064BA4
004CADE1  mulss    xmm0, xmm9
004CADE6  movaps   xmm2, xmm6
004CADE9  mulss    xmm2, xmm6
004CADED  addss    xmm1, xmm0
004CADF1  movss    dword ptr [rip + 0x1b99daf], xmm2  ; -> 02064BA8
004CADF9  mulss    xmm2, xmm9
004CADFE  addss    xmm2, xmm1
004CAE02  movaps   xmm1, xmm9
004CAE06  movss    dword ptr [rip + 0x1b99d9e], xmm2  ; -> 02064BAC
004CAE0E  call     0x4cf350  ; -> 004CF350 fn
004CAE13  movups   xmm0, xmmword ptr [rip + 0x1b99e16]  ; -> 02064C30
004CAE1A  movaps   xmm1, xmm11
004CAE1E  movaps   xmm5, xmm13
004CAE22  mulss    xmm1, dword ptr [rip + 0x1b99e1e]  ; -> 02064C48
004CAE2A  shufps   xmm5, xmm5, 0
004CAE2E  mulps    xmm5, xmm0
004CAE31  movaps   xmm0, xmm11
004CAE35  mulss    xmm0, dword ptr [rip + 0x1b99e03]  ; -> 02064C40
004CAE3D  movups   xmmword ptr [rip + 0x1b99cdc], xmm5  ; -> 02064B20
004CAE44  movss    xmm2, dword ptr [rip + 0x1b99cd8]  ; -> 02064B24
004CAE4C  addss    xmm5, xmm0
004CAE50  movss    xmm3, dword ptr [rip + 0x1b99cd0]  ; -> 02064B28
004CAE58  movaps   xmm0, xmm11
004CAE5C  mulss    xmm0, dword ptr [rip + 0x1b99de0]  ; -> 02064C44
004CAE64  addss    xmm3, xmm1
004CAE68  movss    xmm4, dword ptr [rip + 0x1b99cbc]  ; -> 02064B2C
004CAE70  movaps   xmm1, xmm12
004CAE74  mulss    xmm11, dword ptr [rip + 0x1b99dcf]  ; -> 02064C4C
004CAE7D  mulss    xmm1, dword ptr [rip + 0x1b99dcf]  ; -> 02064C54
004CAE85  addss    xmm2, xmm0
004CAE89  movaps   xmm0, xmm12
004CAE8D  movss    dword ptr [rip + 0x1b99c8b], xmm5  ; -> 02064B20
004CAE95  mulss    xmm0, dword ptr [rip + 0x1b99db3]  ; -> 02064C50
004CAE9D  addss    xmm4, xmm11
004CAEA2  addss    xmm1, xmm2
004CAEA6  movss    dword ptr [rip + 0x1b99c76], xmm2  ; -> 02064B24
004CAEAE  movss    dword ptr [rip + 0x1b99c72], xmm3  ; -> 02064B28
004CAEB6  addss    xmm0, xmm5
004CAEBA  movss    dword ptr [rip + 0x1b99c6a], xmm4  ; -> 02064B2C
004CAEC2  movss    dword ptr [rip + 0x1b99c7a], xmm1  ; -> 02064B44
004CAECA  movss    dword ptr [rip + 0x1b99c6e], xmm0  ; -> 02064B40
004CAED2  movaps   xmm0, xmm12
004CAED6  mulss    xmm0, dword ptr [rip + 0x1b99d7a]  ; -> 02064C58
004CAEDE  mulss    xmm12, dword ptr [rip + 0x1b99d75]  ; -> 02064C5C
004CAEE7  addss    xmm0, xmm3
004CAEEB  movss    dword ptr [rip + 0x1b99c55], xmm0  ; -> 02064B48
004CAEF3  movsx    r8d, word ptr [rip + 0x1b99ee5]  ; -> 02064DE0
004CAEFB  addss    xmm12, xmm4
004CAF00  movss    xmm0, dword ptr [rip + 0x1b99bf8]  ; -> 02064B00
004CAF08  mulss    xmm8, xmm0
004CAF0D  mulss    xmm7, xmm0
004CAF11  lea      eax, [r8 + 0x12c]
004CAF18  shl      eax, 4
004CAF1B  movsxd   rcx, eax
004CAF1E  mulss    xmm6, xmm0
004CAF22  movzx    eax, bp
004CAF25  movss    dword ptr [rip + 0x1b99c1e], xmm12  ; -> 02064B4C
004CAF2E  movups   xmm0, xmmword ptr [rip + 0x1b99c0b]  ; -> 02064B40
004CAF35  mov      dword ptr [rcx + rbx], eax
004CAF38  movzx    eax, si
004CAF3B  mov      dword ptr [rbx + rcx + 4], eax
004CAF3F  lea      eax, [r8 + 0x15e]
004CAF46  shl      eax, 4
004CAF49  movsxd   rcx, eax
004CAF4C  lea      eax, [r8 + 0x177]
004CAF53  shl      eax, 4
004CAF56  movss    dword ptr [rip + 0x1b99bf1], xmm8  ; -> 02064B50
004CAF5F  inc      r8w
004CAF63  movss    dword ptr [rip + 0x1b99be9], xmm7  ; -> 02064B54
004CAF6B  movups   xmmword ptr [rcx + rbx], xmm0
004CAF6F  movsxd   rcx, eax
004CAF72  movss    dword ptr [rip + 0x1b99bde], xmm6  ; -> 02064B58
004CAF7A  movups   xmm0, xmmword ptr [rip + 0x1b99bcf]  ; -> 02064B50
004CAF81  mov      word ptr [rip + 0x1b99e57], r8w  ; -> 02064DE0
004CAF89  movups   xmmword ptr [rcx + rbx], xmm0
004CAF8D  jmp      0x4caf98  ; -> 004CAF98
004CAF8F  movss    xmm9, dword ptr [rip + 0x19378a4]  ; -> 01E0283C [f32 1]
004CAF98  movsx    eax, word ptr [rip + 0x1b99e39]  ; -> 02064DD8
004CAF9F  lea      ecx, [rdi + 4]
004CAFA2  and      cx, word ptr [rip + 0x1b99e13]  ; -> 02064DBC
004CAFA9  add      eax, 0x96
004CAFAE  shl      eax, 4
004CAFB1  movsxd   rdx, eax
004CAFB4  mov      word ptr [rip + 0x1b99e05], cx  ; -> 02064DC0
004CAFBB  movzx    r8d, word ptr [rdx + rbx]
004CAFC0  mov      word ptr [rip + 0x1b99dfc], r8w  ; -> 02064DC4
004CAFC8  cmp      cx, di
004CAFCB  je       0x4cb697  ; -> 004CB697
004CAFD1  movsx    eax, word ptr [rdx + rbx + 8]
004CAFD6  mov      word ptr [rip + 0x1b99de3], ax  ; -> 02064DC0
004CAFDD  mov      edx, eax
004CAFDF  add      eax, 0x190
004CAFE4  shl      eax, 4
004CAFE7  movsxd   rcx, eax
004CAFEA  movsx    eax, r8w
004CAFEE  add      eax, 0x190
004CAFF3  shl      eax, 4
004CAFF6  movups   xmm3, xmmword ptr [rcx + rbx]
004CAFFA  cdqe     
004CAFFC  movups   xmmword ptr [rip + 0x1b99c9d], xmm3  ; -> 02064CA0
004CB003  movups   xmm2, xmmword ptr [rax + rbx]
004CB007  lea      eax, [rdx + 0x1f4]
004CB00D  shl      eax, 4
004CB010  movups   xmmword ptr [rip + 0x1b99c99], xmm2  ; -> 02064CB0
004CB017  movsxd   rcx, eax
004CB01A  movaps   xmm1, xmm2
004CB01D  movss    dword ptr [rip + 0x1b99c8b], xmm2  ; -> 02064CB0
004CB025  shufps   xmm1, xmm2, 0x55
004CB029  movss    dword ptr [rip + 0x1b99c83], xmm1  ; -> 02064CB4
004CB031  movups   xmm0, xmmword ptr [rcx + rbx]
004CB035  movups   xmmword ptr [rip + 0x1b99c84], xmm0  ; -> 02064CC0
004CB03C  movaps   xmm0, xmm2
004CB03F  shufps   xmm2, xmm2, 0xaa
004CB043  subss    xmm0, xmm3
004CB047  movss    dword ptr [rip + 0x1b99c69], xmm2  ; -> 02064CB8
004CB04F  movss    dword ptr [rip + 0x1b99c99], xmm0  ; -> 02064CF0
004CB057  movaps   xmm0, xmm3
004CB05A  shufps   xmm0, xmm3, 0x55
004CB05E  shufps   xmm3, xmm3, 0xaa
004CB062  subss    xmm1, xmm0
004CB066  subss    xmm2, xmm3
004CB06A  movss    dword ptr [rip + 0x1b99c82], xmm1  ; -> 02064CF4
004CB072  movss    dword ptr [rip + 0x1b99c7e], xmm2  ; -> 02064CF8
004CB07A  call     0x22cc20  ; -> 0022CC20 fn
004CB07F  movss    xmm0, dword ptr [rip + 0x1b99c19]  ; -> 02064CA0
004CB087  subss    xmm0, dword ptr [rip + 0x1b99c31]  ; -> 02064CC0
004CB08F  movss    xmm1, dword ptr [rip + 0x1b99c0d]  ; -> 02064CA4
004CB097  subss    xmm1, dword ptr [rip + 0x1b99c25]  ; -> 02064CC4
004CB09F  movss    dword ptr [rip + 0x1b99c59], xmm0  ; -> 02064D00
004CB0A7  movss    xmm0, dword ptr [rip + 0x1b99bf9]  ; -> 02064CA8
004CB0AF  subss    xmm0, dword ptr [rip + 0x1b99c11]  ; -> 02064CC8
004CB0B7  movss    dword ptr [rip + 0x1b99c45], xmm1  ; -> 02064D04
004CB0BF  movss    dword ptr [rip + 0x1b99c41], xmm0  ; -> 02064D08
004CB0C7  call     0x22cc20  ; -> 0022CC20 fn
004CB0CC  movups   xmm6, xmmword ptr [rip + 0x1b99c1d]  ; -> 02064CF0
004CB0D3  movups   xmm2, xmmword ptr [rip + 0x1b99c26]  ; -> 02064D00
004CB0DA  movss    xmm5, dword ptr [rip + 0x1b99c22]  ; -> 02064D04
004CB0E2  movaps   xmm3, xmm6
004CB0E5  shufps   xmm3, xmm6, 0x55
004CB0E9  movaps   xmm1, xmm2
004CB0EC  mulss    xmm3, dword ptr [rip + 0x1b99c14]  ; -> 02064D08
004CB0F4  movaps   xmm0, xmm6
004CB0F7  shufps   xmm0, xmm6, 0xaa
004CB0FB  movaps   xmm4, xmm6
004CB0FE  shufps   xmm1, xmm2, 0x55
004CB102  mulss    xmm1, xmm0
004CB106  movss    dword ptr [rip + 0x1b99bea], xmm0  ; -> 02064CF8
004CB10E  movaps   xmm0, xmm2
004CB111  shufps   xmm4, xmm6, 0xaa
004CB115  mulss    xmm4, dword ptr [rip + 0x1b99be3]  ; -> 02064D00
004CB11D  mulss    xmm5, xmm6
004CB121  movss    dword ptr [rip + 0x1b999f7], xmm3  ; -> 02064B20
004CB129  subss    xmm3, xmm1
004CB12D  movaps   xmm1, xmm6
004CB130  shufps   xmm0, xmm2, 0xaa
004CB134  shufps   xmm1, xmm6, 0x55
004CB138  movss    dword ptr [rip + 0x1b99bb4], xmm1  ; -> 02064CF4
004CB140  mulss    xmm1, xmm2
004CB144  mulss    xmm0, xmm6
004CB148  movss    dword ptr [rip + 0x1b999d4], xmm4  ; -> 02064B24
004CB150  movss    dword ptr [rip + 0x1b999d0], xmm5  ; -> 02064B28
004CB158  subss    xmm5, xmm1
004CB15C  subss    xmm4, xmm0
004CB160  movss    dword ptr [rip + 0x1b999d8], xmm3  ; -> 02064B40
004CB168  movss    dword ptr [rip + 0x1b99b80], xmm6  ; -> 02064CF0
004CB170  movups   xmmword ptr [rsp + 0x110], xmm6
004CB178  movss    dword ptr [rip + 0x1b999c8], xmm5  ; -> 02064B48
004CB180  movss    dword ptr [rip + 0x1b999bc], xmm4  ; -> 02064B44
004CB188  movups   xmmword ptr [rsp + 0x100], xmm2
004CB190  lea      r8, [rsp + 0x40]
004CB195  movdqa   xmmword ptr [rsp + 0x40], xmm6
004CB19B  lea      rdx, [rip + 0x1b99b5e]  ; -> 02064D00
004CB1A2  lea      rcx, [rip + 0x1b99967]  ; -> 02064B10
004CB1A9  call     0x4cf280  ; -> 004CF280 fn
004CB1AE  movsx    r9d, word ptr [rip + 0x1b99c0a]  ; -> 02064DC0
004CB1B6  movzx    r8d, word ptr [rip + 0x1b9994e]  ; -> 02064B0C
004CB1BE  lea      eax, [r9 + 0x258]
004CB1C5  shl      eax, 4
004CB1C8  lea      edx, [r8 + 0x20]
004CB1CC  and      dx, word ptr [rip + 0x1b9993d]  ; -> 02064B10
004CB1D3  movsxd   rcx, eax
004CB1D6  movsx    eax, word ptr [rip + 0x1b99be7]  ; -> 02064DC4
004CB1DD  add      eax, 0x258
004CB1E2  mov      word ptr [rip + 0x1b99bdf], dx  ; -> 02064DC8
004CB1E9  shl      eax, 4
004CB1EC  movups   xmm0, xmmword ptr [rcx + rbx]
004CB1F0  cdqe     
004CB1F2  movups   xmmword ptr [rip + 0x1b99aa7], xmm0  ; -> 02064CA0
004CB1F9  movups   xmm0, xmmword ptr [rax + rbx]
004CB1FD  lea      eax, [r9 + 0x2bc]
004CB204  shl      eax, 4
004CB207  movsxd   rcx, eax
004CB20A  movups   xmmword ptr [rip + 0x1b99a9f], xmm0  ; -> 02064CB0
004CB211  movups   xmm0, xmmword ptr [rcx + rbx]
004CB215  movups   xmmword ptr [rip + 0x1b99aa4], xmm0  ; -> 02064CC0
004CB21C  cmp      dx, r8w
004CB220  je       0x4cb68e  ; -> 004CB68E
004CB226  movss    xmm0, dword ptr [rip + 0x1b99a82]  ; -> 02064CB0
004CB22E  subss    xmm0, dword ptr [rip + 0x1b99a6a]  ; -> 02064CA0
004CB236  movss    xmm1, dword ptr [rip + 0x1b99a76]  ; -> 02064CB4
004CB23E  subss    xmm1, dword ptr [rip + 0x1b99a5e]  ; -> 02064CA4
004CB246  movss    dword ptr [rip + 0x1b99aa2], xmm0  ; -> 02064CF0
004CB24E  movss    xmm0, dword ptr [rip + 0x1b99a62]  ; -> 02064CB8
004CB256  subss    xmm0, dword ptr [rip + 0x1b99a4a]  ; -> 02064CA8
004CB25E  movss    dword ptr [rip + 0x1b99a8e], xmm1  ; -> 02064CF4
004CB266  movss    dword ptr [rip + 0x1b99a8a], xmm0  ; -> 02064CF8
004CB26E  call     0x22cc20  ; -> 0022CC20 fn
004CB273  movss    xmm0, dword ptr [rip + 0x1b99a25]  ; -> 02064CA0
004CB27B  subss    xmm0, dword ptr [rip + 0x1b99a3d]  ; -> 02064CC0
004CB283  movsx    eax, word ptr [rip + 0x1b99b36]  ; -> 02064DC0
004CB28A  movss    xmm1, dword ptr [rip + 0x1b99a12]  ; -> 02064CA4
004CB292  add      eax, 0x190
004CB297  subss    xmm1, dword ptr [rip + 0x1b99a25]  ; -> 02064CC4
004CB29F  shl      eax, 4
004CB2A2  movss    dword ptr [rip + 0x1b99a56], xmm0  ; -> 02064D00
004CB2AA  movss    xmm0, dword ptr [rip + 0x1b999f6]  ; -> 02064CA8
004CB2B2  subss    xmm0, dword ptr [rip + 0x1b99a0e]  ; -> 02064CC8
004CB2BA  cdqe     
004CB2BC  movss    dword ptr [rip + 0x1b99a40], xmm1  ; -> 02064D04
004CB2C4  movzx    eax, word ptr [rax + rbx + 0xc]
004CB2C9  movss    dword ptr [rip + 0x1b99a37], xmm0  ; -> 02064D08
004CB2D1  mov      word ptr [rip + 0x1b99af0], ax  ; -> 02064DC8
004CB2D8  call     0x22cc20  ; -> 0022CC20 fn
004CB2DD  movups   xmm3, xmmword ptr [rip + 0x1b99a0c]  ; -> 02064CF0
004CB2E4  movsx    edx, word ptr [rip + 0x1b99add]  ; -> 02064DC8
004CB2EB  movups   xmm2, xmmword ptr [rip + 0x1b99a0e]  ; -> 02064D00
004CB2F2  movsx    edi, word ptr [rip + 0x1b99acb]  ; -> 02064DC4
004CB2F9  movsx    esi, word ptr [rip + 0x1b99ac0]  ; -> 02064DC0
004CB300  movaps   xmm0, xmm3
004CB303  movss    xmm12, dword ptr [rip + 0x1b999f8]  ; -> 02064D04
004CB30C  movaps   xmm13, xmm3
004CB310  shufps   xmm0, xmm3, 0xaa
004CB314  movaps   xmm11, xmm3
004CB318  shufps   xmm13, xmm3, 0x55
004CB31D  lea      eax, [rdi + 0x190]
004CB323  mulss    xmm13, dword ptr [rip + 0x1b999dc]  ; -> 02064D08
004CB32C  movaps   xmm1, xmm2
004CB32F  shl      eax, 4
004CB332  movsxd   rcx, eax
004CB335  lea      eax, [rsi + 0x1f4]
004CB33B  shl      eax, 4
004CB33E  cdqe     
004CB340  shufps   xmm11, xmm3, 0xaa
004CB345  movzx    r9d, word ptr [rcx + rbx + 0xc]
004CB34B  mulss    xmm11, dword ptr [rip + 0x1b999ac]  ; -> 02064D00
004CB354  or       r9w, dx
004CB358  movsx    edx, word ptr [rax + rbx + 0xc]
004CB35D  lea      eax, [rdi + 0x1f4]
004CB363  mulss    xmm12, xmm3
004CB368  or       r9w, dx
004CB36C  shl      eax, 4
004CB36F  movss    dword ptr [rip + 0x1b99981], xmm0  ; -> 02064CF8
004CB377  movss    dword ptr [rip + 0x1b99971], xmm3  ; -> 02064CF0
004CB37F  movups   xmmword ptr [rsp + 0xf0], xmm3
004CB387  movsxd   rcx, eax
004CB38A  shufps   xmm1, xmm2, 0x55
004CB38E  mulss    xmm1, xmm0
004CB392  movaps   xmm0, xmm2
004CB395  mov      word ptr [rip + 0x1b99a2c], dx  ; -> 02064DC8
004CB39C  movsx    r8d, word ptr [rcx + rbx + 0xc]
004CB3A2  shufps   xmm0, xmm2, 0xaa
004CB3A6  mov      eax, r8d
004CB3A9  mulss    xmm0, xmm3
004CB3AD  or       r9w, r8w
004CB3B1  mov      word ptr [rip + 0x1b99a13], r8w  ; -> 02064DCC
004CB3B9  shufps   xmm3, xmm3, 0x55
004CB3BD  movss    dword ptr [rip + 0x1b9992f], xmm3  ; -> 02064CF4
004CB3C5  mulss    xmm3, xmm2
004CB3C9  movss    dword ptr [rip + 0x1b9974e], xmm13  ; -> 02064B20
004CB3D2  subss    xmm13, xmm1
004CB3D7  movss    dword ptr [rip + 0x1b99744], xmm11  ; -> 02064B24
004CB3E0  subss    xmm11, xmm0
004CB3E5  movss    dword ptr [rip + 0x1b9973a], xmm12  ; -> 02064B28
004CB3EE  subss    xmm12, xmm3
004CB3F3  movups   xmmword ptr [rsp + 0x1c0], xmm2
004CB3FB  movss    dword ptr [rip + 0x1b9973c], xmm13  ; -> 02064B40
004CB404  movss    dword ptr [rip + 0x1b99737], xmm11  ; -> 02064B44
004CB40D  movss    dword ptr [rip + 0x1b99732], xmm12  ; -> 02064B48
004CB416  cmp      r9w, word ptr [rip + 0x1b996ee]  ; -> 02064B0C
004CB41E  mov      word ptr [rip + 0x1b999aa], r9w  ; -> 02064DD0
004CB426  jne      0x4cb68e  ; -> 004CB68E
004CB42C  movss    xmm9, dword ptr [rip + 0x1937407]  ; -> 01E0283C [f32 1]
004CB435  lea      rcx, [rip + 0x1b996c4]  ; -> 02064B00
004CB43C  movaps   xmm1, xmm13
004CB440  movaps   xmm0, xmm11
004CB444  mulss    xmm1, xmm13
004CB449  movaps   xmm2, xmm12
004CB44D  mulss    xmm2, xmm12
004CB452  mulss    xmm1, xmm9
004CB457  mulss    xmm0, xmm11
004CB45C  mulss    xmm2, xmm9
004CB461  mulss    xmm0, xmm9
004CB466  addss    xmm1, xmm0
004CB46A  addss    xmm2, xmm1
004CB46E  movaps   xmm1, xmm9
004CB472  movss    dword ptr [rip + 0x1b996e2], xmm2  ; -> 02064B5C
004CB47A  call     0x4cf350  ; -> 004CF350 fn
004CB47F  movss    xmm0, dword ptr [rip + 0x1b99679]  ; -> 02064B00
004CB487  lea      rcx, [rip + 0x1b99672]  ; -> 02064B00
004CB48E  movaps   xmm8, xmm13
004CB492  movaps   xmm7, xmm11
004CB496  mulss    xmm8, xmm0
004CB49B  movaps   xmm6, xmm12
004CB49F  mulss    xmm6, xmm0
004CB4A3  mulss    xmm7, xmm0
004CB4A7  movaps   xmm1, xmm8
004CB4AB  mulss    xmm1, xmm8
004CB4B0  mulss    xmm13, xmm0
004CB4B5  mulss    xmm11, xmm0
004CB4BA  mulss    xmm12, xmm0
004CB4BF  movaps   xmm0, xmm7
004CB4C2  movss    dword ptr [rip + 0x1b996d6], xmm1  ; -> 02064BA0
004CB4CA  mulss    xmm0, xmm7
004CB4CE  mulss    xmm1, xmm9
004CB4D3  mulss    xmm6, xmm9
004CB4D8  movss    dword ptr [rip + 0x1b996c4], xmm0  ; -> 02064BA4
004CB4E0  mulss    xmm0, xmm9
004CB4E5  movaps   xmm2, xmm6
004CB4E8  mulss    xmm2, xmm6
004CB4EC  addss    xmm1, xmm0
004CB4F0  movss    dword ptr [rip + 0x1b996b0], xmm2  ; -> 02064BA8
004CB4F8  mulss    xmm2, xmm9
004CB4FD  addss    xmm2, xmm1
004CB501  movaps   xmm1, xmm9
004CB505  movss    dword ptr [rip + 0x1b9969f], xmm2  ; -> 02064BAC
004CB50D  call     0x4cf350  ; -> 004CF350 fn
004CB512  movups   xmm0, xmmword ptr [rip + 0x1b99717]  ; -> 02064C30
004CB519  movaps   xmm1, xmm11
004CB51D  movaps   xmm5, xmm13
004CB521  mulss    xmm1, dword ptr [rip + 0x1b9971f]  ; -> 02064C48
004CB529  shufps   xmm5, xmm5, 0
004CB52D  mulps    xmm5, xmm0
004CB530  movaps   xmm0, xmm11
004CB534  mulss    xmm0, dword ptr [rip + 0x1b99704]  ; -> 02064C40
004CB53C  movups   xmmword ptr [rip + 0x1b995dd], xmm5  ; -> 02064B20
004CB543  movss    xmm2, dword ptr [rip + 0x1b995d9]  ; -> 02064B24
004CB54B  addss    xmm5, xmm0
004CB54F  movss    xmm3, dword ptr [rip + 0x1b995d1]  ; -> 02064B28
004CB557  movaps   xmm0, xmm11
004CB55B  mulss    xmm0, dword ptr [rip + 0x1b996e1]  ; -> 02064C44
004CB563  addss    xmm3, xmm1
004CB567  movss    xmm4, dword ptr [rip + 0x1b995bd]  ; -> 02064B2C
004CB56F  movaps   xmm1, xmm12
004CB573  mulss    xmm11, dword ptr [rip + 0x1b996d0]  ; -> 02064C4C
004CB57C  mulss    xmm1, dword ptr [rip + 0x1b996d0]  ; -> 02064C54
004CB584  addss    xmm2, xmm0
004CB588  movaps   xmm0, xmm12
004CB58C  movss    dword ptr [rip + 0x1b9958c], xmm5  ; -> 02064B20
004CB594  mulss    xmm0, dword ptr [rip + 0x1b996b4]  ; -> 02064C50
004CB59C  addss    xmm4, xmm11
004CB5A1  addss    xmm1, xmm2
004CB5A5  movss    dword ptr [rip + 0x1b99577], xmm2  ; -> 02064B24
004CB5AD  movss    dword ptr [rip + 0x1b99573], xmm3  ; -> 02064B28
004CB5B5  addss    xmm0, xmm5
004CB5B9  movss    dword ptr [rip + 0x1b9956b], xmm4  ; -> 02064B2C
004CB5C1  movss    dword ptr [rip + 0x1b9957b], xmm1  ; -> 02064B44
004CB5C9  movss    dword ptr [rip + 0x1b9956f], xmm0  ; -> 02064B40
004CB5D1  movaps   xmm0, xmm12
004CB5D5  mulss    xmm0, dword ptr [rip + 0x1b9967b]  ; -> 02064C58
004CB5DD  mulss    xmm12, dword ptr [rip + 0x1b99676]  ; -> 02064C5C
004CB5E6  addss    xmm0, xmm3
004CB5EA  movss    dword ptr [rip + 0x1b99556], xmm0  ; -> 02064B48
004CB5F2  movsx    r8d, word ptr [rip + 0x1b997e6]  ; -> 02064DE0
004CB5FA  addss    xmm12, xmm4
004CB5FF  movss    xmm0, dword ptr [rip + 0x1b994f9]  ; -> 02064B00
004CB607  mulss    xmm8, xmm0
004CB60C  mulss    xmm7, xmm0
004CB610  lea      eax, [r8 + 0x12c]
004CB617  shl      eax, 4
004CB61A  movsxd   rcx, eax
004CB61D  mulss    xmm6, xmm0
004CB621  movzx    eax, si
004CB624  movss    dword ptr [rip + 0x1b9951f], xmm12  ; -> 02064B4C
004CB62D  movups   xmm0, xmmword ptr [rip + 0x1b9950c]  ; -> 02064B40
004CB634  mov      dword ptr [rcx + rbx], eax
004CB637  movzx    eax, di
004CB63A  mov      dword ptr [rbx + rcx + 4], eax
004CB63E  lea      eax, [r8 + 0x15e]
004CB645  shl      eax, 4
004CB648  movsxd   rcx, eax
004CB64B  lea      eax, [r8 + 0x177]
004CB652  shl      eax, 4
004CB655  movss    dword ptr [rip + 0x1b994f2], xmm8  ; -> 02064B50
004CB65E  inc      r8w
004CB662  movss    dword ptr [rip + 0x1b994ea], xmm7  ; -> 02064B54
004CB66A  movups   xmmword ptr [rcx + rbx], xmm0
004CB66E  movsxd   rcx, eax
004CB671  movss    dword ptr [rip + 0x1b994df], xmm6  ; -> 02064B58
004CB679  movups   xmm0, xmmword ptr [rip + 0x1b994d0]  ; -> 02064B50
004CB680  mov      word ptr [rip + 0x1b99758], r8w  ; -> 02064DE0
004CB688  movups   xmmword ptr [rcx + rbx], xmm0
004CB68C  jmp      0x4cb697  ; -> 004CB697
004CB68E  movss    xmm9, dword ptr [rip + 0x19371a5]  ; -> 01E0283C [f32 1]
004CB697  inc      word ptr [rip + 0x1b9973a]  ; -> 02064DD8
004CB69E  movzx    eax, word ptr [rip + 0x1b9972f]  ; -> 02064DD4
004CB6A5  test     ax, ax
004CB6A8  jle      0x4cb6c8  ; -> 004CB6C8
004CB6AA  movss    xmm7, dword ptr [rip + 0x1937186]  ; -> 01E02838 [u32 0x00000000]
004CB6B2  movss    xmm6, dword ptr [rip + 0x193717a]  ; -> 01E02834 [u32 0x00000000]
004CB6BA  movss    xmm13, dword ptr [rip + 0x193716d]  ; -> 01E02830 [u32 0x00000000]
004CB6C3  jmp      0x4c99c0  ; -> 004C99C0
004CB6C8  mov      r13, qword ptr [rsp + 0x280]
004CB6D0  mov      r12, qword ptr [rsp + 0x2d0]
004CB6D8  jmp      0x4cf1c7  ; -> 004CF1C7
004CB6DD  cmp      r8d, 2
004CB6E1  jne      0x4cf0e0  ; -> 004CF0E0
004CB6E7  movsx    eax, word ptr [rip + 0x1b9941e]  ; -> 02064B0C
004CB6EE  lea      rbx, [rip + 0x1b9973b]  ; -> 02064E30
004CB6F5  add      eax, 0x36
004CB6F8  xor      r8d, r8d
004CB6FB  shl      eax, 4
004CB6FE  movsxd   rcx, eax
004CB701  movzx    eax, word ptr [rcx + rbx + 8]
004CB706  mov      word ptr [rip + 0x1b996a3], ax  ; -> 02064DB0
004CB70D  add      ax, 0x12
004CB711  mov      word ptr [rip + 0x1b996d0], ax  ; -> 02064DE8
004CB718  cwde     
004CB719  shl      eax, 4
004CB71C  movsxd   rcx, eax
004CB71F  add      rcx, rbx
004CB722  call     rbp
004CB724  movsx    esi, word ptr [rip + 0x1b993e1]  ; -> 02064B0C
004CB72B  mov      edi, 0x320
004CB730  add      edi, esi
004CB732  mov      word ptr [rip + 0x1b9967f], si  ; -> 02064DB8
004CB739  mov      word ptr [rip + 0x1b99670], di  ; -> 02064DB0
004CB740  mov      edx, esi
004CB742  lea      eax, [rsi + 0x33]
004CB745  shl      eax, 4
004CB748  movsxd   r11, eax
004CB74B  movzx    eax, word ptr [r11 + rbx + 4]
004CB751  movzx    r10d, word ptr [r11 + rbx]
004CB756  mov      word ptr [rip + 0x1b99687], ax  ; -> 02064DE4
004CB75D  lea      eax, [rsi + 0x32]
004CB760  shl      eax, 4
004CB763  movsxd   rcx, eax
004CB766  lea      eax, [rsi + 0x34]
004CB769  shl      eax, 4
004CB76C  movsxd   r15, eax
004CB76F  lea      eax, [rsi + 0x36]
004CB772  shl      eax, 4
004CB775  movups   xmm0, xmmword ptr [rcx + rbx]
004CB779  movsxd   rcx, eax
004CB77C  inc      di
004CB77F  mov      word ptr [rip + 0x1b99641], r10w  ; -> 02064DC8
004CB787  movups   xmmword ptr [rip + 0x1b99582], xmm0  ; -> 02064D10
004CB78E  mov      word ptr [rip + 0x1b9961f], di  ; -> 02064DB4
004CB795  movups   xmm0, xmmword ptr [r15 + rbx]
004CB79A  movups   xmmword ptr [rip + 0x1b993ff], xmm0  ; -> 02064BA0
004CB7A1  movups   xmm0, xmmword ptr [rcx + rbx]
004CB7A5  movups   xmmword ptr [rip + 0x1b99404], xmm0  ; -> 02064BB0
004CB7AC  lea      eax, [rsi + 0x35]
004CB7AF  shl      eax, 4
004CB7B2  lea      ecx, [rsi + 1]
004CB7B5  and      cx, r10w
004CB7B9  movsxd   r9, eax
004CB7BC  mov      word ptr [rip + 0x1b99609], cx  ; -> 02064DCC
004CB7C3  movups   xmm0, xmmword ptr [r9 + rbx]
004CB7C8  cvtdq2ps xmm2, xmm0
004CB7CB  movups   xmmword ptr [rip + 0x1b993ee], xmm2  ; -> 02064BC0
004CB7D2  cmp      cx, si
004CB7D5  jne      0x4ce444  ; -> 004CE444
004CB7DB  lea      r8d, [rsi + 2]
004CB7DF  cvtdq2ps xmm2, xmm0
004CB7E2  movzx    eax, r8w
004CB7E6  and      ax, r10w
004CB7EA  mov      word ptr [rip + 0x1b995db], ax  ; -> 02064DCC
004CB7F1  movups   xmmword ptr [rip + 0x1b993c8], xmm2  ; -> 02064BC0
004CB7F8  cmp      ax, si
004CB7FB  jne      0x4cd92a  ; -> 004CD92A
004CB801  cvtdq2ps xmm2, xmm0
004CB804  lea      eax, [rsi + 4]
004CB807  and      ax, r10w
004CB80B  mov      word ptr [rip + 0x1b995ba], ax  ; -> 02064DCC
004CB812  movups   xmmword ptr [rip + 0x1b993a7], xmm2  ; -> 02064BC0
004CB819  cmp      ax, si
004CB81C  jne      0x4ccdf3  ; -> 004CCDF3
004CB822  cvtdq2ps xmm2, xmm0
004CB825  lea      eax, [rsi + 8]
004CB828  and      ax, r10w
004CB82C  mov      word ptr [rip + 0x1b99599], ax  ; -> 02064DCC
004CB833  movups   xmmword ptr [rip + 0x1b99386], xmm2  ; -> 02064BC0
004CB83A  cmp      ax, si
004CB83D  jne      0x4cc119  ; -> 004CC119
004CB843  movzx    eax, word ptr [r11 + rbx + 8]
004CB849  movss    xmm12, dword ptr [rip + 0x1936fea]  ; -> 01E0283C [f32 1]
004CB852  movss    xmm11, dword ptr [rip + 0x1936fd5]  ; -> 01E02830 [u32 0x00000000]
004CB85B  mov      word ptr [rip + 0x1b9956a], ax  ; -> 02064DCC
004CB862  cvtdq2ps xmm10, xmm0
004CB866  movups   xmmword ptr [rip + 0x1b99352], xmm10  ; -> 02064BC0
004CB86E  shufps   xmm10, xmm10, 0xff
004CB873  mulss    xmm10, dword ptr [rip + 0x1b993a4]  ; -> 02064C20
004CB87C  movss    dword ptr [rip + 0x1b99347], xmm10  ; -> 02064BCC
004CB885  cmp      ax, si
004CB888  je       0x4cb8c1  ; -> 004CB8C1
004CB88A  movss    xmm1, dword ptr [rip + 0x1936fa2]  ; -> 01E02834 [u32 0x00000000]
004CB892  movaps   xmm0, xmm11
004CB896  addss    xmm0, xmm11
004CB89B  addss    xmm1, xmm1
004CB89F  movss    dword ptr [rip + 0x1b99329], xmm0  ; -> 02064BD0
004CB8A7  movss    xmm0, dword ptr [rip + 0x1936f89]  ; -> 01E02838 [u32 0x00000000]
004CB8AF  addss    xmm0, xmm12
004CB8B4  movss    dword ptr [rip + 0x1b9931c], xmm0  ; -> 02064BD8
004CB8BC  jmp      0x4cb9f8  ; -> 004CB9F8
004CB8C1  movups   xmm9, xmmword ptr [r15 + rbx]
004CB8C6  lea      eax, [rdx + 0xb]
004CB8C9  shl      eax, 4
004CB8CC  movsxd   rcx, eax
004CB8CF  movaps   xmm6, xmm9
004CB8D3  movups   xmmword ptr [rip + 0x1b992f5], xmm9  ; -> 02064BD0
004CB8DB  lea      eax, [rdx + 0xc]
004CB8DE  movaps   xmm2, xmm9
004CB8E2  shufps   xmm6, xmm6, 0
004CB8E6  movups   xmm1, xmmword ptr [rcx + rbx]
004CB8EA  shl      eax, 4
004CB8ED  shufps   xmm2, xmm9, 0x55
004CB8F2  mulps    xmm6, xmm1
004CB8F5  movsxd   rcx, eax
004CB8F8  lea      eax, [rdx + 0xd]
004CB8FB  movups   xmmword ptr [rip + 0x1b9925e], xmm1  ; -> 02064B60
004CB902  shl      eax, 4
004CB905  shufps   xmm9, xmm9, 0xaa
004CB90A  movups   xmm0, xmmword ptr [rcx + rbx]
004CB90E  movsxd   rcx, eax
004CB911  movups   xmmword ptr [rip + 0x1b99208], xmm6  ; -> 02064B20
004CB918  movss    xmm3, dword ptr [rip + 0x1b99204]  ; -> 02064B24
004CB920  movups   xmm7, xmm0
004CB923  movups   xmm8, xmmword ptr [rcx + rbx]
004CB928  movss    xmm4, dword ptr [rip + 0x1b991f8]  ; -> 02064B28
004CB930  movaps   xmm1, xmm7
004CB933  movss    xmm5, dword ptr [rip + 0x1b991f1]  ; -> 02064B2C
004CB93B  movups   xmmword ptr [rip + 0x1b9922e], xmm0  ; -> 02064B70
004CB942  mulss    xmm0, xmm2
004CB946  shufps   xmm1, xmm7, 0xaa
004CB94A  mulss    xmm1, xmm2
004CB94E  addss    xmm6, xmm0
004CB952  movaps   xmm0, xmm7
004CB955  shufps   xmm0, xmm7, 0x55
004CB959  mulss    xmm0, xmm2
004CB95D  addss    xmm4, xmm1
004CB961  movaps   xmm1, xmm9
004CB965  shufps   xmm7, xmm7, 0xff
004CB969  mulss    xmm7, xmm2
004CB96D  movaps   xmm2, xmm9
004CB971  addss    xmm3, xmm0
004CB975  movss    dword ptr [rip + 0x1b991a3], xmm6  ; -> 02064B20
004CB97D  movaps   xmm0, xmm9
004CB981  movss    dword ptr [rip + 0x1b9919f], xmm4  ; -> 02064B28
004CB989  mulss    xmm0, xmm8
004CB98E  addss    xmm5, xmm7
004CB992  movups   xmmword ptr [rip + 0x1b991e6], xmm8  ; -> 02064B80
004CB99A  addss    xmm0, xmm6
004CB99E  movss    dword ptr [rip + 0x1b9917e], xmm3  ; -> 02064B24
004CB9A6  movss    dword ptr [rip + 0x1b9917e], xmm5  ; -> 02064B2C
004CB9AE  movss    dword ptr [rip + 0x1b9921a], xmm0  ; -> 02064BD0
004CB9B6  movaps   xmm0, xmm8
004CB9BA  shufps   xmm0, xmm8, 0x55
004CB9BF  mulss    xmm1, xmm0
004CB9C3  movaps   xmm0, xmm8
004CB9C7  shufps   xmm0, xmm8, 0xaa
004CB9CC  shufps   xmm8, xmm8, 0xff
004CB9D1  mulss    xmm9, xmm8
004CB9D6  addss    xmm1, xmm3
004CB9DA  mulss    xmm2, xmm0
004CB9DE  addss    xmm9, xmm5
004CB9E3  addss    xmm2, xmm4
004CB9E7  movss    dword ptr [rip + 0x1b991ec], xmm9  ; -> 02064BDC
004CB9F0  movss    dword ptr [rip + 0x1b991e0], xmm2  ; -> 02064BD8
004CB9F8  movss    dword ptr [rip + 0x1b991d4], xmm1  ; -> 02064BD4
004CBA00  movzx    eax, word ptr [rip + 0x1b993d5]  ; -> 02064DDC
004CBA07  movss    xmm7, dword ptr [rip + 0x1820275]  ; -> 01CEBC84 [f32 16]
004CBA0F  movss    xmm8, dword ptr [rip + 0x3fa128]  ; -> 008C5B40 [f32 255]
004CBA18  cmp      ax, si
004CBA1B  je       0x4cbd4e  ; -> 004CBD4E
004CBA21  movsx    r9d, ax
004CBA25  add      r9w, si
004CBA29  mov      word ptr [rip + 0x1b993a0], si  ; -> 02064DD0
004CBA30  mov      word ptr [rip + 0x1b993a1], si  ; -> 02064DD8
004CBA37  nop      word ptr [rax + rax]
004CBA40  movsx    edx, si
004CBA43  lea      eax, [rdx + 0xfa]
004CBA49  shl      eax, 4
004CBA4C  movsxd   rcx, eax
004CBA4F  lea      eax, [rdx + 0xc8]
004CBA55  shl      eax, 4
004CBA58  movups   xmm6, xmmword ptr [rcx + rbx]
004CBA5C  movsxd   rcx, eax
004CBA5F  movups   xmmword ptr [rip + 0x1b990da], xmm6  ; -> 02064B40
004CBA66  movaps   xmm1, xmm6
004CBA69  movss    dword ptr [rip + 0x1b990cf], xmm6  ; -> 02064B40
004CBA71  movsx    eax, word ptr [rcx + rbx]
004CBA75  movaps   xmm5, xmm6
004CBA78  mulss    xmm5, dword ptr [rip + 0x1b99150]  ; -> 02064BD0
004CBA80  movsx    edx, word ptr [rcx + rbx + 4]
004CBA85  movsx    r8d, word ptr [rcx + rbx + 8]
004CBA8B  mov      word ptr [rip + 0x1b9932a], ax  ; -> 02064DBC
004CBA92  add      eax, 0x190
004CBA97  shl      eax, 4
004CBA9A  shufps   xmm1, xmm6, 0x55
004CBA9E  cdqe     
004CBAA0  shufps   xmm6, xmm6, 0xaa
004CBAA4  movss    dword ptr [rip + 0x1b9909c], xmm6  ; -> 02064B48
004CBAAC  mulss    xmm6, dword ptr [rip + 0x1b99124]  ; -> 02064BD8
004CBAB4  mov      word ptr [rip + 0x1b99305], dx  ; -> 02064DC0
004CBABB  movups   xmm2, xmmword ptr [rax + rbx]
004CBABF  lea      eax, [rdx + 0x190]
004CBAC5  mov      word ptr [rip + 0x1b992f7], r8w  ; -> 02064DC4
004CBACD  movss    dword ptr [rip + 0x1b9906f], xmm1  ; -> 02064B44
004CBAD5  mulss    xmm1, dword ptr [rip + 0x1b990f7]  ; -> 02064BD4
004CBADD  shl      eax, 4
004CBAE0  cdqe     
004CBAE2  movups   xmmword ptr [rip + 0x1b991b7], xmm2  ; -> 02064CA0
004CBAE9  movss    xmm0, dword ptr [rip + 0x1b991b3]  ; -> 02064CA4
004CBAF1  movups   xmm3, xmmword ptr [rax + rbx]
004CBAF5  lea      eax, [r8 + 0x190]
004CBAFC  movss    dword ptr [rip + 0x1b99054], xmm6  ; -> 02064B58
004CBB04  shl      eax, 4
004CBB07  cdqe     
004CBB09  dec      r9w
004CBB0D  movups   xmmword ptr [rip + 0x1b9919c], xmm3  ; -> 02064CB0
004CBB14  mov      word ptr [rip + 0x1b992b8], r9w  ; -> 02064DD4
004CBB1C  movss    dword ptr [rip + 0x1b99030], xmm1  ; -> 02064B54
004CBB24  movups   xmm4, xmmword ptr [rax + rbx]
004CBB28  mulss    xmm1, xmm12
004CBB2D  mulss    xmm6, xmm12
004CBB32  mulss    xmm0, xmm7
004CBB36  movss    dword ptr [rip + 0x1b99012], xmm5  ; -> 02064B50
004CBB3E  mulss    xmm2, xmm7
004CBB42  mulss    xmm5, xmm12
004CBB47  cvttss2si eax, xmm2
004CBB4B  addss    xmm5, xmm1
004CBB4F  mulss    xmm3, xmm7
004CBB53  mov      dword ptr [rip + 0x1b99147], eax  ; -> 02064CA0
004CBB59  movss    xmm1, dword ptr [rip + 0x1b99147]  ; -> 02064CA8
004CBB61  cvttss2si eax, xmm0
004CBB65  movss    xmm0, dword ptr [rip + 0x1b99147]  ; -> 02064CB4
004CBB6D  addss    xmm6, xmm5
004CBB71  mov      dword ptr [rip + 0x1b9912d], eax  ; -> 02064CA4
004CBB77  mulss    xmm1, xmm7
004CBB7B  movups   xmmword ptr [rip + 0x1b9913e], xmm4  ; -> 02064CC0
004CBB82  maxss    xmm6, xmm11
004CBB87  mulss    xmm0, xmm7
004CBB8B  cvttss2si eax, xmm1
004CBB8F  movss    xmm1, dword ptr [rip + 0x1b99121]  ; -> 02064CB8
004CBB97  mov      dword ptr [rip + 0x1b9910b], eax  ; -> 02064CA8
004CBB9D  cvttss2si eax, xmm3
004CBBA1  mulss    xmm6, xmm6
004CBBA5  mov      dword ptr [rip + 0x1b99105], eax  ; -> 02064CB0
004CBBAB  cvttss2si eax, xmm0
004CBBAF  mulss    xmm1, xmm7
004CBBB3  mov      dword ptr [rip + 0x1b990fb], eax  ; -> 02064CB4
004CBBB9  mulss    xmm4, xmm7
004CBBBD  cvttss2si eax, xmm1
004CBBC1  mulss    xmm6, xmm6
004CBBC5  mov      dword ptr [rip + 0x1b990ed], eax  ; -> 02064CB8
004CBBCB  cvttss2si eax, xmm4
004CBBCF  mulss    xmm6, xmm6
004CBBD3  mov      dword ptr [rip + 0x1b990e7], eax  ; -> 02064CC0
004CBBD9  movss    dword ptr [rip + 0x1b98f4b], xmm5  ; -> 02064B2C
004CBBE1  movss    dword ptr [rip + 0x1b98f73], xmm6  ; -> 02064B5C
004CBBE9  movss    xmm0, dword ptr [rip + 0x1b990d3]  ; -> 02064CC4
004CBBF1  lea      rdx, [rip + 0x1b990e8]  ; -> 02064CE0
004CBBF8  movss    xmm1, dword ptr [rip + 0x1b990c8]  ; -> 02064CC8
004CBC00  lea      rcx, [rip + 0x1b990d9]  ; -> 02064CE0
004CBC07  inc      word ptr [rip + 0x1b991aa]  ; -> 02064DB8
004CBC0E  movaps   xmm2, xmm8
004CBC12  mulss    xmm0, xmm7
004CBC16  mov      dword ptr [rip + 0x1b98ee4], 0x437f0000  ; -> 02064B04
004CBC20  mulss    xmm1, xmm7
004CBC24  cvttss2si eax, xmm0
004CBC28  movss    xmm0, dword ptr [rip + 0x1b98f90]  ; -> 02064BC0
004CBC30  maxss    xmm0, xmm11
004CBC35  mulss    xmm10, xmm6
004CBC3A  mov      dword ptr [rip + 0x1b99084], eax  ; -> 02064CC4
004CBC40  cvttss2si eax, xmm1
004CBC44  movss    xmm1, dword ptr [rip + 0x1b98f78]  ; -> 02064BC4
004CBC4C  maxss    xmm10, xmm11
004CBC51  movss    dword ptr [rip + 0x1b99087], xmm0  ; -> 02064CE0
004CBC59  maxss    xmm1, xmm11
004CBC5E  movss    xmm0, dword ptr [rip + 0x1b98f62]  ; -> 02064BC8
004CBC66  maxss    xmm0, xmm11
004CBC6B  mov      dword ptr [rip + 0x1b99057], eax  ; -> 02064CC8
004CBC71  movss    dword ptr [rip + 0x1b99072], xmm10  ; -> 02064CEC
004CBC7A  movss    dword ptr [rip + 0x1b99062], xmm1  ; -> 02064CE4
004CBC82  movss    dword ptr [rip + 0x1b9905e], xmm0  ; -> 02064CE8
004CBC8A  call     0x4cf230  ; -> 004CF230 fn
004CBC8F  movups   xmm0, xmmword ptr [rip + 0x1b9900a]  ; -> 02064CA0
004CBC96  movsx    edx, di
004CBC99  add      di, 7
004CBC9D  movups   xmm1, xmmword ptr [rip + 0x1b9903c]  ; -> 02064CE0
004CBCA4  mov      r8d, edx
004CBCA7  mov      word ptr [rip + 0x1b99106], di  ; -> 02064DB4
004CBCAE  shl      r8d, 4
004CBCB2  cvttps2dq xmm2, xmm1
004CBCB6  lea      eax, [r8 + 0x10]
004CBCBA  movsxd   rcx, eax
004CBCBD  lea      eax, [rdx + 2]
004CBCC0  shl      eax, 4
004CBCC3  movups   xmmword ptr [rip + 0x1b99016], xmm2  ; -> 02064CE0
004CBCCA  movups   xmmword ptr [rcx + rbx], xmm0
004CBCCE  movsxd   rcx, eax
004CBCD1  lea      eax, [rdx + 3]
004CBCD4  movups   xmm0, xmmword ptr [rip + 0x1b98fd5]  ; -> 02064CB0
004CBCDB  shl      eax, 4
004CBCDE  mov      rdx, r14
004CBCE1  movups   xmmword ptr [rcx + rbx], xmm0
004CBCE5  movsxd   rcx, eax
004CBCE8  movups   xmm0, xmmword ptr [rip + 0x1b98fd1]  ; -> 02064CC0
004CBCEF  movsxd   rax, r8d
004CBCF2  movups   xmmword ptr [rcx + rbx], xmm0
004CBCF6  mov      rcx, rbp
004CBCF9  movups   xmmword ptr [rax + rbx], xmm2
004CBCFD  call     0x4c7f00  ; -> 004C7F00 fn
004CBD02  movzx    esi, word ptr [rip + 0x1b990cf]  ; -> 02064DD8
004CBD09  movzx    r9d, word ptr [rip + 0x1b990c3]  ; -> 02064DD4
004CBD11  inc      si
004CBD14  movss    xmm12, dword ptr [rip + 0x1936b1f]  ; -> 01E0283C [f32 1]
004CBD1D  movss    xmm11, dword ptr [rip + 0x1936b0a]  ; -> 01E02830 [u32 0x00000000]
004CBD26  movzx    edi, word ptr [rip + 0x1b99087]  ; -> 02064DB4
004CBD2D  movss    xmm10, dword ptr [rip + 0x1b98e96]  ; -> 02064BCC
004CBD36  mov      word ptr [rip + 0x1b9909b], si  ; -> 02064DD8
004CBD3D  test     r9w, r9w
004CBD41  jg       0x4cba40  ; -> 004CBA40
004CBD47  movzx    esi, word ptr [rip + 0x1b98dbe]  ; -> 02064B0C
004CBD4E  movzx    ecx, word ptr [rip + 0x1b9908b]  ; -> 02064DE0
004CBD55  cmp      cx, si
004CBD58  je       0x4cc0f5  ; -> 004CC0F5
004CBD5E  lea      eax, [rsi + 1]
004CBD61  movsx    r10d, cx
004CBD65  mov      word ptr [rip + 0x1b99064], ax  ; -> 02064DD0
004CBD6C  add      r10w, si
004CBD70  mov      word ptr [rip + 0x1b99061], si  ; -> 02064DD8
004CBD77  nop      word ptr [rax + rax]
004CBD80  movsx    edx, si
004CBD83  dec      r10w
004CBD87  mov      word ptr [rip + 0x1b99045], r10w  ; -> 02064DD4
004CBD8F  lea      eax, [rdx + 0x12c]
004CBD95  shl      eax, 4
004CBD98  movsxd   rcx, eax
004CBD9B  lea      eax, [rdx + 0x15e]
004CBDA1  shl      eax, 4
004CBDA4  movsx    r8d, word ptr [rcx + rbx]
004CBDA9  movsx    r9d, word ptr [rcx + rbx + 4]
004CBDAF  movsxd   rcx, eax
004CBDB2  mov      word ptr [rip + 0x1b99002], r8w  ; -> 02064DBC
004CBDBA  lea      eax, [r8 + 0x190]
004CBDC1  mov      word ptr [rip + 0x1b98ff7], r9w  ; -> 02064DC0
004CBDC9  shl      eax, 4
004CBDCC  movups   xmm0, xmmword ptr [rcx + rbx]
004CBDD0  movsxd   rcx, eax
004CBDD3  lea      eax, [r9 + 0x190]
004CBDDA  shl      eax, 4
004CBDDD  movups   xmmword ptr [rip + 0x1b98d5c], xmm0  ; -> 02064B40
004CBDE4  movups   xmm6, xmm0
004CBDE7  movaps   xmm1, xmm0
004CBDEA  mulss    xmm1, dword ptr [rip + 0x1b98dde]  ; -> 02064BD0
004CBDF2  movups   xmm3, xmmword ptr [rcx + rbx]
004CBDF6  movsxd   rcx, eax
004CBDF9  lea      eax, [r8 + 0x1f4]
004CBE00  shl      eax, 4
004CBE03  movss    dword ptr [rip + 0x1b98d35], xmm6  ; -> 02064B40
004CBE0B  shufps   xmm6, xmm6, 0xaa
004CBE0F  movups   xmm4, xmmword ptr [rcx + rbx]
004CBE13  movsxd   rcx, eax
004CBE16  lea      eax, [r9 + 0x1f4]
004CBE1D  shufps   xmm0, xmm0, 0x55
004CBE21  shl      eax, 4
004CBE24  movss    dword ptr [rip + 0x1b98d1c], xmm6  ; -> 02064B48
004CBE2C  mulss    xmm6, dword ptr [rip + 0x1b98da4]  ; -> 02064BD8
004CBE34  movups   xmm5, xmmword ptr [rcx + rbx]
004CBE38  movsxd   rcx, eax
004CBE3B  movss    dword ptr [rip + 0x1b98d01], xmm0  ; -> 02064B44
004CBE43  mulss    xmm0, dword ptr [rip + 0x1b98d89]  ; -> 02064BD4
004CBE4B  movups   xmm2, xmmword ptr [rcx + rbx]
004CBE4F  movups   xmmword ptr [rip + 0x1b98e3a], xmm3  ; -> 02064C90
004CBE56  movss    dword ptr [rip + 0x1b98cf2], xmm1  ; -> 02064B50
004CBE5E  movss    dword ptr [rip + 0x1b98cf2], xmm6  ; -> 02064B58
004CBE66  movups   xmmword ptr [rip + 0x1b98e33], xmm4  ; -> 02064CA0
004CBE6D  movss    dword ptr [rip + 0x1b98cdf], xmm0  ; -> 02064B54
004CBE75  mulss    xmm1, xmm12
004CBE7A  mulss    xmm0, xmm12
004CBE7F  mulss    xmm6, xmm12
004CBE84  addss    xmm1, xmm0
004CBE88  mulss    xmm3, xmm7
004CBE8C  movss    xmm0, dword ptr [rip + 0x1b98e00]  ; -> 02064C94
004CBE94  mulss    xmm0, xmm7
004CBE98  addss    xmm6, xmm1
004CBE9C  movss    dword ptr [rip + 0x1b98c88], xmm1  ; -> 02064B2C
004CBEA4  movss    xmm1, dword ptr [rip + 0x1b98dec]  ; -> 02064C98
004CBEAC  mulss    xmm1, xmm7
004CBEB0  cvttss2si eax, xmm3
004CBEB4  maxss    xmm6, xmm11
004CBEB9  mulss    xmm4, xmm7
004CBEBD  mov      dword ptr [rip + 0x1b98dcd], eax  ; -> 02064C90
004CBEC3  cvttss2si eax, xmm0
004CBEC7  movss    xmm0, dword ptr [rip + 0x1b98dd5]  ; -> 02064CA4
004CBECF  mov      dword ptr [rip + 0x1b98dbf], eax  ; -> 02064C94
004CBED5  cvttss2si eax, xmm1
004CBED9  movss    xmm1, dword ptr [rip + 0x1b98dc7]  ; -> 02064CA8
004CBEE1  mov      dword ptr [rip + 0x1b98db1], eax  ; -> 02064C98
004CBEE7  cvttss2si eax, xmm4
004CBEEB  mulss    xmm6, xmm6
004CBEEF  mov      dword ptr [rip + 0x1b98dab], eax  ; -> 02064CA0
004CBEF5  mulss    xmm0, xmm7
004CBEF9  mulss    xmm1, xmm7
004CBEFD  cvttss2si eax, xmm0
004CBF01  mulss    xmm6, xmm6
004CBF05  mov      dword ptr [rip + 0x1b98d99], eax  ; -> 02064CA4
004CBF0B  cvttss2si eax, xmm1
004CBF0F  mulss    xmm6, xmm6
004CBF13  mov      dword ptr [rip + 0x1b98d8f], eax  ; -> 02064CA8
004CBF19  movups   xmmword ptr [rip + 0x1b98d90], xmm5  ; -> 02064CB0
004CBF20  movss    dword ptr [rip + 0x1b98c34], xmm6  ; -> 02064B5C
004CBF28  movups   xmmword ptr [rip + 0x1b98d91], xmm2  ; -> 02064CC0
004CBF2F  movss    xmm0, dword ptr [rip + 0x1b98d7d]  ; -> 02064CB4
004CBF37  lea      rdx, [rip + 0x1b98da2]  ; -> 02064CE0
004CBF3E  movss    xmm1, dword ptr [rip + 0x1b98d72]  ; -> 02064CB8
004CBF46  mulss    xmm0, xmm7
004CBF4A  movsx    r8d, di
004CBF4E  mulss    xmm1, xmm7
004CBF52  mov      r9d, r8d
004CBF55  shl      r9d, 4
004CBF59  mulss    xmm2, xmm7
004CBF5D  mov      dword ptr [rip + 0x1b98b9d], 0x437f0000  ; -> 02064B04
004CBF67  mulss    xmm5, xmm7
004CBF6B  mulss    xmm10, xmm6
004CBF70  cvttss2si eax, xmm5
004CBF74  maxss    xmm10, xmm11
004CBF79  mov      dword ptr [rip + 0x1b98d31], eax  ; -> 02064CB0
004CBF7F  cvttss2si eax, xmm0
004CBF83  movss    xmm0, dword ptr [rip + 0x1b98d39]  ; -> 02064CC4
004CBF8B  mulss    xmm0, xmm7
004CBF8F  mov      dword ptr [rip + 0x1b98d1f], eax  ; -> 02064CB4
004CBF95  cvttss2si eax, xmm1
004CBF99  movss    xmm1, dword ptr [rip + 0x1b98d27]  ; -> 02064CC8
004CBFA1  mov      dword ptr [rip + 0x1b98d11], eax  ; -> 02064CB8
004CBFA7  mulss    xmm1, xmm7
004CBFAB  cvttss2si eax, xmm2
004CBFAF  movaps   xmm2, xmm8
004CBFB3  movss    dword ptr [rip + 0x1b98d30], xmm10  ; -> 02064CEC
004CBFBC  mov      dword ptr [rip + 0x1b98cfe], eax  ; -> 02064CC0
004CBFC2  cvttss2si eax, xmm0
004CBFC6  movss    xmm0, dword ptr [rip + 0x1b98bf2]  ; -> 02064BC0
004CBFCE  maxss    xmm0, xmm11
004CBFD3  mov      dword ptr [rip + 0x1b98ceb], eax  ; -> 02064CC4
004CBFD9  cvttss2si eax, xmm1
004CBFDD  movss    xmm1, dword ptr [rip + 0x1b98bdf]  ; -> 02064BC4
004CBFE5  movss    dword ptr [rip + 0x1b98cf3], xmm0  ; -> 02064CE0
004CBFED  maxss    xmm1, xmm11
004CBFF2  movss    xmm0, dword ptr [rip + 0x1b98bce]  ; -> 02064BC8
004CBFFA  maxss    xmm0, xmm11
004CBFFF  mov      dword ptr [rip + 0x1b98cc3], eax  ; -> 02064CC8
004CC005  lea      eax, [r9 + 0x10]
004CC009  movsxd   rcx, eax
004CC00C  movss    dword ptr [rip + 0x1b98cd0], xmm1  ; -> 02064CE4
004CC014  movss    dword ptr [rip + 0x1b98ccc], xmm0  ; -> 02064CE8
004CC01C  movups   xmm0, xmmword ptr [rip + 0x1b98c6d]  ; -> 02064C90
004CC023  movups   xmmword ptr [rcx + rbx], xmm0
004CC027  lea      rcx, [rip + 0x1b98cb2]  ; -> 02064CE0
004CC02E  call     0x4cf230  ; -> 004CF230 fn
004CC033  movups   xmm0, xmmword ptr [rip + 0x1b98c66]  ; -> 02064CA0
004CC03A  inc      word ptr [rip + 0x1b98d77]  ; -> 02064DB8
004CC041  lea      eax, [r8 + 2]
004CC045  movups   xmm1, xmmword ptr [rip + 0x1b98c94]  ; -> 02064CE0
004CC04C  shl      eax, 4
004CC04F  add      di, 5
004CC053  movsxd   rcx, eax
004CC056  mov      rdx, r14
004CC059  lea      eax, [r8 + 3]
004CC05D  mov      word ptr [rip + 0x1b98d50], di  ; -> 02064DB4
004CC064  shl      eax, 4
004CC067  cvttps2dq xmm2, xmm1
004CC06B  movups   xmmword ptr [rcx + rbx], xmm0
004CC06F  movsxd   rcx, eax
004CC072  lea      eax, [r8 + 4]
004CC076  movups   xmm0, xmmword ptr [rip + 0x1b98c33]  ; -> 02064CB0
004CC07D  shl      eax, 4
004CC080  movups   xmmword ptr [rip + 0x1b98c59], xmm2  ; -> 02064CE0
004CC087  movups   xmmword ptr [rcx + rbx], xmm0
004CC08B  movsxd   rcx, eax
004CC08E  movups   xmm0, xmmword ptr [rip + 0x1b98c2b]  ; -> 02064CC0
004CC095  movsxd   rax, r9d
004CC098  movups   xmmword ptr [rcx + rbx], xmm0
004CC09C  mov      rcx, rbp
004CC09F  movups   xmmword ptr [rax + rbx], xmm2
004CC0A3  call     0x4c7f00  ; -> 004C7F00 fn
004CC0A8  movzx    esi, word ptr [rip + 0x1b98d29]  ; -> 02064DD8
004CC0AF  movzx    r10d, word ptr [rip + 0x1b98d1d]  ; -> 02064DD4
004CC0B7  inc      si
004CC0BA  mov      word ptr [rip + 0x1b98d17], si  ; -> 02064DD8
004CC0C1  test     r10w, r10w
004CC0C5  jle      0x4cc0ee  ; -> 004CC0EE
004CC0C7  movss    xmm12, dword ptr [rip + 0x193676c]  ; -> 01E0283C [f32 1]
004CC0D0  movss    xmm11, dword ptr [rip + 0x1936757]  ; -> 01E02830 [u32 0x00000000]
004CC0D9  movzx    edi, word ptr [rip + 0x1b98cd4]  ; -> 02064DB4
004CC0E0  movss    xmm10, dword ptr [rip + 0x1b98ae3]  ; -> 02064BCC
004CC0E9  jmp      0x4cbd80  ; -> 004CBD80
004CC0EE  movzx    esi, word ptr [rip + 0x1b98a17]  ; -> 02064B0C
004CC0F5  add      si, 0x10
004CC0F9  xor      r8d, r8d
004CC0FC  movsx    eax, si
004CC0FF  mov      rdx, r14
004CC102  shl      eax, 4
004CC105  movsxd   rcx, eax
004CC108  add      rcx, rbx
004CC10B  mov      word ptr [rip + 0x1b98cd6], si  ; -> 02064DE8
004CC112  call     rbp
004CC114  jmp      0x4cf1c7  ; -> 004CF1C7
004CC119  movss    xmm4, dword ptr [rip + 0x193670f]  ; -> 01E02830 [u32 0x00000000]
004CC121  lea      rdx, [rip + 0x1b98a68]  ; -> 02064B90
004CC128  movss    xmm5, dword ptr [rip + 0x1b98a9c]  ; -> 02064BCC
004CC130  lea      rcx, [rip + 0x1b98a59]  ; -> 02064B90
004CC137  movss    xmm8, dword ptr [rip + 0x1b98a80]  ; -> 02064BC0
004CC140  movaps   xmm0, xmm5
004CC143  movss    xmm7, dword ptr [rip + 0x1b98a79]  ; -> 02064BC4
004CC14B  movaps   xmm3, xmm8
004CC14F  movss    xmm6, dword ptr [rip + 0x1b98a71]  ; -> 02064BC8
004CC157  movaps   xmm2, xmm7
004CC15A  mulss    xmm3, dword ptr [rip + 0x1b98aae]  ; -> 02064C10
004CC162  movaps   xmm1, xmm6
004CC165  mov      dword ptr [rip + 0x1b98995], 0x437f0000  ; -> 02064B04
004CC16F  mulss    xmm2, dword ptr [rip + 0x1b98a9d]  ; -> 02064C14
004CC177  mulss    xmm1, dword ptr [rip + 0x1b98a99]  ; -> 02064C18
004CC17F  maxss    xmm3, xmm4
004CC183  mulss    xmm0, dword ptr [rip + 0x1b98a91]  ; -> 02064C1C
004CC18B  maxss    xmm2, xmm4
004CC18F  mulss    xmm8, dword ptr [rip + 0x1b98a68]  ; -> 02064C00
004CC198  maxss    xmm1, xmm4
004CC19C  mulss    xmm7, dword ptr [rip + 0x1b98a60]  ; -> 02064C04
004CC1A4  maxss    xmm0, xmm4
004CC1A8  mulss    xmm6, dword ptr [rip + 0x1b98a58]  ; -> 02064C08
004CC1B0  maxss    xmm8, xmm4
004CC1B5  mulss    xmm5, dword ptr [rip + 0x1b98a4f]  ; -> 02064C0C
004CC1BD  maxss    xmm7, xmm4
004CC1C1  movss    dword ptr [rip + 0x1b989c7], xmm3  ; -> 02064B90
004CC1C9  maxss    xmm6, xmm4
004CC1CD  movss    xmm3, dword ptr [rip + 0x3f996b]  ; -> 008C5B40 [f32 255]
004CC1D5  movss    dword ptr [rip + 0x1b989b7], xmm2  ; -> 02064B94
004CC1DD  maxss    xmm5, xmm4
004CC1E1  movaps   xmm2, xmm3
004CC1E4  movss    dword ptr [rip + 0x1b989ac], xmm1  ; -> 02064B98
004CC1EC  movss    dword ptr [rip + 0x1b989a8], xmm0  ; -> 02064B9C
004CC1F4  movss    dword ptr [rip + 0x1b989c3], xmm8  ; -> 02064BC0
004CC1FD  movss    dword ptr [rip + 0x1b989bf], xmm7  ; -> 02064BC4
004CC205  movss    dword ptr [rip + 0x1b989bb], xmm6  ; -> 02064BC8
004CC20D  movss    dword ptr [rip + 0x1b989b7], xmm5  ; -> 02064BCC
004CC215  call     0x4cf230  ; -> 004CF230 fn
004CC21A  lea      rdx, [rip + 0x1b9899f]  ; -> 02064BC0
004CC221  lea      rcx, [rip + 0x1b98998]  ; -> 02064BC0
004CC228  call     0x4cf230  ; -> 004CF230 fn
004CC22D  movups   xmm0, xmmword ptr [rip + 0x1b9895c]  ; -> 02064B90
004CC234  movzx    eax, word ptr [rip + 0x1b98ba1]  ; -> 02064DDC
004CC23B  movss    xmm9, dword ptr [rip + 0x181fa40]  ; -> 01CEBC84 [f32 16]
004CC244  movss    xmm13, dword ptr [rip + 0x4493cb]  ; -> 00915618 [f32 1792]
004CC24D  movss    xmm7, dword ptr [rip + 0x4493c7]  ; -> 0091561C [f32 1824]
004CC255  movss    xmm4, dword ptr [rip + 0x3f98d3]  ; -> 008C5B30 [f32 0.001953125]
004CC25D  cvttps2dq xmm1, xmm0
004CC261  movups   xmm0, xmmword ptr [rip + 0x1b98958]  ; -> 02064BC0
004CC268  movups   xmmword ptr [rip + 0x1b98921], xmm1  ; -> 02064B90
004CC26F  cvttps2dq xmm0, xmm0
004CC273  movups   xmmword ptr [rip + 0x1b98946], xmm0  ; -> 02064BC0
004CC27A  cmp      ax, si
004CC27D  je       0x4cc762  ; -> 004CC762
004CC283  cwde     
004CC284  movzx    ecx, si
004CC287  add      ax, si
004CC28A  mov      word ptr [rip + 0x1b98b47], cx  ; -> 02064DD8
004CC291  mov      word ptr [rip + 0x1b98b37], r8w  ; -> 02064DD0
004CC299  nop      dword ptr [rax]
004CC2A0  movss    xmm1, dword ptr [rip + 0x1936590]  ; -> 01E02838 [u32 0x00000000]
004CC2A8  dec      ax
004CC2AB  addss    xmm1, dword ptr [rip + 0x1936589]  ; -> 01E0283C [f32 1]
004CC2B3  mov      word ptr [rip + 0x1b98b1a], ax  ; -> 02064DD4
004CC2BA  movsx    eax, cx
004CC2BD  add      eax, 0xc8
004CC2C2  shl      eax, 4
004CC2C5  movsxd   rcx, eax
004CC2C8  movsx    eax, word ptr [rcx + rbx]
004CC2CC  movsx    edx, word ptr [rcx + rbx + 4]
004CC2D1  mov      r9d, eax
004CC2D4  movsx    r8d, word ptr [rcx + rbx + 8]
004CC2DA  mov      word ptr [rip + 0x1b98adb], ax  ; -> 02064DBC
004CC2E1  add      eax, 0x190
004CC2E6  shl      eax, 4
004CC2E9  movsxd   rcx, eax
004CC2EC  lea      eax, [rdx + 0x190]
004CC2F2  shl      eax, 4
004CC2F5  mov      word ptr [rip + 0x1b98ac4], dx  ; -> 02064DC0
004CC2FC  mov      word ptr [rip + 0x1b98ac0], r8w  ; -> 02064DC4
004CC304  movups   xmm2, xmmword ptr [rcx + rbx]
004CC308  movsxd   rcx, eax
004CC30B  lea      eax, [r8 + 0x190]
004CC312  shl      eax, 4
004CC315  movaps   xmm7, xmm2
004CC318  movaps   xmm3, xmm2
004CC31B  subss    xmm7, xmm13
004CC320  shufps   xmm3, xmm2, 0x55
004CC324  movups   xmm14, xmmword ptr [rcx + rbx]
004CC329  movsxd   rcx, eax
004CC32C  lea      eax, [r9 + 0x258]
004CC333  shl      eax, 4
004CC336  movaps   xmm11, xmm3
004CC33A  movaps   xmm5, xmm14
004CC33E  movaps   xmm8, xmm14
004CC342  shufps   xmm5, xmm14, 0x55
004CC347  subss    xmm8, xmm13
004CC34C  movups   xmm15, xmmword ptr [rcx + rbx]
004CC351  movsxd   rcx, eax
004CC354  lea      eax, [rdx + 0x258]
004CC35A  shl      eax, 4
004CC35D  movaps   xmm12, xmm5
004CC361  movaps   xmmword ptr [rsp + 0x40], xmm5
004CC366  movaps   xmm10, xmm15
004CC36A  subss    xmm10, xmm13
004CC36F  mulss    xmm7, xmm4
004CC373  movups   xmm0, xmmword ptr [rcx + rbx]
004CC377  movsxd   rcx, eax
004CC37A  lea      eax, [r8 + 0x258]
004CC381  shl      eax, 4
004CC384  movaps   xmm5, xmm15
004CC388  cmp      word ptr [rip + 0x1b98a55], si  ; -> 02064DE4
004CC38F  movups   xmmword ptr [rip + 0x1b9893a], xmm0  ; -> 02064CD0
004CC396  movups   xmm0, xmmword ptr [rcx + rbx]
004CC39A  movsxd   rcx, eax
004CC39D  shufps   xmm5, xmm15, 0x55
004CC3A2  movups   xmmword ptr [rip + 0x1b98937], xmm0  ; -> 02064CE0
004CC3A9  movss    dword ptr [rip + 0x1b98927], xmm1  ; -> 02064CD8
004CC3B1  movaps   xmm13, xmm5
004CC3B5  movups   xmm0, xmmword ptr [rcx + rbx]
004CC3B9  movss    dword ptr [rip + 0x1b98927], xmm1  ; -> 02064CE8
004CC3C1  movups   xmmword ptr [rip + 0x1b98928], xmm0  ; -> 02064CF0
004CC3C8  movss    xmm0, dword ptr [rip + 0x44924c]  ; -> 0091561C [f32 1824]
004CC3D0  movss    dword ptr [rip + 0x1b98920], xmm1  ; -> 02064CF8
004CC3D8  subss    xmm11, xmm0
004CC3DD  movss    xmm1, dword ptr [rip + 0x8562fb]  ; -> 00D226E0 [f32 0.002232142]
004CC3E5  subss    xmm12, xmm0
004CC3EA  movss    dword ptr [rip + 0x1b98712], xmm1  ; -> 02064B04
004CC3F2  subss    xmm13, xmm0
004CC3F7  movups   xmmword ptr [rip + 0x1b988a2], xmm2  ; -> 02064CA0
004CC3FE  movups   xmmword ptr [rip + 0x1b988aa], xmm14  ; -> 02064CB0
004CC406  movups   xmmword ptr [rip + 0x1b988b2], xmm15  ; -> 02064CC0
004CC40E  movaps   xmmword ptr [rsp + 0x80], xmm5
004CC416  mulss    xmm8, xmm4
004CC41B  mulss    xmm10, xmm4
004CC420  je       0x4cc42d  ; -> 004CC42D
004CC422  movss    dword ptr [rip + 0x1b986da], xmm4  ; -> 02064B04
004CC42A  movaps   xmm1, xmm4
004CC42D  movss    xmm0, dword ptr [rip + 0x1b98873]  ; -> 02064CA8
004CC435  lea      eax, [r9 + 0x1c2]
004CC43C  shl      eax, 4
004CC43F  movsxd   rcx, eax
004CC442  lea      eax, [rdx + 0x1c2]
004CC448  shl      eax, 4
004CC44B  mulss    xmm0, xmm9
004CC450  movups   xmm6, xmmword ptr [rcx + rbx]
004CC454  movsxd   rcx, eax
004CC457  lea      eax, [r8 + 0x1c2]
004CC45E  shl      eax, 4
004CC461  mulss    xmm2, xmm9
004CC466  movsx    r8d, di
004CC46A  movups   xmm5, xmmword ptr [rcx + rbx]
004CC46E  movsxd   rcx, eax
004CC471  mov      edx, r8d
004CC474  cvttss2si eax, xmm2
004CC478  shl      edx, 4
004CC47B  movups   xmm4, xmmword ptr [rcx + rbx]
004CC47F  mov      dword ptr [rip + 0x1b9881b], eax  ; -> 02064CA0
004CC485  movups   xmmword ptr [rip + 0x1b987d4], xmm6  ; -> 02064C60
004CC48C  movups   xmmword ptr [rip + 0x1b987dd], xmm5  ; -> 02064C70
004CC493  movss    xmm2, dword ptr [rip + 0x1b987d9]  ; -> 02064C74
004CC49B  movups   xmmword ptr [rip + 0x1b987de], xmm4  ; -> 02064C80
004CC4A2  mulss    xmm3, xmm9
004CC4A7  mulss    xmm11, xmm1
004CC4AC  cvttss2si eax, xmm3
004CC4B0  movss    xmm3, dword ptr [rip + 0x1b987ac]  ; -> 02064C64
004CC4B8  mov      dword ptr [rip + 0x1b987e6], eax  ; -> 02064CA4
004CC4BE  cvttss2si eax, xmm0
004CC4C2  movups   xmm0, xmmword ptr [rip + 0x1b986f7]  ; -> 02064BC0
004CC4C9  mov      dword ptr [rip + 0x1b987d9], eax  ; -> 02064CA8
004CC4CF  lea      eax, [rdx + 0x10]
004CC4D2  movsxd   rcx, eax
004CC4D5  mulss    xmm12, xmm1
004CC4DA  mulss    xmm13, xmm1
004CC4DF  movss    xmm1, dword ptr [rip + 0x1b9879d]  ; -> 02064C84
004CC4E7  movups   xmmword ptr [rcx + rbx], xmm0
004CC4EB  movss    xmm0, dword ptr [rip + 0x1b986b9]  ; -> 02064BAC
004CC4F3  mulss    xmm6, xmm0
004CC4F7  mulss    xmm3, xmm0
004CC4FB  mulss    xmm5, xmm0
004CC4FF  addss    xmm7, xmm6
004CC503  mulss    xmm2, xmm0
004CC507  addss    xmm11, xmm3
004CC50C  mulss    xmm4, xmm0
004CC510  addss    xmm8, xmm5
004CC515  mulss    xmm1, xmm0
004CC519  addss    xmm12, xmm2
004CC51E  movaps   xmm0, xmmword ptr [rsp + 0x40]
004CC523  addss    xmm10, xmm4
004CC528  mulss    xmm0, xmm9
004CC52D  mulss    xmm14, xmm9
004CC532  addss    xmm13, xmm1
004CC537  mulss    xmm15, xmm9
004CC53C  cvttss2si eax, xmm14
004CC541  movups   xmm14, xmmword ptr [rip + 0x1b98677]  ; -> 02064BC0
004CC549  mov      dword ptr [rip + 0x1b98761], eax  ; -> 02064CB0
004CC54F  cvttss2si eax, xmm0
004CC553  movss    xmm0, dword ptr [rip + 0x1b9875d]  ; -> 02064CB8
004CC55B  mov      dword ptr [rip + 0x1b98753], eax  ; -> 02064CB4
004CC561  mulss    xmm0, xmm9
004CC566  movss    dword ptr [rip + 0x1b986f2], xmm6  ; -> 02064C60
004CC56E  movss    dword ptr [rip + 0x1b986ee], xmm3  ; -> 02064C64
004CC576  cvttss2si eax, xmm0
004CC57A  movaps   xmm0, xmmword ptr [rsp + 0x80]
004CC582  mov      dword ptr [rip + 0x1b98730], eax  ; -> 02064CB8
004CC588  lea      eax, [r8 + 4]
004CC58C  shl      eax, 4
004CC58F  movsxd   rcx, eax
004CC592  cvttss2si eax, xmm15
004CC597  mulss    xmm0, xmm9
004CC59C  mov      dword ptr [rip + 0x1b9871e], eax  ; -> 02064CC0
004CC5A2  movss    dword ptr [rip + 0x1b986c6], xmm5  ; -> 02064C70
004CC5AA  movss    dword ptr [rip + 0x1b986c2], xmm2  ; -> 02064C74
004CC5B2  cvttss2si eax, xmm0
004CC5B6  movss    xmm0, dword ptr [rip + 0x1b9870a]  ; -> 02064CC8
004CC5BE  mov      dword ptr [rip + 0x1b98700], eax  ; -> 02064CC4
004CC5C4  movss    dword ptr [rip + 0x1b986b4], xmm4  ; -> 02064C80
004CC5CC  movss    dword ptr [rip + 0x1b986b0], xmm1  ; -> 02064C84
004CC5D4  movups   xmmword ptr [rcx + rbx], xmm14
004CC5D9  movss    xmm1, dword ptr [rip + 0x1b98737]  ; -> 02064D18
004CC5E1  add      di, 9
004CC5E5  movss    xmm2, dword ptr [rip + 0x1b98723]  ; -> 02064D10
004CC5ED  inc      word ptr [rip + 0x1b987c4]  ; -> 02064DB8
004CC5F4  mulss    xmm0, xmm9
004CC5F9  mov      word ptr [rip + 0x1b987b4], di  ; -> 02064DB4
004CC600  mulss    xmm7, xmm1
004CC604  cvttss2si eax, xmm0
004CC608  movss    xmm0, dword ptr [rip + 0x1b9870c]  ; -> 02064D1C
004CC610  addss    xmm7, xmm2
004CC614  mov      dword ptr [rip + 0x1b986ae], eax  ; -> 02064CC8
004CC61A  lea      eax, [r8 + 7]
004CC61E  shl      eax, 4
004CC621  movsxd   rcx, eax
004CC624  lea      eax, [r8 + 2]
004CC628  shl      eax, 4
004CC62B  mulss    xmm11, xmm0
004CC630  movups   xmmword ptr [rcx + rbx], xmm14
004CC635  movsxd   rcx, eax
004CC638  lea      eax, [r8 + 5]
004CC63C  shl      eax, 4
004CC63F  mulss    xmm12, xmm0
004CC644  mulss    xmm13, xmm0
004CC649  movups   xmm0, xmmword ptr [rip + 0x1b98650]  ; -> 02064CA0
004CC650  mulss    xmm8, xmm1
004CC655  movups   xmmword ptr [rcx + rbx], xmm0
004CC659  movsxd   rcx, eax
004CC65C  lea      eax, [r8 + 8]
004CC660  movups   xmm0, xmmword ptr [rip + 0x1b98649]  ; -> 02064CB0
004CC667  shl      eax, 4
004CC66A  mulss    xmm10, xmm1
004CC66F  addss    xmm8, xmm2
004CC674  movss    xmm1, dword ptr [rip + 0x1b98698]  ; -> 02064D14
004CC67C  movups   xmmword ptr [rcx + rbx], xmm0
004CC680  movsxd   rcx, eax
004CC683  movups   xmm0, xmmword ptr [rip + 0x1b98636]  ; -> 02064CC0
004CC68A  movsxd   rax, edx
004CC68D  mov      rdx, r14
004CC690  addss    xmm11, xmm1
004CC695  movss    dword ptr [rip + 0x1b98633], xmm7  ; -> 02064CD0
004CC69D  movups   xmmword ptr [rcx + rbx], xmm0
004CC6A1  addss    xmm12, xmm1
004CC6A6  movss    dword ptr [rip + 0x1b98631], xmm8  ; -> 02064CE0
004CC6AF  addss    xmm10, xmm2
004CC6B4  movss    dword ptr [rip + 0x1b98617], xmm11  ; -> 02064CD4
004CC6BD  addss    xmm13, xmm1
004CC6C2  movups   xmm0, xmmword ptr [rip + 0x1b98607]  ; -> 02064CD0
004CC6C9  movss    dword ptr [rip + 0x1b98612], xmm12  ; -> 02064CE4
004CC6D2  movups   xmmword ptr [rax + rbx], xmm0
004CC6D6  lea      eax, [r8 + 3]
004CC6DA  movups   xmm0, xmmword ptr [rip + 0x1b985ff]  ; -> 02064CE0
004CC6E1  shl      eax, 4
004CC6E4  movsxd   rcx, eax
004CC6E7  lea      eax, [r8 + 6]
004CC6EB  shl      eax, 4
004CC6EE  movss    dword ptr [rip + 0x1b985f9], xmm10  ; -> 02064CF0
004CC6F7  movss    dword ptr [rip + 0x1b985f4], xmm13  ; -> 02064CF4
004CC700  movups   xmmword ptr [rcx + rbx], xmm0
004CC704  movsxd   rcx, eax
004CC707  movups   xmm0, xmmword ptr [rip + 0x1b985e2]  ; -> 02064CF0
004CC70E  movups   xmmword ptr [rcx + rbx], xmm0
004CC712  mov      rcx, rbp
004CC715  call     0x4c7f00  ; -> 004C7F00 fn
004CC71A  movzx    ecx, word ptr [rip + 0x1b986b7]  ; -> 02064DD8
004CC721  movzx    eax, word ptr [rip + 0x1b986ac]  ; -> 02064DD4
004CC728  inc      cx
004CC72B  movzx    esi, word ptr [rip + 0x1b983da]  ; -> 02064B0C
004CC732  movzx    edi, word ptr [rip + 0x1b9867b]  ; -> 02064DB4
004CC739  movss    xmm4, dword ptr [rip + 0x3f93ef]  ; -> 008C5B30 [f32 0.001953125]
004CC741  movss    xmm13, dword ptr [rip + 0x448ece]  ; -> 00915618 [f32 1792]
004CC74A  mov      word ptr [rip + 0x1b98687], cx  ; -> 02064DD8
004CC751  test     ax, ax
004CC754  jg       0x4cc2a0  ; -> 004CC2A0
004CC75A  movss    xmm7, dword ptr [rip + 0x448eba]  ; -> 0091561C [f32 1824]
004CC762  movzx    ecx, word ptr [rip + 0x1b98677]  ; -> 02064DE0
004CC769  cmp      cx, si
004CC76C  je       0x4cc0f5  ; -> 004CC0F5
004CC772  lea      eax, [rsi + 3]
004CC775  mov      word ptr [rip + 0x1b98654], ax  ; -> 02064DD0
004CC77C  movsx    eax, cx
004CC77F  movzx    ecx, si
004CC782  mov      word ptr [rip + 0x1b9864f], cx  ; -> 02064DD8
004CC789  add      ax, si
004CC78C  nop      dword ptr [rax]
004CC790  movss    xmm1, dword ptr [rip + 0x19360a0]  ; -> 01E02838 [u32 0x00000000]
004CC798  dec      ax
004CC79B  addss    xmm1, dword ptr [rip + 0x1936099]  ; -> 01E0283C [f32 1]
004CC7A3  mov      word ptr [rip + 0x1b9862a], ax  ; -> 02064DD4
004CC7AA  movsx    edx, cx
004CC7AD  lea      eax, [rdx + 0x12c]
004CC7B3  shl      eax, 4
004CC7B6  movsxd   rcx, eax
004CC7B9  lea      eax, [rdx + 0x15e]
004CC7BF  shl      eax, 4
004CC7C2  movsx    r8d, word ptr [rcx + rbx]
004CC7C7  movsx    r9d, word ptr [rcx + rbx + 4]
004CC7CD  movsxd   rcx, eax
004CC7D0  mov      word ptr [rip + 0x1b985e4], r8w  ; -> 02064DBC
004CC7D8  lea      eax, [r8 + 0x190]
004CC7DF  mov      word ptr [rip + 0x1b985d9], r9w  ; -> 02064DC0
004CC7E7  shl      eax, 4
004CC7EA  movups   xmm0, xmmword ptr [rcx + rbx]
004CC7EE  movsxd   rcx, eax
004CC7F1  lea      eax, [r9 + 0x190]
004CC7F8  shl      eax, 4
004CC7FB  movups   xmmword ptr [rip + 0x1b9833e], xmm0  ; -> 02064B40
004CC802  movups   xmm2, xmmword ptr [rcx + rbx]
004CC806  movsxd   rcx, eax
004CC809  lea      eax, [r8 + 0x1f4]
004CC810  shl      eax, 4
004CC813  movaps   xmm10, xmm2
004CC817  subss    xmm10, xmm13
004CC81C  movups   xmm3, xmmword ptr [rcx + rbx]
004CC820  movsxd   rcx, eax
004CC823  lea      eax, [r9 + 0x1f4]
004CC82A  shl      eax, 4
004CC82D  movaps   xmm11, xmm3
004CC831  subss    xmm11, xmm13
004CC836  movups   xmm5, xmmword ptr [rcx + rbx]
004CC83A  movsxd   rcx, eax
004CC83D  lea      eax, [r8 + 0x258]
004CC844  shl      eax, 4
004CC847  movaps   xmm12, xmm5
004CC84B  subss    xmm12, xmm13
004CC850  movups   xmm6, xmmword ptr [rcx + rbx]
004CC854  movsxd   rcx, eax
004CC857  lea      eax, [r9 + 0x258]
004CC85E  shl      eax, 4
004CC861  movaps   xmm13, xmm6
004CC865  subss    xmm13, dword ptr [rip + 0x448daa]  ; -> 00915618 [f32 1792]
004CC86E  movups   xmm0, xmmword ptr [rcx + rbx]
004CC872  movsxd   rcx, eax
004CC875  lea      eax, [r8 + 0x2bc]
004CC87C  shl      eax, 4
004CC87F  movups   xmmword ptr [rip + 0x1b9844a], xmm0  ; -> 02064CD0
004CC886  movups   xmm0, xmmword ptr [rcx + rbx]
004CC88A  movsxd   rcx, eax
004CC88D  lea      eax, [r9 + 0x2bc]
004CC894  shl      eax, 4
004CC897  movups   xmmword ptr [rip + 0x1b98442], xmm0  ; -> 02064CE0
004CC89E  movups   xmm0, xmmword ptr [rcx + rbx]
004CC8A2  movsxd   rcx, eax
004CC8A5  movss    dword ptr [rip + 0x1b9842b], xmm1  ; -> 02064CD8
004CC8AD  movups   xmmword ptr [rip + 0x1b9843c], xmm0  ; -> 02064CF0
004CC8B4  movups   xmm0, xmmword ptr [rcx + rbx]
004CC8B8  movss    dword ptr [rip + 0x1b98428], xmm1  ; -> 02064CE8
004CC8C0  movups   xmmword ptr [rip + 0x1b98439], xmm0  ; -> 02064D00
004CC8C7  movaps   xmm0, xmm2
004CC8CA  shufps   xmm0, xmm2, 0x55
004CC8CE  movaps   xmm14, xmm0
004CC8D2  movaps   xmmword ptr [rsp + 0x80], xmm0
004CC8DA  movaps   xmm0, xmm3
004CC8DD  subss    xmm14, xmm7
004CC8E2  shufps   xmm0, xmm3, 0x55
004CC8E6  movaps   xmm15, xmm0
004CC8EA  movaps   xmmword ptr [rsp + 0xa0], xmm0
004CC8F2  subss    xmm15, xmm7
004CC8F7  movups   xmmword ptr [rsp + 0x40], xmm2
004CC8FC  movups   xmmword ptr [rip + 0x1b9838d], xmm2  ; -> 02064C90
004CC903  movups   xmmword ptr [rsp + 0xb0], xmm3
004CC90B  movups   xmmword ptr [rip + 0x1b9838e], xmm3  ; -> 02064CA0
004CC912  movups   xmmword ptr [rsp + 0x90], xmm5
004CC91A  movups   xmmword ptr [rip + 0x1b9838f], xmm5  ; -> 02064CB0
004CC921  movups   xmmword ptr [rsp + 0xd0], xmm6
004CC929  movups   xmmword ptr [rip + 0x1b98390], xmm6  ; -> 02064CC0
004CC930  cmp      word ptr [rip + 0x1b984ad], si  ; -> 02064DE4
004CC937  movaps   xmm0, xmm5
004CC93A  shufps   xmm0, xmm5, 0x55
004CC93E  movss    xmm5, dword ptr [rip + 0x855d9a]  ; -> 00D226E0 [f32 0.002232142]
004CC946  movaps   xmm2, xmm0
004CC949  movaps   xmmword ptr [rsp + 0xe0], xmm0
004CC951  subss    xmm2, xmm7
004CC955  movaps   xmm0, xmm6
004CC958  movss    dword ptr [rip + 0x1b98398], xmm1  ; -> 02064CF8
004CC960  shufps   xmm0, xmm6, 0x55
004CC964  movaps   xmm3, xmm0
004CC967  movss    dword ptr [rip + 0x1b98399], xmm1  ; -> 02064D08
004CC96F  subss    xmm3, xmm7
004CC973  movss    dword ptr [rip + 0x1b98189], xmm5  ; -> 02064B04
004CC97B  movaps   xmmword ptr [rsp + 0xc0], xmm0
004CC983  mulss    xmm10, xmm4
004CC988  mulss    xmm11, xmm4
004CC98D  mulss    xmm12, xmm4
004CC992  mulss    xmm13, xmm4
004CC997  je       0x4cc9a4  ; -> 004CC9A4
004CC999  movss    dword ptr [rip + 0x1b98163], xmm4  ; -> 02064B04
004CC9A1  movaps   xmm5, xmm4
004CC9A4  movups   xmm0, xmmword ptr [rsp + 0x40]
004CC9A9  lea      eax, [r8 + 0x1c2]
004CC9B0  movups   xmm1, xmmword ptr [rsp + 0xb0]
004CC9B8  shl      eax, 4
004CC9BB  movsxd   rcx, eax
004CC9BE  lea      eax, [r9 + 0x1c2]
004CC9C5  shl      eax, 4
004CC9C8  mulss    xmm0, xmm9
004CC9CD  movups   xmm8, xmmword ptr [rcx + rbx]
004CC9D2  movsxd   rcx, eax
004CC9D5  lea      eax, [r8 + 0x226]
004CC9DC  shl      eax, 4
004CC9DF  mulss    xmm1, xmm9
004CC9E4  movsx    r8d, di
004CC9E8  movups   xmm7, xmmword ptr [rcx + rbx]
004CC9EC  movsxd   rcx, eax
004CC9EF  mov      edx, r8d
004CC9F2  mulss    xmm2, xmm5
004CC9F6  lea      eax, [r9 + 0x226]
004CC9FD  shl      eax, 4
004CCA00  shl      edx, 4
004CCA03  movups   xmm6, xmmword ptr [rcx + rbx]
004CCA07  movsxd   rcx, eax
004CCA0A  cvttss2si eax, xmm0
004CCA0E  movaps   xmm0, xmmword ptr [rsp + 0x80]
004CCA16  mov      dword ptr [rip + 0x1b98274], eax  ; -> 02064C90
004CCA1C  mulss    xmm0, xmm9
004CCA21  mulss    xmm3, xmm5
004CCA25  cvttss2si eax, xmm0
004CCA29  movss    xmm0, dword ptr [rip + 0x1b98267]  ; -> 02064C98
004CCA31  mov      dword ptr [rip + 0x1b9825d], eax  ; -> 02064C94
004CCA37  mulss    xmm0, xmm9
004CCA3C  mulss    xmm14, xmm5
004CCA41  cvttss2si eax, xmm0
004CCA45  movaps   xmm0, xmmword ptr [rsp + 0xa0]
004CCA4D  mov      dword ptr [rip + 0x1b98245], eax  ; -> 02064C98
004CCA53  lea      eax, [rdx + 0x10]
004CCA56  mulss    xmm0, xmm9
004CCA5B  mulss    xmm15, xmm5
004CCA60  movups   xmm5, xmmword ptr [rcx + rbx]
004CCA64  movsxd   rcx, eax
004CCA67  cvttss2si eax, xmm1
004CCA6B  movups   xmm1, xmmword ptr [rsp + 0x90]
004CCA73  mov      dword ptr [rip + 0x1b98227], eax  ; -> 02064CA0
004CCA79  cvttss2si eax, xmm0
004CCA7D  movss    xmm0, dword ptr [rip + 0x1b98223]  ; -> 02064CA8
004CCA85  mov      dword ptr [rip + 0x1b98219], eax  ; -> 02064CA4
004CCA8B  mulss    xmm0, xmm9
004CCA90  mulss    xmm1, xmm9
004CCA95  cvttss2si eax, xmm0
004CCA99  movaps   xmm0, xmmword ptr [rsp + 0xe0]
004CCAA1  mov      dword ptr [rip + 0x1b98201], eax  ; -> 02064CA8
004CCAA7  lea      eax, [r8 + 4]
004CCAAB  shl      eax, 4
004CCAAE  mulss    xmm0, xmm9
004CCAB3  movss    dword ptr [rsp + 0x30], xmm2
004CCAB9  movups   xmm2, xmmword ptr [rip + 0x1b980d0]  ; -> 02064B90
004CCAC0  movss    dword ptr [rsp + 0x20], xmm3
004CCAC6  movups   xmmword ptr [rcx + rbx], xmm2
004CCACA  movsxd   rcx, eax
004CCACD  cvttss2si eax, xmm1
004CCAD1  movups   xmm1, xmmword ptr [rsp + 0xd0]
004CCAD9  mov      dword ptr [rip + 0x1b981d1], eax  ; -> 02064CB0
004CCADF  cvttss2si eax, xmm0
004CCAE3  movss    xmm0, dword ptr [rip + 0x1b981cd]  ; -> 02064CB8
004CCAEB  mov      dword ptr [rip + 0x1b981c3], eax  ; -> 02064CB4
004CCAF1  movups   xmmword ptr [rcx + rbx], xmm2
004CCAF5  mulss    xmm0, xmm9
004CCAFA  mulss    xmm1, xmm9
004CCAFF  cvttss2si eax, xmm0
004CCB03  movups   xmmword ptr [rip + 0x1b98145], xmm8  ; -> 02064C50
004CCB0B  mov      dword ptr [rip + 0x1b981a7], eax  ; -> 02064CB8
004CCB11  lea      eax, [r8 + 7]
004CCB15  shl      eax, 4
004CCB18  movsxd   rcx, eax
004CCB1B  cvttss2si eax, xmm1
004CCB1F  movups   xmmword ptr [rip + 0x1b9813a], xmm7  ; -> 02064C60
004CCB26  mov      dword ptr [rip + 0x1b98194], eax  ; -> 02064CC0
004CCB2C  movups   xmmword ptr [rip + 0x1b9813d], xmm6  ; -> 02064C70
004CCB33  movups   xmmword ptr [rip + 0x1b98146], xmm5  ; -> 02064C80
004CCB3A  movups   xmmword ptr [rcx + rbx], xmm2
004CCB3E  movss    xmm3, dword ptr [rip + 0x1b98066]  ; -> 02064BAC
004CCB46  movaps   xmm0, xmmword ptr [rsp + 0xc0]
004CCB4E  movss    xmm4, dword ptr [rip + 0x1b980fe]  ; -> 02064C54
004CCB56  movss    xmm1, dword ptr [rip + 0x1b98116]  ; -> 02064C74
004CCB5E  mulss    xmm0, xmm9
004CCB63  mulss    xmm4, xmm3
004CCB67  cvttss2si eax, xmm0
004CCB6B  movss    xmm0, dword ptr [rip + 0x1b98155]  ; -> 02064CC8
004CCB73  addss    xmm14, xmm4
004CCB78  mov      dword ptr [rip + 0x1b98146], eax  ; -> 02064CC4
004CCB7E  mulss    xmm0, xmm9
004CCB83  mulss    xmm1, xmm3
004CCB87  cvttss2si eax, xmm0
004CCB8B  movss    xmm0, dword ptr [rip + 0x1b980f1]  ; -> 02064C84
004CCB93  mulss    xmm0, xmm3
004CCB97  mov      dword ptr [rip + 0x1b9812b], eax  ; -> 02064CC8
004CCB9D  lea      eax, [r8 + 0xa]
004CCBA1  shl      eax, 4
004CCBA4  movsxd   rcx, eax
004CCBA7  lea      eax, [r8 + 2]
004CCBAB  mulss    xmm8, xmm3
004CCBB0  shl      eax, 4
004CCBB3  mulss    xmm7, xmm3
004CCBB7  movups   xmmword ptr [rcx + rbx], xmm2
004CCBBB  movsxd   rcx, eax
004CCBBE  lea      eax, [r8 + 5]
004CCBC2  movss    xmm2, dword ptr [rip + 0x1b9809a]  ; -> 02064C64
004CCBCA  addss    xmm10, xmm8
004CCBCF  mulss    xmm2, xmm3
004CCBD3  addss    xmm11, xmm7
004CCBD8  shl      eax, 4
004CCBDB  mulss    xmm6, xmm3
004CCBDF  mulss    xmm5, xmm3
004CCBE3  addss    xmm15, xmm2
004CCBE8  movss    xmm3, dword ptr [rsp + 0x30]
004CCBEE  addss    xmm12, xmm6
004CCBF3  addss    xmm3, xmm1
004CCBF7  movss    dword ptr [rip + 0x1b98085], xmm0  ; -> 02064C84
004CCBFF  movss    dword ptr [rip + 0x1b9804d], xmm4  ; -> 02064C54
004CCC07  addss    xmm13, xmm5
004CCC0C  movss    xmm4, dword ptr [rsp + 0x20]
004CCC12  addss    xmm4, xmm0
004CCC16  movss    dword ptr [rip + 0x1b98056], xmm1  ; -> 02064C74
004CCC1E  movss    xmm0, dword ptr [rip + 0x1b980f6]  ; -> 02064D1C
004CCC26  movss    xmm1, dword ptr [rip + 0x1b980ea]  ; -> 02064D18
004CCC2E  mulss    xmm15, xmm0
004CCC33  mulss    xmm14, xmm0
004CCC38  mulss    xmm3, xmm0
004CCC3C  mulss    xmm4, xmm0
004CCC40  movups   xmm0, xmmword ptr [rip + 0x1b98049]  ; -> 02064C90
004CCC47  mulss    xmm10, xmm1
004CCC4C  movups   xmmword ptr [rcx + rbx], xmm0
004CCC50  movsxd   rcx, eax
004CCC53  lea      eax, [r8 + 8]
004CCC57  movups   xmm0, xmmword ptr [rip + 0x1b98042]  ; -> 02064CA0
004CCC5E  shl      eax, 4
004CCC61  mulss    xmm11, xmm1
004CCC66  mulss    xmm12, xmm1
004CCC6B  movups   xmmword ptr [rcx + rbx], xmm0
004CCC6F  movsxd   rcx, eax
004CCC72  movups   xmm0, xmmword ptr [rip + 0x1b98037]  ; -> 02064CB0
004CCC79  movss    dword ptr [rip + 0x1b97fe3], xmm2  ; -> 02064C64
004CCC81  movss    xmm2, dword ptr [rip + 0x1b98087]  ; -> 02064D10
004CCC89  mulss    xmm13, xmm1
004CCC8E  addss    xmm10, xmm2
004CCC93  movss    xmm1, dword ptr [rip + 0x1b98079]  ; -> 02064D14
004CCC9B  addss    xmm11, xmm2
004CCCA0  addss    xmm14, xmm1
004CCCA5  movss    dword ptr [rip + 0x1b97fa2], xmm8  ; -> 02064C50
004CCCAE  addss    xmm15, xmm1
004CCCB3  movss    dword ptr [rip + 0x1b97fa5], xmm7  ; -> 02064C60
004CCCBB  addss    xmm12, xmm2
004CCCC0  movss    dword ptr [rip + 0x1b97fa8], xmm6  ; -> 02064C70
004CCCC8  addss    xmm3, xmm1
004CCCCC  movss    dword ptr [rip + 0x1b97fac], xmm5  ; -> 02064C80
004CCCD4  movss    dword ptr [rip + 0x1b97ff3], xmm10  ; -> 02064CD0
004CCCDD  movss    dword ptr [rip + 0x1b97fee], xmm14  ; -> 02064CD4
004CCCE6  movss    dword ptr [rip + 0x1b97ff1], xmm11  ; -> 02064CE0
004CCCEF  movss    dword ptr [rip + 0x1b97fec], xmm15  ; -> 02064CE4
004CCCF8  movss    dword ptr [rip + 0x1b97fef], xmm12  ; -> 02064CF0
004CCD01  movss    dword ptr [rip + 0x1b97feb], xmm3  ; -> 02064CF4
004CCD09  inc      word ptr [rip + 0x1b980a8]  ; -> 02064DB8
004CCD10  lea      eax, [r8 + 0xb]
004CCD14  movups   xmmword ptr [rcx + rbx], xmm0
004CCD18  shl      eax, 4
004CCD1B  add      di, 0xc
004CCD1F  movups   xmm0, xmmword ptr [rip + 0x1b97f9a]  ; -> 02064CC0
004CCD26  movsxd   rcx, eax
004CCD29  movsxd   rax, edx
004CCD2C  addss    xmm13, xmm2
004CCD31  addss    xmm4, xmm1
004CCD35  mov      word ptr [rip + 0x1b98078], di  ; -> 02064DB4
004CCD3C  mov      rdx, r14
004CCD3F  movups   xmmword ptr [rcx + rbx], xmm0
004CCD43  movups   xmm0, xmmword ptr [rip + 0x1b97f86]  ; -> 02064CD0
004CCD4A  movss    dword ptr [rip + 0x1b97fad], xmm13  ; -> 02064D00
004CCD53  movups   xmmword ptr [rax + rbx], xmm0
004CCD57  lea      eax, [r8 + 3]
004CCD5B  movups   xmm0, xmmword ptr [rip + 0x1b97f7e]  ; -> 02064CE0
004CCD62  shl      eax, 4
004CCD65  movsxd   rcx, eax
004CCD68  lea      eax, [r8 + 6]
004CCD6C  shl      eax, 4
004CCD6F  movss    dword ptr [rip + 0x1b97f8d], xmm4  ; -> 02064D04
004CCD77  movups   xmmword ptr [rcx + rbx], xmm0
004CCD7B  movsxd   rcx, eax
004CCD7E  lea      eax, [r8 + 9]
004CCD82  movups   xmm0, xmmword ptr [rip + 0x1b97f67]  ; -> 02064CF0
004CCD89  shl      eax, 4
004CCD8C  movups   xmmword ptr [rcx + rbx], xmm0
004CCD90  movsxd   rcx, eax
004CCD93  movups   xmm0, xmmword ptr [rip + 0x1b97f66]  ; -> 02064D00
004CCD9A  movups   xmmword ptr [rcx + rbx], xmm0
004CCD9E  mov      rcx, rbp
004CCDA1  call     0x4c7f00  ; -> 004C7F00 fn
004CCDA6  movzx    ecx, word ptr [rip + 0x1b9802b]  ; -> 02064DD8
004CCDAD  movzx    eax, word ptr [rip + 0x1b98020]  ; -> 02064DD4
004CCDB4  inc      cx
004CCDB7  movzx    esi, word ptr [rip + 0x1b97d4e]  ; -> 02064B0C
004CCDBE  mov      word ptr [rip + 0x1b98013], cx  ; -> 02064DD8
004CCDC5  test     ax, ax
004CCDC8  jle      0x4cc0f5  ; -> 004CC0F5
004CCDCE  movzx    edi, word ptr [rip + 0x1b97fdf]  ; -> 02064DB4
004CCDD5  movss    xmm4, dword ptr [rip + 0x3f8d53]  ; -> 008C5B30 [f32 0.001953125]
004CCDDD  movss    xmm13, dword ptr [rip + 0x448832]  ; -> 00915618 [f32 1792]
004CCDE6  movss    xmm7, dword ptr [rip + 0x44882e]  ; -> 0091561C [f32 1824]
004CCDEE  jmp      0x4cc790  ; -> 004CC790
004CCDF3  movss    xmm4, dword ptr [rip + 0x1935a35]  ; -> 01E02830 [u32 0x00000000]
004CCDFB  lea      rdx, [rip + 0x1b97d8e]  ; -> 02064B90
004CCE02  movss    xmm5, dword ptr [rip + 0x1b97dc2]  ; -> 02064BCC
004CCE0A  lea      rcx, [rip + 0x1b97d7f]  ; -> 02064B90
004CCE11  movss    xmm8, dword ptr [rip + 0x1b97da6]  ; -> 02064BC0
004CCE1A  movaps   xmm0, xmm5
004CCE1D  movss    xmm7, dword ptr [rip + 0x1b97d9f]  ; -> 02064BC4
004CCE25  movaps   xmm3, xmm8
004CCE29  movss    xmm6, dword ptr [rip + 0x1b97d97]  ; -> 02064BC8
004CCE31  movaps   xmm2, xmm7
004CCE34  mulss    xmm3, dword ptr [rip + 0x1b97dd4]  ; -> 02064C10
004CCE3C  movaps   xmm1, xmm6
004CCE3F  mov      dword ptr [rip + 0x1b97cbb], 0x437f0000  ; -> 02064B04
004CCE49  mulss    xmm2, dword ptr [rip + 0x1b97dc3]  ; -> 02064C14
004CCE51  mulss    xmm1, dword ptr [rip + 0x1b97dbf]  ; -> 02064C18
004CCE59  maxss    xmm3, xmm4
004CCE5D  mulss    xmm0, dword ptr [rip + 0x1b97db7]  ; -> 02064C1C
004CCE65  maxss    xmm2, xmm4
004CCE69  mulss    xmm8, dword ptr [rip + 0x1b97d8e]  ; -> 02064C00
004CCE72  maxss    xmm1, xmm4
004CCE76  mulss    xmm7, dword ptr [rip + 0x1b97d86]  ; -> 02064C04
004CCE7E  maxss    xmm0, xmm4
004CCE82  mulss    xmm6, dword ptr [rip + 0x1b97d7e]  ; -> 02064C08
004CCE8A  maxss    xmm8, xmm4
004CCE8F  mulss    xmm5, dword ptr [rip + 0x1b97d75]  ; -> 02064C0C
004CCE97  maxss    xmm7, xmm4
004CCE9B  movss    dword ptr [rip + 0x1b97ced], xmm3  ; -> 02064B90
004CCEA3  maxss    xmm6, xmm4
004CCEA7  movss    xmm3, dword ptr [rip + 0x3f8c91]  ; -> 008C5B40 [f32 255]
004CCEAF  movss    dword ptr [rip + 0x1b97cdd], xmm2  ; -> 02064B94
004CCEB7  maxss    xmm5, xmm4
004CCEBB  movaps   xmm2, xmm3
004CCEBE  movss    dword ptr [rip + 0x1b97cd2], xmm1  ; -> 02064B98
004CCEC6  movss    dword ptr [rip + 0x1b97cce], xmm0  ; -> 02064B9C
004CCECE  movss    dword ptr [rip + 0x1b97ce9], xmm8  ; -> 02064BC0
004CCED7  movss    dword ptr [rip + 0x1b97ce5], xmm7  ; -> 02064BC4
004CCEDF  movss    dword ptr [rip + 0x1b97ce1], xmm6  ; -> 02064BC8
004CCEE7  movss    dword ptr [rip + 0x1b97cdd], xmm5  ; -> 02064BCC
004CCEEF  call     0x4cf230  ; -> 004CF230 fn
004CCEF4  lea      rdx, [rip + 0x1b97cc5]  ; -> 02064BC0
004CCEFB  lea      rcx, [rip + 0x1b97cbe]  ; -> 02064BC0
004CCF02  call     0x4cf230  ; -> 004CF230 fn
004CCF07  movups   xmm0, xmmword ptr [rip + 0x1b97c82]  ; -> 02064B90
004CCF0E  movzx    eax, word ptr [rip + 0x1b97ec7]  ; -> 02064DDC
004CCF15  movss    xmm6, dword ptr [rip + 0x181ed67]  ; -> 01CEBC84 [f32 16]
004CCF1D  movss    xmm8, dword ptr [rip + 0x4486f2]  ; -> 00915618 [f32 1792]
004CCF26  movss    xmm12, dword ptr [rip + 0x3f8c01]  ; -> 008C5B30 [f32 0.001953125]
004CCF2F  cvttps2dq xmm1, xmm0
004CCF33  movups   xmm0, xmmword ptr [rip + 0x1b97c86]  ; -> 02064BC0
004CCF3A  movups   xmmword ptr [rip + 0x1b97c4f], xmm1  ; -> 02064B90
004CCF41  cvttps2dq xmm2, xmm0
004CCF45  movups   xmmword ptr [rip + 0x1b97c74], xmm2  ; -> 02064BC0
004CCF4C  movss    xmm2, dword ptr [rip + 0x4486c8]  ; -> 0091561C [f32 1824]
004CCF54  cmp      ax, si
004CCF57  je       0x4cd39c  ; -> 004CD39C
004CCF5D  cwde     
004CCF5E  movzx    ecx, si
004CCF61  add      ax, si
004CCF64  mov      word ptr [rip + 0x1b97e6d], cx  ; -> 02064DD8
004CCF6B  mov      word ptr [rip + 0x1b97e5d], r8w  ; -> 02064DD0
004CCF73  movss    xmm1, dword ptr [rip + 0x19358bd]  ; -> 01E02838 [u32 0x00000000]
004CCF7B  dec      ax
004CCF7E  addss    xmm1, dword ptr [rip + 0x19358b6]  ; -> 01E0283C [f32 1]
004CCF86  mov      word ptr [rip + 0x1b97e47], ax  ; -> 02064DD4
004CCF8D  movsx    r11d, cx
004CCF91  lea      eax, [r11 + 0xc8]
004CCF98  shl      eax, 4
004CCF9B  movsxd   rcx, eax
004CCF9E  movsx    eax, word ptr [rcx + rbx]
004CCFA2  movsx    edx, word ptr [rcx + rbx + 4]
004CCFA7  mov      r10d, eax
004CCFAA  movsx    r8d, word ptr [rcx + rbx + 8]
004CCFB0  mov      word ptr [rip + 0x1b97e05], ax  ; -> 02064DBC
004CCFB7  add      eax, 0x190
004CCFBC  shl      eax, 4
004CCFBF  movsxd   rcx, eax
004CCFC2  lea      eax, [rdx + 0x190]
004CCFC8  shl      eax, 4
004CCFCB  mov      word ptr [rip + 0x1b97dee], dx  ; -> 02064DC0
004CCFD2  mov      word ptr [rip + 0x1b97dea], r8w  ; -> 02064DC4
004CCFDA  movups   xmm10, xmmword ptr [rcx + rbx]
004CCFDF  movsxd   rcx, eax
004CCFE2  lea      eax, [r8 + 0x190]
004CCFE9  shl      eax, 4
004CCFEC  movaps   xmm3, xmm10
004CCFF0  movaps   xmm14, xmm10
004CCFF4  subss    xmm3, xmm8
004CCFF9  shufps   xmm14, xmm10, 0x55
004CCFFE  movups   xmm11, xmmword ptr [rcx + rbx]
004CD003  movsxd   rcx, eax
004CD006  lea      eax, [r10 + 0x258]
004CD00D  shl      eax, 4
004CD010  movaps   xmm7, xmm14
004CD014  movaps   xmm4, xmm11
004CD018  subss    xmm7, xmm2
004CD01C  subss    xmm4, xmm8
004CD021  mulss    xmm3, xmm12
004CD026  movups   xmm13, xmmword ptr [rcx + rbx]
004CD02B  movsxd   rcx, eax
004CD02E  lea      eax, [rdx + 0x258]
004CD034  shl      eax, 4
004CD037  movaps   xmm15, xmm11
004CD03B  movaps   xmm5, xmm13
004CD03F  shufps   xmm15, xmm11, 0x55
004CD044  subss    xmm5, xmm8
004CD049  mulss    xmm4, xmm12
004CD04E  movups   xmm0, xmmword ptr [rcx + rbx]
004CD052  movsxd   rcx, eax
004CD055  lea      eax, [r8 + 0x258]
004CD05C  shl      eax, 4
004CD05F  movaps   xmm8, xmm15
004CD063  cmp      word ptr [rip + 0x1b97d7a], si  ; -> 02064DE4
004CD06A  subss    xmm8, xmm2
004CD06F  movups   xmmword ptr [rip + 0x1b97c5a], xmm0  ; -> 02064CD0
004CD076  movups   xmm0, xmmword ptr [rcx + rbx]
004CD07A  movsxd   rcx, eax
004CD07D  movss    dword ptr [rip + 0x1b97c53], xmm1  ; -> 02064CD8
004CD085  movups   xmmword ptr [rip + 0x1b97c54], xmm0  ; -> 02064CE0
004CD08C  movups   xmm0, xmmword ptr [rcx + rbx]
004CD090  movss    dword ptr [rip + 0x1b97c50], xmm1  ; -> 02064CE8
004CD098  movups   xmmword ptr [rip + 0x1b97c51], xmm0  ; -> 02064CF0
004CD09F  movaps   xmm0, xmm13
004CD0A3  movss    dword ptr [rip + 0x1b97c4d], xmm1  ; -> 02064CF8
004CD0AB  movss    xmm1, dword ptr [rip + 0x85562d]  ; -> 00D226E0 [f32 0.002232142]
004CD0B3  shufps   xmm0, xmm13, 0x55
004CD0B8  movaps   xmm9, xmm0
004CD0BC  movss    dword ptr [rip + 0x1b97a40], xmm1  ; -> 02064B04
004CD0C4  subss    xmm9, xmm2
004CD0C9  movaps   xmmword ptr [rsp + 0x40], xmm0
004CD0CE  movups   xmmword ptr [rip + 0x1b97bca], xmm10  ; -> 02064CA0
004CD0D6  movups   xmmword ptr [rip + 0x1b97bd2], xmm11  ; -> 02064CB0
004CD0DE  movups   xmmword ptr [rip + 0x1b97bda], xmm13  ; -> 02064CC0
004CD0E6  mulss    xmm5, xmm12
004CD0EB  je       0x4cd0f9  ; -> 004CD0F9
004CD0ED  movaps   xmm1, xmm12
004CD0F1  movss    dword ptr [rip + 0x1b97a0b], xmm1  ; -> 02064B04
004CD0F9  movss    xmm0, dword ptr [rip + 0x1b97ba7]  ; -> 02064CA8
004CD101  lea      eax, [r11 + 0xfa]
004CD108  shl      eax, 4
004CD10B  movsxd   rcx, eax
004CD10E  mulss    xmm0, xmm6
004CD112  movsx    r8d, di
004CD116  mulss    xmm7, xmm1
004CD11A  mov      edx, r8d
004CD11D  shl      edx, 4
004CD120  movups   xmm2, xmmword ptr [rcx + rbx]
004CD124  mulss    xmm8, xmm1
004CD129  mulss    xmm9, xmm1
004CD12E  movups   xmmword ptr [rip + 0x1b97b2b], xmm2  ; -> 02064C60
004CD135  mulss    xmm2, dword ptr [rip + 0x1b97a6f]  ; -> 02064BAC
004CD13D  movss    xmm1, dword ptr [rip + 0x1b97b1f]  ; -> 02064C64
004CD145  mulss    xmm1, dword ptr [rip + 0x1b97a5f]  ; -> 02064BAC
004CD14D  mulss    xmm10, xmm6
004CD152  addss    xmm3, xmm2
004CD156  mulss    xmm14, xmm6
004CD15B  addss    xmm4, xmm2
004CD15F  addss    xmm7, xmm1
004CD163  mulss    xmm11, xmm6
004CD168  cvttss2si eax, xmm10
004CD16D  movups   xmm10, xmmword ptr [rip + 0x1b97a4b]  ; -> 02064BC0
004CD175  mov      dword ptr [rip + 0x1b97b25], eax  ; -> 02064CA0
004CD17B  addss    xmm8, xmm1
004CD180  mulss    xmm15, xmm6
004CD185  cvttss2si eax, xmm14
004CD18A  addss    xmm9, xmm1
004CD18F  movss    dword ptr [rip + 0x1b97acd], xmm1  ; -> 02064C64
004CD197  movss    xmm1, dword ptr [rip + 0x1b97b79]  ; -> 02064D18
004CD19F  addss    xmm5, xmm2
004CD1A3  mov      dword ptr [rip + 0x1b97afb], eax  ; -> 02064CA4
004CD1A9  cvttss2si eax, xmm0
004CD1AD  movss    xmm0, dword ptr [rip + 0x1b97b03]  ; -> 02064CB8
004CD1B5  mov      dword ptr [rip + 0x1b97aed], eax  ; -> 02064CA8
004CD1BB  lea      eax, [rdx + 0x10]
004CD1BE  movsxd   rcx, eax
004CD1C1  mulss    xmm0, xmm6
004CD1C5  cvttss2si eax, xmm11
004CD1CA  movups   xmmword ptr [rcx + rbx], xmm10
004CD1CF  mov      dword ptr [rip + 0x1b97adb], eax  ; -> 02064CB0
004CD1D5  cvttss2si eax, xmm15
004CD1DA  mulss    xmm13, xmm6
004CD1DF  mov      dword ptr [rip + 0x1b97acf], eax  ; -> 02064CB4
004CD1E5  cvttss2si eax, xmm0
004CD1E9  movaps   xmm0, xmmword ptr [rsp + 0x40]
004CD1EE  mov      dword ptr [rip + 0x1b97ac4], eax  ; -> 02064CB8
004CD1F4  lea      eax, [r8 + 4]
004CD1F8  shl      eax, 4
004CD1FB  movsxd   rcx, eax
004CD1FE  mulss    xmm0, xmm6
004CD202  cvttss2si eax, xmm13
004CD207  mulss    xmm3, xmm1
004CD20B  mov      dword ptr [rip + 0x1b97aaf], eax  ; -> 02064CC0
004CD211  cvttss2si eax, xmm0
004CD215  movss    xmm0, dword ptr [rip + 0x1b97aab]  ; -> 02064CC8
004CD21D  mov      dword ptr [rip + 0x1b97aa1], eax  ; -> 02064CC4
004CD223  mulss    xmm0, xmm6
004CD227  movups   xmmword ptr [rcx + rbx], xmm10
004CD22C  cvttss2si eax, xmm0
004CD230  movss    xmm0, dword ptr [rip + 0x1b97ae4]  ; -> 02064D1C
004CD238  mov      dword ptr [rip + 0x1b97a8a], eax  ; -> 02064CC8
004CD23E  lea      eax, [r8 + 7]
004CD242  shl      eax, 4
004CD245  movsxd   rcx, eax
004CD248  lea      eax, [r8 + 2]
004CD24C  mulss    xmm7, xmm0
004CD250  shl      eax, 4
004CD253  movss    dword ptr [rip + 0x1b97a05], xmm2  ; -> 02064C60
004CD25B  movss    xmm2, dword ptr [rip + 0x1b97aad]  ; -> 02064D10
004CD263  mulss    xmm4, xmm1
004CD267  addss    xmm3, xmm2
004CD26B  mulss    xmm5, xmm1
004CD26F  movss    xmm1, dword ptr [rip + 0x1b97a9d]  ; -> 02064D14
004CD277  addss    xmm7, xmm1
004CD27B  movss    dword ptr [rip + 0x1b97a4d], xmm3  ; -> 02064CD0
004CD283  movups   xmmword ptr [rcx + rbx], xmm10
004CD288  mulss    xmm8, xmm0
004CD28D  movss    dword ptr [rip + 0x1b97a3f], xmm7  ; -> 02064CD4
004CD295  mulss    xmm9, xmm0
004CD29A  movups   xmm0, xmmword ptr [rip + 0x1b979ff]  ; -> 02064CA0
004CD2A1  inc      word ptr [rip + 0x1b97b10]  ; -> 02064DB8
004CD2A8  add      di, 9
004CD2AC  movsxd   rcx, eax
004CD2AF  addss    xmm4, xmm2
004CD2B3  lea      eax, [r8 + 5]
004CD2B7  mov      word ptr [rip + 0x1b97af6], di  ; -> 02064DB4
004CD2BE  shl      eax, 4
004CD2C1  addss    xmm8, xmm1
004CD2C6  addss    xmm5, xmm2
004CD2CA  movups   xmmword ptr [rcx + rbx], xmm0
004CD2CE  movsxd   rcx, eax
004CD2D1  lea      eax, [r8 + 8]
004CD2D5  movups   xmm0, xmmword ptr [rip + 0x1b979d4]  ; -> 02064CB0
004CD2DC  shl      eax, 4
004CD2DF  movss    dword ptr [rip + 0x1b979f9], xmm4  ; -> 02064CE0
004CD2E7  addss    xmm9, xmm1
004CD2EC  movups   xmmword ptr [rcx + rbx], xmm0
004CD2F0  movsxd   rcx, eax
004CD2F3  movups   xmm0, xmmword ptr [rip + 0x1b979c6]  ; -> 02064CC0
004CD2FA  movsxd   rax, edx
004CD2FD  mov      rdx, r14
004CD300  movss    dword ptr [rip + 0x1b979db], xmm8  ; -> 02064CE4
004CD309  movups   xmmword ptr [rcx + rbx], xmm0
004CD30D  movups   xmm0, xmmword ptr [rip + 0x1b979bc]  ; -> 02064CD0
004CD314  movss    dword ptr [rip + 0x1b979d4], xmm5  ; -> 02064CF0
004CD31C  movups   xmmword ptr [rax + rbx], xmm0
004CD320  lea      eax, [r8 + 3]
004CD324  movups   xmm0, xmmword ptr [rip + 0x1b979b5]  ; -> 02064CE0
004CD32B  shl      eax, 4
004CD32E  movsxd   rcx, eax
004CD331  lea      eax, [r8 + 6]
004CD335  shl      eax, 4
004CD338  movss    dword ptr [rip + 0x1b979b3], xmm9  ; -> 02064CF4
004CD341  movups   xmmword ptr [rcx + rbx], xmm0
004CD345  movsxd   rcx, eax
004CD348  movups   xmm0, xmmword ptr [rip + 0x1b979a1]  ; -> 02064CF0
004CD34F  movups   xmmword ptr [rcx + rbx], xmm0
004CD353  mov      rcx, rbp
004CD356  call     0x4c7f00  ; -> 004C7F00 fn
004CD35B  movzx    ecx, word ptr [rip + 0x1b97a76]  ; -> 02064DD8
004CD362  movzx    eax, word ptr [rip + 0x1b97a6b]  ; -> 02064DD4
004CD369  inc      cx
004CD36C  movzx    esi, word ptr [rip + 0x1b97799]  ; -> 02064B0C
004CD373  movzx    edi, word ptr [rip + 0x1b97a3a]  ; -> 02064DB4
004CD37A  movss    xmm8, dword ptr [rip + 0x448295]  ; -> 00915618 [f32 1792]
004CD383  mov      word ptr [rip + 0x1b97a4e], cx  ; -> 02064DD8
004CD38A  test     ax, ax
004CD38D  jle      0x4cd39c  ; -> 004CD39C
004CD38F  movss    xmm2, dword ptr [rip + 0x448285]  ; -> 0091561C [f32 1824]
004CD397  jmp      0x4ccf73  ; -> 004CCF73
004CD39C  movzx    ecx, word ptr [rip + 0x1b97a3d]  ; -> 02064DE0
004CD3A3  cmp      cx, si
004CD3A6  je       0x4cc0f5  ; -> 004CC0F5
004CD3AC  lea      eax, [rsi + 3]
004CD3AF  mov      word ptr [rip + 0x1b97a1a], ax  ; -> 02064DD0
004CD3B6  movsx    eax, cx
004CD3B9  movzx    ecx, si
004CD3BC  mov      word ptr [rip + 0x1b97a15], cx  ; -> 02064DD8
004CD3C3  add      ax, si
004CD3C6  nop      word ptr [rax + rax]
004CD3D0  movss    xmm1, dword ptr [rip + 0x1935460]  ; -> 01E02838 [u32 0x00000000]
004CD3D8  dec      ax
004CD3DB  addss    xmm1, dword ptr [rip + 0x1935459]  ; -> 01E0283C [f32 1]
004CD3E3  mov      word ptr [rip + 0x1b979ea], ax  ; -> 02064DD4
004CD3EA  movsx    edx, cx
004CD3ED  lea      eax, [rdx + 0x12c]
004CD3F3  shl      eax, 4
004CD3F6  movsxd   rcx, eax
004CD3F9  lea      eax, [rdx + 0x15e]
004CD3FF  shl      eax, 4
004CD402  movsxd   r11, eax
004CD405  movsx    r8d, word ptr [rcx + rbx]
004CD40A  movsx    r9d, word ptr [rcx + rbx + 4]
004CD410  movups   xmm0, xmmword ptr [r11 + rbx]
004CD415  mov      word ptr [rip + 0x1b9799f], r8w  ; -> 02064DBC
004CD41D  lea      eax, [r8 + 0x190]
004CD424  mov      word ptr [rip + 0x1b97994], r9w  ; -> 02064DC0
004CD42C  shl      eax, 4
004CD42F  movsxd   rcx, eax
004CD432  lea      eax, [r9 + 0x190]
004CD439  shl      eax, 4
004CD43C  movups   xmmword ptr [rip + 0x1b976fd], xmm0  ; -> 02064B40
004CD443  movups   xmm13, xmmword ptr [rcx + rbx]
004CD448  movsxd   rcx, eax
004CD44B  lea      eax, [r8 + 0x1f4]
004CD452  shl      eax, 4
004CD455  movaps   xmm3, xmm13
004CD459  subss    xmm3, xmm8
004CD45E  movups   xmm14, xmmword ptr [rcx + rbx]
004CD463  movsxd   rcx, eax
004CD466  lea      eax, [r9 + 0x1f4]
004CD46D  shl      eax, 4
004CD470  movaps   xmm4, xmm14
004CD474  movaps   xmm9, xmm14
004CD478  subss    xmm4, xmm8
004CD47D  shufps   xmm9, xmm14, 0x55
004CD482  movups   xmm15, xmmword ptr [rcx + rbx]
004CD487  movsxd   rcx, eax
004CD48A  lea      eax, [r8 + 0x258]
004CD491  shl      eax, 4
004CD494  movaps   xmm5, xmm15
004CD498  movaps   xmmword ptr [rsp + 0x80], xmm9
004CD4A1  subss    xmm5, xmm8
004CD4A6  movaps   xmm10, xmm15
004CD4AA  movups   xmm2, xmmword ptr [rcx + rbx]
004CD4AE  movsxd   rcx, eax
004CD4B1  lea      eax, [r9 + 0x258]
004CD4B8  shl      eax, 4
004CD4BB  movaps   xmm7, xmm2
004CD4BE  shufps   xmm10, xmm15, 0x55
004CD4C3  subss    xmm7, xmm8
004CD4C8  movaps   xmmword ptr [rsp + 0xb0], xmm10
004CD4D1  movups   xmm0, xmmword ptr [rcx + rbx]
004CD4D5  movsxd   rcx, eax
004CD4D8  lea      eax, [r8 + 0x2bc]
004CD4DF  shl      eax, 4
004CD4E2  movups   xmmword ptr [rip + 0x1b977e7], xmm0  ; -> 02064CD0
004CD4E9  movups   xmm0, xmmword ptr [rcx + rbx]
004CD4ED  movsxd   rcx, eax
004CD4F0  lea      eax, [r9 + 0x2bc]
004CD4F7  shl      eax, 4
004CD4FA  movups   xmmword ptr [rip + 0x1b977df], xmm0  ; -> 02064CE0
004CD501  movups   xmm0, xmmword ptr [rcx + rbx]
004CD505  movsxd   rcx, eax
004CD508  movss    dword ptr [rip + 0x1b977c8], xmm1  ; -> 02064CD8
004CD510  movups   xmmword ptr [rip + 0x1b977d9], xmm0  ; -> 02064CF0
004CD517  movups   xmm0, xmmword ptr [rcx + rbx]
004CD51B  movss    dword ptr [rip + 0x1b977c5], xmm1  ; -> 02064CE8
004CD523  movups   xmmword ptr [rip + 0x1b977d6], xmm0  ; -> 02064D00
004CD52A  movaps   xmm0, xmm13
004CD52E  shufps   xmm0, xmm13, 0x55
004CD533  movaps   xmm8, xmm0
004CD537  movaps   xmmword ptr [rsp + 0x40], xmm0
004CD53C  movss    xmm0, dword ptr [rip + 0x4480d8]  ; -> 0091561C [f32 1824]
004CD544  subss    xmm8, xmm0
004CD549  subss    xmm9, xmm0
004CD54E  movups   xmmword ptr [rip + 0x1b9773a], xmm13  ; -> 02064C90
004CD556  movups   xmmword ptr [rip + 0x1b97742], xmm14  ; -> 02064CA0
004CD55E  movups   xmmword ptr [rip + 0x1b9774a], xmm15  ; -> 02064CB0
004CD566  movups   xmmword ptr [rsp + 0xa0], xmm2
004CD56E  movups   xmmword ptr [rip + 0x1b9774b], xmm2  ; -> 02064CC0
004CD575  cmp      word ptr [rip + 0x1b97868], si  ; -> 02064DE4
004CD57C  subss    xmm10, xmm0
004CD581  movaps   xmm11, xmm2
004CD585  movss    dword ptr [rip + 0x1b9776b], xmm1  ; -> 02064CF8
004CD58D  shufps   xmm11, xmm2, 0x55
004CD592  movaps   xmmword ptr [rsp + 0x90], xmm11
004CD59B  subss    xmm11, xmm0
004CD5A0  movss    xmm0, dword ptr [rip + 0x855138]  ; -> 00D226E0 [f32 0.002232142]
004CD5A8  movss    dword ptr [rip + 0x1b97554], xmm0  ; -> 02064B04
004CD5B0  movss    dword ptr [rip + 0x1b97750], xmm1  ; -> 02064D08
004CD5B8  mulss    xmm3, xmm12
004CD5BD  mulss    xmm4, xmm12
004CD5C2  mulss    xmm5, xmm12
004CD5C7  mulss    xmm7, xmm12
004CD5CC  je       0x4cd5da  ; -> 004CD5DA
004CD5CE  movaps   xmm0, xmm12
004CD5D2  movss    dword ptr [rip + 0x1b9752a], xmm0  ; -> 02064B04
004CD5DA  movups   xmm2, xmmword ptr [r11 + rbx]
004CD5DF  movsx    r8d, di
004CD5E3  movups   xmm1, xmmword ptr [rsp + 0xa0]
004CD5EB  mov      edx, r8d
004CD5EE  mulss    xmm8, xmm0
004CD5F3  shl      edx, 4
004CD5F6  mulss    xmm9, xmm0
004CD5FB  mulss    xmm10, xmm0
004CD600  mulss    xmm11, xmm0
004CD605  movaps   xmm0, xmmword ptr [rsp + 0x40]
004CD60A  mulss    xmm0, xmm6
004CD60E  mulss    xmm13, xmm6
004CD613  mulss    xmm14, xmm6
004CD618  cvttss2si eax, xmm13
004CD61D  movups   xmm13, xmmword ptr [rip + 0x1b9756b]  ; -> 02064B90
004CD625  mov      dword ptr [rip + 0x1b97665], eax  ; -> 02064C90
004CD62B  cvttss2si eax, xmm0
004CD62F  movss    xmm0, dword ptr [rip + 0x1b97661]  ; -> 02064C98
004CD637  mov      dword ptr [rip + 0x1b97657], eax  ; -> 02064C94
004CD63D  mulss    xmm0, xmm6
004CD641  mulss    xmm1, xmm6
004CD645  cvttss2si eax, xmm0
004CD649  movaps   xmm0, xmmword ptr [rsp + 0x80]
004CD651  mov      dword ptr [rip + 0x1b97641], eax  ; -> 02064C98
004CD657  lea      eax, [rdx + 0x10]
004CD65A  movsxd   rcx, eax
004CD65D  mulss    xmm0, xmm6
004CD661  cvttss2si eax, xmm14
004CD666  movups   xmmword ptr [rcx + rbx], xmm13
004CD66B  mov      dword ptr [rip + 0x1b9762f], eax  ; -> 02064CA0
004CD671  cvttss2si eax, xmm0
004CD675  movss    xmm0, dword ptr [rip + 0x1b9762b]  ; -> 02064CA8
004CD67D  mov      dword ptr [rip + 0x1b97621], eax  ; -> 02064CA4
004CD683  mulss    xmm0, xmm6
004CD687  movups   xmmword ptr [rip + 0x1b975c2], xmm2  ; -> 02064C50
004CD68E  mulss    xmm2, dword ptr [rip + 0x1b97516]  ; -> 02064BAC
004CD696  cvttss2si eax, xmm0
004CD69A  movaps   xmm0, xmmword ptr [rsp + 0xb0]
004CD6A2  addss    xmm3, xmm2
004CD6A6  mov      dword ptr [rip + 0x1b975fc], eax  ; -> 02064CA8
004CD6AC  addss    xmm4, xmm2
004CD6B0  mulss    xmm0, xmm6
004CD6B4  lea      eax, [r8 + 4]
004CD6B8  shl      eax, 4
004CD6BB  movsxd   rcx, eax
004CD6BE  addss    xmm5, xmm2
004CD6C2  mulss    xmm15, xmm6
004CD6C7  movss    dword ptr [rip + 0x1b97581], xmm2  ; -> 02064C50
004CD6CF  movups   xmmword ptr [rcx + rbx], xmm13
004CD6D4  cvttss2si eax, xmm15
004CD6D9  mov      dword ptr [rip + 0x1b975d1], eax  ; -> 02064CB0
004CD6DF  cvttss2si eax, xmm0
004CD6E3  movss    xmm0, dword ptr [rip + 0x1b975cd]  ; -> 02064CB8
004CD6EB  mov      dword ptr [rip + 0x1b975c3], eax  ; -> 02064CB4
004CD6F1  mulss    xmm0, xmm6
004CD6F5  cvttss2si eax, xmm0
004CD6F9  movaps   xmm0, xmmword ptr [rsp + 0x90]
004CD701  mov      dword ptr [rip + 0x1b975b1], eax  ; -> 02064CB8
004CD707  lea      eax, [r8 + 7]
004CD70B  shl      eax, 4
004CD70E  movsxd   rcx, eax
004CD711  cvttss2si eax, xmm1
004CD715  movss    xmm1, dword ptr [rip + 0x1b97537]  ; -> 02064C54
004CD71D  mulss    xmm1, dword ptr [rip + 0x1b97487]  ; -> 02064BAC
004CD725  mov      dword ptr [rip + 0x1b97595], eax  ; -> 02064CC0
004CD72B  mulss    xmm0, xmm6
004CD72F  movups   xmmword ptr [rcx + rbx], xmm13
004CD734  movss    dword ptr [rip + 0x1b97518], xmm1  ; -> 02064C54
004CD73C  addss    xmm8, xmm1
004CD741  cvttss2si eax, xmm0
004CD745  movss    xmm0, dword ptr [rip + 0x1b9757b]  ; -> 02064CC8
004CD74D  addss    xmm9, xmm1
004CD752  mov      dword ptr [rip + 0x1b9756c], eax  ; -> 02064CC4
004CD758  addss    xmm10, xmm1
004CD75D  mulss    xmm0, xmm6
004CD761  cvttss2si eax, xmm0
004CD765  mov      dword ptr [rip + 0x1b9755d], eax  ; -> 02064CC8
004CD76B  lea      eax, [r8 + 0xa]
004CD76F  shl      eax, 4
004CD772  movsxd   rcx, eax
004CD775  movups   xmmword ptr [rcx + rbx], xmm13
004CD77A  movss    xmm0, dword ptr [rip + 0x1b9759a]  ; -> 02064D1C
004CD782  addss    xmm11, xmm1
004CD787  movss    xmm1, dword ptr [rip + 0x1b97589]  ; -> 02064D18
004CD78F  addss    xmm7, xmm2
004CD793  movss    xmm2, dword ptr [rip + 0x1b97575]  ; -> 02064D10
004CD79B  lea      eax, [r8 + 2]
004CD79F  inc      word ptr [rip + 0x1b97612]  ; -> 02064DB8
004CD7A6  add      di, 0xc
004CD7AA  shl      eax, 4
004CD7AD  movsxd   rcx, eax
004CD7B0  lea      eax, [r8 + 5]
004CD7B4  shl      eax, 4
004CD7B7  mulss    xmm11, xmm0
004CD7BC  mov      word ptr [rip + 0x1b975f1], di  ; -> 02064DB4
004CD7C3  mulss    xmm8, xmm0
004CD7C8  mulss    xmm9, xmm0
004CD7CD  mulss    xmm10, xmm0
004CD7D2  movups   xmm0, xmmword ptr [rip + 0x1b974b7]  ; -> 02064C90
004CD7D9  mulss    xmm3, xmm1
004CD7DD  movups   xmmword ptr [rcx + rbx], xmm0
004CD7E1  movsxd   rcx, eax
004CD7E4  lea      eax, [r8 + 8]
004CD7E8  movups   xmm0, xmmword ptr [rip + 0x1b974b1]  ; -> 02064CA0
004CD7EF  shl      eax, 4
004CD7F2  mulss    xmm4, xmm1
004CD7F6  addss    xmm3, xmm2
004CD7FA  movups   xmmword ptr [rcx + rbx], xmm0
004CD7FE  movsxd   rcx, eax
004CD801  lea      eax, [r8 + 0xb]
004CD805  movups   xmm0, xmmword ptr [rip + 0x1b974a4]  ; -> 02064CB0
004CD80C  shl      eax, 4
004CD80F  mulss    xmm5, xmm1
004CD813  addss    xmm4, xmm2
004CD817  movups   xmmword ptr [rcx + rbx], xmm0
004CD81B  movsxd   rcx, eax
004CD81E  movups   xmm0, xmmword ptr [rip + 0x1b9749b]  ; -> 02064CC0
004CD825  movsxd   rax, edx
004CD828  mov      rdx, r14
004CD82B  mulss    xmm7, xmm1
004CD82F  addss    xmm5, xmm2
004CD833  movss    xmm1, dword ptr [rip + 0x1b974d9]  ; -> 02064D14
004CD83B  movups   xmmword ptr [rcx + rbx], xmm0
004CD83F  addss    xmm8, xmm1
004CD844  movss    dword ptr [rip + 0x1b97484], xmm3  ; -> 02064CD0
004CD84C  addss    xmm9, xmm1
004CD851  movss    dword ptr [rip + 0x1b97487], xmm4  ; -> 02064CE0
004CD859  addss    xmm10, xmm1
004CD85E  movss    dword ptr [rip + 0x1b9748a], xmm5  ; -> 02064CF0
004CD866  addss    xmm7, xmm2
004CD86A  addss    xmm11, xmm1
004CD86F  movss    dword ptr [rip + 0x1b9745c], xmm8  ; -> 02064CD4
004CD878  movups   xmm0, xmmword ptr [rip + 0x1b97451]  ; -> 02064CD0
004CD87F  movss    dword ptr [rip + 0x1b9745c], xmm9  ; -> 02064CE4
004CD888  movups   xmmword ptr [rax + rbx], xmm0
004CD88C  lea      eax, [r8 + 3]
004CD890  movups   xmm0, xmmword ptr [rip + 0x1b97449]  ; -> 02064CE0
004CD897  shl      eax, 4
004CD89A  movsxd   rcx, eax
004CD89D  lea      eax, [r8 + 6]
004CD8A1  shl      eax, 4
004CD8A4  movss    dword ptr [rip + 0x1b97447], xmm10  ; -> 02064CF4
004CD8AD  movss    dword ptr [rip + 0x1b9744b], xmm7  ; -> 02064D00
004CD8B5  movups   xmmword ptr [rcx + rbx], xmm0
004CD8B9  movsxd   rcx, eax
004CD8BC  lea      eax, [r8 + 9]
004CD8C0  movups   xmm0, xmmword ptr [rip + 0x1b97429]  ; -> 02064CF0
004CD8C7  shl      eax, 4
004CD8CA  movss    dword ptr [rip + 0x1b97431], xmm11  ; -> 02064D04
004CD8D3  movups   xmmword ptr [rcx + rbx], xmm0
004CD8D7  movsxd   rcx, eax
004CD8DA  movups   xmm0, xmmword ptr [rip + 0x1b9741f]  ; -> 02064D00
004CD8E1  movups   xmmword ptr [rcx + rbx], xmm0
004CD8E5  mov      rcx, rbp
004CD8E8  call     0x4c7f00  ; -> 004C7F00 fn
004CD8ED  movzx    ecx, word ptr [rip + 0x1b974e4]  ; -> 02064DD8
004CD8F4  movzx    eax, word ptr [rip + 0x1b974d9]  ; -> 02064DD4
004CD8FB  inc      cx
004CD8FE  movzx    esi, word ptr [rip + 0x1b97207]  ; -> 02064B0C
004CD905  mov      word ptr [rip + 0x1b974cc], cx  ; -> 02064DD8
004CD90C  test     ax, ax
004CD90F  jle      0x4cc0f5  ; -> 004CC0F5
004CD915  movzx    edi, word ptr [rip + 0x1b97498]  ; -> 02064DB4
004CD91C  movss    xmm8, dword ptr [rip + 0x447cf3]  ; -> 00915618 [f32 1792]
004CD925  jmp      0x4cd3d0  ; -> 004CD3D0
004CD92A  movss    xmm4, dword ptr [rip + 0x1934efe]  ; -> 01E02830 [u32 0x00000000]
004CD932  lea      rdx, [rip + 0x1b97257]  ; -> 02064B90
004CD939  movss    xmm5, dword ptr [rip + 0x1b9728b]  ; -> 02064BCC
004CD941  lea      rcx, [rip + 0x1b97248]  ; -> 02064B90
004CD948  movss    xmm8, dword ptr [rip + 0x1b9726f]  ; -> 02064BC0
004CD951  movaps   xmm0, xmm5
004CD954  movss    xmm7, dword ptr [rip + 0x1b97268]  ; -> 02064BC4
004CD95C  movaps   xmm3, xmm8
004CD960  movss    xmm6, dword ptr [rip + 0x1b97260]  ; -> 02064BC8
004CD968  movaps   xmm2, xmm7
004CD96B  mulss    xmm3, dword ptr [rip + 0x1b9729d]  ; -> 02064C10
004CD973  movaps   xmm1, xmm6
004CD976  mov      dword ptr [rip + 0x1b97184], 0x437f0000  ; -> 02064B04
004CD980  mulss    xmm2, dword ptr [rip + 0x1b9728c]  ; -> 02064C14
004CD988  mulss    xmm1, dword ptr [rip + 0x1b97288]  ; -> 02064C18
004CD990  maxss    xmm3, xmm4
004CD994  mulss    xmm0, dword ptr [rip + 0x1b97280]  ; -> 02064C1C
004CD99C  maxss    xmm2, xmm4
004CD9A0  mulss    xmm8, dword ptr [rip + 0x1b97257]  ; -> 02064C00
004CD9A9  maxss    xmm1, xmm4
004CD9AD  mulss    xmm7, dword ptr [rip + 0x1b9724f]  ; -> 02064C04
004CD9B5  maxss    xmm0, xmm4
004CD9B9  mulss    xmm6, dword ptr [rip + 0x1b97247]  ; -> 02064C08
004CD9C1  maxss    xmm8, xmm4
004CD9C6  mulss    xmm5, dword ptr [rip + 0x1b9723e]  ; -> 02064C0C
004CD9CE  maxss    xmm7, xmm4
004CD9D2  movss    dword ptr [rip + 0x1b971b6], xmm3  ; -> 02064B90
004CD9DA  maxss    xmm6, xmm4
004CD9DE  movss    xmm3, dword ptr [rip + 0x3f815a]  ; -> 008C5B40 [f32 255]
004CD9E6  movss    dword ptr [rip + 0x1b971a6], xmm2  ; -> 02064B94
004CD9EE  maxss    xmm5, xmm4
004CD9F2  movaps   xmm2, xmm3
004CD9F5  movss    dword ptr [rip + 0x1b9719b], xmm1  ; -> 02064B98
004CD9FD  movss    dword ptr [rip + 0x1b97197], xmm0  ; -> 02064B9C
004CDA05  movss    dword ptr [rip + 0x1b971b2], xmm8  ; -> 02064BC0
004CDA0E  movss    dword ptr [rip + 0x1b971ae], xmm7  ; -> 02064BC4
004CDA16  movss    dword ptr [rip + 0x1b971aa], xmm6  ; -> 02064BC8
004CDA1E  movss    dword ptr [rip + 0x1b971a6], xmm5  ; -> 02064BCC
004CDA26  call     0x4cf230  ; -> 004CF230 fn
004CDA2B  lea      rdx, [rip + 0x1b9718e]  ; -> 02064BC0
004CDA32  lea      rcx, [rip + 0x1b97187]  ; -> 02064BC0
004CDA39  call     0x4cf230  ; -> 004CF230 fn
004CDA3E  movups   xmm0, xmmword ptr [rip + 0x1b9714b]  ; -> 02064B90
004CDA45  movzx    eax, word ptr [rip + 0x1b97390]  ; -> 02064DDC
004CDA4C  movss    xmm7, dword ptr [rip + 0x181e230]  ; -> 01CEBC84 [f32 16]
004CDA54  movss    xmm14, dword ptr [rip + 0x181e113]  ; -> 01CEBB70 [f32 0.5]
004CDA5D  movss    xmm6, dword ptr [rip + 0x4328a7]  ; -> 0090030C [f32 -0.5]
004CDA65  cvttps2dq xmm15, xmm0
004CDA6A  movups   xmm0, xmmword ptr [rip + 0x1b9714f]  ; -> 02064BC0
004CDA71  movups   xmmword ptr [rip + 0x1b97117], xmm15  ; -> 02064B90
004CDA79  cvttps2dq xmm12, xmm0
004CDA7E  movups   xmmword ptr [rip + 0x1b9713a], xmm12  ; -> 02064BC0
004CDA86  cmp      ax, si
004CDA89  je       0x4cdee7  ; -> 004CDEE7
004CDA8F  movsx    r15d, ax
004CDA93  movzx    eax, si
004CDA96  mov      word ptr [rip + 0x1b9733b], ax  ; -> 02064DD8
004CDA9D  add      r15w, si
004CDAA1  mov      word ptr [rip + 0x1b97327], r8w  ; -> 02064DD0
004CDAA9  nop      dword ptr [rax]
004CDAB0  movsx    r11d, ax
004CDAB4  dec      r15w
004CDAB8  mov      dword ptr [rip + 0x1b97042], 0xbf000000  ; -> 02064B04
004CDAC2  mov      word ptr [rip + 0x1b9730a], r15w  ; -> 02064DD4
004CDACA  lea      eax, [r11 + 0xc8]
004CDAD1  shl      eax, 4
004CDAD4  movsxd   rcx, eax
004CDAD7  movsx    eax, word ptr [rcx + rbx]
004CDADB  movsx    edx, word ptr [rcx + rbx + 4]
004CDAE0  mov      r9d, eax
004CDAE3  movsx    r8d, word ptr [rcx + rbx + 8]
004CDAE9  mov      word ptr [rip + 0x1b972cc], ax  ; -> 02064DBC
004CDAF0  add      eax, 0x1c2
004CDAF5  shl      eax, 4
004CDAF8  movsxd   rcx, eax
004CDAFB  lea      eax, [rdx + 0x1c2]
004CDB01  shl      eax, 4
004CDB04  mov      word ptr [rip + 0x1b972b5], dx  ; -> 02064DC0
004CDB0B  mov      word ptr [rip + 0x1b972b1], r8w  ; -> 02064DC4
004CDB13  movups   xmm9, xmmword ptr [rcx + rbx]
004CDB18  movsxd   rcx, eax
004CDB1B  lea      eax, [r8 + 0x1c2]
004CDB22  shl      eax, 4
004CDB25  movups   xmmword ptr [rip + 0x1b971a3], xmm9  ; -> 02064CD0
004CDB2D  movups   xmm10, xmmword ptr [rcx + rbx]
004CDB32  movsxd   rcx, eax
004CDB35  lea      eax, [r9 + 0x190]
004CDB3C  movss    xmm4, dword ptr [rip + 0x1b97190]  ; -> 02064CD4
004CDB44  shl      eax, 4
004CDB47  movups   xmmword ptr [rip + 0x1b97191], xmm10  ; -> 02064CE0
004CDB4F  movups   xmm11, xmmword ptr [rcx + rbx]
004CDB54  movsxd   rcx, eax
004CDB57  lea      eax, [rdx + 0x190]
004CDB5D  movss    xmm5, dword ptr [rip + 0x1b9717f]  ; -> 02064CE4
004CDB65  shl      eax, 4
004CDB68  movups   xmmword ptr [rip + 0x1b97180], xmm11  ; -> 02064CF0
004CDB70  movups   xmm0, xmmword ptr [rcx + rbx]
004CDB74  movsxd   rcx, eax
004CDB77  lea      eax, [r8 + 0x190]
004CDB7E  movss    xmm8, dword ptr [rip + 0x1b9716d]  ; -> 02064CF4
004CDB87  shl      eax, 4
004CDB8A  movups   xmmword ptr [rip + 0x1b9710f], xmm0  ; -> 02064CA0
004CDB91  movups   xmm0, xmmword ptr [rcx + rbx]
004CDB95  movsxd   rcx, eax
004CDB98  lea      eax, [r11 + 0xfa]
004CDB9F  shl      eax, 4
004CDBA2  cmp      word ptr [rip + 0x1b9723b], si  ; -> 02064DE4
004CDBA9  movups   xmmword ptr [rip + 0x1b97100], xmm0  ; -> 02064CB0
004CDBB0  movups   xmm0, xmmword ptr [rcx + rbx]
004CDBB4  movsxd   rcx, eax
004CDBB7  mulss    xmm9, xmm14
004CDBBC  mulss    xmm10, xmm14
004CDBC1  mulss    xmm11, xmm14
004CDBC6  addss    xmm9, xmm6
004CDBCB  movups   xmmword ptr [rip + 0x1b970ee], xmm0  ; -> 02064CC0
004CDBD2  movups   xmm0, xmmword ptr [rcx + rbx]
004CDBD6  mulss    xmm4, xmm6
004CDBDA  addss    xmm10, xmm6
004CDBDF  mulss    xmm5, xmm6
004CDBE3  addss    xmm11, xmm6
004CDBE8  mulss    xmm8, xmm6
004CDBED  addss    xmm4, xmm6
004CDBF1  movups   xmmword ptr [rip + 0x1b97068], xmm0  ; -> 02064C60
004CDBF8  addss    xmm5, xmm6
004CDBFC  addss    xmm8, xmm6
004CDC01  je       0x4cdc18  ; -> 004CDC18
004CDC03  movss    xmm0, dword ptr [rip + 0x1b96fa9]  ; -> 02064BB4
004CDC0B  mulss    xmm4, xmm0
004CDC0F  mulss    xmm5, xmm0
004CDC13  mulss    xmm8, xmm0
004CDC18  movss    xmm0, dword ptr [rip + 0x1b97080]  ; -> 02064CA0
004CDC20  movss    xmm1, dword ptr [rip + 0x1b9707c]  ; -> 02064CA4
004CDC28  movss    xmm2, dword ptr [rip + 0x1b97034]  ; -> 02064C64
004CDC30  mulss    xmm2, dword ptr [rip + 0x1b96f74]  ; -> 02064BAC
004CDC38  movsx    r8d, di
004CDC3C  movss    xmm3, dword ptr [rip + 0x1b9701c]  ; -> 02064C60
004CDC44  mov      edx, r8d
004CDC47  mulss    xmm3, dword ptr [rip + 0x1b96f5d]  ; -> 02064BAC
004CDC4F  shl      edx, 4
004CDC52  mulss    xmm1, xmm7
004CDC56  addss    xmm4, xmm2
004CDC5A  mulss    xmm0, xmm7
004CDC5E  addss    xmm5, xmm2
004CDC62  addss    xmm9, xmm3
004CDC67  movss    dword ptr [rip + 0x1b96ff5], xmm2  ; -> 02064C64
004CDC6F  addss    xmm8, xmm2
004CDC74  movss    dword ptr [rip + 0x1b96fe4], xmm3  ; -> 02064C60
004CDC7C  movss    xmm2, dword ptr [rip + 0x1b9708c]  ; -> 02064D10
004CDC84  addss    xmm10, xmm3
004CDC89  cvttss2si eax, xmm0
004CDC8D  movss    xmm0, dword ptr [rip + 0x1b97013]  ; -> 02064CA8
004CDC95  addss    xmm11, xmm3
004CDC9A  mov      dword ptr [rip + 0x1b97000], eax  ; -> 02064CA0
004CDCA0  cvttss2si eax, xmm1
004CDCA4  movss    xmm1, dword ptr [rip + 0x1b97004]  ; -> 02064CB0
004CDCAC  mov      dword ptr [rip + 0x1b96ff2], eax  ; -> 02064CA4
004CDCB2  mulss    xmm1, xmm7
004CDCB6  mulss    xmm0, xmm7
004CDCBA  cvttss2si eax, xmm0
004CDCBE  movss    xmm0, dword ptr [rip + 0x1b96fee]  ; -> 02064CB4
004CDCC6  mov      dword ptr [rip + 0x1b96fdc], eax  ; -> 02064CA8
004CDCCC  lea      eax, [rdx + 0x10]
004CDCCF  movsxd   rcx, eax
004CDCD2  cvttss2si eax, xmm1
004CDCD6  movss    xmm1, dword ptr [rip + 0x1b96fda]  ; -> 02064CB8
004CDCDE  mov      dword ptr [rip + 0x1b96fcc], eax  ; -> 02064CB0
004CDCE4  mulss    xmm1, xmm7
004CDCE8  mulss    xmm0, xmm7
004CDCEC  movups   xmmword ptr [rcx + rbx], xmm12
004CDCF1  cvttss2si eax, xmm0
004CDCF5  movss    xmm0, dword ptr [rip + 0x1b96fc7]  ; -> 02064CC4
004CDCFD  mov      dword ptr [rip + 0x1b96fb1], eax  ; -> 02064CB4
004CDD03  cvttss2si eax, xmm1
004CDD07  movss    xmm1, dword ptr [rip + 0x1b96fb1]  ; -> 02064CC0
004CDD0F  mov      dword ptr [rip + 0x1b96fa3], eax  ; -> 02064CB8
004CDD15  lea      eax, [r8 + 4]
004CDD19  shl      eax, 4
004CDD1C  movsxd   rcx, eax
004CDD1F  mulss    xmm1, xmm7
004CDD23  mulss    xmm0, xmm7
004CDD27  cvttss2si eax, xmm1
004CDD2B  movss    xmm1, dword ptr [rip + 0x1b96f95]  ; -> 02064CC8
004CDD33  mov      dword ptr [rip + 0x1b96f87], eax  ; -> 02064CC0
004CDD39  cvttss2si eax, xmm0
004CDD3D  movss    xmm0, dword ptr [rip + 0x1934af3]  ; -> 01E02838 [u32 0x00000000]
004CDD45  addss    xmm0, dword ptr [rip + 0x1934aef]  ; -> 01E0283C [f32 1]
004CDD4D  mulss    xmm1, xmm7
004CDD51  mov      dword ptr [rip + 0x1b96f6d], eax  ; -> 02064CC4
004CDD57  movups   xmmword ptr [rcx + rbx], xmm12
004CDD5C  cvttss2si eax, xmm1
004CDD60  movss    xmm1, dword ptr [rip + 0x1b96fb0]  ; -> 02064D18
004CDD68  mulss    xmm9, xmm1
004CDD6D  mov      dword ptr [rip + 0x1b96f55], eax  ; -> 02064CC8
004CDD73  lea      eax, [r8 + 7]
004CDD77  movss    dword ptr [rip + 0x1b96f59], xmm0  ; -> 02064CD8
004CDD7F  movss    dword ptr [rip + 0x1b96f61], xmm0  ; -> 02064CE8
004CDD87  movss    dword ptr [rip + 0x1b96f69], xmm0  ; -> 02064CF8
004CDD8F  addss    xmm9, xmm2
004CDD94  movss    xmm0, dword ptr [rip + 0x1b96f80]  ; -> 02064D1C
004CDD9C  mulss    xmm4, xmm0
004CDDA0  shl      eax, 4
004CDDA3  mulss    xmm10, xmm1
004CDDA8  movsxd   rcx, eax
004CDDAB  mulss    xmm11, xmm1
004CDDB0  movss    xmm1, dword ptr [rip + 0x1b96f5c]  ; -> 02064D14
004CDDB8  addss    xmm4, xmm1
004CDDBC  movss    dword ptr [rip + 0x1b96f0b], xmm9  ; -> 02064CD0
004CDDC5  movups   xmmword ptr [rcx + rbx], xmm12
004CDDCA  mulss    xmm5, xmm0
004CDDCE  movss    dword ptr [rip + 0x1b96efe], xmm4  ; -> 02064CD4
004CDDD6  mulss    xmm8, xmm0
004CDDDB  movups   xmm0, xmmword ptr [rip + 0x1b96ebe]  ; -> 02064CA0
004CDDE2  inc      word ptr [rip + 0x1b96fcf]  ; -> 02064DB8
004CDDE9  lea      eax, [r8 + 2]
004CDDED  shl      eax, 4
004CDDF0  addss    xmm10, xmm2
004CDDF5  movsxd   rcx, eax
004CDDF8  addss    xmm5, xmm1
004CDDFC  lea      eax, [r8 + 5]
004CDE00  add      di, 9
004CDE04  shl      eax, 4
004CDE07  addss    xmm11, xmm2
004CDE0C  addss    xmm8, xmm1
004CDE11  mov      word ptr [rip + 0x1b96f9c], di  ; -> 02064DB4
004CDE18  movups   xmmword ptr [rcx + rbx], xmm0
004CDE1C  movsxd   rcx, eax
004CDE1F  lea      eax, [r8 + 8]
004CDE23  movups   xmm0, xmmword ptr [rip + 0x1b96e86]  ; -> 02064CB0
004CDE2A  shl      eax, 4
004CDE2D  movss    dword ptr [rip + 0x1b96eaa], xmm10  ; -> 02064CE0
004CDE36  movups   xmmword ptr [rcx + rbx], xmm0
004CDE3A  movsxd   rcx, eax
004CDE3D  movups   xmm0, xmmword ptr [rip + 0x1b96e7c]  ; -> 02064CC0
004CDE44  movsxd   rax, edx
004CDE47  mov      rdx, r14
004CDE4A  movss    dword ptr [rip + 0x1b96e92], xmm5  ; -> 02064CE4
004CDE52  movups   xmmword ptr [rcx + rbx], xmm0
004CDE56  movups   xmm0, xmmword ptr [rip + 0x1b96e73]  ; -> 02064CD0
004CDE5D  movss    dword ptr [rip + 0x1b96e8a], xmm11  ; -> 02064CF0
004CDE66  movups   xmmword ptr [rax + rbx], xmm0
004CDE6A  lea      eax, [r8 + 3]
004CDE6E  movups   xmm0, xmmword ptr [rip + 0x1b96e6b]  ; -> 02064CE0
004CDE75  shl      eax, 4
004CDE78  movsxd   rcx, eax
004CDE7B  lea      eax, [r8 + 6]
004CDE7F  shl      eax, 4
004CDE82  movss    dword ptr [rip + 0x1b96e69], xmm8  ; -> 02064CF4
004CDE8B  movups   xmmword ptr [rcx + rbx], xmm0
004CDE8F  movsxd   rcx, eax
004CDE92  movups   xmm0, xmmword ptr [rip + 0x1b96e57]  ; -> 02064CF0
004CDE99  movups   xmmword ptr [rcx + rbx], xmm0
004CDE9D  mov      rcx, rbp
004CDEA0  call     0x4c7f00  ; -> 004C7F00 fn
004CDEA5  movzx    eax, word ptr [rip + 0x1b96f2c]  ; -> 02064DD8
004CDEAC  movzx    r15d, word ptr [rip + 0x1b96f20]  ; -> 02064DD4
004CDEB4  inc      ax
004CDEB7  movzx    esi, word ptr [rip + 0x1b96c4e]  ; -> 02064B0C
004CDEBE  movzx    edi, word ptr [rip + 0x1b96eef]  ; -> 02064DB4
004CDEC5  mov      word ptr [rip + 0x1b96f0c], ax  ; -> 02064DD8
004CDECC  test     r15w, r15w
004CDED0  jle      0x4cdedf  ; -> 004CDEDF
004CDED2  movups   xmm12, xmmword ptr [rip + 0x1b96ce6]  ; -> 02064BC0
004CDEDA  jmp      0x4cdab0  ; -> 004CDAB0
004CDEDF  movups   xmm15, xmmword ptr [rip + 0x1b96ca9]  ; -> 02064B90
004CDEE7  movzx    ecx, word ptr [rip + 0x1b96ef2]  ; -> 02064DE0
004CDEEE  cmp      cx, si
004CDEF1  je       0x4cc0f5  ; -> 004CC0F5
004CDEF7  lea      eax, [rsi + 3]
004CDEFA  movsx    r11d, cx
004CDEFE  mov      word ptr [rip + 0x1b96ecb], ax  ; -> 02064DD0
004CDF05  add      r11w, si
004CDF09  movzx    eax, si
004CDF0C  mov      word ptr [rip + 0x1b96ec5], ax  ; -> 02064DD8
004CDF13  movsx    r10d, ax
004CDF17  dec      r11w
004CDF1B  mov      dword ptr [rip + 0x1b96bdf], 0xbf000000  ; -> 02064B04
004CDF25  mov      word ptr [rip + 0x1b96ea7], r11w  ; -> 02064DD4
004CDF2D  lea      eax, [r10 + 0x12c]
004CDF34  shl      eax, 4
004CDF37  movsxd   rcx, eax
004CDF3A  movsx    edx, word ptr [rcx + rbx + 4]
004CDF3F  movsx    eax, word ptr [rcx + rbx]
004CDF43  mov      word ptr [rip + 0x1b96e72], ax  ; -> 02064DBC
004CDF4A  mov      r8d, eax
004CDF4D  add      eax, 0x1c2
004CDF52  mov      word ptr [rip + 0x1b96e67], dx  ; -> 02064DC0
004CDF59  shl      eax, 4
004CDF5C  movsxd   rcx, eax
004CDF5F  lea      eax, [rdx + 0x1c2]
004CDF65  shl      eax, 4
004CDF68  movups   xmm10, xmmword ptr [rcx + rbx]
004CDF6D  movsxd   rcx, eax
004CDF70  lea      eax, [r8 + 0x226]
004CDF77  shl      eax, 4
004CDF7A  movups   xmmword ptr [rip + 0x1b96d4e], xmm10  ; -> 02064CD0
004CDF82  movups   xmm11, xmmword ptr [rcx + rbx]
004CDF87  movsxd   rcx, eax
004CDF8A  lea      eax, [rdx + 0x226]
004CDF90  movss    xmm4, dword ptr [rip + 0x1b96d3c]  ; -> 02064CD4
004CDF98  shl      eax, 4
004CDF9B  movups   xmmword ptr [rip + 0x1b96d3d], xmm11  ; -> 02064CE0
004CDFA3  movups   xmm12, xmmword ptr [rcx + rbx]
004CDFA8  movsxd   rcx, eax
004CDFAB  lea      eax, [r8 + 0x190]
004CDFB2  movss    xmm5, dword ptr [rip + 0x1b96d2a]  ; -> 02064CE4
004CDFBA  shl      eax, 4
004CDFBD  movups   xmmword ptr [rip + 0x1b96d2b], xmm12  ; -> 02064CF0
004CDFC5  movups   xmm13, xmmword ptr [rcx + rbx]
004CDFCA  movsxd   rcx, eax
004CDFCD  lea      eax, [rdx + 0x190]
004CDFD3  movss    xmm8, dword ptr [rip + 0x1b96d18]  ; -> 02064CF4
004CDFDC  shl      eax, 4
004CDFDF  movups   xmmword ptr [rip + 0x1b96d19], xmm13  ; -> 02064D00
004CDFE7  movups   xmm0, xmmword ptr [rcx + rbx]
004CDFEB  movsxd   rcx, eax
004CDFEE  lea      eax, [r8 + 0x1f4]
004CDFF5  movss    xmm9, dword ptr [rip + 0x1b96d06]  ; -> 02064D04
004CDFFE  shl      eax, 4
004CE001  movups   xmmword ptr [rip + 0x1b96c88], xmm0  ; -> 02064C90
004CE008  movups   xmm0, xmmword ptr [rcx + rbx]
004CE00C  movsxd   rcx, eax
004CE00F  lea      eax, [rdx + 0x1f4]
004CE015  shl      eax, 4
004CE018  movups   xmmword ptr [rip + 0x1b96c81], xmm0  ; -> 02064CA0
004CE01F  movups   xmm0, xmmword ptr [rcx + rbx]
004CE023  movsxd   rcx, eax
004CE026  lea      eax, [r10 + 0x15e]
004CE02D  shl      eax, 4
004CE030  cmp      word ptr [rip + 0x1b96dad], si  ; -> 02064DE4
004CE037  movups   xmmword ptr [rip + 0x1b96c72], xmm0  ; -> 02064CB0
004CE03E  movups   xmm0, xmmword ptr [rcx + rbx]
004CE042  movsxd   rcx, eax
004CE045  mulss    xmm10, xmm14
004CE04A  mulss    xmm11, xmm14
004CE04F  mulss    xmm12, xmm14
004CE054  addss    xmm10, xmm6
004CE059  mulss    xmm13, xmm14
004CE05E  addss    xmm11, xmm6
004CE063  movups   xmmword ptr [rip + 0x1b96c56], xmm0  ; -> 02064CC0
004CE06A  movups   xmm0, xmmword ptr [rcx + rbx]
004CE06E  mulss    xmm4, xmm6
004CE072  addss    xmm12, xmm6
004CE077  mulss    xmm5, xmm6
004CE07B  addss    xmm13, xmm6
004CE080  mulss    xmm8, xmm6
004CE085  addss    xmm4, xmm6
004CE089  mulss    xmm9, xmm6
004CE08E  addss    xmm5, xmm6
004CE092  movups   xmmword ptr [rip + 0x1b96aa7], xmm0  ; -> 02064B40
004CE099  movups   xmmword ptr [rip + 0x1b96bb0], xmm0  ; -> 02064C50
004CE0A0  addss    xmm8, xmm6
004CE0A5  addss    xmm9, xmm6
004CE0AA  je       0x4ce0c6  ; -> 004CE0C6
004CE0AC  movss    xmm0, dword ptr [rip + 0x1b96b00]  ; -> 02064BB4
004CE0B4  mulss    xmm4, xmm0
004CE0B8  mulss    xmm5, xmm0
004CE0BC  mulss    xmm8, xmm0
004CE0C1  mulss    xmm9, xmm0
004CE0C6  movss    xmm0, dword ptr [rip + 0x1b96bc2]  ; -> 02064C90
004CE0CE  movss    xmm1, dword ptr [rip + 0x1b96bbe]  ; -> 02064C94
004CE0D6  movss    xmm3, dword ptr [rip + 0x1b96b72]  ; -> 02064C50
004CE0DE  mulss    xmm3, dword ptr [rip + 0x1b96ac6]  ; -> 02064BAC
004CE0E6  movsx    r8d, di
004CE0EA  movss    xmm2, dword ptr [rip + 0x1b96b62]  ; -> 02064C54
004CE0F2  mov      edx, r8d
004CE0F5  mulss    xmm2, dword ptr [rip + 0x1b96aaf]  ; -> 02064BAC
004CE0FD  shl      edx, 4
004CE100  mulss    xmm1, xmm7
004CE104  addss    xmm10, xmm3
004CE109  mulss    xmm0, xmm7
004CE10D  addss    xmm11, xmm3
004CE112  movss    dword ptr [rip + 0x1b96b36], xmm3  ; -> 02064C50
004CE11A  addss    xmm4, xmm2
004CE11E  movss    dword ptr [rip + 0x1b96b2e], xmm2  ; -> 02064C54
004CE126  addss    xmm5, xmm2
004CE12A  cvttss2si eax, xmm0
004CE12E  movss    xmm0, dword ptr [rip + 0x1b96b62]  ; -> 02064C98
004CE136  addss    xmm12, xmm3
004CE13B  mov      dword ptr [rip + 0x1b96b4f], eax  ; -> 02064C90
004CE141  addss    xmm8, xmm2
004CE146  cvttss2si eax, xmm1
004CE14A  movss    xmm1, dword ptr [rip + 0x1b96b4e]  ; -> 02064CA0
004CE152  addss    xmm13, xmm3
004CE157  mov      dword ptr [rip + 0x1b96b37], eax  ; -> 02064C94
004CE15D  addss    xmm9, xmm2
004CE162  mulss    xmm1, xmm7
004CE166  mulss    xmm0, xmm7
004CE16A  cvttss2si eax, xmm0
004CE16E  movss    xmm0, dword ptr [rip + 0x1b96b2e]  ; -> 02064CA4
004CE176  mov      dword ptr [rip + 0x1b96b1c], eax  ; -> 02064C98
004CE17C  lea      eax, [rdx + 0x10]
004CE17F  movsxd   rcx, eax
004CE182  cvttss2si eax, xmm1
004CE186  movss    xmm1, dword ptr [rip + 0x1b96b1a]  ; -> 02064CA8
004CE18E  mov      dword ptr [rip + 0x1b96b0c], eax  ; -> 02064CA0
004CE194  mulss    xmm1, xmm7
004CE198  mulss    xmm0, xmm7
004CE19C  movups   xmmword ptr [rcx + rbx], xmm15
004CE1A1  cvttss2si eax, xmm0
004CE1A5  movss    xmm0, dword ptr [rip + 0x1b96b07]  ; -> 02064CB4
004CE1AD  mov      dword ptr [rip + 0x1b96af1], eax  ; -> 02064CA4
004CE1B3  cvttss2si eax, xmm1
004CE1B7  movss    xmm1, dword ptr [rip + 0x1b96af1]  ; -> 02064CB0
004CE1BF  mov      dword ptr [rip + 0x1b96ae3], eax  ; -> 02064CA8
004CE1C5  lea      eax, [r8 + 4]
004CE1C9  shl      eax, 4
004CE1CC  movsxd   rcx, eax
004CE1CF  mulss    xmm1, xmm7
004CE1D3  mulss    xmm0, xmm7
004CE1D7  cvttss2si eax, xmm1
004CE1DB  movss    xmm1, dword ptr [rip + 0x1b96ad5]  ; -> 02064CB8
004CE1E3  mov      dword ptr [rip + 0x1b96ac7], eax  ; -> 02064CB0
004CE1E9  cvttss2si eax, xmm0
004CE1ED  movss    xmm0, dword ptr [rip + 0x1b96acf]  ; -> 02064CC4
004CE1F5  mov      dword ptr [rip + 0x1b96ab9], eax  ; -> 02064CB4
004CE1FB  mulss    xmm1, xmm7
004CE1FF  movups   xmmword ptr [rcx + rbx], xmm15
004CE204  cvttss2si eax, xmm1
004CE208  movss    xmm1, dword ptr [rip + 0x1b96ab0]  ; -> 02064CC0
004CE210  mov      dword ptr [rip + 0x1b96aa2], eax  ; -> 02064CB8
004CE216  lea      eax, [r8 + 7]
004CE21A  shl      eax, 4
004CE21D  movsxd   rcx, eax
004CE220  mulss    xmm1, xmm7
004CE224  mulss    xmm0, xmm7
004CE228  cvttss2si eax, xmm1
004CE22C  movss    xmm1, dword ptr [rip + 0x1b96a94]  ; -> 02064CC8
004CE234  mov      dword ptr [rip + 0x1b96a86], eax  ; -> 02064CC0
004CE23A  cvttss2si eax, xmm0
004CE23E  movss    xmm0, dword ptr [rip + 0x19345f2]  ; -> 01E02838 [u32 0x00000000]
004CE246  mov      dword ptr [rip + 0x1b96a78], eax  ; -> 02064CC4
004CE24C  movups   xmmword ptr [rcx + rbx], xmm15
004CE251  mulss    xmm1, xmm7
004CE255  cvttss2si eax, xmm1
004CE259  mov      dword ptr [rip + 0x1b96a69], eax  ; -> 02064CC8
004CE25F  lea      eax, [r8 + 0xa]
004CE263  shl      eax, 4
004CE266  movsxd   rcx, eax
004CE269  movups   xmmword ptr [rcx + rbx], xmm15
004CE26E  addss    xmm0, dword ptr [rip + 0x19345c6]  ; -> 01E0283C [f32 1]
004CE276  movss    xmm1, dword ptr [rip + 0x1b96a9a]  ; -> 02064D18
004CE27E  lea      eax, [r8 + 2]
004CE282  movss    xmm2, dword ptr [rip + 0x1b96a86]  ; -> 02064D10
004CE28A  add      di, 0xc
004CE28E  inc      word ptr [rip + 0x1b96b23]  ; -> 02064DB8
004CE295  shl      eax, 4
004CE298  movsxd   rcx, eax
004CE29B  lea      eax, [r8 + 5]
004CE29F  shl      eax, 4
004CE2A2  movss    dword ptr [rip + 0x1b96a2e], xmm0  ; -> 02064CD8
004CE2AA  movss    dword ptr [rip + 0x1b96a36], xmm0  ; -> 02064CE8
004CE2B2  movss    dword ptr [rip + 0x1b96a3e], xmm0  ; -> 02064CF8
004CE2BA  movss    dword ptr [rip + 0x1b96a46], xmm0  ; -> 02064D08
004CE2C2  movss    xmm0, dword ptr [rip + 0x1b96a52]  ; -> 02064D1C
004CE2CA  mulss    xmm4, xmm0
004CE2CE  mov      word ptr [rip + 0x1b96adf], di  ; -> 02064DB4
004CE2D5  mulss    xmm5, xmm0
004CE2D9  mulss    xmm8, xmm0
004CE2DE  mulss    xmm9, xmm0
004CE2E3  movups   xmm0, xmmword ptr [rip + 0x1b969a6]  ; -> 02064C90
004CE2EA  mulss    xmm10, xmm1
004CE2EF  movups   xmmword ptr [rcx + rbx], xmm0
004CE2F3  movsxd   rcx, eax
004CE2F6  lea      eax, [r8 + 8]
004CE2FA  movups   xmm0, xmmword ptr [rip + 0x1b9699f]  ; -> 02064CA0
004CE301  shl      eax, 4
004CE304  mulss    xmm11, xmm1
004CE309  addss    xmm10, xmm2
004CE30E  movups   xmmword ptr [rcx + rbx], xmm0
004CE312  movsxd   rcx, eax
004CE315  lea      eax, [r8 + 0xb]
004CE319  movups   xmm0, xmmword ptr [rip + 0x1b96990]  ; -> 02064CB0
004CE320  shl      eax, 4
004CE323  mulss    xmm12, xmm1
004CE328  addss    xmm11, xmm2
004CE32D  movups   xmmword ptr [rcx + rbx], xmm0
004CE331  movsxd   rcx, eax
004CE334  movups   xmm0, xmmword ptr [rip + 0x1b96985]  ; -> 02064CC0
004CE33B  movsxd   rax, edx
004CE33E  mov      rdx, r14
004CE341  mulss    xmm13, xmm1
004CE346  addss    xmm12, xmm2
004CE34B  movss    xmm1, dword ptr [rip + 0x1b969c1]  ; -> 02064D14
004CE353  movups   xmmword ptr [rcx + rbx], xmm0
004CE357  addss    xmm4, xmm1
004CE35B  movss    dword ptr [rip + 0x1b9696c], xmm10  ; -> 02064CD0
004CE364  addss    xmm5, xmm1
004CE368  movss    dword ptr [rip + 0x1b9696f], xmm11  ; -> 02064CE0
004CE371  addss    xmm8, xmm1
004CE376  movss    dword ptr [rip + 0x1b96971], xmm12  ; -> 02064CF0
004CE37F  addss    xmm13, xmm2
004CE384  addss    xmm9, xmm1
004CE389  movss    dword ptr [rip + 0x1b96943], xmm4  ; -> 02064CD4
004CE391  movups   xmm0, xmmword ptr [rip + 0x1b96938]  ; -> 02064CD0
004CE398  movss    dword ptr [rip + 0x1b96944], xmm5  ; -> 02064CE4
004CE3A0  movups   xmmword ptr [rax + rbx], xmm0
004CE3A4  lea      eax, [r8 + 3]
004CE3A8  movups   xmm0, xmmword ptr [rip + 0x1b96931]  ; -> 02064CE0
004CE3AF  shl      eax, 4
004CE3B2  movsxd   rcx, eax
004CE3B5  lea      eax, [r8 + 6]
004CE3B9  shl      eax, 4
004CE3BC  movss    dword ptr [rip + 0x1b9692f], xmm8  ; -> 02064CF4
004CE3C5  movss    dword ptr [rip + 0x1b96932], xmm13  ; -> 02064D00
004CE3CE  movups   xmmword ptr [rcx + rbx], xmm0
004CE3D2  movsxd   rcx, eax
004CE3D5  lea      eax, [r8 + 9]
004CE3D9  movups   xmm0, xmmword ptr [rip + 0x1b96910]  ; -> 02064CF0
004CE3E0  shl      eax, 4
004CE3E3  movss    dword ptr [rip + 0x1b96918], xmm9  ; -> 02064D04
004CE3EC  movups   xmmword ptr [rcx + rbx], xmm0
004CE3F0  movsxd   rcx, eax
004CE3F3  movups   xmm0, xmmword ptr [rip + 0x1b96906]  ; -> 02064D00
004CE3FA  movups   xmmword ptr [rcx + rbx], xmm0
004CE3FE  mov      rcx, rbp
004CE401  call     0x4c7f00  ; -> 004C7F00 fn
004CE406  movzx    eax, word ptr [rip + 0x1b969cb]  ; -> 02064DD8
004CE40D  movzx    r11d, word ptr [rip + 0x1b969bf]  ; -> 02064DD4
004CE415  inc      ax
004CE418  mov      word ptr [rip + 0x1b969b9], ax  ; -> 02064DD8
004CE41F  movzx    esi, word ptr [rip + 0x1b966e6]  ; -> 02064B0C
004CE426  test     r11w, r11w
004CE42A  jle      0x4cc0f5  ; -> 004CC0F5
004CE430  movzx    edi, word ptr [rip + 0x1b9697d]  ; -> 02064DB4
004CE437  movups   xmm15, xmmword ptr [rip + 0x1b96751]  ; -> 02064B90
004CE43F  jmp      0x4cdf13  ; -> 004CDF13
004CE444  movss    xmm4, dword ptr [rip + 0x19343e4]  ; -> 01E02830 [u32 0x00000000]
004CE44C  lea      rdx, [rip + 0x1b9673d]  ; -> 02064B90
004CE453  movss    xmm5, dword ptr [rip + 0x1b96771]  ; -> 02064BCC
004CE45B  lea      rcx, [rip + 0x1b9672e]  ; -> 02064B90
004CE462  movss    xmm8, dword ptr [rip + 0x1b96755]  ; -> 02064BC0
004CE46B  movaps   xmm0, xmm5
004CE46E  movss    xmm7, dword ptr [rip + 0x1b9674e]  ; -> 02064BC4
004CE476  movaps   xmm3, xmm8
004CE47A  movss    xmm6, dword ptr [rip + 0x1b96746]  ; -> 02064BC8
004CE482  movaps   xmm2, xmm7
004CE485  mulss    xmm3, dword ptr [rip + 0x1b96783]  ; -> 02064C10
004CE48D  movaps   xmm1, xmm6
004CE490  mov      dword ptr [rip + 0x1b9666a], 0x437f0000  ; -> 02064B04
004CE49A  mulss    xmm2, dword ptr [rip + 0x1b96772]  ; -> 02064C14
004CE4A2  mulss    xmm1, dword ptr [rip + 0x1b9676e]  ; -> 02064C18
004CE4AA  maxss    xmm3, xmm4
004CE4AE  mulss    xmm0, dword ptr [rip + 0x1b96766]  ; -> 02064C1C
004CE4B6  maxss    xmm2, xmm4
004CE4BA  mulss    xmm8, dword ptr [rip + 0x1b9673d]  ; -> 02064C00
004CE4C3  maxss    xmm1, xmm4
004CE4C7  mulss    xmm7, dword ptr [rip + 0x1b96735]  ; -> 02064C04
004CE4CF  maxss    xmm0, xmm4
004CE4D3  mulss    xmm6, dword ptr [rip + 0x1b9672d]  ; -> 02064C08
004CE4DB  maxss    xmm8, xmm4
004CE4E0  mulss    xmm5, dword ptr [rip + 0x1b96724]  ; -> 02064C0C
004CE4E8  maxss    xmm7, xmm4
004CE4EC  movss    dword ptr [rip + 0x1b9669c], xmm3  ; -> 02064B90
004CE4F4  maxss    xmm6, xmm4
004CE4F8  movss    xmm3, dword ptr [rip + 0x3f7640]  ; -> 008C5B40 [f32 255]
004CE500  movss    dword ptr [rip + 0x1b9668c], xmm2  ; -> 02064B94
004CE508  maxss    xmm5, xmm4
004CE50C  movaps   xmm2, xmm3
004CE50F  movss    dword ptr [rip + 0x1b96681], xmm1  ; -> 02064B98
004CE517  movss    dword ptr [rip + 0x1b9667d], xmm0  ; -> 02064B9C
004CE51F  movss    dword ptr [rip + 0x1b96698], xmm8  ; -> 02064BC0
004CE528  movss    dword ptr [rip + 0x1b96694], xmm7  ; -> 02064BC4
004CE530  movss    dword ptr [rip + 0x1b96690], xmm6  ; -> 02064BC8
004CE538  movss    dword ptr [rip + 0x1b9668c], xmm5  ; -> 02064BCC
004CE540  call     0x4cf230  ; -> 004CF230 fn
004CE545  lea      eax, [rsi + 2]
004CE548  lea      rdx, [rip + 0x1b96671]  ; -> 02064BC0
004CE54F  mov      word ptr [rip + 0x1b9687a], ax  ; -> 02064DD0
004CE556  lea      rcx, [rip + 0x1b96663]  ; -> 02064BC0
004CE55D  call     0x4cf230  ; -> 004CF230 fn
004CE562  movups   xmm0, xmmword ptr [rip + 0x1b96627]  ; -> 02064B90
004CE569  movsx    eax, word ptr [rip + 0x1b9686c]  ; -> 02064DDC
004CE570  movzx    edx, si
004CE573  movss    xmm9, dword ptr [rip + 0x181d708]  ; -> 01CEBC84 [f32 16]
004CE57C  mov      ecx, eax
004CE57E  cvttps2dq xmm4, xmm0
004CE582  add      cx, si
004CE585  mov      word ptr [rip + 0x1b9684c], dx  ; -> 02064DD8
004CE58C  mov      word ptr [rip + 0x1b96841], cx  ; -> 02064DD4
004CE593  movups   xmm0, xmmword ptr [rip + 0x1b96626]  ; -> 02064BC0
004CE59A  movups   xmmword ptr [rip + 0x1b965ef], xmm4  ; -> 02064B90
004CE5A1  cvttps2dq xmm13, xmm0
004CE5A6  movups   xmmword ptr [rip + 0x1b96612], xmm13  ; -> 02064BC0
004CE5AE  cmp      ax, si
004CE5B1  je       0x4cea63  ; -> 004CEA63
004CE5B7  nop      word ptr [rax + rax]
004CE5C0  dec      cx
004CE5C3  movsx    r9d, dx
004CE5C7  mov      word ptr [rip + 0x1b96806], cx  ; -> 02064DD4
004CE5CE  lea      eax, [r9 + 0xc8]
004CE5D5  shl      eax, 4
004CE5D8  movsxd   rcx, eax
004CE5DB  movsx    eax, word ptr [rcx + rbx]
004CE5DF  movsx    edx, word ptr [rcx + rbx + 4]
004CE5E4  mov      r10d, eax
004CE5E7  movsx    r8d, word ptr [rcx + rbx + 8]
004CE5ED  mov      word ptr [rip + 0x1b967c8], ax  ; -> 02064DBC
004CE5F4  add      eax, 0x190
004CE5F9  shl      eax, 4
004CE5FC  movsxd   rcx, eax
004CE5FF  lea      eax, [rdx + 0x190]
004CE605  shl      eax, 4
004CE608  mov      word ptr [rip + 0x1b967b1], dx  ; -> 02064DC0
004CE60F  mov      word ptr [rip + 0x1b967ad], r8w  ; -> 02064DC4
004CE617  movups   xmm0, xmmword ptr [rcx + rbx]
004CE61B  movsxd   rcx, eax
004CE61E  lea      eax, [r8 + 0x190]
004CE625  shl      eax, 4
004CE628  movups   xmmword ptr [rip + 0x1b96671], xmm0  ; -> 02064CA0
004CE62F  movups   xmm0, xmmword ptr [rcx + rbx]
004CE633  movsxd   rcx, eax
004CE636  lea      eax, [r10 + 0x28a]
004CE63D  shl      eax, 4
004CE640  movups   xmmword ptr [rip + 0x1b96669], xmm0  ; -> 02064CB0
004CE647  movups   xmm0, xmmword ptr [rcx + rbx]
004CE64B  movsxd   rcx, eax
004CE64E  lea      eax, [rdx + 0x28a]
004CE654  shl      eax, 4
004CE657  movups   xmmword ptr [rip + 0x1b96662], xmm0  ; -> 02064CC0
004CE65E  movups   xmm0, xmmword ptr [rcx + rbx]
004CE662  movsxd   rcx, eax
004CE665  lea      eax, [r8 + 0x28a]
004CE66C  shl      eax, 4
004CE66F  movups   xmmword ptr [rip + 0x1b9665a], xmm0  ; -> 02064CD0
004CE676  movups   xmm0, xmmword ptr [rcx + rbx]
004CE67A  movsxd   rcx, eax
004CE67D  lea      eax, [r9 + 0xfa]
004CE684  movss    xmm10, dword ptr [rip + 0x1b96647]  ; -> 02064CD4
004CE68D  movups   xmmword ptr [rip + 0x1b9664c], xmm0  ; -> 02064CE0
004CE694  shl      eax, 4
004CE697  cmp      word ptr [rip + 0x1b96746], si  ; -> 02064DE4
004CE69E  movups   xmm0, xmmword ptr [rcx + rbx]
004CE6A2  movsxd   rcx, eax
004CE6A5  movss    xmm11, dword ptr [rip + 0x1b96636]  ; -> 02064CE4
004CE6AE  movups   xmmword ptr [rip + 0x1b9663b], xmm0  ; -> 02064CF0
004CE6B5  movups   xmm0, xmmword ptr [rcx + rbx]
004CE6B9  movss    xmm12, dword ptr [rip + 0x1b96632]  ; -> 02064CF4
004CE6C2  movups   xmmword ptr [rip + 0x1b96587], xmm0  ; -> 02064C50
004CE6C9  je       0x4ce6e2  ; -> 004CE6E2
004CE6CB  movss    xmm0, dword ptr [rip + 0x1b964e1]  ; -> 02064BB4
004CE6D3  mulss    xmm10, xmm0
004CE6D8  mulss    xmm11, xmm0
004CE6DD  mulss    xmm12, xmm0
004CE6E2  movss    xmm0, dword ptr [rip + 0x1b9662a]  ; -> 02064D14
004CE6EA  lea      eax, [r10 + 0x258]
004CE6F1  movss    xmm1, dword ptr [rip + 0x1b9655b]  ; -> 02064C54
004CE6F9  mulss    xmm1, dword ptr [rip + 0x1b964ab]  ; -> 02064BAC
004CE701  shl      eax, 4
004CE704  movss    xmm2, dword ptr [rip + 0x1b96544]  ; -> 02064C50
004CE70C  mulss    xmm2, dword ptr [rip + 0x1b96498]  ; -> 02064BAC
004CE714  movsxd   rcx, eax
004CE717  lea      eax, [rdx + 0x258]
004CE71D  movss    xmm3, dword ptr [rip + 0x1b965f3]  ; -> 02064D18
004CE725  addss    xmm10, xmm1
004CE72A  movss    xmm5, dword ptr [rip + 0x1b9659e]  ; -> 02064CD0
004CE732  addss    xmm11, xmm1
004CE737  movss    xmm7, dword ptr [rip + 0x1b965a1]  ; -> 02064CE0
004CE73F  addss    xmm12, xmm1
004CE744  movss    xmm8, dword ptr [rip + 0x1b965a3]  ; -> 02064CF0
004CE74D  addss    xmm5, xmm2
004CE751  shl      eax, 4
004CE754  addss    xmm7, xmm2
004CE758  movss    dword ptr [rip + 0x1b964f4], xmm1  ; -> 02064C54
004CE760  addss    xmm8, xmm2
004CE765  movss    xmm1, dword ptr [rip + 0x1b965af]  ; -> 02064D1C
004CE76D  mulss    xmm10, xmm1
004CE772  mulss    xmm11, xmm1
004CE777  mulss    xmm12, xmm1
004CE77C  addss    xmm10, xmm0
004CE781  movss    xmm1, dword ptr [rip + 0x1b96587]  ; -> 02064D10
004CE789  addss    xmm11, xmm0
004CE78E  movss    dword ptr [rip + 0x1b964ba], xmm2  ; -> 02064C50
004CE796  movups   xmm2, xmmword ptr [rcx + rbx]
004CE79A  movsxd   rcx, eax
004CE79D  lea      eax, [r8 + 0x258]
004CE7A4  shl      eax, 4
004CE7A7  addss    xmm12, xmm0
004CE7AC  movss    xmm0, dword ptr [rip + 0x1b964ec]  ; -> 02064CA0
004CE7B4  mulss    xmm0, xmm9
004CE7B9  movsx    r8d, di
004CE7BD  movups   xmm4, xmmword ptr [rcx + rbx]
004CE7C1  movsxd   rcx, eax
004CE7C4  mov      edx, r8d
004CE7C7  cvttss2si eax, xmm0
004CE7CB  shl      edx, 4
004CE7CE  movups   xmm6, xmmword ptr [rcx + rbx]
004CE7D2  mov      dword ptr [rip + 0x1b964c8], eax  ; -> 02064CA0
004CE7D8  movss    xmm0, dword ptr [rip + 0x1b964c8]  ; -> 02064CA8
004CE7E0  mulss    xmm0, xmm9
004CE7E5  mulss    xmm5, xmm3
004CE7E9  mulss    xmm7, xmm3
004CE7ED  addss    xmm5, xmm1
004CE7F1  mulss    xmm8, xmm3
004CE7F6  addss    xmm7, xmm1
004CE7FA  movups   xmmword ptr [rip + 0x1b9633f], xmm2  ; -> 02064B40
004CE801  addss    xmm8, xmm1
004CE806  movss    xmm1, dword ptr [rip + 0x1b96496]  ; -> 02064CA4
004CE80E  mulss    xmm1, xmm9
004CE813  movups   xmmword ptr [rip + 0x1b96336], xmm4  ; -> 02064B50
004CE81A  cvttss2si eax, xmm1
004CE81E  movss    xmm1, dword ptr [rip + 0x1b9648a]  ; -> 02064CB0
004CE826  mov      dword ptr [rip + 0x1b96478], eax  ; -> 02064CA4
004CE82C  cvttss2si eax, xmm0
004CE830  movss    xmm0, dword ptr [rip + 0x1b9647c]  ; -> 02064CB4
004CE838  mov      dword ptr [rip + 0x1b9646a], eax  ; -> 02064CA8
004CE83E  lea      eax, [rdx + 0x10]
004CE841  movsxd   rcx, eax
004CE844  mulss    xmm1, xmm9
004CE849  mulss    xmm0, xmm9
004CE84E  cvttss2si eax, xmm1
004CE852  movss    xmm1, dword ptr [rip + 0x1b9645e]  ; -> 02064CB8
004CE85A  mov      dword ptr [rip + 0x1b96450], eax  ; -> 02064CB0
004CE860  cvttss2si eax, xmm0
004CE864  mulss    xmm1, xmm9
004CE869  mov      dword ptr [rip + 0x1b96445], eax  ; -> 02064CB4
004CE86F  movups   xmmword ptr [rcx + rbx], xmm13
004CE874  cvttss2si eax, xmm1
004CE878  movss    xmm1, dword ptr [rip + 0x1b96440]  ; -> 02064CC0
004CE880  mov      dword ptr [rip + 0x1b96432], eax  ; -> 02064CB8
004CE886  lea      eax, [r8 + 4]
004CE88A  shl      eax, 4
004CE88D  movsxd   rcx, eax
004CE890  movups   xmmword ptr [rip + 0x1b962c9], xmm6  ; -> 02064B60
004CE897  movups   xmmword ptr [rcx + rbx], xmm13
004CE89C  movss    xmm0, dword ptr [rip + 0x1b96420]  ; -> 02064CC4
004CE8A4  add      di, 9
004CE8A8  inc      word ptr [rip + 0x1b96509]  ; -> 02064DB8
004CE8AF  mulss    xmm0, xmm9
004CE8B4  mov      word ptr [rip + 0x1b964f9], di  ; -> 02064DB4
004CE8BB  mulss    xmm1, xmm9
004CE8C0  shufps   xmm2, xmm2, 0xff
004CE8C4  shufps   xmm4, xmm4, 0xff
004CE8C8  cvttss2si eax, xmm1
004CE8CC  movss    xmm1, dword ptr [rip + 0x1b963f4]  ; -> 02064CC8
004CE8D4  mov      dword ptr [rip + 0x1b963e6], eax  ; -> 02064CC0
004CE8DA  cvttss2si eax, xmm0
004CE8DE  movss    xmm0, dword ptr [rip + 0x1b963f2]  ; -> 02064CD8
004CE8E6  mov      dword ptr [rip + 0x1b963d8], eax  ; -> 02064CC4
004CE8EC  mulss    xmm0, xmm2
004CE8F0  mulss    xmm1, xmm9
004CE8F5  movss    dword ptr [rip + 0x1b963db], xmm0  ; -> 02064CD8
004CE8FD  movups   xmm0, xmmword ptr [rip + 0x1b9639c]  ; -> 02064CA0
004CE904  cvttss2si eax, xmm1
004CE908  shufps   xmm6, xmm6, 0xff
004CE90C  mov      dword ptr [rip + 0x1b963b6], eax  ; -> 02064CC8
004CE912  lea      eax, [r8 + 7]
004CE916  shl      eax, 4
004CE919  movsxd   rcx, eax
004CE91C  lea      eax, [r8 + 2]
004CE920  shl      eax, 4
004CE923  mulss    xmm5, xmm2
004CE927  movups   xmmword ptr [rcx + rbx], xmm13
004CE92C  movsxd   rcx, eax
004CE92F  lea      eax, [r8 + 5]
004CE933  shl      eax, 4
004CE936  mulss    xmm10, xmm2
004CE93B  movups   xmmword ptr [rcx + rbx], xmm0
004CE93F  movsxd   rcx, eax
004CE942  lea      eax, [r8 + 8]
004CE946  movss    xmm0, dword ptr [rip + 0x1b9639a]  ; -> 02064CE8
004CE94E  mulss    xmm0, xmm4
004CE952  shl      eax, 4
004CE955  movss    dword ptr [rip + 0x1b96373], xmm5  ; -> 02064CD0
004CE95D  movss    dword ptr [rip + 0x1b9636e], xmm10  ; -> 02064CD4
004CE966  movss    dword ptr [rip + 0x1b9637a], xmm0  ; -> 02064CE8
004CE96E  movups   xmm0, xmmword ptr [rip + 0x1b9633b]  ; -> 02064CB0
004CE975  mulss    xmm7, xmm4
004CE979  movups   xmmword ptr [rcx + rbx], xmm0
004CE97D  movsxd   rcx, eax
004CE980  movss    xmm0, dword ptr [rip + 0x1b96370]  ; -> 02064CF8
004CE988  mulss    xmm0, xmm6
004CE98C  movsxd   rax, edx
004CE98F  mov      rdx, r14
004CE992  mulss    xmm11, xmm4
004CE997  movss    dword ptr [rip + 0x1b96359], xmm0  ; -> 02064CF8
004CE99F  movups   xmm0, xmmword ptr [rip + 0x1b9631a]  ; -> 02064CC0
004CE9A6  movss    dword ptr [rip + 0x1b96332], xmm7  ; -> 02064CE0
004CE9AE  movups   xmmword ptr [rcx + rbx], xmm0
004CE9B2  movups   xmm0, xmmword ptr [rip + 0x1b96317]  ; -> 02064CD0
004CE9B9  movss    dword ptr [rip + 0x1b96322], xmm11  ; -> 02064CE4
004CE9C2  movups   xmmword ptr [rax + rbx], xmm0
004CE9C6  lea      eax, [r8 + 3]
004CE9CA  movups   xmm0, xmmword ptr [rip + 0x1b9630f]  ; -> 02064CE0
004CE9D1  shl      eax, 4
004CE9D4  movsxd   rcx, eax
004CE9D7  lea      eax, [r8 + 6]
004CE9DB  shl      eax, 4
004CE9DE  mulss    xmm8, xmm6
004CE9E3  movups   xmmword ptr [rcx + rbx], xmm0
004CE9E7  movsxd   rcx, eax
004CE9EA  movss    dword ptr [rip + 0x1b962fd], xmm8  ; -> 02064CF0
004CE9F3  mulss    xmm12, xmm6
004CE9F8  movss    dword ptr [rip + 0x1b9614c], xmm2  ; -> 02064B4C
004CEA00  movss    dword ptr [rip + 0x1b96154], xmm4  ; -> 02064B5C
004CEA08  movss    dword ptr [rip + 0x1b962e3], xmm12  ; -> 02064CF4
004CEA11  movups   xmm0, xmmword ptr [rip + 0x1b962d8]  ; -> 02064CF0
004CEA18  movups   xmmword ptr [rcx + rbx], xmm0
004CEA1C  mov      rcx, rbp
004CEA1F  call     0x4c7f00  ; -> 004C7F00 fn
004CEA24  movzx    edx, word ptr [rip + 0x1b963ad]  ; -> 02064DD8
004CEA2B  movzx    ecx, word ptr [rip + 0x1b963a2]  ; -> 02064DD4
004CEA32  inc      dx
004CEA35  movzx    esi, word ptr [rip + 0x1b960d0]  ; -> 02064B0C
004CEA3C  movzx    edi, word ptr [rip + 0x1b96371]  ; -> 02064DB4
004CEA43  mov      word ptr [rip + 0x1b9638e], dx  ; -> 02064DD8
004CEA4A  test     cx, cx
004CEA4D  jle      0x4cea5c  ; -> 004CEA5C
004CEA4F  movups   xmm13, xmmword ptr [rip + 0x1b96169]  ; -> 02064BC0
004CEA57  jmp      0x4ce5c0  ; -> 004CE5C0
004CEA5C  movups   xmm4, xmmword ptr [rip + 0x1b9612d]  ; -> 02064B90
004CEA63  movzx    ecx, word ptr [rip + 0x1b96376]  ; -> 02064DE0
004CEA6A  cmp      cx, si
004CEA6D  je       0x4cc0f5  ; -> 004CC0F5
004CEA73  movss    xmm14, dword ptr [rip + 0x431884]  ; -> 00900300 [f32 -0.05]
004CEA7C  lea      eax, [rsi + 3]
004CEA7F  mov      word ptr [rip + 0x1b9634a], ax  ; -> 02064DD0
004CEA86  movsx    eax, cx
004CEA89  movzx    ecx, si
004CEA8C  mov      word ptr [rip + 0x1b96345], cx  ; -> 02064DD8
004CEA93  add      ax, si
004CEA96  nop      word ptr [rax + rax]
004CEAA0  dec      ax
004CEAA3  movsx    r8d, cx
004CEAA7  mov      word ptr [rip + 0x1b96326], ax  ; -> 02064DD4
004CEAAE  lea      eax, [r8 + 0x12c]
004CEAB5  shl      eax, 4
004CEAB8  movsxd   rcx, eax
004CEABB  movsx    edx, word ptr [rcx + rbx + 4]
004CEAC0  movsx    eax, word ptr [rcx + rbx]
004CEAC4  mov      r10d, edx
004CEAC7  mov      word ptr [rip + 0x1b962ee], ax  ; -> 02064DBC
004CEACE  mov      r9d, eax
004CEAD1  add      eax, 0x190
004CEAD6  mov      word ptr [rip + 0x1b962e3], dx  ; -> 02064DC0
004CEADD  shl      eax, 4
004CEAE0  movsxd   rcx, eax
004CEAE3  lea      eax, [rdx + 0x190]
004CEAE9  shl      eax, 4
004CEAEC  movups   xmm0, xmmword ptr [rcx + rbx]
004CEAF0  movsxd   rcx, eax
004CEAF3  lea      eax, [r9 + 0x1f4]
004CEAFA  shl      eax, 4
004CEAFD  movups   xmmword ptr [rip + 0x1b9618c], xmm0  ; -> 02064C90
004CEB04  movups   xmm0, xmmword ptr [rcx + rbx]
004CEB08  movsxd   rcx, eax
004CEB0B  lea      eax, [rdx + 0x1f4]
004CEB11  shl      eax, 4
004CEB14  movups   xmmword ptr [rip + 0x1b96185], xmm0  ; -> 02064CA0
004CEB1B  movups   xmm0, xmmword ptr [rcx + rbx]
004CEB1F  movsxd   rcx, eax
004CEB22  lea      eax, [r9 + 0x28a]
004CEB29  shl      eax, 4
004CEB2C  movups   xmmword ptr [rip + 0x1b9617d], xmm0  ; -> 02064CB0
004CEB33  movups   xmm0, xmmword ptr [rcx + rbx]
004CEB37  movsxd   rcx, eax
004CEB3A  lea      eax, [rdx + 0x28a]
004CEB40  shl      eax, 4
004CEB43  movups   xmmword ptr [rip + 0x1b96176], xmm0  ; -> 02064CC0
004CEB4A  movups   xmm0, xmmword ptr [rcx + rbx]
004CEB4E  movsxd   rcx, eax
004CEB51  lea      eax, [r9 + 0x2ee]
004CEB58  shl      eax, 4
004CEB5B  movups   xmmword ptr [rip + 0x1b9616e], xmm0  ; -> 02064CD0
004CEB62  movups   xmm0, xmmword ptr [rcx + rbx]
004CEB66  movsxd   rcx, eax
004CEB69  lea      eax, [rdx + 0x2ee]
004CEB6F  movss    xmm10, dword ptr [rip + 0x1b9615c]  ; -> 02064CD4
004CEB78  movups   xmmword ptr [rip + 0x1b96161], xmm0  ; -> 02064CE0
004CEB7F  shl      eax, 4
004CEB82  movups   xmm0, xmmword ptr [rcx + rbx]
004CEB86  movsxd   rcx, eax
004CEB89  lea      eax, [r8 + 0x177]
004CEB90  movss    xmm11, dword ptr [rip + 0x1b9614b]  ; -> 02064CE4
004CEB99  movups   xmmword ptr [rip + 0x1b96150], xmm0  ; -> 02064CF0
004CEBA0  shl      eax, 4
004CEBA3  cmp      word ptr [rip + 0x1b9623a], si  ; -> 02064DE4
004CEBAA  movups   xmm0, xmmword ptr [rcx + rbx]
004CEBAE  movsxd   rcx, eax
004CEBB1  movss    xmm12, dword ptr [rip + 0x1b9613a]  ; -> 02064CF4
004CEBBA  movups   xmmword ptr [rip + 0x1b9613f], xmm0  ; -> 02064D00
004CEBC1  movups   xmm0, xmmword ptr [rcx + rbx]
004CEBC5  movss    xmm13, dword ptr [rip + 0x1b96136]  ; -> 02064D04
004CEBCE  movups   xmmword ptr [rip + 0x1b95f7b], xmm0  ; -> 02064B50
004CEBD5  movups   xmmword ptr [rip + 0x1b95f84], xmm0  ; -> 02064B60
004CEBDC  je       0x4cebfa  ; -> 004CEBFA
004CEBDE  movss    xmm0, dword ptr [rip + 0x1b95fce]  ; -> 02064BB4
004CEBE6  mulss    xmm10, xmm0
004CEBEB  mulss    xmm11, xmm0
004CEBF0  mulss    xmm12, xmm0
004CEBF5  mulss    xmm13, xmm0
004CEBFA  movss    xmm2, dword ptr [rip + 0x1b95f52]  ; -> 02064B54
004CEC02  lea      eax, [r8 + 0x15e]
004CEC09  mulss    xmm2, dword ptr [rip + 0x1b95f9f]  ; -> 02064BB0
004CEC11  shl      eax, 4
004CEC14  movss    xmm0, dword ptr [rip + 0x1b95f48]  ; -> 02064B64
004CEC1C  movss    xmm1, dword ptr [rip + 0x1b95f3c]  ; -> 02064B60
004CEC24  movss    xmm3, dword ptr [rip + 0x1b95f24]  ; -> 02064B50
004CEC2C  mulss    xmm3, dword ptr [rip + 0x1b95f7c]  ; -> 02064BB0
004CEC34  movsxd   rcx, eax
004CEC37  movss    xmm5, dword ptr [rip + 0x1b96091]  ; -> 02064CD0
004CEC3F  movss    xmm6, dword ptr [rip + 0x1b96099]  ; -> 02064CE0
004CEC47  movss    xmm7, dword ptr [rip + 0x1b960a1]  ; -> 02064CF0
004CEC4F  movss    xmm8, dword ptr [rip + 0x1b960a8]  ; -> 02064D00
004CEC58  mulss    xmm1, xmm14
004CEC5D  movsx    r8d, di
004CEC61  mulss    xmm0, xmm14
004CEC66  mov      edx, r8d
004CEC69  shl      edx, 4
004CEC6C  addss    xmm5, xmm1
004CEC70  mov      dword ptr [rip + 0x1b95e8a], 0xbd4ccccd  ; -> 02064B04
004CEC7A  addss    xmm6, xmm1
004CEC7E  addss    xmm3, xmm1
004CEC82  addss    xmm2, xmm0
004CEC86  addss    xmm10, xmm0
004CEC8B  addss    xmm11, xmm0
004CEC90  movss    xmm0, dword ptr [rip + 0x1b96084]  ; -> 02064D1C
004CEC98  lea      eax, [rdx + 0x10]
004CEC9B  addss    xmm7, xmm3
004CEC9F  addss    xmm12, xmm2
004CECA4  addss    xmm13, xmm2
004CECA9  movups   xmm2, xmmword ptr [rcx + rbx]
004CECAD  movsxd   rcx, eax
004CECB0  lea      eax, [r8 + 4]
004CECB4  shl      eax, 4
004CECB7  addss    xmm8, xmm3
004CECBC  movups   xmmword ptr [rip + 0x1b95f8d], xmm2  ; -> 02064C50
004CECC3  mulss    xmm2, dword ptr [rip + 0x1b95ee1]  ; -> 02064BAC
004CECCB  movss    xmm1, dword ptr [rip + 0x1b95f81]  ; -> 02064C54
004CECD3  mulss    xmm1, dword ptr [rip + 0x1b95ed1]  ; -> 02064BAC
004CECDB  movups   xmmword ptr [rcx + rbx], xmm4
004CECDF  movsxd   rcx, eax
004CECE2  lea      eax, [r8 + 7]
004CECE6  movss    dword ptr [rip + 0x1b95f66], xmm1  ; -> 02064C54
004CECEE  addss    xmm5, xmm2
004CECF2  addss    xmm10, xmm1
004CECF7  shl      eax, 4
004CECFA  addss    xmm11, xmm1
004CECFF  movss    dword ptr [rip + 0x1b95f49], xmm2  ; -> 02064C50
004CED07  addss    xmm12, xmm1
004CED0C  addss    xmm13, xmm1
004CED11  movss    xmm1, dword ptr [rip + 0x1b95fff]  ; -> 02064D18
004CED19  movups   xmmword ptr [rcx + rbx], xmm4
004CED1D  movsxd   rcx, eax
004CED20  lea      eax, [r8 + 0xa]
004CED24  mulss    xmm5, xmm1
004CED28  addss    xmm6, xmm2
004CED2C  shl      eax, 4
004CED2F  addss    xmm7, xmm2
004CED33  mulss    xmm10, xmm0
004CED38  addss    xmm8, xmm2
004CED3D  mulss    xmm11, xmm0
004CED42  movss    xmm2, dword ptr [rip + 0x1b95fc6]  ; -> 02064D10
004CED4A  mulss    xmm6, xmm1
004CED4E  addss    xmm5, xmm2
004CED52  mulss    xmm7, xmm1
004CED56  mulss    xmm8, xmm1
004CED5B  addss    xmm6, xmm2
004CED5F  movss    xmm1, dword ptr [rip + 0x1b95fad]  ; -> 02064D14
004CED67  addss    xmm7, xmm2
004CED6B  movups   xmmword ptr [rcx + rbx], xmm4
004CED6F  movsxd   rcx, eax
004CED72  addss    xmm10, xmm1
004CED77  mulss    xmm12, xmm0
004CED7C  addss    xmm11, xmm1
004CED81  mulss    xmm13, xmm0
004CED86  addss    xmm12, xmm1
004CED8B  addss    xmm8, xmm2
004CED90  addss    xmm13, xmm1
004CED95  movss    xmm1, dword ptr [rip + 0x1b95ef3]  ; -> 02064C90
004CED9D  mulss    xmm1, xmm9
004CEDA2  movups   xmmword ptr [rcx + rbx], xmm4
004CEDA6  movss    xmm0, dword ptr [rip + 0x1b95ee6]  ; -> 02064C94
004CEDAE  cvttss2si eax, xmm1
004CEDB2  movss    xmm1, dword ptr [rip + 0x1b95ede]  ; -> 02064C98
004CEDBA  mov      dword ptr [rip + 0x1b95ed0], eax  ; -> 02064C90
004CEDC0  mulss    xmm1, xmm9
004CEDC5  mulss    xmm0, xmm9
004CEDCA  cvttss2si eax, xmm0
004CEDCE  movss    xmm0, dword ptr [rip + 0x1b95ece]  ; -> 02064CA4
004CEDD6  mov      dword ptr [rip + 0x1b95eb8], eax  ; -> 02064C94
004CEDDC  cvttss2si eax, xmm1
004CEDE0  movss    xmm1, dword ptr [rip + 0x1b95eb8]  ; -> 02064CA0
004CEDE8  mov      dword ptr [rip + 0x1b95eaa], eax  ; -> 02064C98
004CEDEE  lea      eax, [r9 + 0x258]
004CEDF5  shl      eax, 4
004CEDF8  movsxd   rcx, eax
004CEDFB  mulss    xmm1, xmm9
004CEE00  mulss    xmm0, xmm9
004CEE05  movups   xmm4, xmmword ptr [rcx + rbx]
004CEE09  cvttss2si eax, xmm1
004CEE0D  movss    xmm1, dword ptr [rip + 0x1b95e93]  ; -> 02064CA8
004CEE15  mov      dword ptr [rip + 0x1b95e85], eax  ; -> 02064CA0
004CEE1B  mulss    xmm1, xmm9
004CEE20  cvttss2si eax, xmm0
004CEE24  movss    xmm0, dword ptr [rip + 0x1b95e88]  ; -> 02064CB4
004CEE2C  mov      dword ptr [rip + 0x1b95e72], eax  ; -> 02064CA4
004CEE32  cvttss2si eax, xmm1
004CEE36  movss    xmm1, dword ptr [rip + 0x1b95e72]  ; -> 02064CB0
004CEE3E  mov      dword ptr [rip + 0x1b95e64], eax  ; -> 02064CA8
004CEE44  lea      eax, [r10 + 0x258]
004CEE4B  shl      eax, 4
004CEE4E  movsxd   rcx, eax
004CEE51  mulss    xmm1, xmm9
004CEE56  mulss    xmm0, xmm9
004CEE5B  movups   xmm2, xmmword ptr [rcx + rbx]
004CEE5F  cvttss2si eax, xmm1
004CEE63  movss    xmm1, dword ptr [rip + 0x1b95e4d]  ; -> 02064CB8
004CEE6B  mov      dword ptr [rip + 0x1b95e3f], eax  ; -> 02064CB0
004CEE71  cvttss2si eax, xmm0
004CEE75  movss    xmm0, dword ptr [rip + 0x1b95e47]  ; -> 02064CC4
004CEE7D  mov      dword ptr [rip + 0x1b95e31], eax  ; -> 02064CB4
004CEE83  mulss    xmm1, xmm9
004CEE88  mulss    xmm0, xmm9
004CEE8D  cvttss2si eax, xmm1
004CEE91  movss    xmm1, dword ptr [rip + 0x1b95e27]  ; -> 02064CC0
004CEE99  mov      dword ptr [rip + 0x1b95e19], eax  ; -> 02064CB8
004CEE9F  lea      eax, [r9 + 0x2bc]
004CEEA6  shl      eax, 4
004CEEA9  movsxd   rcx, eax
004CEEAC  mulss    xmm1, xmm9
004CEEB1  movups   xmmword ptr [rip + 0x1b95c98], xmm2  ; -> 02064B50
004CEEB8  movups   xmm3, xmmword ptr [rcx + rbx]
004CEEBC  cvttss2si eax, xmm1
004CEEC0  movss    xmm1, dword ptr [rip + 0x1b95e00]  ; -> 02064CC8
004CEEC8  mov      dword ptr [rip + 0x1b95df2], eax  ; -> 02064CC0
004CEECE  cvttss2si eax, xmm0
004CEED2  movss    xmm0, dword ptr [rip + 0x1b95dfe]  ; -> 02064CD8
004CEEDA  mov      dword ptr [rip + 0x1b95de4], eax  ; -> 02064CC4
004CEEE0  shufps   xmm2, xmm2, 0xff
004CEEE4  mulss    xmm1, xmm9
004CEEE9  mulss    xmm0, xmm2
004CEEED  cvttss2si eax, xmm1
004CEEF1  movss    dword ptr [rip + 0x1b95ddf], xmm0  ; -> 02064CD8
004CEEF9  movups   xmm0, xmmword ptr [rip + 0x1b95d90]  ; -> 02064C90
004CEF00  mov      dword ptr [rip + 0x1b95dc2], eax  ; -> 02064CC8
004CEF06  lea      eax, [r10 + 0x2bc]
004CEF0D  shl      eax, 4
004CEF10  movsxd   rcx, eax
004CEF13  lea      eax, [r8 + 2]
004CEF17  shl      eax, 4
004CEF1A  mulss    xmm5, xmm2
004CEF1E  movups   xmm1, xmmword ptr [rcx + rbx]
004CEF22  movsxd   rcx, eax
004CEF25  mulss    xmm10, xmm2
004CEF2A  movups   xmmword ptr [rip + 0x1b95c0f], xmm4  ; -> 02064B40
004CEF31  movups   xmmword ptr [rcx + rbx], xmm0
004CEF35  movss    dword ptr [rip + 0x1b95c1f], xmm2  ; -> 02064B5C
004CEF3D  movss    dword ptr [rip + 0x1b95d8b], xmm5  ; -> 02064CD0
004CEF45  movss    dword ptr [rip + 0x1b95d86], xmm10  ; -> 02064CD4
004CEF4E  movups   xmmword ptr [rip + 0x1b95c0b], xmm3  ; -> 02064B60
004CEF55  movups   xmmword ptr [rip + 0x1b95c14], xmm1  ; -> 02064B70
004CEF5C  shufps   xmm4, xmm4, 0xff
004CEF60  movss    xmm0, dword ptr [rip + 0x1b95d80]  ; -> 02064CE8
004CEF68  lea      eax, [r8 + 5]
004CEF6C  inc      word ptr [rip + 0x1b95e45]  ; -> 02064DB8
004CEF73  add      di, 0xc
004CEF77  mulss    xmm0, xmm4
004CEF7B  shl      eax, 4
004CEF7E  movsxd   rcx, eax
004CEF81  lea      eax, [r8 + 8]
004CEF85  shl      eax, 4
004CEF88  movss    dword ptr [rip + 0x1b95d58], xmm0  ; -> 02064CE8
004CEF90  movups   xmm0, xmmword ptr [rip + 0x1b95d09]  ; -> 02064CA0
004CEF97  mov      word ptr [rip + 0x1b95e16], di  ; -> 02064DB4
004CEF9E  shufps   xmm1, xmm1, 0xff
004CEFA2  movups   xmmword ptr [rcx + rbx], xmm0
004CEFA6  movsxd   rcx, eax
004CEFA9  lea      eax, [r8 + 0xb]
004CEFAD  movss    xmm0, dword ptr [rip + 0x1b95d43]  ; -> 02064CF8
004CEFB5  mulss    xmm0, xmm1
004CEFB9  shl      eax, 4
004CEFBC  shufps   xmm3, xmm3, 0xff
004CEFC0  mulss    xmm6, xmm4
004CEFC4  movss    dword ptr [rip + 0x1b95d2c], xmm0  ; -> 02064CF8
004CEFCC  movups   xmm0, xmmword ptr [rip + 0x1b95cdd]  ; -> 02064CB0
004CEFD3  mulss    xmm11, xmm4
004CEFD8  movups   xmmword ptr [rcx + rbx], xmm0
004CEFDC  movsxd   rcx, eax
004CEFDF  movss    xmm0, dword ptr [rip + 0x1b95d21]  ; -> 02064D08
004CEFE7  mulss    xmm0, xmm3
004CEFEB  movsxd   rax, edx
004CEFEE  mov      rdx, r14
004CEFF1  movss    dword ptr [rip + 0x1b95ce7], xmm6  ; -> 02064CE0
004CEFF9  movss    dword ptr [rip + 0x1b95ce2], xmm11  ; -> 02064CE4
004CF002  movss    dword ptr [rip + 0x1b95cfe], xmm0  ; -> 02064D08
004CF00A  movups   xmm0, xmmword ptr [rip + 0x1b95caf]  ; -> 02064CC0
004CF011  mulss    xmm8, xmm3
004CF016  movups   xmmword ptr [rcx + rbx], xmm0
004CF01A  movups   xmm0, xmmword ptr [rip + 0x1b95cbf]  ; -> 02064CE0
004CF021  mulss    xmm13, xmm3
004CF026  movups   xmmword ptr [rax + rbx], xmm0
004CF02A  lea      eax, [r8 + 3]
004CF02E  movups   xmm0, xmmword ptr [rip + 0x1b95c9b]  ; -> 02064CD0
004CF035  shl      eax, 4
004CF038  movsxd   rcx, eax
004CF03B  lea      eax, [r8 + 6]
004CF03F  shl      eax, 4
004CF042  movss    dword ptr [rip + 0x1b95cb5], xmm8  ; -> 02064D00
004CF04B  movss    dword ptr [rip + 0x1b95cb0], xmm13  ; -> 02064D04
004CF054  movups   xmmword ptr [rcx + rbx], xmm0
004CF058  movsxd   rcx, eax
004CF05B  lea      eax, [r8 + 9]
004CF05F  movups   xmm0, xmmword ptr [rip + 0x1b95c9a]  ; -> 02064D00
004CF066  shl      eax, 4
004CF069  mulss    xmm7, xmm1
004CF06D  movups   xmmword ptr [rcx + rbx], xmm0
004CF071  movsxd   rcx, eax
004CF074  mulss    xmm12, xmm1
004CF079  movss    dword ptr [rip + 0x1b95c6f], xmm7  ; -> 02064CF0
004CF081  movss    dword ptr [rip + 0x1b95ac3], xmm4  ; -> 02064B4C
004CF089  movss    dword ptr [rip + 0x1b95c62], xmm12  ; -> 02064CF4
004CF092  movups   xmm0, xmmword ptr [rip + 0x1b95c57]  ; -> 02064CF0
004CF099  movups   xmmword ptr [rcx + rbx], xmm0
004CF09D  mov      rcx, rbp
004CF0A0  call     0x4c7f00  ; -> 004C7F00 fn
004CF0A5  movzx    ecx, word ptr [rip + 0x1b95d2c]  ; -> 02064DD8
004CF0AC  movzx    eax, word ptr [rip + 0x1b95d21]  ; -> 02064DD4
004CF0B3  inc      cx
004CF0B6  movzx    esi, word ptr [rip + 0x1b95a4f]  ; -> 02064B0C
004CF0BD  mov      word ptr [rip + 0x1b95d14], cx  ; -> 02064DD8
004CF0C4  test     ax, ax
004CF0C7  jle      0x4cc0f5  ; -> 004CC0F5
004CF0CD  movzx    edi, word ptr [rip + 0x1b95ce0]  ; -> 02064DB4
004CF0D4  movups   xmm4, xmmword ptr [rip + 0x1b95ab5]  ; -> 02064B90
004CF0DB  jmp      0x4ceaa0  ; -> 004CEAA0
004CF0E0  mov      dword ptr [0], 0
004CF0EB  movsx    edx, word ptr [rip + 0x1b95a1a]  ; -> 02064B0C
004CF0F2  lea      rbx, [rip + 0x1b95d37]  ; -> 02064E30
004CF0F9  lea      eax, [rdx + 5]
004CF0FC  shl      eax, 4
004CF0FF  movsxd   rcx, eax
004CF102  lea      eax, [rdx + 0xf]
004CF105  shl      eax, 4
004CF108  movups   xmm0, xmmword ptr [rcx + rbx]
004CF10C  movsxd   rcx, eax
004CF10F  lea      eax, [rdx + 6]
004CF112  shl      eax, 4
004CF115  cvtdq2ps xmm5, xmm0
004CF118  movups   xmm2, xmmword ptr [rcx + rbx]
004CF11C  movsxd   rcx, eax
004CF11F  lea      eax, [rdx + 4]
004CF122  movdqu   xmmword ptr [rip + 0x1b95ae6], xmm5  ; -> 02064C10
004CF12A  shl      eax, 4
004CF12D  cvtdq2ps xmm4, xmm2
004CF130  movups   xmm3, xmmword ptr [rcx + rbx]
004CF134  movsxd   rcx, eax
004CF137  movdqu   xmmword ptr [rip + 0x1b95ac1], xmm4  ; -> 02064C00
004CF13F  movups   xmmword ptr [rip + 0x1b95ada], xmm3  ; -> 02064C20
004CF146  movups   xmm0, xmmword ptr [rcx + rbx]
004CF14A  shufps   xmm4, xmm4, 0xff
004CF14E  mulss    xmm4, dword ptr [rip + 0x1b95aca]  ; -> 02064C20
004CF156  movups   xmmword ptr [rip + 0x1b959d3], xmm0  ; -> 02064B30
004CF15D  movss    xmm0, dword ptr [rip + 0x3f69cf]  ; -> 008C5B34 [f32 0.0078125]
004CF165  movss    dword ptr [rip + 0x1b95997], xmm0  ; -> 02064B04
004CF16D  movss    dword ptr [rip + 0x1b95a97], xmm4  ; -> 02064C0C
004CF175  movups   xmm1, xmmword ptr [rip + 0x1b95a84]  ; -> 02064C00
004CF17C  shufps   xmm5, xmm5, 0xff
004CF180  mulss    xmm5, dword ptr [rip + 0x1b95a98]  ; -> 02064C20
004CF188  mulps    xmm1, xmmword ptr [rip + 0x853581]  ; -> 00D22710 [f32x4 0.0078125, 0.0078125, 0.0078125, 0.0078125]
004CF18F  movss    dword ptr [rip + 0x1b95a85], xmm5  ; -> 02064C1C
004CF197  movups   xmm0, xmmword ptr [rip + 0x1b95a72]  ; -> 02064C10
004CF19E  shufps   xmm3, xmm3, 0xff
004CF1A2  mulps    xmm0, xmmword ptr [rip + 0x853567]  ; -> 00D22710 [f32x4 0.0078125, 0.0078125, 0.0078125, 0.0078125]
004CF1A9  mulss    xmm3, dword ptr [rip + 0x181c9bf]  ; -> 01CEBB70 [f32 0.5]
004CF1B1  movups   xmmword ptr [rip + 0x1b95a48], xmm1  ; -> 02064C00
004CF1B8  movups   xmmword ptr [rip + 0x1b95a51], xmm0  ; -> 02064C10
004CF1BF  movss    dword ptr [rip + 0x1b95a65], xmm3  ; -> 02064C2C
004CF1C7  mov      rcx, qword ptr [rsp + 0x1d0]
004CF1CF  xor      rcx, rsp
004CF1D2  call     0x808c40  ; -> 00808C40 fn
004CF1D7  lea      r11, [rsp + 0x288]
004CF1DF  movaps   xmm6, xmmword ptr [r11 - 0x18]
004CF1E4  movaps   xmm7, xmmword ptr [r11 - 0x28]
004CF1E9  movaps   xmm8, xmmword ptr [r11 - 0x38]
004CF1EE  movaps   xmm9, xmmword ptr [r11 - 0x48]
004CF1F3  movaps   xmm10, xmmword ptr [r11 - 0x58]
004CF1F8  movaps   xmm11, xmmword ptr [r11 - 0x68]
004CF1FD  movaps   xmm12, xmmword ptr [r11 - 0x78]
004CF202  movaps   xmm13, xmmword ptr [r11 - 0x88]
004CF20A  movaps   xmm14, xmmword ptr [r11 - 0x98]
004CF212  movaps   xmm15, xmmword ptr [r11 - 0xa8]
004CF21A  mov      rsp, r11
004CF21D  pop      r15
004CF21F  pop      r14
004CF221  pop      rdi
004CF222  pop      rsi
004CF223  pop      rbp
004CF224  pop      rbx
004CF225  ret      
```

## 004CF490 (5098 B, extent 004CF490-004D087A)

Page context: "xFF) - a module record's field init.  Interior anchor '004E2DEE' (function '004E2DE0').  '004D0880' (720 B) is the battery constructor '0037E0F0' calls on its '02AE8xxx' global: '008631E0' registers '004CF490', '008631D0(0x19)' fills '+0x10', '+0x18' = 0x1000404 / '+0x1C' = 0x6C160000 head the constant fill - a module record's init.  Interior anchor '004D089D' (function '004D0880').  '004E7A90' (707 B) is the battery's pure-fill twin of"

```
004CF490  mov      rax, rsp
004CF493  mov      qword ptr [rax + 0x18], rbx
004CF497  push     rbp
004CF498  push     rsi
004CF499  push     rdi
004CF49A  push     r12
004CF49C  push     r13
004CF49E  push     r14
004CF4A0  push     r15
004CF4A2  sub      rsp, 0xd0
004CF4A9  movsx    r10d, word ptr [rip + 0x1b9565b]  ; -> 02064B0C
004CF4B1  lea      rbx, [rip + 0x1b95978]  ; -> 02064E30
004CF4B8  movaps   xmmword ptr [rax - 0x48], xmm6
004CF4BC  mov      r13, rcx
004CF4BF  movaps   xmmword ptr [rax - 0x58], xmm7
004CF4C3  movaps   xmmword ptr [rax - 0x68], xmm8
004CF4C8  movaps   xmmword ptr [rax - 0x78], xmm9
004CF4CD  movaps   xmmword ptr [rax - 0x88], xmm10
004CF4D5  lea      eax, [r10 + 1]
004CF4D9  shl      eax, 4
004CF4DC  movsxd   r8, eax
004CF4DF  lea      eax, [r10 + 2]
004CF4E3  shl      eax, 4
004CF4E6  movsxd   rcx, eax
004CF4E9  lea      eax, [r10 + 3]
004CF4ED  shl      eax, 4
004CF4F0  movups   xmm0, xmmword ptr [r8 + rbx]
004CF4F5  mov      word ptr [rip + 0x1b958bb], r10w  ; -> 02064DB8
004CF4FD  movups   xmm3, xmmword ptr [rcx + rbx]
004CF501  movsxd   rcx, eax
004CF504  movaps   xmmword ptr [rsp + 0x70], xmm11
004CF50A  movaps   xmmword ptr [rsp + 0x60], xmm12
004CF510  movaps   xmmword ptr [rsp + 0x50], xmm13
004CF516  movaps   xmmword ptr [rsp + 0x40], xmm14
004CF51C  movaps   xmmword ptr [rsp + 0x30], xmm15
004CF522  lea      eax, [r10 + 4]
004CF526  mov      word ptr [rip + 0x1b958a2], r10w  ; -> 02064DD0
004CF52E  movups   xmm4, xmmword ptr [rcx + rbx]
004CF532  shl      eax, 4
004CF535  movsxd   rcx, eax
004CF538  lea      eax, [r10 + 5]
004CF53C  shl      eax, 4
004CF53F  movaps   xmm1, xmm4
004CF542  movups   xmmword ptr [rip + 0x1b955e7], xmm0  ; -> 02064B30
004CF549  mov      qword ptr [rsp + 0x20], rdx
004CF54E  movups   xmm0, xmmword ptr [rcx + rbx]
004CF552  movsxd   rcx, eax
004CF555  lea      eax, [r10 + 6]
004CF559  shl      eax, 4
004CF55C  movaps   xmm2, xmm4
004CF55F  movups   xmmword ptr [rip + 0x1b955fa], xmm0  ; -> 02064B60
004CF566  mov      dword ptr [rip + 0x1b95594], 0x3f000000  ; -> 02064B04
004CF570  movups   xmm0, xmmword ptr [rcx + rbx]
004CF574  movsxd   rcx, eax
004CF577  lea      eax, [r10 + 7]
004CF57B  shl      eax, 4
004CF57E  movups   xmmword ptr [rip + 0x1b955eb], xmm0  ; -> 02064B70
004CF585  movups   xmm0, xmmword ptr [rcx + rbx]
004CF589  movsxd   rcx, eax
004CF58C  lea      eax, [r10 + 8]
004CF590  shl      eax, 4
004CF593  movups   xmmword ptr [rip + 0x1b955e6], xmm0  ; -> 02064B80
004CF59A  movups   xmm0, xmmword ptr [rcx + rbx]
004CF59E  movsxd   rcx, eax
004CF5A1  lea      eax, [r10 + 9]
004CF5A5  shl      eax, 4
004CF5A8  movups   xmmword ptr [rip + 0x1b95591], xmm3  ; -> 02064B40
004CF5AF  mulss    xmm3, dword ptr [rip + 0x181c5b9]  ; -> 01CEBB70 [f32 0.5]
004CF5B7  shufps   xmm1, xmm4, 0x55
004CF5BB  movups   xmmword ptr [rip + 0x1b955ce], xmm0  ; -> 02064B90
004CF5C2  movups   xmm0, xmmword ptr [rcx + rbx]
004CF5C6  movsxd   rcx, eax
004CF5C9  mov      eax, 0x12c
004CF5CE  add      eax, r10d
004CF5D1  mulss    xmm2, xmm3
004CF5D5  mov      word ptr [rip + 0x1b957d4], ax  ; -> 02064DB0
004CF5DC  inc      ax
004CF5DF  movups   xmmword ptr [rip + 0x1b9556a], xmm4  ; -> 02064B50
004CF5E6  mov      word ptr [rip + 0x1b957c7], ax  ; -> 02064DB4
004CF5ED  lea      eax, [r10 + 0x64]
004CF5F1  movups   xmmword ptr [rip + 0x1b955a8], xmm0  ; -> 02064BA0
004CF5F8  add      r10w, 0xa
004CF5FD  mov      word ptr [rip + 0x1b957b8], ax  ; -> 02064DBC
004CF604  movups   xmm0, xmmword ptr [rcx + rbx]
004CF608  mov      word ptr [rip + 0x1b957b0], r10w  ; -> 02064DC0
004CF610  mulss    xmm1, xmm3
004CF614  shufps   xmm4, xmm4, 0xaa
004CF618  movss    dword ptr [rip + 0x1b95520], xmm2  ; -> 02064B40
004CF620  movss    dword ptr [rip + 0x1b9551c], xmm1  ; -> 02064B44
004CF628  movups   xmmword ptr [rip + 0x1b95581], xmm0  ; -> 02064BB0
004CF62F  mulss    xmm4, xmm3
004CF633  movss    xmm0, dword ptr [rip + 0x19331f9]  ; -> 01E02834 [u32 0x00000000]
004CF63B  addss    xmm0, xmm1
004CF63F  movss    dword ptr [rip + 0x1b95501], xmm4  ; -> 02064B48
004CF647  movss    xmm1, dword ptr [rip + 0x19331e1]  ; -> 01E02830 [u32 0x00000000]
004CF64F  subss    xmm1, xmm2
004CF653  movss    dword ptr [rip + 0x1b95649], xmm0  ; -> 02064CA4
004CF65B  movss    xmm0, dword ptr [rip + 0x19331d9]  ; -> 01E0283C [f32 1]
004CF663  movss    dword ptr [rip + 0x1b956b1], xmm0  ; -> 02064D1C
004CF66B  movss    xmm0, dword ptr [rip + 0x19331c5]  ; -> 01E02838 [u32 0x00000000]
004CF673  subss    xmm0, xmm4
004CF677  movss    dword ptr [rip + 0x1b95621], xmm1  ; -> 02064CA0
004CF67F  movss    dword ptr [rip + 0x1b95621], xmm0  ; -> 02064CA8
004CF687  call     0x22cc20  ; -> 0022CC20 fn
004CF68C  movss    xmm1, dword ptr [rip + 0x19331a4]  ; -> 01E02838 [u32 0x00000000]
004CF694  addss    xmm1, dword ptr [rip + 0x1b954ac]  ; -> 02064B48
004CF69C  movss    xmm0, dword ptr [rip + 0x1933190]  ; -> 01E02834 [u32 0x00000000]
004CF6A4  addss    xmm0, dword ptr [rip + 0x1b95498]  ; -> 02064B44
004CF6AC  movss    dword ptr [rip + 0x1b95604], xmm1  ; -> 02064CB8
004CF6B4  movss    xmm1, dword ptr [rip + 0x1933174]  ; -> 01E02830 [u32 0x00000000]
004CF6BC  subss    xmm1, dword ptr [rip + 0x1b9547c]  ; -> 02064B40
004CF6C4  movss    dword ptr [rip + 0x1b955e8], xmm0  ; -> 02064CB4
004CF6CC  movss    xmm0, dword ptr [rip + 0x1933168]  ; -> 01E0283C [f32 1]
004CF6D4  movss    dword ptr [rip + 0x1b95630], xmm0  ; -> 02064D0C
004CF6DC  movss    dword ptr [rip + 0x1b955cc], xmm1  ; -> 02064CB0
004CF6E4  call     0x22cc20  ; -> 0022CC20 fn
004CF6E9  movss    xmm4, dword ptr [rip + 0x1933147]  ; -> 01E02838 [u32 0x00000000]
004CF6F1  movss    xmm1, dword ptr [rip + 0x1933143]  ; -> 01E0283C [f32 1]
004CF6F9  movaps   xmm0, xmm4
004CF6FC  movss    xmm5, dword ptr [rip + 0x193312c]  ; -> 01E02830 [u32 0x00000000]
004CF704  addss    xmm5, dword ptr [rip + 0x1b95434]  ; -> 02064B40
004CF70C  movss    xmm3, dword ptr [rip + 0x1933120]  ; -> 01E02834 [u32 0x00000000]
004CF714  addss    xmm3, dword ptr [rip + 0x1b95428]  ; -> 02064B44
004CF71C  addss    xmm0, dword ptr [rip + 0x1b95424]  ; -> 02064B48
004CF724  subss    xmm4, dword ptr [rip + 0x1b9541c]  ; -> 02064B48
004CF72C  movss    dword ptr [rip + 0x1b9558c], xmm5  ; -> 02064CC0
004CF734  movss    dword ptr [rip + 0x1b955c0], xmm1  ; -> 02064CFC
004CF73C  movss    dword ptr [rip + 0x1b95580], xmm3  ; -> 02064CC4
004CF744  movss    dword ptr [rip + 0x1b9557c], xmm0  ; -> 02064CC8
004CF74C  movss    dword ptr [rip + 0x1b9557c], xmm5  ; -> 02064CD0
004CF754  movss    dword ptr [rip + 0x1b95578], xmm3  ; -> 02064CD4
004CF75C  movss    dword ptr [rip + 0x1b95588], xmm1  ; -> 02064CEC
004CF764  movss    dword ptr [rip + 0x1b9556c], xmm4  ; -> 02064CD8
004CF76C  call     0x22cc20  ; -> 0022CC20 fn
004CF771  movss    xmm0, dword ptr [rip + 0x19330b7]  ; -> 01E02830 [u32 0x00000000]
004CF779  subss    xmm0, dword ptr [rip + 0x1b953bf]  ; -> 02064B40
004CF781  movss    xmm1, dword ptr [rip + 0x19330ab]  ; -> 01E02834 [u32 0x00000000]
004CF789  subss    xmm1, dword ptr [rip + 0x1b953b3]  ; -> 02064B44
004CF791  movss    dword ptr [rip + 0x1b95547], xmm0  ; -> 02064CE0
004CF799  movss    xmm0, dword ptr [rip + 0x1933097]  ; -> 01E02838 [u32 0x00000000]
004CF7A1  subss    xmm0, dword ptr [rip + 0x1b9539f]  ; -> 02064B48
004CF7A9  movss    dword ptr [rip + 0x1b95533], xmm1  ; -> 02064CE4
004CF7B1  movss    dword ptr [rip + 0x1b9552f], xmm0  ; -> 02064CE8
004CF7B9  call     0x22cc20  ; -> 0022CC20 fn
004CF7BE  movss    xmm0, dword ptr [rip + 0x1933072]  ; -> 01E02838 [u32 0x00000000]
004CF7C6  xorps    xmm8, xmm8
004CF7CA  addss    xmm0, dword ptr [rip + 0x1b95376]  ; -> 02064B48
004CF7D2  movss    xmm1, dword ptr [rip + 0x1933062]  ; -> 01E0283C [f32 1]
004CF7DA  movss    xmm2, dword ptr [rip + 0x193304e]  ; -> 01E02830 [u32 0x00000000]
004CF7E2  subss    xmm2, dword ptr [rip + 0x1b95356]  ; -> 02064B40
004CF7EA  movss    dword ptr [rip + 0x1b954ea], xmm1  ; -> 02064CDC
004CF7F2  movss    dword ptr [rip + 0x1b954fe], xmm0  ; -> 02064CF8
004CF7FA  movss    xmm0, dword ptr [rip + 0x1933032]  ; -> 01E02834 [u32 0x00000000]
004CF802  subss    xmm0, dword ptr [rip + 0x1b9533a]  ; -> 02064B44
004CF80A  ucomiss  xmm2, xmm8
004CF80E  movss    dword ptr [rip + 0x1b954de], xmm0  ; -> 02064CF4
004CF816  movss    dword ptr [rip + 0x1b9548e], xmm1  ; -> 02064CAC
004CF81E  movss    dword ptr [rip + 0x1b954ca], xmm2  ; -> 02064CF0
004CF826  jp       0x4cf82a  ; -> 004CF82A
004CF828  je       0x4cf832  ; -> 004CF832
004CF82A  ucomiss  xmm0, xmm8
004CF82E  jp       0x4cf847  ; -> 004CF847
004CF830  jne      0x4cf847  ; -> 004CF847
004CF832  call     0x22cc40  ; -> 0022CC40 fn
004CF837  movss    xmm0, dword ptr [rip + 0x1b954b5]  ; -> 02064CF4
004CF83F  movss    xmm2, dword ptr [rip + 0x1b954a9]  ; -> 02064CF0
004CF847  comiss   xmm8, xmm2
004CF84B  ja       0x4cf853  ; -> 004CF853
004CF84D  comiss   xmm8, xmm0
004CF851  jbe      0x4cf858  ; -> 004CF858
004CF853  call     0x22cc30  ; -> 0022CC30 fn
004CF858  call     0x22cc20  ; -> 0022CC20 fn
004CF85D  movss    xmm1, dword ptr [rip + 0x1932fd3]  ; -> 01E02838 [u32 0x00000000]
004CF865  addss    xmm1, dword ptr [rip + 0x1b952db]  ; -> 02064B48
004CF86D  movss    xmm0, dword ptr [rip + 0x1932fbb]  ; -> 01E02830 [u32 0x00000000]
004CF875  addss    xmm0, dword ptr [rip + 0x1b952c3]  ; -> 02064B40
004CF87D  movss    dword ptr [rip + 0x1b95483], xmm1  ; -> 02064D08
004CF885  movss    xmm1, dword ptr [rip + 0x1932fa7]  ; -> 01E02834 [u32 0x00000000]
004CF88D  subss    xmm1, dword ptr [rip + 0x1b952af]  ; -> 02064B44
004CF895  movss    dword ptr [rip + 0x1b95463], xmm0  ; -> 02064D00
004CF89D  movss    xmm0, dword ptr [rip + 0x1932f97]  ; -> 01E0283C [f32 1]
004CF8A5  movss    dword ptr [rip + 0x1b9540f], xmm0  ; -> 02064CBC
004CF8AD  movss    dword ptr [rip + 0x1b9544f], xmm1  ; -> 02064D04
004CF8B5  call     0x22cc20  ; -> 0022CC20 fn
004CF8BA  movss    xmm0, dword ptr [rip + 0x1932f6e]  ; -> 01E02830 [u32 0x00000000]
004CF8C2  addss    xmm0, dword ptr [rip + 0x1b95276]  ; -> 02064B40
004CF8CA  movss    xmm1, dword ptr [rip + 0x1932f62]  ; -> 01E02834 [u32 0x00000000]
004CF8D2  subss    xmm1, dword ptr [rip + 0x1b9526a]  ; -> 02064B44
004CF8DA  movss    dword ptr [rip + 0x1b9542e], xmm0  ; -> 02064D10
004CF8E2  movss    xmm0, dword ptr [rip + 0x1932f52]  ; -> 01E0283C [f32 1]
004CF8EA  movss    dword ptr [rip + 0x1b953da], xmm0  ; -> 02064CCC
004CF8F2  movss    xmm0, dword ptr [rip + 0x1932f3e]  ; -> 01E02838 [u32 0x00000000]
004CF8FA  subss    xmm0, dword ptr [rip + 0x1b95246]  ; -> 02064B48
004CF902  movss    dword ptr [rip + 0x1b9540a], xmm1  ; -> 02064D14
004CF90A  movss    dword ptr [rip + 0x1b95406], xmm0  ; -> 02064D18
004CF912  call     0x22cc20  ; -> 0022CC20 fn
004CF917  movsx    edi, word ptr [rip + 0x1b9549e]  ; -> 02064DBC
004CF91E  mov      r12d, 0xe0
004CF924  movups   xmm0, xmmword ptr [rip + 0x1b95375]  ; -> 02064CA0
004CF92B  movzx    r15d, word ptr [rip + 0x1b951d9]  ; -> 02064B0C
004CF933  mov      ecx, edi
004CF935  movss    xmm10, dword ptr [rip + 0x1b951fa]  ; -> 02064B38
004CF93E  movss    xmm9, dword ptr [rip + 0x1b951ed]  ; -> 02064B34
004CF947  movss    xmm11, dword ptr [rip + 0x1b951e0]  ; -> 02064B30
004CF950  movss    xmm13, dword ptr [rip + 0x1932edf]  ; -> 01E02838 [u32 0x00000000]
004CF959  lea      r14d, [r15 + 4]
004CF95D  movss    xmm12, dword ptr [rip + 0x1932ece]  ; -> 01E02834 [u32 0x00000000]
004CF966  movss    xmm14, dword ptr [rip + 0x1932ec1]  ; -> 01E02830 [u32 0x00000000]
004CF96F  movss    xmm15, dword ptr [rip + 0x4309e8]  ; -> 00900360 [u32 0x7F7FFFFF]
004CF978  shl      ecx, 4
004CF97B  movsxd   rax, ecx
004CF97E  movups   xmmword ptr [rax + rbx], xmm0
004CF982  lea      eax, [rcx + 0x10]
004CF985  movups   xmm0, xmmword ptr [rip + 0x1b95324]  ; -> 02064CB0
004CF98C  movsxd   rcx, eax
004CF98F  lea      eax, [rdi + 2]
004CF992  shl      eax, 4
004CF995  movups   xmmword ptr [rcx + rbx], xmm0
004CF999  movsxd   rcx, eax
004CF99C  lea      eax, [rdi + 3]
004CF99F  movups   xmm0, xmmword ptr [rip + 0x1b9531a]  ; -> 02064CC0
004CF9A6  shl      eax, 4
004CF9A9  movups   xmmword ptr [rcx + rbx], xmm0
004CF9AD  movsxd   rcx, eax
004CF9B0  lea      eax, [rdi + 4]
004CF9B3  movups   xmm0, xmmword ptr [rip + 0x1b95316]  ; -> 02064CD0
004CF9BA  shl      eax, 4
004CF9BD  movups   xmmword ptr [rcx + rbx], xmm0
004CF9C1  movsxd   rcx, eax
004CF9C4  lea      eax, [rdi + 5]
004CF9C7  movups   xmm0, xmmword ptr [rip + 0x1b95312]  ; -> 02064CE0
004CF9CE  shl      eax, 4
004CF9D1  movups   xmmword ptr [rcx + rbx], xmm0
004CF9D5  movsxd   rcx, eax
004CF9D8  lea      eax, [rdi + 6]
004CF9DB  movups   xmm0, xmmword ptr [rip + 0x1b9530e]  ; -> 02064CF0
004CF9E2  shl      eax, 4
004CF9E5  movups   xmmword ptr [rcx + rbx], xmm0
004CF9E9  movsxd   rcx, eax
004CF9EC  lea      eax, [rdi + 7]
004CF9EF  movups   xmm0, xmmword ptr [rip + 0x1b9530a]  ; -> 02064D00
004CF9F6  shl      eax, 4
004CF9F9  add      di, r15w
004CF9FD  add      r12d, r15d
004CFA00  movups   xmmword ptr [rcx + rbx], xmm0
004CFA04  movsxd   rcx, eax
004CFA07  movups   xmm0, xmmword ptr [rip + 0x1b95302]  ; -> 02064D10
004CFA0E  movups   xmmword ptr [rcx + rbx], xmm0
004CFA12  nop      dword ptr [rax]
004CFA16  nop      word ptr [rax + rax]
004CFA20  movss    xmm1, dword ptr [rip + 0x1b95150]  ; -> 02064B78
004CFA28  dec      r14w
004CFA2C  movsx    eax, di
004CFA2F  shl      eax, 4
004CFA32  movsxd   rsi, eax
004CFA35  add      eax, 0x10
004CFA38  movsxd   rbp, eax
004CFA3B  movups   xmm7, xmmword ptr [rsi + rbx]
004CFA3F  movups   xmm0, xmmword ptr [rbx + rbp]
004CFA43  movups   xmmword ptr [rip + 0x1b95266], xmm7  ; -> 02064CB0
004CFA4A  movups   xmmword ptr [rip + 0x1b9526f], xmm0  ; -> 02064CC0
004CFA51  movups   xmm0, xmmword ptr [rip + 0x1b95108]  ; -> 02064B60
004CFA58  movaps   xmm6, xmm7
004CFA5B  movaps   xmm2, xmm7
004CFA5E  shufps   xmm2, xmm7, 0x55
004CFA62  mulss    xmm1, xmm2
004CFA66  shufps   xmm6, xmm6, 0
004CFA6A  mulps    xmm6, xmm0
004CFA6D  movss    xmm0, dword ptr [rip + 0x1b950fb]  ; -> 02064B70
004CFA75  mulss    xmm0, xmm2
004CFA79  movups   xmmword ptr [rip + 0x1b950a0], xmm6  ; -> 02064B20
004CFA80  movss    xmm3, dword ptr [rip + 0x1b9509c]  ; -> 02064B24
004CFA88  addss    xmm6, xmm0
004CFA8C  movss    xmm0, dword ptr [rip + 0x1b950e0]  ; -> 02064B74
004CFA94  movss    xmm4, dword ptr [rip + 0x1b9508c]  ; -> 02064B28
004CFA9C  movss    xmm5, dword ptr [rip + 0x1b95088]  ; -> 02064B2C
004CFAA4  addss    xmm4, xmm1
004CFAA8  movss    xmm1, dword ptr [rip + 0x1b950d0]  ; -> 02064B80
004CFAB0  mulss    xmm0, xmm2
004CFAB4  addss    xmm3, xmm0
004CFAB8  movss    xmm0, dword ptr [rip + 0x1b950bc]  ; -> 02064B7C
004CFAC0  mulss    xmm0, xmm2
004CFAC4  movaps   xmm2, xmm7
004CFAC7  shufps   xmm2, xmm7, 0xaa
004CFACB  mulss    xmm1, xmm2
004CFACF  addss    xmm5, xmm0
004CFAD3  shufps   xmm7, xmm7, 0xff
004CFAD7  movss    xmm0, dword ptr [rip + 0x1b950a5]  ; -> 02064B84
004CFADF  mulss    xmm0, xmm2
004CFAE3  addss    xmm6, xmm1
004CFAE7  movss    xmm1, dword ptr [rip + 0x1b95099]  ; -> 02064B88
004CFAEF  mulss    xmm1, xmm2
004CFAF3  addss    xmm3, xmm0
004CFAF7  movss    xmm0, dword ptr [rip + 0x1b9508d]  ; -> 02064B8C
004CFAFF  mulss    xmm0, xmm2
004CFB03  movss    xmm2, dword ptr [rip + 0x1b95091]  ; -> 02064B9C
004CFB0B  addss    xmm4, xmm1
004CFB0F  movss    xmm1, dword ptr [rip + 0x1b95079]  ; -> 02064B90
004CFB17  mulss    xmm1, xmm7
004CFB1B  addss    xmm5, xmm0
004CFB1F  movss    xmm0, dword ptr [rip + 0x1b9506d]  ; -> 02064B94
004CFB27  mulss    xmm2, xmm7
004CFB2B  addss    xmm1, xmm6
004CFB2F  mulss    xmm0, xmm7
004CFB33  addss    xmm2, xmm5
004CFB37  addss    xmm0, xmm3
004CFB3B  movss    dword ptr [rip + 0x1b9516d], xmm1  ; -> 02064CB0
004CFB43  movss    xmm1, dword ptr [rip + 0x1b9504d]  ; -> 02064B98
004CFB4B  ucomiss  xmm2, xmm8
004CFB4F  mulss    xmm1, xmm7
004CFB53  movss    dword ptr [rip + 0x1b95159], xmm0  ; -> 02064CB4
004CFB5B  movss    dword ptr [rip + 0x1b95159], xmm2  ; -> 02064CBC
004CFB63  addss    xmm1, xmm4
004CFB67  movss    dword ptr [rip + 0x1b95149], xmm1  ; -> 02064CB8
004CFB6F  jp       0x4cfb81  ; -> 004CFB81
004CFB71  jne      0x4cfb81  ; -> 004CFB81
004CFB73  movss    xmm7, dword ptr [rip + 0x1932cc1]  ; -> 01E0283C [f32 1]
004CFB7B  movaps   xmm0, xmm15
004CFB7F  jmp      0x4cfb90  ; -> 004CFB90
004CFB81  movss    xmm7, dword ptr [rip + 0x1932cb3]  ; -> 01E0283C [f32 1]
004CFB89  movaps   xmm0, xmm7
004CFB8C  divss    xmm0, xmm2
004CFB90  movss    xmm2, dword ptr [rip + 0x1b9512c]  ; -> 02064CC4
004CFB98  movups   xmm1, xmmword ptr [rip + 0x1b95111]  ; -> 02064CB0
004CFB9F  movss    xmm6, dword ptr [rip + 0x1b95119]  ; -> 02064CC0
004CFBA7  shufps   xmm0, xmm0, 0
004CFBAB  mulps    xmm1, xmm0
004CFBAE  movups   xmm0, xmmword ptr [rip + 0x1b94fab]  ; -> 02064B60
004CFBB5  shufps   xmm6, xmm6, 0
004CFBB9  mulps    xmm6, xmm0
004CFBBC  movss    xmm0, dword ptr [rip + 0x1b94fac]  ; -> 02064B70
004CFBC4  mulss    xmm0, xmm2
004CFBC8  movups   xmmword ptr [rip + 0x1b950e1], xmm1  ; -> 02064CB0
004CFBCF  movss    xmm1, dword ptr [rip + 0x1b94fa1]  ; -> 02064B78
004CFBD7  mulss    xmm1, xmm2
004CFBDB  movups   xmmword ptr [rip + 0x1b94f3e], xmm6  ; -> 02064B20
004CFBE2  movss    xmm3, dword ptr [rip + 0x1b94f3a]  ; -> 02064B24
004CFBEA  addss    xmm6, xmm0
004CFBEE  movss    xmm0, dword ptr [rip + 0x1b94f7e]  ; -> 02064B74
004CFBF6  movss    xmm4, dword ptr [rip + 0x1b94f2a]  ; -> 02064B28
004CFBFE  movss    xmm5, dword ptr [rip + 0x1b94f26]  ; -> 02064B2C
004CFC06  addss    xmm4, xmm1
004CFC0A  movss    xmm1, dword ptr [rip + 0x1b94f6e]  ; -> 02064B80
004CFC12  mulss    xmm0, xmm2
004CFC16  addss    xmm3, xmm0
004CFC1A  movss    xmm0, dword ptr [rip + 0x1b94f5a]  ; -> 02064B7C
004CFC22  mulss    xmm0, xmm2
004CFC26  movss    xmm2, dword ptr [rip + 0x1b9509a]  ; -> 02064CC8
004CFC2E  mulss    xmm1, xmm2
004CFC32  addss    xmm5, xmm0
004CFC36  movss    xmm0, dword ptr [rip + 0x1b94f46]  ; -> 02064B84
004CFC3E  mulss    xmm0, xmm2
004CFC42  addss    xmm6, xmm1
004CFC46  movss    xmm1, dword ptr [rip + 0x1b94f3a]  ; -> 02064B88
004CFC4E  mulss    xmm1, xmm2
004CFC52  addss    xmm3, xmm0
004CFC56  movss    xmm0, dword ptr [rip + 0x1b94f2e]  ; -> 02064B8C
004CFC5E  mulss    xmm0, xmm2
004CFC62  movss    xmm2, dword ptr [rip + 0x1b95062]  ; -> 02064CCC
004CFC6A  addss    xmm4, xmm1
004CFC6E  movss    xmm1, dword ptr [rip + 0x1b94f1a]  ; -> 02064B90
004CFC76  addss    xmm5, xmm0
004CFC7A  mulss    xmm1, xmm2
004CFC7E  movss    xmm0, dword ptr [rip + 0x1b94f0e]  ; -> 02064B94
004CFC86  movss    dword ptr [rip + 0x1b94e96], xmm3  ; -> 02064B24
004CFC8E  addss    xmm1, xmm6
004CFC92  mulss    xmm0, xmm2
004CFC96  movss    dword ptr [rip + 0x1b94e82], xmm6  ; -> 02064B20
004CFC9E  movss    dword ptr [rip + 0x1b94e82], xmm4  ; -> 02064B28
004CFCA6  addss    xmm0, xmm3
004CFCAA  movss    dword ptr [rip + 0x1b94e7a], xmm5  ; -> 02064B2C
004CFCB2  movss    xmm3, dword ptr [rip + 0x1b94ee2]  ; -> 02064B9C
004CFCBA  movss    dword ptr [rip + 0x1b94ffe], xmm1  ; -> 02064CC0
004CFCC2  movss    xmm1, dword ptr [rip + 0x1b94ece]  ; -> 02064B98
004CFCCA  mulss    xmm3, xmm2
004CFCCE  mulss    xmm1, xmm2
004CFCD2  addss    xmm3, xmm5
004CFCD6  movss    dword ptr [rip + 0x1b94fe6], xmm0  ; -> 02064CC4
004CFCDE  addss    xmm1, xmm4
004CFCE2  ucomiss  xmm3, xmm8
004CFCE6  movss    dword ptr [rip + 0x1b94fda], xmm1  ; -> 02064CC8
004CFCEE  movss    dword ptr [rip + 0x1b94fd6], xmm3  ; -> 02064CCC
004CFCF6  jp       0x4cfd00  ; -> 004CFD00
004CFCF8  jne      0x4cfd00  ; -> 004CFD00
004CFCFA  movaps   xmm0, xmm15
004CFCFE  jmp      0x4cfd07  ; -> 004CFD07
004CFD00  movaps   xmm0, xmm7
004CFD03  divss    xmm0, xmm3
004CFD07  movups   xmm1, xmmword ptr [rip + 0x1b94fb2]  ; -> 02064CC0
004CFD0E  movss    xmm4, dword ptr [rip + 0x1b94f9a]  ; -> 02064CB0
004CFD16  ucomiss  xmm11, xmm4
004CFD1A  movss    dword ptr [rip + 0x1b94dde], xmm0  ; -> 02064B00
004CFD22  shufps   xmm0, xmm0, 0
004CFD26  mulps    xmm1, xmm0
004CFD29  movups   xmmword ptr [rip + 0x1b94f90], xmm1  ; -> 02064CC0
004CFD30  jp       0x4cfd3c  ; -> 004CFD3C
004CFD32  jne      0x4cfd3c  ; -> 004CFD3C
004CFD34  mov      r9d, 1
004CFD3A  jmp      0x4cfd3f  ; -> 004CFD3F
004CFD3C  xor      r9d, r9d
004CFD3F  movss    xmm1, dword ptr [rip + 0x1b94f6d]  ; -> 02064CB4
004CFD47  ucomiss  xmm9, xmm1
004CFD4B  jp       0x4cfd56  ; -> 004CFD56
004CFD4D  jne      0x4cfd56  ; -> 004CFD56
004CFD4F  mov      edx, 1
004CFD54  jmp      0x4cfd58  ; -> 004CFD58
004CFD56  xor      edx, edx
004CFD58  movss    xmm0, dword ptr [rip + 0x1b94f58]  ; -> 02064CB8
004CFD60  ucomiss  xmm10, xmm0
004CFD64  jp       0x4cfd6f  ; -> 004CFD6F
004CFD66  jne      0x4cfd6f  ; -> 004CFD6F
004CFD68  mov      ecx, 1
004CFD6D  jmp      0x4cfd71  ; -> 004CFD71
004CFD6F  xor      ecx, ecx
004CFD71  movss    xmm5, dword ptr [rip + 0x1b94f47]  ; -> 02064CC0
004CFD79  xor      r8d, r8d
004CFD7C  comiss   xmm4, xmm11
004CFD80  seta     r8b
004CFD84  xor      eax, eax
004CFD86  add      r8w, r8w
004CFD8A  comiss   xmm1, xmm9
004CFD8E  seta     al
004CFD91  add      r8w, ax
004CFD95  xor      eax, eax
004CFD97  add      r8w, r8w
004CFD9B  comiss   xmm0, xmm10
004CFD9F  seta     al
004CFDA2  add      r8w, ax
004CFDA6  shl      r8w, 2
004CFDAB  add      r8w, r9w
004CFDAF  add      r8w, r8w
004CFDB3  add      r8w, dx
004CFDB7  add      r8w, r8w
004CFDBB  add      r8w, cx
004CFDBF  add      r8w, r8w
004CFDC3  ucomiss  xmm11, xmm5
004CFDC7  mov      word ptr [rip + 0x1b94d41], r8w  ; -> 02064B10
004CFDCF  jp       0x4cfddb  ; -> 004CFDDB
004CFDD1  jne      0x4cfddb  ; -> 004CFDDB
004CFDD3  mov      r10d, 1
004CFDD9  jmp      0x4cfdde  ; -> 004CFDDE
004CFDDB  xor      r10d, r10d
004CFDDE  movss    xmm2, dword ptr [rip + 0x1b94ede]  ; -> 02064CC4
004CFDE6  ucomiss  xmm9, xmm2
004CFDEA  jp       0x4cfdf5  ; -> 004CFDF5
004CFDEC  jne      0x4cfdf5  ; -> 004CFDF5
004CFDEE  mov      edx, 1
004CFDF3  jmp      0x4cfdf7  ; -> 004CFDF7
004CFDF5  xor      edx, edx
004CFDF7  movss    xmm3, dword ptr [rip + 0x1b94ec9]  ; -> 02064CC8
004CFDFF  ucomiss  xmm10, xmm3
004CFE03  jp       0x4cfe0e  ; -> 004CFE0E
004CFE05  jne      0x4cfe0e  ; -> 004CFE0E
004CFE07  mov      ecx, 1
004CFE0C  jmp      0x4cfe10  ; -> 004CFE10
004CFE0E  xor      ecx, ecx
004CFE10  xor      r9d, r9d
004CFE13  comiss   xmm5, xmm11
004CFE17  seta     r9b
004CFE1B  xor      eax, eax
004CFE1D  add      r9w, r9w
004CFE21  comiss   xmm2, xmm9
004CFE25  seta     al
004CFE28  add      r9w, ax
004CFE2C  xor      eax, eax
004CFE2E  add      r9w, r9w
004CFE32  comiss   xmm3, xmm10
004CFE36  seta     al
004CFE39  add      r9w, ax
004CFE3D  shl      r9w, 2
004CFE42  add      r9w, r10w
004CFE46  add      r9w, r9w
004CFE4A  add      r9w, dx
004CFE4E  add      r9w, r9w
004CFE52  add      r9w, cx
004CFE56  add      r9w, r9w
004CFE5A  ucomiss  xmm4, xmm14
004CFE5E  mov      word ptr [rip + 0x1b94cac], r9w  ; -> 02064B12
004CFE66  jp       0x4cfe72  ; -> 004CFE72
004CFE68  jne      0x4cfe72  ; -> 004CFE72
004CFE6A  mov      r11d, 1
004CFE70  jmp      0x4cfe75  ; -> 004CFE75
004CFE72  xor      r11d, r11d
004CFE75  ucomiss  xmm1, xmm12
004CFE79  jp       0x4cfe84  ; -> 004CFE84
004CFE7B  jne      0x4cfe84  ; -> 004CFE84
004CFE7D  mov      edx, 1
004CFE82  jmp      0x4cfe86  ; -> 004CFE86
004CFE84  xor      edx, edx
004CFE86  ucomiss  xmm0, xmm13
004CFE8A  jp       0x4cfe95  ; -> 004CFE95
004CFE8C  jne      0x4cfe95  ; -> 004CFE95
004CFE8E  mov      ecx, 1
004CFE93  jmp      0x4cfe97  ; -> 004CFE97
004CFE95  xor      ecx, ecx
004CFE97  xor      r10d, r10d
004CFE9A  comiss   xmm14, xmm4
004CFE9E  seta     r10b
004CFEA2  xor      eax, eax
004CFEA4  add      r10w, r10w
004CFEA8  comiss   xmm12, xmm1
004CFEAC  seta     al
004CFEAF  add      r10w, ax
004CFEB3  xor      eax, eax
004CFEB5  add      r10w, r10w
004CFEB9  comiss   xmm13, xmm0
004CFEBD  seta     al
004CFEC0  add      r10w, ax
004CFEC4  shl      r10w, 2
004CFEC9  add      r10w, r11w
004CFECD  add      r10w, r10w
004CFED1  add      r10w, dx
004CFED5  add      r10w, r10w
004CFED9  add      r10w, cx
004CFEDD  add      r10w, r10w
004CFEE1  ucomiss  xmm5, xmm14
004CFEE5  mov      word ptr [rip + 0x1b94c27], r10w  ; -> 02064B14
004CFEED  jp       0x4cfef8  ; -> 004CFEF8
004CFEEF  jne      0x4cfef8  ; -> 004CFEF8
004CFEF1  mov      ebx, 1
004CFEF6  jmp      0x4cfefa  ; -> 004CFEFA
004CFEF8  xor      ebx, ebx
004CFEFA  ucomiss  xmm2, xmm12
004CFEFE  jp       0x4cff0a  ; -> 004CFF0A
004CFF00  jne      0x4cff0a  ; -> 004CFF0A
004CFF02  mov      r11d, 1
004CFF08  jmp      0x4cff0d  ; -> 004CFF0D
004CFF0A  xor      r11d, r11d
004CFF0D  ucomiss  xmm3, xmm13
004CFF11  jp       0x4cff1c  ; -> 004CFF1C
004CFF13  jne      0x4cff1c  ; -> 004CFF1C
004CFF15  mov      ecx, 1
004CFF1A  jmp      0x4cff1e  ; -> 004CFF1E
004CFF1C  xor      ecx, ecx
004CFF1E  movsd    xmm0, qword ptr [rip + 0x1b94d8a]  ; -> 02064CB0
004CFF26  xor      edx, edx
004CFF28  comiss   xmm14, xmm5
004CFF2C  seta     dl
004CFF2F  xor      eax, eax
004CFF31  add      dx, dx
004CFF34  comiss   xmm12, xmm2
004CFF38  seta     al
004CFF3B  add      dx, ax
004CFF3E  xor      eax, eax
004CFF40  add      dx, dx
004CFF43  comiss   xmm13, xmm3
004CFF47  seta     al
004CFF4A  and      r10w, r12w
004CFF4E  add      dx, ax
004CFF51  mov      word ptr [rip + 0x1b94e87], r10w  ; -> 02064DE0
004CFF59  shl      dx, 2
004CFF5D  and      r8w, r12w
004CFF61  add      dx, bx
004CFF64  movsx    eax, r10w
004CFF68  or       r8w, ax
004CFF6C  lea      rbx, [rip + 0x1b94ebd]  ; -> 02064E30
004CFF73  movsd    qword ptr [rsi + rbx], xmm0
004CFF78  add      dx, dx
004CFF7B  add      dx, r11w
004CFF7F  mov      word ptr [rip + 0x1b94e51], r8w  ; -> 02064DD8
004CFF87  add      dx, dx
004CFF8A  and      r9w, r12w
004CFF8E  add      dx, cx
004CFF91  add      di, 2
004CFF95  add      dx, dx
004CFF98  mov      word ptr [rip + 0x1b94e29], di  ; -> 02064DC8
004CFF9F  movzx    ecx, r12w
004CFFA3  mov      word ptr [rip + 0x1b94b6c], dx  ; -> 02064B16
004CFFAA  and      cx, dx
004CFFAD  movaps   xmm0, xmm5
004CFFB0  movsx    eax, cx
004CFFB3  or       r9w, ax
004CFFB7  unpcklps xmm0, xmm2
004CFFBA  mov      eax, dword ptr [rip + 0x1b94cf8]  ; -> 02064CB8
004CFFC0  mov      dword ptr [rsi + rbx + 8], eax
004CFFC4  mov      eax, dword ptr [rip + 0x1b94cfe]  ; -> 02064CC8
004CFFCA  movsd    qword ptr [rbx + rbp], xmm0
004CFFCF  mov      dword ptr [rbx + rbp + 8], eax
004CFFD3  movzx    eax, r8w
004CFFD7  mov      dword ptr [rsi + rbx + 0xc], eax
004CFFDB  movzx    eax, r9w
004CFFDF  mov      dword ptr [rbx + rbp + 0xc], eax
004CFFE3  mov      word ptr [rip + 0x1b94dfa], cx  ; -> 02064DE4
004CFFEA  mov      word ptr [rip + 0x1b94dea], r9w  ; -> 02064DDC
004CFFF2  movsd    qword ptr [rip + 0x1b94cc6], xmm0  ; -> 02064CC0
004CFFFA  cmp      r14w, r15w
004CFFFE  jne      0x4cfa20  ; -> 004CFA20
004D0004  mov      rsi, qword ptr [rsp + 0x20]
004D0009  lea      rbp, [rip + 0x1b94e20]  ; -> 02064E30
004D0010  add      r15w, 0x10
004D0015  mov      word ptr [rip + 0x1b94da7], r14w  ; -> 02064DC4
004D001D  movsx    eax, r15w
004D0021  xor      r8d, r8d
004D0024  shl      eax, 4
004D0027  mov      rdx, rsi
004D002A  movsxd   rcx, eax
004D002D  add      rcx, rbp
004D0030  mov      word ptr [rip + 0x1b94d9c], r15w  ; -> 02064DD4
004D0038  call     r13
004D003B  movsx    r11d, word ptr [rip + 0x1b94ac9]  ; -> 02064B0C
004D0043  mov      r14d, 4
004D0049  mov      ebx, r11d
004D004C  add      bx, r11w
004D0050  mov      word ptr [rip + 0x1b94d71], bx  ; -> 02064DC8
004D0057  lea      edi, [r11 + 6]
004D005B  lea      r15d, [r14 + 4]
004D005F  lea      r12d, [r14 + 0xc]
004D0063  nop      dword ptr [rax]
004D0067  nop      word ptr [rax + rax]
004D0070  movsx    eax, bx
004D0073  dec      di
004D0076  add      eax, 0xa
004D0079  mov      word ptr [rip + 0x1b94d44], di  ; -> 02064DC4
004D0080  shl      eax, 4
004D0083  movsxd   rcx, eax
004D0086  movsx    r8d, word ptr [rcx + rbp + 0xc]
004D008C  movsx    eax, word ptr [rcx + rbp]
004D0090  add      eax, 0x64
004D0093  mov      word ptr [rip + 0x1b94d49], r8w  ; -> 02064DE4
004D009B  shl      eax, 4
004D009E  movsxd   r9, eax
004D00A1  movsx    eax, word ptr [rcx + rbp + 4]
004D00A6  add      eax, 0x64
004D00A9  shl      eax, 4
004D00AC  movups   xmm0, xmmword ptr [r9 + rbp]
004D00B1  movzx    r9d, word ptr [r9 + rbp + 0xc]
004D00B7  movsxd   r10, eax
004D00BA  movsx    eax, word ptr [rcx + rbp + 8]
004D00BF  add      eax, 0x64
004D00C2  shl      eax, 4
004D00C5  movsx    ecx, word ptr [r10 + rbp + 0xc]
004D00CB  movsxd   rdx, eax
004D00CE  lea      eax, [r8 + 0x64]
004D00D2  shl      eax, 4
004D00D5  movsxd   r8, eax
004D00D8  movups   xmmword ptr [rip + 0x1b94bd1], xmm0  ; -> 02064CB0
004D00DF  mov      word ptr [rip + 0x1b94cf2], cx  ; -> 02064DD8
004D00E6  movups   xmm0, xmmword ptr [r10 + rbp]
004D00EB  movsx    eax, word ptr [r8 + rbp + 0xc]
004D00F1  mov      word ptr [rip + 0x1b94ce8], ax  ; -> 02064DE0
004D00F8  movups   xmmword ptr [rip + 0x1b94bc1], xmm0  ; -> 02064CC0
004D00FF  movups   xmm0, xmmword ptr [rdx + rbp]
004D0103  movzx    edx, word ptr [rdx + rbp + 0xc]
004D0108  or       dx, ax
004D010B  movsx    eax, dx
004D010E  or       ax, cx
004D0111  mov      word ptr [rip + 0x1b94cc4], dx  ; -> 02064DDC
004D0118  or       r9w, ax
004D011C  mov      word ptr [rip + 0x1b94cb0], r9w  ; -> 02064DD4
004D0124  movups   xmmword ptr [rip + 0x1b94ba5], xmm0  ; -> 02064CD0
004D012B  movups   xmm0, xmmword ptr [r8 + rbp]
004D0130  movups   xmmword ptr [rip + 0x1b94ba9], xmm0  ; -> 02064CE0
004D0137  cmp      r9w, r11w
004D013B  jne      0x4d0418  ; -> 004D0418
004D0141  movss    xmm1, dword ptr [rip + 0x1b94b77]  ; -> 02064CC0
004D0149  subss    xmm1, dword ptr [rip + 0x1b94b5f]  ; -> 02064CB0
004D0151  movss    xmm0, dword ptr [rip + 0x1b94b6b]  ; -> 02064CC4
004D0159  subss    xmm0, dword ptr [rip + 0x1b94b53]  ; -> 02064CB4
004D0161  ucomiss  xmm1, xmm8
004D0165  movss    dword ptr [rip + 0x1b94b83], xmm1  ; -> 02064CF0
004D016D  movss    dword ptr [rip + 0x1b94b7f], xmm0  ; -> 02064CF4
004D0175  jp       0x4d0179  ; -> 004D0179
004D0177  je       0x4d0181  ; -> 004D0181
004D0179  ucomiss  xmm0, xmm8
004D017D  jp       0x4d0196  ; -> 004D0196
004D017F  jne      0x4d0196  ; -> 004D0196
004D0181  call     0x22cc40  ; -> 0022CC40 fn
004D0186  movss    xmm0, dword ptr [rip + 0x1b94b66]  ; -> 02064CF4
004D018E  movss    xmm1, dword ptr [rip + 0x1b94b5a]  ; -> 02064CF0
004D0196  comiss   xmm8, xmm1
004D019A  ja       0x4d01a2  ; -> 004D01A2
004D019C  comiss   xmm8, xmm0
004D01A0  jbe      0x4d01a7  ; -> 004D01A7
004D01A2  call     0x22cc30  ; -> 0022CC30 fn
004D01A7  call     0x22cc20  ; -> 0022CC20 fn
004D01AC  movss    xmm1, dword ptr [rip + 0x1b94b2c]  ; -> 02064CE0
004D01B4  subss    xmm1, dword ptr [rip + 0x1b94af4]  ; -> 02064CB0
004D01BC  movss    xmm0, dword ptr [rip + 0x1b94b20]  ; -> 02064CE4
004D01C4  subss    xmm0, dword ptr [rip + 0x1b94ae8]  ; -> 02064CB4
004D01CC  ucomiss  xmm1, xmm8
004D01D0  movss    dword ptr [rip + 0x1b94b28], xmm1  ; -> 02064D00
004D01D8  movss    dword ptr [rip + 0x1b94b24], xmm0  ; -> 02064D04
004D01E0  jp       0x4d01e4  ; -> 004D01E4
004D01E2  je       0x4d01ec  ; -> 004D01EC
004D01E4  ucomiss  xmm0, xmm8
004D01E8  jp       0x4d0201  ; -> 004D0201
004D01EA  jne      0x4d0201  ; -> 004D0201
004D01EC  call     0x22cc40  ; -> 0022CC40 fn
004D01F1  movss    xmm0, dword ptr [rip + 0x1b94b0b]  ; -> 02064D04
004D01F9  movss    xmm1, dword ptr [rip + 0x1b94aff]  ; -> 02064D00
004D0201  comiss   xmm8, xmm1
004D0205  ja       0x4d020d  ; -> 004D020D
004D0207  comiss   xmm8, xmm0
004D020B  jbe      0x4d0212  ; -> 004D0212
004D020D  call     0x22cc30  ; -> 0022CC30 fn
004D0212  call     0x22cc20  ; -> 0022CC20 fn
004D0217  movss    xmm5, dword ptr [rip + 0x1b94ad5]  ; -> 02064CF4
004D021F  movss    xmm1, dword ptr [rip + 0x1b94ad1]  ; -> 02064CF8
004D0227  movaps   xmm9, xmm5
004D022B  mulss    xmm9, dword ptr [rip + 0x1b94ad4]  ; -> 02064D08
004D0234  movaps   xmm6, xmm1
004D0237  movss    xmm4, dword ptr [rip + 0x1b94ab1]  ; -> 02064CF0
004D023F  mulss    xmm6, dword ptr [rip + 0x1b94ab9]  ; -> 02064D00
004D0247  movaps   xmm7, xmm4
004D024A  mulss    xmm7, dword ptr [rip + 0x1b94ab2]  ; -> 02064D04
004D0252  mulss    xmm1, dword ptr [rip + 0x1b94aaa]  ; -> 02064D04
004D025A  mulss    xmm4, dword ptr [rip + 0x1b94aa6]  ; -> 02064D08
004D0262  mulss    xmm5, dword ptr [rip + 0x1b94a96]  ; -> 02064D00
004D026A  movss    dword ptr [rip + 0x1b948ad], xmm9  ; -> 02064B20
004D0273  subss    xmm9, xmm1
004D0278  movss    dword ptr [rip + 0x1b948a4], xmm6  ; -> 02064B24
004D0280  subss    xmm6, xmm4
004D0284  movss    dword ptr [rip + 0x1b9489c], xmm7  ; -> 02064B28
004D028C  subss    xmm7, xmm5
004D0290  ucomiss  xmm9, xmm8
004D0294  jp       0x4d02a0  ; -> 004D02A0
004D0296  jne      0x4d02a0  ; -> 004D02A0
004D0298  mov      r9d, 1
004D029E  jmp      0x4d02a3  ; -> 004D02A3
004D02A0  xor      r9d, r9d
004D02A3  ucomiss  xmm6, xmm8
004D02A7  jp       0x4d02b3  ; -> 004D02B3
004D02A9  jne      0x4d02b3  ; -> 004D02B3
004D02AB  mov      r8d, 1
004D02B1  jmp      0x4d02b6  ; -> 004D02B6
004D02B3  xor      r8d, r8d
004D02B6  ucomiss  xmm7, xmm8
004D02BA  jp       0x4d02c5  ; -> 004D02C5
004D02BC  jne      0x4d02c5  ; -> 004D02C5
004D02BE  mov      edx, 1
004D02C3  jmp      0x4d02c7  ; -> 004D02C7
004D02C5  xor      edx, edx
004D02C7  movzx    r11d, word ptr [rip + 0x1b9483d]  ; -> 02064B0C
004D02CF  xor      ecx, ecx
004D02D1  comiss   xmm8, xmm7
004D02D5  cmova    cx, r14w
004D02DA  xor      eax, eax
004D02DC  comiss   xmm8, xmm6
004D02E0  cmova    ax, r15w
004D02E5  add      cx, ax
004D02E8  xor      eax, eax
004D02EA  comiss   xmm8, xmm9
004D02EE  cmova    ax, r12w
004D02F3  add      cx, ax
004D02F6  lea      eax, [r11 + 0x20]
004D02FA  add      cx, r9w
004D02FE  add      cx, cx
004D0301  add      cx, r8w
004D0305  add      cx, cx
004D0308  add      cx, dx
004D030B  add      cx, cx
004D030E  and      ax, cx
004D0311  mov      word ptr [rip + 0x1b947f8], cx  ; -> 02064B10
004D0318  mov      word ptr [rip + 0x1b94ab5], ax  ; -> 02064DD4
004D031F  cmp      ax, r11w
004D0323  je       0x4d040a  ; -> 004D040A
004D0329  movaps   xmm2, xmmword ptr [rip + 0x4450c0]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004D0330  movsx    edx, word ptr [rip + 0x1b94a7d]  ; -> 02064DB4
004D0337  movaps   xmm1, xmm2
004D033A  movups   xmm0, xmmword ptr [rip + 0x1b9496f]  ; -> 02064CB0
004D0341  inc      word ptr [rip + 0x1b94a70]  ; -> 02064DB8
004D0348  mov      eax, edx
004D034A  shl      eax, 4
004D034D  inc      dx
004D0350  movsxd   rcx, eax
004D0353  mulps    xmm1, xmm0
004D0356  movsx    eax, dx
004D0359  inc      dx
004D035C  movups   xmm0, xmmword ptr [rip + 0x1b9495d]  ; -> 02064CC0
004D0363  shl      eax, 4
004D0366  cvttps2dq xmm3, xmm1
004D036A  movaps   xmm1, xmm2
004D036D  mulps    xmm1, xmm0
004D0370  movups   xmm0, xmmword ptr [rip + 0x1b94959]  ; -> 02064CD0
004D0377  movups   xmmword ptr [rip + 0x1b94932], xmm3  ; -> 02064CB0
004D037E  cvttps2dq xmm4, xmm1
004D0382  movaps   xmm1, xmm2
004D0385  mulps    xmm1, xmm0
004D0388  movups   xmm0, xmmword ptr [rip + 0x1b94951]  ; -> 02064CE0
004D038F  movups   xmmword ptr [rip + 0x1b9492a], xmm4  ; -> 02064CC0
004D0396  cvttps2dq xmm5, xmm1
004D039A  mulps    xmm2, xmm0
004D039D  movups   xmm0, xmmword ptr [rip + 0x1b947fc]  ; -> 02064BA0
004D03A4  movups   xmmword ptr [rip + 0x1b94925], xmm5  ; -> 02064CD0
004D03AB  movups   xmmword ptr [rcx + rbp], xmm0
004D03AF  movsxd   rcx, eax
004D03B2  movsx    eax, dx
004D03B5  inc      dx
004D03B8  shl      eax, 4
004D03BB  cvttps2dq xmm1, xmm2
004D03BF  movups   xmmword ptr [rcx + rbp], xmm3
004D03C3  movsxd   rcx, eax
004D03C6  movsx    eax, dx
004D03C9  inc      dx
004D03CC  shl      eax, 4
004D03CF  movups   xmmword ptr [rip + 0x1b9490a], xmm1  ; -> 02064CE0
004D03D6  movups   xmmword ptr [rcx + rbp], xmm4
004D03DA  movsxd   rcx, eax
004D03DD  movsx    eax, dx
004D03E0  inc      dx
004D03E3  shl      eax, 4
004D03E6  cdqe     
004D03E8  movups   xmmword ptr [rcx + rbp], xmm5
004D03EC  mov      word ptr [rip + 0x1b949c1], dx  ; -> 02064DB4
004D03F3  mov      rcx, r13
004D03F6  mov      rdx, rsi
004D03F9  movups   xmmword ptr [rax + rbp], xmm1
004D03FD  call     0x4cf3b0  ; -> 004CF3B0 fn
004D0402  movzx    r11d, word ptr [rip + 0x1b94702]  ; -> 02064B0C
004D040A  movzx    ebx, word ptr [rip + 0x1b949b7]  ; -> 02064DC8
004D0411  movzx    edi, word ptr [rip + 0x1b949ac]  ; -> 02064DC4
004D0418  inc      bx
004D041B  mov      word ptr [rip + 0x1b949a6], bx  ; -> 02064DC8
004D0422  cmp      di, r11w
004D0426  jne      0x4d0070  ; -> 004D0070
004D042C  add      r11w, 0x13
004D0431  xor      r8d, r8d
004D0434  movsx    eax, r11w
004D0438  mov      rdx, rsi
004D043B  shl      eax, 4
004D043E  movsxd   rcx, eax
004D0441  add      rcx, rbp
004D0444  mov      word ptr [rip + 0x1b94988], r11w  ; -> 02064DD4
004D044C  call     r13
004D044F  movsx    ebx, word ptr [rip + 0x1b946b6]  ; -> 02064B0C
004D0456  mov      r11d, ebx
004D0459  add      r11w, bx
004D045D  mov      word ptr [rip + 0x1b94963], r11w  ; -> 02064DC8
004D0465  lea      edi, [rbx + 6]
004D0468  nop      dword ptr [rax + rax]
004D0470  movsx    eax, r11w
004D0474  dec      di
004D0477  add      eax, 0xa
004D047A  mov      word ptr [rip + 0x1b94943], di  ; -> 02064DC4
004D0481  shl      eax, 4
004D0484  movsxd   rcx, eax
004D0487  movsx    r8d, word ptr [rcx + rbp + 0xc]
004D048D  movsx    eax, word ptr [rcx + rbp]
004D0491  add      eax, 0x64
004D0494  mov      word ptr [rip + 0x1b94948], r8w  ; -> 02064DE4
004D049C  shl      eax, 4
004D049F  movsxd   r9, eax
004D04A2  movsx    eax, word ptr [rcx + rbp + 4]
004D04A7  add      eax, 0x64
004D04AA  shl      eax, 4
004D04AD  movups   xmm0, xmmword ptr [r9 + rbp]
004D04B2  movzx    r9d, word ptr [r9 + rbp + 0xc]
004D04B8  movsxd   r10, eax
004D04BB  movsx    eax, word ptr [rcx + rbp + 8]
004D04C0  add      eax, 0x64
004D04C3  shl      eax, 4
004D04C6  movsx    ecx, word ptr [r10 + rbp + 0xc]
004D04CC  movsxd   rdx, eax
004D04CF  lea      eax, [r8 + 0x64]
004D04D3  shl      eax, 4
004D04D6  movsxd   r8, eax
004D04D9  movups   xmmword ptr [rip + 0x1b947d0], xmm0  ; -> 02064CB0
004D04E0  mov      word ptr [rip + 0x1b948f1], cx  ; -> 02064DD8
004D04E7  movups   xmm0, xmmword ptr [r10 + rbp]
004D04EC  movsx    eax, word ptr [r8 + rbp + 0xc]
004D04F2  mov      word ptr [rip + 0x1b948e7], ax  ; -> 02064DE0
004D04F9  movups   xmmword ptr [rip + 0x1b947c0], xmm0  ; -> 02064CC0
004D0500  movups   xmm0, xmmword ptr [rdx + rbp]
004D0504  movzx    edx, word ptr [rdx + rbp + 0xc]
004D0509  or       dx, ax
004D050C  movsx    eax, dx
004D050F  or       ax, cx
004D0512  mov      word ptr [rip + 0x1b948c3], dx  ; -> 02064DDC
004D0519  or       r9w, ax
004D051D  mov      word ptr [rip + 0x1b948af], r9w  ; -> 02064DD4
004D0525  movups   xmmword ptr [rip + 0x1b947a4], xmm0  ; -> 02064CD0
004D052C  movups   xmm0, xmmword ptr [r8 + rbp]
004D0531  movups   xmmword ptr [rip + 0x1b947a8], xmm0  ; -> 02064CE0
004D0538  cmp      r9w, bx
004D053C  jne      0x4d0816  ; -> 004D0816
004D0542  movss    xmm1, dword ptr [rip + 0x1b94776]  ; -> 02064CC0
004D054A  subss    xmm1, dword ptr [rip + 0x1b9475e]  ; -> 02064CB0
004D0552  movss    xmm0, dword ptr [rip + 0x1b9476a]  ; -> 02064CC4
004D055A  subss    xmm0, dword ptr [rip + 0x1b94752]  ; -> 02064CB4
004D0562  ucomiss  xmm1, xmm8
004D0566  movss    dword ptr [rip + 0x1b94782], xmm1  ; -> 02064CF0
004D056E  movss    dword ptr [rip + 0x1b9477e], xmm0  ; -> 02064CF4
004D0576  jp       0x4d057a  ; -> 004D057A
004D0578  je       0x4d0582  ; -> 004D0582
004D057A  ucomiss  xmm0, xmm8
004D057E  jp       0x4d0597  ; -> 004D0597
004D0580  jne      0x4d0597  ; -> 004D0597
004D0582  call     0x22cc40  ; -> 0022CC40 fn
004D0587  movss    xmm0, dword ptr [rip + 0x1b94765]  ; -> 02064CF4
004D058F  movss    xmm1, dword ptr [rip + 0x1b94759]  ; -> 02064CF0
004D0597  comiss   xmm8, xmm1
004D059B  ja       0x4d05a3  ; -> 004D05A3
004D059D  comiss   xmm8, xmm0
004D05A1  jbe      0x4d05a8  ; -> 004D05A8
004D05A3  call     0x22cc30  ; -> 0022CC30 fn
004D05A8  call     0x22cc20  ; -> 0022CC20 fn
004D05AD  movss    xmm1, dword ptr [rip + 0x1b9472b]  ; -> 02064CE0
004D05B5  subss    xmm1, dword ptr [rip + 0x1b946f3]  ; -> 02064CB0
004D05BD  movss    xmm0, dword ptr [rip + 0x1b9471f]  ; -> 02064CE4
004D05C5  subss    xmm0, dword ptr [rip + 0x1b946e7]  ; -> 02064CB4
004D05CD  ucomiss  xmm1, xmm8
004D05D1  movss    dword ptr [rip + 0x1b94727], xmm1  ; -> 02064D00
004D05D9  movss    dword ptr [rip + 0x1b94723], xmm0  ; -> 02064D04
004D05E1  jp       0x4d05e5  ; -> 004D05E5
004D05E3  je       0x4d05ed  ; -> 004D05ED
004D05E5  ucomiss  xmm0, xmm8
004D05E9  jp       0x4d0602  ; -> 004D0602
004D05EB  jne      0x4d0602  ; -> 004D0602
004D05ED  call     0x22cc40  ; -> 0022CC40 fn
004D05F2  movss    xmm0, dword ptr [rip + 0x1b9470a]  ; -> 02064D04
004D05FA  movss    xmm1, dword ptr [rip + 0x1b946fe]  ; -> 02064D00
004D0602  comiss   xmm8, xmm1
004D0606  ja       0x4d060e  ; -> 004D060E
004D0608  comiss   xmm8, xmm0
004D060C  jbe      0x4d0613  ; -> 004D0613
004D060E  call     0x22cc30  ; -> 0022CC30 fn
004D0613  call     0x22cc20  ; -> 0022CC20 fn
004D0618  movss    xmm5, dword ptr [rip + 0x1b946d4]  ; -> 02064CF4
004D0620  movss    xmm1, dword ptr [rip + 0x1b946d0]  ; -> 02064CF8
004D0628  movaps   xmm9, xmm5
004D062C  mulss    xmm9, dword ptr [rip + 0x1b946d3]  ; -> 02064D08
004D0635  movaps   xmm6, xmm1
004D0638  movss    xmm4, dword ptr [rip + 0x1b946b0]  ; -> 02064CF0
004D0640  mulss    xmm6, dword ptr [rip + 0x1b946b8]  ; -> 02064D00
004D0648  movaps   xmm7, xmm4
004D064B  mulss    xmm7, dword ptr [rip + 0x1b946b1]  ; -> 02064D04
004D0653  mulss    xmm1, dword ptr [rip + 0x1b946a9]  ; -> 02064D04
004D065B  mulss    xmm4, dword ptr [rip + 0x1b946a5]  ; -> 02064D08
004D0663  mulss    xmm5, dword ptr [rip + 0x1b94695]  ; -> 02064D00
004D066B  movss    dword ptr [rip + 0x1b944ac], xmm9  ; -> 02064B20
004D0674  subss    xmm9, xmm1
004D0679  movss    dword ptr [rip + 0x1b944a3], xmm6  ; -> 02064B24
004D0681  subss    xmm6, xmm4
004D0685  movss    dword ptr [rip + 0x1b9449b], xmm7  ; -> 02064B28
004D068D  subss    xmm7, xmm5
004D0691  ucomiss  xmm9, xmm8
004D0695  jp       0x4d06a1  ; -> 004D06A1
004D0697  jne      0x4d06a1  ; -> 004D06A1
004D0699  mov      r9d, 1
004D069F  jmp      0x4d06a4  ; -> 004D06A4
004D06A1  xor      r9d, r9d
004D06A4  ucomiss  xmm6, xmm8
004D06A8  jp       0x4d06b4  ; -> 004D06B4
004D06AA  jne      0x4d06b4  ; -> 004D06B4
004D06AC  mov      r8d, 1
004D06B2  jmp      0x4d06b7  ; -> 004D06B7
004D06B4  xor      r8d, r8d
004D06B7  ucomiss  xmm7, xmm8
004D06BB  jp       0x4d06c6  ; -> 004D06C6
004D06BD  jne      0x4d06c6  ; -> 004D06C6
004D06BF  mov      edx, 1
004D06C4  jmp      0x4d06c8  ; -> 004D06C8
004D06C6  xor      edx, edx
004D06C8  movzx    ebx, word ptr [rip + 0x1b9443d]  ; -> 02064B0C
004D06CF  xor      ecx, ecx
004D06D1  comiss   xmm8, xmm7
004D06D5  cmova    cx, r14w
004D06DA  xor      eax, eax
004D06DC  comiss   xmm8, xmm6
004D06E0  cmova    ax, r15w
004D06E5  add      cx, ax
004D06E8  xor      eax, eax
004D06EA  comiss   xmm8, xmm9
004D06EE  cmova    ax, r12w
004D06F3  add      cx, ax
004D06F6  lea      eax, [rbx + 0x20]
004D06F9  add      cx, r9w
004D06FD  add      cx, cx
004D0700  add      cx, r8w
004D0704  add      cx, cx
004D0707  add      cx, dx
004D070A  add      cx, cx
004D070D  and      ax, cx
004D0710  mov      word ptr [rip + 0x1b943f9], cx  ; -> 02064B10
004D0717  mov      word ptr [rip + 0x1b946b6], ax  ; -> 02064DD4
004D071E  cmp      ax, bx
004D0721  jne      0x4d0807  ; -> 004D0807
004D0727  movaps   xmm2, xmmword ptr [rip + 0x444cc2]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004D072E  movsx    edx, word ptr [rip + 0x1b9467f]  ; -> 02064DB4
004D0735  movaps   xmm1, xmm2
004D0738  movups   xmm0, xmmword ptr [rip + 0x1b94571]  ; -> 02064CB0
004D073F  inc      word ptr [rip + 0x1b94672]  ; -> 02064DB8
004D0746  mov      eax, edx
004D0748  shl      eax, 4
004D074B  inc      dx
004D074E  movsxd   rcx, eax
004D0751  mulps    xmm1, xmm0
004D0754  movsx    eax, dx
004D0757  inc      dx
004D075A  movups   xmm0, xmmword ptr [rip + 0x1b9455f]  ; -> 02064CC0
004D0761  shl      eax, 4
004D0764  cvttps2dq xmm3, xmm1
004D0768  movaps   xmm1, xmm2
004D076B  mulps    xmm1, xmm0
004D076E  movups   xmm0, xmmword ptr [rip + 0x1b9455b]  ; -> 02064CD0
004D0775  movups   xmmword ptr [rip + 0x1b94534], xmm3  ; -> 02064CB0
004D077C  cvttps2dq xmm4, xmm1
004D0780  movaps   xmm1, xmm2
004D0783  mulps    xmm1, xmm0
004D0786  movups   xmm0, xmmword ptr [rip + 0x1b94553]  ; -> 02064CE0
004D078D  movups   xmmword ptr [rip + 0x1b9452c], xmm4  ; -> 02064CC0
004D0794  cvttps2dq xmm5, xmm1
004D0798  mulps    xmm2, xmm0
004D079B  movups   xmm0, xmmword ptr [rip + 0x1b9440e]  ; -> 02064BB0
004D07A2  movups   xmmword ptr [rip + 0x1b94527], xmm5  ; -> 02064CD0
004D07A9  movups   xmmword ptr [rcx + rbp], xmm0
004D07AD  movsxd   rcx, eax
004D07B0  movsx    eax, dx
004D07B3  inc      dx
004D07B6  shl      eax, 4
004D07B9  cvttps2dq xmm1, xmm2
004D07BD  movups   xmmword ptr [rcx + rbp], xmm3
004D07C1  movsxd   rcx, eax
004D07C4  movsx    eax, dx
004D07C7  inc      dx
004D07CA  shl      eax, 4
004D07CD  movups   xmmword ptr [rip + 0x1b9450c], xmm1  ; -> 02064CE0
004D07D4  movups   xmmword ptr [rcx + rbp], xmm4
004D07D8  movsxd   rcx, eax
004D07DB  movsx    eax, dx
004D07DE  inc      dx
004D07E1  shl      eax, 4
004D07E4  cdqe     
004D07E6  movups   xmmword ptr [rcx + rbp], xmm5
004D07EA  mov      word ptr [rip + 0x1b945c3], dx  ; -> 02064DB4
004D07F1  mov      rcx, r13
004D07F4  mov      rdx, rsi
004D07F7  movups   xmmword ptr [rax + rbp], xmm1
004D07FB  call     0x4cf3b0  ; -> 004CF3B0 fn
004D0800  movzx    ebx, word ptr [rip + 0x1b94305]  ; -> 02064B0C
004D0807  movzx    r11d, word ptr [rip + 0x1b945b9]  ; -> 02064DC8
004D080F  movzx    edi, word ptr [rip + 0x1b945ae]  ; -> 02064DC4
004D0816  inc      r11w
004D081A  mov      word ptr [rip + 0x1b945a6], r11w  ; -> 02064DC8
004D0822  cmp      di, bx
004D0825  jne      0x4d0470  ; -> 004D0470
004D082B  movaps   xmm14, xmmword ptr [rsp + 0x40]
004D0831  lea      r11, [rsp + 0xd0]
004D0839  mov      rbx, qword ptr [r11 + 0x50]
004D083D  movaps   xmm6, xmmword ptr [r11 - 0x10]
004D0842  movaps   xmm7, xmmword ptr [r11 - 0x20]
004D0847  movaps   xmm8, xmmword ptr [r11 - 0x30]
004D084C  movaps   xmm9, xmmword ptr [r11 - 0x40]
004D0851  movaps   xmm10, xmmword ptr [r11 - 0x50]
004D0856  movaps   xmm11, xmmword ptr [r11 - 0x60]
004D085B  movaps   xmm12, xmmword ptr [r11 - 0x70]
004D0860  movaps   xmm13, xmmword ptr [r11 - 0x80]
004D0865  movaps   xmm15, xmmword ptr [rsp + 0x30]
004D086B  mov      rsp, r11
004D086E  pop      r15
004D0870  pop      r14
004D0872  pop      r13
004D0874  pop      r12
004D0876  pop      rdi
004D0877  pop      rsi
004D0878  pop      rbp
004D0879  ret      
```

## 004D0FA0 (11709 B, extent 004D0FA0-004D3D5D)

Page context: "18' = 0x1000404, '+0x1C' = 0x6C0E0000 - a module record's init.  Interior anchor '004ED973' (function '004ED960').  '004D0CB0' (450 B) is a battery constructor '0037E0F0' calls: '008631E0' registers '004D0FA0', '008631D0(0x17)' fills '+0x10', then '+0x8' = 0x03000000, '+0xC' = 0x02000000, '+0x18' = 0x1000404, '+0x1C' = 0x6C140000, and the '+0x20'..'+0x68' constant flood ('0x8000'/'0x602E4000'/'0x412412'/'0x457FA000'/'0x4B7FFF28'/'0x80' "

```
004D0FA0  mov      rax, rsp
004D0FA3  mov      qword ptr [rax + 8], rcx
004D0FA7  push     rbx
004D0FA8  push     rbp
004D0FA9  push     rsi
004D0FAA  push     rdi
004D0FAB  push     r13
004D0FAD  push     r14
004D0FAF  sub      rsp, 0xe8
004D0FB6  movaps   xmmword ptr [rax - 0x48], xmm6
004D0FBA  mov      r13, rdx
004D0FBD  movaps   xmmword ptr [rax - 0x58], xmm7
004D0FC1  mov      r9, rcx
004D0FC4  movaps   xmmword ptr [rax - 0x68], xmm8
004D0FC9  movaps   xmmword ptr [rax - 0x78], xmm9
004D0FCE  movaps   xmmword ptr [rax - 0x88], xmm10
004D0FD6  movaps   xmmword ptr [rax - 0x98], xmm11
004D0FDE  movaps   xmmword ptr [rsp + 0x70], xmm12
004D0FE4  movaps   xmmword ptr [rsp + 0x60], xmm13
004D0FEA  movaps   xmmword ptr [rsp + 0x50], xmm14
004D0FF0  movaps   xmmword ptr [rsp + 0x40], xmm15
004D0FF6  test     r8d, r8d
004D0FF9  je       0x4d3bfa  ; -> 004D3BFA
004D0FFF  cmp      r8d, 1
004D1003  jne      0x4d24ee  ; -> 004D24EE
004D1009  movsx    r8d, word ptr [rip + 0x1b93afb]  ; -> 02064B0C
004D1011  lea      rbp, [rip + 0x1b93e18]  ; -> 02064E30
004D1018  movsd    xmm15, qword ptr [rip + 0x181ad5f]  ; -> 01CEBD80 [u64 0x7FFFFFFFFFFFFFFF]
004D1021  mov      ecx, r8d
004D1024  movss    xmm12, dword ptr [rip + 0x42f333]  ; -> 00900360 [u32 0x7F7FFFFF]
004D102D  xorps    xmm10, xmm10
004D1031  shl      ecx, 4
004D1034  movsxd   rax, ecx
004D1037  mov      word ptr [rip + 0x1b93d99], r8w  ; -> 02064DD8
004D103F  movzx    eax, word ptr [rax + rbp]
004D1043  mov      word ptr [rip + 0x1b93d72], ax  ; -> 02064DBC
004D104A  lea      eax, [rcx + 0x10]
004D104D  movsxd   rcx, eax
004D1050  lea      eax, [r8 + 0x1e]
004D1054  shl      eax, 4
004D1057  movups   xmm0, xmmword ptr [rcx + rbp]
004D105B  movsxd   rcx, eax
004D105E  movups   xmmword ptr [rip + 0x1b93acb], xmm0  ; -> 02064B30
004D1065  movups   xmm0, xmmword ptr [rcx + rbp]
004D1069  movzx    r9d, word ptr [rcx + rbp]
004D106E  dec      r9w
004D1072  movups   xmmword ptr [rip + 0x1b93b57], xmm0  ; -> 02064BD0
004D1079  nop      dword ptr [rax]
004D1080  movsx    edx, r8w
004D1084  dec      r9w
004D1088  mov      word ptr [rip + 0x1b93d40], r9w  ; -> 02064DD0
004D1090  lea      eax, [rdx + 0x22]
004D1093  shl      eax, 4
004D1096  movsxd   rcx, eax
004D1099  lea      eax, [rdx + 0x23]
004D109C  shl      eax, 4
004D109F  movups   xmm2, xmmword ptr [rcx + rbp]
004D10A3  movsxd   rcx, eax
004D10A6  movdqu   xmmword ptr [rip + 0x1b93b82], xmm2  ; -> 02064C30
004D10AE  movups   xmm1, xmmword ptr [rcx + rbp]
004D10B2  movss    dword ptr [rip + 0x1b93b76], xmm2  ; -> 02064C30
004D10BA  movdqu   xmmword ptr [rip + 0x1b93b7e], xmm1  ; -> 02064C40
004D10C2  movss    xmm0, dword ptr [rip + 0x1b93b7a]  ; -> 02064C44
004D10CA  subss    xmm1, xmm2
004D10CE  movss    dword ptr [rip + 0x1b93b6a], xmm1  ; -> 02064C40
004D10D6  movaps   xmm1, xmm2
004D10D9  shufps   xmm1, xmm2, 0x55
004D10DD  subss    xmm0, xmm1
004D10E1  movss    dword ptr [rip + 0x1b93b4b], xmm1  ; -> 02064C34
004D10E9  movaps   xmm1, xmm2
004D10EC  shufps   xmm1, xmm2, 0xaa
004D10F0  shufps   xmm2, xmm2, 0xff
004D10F4  movss    dword ptr [rip + 0x1b93b3c], xmm1  ; -> 02064C38
004D10FC  movss    dword ptr [rip + 0x1b93b40], xmm0  ; -> 02064C44
004D1104  movss    xmm0, dword ptr [rip + 0x1b93b3c]  ; -> 02064C48
004D110C  subss    xmm0, xmm1
004D1110  movss    dword ptr [rip + 0x1b93b24], xmm2  ; -> 02064C3C
004D1118  movss    dword ptr [rip + 0x1b93b28], xmm0  ; -> 02064C48
004D1120  movss    xmm0, dword ptr [rip + 0x1b93b24]  ; -> 02064C4C
004D1128  subss    xmm0, xmm2
004D112C  movss    dword ptr [rip + 0x1b93b18], xmm0  ; -> 02064C4C
004D1134  call     0x22cc20  ; -> 0022CC20 fn
004D1139  movss    xmm11, dword ptr [rip + 0x19316fa]  ; -> 01E0283C [f32 1]
004D1142  movss    xmm6, dword ptr [rip + 0x1b93af6]  ; -> 02064C40
004D114A  movss    xmm7, dword ptr [rip + 0x1b93af2]  ; -> 02064C44
004D1152  movaps   xmm2, xmm6
004D1155  movss    xmm8, dword ptr [rip + 0x1b93aea]  ; -> 02064C48
004D115E  movaps   xmm0, xmm7
004D1161  mulss    xmm0, xmm7
004D1165  movaps   xmm1, xmm8
004D1169  mulss    xmm1, xmm8
004D116E  movss    dword ptr [rip + 0x1b93aae], xmm0  ; -> 02064C24
004D1176  mulss    xmm0, xmm11
004D117B  mulss    xmm2, xmm6
004D117F  movss    dword ptr [rip + 0x1b93aa1], xmm1  ; -> 02064C28
004D1187  mulss    xmm1, xmm11
004D118C  movss    dword ptr [rip + 0x1b93a8c], xmm2  ; -> 02064C20
004D1194  mulss    xmm2, xmm11
004D1199  addss    xmm2, xmm0
004D119D  addss    xmm1, xmm2
004D11A1  movss    dword ptr [rip + 0x1b93983], xmm2  ; -> 02064B2C
004D11A9  cvtps2pd xmm0, xmm1
004D11AC  movss    dword ptr [rip + 0x1b93a78], xmm1  ; -> 02064C2C
004D11B4  andps    xmm0, xmm15
004D11B8  cvtpd2ps xmm0, xmm0
004D11BC  call     0x861f14  ; -> 00861F14 fn
004D11C1  movaps   xmm1, xmm0
004D11C4  ucomiss  xmm1, xmm10
004D11C8  jp       0x4d11d2  ; -> 004D11D2
004D11CA  jne      0x4d11d2  ; -> 004D11D2
004D11CC  movaps   xmm0, xmm12
004D11D0  jmp      0x4d11da  ; -> 004D11DA
004D11D2  movaps   xmm0, xmm11
004D11D6  divss    xmm0, xmm1
004D11DA  movss    xmm1, dword ptr [rip + 0x1b93a4e]  ; -> 02064C30
004D11E2  movsx    r8d, word ptr [rip + 0x1b93bee]  ; -> 02064DD8
004D11EA  movzx    r9d, word ptr [rip + 0x1b93bde]  ; -> 02064DD0
004D11F2  movzx    edx, word ptr [rip + 0x1b93913]  ; -> 02064B0C
004D11F9  mulss    xmm6, xmm0
004D11FD  lea      eax, [r8 + 0x23]
004D1201  inc      r8w
004D1205  mulss    xmm7, xmm0
004D1209  shl      eax, 4
004D120C  mulss    xmm8, xmm0
004D1211  movsxd   rcx, eax
004D1214  movss    dword ptr [rip + 0x1b938e4], xmm0  ; -> 02064B00
004D121C  movss    xmm0, dword ptr [rip + 0x1b939b8]  ; -> 02064BDC
004D1224  mulss    xmm6, xmm0
004D1228  mov      word ptr [rip + 0x1b93ba8], r8w  ; -> 02064DD8
004D1230  mulss    xmm8, xmm0
004D1235  mulss    xmm7, xmm0
004D1239  addss    xmm1, xmm6
004D123D  movss    xmm0, dword ptr [rip + 0x1b939ef]  ; -> 02064C34
004D1245  addss    xmm0, xmm7
004D1249  movss    dword ptr [rip + 0x1b939df], xmm1  ; -> 02064C30
004D1251  movss    xmm1, dword ptr [rip + 0x1b939df]  ; -> 02064C38
004D1259  addss    xmm1, xmm8
004D125E  movss    dword ptr [rip + 0x1b939ce], xmm0  ; -> 02064C34
004D1266  movss    dword ptr [rip + 0x1b939ca], xmm1  ; -> 02064C38
004D126E  movups   xmm0, xmmword ptr [rip + 0x1b939bb]  ; -> 02064C30
004D1275  movups   xmmword ptr [rcx + rbp], xmm0
004D1279  cmp      r9w, dx
004D127D  jne      0x4d1080  ; -> 004D1080
004D1283  movss    xmm0, dword ptr [rip + 0x181a91d]  ; -> 01CEBBA8 [f32 1]
004D128B  movzx    r10d, dx
004D128F  movsx    r8d, dx
004D1293  mov      word ptr [rip + 0x1b93b26], dx  ; -> 02064DC0
004D129A  lea      eax, [r8 + 0x1f]
004D129E  shl      eax, 4
004D12A1  movsxd   rcx, eax
004D12A4  movups   xmm13, xmmword ptr [rcx + rbp]
004D12A9  comiss   xmm0, xmm13
004D12AD  movdqu   xmmword ptr [rip + 0x1b939aa], xmm13  ; -> 02064C60
004D12B6  ja       0x4d12bc  ; -> 004D12BC
004D12B8  movaps   xmm13, xmm0
004D12BC  maxss    xmm13, dword ptr [rip + 0x193156b]  ; -> 01E02830 [u32 0x00000000]
004D12C5  mov      dword ptr [rip + 0x1b93835], 0x3f7d70a4  ; -> 02064B04
004D12CF  mulss    xmm13, dword ptr [rip + 0x421e38]  ; -> 008F3110 [f32 0.99]
004D12D8  ucomiss  xmm13, xmm10
004D12DC  movss    dword ptr [rip + 0x1b9397b], xmm13  ; -> 02064C60
004D12E5  jp       0x4d12ef  ; -> 004D12EF
004D12E7  jne      0x4d12ef  ; -> 004D12EF
004D12E9  movaps   xmm1, xmm12
004D12ED  jmp      0x4d12f8  ; -> 004D12F8
004D12EF  movaps   xmm1, xmm11
004D12F3  divss    xmm1, xmm13
004D12F8  movss    xmm8, dword ptr [rip + 0x1931533]  ; -> 01E02834 [u32 0x00000000]
004D1301  lea      eax, [r8 + 0xc]
004D1305  shl      eax, 4
004D1308  addss    xmm8, xmm1
004D130D  movsxd   rcx, eax
004D1310  movzx    r11d, dx
004D1314  lea      eax, [r8 + 0xd]
004D1318  movss    dword ptr [rip + 0x1b937e0], xmm1  ; -> 02064B00
004D1320  shl      eax, 4
004D1323  mov      word ptr [rip + 0x1b93aae], dx  ; -> 02064DD8
004D132A  movups   xmm0, xmmword ptr [rcx + rbp]
004D132E  movsxd   rcx, eax
004D1331  lea      eax, [r8 + 0xe]
004D1335  shl      eax, 4
004D1338  movups   xmmword ptr [rip + 0x1b93891], xmm0  ; -> 02064BD0
004D133F  mov      word ptr [rip + 0x1b93a86], dx  ; -> 02064DCC
004D1346  movups   xmm0, xmmword ptr [rcx + rbp]
004D134A  movsxd   rcx, eax
004D134D  lea      eax, [r8 + 0xf]
004D1351  shl      eax, 4
004D1354  movups   xmmword ptr [rip + 0x1b93885], xmm0  ; -> 02064BE0
004D135B  movups   xmm0, xmmword ptr [rcx + rbp]
004D135F  movsxd   rcx, eax
004D1362  lea      eax, [r8 + 0x10]
004D1366  shl      eax, 4
004D1369  movups   xmmword ptr [rip + 0x1b93880], xmm0  ; -> 02064BF0
004D1370  movups   xmm0, xmmword ptr [rcx + rbp]
004D1374  movsxd   rcx, eax
004D1377  lea      eax, [r8 + 0x11]
004D137B  shl      eax, 4
004D137E  movups   xmmword ptr [rip + 0x1b9387b], xmm0  ; -> 02064C00
004D1385  movups   xmm0, xmmword ptr [rcx + rbp]
004D1389  movsxd   rcx, eax
004D138C  lea      eax, [r8 + 0x12]
004D1390  shl      eax, 4
004D1393  movups   xmmword ptr [rip + 0x1b93876], xmm0  ; -> 02064C10
004D139A  movups   xmm0, xmmword ptr [rcx + rbp]
004D139E  movsxd   rcx, eax
004D13A1  lea      eax, [r8 + 0x13]
004D13A5  shl      eax, 4
004D13A8  movups   xmmword ptr [rip + 0x1b93871], xmm0  ; -> 02064C20
004D13AF  movups   xmm0, xmmword ptr [rcx + rbp]
004D13B3  movsxd   rcx, eax
004D13B6  lea      eax, [r8 + 0x1e]
004D13BA  shl      eax, 4
004D13BD  ucomiss  xmm8, xmm10
004D13C1  movups   xmmword ptr [rip + 0x1b93868], xmm0  ; -> 02064C30
004D13C8  movups   xmm0, xmmword ptr [rcx + rbp]
004D13CC  movsxd   rcx, eax
004D13CF  movss    dword ptr [rip + 0x1b9388c], xmm8  ; -> 02064C64
004D13D8  movups   xmmword ptr [rip + 0x1b93861], xmm0  ; -> 02064C40
004D13DF  movzx    r8d, word ptr [rcx + rbp]
004D13E4  mov      word ptr [rip + 0x1b939e4], r8w  ; -> 02064DD0
004D13EC  jp       0x4d142f  ; -> 004D142F
004D13EE  jne      0x4d142f  ; -> 004D142F
004D13F0  call     0x22cc40  ; -> 0022CC40 fn
004D13F5  movzx    edx, word ptr [rip + 0x1b93710]  ; -> 02064B0C
004D13FC  movzx    r8d, word ptr [rip + 0x1b939cc]  ; -> 02064DD0
004D1404  movzx    r11d, word ptr [rip + 0x1b939cc]  ; -> 02064DD8
004D140C  movzx    r10d, word ptr [rip + 0x1b939ac]  ; -> 02064DC0
004D1414  movss    xmm11, dword ptr [rip + 0x193141f]  ; -> 01E0283C [f32 1]
004D141D  movss    xmm8, dword ptr [rip + 0x1b9383e]  ; -> 02064C64
004D1426  movss    xmm13, dword ptr [rip + 0x1b93831]  ; -> 02064C60
004D142F  comiss   xmm10, xmm8
004D1433  jbe      0x4d1474  ; -> 004D1474
004D1435  call     0x22cc30  ; -> 0022CC30 fn
004D143A  movzx    edx, word ptr [rip + 0x1b936cb]  ; -> 02064B0C
004D1441  movzx    r8d, word ptr [rip + 0x1b93987]  ; -> 02064DD0
004D1449  movzx    r11d, word ptr [rip + 0x1b93987]  ; -> 02064DD8
004D1451  movzx    r10d, word ptr [rip + 0x1b93967]  ; -> 02064DC0
004D1459  movss    xmm11, dword ptr [rip + 0x19313da]  ; -> 01E0283C [f32 1]
004D1462  movss    xmm8, dword ptr [rip + 0x1b937f9]  ; -> 02064C64
004D146B  movss    xmm13, dword ptr [rip + 0x1b937ec]  ; -> 02064C60
004D1474  movups   xmm0, xmmword ptr [rip + 0x1b937e5]  ; -> 02064C60
004D147B  mov      esi, 0x80
004D1480  movsx    edi, dx
004D1483  movss    xmm15, dword ptr [rip + 0x19313a4]  ; -> 01E02830 [u32 0x00000000]
004D148C  movss    xmm14, dword ptr [rip + 0x19313a3]  ; -> 01E02838 [u32 0x00000000]
004D1495  movaps   xmm3, xmm15
004D1499  addss    xmm3, xmm11
004D149E  lea      eax, [rdi + 0x1f]
004D14A1  shl      eax, 4
004D14A4  addss    xmm14, xmm15
004D14A9  movsxd   rcx, eax
004D14AC  lea      eax, [rdi + 0x1e]
004D14AF  shl      eax, 4
004D14B2  movss    dword ptr [rsp + 0x130], xmm3
004D14BB  add      esi, edx
004D14BD  movups   xmmword ptr [rcx + rbp], xmm0
004D14C1  movsxd   rcx, eax
004D14C4  movups   xmm0, xmmword ptr [rcx + rbp]
004D14C8  movups   xmmword ptr [rip + 0x1b937a1], xmm0  ; -> 02064C70
004D14CF  movss    xmm1, dword ptr [rip + 0x1b9379d]  ; -> 02064C74
004D14D7  movups   xmm2, xmm0
004D14DA  nop      word ptr [rax + rax]
004D14E0  movsx    r9d, r11w
004D14E4  dec      r8w
004D14E8  movaps   xmm0, xmm1
004D14EB  movss    dword ptr [rip + 0x1b9378d], xmm3  ; -> 02064C80
004D14F3  mulss    xmm0, xmm8
004D14F8  inc      r10w
004D14FC  mov      word ptr [rip + 0x1b938cc], r8w  ; -> 02064DD0
004D1504  lea      eax, [r9 + 0x226]
004D150B  shl      eax, 4
004D150E  movsxd   rbx, eax
004D1511  lea      eax, [r9 + 0x22]
004D1515  shl      eax, 4
004D1518  movsxd   rcx, eax
004D151B  lea      eax, [r9 + 0x28a]
004D1522  shl      eax, 4
004D1525  movss    dword ptr [rip + 0x1b93757], xmm0  ; -> 02064C84
004D152D  movups   xmmword ptr [rbx + rbp], xmm2
004D1531  movups   xmm0, xmmword ptr [rcx + rbp]
004D1535  movsxd   rcx, eax
004D1538  xor      eax, eax
004D153A  comiss   xmm14, xmm13
004D153E  movups   xmmword ptr [rip + 0x1b9376b], xmm0  ; -> 02064CB0
004D1545  movups   xmm0, xmmword ptr [rip + 0x1b93734]  ; -> 02064C80
004D154C  seta     al
004D154F  shl      ax, 7
004D1553  and      ax, si
004D1556  mov      word ptr [rip + 0x1b93887], ax  ; -> 02064DE4
004D155D  movups   xmmword ptr [rcx + rbp], xmm0
004D1561  cmp      ax, dx
004D1564  je       0x4d1666  ; -> 004D1666
004D156A  movss    xmm4, dword ptr [rip + 0x1b93742]  ; -> 02064CB4
004D1572  lea      eax, [r9 + 0x21]
004D1576  movss    xmm6, dword ptr [rip + 0x1b9373a]  ; -> 02064CB8
004D157E  movaps   xmm0, xmm14
004D1582  subss    xmm0, xmm13
004D1587  shl      eax, 4
004D158A  movzx    r8d, dx
004D158E  mov      word ptr [rip + 0x1b9383b], dx  ; -> 02064DD0
004D1595  subss    xmm1, xmm0
004D1599  movss    dword ptr [rip + 0x1b93727], xmm0  ; -> 02064CC8
004D15A1  movaps   xmm0, xmm1
004D15A4  movss    dword ptr [rip + 0x1b93718], xmm1  ; -> 02064CC4
004D15AC  mulss    xmm0, xmm8
004D15B1  movss    xmm8, dword ptr [rip + 0x1b936be]  ; -> 02064C78
004D15BA  mulss    xmm8, xmm1
004D15BF  movss    dword ptr [rip + 0x1b936bd], xmm0  ; -> 02064C84
004D15C7  movaps   xmm0, xmm15
004D15CB  addss    xmm0, xmm8
004D15D0  mulss    xmm4, xmm8
004D15D5  mulss    xmm6, xmm8
004D15DA  movss    dword ptr [rip + 0x1b9369e], xmm0  ; -> 02064C80
004D15E2  movups   xmm0, xmmword ptr [rip + 0x1b936d7]  ; -> 02064CC0
004D15E9  movups   xmm1, xmmword ptr [rip + 0x1b93690]  ; -> 02064C80
004D15F0  movups   xmmword ptr [rbx + rbp], xmm0
004D15F4  movups   xmmword ptr [rcx + rbp], xmm1
004D15F8  movsxd   rcx, eax
004D15FB  movaps   xmm1, xmm11
004D15FF  subss    xmm1, xmm8
004D1604  movups   xmm3, xmmword ptr [rcx + rbp]
004D1608  movups   xmmword ptr [rip + 0x1b93691], xmm3  ; -> 02064CA0
004D160F  movss    xmm2, dword ptr [rip + 0x1b9368d]  ; -> 02064CA4
004D1617  movss    xmm0, dword ptr [rip + 0x1b93689]  ; -> 02064CA8
004D161F  mulss    xmm2, xmm1
004D1623  mulss    xmm0, xmm1
004D1627  mulss    xmm3, xmm1
004D162B  addss    xmm4, xmm2
004D162F  movss    dword ptr [rip + 0x1b93645], xmm1  ; -> 02064C7C
004D1637  addss    xmm6, xmm0
004D163B  movss    xmm1, dword ptr [rip + 0x1b9366d]  ; -> 02064CB0
004D1643  mulss    xmm1, xmm8
004D1648  movss    dword ptr [rip + 0x1b93650], xmm3  ; -> 02064CA0
004D1650  movss    dword ptr [rip + 0x1b9364c], xmm2  ; -> 02064CA4
004D1658  addss    xmm1, xmm3
004D165C  movss    dword ptr [rip + 0x1b93644], xmm0  ; -> 02064CA8
004D1664  jmp      0x4d167e  ; -> 004D167E
004D1666  movss    xmm6, dword ptr [rip + 0x1b9364a]  ; -> 02064CB8
004D166E  movss    xmm4, dword ptr [rip + 0x1b9363e]  ; -> 02064CB4
004D1676  movss    xmm1, dword ptr [rip + 0x1b93632]  ; -> 02064CB0
004D167E  movss    xmm9, dword ptr [rip + 0x1b93635]  ; -> 02064CBC
004D1687  movaps   xmm0, xmm4
004D168A  mulss    xmm0, dword ptr [rip + 0x1b9354e]  ; -> 02064BE0
004D1692  movss    xmm2, dword ptr [rip + 0x1b93536]  ; -> 02064BD0
004D169A  movss    xmm3, dword ptr [rip + 0x1b93532]  ; -> 02064BD4
004D16A2  movss    xmm5, dword ptr [rip + 0x1b9352e]  ; -> 02064BD8
004D16AA  mulss    xmm2, xmm1
004D16AE  mulss    xmm3, xmm1
004D16B2  addss    xmm2, xmm0
004D16B6  mulss    xmm5, xmm1
004D16BA  movss    xmm0, dword ptr [rip + 0x1b9352e]  ; -> 02064BF0
004D16C2  movss    xmm1, dword ptr [rip + 0x1b9351a]  ; -> 02064BE4
004D16CA  mulss    xmm0, xmm6
004D16CE  mulss    xmm1, xmm4
004D16D2  mulss    xmm4, dword ptr [rip + 0x1b9350e]  ; -> 02064BE8
004D16DA  addss    xmm2, xmm0
004D16DE  movss    xmm0, dword ptr [rip + 0x1b9351a]  ; -> 02064C00
004D16E6  addss    xmm3, xmm1
004D16EA  mulss    xmm0, xmm9
004D16EF  movaps   xmm1, xmm6
004D16F2  mulss    xmm1, dword ptr [rip + 0x1b934fa]  ; -> 02064BF4
004D16FA  addss    xmm5, xmm4
004D16FE  movss    xmm4, dword ptr [rip + 0x1b934fe]  ; -> 02064C04
004D1706  addss    xmm0, xmm2
004D170A  mulss    xmm6, dword ptr [rip + 0x1b934e6]  ; -> 02064BF8
004D1712  addss    xmm3, xmm1
004D1716  mulss    xmm4, xmm9
004D171B  movaps   xmm7, xmm0
004D171E  movss    dword ptr [rip + 0x1b9358a], xmm0  ; -> 02064CB0
004D1726  movups   xmm0, xmmword ptr [rip + 0x1b934e3]  ; -> 02064C10
004D172D  addss    xmm5, xmm6
004D1731  shufps   xmm7, xmm7, 0
004D1735  movss    xmm6, dword ptr [rip + 0x1b934cb]  ; -> 02064C08
004D173D  addss    xmm4, xmm3
004D1741  mulps    xmm7, xmm0
004D1744  mulss    xmm6, xmm9
004D1749  movaps   xmm0, xmm4
004D174C  movss    dword ptr [rip + 0x1b93560], xmm4  ; -> 02064CB4
004D1754  mulss    xmm0, dword ptr [rip + 0x1b934c4]  ; -> 02064C20
004D175C  movaps   xmm1, xmm4
004D175F  mulss    xmm1, dword ptr [rip + 0x1b934c1]  ; -> 02064C28
004D1767  addss    xmm6, xmm5
004D176B  movups   xmmword ptr [rip + 0x1b933ae], xmm7  ; -> 02064B20
004D1772  movss    xmm2, dword ptr [rip + 0x1b933aa]  ; -> 02064B24
004D177A  addss    xmm7, xmm0
004D177E  movss    xmm3, dword ptr [rip + 0x1b933a2]  ; -> 02064B28
004D1786  movaps   xmm0, xmm4
004D1789  mulss    xmm0, dword ptr [rip + 0x1b93493]  ; -> 02064C24
004D1791  addss    xmm3, xmm1
004D1795  movss    xmm1, dword ptr [rip + 0x1b93497]  ; -> 02064C34
004D179D  movss    xmm5, dword ptr [rip + 0x1b93387]  ; -> 02064B2C
004D17A5  mulss    xmm4, dword ptr [rip + 0x1b9347f]  ; -> 02064C2C
004D17AD  addss    xmm2, xmm0
004D17B1  mulss    xmm1, xmm6
004D17B5  movaps   xmm0, xmm6
004D17B8  mulss    xmm0, dword ptr [rip + 0x1b93470]  ; -> 02064C30
004D17C0  addss    xmm5, xmm4
004D17C4  addss    xmm2, xmm1
004D17C8  movss    dword ptr [rip + 0x1b934e8], xmm6  ; -> 02064CB8
004D17D0  movss    xmm1, dword ptr [rip + 0x1b93464]  ; -> 02064C3C
004D17D8  addss    xmm7, xmm0
004D17DC  mulss    xmm1, xmm6
004D17E0  movss    xmm0, dword ptr [rip + 0x1b93450]  ; -> 02064C38
004D17E8  mulss    xmm0, xmm6
004D17EC  addss    xmm5, xmm1
004D17F0  movss    dword ptr [rip + 0x1b9332c], xmm2  ; -> 02064B24
004D17F8  movaps   xmm1, xmm9
004D17FC  movss    dword ptr [rip + 0x1b9331c], xmm7  ; -> 02064B20
004D1804  mulss    xmm1, dword ptr [rip + 0x1b93438]  ; -> 02064C44
004D180C  addss    xmm3, xmm0
004D1810  movaps   xmm0, xmm9
004D1814  mulss    xmm0, dword ptr [rip + 0x1b93424]  ; -> 02064C40
004D181C  addss    xmm1, xmm2
004D1820  movss    dword ptr [rip + 0x1b93304], xmm5  ; -> 02064B2C
004D1828  movss    dword ptr [rip + 0x1b932f8], xmm3  ; -> 02064B28
004D1830  addss    xmm0, xmm7
004D1834  movss    dword ptr [rip + 0x1b93488], xmm1  ; -> 02064CC4
004D183C  movss    dword ptr [rip + 0x1b9347c], xmm0  ; -> 02064CC0
004D1844  movaps   xmm0, xmm9
004D1848  mulss    xmm0, dword ptr [rip + 0x1b933f8]  ; -> 02064C48
004D1850  addss    xmm0, xmm3
004D1854  mulss    xmm9, dword ptr [rip + 0x1b933ef]  ; -> 02064C4C
004D185D  movss    dword ptr [rip + 0x1b93463], xmm0  ; -> 02064CC8
004D1865  addss    xmm9, xmm5
004D186A  ucomiss  xmm9, xmm10
004D186E  movss    dword ptr [rip + 0x1b93455], xmm9  ; -> 02064CCC
004D1877  jp       0x4d1881  ; -> 004D1881
004D1879  jne      0x4d1881  ; -> 004D1881
004D187B  movaps   xmm0, xmm12
004D187F  jmp      0x4d188a  ; -> 004D188A
004D1881  movaps   xmm0, xmm11
004D1885  divss    xmm0, xmm9
004D188A  movups   xmm1, xmmword ptr [rip + 0x1b9342f]  ; -> 02064CC0
004D1891  lea      eax, [r9 + 0x2bc]
004D1898  inc      r11w
004D189C  addss    xmm14, dword ptr [rip + 0x1b933cf]  ; -> 02064C74
004D18A5  movups   xmm2, xmmword ptr [rip + 0x1b933c4]  ; -> 02064C70
004D18AC  shl      eax, 4
004D18AF  movss    xmm3, dword ptr [rsp + 0x130]
004D18B8  movsxd   rcx, eax
004D18BB  lea      eax, [r9 + 0x64]
004D18BF  movss    dword ptr [rip + 0x1b93239], xmm0  ; -> 02064B00
004D18C7  shufps   xmm0, xmm0, 0
004D18CB  mulps    xmm1, xmm0
004D18CE  shl      eax, 4
004D18D1  movups   xmm0, xmmword ptr [rip + 0x1b933d8]  ; -> 02064CB0
004D18D8  movups   xmmword ptr [rcx + rbp], xmm0
004D18DC  movsxd   rcx, eax
004D18DF  movups   xmmword ptr [rip + 0x1b933da], xmm1  ; -> 02064CC0
004D18E6  movups   xmmword ptr [rcx + rbp], xmm1
004D18EA  movss    xmm1, dword ptr [rip + 0x1b93382]  ; -> 02064C74
004D18F2  cmp      r8w, dx
004D18F6  jne      0x4d14e0  ; -> 004D14E0
004D18FC  movsd    xmm15, qword ptr [rip + 0x181a47b]  ; -> 01CEBD80 [u64 0x7FFFFFFFFFFFFFFF]
004D1905  add      di, dx
004D1908  movsx    eax, r10w
004D190C  sub      ax, 2
004D1910  mov      word ptr [rip + 0x1b934a8], r10w  ; -> 02064DC0
004D1918  add      ax, dx
004D191B  mov      word ptr [rip + 0x1b934b6], di  ; -> 02064DD8
004D1922  mov      word ptr [rip + 0x1b934ab], ax  ; -> 02064DD4
004D1929  movsx    edx, di
004D192C  lea      eax, [rdx + 0x64]
004D192F  shl      eax, 4
004D1932  movsxd   rcx, eax
004D1935  lea      eax, [rdx + 0x65]
004D1938  shl      eax, 4
004D193B  movups   xmm1, xmmword ptr [rcx + rbp]
004D193F  movsxd   rcx, eax
004D1942  movdqu   xmmword ptr [rip + 0x1b93316], xmm1  ; -> 02064C60
004D194A  movups   xmm0, xmmword ptr [rcx + rbp]
004D194E  movups   xmm2, xmm0
004D1951  movups   xmmword ptr [rip + 0x1b93318], xmm0  ; -> 02064C70
004D1958  movss    dword ptr [rip + 0x1b93310], xmm2  ; -> 02064C70
004D1960  subss    xmm0, xmm1
004D1964  shufps   xmm2, xmm2, 0x55
004D1968  movss    dword ptr [rip + 0x1b93304], xmm2  ; -> 02064C74
004D1970  subss    xmm2, dword ptr [rip + 0x1b932ec]  ; -> 02064C64
004D1978  ucomiss  xmm0, xmm10
004D197C  movss    dword ptr [rip + 0x1b932e0], xmm2  ; -> 02064C64
004D1984  movss    dword ptr [rip + 0x1b932d4], xmm0  ; -> 02064C60
004D198C  jp       0x4d1990  ; -> 004D1990
004D198E  je       0x4d1998  ; -> 004D1998
004D1990  ucomiss  xmm2, xmm10
004D1994  jp       0x4d19ad  ; -> 004D19AD
004D1996  jne      0x4d19ad  ; -> 004D19AD
004D1998  call     0x22cc40  ; -> 0022CC40 fn
004D199D  movss    xmm2, dword ptr [rip + 0x1b932bf]  ; -> 02064C64
004D19A5  movss    xmm0, dword ptr [rip + 0x1b932b3]  ; -> 02064C60
004D19AD  comiss   xmm10, xmm0
004D19B1  ja       0x4d19b9  ; -> 004D19B9
004D19B3  comiss   xmm10, xmm2
004D19B7  jbe      0x4d19be  ; -> 004D19BE
004D19B9  call     0x22cc30  ; -> 0022CC30 fn
004D19BE  call     0x22cc20  ; -> 0022CC20 fn
004D19C3  movss    xmm7, dword ptr [rip + 0x1930e65]  ; -> 01E02830 [u32 0x00000000]
004D19CB  movss    xmm8, dword ptr [rip + 0x1930e60]  ; -> 01E02834 [u32 0x00000000]
004D19D4  subss    xmm7, dword ptr [rip + 0x1b93288]  ; -> 02064C64
004D19DC  subss    xmm8, dword ptr [rip + 0x1b9327b]  ; -> 02064C60
004D19E5  movss    xmm6, dword ptr [rip + 0x1930e4f]  ; -> 01E0283C [f32 1]
004D19ED  movaps   xmm1, xmm7
004D19F0  mulss    xmm1, xmm7
004D19F4  movaps   xmm0, xmm8
004D19F8  mulss    xmm0, xmm8
004D19FD  movss    dword ptr [rip + 0x1b9327b], xmm1  ; -> 02064C80
004D1A05  mulss    xmm1, xmm6
004D1A09  movss    dword ptr [rip + 0x1b93273], xmm0  ; -> 02064C84
004D1A11  mulss    xmm0, xmm6
004D1A15  movss    dword ptr [rip + 0x1b9310f], xmm1  ; -> 02064B2C
004D1A1D  addss    xmm0, xmm1
004D1A21  movss    dword ptr [rip + 0x1b93263], xmm0  ; -> 02064C8C
004D1A29  cvtps2pd xmm0, xmm0
004D1A2C  andps    xmm0, xmm15
004D1A30  cvtpd2ps xmm0, xmm0
004D1A34  call     0x861f14  ; -> 00861F14 fn
004D1A39  ucomiss  xmm0, xmm10
004D1A3D  jp       0x4d1a47  ; -> 004D1A47
004D1A3F  jne      0x4d1a47  ; -> 004D1A47
004D1A41  movaps   xmm6, xmm12
004D1A45  jmp      0x4d1a4b  ; -> 004D1A4B
004D1A47  divss    xmm6, xmm0
004D1A4B  movsx    edx, word ptr [rip + 0x1b93386]  ; -> 02064DD8
004D1A52  movzx    r8d, word ptr [rip + 0x1b930b2]  ; -> 02064B0C
004D1A5A  mulss    xmm7, xmm6
004D1A5E  lea      eax, [rdx + 0x352]
004D1A64  mulss    xmm8, xmm6
004D1A69  shl      eax, 4
004D1A6C  inc      dx
004D1A6F  cmp      r8w, word ptr [rip + 0x1b9335d]  ; -> 02064DD4
004D1A77  movsxd   rcx, eax
004D1A7A  movss    dword ptr [rip + 0x1b9321e], xmm7  ; -> 02064CA0
004D1A82  movss    dword ptr [rip + 0x1b93219], xmm8  ; -> 02064CA4
004D1A8B  movups   xmm1, xmmword ptr [rip + 0x1b9320e]  ; -> 02064CA0
004D1A92  mov      word ptr [rip + 0x1b9333f], dx  ; -> 02064DD8
004D1A99  movss    dword ptr [rip + 0x1b9305f], xmm6  ; -> 02064B00
004D1AA1  movups   xmmword ptr [rcx + rbp], xmm1
004D1AA5  je       0x4d1cf4  ; -> 004D1CF4
004D1AAB  nop      dword ptr [rax + rax]
004D1AB0  movsx    edx, dx
004D1AB3  lea      eax, [rdx + 0x64]
004D1AB6  shl      eax, 4
004D1AB9  movsxd   rcx, eax
004D1ABC  lea      eax, [rdx + 0x65]
004D1ABF  shl      eax, 4
004D1AC2  movups   xmm1, xmmword ptr [rcx + rbp]
004D1AC6  movsxd   rcx, eax
004D1AC9  movdqu   xmmword ptr [rip + 0x1b9318f], xmm1  ; -> 02064C60
004D1AD1  movups   xmm0, xmmword ptr [rcx + rbp]
004D1AD5  movups   xmm2, xmm0
004D1AD8  movups   xmmword ptr [rip + 0x1b93191], xmm0  ; -> 02064C70
004D1ADF  movss    dword ptr [rip + 0x1b93189], xmm2  ; -> 02064C70
004D1AE7  subss    xmm0, xmm1
004D1AEB  shufps   xmm2, xmm2, 0x55
004D1AEF  movss    dword ptr [rip + 0x1b9317d], xmm2  ; -> 02064C74
004D1AF7  subss    xmm2, dword ptr [rip + 0x1b93165]  ; -> 02064C64
004D1AFF  ucomiss  xmm0, xmm10
004D1B03  movss    dword ptr [rip + 0x1b93159], xmm2  ; -> 02064C64
004D1B0B  movss    dword ptr [rip + 0x1b9314d], xmm0  ; -> 02064C60
004D1B13  jp       0x4d1b17  ; -> 004D1B17
004D1B15  je       0x4d1b1f  ; -> 004D1B1F
004D1B17  ucomiss  xmm2, xmm10
004D1B1B  jp       0x4d1b34  ; -> 004D1B34
004D1B1D  jne      0x4d1b34  ; -> 004D1B34
004D1B1F  call     0x22cc40  ; -> 0022CC40 fn
004D1B24  movss    xmm2, dword ptr [rip + 0x1b93138]  ; -> 02064C64
004D1B2C  movss    xmm0, dword ptr [rip + 0x1b9312c]  ; -> 02064C60
004D1B34  comiss   xmm10, xmm0
004D1B38  ja       0x4d1b40  ; -> 004D1B40
004D1B3A  comiss   xmm10, xmm2
004D1B3E  jbe      0x4d1b45  ; -> 004D1B45
004D1B40  call     0x22cc30  ; -> 0022CC30 fn
004D1B45  call     0x22cc20  ; -> 0022CC20 fn
004D1B4A  movss    xmm7, dword ptr [rip + 0x1930cde]  ; -> 01E02830 [u32 0x00000000]
004D1B52  movss    xmm8, dword ptr [rip + 0x1930cd9]  ; -> 01E02834 [u32 0x00000000]
004D1B5B  subss    xmm7, dword ptr [rip + 0x1b93101]  ; -> 02064C64
004D1B63  subss    xmm8, dword ptr [rip + 0x1b930f4]  ; -> 02064C60
004D1B6C  movss    xmm6, dword ptr [rip + 0x1930cc8]  ; -> 01E0283C [f32 1]
004D1B74  movzx    ebx, word ptr [rip + 0x1b93259]  ; -> 02064DD4
004D1B7B  dec      bx
004D1B7E  movaps   xmm1, xmm7
004D1B81  mov      word ptr [rip + 0x1b9324c], bx  ; -> 02064DD4
004D1B88  movaps   xmm0, xmm8
004D1B8C  mulss    xmm1, xmm7
004D1B90  mulss    xmm0, xmm8
004D1B95  mulss    xmm1, xmm6
004D1B99  mulss    xmm0, xmm6
004D1B9D  addss    xmm0, xmm1
004D1BA1  cvtps2pd xmm0, xmm0
004D1BA4  andps    xmm0, xmm15
004D1BA8  cvtpd2ps xmm0, xmm0
004D1BAC  call     0x861f14  ; -> 00861F14 fn
004D1BB1  movaps   xmm1, xmm0
004D1BB4  ucomiss  xmm1, xmm10
004D1BB8  jp       0x4d1bc2  ; -> 004D1BC2
004D1BBA  jne      0x4d1bc2  ; -> 004D1BC2
004D1BBC  movaps   xmm0, xmm12
004D1BC0  jmp      0x4d1bc9  ; -> 004D1BC9
004D1BC2  movaps   xmm0, xmm6
004D1BC5  divss    xmm0, xmm1
004D1BC9  movss    xmm11, dword ptr [rip + 0x1b930d2]  ; -> 02064CA4
004D1BD2  mulss    xmm7, xmm0
004D1BD6  mulss    xmm8, xmm0
004D1BDB  movaps   xmm9, xmm7
004D1BDF  movss    dword ptr [rip + 0x1b930a9], xmm7  ; -> 02064C90
004D1BE7  addss    xmm9, dword ptr [rip + 0x1b930b0]  ; -> 02064CA0
004D1BF0  addss    xmm11, xmm8
004D1BF5  movss    dword ptr [rip + 0x1b93096], xmm8  ; -> 02064C94
004D1BFE  movaps   xmm1, xmm9
004D1C02  mulss    xmm1, xmm9
004D1C07  movaps   xmm0, xmm11
004D1C0B  mulss    xmm0, xmm11
004D1C10  movss    dword ptr [rip + 0x1b93068], xmm1  ; -> 02064C80
004D1C18  mulss    xmm1, xmm6
004D1C1C  movss    dword ptr [rip + 0x1b93060], xmm0  ; -> 02064C84
004D1C24  mulss    xmm0, xmm6
004D1C28  movss    dword ptr [rip + 0x1b92efc], xmm1  ; -> 02064B2C
004D1C30  addss    xmm0, xmm1
004D1C34  movss    dword ptr [rip + 0x1b93050], xmm0  ; -> 02064C8C
004D1C3C  cvtps2pd xmm0, xmm0
004D1C3F  andps    xmm0, xmm15
004D1C43  cvtpd2ps xmm0, xmm0
004D1C47  call     0x861f14  ; -> 00861F14 fn
004D1C4C  ucomiss  xmm0, xmm10
004D1C50  jp       0x4d1c5a  ; -> 004D1C5A
004D1C52  jne      0x4d1c5a  ; -> 004D1C5A
004D1C54  movaps   xmm6, xmm12
004D1C58  jmp      0x4d1c5e  ; -> 004D1C5E
004D1C5A  divss    xmm6, xmm0
004D1C5E  movsx    edx, word ptr [rip + 0x1b93173]  ; -> 02064DD8
004D1C65  movzx    r8d, word ptr [rip + 0x1b92e9f]  ; -> 02064B0C
004D1C6D  movss    xmm1, dword ptr [rip + 0x1b93027]  ; -> 02064C9C
004D1C75  mulss    xmm9, xmm6
004D1C7A  lea      eax, [rdx + 0x352]
004D1C80  inc      dx
004D1C83  mulss    xmm11, xmm6
004D1C88  shl      eax, 4
004D1C8B  movsxd   rcx, eax
004D1C8E  movss    dword ptr [rip + 0x1b92fd9], xmm9  ; -> 02064C70
004D1C97  movss    dword ptr [rip + 0x1b92fd4], xmm11  ; -> 02064C74
004D1CA0  movss    dword ptr [rip + 0x1b92e58], xmm6  ; -> 02064B00
004D1CA8  movss    dword ptr [rip + 0x1b92ff0], xmm7  ; -> 02064CA0
004D1CB0  movss    dword ptr [rip + 0x1b92feb], xmm8  ; -> 02064CA4
004D1CB9  movss    dword ptr [rip + 0x1b92feb], xmm1  ; -> 02064CAC
004D1CC1  mov      word ptr [rip + 0x1b93110], dx  ; -> 02064DD8
004D1CC8  movups   xmm0, xmmword ptr [rip + 0x1b92fa1]  ; -> 02064C70
004D1CCF  movups   xmmword ptr [rcx + rbp], xmm0
004D1CD3  movss    xmm0, dword ptr [rip + 0x1b92fbd]  ; -> 02064C98
004D1CDB  movss    dword ptr [rip + 0x1b92fc5], xmm0  ; -> 02064CA8
004D1CE3  cmp      r8w, bx
004D1CE7  jne      0x4d1ab0  ; -> 004D1AB0
004D1CED  movups   xmm1, xmmword ptr [rip + 0x1b92fac]  ; -> 02064CA0
004D1CF4  movsx    ebx, r8w
004D1CF8  mov      r14d, 0xe0
004D1CFE  movsx    eax, dx
004D1D01  add      eax, 0x352
004D1D06  shl      eax, 4
004D1D09  movsxd   rcx, eax
004D1D0C  lea      eax, [rbx + 0x1f]
004D1D0F  shl      eax, 4
004D1D12  movups   xmmword ptr [rcx + rbp], xmm1
004D1D16  movsxd   rcx, eax
004D1D19  lea      eax, [rbx + 0x1e]
004D1D1C  shl      eax, 4
004D1D1F  movups   xmm0, xmmword ptr [rcx + rbp]
004D1D23  movsxd   rcx, eax
004D1D26  movsx    eax, word ptr [rip + 0x1b93093]  ; -> 02064DC0
004D1D2D  movdqu   xmmword ptr [rip + 0x1b92ecb], xmm0  ; -> 02064C00
004D1D35  add      ax, r8w
004D1D39  movups   xmm5, xmm0
004D1D3C  mov      word ptr [rip + 0x1b93091], ax  ; -> 02064DD4
004D1D43  movups   xmm1, xmmword ptr [rcx + rbp]
004D1D47  add      bx, r8w
004D1D4B  shufps   xmm5, xmm5, 0xaa
004D1D4F  shufps   xmm0, xmm0, 0xff
004D1D53  subss    xmm0, xmm5
004D1D57  movss    dword ptr [rip + 0x1b92ea9], xmm5  ; -> 02064C08
004D1D5F  movdqu   xmmword ptr [rip + 0x1b92e59], xmm1  ; -> 02064BC0
004D1D67  mov      word ptr [rip + 0x1b9306a], bx  ; -> 02064DD8
004D1D6E  shufps   xmm1, xmm1, 0x55
004D1D72  mulss    xmm0, xmm1
004D1D76  movss    dword ptr [rip + 0x1b92e8e], xmm0  ; -> 02064C0C
004D1D7E  nop      
004D1D80  movsx    edx, bx
004D1D83  lea      eax, [rdx + 0x352]
004D1D89  shl      eax, 4
004D1D8C  movsxd   rcx, eax
004D1D8F  lea      eax, [rdx + 0x2bc]
004D1D95  shl      eax, 4
004D1D98  movups   xmm3, xmmword ptr [rcx + rbp]
004D1D9C  movsxd   rcx, eax
004D1D9F  movups   xmmword ptr [rip + 0x1b92eca], xmm3  ; -> 02064C70
004D1DA6  movups   xmm4, xmmword ptr [rcx + rbp]
004D1DAA  movss    xmm2, dword ptr [rip + 0x1b92ebe]  ; -> 02064C70
004D1DB2  mulss    xmm2, xmm5
004D1DB6  movdqu   xmmword ptr [rip + 0x1b92ea2], xmm4  ; -> 02064C60
004D1DBE  shufps   xmm3, xmm3, 0x55
004D1DC2  movaps   xmm0, xmm2
004D1DC5  mulss    xmm3, xmm5
004D1DC9  addss    xmm0, xmm4
004D1DCD  movaps   xmm5, xmm4
004D1DD0  movss    dword ptr [rip + 0x1b92e88], xmm4  ; -> 02064C60
004D1DD8  shufps   xmm5, xmm4, 0x55
004D1DDC  movaps   xmm1, xmm3
004D1DDF  movss    dword ptr [rip + 0x1b92e7d], xmm5  ; -> 02064C64
004D1DE7  addss    xmm1, xmm5
004D1DEB  movss    dword ptr [rip + 0x1b92e8d], xmm0  ; -> 02064C80
004D1DF3  movaps   xmm0, xmm4
004D1DF6  movss    dword ptr [rip + 0x1b92e76], xmm3  ; -> 02064C74
004D1DFE  shufps   xmm0, xmm4, 0xaa
004D1E02  subss    xmm5, xmm3
004D1E06  movss    dword ptr [rip + 0x1b92e62], xmm2  ; -> 02064C70
004D1E0E  movss    dword ptr [rip + 0x1b92e52], xmm0  ; -> 02064C68
004D1E16  movss    dword ptr [rip + 0x1b92e66], xmm1  ; -> 02064C84
004D1E1E  movaps   xmm1, xmm4
004D1E21  shufps   xmm1, xmm4, 0xff
004D1E25  subss    xmm4, xmm2
004D1E29  movss    dword ptr [rip + 0x1b92e67], xmm0  ; -> 02064C98
004D1E31  movss    dword ptr [rip + 0x1b92e33], xmm1  ; -> 02064C6C
004D1E39  movss    dword ptr [rip + 0x1b92e5b], xmm1  ; -> 02064C9C
004D1E41  movss    dword ptr [rip + 0x1b92e4b], xmm5  ; -> 02064C94
004D1E49  ucomiss  xmm4, xmm10
004D1E4D  movss    dword ptr [rip + 0x1b92e3b], xmm4  ; -> 02064C90
004D1E55  jp       0x4d1e59  ; -> 004D1E59
004D1E57  je       0x4d1e61  ; -> 004D1E61
004D1E59  ucomiss  xmm5, xmm10
004D1E5D  jp       0x4d1e76  ; -> 004D1E76
004D1E5F  jne      0x4d1e76  ; -> 004D1E76
004D1E61  call     0x22cc40  ; -> 0022CC40 fn
004D1E66  movss    xmm5, dword ptr [rip + 0x1b92e26]  ; -> 02064C94
004D1E6E  movss    xmm4, dword ptr [rip + 0x1b92e1a]  ; -> 02064C90
004D1E76  comiss   xmm10, xmm4
004D1E7A  ja       0x4d1e82  ; -> 004D1E82
004D1E7C  comiss   xmm10, xmm5
004D1E80  jbe      0x4d1e87  ; -> 004D1E87
004D1E82  call     0x22cc30  ; -> 0022CC30 fn
004D1E87  call     0x22cc20  ; -> 0022CC20 fn
004D1E8C  movss    xmm2, dword ptr [rip + 0x1b92dd0]  ; -> 02064C64
004D1E94  movss    xmm6, dword ptr [rip + 0x1b92dd0]  ; -> 02064C6C
004D1E9C  movaps   xmm0, xmm2
004D1E9F  mulss    xmm0, dword ptr [rip + 0x1b92d79]  ; -> 02064C20
004D1EA7  movaps   xmm1, xmm2
004D1EAA  mulss    xmm1, dword ptr [rip + 0x1b92d76]  ; -> 02064C28
004D1EB2  movaps   xmm13, xmm6
004D1EB6  movss    xmm5, dword ptr [rip + 0x1b92da2]  ; -> 02064C60
004D1EBE  movaps   xmm7, xmm6
004D1EC1  movups   xmm8, xmmword ptr [rip + 0x1b92d47]  ; -> 02064C10
004D1EC9  mulss    xmm13, dword ptr [rip + 0x1b92d76]  ; -> 02064C48
004D1ED2  movaps   xmm11, xmm6
004D1ED6  mulss    xmm6, dword ptr [rip + 0x1b92d6e]  ; -> 02064C4C
004D1EDE  mulss    xmm7, dword ptr [rip + 0x1b92d5a]  ; -> 02064C40
004D1EE6  mulss    xmm11, dword ptr [rip + 0x1b92d55]  ; -> 02064C44
004D1EEF  movss    xmm9, dword ptr [rip + 0x1930944]  ; -> 01E0283C [f32 1]
004D1EF8  movaps   xmm14, xmm7
004D1EFC  shufps   xmm5, xmm5, 0
004D1F00  mulps    xmm5, xmm8
004D1F04  movaps   xmm15, xmm11
004D1F08  movups   xmmword ptr [rip + 0x1b92c11], xmm5  ; -> 02064B20
004D1F0F  movss    xmm4, dword ptr [rip + 0x1b92c11]  ; -> 02064B28
004D1F17  addss    xmm5, xmm0
004D1F1B  movss    xmm3, dword ptr [rip + 0x1b92c01]  ; -> 02064B24
004D1F23  addss    xmm4, xmm1
004D1F27  movss    xmm1, dword ptr [rip + 0x1b92bfd]  ; -> 02064B2C
004D1F2F  movaps   xmm0, xmm2
004D1F32  mulss    xmm2, dword ptr [rip + 0x1b92cf2]  ; -> 02064C2C
004D1F3A  mulss    xmm0, dword ptr [rip + 0x1b92ce2]  ; -> 02064C24
004D1F42  addss    xmm1, xmm2
004D1F46  movss    xmm2, dword ptr [rip + 0x1b92ce2]  ; -> 02064C30
004D1F4E  addss    xmm3, xmm0
004D1F52  movss    xmm0, dword ptr [rip + 0x1b92d0e]  ; -> 02064C68
004D1F5A  mulss    xmm2, xmm0
004D1F5E  addss    xmm5, xmm2
004D1F62  movss    dword ptr [rsp + 0x130], xmm2
004D1F6B  movss    xmm2, dword ptr [rip + 0x1b92cc1]  ; -> 02064C34
004D1F73  movss    dword ptr [rsp + 0x2c], xmm2
004D1F79  mulss    xmm2, xmm0
004D1F7D  addss    xmm14, xmm5
004D1F82  addss    xmm3, xmm2
004D1F86  movss    dword ptr [rsp + 0x138], xmm2
004D1F8F  movss    xmm2, dword ptr [rip + 0x1b92ca1]  ; -> 02064C38
004D1F97  movss    dword ptr [rsp + 0x30], xmm2
004D1F9D  mulss    xmm2, xmm0
004D1FA1  addss    xmm15, xmm3
004D1FA6  addss    xmm4, xmm2
004D1FAA  movss    dword ptr [rsp + 0x20], xmm2
004D1FB0  movss    xmm2, dword ptr [rip + 0x1b92c84]  ; -> 02064C3C
004D1FB8  movss    dword ptr [rsp + 0x34], xmm2
004D1FBE  mulss    xmm2, xmm0
004D1FC2  movaps   xmm0, xmm13
004D1FC6  addss    xmm0, xmm4
004D1FCA  addss    xmm1, xmm2
004D1FCE  movss    dword ptr [rsp + 0x24], xmm2
004D1FD4  movss    dword ptr [rsp + 0x28], xmm0
004D1FDA  addss    xmm1, xmm6
004D1FDE  ucomiss  xmm1, xmm10
004D1FE2  jp       0x4d1fec  ; -> 004D1FEC
004D1FE4  jne      0x4d1fec  ; -> 004D1FEC
004D1FE6  movaps   xmm5, xmm12
004D1FEA  jmp      0x4d1ff4  ; -> 004D1FF4
004D1FEC  movaps   xmm5, xmm9
004D1FF0  divss    xmm5, xmm1
004D1FF4  movss    xmm2, dword ptr [rip + 0x1b92c88]  ; -> 02064C84
004D1FFC  movss    xmm4, dword ptr [rip + 0x1b92c7c]  ; -> 02064C80
004D2004  movaps   xmm0, xmm2
004D2007  mulss    xmm0, dword ptr [rip + 0x1b92c11]  ; -> 02064C20
004D200F  movaps   xmm1, xmm2
004D2012  mulss    xmm1, dword ptr [rip + 0x1b92c0e]  ; -> 02064C28
004D201A  shufps   xmm4, xmm4, 0
004D201E  mulps    xmm4, xmm8
004D2022  mulss    xmm14, xmm5
004D2027  mulss    xmm15, xmm5
004D202C  movups   xmmword ptr [rip + 0x1b92aed], xmm4  ; -> 02064B20
004D2033  movss    xmm3, dword ptr [rip + 0x1b92ae9]  ; -> 02064B24
004D203B  addss    xmm4, xmm0
004D203F  movss    xmm8, dword ptr [rip + 0x1b92ae4]  ; -> 02064B2C
004D2048  movaps   xmm0, xmm2
004D204B  mulss    xmm0, dword ptr [rip + 0x1b92bd1]  ; -> 02064C24
004D2053  mulss    xmm2, dword ptr [rip + 0x1b92bd1]  ; -> 02064C2C
004D205B  addss    xmm4, dword ptr [rsp + 0x130]
004D2064  addss    xmm3, xmm0
004D2068  movss    dword ptr [rip + 0x1b92bef], xmm14  ; -> 02064C60
004D2071  movss    xmm0, dword ptr [rip + 0x1b92aaf]  ; -> 02064B28
004D2079  addss    xmm8, xmm2
004D207E  movss    xmm2, dword ptr [rip + 0x1b92c0e]  ; -> 02064C94
004D2086  addss    xmm0, xmm1
004D208A  movaps   xmm1, xmm2
004D208D  movss    dword ptr [rip + 0x1b92bce], xmm15  ; -> 02064C64
004D2096  mulss    xmm1, dword ptr [rip + 0x1b92b8a]  ; -> 02064C28
004D209E  addss    xmm7, xmm4
004D20A2  addss    xmm3, dword ptr [rsp + 0x138]
004D20AB  addss    xmm0, dword ptr [rsp + 0x20]
004D20B1  addss    xmm8, dword ptr [rsp + 0x24]
004D20B8  movss    dword ptr [rip + 0x1b92bc0], xmm7  ; -> 02064C80
004D20C0  movss    xmm7, dword ptr [rip + 0x1b92bd4]  ; -> 02064C9C
004D20C8  addss    xmm11, xmm3
004D20CD  addss    xmm13, xmm0
004D20D2  movss    xmm0, dword ptr [rsp + 0x28]
004D20D8  mulss    xmm0, xmm5
004D20DC  addss    xmm8, xmm6
004D20E1  movss    xmm6, dword ptr [rip + 0x1b92ba7]  ; -> 02064C90
004D20E9  shufps   xmm6, xmm6, 0
004D20ED  movss    dword ptr [rip + 0x1b92b73], xmm0  ; -> 02064C68
004D20F5  movups   xmm0, xmmword ptr [rip + 0x1b92b14]  ; -> 02064C10
004D20FC  mulss    xmm5, xmm9
004D2101  mulps    xmm6, xmm0
004D2104  movaps   xmm0, xmm2
004D2107  mulss    xmm0, dword ptr [rip + 0x1b92b11]  ; -> 02064C20
004D210F  movss    dword ptr [rip + 0x1b92b55], xmm5  ; -> 02064C6C
004D2117  movups   xmmword ptr [rip + 0x1b92a02], xmm6  ; -> 02064B20
004D211E  movss    xmm4, dword ptr [rip + 0x1b92a02]  ; -> 02064B28
004D2126  addss    xmm6, xmm0
004D212A  movss    xmm3, dword ptr [rip + 0x1b929f2]  ; -> 02064B24
004D2132  addss    xmm4, xmm1
004D2136  movss    xmm1, dword ptr [rip + 0x1b92b5a]  ; -> 02064C98
004D213E  movaps   xmm0, xmm2
004D2141  mulss    xmm0, dword ptr [rip + 0x1b92adb]  ; -> 02064C24
004D2149  movss    xmm5, dword ptr [rip + 0x1b929db]  ; -> 02064B2C
004D2151  mulss    xmm2, dword ptr [rip + 0x1b92ad3]  ; -> 02064C2C
004D2159  addss    xmm3, xmm0
004D215D  movss    dword ptr [rip + 0x1b92b1e], xmm11  ; -> 02064C84
004D2166  movaps   xmm0, xmm1
004D2169  movss    dword ptr [rip + 0x1b92b16], xmm13  ; -> 02064C88
004D2172  mulss    xmm0, dword ptr [rip + 0x1b92ab6]  ; -> 02064C30
004D217A  addss    xmm5, xmm2
004D217E  movss    dword ptr [rip + 0x1b92b05], xmm8  ; -> 02064C8C
004D2187  addss    xmm6, xmm0
004D218B  movss    xmm0, dword ptr [rsp + 0x2c]
004D2191  mulss    xmm0, xmm1
004D2195  addss    xmm3, xmm0
004D2199  movss    dword ptr [rip + 0x1b9297f], xmm6  ; -> 02064B20
004D21A1  movss    xmm0, dword ptr [rsp + 0x30]
004D21A7  mulss    xmm0, xmm1
004D21AB  movss    dword ptr [rip + 0x1b92971], xmm3  ; -> 02064B24
004D21B3  addss    xmm4, xmm0
004D21B7  movss    xmm0, dword ptr [rsp + 0x34]
004D21BD  mulss    xmm0, xmm1
004D21C1  addss    xmm5, xmm0
004D21C5  movss    dword ptr [rip + 0x1b9295b], xmm4  ; -> 02064B28
004D21CD  movaps   xmm0, xmm7
004D21D0  mulss    xmm0, dword ptr [rip + 0x1b92a68]  ; -> 02064C40
004D21D8  movss    dword ptr [rip + 0x1b9294c], xmm5  ; -> 02064B2C
004D21E0  addss    xmm0, xmm6
004D21E4  ucomiss  xmm8, xmm10
004D21E8  movss    dword ptr [rip + 0x1b92aa0], xmm0  ; -> 02064C90
004D21F0  movaps   xmm1, xmm7
004D21F3  mulss    xmm1, dword ptr [rip + 0x1b92a49]  ; -> 02064C44
004D21FB  movaps   xmm0, xmm7
004D21FE  mulss    xmm0, dword ptr [rip + 0x1b92a42]  ; -> 02064C48
004D2206  mulss    xmm7, dword ptr [rip + 0x1b92a3e]  ; -> 02064C4C
004D220E  addss    xmm1, xmm3
004D2212  addss    xmm0, xmm4
004D2216  addss    xmm7, xmm5
004D221A  movss    dword ptr [rip + 0x1b92a72], xmm1  ; -> 02064C94
004D2222  movss    dword ptr [rip + 0x1b92a6e], xmm0  ; -> 02064C98
004D222A  movss    dword ptr [rip + 0x1b92a6a], xmm7  ; -> 02064C9C
004D2232  jp       0x4d223c  ; -> 004D223C
004D2234  jne      0x4d223c  ; -> 004D223C
004D2236  movaps   xmm2, xmm12
004D223A  jmp      0x4d2245  ; -> 004D2245
004D223C  movaps   xmm2, xmm9
004D2240  divss    xmm2, xmm8
004D2245  ucomiss  xmm7, xmm10
004D2249  movups   xmm1, xmmword ptr [rip + 0x1b92a30]  ; -> 02064C80
004D2250  movaps   xmm0, xmm2
004D2253  mulss    xmm2, xmm9
004D2258  shufps   xmm0, xmm0, 0
004D225C  mulps    xmm1, xmm0
004D225F  movups   xmmword ptr [rip + 0x1b92a1a], xmm1  ; -> 02064C80
004D2266  movss    dword ptr [rip + 0x1b92a1e], xmm2  ; -> 02064C8C
004D226E  jp       0x4d2278  ; -> 004D2278
004D2270  jne      0x4d2278  ; -> 004D2278
004D2272  movaps   xmm2, xmm12
004D2276  jmp      0x4d2280  ; -> 004D2280
004D2278  movaps   xmm2, xmm9
004D227C  divss    xmm2, xmm7
004D2280  movsx    ebx, word ptr [rip + 0x1b92b51]  ; -> 02064DD8
004D2287  xor      r10d, r10d
004D228A  movups   xmm1, xmmword ptr [rip + 0x1b929ff]  ; -> 02064C90
004D2291  movzx    edi, word ptr [rip + 0x1b92874]  ; -> 02064B0C
004D2298  movss    xmm5, dword ptr [rip + 0x1930590]  ; -> 01E02830 [u32 0x00000000]
004D22A0  movaps   xmm0, xmm2
004D22A3  movss    xmm4, dword ptr [rip + 0x1930589]  ; -> 01E02834 [u32 0x00000000]
004D22AB  lea      eax, [rbx + 0x28b]
004D22B1  shl      eax, 4
004D22B4  movsxd   rcx, eax
004D22B7  lea      r9d, [r14 + rdi]
004D22BB  shufps   xmm0, xmm0, 0
004D22BF  lea      eax, [rbx + 0xfa]
004D22C5  shl      eax, 4
004D22C8  movsxd   rsi, eax
004D22CB  movups   xmm3, xmmword ptr [rcx + rbp]
004D22CF  mov      eax, dword ptr [rip + 0x1b92993]  ; -> 02064C68
004D22D5  mulps    xmm1, xmm0
004D22D8  movsd    xmm0, qword ptr [rip + 0x1b92980]  ; -> 02064C60
004D22E0  movsd    qword ptr [rsi + rbp], xmm0
004D22E5  mov      dword ptr [rsi + rbp + 8], eax
004D22E9  lea      eax, [rbx + 0x64]
004D22EC  shl      eax, 4
004D22EF  movsxd   rcx, eax
004D22F2  movups   xmmword ptr [rip + 0x1b92997], xmm1  ; -> 02064C90
004D22F9  movss    dword ptr [rip + 0x1b927ff], xmm2  ; -> 02064B00
004D2301  mulss    xmm2, xmm9
004D2306  movss    xmm9, dword ptr [rip + 0x1b928fd]  ; -> 02064C0C
004D230F  movups   xmmword ptr [rip + 0x1b929aa], xmm3  ; -> 02064CC0
004D2316  movss    dword ptr [rip + 0x1b9297e], xmm2  ; -> 02064C9C
004D231E  movups   xmm2, xmmword ptr [rip + 0x1b9295b]  ; -> 02064C80
004D2325  mulss    xmm9, xmm3
004D232A  comiss   xmm2, dword ptr [rip + 0x1b927ff]  ; -> 02064B30
004D2331  movss    xmm3, dword ptr [rip + 0x19304ff]  ; -> 01E02838 [u32 0x00000000]
004D2339  movaps   xmm1, xmm2
004D233C  shufps   xmm1, xmm2, 0x55
004D2340  movaps   xmm0, xmm2
004D2343  seta     r10b
004D2347  shufps   xmm0, xmm2, 0xaa
004D234B  xor      eax, eax
004D234D  movss    dword ptr [rip + 0x1b9292b], xmm2  ; -> 02064C80
004D2355  add      r10w, r10w
004D2359  movss    dword ptr [rip + 0x1b92923], xmm1  ; -> 02064C84
004D2361  comiss   xmm1, dword ptr [rip + 0x1b927cc]  ; -> 02064B34
004D2368  movups   xmmword ptr [rcx + rbp], xmm2
004D236C  seta     al
004D236F  movss    dword ptr [rip + 0x1b92911], xmm0  ; -> 02064C88
004D2377  add      r10w, ax
004D237B  movss    dword ptr [rip + 0x1b92948], xmm9  ; -> 02064CCC
004D2384  xor      eax, eax
004D2386  add      r10w, r10w
004D238A  comiss   xmm0, dword ptr [rip + 0x1b927a7]  ; -> 02064B38
004D2391  seta     al
004D2394  xor      edx, edx
004D2396  add      r10w, ax
004D239A  shl      r10w, 5
004D239F  and      r10w, r9w
004D23A3  comiss   xmm5, xmm2
004D23A6  movss    xmm2, dword ptr [rip + 0x1b928e2]  ; -> 02064C90
004D23AE  seta     dl
004D23B1  xor      eax, eax
004D23B3  add      dx, dx
004D23B6  comiss   xmm4, xmm1
004D23B9  movss    xmm1, dword ptr [rip + 0x1b928d3]  ; -> 02064C94
004D23C1  seta     al
004D23C4  add      dx, ax
004D23C7  xor      eax, eax
004D23C9  add      dx, dx
004D23CC  comiss   xmm3, xmm0
004D23CF  seta     al
004D23D2  xor      r8d, r8d
004D23D5  add      dx, ax
004D23D8  shl      dx, 5
004D23DC  and      dx, r9w
004D23E0  comiss   xmm2, dword ptr [rip + 0x1b92749]  ; -> 02064B30
004D23E7  mov      word ptr [rip + 0x1b929f2], dx  ; -> 02064DE0
004D23EE  seta     r8b
004D23F2  xor      eax, eax
004D23F4  add      r8w, r8w
004D23F8  comiss   xmm1, dword ptr [rip + 0x1b92735]  ; -> 02064B34
004D23FF  seta     al
004D2402  movss    xmm0, dword ptr [rip + 0x1b9288e]  ; -> 02064C98
004D240A  add      r8w, ax
004D240E  xor      eax, eax
004D2410  movsx    edx, dx
004D2413  add      r8w, r8w
004D2417  comiss   xmm0, dword ptr [rip + 0x1b9271a]  ; -> 02064B38
004D241E  seta     al
004D2421  xor      ecx, ecx
004D2423  add      r8w, ax
004D2427  shl      r8w, 5
004D242C  and      r8w, r9w
004D2430  comiss   xmm5, xmm2
004D2433  mov      word ptr [rip + 0x1b929a9], r8w  ; -> 02064DE4
004D243B  movss    xmm5, dword ptr [rip + 0x1b927c5]  ; -> 02064C08
004D2443  addss    xmm5, xmm9
004D2448  seta     cl
004D244B  xor      eax, eax
004D244D  add      cx, cx
004D2450  comiss   xmm4, xmm1
004D2453  movss    dword ptr [rip + 0x1b927ad], xmm5  ; -> 02064C08
004D245B  seta     al
004D245E  add      cx, ax
004D2461  xor      eax, eax
004D2463  add      cx, cx
004D2466  comiss   xmm3, xmm0
004D2469  movups   xmm0, xmmword ptr [rip + 0x1b92820]  ; -> 02064C90
004D2470  seta     al
004D2473  add      cx, ax
004D2476  shl      cx, 5
004D247A  and      r9w, cx
004D247E  movsx    ecx, r8w
004D2482  movsx    eax, r9w
004D2486  add      ax, cx
004D2489  mov      word ptr [rip + 0x1b92957], r9w  ; -> 02064DE8
004D2491  add      ax, dx
004D2494  movzx    edx, word ptr [rip + 0x1b92939]  ; -> 02064DD4
004D249B  add      r10w, ax
004D249F  dec      dx
004D24A2  lea      eax, [rbx + 0x190]
004D24A8  mov      word ptr [rip + 0x1b9292c], r10w  ; -> 02064DDC
004D24B0  shl      eax, 4
004D24B3  movsxd   rcx, eax
004D24B6  mov      word ptr [rip + 0x1b92917], dx  ; -> 02064DD4
004D24BD  movups   xmmword ptr [rcx + rbp], xmm0
004D24C1  mov      dword ptr [rsi + rbp + 0xc], edi
004D24C5  cmp      r10w, di
004D24C9  je       0x4d24d6  ; -> 004D24D6
004D24CB  movzx    eax, word ptr [rip + 0x1b928ea]  ; -> 02064DBC
004D24D2  mov      dword ptr [rsi + rbp + 0xc], eax
004D24D6  inc      bx
004D24D9  mov      word ptr [rip + 0x1b928f8], bx  ; -> 02064DD8
004D24E0  cmp      di, dx
004D24E3  jne      0x4d1d80  ; -> 004D1D80
004D24E9  jmp      0x4d3d14  ; -> 004D3D14
004D24EE  cmp      r8d, 2
004D24F2  jne      0x4d3bfa  ; -> 004D3BFA
004D24F8  movzx    eax, word ptr [rip + 0x1b9260d]  ; -> 02064B0C
004D24FF  lea      rbp, [rip + 0x1b9292a]  ; -> 02064E30
004D2506  add      ax, 0x4a
004D250A  xor      r8d, r8d
004D250D  mov      word ptr [rip + 0x1b928d4], ax  ; -> 02064DE8
004D2514  cwde     
004D2515  shl      eax, 4
004D2518  movsxd   rcx, eax
004D251B  add      rcx, rbp
004D251E  call     r9
004D2521  movsx    r10d, word ptr [rip + 0x1b925e3]  ; -> 02064B0C
004D2529  mov      ebx, 0x2bc
004D252E  movss    xmm11, dword ptr [rip + 0x1930301]  ; -> 01E02838 [u32 0x00000000]
004D2537  add      ebx, r10d
004D253A  movss    xmm13, dword ptr [rip + 0x19302f9]  ; -> 01E0283C [f32 1]
004D2543  xorps    xmm15, xmm15
004D2547  movss    xmm12, dword ptr [rip + 0x19302e0]  ; -> 01E02830 [u32 0x00000000]
004D2550  addss    xmm11, xmm13
004D2555  movss    xmm8, dword ptr [rip + 0x42de02]  ; -> 00900360 [u32 0x7F7FFFFF]
004D255E  lea      eax, [r10 + 0x49]
004D2562  shl      eax, 4
004D2565  mov      edx, r10d
004D2568  movsxd   rcx, eax
004D256B  lea      eax, [r10 + 0x46]
004D256F  shl      eax, 4
004D2572  mov      word ptr [rip + 0x1b92837], bx  ; -> 02064DB0
004D2579  inc      bx
004D257C  mov      word ptr [rip + 0x1b92831], bx  ; -> 02064DB4
004D2583  movups   xmm0, xmmword ptr [rcx + rbp]
004D2587  movsxd   rcx, eax
004D258A  lea      eax, [r10 + 0x48]
004D258E  shl      eax, 4
004D2591  cvtdq2ps xmm2, xmm0
004D2594  mov      word ptr [rip + 0x1b9281c], r10w  ; -> 02064DB8
004D259C  mov      word ptr [rip + 0x1b9282c], r10w  ; -> 02064DD0
004D25A4  movups   xmm9, xmmword ptr [rcx + rbp]
004D25A9  movsxd   rcx, eax
004D25AC  movss    xmm0, dword ptr [rip + 0x3f3580]  ; -> 008C5B34 [f32 0.0078125]
004D25B4  mulps    xmm2, xmmword ptr [rip + 0x850155]  ; -> 00D22710 [f32x4 0.0078125, 0.0078125, 0.0078125, 0.0078125]
004D25BB  movzx    eax, word ptr [rcx + rbp]
004D25BF  mov      word ptr [rip + 0x1b9281a], ax  ; -> 02064DE0
004D25C6  lea      eax, [r10 + 0x20]
004D25CA  shl      eax, 4
004D25CD  movdqu   xmmword ptr [rip + 0x1b925fa], xmm9  ; -> 02064BD0
004D25D6  movsxd   rcx, eax
004D25D9  shufps   xmm9, xmm9, 0xaa
004D25DE  movss    dword ptr [rip + 0x1b9251e], xmm0  ; -> 02064B04
004D25E6  subss    xmm11, xmm9
004D25EB  movss    xmm0, dword ptr [rip + 0x1930241]  ; -> 01E02834 [u32 0x00000000]
004D25F3  movaps   xmm10, xmm9
004D25F7  movzx    eax, word ptr [rcx + rbp]
004D25FB  addss    xmm10, xmm12
004D2600  movaps   xmm7, xmm0
004D2603  mov      word ptr [rip + 0x1b927ba], ax  ; -> 02064DC4
004D260A  addss    xmm7, xmm0
004D260E  movss    dword ptr [rip + 0x1b925d1], xmm11  ; -> 02064BE8
004D2617  movups   xmmword ptr [rip + 0x1b92642], xmm2  ; -> 02064C60
004D261E  ucomiss  xmm10, xmm15
004D2622  movss    dword ptr [rip + 0x1b925b5], xmm10  ; -> 02064BE0
004D262B  movss    dword ptr [rip + 0x1b92621], xmm7  ; -> 02064C54
004D2633  jp       0x4d2646  ; -> 004D2646
004D2635  jne      0x4d2646  ; -> 004D2646
004D2637  movss    dword ptr [rip + 0x1b924c0], xmm8  ; -> 02064B00
004D2640  movaps   xmm14, xmm8
004D2644  jmp      0x4d2658  ; -> 004D2658
004D2646  movaps   xmm14, xmm13
004D264A  divss    xmm14, xmm10
004D264F  movss    dword ptr [rip + 0x1b924a8], xmm14  ; -> 02064B00
004D2658  movss    xmm2, dword ptr [rip + 0x1b92600]  ; -> 02064C60
004D2660  lea      eax, [rdx + 3]
004D2663  shl      eax, 4
004D2666  movaps   xmm1, xmm12
004D266A  movsxd   rcx, eax
004D266D  addss    xmm1, xmm13
004D2672  lea      eax, [rdx + 4]
004D2675  movss    dword ptr [rip + 0x1b92627], xmm7  ; -> 02064CA4
004D267D  shl      eax, 4
004D2680  movups   xmm0, xmmword ptr [rcx + rbp]
004D2684  movsxd   rcx, eax
004D2687  lea      eax, [rdx + 5]
004D268A  movss    dword ptr [rip + 0x1b9260e], xmm1  ; -> 02064CA0
004D2692  movups   xmmword ptr [rip + 0x1b92497], xmm0  ; -> 02064B30
004D2699  shl      eax, 4
004D269C  movups   xmm3, xmmword ptr [rcx + rbp]
004D26A0  movsxd   rcx, eax
004D26A3  lea      eax, [rdx + 6]
004D26A6  movss    xmm1, dword ptr [rip + 0x1b92486]  ; -> 02064B34
004D26AE  mulss    xmm1, dword ptr [rip + 0x1b925ae]  ; -> 02064C64
004D26B6  shl      eax, 4
004D26B9  movups   xmm4, xmmword ptr [rcx + rbp]
004D26BD  movsxd   rcx, eax
004D26C0  lea      eax, [rdx + 7]
004D26C3  movss    dword ptr [rip + 0x1b92465], xmm0  ; -> 02064B30
004D26CB  mulss    xmm0, xmm2
004D26CF  shl      eax, 4
004D26D2  movups   xmm6, xmmword ptr [rcx + rbp]
004D26D6  movsxd   rcx, eax
004D26D9  lea      eax, [rdx + 8]
004D26DC  movss    dword ptr [rip + 0x1b9244c], xmm0  ; -> 02064B30
004D26E4  movss    xmm0, dword ptr [rip + 0x1b9244c]  ; -> 02064B38
004D26EC  mulss    xmm0, dword ptr [rip + 0x1b92574]  ; -> 02064C68
004D26F4  shl      eax, 4
004D26F7  movups   xmm5, xmmword ptr [rcx + rbp]
004D26FB  movsxd   rcx, eax
004D26FE  lea      eax, [rdx + 9]
004D2701  movss    dword ptr [rip + 0x1b9242f], xmm0  ; -> 02064B38
004D2709  movups   xmmword ptr [rip + 0x1b92430], xmm3  ; -> 02064B40
004D2710  shl      eax, 4
004D2713  movss    xmm0, dword ptr [rip + 0x1b92429]  ; -> 02064B44
004D271B  mulss    xmm0, dword ptr [rip + 0x1b92541]  ; -> 02064C64
004D2723  movups   xmmword ptr [rip + 0x1b92426], xmm4  ; -> 02064B50
004D272A  movss    dword ptr [rip + 0x1b92412], xmm0  ; -> 02064B44
004D2732  movss    xmm0, dword ptr [rip + 0x1b92412]  ; -> 02064B4C
004D273A  mulss    xmm0, dword ptr [rip + 0x1b9252a]  ; -> 02064C6C
004D2742  movss    dword ptr [rip + 0x1b923ea], xmm1  ; -> 02064B34
004D274A  movss    xmm1, dword ptr [rip + 0x1b923ea]  ; -> 02064B3C
004D2752  mulss    xmm1, dword ptr [rip + 0x1b92512]  ; -> 02064C6C
004D275A  movss    dword ptr [rip + 0x1b923ea], xmm0  ; -> 02064B4C
004D2762  movss    xmm0, dword ptr [rip + 0x1b923ea]  ; -> 02064B54
004D276A  mulss    xmm0, dword ptr [rip + 0x1b924f2]  ; -> 02064C64
004D2772  movss    dword ptr [rip + 0x1b923c2], xmm1  ; -> 02064B3C
004D277A  movss    xmm1, dword ptr [rip + 0x1b923c6]  ; -> 02064B48
004D2782  mulss    xmm1, dword ptr [rip + 0x1b924de]  ; -> 02064C68
004D278A  movss    dword ptr [rip + 0x1b923c2], xmm0  ; -> 02064B54
004D2792  movss    xmm0, dword ptr [rip + 0x1b923c2]  ; -> 02064B5C
004D279A  mulss    xmm0, dword ptr [rip + 0x1b924ca]  ; -> 02064C6C
004D27A2  movss    dword ptr [rip + 0x1b9239e], xmm1  ; -> 02064B48
004D27AA  movss    xmm1, dword ptr [rip + 0x1b923a6]  ; -> 02064B58
004D27B2  mulss    xmm1, dword ptr [rip + 0x1b924ae]  ; -> 02064C68
004D27BA  movups   xmmword ptr [rip + 0x1b9239f], xmm6  ; -> 02064B60
004D27C1  mulss    xmm3, xmm2
004D27C5  mulss    xmm4, xmm2
004D27C9  movss    dword ptr [rip + 0x1b9238b], xmm0  ; -> 02064B5C
004D27D1  movaps   xmm0, xmm6
004D27D4  movss    dword ptr [rip + 0x1b92384], xmm6  ; -> 02064B60
004D27DC  movaps   xmm6, xmm2
004D27DF  movss    dword ptr [rip + 0x1b92371], xmm1  ; -> 02064B58
004D27E7  movss    xmm1, dword ptr [rip + 0x1b92375]  ; -> 02064B64
004D27EF  mulss    xmm1, dword ptr [rip + 0x1b9246d]  ; -> 02064C64
004D27F7  movss    dword ptr [rip + 0x1b92341], xmm3  ; -> 02064B40
004D27FF  movups   xmm3, xmmword ptr [rcx + rbp]
004D2803  movsxd   rcx, eax
004D2806  mulss    xmm0, xmm6
004D280A  movss    dword ptr [rip + 0x1b9233e], xmm4  ; -> 02064B50
004D2812  movups   xmm4, xmmword ptr [rcx + rbp]
004D2816  movss    dword ptr [rip + 0x1b92342], xmm0  ; -> 02064B60
004D281E  movups   xmmword ptr [rip + 0x1b9234b], xmm5  ; -> 02064B70
004D2825  movups   xmmword ptr [rip + 0x1b92354], xmm3  ; -> 02064B80
004D282C  movups   xmmword ptr [rip + 0x1b9235d], xmm4  ; -> 02064B90
004D2833  movss    xmm0, dword ptr [rip + 0x1b9232d]  ; -> 02064B68
004D283B  lea      eax, [rdx + 0xa]
004D283E  mulss    xmm0, dword ptr [rip + 0x1b92422]  ; -> 02064C68
004D2846  shl      eax, 4
004D2849  movss    dword ptr [rip + 0x1b92313], xmm1  ; -> 02064B64
004D2851  movss    xmm1, dword ptr [rip + 0x1b92313]  ; -> 02064B6C
004D2859  mulss    xmm1, dword ptr [rip + 0x1b9240b]  ; -> 02064C6C
004D2861  movsxd   rcx, eax
004D2864  lea      eax, [rdx + 0xb]
004D2867  movss    dword ptr [rip + 0x1b922f9], xmm0  ; -> 02064B68
004D286F  movss    xmm0, dword ptr [rip + 0x1b922fd]  ; -> 02064B74
004D2877  movss    dword ptr [rip + 0x1b922ed], xmm1  ; -> 02064B6C
004D287F  movups   xmm2, xmmword ptr [rcx + rbp]
004D2883  shl      eax, 4
004D2886  movss    xmm1, dword ptr [rip + 0x1b922ea]  ; -> 02064B78
004D288E  mulss    xmm1, dword ptr [rip + 0x1b923d2]  ; -> 02064C68
004D2896  movsxd   rcx, eax
004D2899  movups   xmmword ptr [rip + 0x1b92300], xmm2  ; -> 02064BA0
004D28A0  movss    dword ptr [rip + 0x1b922d0], xmm1  ; -> 02064B78
004D28A8  movss    xmm1, dword ptr [rip + 0x1b922d8]  ; -> 02064B88
004D28B0  mulss    xmm5, xmm6
004D28B4  mulss    xmm3, xmm6
004D28B8  movss    dword ptr [rip + 0x1b922b0], xmm5  ; -> 02064B70
004D28C0  movss    xmm5, dword ptr [rip + 0x1b9239c]  ; -> 02064C64
004D28C8  mulss    xmm0, xmm5
004D28CC  movss    dword ptr [rip + 0x1b922ac], xmm3  ; -> 02064B80
004D28D4  movss    xmm3, dword ptr [rip + 0x1b9238c]  ; -> 02064C68
004D28DC  movss    dword ptr [rip + 0x1b92290], xmm0  ; -> 02064B74
004D28E4  movss    xmm0, dword ptr [rip + 0x1b92290]  ; -> 02064B7C
004D28EC  mulss    xmm0, dword ptr [rip + 0x1b92378]  ; -> 02064C6C
004D28F4  mulss    xmm1, xmm3
004D28F8  movss    dword ptr [rip + 0x1b9227c], xmm0  ; -> 02064B7C
004D2900  movups   xmm0, xmmword ptr [rcx + rbp]
004D2904  movss    dword ptr [rip + 0x1b9227c], xmm1  ; -> 02064B88
004D290C  movss    xmm1, dword ptr [rip + 0x1b92284]  ; -> 02064B98
004D2914  movups   xmmword ptr [rip + 0x1b92295], xmm0  ; -> 02064BB0
004D291B  movss    xmm0, dword ptr [rip + 0x1b92261]  ; -> 02064B84
004D2923  mulss    xmm0, xmm5
004D2927  mulss    xmm1, xmm3
004D292B  movss    dword ptr [rip + 0x1b92251], xmm0  ; -> 02064B84
004D2933  movss    xmm0, dword ptr [rip + 0x1b92251]  ; -> 02064B8C
004D293B  mulss    xmm0, dword ptr [rip + 0x1b92329]  ; -> 02064C6C
004D2943  movss    dword ptr [rip + 0x1b9224d], xmm1  ; -> 02064B98
004D294B  movss    xmm1, dword ptr [rip + 0x1b92255]  ; -> 02064BA8
004D2953  movss    dword ptr [rip + 0x1b92231], xmm0  ; -> 02064B8C
004D295B  movss    xmm0, dword ptr [rip + 0x1b92231]  ; -> 02064B94
004D2963  mulss    xmm0, xmm5
004D2967  mulss    xmm4, xmm6
004D296B  movss    dword ptr [rip + 0x1b92221], xmm0  ; -> 02064B94
004D2973  movss    xmm0, dword ptr [rip + 0x1b92221]  ; -> 02064B9C
004D297B  mulss    xmm0, dword ptr [rip + 0x1b922e9]  ; -> 02064C6C
004D2983  mulss    xmm2, xmm6
004D2987  movss    dword ptr [rip + 0x1b9220d], xmm0  ; -> 02064B9C
004D298F  movss    xmm0, dword ptr [rip + 0x1b9220d]  ; -> 02064BA4
004D2997  mulss    xmm0, xmm5
004D299B  mulss    xmm1, xmm3
004D299F  movss    dword ptr [rip + 0x1b921fd], xmm0  ; -> 02064BA4
004D29A7  movss    xmm0, dword ptr [rip + 0x1b921fd]  ; -> 02064BAC
004D29AF  mulss    xmm0, dword ptr [rip + 0x1b922b5]  ; -> 02064C6C
004D29B7  movss    dword ptr [rip + 0x1b921d1], xmm4  ; -> 02064B90
004D29BF  movss    dword ptr [rip + 0x1b921d9], xmm2  ; -> 02064BA0
004D29C7  movss    dword ptr [rip + 0x1b921dd], xmm0  ; -> 02064BAC
004D29CF  movss    xmm0, dword ptr [rip + 0x192fe5d]  ; -> 01E02834 [u32 0x00000000]
004D29D7  addss    xmm0, xmm14
004D29DC  movss    dword ptr [rip + 0x1b921c4], xmm1  ; -> 02064BA8
004D29E4  ucomiss  xmm0, xmm15
004D29E8  movss    dword ptr [rip + 0x1b921f4], xmm0  ; -> 02064BE4
004D29F0  jp       0x4d2a45  ; -> 004D2A45
004D29F2  jne      0x4d2a45  ; -> 004D2A45
004D29F4  call     0x22cc40  ; -> 0022CC40 fn
004D29F9  movzx    r10d, word ptr [rip + 0x1b9210b]  ; -> 02064B0C
004D2A01  movss    xmm4, dword ptr [rip + 0x1b92187]  ; -> 02064B90
004D2A09  movss    xmm13, dword ptr [rip + 0x192fe2a]  ; -> 01E0283C [f32 1]
004D2A12  movss    xmm12, dword ptr [rip + 0x192fe15]  ; -> 01E02830 [u32 0x00000000]
004D2A1B  movzx    ebx, word ptr [rip + 0x1b92392]  ; -> 02064DB4
004D2A22  movss    xmm7, dword ptr [rip + 0x1b9222a]  ; -> 02064C54
004D2A2A  movss    xmm9, dword ptr [rip + 0x1b921a5]  ; -> 02064BD8
004D2A33  movss    xmm11, dword ptr [rip + 0x1b921ac]  ; -> 02064BE8
004D2A3C  movss    xmm10, dword ptr [rip + 0x1b9219b]  ; -> 02064BE0
004D2A45  comiss   xmm15, dword ptr [rip + 0x1b92197]  ; -> 02064BE4
004D2A4D  jbe      0x4d2aa0  ; -> 004D2AA0
004D2A4F  call     0x22cc30  ; -> 0022CC30 fn
004D2A54  movzx    r10d, word ptr [rip + 0x1b920b0]  ; -> 02064B0C
004D2A5C  movss    xmm4, dword ptr [rip + 0x1b9212c]  ; -> 02064B90
004D2A64  movss    xmm13, dword ptr [rip + 0x192fdcf]  ; -> 01E0283C [f32 1]
004D2A6D  movss    xmm12, dword ptr [rip + 0x192fdba]  ; -> 01E02830 [u32 0x00000000]
004D2A76  movzx    ebx, word ptr [rip + 0x1b92337]  ; -> 02064DB4
004D2A7D  movss    xmm7, dword ptr [rip + 0x1b921cf]  ; -> 02064C54
004D2A85  movss    xmm9, dword ptr [rip + 0x1b9214a]  ; -> 02064BD8
004D2A8E  movss    xmm11, dword ptr [rip + 0x1b92151]  ; -> 02064BE8
004D2A97  movss    xmm10, dword ptr [rip + 0x1b92140]  ; -> 02064BE0
004D2AA0  ucomiss  xmm11, xmm15
004D2AA4  movss    xmm0, dword ptr [rip + 0x1b92104]  ; -> 02064BB0
004D2AAC  mulss    xmm0, dword ptr [rip + 0x1b921ac]  ; -> 02064C60
004D2AB4  movss    xmm1, dword ptr [rip + 0x1b920f8]  ; -> 02064BB4
004D2ABC  mulss    xmm1, dword ptr [rip + 0x1b921a0]  ; -> 02064C64
004D2AC4  movss    xmm3, dword ptr [rip + 0x1b920f0]  ; -> 02064BBC
004D2ACC  mulss    xmm3, dword ptr [rip + 0x1b92198]  ; -> 02064C6C
004D2AD4  movss    dword ptr [rip + 0x1b920d4], xmm0  ; -> 02064BB0
004D2ADC  movss    xmm0, dword ptr [rip + 0x1b920d4]  ; -> 02064BB8
004D2AE4  mulss    xmm0, dword ptr [rip + 0x1b9217c]  ; -> 02064C68
004D2AEC  movss    dword ptr [rip + 0x1b920c0], xmm1  ; -> 02064BB4
004D2AF4  movss    dword ptr [rip + 0x1b920bc], xmm0  ; -> 02064BB8
004D2AFC  jp       0x4d2b00  ; -> 004D2B00
004D2AFE  je       0x4d2b09  ; -> 004D2B09
004D2B00  movaps   xmm8, xmm13
004D2B04  divss    xmm8, xmm11
004D2B09  movss    xmm2, dword ptr [rip + 0x1b920cb]  ; -> 02064BDC
004D2B11  movss    xmm0, dword ptr [rip + 0x1b92023]  ; -> 02064B3C
004D2B19  movss    xmm1, dword ptr [rip + 0x1b9202b]  ; -> 02064B4C
004D2B21  movsx    r9d, word ptr [rip + 0x1b92297]  ; -> 02064DC0
004D2B29  mulss    xmm0, xmm2
004D2B2D  add      r9w, r10w
004D2B31  movsx    edx, r10w
004D2B35  mulss    xmm1, xmm2
004D2B39  mov      word ptr [rip + 0x1b92297], r10w  ; -> 02064DD8
004D2B41  movss    dword ptr [rip + 0x1b91ff3], xmm0  ; -> 02064B3C
004D2B49  movss    xmm0, dword ptr [rip + 0x1b9200b]  ; -> 02064B5C
004D2B51  lea      eax, [r10 + rdx]
004D2B55  mulss    xmm0, xmm2
004D2B59  mov      word ptr [rip + 0x1b9226c], ax  ; -> 02064DCC
004D2B60  lea      eax, [rdx + 0x46]
004D2B63  movss    dword ptr [rip + 0x1b91fe1], xmm1  ; -> 02064B4C
004D2B6B  movss    xmm1, dword ptr [rip + 0x1b91ff9]  ; -> 02064B6C
004D2B73  movss    dword ptr [rip + 0x1b91fe1], xmm0  ; -> 02064B5C
004D2B7B  movss    xmm0, dword ptr [rip + 0x1b91ff9]  ; -> 02064B7C
004D2B83  mulss    xmm0, xmm2
004D2B87  shl      eax, 4
004D2B8A  movsxd   r8, eax
004D2B8D  lea      eax, [rdx + 0x47]
004D2B90  mulss    xmm1, xmm2
004D2B94  shl      eax, 4
004D2B97  movss    dword ptr [rip + 0x1b91fdd], xmm0  ; -> 02064B7C
004D2B9F  movss    xmm0, dword ptr [rip + 0x1b91ff5]  ; -> 02064B9C
004D2BA7  mulss    xmm0, xmm2
004D2BAB  movsxd   rcx, eax
004D2BAE  movss    dword ptr [rip + 0x1b91fb6], xmm1  ; -> 02064B6C
004D2BB6  movss    xmm1, dword ptr [rip + 0x1b91fce]  ; -> 02064B8C
004D2BBE  movss    dword ptr [rip + 0x1b91fd6], xmm0  ; -> 02064B9C
004D2BC6  movss    xmm0, dword ptr [rip + 0x1b91fde]  ; -> 02064BAC
004D2BCE  mulss    xmm0, xmm2
004D2BD2  movss    dword ptr [rip + 0x1b91f25], xmm8  ; -> 02064B00
004D2BDB  mulss    xmm1, xmm2
004D2BDF  movss    dword ptr [rip + 0x1b91fc5], xmm0  ; -> 02064BAC
004D2BE7  movups   xmm0, xmmword ptr [rcx + rbp]
004D2BEB  mulss    xmm3, xmm2
004D2BEF  mulss    xmm8, xmm13
004D2BF4  movups   xmmword ptr [rip + 0x1b92115], xmm0  ; -> 02064D10
004D2BFB  movss    dword ptr [rip + 0x1b91f89], xmm1  ; -> 02064B8C
004D2C03  movss    dword ptr [rip + 0x1b91fb1], xmm3  ; -> 02064BBC
004D2C0B  movss    dword ptr [rip + 0x1b91fd8], xmm8  ; -> 02064BEC
004D2C14  cmp      word ptr [r8 + rbp + 4], r10w
004D2C1A  jne      0x4d2c4a  ; -> 004D2C4A
004D2C1C  lea      eax, [rdx + 0x1f]
004D2C1F  shl      eax, 4
004D2C22  movsxd   rcx, eax
004D2C25  movups   xmm1, xmmword ptr [rcx + rbp]
004D2C29  movups   xmmword ptr [rip + 0x1b92090], xmm1  ; -> 02064CC0
004D2C30  shufps   xmm1, xmm1, 0x55
004D2C34  addss    xmm12, xmm1
004D2C39  movss    dword ptr [rip + 0x1b92083], xmm1  ; -> 02064CC4
004D2C41  movss    dword ptr [rip + 0x1b92056], xmm12  ; -> 02064CA0
004D2C4A  movzx    eax, word ptr [r8 + rbp]
004D2C4F  movss    xmm6, dword ptr [rip + 0x3f2ee9]  ; -> 008C5B40 [f32 255]
004D2C57  movss    xmm15, dword ptr [rip + 0x1819024]  ; -> 01CEBC84 [f32 16]
004D2C60  mov      qword ptr [rsp + 0x128], r12
004D2C68  mov      word ptr [rip + 0x1b9216d], ax  ; -> 02064DDC
004D2C6F  mov      qword ptr [rsp + 0xe0], r15
004D2C77  nop      word ptr [rax + rax]
004D2C80  movups   xmm0, xmmword ptr [rip + 0x1b91fe9]  ; -> 02064C70
004D2C87  xor      edx, edx
004D2C89  movsx    r8d, bx
004D2C8D  movups   xmm1, xmmword ptr [rip + 0x1b91fec]  ; -> 02064C80
004D2C94  lea      eax, [r8 + 1]
004D2C98  shl      eax, 4
004D2C9B  movsxd   rcx, eax
004D2C9E  lea      eax, [r8 + 7]
004D2CA2  shl      eax, 4
004D2CA5  movups   xmmword ptr [rcx + rbp], xmm0
004D2CA9  movsxd   rcx, eax
004D2CAC  lea      eax, [r8 + 0xd]
004D2CB0  movups   xmm0, xmmword ptr [rip + 0x1b91fd9]  ; -> 02064C90
004D2CB7  shl      eax, 4
004D2CBA  comiss   xmm7, xmm9
004D2CBE  movups   xmmword ptr [rcx + rbp], xmm1
004D2CC2  movsxd   rcx, eax
004D2CC5  lea      eax, [r10 + 0x20]
004D2CC9  seta     dl
004D2CCC  dec      r9w
004D2CD0  shl      dx, 5
004D2CD4  and      dx, ax
004D2CD7  mov      word ptr [rip + 0x1b920f5], r9w  ; -> 02064DD4
004D2CDF  movups   xmmword ptr [rcx + rbp], xmm0
004D2CE3  lea      eax, [r8 + 0x13]
004D2CE7  mov      word ptr [rip + 0x1b920f6], dx  ; -> 02064DE4
004D2CEE  shl      eax, 4
004D2CF1  movsxd   rcx, eax
004D2CF4  movups   xmmword ptr [rcx + rbp], xmm1
004D2CF8  cmp      dx, r10w
004D2CFC  jne      0x4d2fac  ; -> 004D2FAC
004D2D02  movss    xmm0, dword ptr [rip + 0x1b91eda]  ; -> 02064BE4
004D2D0A  movss    xmm1, dword ptr [rip + 0x1b91e4e]  ; -> 02064B60
004D2D12  subss    xmm1, dword ptr [rip + 0x1b91e16]  ; -> 02064B30
004D2D1A  mulss    xmm0, xmm7
004D2D1E  movss    dword ptr [rip + 0x1b91f1e], xmm0  ; -> 02064C44
004D2D26  movss    xmm0, dword ptr [rip + 0x1b91e36]  ; -> 02064B64
004D2D2E  subss    xmm0, dword ptr [rip + 0x1b91dfe]  ; -> 02064B34
004D2D36  movss    dword ptr [rip + 0x1b91f32], xmm1  ; -> 02064C70
004D2D3E  movss    xmm1, dword ptr [rip + 0x1b91e22]  ; -> 02064B68
004D2D46  subss    xmm1, dword ptr [rip + 0x1b91dea]  ; -> 02064B38
004D2D4E  movss    dword ptr [rip + 0x1b91f1e], xmm0  ; -> 02064C74
004D2D56  movss    xmm0, dword ptr [rip + 0x1b91e0e]  ; -> 02064B6C
004D2D5E  subss    xmm0, dword ptr [rip + 0x1b91dd6]  ; -> 02064B3C
004D2D66  movss    dword ptr [rip + 0x1b91f0a], xmm1  ; -> 02064C78
004D2D6E  movss    dword ptr [rip + 0x1b91f06], xmm0  ; -> 02064C7C
004D2D76  call     0x22cc20  ; -> 0022CC20 fn
004D2D7B  movups   xmm0, xmmword ptr [rip + 0x1b91f2e]  ; -> 02064CB0
004D2D82  movsx    eax, word ptr [rip + 0x1b9202b]  ; -> 02064DB4
004D2D89  movss    xmm1, dword ptr [rip + 0x1b91ddf]  ; -> 02064B70
004D2D91  add      eax, 2
004D2D94  subss    xmm1, dword ptr [rip + 0x1b91da4]  ; -> 02064B40
004D2D9C  shl      eax, 4
004D2D9F  movsxd   rcx, eax
004D2DA2  movss    dword ptr [rip + 0x1b91ed6], xmm1  ; -> 02064C80
004D2DAA  movss    xmm1, dword ptr [rip + 0x1b91dc6]  ; -> 02064B78
004D2DB2  subss    xmm1, dword ptr [rip + 0x1b91d8e]  ; -> 02064B48
004D2DBA  movups   xmmword ptr [rcx + rbp], xmm0
004D2DBE  movss    xmm0, dword ptr [rip + 0x1b91dae]  ; -> 02064B74
004D2DC6  subss    xmm0, dword ptr [rip + 0x1b91d76]  ; -> 02064B44
004D2DCE  movss    dword ptr [rip + 0x1b91eb2], xmm1  ; -> 02064C88
004D2DD6  movss    dword ptr [rip + 0x1b91ea6], xmm0  ; -> 02064C84
004D2DDE  movss    xmm0, dword ptr [rip + 0x1b91d96]  ; -> 02064B7C
004D2DE6  subss    xmm0, dword ptr [rip + 0x1b91d5e]  ; -> 02064B4C
004D2DEE  movss    dword ptr [rip + 0x1b91e96], xmm0  ; -> 02064C8C
004D2DF6  call     0x22cc20  ; -> 0022CC20 fn
004D2DFB  movups   xmm0, xmmword ptr [rip + 0x1b91ebe]  ; -> 02064CC0
004D2E02  movsx    eax, word ptr [rip + 0x1b91fab]  ; -> 02064DB4
004D2E09  movss    xmm1, dword ptr [rip + 0x1b91d6f]  ; -> 02064B80
004D2E11  add      eax, 8
004D2E14  subss    xmm1, dword ptr [rip + 0x1b91d34]  ; -> 02064B50
004D2E1C  shl      eax, 4
004D2E1F  movsxd   rcx, eax
004D2E22  movss    dword ptr [rip + 0x1b91e66], xmm1  ; -> 02064C90
004D2E2A  movss    xmm1, dword ptr [rip + 0x1b91d56]  ; -> 02064B88
004D2E32  subss    xmm1, dword ptr [rip + 0x1b91d1e]  ; -> 02064B58
004D2E3A  movups   xmmword ptr [rcx + rbp], xmm0
004D2E3E  movss    xmm0, dword ptr [rip + 0x1b91d3e]  ; -> 02064B84
004D2E46  subss    xmm0, dword ptr [rip + 0x1b91d06]  ; -> 02064B54
004D2E4E  movss    dword ptr [rip + 0x1b91e42], xmm1  ; -> 02064C98
004D2E56  movss    dword ptr [rip + 0x1b91e36], xmm0  ; -> 02064C94
004D2E5E  movss    xmm0, dword ptr [rip + 0x1b91d26]  ; -> 02064B8C
004D2E66  subss    xmm0, dword ptr [rip + 0x1b91cee]  ; -> 02064B5C
004D2E6E  movss    dword ptr [rip + 0x1b91e26], xmm0  ; -> 02064C9C
004D2E76  call     0x22cc20  ; -> 0022CC20 fn
004D2E7B  movss    xmm1, dword ptr [rip + 0x1b91dc1]  ; -> 02064C44
004D2E83  movsx    ebx, word ptr [rip + 0x1b91f2a]  ; -> 02064DB4
004D2E8A  movups   xmm0, xmmword ptr [rip + 0x1b91e3f]  ; -> 02064CD0
004D2E91  mov      r9d, ebx
004D2E94  movss    xmm3, dword ptr [rip + 0x1b91dd8]  ; -> 02064C74
004D2E9C  movss    xmm2, dword ptr [rip + 0x1b91dcc]  ; -> 02064C70
004D2EA4  lea      eax, [rbx + 0xe]
004D2EA7  movss    xmm4, dword ptr [rip + 0x1b91dc9]  ; -> 02064C78
004D2EAF  movss    xmm5, dword ptr [rip + 0x1b91dc5]  ; -> 02064C7C
004D2EB7  movss    xmm8, dword ptr [rip + 0x1b91dc4]  ; -> 02064C84
004D2EC0  movss    xmm7, dword ptr [rip + 0x1b91db8]  ; -> 02064C80
004D2EC8  movss    xmm9, dword ptr [rip + 0x1b91db7]  ; -> 02064C88
004D2ED1  movss    xmm10, dword ptr [rip + 0x1b91db2]  ; -> 02064C8C
004D2EDA  movss    xmm12, dword ptr [rip + 0x1b91db1]  ; -> 02064C94
004D2EE3  movss    xmm11, dword ptr [rip + 0x1b91da4]  ; -> 02064C90
004D2EEC  shl      eax, 4
004D2EEF  movsxd   r15, eax
004D2EF2  mulss    xmm3, xmm1
004D2EF6  mulss    xmm2, xmm1
004D2EFA  movups   xmmword ptr [r15 + rbp], xmm0
004D2EFF  mulss    xmm4, xmm1
004D2F03  mulss    xmm5, xmm1
004D2F07  mulss    xmm8, xmm1
004D2F0C  mulss    xmm7, xmm1
004D2F10  mulss    xmm9, xmm1
004D2F15  mulss    xmm10, xmm1
004D2F1A  mulss    xmm12, xmm1
004D2F1F  movss    xmm13, dword ptr [rip + 0x1b91d70]  ; -> 02064C98
004D2F28  movss    xmm14, dword ptr [rip + 0x1b91d6b]  ; -> 02064C9C
004D2F31  addss    xmm2, dword ptr [rip + 0x1b91bf7]  ; -> 02064B30
004D2F39  addss    xmm3, dword ptr [rip + 0x1b91bf3]  ; -> 02064B34
004D2F41  addss    xmm4, dword ptr [rip + 0x1b91bef]  ; -> 02064B38
004D2F49  addss    xmm5, dword ptr [rip + 0x1b91beb]  ; -> 02064B3C
004D2F51  addss    xmm7, dword ptr [rip + 0x1b91be7]  ; -> 02064B40
004D2F59  addss    xmm8, dword ptr [rip + 0x1b91be2]  ; -> 02064B44
004D2F62  addss    xmm9, dword ptr [rip + 0x1b91bdd]  ; -> 02064B48
004D2F6B  addss    xmm10, dword ptr [rip + 0x1b91bd8]  ; -> 02064B4C
004D2F74  addss    xmm12, dword ptr [rip + 0x1b91bd7]  ; -> 02064B54
004D2F7D  mulss    xmm13, xmm1
004D2F82  mulss    xmm14, xmm1
004D2F87  addss    xmm13, dword ptr [rip + 0x1b91bc8]  ; -> 02064B58
004D2F90  mulss    xmm11, xmm1
004D2F95  addss    xmm14, dword ptr [rip + 0x1b91bbe]  ; -> 02064B5C
004D2F9E  addss    xmm11, dword ptr [rip + 0x1b91ba9]  ; -> 02064B50
004D2FA7  jmp      0x4d3247  ; -> 004D3247
004D2FAC  movss    xmm0, dword ptr [rip + 0x1b91be0]  ; -> 02064B94
004D2FB4  subss    xmm7, xmm10
004D2FB9  subss    xmm0, dword ptr [rip + 0x1b91ba3]  ; -> 02064B64
004D2FC1  movss    xmm1, dword ptr [rip + 0x1b91bcf]  ; -> 02064B98
004D2FC9  subss    xmm4, dword ptr [rip + 0x1b91b8f]  ; -> 02064B60
004D2FD1  subss    xmm1, dword ptr [rip + 0x1b91b8f]  ; -> 02064B68
004D2FD9  mulss    xmm7, xmm8
004D2FDE  movss    dword ptr [rip + 0x1b91c8e], xmm0  ; -> 02064C74
004D2FE6  movss    xmm0, dword ptr [rip + 0x1b91bae]  ; -> 02064B9C
004D2FEE  subss    xmm0, dword ptr [rip + 0x1b91b76]  ; -> 02064B6C
004D2FF6  movss    dword ptr [rip + 0x1b91c46], xmm7  ; -> 02064C44
004D2FFE  movss    dword ptr [rip + 0x1b91c6a], xmm4  ; -> 02064C70
004D3006  movss    dword ptr [rip + 0x1b91c6a], xmm1  ; -> 02064C78
004D300E  movss    dword ptr [rip + 0x1b91c66], xmm0  ; -> 02064C7C
004D3016  call     0x22cc20  ; -> 0022CC20 fn
004D301B  movups   xmm0, xmmword ptr [rip + 0x1b91c8e]  ; -> 02064CB0
004D3022  movsx    eax, word ptr [rip + 0x1b91d8b]  ; -> 02064DB4
004D3029  movss    xmm1, dword ptr [rip + 0x1b91b6f]  ; -> 02064BA0
004D3031  add      eax, 2
004D3034  subss    xmm1, dword ptr [rip + 0x1b91b34]  ; -> 02064B70
004D303C  shl      eax, 4
004D303F  movsxd   rcx, eax
004D3042  movss    dword ptr [rip + 0x1b91c36], xmm1  ; -> 02064C80
004D304A  movss    xmm1, dword ptr [rip + 0x1b91b56]  ; -> 02064BA8
004D3052  subss    xmm1, dword ptr [rip + 0x1b91b1e]  ; -> 02064B78
004D305A  movups   xmmword ptr [rcx + rbp], xmm0
004D305E  movss    xmm0, dword ptr [rip + 0x1b91b3e]  ; -> 02064BA4
004D3066  subss    xmm0, dword ptr [rip + 0x1b91b06]  ; -> 02064B74
004D306E  movss    dword ptr [rip + 0x1b91c12], xmm1  ; -> 02064C88
004D3076  movss    dword ptr [rip + 0x1b91c06], xmm0  ; -> 02064C84
004D307E  movss    xmm0, dword ptr [rip + 0x1b91b26]  ; -> 02064BAC
004D3086  subss    xmm0, dword ptr [rip + 0x1b91aee]  ; -> 02064B7C
004D308E  movss    dword ptr [rip + 0x1b91bf6], xmm0  ; -> 02064C8C
004D3096  call     0x22cc20  ; -> 0022CC20 fn
004D309B  movups   xmm0, xmmword ptr [rip + 0x1b91c1e]  ; -> 02064CC0
004D30A2  movsx    eax, word ptr [rip + 0x1b91d0b]  ; -> 02064DB4
004D30A9  movss    xmm1, dword ptr [rip + 0x1b91aff]  ; -> 02064BB0
004D30B1  add      eax, 8
004D30B4  subss    xmm1, dword ptr [rip + 0x1b91ac4]  ; -> 02064B80
004D30BC  shl      eax, 4
004D30BF  movsxd   rcx, eax
004D30C2  movss    dword ptr [rip + 0x1b91bc6], xmm1  ; -> 02064C90
004D30CA  movss    xmm1, dword ptr [rip + 0x1b91ae6]  ; -> 02064BB8
004D30D2  subss    xmm1, dword ptr [rip + 0x1b91aae]  ; -> 02064B88
004D30DA  movups   xmmword ptr [rcx + rbp], xmm0
004D30DE  movss    xmm0, dword ptr [rip + 0x1b91ace]  ; -> 02064BB4
004D30E6  subss    xmm0, dword ptr [rip + 0x1b91a96]  ; -> 02064B84
004D30EE  movss    dword ptr [rip + 0x1b91ba2], xmm1  ; -> 02064C98
004D30F6  movss    dword ptr [rip + 0x1b91b96], xmm0  ; -> 02064C94
004D30FE  movss    xmm0, dword ptr [rip + 0x1b91ab6]  ; -> 02064BBC
004D3106  subss    xmm0, dword ptr [rip + 0x1b91a7e]  ; -> 02064B8C
004D310E  movss    dword ptr [rip + 0x1b91b86], xmm0  ; -> 02064C9C
004D3116  call     0x22cc20  ; -> 0022CC20 fn
004D311B  movss    xmm1, dword ptr [rip + 0x1b91b21]  ; -> 02064C44
004D3123  movsx    ebx, word ptr [rip + 0x1b91c8a]  ; -> 02064DB4
004D312A  movups   xmm0, xmmword ptr [rip + 0x1b91b9f]  ; -> 02064CD0
004D3131  mov      r9d, ebx
004D3134  movss    xmm3, dword ptr [rip + 0x1b91b38]  ; -> 02064C74
004D313C  movss    xmm2, dword ptr [rip + 0x1b91b2c]  ; -> 02064C70
004D3144  lea      eax, [rbx + 0xe]
004D3147  movss    xmm4, dword ptr [rip + 0x1b91b29]  ; -> 02064C78
004D314F  movss    xmm5, dword ptr [rip + 0x1b91b25]  ; -> 02064C7C
004D3157  movss    xmm8, dword ptr [rip + 0x1b91b24]  ; -> 02064C84
004D3160  movss    xmm7, dword ptr [rip + 0x1b91b18]  ; -> 02064C80
004D3168  movss    xmm9, dword ptr [rip + 0x1b91b17]  ; -> 02064C88
004D3171  movss    xmm10, dword ptr [rip + 0x1b91b12]  ; -> 02064C8C
004D317A  movss    xmm12, dword ptr [rip + 0x1b91b11]  ; -> 02064C94
004D3183  movss    xmm11, dword ptr [rip + 0x1b91b04]  ; -> 02064C90
004D318C  shl      eax, 4
004D318F  movsxd   r15, eax
004D3192  mulss    xmm3, xmm1
004D3196  mulss    xmm2, xmm1
004D319A  movups   xmmword ptr [r15 + rbp], xmm0
004D319F  mulss    xmm4, xmm1
004D31A3  mulss    xmm5, xmm1
004D31A7  mulss    xmm8, xmm1
004D31AC  mulss    xmm7, xmm1
004D31B0  mulss    xmm9, xmm1
004D31B5  mulss    xmm10, xmm1
004D31BA  mulss    xmm12, xmm1
004D31BF  mulss    xmm11, xmm1
004D31C4  movss    xmm13, dword ptr [rip + 0x1b91acb]  ; -> 02064C98
004D31CD  movss    xmm14, dword ptr [rip + 0x1b91ac6]  ; -> 02064C9C
004D31D6  addss    xmm2, dword ptr [rip + 0x1b91982]  ; -> 02064B60
004D31DE  addss    xmm3, dword ptr [rip + 0x1b9197e]  ; -> 02064B64
004D31E6  addss    xmm4, dword ptr [rip + 0x1b9197a]  ; -> 02064B68
004D31EE  addss    xmm5, dword ptr [rip + 0x1b91976]  ; -> 02064B6C
004D31F6  addss    xmm7, dword ptr [rip + 0x1b91972]  ; -> 02064B70
004D31FE  addss    xmm8, dword ptr [rip + 0x1b9196d]  ; -> 02064B74
004D3207  addss    xmm9, dword ptr [rip + 0x1b91968]  ; -> 02064B78
004D3210  addss    xmm10, dword ptr [rip + 0x1b91963]  ; -> 02064B7C
004D3219  addss    xmm11, dword ptr [rip + 0x1b9195e]  ; -> 02064B80
004D3222  addss    xmm12, dword ptr [rip + 0x1b91959]  ; -> 02064B84
004D322B  mulss    xmm13, xmm1
004D3230  mulss    xmm14, xmm1
004D3235  addss    xmm13, dword ptr [rip + 0x1b9194a]  ; -> 02064B88
004D323E  addss    xmm14, dword ptr [rip + 0x1b91945]  ; -> 02064B8C
004D3247  movups   xmm0, xmmword ptr [rip + 0x1b91a72]  ; -> 02064CC0
004D324E  lea      eax, [rbx + 0x14]
004D3251  movdqu   xmm1, xmmword ptr [rip + 0x1b919c7]  ; -> 02064C20
004D3259  shl      eax, 4
004D325C  movsxd   r12, eax
004D325F  mov      eax, ebx
004D3261  shl      eax, 4
004D3264  movsxd   rcx, eax
004D3267  lea      eax, [rbx + 6]
004D326A  shl      eax, 4
004D326D  movups   xmmword ptr [r12 + rbp], xmm0
004D3272  movups   xmm0, xmmword ptr [rip + 0x1b91997]  ; -> 02064C10
004D3279  movss    dword ptr [rip + 0x1b919f3], xmm3  ; -> 02064C74
004D3281  movups   xmmword ptr [rcx + rbp], xmm0
004D3285  movsxd   rcx, eax
004D3288  lea      eax, [rbx + 0xc]
004D328B  movups   xmm0, xmmword ptr [rip + 0x1b9199e]  ; -> 02064C30
004D3292  shl      eax, 4
004D3295  movss    dword ptr [rip + 0x1b919d3], xmm2  ; -> 02064C70
004D329D  movups   xmmword ptr [rcx + rbp], xmm1
004D32A1  movsxd   rcx, eax
004D32A4  lea      eax, [rbx + 0x12]
004D32A7  shl      eax, 4
004D32AA  comiss   xmm6, xmm2
004D32AD  movups   xmmword ptr [rcx + rbp], xmm0
004D32B1  movsxd   rcx, eax
004D32B4  movss    dword ptr [rip + 0x1b919df], xmm14  ; -> 02064C9C
004D32BD  movss    dword ptr [rip + 0x1b919d2], xmm13  ; -> 02064C98
004D32C6  movss    dword ptr [rip + 0x1b919c5], xmm12  ; -> 02064C94
004D32CF  movups   xmmword ptr [rcx + rbp], xmm1
004D32D3  movss    dword ptr [rip + 0x1b919b4], xmm11  ; -> 02064C90
004D32DC  movss    dword ptr [rip + 0x1b919a7], xmm10  ; -> 02064C8C
004D32E5  movss    dword ptr [rip + 0x1b9199a], xmm9  ; -> 02064C88
004D32EE  movss    dword ptr [rip + 0x1b9198d], xmm8  ; -> 02064C84
004D32F7  movss    dword ptr [rip + 0x1b91981], xmm7  ; -> 02064C80
004D32FF  movss    dword ptr [rip + 0x1b91975], xmm5  ; -> 02064C7C
004D3307  movss    dword ptr [rip + 0x1b91969], xmm4  ; -> 02064C78
004D330F  ja       0x4d331b  ; -> 004D331B
004D3311  mov      dword ptr [rip + 0x1b91955], 0x437f0000  ; -> 02064C70
004D331B  comiss   xmm6, xmm3
004D331E  ja       0x4d332a  ; -> 004D332A
004D3320  mov      dword ptr [rip + 0x1b9194a], 0x437f0000  ; -> 02064C74
004D332A  comiss   xmm6, xmm4
004D332D  ja       0x4d3339  ; -> 004D3339
004D332F  mov      dword ptr [rip + 0x1b9193f], 0x437f0000  ; -> 02064C78
004D3339  comiss   xmm6, xmm5
004D333C  ja       0x4d3348  ; -> 004D3348
004D333E  mov      dword ptr [rip + 0x1b91934], 0x437f0000  ; -> 02064C7C
004D3348  comiss   xmm6, xmm7
004D334B  ja       0x4d3357  ; -> 004D3357
004D334D  mov      dword ptr [rip + 0x1b91929], 0x437f0000  ; -> 02064C80
004D3357  comiss   xmm6, xmm8
004D335B  ja       0x4d3367  ; -> 004D3367
004D335D  mov      dword ptr [rip + 0x1b9191d], 0x437f0000  ; -> 02064C84
004D3367  comiss   xmm6, xmm9
004D336B  ja       0x4d3377  ; -> 004D3377
004D336D  mov      dword ptr [rip + 0x1b91911], 0x437f0000  ; -> 02064C88
004D3377  comiss   xmm6, xmm10
004D337B  ja       0x4d3387  ; -> 004D3387
004D337D  mov      dword ptr [rip + 0x1b91905], 0x437f0000  ; -> 02064C8C
004D3387  comiss   xmm6, xmm11
004D338B  ja       0x4d3397  ; -> 004D3397
004D338D  mov      dword ptr [rip + 0x1b918f9], 0x437f0000  ; -> 02064C90
004D3397  comiss   xmm6, xmm12
004D339B  ja       0x4d33a7  ; -> 004D33A7
004D339D  mov      dword ptr [rip + 0x1b918ed], 0x437f0000  ; -> 02064C94
004D33A7  comiss   xmm6, xmm13
004D33AB  ja       0x4d33b7  ; -> 004D33B7
004D33AD  mov      dword ptr [rip + 0x1b918e1], 0x437f0000  ; -> 02064C98
004D33B7  comiss   xmm6, xmm14
004D33BB  ja       0x4d33c7  ; -> 004D33C7
004D33BD  mov      dword ptr [rip + 0x1b918d5], 0x437f0000  ; -> 02064C9C
004D33C7  movsx    r11d, word ptr [rip + 0x1b91a09]  ; -> 02064DD8
004D33CF  movups   xmm1, xmmword ptr [rip + 0x1b918aa]  ; -> 02064C80
004D33D6  movzx    r10d, word ptr [rip + 0x1b9172e]  ; -> 02064B0C
004D33DE  mov      r8d, r11d
004D33E1  movups   xmm0, xmmword ptr [rip + 0x1b91888]  ; -> 02064C70
004D33E8  lea      eax, [r11 + 0x64]
004D33EC  movss    xmm14, dword ptr [rip + 0x181877b]  ; -> 01CEBB70 [f32 0.5]
004D33F5  movss    xmm2, dword ptr [rip + 0x192f437]  ; -> 01E02834 [u32 0x00000000]
004D33FD  shl      eax, 4
004D3400  movsxd   rcx, eax
004D3403  lea      eax, [r11 + 0xfa]
004D340A  shl      eax, 4
004D340D  movsxd   rdx, eax
004D3410  lea      eax, [r11 + 0x190]
004D3417  shl      eax, 4
004D341A  movups   xmm9, xmmword ptr [rcx + rbp]
004D341F  movsxd   rcx, eax
004D3422  movzx    r8d, word ptr [rdx + rbp + 0xc]
004D3428  movsx    eax, word ptr [rip + 0x1b9199d]  ; -> 02064DCC
004D342F  cvttps2dq xmm0, xmm0
004D3433  mov      word ptr [rip + 0x1b9198d], r8w  ; -> 02064DC8
004D343B  movups   xmm10, xmmword ptr [rcx + rbp]
004D3440  movzx    ecx, r8w
004D3444  movups   xmmword ptr [rip + 0x1b91864], xmm9  ; -> 02064CB0
004D344C  or       cx, ax
004D344F  movss    xmm5, dword ptr [rip + 0x1b9185d]  ; -> 02064CB4
004D3457  cmp      word ptr [rip + 0x1b9197d], r10w  ; -> 02064DDC
004D345F  movss    xmm7, dword ptr [rip + 0x1b91849]  ; -> 02064CB0
004D3467  movups   xmmword ptr [rip + 0x1b91861], xmm10  ; -> 02064CD0
004D346F  mov      word ptr [rip + 0x1b91956], cx  ; -> 02064DCC
004D3476  movss    xmm8, dword ptr [rip + 0x1b91855]  ; -> 02064CD4
004D347F  movss    xmm11, dword ptr [rip + 0x1b91848]  ; -> 02064CD0
004D3488  movups   xmmword ptr [rip + 0x1b917e1], xmm0  ; -> 02064C70
004D348F  movups   xmm0, xmmword ptr [rdx + rbp]
004D3493  cvttps2dq xmm3, xmm1
004D3497  movups   xmm1, xmmword ptr [rip + 0x1b917f2]  ; -> 02064C90
004D349E  movups   xmmword ptr [rip + 0x1b9181b], xmm0  ; -> 02064CC0
004D34A5  movss    xmm12, dword ptr [rip + 0x1b91816]  ; -> 02064CC4
004D34AE  movss    xmm13, dword ptr [rip + 0x1b91809]  ; -> 02064CC0
004D34B7  shufps   xmm10, xmm10, 0xff
004D34BC  movaps   xmm4, xmm10
004D34C0  shufps   xmm9, xmm9, 0xff
004D34C5  addss    xmm4, xmm9
004D34CA  movss    dword ptr [rsp + 0x34], xmm5
004D34D0  cvttps2dq xmm0, xmm1
004D34D4  mulss    xmm4, xmm14
004D34D9  movss    dword ptr [rsp + 0x138], xmm7
004D34E2  movss    dword ptr [rsp + 0x2c], xmm12
004D34E9  movss    dword ptr [rip + 0x1b917db], xmm4  ; -> 02064CCC
004D34F1  movss    dword ptr [rsp + 0x30], xmm13
004D34F8  movss    dword ptr [rsp + 0x24], xmm8
004D34FF  movss    dword ptr [rsp + 0x28], xmm11
004D3506  movss    dword ptr [rsp + 0x130], xmm2
004D350F  movups   xmmword ptr [rip + 0x1b9176a], xmm3  ; -> 02064C80
004D3516  movups   xmmword ptr [rip + 0x1b91773], xmm0  ; -> 02064C90
004D351D  jne      0x4d36cf  ; -> 004D36CF
004D3523  cmp      word ptr [rip + 0x1b91899], r10w  ; -> 02064DC4
004D352B  movss    xmm5, dword ptr [rip + 0x1b917e1]  ; -> 02064D14
004D3533  movss    xmm0, dword ptr [rip + 0x1b917e1]  ; -> 02064D1C
004D353B  addss    xmm5, xmm2
004D353F  movss    xmm7, dword ptr [rip + 0x1b917c9]  ; -> 02064D10
004D3547  movaps   xmm1, xmm0
004D354A  addss    xmm7, dword ptr [rip + 0x192f2de]  ; -> 01E02830 [u32 0x00000000]
004D3552  mulss    xmm1, xmm14
004D3557  mov      dword ptr [rip + 0x1b915a3], 0x3f000000  ; -> 02064B04
004D3561  movaps   xmm12, xmm5
004D3565  movaps   xmm8, xmm5
004D3569  addss    xmm8, xmm0
004D356E  movss    xmm0, dword ptr [rip + 0x192f2c2]  ; -> 01E02838 [u32 0x00000000]
004D3576  addss    xmm12, xmm1
004D357B  movss    dword ptr [rip + 0x1b916c9], xmm1  ; -> 02064C4C
004D3583  movss    xmm1, dword ptr [rip + 0x1b9178d]  ; -> 02064D18
004D358B  addss    xmm9, xmm0
004D3590  mulss    xmm1, dword ptr [rip + 0x1b9170c]  ; -> 02064CA4
004D3598  addss    xmm10, xmm0
004D359D  movaps   xmm13, xmm7
004D35A1  movaps   xmm11, xmm7
004D35A5  movaps   xmm14, xmm0
004D35A9  addss    xmm14, xmm4
004D35AE  mulss    xmm5, xmm9
004D35B3  addss    xmm7, xmm1
004D35B7  mulss    xmm8, xmm10
004D35BC  addss    xmm13, xmm1
004D35C1  movss    dword ptr [rip + 0x1b9167b], xmm1  ; -> 02064C44
004D35C9  addss    xmm11, xmm1
004D35CE  mulss    xmm12, xmm14
004D35D3  mulss    xmm7, xmm9
004D35D8  mulss    xmm13, xmm14
004D35DD  mulss    xmm11, xmm10
004D35E2  movss    dword ptr [rip + 0x1b91626], xmm7  ; -> 02064C10
004D35EA  movss    dword ptr [rip + 0x1b9162d], xmm13  ; -> 02064C20
004D35F3  movss    dword ptr [rip + 0x1b91634], xmm11  ; -> 02064C30
004D35FC  movss    dword ptr [rip + 0x1b91613], xmm9  ; -> 02064C18
004D3605  movss    dword ptr [rip + 0x1b9161a], xmm14  ; -> 02064C28
004D360E  movss    dword ptr [rip + 0x1b91621], xmm10  ; -> 02064C38
004D3617  movss    dword ptr [rip + 0x1b915f5], xmm5  ; -> 02064C14
004D361F  movss    dword ptr [rip + 0x1b915fc], xmm12  ; -> 02064C24
004D3628  movss    dword ptr [rip + 0x1b91603], xmm8  ; -> 02064C34
004D3631  je       0x4d37eb  ; -> 004D37EB
004D3637  movss    xmm4, dword ptr [rip + 0x1b915dd]  ; -> 02064C1C
004D363F  movaps   xmm2, xmm5
004D3642  movss    xmm0, dword ptr [rip + 0x1b915f2]  ; -> 02064C3C
004D364A  movaps   xmm3, xmm9
004D364E  movaps   xmm1, xmm7
004D3651  movss    dword ptr [rip + 0x1b915be], xmm10  ; -> 02064C18
004D365A  movaps   xmm5, xmm8
004D365E  movss    dword ptr [rip + 0x1b9167e], xmm2  ; -> 02064CE4
004D3666  movaps   xmm9, xmm10
004D366A  movss    dword ptr [rip + 0x1b91676], xmm3  ; -> 02064CE8
004D3672  movss    dword ptr [rip + 0x1b915ba], xmm2  ; -> 02064C34
004D367A  movaps   xmm8, xmm2
004D367E  movss    xmm2, dword ptr [rsp + 0x130]
004D3687  movaps   xmm10, xmm3
004D368B  movss    dword ptr [rip + 0x1b915a5], xmm3  ; -> 02064C38
004D3693  movaps   xmm7, xmm11
004D3697  movups   xmm3, xmmword ptr [rip + 0x1b915e2]  ; -> 02064C80
004D369E  movss    dword ptr [rip + 0x1b9163a], xmm1  ; -> 02064CE0
004D36A6  movaps   xmm11, xmm1
004D36AA  movss    dword ptr [rip + 0x1b9163a], xmm4  ; -> 02064CEC
004D36B2  movss    dword ptr [rip + 0x1b91562], xmm0  ; -> 02064C1C
004D36BA  movss    dword ptr [rip + 0x1b9156e], xmm1  ; -> 02064C30
004D36C2  movss    dword ptr [rip + 0x1b91572], xmm4  ; -> 02064C3C
004D36CA  jmp      0x4d37db  ; -> 004D37DB
004D36CF  movss    xmm0, dword ptr [rip + 0x441f41]  ; -> 00915618 [f32 1792]
004D36D7  movss    xmm14, dword ptr [rip + 0x192f158]  ; -> 01E02838 [u32 0x00000000]
004D36E0  subss    xmm7, xmm0
004D36E4  addss    xmm14, dword ptr [rip + 0x192f14f]  ; -> 01E0283C [f32 1]
004D36ED  movss    xmm1, dword ptr [rip + 0x1b9161b]  ; -> 02064D10
004D36F5  subss    xmm13, xmm0
004D36FA  subss    xmm11, xmm0
004D36FF  mov      dword ptr [rip + 0x1b913fb], 0x3b000000  ; -> 02064B04
004D3709  movss    xmm0, dword ptr [rip + 0x441f0b]  ; -> 0091561C [f32 1824]
004D3711  subss    xmm5, xmm0
004D3715  subss    xmm12, xmm0
004D371A  movaps   xmm9, xmm14
004D371E  subss    xmm8, xmm0
004D3723  movaps   xmm10, xmm14
004D3727  movss    xmm0, dword ptr [rip + 0x3f2401]  ; -> 008C5B30 [f32 0.001953125]
004D372F  mulss    xmm7, xmm0
004D3733  mulss    xmm5, xmm0
004D3737  mulss    xmm12, xmm0
004D373C  addss    xmm7, xmm1
004D3740  mulss    xmm8, xmm0
004D3745  mulss    xmm13, xmm0
004D374A  mulss    xmm11, xmm0
004D374F  movss    xmm0, dword ptr [rip + 0x1b915bd]  ; -> 02064D14
004D3757  addss    xmm13, xmm1
004D375C  addss    xmm5, xmm0
004D3760  mulss    xmm7, xmm9
004D3765  addss    xmm12, xmm0
004D376A  addss    xmm8, xmm0
004D376F  mulss    xmm13, xmm14
004D3774  addss    xmm11, xmm1
004D3779  mulss    xmm5, xmm9
004D377E  mulss    xmm12, xmm14
004D3783  mulss    xmm8, xmm10
004D3788  mulss    xmm11, xmm10
004D378D  mulss    xmm9, xmm9
004D3792  mulss    xmm14, xmm14
004D3797  mulss    xmm10, xmm10
004D379C  movss    dword ptr [rip + 0x1b91473], xmm9  ; -> 02064C18
004D37A5  movss    dword ptr [rip + 0x1b9147a], xmm14  ; -> 02064C28
004D37AE  movss    dword ptr [rip + 0x1b91481], xmm10  ; -> 02064C38
004D37B7  movss    dword ptr [rip + 0x1b91460], xmm13  ; -> 02064C20
004D37C0  movss    dword ptr [rip + 0x1b9145b], xmm12  ; -> 02064C24
004D37C9  movss    dword ptr [rip + 0x1b9145e], xmm11  ; -> 02064C30
004D37D2  movss    dword ptr [rip + 0x1b91459], xmm8  ; -> 02064C34
004D37DB  movss    dword ptr [rip + 0x1b91431], xmm5  ; -> 02064C14
004D37E3  movss    dword ptr [rip + 0x1b91425], xmm7  ; -> 02064C10
004D37EB  movss    xmm0, dword ptr [rsp + 0x138]
004D37F4  mulss    xmm0, xmm15
004D37F9  cvttss2si eax, xmm0
004D37FD  movss    xmm0, dword ptr [rsp + 0x34]
004D3803  mulss    xmm0, xmm15
004D3808  mov      dword ptr [rip + 0x1b914a2], eax  ; -> 02064CB0
004D380E  cvttss2si eax, xmm0
004D3812  movss    xmm0, dword ptr [rip + 0x1b9149e]  ; -> 02064CB8
004D381A  mulss    xmm0, xmm15
004D381F  mov      dword ptr [rip + 0x1b9148f], eax  ; -> 02064CB4
004D3825  cvttss2si eax, xmm0
004D3829  movss    xmm0, dword ptr [rsp + 0x30]
004D382F  mulss    xmm0, xmm15
004D3834  mov      dword ptr [rip + 0x1b9147e], eax  ; -> 02064CB8
004D383A  cvttss2si eax, xmm0
004D383E  movss    xmm0, dword ptr [rsp + 0x2c]
004D3844  mulss    xmm0, xmm15
004D3849  mov      dword ptr [rip + 0x1b91471], eax  ; -> 02064CC0
004D384F  cvttss2si eax, xmm0
004D3853  movss    xmm0, dword ptr [rip + 0x1b9146d]  ; -> 02064CC8
004D385B  mulss    xmm0, xmm15
004D3860  mov      dword ptr [rip + 0x1b9145e], eax  ; -> 02064CC4
004D3866  cvttss2si eax, xmm0
004D386A  movss    xmm0, dword ptr [rsp + 0x28]
004D3870  mulss    xmm0, xmm15
004D3875  mov      dword ptr [rip + 0x1b9144d], eax  ; -> 02064CC8
004D387B  cvttss2si eax, xmm0
004D387F  movss    xmm0, dword ptr [rsp + 0x24]
004D3885  mulss    xmm0, xmm15
004D388A  mov      dword ptr [rip + 0x1b91440], eax  ; -> 02064CD0
004D3890  cvttss2si eax, xmm0
004D3894  movss    xmm0, dword ptr [rip + 0x1b9143c]  ; -> 02064CD8
004D389C  mulss    xmm0, xmm15
004D38A1  mov      dword ptr [rip + 0x1b9142d], eax  ; -> 02064CD4
004D38A7  cvttss2si eax, xmm0
004D38AB  mov      dword ptr [rip + 0x1b91427], eax  ; -> 02064CD8
004D38B1  cmp      r10w, cx
004D38B5  jne      0x4d3b19  ; -> 004D3B19
004D38BB  cmp      r10w, r11w
004D38BF  je       0x4d3b19  ; -> 004D3B19
004D38C5  movups   xmm0, xmmword ptr [rip + 0x1b913a4]  ; -> 02064C70
004D38CC  lea      eax, [r9 + 4]
004D38D0  movups   xmm1, xmmword ptr [rip + 0x1b913e9]  ; -> 02064CC0
004D38D7  shl      eax, 4
004D38DA  movsxd   rcx, eax
004D38DD  lea      eax, [r9 + 0xa]
004D38E1  shl      eax, 4
004D38E4  movups   xmmword ptr [rcx + rbp], xmm0
004D38E8  movsxd   rcx, eax
004D38EB  lea      eax, [r9 + 0x10]
004D38EF  movups   xmm0, xmmword ptr [rip + 0x1b9139a]  ; -> 02064C90
004D38F6  shl      eax, 4
004D38F9  movups   xmmword ptr [rcx + rbp], xmm3
004D38FD  movsxd   rcx, eax
004D3900  lea      eax, [r9 + 0x16]
004D3904  shl      eax, 4
004D3907  movups   xmmword ptr [rcx + rbp], xmm0
004D390B  movsxd   rcx, eax
004D390E  lea      eax, [r9 + 5]
004D3912  movups   xmm0, xmmword ptr [rip + 0x1b91397]  ; -> 02064CB0
004D3919  shl      eax, 4
004D391C  movsxd   r11, eax
004D391F  lea      eax, [r9 + 0xb]
004D3923  shl      eax, 4
004D3926  movsxd   rdi, eax
004D3929  lea      eax, [r9 + 0x11]
004D392D  shl      eax, 4
004D3930  movups   xmmword ptr [rcx + rbp], xmm3
004D3934  movsxd   rsi, eax
004D3937  lea      eax, [r9 + 0x17]
004D393B  movups   xmmword ptr [r11 + rbp], xmm0
004D3940  shl      eax, 4
004D3943  cmp      word ptr [rip + 0x1b91495], r10w  ; -> 02064DE0
004D394B  movups   xmm0, xmmword ptr [rip + 0x1b9137e]  ; -> 02064CD0
004D3952  movsxd   r14, eax
004D3955  movups   xmmword ptr [rdi + rbp], xmm1
004D3959  movups   xmmword ptr [rsi + rbp], xmm0
004D395D  movups   xmmword ptr [r14 + rbp], xmm1
004D3962  je       0x4d3a43  ; -> 004D3A43
004D3968  movss    xmm0, dword ptr [rip + 0x1b912ac]  ; -> 02064C1C
004D3970  movaps   xmm1, xmm2
004D3973  movss    dword ptr [rip + 0x1b91371], xmm0  ; -> 02064CEC
004D397B  addss    xmm1, xmm7
004D397F  movss    xmm0, dword ptr [rip + 0x1b912a5]  ; -> 02064C2C
004D3987  movss    dword ptr [rip + 0x1b9136d], xmm0  ; -> 02064CFC
004D398F  movss    xmm0, dword ptr [rip + 0x1b912a5]  ; -> 02064C3C
004D3997  movss    dword ptr [rip + 0x1b9136d], xmm0  ; -> 02064D0C
004D399F  movaps   xmm0, xmm2
004D39A2  addss    xmm0, xmm13
004D39A7  movss    dword ptr [rip + 0x1b91335], xmm5  ; -> 02064CE4
004D39AF  movss    dword ptr [rip + 0x1b9133c], xmm12  ; -> 02064CF4
004D39B8  addss    xmm2, xmm11
004D39BD  movss    dword ptr [rip + 0x1b9133e], xmm8  ; -> 02064D04
004D39C6  movss    dword ptr [rip + 0x1b91312], xmm7  ; -> 02064CE0
004D39CE  movss    dword ptr [rip + 0x1b91311], xmm9  ; -> 02064CE8
004D39D7  movss    dword ptr [rip + 0x1b91245], xmm0  ; -> 02064C24
004D39DF  movss    xmm0, dword ptr [rip + 0x192ee49]  ; -> 01E02830 [u32 0x00000000]
004D39E7  addss    xmm5, xmm0
004D39EB  movss    dword ptr [rip + 0x1b912fc], xmm13  ; -> 02064CF0
004D39F4  addss    xmm12, xmm0
004D39F9  movss    dword ptr [rip + 0x1b912f6], xmm14  ; -> 02064CF8
004D3A02  addss    xmm8, xmm0
004D3A07  movss    dword ptr [rip + 0x1b912f0], xmm11  ; -> 02064D00
004D3A10  movss    dword ptr [rip + 0x1b912ef], xmm10  ; -> 02064D08
004D3A19  movss    dword ptr [rip + 0x1b911f3], xmm1  ; -> 02064C14
004D3A21  movss    dword ptr [rip + 0x1b911e7], xmm5  ; -> 02064C10
004D3A29  movss    dword ptr [rip + 0x1b911ee], xmm12  ; -> 02064C20
004D3A32  movss    dword ptr [rip + 0x1b911f5], xmm8  ; -> 02064C30
004D3A3B  movss    dword ptr [rip + 0x1b911f1], xmm2  ; -> 02064C34
004D3A43  movzx    r8d, word ptr [rip + 0x1b91371]  ; -> 02064DBC
004D3A4B  lea      eax, [r9 + 3]
004D3A4F  movups   xmm0, xmmword ptr [rip + 0x1b911ba]  ; -> 02064C10
004D3A56  add      word ptr [rip + 0x1b9135a], 4  ; -> 02064DB8
004D3A5E  add      bx, 0x17
004D3A62  movdqu   xmm1, xmmword ptr [rip + 0x1b911b6]  ; -> 02064C20
004D3A6A  shl      eax, 4
004D3A6D  movsxd   rcx, eax
004D3A70  lea      eax, [r9 + 9]
004D3A74  shl      eax, 4
004D3A77  movzx    edx, r10w
004D3A7B  mov      word ptr [rip + 0x1b91332], bx  ; -> 02064DB4
004D3A82  movups   xmmword ptr [rcx + rbp], xmm0
004D3A86  movsxd   rcx, eax
004D3A89  lea      eax, [r9 + 0xf]
004D3A8D  movups   xmm0, xmmword ptr [rip + 0x1b9119c]  ; -> 02064C30
004D3A94  shl      eax, 4
004D3A97  movups   xmmword ptr [rcx + rbp], xmm1
004D3A9B  movsxd   rcx, eax
004D3A9E  lea      eax, [r9 + 0x15]
004D3AA2  shl      eax, 4
004D3AA5  movups   xmmword ptr [rcx + rbp], xmm0
004D3AA9  movsxd   rcx, eax
004D3AAC  lea      eax, [r9 + 2]
004D3AB0  shl      eax, 4
004D3AB3  movups   xmmword ptr [rcx + rbp], xmm1
004D3AB7  movsxd   rcx, eax
004D3ABA  lea      eax, [r9 + 8]
004D3ABE  shl      eax, 4
004D3AC1  mov      dword ptr [rcx + rbp + 0xc], r8d
004D3AC6  movsxd   rcx, eax
004D3AC9  mov      dword ptr [rcx + rbp + 0xc], edx
004D3ACD  mov      rcx, qword ptr [rsp + 0x120]
004D3AD5  mov      dword ptr [r15 + rbp + 0xc], r8d
004D3ADA  mov      dword ptr [r12 + rbp + 0xc], edx
004D3ADF  mov      dword ptr [r11 + rbp + 0xc], r8d
004D3AE4  mov      dword ptr [rdi + rbp + 0xc], edx
004D3AE8  mov      dword ptr [rsi + rbp + 0xc], r8d
004D3AED  mov      dword ptr [r14 + rbp + 0xc], edx
004D3AF2  mov      rdx, r13
004D3AF5  call     0x4df360  ; -> 004DF360 fn
004D3AFA  movzx    r10d, word ptr [rip + 0x1b9100a]  ; -> 02064B0C
004D3B02  movzx    r11d, word ptr [rip + 0x1b912ce]  ; -> 02064DD8
004D3B0A  movzx    r8d, word ptr [rip + 0x1b912b6]  ; -> 02064DC8
004D3B12  movzx    ebx, word ptr [rip + 0x1b9129b]  ; -> 02064DB4
004D3B19  movss    xmm7, dword ptr [rip + 0x1b91133]  ; -> 02064C54
004D3B21  movss    xmm0, dword ptr [rip + 0x1b9117b]  ; -> 02064CA4
004D3B29  movzx    r9d, word ptr [rip + 0x1b912a3]  ; -> 02064DD4
004D3B31  movsx    edx, r11w
004D3B35  inc      r11w
004D3B39  mov      word ptr [rip + 0x1b91297], r11w  ; -> 02064DD8
004D3B41  lea      eax, [rdx + 0x28b]
004D3B47  shl      eax, 4
004D3B4A  movsxd   rcx, eax
004D3B4D  lea      eax, [rdx + 0x227]
004D3B53  shl      eax, 4
004D3B56  movups   xmm2, xmmword ptr [rcx + rbp]
004D3B5A  movsxd   rcx, eax
004D3B5D  movsx    eax, r10w
004D3B61  movups   xmmword ptr [rip + 0x1b91178], xmm2  ; -> 02064CE0
004D3B68  add      r8w, ax
004D3B6C  shufps   xmm2, xmm2, 0x55
004D3B70  movss    dword ptr [rip + 0x1b9116c], xmm2  ; -> 02064CE4
004D3B78  addss    xmm7, xmm2
004D3B7C  mov      word ptr [rip + 0x1b91248], r8w  ; -> 02064DCC
004D3B84  movups   xmm1, xmmword ptr [rcx + rbp]
004D3B88  movss    dword ptr [rip + 0x1b910c4], xmm7  ; -> 02064C54
004D3B90  movups   xmmword ptr [rip + 0x1b91159], xmm1  ; -> 02064CF0
004D3B97  shufps   xmm1, xmm1, 0x55
004D3B9B  mulss    xmm1, dword ptr [rip + 0x1b910fd]  ; -> 02064CA0
004D3BA3  movss    dword ptr [rip + 0x1b91149], xmm1  ; -> 02064CF4
004D3BAB  addss    xmm0, xmm1
004D3BAF  movss    dword ptr [rip + 0x1b910ed], xmm0  ; -> 02064CA4
004D3BB7  cmp      r9w, r10w
004D3BBB  je       0x4d3be5  ; -> 004D3BE5
004D3BBD  movss    xmm4, dword ptr [rip + 0x1b90fcb]  ; -> 02064B90
004D3BC5  movss    xmm9, dword ptr [rip + 0x1b9100a]  ; -> 02064BD8
004D3BCE  movss    xmm8, dword ptr [rip + 0x1b91015]  ; -> 02064BEC
004D3BD7  movss    xmm10, dword ptr [rip + 0x1b91000]  ; -> 02064BE0
004D3BE0  jmp      0x4d2c80  ; -> 004D2C80
004D3BE5  mov      r15, qword ptr [rsp + 0xe0]
004D3BED  mov      r12, qword ptr [rsp + 0x128]
004D3BF5  jmp      0x4d3d14  ; -> 004D3D14
004D3BFA  movsx    ecx, word ptr [rip + 0x1b90f0b]  ; -> 02064B0C
004D3C01  lea      rbp, [rip + 0x1b91228]  ; -> 02064E30
004D3C08  lea      eax, [rcx + 3]
004D3C0B  shl      eax, 4
004D3C0E  movsxd   rsi, eax
004D3C11  lea      eax, [rcx + 4]
004D3C14  shl      eax, 4
004D3C17  movsxd   rdi, eax
004D3C1A  lea      eax, [rcx + 5]
004D3C1D  shl      eax, 4
004D3C20  movups   xmm0, xmmword ptr [rsi + rbp]
004D3C24  movsxd   rbx, eax
004D3C27  lea      eax, [rcx + 6]
004D3C2A  movups   xmm2, xmmword ptr [rdi + rbp]
004D3C2E  shl      eax, 4
004D3C31  movsxd   r11, eax
004D3C34  lea      eax, [rcx + 7]
004D3C37  movups   xmm3, xmmword ptr [rbx + rbp]
004D3C3B  shl      eax, 4
004D3C3E  movsxd   r10, eax
004D3C41  lea      eax, [rcx + 8]
004D3C44  movups   xmm4, xmmword ptr [r11 + rbp]
004D3C49  shl      eax, 4
004D3C4C  movsxd   r9, eax
004D3C4F  lea      eax, [rcx + 9]
004D3C52  shl      eax, 4
004D3C55  movsxd   r8, eax
004D3C58  lea      eax, [rcx + 0xa]
004D3C5B  cvtdq2ps xmm10, xmm0
004D3C5F  shl      eax, 4
004D3C62  movsxd   rdx, eax
004D3C65  lea      eax, [rcx + 0xb]
004D3C68  shl      eax, 4
004D3C6B  movsxd   rcx, eax
004D3C6E  movups   xmm0, xmmword ptr [r10 + rbp]
004D3C73  movups   xmm5, xmmword ptr [r9 + rbp]
004D3C78  cvtdq2ps xmm9, xmm2
004D3C7C  movups   xmm2, xmmword ptr [rdx + rbp]
004D3C80  cvtdq2ps xmm8, xmm3
004D3C84  movups   xmm3, xmmword ptr [r8 + rbp]
004D3C89  cvtdq2ps xmm7, xmm4
004D3C8C  cvtdq2ps xmm6, xmm0
004D3C8F  movups   xmm0, xmmword ptr [rcx + rbp]
004D3C93  movups   xmmword ptr [rsi + rbp], xmm10
004D3C98  movups   xmmword ptr [rdi + rbp], xmm9
004D3C9D  movups   xmmword ptr [rbx + rbp], xmm8
004D3CA2  movups   xmmword ptr [r11 + rbp], xmm7
004D3CA7  movups   xmmword ptr [r10 + rbp], xmm6
004D3CAC  cvtdq2ps xmm4, xmm3
004D3CAF  cvtdq2ps xmm3, xmm2
004D3CB2  cvtdq2ps xmm5, xmm5
004D3CB5  cvtdq2ps xmm2, xmm0
004D3CB8  movups   xmmword ptr [r9 + rbp], xmm5
004D3CBD  movups   xmmword ptr [r8 + rbp], xmm4
004D3CC2  movups   xmmword ptr [rdx + rbp], xmm3
004D3CC6  movdqu   xmmword ptr [rip + 0x1b90f72], xmm2  ; -> 02064C40
004D3CCE  movups   xmmword ptr [rcx + rbp], xmm2
004D3CD2  movdqu   xmmword ptr [rip + 0x1b90ee5], xmm10  ; -> 02064BC0
004D3CDB  movdqu   xmmword ptr [rip + 0x1b90eec], xmm9  ; -> 02064BD0
004D3CE4  movdqu   xmmword ptr [rip + 0x1b90ef3], xmm8  ; -> 02064BE0
004D3CED  movdqu   xmmword ptr [rip + 0x1b90efb], xmm7  ; -> 02064BF0
004D3CF5  movdqu   xmmword ptr [rip + 0x1b90f03], xmm6  ; -> 02064C00
004D3CFD  movups   xmmword ptr [rip + 0x1b90f0c], xmm5  ; -> 02064C10
004D3D04  movdqu   xmmword ptr [rip + 0x1b90f14], xmm4  ; -> 02064C20
004D3D0C  movdqu   xmmword ptr [rip + 0x1b90f1c], xmm3  ; -> 02064C30
004D3D14  movaps   xmm13, xmmword ptr [rsp + 0x60]
004D3D1A  lea      r11, [rsp + 0xe8]
004D3D22  movaps   xmm6, xmmword ptr [r11 - 0x18]
004D3D27  movaps   xmm7, xmmword ptr [r11 - 0x28]
004D3D2C  movaps   xmm8, xmmword ptr [r11 - 0x38]
004D3D31  movaps   xmm9, xmmword ptr [r11 - 0x48]
004D3D36  movaps   xmm10, xmmword ptr [r11 - 0x58]
004D3D3B  movaps   xmm11, xmmword ptr [r11 - 0x68]
004D3D40  movaps   xmm12, xmmword ptr [r11 - 0x78]
004D3D45  movaps   xmm14, xmmword ptr [rsp + 0x50]
004D3D4B  movaps   xmm15, xmmword ptr [rsp + 0x40]
004D3D51  mov      rsp, r11
004D3D54  pop      r14
004D3D56  pop      r13
004D3D58  pop      rdi
004D3D59  pop      rsi
004D3D5A  pop      rbp
004D3D5B  pop      rbx
004D3D5C  ret      
```

## 004DB350 (4953 B, extent 004DB350-004DC6A9)

Page context: "0x1C' = 0x6C150000 - a module record's init.  Interior anchor '004DCA17' (function '004DCA00').  '004DC6B0' (498 B) is a battery constructor '0037E0F0' calls: '00861EC0' zeroes, '008631E0' registers '004DB350', '008631D0(0x11)' fills '+0x10', '004DC8B0' runs mid-fill, then '+0xC' = 0x02000000, '+0x18' = 0x1000404, '+0x1C' = 0x6C0E0000 - a module record's init.  Interior anchor '004DC6C1' (function '004DC6B0').  '004C4A50' (494 B) is the"

```
004DB350  mov      rax, rsp
004DB353  mov      qword ptr [rax + 0x10], rbx
004DB357  push     rbp
004DB358  push     rsi
004DB359  push     rdi
004DB35A  push     r12
004DB35C  push     r13
004DB35E  push     r14
004DB360  push     r15
004DB362  sub      rsp, 0xd0
004DB369  movaps   xmmword ptr [rax - 0x48], xmm6
004DB36D  lea      r14, [rip + 0x1b89abc]  ; -> 02064E30
004DB374  movaps   xmmword ptr [rax - 0x58], xmm7
004DB378  mov      r12, rcx
004DB37B  movaps   xmmword ptr [rax - 0x68], xmm8
004DB380  xor      r8d, r8d
004DB383  movaps   xmmword ptr [rax - 0x78], xmm9
004DB388  mov      r15, rdx
004DB38B  movaps   xmmword ptr [rax - 0x88], xmm10
004DB393  movzx    eax, word ptr [rip + 0x1b89772]  ; -> 02064B0C
004DB39A  add      ax, 0xb
004DB39E  movaps   xmmword ptr [rsp + 0x70], xmm11
004DB3A4  mov      word ptr [rip + 0x1b89a3d], ax  ; -> 02064DE8
004DB3AB  movaps   xmmword ptr [rsp + 0x60], xmm12
004DB3B1  cwde     
004DB3B2  shl      eax, 4
004DB3B5  movsxd   rcx, eax
004DB3B8  movaps   xmmword ptr [rsp + 0x50], xmm13
004DB3BE  add      rcx, r14
004DB3C1  movaps   xmmword ptr [rsp + 0x40], xmm14
004DB3C7  movaps   xmmword ptr [rsp + 0x30], xmm15
004DB3CD  call     r12
004DB3D0  movsx    r8d, word ptr [rip + 0x1b89734]  ; -> 02064B0C
004DB3D8  xorps    xmm6, xmm6
004DB3DB  movss    xmm14, dword ptr [rip + 0x1927458]  ; -> 01E0283C [f32 1]
004DB3E4  mov      r9d, r8d
004DB3E7  movss    xmm12, dword ptr [rip + 0x424f70]  ; -> 00900360 [u32 0x7F7FFFFF]
004DB3F0  mov      edx, r8d
004DB3F3  shl      r9d, 4
004DB3F7  lea      eax, [r8 + 3]
004DB3FB  mov      word ptr [rip + 0x1b899b5], r8w  ; -> 02064DB8
004DB403  shl      eax, 4
004DB406  movsxd   rcx, eax
004DB409  mov      eax, 0x334
004DB40E  add      eax, r8d
004DB411  mov      word ptr [rip + 0x1b899b7], r8w  ; -> 02064DD0
004DB419  mov      word ptr [rip + 0x1b89990], ax  ; -> 02064DB0
004DB420  inc      ax
004DB423  mov      word ptr [rip + 0x1b8998a], ax  ; -> 02064DB4
004DB42A  movups   xmm0, xmmword ptr [rcx + r14]
004DB42F  movsxd   rax, r9d
004DB432  movups   xmmword ptr [rip + 0x1b89727], xmm0  ; -> 02064B60
004DB439  movss    xmm2, dword ptr [rip + 0x1b89727]  ; -> 02064B68
004DB441  movups   xmm1, xmm0
004DB444  movzx    eax, word ptr [rax + r14 + 0xc]
004DB44A  subss    xmm2, dword ptr [rip + 0x1b8970e]  ; -> 02064B60
004DB452  shufps   xmm1, xmm1, 0x55
004DB456  shufps   xmm0, xmm0, 0xff
004DB45A  subss    xmm0, xmm1
004DB45E  mov      word ptr [rip + 0x1b8996f], ax  ; -> 02064DD4
004DB465  lea      eax, [r8 + 0x14]
004DB469  ucomiss  xmm2, xmm6
004DB46C  mov      word ptr [rip + 0x1b89949], ax  ; -> 02064DBC
004DB473  movss    dword ptr [rip + 0x1b896f1], xmm0  ; -> 02064B6C
004DB47B  jp       0x4db485  ; -> 004DB485
004DB47D  jne      0x4db485  ; -> 004DB485
004DB47F  movaps   xmm3, xmm12
004DB483  jmp      0x4db48d  ; -> 004DB48D
004DB485  movaps   xmm3, xmm14
004DB489  divss    xmm3, xmm2
004DB48D  lea      eax, [rdx + 4]
004DB490  movss    dword ptr [rip + 0x1b89668], xmm3  ; -> 02064B00
004DB498  shl      eax, 4
004DB49B  movsxd   rcx, eax
004DB49E  lea      eax, [rdx + 5]
004DB4A1  shl      eax, 4
004DB4A4  mov      word ptr [rip + 0x1b89918], r8w  ; -> 02064DC4
004DB4AC  movups   xmm1, xmmword ptr [rcx + r14]
004DB4B1  movsxd   rcx, eax
004DB4B4  lea      eax, [r9 + 0x10]
004DB4B8  cvtdq2ps xmm1, xmm1
004DB4BB  movups   xmm2, xmmword ptr [rcx + r14]
004DB4C0  movsxd   rcx, eax
004DB4C3  lea      eax, [rdx + 0xa]
004DB4C6  shl      eax, 4
004DB4C9  movups   xmmword ptr [rip + 0x1b896f0], xmm1  ; -> 02064BC0
004DB4D0  movups   xmm0, xmmword ptr [rcx + r14]
004DB4D5  movsxd   rcx, eax
004DB4D8  lea      eax, [rdx + 6]
004DB4DB  shl      eax, 4
004DB4DE  movups   xmmword ptr [rip + 0x1b8964b], xmm0  ; -> 02064B30
004DB4E5  movups   xmm0, xmmword ptr [rcx + r14]
004DB4EA  movsxd   rcx, eax
004DB4ED  lea      eax, [rdx + 7]
004DB4F0  shl      eax, 4
004DB4F3  movups   xmmword ptr [rip + 0x1b89656], xmm0  ; -> 02064B50
004DB4FA  movups   xmm0, xmmword ptr [rcx + r14]
004DB4FF  movsxd   rcx, eax
004DB502  lea      eax, [rdx + 8]
004DB505  shl      eax, 4
004DB508  movups   xmmword ptr [rip + 0x1b897d1], xmm0  ; -> 02064CE0
004DB50F  movups   xmm0, xmmword ptr [rcx + r14]
004DB514  movsxd   rcx, eax
004DB517  lea      eax, [rdx + 9]
004DB51A  shl      eax, 4
004DB51D  movups   xmmword ptr [rip + 0x1b897cc], xmm0  ; -> 02064CF0
004DB524  movups   xmm0, xmmword ptr [rcx + r14]
004DB529  movsxd   rcx, eax
004DB52C  lea      eax, [rdx + 2]
004DB52F  shl      eax, 4
004DB532  movups   xmmword ptr [rip + 0x1b897c7], xmm0  ; -> 02064D00
004DB539  movups   xmm0, xmmword ptr [rcx + r14]
004DB53E  movsxd   rcx, eax
004DB541  movups   xmmword ptr [rip + 0x1b897c8], xmm0  ; -> 02064D10
004DB548  movzx    r9d, word ptr [rcx + r14]
004DB54D  cvtdq2ps xmm0, xmm2
004DB550  mov      word ptr [rip + 0x1b89868], r9w  ; -> 02064DC0
004DB558  movups   xmmword ptr [rip + 0x1b89671], xmm0  ; -> 02064BD0
004DB55F  movss    xmm0, dword ptr [rip + 0x19272d1]  ; -> 01E02838 [u32 0x00000000]
004DB567  addss    xmm0, xmm3
004DB56B  ucomiss  xmm0, xmm6
004DB56E  movss    dword ptr [rip + 0x1b895f2], xmm0  ; -> 02064B68
004DB576  jp       0x4db5a0  ; -> 004DB5A0
004DB578  jne      0x4db5a0  ; -> 004DB5A0
004DB57A  call     0x22cc40  ; -> 0022CC40 fn
004DB57F  movss    xmm0, dword ptr [rip + 0x1b895e1]  ; -> 02064B68
004DB587  movzx    r9d, word ptr [rip + 0x1b89831]  ; -> 02064DC0
004DB58F  movzx    r8d, word ptr [rip + 0x1b8982d]  ; -> 02064DC4
004DB597  movss    xmm14, dword ptr [rip + 0x192729c]  ; -> 01E0283C [f32 1]
004DB5A0  comiss   xmm6, xmm0
004DB5A3  jbe      0x4db5c3  ; -> 004DB5C3
004DB5A5  call     0x22cc30  ; -> 0022CC30 fn
004DB5AA  movzx    r9d, word ptr [rip + 0x1b8980e]  ; -> 02064DC0
004DB5B2  movzx    r8d, word ptr [rip + 0x1b8980a]  ; -> 02064DC4
004DB5BA  movss    xmm14, dword ptr [rip + 0x1927279]  ; -> 01E0283C [f32 1]
004DB5C3  xor      r13d, r13d
004DB5C6  movsd    xmm15, qword ptr [rip + 0x18107b1]  ; -> 01CEBD80 [u64 0x7FFFFFFFFFFFFFFF]
004DB5CF  mov      edi, 0xe0
004DB5D4  movsx    edx, r8w
004DB5D8  add      r8w, 4
004DB5DD  mov      word ptr [rip + 0x1b897df], r8w  ; -> 02064DC4
004DB5E5  lea      eax, [rdx + 0x14]
004DB5E8  shl      eax, 4
004DB5EB  movsxd   rcx, eax
004DB5EE  lea      eax, [rdx + 0x16]
004DB5F1  shl      eax, 4
004DB5F4  movups   xmm10, xmmword ptr [rcx + r14]
004DB5F9  movsxd   rcx, eax
004DB5FC  lea      eax, [rdx + 0x15]
004DB5FF  shl      eax, 4
004DB602  movaps   xmm4, xmm10
004DB606  movaps   xmm7, xmm10
004DB60A  shufps   xmm7, xmm10, 0xaa
004DB60F  movaps   xmm8, xmm10
004DB613  movups   xmm9, xmmword ptr [rcx + r14]
004DB618  movsxd   rcx, eax
004DB61B  lea      eax, [rdx + 0x17]
004DB61E  movaps   xmm2, xmm7
004DB621  shufps   xmm8, xmm10, 0x55
004DB626  subss    xmm7, dword ptr [rip + 0x1b8952a]  ; -> 02064B58
004DB62E  mulss    xmm2, xmm14
004DB633  movaps   xmm3, xmm8
004DB637  shl      eax, 4
004DB63A  movups   xmm5, xmmword ptr [rcx + r14]
004DB63F  movsxd   rcx, eax
004DB642  add      r9w, -2
004DB647  subss    xmm8, dword ptr [rip + 0x1b89504]  ; -> 02064B54
004DB650  movups   xmmword ptr [rip + 0x1b895c9], xmm5  ; -> 02064C20
004DB657  mov      word ptr [rip + 0x1b89761], r9w  ; -> 02064DC0
004DB65F  mulss    xmm3, xmm14
004DB664  movaps   xmm1, xmm5
004DB667  movups   xmm6, xmmword ptr [rcx + r14]
004DB66C  shufps   xmm1, xmm5, 0xff
004DB670  movaps   xmm0, xmm1
004DB673  mulss    xmm4, xmm14
004DB678  mulss    xmm0, xmm5
004DB67C  movups   xmmword ptr [rip + 0x1b895ad], xmm6  ; -> 02064C30
004DB683  addss    xmm0, xmm4
004DB687  movss    dword ptr [rip + 0x1b8959c], xmm14  ; -> 02064C2C
004DB690  movups   xmmword ptr [rip + 0x1b89558], xmm9  ; -> 02064BF0
004DB698  movups   xmmword ptr [rip + 0x1b89540], xmm10  ; -> 02064BE0
004DB6A0  subss    xmm10, dword ptr [rip + 0x1b894a7]  ; -> 02064B50
004DB6A9  movss    dword ptr [rip + 0x1b8956f], xmm0  ; -> 02064C20
004DB6B1  movaps   xmm0, xmm1
004DB6B4  mulss    xmm0, dword ptr [rip + 0x1b89568]  ; -> 02064C24
004DB6BC  mulss    xmm1, dword ptr [rip + 0x1b89564]  ; -> 02064C28
004DB6C4  addss    xmm0, xmm3
004DB6C8  movss    dword ptr [rip + 0x1b8951b], xmm14  ; -> 02064BEC
004DB6D1  movaps   xmm3, xmm9
004DB6D5  movss    dword ptr [rip + 0x1b8951e], xmm14  ; -> 02064BFC
004DB6DE  addss    xmm1, xmm2
004DB6E2  shufps   xmm3, xmm9, 0x55
004DB6E7  movaps   xmm2, xmm9
004DB6EB  mulss    xmm3, xmm14
004DB6F0  movss    dword ptr [rip + 0x1b8952c], xmm0  ; -> 02064C24
004DB6F8  mulss    xmm2, xmm14
004DB6FD  movss    dword ptr [rip + 0x1b89523], xmm1  ; -> 02064C28
004DB705  movaps   xmm1, xmm6
004DB708  shufps   xmm1, xmm6, 0xff
004DB70C  movaps   xmm0, xmm1
004DB70F  shufps   xmm9, xmm9, 0xaa
004DB714  mulss    xmm0, xmm6
004DB718  mulss    xmm9, xmm14
004DB71D  addss    xmm0, xmm2
004DB721  movss    dword ptr [rip + 0x1b893f7], xmm2  ; -> 02064B20
004DB729  movss    dword ptr [rip + 0x1b893f3], xmm3  ; -> 02064B24
004DB731  movss    dword ptr [rip + 0x1b893ee], xmm9  ; -> 02064B28
004DB73A  movss    dword ptr [rip + 0x1b894f9], xmm14  ; -> 02064C3C
004DB743  movss    dword ptr [rip + 0x1b894b4], xmm10  ; -> 02064C00
004DB74C  movss    dword ptr [rip + 0x1b894dc], xmm0  ; -> 02064C30
004DB754  movaps   xmm0, xmm1
004DB757  mulss    xmm0, dword ptr [rip + 0x1b894d5]  ; -> 02064C34
004DB75F  mulss    xmm1, dword ptr [rip + 0x1b894d1]  ; -> 02064C38
004DB767  addss    xmm0, xmm3
004DB76B  movss    dword ptr [rip + 0x1b89490], xmm8  ; -> 02064C04
004DB774  movss    dword ptr [rip + 0x1b8948c], xmm7  ; -> 02064C08
004DB77C  addss    xmm1, xmm9
004DB781  movss    dword ptr [rip + 0x1b894ab], xmm0  ; -> 02064C34
004DB789  movss    dword ptr [rip + 0x1b894a7], xmm1  ; -> 02064C38
004DB791  call     0x22cc20  ; -> 0022CC20 fn
004DB796  movups   xmm0, xmmword ptr [rip + 0x1b89423]  ; -> 02064BC0
004DB79D  movss    xmm1, dword ptr [rip + 0x1b8944f]  ; -> 02064BF4
004DB7A5  subss    xmm1, dword ptr [rip + 0x1b893a7]  ; -> 02064B54
004DB7AD  movups   xmmword ptr [rip + 0x1b8948c], xmm0  ; -> 02064C40
004DB7B4  movss    xmm0, dword ptr [rip + 0x1b89434]  ; -> 02064BF0
004DB7BC  subss    xmm0, dword ptr [rip + 0x1b8938c]  ; -> 02064B50
004DB7C4  movss    dword ptr [rip + 0x1b89448], xmm1  ; -> 02064C14
004DB7CC  movss    dword ptr [rip + 0x1b8943c], xmm0  ; -> 02064C10
004DB7D4  movss    xmm0, dword ptr [rip + 0x1b8941c]  ; -> 02064BF8
004DB7DC  subss    xmm0, dword ptr [rip + 0x1b89374]  ; -> 02064B58
004DB7E4  movss    dword ptr [rip + 0x1b8942c], xmm0  ; -> 02064C18
004DB7EC  call     0x22cc20  ; -> 0022CC20 fn
004DB7F1  movss    xmm14, dword ptr [rip + 0x1927042]  ; -> 01E0283C [f32 1]
004DB7FA  movss    xmm1, dword ptr [rip + 0x1b893c2]  ; -> 02064BC4
004DB802  movss    xmm4, dword ptr [rip + 0x1b893fa]  ; -> 02064C04
004DB80A  movss    xmm0, dword ptr [rip + 0x1b893ae]  ; -> 02064BC0
004DB812  movss    xmm7, dword ptr [rip + 0x1b893ee]  ; -> 02064C08
004DB81A  movss    xmm5, dword ptr [rip + 0x1b893ae]  ; -> 02064BD0
004DB822  movss    xmm3, dword ptr [rip + 0x1b893aa]  ; -> 02064BD4
004DB82A  movss    xmm2, dword ptr [rip + 0x1b893a6]  ; -> 02064BD8
004DB832  movss    xmm6, dword ptr [rip + 0x1b893c6]  ; -> 02064C00
004DB83A  movss    xmm11, dword ptr [rip + 0x1b893d5]  ; -> 02064C18
004DB843  movss    dword ptr [rip + 0x1b89415], xmm0  ; -> 02064C60
004DB84B  movss    xmm0, dword ptr [rip + 0x1b89375]  ; -> 02064BC8
004DB853  movss    dword ptr [rip + 0x1b8940d], xmm0  ; -> 02064C68
004DB85B  movss    xmm0, dword ptr [rip + 0x1b893b1]  ; -> 02064C14
004DB863  mulss    xmm0, xmm0
004DB867  movss    dword ptr [rip + 0x1b893f5], xmm1  ; -> 02064C64
004DB86F  movss    xmm1, dword ptr [rip + 0x1b89399]  ; -> 02064C10
004DB877  movss    dword ptr [rip + 0x1b89415], xmm0  ; -> 02064C94
004DB87F  mulss    xmm0, xmm14
004DB884  mulss    xmm7, xmm7
004DB888  mulss    xmm4, xmm4
004DB88C  mulss    xmm1, xmm1
004DB890  mulss    xmm11, xmm11
004DB895  mulss    xmm6, xmm6
004DB899  movss    dword ptr [rip + 0x1b893e3], xmm4  ; -> 02064C84
004DB8A1  mulss    xmm4, xmm14
004DB8A6  movss    dword ptr [rip + 0x1b893da], xmm7  ; -> 02064C88
004DB8AE  mulss    xmm7, xmm14
004DB8B3  mulss    xmm1, xmm14
004DB8B8  movss    dword ptr [rip + 0x1b893d7], xmm11  ; -> 02064C98
004DB8C1  mulss    xmm6, xmm14
004DB8C6  addss    xmm1, xmm0
004DB8CA  mulss    xmm11, xmm14
004DB8CF  addss    xmm6, xmm4
004DB8D3  movss    dword ptr [rip + 0x1b89375], xmm5  ; -> 02064C50
004DB8DB  movss    dword ptr [rip + 0x1b89371], xmm3  ; -> 02064C54
004DB8E3  movss    dword ptr [rip + 0x1b8936d], xmm2  ; -> 02064C58
004DB8EB  addss    xmm11, xmm1
004DB8F0  movss    dword ptr [rip + 0x1b89378], xmm5  ; -> 02064C70
004DB8F8  movss    dword ptr [rip + 0x1b89374], xmm3  ; -> 02064C74
004DB900  addss    xmm7, xmm6
004DB904  movss    dword ptr [rip + 0x1b8936c], xmm2  ; -> 02064C78
004DB90C  movss    dword ptr [rip + 0x1b89387], xmm11  ; -> 02064C9C
004DB915  cvtps2pd xmm0, xmm7
004DB918  movss    dword ptr [rip + 0x1b8936c], xmm7  ; -> 02064C8C
004DB920  andps    xmm0, xmm15
004DB924  cvtpd2ps xmm0, xmm0
004DB928  call     0x861f14  ; -> 00861F14 fn
004DB92D  movss    xmm13, dword ptr [rip + 0x1926efa]  ; -> 01E02830 [u32 0x00000000]
004DB936  movaps   xmm10, xmm0
004DB93A  addss    xmm10, xmm13
004DB93F  cvtps2pd xmm0, xmm11
004DB943  subss    xmm10, dword ptr [rip + 0x1b89214]  ; -> 02064B60
004DB94C  andps    xmm0, xmm15
004DB950  cvtpd2ps xmm0, xmm0
004DB954  mulss    xmm10, dword ptr [rip + 0x1b8920b]  ; -> 02064B68
004DB95D  minss    xmm10, xmm14
004DB962  maxss    xmm10, xmm13
004DB967  mulss    xmm10, dword ptr [rip + 0x1b891fc]  ; -> 02064B6C
004DB970  addss    xmm10, dword ptr [rip + 0x1b891eb]  ; -> 02064B64
004DB979  movss    dword ptr [rip + 0x1b892fe], xmm10  ; -> 02064C80
004DB982  call     0x861f14  ; -> 00861F14 fn
004DB987  movaps   xmm3, xmm0
004DB98A  addss    xmm3, xmm13
004DB98F  subss    xmm3, dword ptr [rip + 0x1b891c9]  ; -> 02064B60
004DB997  mulss    xmm3, dword ptr [rip + 0x1b891c9]  ; -> 02064B68
004DB99F  minss    xmm3, xmm14
004DB9A4  maxss    xmm3, xmm13
004DB9A9  mulss    xmm3, dword ptr [rip + 0x1b891bb]  ; -> 02064B6C
004DB9B1  movss    xmm0, dword ptr [rip + 0x1b89293]  ; -> 02064C4C
004DB9B9  movss    xmm2, dword ptr [rip + 0x1b8921b]  ; -> 02064BDC
004DB9C1  addss    xmm3, dword ptr [rip + 0x1b8919b]  ; -> 02064B64
004DB9C9  movss    xmm6, dword ptr [rip + 0x1b8920f]  ; -> 02064BE0
004DB9D1  movss    xmm1, dword ptr [rip + 0x1b891f3]  ; -> 02064BCC
004DB9D9  movss    xmm15, dword ptr [rip + 0x1b8930e]  ; -> 02064CF0
004DB9E2  movss    xmm9, dword ptr [rip + 0x1b89325]  ; -> 02064D10
004DB9EB  movss    xmm11, dword ptr [rip + 0x1b89324]  ; -> 02064D18
004DB9F4  movss    xmm8, dword ptr [rip + 0x1b8931f]  ; -> 02064D1C
004DB9FD  mulss    xmm0, xmm10
004DBA02  mulss    xmm1, xmm3
004DBA06  movss    dword ptr [rip + 0x1b8923e], xmm0  ; -> 02064C4C
004DBA0E  movaps   xmm0, xmm2
004DBA11  mulss    xmm0, xmm10
004DBA16  movss    xmm10, dword ptr [rip + 0x1b892f5]  ; -> 02064D14
004DBA1F  movss    dword ptr [rip + 0x1b89245], xmm1  ; -> 02064C6C
004DBA27  movss    dword ptr [rip + 0x1b8922d], xmm0  ; -> 02064C5C
004DBA2F  movups   xmm0, xmmword ptr [rip + 0x1b892aa]  ; -> 02064CE0
004DBA36  mulss    xmm2, xmm3
004DBA3A  shufps   xmm6, xmm6, 0
004DBA3E  mulps    xmm6, xmm0
004DBA41  movaps   xmm0, xmm15
004DBA45  movss    dword ptr [rip + 0x1b8922f], xmm2  ; -> 02064C7C
004DBA4D  movss    xmm2, dword ptr [rip + 0x1b8918f]  ; -> 02064BE4
004DBA55  mulss    xmm0, xmm2
004DBA59  movups   xmmword ptr [rip + 0x1b890c0], xmm6  ; -> 02064B20
004DBA60  movss    xmm5, dword ptr [rip + 0x1b890c4]  ; -> 02064B2C
004DBA68  addss    xmm6, xmm0
004DBA6C  movss    xmm0, dword ptr [rip + 0x1b89280]  ; -> 02064CF4
004DBA74  movss    xmm4, dword ptr [rip + 0x1b890ac]  ; -> 02064B28
004DBA7C  movss    dword ptr [rsp + 0x110], xmm0
004DBA85  mulss    xmm0, xmm2
004DBA89  movss    dword ptr [rip + 0x1b891ff], xmm3  ; -> 02064C90
004DBA91  movss    xmm3, dword ptr [rip + 0x1b8908b]  ; -> 02064B24
004DBA99  addss    xmm3, xmm0
004DBA9D  movss    xmm0, dword ptr [rip + 0x1b89253]  ; -> 02064CF8
004DBAA5  movaps   xmm1, xmm0
004DBAA8  movss    dword ptr [rsp + 0x120], xmm0
004DBAB1  movss    xmm0, dword ptr [rip + 0x1b89243]  ; -> 02064CFC
004DBAB9  movss    dword ptr [rsp + 0x128], xmm0
004DBAC2  mulss    xmm0, xmm2
004DBAC6  mulss    xmm1, xmm2
004DBACA  movss    xmm2, dword ptr [rip + 0x1b89116]  ; -> 02064BE8
004DBAD2  addss    xmm5, xmm0
004DBAD6  movss    xmm0, dword ptr [rip + 0x1b89222]  ; -> 02064D00
004DBADE  movss    dword ptr [rsp + 0x20], xmm0
004DBAE4  addss    xmm4, xmm1
004DBAE8  movaps   xmm1, xmm0
004DBAEB  movss    xmm0, dword ptr [rip + 0x1b89211]  ; -> 02064D04
004DBAF3  movss    dword ptr [rsp + 0x24], xmm0
004DBAF9  mulss    xmm0, xmm2
004DBAFD  mulss    xmm1, xmm2
004DBB01  addss    xmm3, xmm0
004DBB05  movss    xmm0, dword ptr [rip + 0x1b891fb]  ; -> 02064D08
004DBB0D  movss    dword ptr [rsp + 0x28], xmm0
004DBB13  addss    xmm6, xmm1
004DBB17  movaps   xmm1, xmm0
004DBB1A  movss    xmm0, dword ptr [rip + 0x1b891ea]  ; -> 02064D0C
004DBB22  movss    dword ptr [rsp + 0x2c], xmm0
004DBB28  mulss    xmm1, xmm2
004DBB2C  mulss    xmm2, xmm0
004DBB30  movaps   xmm0, xmm9
004DBB34  addss    xmm4, xmm1
004DBB38  movaps   xmm1, xmm11
004DBB3C  addss    xmm5, xmm2
004DBB40  movss    xmm2, dword ptr [rip + 0x1b890a4]  ; -> 02064BEC
004DBB48  mulss    xmm0, xmm2
004DBB4C  mulss    xmm1, xmm2
004DBB50  addss    xmm0, xmm6
004DBB54  addss    xmm1, xmm4
004DBB58  movss    dword ptr [rip + 0x1b89080], xmm0  ; -> 02064BE0
004DBB60  movaps   xmm0, xmm10
004DBB64  mulss    xmm0, xmm2
004DBB68  movss    dword ptr [rip + 0x1b89078], xmm1  ; -> 02064BE8
004DBB70  addss    xmm0, xmm3
004DBB74  movss    dword ptr [rip + 0x1b89068], xmm0  ; -> 02064BE4
004DBB7C  movaps   xmm0, xmm8
004DBB80  mulss    xmm0, xmm2
004DBB84  addss    xmm0, xmm5
004DBB88  movss    dword ptr [rip + 0x1b8905c], xmm0  ; -> 02064BEC
004DBB90  ucomiss  xmm0, dword ptr [rip + 0x425ded]  ; -> 00901984 [u32 0x00000000]
004DBB97  jp       0x4dbb9b  ; -> 004DBB9B
004DBB99  je       0x4dbba4  ; -> 004DBBA4
004DBB9B  movaps   xmm12, xmm14
004DBB9F  divss    xmm12, xmm0
004DBBA4  movss    xmm2, dword ptr [rip + 0x1b89048]  ; -> 02064BF4
004DBBAC  movss    xmm3, dword ptr [rip + 0x1b89048]  ; -> 02064BFC
004DBBB4  movss    xmm7, dword ptr [rip + 0x1b89034]  ; -> 02064BF0
004DBBBC  movups   xmm0, xmmword ptr [rip + 0x1b8911d]  ; -> 02064CE0
004DBBC3  movss    xmm1, dword ptr [rsp + 0x120]
004DBBCC  mulss    xmm1, xmm2
004DBBD0  shufps   xmm7, xmm7, 0
004DBBD4  mulps    xmm7, xmm0
004DBBD7  movaps   xmm0, xmm15
004DBBDB  mulss    xmm0, xmm2
004DBBDF  movups   xmmword ptr [rip + 0x1b88f3a], xmm7  ; -> 02064B20
004DBBE6  movss    xmm4, dword ptr [rip + 0x1b88f36]  ; -> 02064B24
004DBBEE  addss    xmm7, xmm0
004DBBF2  movss    xmm0, dword ptr [rsp + 0x110]
004DBBFB  movss    xmm6, dword ptr [rip + 0x1b88f29]  ; -> 02064B2C
004DBC03  movss    xmm5, dword ptr [rip + 0x1b88f1d]  ; -> 02064B28
004DBC0B  mulss    xmm0, xmm2
004DBC0F  addss    xmm5, xmm1
004DBC13  movss    xmm1, dword ptr [rsp + 0x20]
004DBC19  addss    xmm4, xmm0
004DBC1D  movss    xmm0, dword ptr [rsp + 0x128]
004DBC26  mulss    xmm0, xmm2
004DBC2A  movss    xmm2, dword ptr [rip + 0x1b88fc6]  ; -> 02064BF8
004DBC32  mulss    xmm1, xmm2
004DBC36  addss    xmm6, xmm0
004DBC3A  movss    xmm0, dword ptr [rsp + 0x24]
004DBC40  mulss    xmm0, xmm2
004DBC44  addss    xmm7, xmm1
004DBC48  movss    xmm1, dword ptr [rsp + 0x28]
004DBC4E  mulss    xmm1, xmm2
004DBC52  mulss    xmm2, dword ptr [rsp + 0x2c]
004DBC58  addss    xmm4, xmm0
004DBC5C  addss    xmm5, xmm1
004DBC60  movaps   xmm0, xmm9
004DBC64  mulss    xmm0, xmm3
004DBC68  movaps   xmm1, xmm11
004DBC6C  addss    xmm6, xmm2
004DBC70  mulss    xmm1, xmm3
004DBC74  addss    xmm0, xmm7
004DBC78  movaps   xmm2, xmm8
004DBC7C  movups   xmm7, xmmword ptr [rip + 0x1b88f5d]  ; -> 02064BE0
004DBC83  mulss    xmm2, xmm3
004DBC87  addss    xmm1, xmm5
004DBC8B  movss    dword ptr [rip + 0x1b88f5d], xmm0  ; -> 02064BF0
004DBC93  movaps   xmm0, xmm10
004DBC97  mulss    xmm0, xmm3
004DBC9B  addss    xmm2, xmm6
004DBC9F  movss    dword ptr [rip + 0x1b88f51], xmm1  ; -> 02064BF8
004DBCA7  addss    xmm0, xmm4
004DBCAB  ucomiss  xmm2, dword ptr [rip + 0x425cd2]  ; -> 00901984 [u32 0x00000000]
004DBCB2  movss    dword ptr [rip + 0x1b88f3a], xmm0  ; -> 02064BF4
004DBCBA  movaps   xmm0, xmm12
004DBCBE  shufps   xmm0, xmm0, 0
004DBCC2  mulps    xmm7, xmm0
004DBCC5  movss    dword ptr [rip + 0x1b88f2f], xmm2  ; -> 02064BFC
004DBCCD  jp       0x4dbcdc  ; -> 004DBCDC
004DBCCF  jne      0x4dbcdc  ; -> 004DBCDC
004DBCD1  movss    xmm12, dword ptr [rip + 0x424686]  ; -> 00900360 [u32 0x7F7FFFFF]
004DBCDA  jmp      0x4dbce5  ; -> 004DBCE5
004DBCDC  movaps   xmm12, xmm14
004DBCE0  divss    xmm12, xmm2
004DBCE5  movss    xmm2, dword ptr [rip + 0x1b88f37]  ; -> 02064C24
004DBCED  movss    xmm6, dword ptr [rip + 0x1b88f2b]  ; -> 02064C20
004DBCF5  movups   xmm0, xmmword ptr [rip + 0x1b88fe4]  ; -> 02064CE0
004DBCFC  movss    xmm1, dword ptr [rsp + 0x120]
004DBD05  mulss    xmm1, xmm2
004DBD09  shufps   xmm6, xmm6, 0
004DBD0D  mulps    xmm6, xmm0
004DBD10  movaps   xmm0, xmm15
004DBD14  mulss    xmm0, xmm2
004DBD18  movups   xmmword ptr [rip + 0x1b88e01], xmm6  ; -> 02064B20
004DBD1F  movss    xmm3, dword ptr [rip + 0x1b88dfd]  ; -> 02064B24
004DBD27  addss    xmm6, xmm0
004DBD2B  movss    xmm0, dword ptr [rsp + 0x110]
004DBD34  movss    xmm5, dword ptr [rip + 0x1b88df0]  ; -> 02064B2C
004DBD3C  movss    xmm4, dword ptr [rip + 0x1b88de4]  ; -> 02064B28
004DBD44  mulss    xmm0, xmm2
004DBD48  addss    xmm4, xmm1
004DBD4C  movss    xmm1, dword ptr [rsp + 0x20]
004DBD52  addss    xmm3, xmm0
004DBD56  movss    xmm0, dword ptr [rsp + 0x128]
004DBD5F  mulss    xmm0, xmm2
004DBD63  movss    xmm2, dword ptr [rip + 0x1b88ebd]  ; -> 02064C28
004DBD6B  mulss    xmm1, xmm2
004DBD6F  addss    xmm5, xmm0
004DBD73  movss    xmm0, dword ptr [rsp + 0x24]
004DBD79  mulss    xmm0, xmm2
004DBD7D  addss    xmm6, xmm1
004DBD81  movss    xmm1, dword ptr [rsp + 0x28]
004DBD87  mulss    xmm1, xmm2
004DBD8B  addss    xmm3, xmm0
004DBD8F  movss    xmm0, dword ptr [rsp + 0x2c]
004DBD95  mulss    xmm0, xmm2
004DBD99  movss    xmm2, dword ptr [rip + 0x1b88e8b]  ; -> 02064C2C
004DBDA1  addss    xmm4, xmm1
004DBDA5  movaps   xmm1, xmm9
004DBDA9  addss    xmm5, xmm0
004DBDAD  mulss    xmm1, xmm2
004DBDB1  movaps   xmm0, xmm10
004DBDB5  mulss    xmm0, xmm2
004DBDB9  addss    xmm1, xmm6
004DBDBD  addss    xmm0, xmm3
004DBDC1  movaps   xmm3, xmm8
004DBDC5  mulss    xmm3, xmm2
004DBDC9  movss    dword ptr [rip + 0x1b88e4f], xmm1  ; -> 02064C20
004DBDD1  movaps   xmm1, xmm11
004DBDD5  mulss    xmm1, xmm2
004DBDD9  addss    xmm3, xmm5
004DBDDD  movss    dword ptr [rip + 0x1b88e3f], xmm0  ; -> 02064C24
004DBDE5  movups   xmm5, xmmword ptr [rip + 0x1b88e04]  ; -> 02064BF0
004DBDEC  addss    xmm1, xmm4
004DBDF0  movaps   xmm0, xmm12
004DBDF4  shufps   xmm0, xmm0, 0
004DBDF8  ucomiss  xmm3, dword ptr [rip + 0x425b85]  ; -> 00901984 [u32 0x00000000]
004DBDFF  movss    dword ptr [rip + 0x1b88e21], xmm1  ; -> 02064C28
004DBE07  movss    dword ptr [rip + 0x1b88e1d], xmm3  ; -> 02064C2C
004DBE0F  mulps    xmm5, xmm0
004DBE12  jp       0x4dbe20  ; -> 004DBE20
004DBE14  jne      0x4dbe20  ; -> 004DBE20
004DBE16  movss    xmm6, dword ptr [rip + 0x424542]  ; -> 00900360 [u32 0x7F7FFFFF]
004DBE1E  jmp      0x4dbe28  ; -> 004DBE28
004DBE20  movaps   xmm6, xmm14
004DBE24  divss    xmm6, xmm3
004DBE28  movss    xmm4, dword ptr [rip + 0x1b88e00]  ; -> 02064C30
004DBE30  movups   xmm0, xmmword ptr [rip + 0x1b88ea9]  ; -> 02064CE0
004DBE37  movss    xmm2, dword ptr [rsp + 0x110]
004DBE40  movss    xmm3, dword ptr [rsp + 0x120]
004DBE49  movss    xmm12, dword ptr [rsp + 0x128]
004DBE53  shufps   xmm4, xmm4, 0
004DBE57  mulps    xmm4, xmm0
004DBE5A  movss    xmm0, dword ptr [rip + 0x1b88dd2]  ; -> 02064C34
004DBE62  mulss    xmm12, xmm0
004DBE67  movups   xmmword ptr [rip + 0x1b88cb2], xmm4  ; -> 02064B20
004DBE6E  movss    xmm1, dword ptr [rip + 0x1b88cae]  ; -> 02064B24
004DBE76  mulss    xmm2, xmm0
004DBE7A  mulss    xmm3, xmm0
004DBE7E  addss    xmm1, xmm2
004DBE82  mulss    xmm15, xmm0
004DBE87  movss    xmm0, dword ptr [rip + 0x1b88da9]  ; -> 02064C38
004DBE8F  movss    xmm2, dword ptr [rip + 0x1b88c91]  ; -> 02064B28
004DBE97  addss    xmm2, xmm3
004DBE9B  movss    xmm3, dword ptr [rip + 0x1b88c89]  ; -> 02064B2C
004DBEA3  addss    xmm3, xmm12
004DBEA8  movss    xmm12, dword ptr [rsp + 0x20]
004DBEAF  mulss    xmm12, xmm0
004DBEB4  addss    xmm4, xmm15
004DBEB9  addss    xmm4, xmm12
004DBEBE  movss    xmm12, dword ptr [rsp + 0x24]
004DBEC5  mulss    xmm12, xmm0
004DBECA  addss    xmm1, xmm12
004DBECF  movss    dword ptr [rip + 0x1b88c49], xmm4  ; -> 02064B20
004DBED7  movss    xmm12, dword ptr [rsp + 0x28]
004DBEDE  mulss    xmm12, xmm0
004DBEE3  movss    dword ptr [rip + 0x1b88c39], xmm1  ; -> 02064B24
004DBEEB  addss    xmm2, xmm12
004DBEF0  movss    xmm12, dword ptr [rsp + 0x2c]
004DBEF7  mulss    xmm12, xmm0
004DBEFC  movss    xmm0, dword ptr [rip + 0x1b88d38]  ; -> 02064C3C
004DBF04  mulss    xmm8, xmm0
004DBF09  mulss    xmm9, xmm0
004DBF0E  addss    xmm3, xmm12
004DBF13  mulss    xmm10, xmm0
004DBF18  mulss    xmm11, xmm0
004DBF1D  addss    xmm9, xmm4
004DBF22  movaps   xmm0, xmm6
004DBF25  movss    dword ptr [rip + 0x1b88bfb], xmm2  ; -> 02064B28
004DBF2D  addss    xmm10, xmm1
004DBF32  shufps   xmm0, xmm0, 0
004DBF36  movups   xmm1, xmmword ptr [rip + 0x1b88ce3]  ; -> 02064C20
004DBF3D  addss    xmm8, xmm3
004DBF42  movss    dword ptr [rip + 0x1b88be2], xmm3  ; -> 02064B2C
004DBF4A  addss    xmm11, xmm2
004DBF4F  movss    dword ptr [rip + 0x1b88cd8], xmm9  ; -> 02064C30
004DBF58  movss    dword ptr [rip + 0x1b88cd3], xmm10  ; -> 02064C34
004DBF61  mulps    xmm1, xmm0
004DBF64  ucomiss  xmm8, dword ptr [rip + 0x425a18]  ; -> 00901984 [u32 0x00000000]
004DBF6C  movss    dword ptr [rip + 0x1b88cc3], xmm11  ; -> 02064C38
004DBF75  movss    dword ptr [rip + 0x1b88cbe], xmm8  ; -> 02064C3C
004DBF7E  jp       0x4dbf9a  ; -> 004DBF9A
004DBF80  jne      0x4dbf9a  ; -> 004DBF9A
004DBF82  movss    xmm12, dword ptr [rip + 0x4243d5]  ; -> 00900360 [u32 0x7F7FFFFF]
004DBF8B  movss    dword ptr [rip + 0x1b88b6c], xmm12  ; -> 02064B00
004DBF94  movaps   xmm10, xmm12
004DBF98  jmp      0x4dbfb5  ; -> 004DBFB5
004DBF9A  movss    xmm12, dword ptr [rip + 0x4243bd]  ; -> 00900360 [u32 0x7F7FFFFF]
004DBFA3  movaps   xmm10, xmm14
004DBFA7  divss    xmm10, xmm8
004DBFAC  movss    dword ptr [rip + 0x1b88b4b], xmm10  ; -> 02064B00
004DBFB5  movss    xmm4, dword ptr [rip + 0x1b88b73]  ; -> 02064B30
004DBFBD  ucomiss  xmm4, xmm7
004DBFC0  jp       0x4dbfca  ; -> 004DBFCA
004DBFC2  mov      r9d, 1
004DBFC8  je       0x4dbfcd  ; -> 004DBFCD
004DBFCA  mov      r9d, r13d
004DBFCD  movss    xmm2, dword ptr [rip + 0x1b88b5f]  ; -> 02064B34
004DBFD5  movaps   xmm0, xmm7
004DBFD8  shufps   xmm0, xmm7, 0x55
004DBFDC  ucomiss  xmm2, xmm0
004DBFDF  jp       0x4dbfe9  ; -> 004DBFE9
004DBFE1  mov      r8d, 1
004DBFE7  je       0x4dbfec  ; -> 004DBFEC
004DBFE9  mov      r8d, r13d
004DBFEC  movss    xmm3, dword ptr [rip + 0x1b88b44]  ; -> 02064B38
004DBFF4  movaps   xmm6, xmm7
004DBFF7  shufps   xmm6, xmm7, 0xaa
004DBFFB  ucomiss  xmm3, xmm6
004DBFFE  jp       0x4dc007  ; -> 004DC007
004DC000  mov      ecx, 1
004DC005  je       0x4dc00a  ; -> 004DC00A
004DC007  mov      ecx, r13d
004DC00A  comiss   xmm7, xmm4
004DC00D  mov      eax, r13d
004DC010  mov      edx, r13d
004DC013  seta     dl
004DC016  add      dx, dx
004DC019  comiss   xmm0, xmm2
004DC01C  seta     al
004DC01F  add      dx, ax
004DC022  mov      eax, r13d
004DC025  add      dx, dx
004DC028  comiss   xmm6, xmm3
004DC02B  seta     al
004DC02E  add      dx, ax
004DC031  shl      dx, 2
004DC035  add      dx, r9w
004DC039  add      dx, dx
004DC03C  add      dx, r8w
004DC040  add      dx, dx
004DC043  add      dx, cx
004DC046  add      dx, dx
004DC049  ucomiss  xmm7, xmm13
004DC04D  jp       0x4dc057  ; -> 004DC057
004DC04F  mov      r10d, 1
004DC055  je       0x4dc05a  ; -> 004DC05A
004DC057  mov      r10d, r13d
004DC05A  movss    xmm9, dword ptr [rip + 0x19267d1]  ; -> 01E02834 [u32 0x00000000]
004DC063  ucomiss  xmm0, xmm9
004DC067  jp       0x4dc071  ; -> 004DC071
004DC069  mov      r8d, 1
004DC06F  je       0x4dc074  ; -> 004DC074
004DC071  mov      r8d, r13d
004DC074  movss    xmm8, dword ptr [rip + 0x19267bb]  ; -> 01E02838 [u32 0x00000000]
004DC07D  ucomiss  xmm6, xmm8
004DC081  jp       0x4dc08a  ; -> 004DC08A
004DC083  mov      ecx, 1
004DC088  je       0x4dc08d  ; -> 004DC08D
004DC08A  mov      ecx, r13d
004DC08D  comiss   xmm13, xmm7
004DC091  mov      eax, r13d
004DC094  mov      r9d, r13d
004DC097  seta     r9b
004DC09B  add      r9w, r9w
004DC09F  comiss   xmm9, xmm0
004DC0A3  seta     al
004DC0A6  add      r9w, ax
004DC0AA  mov      eax, r13d
004DC0AD  add      r9w, r9w
004DC0B1  comiss   xmm8, xmm6
004DC0B5  seta     al
004DC0B8  add      r9w, ax
004DC0BC  shl      r9w, 2
004DC0C1  add      r9w, r10w
004DC0C5  add      r9w, r9w
004DC0C9  add      r9w, r8w
004DC0CD  add      r9w, r9w
004DC0D1  add      r9w, cx
004DC0D5  add      r9w, r9w
004DC0D9  ucomiss  xmm4, xmm1
004DC0DC  jp       0x4dc0e6  ; -> 004DC0E6
004DC0DE  mov      r11d, 1
004DC0E4  je       0x4dc0e9  ; -> 004DC0E9
004DC0E6  mov      r11d, r13d
004DC0E9  movaps   xmm6, xmm1
004DC0EC  shufps   xmm6, xmm1, 0x55
004DC0F0  ucomiss  xmm2, xmm6
004DC0F3  jp       0x4dc0fd  ; -> 004DC0FD
004DC0F5  mov      r10d, 1
004DC0FB  je       0x4dc100  ; -> 004DC100
004DC0FD  mov      r10d, r13d
004DC100  movaps   xmm0, xmm1
004DC103  shufps   xmm0, xmm1, 0xaa
004DC107  ucomiss  xmm3, xmm0
004DC10A  jp       0x4dc113  ; -> 004DC113
004DC10C  mov      ecx, 1
004DC111  je       0x4dc116  ; -> 004DC116
004DC113  mov      ecx, r13d
004DC116  comiss   xmm1, xmm4
004DC119  mov      eax, r13d
004DC11C  mov      r8d, r13d
004DC11F  seta     r8b
004DC123  add      r8w, r8w
004DC127  comiss   xmm6, xmm2
004DC12A  seta     al
004DC12D  add      r8w, ax
004DC131  mov      eax, r13d
004DC134  add      r8w, r8w
004DC138  comiss   xmm0, xmm3
004DC13B  seta     al
004DC13E  add      r8w, ax
004DC142  shl      r8w, 2
004DC147  add      r8w, r11w
004DC14B  add      r8w, r8w
004DC14F  add      r8w, r10w
004DC153  add      r8w, r8w
004DC157  add      r8w, cx
004DC15B  add      r8w, r8w
004DC15F  ucomiss  xmm1, xmm13
004DC163  jp       0x4dc16c  ; -> 004DC16C
004DC165  mov      ebx, 1
004DC16A  je       0x4dc16f  ; -> 004DC16F
004DC16C  mov      ebx, r13d
004DC16F  ucomiss  xmm6, xmm9
004DC173  jp       0x4dc17d  ; -> 004DC17D
004DC175  mov      r11d, 1
004DC17B  je       0x4dc180  ; -> 004DC180
004DC17D  mov      r11d, r13d
004DC180  ucomiss  xmm0, xmm8
004DC184  jp       0x4dc18e  ; -> 004DC18E
004DC186  mov      r10d, 1
004DC18C  je       0x4dc191  ; -> 004DC191
004DC18E  mov      r10d, r13d
004DC191  movaps   xmm15, xmmword ptr [rip + 0x439257]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004DC199  mov      eax, r13d
004DC19C  movzx    esi, word ptr [rip + 0x1b88969]  ; -> 02064B0C
004DC1A3  mov      ecx, r13d
004DC1A6  comiss   xmm13, xmm1
004DC1AA  seta     cl
004DC1AD  add      cx, cx
004DC1B0  comiss   xmm9, xmm6
004DC1B4  seta     al
004DC1B7  add      cx, ax
004DC1BA  mov      eax, r13d
004DC1BD  add      cx, cx
004DC1C0  comiss   xmm8, xmm0
004DC1C4  movaps   xmm0, xmm15
004DC1C8  mulps    xmm0, xmm7
004DC1CB  seta     al
004DC1CE  add      cx, ax
004DC1D1  shl      cx, 2
004DC1D5  add      cx, bx
004DC1D8  lea      ebx, [rdi + rsi]
004DC1DB  cvttps2dq xmm7, xmm0
004DC1DF  add      cx, cx
004DC1E2  movzx    edi, bx
004DC1E5  add      cx, r11w
004DC1E9  and      dx, bx
004DC1EC  add      cx, cx
004DC1EF  and      r9w, bx
004DC1F3  add      cx, r10w
004DC1F7  and      r8w, bx
004DC1FB  add      cx, cx
004DC1FE  movaps   xmm0, xmm15
004DC202  mulps    xmm0, xmm1
004DC205  and      di, cx
004DC208  ucomiss  xmm4, xmm5
004DC20B  movups   xmm1, xmmword ptr [rip + 0x1b88a1e]  ; -> 02064C30
004DC212  cvttps2dq xmm11, xmm0
004DC217  movaps   xmm0, xmm10
004DC21B  shufps   xmm0, xmm0, 0
004DC21F  movups   xmmword ptr [rip + 0x1b889ba], xmm7  ; -> 02064BE0
004DC226  movups   xmmword ptr [rip + 0x1b889f2], xmm11  ; -> 02064C20
004DC22E  mulps    xmm1, xmm0
004DC231  jp       0x4dc23a  ; -> 004DC23A
004DC233  mov      ebp, 1
004DC238  je       0x4dc23d  ; -> 004DC23D
004DC23A  mov      ebp, r13d
004DC23D  movaps   xmm6, xmm5
004DC240  shufps   xmm6, xmm5, 0x55
004DC244  ucomiss  xmm2, xmm6
004DC247  jp       0x4dc251  ; -> 004DC251
004DC249  mov      r11d, 1
004DC24F  je       0x4dc254  ; -> 004DC254
004DC251  mov      r11d, r13d
004DC254  movaps   xmm0, xmm5
004DC257  shufps   xmm0, xmm5, 0xaa
004DC25B  ucomiss  xmm3, xmm0
004DC25E  jp       0x4dc267  ; -> 004DC267
004DC260  mov      ecx, 1
004DC265  je       0x4dc26a  ; -> 004DC26A
004DC267  mov      ecx, r13d
004DC26A  comiss   xmm5, xmm4
004DC26D  mov      eax, r13d
004DC270  mov      r10d, r13d
004DC273  seta     r10b
004DC277  add      r10w, r10w
004DC27B  comiss   xmm6, xmm2
004DC27E  seta     al
004DC281  add      r10w, ax
004DC285  mov      eax, r13d
004DC288  add      r10w, r10w
004DC28C  comiss   xmm0, xmm3
004DC28F  seta     al
004DC292  add      r10w, ax
004DC296  movsx    eax, r9w
004DC29A  shl      r10w, 2
004DC29F  or       dx, ax
004DC2A2  add      r10w, bp
004DC2A6  add      r10w, r10w
004DC2AA  add      r10w, r11w
004DC2AE  add      r10w, r10w
004DC2B2  add      r10w, cx
004DC2B6  add      r10w, r10w
004DC2BA  ucomiss  xmm5, xmm13
004DC2BE  mov      word ptr [rip + 0x1b8884a], r10w  ; -> 02064B10
004DC2C6  jp       0x4dc2cf  ; -> 004DC2CF
004DC2C8  mov      ebp, 1
004DC2CD  je       0x4dc2d2  ; -> 004DC2D2
004DC2CF  mov      ebp, r13d
004DC2D2  ucomiss  xmm6, xmm9
004DC2D6  jp       0x4dc2e0  ; -> 004DC2E0
004DC2D8  mov      r9d, 1
004DC2DE  je       0x4dc2e3  ; -> 004DC2E3
004DC2E0  mov      r9d, r13d
004DC2E3  ucomiss  xmm0, xmm8
004DC2E7  jp       0x4dc2f0  ; -> 004DC2F0
004DC2E9  mov      ecx, 1
004DC2EE  je       0x4dc2f3  ; -> 004DC2F3
004DC2F0  mov      ecx, r13d
004DC2F3  comiss   xmm13, xmm5
004DC2F7  mov      eax, r13d
004DC2FA  mov      r11d, r13d
004DC2FD  seta     r11b
004DC301  add      r11w, r11w
004DC305  comiss   xmm9, xmm6
004DC309  seta     al
004DC30C  add      r11w, ax
004DC310  mov      eax, r13d
004DC313  add      r11w, r11w
004DC317  comiss   xmm8, xmm0
004DC31B  seta     al
004DC31E  add      r11w, ax
004DC322  movsx    eax, di
004DC325  shl      r11w, 2
004DC32A  or       r8w, ax
004DC32E  add      r11w, bp
004DC332  add      r11w, r11w
004DC336  add      r11w, r9w
004DC33A  add      r11w, r11w
004DC33E  add      r11w, cx
004DC342  add      r11w, r11w
004DC346  ucomiss  xmm4, xmm1
004DC349  mov      word ptr [rip + 0x1b887c1], r11w  ; -> 02064B12
004DC351  jp       0x4dc35a  ; -> 004DC35A
004DC353  mov      ebp, 1
004DC358  je       0x4dc35d  ; -> 004DC35D
004DC35A  mov      ebp, r13d
004DC35D  movaps   xmm6, xmm1
004DC360  shufps   xmm6, xmm1, 0x55
004DC364  ucomiss  xmm2, xmm6
004DC367  jp       0x4dc370  ; -> 004DC370
004DC369  mov      edi, 1
004DC36E  je       0x4dc373  ; -> 004DC373
004DC370  mov      edi, r13d
004DC373  movaps   xmm0, xmm1
004DC376  shufps   xmm0, xmm1, 0xaa
004DC37A  ucomiss  xmm3, xmm0
004DC37D  jp       0x4dc386  ; -> 004DC386
004DC37F  mov      ecx, 1
004DC384  je       0x4dc389  ; -> 004DC389
004DC386  mov      ecx, r13d
004DC389  comiss   xmm1, xmm4
004DC38C  mov      eax, r13d
004DC38F  mov      r9d, r13d
004DC392  seta     r9b
004DC396  add      r9w, r9w
004DC39A  comiss   xmm6, xmm2
004DC39D  seta     al
004DC3A0  add      r9w, ax
004DC3A4  mov      eax, r13d
004DC3A7  add      r9w, r9w
004DC3AB  comiss   xmm0, xmm3
004DC3AE  seta     al
004DC3B1  add      r9w, ax
004DC3B5  movsx    eax, dx
004DC3B8  shl      r9w, 2
004DC3BD  or       r8w, ax
004DC3C1  add      r9w, bp
004DC3C5  mov      word ptr [rip + 0x1b88a13], r8w  ; -> 02064DE0
004DC3CD  add      r9w, r9w
004DC3D1  add      r9w, di
004DC3D5  add      r9w, r9w
004DC3D9  add      r9w, cx
004DC3DD  add      r9w, r9w
004DC3E1  ucomiss  xmm1, xmm13
004DC3E5  mov      word ptr [rip + 0x1b88727], r9w  ; -> 02064B14
004DC3ED  jp       0x4dc3f6  ; -> 004DC3F6
004DC3EF  mov      ebp, 1
004DC3F4  je       0x4dc3f9  ; -> 004DC3F9
004DC3F6  mov      ebp, r13d
004DC3F9  ucomiss  xmm6, xmm9
004DC3FD  jp       0x4dc406  ; -> 004DC406
004DC3FF  mov      edi, 1
004DC404  je       0x4dc409  ; -> 004DC409
004DC406  mov      edi, r13d
004DC409  ucomiss  xmm0, xmm8
004DC40D  jp       0x4dc416  ; -> 004DC416
004DC40F  mov      edx, 1
004DC414  je       0x4dc419  ; -> 004DC419
004DC416  mov      edx, r13d
004DC419  comiss   xmm13, xmm1
004DC41D  mov      ecx, r13d
004DC420  mov      eax, r13d
004DC423  seta     cl
004DC426  add      cx, cx
004DC429  comiss   xmm9, xmm6
004DC42D  seta     al
004DC430  add      cx, ax
004DC433  mov      eax, r13d
004DC436  add      cx, cx
004DC439  comiss   xmm8, xmm0
004DC43D  movaps   xmm0, xmm15
004DC441  mulps    xmm0, xmm5
004DC444  seta     al
004DC447  and      r10w, bx
004DC44B  add      cx, ax
004DC44E  and      r11w, bx
004DC452  shl      cx, 2
004DC456  and      r9w, bx
004DC45A  add      cx, bp
004DC45D  movsx    eax, r11w
004DC461  or       r10w, ax
004DC465  mov      word ptr [rip + 0x1b8896f], r11w  ; -> 02064DDC
004DC46D  add      cx, cx
004DC470  mov      word ptr [rip + 0x1b88960], r10w  ; -> 02064DD8
004DC478  add      cx, di
004DC47B  cvttps2dq xmm5, xmm0
004DC47F  add      cx, cx
004DC482  add      cx, dx
004DC485  add      cx, cx
004DC488  mov      word ptr [rip + 0x1b88687], cx  ; -> 02064B16
004DC48F  and      bx, cx
004DC492  movsx    eax, bx
004DC495  movaps   xmm0, xmm15
004DC499  or       r9w, ax
004DC49D  mulps    xmm0, xmm1
004DC4A0  movsx    eax, r10w
004DC4A4  movsx    r10d, word ptr [rip + 0x1b88908]  ; -> 02064DB4
004DC4AC  or       r9w, ax
004DC4B0  mov      ecx, r10d
004DC4B3  mov      word ptr [rip + 0x1b8892e], bx  ; -> 02064DE8
004DC4BA  shl      ecx, 4
004DC4BD  cvttps2dq xmm6, xmm0
004DC4C1  movsxd   rax, ecx
004DC4C4  mov      word ptr [rip + 0x1b88918], r9w  ; -> 02064DE4
004DC4CC  movups   xmm0, xmmword ptr [rip + 0x1b8876d]  ; -> 02064C40
004DC4D3  movups   xmmword ptr [rip + 0x1b88716], xmm5  ; -> 02064BF0
004DC4DA  cvttps2dq xmm1, xmm0
004DC4DE  movups   xmm0, xmmword ptr [rip + 0x1b8876b]  ; -> 02064C50
004DC4E5  movups   xmmword ptr [rax + r14], xmm1
004DC4EA  lea      eax, [rcx + 0x10]
004DC4ED  movsxd   r11, eax
004DC4F0  lea      eax, [r10 + 2]
004DC4F4  shl      eax, 4
004DC4F7  movsxd   rbp, eax
004DC4FA  lea      eax, [r10 + 3]
004DC4FE  shl      eax, 4
004DC501  movsxd   rbx, eax
004DC504  lea      eax, [r10 + 4]
004DC508  shl      eax, 4
004DC50B  movsxd   rcx, eax
004DC50E  lea      eax, [r10 + 5]
004DC512  cvttps2dq xmm2, xmm0
004DC516  shl      eax, 4
004DC519  movups   xmm0, xmmword ptr [rip + 0x1b88740]  ; -> 02064C60
004DC520  movups   xmmword ptr [r11 + r14], xmm7
004DC525  cvttps2dq xmm3, xmm0
004DC529  movups   xmm0, xmmword ptr [rip + 0x1b88740]  ; -> 02064C70
004DC530  movups   xmmword ptr [r14 + rbp], xmm2
004DC535  movups   xmmword ptr [rbx + r14], xmm11
004DC53A  movups   xmmword ptr [rcx + r14], xmm3
004DC53F  movsxd   rcx, eax
004DC542  lea      eax, [r10 + 6]
004DC546  cvttps2dq xmm4, xmm0
004DC54A  shl      eax, 4
004DC54D  movups   xmmword ptr [rcx + r14], xmm5
004DC552  movups   xmmword ptr [rip + 0x1b886d7], xmm6  ; -> 02064C30
004DC559  movups   xmmword ptr [rip + 0x1b886e0], xmm1  ; -> 02064C40
004DC560  movups   xmmword ptr [rip + 0x1b886e9], xmm2  ; -> 02064C50
004DC567  movups   xmmword ptr [rip + 0x1b886f2], xmm3  ; -> 02064C60
004DC56E  movups   xmmword ptr [rip + 0x1b886fb], xmm4  ; -> 02064C70
004DC575  movsxd   r14, eax
004DC578  lea      rdi, [rip + 0x1b888b1]  ; -> 02064E30
004DC57F  lea      eax, [r10 + 7]
004DC583  shl      eax, 4
004DC586  movsxd   rdx, eax
004DC589  cmp      r8w, si
004DC58D  movups   xmmword ptr [r14 + rdi], xmm4
004DC592  lea      r8, [rip + 0x1b88897]  ; -> 02064E30
004DC599  movups   xmmword ptr [rdx + rdi], xmm6
004DC59D  movzx    edi, word ptr [rip + 0x1b88830]  ; -> 02064DD4
004DC5A4  je       0x4dc5b8  ; -> 004DC5B8
004DC5A6  mov      dword ptr [r11 + r8 + 0xc], r13d
004DC5AB  mov      dword ptr [r8 + rbp + 0xc], r13d
004DC5B0  mov      dword ptr [rbx + r8 + 0xc], r13d
004DC5B5  movzx    eax, di
004DC5B8  cmp      r9w, si
004DC5BC  je       0x4dc5de  ; -> 004DC5DE
004DC5BE  movzx    eax, di
004DC5C1  mov      dword ptr [rdx + r8 + 0xc], eax
004DC5C6  mov      dword ptr [rcx + r8 + 0xc], r13d
004DC5CB  mov      dword ptr [r14 + r8 + 0xc], r13d
004DC5D0  lea      r14, [rip + 0x1b88859]  ; -> 02064E30
004DC5D7  mov      dword ptr [rdx + r14 + 0xc], r13d
004DC5DC  jmp      0x4dc5e5  ; -> 004DC5E5
004DC5DE  lea      r14, [rip + 0x1b8884b]  ; -> 02064E30
004DC5E5  movzx    eax, word ptr [rip + 0x1b887cc]  ; -> 02064DB8
004DC5EC  add      r10w, 8
004DC5F1  add      ax, 2
004DC5F5  mov      word ptr [rip + 0x1b887b7], r10w  ; -> 02064DB4
004DC5FD  cmp      ax, word ptr [rip + 0x1b887b8]  ; -> 02064DBC
004DC604  mov      word ptr [rip + 0x1b887ad], ax  ; -> 02064DB8
004DC60B  jne      0x4dc62f  ; -> 004DC62F
004DC60D  mov      rdx, r15
004DC610  mov      rcx, r12
004DC613  call     0x4db270  ; -> 004DB270 fn
004DC618  movzx    eax, word ptr [rip + 0x1b88799]  ; -> 02064DB8
004DC61F  movzx    esi, word ptr [rip + 0x1b884e6]  ; -> 02064B0C
004DC626  movss    xmm14, dword ptr [rip + 0x192620d]  ; -> 01E0283C [f32 1]
004DC62F  movzx    r9d, word ptr [rip + 0x1b88789]  ; -> 02064DC0
004DC637  test     r9w, r9w
004DC63B  jle      0x4dc64a  ; -> 004DC64A
004DC63D  movzx    r8d, word ptr [rip + 0x1b8877f]  ; -> 02064DC4
004DC645  jmp      0x4db5c6  ; -> 004DB5C6
004DC64A  cmp      ax, si
004DC64D  je       0x4dc65a  ; -> 004DC65A
004DC64F  mov      rdx, r15
004DC652  mov      rcx, r12
004DC655  call     0x4db270  ; -> 004DB270 fn
004DC65A  movaps   xmm14, xmmword ptr [rsp + 0x40]
004DC660  lea      r11, [rsp + 0xd0]
004DC668  mov      rbx, qword ptr [r11 + 0x48]
004DC66C  movaps   xmm6, xmmword ptr [r11 - 0x10]
004DC671  movaps   xmm7, xmmword ptr [r11 - 0x20]
004DC676  movaps   xmm8, xmmword ptr [r11 - 0x30]
004DC67B  movaps   xmm9, xmmword ptr [r11 - 0x40]
004DC680  movaps   xmm10, xmmword ptr [r11 - 0x50]
004DC685  movaps   xmm11, xmmword ptr [r11 - 0x60]
004DC68A  movaps   xmm12, xmmword ptr [r11 - 0x70]
004DC68F  movaps   xmm13, xmmword ptr [r11 - 0x80]
004DC694  movaps   xmm15, xmmword ptr [rsp + 0x30]
004DC69A  mov      rsp, r11
004DC69D  pop      r15
004DC69F  pop      r14
004DC6A1  pop      r13
004DC6A3  pop      r12
004DC6A5  pop      rdi
004DC6A6  pop      rsi
004DC6A7  pop      rbp
004DC6A8  ret      
```

## 004DF440 (6957 B, extent 004DF440-004E0F6D)

Page context: "- a sibling module record's init.  Interior anchor '004F4FA3' (function '004F4F80').  '004E2930' (863 B) is the battery constructor with the extra call: '00861EC0' zeroes 0x200, '008631E0' registers '004DF440', '008631D0(0x1E)' fills '+0x10', '004DC8B0' runs mid-fill, then constants ('+0x1C' = 0x6C1B0000, '+0x3C' = 0x4B189680) - another module record's init.  Interior anchor '004E2953' (function '004E2930').  '004E2DE0' (814 B) is the b"

```
004DF440  mov      rax, rsp
004DF443  mov      qword ptr [rax + 8], rbx
004DF447  push     rbp
004DF448  push     rsi
004DF449  push     rdi
004DF44A  push     r12
004DF44C  push     r13
004DF44E  push     r14
004DF450  push     r15
004DF452  sub      rsp, 0xc0
004DF459  movsx    r11d, word ptr [rip + 0x1b856ab]  ; -> 02064B0C
004DF461  lea      r13, [rip + 0x1b859c8]  ; -> 02064E30
004DF468  movaps   xmmword ptr [rax - 0x48], xmm6
004DF46C  mov      edx, r11d
004DF46F  movaps   xmmword ptr [rax - 0x58], xmm7
004DF473  movaps   xmmword ptr [rax - 0x68], xmm8
004DF478  movaps   xmmword ptr [rax - 0x78], xmm9
004DF47D  lea      r10d, [r11 + r11]
004DF481  movaps   xmmword ptr [rsp + 0x70], xmm10
004DF487  lea      eax, [r11 + 4]
004DF48B  shl      eax, 4
004DF48E  cdqe     
004DF490  mov      qword ptr [rsp + 0x118], rax
004DF498  movaps   xmmword ptr [rsp + 0x60], xmm11
004DF49E  movaps   xmmword ptr [rsp + 0x50], xmm12
004DF4A4  movzx    r9d, word ptr [rax + r13]
004DF4A9  lea      eax, [r11 + 5]
004DF4AD  movss    xmm12, dword ptr [rip + 0x192337a]  ; -> 01E02830 [u32 0x00000000]
004DF4B6  add      r9w, 2
004DF4BB  shl      eax, 4
004DF4BE  movaps   xmm3, xmm12
004DF4C2  movsxd   rcx, eax
004DF4C5  movaps   xmmword ptr [rsp + 0x40], xmm13
004DF4CB  movaps   xmmword ptr [rsp + 0x30], xmm14
004DF4D1  movaps   xmmword ptr [rsp + 0x20], xmm15
004DF4D7  lea      eax, [r11 + 6]
004DF4DB  shl      edx, 4
004DF4DE  movups   xmm2, xmmword ptr [rcx + r13]
004DF4E3  shl      eax, 4
004DF4E6  movss    xmm13, dword ptr [rip + 0x192334d]  ; -> 01E0283C [f32 1]
004DF4EF  movsxd   rcx, eax
004DF4F2  addss    xmm3, xmm13
004DF4F7  lea      eax, [r11 + 7]
004DF4FB  movaps   xmm1, xmm2
004DF4FE  shl      eax, 4
004DF501  shufps   xmm1, xmm2, 0x55
004DF505  movups   xmm0, xmmword ptr [rcx + r13]
004DF50A  movsxd   rcx, eax
004DF50D  lea      eax, [r11 + 8]
004DF511  shl      eax, 4
004DF514  subss    xmm1, xmm2
004DF518  movups   xmmword ptr [rip + 0x1b856a1], xmm0  ; -> 02064BC0
004DF51F  movups   xmm0, xmmword ptr [rcx + r13]
004DF524  movsxd   rcx, eax
004DF527  lea      eax, [r11 + 9]
004DF52B  shl      eax, 4
004DF52E  movups   xmmword ptr [rip + 0x1b8569b], xmm0  ; -> 02064BD0
004DF535  movups   xmm0, xmmword ptr [rcx + r13]
004DF53A  movsxd   rcx, eax
004DF53D  lea      eax, [r11 + 3]
004DF541  shl      eax, 4
004DF544  movups   xmmword ptr [rip + 0x1b856c5], xmm2  ; -> 02064C10
004DF54B  movups   xmmword ptr [rip + 0x1b8568e], xmm0  ; -> 02064BE0
004DF552  movups   xmm0, xmmword ptr [rcx + r13]
004DF557  movsxd   rcx, eax
004DF55A  lea      eax, [rdx + 0x10]
004DF55D  movss    dword ptr [rip + 0x1b856af], xmm1  ; -> 02064C14
004DF565  movups   xmmword ptr [rip + 0x1b85684], xmm0  ; -> 02064BF0
004DF56C  movups   xmm11, xmmword ptr [rcx + r13]
004DF571  movsxd   rcx, eax
004DF574  movsxd   rax, edx
004DF577  movaps   xmm2, xmm11
004DF57B  subss    xmm3, xmm11
004DF580  mulss    xmm2, dword ptr [rip + 0x413b94]  ; -> 008F311C [f32 3]
004DF588  movaps   xmm10, xmm11
004DF58C  movzx    eax, word ptr [rax + r13]
004DF591  movaps   xmm5, xmm11
004DF595  movups   xmm0, xmmword ptr [rcx + r13]
004DF59A  mov      word ptr [rip + 0x1b8581f], ax  ; -> 02064DC0
004DF5A1  lea      eax, [r11 + 0x13]
004DF5A5  addss    xmm10, dword ptr [rip + 0x192328a]  ; -> 01E02838 [u32 0x00000000]
004DF5AE  shl      eax, 4
004DF5B1  movaps   xmm1, xmm11
004DF5B5  movsxd   rbx, eax
004DF5B8  movaps   xmm7, xmm2
004DF5BB  addss    xmm7, dword ptr [rip + 0x1923271]  ; -> 01E02834 [u32 0x00000000]
004DF5C3  movups   xmmword ptr [rip + 0x1b85635], xmm11  ; -> 02064C00
004DF5CB  movups   xmm8, xmmword ptr [rbx + r13]
004DF5D0  movups   xmmword ptr [rip + 0x1b85559], xmm0  ; -> 02064B30
004DF5D7  mulss    xmm5, xmm13
004DF5DC  mulss    xmm1, xmm11
004DF5E1  lea      eax, [r11 + 0x14]
004DF5E5  mulss    xmm10, xmm2
004DF5EA  shl      eax, 4
004DF5ED  lea      r8, [rip + 0x1b8583c]  ; -> 02064E30
004DF5F4  movsxd   rdi, eax
004DF5F7  addss    xmm12, xmm13
004DF5FC  lea      eax, [r11 + 0x15]
004DF600  movss    dword ptr [rip + 0x1b85653], xmm13  ; -> 02064C5C
004DF609  shl      eax, 4
004DF60C  movaps   xmm6, xmm3
004DF60F  movsxd   rsi, eax
004DF612  xorps    xmm9, xmm9
004DF616  movups   xmm0, xmmword ptr [rdi + r13]
004DF61B  lea      eax, [r11 + 0x16]
004DF61F  mov      dword ptr [rip + 0x1b854db], 0x40400000  ; -> 02064B04
004DF629  mulss    xmm6, xmm3
004DF62D  shl      eax, 4
004DF630  movsxd   rbp, eax
004DF633  lea      eax, [r11 + 0x17]
004DF637  shl      eax, 4
004DF63A  movsxd   r14, eax
004DF63D  lea      eax, [r11 + 0x18]
004DF641  movups   xmmword ptr [rip + 0x1b85668], xmm0  ; -> 02064CB0
004DF648  shl      eax, 4
004DF64B  movups   xmm0, xmmword ptr [rsi + r13]
004DF650  movsxd   r15, eax
004DF653  lea      eax, [r11 + 0x19]
004DF657  movups   xmm15, xmmword ptr [r14 + r13]
004DF65C  shl      eax, 4
004DF65F  movups   xmmword ptr [rip + 0x1b8565a], xmm0  ; -> 02064CC0
004DF666  movsxd   r12, eax
004DF669  lea      eax, [r11 + 0x1a]
004DF66D  movups   xmm0, xmmword ptr [r13 + rbp]
004DF673  shl      eax, 4
004DF676  mulss    xmm7, xmm6
004DF67A  movups   xmmword ptr [rip + 0x1b8564f], xmm0  ; -> 02064CD0
004DF681  movups   xmm0, xmmword ptr [r15 + r13]
004DF686  movss    dword ptr [rsp + 0x110], xmm12
004DF690  movups   xmmword ptr [rip + 0x1b85659], xmm0  ; -> 02064CF0
004DF697  movups   xmm0, xmmword ptr [r12 + r13]
004DF69C  movsxd   r13, eax
004DF69F  mulss    xmm5, xmm1
004DF6A3  movups   xmmword ptr [rip + 0x1b85656], xmm0  ; -> 02064D00
004DF6AA  movups   xmm0, xmmword ptr [r8 + r13]
004DF6AF  mulss    xmm10, xmm3
004DF6B4  movups   xmmword ptr [rip + 0x1b85655], xmm0  ; -> 02064D10
004DF6BB  mulss    xmm6, xmm3
004DF6BF  nop      
004DF6C0  movss    xmm2, dword ptr [rip + 0x1b85508]  ; -> 02064BD0
004DF6C8  movaps   xmm3, xmm5
004DF6CB  mulss    xmm3, dword ptr [rip + 0x1b85501]  ; -> 02064BD4
004DF6D3  movaps   xmm1, xmm10
004DF6D7  mulss    xmm1, dword ptr [rip + 0x1b85515]  ; -> 02064BF4
004DF6DF  movss    xmm0, dword ptr [rip + 0x1b85509]  ; -> 02064BF0
004DF6E7  movss    xmm4, dword ptr [rip + 0x1b854e9]  ; -> 02064BD8
004DF6EF  addss    xmm11, dword ptr [rip + 0x1b8550c]  ; -> 02064C04
004DF6F8  mulss    xmm0, xmm10
004DF6FD  addss    xmm3, xmm1
004DF701  movss    xmm1, dword ptr [rip + 0x1b854d7]  ; -> 02064BE0
004DF709  mulss    xmm1, xmm7
004DF70D  mulss    xmm2, xmm5
004DF711  mulss    xmm4, xmm5
004DF715  movss    xmm5, dword ptr [rip + 0x1b854a7]  ; -> 02064BC4
004DF71D  addss    xmm2, xmm0
004DF721  movss    xmm0, dword ptr [rip + 0x1b854cf]  ; -> 02064BF8
004DF729  mulss    xmm0, xmm10
004DF72E  mulss    xmm5, xmm6
004DF732  addss    xmm2, xmm1
004DF736  movss    dword ptr [rip + 0x1b854c1], xmm11  ; -> 02064C00
004DF73F  movss    xmm1, dword ptr [rip + 0x1b854a1]  ; -> 02064BE8
004DF747  addss    xmm4, xmm0
004DF74B  mulss    xmm1, xmm7
004DF74F  movaps   xmm0, xmm7
004DF752  mulss    xmm0, dword ptr [rip + 0x1b8548a]  ; -> 02064BE4
004DF75A  movss    xmm7, dword ptr [rip + 0x1b85466]  ; -> 02064BC8
004DF762  addss    xmm4, xmm1
004DF766  movss    xmm1, dword ptr [rip + 0x1b8554a]  ; -> 02064CB8
004DF76E  addss    xmm3, xmm0
004DF772  mulss    xmm7, xmm6
004DF776  movss    xmm0, dword ptr [rip + 0x1b85442]  ; -> 02064BC0
004DF77E  mulss    xmm0, xmm6
004DF782  addss    xmm7, xmm4
004DF786  addss    xmm5, xmm3
004DF78A  addss    xmm0, xmm2
004DF78E  movss    dword ptr [rip + 0x1b854c2], xmm7  ; -> 02064C58
004DF796  mulss    xmm1, xmm5
004DF79A  movaps   xmm6, xmm0
004DF79D  movss    dword ptr [rip + 0x1b854af], xmm5  ; -> 02064C54
004DF7A5  movss    xmm0, dword ptr [rip + 0x1b85503]  ; -> 02064CB0
004DF7AD  mulss    xmm0, xmm5
004DF7B1  shufps   xmm6, xmm6, 0
004DF7B5  mulps    xmm6, xmm8
004DF7B9  movss    xmm8, dword ptr [rip + 0x1b8551a]  ; -> 02064CDC
004DF7C2  mulss    xmm8, xmm13
004DF7C7  movups   xmmword ptr [rip + 0x1b85352], xmm6  ; -> 02064B20
004DF7CE  movss    xmm2, dword ptr [rip + 0x1b8534e]  ; -> 02064B24
004DF7D6  addss    xmm6, xmm0
004DF7DA  movss    xmm0, dword ptr [rip + 0x1b854d2]  ; -> 02064CB4
004DF7E2  movss    xmm4, dword ptr [rip + 0x1b85342]  ; -> 02064B2C
004DF7EA  movss    xmm3, dword ptr [rip + 0x1b85336]  ; -> 02064B28
004DF7F2  mulss    xmm0, xmm5
004DF7F6  addss    xmm3, xmm1
004DF7FA  movaps   xmm1, xmm7
004DF7FD  mulss    xmm1, dword ptr [rip + 0x1b854bf]  ; -> 02064CC4
004DF805  addss    xmm2, xmm0
004DF809  movss    xmm0, dword ptr [rip + 0x1b854ab]  ; -> 02064CBC
004DF811  mulss    xmm0, xmm5
004DF815  addss    xmm4, xmm0
004DF819  movaps   xmm0, xmm7
004DF81C  mulss    xmm0, dword ptr [rip + 0x1b8549c]  ; -> 02064CC0
004DF824  addss    xmm2, xmm1
004DF828  addss    xmm6, xmm0
004DF82C  movaps   xmm0, xmm7
004DF82F  mulss    xmm0, dword ptr [rip + 0x1b85491]  ; -> 02064CC8
004DF837  mulss    xmm7, dword ptr [rip + 0x1b8548d]  ; -> 02064CCC
004DF83F  addss    xmm3, xmm0
004DF843  movss    xmm0, dword ptr [rip + 0x1b85485]  ; -> 02064CD0
004DF84B  mulss    xmm0, xmm13
004DF850  addss    xmm4, xmm7
004DF854  movss    xmm7, dword ptr [rip + 0x1b8547c]  ; -> 02064CD8
004DF85C  mulss    xmm7, xmm13
004DF861  addss    xmm0, xmm6
004DF865  movss    xmm6, dword ptr [rip + 0x1b85467]  ; -> 02064CD4
004DF86D  mulss    xmm6, xmm13
004DF872  addss    xmm7, xmm3
004DF876  addss    xmm6, xmm2
004DF87A  movss    dword ptr [rip + 0x1b853fe], xmm0  ; -> 02064C80
004DF882  movss    dword ptr [rip + 0x1b853fe], xmm7  ; -> 02064C88
004DF88A  movss    dword ptr [rip + 0x1b853f2], xmm6  ; -> 02064C84
004DF892  movaps   xmm5, xmm0
004DF895  addss    xmm8, xmm4
004DF89A  shufps   xmm5, xmm5, 0
004DF89E  movaps   xmm0, xmm6
004DF8A1  mulss    xmm0, dword ptr [rip + 0x1b85447]  ; -> 02064CF0
004DF8A9  movaps   xmm1, xmm6
004DF8AC  mulss    xmm1, dword ptr [rip + 0x1b85444]  ; -> 02064CF8
004DF8B4  movaps   xmm14, xmm11
004DF8B8  mulss    xmm14, dword ptr [rip + 0x41385b]  ; -> 008F311C [f32 3]
004DF8C1  movaps   xmm10, xmm11
004DF8C5  addss    xmm10, dword ptr [rip + 0x1922f6a]  ; -> 01E02838 [u32 0x00000000]
004DF8CE  mulps    xmm5, xmm15
004DF8D2  movss    dword ptr [rip + 0x1b853b1], xmm8  ; -> 02064C8C
004DF8DB  movss    dword ptr [rip + 0x1b8535c], xmm14  ; -> 02064C40
004DF8E4  movups   xmmword ptr [rip + 0x1b85235], xmm5  ; -> 02064B20
004DF8EB  movss    xmm2, dword ptr [rip + 0x1b85231]  ; -> 02064B24
004DF8F3  addss    xmm5, xmm0
004DF8F7  movss    xmm3, dword ptr [rip + 0x1b85229]  ; -> 02064B28
004DF8FF  movaps   xmm0, xmm6
004DF902  mulss    xmm0, dword ptr [rip + 0x1b853ea]  ; -> 02064CF4
004DF90A  addss    xmm3, xmm1
004DF90E  movss    xmm4, dword ptr [rip + 0x1b85216]  ; -> 02064B2C
004DF916  movaps   xmm1, xmm7
004DF919  mulss    xmm1, dword ptr [rip + 0x1b853e3]  ; -> 02064D04
004DF921  mulss    xmm6, dword ptr [rip + 0x1b853d3]  ; -> 02064CFC
004DF929  addss    xmm2, xmm0
004DF92D  movaps   xmm0, xmm7
004DF930  mulss    xmm0, dword ptr [rip + 0x1b853c8]  ; -> 02064D00
004DF938  addss    xmm2, xmm1
004DF93C  movaps   xmm1, xmm8
004DF940  mulss    xmm1, dword ptr [rip + 0x1b853cc]  ; -> 02064D14
004DF948  addss    xmm4, xmm6
004DF94C  addss    xmm5, xmm0
004DF950  movaps   xmm0, xmm7
004DF953  mulss    xmm0, dword ptr [rip + 0x1b853ad]  ; -> 02064D08
004DF95B  mulss    xmm7, dword ptr [rip + 0x1b853a9]  ; -> 02064D0C
004DF963  addss    xmm1, xmm2
004DF967  addss    xmm3, xmm0
004DF96B  movss    dword ptr [rip + 0x1b851ad], xmm5  ; -> 02064B20
004DF973  movaps   xmm0, xmm8
004DF977  movss    dword ptr [rip + 0x1b851a5], xmm2  ; -> 02064B24
004DF97F  mulss    xmm0, dword ptr [rip + 0x1b85389]  ; -> 02064D10
004DF987  addss    xmm4, xmm7
004DF98B  movss    dword ptr [rip + 0x1b852d1], xmm1  ; -> 02064C64
004DF993  movss    dword ptr [rip + 0x1b8518d], xmm3  ; -> 02064B28
004DF99B  addss    xmm0, xmm5
004DF99F  movss    dword ptr [rip + 0x1b85185], xmm4  ; -> 02064B2C
004DF9A7  movss    dword ptr [rip + 0x1b852b1], xmm0  ; -> 02064C60
004DF9AF  movaps   xmm0, xmm8
004DF9B3  mulss    xmm8, dword ptr [rip + 0x1b85360]  ; -> 02064D1C
004DF9BC  mulss    xmm0, dword ptr [rip + 0x1b85354]  ; -> 02064D18
004DF9C4  addss    xmm8, xmm4
004DF9C9  addss    xmm0, xmm3
004DF9CD  ucomiss  xmm8, xmm9
004DF9D1  movss    dword ptr [rip + 0x1b8528f], xmm0  ; -> 02064C68
004DF9D9  movss    dword ptr [rip + 0x1b8528a], xmm8  ; -> 02064C6C
004DF9E2  jp       0x4df9f0  ; -> 004DF9F0
004DF9E4  jne      0x4df9f0  ; -> 004DF9F0
004DF9E6  movss    xmm2, dword ptr [rip + 0x420972]  ; -> 00900360 [u32 0x7F7FFFFF]
004DF9EE  jmp      0x4df9f9  ; -> 004DF9F9
004DF9F0  movaps   xmm2, xmm13
004DF9F4  divss    xmm2, xmm8
004DF9F9  movups   xmm0, xmmword ptr [rdi + r8]
004DF9FE  movsx    edx, r10w
004DFA02  dec      r9w
004DFA06  movups   xmm8, xmmword ptr [rbx + r8]
004DFA0B  inc      r10w
004DFA0F  movups   xmm15, xmmword ptr [r14 + r8]
004DFA14  lea      eax, [rdx + 0x2bc]
004DFA1A  movups   xmmword ptr [rip + 0x1b8528f], xmm0  ; -> 02064CB0
004DFA21  shl      eax, 4
004DFA24  movups   xmm0, xmmword ptr [rsi + r8]
004DFA29  movsxd   rcx, eax
004DFA2C  lea      eax, [rdx + 0x80]
004DFA32  subss    xmm12, xmm11
004DFA37  movss    dword ptr [rip + 0x1b850c1], xmm2  ; -> 02064B00
004DFA3F  movups   xmmword ptr [rip + 0x1b8527a], xmm0  ; -> 02064CC0
004DFA46  shl      eax, 4
004DFA49  mulss    xmm10, xmm14
004DFA4E  movaps   xmm1, xmm11
004DFA52  mulss    xmm1, xmm11
004DFA57  movaps   xmm6, xmm12
004DFA5B  mulss    xmm6, xmm12
004DFA60  movaps   xmm5, xmm11
004DFA64  mulss    xmm5, xmm13
004DFA69  movaps   xmm7, xmm14
004DFA6D  movss    dword ptr [rip + 0x1b851db], xmm1  ; -> 02064C50
004DFA75  movss    dword ptr [rip + 0x1b851b2], xmm12  ; -> 02064C30
004DFA7E  mulss    xmm5, xmm1
004DFA82  movaps   xmm1, xmm2
004DFA85  shufps   xmm1, xmm1, 0
004DFA89  mulss    xmm10, xmm12
004DFA8E  movups   xmm0, xmmword ptr [r8 + rbp]
004DFA93  movups   xmm2, xmmword ptr [rip + 0x1b851c6]  ; -> 02064C60
004DFA9A  addss    xmm7, dword ptr [rip + 0x1922d92]  ; -> 01E02834 [u32 0x00000000]
004DFAA2  mulps    xmm2, xmm1
004DFAA5  movups   xmmword ptr [rip + 0x1b85224], xmm0  ; -> 02064CD0
004DFAAC  mulss    xmm7, xmm6
004DFAB0  mulss    xmm6, xmm12
004DFAB5  movss    xmm12, dword ptr [rsp + 0x110]
004DFABF  movups   xmm0, xmmword ptr [r15 + r8]
004DFAC4  movups   xmmword ptr [rip + 0x1b85195], xmm2  ; -> 02064C60
004DFACB  movups   xmmword ptr [rip + 0x1b8521e], xmm0  ; -> 02064CF0
004DFAD2  movups   xmm0, xmmword ptr [r12 + r8]
004DFAD7  movups   xmmword ptr [rip + 0x1b85222], xmm0  ; -> 02064D00
004DFADE  movups   xmm0, xmmword ptr [r8 + r13]
004DFAE3  movups   xmmword ptr [rip + 0x1b85226], xmm0  ; -> 02064D10
004DFAEA  movups   xmm0, xmmword ptr [rip + 0x1b8518f]  ; -> 02064C80
004DFAF1  movups   xmmword ptr [rcx + r8], xmm0
004DFAF6  movsxd   rcx, eax
004DFAF9  movups   xmmword ptr [rcx + r8], xmm2
004DFAFE  cmp      r9w, r11w
004DFB02  jne      0x4df6c0  ; -> 004DF6C0
004DFB08  mov      rax, qword ptr [rsp + 0x118]
004DFB10  lea      r15, [rip + 0x1b85319]  ; -> 02064E30
004DFB17  movsx    r8d, r11w
004DFB1B  add      r8w, r11w
004DFB1F  movss    dword ptr [rip + 0x1b850f9], xmm6  ; -> 02064C20
004DFB27  movsx    edx, r8w
004DFB2B  movzx    eax, word ptr [rax + r15]
004DFB30  mov      word ptr [rip + 0x1b8529d], ax  ; -> 02064DD4
004DFB37  movss    dword ptr [rip + 0x1b850e8], xmm10  ; -> 02064C28
004DFB40  lea      eax, [rdx + 0x80]
004DFB46  movss    dword ptr [rip + 0x1b850de], xmm5  ; -> 02064C2C
004DFB4E  shl      eax, 4
004DFB51  movsxd   rcx, eax
004DFB54  lea      eax, [rdx + 0x81]
004DFB5A  shl      eax, 4
004DFB5D  movss    dword ptr [rip + 0x1b850bf], xmm7  ; -> 02064C24
004DFB65  movups   xmmword ptr [rip + 0x1b85133], xmm8  ; -> 02064CA0
004DFB6D  mov      word ptr [rip + 0x1b85263], r8w  ; -> 02064DD8
004DFB75  movups   xmm1, xmmword ptr [rcx + r15]
004DFB7A  movsxd   rcx, eax
004DFB7D  movups   xmmword ptr [rip + 0x1b8515b], xmm15  ; -> 02064CE0
004DFB85  movups   xmmword ptr [rip + 0x1b850d4], xmm1  ; -> 02064C60
004DFB8C  movups   xmm0, xmmword ptr [rcx + r15]
004DFB91  movups   xmm2, xmm0
004DFB94  movups   xmmword ptr [rip + 0x1b850d5], xmm0  ; -> 02064C70
004DFB9B  movss    dword ptr [rip + 0x1b850cd], xmm2  ; -> 02064C70
004DFBA3  subss    xmm0, xmm1
004DFBA7  shufps   xmm2, xmm2, 0x55
004DFBAB  movss    dword ptr [rip + 0x1b850c1], xmm2  ; -> 02064C74
004DFBB3  subss    xmm2, dword ptr [rip + 0x1b850a9]  ; -> 02064C64
004DFBBB  ucomiss  xmm0, xmm9
004DFBBF  movss    dword ptr [rip + 0x1b8509d], xmm2  ; -> 02064C64
004DFBC7  movss    dword ptr [rip + 0x1b85091], xmm0  ; -> 02064C60
004DFBCF  jp       0x4dfbd3  ; -> 004DFBD3
004DFBD1  je       0x4dfbdb  ; -> 004DFBDB
004DFBD3  ucomiss  xmm2, xmm9
004DFBD7  jp       0x4dfbf0  ; -> 004DFBF0
004DFBD9  jne      0x4dfbf0  ; -> 004DFBF0
004DFBDB  call     0x22cc40  ; -> 0022CC40 fn
004DFBE0  movss    xmm2, dword ptr [rip + 0x1b8507c]  ; -> 02064C64
004DFBE8  movss    xmm0, dword ptr [rip + 0x1b85070]  ; -> 02064C60
004DFBF0  comiss   xmm9, xmm0
004DFBF4  ja       0x4dfbfc  ; -> 004DFBFC
004DFBF6  comiss   xmm9, xmm2
004DFBFA  jbe      0x4dfc01  ; -> 004DFC01
004DFBFC  call     0x22cc30  ; -> 0022CC30 fn
004DFC01  call     0x22cc20  ; -> 0022CC20 fn
004DFC06  movss    xmm1, dword ptr [rip + 0x1922c22]  ; -> 01E02830 [u32 0x00000000]
004DFC0E  subss    xmm1, dword ptr [rip + 0x1b8504e]  ; -> 02064C64
004DFC16  movss    xmm0, dword ptr [rip + 0x1922c16]  ; -> 01E02834 [u32 0x00000000]
004DFC1E  subss    xmm0, dword ptr [rip + 0x1b8503a]  ; -> 02064C60
004DFC26  movss    xmm6, dword ptr [rip + 0x1922c0e]  ; -> 01E0283C [f32 1]
004DFC2E  movsd    xmm10, qword ptr [rip + 0x180c149]  ; -> 01CEBD80 [u64 0x7FFFFFFFFFFFFFFF]
004DFC37  movss    dword ptr [rip + 0x1b85061], xmm1  ; -> 02064CA0
004DFC3F  mulss    xmm1, xmm1
004DFC43  movss    dword ptr [rip + 0x1b85059], xmm0  ; -> 02064CA4
004DFC4B  mulss    xmm0, xmm0
004DFC4F  movss    dword ptr [rip + 0x1b85029], xmm1  ; -> 02064C80
004DFC57  mulss    xmm1, xmm6
004DFC5B  movss    dword ptr [rip + 0x1b85021], xmm0  ; -> 02064C84
004DFC63  mulss    xmm0, xmm6
004DFC67  movss    dword ptr [rip + 0x1b84ebd], xmm1  ; -> 02064B2C
004DFC6F  addss    xmm0, xmm1
004DFC73  movss    dword ptr [rip + 0x1b85011], xmm0  ; -> 02064C8C
004DFC7B  cvtps2pd xmm0, xmm0
004DFC7E  andps    xmm0, xmm10
004DFC82  cvtpd2ps xmm0, xmm0
004DFC86  call     0x861f14  ; -> 00861F14 fn
004DFC8B  ucomiss  xmm0, xmm9
004DFC8F  jp       0x4dfc9f  ; -> 004DFC9F
004DFC91  jne      0x4dfc9f  ; -> 004DFC9F
004DFC93  mov      dword ptr [rip + 0x1b84e63], 0x7f7fffff  ; -> 02064B00
004DFC9D  jmp      0x4dfcab  ; -> 004DFCAB
004DFC9F  divss    xmm6, xmm0
004DFCA3  movss    dword ptr [rip + 0x1b84e55], xmm6  ; -> 02064B00
004DFCAB  movsx    edx, word ptr [rip + 0x1b85126]  ; -> 02064DD8
004DFCB2  lea      eax, [rdx + 0x81]
004DFCB8  shl      eax, 4
004DFCBB  movsxd   rcx, eax
004DFCBE  lea      eax, [rdx + 0x82]
004DFCC4  shl      eax, 4
004DFCC7  movups   xmm1, xmmword ptr [rcx + r15]
004DFCCC  movsxd   rcx, eax
004DFCCF  movups   xmmword ptr [rip + 0x1b84f8a], xmm1  ; -> 02064C60
004DFCD6  movups   xmm0, xmmword ptr [rcx + r15]
004DFCDB  movups   xmm2, xmm0
004DFCDE  movups   xmmword ptr [rip + 0x1b84f8b], xmm0  ; -> 02064C70
004DFCE5  movss    dword ptr [rip + 0x1b84f83], xmm2  ; -> 02064C70
004DFCED  subss    xmm0, xmm1
004DFCF1  shufps   xmm2, xmm2, 0x55
004DFCF5  movss    dword ptr [rip + 0x1b84f77], xmm2  ; -> 02064C74
004DFCFD  subss    xmm2, dword ptr [rip + 0x1b84f5f]  ; -> 02064C64
004DFD05  ucomiss  xmm0, xmm9
004DFD09  movss    dword ptr [rip + 0x1b84f53], xmm2  ; -> 02064C64
004DFD11  movss    dword ptr [rip + 0x1b84f47], xmm0  ; -> 02064C60
004DFD19  jp       0x4dfd1d  ; -> 004DFD1D
004DFD1B  je       0x4dfd25  ; -> 004DFD25
004DFD1D  ucomiss  xmm2, xmm9
004DFD21  jp       0x4dfd3a  ; -> 004DFD3A
004DFD23  jne      0x4dfd3a  ; -> 004DFD3A
004DFD25  call     0x22cc40  ; -> 0022CC40 fn
004DFD2A  movss    xmm2, dword ptr [rip + 0x1b84f32]  ; -> 02064C64
004DFD32  movss    xmm0, dword ptr [rip + 0x1b84f26]  ; -> 02064C60
004DFD3A  comiss   xmm9, xmm0
004DFD3E  ja       0x4dfd46  ; -> 004DFD46
004DFD40  comiss   xmm9, xmm2
004DFD44  jbe      0x4dfd4b  ; -> 004DFD4B
004DFD46  call     0x22cc30  ; -> 0022CC30 fn
004DFD4B  call     0x22cc20  ; -> 0022CC20 fn
004DFD50  movsx    ebx, word ptr [rip + 0x1b85081]  ; -> 02064DD8
004DFD57  movss    xmm1, dword ptr [rip + 0x1b84f45]  ; -> 02064CA4
004DFD5F  movss    xmm4, dword ptr [rip + 0x1922ac9]  ; -> 01E02830 [u32 0x00000000]
004DFD67  subss    xmm4, dword ptr [rip + 0x1b84ef5]  ; -> 02064C64
004DFD6F  movss    xmm3, dword ptr [rip + 0x1922abd]  ; -> 01E02834 [u32 0x00000000]
004DFD77  lea      eax, [rbx + 0x352]
004DFD7D  subss    xmm3, dword ptr [rip + 0x1b84edb]  ; -> 02064C60
004DFD85  movss    xmm8, dword ptr [rip + 0x1922aae]  ; -> 01E0283C [f32 1]
004DFD8E  inc      bx
004DFD91  mulss    xmm1, dword ptr [rip + 0x1b84d67]  ; -> 02064B00
004DFD99  movzx    r8d, word ptr [rip + 0x1b84d6b]  ; -> 02064B0C
004DFDA1  movaps   xmm0, xmm4
004DFDA4  shl      eax, 4
004DFDA7  cmp      r8w, word ptr [rip + 0x1b85025]  ; -> 02064DD4
004DFDAF  movaps   xmm6, xmm3
004DFDB2  mulss    xmm0, xmm4
004DFDB6  movsxd   rcx, eax
004DFDB9  mulss    xmm6, xmm3
004DFDBD  mov      word ptr [rip + 0x1b85014], bx  ; -> 02064DD8
004DFDC4  movss    dword ptr [rip + 0x1b84eb4], xmm0  ; -> 02064C80
004DFDCC  mulss    xmm0, xmm8
004DFDD1  movss    dword ptr [rip + 0x1b84eab], xmm6  ; -> 02064C84
004DFDD9  movss    dword ptr [rip + 0x1b84ec3], xmm1  ; -> 02064CA4
004DFDE1  movss    xmm1, dword ptr [rip + 0x1b84ed3]  ; -> 02064CBC
004DFDE9  movss    dword ptr [rip + 0x1b84d3b], xmm0  ; -> 02064B2C
004DFDF1  mulss    xmm6, xmm8
004DFDF6  movss    dword ptr [rip + 0x1b84eb2], xmm4  ; -> 02064CB0
004DFDFE  movss    dword ptr [rip + 0x1b84eae], xmm3  ; -> 02064CB4
004DFE06  addss    xmm6, xmm0
004DFE0A  movss    dword ptr [rip + 0x1b84e7e], xmm4  ; -> 02064C90
004DFE12  movss    xmm0, dword ptr [rip + 0x1b84e86]  ; -> 02064CA0
004DFE1A  mulss    xmm0, dword ptr [rip + 0x1b84cde]  ; -> 02064B00
004DFE22  movss    dword ptr [rip + 0x1b84e6a], xmm3  ; -> 02064C94
004DFE2A  movss    dword ptr [rip + 0x1b84e5a], xmm6  ; -> 02064C8C
004DFE32  movss    dword ptr [rip + 0x1b84e66], xmm0  ; -> 02064CA0
004DFE3A  movups   xmm2, xmmword ptr [rip + 0x1b84e5f]  ; -> 02064CA0
004DFE41  movss    xmm0, dword ptr [rip + 0x1b84e6f]  ; -> 02064CB8
004DFE49  movups   xmmword ptr [rcx + r15], xmm2
004DFE4E  movss    dword ptr [rip + 0x1b84e42], xmm0  ; -> 02064C98
004DFE56  movss    dword ptr [rip + 0x1b84e3e], xmm1  ; -> 02064C9C
004DFE5E  je       0x4e00c3  ; -> 004E00C3
004DFE64  movss    xmm7, dword ptr [rip + 0x180bd04]  ; -> 01CEBB70 [f32 0.5]
004DFE6C  nop      dword ptr [rax]
004DFE70  cvtps2pd xmm0, xmm6
004DFE73  andps    xmm0, xmm10
004DFE77  cvtpd2ps xmm0, xmm0
004DFE7B  call     0x861f14  ; -> 00861F14 fn
004DFE80  ucomiss  xmm0, xmm9
004DFE84  jp       0x4dfe94  ; -> 004DFE94
004DFE86  jne      0x4dfe94  ; -> 004DFE94
004DFE88  mov      dword ptr [rip + 0x1b84c6e], 0x7f7fffff  ; -> 02064B00
004DFE92  jmp      0x4dfea2  ; -> 004DFEA2
004DFE94  divss    xmm8, xmm0
004DFE99  movss    dword ptr [rip + 0x1b84c5e], xmm8  ; -> 02064B00
004DFEA2  movsx    edx, bx
004DFEA5  lea      eax, [rdx + 0x81]
004DFEAB  shl      eax, 4
004DFEAE  movsxd   rcx, eax
004DFEB1  lea      eax, [rdx + 0x82]
004DFEB7  shl      eax, 4
004DFEBA  movups   xmm1, xmmword ptr [rcx + r15]
004DFEBF  movsxd   rcx, eax
004DFEC2  movups   xmmword ptr [rip + 0x1b84d97], xmm1  ; -> 02064C60
004DFEC9  movups   xmm0, xmmword ptr [rcx + r15]
004DFECE  movups   xmm2, xmm0
004DFED1  movups   xmmword ptr [rip + 0x1b84d98], xmm0  ; -> 02064C70
004DFED8  movss    dword ptr [rip + 0x1b84d90], xmm2  ; -> 02064C70
004DFEE0  subss    xmm0, xmm1
004DFEE4  shufps   xmm2, xmm2, 0x55
004DFEE8  movss    dword ptr [rip + 0x1b84d84], xmm2  ; -> 02064C74
004DFEF0  subss    xmm2, dword ptr [rip + 0x1b84d6c]  ; -> 02064C64
004DFEF8  ucomiss  xmm0, xmm9
004DFEFC  movss    dword ptr [rip + 0x1b84d60], xmm2  ; -> 02064C64
004DFF04  movss    dword ptr [rip + 0x1b84d54], xmm0  ; -> 02064C60
004DFF0C  jp       0x4dff10  ; -> 004DFF10
004DFF0E  je       0x4dff18  ; -> 004DFF18
004DFF10  ucomiss  xmm2, xmm9
004DFF14  jp       0x4dff2d  ; -> 004DFF2D
004DFF16  jne      0x4dff2d  ; -> 004DFF2D
004DFF18  call     0x22cc40  ; -> 0022CC40 fn
004DFF1D  movss    xmm2, dword ptr [rip + 0x1b84d3f]  ; -> 02064C64
004DFF25  movss    xmm0, dword ptr [rip + 0x1b84d33]  ; -> 02064C60
004DFF2D  comiss   xmm9, xmm0
004DFF31  ja       0x4dff39  ; -> 004DFF39
004DFF33  comiss   xmm9, xmm2
004DFF37  jbe      0x4dff3e  ; -> 004DFF3E
004DFF39  call     0x22cc30  ; -> 0022CC30 fn
004DFF3E  call     0x22cc20  ; -> 0022CC20 fn
004DFF43  movss    xmm2, dword ptr [rip + 0x1b84d49]  ; -> 02064C94
004DFF4B  movss    xmm3, dword ptr [rip + 0x1b84d3d]  ; -> 02064C90
004DFF53  movsx    ebx, word ptr [rip + 0x1b84e7e]  ; -> 02064DD8
004DFF5A  movss    xmm5, dword ptr [rip + 0x19228ce]  ; -> 01E02830 [u32 0x00000000]
004DFF62  subss    xmm5, dword ptr [rip + 0x1b84cfa]  ; -> 02064C64
004DFF6A  movss    xmm4, dword ptr [rip + 0x19228c2]  ; -> 01E02834 [u32 0x00000000]
004DFF72  subss    xmm4, dword ptr [rip + 0x1b84ce6]  ; -> 02064C60
004DFF7A  mulss    xmm2, dword ptr [rip + 0x1b84b7e]  ; -> 02064B00
004DFF82  lea      eax, [rbx + 0x352]
004DFF88  inc      bx
004DFF8B  movzx    edx, word ptr [rip + 0x1b84e42]  ; -> 02064DD4
004DFF92  movss    xmm8, dword ptr [rip + 0x19228a1]  ; -> 01E0283C [f32 1]
004DFF9B  movaps   xmm1, xmm5
004DFF9E  mulss    xmm3, dword ptr [rip + 0x1b84b5a]  ; -> 02064B00
004DFFA6  dec      dx
004DFFA9  movzx    r8d, word ptr [rip + 0x1b84b5b]  ; -> 02064B0C
004DFFB1  mulss    xmm1, xmm5
004DFFB5  movaps   xmm0, xmm2
004DFFB8  shl      eax, 4
004DFFBB  movsxd   rcx, eax
004DFFBE  movaps   xmm6, xmm4
004DFFC1  mulss    xmm6, xmm4
004DFFC5  mov      word ptr [rip + 0x1b84e08], dx  ; -> 02064DD4
004DFFCC  movss    dword ptr [rip + 0x1b84cac], xmm1  ; -> 02064C80
004DFFD4  mulss    xmm1, xmm8
004DFFD9  mov      dword ptr [rip + 0x1b84b21], 0x3f000000  ; -> 02064B04
004DFFE3  movss    dword ptr [rip + 0x1b84c99], xmm6  ; -> 02064C84
004DFFEB  mulss    xmm6, xmm8
004DFFF0  mov      word ptr [rip + 0x1b84de1], bx  ; -> 02064DD8
004DFFF7  movss    dword ptr [rip + 0x1b84b2d], xmm1  ; -> 02064B2C
004DFFFF  movss    dword ptr [rip + 0x1b84ca9], xmm5  ; -> 02064CB0
004E0007  movss    dword ptr [rip + 0x1b84ca5], xmm4  ; -> 02064CB4
004E000F  addss    xmm6, xmm1
004E0013  movss    dword ptr [rip + 0x1b84c75], xmm5  ; -> 02064C90
004E001B  movaps   xmm1, xmm3
004E001E  movss    dword ptr [rip + 0x1b84c6e], xmm4  ; -> 02064C94
004E0026  addss    xmm0, dword ptr [rip + 0x1b84c76]  ; -> 02064CA4
004E002E  movss    dword ptr [rip + 0x1b84c6e], xmm2  ; -> 02064CA4
004E0036  movss    dword ptr [rip + 0x1b84c4e], xmm6  ; -> 02064C8C
004E003E  addss    xmm1, dword ptr [rip + 0x1b84c5a]  ; -> 02064CA0
004E0046  movss    dword ptr [rip + 0x1b84c52], xmm3  ; -> 02064CA0
004E004E  mulss    xmm0, xmm7
004E0052  mulss    xmm1, xmm7
004E0056  movss    dword ptr [rip + 0x1b84c16], xmm0  ; -> 02064C74
004E005E  movss    xmm0, dword ptr [rip + 0x1b84c32]  ; -> 02064C98
004E0066  movss    dword ptr [rip + 0x1b84c02], xmm1  ; -> 02064C70
004E006E  movss    xmm1, dword ptr [rip + 0x1b84c26]  ; -> 02064C9C
004E0076  movss    dword ptr [rip + 0x1b84c2a], xmm0  ; -> 02064CA8
004E007E  movss    dword ptr [rip + 0x1b84c26], xmm1  ; -> 02064CAC
004E0086  movss    xmm1, dword ptr [rip + 0x1b84c2e]  ; -> 02064CBC
004E008E  movss    dword ptr [rip + 0x1b84c06], xmm1  ; -> 02064C9C
004E0096  movups   xmm0, xmmword ptr [rip + 0x1b84bd3]  ; -> 02064C70
004E009D  movups   xmmword ptr [rcx + r15], xmm0
004E00A2  movss    xmm0, dword ptr [rip + 0x1b84c0e]  ; -> 02064CB8
004E00AA  movss    dword ptr [rip + 0x1b84be6], xmm0  ; -> 02064C98
004E00B2  cmp      r8w, dx
004E00B6  jne      0x4dfe70  ; -> 004DFE70
004E00BC  movups   xmm2, xmmword ptr [rip + 0x1b84bdd]  ; -> 02064CA0
004E00C3  movss    xmm12, dword ptr [rip + 0x180bbb8]  ; -> 01CEBC84 [f32 16]
004E00CC  mov      ebp, 0xe0
004E00D1  movss    xmm1, dword ptr [rip + 0x1b84b2f]  ; -> 02064C08
004E00D9  movsx    r9d, r8w
004E00DD  movsx    eax, bx
004E00E0  add      eax, 0x352
004E00E5  shl      eax, 4
004E00E8  movsxd   rcx, eax
004E00EB  lea      eax, [r9 + 4]
004E00EF  shl      eax, 4
004E00F2  movups   xmmword ptr [rcx + r15], xmm2
004E00F7  movsxd   rcx, eax
004E00FA  movzx    eax, word ptr [rcx + r15]
004E00FF  add      ax, 2
004E0103  add      r9w, r8w
004E0107  mov      word ptr [rip + 0x1b84cc6], ax  ; -> 02064DD4
004E010E  mov      word ptr [rip + 0x1b84cc2], r9w  ; -> 02064DD8
004E0116  nop      word ptr [rax + rax]
004E0120  mulss    xmm1, dword ptr [rip + 0x1b84aec]  ; -> 02064C14
004E0128  movsx    ecx, r9w
004E012C  movups   xmm0, xmmword ptr [rip + 0x1b84bad]  ; -> 02064CE0
004E0133  addss    xmm1, dword ptr [rip + 0x1b84ad5]  ; -> 02064C10
004E013B  lea      eax, [rcx + 0x2bc]
004E0141  shl      eax, 4
004E0144  movsxd   rdx, eax
004E0147  lea      eax, [rcx + 0x352]
004E014D  shl      eax, 4
004E0150  movsxd   rcx, eax
004E0153  movups   xmm7, xmmword ptr [rdx + r15]
004E0158  movups   xmm10, xmmword ptr [rcx + r15]
004E015D  movups   xmmword ptr [rip + 0x1b84afc], xmm7  ; -> 02064C60
004E0164  movaps   xmm6, xmm7
004E0167  movaps   xmm2, xmm7
004E016A  shufps   xmm2, xmm7, 0x55
004E016E  movups   xmmword ptr [rip + 0x1b84afa], xmm10  ; -> 02064C70
004E0176  movss    xmm11, dword ptr [rip + 0x1b84af5]  ; -> 02064C74
004E017F  mulss    xmm10, xmm1
004E0184  mulss    xmm11, xmm1
004E0189  movaps   xmm1, xmm2
004E018C  mulss    xmm1, dword ptr [rip + 0x1b84b64]  ; -> 02064CF8
004E0194  shufps   xmm6, xmm6, 0
004E0198  mulps    xmm6, xmm0
004E019B  movaps   xmm0, xmm2
004E019E  mulss    xmm0, dword ptr [rip + 0x1b84b4a]  ; -> 02064CF0
004E01A6  movups   xmmword ptr [rip + 0x1b84af3], xmm7  ; -> 02064CA0
004E01AD  movups   xmmword ptr [rip + 0x1b8496c], xmm6  ; -> 02064B20
004E01B4  movss    xmm5, dword ptr [rip + 0x1b84970]  ; -> 02064B2C
004E01BC  addss    xmm6, xmm0
004E01C0  movss    xmm3, dword ptr [rip + 0x1b8495c]  ; -> 02064B24
004E01C8  movaps   xmm0, xmm2
004E01CB  mulss    xmm0, dword ptr [rip + 0x1b84b21]  ; -> 02064CF4
004E01D3  mulss    xmm2, dword ptr [rip + 0x1b84b21]  ; -> 02064CFC
004E01DB  movss    xmm4, dword ptr [rip + 0x1b84945]  ; -> 02064B28
004E01E3  addss    xmm3, xmm0
004E01E7  addss    xmm4, xmm1
004E01EB  movss    dword ptr [rip + 0x1b84a7c], xmm10  ; -> 02064C70
004E01F4  addss    xmm5, xmm2
004E01F8  movss    dword ptr [rip + 0x1b84a73], xmm11  ; -> 02064C74
004E0201  movaps   xmm2, xmm7
004E0204  shufps   xmm2, xmm7, 0xaa
004E0208  shufps   xmm7, xmm7, 0xff
004E020C  movaps   xmm0, xmm2
004E020F  mulss    xmm0, dword ptr [rip + 0x1b84ae9]  ; -> 02064D00
004E0217  movaps   xmm1, xmm2
004E021A  mulss    xmm1, dword ptr [rip + 0x1b84ae2]  ; -> 02064D04
004E0222  addss    xmm6, xmm0
004E0226  movaps   xmm0, xmm2
004E0229  mulss    xmm0, dword ptr [rip + 0x1b84ad7]  ; -> 02064D08
004E0231  mulss    xmm2, dword ptr [rip + 0x1b84ad3]  ; -> 02064D0C
004E0239  addss    xmm3, xmm1
004E023D  addss    xmm4, xmm0
004E0241  movss    dword ptr [rip + 0x1b848d7], xmm6  ; -> 02064B20
004E0249  movaps   xmm0, xmm7
004E024C  movaps   xmm1, xmm7
004E024F  mulss    xmm0, dword ptr [rip + 0x1b84ab9]  ; -> 02064D10
004E0257  addss    xmm5, xmm2
004E025B  mulss    xmm1, dword ptr [rip + 0x1b84ab1]  ; -> 02064D14
004E0263  addss    xmm0, xmm6
004E0267  movss    dword ptr [rip + 0x1b848b5], xmm3  ; -> 02064B24
004E026F  movss    dword ptr [rip + 0x1b848b1], xmm4  ; -> 02064B28
004E0277  addss    xmm1, xmm3
004E027B  movss    dword ptr [rip + 0x1b848a9], xmm5  ; -> 02064B2C
004E0283  movss    dword ptr [rip + 0x1b849d5], xmm0  ; -> 02064C60
004E028B  movaps   xmm0, xmm7
004E028E  mulss    xmm7, dword ptr [rip + 0x1b84a86]  ; -> 02064D1C
004E0296  mulss    xmm0, dword ptr [rip + 0x1b84a7a]  ; -> 02064D18
004E029E  addss    xmm7, xmm5
004E02A2  movss    dword ptr [rip + 0x1b849ba], xmm1  ; -> 02064C64
004E02AA  addss    xmm0, xmm4
004E02AE  ucomiss  xmm7, xmm9
004E02B2  movss    dword ptr [rip + 0x1b849ae], xmm0  ; -> 02064C68
004E02BA  movss    dword ptr [rip + 0x1b849aa], xmm7  ; -> 02064C6C
004E02C2  jp       0x4e02d2  ; -> 004E02D2
004E02C4  jne      0x4e02d2  ; -> 004E02D2
004E02C6  mov      dword ptr [rip + 0x1b84830], 0x7f7fffff  ; -> 02064B00
004E02D0  jmp      0x4e02e0  ; -> 004E02E0
004E02D2  divss    xmm8, xmm7
004E02D7  movss    dword ptr [rip + 0x1b84820], xmm8  ; -> 02064B00
004E02E0  movss    xmm3, dword ptr [rip + 0x1b849b8]  ; -> 02064CA0
004E02E8  movaps   xmm0, xmm10
004E02EC  movss    xmm2, dword ptr [rip + 0x1b849b0]  ; -> 02064CA4
004E02F4  addss    xmm0, xmm3
004E02F8  movaps   xmm1, xmm11
004E02FC  subss    xmm3, xmm10
004E0301  addss    xmm1, xmm2
004E0305  subss    xmm2, xmm11
004E030A  movss    dword ptr [rip + 0x1b8496e], xmm0  ; -> 02064C80
004E0312  ucomiss  xmm3, xmm9
004E0316  movss    xmm0, dword ptr [rip + 0x1b8498a]  ; -> 02064CA8
004E031E  movss    dword ptr [rip + 0x1b8495e], xmm1  ; -> 02064C84
004E0326  movss    xmm1, dword ptr [rip + 0x1b8497e]  ; -> 02064CAC
004E032E  movss    dword ptr [rip + 0x1b84962], xmm0  ; -> 02064C98
004E0336  movss    dword ptr [rip + 0x1b8495e], xmm1  ; -> 02064C9C
004E033E  movss    dword ptr [rip + 0x1b8494a], xmm3  ; -> 02064C90
004E0346  movss    dword ptr [rip + 0x1b84946], xmm2  ; -> 02064C94
004E034E  jp       0x4e0352  ; -> 004E0352
004E0350  je       0x4e035a  ; -> 004E035A
004E0352  ucomiss  xmm2, xmm9
004E0356  jp       0x4e036f  ; -> 004E036F
004E0358  jne      0x4e036f  ; -> 004E036F
004E035A  call     0x22cc40  ; -> 0022CC40 fn
004E035F  movss    xmm2, dword ptr [rip + 0x1b8492d]  ; -> 02064C94
004E0367  movss    xmm3, dword ptr [rip + 0x1b84921]  ; -> 02064C90
004E036F  comiss   xmm9, xmm3
004E0373  ja       0x4e037b  ; -> 004E037B
004E0375  comiss   xmm9, xmm2
004E0379  jbe      0x4e0380  ; -> 004E0380
004E037B  call     0x22cc30  ; -> 0022CC30 fn
004E0380  call     0x22cc20  ; -> 0022CC20 fn
004E0385  movss    xmm2, dword ptr [rip + 0x1b848f7]  ; -> 02064C84
004E038D  movss    xmm6, dword ptr [rip + 0x1b848eb]  ; -> 02064C80
004E0395  movaps   xmm0, xmm2
004E0398  mulss    xmm0, dword ptr [rip + 0x1b84950]  ; -> 02064CF0
004E03A0  movaps   xmm1, xmm2
004E03A3  movups   xmm7, xmmword ptr [rip + 0x1b84936]  ; -> 02064CE0
004E03AA  movss    xmm11, dword ptr [rip + 0x1b84949]  ; -> 02064CFC
004E03B3  movss    xmm14, dword ptr [rip + 0x1b84938]  ; -> 02064CF4
004E03BC  movss    xmm13, dword ptr [rip + 0x1b84933]  ; -> 02064CF8
004E03C5  movss    xmm15, dword ptr [rip + 0x1b84892]  ; -> 02064C60
004E03CE  movss    xmm8, dword ptr [rip + 0x1922465]  ; -> 01E0283C [f32 1]
004E03D7  mulss    xmm1, xmm13
004E03DC  shufps   xmm6, xmm6, 0
004E03E0  mulps    xmm6, xmm7
004E03E3  movups   xmmword ptr [rip + 0x1b84736], xmm6  ; -> 02064B20
004E03EA  movss    xmm5, dword ptr [rip + 0x1b8473a]  ; -> 02064B2C
004E03F2  addss    xmm6, xmm0
004E03F6  movss    xmm3, dword ptr [rip + 0x1b84726]  ; -> 02064B24
004E03FE  movaps   xmm0, xmm2
004E0401  movss    xmm4, dword ptr [rip + 0x1b8471f]  ; -> 02064B28
004E0409  mulss    xmm0, xmm14
004E040E  addss    xmm4, xmm1
004E0412  mulss    xmm2, xmm11
004E0417  addss    xmm3, xmm0
004E041B  addss    xmm5, xmm2
004E041F  movss    xmm2, dword ptr [rip + 0x1b84881]  ; -> 02064CA8
004E0427  movaps   xmm0, xmm2
004E042A  movaps   xmm1, xmm2
004E042D  mulss    xmm0, dword ptr [rip + 0x1b848cb]  ; -> 02064D00
004E0435  mulss    xmm1, dword ptr [rip + 0x1b848c7]  ; -> 02064D04
004E043D  addss    xmm6, xmm0
004E0441  movaps   xmm0, xmm2
004E0444  mulss    xmm0, dword ptr [rip + 0x1b848bc]  ; -> 02064D08
004E044C  mulss    xmm2, dword ptr [rip + 0x1b848b8]  ; -> 02064D0C
004E0454  addss    xmm3, xmm1
004E0458  addss    xmm4, xmm0
004E045C  addss    xmm5, xmm2
004E0460  movss    xmm2, dword ptr [rip + 0x1b84844]  ; -> 02064CAC
004E0468  movaps   xmm0, xmm2
004E046B  movaps   xmm1, xmm2
004E046E  mulss    xmm0, dword ptr [rip + 0x1b8489a]  ; -> 02064D10
004E0476  mulss    xmm1, dword ptr [rip + 0x1b84896]  ; -> 02064D14
004E047E  addss    xmm0, xmm6
004E0482  addss    xmm1, xmm3
004E0486  movss    dword ptr [rip + 0x1b847f2], xmm0  ; -> 02064C80
004E048E  movaps   xmm0, xmm2
004E0491  mulss    xmm0, dword ptr [rip + 0x1b8487f]  ; -> 02064D18
004E0499  mulss    xmm2, dword ptr [rip + 0x1b8487b]  ; -> 02064D1C
004E04A1  movss    dword ptr [rip + 0x1b847db], xmm1  ; -> 02064C84
004E04A9  addss    xmm0, xmm4
004E04AD  movss    xmm1, dword ptr [rip + 0x1b847af]  ; -> 02064C64
004E04B5  addss    xmm2, xmm5
004E04B9  movss    dword ptr [rip + 0x1b847c7], xmm0  ; -> 02064C88
004E04C1  movss    xmm0, dword ptr [rip + 0x1b84637]  ; -> 02064B00
004E04C9  ucomiss  xmm2, xmm9
004E04CD  mulss    xmm1, xmm0
004E04D1  mulss    xmm15, xmm0
004E04D6  movss    dword ptr [rsp + 0x110], xmm1
004E04DF  movss    xmm1, dword ptr [rip + 0x1b84781]  ; -> 02064C68
004E04E7  mulss    xmm1, xmm0
004E04EB  mulss    xmm0, xmm8
004E04F0  movss    dword ptr [rip + 0x1b84794], xmm2  ; -> 02064C8C
004E04F8  movss    dword ptr [rsp + 0x118], xmm1
004E0501  movss    dword ptr [rip + 0x1b84763], xmm0  ; -> 02064C6C
004E0509  jp       0x4e0518  ; -> 004E0518
004E050B  jne      0x4e0518  ; -> 004E0518
004E050D  movss    xmm10, dword ptr [rip + 0x41fe4a]  ; -> 00900360 [u32 0x7F7FFFFF]
004E0516  jmp      0x4e0521  ; -> 004E0521
004E0518  movaps   xmm10, xmm8
004E051C  divss    xmm10, xmm2
004E0521  movss    xmm2, dword ptr [rip + 0x1b8476b]  ; -> 02064C94
004E0529  movss    xmm6, dword ptr [rip + 0x1b8475f]  ; -> 02064C90
004E0531  movaps   xmm0, xmm2
004E0534  mulss    xmm0, dword ptr [rip + 0x1b847b4]  ; -> 02064CF0
004E053C  movaps   xmm1, xmm2
004E053F  mulss    xmm1, xmm13
004E0544  shufps   xmm6, xmm6, 0
004E0548  mulps    xmm6, xmm7
004E054B  movss    xmm7, dword ptr [rip + 0x1b84749]  ; -> 02064C9C
004E0553  movups   xmmword ptr [rip + 0x1b845c6], xmm6  ; -> 02064B20
004E055A  movss    xmm5, dword ptr [rip + 0x1b845ca]  ; -> 02064B2C
004E0562  addss    xmm6, xmm0
004E0566  movss    xmm3, dword ptr [rip + 0x1b845b6]  ; -> 02064B24
004E056E  movaps   xmm0, xmm2
004E0571  movss    xmm4, dword ptr [rip + 0x1b845af]  ; -> 02064B28
004E0579  mulss    xmm0, xmm14
004E057E  addss    xmm4, xmm1
004E0582  mulss    xmm2, xmm11
004E0587  addss    xmm3, xmm0
004E058B  addss    xmm5, xmm2
004E058F  movss    xmm2, dword ptr [rip + 0x1b84701]  ; -> 02064C98
004E0597  movaps   xmm0, xmm2
004E059A  movaps   xmm1, xmm2
004E059D  mulss    xmm0, dword ptr [rip + 0x1b8475b]  ; -> 02064D00
004E05A5  mulss    xmm1, dword ptr [rip + 0x1b84757]  ; -> 02064D04
004E05AD  addss    xmm6, xmm0
004E05B1  movaps   xmm0, xmm2
004E05B4  mulss    xmm0, dword ptr [rip + 0x1b8474c]  ; -> 02064D08
004E05BC  mulss    xmm2, dword ptr [rip + 0x1b84748]  ; -> 02064D0C
004E05C4  addss    xmm3, xmm1
004E05C8  addss    xmm4, xmm0
004E05CC  movss    dword ptr [rip + 0x1b8454c], xmm6  ; -> 02064B20
004E05D4  movaps   xmm0, xmm7
004E05D7  movaps   xmm1, xmm7
004E05DA  mulss    xmm0, dword ptr [rip + 0x1b8472e]  ; -> 02064D10
004E05E2  addss    xmm5, xmm2
004E05E6  mulss    xmm1, dword ptr [rip + 0x1b84726]  ; -> 02064D14
004E05EE  addss    xmm0, xmm6
004E05F2  movss    dword ptr [rip + 0x1b8452a], xmm3  ; -> 02064B24
004E05FA  movss    dword ptr [rip + 0x1b84526], xmm4  ; -> 02064B28
004E0602  addss    xmm1, xmm3
004E0606  movss    dword ptr [rip + 0x1b8451e], xmm5  ; -> 02064B2C
004E060E  movss    dword ptr [rip + 0x1b8467a], xmm0  ; -> 02064C90
004E0616  movaps   xmm0, xmm7
004E0619  mulss    xmm0, dword ptr [rip + 0x1b846f7]  ; -> 02064D18
004E0621  mulss    xmm7, dword ptr [rip + 0x1b846f3]  ; -> 02064D1C
004E0629  addss    xmm0, xmm4
004E062D  movss    dword ptr [rip + 0x1b8465f], xmm1  ; -> 02064C94
004E0635  movups   xmm1, xmmword ptr [rip + 0x1b84644]  ; -> 02064C80
004E063C  addss    xmm7, xmm5
004E0640  movss    dword ptr [rip + 0x1b84650], xmm0  ; -> 02064C98
004E0648  movaps   xmm0, xmm10
004E064C  shufps   xmm0, xmm0, 0
004E0650  mulps    xmm1, xmm0
004E0653  ucomiss  xmm7, xmm9
004E0657  mulss    xmm10, xmm8
004E065C  movups   xmmword ptr [rip + 0x1b8461d], xmm1  ; -> 02064C80
004E0663  movss    dword ptr [rip + 0x1b84620], xmm10  ; -> 02064C8C
004E066C  movss    dword ptr [rip + 0x1b84628], xmm7  ; -> 02064C9C
004E0674  jp       0x4e0682  ; -> 004E0682
004E0676  jne      0x4e0682  ; -> 004E0682
004E0678  movss    xmm2, dword ptr [rip + 0x41fce0]  ; -> 00900360 [u32 0x7F7FFFFF]
004E0680  jmp      0x4e068a  ; -> 004E068A
004E0682  movaps   xmm2, xmm8
004E0686  divss    xmm2, xmm7
004E068A  movups   xmm1, xmmword ptr [rip + 0x1b845ff]  ; -> 02064C90
004E0691  movss    xmm10, dword ptr [rip + 0x1b84496]  ; -> 02064B30
004E069A  movaps   xmm0, xmm2
004E069D  movss    xmm5, dword ptr [rip + 0x1b845db]  ; -> 02064C80
004E06A5  ucomiss  xmm10, xmm5
004E06A9  shufps   xmm0, xmm0, 0
004E06AD  mulps    xmm1, xmm0
004E06B0  movss    dword ptr [rip + 0x1b84448], xmm2  ; -> 02064B00
004E06B8  mulss    xmm2, xmm8
004E06BD  movups   xmmword ptr [rip + 0x1b845cc], xmm1  ; -> 02064C90
004E06C4  movss    dword ptr [rip + 0x1b845d0], xmm2  ; -> 02064C9C
004E06CC  jp       0x4e06d8  ; -> 004E06D8
004E06CE  jne      0x4e06d8  ; -> 004E06D8
004E06D0  mov      r9d, 1
004E06D6  jmp      0x4e06db  ; -> 004E06DB
004E06D8  xor      r9d, r9d
004E06DB  movss    xmm7, dword ptr [rip + 0x1b84451]  ; -> 02064B34
004E06E3  movss    xmm4, dword ptr [rip + 0x1b84599]  ; -> 02064C84
004E06EB  ucomiss  xmm7, xmm4
004E06EE  jp       0x4e06fa  ; -> 004E06FA
004E06F0  jne      0x4e06fa  ; -> 004E06FA
004E06F2  mov      r8d, 1
004E06F8  jmp      0x4e06fd  ; -> 004E06FD
004E06FA  xor      r8d, r8d
004E06FD  movss    xmm1, dword ptr [rip + 0x1b84433]  ; -> 02064B38
004E0705  movss    xmm3, dword ptr [rip + 0x1b8457b]  ; -> 02064C88
004E070D  ucomiss  xmm1, xmm3
004E0710  jp       0x4e071b  ; -> 004E071B
004E0712  jne      0x4e071b  ; -> 004E071B
004E0714  mov      edx, 1
004E0719  jmp      0x4e071d  ; -> 004E071D
004E071B  xor      edx, edx
004E071D  movzx    edi, word ptr [rip + 0x1b846b0]  ; -> 02064DD4
004E0724  xor      ecx, ecx
004E0726  movss    xmm14, dword ptr [rip + 0x1922101]  ; -> 01E02830 [u32 0x00000000]
004E072F  comiss   xmm5, xmm10
004E0733  seta     cl
004E0736  xor      eax, eax
004E0738  add      cx, cx
004E073B  comiss   xmm4, xmm7
004E073E  seta     al
004E0741  add      cx, ax
004E0744  xor      eax, eax
004E0746  add      cx, cx
004E0749  comiss   xmm3, xmm1
004E074C  seta     al
004E074F  dec      di
004E0752  add      cx, ax
004E0755  mov      word ptr [rip + 0x1b84678], di  ; -> 02064DD4
004E075C  shl      cx, 2
004E0760  add      cx, r9w
004E0764  add      cx, cx
004E0767  add      cx, r8w
004E076B  add      cx, cx
004E076E  add      cx, dx
004E0771  add      cx, cx
004E0774  ucomiss  xmm5, xmm14
004E0778  mov      word ptr [rip + 0x1b84391], cx  ; -> 02064B10
004E077F  jp       0x4e078b  ; -> 004E078B
004E0781  jne      0x4e078b  ; -> 004E078B
004E0783  mov      r10d, 1
004E0789  jmp      0x4e078e  ; -> 004E078E
004E078B  xor      r10d, r10d
004E078E  movss    xmm13, dword ptr [rip + 0x192209d]  ; -> 01E02834 [u32 0x00000000]
004E0797  ucomiss  xmm4, xmm13
004E079B  jp       0x4e07a7  ; -> 004E07A7
004E079D  jne      0x4e07a7  ; -> 004E07A7
004E079F  mov      r9d, 1
004E07A5  jmp      0x4e07aa  ; -> 004E07AA
004E07A7  xor      r9d, r9d
004E07AA  movss    xmm11, dword ptr [rip + 0x1922085]  ; -> 01E02838 [u32 0x00000000]
004E07B3  ucomiss  xmm3, xmm11
004E07B7  jp       0x4e07c2  ; -> 004E07C2
004E07B9  jne      0x4e07c2  ; -> 004E07C2
004E07BB  mov      edx, 1
004E07C0  jmp      0x4e07c4  ; -> 004E07C4
004E07C2  xor      edx, edx
004E07C4  movss    xmm6, dword ptr [rip + 0x1b844c4]  ; -> 02064C90
004E07CC  xor      r8d, r8d
004E07CF  comiss   xmm14, xmm5
004E07D3  seta     r8b
004E07D7  xor      eax, eax
004E07D9  add      r8w, r8w
004E07DD  comiss   xmm13, xmm4
004E07E1  seta     al
004E07E4  add      r8w, ax
004E07E8  xor      eax, eax
004E07EA  add      r8w, r8w
004E07EE  comiss   xmm11, xmm3
004E07F2  seta     al
004E07F5  add      r8w, ax
004E07F9  shl      r8w, 2
004E07FE  add      r8w, r10w
004E0802  add      r8w, r8w
004E0806  add      r8w, r9w
004E080A  add      r8w, r8w
004E080E  add      r8w, dx
004E0812  add      r8w, r8w
004E0816  ucomiss  xmm10, xmm6
004E081A  mov      word ptr [rip + 0x1b842f0], r8w  ; -> 02064B12
004E0822  jp       0x4e082e  ; -> 004E082E
004E0824  jne      0x4e082e  ; -> 004E082E
004E0826  mov      r10d, 1
004E082C  jmp      0x4e0831  ; -> 004E0831
004E082E  xor      r10d, r10d
004E0831  movss    xmm2, dword ptr [rip + 0x1b8445b]  ; -> 02064C94
004E0839  ucomiss  xmm7, xmm2
004E083C  jp       0x4e0848  ; -> 004E0848
004E083E  jne      0x4e0848  ; -> 004E0848
004E0840  mov      r9d, 1
004E0846  jmp      0x4e084b  ; -> 004E084B
004E0848  xor      r9d, r9d
004E084B  movss    xmm0, dword ptr [rip + 0x1b84445]  ; -> 02064C98
004E0853  ucomiss  xmm1, xmm0
004E0856  jp       0x4e0861  ; -> 004E0861
004E0858  jne      0x4e0861  ; -> 004E0861
004E085A  mov      edx, 1
004E085F  jmp      0x4e0863  ; -> 004E0863
004E0861  xor      edx, edx
004E0863  xor      ebx, ebx
004E0865  comiss   xmm6, xmm10
004E0869  seta     bl
004E086C  xor      eax, eax
004E086E  add      bx, bx
004E0871  comiss   xmm2, xmm7
004E0874  seta     al
004E0877  add      bx, ax
004E087A  xor      eax, eax
004E087C  add      bx, bx
004E087F  comiss   xmm0, xmm1
004E0882  seta     al
004E0885  add      bx, ax
004E0888  shl      bx, 2
004E088C  add      bx, r10w
004E0890  add      bx, bx
004E0893  add      bx, r9w
004E0897  add      bx, bx
004E089A  add      bx, dx
004E089D  add      bx, bx
004E08A0  ucomiss  xmm6, xmm14
004E08A4  mov      word ptr [rip + 0x1b84269], bx  ; -> 02064B14
004E08AB  jp       0x4e08b7  ; -> 004E08B7
004E08AD  jne      0x4e08b7  ; -> 004E08B7
004E08AF  mov      r11d, 1
004E08B5  jmp      0x4e08ba  ; -> 004E08BA
004E08B7  xor      r11d, r11d
004E08BA  ucomiss  xmm2, xmm13
004E08BE  jp       0x4e08ca  ; -> 004E08CA
004E08C0  jne      0x4e08ca  ; -> 004E08CA
004E08C2  mov      r9d, 1
004E08C8  jmp      0x4e08cd  ; -> 004E08CD
004E08CA  xor      r9d, r9d
004E08CD  ucomiss  xmm0, xmm11
004E08D1  jp       0x4e08dc  ; -> 004E08DC
004E08D3  jne      0x4e08dc  ; -> 004E08DC
004E08D5  mov      edx, 1
004E08DA  jmp      0x4e08de  ; -> 004E08DE
004E08DC  xor      edx, edx
004E08DE  movss    xmm1, dword ptr [rip + 0x1b84322]  ; -> 02064C08
004E08E6  xor      r10d, r10d
004E08E9  movzx    esi, word ptr [rip + 0x1b8421c]  ; -> 02064B0C
004E08F0  addss    xmm1, dword ptr [rip + 0x1b84314]  ; -> 02064C0C
004E08F8  comiss   xmm14, xmm6
004E08FC  mulss    xmm3, xmm12
004E0901  seta     r10b
004E0905  mulss    xmm5, xmm12
004E090A  xor      eax, eax
004E090C  add      r10w, r10w
004E0910  mulss    xmm4, xmm12
004E0915  comiss   xmm13, xmm2
004E0919  mulss    xmm15, xmm12
004E091E  seta     al
004E0921  mulss    xmm6, xmm12
004E0926  add      r10w, ax
004E092A  xor      eax, eax
004E092C  add      r10w, r10w
004E0930  mulss    xmm2, xmm12
004E0935  comiss   xmm11, xmm0
004E0939  mulss    xmm0, xmm12
004E093E  seta     al
004E0941  movss    dword ptr [rip + 0x1b842bf], xmm1  ; -> 02064C08
004E0949  add      r10w, ax
004E094D  shl      r10w, 2
004E0952  add      r10w, r11w
004E0956  add      r10w, r10w
004E095A  add      r10w, r9w
004E095E  lea      r9d, [rsi + rbp]
004E0962  cvttss2si eax, xmm5
004E0966  add      r10w, r10w
004E096A  movzx    r11d, r9w
004E096E  add      r10w, dx
004E0972  and      r11w, cx
004E0976  movzx    edx, r9w
004E097A  movzx    ecx, r9w
004E097E  and      dx, r8w
004E0982  add      r10w, r10w
004E0986  and      r9w, r10w
004E098A  mov      word ptr [rip + 0x1b8444f], dx  ; -> 02064DE0
004E0991  and      cx, bx
004E0994  mov      word ptr [rip + 0x1b8444c], r9w  ; -> 02064DE8
004E099C  mov      word ptr [rip + 0x1b84441], cx  ; -> 02064DE4
004E09A3  mov      dword ptr [rip + 0x1b842d7], eax  ; -> 02064C80
004E09A9  cvttss2si eax, xmm4
004E09AD  mov      word ptr [rip + 0x1b84161], r10w  ; -> 02064B16
004E09B5  mov      dword ptr [rip + 0x1b842c9], eax  ; -> 02064C84
004E09BB  cvttss2si eax, xmm3
004E09BF  movss    xmm3, dword ptr [rsp + 0x110]
004E09C8  mov      dword ptr [rip + 0x1b842ba], eax  ; -> 02064C88
004E09CE  mulss    xmm3, xmm12
004E09D3  cvttss2si eax, xmm15
004E09D8  mov      dword ptr [rip + 0x1b84282], eax  ; -> 02064C60
004E09DE  cvttss2si eax, xmm3
004E09E2  movss    xmm3, dword ptr [rsp + 0x118]
004E09EB  mov      dword ptr [rip + 0x1b84273], eax  ; -> 02064C64
004E09F1  cvttss2si eax, xmm6
004E09F5  mulss    xmm3, xmm12
004E09FA  mov      dword ptr [rip + 0x1b84290], eax  ; -> 02064C90
004E0A00  cvttss2si eax, xmm2
004E0A04  cvttss2si r8d, xmm3
004E0A09  mov      dword ptr [rip + 0x1b84285], eax  ; -> 02064C94
004E0A0F  cvttss2si eax, xmm0
004E0A13  mov      dword ptr [rip + 0x1b8424e], r8d  ; -> 02064C68
004E0A1A  movsd    xmm0, qword ptr [rip + 0x1b8423e]  ; -> 02064C60
004E0A22  mov      dword ptr [rip + 0x1b84270], eax  ; -> 02064C98
004E0A28  movsx    eax, dx
004E0A2B  movsx    edx, cx
004E0A2E  add      dx, ax
004E0A31  movsx    ecx, r9w
004E0A35  movsx    r9d, word ptr [rip + 0x1b8439b]  ; -> 02064DD8
004E0A3D  add      dx, cx
004E0A40  add      r11w, dx
004E0A44  mov      word ptr [rip + 0x1b84390], r11w  ; -> 02064DDC
004E0A4C  lea      eax, [r9 + 0x100]
004E0A53  shl      eax, 4
004E0A56  movsxd   r10, eax
004E0A59  lea      eax, [r9 + 0x180]
004E0A60  shl      eax, 4
004E0A63  movsd    qword ptr [r10 + r15], xmm0
004E0A69  mov      dword ptr [r10 + r15 + 8], r8d
004E0A6E  movups   xmm0, xmmword ptr [rip + 0x1b8421b]  ; -> 02064C90
004E0A75  movsxd   rcx, eax
004E0A78  lea      eax, [r9 + 0x80]
004E0A7F  shl      eax, 4
004E0A82  movups   xmmword ptr [rcx + r15], xmm0
004E0A87  movsxd   rcx, eax
004E0A8A  mov      dword ptr [r10 + r15 + 0xc], esi
004E0A8F  movups   xmm0, xmmword ptr [rip + 0x1b841ea]  ; -> 02064C80
004E0A96  movups   xmmword ptr [rcx + r15], xmm0
004E0A9B  cmp      r11w, si
004E0A9F  je       0x4e0aad  ; -> 004E0AAD
004E0AA1  movzx    eax, word ptr [rip + 0x1b84318]  ; -> 02064DC0
004E0AA8  mov      dword ptr [r10 + r15 + 0xc], eax
004E0AAD  inc      r9w
004E0AB1  mov      word ptr [rip + 0x1b8431f], r9w  ; -> 02064DD8
004E0AB9  cmp      si, di
004E0ABC  jne      0x4e0120  ; -> 004E0120
004E0AC2  movsx    edx, si
004E0AC5  lea      eax, [rdx + 0xa]
004E0AC8  shl      eax, 4
004E0ACB  movsxd   r8, eax
004E0ACE  lea      eax, [rdx + 0xb]
004E0AD1  shl      eax, 4
004E0AD4  movsxd   r9, eax
004E0AD7  lea      eax, [rdx + 0xc]
004E0ADA  shl      eax, 4
004E0ADD  movups   xmm0, xmmword ptr [r8 + r15]
004E0AE2  movsxd   r11, eax
004E0AE5  lea      eax, [rdx + 0xd]
004E0AE8  movups   xmm2, xmmword ptr [r9 + r15]
004E0AED  shl      eax, 4
004E0AF0  movsxd   rsi, eax
004E0AF3  lea      eax, [rdx + 0xe]
004E0AF6  movups   xmm3, xmmword ptr [r11 + r15]
004E0AFB  shl      eax, 4
004E0AFE  movsxd   r14, eax
004E0B01  lea      eax, [rdx + 0xf]
004E0B04  movups   xmm4, xmmword ptr [rsi + r15]
004E0B09  shl      eax, 4
004E0B0C  cvtdq2ps xmm6, xmm0
004E0B0F  movsxd   rbp, eax
004E0B12  lea      eax, [rdx + 0x10]
004E0B15  shl      eax, 4
004E0B18  movsxd   rdi, eax
004E0B1B  lea      eax, [rdx + 0x11]
004E0B1E  shl      eax, 4
004E0B21  movups   xmm0, xmmword ptr [r14 + r15]
004E0B26  movsxd   rbx, eax
004E0B29  lea      eax, [rdx + 0x12]
004E0B2C  movups   xmm5, xmmword ptr [r15 + rbp]
004E0B31  shl      eax, 4
004E0B34  movdqu   xmmword ptr [rip + 0x1b83ff4], xmm6  ; -> 02064B30
004E0B3C  movsxd   r10, eax
004E0B3F  lea      eax, [rdx + 2]
004E0B42  movss    xmm1, dword ptr [rip + 0x1b83fee]  ; -> 02064B38
004E0B4A  cvtdq2ps xmm9, xmm0
004E0B4E  shl      eax, 4
004E0B51  movsxd   rcx, eax
004E0B54  movups   xmm0, xmmword ptr [r10 + r15]
004E0B59  movups   xmm11, xmmword ptr [rcx + r15]
004E0B5E  cvtdq2ps xmm10, xmm0
004E0B62  movss    xmm0, dword ptr [rip + 0x1b83fc6]  ; -> 02064B30
004E0B6A  cvtdq2ps xmm7, xmm2
004E0B6D  movups   xmm2, xmmword ptr [rbx + r15]
004E0B72  movdqu   xmmword ptr [rip + 0x1b83fc6], xmm7  ; -> 02064B40
004E0B7A  cvtdq2ps xmm8, xmm3
004E0B7E  movups   xmm3, xmmword ptr [rdi + r15]
004E0B83  movups   xmmword ptr [rip + 0x1b84035], xmm11  ; -> 02064BC0
004E0B8B  shufps   xmm11, xmm11, 0x55
004E0B90  mulss    xmm0, xmm11
004E0B95  mulss    xmm1, xmm11
004E0B9A  movss    dword ptr [rip + 0x1b83f8e], xmm0  ; -> 02064B30
004E0BA2  movss    xmm0, dword ptr [rip + 0x1b83f92]  ; -> 02064B3C
004E0BAA  mulss    xmm0, xmm11
004E0BAF  movss    dword ptr [rip + 0x1b83f81], xmm1  ; -> 02064B38
004E0BB7  movss    xmm1, dword ptr [rip + 0x1b83f89]  ; -> 02064B48
004E0BBF  movss    dword ptr [rip + 0x1b83f75], xmm0  ; -> 02064B3C
004E0BC7  movss    xmm0, dword ptr [rip + 0x1b83f71]  ; -> 02064B40
004E0BCF  cvtdq2ps xmm4, xmm4
004E0BD2  cvtdq2ps xmm5, xmm5
004E0BD5  cvtdq2ps xmm3, xmm3
004E0BD8  cvtdq2ps xmm2, xmm2
004E0BDB  shufps   xmm6, xmm6, 0x55
004E0BDF  shufps   xmm7, xmm7, 0x55
004E0BE3  mulss    xmm0, xmm11
004E0BE8  mulss    xmm6, xmm11
004E0BED  mulss    xmm7, xmm11
004E0BF2  movss    dword ptr [rip + 0x1b83f46], xmm0  ; -> 02064B40
004E0BFA  movss    dword ptr [rip + 0x1b83f32], xmm6  ; -> 02064B34
004E0C02  movss    dword ptr [rip + 0x1b83f3a], xmm7  ; -> 02064B44
004E0C0A  movdqu   xmmword ptr [rip + 0x1b83f3d], xmm8  ; -> 02064B50
004E0C13  movdqu   xmmword ptr [rip + 0x1b83f45], xmm4  ; -> 02064B60
004E0C1B  movdqu   xmmword ptr [rip + 0x1b83f4c], xmm9  ; -> 02064B70
004E0C24  movdqu   xmmword ptr [rip + 0x1b83f54], xmm5  ; -> 02064B80
004E0C2C  movdqu   xmmword ptr [rip + 0x1b83f5c], xmm3  ; -> 02064B90
004E0C34  movdqu   xmmword ptr [rip + 0x1b83f64], xmm2  ; -> 02064BA0
004E0C3C  movdqu   xmmword ptr [rip + 0x1b83f6b], xmm10  ; -> 02064BB0
004E0C45  mulss    xmm1, xmm11
004E0C4A  movss    xmm0, dword ptr [rip + 0x1b83efa]  ; -> 02064B4C
004E0C52  lea      eax, [rdx + 4]
004E0C55  mulss    xmm0, xmm11
004E0C5A  shl      eax, 4
004E0C5D  movss    dword ptr [rip + 0x1b83ee3], xmm1  ; -> 02064B48
004E0C65  movss    xmm1, dword ptr [rip + 0x1b83eeb]  ; -> 02064B58
004E0C6D  movss    dword ptr [rip + 0x1b83ed7], xmm0  ; -> 02064B4C
004E0C75  movss    xmm0, dword ptr [rip + 0x1b83ed3]  ; -> 02064B50
004E0C7D  mulss    xmm0, xmm11
004E0C82  movsxd   rcx, eax
004E0C85  mulss    xmm1, xmm11
004E0C8A  movss    dword ptr [rip + 0x1b83ebe], xmm0  ; -> 02064B50
004E0C92  movss    xmm0, dword ptr [rip + 0x1b83ec2]  ; -> 02064B5C
004E0C9A  mulss    xmm0, xmm11
004E0C9F  movss    dword ptr [rip + 0x1b83eb1], xmm1  ; -> 02064B58
004E0CA7  movss    xmm1, dword ptr [rip + 0x1b83eb9]  ; -> 02064B68
004E0CAF  movss    dword ptr [rip + 0x1b83ea5], xmm0  ; -> 02064B5C
004E0CB7  movss    xmm0, dword ptr [rip + 0x1b83ea1]  ; -> 02064B60
004E0CBF  mulss    xmm0, xmm11
004E0CC4  mulss    xmm1, xmm11
004E0CC9  movss    dword ptr [rip + 0x1b83e8f], xmm0  ; -> 02064B60
004E0CD1  movss    xmm0, dword ptr [rip + 0x1b83e93]  ; -> 02064B6C
004E0CD9  mulss    xmm0, xmm11
004E0CDE  movss    dword ptr [rip + 0x1b83e82], xmm1  ; -> 02064B68
004E0CE6  movss    xmm1, dword ptr [rip + 0x1b83e8a]  ; -> 02064B78
004E0CEE  movss    dword ptr [rip + 0x1b83e76], xmm0  ; -> 02064B6C
004E0CF6  movups   xmm0, xmmword ptr [rcx + r15]
004E0CFB  mulss    xmm1, xmm11
004E0D00  movups   xmmword ptr [rip + 0x1b83ef9], xmm0  ; -> 02064C00
004E0D07  movss    xmm0, dword ptr [rip + 0x1b83e61]  ; -> 02064B70
004E0D0F  mulss    xmm0, xmm11
004E0D14  movss    dword ptr [rip + 0x1b83e5c], xmm1  ; -> 02064B78
004E0D1C  movss    xmm1, dword ptr [rip + 0x1b83e64]  ; -> 02064B88
004E0D24  movss    dword ptr [rip + 0x1b83e44], xmm0  ; -> 02064B70
004E0D2C  movss    xmm0, dword ptr [rip + 0x1b83e48]  ; -> 02064B7C
004E0D34  mulss    xmm0, xmm11
004E0D39  mulss    xmm1, xmm11
004E0D3E  movss    dword ptr [rip + 0x1b83e36], xmm0  ; -> 02064B7C
004E0D46  movups   xmm0, xmmword ptr [rip + 0x1b83de3]  ; -> 02064B30
004E0D4D  movss    dword ptr [rip + 0x1b83e33], xmm1  ; -> 02064B88
004E0D55  movss    xmm1, dword ptr [rip + 0x1b83e3b]  ; -> 02064B98
004E0D5D  movups   xmmword ptr [r8 + r15], xmm0
004E0D62  movss    xmm0, dword ptr [rip + 0x1b83e16]  ; -> 02064B80
004E0D6A  mulss    xmm0, xmm11
004E0D6F  shufps   xmm8, xmm8, 0x55
004E0D74  mulss    xmm8, xmm11
004E0D79  movss    dword ptr [rip + 0x1b83dff], xmm0  ; -> 02064B80
004E0D81  movss    xmm0, dword ptr [rip + 0x1b83e03]  ; -> 02064B8C
004E0D89  mulss    xmm0, xmm11
004E0D8E  movss    dword ptr [rip + 0x1b83dbd], xmm8  ; -> 02064B54
004E0D97  shufps   xmm4, xmm4, 0x55
004E0D9B  movss    dword ptr [rip + 0x1b83de9], xmm0  ; -> 02064B8C
004E0DA3  movups   xmm0, xmmword ptr [rip + 0x1b83d96]  ; -> 02064B40
004E0DAA  shufps   xmm9, xmm9, 0x55
004E0DAF  movups   xmmword ptr [r9 + r15], xmm0
004E0DB4  movss    xmm0, dword ptr [rip + 0x1b83dd4]  ; -> 02064B90
004E0DBC  mulss    xmm0, xmm11
004E0DC1  shufps   xmm5, xmm5, 0x55
004E0DC5  shufps   xmm3, xmm3, 0x55
004E0DC9  movss    dword ptr [rip + 0x1b83dbf], xmm0  ; -> 02064B90
004E0DD1  movss    xmm0, dword ptr [rip + 0x1b83dc3]  ; -> 02064B9C
004E0DD9  mulss    xmm0, xmm11
004E0DDE  shufps   xmm2, xmm2, 0x55
004E0DE2  mulss    xmm4, xmm11
004E0DE7  movss    dword ptr [rip + 0x1b83dad], xmm0  ; -> 02064B9C
004E0DEF  movups   xmm0, xmmword ptr [rip + 0x1b83d5a]  ; -> 02064B50
004E0DF6  mulss    xmm9, xmm11
004E0DFB  movups   xmmword ptr [r11 + r15], xmm0
004E0E00  movss    xmm0, dword ptr [rip + 0x1b83d98]  ; -> 02064BA0
004E0E08  mulss    xmm0, xmm11
004E0E0D  mulss    xmm5, xmm11
004E0E12  mulss    xmm3, xmm11
004E0E17  mulss    xmm1, xmm11
004E0E1C  mulss    xmm2, xmm11
004E0E21  movss    dword ptr [rip + 0x1b83d77], xmm0  ; -> 02064BA0
004E0E29  movss    dword ptr [rip + 0x1b83d33], xmm4  ; -> 02064B64
004E0E31  movss    dword ptr [rip + 0x1b83d3a], xmm9  ; -> 02064B74
004E0E3A  movss    dword ptr [rip + 0x1b83d42], xmm5  ; -> 02064B84
004E0E42  movss    dword ptr [rip + 0x1b83d4a], xmm3  ; -> 02064B94
004E0E4A  movss    dword ptr [rip + 0x1b83d46], xmm1  ; -> 02064B98
004E0E52  movss    dword ptr [rip + 0x1b83d4a], xmm2  ; -> 02064BA4
004E0E5A  movss    xmm0, dword ptr [rip + 0x1b83d4a]  ; -> 02064BAC
004E0E62  lea      r11, [rsp + 0xc0]
004E0E6A  movss    xmm1, dword ptr [rip + 0x1b83d36]  ; -> 02064BA8
004E0E72  movaps   xmm6, xmmword ptr [r11 - 0x10]
004E0E77  movaps   xmm7, xmmword ptr [r11 - 0x20]
004E0E7C  movaps   xmm8, xmmword ptr [r11 - 0x30]
004E0E81  movaps   xmm9, xmmword ptr [r11 - 0x40]
004E0E86  movaps   xmm12, xmmword ptr [r11 - 0x70]
004E0E8B  movaps   xmm13, xmmword ptr [r11 - 0x80]
004E0E90  movaps   xmm14, xmmword ptr [rsp + 0x30]
004E0E96  movaps   xmm15, xmmword ptr [rsp + 0x20]
004E0E9C  mulss    xmm0, xmm11
004E0EA1  mulss    xmm1, xmm11
004E0EA6  movss    dword ptr [rip + 0x1b83cfe], xmm0  ; -> 02064BAC
004E0EAE  movups   xmm0, xmmword ptr [rip + 0x1b83cab]  ; -> 02064B60
004E0EB5  movss    dword ptr [rip + 0x1b83ceb], xmm1  ; -> 02064BA8
004E0EBD  movss    xmm1, dword ptr [rip + 0x1b83cf3]  ; -> 02064BB8
004E0EC5  movups   xmmword ptr [rsi + r15], xmm0
004E0ECA  movss    xmm0, dword ptr [rip + 0x1b83cde]  ; -> 02064BB0
004E0ED2  mulss    xmm0, xmm11
004E0ED7  mulss    xmm1, xmm11
004E0EDC  movss    dword ptr [rip + 0x1b83ccc], xmm0  ; -> 02064BB0
004E0EE4  movss    xmm0, dword ptr [rip + 0x1b83cd0]  ; -> 02064BBC
004E0EEC  mulss    xmm0, xmm11
004E0EF1  movss    dword ptr [rip + 0x1b83cbf], xmm1  ; -> 02064BB8
004E0EF9  movups   xmm1, xmmword ptr [rip + 0x1b83c80]  ; -> 02064B80
004E0F00  movss    dword ptr [rip + 0x1b83cb4], xmm0  ; -> 02064BBC
004E0F08  movups   xmm0, xmmword ptr [rip + 0x1b83c61]  ; -> 02064B70
004E0F0F  shufps   xmm10, xmm10, 0x55
004E0F14  movups   xmmword ptr [r14 + r15], xmm0
004E0F19  movups   xmm0, xmmword ptr [rip + 0x1b83c70]  ; -> 02064B90
004E0F20  movups   xmmword ptr [r15 + rbp], xmm1
004E0F25  movups   xmm1, xmmword ptr [rip + 0x1b83c74]  ; -> 02064BA0
004E0F2C  mulss    xmm10, xmm11
004E0F31  movaps   xmm11, xmmword ptr [r11 - 0x60]
004E0F36  movups   xmmword ptr [rdi + r15], xmm0
004E0F3B  movss    dword ptr [rip + 0x1b83c70], xmm10  ; -> 02064BB4
004E0F44  movups   xmm0, xmmword ptr [rip + 0x1b83c65]  ; -> 02064BB0
004E0F4B  movaps   xmm10, xmmword ptr [r11 - 0x50]
004E0F50  movups   xmmword ptr [rbx + r15], xmm1
004E0F55  mov      rbx, qword ptr [r11 + 0x40]
004E0F59  movups   xmmword ptr [r10 + r15], xmm0
004E0F5E  mov      rsp, r11
004E0F61  pop      r15
004E0F63  pop      r14
004E0F65  pop      r13
004E0F67  pop      r12
004E0F69  pop      rdi
004E0F6A  pop      rsi
004E0F6B  pop      rbp
004E0F6C  ret      
```

## 004EBE80 (2769 B, extent 004EBE80-004EC951)

Page context: "00') at '+0x1C'/'+0x20'/'+0x24' - a module record's field init.  Interior anchor '004DB06E' (function '004DB060').  '004EC960' (515 B) is a battery constructor '0037E0F0' calls: '008631E0' registers '004EBE80', '008631D0(0x11)' fills '+0x10', then '+0xC' = 0x02000000, '+0x18' = 0x1000404, '+0x1C' = 0x6C0E0000 head the constant fill - a module record's init.  Interior anchor '004EC973' (function '004EC960').  '004C8080' (509 B) is a batt"

```
004EBE80  mov      rax, rsp
004EBE83  mov      qword ptr [rax + 8], rbx
004EBE87  mov      qword ptr [rax + 0x10], rsi
004EBE8B  push     rdi
004EBE8C  sub      rsp, 0x90
004EBE93  movaps   xmmword ptr [rax - 0x18], xmm6
004EBE97  lea      rsi, [rip + 0x1b78f92]  ; -> 02064E30
004EBE9E  movaps   xmmword ptr [rax - 0x28], xmm7
004EBEA2  mov      rdi, rcx
004EBEA5  movaps   xmmword ptr [rax - 0x38], xmm8
004EBEAA  xor      r8d, r8d
004EBEAD  movaps   xmmword ptr [rax - 0x48], xmm9
004EBEB2  mov      rbx, rdx
004EBEB5  movaps   xmmword ptr [rax - 0x58], xmm10
004EBEBA  movaps   xmmword ptr [rax - 0x68], xmm11
004EBEBF  movzx    eax, word ptr [rip + 0x1b78c46]  ; -> 02064B0C
004EBEC6  add      ax, 9
004EBECA  mov      word ptr [rip + 0x1b78f03], ax  ; -> 02064DD4
004EBED1  cwde     
004EBED2  shl      eax, 4
004EBED5  movsxd   rcx, eax
004EBED8  add      rcx, rsi
004EBEDB  call     rdi
004EBEDD  movsx    r8d, word ptr [rip + 0x1b78c27]  ; -> 02064B0C
004EBEE5  mov      word ptr [rip + 0x1b78ecb], r8w  ; -> 02064DB8
004EBEED  mov      word ptr [rip + 0x1b78edb], r8w  ; -> 02064DD0
004EBEF5  lea      eax, [r8 + 2]
004EBEF9  shl      eax, 4
004EBEFC  movsxd   rcx, eax
004EBEFF  lea      eax, [r8 + 3]
004EBF03  shl      eax, 4
004EBF06  movups   xmm5, xmmword ptr [rcx + rsi]
004EBF0A  movsxd   rcx, eax
004EBF0D  lea      eax, [r8 + 4]
004EBF11  shl      eax, 4
004EBF14  movups   xmmword ptr [rip + 0x1b78c15], xmm5  ; -> 02064B30
004EBF1B  movups   xmm6, xmmword ptr [rcx + rsi]
004EBF1F  movsxd   rcx, eax
004EBF22  lea      eax, [r8 + 5]
004EBF26  shl      eax, 4
004EBF29  movups   xmmword ptr [rip + 0x1b78c10], xmm6  ; -> 02064B40
004EBF30  movups   xmm3, xmmword ptr [rcx + rsi]
004EBF34  movsxd   rcx, eax
004EBF37  lea      eax, [r8 + 6]
004EBF3B  shl      eax, 4
004EBF3E  movups   xmmword ptr [rip + 0x1b78c0b], xmm3  ; -> 02064B50
004EBF45  movups   xmm0, xmmword ptr [rcx + rsi]
004EBF49  movsxd   rcx, eax
004EBF4C  lea      eax, [r8 + 7]
004EBF50  shl      eax, 4
004EBF53  movups   xmmword ptr [rip + 0x1b78c06], xmm0  ; -> 02064B60
004EBF5A  movups   xmm1, xmmword ptr [rcx + rsi]
004EBF5E  movsxd   rcx, eax
004EBF61  lea      eax, [r8 + 8]
004EBF65  shl      eax, 4
004EBF68  movups   xmmword ptr [rip + 0x1b78c01], xmm1  ; -> 02064B70
004EBF6F  movups   xmm2, xmmword ptr [rcx + rsi]
004EBF73  movsxd   rcx, eax
004EBF76  lea      eax, [r8 + 1]
004EBF7A  shl      eax, 4
004EBF7D  shufps   xmm1, xmm1, 0xff
004EBF81  movss    dword ptr [rsp + 0x2c], xmm1
004EBF87  movups   xmm4, xmmword ptr [rcx + rsi]
004EBF8B  movsxd   rcx, eax
004EBF8E  movd     xmm1, dword ptr [rsp + 0x2c]
004EBF94  cvtdq2ps xmm1, xmm1
004EBF97  movzx    eax, word ptr [rcx + rsi]
004EBF9B  mov      word ptr [rip + 0x1b78e1a], ax  ; -> 02064DBC
004EBFA2  movzx    eax, word ptr [rcx + rsi + 8]
004EBFA7  mov      word ptr [rip + 0x1b78e12], ax  ; -> 02064DC0
004EBFAE  lea      eax, [r8 + 0x14]
004EBFB2  mov      word ptr [rip + 0x1b78e0f], ax  ; -> 02064DC8
004EBFB9  mov      eax, 0x190
004EBFBE  add      eax, r8d
004EBFC1  shufps   xmm3, xmm3, 0xaa
004EBFC5  mov      word ptr [rip + 0x1b78de4], ax  ; -> 02064DB0
004EBFCC  movaps   xmm0, xmm3
004EBFCF  inc      ax
004EBFD2  mulss    xmm0, xmm1
004EBFD6  mov      word ptr [rip + 0x1b78dd7], ax  ; -> 02064DB4
004EBFDD  movups   xmmword ptr [rip + 0x1b78b9c], xmm2  ; -> 02064B80
004EBFE4  cvttss2si eax, xmm0
004EBFE8  shufps   xmm2, xmm2, 0xff
004EBFEC  mov      dword ptr [rip + 0x1b78b8a], eax  ; -> 02064B7C
004EBFF2  movss    dword ptr [rsp + 0x2c], xmm2
004EBFF8  movups   xmmword ptr [rip + 0x1b78b91], xmm4  ; -> 02064B90
004EBFFF  movss    xmm0, dword ptr [rip + 0x1b78b2d]  ; -> 02064B34
004EC007  xorps    xmm7, xmm7
004EC00A  movd     xmm1, dword ptr [rsp + 0x2c]
004EC010  cvtdq2ps xmm1, xmm1
004EC013  mulss    xmm1, xmm3
004EC017  movaps   xmm3, xmm6
004EC01A  shufps   xmm3, xmm6, 0xaa
004EC01E  shufps   xmm6, xmm6, 0xff
004EC022  subss    xmm5, xmm3
004EC026  subss    xmm0, xmm6
004EC02A  cvttss2si eax, xmm1
004EC02E  movaps   xmm1, xmm4
004EC031  addss    xmm3, xmm3
004EC035  addss    xmm6, xmm6
004EC039  movss    dword ptr [rip + 0x1b78aef], xmm5  ; -> 02064B30
004EC041  shufps   xmm1, xmm4, 0xff
004EC045  movss    dword ptr [rip + 0x1b78ae7], xmm0  ; -> 02064B34
004EC04D  movaps   xmm0, xmm4
004EC050  shufps   xmm0, xmm4, 0xaa
004EC054  ucomiss  xmm3, xmm7
004EC057  mov      dword ptr [rip + 0x1b78b2f], eax  ; -> 02064B8C
004EC05D  subss    xmm0, xmm4
004EC061  movss    dword ptr [rip + 0x1b78b4f], xmm3  ; -> 02064BB8
004EC069  shufps   xmm4, xmm4, 0x55
004EC06D  subss    xmm1, xmm4
004EC071  movss    dword ptr [rip + 0x1b78b43], xmm6  ; -> 02064BBC
004EC079  movss    xmm4, dword ptr [rip + 0x19167bb]  ; -> 01E0283C [f32 1]
004EC081  movss    dword ptr [rip + 0x1b78b1f], xmm0  ; -> 02064BA8
004EC089  movss    dword ptr [rip + 0x1b78b1b], xmm1  ; -> 02064BAC
004EC091  movss    xmm1, dword ptr [rip + 0x4142c7]  ; -> 00900360 [u32 0x7F7FFFFF]
004EC099  jp       0x4ec0a2  ; -> 004EC0A2
004EC09B  jne      0x4ec0a2  ; -> 004EC0A2
004EC09D  movaps   xmm2, xmm1
004EC0A0  jmp      0x4ec0a9  ; -> 004EC0A9
004EC0A2  movaps   xmm2, xmm4
004EC0A5  divss    xmm2, xmm3
004EC0A9  ucomiss  xmm6, xmm7
004EC0AC  movss    xmm3, dword ptr [rip + 0x191677c]  ; -> 01E02830 [u32 0x00000000]
004EC0B4  movaps   xmm0, xmm3
004EC0B7  addss    xmm0, xmm2
004EC0BB  movss    dword ptr [rip + 0x1b78aed], xmm0  ; -> 02064BB0
004EC0C3  jp       0x4ec0c7  ; -> 004EC0C7
004EC0C5  je       0x4ec0ce  ; -> 004EC0CE
004EC0C7  movaps   xmm1, xmm4
004EC0CA  divss    xmm1, xmm6
004EC0CE  movss    xmm2, dword ptr [rip + 0x191675e]  ; -> 01E02834 [u32 0x00000000]
004EC0D6  addss    xmm2, xmm1
004EC0DA  movss    dword ptr [rip + 0x1b78a1e], xmm1  ; -> 02064B00
004EC0E2  ucomiss  xmm2, xmm7
004EC0E5  movss    dword ptr [rip + 0x1b78ac7], xmm2  ; -> 02064BB4
004EC0ED  jp       0x4ec106  ; -> 004EC106
004EC0EF  jne      0x4ec106  ; -> 004EC106
004EC0F1  call     0x22cc40  ; -> 0022CC40 fn
004EC0F6  movss    xmm3, dword ptr [rip + 0x1916732]  ; -> 01E02830 [u32 0x00000000]
004EC0FE  movss    xmm2, dword ptr [rip + 0x1b78aae]  ; -> 02064BB4
004EC106  comiss   xmm7, xmm2
004EC109  jbe      0x4ec120  ; -> 004EC120
004EC10B  call     0x22cc30  ; -> 0022CC30 fn
004EC110  movss    xmm3, dword ptr [rip + 0x1916718]  ; -> 01E02830 [u32 0x00000000]
004EC118  movss    xmm2, dword ptr [rip + 0x1b78a94]  ; -> 02064BB4
004EC120  movss    xmm0, dword ptr [rip + 0x191670c]  ; -> 01E02834 [u32 0x00000000]
004EC128  movaps   xmm1, xmm3
004EC12B  addss    xmm1, dword ptr [rip + 0x1b78a75]  ; -> 02064BA8
004EC133  addss    xmm0, dword ptr [rip + 0x1b78a71]  ; -> 02064BAC
004EC13B  addss    xmm3, dword ptr [rip + 0x1b78a25]  ; -> 02064B68
004EC143  mulss    xmm1, dword ptr [rip + 0x1b78a65]  ; -> 02064BB0
004EC14B  mulss    xmm0, xmm2
004EC14F  movss    dword ptr [rip + 0x1b78a49], xmm1  ; -> 02064BA0
004EC157  movss    dword ptr [rip + 0x1b78b51], xmm3  ; -> 02064CB0
004EC15F  movss    dword ptr [rip + 0x1b78a3d], xmm0  ; -> 02064BA4
004EC167  call     0x5375f0  ; -> 005375F0 fn
004EC16C  call     0x5376d0  ; -> 005376D0 fn
004EC171  movss    xmm3, dword ptr [rip + 0x19166b7]  ; -> 01E02830 [u32 0x00000000]
004EC179  movss    xmm1, dword ptr [rip + 0x19166b3]  ; -> 01E02834 [u32 0x00000000]
004EC181  movaps   xmm0, xmm3
004EC184  addss    xmm0, dword ptr [rip + 0x1b78b38]  ; -> 02064CC4
004EC18C  addss    xmm1, dword ptr [rip + 0x1b78b2c]  ; -> 02064CC0
004EC194  subss    xmm3, dword ptr [rip + 0x1b78b24]  ; -> 02064CC0
004EC19C  movss    dword ptr [rip + 0x1b78b5c], xmm0  ; -> 02064D00
004EC1A4  movss    dword ptr [rip + 0x1b78b58], xmm1  ; -> 02064D04
004EC1AC  movss    dword ptr [rip + 0x1b78b5c], xmm3  ; -> 02064D10
004EC1B4  call     0x22cc20  ; -> 0022CC20 fn
004EC1B9  movss    xmm8, dword ptr [rip + 0x191667a]  ; -> 01E0283C [f32 1]
004EC1C2  mov      ecx, 1
004EC1C7  movss    xmm0, dword ptr [rip + 0x1916669]  ; -> 01E02838 [u32 0x00000000]
004EC1CF  movss    xmm4, dword ptr [rip + 0x191665d]  ; -> 01E02834 [u32 0x00000000]
004EC1D7  movss    xmm9, dword ptr [rip + 0x1916650]  ; -> 01E02830 [u32 0x00000000]
004EC1E0  movaps   xmm5, xmm4
004EC1E3  addss    xmm5, dword ptr [rip + 0x1b78ad9]  ; -> 02064CC4
004EC1EB  movss    xmm1, dword ptr [rip + 0x1b78b0d]  ; -> 02064D00
004EC1F3  movaps   xmm3, xmm9
004EC1F7  movss    xmm2, dword ptr [rip + 0x1b78b05]  ; -> 02064D04
004EC1FF  addss    xmm3, xmm8
004EC204  movss    xmm6, dword ptr [rip + 0x17ff99c]  ; -> 01CEBBA8 [f32 1]
004EC20C  movss    xmm10, dword ptr [rip + 0x415927]  ; -> 00901B3C [f32 1.5]
004EC215  movss    xmm7, dword ptr [rip + 0x17ff9eb]  ; -> 01CEBC08 [f32 2]
004EC21D  movss    xmm11, dword ptr [rip + 0x17ff94a]  ; -> 01CEBB70 [f32 0.5]
004EC226  movzx    r8d, word ptr [rip + 0x1b788de]  ; -> 02064B0C
004EC22E  movzx    eax, word ptr [rip + 0x1b78b8b]  ; -> 02064DC0
004EC235  mulss    xmm0, xmm8
004EC23A  mov      dword ptr [rip + 0x1b788bc], ecx  ; -> 02064AFC
004EC240  mulss    xmm4, xmm8
004EC245  movss    dword ptr [rip + 0x1b78aab], xmm0  ; -> 02064CF8
004EC24D  movss    xmm0, dword ptr [rip + 0x1b78abb]  ; -> 02064D10
004EC255  mulss    xmm0, xmm4
004EC259  mulss    xmm1, xmm3
004EC25D  movss    dword ptr [rip + 0x1b78aaf], xmm5  ; -> 02064D14
004EC265  mulss    xmm2, xmm3
004EC269  addss    xmm0, xmm1
004EC26D  mulss    xmm5, xmm4
004EC271  movss    dword ptr [rip + 0x1b788a7], xmm1  ; -> 02064B20
004EC279  movss    dword ptr [rip + 0x1b788a3], xmm2  ; -> 02064B24
004EC281  addss    xmm5, xmm2
004EC285  movss    dword ptr [rip + 0x1b78a63], xmm0  ; -> 02064CF0
004EC28D  movss    xmm0, dword ptr [rip + 0x1b788c7]  ; -> 02064B5C
004EC295  movss    dword ptr [rip + 0x191658b], xmm0  ; -> 01E02828 [f32 1]
004EC29D  movss    dword ptr [rip + 0x1b78a4f], xmm5  ; -> 02064CF4
004EC2A5  nop      word ptr [rax + rax]
004EC2B0  dec      ax
004EC2B3  mov      word ptr [rip + 0x1b78b06], ax  ; -> 02064DC0
004EC2BA  test     ecx, ecx
004EC2BC  je       0x4ec499  ; -> 004EC499
004EC2C2  mov      eax, dword ptr [rip + 0x1916560]  ; -> 01E02828 [f32 1]
004EC2C8  mov      ecx, eax
004EC2CA  shr      ecx, 0x12
004EC2CD  xor      ecx, eax
004EC2CF  and      eax, 0x3fffff
004EC2D4  shr      ecx, 4
004EC2D7  or       eax, 0x1fc00000
004EC2DC  and      ecx, 1
004EC2DF  add      eax, eax
004EC2E1  or       ecx, eax
004EC2E3  mov      eax, ecx
004EC2E5  shr      eax, 0x12
004EC2E8  xor      eax, ecx
004EC2EA  and      ecx, 0x3fffff
004EC2F0  or       ecx, 0x1fc00000
004EC2F6  shr      eax, 4
004EC2F9  add      ecx, ecx
004EC2FB  and      eax, 1
004EC2FE  or       eax, ecx
004EC300  mov      ecx, eax
004EC302  shr      ecx, 0x12
004EC305  xor      ecx, eax
004EC307  and      eax, 0x3fffff
004EC30C  shr      ecx, 4
004EC30F  or       eax, 0x1fc00000
004EC314  and      ecx, 1
004EC317  add      eax, eax
004EC319  or       ecx, eax
004EC31B  mov      eax, ecx
004EC31D  shr      eax, 0x12
004EC320  xor      eax, ecx
004EC322  and      ecx, 0x3fffff
004EC328  or       ecx, 0x1fc00000
004EC32E  shr      eax, 4
004EC331  add      ecx, ecx
004EC333  and      eax, 1
004EC336  or       eax, ecx
004EC338  mov      ecx, eax
004EC33A  shr      ecx, 0x12
004EC33D  xor      ecx, eax
004EC33F  and      eax, 0x3fffff
004EC344  shr      ecx, 4
004EC347  or       eax, 0x1fc00000
004EC34C  and      ecx, 1
004EC34F  add      eax, eax
004EC351  or       ecx, eax
004EC353  mov      eax, ecx
004EC355  mov      dword ptr [rip + 0x19164cd], ecx  ; -> 01E02828 [f32 1]
004EC35B  movss    xmm2, dword ptr [rip + 0x19164c5]  ; -> 01E02828 [f32 1]
004EC363  shr      eax, 0x12
004EC366  xor      eax, ecx
004EC368  and      ecx, 0x3fffff
004EC36E  or       ecx, 0x1fc00000
004EC374  shr      eax, 4
004EC377  add      ecx, ecx
004EC379  and      eax, 1
004EC37C  or       eax, ecx
004EC37E  mov      ecx, eax
004EC380  shr      ecx, 0x12
004EC383  xor      ecx, eax
004EC385  and      eax, 0x3fffff
004EC38A  shr      ecx, 4
004EC38D  or       eax, 0x1fc00000
004EC392  and      ecx, 1
004EC395  add      eax, eax
004EC397  or       ecx, eax
004EC399  mov      eax, ecx
004EC39B  shr      eax, 0x12
004EC39E  xor      eax, ecx
004EC3A0  and      ecx, 0x3fffff
004EC3A6  or       ecx, 0x1fc00000
004EC3AC  shr      eax, 4
004EC3AF  add      ecx, ecx
004EC3B1  and      eax, 1
004EC3B4  or       eax, ecx
004EC3B6  mov      ecx, eax
004EC3B8  shr      ecx, 0x12
004EC3BB  xor      ecx, eax
004EC3BD  shr      ecx, 4
004EC3C0  and      ecx, 1
004EC3C3  and      eax, 0x3fffff
004EC3C8  or       eax, 0x1fc00000
004EC3CD  add      eax, eax
004EC3CF  or       ecx, eax
004EC3D1  mov      edx, ecx
004EC3D3  shr      edx, 0x12
004EC3D6  xor      edx, ecx
004EC3D8  and      ecx, 0x3fffff
004EC3DE  or       ecx, 0x1fc00000
004EC3E4  shr      edx, 4
004EC3E7  add      ecx, ecx
004EC3E9  and      edx, 1
004EC3EC  or       edx, ecx
004EC3EE  mov      dword ptr [rip + 0x1916434], edx  ; -> 01E02828 [f32 1]
004EC3F4  mov      eax, edx
004EC3F6  movss    xmm0, dword ptr [rip + 0x191642a]  ; -> 01E02828 [f32 1]
004EC3FE  shr      eax, 0x12
004EC401  xor      eax, edx
004EC403  and      edx, 0x3fffff
004EC409  shr      eax, 4
004EC40C  or       edx, 0x1fc00000
004EC412  and      eax, 1
004EC415  add      edx, edx
004EC417  or       eax, edx
004EC419  mov      ecx, eax
004EC41B  shr      ecx, 0x12
004EC41E  xor      ecx, eax
004EC420  and      eax, 0x3fffff
004EC425  or       eax, 0x1fc00000
004EC42A  shr      ecx, 4
004EC42D  add      eax, eax
004EC42F  and      ecx, 1
004EC432  or       ecx, eax
004EC434  mov      eax, ecx
004EC436  shr      eax, 0x12
004EC439  xor      eax, ecx
004EC43B  and      ecx, 0x3fffff
004EC441  or       ecx, 0x1fc00000
004EC447  shr      eax, 4
004EC44A  add      ecx, ecx
004EC44C  and      eax, 1
004EC44F  or       eax, ecx
004EC451  mov      ecx, eax
004EC453  shr      ecx, 0x12
004EC456  xor      ecx, eax
004EC458  and      eax, 0x3fffff
004EC45D  or       eax, 0x1fc00000
004EC462  shr      ecx, 4
004EC465  add      eax, eax
004EC467  and      ecx, 1
004EC46A  or       ecx, eax
004EC46C  mov      eax, ecx
004EC46E  shr      eax, 0x12
004EC471  xor      eax, ecx
004EC473  and      ecx, 0x3fffff
004EC479  or       ecx, 0x1fc00000
004EC47F  shr      eax, 4
004EC482  add      ecx, ecx
004EC484  and      eax, 1
004EC487  or       eax, ecx
004EC489  mov      dword ptr [rip + 0x1916399], eax  ; -> 01E02828 [f32 1]
004EC48F  movss    xmm1, dword ptr [rip + 0x1916391]  ; -> 01E02828 [f32 1]
004EC497  jmp      0x4ec4a2  ; -> 004EC4A2
004EC499  movaps   xmm2, xmm6
004EC49C  movaps   xmm0, xmm6
004EC49F  movaps   xmm1, xmm6
004EC4A2  movss    xmm3, dword ptr [rip + 0x1b78696]  ; -> 02064B40
004EC4AA  subss    xmm1, xmm8
004EC4AF  subss    xmm0, xmm10
004EC4B4  movsx    eax, r8w
004EC4B8  subss    xmm2, xmm10
004EC4BD  mov      dword ptr [rip + 0x1b7863d], 0x3f000000  ; -> 02064B04
004EC4C7  inc      eax
004EC4C9  shl      eax, 4
004EC4CC  movss    dword ptr [rip + 0x1b787e4], xmm1  ; -> 02064CB8
004EC4D4  mulss    xmm1, dword ptr [rip + 0x1b78678]  ; -> 02064B54
004EC4DC  addss    xmm0, xmm0
004EC4E0  cdqe     
004EC4E2  mulss    xmm2, xmm7
004EC4E6  addss    xmm1, dword ptr [rip + 0x1b78662]  ; -> 02064B50
004EC4EE  movzx    eax, word ptr [rax + rsi + 4]
004EC4F3  mulss    xmm3, xmm2
004EC4F7  dec      ax
004EC4FA  mov      word ptr [rip + 0x1b788c3], ax  ; -> 02064DC4
004EC501  movss    dword ptr [rip + 0x1b787ab], xmm0  ; -> 02064CB4
004EC509  mulss    xmm1, xmm11
004EC50E  movss    dword ptr [rip + 0x1b7879a], xmm2  ; -> 02064CB0
004EC516  movss    xmm2, dword ptr [rip + 0x1b78626]  ; -> 02064B44
004EC51E  mulss    xmm2, xmm0
004EC522  movaps   xmm0, xmm1
004EC525  addss    xmm0, xmm3
004EC529  movss    dword ptr [rip + 0x1b78757], xmm1  ; -> 02064C88
004EC531  movss    dword ptr [rip + 0x1b78747], xmm3  ; -> 02064C80
004EC539  subss    xmm3, xmm1
004EC53D  movss    xmm1, dword ptr [rip + 0x1b78757]  ; -> 02064C9C
004EC545  movss    dword ptr [rip + 0x1b78737], xmm2  ; -> 02064C84
004EC54D  addss    xmm2, xmm9
004EC552  movss    dword ptr [rip + 0x1b786a2], xmm1  ; -> 02064BFC
004EC55A  movss    xmm1, dword ptr [rip + 0x1b7874a]  ; -> 02064CAC
004EC562  movss    dword ptr [rip + 0x1b78726], xmm0  ; -> 02064C90
004EC56A  movss    dword ptr [rip + 0x1b7867e], xmm0  ; -> 02064BF0
004EC572  movss    xmm0, dword ptr [rip + 0x1b7871e]  ; -> 02064C98
004EC57A  movss    dword ptr [rip + 0x1b78676], xmm0  ; -> 02064BF8
004EC582  movss    xmm0, dword ptr [rip + 0x1b7871e]  ; -> 02064CA8
004EC58A  movss    dword ptr [rip + 0x1b78676], xmm0  ; -> 02064C08
004EC592  movss    dword ptr [rip + 0x1b786fa], xmm2  ; -> 02064C94
004EC59A  movss    dword ptr [rip + 0x1b786fe], xmm3  ; -> 02064CA0
004EC5A2  movss    dword ptr [rip + 0x1b786fa], xmm2  ; -> 02064CA4
004EC5AA  movss    dword ptr [rip + 0x1b78642], xmm2  ; -> 02064BF4
004EC5B2  movss    dword ptr [rip + 0x1b78646], xmm3  ; -> 02064C00
004EC5BA  movss    dword ptr [rip + 0x1b78642], xmm2  ; -> 02064C04
004EC5C2  movss    dword ptr [rip + 0x1b78642], xmm1  ; -> 02064C0C
004EC5CA  call     0x4eb910  ; -> 004EB910 fn
004EC5CF  movzx    eax, word ptr [rip + 0x1b787ee]  ; -> 02064DC4
004EC5D6  movzx    r8d, word ptr [rip + 0x1b7852e]  ; -> 02064B0C
004EC5DE  mov      dword ptr [rip + 0x1b7851c], 0x3f800000  ; -> 02064B04
004EC5E8  cmp      ax, r8w
004EC5EC  je       0x4ec8b2  ; -> 004EC8B2
004EC5F2  movss    xmm0, dword ptr [rip + 0x1b78696]  ; -> 02064C90
004EC5FA  dec      ax
004EC5FD  movss    xmm1, dword ptr [rip + 0x1b78693]  ; -> 02064C98
004EC605  movss    dword ptr [rip + 0x1b785e3], xmm0  ; -> 02064BF0
004EC60D  movss    xmm0, dword ptr [rip + 0x1b78687]  ; -> 02064C9C
004EC615  movss    dword ptr [rip + 0x1b785db], xmm1  ; -> 02064BF8
004EC61D  movss    xmm1, dword ptr [rip + 0x1b7867b]  ; -> 02064CA0
004EC625  movss    dword ptr [rip + 0x1b785cf], xmm0  ; -> 02064BFC
004EC62D  movss    xmm0, dword ptr [rip + 0x1b78673]  ; -> 02064CA8
004EC635  movss    dword ptr [rip + 0x1b785c3], xmm1  ; -> 02064C00
004EC63D  movss    xmm1, dword ptr [rip + 0x1b78667]  ; -> 02064CAC
004EC645  movss    dword ptr [rip + 0x1b785bb], xmm0  ; -> 02064C08
004EC64D  movss    xmm0, dword ptr [rip + 0x1b7863f]  ; -> 02064C94
004EC655  movss    dword ptr [rip + 0x1b785af], xmm1  ; -> 02064C0C
004EC65D  addss    xmm0, xmm6
004EC661  movss    xmm1, dword ptr [rip + 0x1b7863b]  ; -> 02064CA4
004EC669  addss    xmm1, xmm6
004EC66D  mov      word ptr [rip + 0x1b78750], ax  ; -> 02064DC4
004EC674  movss    dword ptr [rip + 0x1b78578], xmm0  ; -> 02064BF4
004EC67C  movss    dword ptr [rip + 0x1b78580], xmm1  ; -> 02064C04
004EC684  call     0x4eb910  ; -> 004EB910 fn
004EC689  movzx    eax, word ptr [rip + 0x1b78734]  ; -> 02064DC4
004EC690  movzx    r8d, word ptr [rip + 0x1b78474]  ; -> 02064B0C
004EC698  mov      dword ptr [rip + 0x1b78462], 0xbf800000  ; -> 02064B04
004EC6A2  cmp      ax, r8w
004EC6A6  je       0x4ec8b2  ; -> 004EC8B2
004EC6AC  movss    xmm0, dword ptr [rip + 0x1b785dc]  ; -> 02064C90
004EC6B4  dec      ax
004EC6B7  movss    xmm1, dword ptr [rip + 0x1b785d9]  ; -> 02064C98
004EC6BF  movss    dword ptr [rip + 0x1b78529], xmm0  ; -> 02064BF0
004EC6C7  movss    xmm0, dword ptr [rip + 0x1b785cd]  ; -> 02064C9C
004EC6CF  movss    dword ptr [rip + 0x1b78521], xmm1  ; -> 02064BF8
004EC6D7  movss    xmm1, dword ptr [rip + 0x1b785c1]  ; -> 02064CA0
004EC6DF  movss    dword ptr [rip + 0x1b78515], xmm0  ; -> 02064BFC
004EC6E7  movss    xmm0, dword ptr [rip + 0x1b785b9]  ; -> 02064CA8
004EC6EF  movss    dword ptr [rip + 0x1b78509], xmm1  ; -> 02064C00
004EC6F7  movss    xmm1, dword ptr [rip + 0x1b785ad]  ; -> 02064CAC
004EC6FF  movss    dword ptr [rip + 0x1b78501], xmm0  ; -> 02064C08
004EC707  movss    xmm0, dword ptr [rip + 0x1b78585]  ; -> 02064C94
004EC70F  movss    dword ptr [rip + 0x1b784f5], xmm1  ; -> 02064C0C
004EC717  subss    xmm0, xmm6
004EC71B  movss    xmm1, dword ptr [rip + 0x1b78581]  ; -> 02064CA4
004EC723  subss    xmm1, xmm6
004EC727  mov      word ptr [rip + 0x1b78696], ax  ; -> 02064DC4
004EC72E  movss    dword ptr [rip + 0x1b784be], xmm0  ; -> 02064BF4
004EC736  movss    dword ptr [rip + 0x1b784c6], xmm1  ; -> 02064C04
004EC73E  call     0x4eb910  ; -> 004EB910 fn
004EC743  movzx    eax, word ptr [rip + 0x1b7867a]  ; -> 02064DC4
004EC74A  movzx    r8d, word ptr [rip + 0x1b783ba]  ; -> 02064B0C
004EC752  mov      dword ptr [rip + 0x1b783a8], 0x40000000  ; -> 02064B04
004EC75C  cmp      ax, r8w
004EC760  je       0x4ec8b2  ; -> 004EC8B2
004EC766  movss    xmm0, dword ptr [rip + 0x1b78522]  ; -> 02064C90
004EC76E  dec      ax
004EC771  movss    xmm1, dword ptr [rip + 0x1b7851f]  ; -> 02064C98
004EC779  movss    dword ptr [rip + 0x1b7846f], xmm0  ; -> 02064BF0
004EC781  movss    xmm0, dword ptr [rip + 0x1b78513]  ; -> 02064C9C
004EC789  movss    dword ptr [rip + 0x1b78467], xmm1  ; -> 02064BF8
004EC791  movss    xmm1, dword ptr [rip + 0x1b78507]  ; -> 02064CA0
004EC799  movss    dword ptr [rip + 0x1b7845b], xmm0  ; -> 02064BFC
004EC7A1  movss    xmm0, dword ptr [rip + 0x1b784ff]  ; -> 02064CA8
004EC7A9  movss    dword ptr [rip + 0x1b7844f], xmm1  ; -> 02064C00
004EC7B1  movss    xmm1, dword ptr [rip + 0x1b784f3]  ; -> 02064CAC
004EC7B9  movss    dword ptr [rip + 0x1b78447], xmm0  ; -> 02064C08
004EC7C1  movss    xmm0, dword ptr [rip + 0x1b784cb]  ; -> 02064C94
004EC7C9  movss    dword ptr [rip + 0x1b7843b], xmm1  ; -> 02064C0C
004EC7D1  addss    xmm0, xmm7
004EC7D5  movss    xmm1, dword ptr [rip + 0x1b784c7]  ; -> 02064CA4
004EC7DD  addss    xmm1, xmm7
004EC7E1  mov      word ptr [rip + 0x1b785dc], ax  ; -> 02064DC4
004EC7E8  movss    dword ptr [rip + 0x1b78404], xmm0  ; -> 02064BF4
004EC7F0  movss    dword ptr [rip + 0x1b7840c], xmm1  ; -> 02064C04
004EC7F8  call     0x4eb910  ; -> 004EB910 fn
004EC7FD  movzx    r8d, word ptr [rip + 0x1b78307]  ; -> 02064B0C
004EC805  cmp      word ptr [rip + 0x1b785b7], r8w  ; -> 02064DC4
004EC80D  mov      dword ptr [rip + 0x1b782ed], 0xc0000000  ; -> 02064B04
004EC817  je       0x4ec8b2  ; -> 004EC8B2
004EC81D  movss    xmm0, dword ptr [rip + 0x1b7846b]  ; -> 02064C90
004EC825  movss    xmm1, dword ptr [rip + 0x1b7846b]  ; -> 02064C98
004EC82D  movss    dword ptr [rip + 0x1b783bb], xmm0  ; -> 02064BF0
004EC835  movss    xmm0, dword ptr [rip + 0x1b7845f]  ; -> 02064C9C
004EC83D  movss    dword ptr [rip + 0x1b783b3], xmm1  ; -> 02064BF8
004EC845  movss    xmm1, dword ptr [rip + 0x1b78453]  ; -> 02064CA0
004EC84D  movss    dword ptr [rip + 0x1b783a7], xmm0  ; -> 02064BFC
004EC855  movss    xmm0, dword ptr [rip + 0x1b7844b]  ; -> 02064CA8
004EC85D  movss    dword ptr [rip + 0x1b7839b], xmm1  ; -> 02064C00
004EC865  movss    xmm1, dword ptr [rip + 0x1b7843f]  ; -> 02064CAC
004EC86D  movss    dword ptr [rip + 0x1b78393], xmm0  ; -> 02064C08
004EC875  movss    xmm0, dword ptr [rip + 0x1b78417]  ; -> 02064C94
004EC87D  movss    dword ptr [rip + 0x1b78387], xmm1  ; -> 02064C0C
004EC885  subss    xmm0, xmm7
004EC889  movss    xmm1, dword ptr [rip + 0x1b78413]  ; -> 02064CA4
004EC891  subss    xmm1, xmm7
004EC895  movss    dword ptr [rip + 0x1b78357], xmm0  ; -> 02064BF4
004EC89D  movss    dword ptr [rip + 0x1b7835f], xmm1  ; -> 02064C04
004EC8A5  call     0x4eb910  ; -> 004EB910 fn
004EC8AA  movzx    r8d, word ptr [rip + 0x1b7825a]  ; -> 02064B0C
004EC8B2  movzx    eax, word ptr [rip + 0x1b7850f]  ; -> 02064DC8
004EC8B9  sub      ax, word ptr [rip + 0x1b784f8]  ; -> 02064DB8
004EC8C0  mov      word ptr [rip + 0x1b78521], ax  ; -> 02064DE8
004EC8C7  test     ax, ax
004EC8CA  jle      0x4ec8df  ; -> 004EC8DF
004EC8CC  mov      rdx, rbx
004EC8CF  mov      rcx, rdi
004EC8D2  call     0x2efe70  ; -> 002EFE70 fn
004EC8D7  movzx    r8d, word ptr [rip + 0x1b7822d]  ; -> 02064B0C
004EC8DF  movzx    eax, word ptr [rip + 0x1b784da]  ; -> 02064DC0
004EC8E6  cmp      ax, r8w
004EC8EA  je       0x4ec909  ; -> 004EC909
004EC8EC  movss    xmm8, dword ptr [rip + 0x1915f47]  ; -> 01E0283C [f32 1]
004EC8F5  movss    xmm9, dword ptr [rip + 0x1915f32]  ; -> 01E02830 [u32 0x00000000]
004EC8FE  mov      ecx, dword ptr [rip + 0x1b781f8]  ; -> 02064AFC
004EC904  jmp      0x4ec2b0  ; -> 004EC2B0
004EC909  cmp      word ptr [rip + 0x1b784a7], r8w  ; -> 02064DB8
004EC911  je       0x4ec91e  ; -> 004EC91E
004EC913  mov      rdx, rbx
004EC916  mov      rcx, rdi
004EC919  call     0x2efe70  ; -> 002EFE70 fn
004EC91E  movaps   xmm7, xmmword ptr [rsp + 0x70]
004EC923  lea      r11, [rsp + 0x90]
004EC92B  mov      rbx, qword ptr [r11 + 0x10]
004EC92F  mov      rsi, qword ptr [r11 + 0x18]
004EC933  movaps   xmm6, xmmword ptr [r11 - 0x10]
004EC938  movaps   xmm8, xmmword ptr [r11 - 0x30]
004EC93D  movaps   xmm9, xmmword ptr [r11 - 0x40]
004EC942  movaps   xmm10, xmmword ptr [r11 - 0x50]
004EC947  movaps   xmm11, xmmword ptr [r11 - 0x60]
004EC94C  mov      rsp, r11
004EC94F  pop      rdi
004EC950  ret      
```

## 004ECC50 (3334 B, extent 004ECC50-004ED956)

Page context: "18' = 0x1000404, '+0x1C' = 0x6C420000 - a module record's init.  Interior anchor '00476C93' (function '00476C80').  '004ED960' (482 B) is a battery constructor '0037E0F0' calls: '008631E0' registers '004ECC50', '008631D0(0x11)' fills '+0x10', then '+0xC' = 0x02000000, '+0x18' = 0x1000404, '+0x1C' = 0x6C0E0000 - a module record's init.  Interior anchor '004ED973' (function '004ED960').  '004D0CB0' (450 B) is a battery constructor '0037E0"

```
004ECC50  mov      rax, rsp
004ECC53  mov      qword ptr [rax + 8], rbx
004ECC57  mov      qword ptr [rax + 0x10], rsi
004ECC5B  push     rdi
004ECC5C  sub      rsp, 0xd0
004ECC63  movaps   xmmword ptr [rax - 0x18], xmm6
004ECC67  lea      rsi, [rip + 0x1b781c2]  ; -> 02064E30
004ECC6E  movaps   xmmword ptr [rax - 0x28], xmm7
004ECC72  mov      rdi, rcx
004ECC75  movaps   xmmword ptr [rax - 0x38], xmm8
004ECC7A  xor      r8d, r8d
004ECC7D  movaps   xmmword ptr [rax - 0x48], xmm9
004ECC82  mov      rbx, rdx
004ECC85  movaps   xmmword ptr [rax - 0x58], xmm10
004ECC8A  movaps   xmmword ptr [rax - 0x68], xmm11
004ECC8F  movaps   xmmword ptr [rax - 0x78], xmm12
004ECC94  movzx    eax, word ptr [rip + 0x1b77e71]  ; -> 02064B0C
004ECC9B  add      ax, 9
004ECC9F  movaps   xmmword ptr [rsp + 0x50], xmm13
004ECCA5  mov      word ptr [rip + 0x1b78128], ax  ; -> 02064DD4
004ECCAC  cwde     
004ECCAD  shl      eax, 4
004ECCB0  movsxd   rcx, eax
004ECCB3  add      rcx, rsi
004ECCB6  movaps   xmmword ptr [rsp + 0x40], xmm14
004ECCBC  movaps   xmmword ptr [rsp + 0x30], xmm15
004ECCC2  call     rdi
004ECCC4  movsx    edx, word ptr [rip + 0x1b77e41]  ; -> 02064B0C
004ECCCB  mov      ecx, edx
004ECCCD  shl      ecx, 4
004ECCD0  movsxd   rax, ecx
004ECCD3  movups   xmm5, xmmword ptr [rax + rsi]
004ECCD7  lea      eax, [rcx + 0x10]
004ECCDA  movsxd   rcx, eax
004ECCDD  lea      eax, [rdx + 3]
004ECCE0  shl      eax, 4
004ECCE3  movups   xmmword ptr [rip + 0x1b77e46], xmm5  ; -> 02064B30
004ECCEA  movups   xmm4, xmmword ptr [rcx + rsi]
004ECCEE  movsxd   rcx, eax
004ECCF1  lea      eax, [rdx + 4]
004ECCF4  shl      eax, 4
004ECCF7  movups   xmmword ptr [rip + 0x1b77e42], xmm4  ; -> 02064B40
004ECCFE  movups   xmm3, xmmword ptr [rcx + rsi]
004ECD02  movsxd   rcx, eax
004ECD05  lea      eax, [rdx + 5]
004ECD08  shl      eax, 4
004ECD0B  movups   xmmword ptr [rip + 0x1b77e3e], xmm3  ; -> 02064B50
004ECD12  movups   xmm0, xmmword ptr [rcx + rsi]
004ECD16  movsxd   rcx, eax
004ECD19  lea      eax, [rdx + 6]
004ECD1C  shl      eax, 4
004ECD1F  addss    xmm3, xmm5
004ECD23  movups   xmmword ptr [rip + 0x1b77e36], xmm0  ; -> 02064B60
004ECD2A  movups   xmm1, xmmword ptr [rcx + rsi]
004ECD2E  movsxd   rcx, eax
004ECD31  lea      eax, [rdx + 7]
004ECD34  shl      eax, 4
004ECD37  movups   xmmword ptr [rip + 0x1b77e32], xmm1  ; -> 02064B70
004ECD3E  movups   xmm2, xmmword ptr [rcx + rsi]
004ECD42  movsxd   rcx, eax
004ECD45  lea      eax, [rdx + 2]
004ECD48  shufps   xmm1, xmm1, 0xff
004ECD4C  movss    dword ptr [rsp + 0x2c], xmm1
004ECD52  movd     xmm1, dword ptr [rsp + 0x2c]
004ECD58  movups   xmm0, xmmword ptr [rcx + rsi]
004ECD5C  shl      eax, 4
004ECD5F  movups   xmmword ptr [rip + 0x1b77e1a], xmm2  ; -> 02064B80
004ECD66  movsxd   rcx, eax
004ECD69  cvtdq2ps xmm1, xmm1
004ECD6C  movzx    eax, word ptr [rcx + rsi]
004ECD70  mov      word ptr [rip + 0x1b78045], ax  ; -> 02064DBC
004ECD77  shufps   xmm2, xmm2, 0xff
004ECD7B  movss    dword ptr [rsp + 0x2c], xmm2
004ECD81  movaps   xmm2, xmm4
004ECD84  shufps   xmm2, xmm4, 0xff
004ECD88  movups   xmmword ptr [rip + 0x1b77e01], xmm0  ; -> 02064B90
004ECD8F  movaps   xmm0, xmm2
004ECD92  movss    dword ptr [rip + 0x1b77db6], xmm3  ; -> 02064B50
004ECD9A  mulss    xmm0, xmm1
004ECD9E  movd     xmm1, dword ptr [rsp + 0x2c]
004ECDA4  cvtdq2ps xmm1, xmm1
004ECDA7  cvttss2si eax, xmm0
004ECDAB  mulss    xmm1, xmm2
004ECDAF  mov      dword ptr [rip + 0x1b77dc7], eax  ; -> 02064B7C
004ECDB5  cvttss2si eax, xmm1
004ECDB9  mov      dword ptr [rip + 0x1b77dcd], eax  ; -> 02064B8C
004ECDBF  movss    xmm0, dword ptr [rip + 0x1b77d8d]  ; -> 02064B54
004ECDC7  movaps   xmm1, xmm5
004ECDCA  shufps   xmm1, xmm5, 0x55
004ECDCE  xorps    xmm9, xmm9
004ECDD2  subss    xmm5, xmm4
004ECDD6  movss    dword ptr [rip + 0x1b77d62], xmm4  ; -> 02064B40
004ECDDE  shufps   xmm4, xmm4, 0x55
004ECDE2  addss    xmm0, xmm1
004ECDE6  subss    xmm1, xmm4
004ECDEA  movss    dword ptr [rip + 0x1b77d52], xmm4  ; -> 02064B44
004ECDF2  ucomiss  xmm5, xmm9
004ECDF6  movss    dword ptr [rip + 0x1b77d36], xmm1  ; -> 02064B34
004ECDFE  movss    dword ptr [rip + 0x1b77d4e], xmm0  ; -> 02064B54
004ECE06  movss    dword ptr [rip + 0x1b77d22], xmm5  ; -> 02064B30
004ECE0E  jp       0x4ece12  ; -> 004ECE12
004ECE10  je       0x4ece1a  ; -> 004ECE1A
004ECE12  ucomiss  xmm1, xmm9
004ECE16  jp       0x4ece2f  ; -> 004ECE2F
004ECE18  jne      0x4ece2f  ; -> 004ECE2F
004ECE1A  call     0x22cc40  ; -> 0022CC40 fn
004ECE1F  movss    xmm1, dword ptr [rip + 0x1b77d0d]  ; -> 02064B34
004ECE27  movss    xmm5, dword ptr [rip + 0x1b77d01]  ; -> 02064B30
004ECE2F  comiss   xmm9, xmm5
004ECE33  ja       0x4ece3b  ; -> 004ECE3B
004ECE35  comiss   xmm9, xmm1
004ECE39  jbe      0x4ece40  ; -> 004ECE40
004ECE3B  call     0x22cc30  ; -> 0022CC30 fn
004ECE40  call     0x22cc20  ; -> 0022CC20 fn
004ECE45  movss    xmm2, dword ptr [rip + 0x1b77cf3]  ; -> 02064B40
004ECE4D  movss    xmm0, dword ptr [rip + 0x1b77d43]  ; -> 02064B98
004ECE55  addss    xmm2, xmm2
004ECE59  movss    xmm1, dword ptr [rip + 0x1b77d3b]  ; -> 02064B9C
004ECE61  subss    xmm0, dword ptr [rip + 0x1b77d27]  ; -> 02064B90
004ECE69  subss    xmm1, dword ptr [rip + 0x1b77d23]  ; -> 02064B94
004ECE71  movss    xmm4, dword ptr [rip + 0x1b77ccb]  ; -> 02064B44
004ECE79  ucomiss  xmm2, xmm9
004ECE7D  movss    xmm5, dword ptr [rip + 0x19159b7]  ; -> 01E0283C [f32 1]
004ECE85  addss    xmm4, xmm4
004ECE89  movss    xmm6, dword ptr [rip + 0x4134cf]  ; -> 00900360 [u32 0x7F7FFFFF]
004ECE91  movss    dword ptr [rip + 0x1b77d0f], xmm0  ; -> 02064BA8
004ECE99  movss    dword ptr [rip + 0x1b77d0b], xmm1  ; -> 02064BAC
004ECEA1  jp       0x4eceaa  ; -> 004ECEAA
004ECEA3  jne      0x4eceaa  ; -> 004ECEAA
004ECEA5  movaps   xmm1, xmm6
004ECEA8  jmp      0x4eceb1  ; -> 004ECEB1
004ECEAA  movaps   xmm1, xmm5
004ECEAD  divss    xmm1, xmm2
004ECEB1  ucomiss  xmm4, xmm9
004ECEB5  movss    xmm3, dword ptr [rip + 0x1915973]  ; -> 01E02830 [u32 0x00000000]
004ECEBD  movaps   xmm0, xmm3
004ECEC0  addss    xmm0, xmm1
004ECEC4  movss    dword ptr [rip + 0x1b77c74], xmm0  ; -> 02064B40
004ECECC  jp       0x4ecedd  ; -> 004ECEDD
004ECECE  jne      0x4ecedd  ; -> 004ECEDD
004ECED0  movss    dword ptr [rip + 0x1b77c28], xmm6  ; -> 02064B00
004ECED8  movaps   xmm0, xmm6
004ECEDB  jmp      0x4eceec  ; -> 004ECEEC
004ECEDD  movaps   xmm0, xmm5
004ECEE0  divss    xmm0, xmm4
004ECEE4  movss    dword ptr [rip + 0x1b77c14], xmm0  ; -> 02064B00
004ECEEC  movss    xmm2, dword ptr [rip + 0x1915940]  ; -> 01E02834 [u32 0x00000000]
004ECEF4  movaps   xmm1, xmm2
004ECEF7  addss    xmm1, xmm0
004ECEFB  ucomiss  xmm1, xmm9
004ECEFF  movss    dword ptr [rip + 0x1b77c3d], xmm1  ; -> 02064B44
004ECF07  jp       0x4ecf30  ; -> 004ECF30
004ECF09  jne      0x4ecf30  ; -> 004ECF30
004ECF0B  call     0x22cc40  ; -> 0022CC40 fn
004ECF10  movss    xmm1, dword ptr [rip + 0x1b77c2c]  ; -> 02064B44
004ECF18  movss    xmm5, dword ptr [rip + 0x191591c]  ; -> 01E0283C [f32 1]
004ECF20  movss    xmm2, dword ptr [rip + 0x191590c]  ; -> 01E02834 [u32 0x00000000]
004ECF28  movss    xmm3, dword ptr [rip + 0x1915900]  ; -> 01E02830 [u32 0x00000000]
004ECF30  comiss   xmm9, xmm1
004ECF34  jbe      0x4ecf53  ; -> 004ECF53
004ECF36  call     0x22cc30  ; -> 0022CC30 fn
004ECF3B  movss    xmm5, dword ptr [rip + 0x19158f9]  ; -> 01E0283C [f32 1]
004ECF43  movss    xmm2, dword ptr [rip + 0x19158e9]  ; -> 01E02834 [u32 0x00000000]
004ECF4B  movss    xmm3, dword ptr [rip + 0x19158dd]  ; -> 01E02830 [u32 0x00000000]
004ECF53  movzx    ecx, word ptr [rip + 0x1b77bb2]  ; -> 02064B0C
004ECF5A  movaps   xmm0, xmm3
004ECF5D  addss    xmm0, dword ptr [rip + 0x1b77c43]  ; -> 02064BA8
004ECF65  mov      word ptr [rip + 0x1b77e4c], cx  ; -> 02064DB8
004ECF6C  addss    xmm3, xmm5
004ECF70  movaps   xmm1, xmm2
004ECF73  mov      dword ptr [rip + 0x1b77b7f], 1  ; -> 02064AFC
004ECF7D  addss    xmm1, dword ptr [rip + 0x1b77c27]  ; -> 02064BAC
004ECF85  lea      eax, [rcx + 0x40]
004ECF88  add      cx, 8
004ECF8C  mov      word ptr [rip + 0x1b77e3d], cx  ; -> 02064DD0
004ECF93  addss    xmm2, xmm2
004ECF97  mov      word ptr [rip + 0x1b77e12], ax  ; -> 02064DB0
004ECF9E  inc      ax
004ECFA1  mov      word ptr [rip + 0x1b77e0c], ax  ; -> 02064DB4
004ECFA8  movss    dword ptr [rip + 0x1b77bf0], xmm0  ; -> 02064BA0
004ECFB0  movss    xmm0, dword ptr [rip + 0x1b77b84]  ; -> 02064B3C
004ECFB8  movss    dword ptr [rip + 0x1915868], xmm0  ; -> 01E02828 [f32 1]
004ECFC0  mov      eax, dword ptr [rip + 0x1915862]  ; -> 01E02828 [f32 1]
004ECFC6  mov      ecx, eax
004ECFC8  shr      ecx, 0x12
004ECFCB  xor      ecx, eax
004ECFCD  movss    dword ptr [rip + 0x1b77bcf], xmm1  ; -> 02064BA4
004ECFD5  and      eax, 0x3fffff
004ECFDA  shr      ecx, 4
004ECFDD  or       eax, 0x1fc00000
004ECFE2  movss    dword ptr [rip + 0x1b77bd6], xmm3  ; -> 02064BC0
004ECFEA  add      eax, eax
004ECFEC  movss    dword ptr [rip + 0x1b77bd0], xmm2  ; -> 02064BC4
004ECFF4  and      ecx, 1
004ECFF7  or       ecx, eax
004ECFF9  mov      dword ptr [rip + 0x1915829], ecx  ; -> 01E02828 [f32 1]
004ECFFF  movss    xmm0, dword ptr [rip + 0x1915821]  ; -> 01E02828 [f32 1]
004ED007  movss    dword ptr [rip + 0x1b77ca1], xmm0  ; -> 02064CB0
004ED00F  call     0x5375f0  ; -> 005375F0 fn
004ED014  call     0x5376d0  ; -> 005376D0 fn
004ED019  movss    xmm0, dword ptr [rip + 0x1b77ca3]  ; -> 02064CC4
004ED021  movss    xmm2, dword ptr [rip + 0x1915807]  ; -> 01E02830 [u32 0x00000000]
004ED029  movss    xmm1, dword ptr [rip + 0x1b77c8f]  ; -> 02064CC0
004ED031  addss    xmm0, xmm2
004ED035  subss    xmm2, xmm1
004ED039  movss    dword ptr [rip + 0x1b77cbf], xmm0  ; -> 02064D00
004ED041  movaps   xmm0, xmm1
004ED044  addss    xmm0, dword ptr [rip + 0x19157e8]  ; -> 01E02834 [u32 0x00000000]
004ED04C  movss    dword ptr [rip + 0x1b77cbc], xmm2  ; -> 02064D10
004ED054  movss    dword ptr [rip + 0x1b77ca8], xmm0  ; -> 02064D04
004ED05C  call     0x22cc20  ; -> 0022CC20 fn
004ED061  movss    xmm0, dword ptr [rip + 0x1b77ca7]  ; -> 02064D10
004ED069  mulss    xmm0, dword ptr [rip + 0x1b77b53]  ; -> 02064BC4
004ED071  movsx    eax, word ptr [rip + 0x1b77a94]  ; -> 02064B0C
004ED078  movss    xmm2, dword ptr [rip + 0x1b77c80]  ; -> 02064D00
004ED080  add      eax, 2
004ED083  mulss    xmm2, dword ptr [rip + 0x1b77b35]  ; -> 02064BC0
004ED08B  shl      eax, 4
004ED08E  movss    xmm4, dword ptr [rip + 0x1b77c2e]  ; -> 02064CC4
004ED096  addss    xmm4, dword ptr [rip + 0x1915796]  ; -> 01E02834 [u32 0x00000000]
004ED09E  movss    xmm3, dword ptr [rip + 0x1b77c5e]  ; -> 02064D04
004ED0A6  addss    xmm0, xmm2
004ED0AA  mulss    xmm3, dword ptr [rip + 0x1b77b0e]  ; -> 02064BC0
004ED0B2  cdqe     
004ED0B4  movss    dword ptr [rip + 0x1b77a64], xmm2  ; -> 02064B20
004ED0BC  movss    dword ptr [rip + 0x1b77c50], xmm4  ; -> 02064D14
004ED0C4  mulss    xmm4, dword ptr [rip + 0x1b77af8]  ; -> 02064BC4
004ED0CC  movss    dword ptr [rip + 0x1b77aec], xmm0  ; -> 02064BC0
004ED0D4  movss    xmm0, dword ptr [rax + rsi]
004ED0D9  movss    dword ptr [rip + 0x1b77bcf], xmm0  ; -> 02064CB0
004ED0E1  addss    xmm4, xmm3
004ED0E5  movd     xmm1, dword ptr [rip + 0x1b77bc3]  ; -> 02064CB0
004ED0ED  cvtdq2ps xmm1, xmm1
004ED0F0  movss    dword ptr [rip + 0x1b77a2c], xmm3  ; -> 02064B24
004ED0F8  ucomiss  xmm1, xmm9
004ED0FC  movss    dword ptr [rip + 0x1b77ac0], xmm4  ; -> 02064BC4
004ED104  jp       0x4ed108  ; -> 004ED108
004ED106  je       0x4ed114  ; -> 004ED114
004ED108  movss    xmm6, dword ptr [rip + 0x1b77a28]  ; -> 02064B38
004ED110  divss    xmm6, xmm1
004ED114  movss    xmm0, dword ptr [rip + 0x1915714]  ; -> 01E02830 [u32 0x00000000]
004ED11C  addss    xmm0, xmm6
004ED120  movss    dword ptr [rip + 0x1b779d8], xmm6  ; -> 02064B00
004ED128  movss    dword ptr [rip + 0x1b77b80], xmm0  ; -> 02064CB0
004ED130  call     0x5375f0  ; -> 005375F0 fn
004ED135  call     0x5376d0  ; -> 005376D0 fn
004ED13A  movss    xmm0, dword ptr [rip + 0x1b77b82]  ; -> 02064CC4
004ED142  movss    xmm2, dword ptr [rip + 0x19156e6]  ; -> 01E02830 [u32 0x00000000]
004ED14A  movss    xmm1, dword ptr [rip + 0x1b77b6e]  ; -> 02064CC0
004ED152  addss    xmm0, xmm2
004ED156  subss    xmm2, xmm1
004ED15A  movss    dword ptr [rip + 0x1b77b9e], xmm0  ; -> 02064D00
004ED162  movaps   xmm0, xmm1
004ED165  addss    xmm0, dword ptr [rip + 0x19156c7]  ; -> 01E02834 [u32 0x00000000]
004ED16D  movss    dword ptr [rip + 0x1b77b9b], xmm2  ; -> 02064D10
004ED175  movss    dword ptr [rip + 0x1b77b87], xmm0  ; -> 02064D04
004ED17D  call     0x22cc20  ; -> 0022CC20 fn
004ED182  movss    xmm10, dword ptr [rip + 0x1b77b39]  ; -> 02064CC4
004ED18B  addss    xmm10, dword ptr [rip + 0x19156a0]  ; -> 01E02834 [u32 0x00000000]
004ED194  movaps   xmm15, xmmword ptr [rip + 0x428254]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004ED19C  movss    xmm14, dword ptr [rip + 0x17fea03]  ; -> 01CEBBA8 [f32 1]
004ED1A5  movzx    eax, word ptr [rip + 0x1b77c10]  ; -> 02064DBC
004ED1AC  movzx    ecx, word ptr [rip + 0x1b77c05]  ; -> 02064DB8
004ED1B3  movss    dword ptr [rip + 0x1b77b58], xmm10  ; -> 02064D14
004ED1BC  nop      dword ptr [rax]
004ED1C0  mulss    xmm10, dword ptr [rip + 0x1b779fb]  ; -> 02064BC4
004ED1C9  dec      ax
004ED1CC  inc      cx
004ED1CF  mov      word ptr [rip + 0x1b77be6], ax  ; -> 02064DBC
004ED1D6  movss    xmm1, dword ptr [rip + 0x1b77b22]  ; -> 02064D00
004ED1DE  cmp      dword ptr [rip + 0x1b77917], 0  ; -> 02064AFC
004ED1E5  mulss    xmm1, dword ptr [rip + 0x1b779d3]  ; -> 02064BC0
004ED1ED  mov      word ptr [rip + 0x1b77bc4], cx  ; -> 02064DB8
004ED1F4  movss    xmm2, dword ptr [rip + 0x1b77b08]  ; -> 02064D04
004ED1FC  mulss    xmm2, dword ptr [rip + 0x1b779bc]  ; -> 02064BC0
004ED204  movss    xmm11, dword ptr [rip + 0x1b77b03]  ; -> 02064D10
004ED20D  mulss    xmm11, dword ptr [rip + 0x1b779ae]  ; -> 02064BC4
004ED216  addss    xmm10, xmm2
004ED21B  movss    dword ptr [rip + 0x1b778fd], xmm1  ; -> 02064B20
004ED223  movss    dword ptr [rip + 0x1b778f9], xmm2  ; -> 02064B24
004ED22B  addss    xmm11, xmm1
004ED230  movss    dword ptr [rip + 0x1b7798b], xmm10  ; -> 02064BC4
004ED239  movss    dword ptr [rip + 0x1b7797e], xmm11  ; -> 02064BC0
004ED242  je       0x4ed4bc  ; -> 004ED4BC
004ED248  mov      eax, dword ptr [rip + 0x19155da]  ; -> 01E02828 [f32 1]
004ED24E  mov      ecx, eax
004ED250  shr      ecx, 0x12
004ED253  xor      ecx, eax
004ED255  and      eax, 0x3fffff
004ED25A  shr      ecx, 4
004ED25D  or       eax, 0x1fc00000
004ED262  and      ecx, 1
004ED265  add      eax, eax
004ED267  or       ecx, eax
004ED269  mov      eax, ecx
004ED26B  shr      eax, 0x12
004ED26E  xor      eax, ecx
004ED270  and      ecx, 0x3fffff
004ED276  or       ecx, 0x1fc00000
004ED27C  shr      eax, 4
004ED27F  add      ecx, ecx
004ED281  and      eax, 1
004ED284  or       eax, ecx
004ED286  mov      ecx, eax
004ED288  shr      ecx, 0x12
004ED28B  xor      ecx, eax
004ED28D  and      eax, 0x3fffff
004ED292  shr      ecx, 4
004ED295  or       eax, 0x1fc00000
004ED29A  and      ecx, 1
004ED29D  add      eax, eax
004ED29F  or       ecx, eax
004ED2A1  mov      eax, ecx
004ED2A3  shr      eax, 0x12
004ED2A6  xor      eax, ecx
004ED2A8  and      ecx, 0x3fffff
004ED2AE  or       ecx, 0x1fc00000
004ED2B4  shr      eax, 4
004ED2B7  add      ecx, ecx
004ED2B9  and      eax, 1
004ED2BC  or       eax, ecx
004ED2BE  mov      ecx, eax
004ED2C0  shr      ecx, 0x12
004ED2C3  xor      ecx, eax
004ED2C5  and      eax, 0x3fffff
004ED2CA  shr      ecx, 4
004ED2CD  or       eax, 0x1fc00000
004ED2D2  and      ecx, 1
004ED2D5  add      eax, eax
004ED2D7  or       ecx, eax
004ED2D9  mov      eax, ecx
004ED2DB  mov      dword ptr [rip + 0x1915547], ecx  ; -> 01E02828 [f32 1]
004ED2E1  movss    xmm4, dword ptr [rip + 0x191553f]  ; -> 01E02828 [f32 1]
004ED2E9  shr      eax, 0x12
004ED2EC  xor      eax, ecx
004ED2EE  and      ecx, 0x3fffff
004ED2F4  or       ecx, 0x1fc00000
004ED2FA  shr      eax, 4
004ED2FD  add      ecx, ecx
004ED2FF  and      eax, 1
004ED302  or       eax, ecx
004ED304  mov      ecx, eax
004ED306  shr      ecx, 0x12
004ED309  xor      ecx, eax
004ED30B  and      eax, 0x3fffff
004ED310  shr      ecx, 4
004ED313  or       eax, 0x1fc00000
004ED318  and      ecx, 1
004ED31B  add      eax, eax
004ED31D  or       ecx, eax
004ED31F  mov      eax, ecx
004ED321  shr      eax, 0x12
004ED324  xor      eax, ecx
004ED326  and      ecx, 0x3fffff
004ED32C  or       ecx, 0x1fc00000
004ED332  shr      eax, 4
004ED335  add      ecx, ecx
004ED337  and      eax, 1
004ED33A  or       eax, ecx
004ED33C  mov      ecx, eax
004ED33E  shr      ecx, 0x12
004ED341  xor      ecx, eax
004ED343  shr      ecx, 4
004ED346  and      ecx, 1
004ED349  and      eax, 0x3fffff
004ED34E  or       eax, 0x1fc00000
004ED353  add      eax, eax
004ED355  or       ecx, eax
004ED357  mov      edx, ecx
004ED359  shr      edx, 0x12
004ED35C  xor      edx, ecx
004ED35E  and      ecx, 0x3fffff
004ED364  or       ecx, 0x1fc00000
004ED36A  shr      edx, 4
004ED36D  add      ecx, ecx
004ED36F  and      edx, 1
004ED372  or       edx, ecx
004ED374  mov      dword ptr [rip + 0x19154ae], edx  ; -> 01E02828 [f32 1]
004ED37A  mov      eax, edx
004ED37C  movss    xmm3, dword ptr [rip + 0x19154a4]  ; -> 01E02828 [f32 1]
004ED384  shr      eax, 0x12
004ED387  xor      eax, edx
004ED389  and      edx, 0x3fffff
004ED38F  shr      eax, 4
004ED392  or       edx, 0x1fc00000
004ED398  and      eax, 1
004ED39B  add      edx, edx
004ED39D  or       eax, edx
004ED39F  mov      ecx, eax
004ED3A1  shr      ecx, 0x12
004ED3A4  xor      ecx, eax
004ED3A6  and      eax, 0x3fffff
004ED3AB  or       eax, 0x1fc00000
004ED3B0  shr      ecx, 4
004ED3B3  add      eax, eax
004ED3B5  and      ecx, 1
004ED3B8  or       ecx, eax
004ED3BA  mov      eax, ecx
004ED3BC  shr      eax, 0x12
004ED3BF  xor      eax, ecx
004ED3C1  and      ecx, 0x3fffff
004ED3C7  or       ecx, 0x1fc00000
004ED3CD  shr      eax, 4
004ED3D0  add      ecx, ecx
004ED3D2  and      eax, 1
004ED3D5  or       eax, ecx
004ED3D7  mov      ecx, eax
004ED3D9  shr      ecx, 0x12
004ED3DC  xor      ecx, eax
004ED3DE  and      eax, 0x3fffff
004ED3E3  or       eax, 0x1fc00000
004ED3E8  shr      ecx, 4
004ED3EB  add      eax, eax
004ED3ED  and      ecx, 1
004ED3F0  or       ecx, eax
004ED3F2  mov      edx, ecx
004ED3F4  shr      edx, 0x12
004ED3F7  xor      edx, ecx
004ED3F9  and      ecx, 0x3fffff
004ED3FF  or       ecx, 0x1fc00000
004ED405  shr      edx, 4
004ED408  add      ecx, ecx
004ED40A  and      edx, 1
004ED40D  or       edx, ecx
004ED40F  mov      eax, edx
004ED411  mov      dword ptr [rip + 0x1915411], edx  ; -> 01E02828 [f32 1]
004ED417  movss    xmm12, dword ptr [rip + 0x1915408]  ; -> 01E02828 [f32 1]
004ED420  shr      eax, 0x12
004ED423  xor      eax, edx
004ED425  and      edx, 0x3fffff
004ED42B  shr      eax, 4
004ED42E  or       edx, 0x1fc00000
004ED434  and      eax, 1
004ED437  add      edx, edx
004ED439  or       eax, edx
004ED43B  mov      ecx, eax
004ED43D  shr      ecx, 0x12
004ED440  xor      ecx, eax
004ED442  and      eax, 0x3fffff
004ED447  or       eax, 0x1fc00000
004ED44C  shr      ecx, 4
004ED44F  add      eax, eax
004ED451  and      ecx, 1
004ED454  or       ecx, eax
004ED456  mov      eax, ecx
004ED458  shr      eax, 0x12
004ED45B  xor      eax, ecx
004ED45D  and      ecx, 0x3fffff
004ED463  or       ecx, 0x1fc00000
004ED469  shr      eax, 4
004ED46C  add      ecx, ecx
004ED46E  and      eax, 1
004ED471  or       eax, ecx
004ED473  mov      ecx, eax
004ED475  shr      ecx, 0x12
004ED478  xor      ecx, eax
004ED47A  and      eax, 0x3fffff
004ED47F  or       eax, 0x1fc00000
004ED484  shr      ecx, 4
004ED487  add      eax, eax
004ED489  and      ecx, 1
004ED48C  or       ecx, eax
004ED48E  mov      eax, ecx
004ED490  shr      eax, 0x12
004ED493  xor      eax, ecx
004ED495  and      ecx, 0x3fffff
004ED49B  or       ecx, 0x1fc00000
004ED4A1  shr      eax, 4
004ED4A4  add      ecx, ecx
004ED4A6  and      eax, 1
004ED4A9  or       eax, ecx
004ED4AB  mov      dword ptr [rip + 0x1915377], eax  ; -> 01E02828 [f32 1]
004ED4B1  movss    xmm13, dword ptr [rip + 0x191536e]  ; -> 01E02828 [f32 1]
004ED4BA  jmp      0x4ed4cc  ; -> 004ED4CC
004ED4BC  movaps   xmm4, xmm14
004ED4C0  movaps   xmm3, xmm14
004ED4C4  movaps   xmm12, xmm14
004ED4C8  movaps   xmm13, xmm14
004ED4CC  movss    xmm8, dword ptr [rip + 0x1915367]  ; -> 01E0283C [f32 1]
004ED4D5  movaps   xmm5, xmm11
004ED4D9  movss    xmm2, dword ptr [rip + 0x1915357]  ; -> 01E02838 [u32 0x00000000]
004ED4E1  subss    xmm3, xmm8
004ED4E6  movaps   xmm0, xmm2
004ED4E9  subss    xmm4, xmm8
004ED4EE  addss    xmm0, dword ptr [rip + 0x1b77652]  ; -> 02064B48
004ED4F6  addss    xmm2, xmm8
004ED4FB  movaps   xmm7, xmm11
004ED4FF  movaps   xmm6, xmm10
004ED503  subss    xmm12, xmm8
004ED508  mulss    xmm3, dword ptr [rip + 0x1b77654]  ; -> 02064B64
004ED510  subss    xmm13, xmm8
004ED515  movss    dword ptr [rip + 0x1b776cb], xmm0  ; -> 02064BE8
004ED51D  movaps   xmm1, xmm8
004ED521  movss    dword ptr [rip + 0x1b776df], xmm0  ; -> 02064C08
004ED529  movss    xmm0, dword ptr [rip + 0x1b7762b]  ; -> 02064B5C
004ED531  mulss    xmm0, xmm4
004ED535  movaps   xmm4, xmm10
004ED539  mulss    xmm4, xmm3
004ED53D  mulss    xmm7, xmm0
004ED541  mulss    xmm6, xmm0
004ED545  mulss    xmm1, xmm8
004ED54A  mulss    xmm5, xmm3
004ED54E  movaps   xmm3, xmm10
004ED552  mulss    xmm3, dword ptr [rip + 0x1b775fe]  ; -> 02064B58
004ED55A  movss    dword ptr [rip + 0x1b7768a], xmm1  ; -> 02064BEC
004ED562  movss    dword ptr [rip + 0x1b776a2], xmm1  ; -> 02064C0C
004ED56A  movss    xmm1, dword ptr [rip + 0x1b775ee]  ; -> 02064B60
004ED572  addss    xmm6, xmm3
004ED576  movaps   xmm0, xmm1
004ED579  movss    dword ptr [rip + 0x1b77657], xmm2  ; -> 02064BD8
004ED581  mulss    xmm0, xmm11
004ED586  mulss    xmm1, xmm10
004ED58B  addss    xmm5, xmm0
004ED58F  movss    dword ptr [rip + 0x1b77661], xmm2  ; -> 02064BF8
004ED597  movss    dword ptr [rip + 0x1b77721], xmm0  ; -> 02064CC0
004ED59F  movaps   xmm10, xmm6
004ED5A3  movss    xmm0, dword ptr [rip + 0x1b775a5]  ; -> 02064B50
004ED5AB  addss    xmm4, xmm1
004ED5AF  movaps   xmm2, xmm11
004ED5B3  movss    dword ptr [rip + 0x1b77709], xmm1  ; -> 02064CC4
004ED5BB  mulss    xmm2, dword ptr [rip + 0x1b77595]  ; -> 02064B58
004ED5C3  movss    xmm1, dword ptr [rip + 0x1b77589]  ; -> 02064B54
004ED5CB  movss    dword ptr [rip + 0x1b776e1], xmm3  ; -> 02064CB4
004ED5D3  addss    xmm6, xmm1
004ED5D7  addss    xmm7, xmm2
004ED5DB  movss    dword ptr [rip + 0x1b776cd], xmm2  ; -> 02064CB0
004ED5E3  movss    dword ptr [rip + 0x1b776e4], xmm12  ; -> 02064CD0
004ED5EC  movaps   xmm3, xmm5
004ED5EF  mulss    xmm12, dword ptr [rip + 0x1b77570]  ; -> 02064B68
004ED5F8  addss    xmm5, xmm0
004ED5FC  movss    dword ptr [rip + 0x1b776db], xmm13  ; -> 02064CE0
004ED605  movaps   xmm2, xmm4
004ED608  mulss    xmm13, dword ptr [rip + 0x1b7755b]  ; -> 02064B6C
004ED611  addss    xmm4, xmm1
004ED615  addss    xmm12, xmm8
004ED61A  movss    dword ptr [rip + 0x1b775c2], xmm6  ; -> 02064BE4
004ED622  movaps   xmm11, xmm7
004ED626  movss    dword ptr [rip + 0x1b775d2], xmm5  ; -> 02064C00
004ED62E  addss    xmm7, xmm0
004ED632  addss    xmm13, xmm8
004ED637  movss    dword ptr [rip + 0x1b775c5], xmm4  ; -> 02064C04
004ED63F  mulss    xmm11, xmm12
004ED644  movss    dword ptr [rip + 0x1b77594], xmm7  ; -> 02064BE0
004ED64C  mulss    xmm3, xmm13
004ED651  addss    xmm11, xmm0
004ED656  mulss    xmm10, xmm12
004ED65B  addss    xmm3, xmm0
004ED65F  mulss    xmm2, xmm13
004ED664  movups   xmm0, xmmword ptr [rip + 0x1b77575]  ; -> 02064BE0
004ED66B  addss    xmm2, xmm1
004ED66F  mulps    xmm0, xmm15
004ED673  addss    xmm10, xmm1
004ED678  movups   xmm1, xmmword ptr [rip + 0x1b77581]  ; -> 02064C00
004ED67F  movss    dword ptr [rip + 0x1b77569], xmm3  ; -> 02064BF0
004ED687  cvttps2dq xmm0, xmm0
004ED68B  mulps    xmm1, xmm15
004ED68F  movdqu   xmmword ptr [rip + 0x1b77549], xmm0  ; -> 02064BE0
004ED697  movss    dword ptr [rip + 0x1b77555], xmm2  ; -> 02064BF4
004ED69F  cvttps2dq xmm0, xmm1
004ED6A3  subss    xmm11, dword ptr [rip + 0x1b77484]  ; -> 02064B30
004ED6AC  subss    xmm10, dword ptr [rip + 0x1b7747f]  ; -> 02064B34
004ED6B5  movdqu   xmmword ptr [rip + 0x1b77543], xmm0  ; -> 02064C00
004ED6BD  ucomiss  xmm11, xmm9
004ED6C1  movss    dword ptr [rip + 0x1b77506], xmm11  ; -> 02064BD0
004ED6CA  movss    dword ptr [rip + 0x1b77501], xmm10  ; -> 02064BD4
004ED6D3  jp       0x4ed6d7  ; -> 004ED6D7
004ED6D5  je       0x4ed6df  ; -> 004ED6DF
004ED6D7  ucomiss  xmm10, xmm9
004ED6DB  jp       0x4ed6f6  ; -> 004ED6F6
004ED6DD  jne      0x4ed6f6  ; -> 004ED6F6
004ED6DF  call     0x22cc40  ; -> 0022CC40 fn
004ED6E4  movss    xmm10, dword ptr [rip + 0x1b774e7]  ; -> 02064BD4
004ED6ED  movss    xmm11, dword ptr [rip + 0x1b774da]  ; -> 02064BD0
004ED6F6  comiss   xmm9, xmm11
004ED6FA  ja       0x4ed702  ; -> 004ED702
004ED6FC  comiss   xmm9, xmm10
004ED700  jbe      0x4ed707  ; -> 004ED707
004ED702  call     0x22cc30  ; -> 0022CC30 fn
004ED707  call     0x22cc20  ; -> 0022CC20 fn
004ED70C  movss    xmm1, dword ptr [rip + 0x1b774dc]  ; -> 02064BF0
004ED714  movss    xmm0, dword ptr [rip + 0x1b774d8]  ; -> 02064BF4
004ED71C  subss    xmm1, dword ptr [rip + 0x1b7740c]  ; -> 02064B30
004ED724  subss    xmm0, dword ptr [rip + 0x1b77408]  ; -> 02064B34
004ED72C  ucomiss  xmm1, xmm9
004ED730  movss    dword ptr [rip + 0x1b774b8], xmm1  ; -> 02064BF0
004ED738  movss    dword ptr [rip + 0x1b774b4], xmm0  ; -> 02064BF4
004ED740  jp       0x4ed744  ; -> 004ED744
004ED742  je       0x4ed74c  ; -> 004ED74C
004ED744  ucomiss  xmm0, xmm9
004ED748  jp       0x4ed761  ; -> 004ED761
004ED74A  jne      0x4ed761  ; -> 004ED761
004ED74C  call     0x22cc40  ; -> 0022CC40 fn
004ED751  movss    xmm0, dword ptr [rip + 0x1b7749b]  ; -> 02064BF4
004ED759  movss    xmm1, dword ptr [rip + 0x1b7748f]  ; -> 02064BF0
004ED761  comiss   xmm9, xmm1
004ED765  ja       0x4ed76d  ; -> 004ED76D
004ED767  comiss   xmm9, xmm0
004ED76B  jbe      0x4ed772  ; -> 004ED772
004ED76D  call     0x22cc30  ; -> 0022CC30 fn
004ED772  call     0x22cc20  ; -> 0022CC20 fn
004ED777  movsx    edx, word ptr [rip + 0x1b77636]  ; -> 02064DB4
004ED77E  movss    xmm5, dword ptr [rip + 0x1b7744a]  ; -> 02064BD0
004ED786  mov      eax, edx
004ED788  movss    xmm6, dword ptr [rip + 0x1b77444]  ; -> 02064BD4
004ED790  inc      dx
004ED793  mulss    xmm5, dword ptr [rip + 0x1b773a5]  ; -> 02064B40
004ED79B  shl      eax, 4
004ED79E  mulss    xmm6, dword ptr [rip + 0x1b7739e]  ; -> 02064B44
004ED7A6  movsxd   rcx, eax
004ED7A9  movss    xmm3, dword ptr [rip + 0x1b7743f]  ; -> 02064BF0
004ED7B1  movss    xmm4, dword ptr [rip + 0x1b7743b]  ; -> 02064BF4
004ED7B9  mulss    xmm3, dword ptr [rip + 0x1b7737f]  ; -> 02064B40
004ED7C1  movsx    eax, dx
004ED7C4  inc      dx
004ED7C7  mulss    xmm4, dword ptr [rip + 0x1b77375]  ; -> 02064B44
004ED7CF  shl      eax, 4
004ED7D2  mulss    xmm5, dword ptr [rip + 0x1b773c6]  ; -> 02064BA0
004ED7DA  mulss    xmm6, dword ptr [rip + 0x1b773c2]  ; -> 02064BA4
004ED7E2  addss    xmm5, dword ptr [rip + 0x1b773a6]  ; -> 02064B90
004ED7EA  mulss    xmm3, dword ptr [rip + 0x1b773ae]  ; -> 02064BA0
004ED7F2  addss    xmm6, dword ptr [rip + 0x1b7739a]  ; -> 02064B94
004ED7FA  mulss    xmm4, dword ptr [rip + 0x1b773a2]  ; -> 02064BA4
004ED802  addss    xmm3, dword ptr [rip + 0x1b77386]  ; -> 02064B90
004ED80A  movss    dword ptr [rip + 0x1b773be], xmm5  ; -> 02064BD0
004ED812  addss    xmm4, dword ptr [rip + 0x1b7737a]  ; -> 02064B94
004ED81A  movss    dword ptr [rip + 0x1b773b2], xmm6  ; -> 02064BD4
004ED822  movups   xmm0, xmmword ptr [rip + 0x1b773a7]  ; -> 02064BD0
004ED829  movss    dword ptr [rip + 0x1b773bf], xmm3  ; -> 02064BF0
004ED831  movups   xmmword ptr [rcx + rsi], xmm0
004ED835  movsxd   rcx, eax
004ED838  movups   xmm0, xmmword ptr [rip + 0x1b77331]  ; -> 02064B70
004ED83F  movsx    eax, dx
004ED842  inc      dx
004ED845  shl      eax, 4
004ED848  movups   xmmword ptr [rcx + rsi], xmm0
004ED84C  movsxd   rcx, eax
004ED84F  movups   xmm0, xmmword ptr [rip + 0x1b7738a]  ; -> 02064BE0
004ED856  movsx    eax, dx
004ED859  inc      dx
004ED85C  shl      eax, 4
004ED85F  movups   xmmword ptr [rcx + rsi], xmm0
004ED863  movsxd   rcx, eax
004ED866  movsx    eax, dx
004ED869  inc      dx
004ED86C  shl      eax, 4
004ED86F  movss    dword ptr [rip + 0x1b7737d], xmm4  ; -> 02064BF4
004ED877  movups   xmm0, xmmword ptr [rip + 0x1b77372]  ; -> 02064BF0
004ED87E  movups   xmmword ptr [rcx + rsi], xmm0
004ED882  movsxd   rcx, eax
004ED885  movups   xmm0, xmmword ptr [rip + 0x1b772f4]  ; -> 02064B80
004ED88C  movsx    eax, dx
004ED88F  inc      dx
004ED892  shl      eax, 4
004ED895  movups   xmmword ptr [rcx + rsi], xmm0
004ED899  movzx    ecx, word ptr [rip + 0x1b77518]  ; -> 02064DB8
004ED8A0  movups   xmm0, xmmword ptr [rip + 0x1b77359]  ; -> 02064C00
004ED8A7  cdqe     
004ED8A9  mov      word ptr [rip + 0x1b77504], dx  ; -> 02064DB4
004ED8B0  movzx    edx, word ptr [rip + 0x1b77255]  ; -> 02064B0C
004ED8B7  movups   xmmword ptr [rax + rsi], xmm0
004ED8BB  lea      eax, [rdx + 0x40]
004ED8BE  mov      word ptr [rip + 0x1b7750f], ax  ; -> 02064DD4
004ED8C5  cmp      cx, ax
004ED8C8  jne      0x4ed8e3  ; -> 004ED8E3
004ED8CA  mov      rdx, rbx
004ED8CD  mov      rcx, rdi
004ED8D0  call     0x4ecb70  ; -> 004ECB70 fn
004ED8D5  movzx    edx, word ptr [rip + 0x1b77230]  ; -> 02064B0C
004ED8DC  movzx    ecx, word ptr [rip + 0x1b774d5]  ; -> 02064DB8
004ED8E3  movzx    eax, word ptr [rip + 0x1b774d2]  ; -> 02064DBC
004ED8EA  cmp      ax, dx
004ED8ED  je       0x4ed8fd  ; -> 004ED8FD
004ED8EF  movss    xmm10, dword ptr [rip + 0x1b7741c]  ; -> 02064D14
004ED8F8  jmp      0x4ed1c0  ; -> 004ED1C0
004ED8FD  cmp      cx, dx
004ED900  je       0x4ed90d  ; -> 004ED90D
004ED902  mov      rdx, rbx
004ED905  mov      rcx, rdi
004ED908  call     0x4ecb70  ; -> 004ECB70 fn
004ED90D  movaps   xmm14, xmmword ptr [rsp + 0x40]
004ED913  lea      r11, [rsp + 0xd0]
004ED91B  mov      rbx, qword ptr [r11 + 0x10]
004ED91F  mov      rsi, qword ptr [r11 + 0x18]
004ED923  movaps   xmm6, xmmword ptr [r11 - 0x10]
004ED928  movaps   xmm7, xmmword ptr [r11 - 0x20]
004ED92D  movaps   xmm8, xmmword ptr [r11 - 0x30]
004ED932  movaps   xmm9, xmmword ptr [r11 - 0x40]
004ED937  movaps   xmm10, xmmword ptr [r11 - 0x50]
004ED93C  movaps   xmm11, xmmword ptr [r11 - 0x60]
004ED941  movaps   xmm12, xmmword ptr [r11 - 0x70]
004ED946  movaps   xmm13, xmmword ptr [r11 - 0x80]
004ED94B  movaps   xmm15, xmmword ptr [rsp + 0x30]
004ED951  mov      rsp, r11
004ED954  pop      rdi
004ED955  ret      
```

## 004F7070 (24541 B, extent 004F7070-004FD04D)

Page context: "not by address).  Interior anchor '0037E15B' (function '0037E0F0').  '004FD060' (1104 B) is the largest of the register battery's constructors: '00861EC0' zeroes 0x300, '008631E0' registers callback '004F7070', '008631D0(0x2E)' fills the '+0x10' array, then sixty-odd constant stores write '+0x18'..'+0x2FF' defaults ('+0x18' = 0x1000404, '+0x1C' = 0x6C2B0000, floats 457FA000/4B7FFF28) - the module record's init.  Interior anchor '004FD08"

```
004F7070  mov      rax, rsp
004F7073  mov      qword ptr [rax + 0x18], rbx
004F7077  mov      qword ptr [rax + 0x20], rbp
004F707B  push     rsi
004F707C  push     rdi
004F707D  push     r12
004F707F  push     r14
004F7081  push     r15
004F7083  sub      rsp, 0x200
004F708A  movaps   xmmword ptr [rax - 0x38], xmm6
004F708E  movaps   xmmword ptr [rax - 0x48], xmm7
004F7092  movaps   xmmword ptr [rax - 0x58], xmm8
004F7097  movaps   xmmword ptr [rax - 0x68], xmm9
004F709C  movaps   xmmword ptr [rax - 0x78], xmm10
004F70A1  movaps   xmmword ptr [rax - 0x88], xmm11
004F70A9  movaps   xmmword ptr [rax - 0x98], xmm12
004F70B1  movaps   xmmword ptr [rax - 0xa8], xmm13
004F70B9  movaps   xmmword ptr [rax - 0xb8], xmm14
004F70C1  movaps   xmmword ptr [rax - 0xc8], xmm15
004F70C9  mov      rax, qword ptr [rip + 0x1a4d760]  ; -> 01F44830 [u64 0x00002B992DDFA232]
004F70D0  xor      rax, rsp
004F70D3  mov      qword ptr [rsp + 0x150], rax
004F70DB  movsx    ebx, word ptr [rip + 0x1b6da2a]  ; -> 02064B0C
004F70E2  lea      r15, [rip + 0x1b6dd47]  ; -> 02064E30
004F70E9  movss    xmm6, dword ptr [rip + 0x190b74b]  ; -> 01E0283C [f32 1]
004F70F1  mov      rbp, rcx
004F70F4  movss    xmm12, dword ptr [rip + 0x409263]  ; -> 00900360 [u32 0x7F7FFFFF]
004F70FD  movaps   xmm7, xmm6
004F7100  xorps    xmm11, xmm11
004F7104  mov      word ptr [rip + 0x1b6dcad], bx  ; -> 02064DB8
004F710B  lea      eax, [rbx + 9]
004F710E  mov      word ptr [rip + 0x1b6dcbb], bx  ; -> 02064DD0
004F7115  shl      eax, 4
004F7118  mov      r14, rdx
004F711B  movsxd   r8, eax
004F711E  mov      r9d, ebx
004F7121  mov      eax, 0x168
004F7126  mov      dword ptr [rip + 0x1b6d9d4], 0x40000000  ; -> 02064B04
004F7130  add      eax, ebx
004F7132  mov      word ptr [rip + 0x1b6dc77], ax  ; -> 02064DB0
004F7139  inc      ax
004F713C  movups   xmm1, xmmword ptr [r8 + r15]
004F7141  mov      word ptr [rip + 0x1b6dc6c], ax  ; -> 02064DB4
004F7148  mov      eax, ebx
004F714A  shl      eax, 4
004F714D  movups   xmmword ptr [rip + 0x1b6da1c], xmm1  ; -> 02064B70
004F7154  movsxd   rcx, eax
004F7157  shufps   xmm1, xmm1, 0xaa
004F715B  addss    xmm1, dword ptr [rip + 0x190b6cd]  ; -> 01E02830 [u32 0x00000000]
004F7163  movzx    eax, word ptr [rcx + r15 + 0xc]
004F7169  mov      word ptr [rip + 0x1b6dc64], ax  ; -> 02064DD4
004F7170  lea      eax, [rbx + 0x33]
004F7173  mov      word ptr [rip + 0x1b6dc5e], ax  ; -> 02064DD8
004F717A  subss    xmm7, xmm1
004F717E  mulss    xmm1, dword ptr [rip + 0x17f4a82]  ; -> 01CEBC08 [f32 2]
004F7186  ucomiss  xmm1, xmm11
004F718A  mulss    xmm7, dword ptr [rip + 0x17f4a76]  ; -> 01CEBC08 [f32 2]
004F7192  movss    dword ptr [rip + 0x1b6d9c6], xmm1  ; -> 02064B60
004F719A  movss    dword ptr [rip + 0x1b6d9ca], xmm7  ; -> 02064B6C
004F71A2  jp       0x4f71b5  ; -> 004F71B5
004F71A4  jne      0x4f71b5  ; -> 004F71B5
004F71A6  movss    dword ptr [rip + 0x1b6d951], xmm12  ; -> 02064B00
004F71AF  movaps   xmm8, xmm12
004F71B3  jmp      0x4f71c7  ; -> 004F71C7
004F71B5  movaps   xmm8, xmm6
004F71B9  divss    xmm8, xmm1
004F71BE  movss    dword ptr [rip + 0x1b6d939], xmm8  ; -> 02064B00
004F71C7  lea      eax, [r9 + 0xe]
004F71CB  shl      eax, 4
004F71CE  movsxd   rcx, eax
004F71D1  lea      eax, [r9 + 0xf]
004F71D5  shl      eax, 4
004F71D8  movups   xmm1, xmmword ptr [rcx + r15]
004F71DD  movsxd   rcx, eax
004F71E0  lea      eax, [r9 + 0x10]
004F71E4  shl      eax, 4
004F71E7  cvtdq2ps xmm1, xmm1
004F71EA  movups   xmm2, xmmword ptr [rcx + r15]
004F71EF  movsxd   rcx, eax
004F71F2  lea      eax, [r9 + 0x11]
004F71F6  shl      eax, 4
004F71F9  movups   xmmword ptr [rip + 0x1b6d9c0], xmm1  ; -> 02064BC0
004F7200  movups   xmm3, xmmword ptr [rcx + r15]
004F7205  movsxd   rcx, eax
004F7208  lea      eax, [r9 + 0x12]
004F720C  shl      eax, 4
004F720F  cvtdq2ps xmm1, xmm2
004F7212  movups   xmm0, xmmword ptr [rcx + r15]
004F7217  movsxd   rcx, eax
004F721A  lea      eax, [r9 + 0x13]
004F721E  shl      eax, 4
004F7221  movups   xmmword ptr [rip + 0x1b6d9a8], xmm1  ; -> 02064BD0
004F7228  movups   xmm5, xmmword ptr [rcx + r15]
004F722D  movsxd   rcx, eax
004F7230  lea      eax, [r9 + 0x14]
004F7234  shl      eax, 4
004F7237  cvtdq2ps xmm1, xmm3
004F723A  movups   xmm2, xmmword ptr [rcx + r15]
004F723F  movsxd   rcx, eax
004F7242  lea      eax, [r9 + 0x15]
004F7246  shl      eax, 4
004F7249  movups   xmmword ptr [rip + 0x1b6d990], xmm1  ; -> 02064BE0
004F7250  movups   xmm3, xmmword ptr [rcx + r15]
004F7255  movsxd   rcx, eax
004F7258  lea      eax, [r9 + 0x16]
004F725C  cvtdq2ps xmm1, xmm0
004F725F  shl      eax, 4
004F7262  movups   xmm0, xmmword ptr [rcx + r15]
004F7267  movsxd   rcx, eax
004F726A  lea      eax, [r9 + 0x17]
004F726E  movups   xmmword ptr [rip + 0x1b6d97b], xmm1  ; -> 02064BF0
004F7275  shl      eax, 4
004F7278  movups   xmmword ptr [rip + 0x1b6d9b1], xmm0  ; -> 02064C30
004F727F  movups   xmm0, xmmword ptr [rcx + r15]
004F7284  movsxd   rcx, eax
004F7287  lea      eax, [r9 + 0x18]
004F728B  cvtdq2ps xmm1, xmm5
004F728E  shl      eax, 4
004F7291  movups   xmmword ptr [rip + 0x1b6d9a8], xmm0  ; -> 02064C40
004F7298  movups   xmm0, xmmword ptr [rcx + r15]
004F729D  movsxd   rcx, eax
004F72A0  movups   xmmword ptr [rip + 0x1b6d959], xmm1  ; -> 02064C00
004F72A7  cvtdq2ps xmm1, xmm2
004F72AA  movups   xmmword ptr [rip + 0x1b6d99f], xmm0  ; -> 02064C50
004F72B1  movups   xmm0, xmmword ptr [rcx + r15]
004F72B6  movups   xmmword ptr [rip + 0x1b6d953], xmm1  ; -> 02064C10
004F72BD  cvtdq2ps xmm1, xmm3
004F72C0  movups   xmmword ptr [rip + 0x1b6d999], xmm0  ; -> 02064C60
004F72C7  movups   xmmword ptr [rip + 0x1b6d952], xmm1  ; -> 02064C20
004F72CE  movss    xmm1, dword ptr [rip + 0x190b562]  ; -> 01E02838 [u32 0x00000000]
004F72D6  addss    xmm1, xmm8
004F72DB  ucomiss  xmm1, xmm11
004F72DF  movss    dword ptr [rip + 0x1b6d881], xmm1  ; -> 02064B68
004F72E7  jp       0x4f730f  ; -> 004F730F
004F72E9  jne      0x4f730f  ; -> 004F730F
004F72EB  call     0x22cc40  ; -> 0022CC40 fn
004F72F0  movss    xmm1, dword ptr [rip + 0x1b6d870]  ; -> 02064B68
004F72F8  movzx    ebx, word ptr [rip + 0x1b6d80d]  ; -> 02064B0C
004F72FF  movss    xmm7, dword ptr [rip + 0x1b6d865]  ; -> 02064B6C
004F7307  movss    xmm6, dword ptr [rip + 0x190b52d]  ; -> 01E0283C [f32 1]
004F730F  comiss   xmm11, xmm1
004F7313  jbe      0x4f7331  ; -> 004F7331
004F7315  call     0x22cc30  ; -> 0022CC30 fn
004F731A  movzx    ebx, word ptr [rip + 0x1b6d7eb]  ; -> 02064B0C
004F7321  movss    xmm7, dword ptr [rip + 0x1b6d843]  ; -> 02064B6C
004F7329  movss    xmm6, dword ptr [rip + 0x190b50b]  ; -> 01E0283C [f32 1]
004F7331  ucomiss  xmm7, xmm11
004F7335  jp       0x4f733f  ; -> 004F733F
004F7337  jne      0x4f733f  ; -> 004F733F
004F7339  movaps   xmm8, xmm12
004F733D  jmp      0x4f7350  ; -> 004F7350
004F733F  movaps   xmm8, xmm6
004F7343  divss    xmm8, xmm7
004F7348  nop      dword ptr [rax + rax]
004F7350  movups   xmm5, xmmword ptr [rip + 0x1b6d869]  ; -> 02064BC0
004F7357  movdqu   xmm0, xmmword ptr [rip + 0x1b6d8d1]  ; -> 02064C30
004F735F  mulps    xmm5, xmmword ptr [rip + 0x82b3aa]  ; -> 00D22710 [f32x4 0.0078125, 0.0078125, 0.0078125, 0.0078125]
004F7366  cvtdq2ps xmm9, xmm0
004F736A  movups   xmm0, xmmword ptr [rip + 0x1b6d85f]  ; -> 02064BD0
004F7371  movdqu   xmmword ptr [rip + 0x1b6d847], xmm5  ; -> 02064BC0
004F7379  mulps    xmm0, xmmword ptr [rip + 0x82b390]  ; -> 00D22710 [f32x4 0.0078125, 0.0078125, 0.0078125, 0.0078125]
004F7380  movaps   xmm1, xmm5
004F7383  mulss    xmm1, dword ptr [rip + 0x1b6d865]  ; -> 02064BF0
004F738B  movaps   xmm4, xmm5
004F738E  shufps   xmm4, xmm5, 0x55
004F7392  movaps   xmm3, xmm5
004F7395  movups   xmmword ptr [rip + 0x1b6d834], xmm0  ; -> 02064BD0
004F739C  movdqu   xmm0, xmmword ptr [rip + 0x1b6d89c]  ; -> 02064C40
004F73A4  movss    dword ptr [rip + 0x1b6d8d4], xmm1  ; -> 02064C80
004F73AC  movaps   xmm2, xmm5
004F73AF  cvtdq2ps xmm10, xmm0
004F73B3  movdqu   xmm0, xmmword ptr [rip + 0x1b6d895]  ; -> 02064C50
004F73BB  shufps   xmm3, xmm5, 0xaa
004F73BF  cvtdq2ps xmm13, xmm0
004F73C3  movdqu   xmm0, xmmword ptr [rip + 0x1b6d895]  ; -> 02064C60
004F73CB  shufps   xmm2, xmm5, 0xff
004F73CF  movaps   xmm1, xmm3
004F73D2  mulss    xmm1, dword ptr [rip + 0x1b6d81e]  ; -> 02064BF8
004F73DA  cvtdq2ps xmm14, xmm0
004F73DE  movaps   xmm0, xmm5
004F73E1  movss    dword ptr [rip + 0x1b6d7d7], xmm5  ; -> 02064BC0
004F73E9  mulss    xmm0, dword ptr [rip + 0x1b6d7ef]  ; -> 02064BE0
004F73F1  movss    dword ptr [rip + 0x1b6d88f], xmm1  ; -> 02064C88
004F73F9  movaps   xmm1, xmm5
004F73FC  mulss    xmm1, dword ptr [rip + 0x1b6d7fc]  ; -> 02064C00
004F7404  movss    dword ptr [rip + 0x1b6d864], xmm0  ; -> 02064C70
004F740C  movaps   xmm0, xmm4
004F740F  mulss    xmm0, dword ptr [rip + 0x1b6d7cd]  ; -> 02064BE4
004F7417  movss    dword ptr [rip + 0x1b6d871], xmm1  ; -> 02064C90
004F741F  movaps   xmm1, xmm3
004F7422  mulss    xmm1, dword ptr [rip + 0x1b6d7de]  ; -> 02064C08
004F742A  movss    dword ptr [rip + 0x1b6d842], xmm0  ; -> 02064C74
004F7432  movaps   xmm0, xmm3
004F7435  mulss    xmm0, dword ptr [rip + 0x1b6d7ab]  ; -> 02064BE8
004F743D  movss    dword ptr [rip + 0x1b6d853], xmm1  ; -> 02064C98
004F7445  movaps   xmm1, xmm5
004F7448  mulss    xmm1, dword ptr [rip + 0x1b6d7c0]  ; -> 02064C10
004F7450  movss    dword ptr [rip + 0x1b6d820], xmm0  ; -> 02064C78
004F7458  movaps   xmm0, xmm2
004F745B  mulss    xmm0, dword ptr [rip + 0x1b6d789]  ; -> 02064BEC
004F7463  movss    dword ptr [rip + 0x1b6d835], xmm1  ; -> 02064CA0
004F746B  movaps   xmm1, xmm3
004F746E  mulss    xmm1, dword ptr [rip + 0x1b6d7a2]  ; -> 02064C18
004F7476  movss    dword ptr [rip + 0x1b6d7fe], xmm0  ; -> 02064C7C
004F747E  movaps   xmm0, xmm4
004F7481  mulss    xmm0, dword ptr [rip + 0x1b6d76b]  ; -> 02064BF4
004F7489  movss    dword ptr [rip + 0x1b6d817], xmm1  ; -> 02064CA8
004F7491  movaps   xmm1, xmm5
004F7494  mulss    xmm1, dword ptr [rip + 0x1b6d784]  ; -> 02064C20
004F749C  movss    dword ptr [rip + 0x1b6d7e0], xmm0  ; -> 02064C84
004F74A4  movaps   xmm0, xmm2
004F74A7  mulss    xmm0, dword ptr [rip + 0x1b6d74d]  ; -> 02064BFC
004F74AF  movss    dword ptr [rip + 0x1b6d70d], xmm4  ; -> 02064BC4
004F74B7  movss    dword ptr [rip + 0x1b6d709], xmm3  ; -> 02064BC8
004F74BF  movss    dword ptr [rip + 0x1b6d7c5], xmm0  ; -> 02064C8C
004F74C7  movaps   xmm0, xmm4
004F74CA  mulss    xmm0, dword ptr [rip + 0x1b6d732]  ; -> 02064C04
004F74D2  movss    dword ptr [rip + 0x1b6d6f2], xmm2  ; -> 02064BCC
004F74DA  movss    dword ptr [rip + 0x1b6d7ce], xmm1  ; -> 02064CB0
004F74E2  movss    dword ptr [rip + 0x1b6d7aa], xmm0  ; -> 02064C94
004F74EA  movaps   xmm0, xmm2
004F74ED  mulss    xmm0, dword ptr [rip + 0x1b6d717]  ; -> 02064C0C
004F74F5  movdqu   xmmword ptr [rip + 0x1b6d732], xmm9  ; -> 02064C30
004F74FE  movss    dword ptr [rip + 0x1b6d796], xmm0  ; -> 02064C9C
004F7506  movaps   xmm0, xmm4
004F7509  mulss    xmm0, dword ptr [rip + 0x1b6d703]  ; -> 02064C14
004F7511  movdqu   xmmword ptr [rip + 0x1b6d726], xmm10  ; -> 02064C40
004F751A  movss    dword ptr [rip + 0x1b6d782], xmm0  ; -> 02064CA4
004F7522  movaps   xmm0, xmm2
004F7525  mulss    xmm0, dword ptr [rip + 0x1b6d6ef]  ; -> 02064C1C
004F752D  movdqu   xmmword ptr [rip + 0x1b6d71a], xmm13  ; -> 02064C50
004F7536  movss    dword ptr [rip + 0x1b6d76e], xmm0  ; -> 02064CAC
004F753E  movaps   xmm0, xmm4
004F7541  mulss    xmm0, dword ptr [rip + 0x1b6d6db]  ; -> 02064C24
004F7549  movdqu   xmmword ptr [rip + 0x1b6d70e], xmm14  ; -> 02064C60
004F7552  movss    dword ptr [rip + 0x1b6d75a], xmm0  ; -> 02064CB4
004F755A  movaps   xmm1, xmm3
004F755D  mulss    xmm1, dword ptr [rip + 0x1b6d6c3]  ; -> 02064C28
004F7565  movaps   xmm0, xmm2
004F7568  movsx    edx, bx
004F756B  mulss    xmm0, dword ptr [rip + 0x1b6d6b9]  ; -> 02064C2C
004F7573  movaps   xmm15, xmm9
004F7577  movss    dword ptr [rip + 0x1b6d739], xmm1  ; -> 02064CB8
004F757F  movaps   xmm1, xmm5
004F7582  mulss    xmm1, xmm9
004F7587  lea      eax, [rdx + 0x2c]
004F758A  shl      eax, 4
004F758D  movss    dword ptr [rip + 0x1b6d727], xmm0  ; -> 02064CBC
004F7595  movups   xmm0, xmmword ptr [rip + 0x1b6d6d4]  ; -> 02064C70
004F759C  movsxd   rcx, eax
004F759F  lea      eax, [rdx + 0x2d]
004F75A2  movss    dword ptr [rip + 0x1b6d716], xmm1  ; -> 02064CC0
004F75AA  movaps   xmm1, xmm3
004F75AD  shl      eax, 4
004F75B0  shufps   xmm15, xmm9, 0x55
004F75B5  movups   xmmword ptr [rcx + r15], xmm0
004F75BA  movsxd   rcx, eax
004F75BD  lea      eax, [rdx + 0x2e]
004F75C0  movaps   xmm0, xmm4
004F75C3  shl      eax, 4
004F75C6  mulss    xmm0, xmm15
004F75CB  movss    dword ptr [rip + 0x1b6d65c], xmm9  ; -> 02064C30
004F75D4  movss    dword ptr [rip + 0x1b6d657], xmm15  ; -> 02064C34
004F75DD  movss    dword ptr [rip + 0x1b6d6df], xmm0  ; -> 02064CC4
004F75E5  movaps   xmm0, xmm9
004F75E9  shufps   xmm0, xmm9, 0xaa
004F75EE  mulss    xmm1, xmm0
004F75F2  movss    dword ptr [rip + 0x1b6d63e], xmm0  ; -> 02064C38
004F75FA  movaps   xmmword ptr [rsp + 0x100], xmm0
004F7602  movaps   xmm0, xmm2
004F7605  movss    dword ptr [rip + 0x1b6d6bb], xmm1  ; -> 02064CC8
004F760D  movaps   xmm1, xmm9
004F7611  shufps   xmm1, xmm9, 0xff
004F7616  mulss    xmm0, xmm1
004F761A  movss    dword ptr [rip + 0x1b6d61a], xmm1  ; -> 02064C3C
004F7622  movaps   xmmword ptr [rsp + 0xf0], xmm1
004F762A  movaps   xmm1, xmm5
004F762D  mulss    xmm1, xmm10
004F7632  movss    dword ptr [rip + 0x1b6d692], xmm0  ; -> 02064CCC
004F763A  movups   xmm0, xmmword ptr [rip + 0x1b6d63f]  ; -> 02064C80
004F7641  movss    dword ptr [rip + 0x1b6d687], xmm1  ; -> 02064CD0
004F7649  movaps   xmm1, xmm10
004F764D  shufps   xmm1, xmm10, 0x55
004F7652  movups   xmmword ptr [rcx + r15], xmm0
004F7657  movsxd   rcx, eax
004F765A  movss    dword ptr [rip + 0x1b6d5e2], xmm1  ; -> 02064C44
004F7662  movaps   xmm0, xmm4
004F7665  mulss    xmm0, xmm1
004F7669  movaps   xmmword ptr [rsp + 0xe0], xmm1
004F7671  movaps   xmm1, xmm3
004F7674  movss    dword ptr [rip + 0x1b6d5c3], xmm10  ; -> 02064C40
004F767D  movss    dword ptr [rip + 0x1b6d64f], xmm0  ; -> 02064CD4
004F7685  movaps   xmm0, xmm10
004F7689  shufps   xmm0, xmm10, 0xaa
004F768E  mulss    xmm1, xmm0
004F7692  movss    dword ptr [rip + 0x1b6d5ae], xmm0  ; -> 02064C48
004F769A  movaps   xmmword ptr [rsp + 0xd0], xmm0
004F76A2  movaps   xmm0, xmm2
004F76A5  movss    dword ptr [rip + 0x1b6d62b], xmm1  ; -> 02064CD8
004F76AD  movaps   xmm1, xmm10
004F76B1  shufps   xmm1, xmm10, 0xff
004F76B6  mulss    xmm0, xmm1
004F76BA  movss    dword ptr [rip + 0x1b6d58a], xmm1  ; -> 02064C4C
004F76C2  movaps   xmmword ptr [rsp + 0xc0], xmm1
004F76CA  movaps   xmm1, xmm5
004F76CD  mulss    xmm1, xmm13
004F76D2  movss    dword ptr [rip + 0x1b6d602], xmm0  ; -> 02064CDC
004F76DA  movups   xmm0, xmmword ptr [rip + 0x1b6d5af]  ; -> 02064C90
004F76E1  movss    dword ptr [rip + 0x1b6d5f7], xmm1  ; -> 02064CE0
004F76E9  movaps   xmm1, xmm13
004F76ED  shufps   xmm1, xmm13, 0x55
004F76F2  movups   xmmword ptr [rcx + r15], xmm0
004F76F7  movss    dword ptr [rip + 0x1b6d555], xmm1  ; -> 02064C54
004F76FF  movaps   xmm0, xmm4
004F7702  movaps   xmmword ptr [rsp + 0xb0], xmm1
004F770A  movss    dword ptr [rip + 0x1b6d53d], xmm13  ; -> 02064C50
004F7713  mulss    xmm0, xmm1
004F7717  lea      eax, [rdx + 0x2f]
004F771A  shl      eax, 4
004F771D  movsxd   rcx, eax
004F7720  movaps   xmm1, xmm3
004F7723  lea      eax, [rdx + 0x30]
004F7726  mulss    xmm8, xmm6
004F772B  shl      eax, 4
004F772E  movss    dword ptr [rip + 0x1b6d5ae], xmm0  ; -> 02064CE4
004F7736  movaps   xmm7, xmm6
004F7739  movaps   xmm0, xmm13
004F773D  mulss    xmm5, xmm14
004F7742  mov      dword ptr [rip + 0x1b6d3b8], 0x40000000  ; -> 02064B04
004F774C  shufps   xmm0, xmm13, 0xaa
004F7751  mulss    xmm1, xmm0
004F7755  movss    dword ptr [rip + 0x1b6d4fb], xmm0  ; -> 02064C58
004F775D  movaps   xmmword ptr [rsp + 0xa0], xmm0
004F7765  movaps   xmm0, xmm2
004F7768  movss    dword ptr [rip + 0x1b6d578], xmm1  ; -> 02064CE8
004F7770  movaps   xmm1, xmm13
004F7774  shufps   xmm1, xmm13, 0xff
004F7779  mulss    xmm0, xmm1
004F777D  movss    dword ptr [rip + 0x1b6d4d7], xmm1  ; -> 02064C5C
004F7785  movaps   xmmword ptr [rsp + 0x90], xmm1
004F778D  movss    xmm1, dword ptr [rip + 0x190b09b]  ; -> 01E02830 [u32 0x00000000]
004F7795  addss    xmm1, dword ptr [rip + 0x1b6d3df]  ; -> 02064B7C
004F779D  movss    dword ptr [rip + 0x1b6d547], xmm0  ; -> 02064CEC
004F77A5  movups   xmm0, xmmword ptr [rip + 0x1b6d4f4]  ; -> 02064CA0
004F77AC  movss    dword ptr [rip + 0x1b6d3b7], xmm8  ; -> 02064B6C
004F77B5  movups   xmmword ptr [rcx + r15], xmm0
004F77BA  movsxd   rcx, eax
004F77BD  lea      eax, [rdx + 0x40]
004F77C0  subss    xmm7, xmm1
004F77C4  shl      eax, 4
004F77C7  mulss    xmm1, dword ptr [rip + 0x17f4439]  ; -> 01CEBC08 [f32 2]
004F77CF  movaps   xmm0, xmm14
004F77D3  shufps   xmm0, xmm14, 0x55
004F77D8  mulss    xmm4, xmm0
004F77DC  ucomiss  xmm1, xmm11
004F77E0  mulss    xmm7, dword ptr [rip + 0x17f4420]  ; -> 01CEBC08 [f32 2]
004F77E8  movss    dword ptr [rip + 0x1b6d474], xmm0  ; -> 02064C64
004F77F0  movaps   xmmword ptr [rsp + 0x80], xmm0
004F77F8  movaps   xmm0, xmm14
004F77FC  shufps   xmm0, xmm14, 0xaa
004F7801  mulss    xmm3, xmm0
004F7805  movss    dword ptr [rip + 0x1b6d45b], xmm0  ; -> 02064C68
004F780D  movaps   xmmword ptr [rsp + 0x50], xmm0
004F7812  movaps   xmm0, xmm14
004F7816  shufps   xmm0, xmm14, 0xff
004F781B  mulss    xmm2, xmm0
004F781F  movss    dword ptr [rip + 0x1b6d445], xmm0  ; -> 02064C6C
004F7827  movaps   xmmword ptr [rsp + 0x40], xmm0
004F782C  movups   xmm0, xmmword ptr [rip + 0x1b6d47d]  ; -> 02064CB0
004F7833  movss    dword ptr [rip + 0x1b6d424], xmm14  ; -> 02064C60
004F783C  movups   xmmword ptr [rcx + r15], xmm0
004F7841  movsxd   rcx, eax
004F7844  movups   xmm0, xmmword ptr [rip + 0x1b6d315]  ; -> 02064B60
004F784B  movss    dword ptr [rip + 0x1b6d49d], xmm5  ; -> 02064CF0
004F7853  movups   xmmword ptr [rcx + r15], xmm0
004F7858  movss    dword ptr [rip + 0x1b6d494], xmm4  ; -> 02064CF4
004F7860  movss    dword ptr [rip + 0x1b6d490], xmm3  ; -> 02064CF8
004F7868  movss    dword ptr [rip + 0x1b6d48c], xmm2  ; -> 02064CFC
004F7870  movss    dword ptr [rip + 0x1b6d2e8], xmm1  ; -> 02064B60
004F7878  movss    dword ptr [rip + 0x1b6d2ec], xmm7  ; -> 02064B6C
004F7880  jp       0x4f7893  ; -> 004F7893
004F7882  jne      0x4f7893  ; -> 004F7893
004F7884  movss    dword ptr [rip + 0x1b6d273], xmm12  ; -> 02064B00
004F788D  movaps   xmm8, xmm12
004F7891  jmp      0x4f78a5  ; -> 004F78A5
004F7893  movaps   xmm8, xmm6
004F7897  divss    xmm8, xmm1
004F789C  movss    dword ptr [rip + 0x1b6d25b], xmm8  ; -> 02064B00
004F78A5  movss    xmm5, dword ptr [rip + 0x1b6d323]  ; -> 02064BD0
004F78AD  lea      eax, [rdx + 0x31]
004F78B0  movss    xmm2, dword ptr [rip + 0x1b6d320]  ; -> 02064BD8
004F78B8  movaps   xmm0, xmm5
004F78BB  mulss    xmm0, dword ptr [rip + 0x1b6d31d]  ; -> 02064BE0
004F78C3  shl      eax, 4
004F78C6  movss    xmm4, dword ptr [rip + 0x1b6d306]  ; -> 02064BD4
004F78CE  movss    xmm3, dword ptr [rip + 0x1b6d306]  ; -> 02064BDC
004F78D6  movaps   xmm1, xmm4
004F78D9  mulss    xmm1, dword ptr [rip + 0x1b6d303]  ; -> 02064BE4
004F78E1  movsxd   rcx, eax
004F78E4  lea      eax, [rdx + 0x32]
004F78E7  movss    dword ptr [rip + 0x1b6d381], xmm0  ; -> 02064C70
004F78EF  movaps   xmm0, xmm2
004F78F2  mulss    xmm0, dword ptr [rip + 0x1b6d2ee]  ; -> 02064BE8
004F78FA  shl      eax, 4
004F78FD  movss    dword ptr [rip + 0x1b6d36f], xmm1  ; -> 02064C74
004F7905  movaps   xmm1, xmm3
004F7908  mulss    xmm1, dword ptr [rip + 0x1b6d2dc]  ; -> 02064BEC
004F7910  movss    dword ptr [rip + 0x1b6d360], xmm0  ; -> 02064C78
004F7918  movups   xmm0, xmmword ptr [rip + 0x1b6d3a1]  ; -> 02064CC0
004F791F  movss    dword ptr [rip + 0x1b6d355], xmm1  ; -> 02064C7C
004F7927  movaps   xmm1, xmm5
004F792A  mulss    xmm1, dword ptr [rip + 0x1b6d2be]  ; -> 02064BF0
004F7932  movups   xmmword ptr [rcx + r15], xmm0
004F7937  movsxd   rcx, eax
004F793A  lea      eax, [rdx + 0x33]
004F793D  movss    dword ptr [rip + 0x1b6d33b], xmm1  ; -> 02064C80
004F7945  movaps   xmm0, xmm4
004F7948  mulss    xmm0, dword ptr [rip + 0x1b6d2a4]  ; -> 02064BF4
004F7950  movaps   xmm1, xmm2
004F7953  shl      eax, 4
004F7956  mulss    xmm1, dword ptr [rip + 0x1b6d29a]  ; -> 02064BF8
004F795E  movss    dword ptr [rip + 0x1b6d31e], xmm0  ; -> 02064C84
004F7966  movaps   xmm0, xmm3
004F7969  mulss    xmm0, dword ptr [rip + 0x1b6d28b]  ; -> 02064BFC
004F7971  movss    dword ptr [rip + 0x1b6d30f], xmm1  ; -> 02064C88
004F7979  movaps   xmm1, xmm5
004F797C  mulss    xmm1, dword ptr [rip + 0x1b6d27c]  ; -> 02064C00
004F7984  movss    dword ptr [rip + 0x1b6d300], xmm0  ; -> 02064C8C
004F798C  movups   xmm0, xmmword ptr [rip + 0x1b6d33d]  ; -> 02064CD0
004F7993  movss    dword ptr [rip + 0x1b6d2f5], xmm1  ; -> 02064C90
004F799B  movaps   xmm1, xmm2
004F799E  mulss    xmm1, dword ptr [rip + 0x1b6d262]  ; -> 02064C08
004F79A6  movups   xmmword ptr [rcx + r15], xmm0
004F79AB  movsxd   rcx, eax
004F79AE  lea      eax, [rdx + 0x34]
004F79B1  movss    dword ptr [rip + 0x1b6d2df], xmm1  ; -> 02064C98
004F79B9  movaps   xmm0, xmm4
004F79BC  mulss    xmm0, dword ptr [rip + 0x1b6d240]  ; -> 02064C04
004F79C4  movaps   xmm1, xmm5
004F79C7  shl      eax, 4
004F79CA  mulss    xmm1, dword ptr [rip + 0x1b6d23e]  ; -> 02064C10
004F79D2  movss    dword ptr [rip + 0x1b6d2ba], xmm0  ; -> 02064C94
004F79DA  movaps   xmm0, xmm3
004F79DD  mulss    xmm0, dword ptr [rip + 0x1b6d227]  ; -> 02064C0C
004F79E5  movss    dword ptr [rip + 0x1b6d2b3], xmm1  ; -> 02064CA0
004F79ED  movaps   xmm1, xmm5
004F79F0  mulss    xmm1, dword ptr [rip + 0x1b6d228]  ; -> 02064C20
004F79F8  movss    dword ptr [rip + 0x1b6d29c], xmm0  ; -> 02064C9C
004F7A00  movups   xmm0, xmmword ptr [rip + 0x1b6d2d9]  ; -> 02064CE0
004F7A07  movss    dword ptr [rip + 0x1b6d2a1], xmm1  ; -> 02064CB0
004F7A0F  movups   xmmword ptr [rcx + r15], xmm0
004F7A14  movsxd   rcx, eax
004F7A17  movss    xmm0, dword ptr [rip + 0x1b6d1f5]  ; -> 02064C14
004F7A1F  mulss    xmm0, xmm4
004F7A23  movss    dword ptr [rip + 0x1b6d279], xmm0  ; -> 02064CA4
004F7A2B  movss    xmm0, dword ptr [rip + 0x1b6d1e5]  ; -> 02064C18
004F7A33  mulss    xmm0, xmm2
004F7A37  movss    dword ptr [rip + 0x1b6d269], xmm0  ; -> 02064CA8
004F7A3F  movaps   xmm0, xmm3
004F7A42  mulss    xmm0, dword ptr [rip + 0x1b6d1d2]  ; -> 02064C1C
004F7A4A  movss    dword ptr [rip + 0x1b6d25a], xmm0  ; -> 02064CAC
004F7A52  movups   xmm0, xmmword ptr [rip + 0x1b6d297]  ; -> 02064CF0
004F7A59  movups   xmmword ptr [rcx + r15], xmm0
004F7A5E  movss    xmm0, dword ptr [rip + 0x1b6d1be]  ; -> 02064C24
004F7A66  mulss    xmm0, xmm4
004F7A6A  movss    dword ptr [rip + 0x1b6d242], xmm0  ; -> 02064CB4
004F7A72  movss    xmm0, dword ptr [rip + 0x1b6d1ae]  ; -> 02064C28
004F7A7A  mulss    xmm0, xmm2
004F7A7E  movss    dword ptr [rip + 0x1b6d232], xmm0  ; -> 02064CB8
004F7A86  movaps   xmm0, xmm3
004F7A89  mulss    xmm15, xmm4
004F7A8E  lea      eax, [rdx + 0x35]
004F7A91  mulss    xmm0, dword ptr [rip + 0x1b6d193]  ; -> 02064C2C
004F7A99  movaps   xmm1, xmm5
004F7A9C  shl      eax, 4
004F7A9F  movsxd   rcx, eax
004F7AA2  lea      eax, [rdx + 0x36]
004F7AA5  shl      eax, 4
004F7AA8  movss    dword ptr [rip + 0x1b6d20c], xmm0  ; -> 02064CBC
004F7AB0  movups   xmm0, xmmword ptr [rip + 0x1b6d1b9]  ; -> 02064C70
004F7AB7  mulss    xmm1, xmm9
004F7ABC  movups   xmmword ptr [rcx + r15], xmm0
004F7AC1  movsxd   rcx, eax
004F7AC4  lea      eax, [rdx + 0x37]
004F7AC7  movaps   xmm0, xmmword ptr [rsp + 0x100]
004F7ACF  mulss    xmm0, xmm2
004F7AD3  shl      eax, 4
004F7AD6  movss    dword ptr [rip + 0x1b6d1e2], xmm1  ; -> 02064CC0
004F7ADE  movaps   xmm1, xmm5
004F7AE1  mulss    xmm1, xmm10
004F7AE6  movss    dword ptr [rip + 0x1b6d1da], xmm0  ; -> 02064CC8
004F7AEE  movaps   xmm0, xmm3
004F7AF1  mulss    xmm0, dword ptr [rsp + 0xf0]
004F7AFA  movss    dword ptr [rip + 0x1b6d1ce], xmm1  ; -> 02064CD0
004F7B02  movaps   xmm1, xmmword ptr [rsp + 0xd0]
004F7B0A  movss    dword ptr [rip + 0x1b6d1ba], xmm0  ; -> 02064CCC
004F7B12  movups   xmm0, xmmword ptr [rip + 0x1b6d167]  ; -> 02064C80
004F7B19  mulss    xmm1, xmm2
004F7B1D  movups   xmmword ptr [rcx + r15], xmm0
004F7B22  movsxd   rcx, eax
004F7B25  lea      eax, [rdx + 0x38]
004F7B28  movaps   xmm0, xmmword ptr [rsp + 0xe0]
004F7B30  mulss    xmm0, xmm4
004F7B34  shl      eax, 4
004F7B37  movss    dword ptr [rip + 0x1b6d199], xmm1  ; -> 02064CD8
004F7B3F  movaps   xmm1, xmm5
004F7B42  mulss    xmm1, xmm13
004F7B47  movss    dword ptr [rip + 0x1b6d185], xmm0  ; -> 02064CD4
004F7B4F  movaps   xmm0, xmm3
004F7B52  mulss    xmm0, dword ptr [rsp + 0xc0]
004F7B5B  movss    dword ptr [rip + 0x1b6d17d], xmm1  ; -> 02064CE0
004F7B63  movaps   xmm1, xmmword ptr [rsp + 0xa0]
004F7B6B  movss    dword ptr [rip + 0x1b6d169], xmm0  ; -> 02064CDC
004F7B73  movups   xmm0, xmmword ptr [rip + 0x1b6d116]  ; -> 02064C90
004F7B7A  mulss    xmm1, xmm2
004F7B7E  movups   xmmword ptr [rcx + r15], xmm0
004F7B83  movsxd   rcx, eax
004F7B86  lea      eax, [rdx + 0x39]
004F7B89  movaps   xmm0, xmmword ptr [rsp + 0xb0]
004F7B91  mulss    xmm0, xmm4
004F7B95  shl      eax, 4
004F7B98  movss    dword ptr [rip + 0x1b6d148], xmm1  ; -> 02064CE8
004F7BA0  movaps   xmm1, xmmword ptr [rsp + 0x50]
004F7BA5  movss    dword ptr [rip + 0x1b6d137], xmm0  ; -> 02064CE4
004F7BAD  movaps   xmm0, xmm3
004F7BB0  mulss    xmm0, dword ptr [rsp + 0x90]
004F7BB9  mulss    xmm3, dword ptr [rsp + 0x40]
004F7BBF  movss    dword ptr [rip + 0x1b6d125], xmm0  ; -> 02064CEC
004F7BC7  movups   xmm0, xmmword ptr [rip + 0x1b6d0d2]  ; -> 02064CA0
004F7BCE  movss    dword ptr [rip + 0x1b6d0ed], xmm15  ; -> 02064CC4
004F7BD7  movups   xmmword ptr [rcx + r15], xmm0
004F7BDC  movsxd   rcx, eax
004F7BDF  lea      eax, [rdx + 0x3a]
004F7BE2  movaps   xmm0, xmmword ptr [rsp + 0x80]
004F7BEA  mulss    xmm0, xmm4
004F7BEE  shl      eax, 4
004F7BF1  mulss    xmm5, xmm14
004F7BF6  movss    dword ptr [rip + 0x1b6d0f6], xmm0  ; -> 02064CF4
004F7BFE  movups   xmm0, xmmword ptr [rip + 0x1b6d0ab]  ; -> 02064CB0
004F7C05  mulss    xmm1, xmm2
004F7C09  movups   xmmword ptr [rcx + r15], xmm0
004F7C0E  movsxd   rcx, eax
004F7C11  lea      eax, [rdx + 0x3b]
004F7C14  movups   xmm0, xmmword ptr [rip + 0x1b6d0a5]  ; -> 02064CC0
004F7C1B  shl      eax, 4
004F7C1E  movss    dword ptr [rip + 0x1b6d0ca], xmm5  ; -> 02064CF0
004F7C26  movups   xmmword ptr [rcx + r15], xmm0
004F7C2B  movsxd   rcx, eax
004F7C2E  movss    dword ptr [rip + 0x1b6d0c2], xmm1  ; -> 02064CF8
004F7C36  movss    dword ptr [rip + 0x1b6d0be], xmm3  ; -> 02064CFC
004F7C3E  movups   xmm0, xmmword ptr [rip + 0x1b6d08b]  ; -> 02064CD0
004F7C45  lea      eax, [rdx + 0x3c]
004F7C48  movss    xmm1, dword ptr [rip + 0x190abe8]  ; -> 01E02838 [u32 0x00000000]
004F7C50  movups   xmmword ptr [rcx + r15], xmm0
004F7C55  shl      eax, 4
004F7C58  movups   xmm0, xmmword ptr [rip + 0x1b6d081]  ; -> 02064CE0
004F7C5F  movsxd   rcx, eax
004F7C62  lea      eax, [rdx + 0x3d]
004F7C65  shl      eax, 4
004F7C68  addss    xmm1, xmm8
004F7C6D  movups   xmmword ptr [rcx + r15], xmm0
004F7C72  movsxd   rcx, eax
004F7C75  ucomiss  xmm1, xmm11
004F7C79  movups   xmm0, xmmword ptr [rip + 0x1b6d070]  ; -> 02064CF0
004F7C80  movss    dword ptr [rip + 0x1b6cee0], xmm1  ; -> 02064B68
004F7C88  movups   xmmword ptr [rcx + r15], xmm0
004F7C8D  jp       0x4f7cb5  ; -> 004F7CB5
004F7C8F  jne      0x4f7cb5  ; -> 004F7CB5
004F7C91  call     0x22cc40  ; -> 0022CC40 fn
004F7C96  movss    xmm1, dword ptr [rip + 0x1b6ceca]  ; -> 02064B68
004F7C9E  movzx    ebx, word ptr [rip + 0x1b6ce67]  ; -> 02064B0C
004F7CA5  movss    xmm7, dword ptr [rip + 0x1b6cebf]  ; -> 02064B6C
004F7CAD  movss    xmm6, dword ptr [rip + 0x190ab87]  ; -> 01E0283C [f32 1]
004F7CB5  comiss   xmm11, xmm1
004F7CB9  jbe      0x4f7cd7  ; -> 004F7CD7
004F7CBB  call     0x22cc30  ; -> 0022CC30 fn
004F7CC0  movzx    ebx, word ptr [rip + 0x1b6ce45]  ; -> 02064B0C
004F7CC7  movss    xmm7, dword ptr [rip + 0x1b6ce9d]  ; -> 02064B6C
004F7CCF  movss    xmm6, dword ptr [rip + 0x190ab65]  ; -> 01E0283C [f32 1]
004F7CD7  ucomiss  xmm7, xmm11
004F7CDB  jp       0x4f7ce5  ; -> 004F7CE5
004F7CDD  jne      0x4f7ce5  ; -> 004F7CE5
004F7CDF  movaps   xmm4, xmm12
004F7CE3  jmp      0x4f7cec  ; -> 004F7CEC
004F7CE5  movaps   xmm4, xmm6
004F7CE8  divss    xmm4, xmm7
004F7CEC  movss    xmm15, dword ptr [rip + 0x17f3eb3]  ; -> 01CEBBA8 [f32 1]
004F7CF5  movsx    r9d, bx
004F7CF9  movss    dword ptr [rip + 0x1b6cdff], xmm4  ; -> 02064B00
004F7D01  mulss    xmm4, xmm6
004F7D05  lea      eax, [r9 + 1]
004F7D09  shl      eax, 4
004F7D0C  movsxd   rcx, eax
004F7D0F  lea      eax, [r9 + 7]
004F7D13  shl      eax, 4
004F7D16  movss    dword ptr [rip + 0x1b6ce4e], xmm4  ; -> 02064B6C
004F7D1E  movups   xmm0, xmmword ptr [rcx + r15]
004F7D23  movsxd   rcx, eax
004F7D26  lea      eax, [r9 + 4]
004F7D2A  shl      eax, 4
004F7D2D  movsxd   r8, eax
004F7D30  movups   xmmword ptr [rip + 0x1b6cdf9], xmm0  ; -> 02064B30
004F7D37  movups   xmm2, xmmword ptr [rcx + r15]
004F7D3C  movups   xmm0, xmmword ptr [r8 + r15]
004F7D41  movups   xmmword ptr [rip + 0x1b6cdf8], xmm2  ; -> 02064B40
004F7D48  cvtdq2ps xmm3, xmm0
004F7D4B  shufps   xmm2, xmm2, 0xaa
004F7D4F  movdqu   xmmword ptr [rip + 0x1b6cdf9], xmm3  ; -> 02064B50
004F7D57  movss    dword ptr [rsp + 0x20], xmm2
004F7D5D  mov      eax, dword ptr [rsp + 0x20]
004F7D61  mov      ecx, eax
004F7D63  shr      ecx, 0x12
004F7D66  xor      ecx, eax
004F7D68  shufps   xmm3, xmm3, 0x55
004F7D6C  and      eax, 0x3fffff
004F7D71  shr      ecx, 4
004F7D74  or       eax, 0x1fc00000
004F7D79  and      ecx, 1
004F7D7C  add      eax, eax
004F7D7E  or       ecx, eax
004F7D80  mov      eax, ecx
004F7D82  shr      eax, 0x12
004F7D85  xor      eax, ecx
004F7D87  and      ecx, 0x3fffff
004F7D8D  shr      eax, 4
004F7D90  or       ecx, 0x1fc00000
004F7D96  and      eax, 1
004F7D99  add      ecx, ecx
004F7D9B  or       eax, ecx
004F7D9D  mov      ecx, eax
004F7D9F  shr      ecx, 0x12
004F7DA2  xor      ecx, eax
004F7DA4  and      eax, 0x3fffff
004F7DA9  or       eax, 0x1fc00000
004F7DAE  shr      ecx, 4
004F7DB1  add      eax, eax
004F7DB3  and      ecx, 1
004F7DB6  or       ecx, eax
004F7DB8  mov      edx, ecx
004F7DBA  shr      edx, 0x12
004F7DBD  xor      edx, ecx
004F7DBF  and      ecx, 0x3fffff
004F7DC5  shr      edx, 4
004F7DC8  or       ecx, 0x1fc00000
004F7DCE  and      edx, 1
004F7DD1  add      ecx, ecx
004F7DD3  or       edx, ecx
004F7DD5  mov      eax, edx
004F7DD7  shr      eax, 0x12
004F7DDA  xor      eax, edx
004F7DDC  and      edx, 0x3fffff
004F7DE2  shr      eax, 4
004F7DE5  or       edx, 0x1fc00000
004F7DEB  and      eax, 1
004F7DEE  add      edx, edx
004F7DF0  or       eax, edx
004F7DF2  mov      dword ptr [rip + 0x190aa30], eax  ; -> 01E02828 [f32 1]
004F7DF8  movss    xmm5, dword ptr [rip + 0x190aa28]  ; -> 01E02828 [f32 1]
004F7E00  movaps   xmm0, xmm5
004F7E03  subss    xmm0, xmm15
004F7E08  mulss    xmm3, xmm0
004F7E0C  movss    dword ptr [rip + 0x1b6cd40], xmm3  ; -> 02064B54
004F7E14  addss    xmm3, dword ptr [rip + 0x1b6cd34]  ; -> 02064B50
004F7E1C  cvttss2si eax, xmm3
004F7E20  mov      dword ptr [rip + 0x1b6cd2a], eax  ; -> 02064B50
004F7E26  mov      dword ptr [r8 + r15], eax
004F7E2A  lea      eax, [r9 + 0x41]
004F7E2E  movups   xmm0, xmmword ptr [rip + 0x1b6cd2b]  ; -> 02064B60
004F7E35  shl      eax, 4
004F7E38  mov      r12d, 0xe0
004F7E3E  movsxd   rcx, eax
004F7E41  movups   xmmword ptr [rcx + r15], xmm0
004F7E46  movzx    eax, word ptr [r8 + r15]
004F7E4B  mov      word ptr [rip + 0x1b6cf6a], ax  ; -> 02064DBC
004F7E52  movsd    xmm13, qword ptr [rip + 0x17f3f25]  ; -> 01CEBD80 [u64 0x7FFFFFFFFFFFFFFF]
004F7E5B  nop      dword ptr [rax + rax]
004F7E60  movsx    r8d, bx
004F7E64  movss    dword ptr [rip + 0x1b6ce4c], xmm5  ; -> 02064CB8
004F7E6C  lea      eax, [r8 + 0xd]
004F7E70  shl      eax, 4
004F7E73  movsxd   rdx, eax
004F7E76  movups   xmm3, xmmword ptr [rdx + r15]
004F7E7B  movss    dword ptr [rsp + 0x20], xmm3
004F7E81  mov      eax, dword ptr [rsp + 0x20]
004F7E85  mov      ecx, eax
004F7E87  shr      ecx, 0x12
004F7E8A  xor      ecx, eax
004F7E8C  and      eax, 0x3fffff
004F7E91  or       eax, 0x1fc00000
004F7E96  shr      ecx, 4
004F7E99  add      eax, eax
004F7E9B  and      ecx, 1
004F7E9E  or       ecx, eax
004F7EA0  mov      eax, ecx
004F7EA2  shr      eax, 0x12
004F7EA5  xor      eax, ecx
004F7EA7  and      ecx, 0x3fffff
004F7EAD  shr      eax, 4
004F7EB0  or       ecx, 0x1fc00000
004F7EB6  and      eax, 1
004F7EB9  add      ecx, ecx
004F7EBB  or       eax, ecx
004F7EBD  mov      ecx, eax
004F7EBF  shr      ecx, 0x12
004F7EC2  xor      ecx, eax
004F7EC4  and      eax, 0x3fffff
004F7EC9  or       eax, 0x1fc00000
004F7ECE  shr      ecx, 4
004F7ED1  add      eax, eax
004F7ED3  and      ecx, 1
004F7ED6  or       ecx, eax
004F7ED8  mov      eax, ecx
004F7EDA  shr      eax, 0x12
004F7EDD  xor      eax, ecx
004F7EDF  and      ecx, 0x3fffff
004F7EE5  shr      eax, 4
004F7EE8  or       ecx, 0x1fc00000
004F7EEE  and      eax, 1
004F7EF1  add      ecx, ecx
004F7EF3  or       eax, ecx
004F7EF5  mov      ecx, eax
004F7EF7  shr      ecx, 0x12
004F7EFA  xor      ecx, eax
004F7EFC  and      eax, 0x3fffff
004F7F01  or       eax, 0x1fc00000
004F7F06  shr      ecx, 4
004F7F09  add      eax, eax
004F7F0B  and      ecx, 1
004F7F0E  or       ecx, eax
004F7F10  mov      eax, ecx
004F7F12  mov      dword ptr [rip + 0x190a910], ecx  ; -> 01E02828 [f32 1]
004F7F18  movss    xmm0, dword ptr [rip + 0x190a908]  ; -> 01E02828 [f32 1]
004F7F20  shr      eax, 0x12
004F7F23  xor      eax, ecx
004F7F25  and      ecx, 0x3fffff
004F7F2B  shr      eax, 4
004F7F2E  or       ecx, 0x1fc00000
004F7F34  and      eax, 1
004F7F37  add      ecx, ecx
004F7F39  or       eax, ecx
004F7F3B  mov      ecx, eax
004F7F3D  shr      ecx, 0x12
004F7F40  xor      ecx, eax
004F7F42  and      eax, 0x3fffff
004F7F47  or       eax, 0x1fc00000
004F7F4C  shr      ecx, 4
004F7F4F  add      eax, eax
004F7F51  and      ecx, 1
004F7F54  or       ecx, eax
004F7F56  mov      eax, ecx
004F7F58  shr      eax, 0x12
004F7F5B  xor      eax, ecx
004F7F5D  and      ecx, 0x3fffff
004F7F63  shr      eax, 4
004F7F66  and      eax, 1
004F7F69  or       ecx, 0x1fc00000
004F7F6F  movups   xmmword ptr [rip + 0x1b6cd2a], xmm3  ; -> 02064CA0
004F7F76  add      ecx, ecx
004F7F78  shufps   xmm3, xmm3, 0xaa
004F7F7C  or       eax, ecx
004F7F7E  mov      dword ptr [rip + 0x1b6cb74], 1  ; -> 02064AFC
004F7F88  mov      ecx, eax
004F7F8A  subss    xmm0, xmm15
004F7F8F  shr      ecx, 0x12
004F7F92  xor      ecx, eax
004F7F94  and      eax, 0x3fffff
004F7F99  or       eax, 0x1fc00000
004F7F9E  shr      ecx, 4
004F7FA1  add      eax, eax
004F7FA3  and      ecx, 1
004F7FA6  or       ecx, eax
004F7FA8  mulss    xmm3, xmm0
004F7FAC  mov      eax, ecx
004F7FAE  movss    xmm0, dword ptr [rip + 0x1b6ccee]  ; -> 02064CA4
004F7FB6  shr      eax, 0x12
004F7FB9  xor      eax, ecx
004F7FBB  movss    dword ptr [rip + 0x1b6cce5], xmm3  ; -> 02064CA8
004F7FC3  shr      eax, 4
004F7FC6  and      ecx, 0x3fffff
004F7FCC  and      eax, 1
004F7FCF  or       ecx, 0x1fc00000
004F7FD5  add      ecx, ecx
004F7FD7  or       eax, ecx
004F7FD9  mov      dword ptr [rip + 0x190a849], eax  ; -> 01E02828 [f32 1]
004F7FDF  lea      eax, [r8 + 5]
004F7FE3  movss    xmm2, dword ptr [rip + 0x190a83d]  ; -> 01E02828 [f32 1]
004F7FEB  shl      eax, 4
004F7FEE  movaps   xmm1, xmm2
004F7FF1  movsxd   rcx, eax
004F7FF4  subss    xmm1, xmm15
004F7FF9  movss    dword ptr [rip + 0x1b6cc9f], xmm2  ; -> 02064CA0
004F8001  mov      eax, dword ptr [rip + 0x1b6cc99]  ; -> 02064CA0
004F8007  movss    dword ptr [rip + 0x190a819], xmm5  ; -> 01E02828 [f32 1]
004F800F  movups   xmm3, xmmword ptr [rcx + r15]
004F8014  mov      dword ptr [rdx + r15], eax
004F8018  lea      eax, [r8 + 0x2b]
004F801C  shl      eax, 4
004F801F  movsxd   rcx, eax
004F8022  mulss    xmm0, xmm1
004F8026  movdqu   xmmword ptr [rip + 0x1b6cb92], xmm3  ; -> 02064BC0
004F802E  movss    dword ptr [rip + 0x1b6cc6e], xmm0  ; -> 02064CA4
004F8036  mov      rax, qword ptr [rip + 0x1b6cc67]  ; -> 02064CA4
004F803D  mov      qword ptr [rcx + r15 + 4], rax
004F8042  mov      eax, dword ptr [rip + 0x190a7e0]  ; -> 01E02828 [f32 1]
004F8048  mov      ecx, eax
004F804A  shr      ecx, 0x12
004F804D  xor      ecx, eax
004F804F  and      eax, 0x3fffff
004F8054  or       eax, 0x1fc00000
004F8059  shr      ecx, 4
004F805C  add      eax, eax
004F805E  and      ecx, 1
004F8061  or       ecx, eax
004F8063  mov      eax, ecx
004F8065  shr      eax, 0x12
004F8068  xor      eax, ecx
004F806A  and      ecx, 0x3fffff
004F8070  shr      eax, 4
004F8073  or       ecx, 0x1fc00000
004F8079  and      eax, 1
004F807C  add      ecx, ecx
004F807E  or       eax, ecx
004F8080  mov      ecx, eax
004F8082  shr      ecx, 0x12
004F8085  xor      ecx, eax
004F8087  and      eax, 0x3fffff
004F808C  or       eax, 0x1fc00000
004F8091  shr      ecx, 4
004F8094  add      eax, eax
004F8096  and      ecx, 1
004F8099  or       ecx, eax
004F809B  mov      eax, ecx
004F809D  shr      eax, 0x12
004F80A0  xor      eax, ecx
004F80A2  and      ecx, 0x3fffff
004F80A8  shr      eax, 4
004F80AB  and      eax, 1
004F80AE  or       ecx, 0x1fc00000
004F80B4  add      ecx, ecx
004F80B6  shufps   xmm3, xmm3, 0xaa
004F80BA  or       eax, ecx
004F80BC  mov      dword ptr [rip + 0x1b6ca3e], 0x3f800000  ; -> 02064B04
004F80C6  mov      ecx, eax
004F80C8  shr      ecx, 0x12
004F80CB  xor      ecx, eax
004F80CD  and      eax, 0x3fffff
004F80D2  or       eax, 0x1fc00000
004F80D7  shr      ecx, 4
004F80DA  add      eax, eax
004F80DC  and      ecx, 1
004F80DF  or       ecx, eax
004F80E1  mov      dword ptr [rip + 0x190a741], ecx  ; -> 01E02828 [f32 1]
004F80E7  mov      eax, ecx
004F80E9  movss    xmm2, dword ptr [rip + 0x190a737]  ; -> 01E02828 [f32 1]
004F80F1  shr      eax, 0x12
004F80F4  subss    xmm2, xmm15
004F80F9  xor      eax, ecx
004F80FB  and      ecx, 0x3fffff
004F8101  shr      eax, 4
004F8104  or       ecx, 0x1fc00000
004F810A  and      eax, 1
004F810D  add      ecx, ecx
004F810F  or       eax, ecx
004F8111  mov      ecx, eax
004F8113  mulss    xmm3, xmm2
004F8117  shr      ecx, 0x12
004F811A  xor      ecx, eax
004F811C  movss    dword ptr [rip + 0x1b6cb8c], xmm2  ; -> 02064CB0
004F8124  movss    xmm2, dword ptr [rip + 0x1b6caa0]  ; -> 02064BCC
004F812C  and      eax, 0x3fffff
004F8131  or       eax, 0x1fc00000
004F8136  shr      ecx, 4
004F8139  add      eax, eax
004F813B  movss    dword ptr [rip + 0x1b6ca85], xmm3  ; -> 02064BC8
004F8143  and      ecx, 1
004F8146  or       ecx, eax
004F8148  mov      eax, ecx
004F814A  shr      eax, 0x12
004F814D  xor      eax, ecx
004F814F  and      ecx, 0x3fffff
004F8155  shr      eax, 4
004F8158  or       ecx, 0x1fc00000
004F815E  and      eax, 1
004F8161  add      ecx, ecx
004F8163  or       eax, ecx
004F8165  mov      ecx, eax
004F8167  shr      ecx, 0x12
004F816A  xor      ecx, eax
004F816C  and      eax, 0x3fffff
004F8171  or       eax, 0x1fc00000
004F8176  shr      ecx, 4
004F8179  add      eax, eax
004F817B  and      ecx, 1
004F817E  or       ecx, eax
004F8180  mov      eax, ecx
004F8182  shr      eax, 0x12
004F8185  xor      eax, ecx
004F8187  and      ecx, 0x3fffff
004F818D  shr      eax, 4
004F8190  or       ecx, 0x1fc00000
004F8196  and      eax, 1
004F8199  add      ecx, ecx
004F819B  or       eax, ecx
004F819D  mov      dword ptr [rip + 0x190a685], eax  ; -> 01E02828 [f32 1]
004F81A3  lea      eax, [r8 + 3]
004F81A7  movss    xmm1, dword ptr [rip + 0x190a679]  ; -> 01E02828 [f32 1]
004F81AF  shl      eax, 4
004F81B2  subss    xmm1, xmm15
004F81B7  movsxd   rcx, eax
004F81BA  lea      eax, [r8 + 2]
004F81BE  shl      eax, 4
004F81C1  movups   xmm4, xmmword ptr [rcx + r15]
004F81C6  movsxd   rcx, eax
004F81C9  mulss    xmm2, xmm1
004F81CD  movss    dword ptr [rip + 0x1b6cb0f], xmm1  ; -> 02064CE4
004F81D5  movups   xmm0, xmmword ptr [rcx + r15]
004F81DA  movss    dword ptr [rip + 0x1b6c9ea], xmm2  ; -> 02064BCC
004F81E2  movups   xmmword ptr [rip + 0x1b6cad7], xmm0  ; -> 02064CC0
004F81E9  movups   xmmword ptr [rip + 0x1b6cae0], xmm4  ; -> 02064CD0
004F81F0  movss    xmm0, dword ptr [rip + 0x1b6c9c8]  ; -> 02064BC0
004F81F8  movss    xmm1, dword ptr [rip + 0x1b6c9c4]  ; -> 02064BC4
004F8200  addss    xmm0, xmm3
004F8204  movups   xmm3, xmmword ptr [rcx + r15]
004F8209  addss    xmm1, xmm2
004F820D  movss    dword ptr [rip + 0x1b6cabb], xmm4  ; -> 02064CD0
004F8215  movaps   xmm2, xmm4
004F8218  movss    dword ptr [rip + 0x1b6c9a0], xmm0  ; -> 02064BC0
004F8220  movaps   xmm0, xmm4
004F8223  subss    xmm0, xmm3
004F8227  shufps   xmm2, xmm4, 0xaa
004F822B  movss    dword ptr [rip + 0x1b6caa5], xmm2  ; -> 02064CD8
004F8233  movss    dword ptr [rip + 0x1b6c989], xmm1  ; -> 02064BC4
004F823B  movaps   xmm1, xmm4
004F823E  shufps   xmm1, xmm4, 0x55
004F8242  movss    dword ptr [rip + 0x1b6ca8a], xmm1  ; -> 02064CD4
004F824A  movss    dword ptr [rip + 0x1b6ca4e], xmm0  ; -> 02064CA0
004F8252  movaps   xmm0, xmm3
004F8255  shufps   xmm0, xmm3, 0x55
004F8259  subss    xmm1, xmm0
004F825D  shufps   xmm4, xmm4, 0xff
004F8261  movaps   xmm0, xmm3
004F8264  shufps   xmm0, xmm3, 0xaa
004F8268  shufps   xmm3, xmm3, 0xff
004F826C  subss    xmm2, xmm0
004F8270  subss    xmm4, xmm3
004F8274  movss    dword ptr [rip + 0x1b6ca28], xmm1  ; -> 02064CA4
004F827C  movss    dword ptr [rip + 0x1b6ca24], xmm2  ; -> 02064CA8
004F8284  movss    dword ptr [rip + 0x1b6ca20], xmm4  ; -> 02064CAC
004F828C  call     0x22cc20  ; -> 0022CC20 fn
004F8291  movss    xmm9, dword ptr [rip + 0x190a5a2]  ; -> 01E0283C [f32 1]
004F829A  movss    xmm0, dword ptr [rip + 0x190a58e]  ; -> 01E02830 [u32 0x00000000]
004F82A2  movss    xmm14, dword ptr [rip + 0x1b6c9f5]  ; -> 02064CA0
004F82AB  movss    xmm7, dword ptr [rip + 0x1b6c9f1]  ; -> 02064CA4
004F82B3  movaps   xmm2, xmm14
004F82B7  movss    xmm6, dword ptr [rip + 0x1b6c9e9]  ; -> 02064CA8
004F82BF  movss    xmm8, dword ptr [rip + 0x190a56c]  ; -> 01E02834 [u32 0x00000000]
004F82C8  movaps   xmm1, xmm6
004F82CB  movss    xmm10, dword ptr [rip + 0x190a564]  ; -> 01E02838 [u32 0x00000000]
004F82D4  movss    dword ptr [rip + 0x1b6c9e0], xmm0  ; -> 02064CBC
004F82DC  movaps   xmm0, xmm9
004F82E0  mulss    xmm0, xmm9
004F82E5  mulss    xmm1, xmm6
004F82E9  movss    dword ptr [rip + 0x1b6c9eb], xmm0  ; -> 02064CDC
004F82F1  movaps   xmm0, xmm7
004F82F4  mulss    xmm0, xmm7
004F82F8  mulss    xmm2, xmm14
004F82FD  mulss    xmm0, xmm9
004F8302  mulss    xmm1, xmm9
004F8307  mulss    xmm2, xmm9
004F830C  movss    dword ptr [rsp + 0x20], xmm8
004F8313  movss    dword ptr [rip + 0x1b6c994], xmm8  ; -> 02064CB0
004F831C  addss    xmm2, xmm0
004F8320  movss    dword ptr [rip + 0x1b6c98b], xmm10  ; -> 02064CB4
004F8329  movss    dword ptr [rip + 0x1b6c986], xmm9  ; -> 02064CB8
004F8332  movss    dword ptr [rip + 0x1b6c995], xmm8  ; -> 02064CD0
004F833B  movss    dword ptr [rip + 0x1b6c990], xmm10  ; -> 02064CD4
004F8344  addss    xmm1, xmm2
004F8348  cvtps2pd xmm0, xmm1
004F834B  andps    xmm0, xmm13
004F834F  cvtpd2ps xmm0, xmm0
004F8353  call     0x861f14  ; -> 00861F14 fn
004F8358  movaps   xmm1, xmm0
004F835B  mulss    xmm1, xmm9
004F8360  ucomiss  xmm1, xmm11
004F8364  movss    dword ptr [rip + 0x1b6c96c], xmm1  ; -> 02064CD8
004F836C  jp       0x4f8376  ; -> 004F8376
004F836E  jne      0x4f8376  ; -> 004F8376
004F8370  movaps   xmm0, xmm12
004F8374  jmp      0x4f837e  ; -> 004F837E
004F8376  movaps   xmm0, xmm9
004F837A  divss    xmm0, xmm1
004F837E  movss    xmm3, dword ptr [rsp + 0x20]
004F8384  movaps   xmm1, xmm8
004F8388  mulss    xmm6, xmm0
004F838C  mulss    xmm7, xmm0
004F8390  mulss    xmm14, xmm0
004F8395  movaps   xmm8, xmm6
004F8399  movaps   xmm0, xmm7
004F839C  movss    dword ptr [rip + 0x1b6c900], xmm7  ; -> 02064CA4
004F83A4  mulss    xmm0, xmm10
004F83A9  movss    dword ptr [rip + 0x1b6c8f7], xmm6  ; -> 02064CA8
004F83B1  mulss    xmm1, xmm14
004F83B6  movss    dword ptr [rip + 0x1b6c8d6], xmm0  ; -> 02064C94
004F83BE  mulss    xmm0, xmm9
004F83C3  movss    dword ptr [rip + 0x1b6c8c5], xmm1  ; -> 02064C90
004F83CB  mulss    xmm1, xmm9
004F83D0  mulss    xmm8, xmm9
004F83D5  addss    xmm1, xmm0
004F83D9  movss    dword ptr [rip + 0x1b6c8be], xmm14  ; -> 02064CA0
004F83E2  movss    dword ptr [rip + 0x1b6c8ad], xmm8  ; -> 02064C98
004F83EB  mulss    xmm8, xmm9
004F83F0  addss    xmm8, xmm1
004F83F5  movups   xmm1, xmmword ptr [rip + 0x1b6c8b4]  ; -> 02064CB0
004F83FC  mulss    xmm7, xmm1
004F8400  movaps   xmm0, xmm1
004F8403  shufps   xmm0, xmm1, 0x55
004F8407  movaps   xmm2, xmm1
004F840A  mulss    xmm6, xmm0
004F840E  shufps   xmm2, xmm1, 0xaa
004F8412  mulss    xmm2, xmm14
004F8417  movss    dword ptr [rip + 0x1b6c701], xmm6  ; -> 02064B20
004F841F  movss    dword ptr [rip + 0x1b6c701], xmm7  ; -> 02064B28
004F8427  movss    dword ptr [rip + 0x1b6c6f5], xmm2  ; -> 02064B24
004F842F  movups   xmmword ptr [rsp + 0x110], xmm1
004F8437  movups   xmm1, xmmword ptr [rip + 0x1b6c862]  ; -> 02064CA0
004F843E  movss    dword ptr [rip + 0x1b6c855], xmm8  ; -> 02064C9C
004F8447  movaps   xmm0, xmm1
004F844A  shufps   xmm0, xmm1, 0x55
004F844E  mulss    xmm0, xmm9
004F8453  movups   xmmword ptr [rsp + 0x120], xmm1
004F845B  subss    xmm6, xmm0
004F845F  movaps   xmm0, xmm1
004F8462  shufps   xmm0, xmm1, 0xaa
004F8466  mulss    xmm3, xmm0
004F846A  movaps   xmm0, xmm10
004F846E  mulss    xmm0, xmm1
004F8472  subss    xmm2, xmm3
004F8476  movss    dword ptr [rip + 0x1b6c822], xmm6  ; -> 02064CA0
004F847E  mulss    xmm6, xmm6
004F8482  subss    xmm7, xmm0
004F8486  movss    dword ptr [rip + 0x1b6c816], xmm2  ; -> 02064CA4
004F848E  mulss    xmm2, xmm2
004F8492  movss    dword ptr [rip + 0x1b6c80e], xmm7  ; -> 02064CA8
004F849A  mulss    xmm7, xmm7
004F849E  movss    dword ptr [rip + 0x1b6c80e], xmm2  ; -> 02064CB4
004F84A6  movss    dword ptr [rip + 0x1b6c802], xmm6  ; -> 02064CB0
004F84AE  mulss    xmm2, xmm9
004F84B3  movss    dword ptr [rip + 0x1b6c7fd], xmm7  ; -> 02064CB8
004F84BB  mulss    xmm7, xmm9
004F84C0  mulss    xmm6, xmm9
004F84C5  addss    xmm6, xmm2
004F84C9  addss    xmm7, xmm6
004F84CD  movss    dword ptr [rip + 0x1b6c657], xmm6  ; -> 02064B2C
004F84D5  cvtps2pd xmm0, xmm7
004F84D8  movss    dword ptr [rip + 0x1b6c7dc], xmm7  ; -> 02064CBC
004F84E0  andps    xmm0, xmm13
004F84E4  cvtpd2ps xmm0, xmm0
004F84E8  call     0x861f14  ; -> 00861F14 fn
004F84ED  movaps   xmm1, xmm0
004F84F0  ucomiss  xmm1, xmm11
004F84F4  jp       0x4f8504  ; -> 004F8504
004F84F6  jne      0x4f8504  ; -> 004F8504
004F84F8  mov      dword ptr [rip + 0x1b6c5fe], 0x7f7fffff  ; -> 02064B00
004F8502  jmp      0x4f8514  ; -> 004F8514
004F8504  movaps   xmm0, xmm9
004F8508  divss    xmm0, xmm1
004F850C  movss    dword ptr [rip + 0x1b6c5ec], xmm0  ; -> 02064B00
004F8514  addss    xmm10, xmm8
004F8519  mulss    xmm8, xmm8
004F851E  subss    xmm9, xmm8
004F8523  movss    dword ptr [rip + 0x1b6c74c], xmm10  ; -> 02064C78
004F852C  movss    dword ptr [rip + 0x1b6c747], xmm9  ; -> 02064C7C
004F8535  call     0x22cc20  ; -> 0022CC20 fn
004F853A  movss    xmm0, dword ptr [rip + 0x1b6c5be]  ; -> 02064B00
004F8542  movss    xmm6, dword ptr [rip + 0x1b6c756]  ; -> 02064CA0
004F854A  movss    xmm7, dword ptr [rip + 0x1b6c752]  ; -> 02064CA4
004F8552  movss    xmm8, dword ptr [rip + 0x1b6c74d]  ; -> 02064CA8
004F855B  mulss    xmm6, xmm0
004F855F  mulss    xmm7, xmm0
004F8563  mulss    xmm8, xmm0
004F8568  movss    xmm0, dword ptr [rip + 0x1b6c70c]  ; -> 02064C7C
004F8570  cvtps2pd xmm0, xmm0
004F8573  movss    dword ptr [rip + 0x1b6c725], xmm6  ; -> 02064CA0
004F857B  andps    xmm0, xmm13
004F857F  movss    dword ptr [rip + 0x1b6c71d], xmm7  ; -> 02064CA4
004F8587  cvtpd2ps xmm0, xmm0
004F858B  movss    dword ptr [rip + 0x1b6c714], xmm8  ; -> 02064CA8
004F8594  call     0x861f14  ; -> 00861F14 fn
004F8599  movups   xmm3, xmmword ptr [rip + 0x1b6c700]  ; -> 02064CA0
004F85A0  mov      edx, dword ptr [rip + 0x1b6c556]  ; -> 02064AFC
004F85A6  movss    xmm5, dword ptr [rip + 0x190a282]  ; -> 01E02830 [u32 0x00000000]
004F85AE  movaps   xmm4, xmm0
004F85B1  movss    dword ptr [rip + 0x1b6c547], xmm4  ; -> 02064B00
004F85B9  movaps   xmm0, xmm7
004F85BC  mulss    xmm0, xmm8
004F85C1  movaps   xmm2, xmm7
004F85C4  mulss    xmm2, xmm6
004F85C8  movaps   xmm1, xmm6
004F85CB  shufps   xmm1, xmm1, 0
004F85CF  mulps    xmm1, xmm3
004F85D2  movss    dword ptr [rip + 0x1b6c71e], xmm0  ; -> 02064CF8
004F85DA  movaps   xmm0, xmm8
004F85DE  shufps   xmm0, xmm0, 0
004F85E2  mulps    xmm0, xmm3
004F85E5  movss    dword ptr [rip + 0x1b6c703], xmm2  ; -> 02064CF0
004F85ED  movaps   xmm2, xmm7
004F85F0  movups   xmmword ptr [rip + 0x1b6c6e9], xmm1  ; -> 02064CE0
004F85F7  movaps   xmm1, xmm7
004F85FA  mulss    xmm1, xmm7
004F85FE  movups   xmmword ptr [rip + 0x1b6c6fb], xmm0  ; -> 02064D00
004F8605  movss    xmm0, dword ptr [rip + 0x190a22f]  ; -> 01E0283C [f32 1]
004F860D  movss    dword ptr [rip + 0x1b6c6df], xmm1  ; -> 02064CF4
004F8615  movaps   xmm1, xmm3
004F8618  shufps   xmm1, xmm3, 0xff
004F861C  mulss    xmm2, xmm1
004F8620  movss    dword ptr [rip + 0x1b6c684], xmm1  ; -> 02064CAC
004F8628  subss    xmm0, dword ptr [rip + 0x1b6c668]  ; -> 02064C98
004F8630  movss    dword ptr [rip + 0x1b6c6c4], xmm2  ; -> 02064CFC
004F8638  movaps   xmm2, xmm5
004F863B  addss    xmm2, xmm4
004F863F  movss    xmm4, dword ptr [rip + 0x190a1f1]  ; -> 01E02838 [u32 0x00000000]
004F8647  movaps   xmm3, xmm4
004F864A  addss    xmm3, dword ptr [rip + 0x1b6c64a]  ; -> 02064C9C
004F8652  movss    dword ptr [rip + 0x1b6c622], xmm0  ; -> 02064C7C
004F865A  movss    dword ptr [rip + 0x1b6c60e], xmm2  ; -> 02064C70
004F8662  movaps   xmm1, xmm2
004F8665  mulss    xmm1, xmm6
004F8669  movaps   xmm0, xmm2
004F866C  mulss    xmm0, xmm7
004F8670  mulss    xmm2, xmm8
004F8675  movss    dword ptr [rip + 0x1b6c603], xmm1  ; -> 02064C80
004F867D  movss    dword ptr [rip + 0x1b6c5ff], xmm0  ; -> 02064C84
004F8685  movss    dword ptr [rip + 0x1b6c5eb], xmm3  ; -> 02064C78
004F868D  movss    dword ptr [rip + 0x1b6c5f3], xmm2  ; -> 02064C88
004F8695  test     edx, edx
004F8697  je       0x4f86c2  ; -> 004F86C2
004F8699  mov      eax, dword ptr [rip + 0x190a189]  ; -> 01E02828 [f32 1]
004F869F  mov      ecx, eax
004F86A1  shr      ecx, 0x12
004F86A4  xor      ecx, eax
004F86A6  and      eax, 0x3fffff
004F86AB  or       eax, 0x1fc00000
004F86B0  shr      ecx, 4
004F86B3  add      eax, eax
004F86B5  and      ecx, 1
004F86B8  or       ecx, eax
004F86BA  mov      dword ptr [rip + 0x190a168], ecx  ; -> 01E02828 [f32 1]
004F86C0  jmp      0x4f86c8  ; -> 004F86C8
004F86C2  mov      ecx, dword ptr [rip + 0x190a160]  ; -> 01E02828 [f32 1]
004F86C8  addss    xmm3, xmm5
004F86CC  movss    dword ptr [rip + 0x1b6c44c], xmm3  ; -> 02064B20
004F86D4  test     edx, edx
004F86D6  je       0x4f86f9  ; -> 004F86F9
004F86D8  mov      eax, ecx
004F86DA  shr      ecx, 0x12
004F86DD  xor      ecx, eax
004F86DF  and      eax, 0x3fffff
004F86E4  or       eax, 0x1fc00000
004F86E9  shr      ecx, 4
004F86EC  add      eax, eax
004F86EE  and      ecx, 1
004F86F1  or       ecx, eax
004F86F3  mov      dword ptr [rip + 0x190a12f], ecx  ; -> 01E02828 [f32 1]
004F86F9  addss    xmm2, dword ptr [rip + 0x190a133]  ; -> 01E02834 [u32 0x00000000]
004F8701  movss    dword ptr [rip + 0x1b6c41b], xmm2  ; -> 02064B24
004F8709  test     edx, edx
004F870B  jne      0x4f8713  ; -> 004F8713
004F870D  movaps   xmm1, xmm15
004F8711  jmp      0x4f873e  ; -> 004F873E
004F8713  mov      eax, ecx
004F8715  shr      eax, 0x12
004F8718  xor      eax, ecx
004F871A  and      ecx, 0x3fffff
004F8720  or       ecx, 0x1fc00000
004F8726  shr      eax, 4
004F8729  add      ecx, ecx
004F872B  and      eax, 1
004F872E  or       eax, ecx
004F8730  mov      dword ptr [rip + 0x190a0f2], eax  ; -> 01E02828 [f32 1]
004F8736  movss    xmm1, dword ptr [rip + 0x190a0ea]  ; -> 01E02828 [f32 1]
004F873E  subss    xmm4, xmm0
004F8742  movss    dword ptr [rip + 0x1b6c566], xmm1  ; -> 02064CB0
004F874A  movss    dword ptr [rip + 0x1b6c3d6], xmm4  ; -> 02064B28
004F8752  call     0x22cc20  ; -> 0022CC20 fn
004F8757  mov      edx, dword ptr [rip + 0x1b6c39f]  ; -> 02064AFC
004F875D  test     edx, edx
004F875F  je       0x4f878a  ; -> 004F878A
004F8761  mov      eax, dword ptr [rip + 0x190a0c1]  ; -> 01E02828 [f32 1]
004F8767  mov      ecx, eax
004F8769  shr      ecx, 0x12
004F876C  xor      ecx, eax
004F876E  and      eax, 0x3fffff
004F8773  or       eax, 0x1fc00000
004F8778  shr      ecx, 4
004F877B  add      eax, eax
004F877D  and      ecx, 1
004F8780  or       ecx, eax
004F8782  mov      dword ptr [rip + 0x190a0a0], ecx  ; -> 01E02828 [f32 1]
004F8788  jmp      0x4f8790  ; -> 004F8790
004F878A  mov      ecx, dword ptr [rip + 0x190a098]  ; -> 01E02828 [f32 1]
004F8790  movss    xmm0, dword ptr [rip + 0x1b6c548]  ; -> 02064CE0
004F8798  movss    xmm2, dword ptr [rip + 0x1b6c4dc]  ; -> 02064C7C
004F87A0  movss    xmm1, dword ptr [rip + 0x1b6c540]  ; -> 02064CE8
004F87A8  mulss    xmm0, xmm2
004F87AC  mulss    xmm1, xmm2
004F87B0  addss    xmm0, dword ptr [rip + 0x1b6c368]  ; -> 02064B20
004F87B8  addss    xmm1, dword ptr [rip + 0x1b6c368]  ; -> 02064B28
004F87C0  movss    dword ptr [rip + 0x1b6c518], xmm0  ; -> 02064CE0
004F87C8  movss    xmm0, dword ptr [rip + 0x1b6c514]  ; -> 02064CE4
004F87D0  mulss    xmm0, xmm2
004F87D4  movss    dword ptr [rip + 0x1b6c50c], xmm1  ; -> 02064CE8
004F87DC  addss    xmm0, dword ptr [rip + 0x1b6c340]  ; -> 02064B24
004F87E4  movss    dword ptr [rip + 0x1b6c4f8], xmm0  ; -> 02064CE4
004F87EC  test     edx, edx
004F87EE  jne      0x4f87f6  ; -> 004F87F6
004F87F0  movaps   xmm0, xmm15
004F87F4  jmp      0x4f8821  ; -> 004F8821
004F87F6  mov      eax, ecx
004F87F8  shr      eax, 0x12
004F87FB  xor      eax, ecx
004F87FD  and      ecx, 0x3fffff
004F8803  or       ecx, 0x1fc00000
004F8809  shr      eax, 4
004F880C  add      ecx, ecx
004F880E  and      eax, 1
004F8811  or       eax, ecx
004F8813  mov      dword ptr [rip + 0x190a00f], eax  ; -> 01E02828 [f32 1]
004F8819  movss    xmm0, dword ptr [rip + 0x190a007]  ; -> 01E02828 [f32 1]
004F8821  movss    xmm6, dword ptr [rip + 0x409313]  ; -> 00901B3C [f32 1.5]
004F8829  subss    xmm0, xmm6
004F882D  mov      dword ptr [rip + 0x1b6c2cd], 0x3fc00000  ; -> 02064B04
004F8837  movss    dword ptr [rip + 0x1b6c471], xmm0  ; -> 02064CB0
004F883F  movss    xmm0, dword ptr [rip + 0x1909fe9]  ; -> 01E02830 [u32 0x00000000]
004F8847  subss    xmm0, dword ptr [rip + 0x1b6c439]  ; -> 02064C88
004F884F  movss    dword ptr [rip + 0x1b6c2c9], xmm0  ; -> 02064B20
004F8857  call     0x22cc20  ; -> 0022CC20 fn
004F885C  movss    xmm0, dword ptr [rip + 0x1b6c48c]  ; -> 02064CF0
004F8864  movss    xmm2, dword ptr [rip + 0x1b6c410]  ; -> 02064C7C
004F886C  movss    xmm1, dword ptr [rip + 0x1b6c404]  ; -> 02064C78
004F8874  movss    xmm5, dword ptr [rip + 0x1909fb8]  ; -> 01E02834 [u32 0x00000000]
004F887C  movss    xmm4, dword ptr [rip + 0x1b6c3fc]  ; -> 02064C80
004F8884  addss    xmm1, xmm5
004F8888  movss    xmm7, dword ptr [rip + 0x17f33e8]  ; -> 01CEBC78 [f32 6.283185]
004F8890  subss    xmm5, xmm4
004F8894  mulss    xmm0, xmm2
004F8898  movaps   xmm3, xmm4
004F889B  mov      dword ptr [rip + 0x1b6c25f], 0x40c90fdb  ; -> 02064B04
004F88A5  addss    xmm3, dword ptr [rip + 0x1909f8b]  ; -> 01E02838 [u32 0x00000000]
004F88AD  addss    xmm0, dword ptr [rip + 0x1b6c26b]  ; -> 02064B20
004F88B5  movss    dword ptr [rip + 0x1b6c267], xmm5  ; -> 02064B24
004F88BD  movss    dword ptr [rip + 0x1b6c263], xmm3  ; -> 02064B28
004F88C5  movss    dword ptr [rip + 0x1b6c423], xmm0  ; -> 02064CF0
004F88CD  movss    xmm0, dword ptr [rip + 0x1b6c41f]  ; -> 02064CF4
004F88D5  mulss    xmm0, xmm2
004F88D9  addss    xmm0, xmm1
004F88DD  movss    xmm1, dword ptr [rip + 0x1b6c413]  ; -> 02064CF8
004F88E5  mulss    xmm1, xmm2
004F88E9  movss    dword ptr [rip + 0x1b6c403], xmm0  ; -> 02064CF4
004F88F1  addss    xmm1, xmm3
004F88F5  movss    xmm0, dword ptr [rip + 0x1b6c3b3]  ; -> 02064CB0
004F88FD  mulss    xmm0, xmm7
004F8901  movss    dword ptr [rip + 0x1b6c3ef], xmm1  ; -> 02064CF8
004F8909  movss    dword ptr [rip + 0x1b6c39f], xmm0  ; -> 02064CB0
004F8911  movss    xmm0, dword ptr [rip + 0x1b6c36b]  ; -> 02064C84
004F8919  addss    xmm0, dword ptr [rip + 0x1909f0f]  ; -> 01E02830 [u32 0x00000000]
004F8921  movss    dword ptr [rip + 0x1b6c1f7], xmm0  ; -> 02064B20
004F8929  call     0x22cc20  ; -> 0022CC20 fn
004F892E  movss    xmm0, dword ptr [rip + 0x1b6c3ca]  ; -> 02064D00
004F8936  movss    xmm2, dword ptr [rip + 0x1b6c33e]  ; -> 02064C7C
004F893E  movss    xmm1, dword ptr [rip + 0x1b6c3c2]  ; -> 02064D08
004F8946  movss    xmm3, dword ptr [rip + 0x1b6c32a]  ; -> 02064C78
004F894E  addss    xmm3, dword ptr [rip + 0x1909ee2]  ; -> 01E02838 [u32 0x00000000]
004F8956  mulss    xmm0, xmm2
004F895A  mulss    xmm1, xmm2
004F895E  addss    xmm0, dword ptr [rip + 0x1b6c1ba]  ; -> 02064B20
004F8966  movss    dword ptr [rip + 0x1b6c1ba], xmm3  ; -> 02064B28
004F896E  addss    xmm1, xmm3
004F8972  movss    dword ptr [rip + 0x1b6c386], xmm0  ; -> 02064D00
004F897A  movss    xmm0, dword ptr [rip + 0x1b6c382]  ; -> 02064D04
004F8982  mulss    xmm0, xmm2
004F8986  movss    dword ptr [rip + 0x1b6c37a], xmm1  ; -> 02064D08
004F898E  addss    xmm0, dword ptr [rip + 0x1b6c18e]  ; -> 02064B24
004F8996  movss    dword ptr [rip + 0x1b6c366], xmm0  ; -> 02064D04
004F899E  movups   xmm0, xmmword ptr [rip + 0x1b6c31b]  ; -> 02064CC0
004F89A5  movups   xmmword ptr [rip + 0x1b6c364], xmm0  ; -> 02064D10
004F89AC  call     0x5376d0  ; -> 005376D0 fn
004F89B1  cmp      dword ptr [rip + 0x1b6c144], 0  ; -> 02064AFC
004F89B8  movss    xmm1, dword ptr [rip + 0x1b6c200]  ; -> 02064BC0
004F89C0  movaps   xmm0, xmm1
004F89C3  mulss    xmm1, dword ptr [rip + 0x1b6c2f9]  ; -> 02064CC4
004F89CB  mulss    xmm0, dword ptr [rip + 0x1b6c2ed]  ; -> 02064CC0
004F89D3  movss    dword ptr [rip + 0x1b6c1d9], xmm1  ; -> 02064BB4
004F89DB  movss    dword ptr [rip + 0x1b6c1cd], xmm0  ; -> 02064BB0
004F89E3  je       0x4f8a8b  ; -> 004F8A8B
004F89E9  mov      eax, dword ptr [rip + 0x1909e39]  ; -> 01E02828 [f32 1]
004F89EF  mov      ecx, eax
004F89F1  shr      ecx, 0x12
004F89F4  xor      ecx, eax
004F89F6  and      eax, 0x3fffff
004F89FB  or       eax, 0x1fc00000
004F8A00  shr      ecx, 4
004F8A03  add      eax, eax
004F8A05  and      ecx, 1
004F8A08  or       ecx, eax
004F8A0A  mov      eax, ecx
004F8A0C  shr      eax, 0x12
004F8A0F  xor      eax, ecx
004F8A11  and      ecx, 0x3fffff
004F8A17  or       ecx, 0x1fc00000
004F8A1D  shr      eax, 4
004F8A20  add      ecx, ecx
004F8A22  and      eax, 1
004F8A25  or       eax, ecx
004F8A27  mov      ecx, eax
004F8A29  shr      ecx, 0x12
004F8A2C  xor      ecx, eax
004F8A2E  and      eax, 0x3fffff
004F8A33  or       eax, 0x1fc00000
004F8A38  shr      ecx, 4
004F8A3B  add      eax, eax
004F8A3D  and      ecx, 1
004F8A40  or       ecx, eax
004F8A42  mov      edx, ecx
004F8A44  shr      edx, 0x12
004F8A47  xor      edx, ecx
004F8A49  and      ecx, 0x3fffff
004F8A4F  shr      edx, 4
004F8A52  or       ecx, 0x1fc00000
004F8A58  and      edx, 1
004F8A5B  add      ecx, ecx
004F8A5D  or       edx, ecx
004F8A5F  mov      eax, edx
004F8A61  shr      eax, 0x12
004F8A64  xor      eax, edx
004F8A66  and      edx, 0x3fffff
004F8A6C  or       edx, 0x1fc00000
004F8A72  shr      eax, 4
004F8A75  add      edx, edx
004F8A77  and      eax, 1
004F8A7A  or       eax, edx
004F8A7C  mov      dword ptr [rip + 0x1909da6], eax  ; -> 01E02828 [f32 1]
004F8A82  movss    xmm15, dword ptr [rip + 0x1909d9d]  ; -> 01E02828 [f32 1]
004F8A8B  subss    xmm15, xmm6
004F8A90  mov      dword ptr [rip + 0x1b6c06a], 0x40c90fdb  ; -> 02064B04
004F8A9A  mulss    xmm15, xmm7
004F8A9F  movss    dword ptr [rip + 0x1b6c208], xmm15  ; -> 02064CB0
004F8AA8  call     0x5376d0  ; -> 005376D0 fn
004F8AAD  movss    xmm0, dword ptr [rip + 0x1b6c10f]  ; -> 02064BC4
004F8AB5  movss    xmm1, dword ptr [rip + 0x1909d73]  ; -> 01E02830 [u32 0x00000000]
004F8ABD  movaps   xmm6, xmm0
004F8AC0  mulss    xmm0, dword ptr [rip + 0x1b6c1f8]  ; -> 02064CC0
004F8AC8  movaps   xmm5, xmm1
004F8ACB  mulss    xmm6, dword ptr [rip + 0x1b6c1f1]  ; -> 02064CC4
004F8AD3  movss    xmm4, dword ptr [rip + 0x1909d61]  ; -> 01E0283C [f32 1]
004F8ADB  addss    xmm5, xmm0
004F8ADF  movss    xmm3, dword ptr [rip + 0x1b6c0c9]  ; -> 02064BB0
004F8AE7  movss    xmm2, dword ptr [rip + 0x1b6c0c5]  ; -> 02064BB4
004F8AEF  addss    xmm3, xmm1
004F8AF3  movss    xmm1, dword ptr [rip + 0x1909d3d]  ; -> 01E02838 [u32 0x00000000]
004F8AFB  addss    xmm2, dword ptr [rip + 0x1909d31]  ; -> 01E02834 [u32 0x00000000]
004F8B03  mulss    xmm1, xmm4
004F8B07  movss    dword ptr [rip + 0x1b6c1a5], xmm6  ; -> 02064CB4
004F8B0F  addss    xmm6, dword ptr [rip + 0x1909d1d]  ; -> 01E02834 [u32 0x00000000]
004F8B17  movss    dword ptr [rip + 0x1b6c191], xmm0  ; -> 02064CB0
004F8B1F  movss    xmm0, dword ptr [rip + 0x1b6c1b1]  ; -> 02064CD8
004F8B27  subss    xmm0, xmm1
004F8B2B  mulss    xmm4, xmm4
004F8B2F  movss    dword ptr [rip + 0x1b6c191], xmm1  ; -> 02064CC8
004F8B37  movss    xmm1, dword ptr [rip + 0x1b6c19d]  ; -> 02064CDC
004F8B3F  movss    dword ptr [rip + 0x1b6c18d], xmm6  ; -> 02064CD4
004F8B47  subss    xmm1, xmm4
004F8B4B  movss    dword ptr [rip + 0x1b6c17d], xmm5  ; -> 02064CD0
004F8B53  subss    xmm6, xmm2
004F8B57  subss    xmm5, xmm3
004F8B5B  movss    dword ptr [rip + 0x1b6c15d], xmm3  ; -> 02064CC0
004F8B63  movss    dword ptr [rip + 0x1b6c159], xmm2  ; -> 02064CC4
004F8B6B  movss    dword ptr [rip + 0x1b6c159], xmm4  ; -> 02064CCC
004F8B73  movss    dword ptr [rip + 0x1b6c12d], xmm0  ; -> 02064CA8
004F8B7B  movss    dword ptr [rip + 0x1b6c121], xmm6  ; -> 02064CA4
004F8B83  movss    dword ptr [rip + 0x1b6c115], xmm5  ; -> 02064CA0
004F8B8B  movss    dword ptr [rip + 0x1b6c119], xmm1  ; -> 02064CAC
004F8B93  call     0x22cc20  ; -> 0022CC20 fn
004F8B98  movss    xmm8, dword ptr [rip + 0x1909c9b]  ; -> 01E0283C [f32 1]
004F8BA1  movss    xmm0, dword ptr [rip + 0x1909c87]  ; -> 01E02830 [u32 0x00000000]
004F8BA9  movss    xmm10, dword ptr [rip + 0x1b6c0ee]  ; -> 02064CA0
004F8BB2  movss    xmm7, dword ptr [rip + 0x1b6c0ea]  ; -> 02064CA4
004F8BBA  movaps   xmm2, xmm10
004F8BBE  movss    xmm6, dword ptr [rip + 0x1b6c0e2]  ; -> 02064CA8
004F8BC6  movss    xmm14, dword ptr [rip + 0x1909c65]  ; -> 01E02834 [u32 0x00000000]
004F8BCF  movaps   xmm1, xmm6
004F8BD2  movss    xmm15, dword ptr [rip + 0x1909c5d]  ; -> 01E02838 [u32 0x00000000]
004F8BDB  movss    dword ptr [rip + 0x1b6c0d9], xmm0  ; -> 02064CBC
004F8BE3  movaps   xmm0, xmm8
004F8BE7  mulss    xmm0, xmm8
004F8BEC  mulss    xmm1, xmm6
004F8BF0  movss    dword ptr [rip + 0x1b6c0e4], xmm0  ; -> 02064CDC
004F8BF8  movaps   xmm0, xmm7
004F8BFB  mulss    xmm0, xmm7
004F8BFF  mulss    xmm2, xmm10
004F8C04  mulss    xmm0, xmm8
004F8C09  mulss    xmm1, xmm8
004F8C0E  mulss    xmm2, xmm8
004F8C13  movss    dword ptr [rip + 0x1b6c094], xmm14  ; -> 02064CB0
004F8C1C  movss    dword ptr [rip + 0x1b6c08f], xmm15  ; -> 02064CB4
004F8C25  addss    xmm2, xmm0
004F8C29  movss    dword ptr [rip + 0x1b6c086], xmm8  ; -> 02064CB8
004F8C32  movss    dword ptr [rip + 0x1b6c095], xmm14  ; -> 02064CD0
004F8C3B  movss    dword ptr [rip + 0x1b6c090], xmm15  ; -> 02064CD4
004F8C44  addss    xmm1, xmm2
004F8C48  cvtps2pd xmm0, xmm1
004F8C4B  andps    xmm0, xmm13
004F8C4F  cvtpd2ps xmm0, xmm0
004F8C53  call     0x861f14  ; -> 00861F14 fn
004F8C58  mulss    xmm0, xmm8
004F8C5D  ucomiss  xmm0, xmm11
004F8C61  movss    dword ptr [rip + 0x1b6c06f], xmm0  ; -> 02064CD8
004F8C69  jp       0x4f8c6d  ; -> 004F8C6D
004F8C6B  je       0x4f8c76  ; -> 004F8C76
004F8C6D  movaps   xmm12, xmm8
004F8C71  divss    xmm12, xmm0
004F8C76  mulss    xmm7, xmm12
004F8C7B  movaps   xmm1, xmm14
004F8C7F  mulss    xmm6, xmm12
004F8C84  movaps   xmm0, xmm7
004F8C87  movss    dword ptr [rip + 0x1b6c015], xmm7  ; -> 02064CA4
004F8C8F  mulss    xmm0, xmm15
004F8C94  movss    dword ptr [rip + 0x1b6c00c], xmm6  ; -> 02064CA8
004F8C9C  movaps   xmm9, xmm6
004F8CA0  mulss    xmm10, xmm12
004F8CA5  movss    dword ptr [rip + 0x1b6bfe7], xmm0  ; -> 02064C94
004F8CAD  mulss    xmm0, xmm8
004F8CB2  mulss    xmm1, xmm10
004F8CB7  mulss    xmm9, xmm8
004F8CBC  movss    dword ptr [rip + 0x1b6bfcc], xmm1  ; -> 02064C90
004F8CC4  mulss    xmm1, xmm8
004F8CC9  movss    dword ptr [rip + 0x1b6bfc6], xmm9  ; -> 02064C98
004F8CD2  movss    dword ptr [rip + 0x1b6bfc5], xmm10  ; -> 02064CA0
004F8CDB  addss    xmm1, xmm0
004F8CDF  mulss    xmm9, xmm8
004F8CE4  addss    xmm9, xmm1
004F8CE9  movups   xmm1, xmmword ptr [rip + 0x1b6bfc0]  ; -> 02064CB0
004F8CF0  mulss    xmm7, xmm1
004F8CF4  movaps   xmm0, xmm1
004F8CF7  shufps   xmm0, xmm1, 0x55
004F8CFB  movaps   xmm2, xmm1
004F8CFE  mulss    xmm6, xmm0
004F8D02  shufps   xmm2, xmm1, 0xaa
004F8D06  mulss    xmm2, xmm10
004F8D0B  movss    dword ptr [rip + 0x1b6be0d], xmm6  ; -> 02064B20
004F8D13  movss    dword ptr [rip + 0x1b6be0d], xmm7  ; -> 02064B28
004F8D1B  movss    dword ptr [rip + 0x1b6be01], xmm2  ; -> 02064B24
004F8D23  movups   xmmword ptr [rsp + 0x130], xmm1
004F8D2B  movups   xmm1, xmmword ptr [rip + 0x1b6bf6e]  ; -> 02064CA0
004F8D32  movss    dword ptr [rip + 0x1b6bf61], xmm9  ; -> 02064C9C
004F8D3B  movaps   xmm0, xmm1
004F8D3E  shufps   xmm0, xmm1, 0x55
004F8D42  mulss    xmm0, xmm8
004F8D47  movups   xmmword ptr [rsp + 0x140], xmm1
004F8D4F  subss    xmm6, xmm0
004F8D53  movaps   xmm0, xmm1
004F8D56  shufps   xmm0, xmm1, 0xaa
004F8D5A  mulss    xmm14, xmm0
004F8D5F  movaps   xmm0, xmm15
004F8D63  mulss    xmm0, xmm1
004F8D67  subss    xmm2, xmm14
004F8D6C  movss    dword ptr [rip + 0x1b6bf2c], xmm6  ; -> 02064CA0
004F8D74  mulss    xmm6, xmm6
004F8D78  subss    xmm7, xmm0
004F8D7C  movss    dword ptr [rip + 0x1b6bf20], xmm2  ; -> 02064CA4
004F8D84  mulss    xmm2, xmm2
004F8D88  movss    dword ptr [rip + 0x1b6bf18], xmm7  ; -> 02064CA8
004F8D90  mulss    xmm7, xmm7
004F8D94  movss    dword ptr [rip + 0x1b6bf18], xmm2  ; -> 02064CB4
004F8D9C  movss    dword ptr [rip + 0x1b6bf0c], xmm6  ; -> 02064CB0
004F8DA4  mulss    xmm2, xmm8
004F8DA9  movss    dword ptr [rip + 0x1b6bf07], xmm7  ; -> 02064CB8
004F8DB1  mulss    xmm7, xmm8
004F8DB6  mulss    xmm6, xmm8
004F8DBB  addss    xmm6, xmm2
004F8DBF  addss    xmm7, xmm6
004F8DC3  movss    dword ptr [rip + 0x1b6bd61], xmm6  ; -> 02064B2C
004F8DCB  cvtps2pd xmm0, xmm7
004F8DCE  movss    dword ptr [rip + 0x1b6bee6], xmm7  ; -> 02064CBC
004F8DD6  andps    xmm0, xmm13
004F8DDA  cvtpd2ps xmm0, xmm0
004F8DDE  call     0x861f14  ; -> 00861F14 fn
004F8DE3  movaps   xmm1, xmm0
004F8DE6  ucomiss  xmm1, xmm11
004F8DEA  jp       0x4f8dfa  ; -> 004F8DFA
004F8DEC  jne      0x4f8dfa  ; -> 004F8DFA
004F8DEE  mov      dword ptr [rip + 0x1b6bd08], 0x7f7fffff  ; -> 02064B00
004F8DF8  jmp      0x4f8e0a  ; -> 004F8E0A
004F8DFA  movaps   xmm0, xmm8
004F8DFE  divss    xmm0, xmm1
004F8E02  movss    dword ptr [rip + 0x1b6bcf6], xmm0  ; -> 02064B00
004F8E0A  addss    xmm15, xmm9
004F8E0F  mulss    xmm9, xmm9
004F8E14  subss    xmm8, xmm9
004F8E19  movss    dword ptr [rip + 0x1b6be56], xmm15  ; -> 02064C78
004F8E22  movss    dword ptr [rip + 0x1b6be51], xmm8  ; -> 02064C7C
004F8E2B  call     0x22cc20  ; -> 0022CC20 fn
004F8E30  movss    xmm0, dword ptr [rip + 0x1b6bcc8]  ; -> 02064B00
004F8E38  movss    xmm6, dword ptr [rip + 0x1b6be60]  ; -> 02064CA0
004F8E40  movss    xmm7, dword ptr [rip + 0x1b6be5c]  ; -> 02064CA4
004F8E48  movss    xmm8, dword ptr [rip + 0x1b6be57]  ; -> 02064CA8
004F8E51  mulss    xmm6, xmm0
004F8E55  mulss    xmm7, xmm0
004F8E59  mulss    xmm8, xmm0
004F8E5E  movss    xmm0, dword ptr [rip + 0x1b6be16]  ; -> 02064C7C
004F8E66  cvtps2pd xmm0, xmm0
004F8E69  movss    dword ptr [rip + 0x1b6be2f], xmm6  ; -> 02064CA0
004F8E71  andps    xmm0, xmm13
004F8E75  movss    dword ptr [rip + 0x1b6be27], xmm7  ; -> 02064CA4
004F8E7D  cvtpd2ps xmm0, xmm0
004F8E81  movss    dword ptr [rip + 0x1b6be1e], xmm8  ; -> 02064CA8
004F8E8A  call     0x861f14  ; -> 00861F14 fn
004F8E8F  movups   xmm3, xmmword ptr [rip + 0x1b6be0a]  ; -> 02064CA0
004F8E96  movaps   xmm4, xmm0
004F8E99  movaps   xmm2, xmm7
004F8E9C  mulss    xmm2, xmm6
004F8EA0  movaps   xmm0, xmm7
004F8EA3  mulss    xmm0, xmm8
004F8EA8  movaps   xmm1, xmm6
004F8EAB  shufps   xmm1, xmm1, 0
004F8EAF  mulps    xmm1, xmm3
004F8EB2  movss    dword ptr [rip + 0x1b6bd6e], xmm0  ; -> 02064C28
004F8EBA  movaps   xmm0, xmm8
004F8EBE  shufps   xmm0, xmm0, 0
004F8EC2  mulps    xmm0, xmm3
004F8EC5  movups   xmmword ptr [rip + 0x1b6bd44], xmm1  ; -> 02064C10
004F8ECC  movss    dword ptr [rip + 0x1b6bd4c], xmm2  ; -> 02064C20
004F8ED4  movaps   xmm1, xmm7
004F8ED7  mulss    xmm1, xmm7
004F8EDB  movaps   xmm2, xmm7
004F8EDE  movups   xmmword ptr [rip + 0x1b6bd4b], xmm0  ; -> 02064C30
004F8EE5  movss    xmm0, dword ptr [rip + 0x190994f]  ; -> 01E0283C [f32 1]
004F8EED  subss    xmm0, dword ptr [rip + 0x1b6bda3]  ; -> 02064C98
004F8EF5  movss    dword ptr [rip + 0x1b6bd27], xmm1  ; -> 02064C24
004F8EFD  movaps   xmm1, xmm3
004F8F00  shufps   xmm1, xmm3, 0xff
004F8F04  movss    xmm3, dword ptr [rip + 0x1909924]  ; -> 01E02830 [u32 0x00000000]
004F8F0C  mulss    xmm2, xmm1
004F8F10  movaps   xmm5, xmm3
004F8F13  addss    xmm5, xmm4
004F8F17  movss    dword ptr [rip + 0x1b6bbe1], xmm4  ; -> 02064B00
004F8F1F  movss    xmm4, dword ptr [rip + 0x1909911]  ; -> 01E02838 [u32 0x00000000]
004F8F27  movss    dword ptr [rip + 0x1b6bcfd], xmm2  ; -> 02064C2C
004F8F2F  movaps   xmm2, xmm4
004F8F32  addss    xmm2, dword ptr [rip + 0x1b6bd62]  ; -> 02064C9C
004F8F3A  movss    dword ptr [rip + 0x1b6bd6a], xmm1  ; -> 02064CAC
004F8F42  movaps   xmm1, xmm5
004F8F45  movss    dword ptr [rip + 0x1b6bd2f], xmm0  ; -> 02064C7C
004F8F4D  movaps   xmm0, xmm5
004F8F50  movss    dword ptr [rip + 0x1b6bd18], xmm5  ; -> 02064C70
004F8F58  mulss    xmm5, xmm8
004F8F5D  mulss    xmm0, xmm7
004F8F61  movss    dword ptr [rip + 0x1b6bd0f], xmm2  ; -> 02064C78
004F8F69  addss    xmm2, xmm3
004F8F6D  movss    dword ptr [rip + 0x1b6bd13], xmm5  ; -> 02064C88
004F8F75  addss    xmm5, dword ptr [rip + 0x19098b7]  ; -> 01E02834 [u32 0x00000000]
004F8F7D  subss    xmm4, xmm0
004F8F81  mulss    xmm1, xmm6
004F8F85  movss    dword ptr [rip + 0x1b6bcf7], xmm0  ; -> 02064C84
004F8F8D  movss    dword ptr [rip + 0x1b6bb8b], xmm2  ; -> 02064B20
004F8F95  movss    dword ptr [rip + 0x1b6bb87], xmm5  ; -> 02064B24
004F8F9D  movss    dword ptr [rip + 0x1b6bb83], xmm4  ; -> 02064B28
004F8FA5  movss    dword ptr [rip + 0x1b6bcd3], xmm1  ; -> 02064C80
004F8FAD  call     0x22cc20  ; -> 0022CC20 fn
004F8FB2  movss    xmm0, dword ptr [rip + 0x1b6bc56]  ; -> 02064C10
004F8FBA  movss    xmm2, dword ptr [rip + 0x1b6bcba]  ; -> 02064C7C
004F8FC2  mulss    xmm0, xmm2
004F8FC6  addss    xmm0, dword ptr [rip + 0x1b6bb52]  ; -> 02064B20
004F8FCE  movss    dword ptr [rip + 0x1b6bc3a], xmm0  ; -> 02064C10
004F8FD6  movss    xmm0, dword ptr [rip + 0x1b6bc36]  ; -> 02064C14
004F8FDE  mulss    xmm0, xmm2
004F8FE2  addss    xmm0, dword ptr [rip + 0x1b6bb3a]  ; -> 02064B24
004F8FEA  movss    xmm1, dword ptr [rip + 0x1b6bc26]  ; -> 02064C18
004F8FF2  movss    dword ptr [rip + 0x1b6bc1a], xmm0  ; -> 02064C14
004F8FFA  movss    xmm0, dword ptr [rip + 0x190982e]  ; -> 01E02830 [u32 0x00000000]
004F9002  subss    xmm0, dword ptr [rip + 0x1b6bc7e]  ; -> 02064C88
004F900A  mulss    xmm1, xmm2
004F900E  addss    xmm1, dword ptr [rip + 0x1b6bb12]  ; -> 02064B28
004F9016  movss    dword ptr [rip + 0x1b6bb02], xmm0  ; -> 02064B20
004F901E  movss    dword ptr [rip + 0x1b6bbf2], xmm1  ; -> 02064C18
004F9026  call     0x22cc20  ; -> 0022CC20 fn
004F902B  movss    xmm0, dword ptr [rip + 0x1b6bbed]  ; -> 02064C20
004F9033  movss    xmm2, dword ptr [rip + 0x1b6bc41]  ; -> 02064C7C
004F903B  movss    xmm1, dword ptr [rip + 0x1b6bc35]  ; -> 02064C78
004F9043  movss    xmm5, dword ptr [rip + 0x19097e9]  ; -> 01E02834 [u32 0x00000000]
004F904B  movss    xmm4, dword ptr [rip + 0x1b6bc2d]  ; -> 02064C80
004F9053  addss    xmm1, xmm5
004F9057  mulss    xmm0, xmm2
004F905B  subss    xmm5, xmm4
004F905F  movaps   xmm3, xmm4
004F9062  addss    xmm3, dword ptr [rip + 0x19097ce]  ; -> 01E02838 [u32 0x00000000]
004F906A  addss    xmm0, dword ptr [rip + 0x1b6baae]  ; -> 02064B20
004F9072  movss    dword ptr [rip + 0x1b6baaa], xmm5  ; -> 02064B24
004F907A  movss    dword ptr [rip + 0x1b6baa6], xmm3  ; -> 02064B28
004F9082  movss    dword ptr [rip + 0x1b6bb96], xmm0  ; -> 02064C20
004F908A  movss    xmm0, dword ptr [rip + 0x1b6bb92]  ; -> 02064C24
004F9092  mulss    xmm0, xmm2
004F9096  addss    xmm0, xmm1
004F909A  movss    xmm1, dword ptr [rip + 0x1b6bb86]  ; -> 02064C28
004F90A2  mulss    xmm1, xmm2
004F90A6  movss    dword ptr [rip + 0x1b6bb76], xmm0  ; -> 02064C24
004F90AE  addss    xmm1, xmm3
004F90B2  movss    xmm0, dword ptr [rip + 0x1b6bbca]  ; -> 02064C84
004F90BA  addss    xmm0, dword ptr [rip + 0x190976e]  ; -> 01E02830 [u32 0x00000000]
004F90C2  movss    dword ptr [rip + 0x1b6bb5e], xmm1  ; -> 02064C28
004F90CA  movss    dword ptr [rip + 0x1b6ba4e], xmm0  ; -> 02064B20
004F90D2  call     0x22cc20  ; -> 0022CC20 fn
004F90D7  movss    xmm2, dword ptr [rip + 0x1b6bb35]  ; -> 02064C14
004F90DF  movss    xmm0, dword ptr [rip + 0x1b6bb95]  ; -> 02064C7C
004F90E7  movss    xmm1, dword ptr [rip + 0x1b6bb89]  ; -> 02064C78
004F90EF  addss    xmm1, dword ptr [rip + 0x1909741]  ; -> 01E02838 [u32 0x00000000]
004F90F7  movss    xmm7, dword ptr [rip + 0x1b6bb31]  ; -> 02064C30
004F90FF  movss    xmm8, dword ptr [rip + 0x1b6bb2c]  ; -> 02064C34
004F9108  movss    xmm9, dword ptr [rip + 0x1b6bb27]  ; -> 02064C38
004F9111  movss    xmm6, dword ptr [rip + 0x1b6baf7]  ; -> 02064C10
004F9119  movss    xmm15, dword ptr [rip + 0x1b6bbe2]  ; -> 02064D04
004F9122  movss    xmm14, dword ptr [rip + 0x1b6bbdd]  ; -> 02064D08
004F912B  movss    xmm13, dword ptr [rip + 0x1b6bbd8]  ; -> 02064D0C
004F9134  mulss    xmm7, xmm0
004F9138  mulss    xmm8, xmm0
004F913D  addss    xmm7, dword ptr [rip + 0x1b6b9db]  ; -> 02064B20
004F9145  mulss    xmm9, xmm0
004F914A  movups   xmm0, xmmword ptr [rip + 0x1b6bb8f]  ; -> 02064CE0
004F9151  addss    xmm8, dword ptr [rip + 0x1b6b9ca]  ; -> 02064B24
004F915A  addss    xmm9, xmm1
004F915F  shufps   xmm6, xmm6, 0
004F9163  movss    xmm1, dword ptr [rip + 0x1b6bb91]  ; -> 02064CFC
004F916B  mulps    xmm6, xmm0
004F916E  movss    xmm0, dword ptr [rip + 0x1b6bb7a]  ; -> 02064CF0
004F9176  mulss    xmm0, xmm2
004F917A  movups   xmmword ptr [rip + 0x1b6b99f], xmm6  ; -> 02064B20
004F9181  movss    xmm3, dword ptr [rip + 0x1b6b99b]  ; -> 02064B24
004F9189  addss    xmm6, xmm0
004F918D  movss    xmm4, dword ptr [rip + 0x1b6b993]  ; -> 02064B28
004F9195  movaps   xmm0, xmm2
004F9198  mulss    xmm0, dword ptr [rip + 0x1b6bb54]  ; -> 02064CF4
004F91A0  movss    xmm5, dword ptr [rip + 0x1b6b984]  ; -> 02064B2C
004F91A8  mulss    xmm1, xmm2
004F91AC  addss    xmm3, xmm0
004F91B0  movss    xmm0, dword ptr [rip + 0x1b6bb40]  ; -> 02064CF8
004F91B8  mulss    xmm0, xmm2
004F91BC  movss    xmm2, dword ptr [rip + 0x1b6ba54]  ; -> 02064C18
004F91C4  addss    xmm5, xmm1
004F91C8  movaps   xmm1, xmm2
004F91CB  addss    xmm4, xmm0
004F91CF  mulss    xmm1, xmm15
004F91D4  movaps   xmm0, xmm2
004F91D7  mulss    xmm0, dword ptr [rip + 0x1b6bb21]  ; -> 02064D00
004F91DF  addss    xmm3, xmm1
004F91E3  addss    xmm6, xmm0
004F91E7  movaps   xmm0, xmm2
004F91EA  mulss    xmm0, xmm14
004F91EF  addss    xmm4, xmm0
004F91F3  movss    xmm1, dword ptr [rip + 0x1b6ba21]  ; -> 02064C1C
004F91FB  movss    xmm12, dword ptr [rip + 0x1b6bb0c]  ; -> 02064D10
004F9204  movaps   xmm0, xmm1
004F9207  movss    xmm11, dword ptr [rip + 0x1b6bb08]  ; -> 02064D18
004F9210  movss    xmm10, dword ptr [rip + 0x1b6bb03]  ; -> 02064D1C
004F9219  mulss    xmm0, xmm12
004F921E  mulss    xmm2, xmm13
004F9223  addss    xmm0, xmm6
004F9227  movss    xmm6, dword ptr [rip + 0x1b6b9f1]  ; -> 02064C20
004F922F  shufps   xmm6, xmm6, 0
004F9233  addss    xmm5, xmm2
004F9237  movss    xmm2, dword ptr [rip + 0x1b6b9e5]  ; -> 02064C24
004F923F  movss    dword ptr [rsp + 0x20], xmm0
004F9245  movss    xmm0, dword ptr [rip + 0x1b6bac7]  ; -> 02064D14
004F924D  movss    dword ptr [rsp + 0x24], xmm0
004F9253  mulss    xmm0, xmm1
004F9257  addss    xmm0, xmm3
004F925B  movss    dword ptr [rsp + 0x2c], xmm0
004F9261  movaps   xmm0, xmm1
004F9264  mulss    xmm0, xmm11
004F9269  mulss    xmm1, xmm10
004F926E  addss    xmm0, xmm4
004F9272  addss    xmm1, xmm5
004F9276  movss    dword ptr [rsp + 0x28], xmm0
004F927C  movups   xmm0, xmmword ptr [rip + 0x1b6ba5d]  ; -> 02064CE0
004F9283  movss    dword ptr [rsp + 0x60], xmm1
004F9289  movss    xmm1, dword ptr [rip + 0x1b6ba67]  ; -> 02064CF8
004F9291  mulps    xmm6, xmm0
004F9294  movss    xmm0, dword ptr [rip + 0x1b6ba54]  ; -> 02064CF0
004F929C  mulss    xmm0, xmm2
004F92A0  mulss    xmm1, xmm2
004F92A4  movups   xmmword ptr [rip + 0x1b6b875], xmm6  ; -> 02064B20
004F92AB  movss    xmm5, dword ptr [rip + 0x1b6b879]  ; -> 02064B2C
004F92B3  addss    xmm6, xmm0
004F92B7  movss    xmm3, dword ptr [rip + 0x1b6b865]  ; -> 02064B24
004F92BF  movaps   xmm0, xmm2
004F92C2  mulss    xmm0, dword ptr [rip + 0x1b6ba2a]  ; -> 02064CF4
004F92CA  movss    xmm4, dword ptr [rip + 0x1b6b856]  ; -> 02064B28
004F92D2  addss    xmm4, xmm1
004F92D6  addss    xmm3, xmm0
004F92DA  movss    xmm0, dword ptr [rip + 0x1b6ba1a]  ; -> 02064CFC
004F92E2  mulss    xmm0, xmm2
004F92E6  movss    xmm2, dword ptr [rip + 0x1b6b93a]  ; -> 02064C28
004F92EE  movaps   xmm1, xmm2
004F92F1  addss    xmm5, xmm0
004F92F5  mulss    xmm1, xmm15
004F92FA  movaps   xmm0, xmm2
004F92FD  mulss    xmm0, dword ptr [rip + 0x1b6b9fb]  ; -> 02064D00
004F9305  addss    xmm3, xmm1
004F9309  addss    xmm6, xmm0
004F930D  movaps   xmm0, xmm2
004F9310  mulss    xmm0, xmm14
004F9315  mulss    xmm2, xmm13
004F931A  addss    xmm4, xmm0
004F931E  movss    xmm0, dword ptr [rip + 0x1b6b906]  ; -> 02064C2C
004F9326  movaps   xmm1, xmm0
004F9329  mulss    xmm1, xmm12
004F932E  addss    xmm5, xmm2
004F9332  addss    xmm1, xmm6
004F9336  movss    dword ptr [rsp + 0x64], xmm1
004F933C  movss    xmm1, dword ptr [rsp + 0x24]
004F9342  mulss    xmm1, xmm0
004F9346  addss    xmm1, xmm3
004F934A  movss    dword ptr [rsp + 0x68], xmm1
004F9350  movaps   xmm1, xmm0
004F9353  mulss    xmm0, xmm10
004F9358  mulss    xmm1, xmm11
004F935D  addss    xmm0, xmm5
004F9361  movaps   xmm5, xmm7
004F9364  shufps   xmm5, xmm5, 0
004F9368  addss    xmm1, xmm4
004F936C  movss    dword ptr [rsp + 0x70], xmm0
004F9372  movups   xmm0, xmmword ptr [rip + 0x1b6b967]  ; -> 02064CE0
004F9379  movss    dword ptr [rsp + 0x6c], xmm1
004F937F  mulps    xmm5, xmm0
004F9382  movss    xmm0, dword ptr [rip + 0x1b6b966]  ; -> 02064CF0
004F938A  mulss    xmm0, xmm8
004F938F  movups   xmmword ptr [rip + 0x1b6b78a], xmm5  ; -> 02064B20
004F9396  addss    xmm5, xmm0
004F939A  movaps   xmm0, xmm8
004F939E  mulss    xmm0, dword ptr [rip + 0x1b6b94e]  ; -> 02064CF4
004F93A6  movss    xmm2, dword ptr [rip + 0x1b6b776]  ; -> 02064B24
004F93AE  movss    xmm4, dword ptr [rip + 0x1b6b776]  ; -> 02064B2C
004F93B6  addss    xmm2, xmm0
004F93BA  movss    xmm3, dword ptr [rip + 0x1b6b766]  ; -> 02064B28
004F93C2  movss    xmm0, dword ptr [rip + 0x1b6b932]  ; -> 02064CFC
004F93CA  movss    xmm1, dword ptr [rip + 0x1b6b926]  ; -> 02064CF8
004F93D2  mulss    xmm0, xmm8
004F93D7  movss    xmm7, dword ptr [rip + 0x1b6b8ed]  ; -> 02064CCC
004F93DF  movss    xmm6, dword ptr [rip + 0x1b6b8d9]  ; -> 02064CC0
004F93E7  addss    xmm4, xmm0
004F93EB  mulss    xmm1, xmm8
004F93F0  movss    xmm8, dword ptr [rip + 0x1b6b843]  ; -> 02064C3C
004F93F9  movaps   xmm0, xmm9
004F93FD  mulss    xmm0, dword ptr [rip + 0x1b6b8fb]  ; -> 02064D00
004F9405  addss    xmm3, xmm1
004F9409  shufps   xmm6, xmm6, 0
004F940D  movaps   xmm1, xmm9
004F9411  addss    xmm5, xmm0
004F9415  mulss    xmm1, xmm15
004F941A  movaps   xmm0, xmm9
004F941E  mulss    xmm9, xmm13
004F9423  mulss    xmm0, xmm14
004F9428  addss    xmm2, xmm1
004F942C  movss    xmm1, dword ptr [rip + 0x1b6b890]  ; -> 02064CC4
004F9434  addss    xmm4, xmm9
004F9439  movss    xmm9, dword ptr [rsp + 0x24]
004F9440  addss    xmm3, xmm0
004F9444  movaps   xmm0, xmm8
004F9448  mulss    xmm0, xmm12
004F944D  addss    xmm0, xmm5
004F9451  movss    dword ptr [rsp + 0x74], xmm0
004F9457  movaps   xmm0, xmm9
004F945B  mulss    xmm0, xmm8
004F9460  mulss    xmm9, xmm7
004F9465  addss    xmm0, xmm2
004F9469  movss    xmm2, dword ptr [rip + 0x1b6b857]  ; -> 02064CC8
004F9471  movss    dword ptr [rsp + 0x78], xmm0
004F9477  movaps   xmm0, xmm8
004F947B  mulss    xmm0, xmm11
004F9480  mulss    xmm8, xmm10
004F9485  addss    xmm0, xmm3
004F9489  addss    xmm8, xmm4
004F948E  movss    dword ptr [rsp + 0x34], xmm0
004F9494  movups   xmm0, xmmword ptr [rip + 0x1b6b845]  ; -> 02064CE0
004F949B  mulps    xmm6, xmm0
004F949E  movss    xmm0, dword ptr [rip + 0x1b6b84a]  ; -> 02064CF0
004F94A6  mulss    xmm0, xmm1
004F94AA  movups   xmmword ptr [rip + 0x1b6b66f], xmm6  ; -> 02064B20
004F94B1  movss    xmm3, dword ptr [rip + 0x1b6b66b]  ; -> 02064B24
004F94B9  addss    xmm6, xmm0
004F94BD  movss    xmm4, dword ptr [rip + 0x1b6b663]  ; -> 02064B28
004F94C5  movaps   xmm0, xmm1
004F94C8  mulss    xmm0, dword ptr [rip + 0x1b6b824]  ; -> 02064CF4
004F94D0  movss    xmm5, dword ptr [rip + 0x1b6b654]  ; -> 02064B2C
004F94D8  addss    xmm3, xmm0
004F94DC  movss    xmm0, dword ptr [rip + 0x1b6b814]  ; -> 02064CF8
004F94E4  mulss    xmm0, xmm1
004F94E8  addss    xmm4, xmm0
004F94EC  movss    xmm0, dword ptr [rip + 0x1b6b808]  ; -> 02064CFC
004F94F4  mulss    xmm0, xmm1
004F94F8  movaps   xmm1, xmm2
004F94FB  mulss    xmm1, xmm15
004F9500  addss    xmm5, xmm0
004F9504  movaps   xmm0, xmm2
004F9507  mulss    xmm0, dword ptr [rip + 0x1b6b7f1]  ; -> 02064D00
004F950F  addss    xmm3, xmm1
004F9513  addss    xmm6, xmm0
004F9517  movaps   xmm0, xmm2
004F951A  mulss    xmm0, xmm14
004F951F  addss    xmm9, xmm3
004F9524  mulss    xmm2, xmm13
004F9529  addss    xmm4, xmm0
004F952D  movaps   xmm0, xmm7
004F9530  mulss    xmm0, xmm12
004F9535  movaps   xmm12, xmm7
004F9539  mulss    xmm12, xmm11
004F953E  addss    xmm5, xmm2
004F9542  addss    xmm0, xmm6
004F9546  movss    dword ptr [rsp + 0x24], xmm9
004F954D  addss    xmm12, xmm4
004F9552  movss    dword ptr [rsp + 0x38], xmm0
004F9558  movsx    edx, word ptr [rip + 0x1b6b5ad]  ; -> 02064B0C
004F955F  movss    xmm2, dword ptr [rsp + 0x2c]
004F9565  movaps   xmm1, xmm2
004F9568  mulss    xmm7, xmm10
004F956D  lea      eax, [rdx + 0x19]
004F9570  shl      eax, 4
004F9573  movsxd   rcx, eax
004F9576  addss    xmm7, xmm5
004F957A  movss    xmm5, dword ptr [rsp + 0x20]
004F9580  lea      eax, [rdx + 0x1a]
004F9583  shl      eax, 4
004F9586  shufps   xmm5, xmm5, 0
004F958A  movups   xmm3, xmmword ptr [rcx + r15]
004F958F  movsxd   rcx, eax
004F9592  lea      eax, [rdx + 0x1b]
004F9595  shl      eax, 4
004F9598  mulps    xmm5, xmm3
004F959B  movups   xmm11, xmmword ptr [rcx + r15]
004F95A0  movsxd   rcx, eax
004F95A3  lea      eax, [rdx + 0x1c]
004F95A6  shl      eax, 4
004F95A9  movups   xmmword ptr [rip + 0x1b6b570], xmm5  ; -> 02064B20
004F95B0  movss    xmm6, dword ptr [rip + 0x1b6b570]  ; -> 02064B28
004F95B8  movaps   xmm13, xmm11
004F95BC  movups   xmm10, xmmword ptr [rcx + r15]
004F95C1  movsxd   rcx, eax
004F95C4  lea      eax, [rdx + 8]
004F95C7  movss    xmm9, dword ptr [rip + 0x1b6b554]  ; -> 02064B24
004F95D0  movaps   xmm4, xmm11
004F95D4  shl      eax, 4
004F95D7  movaps   xmm14, xmm11
004F95DB  shufps   xmm4, xmm11, 0x55
004F95E0  movaps   xmm15, xmm10
004F95E4  movups   xmm0, xmmword ptr [rcx + r15]
004F95E9  movsxd   rcx, eax
004F95EC  lea      eax, [rdx + 9]
004F95EF  mulss    xmm1, xmm4
004F95F3  shl      eax, 4
004F95F6  movups   xmmword ptr [rip + 0x1b6b713], xmm0  ; -> 02064D10
004F95FD  movups   xmm0, xmmword ptr [rcx + r15]
004F9602  movsxd   rcx, eax
004F9605  addss    xmm9, xmm1
004F960A  shufps   xmm13, xmm11, 0xaa
004F960F  movss    xmm1, dword ptr [rip + 0x1b6b515]  ; -> 02064B2C
004F9617  movups   xmmword ptr [rip + 0x1b6b672], xmm0  ; -> 02064C90
004F961E  movaps   xmm0, xmm11
004F9622  shufps   xmm15, xmm10, 0x55
004F9627  mulss    xmm0, xmm2
004F962B  movups   xmmword ptr [rip + 0x1b6b6bd], xmm11  ; -> 02064CF0
004F9633  addss    xmm5, xmm0
004F9637  shufps   xmm14, xmm11, 0xff
004F963C  movaps   xmm0, xmm13
004F9640  movss    dword ptr [rip + 0x1b6b6a7], xmm11  ; -> 02064CF0
004F9649  mulss    xmm0, xmm2
004F964D  movss    dword ptr [rip + 0x1b6b69f], xmm4  ; -> 02064CF4
004F9655  movss    dword ptr [rip + 0x1b6b69a], xmm13  ; -> 02064CF8
004F965E  addss    xmm6, xmm0
004F9662  movaps   xmmword ptr [rsp + 0x80], xmm4
004F966A  movaps   xmm0, xmm14
004F966E  movaps   xmmword ptr [rsp + 0x90], xmm15
004F9677  mulss    xmm0, xmm2
004F967B  movss    xmm2, dword ptr [rsp + 0x28]
004F9681  movups   xmmword ptr [rip + 0x1b6b658], xmm3  ; -> 02064CE0
004F9688  addss    xmm1, xmm0
004F968C  movups   xmm0, xmmword ptr [rcx + r15]
004F9691  movups   xmmword ptr [rip + 0x1b6b667], xmm10  ; -> 02064D00
004F9699  movups   xmmword ptr [rip + 0x1b6b600], xmm0  ; -> 02064CA0
004F96A0  movss    dword ptr [rsp + 0x30], xmm1
004F96A6  movaps   xmm0, xmm2
004F96A9  mulss    xmm0, xmm15
004F96AE  movaps   xmm1, xmm2
004F96B1  mulss    xmm1, xmm10
004F96B6  addss    xmm9, xmm0
004F96BB  movaps   xmm0, xmm10
004F96BF  shufps   xmm0, xmm10, 0xaa
004F96C4  addss    xmm5, xmm1
004F96C8  movaps   xmmword ptr [rsp + 0x40], xmm0
004F96CD  movaps   xmm1, xmm2
004F96D0  mulss    xmm1, xmm0
004F96D4  addss    xmm6, xmm1
004F96D8  movss    dword ptr [rsp + 0x20], xmm6
004F96DE  mov      edx, dword ptr [rip + 0x1b6b418]  ; -> 02064AFC
004F96E4  movaps   xmm0, xmm10
004F96E8  shufps   xmm0, xmm10, 0xff
004F96ED  mulss    xmm2, xmm0
004F96F1  movaps   xmmword ptr [rsp + 0x50], xmm0
004F96F6  movss    xmm0, dword ptr [rsp + 0x30]
004F96FC  addss    xmm0, xmm2
004F9700  movss    dword ptr [rsp + 0x30], xmm0
004F9706  test     edx, edx
004F9708  je       0x4f9733  ; -> 004F9733
004F970A  mov      eax, dword ptr [rip + 0x1909118]  ; -> 01E02828 [f32 1]
004F9710  mov      ecx, eax
004F9712  shr      ecx, 0x12
004F9715  xor      ecx, eax
004F9717  and      eax, 0x3fffff
004F971C  or       eax, 0x1fc00000
004F9721  shr      ecx, 4
004F9724  add      eax, eax
004F9726  and      ecx, 1
004F9729  or       ecx, eax
004F972B  mov      dword ptr [rip + 0x19090f7], ecx  ; -> 01E02828 [f32 1]
004F9731  jmp      0x4f9739  ; -> 004F9739
004F9733  mov      ecx, dword ptr [rip + 0x19090ef]  ; -> 01E02828 [f32 1]
004F9739  movss    xmm2, dword ptr [rsp + 0x60]
004F973F  movss    xmm6, dword ptr [rip + 0x1b6b5cd]  ; -> 02064D14
004F9747  movaps   xmm0, xmm2
004F974A  mulss    xmm0, dword ptr [rip + 0x1b6b5be]  ; -> 02064D10
004F9752  movaps   xmm1, xmm2
004F9755  mulss    xmm1, dword ptr [rip + 0x1b6b5bb]  ; -> 02064D18
004F975D  addss    xmm0, xmm5
004F9761  addss    xmm1, dword ptr [rsp + 0x20]
004F9767  movss    dword ptr [rip + 0x1b6b4a1], xmm0  ; -> 02064C10
004F976F  movaps   xmm0, xmm6
004F9772  mulss    xmm0, xmm2
004F9776  mulss    xmm2, dword ptr [rip + 0x1b6b59e]  ; -> 02064D1C
004F977E  movss    dword ptr [rip + 0x1b6b492], xmm1  ; -> 02064C18
004F9786  addss    xmm0, xmm9
004F978B  addss    xmm2, dword ptr [rsp + 0x30]
004F9791  movss    dword ptr [rip + 0x1b6b47b], xmm0  ; -> 02064C14
004F9799  movss    dword ptr [rip + 0x1b6b47b], xmm2  ; -> 02064C1C
004F97A1  test     edx, edx
004F97A3  je       0x4f97c6  ; -> 004F97C6
004F97A5  mov      eax, ecx
004F97A7  shr      ecx, 0x12
004F97AA  xor      ecx, eax
004F97AC  and      eax, 0x3fffff
004F97B1  or       eax, 0x1fc00000
004F97B6  shr      ecx, 4
004F97B9  add      eax, eax
004F97BB  and      ecx, 1
004F97BE  or       ecx, eax
004F97C0  mov      dword ptr [rip + 0x1909062], ecx  ; -> 01E02828 [f32 1]
004F97C6  movss    xmm0, dword ptr [rsp + 0x64]
004F97CC  shufps   xmm0, xmm0, 0
004F97D0  mulps    xmm0, xmm3
004F97D3  movups   xmmword ptr [rip + 0x1b6b346], xmm0  ; -> 02064B20
004F97DA  test     edx, edx
004F97DC  je       0x4f97ff  ; -> 004F97FF
004F97DE  mov      eax, ecx
004F97E0  shr      ecx, 0x12
004F97E3  xor      ecx, eax
004F97E5  and      eax, 0x3fffff
004F97EA  or       eax, 0x1fc00000
004F97EF  shr      ecx, 4
004F97F2  add      eax, eax
004F97F4  and      ecx, 1
004F97F7  or       ecx, eax
004F97F9  mov      dword ptr [rip + 0x1909029], ecx  ; -> 01E02828 [f32 1]
004F97FF  movss    xmm2, dword ptr [rsp + 0x68]
004F9805  movaps   xmm0, xmm11
004F9809  movss    xmm3, dword ptr [rip + 0x1b6b30f]  ; -> 02064B20
004F9811  movaps   xmm1, xmm2
004F9814  movss    xmm5, dword ptr [rip + 0x1b6b30c]  ; -> 02064B28
004F981C  movss    xmm9, dword ptr [rip + 0x1b6b307]  ; -> 02064B2C
004F9825  mulss    xmm1, xmm4
004F9829  movss    xmm4, dword ptr [rip + 0x1b6b2f3]  ; -> 02064B24
004F9831  mulss    xmm0, xmm2
004F9835  addss    xmm4, xmm1
004F9839  movaps   xmm1, xmm14
004F983D  mulss    xmm1, xmm2
004F9841  addss    xmm3, xmm0
004F9845  movaps   xmm0, xmm13
004F9849  mulss    xmm0, xmm2
004F984D  addss    xmm9, xmm1
004F9852  addss    xmm5, xmm0
004F9856  test     edx, edx
004F9858  je       0x4f987b  ; -> 004F987B
004F985A  mov      eax, ecx
004F985C  shr      ecx, 0x12
004F985F  xor      ecx, eax
004F9861  and      eax, 0x3fffff
004F9866  or       eax, 0x1fc00000
004F986B  shr      ecx, 4
004F986E  add      eax, eax
004F9870  and      ecx, 1
004F9873  or       ecx, eax
004F9875  mov      dword ptr [rip + 0x1908fad], ecx  ; -> 01E02828 [f32 1]
004F987B  movss    xmm2, dword ptr [rsp + 0x6c]
004F9881  movaps   xmm0, xmm2
004F9884  movaps   xmm1, xmm2
004F9887  mulss    xmm0, xmm10
004F988C  mulss    xmm1, xmm15
004F9891  movss    xmm15, dword ptr [rip + 0x17f230e]  ; -> 01CEBBA8 [f32 1]
004F989A  addss    xmm3, xmm0
004F989E  movaps   xmm0, xmm2
004F98A1  mulss    xmm2, dword ptr [rsp + 0x50]
004F98A7  mulss    xmm0, dword ptr [rsp + 0x40]
004F98AD  addss    xmm4, xmm1
004F98B1  addss    xmm9, xmm2
004F98B6  addss    xmm5, xmm0
004F98BA  test     edx, edx
004F98BC  jne      0x4f98c4  ; -> 004F98C4
004F98BE  movaps   xmm10, xmm15
004F98C2  jmp      0x4f98ee  ; -> 004F98EE
004F98C4  mov      eax, ecx
004F98C6  shr      ecx, 0x12
004F98C9  xor      ecx, eax
004F98CB  and      eax, 0x3fffff
004F98D0  or       eax, 0x1fc00000
004F98D5  shr      ecx, 4
004F98D8  add      eax, eax
004F98DA  and      ecx, 1
004F98DD  or       ecx, eax
004F98DF  mov      dword ptr [rip + 0x1908f43], ecx  ; -> 01E02828 [f32 1]
004F98E5  movss    xmm10, dword ptr [rip + 0x1908f3a]  ; -> 01E02828 [f32 1]
004F98EE  movss    xmm2, dword ptr [rsp + 0x70]
004F98F4  movaps   xmm1, xmm6
004F98F7  mulss    xmm1, xmm2
004F98FB  movaps   xmm0, xmm2
004F98FE  mulss    xmm0, dword ptr [rip + 0x1b6b40a]  ; -> 02064D10
004F9906  addss    xmm1, xmm4
004F990A  addss    xmm0, xmm3
004F990E  movss    dword ptr [rip + 0x1b6b30e], xmm1  ; -> 02064C24
004F9916  movss    dword ptr [rip + 0x1b6b302], xmm0  ; -> 02064C20
004F991E  movaps   xmm0, xmm2
004F9921  mulss    xmm0, dword ptr [rip + 0x1b6b3ef]  ; -> 02064D18
004F9929  mulss    xmm2, dword ptr [rip + 0x1b6b3eb]  ; -> 02064D1C
004F9931  addss    xmm0, xmm5
004F9935  addss    xmm2, xmm9
004F993A  movss    dword ptr [rip + 0x1b6b2e6], xmm0  ; -> 02064C28
004F9942  movss    dword ptr [rip + 0x1b6b2e2], xmm2  ; -> 02064C2C
004F994A  test     edx, edx
004F994C  je       0x4f996f  ; -> 004F996F
004F994E  mov      eax, ecx
004F9950  shr      ecx, 0x12
004F9953  xor      ecx, eax
004F9955  and      eax, 0x3fffff
004F995A  or       eax, 0x1fc00000
004F995F  shr      ecx, 4
004F9962  add      eax, eax
004F9964  and      ecx, 1
004F9967  or       ecx, eax
004F9969  mov      dword ptr [rip + 0x1908eb9], ecx  ; -> 01E02828 [f32 1]
004F996F  movss    xmm0, dword ptr [rsp + 0x74]
004F9975  shufps   xmm0, xmm0, 0
004F9979  movups   xmm1, xmmword ptr [rip + 0x1b6b360]  ; -> 02064CE0
004F9980  mulps    xmm0, xmm1
004F9983  movups   xmmword ptr [rip + 0x1b6b196], xmm0  ; -> 02064B20
004F998A  test     edx, edx
004F998C  je       0x4f99af  ; -> 004F99AF
004F998E  mov      eax, ecx
004F9990  shr      ecx, 0x12
004F9993  xor      ecx, eax
004F9995  and      eax, 0x3fffff
004F999A  or       eax, 0x1fc00000
004F999F  shr      ecx, 4
004F99A2  add      eax, eax
004F99A4  and      ecx, 1
004F99A7  or       ecx, eax
004F99A9  mov      dword ptr [rip + 0x1908e79], ecx  ; -> 01E02828 [f32 1]
004F99AF  movss    xmm5, dword ptr [rsp + 0x78]
004F99B5  movaps   xmm0, xmm11
004F99B9  movss    xmm2, dword ptr [rip + 0x1b6b15f]  ; -> 02064B20
004F99C1  movaps   xmm1, xmm5
004F99C4  mulss    xmm1, dword ptr [rsp + 0x80]
004F99CD  movss    xmm3, dword ptr [rip + 0x1b6b14f]  ; -> 02064B24
004F99D5  movss    xmm4, dword ptr [rip + 0x1b6b14b]  ; -> 02064B28
004F99DD  mulss    xmm0, xmm5
004F99E1  addss    xmm3, xmm1
004F99E5  movaps   xmm1, xmm14
004F99E9  mulss    xmm1, xmm5
004F99ED  addss    xmm2, xmm0
004F99F1  movaps   xmm0, xmm13
004F99F5  mulss    xmm0, xmm5
004F99F9  movss    xmm5, dword ptr [rip + 0x1b6b12b]  ; -> 02064B2C
004F9A01  addss    xmm5, xmm1
004F9A05  addss    xmm4, xmm0
004F9A09  test     edx, edx
004F9A0B  je       0x4f9a2e  ; -> 004F9A2E
004F9A0D  mov      eax, ecx
004F9A0F  shr      ecx, 0x12
004F9A12  xor      ecx, eax
004F9A14  and      eax, 0x3fffff
004F9A19  or       eax, 0x1fc00000
004F9A1E  shr      ecx, 4
004F9A21  add      eax, eax
004F9A23  and      ecx, 1
004F9A26  or       ecx, eax
004F9A28  mov      dword ptr [rip + 0x1908dfa], ecx  ; -> 01E02828 [f32 1]
004F9A2E  movss    xmm9, dword ptr [rsp + 0x34]
004F9A35  movaps   xmm0, xmm9
004F9A39  movaps   xmm1, xmm9
004F9A3D  mulss    xmm0, dword ptr [rip + 0x1b6b2bb]  ; -> 02064D00
004F9A45  mulss    xmm1, dword ptr [rsp + 0x90]
004F9A4E  addss    xmm2, xmm0
004F9A52  movaps   xmm0, xmm9
004F9A56  mulss    xmm0, dword ptr [rsp + 0x40]
004F9A5C  mulss    xmm9, dword ptr [rsp + 0x50]
004F9A63  addss    xmm3, xmm1
004F9A67  addss    xmm4, xmm0
004F9A6B  addss    xmm5, xmm9
004F9A70  test     edx, edx
004F9A72  je       0x4f9a95  ; -> 004F9A95
004F9A74  mov      eax, ecx
004F9A76  shr      ecx, 0x12
004F9A79  xor      ecx, eax
004F9A7B  and      eax, 0x3fffff
004F9A80  or       eax, 0x1fc00000
004F9A85  shr      ecx, 4
004F9A88  add      eax, eax
004F9A8A  and      ecx, 1
004F9A8D  or       ecx, eax
004F9A8F  mov      dword ptr [rip + 0x1908d93], ecx  ; -> 01E02828 [f32 1]
004F9A95  movss    xmm9, dword ptr [rip + 0x1b6b272]  ; -> 02064D10
004F9A9E  movaps   xmm0, xmm8
004F9AA2  mulss    xmm0, xmm9
004F9AA7  movaps   xmm1, xmm6
004F9AAA  mulss    xmm1, xmm8
004F9AAF  addss    xmm0, xmm2
004F9AB3  addss    xmm1, xmm3
004F9AB7  movss    dword ptr [rip + 0x1b6b171], xmm0  ; -> 02064C30
004F9ABF  movaps   xmm0, xmm8
004F9AC3  mulss    xmm0, dword ptr [rip + 0x1b6b24d]  ; -> 02064D18
004F9ACB  mulss    xmm8, dword ptr [rip + 0x1b6b248]  ; -> 02064D1C
004F9AD4  movss    dword ptr [rip + 0x1b6b158], xmm1  ; -> 02064C34
004F9ADC  addss    xmm0, xmm4
004F9AE0  addss    xmm8, xmm5
004F9AE5  movss    dword ptr [rip + 0x1b6b14b], xmm0  ; -> 02064C38
004F9AED  movss    dword ptr [rip + 0x1b6b146], xmm8  ; -> 02064C3C
004F9AF6  test     edx, edx
004F9AF8  jne      0x4f9b00  ; -> 004F9B00
004F9AFA  movaps   xmm8, xmm15
004F9AFE  jmp      0x4f9b2a  ; -> 004F9B2A
004F9B00  mov      eax, ecx
004F9B02  shr      ecx, 0x12
004F9B05  xor      ecx, eax
004F9B07  and      eax, 0x3fffff
004F9B0C  or       eax, 0x1fc00000
004F9B11  shr      ecx, 4
004F9B14  add      eax, eax
004F9B16  and      ecx, 1
004F9B19  or       ecx, eax
004F9B1B  mov      dword ptr [rip + 0x1908d07], ecx  ; -> 01E02828 [f32 1]
004F9B21  movss    xmm8, dword ptr [rip + 0x1908cfe]  ; -> 01E02828 [f32 1]
004F9B2A  movss    xmm1, dword ptr [rsp + 0x24]
004F9B30  subss    xmm10, xmm15
004F9B35  movss    xmm5, dword ptr [rsp + 0x38]
004F9B3B  subss    xmm8, xmm15
004F9B40  mulss    xmm11, xmm1
004F9B45  mov      dword ptr [rip + 0x1b6afb5], 0x3f800000  ; -> 02064B04
004F9B4F  mulss    xmm13, xmm1
004F9B54  mulss    xmm14, xmm1
004F9B59  shufps   xmm5, xmm5, 0
004F9B5D  mulss    xmm6, xmm7
004F9B61  movss    dword ptr [rip + 0x1b6b006], xmm10  ; -> 02064B70
004F9B6A  movss    dword ptr [rip + 0x1b6b00d], xmm8  ; -> 02064B80
004F9B73  movups   xmm0, xmmword ptr [rip + 0x1b6b166]  ; -> 02064CE0
004F9B7A  mulps    xmm5, xmm0
004F9B7D  movaps   xmm0, xmm1
004F9B80  mulss    xmm0, dword ptr [rsp + 0x80]
004F9B89  movaps   xmm1, xmm12
004F9B8D  mulss    xmm1, dword ptr [rsp + 0x90]
004F9B96  movups   xmmword ptr [rip + 0x1b6af83], xmm5  ; -> 02064B20
004F9B9D  movss    xmm2, dword ptr [rip + 0x1b6af7f]  ; -> 02064B24
004F9BA5  addss    xmm5, xmm11
004F9BAA  movss    xmm3, dword ptr [rip + 0x1b6af76]  ; -> 02064B28
004F9BB2  addss    xmm2, xmm0
004F9BB6  movss    xmm4, dword ptr [rip + 0x1b6af6e]  ; -> 02064B2C
004F9BBE  movaps   xmm0, xmm12
004F9BC2  mulss    xmm0, dword ptr [rip + 0x1b6b136]  ; -> 02064D00
004F9BCA  addss    xmm3, xmm13
004F9BCF  addss    xmm4, xmm14
004F9BD4  addss    xmm2, xmm1
004F9BD8  movss    xmm1, dword ptr [rip + 0x1b6b0b4]  ; -> 02064C94
004F9BE0  mulss    xmm1, xmm10
004F9BE5  addss    xmm5, xmm0
004F9BE9  movaps   xmm0, xmm12
004F9BED  mulss    xmm12, dword ptr [rsp + 0x50]
004F9BF4  mulss    xmm0, dword ptr [rsp + 0x40]
004F9BFA  addss    xmm6, xmm2
004F9BFE  movss    dword ptr [rip + 0x1b6af1a], xmm5  ; -> 02064B20
004F9C06  addss    xmm4, xmm12
004F9C0B  movss    dword ptr [rip + 0x1b6af11], xmm2  ; -> 02064B24
004F9C13  movss    dword ptr [rip + 0x1b6b079], xmm1  ; -> 02064C94
004F9C1B  addss    xmm3, xmm0
004F9C1F  movss    dword ptr [rip + 0x1b6b01d], xmm6  ; -> 02064C44
004F9C27  movaps   xmm0, xmm7
004F9C2A  mulss    xmm0, xmm9
004F9C2F  movss    dword ptr [rip + 0x1b6aef5], xmm4  ; -> 02064B2C
004F9C37  movss    dword ptr [rip + 0x1b6aee9], xmm3  ; -> 02064B28
004F9C3F  addss    xmm0, xmm5
004F9C43  movss    dword ptr [rip + 0x1b6aff5], xmm0  ; -> 02064C40
004F9C4B  movaps   xmm0, xmm7
004F9C4E  mulss    xmm0, dword ptr [rip + 0x1b6b0c2]  ; -> 02064D18
004F9C56  mulss    xmm7, dword ptr [rip + 0x1b6b0be]  ; -> 02064D1C
004F9C5E  addss    xmm0, xmm3
004F9C62  addss    xmm7, xmm4
004F9C66  movss    dword ptr [rip + 0x1b6afda], xmm0  ; -> 02064C48
004F9C6E  movss    dword ptr [rip + 0x1b6afd6], xmm7  ; -> 02064C4C
004F9C76  test     edx, edx
004F9C78  je       0x4f9c9b  ; -> 004F9C9B
004F9C7A  mov      eax, ecx
004F9C7C  shr      ecx, 0x12
004F9C7F  xor      ecx, eax
004F9C81  and      eax, 0x3fffff
004F9C86  or       eax, 0x1fc00000
004F9C8B  shr      ecx, 4
004F9C8E  add      eax, eax
004F9C90  and      ecx, 1
004F9C93  or       ecx, eax
004F9C95  mov      dword ptr [rip + 0x1908b8d], ecx  ; -> 01E02828 [f32 1]
004F9C9B  movss    xmm0, dword ptr [rip + 0x1b6b001]  ; -> 02064CA4
004F9CA3  mulss    xmm0, xmm8
004F9CA8  movss    dword ptr [rip + 0x1b6aff4], xmm0  ; -> 02064CA4
004F9CB0  test     edx, edx
004F9CB2  je       0x4f9cd5  ; -> 004F9CD5
004F9CB4  mov      eax, ecx
004F9CB6  shr      ecx, 0x12
004F9CB9  xor      ecx, eax
004F9CBB  and      eax, 0x3fffff
004F9CC0  or       eax, 0x1fc00000
004F9CC5  shr      ecx, 4
004F9CC8  add      eax, eax
004F9CCA  and      ecx, 1
004F9CCD  or       ecx, eax
004F9CCF  mov      dword ptr [rip + 0x1908b53], ecx  ; -> 01E02828 [f32 1]
004F9CD5  movss    xmm2, dword ptr [rip + 0x1b6afb3]  ; -> 02064C90
004F9CDD  addss    xmm2, xmm1
004F9CE1  movss    dword ptr [rip + 0x1b6afa7], xmm2  ; -> 02064C90
004F9CE9  test     edx, edx
004F9CEB  je       0x4f9d0e  ; -> 004F9D0E
004F9CED  mov      eax, ecx
004F9CEF  shr      ecx, 0x12
004F9CF2  xor      ecx, eax
004F9CF4  and      eax, 0x3fffff
004F9CF9  or       eax, 0x1fc00000
004F9CFE  shr      ecx, 4
004F9D01  add      eax, eax
004F9D03  and      ecx, 1
004F9D06  or       ecx, eax
004F9D08  mov      dword ptr [rip + 0x1908b1a], ecx  ; -> 01E02828 [f32 1]
004F9D0E  addss    xmm0, dword ptr [rip + 0x1b6af8a]  ; -> 02064CA0
004F9D16  movss    dword ptr [rip + 0x1b6af92], xmm0  ; -> 02064CB0
004F9D1E  test     edx, edx
004F9D20  je       0x4f9d43  ; -> 004F9D43
004F9D22  mov      eax, ecx
004F9D24  shr      ecx, 0x12
004F9D27  xor      ecx, eax
004F9D29  and      eax, 0x3fffff
004F9D2E  or       eax, 0x1fc00000
004F9D33  shr      ecx, 4
004F9D36  add      eax, eax
004F9D38  and      ecx, 1
004F9D3B  or       ecx, eax
004F9D3D  mov      dword ptr [rip + 0x1908ae5], ecx  ; -> 01E02828 [f32 1]
004F9D43  movss    xmm0, dword ptr [rip + 0x1b6af85]  ; -> 02064CD0
004F9D4B  movss    xmm1, dword ptr [rip + 0x1b6af81]  ; -> 02064CD4
004F9D53  mulss    xmm0, xmm2
004F9D57  mulss    xmm1, xmm2
004F9D5B  mulss    xmm2, dword ptr [rip + 0x1b6af75]  ; -> 02064CD8
004F9D63  movss    dword ptr [rip + 0x1b6af75], xmm0  ; -> 02064CE0
004F9D6B  movss    dword ptr [rip + 0x1b6af71], xmm1  ; -> 02064CE4
004F9D73  movss    dword ptr [rip + 0x1b6af6d], xmm2  ; -> 02064CE8
004F9D7B  test     edx, edx
004F9D7D  jne      0x4f9d85  ; -> 004F9D85
004F9D7F  movaps   xmm0, xmm15
004F9D83  jmp      0x4f9db0  ; -> 004F9DB0
004F9D85  mov      eax, ecx
004F9D87  shr      eax, 0x12
004F9D8A  xor      eax, ecx
004F9D8C  and      ecx, 0x3fffff
004F9D92  or       ecx, 0x1fc00000
004F9D98  shr      eax, 4
004F9D9B  add      ecx, ecx
004F9D9D  and      eax, 1
004F9DA0  or       eax, ecx
004F9DA2  mov      dword ptr [rip + 0x1908a80], eax  ; -> 01E02828 [f32 1]
004F9DA8  movss    xmm0, dword ptr [rip + 0x1908a78]  ; -> 01E02828 [f32 1]
004F9DB0  movss    dword ptr [rip + 0x1b6add8], xmm0  ; -> 02064B90
004F9DB8  call     0x5375f0  ; -> 005375F0 fn
004F9DBD  call     0x5376d0  ; -> 005376D0 fn
004F9DC2  movss    xmm1, dword ptr [rip + 0x1b6aed2]  ; -> 02064C9C
004F9DCA  movss    xmm0, dword ptr [rip + 0x1b6adbe]  ; -> 02064B90
004F9DD2  movss    xmm2, dword ptr [rip + 0x1b6aebe]  ; -> 02064C98
004F9DDA  movsx    edx, word ptr [rip + 0x1b6ad2b]  ; -> 02064B0C
004F9DE1  movss    xmm3, dword ptr [rip + 0x1b6aedb]  ; -> 02064CC4
004F9DE9  movss    xmm6, dword ptr [rip + 0x17f1eab]  ; -> 01CEBC9C [f32 -1]
004F9DF1  mov      r8d, dword ptr [rip + 0x1b6ad04]  ; -> 02064AFC
004F9DF8  addss    xmm0, xmm6
004F9DFC  lea      eax, [rdx + 0xa]
004F9DFF  shl      eax, 4
004F9E02  movsxd   rcx, eax
004F9E05  lea      eax, [rdx + 0xb]
004F9E08  shl      eax, 4
004F9E0B  mulss    xmm1, xmm0
004F9E0F  movss    xmm0, dword ptr [rip + 0x1b6aec9]  ; -> 02064CE0
004F9E17  addss    xmm2, xmm1
004F9E1B  movss    xmm1, dword ptr [rip + 0x1b6ae9d]  ; -> 02064CC0
004F9E23  mulss    xmm1, xmm2
004F9E27  mulss    xmm3, xmm2
004F9E2B  movss    dword ptr [rip + 0x1b6ae8d], xmm1  ; -> 02064CC0
004F9E33  addss    xmm0, xmm1
004F9E37  movss    xmm1, dword ptr [rip + 0x1b6aea5]  ; -> 02064CE4
004F9E3F  movss    dword ptr [rip + 0x1b6ae7d], xmm3  ; -> 02064CC4
004F9E47  addss    xmm1, xmm3
004F9E4B  movss    dword ptr [rip + 0x1b6ae8d], xmm0  ; -> 02064CE0
004F9E53  movups   xmm0, xmmword ptr [rcx + r15]
004F9E58  movsxd   rcx, eax
004F9E5B  movss    dword ptr [rip + 0x1b6ae81], xmm1  ; -> 02064CE4
004F9E63  movups   xmmword ptr [rip + 0x1b6ae26], xmm0  ; -> 02064C90
004F9E6A  movups   xmm0, xmmword ptr [rcx + r15]
004F9E6F  movups   xmmword ptr [rip + 0x1b6ae2a], xmm0  ; -> 02064CA0
004F9E76  test     r8d, r8d
004F9E79  je       0x4f9fbb  ; -> 004F9FBB
004F9E7F  mov      eax, dword ptr [rip + 0x19089a3]  ; -> 01E02828 [f32 1]
004F9E85  mov      ecx, eax
004F9E87  shr      ecx, 0x12
004F9E8A  xor      ecx, eax
004F9E8C  and      eax, 0x3fffff
004F9E91  shr      ecx, 4
004F9E94  or       eax, 0x1fc00000
004F9E99  and      ecx, 1
004F9E9C  add      eax, eax
004F9E9E  or       ecx, eax
004F9EA0  mov      eax, ecx
004F9EA2  shr      eax, 0x12
004F9EA5  xor      eax, ecx
004F9EA7  and      ecx, 0x3fffff
004F9EAD  or       ecx, 0x1fc00000
004F9EB3  shr      eax, 4
004F9EB6  add      ecx, ecx
004F9EB8  and      eax, 1
004F9EBB  or       eax, ecx
004F9EBD  mov      ecx, eax
004F9EBF  shr      ecx, 0x12
004F9EC2  xor      ecx, eax
004F9EC4  and      eax, 0x3fffff
004F9EC9  shr      ecx, 4
004F9ECC  or       eax, 0x1fc00000
004F9ED1  and      ecx, 1
004F9ED4  add      eax, eax
004F9ED6  or       ecx, eax
004F9ED8  mov      eax, ecx
004F9EDA  shr      eax, 0x12
004F9EDD  xor      eax, ecx
004F9EDF  and      ecx, 0x3fffff
004F9EE5  or       ecx, 0x1fc00000
004F9EEB  shr      eax, 4
004F9EEE  add      ecx, ecx
004F9EF0  and      eax, 1
004F9EF3  or       eax, ecx
004F9EF5  mov      ecx, eax
004F9EF7  shr      ecx, 0x12
004F9EFA  xor      ecx, eax
004F9EFC  and      eax, 0x3fffff
004F9F01  shr      ecx, 4
004F9F04  or       eax, 0x1fc00000
004F9F09  and      ecx, 1
004F9F0C  add      eax, eax
004F9F0E  or       ecx, eax
004F9F10  mov      eax, ecx
004F9F12  mov      dword ptr [rip + 0x1908910], ecx  ; -> 01E02828 [f32 1]
004F9F18  movss    xmm0, dword ptr [rip + 0x1908908]  ; -> 01E02828 [f32 1]
004F9F20  shr      eax, 0x12
004F9F23  xor      eax, ecx
004F9F25  and      ecx, 0x3fffff
004F9F2B  or       ecx, 0x1fc00000
004F9F31  shr      eax, 4
004F9F34  add      ecx, ecx
004F9F36  and      eax, 1
004F9F39  or       eax, ecx
004F9F3B  mov      ecx, eax
004F9F3D  shr      ecx, 0x12
004F9F40  xor      ecx, eax
004F9F42  and      eax, 0x3fffff
004F9F47  shr      ecx, 4
004F9F4A  or       eax, 0x1fc00000
004F9F4F  and      ecx, 1
004F9F52  add      eax, eax
004F9F54  or       ecx, eax
004F9F56  mov      eax, ecx
004F9F58  shr      eax, 0x12
004F9F5B  xor      eax, ecx
004F9F5D  and      ecx, 0x3fffff
004F9F63  or       ecx, 0x1fc00000
004F9F69  shr      eax, 4
004F9F6C  add      ecx, ecx
004F9F6E  and      eax, 1
004F9F71  or       eax, ecx
004F9F73  mov      ecx, eax
004F9F75  shr      ecx, 0x12
004F9F78  xor      ecx, eax
004F9F7A  shr      ecx, 4
004F9F7D  and      ecx, 1
004F9F80  and      eax, 0x3fffff
004F9F85  or       eax, 0x1fc00000
004F9F8A  add      eax, eax
004F9F8C  or       ecx, eax
004F9F8E  mov      edx, ecx
004F9F90  shr      edx, 0x12
004F9F93  xor      edx, ecx
004F9F95  and      ecx, 0x3fffff
004F9F9B  or       ecx, 0x1fc00000
004F9FA1  shr      edx, 4
004F9FA4  add      ecx, ecx
004F9FA6  and      edx, 1
004F9FA9  or       edx, ecx
004F9FAB  mov      dword ptr [rip + 0x1908877], edx  ; -> 01E02828 [f32 1]
004F9FB1  movss    xmm1, dword ptr [rip + 0x190886f]  ; -> 01E02828 [f32 1]
004F9FB9  jmp      0x4f9fc9  ; -> 004F9FC9
004F9FBB  mov      edx, dword ptr [rip + 0x1908867]  ; -> 01E02828 [f32 1]
004F9FC1  movaps   xmm0, xmm15
004F9FC5  movaps   xmm1, xmm15
004F9FC9  movss    xmm3, dword ptr [rip + 0x1b6acc3]  ; -> 02064C94
004F9FD1  subss    xmm0, xmm15
004F9FD6  mov      dword ptr [rip + 0x1b6ab24], 0x3f800000  ; -> 02064B04
004F9FE0  subss    xmm1, xmm15
004F9FE5  mulss    xmm3, xmm0
004F9FE9  movss    dword ptr [rip + 0x1b6ab7f], xmm0  ; -> 02064B70
004F9FF1  movss    dword ptr [rip + 0x1b6ab87], xmm1  ; -> 02064B80
004F9FF9  movss    dword ptr [rip + 0x1b6ac93], xmm3  ; -> 02064C94
004FA001  test     r8d, r8d
004FA004  je       0x4fa027  ; -> 004FA027
004FA006  mov      eax, edx
004FA008  shr      edx, 0x12
004FA00B  xor      edx, eax
004FA00D  and      eax, 0x3fffff
004FA012  or       eax, 0x1fc00000
004FA017  shr      edx, 4
004FA01A  add      eax, eax
004FA01C  and      edx, 1
004FA01F  or       edx, eax
004FA021  mov      dword ptr [rip + 0x1908801], edx  ; -> 01E02828 [f32 1]
004FA027  movss    xmm0, dword ptr [rip + 0x1b6ac75]  ; -> 02064CA4
004FA02F  mulss    xmm0, xmm1
004FA033  movss    dword ptr [rip + 0x1b6ac69], xmm0  ; -> 02064CA4
004FA03B  test     r8d, r8d
004FA03E  je       0x4fa061  ; -> 004FA061
004FA040  mov      eax, edx
004FA042  shr      edx, 0x12
004FA045  xor      edx, eax
004FA047  and      eax, 0x3fffff
004FA04C  or       eax, 0x1fc00000
004FA051  shr      edx, 4
004FA054  add      eax, eax
004FA056  and      edx, 1
004FA059  or       edx, eax
004FA05B  mov      dword ptr [rip + 0x19087c7], edx  ; -> 01E02828 [f32 1]
004FA061  movss    xmm2, dword ptr [rip + 0x1b6ac27]  ; -> 02064C90
004FA069  addss    xmm2, xmm3
004FA06D  movss    dword ptr [rip + 0x1b6ac1b], xmm2  ; -> 02064C90
004FA075  test     r8d, r8d
004FA078  je       0x4fa09b  ; -> 004FA09B
004FA07A  mov      eax, edx
004FA07C  shr      edx, 0x12
004FA07F  xor      edx, eax
004FA081  and      eax, 0x3fffff
004FA086  or       eax, 0x1fc00000
004FA08B  shr      edx, 4
004FA08E  add      eax, eax
004FA090  and      edx, 1
004FA093  or       edx, eax
004FA095  mov      dword ptr [rip + 0x190878d], edx  ; -> 01E02828 [f32 1]
004FA09B  addss    xmm0, dword ptr [rip + 0x1b6abfd]  ; -> 02064CA0
004FA0A3  movss    dword ptr [rip + 0x1b6ac05], xmm0  ; -> 02064CB0
004FA0AB  test     r8d, r8d
004FA0AE  je       0x4fa0d1  ; -> 004FA0D1
004FA0B0  mov      eax, edx
004FA0B2  shr      edx, 0x12
004FA0B5  xor      edx, eax
004FA0B7  and      eax, 0x3fffff
004FA0BC  or       eax, 0x1fc00000
004FA0C1  shr      edx, 4
004FA0C4  add      eax, eax
004FA0C6  and      edx, 1
004FA0C9  or       edx, eax
004FA0CB  mov      dword ptr [rip + 0x1908757], edx  ; -> 01E02828 [f32 1]
004FA0D1  movss    xmm0, dword ptr [rip + 0x1b6abf7]  ; -> 02064CD0
004FA0D9  movss    xmm1, dword ptr [rip + 0x1b6abf3]  ; -> 02064CD4
004FA0E1  mulss    xmm0, xmm2
004FA0E5  mulss    xmm1, xmm2
004FA0E9  mulss    xmm2, dword ptr [rip + 0x1b6abe7]  ; -> 02064CD8
004FA0F1  movss    dword ptr [rip + 0x1b6abf7], xmm0  ; -> 02064CF0
004FA0F9  movss    dword ptr [rip + 0x1b6abf3], xmm1  ; -> 02064CF4
004FA101  movss    dword ptr [rip + 0x1b6abef], xmm2  ; -> 02064CF8
004FA109  test     r8d, r8d
004FA10C  jne      0x4fa114  ; -> 004FA114
004FA10E  movaps   xmm0, xmm15
004FA112  jmp      0x4fa13f  ; -> 004FA13F
004FA114  mov      eax, edx
004FA116  shr      eax, 0x12
004FA119  xor      eax, edx
004FA11B  and      edx, 0x3fffff
004FA121  or       edx, 0x1fc00000
004FA127  shr      eax, 4
004FA12A  add      edx, edx
004FA12C  and      eax, 1
004FA12F  or       eax, edx
004FA131  mov      dword ptr [rip + 0x19086f1], eax  ; -> 01E02828 [f32 1]
004FA137  movss    xmm0, dword ptr [rip + 0x19086e9]  ; -> 01E02828 [f32 1]
004FA13F  movss    dword ptr [rip + 0x1b6aa49], xmm0  ; -> 02064B90
004FA147  call     0x5375f0  ; -> 005375F0 fn
004FA14C  call     0x5376d0  ; -> 005376D0 fn
004FA151  movss    xmm0, dword ptr [rip + 0x1b6aa37]  ; -> 02064B90
004FA159  mov      r11d, dword ptr [rip + 0x1b6a99c]  ; -> 02064AFC
004FA160  addss    xmm0, xmm6
004FA164  movss    dword ptr [rip + 0x1b6aa24], xmm0  ; -> 02064B90
004FA16C  test     r11d, r11d
004FA16F  je       0x4fa1a1  ; -> 004FA1A1
004FA171  mov      eax, dword ptr [rip + 0x19086b1]  ; -> 01E02828 [f32 1]
004FA177  mov      r8d, eax
004FA17A  shr      r8d, 0x12
004FA17E  xor      r8d, eax
004FA181  and      eax, 0x3fffff
004FA186  or       eax, 0x1fc00000
004FA18B  shr      r8d, 4
004FA18F  add      eax, eax
004FA191  and      r8d, 1
004FA195  or       r8d, eax
004FA198  mov      dword ptr [rip + 0x1908689], r8d  ; -> 01E02828 [f32 1]
004FA19F  jmp      0x4fa1a8  ; -> 004FA1A8
004FA1A1  mov      r8d, dword ptr [rip + 0x1908680]  ; -> 01E02828 [f32 1]
004FA1A8  movss    xmm1, dword ptr [rip + 0x1b6aaec]  ; -> 02064C9C
004FA1B0  mulss    xmm1, xmm0
004FA1B4  movss    dword ptr [rip + 0x1b6aae0], xmm1  ; -> 02064C9C
004FA1BC  test     r11d, r11d
004FA1BF  je       0x4fa1e9  ; -> 004FA1E9
004FA1C1  mov      eax, r8d
004FA1C4  shr      r8d, 0x12
004FA1C8  xor      r8d, eax
004FA1CB  and      eax, 0x3fffff
004FA1D0  or       eax, 0x1fc00000
004FA1D5  shr      r8d, 4
004FA1D9  add      eax, eax
004FA1DB  and      r8d, 1
004FA1DF  or       r8d, eax
004FA1E2  mov      dword ptr [rip + 0x190863f], r8d  ; -> 01E02828 [f32 1]
004FA1E9  movss    xmm0, dword ptr [rip + 0x1b6aaa7]  ; -> 02064C98
004FA1F1  addss    xmm0, xmm1
004FA1F5  movss    dword ptr [rip + 0x1b6aa9b], xmm0  ; -> 02064C98
004FA1FD  test     r11d, r11d
004FA200  je       0x4fa22a  ; -> 004FA22A
004FA202  mov      eax, r8d
004FA205  shr      r8d, 0x12
004FA209  xor      r8d, eax
004FA20C  and      eax, 0x3fffff
004FA211  or       eax, 0x1fc00000
004FA216  shr      r8d, 4
004FA21A  add      eax, eax
004FA21C  and      r8d, 1
004FA220  or       r8d, eax
004FA223  mov      dword ptr [rip + 0x19085fe], r8d  ; -> 01E02828 [f32 1]
004FA22A  movss    xmm2, dword ptr [rip + 0x1b6aa92]  ; -> 02064CC4
004FA232  movss    xmm1, dword ptr [rip + 0x1b6aa86]  ; -> 02064CC0
004FA23A  mulss    xmm2, xmm0
004FA23E  mulss    xmm1, xmm0
004FA242  movss    dword ptr [rip + 0x1b6aa7a], xmm2  ; -> 02064CC4
004FA24A  movss    dword ptr [rip + 0x1b6aa6e], xmm1  ; -> 02064CC0
004FA252  test     r11d, r11d
004FA255  je       0x4fa27f  ; -> 004FA27F
004FA257  mov      eax, r8d
004FA25A  shr      r8d, 0x12
004FA25E  xor      r8d, eax
004FA261  and      eax, 0x3fffff
004FA266  or       eax, 0x1fc00000
004FA26B  shr      r8d, 4
004FA26F  add      eax, eax
004FA271  and      r8d, 1
004FA275  or       r8d, eax
004FA278  mov      dword ptr [rip + 0x19085a9], r8d  ; -> 01E02828 [f32 1]
004FA27F  movss    xmm0, dword ptr [rip + 0x1b6aa69]  ; -> 02064CF0
004FA287  addss    xmm0, xmm1
004FA28B  movss    xmm1, dword ptr [rip + 0x1b6aa61]  ; -> 02064CF4
004FA293  addss    xmm1, xmm2
004FA297  movss    dword ptr [rip + 0x1b6aa51], xmm0  ; -> 02064CF0
004FA29F  movss    dword ptr [rip + 0x1b6aa4d], xmm1  ; -> 02064CF4
004FA2A7  test     r11d, r11d
004FA2AA  jne      0x4fa2b2  ; -> 004FA2B2
004FA2AC  movaps   xmm1, xmm15
004FA2B0  jmp      0x4fa2e2  ; -> 004FA2E2
004FA2B2  mov      eax, r8d
004FA2B5  shr      r8d, 0x12
004FA2B9  xor      r8d, eax
004FA2BC  and      eax, 0x3fffff
004FA2C1  or       eax, 0x1fc00000
004FA2C6  shr      r8d, 4
004FA2CA  add      eax, eax
004FA2CC  and      r8d, 1
004FA2D0  or       r8d, eax
004FA2D3  mov      dword ptr [rip + 0x190854e], r8d  ; -> 01E02828 [f32 1]
004FA2DA  movss    xmm1, dword ptr [rip + 0x1908546]  ; -> 01E02828 [f32 1]
004FA2E2  movss    xmm0, dword ptr [rip + 0x1b6a872]  ; -> 02064B5C
004FA2EA  subss    xmm1, xmm15
004FA2EF  dec      word ptr [rip + 0x1b6aac6]  ; -> 02064DBC
004FA2F6  mulss    xmm0, xmm1
004FA2FA  movss    dword ptr [rip + 0x1b6a9ae], xmm1  ; -> 02064CB0
004FA302  movss    xmm1, dword ptr [rip + 0x1b6a84e]  ; -> 02064B58
004FA30A  addss    xmm1, xmm0
004FA30E  movss    dword ptr [rip + 0x1b6a9a6], xmm0  ; -> 02064CBC
004FA316  movss    xmm0, dword ptr [rip + 0x3f970a]  ; -> 008F3A28 [f32 120]
004FA31E  comiss   xmm0, xmm1
004FA321  ja       0x4fa326  ; -> 004FA326
004FA323  movaps   xmm1, xmm0
004FA326  movsx    r10d, word ptr [rip + 0x1b6a7de]  ; -> 02064B0C
004FA32E  xorps    xmm11, xmm11
004FA332  movss    xmm13, dword ptr [rip + 0x1908501]  ; -> 01E0283C [f32 1]
004FA33B  cvttss2si eax, xmm1
004FA33F  mov      dword ptr [rip + 0x1b6a7bb], 0x3f800000  ; -> 02064B04
004FA349  lea      ecx, [r10 + 0x46]
004FA34D  shl      ecx, 4
004FA350  movsxd   rcx, ecx
004FA353  mov      dword ptr [rip + 0x1b6a96f], eax  ; -> 02064CC8
004FA359  movups   xmm0, xmmword ptr [rip + 0x1b6a960]  ; -> 02064CC0
004FA360  mov      dword ptr [rcx + r15 + 8], eax
004FA365  psrldq   xmm0, 8
004FA36A  movd     eax, xmm0
004FA36E  movd     xmm1, eax
004FA372  cvtdq2ps xmm1, xmm1
004FA375  addss    xmm1, xmm15
004FA37A  ucomiss  xmm1, xmm11
004FA37E  movss    dword ptr [rip + 0x1b6a932], xmm1  ; -> 02064CB8
004FA386  jp       0x4fa399  ; -> 004FA399
004FA388  jne      0x4fa399  ; -> 004FA399
004FA38A  movss    xmm12, dword ptr [rip + 0x405fcd]  ; -> 00900360 [u32 0x7F7FFFFF]
004FA393  movaps   xmm5, xmm12
004FA397  jmp      0x4fa3aa  ; -> 004FA3AA
004FA399  movss    xmm12, dword ptr [rip + 0x405fbe]  ; -> 00900360 [u32 0x7F7FFFFF]
004FA3A2  movaps   xmm5, xmm13
004FA3A6  divss    xmm5, xmm1
004FA3AA  movss    xmm14, dword ptr [rip + 0x190847d]  ; -> 01E02830 [u32 0x00000000]
004FA3B3  movaps   xmm0, xmm14
004FA3B7  movss    dword ptr [rip + 0x1b6a741], xmm5  ; -> 02064B00
004FA3BF  mulss    xmm0, xmm14
004FA3C4  movss    dword ptr [rsp + 0x24], xmm0
004FA3CA  movss    dword ptr [rip + 0x1b6a78e], xmm0  ; -> 02064B60
004FA3D2  movss    xmm0, dword ptr [rip + 0x190845a]  ; -> 01E02834 [u32 0x00000000]
004FA3DA  addss    xmm0, xmm5
004FA3DE  ucomiss  xmm0, xmm11
004FA3E2  movss    dword ptr [rip + 0x1b6a77a], xmm0  ; -> 02064B64
004FA3EA  jp       0x4fa431  ; -> 004FA431
004FA3EC  jne      0x4fa431  ; -> 004FA431
004FA3EE  call     0x22cc40  ; -> 0022CC40 fn
004FA3F3  movss    xmm0, dword ptr [rip + 0x1b6a765]  ; -> 02064B60
004FA3FB  movzx    r10d, word ptr [rip + 0x1b6a709]  ; -> 02064B0C
004FA403  movss    xmm5, dword ptr [rip + 0x1b6a6f5]  ; -> 02064B00
004FA40B  mov      r8d, dword ptr [rip + 0x1908416]  ; -> 01E02828 [f32 1]
004FA412  mov      r11d, dword ptr [rip + 0x1b6a6e3]  ; -> 02064AFC
004FA419  movss    xmm13, dword ptr [rip + 0x190841a]  ; -> 01E0283C [f32 1]
004FA422  movss    xmm14, dword ptr [rip + 0x1908405]  ; -> 01E02830 [u32 0x00000000]
004FA42B  movss    dword ptr [rsp + 0x24], xmm0
004FA431  comiss   xmm11, dword ptr [rip + 0x1b6a72b]  ; -> 02064B64
004FA439  jbe      0x4fa47e  ; -> 004FA47E
004FA43B  call     0x22cc30  ; -> 0022CC30 fn
004FA440  movss    xmm0, dword ptr [rip + 0x1b6a718]  ; -> 02064B60
004FA448  movzx    r10d, word ptr [rip + 0x1b6a6bc]  ; -> 02064B0C
004FA450  movss    xmm5, dword ptr [rip + 0x1b6a6a8]  ; -> 02064B00
004FA458  mov      r8d, dword ptr [rip + 0x19083c9]  ; -> 01E02828 [f32 1]
004FA45F  mov      r11d, dword ptr [rip + 0x1b6a696]  ; -> 02064AFC
004FA466  movss    xmm13, dword ptr [rip + 0x19083cd]  ; -> 01E0283C [f32 1]
004FA46F  movss    xmm14, dword ptr [rip + 0x19083b8]  ; -> 01E02830 [u32 0x00000000]
004FA478  movss    dword ptr [rsp + 0x24], xmm0
004FA47E  movss    xmm4, dword ptr [rip + 0x19083ae]  ; -> 01E02834 [u32 0x00000000]
004FA486  movaps   xmm3, xmm14
004FA48A  movss    xmm1, dword ptr [rip + 0x19083a6]  ; -> 01E02838 [u32 0x00000000]
004FA492  movaps   xmm0, xmm4
004FA495  addss    xmm0, dword ptr [rip + 0x17f176b]  ; -> 01CEBC08 [f32 2]
004FA49D  movsx    eax, r10w
004FA4A1  addss    xmm4, xmm5
004FA4A5  add      eax, 0x46
004FA4A8  mulss    xmm3, xmm14
004FA4AD  shl      eax, 4
004FA4B0  mulss    xmm1, xmm14
004FA4B5  movaps   xmm2, xmm14
004FA4B9  cdqe     
004FA4BB  ucomiss  xmm4, xmm11
004FA4BF  mov      dword ptr [rip + 0x1b6a63b], 0x40000000  ; -> 02064B04
004FA4C9  movzx    edx, word ptr [rax + r15 + 8]
004FA4CF  mov      word ptr [rip + 0x1b6a8ea], dx  ; -> 02064DC0
004FA4D6  mulss    xmm2, xmm13
004FA4DB  mulss    xmm0, xmm5
004FA4DF  movss    dword ptr [rip + 0x1b6a6d9], xmm3  ; -> 02064BC0
004FA4E7  movss    dword ptr [rip + 0x1b6a6dd], xmm2  ; -> 02064BCC
004FA4EF  movss    dword ptr [rip + 0x1b6a6cd], xmm0  ; -> 02064BC4
004FA4F7  movss    dword ptr [rip + 0x1b6a6c9], xmm1  ; -> 02064BC8
004FA4FF  movss    dword ptr [rip + 0x1b6a6c9], xmm3  ; -> 02064BD0
004FA507  movss    dword ptr [rip + 0x1b6a6cd], xmm2  ; -> 02064BDC
004FA50F  movss    dword ptr [rip + 0x1b6a6c1], xmm1  ; -> 02064BD8
004FA517  movss    dword ptr [rip + 0x1b6a6b5], xmm4  ; -> 02064BD4
004FA51F  jp       0x4fa56d  ; -> 004FA56D
004FA521  jne      0x4fa56d  ; -> 004FA56D
004FA523  call     0x22cc40  ; -> 0022CC40 fn
004FA528  movss    xmm0, dword ptr [rip + 0x1b6a630]  ; -> 02064B60
004FA530  movzx    r10d, word ptr [rip + 0x1b6a5d4]  ; -> 02064B0C
004FA538  mov      r8d, dword ptr [rip + 0x19082e9]  ; -> 01E02828 [f32 1]
004FA53F  movzx    edx, word ptr [rip + 0x1b6a87a]  ; -> 02064DC0
004FA546  mov      r11d, dword ptr [rip + 0x1b6a5af]  ; -> 02064AFC
004FA54D  movss    xmm13, dword ptr [rip + 0x19082e6]  ; -> 01E0283C [f32 1]
004FA556  movss    xmm14, dword ptr [rip + 0x19082d1]  ; -> 01E02830 [u32 0x00000000]
004FA55F  movss    xmm4, dword ptr [rip + 0x1b6a66d]  ; -> 02064BD4
004FA567  movss    dword ptr [rsp + 0x24], xmm0
004FA56D  comiss   xmm11, xmm4
004FA571  jbe      0x4fa5b5  ; -> 004FA5B5
004FA573  call     0x22cc30  ; -> 0022CC30 fn
004FA578  movss    xmm0, dword ptr [rip + 0x1b6a5e0]  ; -> 02064B60
004FA580  movzx    r10d, word ptr [rip + 0x1b6a584]  ; -> 02064B0C
004FA588  mov      r8d, dword ptr [rip + 0x1908299]  ; -> 01E02828 [f32 1]
004FA58F  movzx    edx, word ptr [rip + 0x1b6a82a]  ; -> 02064DC0
004FA596  mov      r11d, dword ptr [rip + 0x1b6a55f]  ; -> 02064AFC
004FA59D  movss    xmm13, dword ptr [rip + 0x1908296]  ; -> 01E0283C [f32 1]
004FA5A6  movss    xmm14, dword ptr [rip + 0x1908281]  ; -> 01E02830 [u32 0x00000000]
004FA5AF  movss    dword ptr [rsp + 0x24], xmm0
004FA5B5  movss    xmm8, dword ptr [rip + 0x1908276]  ; -> 01E02834 [u32 0x00000000]
004FA5BE  movaps   xmm5, xmm14
004FA5C2  movss    xmm9, dword ptr [rip + 0x190826d]  ; -> 01E02838 [u32 0x00000000]
004FA5CB  movdqu   xmm0, xmmword ptr [rip + 0x1b6a63d]  ; -> 02064C10
004FA5D3  movsx    r9d, r10w
004FA5D7  movss    xmm1, dword ptr [rip + 0x1b6a649]  ; -> 02064C28
004FA5DF  movss    xmm6, dword ptr [rip + 0x1b6a661]  ; -> 02064C48
004FA5E7  movss    xmm7, dword ptr [rip + 0x1b6a65d]  ; -> 02064C4C
004FA5EF  mulss    xmm1, xmm8
004FA5F4  lea      eax, [r9 + 0x1d]
004FA5F8  shl      eax, 4
004FA5FB  movsxd   rcx, eax
004FA5FE  lea      eax, [r9 + 0x1e]
004FA602  shufps   xmm5, xmm5, 0
004FA606  mulps    xmm5, xmm0
004FA609  shl      eax, 4
004FA60C  movups   xmm0, xmmword ptr [rcx + r15]
004FA611  movsxd   rcx, eax
004FA614  lea      eax, [r9 + 0x1f]
004FA618  shl      eax, 4
004FA61B  movups   xmmword ptr [rip + 0x1b6a54e], xmm0  ; -> 02064B70
004FA622  movss    xmm0, dword ptr [rip + 0x1b6a5f6]  ; -> 02064C20
004FA62A  mulss    xmm0, xmm8
004FA62F  movups   xmmword ptr [rip + 0x1b6a4ea], xmm5  ; -> 02064B20
004FA636  movss    xmm4, dword ptr [rip + 0x1b6a4ee]  ; -> 02064B2C
004FA63E  addss    xmm5, xmm0
004FA642  movss    xmm0, dword ptr [rip + 0x1b6a5da]  ; -> 02064C24
004FA64A  movss    xmm2, dword ptr [rip + 0x1b6a4d2]  ; -> 02064B24
004FA652  movss    xmm3, dword ptr [rip + 0x1b6a4ce]  ; -> 02064B28
004FA65A  mulss    xmm0, xmm8
004FA65F  addss    xmm3, xmm1
004FA663  mulss    xmm6, xmm13
004FA668  addss    xmm2, xmm0
004FA66C  mulss    xmm7, xmm13
004FA671  movss    xmm0, dword ptr [rip + 0x1b6a5b3]  ; -> 02064C2C
004FA679  mulss    xmm0, xmm8
004FA67E  addss    xmm4, xmm0
004FA682  movups   xmm0, xmmword ptr [rcx + r15]
004FA687  movsxd   rcx, eax
004FA68A  lea      eax, [r9 + 0x20]
004FA68E  shl      eax, 4
004FA691  movups   xmmword ptr [rsp + 0x50], xmm0
004FA696  movups   xmmword ptr [rip + 0x1b6a4e3], xmm0  ; -> 02064B80
004FA69D  movss    xmm0, dword ptr [rip + 0x1b6a58b]  ; -> 02064C30
004FA6A5  movss    dword ptr [rsp + 0x30], xmm0
004FA6AB  mulss    xmm0, xmm9
004FA6B0  addss    xmm5, xmm0
004FA6B4  movss    xmm0, dword ptr [rip + 0x1b6a578]  ; -> 02064C34
004FA6BC  movaps   xmm1, xmm0
004FA6BF  movss    dword ptr [rsp + 0x28], xmm0
004FA6C5  movss    xmm0, dword ptr [rip + 0x1b6a56b]  ; -> 02064C38
004FA6CD  mulss    xmm1, xmm9
004FA6D2  movss    dword ptr [rsp + 0x2c], xmm0
004FA6D8  mulss    xmm0, xmm9
004FA6DD  addss    xmm2, xmm1
004FA6E1  addss    xmm3, xmm0
004FA6E5  movss    xmm0, dword ptr [rip + 0x1b6a54f]  ; -> 02064C3C
004FA6ED  movaps   xmm1, xmm0
004FA6F0  movss    dword ptr [rsp + 0x20], xmm0
004FA6F6  movups   xmm0, xmmword ptr [rcx + r15]
004FA6FB  movsxd   rcx, eax
004FA6FE  mulss    xmm1, xmm9
004FA703  addss    xmm6, xmm3
004FA707  movups   xmm10, xmmword ptr [rcx + r15]
004FA70C  addss    xmm4, xmm1
004FA710  movss    xmm1, dword ptr [rip + 0x1b6a528]  ; -> 02064C40
004FA718  mulss    xmm1, xmm13
004FA71D  movss    dword ptr [rip + 0x1b6a593], xmm6  ; -> 02064CB8
004FA725  movups   xmmword ptr [rsp + 0x40], xmm0
004FA72A  addss    xmm1, xmm5
004FA72E  movss    xmm5, dword ptr [rip + 0x1b6a50e]  ; -> 02064C44
004FA736  addss    xmm7, xmm4
004FA73A  mulss    xmm5, xmm13
004FA73F  movups   xmmword ptr [rip + 0x1b6a44a], xmm0  ; -> 02064B90
004FA746  addss    xmm5, xmm2
004FA74A  movss    dword ptr [rip + 0x1b6a55e], xmm1  ; -> 02064CB0
004FA752  movaps   xmm4, xmm1
004FA755  movss    dword ptr [rip + 0x1b6a55f], xmm7  ; -> 02064CBC
004FA75D  movups   xmmword ptr [rip + 0x1b6a43b], xmm10  ; -> 02064BA0
004FA765  shufps   xmm4, xmm4, 0
004FA769  movss    dword ptr [rip + 0x1b6a543], xmm5  ; -> 02064CB4
004FA771  movups   xmm3, xmmword ptr [rsp + 0x50]
004FA776  movups   xmm0, xmmword ptr [rip + 0x1b6a3f3]  ; -> 02064B70
004FA77D  movaps   xmm1, xmm5
004FA780  movss    dword ptr [rip + 0x1b6a3f8], xmm3  ; -> 02064B80
004FA788  mulps    xmm4, xmm0
004FA78B  movaps   xmm0, xmm5
004FA78E  mulss    xmm0, xmm3
004FA792  movups   xmmword ptr [rip + 0x1b6a387], xmm4  ; -> 02064B20
004FA799  movss    xmm2, dword ptr [rip + 0x1b6a383]  ; -> 02064B24
004FA7A1  addss    xmm4, xmm0
004FA7A5  movaps   xmm0, xmm3
004FA7A8  shufps   xmm0, xmm3, 0x55
004FA7AC  mulss    xmm1, xmm0
004FA7B0  movss    dword ptr [rip + 0x1b6a3cc], xmm0  ; -> 02064B84
004FA7B8  movaps   xmmword ptr [rsp + 0x90], xmm0
004FA7C0  movaps   xmm0, xmm5
004FA7C3  addss    xmm2, xmm1
004FA7C7  movaps   xmm1, xmm3
004FA7CA  shufps   xmm1, xmm3, 0xaa
004FA7CE  mulss    xmm0, xmm1
004FA7D2  movaps   xmmword ptr [rsp + 0x80], xmm1
004FA7DA  movss    xmm1, dword ptr [rip + 0x1b6a346]  ; -> 02064B28
004FA7E2  addss    xmm1, xmm0
004FA7E6  movaps   xmm0, xmm3
004FA7E9  shufps   xmm0, xmm3, 0xff
004FA7ED  movss    xmm3, dword ptr [rip + 0x1b6a337]  ; -> 02064B2C
004FA7F5  mulss    xmm5, xmm0
004FA7F9  movss    dword ptr [rip + 0x1b6a38b], xmm0  ; -> 02064B8C
004FA801  movaps   xmmword ptr [rsp + 0xa0], xmm0
004FA809  addss    xmm3, xmm5
004FA80D  movups   xmm5, xmmword ptr [rsp + 0x40]
004FA812  movaps   xmm0, xmm5
004FA815  movss    dword ptr [rip + 0x1b6a373], xmm5  ; -> 02064B90
004FA81D  mulss    xmm0, xmm6
004FA821  addss    xmm4, xmm0
004FA825  movaps   xmm0, xmm5
004FA828  shufps   xmm0, xmm5, 0x55
004FA82C  movaps   xmmword ptr [rsp + 0xb0], xmm0
004FA834  mulss    xmm0, xmm6
004FA838  addss    xmm2, xmm0
004FA83C  movaps   xmm0, xmm5
004FA83F  shufps   xmm0, xmm5, 0xaa
004FA843  movaps   xmmword ptr [rsp + 0xc0], xmm0
004FA84B  mulss    xmm0, xmm6
004FA84F  addss    xmm1, xmm0
004FA853  movaps   xmm0, xmm5
004FA856  shufps   xmm0, xmm5, 0xff
004FA85A  movaps   xmmword ptr [rsp + 0xd0], xmm0
004FA862  mulss    xmm0, xmm6
004FA866  addss    xmm3, xmm0
004FA86A  movaps   xmm0, xmm10
004FA86E  mulss    xmm0, xmm7
004FA872  addss    xmm0, xmm4
004FA876  movss    dword ptr [rip + 0x1b6a2ae], xmm3  ; -> 02064B2C
004FA87E  movss    dword ptr [rip + 0x1b6a43a], xmm0  ; -> 02064CC0
004FA886  movaps   xmm0, xmm10
004FA88A  shufps   xmm0, xmm10, 0x55
004FA88F  movaps   xmmword ptr [rsp + 0xe0], xmm0
004FA897  mulss    xmm0, xmm7
004FA89B  addss    xmm0, xmm2
004FA89F  movaps   xmm2, xmm10
004FA8A3  shufps   xmm2, xmm10, 0xff
004FA8A8  movaps   xmmword ptr [rsp + 0x100], xmm2
004FA8B0  movss    dword ptr [rip + 0x1b6a40c], xmm0  ; -> 02064CC4
004FA8B8  movaps   xmm0, xmm10
004FA8BC  shufps   xmm0, xmm10, 0xaa
004FA8C1  movaps   xmmword ptr [rsp + 0xf0], xmm0
004FA8C9  mulss    xmm0, xmm7
004FA8CD  addss    xmm0, xmm1
004FA8D1  movaps   xmm1, xmm2
004FA8D4  mulss    xmm1, xmm7
004FA8D8  addss    xmm1, xmm3
004FA8DC  movss    dword ptr [rip + 0x1b6a3e4], xmm0  ; -> 02064CC8
004FA8E4  ucomiss  xmm1, xmm11
004FA8E8  movss    dword ptr [rip + 0x1b6a3dc], xmm1  ; -> 02064CCC
004FA8F0  jp       0x4fa8fa  ; -> 004FA8FA
004FA8F2  jne      0x4fa8fa  ; -> 004FA8FA
004FA8F4  movaps   xmm0, xmm12
004FA8F8  jmp      0x4fa902  ; -> 004FA902
004FA8FA  movaps   xmm0, xmm13
004FA8FE  divss    xmm0, xmm1
004FA902  movups   xmm1, xmmword ptr [rip + 0x1b6a3b7]  ; -> 02064CC0
004FA909  lea      eax, [r9 + 0x46]
004FA90D  movss    dword ptr [rip + 0x1b6a1eb], xmm0  ; -> 02064B00
004FA915  shl      eax, 4
004FA918  movsxd   rcx, eax
004FA91B  lea      eax, [r9 + 0xc8]
004FA922  shufps   xmm0, xmm0, 0
004FA926  lea      r9d, [r10 + 1]
004FA92A  mulps    xmm1, xmm0
004FA92D  shl      eax, 4
004FA930  mov      word ptr [rip + 0x1b6a48c], r9w  ; -> 02064DC4
004FA938  movups   xmm0, xmmword ptr [rip + 0x1b6a371]  ; -> 02064CB0
004FA93F  movups   xmmword ptr [rip + 0x1b6a37a], xmm1  ; -> 02064CC0
004FA946  movups   xmmword ptr [rcx + r15], xmm0
004FA94B  movsxd   rcx, eax
004FA94E  movups   xmmword ptr [rcx + r15], xmm1
004FA953  cmp      dx, r10w
004FA957  je       0x4fb0c2  ; -> 004FB0C2
004FA95D  movss    xmm3, dword ptr [rsp + 0x24]
004FA963  mov      dword ptr [rip + 0x1b6a18f], 1  ; -> 02064AFC
004FA96D  nop      dword ptr [rax]
004FA970  addss    xmm3, dword ptr [rip + 0x1b6a1ec]  ; -> 02064B64
004FA978  movss    xmm0, dword ptr [rip + 0x1907ea8]  ; -> 01E02828 [f32 1]
004FA980  movaps   xmm8, xmm9
004FA984  movss    dword ptr [rip + 0x1b6a1bc], xmm0  ; -> 02064B48
004FA98C  movaps   xmm2, xmm14
004FA990  movss    xmm0, dword ptr [rip + 0x1b6a1b4]  ; -> 02064B4C
004FA998  addss    xmm2, xmm13
004FA99D  movss    dword ptr [rip + 0x1907e83], xmm0  ; -> 01E02828 [f32 1]
004FA9A5  dec      dx
004FA9A8  movsx    eax, r10w
004FA9AC  addss    xmm8, xmm3
004FA9B1  add      eax, 6
004FA9B4  movss    dword ptr [rip + 0x1b6a1a4], xmm3  ; -> 02064B60
004FA9BC  shl      eax, 4
004FA9BF  movaps   xmm1, xmm3
004FA9C2  mulss    xmm1, dword ptr [rip + 0x3f8752]  ; -> 008F311C [f32 3]
004FA9CA  subss    xmm2, xmm3
004FA9CE  cdqe     
004FA9D0  movaps   xmm9, xmm13
004FA9D4  mov      word ptr [rip + 0x1b6a3e5], dx  ; -> 02064DC0
004FA9DB  movaps   xmm0, xmm3
004FA9DE  mulss    xmm9, xmm3
004FA9E3  mulss    xmm0, xmm3
004FA9E7  movaps   xmm7, xmm1
004FA9EA  movups   xmm10, xmmword ptr [rax + r15]
004FA9EF  mov      eax, dword ptr [rip + 0x1907e33]  ; -> 01E02828 [f32 1]
004FA9F5  mov      ecx, eax
004FA9F7  shr      ecx, 0x12
004FA9FA  movaps   xmm6, xmm2
004FA9FD  xor      ecx, eax
004FA9FF  mulss    xmm9, xmm0
004FAA04  and      eax, 0x3fffff
004FAA09  shr      ecx, 4
004FAA0C  addss    xmm7, dword ptr [rip + 0x1907e20]  ; -> 01E02834 [u32 0x00000000]
004FAA14  or       eax, 0x1fc00000
004FAA19  movss    dword ptr [rip + 0x1b6a26f], xmm0  ; -> 02064C90
004FAA21  add      eax, eax
004FAA23  movss    dword ptr [rip + 0x1b6a245], xmm2  ; -> 02064C70
004FAA2B  and      ecx, 1
004FAA2E  movss    dword ptr [rip + 0x1b6a235], xmm9  ; -> 02064C6C
004FAA37  or       ecx, eax
004FAA39  mulss    xmm8, xmm1
004FAA3E  mov      eax, ecx
004FAA40  mulss    xmm6, xmm2
004FAA44  shr      eax, 0x12
004FAA47  xor      eax, ecx
004FAA49  and      ecx, 0x3fffff
004FAA4F  or       ecx, 0x1fc00000
004FAA55  shr      eax, 4
004FAA58  add      ecx, ecx
004FAA5A  and      eax, 1
004FAA5D  or       eax, ecx
004FAA5F  mov      ecx, eax
004FAA61  shr      ecx, 0x12
004FAA64  xor      ecx, eax
004FAA66  and      eax, 0x3fffff
004FAA6B  or       eax, 0x1fc00000
004FAA70  shr      ecx, 4
004FAA73  add      eax, eax
004FAA75  and      ecx, 1
004FAA78  or       ecx, eax
004FAA7A  mov      eax, ecx
004FAA7C  shr      eax, 0x12
004FAA7F  xor      eax, ecx
004FAA81  and      ecx, 0x3fffff
004FAA87  or       ecx, 0x1fc00000
004FAA8D  shr      eax, 4
004FAA90  add      ecx, ecx
004FAA92  and      eax, 1
004FAA95  or       eax, ecx
004FAA97  mov      ecx, eax
004FAA99  shr      ecx, 0x12
004FAA9C  xor      ecx, eax
004FAA9E  and      eax, 0x3fffff
004FAAA3  or       eax, 0x1fc00000
004FAAA8  shr      ecx, 4
004FAAAB  add      eax, eax
004FAAAD  and      ecx, 1
004FAAB0  or       ecx, eax
004FAAB2  mov      dword ptr [rip + 0x1907d70], ecx  ; -> 01E02828 [f32 1]
004FAAB8  movups   xmmword ptr [rip + 0x1b6a0f0], xmm10  ; -> 02064BB0
004FAAC0  movss    xmm0, dword ptr [rip + 0x1b6a228]  ; -> 02064CF0
004FAAC8  mov      eax, ecx
004FAACA  movss    xmm3, dword ptr [rip + 0x1b6a1fe]  ; -> 02064CD0
004FAAD2  movss    xmm4, dword ptr [rip + 0x1b6a1fa]  ; -> 02064CD4
004FAADA  movss    xmm5, dword ptr [rip + 0x1907d46]  ; -> 01E02828 [f32 1]
004FAAE2  shr      eax, 0x12
004FAAE5  xor      eax, ecx
004FAAE7  mulss    xmm8, xmm2
004FAAEC  and      ecx, 0x3fffff
004FAAF2  shr      eax, 4
004FAAF5  or       ecx, 0x1fc00000
004FAAFB  mulss    xmm3, xmm9
004FAB00  add      ecx, ecx
004FAB02  and      eax, 1
004FAB05  or       eax, ecx
004FAB07  mulss    xmm4, xmm9
004FAB0C  mov      ecx, eax
004FAB0E  mulss    xmm9, dword ptr [rip + 0x1b6a1c1]  ; -> 02064CD8
004FAB17  movaps   xmm1, xmm8
004FAB1B  shr      ecx, 0x12
004FAB1E  mulss    xmm1, dword ptr [rip + 0x1b6a1ce]  ; -> 02064CF4
004FAB26  xor      ecx, eax
004FAB28  and      eax, 0x3fffff
004FAB2D  shr      ecx, 4
004FAB30  or       eax, 0x1fc00000
004FAB35  mulss    xmm0, xmm8
004FAB3A  add      eax, eax
004FAB3C  and      ecx, 1
004FAB3F  mulss    xmm7, xmm6
004FAB43  addss    xmm4, xmm1
004FAB47  or       ecx, eax
004FAB49  addss    xmm3, xmm0
004FAB4D  mulss    xmm6, xmm2
004FAB51  mov      eax, ecx
004FAB53  movss    xmm0, dword ptr [rip + 0x1b6a19d]  ; -> 02064CF8
004FAB5B  movaps   xmm1, xmm7
004FAB5E  mulss    xmm1, dword ptr [rip + 0x1b6a17e]  ; -> 02064CE4
004FAB66  shr      eax, 0x12
004FAB69  xor      eax, ecx
004FAB6B  mulss    xmm0, xmm8
004FAB70  and      ecx, 0x3fffff
004FAB76  shr      eax, 4
004FAB79  or       ecx, 0x1fc00000
004FAB7F  movss    dword ptr [rip + 0x1b6a0dd], xmm7  ; -> 02064C64
004FAB87  add      ecx, ecx
004FAB89  movss    dword ptr [rip + 0x1b6a0d6], xmm8  ; -> 02064C68
004FAB92  and      eax, 1
004FAB95  movss    dword ptr [rip + 0x1b6a0c3], xmm6  ; -> 02064C60
004FAB9D  or       eax, ecx
004FAB9F  movss    dword ptr [rip + 0x1b6a0b4], xmm13  ; -> 02064C5C
004FABA8  mov      ecx, eax
004FABAA  addss    xmm9, xmm0
004FABAF  shr      ecx, 0x12
004FABB2  addss    xmm4, xmm1
004FABB6  xor      ecx, eax
004FABB8  movaps   xmm0, xmm7
004FABBB  mulss    xmm0, dword ptr [rip + 0x1b6a11d]  ; -> 02064CE0
004FABC3  and      eax, 0x3fffff
004FABC8  or       eax, 0x1fc00000
004FABCD  shr      ecx, 4
004FABD0  mulss    xmm7, dword ptr [rip + 0x1b6a110]  ; -> 02064CE8
004FABD8  add      eax, eax
004FABDA  and      ecx, 1
004FABDD  addss    xmm3, xmm0
004FABE1  movss    dword ptr [rip + 0x1b69f3b], xmm4  ; -> 02064B24
004FABE9  or       ecx, eax
004FABEB  movaps   xmm0, xmm6
004FABEE  mov      eax, ecx
004FABF0  addss    xmm9, xmm7
004FABF5  shr      eax, 0x12
004FABF8  xor      eax, ecx
004FABFA  and      ecx, 0x3fffff
004FAC00  or       ecx, 0x1fc00000
004FAC06  shr      eax, 4
004FAC09  add      ecx, ecx
004FAC0B  movss    dword ptr [rip + 0x1b69f0d], xmm3  ; -> 02064B20
004FAC13  and      eax, 1
004FAC16  movss    dword ptr [rip + 0x1b69f09], xmm9  ; -> 02064B28
004FAC1F  or       eax, ecx
004FAC21  mov      dword ptr [rip + 0x1907c01], eax  ; -> 01E02828 [f32 1]
004FAC27  movss    xmm2, dword ptr [rip + 0x1907bf9]  ; -> 01E02828 [f32 1]
004FAC2F  subss    xmm5, dword ptr [rip + 0x406f05]  ; -> 00901B3C [f32 1.5]
004FAC37  mulss    xmm0, xmm14
004FAC3C  subss    xmm2, xmm15
004FAC41  mov      dword ptr [rip + 0x1b69eb9], 0x40c90fdb  ; -> 02064B04
004FAC4B  movaps   xmm1, xmm6
004FAC4E  shufps   xmm10, xmm10, 0x55
004FAC53  mulss    xmm1, dword ptr [rip + 0x1907bd9]  ; -> 01E02834 [u32 0x00000000]
004FAC5B  mulss    xmm6, dword ptr [rip + 0x1907bd5]  ; -> 01E02838 [u32 0x00000000]
004FAC63  addss    xmm0, xmm3
004FAC67  mulss    xmm5, dword ptr [rip + 0x17f1009]  ; -> 01CEBC78 [f32 6.283185]
004FAC6F  addss    xmm1, xmm4
004FAC73  mulss    xmm10, xmm2
004FAC78  addss    xmm6, xmm9
004FAC7D  movss    dword ptr [rip + 0x1b69fcb], xmm0  ; -> 02064C50
004FAC85  movss    xmm0, dword ptr [rip + 0x1b69f23]  ; -> 02064BB0
004FAC8D  addss    xmm0, xmm10
004FAC92  movss    dword ptr [rip + 0x1b69fba], xmm1  ; -> 02064C54
004FAC9A  movss    dword ptr [rip + 0x1b69fb6], xmm6  ; -> 02064C58
004FACA2  movss    dword ptr [rip + 0x1b69fd6], xmm2  ; -> 02064C80
004FACAA  movss    dword ptr [rip + 0x1b69f01], xmm10  ; -> 02064BB4
004FACB3  movss    dword ptr [rip + 0x1b69ff5], xmm5  ; -> 02064CB0
004FACBB  movss    dword ptr [rip + 0x1b69eed], xmm0  ; -> 02064BB0
004FACC3  call     0x5376d0  ; -> 005376D0 fn
004FACC8  movss    xmm3, dword ptr [rip + 0x1b69f84]  ; -> 02064C54
004FACD0  mov      r11d, 1
004FACD6  movss    xmm1, dword ptr [rip + 0x1907b4a]  ; -> 01E02828 [f32 1]
004FACDE  movss    xmm2, dword ptr [rip + 0x1b69fda]  ; -> 02064CC0
004FACE6  mulss    xmm2, dword ptr [rip + 0x1b69ec2]  ; -> 02064BB0
004FACEE  mov      dword ptr [rip + 0x1b69e07], r11d  ; -> 02064AFC
004FACF5  movss    xmm0, dword ptr [rip + 0x1b69eb7]  ; -> 02064BB4
004FACFD  mulss    xmm0, dword ptr [rip + 0x1b69fbf]  ; -> 02064CC4
004FAD05  movss    xmm9, dword ptr [rip + 0x1b69f4e]  ; -> 02064C5C
004FAD0E  movss    dword ptr [rip + 0x1b69e36], xmm1  ; -> 02064B4C
004FAD16  movss    xmm1, dword ptr [rip + 0x1b69f32]  ; -> 02064C50
004FAD1E  addss    xmm3, xmm0
004FAD22  movss    dword ptr [rip + 0x1b69f8a], xmm0  ; -> 02064CB4
004FAD2A  addss    xmm1, xmm2
004FAD2E  movss    xmm2, dword ptr [rip + 0x1b69f22]  ; -> 02064C58
004FAD36  movss    xmm0, dword ptr [rip + 0x1b69e0a]  ; -> 02064B48
004FAD3E  movss    dword ptr [rip + 0x1907ae2], xmm0  ; -> 01E02828 [f32 1]
004FAD46  movdqu   xmm0, xmmword ptr [rip + 0x1b69ec2]  ; -> 02064C10
004FAD4E  movaps   xmm7, xmm1
004FAD51  movaps   xmm1, xmm3
004FAD54  mulss    xmm1, dword ptr [rip + 0x1b69ecc]  ; -> 02064C28
004FAD5C  shufps   xmm7, xmm7, 0
004FAD60  mulps    xmm7, xmm0
004FAD63  movaps   xmm0, xmm3
004FAD66  mulss    xmm0, dword ptr [rip + 0x1b69eb2]  ; -> 02064C20
004FAD6E  movups   xmmword ptr [rip + 0x1b69dab], xmm7  ; -> 02064B20
004FAD75  movss    xmm4, dword ptr [rip + 0x1b69da7]  ; -> 02064B24
004FAD7D  addss    xmm7, xmm0
004FAD81  movss    xmm5, dword ptr [rip + 0x1b69d9f]  ; -> 02064B28
004FAD89  movaps   xmm0, xmm3
004FAD8C  mulss    xmm0, dword ptr [rip + 0x1b69e90]  ; -> 02064C24
004FAD94  addss    xmm5, xmm1
004FAD98  movss    xmm1, dword ptr [rip + 0x1b69e90]  ; -> 02064C30
004FADA0  mulss    xmm3, dword ptr [rip + 0x1b69e84]  ; -> 02064C2C
004FADA8  movss    xmm6, dword ptr [rip + 0x1b69d7c]  ; -> 02064B2C
004FADB0  addss    xmm4, xmm0
004FADB4  movaps   xmm0, xmm2
004FADB7  movss    dword ptr [rsp + 0x30], xmm1
004FADBD  mulss    xmm0, xmm1
004FADC1  addss    xmm6, xmm3
004FADC5  movaps   xmm1, xmm2
004FADC8  addss    xmm7, xmm0
004FADCC  movss    xmm0, dword ptr [rip + 0x1b69e60]  ; -> 02064C34
004FADD4  mulss    xmm1, xmm0
004FADD8  movss    dword ptr [rsp + 0x28], xmm0
004FADDE  movaps   xmm0, xmm2
004FADE1  addss    xmm4, xmm1
004FADE5  movss    xmm1, dword ptr [rip + 0x1b69e4b]  ; -> 02064C38
004FADED  mulss    xmm0, xmm1
004FADF1  movss    dword ptr [rsp + 0x2c], xmm1
004FADF7  addss    xmm5, xmm0
004FADFB  movss    xmm0, dword ptr [rip + 0x1b69e39]  ; -> 02064C3C
004FAE03  mulss    xmm2, xmm0
004FAE07  movss    dword ptr [rsp + 0x20], xmm0
004FAE0D  movaps   xmm0, xmm9
004FAE11  mulss    xmm0, dword ptr [rip + 0x1b69e27]  ; -> 02064C40
004FAE19  addss    xmm6, xmm2
004FAE1D  addss    xmm0, xmm7
004FAE21  movss    xmm1, dword ptr [rip + 0x1b69d57]  ; -> 02064B80
004FAE29  movaps   xmm7, xmm9
004FAE2D  mulss    xmm7, dword ptr [rip + 0x1b69e0f]  ; -> 02064C44
004FAE35  movaps   xmm8, xmm9
004FAE39  mulss    xmm9, dword ptr [rip + 0x1b69e0a]  ; -> 02064C4C
004FAE42  mulss    xmm8, dword ptr [rip + 0x1b69dfd]  ; -> 02064C48
004FAE4B  addss    xmm7, xmm4
004FAE4F  movss    xmm10, dword ptr [rip + 0x1b69d48]  ; -> 02064BA0
004FAE58  addss    xmm9, xmm6
004FAE5D  movss    xmm13, dword ptr [rip + 0x19079d6]  ; -> 01E0283C [f32 1]
004FAE66  movss    dword ptr [rip + 0x1b69de2], xmm0  ; -> 02064C50
004FAE6E  addss    xmm8, xmm5
004FAE73  movaps   xmm5, xmm0
004FAE76  movss    dword ptr [rip + 0x1b69dd6], xmm7  ; -> 02064C54
004FAE7E  movups   xmm0, xmmword ptr [rip + 0x1b69ceb]  ; -> 02064B70
004FAE85  movups   xmmword ptr [rsp + 0x50], xmm1
004FAE8A  shufps   xmm5, xmm5, 0
004FAE8E  mulps    xmm5, xmm0
004FAE91  movaps   xmm0, xmm7
004FAE94  mulss    xmm0, xmm1
004FAE98  movss    xmm1, dword ptr [rip + 0x1b69ce4]  ; -> 02064B84
004FAEA0  movaps   xmmword ptr [rsp + 0x90], xmm1
004FAEA8  movups   xmmword ptr [rip + 0x1b69c71], xmm5  ; -> 02064B20
004FAEAF  movss    xmm2, dword ptr [rip + 0x1b69c6d]  ; -> 02064B24
004FAEB7  addss    xmm5, xmm0
004FAEBB  movss    xmm3, dword ptr [rip + 0x1b69c65]  ; -> 02064B28
004FAEC3  movaps   xmm0, xmm7
004FAEC6  movss    xmm4, dword ptr [rip + 0x1b69c5e]  ; -> 02064B2C
004FAECE  mulss    xmm0, xmm1
004FAED2  movaps   xmm1, xmm7
004FAED5  movss    dword ptr [rip + 0x1b69d7a], xmm8  ; -> 02064C58
004FAEDE  movss    dword ptr [rip + 0x1b69d75], xmm9  ; -> 02064C5C
004FAEE7  addss    xmm2, xmm0
004FAEEB  movss    xmm0, dword ptr [rip + 0x1b69c95]  ; -> 02064B88
004FAEF3  mulss    xmm1, xmm0
004FAEF7  movaps   xmmword ptr [rsp + 0x80], xmm0
004FAEFF  movss    xmm0, dword ptr [rip + 0x1b69c85]  ; -> 02064B8C
004FAF07  mulss    xmm7, xmm0
004FAF0B  addss    xmm3, xmm1
004FAF0F  movaps   xmmword ptr [rsp + 0xa0], xmm0
004FAF17  movaps   xmm1, xmm8
004FAF1B  movss    xmm0, dword ptr [rip + 0x1b69c6d]  ; -> 02064B90
004FAF23  movups   xmmword ptr [rsp + 0x40], xmm0
004FAF28  mulss    xmm0, xmm8
004FAF2D  addss    xmm4, xmm7
004FAF31  addss    xmm5, xmm0
004FAF35  movss    xmm0, dword ptr [rip + 0x1b69c57]  ; -> 02064B94
004FAF3D  mulss    xmm1, xmm0
004FAF41  movaps   xmmword ptr [rsp + 0xb0], xmm0
004FAF49  movaps   xmm0, xmm8
004FAF4D  addss    xmm2, xmm1
004FAF51  movss    xmm1, dword ptr [rip + 0x1b69c3f]  ; -> 02064B98
004FAF59  mulss    xmm0, xmm1
004FAF5D  movaps   xmmword ptr [rsp + 0xc0], xmm1
004FAF65  movaps   xmm1, xmm9
004FAF69  addss    xmm3, xmm0
004FAF6D  movss    xmm0, dword ptr [rip + 0x1b69c27]  ; -> 02064B9C
004FAF75  mulss    xmm8, xmm0
004FAF7A  movaps   xmmword ptr [rsp + 0xd0], xmm0
004FAF82  movaps   xmm0, xmm9
004FAF86  mulss    xmm0, xmm10
004FAF8B  addss    xmm4, xmm8
004FAF90  addss    xmm0, xmm5
004FAF94  movss    dword ptr [rip + 0x1b69b90], xmm4  ; -> 02064B2C
004FAF9C  movss    dword ptr [rip + 0x1b69d1c], xmm0  ; -> 02064CC0
004FAFA4  movss    xmm0, dword ptr [rip + 0x1b69bf8]  ; -> 02064BA4
004FAFAC  mulss    xmm1, xmm0
004FAFB0  movaps   xmmword ptr [rsp + 0xe0], xmm0
004FAFB8  movaps   xmm0, xmm9
004FAFBC  addss    xmm1, xmm2
004FAFC0  movss    dword ptr [rip + 0x1b69cfc], xmm1  ; -> 02064CC4
004FAFC8  movss    xmm1, dword ptr [rip + 0x1b69bd8]  ; -> 02064BA8
004FAFD0  mulss    xmm0, xmm1
004FAFD4  movaps   xmmword ptr [rsp + 0xf0], xmm1
004FAFDC  addss    xmm0, xmm3
004FAFE0  movss    dword ptr [rip + 0x1b69ce0], xmm0  ; -> 02064CC8
004FAFE8  movss    xmm0, dword ptr [rip + 0x1b69bbc]  ; -> 02064BAC
004FAFF0  mulss    xmm9, xmm0
004FAFF5  movaps   xmmword ptr [rsp + 0x100], xmm0
004FAFFD  addss    xmm9, xmm4
004FB002  movss    dword ptr [rip + 0x1b69cc1], xmm9  ; -> 02064CCC
004FB00B  ucomiss  xmm9, xmm11
004FB00F  jp       0x4fb019  ; -> 004FB019
004FB011  jne      0x4fb019  ; -> 004FB019
004FB013  movaps   xmm0, xmm12
004FB017  jmp      0x4fb022  ; -> 004FB022
004FB019  movaps   xmm0, xmm13
004FB01D  divss    xmm0, xmm9
004FB022  movsx    r9d, word ptr [rip + 0x1b69d9a]  ; -> 02064DC4
004FB02A  movups   xmm1, xmmword ptr [rip + 0x1b69c8f]  ; -> 02064CC0
004FB031  movzx    r10d, word ptr [rip + 0x1b69ad3]  ; -> 02064B0C
004FB039  mov      edx, r9d
004FB03C  movzx    edx, word ptr [rip + 0x1b69d7d]  ; -> 02064DC0
004FB043  movss    xmm14, dword ptr [rip + 0x19077e4]  ; -> 01E02830 [u32 0x00000000]
004FB04C  lea      eax, [r9 + 0x46]
004FB050  movss    xmm9, dword ptr [rip + 0x19077df]  ; -> 01E02838 [u32 0x00000000]
004FB059  shl      eax, 4
004FB05C  movsxd   rcx, eax
004FB05F  lea      eax, [r9 + 0xc8]
004FB066  movss    dword ptr [rip + 0x1b69a92], xmm0  ; -> 02064B00
004FB06E  inc      r9w
004FB072  shufps   xmm0, xmm0, 0
004FB076  mulps    xmm1, xmm0
004FB079  shl      eax, 4
004FB07C  mov      word ptr [rip + 0x1b69d40], r9w  ; -> 02064DC4
004FB084  movups   xmm0, xmmword ptr [rip + 0x1b69bc5]  ; -> 02064C50
004FB08B  movups   xmmword ptr [rip + 0x1b69c2e], xmm1  ; -> 02064CC0
004FB092  movups   xmmword ptr [rcx + r15], xmm0
004FB097  movsxd   rcx, eax
004FB09A  movups   xmmword ptr [rcx + r15], xmm1
004FB09F  cmp      dx, r10w
004FB0A3  je       0x4fb0b2  ; -> 004FB0B2
004FB0A5  movss    xmm3, dword ptr [rip + 0x1b69ab3]  ; -> 02064B60
004FB0AD  jmp      0x4fa970  ; -> 004FA970
004FB0B2  mov      r8d, dword ptr [rip + 0x190776f]  ; -> 01E02828 [f32 1]
004FB0B9  movss    xmm8, dword ptr [rip + 0x1907772]  ; -> 01E02834 [u32 0x00000000]
004FB0C2  movss    xmm2, dword ptr [rip + 0x1b69c0a]  ; -> 02064CD4
004FB0CA  movss    xmm7, dword ptr [rip + 0x1b69c0a]  ; -> 02064CDC
004FB0D2  movaps   xmm1, xmm2
004FB0D5  mulss    xmm1, dword ptr [rip + 0x1b69b4b]  ; -> 02064C28
004FB0DD  movaps   xmm6, xmm7
004FB0E0  movdqu   xmm0, xmmword ptr [rip + 0x1b69b28]  ; -> 02064C10
004FB0E8  movss    xmm5, dword ptr [rip + 0x1b69be0]  ; -> 02064CD0
004FB0F0  mulss    xmm6, dword ptr [rip + 0x1b69b50]  ; -> 02064C48
004FB0F8  shufps   xmm5, xmm5, 0
004FB0FC  mulps    xmm5, xmm0
004FB0FF  movaps   xmm0, xmm2
004FB102  mulss    xmm0, dword ptr [rip + 0x1b69b16]  ; -> 02064C20
004FB10A  movups   xmmword ptr [rip + 0x1b69a0f], xmm5  ; -> 02064B20
004FB111  movss    xmm4, dword ptr [rip + 0x1b69a0f]  ; -> 02064B28
004FB119  addss    xmm5, xmm0
004FB11D  movss    xmm3, dword ptr [rip + 0x1b699ff]  ; -> 02064B24
004FB125  addss    xmm4, xmm1
004FB129  movss    xmm1, dword ptr [rip + 0x1b699fb]  ; -> 02064B2C
004FB131  movaps   xmm0, xmm2
004FB134  mulss    xmm0, dword ptr [rip + 0x1b69ae8]  ; -> 02064C24
004FB13C  mulss    xmm2, dword ptr [rip + 0x1b69ae8]  ; -> 02064C2C
004FB144  addss    xmm3, xmm0
004FB148  movss    xmm0, dword ptr [rip + 0x1b69b88]  ; -> 02064CD8
004FB150  addss    xmm1, xmm2
004FB154  movss    xmm2, dword ptr [rsp + 0x30]
004FB15A  mulss    xmm2, xmm0
004FB15E  addss    xmm5, xmm2
004FB162  movss    xmm2, dword ptr [rsp + 0x28]
004FB168  mulss    xmm2, xmm0
004FB16C  addss    xmm3, xmm2
004FB170  movss    xmm2, dword ptr [rsp + 0x2c]
004FB176  mulss    xmm2, xmm0
004FB17A  addss    xmm4, xmm2
004FB17E  movss    xmm2, dword ptr [rsp + 0x20]
004FB184  mulss    xmm2, xmm0
004FB188  movaps   xmm0, xmm7
004FB18B  mulss    xmm0, dword ptr [rip + 0x1b69aad]  ; -> 02064C40
004FB193  addss    xmm1, xmm2
004FB197  addss    xmm6, xmm4
004FB19B  movups   xmm4, xmmword ptr [rsp + 0x40]
004FB1A0  addss    xmm0, xmm5
004FB1A4  movaps   xmm5, xmm7
004FB1A7  mulss    xmm5, dword ptr [rip + 0x1b69a95]  ; -> 02064C44
004FB1AF  mulss    xmm7, dword ptr [rip + 0x1b69a95]  ; -> 02064C4C
004FB1B7  addss    xmm5, xmm3
004FB1BB  movss    dword ptr [rip + 0x1b69aed], xmm0  ; -> 02064CB0
004FB1C3  movaps   xmm3, xmm0
004FB1C6  mulss    xmm4, xmm6
004FB1CA  movups   xmm0, xmmword ptr [rip + 0x1b6999f]  ; -> 02064B70
004FB1D1  addss    xmm7, xmm1
004FB1D5  shufps   xmm3, xmm3, 0
004FB1D9  movups   xmm1, xmmword ptr [rsp + 0x50]
004FB1DE  mulps    xmm3, xmm0
004FB1E1  movaps   xmm0, xmm5
004FB1E4  mulss    xmm0, xmm1
004FB1E8  movaps   xmm1, xmm5
004FB1EB  mulss    xmm1, dword ptr [rsp + 0x80]
004FB1F4  movups   xmmword ptr [rip + 0x1b69925], xmm3  ; -> 02064B20
004FB1FB  movss    xmm2, dword ptr [rip + 0x1b69921]  ; -> 02064B24
004FB203  addss    xmm3, xmm0
004FB207  movaps   xmm0, xmm5
004FB20A  movss    dword ptr [rip + 0x1b69aa2], xmm5  ; -> 02064CB4
004FB212  mulss    xmm0, dword ptr [rsp + 0x90]
004FB21B  mulss    xmm5, dword ptr [rsp + 0xa0]
004FB224  addss    xmm3, xmm4
004FB228  movss    dword ptr [rip + 0x1b69a88], xmm6  ; -> 02064CB8
004FB230  movaps   xmm4, xmmword ptr [rsp + 0xb0]
004FB238  addss    xmm2, xmm0
004FB23C  movss    xmm0, dword ptr [rip + 0x1b698e4]  ; -> 02064B28
004FB244  mulss    xmm4, xmm6
004FB248  addss    xmm0, xmm1
004FB24C  movss    xmm1, dword ptr [rip + 0x1b698d8]  ; -> 02064B2C
004FB254  movss    dword ptr [rip + 0x1b69a60], xmm7  ; -> 02064CBC
004FB25C  addss    xmm1, xmm5
004FB260  addss    xmm2, xmm4
004FB264  movss    dword ptr [rip + 0x1b698b4], xmm3  ; -> 02064B20
004FB26C  movaps   xmm4, xmmword ptr [rsp + 0xc0]
004FB274  mulss    xmm4, xmm6
004FB278  movss    dword ptr [rip + 0x1b698a4], xmm2  ; -> 02064B24
004FB280  addss    xmm0, xmm4
004FB284  movss    dword ptr [rip + 0x1b6989c], xmm0  ; -> 02064B28
004FB28C  movaps   xmm4, xmmword ptr [rsp + 0xd0]
004FB294  mulss    xmm10, xmm7
004FB299  mulss    xmm4, xmm6
004FB29D  addss    xmm10, xmm3
004FB2A2  movaps   xmm3, xmmword ptr [rsp + 0xe0]
004FB2AA  mulss    xmm3, xmm7
004FB2AE  addss    xmm1, xmm4
004FB2B2  addss    xmm3, xmm2
004FB2B6  movss    dword ptr [rip + 0x1b69a01], xmm10  ; -> 02064CC0
004FB2BF  movaps   xmm2, xmmword ptr [rsp + 0xf0]
004FB2C7  mulss    xmm2, xmm7
004FB2CB  movss    dword ptr [rip + 0x1b69859], xmm1  ; -> 02064B2C
004FB2D3  movss    dword ptr [rip + 0x1b699e9], xmm3  ; -> 02064CC4
004FB2DB  addss    xmm2, xmm0
004FB2DF  movaps   xmm0, xmmword ptr [rsp + 0x100]
004FB2E7  mulss    xmm0, xmm7
004FB2EB  addss    xmm0, xmm1
004FB2EF  movss    dword ptr [rip + 0x1b699d1], xmm2  ; -> 02064CC8
004FB2F7  ucomiss  xmm0, xmm11
004FB2FB  movss    dword ptr [rip + 0x1b699c9], xmm0  ; -> 02064CCC
004FB303  jp       0x4fb30d  ; -> 004FB30D
004FB305  jne      0x4fb30d  ; -> 004FB30D
004FB307  movaps   xmm1, xmm12
004FB30B  jmp      0x4fb315  ; -> 004FB315
004FB30D  movaps   xmm1, xmm13
004FB311  divss    xmm1, xmm0
004FB315  movsx    edx, r9w
004FB319  movaps   xmm0, xmm1
004FB31C  movss    dword ptr [rip + 0x1b697dc], xmm1  ; -> 02064B00
004FB324  inc      r9w
004FB328  movups   xmm1, xmmword ptr [rip + 0x1b69991]  ; -> 02064CC0
004FB32F  movsx    ebx, r10w
004FB333  lea      eax, [rdx + 0x46]
004FB336  shufps   xmm0, xmm0, 0
004FB33A  shl      eax, 4
004FB33D  movsxd   rcx, eax
004FB340  lea      eax, [rdx + 0xc8]
004FB346  shl      eax, 4
004FB349  mulps    xmm1, xmm0
004FB34C  movups   xmm0, xmmword ptr [rip + 0x1b6995d]  ; -> 02064CB0
004FB353  movups   xmmword ptr [rcx + r15], xmm0
004FB358  movsxd   rcx, eax
004FB35B  lea      eax, [rdx + 0xc9]
004FB361  shl      eax, 4
004FB364  lea      edx, [r10 + 2]
004FB368  movups   xmmword ptr [rip + 0x1b69951], xmm1  ; -> 02064CC0
004FB36F  movups   xmmword ptr [rcx + r15], xmm1
004FB374  movsxd   rcx, eax
004FB377  lea      eax, [rbx + 0xd]
004FB37A  shl      eax, 4
004FB37D  movsxd   rdi, eax
004FB380  lea      eax, [rbx + 0xc]
004FB383  shl      eax, 4
004FB386  movups   xmmword ptr [rcx + r15], xmm1
004FB38B  movsxd   rcx, eax
004FB38E  and      dx, word ptr [rdi + r15 + 0xc]
004FB394  movups   xmm1, xmmword ptr [rcx + r15]
004FB399  movups   xmmword ptr [rip + 0x1b69970], xmm1  ; -> 02064D10
004FB3A0  cmp      dx, r10w
004FB3A4  je       0x4fb4a0  ; -> 004FB4A0
004FB3AA  test     r11d, r11d
004FB3AD  je       0x4fb45d  ; -> 004FB45D
004FB3B3  mov      eax, r8d
004FB3B6  shr      eax, 0x12
004FB3B9  xor      eax, r8d
004FB3BC  and      r8d, 0x3fffff
004FB3C3  shr      eax, 4
004FB3C6  or       r8d, 0x1fc00000
004FB3CD  and      eax, 1
004FB3D0  add      r8d, r8d
004FB3D3  or       eax, r8d
004FB3D6  mov      ecx, eax
004FB3D8  shr      ecx, 0x12
004FB3DB  xor      ecx, eax
004FB3DD  and      eax, 0x3fffff
004FB3E2  shr      ecx, 4
004FB3E5  or       eax, 0x1fc00000
004FB3EA  and      ecx, 1
004FB3ED  add      eax, eax
004FB3EF  or       ecx, eax
004FB3F1  mov      eax, ecx
004FB3F3  shr      eax, 0x12
004FB3F6  xor      eax, ecx
004FB3F8  and      ecx, 0x3fffff
004FB3FE  or       ecx, 0x1fc00000
004FB404  shr      eax, 4
004FB407  add      ecx, ecx
004FB409  and      eax, 1
004FB40C  or       eax, ecx
004FB40E  mov      ecx, eax
004FB410  shr      ecx, 0x12
004FB413  xor      ecx, eax
004FB415  and      eax, 0x3fffff
004FB41A  shr      ecx, 4
004FB41D  or       eax, 0x1fc00000
004FB422  and      ecx, 1
004FB425  add      eax, eax
004FB427  or       ecx, eax
004FB429  mov      r8d, ecx
004FB42C  shr      r8d, 0x12
004FB430  xor      r8d, ecx
004FB433  and      ecx, 0x3fffff
004FB439  or       ecx, 0x1fc00000
004FB43F  shr      r8d, 4
004FB443  add      ecx, ecx
004FB445  and      r8d, 1
004FB449  or       r8d, ecx
004FB44C  mov      dword ptr [rip + 0x19073d5], r8d  ; -> 01E02828 [f32 1]
004FB453  movss    xmm2, dword ptr [rip + 0x19073cd]  ; -> 01E02828 [f32 1]
004FB45B  jmp      0x4fb461  ; -> 004FB461
004FB45D  movaps   xmm2, xmm15
004FB461  movss    xmm3, dword ptr [rip + 0x4066d3]  ; -> 00901B3C [f32 1.5]
004FB469  lea      eax, [r10 + 0x10]
004FB46D  xor      ecx, ecx
004FB46F  movaps   xmm0, xmm13
004FB473  mulss    xmm0, xmm3
004FB477  comiss   xmm2, xmm0
004FB47A  seta     cl
004FB47D  shl      cx, 4
004FB481  and      cx, ax
004FB484  cmp      cx, r10w
004FB488  je       0x4fb4a8  ; -> 004FB4A8
004FB48A  mulps    xmm1, xmmword ptr [rip + 0x82728f]  ; -> 00D22720 [f32x4 -1, -1, -1, -1]
004FB491  movups   xmmword ptr [rip + 0x1b69878], xmm1  ; -> 02064D10
004FB498  jmp      0x4fb4a8  ; -> 004FB4A8
004FB49A  nop      word ptr [rax + rax]
004FB4A0  movss    xmm3, dword ptr [rip + 0x406694]  ; -> 00901B3C [f32 1.5]
004FB4A8  movaps   xmm0, xmm14
004FB4AC  lea      edx, [r10 + 1]
004FB4B0  mulss    xmm0, xmm14
004FB4B5  lea      eax, [rbx + 0x45]
004FB4B8  shl      eax, 4
004FB4BB  movsxd   rcx, eax
004FB4BE  movzx    eax, dx
004FB4C1  mov      word ptr [rip + 0x1b6991c], dx  ; -> 02064DE4
004FB4C8  movss    dword ptr [rip + 0x1b69840], xmm0  ; -> 02064D10
004FB4D0  movaps   xmm0, xmm9
004FB4D4  addss    xmm0, xmm13
004FB4D9  movups   xmmword ptr [rcx + r15], xmm1
004FB4DE  and      ax, word ptr [rdi + r15 + 0xc]
004FB4E4  movaps   xmm1, xmm8
004FB4E8  mov      word ptr [rip + 0x1b698f9], ax  ; -> 02064DE8
004FB4EF  addss    xmm1, dword ptr [rip + 0x17f0679]  ; -> 01CEBB70 [f32 0.5]
004FB4F7  movss    dword ptr [rip + 0x1b69819], xmm0  ; -> 02064D18
004FB4FF  movss    dword ptr [rip + 0x1b6980d], xmm1  ; -> 02064D14
004FB507  cmp      ax, r10w
004FB50B  je       0x4fb612  ; -> 004FB612
004FB511  test     r11d, r11d
004FB514  je       0x4fb5c4  ; -> 004FB5C4
004FB51A  mov      eax, r8d
004FB51D  shr      eax, 0x12
004FB520  xor      eax, r8d
004FB523  and      r8d, 0x3fffff
004FB52A  shr      eax, 4
004FB52D  or       r8d, 0x1fc00000
004FB534  and      eax, 1
004FB537  add      r8d, r8d
004FB53A  or       eax, r8d
004FB53D  mov      ecx, eax
004FB53F  shr      ecx, 0x12
004FB542  xor      ecx, eax
004FB544  and      eax, 0x3fffff
004FB549  shr      ecx, 4
004FB54C  or       eax, 0x1fc00000
004FB551  and      ecx, 1
004FB554  add      eax, eax
004FB556  or       ecx, eax
004FB558  mov      eax, ecx
004FB55A  shr      eax, 0x12
004FB55D  xor      eax, ecx
004FB55F  and      ecx, 0x3fffff
004FB565  or       ecx, 0x1fc00000
004FB56B  shr      eax, 4
004FB56E  add      ecx, ecx
004FB570  and      eax, 1
004FB573  or       eax, ecx
004FB575  mov      ecx, eax
004FB577  shr      ecx, 0x12
004FB57A  xor      ecx, eax
004FB57C  and      eax, 0x3fffff
004FB581  shr      ecx, 4
004FB584  or       eax, 0x1fc00000
004FB589  and      ecx, 1
004FB58C  add      eax, eax
004FB58E  or       ecx, eax
004FB590  mov      r8d, ecx
004FB593  shr      r8d, 0x12
004FB597  xor      r8d, ecx
004FB59A  and      ecx, 0x3fffff
004FB5A0  or       ecx, 0x1fc00000
004FB5A6  shr      r8d, 4
004FB5AA  add      ecx, ecx
004FB5AC  and      r8d, 1
004FB5B0  or       r8d, ecx
004FB5B3  mov      dword ptr [rip + 0x190726e], r8d  ; -> 01E02828 [f32 1]
004FB5BA  movss    xmm1, dword ptr [rip + 0x1907266]  ; -> 01E02828 [f32 1]
004FB5C2  jmp      0x4fb5c8  ; -> 004FB5C8
004FB5C4  movaps   xmm1, xmm15
004FB5C8  xor      ecx, ecx
004FB5CA  lea      eax, [r10 + 0x10]
004FB5CE  movaps   xmm0, xmm13
004FB5D2  mulss    xmm0, xmm3
004FB5D6  comiss   xmm1, xmm0
004FB5D9  seta     cl
004FB5DC  shl      cx, 4
004FB5E0  and      cx, ax
004FB5E3  mov      word ptr [rip + 0x1b697fe], cx  ; -> 02064DE8
004FB5EA  cmp      cx, r10w
004FB5EE  je       0x4fb612  ; -> 004FB612
004FB5F0  movaps   xmm0, xmm14
004FB5F4  movaps   xmm1, xmm9
004FB5F8  addss    xmm0, xmm13
004FB5FD  mulss    xmm1, xmm13
004FB602  movss    dword ptr [rip + 0x1b6970e], xmm1  ; -> 02064D18
004FB60A  movss    dword ptr [rip + 0x1b696fe], xmm0  ; -> 02064D10
004FB612  lea      eax, [rbx + 6]
004FB615  shl      eax, 4
004FB618  movsxd   r10, eax
004FB61B  lea      eax, [rbx + 0xb]
004FB61E  shl      eax, 4
004FB621  movsxd   rcx, eax
004FB624  movups   xmm0, xmmword ptr [r10 + r15]
004FB629  movups   xmmword ptr [rip + 0x1b69660], xmm0  ; -> 02064C90
004FB630  movups   xmmword ptr [rip + 0x1b69669], xmm0  ; -> 02064CA0
004FB637  movups   xmm0, xmmword ptr [rcx + r15]
004FB63C  movups   xmmword ptr [rip + 0x1b6966d], xmm0  ; -> 02064CB0
004FB643  test     r11d, r11d
004FB646  je       0x4fb6f6  ; -> 004FB6F6
004FB64C  mov      eax, r8d
004FB64F  shr      eax, 0x12
004FB652  xor      eax, r8d
004FB655  and      r8d, 0x3fffff
004FB65C  shr      eax, 4
004FB65F  or       r8d, 0x1fc00000
004FB666  and      eax, 1
004FB669  add      r8d, r8d
004FB66C  or       eax, r8d
004FB66F  mov      ecx, eax
004FB671  shr      ecx, 0x12
004FB674  xor      ecx, eax
004FB676  and      eax, 0x3fffff
004FB67B  shr      ecx, 4
004FB67E  or       eax, 0x1fc00000
004FB683  and      ecx, 1
004FB686  add      eax, eax
004FB688  or       ecx, eax
004FB68A  mov      eax, ecx
004FB68C  shr      eax, 0x12
004FB68F  xor      eax, ecx
004FB691  and      ecx, 0x3fffff
004FB697  or       ecx, 0x1fc00000
004FB69D  shr      eax, 4
004FB6A0  add      ecx, ecx
004FB6A2  and      eax, 1
004FB6A5  or       eax, ecx
004FB6A7  mov      ecx, eax
004FB6A9  shr      ecx, 0x12
004FB6AC  xor      ecx, eax
004FB6AE  and      eax, 0x3fffff
004FB6B3  shr      ecx, 4
004FB6B6  or       eax, 0x1fc00000
004FB6BB  and      ecx, 1
004FB6BE  add      eax, eax
004FB6C0  or       ecx, eax
004FB6C2  mov      r8d, ecx
004FB6C5  shr      r8d, 0x12
004FB6C9  xor      r8d, ecx
004FB6CC  and      ecx, 0x3fffff
004FB6D2  or       ecx, 0x1fc00000
004FB6D8  shr      r8d, 4
004FB6DC  add      ecx, ecx
004FB6DE  and      r8d, 1
004FB6E2  or       r8d, ecx
004FB6E5  mov      dword ptr [rip + 0x190713c], r8d  ; -> 01E02828 [f32 1]
004FB6EC  movss    xmm1, dword ptr [rip + 0x1907134]  ; -> 01E02828 [f32 1]
004FB6F4  jmp      0x4fb6fa  ; -> 004FB6FA
004FB6F6  movaps   xmm1, xmm15
004FB6FA  movss    xmm0, dword ptr [rip + 0x1b695ba]  ; -> 02064CBC
004FB702  subss    xmm1, xmm15
004FB707  movss    xmm2, dword ptr [rip + 0x1b695a9]  ; -> 02064CB8
004FB70F  lea      eax, [rbx + 0x44]
004FB712  movss    xmm3, dword ptr [rip + 0x1b6957e]  ; -> 02064C98
004FB71A  shl      eax, 4
004FB71D  movsxd   rcx, eax
004FB720  lea      eax, [rbx + 7]
004FB723  mulss    xmm0, xmm1
004FB727  shl      eax, 4
004FB72A  movss    xmm1, dword ptr [rip + 0x1b6957a]  ; -> 02064CAC
004FB732  cdqe     
004FB734  movss    dword ptr [rip + 0x1b69580], xmm0  ; -> 02064CBC
004FB73C  addss    xmm2, xmm0
004FB740  movss    xmm0, dword ptr [rip + 0x1b69560]  ; -> 02064CA8
004FB748  subss    xmm1, xmm0
004FB74C  mulss    xmm0, xmm2
004FB750  mulss    xmm3, xmm2
004FB754  mulss    xmm1, dword ptr [rip + 0x1b69408]  ; -> 02064B64
004FB75C  movss    dword ptr [rip + 0x1b69544], xmm0  ; -> 02064CA8
004FB764  movss    dword ptr [rip + 0x1b6954c], xmm2  ; -> 02064CB8
004FB76C  mulss    xmm1, xmm2
004FB770  movss    dword ptr [rip + 0x1b69520], xmm3  ; -> 02064C98
004FB778  movss    dword ptr [rip + 0x1b6952c], xmm1  ; -> 02064CAC
004FB780  movups   xmm0, xmmword ptr [rip + 0x1b69519]  ; -> 02064CA0
004FB787  movups   xmmword ptr [rcx + r15], xmm0
004FB78C  mov      rax, qword ptr [rax + r15]
004FB790  mov      qword ptr [rip + 0x1b693a9], rax  ; -> 02064B40
004FB797  test     r11d, r11d
004FB79A  je       0x4fb843  ; -> 004FB843
004FB7A0  mov      eax, r8d
004FB7A3  shr      eax, 0x12
004FB7A6  xor      eax, r8d
004FB7A9  and      r8d, 0x3fffff
004FB7B0  shr      eax, 4
004FB7B3  or       r8d, 0x1fc00000
004FB7BA  and      eax, 1
004FB7BD  add      r8d, r8d
004FB7C0  or       eax, r8d
004FB7C3  mov      ecx, eax
004FB7C5  shr      ecx, 0x12
004FB7C8  xor      ecx, eax
004FB7CA  and      eax, 0x3fffff
004FB7CF  or       eax, 0x1fc00000
004FB7D4  shr      ecx, 4
004FB7D7  add      eax, eax
004FB7D9  and      ecx, 1
004FB7DC  or       ecx, eax
004FB7DE  mov      eax, ecx
004FB7E0  shr      eax, 0x12
004FB7E3  xor      eax, ecx
004FB7E5  and      ecx, 0x3fffff
004FB7EB  or       ecx, 0x1fc00000
004FB7F1  shr      eax, 4
004FB7F4  add      ecx, ecx
004FB7F6  and      eax, 1
004FB7F9  or       eax, ecx
004FB7FB  mov      ecx, eax
004FB7FD  shr      ecx, 0x12
004FB800  xor      ecx, eax
004FB802  and      eax, 0x3fffff
004FB807  or       eax, 0x1fc00000
004FB80C  shr      ecx, 4
004FB80F  add      eax, eax
004FB811  and      ecx, 1
004FB814  or       ecx, eax
004FB816  mov      eax, ecx
004FB818  shr      eax, 0x12
004FB81B  xor      eax, ecx
004FB81D  and      ecx, 0x3fffff
004FB823  or       ecx, 0x1fc00000
004FB829  shr      eax, 4
004FB82C  add      ecx, ecx
004FB82E  and      eax, 1
004FB831  or       eax, ecx
004FB833  mov      dword ptr [rip + 0x1906fef], eax  ; -> 01E02828 [f32 1]
004FB839  movss    xmm1, dword ptr [rip + 0x1906fe7]  ; -> 01E02828 [f32 1]
004FB841  jmp      0x4fb847  ; -> 004FB847
004FB843  movaps   xmm1, xmm15
004FB847  movups   xmm0, xmmword ptr [r10 + r15]
004FB84C  lea      eax, [rbx + 0xc8]
004FB852  dec      r9w
004FB856  subss    xmm1, xmm15
004FB85B  movss    dword ptr [rip + 0x1b693ec], xmm14  ; -> 02064C50
004FB864  movups   xmmword ptr [rip + 0x1b69435], xmm0  ; -> 02064CA0
004FB86B  shl      eax, 4
004FB86E  movss    xmm0, dword ptr [rip + 0x1b692ce]  ; -> 02064B44
004FB876  movsxd   rcx, eax
004FB879  mulss    xmm0, xmm1
004FB87D  movsx    eax, dx
004FB880  add      eax, 0xc8
004FB885  movss    dword ptr [rip + 0x1b69423], xmm1  ; -> 02064CB0
004FB88D  movups   xmm1, xmmword ptr [rcx + r15]
004FB892  shl      eax, 4
004FB895  movss    dword ptr [rip + 0x1b692a7], xmm0  ; -> 02064B44
004FB89D  addss    xmm0, dword ptr [rip + 0x1b6929b]  ; -> 02064B40
004FB8A5  movups   xmmword ptr [rip + 0x1b693c4], xmm1  ; -> 02064C70
004FB8AC  cdqe     
004FB8AE  movss    dword ptr [rip + 0x1b6939d], xmm8  ; -> 02064C54
004FB8B7  movss    dword ptr [rip + 0x1b69398], xmm9  ; -> 02064C58
004FB8C0  mulss    xmm0, xmm3
004FB8C4  mov      dword ptr [rip + 0x1b69236], 0x3f800000  ; -> 02064B04
004FB8CE  movss    dword ptr [rip + 0x1b69385], xmm13  ; -> 02064C5C
004FB8D7  mov      word ptr [rip + 0x1b694ea], dx  ; -> 02064DC8
004FB8DE  movss    dword ptr [rip + 0x1b6925a], xmm0  ; -> 02064B40
004FB8E6  movups   xmm0, xmmword ptr [rax + r15]
004FB8EB  mov      word ptr [rip + 0x1b694d1], r9w  ; -> 02064DC4
004FB8F3  movups   xmm2, xmm0
004FB8F6  movups   xmmword ptr [rip + 0x1b69383], xmm0  ; -> 02064C80
004FB8FD  movss    dword ptr [rip + 0x1b6937b], xmm2  ; -> 02064C80
004FB905  subss    xmm0, xmm1
004FB909  shufps   xmm2, xmm2, 0x55
004FB90D  movss    dword ptr [rip + 0x1b6936f], xmm2  ; -> 02064C84
004FB915  subss    xmm2, dword ptr [rip + 0x1b69357]  ; -> 02064C74
004FB91D  ucomiss  xmm0, xmm11
004FB921  movss    dword ptr [rip + 0x1b6934b], xmm2  ; -> 02064C74
004FB929  movss    dword ptr [rip + 0x1b6933f], xmm0  ; -> 02064C70
004FB931  jp       0x4fb935  ; -> 004FB935
004FB933  je       0x4fb93d  ; -> 004FB93D
004FB935  ucomiss  xmm2, xmm11
004FB939  jp       0x4fb952  ; -> 004FB952
004FB93B  jne      0x4fb952  ; -> 004FB952
004FB93D  call     0x22cc40  ; -> 0022CC40 fn
004FB942  movss    xmm2, dword ptr [rip + 0x1b6932a]  ; -> 02064C74
004FB94A  movss    xmm0, dword ptr [rip + 0x1b6931e]  ; -> 02064C70
004FB952  comiss   xmm11, xmm0
004FB956  ja       0x4fb95e  ; -> 004FB95E
004FB958  comiss   xmm11, xmm2
004FB95C  jbe      0x4fb963  ; -> 004FB963
004FB95E  call     0x22cc30  ; -> 0022CC30 fn
004FB963  call     0x22cc20  ; -> 0022CC20 fn
004FB968  movss    xmm8, dword ptr [rip + 0x1b69303]  ; -> 02064C74
004FB971  movss    xmm9, dword ptr [rip + 0x1906eba]  ; -> 01E02834 [u32 0x00000000]
004FB97A  addss    xmm8, dword ptr [rip + 0x1906ead]  ; -> 01E02830 [u32 0x00000000]
004FB983  subss    xmm9, dword ptr [rip + 0x1b692e4]  ; -> 02064C70
004FB98C  movss    xmm7, dword ptr [rip + 0x1906ea8]  ; -> 01E0283C [f32 1]
004FB994  movsd    xmm10, qword ptr [rip + 0x17f03e3]  ; -> 01CEBD80 [u64 0x7FFFFFFFFFFFFFFF]
004FB99D  movaps   xmm1, xmm8
004FB9A1  movaps   xmm0, xmm9
004FB9A5  mulss    xmm1, xmm8
004FB9AA  mulss    xmm0, xmm9
004FB9AF  mulss    xmm1, xmm7
004FB9B3  mulss    xmm0, xmm7
004FB9B7  addss    xmm0, xmm1
004FB9BB  cvtps2pd xmm0, xmm0
004FB9BE  andps    xmm0, xmm10
004FB9C2  cvtpd2ps xmm0, xmm0
004FB9C6  call     0x861f14  ; -> 00861F14 fn
004FB9CB  movaps   xmm1, xmm0
004FB9CE  ucomiss  xmm1, xmm11
004FB9D2  jp       0x4fb9dc  ; -> 004FB9DC
004FB9D4  jne      0x4fb9dc  ; -> 004FB9DC
004FB9D6  movaps   xmm0, xmm12
004FB9DA  jmp      0x4fb9e3  ; -> 004FB9E3
004FB9DC  movaps   xmm0, xmm7
004FB9DF  divss    xmm0, xmm1
004FB9E3  movss    xmm6, dword ptr [rip + 0x1b69265]  ; -> 02064C50
004FB9EB  mulss    xmm8, xmm0
004FB9F0  mov      dword ptr [rip + 0x1b6910a], 0xbf800000  ; -> 02064B04
004FB9FA  mulss    xmm9, xmm0
004FB9FF  addss    xmm6, xmm8
004FBA04  movss    dword ptr [rip + 0x1b692e3], xmm8  ; -> 02064CF0
004FBA0D  movss    xmm8, dword ptr [rip + 0x1b6923e]  ; -> 02064C54
004FBA16  addss    xmm8, xmm9
004FBA1B  movss    dword ptr [rip + 0x1b692d0], xmm9  ; -> 02064CF4
004FBA24  mulss    xmm6, dword ptr [rip + 0x17f0270]  ; -> 01CEBC9C [f32 -1]
004FBA2C  movaps   xmm0, xmm8
004FBA30  mulss    xmm0, xmm8
004FBA35  movaps   xmm1, xmm6
004FBA38  mulss    xmm1, xmm6
004FBA3C  mulss    xmm0, xmm7
004FBA40  mulss    xmm1, xmm7
004FBA44  addss    xmm0, xmm1
004FBA48  movss    dword ptr [rip + 0x1b690dc], xmm1  ; -> 02064B2C
004FBA50  cvtps2pd xmm0, xmm0
004FBA53  andps    xmm0, xmm10
004FBA57  cvtpd2ps xmm0, xmm0
004FBA5B  call     0x861f14  ; -> 00861F14 fn
004FBA60  ucomiss  xmm0, xmm11
004FBA64  jp       0x4fba6e  ; -> 004FBA6E
004FBA66  jne      0x4fba6e  ; -> 004FBA6E
004FBA68  movaps   xmm7, xmm12
004FBA6C  jmp      0x4fba72  ; -> 004FBA72
004FBA6E  divss    xmm7, xmm0
004FBA72  movsx    edx, word ptr [rip + 0x1b69093]  ; -> 02064B0C
004FBA79  mulss    xmm8, xmm7
004FBA7E  mulss    xmm6, xmm7
004FBA82  lea      eax, [rdx + 0x1d]
004FBA85  movss    dword ptr [rip + 0x1b69073], xmm7  ; -> 02064B00
004FBA8D  mulss    xmm8, dword ptr [rip + 0x1b690aa]  ; -> 02064B40
004FBA96  shl      eax, 4
004FBA99  mulss    xmm6, dword ptr [rip + 0x1b6909f]  ; -> 02064B40
004FBAA1  movsxd   rcx, eax
004FBAA4  lea      eax, [rdx + 0x1e]
004FBAA7  shl      eax, 4
004FBAAA  movss    dword ptr [rip + 0x1b691a1], xmm8  ; -> 02064C54
004FBAB3  movss    dword ptr [rip + 0x1b69195], xmm6  ; -> 02064C50
004FBABB  movups   xmm0, xmmword ptr [rcx + r15]
004FBAC0  movsxd   rcx, eax
004FBAC3  lea      eax, [rdx + 0x1f]
004FBAC6  shl      eax, 4
004FBAC9  movups   xmmword ptr [rip + 0x1b691c0], xmm0  ; -> 02064C90
004FBAD0  movups   xmm0, xmmword ptr [rcx + r15]
004FBAD5  movsxd   rcx, eax
004FBAD8  lea      eax, [rdx + 0x20]
004FBADB  shl      eax, 4
004FBADE  movups   xmmword ptr [rip + 0x1b691bb], xmm0  ; -> 02064CA0
004FBAE5  movups   xmm0, xmmword ptr [rcx + r15]
004FBAEA  movsxd   rcx, eax
004FBAED  movsx    eax, word ptr [rip + 0x1b692d4]  ; -> 02064DC8
004FBAF4  movups   xmmword ptr [rip + 0x1b691b5], xmm0  ; -> 02064CB0
004FBAFB  add      eax, 0x45
004FBAFE  movups   xmm0, xmmword ptr [rcx + r15]
004FBB03  shl      eax, 4
004FBB06  movsxd   rcx, eax
004FBB09  movups   xmmword ptr [rip + 0x1b691b0], xmm0  ; -> 02064CC0
004FBB10  movups   xmm0, xmmword ptr [rcx + r15]
004FBB15  movups   xmmword ptr [rip + 0x1b69044], xmm0  ; -> 02064B60
004FBB1C  movups   xmmword ptr [rip + 0x1b6905d], xmm0  ; -> 02064B80
004FBB23  movups   xmm2, xmm0
004FBB26  movups   xmm3, xmm0
004FBB29  movups   xmmword ptr [rip + 0x1b69040], xmm0  ; -> 02064B70
004FBB30  movss    xmm0, dword ptr [rip + 0x1b6902c]  ; -> 02064B64
004FBB38  subss    xmm3, xmm6
004FBB3C  addss    xmm0, xmm8
004FBB41  addss    xmm2, xmm6
004FBB45  ucomiss  xmm3, xmm11
004FBB49  movss    dword ptr [rip + 0x1b69013], xmm0  ; -> 02064B64
004FBB51  movss    xmm0, dword ptr [rip + 0x1b6902b]  ; -> 02064B84
004FBB59  subss    xmm0, xmm8
004FBB5E  movss    dword ptr [rip + 0x1b68ffa], xmm2  ; -> 02064B60
004FBB66  movss    dword ptr [rip + 0x1b69012], xmm3  ; -> 02064B80
004FBB6E  movss    dword ptr [rip + 0x1b6900e], xmm0  ; -> 02064B84
004FBB76  jp       0x4fbb7a  ; -> 004FBB7A
004FBB78  je       0x4fbb82  ; -> 004FBB82
004FBB7A  ucomiss  xmm0, xmm11
004FBB7E  jp       0x4fbb97  ; -> 004FBB97
004FBB80  jne      0x4fbb97  ; -> 004FBB97
004FBB82  call     0x22cc40  ; -> 0022CC40 fn
004FBB87  movss    xmm0, dword ptr [rip + 0x1b68ff5]  ; -> 02064B84
004FBB8F  movss    xmm3, dword ptr [rip + 0x1b68fe9]  ; -> 02064B80
004FBB97  comiss   xmm11, xmm3
004FBB9B  ja       0x4fbba3  ; -> 004FBBA3
004FBB9D  comiss   xmm11, xmm0
004FBBA1  jbe      0x4fbba8  ; -> 004FBBA8
004FBBA3  call     0x22cc30  ; -> 0022CC30 fn
004FBBA8  call     0x22cc20  ; -> 0022CC20 fn
004FBBAD  movss    xmm2, dword ptr [rip + 0x1b68faf]  ; -> 02064B64
004FBBB5  movups   xmm0, xmmword ptr [rip + 0x1b690d4]  ; -> 02064C90
004FBBBC  movss    xmm6, dword ptr [rip + 0x1b68f9c]  ; -> 02064B60
004FBBC4  movss    xmm13, dword ptr [rip + 0x1b690d7]  ; -> 02064CA4
004FBBCD  movss    xmm8, dword ptr [rip + 0x1b690ea]  ; -> 02064CC0
004FBBD6  movss    xmm10, dword ptr [rip + 0x1b690e5]  ; -> 02064CC4
004FBBDF  movss    xmm14, dword ptr [rip + 0x1b690e0]  ; -> 02064CC8
004FBBE8  movss    xmm9, dword ptr [rip + 0x1906c4b]  ; -> 01E0283C [f32 1]
004FBBF1  shufps   xmm6, xmm6, 0
004FBBF5  mulps    xmm6, xmm0
004FBBF8  movaps   xmm0, xmm2
004FBBFB  mulss    xmm0, dword ptr [rip + 0x1b6909d]  ; -> 02064CA0
004FBC03  movss    dword ptr [rsp + 0x38], xmm13
004FBC0A  movups   xmmword ptr [rip + 0x1b68f0f], xmm6  ; -> 02064B20
004FBC11  movss    xmm3, dword ptr [rip + 0x1b68f0b]  ; -> 02064B24
004FBC19  addss    xmm6, xmm0
004FBC1D  movss    xmm4, dword ptr [rip + 0x1b68f03]  ; -> 02064B28
004FBC25  movaps   xmm0, xmm13
004FBC29  movss    xmm5, dword ptr [rip + 0x1b68efb]  ; -> 02064B2C
004FBC31  mulss    xmm0, xmm2
004FBC35  addss    xmm3, xmm0
004FBC39  movss    xmm0, dword ptr [rip + 0x1b69067]  ; -> 02064CA8
004FBC41  movaps   xmm1, xmm0
004FBC44  movss    dword ptr [rsp + 0x20], xmm0
004FBC4A  movss    xmm0, dword ptr [rip + 0x1b6905a]  ; -> 02064CAC
004FBC52  movss    dword ptr [rsp + 0x2c], xmm0
004FBC58  mulss    xmm0, xmm2
004FBC5C  mulss    xmm1, xmm2
004FBC60  movss    xmm2, dword ptr [rip + 0x1b68f00]  ; -> 02064B68
004FBC68  addss    xmm5, xmm0
004FBC6C  movss    xmm0, dword ptr [rip + 0x1b69040]  ; -> 02064CB4
004FBC74  movss    dword ptr [rsp + 0x28], xmm0
004FBC7A  addss    xmm4, xmm1
004FBC7E  mulss    xmm0, xmm2
004FBC82  movaps   xmm1, xmm2
004FBC85  mulss    xmm1, dword ptr [rip + 0x1b69023]  ; -> 02064CB0
004FBC8D  addss    xmm3, xmm0
004FBC91  movaps   xmm0, xmm8
004FBC95  addss    xmm6, xmm1
004FBC99  movaps   xmm1, xmm2
004FBC9C  mulss    xmm1, dword ptr [rip + 0x1b69014]  ; -> 02064CB8
004FBCA4  mulss    xmm2, dword ptr [rip + 0x1b69010]  ; -> 02064CBC
004FBCAC  addss    xmm4, xmm1
004FBCB0  movaps   xmm1, xmm14
004FBCB4  addss    xmm5, xmm2
004FBCB8  movss    xmm2, dword ptr [rip + 0x1b68eac]  ; -> 02064B6C
004FBCC0  mulss    xmm0, xmm2
004FBCC4  mulss    xmm1, xmm2
004FBCC8  addss    xmm0, xmm6
004FBCCC  addss    xmm1, xmm4
004FBCD0  movss    dword ptr [rip + 0x1b68e88], xmm0  ; -> 02064B60
004FBCD8  movaps   xmm0, xmm10
004FBCDC  mulss    xmm0, xmm2
004FBCE0  movss    dword ptr [rip + 0x1b68e80], xmm1  ; -> 02064B68
004FBCE8  addss    xmm0, xmm3
004FBCEC  movss    dword ptr [rip + 0x1b68e70], xmm0  ; -> 02064B64
004FBCF4  movss    xmm0, dword ptr [rip + 0x1b68fd0]  ; -> 02064CCC
004FBCFC  mulss    xmm0, xmm2
004FBD00  addss    xmm0, xmm5
004FBD04  ucomiss  xmm0, xmm11
004FBD08  movss    dword ptr [rip + 0x1b68e5c], xmm0  ; -> 02064B6C
004FBD10  jp       0x4fbd1a  ; -> 004FBD1A
004FBD12  jne      0x4fbd1a  ; -> 004FBD1A
004FBD14  movaps   xmm7, xmm12
004FBD18  jmp      0x4fbd22  ; -> 004FBD22
004FBD1A  movaps   xmm7, xmm9
004FBD1E  divss    xmm7, xmm0
004FBD22  movss    xmm2, dword ptr [rip + 0x1b68e4a]  ; -> 02064B74
004FBD2A  movss    xmm6, dword ptr [rip + 0x1b68e3e]  ; -> 02064B70
004FBD32  movaps   xmm1, xmm2
004FBD35  mulss    xmm1, dword ptr [rsp + 0x20]
004FBD3B  movups   xmm0, xmmword ptr [rip + 0x1b68f4e]  ; -> 02064C90
004FBD42  shufps   xmm6, xmm6, 0
004FBD46  mulps    xmm6, xmm0
004FBD49  movaps   xmm0, xmm2
004FBD4C  mulss    xmm0, dword ptr [rip + 0x1b68f4c]  ; -> 02064CA0
004FBD54  movups   xmmword ptr [rip + 0x1b68dc5], xmm6  ; -> 02064B20
004FBD5B  movss    xmm5, dword ptr [rip + 0x1b68dc9]  ; -> 02064B2C
004FBD63  addss    xmm6, xmm0
004FBD67  movss    xmm3, dword ptr [rip + 0x1b68db5]  ; -> 02064B24
004FBD6F  movaps   xmm0, xmm2
004FBD72  mulss    xmm2, dword ptr [rsp + 0x2c]
004FBD78  movss    xmm4, dword ptr [rip + 0x1b68da8]  ; -> 02064B28
004FBD80  mulss    xmm0, xmm13
004FBD85  addss    xmm4, xmm1
004FBD89  movups   xmm13, xmmword ptr [rip + 0x1b68dcf]  ; -> 02064B60
004FBD91  addss    xmm5, xmm2
004FBD95  movss    xmm2, dword ptr [rip + 0x1b68ddb]  ; -> 02064B78
004FBD9D  addss    xmm3, xmm0
004FBDA1  movaps   xmm1, xmm2
004FBDA4  mulss    xmm1, dword ptr [rsp + 0x28]
004FBDAA  movaps   xmm0, xmm2
004FBDAD  mulss    xmm0, dword ptr [rip + 0x1b68efb]  ; -> 02064CB0
004FBDB5  addss    xmm3, xmm1
004FBDB9  movaps   xmm1, xmm14
004FBDBD  addss    xmm6, xmm0
004FBDC1  movaps   xmm0, xmm2
004FBDC4  mulss    xmm0, dword ptr [rip + 0x1b68eec]  ; -> 02064CB8
004FBDCC  mulss    xmm2, dword ptr [rip + 0x1b68ee8]  ; -> 02064CBC
004FBDD4  addss    xmm4, xmm0
004FBDD8  movaps   xmm0, xmm8
004FBDDC  addss    xmm5, xmm2
004FBDE0  movss    xmm2, dword ptr [rip + 0x1b68d94]  ; -> 02064B7C
004FBDE8  mulss    xmm0, xmm2
004FBDEC  mulss    xmm1, xmm2
004FBDF0  addss    xmm0, xmm6
004FBDF4  addss    xmm1, xmm4
004FBDF8  movss    dword ptr [rip + 0x1b68d70], xmm0  ; -> 02064B70
004FBE00  movaps   xmm0, xmm10
004FBE04  mulss    xmm0, xmm2
004FBE08  mulss    xmm2, dword ptr [rip + 0x1b68ebc]  ; -> 02064CCC
004FBE10  addss    xmm0, xmm3
004FBE14  movss    dword ptr [rip + 0x1b68d5c], xmm1  ; -> 02064B78
004FBE1C  addss    xmm2, xmm5
004FBE20  movss    dword ptr [rip + 0x1b68d4c], xmm0  ; -> 02064B74
004FBE28  movss    xmm0, dword ptr [rip + 0x1906a04]  ; -> 01E02834 [u32 0x00000000]
004FBE30  ucomiss  xmm2, xmm11
004FBE34  addss    xmm0, dword ptr [rip + 0x1b68ed4]  ; -> 02064D10
004FBE3C  movss    dword ptr [rip + 0x1b68d38], xmm2  ; -> 02064B7C
004FBE44  movss    dword ptr [rip + 0x1b68d48], xmm0  ; -> 02064B94
004FBE4C  movss    xmm0, dword ptr [rip + 0x19069e4]  ; -> 01E02838 [u32 0x00000000]
004FBE54  addss    xmm0, xmm9
004FBE59  movss    dword ptr [rsp + 0x34], xmm0
004FBE5F  movss    dword ptr [rip + 0x1b68d31], xmm0  ; -> 02064B98
004FBE67  movaps   xmm0, xmm7
004FBE6A  mulss    xmm7, xmm9
004FBE6F  shufps   xmm0, xmm0, 0
004FBE73  mulps    xmm13, xmm0
004FBE77  movss    dword ptr [rip + 0x1b68d1d], xmm7  ; -> 02064B9C
004FBE7F  jp       0x4fbe89  ; -> 004FBE89
004FBE81  jne      0x4fbe89  ; -> 004FBE89
004FBE83  movaps   xmm6, xmm12
004FBE87  jmp      0x4fbe91  ; -> 004FBE91
004FBE89  movaps   xmm6, xmm9
004FBE8D  divss    xmm6, xmm2
004FBE91  movss    xmm1, dword ptr [rip + 0x1b68ceb]  ; -> 02064B84
004FBE99  movss    xmm5, dword ptr [rip + 0x1b68cdf]  ; -> 02064B80
004FBEA1  movups   xmm0, xmmword ptr [rip + 0x1b68de8]  ; -> 02064C90
004FBEA8  movss    xmm3, dword ptr [rsp + 0x38]
004FBEAE  mulss    xmm3, xmm1
004FBEB2  shufps   xmm5, xmm5, 0
004FBEB6  mulps    xmm5, xmm0
004FBEB9  movaps   xmm0, xmm1
004FBEBC  mulss    xmm0, dword ptr [rip + 0x1b68ddc]  ; -> 02064CA0
004FBEC4  movups   xmmword ptr [rip + 0x1b68c55], xmm5  ; -> 02064B20
004FBECB  movss    xmm2, dword ptr [rip + 0x1b68c51]  ; -> 02064B24
004FBED3  addss    xmm5, xmm0
004FBED7  movss    xmm0, dword ptr [rsp + 0x20]
004FBEDD  addss    xmm2, xmm3
004FBEE1  movss    xmm3, dword ptr [rip + 0x1b68c3f]  ; -> 02064B28
004FBEE9  movss    xmm4, dword ptr [rip + 0x1b68c3b]  ; -> 02064B2C
004FBEF1  mulss    xmm0, xmm1
004FBEF5  addss    xmm3, xmm0
004FBEF9  movss    xmm0, dword ptr [rsp + 0x2c]
004FBEFF  mulss    xmm0, xmm1
004FBF03  movss    xmm1, dword ptr [rip + 0x1b68c7d]  ; -> 02064B88
004FBF0B  addss    xmm4, xmm0
004FBF0F  movaps   xmm0, xmm1
004FBF12  mulss    xmm0, dword ptr [rip + 0x1b68d96]  ; -> 02064CB0
004FBF1A  addss    xmm5, xmm0
004FBF1E  movss    xmm0, dword ptr [rsp + 0x28]
004FBF24  mulss    xmm0, xmm1
004FBF28  addss    xmm2, xmm0
004FBF2C  movss    dword ptr [rip + 0x1b68bec], xmm5  ; -> 02064B20
004FBF34  movaps   xmm0, xmm1
004FBF37  mulss    xmm1, dword ptr [rip + 0x1b68d7d]  ; -> 02064CBC
004FBF3F  mulss    xmm0, dword ptr [rip + 0x1b68d71]  ; -> 02064CB8
004FBF47  addss    xmm4, xmm1
004FBF4B  movss    dword ptr [rip + 0x1b68bd1], xmm2  ; -> 02064B24
004FBF53  movss    xmm1, dword ptr [rip + 0x1b68c31]  ; -> 02064B8C
004FBF5B  addss    xmm3, xmm0
004FBF5F  mulss    xmm14, xmm1
004FBF64  movss    xmm0, dword ptr [rip + 0x1b68da8]  ; -> 02064D14
004FBF6C  mulss    xmm10, xmm1
004FBF71  addss    xmm14, xmm3
004FBF76  mulss    xmm8, xmm1
004FBF7B  mulss    xmm1, dword ptr [rip + 0x1b68d49]  ; -> 02064CCC
004FBF83  addss    xmm10, xmm2
004FBF88  addss    xmm8, xmm5
004FBF8D  movss    dword ptr [rip + 0x1b68b93], xmm3  ; -> 02064B28
004FBF95  movss    xmm3, dword ptr [rsp + 0x34]
004FBF9B  addss    xmm1, xmm4
004FBF9F  movss    dword ptr [rip + 0x1b68be0], xmm14  ; -> 02064B88
004FBFA8  movups   xmm14, xmmword ptr [rip + 0x1b68bc0]  ; -> 02064B70
004FBFB0  movss    dword ptr [rip + 0x1b68bcb], xmm10  ; -> 02064B84
004FBFB9  movss    xmm10, dword ptr [rip + 0x1906872]  ; -> 01E02834 [u32 0x00000000]
004FBFC2  ucomiss  xmm1, xmm11
004FBFC6  addss    xmm0, xmm10
004FBFCB  movss    dword ptr [rip + 0x1b68b59], xmm4  ; -> 02064B2C
004FBFD3  movss    dword ptr [rip + 0x1b68ba4], xmm8  ; -> 02064B80
004FBFDC  movss    dword ptr [rip + 0x1b68ba8], xmm1  ; -> 02064B8C
004FBFE4  movss    dword ptr [rip + 0x1b68bbc], xmm3  ; -> 02064BA8
004FBFEC  movss    dword ptr [rip + 0x1b68bb0], xmm0  ; -> 02064BA4
004FBFF4  movaps   xmm0, xmm6
004FBFF7  mulss    xmm6, xmm9
004FBFFC  shufps   xmm0, xmm0, 0
004FC000  mulps    xmm14, xmm0
004FC004  movss    dword ptr [rip + 0x1b68ba0], xmm6  ; -> 02064BAC
004FC00C  jp       0x4fc016  ; -> 004FC016
004FC00E  jne      0x4fc016  ; -> 004FC016
004FC010  movaps   xmm2, xmm12
004FC014  jmp      0x4fc01e  ; -> 004FC01E
004FC016  movaps   xmm2, xmm9
004FC01A  divss    xmm2, xmm1
004FC01E  movzx    r11d, word ptr [rip + 0x1b68da2]  ; -> 02064DC8
004FC026  xor      ecx, ecx
004FC028  comiss   xmm13, dword ptr [rip + 0x1b68b00]  ; -> 02064B30
004FC030  movzx    ebx, word ptr [rip + 0x1b68ad5]  ; -> 02064B0C
004FC037  lea      r8d, [r12 + rbx]
004FC03B  movzx    r9d, r8w
004FC03F  movss    xmm1, dword ptr [rip + 0x1b68c45]  ; -> 02064C8C
004FC047  movaps   xmm0, xmm10
004FC04B  addss    xmm0, dword ptr [rip + 0x1b68cc5]  ; -> 02064D18
004FC053  seta     cl
004FC056  movss    dword ptr [rip + 0x1b68b5a], xmm3  ; -> 02064BB8
004FC05E  movups   xmm8, xmmword ptr [rip + 0x1b68b1a]  ; -> 02064B80
004FC066  xor      eax, eax
004FC068  add      cx, cx
004FC06B  movss    dword ptr [rip + 0x1b68a8d], xmm2  ; -> 02064B00
004FC073  movaps   xmm4, xmm13
004FC077  movss    dword ptr [rip + 0x1b68b35], xmm0  ; -> 02064BB4
004FC07F  movaps   xmm3, xmm13
004FC083  shufps   xmm4, xmm13, 0x55
004FC088  movaps   xmm0, xmm2
004FC08B  comiss   xmm4, dword ptr [rip + 0x1b68aa2]  ; -> 02064B34
004FC092  shufps   xmm0, xmm0, 0
004FC096  mulps    xmm8, xmm0
004FC09A  seta     al
004FC09D  movups   xmm0, xmmword ptr [rip + 0x1b68c4c]  ; -> 02064CF0
004FC0A4  add      cx, ax
004FC0A7  xor      eax, eax
004FC0A9  add      cx, cx
004FC0AC  mulss    xmm2, xmm9
004FC0B1  movss    xmm9, dword ptr [rip + 0x1b68bc6]  ; -> 02064C80
004FC0BA  shufps   xmm3, xmm13, 0xaa
004FC0BF  comiss   xmm3, dword ptr [rip + 0x1b68a72]  ; -> 02064B38
004FC0C6  movups   xmmword ptr [rip + 0x1b68b83], xmm0  ; -> 02064C50
004FC0CD  movss    xmm0, dword ptr [rip + 0x1b68bb3]  ; -> 02064C88
004FC0D5  seta     al
004FC0D8  add      cx, ax
004FC0DB  movss    dword ptr [rip + 0x1b68ad9], xmm2  ; -> 02064BBC
004FC0E3  movss    xmm2, dword ptr [rip + 0x1906745]  ; -> 01E02830 [u32 0x00000000]
004FC0EB  xor      edx, edx
004FC0ED  shl      cx, 5
004FC0F1  comiss   xmm2, xmm13
004FC0F5  movss    dword ptr [rip + 0x1b68b7b], xmm0  ; -> 02064C78
004FC0FD  movss    xmm0, dword ptr [rip + 0x190672f]  ; -> 01E02834 [u32 0x00000000]
004FC105  seta     dl
004FC108  movss    dword ptr [rip + 0x1b68b6c], xmm1  ; -> 02064C7C
004FC110  xor      eax, eax
004FC112  add      dx, dx
004FC115  comiss   xmm10, xmm4
004FC119  movss    xmm4, dword ptr [rip + 0x1906717]  ; -> 01E02838 [u32 0x00000000]
004FC121  movaps   xmm1, xmm8
004FC125  movss    xmm10, dword ptr [rip + 0x1b68b56]  ; -> 02064C84
004FC12E  seta     al
004FC131  shufps   xmm1, xmm8, 0x55
004FC136  add      dx, ax
004FC139  xor      eax, eax
004FC13B  add      dx, dx
004FC13E  comiss   xmm4, xmm3
004FC141  seta     al
004FC144  xor      r10d, r10d
004FC147  add      dx, ax
004FC14A  inc      r11w
004FC14E  shl      dx, 5
004FC152  comiss   xmm2, xmm8
004FC156  mov      word ptr [rip + 0x1b68c6a], r11w  ; -> 02064DC8
004FC15E  seta     r10b
004FC162  xor      eax, eax
004FC164  add      r10w, r10w
004FC168  comiss   xmm0, xmm1
004FC16B  movaps   xmm0, xmm8
004FC16F  shufps   xmm0, xmm8, 0xaa
004FC174  seta     al
004FC177  add      r10w, ax
004FC17B  xor      eax, eax
004FC17D  add      r10w, r10w
004FC181  comiss   xmm4, xmm0
004FC184  seta     al
004FC187  and      r9w, cx
004FC18B  add      r10w, ax
004FC18F  movzx    ecx, r8w
004FC193  shl      r10w, 5
004FC198  and      cx, dx
004FC19B  movzx    edi, word ptr [rip + 0x1b68c12]  ; -> 02064DB4
004FC1A2  xor      edx, edx
004FC1A4  comiss   xmm8, dword ptr [rip + 0x1b68984]  ; -> 02064B30
004FC1AC  mov      word ptr [rip + 0x1b68c2d], cx  ; -> 02064DE0
004FC1B3  movss    xmm4, dword ptr [rip + 0x1b68a05]  ; -> 02064BC0
004FC1BB  movss    xmm5, dword ptr [rip + 0x1b68a0d]  ; -> 02064BD0
004FC1C3  seta     dl
004FC1C6  xor      eax, eax
004FC1C8  add      dx, dx
004FC1CB  comiss   xmm1, dword ptr [rip + 0x1b68962]  ; -> 02064B34
004FC1D2  seta     al
004FC1D5  add      dx, ax
004FC1D8  xor      eax, eax
004FC1DA  add      dx, dx
004FC1DD  comiss   xmm0, dword ptr [rip + 0x1b68954]  ; -> 02064B38
004FC1E4  movaps   xmm0, xmmword ptr [rip + 0x419205]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004FC1EB  mulps    xmm13, xmm0
004FC1EF  seta     al
004FC1F2  add      dx, ax
004FC1F5  mulps    xmm14, xmm0
004FC1F9  shl      dx, 5
004FC1FD  and      dx, r8w
004FC201  movsx    eax, cx
004FC204  add      r9w, ax
004FC208  mulps    xmm8, xmm0
004FC20C  and      r8w, r10w
004FC210  movsx    eax, dx
004FC213  add      r9w, ax
004FC217  mov      word ptr [rip + 0x1b68bc9], r8w  ; -> 02064DE8
004FC21F  movsx    eax, r8w
004FC223  movzx    r8d, word ptr [rip + 0x1b68b99]  ; -> 02064DC4
004FC22B  cvttps2dq xmm6, xmm13
004FC230  mov      word ptr [rip + 0x1b68ba4], r9w  ; -> 02064DDC
004FC238  add      r9w, ax
004FC23C  mov      word ptr [rip + 0x1b68b88], r9w  ; -> 02064DCC
004FC244  mov      word ptr [rip + 0x1b68b99], dx  ; -> 02064DE4
004FC24B  cvttps2dq xmm14, xmm14
004FC250  cvttps2dq xmm7, xmm8
004FC255  movups   xmmword ptr [rip + 0x1b68904], xmm6  ; -> 02064B60
004FC25C  movups   xmmword ptr [rip + 0x1b6890c], xmm14  ; -> 02064B70
004FC264  movups   xmmword ptr [rip + 0x1b68915], xmm7  ; -> 02064B80
004FC26B  nop      dword ptr [rax + rax]
004FC270  movsx    r9d, bx
004FC274  lea      eax, [r9 + 0x44]
004FC278  shl      eax, 4
004FC27B  cmp      dword ptr [rip + 0x1b6887a], 0  ; -> 02064AFC
004FC282  movsxd   r10, eax
004FC285  movups   xmm0, xmmword ptr [r10 + r15]
004FC28A  movups   xmmword ptr [rip + 0x1b68a5f], xmm0  ; -> 02064CF0
004FC291  je       0x4fc33a  ; -> 004FC33A
004FC297  mov      eax, dword ptr [rip + 0x190658b]  ; -> 01E02828 [f32 1]
004FC29D  mov      ecx, eax
004FC29F  shr      ecx, 0x12
004FC2A2  xor      ecx, eax
004FC2A4  and      eax, 0x3fffff
004FC2A9  or       eax, 0x1fc00000
004FC2AE  shr      ecx, 4
004FC2B1  add      eax, eax
004FC2B3  and      ecx, 1
004FC2B6  or       ecx, eax
004FC2B8  mov      eax, ecx
004FC2BA  shr      eax, 0x12
004FC2BD  xor      eax, ecx
004FC2BF  and      ecx, 0x3fffff
004FC2C5  or       ecx, 0x1fc00000
004FC2CB  shr      eax, 4
004FC2CE  add      ecx, ecx
004FC2D0  and      eax, 1
004FC2D3  or       eax, ecx
004FC2D5  mov      ecx, eax
004FC2D7  shr      ecx, 0x12
004FC2DA  xor      ecx, eax
004FC2DC  and      eax, 0x3fffff
004FC2E1  or       eax, 0x1fc00000
004FC2E6  shr      ecx, 4
004FC2E9  add      eax, eax
004FC2EB  and      ecx, 1
004FC2EE  or       ecx, eax
004FC2F0  mov      edx, ecx
004FC2F2  shr      edx, 0x12
004FC2F5  xor      edx, ecx
004FC2F7  and      ecx, 0x3fffff
004FC2FD  shr      edx, 4
004FC300  or       ecx, 0x1fc00000
004FC306  and      edx, 1
004FC309  add      ecx, ecx
004FC30B  or       edx, ecx
004FC30D  mov      eax, edx
004FC30F  shr      eax, 0x12
004FC312  xor      eax, edx
004FC314  and      edx, 0x3fffff
004FC31A  or       edx, 0x1fc00000
004FC320  shr      eax, 4
004FC323  add      edx, edx
004FC325  and      eax, 1
004FC328  or       eax, edx
004FC32A  mov      dword ptr [rip + 0x19064f8], eax  ; -> 01E02828 [f32 1]
004FC330  movss    xmm3, dword ptr [rip + 0x19064f0]  ; -> 01E02828 [f32 1]
004FC338  jmp      0x4fc33e  ; -> 004FC33E
004FC33A  movaps   xmm3, xmm15
004FC33E  movups   xmm0, xmmword ptr [rip + 0x1b6884b]  ; -> 02064B90
004FC345  movsx    edx, di
004FC348  lea      eax, [r9 + 7]
004FC34C  movss    xmm2, dword ptr [rip + 0x1b689a4]  ; -> 02064CF8
004FC354  subss    xmm3, xmm15
004FC359  addss    xmm2, dword ptr [rip + 0x1b6899b]  ; -> 02064CFC
004FC361  addss    xmm4, dword ptr [rip + 0x1b6885b]  ; -> 02064BC4
004FC369  addss    xmm5, dword ptr [rip + 0x1b68863]  ; -> 02064BD4
004FC371  shl      eax, 4
004FC374  dec      r8w
004FC378  cdqe     
004FC37A  movss    dword ptr [rip + 0x1b6892e], xmm3  ; -> 02064CB0
004FC382  movss    dword ptr [rip + 0x1b6896e], xmm2  ; -> 02064CF8
004FC38A  movss    dword ptr [rip + 0x1b6882e], xmm4  ; -> 02064BC0
004FC392  mov      rax, qword ptr [rax + r15]
004FC396  mov      qword ptr [rip + 0x1b687a3], rax  ; -> 02064B40
004FC39D  lea      eax, [rdx + 2]
004FC3A0  movss    xmm1, dword ptr [rip + 0x1b6879c]  ; -> 02064B44
004FC3A8  shl      eax, 4
004FC3AB  movsxd   rcx, eax
004FC3AE  lea      eax, [rdx + 8]
004FC3B1  shl      eax, 4
004FC3B4  mulss    xmm1, xmm3
004FC3B8  mov      dword ptr [rip + 0x1b68742], 0x3f800000  ; -> 02064B04
004FC3C2  movups   xmmword ptr [rcx + r15], xmm6
004FC3C7  movsxd   rcx, eax
004FC3CA  lea      eax, [rdx + 0xe]
004FC3CD  shl      eax, 4
004FC3D0  movss    dword ptr [rip + 0x1b6876c], xmm1  ; -> 02064B44
004FC3D8  addss    xmm1, dword ptr [rip + 0x1b68760]  ; -> 02064B40
004FC3E0  movups   xmmword ptr [rcx + r15], xmm14
004FC3E5  movsxd   rcx, eax
004FC3E8  movsx    eax, r11w
004FC3EC  add      eax, 0xc8
004FC3F1  movss    dword ptr [rip + 0x1b687d7], xmm5  ; -> 02064BD0
004FC3F9  shl      eax, 4
004FC3FC  movups   xmmword ptr [rcx + r15], xmm7
004FC401  cdqe     
004FC403  mulss    xmm1, xmm2
004FC407  mov      word ptr [rip + 0x1b689b5], r8w  ; -> 02064DC4
004FC40F  movups   xmm3, xmmword ptr [rax + r15]
004FC414  mov      eax, edx
004FC416  movss    dword ptr [rip + 0x1b68722], xmm1  ; -> 02064B40
004FC41E  movups   xmm1, xmmword ptr [rip + 0x1b688cb]  ; -> 02064CF0
004FC425  shl      eax, 4
004FC428  movsxd   rcx, eax
004FC42B  lea      eax, [rdx + 6]
004FC42E  shl      eax, 4
004FC431  movups   xmmword ptr [rip + 0x1b68848], xmm3  ; -> 02064C80
004FC438  movups   xmmword ptr [rcx + r15], xmm0
004FC43D  movsxd   rcx, eax
004FC440  lea      eax, [rdx + 0xc]
004FC443  movups   xmm0, xmmword ptr [rip + 0x1b68756]  ; -> 02064BA0
004FC44A  shl      eax, 4
004FC44D  movss    dword ptr [rip + 0x1b6882b], xmm3  ; -> 02064C80
004FC455  movups   xmmword ptr [rcx + r15], xmm0
004FC45A  movsxd   rcx, eax
004FC45D  movups   xmm0, xmmword ptr [rip + 0x1b6874c]  ; -> 02064BB0
004FC464  movups   xmmword ptr [rcx + r15], xmm0
004FC469  movaps   xmm0, xmm3
004FC46C  shufps   xmm3, xmm3, 0x55
004FC470  subss    xmm0, xmm9
004FC475  movss    dword ptr [rip + 0x1b68807], xmm3  ; -> 02064C84
004FC47D  subss    xmm3, xmm10
004FC482  movups   xmmword ptr [r10 + r15], xmm1
004FC487  ucomiss  xmm0, xmm11
004FC48B  movss    dword ptr [rip + 0x1b687e1], xmm3  ; -> 02064C74
004FC493  movss    dword ptr [rip + 0x1b687d5], xmm0  ; -> 02064C70
004FC49B  jp       0x4fc49f  ; -> 004FC49F
004FC49D  je       0x4fc4a7  ; -> 004FC4A7
004FC49F  ucomiss  xmm3, xmm11
004FC4A3  jp       0x4fc4bc  ; -> 004FC4BC
004FC4A5  jne      0x4fc4bc  ; -> 004FC4BC
004FC4A7  call     0x22cc40  ; -> 0022CC40 fn
004FC4AC  movss    xmm3, dword ptr [rip + 0x1b687c0]  ; -> 02064C74
004FC4B4  movss    xmm0, dword ptr [rip + 0x1b687b4]  ; -> 02064C70
004FC4BC  comiss   xmm11, xmm0
004FC4C0  ja       0x4fc4c8  ; -> 004FC4C8
004FC4C2  comiss   xmm11, xmm3
004FC4C6  jbe      0x4fc4cd  ; -> 004FC4CD
004FC4C8  call     0x22cc30  ; -> 0022CC30 fn
004FC4CD  call     0x22cc20  ; -> 0022CC20 fn
004FC4D2  movss    xmm8, dword ptr [rip + 0x1b68799]  ; -> 02064C74
004FC4DB  movss    xmm9, dword ptr [rip + 0x1906350]  ; -> 01E02834 [u32 0x00000000]
004FC4E4  addss    xmm8, dword ptr [rip + 0x1906343]  ; -> 01E02830 [u32 0x00000000]
004FC4ED  subss    xmm9, dword ptr [rip + 0x1b6877a]  ; -> 02064C70
004FC4F6  movss    xmm6, dword ptr [rip + 0x190633e]  ; -> 01E0283C [f32 1]
004FC4FE  movsd    xmm10, qword ptr [rip + 0x17ef879]  ; -> 01CEBD80 [u64 0x7FFFFFFFFFFFFFFF]
004FC507  movaps   xmm1, xmm8
004FC50B  movaps   xmm0, xmm9
004FC50F  mulss    xmm1, xmm8
004FC514  mulss    xmm0, xmm9
004FC519  mulss    xmm1, xmm6
004FC51D  mulss    xmm0, xmm6
004FC521  addss    xmm0, xmm1
004FC525  cvtps2pd xmm0, xmm0
004FC528  andps    xmm0, xmm10
004FC52C  cvtpd2ps xmm0, xmm0
004FC530  call     0x861f14  ; -> 00861F14 fn
004FC535  movaps   xmm1, xmm0
004FC538  ucomiss  xmm1, xmm11
004FC53C  jp       0x4fc546  ; -> 004FC546
004FC53E  jne      0x4fc546  ; -> 004FC546
004FC540  movaps   xmm0, xmm12
004FC544  jmp      0x4fc54d  ; -> 004FC54D
004FC546  movaps   xmm0, xmm6
004FC549  divss    xmm0, xmm1
004FC54D  movss    xmm7, dword ptr [rip + 0x1b686fb]  ; -> 02064C50
004FC555  mulss    xmm8, xmm0
004FC55A  mulss    xmm9, xmm0
004FC55F  addss    xmm7, xmm8
004FC564  movss    dword ptr [rip + 0x1b68783], xmm8  ; -> 02064CF0
004FC56D  movss    xmm8, dword ptr [rip + 0x1b686de]  ; -> 02064C54
004FC576  addss    xmm8, xmm9
004FC57B  movss    dword ptr [rip + 0x1b68770], xmm9  ; -> 02064CF4
004FC584  movaps   xmm1, xmm7
004FC587  mulss    xmm1, xmm7
004FC58B  movaps   xmm0, xmm8
004FC58F  mulss    xmm0, xmm8
004FC594  mulss    xmm1, xmm6
004FC598  mulss    xmm0, xmm6
004FC59C  movss    dword ptr [rip + 0x1b68588], xmm1  ; -> 02064B2C
004FC5A4  addss    xmm0, xmm1
004FC5A8  cvtps2pd xmm0, xmm0
004FC5AB  andps    xmm0, xmm10
004FC5AF  cvtpd2ps xmm0, xmm0
004FC5B3  call     0x861f14  ; -> 00861F14 fn
004FC5B8  ucomiss  xmm0, xmm11
004FC5BC  jp       0x4fc5c6  ; -> 004FC5C6
004FC5BE  jne      0x4fc5c6  ; -> 004FC5C6
004FC5C0  movaps   xmm6, xmm12
004FC5C4  jmp      0x4fc5ca  ; -> 004FC5CA
004FC5C6  divss    xmm6, xmm0
004FC5CA  movsx    edx, word ptr [rip + 0x1b6853b]  ; -> 02064B0C
004FC5D1  mulss    xmm7, xmm6
004FC5D5  mov      dword ptr [rip + 0x1b68525], 0xbf800000  ; -> 02064B04
004FC5DF  mulss    xmm8, xmm6
004FC5E4  lea      eax, [rdx + 0x1d]
004FC5E7  movss    dword ptr [rip + 0x1b68511], xmm6  ; -> 02064B00
004FC5EF  mulss    xmm7, dword ptr [rip + 0x1b68549]  ; -> 02064B40
004FC5F7  shl      eax, 4
004FC5FA  mulss    xmm8, dword ptr [rip + 0x1b6853d]  ; -> 02064B40
004FC603  movsxd   rcx, eax
004FC606  lea      eax, [rdx + 0x1e]
004FC609  mulss    xmm7, dword ptr [rip + 0x17ef68b]  ; -> 01CEBC9C [f32 -1]
004FC611  shl      eax, 4
004FC614  movss    dword ptr [rip + 0x1b68637], xmm8  ; -> 02064C54
004FC61D  movups   xmm0, xmmword ptr [rcx + r15]
004FC622  movsxd   rcx, eax
004FC625  lea      eax, [rdx + 0x1f]
004FC628  shl      eax, 4
004FC62B  movups   xmmword ptr [rip + 0x1b6865e], xmm0  ; -> 02064C90
004FC632  movups   xmm0, xmmword ptr [rcx + r15]
004FC637  movsxd   rcx, eax
004FC63A  lea      eax, [rdx + 0x20]
004FC63D  shl      eax, 4
004FC640  movups   xmmword ptr [rip + 0x1b68659], xmm0  ; -> 02064CA0
004FC647  movups   xmm0, xmmword ptr [rcx + r15]
004FC64C  movsxd   rcx, eax
004FC64F  movsx    eax, word ptr [rip + 0x1b68772]  ; -> 02064DC8
004FC656  movups   xmmword ptr [rip + 0x1b68653], xmm0  ; -> 02064CB0
004FC65D  add      eax, 0x45
004FC660  movss    dword ptr [rip + 0x1b685e8], xmm7  ; -> 02064C50
004FC668  movups   xmm0, xmmword ptr [rcx + r15]
004FC66D  shl      eax, 4
004FC670  movsxd   rcx, eax
004FC673  movups   xmmword ptr [rip + 0x1b68646], xmm0  ; -> 02064CC0
004FC67A  movups   xmm0, xmmword ptr [rcx + r15]
004FC67F  movups   xmmword ptr [rip + 0x1b684da], xmm0  ; -> 02064B60
004FC686  movups   xmmword ptr [rip + 0x1b684f3], xmm0  ; -> 02064B80
004FC68D  movups   xmm2, xmm0
004FC690  movups   xmm3, xmm0
004FC693  movups   xmmword ptr [rip + 0x1b684d6], xmm0  ; -> 02064B70
004FC69A  movss    xmm0, dword ptr [rip + 0x1b684c2]  ; -> 02064B64
004FC6A2  subss    xmm3, xmm7
004FC6A6  addss    xmm0, xmm8
004FC6AB  addss    xmm2, xmm7
004FC6AF  ucomiss  xmm3, xmm11
004FC6B3  movss    dword ptr [rip + 0x1b684a9], xmm0  ; -> 02064B64
004FC6BB  movss    xmm0, dword ptr [rip + 0x1b684c1]  ; -> 02064B84
004FC6C3  subss    xmm0, xmm8
004FC6C8  movss    dword ptr [rip + 0x1b68490], xmm2  ; -> 02064B60
004FC6D0  movss    dword ptr [rip + 0x1b684a8], xmm3  ; -> 02064B80
004FC6D8  movss    dword ptr [rip + 0x1b684a4], xmm0  ; -> 02064B84
004FC6E0  jp       0x4fc6e4  ; -> 004FC6E4
004FC6E2  je       0x4fc6ec  ; -> 004FC6EC
004FC6E4  ucomiss  xmm0, xmm11
004FC6E8  jp       0x4fc701  ; -> 004FC701
004FC6EA  jne      0x4fc701  ; -> 004FC701
004FC6EC  call     0x22cc40  ; -> 0022CC40 fn
004FC6F1  movss    xmm0, dword ptr [rip + 0x1b6848b]  ; -> 02064B84
004FC6F9  movss    xmm3, dword ptr [rip + 0x1b6847f]  ; -> 02064B80
004FC701  comiss   xmm11, xmm3
004FC705  ja       0x4fc70d  ; -> 004FC70D
004FC707  comiss   xmm11, xmm0
004FC70B  jbe      0x4fc712  ; -> 004FC712
004FC70D  call     0x22cc30  ; -> 0022CC30 fn
004FC712  call     0x22cc20  ; -> 0022CC20 fn
004FC717  movss    xmm2, dword ptr [rip + 0x1b68445]  ; -> 02064B64
004FC71F  movups   xmm0, xmmword ptr [rip + 0x1b6856a]  ; -> 02064C90
004FC726  movss    xmm6, dword ptr [rip + 0x1b68432]  ; -> 02064B60
004FC72E  movss    xmm9, dword ptr [rip + 0x1b6856d]  ; -> 02064CA4
004FC737  movss    xmm8, dword ptr [rip + 0x1b68580]  ; -> 02064CC0
004FC740  movss    xmm13, dword ptr [rip + 0x1b6857b]  ; -> 02064CC4
004FC749  movss    xmm14, dword ptr [rip + 0x1b68576]  ; -> 02064CC8
004FC752  movss    xmm10, dword ptr [rip + 0x19060e1]  ; -> 01E0283C [f32 1]
004FC75B  shufps   xmm6, xmm6, 0
004FC75F  mulps    xmm6, xmm0
004FC762  movaps   xmm0, xmm2
004FC765  mulss    xmm0, dword ptr [rip + 0x1b68533]  ; -> 02064CA0
004FC76D  movss    dword ptr [rsp + 0x38], xmm9
004FC774  movups   xmmword ptr [rip + 0x1b683a5], xmm6  ; -> 02064B20
004FC77B  movss    xmm3, dword ptr [rip + 0x1b683a1]  ; -> 02064B24
004FC783  addss    xmm6, xmm0
004FC787  movss    xmm4, dword ptr [rip + 0x1b68399]  ; -> 02064B28
004FC78F  movaps   xmm0, xmm9
004FC793  movss    xmm5, dword ptr [rip + 0x1b68391]  ; -> 02064B2C
004FC79B  mulss    xmm0, xmm2
004FC79F  addss    xmm3, xmm0
004FC7A3  movss    xmm0, dword ptr [rip + 0x1b684fd]  ; -> 02064CA8
004FC7AB  movaps   xmm1, xmm0
004FC7AE  movss    dword ptr [rsp + 0x20], xmm0
004FC7B4  movss    xmm0, dword ptr [rip + 0x1b684f0]  ; -> 02064CAC
004FC7BC  movss    dword ptr [rsp + 0x2c], xmm0
004FC7C2  mulss    xmm0, xmm2
004FC7C6  mulss    xmm1, xmm2
004FC7CA  movss    xmm2, dword ptr [rip + 0x1b68396]  ; -> 02064B68
004FC7D2  addss    xmm5, xmm0
004FC7D6  movss    xmm0, dword ptr [rip + 0x1b684d6]  ; -> 02064CB4
004FC7DE  movss    dword ptr [rsp + 0x28], xmm0
004FC7E4  addss    xmm4, xmm1
004FC7E8  mulss    xmm0, xmm2
004FC7EC  movaps   xmm1, xmm2
004FC7EF  mulss    xmm1, dword ptr [rip + 0x1b684b9]  ; -> 02064CB0
004FC7F7  addss    xmm3, xmm0
004FC7FB  movaps   xmm0, xmm8
004FC7FF  addss    xmm6, xmm1
004FC803  movaps   xmm1, xmm2
004FC806  mulss    xmm1, dword ptr [rip + 0x1b684aa]  ; -> 02064CB8
004FC80E  mulss    xmm2, dword ptr [rip + 0x1b684a6]  ; -> 02064CBC
004FC816  addss    xmm4, xmm1
004FC81A  movaps   xmm1, xmm14
004FC81E  addss    xmm5, xmm2
004FC822  movss    xmm2, dword ptr [rip + 0x1b68342]  ; -> 02064B6C
004FC82A  mulss    xmm0, xmm2
004FC82E  mulss    xmm1, xmm2
004FC832  addss    xmm0, xmm6
004FC836  addss    xmm1, xmm4
004FC83A  movss    dword ptr [rip + 0x1b6831e], xmm0  ; -> 02064B60
004FC842  movaps   xmm0, xmm13
004FC846  mulss    xmm0, xmm2
004FC84A  movss    dword ptr [rip + 0x1b68316], xmm1  ; -> 02064B68
004FC852  addss    xmm0, xmm3
004FC856  movss    dword ptr [rip + 0x1b68306], xmm0  ; -> 02064B64
004FC85E  movss    xmm0, dword ptr [rip + 0x1b68466]  ; -> 02064CCC
004FC866  mulss    xmm0, xmm2
004FC86A  addss    xmm0, xmm5
004FC86E  ucomiss  xmm0, xmm11
004FC872  movss    dword ptr [rip + 0x1b682f2], xmm0  ; -> 02064B6C
004FC87A  jp       0x4fc884  ; -> 004FC884
004FC87C  jne      0x4fc884  ; -> 004FC884
004FC87E  movaps   xmm7, xmm12
004FC882  jmp      0x4fc88c  ; -> 004FC88C
004FC884  movaps   xmm7, xmm10
004FC888  divss    xmm7, xmm0
004FC88C  movss    xmm2, dword ptr [rip + 0x1b682e0]  ; -> 02064B74
004FC894  movss    xmm6, dword ptr [rip + 0x1b682d4]  ; -> 02064B70
004FC89C  movaps   xmm1, xmm2
004FC89F  mulss    xmm1, dword ptr [rsp + 0x20]
004FC8A5  movups   xmm0, xmmword ptr [rip + 0x1b683e4]  ; -> 02064C90
004FC8AC  shufps   xmm6, xmm6, 0
004FC8B0  mulps    xmm6, xmm0
004FC8B3  movaps   xmm0, xmm2
004FC8B6  mulss    xmm0, dword ptr [rip + 0x1b683e2]  ; -> 02064CA0
004FC8BE  movups   xmmword ptr [rip + 0x1b6825b], xmm6  ; -> 02064B20
004FC8C5  movss    xmm5, dword ptr [rip + 0x1b6825f]  ; -> 02064B2C
004FC8CD  addss    xmm6, xmm0
004FC8D1  movss    xmm3, dword ptr [rip + 0x1b6824b]  ; -> 02064B24
004FC8D9  movaps   xmm0, xmm2
004FC8DC  mulss    xmm2, dword ptr [rsp + 0x2c]
004FC8E2  movss    xmm4, dword ptr [rip + 0x1b6823e]  ; -> 02064B28
004FC8EA  mulss    xmm0, xmm9
004FC8EF  addss    xmm4, xmm1
004FC8F3  movups   xmm9, xmmword ptr [rip + 0x1b68265]  ; -> 02064B60
004FC8FB  addss    xmm5, xmm2
004FC8FF  movss    xmm2, dword ptr [rip + 0x1b68271]  ; -> 02064B78
004FC907  addss    xmm3, xmm0
004FC90B  movaps   xmm1, xmm2
004FC90E  mulss    xmm1, dword ptr [rsp + 0x28]
004FC914  movaps   xmm0, xmm2
004FC917  mulss    xmm0, dword ptr [rip + 0x1b68391]  ; -> 02064CB0
004FC91F  addss    xmm3, xmm1
004FC923  movaps   xmm1, xmm14
004FC927  addss    xmm6, xmm0
004FC92B  movaps   xmm0, xmm2
004FC92E  mulss    xmm0, dword ptr [rip + 0x1b68382]  ; -> 02064CB8
004FC936  mulss    xmm2, dword ptr [rip + 0x1b6837e]  ; -> 02064CBC
004FC93E  addss    xmm4, xmm0
004FC942  movaps   xmm0, xmm8
004FC946  addss    xmm5, xmm2
004FC94A  movss    xmm2, dword ptr [rip + 0x1b6822a]  ; -> 02064B7C
004FC952  mulss    xmm0, xmm2
004FC956  mulss    xmm1, xmm2
004FC95A  addss    xmm0, xmm6
004FC95E  addss    xmm1, xmm4
004FC962  movss    dword ptr [rip + 0x1b68206], xmm0  ; -> 02064B70
004FC96A  movaps   xmm0, xmm13
004FC96E  mulss    xmm0, xmm2
004FC972  mulss    xmm2, dword ptr [rip + 0x1b68352]  ; -> 02064CCC
004FC97A  addss    xmm0, xmm3
004FC97E  movss    dword ptr [rip + 0x1b681f2], xmm1  ; -> 02064B78
004FC986  addss    xmm2, xmm5
004FC98A  movss    dword ptr [rip + 0x1b681e2], xmm0  ; -> 02064B74
004FC992  movss    xmm0, dword ptr [rip + 0x1905e9a]  ; -> 01E02834 [u32 0x00000000]
004FC99A  ucomiss  xmm2, xmm11
004FC99E  addss    xmm0, dword ptr [rip + 0x1b6836a]  ; -> 02064D10
004FC9A6  movss    dword ptr [rip + 0x1b681ce], xmm2  ; -> 02064B7C
004FC9AE  movss    dword ptr [rip + 0x1b681de], xmm0  ; -> 02064B94
004FC9B6  movss    xmm0, dword ptr [rip + 0x1905e7a]  ; -> 01E02838 [u32 0x00000000]
004FC9BE  addss    xmm0, xmm10
004FC9C3  movss    dword ptr [rsp + 0x34], xmm0
004FC9C9  movss    dword ptr [rip + 0x1b681c7], xmm0  ; -> 02064B98
004FC9D1  movaps   xmm0, xmm7
004FC9D4  mulss    xmm7, xmm10
004FC9D9  shufps   xmm0, xmm0, 0
004FC9DD  mulps    xmm9, xmm0
004FC9E1  movss    dword ptr [rip + 0x1b681b3], xmm7  ; -> 02064B9C
004FC9E9  jp       0x4fc9f3  ; -> 004FC9F3
004FC9EB  jne      0x4fc9f3  ; -> 004FC9F3
004FC9ED  movaps   xmm6, xmm12
004FC9F1  jmp      0x4fc9fb  ; -> 004FC9FB
004FC9F3  movaps   xmm6, xmm10
004FC9F7  divss    xmm6, xmm2
004FC9FB  movss    xmm1, dword ptr [rip + 0x1b68181]  ; -> 02064B84
004FCA03  movss    xmm5, dword ptr [rip + 0x1b68175]  ; -> 02064B80
004FCA0B  movups   xmm0, xmmword ptr [rip + 0x1b6827e]  ; -> 02064C90
004FCA12  movss    xmm3, dword ptr [rsp + 0x38]
004FCA18  mulss    xmm3, xmm1
004FCA1C  shufps   xmm5, xmm5, 0
004FCA20  mulps    xmm5, xmm0
004FCA23  movaps   xmm0, xmm1
004FCA26  mulss    xmm0, dword ptr [rip + 0x1b68272]  ; -> 02064CA0
004FCA2E  movups   xmmword ptr [rip + 0x1b680eb], xmm5  ; -> 02064B20
004FCA35  movss    xmm4, dword ptr [rip + 0x1b680ef]  ; -> 02064B2C
004FCA3D  addss    xmm5, xmm0
004FCA41  movss    xmm0, dword ptr [rsp + 0x20]
004FCA47  movss    xmm2, dword ptr [rip + 0x1b680d5]  ; -> 02064B24
004FCA4F  mulss    xmm0, xmm1
004FCA53  addss    xmm2, xmm3
004FCA57  movss    xmm3, dword ptr [rip + 0x1b680c9]  ; -> 02064B28
004FCA5F  addss    xmm3, xmm0
004FCA63  movss    xmm0, dword ptr [rsp + 0x2c]
004FCA69  mulss    xmm0, xmm1
004FCA6D  movss    xmm1, dword ptr [rip + 0x1b68113]  ; -> 02064B88
004FCA75  addss    xmm4, xmm0
004FCA79  movaps   xmm0, xmm1
004FCA7C  mulss    xmm0, dword ptr [rip + 0x1b6822c]  ; -> 02064CB0
004FCA84  addss    xmm5, xmm0
004FCA88  movss    xmm0, dword ptr [rsp + 0x28]
004FCA8E  mulss    xmm0, xmm1
004FCA92  addss    xmm2, xmm0
004FCA96  movss    dword ptr [rip + 0x1b68082], xmm5  ; -> 02064B20
004FCA9E  movaps   xmm0, xmm1
004FCAA1  mulss    xmm1, dword ptr [rip + 0x1b68213]  ; -> 02064CBC
004FCAA9  mulss    xmm0, dword ptr [rip + 0x1b68207]  ; -> 02064CB8
004FCAB1  addss    xmm4, xmm1
004FCAB5  movss    dword ptr [rip + 0x1b68067], xmm2  ; -> 02064B24
004FCABD  movss    xmm1, dword ptr [rip + 0x1b680c7]  ; -> 02064B8C
004FCAC5  addss    xmm3, xmm0
004FCAC9  mulss    xmm13, xmm1
004FCACE  movss    xmm0, dword ptr [rip + 0x1b6823e]  ; -> 02064D14
004FCAD6  mulss    xmm8, xmm1
004FCADB  mulss    xmm14, xmm1
004FCAE0  addss    xmm13, xmm2
004FCAE5  mulss    xmm1, dword ptr [rip + 0x1b681df]  ; -> 02064CCC
004FCAED  addss    xmm8, xmm5
004FCAF2  addss    xmm14, xmm3
004FCAF7  movss    dword ptr [rip + 0x1b6802d], xmm4  ; -> 02064B2C
004FCAFF  movss    dword ptr [rip + 0x1b6807c], xmm13  ; -> 02064B84
004FCB08  movss    xmm13, dword ptr [rip + 0x1905d23]  ; -> 01E02834 [u32 0x00000000]
004FCB11  addss    xmm1, xmm4
004FCB15  movups   xmm4, xmmword ptr [rip + 0x1b68054]  ; -> 02064B70
004FCB1C  addss    xmm0, xmm13
004FCB21  movss    dword ptr [rip + 0x1b67fff], xmm3  ; -> 02064B28
004FCB29  movss    xmm3, dword ptr [rsp + 0x34]
004FCB2F  ucomiss  xmm1, xmm11
004FCB33  movss    dword ptr [rip + 0x1b68069], xmm0  ; -> 02064BA4
004FCB3B  movaps   xmm0, xmm6
004FCB3E  mulss    xmm6, xmm10
004FCB43  shufps   xmm0, xmm0, 0
004FCB47  movss    dword ptr [rip + 0x1b68030], xmm8  ; -> 02064B80
004FCB50  movss    dword ptr [rip + 0x1b68054], xmm6  ; -> 02064BAC
004FCB58  movss    dword ptr [rip + 0x1b68027], xmm14  ; -> 02064B88
004FCB61  movss    dword ptr [rip + 0x1b68023], xmm1  ; -> 02064B8C
004FCB69  movss    dword ptr [rip + 0x1b68037], xmm3  ; -> 02064BA8
004FCB71  mulps    xmm4, xmm0
004FCB74  jp       0x4fcb7e  ; -> 004FCB7E
004FCB76  jne      0x4fcb7e  ; -> 004FCB7E
004FCB78  movaps   xmm2, xmm12
004FCB7C  jmp      0x4fcb86  ; -> 004FCB86
004FCB7E  movaps   xmm2, xmm10
004FCB82  divss    xmm2, xmm1
004FCB86  movsx    edi, word ptr [rip + 0x1b68227]  ; -> 02064DB4
004FCB8D  xor      r10d, r10d
004FCB90  movzx    esi, word ptr [rip + 0x1b68221]  ; -> 02064DB8
004FCB97  movaps   xmm0, xmm13
004FCB9B  addss    xmm0, dword ptr [rip + 0x1b68175]  ; -> 02064D18
004FCBA3  movss    xmm5, dword ptr [rip + 0x1905c85]  ; -> 01E02830 [u32 0x00000000]
004FCBAB  add      si, 3
004FCBAF  mulps    xmm4, xmmword ptr [rip + 0x41883a]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004FCBB6  lea      eax, [rdi + 0xb]
004FCBB9  movzx    ebx, word ptr [rip + 0x1b67f4c]  ; -> 02064B0C
004FCBC0  mov      r11d, edi
004FCBC3  movups   xmm8, xmmword ptr [rip + 0x1b67fb5]  ; -> 02064B80
004FCBCB  shl      eax, 4
004FCBCE  movsxd   rcx, eax
004FCBD1  movaps   xmm1, xmm2
004FCBD4  movss    dword ptr [rip + 0x1b67fd8], xmm0  ; -> 02064BB4
004FCBDC  lea      eax, [rdi + 3]
004FCBDF  movups   xmm0, xmmword ptr [rip + 0x1b67faa]  ; -> 02064B90
004FCBE6  shl      eax, 4
004FCBE9  lea      r8d, [r12 + rbx]
004FCBED  shufps   xmm1, xmm1, 0
004FCBF1  mulps    xmm8, xmm1
004FCBF5  movaps   xmm1, xmm9
004FCBF9  mov      word ptr [rip + 0x1b681b8], si  ; -> 02064DB8
004FCC00  cvttps2dq xmm14, xmm4
004FCC05  movaps   xmm7, xmm8
004FCC09  movss    dword ptr [rip + 0x1b67eef], xmm2  ; -> 02064B00
004FCC11  movups   xmmword ptr [rcx + r15], xmm14
004FCC16  movsxd   rcx, eax
004FCC19  lea      eax, [rdi + 9]
004FCC1C  shl      eax, 4
004FCC1F  movaps   xmm6, xmm8
004FCC23  mulss    xmm2, xmm10
004FCC28  movss    xmm10, dword ptr [rip + 0x1905c07]  ; -> 01E02838 [u32 0x00000000]
004FCC31  movups   xmmword ptr [rcx + r15], xmm0
004FCC36  movsxd   rcx, eax
004FCC39  lea      eax, [rdi + 0xf]
004FCC3C  movups   xmm0, xmmword ptr [rip + 0x1b67f5d]  ; -> 02064BA0
004FCC43  shl      eax, 4
004FCC46  comiss   xmm5, xmm8
004FCC4A  movups   xmmword ptr [rcx + r15], xmm0
004FCC4F  movsxd   rcx, eax
004FCC52  seta     r10b
004FCC56  shufps   xmm7, xmm8, 0x55
004FCC5B  xor      eax, eax
004FCC5D  shufps   xmm6, xmm8, 0xaa
004FCC62  add      r10w, r10w
004FCC66  shufps   xmm1, xmm9, 0x55
004FCC6B  comiss   xmm13, xmm7
004FCC6F  movss    dword ptr [rip + 0x1b67f41], xmm3  ; -> 02064BB8
004FCC77  movss    dword ptr [rip + 0x1b67f3d], xmm2  ; -> 02064BBC
004FCC7F  movups   xmm0, xmmword ptr [rip + 0x1b67f2a]  ; -> 02064BB0
004FCC86  seta     al
004FCC89  add      r10w, ax
004FCC8D  xor      eax, eax
004FCC8F  add      r10w, r10w
004FCC93  comiss   xmm10, xmm6
004FCC97  movups   xmmword ptr [rcx + r15], xmm0
004FCC9C  seta     al
004FCC9F  movaps   xmm0, xmm9
004FCCA3  xor      r9d, r9d
004FCCA6  shufps   xmm0, xmm9, 0xaa
004FCCAB  add      r10w, ax
004FCCAF  shl      r10w, 5
004FCCB4  comiss   xmm9, dword ptr [rip + 0x1b67e74]  ; -> 02064B30
004FCCBC  movups   xmmword ptr [rip + 0x1b67eac], xmm14  ; -> 02064B70
004FCCC4  seta     r9b
004FCCC8  xor      eax, eax
004FCCCA  add      r9w, r9w
004FCCCE  comiss   xmm1, dword ptr [rip + 0x1b67e5f]  ; -> 02064B34
004FCCD5  seta     al
004FCCD8  add      r9w, ax
004FCCDC  xor      eax, eax
004FCCDE  add      r9w, r9w
004FCCE2  comiss   xmm0, dword ptr [rip + 0x1b67e4f]  ; -> 02064B38
004FCCE9  seta     al
004FCCEC  xor      edx, edx
004FCCEE  add      r9w, ax
004FCCF2  shl      r9w, 5
004FCCF7  and      r9w, r8w
004FCCFB  comiss   xmm5, xmm9
004FCCFF  seta     dl
004FCD02  mulps    xmm9, xmmword ptr [rip + 0x4186e6]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004FCD0A  xor      eax, eax
004FCD0C  add      dx, dx
004FCD0F  comiss   xmm13, xmm1
004FCD13  seta     al
004FCD16  add      dx, ax
004FCD19  xor      eax, eax
004FCD1B  add      dx, dx
004FCD1E  comiss   xmm10, xmm0
004FCD22  seta     al
004FCD25  xor      ecx, ecx
004FCD27  add      dx, ax
004FCD2A  shl      dx, 5
004FCD2E  and      dx, r8w
004FCD32  comiss   xmm8, dword ptr [rip + 0x1b67df6]  ; -> 02064B30
004FCD3A  mov      word ptr [rip + 0x1b6809f], dx  ; -> 02064DE0
004FCD41  movsx    edx, dx
004FCD44  mulps    xmm8, xmmword ptr [rip + 0x4186a4]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004FCD4C  seta     cl
004FCD4F  xor      eax, eax
004FCD51  add      cx, cx
004FCD54  comiss   xmm7, dword ptr [rip + 0x1b67dd9]  ; -> 02064B34
004FCD5B  cvttps2dq xmm7, xmm8
004FCD60  seta     al
004FCD63  add      cx, ax
004FCD66  xor      eax, eax
004FCD68  add      cx, cx
004FCD6B  comiss   xmm6, dword ptr [rip + 0x1b67dc6]  ; -> 02064B38
004FCD72  cvttps2dq xmm6, xmm9
004FCD77  seta     al
004FCD7A  add      cx, ax
004FCD7D  shl      cx, 5
004FCD81  and      cx, r8w
004FCD85  and      r8w, r10w
004FCD89  movsx    eax, cx
004FCD8C  mov      word ptr [rip + 0x1b68051], cx  ; -> 02064DE4
004FCD93  movsx    ecx, r8w
004FCD97  add      cx, ax
004FCD9A  mov      word ptr [rip + 0x1b68046], r8w  ; -> 02064DE8
004FCDA2  add      cx, dx
004FCDA5  lea      eax, [rdi + 0x11]
004FCDA8  movzx    edx, word ptr [rip + 0x1b6801d]  ; -> 02064DCC
004FCDAF  add      r9w, cx
004FCDB3  shl      eax, 4
004FCDB6  movsxd   rcx, eax
004FCDB9  lea      eax, [rdi + 5]
004FCDBC  shl      eax, 4
004FCDBF  add      di, 0x12
004FCDC3  movsx    r8d, di
004FCDC7  movsx    r10d, r9w
004FCDCB  movups   xmmword ptr [rcx + r15], xmm7
004FCDD0  movsxd   rcx, eax
004FCDD3  add      dx, r10w
004FCDD7  lea      eax, [r8 - 0x10]
004FCDDB  mov      word ptr [rip + 0x1b67ff9], r9w  ; -> 02064DDC
004FCDE3  movzx    r9d, word ptr [rip + 0x1b67fe9]  ; -> 02064DD4
004FCDEB  shl      eax, 4
004FCDEE  movups   xmmword ptr [rcx + r15], xmm6
004FCDF3  movsxd   rcx, eax
004FCDF6  lea      eax, [r8 - 0xd]
004FCDFA  shl      eax, 4
004FCDFD  mov      word ptr [rip + 0x1b67fb0], di  ; -> 02064DB4
004FCE04  movups   xmmword ptr [rip + 0x1b67d75], xmm7  ; -> 02064B80
004FCE0B  mov      dword ptr [rcx + r15 + 0xc], r9d
004FCE10  movsxd   rcx, eax
004FCE13  movups   xmmword ptr [rip + 0x1b67d46], xmm6  ; -> 02064B60
004FCE1A  mov      dword ptr [rcx + r15 + 0xc], r9d
004FCE1F  cmp      dx, bx
004FCE22  je       0x4fce61  ; -> 004FCE61
004FCE24  lea      eax, [r8 - 0xa]
004FCE28  shl      eax, 4
004FCE2B  movsxd   rcx, eax
004FCE2E  lea      eax, [r8 - 7]
004FCE32  shl      eax, 4
004FCE35  mov      dword ptr [rcx + r15 + 0xc], r9d
004FCE3A  movsxd   rcx, eax
004FCE3D  lea      eax, [r8 - 4]
004FCE41  shl      eax, 4
004FCE44  shl      r8d, 4
004FCE48  sub      r8d, 0x10
004FCE4C  mov      dword ptr [rcx + r15 + 0xc], r9d
004FCE51  movsxd   rcx, eax
004FCE54  movsxd   rax, r8d
004FCE57  mov      dword ptr [rcx + r15 + 0xc], r9d
004FCE5C  mov      dword ptr [rax + r15 + 0xc], r9d
004FCE61  add      r10w, bx
004FCE65  cmp      si, word ptr [rip + 0x1b67f6c]  ; -> 02064DD8
004FCE6C  mov      word ptr [rip + 0x1b67f58], r10w  ; -> 02064DCC
004FCE74  jne      0x4fcf3a  ; -> 004FCF3A
004FCE7A  movups   xmm0, xmmword ptr [rip + 0x1b67e8f]  ; -> 02064D10
004FCE81  movsx    eax, bx
004FCE84  mov      rdx, r14
004FCE87  add      eax, 0x43
004FCE8A  shl      eax, 4
004FCE8D  movsxd   rcx, eax
004FCE90  movups   xmmword ptr [rcx + r15], xmm0
004FCE95  mov      rcx, rbp
004FCE98  call     0x4f5360  ; -> 004F5360 fn
004FCE9D  movss    xmm4, dword ptr [rip + 0x1b67d1b]  ; -> 02064BC0
004FCEA5  movss    xmm5, dword ptr [rip + 0x1b67d23]  ; -> 02064BD0
004FCEAD  movaps   xmm0, xmm4
004FCEB0  addss    xmm0, dword ptr [rip + 0x1905980]  ; -> 01E02838 [u32 0x00000000]
004FCEB8  movsx    ebx, word ptr [rip + 0x1b67c4d]  ; -> 02064B0C
004FCEBF  movaps   xmm1, xmm4
004FCEC2  mulss    xmm1, dword ptr [rip + 0x1905972]  ; -> 01E0283C [f32 1]
004FCECA  movzx    edi, word ptr [rip + 0x1b67ee3]  ; -> 02064DB4
004FCED1  movups   xmm14, xmmword ptr [rip + 0x1b67c97]  ; -> 02064B70
004FCED9  movzx    esi, word ptr [rip + 0x1b67ed8]  ; -> 02064DB8
004FCEE0  lea      eax, [rbx + 0x43]
004FCEE3  movups   xmm7, xmmword ptr [rip + 0x1b67c96]  ; -> 02064B80
004FCEEA  shl      eax, 4
004FCEED  movups   xmm6, xmmword ptr [rip + 0x1b67c6c]  ; -> 02064B60
004FCEF4  cdqe     
004FCEF6  movss    dword ptr [rip + 0x1b67cca], xmm0  ; -> 02064BC8
004FCEFE  movaps   xmm0, xmm5
004FCF01  addss    xmm0, dword ptr [rip + 0x190592f]  ; -> 01E02838 [u32 0x00000000]
004FCF09  movss    dword ptr [rip + 0x1b67cbb], xmm1  ; -> 02064BCC
004FCF11  movaps   xmm1, xmm5
004FCF14  mulss    xmm1, dword ptr [rip + 0x1905920]  ; -> 01E0283C [f32 1]
004FCF1C  movss    dword ptr [rip + 0x1b67cb4], xmm0  ; -> 02064BD8
004FCF24  movups   xmm0, xmmword ptr [rax + r15]
004FCF29  movss    dword ptr [rip + 0x1b67cab], xmm1  ; -> 02064BDC
004FCF31  movups   xmmword ptr [rip + 0x1b67dd8], xmm0  ; -> 02064D10
004FCF38  jmp      0x4fcf4a  ; -> 004FCF4A
004FCF3A  movss    xmm4, dword ptr [rip + 0x1b67c7e]  ; -> 02064BC0
004FCF42  movss    xmm5, dword ptr [rip + 0x1b67c86]  ; -> 02064BD0
004FCF4A  movups   xmm0, xmmword ptr [rip + 0x1b67d9f]  ; -> 02064CF0
004FCF51  movzx    r11d, word ptr [rip + 0x1b67e6f]  ; -> 02064DC8
004FCF59  movzx    r8d, word ptr [rip + 0x1b67e63]  ; -> 02064DC4
004FCF61  inc      r11w
004FCF65  movss    xmm9, dword ptr [rip + 0x1b67d12]  ; -> 02064C80
004FCF6E  movss    xmm10, dword ptr [rip + 0x1b67d0d]  ; -> 02064C84
004FCF77  movss    xmm1, dword ptr [rip + 0x1b67d0d]  ; -> 02064C8C
004FCF7F  movss    dword ptr [rip + 0x1b67ce8], xmm9  ; -> 02064C70
004FCF88  movss    dword ptr [rip + 0x1b67ce3], xmm10  ; -> 02064C74
004FCF91  movss    dword ptr [rip + 0x1b67ce3], xmm1  ; -> 02064C7C
004FCF99  mov      word ptr [rip + 0x1b67e27], r11w  ; -> 02064DC8
004FCFA1  movups   xmmword ptr [rip + 0x1b67ca8], xmm0  ; -> 02064C50
004FCFA8  movss    xmm0, dword ptr [rip + 0x1b67cd8]  ; -> 02064C88
004FCFB0  movss    dword ptr [rip + 0x1b67cc0], xmm0  ; -> 02064C78
004FCFB8  cmp      r8w, bx
004FCFBC  jne      0x4fc270  ; -> 004FC270
004FCFC2  cmp      si, bx
004FCFC5  je       0x4fcfd9  ; -> 004FCFD9
004FCFC7  mov      rdx, r14
004FCFCA  mov      rcx, rbp
004FCFCD  call     0x4f5360  ; -> 004F5360 fn
004FCFD2  movzx    ebx, word ptr [rip + 0x1b67b33]  ; -> 02064B0C
004FCFD9  cmp      word ptr [rip + 0x1b67ddc], bx  ; -> 02064DBC
004FCFE0  je       0x4fcfef  ; -> 004FCFEF
004FCFE2  movss    xmm5, dword ptr [rip + 0x190583e]  ; -> 01E02828 [f32 1]
004FCFEA  jmp      0x4f7e52  ; -> 004F7E52
004FCFEF  mov      rcx, qword ptr [rsp + 0x150]
004FCFF7  xor      rcx, rsp
004FCFFA  call     0x808c40  ; -> 00808C40 fn
004FCFFF  lea      r11, [rsp + 0x200]
004FD007  mov      rbx, qword ptr [r11 + 0x40]
004FD00B  mov      rbp, qword ptr [r11 + 0x48]
004FD00F  movaps   xmm6, xmmword ptr [r11 - 0x10]
004FD014  movaps   xmm7, xmmword ptr [r11 - 0x20]
004FD019  movaps   xmm8, xmmword ptr [r11 - 0x30]
004FD01E  movaps   xmm9, xmmword ptr [r11 - 0x40]
004FD023  movaps   xmm10, xmmword ptr [r11 - 0x50]
004FD028  movaps   xmm11, xmmword ptr [r11 - 0x60]
004FD02D  movaps   xmm12, xmmword ptr [r11 - 0x70]
004FD032  movaps   xmm13, xmmword ptr [r11 - 0x80]
004FD037  movaps   xmm14, xmmword ptr [r11 - 0x90]
004FD03F  movaps   xmm15, xmmword ptr [r11 - 0xa0]
004FD047  mov      rsp, r11
004FD04A  pop      r15
```
