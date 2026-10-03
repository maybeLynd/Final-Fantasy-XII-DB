# Homing pack: `99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-the-text-element-dispatch-table.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0028F830 (26 B, extent 0028F830-0028F84A)

Entered from (direct sites whose caller this page cites): `00299090` + 0x67 (call; `00299090` is cited on this page)
Other direct sites: `0029BE50` + 0x384 (call)

Host context: "yOrAuthoredThresholdGate' ('0032A8A0') calls 'PersistentFlag_QueryAuthoredThresholdSchedule' ('00377970').  **UI — MECHANICAL, 87 edges.** '001EDEC0' is called by '00252030', '00276D30', '0027C870', '00299090' and 9 more; '00254A10' is called by '00273E30', '00295D90', '00298250', '002A4430' and 8 more; '002B3400' is called by '00243860', '0027AD70', '002A86A0', '003EE420' and 4 more; '002475D0' is called by '00296960', '00298250', '002"

```
0028F830  mov      rdx, qword ptr [rip + 0x1e0c649]  ; -> 0209BE80
0028F837  test     rdx, rdx
0028F83A  jne      0x28f83f  ; -> 0028F83F
0028F83C  xor      eax, eax
0028F83E  ret      
0028F83F  movsxd   rax, ecx
0028F842  shl      rax, 5
0028F846  add      rax, rdx
0028F849  ret      
```

## 00297290 (336 B, extent 00297290-002973E0)

Entered from (direct sites whose caller this page cites): `00299090` + 0x389 (call; `00299090` is cited on this page)
Other direct sites: none

Host context: "yOrAuthoredThresholdGate' ('0032A8A0') calls 'PersistentFlag_QueryAuthoredThresholdSchedule' ('00377970').  **UI — MECHANICAL, 87 edges.** '001EDEC0' is called by '00252030', '00276D30', '0027C870', '00299090' and 9 more; '00254A10' is called by '00273E30', '00295D90', '00298250', '002A4430' and 8 more; '002B3400' is called by '00243860', '0027AD70', '002A86A0', '003EE420' and 4 more; '002475D0' is called by '00296960', '00298250', '002"

```
00297290  mov      qword ptr [rsp + 0x18], rbx
00297295  push     rbp
00297296  mov      rbp, rsp
00297299  sub      rsp, 0x80
002972A0  mov      rax, qword ptr [rip + 0x1cad589]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002972A7  xor      rax, rsp
002972AA  mov      qword ptr [rbp - 8], rax
002972AE  xor      r9d, r9d
002972B1  test     rdx, rdx
002972B4  jne      0x2972bb  ; -> 002972BB
002972B6  mov      ebx, r9d
002972B9  jmp      0x2972c3  ; -> 002972C3
002972BB  mov      rax, qword ptr [rdx + 0x60]
002972BF  mov      rbx, qword ptr [rax + 0x10]
002972C3  test     byte ptr [rcx + 2], 1
002972C7  jne      0x2972d2  ; -> 002972D2
002972C9  and      dword ptr [rbx + 8], 0xfffffffe
002972CD  jmp      0x2973c3  ; -> 002973C3
002972D2  mov      r10d, 0x100
002972D8  mov      dword ptr [rbp - 0x30], r9d
002972DC  mov      r8d, 2
002972E2  mov      word ptr [rbp - 0x2c], r9w
002972E7  mov      dword ptr [rbp - 0x2a], 0x28000
002972EE  mov      dword ptr [rbp - 0x26], r10d
002972F2  mov      dword ptr [rbp - 0x22], 0x800000
002972F9  lea      eax, [r8 - 1]
002972FD  mov      dword ptr [rbp - 0x1e], 0x1ffff
00297304  or       dword ptr [rbx + 8], eax
00297307  movzx    eax, byte ptr [rcx + 2]
0029730B  mov      dword ptr [rbp - 0x1a], r10d
0029730F  mov      dword ptr [rbp - 0x16], 0x1000000
00297316  mov      dword ptr [rbp - 0x12], 0x28080
0029731D  mov      word ptr [rbp - 0xe], r10w
00297322  mov      dword ptr [rbp - 0x48], r9d
00297326  mov      word ptr [rbp - 0x44], r9w
0029732B  mov      dword ptr [rbp - 0x42], 0x8000
00297332  mov      dword ptr [rbp - 0x3e], r10d
00297336  mov      dword ptr [rbp - 0x3a], 0x1000000
0029733D  mov      dword ptr [rbp - 0x36], 0x8080
00297344  mov      word ptr [rbp - 0x32], r10w
00297349  test     r8b, al
0029734C  je       0x29736a  ; -> 0029736A
0029734E  add      word ptr [rcx], 0x10
00297352  lea      rdx, [rbp - 0x30]
00297356  mov      r8d, 3
0029735C  cmp      word ptr [rcx], r10w
00297360  jl       0x297393  ; -> 00297393
00297362  mov      word ptr [rcx], r10w
00297366  and      al, 0xfd
00297368  jmp      0x29738a  ; -> 0029738A
0029736A  lea      rdx, [rbp - 0x48]
0029736E  test     al, 4
00297370  je       0x297381  ; -> 00297381
00297372  add      word ptr [rcx], -0x10
00297376  cmp      word ptr [rcx], r9w
0029737A  jg       0x297393  ; -> 00297393
0029737C  mov      dword ptr [rcx], r9d
0029737F  jmp      0x297393  ; -> 00297393
00297381  inc      byte ptr [rcx + 3]
00297384  cmp      byte ptr [rcx + 3], 0x40
00297388  jbe      0x297393  ; -> 00297393
0029738A  or       al, 4
0029738C  mov      byte ptr [rcx + 3], r9b
00297390  mov      byte ptr [rcx + 2], al
00297393  movsx    r9d, word ptr [rcx]
00297397  lea      rcx, [rbp - 0x58]
0029739B  call     0x271ab0  ; -> 00271AB0 fn
002973A0  movzx    eax, word ptr [rbp - 0x52]
002973A4  mov      byte ptr [rbp - 0x60], al
002973A7  mov      byte ptr [rbp - 0x5f], al
002973AA  mov      byte ptr [rbp - 0x5e], al
002973AD  movzx    eax, byte ptr [rbp - 0x54]
002973B1  mov      byte ptr [rbp - 0x5d], al
002973B4  mov      eax, dword ptr [rbp - 0x60]
002973B7  mov      dword ptr [rbx + 0x34], eax
002973BA  mov      dword ptr [rbx + 0x30], eax
002973BD  mov      dword ptr [rbx + 0x2c], eax
002973C0  mov      dword ptr [rbx + 0x28], eax
002973C3  mov      rcx, qword ptr [rbp - 8]
002973C7  xor      rcx, rsp
002973CA  call     0x808c40  ; -> 00808C40 fn
002973CF  mov      rbx, qword ptr [rsp + 0xa0]
002973D7  add      rsp, 0x80
002973DE  pop      rbp
002973DF  ret      
```

## 002974E0 (208 B, extent 002974E0-002975B0)

Entered from (direct sites whose caller this page cites): `0029C770` + 0x4E (call; `0029C770` is cited on this page); `0029C9D0` + 0x4E (call; `0029C9D0` is cited on this page)
Other direct sites: none

Host context: "alled by '00273E30', '00295D90', '00298250', '002A4430' and 8 more; '002B3400' is called by '00243860', '0027AD70', '002A86A0', '003EE420' and 4 more; '002475D0' is called by '00296960', '00298250', '0029C770', '0029C9D0' and 1 more; '00247680' is called by '005599D0', '0055A1F0', '0056B4D0'; '002A8C50' calls '002ABF70', '002AC5F0', '002B2150'; '002AC2F0' is called by '002AE610', '002AF340', '002B2150'; '0017F8C0' is called by '002AF340" / "273E30', '00295D90', '00298250', '002A4430' and 8 more; '002B3400' is called by '00243860', '0027AD70', '002A86A0', '003EE420' and 4 more; '002475D0' is called by '00296960', '00298250', '0029C770', '0029C9D0' and 1 more; '00247680' is called by '005599D0', '0055A1F0', '0056B4D0'; '002A8C50' calls '002ABF70', '002AC5F0', '002B2150'; '002AC2F0' is called by '002AE610', '002AF340', '002B2150'; '0017F8C0' is called by '002AF340', '002B2150"

```
002974E0  mov      qword ptr [rsp + 0x10], rsi
002974E5  mov      qword ptr [rsp + 0x18], rdi
002974EA  push     r14
002974EC  sub      rsp, 0x20
002974F0  mov      r14, rdx
002974F3  mov      rsi, rcx
002974F6  xor      edi, edi
002974F8  call     0x35bb60  ; -> 0035BB60 fn
002974FD  test     eax, eax
002974FF  jle      0x29759f  ; -> 0029759F
00297505  mov      qword ptr [rsp + 0x30], rbx
0029750A  lea      rbx, [rsi + 0x240]
00297511  cmp      byte ptr [rbx + 0xde], 1
00297518  je       0x29752e  ; -> 0029752E
0029751A  inc      edi
0029751C  add      rbx, 0x160
00297523  call     0x35bb60  ; -> 0035BB60 fn
00297528  cmp      edi, eax
0029752A  jl       0x297511  ; -> 00297511
0029752C  jmp      0x29759a  ; -> 0029759A
0029752E  mov      rax, qword ptr [rbx + 0x60]
00297532  mov      r9, qword ptr [rax + 0xd0]
00297539  movzx    eax, word ptr [r9 + 0xc]
0029753E  mov      word ptr [r14], ax
00297542  mov      rax, qword ptr [rsi + 0xb38]
00297549  mov      r8, qword ptr [rax + 0x58]
0029754D  movzx    eax, byte ptr [rsi + 0xb42]
00297554  dec      ax
00297557  movsx    edx, ax
0029755A  movsx    ecx, word ptr [r8 + 0xc]
0029755F  movzx    eax, word ptr [r8 + 6]
00297564  imul     edx, ecx
00297567  sub      ax, dx
0029756A  add      ax, word ptr [r9 + 0xe]
0029756F  mov      word ptr [r14 + 2], ax
00297574  movzx    eax, word ptr [r9 + 0x10]
00297579  mov      word ptr [r14 + 4], ax
0029757E  mov      rcx, qword ptr [rbx + 0x58]
00297582  movzx    edx, byte ptr [rsi + 0xb42]
00297589  movsx    eax, word ptr [rcx + 0xc]
0029758D  imul     eax, edx
00297590  sub      ax, word ptr [r9 + 0x12]
00297595  mov      word ptr [r14 + 6], ax
0029759A  mov      rbx, qword ptr [rsp + 0x30]
0029759F  mov      rsi, qword ptr [rsp + 0x38]
002975A4  mov      rdi, qword ptr [rsp + 0x40]
002975A9  add      rsp, 0x20
002975AD  pop      r14
002975AF  ret      
```

## 002975B0 (138 B, extent 002975B0-0029763A)

Entered from (direct sites whose caller this page cites): `0029B870` + 0x23C (call; `0029B870` is cited on this page)
Other direct sites: none

Host context: "; '002A8C50' calls '002ABF70', '002AC5F0', '002B2150'; '002AC2F0' is called by '002AE610', '002AF340', '002B2150'; '0017F8C0' is called by '002AF340', '002B2150'; '001E0A10' is called by '00284EC0', '0029B870'; '002A6190' calls '002A4430', '002A4830'; '002A9F00' is called by '002AC5F0', '002AE610'; '002AAE40' calls '002AC5F0', '002B2150'; '002AC5F0' calls '002AE610', '002B2150'; '002AC5F0' is called by '002AF340', '002B2150'; '002AF960'"

```
002975B0  mov      qword ptr [rsp + 8], rbx
002975B5  mov      qword ptr [rsp + 0x10], rdi
002975BA  mov      edi, r9d
002975BD  mov      r10d, r8d
002975C0  mov      r11d, edx
002975C3  mov      rbx, rcx
002975C6  test     r8d, r8d
002975C9  jne      0x2975d0  ; -> 002975D0
002975CB  test     r9d, r9d
002975CE  je       0x29762c  ; -> 0029762C
002975D0  movzx    r8d, byte ptr [rcx + 0xb42]
002975D8  xor      r9d, r9d
002975DB  mov      eax, r11d
002975DE  test     r8d, r8d
002975E1  je       0x29762c  ; -> 0029762C
002975E3  test     r10d, r10d
002975E6  je       0x2975fd  ; -> 002975FD
002975E8  add      eax, r10d
002975EB  jns      0x2975f1  ; -> 002975F1
002975ED  lea      eax, [r8 - 1]
002975F1  xor      ecx, ecx
002975F3  cmp      eax, r8d
002975F6  cmovl    ecx, eax
002975F9  mov      eax, ecx
002975FB  jmp      0x297610  ; -> 00297610
002975FD  lea      ecx, [rax + rdi]
00297600  xor      eax, eax
00297602  test     ecx, ecx
00297604  cmovns   eax, ecx
00297607  cmp      eax, r8d
0029760A  jl       0x297610  ; -> 00297610
0029760C  lea      eax, [r8 - 1]
00297610  movsxd   rcx, eax
00297613  imul     rdx, rcx, 0x160
0029761A  test     byte ptr [rdx + rbx + 0x318], 1
00297622  jne      0x29762f  ; -> 0029762F
00297624  inc      r9d
00297627  cmp      r9d, r8d
0029762A  jl       0x2975e3  ; -> 002975E3
0029762C  mov      eax, r11d
0029762F  mov      rbx, qword ptr [rsp + 8]
00297634  mov      rdi, qword ptr [rsp + 0x10]
00297639  ret      
```
