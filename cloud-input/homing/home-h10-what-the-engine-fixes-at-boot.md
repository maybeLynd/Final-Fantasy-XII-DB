# Homing pack: `00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-what-the-engine-fixes-at-boot.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0028F6A0 (80 B, extent 0028F6A0-0028F6F0)

Entered from (direct sites whose caller this page cites): `0022A770` + 0x2E0 (call; `0022A770` is cited on this page)
Other direct sites: `002E2340` + 0x4 (call)

Host context: "to the CRT 'malloc' thunk | | '00369D30' | the arena initializer | 707 B | '(id, block, size, slotCount)' | | '0022A4F0' | the button-mask applier | 66 B | the only other writer of the two masks | | '0022A770' | the field frame | 2,001 B | the one reader of '02064ACC' ('0022AE8F') | | '0035EB70' | the tick pacer | 258 B | waits 'max(n, 1)' ticks | | '00229F10' | frame-base setter | 7 B | 'mov [02064ACC], ecx; ret' |  ### Data addresses "

```
0028F6A0  sub      rsp, 0x28
0028F6A4  mov      rcx, qword ptr [rip + 0x1e0c7d5]  ; -> 0209BE80
0028F6AB  test     rcx, rcx
0028F6AE  jne      0x28f6b7  ; -> 0028F6B7
0028F6B0  xor      eax, eax
0028F6B2  add      rsp, 0x28
0028F6B6  ret      
0028F6B7  test     dword ptr [rcx + 0x10f68], 0x2000
0028F6C1  jne      0x28f6b0  ; -> 0028F6B0
0028F6C3  add      rcx, 0xab30
0028F6CA  call     0x273a20  ; -> 00273A20 fn
0028F6CF  test     eax, eax
0028F6D1  je       0x28f6b0  ; -> 0028F6B0
0028F6D3  mov      rax, qword ptr [rip + 0x1e0c7a6]  ; -> 0209BE80
0028F6DA  movzx    ecx, byte ptr [rax + 0x10f68]
0028F6E1  and      cl, 0x10
0028F6E4  neg      cl
0028F6E6  sbb      eax, eax
0028F6E8  add      eax, 2
0028F6EB  add      rsp, 0x28
0028F6EF  ret      
```

## 0036B060 (29 B, extent 0036B060-0036B07D)

Entered from (direct sites whose caller this page cites): `0037B3D0` + 0xB (call; `0037B3D0` is cited on this page)
Other direct sites: none

Host context: "   '00369D30' has five callers in the edge list (calls and tail jumps), and the id each passes is read at the call:   boot '0022A0B0' passes 2–9 and '0xB' (the positive control, matching 'EXP-142'), '0037B3D0' re-registers '0xB' (the   arena-11 regrowth), '003E9AA0' passes '0xC', '0025A990' '0xD' and '0025AA30' '0xE' — the nested arenas. No   rip-relative operand and no absolute qword in the file points at '00369D30', so no pointer rout"

```
0036B060  cmp      ecx, 0xe
0036B063  ja       0x36b07a  ; -> 0036B07A
0036B065  movsxd   rax, ecx
0036B068  lea      rcx, [rip + 0x1f6cf61]  ; -> 022D7FD0
0036B06F  imul     rax, rax, 0xa8
0036B076  add      rax, rcx
0036B079  ret      
0036B07A  xor      eax, eax
0036B07C  ret      
```

## 003AA1F0 (77 B, extent 003AA1F0-003AA23D)

Entered from (direct sites whose caller this page cites): `00501750` + 0x93 (call; `00501750` is cited on this page)
Other direct sites: none

Host context: " under '00259DF0'/'00379E90') — boot primes the resource pipeline as well as the heap. And upstream, '0036A100' — one of the alloc triple primed here — is later called from 25 Presentation builders ('00501750', '00503CD0', '003EDAD0'…), so the boot-primed allocator serves the render path at run time, not only startup.  The other directions are smaller but real: '007980A0' calls **platform**/online init ('007A0C60', '008655E0', '0020CD80"

```
003AA1F0  mov      qword ptr [rsp + 8], rbx
003AA1F5  push     rdi
003AA1F6  sub      rsp, 0x20
003AA1FA  mov      rax, qword ptr [rip + 0x2b14d6f]  ; -> 02EBEF70
003AA201  mov      ebx, edx
003AA203  mov      edi, ecx
003AA205  mov      rax, qword ptr [rax]
003AA208  test     rax, rax
003AA20B  je       0x3aa230  ; -> 003AA230
003AA20D  nop      dword ptr [rax]
003AA210  movsx    r8d, word ptr [rax + 0xc]
003AA215  cmp      r8d, edi
003AA218  jne      0x3aa224  ; -> 003AA224
003AA21A  movsx    r8d, byte ptr [rax + 0xe]
003AA21F  cmp      r8d, ebx
003AA222  je       0x3aa232  ; -> 003AA232
003AA224  mov      ecx, dword ptr [rax]
003AA226  call     0x20e600  ; -> 0020E600 fn
003AA22B  test     rax, rax
003AA22E  jne      0x3aa210  ; -> 003AA210
003AA230  xor      eax, eax
003AA232  mov      rbx, qword ptr [rsp + 0x30]
003AA237  add      rsp, 0x20
003AA23B  pop      rdi
003AA23C  ret      
```

## 008632E0 (106 B, extent 008632E0-0086334A)

Entered from (direct sites whose caller this page cites): `00863540` + 0x28 (call; `00863540` is cited on this page)
Other direct sites: none

Host context: "'008631D0' pair + '002F0280') | the in-scope *callers* of the excluded VU1 install band — the boot sequence's DMA/program upload arms | | '00368xxx' init family | '0035E820' (382 B — '005C5230' ×3 + '00863540'/'008636E0'/'00863610', '022CA62C'/'30'/'022CAE40', tables '0035EA40'/'0035EC90'/'00D10C78'), '00368C80', '00368DD0', '00368ED0', '00368F70', '00369070', '003692C0' | a '00863540'/'008636E0'/'00863610' + '00D10Cxx' table shape over"

```
008632E0  mov      qword ptr [rsp + 0x10], rbx
008632E5  mov      qword ptr [rsp + 0x18], rbp
008632EA  mov      qword ptr [rsp + 0x20], rsi
008632EF  push     rdi
008632F0  sub      rsp, 0x20
008632F4  mov      rbx, rcx
008632F7  mov      esi, r8d
008632FA  mov      ecx, 8
008632FF  mov      ebp, edx
00863301  call     0x210ec0  ; -> 00210EC0 fn
00863306  mov      qword ptr [rsp + 0x30], rax
0086330B  mov      rdi, rax
0086330E  test     rax, rax
00863311  je       0x86332b  ; -> 0086332B
00863313  xor      r9d, r9d
00863316  mov      r8d, esi
00863319  mov      edx, ebp
0086331B  xor      ecx, ecx
0086331D  call     qword ptr [rip + 0x5eddd]  ; -> 008C2100 [u64 0x0000000001CCC184]
00863323  mov      qword ptr [rdi], rax
00863326  mov      qword ptr [rbx], rdi
00863329  jmp      0x863332  ; -> 00863332
0086332B  mov      qword ptr [rbx], 0
00863332  mov      rbp, qword ptr [rsp + 0x40]
00863337  mov      rax, rbx
0086333A  mov      rbx, qword ptr [rsp + 0x38]
0086333F  mov      rsi, qword ptr [rsp + 0x48]
00863344  add      rsp, 0x20
00863348  pop      rdi
00863349  ret      
```
