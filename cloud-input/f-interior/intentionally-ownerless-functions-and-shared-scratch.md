# F-interior pack: `00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/intentionally-ownerless-functions-and-shared-scratch.json`.

Functions: 24. Each is cited on the page only at its entry and is still in the F frontier.

## 0017F2A0 (77 B, extent 0017F2A0-0017F2ED)

Page context: "oaded ×5 beginning ['003B9A2A'](../../_index/ADDRESS-INDEX.md), helper set '0046C8D0'/'003616F0'/'00181DD0' ×2 each — the opcode-5/39 arm), '003B9FE0' ('0024B240'), '003BA020' ('00182B40'/'00375900'/'0017F2A0'/'001E0580', '020926D0'), '003BA1F0' ('01DFE0B4'/'020926F6'/'02EBA4F0'/'02EC0F88'/'02F97340') | bodies that read '02F97348' (the §12 action context) or '02EBA4F0' (the target array) — the heavyweight opcode arms | | '02EBEF88' fami"

```
0017F2A0  mov      qword ptr [rsp + 8], rbx
0017F2A5  push     rdi
0017F2A6  sub      rsp, 0x30
0017F2AA  mov      rbx, rdx
0017F2AD  mov      rdi, rcx
0017F2B0  call     0x189120  ; -> 00189120 fn
0017F2B5  test     rax, rax
0017F2B8  je       0x17f2e2  ; -> 0017F2E2
0017F2BA  cmp      byte ptr [rbx + 8], 0
0017F2BE  jne      0x17f2c5  ; -> 0017F2C5
0017F2C0  mov      rbx, qword ptr [rbx]
0017F2C3  jmp      0x17f2c7  ; -> 0017F2C7
0017F2C5  xor      ebx, ebx
0017F2C7  call     0x18ca40  ; -> 0018CA40 fn
0017F2CC  mov      rcx, rax
0017F2CF  mov      byte ptr [rsp + 0x20], 0
0017F2D4  xor      r9d, r9d
0017F2D7  mov      r8, rdi
0017F2DA  mov      rdx, rbx
0017F2DD  call     0x18b8b0  ; -> 0018B8B0 fn
0017F2E2  mov      rbx, qword ptr [rsp + 0x40]
0017F2E7  add      rsp, 0x30
0017F2EB  pop      rdi
0017F2EC  ret      
```

## 001DC510 (127 B, extent 001DC510-001DC58F)

Page context: " named beside it on this page): '+0x2E0'/'+0x2E4' compare-and-store on dirty, five '001EEE80' refreshes across '+0x280'..'+0x298' plus the midpoint-aligned '+0x2A0' write, then '001DC4A0'/'001DC4C0'/'001DC510'/'001DC590'/'001FDF70'/'00615BC0'/'00616700'/'00624660'/'00624670'/'0065C750' - the render-pass record's resize-on-change.  Interior anchor '00193B10' (function '00193AD0').  '002FCCC0' (562 B) is the keyed release '002EAD00' and '"

```
001DC510  push     rbx
001DC512  sub      rsp, 0x30
001DC516  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001DC51F  mov      rax, qword ptr [rip + 0x1da67ea]  ; -> 01F82D10
001DC526  test     rax, rax
001DC529  jne      0x1dc589  ; -> 001DC589
001DC52B  call     0x1ddab0  ; -> 001DDAB0 fn
001DC530  test     rax, rax
001DC533  je       0x1dc582  ; -> 001DC582
001DC535  mov      ecx, 0x18
001DC53A  call     0x210ec0  ; -> 00210EC0 fn
001DC53F  mov      rbx, rax
001DC542  mov      qword ptr [rsp + 0x40], rax
001DC547  test     rax, rax
001DC54A  je       0x1dc573  ; -> 001DC573
001DC54C  xor      eax, eax
001DC54E  mov      qword ptr [rbx], rax
001DC551  mov      dword ptr [rbx + 8], eax
001DC554  mov      dword ptr [rbx + 0xc], 0x3f800000
001DC55B  mov      dword ptr [rbx + 0x10], 0x3f000000
001DC562  mov      dword ptr [rbx + 0x14], 0x3f19999a
001DC569  mov      rcx, rbx
001DC56C  call     0x1dc3d0  ; -> 001DC3D0 fn
001DC571  jmp      0x1dc576  ; -> 001DC576
001DC573  mov      rbx, rax
001DC576  mov      qword ptr [rip + 0x1da6793], rbx  ; -> 01F82D10
001DC57D  mov      rax, rbx
001DC580  jmp      0x1dc589  ; -> 001DC589
001DC582  mov      rax, qword ptr [rip + 0x1da6787]  ; -> 01F82D10
001DC589  add      rsp, 0x30
001DC58D  pop      rbx
001DC58E  ret      
```

## 00258130 (95 B, extent 00258130-0025818F)

Page context: "ements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)  | function | size | role (call-signature read) | |---|---:|---| | '00188B10' | 643 | per-entry loop over '[rsi+0xB08..0xB30]' fields: '00258130'/'00259360'/'0025A890' accessors, '00610330', repeating '00182E80' x11/'00182EB0' x11/'001EEE80' x10 |  ## The '003B8670' exclusive subtree — the interpreter's 33 opcode helpers (SWE2-FRONTIER, exclusive-subtrees package)  The excl"

```
00258130  mov      qword ptr [rsp + 8], rbx
00258135  mov      qword ptr [rsp + 0x10], rbp
0025813A  mov      qword ptr [rsp + 0x18], rsi
0025813F  push     rdi
00258140  sub      rsp, 0x20
00258144  lea      rsi, [rip + 0x1e3a8f5]  ; -> 02092A40
0025814B  mov      ebp, 5
00258150  mov      rbx, rsi
00258153  mov      edi, 4
00258158  mov      rcx, rbx
0025815B  call     0x3cbad0  ; -> 003CBAD0 fn
00258160  add      rbx, 0x2e0
00258167  sub      rdi, 1
0025816B  jne      0x258158  ; -> 00258158
0025816D  add      rsi, 0xbb0
00258174  sub      rbp, 1
00258178  jne      0x258150  ; -> 00258150
0025817A  mov      rbx, qword ptr [rsp + 0x30]
0025817F  mov      rbp, qword ptr [rsp + 0x38]
00258184  mov      rsi, qword ptr [rsp + 0x40]
00258189  add      rsp, 0x20
0025818D  pop      rdi
0025818E  ret      
```

## 0025A890 (77 B, extent 0025A890-0025A8DD)

Page context: "WE2-FRONTIER, residual-placement package)  | function | size | role (call-signature read) | |---|---:|---| | '00188B10' | 643 | per-entry loop over '[rsi+0xB08..0xB30]' fields: '00258130'/'00259360'/'0025A890' accessors, '00610330', repeating '00182E80' x11/'00182EB0' x11/'001EEE80' x10 |  ## The '003B8670' exclusive subtree — the interpreter's 33 opcode helpers (SWE2-FRONTIER, exclusive-subtrees package)  The exclusive-callee census as"

```
0025A890  mov      qword ptr [rsp + 8], rbx
0025A895  push     rdi
0025A896  sub      rsp, 0x20
0025A89A  lea      rbx, [rip + 0x1e3ca7f]  ; -> 02097320
0025A8A1  mov      edi, 8
0025A8A6  mov      rcx, rbx
0025A8A9  call     0x3cbad0  ; -> 003CBAD0 fn
0025A8AE  add      rbx, 0x110
0025A8B5  sub      rdi, 1
0025A8B9  jne      0x25a8a6  ; -> 0025A8A6
0025A8BB  lea      rcx, [rip + 0x1e3d2be]  ; -> 02097B80
0025A8C2  call     0x3cbad0  ; -> 003CBAD0 fn
0025A8C7  lea      rcx, [rip + 0x1e3d382]  ; -> 02097C50
0025A8CE  mov      rbx, qword ptr [rsp + 0x30]
0025A8D3  add      rsp, 0x20
0025A8D7  pop      rdi
0025A8D8  jmp      0x3cbad0  ; -> 003CBAD0 fn
```

## 002986E0 (2468 B, extent 002986E0-00299084)

Page context: "Menu_BuildCommandEntryList' (0031EB20)). Substantive edges include '00181DD0' is called by '0024B9B0'; '001E0E30' is called by '0029B870'; '00225580' is called by '00299090'; '00225580' is called by '002986E0'; the remaining edges run through shared helpers the page cites. - **PlatformOnlineAchievements — MECHANICAL (1 edge).** 1 call from page-cited bodies into shared PlatformOnlineAchievements plumbing ('00316A50') - the helpers' gene"

```
002986E0  mov      qword ptr [rsp + 0x18], rbx
002986E5  push     rbp
002986E6  push     rsi
002986E7  push     rdi
002986E8  push     r12
002986EA  push     r13
002986EC  push     r14
002986EE  push     r15
002986F0  lea      rbp, [rsp - 0x27]
002986F5  sub      rsp, 0xf0
002986FC  mov      rax, qword ptr [rip + 0x1cac12d]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00298703  xor      rax, rsp
00298706  mov      qword ptr [rbp + 0x1f], rax
0029870A  mov      rsi, rdx
0029870D  mov      dword ptr [rbp + 0x17], 0x820081
00298714  xor      edx, edx
00298716  mov      dword ptr [rbp + 0x1b], 0x810083
0029871D  mov      rdi, rcx
00298720  test     rcx, rcx
00298723  jne      0x29872a  ; -> 0029872A
00298725  mov      r13d, edx
00298728  jmp      0x298732  ; -> 00298732
0029872A  mov      rax, qword ptr [rcx + 0x60]
0029872E  mov      r13, qword ptr [rax + 8]
00298732  mov      rcx, qword ptr [rcx + 0xc0]
00298739  mov      eax, 0x100
0029873E  mov      r10d, 0x4000
00298744  mov      dword ptr [rbp - 0x79], 0x80808080
0029874B  mov      dword ptr [rbp - 0x75], 0x40
00298752  mov      dword ptr [rbp - 0x71], 0x80c0c0c0
00298759  lea      r8d, [rax - 0x80]
0029875D  mov      dword ptr [rbp - 0x6d], 0x20
00298764  mov      dword ptr [rbp - 0x69], 0x80008080
0029876B  mov      dword ptr [rbp - 0x65], 0x10
00298772  mov      dword ptr [rbp - 0x61], 0x80808080
00298779  mov      dword ptr [rbp - 0x5d], 0x10
00298780  movzx    r12d, word ptr [rcx + 4]
00298785  mov      dword ptr [rsp + 0x20], 0x80808080
0029878D  cmp      word ptr [rsi + 0x5e], r10w
00298792  jae      0x2987af  ; -> 002987AF
00298794  cmp      word ptr [rsi + 0x5c], r10w
00298799  jae      0x2987af  ; -> 002987AF
0029879B  test     dword ptr [rsi], eax
0029879D  je       0x2987af  ; -> 002987AF
0029879F  movzx    eax, word ptr [rcx + 0x14]
002987A3  add      eax, 0x10
002987A6  cmp      eax, r8d
002987A9  cmovg    eax, r8d
002987AD  jmp      0x2987b9  ; -> 002987B9
002987AF  movzx    eax, word ptr [rcx + 0x14]
002987B3  sub      eax, 0x10
002987B6  cmovs    eax, edx
002987B9  mov      word ptr [rcx + 0x14], ax
002987BD  lea      r14, [rbp - 0x79]
002987C1  mov      rax, qword ptr [rdi + 0xc0]
002987C8  lea      r15, [rbp + 0x17]
002987CC  mov      ebx, edx
002987CE  movzx    ecx, byte ptr [rax + 0x14]
002987D2  mov      rax, qword ptr [rdi + 0x60]
002987D6  mov      byte ptr [rsp + 0x23], cl
002987DA  mov      rcx, qword ptr [rax + 0x18]
002987DE  mov      eax, dword ptr [rsp + 0x20]
002987E2  mov      dword ptr [rcx + 0x34], eax
002987E5  mov      dword ptr [rcx + 0x30], eax
002987E8  mov      dword ptr [rcx + 0x2c], eax
002987EB  mov      dword ptr [rcx + 0x28], eax
002987EE  nop      
002987F0  movzx    ecx, word ptr [r15]
002987F4  call     0x2dd7e0  ; -> 002DD7E0 fn
002987F9  inc      ebx
002987FB  mov      dword ptr [r14], eax
002987FE  lea      r15, [r15 + 2]
00298802  lea      r14, [r14 + 8]
00298806  cmp      ebx, 4
00298809  jb       0x2987f0  ; -> 002987F0
0029880B  xor      ecx, ecx
0029880D  mov      dword ptr [rbp + 0x17], 0x7b007a
00298814  mov      r14d, ecx
00298817  mov      dword ptr [rbp + 0x1b], 0x7d007c
0029881E  lea      rbx, [rbp - 0x21]
00298822  lea      r15, [rbp + 0x17]
00298826  movzx    ecx, word ptr [r15]
0029882A  call     0x2dd7e0  ; -> 002DD7E0 fn
0029882F  movzx    ecx, al
00298832  inc      r14d
00298835  mov      dword ptr [rbx - 8], ecx
00298838  lea      rbx, [rbx + 0x10]
0029883C  mov      dword ptr [rsp + 0x20], eax
00298840  lea      r15, [r15 + 2]
00298844  movzx    eax, byte ptr [rsp + 0x21]
00298849  mov      dword ptr [rbx - 0x14], eax
0029884C  movzx    eax, byte ptr [rsp + 0x22]
00298851  mov      dword ptr [rbx - 0x10], eax
00298854  movzx    eax, byte ptr [rsp + 0x23]
00298859  mov      dword ptr [rbx - 0xc], eax
0029885C  cmp      r14d, 4
00298860  jb       0x298826  ; -> 00298826
00298862  mov      eax, 0x80
00298867  mov      dword ptr [rbp + 0x17], 0x7f007e
0029886E  mov      word ptr [rbp + 0x1b], ax
00298872  lea      rbx, [rbp - 0x51]
00298876  xor      eax, eax
00298878  lea      r15, [rbp + 0x17]
0029887C  mov      r14d, eax
0029887F  nop      
00298880  movzx    ecx, word ptr [r15]
00298884  call     0x2dd7e0  ; -> 002DD7E0 fn
00298889  movzx    ecx, al
0029888C  inc      r14d
0029888F  mov      dword ptr [rbx - 8], ecx
00298892  lea      rbx, [rbx + 0x10]
00298896  mov      dword ptr [rsp + 0x20], eax
0029889A  lea      r15, [r15 + 2]
0029889E  movzx    eax, byte ptr [rsp + 0x21]
002988A3  mov      dword ptr [rbx - 0x14], eax
002988A6  movzx    eax, byte ptr [rsp + 0x22]
002988AB  mov      dword ptr [rbx - 0x10], eax
002988AE  movzx    eax, byte ptr [rsp + 0x23]
002988B3  mov      dword ptr [rbx - 0xc], eax
002988B6  cmp      r14d, 3
002988BA  jb       0x298880  ; -> 00298880
002988BC  mov      r14d, dword ptr [rsi + 0x40]
002988C0  mov      r8d, 0x64
002988C6  mov      rax, qword ptr [rdi + 0xc0]
002988CD  test     r14d, r14d
002988D0  mov      r15d, dword ptr [rsi + 0x3c]
002988D4  mov      ebx, 0x4000
002988D9  cmove    r14d, r8d
002988DD  movzx    ecx, word ptr [rax + 4]
002988E1  cmp      cx, bx
002988E4  jb       0x2988ef  ; -> 002988EF
002988E6  movzx    eax, word ptr [rsi + 0x5c]
002988EA  cmp      ax, bx
002988ED  jb       0x298905  ; -> 00298905
002988EF  movzx    eax, word ptr [rsi + 0x5c]
002988F3  cmp      cx, ax
002988F6  je       0x298951  ; -> 00298951
002988F8  test     dword ptr [rsi], 0x8000
002988FE  jne      0x298951  ; -> 00298951
00298900  cmp      ax, bx
00298903  jae      0x298951  ; -> 00298951
00298905  test     dword ptr [rsi], 0x2000
0029890B  je       0x298951  ; -> 00298951
0029890D  movzx    edx, ax
00298910  mov      ecx, 0x14
00298915  call     0x35d330  ; -> 0035D330 fn
0029891A  xor      edx, edx
0029891C  mov      rcx, qword ptr [rax + 0x18]
00298920  call     0x2b58b0  ; -> 002B58B0 fn
00298925  xor      ecx, ecx
00298927  mov      qword ptr [r13 + 0x18], rax
0029892B  call     0x20e620  ; -> 0020E620 fn
00298930  mov      rcx, r13
00298933  mov      dword ptr [r13 + 0x20], eax
00298937  call     0x29fb50  ; -> 0029FB50 fn
0029893C  mov      rcx, qword ptr [rdi + 0xc0]
00298943  mov      r8d, 0x64
00298949  movzx    eax, word ptr [rsi + 0x5c]
0029894D  mov      word ptr [rcx + 4], ax
00298951  cmp      word ptr [rsi + 0x5c], bx
00298955  jae      0x298988  ; -> 00298988
00298957  test     dword ptr [rsi], 0x2000
0029895D  je       0x298988  ; -> 00298988
0029895F  mov      rcx, qword ptr [rdi + 0xc0]
00298966  movzx    eax, byte ptr [rcx + 6]
0029896A  cmp      al, 0x80
0029896C  jae      0x2989b2  ; -> 002989B2
0029896E  add      al, 0x10
00298970  xor      edx, edx
00298972  mov      byte ptr [rcx + 6], al
00298975  mov      rax, qword ptr [rdi + 0xc0]
0029897C  cmp      byte ptr [rax + 6], 0x80
00298980  jbe      0x2989b4  ; -> 002989B4
00298982  mov      byte ptr [rax + 6], 0x80
00298986  jmp      0x2989b4  ; -> 002989B4
00298988  mov      rcx, qword ptr [rdi + 0xc0]
0029898F  movzx    eax, byte ptr [rcx + 6]
00298993  test     al, al
00298995  je       0x2989b2  ; -> 002989B2
00298997  test     dword ptr [rsi], 0x8000
0029899D  jne      0x2989b2  ; -> 002989B2
0029899F  movzx    eax, al
002989A2  mov      edx, 0
002989A7  sub      eax, 0x10
002989AA  cmovs    eax, edx
002989AD  mov      byte ptr [rcx + 6], al
002989B0  jmp      0x2989b4  ; -> 002989B4
002989B2  xor      edx, edx
002989B4  test     dword ptr [rsi], 0x1000
002989BA  mov      rax, qword ptr [rdi + 0xc0]
002989C1  je       0x298a17  ; -> 00298A17
002989C3  mov      byte ptr [rax + 0x13], 0x64
002989C7  cmp      dword ptr [rsi + 0x40], 0
002989CB  je       0x2989d2  ; -> 002989D2
002989CD  mov      r15d, r14d
002989D0  jmp      0x2989d8  ; -> 002989D8
002989D2  mov      r14d, r8d
002989D5  mov      r15d, r8d
002989D8  mov      rcx, qword ptr [rdi + 0xc0]
002989DF  movzx    eax, byte ptr [rcx + 7]
002989E3  sub      eax, 0x10
002989E6  cmovs    eax, edx
002989E9  mov      byte ptr [rcx + 7], al
002989EC  mov      rcx, qword ptr [rdi + 0xc0]
002989F3  movzx    eax, word ptr [rcx + 2]
002989F7  test     al, 4
002989F9  jne      0x298aae  ; -> 00298AAE
002989FF  or       ax, 4
00298A03  mov      word ptr [rcx + 2], ax
00298A07  mov      rax, qword ptr [rdi + 0xc0]
00298A0E  mov      word ptr [rax + 8], dx
00298A12  jmp      0x298aae  ; -> 00298AAE
00298A17  mov      ecx, 0xfffb
00298A1C  and      word ptr [rax + 2], cx
00298A20  mov      ecx, 0x400
00298A25  mov      rax, qword ptr [rdi + 0xc0]
00298A2C  mov      word ptr [rax + 8], cx
00298A30  cmp      word ptr [rsi + 0x5c], bx
00298A34  jae      0x298a98  ; -> 00298A98
00298A36  test     dword ptr [rsi], 0x2000
00298A3C  je       0x298a98  ; -> 00298A98
00298A3E  mov      eax, dword ptr [rsi + 0x40]
00298A41  cmp      dword ptr [rsi + 0x3c], eax
00298A44  jl       0x298a7b  ; -> 00298A7B
00298A46  mov      rax, qword ptr [rdi + 0xc0]
00298A4D  mov      r14d, r8d
00298A50  mov      r15d, r8d
00298A53  mov      byte ptr [rax + 0x13], 0x64
00298A57  mov      rcx, qword ptr [rdi + 0xc0]
00298A5E  movzx    eax, byte ptr [rcx + 7]
00298A62  cmp      al, 0x80
00298A64  jae      0x298aae  ; -> 00298AAE
00298A66  movzx    eax, al
00298A69  mov      edx, 0x80
00298A6E  add      eax, 0x10
00298A71  cmp      eax, edx
00298A73  cmovg    eax, edx
00298A76  mov      byte ptr [rcx + 7], al
00298A79  jmp      0x298aae  ; -> 00298AAE
00298A7B  mov      rcx, qword ptr [rdi + 0xc0]
00298A82  movzx    eax, byte ptr [rcx + 7]
00298A86  test     al, al
00298A88  je       0x298aae  ; -> 00298AAE
00298A8A  movzx    eax, al
00298A8D  sub      eax, 0x10
00298A90  cmovs    eax, edx
00298A93  mov      byte ptr [rcx + 7], al
00298A96  jmp      0x298aae  ; -> 00298AAE
00298A98  test     dword ptr [rsi], 0x8000
00298A9E  jne      0x298aab  ; -> 00298AAB
00298AA0  mov      rax, qword ptr [rdi + 0xc0]
00298AA7  mov      byte ptr [rax + 0x13], 0
00298AAB  mov      r15d, edx
00298AAE  call     0x36d830  ; -> 0036D830 fn
00298AB3  mov      ebx, 4
00298AB8  test     eax, eax
00298ABA  jne      0x298ae2  ; -> 00298AE2
00298ABC  mov      rax, qword ptr [rdi + 0xc0]
00298AC3  lea      r9d, [rbx - 3]
00298AC7  mov      edx, ebx
00298AC9  lea      rcx, [rbp - 0x79]
00298ACD  movsx    r8d, word ptr [rax + 8]
00298AD2  call     0x274870  ; -> 00274870 fn
00298AD7  mov      rcx, qword ptr [rdi + 0xc0]
00298ADE  mov      word ptr [rcx + 8], ax
00298AE2  mov      rax, qword ptr [rdi + 0xc0]
00298AE9  lea      rcx, [rbp - 0x79]
00298AED  mov      edx, ebx
00298AEF  movsx    r8d, word ptr [rax + 8]
00298AF4  call     0x271e50  ; -> 00271E50 fn
00298AF9  mov      rbx, qword ptr [rdi + 0xc0]
00298B00  xorps    xmm0, xmm0
00298B03  mov      dword ptr [rbp + 0x17], eax
00298B06  mov      eax, dword ptr [rip + 0x1df6a64]  ; -> 0208F570
00298B0C  cvtsi2ss xmm0, rax
00298B11  mulss    xmm0, dword ptr [rip + 0x1a53137]  ; -> 01CEBC50 [f32 3.141593]
00298B19  divss    xmm0, dword ptr [rip + 0x67d7f3]  ; -> 00916314 [f32 15]
00298B21  call     0x861f0e  ; -> 00861F0E fn
00298B26  movzx    eax, byte ptr [rbx + 7]
00298B2A  mov      edx, 0xff
00298B2F  shl      eax, 6
00298B32  mov      r10d, 0x4000
00298B38  sar      eax, 7
00298B3B  movd     xmm1, eax
00298B3F  movzx    eax, byte ptr [rbp + 0x17]
00298B43  cvtdq2ps xmm1, xmm1
00298B46  mulss    xmm0, xmm1
00298B4A  addss    xmm0, dword ptr [rip + 0x65aeda]  ; -> 008F3A2C [f32 128]
00298B52  cvttss2si rcx, xmm0
00298B57  imul     eax, ecx
00298B5A  shr      eax, 7
00298B5D  cmp      eax, edx
00298B5F  cmovge   eax, edx
00298B62  mov      byte ptr [rbp + 0x17], al
00298B65  movzx    eax, byte ptr [rbp + 0x18]
00298B69  imul     eax, ecx
00298B6C  shr      eax, 7
00298B6F  cmp      eax, edx
00298B71  cmovge   eax, edx
00298B74  mov      byte ptr [rbp + 0x18], al
00298B77  movzx    eax, byte ptr [rbp + 0x19]
00298B7B  imul     eax, ecx
00298B7E  shr      eax, 7
00298B81  cmp      eax, edx
00298B83  cmovge   eax, edx
00298B86  mov      byte ptr [rbp + 0x19], al
00298B89  movzx    eax, byte ptr [rbx + 6]
00298B8D  mov      byte ptr [rbp + 0x1a], al
00298B90  mov      eax, dword ptr [rbp + 0x17]
00298B93  mov      dword ptr [r13 + 0x24], eax
00298B97  test     dword ptr [rsi], 0x8000
00298B9D  je       0x298bb3  ; -> 00298BB3
00298B9F  cmp      r12w, r10w
00298BA3  jae      0x298bb3  ; -> 00298BB3
00298BA5  mov      rax, qword ptr [rdi + 0xc0]
00298BAC  movsx    r8d, byte ptr [rax + 0x13]
00298BB1  jmp      0x298bdb  ; -> 00298BDB
00298BB3  cmp      word ptr [rsi + 0x5c], r10w
00298BB8  jae      0x298bbf  ; -> 00298BBF
00298BBA  cmp      r15d, r14d
00298BBD  jge      0x298bd0  ; -> 00298BD0
00298BBF  mov      rax, qword ptr [rdi + 0xc0]
00298BC6  cmp      byte ptr [rax + 0xa], 1
00298BCA  jne      0x298bd0  ; -> 00298BD0
00298BCC  mov      byte ptr [rax + 0xa], 2
00298BD0  imul     eax, r15d, 0x64
00298BD4  cdq      
00298BD5  idiv     r14d
00298BD8  mov      r8d, eax
00298BDB  mov      rcx, qword ptr [rdi + 0xc0]
00298BE2  mov      eax, 0xfff7
00298BE7  and      word ptr [rcx + 2], ax
00298BEB  test     dword ptr [rsi], 0x1100
00298BF1  je       0x298bff  ; -> 00298BFF
00298BF3  mov      rcx, qword ptr [rdi + 0xc0]
00298BFA  or       word ptr [rcx + 2], 8
00298BFF  test     dword ptr [rsi], 0x8100
00298C05  jne      0x298c20  ; -> 00298C20
00298C07  mov      eax, dword ptr [rsi + 0x40]
00298C0A  cmp      dword ptr [rsi + 0x3c], eax
00298C0D  jge      0x298c20  ; -> 00298C20
00298C0F  mov      rax, qword ptr [rdi + 0xc0]
00298C16  cmp      byte ptr [rax + 0xa], 1
00298C1A  jne      0x298c20  ; -> 00298C20
00298C1C  mov      byte ptr [rax + 0xa], 2
00298C20  mov      rdx, qword ptr [rdi + 0xc0]
00298C27  mov      rax, qword ptr [rdi + 0x60]
00298C2B  movzx    ecx, byte ptr [rdx + 0xa]
00298C2F  mov      r14, qword ptr [rax]
00298C32  test     ecx, ecx
00298C34  je       0x298e8d  ; -> 00298E8D
00298C3A  sub      ecx, 1
00298C3D  je       0x298d67  ; -> 00298D67
00298C43  cmp      ecx, 1
00298C46  jne      0x298d2e  ; -> 00298D2E
00298C4C  add      word ptr [rdx + 0x10], 0x10
00298C51  mov      ecx, 0x100
00298C56  mov      rax, qword ptr [rdi + 0xc0]
00298C5D  cmp      word ptr [rax + 0x10], cx
00298C61  jl       0x298c8a  ; -> 00298C8A
00298C63  mov      word ptr [rax + 0x10], cx
00298C67  mov      rax, qword ptr [rdi + 0xc0]
00298C6E  test     byte ptr [rax + 2], 8
00298C72  je       0x298c7b  ; -> 00298C7B
00298C74  cmp      word ptr [rsi + 0x5c], r10w
00298C79  jb       0x298c8a  ; -> 00298C8A
00298C7B  mov      byte ptr [rax + 0xa], 0
00298C7F  mov      rax, qword ptr [rdi + 0xc0]
00298C86  mov      byte ptr [rax + 0x13], 0
00298C8A  mov      rax, qword ptr [rdi + 0xc0]
00298C91  lea      r8, [rbp + 7]
00298C95  lea      rdx, [rbp - 9]
00298C99  lea      rcx, [rsp + 0x30]
00298C9E  movsx    r9d, word ptr [rax + 0x10]
00298CA3  call     0x2752e0  ; -> 002752E0 fn
00298CA8  mov      rax, qword ptr [rdi + 0xc0]
00298CAF  lea      r8, [rbp - 0x59]
00298CB3  lea      rdx, [rbp - 0x39]
00298CB7  lea      rcx, [rsp + 0x40]
00298CBC  movsx    r9d, word ptr [rax + 0x10]
00298CC1  call     0x2752e0  ; -> 002752E0 fn
00298CC6  movzx    eax, byte ptr [rsp + 0x30]
00298CCB  lea      rdx, [rbp + 0x17]
00298CCF  mov      byte ptr [rbp + 0x17], al
00298CD2  mov      r8d, 1
00298CD8  movzx    eax, byte ptr [rsp + 0x34]
00298CDD  mov      rcx, r14
00298CE0  mov      byte ptr [rbp + 0x18], al
00298CE3  movzx    eax, byte ptr [rsp + 0x38]
00298CE8  mov      byte ptr [rbp + 0x19], al
00298CEB  movzx    eax, byte ptr [rsp + 0x3c]
00298CF0  mov      byte ptr [rbp + 0x1a], al
00298CF3  movzx    eax, byte ptr [rsp + 0x40]
00298CF8  mov      byte ptr [rsp + 0x20], al
00298CFC  movzx    eax, byte ptr [rsp + 0x44]
00298D01  mov      byte ptr [rsp + 0x21], al
00298D05  movzx    eax, byte ptr [rsp + 0x48]
00298D0A  mov      byte ptr [rsp + 0x22], al
00298D0E  movzx    eax, byte ptr [rbp - 0x7d]
00298D12  mov      byte ptr [rsp + 0x23], al
00298D16  call     0x29f480  ; -> 0029F480 fn
00298D1B  mov      r8d, 2
00298D21  lea      rdx, [rsp + 0x20]
00298D26  mov      rcx, r14
00298D29  call     0x29f480  ; -> 0029F480 fn
00298D2E  xor      r15d, r15d
00298D31  test     dword ptr [rsi], 0x1000
00298D37  mov      rax, qword ptr [rdi + 0x60]
00298D3B  mov      dword ptr [rsp + 0x20], 0x80808080
00298D43  mov      rdx, qword ptr [rax + 0x20]
00298D47  jne      0x299022  ; -> 00299022
00298D4D  mov      rcx, qword ptr [rdi + 0xc0]
00298D54  movzx    eax, byte ptr [rcx + 0x12]
00298D58  sub      eax, 0x10
00298D5B  cmovs    eax, r15d
00298D5F  mov      byte ptr [rcx + 0x12], al
00298D62  jmp      0x29903e  ; -> 0029903E
00298D67  or       dword ptr [r14 + 0x20], 0x4000000
00298D6F  mov      rcx, qword ptr [rdi + 0xc0]
00298D76  movzx    eax, byte ptr [rcx + 0xb]
00298D7A  test     al, al
00298D7C  je       0x298d83  ; -> 00298D83
00298D7E  dec      al
00298D80  mov      byte ptr [rcx + 0xb], al
00298D83  mov      rcx, qword ptr [rdi + 0xc0]
00298D8A  test     byte ptr [rcx + 2], 8
00298D8E  jne      0x298d99  ; -> 00298D99
00298D90  movsx    eax, byte ptr [rcx + 0x13]
00298D94  cmp      r8d, eax
00298D97  jge      0x298db8  ; -> 00298DB8
00298D99  cmp      byte ptr [rcx + 0xb], 0
00298D9D  jne      0x298db8  ; -> 00298DB8
00298D9F  mov      byte ptr [rcx + 0xa], 2
00298DA3  xor      ecx, ecx
00298DA5  mov      rax, qword ptr [rdi + 0xc0]
00298DAC  mov      word ptr [rax + 0x10], cx
00298DB0  and      dword ptr [r14 + 0x20], 0xfbffffff
00298DB8  mov      rax, qword ptr [rdi + 0xc0]
00298DBF  xorps    xmm0, xmm0
00298DC2  mov      ecx, dword ptr [rip + 0x1df67a8]  ; -> 0208F570
00298DC8  sub      ecx, dword ptr [rax + 0xc]
00298DCB  mov      eax, ecx
00298DCD  cvtsi2ss xmm0, rax
00298DD2  mulss    xmm0, dword ptr [rip + 0x1a52e76]  ; -> 01CEBC50 [f32 3.141593]
00298DDA  divss    xmm0, dword ptr [rip + 0x67d532]  ; -> 00916314 [f32 15]
00298DE2  call     0x861f0e  ; -> 00861F0E fn
00298DE7  mulss    xmm0, dword ptr [rip + 0x65ac3d]  ; -> 008F3A2C [f32 128]
00298DEF  lea      r8, [rbp - 9]
00298DF3  lea      rdx, [rbp - 0x19]
00298DF7  lea      rcx, [rsp + 0x40]
00298DFC  cvttss2si eax, xmm0
00298E00  movsx    ebx, ax
00298E03  lea      r9d, [rbx + 0x80]
00298E0A  call     0x2752e0  ; -> 002752E0 fn
00298E0F  lea      r9d, [rbx + 0x80]
00298E16  lea      r8, [rbp - 0x39]
00298E1A  lea      rdx, [rbp - 0x49]
00298E1E  lea      rcx, [rsp + 0x30]
00298E23  call     0x2752e0  ; -> 002752E0 fn
00298E28  movzx    eax, byte ptr [rsp + 0x40]
00298E2D  lea      rdx, [rsp + 0x20]
00298E32  mov      byte ptr [rsp + 0x20], al
00298E36  mov      r8d, 1
00298E3C  movzx    eax, byte ptr [rsp + 0x44]
00298E41  mov      rcx, r14
00298E44  mov      byte ptr [rsp + 0x21], al
00298E48  movzx    eax, byte ptr [rsp + 0x48]
00298E4D  mov      byte ptr [rsp + 0x22], al
00298E51  movzx    eax, byte ptr [rbp - 0x7d]
00298E55  mov      byte ptr [rsp + 0x23], al
00298E59  movzx    eax, byte ptr [rsp + 0x30]
00298E5E  mov      byte ptr [rbp + 0x17], al
00298E61  movzx    eax, byte ptr [rsp + 0x34]
00298E66  mov      byte ptr [rbp + 0x18], al
00298E69  movzx    eax, byte ptr [rsp + 0x38]
00298E6E  mov      byte ptr [rbp + 0x19], al
00298E71  movzx    eax, byte ptr [rsp + 0x3c]
00298E76  mov      byte ptr [rbp + 0x1a], al
00298E79  call     0x29f480  ; -> 0029F480 fn
00298E7E  mov      r8d, 2
00298E84  lea      rdx, [rbp + 0x17]
00298E88  jmp      0x298d26  ; -> 00298D26
00298E8D  movzx    eax, byte ptr [rdx + 0x13]
00298E91  xor      r15d, r15d
00298E94  mov      r9d, r15d
00298E97  cmp      al, 0x64
00298E99  jl       0x298ee0  ; -> 00298EE0
00298E9B  cmp      word ptr [rsi + 0x5c], r10w
00298EA0  jae      0x298ee0  ; -> 00298EE0
00298EA2  mov      byte ptr [rdx + 0xa], 1
00298EA6  lea      r9d, [r15 + 1]
00298EAA  mov      eax, dword ptr [rip + 0x1df66c0]  ; -> 0208F570
00298EB0  mov      rcx, qword ptr [rdi + 0xc0]
00298EB7  mov      dword ptr [rcx + 0xc], eax
00298EBA  or       dword ptr [r14 + 0x20], 0x4000000
00298EC2  mov      byte ptr [r14 + 0x21], 0x80
00298EC7  mov      rax, qword ptr [rdi + 0xc0]
00298ECE  mov      byte ptr [rax + 0xb], 8
00298ED2  mov      rax, qword ptr [rdi + 0xc0]
00298ED9  mov      word ptr [rax + 0x16], r15w
00298EDE  jmp      0x298f37  ; -> 00298F37
00298EE0  movsx    eax, al
00298EE3  cmp      r8d, eax
00298EE6  jl       0x298eef  ; -> 00298EEF
00298EE8  mov      word ptr [rdx + 0x16], r15w
00298EED  jmp      0x298f37  ; -> 00298F37
00298EEF  and      dword ptr [r14 + 0x20], 0xfbffffff
00298EF7  mov      rax, qword ptr [rdi + 0xc0]
00298EFE  mov      word ptr [rax + 0x10], r15w
00298F03  mov      rax, qword ptr [rdi + 0xc0]
00298F0A  inc      word ptr [rax + 0x16]
00298F0E  mov      rax, qword ptr [rdi + 0xc0]
00298F15  cmp      word ptr [rax + 0x16], 4
00298F1A  jge      0x298f23  ; -> 00298F23
00298F1C  movsx    r8d, byte ptr [rax + 0x13]
00298F21  jmp      0x298f2c  ; -> 00298F2C
00298F23  mov      ecx, 4
00298F28  mov      word ptr [rax + 0x16], cx
00298F2C  mov      rax, qword ptr [rdi + 0xc0]
00298F33  mov      byte ptr [rax + 0x13], r8b
00298F37  mov      rax, qword ptr [rdi + 0xc0]
00298F3E  shl      r9d, 0x1a
00298F42  mov      byte ptr [rax + 0x13], r8b
00298F46  mov      rax, qword ptr [rdi + 0xc0]
00298F4D  movsx    ecx, byte ptr [rax + 0x13]
00298F51  mov      eax, 0x51eb851f
00298F56  and      dword ptr [r14 + 0x20], 0xfbffffff
00298F5E  or       dword ptr [r14 + 0x20], r9d
00298F62  shl      ecx, 8
00298F65  imul     ecx
00298F67  mov      rcx, r14
00298F6A  mov      ebx, edx
00298F6C  sar      ebx, 5
00298F6F  mov      eax, ebx
00298F71  shr      eax, 0x1f
00298F74  add      ebx, eax
00298F76  mov      rax, qword ptr [rdi + 0xc0]
00298F7D  movsx    edx, byte ptr [rax + 0x13]
00298F81  call     0x225580  ; -> 00225580 fn
00298F86  mov      r9d, ebx
00298F89  mov      byte ptr [r14 + 0x21], 0x80
00298F8E  lea      r8, [rbp - 0x19]
00298F92  lea      rdx, [rbp - 0x29]
00298F96  lea      rcx, [rsp + 0x40]
00298F9B  call     0x2752e0  ; -> 002752E0 fn
00298FA0  mov      r9d, ebx
00298FA3  lea      r8, [rbp - 0x49]
00298FA7  lea      rdx, [rbp - 0x59]
00298FAB  lea      rcx, [rsp + 0x30]
00298FB0  call     0x2752e0  ; -> 002752E0 fn
00298FB5  movzx    eax, byte ptr [rsp + 0x40]
00298FBA  lea      rdx, [rsp + 0x20]
00298FBF  mov      byte ptr [rsp + 0x20], al
00298FC3  mov      r8d, 1
00298FC9  movzx    eax, byte ptr [rsp + 0x44]
00298FCE  mov      rcx, r14
00298FD1  mov      byte ptr [rsp + 0x21], al
00298FD5  movzx    eax, byte ptr [rsp + 0x48]
00298FDA  mov      byte ptr [rsp + 0x22], al
00298FDE  movzx    eax, byte ptr [rbp - 0x7d]
00298FE2  mov      byte ptr [rsp + 0x23], al
00298FE6  movzx    eax, byte ptr [rsp + 0x30]
00298FEB  mov      byte ptr [rbp + 0x17], al
00298FEE  movzx    eax, byte ptr [rsp + 0x34]
00298FF3  mov      byte ptr [rbp + 0x18], al
00298FF6  movzx    eax, byte ptr [rsp + 0x38]
00298FFB  mov      byte ptr [rbp + 0x19], al
00298FFE  movzx    eax, byte ptr [rsp + 0x3c]
00299003  mov      byte ptr [rbp + 0x1a], al
00299006  call     0x29f480  ; -> 0029F480 fn
0029900B  mov      r8d, 2
00299011  lea      rdx, [rbp + 0x17]
00299015  mov      rcx, r14
00299018  call     0x29f480  ; -> 0029F480 fn
0029901D  jmp      0x298d31  ; -> 00298D31
00299022  mov      rax, qword ptr [rdi + 0xc0]
00299029  add      byte ptr [rax + 0x12], 0x10
0029902D  mov      rax, qword ptr [rdi + 0xc0]
00299034  cmp      byte ptr [rax + 0x12], 0x80
00299038  jbe      0x29903e  ; -> 0029903E
0029903A  mov      byte ptr [rax + 0x12], 0x80
0029903E  mov      rax, qword ptr [rdi + 0xc0]
00299045  movzx    ecx, byte ptr [rax + 0x12]
00299049  mov      byte ptr [rsp + 0x23], cl
0029904D  mov      eax, dword ptr [rsp + 0x20]
00299051  mov      dword ptr [rdx + 0x34], eax
00299054  mov      dword ptr [rdx + 0x30], eax
00299057  mov      dword ptr [rdx + 0x2c], eax
0029905A  mov      dword ptr [rdx + 0x28], eax
0029905D  mov      rcx, qword ptr [rbp + 0x1f]
00299061  xor      rcx, rsp
00299064  call     0x808c40  ; -> 00808C40 fn
00299069  mov      rbx, qword ptr [rsp + 0x140]
00299071  add      rsp, 0xf0
00299078  pop      r15
0029907A  pop      r14
0029907C  pop      r13
0029907E  pop      r12
00299080  pop      rdi
00299081  pop      rsi
00299082  pop      rbp
00299083  ret      
```

## 002EAD00 (80 B, extent 002EAD00-002EAD50)

Page context: "FDF70'/'00615BC0'/'00616700'/'00624660'/'00624670'/'0065C750' - the render-pass record's resize-on-change.  Interior anchor '00193B10' (function '00193AD0').  '002FCCC0' (562 B) is the keyed release '002EAD00' and '003B8670' call: 'r9d & 0x3F < 0x30' selects a 0x38-stride record of '02EC32E0', '[rdi]' must equal the key and 'byte[+0x23] & 0xF == 5', then the '02EC3D60' list sums 'word[+0x20]'-indexed '& 0x1F' fields, '003AFFB0(0x24 - su"

```
002EAD00  mov      qword ptr [rsp + 8], rbx
002EAD05  mov      qword ptr [rsp + 0x10], rbp
002EAD0A  mov      qword ptr [rsp + 0x18], rsi
002EAD0F  push     rdi
002EAD10  sub      rsp, 0x20
002EAD14  mov      edi, r9d
002EAD17  mov      rsi, r8
002EAD1A  mov      ebx, edx
002EAD1C  mov      ebp, ecx
002EAD1E  test     edx, edx
002EAD20  jne      0x2ead26  ; -> 002EAD26
002EAD22  xor      eax, eax
002EAD24  jmp      0x2ead3b  ; -> 002EAD3B
002EAD26  call     0x42fcb0  ; -> 0042FCB0 fn
002EAD2B  mov      r9d, edi
002EAD2E  mov      r8d, ebx
002EAD31  mov      rdx, rsi
002EAD34  mov      ecx, ebp
002EAD36  call     0x2fccc0  ; -> 002FCCC0 fn
002EAD3B  mov      rbx, qword ptr [rsp + 0x30]
002EAD40  mov      rbp, qword ptr [rsp + 0x38]
002EAD45  mov      rsi, qword ptr [rsp + 0x40]
002EAD4A  add      rsp, 0x20
002EAD4E  pop      rdi
002EAD4F  ret      
```

## 003326F0 (96 B, extent 003326F0-00332750)

Page context: "rappers | '003A8C80', '003A8CB0', '003A8CE0', '003A8D40' (33–89 B each on '02EBEF88'), '003A8DD0' (423 B — '001EDDA0'/'003A8AE0'/'002F31C0'), '003A8290' ('004FF080'/'004FF0D0', '02EBEF98'); wrappers '003326F0'/'00333430'/'003335A0'/'00333A40' (each '0046EE70' + '003697F0' + one '003A8Cxx') | a shared sub-object at '02EBEF88' with four field ops plus one larger step — '0046EE70'/'003697F0' bracket it | | hit/target helpers | '00322850' ("

```
003326F0  test     rcx, rcx
003326F3  je       0x33274f  ; -> 0033274F
003326F5  push     rsi
003326F6  sub      rsp, 0x20
003326FA  mov      qword ptr [rsp + 0x30], rbx
003326FF  mov      rsi, rcx
00332702  mov      qword ptr [rsp + 0x38], rbp
00332707  xor      ebp, ebp
00332709  mov      ebx, ebp
0033270B  mov      qword ptr [rsp + 0x40], rdi
00332710  mov      rdi, qword ptr [rsi + rbx*8]
00332714  test     rdi, rdi
00332717  je       0x33272d  ; -> 0033272D
00332719  mov      rcx, rdi
0033271C  call     0x46ee70  ; -> 0046EE70 fn
00332721  mov      rcx, rdi
00332724  call     0x3697f0  ; -> 003697F0 fn
00332729  mov      qword ptr [rsi + rbx*8], rbp
0033272D  inc      rbx
00332730  cmp      rbx, 0x10
00332734  jl       0x332710  ; -> 00332710
00332736  call     0x3a8c80  ; -> 003A8C80 fn
0033273B  mov      rdi, qword ptr [rsp + 0x40]
00332740  mov      rbp, qword ptr [rsp + 0x38]
00332745  mov      rbx, qword ptr [rsp + 0x30]
0033274A  add      rsp, 0x20
0033274E  pop      rsi
0033274F  ret      
```

## 00333430 (117 B, extent 00333430-003334A5)

Page context: "003A8C80', '003A8CB0', '003A8CE0', '003A8D40' (33–89 B each on '02EBEF88'), '003A8DD0' (423 B — '001EDDA0'/'003A8AE0'/'002F31C0'), '003A8290' ('004FF080'/'004FF0D0', '02EBEF98'); wrappers '003326F0'/'00333430'/'003335A0'/'00333A40' (each '0046EE70' + '003697F0' + one '003A8Cxx') | a shared sub-object at '02EBEF88' with four field ops plus one larger step — '0046EE70'/'003697F0' bracket it | | hit/target helpers | '00322850' (the §12 pos"

```
00333430  test     rcx, rcx
00333433  je       0x3334a4  ; -> 003334A4
00333435  mov      qword ptr [rsp + 0x18], rbx
0033343A  push     rsi
0033343B  sub      rsp, 0x20
0033343F  mov      rsi, rdx
00333442  mov      rbx, rcx
00333445  test     rdx, rdx
00333448  je       0x33349a  ; -> 0033349A
0033344A  mov      qword ptr [rsp + 0x30], rbp
0033344F  xor      ebp, ebp
00333451  mov      qword ptr [rsp + 0x38], rdi
00333456  mov      edi, 0x10
0033345B  nop      dword ptr [rax + rax]
00333460  mov      rcx, qword ptr [rbx]
00333463  test     rcx, rcx
00333466  je       0x33347d  ; -> 0033347D
00333468  cmp      rcx, rsi
0033346B  je       0x33347d  ; -> 0033347D
0033346D  call     0x46ee70  ; -> 0046EE70 fn
00333472  mov      rcx, qword ptr [rbx]
00333475  call     0x3697f0  ; -> 003697F0 fn
0033347A  mov      qword ptr [rbx], rbp
0033347D  add      rbx, 8
00333481  sub      rdi, 1
00333485  jne      0x333460  ; -> 00333460
00333487  movzx    ecx, word ptr [rsi + 8]
0033348B  call     0x3a8660  ; -> 003A8660 fn
00333490  mov      rdi, qword ptr [rsp + 0x38]
00333495  mov      rbp, qword ptr [rsp + 0x30]
0033349A  mov      rbx, qword ptr [rsp + 0x40]
0033349F  add      rsp, 0x20
003334A3  pop      rsi
003334A4  ret      
```

## 00333520 (123 B, extent 00333520-0033359B)

Page context: "'/'A8'/'AC'/'B4'/'BC' + '003A6D90'/'003588B0'/'00265020'/'00265200'/'00263F70'/'00263E70'/'003B7E10'), '0024C3C0' ('020910A0'/'02092170'), '0024F9B0' ('020925A0'–'B4' cells + '0026A430'/'0026AF80'), '00333520', '00333640', '003A4070' ('02096A20' + '003B0BF0'), '003A7F60' ('02EBEF98' + '003697F0'), '003B8260' (1,028 B — '0020E600' ×7 + resolve '003E1350'/'003E1610' + '003B3CA0' ×2, '00D115BC'–'E0' table + '02EBA4F0'; interior verified 20"

```
00333520  test     rcx, rcx
00333523  je       0x33359a  ; -> 0033359A
00333525  test     rdx, rdx
00333528  je       0x33359a  ; -> 0033359A
0033352A  cmp      r8d, 2
0033352E  jl       0x333430  ; -> 00333430 fn
00333534  mov      rax, qword ptr [rip + 0x2c63e0d]  ; -> 02F97348
0033353B  mov      ecx, 0x1000
00333540  or       word ptr [rax + 0x368], cx
00333547  mov      ecx, 0xdfff
0033354C  mov      rax, qword ptr [rip + 0x2c63df5]  ; -> 02F97348
00333553  and      word ptr [rax + 0x368], cx
0033355A  mov      rax, qword ptr [rip + 0x2c63de7]  ; -> 02F97348
00333561  movzx    ecx, word ptr [rdx + 8]
00333565  mov      dword ptr [rax + 0x37c], ecx
0033356B  mov      rax, qword ptr [rip + 0x2c63dd6]  ; -> 02F97348
00333572  mov      word ptr [rax + 0x358], r8w
0033357A  mov      rax, qword ptr [rip + 0x2c63dc7]  ; -> 02F97348
00333581  mov      word ptr [rax + 0x35a], r8w
00333589  mov      rax, qword ptr [rip + 0x2c63db8]  ; -> 02F97348
00333590  mov      dword ptr [rax + 0x35c], 0x3f800000
0033359A  ret      
```

## 003335A0 (117 B, extent 003335A0-00333615)

Page context: "'003A8CB0', '003A8CE0', '003A8D40' (33–89 B each on '02EBEF88'), '003A8DD0' (423 B — '001EDDA0'/'003A8AE0'/'002F31C0'), '003A8290' ('004FF080'/'004FF0D0', '02EBEF98'); wrappers '003326F0'/'00333430'/'003335A0'/'00333A40' (each '0046EE70' + '003697F0' + one '003A8Cxx') | a shared sub-object at '02EBEF88' with four field ops plus one larger step — '0046EE70'/'003697F0' bracket it | | hit/target helpers | '00322850' (the §12 post-hit call "

```
003335A0  test     rcx, rcx
003335A3  je       0x333614  ; -> 00333614
003335A5  mov      qword ptr [rsp + 0x18], rbx
003335AA  push     rsi
003335AB  sub      rsp, 0x20
003335AF  mov      rsi, rdx
003335B2  mov      rbx, rcx
003335B5  test     rdx, rdx
003335B8  je       0x33360a  ; -> 0033360A
003335BA  mov      qword ptr [rsp + 0x30], rbp
003335BF  xor      ebp, ebp
003335C1  mov      qword ptr [rsp + 0x38], rdi
003335C6  mov      edi, 0x10
003335CB  nop      dword ptr [rax + rax]
003335D0  mov      rcx, qword ptr [rbx]
003335D3  test     rcx, rcx
003335D6  je       0x3335ed  ; -> 003335ED
003335D8  cmp      rcx, rsi
003335DB  je       0x3335ed  ; -> 003335ED
003335DD  call     0x46ee70  ; -> 0046EE70 fn
003335E2  mov      rcx, qword ptr [rbx]
003335E5  call     0x3697f0  ; -> 003697F0 fn
003335EA  mov      qword ptr [rbx], rbp
003335ED  add      rbx, 8
003335F1  sub      rdi, 1
003335F5  jne      0x3335d0  ; -> 003335D0
003335F7  movzx    ecx, word ptr [rsi + 8]
003335FB  call     0x3a8cb0  ; -> 003A8CB0 fn
00333600  mov      rdi, qword ptr [rsp + 0x38]
00333605  mov      rbp, qword ptr [rsp + 0x30]
0033360A  mov      rbx, qword ptr [rsp + 0x40]
0033360F  add      rsp, 0x20
00333613  pop      rsi
00333614  ret      
```

## 00333620 (20 B, extent 00333620-00333634)

Page context: "46CC20' ('002E9D90'), '003D7C50' ('02EBBA00') | resolve-and-apply steps behind the hit/placement opcodes | | leaves | '0017F2A0' ('00189120'/'0018CA40'/'0018B8B0' — a command-list emit), '003333B0', '00333620', '00379940' | small bodies the arms call |  This confirms §12's shape from the callee side: the singleton context '02F97348' and the target array '02EBA4F0' dominate the subtree exactly as the opcode analysis describes. The '02EBE"

```
00333620  test     rcx, rcx
00333623  je       0x333633  ; -> 00333633
00333625  test     rdx, rdx
00333628  je       0x333633  ; -> 00333633
0033362A  movzx    ecx, word ptr [rdx + 8]
0033362E  jmp      0x3a8ce0  ; -> 003A8CE0 fn
00333633  ret      
```

## 00333640 (123 B, extent 00333640-003336BB)

Page context: "'B4'/'BC' + '003A6D90'/'003588B0'/'00265020'/'00265200'/'00263F70'/'00263E70'/'003B7E10'), '0024C3C0' ('020910A0'/'02092170'), '0024F9B0' ('020925A0'–'B4' cells + '0026A430'/'0026AF80'), '00333520', '00333640', '003A4070' ('02096A20' + '003B0BF0'), '003A7F60' ('02EBEF98' + '003697F0'), '003B8260' (1,028 B — '0020E600' ×7 + resolve '003E1350'/'003E1610' + '003B3CA0' ×2, '00D115BC'–'E0' table + '02EBA4F0'; interior verified 2026-09-17, SW"

```
00333640  test     rcx, rcx
00333643  je       0x3336ba  ; -> 003336BA
00333645  test     rdx, rdx
00333648  je       0x3336ba  ; -> 003336BA
0033364A  cmp      r8d, 2
0033364E  jl       0x3336c0  ; -> 003336C0 fn
00333654  mov      rax, qword ptr [rip + 0x2c63ced]  ; -> 02F97348
0033365B  mov      ecx, 0x2000
00333660  or       word ptr [rax + 0x368], cx
00333667  mov      ecx, 0xefff
0033366C  mov      rax, qword ptr [rip + 0x2c63cd5]  ; -> 02F97348
00333673  and      word ptr [rax + 0x368], cx
0033367A  mov      rax, qword ptr [rip + 0x2c63cc7]  ; -> 02F97348
00333681  movzx    ecx, word ptr [rdx + 8]
00333685  mov      dword ptr [rax + 0x37c], ecx
0033368B  mov      rax, qword ptr [rip + 0x2c63cb6]  ; -> 02F97348
00333692  mov      word ptr [rax + 0x358], r8w
0033369A  mov      rax, qword ptr [rip + 0x2c63ca7]  ; -> 02F97348
003336A1  mov      word ptr [rax + 0x35a], r8w
003336A9  mov      rax, qword ptr [rip + 0x2c63c98]  ; -> 02F97348
003336B0  mov      dword ptr [rax + 0x35c], 0x3f800000
003336BA  ret      
```

## 00370390 (14 B, extent 00370390-0037039E)

Page context: "0428AF0'/'00428CD0' plus '022C6F28'. Interior anchor '004655ED' (a '00428AF0' call).  ## SWE2-EC7-59 update (2026-09-19) - '0046E640'  '0046E640' (161 B) is an ownerless body - '0020E620'/'002ED570'/'00370390'. Interior anchor '0046E66E' (a '002ED570' call).   ## SWE2-EC7-59 update (2026-09-19) - '003A7F60'  '003A7F60' (160 B) is an ownerless action-context arm - '003697F0' single call plus '02EBEF98'/'02F97348'. Interior anchor '003A7F"

```
00370390  cmp      dword ptr [rcx + 0x9c], 2
00370397  je       0x373160  ; -> 00373160 fn
0037039D  ret      
```

## 003A4070 (122 B, extent 003A4070-003A40EA)

Page context: "'003A6D90'/'003588B0'/'00265020'/'00265200'/'00263F70'/'00263E70'/'003B7E10'), '0024C3C0' ('020910A0'/'02092170'), '0024F9B0' ('020925A0'–'B4' cells + '0026A430'/'0026AF80'), '00333520', '00333640', '003A4070' ('02096A20' + '003B0BF0'), '003A7F60' ('02EBEF98' + '003697F0'), '003B8260' (1,028 B — '0020E600' ×7 + resolve '003E1350'/'003E1610' + '003B3CA0' ×2, '00D115BC'–'E0' table + '02EBA4F0'; interior verified 2026-09-17, SWE2-FRONTIER "

```
003A4070  push     rbx
003A4072  sub      rsp, 0x20
003A4076  movsxd   rbx, ecx
003A4079  mov      eax, 0x200
003A407E  mov      rcx, qword ptr [rip + 0x2bf32c3]  ; -> 02F97348
003A4085  test     word ptr [rcx + 0x378], ax
003A408C  jne      0x3a40de  ; -> 003A40DE
003A408E  movzx    edx, byte ptr [rcx]
003A4091  cmp      dl, 3
003A4094  je       0x3a40d5  ; -> 003A40D5
003A4096  lea      eax, [rdx - 5]
003A4099  test     al, 0xfa
003A409B  jne      0x3a40bc  ; -> 003A40BC
003A409D  cmp      dl, 0xa
003A40A0  je       0x3a40bc  ; -> 003A40BC
003A40A2  mov      ecx, dword ptr [rcx + 4]
003A40A5  call     0x3b0bf0  ; -> 003B0BF0 fn
003A40AA  test     rax, rax
003A40AD  je       0x3a40d5  ; -> 003A40D5
003A40AF  cmp      byte ptr [rax + 0x11], 1
003A40B3  je       0x3a40d5  ; -> 003A40D5
003A40B5  mov      rcx, qword ptr [rip + 0x2bf328c]  ; -> 02F97348
003A40BC  cmp      ebx, -1
003A40BF  je       0x3a40cc  ; -> 003A40CC
003A40C1  mov      eax, dword ptr [rcx + rbx*4 + 0x90]
003A40C8  test     eax, eax
003A40CA  jne      0x3a40e4  ; -> 003A40E4
003A40CC  mov      eax, dword ptr [rcx + 8]
003A40CF  add      rsp, 0x20
003A40D3  pop      rbx
003A40D4  ret      
003A40D5  or       eax, 0xffffffff
003A40D8  add      rsp, 0x20
003A40DC  pop      rbx
003A40DD  ret      
003A40DE  mov      eax, dword ptr [rip + 0x1cf293c]  ; -> 02096A20
003A40E4  add      rsp, 0x20
003A40E8  pop      rbx
003A40E9  ret      
```

## 003A8C80 (33 B, extent 003A8C80-003A8CA1)

Page context: "/'020926F6'/'02EBA4F0'/'02EC0F88'/'02F97340') | bodies that read '02F97348' (the §12 action context) or '02EBA4F0' (the target array) — the heavyweight opcode arms | | '02EBEF88' family + wrappers | '003A8C80', '003A8CB0', '003A8CE0', '003A8D40' (33–89 B each on '02EBEF88'), '003A8DD0' (423 B — '001EDDA0'/'003A8AE0'/'002F31C0'), '003A8290' ('004FF080'/'004FF0D0', '02EBEF98'); wrappers '003326F0'/'00333430'/'003335A0'/'00333A40' (each '0"

```
003A8C80  mov      rax, qword ptr [rip + 0x2b16301]  ; -> 02EBEF88
003A8C87  mov      rax, qword ptr [rax + 8]
003A8C8B  test     rax, rax
003A8C8E  je       0x3a8ca0  ; -> 003A8CA0
003A8C90  mov      byte ptr [rax + 0x139], 1
003A8C97  mov      rax, qword ptr [rax + 8]
003A8C9B  test     rax, rax
003A8C9E  jne      0x3a8c90  ; -> 003A8C90
003A8CA0  ret      
```

## 003A8CB0 (41 B, extent 003A8CB0-003A8CD9)

Page context: "'02EBA4F0'/'02EC0F88'/'02F97340') | bodies that read '02F97348' (the §12 action context) or '02EBA4F0' (the target array) — the heavyweight opcode arms | | '02EBEF88' family + wrappers | '003A8C80', '003A8CB0', '003A8CE0', '003A8D40' (33–89 B each on '02EBEF88'), '003A8DD0' (423 B — '001EDDA0'/'003A8AE0'/'002F31C0'), '003A8290' ('004FF080'/'004FF0D0', '02EBEF98'); wrappers '003326F0'/'00333430'/'003335A0'/'00333A40' (each '0046EE70' + '"

```
003A8CB0  mov      rax, qword ptr [rip + 0x2b162d1]  ; -> 02EBEF88
003A8CB7  mov      rax, qword ptr [rax + 8]
003A8CBB  test     rax, rax
003A8CBE  je       0x3a8cd8  ; -> 003A8CD8
003A8CC0  movzx    edx, byte ptr [rax + 0x1c]
003A8CC4  cmp      edx, ecx
003A8CC6  je       0x3a8ccf  ; -> 003A8CCF
003A8CC8  mov      byte ptr [rax + 0x139], 1
003A8CCF  mov      rax, qword ptr [rax + 8]
003A8CD3  test     rax, rax
003A8CD6  jne      0x3a8cc0  ; -> 003A8CC0
003A8CD8  ret      
```

## 003A8CE0 (89 B, extent 003A8CE0-003A8D39)

Page context: "02EC0F88'/'02F97340') | bodies that read '02F97348' (the §12 action context) or '02EBA4F0' (the target array) — the heavyweight opcode arms | | '02EBEF88' family + wrappers | '003A8C80', '003A8CB0', '003A8CE0', '003A8D40' (33–89 B each on '02EBEF88'), '003A8DD0' (423 B — '001EDDA0'/'003A8AE0'/'002F31C0'), '003A8290' ('004FF080'/'004FF0D0', '02EBEF98'); wrappers '003326F0'/'00333430'/'003335A0'/'00333A40' (each '0046EE70' + '003697F0' + "

```
003A8CE0  mov      rax, qword ptr [rip + 0x2b162a1]  ; -> 02EBEF88
003A8CE7  mov      rdx, qword ptr [rax + 8]
003A8CEB  test     rdx, rdx
003A8CEE  je       0x3a8d38  ; -> 003A8D38
003A8CF0  movzx    eax, byte ptr [rdx + 0x1c]
003A8CF4  mov      r8, qword ptr [rdx + 8]
003A8CF8  cmp      eax, ecx
003A8CFA  je       0x3a8d30  ; -> 003A8D30
003A8CFC  mov      rax, qword ptr [rdx + 0x108]
003A8D03  test     rax, rax
003A8D06  je       0x3a8d30  ; -> 003A8D30
003A8D08  cmp      byte ptr [rax + 0x44], 0x40
003A8D0C  jne      0x3a8d30  ; -> 003A8D30
003A8D0E  mov      rax, qword ptr [rdx + 0x118]
003A8D15  test     rax, rax
003A8D18  je       0x3a8d30  ; -> 003A8D30
003A8D1A  nop      word ptr [rax + rax]
003A8D20  or       byte ptr [rax + 0x248], 1
003A8D27  mov      rax, qword ptr [rax + 0x30]
003A8D2B  test     rax, rax
003A8D2E  jne      0x3a8d20  ; -> 003A8D20
003A8D30  mov      rdx, r8
003A8D33  test     r8, r8
003A8D36  jne      0x3a8cf0  ; -> 003A8CF0
003A8D38  ret      
```

## 003A8D40 (44 B, extent 003A8D40-003A8D6C)

Page context: "2F97340') | bodies that read '02F97348' (the §12 action context) or '02EBA4F0' (the target array) — the heavyweight opcode arms | | '02EBEF88' family + wrappers | '003A8C80', '003A8CB0', '003A8CE0', '003A8D40' (33–89 B each on '02EBEF88'), '003A8DD0' (423 B — '001EDDA0'/'003A8AE0'/'002F31C0'), '003A8290' ('004FF080'/'004FF0D0', '02EBEF98'); wrappers '003326F0'/'00333430'/'003335A0'/'00333A40' (each '0046EE70' + '003697F0' + one '003A8Cx"

```
003A8D40  mov      rax, qword ptr [rip + 0x2b16241]  ; -> 02EBEF88
003A8D47  mov      rax, qword ptr [rax + 8]
003A8D4B  test     rax, rax
003A8D4E  je       0x3a8d6b  ; -> 003A8D6B
003A8D50  movzx    edx, byte ptr [rax + 0x13a]
003A8D57  cmp      edx, ecx
003A8D59  jne      0x3a8d62  ; -> 003A8D62
003A8D5B  mov      byte ptr [rax + 0x139], 1
003A8D62  mov      rax, qword ptr [rax + 8]
003A8D66  test     rax, rax
003A8D69  jne      0x3a8d50  ; -> 003A8D50
003A8D6B  ret      
```

## 003B9FE0 (51 B, extent 003B9FE0-003BA013)

Page context: "2EBA4F0'; interior 2026-09-17, SWE2-FRONTIER — '02EBA4F0' loaded ×5 beginning ['003B9A2A'](../../_index/ADDRESS-INDEX.md), helper set '0046C8D0'/'003616F0'/'00181DD0' ×2 each — the opcode-5/39 arm), '003B9FE0' ('0024B240'), '003BA020' ('00182B40'/'00375900'/'0017F2A0'/'001E0580', '020926D0'), '003BA1F0' ('01DFE0B4'/'020926F6'/'02EBA4F0'/'02EC0F88'/'02F97340') | bodies that read '02F97348' (the §12 action context) or '02EBA4F0' (the targ"

```
003B9FE0  sub      rsp, 0x28
003B9FE4  mov      rax, qword ptr [rip + 0x2bdd35d]  ; -> 02F97348
003B9FEB  mov      rcx, qword ptr [rax + 0x380]
003B9FF2  test     rcx, rcx
003B9FF5  je       0x3ba00e  ; -> 003BA00E
003B9FF7  call     0x24b240  ; -> 0024B240 fn
003B9FFC  mov      rax, qword ptr [rip + 0x2bdd345]  ; -> 02F97348
003BA003  mov      qword ptr [rax + 0x380], 0
003BA00E  add      rsp, 0x28
003BA012  ret      
```

## 00423190 (72 B, extent 00423190-004231D8)

Page context: "rger step — '0046EE70'/'003697F0' bracket it | | hit/target helpers | '00322850' (the §12 post-hit call — '003588B0' ×2 + '00263E30' ×2), '0042F2A0' ('0020E600' + '004219C0'/'00426E40', '022C6F28'), '00423190'/'004231E0' (72 B twins: '0020E600' + '0051B9E0'), '003BA150' ('002EE050' ×2 + '003A6BA0', '01EFE318'/'022C6F28'), '0046CC20' ('002E9D90'), '003D7C50' ('02EBBA00') | resolve-and-apply steps behind the hit/placement opcodes | | leav"

```
00423190  push     rbx
00423192  sub      rsp, 0x20
00423196  cmp      dword ptr [rcx + 0xc4], -1
0042319D  mov      rbx, rcx
004231A0  je       0x4231d0  ; -> 004231D0
004231A2  mov      ecx, dword ptr [rcx + 0x10]
004231A5  call     0x20e600  ; -> 0020E600 fn
004231AA  mov      edx, dword ptr [rbx + 0xc4]
004231B0  mov      rcx, qword ptr [rax + 0xda8]
004231B7  call     0x51b9e0  ; -> 0051B9E0 fn
004231BC  test     rax, rax
004231BF  je       0x4231d0  ; -> 004231D0
004231C1  mov      eax, dword ptr [rax + 0xc]
004231C4  shr      eax, 6
004231C7  and      eax, 1
004231CA  add      rsp, 0x20
004231CE  pop      rbx
004231CF  ret      
004231D0  xor      eax, eax
004231D2  add      rsp, 0x20
004231D6  pop      rbx
004231D7  ret      
```

## 004231E0 (72 B, extent 004231E0-00423228)

Page context: " '0046EE70'/'003697F0' bracket it | | hit/target helpers | '00322850' (the §12 post-hit call — '003588B0' ×2 + '00263E30' ×2), '0042F2A0' ('0020E600' + '004219C0'/'00426E40', '022C6F28'), '00423190'/'004231E0' (72 B twins: '0020E600' + '0051B9E0'), '003BA150' ('002EE050' ×2 + '003A6BA0', '01EFE318'/'022C6F28'), '0046CC20' ('002E9D90'), '003D7C50' ('02EBBA00') | resolve-and-apply steps behind the hit/placement opcodes | | leaves | '0017F"

```
004231E0  push     rbx
004231E2  sub      rsp, 0x20
004231E6  cmp      dword ptr [rcx + 0xc4], -1
004231ED  mov      rbx, rcx
004231F0  je       0x423220  ; -> 00423220
004231F2  mov      ecx, dword ptr [rcx + 0x10]
004231F5  call     0x20e600  ; -> 0020E600 fn
004231FA  mov      edx, dword ptr [rbx + 0xc4]
00423200  mov      rcx, qword ptr [rax + 0xda8]
00423207  call     0x51b9e0  ; -> 0051B9E0 fn
0042320C  test     rax, rax
0042320F  je       0x423220  ; -> 00423220
00423211  mov      eax, dword ptr [rax + 0xc]
00423214  shr      eax, 7
00423217  and      eax, 1
0042321A  add      rsp, 0x20
0042321E  pop      rbx
0042321F  ret      
00423220  xor      eax, eax
00423222  add      rsp, 0x20
00423226  pop      rbx
00423227  ret      
```

## 0046CC20 (76 B, extent 0046CC20-0046CC6C)

Page context: "263E30' ×2), '0042F2A0' ('0020E600' + '004219C0'/'00426E40', '022C6F28'), '00423190'/'004231E0' (72 B twins: '0020E600' + '0051B9E0'), '003BA150' ('002EE050' ×2 + '003A6BA0', '01EFE318'/'022C6F28'), '0046CC20' ('002E9D90'), '003D7C50' ('02EBBA00') | resolve-and-apply steps behind the hit/placement opcodes | | leaves | '0017F2A0' ('00189120'/'0018CA40'/'0018B8B0' — a command-list emit), '003333B0', '00333620', '00379940' | small bodies t"

```
0046CC20  sub      rsp, 0x28
0046CC24  test     edx, edx
0046CC26  jle      0x46cc67  ; -> 0046CC67
0046CC28  cmp      edx, 3
0046CC2B  jle      0x46cc37  ; -> 0046CC37
0046CC2D  cmp      edx, 5
0046CC30  jg       0x46cc67  ; -> 0046CC67
0046CC32  add      edx, 2
0046CC35  jmp      0x46cc39  ; -> 0046CC39
0046CC37  dec      edx
0046CC39  mov      rcx, qword ptr [rcx + 0x108]
0046CC40  xor      r9d, r9d
0046CC43  mov      r8d, edx
0046CC46  lea      edx, [r9 + 2]
0046CC4A  call     0x2e9d90  ; -> 002E9D90 fn
0046CC4F  test     eax, eax
0046CC51  js       0x46cc67  ; -> 0046CC67
0046CC53  mov      edx, 0x40
0046CC58  mov      ecx, eax
0046CC5A  lea      r8d, [rdx + 0x3f]
0046CC5E  add      rsp, 0x28
0046CC62  jmp      0x3a0e20  ; -> 003A0E20 fn
0046CC67  add      rsp, 0x28
0046CC6B  ret      
```

## 00472950 (20 B, extent 00472950-00472964)

Page context: "00' resolves then '00472810'. Interior anchor '003E1378' (an '0020E600' call).  ## SWE2-EC7-36 update (2026-09-19) - '003E1610'  '003E1610' (629 B) is the sibling sweep - 32 '0020E600' resolves then '00472950'. Interior anchor '003E1638' (an '0020E600' call).  ## SWE2-EC7-39 update (2026-09-19) - '003A8DD0'  '003A8DD0' (423 B) is the '02EBEF88' family's larger step the page names - '001EDDA0'/'003A8AE0'/'002F31C0'. Interior anchor '003A"

```
00472950  movzx    eax, byte ptr [rcx]
00472953  test     al, 1
00472955  jne      0x472963  ; -> 00472963
00472957  or       al, 5
00472959  mov      qword ptr [rcx + 8], 6
00472961  mov      byte ptr [rcx], al
00472963  ret      
```

## 005388F0 (24 B, extent 005388F0-00538908)

Page context: "e multi-arm record interpreter this page cites: 'byte[rcx+1]' selects the arm ('1'/'2'/'3' at '004FF2CB'–'004FF2D5') — '005372D0' ('004FF2DD'), '00538820' ('004FF306'), and the '005375B0'/'003B9FB0'/'005388F0' tails ('004FF340'–'004FF34A') — then a '0x61'-bound image-base switch 'byte[00120000+rax+0x3DF3D8]' → 'jmp rdx' ('004FF380'–'004FF39B'), a second '0x3E0270' table at '004FF463', 'word[rbx+0x20]' compares ('004FF477'/'004FF4B8'/'00"

```
005388F0  push     rbx
005388F2  sub      rsp, 0x20
005388F6  mov      rbx, rcx
005388F9  call     0x4ff2b0  ; -> 004FF2B0 fn
005388FE  lea      rax, [rbx + 0x20]
00538902  add      rsp, 0x20
00538906  pop      rbx
00538907  ret      
```
