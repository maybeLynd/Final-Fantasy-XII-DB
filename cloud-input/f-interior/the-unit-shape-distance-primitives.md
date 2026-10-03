# F-interior pack: `06-Movement-And-Navigation/the-unit-shape-distance-primitives.md`

Generated 2026-10-03 02:32 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-unit-shape-distance-primitives.json`.

Functions: 6. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: cd6bd7f58	SWE2-DATA consolidated publish: progress-report cluster (generation store, R3 semantics, DB_GOAL, me; 06c849caf	SWE2-DATA: restate batches 0930E and GR - SD-3, SD-23, SD-166, SD-181..SD-184, SD-190, SD-191, SD-19; inbox mentions: SWE2-ORACLE.md). OPUS read these before packing.

## 0022CF50 (381 B, extent 0022CF50-0022D0CD)

Page context: " planted callback 'q[ctx+0x28]'): subrecords route to FA0, plain edges route to E6D0 + CF50 | 815 B | | '0022E6D0' | E6D0 — signed projected distance '−L·num/den' against an edge's plane | 249 B | | '0022CF50' | CF50 — triangle winding test, three XPROD edge checks over the '0x908DE8' index table | 381 B | | '00380FA0' | FA0 — segment-vs-shape distance: both endpoints to local frame, type dispatch to a primitive, result mapped back, '−1"

```
0022CF50  mov      qword ptr [rsp + 8], rbx
0022CF55  mov      qword ptr [rsp + 0x10], rbp
0022CF5A  mov      qword ptr [rsp + 0x18], rsi
0022CF5F  push     rdi
0022CF60  push     r14
0022CF62  push     r15
0022CF64  sub      rsp, 0x70
0022CF68  movaps   xmmword ptr [rsp + 0x60], xmm6
0022CF6D  mov      rax, qword ptr [rip + 0x1d178bc]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0022CF74  xor      rax, rsp
0022CF77  mov      qword ptr [rsp + 0x50], rax
0022CF7C  movsx    rsi, dx
0022CF80  lea      rbx, [rip + 0x6dbe61]  ; -> 00908DE8
0022CF87  shl      rsi, 5
0022CF8B  lea      r15, [rip + 0x6dbe62]  ; -> 00908DF4
0022CF92  add      rsi, qword ptr [rcx + 0x10]
0022CF96  mov      rbp, r8
0022CF99  mov      r14, rcx
0022CF9C  xorps    xmm6, xmm6
0022CF9F  lea      rdi, [rsi + 0x10]
0022CFA3  nop      dword ptr [rax]
0022CFA7  nop      word ptr [rax + rax]
0022CFB0  movsxd   rax, dword ptr [rbx]
0022CFB3  lea      rcx, [rsp + 0x40]
0022CFB8  movsx    r8, word ptr [rdi]
0022CFBC  shl      r8, 4
0022CFC0  add      r8, qword ptr [r14 + 8]
0022CFC4  movsx    rdx, word ptr [rsi + rax*2 + 0x10]
0022CFCA  shl      rdx, 4
0022CFCE  add      rdx, qword ptr [r14 + 8]
0022CFD2  movss    xmm0, dword ptr [rdx]
0022CFD6  subss    xmm0, dword ptr [r8]
0022CFDB  movss    dword ptr [rsp + 0x30], xmm0
0022CFE1  movss    xmm1, dword ptr [rdx + 4]
0022CFE6  subss    xmm1, dword ptr [r8 + 4]
0022CFEC  movss    dword ptr [rsp + 0x34], xmm1
0022CFF2  movss    xmm0, dword ptr [rdx + 8]
0022CFF7  subss    xmm0, dword ptr [r8 + 8]
0022CFFD  movss    xmm1, dword ptr [rbp]
0022D002  movss    dword ptr [rsp + 0x38], xmm0
0022D008  movss    xmm0, dword ptr [rdx + 0xc]
0022D00D  lea      rdx, [rsp + 0x30]
0022D012  movss    dword ptr [rsp + 0x3c], xmm0
0022D018  subss    xmm1, dword ptr [r8]
0022D01D  movss    xmm0, dword ptr [rbp + 4]
0022D022  movss    dword ptr [rsp + 0x20], xmm1
0022D028  subss    xmm0, dword ptr [r8 + 4]
0022D02E  movss    xmm1, dword ptr [rbp + 8]
0022D033  movss    dword ptr [rsp + 0x24], xmm0
0022D039  subss    xmm1, dword ptr [r8 + 8]
0022D03F  movss    xmm0, dword ptr [rbp + 0xc]
0022D044  lea      r8, [rsp + 0x20]
0022D049  movss    dword ptr [rsp + 0x2c], xmm0
0022D04F  movss    dword ptr [rsp + 0x28], xmm1
0022D055  call     0x202e10  ; -> 00202E10 fn
0022D05A  movss    xmm2, dword ptr [rsp + 0x40]
0022D060  mulss    xmm2, dword ptr [rsi]
0022D064  movss    xmm0, dword ptr [rsp + 0x44]
0022D06A  mulss    xmm0, dword ptr [rsi + 4]
0022D06F  movss    xmm1, dword ptr [rsp + 0x48]
0022D075  mulss    xmm1, dword ptr [rsi + 8]
0022D07A  addss    xmm2, xmm0
0022D07E  addss    xmm2, xmm1
0022D082  comiss   xmm6, xmm2
0022D085  ja       0x22d09f  ; -> 0022D09F
0022D087  add      rdi, 2
0022D08B  add      rbx, 4
0022D08F  cmp      rbx, r15
0022D092  jl       0x22cfb0  ; -> 0022CFB0
0022D098  mov      eax, 1
0022D09D  jmp      0x22d0a1  ; -> 0022D0A1
0022D09F  xor      eax, eax
0022D0A1  mov      rcx, qword ptr [rsp + 0x50]
0022D0A6  xor      rcx, rsp
0022D0A9  call     0x808c40  ; -> 00808C40 fn
0022D0AE  lea      r11, [rsp + 0x70]
0022D0B3  mov      rbx, qword ptr [r11 + 0x20]
0022D0B7  mov      rbp, qword ptr [r11 + 0x28]
0022D0BB  mov      rsi, qword ptr [r11 + 0x30]
0022D0BF  movaps   xmm6, xmmword ptr [rsp + 0x60]
0022D0C4  mov      rsp, r11
0022D0C7  pop      r15
0022D0C9  pop      r14
0022D0CB  pop      rdi
0022D0CC  ret      
```

## 0022E6D0 (249 B, extent 0022E6D0-0022E7C9)

Page context: "  | VA | role | span | |---|---|---| | '0022D4B0' | D4B0 — the nav-grid edge-range scan (F430's planted callback 'q[ctx+0x28]'): subrecords route to FA0, plain edges route to E6D0 + CF50 | 815 B | | '0022E6D0' | E6D0 — signed projected distance '−L·num/den' against an edge's plane | 249 B | | '0022CF50' | CF50 — triangle winding test, three XPROD edge checks over the '0x908DE8' index table | 381 B | | '00380FA0' | FA0 — segment-vs-shape"

```
0022E6D0  push     rbx
0022E6D2  sub      rsp, 0x80
0022E6D9  mov      rax, qword ptr [r8 + 8]
0022E6DD  mov      rbx, qword ptr [r8]
0022E6E0  movaps   xmmword ptr [rsp + 0x70], xmm6
0022E6E5  movss    xmm6, dword ptr [rdx]
0022E6E9  movaps   xmmword ptr [rsp + 0x60], xmm7
0022E6EE  movaps   xmm0, xmm6
0022E6F1  movss    xmm7, dword ptr [rcx + 8]
0022E6F6  subss    xmm7, dword ptr [rax + 8]
0022E6FB  movaps   xmmword ptr [rsp + 0x50], xmm8
0022E701  movss    xmm8, dword ptr [rcx]
0022E706  subss    xmm8, dword ptr [rax]
0022E70B  movaps   xmmword ptr [rsp + 0x40], xmm9
0022E711  movss    xmm9, dword ptr [rdx + 8]
0022E717  mulss    xmm0, xmm6
0022E71B  movaps   xmm2, xmm9
0022E71F  movaps   xmmword ptr [rsp + 0x30], xmm10
0022E725  movss    xmm10, dword ptr [rdx + 4]
0022E72B  movaps   xmm1, xmm10
0022E72F  mulss    xmm2, xmm9
0022E734  mulss    xmm1, xmm10
0022E739  movaps   xmmword ptr [rsp + 0x20], xmm11
0022E73F  movss    xmm11, dword ptr [rcx + 4]
0022E745  subss    xmm11, dword ptr [rax + 4]
0022E74B  addss    xmm0, xmm1
0022E74F  addss    xmm0, xmm2
0022E753  call     0x861f14  ; -> 00861F14 fn
0022E758  mulss    xmm11, dword ptr [rbx + 4]
0022E75E  mulss    xmm10, dword ptr [rbx + 4]
0022E764  mulss    xmm8, dword ptr [rbx]
0022E769  mulss    xmm6, dword ptr [rbx]
0022E76D  mulss    xmm7, dword ptr [rbx + 8]
0022E772  addss    xmm11, xmm8
0022E777  mulss    xmm9, dword ptr [rbx + 8]
0022E77D  addss    xmm10, xmm6
0022E782  movaps   xmm6, xmmword ptr [rsp + 0x70]
0022E787  movaps   xmm8, xmmword ptr [rsp + 0x50]
0022E78D  addss    xmm11, xmm7
0022E792  movaps   xmm7, xmmword ptr [rsp + 0x60]
0022E797  addss    xmm10, xmm9
0022E79C  movaps   xmm9, xmmword ptr [rsp + 0x40]
0022E7A2  divss    xmm11, xmm10
0022E7A7  movaps   xmm10, xmmword ptr [rsp + 0x30]
0022E7AD  xorps    xmm11, xmmword ptr [rip + 0x1abd5eb]  ; -> 01CEBDA0 [f32x4 -0, -0, -0, -0]
0022E7B5  mulss    xmm0, xmm11
0022E7BA  movaps   xmm11, xmmword ptr [rsp + 0x20]
0022E7C0  add      rsp, 0x80
0022E7C7  pop      rbx
0022E7C8  ret      
```

## 0022EAC0 (1115 B, extent 0022EAC0-0022EF1B)

Page context: "002316B7' ('00231690') and '00232B22' ('002327D0') | '00230790', '00381D90', '003810B0', '0022E7D0' | | '0022DE60' | 1,240 B | planted by 'lea' at '00230EB1' **and '0023126A'**, both in '00230C10' | '0022EAC0', '003810B0', '00381D90' | | '00230790' | 688 B | '0022D7E0' | '00202C70', '00202D50', '00202D70', '00203170' | | '0022E7D0' | 740 B | '0022D7E0' | '00202E10' | | '003810B0' | 923 B | '0022D7E0', '0022DE60' | '00202B70', the box pr"

```
0022EAC0  mov      rax, rsp
0022EAC3  mov      qword ptr [rax + 8], rbx
0022EAC7  mov      qword ptr [rax + 0x10], rsi
0022EACB  mov      qword ptr [rax + 0x18], rdi
0022EACF  push     rbp
0022EAD0  push     r12
0022EAD2  push     r13
0022EAD4  push     r14
0022EAD6  push     r15
0022EAD8  lea      rbp, [rax - 0x38]
0022EADC  sub      rsp, 0x110
0022EAE3  movaps   xmmword ptr [rax - 0x68], xmm9
0022EAE8  movaps   xmmword ptr [rax - 0x78], xmm10
0022EAED  movaps   xmmword ptr [rax - 0x88], xmm11
0022EAF5  movaps   xmmword ptr [rax - 0xb8], xmm14
0022EAFD  movaps   xmmword ptr [rsp + 0x70], xmm15
0022EB03  mov      rax, qword ptr [rip + 0x1d15d26]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0022EB0A  xor      rax, rsp
0022EB0D  mov      qword ptr [rsp + 0x60], rax
0022EB12  mov      rax, qword ptr [rcx + 0x10]
0022EB16  mov      r10, r8
0022EB19  mov      dword ptr [r9 + 0xc], 0x3f800000
0022EB21  mov      rbx, r9
0022EB24  movsx    r13, dx
0022EB28  xorps    xmm14, xmm14
0022EB2C  mov      r12, r13
0022EB2F  mov      qword ptr [rsp + 0x28], r8
0022EB34  xor      r8d, r8d
0022EB37  shl      r12, 5
0022EB3B  mov      qword ptr [r9 + 4], r8
0022EB3F  mov      esi, r8d
0022EB42  mov      dword ptr [r9], r8d
0022EB45  mov      edi, r8d
0022EB48  shl      r13, 4
0022EB4C  movss    xmm9, dword ptr [r12 + rax]
0022EB52  lea      r14d, [r8 + 1]
0022EB56  movss    xmm10, dword ptr [r12 + rax + 4]
0022EB5D  movss    xmm11, dword ptr [r12 + rax + 8]
0022EB64  movss    xmm15, dword ptr [r12 + rax + 0xc]
0022EB6B  lea      r15, [r13*2 + 0x10]
0022EB73  mov      qword ptr [rsp + 0x20], rcx
0022EB78  nop      dword ptr [rax + rax]
0022EB80  mov      r8, qword ptr [rcx + 0x10]
0022EB84  mov      eax, 0x55555556
0022EB89  mov      r9, qword ptr [rcx + 8]
0022EB8D  mov      ecx, r14d
0022EB90  imul     r14d
0022EB93  mov      eax, edx
0022EB95  shr      eax, 0x1f
0022EB98  add      edx, eax
0022EB9A  lea      eax, [rdx + rdx*2]
0022EB9D  sub      ecx, eax
0022EB9F  lea      rdx, [rsp + 0x30]
0022EBA4  movsxd   rax, ecx
0022EBA7  add      rax, r13
0022EBAA  movsx    rcx, word ptr [r8 + rax*2 + 0x10]
0022EBB0  movsx    rax, word ptr [r8 + r15]
0022EBB5  lea      r8, [rsp + 0x40]
0022EBBA  shl      rcx, 4
0022EBBE  add      rcx, r9
0022EBC1  shl      rax, 4
0022EBC5  add      rax, r9
0022EBC8  movss    xmm0, dword ptr [rcx]
0022EBCC  subss    xmm0, dword ptr [rax]
0022EBD0  movss    dword ptr [rsp + 0x30], xmm0
0022EBD6  movss    xmm1, dword ptr [rcx + 4]
0022EBDB  subss    xmm1, dword ptr [rax + 4]
0022EBE0  movss    dword ptr [rsp + 0x34], xmm1
0022EBE6  movss    xmm0, dword ptr [rcx + 8]
0022EBEB  subss    xmm0, dword ptr [rax + 8]
0022EBF0  movss    xmm1, dword ptr [r10]
0022EBF5  movss    dword ptr [rsp + 0x38], xmm0
0022EBFB  movss    xmm0, dword ptr [rcx + 0xc]
0022EC00  lea      rcx, [rsp + 0x50]
0022EC05  movss    dword ptr [rsp + 0x3c], xmm0
0022EC0B  subss    xmm1, dword ptr [rax]
0022EC0F  movss    xmm0, dword ptr [r10 + 4]
0022EC15  movss    dword ptr [rsp + 0x40], xmm1
0022EC1B  subss    xmm0, dword ptr [rax + 4]
0022EC20  movss    xmm1, dword ptr [r10 + 8]
0022EC26  movss    dword ptr [rsp + 0x44], xmm0
0022EC2C  subss    xmm1, dword ptr [rax + 8]
0022EC31  movss    xmm0, dword ptr [r10 + 0xc]
0022EC37  movss    dword ptr [rsp + 0x4c], xmm0
0022EC3D  movss    dword ptr [rsp + 0x48], xmm1
0022EC43  call     0x202e10  ; -> 00202E10 fn
0022EC48  movaps   xmm2, xmm10
0022EC4C  movaps   xmm0, xmm9
0022EC50  mulss    xmm2, dword ptr [rsp + 0x54]
0022EC56  movaps   xmm1, xmm11
0022EC5A  mulss    xmm0, dword ptr [rsp + 0x50]
0022EC60  mulss    xmm1, dword ptr [rsp + 0x58]
0022EC66  addss    xmm2, xmm0
0022EC6A  addss    xmm2, xmm1
0022EC6E  comiss   xmm14, xmm2
0022EC72  ja       0x22ec99  ; -> 0022EC99
0022EC74  mov      rcx, qword ptr [rsp + 0x20]
0022EC79  inc      esi
0022EC7B  mov      r10, qword ptr [rsp + 0x28]
0022EC80  inc      r14d
0022EC83  inc      rdi
0022EC86  add      r15, 2
0022EC8A  cmp      rdi, 3
0022EC8E  jl       0x22eb80  ; -> 0022EB80
0022EC94  jmp      0x22eecb  ; -> 0022EECB
0022EC99  mov      rdi, qword ptr [rsp + 0x20]
0022EC9E  mov      rdi, qword ptr [rdi + 0x10]
0022ECA2  test     dword ptr [rdi + r12 + 0x1c], 0x400
0022ECAB  je       0x22ecb9  ; -> 0022ECB9
0022ECAD  cmp      esi, 2
0022ECB0  jne      0x22ecb9  ; -> 0022ECB9
0022ECB2  xor      eax, eax
0022ECB4  jmp      0x22eed0  ; -> 0022EED0
0022ECB9  movaps   xmmword ptr [rsp + 0x100], xmm6
0022ECC1  movss    xmm6, dword ptr [rsp + 0x34]
0022ECC7  movaps   xmmword ptr [rsp + 0xf0], xmm7
0022ECCF  movaps   xmm0, xmm6
0022ECD2  movss    xmm7, dword ptr [rsp + 0x30]
0022ECD8  mulss    xmm0, xmm6
0022ECDC  movaps   xmm1, xmm7
0022ECDF  movsxd   rax, esi
0022ECE2  movaps   xmmword ptr [rsp + 0xe0], xmm8
0022ECEB  add      rax, r13
0022ECEE  movss    xmm8, dword ptr [rsp + 0x38]
0022ECF5  mulss    xmm1, xmm7
0022ECF9  movaps   xmm2, xmm8
0022ECFD  movzx    esi, word ptr [rdi + rax*2 + 0x16]
0022ED02  mulss    xmm2, xmm8
0022ED07  addss    xmm0, xmm1
0022ED0B  movaps   xmmword ptr [rsp + 0xa0], xmm12
0022ED14  movaps   xmmword ptr [rsp + 0x90], xmm13
0022ED1D  addss    xmm0, xmm2
0022ED21  call     0x861f14  ; -> 00861F14 fn
0022ED26  movss    xmm12, dword ptr [rip + 0x1abce79]  ; -> 01CEBBA8 [f32 1]
0022ED2F  movaps   xmm13, xmm0
0022ED33  movss    xmm5, dword ptr [rsp + 0x40]
0022ED39  movaps   xmm1, xmm12
0022ED3D  divss    xmm1, xmm13
0022ED42  movss    dword ptr [rbx], xmm5
0022ED46  movaps   xmm3, xmm7
0022ED49  mulss    xmm3, xmm1
0022ED4D  movaps   xmm2, xmm8
0022ED51  mulss    xmm2, xmm1
0022ED55  movaps   xmm4, xmm6
0022ED58  mulss    xmm4, xmm1
0022ED5C  movss    xmm1, dword ptr [rsp + 0x44]
0022ED62  mulss    xmm3, xmm5
0022ED66  mulss    xmm4, xmm1
0022ED6A  movss    dword ptr [rbx + 4], xmm1
0022ED6F  addss    xmm4, xmm3
0022ED73  movss    xmm3, dword ptr [rsp + 0x48]
0022ED79  mulss    xmm2, xmm3
0022ED7D  movss    dword ptr [rbx + 8], xmm3
0022ED82  addss    xmm4, xmm2
0022ED86  movss    xmm2, dword ptr [rsp + 0x4c]
0022ED8C  movss    dword ptr [rbx + 0xc], xmm2
0022ED91  comiss   xmm4, xmm14
0022ED95  jbe      0x22edf3  ; -> 0022EDF3
0022ED97  comiss   xmm13, xmm4
0022ED9B  jbe      0x22edd3  ; -> 0022EDD3
0022ED9D  movaps   xmm0, xmm12
0022EDA1  mulss    xmm7, xmm4
0022EDA5  divss    xmm0, xmm13
0022EDAA  mulss    xmm6, xmm4
0022EDAE  mulss    xmm8, xmm4
0022EDB3  mulss    xmm7, xmm0
0022EDB7  mulss    xmm6, xmm0
0022EDBB  mulss    xmm8, xmm0
0022EDC0  movss    dword ptr [rsp + 0x30], xmm7
0022EDC6  movss    dword ptr [rsp + 0x34], xmm6
0022EDCC  movss    dword ptr [rsp + 0x38], xmm8
0022EDD3  subss    xmm5, xmm7
0022EDD7  movss    dword ptr [rbx + 0xc], xmm2
0022EDDC  subss    xmm1, xmm6
0022EDE0  subss    xmm3, xmm8
0022EDE5  movss    dword ptr [rbx], xmm5
0022EDE9  movss    dword ptr [rbx + 4], xmm1
0022EDEE  movss    dword ptr [rbx + 8], xmm3
0022EDF3  movaps   xmm13, xmmword ptr [rsp + 0x90]
0022EDFC  movaps   xmm8, xmmword ptr [rsp + 0xe0]
0022EE05  movaps   xmm7, xmmword ptr [rsp + 0xf0]
0022EE0D  test     si, si
0022EE10  js       0x22ee2e  ; -> 0022EE2E
0022EE12  movsx    rax, si
0022EE16  shl      rax, 5
0022EE1A  addss    xmm9, dword ptr [rax + rdi]
0022EE20  addss    xmm10, dword ptr [rax + rdi + 4]
0022EE27  addss    xmm11, dword ptr [rax + rdi + 8]
0022EE2E  movss    xmm1, dword ptr [rbx + 4]
0022EE33  movss    xmm0, dword ptr [rbx]
0022EE37  movss    xmm2, dword ptr [rbx + 8]
0022EE3C  mulss    xmm0, xmm0
0022EE40  mulss    xmm1, xmm1
0022EE44  mulss    xmm2, xmm2
0022EE48  addss    xmm0, xmm1
0022EE4C  addss    xmm0, xmm2
0022EE50  call     0x861f14  ; -> 00861F14 fn
0022EE55  movaps   xmm6, xmm0
0022EE58  movaps   xmm1, xmm9
0022EE5C  movaps   xmm0, xmm10
0022EE60  mulss    xmm1, xmm9
0022EE65  mulss    xmm0, xmm10
0022EE6A  movaps   xmm2, xmm11
0022EE6E  mulss    xmm2, xmm11
0022EE73  addss    xmm0, xmm1
0022EE77  addss    xmm0, xmm2
0022EE7B  call     0x861f14  ; -> 00861F14 fn
0022EE80  divss    xmm12, xmm0
0022EE85  mulss    xmm9, xmm6
0022EE8A  mulss    xmm10, xmm6
0022EE8F  mulss    xmm11, xmm6
0022EE94  movaps   xmm6, xmmword ptr [rsp + 0x100]
0022EE9C  mulss    xmm9, xmm12
0022EEA1  mulss    xmm10, xmm12
0022EEA6  mulss    xmm11, xmm12
0022EEAB  movaps   xmm12, xmmword ptr [rsp + 0xa0]
0022EEB4  movss    dword ptr [rbx], xmm9
0022EEB9  movss    dword ptr [rbx + 4], xmm10
0022EEBF  movss    dword ptr [rbx + 8], xmm11
0022EEC5  movss    dword ptr [rbx + 0xc], xmm15
0022EECB  mov      eax, 1
0022EED0  mov      rcx, qword ptr [rsp + 0x60]
0022EED5  xor      rcx, rsp
0022EED8  call     0x808c40  ; -> 00808C40 fn
0022EEDD  lea      r11, [rsp + 0x110]
0022EEE5  mov      rbx, qword ptr [r11 + 0x30]
0022EEE9  mov      rsi, qword ptr [r11 + 0x38]
0022EEED  mov      rdi, qword ptr [r11 + 0x40]
0022EEF1  movaps   xmm9, xmmword ptr [r11 - 0x40]
0022EEF6  movaps   xmm10, xmmword ptr [r11 - 0x50]
0022EEFB  movaps   xmm11, xmmword ptr [r11 - 0x60]
0022EF00  movaps   xmm14, xmmword ptr [r11 - 0x90]
0022EF08  movaps   xmm15, xmmword ptr [rsp + 0x70]
0022EF0E  mov      rsp, r11
0022EF11  pop      r15
0022EF13  pop      r14
0022EF15  pop      r13
0022EF17  pop      r12
0022EF19  pop      rbp
0022EF1A  ret      
```

## 00381630 (1168 B, extent 00381630-00381AC0)

Page context: "both endpoints to local frame, type dispatch to a primitive, result mapped back, '−1.0' on no-hit | 263 B | | '00381AC0' | sphere primitive — unit-sphere surface solve via 'acosf'/'sinf' | 708 B | | '00381630' | cylinder primitive — top/bottom cap-plane tests plus the XZ-radial side solve | 1,168 B | | '00381450' | box primitive — six-face unit-cube test over the '0xD11200' face table, margin '1.001' | 477 B | | '00381EB0' | EB0 — point"

```
00381630  mov      rax, rsp
00381633  mov      qword ptr [rax + 0x18], rbx
00381637  push     rbp
00381638  push     rsi
00381639  push     rdi
0038163A  lea      rbp, [rax - 0x5f]
0038163E  sub      rsp, 0xf0
00381645  movaps   xmmword ptr [rax - 0x28], xmm6
00381649  movaps   xmmword ptr [rax - 0x38], xmm7
0038164D  movaps   xmmword ptr [rax - 0x48], xmm8
00381652  movaps   xmmword ptr [rax - 0x58], xmm9
00381657  movaps   xmmword ptr [rax - 0x68], xmm10
0038165C  movaps   xmmword ptr [rax - 0x78], xmm11
00381661  movaps   xmmword ptr [rax - 0x88], xmm12
00381669  movaps   xmmword ptr [rsp + 0x70], xmm13
0038166F  mov      rax, qword ptr [rip + 0x1bc31ba]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00381676  xor      rax, rsp
00381679  mov      qword ptr [rbp - 0x59], rax
0038167D  movss    xmm7, dword ptr [r8]
00381682  mov      rsi, r8
00381685  subss    xmm7, dword ptr [rdx]
00381689  movss    xmm1, dword ptr [r8 + 0xc]
0038168F  mov      rdi, rdx
00381692  movss    xmm8, dword ptr [r8 + 8]
00381698  mov      rbx, rcx
0038169B  subss    xmm8, dword ptr [rdx + 8]
003816A1  movss    xmm10, dword ptr [r8 + 4]
003816A7  movss    xmm6, dword ptr [rdx + 4]
003816AC  movaps   xmm0, xmm10
003816B0  subss    xmm0, xmm6
003816B4  movss    dword ptr [rbp - 0x7d], xmm1
003816B9  movaps   xmm1, xmm7
003816BC  movss    dword ptr [rsp + 0x20], xmm7
003816C2  mulss    xmm1, xmm7
003816C6  movaps   xmm2, xmm8
003816CA  mulss    xmm2, xmm8
003816CF  movss    dword ptr [rsp + 0x24], xmm0
003816D5  mulss    xmm0, xmm0
003816D9  movss    dword ptr [rsp + 0x28], xmm8
003816E0  addss    xmm0, xmm1
003816E4  addss    xmm0, xmm2
003816E8  call     0x861f14  ; -> 00861F14 fn
003816ED  movss    xmm9, dword ptr [rip + 0x196a4b2]  ; -> 01CEBBA8 [f32 1]
003816F6  movaps   xmm13, xmm0
003816FA  comiss   xmm6, xmm9
003816FE  xorps    xmm11, xmm11
00381702  jbe      0x3817cf  ; -> 003817CF
00381708  comiss   xmm9, xmm10
0038170C  jbe      0x3818a8  ; -> 003818A8
00381712  lea      r9, [rip + 0x98fb67]  ; -> 00D11280
00381719  mov      rcx, rdi
0038171C  lea      r8, [rip + 0x98fb5d]  ; -> 00D11280
00381723  lea      rdx, [rsp + 0x20]
00381728  call     0x46bfa0  ; -> 0046BFA0 fn
0038172D  comiss   xmm0, xmm11
00381731  jbe      0x3817c2  ; -> 003817C2
00381737  comiss   xmm13, xmm0
0038173B  jbe      0x3817c2  ; -> 003817C2
00381741  movss    xmm7, dword ptr [rsp + 0x20]
00381747  movss    xmm8, dword ptr [rsp + 0x28]
0038174E  movaps   xmm6, xmm7
00381751  movss    xmm12, dword ptr [rsp + 0x24]
00381758  movaps   xmm10, xmm8
0038175C  divss    xmm0, xmm13
00381761  mulss    xmm6, xmm0
00381765  mulss    xmm10, xmm0
0038176A  addss    xmm6, dword ptr [rdi]
0038176E  mulss    xmm12, xmm0
00381773  addss    xmm10, dword ptr [rdi + 8]
00381779  addss    xmm12, dword ptr [rdi + 4]
0038177F  movaps   xmm1, xmm6
00381782  mulss    xmm1, xmm6
00381786  movaps   xmm0, xmm10
0038178A  mulss    xmm0, xmm10
0038178F  addss    xmm0, xmm1
00381793  call     0x861f14  ; -> 00861F14 fn
00381798  comiss   xmm9, xmm0
0038179C  jbe      0x3817cf  ; -> 003817CF
0038179E  movss    xmm0, dword ptr [rbp - 0x7d]
003817A3  mov      eax, 1
003817A8  movss    dword ptr [rbx], xmm6
003817AC  movss    dword ptr [rbx + 4], xmm12
003817B2  movss    dword ptr [rbx + 8], xmm10
003817B8  movss    dword ptr [rbx + 0xc], xmm0
003817BD  jmp      0x381a79  ; -> 00381A79
003817C2  movss    xmm8, dword ptr [rsp + 0x28]
003817C9  movss    xmm7, dword ptr [rsp + 0x20]
003817CF  movaps   xmmword ptr [rsp + 0x60], xmm14
003817D5  movss    xmm14, dword ptr [rip + 0x196a4be]  ; -> 01CEBC9C [f32 -1]
003817DE  comiss   xmm14, dword ptr [rdi + 4]
003817E3  jbe      0x3818bc  ; -> 003818BC
003817E9  movss    xmm0, dword ptr [rsi + 4]
003817EE  comiss   xmm0, xmm14
003817F2  jbe      0x381a71  ; -> 00381A71
003817F8  lea      r9, [rip + 0x98fa91]  ; -> 00D11290
003817FF  mov      rcx, rdi
00381802  lea      r8, [rip + 0x98fa87]  ; -> 00D11290
00381809  lea      rdx, [rsp + 0x20]
0038180E  call     0x46bfa0  ; -> 0046BFA0 fn
00381813  comiss   xmm0, xmm11
00381817  jbe      0x3818af  ; -> 003818AF
0038181D  comiss   xmm13, xmm0
00381821  jbe      0x3818af  ; -> 003818AF
00381827  movss    xmm7, dword ptr [rsp + 0x20]
0038182D  movss    xmm8, dword ptr [rsp + 0x28]
00381834  movaps   xmm6, xmm7
00381837  movss    xmm12, dword ptr [rsp + 0x24]
0038183E  movaps   xmm10, xmm8
00381842  divss    xmm0, xmm13
00381847  mulss    xmm6, xmm0
0038184B  mulss    xmm10, xmm0
00381850  addss    xmm6, dword ptr [rdi]
00381854  mulss    xmm12, xmm0
00381859  addss    xmm10, dword ptr [rdi + 8]
0038185F  addss    xmm12, dword ptr [rdi + 4]
00381865  movaps   xmm1, xmm6
00381868  mulss    xmm1, xmm6
0038186C  movaps   xmm0, xmm10
00381870  mulss    xmm0, xmm10
00381875  addss    xmm0, xmm1
00381879  call     0x861f14  ; -> 00861F14 fn
0038187E  comiss   xmm9, xmm0
00381882  jbe      0x3818bc  ; -> 003818BC
00381884  movss    xmm0, dword ptr [rbp - 0x7d]
00381889  movss    dword ptr [rbx], xmm6
0038188D  movss    dword ptr [rbx + 4], xmm12
00381893  movss    dword ptr [rbx + 8], xmm10
00381899  movss    dword ptr [rbx + 0xc], xmm0
0038189E  mov      eax, 1
003818A3  jmp      0x381a73  ; -> 00381A73
003818A8  xor      eax, eax
003818AA  jmp      0x381a79  ; -> 00381A79
003818AF  movss    xmm8, dword ptr [rsp + 0x28]
003818B6  movss    xmm7, dword ptr [rsp + 0x20]
003818BC  movss    xmm0, dword ptr [rdi]
003818C0  movaps   xmm10, xmm7
003818C4  movss    xmm1, dword ptr [rdi + 8]
003818C9  movaps   xmm12, xmm8
003818CD  movss    dword ptr [rbp - 0x79], xmm0
003818D2  mulss    xmm10, xmm7
003818D7  mov      dword ptr [rbp - 0x75], 0
003818DE  mulss    xmm12, xmm8
003818E3  mov      dword ptr [rbp - 0x6d], 0x3f800000
003818EA  movaps   xmm0, xmm10
003818EE  movss    dword ptr [rbp - 0x71], xmm1
003818F3  addss    xmm0, xmm11
003818F8  addss    xmm0, xmm12
003818FD  call     0x861f14  ; -> 00861F14 fn
00381902  movss    xmm1, dword ptr [rip + 0x587506]  ; -> 00908E10 [u32 0x358637BD]
0038190A  comiss   xmm1, xmm0
0038190D  jbe      0x381915  ; -> 00381915
0038190F  movaps   xmm2, xmm11
00381913  jmp      0x38191d  ; -> 0038191D
00381915  movaps   xmm2, xmm9
00381919  divss    xmm2, xmm0
0038191D  movaps   xmm1, xmm2
00381920  mov      dword ptr [rbp - 0x5d], 0x3f800000
00381927  mulss    xmm1, xmm11
0038192C  lea      r8, [rbp - 0x79]
00381930  lea      rdx, [rbp - 0x69]
00381934  movaps   xmm0, xmm7
00381937  lea      rcx, [rip + 0x98f932]  ; -> 00D11270
0038193E  mulss    xmm0, xmm2
00381942  movss    dword ptr [rbp - 0x65], xmm1
00381947  movaps   xmm1, xmm8
0038194B  mulss    xmm1, xmm2
0038194F  movss    dword ptr [rbp - 0x69], xmm0
00381954  movss    dword ptr [rbp - 0x61], xmm1
00381959  call     0x46bf60  ; -> 0046BF60 fn
0038195E  addss    xmm10, xmm11
00381963  movaps   xmm6, xmm0
00381966  addss    xmm10, xmm12
0038196B  movaps   xmm0, xmm10
0038196F  call     0x861f14  ; -> 00861F14 fn
00381974  movaps   xmm12, xmm0
00381978  movaps   xmm10, xmm6
0038197C  divss    xmm10, xmm12
00381981  movaps   xmm0, xmm10
00381985  mulss    xmm7, xmm10
0038198A  mulss    xmm0, xmm11
0038198F  addss    xmm7, dword ptr [rbp - 0x79]
00381994  mulss    xmm8, xmm10
00381999  addss    xmm0, dword ptr [rbp - 0x75]
0038199E  addss    xmm8, dword ptr [rbp - 0x71]
003819A4  mulss    xmm7, xmm7
003819A8  mulss    xmm0, xmm0
003819AC  mulss    xmm8, xmm8
003819B1  addss    xmm0, xmm7
003819B5  addss    xmm0, xmm8
003819BA  call     0x861f14  ; -> 00861F14 fn
003819BF  mov      rcx, rdi
003819C2  movaps   xmm7, xmm0
003819C5  call     0x382020  ; -> 00382020 fn
003819CA  test     eax, eax
003819CC  jne      0x3819f4  ; -> 003819F4
003819CE  mov      rcx, rsi
003819D1  call     0x382020  ; -> 00382020 fn
003819D6  test     eax, eax
003819D8  jne      0x3819f4  ; -> 003819F4
003819DA  comiss   xmm7, xmm9
003819DE  ja       0x381a71  ; -> 00381A71
003819E4  comiss   xmm11, xmm10
003819E8  ja       0x381a71  ; -> 00381A71
003819EE  comiss   xmm10, xmm9
003819F2  ja       0x381a71  ; -> 00381A71
003819F4  movaps   xmm0, xmm7
003819F7  call     0x861f56  ; -> 00861F56 fn
003819FC  call     0x861f0e  ; -> 00861F0E fn
00381A01  movss    xmm2, dword ptr [rsp + 0x20]
00381A07  subss    xmm6, xmm0
00381A0B  movss    xmm0, dword ptr [rbp - 0x7d]
00381A10  movss    xmm3, dword ptr [rsp + 0x24]
00381A16  movss    xmm1, dword ptr [rsp + 0x28]
00381A1C  movss    dword ptr [rbx + 0xc], xmm0
00381A21  divss    xmm6, xmm12
00381A26  mulss    xmm2, xmm6
00381A2A  mulss    xmm3, xmm6
00381A2E  movss    dword ptr [rbx], xmm2
00381A32  mulss    xmm1, xmm6
00381A36  movss    dword ptr [rbx + 4], xmm3
00381A3B  movss    dword ptr [rbx + 8], xmm1
00381A40  addss    xmm2, dword ptr [rdi]
00381A44  movss    dword ptr [rbx], xmm2
00381A48  addss    xmm3, dword ptr [rdi + 4]
00381A4D  comiss   xmm3, xmm9
00381A51  movss    dword ptr [rbx + 4], xmm3
00381A56  addss    xmm1, dword ptr [rdi + 8]
00381A5B  movss    dword ptr [rbx + 0xc], xmm0
00381A60  movss    dword ptr [rbx + 8], xmm1
00381A65  ja       0x381a71  ; -> 00381A71
00381A67  comiss   xmm14, xmm3
00381A6B  jbe      0x38189e  ; -> 0038189E
00381A71  xor      eax, eax
00381A73  movaps   xmm14, xmmword ptr [rsp + 0x60]
00381A79  mov      rcx, qword ptr [rbp - 0x59]
00381A7D  xor      rcx, rsp
00381A80  call     0x808c40  ; -> 00808C40 fn
00381A85  lea      r11, [rsp + 0xf0]
00381A8D  mov      rbx, qword ptr [r11 + 0x30]
00381A91  movaps   xmm6, xmmword ptr [r11 - 0x10]
00381A96  movaps   xmm7, xmmword ptr [r11 - 0x20]
00381A9B  movaps   xmm8, xmmword ptr [r11 - 0x30]
00381AA0  movaps   xmm9, xmmword ptr [r11 - 0x40]
00381AA5  movaps   xmm10, xmmword ptr [r11 - 0x50]
00381AAA  movaps   xmm11, xmmword ptr [r11 - 0x60]
00381AAF  movaps   xmm12, xmmword ptr [r11 - 0x70]
00381AB4  movaps   xmm13, xmmword ptr [r11 - 0x80]
00381AB9  mov      rsp, r11
00381ABC  pop      rdi
00381ABD  pop      rsi
00381ABE  pop      rbp
00381ABF  ret      
```

## 00381AC0 (708 B, extent 00381AC0-00381D84)

Page context: "ver the '0x908DE8' index table | 381 B | | '00380FA0' | FA0 — segment-vs-shape distance: both endpoints to local frame, type dispatch to a primitive, result mapped back, '−1.0' on no-hit | 263 B | | '00381AC0' | sphere primitive — unit-sphere surface solve via 'acosf'/'sinf' | 708 B | | '00381630' | cylinder primitive — top/bottom cap-plane tests plus the XZ-radial side solve | 1,168 B | | '00381450' | box primitive — six-face unit-cube"

```
00381AC0  mov      rax, rsp
00381AC3  mov      qword ptr [rax + 0x18], rbx
00381AC7  mov      qword ptr [rax + 0x20], rsi
00381ACB  push     rdi
00381ACC  sub      rsp, 0xf0
00381AD3  movaps   xmmword ptr [rax - 0x18], xmm6
00381AD7  movaps   xmmword ptr [rax - 0x28], xmm7
00381ADB  movaps   xmmword ptr [rax - 0x38], xmm8
00381AE0  movaps   xmmword ptr [rax - 0x48], xmm9
00381AE5  movaps   xmmword ptr [rax - 0x58], xmm10
00381AEA  movaps   xmmword ptr [rax - 0x68], xmm11
00381AEF  movaps   xmmword ptr [rax - 0x78], xmm12
00381AF4  movaps   xmmword ptr [rsp + 0x70], xmm13
00381AFA  movaps   xmmword ptr [rsp + 0x60], xmm14
00381B00  movaps   xmmword ptr [rsp + 0x50], xmm15
00381B06  mov      rax, qword ptr [rip + 0x1bc2d23]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00381B0D  xor      rax, rsp
00381B10  mov      qword ptr [rsp + 0x40], rax
00381B15  movss    xmm6, dword ptr [r8]
00381B1A  mov      rbx, r8
00381B1D  movss    xmm7, dword ptr [r8 + 4]
00381B23  mov      rsi, rdx
00381B26  subss    xmm6, dword ptr [rdx]
00381B2A  subss    xmm7, dword ptr [rdx + 4]
00381B2F  movss    xmm8, dword ptr [r8 + 8]
00381B35  mov      rdi, rcx
00381B38  subss    xmm8, dword ptr [rdx + 8]
00381B3E  movss    xmm11, dword ptr [r8 + 0xc]
00381B44  movaps   xmm1, xmm6
00381B47  movaps   xmm0, xmm7
00381B4A  mulss    xmm1, xmm6
00381B4E  mulss    xmm0, xmm7
00381B52  movaps   xmm2, xmm8
00381B56  mulss    xmm2, xmm8
00381B5B  addss    xmm0, xmm1
00381B5F  addss    xmm0, xmm2
00381B63  call     0x861f14  ; -> 00861F14 fn
00381B68  movss    xmm1, dword ptr [rip + 0x5872a0]  ; -> 00908E10 [u32 0x358637BD]
00381B70  movaps   xmm10, xmm0
00381B74  comiss   xmm1, xmm10
00381B78  movss    xmm9, dword ptr [rip + 0x196a027]  ; -> 01CEBBA8 [f32 1]
00381B81  jbe      0x381b88  ; -> 00381B88
00381B83  xorps    xmm1, xmm1
00381B86  jmp      0x381b91  ; -> 00381B91
00381B88  movaps   xmm1, xmm9
00381B8C  divss    xmm1, xmm10
00381B91  mulss    xmm6, xmm1
00381B95  lea      rdx, [rsp + 0x30]
00381B9A  lea      rcx, [rip + 0x98f6bf]  ; -> 00D11260
00381BA1  mov      r8, rsi
00381BA4  mulss    xmm7, xmm1
00381BA8  mulss    xmm8, xmm1
00381BAD  movss    dword ptr [rsp + 0x30], xmm6
00381BB3  movss    dword ptr [rsp + 0x34], xmm7
00381BB9  movss    dword ptr [rsp + 0x38], xmm8
00381BC0  movss    dword ptr [rsp + 0x3c], xmm11
00381BC7  call     0x46bf60  ; -> 0046BF60 fn
00381BCC  movss    xmm13, dword ptr [rsp + 0x30]
00381BD3  movaps   xmm1, xmm0
00381BD6  movss    xmm14, dword ptr [rsp + 0x34]
00381BDD  movss    xmm15, dword ptr [rsp + 0x38]
00381BE4  movaps   xmm11, xmm14
00381BE8  movss    xmm6, dword ptr [rsi]
00381BEC  movaps   xmm12, xmm15
00381BF0  movss    xmm8, dword ptr [rsi + 4]
00381BF6  movss    xmm7, dword ptr [rsi + 8]
00381BFB  divss    xmm1, xmm10
00381C00  mulss    xmm12, xmm0
00381C05  movaps   xmm10, xmm13
00381C09  mulss    xmm10, xmm0
00381C0E  mulss    xmm11, xmm0
00381C13  addss    xmm12, xmm7
00381C18  movss    dword ptr [rsp + 0x24], xmm1
00381C1E  addss    xmm10, xmm6
00381C23  addss    xmm11, xmm8
00381C28  movaps   xmm2, xmm12
00381C2C  mulss    xmm2, xmm12
00381C31  movaps   xmm1, xmm10
00381C35  movaps   xmm0, xmm11
00381C39  mulss    xmm1, xmm10
00381C3E  mulss    xmm0, xmm11
00381C43  addss    xmm0, xmm1
00381C47  addss    xmm0, xmm2
00381C4B  call     0x861f14  ; -> 00861F14 fn
00381C50  mulss    xmm8, xmm8
00381C55  movss    dword ptr [rsp + 0x20], xmm0
00381C5B  mulss    xmm6, xmm6
00381C5F  mulss    xmm7, xmm7
00381C63  addss    xmm8, xmm6
00381C68  addss    xmm8, xmm7
00381C6D  movaps   xmm0, xmm8
00381C71  call     0x861f14  ; -> 00861F14 fn
00381C76  xor      esi, esi
00381C78  comiss   xmm9, xmm0
00381C7C  mov      eax, esi
00381C7E  seta     al
00381C81  test     eax, eax
00381C83  jne      0x381cdc  ; -> 00381CDC
00381C85  movss    xmm1, dword ptr [rbx + 4]
00381C8A  movss    xmm0, dword ptr [rbx]
00381C8E  movss    xmm2, dword ptr [rbx + 8]
00381C93  mulss    xmm0, xmm0
00381C97  mulss    xmm1, xmm1
00381C9B  mulss    xmm2, xmm2
00381C9F  addss    xmm0, xmm1
00381CA3  addss    xmm0, xmm2
00381CA7  call     0x861f14  ; -> 00861F14 fn
00381CAC  movss    xmm2, dword ptr [rsp + 0x20]
00381CB2  comiss   xmm9, xmm0
00381CB6  seta     sil
00381CBA  test     esi, esi
00381CBC  jne      0x381ce2  ; -> 00381CE2
00381CBE  comiss   xmm2, xmm9
00381CC2  ja       0x381cd8  ; -> 00381CD8
00381CC4  movss    xmm1, dword ptr [rsp + 0x24]
00381CCA  xorps    xmm0, xmm0
00381CCD  comiss   xmm0, xmm1
00381CD0  ja       0x381cd8  ; -> 00381CD8
00381CD2  comiss   xmm1, xmm9
00381CD6  jbe      0x381ce2  ; -> 00381CE2
00381CD8  xor      eax, eax
00381CDA  jmp      0x381d2e  ; -> 00381D2E
00381CDC  movss    xmm2, dword ptr [rsp + 0x20]
00381CE2  movaps   xmm0, xmm2
00381CE5  call     0x861f56  ; -> 00861F56 fn
00381CEA  call     0x861f0e  ; -> 00861F0E fn
00381CEF  mulss    xmm13, xmm0
00381CF4  mov      eax, 1
00381CF9  mulss    xmm14, xmm0
00381CFE  mulss    xmm15, xmm0
00381D03  subss    xmm10, xmm13
00381D08  movss    xmm0, dword ptr [rsp + 0x3c]
00381D0E  subss    xmm11, xmm14
00381D13  movss    dword ptr [rdi + 0xc], xmm0
00381D18  subss    xmm12, xmm15
00381D1D  movss    dword ptr [rdi], xmm10
00381D22  movss    dword ptr [rdi + 4], xmm11
00381D28  movss    dword ptr [rdi + 8], xmm12
00381D2E  mov      rcx, qword ptr [rsp + 0x40]
00381D33  xor      rcx, rsp
00381D36  call     0x808c40  ; -> 00808C40 fn
00381D3B  lea      r11, [rsp + 0xf0]
00381D43  mov      rbx, qword ptr [r11 + 0x20]
00381D47  mov      rsi, qword ptr [r11 + 0x28]
00381D4B  movaps   xmm6, xmmword ptr [r11 - 0x10]
00381D50  movaps   xmm7, xmmword ptr [r11 - 0x20]
00381D55  movaps   xmm8, xmmword ptr [r11 - 0x30]
00381D5A  movaps   xmm9, xmmword ptr [r11 - 0x40]
00381D5F  movaps   xmm10, xmmword ptr [r11 - 0x50]
00381D64  movaps   xmm11, xmmword ptr [r11 - 0x60]
00381D69  movaps   xmm12, xmmword ptr [r11 - 0x70]
00381D6E  movaps   xmm13, xmmword ptr [r11 - 0x80]
00381D73  movaps   xmm14, xmmword ptr [rsp + 0x60]
00381D79  movaps   xmm15, xmmword ptr [rsp + 0x50]
00381D7F  mov      rsp, r11
00381D82  pop      rdi
00381D83  ret      
```

## 0046BF60 (54 B, extent 0046BF60-0046BF96)

Page context: " box primitive — six-face unit-cube test over the '0xD11200' face table, margin '1.001' | 477 B | | '00381EB0' | EB0 — point-in-unit-shape test: local transform, then per-type membership | 365 B | | '0046BF60' | BF60 — point-plane dot distance | 54 B | | '0046BFA0' | BFA0 — signed projected distance '−|d|·dot/den' (same form as E6D0, different arg roles) | 294 B |  ### Who reaches it  - '0022F430' F430 (the waypoint walker) ~~plants D4B"

```
0046BF60  movss    xmm2, dword ptr [rcx]
0046BF64  movss    xmm0, dword ptr [rcx + 4]
0046BF69  subss    xmm0, dword ptr [r8 + 4]
0046BF6F  subss    xmm2, dword ptr [r8]
0046BF74  movss    xmm1, dword ptr [rcx + 8]
0046BF79  subss    xmm1, dword ptr [r8 + 8]
0046BF7F  mulss    xmm0, dword ptr [rdx + 4]
0046BF84  mulss    xmm2, dword ptr [rdx]
0046BF88  mulss    xmm1, dword ptr [rdx + 8]
0046BF8D  addss    xmm0, xmm2
0046BF91  addss    xmm0, xmm1
0046BF95  ret      
```
