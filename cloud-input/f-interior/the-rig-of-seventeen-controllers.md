# F-interior pack: `17-Presentation-Rendering/Character-Render-Records/the-rig-of-seventeen-controllers.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-rig-of-seventeen-controllers.json`.

Functions: 17. Each is cited on the page only at its entry and is still in the F frontier.

## 002E8570 (110 B, extent 002E8570-002E85DE)

Page context: "y-state pass carries it over:  | record '+0x304' | dirty bit in '+0x290' | controller | set by | |---|---|---:|---| | bit 6 | bit 13 | 9 lip flap | 'setkutipakustatus': handler '00352370' -> service '002E8570' (110 B); timed: '00352B90' -> '002E85E0' -> '002EDF30' (89 B) | | bit 7 | bit 14 | 13 nod | 'setunazukistatus': '003528A0' -> '002E8B60' -> '002EE0D0' (91 B); timed: '00352F20' -> '002E8B80' -> '002EE130' | | bit 15 | bit 15 | 15 "

```
002E8570  test     rcx, rcx
002E8573  je       0x2e85dd  ; -> 002E85DD
002E8575  mov      rax, qword ptr [rcx + 0xc0]
002E857C  test     rax, rax
002E857F  je       0x2e85dd  ; -> 002E85DD
002E8581  cmp      dword ptr [rax], -1
002E8584  je       0x2e85dd  ; -> 002E85DD
002E8586  movzx    ecx, word ptr [rax]
002E8589  cmp      cx, -1
002E858D  je       0x2e85dd  ; -> 002E85DD
002E858F  movsx    rax, cx
002E8593  imul     rcx, rax, 0x740
002E859A  add      rcx, qword ptr [rip + 0x1fde987]  ; -> 022C6F28
002E85A1  je       0x2e85dd  ; -> 002E85DD
002E85A3  cmp      dword ptr [rcx + 0x284], 0
002E85AA  je       0x2e85dd  ; -> 002E85DD
002E85AC  mov      dword ptr [rcx + 0x640], 0
002E85B6  test     edx, edx
002E85B8  jne      0x2e85cc  ; -> 002E85CC
002E85BA  and      dword ptr [rcx + 0x304], 0xffffffbf
002E85C1  or       dword ptr [rcx + 0x290], 0x2000
002E85CB  ret      
002E85CC  or       dword ptr [rcx + 0x304], 0x40
002E85D3  or       dword ptr [rcx + 0x290], 0x2000
002E85DD  ret      
```

## 002E85E0 (39 B, extent 002E85E0-002E8607)

Page context: "+0x304' | dirty bit in '+0x290' | controller | set by | |---|---|---:|---| | bit 6 | bit 13 | 9 lip flap | 'setkutipakustatus': handler '00352370' -> service '002E8570' (110 B); timed: '00352B90' -> '002E85E0' -> '002EDF30' (89 B) | | bit 7 | bit 14 | 13 nod | 'setunazukistatus': '003528A0' -> '002E8B60' -> '002EE0D0' (91 B); timed: '00352F20' -> '002E8B80' -> '002EE130' | | bit 15 | bit 15 | 15 head shake | 'setkubifuristatus': '0034F4"

```
002E85E0  test     rcx, rcx
002E85E3  je       0x2e8606  ; -> 002E8606
002E85E5  mov      rax, qword ptr [rcx + 0xc0]
002E85EC  test     rax, rax
002E85EF  je       0x2e8606  ; -> 002E8606
002E85F1  cmp      dword ptr [rax], -1
002E85F4  je       0x2e8606  ; -> 002E8606
002E85F6  divss    xmm2, dword ptr [rip + 0x1b15abe]  ; -> 01DFE0BC [f32 1]
002E85FE  movzx    ecx, word ptr [rax]
002E8601  jmp      0x2edf30  ; -> 002EDF30 fn
002E8606  ret      
```

## 002E8B80 (39 B, extent 002E8B80-002E8BA7)

Page context: "service '002E8570' (110 B); timed: '00352B90' -> '002E85E0' -> '002EDF30' (89 B) | | bit 7 | bit 14 | 13 nod | 'setunazukistatus': '003528A0' -> '002E8B60' -> '002EE0D0' (91 B); timed: '00352F20' -> '002E8B80' -> '002EE130' | | bit 15 | bit 15 | 15 head shake | 'setkubifuristatus': '0034F430' -> '002ED300' -> '002EDE70' (91 B); timed: '0034F9B0' -> '002ED320' -> '002EDED0' | | bit 8 | - | 10 eyes | not traced here |  Each setter finds t"

```
002E8B80  test     rcx, rcx
002E8B83  je       0x2e8ba6  ; -> 002E8BA6
002E8B85  mov      rax, qword ptr [rcx + 0xc0]
002E8B8C  test     rax, rax
002E8B8F  je       0x2e8ba6  ; -> 002E8BA6
002E8B91  cmp      dword ptr [rax], -1
002E8B94  je       0x2e8ba6  ; -> 002E8BA6
002E8B96  divss    xmm2, dword ptr [rip + 0x1b1551e]  ; -> 01DFE0BC [f32 1]
002E8B9E  movzx    ecx, word ptr [rax]
002E8BA1  jmp      0x2ee130  ; -> 002EE130 fn
002E8BA6  ret      
```

## 002ED320 (39 B, extent 002ED320-002ED347)

Page context: "60' -> '002EE0D0' (91 B); timed: '00352F20' -> '002E8B80' -> '002EE130' | | bit 15 | bit 15 | 15 head shake | 'setkubifuristatus': '0034F430' -> '002ED300' -> '002EDE70' (91 B); timed: '0034F9B0' -> '002ED320' -> '002EDED0' | | bit 8 | - | 10 eyes | not traced here |  Each setter finds the record from the actor ('+0xC0' -> record index -> the '0x740'-stride array), refuses a free record, sets or clears the flag bit, raises the dirty bit"

```
002ED320  test     rcx, rcx
002ED323  je       0x2ed346  ; -> 002ED346
002ED325  mov      rax, qword ptr [rcx + 0xc0]
002ED32C  test     rax, rax
002ED32F  je       0x2ed346  ; -> 002ED346
002ED331  cmp      dword ptr [rax], -1
002ED334  je       0x2ed346  ; -> 002ED346
002ED336  divss    xmm2, dword ptr [rip + 0x1b10d7e]  ; -> 01DFE0BC [f32 1]
002ED33E  movzx    ecx, word ptr [rax]
002ED341  jmp      0x2eded0  ; -> 002EDED0 fn
002ED346  ret      
```

## 002EDE70 (91 B, extent 002EDE70-002EDECB)

Page context: "setunazukistatus': '003528A0' -> '002E8B60' -> '002EE0D0' (91 B); timed: '00352F20' -> '002E8B80' -> '002EE130' | | bit 15 | bit 15 | 15 head shake | 'setkubifuristatus': '0034F430' -> '002ED300' -> '002EDE70' (91 B); timed: '0034F9B0' -> '002ED320' -> '002EDED0' | | bit 8 | - | 10 eyes | not traced here |  Each setter finds the record from the actor ('+0xC0' -> record index -> the '0x740'-stride array), refuses a free record, sets or c"

```
002EDE70  cmp      cx, -1
002EDE74  je       0x2edeca  ; -> 002EDECA
002EDE76  movsx    rax, cx
002EDE7A  imul     rcx, rax, 0x740
002EDE81  add      rcx, qword ptr [rip + 0x1fd90a0]  ; -> 022C6F28
002EDE88  je       0x2edeca  ; -> 002EDECA
002EDE8A  cmp      dword ptr [rcx + 0x284], 0
002EDE91  je       0x2edeca  ; -> 002EDECA
002EDE93  mov      dword ptr [rcx + 0x648], 0
002EDE9D  test     edx, edx
002EDE9F  jne      0x2edeb6  ; -> 002EDEB6
002EDEA1  and      dword ptr [rcx + 0x304], 0xffff7fff
002EDEAB  or       dword ptr [rcx + 0x290], 0x8000
002EDEB5  ret      
002EDEB6  or       dword ptr [rcx + 0x304], 0x8000
002EDEC0  or       dword ptr [rcx + 0x290], 0x8000
002EDECA  ret      
```

## 002EDED0 (95 B, extent 002EDED0-002EDF2F)

Page context: "D0' (91 B); timed: '00352F20' -> '002E8B80' -> '002EE130' | | bit 15 | bit 15 | 15 head shake | 'setkubifuristatus': '0034F430' -> '002ED300' -> '002EDE70' (91 B); timed: '0034F9B0' -> '002ED320' -> '002EDED0' | | bit 8 | - | 10 eyes | not traced here |  Each setter finds the record from the actor ('+0xC0' -> record index -> the '0x740'-stride array), refuses a free record, sets or clears the flag bit, raises the dirty bit, and stores t"

```
002EDED0  cmp      cx, -1
002EDED4  je       0x2edf2e  ; -> 002EDF2E
002EDED6  movsx    rax, cx
002EDEDA  imul     rcx, rax, 0x740
002EDEE1  add      rcx, qword ptr [rip + 0x1fd9040]  ; -> 022C6F28
002EDEE8  je       0x2edf2e  ; -> 002EDF2E
002EDEEA  cmp      dword ptr [rcx + 0x284], 0
002EDEF1  je       0x2edf2e  ; -> 002EDF2E
002EDEF3  test     edx, edx
002EDEF5  jne      0x2edf12  ; -> 002EDF12
002EDEF7  and      dword ptr [rcx + 0x304], 0xffff7fff
002EDF01  mov      dword ptr [rcx + 0x648], edx
002EDF07  or       dword ptr [rcx + 0x290], 0x8000
002EDF11  ret      
002EDF12  or       dword ptr [rcx + 0x304], 0x8000
002EDF1C  movss    dword ptr [rcx + 0x648], xmm2
002EDF24  or       dword ptr [rcx + 0x290], 0x8000
002EDF2E  ret      
```

## 002EDF30 (89 B, extent 002EDF30-002EDF89)

Page context: "y bit in '+0x290' | controller | set by | |---|---|---:|---| | bit 6 | bit 13 | 9 lip flap | 'setkutipakustatus': handler '00352370' -> service '002E8570' (110 B); timed: '00352B90' -> '002E85E0' -> '002EDF30' (89 B) | | bit 7 | bit 14 | 13 nod | 'setunazukistatus': '003528A0' -> '002E8B60' -> '002EE0D0' (91 B); timed: '00352F20' -> '002E8B80' -> '002EE130' | | bit 15 | bit 15 | 15 head shake | 'setkubifuristatus': '0034F430' -> '002ED3"

```
002EDF30  cmp      cx, -1
002EDF34  je       0x2edf88  ; -> 002EDF88
002EDF36  movsx    rax, cx
002EDF3A  imul     rcx, rax, 0x740
002EDF41  add      rcx, qword ptr [rip + 0x1fd8fe0]  ; -> 022C6F28
002EDF48  je       0x2edf88  ; -> 002EDF88
002EDF4A  cmp      dword ptr [rcx + 0x284], 0
002EDF51  je       0x2edf88  ; -> 002EDF88
002EDF53  test     edx, edx
002EDF55  jne      0x2edf6f  ; -> 002EDF6F
002EDF57  and      dword ptr [rcx + 0x304], 0xffffffbf
002EDF5E  mov      dword ptr [rcx + 0x640], edx
002EDF64  or       dword ptr [rcx + 0x290], 0x2000
002EDF6E  ret      
002EDF6F  or       dword ptr [rcx + 0x304], 0x40
002EDF76  movss    dword ptr [rcx + 0x640], xmm2
002EDF7E  or       dword ptr [rcx + 0x290], 0x2000
002EDF88  ret      
```

## 002EE0D0 (91 B, extent 002EE0D0-002EE12B)

Page context: "tkutipakustatus': handler '00352370' -> service '002E8570' (110 B); timed: '00352B90' -> '002E85E0' -> '002EDF30' (89 B) | | bit 7 | bit 14 | 13 nod | 'setunazukistatus': '003528A0' -> '002E8B60' -> '002EE0D0' (91 B); timed: '00352F20' -> '002E8B80' -> '002EE130' | | bit 15 | bit 15 | 15 head shake | 'setkubifuristatus': '0034F430' -> '002ED300' -> '002EDE70' (91 B); timed: '0034F9B0' -> '002ED320' -> '002EDED0' | | bit 8 | - | 10 eyes "

```
002EE0D0  cmp      cx, -1
002EE0D4  je       0x2ee12a  ; -> 002EE12A
002EE0D6  movsx    rax, cx
002EE0DA  imul     rcx, rax, 0x740
002EE0E1  add      rcx, qword ptr [rip + 0x1fd8e40]  ; -> 022C6F28
002EE0E8  je       0x2ee12a  ; -> 002EE12A
002EE0EA  cmp      dword ptr [rcx + 0x284], 0
002EE0F1  je       0x2ee12a  ; -> 002EE12A
002EE0F3  mov      dword ptr [rcx + 0x644], 0
002EE0FD  test     edx, edx
002EE0FF  jne      0x2ee116  ; -> 002EE116
002EE101  and      dword ptr [rcx + 0x304], 0xffffff7f
002EE10B  or       dword ptr [rcx + 0x290], 0x4000
002EE115  ret      
002EE116  or       dword ptr [rcx + 0x304], 0x80
002EE120  or       dword ptr [rcx + 0x290], 0x4000
002EE12A  ret      
```

## 002EE130 (95 B, extent 002EE130-002EE18F)

Page context: "570' (110 B); timed: '00352B90' -> '002E85E0' -> '002EDF30' (89 B) | | bit 7 | bit 14 | 13 nod | 'setunazukistatus': '003528A0' -> '002E8B60' -> '002EE0D0' (91 B); timed: '00352F20' -> '002E8B80' -> '002EE130' | | bit 15 | bit 15 | 15 head shake | 'setkubifuristatus': '0034F430' -> '002ED300' -> '002EDE70' (91 B); timed: '0034F9B0' -> '002ED320' -> '002EDED0' | | bit 8 | - | 10 eyes | not traced here |  Each setter finds the record from"

```
002EE130  cmp      cx, -1
002EE134  je       0x2ee18e  ; -> 002EE18E
002EE136  movsx    rax, cx
002EE13A  imul     rcx, rax, 0x740
002EE141  add      rcx, qword ptr [rip + 0x1fd8de0]  ; -> 022C6F28
002EE148  je       0x2ee18e  ; -> 002EE18E
002EE14A  cmp      dword ptr [rcx + 0x284], 0
002EE151  je       0x2ee18e  ; -> 002EE18E
002EE153  test     edx, edx
002EE155  jne      0x2ee172  ; -> 002EE172
002EE157  and      dword ptr [rcx + 0x304], 0xffffff7f
002EE161  mov      dword ptr [rcx + 0x644], edx
002EE167  or       dword ptr [rcx + 0x290], 0x4000
002EE171  ret      
002EE172  or       dword ptr [rcx + 0x304], 0x80
002EE17C  movss    dword ptr [rcx + 0x644], xmm2
002EE184  or       dword ptr [rcx + 0x290], 0x4000
002EE18E  ret      
```

## 003E0E70 (132 B, extent 003E0E70-003E0EF4)

Page context: "a long field-copy/resolve pass over the controller record with almost no helper traffic.  Interior anchor '005121BB' (function '005121A0').  '003E0B50' (797 B) is the controller apply '0042BED0' and '003E0E70' call: '0020E600' x17 with '0040ED90' x6 - the rig's resolve-heavy record walker, one of the pair.  Interior anchor '003E0B70' (function '003E0B50').  '003E0F00' (770 B) is the sibling '0042BED0'/'003E1210' call beside '003E0B50': "

```
003E0E70  mov      qword ptr [rsp + 8], rbx
003E0E75  mov      qword ptr [rsp + 0x10], rsi
003E0E7A  push     rdi
003E0E7B  sub      rsp, 0x20
003E0E7F  xor      eax, eax
003E0E81  mov      esi, r8d
003E0E84  mov      edi, edx
003E0E86  mov      rbx, rcx
003E0E89  test     edx, edx
003E0E8B  je       0x3e0eb3  ; -> 003E0EB3
003E0E8D  cmp      edx, 0xb
003E0E90  jne      0x3e0ed7  ; -> 003E0ED7
003E0E92  mov      ecx, dword ptr [rcx + 0x2c]
003E0E95  call     0x20e600  ; -> 0020E600 fn
003E0E9A  test     rax, rax
003E0E9D  je       0x3e0ee4  ; -> 003E0EE4
003E0E9F  mov      ecx, dword ptr [rbx + 0x2c]
003E0EA2  call     0x20e600  ; -> 0020E600 fn
003E0EA7  mov      rcx, rax
003E0EAA  mov      edx, esi
003E0EAC  call     0x519100  ; -> 00519100 fn
003E0EB1  jmp      0x3e0ed0  ; -> 003E0ED0
003E0EB3  mov      ecx, dword ptr [rcx]
003E0EB5  call     0x20e600  ; -> 0020E600 fn
003E0EBA  test     rax, rax
003E0EBD  je       0x3e0ee4  ; -> 003E0EE4
003E0EBF  mov      ecx, dword ptr [rbx]
003E0EC1  call     0x20e600  ; -> 0020E600 fn
003E0EC6  mov      rcx, rax
003E0EC9  mov      edx, esi
003E0ECB  call     0x40db00  ; -> 0040DB00 fn
003E0ED0  cmp      eax, 0xfff
003E0ED5  je       0x3e0ee4  ; -> 003E0EE4
003E0ED7  mov      r8d, eax
003E0EDA  mov      edx, edi
003E0EDC  mov      rcx, rbx
003E0EDF  call     0x3e0b50  ; -> 003E0B50 fn
003E0EE4  mov      rbx, qword ptr [rsp + 0x30]
003E0EE9  mov      rsi, qword ptr [rsp + 0x38]
003E0EEE  add      rsp, 0x20
003E0EF2  pop      rdi
003E0EF3  ret      
```

## 003E1210 (132 B, extent 003E1210-003E1294)

Page context: "70' call: '0020E600' x17 with '0040ED90' x6 - the rig's resolve-heavy record walker, one of the pair.  Interior anchor '003E0B70' (function '003E0B50').  '003E0F00' (770 B) is the sibling '0042BED0'/'003E1210' call beside '003E0B50': identical '0020E600' x17 + '0040ED90' x6 shape - the second resolve-heavy walker of the pair.  Interior anchor '003E0F20' (function '003E0F00').  '00471B60' (733 B) is the rig body '003E00C0' calls: '0020E6"

```
003E1210  mov      qword ptr [rsp + 8], rbx
003E1215  mov      qword ptr [rsp + 0x10], rsi
003E121A  push     rdi
003E121B  sub      rsp, 0x20
003E121F  xor      eax, eax
003E1221  mov      esi, r8d
003E1224  mov      edi, edx
003E1226  mov      rbx, rcx
003E1229  test     edx, edx
003E122B  je       0x3e1253  ; -> 003E1253
003E122D  cmp      edx, 0xb
003E1230  jne      0x3e1277  ; -> 003E1277
003E1232  mov      ecx, dword ptr [rcx + 0x2c]
003E1235  call     0x20e600  ; -> 0020E600 fn
003E123A  test     rax, rax
003E123D  je       0x3e1284  ; -> 003E1284
003E123F  mov      ecx, dword ptr [rbx + 0x2c]
003E1242  call     0x20e600  ; -> 0020E600 fn
003E1247  mov      rcx, rax
003E124A  mov      edx, esi
003E124C  call     0x519100  ; -> 00519100 fn
003E1251  jmp      0x3e1270  ; -> 003E1270
003E1253  mov      ecx, dword ptr [rcx]
003E1255  call     0x20e600  ; -> 0020E600 fn
003E125A  test     rax, rax
003E125D  je       0x3e1284  ; -> 003E1284
003E125F  mov      ecx, dword ptr [rbx]
003E1261  call     0x20e600  ; -> 0020E600 fn
003E1266  mov      rcx, rax
003E1269  mov      edx, esi
003E126B  call     0x40db00  ; -> 0040DB00 fn
003E1270  cmp      eax, 0xfff
003E1275  je       0x3e1284  ; -> 003E1284
003E1277  mov      r8d, eax
003E127A  mov      edx, edi
003E127C  mov      rcx, rbx
003E127F  call     0x3e0f00  ; -> 003E0F00 fn
003E1284  mov      rbx, qword ptr [rsp + 0x30]
003E1289  mov      rsi, qword ptr [rsp + 0x38]
003E128E  add      rsp, 0x20
003E1292  pop      rdi
003E1293  ret      
```

## 003E3400 (57 B, extent 003E3400-003E3439)

Page context: "' call: '0020E600([rbx+8])' resolves, 'esi-1' dispatches three cases - '2' copies 'bpl<<7' into 'byte[+0x1C]' bit 7, '1' runs '[rbx+0x70]' through '0020E600' into the '+0x650' record with '003E3340'/'003E3400'/'00512D80'/'00513150'/'00515600', '3' falls to '0046D560'-side work - the rig's per-kind option write.  Interior anchor '003E2A19' (function '003E29F0').  '005186A0' (371 B) is the state publish '003E00C0' calls: '[rcx + 0x80] == "

```
003E3400  mov      qword ptr [rsp + 8], rbx
003E3405  push     rdi
003E3406  sub      rsp, 0x20
003E340A  mov      rdi, rcx
003E340D  mov      ebx, edx
003E340F  mov      ecx, dword ptr [rcx + 8]
003E3412  call     0x20e600  ; -> 0020E600 fn
003E3417  test     rax, rax
003E341A  je       0x3e342e  ; -> 003E342E
003E341C  mov      ecx, dword ptr [rdi + 8]
003E341F  call     0x20e600  ; -> 0020E600 fn
003E3424  and      bl, 0xf
003E3427  and      byte ptr [rax + 0x1d], 0xf0
003E342B  or       byte ptr [rax + 0x1d], bl
003E342E  mov      rbx, qword ptr [rsp + 0x30]
003E3433  add      rsp, 0x20
003E3437  pop      rdi
003E3438  ret      
```

## 00428F80 (82 B, extent 00428F80-00428FD2)

Page context: "the record's resource entry, takes its rig from '+0x94', and calls the on switch if the flag bit is set and the off switch if it is clear.  **Who runs the countdown (added 2026-09-19; read whole).** '00428F80' (82 B) is a system phase: it walks the **active-record list** - head index at the record system's '+0x48800', next at each record's word '+4', -1 ends it - and calls the countdown below on every record in it. And the rig's neighbo"

```
00428F80  push     rdi
00428F82  sub      rsp, 0x20
00428F86  mov      rax, qword ptr [rip + 0x1e9df9b]  ; -> 022C6F28
00428F8D  mov      rdi, rax
00428F90  mov      ecx, dword ptr [rax + 0x48800]
00428F96  cmp      ecx, -1
00428F99  je       0x428fcc  ; -> 00428FCC
00428F9B  mov      qword ptr [rsp + 0x30], rbx
00428FA0  movsxd   rcx, ecx
00428FA3  mov      rdx, rdi
00428FA6  imul     rbx, rcx, 0x740
00428FAD  lea      rcx, [rbx + rax]
00428FB1  call     0x42ee90  ; -> 0042EE90 fn
00428FB6  mov      rax, qword ptr [rip + 0x1e9df6b]  ; -> 022C6F28
00428FBD  movsx    ecx, word ptr [rbx + rax + 4]
00428FC2  cmp      ecx, -1
00428FC5  jne      0x428fa0  ; -> 00428FA0
00428FC7  mov      rbx, qword ptr [rsp + 0x30]
00428FCC  add      rsp, 0x20
00428FD0  pop      rdi
00428FD1  ret      
```

## 0046D360 (27 B, extent 0046D360-0046D37B)

Page context: "m save) is the large presentation pass the rig callers drive: '0020E600' five times, the '003E' cluster ('003E56A0'/'003E5700'/'003E5B30'x2/'003E5FA0'x2), the '0046' cluster ('0046D0C0'x3/'0046D2A0'/'0046D360'/'0046F460'x2/ '0046FAA0'x2/'0046FAE0'), '0017D2E0' three formats, '00861F14' twice and '004234B0'/'003326C0'/'00513150' once each across ~300 rip-based data refs - a multi-stage per-element build. Interior anchor '0051323A' (the f"

```
0046D360  push     rbx
0046D362  sub      rsp, 0x20
0046D366  mov      rbx, rcx
0046D369  call     0x202b90  ; -> 00202B90 fn
0046D36E  mov      dword ptr [rbx + 0xc], 0x3f800000
0046D375  add      rsp, 0x20
0046D379  pop      rbx
0046D37A  ret      
```

## 00471640 (27 B, extent 00471640-0047165B)

Page context: "'004718D0', 31 B): if off, sets the active byte '+0' and the running byte '+3' and remaps the attack index '+2' through a table so that a bob interrupted while settling rises from where it was. Off ('00471640', 27 B): clears the active byte and remaps '+2' the other way. Update ('004716A0', 290 B): while active, the envelope '+0x10' rises by '0.125 x [01DFE0BC]' a frame to 1.0, the phase '+1' steps round a **sixty-entry cycle** ('01F223"

```
00471640  cmp      byte ptr [rcx], 0
00471643  je       0x47165a  ; -> 0047165A
00471645  movzx    eax, byte ptr [rcx + 2]
00471649  lea      rdx, [rip + 0x1ab1110]  ; -> 01F22760
00471650  mov      byte ptr [rcx], 0
00471653  movzx    eax, byte ptr [rax + rdx]
00471657  mov      byte ptr [rcx + 2], al
0047165A  ret      
```

## 004718D0 (31 B, extent 004718D0-004718EF)

Page context: "and nothing else writes it ([how a position becomes a single number](../Position-To-Scalar/how-a-position-becomes-a-single-number.md), section 12).  **The Float bob (controller 6), read whole.** On ('004718D0', 31 B): if off, sets the active byte '+0' and the running byte '+3' and remaps the attack index '+2' through a table so that a bob interrupted while settling rises from where it was. Off ('00471640', 27 B): clears the active byte "

```
004718D0  cmp      byte ptr [rcx], 0
004718D3  jne      0x4718ee  ; -> 004718EE
004718D5  movzx    eax, byte ptr [rcx + 2]
004718D9  lea      rdx, [rip + 0x1ab0ec0]  ; -> 01F227A0
004718E0  mov      byte ptr [rcx + 3], 1
004718E4  mov      byte ptr [rcx], 1
004718E7  movzx    eax, byte ptr [rax + rdx]
004718EB  mov      byte ptr [rcx + 2], al
004718EE  ret      
```

## 00517610 (52 B, extent 00517610-00517644)

Page context: "-87 update (2026-09-20) - '003E12A0' two-case mode dispatch measured  '003E12A0' (109 B) is the 'edx'-keyed dispatch the rig callers run: '9' resolves '[rbx+0x24]' through '0020E600' and forwards to '00517610(record, r8d)'; '0xD' resolves '[rbx+0x34]' the same way and tails '00471B20(record, r8d)'; every other value returns untouched. Interior anchor '003E12FD' (the '00517610' call).  ## SWE2-EC7-89 update (2026-09-20) - '003B6B60' inde"

```
00517610  and      byte ptr [rcx + 1], 0x3f
00517614  test     edx, edx
00517616  je       0x517623  ; -> 00517623
00517618  test     byte ptr [rcx + 1], 0x30
0051761C  je       0x517643  ; -> 00517643
0051761E  jmp      0x518820  ; -> 00518820 fn
00517623  mov      eax, dword ptr [rcx + 0x10]
00517626  or       byte ptr [rcx + 1], 0x40
0051762A  mov      dword ptr [rcx + 0x88], eax
00517630  mov      eax, dword ptr [rcx + 0x4c]
00517633  mov      dword ptr [rcx + 0x8c], eax
00517639  mov      byte ptr [rcx], 0
0051763C  mov      dword ptr [rcx + 0xc], 0x3f800000
00517643  ret      
```
