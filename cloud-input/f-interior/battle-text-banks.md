# F-interior pack: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md`

Generated 2026-10-03 02:40 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/battle-text-banks.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: de4492e21	SWE2-CONTRACT: pass-22 debt final - six-folder worklist (597 pairs) fully dispositioned, 0 live find; b199fc9e1	SWE2-CONTRACT: pass-22 round 2 - five helper-only bullets re-read (3 relabelled MECHANICAL, 5 re-exp; inbox mentions: FABLE.md). OPUS read these before packing.

## 00197A40 (11 B, extent 00197A40-00197A4B)

Page context: "# SWE2-EC7-103 update (2026-09-20) - '001E0F00' measured  '001E0F00' (32 B) is the two-call row resolve '002862A0', '00286D60', '002880B0' and '00288A60' call: '00198790()' supplies the record, then '00197A40(record, ecx)' answers a byte which is 'movzx''d into the return - the indexed predicate the '== 0x14' element arm of the nested-list walks consults ('00286D60' passes 'ecx = 2' to pick between its two id tables). Interior anchor '0"

```
00197A40  movsx    eax, byte ptr [rcx + 0x3a]
00197A44  bt       eax, edx
00197A47  setb     al
00197A4A  ret      
```

## 002902D0 (40 B, extent 002902D0-002902F8)

Page context: " ('00305F90'–'00305FD8') | ~~'action_data.bin'~~ action-table row '+0x34' ('battle_pack.bin' '+0x3C'; corrected 2026-09-12, AY-6) | 0 | the action — the HUD post of the current action's name through '002902D0' | | 'BattleUnit_ApplyUnitDefinition' ('0023A88A'–'0023A8E1') | enemy row '+0x08' | by the word | the unit's name text, stored at unit '+0x18' | | 'BattleUnit_ApplyUnitDefinition' ('0023AB03'–'0023AB57') | party row '+0x30' | by th"

```
002902D0  sub      rsp, 0x38
002902D4  mov      r9d, 0x40
002902DA  mov      dword ptr [rsp + 0x28], 0x30
002902E2  mov      dword ptr [rsp + 0x20], 0x28
002902EA  lea      r8d, [r9 - 0x3f]
002902EE  call     0x2d4fb0  ; -> 002D4FB0 fn
002902F3  add      rsp, 0x38
002902F7  ret      
```

## 002B5390 (747 B, extent 002B5390-002B567B)

Page context: "- **UI — CLIENT and SERVICE (80 edges).** 77 inbound (UI bodies '002C4720', '00559E30', '002C38B0' call page-cited '002DD7E0', '002B58B0', '00254A10'); 3 outbound (page-cited '002878E0', '002B41F0', '002B5390' call UI bodies '002814E0', '002AF340', '002B2150'). Read (2026-09-30, SWE2-CONTRACT): '002DD7E0', '002B58B0' and '00254A10' are UI-wide helpers the page cites, MECHANICAL. The relationship is UI widgets laying out battle text thro"

```
002B5390  push     rdi
002B5392  push     r14
002B5394  sub      rsp, 0x148
002B539B  mov      rax, qword ptr [rip + 0x1c8f48e]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002B53A2  xor      rax, rsp
002B53A5  mov      qword ptr [rsp + 0x100], rax
002B53AD  mov      qword ptr [rsp + 0x28], rdx
002B53B2  mov      r14, rdx
002B53B5  mov      rdi, rcx
002B53B8  test     rcx, rcx
002B53BB  jne      0x2b53c4  ; -> 002B53C4
002B53BD  xor      eax, eax
002B53BF  jmp      0x2b563a  ; -> 002B563A
002B53C4  mov      qword ptr [rsp + 0x170], rbx
002B53CC  mov      rbx, qword ptr [rcx + 0x10]
002B53D0  mov      qword ptr [rsp + 0x138], rsi
002B53D8  movaps   xmmword ptr [rsp + 0x110], xmm6
002B53E0  mov      byte ptr [rcx + 0x27], 0
002B53E4  test     rbx, rbx
002B53E7  jne      0x2b53ec  ; -> 002B53EC
002B53E9  mov      rbx, qword ptr [rcx]
002B53EC  movsx    eax, word ptr [rcx + 0x24]
002B53F0  lea      rcx, [rsp + 0x30]
002B53F5  movd     xmm6, eax
002B53F9  cvtdq2ps xmm6, xmm6
002B53FC  call     0x2ac1e0  ; -> 002AC1E0 fn
002B5401  mov      rcx, r14
002B5404  test     r14, r14
002B5407  jne      0x2b540d  ; -> 002B540D
002B5409  mov      rcx, qword ptr [rdi + 0x18]
002B540D  call     0x39bad0  ; -> 0039BAD0 fn
002B5412  mov      rcx, qword ptr [rip + 0x1de7827]  ; -> 0209CC40
002B5419  lea      r9, [rsp + 0x24]
002B541E  mov      byte ptr [rsp + 0xd6], al
002B5425  lea      r8, [rsp + 0x20]
002B542A  mov      eax, dword ptr [rdi + 0x28]
002B542D  mov      rdx, rbx
002B5430  mov      dword ptr [rcx + 0x10d0], eax
002B5436  movzx    eax, byte ptr [rsp + 0xca]
002B543E  mov      byte ptr [rcx + 0x1104], al
002B5444  lea      rcx, [rsp + 0x30]
002B5449  call     0x2b2150  ; -> 002B2150 fn
002B544E  mov      r8, qword ptr [rip + 0x1de77eb]  ; -> 0209CC40
002B5455  cvttss2si edx, dword ptr [rsp + 0x20]
002B545B  movsxd   rsi, eax
002B545E  mov      ecx, dword ptr [r8 + 0x10d0]
002B5465  mov      dword ptr [rdi + 0x28], ecx
002B5468  cvttss2si ecx, xmm6
002B546C  cmp      edx, ecx
002B546E  jg       0x2b54b1  ; -> 002B54B1
002B5470  mov      word ptr [rdi + 0x22], si
002B5474  mov      rcx, rsi
002B5477  mov      qword ptr [rdi + 8], rbx
002B547B  movzx    eax, byte ptr [rsi + rbx]
002B547F  xor      esi, esi
002B5481  mov      byte ptr [rdi + 0x26], al
002B5484  test     al, al
002B5486  je       0x2b5491  ; -> 002B5491
002B5488  lea      rax, [rbx + 1]
002B548C  add      rax, rcx
002B548F  jmp      0x2b5494  ; -> 002B5494
002B5491  mov      rax, rsi
002B5494  mov      qword ptr [rdi + 0x10], rax
002B5498  mov      edx, 2
002B549D  cmp      byte ptr [r8 + 0x1104], 0x26
002B54A5  cmove    esi, edx
002B54A8  mov      byte ptr [rdi + 0x27], sil
002B54AC  jmp      0x2b5622  ; -> 002B5622
002B54B1  call     0x254a10  ; -> 00254A10 fn
002B54B6  test     eax, eax
002B54B8  jne      0x2b5509  ; -> 002B5509
002B54BA  mov      word ptr [rdi + 0x22], si
002B54BE  mov      rcx, rsi
002B54C1  mov      qword ptr [rdi + 8], rbx
002B54C5  movzx    eax, byte ptr [rsi + rbx]
002B54C9  xor      esi, esi
002B54CB  mov      byte ptr [rdi + 0x26], al
002B54CE  test     al, al
002B54D0  je       0x2b54db  ; -> 002B54DB
002B54D2  lea      rax, [rbx + 1]
002B54D6  add      rax, rcx
002B54D9  jmp      0x2b54de  ; -> 002B54DE
002B54DB  mov      rax, rsi
002B54DE  mov      rcx, qword ptr [rip + 0x1de775b]  ; -> 0209CC40
002B54E5  mov      edx, 2
002B54EA  mov      byte ptr [rdi + 0x27], 1
002B54EE  mov      qword ptr [rdi + 0x10], rax
002B54F2  cmp      byte ptr [rcx + 0x1104], 0x26
002B54F9  cmove    esi, edx
002B54FC  or       sil, 1
002B5500  mov      byte ptr [rdi + 0x27], sil
002B5504  jmp      0x2b5622  ; -> 002B5622
002B5509  mov      qword ptr [rsp + 0x140], rbp
002B5511  xor      esi, esi
002B5513  mov      qword ptr [rsp + 0x130], r12
002B551B  mov      ebp, esi
002B551D  mov      qword ptr [rsp + 0x128], r13
002B5525  mov      qword ptr [rsp + 0x120], r15
002B552D  test     rbx, rbx
002B5530  je       0x2b55f0  ; -> 002B55F0
002B5536  lea      rcx, [rsp + 0x30]
002B553B  call     0x2ac1e0  ; -> 002AC1E0 fn
002B5540  mov      rcx, r14
002B5543  test     r14, r14
002B5546  jne      0x2b554c  ; -> 002B554C
002B5548  mov      rcx, qword ptr [rdi + 0x18]
002B554C  call     0x39bad0  ; -> 0039BAD0 fn
002B5551  movsxd   rcx, ebp
002B5554  add      rcx, rbx
002B5557  mov      byte ptr [rsp + 0xd6], al
002B555E  call     0x2b1fb0  ; -> 002B1FB0 fn
002B5563  mov      r12d, eax
002B5566  test     eax, eax
002B5568  je       0x2b55f0  ; -> 002B55F0
002B556E  add      ebp, eax
002B5570  xor      r15b, r15b
002B5573  mov      r14d, ebp
002B5576  or       rcx, 0xffffffffffffffff
002B557A  mov      r13d, esi
002B557D  nop      dword ptr [rax]
002B5580  inc      rcx
002B5583  cmp      byte ptr [rbx + rcx], sil
002B5587  jne      0x2b5580  ; -> 002B5580
002B5589  cmp      r14, rcx
002B558C  jae      0x2b559f  ; -> 002B559F
002B558E  movzx    r15d, byte ptr [rbp + rbx]
002B5594  mov      r13d, 1
002B559A  mov      byte ptr [rbp + rbx], sil
002B559F  lea      r9, [rsp + 0x24]
002B55A4  mov      rdx, rbx
002B55A7  lea      r8, [rsp + 0x20]
002B55AC  lea      rcx, [rsp + 0x30]
002B55B1  call     0x2b2150  ; -> 002B2150 fn
002B55B6  test     r13d, r13d
002B55B9  je       0x2b55c0  ; -> 002B55C0
002B55BB  mov      byte ptr [rbp + rbx], r15b
002B55C0  movss    xmm0, dword ptr [rsp + 0x20]
002B55C6  comiss   xmm0, xmm6
002B55C9  ja       0x2b5655  ; -> 002B5655
002B55CF  mov      rax, qword ptr [rip + 0x1de766a]  ; -> 0209CC40
002B55D6  mov      r14, qword ptr [rsp + 0x28]
002B55DB  mov      ecx, dword ptr [rax + 0x10d0]
002B55E1  movsxd   rax, ebp
002B55E4  mov      dword ptr [rdi + 0x28], ecx
002B55E7  add      rax, rbx
002B55EA  jne      0x2b5536  ; -> 002B5536
002B55F0  mov      word ptr [rdi + 0x22], si
002B55F4  xor      eax, eax
002B55F6  mov      byte ptr [rdi + 0x26], sil
002B55FA  mov      qword ptr [rdi + 8], rsi
002B55FE  mov      r15, qword ptr [rsp + 0x120]
002B5606  mov      r13, qword ptr [rsp + 0x128]
002B560E  mov      r12, qword ptr [rsp + 0x130]
002B5616  mov      rbp, qword ptr [rsp + 0x140]
002B561E  mov      qword ptr [rdi + 0x10], rsi
002B5622  mov      rsi, qword ptr [rsp + 0x138]
002B562A  mov      rbx, qword ptr [rsp + 0x170]
002B5632  movaps   xmm6, xmmword ptr [rsp + 0x110]
002B563A  mov      rcx, qword ptr [rsp + 0x100]
002B5642  xor      rcx, rsp
002B5645  call     0x808c40  ; -> 00808C40 fn
002B564A  add      rsp, 0x148
002B5651  pop      r14
002B5653  pop      rdi
002B5654  ret      
002B5655  or       byte ptr [rdi + 0x27], 1
002B5659  sub      ebp, r12d
002B565C  movsxd   rdx, ebp
002B565F  add      rdx, rbx
002B5662  mov      qword ptr [rdi + 8], rbx
002B5666  mov      word ptr [rdi + 0x22], bp
002B566A  movzx    ecx, byte ptr [rdx]
002B566D  test     cl, cl
002B566F  mov      byte ptr [rdi + 0x26], cl
002B5672  cmovne   rsi, rdx
002B5676  mov      rax, rsi
002B5679  jmp      0x2b55fe  ; -> 002B55FE
```

## 0055FB20 (907 B, extent 0055FB20-0055FEAB)

Page context: "002B58B0' and '00254A10' are UI-wide helpers the page cites, MECHANICAL. The relationship is UI widgets laying out battle text through the page's text entries: '002C38B0', '005569F0', '00559E30' and '0055FB20' call '002B3050', and '00243860' and '002C4720' call the scaled dual-extent measure '0029FE20'. Substantive edges include '002B3050' is called by '002C38B0'; '002B3050' is called by '00559E30'; '0029FE20' is called by '00243860'; '"

```
0055FB20  push     rbx
0055FB22  push     rdi
0055FB23  sub      rsp, 0x38
0055FB27  mov      rdi, qword ptr [rip + 0x1b3b102]  ; -> 0209AC30
0055FB2E  mov      rbx, rdx
0055FB31  mov      r8d, ecx
0055FB34  cmp      qword ptr [rdi + 0x158], 0
0055FB3C  je       0x55fea4  ; -> 0055FEA4
0055FB42  mov      rdi, qword ptr [rdi + 0x320]
0055FB49  test     rdi, rdi
0055FB4C  je       0x55fea4  ; -> 0055FEA4
0055FB52  movzx    eax, byte ptr [rdi + 0x55d]
0055FB59  mov      rdi, qword ptr [rdi + rax*8 + 0x140]
0055FB61  lea      eax, [rcx + 1]
0055FB64  mov      rdx, qword ptr [rdi + 0xd0]
0055FB6B  cmp      eax, 8
0055FB6E  ja       0x55fea4  ; -> 0055FEA4
0055FB74  mov      qword ptr [rsp + 0x50], rbp
0055FB79  lea      r9, [rip - 0x43fb80]  ; -> 00120000 (image base)
0055FB80  cdqe     
0055FB82  mov      qword ptr [rsp + 0x30], rsi
0055FB87  mov      ecx, dword ptr [r9 + rax*4 + 0x43feac]  ; image base + 0x43feac = 0055FEAC
0055FB8F  add      rcx, r9
0055FB92  jmp      rcx
0055FB94  movzx    eax, word ptr [rdi + 0x98]
0055FB9B  mov      rbp, qword ptr [rsp + 0x50]
0055FBA0  mov      rsi, qword ptr [rsp + 0x30]
0055FBA5  mov      word ptr [rbx], ax
0055FBA8  movzx    eax, word ptr [rdi + 0x9a]
0055FBAF  mov      word ptr [rbx + 2], ax
0055FBB3  movzx    eax, word ptr [rdi + 0x9c]
0055FBBA  add      ax, 0xc
0055FBBE  mov      word ptr [rbx + 4], ax
0055FBC2  movzx    eax, word ptr [rdi + 0x9e]
0055FBC9  add      ax, 0xc
0055FBCD  mov      word ptr [rbx + 6], ax
0055FBD1  add      rsp, 0x38
0055FBD5  pop      rdi
0055FBD6  pop      rbx
0055FBD7  ret      
0055FBD8  mov      rax, qword ptr [rdi + 0x60]
0055FBDC  mov      rbp, qword ptr [rax]
0055FBDF  xor      eax, eax
0055FBE1  test     dword ptr [rdx + 0x18], 0x1000
0055FBE8  mov      word ptr [rsp + 0x60], ax
0055FBED  mov      word ptr [rsp + 0x68], ax
0055FBF2  je       0x55fbf9  ; -> 0055FBF9
0055FBF4  mov      rdx, qword ptr [rdx]
0055FBF7  jmp      0x55fbfd  ; -> 0055FBFD
0055FBF9  mov      rdx, qword ptr [rdx + 0x10]
0055FBFD  movsx    esi, word ptr [rdi + 0x98]
0055FC04  movsx    eax, word ptr [rbp + 0xc]
0055FC08  movsx    edi, word ptr [rdi + 0x9a]
0055FC0F  add      esi, eax
0055FC11  movsx    eax, word ptr [rbp + 0xe]
0055FC15  add      edi, eax
0055FC17  test     rdx, rdx
0055FC1A  je       0x55fc45  ; -> 0055FC45
0055FC1C  lea      r9, [rsp + 0x68]
0055FC21  xor      ecx, ecx
0055FC23  lea      r8, [rsp + 0x60]
0055FC28  call     0x2b3050  ; -> 002B3050 fn
0055FC2D  add      word ptr [rsp + 0x60], 0x10
0055FC33  call     0x254a10  ; -> 00254A10 fn
0055FC38  test     eax, eax
0055FC3A  jne      0x55fc45  ; -> 0055FC45
0055FC3C  movzx    eax, word ptr [rbp + 0x10]
0055FC40  mov      word ptr [rsp + 0x60], ax
0055FC45  call     0x254a10  ; -> 00254A10 fn
0055FC4A  test     eax, eax
0055FC4C  jne      0x55fc54  ; -> 0055FC54
0055FC4E  add      esi, 2
0055FC51  add      edi, 2
0055FC54  movzx    eax, word ptr [rsp + 0x60]
0055FC59  test     ax, ax
0055FC5C  mov      word ptr [rbx], si
0055FC5F  movzx    eax, ax
0055FC62  mov      word ptr [rbx + 2], di
0055FC66  jne      0x55fc6c  ; -> 0055FC6C
0055FC68  movzx    eax, word ptr [rbp + 0x10]
0055FC6C  mov      rsi, qword ptr [rsp + 0x30]
0055FC71  mov      word ptr [rbx + 4], ax
0055FC75  movzx    eax, word ptr [rbp + 0x12]
0055FC79  mov      rbp, qword ptr [rsp + 0x50]
0055FC7E  add      ax, 0xc
0055FC82  mov      word ptr [rbx + 6], ax
0055FC86  add      rsp, 0x38
0055FC8A  pop      rdi
0055FC8B  pop      rbx
0055FC8C  ret      
0055FC8D  mov      rax, qword ptr [rdi + 0x60]
0055FC91  mov      rbp, qword ptr [rsp + 0x50]
0055FC96  mov      rsi, qword ptr [rsp + 0x30]
0055FC9B  mov      rcx, qword ptr [rax + 0x28]
0055FC9F  movzx    eax, word ptr [rcx + 0xc]
0055FCA3  add      ax, word ptr [rdi + 0x98]
0055FCAA  mov      word ptr [rbx], ax
0055FCAD  movzx    eax, word ptr [rcx + 0xe]
0055FCB1  add      ax, word ptr [rdi + 0x9a]
0055FCB8  mov      word ptr [rbx + 2], ax
0055FCBC  movzx    eax, word ptr [rcx + 0x10]
0055FCC0  add      ax, 0xa
0055FCC4  mov      word ptr [rbx + 4], ax
0055FCC8  movzx    eax, word ptr [rcx + 0x12]
0055FCCC  add      ax, 0xc
0055FCD0  mov      word ptr [rbx + 6], ax
0055FCD4  add      rsp, 0x38
0055FCD8  pop      rdi
0055FCD9  pop      rbx
0055FCDA  ret      
0055FCDB  mov      rax, qword ptr [rdi + 0x60]
0055FCDF  mov      rbp, qword ptr [rsp + 0x50]
0055FCE4  mov      rsi, qword ptr [rsp + 0x30]
0055FCE9  mov      rcx, qword ptr [rax + 0x18]
0055FCED  mov      rdx, qword ptr [rax + 0x20]
0055FCF1  movzx    eax, word ptr [rcx + 0xc]
0055FCF5  add      ax, word ptr [rdi + 0x98]
0055FCFC  mov      word ptr [rbx], ax
0055FCFF  movzx    eax, word ptr [rcx + 0xe]
0055FD03  add      ax, word ptr [rdi + 0x9a]
0055FD0A  mov      word ptr [rbx + 2], ax
0055FD0E  movzx    eax, word ptr [rdx + 0x10]
0055FD12  sub      ax, 6
0055FD16  mov      word ptr [rbx + 4], ax
0055FD1A  movzx    eax, word ptr [rdx + 0x12]
0055FD1E  add      ax, 0xc
0055FD22  mov      word ptr [rbx + 6], ax
0055FD26  add      rsp, 0x38
0055FD2A  pop      rdi
0055FD2B  pop      rbx
0055FD2C  ret      
0055FD2D  mov      rax, qword ptr [rdi + 0xc0]
0055FD34  movzx    ecx, word ptr [rax + 0x98]
0055FD3B  add      cx, word ptr [rdi + 0x98]
0055FD42  mov      word ptr [rbx], cx
0055FD45  mov      rax, qword ptr [rdi + 0xc0]
0055FD4C  movzx    ecx, word ptr [rax + 0x9a]
0055FD53  add      cx, word ptr [rdi + 0x9a]
0055FD5A  mov      word ptr [rbx + 2], cx
0055FD5E  mov      rax, qword ptr [rdi + 0xc0]
0055FD65  movzx    ecx, word ptr [rax + 0x9c]
0055FD6C  add      cx, 0xc
0055FD70  mov      word ptr [rbx + 4], cx
0055FD74  mov      rax, qword ptr [rdi + 0xc0]
0055FD7B  movzx    ecx, word ptr [rax + 0x9e]
0055FD82  jmp      0x55fe92  ; -> 0055FE92
0055FD87  mov      r9, qword ptr [rdi + 0xc0]
0055FD8E  add      r8d, -4
0055FD92  mov      eax, r8d
0055FD95  mov      qword ptr [rsp + 0x28], r14
0055FD9A  cdq      
0055FD9B  mov      qword ptr [rsp + 0x20], r15
0055FDA0  movzx    ecx, byte ptr [r9 + 0xec]
0055FDA8  idiv     ecx
0055FDAA  movsxd   rcx, r8d
0055FDAD  shl      rcx, 5
0055FDB1  mov      r15d, eax
0055FDB4  xor      eax, eax
0055FDB6  mov      r14d, edx
0055FDB9  mov      word ptr [rsp + 0x60], ax
0055FDBE  mov      word ptr [rsp + 0x68], ax
0055FDC3  mov      rdx, qword ptr [rcx + rdi + 0xe8]
0055FDCB  movsx    esi, word ptr [r9 + 0x98]
0055FDD3  movsx    ebp, word ptr [r9 + 0x9a]
0055FDDB  movsx    eax, word ptr [rdi + 0x9a]
0055FDE2  movsx    ecx, word ptr [rdi + 0x98]
0055FDE9  add      ebp, eax
0055FDEB  add      esi, ecx
0055FDED  test     rdx, rdx
0055FDF0  je       0x55fe09  ; -> 0055FE09
0055FDF2  lea      r9, [rsp + 0x68]
0055FDF7  xor      ecx, ecx
0055FDF9  lea      r8, [rsp + 0x60]
0055FDFE  call     0x2b3050  ; -> 002B3050 fn
0055FE03  add      word ptr [rsp + 0x60], 0x22
0055FE09  call     0x254a10  ; -> 00254A10 fn
0055FE0E  test     eax, eax
0055FE10  jne      0x55fe18  ; -> 0055FE18
0055FE12  add      esi, 2
0055FE15  add      ebp, 2
0055FE18  mov      word ptr [rbx], si
0055FE1B  mov      word ptr [rbx + 2], bp
0055FE1F  mov      rax, qword ptr [rdi + 0xc0]
0055FE26  movsx    ecx, r14w
0055FE2A  mov      r14, qword ptr [rsp + 0x28]
0055FE2F  movsx    edx, word ptr [rax + 0xea]
0055FE36  imul     edx, ecx
0055FE39  movsx    ecx, r15w
0055FE3D  mov      r15, qword ptr [rsp + 0x20]
0055FE42  add      dx, si
0055FE45  mov      word ptr [rbx], dx
0055FE48  mov      rax, qword ptr [rdi + 0xc0]
0055FE4F  movsx    edx, word ptr [rax + 0x100]
0055FE56  movzx    eax, word ptr [rsp + 0x60]
0055FE5B  imul     edx, ecx
0055FE5E  add      dx, bp
0055FE61  mov      word ptr [rbx + 2], dx
0055FE65  test     ax, ax
0055FE68  je       0x55fe6f  ; -> 0055FE6F
0055FE6A  movzx    eax, ax
0055FE6D  jmp      0x55fe80  ; -> 0055FE80
0055FE6F  mov      rax, qword ptr [rdi + 0xc0]
0055FE76  movzx    eax, word ptr [rax + 0xea]
0055FE7D  add      eax, 0xc
0055FE80  mov      word ptr [rbx + 4], ax
0055FE84  mov      rax, qword ptr [rdi + 0xc0]
0055FE8B  movzx    ecx, word ptr [rax + 0x100]
0055FE92  add      cx, 0xc
0055FE96  mov      word ptr [rbx + 6], cx
0055FE9A  mov      rbp, qword ptr [rsp + 0x50]
0055FE9F  mov      rsi, qword ptr [rsp + 0x30]
0055FEA4  add      rsp, 0x38
0055FEA8  pop      rdi
0055FEA9  pop      rbx
0055FEAA  ret      
```
