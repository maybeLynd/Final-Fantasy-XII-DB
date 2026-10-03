# Homing pack: `14-Story-Event-Quest-Hunt/CONTRACT-persistent-flag-banks.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-persistent-flag-banks.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001D9930 (131 B, extent 001D9930-001D99B3)

Entered from (direct sites whose caller this page cites): `001DA220` + 0x42 (call; `001DA220` is cited on this page); `001DA970` + 0x40 (call; `001DA970` is cited on this page)
Other direct sites: none

Host context: "9B20', '002B0280' (Rendering) - shared machinery across the layer boundary, no shared ownership. - **Resource - CLIENT and SERVICE (4 edges).** '00265270' is also called by bodies filed to resource: '001DA220', '001DA970'; '00378540' reaches bodies filed to resource: '0032E400', '0032E620' - shared machinery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (35 edges).** '002E16B0' is also called by bo" / "0280' (Rendering) - shared machinery across the layer boundary, no shared ownership. - **Resource - CLIENT and SERVICE (4 edges).** '00265270' is also called by bodies filed to resource: '001DA220', '001DA970'; '00378540' reaches bodies filed to resource: '0032E400', '0032E620' - shared machinery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (35 edges).** '002E16B0' is also called by bodies filed t"

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

Host context: "9B20', '002B0280' (Rendering) - shared machinery across the layer boundary, no shared ownership. - **Resource - CLIENT and SERVICE (4 edges).** '00265270' is also called by bodies filed to resource: '001DA220', '001DA970'; '00378540' reaches bodies filed to resource: '0032E400', '0032E620' - shared machinery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (35 edges).** '002E16B0' is also called by bo" / "0280' (Rendering) - shared machinery across the layer boundary, no shared ownership. - **Resource - CLIENT and SERVICE (4 edges).** '00265270' is also called by bodies filed to resource: '001DA220', '001DA970'; '00378540' reaches bodies filed to resource: '0032E400', '0032E620' - shared machinery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (35 edges).** '002E16B0' is also called by bodies filed t"

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

## 002A3210 (51 B, extent 002A3210-002A3243)

Entered from (direct sites whose caller this page cites): `002E16B0` + 0x2D7 (call; `002E16B0` is cited on this page)
Other direct sites: none

Host context: "e verdict C-V4, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*, and script accessor '0034E980'; 'SetBank2048'      '0032ABF0' has three — the message-window opener '002E16B0' ('SetBank2048(actor +0x102, 1)')      and script accessors '0034DFA0'/'0034E320'. The index space is the NPC-name dictionary's —      which is why it needs 2,048 bits.    - 'Bank64A'/'Bank64B' **do** have no engine consumer — prov"

```
002A3210  shl      r9d, 0x12
002A3214  xor      r9d, dword ptr [rcx + 0x180]
002A321B  and      r9d, 0x40000
002A3222  mov      byte ptr [rcx + 0x174], dl
002A3228  xor      r9d, dword ptr [rcx + 0x180]
002A322F  bts      r9d, 0x11
002A3234  mov      byte ptr [rcx + 0x175], r8b
002A323B  mov      dword ptr [rcx + 0x180], r9d
002A3242  ret      
```
