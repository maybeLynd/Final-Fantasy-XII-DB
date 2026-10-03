# Homing pack: `12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md`

Generated 2026-10-02 22:54 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-item-id-encoding-and-equipment-compatibility.json`.

Bodies: 6. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00292F60 (51 B, extent 00292F60-00292F93)

Entered from (direct sites whose caller this page cites): `003FF920` + 0x3A (call; `003FF920` is cited on this page)
Other direct sites: none

Host context: "0' fast-paths - 'byte[[+0x170] + 0xFC] = 2' and '003FDA20(idx, saved)' - else 'word[0209AC30 + idx x 0x20 + 0xD48]' is read, '0xFFFF'/'0x1000' return 1, other values run '003FFA20(idx, 0xFFFF)' then '003FF920(idx, (sword[+0xF2] + sword[+0xF4]) x byte[+0xEC] + sbyte[+0xEE] + sbyte[+0xED])' before 'byte[[+0x170] + 0xFC] = 0x19' - the confirm path that weights the roster slot and marks the widget.  Interior anchor '003FF0FC' (function '003"

```
00292F60  test     ecx, ecx
00292F62  je       0x292f8d  ; -> 00292F8D
00292F64  sub      ecx, 1
00292F67  je       0x292f87  ; -> 00292F87
00292F69  sub      ecx, 1
00292F6C  je       0x292f81  ; -> 00292F81
00292F6E  sub      ecx, 1
00292F71  je       0x292f81  ; -> 00292F81
00292F73  cmp      ecx, 1
00292F76  je       0x292f7b  ; -> 00292F7B
00292F78  xor      eax, eax
00292F7A  ret      
00292F7B  mov      eax, 5
00292F80  ret      
00292F81  mov      eax, 4
00292F86  ret      
00292F87  mov      eax, 3
00292F8C  ret      
00292F8D  mov      eax, 1
00292F92  ret      
```

## 003DFDD0 (104 B, extent 003DFDD0-003DFE38)

Entered from (direct sites whose caller this page cites): `003DFBE0` + 0x2F (call; `003DFBE0` is cited on this page)
Other direct sites: none

Host context: "erior anchor '003FE7E8' (an '003FEAD0' call).  ## SWE2-EC7-53 update (2026-09-19) - '00400CF0'  '00400CF0' (396 B) is an item-record lookup helper the HUD's '003FF360' shares - '0032A8A0'/'003C8060'/'003DFBE0'/'003DFCC0'. Interior anchor '00400D1D' (a '003DFCC0' call).   ## SWE2-EC7-70 update (2026-09-19) - '003FEAD0' nine-row config copy measured  '003FEAD0' (741 B) is the config-block copy '003FE720''s command handler runs: under a st"

```
003DFDD0  mov      qword ptr [rsp + 8], rbx
003DFDD5  push     rdi
003DFDD6  sub      rsp, 0x20
003DFDDA  xor      edi, edi
003DFDDC  lea      eax, [rcx - 1]
003DFDDF  mov      qword ptr [r8], rdi
003DFDE2  mov      rbx, r8
003DFDE5  mov      qword ptr [r8 + 8], rdi
003DFDE9  cmp      eax, 7
003DFDEC  ja       0x3dfe24  ; -> 003DFE24
003DFDEE  lea      r8, [rip - 0x2bfdf5]  ; -> 00120000 (image base)
003DFDF5  cdqe     
003DFDF7  mov      r9d, dword ptr [r8 + rax*4 + 0x2bfe38]  ; image base + 0x2bfe38 = 003DFE38
003DFDFF  add      r9, r8
003DFE02  jmp      r9
003DFE05  call     0x264a40  ; -> 00264A40 fn
003DFE0A  mov      qword ptr [rbx], rax
003DFE0D  test     rax, rax
003DFE10  je       0x3dfe24  ; -> 003DFE24
003DFE12  add      rax, 0x10
003DFE16  mov      qword ptr [rbx + 8], rax
003DFE1A  jmp      0x3dfe24  ; -> 003DFE24
003DFE1C  call     0x264ca0  ; -> 00264CA0 fn
003DFE21  mov      qword ptr [rbx], rax
003DFE24  cmp      qword ptr [rbx], rdi
003DFE27  mov      rbx, qword ptr [rsp + 0x30]
003DFE2C  setne    dil
003DFE30  mov      eax, edi
003DFE32  add      rsp, 0x20
003DFE36  pop      rdi
003DFE37  ret      
```

## 003FE3A0 (69 B, extent 003FE3A0-003FE3E5)

Entered from (direct sites whose caller this page cites): `003FF360` + 0x4F2 (call; `003FF360` is cited on this page); `003FF360` + 0x524 (call; `003FF360` is cited on this page)
Other direct sites: none

Host context: "ise" behaviour.~~ **P-4 ANSWERED 2026-09-12 (FABLE) — all three       read whole.**       **The builder** 'Equipment_BuildRecommendedLoadoutForMappedStats(index, out[5])' (callers       '003FE720' / '003FF360', the equip menu) takes the mapped stats record ('00320AB0(index, 3)'),       copies its five equipment words '+0x50'–'+0x58' into 'out', and for **slots 0–3 only** walks       every id of a per-slot range from the tables at '00D0F" / "ise" behaviour.~~ **P-4 ANSWERED 2026-09-12 (FABLE) — all three       read whole.**       **The builder** 'Equipment_BuildRecommendedLoadoutForMappedStats(index, out[5])' (callers       '003FE720' / '003FF360', the equip menu) takes the mapped stats record ('00320AB0(index, 3)'),       copies its five equipment words '+0x50'–'+0x58' into 'out', and for **slots 0–3 only** walks       every id of a per-slot range from the tables at '00D0F"

```
003FE3A0  sub      rsp, 0x28
003FE3A4  xor      ecx, ecx
003FE3A6  call     0x283270  ; -> 00283270 fn
003FE3AB  call     0x27f210  ; -> 0027F210 fn
003FE3B0  xor      ecx, ecx
003FE3B2  call     0x3fead0  ; -> 003FEAD0 fn
003FE3B7  mov      rax, qword ptr [rip + 0x1c9c872]  ; -> 0209AC30
003FE3BE  mov      rcx, qword ptr [rax + 0x130]
003FE3C5  test     rcx, rcx
003FE3C8  je       0x3fe3d8  ; -> 003FE3D8
003FE3CA  mov      rcx, qword ptr [rcx + 0xc0]
003FE3D1  xor      edx, edx
003FE3D3  call     0x283e40  ; -> 00283E40 fn
003FE3D8  xor      edx, edx
003FE3DA  xor      ecx, ecx
003FE3DC  add      rsp, 0x28
003FE3E0  jmp      0x2858a0  ; -> 002858A0 fn
```

## 003FE6E0 (53 B, extent 003FE6E0-003FE715)

Entered from (direct sites whose caller this page cites): `003FF360` + 0x3A6 (call; `003FF360` is cited on this page)
Other direct sites: none

Host context: "ise" behaviour.~~ **P-4 ANSWERED 2026-09-12 (FABLE) — all three       read whole.**       **The builder** 'Equipment_BuildRecommendedLoadoutForMappedStats(index, out[5])' (callers       '003FE720' / '003FF360', the equip menu) takes the mapped stats record ('00320AB0(index, 3)'),       copies its five equipment words '+0x50'–'+0x58' into 'out', and for **slots 0–3 only** walks       every id of a per-slot range from the tables at '00D0F"

```
003FE6E0  sub      rsp, 0x28
003FE6E4  xor      ecx, ecx
003FE6E6  call     0x3fead0  ; -> 003FEAD0 fn
003FE6EB  mov      rax, qword ptr [rip + 0x1c9c53e]  ; -> 0209AC30
003FE6F2  mov      rcx, qword ptr [rax + 0x130]
003FE6F9  test     rcx, rcx
003FE6FC  je       0x3fe710  ; -> 003FE710
003FE6FE  mov      rcx, qword ptr [rcx + 0xc0]
003FE705  xor      edx, edx
003FE707  add      rsp, 0x28
003FE70B  jmp      0x283e40  ; -> 00283E40 fn
003FE710  add      rsp, 0x28
003FE714  ret      
```

## 003FEDC0 (124 B, extent 003FEDC0-003FEE3C)

Entered from (direct sites whose caller this page cites): `003FDA20` + 0x79 (call; `003FDA20` is cited on this page)
Other direct sites: none

Host context: "506700' - a shared leaf consulted by the render side, not a presentation responsibility of this page.  **CoreRuntimeScheduling and Save/Load — CLIENT (shared-callee edges, SWE2-EC7 batch-161).** The '003FDA20' bracketed-reload entry names '00244DD0'/'002470D0'; '00244DD0' fans into core-runtime helpers '00229DF0'/'00229E70'/'00229EA0' and is also invoked from the save/load layer ('00583040'), while '0032A8A0' sits between '00583D60' and"

```
003FEDC0  sub      rsp, 0x48
003FEDC4  mov      rax, qword ptr [rip + 0x1b45a65]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003FEDCB  xor      rax, rsp
003FEDCE  mov      qword ptr [rsp + 0x38], rax
003FEDD3  mov      rax, qword ptr [rip + 0x1c9be56]  ; -> 0209AC30
003FEDDA  cmp      qword ptr [rax + 0x148], 0
003FEDE2  jne      0x3fee2a  ; -> 003FEE2A
003FEDE4  xor      edx, edx
003FEDE6  movsxd   rax, ecx
003FEDE9  mov      dword ptr [rsp + 0x20], edx
003FEDED  lea      r8, [rsp + 0x20]
003FEDF2  mov      qword ptr [rsp + 0x30], rdx
003FEDF7  mov      ecx, 0xc0
003FEDFC  lea      rdx, [rip + 0x3d]  ; -> 003FEE40
003FEE03  mov      qword ptr [rsp + 0x28], rax
003FEE08  call     0x244f50  ; -> 00244F50 fn
003FEE0D  mov      rcx, qword ptr [rip + 0x1c9be1c]  ; -> 0209AC30
003FEE14  mov      rdx, rax
003FEE17  mov      qword ptr [rcx + 0x148], rax
003FEE1E  mov      rcx, qword ptr [rip + 0x1c8fc03]  ; -> 0208EA28
003FEE25  call     0x246ad0  ; -> 00246AD0 fn
003FEE2A  mov      rcx, qword ptr [rsp + 0x38]
003FEE2F  xor      rcx, rsp
003FEE32  call     0x808c40  ; -> 00808C40 fn
003FEE37  add      rsp, 0x48
003FEE3B  ret      
```

## 003FFA20 (133 B, extent 003FFA20-003FFAA5)

Entered from (direct sites whose caller this page cites): `003FF040` + 0xBC (call; `003FF040` is cited on this page)
Other direct sites: `003FDFE0` + 0x1EB (call)

Host context: " first dword; a bit-2 '+0x168' afterwards tails '002C9EB0(rbx, 0x8000, 0)' - the scroll-cursor row fetch with the two conditional tails. Interior anchor '002C2D4C' (the '0x20'-stride indexed load).  '003FF040' (281 B) is the slot dispatch the equip menu '003FF360' runs: 'word[rcx+0x18A]' saves and zeroes, '00252610' runs twice ('8, 0x48, 5' then '8, 0x20, 0x20'); 'dword[+0x178] == 0x400' fast-paths - 'byte[[+0x170] + 0xFC] = 2' and '003"

```
003FFA20  mov      qword ptr [rsp + 8], rbx
003FFA25  push     rdi
003FFA26  sub      rsp, 0x20
003FFA2A  mov      rax, qword ptr [rip + 0x1c9b1ff]  ; -> 0209AC30
003FFA31  mov      edi, ecx
003FFA33  mov      ebx, edx
003FFA35  movsx    ecx, word ptr [rax + 0xde0]
003FFA3C  call     0x282ea0  ; -> 00282EA0 fn
003FFA41  mov      ecx, eax
003FFA43  mov      r9d, 1
003FFA49  movzx    r8d, bx
003FFA4D  mov      edx, edi
003FFA4F  call     0x31a510  ; -> 0031A510 fn
003FFA54  xor      ecx, ecx
003FFA56  call     0x283270  ; -> 00283270 fn
003FFA5B  call     0x27f210  ; -> 0027F210 fn
003FFA60  xor      ecx, ecx
003FFA62  call     0x3fead0  ; -> 003FEAD0 fn
003FFA67  mov      rax, qword ptr [rip + 0x1c9b1c2]  ; -> 0209AC30
003FFA6E  mov      rcx, qword ptr [rax + 0x130]
003FFA75  test     rcx, rcx
003FFA78  je       0x3ffa88  ; -> 003FFA88
003FFA7A  mov      rcx, qword ptr [rcx + 0xc0]
003FFA81  xor      edx, edx
003FFA83  call     0x283e40  ; -> 00283E40 fn
003FFA88  xor      edx, edx
003FFA8A  xor      ecx, ecx
003FFA8C  call     0x2858a0  ; -> 002858A0 fn
003FFA91  mov      ecx, 1
003FFA96  mov      rbx, qword ptr [rsp + 0x30]
003FFA9B  add      rsp, 0x20
003FFA9F  pop      rdi
003FFAA0  jmp      0x283840  ; -> 00283840 fn
```
