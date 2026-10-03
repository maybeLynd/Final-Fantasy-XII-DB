# Homing pack: `16-UI/License-Board-View/the-license-board-screen-widgets.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-license-board-screen-widgets.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0027F150 (69 B, extent 0027F150-0027F195)

Entered from (direct sites whose caller this page cites): `002C2320` + 0x895 (call; `002C2320` is cited on this page)
Other direct sites: none

Host context: "hared dialog posts to the widget that opened it:** '{0x11D, a = the code the opener passed, b = the answer}'. Only three bodies store '0x11D' into a message — '002C2899', '002CE103', '002CE417' — in '002C2320', the Yes/No box '002CDF20' and the message box '002CE370'. The message box is opened by '002CE2F0(owner, code)' ('lea' at '002CE33D'), keeps the owner at '+0xC8' and the code at '+0xD0' ('002CE4BB'–'002CE4C5'), picks its text by t"

```
0027F150  mov      rax, qword ptr [rip + 0x1e1bad9]  ; -> 0209AC30
0027F157  xor      ecx, ecx
0027F159  add      rax, 0xd48
0027F15F  mov      r8d, 0xffff
0027F165  mov      r9d, 0x1000
0027F16B  nop      dword ptr [rax + rax]
0027F170  movzx    edx, word ptr [rax]
0027F173  cmp      dx, r8w
0027F177  je       0x27f17f  ; -> 0027F17F
0027F179  cmp      dx, r9w
0027F17D  jne      0x27f192  ; -> 0027F192
0027F17F  inc      rcx
0027F182  add      rax, 0x20
0027F186  cmp      rcx, 5
0027F18A  jl       0x27f170  ; -> 0027F170
0027F18C  mov      eax, 1
0027F191  ret      
0027F192  xor      eax, eax
0027F194  ret      
```

## 003FF160 (129 B, extent 003FF160-003FF1E1)

Entered from (direct sites whose caller this page cites): `002C2320` + 0x35F (call; `002C2320` is cited on this page)
Other direct sites: none

Host context: "hared dialog posts to the widget that opened it:** '{0x11D, a = the code the opener passed, b = the answer}'. Only three bodies store '0x11D' into a message — '002C2899', '002CE103', '002CE417' — in '002C2320', the Yes/No box '002CDF20' and the message box '002CE370'. The message box is opened by '002CE2F0(owner, code)' ('lea' at '002CE33D'), keeps the owner at '+0xC8' and the code at '+0xD0' ('002CE4BB'–'002CE4C5'), picks its text by t"

```
003FF160  sub      rsp, 0x48
003FF164  mov      rax, qword ptr [rip + 0x1b456c5]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003FF16B  xor      rax, rsp
003FF16E  mov      qword ptr [rsp + 0x38], rax
003FF173  movsxd   rax, ecx
003FF176  mov      qword ptr [rsp + 0x28], rax
003FF17B  movsxd   rax, edx
003FF17E  mov      qword ptr [rsp + 0x30], rax
003FF183  mov      rax, qword ptr [rip + 0x1c9baa6]  ; -> 0209AC30
003FF18A  mov      dword ptr [rsp + 0x20], 0
003FF192  cmp      qword ptr [rax + 0x108], 0
003FF19A  jne      0x3ff1cf  ; -> 003FF1CF
003FF19C  lea      r8, [rsp + 0x20]
003FF1A1  mov      ecx, 0x190
003FF1A6  lea      rdx, [rip + 0x1b3]  ; -> 003FF360
003FF1AD  call     0x244f50  ; -> 00244F50 fn
003FF1B2  mov      rcx, qword ptr [rip + 0x1c9ba77]  ; -> 0209AC30
003FF1B9  mov      rdx, rax
003FF1BC  mov      qword ptr [rcx + 0x108], rax
003FF1C3  mov      rcx, qword ptr [rip + 0x1c8f85e]  ; -> 0208EA28
003FF1CA  call     0x246ad0  ; -> 00246AD0 fn
003FF1CF  mov      rcx, qword ptr [rsp + 0x38]
003FF1D4  xor      rcx, rsp
003FF1D7  call     0x808c40  ; -> 00808C40 fn
003FF1DC  add      rsp, 0x48
003FF1E0  ret      
```

## 003FF9F0 (48 B, extent 003FF9F0-003FFA20)

Entered from (direct sites whose caller this page cites): `002C2320` + 0x5E2 (call; `002C2320` is cited on this page)
Other direct sites: none

Host context: "hared dialog posts to the widget that opened it:** '{0x11D, a = the code the opener passed, b = the answer}'. Only three bodies store '0x11D' into a message — '002C2899', '002CE103', '002CE417' — in '002C2320', the Yes/No box '002CDF20' and the message box '002CE370'. The message box is opened by '002CE2F0(owner, code)' ('lea' at '002CE33D'), keeps the owner at '+0xC8' and the code at '+0xD0' ('002CE4BB'–'002CE4C5'), picks its text by t"

```
003FF9F0  mov      rax, qword ptr [rip + 0x1c9b239]  ; -> 0209AC30
003FF9F7  mov      r8, qword ptr [rax + 0x108]
003FF9FE  test     r8, r8
003FFA01  je       0x3ffa1f  ; -> 003FFA1F
003FFA03  mov      dword ptr [r8 + 0x178], ecx
003FFA0A  mov      rax, qword ptr [rip + 0x1c9b21f]  ; -> 0209AC30
003FFA11  mov      rcx, qword ptr [rax + 0x108]
003FFA18  mov      qword ptr [rcx + 0x180], rdx
003FFA1F  ret      
```
