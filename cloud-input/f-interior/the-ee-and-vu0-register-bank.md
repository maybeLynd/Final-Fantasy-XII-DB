# F-interior pack: `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-ee-and-vu0-register-bank.json`.

Functions: 9. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ; inbox mentions: FABLE.md). OPUS read these before packing.

## 002330D0 (59 B, extent 002330D0-0023310B)

Page context: "— '0022A0B0', the startup hub cited on this page, calls **actor** '002368D0' and **input** '0035B270'; '0025A8E0' and '0036DD80' are called by **actor** '0025C830'; and '002F67C0' calls **movement** '002330D0' (5 edges). The register-bank helpers are reached from actor-init and locomotion code as well as the script verbs; shared state, shared callers.)*  *(Pass 22 live-graph completion, 2026-09-15: '0025C830' also calls 'Party' '00358BB"

```
002330D0  mov      qword ptr [rsp + 8], rbx
002330D5  push     rdi
002330D6  sub      rsp, 0x20
002330DA  mov      edi, r8d
002330DD  mov      rbx, rcx
002330E0  call     0x233050  ; -> 00233050 fn
002330E5  test     ax, ax
002330E8  js       0x233100  ; -> 00233100
002330EA  movzx    ecx, word ptr [rbx + 0x40]
002330EE  inc      cx
002330F1  movsx    edx, di
002330F4  movsx    r8d, cx
002330F8  imul     r8d, edx
002330FC  add      ax, r8w
00233100  mov      rbx, qword ptr [rsp + 0x30]
00233105  add      rsp, 0x20
00233109  pop      rdi
0023310A  ret      
```

## 0029BC80 (451 B, extent 0029BC80-0029BE43)

Page context: "040F390', '0040FF30''s siblings '00413340', '00413C80', '00411650') — the subsystem's heavy stages are exactly the translated-assembly population. Three members have no direct caller in 'edges.tsv' ('0029BC80', '00398390', '0042D050') — installer or indirect reach only; **not** dead-code claims.  **Controls re-derived.** The three known members reproduce under the sequence reader: '00398F90' reads vf01–vf04 with ACC accumulation and a v"

```
0029BC80  mov      qword ptr [rsp + 0x18], rbx
0029BC85  mov      qword ptr [rsp + 0x20], rsi
0029BC8A  push     rdi
0029BC8B  sub      rsp, 0x50
0029BC8F  mov      rax, qword ptr [rip + 0x1ca8b9a]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0029BC96  xor      rax, rsp
0029BC99  mov      qword ptr [rsp + 0x40], rax
0029BC9E  mov      rbx, rcx
0029BCA1  mov      ecx, dword ptr [rdx]
0029BCA3  sub      ecx, 1
0029BCA6  je       0x29bdc8  ; -> 0029BDC8
0029BCAC  sub      ecx, 1
0029BCAF  je       0x29bd7e  ; -> 0029BD7E
0029BCB5  cmp      ecx, 2
0029BCB8  je       0x29bcc7  ; -> 0029BCC7
0029BCBA  mov      rcx, rbx
0029BCBD  call     0x5c5230  ; -> 005C5230 fn
0029BCC2  jmp      0x29be26  ; -> 0029BE26
0029BCC7  movss    xmm0, dword ptr [rip + 0x1c5d721]  ; -> 01EF93F0 [u32 0x00000000]
0029BCCF  lea      rdx, [rsp + 0x20]
0029BCD4  movss    xmm1, dword ptr [rip + 0x1c5d71c]  ; -> 01EF93F8 [u32 0x00000000]
0029BCDC  lea      rcx, [rip + 0x285187d]  ; -> 02AED560
0029BCE3  movss    dword ptr [rsp + 0x30], xmm0
0029BCE9  movss    xmm0, dword ptr [rip + 0x1a4ffab]  ; -> 01CEBC9C [f32 -1]
0029BCF1  movss    dword ptr [rsp + 0x34], xmm0
0029BCF7  movss    dword ptr [rsp + 0x38], xmm1
0029BCFD  mov      dword ptr [rsp + 0x3c], 0
0029BD05  call     0x3cbfa0  ; -> 003CBFA0 fn
0029BD0A  lea      rdx, [rsp + 0x20]
0029BD0F  mov      dword ptr [rsp + 0x2c], 0
0029BD17  lea      rcx, [rsp + 0x20]
0029BD1C  call     0x202de0  ; -> 00202DE0 fn
0029BD21  lea      rdx, [rsp + 0x20]
0029BD26  lea      rcx, [rsp + 0x30]
0029BD2B  call     0x202d20  ; -> 00202D20 fn
0029BD30  movss    xmm2, dword ptr [rip + 0x679504]  ; -> 0091523C [f32 0.3]
0029BD38  movss    xmm4, dword ptr [rip + 0x1a4fe68]  ; -> 01CEBBA8 [f32 1]
0029BD40  movaps   xmm1, xmm2
0029BD43  mov      rcx, qword ptr [rbx + 0x38]
0029BD47  maxss    xmm1, xmm0
0029BD4B  movaps   xmm3, xmm4
0029BD4E  movsx    eax, word ptr [rcx + 0x58]
0029BD52  minss    xmm3, xmm1
0029BD56  movd     xmm0, eax
0029BD5A  cvtdq2ps xmm0, xmm0
0029BD5D  subss    xmm3, xmm2
0029BD61  mulss    xmm3, dword ptr [rip + 0x67a5a7]  ; -> 00916310 [f32 1.428571]
0029BD69  subss    xmm4, xmm3
0029BD6D  mulss    xmm4, xmm0
0029BD71  cvttss2si eax, xmm4
0029BD75  mov      word ptr [rcx + 0x58], ax
0029BD79  jmp      0x29be24  ; -> 0029BE24
0029BD7E  call     0x28f810  ; -> 0028F810 fn
0029BD83  test     eax, eax
0029BD85  js       0x29be24  ; -> 0029BE24
0029BD8B  call     0x28f810  ; -> 0028F810 fn
0029BD90  mov      edi, dword ptr [rip + 0x1b70446]  ; -> 01E0C1DC [u32 0x000001C0]
0029BD96  mov      esi, dword ptr [rip + 0x1b7043c]  ; -> 01E0C1D8 [u32 0x00000200]
0029BD9C  sub      edi, eax
0029BD9E  call     0x28f810  ; -> 0028F810 fn
0029BDA3  test     rbx, rbx
0029BDA6  je       0x29be24  ; -> 0029BE24
0029BDA8  xor      ecx, ecx
0029BDAA  mov      word ptr [rbx + 0x9a], ax
0029BDB1  mov      word ptr [rbx + 0x98], cx
0029BDB8  mov      word ptr [rbx + 0x9c], si
0029BDBF  mov      word ptr [rbx + 0x9e], di
0029BDC6  jmp      0x29be24  ; -> 0029BE24
0029BDC8  xor      ecx, ecx
0029BDCA  call     0x2735e0  ; -> 002735E0 fn
0029BDCF  mov      rdx, rax
0029BDD2  mov      rcx, rbx
0029BDD5  call     0x247570  ; -> 00247570 fn
0029BDDA  call     0x28f810  ; -> 0028F810 fn
0029BDDF  mov      esi, dword ptr [rip + 0x1b703f3]  ; -> 01E0C1D8 [u32 0x00000200]
0029BDE5  mov      edi, eax
0029BDE7  call     0x28f810  ; -> 0028F810 fn
0029BDEC  mov      edx, dword ptr [rip + 0x1b703ea]  ; -> 01E0C1DC [u32 0x000001C0]
0029BDF2  sub      edx, eax
0029BDF4  test     rbx, rbx
0029BDF7  je       0x29be17  ; -> 0029BE17
0029BDF9  xor      ecx, ecx
0029BDFB  mov      word ptr [rbx + 0x9a], dx
0029BE02  mov      word ptr [rbx + 0x98], cx
0029BE09  mov      word ptr [rbx + 0x9c], si
0029BE10  mov      word ptr [rbx + 0x9e], di
0029BE17  mov      edx, 0xa1
0029BE1C  mov      rcx, rbx
0029BE1F  call     0x247930  ; -> 00247930 fn
0029BE24  xor      eax, eax
0029BE26  mov      rcx, qword ptr [rsp + 0x40]
0029BE2B  xor      rcx, rsp
0029BE2E  call     0x808c40  ; -> 00808C40 fn
0029BE33  mov      rbx, qword ptr [rsp + 0x70]
0029BE38  mov      rsi, qword ptr [rsp + 0x78]
0029BE3D  add      rsp, 0x50
0029BE41  pop      rdi
0029BE42  ret      
```

## 00398390 (224 B, extent 00398390-00398470)

Page context: "040FF30''s siblings '00413340', '00413C80', '00411650') — the subsystem's heavy stages are exactly the translated-assembly population. Three members have no direct caller in 'edges.tsv' ('0029BC80', '00398390', '0042D050') — installer or indirect reach only; **not** dead-code claims.  **Controls re-derived.** The three known members reproduce under the sequence reader: '00398F90' reads vf01–vf04 with ACC accumulation and a vf00 read — t"

```
00398390  sub      rsp, 0x38
00398394  movss    xmm1, dword ptr [rip + 0x1f40f70]  ; -> 022D930C
0039839C  mulss    xmm1, dword ptr [rip + 0x1b6104c]  ; -> 01EF93F0 [u32 0x00000000]
003983A4  movaps   xmmword ptr [rsp + 0x20], xmm6
003983A9  movaps   xmmword ptr [rsp + 0x10], xmm7
003983AE  movaps   xmmword ptr [rsp], xmm8
003983B3  movups   xmm8, xmmword ptr [rcx]
003983B7  movups   xmmword ptr [rip + 0x1f40f21], xmm8  ; -> 022D92E0
003983BF  movups   xmm0, xmmword ptr [rdx]
003983C2  movss    dword ptr [rip + 0x1f40f42], xmm1  ; -> 022D930C
003983CA  movaps   xmm6, xmm8
003983CE  shufps   xmm6, xmm8, 0x55
003983D3  movups   xmm7, xmm0
003983D6  movaps   xmm1, xmm8
003983DA  movaps   xmm5, xmm0
003983DD  shufps   xmm1, xmm8, 0xaa
003983E2  movaps   xmm4, xmm6
003983E5  shufps   xmm5, xmm0, 0xaa
003983E9  movaps   xmm2, xmm8
003983ED  movups   xmmword ptr [rip + 0x1f40efc], xmm0  ; -> 022D92F0
003983F4  shufps   xmm0, xmm0, 0x55
003983F8  movaps   xmm3, xmm1
003983FB  mulss    xmm2, xmm0
003983FF  mulss    xmm3, xmm7
00398403  mulss    xmm6, xmm7
00398407  movaps   xmm7, xmmword ptr [rsp + 0x10]
0039840C  mulss    xmm4, xmm5
00398410  mulss    xmm1, xmm0
00398414  mulss    xmm8, xmm5
00398419  movss    dword ptr [rip + 0x1f40d87], xmm2  ; -> 022D91A8
00398421  subss    xmm2, xmm6
00398425  movaps   xmm6, xmmword ptr [rsp + 0x20]
0039842A  movss    dword ptr [rip + 0x1f40d6e], xmm4  ; -> 022D91A0
00398432  subss    xmm4, xmm1
00398436  movss    dword ptr [rip + 0x1f40d66], xmm3  ; -> 022D91A4
0039843E  subss    xmm3, xmm8
00398443  movaps   xmm8, xmmword ptr [rsp]
00398448  movss    dword ptr [rip + 0x1f40eb8], xmm2  ; -> 022D9308
00398450  movss    dword ptr [rip + 0x1f40ea8], xmm4  ; -> 022D9300
00398458  movss    dword ptr [rip + 0x1f40ea4], xmm3  ; -> 022D9304
00398460  movups   xmm0, xmmword ptr [rip + 0x1f40e99]  ; -> 022D9300
00398467  movups   xmmword ptr [r8], xmm0
0039846B  add      rsp, 0x38
0039846F  ret      
```

## 003A2B90 (53 B, extent 003A2B90-003A2BC5)

Page context: " mixed | 16 |  The 20-row 'C-fragment' class is defined by **at most four bank accesses**, not by vf00 alone — eight of them touch non-vf00 registers ('002F67C0' 'Wvf01'; '00376470' 'Rvf00×2 Wvf01'; '003A2B90' '$v0'+'vf21'+'vf20'; '003B4310'/'003B5D40'/'0053DB50' 'W$t0'; '004010A0' 'vf20'+'$t0'; '0044B960' 'vf21'). Rows touching only 'Rvf00' are C routines borrowing the constant.  **Families the caller map already resolves.** BFS throug"

```
003A2B90  movss    dword ptr [rsp + 0x10], xmm1
003A2B96  movups   xmm1, xmmword ptr [rcx]
003A2B99  movsxd   rax, dword ptr [rsp + 0x10]
003A2B9E  mov      qword ptr [rip + 0x1f3638b], rax  ; -> 022D8F30
003A2BA5  movups   xmm0, xmmword ptr [rip + 0x1f36384]  ; -> 022D8F30
003A2BAC  movups   xmmword ptr [rip + 0x1f3673d], xmm0  ; -> 022D92F0
003A2BB3  shufps   xmm0, xmm0, 0
003A2BB7  subps    xmm1, xmm0
003A2BBA  movups   xmmword ptr [rip + 0x1f3671f], xmm1  ; -> 022D92E0
003A2BC1  movups   xmmword ptr [rcx], xmm1
003A2BC4  ret      
```

## 0050C670 (54 B, extent 0050C670-0050C6A6)

Page context: "ted as the pool constructor's carrier, and loading the settings file is its other start-up work.  **Script_VM_Native_Bridge — CLIENT (24 edges).** 24 script-bridge bodies call '0017D280', among them '0050C670', '0050C8D0', '0050D240', '0050D5E0', '0050EBA0' and '00510870'. They print through the same stdout routine the emulation start-up uses; that shares a print helper, not the register bank.  **UI — CLIENT (3 edges).** '0035DCC0' call"

```
0050C670  mov      qword ptr [rsp + 8], rbx
0050C675  push     rdi
0050C676  sub      rsp, 0x20
0050C67A  mov      rdi, rcx
0050C67D  call     0x3bb420  ; -> 003BB420 fn
0050C682  mov      edx, eax
0050C684  lea      rcx, [rip + 0x8161fd]  ; -> 00D22888
0050C68B  mov      ebx, eax
0050C68D  call     0x17d280  ; -> 0017D280 fn
0050C692  mov      edx, ebx
0050C694  mov      rcx, rdi
0050C697  mov      rbx, qword ptr [rsp + 0x30]
0050C69C  add      rsp, 0x20
0050C6A0  pop      rdi
0050C6A1  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0050C8D0 (54 B, extent 0050C8D0-0050C906)

Page context: "ool constructor's carrier, and loading the settings file is its other start-up work.  **Script_VM_Native_Bridge — CLIENT (24 edges).** 24 script-bridge bodies call '0017D280', among them '0050C670', '0050C8D0', '0050D240', '0050D5E0', '0050EBA0' and '00510870'. They print through the same stdout routine the emulation start-up uses; that shares a print helper, not the register bank.  **UI — CLIENT (3 edges).** '0035DCC0' calls '0036DD80'"

```
0050C8D0  mov      qword ptr [rsp + 8], rbx
0050C8D5  push     rdi
0050C8D6  sub      rsp, 0x20
0050C8DA  mov      rdi, rcx
0050C8DD  call     0x3bb420  ; -> 003BB420 fn
0050C8E2  mov      edx, eax
0050C8E4  lea      rcx, [rip + 0x815fbd]  ; -> 00D228A8
0050C8EB  mov      ebx, eax
0050C8ED  call     0x17d280  ; -> 0017D280 fn
0050C8F2  mov      edx, ebx
0050C8F4  mov      rcx, rdi
0050C8F7  mov      rbx, qword ptr [rsp + 0x30]
0050C8FC  add      rsp, 0x20
0050C900  pop      rdi
0050C901  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00510870 (220 B, extent 00510870-0051094C)

Page context: " file is its other start-up work.  **Script_VM_Native_Bridge — CLIENT (24 edges).** 24 script-bridge bodies call '0017D280', among them '0050C670', '0050C8D0', '0050D240', '0050D5E0', '0050EBA0' and '00510870'. They print through the same stdout routine the emulation start-up uses; that shares a print helper, not the register bank.  **UI — CLIENT (3 edges).** '0035DCC0' calls '0036DD80'; '00368010' calls the composer '00397910'; '00247A"

```
00510870  mov      qword ptr [rsp + 8], rbx
00510875  mov      qword ptr [rsp + 0x10], rbp
0051087A  mov      qword ptr [rsp + 0x18], rsi
0051087F  mov      qword ptr [rsp + 0x20], rdi
00510884  push     r14
00510886  sub      rsp, 0x20
0051088A  mov      rbp, rcx
0051088D  mov      rsi, r9
00510890  mov      rcx, r9
00510893  mov      r14, rdx
00510896  call     0x267e10  ; -> 00267E10 fn
0051089B  mov      rcx, rsi
0051089E  mov      edi, eax
005108A0  call     0x267e10  ; -> 00267E10 fn
005108A5  mov      rcx, rsi
005108A8  mov      ebx, eax
005108AA  call     0x267e10  ; -> 00267E10 fn
005108AF  mov      r8d, edi
005108B2  mov      edx, ebx
005108B4  mov      ecx, eax
005108B6  mov      esi, eax
005108B8  call     0x359ea0  ; -> 00359EA0 fn
005108BD  mov      rbx, rax
005108C0  test     rax, rax
005108C3  je       0x510919  ; -> 00510919
005108C5  mov      rdx, rax
005108C8  mov      rcx, r14
005108CB  call     0x262f50  ; -> 00262F50 fn
005108D0  mov      rcx, rbp
005108D3  test     eax, eax
005108D5  je       0x51091c  ; -> 0051091C
005108D7  mov      edx, 1
005108DC  call     0x26b4e0  ; -> 0026B4E0 fn
005108E1  mov      edx, esi
005108E3  lea      rcx, [rip + 0x812246]  ; -> 00D22B30
005108EA  call     0x17d280  ; -> 0017D280 fn
005108EF  mov      edx, 1
005108F4  mov      rcx, rbx
005108F7  call     0x35ae10  ; -> 0035AE10 fn
005108FC  movzx    edx, word ptr [rbx]
005108FF  movzx    ecx, byte ptr [rbx + 0x15]
00510903  call     0x263a30  ; -> 00263A30 fn
00510908  mov      rdx, rax
0051090B  lea      rcx, [rip + 0x812246]  ; -> 00D22B58
00510912  call     0x17d280  ; -> 0017D280 fn
00510917  jmp      0x510931  ; -> 00510931
00510919  mov      rcx, rbp
0051091C  xor      edx, edx
0051091E  call     0x26b4e0  ; -> 0026B4E0 fn
00510923  mov      edx, esi
00510925  lea      rcx, [rip + 0x812254]  ; -> 00D22B80
0051092C  call     0x17d280  ; -> 0017D280 fn
00510931  mov      rbx, qword ptr [rsp + 0x30]
00510936  mov      rbp, qword ptr [rsp + 0x38]
0051093B  mov      rsi, qword ptr [rsp + 0x40]
00510940  mov      rdi, qword ptr [rsp + 0x48]
00510945  add      rsp, 0x20
00510949  pop      r14
0051094B  ret      
```

## 006BA940 (99 B, extent 006BA940-006BA9A3)

Page context: "BAA40'. But nothing hands it work: the constructors are called only from the getter (whole-image call sweep), the pool object is referenced only by the getter and the static destructor '008B41F0' (→ '006BA940'), and the getter's two callers are the boot initialiser '005A08E0', which calls slot 2 *start* ('006BAB40', '005A0A99'), and the shutdown '005A0840', which calls slot 3 *terminate* ('006BAED0', '005A0882'). The submit slot 5 — '00"

```
006BA940  push     rbx
006BA942  sub      rsp, 0x30
006BA946  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006BA94F  mov      rbx, rcx
006BA952  lea      rax, [rip + 0x6c68a7]  ; -> 00D81200
006BA959  mov      qword ptr [rcx], rax
006BA95C  call     0x6baed0  ; -> 006BAED0 fn
006BA961  nop      
006BA962  lea      rcx, [rbx + 0x58]
006BA966  lea      r9, [rip - 0x54d2cd]  ; -> 0016D6A0
006BA96D  mov      edx, 0x10
006BA972  lea      r8d, [rdx - 0xe]
006BA976  call     0x809054  ; -> 00809054 fn
006BA97B  nop      
006BA97C  lea      rcx, [rbx + 0x38]
006BA980  lea      r9, [rip - 0x54d2e7]  ; -> 0016D6A0
006BA987  mov      edx, 0x10
006BA98C  lea      r8d, [rdx - 0xe]
006BA990  call     0x809054  ; -> 00809054 fn
006BA995  nop      
006BA996  mov      rcx, rbx
006BA999  add      rsp, 0x30
006BA99D  pop      rbx
006BA99E  jmp      0x6aa200  ; -> 006AA200 fn
```

## 00863410 (26 B, extent 00863410-0086342A)

Page context: "e '00863500' is a 28-byte trampoline that calls **vtable slot 1** of the object it is given ('call [rax+8]' at '0086350C'), the slot-1 bodies of every thread class the RTTI names — 'crossThreadImpl' '00863410', 'Phyre::PThreadPool' '006AA230', 'PThreadPoolWorkStealing' '006BAA40', 'PThreadPoolImmediate' '006CE570' ('Sys::Thread''s slot 1 is '_purecall'). **Result: the update loop reaches 183 of the 267 members and the draw loop 40; the "

```
00863410  sub      rsp, 0x28
00863414  mov      rax, qword ptr [rcx + 0x18]
00863418  test     rax, rax
0086341B  je       0x863423  ; -> 00863423
0086341D  mov      rcx, qword ptr [rcx + 0x20]
00863421  call     rax
00863423  xor      eax, eax
00863425  add      rsp, 0x28
00863429  ret      
```
