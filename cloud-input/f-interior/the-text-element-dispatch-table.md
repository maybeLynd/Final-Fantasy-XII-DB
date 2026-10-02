# F-interior pack: `99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md`

Generated 2026-10-02 10:27 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-text-element-dispatch-table.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

## 002477A0 (108 B, extent 002477A0-0024780C)

Page context: " block can be reached through:  | displacement | what it reaches | writes | who | |---|---|---|---| | '+0xAC' | the block through a pointer to itself | 10 | 6 in the widget constructors '002465F0' / '002477A0' / '00247810', writing '6' or '0xF9' **to the widget base**; 2 in '002B0280', an 'inc'/clear counter on an object whose other fields are '+0x98'..'+0xC0' (its *context* pointer is a separate register); 2 in '00784E80' / '00786DD0',"

```
002477A0  mov      r8, rcx
002477A3  test     rcx, rcx
002477A6  je       0x24780b  ; -> 0024780B
002477A8  and      dword ptr [rcx + 0x44], 0xfff8ffff
002477AF  movsx    eax, dx
002477B2  and      eax, 7
002477B5  shl      eax, 0x10
002477B8  or       dword ptr [rcx + 0x44], eax
002477BB  mov      edx, dword ptr [rcx + 0x44]
002477BE  shl      edx, 0xd
002477C1  sar      edx, 0x1d
002477C4  test     dl, 4
002477C7  je       0x2477e2  ; -> 002477E2
002477C9  test     dl, 2
002477CC  je       0x2477d5  ; -> 002477D5
002477CE  mov      byte ptr [rcx + 0xad], 0xf9
002477D5  test     dl, 1
002477D8  je       0x24780b  ; -> 0024780B
002477DA  mov      byte ptr [rcx + 0xac], 0xf9
002477E1  ret      
002477E2  mov      ecx, 6
002477E7  test     dl, 2
002477EA  mov      eax, ecx
002477EC  mov      r9d, 0xfffffff9
002477F2  cmovne   eax, r9d
002477F6  test     dl, 1
002477F9  mov      byte ptr [r8 + 0xad], al
00247800  cmovne   ecx, r9d
00247804  mov      byte ptr [r8 + 0xac], cl
0024780B  ret      
```

## 00299090 (1040 B, extent 00299090-002994A0)

Page context: "yOrAuthoredThresholdGate' ('0032A8A0') calls 'PersistentFlag_QueryAuthoredThresholdSchedule' ('00377970').  **UI — MECHANICAL, 87 edges.** '001EDEC0' is called by '00252030', '00276D30', '0027C870', '00299090' and 9 more; '00254A10' is called by '00273E30', '00295D90', '00298250', '002A4430' and 8 more; '002B3400' is called by '00243860', '0027AD70', '002A86A0', '003EE420' and 4 more; '002475D0' is called by '00296960', '00298250', '002"

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

## 0029B870 (720 B, extent 0029B870-0029BB40)

Page context: "; '002A8C50' calls '002ABF70', '002AC5F0', '002B2150'; '002AC2F0' is called by '002AE610', '002AF340', '002B2150'; '0017F8C0' is called by '002AF340', '002B2150'; '001E0A10' is called by '00284EC0', '0029B870'; '002A6190' calls '002A4430', '002A4830'; '002A9F00' is called by '002AC5F0', '002AE610'; '002AAE40' calls '002AC5F0', '002B2150'; '002AC5F0' calls '002AE610', '002B2150'; '002AC5F0' is called by '002AF340', '002B2150'; '002AF960'"

```
0029B870  mov      qword ptr [rsp + 0x18], rbx
0029B875  mov      qword ptr [rsp + 0x20], rsi
0029B87A  push     rdi
0029B87B  sub      rsp, 0x20
0029B87F  movzx    edi, word ptr [rip + 0x2cfbae4]  ; -> 02F9736A
0029B886  mov      rbx, rcx
0029B889  test     word ptr [rip + 0x1b70a14], di  ; -> 01E0C2A4 [u16 0x4000]
0029B890  movzx    esi, word ptr [rip + 0x2cfbad5]  ; -> 02F9736C
0029B897  je       0x29b8e7  ; -> 0029B8E7
0029B899  mov      rax, qword ptr [rcx + 0xb20]
0029B8A0  movsx    r8d, byte ptr [rcx + 0xb48]
0029B8A8  test     rax, rax
0029B8AB  je       0x29b8d2  ; -> 0029B8D2
0029B8AD  mov      rcx, qword ptr [rcx + 0xb30]
0029B8B4  mov      r9d, r8d
0029B8B7  mov      edx, 3
0029B8BC  call     rax
0029B8BE  test     eax, eax
0029B8C0  jne      0x29b8d2  ; -> 0029B8D2
0029B8C2  mov      rbx, qword ptr [rsp + 0x40]
0029B8C7  mov      rsi, qword ptr [rsp + 0x48]
0029B8CC  add      rsp, 0x20
0029B8D0  pop      rdi
0029B8D1  ret      
0029B8D2  mov      eax, 3
0029B8D7  mov      rbx, qword ptr [rsp + 0x40]
0029B8DC  mov      rsi, qword ptr [rsp + 0x48]
0029B8E1  add      rsp, 0x20
0029B8E5  pop      rdi
0029B8E6  ret      
0029B8E7  test     di, di
0029B8EA  jns      0x29b92b  ; -> 0029B92B
0029B8EC  mov      r10, qword ptr [rcx + 0xb20]
0029B8F3  movsx    r8d, byte ptr [rcx + 0xb48]
0029B8FB  test     r10, r10
0029B8FE  je       0x29b916  ; -> 0029B916
0029B900  mov      rcx, qword ptr [rcx + 0xb30]
0029B907  mov      r9d, r8d
0029B90A  mov      edx, 8
0029B90F  call     r10
0029B912  test     eax, eax
0029B914  je       0x29b92b  ; -> 0029B92B
0029B916  mov      eax, 8
0029B91B  mov      rbx, qword ptr [rsp + 0x40]
0029B920  mov      rsi, qword ptr [rsp + 0x48]
0029B925  add      rsp, 0x20
0029B929  pop      rdi
0029B92A  ret      
0029B92B  test     dil, 0xa0
0029B92F  je       0x29b970  ; -> 0029B970
0029B931  mov      r10, qword ptr [rbx + 0xb20]
0029B938  movsx    r8d, byte ptr [rbx + 0xb48]
0029B940  test     r10, r10
0029B943  je       0x29b95b  ; -> 0029B95B
0029B945  mov      rcx, qword ptr [rbx + 0xb30]
0029B94C  mov      r9d, r8d
0029B94F  mov      edx, 6
0029B954  call     r10
0029B957  test     eax, eax
0029B959  je       0x29b970  ; -> 0029B970
0029B95B  mov      eax, 6
0029B960  mov      rbx, qword ptr [rsp + 0x40]
0029B965  mov      rsi, qword ptr [rsp + 0x48]
0029B96A  add      rsp, 0x20
0029B96E  pop      rdi
0029B96F  ret      
0029B970  test     word ptr [rip + 0x1b70929], di  ; -> 01E0C2A0 [u16 0x2000]
0029B977  je       0x29b9b8  ; -> 0029B9B8
0029B979  mov      r10, qword ptr [rbx + 0xb20]
0029B980  movsx    r8d, byte ptr [rbx + 0xb48]
0029B988  test     r10, r10
0029B98B  je       0x29b9a3  ; -> 0029B9A3
0029B98D  mov      rcx, qword ptr [rbx + 0xb30]
0029B994  mov      r9d, r8d
0029B997  mov      edx, 2
0029B99C  call     r10
0029B99F  test     eax, eax
0029B9A1  je       0x29b9b8  ; -> 0029B9B8
0029B9A3  mov      eax, 2
0029B9A8  mov      rbx, qword ptr [rsp + 0x40]
0029B9AD  mov      rsi, qword ptr [rsp + 0x48]
0029B9B2  add      rsp, 0x20
0029B9B6  pop      rdi
0029B9B7  ret      
0029B9B8  mov      eax, 0x400
0029B9BD  test     ax, di
0029B9C0  je       0x29ba01  ; -> 0029BA01
0029B9C2  mov      r10, qword ptr [rbx + 0xb20]
0029B9C9  movsx    r8d, byte ptr [rbx + 0xb48]
0029B9D1  test     r10, r10
0029B9D4  je       0x29b9ec  ; -> 0029B9EC
0029B9D6  mov      rcx, qword ptr [rbx + 0xb30]
0029B9DD  mov      r9d, r8d
0029B9E0  mov      edx, 4
0029B9E5  call     r10
0029B9E8  test     eax, eax
0029B9EA  je       0x29ba01  ; -> 0029BA01
0029B9EC  mov      eax, 4
0029B9F1  mov      rbx, qword ptr [rsp + 0x40]
0029B9F6  mov      rsi, qword ptr [rsp + 0x48]
0029B9FB  add      rsp, 0x20
0029B9FF  pop      rdi
0029BA00  ret      
0029BA01  mov      eax, 0x800
0029BA06  test     ax, di
0029BA09  je       0x29ba4a  ; -> 0029BA4A
0029BA0B  mov      r10, qword ptr [rbx + 0xb20]
0029BA12  movsx    r8d, byte ptr [rbx + 0xb48]
0029BA1A  test     r10, r10
0029BA1D  je       0x29ba35  ; -> 0029BA35
0029BA1F  mov      rcx, qword ptr [rbx + 0xb30]
0029BA26  mov      r9d, r8d
0029BA29  mov      edx, 5
0029BA2E  call     r10
0029BA31  test     eax, eax
0029BA33  je       0x29ba4a  ; -> 0029BA4A
0029BA35  mov      eax, 5
0029BA3A  mov      rbx, qword ptr [rsp + 0x40]
0029BA3F  mov      rsi, qword ptr [rsp + 0x48]
0029BA44  add      rsp, 0x20
0029BA48  pop      rdi
0029BA49  ret      
0029BA4A  movzx    eax, dil
0029BA4E  mov      qword ptr [rsp + 0x30], rbp
0029BA53  and      al, 0x10
0029BA55  mov      qword ptr [rsp + 0x38], r14
0029BA5A  neg      al
0029BA5C  movzx    eax, sil
0029BA60  sbb      ecx, ecx
0029BA62  test     dil, 0x40
0029BA66  lea      edi, [rcx + 1]
0029BA69  cmove    edi, ecx
0029BA6C  and      al, 0x10
0029BA6E  neg      al
0029BA70  sbb      ecx, ecx
0029BA72  test     sil, 0x40
0029BA76  lea      esi, [rcx + 1]
0029BA79  cmove    esi, ecx
0029BA7C  call     0x1e0a10  ; -> 001E0A10 fn
0029BA81  mov      ebp, eax
0029BA83  call     0x1e0e30  ; -> 001E0E30 fn
0029BA88  test     ebp, ebp
0029BA8A  je       0x29ba98  ; -> 0029BA98
0029BA8C  test     eax, eax
0029BA8E  je       0x29ba94  ; -> 0029BA94
0029BA90  xor      edi, edi
0029BA92  jmp      0x29ba96  ; -> 0029BA96
0029BA94  sub      edi, ebp
0029BA96  sub      esi, ebp
0029BA98  movsx    r14d, byte ptr [rbx + 0xb48]
0029BAA0  mov      r9d, esi
0029BAA3  mov      edx, r14d
0029BAA6  mov      r8d, edi
0029BAA9  mov      rcx, rbx
0029BAAC  call     0x2975b0  ; -> 002975B0 fn
0029BAB1  movsxd   rbp, eax
0029BAB4  test     edi, edi
0029BAB6  jne      0x29babc  ; -> 0029BABC
0029BAB8  test     esi, esi
0029BABA  je       0x29bb24  ; -> 0029BB24
0029BABC  mov      r8d, ebp
0029BABF  mov      rcx, rbx
0029BAC2  cmp      ebp, r14d
0029BAC5  jne      0x29badc  ; -> 0029BADC
0029BAC7  mov      edx, 7
0029BACC  call     0x29b790  ; -> 0029B790 fn
0029BAD1  test     eax, eax
0029BAD3  je       0x29bb24  ; -> 0029BB24
0029BAD5  mov      eax, 7
0029BADA  jmp      0x29bb26  ; -> 0029BB26
0029BADC  mov      edx, 1
0029BAE1  call     0x29b790  ; -> 0029B790 fn
0029BAE6  test     eax, eax
0029BAE8  je       0x29bb24  ; -> 0029BB24
0029BAEA  movsx    rcx, byte ptr [rbx + 0xb48]
0029BAF2  mov      eax, 1
0029BAF7  imul     rdx, rcx, 0x160
0029BAFE  mov      ecx, 0xfffb
0029BB03  and      word ptr [rdx + rbx + 0x318], cx
0029BB0B  imul     rdx, rbp, 0x160
0029BB12  or       word ptr [rdx + rbx + 0x318], 4
0029BB1B  mov      byte ptr [rbx + 0xb48], bpl
0029BB22  jmp      0x29bb26  ; -> 0029BB26
0029BB24  xor      eax, eax
0029BB26  mov      rbp, qword ptr [rsp + 0x30]
0029BB2B  mov      r14, qword ptr [rsp + 0x38]
0029BB30  mov      rbx, qword ptr [rsp + 0x40]
0029BB35  mov      rsi, qword ptr [rsp + 0x48]
0029BB3A  add      rsp, 0x20
0029BB3E  pop      rdi
0029BB3F  ret      
```

## 0029C770 (216 B, extent 0029C770-0029C848)

Page context: "alled by '00273E30', '00295D90', '00298250', '002A4430' and 8 more; '002B3400' is called by '00243860', '0027AD70', '002A86A0', '003EE420' and 4 more; '002475D0' is called by '00296960', '00298250', '0029C770', '0029C9D0' and 1 more; '00247680' is called by '005599D0', '0055A1F0', '0056B4D0'; '002A8C50' calls '002ABF70', '002AC5F0', '002B2150'; '002AC2F0' is called by '002AE610', '002AF340', '002B2150'; '0017F8C0' is called by '002AF340"

```
0029C770  mov      qword ptr [rsp + 8], rbx
0029C775  push     rdi
0029C776  sub      rsp, 0x20
0029C77A  lea      rdi, [rcx + 0x180]
0029C781  mov      rbx, rcx
0029C784  mov      rcx, rdi
0029C787  call     0x273a20  ; -> 00273A20 fn
0029C78C  test     eax, eax
0029C78E  je       0x29c79d  ; -> 0029C79D
0029C790  xor      eax, eax
0029C792  mov      rbx, qword ptr [rsp + 0x30]
0029C797  add      rsp, 0x20
0029C79B  pop      rdi
0029C79C  ret      
0029C79D  xor      r9d, r9d
0029C7A0  lea      r8, [rip + 0x328a89]  ; -> 005C5230
0029C7A7  mov      edx, 0xc0
0029C7AC  mov      rcx, rdi
0029C7AF  call     0x245000  ; -> 00245000 fn
0029C7B4  lea      rdx, [rbx + 0x218]
0029C7BB  mov      rcx, rbx
0029C7BE  call     0x2974e0  ; -> 002974E0 fn
0029C7C3  xor      edx, edx
0029C7C5  mov      rcx, rdi
0029C7C8  call     0x2475d0  ; -> 002475D0 fn
0029C7CD  mov      edx, 9
0029C7D2  mov      rcx, rdi
0029C7D5  call     0x247930  ; -> 00247930 fn
0029C7DA  xor      ecx, ecx
0029C7DC  call     0x2735e0  ; -> 002735E0 fn
0029C7E1  mov      rdx, rax
0029C7E4  mov      rcx, rdi
0029C7E7  call     0x247570  ; -> 00247570 fn
0029C7EC  mov      rdx, rdi
0029C7EF  mov      rcx, rbx
0029C7F2  call     0x244960  ; -> 00244960 fn
0029C7F7  mov      rcx, rdi
0029C7FA  call     0x246ac0  ; -> 00246AC0 fn
0029C7FF  xor      edx, edx
0029C801  cmp      byte ptr [rbx + 0xb42], dl
0029C807  jbe      0x29c838  ; -> 0029C838
0029C809  lea      rax, [rbx + 0x318]
0029C810  mov      r8d, 0x80
0029C816  nop      word ptr [rax + rax]
0029C820  or       word ptr [rax], r8w
0029C824  lea      rax, [rax + 0x160]
0029C82B  movzx    ecx, byte ptr [rbx + 0xb42]
0029C832  inc      edx
0029C834  cmp      edx, ecx
0029C836  jl       0x29c820  ; -> 0029C820
0029C838  mov      eax, 1
0029C83D  mov      rbx, qword ptr [rsp + 0x30]
0029C842  add      rsp, 0x20
0029C846  pop      rdi
0029C847  ret      
```

## 0029C9D0 (219 B, extent 0029C9D0-0029CAAB)

Page context: "273E30', '00295D90', '00298250', '002A4430' and 8 more; '002B3400' is called by '00243860', '0027AD70', '002A86A0', '003EE420' and 4 more; '002475D0' is called by '00296960', '00298250', '0029C770', '0029C9D0' and 1 more; '00247680' is called by '005599D0', '0055A1F0', '0056B4D0'; '002A8C50' calls '002ABF70', '002AC5F0', '002B2150'; '002AC2F0' is called by '002AE610', '002AF340', '002B2150'; '0017F8C0' is called by '002AF340', '002B2150"

```
0029C9D0  mov      qword ptr [rsp + 8], rbx
0029C9D5  push     rdi
0029C9D6  sub      rsp, 0x20
0029C9DA  lea      rbx, [rcx + 0xc0]
0029C9E1  mov      rdi, rcx
0029C9E4  mov      rcx, rbx
0029C9E7  call     0x273a20  ; -> 00273A20 fn
0029C9EC  test     eax, eax
0029C9EE  je       0x29c9fd  ; -> 0029C9FD
0029C9F0  xor      eax, eax
0029C9F2  mov      rbx, qword ptr [rsp + 0x30]
0029C9F7  add      rsp, 0x20
0029C9FB  pop      rdi
0029C9FC  ret      
0029C9FD  xor      r9d, r9d
0029CA00  lea      r8, [rip + 0x328829]  ; -> 005C5230
0029CA07  mov      edx, 0xc0
0029CA0C  mov      rcx, rbx
0029CA0F  call     0x245000  ; -> 00245000 fn
0029CA14  lea      rdx, [rdi + 0x158]
0029CA1B  mov      rcx, rdi
0029CA1E  call     0x2974e0  ; -> 002974E0 fn
0029CA23  xor      edx, edx
0029CA25  mov      rcx, rbx
0029CA28  call     0x2475d0  ; -> 002475D0 fn
0029CA2D  mov      edx, 9
0029CA32  mov      rcx, rbx
0029CA35  call     0x247930  ; -> 00247930 fn
0029CA3A  xor      ecx, ecx
0029CA3C  call     0x2735e0  ; -> 002735E0 fn
0029CA41  mov      rdx, rax
0029CA44  mov      rcx, rbx
0029CA47  call     0x247570  ; -> 00247570 fn
0029CA4C  mov      rdx, rbx
0029CA4F  mov      rcx, rdi
0029CA52  call     0x244960  ; -> 00244960 fn
0029CA57  mov      rcx, rbx
0029CA5A  call     0x246ac0  ; -> 00246AC0 fn
0029CA5F  xor      ebx, ebx
0029CA61  cmp      byte ptr [rdi + 0xb42], bl
0029CA67  jbe      0x29ca9b  ; -> 0029CA9B
0029CA69  nop      dword ptr [rax]
0029CA70  movsxd   rax, ebx
0029CA73  mov      edx, 0xb
0029CA78  imul     rcx, rax, 0xd8
0029CA7F  add      rcx, 0x7c0
0029CA86  add      rcx, rdi
0029CA89  call     0x247930  ; -> 00247930 fn
0029CA8E  movzx    eax, byte ptr [rdi + 0xb42]
0029CA95  inc      ebx
0029CA97  cmp      ebx, eax
0029CA99  jl       0x29ca70  ; -> 0029CA70
0029CA9B  mov      eax, 1
0029CAA0  mov      rbx, qword ptr [rsp + 0x30]
0029CAA5  add      rsp, 0x20
0029CAA9  pop      rdi
0029CAAA  ret      
```
