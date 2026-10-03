# F-interior pack: `18-Audio/Sound-Bank-And-Voice-Formats/sead-win-config.md`

Generated 2026-10-02 12:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/sead-win-config.json`.

Functions: 13. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: FABLE.md, SWE2-AUDIT-SPEC.md, SWE2-DATA.md). OPUS read these before packing.

## 0021D990 (100 B, extent 0021D990-0021D9F4)

Page context: "start-up pulls in, none reached from outside this tree. All signature-swept 2026-09-15 ('bshape.py'); the layering is unusually clean:  | layer | members | role | |---|---|---| | record primitives | '0021D990', '0021DA00', '0021DA50', '0021DAD0', '0021DB50', '0021DBE0', '0021DC60', '0021DD40', '0021DDD0', '0021DE80', '0021DEE0', '0021DF70', '0021E020' (13) | call-free 70–251 B bodies keyed on the '009087A8'–'00908808' '.rdata' templates"

```
0021D990  mov      r9, rcx
0021D993  cmp      rdx, rcx
0021D996  je       0x21d9f0  ; -> 0021D9F0
0021D998  sub      rdx, r8
0021D99B  xor      r10d, r10d
0021D99E  nop      
0021D9A0  sub      r8, 0x30
0021D9A4  lea      rax, [rdx + 8]
0021D9A8  add      rax, r8
0021D9AB  lea      rcx, [rdx + r8]
0021D9AF  test     rcx, rcx
0021D9B2  cmove    rax, r10
0021D9B6  mov      rax, qword ptr [rax]
0021D9B9  mov      qword ptr [r8 + 8], rax
0021D9BD  mov      eax, dword ptr [rdx + r8 + 0x10]
0021D9C2  mov      dword ptr [r8 + 0x10], eax
0021D9C6  movzx    eax, byte ptr [rdx + r8 + 0x14]
0021D9CC  mov      byte ptr [r8 + 0x14], al
0021D9D0  mov      eax, dword ptr [rdx + r8 + 0x18]
0021D9D5  mov      dword ptr [r8 + 0x18], eax
0021D9D9  mov      rax, qword ptr [rdx + r8 + 0x20]
0021D9DE  mov      qword ptr [r8 + 0x20], rax
0021D9E2  mov      rax, qword ptr [rdx + r8 + 0x28]
0021D9E7  mov      qword ptr [r8 + 0x28], rax
0021D9EB  cmp      rcx, r9
0021D9EE  jne      0x21d9a0  ; -> 0021D9A0
0021D9F0  mov      rax, r8
0021D9F3  ret      
```

## 0021DA00 (70 B, extent 0021DA00-0021DA46)

Page context: "ls in, none reached from outside this tree. All signature-swept 2026-09-15 ('bshape.py'); the layering is unusually clean:  | layer | members | role | |---|---|---| | record primitives | '0021D990', '0021DA00', '0021DA50', '0021DAD0', '0021DB50', '0021DBE0', '0021DC60', '0021DD40', '0021DDD0', '0021DE80', '0021DEE0', '0021DF70', '0021E020' (13) | call-free 70–251 B bodies keyed on the '009087A8'–'00908808' '.rdata' templates — per-recor"

```
0021DA00  cmp      rdx, rcx
0021DA03  je       0x21da42  ; -> 0021DA42
0021DA05  sub      rdx, r8
0021DA08  nop      dword ptr [rax + rax]
0021DA10  mov      rax, qword ptr [rdx + r8 - 0x20]
0021DA15  sub      r8, 0x28
0021DA19  mov      qword ptr [r8 + 8], rax
0021DA1D  mov      eax, dword ptr [rdx + r8 + 0x10]
0021DA22  mov      dword ptr [r8 + 0x10], eax
0021DA26  mov      rax, qword ptr [rdx + r8 + 0x18]
0021DA2B  mov      qword ptr [r8 + 0x18], rax
0021DA2F  movzx    eax, byte ptr [rdx + r8 + 0x20]
0021DA35  mov      byte ptr [r8 + 0x20], al
0021DA39  lea      rax, [rdx + r8]
0021DA3D  cmp      rax, rcx
0021DA40  jne      0x21da10  ; -> 0021DA10
0021DA42  mov      rax, r8
0021DA45  ret      
```

## 0021DA50 (118 B, extent 0021DA50-0021DAC6)

Page context: "reached from outside this tree. All signature-swept 2026-09-15 ('bshape.py'); the layering is unusually clean:  | layer | members | role | |---|---|---| | record primitives | '0021D990', '0021DA00', '0021DA50', '0021DAD0', '0021DB50', '0021DBE0', '0021DC60', '0021DD40', '0021DDD0', '0021DE80', '0021DEE0', '0021DF70', '0021E020' (13) | call-free 70–251 B bodies keyed on the '009087A8'–'00908808' '.rdata' templates — per-record field ops "

```
0021DA50  cmp      rdx, rcx
0021DA53  je       0x21dac2  ; -> 0021DAC2
0021DA55  lea      r9, [rdx + 0x10]
0021DA59  xor      r10d, r10d
0021DA5C  nop      dword ptr [rax]
0021DA60  sub      r8, 0x30
0021DA64  lea      r9, [r9 - 0x30]
0021DA68  lea      rdx, [r9 - 0x10]
0021DA6C  test     rdx, rdx
0021DA6F  lea      rax, [r9 - 8]
0021DA73  cmove    rax, r10
0021DA77  mov      rax, qword ptr [rax]
0021DA7A  mov      qword ptr [r8 + 8], rax
0021DA7E  mov      eax, dword ptr [r9]
0021DA81  mov      dword ptr [r8 + 0x10], eax
0021DA85  mov      eax, dword ptr [r9 + 4]
0021DA89  mov      dword ptr [r8 + 0x14], eax
0021DA8D  mov      eax, dword ptr [r9 + 8]
0021DA91  mov      dword ptr [r8 + 0x18], eax
0021DA95  mov      eax, dword ptr [r9 + 0xc]
0021DA99  mov      dword ptr [r8 + 0x1c], eax
0021DA9D  mov      eax, dword ptr [r9 + 0x10]
0021DAA1  mov      dword ptr [r8 + 0x20], eax
0021DAA5  mov      eax, dword ptr [r9 + 0x14]
0021DAA9  mov      dword ptr [r8 + 0x24], eax
0021DAAD  mov      eax, dword ptr [r9 + 0x18]
0021DAB1  mov      dword ptr [r8 + 0x28], eax
0021DAB5  mov      eax, dword ptr [r9 + 0x1c]
0021DAB9  mov      dword ptr [r8 + 0x2c], eax
0021DABD  cmp      rdx, rcx
0021DAC0  jne      0x21da60  ; -> 0021DA60
0021DAC2  mov      rax, r8
0021DAC5  ret      
```

## 0021DAD0 (123 B, extent 0021DAD0-0021DB4B)

Page context: " outside this tree. All signature-swept 2026-09-15 ('bshape.py'); the layering is unusually clean:  | layer | members | role | |---|---|---| | record primitives | '0021D990', '0021DA00', '0021DA50', '0021DAD0', '0021DB50', '0021DBE0', '0021DC60', '0021DD40', '0021DDD0', '0021DE80', '0021DEE0', '0021DF70', '0021E020' (13) | call-free 70–251 B bodies keyed on the '009087A8'–'00908808' '.rdata' templates — per-record field ops | | '001EDF0"

```
0021DAD0  cmp      rcx, rdx
0021DAD3  je       0x21db47  ; -> 0021DB47
0021DAD5  lea      r9, [rcx + 0x10]
0021DAD9  xor      r10d, r10d
0021DADC  nop      dword ptr [rax]
0021DAE0  lea      rax, [r9 - 0x10]
0021DAE4  test     rax, rax
0021DAE7  lea      rcx, [r9 - 8]
0021DAEB  lea      r9, [r9 + 0x30]
0021DAEF  cmove    rcx, r10
0021DAF3  mov      rax, qword ptr [rcx]
0021DAF6  mov      qword ptr [r8 + 8], rax
0021DAFA  mov      eax, dword ptr [r9 - 0x30]
0021DAFE  mov      dword ptr [r8 + 0x10], eax
0021DB02  mov      eax, dword ptr [r9 - 0x2c]
0021DB06  mov      dword ptr [r8 + 0x14], eax
0021DB0A  mov      eax, dword ptr [r9 - 0x28]
0021DB0E  mov      dword ptr [r8 + 0x18], eax
0021DB12  mov      eax, dword ptr [r9 - 0x24]
0021DB16  mov      dword ptr [r8 + 0x1c], eax
0021DB1A  mov      eax, dword ptr [r9 - 0x20]
0021DB1E  mov      dword ptr [r8 + 0x20], eax
0021DB22  mov      eax, dword ptr [r9 - 0x1c]
0021DB26  mov      dword ptr [r8 + 0x24], eax
0021DB2A  mov      eax, dword ptr [r9 - 0x18]
0021DB2E  mov      dword ptr [r8 + 0x28], eax
0021DB32  mov      eax, dword ptr [r9 - 0x14]
0021DB36  mov      dword ptr [r8 + 0x2c], eax
0021DB3A  lea      rax, [r9 - 0x10]
0021DB3E  add      r8, 0x30
0021DB42  cmp      rax, rdx
0021DB45  jne      0x21dae0  ; -> 0021DAE0
0021DB47  mov      rax, r8
0021DB4A  ret      
```

## 0021DBE0 (127 B, extent 0021DBE0-0021DC5F)

Page context: "signature-swept 2026-09-15 ('bshape.py'); the layering is unusually clean:  | layer | members | role | |---|---|---| | record primitives | '0021D990', '0021DA00', '0021DA50', '0021DAD0', '0021DB50', '0021DBE0', '0021DC60', '0021DD40', '0021DDD0', '0021DE80', '0021DEE0', '0021DF70', '0021E020' (13) | call-free 70–251 B bodies keyed on the '009087A8'–'00908808' '.rdata' templates — per-record field ops | | '001EDF00' apply arms | '0021E09"

```
0021DBE0  mov      r11, rdx
0021DBE3  mov      r10, rcx
0021DBE6  cmp      rcx, rdx
0021DBE9  je       0x21dc5b  ; -> 0021DC5B
0021DBEB  lea      r9, [rcx + 0x210]
0021DBF2  sub      r10, r8
0021DBF5  nop      word ptr [rax + rax]
0021DC00  mov      rax, qword ptr [r9 - 0x208]
0021DC07  mov      edx, 0x100
0021DC0C  mov      qword ptr [r8 + 8], rax
0021DC10  lea      rax, [r8 + 0x10]
0021DC14  nop      dword ptr [rax]
0021DC18  nop      dword ptr [rax + rax]
0021DC20  movzx    ecx, byte ptr [r10 + rax]
0021DC25  mov      byte ptr [rax], cl
0021DC27  movzx    ecx, byte ptr [r10 + rax + 1]
0021DC2D  mov      byte ptr [rax + 1], cl
0021DC30  lea      rax, [rax + 2]
0021DC34  sub      rdx, 1
0021DC38  jne      0x21dc20  ; -> 0021DC20
0021DC3A  mov      rax, qword ptr [r9]
0021DC3D  add      r9, 0x218
0021DC44  mov      qword ptr [r8 + 0x210], rax
0021DC4B  add      r8, 0x218
0021DC52  lea      rax, [r10 + r8]
0021DC56  cmp      rax, r11
0021DC59  jne      0x21dc00  ; -> 0021DC00
0021DC5B  mov      rax, r8
0021DC5E  ret      
```

## 0021DE80 (84 B, extent 0021DE80-0021DED4)

Page context: "yering is unusually clean:  | layer | members | role | |---|---|---| | record primitives | '0021D990', '0021DA00', '0021DA50', '0021DAD0', '0021DB50', '0021DBE0', '0021DC60', '0021DD40', '0021DDD0', '0021DE80', '0021DEE0', '0021DF70', '0021E020' (13) | call-free 70–251 B bodies keyed on the '009087A8'–'00908808' '.rdata' templates — per-record field ops | | '001EDF00' apply arms | '0021E090', '0021E190', '0021E280', '0021E370', '0021E47"

```
0021DE80  cmp      rcx, rdx
0021DE83  je       0x21ded0  ; -> 0021DED0
0021DE85  mov      r9, r8
0021DE88  lea      rax, [rcx + 0x10]
0021DE8C  sub      r9, rcx
0021DE8F  lea      r10, [rip + 0x6ea972]  ; -> 00908808
0021DE96  test     r8, r8
0021DE99  je       0x21debf  ; -> 0021DEBF
0021DE9B  mov      qword ptr [r8], r10
0021DE9E  mov      rcx, qword ptr [rax - 8]
0021DEA2  mov      qword ptr [r9 + rax - 8], rcx
0021DEA7  mov      ecx, dword ptr [rax]
0021DEA9  mov      dword ptr [r9 + rax], ecx
0021DEAD  mov      rcx, qword ptr [rax + 8]
0021DEB1  mov      qword ptr [r9 + rax + 8], rcx
0021DEB6  movzx    ecx, byte ptr [rax + 0x10]
0021DEBA  mov      byte ptr [r9 + rax + 0x10], cl
0021DEBF  add      rax, 0x28
0021DEC3  add      r8, 0x28
0021DEC7  lea      rcx, [rax - 0x10]
0021DECB  cmp      rcx, rdx
0021DECE  jne      0x21de96  ; -> 0021DE96
0021DED0  mov      rax, r8
0021DED3  ret      
```

## 0021E020 (98 B, extent 0021E020-0021E082)

Page context: "| members | role | |---|---|---| | record primitives | '0021D990', '0021DA00', '0021DA50', '0021DAD0', '0021DB50', '0021DBE0', '0021DC60', '0021DD40', '0021DDD0', '0021DE80', '0021DEE0', '0021DF70', '0021E020' (13) | call-free 70–251 B bodies keyed on the '009087A8'–'00908808' '.rdata' templates — per-record field ops | | '001EDF00' apply arms | '0021E090', '0021E190', '0021E280', '0021E370', '0021E470' (5) | 234–251 B each, '001EDF00' "

```
0021E020  mov      r9, r8
0021E023  test     edx, edx
0021E025  je       0x21e081  ; -> 0021E081
0021E027  lea      rax, [rcx + 0x10]
0021E02B  xor      r10d, r10d
0021E02E  lea      r11, [rip + 0x6ea773]  ; -> 009087A8
0021E035  lea      r8, [rax - 0x10]
0021E039  test     r8, r8
0021E03C  je       0x21e078  ; -> 0021E078
0021E03E  test     r9, r9
0021E041  lea      rcx, [r9 + 8]
0021E045  cmove    rcx, r10
0021E049  mov      rcx, qword ptr [rcx]
0021E04C  mov      qword ptr [rax - 8], rcx
0021E050  mov      qword ptr [r8], r11
0021E053  mov      ecx, dword ptr [r9 + 0x10]
0021E057  mov      dword ptr [rax], ecx
0021E059  movzx    ecx, byte ptr [r9 + 0x14]
0021E05E  mov      byte ptr [rax + 4], cl
0021E061  mov      ecx, dword ptr [r9 + 0x18]
0021E065  mov      dword ptr [rax + 8], ecx
0021E068  mov      rcx, qword ptr [r9 + 0x20]
0021E06C  mov      qword ptr [rax + 0x10], rcx
0021E070  mov      rcx, qword ptr [r9 + 0x28]
0021E074  mov      qword ptr [rax + 0x18], rcx
0021E078  add      rax, 0x30
0021E07C  add      edx, -1
0021E07F  jne      0x21e035  ; -> 0021E035
0021E081  ret      
```

## 002207E0 (113 B, extent 002207E0-00220851)

Page context: "xx' stepped loop, ending with '[r9+0x10]'/'[r9+0x18]' indirect calls — container iteration with a callback pair | | element wrappers | '00220DE0', '00220E80', '00220F20', '00220FC0', '00221060' (5), '002207E0', '00220860', '00220960', '00220A00', '00220AE0' (5) | 146 B '00221xxx' + '00199DB0' shape, or '[rax]'-indirect thunks — per-element entry/alloc | | dispatch layer | '00221310', '00221390', '00221450', '00221510', '002215D0', '0022"

```
002207E0  mov      qword ptr [rsp + 8], rbx
002207E5  mov      r10, qword ptr [rcx + 8]
002207E9  mov      r11, rdx
002207EC  mov      rbx, rcx
002207EF  mov      r9, rdx
002207F2  mov      rax, r8
002207F5  cmp      r8, r10
002207F8  je       0x22081f  ; -> 0022081F
002207FA  nop      word ptr [rax + rax]
00220800  movsd    xmm0, qword ptr [rax]
00220804  movsd    qword ptr [r9], xmm0
00220809  lea      r9, [r9 + 0xa]
0022080D  movzx    ecx, word ptr [rax + 8]
00220811  add      rax, 0xa
00220815  mov      word ptr [r9 - 2], cx
0022081A  cmp      rax, r10
0022081D  jne      0x220800  ; -> 00220800
0022081F  sub      r8, r11
00220822  movabs   rax, 0x9999999999999999
0022082C  imul     r8
0022082F  sar      rdx, 2
00220833  mov      rax, rdx
00220836  shr      rax, 0x3f
0022083A  add      rdx, rax
0022083D  lea      rax, [rdx + rdx*4]
00220841  add      rax, rax
00220844  add      qword ptr [rbx + 8], rax
00220848  mov      rax, r11
0022084B  mov      rbx, qword ptr [rsp + 8]
00220850  ret      
```

## 00221310 (113 B, extent 00221310-00221381)

Page context: "0FC0', '00221060' (5), '002207E0', '00220860', '00220960', '00220A00', '00220AE0' (5) | 146 B '00221xxx' + '00199DB0' shape, or '[rax]'-indirect thunks — per-element entry/alloc | | dispatch layer | '00221310', '00221390', '00221450', '00221510', '002215D0', '002216B0' (6) | each pairs a '00225xxx' step with a '0021Fxxx' processor and a '0022xxxx'/'0020xxxx' tail — the calls the start-up itself makes |  The shape says this is SEAD's lis"

```
00221310  sub      rsp, 0x38
00221314  mov      r9, qword ptr [rcx]
00221317  movabs   rax, 0x6666666666666667
00221321  mov      r8, qword ptr [rcx + 8]
00221325  mov      r11, rcx
00221328  mov      r10d, edx
0022132B  sub      r8, r9
0022132E  imul     r8
00221331  sar      rdx, 2
00221335  mov      rax, rdx
00221338  shr      rax, 0x3f
0022133C  add      rdx, rax
0022133F  cmp      r10d, edx
00221342  jbe      0x221369  ; -> 00221369
00221344  sub      r10d, edx
00221347  lea      r9, [rsp + 0x20]
0022134C  mov      rdx, qword ptr [rcx + 8]
00221350  xor      eax, eax
00221352  mov      r8d, r10d
00221355  mov      qword ptr [rsp + 0x20], rax
0022135A  mov      word ptr [rsp + 0x28], ax
0022135F  call     0x21f130  ; -> 0021F130 fn
00221364  add      rsp, 0x38
00221368  ret      
00221369  mov      r8, qword ptr [r11 + 8]
0022136D  lea      rcx, [r10 + r10*4]
00221371  lea      rdx, [r9 + rcx*2]
00221375  mov      rcx, r11
00221378  add      rsp, 0x38
0022137C  jmp      0x2207e0  ; -> 002207E0 fn
```

## 00225490 (61 B, extent 00225490-002254CD)

Page context: "00' (219 B) is a body - 'call [rax]' vcalls only. Interior anchor '00220A88' (the first vcall).  ## SWE2-EC7-50 update (2026-09-19) - '00221390'  '00221390' (185 B) is a body - '0021F440'/'00220860'/'00225490'/'002254D0'. Interior anchor '002213E2' (a '0021F440' call).  ## SWE2-EC7-50 update (2026-09-19) - '00221450'  '00221450' (185 B) is a body - '0021F790'/'00220960'/'002255C0'/'00225610'. Interior anchor '002214A2' (a '0021F790' cal"

```
00225490  push     rbx
00225492  sub      rsp, 0x20
00225496  mov      rbx, rcx
00225499  add      rcx, 8
0022549D  call     0x7a5f10  ; -> 007A5F10 fn
002254A2  lea      rax, [rip + 0x6e32ff]  ; -> 009087A8
002254A9  mov      dword ptr [rbx + 0x10], 0xffffffff
002254B0  mov      qword ptr [rbx], rax
002254B3  xor      eax, eax
002254B5  mov      dword ptr [rbx + 0x18], eax
002254B8  mov      byte ptr [rbx + 0x14], 0
002254BC  mov      qword ptr [rbx + 0x20], rax
002254C0  mov      qword ptr [rbx + 0x28], rax
002254C4  mov      rax, rbx
002254C7  add      rsp, 0x20
002254CB  pop      rbx
002254CC  ret      
```

## 002255C0 (74 B, extent 002255C0-0022560A)

Page context: " - '0021F440'/'00220860'/'00225490'/'002254D0'. Interior anchor '002213E2' (a '0021F440' call).  ## SWE2-EC7-50 update (2026-09-19) - '00221450'  '00221450' (185 B) is a body - '0021F790'/'00220960'/'002255C0'/'00225610'. Interior anchor '002214A2' (a '0021F790' call).  ## SWE2-EC7-50 update (2026-09-19) - '00221510'  '00221510' (182 B) is a body - '0021FB20'/'00220A00'/'00225830'/'002258D0'. Interior anchor '00221562' (a '0021FB20' cal"

```
002255C0  push     rbx
002255C2  sub      rsp, 0x20
002255C6  mov      rbx, rcx
002255C9  add      rcx, 8
002255CD  call     0x7a5f10  ; -> 007A5F10 fn
002255D2  lea      rax, [rip + 0x6e31e7]  ; -> 009087C0
002255D9  mov      qword ptr [rbx], rax
002255DC  xor      eax, eax
002255DE  mov      dword ptr [rbx + 0x10], eax
002255E1  mov      dword ptr [rbx + 0x28], eax
002255E4  mov      rax, rbx
002255E7  mov      qword ptr [rbx + 0x14], 0xffffffffffffffff
002255EF  mov      dword ptr [rbx + 0x1c], 0x7f
002255F6  mov      dword ptr [rbx + 0x20], 0x40
002255FD  mov      dword ptr [rbx + 0x24], 0xffffffff
00225604  add      rsp, 0x20
00225608  pop      rbx
00225609  ret      
```

## 00225830 (67 B, extent 00225830-00225873)

Page context: " - '0021F790'/'00220960'/'002255C0'/'00225610'. Interior anchor '002214A2' (a '0021F790' call).  ## SWE2-EC7-50 update (2026-09-19) - '00221510'  '00221510' (182 B) is a body - '0021FB20'/'00220A00'/'00225830'/'002258D0'. Interior anchor '00221562' (a '0021FB20' call).  ## SWE2-EC7-58 update (2026-09-19) - '0021DF70'  '0021DF70' (169 B) is a call-free '0x80'-stride record copier - 4-iteration 'movups' pairs ('edx'=4), '009087E0'. Interi"

```
00225830  mov      qword ptr [rsp + 8], rcx
00225835  push     rbx
00225836  sub      rsp, 0x30
0022583A  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00225843  mov      rbx, rcx
00225846  lea      rax, [rip + 0x6e2fbb]  ; -> 00908808
0022584D  mov      qword ptr [rcx], rax
00225850  xor      eax, eax
00225852  mov      qword ptr [rcx + 8], rax
00225856  mov      dword ptr [rcx + 0x10], eax
00225859  mov      byte ptr [rcx + 0x20], al
0022585C  mov      ecx, 0x10000
00225861  call     0x210ec0  ; -> 00210EC0 fn
00225866  mov      qword ptr [rbx + 0x18], rax
0022586A  mov      rax, rbx
0022586D  add      rsp, 0x30
00225871  pop      rbx
00225872  ret      
```

## 00225880 (68 B, extent 00225880-002258C4)

Page context: "' (234 B) is a body - '001EDF00' single call. Interior anchor '0021E2B1' (the '001EDF00' call).  ## SWE2-EC7-46 update (2026-09-19) - '002215D0'  '002215D0' (223 B) is a body - '0021FEF0'/'00220AE0'/'00225880'/'00225920'/'00808C40'. Interior anchor '00221637' (a '0021FEF0' call).  ## SWE2-EC7-47 update (2026-09-19) - '0021DC60'  '0021DC60' (222 B) is a call-free record ctor - installs vtable '009087E0', 'movups' four '0x80'-lane copies "

```
00225880  mov      qword ptr [rsp + 8], rcx
00225885  push     rbx
00225886  sub      rsp, 0x30
0022588A  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00225893  mov      rbx, rcx
00225896  lea      rax, [rip + 0x6e2f43]  ; -> 009087E0
0022589D  mov      qword ptr [rcx], rax
002258A0  xor      eax, eax
002258A2  mov      qword ptr [rcx + 8], rax
002258A6  mov      qword ptr [rcx + 0x210], rax
002258AD  mov      ecx, 0x100000
002258B2  call     0x210ec0  ; -> 00210EC0 fn
002258B7  mov      qword ptr [rbx + 8], rax
002258BB  mov      rax, rbx
002258BE  add      rsp, 0x30
002258C2  pop      rbx
002258C3  ret      
```
