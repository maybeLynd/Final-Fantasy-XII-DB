# Homing pack: `04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md`

Generated 2026-10-03 12:43 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h12-the-record-00329220-builds.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002D76C0 (70 B, extent 002D76C0-002D7706)

Entered from (direct sites whose caller this page cites): `003C6B70` + 0x4BA (call; `003C6B70` is cited on this page); `003C6B70` + 0x6FC (call; `003C6B70` is cited on this page)
Other direct sites: none

Host context: "Per-channel, four channels.   ## SWE2-EC7-39 update (2026-09-19) - '003C3340'  '003C3340' (414 B) is the Presentation builder the page names - '01CEBBA8'/'01F44830'/'02B45A04', '00202B70'/'0031FF70'/'003C6B70'/'00808C40'; builds the record at '[rsp+0x30]' and reads none of it in its own body. Interior anchor '003C3401' (a '00202B70' call).  ## SWE2-EC7-43 update (2026-09-19) - '002C62B0'  '002C62B0' (276 B) is a unit-display-record body" / "Per-channel, four channels.   ## SWE2-EC7-39 update (2026-09-19) - '003C3340'  '003C3340' (414 B) is the Presentation builder the page names - '01CEBBA8'/'01F44830'/'02B45A04', '00202B70'/'0031FF70'/'003C6B70'/'00808C40'; builds the record at '[rsp+0x30]' and reads none of it in its own body. Interior anchor '003C3401' (a '00202B70' call).  ## SWE2-EC7-43 update (2026-09-19) - '002C62B0'  '002C62B0' (276 B) is a unit-display-record body"

```
002D76C0  mov      rax, qword ptr [rip + 0x1dc3569]  ; -> 0209AC30
002D76C7  mov      r8, qword ptr [rax + 0xf0]
002D76CE  test     r8, r8
002D76D1  je       0x2d76fe  ; -> 002D76FE
002D76D3  xor      r9d, r9d
002D76D6  add      r8, 0xd2
002D76DD  nop      dword ptr [rax]
002D76E0  movsx    eax, word ptr [r8 - 2]
002D76E5  cmp      eax, ecx
002D76E7  jne      0x2d76f1  ; -> 002D76F1
002D76E9  movsx    eax, word ptr [r8]
002D76ED  cmp      eax, edx
002D76EF  je       0x2d7702  ; -> 002D7702
002D76F1  inc      r9d
002D76F4  add      r8, 0x18
002D76F8  cmp      r9d, 8
002D76FC  jl       0x2d76e0  ; -> 002D76E0
002D76FE  or       eax, 0xffffffff
002D7701  ret      
002D7702  mov      eax, r9d
002D7705  ret      
```

## 002D7900 (81 B, extent 002D7900-002D7951)

Entered from (direct sites whose caller this page cites): `003C6B70` + 0x722 (call; `003C6B70` is cited on this page)
Other direct sites: none

Host context: "Per-channel, four channels.   ## SWE2-EC7-39 update (2026-09-19) - '003C3340'  '003C3340' (414 B) is the Presentation builder the page names - '01CEBBA8'/'01F44830'/'02B45A04', '00202B70'/'0031FF70'/'003C6B70'/'00808C40'; builds the record at '[rsp+0x30]' and reads none of it in its own body. Interior anchor '003C3401' (a '00202B70' call).  ## SWE2-EC7-43 update (2026-09-19) - '002C62B0'  '002C62B0' (276 B) is a unit-display-record body"

```
002D7900  mov      rax, qword ptr [rip + 0x1dc3329]  ; -> 0209AC30
002D7907  mov      r10, qword ptr [rax + 0xf0]
002D790E  test     r10, r10
002D7911  je       0x2d7950  ; -> 002D7950
002D7913  cmp      ecx, 7
002D7916  ja       0x2d7950  ; -> 002D7950
002D7918  movsxd   rax, ecx
002D791B  add      rax, 8
002D791F  lea      rax, [rax + rax*2]
002D7923  and      dword ptr [r10 + rax*8 + 0x14], 0xffffffef
002D7929  lea      rcx, [r10 + rax*8]
002D792D  movzx    eax, word ptr [rsp + 0x28]
002D7932  mov      word ptr [rcx + 6], ax
002D7936  mov      eax, dword ptr [rsp + 0x30]
002D793A  and      eax, 1
002D793D  mov      word ptr [rcx], dx
002D7940  shl      eax, 4
002D7943  or       dword ptr [rcx + 0x14], eax
002D7946  mov      word ptr [rcx + 2], r8w
002D794B  mov      word ptr [rcx + 4], r9w
002D7950  ret      
```

## 0031FBD0 (51 B, extent 0031FBD0-0031FC03)

Entered from (direct sites whose caller this page cites): `002734F0` + 0x8B (call; `002734F0` is cited on this page)
Other direct sites: none

Host context: "26-09-27, GA-1: earlier called a "link table" and "neighbour table"; the four tables are status order lists, each built with '002D02C0' kind 1-4).  Interior anchor '00273C63' (function '00273BA0').  '002734F0' (230 B) is the unit-record classifier '002BFD20' runs on 'ecx': '0' returns '0xFF'; a '0035BB60'-bounded '0035BB00' scan that finds 'edi' returns '0'; otherwise it resolves the record via '003588B0', requires '00263C20(record) - 1"

```
0031FBD0  sub      rsp, 0x28
0031FBD4  test     rcx, rcx
0031FBD7  je       0x31fbfb  ; -> 0031FBFB
0031FBD9  call     0x263e30  ; -> 00263E30 fn
0031FBDE  test     rax, rax
0031FBE1  je       0x31fbfb  ; -> 0031FBFB
0031FBE3  mov      rax, qword ptr [rax + 0x698]
0031FBEA  test     rax, rax
0031FBED  je       0x31fbfb  ; -> 0031FBFB
0031FBEF  movzx    eax, byte ptr [rax + 0x1c2]
0031FBF6  add      rsp, 0x28
0031FBFA  ret      
0031FBFB  or       eax, 0xffffffff
0031FBFE  add      rsp, 0x28
0031FC02  ret      
```

## 003E4EA0 (162 B, extent 003E4EA0-003E4F42)

Entered from (direct sites whose caller this page cites): `002ED0B0` + 0x61 (jmp; `002ED0B0` is cited on this page)
Other direct sites: none

Host context: "6-09-30, FABLE, [record](../../_index/candidates/sd125-sd128-fable-0930/README.md)) (caller '002C62B0'): '[rcx+0x1D78]' context, '0035D4F0' getter, '00272DE0' ('003588B0'+'002E7E90'), '00263C20' x2, '002ED0B0', '0037C8F0', '0035BAD0' x2, '00273460', then workbench '00202C90' x4/'00203080' — calls '002C7B10'. Interior verified 2026-09-17 (SWE2-FRONTIER): '00272DE0' first at ['002C76C4'](../../_index/ADDRESS-INDEX.md). Its callee '002C7B1"

```
003E4EA0  mov      r10, rcx
003E4EA3  mov      rcx, qword ptr [rcx + 0x400]
003E4EAA  test     rcx, rcx
003E4EAD  jne      0x3e4eb4  ; -> 003E4EB4
003E4EAF  xor      r9d, r9d
003E4EB2  jmp      0x3e4ebd  ; -> 003E4EBD
003E4EB4  movzx    eax, word ptr [rcx + 2]
003E4EB8  add      eax, ecx
003E4EBA  movsxd   r9, eax
003E4EBD  movzx    ecx, byte ptr [r9 + 0x134]
003E4EC5  and      ecx, 7
003E4EC8  sub      ecx, 1
003E4ECB  je       0x3e4f34  ; -> 003E4F34
003E4ECD  mov      dword ptr [rdx], 2
003E4ED3  cmp      ecx, 1
003E4ED6  je       0x3e4ef1  ; -> 003E4EF1
003E4ED8  movss    xmm0, dword ptr [r9 + 0x110]
003E4EE1  maxss    xmm0, dword ptr [r9 + 0x10c]
003E4EEA  movss    dword ptr [r8], xmm0
003E4EEF  jmp      0x3e4f0e  ; -> 003E4F0E
003E4EF1  cmp      dword ptr [r10 + 0x73c], 0
003E4EF9  je       0x3e4f04  ; -> 003E4F04
003E4EFB  mov      dword ptr [r8], 0x3f000000
003E4F02  jmp      0x3e4f0e  ; -> 003E4F0E
003E4F04  mov      eax, dword ptr [r9 + 0x138]
003E4F0B  mov      dword ptr [r8], eax
003E4F0E  movss    xmm0, dword ptr [r10 + 0x260]
003E4F17  mulss    xmm0, dword ptr [r10 + 0x160]
003E4F20  mulss    xmm0, dword ptr [r10 + 0x26c]
003E4F29  mulss    xmm0, dword ptr [r8]
003E4F2E  movss    dword ptr [r8], xmm0
003E4F33  ret      
003E4F34  mov      dword ptr [rdx], 1
003E4F3A  mov      dword ptr [r8], 0
003E4F41  ret      
```
