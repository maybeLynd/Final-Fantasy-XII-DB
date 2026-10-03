# Homing pack: `04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-the-npc-name-dictionary.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00182870 (70 B, extent 00182870-001828B6)

Entered from (direct sites whose caller this page cites): `00382BF0` + 0xCC (call; `00382BF0` is cited on this page); `00382BF0` + 0xF6 (call; `00382BF0` is cited on this page)
Other direct sites: none

Host context: "0'; then the '00254380'/'00264F90'/'00315DC0'/'00380170'/'0046B180'/'0046B240'/'00473BB0' chain iterates 'cx' - the dictionary's armed-table walk.  Interior anchor '003C0A4A' (function '003C0A00').  '00382BF0' (285 B) is the '02AEDFA0'-gated position publisher '0053AB50' calls: 'dword[02AEDFA0] != ecx' exits; 'word[02AEDFA0]' resolves 'sx x 0x740 + 022C6F28' (a '-1', a null base, or 'dword[+0x284] == 0' fails into '00182870(0, -1.0f, 0)" / "0'; then the '00254380'/'00264F90'/'00315DC0'/'00380170'/'0046B180'/'0046B240'/'00473BB0' chain iterates 'cx' - the dictionary's armed-table walk.  Interior anchor '003C0A4A' (function '003C0A00').  '00382BF0' (285 B) is the '02AEDFA0'-gated position publisher '0053AB50' calls: 'dword[02AEDFA0] != ecx' exits; 'word[02AEDFA0]' resolves 'sx x 0x740 + 022C6F28' (a '-1', a null base, or 'dword[+0x284] == 0' fails into '00182870(0, -1.0f, 0)"

```
00182870  mov      qword ptr [rsp + 8], rbx
00182875  push     rdi
00182876  sub      rsp, 0x30
0018287A  movaps   xmmword ptr [rsp + 0x20], xmm6
0018287F  mov      rbx, r8
00182882  movaps   xmm6, xmm1
00182885  mov      edi, ecx
00182887  call     0x193d50  ; -> 00193D50 fn
0018288C  test     rax, rax
0018288F  je       0x1828a6  ; -> 001828A6
00182891  call     0x193d50  ; -> 00193D50 fn
00182896  mov      rcx, rax
00182899  mov      r9, rbx
0018289C  movaps   xmm2, xmm6
0018289F  mov      edx, edi
001828A1  call     0x194490  ; -> 00194490 fn
001828A6  mov      rbx, qword ptr [rsp + 0x40]
001828AB  movaps   xmm6, xmmword ptr [rsp + 0x20]
001828B0  add      rsp, 0x30
001828B4  pop      rdi
001828B5  ret      
```

## 001D9930 (131 B, extent 001D9930-001D99B3)

Entered from (direct sites whose caller this page cites): `001DA220` + 0x42 (call; `001DA220` is cited on this page); `001DA970` + 0x40 (call; `001DA970` is cited on this page)
Other direct sites: none

Host context: "d-helper fan-in; no AI relationship to the dictionary.  **Resource — SERVICE (SWE2-EC7-163, 49 edges).** The dictionary's table helpers are consulted by the Resource loaders: '00265270' is called by '001DA220'/ '001DA970' there, and '002DF780' calls '001D6B40'/'001D6D90' (+45 more of the same shape). Mechanical fan-in; no shared ownership.  ## The '00379D20' exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)  '00379D20' " / "-in; no AI relationship to the dictionary.  **Resource — SERVICE (SWE2-EC7-163, 49 edges).** The dictionary's table helpers are consulted by the Resource loaders: '00265270' is called by '001DA220'/ '001DA970' there, and '002DF780' calls '001D6B40'/'001D6D90' (+45 more of the same shape). Mechanical fan-in; no shared ownership.  ## The '00379D20' exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)  '00379D20' (~36 B) — '0"

```
001D9930  mov      qword ptr [rsp + 0x18], rbp
001D9935  push     rdi
001D9936  sub      rsp, 0x20
001D993A  lea      rdi, [rcx + 0x118]
001D9941  mov      rbp, rcx
001D9944  cmp      qword ptr [rdi], rdi
001D9947  je       0x1d99a8  ; -> 001D99A8
001D9949  mov      qword ptr [rsp + 0x30], rbx
001D994E  mov      rbx, qword ptr [rdi]
001D9951  cmp      rbx, rdi
001D9954  je       0x1d9967  ; -> 001D9967
001D9956  mov      rcx, qword ptr [rbx + 0x10]
001D995A  call     0x210eb0  ; -> 00210EB0 fn
001D995F  mov      rbx, qword ptr [rbx]
001D9962  cmp      rbx, rdi
001D9965  jne      0x1d9956  ; -> 001D9956
001D9967  mov      rbx, qword ptr [rdi]
001D996A  cmp      rbx, rdi
001D996D  je       0x1d9995  ; -> 001D9995
001D996F  mov      qword ptr [rsp + 0x38], rsi
001D9974  mov      rax, qword ptr [rdi + 0x10]
001D9978  lea      rcx, [rdi + 0x10]
001D997C  mov      rdx, rbx
001D997F  mov      r8d, 0x18
001D9985  mov      rbx, qword ptr [rbx]
001D9988  call     qword ptr [rax + 0x18]
001D998B  cmp      rbx, rdi
001D998E  jne      0x1d9974  ; -> 001D9974
001D9990  mov      rsi, qword ptr [rsp + 0x38]
001D9995  mov      rbx, qword ptr [rsp + 0x30]
001D999A  mov      qword ptr [rdi], rdi
001D999D  mov      qword ptr [rdi + 8], rdi
001D99A1  mov      byte ptr [rbp + 0x130], 1
001D99A8  mov      rbp, qword ptr [rsp + 0x40]
001D99AD  add      rsp, 0x20
001D99B1  pop      rdi
001D99B2  ret      
```

## 001D9EC0 (171 B, extent 001D9EC0-001D9F6B)

Entered from (direct sites whose caller this page cites): `001DA220` + 0x56 (call; `001DA220` is cited on this page); `001DA970` + 0x54 (call; `001DA970` is cited on this page)
Other direct sites: none

Host context: "d-helper fan-in; no AI relationship to the dictionary.  **Resource — SERVICE (SWE2-EC7-163, 49 edges).** The dictionary's table helpers are consulted by the Resource loaders: '00265270' is called by '001DA220'/ '001DA970' there, and '002DF780' calls '001D6B40'/'001D6D90' (+45 more of the same shape). Mechanical fan-in; no shared ownership.  ## The '00379D20' exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)  '00379D20' " / "-in; no AI relationship to the dictionary.  **Resource — SERVICE (SWE2-EC7-163, 49 edges).** The dictionary's table helpers are consulted by the Resource loaders: '00265270' is called by '001DA220'/ '001DA970' there, and '002DF780' calls '001D6B40'/'001D6D90' (+45 more of the same shape). Mechanical fan-in; no shared ownership.  ## The '00379D20' exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)  '00379D20' (~36 B) — '0"

```
001D9EC0  mov      qword ptr [rsp + 0x10], rbx
001D9EC5  mov      qword ptr [rsp + 0x18], rbp
001D9ECA  mov      qword ptr [rsp + 0x20], rsi
001D9ECF  push     rdi
001D9ED0  sub      rsp, 0x20
001D9ED4  lea      rsi, [rcx + 0xd0]
001D9EDB  xor      ebp, ebp
001D9EDD  mov      rbx, qword ptr [rsi]
001D9EE0  mov      rdi, rcx
001D9EE3  cmp      rbx, rsi
001D9EE6  je       0x1d9f56  ; -> 001D9F56
001D9EE8  mov      qword ptr [rsp + 0x30], r14
001D9EED  lea      r14d, [rbp + 1]
001D9EF1  mov      rdx, qword ptr [rbx + 0x10]
001D9EF5  movzx    ecx, word ptr [rdi + 0xe8]
001D9EFC  movzx    eax, word ptr [rdx]
001D9EFF  cmp      ax, cx
001D9F02  jne      0x1d9f15  ; -> 001D9F15
001D9F04  cmp      word ptr [rdi + 0x1bc], cx
001D9F0B  je       0x1d9f12  ; -> 001D9F12
001D9F0D  mov      edx, dword ptr [rdx + 4]
001D9F10  jmp      0x1d9f41  ; -> 001D9F41
001D9F12  cmp      ax, cx
001D9F15  jle      0x1d9f49  ; -> 001D9F49
001D9F17  movzx    ecx, word ptr [rdi + 0x1bc]
001D9F1E  cmp      ax, cx
001D9F21  jne      0x1d9f28  ; -> 001D9F28
001D9F23  mov      edx, dword ptr [rdx + 4]
001D9F26  jmp      0x1d9f41  ; -> 001D9F41
001D9F28  jl       0x1d9f2f  ; -> 001D9F2F
001D9F2A  test     bp, bp
001D9F2D  jne      0x1d9f51  ; -> 001D9F51
001D9F2F  mov      word ptr [rdi + 0x1bc], ax
001D9F36  movzx    ebp, r14w
001D9F3A  mov      rax, qword ptr [rbx + 0x10]
001D9F3E  mov      edx, dword ptr [rax + 4]
001D9F41  mov      rcx, rdi
001D9F44  call     0x1d9da0  ; -> 001D9DA0 fn
001D9F49  mov      rbx, qword ptr [rbx]
001D9F4C  cmp      rbx, rsi
001D9F4F  jne      0x1d9ef1  ; -> 001D9EF1
001D9F51  mov      r14, qword ptr [rsp + 0x30]
001D9F56  mov      rbx, qword ptr [rsp + 0x38]
001D9F5B  mov      rbp, qword ptr [rsp + 0x40]
001D9F60  mov      rsi, qword ptr [rsp + 0x48]
001D9F65  add      rsp, 0x20
001D9F69  pop      rdi
001D9F6A  ret      
```
