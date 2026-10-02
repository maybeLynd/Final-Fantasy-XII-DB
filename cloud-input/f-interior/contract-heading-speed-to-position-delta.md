# F-interior pack: `06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-heading-speed-to-position-delta.json`.

Functions: 7. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 1890fe2ef	SWE2-CONTRACT: OPUS-INCORP-RATIFIED-0930 heading part - five ratified heading records and the effect; 9ca3df0ac	FABLE: heading CONTRACT - LD-5a pass-through alias precondition; the caller's registers across 002E4; inbox mentions: SWE2-CONTRACT.md). OPUS read these before packing.

## 00345180 (208 B, extent 00345180-00345250)

Page context: "ery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (23 edges).** '00265020' is also called by bodies filed to script VM / native bridge: '0033FD60', '00344AF0', '00345180' - shared machinery across the layer boundary, no shared ownership. - **Spawn_Encounter_Lifecycle - CLIENT (3 edges).** '00265020' is also called by bodies filed to spawn/encounter lifecycle: '00234AF0', '00234DA0', '002350C0' - sh"

```
00345180  mov      qword ptr [rsp + 8], rbx
00345185  mov      qword ptr [rsp + 0x10], rsi
0034518A  push     rdi
0034518B  sub      rsp, 0x60
0034518F  movaps   xmmword ptr [rsp + 0x50], xmm6
00345194  mov      rsi, rcx
00345197  movaps   xmmword ptr [rsp + 0x40], xmm7
0034519C  mov      rcx, r9
0034519F  movaps   xmmword ptr [rsp + 0x30], xmm8
003451A5  mov      rbx, r9
003451A8  mov      rdi, rdx
003451AB  call     0x267db0  ; -> 00267DB0 fn
003451B0  mov      rcx, rbx
003451B3  movaps   xmm8, xmm0
003451B7  call     0x267db0  ; -> 00267DB0 fn
003451BC  mov      rcx, rbx
003451BF  movaps   xmm6, xmm0
003451C2  call     0x267db0  ; -> 00267DB0 fn
003451C7  lea      r9, [rsp + 0x24]
003451CC  mov      rcx, rdi
003451CF  lea      r8, [rsp + 0x28]
003451D4  movaps   xmm7, xmm0
003451D7  lea      rdx, [rsp + 0x20]
003451DC  call     0x265020  ; -> 00265020 fn
003451E1  subss    xmm7, dword ptr [rsp + 0x20]
003451E7  subss    xmm6, dword ptr [rsp + 0x28]
003451ED  subss    xmm8, dword ptr [rsp + 0x24]
003451F4  movss    dword ptr [rsp + 0x20], xmm7
003451FA  mulss    xmm7, xmm7
003451FE  movss    dword ptr [rsp + 0x28], xmm6
00345204  movss    dword ptr [rsp + 0x24], xmm8
0034520B  mulss    xmm6, xmm6
0034520F  mulss    xmm8, xmm8
00345214  addss    xmm7, xmm6
00345218  addss    xmm7, xmm8
0034521D  movaps   xmm0, xmm7
00345220  call     0x3a1d30  ; -> 003A1D30 fn
00345225  movaps   xmm1, xmm0
00345228  mov      rcx, rsi
0034522B  call     0x26b4c0  ; -> 0026B4C0 fn
00345230  mov      rbx, qword ptr [rsp + 0x70]
00345235  mov      rsi, qword ptr [rsp + 0x78]
0034523A  movaps   xmm6, xmmword ptr [rsp + 0x50]
0034523F  movaps   xmm7, xmmword ptr [rsp + 0x40]
00345244  movaps   xmm8, xmmword ptr [rsp + 0x30]
0034524A  add      rsp, 0x60
0034524E  pop      rdi
0034524F  ret      
```

## 003B73B0 (131 B, extent 003B73B0-003B7433)

Page context: "S-18's first  ## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)  - **ActorEntity - CLIENT (8 edges).** '00265020' is also called by bodies filed to ActorEntity: '00236300', '0037B4D0', '003B73B0' - shared machinery across the layer boundary, no shared ownership. - **Audio - CLIENT (1 edge).** '00265020' is also called by bodies filed to audio: '00362850' - shared machinery across the layer boundary, no shared ownership. - "

```
003B73B0  test     rcx, rcx
003B73B3  je       0x3b7432  ; -> 003B7432
003B73B5  push     rbx
003B73B6  sub      rsp, 0x20
003B73BA  mov      rbx, rcx
003B73BD  mov      qword ptr [rsp + 0x30], rdi
003B73C2  call     0x359b80  ; -> 00359B80 fn
003B73C7  mov      rdi, rax
003B73CA  test     rax, rax
003B73CD  je       0x3b7428  ; -> 003B7428
003B73CF  lea      r9, [rax + 8]
003B73D3  mov      rdx, rax
003B73D6  lea      r8, [rax + 4]
003B73DA  mov      rcx, rbx
003B73DD  call     0x265020  ; -> 00265020 fn
003B73E2  lea      r9, [rdi + 0x18]
003B73E6  mov      rcx, rbx
003B73E9  lea      r8, [rdi + 0x14]
003B73ED  lea      rdx, [rdi + 0x10]
003B73F1  call     0x265240  ; -> 00265240 fn
003B73F6  mov      rcx, rbx
003B73F9  call     0x2e9be0  ; -> 002E9BE0 fn
003B73FE  mov      rcx, rbx
003B7401  mov      byte ptr [rdi + 0x64], al
003B7404  call     0x263cc0  ; -> 00263CC0 fn
003B7409  mov      rcx, rbx
003B740C  movss    dword ptr [rdi + 0x34], xmm0
003B7411  call     0x265200  ; -> 00265200 fn
003B7416  mov      rcx, rbx
003B7419  movss    dword ptr [rdi + 0x24], xmm0
003B741E  call     0x263cc0  ; -> 00263CC0 fn
003B7423  movss    dword ptr [rdi + 0x34], xmm0
003B7428  mov      rdi, qword ptr [rsp + 0x30]
003B742D  add      rsp, 0x20
003B7431  pop      rbx
003B7432  ret      
```

## 003DA6A0 (112 B, extent 003DA6A0-003DA710)

Page context: "h 4 over direct calls and tail jumps ('.pdata' chain-root extents)       is 54 functions, and none writes 'r12'–'r15', 'rbx', 'rbp', 'rsi' or 'rdi' without saving it in the same body       (control: '003DA6A0''s saved 'rbp' writes are seen). Six indirect calls inside those 54, and depth beyond 4, are       not followed.* This settles the alias precondition's register half only, not the class question above.       Regression: 'falsify_he"

```
003DA6A0  mov      qword ptr [rsp + 8], rbx
003DA6A5  mov      qword ptr [rsp + 0x10], rbp
003DA6AA  mov      qword ptr [rsp + 0x18], rsi
003DA6AF  push     rdi
003DA6B0  sub      rsp, 0x30
003DA6B4  mov      rsi, r8
003DA6B7  movaps   xmmword ptr [rsp + 0x20], xmm6
003DA6BC  mov      r8, r9
003DA6BF  mov      rdi, r9
003DA6C2  mov      rbx, rdx
003DA6C5  mov      rbp, rcx
003DA6C8  call     0x3da730  ; -> 003DA730 fn
003DA6CD  call     0x3a1d30  ; -> 003A1D30 fn
003DA6D2  mov      r8, rbx
003DA6D5  mov      rdx, rdi
003DA6D8  mov      rcx, rsi
003DA6DB  movaps   xmm6, xmm0
003DA6DE  call     0x3da730  ; -> 003DA730 fn
003DA6E3  call     0x3a1d30  ; -> 003A1D30 fn
003DA6E8  addss    xmm6, dword ptr [rbp + 0xc]
003DA6ED  addss    xmm0, dword ptr [rsi + 0xc]
003DA6F2  mov      rbx, qword ptr [rsp + 0x40]
003DA6F7  mov      rbp, qword ptr [rsp + 0x48]
003DA6FC  mov      rsi, qword ptr [rsp + 0x50]
003DA701  addss    xmm0, xmm6
003DA705  movaps   xmm6, xmmword ptr [rsp + 0x20]
003DA70A  add      rsp, 0x30
003DA70E  pop      rdi
003DA70F  ret      
```

## 003E33E0 (21 B, extent 003E33E0-003E33F5)

Page context: "     steering mode, and when subrecord '+0x65' is set it calls '002EBE50' and '002E8EE0'. It then calls '002E6300',         whose conditional tail enters '00265510'.       - The object-state setters '003E33E0' / '003E3440' read their flags word twice and replace bit 23 / 24. They         could touch actor byte '+3' only if that word sat at 'actor + 1', an alias neither observed nor excluded.         *Placement condition made exact (2026"

```
003E33E0  movzx    eax, dx
003E33E3  shl      eax, 0x17
003E33E6  xor      eax, dword ptr [rcx]
003E33E8  and      eax, 0x800000
003E33ED  xor      eax, dword ptr [rcx]
003E33EF  or       eax, 2
003E33F2  mov      dword ptr [rcx], eax
003E33F4  ret      
```

## 003E3440 (19 B, extent 003E3440-003E3453)

Page context: " mode, and when subrecord '+0x65' is set it calls '002EBE50' and '002E8EE0'. It then calls '002E6300',         whose conditional tail enters '00265510'.       - The object-state setters '003E33E0' / '003E3440' read their flags word twice and replace bit 23 / 24. They         could touch actor byte '+3' only if that word sat at 'actor + 1', an alias neither observed nor excluded.         *Placement condition made exact (2026-10-01, OPUS,"

```
003E3440  shl      edx, 0x18
003E3443  xor      edx, dword ptr [rcx]
003E3445  and      edx, 0x1000000
003E344B  xor      edx, dword ptr [rcx]
003E344D  or       edx, 4
003E3450  mov      dword ptr [rcx], edx
003E3452  ret      
```

## 0040FEF0 (53 B, extent 0040FEF0-0040FF25)

Page context: "0' hold clears in half-rate ('0043EF74'-'0043EF86'), and consults the test again before its tail ('0043F1A8'). '0054B1F0' runs '0040AA20' a second time in half-rate ('0054B342'-'0054B34E') and gates '0040FEF0' on the test at '0054B353'. None of this changes the delta, the gate or the refusal this contract states.   - Tier 1: '001EDDA0' and all nine of its call sites in the four bodies read from the shipping image.  ## Falsification pass"

```
0040FEF0  mov      qword ptr [rsp + 8], rbx
0040FEF5  push     rdi
0040FEF6  sub      rsp, 0x20
0040FEFA  mov      rbx, rdx
0040FEFD  mov      rdi, rcx
0040FF00  call     0x40ff30  ; -> 0040FF30 fn
0040FF05  mov      rdx, rbx
0040FF08  mov      rcx, rdi
0040FF0B  call     0x413c80  ; -> 00413C80 fn
0040FF10  mov      rdx, rbx
0040FF13  mov      rcx, rdi
0040FF16  mov      rbx, qword ptr [rsp + 0x30]
0040FF1B  add      rsp, 0x20
0040FF1F  pop      rdi
0040FF20  jmp      0x411650  ; -> 00411650 fn
```

## 0043EE70 (49 B, extent 0043EE70-0043EEA1)

Page context: ";         - the node head at instance '+0x118' ('003A94D0', '0043EF9B');         - the node link '+0x30' ('003A94EE', '0043EFB0').          The node-type byte '[node+0]' is read by both dispatchers, '0043EE70' and '002F3910'. This is an address-and-link         result. Three precisions come from the review, and a consumer must carry them:         - **Different visited populations.** The flag walk reaches nodes only for instances with a "

```
0043EE70  movzx    r9d, byte ptr [rcx]
0043EE74  sub      r9d, 0x67
0043EE78  je       0x43ee9b  ; -> 0043EE9B
0043EE7A  sub      r9d, 4
0043EE7E  je       0x43ee96  ; -> 0043EE96
0043EE80  sub      r9d, 6
0043EE84  je       0x43ee91  ; -> 0043EE91
0043EE86  cmp      r9d, 1
0043EE8A  jne      0x43eea0  ; -> 0043EEA0
0043EE8C  jmp      0x52b5d0  ; -> 0052B5D0 fn
0043EE91  jmp      0x52a8a0  ; -> 0052A8A0 fn
0043EE96  jmp      0x529d40  ; -> 00529D40 fn
0043EE9B  jmp      0x45fd00  ; -> 0045FD00 fn
0043EEA0  ret      
```
