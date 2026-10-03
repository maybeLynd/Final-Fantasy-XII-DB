# F homing pack: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

Generated 2026-10-02 21:16 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 71. No bearing page cites them and no documented function calls them directly.

## 00584910 (63 B, extent 00584910-0058494F)

Documented callee on this page: `00599870`

```
00584910  push     rbx
00584912  sub      rsp, 0x20
00584916  mov      rcx, rdx
00584919  mov      rbx, r8
0058491C  call     0x599870  ; -> 00599870 fn
00584921  movups   xmm0, xmmword ptr [rax]
00584924  movups   xmmword ptr [rbx], xmm0
00584927  movups   xmm1, xmmword ptr [rax + 0x10]
0058492B  movups   xmmword ptr [rbx + 0x10], xmm1
0058492F  movups   xmm0, xmmword ptr [rax + 0x20]
00584933  movups   xmmword ptr [rbx + 0x20], xmm0
00584937  movups   xmm1, xmmword ptr [rax + 0x30]
0058493B  movups   xmmword ptr [rbx + 0x30], xmm1
0058493F  movsd    xmm0, qword ptr [rax + 0x40]
00584944  movsd    qword ptr [rbx + 0x40], xmm0
00584949  add      rsp, 0x20
0058494D  pop      rbx
0058494E  ret      
```

## 00584B70 (67 B, extent 00584B70-00584BB3)

Documented callee on this page: `00599970`

```
00584B70  push     rbx
00584B72  sub      rsp, 0x20
00584B76  mov      rcx, rdx
00584B79  mov      rbx, r8
00584B7C  call     0x599970  ; -> 00599970 fn
00584B81  movups   xmm0, xmmword ptr [rax]
00584B84  movups   xmmword ptr [rbx], xmm0
00584B87  movups   xmm1, xmmword ptr [rax + 0x10]
00584B8B  movups   xmmword ptr [rbx + 0x10], xmm1
00584B8F  movups   xmm0, xmmword ptr [rax + 0x20]
00584B93  movups   xmmword ptr [rbx + 0x20], xmm0
00584B97  movups   xmm1, xmmword ptr [rax + 0x30]
00584B9B  movups   xmmword ptr [rbx + 0x30], xmm1
00584B9F  movups   xmm0, xmmword ptr [rax + 0x40]
00584BA3  movups   xmmword ptr [rbx + 0x40], xmm0
00584BA7  mov      eax, dword ptr [rax + 0x50]
00584BAA  mov      dword ptr [rbx + 0x50], eax
00584BAD  add      rsp, 0x20
00584BB1  pop      rbx
00584BB2  ret      
```

## 00585060 (43 B, extent 00585060-0058508B)

Documented callee on this page: `00599A70`

```
00585060  push     rbx
00585062  sub      rsp, 0x20
00585066  mov      rcx, rdx
00585069  mov      rbx, r8
0058506C  call     0x599a70  ; -> 00599A70 fn
00585071  movups   xmm0, xmmword ptr [rax]
00585074  movups   xmmword ptr [rbx], xmm0
00585077  movups   xmm1, xmmword ptr [rax + 0x10]
0058507B  movups   xmmword ptr [rbx + 0x10], xmm1
0058507F  mov      eax, dword ptr [rax + 0x20]
00585082  mov      dword ptr [rbx + 0x20], eax
00585085  add      rsp, 0x20
00585089  pop      rbx
0058508A  ret      
```

## 005A0B60 (28 B, extent 005A0B60-005A0B7C)

Documented callee on this page: `005A05D0`

```
005A0B60  push     rbx
005A0B62  sub      rsp, 0x20
005A0B66  mov      rcx, rdx
005A0B69  mov      rbx, r8
005A0B6C  call     0x5a05d0  ; -> 005A05D0 fn
005A0B71  movzx    ecx, byte ptr [rax]
005A0B74  mov      byte ptr [rbx], cl
005A0B76  add      rsp, 0x20
005A0B7A  pop      rbx
005A0B7B  ret      
```

## 005A0D30 (45 B, extent 005A0D30-005A0D5D)

Documented callee on this page: `005BA950`

```
005A0D30  push     rbx
005A0D32  sub      rsp, 0x20
005A0D36  mov      rcx, rdx
005A0D39  mov      rbx, r8
005A0D3C  call     0x5ba950  ; -> 005BA950 fn
005A0D41  mov      ecx, dword ptr [rax + 8]
005A0D44  mov      dword ptr [rbx + 8], ecx
005A0D47  mov      rcx, qword ptr [rax + 0x10]
005A0D4B  mov      qword ptr [rbx + 0x10], rcx
005A0D4F  mov      rax, qword ptr [rax + 0x18]
005A0D53  mov      qword ptr [rbx + 0x18], rax
005A0D57  add      rsp, 0x20
005A0D5B  pop      rbx
005A0D5C  ret      
```

## 005A0FB0 (112 B, extent 005A0FB0-005A1020)

Documented callee on this page: `005B96D0`

```
005A0FB0  mov      qword ptr [rsp + 8], rbx
005A0FB5  push     rdi
005A0FB6  sub      rsp, 0x20
005A0FBA  mov      rcx, rdx
005A0FBD  mov      rbx, r8
005A0FC0  call     0x5b96d0  ; -> 005B96D0 fn
005A0FC5  mov      rdi, rax
005A0FC8  cmp      rbx, rax
005A0FCB  je       0x5a1015  ; -> 005A1015
005A0FCD  mov      ecx, dword ptr [rax + 0x20]
005A0FD0  lea      rdx, [rax + 0x28]
005A0FD4  mov      dword ptr [rbx + 0x20], ecx
005A0FD7  mov      rcx, qword ptr [rax]
005A0FDA  mov      qword ptr [rbx], rcx
005A0FDD  mov      rcx, qword ptr [rax + 8]
005A0FE1  mov      qword ptr [rbx + 8], rcx
005A0FE5  mov      rcx, qword ptr [rax + 0x10]
005A0FE9  mov      qword ptr [rbx + 0x10], rcx
005A0FED  mov      rcx, qword ptr [rax + 0x18]
005A0FF1  mov      qword ptr [rbx + 0x18], rcx
005A0FF5  lea      rcx, [rbx + 0x28]
005A0FF9  cmp      rcx, rdx
005A0FFC  je       0x5a100f  ; -> 005A100F
005A0FFE  movzx    eax, byte ptr [rdx]
005A1001  mov      rdx, qword ptr [rdx]
005A1004  and      eax, 1
005A1007  sub      rdx, rax
005A100A  call     0x1ead40  ; -> 001EAD40 fn
005A100F  mov      eax, dword ptr [rdi + 0x30]
005A1012  mov      dword ptr [rbx + 0x30], eax
005A1015  mov      rbx, qword ptr [rsp + 0x30]
005A101A  add      rsp, 0x20
005A101E  pop      rdi
005A101F  ret      
```

## 005A1260 (53 B, extent 005A1260-005A1295)

Documented callee on this page: `005B9CD0`

```
005A1260  push     rbx
005A1262  sub      rsp, 0x20
005A1266  mov      rcx, rdx
005A1269  mov      rbx, r8
005A126C  call     0x5b9cd0  ; -> 005B9CD0 fn
005A1271  mov      ecx, dword ptr [rax + 8]
005A1274  mov      dword ptr [rbx + 8], ecx
005A1277  mov      rcx, qword ptr [rax + 0x10]
005A127B  mov      qword ptr [rbx + 0x10], rcx
005A127F  mov      rcx, qword ptr [rax + 0x18]
005A1283  mov      qword ptr [rbx + 0x18], rcx
005A1287  mov      rax, qword ptr [rax + 0x20]
005A128B  mov      qword ptr [rbx + 0x20], rax
005A128F  add      rsp, 0x20
005A1293  pop      rbx
005A1294  ret      
```

## 005A1820 (45 B, extent 005A1820-005A184D)

Documented callee on this page: `005BAA70`

```
005A1820  push     rbx
005A1822  sub      rsp, 0x20
005A1826  mov      rcx, rdx
005A1829  mov      rbx, r8
005A182C  call     0x5baa70  ; -> 005BAA70 fn
005A1831  mov      ecx, dword ptr [rax + 8]
005A1834  mov      dword ptr [rbx + 8], ecx
005A1837  mov      rcx, qword ptr [rax + 0x10]
005A183B  mov      qword ptr [rbx + 0x10], rcx
005A183F  mov      rax, qword ptr [rax + 0x18]
005A1843  mov      qword ptr [rbx + 0x18], rax
005A1847  add      rsp, 0x20
005A184B  pop      rbx
005A184C  ret      
```

## 005A1BF0 (33 B, extent 005A1BF0-005A1C11)

Documented callee on this page: `005B98D0`

```
005A1BF0  push     rbx
005A1BF2  sub      rsp, 0x20
005A1BF6  mov      rcx, rdx
005A1BF9  mov      rbx, r8
005A1BFC  call     0x5b98d0  ; -> 005B98D0 fn
005A1C01  mov      rdx, rax
005A1C04  mov      rcx, rbx
005A1C07  add      rsp, 0x20
005A1C0B  pop      rbx
005A1C0C  jmp      0x5aa8c0  ; -> 005AA8C0 fn
```

## 005A1DD0 (64 B, extent 005A1DD0-005A1E10)

Documented callee on this page: `005BA750`

```
005A1DD0  push     rbx
005A1DD2  sub      rsp, 0x20
005A1DD6  mov      rcx, rdx
005A1DD9  mov      rbx, r8
005A1DDC  call     0x5ba750  ; -> 005BA750 fn
005A1DE1  mov      rcx, qword ptr [rax]
005A1DE4  lea      rdx, [rax + 8]
005A1DE8  mov      qword ptr [rbx], rcx
005A1DEB  lea      rcx, [rbx + 8]
005A1DEF  cmp      rcx, rdx
005A1DF2  je       0x5a1e0a  ; -> 005A1E0A
005A1DF4  movzx    eax, byte ptr [rdx]
005A1DF7  mov      rdx, qword ptr [rdx]
005A1DFA  and      eax, 1
005A1DFD  sub      rdx, rax
005A1E00  add      rsp, 0x20
005A1E04  pop      rbx
005A1E05  jmp      0x1ead40  ; -> 001EAD40 fn
005A1E0A  add      rsp, 0x20
005A1E0E  pop      rbx
005A1E0F  ret      
```

## 005A1EF0 (29 B, extent 005A1EF0-005A1F0D)

Documented callee on this page: `005BAEB0`

```
005A1EF0  push     rbx
005A1EF2  sub      rsp, 0x20
005A1EF6  mov      rcx, rdx
005A1EF9  mov      rbx, r8
005A1EFC  call     0x5baeb0  ; -> 005BAEB0 fn
005A1F01  mov      ecx, dword ptr [rax + 8]
005A1F04  mov      dword ptr [rbx + 8], ecx
005A1F07  add      rsp, 0x20
005A1F0B  pop      rbx
005A1F0C  ret      
```

## 005A20B0 (33 B, extent 005A20B0-005A20D1)

Documented callee on this page: `005B95D0`

```
005A20B0  push     rbx
005A20B2  sub      rsp, 0x20
005A20B6  mov      rcx, rdx
005A20B9  mov      rbx, r8
005A20BC  call     0x5b95d0  ; -> 005B95D0 fn
005A20C1  mov      rdx, rax
005A20C4  mov      rcx, rbx
005A20C7  add      rsp, 0x20
005A20CB  pop      rbx
005A20CC  jmp      0x5aa840  ; -> 005AA840 fn
```

## 005A2430 (55 B, extent 005A2430-005A2467)

Documented callee on this page: `005BAFD0`

```
005A2430  push     rbx
005A2432  sub      rsp, 0x20
005A2436  mov      rcx, rdx
005A2439  mov      rbx, r8
005A243C  call     0x5bafd0  ; -> 005BAFD0 fn
005A2441  mov      ecx, dword ptr [rax + 8]
005A2444  mov      dword ptr [rbx + 8], ecx
005A2447  mov      rcx, qword ptr [rax + 0x10]
005A244B  mov      qword ptr [rbx + 0x10], rcx
005A244F  mov      ecx, dword ptr [rax + 0x18]
005A2452  mov      dword ptr [rbx + 0x18], ecx
005A2455  mov      ecx, dword ptr [rax + 0x1c]
005A2458  mov      dword ptr [rbx + 0x1c], ecx
005A245B  mov      eax, dword ptr [rax + 0x20]
005A245E  mov      dword ptr [rbx + 0x20], eax
005A2461  add      rsp, 0x20
005A2465  pop      rbx
005A2466  ret      
```

## 005A2770 (73 B, extent 005A2770-005A27B9)

Documented callee on this page: `005B94D0`

```
005A2770  mov      qword ptr [rsp + 8], rbx
005A2775  push     rdi
005A2776  sub      rsp, 0x20
005A277A  mov      rcx, rdx
005A277D  mov      rdi, r8
005A2780  call     0x5b94d0  ; -> 005B94D0 fn
005A2785  mov      rdx, rax
005A2788  mov      rcx, rdi
005A278B  mov      rbx, rax
005A278E  call     0x5aa840  ; -> 005AA840 fn
005A2793  mov      rcx, qword ptr [rbx + 0x48]
005A2797  lea      rdx, [rbx + 0x50]
005A279B  mov      qword ptr [rdi + 0x48], rcx
005A279F  lea      rcx, [rdi + 0x50]
005A27A3  call     0x5aa3c0  ; -> 005AA3C0 fn
005A27A8  mov      eax, dword ptr [rbx + 0x60]
005A27AB  mov      rbx, qword ptr [rsp + 0x30]
005A27B0  mov      dword ptr [rdi + 0x60], eax
005A27B3  add      rsp, 0x20
005A27B7  pop      rdi
005A27B8  ret      
```

## 005A3260 (67 B, extent 005A3260-005A32A3)

Documented callee on this page: `005B9BD0`

```
005A3260  mov      qword ptr [rsp + 8], rbx
005A3265  push     rdi
005A3266  sub      rsp, 0x20
005A326A  mov      rcx, rdx
005A326D  mov      rbx, r8
005A3270  call     0x5b9bd0  ; -> 005B9BD0 fn
005A3275  mov      rdi, rax
005A3278  cmp      rbx, rax
005A327B  je       0x5a3298  ; -> 005A3298
005A327D  mov      rdx, rax
005A3280  mov      rcx, rbx
005A3283  call     0x5aa840  ; -> 005AA840 fn
005A3288  mov      rcx, qword ptr [rdi + 0x38]
005A328C  mov      qword ptr [rbx + 0x38], rcx
005A3290  movups   xmm0, xmmword ptr [rdi + 0x48]
005A3294  movups   xmmword ptr [rbx + 0x48], xmm0
005A3298  mov      rbx, qword ptr [rsp + 0x30]
005A329D  add      rsp, 0x20
005A32A1  pop      rdi
005A32A2  ret      
```

## 005A4390 (58 B, extent 005A4390-005A43CA)

Documented callee on this page: `005BAB90`

```
005A4390  mov      qword ptr [rsp + 8], rbx
005A4395  push     rdi
005A4396  sub      rsp, 0x20
005A439A  mov      rcx, rdx
005A439D  mov      rdi, r8
005A43A0  call     0x5bab90  ; -> 005BAB90 fn
005A43A5  mov      rdx, rax
005A43A8  mov      rcx, rdi
005A43AB  mov      rbx, rax
005A43AE  call     0x5aa7d0  ; -> 005AA7D0 fn
005A43B3  lea      rdx, [rbx + 0x28]
005A43B7  lea      rcx, [rdi + 0x28]
005A43BB  mov      rbx, qword ptr [rsp + 0x30]
005A43C0  add      rsp, 0x20
005A43C4  pop      rdi
005A43C5  jmp      0x5aa3c0  ; -> 005AA3C0 fn
```

## 005A5050 (58 B, extent 005A5050-005A508A)

Documented callee on this page: `005B93B0`

```
005A5050  mov      qword ptr [rsp + 8], rbx
005A5055  push     rdi
005A5056  sub      rsp, 0x20
005A505A  mov      rcx, rdx
005A505D  mov      rdi, r8
005A5060  call     0x5b93b0  ; -> 005B93B0 fn
005A5065  mov      rdx, rax
005A5068  mov      rcx, rdi
005A506B  mov      rbx, rax
005A506E  call     0x5aa7d0  ; -> 005AA7D0 fn
005A5073  lea      rdx, [rbx + 0x28]
005A5077  lea      rcx, [rdi + 0x28]
005A507B  mov      rbx, qword ptr [rsp + 0x30]
005A5080  add      rsp, 0x20
005A5084  pop      rdi
005A5085  jmp      0x5aa3c0  ; -> 005AA3C0 fn
```

## 005A50B0 (39 B, extent 005A50B0-005A50D7)

Documented callee on this page: `005B97D0`

```
005A50B0  push     rbx
005A50B2  sub      rsp, 0x20
005A50B6  mov      rcx, rdx
005A50B9  mov      rbx, r8
005A50BC  call     0x5b97d0  ; -> 005B97D0 fn
005A50C1  mov      ecx, dword ptr [rax]
005A50C3  lea      rdx, [rax + 8]
005A50C7  mov      dword ptr [rbx], ecx
005A50C9  lea      rcx, [rbx + 8]
005A50CD  add      rsp, 0x20
005A50D1  pop      rbx
005A50D2  jmp      0x5aa3c0  ; -> 005AA3C0 fn
```

## 005C1390 (91 B, extent 005C1390-005C13EB)

Documented callee on this page: `005BC4D0`

```
005C1390  mov      qword ptr [rsp + 8], rbx
005C1395  push     rdi
005C1396  sub      rsp, 0x20
005C139A  mov      rbx, rcx
005C139D  mov      rdi, rdx
005C13A0  mov      rcx, rdx
005C13A3  call     0x5bc4d0  ; -> 005BC4D0 fn
005C13A8  test     rax, rax
005C13AB  je       0x5c13e0  ; -> 005C13E0
005C13AD  movsxd   rcx, dword ptr [rbx + 0x10]
005C13B1  add      rcx, rax
005C13B4  call     qword ptr [rbx + 8]
005C13B7  mov      edx, 1
005C13BC  mov      rcx, rdi
005C13BF  mov      ebx, eax
005C13C1  call     0x80f420  ; -> 0080F420 fn
005C13C6  mov      edx, ebx
005C13C8  mov      rcx, rdi
005C13CB  call     0x810580  ; -> 00810580 fn
005C13D0  mov      eax, 1
005C13D5  mov      rbx, qword ptr [rsp + 0x30]
005C13DA  add      rsp, 0x20
005C13DE  pop      rdi
005C13DF  ret      
005C13E0  mov      rbx, qword ptr [rsp + 0x30]
005C13E5  add      rsp, 0x20
005C13E9  pop      rdi
005C13EA  ret      
```

## 005C13F0 (103 B, extent 005C13F0-005C1457)

Documented callee on this page: `005BC4D0`

```
005C13F0  mov      qword ptr [rsp + 8], rbx
005C13F5  push     rdi
005C13F6  sub      rsp, 0x30
005C13FA  mov      rdi, rcx
005C13FD  mov      rbx, rdx
005C1400  mov      rcx, rdx
005C1403  call     0x5bc4d0  ; -> 005BC4D0 fn
005C1408  test     rax, rax
005C140B  je       0x5c144c  ; -> 005C144C
005C140D  movsxd   rcx, dword ptr [rdi + 0x10]
005C1411  add      rcx, rax
005C1414  movaps   xmmword ptr [rsp + 0x20], xmm6
005C1419  call     qword ptr [rdi + 8]
005C141C  mov      edx, 1
005C1421  mov      rcx, rbx
005C1424  movaps   xmm6, xmm0
005C1427  call     0x80f420  ; -> 0080F420 fn
005C142C  movaps   xmm1, xmm6
005C142F  mov      rcx, rbx
005C1432  call     0x810640  ; -> 00810640 fn
005C1437  movaps   xmm6, xmmword ptr [rsp + 0x20]
005C143C  mov      eax, 1
005C1441  mov      rbx, qword ptr [rsp + 0x40]
005C1446  add      rsp, 0x30
005C144A  pop      rdi
005C144B  ret      
005C144C  mov      rbx, qword ptr [rsp + 0x40]
005C1451  add      rsp, 0x30
005C1455  pop      rdi
005C1456  ret      
```

## 005C15B0 (123 B, extent 005C15B0-005C162B)

Documented callee on this page: `005BC4D0`

```
005C15B0  mov      qword ptr [rsp + 8], rbx
005C15B5  push     rdi
005C15B6  sub      rsp, 0x20
005C15BA  mov      rdi, rcx
005C15BD  mov      rbx, rdx
005C15C0  mov      rcx, rdx
005C15C3  call     0x5bc4d0  ; -> 005BC4D0 fn
005C15C8  test     rax, rax
005C15CB  je       0x5c1620  ; -> 005C1620
005C15CD  movsxd   rcx, dword ptr [rdi + 0x10]
005C15D1  add      rcx, rax
005C15D4  call     qword ptr [rdi + 8]
005C15D7  mov      rcx, rbx
005C15DA  test     rax, rax
005C15DD  je       0x5c15fe  ; -> 005C15FE
005C15DF  lea      r8, [rip + 0x26ed07a]  ; -> 02CAE660
005C15E6  mov      rdx, rax
005C15E9  call     0x684080  ; -> 00684080 fn
005C15EE  mov      eax, 1
005C15F3  mov      rbx, qword ptr [rsp + 0x30]
005C15F8  add      rsp, 0x20
005C15FC  pop      rdi
005C15FD  ret      
005C15FE  mov      edx, 1
005C1603  call     0x80f420  ; -> 0080F420 fn
005C1608  mov      rcx, rbx
005C160B  call     0x810620  ; -> 00810620 fn
005C1610  mov      eax, 1
005C1615  mov      rbx, qword ptr [rsp + 0x30]
005C161A  add      rsp, 0x20
005C161E  pop      rdi
005C161F  ret      
005C1620  mov      rbx, qword ptr [rsp + 0x30]
005C1625  add      rsp, 0x20
005C1629  pop      rdi
005C162A  ret      
```

## 005C1A30 (40 B, extent 005C1A30-005C1A58)

Documented callee on this page: `005BC4D0`

```
005C1A30  push     rbx
005C1A32  sub      rsp, 0x20
005C1A36  mov      rbx, rcx
005C1A39  mov      rcx, rdx
005C1A3C  call     0x5bc4d0  ; -> 005BC4D0 fn
005C1A41  test     rax, rax
005C1A44  je       0x5c1a50  ; -> 005C1A50
005C1A46  movsxd   rcx, dword ptr [rbx + 0x10]
005C1A4A  add      rcx, rax
005C1A4D  call     qword ptr [rbx + 8]
005C1A50  xor      eax, eax
005C1A52  add      rsp, 0x20
005C1A56  pop      rbx
005C1A57  ret      
```

## 005C1AC0 (92 B, extent 005C1AC0-005C1B1C)

Documented callee on this page: `005BC4D0`

```
005C1AC0  mov      qword ptr [rsp + 8], rbx
005C1AC5  push     rdi
005C1AC6  sub      rsp, 0x20
005C1ACA  mov      rbx, rcx
005C1ACD  mov      rdi, rdx
005C1AD0  mov      rcx, rdx
005C1AD3  call     0x5bc4d0  ; -> 005BC4D0 fn
005C1AD8  test     rax, rax
005C1ADB  je       0x5c1b11  ; -> 005C1B11
005C1ADD  movsxd   rcx, dword ptr [rbx + 0x10]
005C1AE1  add      rcx, rax
005C1AE4  call     qword ptr [rbx + 8]
005C1AE7  mov      edx, 1
005C1AEC  mov      rcx, rdi
005C1AEF  movzx    ebx, al
005C1AF2  call     0x80f420  ; -> 0080F420 fn
005C1AF7  mov      edx, ebx
005C1AF9  mov      rcx, rdi
005C1AFC  call     0x810450  ; -> 00810450 fn
005C1B01  mov      eax, 1
005C1B06  mov      rbx, qword ptr [rsp + 0x30]
005C1B0B  add      rsp, 0x20
005C1B0F  pop      rdi
005C1B10  ret      
005C1B11  mov      rbx, qword ptr [rsp + 0x30]
005C1B16  add      rsp, 0x20
005C1B1A  pop      rdi
005C1B1B  ret      
```

## 005C1BB0 (89 B, extent 005C1BB0-005C1C09)

Documented callee on this page: `005BCAC0`

```
005C1BB0  mov      qword ptr [rsp + 8], rbx
005C1BB5  push     rdi
005C1BB6  sub      rsp, 0x20
005C1BBA  mov      rdi, rcx
005C1BBD  mov      rbx, rdx
005C1BC0  mov      rcx, rdx
005C1BC3  call     0x5bcac0  ; -> 005BCAC0 fn
005C1BC8  test     rax, rax
005C1BCB  je       0x5c1bfe  ; -> 005C1BFE
005C1BCD  mov      rcx, rax
005C1BD0  call     qword ptr [rdi + 8]
005C1BD3  test     rax, rax
005C1BD6  je       0x5c1bdc  ; -> 005C1BDC
005C1BD8  add      rax, 0x30
005C1BDC  lea      r8, [rip + 0x273688d]  ; -> 02CF8470
005C1BE3  mov      rdx, rax
005C1BE6  mov      rcx, rbx
005C1BE9  call     0x684080  ; -> 00684080 fn
005C1BEE  mov      eax, 1
005C1BF3  mov      rbx, qword ptr [rsp + 0x30]
005C1BF8  add      rsp, 0x20
005C1BFC  pop      rdi
005C1BFD  ret      
005C1BFE  mov      rbx, qword ptr [rsp + 0x30]
005C1C03  add      rsp, 0x20
005C1C07  pop      rdi
005C1C08  ret      
```

## 005C1C70 (89 B, extent 005C1C70-005C1CC9)

Documented callee on this page: `005BCAC0`

```
005C1C70  mov      qword ptr [rsp + 8], rbx
005C1C75  push     rdi
005C1C76  sub      rsp, 0x20
005C1C7A  mov      rbx, rcx
005C1C7D  mov      rdi, rdx
005C1C80  mov      rcx, rdx
005C1C83  call     0x5bcac0  ; -> 005BCAC0 fn
005C1C88  test     rax, rax
005C1C8B  je       0x5c1cbe  ; -> 005C1CBE
005C1C8D  mov      rcx, rax
005C1C90  call     qword ptr [rbx + 8]
005C1C93  mov      edx, 1
005C1C98  mov      rcx, rdi
005C1C9B  mov      rbx, rax
005C1C9E  call     0x80f420  ; -> 0080F420 fn
005C1CA3  mov      rdx, rbx
005C1CA6  mov      rcx, rdi
005C1CA9  call     0x810660  ; -> 00810660 fn
005C1CAE  mov      eax, 1
005C1CB3  mov      rbx, qword ptr [rsp + 0x30]
005C1CB8  add      rsp, 0x20
005C1CBC  pop      rdi
005C1CBD  ret      
005C1CBE  mov      rbx, qword ptr [rsp + 0x30]
005C1CC3  add      rsp, 0x20
005C1CC7  pop      rdi
005C1CC8  ret      
```

## 005C1CD0 (120 B, extent 005C1CD0-005C1D48)

Documented callee on this page: `005BCAC0`

```
005C1CD0  mov      qword ptr [rsp + 8], rbx
005C1CD5  push     rdi
005C1CD6  sub      rsp, 0x20
005C1CDA  mov      rdi, rcx
005C1CDD  mov      rbx, rdx
005C1CE0  mov      rcx, rdx
005C1CE3  call     0x5bcac0  ; -> 005BCAC0 fn
005C1CE8  test     rax, rax
005C1CEB  je       0x5c1d3d  ; -> 005C1D3D
005C1CED  mov      rcx, rax
005C1CF0  call     qword ptr [rdi + 8]
005C1CF3  mov      rcx, rbx
005C1CF6  test     rax, rax
005C1CF9  je       0x5c1d1b  ; -> 005C1D1B
005C1CFB  lea      rdx, [rax + 0x30]
005C1CFF  lea      r8, [rip + 0x273676a]  ; -> 02CF8470
005C1D06  call     0x684080  ; -> 00684080 fn
005C1D0B  mov      eax, 1
005C1D10  mov      rbx, qword ptr [rsp + 0x30]
005C1D15  add      rsp, 0x20
005C1D19  pop      rdi
005C1D1A  ret      
005C1D1B  mov      edx, 1
005C1D20  call     0x80f420  ; -> 0080F420 fn
005C1D25  mov      rcx, rbx
005C1D28  call     0x810620  ; -> 00810620 fn
005C1D2D  mov      eax, 1
005C1D32  mov      rbx, qword ptr [rsp + 0x30]
005C1D37  add      rsp, 0x20
005C1D3B  pop      rdi
005C1D3C  ret      
005C1D3D  mov      rbx, qword ptr [rsp + 0x30]
005C1D42  add      rsp, 0x20
005C1D46  pop      rdi
005C1D47  ret      
```

## 005C1E00 (99 B, extent 005C1E00-005C1E63)

Documented callee on this page: `005BCD20`

```
005C1E00  mov      qword ptr [rsp + 8], rbx
005C1E05  push     rdi
005C1E06  sub      rsp, 0x30
005C1E0A  mov      rdi, rcx
005C1E0D  mov      rbx, rdx
005C1E10  mov      rcx, rdx
005C1E13  call     0x5bcd20  ; -> 005BCD20 fn
005C1E18  test     rax, rax
005C1E1B  je       0x5c1e58  ; -> 005C1E58
005C1E1D  mov      rcx, rax
005C1E20  movaps   xmmword ptr [rsp + 0x20], xmm6
005C1E25  call     qword ptr [rdi + 8]
005C1E28  mov      edx, 1
005C1E2D  mov      rcx, rbx
005C1E30  movaps   xmm6, xmm0
005C1E33  call     0x80f420  ; -> 0080F420 fn
005C1E38  movaps   xmm1, xmm6
005C1E3B  mov      rcx, rbx
005C1E3E  call     0x810640  ; -> 00810640 fn
005C1E43  movaps   xmm6, xmmword ptr [rsp + 0x20]
005C1E48  mov      eax, 1
005C1E4D  mov      rbx, qword ptr [rsp + 0x40]
005C1E52  add      rsp, 0x30
005C1E56  pop      rdi
005C1E57  ret      
005C1E58  mov      rbx, qword ptr [rsp + 0x40]
005C1E5D  add      rsp, 0x30
005C1E61  pop      rdi
005C1E62  ret      
```

## 005CF610 (73 B, extent 005CF610-005CF659)

Documented callee on this page: `005F2DE0`

```
005CF610  push     rbx
005CF612  sub      rsp, 0x20
005CF616  mov      rcx, rdx
005CF619  mov      rbx, r8
005CF61C  call     0x5f2de0  ; -> 005F2DE0 fn
005CF621  movups   xmm0, xmmword ptr [rax]
005CF624  lea      rdx, [rax + 0x38]
005CF628  movups   xmmword ptr [rbx], xmm0
005CF62B  movups   xmm1, xmmword ptr [rax + 0x10]
005CF62F  movups   xmmword ptr [rbx + 0x10], xmm1
005CF633  movsd    xmm0, qword ptr [rax + 0x20]
005CF638  movsd    qword ptr [rbx + 0x20], xmm0
005CF63D  mov      ecx, dword ptr [rax + 0x28]
005CF640  mov      dword ptr [rbx + 0x28], ecx
005CF643  mov      rcx, qword ptr [rax + 0x30]
005CF647  mov      qword ptr [rbx + 0x30], rcx
005CF64B  lea      rcx, [rbx + 0x38]
005CF64F  add      rsp, 0x20
005CF653  pop      rbx
005CF654  jmp      0x646c00  ; -> 00646C00 fn
```

## 005CFA40 (99 B, extent 005CFA40-005CFAA3)

Documented callee on this page: `005F47E0`

```
005CFA40  mov      qword ptr [rsp + 8], rbx
005CFA45  push     rdi
005CFA46  sub      rsp, 0x20
005CFA4A  mov      rcx, rdx
005CFA4D  mov      rbx, r8
005CFA50  call     0x5f47e0  ; -> 005F47E0 fn
005CFA55  mov      rdi, rax
005CFA58  movzx    ecx, word ptr [rax]
005CFA5B  lea      rdx, [rax + 8]
005CFA5F  mov      word ptr [rbx], cx
005CFA62  movzx    ecx, byte ptr [rax + 2]
005CFA66  mov      byte ptr [rbx + 2], cl
005CFA69  movzx    ecx, byte ptr [rax + 3]
005CFA6D  mov      byte ptr [rbx + 3], cl
005CFA70  lea      rcx, [rbx + 8]
005CFA74  cmp      rcx, rdx
005CFA77  je       0x5cfa8c  ; -> 005CFA8C
005CFA79  movzx    r8d, byte ptr [rdx]
005CFA7D  mov      rdx, qword ptr [rdx]
005CFA80  and      r8d, 1
005CFA84  sub      rdx, r8
005CFA87  call     0x1ead40  ; -> 001EAD40 fn
005CFA8C  mov      eax, dword ptr [rdi + 0x10]
005CFA8F  mov      dword ptr [rbx + 0x10], eax
005CFA92  mov      eax, dword ptr [rdi + 0x14]
005CFA95  mov      dword ptr [rbx + 0x14], eax
005CFA98  mov      rbx, qword ptr [rsp + 0x30]
005CFA9D  add      rsp, 0x20
005CFAA1  pop      rdi
005CFAA2  ret      
```

## 005D0710 (107 B, extent 005D0710-005D077B)

Documented callee on this page: `005F4BE0`

```
005D0710  mov      qword ptr [rsp + 8], rbx
005D0715  mov      qword ptr [rsp + 0x10], rsi
005D071A  push     rdi
005D071B  sub      rsp, 0x20
005D071F  mov      rcx, rdx
005D0722  mov      rbx, r8
005D0725  call     0x5f4be0  ; -> 005F4BE0 fn
005D072A  movups   xmm0, xmmword ptr [rax]
005D072D  movups   xmmword ptr [rbx], xmm0
005D0730  mov      edi, dword ptr [rax + 0x10]
005D0733  mov      rdx, qword ptr [rax + 0x18]
005D0737  btr      edi, 0x1f
005D073B  mov      ecx, edi
005D073D  call     0x5e2f20  ; -> 005E2F20 fn
005D0742  mov      rcx, qword ptr [rbx + 0x18]
005D0746  mov      rsi, rax
005D0749  mov      eax, dword ptr [rbx + 0x10]
005D074C  cmp      rcx, rsi
005D074F  je       0x5d0764  ; -> 005D0764
005D0751  shr      eax, 0x1f
005D0754  not      al
005D0756  test     al, 1
005D0758  je       0x5d0764  ; -> 005D0764
005D075A  test     rcx, rcx
005D075D  je       0x5d0764  ; -> 005D0764
005D075F  call     0x584730  ; -> 00584730 fn
005D0764  mov      qword ptr [rbx + 0x18], rsi
005D0768  mov      rsi, qword ptr [rsp + 0x38]
005D076D  mov      dword ptr [rbx + 0x10], edi
005D0770  mov      rbx, qword ptr [rsp + 0x30]
005D0775  add      rsp, 0x20
005D0779  pop      rdi
005D077A  ret      
```

## 005D09F0 (101 B, extent 005D09F0-005D0A55)

Documented callee on this page: `005F51E0`

```
005D09F0  mov      qword ptr [rsp + 8], rbx
005D09F5  push     rdi
005D09F6  sub      rsp, 0x20
005D09FA  mov      rcx, rdx
005D09FD  mov      rbx, r8
005D0A00  call     0x5f51e0  ; -> 005F51E0 fn
005D0A05  mov      rdi, rax
005D0A08  mov      rcx, qword ptr [rax]
005D0A0B  lea      rdx, [rax + 8]
005D0A0F  mov      qword ptr [rbx], rcx
005D0A12  lea      rcx, [rbx + 8]
005D0A16  cmp      rcx, rdx
005D0A19  je       0x5d0a2e  ; -> 005D0A2E
005D0A1B  movzx    r9d, byte ptr [rdx]
005D0A1F  mov      rdx, qword ptr [rdx]
005D0A22  and      r9d, 1
005D0A26  sub      rdx, r9
005D0A29  call     0x1ead40  ; -> 001EAD40 fn
005D0A2E  mov      eax, dword ptr [rdi + 0x10]
005D0A31  mov      dword ptr [rbx + 0x10], eax
005D0A34  movzx    eax, word ptr [rdi + 0x14]
005D0A38  mov      word ptr [rbx + 0x14], ax
005D0A3C  movzx    eax, byte ptr [rdi + 0x16]
005D0A40  mov      byte ptr [rbx + 0x16], al
005D0A43  movzx    eax, byte ptr [rdi + 0x17]
005D0A47  mov      byte ptr [rbx + 0x17], al
005D0A4A  mov      rbx, qword ptr [rsp + 0x30]
005D0A4F  add      rsp, 0x20
005D0A53  pop      rdi
005D0A54  ret      
```

## 005D1990 (58 B, extent 005D1990-005D19CA)

Documented callee on this page: `005F50E0`

```
005D1990  mov      qword ptr [rsp + 8], rbx
005D1995  push     rdi
005D1996  sub      rsp, 0x20
005D199A  mov      rcx, rdx
005D199D  mov      rdi, r8
005D19A0  call     0x5f50e0  ; -> 005F50E0 fn
005D19A5  mov      rdx, rax
005D19A8  mov      rcx, rdi
005D19AB  mov      rbx, rax
005D19AE  call     0x5de830  ; -> 005DE830 fn
005D19B3  lea      rdx, [rbx + 0x10]
005D19B7  lea      rcx, [rdi + 0x10]
005D19BB  mov      rbx, qword ptr [rsp + 0x30]
005D19C0  add      rsp, 0x20
005D19C4  pop      rdi
005D19C5  jmp      0x5de680  ; -> 005DE680 fn
```

## 005D24C0 (107 B, extent 005D24C0-005D252B)

Documented callee on this page: `005F4DE0`

```
005D24C0  mov      qword ptr [rsp + 8], rbx
005D24C5  mov      qword ptr [rsp + 0x10], rsi
005D24CA  push     rdi
005D24CB  sub      rsp, 0x20
005D24CF  mov      rcx, rdx
005D24D2  mov      rbx, r8
005D24D5  call     0x5f4de0  ; -> 005F4DE0 fn
005D24DA  movups   xmm0, xmmword ptr [rax]
005D24DD  movups   xmmword ptr [rbx], xmm0
005D24E0  mov      edi, dword ptr [rax + 0x10]
005D24E3  mov      rdx, qword ptr [rax + 0x18]
005D24E7  btr      edi, 0x1f
005D24EB  mov      ecx, edi
005D24ED  call     0x5e2fb0  ; -> 005E2FB0 fn
005D24F2  mov      rcx, qword ptr [rbx + 0x18]
005D24F6  mov      rsi, rax
005D24F9  mov      eax, dword ptr [rbx + 0x10]
005D24FC  cmp      rcx, rsi
005D24FF  je       0x5d2514  ; -> 005D2514
005D2501  shr      eax, 0x1f
005D2504  not      al
005D2506  test     al, 1
005D2508  je       0x5d2514  ; -> 005D2514
005D250A  test     rcx, rcx
005D250D  je       0x5d2514  ; -> 005D2514
005D250F  call     0x584730  ; -> 00584730 fn
005D2514  mov      qword ptr [rbx + 0x18], rsi
005D2518  mov      rsi, qword ptr [rsp + 0x38]
005D251D  mov      dword ptr [rbx + 0x10], edi
005D2520  mov      rbx, qword ptr [rsp + 0x30]
005D2525  add      rsp, 0x20
005D2529  pop      rdi
005D252A  ret      
```

## 005D2C80 (90 B, extent 005D2C80-005D2CDA)

Documented callee on this page: `005F2BE0`

```
005D2C80  mov      qword ptr [rsp + 8], rbx
005D2C85  push     rdi
005D2C86  sub      rsp, 0x20
005D2C8A  mov      rcx, rdx
005D2C8D  mov      rdi, r8
005D2C90  call     0x5f2be0  ; -> 005F2BE0 fn
005D2C95  mov      rbx, rax
005D2C98  cmp      rdi, rax
005D2C9B  je       0x5d2cb1  ; -> 005D2CB1
005D2C9D  movzx    ecx, byte ptr [rax]
005D2CA0  mov      rdx, qword ptr [rax]
005D2CA3  and      ecx, 1
005D2CA6  sub      rdx, rcx
005D2CA9  mov      rcx, rdi
005D2CAC  call     0x1ead40  ; -> 001EAD40 fn
005D2CB1  lea      rdx, [rbx + 8]
005D2CB5  lea      rcx, [rdi + 8]
005D2CB9  cmp      rcx, rdx
005D2CBC  je       0x5d2ccf  ; -> 005D2CCF
005D2CBE  movzx    eax, byte ptr [rdx]
005D2CC1  mov      rdx, qword ptr [rdx]
005D2CC4  and      eax, 1
005D2CC7  sub      rdx, rax
005D2CCA  call     0x1ead40  ; -> 001EAD40 fn
005D2CCF  mov      rbx, qword ptr [rsp + 0x30]
005D2CD4  add      rsp, 0x20
005D2CD8  pop      rdi
005D2CD9  ret      
```

## 005D3D10 (84 B, extent 005D3D10-005D3D64)

Documented callee on this page: `005F34E0`

```
005D3D10  mov      qword ptr [rsp + 8], rbx
005D3D15  push     rdi
005D3D16  sub      rsp, 0x20
005D3D1A  mov      rcx, rdx
005D3D1D  mov      rdi, r8
005D3D20  call     0x5f34e0  ; -> 005F34E0 fn
005D3D25  mov      rbx, rax
005D3D28  mov      ecx, dword ptr [rax]
005D3D2A  lea      rdx, [rax + 8]
005D3D2E  mov      dword ptr [rdi], ecx
005D3D30  lea      rcx, [rdi + 8]
005D3D34  call     0x5de710  ; -> 005DE710 fn
005D3D39  lea      rdx, [rbx + 0x18]
005D3D3D  lea      rcx, [rdi + 0x18]
005D3D41  call     0x5de680  ; -> 005DE680 fn
005D3D46  lea      rdx, [rbx + 0x28]
005D3D4A  lea      rcx, [rdi + 0x28]
005D3D4E  call     0x5de830  ; -> 005DE830 fn
005D3D53  mov      eax, dword ptr [rbx + 0x38]
005D3D56  mov      rbx, qword ptr [rsp + 0x30]
005D3D5B  mov      dword ptr [rdi + 0x38], eax
005D3D5E  add      rsp, 0x20
005D3D62  pop      rdi
005D3D63  ret      
```

## 005D7990 (95 B, extent 005D7990-005D79EF)

Documented callee on this page: `005F2EE0`

```
005D7990  mov      qword ptr [rsp + 8], rbx
005D7995  push     rdi
005D7996  sub      rsp, 0x20
005D799A  mov      rcx, rdx
005D799D  mov      rbx, r8
005D79A0  call     0x5f2ee0  ; -> 005F2EE0 fn
005D79A5  mov      rdi, rax
005D79A8  mov      rcx, qword ptr [rax]
005D79AB  lea      rdx, [rax + 8]
005D79AF  mov      qword ptr [rbx], rcx
005D79B2  lea      rcx, [rbx + 8]
005D79B6  cmp      rcx, rdx
005D79B9  je       0x5d79ce  ; -> 005D79CE
005D79BB  movzx    r9d, byte ptr [rdx]
005D79BF  mov      rdx, qword ptr [rdx]
005D79C2  and      r9d, 1
005D79C6  sub      rdx, r9
005D79C9  call     0x1ead40  ; -> 001EAD40 fn
005D79CE  movzx    eax, word ptr [rdi + 0x10]
005D79D2  mov      word ptr [rbx + 0x10], ax
005D79D6  movzx    eax, byte ptr [rdi + 0x12]
005D79DA  mov      byte ptr [rbx + 0x12], al
005D79DD  movzx    eax, byte ptr [rdi + 0x13]
005D79E1  mov      byte ptr [rbx + 0x13], al
005D79E4  mov      rbx, qword ptr [rsp + 0x30]
005D79E9  add      rsp, 0x20
005D79ED  pop      rdi
005D79EE  ret      
```

## 005FF6D0 (115 B, extent 005FF6D0-005FF743)

Documented callee on this page: `005F8450`

```
005FF6D0  mov      qword ptr [rsp + 8], rbx
005FF6D5  mov      qword ptr [rsp + 0x10], rbp
005FF6DA  mov      qword ptr [rsp + 0x18], rsi
005FF6DF  push     rdi
005FF6E0  sub      rsp, 0x20
005FF6E4  mov      rbx, rdx
005FF6E7  mov      rdi, rcx
005FF6EA  mov      rcx, rbx
005FF6ED  xor      r8d, r8d
005FF6F0  or       edx, 0xffffffff
005FF6F3  call     0x811470  ; -> 00811470 fn
005FF6F8  mov      edx, 0xfffffffe
005FF6FD  mov      rcx, rbx
005FF700  mov      rsi, rax
005FF703  call     0x811130  ; -> 00811130 fn
005FF708  mov      rcx, rbx
005FF70B  call     0x683b50  ; -> 00683B50 fn
005FF710  mov      rcx, rbx
005FF713  mov      rbp, rax
005FF716  call     0x5f8450  ; -> 005F8450 fn
005FF71B  test     rax, rax
005FF71E  je       0x5ff72c  ; -> 005FF72C
005FF720  mov      r8d, esi
005FF723  mov      rdx, rbp
005FF726  mov      rcx, rax
005FF729  call     qword ptr [rdi + 8]
005FF72C  mov      rbx, qword ptr [rsp + 0x30]
005FF731  xor      eax, eax
005FF733  mov      rbp, qword ptr [rsp + 0x38]
005FF738  mov      rsi, qword ptr [rsp + 0x40]
005FF73D  add      rsp, 0x20
005FF741  pop      rdi
005FF742  ret      
```

## 005FF750 (115 B, extent 005FF750-005FF7C3)

Documented callee on this page: `005F8450`

```
005FF750  mov      qword ptr [rsp + 8], rbx
005FF755  mov      qword ptr [rsp + 0x10], rsi
005FF75A  push     rdi
005FF75B  sub      rsp, 0x30
005FF75F  mov      rbx, rdx
005FF762  movaps   xmmword ptr [rsp + 0x20], xmm6
005FF767  mov      rdi, rcx
005FF76A  xor      r8d, r8d
005FF76D  mov      rcx, rbx
005FF770  or       edx, 0xffffffff
005FF773  call     0x811640  ; -> 00811640 fn
005FF778  mov      edx, 0xfffffffe
005FF77D  mov      rcx, rbx
005FF780  movaps   xmm6, xmm0
005FF783  call     0x811130  ; -> 00811130 fn
005FF788  mov      rcx, rbx
005FF78B  call     0x683b50  ; -> 00683B50 fn
005FF790  mov      rcx, rbx
005FF793  mov      rsi, rax
005FF796  call     0x5f8450  ; -> 005F8450 fn
005FF79B  test     rax, rax
005FF79E  je       0x5ff7ac  ; -> 005FF7AC
005FF7A0  movaps   xmm2, xmm6
005FF7A3  mov      rdx, rsi
005FF7A6  mov      rcx, rax
005FF7A9  call     qword ptr [rdi + 8]
005FF7AC  mov      rbx, qword ptr [rsp + 0x40]
005FF7B1  xor      eax, eax
005FF7B3  mov      rsi, qword ptr [rsp + 0x48]
005FF7B8  movaps   xmm6, xmmword ptr [rsp + 0x20]
005FF7BD  add      rsp, 0x30
005FF7C1  pop      rdi
005FF7C2  ret      
```

## 005FF880 (104 B, extent 005FF880-005FF8E8)

Documented callee on this page: `005F8450`

```
005FF880  mov      qword ptr [rsp + 8], rbx
005FF885  mov      qword ptr [rsp + 0x10], rsi
005FF88A  push     rdi
005FF88B  sub      rsp, 0x40
005FF88F  mov      rdi, rcx
005FF892  movaps   xmmword ptr [rsp + 0x30], xmm6
005FF897  mov      rcx, rdx
005FF89A  mov      rbx, rdx
005FF89D  call     0x683bf0  ; -> 00683BF0 fn
005FF8A2  mov      rcx, rbx
005FF8A5  movups   xmm6, xmmword ptr [rax]
005FF8A8  call     0x683b50  ; -> 00683B50 fn
005FF8AD  mov      rcx, rbx
005FF8B0  mov      rsi, rax
005FF8B3  call     0x5f8450  ; -> 005F8450 fn
005FF8B8  test     rax, rax
005FF8BB  je       0x5ff8d1  ; -> 005FF8D1
005FF8BD  lea      r8, [rsp + 0x20]
005FF8C2  movdqa   xmmword ptr [rsp + 0x20], xmm6
005FF8C8  mov      rdx, rsi
005FF8CB  mov      rcx, rax
005FF8CE  call     qword ptr [rdi + 8]
005FF8D1  mov      rbx, qword ptr [rsp + 0x50]
005FF8D6  xor      eax, eax
005FF8D8  mov      rsi, qword ptr [rsp + 0x58]
005FF8DD  movaps   xmm6, xmmword ptr [rsp + 0x30]
005FF8E2  add      rsp, 0x40
005FF8E6  pop      rdi
005FF8E7  ret      
```

## 005FF990 (120 B, extent 005FF990-005FFA08)

Documented callee on this page: `005F86B0`

```
005FF990  mov      qword ptr [rsp + 8], rbx
005FF995  mov      qword ptr [rsp + 0x10], rsi
005FF99A  push     rdi
005FF99B  sub      rsp, 0x20
005FF99F  mov      rbx, rdx
005FF9A2  mov      rdi, rcx
005FF9A5  mov      rcx, rbx
005FF9A8  xor      r8d, r8d
005FF9AB  or       edx, 0xffffffff
005FF9AE  call     0x811470  ; -> 00811470 fn
005FF9B3  mov      edx, 0xfffffffe
005FF9B8  mov      rcx, rbx
005FF9BB  mov      rsi, rax
005FF9BE  call     0x811130  ; -> 00811130 fn
005FF9C3  mov      rcx, rbx
005FF9C6  call     0x5f86b0  ; -> 005F86B0 fn
005FF9CB  test     rax, rax
005FF9CE  je       0x5ff9f8  ; -> 005FF9F8
005FF9D0  mov      edx, esi
005FF9D2  mov      rcx, rax
005FF9D5  call     qword ptr [rdi + 8]
005FF9D8  mov      rdx, rax
005FF9DB  mov      rcx, rbx
005FF9DE  call     0x684130  ; -> 00684130 fn
005FF9E3  mov      eax, 1
005FF9E8  mov      rbx, qword ptr [rsp + 0x30]
005FF9ED  mov      rsi, qword ptr [rsp + 0x38]
005FF9F2  add      rsp, 0x20
005FF9F6  pop      rdi
005FF9F7  ret      
005FF9F8  mov      rbx, qword ptr [rsp + 0x30]
005FF9FD  mov      rsi, qword ptr [rsp + 0x38]
005FFA02  add      rsp, 0x20
005FFA06  pop      rdi
005FFA07  ret      
```

## 005FFCC0 (134 B, extent 005FFCC0-005FFD46)

Documented callee on this page: `005F94F0`

```
005FFCC0  mov      qword ptr [rsp + 8], rbx
005FFCC5  mov      qword ptr [rsp + 0x10], rsi
005FFCCA  push     rdi
005FFCCB  sub      rsp, 0x20
005FFCCF  mov      rdi, rdx
005FFCD2  mov      rbx, rcx
005FFCD5  mov      rcx, rdi
005FFCD8  xor      r8d, r8d
005FFCDB  or       edx, 0xffffffff
005FFCDE  call     0x811470  ; -> 00811470 fn
005FFCE3  mov      edx, 0xfffffffe
005FFCE8  mov      rcx, rdi
005FFCEB  mov      rsi, rax
005FFCEE  call     0x811130  ; -> 00811130 fn
005FFCF3  mov      rcx, rdi
005FFCF6  call     0x5f94f0  ; -> 005F94F0 fn
005FFCFB  test     rax, rax
005FFCFE  je       0x5ffd36  ; -> 005FFD36
005FFD00  mov      edx, esi
005FFD02  mov      rcx, rax
005FFD05  call     qword ptr [rbx + 8]
005FFD08  mov      edx, 1
005FFD0D  mov      rcx, rdi
005FFD10  mov      ebx, eax
005FFD12  call     0x80f420  ; -> 0080F420 fn
005FFD17  mov      edx, ebx
005FFD19  mov      rcx, rdi
005FFD1C  call     0x810580  ; -> 00810580 fn
005FFD21  mov      eax, 1
005FFD26  mov      rbx, qword ptr [rsp + 0x30]
005FFD2B  mov      rsi, qword ptr [rsp + 0x38]
005FFD30  add      rsp, 0x20
005FFD34  pop      rdi
005FFD35  ret      
005FFD36  mov      rbx, qword ptr [rsp + 0x30]
005FFD3B  mov      rsi, qword ptr [rsp + 0x38]
005FFD40  add      rsp, 0x20
005FFD44  pop      rdi
005FFD45  ret      
```

## 005FFDE0 (89 B, extent 005FFDE0-005FFE39)

Documented callee on this page: `005FCB90`

```
005FFDE0  mov      qword ptr [rsp + 8], rbx
005FFDE5  push     rdi
005FFDE6  sub      rsp, 0x20
005FFDEA  mov      rbx, rcx
005FFDED  mov      rdi, rdx
005FFDF0  mov      rcx, rdx
005FFDF3  call     0x5fcb90  ; -> 005FCB90 fn
005FFDF8  test     rax, rax
005FFDFB  je       0x5ffe2e  ; -> 005FFE2E
005FFDFD  mov      rcx, rax
005FFE00  call     qword ptr [rbx + 8]
005FFE03  mov      edx, 1
005FFE08  mov      rcx, rdi
005FFE0B  mov      rbx, rax
005FFE0E  call     0x80f420  ; -> 0080F420 fn
005FFE13  mov      rdx, rbx
005FFE16  mov      rcx, rdi
005FFE19  call     0x810660  ; -> 00810660 fn
005FFE1E  mov      eax, 1
005FFE23  mov      rbx, qword ptr [rsp + 0x30]
005FFE28  add      rsp, 0x20
005FFE2C  pop      rdi
005FFE2D  ret      
005FFE2E  mov      rbx, qword ptr [rsp + 0x30]
005FFE33  add      rsp, 0x20
005FFE37  pop      rdi
005FFE38  ret      
```

## 00604220 (127 B, extent 00604220-0060429F)

Documented callee on this page: `005D8CA0`

```
00604220  sub      rsp, 0x28
00604224  mov      rax, qword ptr gs:[0x58]
0060422D  mov      ecx, dword ptr [rip + 0x28aab09]  ; -> 02EAED3C
00604233  mov      edx, 4
00604238  mov      rcx, qword ptr [rax + rcx*8]
0060423C  mov      eax, dword ptr [rdx + rcx]
0060423F  cmp      dword ptr [rip + 0x26e8e73], eax  ; -> 02CED0B8
00604245  jg       0x604253  ; -> 00604253
00604247  lea      rax, [rip + 0x26e8e52]  ; -> 02CED0A0
0060424E  add      rsp, 0x28
00604252  ret      
00604253  lea      rcx, [rip + 0x26e8e5e]  ; -> 02CED0B8
0060425A  call     0x8092fc  ; -> 008092FC fn
0060425F  cmp      dword ptr [rip + 0x26e8e52], -1  ; -> 02CED0B8
00604266  jne      0x604247  ; -> 00604247
00604268  lea      rax, [rip + 0x26b3531]  ; -> 02CB77A0
0060426F  or       rax, 1
00604273  mov      qword ptr [rip + 0x26e8e26], rax  ; -> 02CED0A0
0060427A  call     0x5d8ca0  ; -> 005D8CA0 fn
0060427F  lea      rcx, [rip + 0x26e8e32]  ; -> 02CED0B8
00604286  mov      qword ptr [rip + 0x26e8e1b], rax  ; -> 02CED0A8
0060428D  mov      qword ptr [rip + 0x26e8e18], 0  ; -> 02CED0B0
00604298  call     0x80929c  ; -> 0080929C fn
0060429D  jmp      0x604247  ; -> 00604247
```

## 006042A0 (127 B, extent 006042A0-0060431F)

Documented callee on this page: `005D8D70`

```
006042A0  sub      rsp, 0x28
006042A4  mov      rax, qword ptr gs:[0x58]
006042AD  mov      ecx, dword ptr [rip + 0x28aaa89]  ; -> 02EAED3C
006042B3  mov      edx, 4
006042B8  mov      rcx, qword ptr [rax + rcx*8]
006042BC  mov      eax, dword ptr [rdx + rcx]
006042BF  cmp      dword ptr [rip + 0x26e8dd3], eax  ; -> 02CED098
006042C5  jg       0x6042d3  ; -> 006042D3
006042C7  lea      rax, [rip + 0x26e8db2]  ; -> 02CED080
006042CE  add      rsp, 0x28
006042D2  ret      
006042D3  lea      rcx, [rip + 0x26e8dbe]  ; -> 02CED098
006042DA  call     0x8092fc  ; -> 008092FC fn
006042DF  cmp      dword ptr [rip + 0x26e8db2], -1  ; -> 02CED098
006042E6  jne      0x6042c7  ; -> 006042C7
006042E8  lea      rax, [rip + 0x26b34b1]  ; -> 02CB77A0
006042EF  or       rax, 1
006042F3  mov      qword ptr [rip + 0x26e8d86], rax  ; -> 02CED080
006042FA  call     0x5d8d70  ; -> 005D8D70 fn
006042FF  lea      rcx, [rip + 0x26e8d92]  ; -> 02CED098
00604306  mov      qword ptr [rip + 0x26e8d7b], rax  ; -> 02CED088
0060430D  mov      qword ptr [rip + 0x26e8d78], 0  ; -> 02CED090
00604318  call     0x80929c  ; -> 0080929C fn
0060431D  jmp      0x6042c7  ; -> 006042C7
```

## 00611460 (117 B, extent 00611460-006114D5)

Documented callee on this page: `00619700`

```
00611460  push     rbx
00611462  sub      rsp, 0x20
00611466  mov      rcx, rdx
00611469  mov      rbx, r8
0061146C  call     0x619700  ; -> 00619700 fn
00611471  mov      ecx, 3
00611476  lea      rbx, [rbx + 0x80]
0061147D  movups   xmm0, xmmword ptr [rax]
00611480  lea      rax, [rax + 0x80]
00611487  movups   xmmword ptr [rbx - 0x80], xmm0
0061148B  movups   xmm1, xmmword ptr [rax - 0x70]
0061148F  movups   xmmword ptr [rbx - 0x70], xmm1
00611493  movups   xmm0, xmmword ptr [rax - 0x60]
00611497  movups   xmmword ptr [rbx - 0x60], xmm0
0061149B  movups   xmm1, xmmword ptr [rax - 0x50]
0061149F  movups   xmmword ptr [rbx - 0x50], xmm1
006114A3  movups   xmm0, xmmword ptr [rax - 0x40]
006114A7  movups   xmmword ptr [rbx - 0x40], xmm0
006114AB  movups   xmm1, xmmword ptr [rax - 0x30]
006114AF  movups   xmmword ptr [rbx - 0x30], xmm1
006114B3  movups   xmm0, xmmword ptr [rax - 0x20]
006114B7  movups   xmmword ptr [rbx - 0x20], xmm0
006114BB  movups   xmm1, xmmword ptr [rax - 0x10]
006114BF  movups   xmmword ptr [rbx - 0x10], xmm1
006114C3  sub      rcx, 1
006114C7  jne      0x611476  ; -> 00611476
006114C9  movups   xmm0, xmmword ptr [rax]
006114CC  movups   xmmword ptr [rbx], xmm0
006114CF  add      rsp, 0x20
006114D3  pop      rbx
006114D4  ret      
```

## 00612A60 (86 B, extent 00612A60-00612AB6)

Documented callee on this page: `00619800`

```
00612A60  mov      qword ptr [rsp + 8], rbx
00612A65  push     rdi
00612A66  sub      rsp, 0x20
00612A6A  mov      rcx, rdx
00612A6D  mov      rdi, r8
00612A70  call     0x619800  ; -> 00619800 fn
00612A75  mov      rbx, rax
00612A78  cmp      rdi, rax
00612A7B  je       0x612a91  ; -> 00612A91
00612A7D  movzx    ecx, byte ptr [rax]
00612A80  mov      rdx, qword ptr [rax]
00612A83  and      ecx, 1
00612A86  sub      rdx, rcx
00612A89  mov      rcx, rdi
00612A8C  call     0x1ead40  ; -> 001EAD40 fn
00612A91  mov      rcx, qword ptr [rbx + 8]
00612A95  mov      qword ptr [rdi + 8], rcx
00612A99  mov      eax, dword ptr [rbx + 0x10]
00612A9C  mov      dword ptr [rdi + 0x10], eax
00612A9F  mov      eax, dword ptr [rbx + 0x14]
00612AA2  mov      dword ptr [rdi + 0x14], eax
00612AA5  mov      eax, dword ptr [rbx + 0x18]
00612AA8  mov      rbx, qword ptr [rsp + 0x30]
00612AAD  mov      dword ptr [rdi + 0x18], eax
00612AB0  add      rsp, 0x20
00612AB4  pop      rdi
00612AB5  ret      
```

## 00624820 (117 B, extent 00624820-00624895)

Documented callee on this page: `00619D00`

```
00624820  push     rbx
00624822  sub      rsp, 0x20
00624826  mov      rcx, rdx
00624829  mov      rbx, r8
0062482C  call     0x619d00  ; -> 00619D00 fn
00624831  mov      ecx, 2
00624836  lea      rbx, [rbx + 0x80]
0062483D  movups   xmm0, xmmword ptr [rax]
00624840  lea      rax, [rax + 0x80]
00624847  movups   xmmword ptr [rbx - 0x80], xmm0
0062484B  movups   xmm1, xmmword ptr [rax - 0x70]
0062484F  movups   xmmword ptr [rbx - 0x70], xmm1
00624853  movups   xmm0, xmmword ptr [rax - 0x60]
00624857  movups   xmmword ptr [rbx - 0x60], xmm0
0062485B  movups   xmm1, xmmword ptr [rax - 0x50]
0062485F  movups   xmmword ptr [rbx - 0x50], xmm1
00624863  movups   xmm0, xmmword ptr [rax - 0x40]
00624867  movups   xmmword ptr [rbx - 0x40], xmm0
0062486B  movups   xmm1, xmmword ptr [rax - 0x30]
0062486F  movups   xmmword ptr [rbx - 0x30], xmm1
00624873  movups   xmm0, xmmword ptr [rax - 0x20]
00624877  movups   xmmword ptr [rbx - 0x20], xmm0
0062487B  movups   xmm1, xmmword ptr [rax - 0x10]
0062487F  movups   xmmword ptr [rbx - 0x10], xmm1
00624883  sub      rcx, 1
00624887  jne      0x624836  ; -> 00624836
00624889  mov      rcx, qword ptr [rax]
0062488C  mov      qword ptr [rbx], rcx
0062488F  add      rsp, 0x20
00624893  pop      rbx
00624894  ret      
```

## 0063A150 (121 B, extent 0063A150-0063A1C9)

Documented callee on this page: `00636B80`

```
0063A150  mov      qword ptr [rsp + 8], rbx
0063A155  mov      qword ptr [rsp + 0x10], rsi
0063A15A  push     rdi
0063A15B  sub      rsp, 0x20
0063A15F  mov      rbx, rcx
0063A162  mov      rdi, rdx
0063A165  mov      rcx, rdx
0063A168  call     0x6366c0  ; -> 006366C0 fn
0063A16D  mov      rcx, rdi
0063A170  mov      rsi, rax
0063A173  call     0x636b80  ; -> 00636B80 fn
0063A178  test     rax, rax
0063A17B  je       0x63a1b9  ; -> 0063A1B9
0063A17D  movsxd   rcx, dword ptr [rbx + 0x10]
0063A181  mov      rdx, rsi
0063A184  add      rcx, rax
0063A187  call     qword ptr [rbx + 8]
0063A18A  mov      edx, 1
0063A18F  mov      rcx, rdi
0063A192  movzx    ebx, al
0063A195  call     0x80f420  ; -> 0080F420 fn
0063A19A  mov      edx, ebx
0063A19C  mov      rcx, rdi
0063A19F  call     0x810450  ; -> 00810450 fn
0063A1A4  mov      eax, 1
0063A1A9  mov      rbx, qword ptr [rsp + 0x30]
0063A1AE  mov      rsi, qword ptr [rsp + 0x38]
0063A1B3  add      rsp, 0x20
0063A1B7  pop      rdi
0063A1B8  ret      
0063A1B9  mov      rbx, qword ptr [rsp + 0x30]
0063A1BE  mov      rsi, qword ptr [rsp + 0x38]
0063A1C3  add      rsp, 0x20
0063A1C7  pop      rdi
0063A1C8  ret      
```

## 0063C310 (71 B, extent 0063C310-0063C357)

Documented callee on this page: `00811640`

```
0063C310  mov      qword ptr [rsp + 8], rbx
0063C315  push     rdi
0063C316  sub      rsp, 0x30
0063C31A  mov      rbx, rdx
0063C31D  movaps   xmmword ptr [rsp + 0x20], xmm6
0063C322  mov      rdi, r8
0063C325  mov      rcx, rbx
0063C328  xor      r8d, r8d
0063C32B  or       edx, 0xffffffff
0063C32E  call     0x811640  ; -> 00811640 fn
0063C333  mov      edx, 0xfffffffe
0063C338  mov      rcx, rbx
0063C33B  movaps   xmm6, xmm0
0063C33E  call     0x811130  ; -> 00811130 fn
0063C343  mov      rbx, qword ptr [rsp + 0x40]
0063C348  movss    dword ptr [rdi], xmm6
0063C34C  movaps   xmm6, xmmword ptr [rsp + 0x20]
0063C351  add      rsp, 0x30
0063C355  pop      rdi
0063C356  ret      
```

## 0063C360 (75 B, extent 0063C360-0063C3AB)

Documented callee on this page: `00811640`

```
0063C360  mov      qword ptr [rsp + 8], rbx
0063C365  push     rdi
0063C366  sub      rsp, 0x30
0063C36A  mov      rbx, rdx
0063C36D  movaps   xmmword ptr [rsp + 0x20], xmm6
0063C372  mov      rdi, r8
0063C375  mov      rcx, rbx
0063C378  xor      r8d, r8d
0063C37B  or       edx, 0xffffffff
0063C37E  call     0x811640  ; -> 00811640 fn
0063C383  xorps    xmm6, xmm6
0063C386  mov      edx, 0xfffffffe
0063C38B  mov      rcx, rbx
0063C38E  cvtss2sd xmm6, xmm0
0063C392  call     0x811130  ; -> 00811130 fn
0063C397  mov      rbx, qword ptr [rsp + 0x40]
0063C39C  movsd    qword ptr [rdi], xmm6
0063C3A0  movaps   xmm6, xmmword ptr [rsp + 0x20]
0063C3A5  add      rsp, 0x30
0063C3A9  pop      rdi
0063C3AA  ret      
```

## 0065F390 (71 B, extent 0065F390-0065F3D7)

Documented callee on this page: `0066C800`

```
0065F390  mov      qword ptr [rsp + 8], rbx
0065F395  push     rdi
0065F396  sub      rsp, 0x20
0065F39A  mov      rcx, rdx
0065F39D  mov      rdi, r8
0065F3A0  call     0x66c800  ; -> 0066C800 fn
0065F3A5  mov      rdx, rax
0065F3A8  mov      rcx, rdi
0065F3AB  mov      rbx, rax
0065F3AE  call     0x6638a0  ; -> 006638A0 fn
0065F3B3  lea      rdx, [rbx + 0x30]
0065F3B7  lea      rcx, [rdi + 0x30]
0065F3BB  call     0x6632f0  ; -> 006632F0 fn
0065F3C0  lea      rdx, [rbx + 0x40]
0065F3C4  lea      rcx, [rdi + 0x40]
0065F3C8  mov      rbx, qword ptr [rsp + 0x30]
0065F3CD  add      rsp, 0x20
0065F3D1  pop      rdi
0065F3D2  jmp      0x6636b0  ; -> 006636B0 fn
```

## 0065FB70 (71 B, extent 0065FB70-0065FBB7)

Documented callee on this page: `0066C600`

```
0065FB70  mov      qword ptr [rsp + 8], rbx
0065FB75  push     rdi
0065FB76  sub      rsp, 0x20
0065FB7A  mov      rcx, rdx
0065FB7D  mov      rdi, r8
0065FB80  call     0x66c600  ; -> 0066C600 fn
0065FB85  mov      rdx, rax
0065FB88  mov      rcx, rdi
0065FB8B  mov      rbx, rax
0065FB8E  call     0x6638a0  ; -> 006638A0 fn
0065FB93  lea      rdx, [rbx + 0x30]
0065FB97  lea      rcx, [rdi + 0x30]
0065FB9B  call     0x6632f0  ; -> 006632F0 fn
0065FBA0  lea      rdx, [rbx + 0x40]
0065FBA4  lea      rcx, [rdi + 0x40]
0065FBA8  mov      rbx, qword ptr [rsp + 0x30]
0065FBAD  add      rsp, 0x20
0065FBB1  pop      rdi
0065FBB2  jmp      0x6636b0  ; -> 006636B0 fn
```

## 00660510 (91 B, extent 00660510-0066056B)

Documented callee on this page: `0066BD00`

```
00660510  mov      qword ptr [rsp + 8], rbx
00660515  push     rdi
00660516  sub      rsp, 0x20
0066051A  mov      rcx, rdx
0066051D  mov      rdi, r8
00660520  call     0x66bd00  ; -> 0066BD00 fn
00660525  mov      rdx, rax
00660528  mov      rcx, rdi
0066052B  mov      rbx, rax
0066052E  call     0x663560  ; -> 00663560 fn
00660533  lea      rdx, [rbx + 0x20]
00660537  lea      rcx, [rdi + 0x20]
0066053B  call     0x663400  ; -> 00663400 fn
00660540  mov      ecx, dword ptr [rbx + 0x70]
00660543  mov      dword ptr [rdi + 0x70], ecx
00660546  mov      ecx, dword ptr [rbx + 0x74]
00660549  mov      dword ptr [rdi + 0x74], ecx
0066054C  mov      ecx, dword ptr [rbx + 0x78]
0066054F  mov      dword ptr [rdi + 0x78], ecx
00660552  mov      rax, qword ptr [rbx + 0x80]
00660559  mov      rbx, qword ptr [rsp + 0x30]
0066055E  mov      qword ptr [rdi + 0x80], rax
00660565  add      rsp, 0x20
00660569  pop      rdi
0066056A  ret      
```

## 006613B0 (91 B, extent 006613B0-0066140B)

Documented callee on this page: `0066BA00`

```
006613B0  mov      qword ptr [rsp + 8], rbx
006613B5  push     rdi
006613B6  sub      rsp, 0x20
006613BA  mov      rcx, rdx
006613BD  mov      rdi, r8
006613C0  call     0x66ba00  ; -> 0066BA00 fn
006613C5  mov      rdx, rax
006613C8  mov      rcx, rdi
006613CB  mov      rbx, rax
006613CE  call     0x663560  ; -> 00663560 fn
006613D3  lea      rdx, [rbx + 0x20]
006613D7  lea      rcx, [rdi + 0x20]
006613DB  call     0x663400  ; -> 00663400 fn
006613E0  mov      ecx, dword ptr [rbx + 0x70]
006613E3  mov      dword ptr [rdi + 0x70], ecx
006613E6  mov      ecx, dword ptr [rbx + 0x74]
006613E9  mov      dword ptr [rdi + 0x74], ecx
006613EC  mov      ecx, dword ptr [rbx + 0x78]
006613EF  mov      dword ptr [rdi + 0x78], ecx
006613F2  mov      rax, qword ptr [rbx + 0x80]
006613F9  mov      rbx, qword ptr [rsp + 0x30]
006613FE  mov      qword ptr [rdi + 0x80], rax
00661405  add      rsp, 0x20
00661409  pop      rdi
0066140A  ret      
```

## 0066FD90 (118 B, extent 0066FD90-0066FE06)

Documented callee on this page: `0066E900`

```
0066FD90  mov      qword ptr [rsp + 8], rbx
0066FD95  mov      qword ptr [rsp + 0x10], rsi
0066FD9A  push     rdi
0066FD9B  sub      rsp, 0x20
0066FD9F  mov      rbx, rcx
0066FDA2  mov      rdi, rdx
0066FDA5  mov      rcx, rdx
0066FDA8  call     0x683b50  ; -> 00683B50 fn
0066FDAD  mov      rcx, rdi
0066FDB0  mov      rsi, rax
0066FDB3  call     0x66e900  ; -> 0066E900 fn
0066FDB8  test     rax, rax
0066FDBB  je       0x66fdf6  ; -> 0066FDF6
0066FDBD  mov      rdx, rsi
0066FDC0  mov      rcx, rax
0066FDC3  call     qword ptr [rbx + 8]
0066FDC6  mov      edx, 1
0066FDCB  mov      rcx, rdi
0066FDCE  movsxd   rbx, eax
0066FDD1  call     0x80f420  ; -> 0080F420 fn
0066FDD6  mov      rdx, rbx
0066FDD9  mov      rcx, rdi
0066FDDC  call     0x810580  ; -> 00810580 fn
0066FDE1  mov      eax, 1
0066FDE6  mov      rbx, qword ptr [rsp + 0x30]
0066FDEB  mov      rsi, qword ptr [rsp + 0x38]
0066FDF0  add      rsp, 0x20
0066FDF4  pop      rdi
0066FDF5  ret      
0066FDF6  mov      rbx, qword ptr [rsp + 0x30]
0066FDFB  mov      rsi, qword ptr [rsp + 0x38]
0066FE00  add      rsp, 0x20
0066FE04  pop      rdi
0066FE05  ret      
```

## 00674E90 (100 B, extent 00674E90-00674EF4)

Documented callee on this page: `00676600`

```
00674E90  mov      qword ptr [rsp + 8], rbx
00674E95  push     rdi
00674E96  sub      rsp, 0x20
00674E9A  mov      rcx, rdx
00674E9D  mov      rbx, r8
00674EA0  call     0x676600  ; -> 00676600 fn
00674EA5  mov      rdi, rax
00674EA8  mov      rcx, qword ptr [rax]
00674EAB  lea      rdx, [rax + 8]
00674EAF  mov      qword ptr [rbx], rcx
00674EB2  lea      rcx, [rbx + 8]
00674EB6  cmp      rcx, rdx
00674EB9  je       0x674ee1  ; -> 00674EE1
00674EBB  movzx    r9d, byte ptr [rdx]
00674EBF  mov      rdx, qword ptr [rdx]
00674EC2  and      r9d, 1
00674EC6  sub      rdx, r9
00674EC9  call     0x1ead40  ; -> 001EAD40 fn
00674ECE  mov      rax, qword ptr [rdi + 0x10]
00674ED2  mov      qword ptr [rbx + 0x10], rax
00674ED6  mov      rbx, qword ptr [rsp + 0x30]
00674EDB  add      rsp, 0x20
00674EDF  pop      rdi
00674EE0  ret      
00674EE1  mov      rax, qword ptr [rax + 0x10]
00674EE5  mov      qword ptr [rbx + 0x10], rax
00674EE9  mov      rbx, qword ptr [rsp + 0x30]
00674EEE  add      rsp, 0x20
00674EF2  pop      rdi
00674EF3  ret      
```

## 00677680 (93 B, extent 00677680-006776DD)

Documented callee on this page: `00676810`

```
00677680  mov      qword ptr [rsp + 8], rbx
00677685  push     rdi
00677686  sub      rsp, 0x20
0067768A  mov      rbx, rcx
0067768D  mov      rdi, rdx
00677690  mov      rcx, rdx
00677693  call     0x676810  ; -> 00676810 fn
00677698  test     rax, rax
0067769B  je       0x6776d2  ; -> 006776D2
0067769D  movsxd   rcx, dword ptr [rbx + 0x10]
006776A1  add      rcx, rax
006776A4  call     qword ptr [rbx + 8]
006776A7  test     rax, rax
006776AA  je       0x6776b0  ; -> 006776B0
006776AC  add      rax, 0x30
006776B0  lea      r8, [rip + 0x2680db9]  ; -> 02CF8470
006776B7  mov      rdx, rax
006776BA  mov      rcx, rdi
006776BD  call     0x684080  ; -> 00684080 fn
006776C2  mov      eax, 1
006776C7  mov      rbx, qword ptr [rsp + 0x30]
006776CC  add      rsp, 0x20
006776D0  pop      rdi
006776D1  ret      
006776D2  mov      rbx, qword ptr [rsp + 0x30]
006776D7  add      rsp, 0x20
006776DB  pop      rdi
006776DC  ret      
```

## 006776E0 (84 B, extent 006776E0-00677734)

Documented callee on this page: `00676810`

```
006776E0  mov      qword ptr [rsp + 8], rbx
006776E5  push     rdi
006776E6  sub      rsp, 0x20
006776EA  mov      rdi, rcx
006776ED  mov      rbx, rdx
006776F0  mov      rcx, rdx
006776F3  call     0x676810  ; -> 00676810 fn
006776F8  test     rax, rax
006776FB  je       0x677729  ; -> 00677729
006776FD  movsxd   rcx, dword ptr [rdi + 0x10]
00677701  add      rcx, rax
00677704  call     qword ptr [rdi + 8]
00677707  lea      r8, [rip + 0x27d5f22]  ; -> 02E4D630
0067770E  mov      rcx, rbx
00677711  mov      rdx, rax
00677714  call     0x684080  ; -> 00684080 fn
00677719  mov      eax, 1
0067771E  mov      rbx, qword ptr [rsp + 0x30]
00677723  add      rsp, 0x20
00677727  pop      rdi
00677728  ret      
00677729  mov      rbx, qword ptr [rsp + 0x30]
0067772E  add      rsp, 0x20
00677732  pop      rdi
00677733  ret      
```

## 00678F90 (95 B, extent 00678F90-00678FEF)

Documented callee on this page: `00678DE0`

```
00678F90  mov      qword ptr [rsp + 8], rbx
00678F95  push     rdi
00678F96  sub      rsp, 0x30
00678F9A  mov      rbx, rdx
00678F9D  movaps   xmmword ptr [rsp + 0x20], xmm6
00678FA2  mov      rdi, rcx
00678FA5  xor      r8d, r8d
00678FA8  mov      rcx, rbx
00678FAB  or       edx, 0xffffffff
00678FAE  call     0x811640  ; -> 00811640 fn
00678FB3  mov      edx, 0xfffffffe
00678FB8  mov      rcx, rbx
00678FBB  movaps   xmm6, xmm0
00678FBE  call     0x811130  ; -> 00811130 fn
00678FC3  mov      rcx, rbx
00678FC6  call     0x678de0  ; -> 00678DE0 fn
00678FCB  test     rax, rax
00678FCE  je       0x678fdd  ; -> 00678FDD
00678FD0  movsxd   rcx, dword ptr [rdi + 0x10]
00678FD4  movaps   xmm1, xmm6
00678FD7  add      rcx, rax
00678FDA  call     qword ptr [rdi + 8]
00678FDD  mov      rbx, qword ptr [rsp + 0x40]
00678FE2  xor      eax, eax
00678FE4  movaps   xmm6, xmmword ptr [rsp + 0x20]
00678FE9  add      rsp, 0x30
00678FED  pop      rdi
00678FEE  ret      
```

## 0067EF00 (73 B, extent 0067EF00-0067EF49)

Documented callee on this page: `0067EDD0`

```
0067EF00  mov      qword ptr [rsp + 8], rbx
0067EF05  push     rdi
0067EF06  sub      rsp, 0x20
0067EF0A  mov      rdi, rcx
0067EF0D  mov      rbx, rdx
0067EF10  mov      rcx, rdx
0067EF13  call     0x67edd0  ; -> 0067EDD0 fn
0067EF18  test     rax, rax
0067EF1B  je       0x67ef3e  ; -> 0067EF3E
0067EF1D  mov      rcx, rax
0067EF20  call     qword ptr [rdi + 8]
0067EF23  mov      rdx, rax
0067EF26  mov      rcx, rbx
0067EF29  call     0x6b3610  ; -> 006B3610 fn
0067EF2E  mov      eax, 1
0067EF33  mov      rbx, qword ptr [rsp + 0x30]
0067EF38  add      rsp, 0x20
0067EF3C  pop      rdi
0067EF3D  ret      
0067EF3E  mov      rbx, qword ptr [rsp + 0x30]
0067EF43  add      rsp, 0x20
0067EF47  pop      rdi
0067EF48  ret      
```

## 00680D20 (76 B, extent 00680D20-00680D6C)

Documented callee on this page: `00683250`

```
00680D20  mov      qword ptr [rsp + 8], rbx
00680D25  push     rdi
00680D26  sub      rsp, 0x20
00680D2A  mov      rcx, rdx
00680D2D  mov      rdi, r8
00680D30  call     0x683250  ; -> 00683250 fn
00680D35  mov      rbx, rax
00680D38  cmp      rdi, rax
00680D3B  je       0x680d51  ; -> 00680D51
00680D3D  movzx    ecx, byte ptr [rax]
00680D40  mov      rdx, qword ptr [rax]
00680D43  and      ecx, 1
00680D46  sub      rdx, rcx
00680D49  mov      rcx, rdi
00680D4C  call     0x1ead40  ; -> 001EAD40 fn
00680D51  mov      rax, qword ptr [rbx + 8]
00680D55  mov      qword ptr [rdi + 8], rax
00680D59  mov      rax, qword ptr [rbx + 0x10]
00680D5D  mov      rbx, qword ptr [rsp + 0x30]
00680D62  mov      qword ptr [rdi + 0x10], rax
00680D66  add      rsp, 0x20
00680D6A  pop      rdi
00680D6B  ret      
```

## 0068A850 (74 B, extent 0068A850-0068A89A)

Documented callee on this page: `0069A950`

```
0068A850  mov      qword ptr [rsp + 8], rbx
0068A855  push     rdi
0068A856  sub      rsp, 0x20
0068A85A  mov      rcx, rdx
0068A85D  mov      rdi, r8
0068A860  call     0x69a950  ; -> 0069A950 fn
0068A865  mov      rdx, rax
0068A868  mov      rcx, rdi
0068A86B  mov      rbx, rax
0068A86E  call     0x6928b0  ; -> 006928B0 fn
0068A873  mov      rcx, qword ptr [rbx + 0x118]
0068A87A  mov      qword ptr [rdi + 0x118], rcx
0068A881  mov      rax, qword ptr [rbx + 0x120]
0068A888  mov      rbx, qword ptr [rsp + 0x30]
0068A88D  mov      qword ptr [rdi + 0x120], rax
0068A894  add      rsp, 0x20
0068A898  pop      rdi
0068A899  ret      
```

## 0068BCC0 (74 B, extent 0068BCC0-0068BD0A)

Documented callee on this page: `0069A750`

```
0068BCC0  mov      qword ptr [rsp + 8], rbx
0068BCC5  push     rdi
0068BCC6  sub      rsp, 0x20
0068BCCA  mov      rcx, rdx
0068BCCD  mov      rdi, r8
0068BCD0  call     0x69a750  ; -> 0069A750 fn
0068BCD5  mov      rdx, rax
0068BCD8  mov      rcx, rdi
0068BCDB  mov      rbx, rax
0068BCDE  call     0x6928b0  ; -> 006928B0 fn
0068BCE3  mov      rcx, qword ptr [rbx + 0x118]
0068BCEA  mov      qword ptr [rdi + 0x118], rcx
0068BCF1  mov      rax, qword ptr [rbx + 0x120]
0068BCF8  mov      rbx, qword ptr [rsp + 0x30]
0068BCFD  mov      qword ptr [rdi + 0x120], rax
0068BD04  add      rsp, 0x20
0068BD08  pop      rdi
0068BD09  ret      
```

## 006A0EE0 (77 B, extent 006A0EE0-006A0F2D)

Documented callee on this page: `0069BFC0`

```
006A0EE0  mov      qword ptr [rsp + 8], rbx
006A0EE5  push     rdi
006A0EE6  sub      rsp, 0x20
006A0EEA  mov      rdi, rcx
006A0EED  mov      rbx, rdx
006A0EF0  mov      rcx, rdx
006A0EF3  call     0x69bfc0  ; -> 0069BFC0 fn
006A0EF8  test     rax, rax
006A0EFB  je       0x6a0f22  ; -> 006A0F22
006A0EFD  movsxd   rcx, dword ptr [rdi + 0x10]
006A0F01  add      rcx, rax
006A0F04  call     qword ptr [rdi + 8]
006A0F07  mov      rdx, rax
006A0F0A  mov      rcx, rbx
006A0F0D  call     0x6843d0  ; -> 006843D0 fn
006A0F12  mov      eax, 1
006A0F17  mov      rbx, qword ptr [rsp + 0x30]
006A0F1C  add      rsp, 0x20
006A0F20  pop      rdi
006A0F21  ret      
006A0F22  mov      rbx, qword ptr [rsp + 0x30]
006A0F27  add      rsp, 0x20
006A0F2B  pop      rdi
006A0F2C  ret      
```

## 006A0FE0 (99 B, extent 006A0FE0-006A1043)

Documented callee on this page: `0069C220`

```
006A0FE0  mov      qword ptr [rsp + 8], rbx
006A0FE5  push     rdi
006A0FE6  sub      rsp, 0x30
006A0FEA  mov      rdi, rcx
006A0FED  mov      rbx, rdx
006A0FF0  mov      rcx, rdx
006A0FF3  call     0x69c220  ; -> 0069C220 fn
006A0FF8  test     rax, rax
006A0FFB  je       0x6a1038  ; -> 006A1038
006A0FFD  mov      rcx, rax
006A1000  movaps   xmmword ptr [rsp + 0x20], xmm6
006A1005  call     qword ptr [rdi + 8]
006A1008  mov      edx, 1
006A100D  mov      rcx, rbx
006A1010  movaps   xmm6, xmm0
006A1013  call     0x80f420  ; -> 0080F420 fn
006A1018  movaps   xmm1, xmm6
006A101B  mov      rcx, rbx
006A101E  call     0x810640  ; -> 00810640 fn
006A1023  movaps   xmm6, xmmword ptr [rsp + 0x20]
006A1028  mov      eax, 1
006A102D  mov      rbx, qword ptr [rsp + 0x40]
006A1032  add      rsp, 0x30
006A1036  pop      rdi
006A1037  ret      
006A1038  mov      rbx, qword ptr [rsp + 0x40]
006A103D  add      rsp, 0x30
006A1041  pop      rdi
006A1042  ret      
```

## 006A1050 (88 B, extent 006A1050-006A10A8)

Documented callee on this page: `0069C220`

```
006A1050  mov      qword ptr [rsp + 8], rbx
006A1055  push     rdi
006A1056  sub      rsp, 0x20
006A105A  mov      rbx, rcx
006A105D  mov      rdi, rdx
006A1060  mov      rcx, rdx
006A1063  call     0x69c220  ; -> 0069C220 fn
006A1068  test     rax, rax
006A106B  je       0x6a109d  ; -> 006A109D
006A106D  mov      rcx, rax
006A1070  call     qword ptr [rbx + 8]
006A1073  mov      edx, 1
006A1078  mov      rcx, rdi
006A107B  movzx    ebx, al
006A107E  call     0x80f420  ; -> 0080F420 fn
006A1083  mov      edx, ebx
006A1085  mov      rcx, rdi
006A1088  call     0x810450  ; -> 00810450 fn
006A108D  mov      eax, 1
006A1092  mov      rbx, qword ptr [rsp + 0x30]
006A1097  add      rsp, 0x20
006A109B  pop      rdi
006A109C  ret      
006A109D  mov      rbx, qword ptr [rsp + 0x30]
006A10A2  add      rsp, 0x20
006A10A6  pop      rdi
006A10A7  ret      
```

## 006A10B0 (88 B, extent 006A10B0-006A1108)

Documented callee on this page: `0069D520`

```
006A10B0  mov      qword ptr [rsp + 8], rbx
006A10B5  push     rdi
006A10B6  sub      rsp, 0x40
006A10BA  mov      rdi, rcx
006A10BD  mov      rbx, rdx
006A10C0  mov      rcx, rdx
006A10C3  call     0x69d520  ; -> 0069D520 fn
006A10C8  test     rax, rax
006A10CB  je       0x6a10fd  ; -> 006A10FD
006A10CD  lea      rdx, [rsp + 0x30]
006A10D2  mov      rcx, rax
006A10D5  call     qword ptr [rdi + 8]
006A10D8  lea      rdx, [rsp + 0x20]
006A10DD  mov      rcx, rbx
006A10E0  movups   xmm0, xmmword ptr [rax]
006A10E3  movaps   xmmword ptr [rsp + 0x20], xmm0
006A10E8  call     0x6843d0  ; -> 006843D0 fn
006A10ED  mov      eax, 1
006A10F2  mov      rbx, qword ptr [rsp + 0x50]
006A10F7  add      rsp, 0x40
006A10FB  pop      rdi
006A10FC  ret      
006A10FD  mov      rbx, qword ptr [rsp + 0x50]
006A1102  add      rsp, 0x40
006A1106  pop      rdi
006A1107  ret      
```

## 006A11C0 (99 B, extent 006A11C0-006A1223)

Documented callee on this page: `0069D650`

```
006A11C0  mov      qword ptr [rsp + 8], rbx
006A11C5  push     rdi
006A11C6  sub      rsp, 0x30
006A11CA  mov      rdi, rcx
006A11CD  mov      rbx, rdx
006A11D0  mov      rcx, rdx
006A11D3  call     0x69d650  ; -> 0069D650 fn
006A11D8  test     rax, rax
006A11DB  je       0x6a1218  ; -> 006A1218
006A11DD  mov      rcx, rax
006A11E0  movaps   xmmword ptr [rsp + 0x20], xmm6
006A11E5  call     qword ptr [rdi + 8]
006A11E8  mov      edx, 1
006A11ED  mov      rcx, rbx
006A11F0  movaps   xmm6, xmm0
006A11F3  call     0x80f420  ; -> 0080F420 fn
006A11F8  movaps   xmm1, xmm6
006A11FB  mov      rcx, rbx
006A11FE  call     0x810640  ; -> 00810640 fn
006A1203  movaps   xmm6, xmmword ptr [rsp + 0x20]
006A1208  mov      eax, 1
006A120D  mov      rbx, qword ptr [rsp + 0x40]
006A1212  add      rsp, 0x30
006A1216  pop      rdi
006A1217  ret      
006A1218  mov      rbx, qword ptr [rsp + 0x40]
006A121D  add      rsp, 0x30
006A1221  pop      rdi
006A1222  ret      
```

## 006A1230 (120 B, extent 006A1230-006A12A8)

Documented callee on this page: `0069D650`

```
006A1230  mov      qword ptr [rsp + 8], rbx
006A1235  push     rdi
006A1236  sub      rsp, 0x20
006A123A  mov      rdi, rcx
006A123D  mov      rbx, rdx
006A1240  mov      rcx, rdx
006A1243  call     0x69d650  ; -> 0069D650 fn
006A1248  test     rax, rax
006A124B  je       0x6a129d  ; -> 006A129D
006A124D  mov      rcx, rax
006A1250  call     qword ptr [rdi + 8]
006A1253  mov      rcx, rbx
006A1256  test     rax, rax
006A1259  je       0x6a127b  ; -> 006A127B
006A125B  lea      rdx, [rax + 8]
006A125F  lea      r8, [rip + 0x27b066a]  ; -> 02E518D0
006A1266  call     0x684080  ; -> 00684080 fn
006A126B  mov      eax, 1
006A1270  mov      rbx, qword ptr [rsp + 0x30]
006A1275  add      rsp, 0x20
006A1279  pop      rdi
006A127A  ret      
006A127B  mov      edx, 1
006A1280  call     0x80f420  ; -> 0080F420 fn
006A1285  mov      rcx, rbx
006A1288  call     0x810620  ; -> 00810620 fn
006A128D  mov      eax, 1
006A1292  mov      rbx, qword ptr [rsp + 0x30]
006A1297  add      rsp, 0x20
006A129B  pop      rdi
006A129C  ret      
006A129D  mov      rbx, qword ptr [rsp + 0x30]
006A12A2  add      rsp, 0x20
006A12A6  pop      rdi
006A12A7  ret      
```

## 006A1330 (36 B, extent 006A1330-006A1354)

Documented callee on this page: `0069D650`

```
006A1330  push     rbx
006A1332  sub      rsp, 0x20
006A1336  mov      rbx, rcx
006A1339  mov      rcx, rdx
006A133C  call     0x69d650  ; -> 0069D650 fn
006A1341  test     rax, rax
006A1344  je       0x6a134c  ; -> 006A134C
006A1346  mov      rcx, rax
006A1349  call     qword ptr [rbx + 8]
006A134C  xor      eax, eax
006A134E  add      rsp, 0x20
006A1352  pop      rbx
006A1353  ret      
```

## 006A13B0 (88 B, extent 006A13B0-006A1408)

Documented callee on this page: `0069D650`

```
006A13B0  mov      qword ptr [rsp + 8], rbx
006A13B5  push     rdi
006A13B6  sub      rsp, 0x20
006A13BA  mov      rbx, rcx
006A13BD  mov      rdi, rdx
006A13C0  mov      rcx, rdx
006A13C3  call     0x69d650  ; -> 0069D650 fn
006A13C8  test     rax, rax
006A13CB  je       0x6a13fd  ; -> 006A13FD
006A13CD  mov      rcx, rax
006A13D0  call     qword ptr [rbx + 8]
006A13D3  mov      edx, 1
006A13D8  mov      rcx, rdi
006A13DB  movzx    ebx, al
006A13DE  call     0x80f420  ; -> 0080F420 fn
006A13E3  mov      edx, ebx
006A13E5  mov      rcx, rdi
006A13E8  call     0x810450  ; -> 00810450 fn
006A13ED  mov      eax, 1
006A13F2  mov      rbx, qword ptr [rsp + 0x30]
006A13F7  add      rsp, 0x20
006A13FB  pop      rdi
006A13FC  ret      
006A13FD  mov      rbx, qword ptr [rsp + 0x30]
006A1402  add      rsp, 0x20
006A1406  pop      rdi
006A1407  ret      
```
