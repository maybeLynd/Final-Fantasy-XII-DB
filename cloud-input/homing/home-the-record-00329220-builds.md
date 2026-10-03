# Homing pack: `04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-record-00329220-builds.json`.

Bodies: 7. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002C03A0 (91 B, extent 002C03A0-002C03FB)

Entered from (direct sites whose caller this page cites): `002BFD20` + 0xA3 (call; `002BFD20` is cited on this page); `002BFD20` + 0xFF (call; `002BFD20` is cited on this page)
Other direct sites: none

Host context: "ers of the wrappers are UI, Input and Presentation code: 'InputGameplay_ArbitrateDigitalInputAndModalState' ('00253C70'), '00254560', '00272E10', '00272E70', '00273270', '00273880' (UI), '00283270', '002BFD20' (UI), '0035BC50' (UI), '003C3340' (Presentation).  ### 2.2 In execution order  | step | site | what | |---|---|---| | clear | '0032923A'–'00329261' | 'memset(out, 0, 0xC0)'; '+0x88 = 0'; '+0x00 = 0'; '+0x60 = 0xFFFF'; '+0x10 = 0';" / "ers of the wrappers are UI, Input and Presentation code: 'InputGameplay_ArbitrateDigitalInputAndModalState' ('00253C70'), '00254560', '00272E10', '00272E70', '00273270', '00273880' (UI), '00283270', '002BFD20' (UI), '0035BC50' (UI), '003C3340' (Presentation).  ### 2.2 In execution order  | step | site | what | |---|---|---| | clear | '0032923A'–'00329261' | 'memset(out, 0, 0xC0)'; '+0x88 = 0'; '+0x00 = 0'; '+0x60 = 0xFFFF'; '+0x10 = 0';"

```
002C03A0  mov      qword ptr [rsp + 8], rbx
002C03A5  mov      qword ptr [rsp + 0x18], rsi
002C03AA  push     rdi
002C03AB  sub      rsp, 0x20
002C03AF  mov      rdi, rcx
002C03B2  mov      dword ptr [rsp + 0x38], 0xc
002C03BA  xor      esi, esi
002C03BC  lea      rbx, [rsp + 0x38]
002C03C1  test     rdi, rdi
002C03C4  jne      0x2c03ca  ; -> 002C03CA
002C03C6  xor      ecx, ecx
002C03C8  jmp      0x2c03d5  ; -> 002C03D5
002C03CA  movsxd   rcx, dword ptr [rbx]
002C03CD  mov      rax, qword ptr [rdi + 0x60]
002C03D1  mov      rcx, qword ptr [rax + rcx*8]
002C03D5  mov      rcx, qword ptr [rcx + 0x18]
002C03D9  xor      edx, edx
002C03DB  call     0x247870  ; -> 00247870 fn
002C03E0  inc      esi
002C03E2  add      rbx, 4
002C03E6  cmp      esi, 1
002C03E9  jb       0x2c03c1  ; -> 002C03C1
002C03EB  mov      rbx, qword ptr [rsp + 0x30]
002C03F0  mov      rsi, qword ptr [rsp + 0x40]
002C03F5  add      rsp, 0x20
002C03F9  pop      rdi
002C03FA  ret      
```

## 002C8A20 (56 B, extent 002C8A20-002C8A58)

Entered from (direct sites whose caller this page cites): `002C6F70` + 0x15D (call; `002C6F70` is cited on this page)
Other direct sites: none

Host context: "and focus fields read the party layer. '+0x04' comes from 'PartyRoster_GetActorBySlot' '00263750', and the focus unit comes from '003590D0'. The builder calls both, and the UI evaluators '002C62B0', '002C6F70' and '002C7660' read '003590D0' too. '0035BC50' reads 'PartyFocus_GetPreferredDefinitionSelector' '003271D0' and the focus thunk '003272E0'. Six party bodies read '003590D0', among them 'PartyRoster_GetActorBySlotOrCurrentFocus' '0"

```
002C8A20  mov      r8, rcx
002C8A23  test     rcx, rcx
002C8A26  jne      0x2c8a2c  ; -> 002C8A2C
002C8A28  mov      rax, rdx
002C8A2B  ret      
002C8A2C  mov      rax, qword ptr [rcx + 0x18]
002C8A30  test     rax, rax
002C8A33  je       0x2c8a4c  ; -> 002C8A4C
002C8A35  nop      word ptr [rax + rax]
002C8A40  mov      rcx, rax
002C8A43  mov      rax, qword ptr [rax + 0x18]
002C8A47  test     rax, rax
002C8A4A  jne      0x2c8a40  ; -> 002C8A40
002C8A4C  mov      qword ptr [rcx + 0x18], rdx
002C8A50  mov      rax, r8
002C8A53  mov      qword ptr [rdx + 0x20], rcx
002C8A57  ret      
```

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

## 003F2600 (234 B, extent 003F2600-003F26EA)

Entered from (direct sites whose caller this page cites): `002915C0` + 0x13F (call; `002915C0` is cited on this page)
Other direct sites: none

Host context: "** '00181350' calls '001B06D0' and is called by '0022FFE0'/'00274CB0'/'003C7xxx' of that layer — a two-way render-helper exchange, not a second owner. **Resource — SERVICE (SWE2-EC7-156, 2 edges).** '002915C0'/'002917E0' call '0024A5A0' of that layer — the record's helpers consume a resource-side helper, not a shared responsibility. **UI — CLIENT (SWE2-EC7-156, 242 edges).** '002A0440' calls '00181560', '002915C0'/'002917E0'/'002C7660' "

```
003F2600  mov      qword ptr [rsp + 8], rbx
003F2605  push     rdi
003F2606  sub      rsp, 0x20
003F260A  mov      r9d, 0x20
003F2610  mov      rbx, rdx
003F2613  lea      rdx, [rcx + 0x3c0]
003F261A  mov      rdi, rcx
003F261D  lea      r8d, [r9 - 0x1a]
003F2621  call     0x3f2a70  ; -> 003F2A70 fn
003F2626  lea      rcx, [rdi + 0x780]
003F262D  mov      dword ptr [rdi + 0x998], 0x3f800000
003F2637  mov      rdx, rbx
003F263A  call     0x3f2f20  ; -> 003F2F20 fn
003F263F  lea      rcx, [rdi + 0x870]
003F2646  mov      rdx, rbx
003F2649  call     0x3f2f20  ; -> 003F2F20 fn
003F264E  mov      eax, dword ptr [rbx]
003F2650  mov      dword ptr [rdi + 0x970], eax
003F2656  movss    xmm0, dword ptr [rbx + 4]
003F265B  movaps   xmm1, xmm0
003F265E  mulss    xmm1, dword ptr [rip + 0x18f950a]  ; -> 01CEBB70 [f32 0.5]
003F2666  divss    xmm0, dword ptr [rip + 0x505b12]  ; -> 008F8180 [f32 10]
003F266E  subss    xmm1, xmm0
003F2672  movss    dword ptr [rdi + 0x974], xmm1
003F267A  mov      eax, dword ptr [rbx + 8]
003F267D  mov      dword ptr [rdi + 0x978], eax
003F2683  movss    xmm0, dword ptr [rbx + 4]
003F2688  movaps   xmm1, xmm0
003F268B  mulss    xmm1, dword ptr [rip + 0x18f94dd]  ; -> 01CEBB70 [f32 0.5]
003F2693  divss    xmm0, dword ptr [rip + 0x505ae5]  ; -> 008F8180 [f32 10]
003F269B  addss    xmm1, dword ptr [rbx + 0xc]
003F26A0  mov      rbx, qword ptr [rsp + 0x30]
003F26A5  mov      dword ptr [rdi + 0x924], 0x3e570a3d
003F26AF  mov      dword ptr [rdi + 0x92c], 0x3e4ccccd
003F26B9  mov      dword ptr [rdi + 0x930], 0x42fe0000
003F26C3  addss    xmm1, xmm0
003F26C7  mov      dword ptr [rdi + 0x934], 0x42fe0000
003F26D1  mov      qword ptr [rdi + 0x938], 0x42fe0000
003F26DC  movss    dword ptr [rdi + 0x97c], xmm1
003F26E4  add      rsp, 0x20
003F26E8  pop      rdi
003F26E9  ret      
```
