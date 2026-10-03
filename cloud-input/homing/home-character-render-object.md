# Homing pack: `17-Presentation-Rendering/Character-Rendering/character-render-object.md`

Generated 2026-10-03 09:39 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-character-render-object.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001E2250 (928 B, extent 001E2250-001E25F0)

Entered from (direct sites whose caller this page cites): `001E5370` + 0x81 (call; `001E5370` is cited on this page)
Other direct sites: none

Host context: "erior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*  | function | size | what the body does | interior anchors | |---|---|---|---| | '001E5370' | 182 B | computes 'n' = (qword '[rcx+8]' minus qword '[rcx]') / 0x18 (signed); when 'edx' is at most 'n' (unsigned, 32-bit) it calls '001E3D80(rcx, qword [rcx] + edx*0x18, qword [rcx+8])'; otherwise it calls '001E5370'+0x52 on a "

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
