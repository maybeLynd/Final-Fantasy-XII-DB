# Homing pack: `08-Combat-Formula/Steal/the-steal-roll.md`

Generated 2026-10-03 00:35 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-steal-roll.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001DD0B0 (92 B, extent 001DD0B0-001DD10C)

Entered from (direct sites whose caller this page cites): `0017FF20` + 0x1A (jmp; `0017FF20` is cited on this page)
Other direct sites: none

Host context: "6F0' call: 'ecx - 1' indexes a '0x16'-entry jump table (byte index at 'r14 + 0x11B6D8' selects a dword offset at 'r14 + 0x11B6C4'); arms clear two '0x100' buffers, resolve names through '0017FDC0' / '0017FF20' and the '0x24'-stride dword table at 'r14 + 0x7F4900' via '002F9860', then format through '002B4090(0x100, rdx, name, ebx)' into the caller's buffer - the text arm the steal roll shares. Out-of-range 'ecx' answers 0. Interior anch"

```
001DD0B0  mov      r8, rcx
001DD0B3  mov      rcx, qword ptr [rip + 0x1da5c66]  ; -> 01F82D20
001DD0BA  mov      eax, dword ptr [rcx + 8]
001DD0BD  cmp      eax, 1
001DD0C0  jne      0x1dd0e1  ; -> 001DD0E1
001DD0C2  mov      eax, dword ptr [r8 + 0x24]
001DD0C6  cmp      eax, dword ptr [r8 + 0x20]
001DD0CA  jae      0x1dd108  ; -> 001DD108
001DD0CC  imul     rdx, rax, 0x1c
001DD0D0  mov      rax, qword ptr [r8 + 0x28]
001DD0D4  mov      ecx, dword ptr [rdx + rax]
001DD0D7  shl      ecx, 0x10
001DD0DA  or       ecx, dword ptr [rdx + rax + 4]
001DD0DE  mov      eax, ecx
001DD0E0  ret      
001DD0E1  test     eax, eax
001DD0E3  jne      0x1dd108  ; -> 001DD108
001DD0E5  mov      eax, dword ptr [r8 + 0x34]
001DD0E9  mov      edx, dword ptr [r8 + 0x38]
001DD0ED  inc      eax
001DD0EF  cmp      edx, eax
001DD0F1  jae      0x1dd108  ; -> 001DD108
001DD0F3  mov      rax, qword ptr [r8 + 0x40]
001DD0F7  imul     rcx, rdx, 0x1c
001DD0FB  mov      edx, dword ptr [rcx + rax]
001DD0FE  mov      eax, dword ptr [rcx + rax + 4]
001DD102  shl      edx, 0x10
001DD105  or       eax, edx
001DD107  ret      
001DD108  mov      eax, dword ptr [rcx + 4]
001DD10B  ret      
```

## 00394380 (123 B, extent 00394380-003943FB)

Entered from (direct sites whose caller this page cites): `003939B0` + 0x3E4 (call; `003939B0` is cited on this page)
Other direct sites: none

Host context: " CLIENT, MECHANICAL (5 edges).** The glyph-run body '001E8580' calls '001A1470', a 93-byte bump allocator (size rounded to 16, cursor advanced, wrapped to the arena base when it would pass the end); '003939B0' calls '001EDE70', a 7-byte getter of the global dword at '01F82E38'; the event poster '0046AB10' calls 'GameClock_GetRawTickCounter' '0032A150'; and the boot frame '0022B6E0' and its sibling init frame '0022B7E0' each call 'RNG_MT"

```
00394380  push     rbx
00394382  sub      rsp, 0x50
00394386  mov      rbx, rcx
00394389  mov      ecx, 1
0039438E  call     0x247780  ; -> 00247780 fn
00394393  xor      eax, eax
00394395  mov      ecx, 0x890
0039439A  mov      qword ptr [rsp + 0x20], rax
0039439F  mov      qword ptr [rsp + 0x28], rax
003943A4  mov      qword ptr [rsp + 0x30], rax
003943A9  mov      qword ptr [rsp + 0x38], rax
003943AE  mov      qword ptr [rsp + 0x40], rax
003943B3  mov      qword ptr [rsp + 0x48], rax
003943B8  call     0x2f9860  ; -> 002F9860 fn
003943BD  xor      ecx, ecx
003943BF  mov      qword ptr [rsp + 0x20], rax
003943C4  mov      rax, qword ptr [rip + 0x1cfa65d]  ; -> 0208EA28
003943CB  lea      rdx, [rsp + 0x20]
003943D0  mov      qword ptr [rsp + 0x30], rax
003943D5  mov      qword ptr [rsp + 0x28], rcx
003943DA  mov      qword ptr [rsp + 0x38], rbx
003943DF  mov      dword ptr [rsp + 0x40], ecx
003943E3  mov      dword ptr [rsp + 0x4c], 0x1002
003943EB  mov      byte ptr [rsp + 0x48], 2
003943F0  call     0x241c90  ; -> 00241C90 fn
003943F5  add      rsp, 0x50
003943F9  pop      rbx
003943FA  ret      
```
