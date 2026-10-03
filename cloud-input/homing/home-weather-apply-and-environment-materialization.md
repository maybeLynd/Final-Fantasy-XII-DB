# Homing pack: `03-World-Area-Field/Weather/weather-apply-and-environment-materialization.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-weather-apply-and-environment-materialization.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0028F830 (26 B, extent 0028F830-0028F84A)

Entered from (direct sites whose caller this page cites): `00299090` + 0x67 (call; `00299090` is cited on this page)
Other direct sites: `0029BE50` + 0x384 (call)

Host context: "/'002DF9A0'/'0032EAE0'/'00379D20' of that layer — the weather frame consumes resource helpers, not a shared responsibility. **UI — CLIENT (SWE2-EC7-156, 25 edges).** '00252030'/'00276D30'/'0027C870'/'00299090' call '001EDEC0' — the interface layer consults this page's helper, shared fan-in. - **Audio - CLIENT (161 edges).** '001243B0' is also called by bodies filed to audio: '00121030', '00121E20', '00210ED0' - shared machinery across t"

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

## 002E80B0 (74 B, extent 002E80B0-002E80FA)

Entered from (direct sites whose caller this page cites): `003DCD00` + 0x34 (call; `003DCD00` is cited on this page)
Other direct sites: none

Host context: "finish - the weather record's per-element initializer (pre-named by the batch-121 crossing row).  Interior anchor '0032B63F' (function '0032B600').  '003DC8D0' (303 B) is the keyed insert '003DC5B0'/'003DCD00' call on '02B580B0' (0xC stride to '02B58170'): the '(ecx, dx, r8b)' triple scans for a live slot; a miss claims '02B58174''s index, stores the key + '-1' + '003DCA30''s byte, and a non-negative 'rsp+0x70' index runs '0032E400' int"

```
002E80B0  test     rcx, rcx
002E80B3  je       0x2e80f4  ; -> 002E80F4
002E80B5  mov      rax, qword ptr [rcx + 0xc0]
002E80BC  test     rax, rax
002E80BF  je       0x2e80f4  ; -> 002E80F4
002E80C1  cmp      dword ptr [rax], -1
002E80C4  je       0x2e80f4  ; -> 002E80F4
002E80C6  movzx    ecx, word ptr [rax]
002E80C9  cmp      cx, -1
002E80CD  jne      0x2e80d2  ; -> 002E80D2
002E80CF  xor      eax, eax
002E80D1  ret      
002E80D2  movsx    rax, cx
002E80D6  imul     rcx, rax, 0x740
002E80DD  add      rcx, qword ptr [rip + 0x1fdee44]  ; -> 022C6F28
002E80E4  je       0x2e80cf  ; -> 002E80CF
002E80E6  cmp      dword ptr [rcx + 0x284], 0
002E80ED  je       0x2e80cf  ; -> 002E80CF
002E80EF  jmp      0x423170  ; -> 00423170 fn
002E80F4  mov      eax, 1
002E80F9  ret      
```

## 0037D7F0 (158 B, extent 0037D7F0-0037D88E)

Entered from (direct sites whose caller this page cites): `00379D00` + 0x4 (call; `00379D00` is cited on this page)
Other direct sites: none

Host context: "'+0x11C' = 1.3f, '+0x374' = 1, the rest zeroed - the weather record's field reset.  Interior anchor '0032B79C' (function '0032B790').  '00379F70' (438 B) is the globals-record initializer '00266D10'/'00379D00' call: '1.0f' defaults flood '02EBF460'..'02EBF50C' while 'movdqu' zero/alternating fills cover '02EBF420'..'02EBF4B0', 'byte' flags clear, and '00861EC0' zeroes the '02ADD8E0' block - the bootstrap's shared-state reset.  Interior "

```
0037D7F0  mov      qword ptr [rsp + 8], rbx
0037D7F5  mov      qword ptr [rsp + 0x10], rbp
0037D7FA  mov      qword ptr [rsp + 0x18], rsi
0037D7FF  mov      qword ptr [rsp + 0x20], rdi
0037D804  push     r14
0037D806  sub      rsp, 0x20
0037D80A  mov      dword ptr [rip + 0x2b41bb0], 1  ; -> 02EBF3C4
0037D814  lea      rdi, [rip + 0x276016d]  ; -> 02ADD988
0037D81B  mov      dword ptr [rip + 0x2b41b9b], 1  ; -> 02EBF3C0
0037D825  lea      r14, [rip + 0x276146c]  ; -> 02ADEC98
0037D82C  xor      ebp, ebp
0037D82E  nop      
0037D830  mov      qword ptr [rdi - 8], rbp
0037D834  lea      rbx, [rdi + 8]
0037D838  mov      qword ptr [rdi], rbp
0037D83B  mov      esi, 4
0037D840  xor      edx, edx
0037D842  mov      r8d, 0xf0
0037D848  mov      rcx, rbx
0037D84B  call     0x861ec0  ; -> 00861EC0 fn
0037D850  mov      dword ptr [rbx + 0xec], 0xffffffff
0037D85A  add      rbx, 0xf0
0037D861  sub      rsi, 1
0037D865  jne      0x37d840  ; -> 0037D840
0037D867  add      rdi, 0x3d0
0037D86E  cmp      rdi, r14
0037D871  jl       0x37d830  ; -> 0037D830
0037D873  mov      rbx, qword ptr [rsp + 0x30]
0037D878  mov      rbp, qword ptr [rsp + 0x38]
0037D87D  mov      rsi, qword ptr [rsp + 0x40]
0037D882  mov      rdi, qword ptr [rsp + 0x48]
0037D887  add      rsp, 0x20
0037D88B  pop      r14
0037D88D  ret      
```

## 003DC6A0 (100 B, extent 003DC6A0-003DC704)

Entered from (direct sites whose caller this page cites): `003DCD00` + 0x15E (call; `003DCD00` is cited on this page); `003DCD00` + 0x1A1 (call; `003DCD00` is cited on this page)
Other direct sites: none

Host context: "finish - the weather record's per-element initializer (pre-named by the batch-121 crossing row).  Interior anchor '0032B63F' (function '0032B600').  '003DC8D0' (303 B) is the keyed insert '003DC5B0'/'003DCD00' call on '02B580B0' (0xC stride to '02B58170'): the '(ecx, dx, r8b)' triple scans for a live slot; a miss claims '02B58174''s index, stores the key + '-1' + '003DCA30''s byte, and a non-negative 'rsp+0x70' index runs '0032E400' int" / "finish - the weather record's per-element initializer (pre-named by the batch-121 crossing row).  Interior anchor '0032B63F' (function '0032B600').  '003DC8D0' (303 B) is the keyed insert '003DC5B0'/'003DCD00' call on '02B580B0' (0xC stride to '02B58170'): the '(ecx, dx, r8b)' triple scans for a live slot; a miss claims '02B58174''s index, stores the key + '-1' + '003DCA30''s byte, and a non-negative 'rsp+0x70' index runs '0032E400' int"

```
003DC6A0  xor      edx, edx
003DC6A2  lea      r9, [rip + 0x277b8c7]  ; -> 02B57F70
003DC6A9  lea      r8d, [rdx + 0x10]
003DC6AD  nop      dword ptr [rax]
003DC6B0  mov      rax, rdx
003DC6B3  and      eax, 0xf
003DC6B6  lea      rax, [rax + rax*4]
003DC6BA  cmp      byte ptr [r9 + rax*4 + 6], 3
003DC6C0  jne      0x3dc6fa  ; -> 003DC6FA
003DC6C2  cmp      word ptr [r9 + rax*4 + 4], 0
003DC6C9  jne      0x3dc6fa  ; -> 003DC6FA
003DC6CB  add      dword ptr [r9 + rax*4 + 8], 0x10
003DC6D1  test     dword ptr [r9 + rax*4 + 8], 0xffff0
003DC6DA  mov      byte ptr [r9 + rax*4 + 6], 4
003DC6E0  mov      dword ptr [rip + 0x277ba86], 1  ; -> 02B58170
003DC6EA  jne      0x3dc6fa  ; -> 003DC6FA
003DC6EC  movzx    ecx, byte ptr [r9 + rax*4 + 0x13]
003DC6F2  or       ecx, 0x10
003DC6F5  mov      dword ptr [r9 + rax*4 + 8], ecx
003DC6FA  inc      rdx
003DC6FD  sub      r8, 1
003DC701  jne      0x3dc6b0  ; -> 003DC6B0
003DC703  ret      
```
