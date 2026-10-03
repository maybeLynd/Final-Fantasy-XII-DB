# F homing pack (FABLE): `00-Engine-Core-Runtime/Application-Root/game-application.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 20. No bearing page cites them and no documented function calls them directly.

## 00158DA0 (63 B, extent 00158DA0-00158DDF)

Documented callee on this page: `00210EB0`

```
00158DA0  mov      qword ptr [rsp + 8], rbx
00158DA5  push     rdi
00158DA6  sub      rsp, 0x20
00158DAA  lea      rax, [rip + 0x1b6ddaf]  ; -> 01CC6B60
00158DB1  mov      rdi, rcx
00158DB4  add      rcx, 8
00158DB8  mov      qword ptr [rcx - 8], rax
00158DBC  mov      ebx, edx
00158DBE  call     qword ptr [rip + 0x76930c]  ; -> 008C20D0 [u64 0x0000000001CCC110]
00158DC4  test     bl, 1
00158DC7  je       0x158dd1  ; -> 00158DD1
00158DC9  mov      rcx, rdi
00158DCC  call     0x210eb0  ; -> 00210EB0 fn
00158DD1  mov      rax, rdi
00158DD4  mov      rbx, qword ptr [rsp + 0x30]
00158DD9  add      rsp, 0x20
00158DDD  pop      rdi
00158DDE  ret      
```

## 00158DE0 (220 B, extent 00158DE0-00158EBC)

Documented callee on this page: `00861EC0`

```
00158DE0  sub      rsp, 0x28
00158DE4  test     edx, edx
00158DE6  jne      0x158e7f  ; -> 00158E7F
00158DEC  lea      rdx, [rip + 0x1b6dd8d]  ; -> 01CC6B80 [str "nvapi_QueryInterface"]
00158DF3  call     qword ptr [rip + 0x769337]  ; -> 008C2130 [u64 0x0000000001CCC1FC]
00158DF9  mov      qword ptr [rip + 0x2d552e0], rax  ; -> 02EAE0E0
00158E00  test     rax, rax
00158E03  je       0x158e18  ; -> 00158E18
00158E05  mov      ecx, 0x150e828
00158E0A  call     rax
00158E0C  test     rax, rax
00158E0F  jne      0x158e20  ; -> 00158E20
00158E11  mov      qword ptr [rip + 0x2d552c8], rax  ; -> 02EAE0E0
00158E18  or       eax, 0xffffffff
00158E1B  add      rsp, 0x28
00158E1F  ret      
00158E20  call     rax
00158E22  mov      r11d, eax
00158E25  test     eax, eax
00158E27  je       0x158e3a  ; -> 00158E3A
00158E29  xor      eax, eax
00158E2B  mov      qword ptr [rip + 0x2d552ae], rax  ; -> 02EAE0E0
00158E32  mov      eax, r11d
00158E35  add      rsp, 0x28
00158E39  ret      
00158E3A  mov      ecx, 0x33c7358c
00158E3F  call     qword ptr [rip + 0x2d5529b]  ; -> 02EAE0E0
00158E45  mov      ecx, 0x593e8644
00158E4A  mov      qword ptr [rip + 0x2d5529f], rax  ; -> 02EAE0F0
00158E51  call     qword ptr [rip + 0x2d55289]  ; -> 02EAE0E0
00158E57  cmp      qword ptr [rip + 0x2d55291], 0  ; -> 02EAE0F0
00158E5F  mov      qword ptr [rip + 0x2d55292], rax  ; -> 02EAE0F8
00158E66  je       0x158e6d  ; -> 00158E6D
00158E68  test     rax, rax
00158E6B  je       0x158ea1  ; -> 00158EA1
00158E6D  xor      eax, eax
00158E6F  mov      qword ptr [rip + 0x2d5527a], rax  ; -> 02EAE0F0
00158E76  mov      qword ptr [rip + 0x2d5527b], rax  ; -> 02EAE0F8
00158E7D  jmp      0x158ea1  ; -> 00158EA1
00158E7F  cmp      edx, 1
00158E82  jne      0x158ea1  ; -> 00158EA1
00158E84  lea      rdx, [rip + 0x1b6dcdd]  ; -> 01CC6B68 [str "nvapi_pepQueryInterface"]
00158E8B  call     qword ptr [rip + 0x76929f]  ; -> 008C2130 [u64 0x0000000001CCC1FC]
00158E91  mov      qword ptr [rip + 0x2d55250], rax  ; -> 02EAE0E8
00158E98  test     rax, rax
00158E9B  je       0x158e18  ; -> 00158E18
00158EA1  lea      rcx, [rip + 0x2d552a8]  ; -> 02EAE150
00158EA8  xor      edx, edx
00158EAA  mov      r8d, 0x918
00158EB0  call     0x861ec0  ; -> 00861EC0 fn
00158EB5  xor      eax, eax
00158EB7  add      rsp, 0x28
00158EBB  ret      
```

## 0015CE40 (37 B, extent 0015CE40-0015CE65)

Documented callee on this page: `00808B90`

```
0015CE40  sub      rsp, 0x28
0015CE44  mov      edx, 0x64
0015CE49  lea      rcx, [rip + 0x1e260c0]  ; -> 01F82F10
0015CE50  call     0x1f4c50  ; -> 001F4C50 fn
0015CE55  lea      rcx, [rip + 0x749ec4]  ; -> 008A6D20
0015CE5C  add      rsp, 0x28
0015CE60  jmp      0x808b90  ; -> 00808B90 fn
```

## 0015DCA0 (78 B, extent 0015DCA0-0015DCEE)

Documented callee on this page: `0016D680`

```
0015DCA0  sub      rsp, 0x28
0015DCA4  lea      rcx, [rip + 0x1ca48e5]  ; -> 01E02590
0015DCAB  call     0x16d680  ; -> 0016D680 fn
0015DCB0  xor      eax, eax
0015DCB2  lea      rcx, [rip + 0x749777]  ; -> 008A7430
0015DCB9  mov      qword ptr [rip + 0x1ca48e0], rax  ; -> 01E025A0 [u64 0x0000000000000000]
0015DCC0  xorps    xmm0, xmm0
0015DCC3  mov      byte ptr [rip + 0x1ca48df], al  ; -> 01E025A8 [u8 0x00]
0015DCC9  mov      dword ptr [rip + 0x1ca48dd], eax  ; -> 01E025AC [u32 0x00000000]
0015DCCF  lea      rax, [rip + 0x7a8a8a]  ; -> 00906760
0015DCD6  mov      qword ptr [rip + 0x1ca48a3], rax  ; -> 01E02580 [u64 0x0000000000906868]
0015DCDD  movdqa   xmmword ptr [rip + 0x1ca48ab], xmm0  ; -> 01E02590 [f32x4 0, 0, 0, 0]
0015DCE5  add      rsp, 0x28
0015DCE9  jmp      0x808b90  ; -> 00808B90 fn
```

## 0015DCF0 (51 B, extent 0015DCF0-0015DD23)

Documented callee on this page: `0016D680`

```
0015DCF0  mov      qword ptr [rsp + 8], rbx
0015DCF5  push     rdi
0015DCF6  sub      rsp, 0x20
0015DCFA  mov      edi, 0x2aa
0015DCFF  lea      rbx, [rip + 0x1e6591a]  ; -> 01FC3620
0015DD06  mov      rcx, rbx
0015DD09  call     0x16d680  ; -> 0016D680 fn
0015DD0E  add      rbx, 0x30
0015DD12  sub      rdi, 1
0015DD16  jne      0x15dd06  ; -> 0015DD06
0015DD18  mov      rbx, qword ptr [rsp + 0x30]
0015DD1D  add      rsp, 0x20
0015DD21  pop      rdi
0015DD22  ret      
```

## 001605C0 (81 B, extent 001605C0-00160611)

Documented callee on this page: `00808B90`

```
001605C0  sub      rsp, 0x28
001605C4  lea      rcx, [rip + 0x2b4d575]  ; -> 02CADB40
001605CB  call     0x5a8400  ; -> 005A8400 fn
001605D0  lea      rax, [rip + 0x45f959]  ; -> 005BFF30
001605D7  mov      qword ptr [rip + 0x2b4d662], rax  ; -> 02CADC40
001605DE  lea      rcx, [rip + 0xbcb183]  ; -> 00D2B768
001605E5  mov      eax, dword ptr [rip + 0x2b4d651]  ; -> 02CADC3C
001605EB  and      eax, 0xfffffffd
001605EE  mov      qword ptr [rip + 0x2b4d54b], rcx  ; -> 02CADB40
001605F5  or       eax, 0xc
001605F8  lea      rcx, [rip + 0x748921]  ; -> 008A8F20
001605FF  and      eax, 0xfffffff7
00160602  mov      dword ptr [rip + 0x2b4d634], eax  ; -> 02CADC3C
00160608  add      rsp, 0x28
0016060C  jmp      0x808b90  ; -> 00808B90 fn
```

## 001615C0 (78 B, extent 001615C0-0016160E)

Documented callee on this page: `00808B90`

```
001615C0  sub      rsp, 0x28
001615C4  lea      rcx, [rip + 0x2b55eb5]  ; -> 02CB7480
001615CB  call     0x5d9b30  ; -> 005D9B30 fn
001615D0  lea      rax, [rip + 0xbda659]  ; -> 00D3BC30
001615D7  mov      qword ptr [rip + 0x2b55ea2], rax  ; -> 02CB7480
001615DE  lea      rcx, [rip + 0x749acb]  ; -> 008AB0B0
001615E5  lea      rax, [rip + 0x49cd64]  ; -> 005FE350
001615EC  mov      qword ptr [rip + 0x2b55f8d], rax  ; -> 02CB7580
001615F3  mov      eax, dword ptr [rip + 0x2b55f83]  ; -> 02CB757C
001615F9  and      eax, 0xfffffffd
001615FC  or       eax, 0xc
001615FF  mov      dword ptr [rip + 0x2b55f77], eax  ; -> 02CB757C
00161605  add      rsp, 0x28
00161609  jmp      0x808b90  ; -> 00808B90 fn
```

## 00163760 (88 B, extent 00163760-001637B8)

Documented callee on this page: `00808B90`

```
00163760  sub      rsp, 0x58
00163764  mov      dword ptr [rsp + 0x40], 0x3d
0016376C  lea      rdx, [rip + 0xbf2965]  ; -> 00D560D8
00163773  mov      dword ptr [rsp + 0x38], 0x3d
0016377B  lea      rcx, [rip + 0x2b93b3e]  ; -> 02CF72C0
00163782  mov      dword ptr [rsp + 0x30], 0x3d
0016378A  mov      r9d, 0x1f8
00163790  mov      dword ptr [rsp + 0x28], 0x3d
00163798  xor      r8d, r8d
0016379B  mov      dword ptr [rsp + 0x20], 0
001637A3  call     0x616210  ; -> 00616210 fn
001637A8  lea      rcx, [rip + 0x74b7c1]  ; -> 008AEF70
001637AF  add      rsp, 0x58
001637B3  jmp      0x808b90  ; -> 00808B90 fn
```

## 00163D60 (68 B, extent 00163D60-00163DA4)

Documented callee on this page: `00808B90`

```
00163D60  sub      rsp, 0x58
00163D64  xor      eax, eax
00163D66  lea      rdx, [rip + 0xbc2f93]  ; -> 00D26D00 [str "UNKNOWN"]
00163D6D  mov      dword ptr [rsp + 0x40], eax
00163D71  lea      rcx, [rip + 0x2b93cb8]  ; -> 02CF7A30
00163D78  mov      dword ptr [rsp + 0x38], eax
00163D7C  xor      r9d, r9d
00163D7F  mov      dword ptr [rsp + 0x30], eax
00163D83  mov      dword ptr [rsp + 0x28], eax
00163D87  lea      r8d, [rax + 0x33]
00163D8B  mov      dword ptr [rsp + 0x20], eax
00163D8F  call     0x616210  ; -> 00616210 fn
00163D94  lea      rcx, [rip + 0x74b2d5]  ; -> 008AF070
00163D9B  add      rsp, 0x58
00163D9F  jmp      0x808b90  ; -> 00808B90 fn
```

## 00163F20 (119 B, extent 00163F20-00163F97)

Documented callee on this page: `00808B90`

```
00163F20  sub      rsp, 0x28
00163F24  xor      r8d, r8d
00163F27  lea      rdx, [rip + 0x2b94342]  ; -> 02CF8270
00163F2E  lea      rcx, [rip + 0x2b9474b]  ; -> 02CF8680
00163F35  call     0x632000  ; -> 00632000 fn
00163F3A  mov      eax, dword ptr [rip + 0x2b9483c]  ; -> 02CF877C
00163F40  lea      rcx, [rip + 0x2b93f89]  ; -> 02CF7ED0
00163F47  mov      qword ptr [rip + 0x2b947f2], rcx  ; -> 02CF8740
00163F4E  or       eax, 2
00163F51  lea      rcx, [rip + 0x2b93fa8]  ; -> 02CF7F00
00163F58  and      eax, 0xfffffffd
00163F5B  mov      qword ptr [rip + 0x2b947e6], rcx  ; -> 02CF8748
00163F62  or       eax, 8
00163F65  lea      rcx, [rip + 0x2b93fc4]  ; -> 02CF7F30
00163F6C  mov      dword ptr [rip + 0x2b9480a], eax  ; -> 02CF877C
00163F72  mov      qword ptr [rip + 0x2b947d7], rcx  ; -> 02CF8750
00163F79  lea      rcx, [rip + 0xbf2fd8]  ; -> 00D56F58
00163F80  mov      qword ptr [rip + 0x2b946f9], rcx  ; -> 02CF8680
00163F87  lea      rcx, [rip + 0x74b162]  ; -> 008AF0F0
00163F8E  add      rsp, 0x28
00163F92  jmp      0x808b90  ; -> 00808B90 fn
```

## 00163FA0 (105 B, extent 00163FA0-00164009)

Documented callee on this page: `00808B90`

```
00163FA0  sub      rsp, 0x28
00163FA4  xor      r8d, r8d
00163FA7  lea      rdx, [rip + 0x2b942c2]  ; -> 02CF8270
00163FAE  lea      rcx, [rip + 0x2b947cb]  ; -> 02CF8780
00163FB5  call     0x6321e0  ; -> 006321E0 fn
00163FBA  or       dword ptr [rip + 0x2b948bb], 2  ; -> 02CF887C
00163FC1  lea      rax, [rip + 0xbf28b0]  ; -> 00D56878
00163FC8  mov      qword ptr [rip + 0x2b947b1], rax  ; -> 02CF8780
00163FCF  lea      rcx, [rip + 0x74b13a]  ; -> 008AF110
00163FD6  lea      rax, [rip + 0x2b94c63]  ; -> 02CF8C40
00163FDD  mov      qword ptr [rip + 0x2b9485c], rax  ; -> 02CF8840
00163FE4  lea      rax, [rip + 0x2b94cf5]  ; -> 02CF8CE0
00163FEB  mov      qword ptr [rip + 0x2b94856], rax  ; -> 02CF8848
00163FF2  lea      rax, [rip + 0x2b94d87]  ; -> 02CF8D80
00163FF9  mov      qword ptr [rip + 0x2b94850], rax  ; -> 02CF8850
00164000  add      rsp, 0x28
00164004  jmp      0x808b90  ; -> 00808B90 fn
```

## 00164010 (116 B, extent 00164010-00164084)

Documented callee on this page: `00808B90`

```
00164010  sub      rsp, 0x28
00164014  xor      r8d, r8d
00164017  lea      rdx, [rip + 0x2b94252]  ; -> 02CF8270
0016401E  lea      rcx, [rip + 0x2b9485b]  ; -> 02CF8880
00164025  call     0x6323c0  ; -> 006323C0 fn
0016402A  mov      eax, dword ptr [rip + 0x2b9494c]  ; -> 02CF897C
00164030  lea      rcx, [rip + 0x2b93e69]  ; -> 02CF7EA0
00164037  mov      qword ptr [rip + 0x2b94902], rcx  ; -> 02CF8940
0016403E  or       eax, 2
00164041  lea      rcx, [rip + 0x2b93e68]  ; -> 02CF7EB0
00164048  and      eax, 0xfffffffd
0016404B  mov      qword ptr [rip + 0x2b948f6], rcx  ; -> 02CF8948
00164052  lea      rcx, [rip + 0x2b93e67]  ; -> 02CF7EC0
00164059  mov      qword ptr [rip + 0x2b948f0], rcx  ; -> 02CF8950
00164060  lea      rcx, [rip + 0xbf2421]  ; -> 00D56488
00164067  mov      qword ptr [rip + 0x2b94812], rcx  ; -> 02CF8880
0016406E  lea      rcx, [rip + 0x74b0bb]  ; -> 008AF130
00164075  mov      dword ptr [rip + 0x2b94901], eax  ; -> 02CF897C
0016407B  add      rsp, 0x28
0016407F  jmp      0x808b90  ; -> 00808B90 fn
```

## 00164090 (108 B, extent 00164090-001640FC)

Documented callee on this page: `00808B90`

```
00164090  sub      rsp, 0x28
00164094  mov      r8d, 0x10
0016409A  lea      rdx, [rip + 0x2b941cf]  ; -> 02CF8270
001640A1  lea      rcx, [rip + 0x2b948d8]  ; -> 02CF8980
001640A8  call     0x6325a0  ; -> 006325A0 fn
001640AD  or       dword ptr [rip + 0x2b949c8], 2  ; -> 02CF8A7C
001640B4  lea      rax, [rip + 0xbf2b45]  ; -> 00D56C00
001640BB  mov      qword ptr [rip + 0x2b948be], rax  ; -> 02CF8980
001640C2  lea      rcx, [rip + 0x74b087]  ; -> 008AF150
001640C9  lea      rax, [rip + 0x2b94ab0]  ; -> 02CF8B80
001640D0  mov      qword ptr [rip + 0x2b94969], rax  ; -> 02CF8A40
001640D7  lea      rax, [rip + 0x2b94ae2]  ; -> 02CF8BC0
001640DE  mov      qword ptr [rip + 0x2b94963], rax  ; -> 02CF8A48
001640E5  lea      rax, [rip + 0x2b94b14]  ; -> 02CF8C00
001640EC  mov      qword ptr [rip + 0x2b9495d], rax  ; -> 02CF8A50
001640F3  add      rsp, 0x28
001640F7  jmp      0x808b90  ; -> 00808B90 fn
```

## 001641C0 (39 B, extent 001641C0-001641E7)

Documented callee on this page: `00808B90`

```
001641C0  sub      rsp, 0x28
001641C4  lea      rdx, [rip + 0xbf233d]  ; -> 00D56508 [str "WriteMask"]
001641CB  lea      rcx, [rip + 0x2b9439e]  ; -> 02CF8570
001641D2  call     0x6b66f0  ; -> 006B66F0 fn
001641D7  lea      rcx, [rip + 0x74afd2]  ; -> 008AF1B0
001641DE  add      rsp, 0x28
001641E2  jmp      0x808b90  ; -> 00808B90 fn
```

## 00165370 (62 B, extent 00165370-001653AE)

Documented callee on this page: `00808FE4`

```
00165370  sub      rsp, 0x38
00165374  lea      rax, [rip + 0x4fdb25]  ; -> 00662EA0
0016537B  mov      edx, 0x88
00165380  lea      r9, [rip + 0x4e04f9]  ; -> 00645880
00165387  mov      qword ptr [rsp + 0x20], rax
0016538C  mov      r8d, 2
00165392  lea      rcx, [rip + 0x2bcfe57]  ; -> 02D351F0
00165399  call     0x808fe4  ; -> 00808FE4 fn
0016539E  lea      rcx, [rip + 0x74b2cb]  ; -> 008B0670
001653A5  add      rsp, 0x38
001653A9  jmp      0x808b90  ; -> 00808B90 fn
```

## 001674B0 (77 B, extent 001674B0-001674FD)

Documented callee on this page: `00808B90`

```
001674B0  sub      rsp, 0x28
001674B4  cmp      qword ptr [rip + 0x2cf17f4], 0  ; -> 02E58CB0
001674BC  jne      0x1674ed  ; -> 001674ED
001674BE  mov      qword ptr [rsp + 0x20], rbx
001674C3  lea      rbx, [rip + 0x1dc787e]  ; -> 01F2ED48
001674CA  mov      rcx, rbx
001674CD  call     0x6bfc60  ; -> 006BFC60 fn
001674D2  test     eax, eax
001674D4  jne      0x1674e8  ; -> 001674E8
001674D6  mov      qword ptr [rip + 0x1dc787f], 1  ; -> 01F2ED60 [u64 0x0000000000000000]
001674E1  mov      qword ptr [rip + 0x2cf17c8], rbx  ; -> 02E58CB0
001674E8  mov      rbx, qword ptr [rsp + 0x20]
001674ED  lea      rcx, [rip + 0x74eb0c]  ; -> 008B6000
001674F4  add      rsp, 0x28
001674F8  jmp      0x808b90  ; -> 00808B90 fn
```

## 001676A0 (77 B, extent 001676A0-001676ED)

Documented callee on this page: `00808B90`

```
001676A0  sub      rsp, 0x28
001676A4  cmp      qword ptr [rip + 0x2cf2514], 0  ; -> 02E59BC0
001676AC  jne      0x1676dd  ; -> 001676DD
001676AE  mov      qword ptr [rsp + 0x20], rbx
001676B3  lea      rbx, [rip + 0x1dc770e]  ; -> 01F2EDC8
001676BA  mov      rcx, rbx
001676BD  call     0x6c2380  ; -> 006C2380 fn
001676C2  test     eax, eax
001676C4  jne      0x1676d8  ; -> 001676D8
001676C6  mov      qword ptr [rip + 0x1dc770f], 1  ; -> 01F2EDE0 [u64 0x0000000000000000]
001676D1  mov      qword ptr [rip + 0x2cf24e8], rbx  ; -> 02E59BC0
001676D8  mov      rbx, qword ptr [rsp + 0x20]
001676DD  lea      rcx, [rip + 0x74f04c]  ; -> 008B6730
001676E4  add      rsp, 0x28
001676E8  jmp      0x808b90  ; -> 00808B90 fn
```

## 00167DB0 (81 B, extent 00167DB0-00167E01)

Documented callee on this page: `00808B90`

```
00167DB0  sub      rsp, 0x28
00167DB4  lea      rcx, [rip + 0x2cf6675]  ; -> 02E5E430
00167DBB  call     0x6cfdb0  ; -> 006CFDB0 fn
00167DC0  lea      rax, [rip + 0x56cf29]  ; -> 006D4CF0
00167DC7  mov      qword ptr [rip + 0x2cf6762], rax  ; -> 02E5E530
00167DCE  lea      rcx, [rip + 0xc2327b]  ; -> 00D8B050
00167DD5  mov      eax, dword ptr [rip + 0x2cf6751]  ; -> 02E5E52C
00167DDB  and      eax, 0xfffffffd
00167DDE  mov      qword ptr [rip + 0x2cf664b], rcx  ; -> 02E5E430
00167DE5  or       eax, 0xc
00167DE8  lea      rcx, [rip + 0x74f361]  ; -> 008B7150
00167DEF  and      eax, 0xfffffff7
00167DF2  mov      dword ptr [rip + 0x2cf6734], eax  ; -> 02E5E52C
00167DF8  add      rsp, 0x28
00167DFC  jmp      0x808b90  ; -> 00808B90 fn
```

## 001688F0 (81 B, extent 001688F0-00168941)

Documented callee on this page: `00808B90`

```
001688F0  sub      rsp, 0x28
001688F4  lea      rcx, [rip + 0x2d37f55]  ; -> 02EA0850
001688FB  call     0x6d9f00  ; -> 006D9F00 fn
00168900  lea      rax, [rip + 0x571a79]  ; -> 006DA380
00168907  mov      qword ptr [rip + 0x2d38042], rax  ; -> 02EA0950
0016890E  lea      rcx, [rip + 0xc25693]  ; -> 00D8DFA8
00168915  mov      eax, dword ptr [rip + 0x2d38031]  ; -> 02EA094C
0016891B  and      eax, 0xfffffffd
0016891E  mov      qword ptr [rip + 0x2d37f2b], rcx  ; -> 02EA0850
00168925  or       eax, 0xc
00168928  lea      rcx, [rip + 0x74ef81]  ; -> 008B78B0
0016892F  and      eax, 0xfffffff7
00168932  mov      dword ptr [rip + 0x2d38014], eax  ; -> 02EA094C
00168938  add      rsp, 0x28
0016893C  jmp      0x808b90  ; -> 00808B90 fn
```

## 00169450 (136 B, extent 00169450-001694D8)

Documented callee on this page: `00808B90`

```
00169450  push     rbx
00169452  sub      rsp, 0x30
00169456  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0016945F  lea      rcx, [rip + 0x2d3c3ea]  ; -> 02EA5850
00169466  call     0x662a50  ; -> 00662A50 fn
0016946B  nop      
0016946C  lea      rax, [rip + 0x1b4a4dd]  ; -> 01CB3950
00169473  mov      qword ptr [rip + 0x2d3c3d6], rax  ; -> 02EA5850
0016947A  xor      eax, eax
0016947C  mov      qword ptr [rip + 0x2d3c405], rax  ; -> 02EA5888
00169483  mov      qword ptr [rip + 0x2d3c406], rax  ; -> 02EA5890
0016948A  mov      rcx, qword ptr [rip + 0x2d3c3e7]  ; -> 02EA5878
00169491  lea      rbx, [rip + 0x2d3c3f0]  ; -> 02EA5888
00169498  cmp      rcx, rbx
0016949B  je       0x1694b6  ; -> 001694B6
0016949D  mov      eax, dword ptr [rip + 0x2d3c3cd]  ; -> 02EA5870
001694A3  shr      eax, 0x1f
001694A6  not      al
001694A8  test     al, 1
001694AA  je       0x1694b6  ; -> 001694B6
001694AC  test     rcx, rcx
001694AF  je       0x1694b6  ; -> 001694B6
001694B1  call     0x584730  ; -> 00584730 fn
001694B6  mov      qword ptr [rip + 0x2d3c3bb], rbx  ; -> 02EA5878
001694BD  mov      dword ptr [rip + 0x2d3c3a9], 0x80000001  ; -> 02EA5870
001694C7  lea      rcx, [rip + 0x74e692]  ; -> 008B7B60
001694CE  add      rsp, 0x30
001694D2  pop      rbx
001694D3  jmp      0x808b90  ; -> 00808B90 fn
```
