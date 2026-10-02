# F-interior pack: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/loader-bound-bin-families.json`.

Functions: 12. Each is cited on the page only at its entry and is still in the F frontier.

## 00259370 (35 B, extent 00259370-00259393)

Page context: "rafted at alloc+0x1DC0, section 4"   - "behindcamera | explained | behindcamera.bin (.bin member): {0, u32 count 16, 0, 0} + 16 BehindCameraRecord {f32 scalar, f32 pad, f32 x[7], f32 y[7]} - bound by 00259370, scattered by 00259FE0, preset setter 0025A160, section 3"   - "packdirectory | explained | the six PackFiles directories clutpack_ys / texpack_ys / tex2pack_ys / mrppack_ys / fontpack_fs / fontpack_it (.bin member): fixed-width se"

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

## 0025A540 (109 B, extent 0025A540-0025A5AD)

Page context: "0 == 2' arm calls '00259990(idx, desc+0x20, arg)'. That arm selects the '0x860' context ('rdi = idx*0x860 + 02097D20'), gates on '00377DB0()', then branches on the transition flag '02098DE9' (set by '0025A540', which seeds the same caller-supplied vec4 into **both** objects' '+0x00' head): while the flag is set it runs '003D9E20(1)' and decrements the countdown bytes '02098DEA'/'02098DEB', calling '003D9930'; once clear it calls '003D99"

```
0025A540  movss    xmm0, dword ptr [rdx]
0025A544  movss    dword ptr [rip + 0x1e3d7e4], xmm0  ; -> 02097D30
0025A54C  movss    xmm1, dword ptr [rdx + 4]
0025A551  movss    dword ptr [rip + 0x1e3d7db], xmm1  ; -> 02097D34
0025A559  movss    xmm0, dword ptr [rdx + 8]
0025A55E  movss    dword ptr [rip + 0x1e3d7d2], xmm0  ; -> 02097D38
0025A566  movss    xmm1, dword ptr [rdx + 0xc]
0025A56B  movss    dword ptr [rip + 0x1e3d7c9], xmm1  ; -> 02097D3C
0025A573  movss    xmm0, dword ptr [rdx]
0025A577  movss    dword ptr [rip + 0x1e3e011], xmm0  ; -> 02098590
0025A57F  movss    xmm1, dword ptr [rdx + 4]
0025A584  movss    dword ptr [rip + 0x1e3e008], xmm1  ; -> 02098594
0025A58C  movss    xmm0, dword ptr [rdx + 8]
0025A591  movss    dword ptr [rip + 0x1e3dfff], xmm0  ; -> 02098598
0025A599  movss    xmm1, dword ptr [rdx + 0xc]
0025A59E  movss    dword ptr [rip + 0x1e3dff6], xmm1  ; -> 0209859C
0025A5A6  mov      byte ptr [rip + 0x1e3e83d], cl  ; -> 02098DE9
0025A5AC  ret      
```

## 00280980 (115 B, extent 00280980-002809F3)

Page context: "_ys / fontpack_fs / fontpack_it (.bin member): fixed-width sentinel-filled u32 self-relative offset directory (0x40 or 0x80) over TIM2 / MRP / CLT2 / font-table payloads - binders 00246A10, 00280670, 00280980, 00280AD0, 003643A0, 0039C150, section 2" audit:   passes: 1   last_pass: 2026-09-29   last_pass_kind: falsification   last_pass_state: opus-loader-bound-falsification-pass-1   crossref_clean: false   reopened_count: 0 ---  # The l"

```
00280980  sub      rsp, 0x28
00280984  mov      rdx, qword ptr [rip + 0x1e1a2a5]  ; -> 0209AC30
0028098B  cmp      qword ptr [rdx + 0x3d0], 0
00280993  je       0x2809ea  ; -> 002809EA
00280995  mov      qword ptr [rsp + 0x30], rbx
0028099A  xor      ebx, ebx
0028099C  mov      qword ptr [rsp + 0x20], rdi
002809A1  mov      edi, ebx
002809A3  cmp      qword ptr [rbx + rdx], 0
002809A8  jne      0x2809d2  ; -> 002809D2
002809AA  mov      rax, qword ptr [rdx + 0x3d0]
002809B1  mov      ecx, dword ptr [rdi + rax]
002809B4  add      rcx, rax
002809B7  mov      qword ptr [rbx + rdx], rcx
002809BB  mov      rcx, qword ptr [rip + 0x1e1a26e]  ; -> 0209AC30
002809C2  mov      rcx, qword ptr [rbx + rcx]
002809C6  call     0x2a00f0  ; -> 002A00F0 fn
002809CB  mov      rdx, qword ptr [rip + 0x1e1a25e]  ; -> 0209AC30
002809D2  add      rdi, 4
002809D6  add      rbx, 8
002809DA  cmp      rdi, 0x5c
002809DE  jl       0x2809a3  ; -> 002809A3
002809E0  mov      rdi, qword ptr [rsp + 0x20]
002809E5  mov      rbx, qword ptr [rsp + 0x30]
002809EA  add      rsp, 0x28
002809EE  jmp      0x280ad0  ; -> 00280AD0 fn
```

## 00291010 (434 B, extent 00291010-002911C2)

Page context: "0'. Shared-helper fan-in; no movement relationship to the bin families.  **UI — CLIENT (SWE2-EC7-168, 54 edges).** '00181000'/'00181250' — the bin-family helpers this page cites — are each called by '00291010' and '002917E0' on the UI layer (+50 more). Shared-helper fan-in; no UI relationship to the bin families. Edge list from 'edges.tsv'. - **Gameplay — MECHANICAL (4 edges).** 1 Gameplay-side calls into shared helper(s) the page cites"

```
00291010  push     rbx
00291012  push     rsi
00291013  push     rdi
00291014  sub      rsp, 0x60
00291018  mov      rax, qword ptr [rip + 0x1cb3811]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0029101F  xor      rax, rsp
00291022  mov      qword ptr [rsp + 0x40], rax
00291027  test     dword ptr [rcx + 0x10f68], 0x800
00291031  mov      edi, r8d
00291034  mov      esi, edx
00291036  mov      rbx, rcx
00291039  je       0x29106a  ; -> 0029106A
0029103B  mov      rcx, qword ptr [rcx + 0x10f30]
00291042  test     rcx, rcx
00291045  je       0x29108e  ; -> 0029108E
00291047  call     0x3f73d0  ; -> 003F73D0 fn
0029104C  test     rax, rax
0029104F  je       0x29108e  ; -> 0029108E
00291051  movzx    ecx, word ptr [rax + 0x2f0]
00291058  cmp      cx, 4
0029105C  jae      0x29108e  ; -> 0029108E
0029105E  cmp      esi, edi
00291060  jne      0x291071  ; -> 00291071
00291062  mov      rcx, rax
00291065  call     0x3f6fd0  ; -> 003F6FD0 fn
0029106A  xor      eax, eax
0029106C  jmp      0x2911ad  ; -> 002911AD
00291071  cmp      cx, 3
00291075  jb       0x291083  ; -> 00291083
00291077  mov      ecx, 2
0029107C  mov      word ptr [rax + 0x2f0], cx
00291083  mov      dword ptr [rax + 0x2d4], edi
00291089  jmp      0x2911ad  ; -> 002911AD
0029108E  cmp      esi, edi
00291090  je       0x29106a  ; -> 0029106A
00291092  mov      rdx, qword ptr [rip + 0x1e0ade7]  ; -> 0209BE80
00291099  mov      r8d, 0x340
0029109F  xor      ecx, ecx
002910A1  mov      qword ptr [rsp + 0x50], r14
002910A6  mov      rdx, qword ptr [rdx + 0x10fc0]
002910AD  call     0x273a30  ; -> 00273A30 fn
002910B2  mov      r14, rax
002910B5  test     rax, rax
002910B8  je       0x2911a8  ; -> 002911A8
002910BE  mov      edx, 0x340
002910C3  mov      qword ptr [rsp + 0x58], rbp
002910C8  mov      rcx, rax
002910CB  call     0x275550  ; -> 00275550 fn
002910D0  cmp      qword ptr [rbx + 0x10f50], 0
002910D8  jne      0x2910ed  ; -> 002910ED
002910DA  mov      rcx, qword ptr [rip + 0x1b7b0ff]  ; -> 01E0C1E0 [u64 0x00000000009152A0]
002910E1  call     0x24a5a0  ; -> 0024A5A0 fn
002910E6  mov      qword ptr [rbx + 0x10f50], rax
002910ED  mov      rbp, qword ptr [rbx + 0x10f50]
002910F4  mov      rcx, rbp
002910F7  call     0x181540  ; -> 00181540 fn
002910FC  test     eax, eax
002910FE  jne      0x291148  ; -> 00291148
00291100  mov      rax, qword ptr [rbp + 0x20]
00291104  mov      rcx, rbp
00291107  movzx    edx, word ptr [rax + 0xc]
0029110B  movzx    r9d, word ptr [rax + 0x16]
00291110  add      rdx, rax
00291113  movzx    r8d, word ptr [rax + 0x14]
00291118  call     0x181250  ; -> 00181250 fn
0029111D  mov      rdx, qword ptr [rbp + 0x20]
00291121  movzx    ecx, byte ptr [rdx + 0x13]
00291125  movzx    eax, word ptr [rdx + 0xc]
00291129  mov      r8d, dword ptr [rdx + 8]
0029112D  add      rax, rdx
00291130  movzx    r9d, byte ptr [rdx + 0x12]
00291135  add      r8, rax
00291138  movzx    edx, word ptr [rdx + 0xe]
0029113C  mov      dword ptr [rsp + 0x20], ecx
00291140  mov      rcx, rbp
00291143  call     0x181000  ; -> 00181000 fn
00291148  mov      rcx, qword ptr [rbp + 0x20]
0029114C  mov      r8, qword ptr [rbp + 0x30]
00291150  add      rcx, 0x30
00291154  movzx    eax, word ptr [rcx + 0x14]
00291158  movzx    r9d, word ptr [rcx + rax*2 + 0x14]
0029115E  movzx    eax, word ptr [rcx + 0x10]
00291162  add      rcx, rax
00291165  lea      rdx, [rcx + r9*8]
00291169  lea      rcx, [rsp + 0x30]
0029116E  call     0x271140  ; -> 00271140 fn
00291173  lea      r9, [rsp + 0x30]
00291178  mov      qword ptr [rsp + 0x20], rbp
0029117D  mov      r8d, edi
00291180  mov      edx, esi
00291182  mov      rcx, r14
00291185  call     0x3f73f0  ; -> 003F73F0 fn
0029118A  mov      rcx, qword ptr [rbx + 0x10f30]
00291191  mov      rdx, r14
00291194  call     0x3f7380  ; -> 003F7380 fn
00291199  mov      rbp, qword ptr [rsp + 0x58]
0029119E  mov      qword ptr [rbx + 0x10f30], rax
002911A5  mov      rax, r14
002911A8  mov      r14, qword ptr [rsp + 0x50]
002911AD  mov      rcx, qword ptr [rsp + 0x40]
002911B2  xor      rcx, rsp
002911B5  call     0x808c40  ; -> 00808C40 fn
002911BA  add      rsp, 0x60
002911BE  pop      rdi
002911BF  pop      rsi
002911C0  pop      rbx
002911C1  ret      
```

## 002DD810 (35 B, extent 002DD810-002DD833)

Page context: "kind-9 named object bound by 003DC330 as PCSkill, section 3"   - "fontcolor | explained | fontcolor.bin (.bin member): {u32 count, u64 colorPair[count]} (0x83C) - (kind 7, 0x05) by 0029CED0, bound by 002DD810, read by 002DD840, section 4"   - "monotonechr | explained | monotone_chr.bin (.bin member): {CLT2 palette, pixels} twice (0x1980) - (kind 7, 0x74) by 002C8EE0 into 0209E640, clutpack palette grafted at alloc+0x1DC0, section 4"   -"

```
002DD810  xor      eax, eax
002DD812  mov      qword ptr [rip + 0x1e80ea7], rax  ; -> 0215E6C0
002DD819  mov      qword ptr [rip + 0x1e80e98], rax  ; -> 0215E6B8
002DD820  mov      qword ptr [rip + 0x1e80ea1], rax  ; -> 0215E6C8
002DD827  mov      rax, qword ptr [rcx + 8]
002DD82B  mov      qword ptr [rip + 0x1e80e8e], rax  ; -> 0215E6C0
002DD832  ret      
```

## 002DD840 (27 B, extent 002DD840-002DD85B)

Page context: "t bound by 003DC330 as PCSkill, section 3"   - "fontcolor | explained | fontcolor.bin (.bin member): {u32 count, u64 colorPair[count]} (0x83C) - (kind 7, 0x05) by 0029CED0, bound by 002DD810, read by 002DD840, section 4"   - "monotonechr | explained | monotone_chr.bin (.bin member): {CLT2 palette, pixels} twice (0x1980) - (kind 7, 0x74) by 002C8EE0 into 0209E640, clutpack palette grafted at alloc+0x1DC0, section 4"   - "behindcamera | e"

```
002DD840  mov      rcx, qword ptr [rip + 0x1e80e79]  ; -> 0215E6C0
002DD847  mov      eax, dword ptr [rcx]
002DD849  mov      dword ptr [rip + 0x1e80e69], eax  ; -> 0215E6B8
002DD84F  lea      rax, [rcx + 4]
002DD853  mov      qword ptr [rip + 0x1e80e6e], rax  ; -> 0215E6C8
002DD85A  ret      
```

## 0032AEC0 (767 B, extent 0032AEC0-0032B1BF)

Page context: "eld '0032B1C0(mover, target)' adds into 'target.y' when it latches the target into the channel state ('mover+0x60'), and whose constructor default ('0032B790') is **1.3 — the record-0 scalar**. Then '0032AEC0(obj+0x2B0, desc, ctx+0x640)': the generic steering mover ('0032B1C0' latch → '0032B900' status → '+0x320' frame counter → '0032C5E0' four-slot classification → '003CC130' direction decompose → '0032D000' angular easing → keys '+0x3"

```
0032AEC0  mov      r11, rsp
0032AEC3  push     rbp
0032AEC4  push     rsi
0032AEC5  push     r14
0032AEC7  sub      rsp, 0x80
0032AECE  mov      rax, qword ptr [rip + 0x1c1995b]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0032AED5  xor      rax, rsp
0032AED8  mov      qword ptr [rsp + 0x60], rax
0032AEDD  mov      qword ptr [rcx + 0x2c0], r8
0032AEE4  mov      rbp, r8
0032AEE7  mov      r14, rdx
0032AEEA  mov      rsi, rcx
0032AEED  test     r8, r8
0032AEF0  je       0x32b1a6  ; -> 0032B1A6
0032AEF6  mov      qword ptr [r11 + 0x18], rbx
0032AEFA  mov      rdx, r8
0032AEFD  mov      qword ptr [r11 + 0x20], rdi
0032AF01  movaps   xmmword ptr [rsp + 0x70], xmm6
0032AF06  call     0x32b1c0  ; -> 0032B1C0 fn
0032AF0B  mov      rcx, rsi
0032AF0E  call     0x32b900  ; -> 0032B900 fn
0032AF13  movss    xmm6, dword ptr [rip + 0x5cbe39]  ; -> 008F6D54 [f32 60]
0032AF1B  test     eax, eax
0032AF1D  je       0x32af9a  ; -> 0032AF9A
0032AF1F  inc      dword ptr [rsi + 0x320]
0032AF25  xorps    xmm1, xmm1
0032AF28  mov      eax, dword ptr [rip + 0x1ad3186]  ; -> 01DFE0B4 [u32 0x00000001]
0032AF2E  movd     xmm0, dword ptr [rsi + 0x320]
0032AF36  cvtdq2ps xmm0, xmm0
0032AF39  cvtsi2ss xmm1, rax
0032AF3E  mulss    xmm1, xmm6
0032AF42  divss    xmm1, xmm6
0032AF46  mulss    xmm1, dword ptr [rip + 0x5eb3c6]  ; -> 00916314 [f32 15]
0032AF4E  comiss   xmm0, xmm1
0032AF51  jbe      0x32af5d  ; -> 0032AF5D
0032AF53  cvttss2si eax, xmm1
0032AF57  mov      dword ptr [rsi + 0x320], eax
0032AF5D  cmp      dword ptr [rip + 0x1bc2510], 0  ; -> 01EED474 [u32 0x00000001]
0032AF64  je       0x32af8d  ; -> 0032AF8D
0032AF66  lea      r9, [rsi + 0x310]
0032AF6D  lea      r8, [rsi + 0x300]
0032AF74  lea      rdx, [rsi + 0x2f0]
0032AF7B  lea      rcx, [rsi + 0x2e0]
0032AF82  call     0x32c5e0  ; -> 0032C5E0 fn
0032AF87  mov      dword ptr [rsi + 0x324], eax
0032AF8D  xor      ecx, ecx
0032AF8F  mov      dword ptr [rip + 0x1bc24df], ecx  ; -> 01EED474 [u32 0x00000001]
0032AF95  jmp      0x32b02f  ; -> 0032B02F
0032AF9A  add      dword ptr [rsi + 0x320], -1
0032AFA1  mov      ecx, 0
0032AFA6  mov      eax, dword ptr [rsi + 0x320]
0032AFAC  cmovs    eax, ecx
0032AFAF  cmp      dword ptr [rip + 0x1bc24bf], ecx  ; -> 01EED474 [u32 0x00000001]
0032AFB5  mov      dword ptr [rsi + 0x320], eax
0032AFBB  jne      0x32b025  ; -> 0032B025
0032AFBD  lea      rax, [rsp + 0x34]
0032AFC2  lea      r9, [rsp + 0x38]
0032AFC7  mov      qword ptr [rsp + 0x20], rax
0032AFCC  lea      r8, [rsp + 0x30]
0032AFD1  lea      rdx, [rsi + 0x300]
0032AFD8  lea      rcx, [rsi + 0x310]
0032AFDF  call     0x3cc130  ; -> 003CC130 fn
0032AFE4  movss    xmm0, dword ptr [rsp + 0x30]
0032AFEA  mov      rdx, rbp
0032AFED  mov      rcx, rsi
0032AFF0  movss    dword ptr [rsi + 0x70], xmm0
0032AFF5  mov      byte ptr [rsi + 0x40], 0
0032AFF9  call     0x32b1c0  ; -> 0032B1C0 fn
0032AFFE  lea      rdx, [rsi + 0x2f0]
0032B005  lea      rcx, [rsi + 0x2e0]
0032B00C  lea      r9, [rsi + 0x310]
0032B013  lea      r8, [rsi + 0x300]
0032B01A  call     0x32c5e0  ; -> 0032C5E0 fn
0032B01F  mov      dword ptr [rsi + 0x324], eax
0032B025  mov      dword ptr [rip + 0x1bc2445], 1  ; -> 01EED474 [u32 0x00000001]
0032B02F  mov      rcx, rsi
0032B032  call     0x32d000  ; -> 0032D000 fn
0032B037  lea      rdi, [rsi + 0x330]
0032B03E  xorps    xmm3, xmm3
0032B041  mov      rdx, rdi
0032B044  lea      r8, [rsi + 0x340]
0032B04B  mov      rcx, r14
0032B04E  call     0x3cc080  ; -> 003CC080 fn
0032B053  mov      eax, dword ptr [rip + 0x1ad305b]  ; -> 01DFE0B4 [u32 0x00000001]
0032B059  xorps    xmm1, xmm1
0032B05C  movd     xmm0, dword ptr [rsi + 0x320]
0032B064  cvtdq2ps xmm0, xmm0
0032B067  cvtsi2ss xmm1, rax
0032B06C  mulss    xmm1, xmm6
0032B070  divss    xmm1, xmm6
0032B074  mulss    xmm1, dword ptr [rip + 0x5eb298]  ; -> 00916314 [f32 15]
0032B07C  divss    xmm0, xmm1
0032B080  movss    xmm1, dword ptr [rip + 0x9e5824]  ; -> 00D108AC [f32 0.16]
0032B088  call     0x861f6e  ; -> 00861F6E fn
0032B08D  lea      rdx, [r14 + 0x20]
0032B091  movaps   xmm6, xmm0
0032B094  lea      r8, [r14 + 0xa0]
0032B09B  lea      rcx, [rsp + 0x50]
0032B0A0  call     0x202b70  ; -> 00202B70 fn
0032B0A5  lea      r8, [r14 + 0x90]
0032B0AC  lea      rdx, [r14 + 0xa0]
0032B0B3  lea      rcx, [rsp + 0x40]
0032B0B8  call     0x203080  ; -> 00203080 fn
0032B0BD  lea      rdx, [rsp + 0x40]
0032B0C2  lea      rcx, [rsp + 0x40]
0032B0C7  call     0x202de0  ; -> 00202DE0 fn
0032B0CC  movss    xmm0, dword ptr [rip + 0x19c0ad4]  ; -> 01CEBBA8 [f32 1]
0032B0D4  lea      r8, [rsp + 0x40]
0032B0D9  movaps   xmm1, xmm6
0032B0DC  mov      ecx, 1
0032B0E1  mulss    xmm1, dword ptr [rip + 0x19c0b1f]  ; -> 01CEBC08 [f32 2]
0032B0E9  mulss    xmm6, dword ptr [rip + 0x5c8017]  ; -> 008F3108 [f32 0.8]
0032B0F1  addss    xmm1, xmm0
0032B0F5  subss    xmm0, xmm6
0032B0F9  mulss    xmm0, dword ptr [rsp + 0x58]
0032B0FF  xorps    xmm0, xmmword ptr [rip + 0x19c0c9a]  ; -> 01CEBDA0 [f32x4 -0, -0, -0, -0]
0032B106  maxss    xmm1, xmm0
0032B10A  call     0x1825c0  ; -> 001825C0 fn
0032B10F  movss    xmm2, dword ptr [rip + 0x1bc2329]  ; -> 01EED440 [u32 0x00000000]
0032B117  movss    xmm0, dword ptr [rip + 0x1bc2325]  ; -> 01EED444 [u32 0x00000000]
0032B11F  subss    xmm0, dword ptr [rdi + 4]
0032B124  subss    xmm2, dword ptr [rdi]
0032B128  movss    xmm1, dword ptr [rip + 0x1bc2318]  ; -> 01EED448 [u32 0x00000000]
0032B130  subss    xmm1, dword ptr [rdi + 8]
0032B135  mulss    xmm0, xmm0
0032B139  mulss    xmm2, xmm2
0032B13D  mulss    xmm1, xmm1
0032B141  addss    xmm0, xmm2
0032B145  addss    xmm0, xmm1
0032B149  call     0x861f14  ; -> 00861F14 fn
0032B14E  addss    xmm0, dword ptr [rsi + 0x368]
0032B156  movaps   xmm6, xmmword ptr [rsp + 0x70]
0032B15B  mov      rbx, qword ptr [rsp + 0xb0]
0032B163  movss    dword ptr [rsi + 0x368], xmm0
0032B16B  movss    xmm0, dword ptr [rdi]
0032B16F  movss    dword ptr [rip + 0x1bc22c9], xmm0  ; -> 01EED440 [u32 0x00000000]
0032B177  movss    xmm1, dword ptr [rdi + 4]
0032B17C  movss    dword ptr [rip + 0x1bc22c0], xmm1  ; -> 01EED444 [u32 0x00000000]
0032B184  movss    xmm0, dword ptr [rdi + 8]
0032B189  movss    dword ptr [rip + 0x1bc22b7], xmm0  ; -> 01EED448 [u32 0x00000000]
0032B191  movss    xmm1, dword ptr [rdi + 0xc]
0032B196  mov      rdi, qword ptr [rsp + 0xb8]
0032B19E  movss    dword ptr [rip + 0x1bc22a6], xmm1  ; -> 01EED44C [f32 1]
0032B1A6  mov      rcx, qword ptr [rsp + 0x60]
0032B1AB  xor      rcx, rsp
0032B1AE  call     0x808c40  ; -> 00808C40 fn
0032B1B3  add      rsp, 0x80
0032B1BA  pop      r14
0032B1BC  pop      rsi
0032B1BD  pop      rbp
0032B1BE  ret      
```

## 0032B900 (177 B, extent 0032B900-0032B9B1)

Page context: "channel state ('mover+0x60'), and whose constructor default ('0032B790') is **1.3 — the record-0 scalar**. Then '0032AEC0(obj+0x2B0, desc, ctx+0x640)': the generic steering mover ('0032B1C0' latch → '0032B900' status → '+0x320' frame counter → '0032C5E0' four-slot classification → '003CC130' direction decompose → '0032D000' angular easing → keys '+0x330'/'+0x340' → '003CC080' into 'desc'). '003CC130' is a spherical-decompose helper (del"

```
0032B900  mov      qword ptr [rsp + 8], rbx
0032B905  push     rdi
0032B906  sub      rsp, 0x20
0032B90A  mov      rbx, rcx
0032B90D  xor      edi, edi
0032B90F  call     0x3d9fe0  ; -> 003D9FE0 fn
0032B914  test     eax, eax
0032B916  je       0x32b936  ; -> 0032B936
0032B918  call     0x3d9fd0  ; -> 003D9FD0 fn
0032B91D  test     eax, eax
0032B91F  jne      0x32b929  ; -> 0032B929
0032B921  cmp      dword ptr [rbx + 0x360], edi
0032B927  jne      0x32b93c  ; -> 0032B93C
0032B929  call     0x3d9fa0  ; -> 003D9FA0 fn
0032B92E  mov      dword ptr [rbx + 0x360], eax
0032B934  jmp      0x32b93c  ; -> 0032B93C
0032B936  mov      dword ptr [rbx + 0x360], edi
0032B93C  call     0x3d9ff0  ; -> 003D9FF0 fn
0032B941  test     eax, eax
0032B943  je       0x32b994  ; -> 0032B994
0032B945  mov      eax, dword ptr [rbx + 0xc0]
0032B94B  shr      eax, 0x13
0032B94E  not      eax
0032B950  and      eax, 1
0032B953  je       0x32b99e  ; -> 0032B99E
0032B955  cmp      dword ptr [rbx + 0x360], edi
0032B95B  je       0x32b99e  ; -> 0032B99E
0032B95D  mov      edx, dword ptr [rip + 0x1f97829]  ; -> 022C318C
0032B963  mov      rcx, rbx
0032B966  call     0x32d250  ; -> 0032D250 fn
0032B96B  mov      rcx, rbx
0032B96E  call     0x32ca70  ; -> 0032CA70 fn
0032B973  mov      edi, eax
0032B975  test     eax, eax
0032B977  jne      0x32b99e  ; -> 0032B99E
0032B979  or       dword ptr [rbx + 0xc0], 0x80000
0032B983  mov      dword ptr [rip + 0x1f97803], eax  ; -> 022C318C
0032B989  mov      rbx, qword ptr [rsp + 0x30]
0032B98E  add      rsp, 0x20
0032B992  pop      rdi
0032B993  ret      
0032B994  and      dword ptr [rbx + 0xc0], 0xfff7ffff
0032B99E  mov      rbx, qword ptr [rsp + 0x30]
0032B9A3  mov      eax, edi
0032B9A5  mov      dword ptr [rip + 0x1f977e1], edi  ; -> 022C318C
0032B9AB  add      rsp, 0x20
0032B9AF  pop      rdi
0032B9B0  ret      
```

## 0032C5E0 (108 B, extent 0032C5E0-0032C64C)

Page context: "ructor default ('0032B790') is **1.3 — the record-0 scalar**. Then '0032AEC0(obj+0x2B0, desc, ctx+0x640)': the generic steering mover ('0032B1C0' latch → '0032B900' status → '+0x320' frame counter → '0032C5E0' four-slot classification → '003CC130' direction decompose → '0032D000' angular easing → keys '+0x330'/'+0x340' → '003CC080' into 'desc'). '003CC130' is a spherical-decompose helper (delta → yaw/pitch/distance), not the curve walk."

```
0032C5E0  mov      r11, rsp
0032C5E3  mov      qword ptr [r11 + 0x20], r9
0032C5E7  mov      qword ptr [r11 + 0x18], r8
0032C5EB  mov      qword ptr [r11 + 0x10], rdx
0032C5EF  mov      qword ptr [r11 + 8], rcx
0032C5F3  sub      rsp, 0x48
0032C5F7  lea      rax, [r11 - 0x18]
0032C5FB  lea      r9, [r11 - 0x14]
0032C5FF  mov      qword ptr [r11 - 0x28], rax
0032C603  lea      r8, [r11 - 0xc]
0032C607  lea      rdx, [r11 + 8]
0032C60B  lea      rcx, [r11 + 0x10]
0032C60F  call     0x3cc130  ; -> 003CC130 fn
0032C614  lea      rax, [rsp + 0x30]
0032C619  lea      r9, [rsp + 0x34]
0032C61E  mov      qword ptr [rsp + 0x20], rax
0032C623  lea      r8, [rsp + 0x38]
0032C628  lea      rdx, [rsp + 0x60]
0032C62D  lea      rcx, [rsp + 0x68]
0032C632  call     0x3cc130  ; -> 003CC130 fn
0032C637  movss    xmm1, dword ptr [rsp + 0x38]
0032C63D  movss    xmm0, dword ptr [rsp + 0x3c]
0032C643  add      rsp, 0x48
0032C647  jmp      0x32cc90  ; -> 0032CC90 fn
```

## 0032D000 (577 B, extent 0032D000-0032D241)

Page context: "2AEC0(obj+0x2B0, desc, ctx+0x640)': the generic steering mover ('0032B1C0' latch → '0032B900' status → '+0x320' frame counter → '0032C5E0' four-slot classification → '003CC130' direction decompose → '0032D000' angular easing → keys '+0x330'/'+0x340' → '003CC080' into 'desc'). '003CC130' is a spherical-decompose helper (delta → yaw/pitch/distance), not the curve walk.  The record-0 curve is also the **baked code default**: '003D99B0' — t"

```
0032D000  mov      r11, rsp
0032D003  push     rbx
0032D004  push     rsi
0032D005  push     rdi
0032D006  sub      rsp, 0x60
0032D00A  mov      rbx, rcx
0032D00D  movaps   xmmword ptr [rsp + 0x50], xmm6
0032D012  lea      rdx, [rcx + 0x2f0]
0032D019  movaps   xmmword ptr [rsp + 0x40], xmm7
0032D01E  lea      rax, [r11 - 0x44]
0032D022  add      rcx, 0x2e0
0032D029  lea      r9, [r11 + 0x20]
0032D02D  mov      qword ptr [r11 - 0x58], rax
0032D031  lea      r8, [r11 + 0x10]
0032D035  call     0x3cc130  ; -> 003CC130 fn
0032D03A  lea      rax, [rsp + 0x30]
0032D03F  lea      rdx, [rbx + 0x310]
0032D046  mov      qword ptr [rsp + 0x20], rax
0032D04B  lea      r9, [rsp + 0x90]
0032D053  lea      r8, [rsp + 0x80]
0032D05B  lea      rcx, [rbx + 0x300]
0032D062  call     0x3cc130  ; -> 003CC130 fn
0032D067  movss    xmm6, dword ptr [rsp + 0x80]
0032D070  movss    xmm7, dword ptr [rsp + 0x88]
0032D079  movaps   xmm1, xmm6
0032D07C  movaps   xmm0, xmm7
0032D07F  call     0x32cc90  ; -> 0032CC90 fn
0032D084  test     eax, eax
0032D086  je       0x32d097  ; -> 0032D097
0032D088  comiss   xmm7, xmm6
0032D08B  jbe      0x32d0ad  ; -> 0032D0AD
0032D08D  addss    xmm6, dword ptr [rip + 0x19bebe3]  ; -> 01CEBC78 [f32 6.283185]
0032D095  jmp      0x32d0a4  ; -> 0032D0A4
0032D097  comiss   xmm6, xmm7
0032D09A  jbe      0x32d0ad  ; -> 0032D0AD
0032D09C  addss    xmm6, dword ptr [rip + 0x5e8580]  ; -> 00915624 [f32 -6.283185]
0032D0A4  movss    dword ptr [rsp + 0x80], xmm6
0032D0AD  mov      eax, dword ptr [rip + 0x1ad1001]  ; -> 01DFE0B4 [u32 0x00000001]
0032D0B3  xorps    xmm2, xmm2
0032D0B6  movd     xmm0, dword ptr [rbx + 0x320]
0032D0BE  cvtdq2ps xmm0, xmm0
0032D0C1  cvtsi2ss xmm2, rax
0032D0C6  mulss    xmm2, dword ptr [rip + 0x5c9c86]  ; -> 008F6D54 [f32 60]
0032D0CE  divss    xmm2, dword ptr [rip + 0x5c9c7e]  ; -> 008F6D54 [f32 60]
0032D0D6  mulss    xmm2, dword ptr [rip + 0x5e9236]  ; -> 00916314 [f32 15]
0032D0DE  divss    xmm0, xmm2
0032D0E2  mulss    xmm0, dword ptr [rip + 0x19beb66]  ; -> 01CEBC50 [f32 3.141593]
0032D0EA  addss    xmm0, dword ptr [rip + 0x19beb5e]  ; -> 01CEBC50 [f32 3.141593]
0032D0F2  call     0x861f08  ; -> 00861F08 fn
0032D0F7  movss    xmm3, dword ptr [rip + 0x5e8511]  ; -> 00915610 [f32 0.3926991]
0032D0FF  subss    xmm6, xmm7
0032D103  movss    xmm2, dword ptr [rip + 0x9e37e5]  ; -> 00D108F0 [f32 -0.3926991]
0032D10B  movaps   xmm5, xmm0
0032D10E  addss    xmm5, dword ptr [rip + 0x19bea92]  ; -> 01CEBBA8 [f32 1]
0032D116  movss    xmm0, dword ptr [rip + 0x1f9607a]  ; -> 022C3198
0032D11E  mulss    xmm5, dword ptr [rip + 0x19bea4a]  ; -> 01CEBB70 [f32 0.5]
0032D126  mulss    xmm6, xmm5
0032D12A  addss    xmm6, xmm7
0032D12E  subss    xmm0, xmm6
0032D132  comiss   xmm0, xmm3
0032D135  ja       0x32d13c  ; -> 0032D13C
0032D137  comiss   xmm2, xmm0
0032D13A  jbe      0x32d145  ; -> 0032D145
0032D13C  movss    dword ptr [rsp + 0x80], xmm7
0032D145  movss    xmm4, dword ptr [rsp + 0x90]
0032D14E  subss    xmm4, dword ptr [rsp + 0x98]
0032D157  movss    xmm1, dword ptr [rip + 0x1f9603d]  ; -> 022C319C
0032D15F  movss    dword ptr [rip + 0x1f96031], xmm6  ; -> 022C3198
0032D167  mulss    xmm4, xmm5
0032D16B  addss    xmm4, dword ptr [rsp + 0x98]
0032D174  subss    xmm1, xmm4
0032D178  comiss   xmm1, xmm3
0032D17B  ja       0x32d182  ; -> 0032D182
0032D17D  comiss   xmm2, xmm1
0032D180  jbe      0x32d18b  ; -> 0032D18B
0032D182  movss    dword ptr [rsp + 0x80], xmm7
0032D18B  movss    xmm0, dword ptr [rbx + 0x300]
0032D193  lea      rcx, [rbx + 0x330]
0032D19A  subss    xmm0, dword ptr [rbx + 0x2e0]
0032D1A2  movss    xmm1, dword ptr [rbx + 0x2e4]
0032D1AA  lea      rax, [rbx + 0x340]
0032D1B1  movss    xmm3, dword ptr [rbx + 0x308]
0032D1B9  movss    xmm2, dword ptr [rbx + 0x304]
0032D1C1  subss    xmm2, xmm1
0032D1C5  movss    dword ptr [rip + 0x1f95fcf], xmm4  ; -> 022C319C
0032D1CD  mulss    xmm0, xmm5
0032D1D1  mov      qword ptr [rsp + 0x20], rax
0032D1D6  addss    xmm0, dword ptr [rbx + 0x2e0]
0032D1DE  mulss    xmm2, xmm5
0032D1E2  addss    xmm2, xmm1
0032D1E6  movss    dword ptr [rcx], xmm0
0032D1EA  movss    xmm0, dword ptr [rbx + 0x2e8]
0032D1F2  movaps   xmm1, xmm6
0032D1F5  subss    xmm3, xmm0
0032D1F9  movss    dword ptr [rbx + 0x334], xmm2
0032D201  movaps   xmm2, xmm4
0032D204  mulss    xmm3, xmm5
0032D208  addss    xmm3, xmm0
0032D20C  movss    dword ptr [rbx + 0x338], xmm3
0032D214  movss    xmm3, dword ptr [rsp + 0x30]
0032D21A  subss    xmm3, dword ptr [rsp + 0x34]
0032D220  mulss    xmm3, xmm5
0032D224  addss    xmm3, dword ptr [rsp + 0x34]
0032D22A  call     0x3cc2f0  ; -> 003CC2F0 fn
0032D22F  movaps   xmm6, xmmword ptr [rsp + 0x50]
0032D234  movaps   xmm7, xmmword ptr [rsp + 0x40]
0032D239  add      rsp, 0x60
0032D23D  pop      rdi
0032D23E  pop      rsi
0032D23F  pop      rbx
0032D240  ret      
```

## 00333BB0 (78 B, extent 00333BB0-00333BFE)

Page context: "24A1D0' single call plus '0208EA88'-'0208EAA0'. Interior anchor '00246A35' (a '0024A1D0' call).  ## SWE2-EC7-58 update (2026-09-19) - '003A78A0'  '003A78A0' (168 B) is a bin-family body - '00333AC0'/'00333BB0'/'0036A190' plus '02EBEFA8'. Interior anchor '003A78CC' (a '0036A190' call).  ## SWE2-EC7-59 update (2026-09-19) - '00333AC0'  '00333AC0' (229 B) is a bin-family body - '0020E600'/'0020E620'/'003697F0'/'0046F370'. Interior anchor '"

```
00333BB0  mov      qword ptr [rsp + 8], rbx
00333BB5  push     rdi
00333BB6  sub      rsp, 0x20
00333BBA  xor      eax, eax
00333BBC  lea      rbx, [rcx + 0x2c]
00333BC0  mov      qword ptr [rcx + 0x18], rax
00333BC4  mov      qword ptr [rcx + 0x20], rax
00333BC8  and      byte ptr [rcx + 0x16], 0xfc
00333BCC  lea      edi, [rax + 0x1d]
00333BCF  mov      dword ptr [rcx + 0x28], eax
00333BD2  mov      qword ptr [rcx], rax
00333BD5  mov      word ptr [rcx + 8], ax
00333BD9  mov      byte ptr [rcx + 0x15], 1
00333BDD  nop      dword ptr [rax]
00333BE0  xor      ecx, ecx
00333BE2  call     0x20e620  ; -> 0020E620 fn
00333BE7  mov      dword ptr [rbx], eax
00333BE9  lea      rbx, [rbx + 4]
00333BED  sub      rdi, 1
00333BF1  jne      0x333be0  ; -> 00333BE0
00333BF3  mov      rbx, qword ptr [rsp + 0x30]
00333BF8  add      rsp, 0x20
00333BFC  pop      rdi
00333BFD  ret      
```

## 003A9100 (93 B, extent 003A9100-003A915D)

Page context: " client base — this page's own 'summoneffectdata' loader '003B53C0' and   '003B2310' complete through '0032E620'/'0032E400', and sixteen Presentation functions   ('003A7460', '003A78A0', '003A8020', '003A9100', '003A9C10', '0044A620', '0045FD50',   '0046F380', '004FF440', '00504350', '00524800', '00525D50', '00529200', '0052A130',   '0052ADF0', '0052D3B0', '0052E430') call the name-registering alloc '0036A190';   '002B0280' and '002D2DB"

```
003A9100  push     rbx
003A9102  sub      rsp, 0x20
003A9106  mov      rbx, qword ptr [rip + 0x2b15e7b]  ; -> 02EBEF88
003A910D  mov      ecx, 0x1c0
003A9112  call     0x36a190  ; -> 0036A190 fn
003A9117  mov      rcx, rax
003A911A  test     rax, rax
003A911D  jne      0x3a9125  ; -> 003A9125
003A911F  add      rsp, 0x20
003A9123  pop      rbx
003A9124  ret      
003A9125  xor      edx, edx
003A9127  mov      qword ptr [rax + 0x110], rdx
003A912E  mov      rax, qword ptr [rbx + 0x10]
003A9132  test     rax, rax
003A9135  je       0x3a913b  ; -> 003A913B
003A9137  mov      qword ptr [rax + 8], rcx
003A913B  mov      rax, qword ptr [rbx + 0x10]
003A913F  mov      qword ptr [rcx], rax
003A9142  mov      qword ptr [rcx + 8], rdx
003A9146  mov      qword ptr [rbx + 0x10], rcx
003A914A  cmp      qword ptr [rbx + 8], rdx
003A914E  jne      0x3a9154  ; -> 003A9154
003A9150  mov      qword ptr [rbx + 8], rcx
003A9154  mov      rax, rcx
003A9157  add      rsp, 0x20
003A915B  pop      rbx
003A915C  ret      
```
