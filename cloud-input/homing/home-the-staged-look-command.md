# Homing pack: `17-Presentation-Rendering/Character-Render-Records/the-staged-look-command.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-staged-look-command.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00263B90 (37 B, extent 00263B90-00263BB5)

Entered from (direct sites whose caller this page cites): `002E64E0` + 0x65 (call; `002E64E0` is cited on this page)
Other direct sites: none

Host context: "allers are the bind and resume chain of [the two steering slots](../../06-Movement-And-Navigation/Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md) ('002E28E0', '002E3110', '002E64E0', '002EAAA0', '002EBE50'), which is where the 'lookat*' verbs arrive. So **the body turn and the head look are two consumers of one steering record**: the resume switch that page describes ignores shapes 2 and 3, and this function "

```
00263B90  movzx    eax, byte ptr [rcx + 3]
00263B94  and      al, 0xe0
00263B96  cmp      al, 0x60
00263B98  jne      0x263bb2  ; -> 00263BB2
00263B9A  mov      rax, qword ptr [rcx + 0xb8]
00263BA1  movsxd   rdx, edx
00263BA4  add      rax, 0x120
00263BAA  shl      rdx, 7
00263BAE  add      rax, rdx
00263BB1  ret      
00263BB2  xor      eax, eax
00263BB4  ret      
```

## 00263BC0 (28 B, extent 00263BC0-00263BDC)

Entered from (direct sites whose caller this page cites): `002E64E0` + 0x4C (call; `002E64E0` is cited on this page)
Other direct sites: none

Host context: "allers are the bind and resume chain of [the two steering slots](../../06-Movement-And-Navigation/Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md) ('002E28E0', '002E3110', '002E64E0', '002EAAA0', '002EBE50'), which is where the 'lookat*' verbs arrive. So **the body turn and the head look are two consumers of one steering record**: the resume switch that page describes ignores shapes 2 and 3, and this function "

```
00263BC0  movzx    eax, byte ptr [rcx + 3]
00263BC4  and      al, 0xe0
00263BC6  cmp      al, 0x60
00263BC8  jne      0x263bd9  ; -> 00263BD9
00263BCA  mov      rax, qword ptr [rcx + 0xb8]
00263BD1  movsx    eax, byte ptr [rax + 0xdc]
00263BD8  ret      
00263BD9  xor      eax, eax
00263BDB  ret      
```

## 00269E60 (95 B, extent 00269E60-00269EBF)

Entered from (direct sites whose caller this page cites): `002E28E0` + 0x677 (call; `002E28E0` is cited on this page)
Other direct sites: `0034D260` + 0x1F (call)

Host context: "he same way. Two builders stage bits the applier never tests: '003E36A0' (bit 7, floats at '+0x10' / '+0x14') and '003E3570' (bit 8, floats at '+0x18' / '+0x1C'), both called only from the bind path '002E28E0'; their reader, if any, is not this applier.  **The angle setters.** '003E2FD0' stores the two angles at controller '+0x50' / '+0x54' and sets both source kinds to **2**; '003E3200' sets them to **3** and converts: the first angle,"

```
00269E60  movzx    edx, byte ptr [rcx + 3]
00269E64  mov      r8, rcx
00269E67  shr      edx, 5
00269E6A  sub      edx, 1
00269E6D  je       0x269e9f  ; -> 00269E9F
00269E6F  cmp      edx, 2
00269E72  jne      0x269eb7  ; -> 00269EB7
00269E74  mov      rdx, qword ptr [rcx + 0xb8]
00269E7B  xorps    xmm0, xmm0
00269E7E  comiss   xmm0, xmm1
00269E81  movss    dword ptr [rdx + 0xc0], xmm1
00269E89  movss    dword ptr [rdx + 0xc8], xmm1
00269E91  seta     al
00269E94  mov      byte ptr [rdx + 0xdd], al
00269E9A  jmp      0x268380  ; -> 00268380 fn
00269E9F  mov      rcx, qword ptr [rcx + 0xb8]
00269EA6  xorps    xmm0, xmm0
00269EA9  comiss   xmm0, xmm1
00269EAC  movss    dword ptr [rcx + 0x68], xmm1
00269EB1  seta     al
00269EB4  mov      byte ptr [rcx + 0x5c], al
00269EB7  mov      rcx, r8
00269EBA  jmp      0x268380  ; -> 00268380 fn
```

## 0026A370 (43 B, extent 0026A370-0026A39B)

Entered from (direct sites whose caller this page cites): `002E28E0` + 0x6C5 (call; `002E28E0` is cited on this page)
Other direct sites: `0034F280` + 0x6A (jmp)

Host context: "he same way. Two builders stage bits the applier never tests: '003E36A0' (bit 7, floats at '+0x10' / '+0x14') and '003E3570' (bit 8, floats at '+0x18' / '+0x1C'), both called only from the bind path '002E28E0'; their reader, if any, is not this applier.  **The angle setters.** '003E2FD0' stores the two angles at controller '+0x50' / '+0x54' and sets both source kinds to **2**; '003E3200' sets them to **3** and converts: the first angle,"

```
0026A370  movzx    eax, byte ptr [rcx + 3]
0026A374  and      al, 0xe0
0026A376  cmp      al, 0x60
0026A378  jne      0x26a39a  ; -> 0026A39A
0026A37A  mov      rax, qword ptr [rcx + 0xb8]
0026A381  mov      byte ptr [rax + 0x104], dl
0026A387  mov      byte ptr [rax + 0x105], r8b
0026A38E  mov      byte ptr [rax + 0x106], r9b
0026A395  jmp      0x268380  ; -> 00268380 fn
0026A39A  ret      
```
