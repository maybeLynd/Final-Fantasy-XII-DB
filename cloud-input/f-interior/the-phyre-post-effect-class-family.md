# F-interior pack: `22-Middleware-PhyreEngine/Post-Process-Chain/the-phyre-post-effect-class-family.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-phyre-post-effect-class-family.json`.

Functions: 9. Each is cited on the page only at its entry and is still in the F frontier.

## 0018FD70 (132 B, extent 0018FD70-0018FDF4)

Page context: "', and '00645DB0' stamps 'PFXAA''s vtable > '00D625D0'. So one 'PFXAA' exists wherever that context does. The game then runs its worker '0065A640' through the thunk > '0065A630', from '00191DA0' and '0018FD70'. ~~Following every vtable-stamping body's callers out of the family's code band > finds exactly three exits, and all three are this 'PFXAA' (its constructor and two destructor paths).~~ > *Corrected 2026-09-30 (OPUS, on SWE2-AUDIT"

```
0018FD70  mov      qword ptr [rsp + 8], rbx
0018FD75  mov      qword ptr [rsp + 0x10], rsi
0018FD7A  push     rdi
0018FD7B  sub      rsp, 0x50
0018FD7F  xor      ebx, ebx
0018FD81  mov      rsi, r9
0018FD84  mov      rdi, rcx
0018FD87  cmp      byte ptr [r8 + 8], bl
0018FD8B  jne      0x18fd92  ; -> 0018FD92
0018FD8D  mov      r9, qword ptr [r8]
0018FD90  jmp      0x18fd95  ; -> 0018FD95
0018FD92  mov      r9, rbx
0018FD95  mov      r8, qword ptr [rdi + 0x278]
0018FD9C  add      rcx, 0x378
0018FDA3  mov      byte ptr [rsp + 0x20], 1
0018FDA8  call     0x65a630  ; -> 0065A630 fn
0018FDAD  xor      eax, eax
0018FDAF  mov      qword ptr [rsp + 0x30], rbx
0018FDB4  mov      qword ptr [rsp + 0x38], rax
0018FDB9  mov      qword ptr [rsp + 0x40], rax
0018FDBE  mov      rax, qword ptr [rdi + 0x278]
0018FDC5  mov      dword ptr [rsp + 0x38], ebx
0018FDC9  cmp      byte ptr [rax + 8], bl
0018FDCC  jne      0x18fdd1  ; -> 0018FDD1
0018FDCE  mov      rbx, qword ptr [rax]
0018FDD1  xor      r9d, r9d
0018FDD4  lea      r8, [rsp + 0x30]
0018FDD9  mov      rdx, rsi
0018FDDC  mov      rcx, rbx
0018FDDF  call     0x1ee8e0  ; -> 001EE8E0 fn
0018FDE4  mov      rbx, qword ptr [rsp + 0x60]
0018FDE9  mov      rsi, qword ptr [rsp + 0x68]
0018FDEE  add      rsp, 0x50
0018FDF2  pop      rdi
0018FDF3  ret      
```

## 0063F850 (17 B, extent 0063F850-0063F861)

Page context: "hey are the same shape — identical in nine of their > first twelve slots — differing at exactly **three**: idx 3, idx 7 and **idx 10**. > > | idx | '00D5AEB0' | '00D5B0C0' | > |---:|---|---| > | 3 | '0063F850' | '00640330' | > | 7 | '00640220' | '006403B0' | > | **10** | **'00657140'** — the universal 3-byte 'xor al, al ; ret' stub | **'00640280'** — the installer, 69 B | > > **So on '00D5AEB0' this class has no default constructor and "

```
0063F850  lea      rdx, [rip + 0x6e48b9]  ; -> 00D24110
0063F857  mov      ecx, 2
0063F85C  jmp      0x5cdaa0  ; -> 005CDAA0 fn
```

## 00646770 (101 B, extent 00646770-006467D5)

Page context: "8CFD5' -> '00645DB0', the 'PFXAA' at 'context + 0x378'. The other two are exception-unwind funclets, not constructions: '008965EC', the context constructor's cleanup of that member (-> '0018D0D0' -> '00646770', the 'PFXAABase' destructor chain), and '0089E870', the cleanup funclet of 'PDeferredLightingBase''s installer '006458A0', whose unwind map is at '01DACB10' (-> '00646AB0', 'PPostEffectBase'). The conclusion is unchanged: the only"

```
00646770  push     rbx
00646772  sub      rsp, 0x30
00646776  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0064677F  mov      rbx, rcx
00646782  lea      rax, [rip + 0x71bda7]  ; -> 00D62530
00646789  mov      qword ptr [rcx], rax
0064678C  mov      rcx, qword ptr [rcx + 0x50]
00646790  call     0x6505a0  ; -> 006505A0 fn
00646795  nop      
00646796  lea      rax, [rip + 0x71b6b3]  ; -> 00D61E50
0064679D  mov      qword ptr [rbx], rax
006467A0  mov      ecx, dword ptr [rbx + 0x30]
006467A3  mov      eax, ecx
006467A5  shr      eax, 0x1f
006467A8  not      al
006467AA  test     al, 1
006467AC  je       0x6467c6  ; -> 006467C6
006467AE  btr      ecx, 0x1f
006467B2  cmp      ecx, 1
006467B5  jbe      0x6467c6  ; -> 006467C6
006467B7  mov      rcx, qword ptr [rbx + 0x38]
006467BB  test     rcx, rcx
006467BE  je       0x6467c6  ; -> 006467C6
006467C0  call     0x584730  ; -> 00584730 fn
006467C5  nop      
006467C6  xor      eax, eax
006467C8  mov      qword ptr [rbx + 0x38], rax
006467CC  mov      dword ptr [rbx + 0x30], eax
006467CF  add      rsp, 0x30
006467D3  pop      rbx
006467D4  ret      
```

## 00646AB0 (81 B, extent 00646AB0-00646B01)

Page context: "t member (-> '0018D0D0' -> '00646770', the 'PFXAABase' destructor chain), and '0089E870', the cleanup funclet of 'PDeferredLightingBase''s installer '006458A0', whose unwind map is at '01DACB10' (-> '00646AB0', 'PPostEffectBase'). The conclusion is unchanged: the only > construction by code is the one 'PFXAA'. *The other 35 > classes are reached only as this section says.* 'falsify_posteffect_family.py' P7, P8.  Each class's vtable is i"

```
00646AB0  push     rbx
00646AB2  sub      rsp, 0x30
00646AB6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00646ABF  mov      rbx, rcx
00646AC2  lea      rax, [rip + 0x71b387]  ; -> 00D61E50
00646AC9  mov      qword ptr [rcx], rax
00646ACC  mov      ecx, dword ptr [rcx + 0x30]
00646ACF  mov      eax, ecx
00646AD1  shr      eax, 0x1f
00646AD4  not      al
00646AD6  test     al, 1
00646AD8  je       0x646af2  ; -> 00646AF2
00646ADA  btr      ecx, 0x1f
00646ADE  cmp      ecx, 1
00646AE1  jbe      0x646af2  ; -> 00646AF2
00646AE3  mov      rcx, qword ptr [rbx + 0x38]
00646AE7  test     rcx, rcx
00646AEA  je       0x646af2  ; -> 00646AF2
00646AEC  call     0x584730  ; -> 00584730 fn
00646AF1  nop      
00646AF2  xor      eax, eax
00646AF4  mov      qword ptr [rbx + 0x38], rax
00646AF8  mov      dword ptr [rbx + 0x30], eax
00646AFB  add      rsp, 0x30
00646AFF  pop      rbx
00646B00  ret      
```

## 00657140 (3 B, extent 00657140-00657143)

Page context: "571C0' | **nobody** | *is this effect ready* — 'return this->+0x10 && *(this->+0x10) && this->+0x41', 27 bytes, shared by all 36 | | 5 | '00657150' | 'PDeferredLighting' and 'PLowResParticles' share '00657140'; 'PScreenSpaceReflection' has '006571A0' | **which render pass do I run in**, answered by name — see §3b | | 6 | '0065B8F0' | the 9 | **the render entry**: ensure configured, then run. See below | | 7 | '00653CD0' | **nobody** | '"

```
00657140  xor      al, al
00657142  ret      
```

## 00658470 (885 B, extent 00658470-006587E5)

Page context: "thods here.  Nine classes carry implementations, and it is the same nine everywhere:  | class | render slot 6 | its '0065xxxx' worker(s) | bytes | |---|---|---|---:| | 'PAtmospherics' | '0065B270' | '00658470' | 885 | | 'PCelShading' | '0065B340' | '006587F0' | 930 | | 'PDeferredLighting' | '0065B400' | '00659EC0' → '0065A960' | 1,889 + 2,307 | | 'PDepthOfField' | '0065B4C0' | '00658BA0' | 1,241 | | 'PFXAA' | '0065B590' | '0065A640' | 7"

```
00658470  mov      rax, rsp
00658473  push     rbp
00658474  push     r14
00658476  push     r15
00658478  mov      rbp, rsp
0065847B  sub      rsp, 0x70
0065847F  mov      qword ptr [rbp - 0x40], 0xfffffffffffffffe
00658487  mov      qword ptr [rax + 8], rbx
0065848B  mov      qword ptr [rax + 0x10], rsi
0065848F  mov      qword ptr [rax + 0x18], rdi
00658493  mov      qword ptr [rax + 0x20], r12
00658497  mov      r14, r9
0065849A  mov      rdi, r8
0065849D  mov      rsi, rdx
006584A0  mov      rbx, rcx
006584A3  movss    xmm0, dword ptr [rcx + 0x84]
006584AB  ucomiss  xmm0, dword ptr [rcx + 0xf4]
006584B2  jp       0x6584b6  ; -> 006584B6
006584B4  je       0x6584ba  ; -> 006584BA
006584B6  mov      byte ptr [rcx + 0x62], 1
006584BA  movss    xmm0, dword ptr [rcx + 0x88]
006584C2  ucomiss  xmm0, dword ptr [rcx + 0xf8]
006584C9  jp       0x6584cd  ; -> 006584CD
006584CB  je       0x6584d1  ; -> 006584D1
006584CD  mov      byte ptr [rcx + 0x62], 1
006584D1  movss    xmm0, dword ptr [rcx + 0x90]
006584D9  ucomiss  xmm0, dword ptr [rcx + 0x100]
006584E0  jp       0x65850a  ; -> 0065850A
006584E2  jne      0x65850a  ; -> 0065850A
006584E4  movss    xmm0, dword ptr [rcx + 0x94]
006584EC  ucomiss  xmm0, dword ptr [rcx + 0x104]
006584F3  jp       0x65850a  ; -> 0065850A
006584F5  jne      0x65850a  ; -> 0065850A
006584F7  movss    xmm0, dword ptr [rcx + 0x98]
006584FF  ucomiss  xmm0, dword ptr [rcx + 0x108]
00658506  jp       0x65850a  ; -> 0065850A
00658508  je       0x65850e  ; -> 0065850E
0065850A  mov      byte ptr [rcx + 0x62], 1
0065850E  movss    xmm0, dword ptr [rcx + 0xa0]
00658516  ucomiss  xmm0, dword ptr [rcx + 0x110]
0065851D  jp       0x658547  ; -> 00658547
0065851F  jne      0x658547  ; -> 00658547
00658521  movss    xmm0, dword ptr [rcx + 0xa4]
00658529  ucomiss  xmm0, dword ptr [rcx + 0x114]
00658530  jp       0x658547  ; -> 00658547
00658532  jne      0x658547  ; -> 00658547
00658534  movss    xmm0, dword ptr [rcx + 0xa8]
0065853C  ucomiss  xmm0, dword ptr [rcx + 0x118]
00658543  jp       0x658547  ; -> 00658547
00658545  je       0x65854b  ; -> 0065854B
00658547  mov      byte ptr [rcx + 0x62], 1
0065854B  movss    xmm0, dword ptr [rcx + 0xc0]
00658553  ucomiss  xmm0, dword ptr [rcx + 0x120]
0065855A  jp       0x65855e  ; -> 0065855E
0065855C  je       0x658562  ; -> 00658562
0065855E  mov      byte ptr [rcx + 0x62], 1
00658562  movss    xmm0, dword ptr [rcx + 0xc4]
0065856A  ucomiss  xmm0, dword ptr [rcx + 0x124]
00658571  jp       0x658575  ; -> 00658575
00658573  je       0x658579  ; -> 00658579
00658575  mov      byte ptr [rcx + 0x62], 1
00658579  cmp      byte ptr [rcx + 0x60], 0
0065857D  je       0x6585bb  ; -> 006585BB
0065857F  cmp      byte ptr [rcx + 0x62], 0
00658583  je       0x6585bb  ; -> 006585BB
00658585  lea      rdx, [rip + 0x70aeac]  ; -> 00D63438
0065858C  xor      ecx, ecx
0065858E  call     0x5cdaa0  ; -> 005CDAA0 fn
00658593  mov      rdx, rsi
00658596  mov      rcx, rbx
00658599  call     0x65c080  ; -> 0065C080 fn
0065859E  mov      rdx, rsi
006585A1  mov      rcx, rbx
006585A4  call     0x657870  ; -> 00657870 fn
006585A9  lea      rdx, [rip + 0x70aea0]  ; -> 00D63450
006585B0  xor      ecx, ecx
006585B2  call     0x5cdaa0  ; -> 005CDAA0 fn
006585B7  mov      byte ptr [rbx + 0x62], 0
006585BB  mov      rcx, rbx
006585BE  call     0x65cd60  ; -> 0065CD60 fn
006585C3  test     eax, eax
006585C5  jne      0x6587c7  ; -> 006587C7
006585CB  mov      rdx, qword ptr [rbx + 0x198]
006585D2  xor      r15d, r15d
006585D5  lea      r12, [rip + 0x26dcb64]  ; -> 02D35140
006585DC  test     rdx, rdx
006585DF  je       0x658611  ; -> 00658611
006585E1  mov      qword ptr [rbp - 0x38], 0x42
006585E9  mov      rax, qword ptr [rbx + 0x128]
006585F0  mov      qword ptr [rbp - 0x28], rax
006585F4  mov      qword ptr [rbp - 0x30], r12
006585F8  mov      rax, qword ptr [rbx + 0x58]
006585FC  lea      r8, [rbp - 0x38]
00658600  mov      rcx, qword ptr [rax + 8]
00658604  call     0x1b81b0  ; -> 001B81B0 fn
00658609  test     eax, eax
0065860B  jne      0x6587c7  ; -> 006587C7
00658611  mov      rdx, qword ptr [rbx + 0x1a0]
00658618  test     rdx, rdx
0065861B  je       0x65864d  ; -> 0065864D
0065861D  mov      qword ptr [rbp - 0x38], 0x42
00658625  mov      rax, qword ptr [rbx + 0x130]
0065862C  mov      qword ptr [rbp - 0x28], rax
00658630  mov      qword ptr [rbp - 0x30], r12
00658634  mov      rax, qword ptr [rbx + 0x58]
00658638  lea      r8, [rbp - 0x38]
0065863C  mov      rcx, qword ptr [rax + 8]
00658640  call     0x1b81b0  ; -> 001B81B0 fn
00658645  test     eax, eax
00658647  jne      0x6587c7  ; -> 006587C7
0065864D  mov      rdx, qword ptr [rbx + 0x1a8]
00658654  test     rdx, rdx
00658657  je       0x658689  ; -> 00658689
00658659  mov      qword ptr [rbp - 0x38], 0x43
00658661  mov      rax, qword ptr [rbx + 0x138]
00658668  mov      qword ptr [rbp - 0x28], rax
0065866C  mov      qword ptr [rbp - 0x30], r12
00658670  mov      rax, qword ptr [rbx + 0x58]
00658674  lea      r8, [rbp - 0x38]
00658678  mov      rcx, qword ptr [rax + 8]
0065867C  call     0x65cc90  ; -> 0065CC90 fn
00658681  test     eax, eax
00658683  jne      0x6587c7  ; -> 006587C7
00658689  mov      rdx, qword ptr [rbx + 0x170]
00658690  test     rdx, rdx
00658693  je       0x6586be  ; -> 006586BE
00658695  mov      qword ptr [rbp - 0x38], 0x42
0065869D  mov      qword ptr [rbp - 0x28], r14
006586A1  mov      qword ptr [rbp - 0x30], r12
006586A5  mov      rax, qword ptr [rbx + 0x58]
006586A9  lea      r8, [rbp - 0x38]
006586AD  mov      rcx, qword ptr [rax + 8]
006586B1  call     0x1b81b0  ; -> 001B81B0 fn
006586B6  test     eax, eax
006586B8  jne      0x6587c7  ; -> 006587C7
006586BE  mov      rdx, qword ptr [rbx + 0x178]
006586C5  test     rdx, rdx
006586C8  je       0x6586f7  ; -> 006586F7
006586CA  mov      qword ptr [rbp - 0x38], 0x42
006586D2  mov      rax, qword ptr [rbp + 0x40]
006586D6  mov      qword ptr [rbp - 0x28], rax
006586DA  mov      qword ptr [rbp - 0x30], r12
006586DE  mov      rax, qword ptr [rbx + 0x58]
006586E2  lea      r8, [rbp - 0x38]
006586E6  mov      rcx, qword ptr [rax + 8]
006586EA  call     0x1b81b0  ; -> 001B81B0 fn
006586EF  test     eax, eax
006586F1  jne      0x6587c7  ; -> 006587C7
006586F7  xor      r8d, r8d
006586FA  mov      rdx, rdi
006586FD  lea      rcx, [rbp - 0x20]
00658701  call     0x5dc190  ; -> 005DC190 fn
00658706  nop      
00658707  cmp      byte ptr [rbx + 0x61], 0
0065870B  je       0x658716  ; -> 00658716
0065870D  lea      rax, [rip + 0x26de8ac]  ; -> 02D36FC0
00658714  jmp      0x658732  ; -> 00658732
00658716  test     rdi, rdi
00658719  je       0x65872b  ; -> 0065872B
0065871B  mov      eax, dword ptr [rdi + 0xc]
0065871E  shr      eax, 1
00658720  test     al, 1
00658722  lea      rax, [rip + 0x26df897]  ; -> 02D37FC0
00658729  jne      0x658732  ; -> 00658732
0065872B  lea      rax, [rip + 0x26de86e]  ; -> 02D36FA0
00658732  mov      qword ptr [rsi + 0x80], rax
00658739  xor      r8d, r8d
0065873C  lea      rdx, [rbp - 0x20]
00658740  mov      rcx, rsi
00658743  call     0x60d4f0  ; -> 0060D4F0 fn
00658748  mov      edi, eax
0065874A  test     eax, eax
0065874C  jne      0x6587bc  ; -> 006587BC
0065874E  xor      edx, edx
00658750  mov      rcx, rsi
00658753  call     0x60db50  ; -> 0060DB50 fn
00658758  mov      edi, eax
0065875A  test     eax, eax
0065875C  jne      0x6587bc  ; -> 006587BC
0065875E  xor      edx, edx
00658760  mov      rcx, rsi
00658763  call     0x5fefd0  ; -> 005FEFD0 fn
00658768  mov      edi, eax
0065876A  test     eax, eax
0065876C  jne      0x6587bc  ; -> 006587BC
0065876E  mov      rdx, qword ptr [rbx + 0x50]
00658772  mov      rax, qword ptr [rdx + 0x20]
00658776  lea      rcx, [rip + 0x26e51b]  ; -> 008C6C98
0065877D  mov      qword ptr [rbp - 0x38], rcx
00658781  mov      qword ptr [rbp - 0x30], rax
00658785  mov      byte ptr [rsp + 0x28], dil
0065878A  mov      eax, dword ptr [rsi + 0x220]
00658790  mov      dword ptr [rsp + 0x20], eax
00658794  xor      r9d, r9d
00658797  lea      r8, [rbp - 0x38]
0065879B  mov      rcx, rsi
0065879E  call     0x60b980  ; -> 0060B980 fn
006587A3  mov      edi, eax
006587A5  test     eax, eax
006587A7  jne      0x6587bc  ; -> 006587BC
006587A9  xor      edx, edx
006587AB  mov      rcx, rsi
006587AE  call     0x600a60  ; -> 00600A60 fn
006587B3  mov      edi, eax
006587B5  test     eax, eax
006587B7  jne      0x6587bc  ; -> 006587BC
006587B9  mov      edi, r15d
006587BC  lea      rcx, [rbp - 0x20]
006587C0  call     0x16d6a0  ; -> 0016D6A0 fn
006587C5  mov      eax, edi
006587C7  lea      r11, [rsp + 0x70]
006587CC  mov      rbx, qword ptr [r11 + 0x20]
006587D0  mov      rsi, qword ptr [r11 + 0x28]
006587D4  mov      rdi, qword ptr [r11 + 0x30]
006587D8  mov      r12, qword ptr [r11 + 0x38]
006587DC  mov      rsp, r11
006587DF  pop      r15
006587E1  pop      r14
006587E3  pop      rbp
006587E4  ret      
```

## 006587F0 (930 B, extent 006587F0-00658B92)

Page context: "nd it is the same nine everywhere:  | class | render slot 6 | its '0065xxxx' worker(s) | bytes | |---|---|---|---:| | 'PAtmospherics' | '0065B270' | '00658470' | 885 | | 'PCelShading' | '0065B340' | '006587F0' | 930 | | 'PDeferredLighting' | '0065B400' | '00659EC0' → '0065A960' | 1,889 + 2,307 | | 'PDepthOfField' | '0065B4C0' | '00658BA0' | 1,241 | | 'PFXAA' | '0065B590' | '0065A640' | 790 | | 'PGlow' | '0065B650' | '00652940' and '0065"

```
006587F0  mov      rax, rsp
006587F3  push     rdi
006587F4  push     r14
006587F6  push     r15
006587F8  sub      rsp, 0x70
006587FC  mov      qword ptr [rax - 0x58], 0xfffffffffffffffe
00658804  mov      qword ptr [rax + 8], rbx
00658808  mov      qword ptr [rax + 0x10], rbp
0065880C  mov      qword ptr [rax + 0x18], rsi
00658810  mov      rbp, r9
00658813  mov      rdi, r8
00658816  mov      rsi, rdx
00658819  mov      rbx, rcx
0065881C  mov      r14, qword ptr [rdx + 0xa8]
00658823  mov      rcx, qword ptr [rcx + 0x88]
0065882A  mov      r15d, 0x1fff
00658830  test     rcx, rcx
00658833  je       0x65888c  ; -> 0065888C
00658835  mov      rax, qword ptr [rbx + 0x50]
00658839  mov      r11, qword ptr [rax + 8]
0065883D  lea      r10, [rbx + 0x58]
00658841  test     r10, r10
00658844  jne      0x658850  ; -> 00658850
00658846  mov      eax, 1
0065884B  jmp      0x658b78  ; -> 00658B78
00658850  movzx    r9d, word ptr [rcx + 0x10]
00658855  movzx    edx, word ptr [rcx + 0x12]
00658859  and      dx, r15w
0065885D  movzx    ecx, dx
00658860  add      ecx, r9d
00658863  cmp      ecx, dword ptr [r11]
00658866  ja       0x65886f  ; -> 0065886F
00658868  cmp      r9w, 4
0065886D  jae      0x658879  ; -> 00658879
0065886F  mov      eax, 3
00658874  jmp      0x658b78  ; -> 00658B78
00658879  movzx    r8d, dx
0065887D  movzx    ecx, r9w
00658881  add      rcx, r11
00658884  mov      rdx, r10
00658887  call     0x861eba  ; -> 00861EBA fn
0065888C  mov      rcx, qword ptr [rbx + 0x90]
00658893  test     rcx, rcx
00658896  je       0x6588db  ; -> 006588DB
00658898  mov      rax, qword ptr [rbx + 0x50]
0065889C  mov      r11, qword ptr [rax + 8]
006588A0  lea      r10, [rbx + 0x5c]
006588A4  test     r10, r10
006588A7  je       0x658846  ; -> 00658846
006588A9  movzx    r9d, word ptr [rcx + 0x10]
006588AE  movzx    edx, word ptr [rcx + 0x12]
006588B2  and      dx, r15w
006588B6  movzx    ecx, dx
006588B9  add      ecx, r9d
006588BC  cmp      ecx, dword ptr [r11]
006588BF  ja       0x65886f  ; -> 0065886F
006588C1  cmp      r9w, 4
006588C6  jb       0x65886f  ; -> 0065886F
006588C8  movzx    r8d, dx
006588CC  movzx    ecx, r9w
006588D0  add      rcx, r11
006588D3  mov      rdx, r10
006588D6  call     0x861eba  ; -> 00861EBA fn
006588DB  mov      rcx, qword ptr [rbx + 0xa0]
006588E2  test     rcx, rcx
006588E5  je       0x658936  ; -> 00658936
006588E7  mov      rax, qword ptr [rbx + 0x50]
006588EB  mov      r11, qword ptr [rax + 8]
006588EF  lea      r10, [rbx + 0x64]
006588F3  test     r10, r10
006588F6  je       0x658846  ; -> 00658846
006588FC  movzx    r9d, word ptr [rcx + 0x10]
00658901  movzx    edx, word ptr [rcx + 0x12]
00658905  and      dx, r15w
00658909  movzx    ecx, dx
0065890C  add      ecx, r9d
0065890F  cmp      ecx, dword ptr [r11]
00658912  ja       0x65886f  ; -> 0065886F
00658918  cmp      r9w, 4
0065891D  jb       0x65886f  ; -> 0065886F
00658923  movzx    r8d, dx
00658927  movzx    ecx, r9w
0065892B  add      rcx, r11
0065892E  mov      rdx, r10
00658931  call     0x861eba  ; -> 00861EBA fn
00658936  mov      rcx, qword ptr [rbx + 0x98]
0065893D  test     rcx, rcx
00658940  je       0x658991  ; -> 00658991
00658942  mov      rax, qword ptr [rbx + 0x50]
00658946  mov      r11, qword ptr [rax + 8]
0065894A  lea      r10, [rbx + 0x60]
0065894E  test     r10, r10
00658951  je       0x658846  ; -> 00658846
00658957  movzx    r9d, word ptr [rcx + 0x10]
0065895C  movzx    edx, word ptr [rcx + 0x12]
00658960  and      dx, r15w
00658964  movzx    ecx, dx
00658967  add      ecx, r9d
0065896A  cmp      ecx, dword ptr [r11]
0065896D  ja       0x65886f  ; -> 0065886F
00658973  cmp      r9w, 4
00658978  jb       0x65886f  ; -> 0065886F
0065897E  movzx    r8d, dx
00658982  movzx    ecx, r9w
00658986  add      rcx, r11
00658989  mov      rdx, r10
0065898C  call     0x861eba  ; -> 00861EBA fn
00658991  mov      rcx, qword ptr [rbx + 0xa8]
00658998  test     rcx, rcx
0065899B  je       0x6589ec  ; -> 006589EC
0065899D  mov      rax, qword ptr [rbx + 0x50]
006589A1  mov      r11, qword ptr [rax + 8]
006589A5  lea      r10, [rbx + 0x74]
006589A9  test     r10, r10
006589AC  je       0x658846  ; -> 00658846
006589B2  movzx    r9d, word ptr [rcx + 0x10]
006589B7  movzx    edx, word ptr [rcx + 0x12]
006589BB  and      dx, r15w
006589BF  movzx    ecx, dx
006589C2  add      ecx, r9d
006589C5  cmp      ecx, dword ptr [r11]
006589C8  ja       0x65886f  ; -> 0065886F
006589CE  cmp      r9w, 4
006589D3  jb       0x65886f  ; -> 0065886F
006589D9  movzx    r8d, dx
006589DD  movzx    ecx, r9w
006589E1  add      rcx, r11
006589E4  mov      rdx, r10
006589E7  call     0x861eba  ; -> 00861EBA fn
006589EC  mov      rcx, qword ptr [rbx + 0xb0]
006589F3  test     rcx, rcx
006589F6  je       0x658a69  ; -> 00658A69
006589F8  movups   xmm0, xmmword ptr [r14 + 0x30]
006589FD  movss    xmm3, dword ptr [rip + 0x16931a3]  ; -> 01CEBBA8 [f32 1]
00658A05  movaps   xmm1, xmm3
00658A08  divss    xmm1, xmm0
00658A0C  movss    dword ptr [rsp + 0x38], xmm1
00658A12  divss    xmm3, dword ptr [r14 + 0x44]
00658A18  movss    dword ptr [rsp + 0x3c], xmm3
00658A1E  mov      qword ptr [rsp + 0x40], 0
00658A27  mov      rax, qword ptr [rbx + 0x50]
00658A2B  mov      r9, qword ptr [rax + 8]
00658A2F  movzx    edx, word ptr [rcx + 0x10]
00658A33  movzx    r8d, word ptr [rcx + 0x12]
00658A38  and      r8w, r15w
00658A3C  movzx    ecx, r8w
00658A40  add      ecx, edx
00658A42  cmp      ecx, dword ptr [r9]
00658A45  ja       0x65886f  ; -> 0065886F
00658A4B  cmp      dx, 4
00658A4F  jb       0x65886f  ; -> 0065886F
00658A55  movzx    r8d, r8w
00658A59  movzx    ecx, dx
00658A5C  add      rcx, r9
00658A5F  lea      rdx, [rsp + 0x38]
00658A64  call     0x861eba  ; -> 00861EBA fn
00658A69  mov      rdx, qword ptr [rbx + 0xb8]
00658A70  test     rdx, rdx
00658A73  je       0x658aa9  ; -> 00658AA9
00658A75  mov      qword ptr [rsp + 0x38], 0x42
00658A7E  mov      qword ptr [rsp + 0x48], rbp
00658A83  lea      rax, [rip + 0x26dbc8e]  ; -> 02D34718
00658A8A  mov      qword ptr [rsp + 0x40], rax
00658A8F  mov      rax, qword ptr [rbx + 0x50]
00658A93  lea      r8, [rsp + 0x38]
00658A98  mov      rcx, qword ptr [rax + 8]
00658A9C  call     0x1b81b0  ; -> 001B81B0 fn
00658AA1  test     eax, eax
00658AA3  jne      0x658b78  ; -> 00658B78
00658AA9  xor      r8d, r8d
00658AAC  mov      rdx, rdi
00658AAF  lea      rcx, [rsp + 0x50]
00658AB4  call     0x5dc190  ; -> 005DC190 fn
00658AB9  nop      
00658ABA  test     rdi, rdi
00658ABD  je       0x658acc  ; -> 00658ACC
00658ABF  mov      eax, dword ptr [rdi + 0xc]
00658AC2  shr      eax, 1
00658AC4  test     al, 1
00658AC6  je       0x658acc  ; -> 00658ACC
00658AC8  mov      cl, 1
00658ACA  jmp      0x658ace  ; -> 00658ACE
00658ACC  xor      cl, cl
00658ACE  lea      rdx, [rip + 0x26def8b]  ; -> 02D37A60
00658AD5  lea      rax, [rip + 0x26de344]  ; -> 02D36E20
00658ADC  test     cl, cl
00658ADE  cmovne   rax, rdx
00658AE2  mov      qword ptr [rsi + 0x80], rax
00658AE9  xor      r8d, r8d
00658AEC  lea      rdx, [rsp + 0x50]
00658AF1  mov      rcx, rsi
00658AF4  call     0x60d4f0  ; -> 0060D4F0 fn
00658AF9  mov      edi, eax
00658AFB  test     eax, eax
00658AFD  jne      0x658b6c  ; -> 00658B6C
00658AFF  xor      edx, edx
00658B01  mov      rcx, rsi
00658B04  call     0x60db50  ; -> 0060DB50 fn
00658B09  mov      edi, eax
00658B0B  test     eax, eax
00658B0D  jne      0x658b6c  ; -> 00658B6C
00658B0F  xor      edx, edx
00658B11  mov      rcx, rsi
00658B14  call     0x5fefd0  ; -> 005FEFD0 fn
00658B19  mov      edi, eax
00658B1B  test     eax, eax
00658B1D  jne      0x658b6c  ; -> 00658B6C
00658B1F  lea      rax, [rip + 0x26e172]  ; -> 008C6C98
00658B26  mov      qword ptr [rsp + 0x38], rax
00658B2B  lea      rax, [rbx + 0x30]
00658B2F  mov      qword ptr [rsp + 0x40], rax
00658B34  mov      byte ptr [rsp + 0x28], dil
00658B39  mov      eax, dword ptr [rsi + 0x220]
00658B3F  mov      dword ptr [rsp + 0x20], eax
00658B43  xor      r9d, r9d
00658B46  lea      r8, [rsp + 0x38]
00658B4B  mov      rdx, qword ptr [rip + 0x26dbbbe]  ; -> 02D34710
00658B52  mov      rcx, rsi
00658B55  call     0x60b980  ; -> 0060B980 fn
00658B5A  mov      edi, eax
00658B5C  test     eax, eax
00658B5E  jne      0x658b6c  ; -> 00658B6C
00658B60  xor      edx, edx
00658B62  mov      rcx, rsi
00658B65  call     0x600a60  ; -> 00600A60 fn
00658B6A  mov      edi, eax
00658B6C  lea      rcx, [rsp + 0x50]
00658B71  call     0x16d6a0  ; -> 0016D6A0 fn
00658B76  mov      eax, edi
00658B78  lea      r11, [rsp + 0x70]
00658B7D  mov      rbx, qword ptr [r11 + 0x20]
00658B81  mov      rbp, qword ptr [r11 + 0x28]
00658B85  mov      rsi, qword ptr [r11 + 0x30]
00658B89  mov      rsp, r11
00658B8C  pop      r15
00658B8E  pop      r14
00658B90  pop      rdi
00658B91  ret      
```

## 00659A90 (391 B, extent 00659A90-00659C17)

Page context: "epthOfField' | '0065B4C0' | '00658BA0' | 1,241 | | 'PFXAA' | '0065B590' | '0065A640' | 790 | | 'PGlow' | '0065B650' | '00652940' and '00659080' | 326 + 2,575 | | 'PMaterialPostEffect' | '0065B750' | '00659A90' | 391 | | 'PMotionBlur' | '0065B820' | '00659C20' | 659 | | 'PScreenSpaceReflection' | '0065B920' | '0065BA00' | 1,658 |  **The four that are compiled in and implement nothing** are 'PMLAA', 'PScreenSpaceAmbientOcclusion', 'PMeshP"

```
00659A90  mov      r11, rsp
00659A93  push     r14
00659A95  sub      rsp, 0x70
00659A99  mov      qword ptr [r11 - 0x48], 0xfffffffffffffffe
00659AA1  mov      qword ptr [r11 + 8], rbx
00659AA5  mov      qword ptr [r11 + 0x10], rsi
00659AA9  mov      qword ptr [r11 + 0x18], rdi
00659AAD  mov      rbx, r8
00659AB0  mov      rdi, rdx
00659AB3  mov      rsi, rcx
00659AB6  mov      rdx, qword ptr [rcx + 0x58]
00659ABA  lea      r14, [rip + 0x26dac57]  ; -> 02D34718
00659AC1  test     rdx, rdx
00659AC4  je       0x659aef  ; -> 00659AEF
00659AC6  mov      qword ptr [r11 - 0x40], 0x42
00659ACE  mov      qword ptr [r11 - 0x30], r9
00659AD2  mov      qword ptr [r11 - 0x38], r14
00659AD6  mov      rax, qword ptr [rcx + 0x10]
00659ADA  lea      r8, [r11 - 0x40]
00659ADE  mov      rcx, qword ptr [rax + 8]
00659AE2  call     0x1b81b0  ; -> 001B81B0 fn
00659AE7  test     eax, eax
00659AE9  jne      0x659c00  ; -> 00659C00
00659AEF  mov      rax, qword ptr [rsp + 0xa0]
00659AF7  test     rax, rax
00659AFA  je       0x659b32  ; -> 00659B32
00659AFC  mov      rdx, qword ptr [rsi + 0x60]
00659B00  test     rdx, rdx
00659B03  je       0x659b32  ; -> 00659B32
00659B05  mov      qword ptr [rsp + 0x38], 0x42
00659B0E  mov      qword ptr [rsp + 0x48], rax
00659B13  mov      qword ptr [rsp + 0x40], r14
00659B18  mov      rax, qword ptr [rsi + 0x10]
00659B1C  lea      r8, [rsp + 0x38]
00659B21  mov      rcx, qword ptr [rax + 8]
00659B25  call     0x1b81b0  ; -> 001B81B0 fn
00659B2A  test     eax, eax
00659B2C  jne      0x659c00  ; -> 00659C00
00659B32  xor      r8d, r8d
00659B35  mov      rdx, rbx
00659B38  lea      rcx, [rsp + 0x50]
00659B3D  call     0x5dc190  ; -> 005DC190 fn
00659B42  nop      
00659B43  test     rbx, rbx
00659B46  je       0x659b55  ; -> 00659B55
00659B48  mov      eax, dword ptr [rbx + 0xc]
00659B4B  shr      eax, 1
00659B4D  test     al, 1
00659B4F  je       0x659b55  ; -> 00659B55
00659B51  mov      cl, 1
00659B53  jmp      0x659b57  ; -> 00659B57
00659B55  xor      cl, cl
00659B57  lea      rdx, [rip + 0x26de4a2]  ; -> 02D38000
00659B5E  lea      rax, [rip + 0x26de47b]  ; -> 02D37FE0
00659B65  test     cl, cl
00659B67  cmovne   rax, rdx
00659B6B  mov      qword ptr [rdi + 0x80], rax
00659B72  xor      r8d, r8d
00659B75  lea      rdx, [rsp + 0x50]
00659B7A  mov      rcx, rdi
00659B7D  call     0x60d4f0  ; -> 0060D4F0 fn
00659B82  mov      ebx, eax
00659B84  test     eax, eax
00659B86  jne      0x659bf4  ; -> 00659BF4
00659B88  xor      edx, edx
00659B8A  mov      rcx, rdi
00659B8D  call     0x60db50  ; -> 0060DB50 fn
00659B92  mov      ebx, eax
00659B94  test     eax, eax
00659B96  jne      0x659bf4  ; -> 00659BF4
00659B98  xor      edx, edx
00659B9A  mov      rcx, rdi
00659B9D  call     0x5fefd0  ; -> 005FEFD0 fn
00659BA2  mov      ebx, eax
00659BA4  test     eax, eax
00659BA6  jne      0x659bf4  ; -> 00659BF4
00659BA8  lea      rax, [rip + 0x26d0e9]  ; -> 008C6C98
00659BAF  mov      qword ptr [rsp + 0x38], rax
00659BB4  lea      rax, [rsi + 0x30]
00659BB8  mov      qword ptr [rsp + 0x40], rax
00659BBD  mov      byte ptr [rsp + 0x28], bl
00659BC1  mov      eax, dword ptr [rdi + 0x220]
00659BC7  mov      dword ptr [rsp + 0x20], eax
00659BCB  xor      r9d, r9d
00659BCE  lea      r8, [rsp + 0x38]
00659BD3  mov      rdx, qword ptr [rip + 0x26dab36]  ; -> 02D34710
00659BDA  mov      rcx, rdi
00659BDD  call     0x60b980  ; -> 0060B980 fn
00659BE2  mov      ebx, eax
00659BE4  test     eax, eax
00659BE6  jne      0x659bf4  ; -> 00659BF4
00659BE8  xor      edx, edx
00659BEA  mov      rcx, rdi
00659BED  call     0x600a60  ; -> 00600A60 fn
00659BF2  mov      ebx, eax
00659BF4  lea      rcx, [rsp + 0x50]
00659BF9  call     0x16d6a0  ; -> 0016D6A0 fn
00659BFE  mov      eax, ebx
00659C00  lea      r11, [rsp + 0x70]
00659C05  mov      rbx, qword ptr [r11 + 0x10]
00659C09  mov      rsi, qword ptr [r11 + 0x18]
00659C0D  mov      rdi, qword ptr [r11 + 0x20]
00659C11  mov      rsp, r11
00659C14  pop      r14
00659C16  ret      
```

## 00659C20 (659 B, extent 00659C20-00659EB3)

Page context: " 'PFXAA' | '0065B590' | '0065A640' | 790 | | 'PGlow' | '0065B650' | '00652940' and '00659080' | 326 + 2,575 | | 'PMaterialPostEffect' | '0065B750' | '00659A90' | 391 | | 'PMotionBlur' | '0065B820' | '00659C20' | 659 | | 'PScreenSpaceReflection' | '0065B920' | '0065BA00' | 1,658 |  **The four that are compiled in and implement nothing** are 'PMLAA', 'PScreenSpaceAmbientOcclusion', 'PMeshParticleSystemBase' and 'PLowResParticles' — each o"

```
00659C20  push     rdi
00659C22  sub      rsp, 0x50
00659C26  mov      qword ptr [rsp + 0x30], 0xfffffffffffffffe
00659C2F  mov      qword ptr [rsp + 0x60], rbx
00659C34  mov      qword ptr [rsp + 0x68], rbp
00659C39  mov      qword ptr [rsp + 0x70], rsi
00659C3E  mov      rbp, r8
00659C41  mov      rsi, rdx
00659C44  mov      rbx, rcx
00659C47  mov      rdx, r9
00659C4A  call     0x65d720  ; -> 0065D720 fn
00659C4F  mov      rdx, qword ptr [rbx + 0xd28]
00659C56  test     rdx, rdx
00659C59  je       0x659c9a  ; -> 00659C9A
00659C5B  mov      qword ptr [rsp + 0x38], 0x42
00659C64  mov      rax, qword ptr [rsp + 0x80]
00659C6C  mov      qword ptr [rsp + 0x48], rax
00659C71  lea      rax, [rip + 0x26db4c8]  ; -> 02D35140
00659C78  mov      qword ptr [rsp + 0x40], rax
00659C7D  mov      rax, qword ptr [rbx + 0xd20]
00659C84  lea      r8, [rsp + 0x38]
00659C89  mov      rcx, qword ptr [rax + 8]
00659C8D  call     0x1b81b0  ; -> 001B81B0 fn
00659C92  test     eax, eax
00659C94  jne      0x659e9e  ; -> 00659E9E
00659C9A  mov      rdx, qword ptr [rbx + 0xd30]
00659CA1  test     rdx, rdx
00659CA4  je       0x659ce5  ; -> 00659CE5
00659CA6  mov      qword ptr [rsp + 0x38], 0x42
00659CAF  mov      rax, qword ptr [rsp + 0x88]
00659CB7  mov      qword ptr [rsp + 0x48], rax
00659CBC  lea      rax, [rip + 0x26daa55]  ; -> 02D34718
00659CC3  mov      qword ptr [rsp + 0x40], rax
00659CC8  mov      rax, qword ptr [rbx + 0xd20]
00659CCF  lea      r8, [rsp + 0x38]
00659CD4  mov      rcx, qword ptr [rax + 8]
00659CD8  call     0x1b81b0  ; -> 001B81B0 fn
00659CDD  test     eax, eax
00659CDF  jne      0x659e9e  ; -> 00659E9E
00659CE5  mov      rcx, qword ptr [rbx + 0xd40]
00659CEC  mov      edi, 0x1fff
00659CF1  test     rcx, rcx
00659CF4  je       0x659d51  ; -> 00659D51
00659CF6  mov      rax, qword ptr [rbx + 0xd20]
00659CFD  mov      r10, qword ptr [rax + 8]
00659D01  lea      r9, [rbx + 0xd10]
00659D08  test     r9, r9
00659D0B  jne      0x659d17  ; -> 00659D17
00659D0D  mov      eax, 1
00659D12  jmp      0x659e9e  ; -> 00659E9E
00659D17  movzx    edx, word ptr [rcx + 0x10]
00659D1B  movzx    r8d, word ptr [rcx + 0x12]
00659D20  and      r8w, di
00659D24  movzx    ecx, r8w
00659D28  add      ecx, edx
00659D2A  cmp      ecx, dword ptr [r10]
00659D2D  ja       0x659d35  ; -> 00659D35
00659D2F  cmp      dx, 4
00659D33  jae      0x659d3f  ; -> 00659D3F
00659D35  mov      eax, 3
00659D3A  jmp      0x659e9e  ; -> 00659E9E
00659D3F  movzx    r8d, r8w
00659D43  movzx    ecx, dx
00659D46  add      rcx, r10
00659D49  mov      rdx, r9
00659D4C  call     0x861eba  ; -> 00861EBA fn
00659D51  mov      rcx, qword ptr [rbx + 0xd58]
00659D58  test     rcx, rcx
00659D5B  je       0x659da4  ; -> 00659DA4
00659D5D  mov      rax, qword ptr [rbx + 0xd20]
00659D64  mov      r10, qword ptr [rax + 8]
00659D68  lea      r9, [rbx + 0xd0]
00659D6F  test     r9, r9
00659D72  je       0x659d0d  ; -> 00659D0D
00659D74  movzx    edx, word ptr [rcx + 0x10]
00659D78  movzx    r8d, word ptr [rcx + 0x12]
00659D7D  and      r8w, di
00659D81  movzx    ecx, r8w
00659D85  add      ecx, edx
00659D87  cmp      ecx, dword ptr [r10]
00659D8A  ja       0x659d35  ; -> 00659D35
00659D8C  cmp      dx, 4
00659D90  jb       0x659d35  ; -> 00659D35
00659D92  movzx    r8d, r8w
00659D96  movzx    ecx, dx
00659D99  add      rcx, r10
00659D9C  mov      rdx, r9
00659D9F  call     0x861eba  ; -> 00861EBA fn
00659DA4  xor      dil, dil
00659DA7  xor      r8d, r8d
00659DAA  test     rbp, rbp
00659DAD  je       0x659df9  ; -> 00659DF9
00659DAF  mov      rdx, rbp
00659DB2  lea      rcx, [rsp + 0x38]
00659DB7  call     0x5dc190  ; -> 005DC190 fn
00659DBC  nop      
00659DBD  xor      r8d, r8d
00659DC0  lea      rdx, [rsp + 0x38]
00659DC5  mov      rcx, rsi
00659DC8  call     0x60d4f0  ; -> 0060D4F0 fn
00659DCD  mov      edi, eax
00659DCF  test     eax, eax
00659DD1  je       0x659de4  ; -> 00659DE4
00659DD3  lea      rcx, [rsp + 0x38]
00659DD8  call     0x16d6a0  ; -> 0016D6A0 fn
00659DDD  mov      eax, edi
00659DDF  jmp      0x659e9e  ; -> 00659E9E
00659DE4  mov      edi, dword ptr [rbp + 0xc]
00659DE7  shr      edi, 1
00659DE9  and      dil, 1
00659DED  lea      rcx, [rsp + 0x38]
00659DF2  call     0x16d6a0  ; -> 0016D6A0 fn
00659DF7  jmp      0x659e0b  ; -> 00659E0B
00659DF9  xor      edx, edx
00659DFB  mov      rcx, rsi
00659DFE  call     0x60d4f0  ; -> 0060D4F0 fn
00659E03  test     eax, eax
00659E05  jne      0x659e9e  ; -> 00659E9E
00659E0B  lea      rcx, [rip + 0x26dd88e]  ; -> 02D376A0
00659E12  lea      rax, [rip + 0x26dd867]  ; -> 02D37680
00659E19  test     dil, dil
00659E1C  cmovne   rax, rcx
00659E20  mov      qword ptr [rsi + 0x80], rax
00659E27  xor      edx, edx
00659E29  mov      rcx, rsi
00659E2C  call     0x60db50  ; -> 0060DB50 fn
00659E31  test     eax, eax
00659E33  jne      0x659e9e  ; -> 00659E9E
00659E35  xor      edx, edx
00659E37  mov      rcx, rsi
00659E3A  call     0x5fefd0  ; -> 005FEFD0 fn
00659E3F  test     eax, eax
00659E41  jne      0x659e9e  ; -> 00659E9E
00659E43  lea      rax, [rip + 0x26ce4e]  ; -> 008C6C98
00659E4A  mov      qword ptr [rsp + 0x38], rax
00659E4F  lea      rax, [rbx + 0x30]
00659E53  mov      qword ptr [rsp + 0x40], rax
00659E58  mov      byte ptr [rsp + 0x28], 0
00659E5D  mov      eax, dword ptr [rsi + 0x220]
00659E63  mov      dword ptr [rsp + 0x20], eax
00659E67  xor      r9d, r9d
00659E6A  lea      r8, [rsp + 0x38]
00659E6F  mov      rdx, qword ptr [rip + 0x26da89a]  ; -> 02D34710
00659E76  mov      rcx, rsi
00659E79  call     0x60b980  ; -> 0060B980 fn
00659E7E  nop      
00659E7F  test     eax, eax
00659E81  jne      0x659e9e  ; -> 00659E9E
00659E83  xor      edx, edx
00659E85  mov      rcx, rsi
00659E88  call     0x600a60  ; -> 00600A60 fn
00659E8D  test     eax, eax
00659E8F  jne      0x659e9e  ; -> 00659E9E
00659E91  xor      r8d, r8d
00659E94  xor      edx, edx
00659E96  mov      rcx, rsi
00659E99  call     0x60d4f0  ; -> 0060D4F0 fn
00659E9E  mov      rbx, qword ptr [rsp + 0x60]
00659EA3  mov      rbp, qword ptr [rsp + 0x68]
00659EA8  mov      rsi, qword ptr [rsp + 0x70]
00659EAD  add      rsp, 0x50
00659EB1  pop      rdi
00659EB2  ret      
```
