# F-interior pack: `03-World-Area-Field/Weather/weather-apply-and-environment-materialization.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/weather-apply-and-environment-materialization.json`.

Functions: 14. Each is cited on the page only at its entry and is still in the F frontier.

## 001AA3B0 (30 B, extent 001AA3B0-001AA3CE)

Page context: " two axis rotations). It stores the         vector as entry 'i' of the per-index table through '001A9B30', which also sets the table's byte '+0x398', the         flag '001A7E40' tests. It then calls '001AA3B0', which selects an entry through '001A7E40' and so publishes it         (Source 2 above).       - **The cutscene path.** The cutscene-JSON loader reads the pair only when the file sets 'enableLightInfo', which         exactly one o"

```
001AA3B0  push     rbx
001AA3B2  sub      rsp, 0x20
001AA3B6  mov      rbx, rcx
001AA3B9  call     0x265920  ; -> 00265920 fn
001AA3BE  mov      rcx, rbx
001AA3C1  lea      edx, [rax - 1]
001AA3C4  add      rsp, 0x20
001AA3C8  pop      rbx
001AA3C9  jmp      0x1a7e40  ; -> 001A7E40 fn
```

## 001DC000 (61 B, extent 001DC000-001DC03D)

Page context: "ecord banks zeroed and primed at boot | | cell writers | '002556F0' ('02092810'/'02096280'/'02096520'/'02096730' quad), '00259E90' ('02097304'/'02097B80'/'B4'/'02097C50' + '003CBFF0' ×3/'00259B30'), '001DC000' ('00210B30'), '00210F60' ('007A5B00'/'007A58D0'/'001243B0'), '002DF2C0' ('02AED560' + '003603C0'/'003CBFA0'/'001DC000') | named-cell initialisation across '02092xxx'/'02097xxx' | | listener block | '00360C70' (190 B — deque family"

```
001DC000  mov      qword ptr [rsp + 8], rbx
001DC005  push     rdi
001DC006  sub      rsp, 0x30
001DC00A  movaps   xmmword ptr [rsp + 0x20], xmm6
001DC00F  mov      rbx, rdx
001DC012  movaps   xmm6, xmm2
001DC015  mov      rdi, rcx
001DC018  call     0x210b30  ; -> 00210B30 fn
001DC01D  mov      rcx, rax
001DC020  movaps   xmm3, xmm6
001DC023  mov      r8, rbx
001DC026  mov      rdx, rdi
001DC029  mov      rbx, qword ptr [rsp + 0x40]
001DC02E  movaps   xmm6, xmmword ptr [rsp + 0x20]
001DC033  add      rsp, 0x30
001DC037  pop      rdi
001DC038  jmp      0x210f60  ; -> 00210F60 fn
```

## 00210ED0 (135 B, extent 00210ED0-00210F57)

Page context: "99090' call '001EDEC0' — the interface layer consults this page's helper, shared fan-in. - **Audio - CLIENT (161 edges).** '001243B0' is also called by bodies filed to audio: '00121030', '00121E20', '00210ED0' - shared machinery across the layer boundary, no shared ownership. - **CombatAction - CLIENT (6 edges).** '003148F0', '003590D0' are also called by bodies filed to combat action: '002F8060', '002FA740', '00317E60' - shared machine"

```
00210ED0  push     rbx
00210ED2  sub      rsp, 0x50
00210ED6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00210EDF  movaps   xmmword ptr [rsp + 0x40], xmm6
00210EE4  movaps   xmmword ptr [rsp + 0x30], xmm7
00210EE9  mov      ebx, r8d
00210EEC  movaps   xmm6, xmm1
00210EEF  xorps    xmm7, xmm7
00210EF2  comiss   xmm6, xmm7
00210EF5  jb       0x210f0b  ; -> 00210F0B
00210EF7  movss    xmm0, dword ptr [rip + 0x1adaca9]  ; -> 01CEBBA8 [f32 1]
00210EFF  comiss   xmm0, xmm6
00210F02  jb       0x210f0b  ; -> 00210F0B
00210F04  mov      ecx, 1
00210F09  jmp      0x210f0d  ; -> 00210F0D
00210F0B  xor      ecx, ecx
00210F0D  call     0x16d6a0  ; -> 0016D6A0 fn
00210F12  lea      rcx, [rsp + 0x78]
00210F17  call     0x7a4380  ; -> 007A4380 fn
00210F1C  nop      
00210F1D  mov      edx, ebx
00210F1F  lea      rcx, [rsp + 0x78]
00210F24  call     0x7a4c70  ; -> 007A4C70 fn
00210F29  xor      r9d, r9d
00210F2C  movaps   xmm2, xmm7
00210F2F  movaps   xmm1, xmm6
00210F32  lea      rcx, [rsp + 0x78]
00210F37  call     0x7a45c0  ; -> 007A45C0 fn
00210F3C  nop      
00210F3D  lea      rcx, [rsp + 0x78]
00210F42  call     0x1243b0  ; -> 001243B0 fn
00210F47  movaps   xmm6, xmmword ptr [rsp + 0x40]
00210F4C  movaps   xmm7, xmmword ptr [rsp + 0x30]
00210F51  add      rsp, 0x50
00210F55  pop      rbx
00210F56  ret      
```

## 00299090 (1040 B, extent 00299090-002994A0)

Page context: "/'002DF9A0'/'0032EAE0'/'00379D20' of that layer — the weather frame consumes resource helpers, not a shared responsibility. **UI — CLIENT (SWE2-EC7-156, 25 edges).** '00252030'/'00276D30'/'0027C870'/'00299090' call '001EDEC0' — the interface layer consults this page's helper, shared fan-in. - **Audio - CLIENT (161 edges).** '001243B0' is also called by bodies filed to audio: '00121030', '00121E20', '00210ED0' - shared machinery across t"

```
00299090  mov      qword ptr [rsp + 0x10], rbx
00299095  mov      qword ptr [rsp + 0x18], rbp
0029909A  push     rsi
0029909B  push     rdi
0029909C  push     r14
0029909E  sub      rsp, 0x20
002990A2  mov      eax, dword ptr [rdx]
002990A4  mov      rsi, rdx
002990A7  dec      eax
002990A9  mov      rdi, rcx
002990AC  cmp      eax, 0x1c
002990AF  ja       0x299485  ; -> 00299485
002990B5  lea      rcx, [rip - 0x1790bc]  ; -> 00120000 (image base)
002990BC  cdqe     
002990BE  movzx    eax, byte ptr [rcx + rax + 0x1794bc]
002990C6  mov      r8d, dword ptr [rcx + rax*4 + 0x1794a0]  ; image base + 0x1794a0 = 002994A0
002990CE  add      r8, rcx
002990D1  jmp      r8
002990D4  mov      rax, qword ptr [rip + 0x1e01b55]  ; -> 0209AC30
002990DB  lea      rcx, [rdi + 0x50]
002990DF  mov      r9, rdi
002990E2  mov      r8d, 0x32
002990E8  mov      rdx, qword ptr [rax + 8]
002990EC  call     0x2432b0  ; -> 002432B0 fn
002990F1  mov      ecx, dword ptr [rsi + 8]
002990F4  mov      rbx, rax
002990F7  call     0x28f830  ; -> 0028F830 fn
002990FC  mov      qword ptr [rdi + 0xc0], rax
00299103  movzx    ecx, byte ptr [rsi + 8]
00299107  mov      byte ptr [rax], cl
00299109  mov      ecx, 5
0029910E  call     0x2735e0  ; -> 002735E0 fn
00299113  mov      rdx, rax
00299116  mov      rcx, rdi
00299119  call     0x247570  ; -> 00247570 fn
0029911E  movzx    edx, word ptr [rbx + 8]
00299122  mov      ecx, dword ptr [rsi + 0x10]
00299125  movzx    r8d, word ptr [rbx + 0xa]
0029912A  movzx    eax, word ptr [rbx + 4]
0029912E  mov      word ptr [rdi + 0x9c], dx
00299135  mov      edx, 3
0029913A  mov      word ptr [rdi + 0x9a], cx
00299141  mov      rcx, rdi
00299144  mov      word ptr [rdi + 0x98], ax
0029914B  mov      word ptr [rdi + 0x9e], r8w
00299153  call     0x247930  ; -> 00247930 fn
00299158  mov      rax, qword ptr [rdi + 0xc0]
0029915F  mov      ebp, 0xffff
00299164  mov      word ptr [rax + 4], bp
00299168  mov      esi, dword ptr [rsi + 8]
0029916B  mov      rbx, qword ptr [rdi + 0xc0]
00299172  call     0x35d320  ; -> 0035D320 fn
00299177  movzx    ecx, byte ptr [rbx]
0029917A  lea      r8, [rcx + rcx*2]
0029917E  shl      r8, 6
00299182  add      r8, rax
00299185  cmp      byte ptr [rbx + 0x13], 0
00299189  jne      0x29918f  ; -> 0029918F
0029918B  mov      byte ptr [rbx + 0x13], 0xff
0029918F  mov      rcx, qword ptr [rdi + 0xc0]
00299196  movsx    eax, byte ptr [rcx + 1]
0029919A  cmp      word ptr [r8 + 0x80], ax
002991A2  je       0x2991d6  ; -> 002991D6
002991A4  xor      eax, eax
002991A6  mov      qword ptr [rcx], rax
002991A9  mov      qword ptr [rcx + 8], rax
002991AD  mov      qword ptr [rcx + 0x10], rax
002991B1  mov      qword ptr [rcx + 0x18], rax
002991B5  mov      byte ptr [rcx + 1], 0xff
002991B9  mov      byte ptr [rcx], sil
002991BC  mov      byte ptr [rcx + 0x13], 0xff
002991C0  mov      word ptr [rcx + 4], bp
002991C4  mov      rcx, qword ptr [rdi + 0xc0]
002991CB  movzx    eax, byte ptr [r8 + 0x80]
002991D3  mov      byte ptr [rcx + 1], al
002991D6  mov      rsi, qword ptr [rdi + 0xc0]
002991DD  call     0x35d320  ; -> 0035D320 fn
002991E2  movzx    ecx, byte ptr [rsi]
002991E5  xor      eax, eax
002991E7  mov      word ptr [rsi + 0x14], ax
002991EB  mov      ebx, 0x4000
002991F0  mov      rax, qword ptr [rdi + 0xc0]
002991F7  mov      dword ptr [rsp + 0x40], 0x80808080
002991FF  lea      rdx, [rcx + rcx*2]
00299203  shl      rdx, 6
00299207  movzx    ecx, byte ptr [rax + 0x14]
0029920B  mov      rax, qword ptr [rdi + 0x60]
0029920F  mov      byte ptr [rsp + 0x43], cl
00299213  mov      rcx, qword ptr [rax + 0x18]
00299217  mov      eax, dword ptr [rsp + 0x40]
0029921B  mov      dword ptr [rcx + 0x34], eax
0029921E  mov      dword ptr [rcx + 0x30], eax
00299221  mov      dword ptr [rcx + 0x2c], eax
00299224  mov      dword ptr [rcx + 0x28], eax
00299227  mov      rsi, qword ptr [rdi + 0xc0]
0029922E  movzx    r14d, byte ptr [rsi]
00299232  call     0x35d320  ; -> 0035D320 fn
00299237  lea      r8, [r14 + r14*2]
0029923B  shl      r8, 6
0029923F  add      r8, rax
00299242  mov      eax, dword ptr [r8 + 0x20]
00299246  bt       eax, 9
0029924A  jb       0x29925a  ; -> 0029925A
0029924C  cmp      word ptr [r8 + 0x7c], bx
00299251  jb       0x29925a  ; -> 0029925A
00299253  cmp      word ptr [r8 + 0x7e], bx
00299258  jae      0x29925e  ; -> 0029925E
0029925A  test     al, 0x40
0029925C  je       0x29929a  ; -> 0029929A
0029925E  xor      ecx, ecx
00299260  movzx    eax, r14b
00299264  mov      qword ptr [rsi], rcx
00299267  mov      qword ptr [rsi + 8], rcx
0029926B  mov      qword ptr [rsi + 0x10], rcx
0029926F  mov      qword ptr [rsi + 0x18], rcx
00299273  mov      byte ptr [rsi], al
00299275  mov      byte ptr [rsi + 1], 0xff
00299279  mov      byte ptr [rsi + 0x13], 0xff
0029927D  mov      word ptr [rsi + 4], bp
00299281  movzx    eax, byte ptr [r8 + 0x80]
00299289  mov      rcx, qword ptr [rdi + 0xc0]
00299290  mov      byte ptr [rcx + 1], al
00299293  xor      eax, eax
00299295  jmp      0x29948d  ; -> 0029948D
0029929A  mov      rax, qword ptr [rdi + 0x60]
0029929E  movsx    edx, byte ptr [rsi + 0x13]
002992A2  mov      rcx, qword ptr [rax]
002992A5  call     0x225580  ; -> 00225580 fn
002992AA  xor      eax, eax
002992AC  jmp      0x29948d  ; -> 0029948D
002992B1  call     0x35d320  ; -> 0035D320 fn
002992B6  mov      rcx, qword ptr [rdi + 0xc0]
002992BD  mov      ebp, 0xffff
002992C2  movzx    edx, byte ptr [rcx]
002992C5  lea      rdx, [rdx + rdx*2]
002992C9  shl      rdx, 6
002992CD  add      rdx, rax
002992D0  mov      rax, qword ptr [rdi + 0x60]
002992D4  mov      rcx, qword ptr [rax]
002992D7  and      dword ptr [rcx + 0x20], 0xfbffffff
002992DE  mov      rcx, qword ptr [rdi + 0xc0]
002992E5  movsx    eax, byte ptr [rcx + 1]
002992E9  cmp      ax, word ptr [rdx + 0x80]
002992F0  jne      0x2992f8  ; -> 002992F8
002992F2  test     byte ptr [rcx + 2], 2
002992F6  je       0x29932c  ; -> 0029932C
002992F8  movzx    eax, byte ptr [rcx]
002992FB  xor      r8d, r8d
002992FE  mov      qword ptr [rcx], r8
00299301  mov      qword ptr [rcx + 8], r8
00299305  mov      qword ptr [rcx + 0x10], r8
00299309  mov      qword ptr [rcx + 0x18], r8
0029930D  mov      byte ptr [rcx + 1], 0xff
00299311  mov      byte ptr [rcx], al
00299313  mov      byte ptr [rcx + 0x13], 0xff
00299317  mov      word ptr [rcx + 4], bp
0029931B  mov      rcx, qword ptr [rdi + 0xc0]
00299322  movzx    eax, byte ptr [rdx + 0x80]
00299329  mov      byte ptr [rcx + 1], al
0029932C  mov      rax, qword ptr [rdi + 0xc0]
00299333  or       word ptr [rax + 2], 1
00299338  mov      rax, qword ptr [rdi + 0xc0]
0029933F  mov      word ptr [rax + 4], bp
00299343  xor      eax, eax
00299345  jmp      0x29948d  ; -> 0029948D
0029934A  mov      rax, qword ptr [rdi + 0xc0]
00299351  or       word ptr [rax + 2], 2
00299356  xor      eax, eax
00299358  jmp      0x29948d  ; -> 0029948D
0029935D  mov      rax, qword ptr [rdi + 0xc0]
00299364  mov      ecx, 0xfffe
00299369  and      word ptr [rax + 2], cx
0029936D  xor      eax, eax
0029936F  jmp      0x29948d  ; -> 0029948D
00299374  mov      ecx, dword ptr [rdi + 0xb4]
0029937A  call     0x1edec0  ; -> 001EDEC0 fn
0029937F  test     eax, eax
00299381  je       0x299481  ; -> 00299481
00299387  cmp      word ptr [rdi + 0xc8], 0
0029938F  jne      0x299481  ; -> 00299481
00299395  mov      rbx, qword ptr [rdi + 0xc0]
0029939C  call     0x35d320  ; -> 0035D320 fn
002993A1  movzx    ecx, byte ptr [rbx]
002993A4  lea      rsi, [rcx + rcx*2]
002993A8  shl      rsi, 6
002993AC  add      rsi, rax
002993AF  movzx    eax, word ptr [rbx + 2]
002993B3  test     al, 1
002993B5  jne      0x299422  ; -> 00299422
002993B7  mov      eax, dword ptr [rsi + 0x20]
002993BA  mov      ebx, 0x4000
002993BF  bt       eax, 9
002993C3  jb       0x2993d5  ; -> 002993D5
002993C5  cmp      word ptr [rsi + 0x7c], bx
002993C9  jb       0x2993d5  ; -> 002993D5
002993CB  cmp      word ptr [rsi + 0x7e], bx
002993CF  jae      0x299481  ; -> 00299481
002993D5  test     al, 0x40
002993D7  jne      0x299481  ; -> 00299481
002993DD  xor      eax, eax
002993DF  mov      rcx, rdi
002993E2  mov      word ptr [rdi + 0xca], ax
002993E9  call     0x246ac0  ; -> 00246AC0 fn
002993EE  cmp      word ptr [rsi + 0x7c], bx
002993F2  jae      0x2993ff  ; -> 002993FF
002993F4  mov      rax, qword ptr [rdi + 0xc0]
002993FB  mov      byte ptr [rax + 6], 0x80
002993FF  lea      rdx, [rsi + 0x20]
00299403  mov      rcx, rdi
00299406  call     0x2986e0  ; -> 002986E0 fn
0029940B  mov      rcx, qword ptr [rdi + 0xc0]
00299412  mov      rdx, rdi
00299415  add      rcx, 0x18
00299419  call     0x297290  ; -> 00297290 fn
0029941E  xor      eax, eax
00299420  jmp      0x29948d  ; -> 0029948D
00299422  test     al, 2
00299424  jne      0x299481  ; -> 00299481
00299426  mov      eax, dword ptr [rsi + 0x20]
00299429  bt       eax, 9
0029942D  jb       0x299440  ; -> 00299440
0029942F  mov      ebx, 0x4000
00299434  cmp      word ptr [rsi + 0x7c], bx
00299438  jb       0x299440  ; -> 00299440
0029943A  cmp      word ptr [rsi + 0x7e], bx
0029943E  jae      0x29944f  ; -> 0029944F
00299440  test     al, 0x40
00299442  jne      0x29944f  ; -> 0029944F
00299444  xor      eax, eax
00299446  mov      word ptr [rdi + 0xca], ax
0029944D  jmp      0x2993ff  ; -> 002993FF
0029944F  inc      word ptr [rdi + 0xca]
00299456  cmp      word ptr [rdi + 0xca], 4
0029945E  jl       0x2993ff  ; -> 002993FF
00299460  xor      eax, eax
00299462  mov      rcx, rdi
00299465  mov      word ptr [rdi + 0xca], ax
0029946C  call     0x244dd0  ; -> 00244DD0 fn
00299471  xor      eax, eax
00299473  jmp      0x29948d  ; -> 0029948D
00299475  mov      eax, 1
0029947A  mov      word ptr [rdi + 0xc8], ax
00299481  xor      eax, eax
00299483  jmp      0x29948d  ; -> 0029948D
00299485  mov      rcx, rdi
00299488  call     0x5c5230  ; -> 005C5230 fn
0029948D  mov      rbx, qword ptr [rsp + 0x48]
00299492  mov      rbp, qword ptr [rsp + 0x50]
00299497  add      rsp, 0x20
0029949B  pop      r14
0029949D  pop      rdi
0029949E  pop      rsi
0029949F  ret      
```

## 002EFA20 (80 B, extent 002EFA20-002EFA70)

Page context: " (190 B — deque family + '022CB9F0'), '00362F70' (516 B — '002DEBA0'/'002DF2C0', '022CBA8C'/'022CBB00'), '0036C5A0' ('022D7FD0') | the '022CB9xx'/'022CBAxx' audio-listener block priming | | leaves | '002EFA20', '002F1A00', '00314940', '0035B790', '0037CB00', '0037CB10', '003B6ED0' ('02EBCBE0'), '003BA310', '003E82B0', '003E90E0' | ten 7–199 B bodies, mostly single-cell or tail thunks |  The shape fits §2's "broad bootstrap": no single d"

```
002EFA20  xor      eax, eax
002EFA22  mov      byte ptr [rip + 0x1fce334], 3  ; -> 022BDD5D
002EFA29  mov      dword ptr [rip + 0x1fce331], eax  ; -> 022BDD60
002EFA2F  mov      dword ptr [rip + 0x1fce35b], eax  ; -> 022BDD90
002EFA35  mov      dword ptr [rip + 0x1fce385], eax  ; -> 022BDDC0
002EFA3B  mov      dword ptr [rip + 0x1fce3af], eax  ; -> 022BDDF0
002EFA41  mov      dword ptr [rip + 0x1fce3d9], eax  ; -> 022BDE20
002EFA47  mov      dword ptr [rip + 0x1fce403], eax  ; -> 022BDE50
002EFA4D  mov      dword ptr [rip + 0x1fce42d], eax  ; -> 022BDE80
002EFA53  mov      byte ptr [rip + 0x1fce303], al  ; -> 022BDD5C
002EFA59  mov      dword ptr [rip + 0x1fce451], eax  ; -> 022BDEB0
002EFA5F  mov      dword ptr [rip + 0x1fce453], eax  ; -> 022BDEB8
002EFA65  mov      dword ptr [rip + 0x1fce445], 6  ; -> 022BDEB4
002EFA6F  ret      
```

## 002F1A00 (23 B, extent 002F1A00-002F1A17)

Page context: "que family + '022CB9F0'), '00362F70' (516 B — '002DEBA0'/'002DF2C0', '022CBA8C'/'022CBB00'), '0036C5A0' ('022D7FD0') | the '022CB9xx'/'022CBAxx' audio-listener block priming | | leaves | '002EFA20', '002F1A00', '00314940', '0035B790', '0037CB00', '0037CB10', '003B6ED0' ('02EBCBE0'), '003BA310', '003E82B0', '003E90E0' | ten 7–199 B bodies, mostly single-cell or tail thunks |  The shape fits §2's "broad bootstrap": no single dominant body"

```
002F1A00  xor      eax, eax
002F1A02  mov      dword ptr [rip + 0x1fccdb8], eax  ; -> 022BE7C0
002F1A08  mov      qword ptr [rip + 0x1fccdb9], rax  ; -> 022BE7C8
002F1A0F  mov      qword ptr [rip + 0x1fccdba], rax  ; -> 022BE7D0
002F1A16  ret      
```

## 0036C5A0 (41 B, extent 0036C5A0-0036C5C9)

Page context: "ll signature-swept 2026-09-15 ('bshape.py'):  | cluster | members | role | |---|---|---| | request/mailbox arms | '002E1450' ('00404DC0' + '0215F200'/'0215F540'), '002EA320' (507 B — '0041D6C0' ×5 + '0036C5A0' ×2 over '0215FD46'–'02164080' cells), '002EA530' (deque ops '0032E400'/'0036C1D0'/'0036A190'/'0036C140'/'0032E620'/'0036C660' + '00D0F8B0'/'021641A0') | the boot-time request-ring fills — '0215Fxxx'/'02161Dxx' are the router cells"

```
0036C5A0  cmp      ecx, 0xe
0036C5A3  ja       0x36c5bf  ; -> 0036C5BF
0036C5A5  movsxd   rax, ecx
0036C5A8  imul     rcx, rax, 0xa8
0036C5AF  lea      rax, [rip + 0x1f6ba1a]  ; -> 022D7FD0
0036C5B6  mov      qword ptr [rcx + rax + 0xa0], rdx
0036C5BE  ret      
0036C5BF  xor      eax, eax
0036C5C1  mov      qword ptr [rax + 0xa0], rdx
0036C5C8  ret      
```

## 003777A0 (15 B, extent 003777A0-003777AF)

Page context: "ches '002E3D40' in zero mode, which resolves field context ('003148F0'), canonical WorldAreaField state ('00264F10'), the committed slot ('00265920'), extracts the three MWeather fields ('00377850', '003777A0', '003777B0'), and tail-enters '0040AAD0' - the Presentation backend mode/orientation initializer.  ### Entry census  Only **four** direct control-flow entries exist in the whole executable:  | From | Context | |---|---| | '0025ACA"

```
003777A0  mov      r9d, 4
003777A6  lea      r8d, [r9 - 1]
003777AA  jmp      0x3777c0  ; -> 003777C0 fn
```

## 003777B0 (15 B, extent 003777B0-003777BF)

Page context: "40' in zero mode, which resolves field context ('003148F0'), canonical WorldAreaField state ('00264F10'), the committed slot ('00265920'), extracts the three MWeather fields ('00377850', '003777A0', '003777B0'), and tail-enters '0040AAD0' - the Presentation backend mode/orientation initializer.  ### Entry census  Only **four** direct control-flow entries exist in the whole executable:  | From | Context | |---|---| | '0025ACA0' (tail jum"

```
003777B0  mov      r9d, 2
003777B6  lea      r8d, [r9 + 5]
003777BA  jmp      0x3777c0  ; -> 003777C0 fn
```

## 003DA2C0 (16 B, extent 003DA2C0-003DA2D0)

Page context: "date (2026-09-19) - '00259B30'  '00259B30' (699 B) is a weather apply body - '02098DE9'/'02098DEA'/'02098DEB'/'02098378' flags, '00861EC0'/'00380D30'/'00380B80' quadruples plus '00861F0E'/'00861F08'/'003DA2C0'. Interior anchor '00259B69' (an '00861EC0' call).  ## SWE2-EC7-40 update (2026-09-19) - '002E1450'  '002E1450' (374 B) is the request/mailbox arm the page names - the '0215F1A3'..'0215F1D0' requester bytes, a single '00404DC0' tai"

```
003DA2C0  xorps    xmm3, xmm3
003DA2C3  xorps    xmm2, xmm2
003DA2C6  xor      edx, edx
003DA2C8  xorps    xmm0, xmm0
003DA2CB  jmp      0x2564d0  ; -> 002564D0 fn
```

## 003DD7E0 (97 B, extent 003DD7E0-003DD841)

Page context: "the router cells the field frame drains | | '02B5xxxx' list accessors | '003DAE30' ('02B4E4C0' + '02B57CE0'), '003DCBC0' (300 B — deque family + '02B57F70'/'02B580BA'/'02B5817A' + '00D11790' table), '003DD7E0' ('02B581AD'), '003DDD10' ('02B58A80'), '003DE710' ('02B58C72'/'02B59372'), '003DF030' ('02B59360'), '003E7DF0' ('02B5C780'–'02B5D040', twelve cells), '003EB750' ('00265F90' ×3 over '02B5E160'–'02B5EBB0'), '003EBAB0', '003EBE40', '"

```
003DD7E0  xor      r8d, r8d
003DD7E3  lea      rax, [rip + 0x277a9c3]  ; -> 02B581AD
003DD7EA  mov      edx, r8d
003DD7ED  mov      qword ptr [rip + 0x277b26c], r8  ; -> 02B58A60
003DD7F4  mov      qword ptr [rip + 0x277b26d], r8  ; -> 02B58A68
003DD7FB  mov      dword ptr [rip + 0x277b26e], r8d  ; -> 02B58A70
003DD802  nop      dword ptr [rax]
003DD806  nop      word ptr [rax + rax]
003DD810  mov      ecx, r8d
003DD813  nop      dword ptr [rax]
003DD817  nop      word ptr [rax + rax]
003DD820  mov      word ptr [rax + 1], cx
003DD824  inc      ecx
003DD826  mov      qword ptr [rax - 0xd], r8
003DD82A  mov      byte ptr [rax], r8b
003DD82D  mov      byte ptr [rax - 1], dl
003DD830  add      rax, 0x1c
003DD834  cmp      ecx, 0x10
003DD837  jl       0x3dd820  ; -> 003DD820
003DD839  inc      edx
003DD83B  cmp      edx, 5
003DD83E  jl       0x3dd810  ; -> 003DD810
003DD840  ret      
```

## 003DF030 (98 B, extent 003DF030-003DF092)

Page context: "2B4E4C0' + '02B57CE0'), '003DCBC0' (300 B — deque family + '02B57F70'/'02B580BA'/'02B5817A' + '00D11790' table), '003DD7E0' ('02B581AD'), '003DDD10' ('02B58A80'), '003DE710' ('02B58C72'/'02B59372'), '003DF030' ('02B59360'), '003E7DF0' ('02B5C780'–'02B5D040', twelve cells), '003EB750' ('00265F90' ×3 over '02B5E160'–'02B5EBB0'), '003EBAB0', '003EBE40', '003EC620' | the initialiser's world-state lists — spawn/area record banks zeroed and p"

```
003DF030  xor      r10d, r10d
003DF033  lea      r11, [rip + 0x277a326]  ; -> 02B59360
003DF03A  mov      r8d, r10d
003DF03D  mov      r9d, r10d
003DF040  mov      ecx, r10d
003DF043  mov      rdx, r10
003DF046  cmp      ecx, 7
003DF049  ja       0x3df058  ; -> 003DF058
003DF04B  lea      rax, [r9 + rdx]
003DF04F  imul     rax, rax, 0x38
003DF053  add      rax, r11
003DF056  jmp      0x3df05b  ; -> 003DF05B
003DF058  mov      rax, r10
003DF05B  mov      byte ptr [rax + 0x12], cl
003DF05E  inc      rdx
003DF061  inc      ecx
003DF063  mov      qword ptr [rax + 8], r10
003DF067  mov      qword ptr [rax + 0x18], r10
003DF06B  mov      qword ptr [rax + 0x20], r10
003DF06F  mov      dword ptr [rax], r10d
003DF072  mov      byte ptr [rax + 0x10], r10b
003DF076  mov      byte ptr [rax + 0x11], r8b
003DF07A  mov      word ptr [rax + 0x28], r10w
003DF07F  cmp      ecx, 8
003DF082  jl       0x3df046  ; -> 003DF046
003DF084  inc      r8d
003DF087  add      r9, 8
003DF08B  cmp      r8d, 5
003DF08F  jl       0x3df040  ; -> 003DF040
003DF091  ret      
```

## 003EBE40 (45 B, extent 003EBE40-003EBE6D)

Page context: "DDD10' ('02B58A80'), '003DE710' ('02B58C72'/'02B59372'), '003DF030' ('02B59360'), '003E7DF0' ('02B5C780'–'02B5D040', twelve cells), '003EB750' ('00265F90' ×3 over '02B5E160'–'02B5EBB0'), '003EBAB0', '003EBE40', '003EC620' | the initialiser's world-state lists — spawn/area record banks zeroed and primed at boot | | cell writers | '002556F0' ('02092810'/'02096280'/'02096520'/'02096730' quad), '00259E90' ('02097304'/'02097B80'/'B4'/'02097C"

```
003EBE40  xor      eax, eax
003EBE42  mov      qword ptr [rip + 0x2772e1f], rax  ; -> 02B5EC68
003EBE49  mov      qword ptr [rip + 0x2772e10], rax  ; -> 02B5EC60
003EBE50  mov      qword ptr [rip + 0x2772e19], rax  ; -> 02B5EC70
003EBE57  mov      qword ptr [rip + 0x2772e1a], rax  ; -> 02B5EC78
003EBE5E  mov      qword ptr [rip + 0x2772e1b], rax  ; -> 02B5EC80
003EBE65  mov      qword ptr [rip + 0x2772e1c], rax  ; -> 02B5EC88
003EBE6C  ret      
```

## 0050CDE0 (91 B, extent 0050CDE0-0050CE3B)

Page context: "ry across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT and SERVICE (36 edges).** '00264F10', '00265920' are also called by bodies filed to script VM / native bridge: '0050CDE0', '00356250', '0050D360'; '00266D10' reaches bodies filed to script VM / native bridge: '003DC2D0' - shared machinery across the layer boundary, no shared ownership. - **Spawn_Encounter_Lifecycle - CLIENT (1 edge).** '003148F0' is "

```
0050CDE0  mov      qword ptr [rsp + 8], rbx
0050CDE5  push     rdi
0050CDE6  sub      rsp, 0x20
0050CDEA  mov      rcx, r9
0050CDED  mov      rbx, r9
0050CDF0  call     0x267e10  ; -> 00267E10 fn
0050CDF5  mov      rcx, rbx
0050CDF8  mov      edi, eax
0050CDFA  call     0x267e10  ; -> 00267E10 fn
0050CDFF  mov      ecx, edi
0050CE01  mov      ebx, eax
0050CE03  call     0x264f10  ; -> 00264F10 fn
0050CE08  mov      edx, eax
0050CE0A  mov      ecx, ebx
0050CE0C  call     0x16d6a0  ; -> 0016D6A0 fn
0050CE11  mov      ecx, edi
0050CE13  call     0x264f40  ; -> 00264F40 fn
0050CE18  mov      edx, eax
0050CE1A  mov      ecx, ebx
0050CE1C  call     0x16d6a0  ; -> 0016D6A0 fn
0050CE21  mov      ecx, edi
0050CE23  call     0x264f90  ; -> 00264F90 fn
0050CE28  mov      edx, eax
0050CE2A  mov      ecx, ebx
0050CE2C  mov      rbx, qword ptr [rsp + 0x30]
0050CE31  add      rsp, 0x20
0050CE35  pop      rdi
0050CE36  jmp      0x16d6a0  ; -> 0016D6A0 fn
```
