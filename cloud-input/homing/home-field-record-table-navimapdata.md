# Homing pack: `03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-field-record-table-navimapdata.json`.

Bodies: 6. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002B61B0 (97 B, extent 002B61B0-002B6211)

Entered from (direct sites whose caller this page cites): `00251F40` + 0x38 (call; `00251F40` is cited on this page)
Other direct sites: none

Host context: "209AC30' tables use. Interior anchors '002543E9' / '00254399' (the '+1+ecx' byte loads).  ## SWE2-EC7-102 update (2026-09-20) - '0028FF20' measured  '0028FF20' (81 B) is the conditional word-publish '00251F40', '00254AC0', '00255330' and '003C5E50' call on the '[0209BE80 + 0x10F80]' object: when the slot is nonnull '002544B0()' runs; a return of 1 zeroes 'word[+0x1D78]', and 'word[+0x1D7A]' always gains bit 3 - the clear-and-arm sequenc"

```
002B61B0  sub      rsp, 0x28
002B61B4  mov      rcx, qword ptr [rip + 0x1de8405]  ; -> 0209E5C0
002B61BB  test     rcx, rcx
002B61BE  je       0x2b620c  ; -> 002B620C
002B61C0  movzx    eax, word ptr [rcx + 0x179d2]
002B61C7  shr      rax, 2
002B61CB  and      eax, 1
002B61CE  mov      qword ptr [rsp + 0x20], rbx
002B61D3  imul     rbx, rax, 0xbc10
002B61DA  add      rbx, rcx
002B61DD  lea      rcx, [rbx + 0x1b0]
002B61E4  call     0x273a20  ; -> 00273A20 fn
002B61E9  test     eax, eax
002B61EB  je       0x2b6207  ; -> 002B6207
002B61ED  mov      edx, 1
002B61F2  lea      rcx, [rbx + 0x1b0]
002B61F9  mov      rbx, qword ptr [rsp + 0x20]
002B61FE  add      rsp, 0x28
002B6202  jmp      0x247870  ; -> 00247870 fn
002B6207  mov      rbx, qword ptr [rsp + 0x20]
002B620C  add      rsp, 0x28
002B6210  ret      
```

## 0035D550 (9 B, extent 0035D550-0035D559)

Entered from (direct sites whose caller this page cites): `00251F40` + 0x6F (call; `00251F40` is cited on this page)
Other direct sites: none

Host context: "209AC30' tables use. Interior anchors '002543E9' / '00254399' (the '+1+ecx' byte loads).  ## SWE2-EC7-102 update (2026-09-20) - '0028FF20' measured  '0028FF20' (81 B) is the conditional word-publish '00251F40', '00254AC0', '00255330' and '003C5E50' call on the '[0209BE80 + 0x10F80]' object: when the slot is nonnull '002544B0()' runs; a return of 1 zeroes 'word[+0x1D78]', and 'word[+0x1D7A]' always gains bit 3 - the clear-and-arm sequenc"

```
0035D550  xor      edx, edx
0035D552  xor      ecx, ecx
0035D554  jmp      0x290280  ; -> 00290280 fn
```

## 0035D560 (12 B, extent 0035D560-0035D56C)

Entered from (direct sites whose caller this page cites): `00251F40` + 0x68 (call; `00251F40` is cited on this page)
Other direct sites: none

Host context: "209AC30' tables use. Interior anchors '002543E9' / '00254399' (the '+1+ecx' byte loads).  ## SWE2-EC7-102 update (2026-09-20) - '0028FF20' measured  '0028FF20' (81 B) is the conditional word-publish '00251F40', '00254AC0', '00255330' and '003C5E50' call on the '[0209BE80 + 0x10F80]' object: when the slot is nonnull '002544B0()' runs; a return of 1 zeroes 'word[+0x1D78]', and 'word[+0x1D7A]' always gains bit 3 - the clear-and-arm sequenc"

```
0035D560  mov      edx, 1
0035D565  xor      ecx, ecx
0035D567  jmp      0x290280  ; -> 00290280 fn
```

## 003C5E00 (61 B, extent 003C5E00-003C5E3D)

Entered from (direct sites whose caller this page cites): `00251F40` + 0x2E (call; `00251F40` is cited on this page)
Other direct sites: `00352390` + 0xF (jmp); `00352AD0` + 0x12 (jmp)

Host context: "209AC30' tables use. Interior anchors '002543E9' / '00254399' (the '+1+ecx' byte loads).  ## SWE2-EC7-102 update (2026-09-20) - '0028FF20' measured  '0028FF20' (81 B) is the conditional word-publish '00251F40', '00254AC0', '00255330' and '003C5E50' call on the '[0209BE80 + 0x10F80]' object: when the slot is nonnull '002544B0()' runs; a return of 1 zeroes 'word[+0x1D78]', and 'word[+0x1D7A]' always gains bit 3 - the clear-and-arm sequenc"

```
003C5E00  sub      rsp, 0x28
003C5E04  mov      eax, dword ptr [rip + 0x277fbf6]  ; -> 02B45A00
003C5E0A  and      eax, 0xfffffffd
003C5E0D  or       eax, 4
003C5E10  mov      dword ptr [rip + 0x277fbea], eax  ; -> 02B45A00
003C5E16  call     0x254a50  ; -> 00254A50 fn
003C5E1B  test     eax, eax
003C5E1D  jne      0x3c5e38  ; -> 003C5E38
003C5E1F  call     0x377750  ; -> 00377750 fn
003C5E24  test     eax, eax
003C5E26  je       0x3c5e38  ; -> 003C5E38
003C5E28  or       dword ptr [rip + 0x277fbd1], 2  ; -> 02B45A00
003C5E2F  add      rsp, 0x28
003C5E33  jmp      0x3c80c0  ; -> 003C80C0 fn
003C5E38  add      rsp, 0x28
003C5E3C  ret      
```

## 003C9900 (66 B, extent 003C9900-003C9942)

Entered from (direct sites whose caller this page cites): `00251F40` + 0xD1 (call; `00251F40` is cited on this page); `00254AC0` + 0x45 (call; `00254AC0` is cited on this page); `00255330` + 0x41 (call; `00255330` is cited on this page)
Other direct sites: none

Host context: "209AC30' tables use. Interior anchors '002543E9' / '00254399' (the '+1+ecx' byte loads).  ## SWE2-EC7-102 update (2026-09-20) - '0028FF20' measured  '0028FF20' (81 B) is the conditional word-publish '00251F40', '00254AC0', '00255330' and '003C5E50' call on the '[0209BE80 + 0x10F80]' object: when the slot is nonnull '002544B0()' runs; a return of 1 zeroes 'word[+0x1D78]', and 'word[+0x1D7A]' always gains bit 3 - the clear-and-arm sequenc" / "les use. Interior anchors '002543E9' / '00254399' (the '+1+ecx' byte loads).  ## SWE2-EC7-102 update (2026-09-20) - '0028FF20' measured  '0028FF20' (81 B) is the conditional word-publish '00251F40', '00254AC0', '00255330' and '003C5E50' call on the '[0209BE80 + 0x10F80]' object: when the slot is nonnull '002544B0()' runs; a return of 1 zeroes 'word[+0x1D78]', and 'word[+0x1D7A]' always gains bit 3 - the clear-and-arm sequence the navima"

```
003C9900  sub      rsp, 0x28
003C9904  cmp      qword ptr [rip + 0x277de34], 0  ; -> 02B47740
003C990C  je       0x3c993d  ; -> 003C993D
003C990E  call     0x2544b0  ; -> 002544B0 fn
003C9913  mov      rcx, qword ptr [rip + 0x277de26]  ; -> 02B47740
003C991A  xor      edx, edx
003C991C  cmp      eax, 1
003C991F  sete     dl
003C9922  test     rcx, rcx
003C9925  je       0x3c9934  ; -> 003C9934
003C9927  and      dword ptr [rcx + 0x40], 0xfffeffff
003C992E  shl      edx, 0x10
003C9931  or       dword ptr [rcx + 0x40], edx
003C9934  add      rsp, 0x28
003C9938  jmp      0x244dd0  ; -> 00244DD0 fn
003C993D  add      rsp, 0x28
003C9941  ret      
```

## 003C9F80 (70 B, extent 003C9F80-003C9FC6)

Entered from (direct sites whose caller this page cites): `00251F40` + 0x8D (call; `00251F40` is cited on this page)
Other direct sites: none

Host context: "209AC30' tables use. Interior anchors '002543E9' / '00254399' (the '+1+ecx' byte loads).  ## SWE2-EC7-102 update (2026-09-20) - '0028FF20' measured  '0028FF20' (81 B) is the conditional word-publish '00251F40', '00254AC0', '00255330' and '003C5E50' call on the '[0209BE80 + 0x10F80]' object: when the slot is nonnull '002544B0()' runs; a return of 1 zeroes 'word[+0x1D78]', and 'word[+0x1D7A]' always gains bit 3 - the clear-and-arm sequenc"

```
003C9F80  sub      rsp, 0x28
003C9F84  cmp      qword ptr [rip + 0x277d7b4], 0  ; -> 02B47740
003C9F8C  je       0x3c9fbd  ; -> 003C9FBD
003C9F8E  call     0x2544b0  ; -> 002544B0 fn
003C9F93  mov      rcx, qword ptr [rip + 0x277d7a6]  ; -> 02B47740
003C9F9A  xor      edx, edx
003C9F9C  cmp      eax, 1
003C9F9F  sete     dl
003C9FA2  test     rcx, rcx
003C9FA5  je       0x3c9fb4  ; -> 003C9FB4
003C9FA7  and      dword ptr [rcx + 0x40], 0xffff7fff
003C9FAE  shl      edx, 0xf
003C9FB1  or       dword ptr [rcx + 0x40], edx
003C9FB4  add      rsp, 0x28
003C9FB8  jmp      0x246ac0  ; -> 00246AC0 fn
003C9FBD  add      rsp, 0x28
003C9FC1  jmp      0x3c99d0  ; -> 003C99D0 fn
```
