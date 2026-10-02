# F-interior pack: `06-Movement-And-Navigation/Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/setting-the-movement-mode-and-which-way-a-character-turns.json`.

Functions: 12. Each is cited on the page only at its entry and is still in the F frontier.

## 0026C330 (117 B, extent 0026C330-0026C3A5)

Page context: " from 'turn_step': '+0x68 = (i16)((target_heading − heading) / +0x58)' at '00269338'–'00269351', sets '+0x28 |= 0x80' (the bit every reader masks off) and '+0x78 = [01DFE0B4]'. The timed turn setter '0026C330' ('turnt', 'rturnt_4b', 'rturnat', 'dira', 'dir_4e') sets '+0x68 = +0x66 = [01DFE0B4] + frames / [01DFE0BC]' and '+0x78 = [01DFE0B4]'. **So 'turn_step' is consumed twice — as the per-frame cap in modes 2 and 3, and as the divisor t"

```
0026C330  test     edx, edx
0026C332  jle      0x26c34a  ; -> 0026C34A
0026C334  movd     xmm0, edx
0026C338  cvtdq2ps xmm0, xmm0
0026C33B  divss    xmm0, dword ptr [rip + 0x1b91d79]  ; -> 01DFE0BC [f32 1]
0026C343  cvttss2si r8d, xmm0
0026C348  jmp      0x26c34d  ; -> 0026C34D
0026C34A  xor      r8d, r8d
0026C34D  movzx    eax, byte ptr [rcx + 3]
0026C351  and      al, 0xe0
0026C353  cmp      al, 0x60
0026C355  jne      0x26c3a4  ; -> 0026C3A4
0026C357  mov      rdx, qword ptr [rcx + 0xb8]
0026C35E  xorps    xmm0, xmm0
0026C361  movzx    ecx, word ptr [rip + 0x1b91d4c]  ; -> 01DFE0B4 [u16 0x0001]
0026C368  add      cx, r8w
0026C36C  mov      rax, qword ptr [rdx + 0xf0]
0026C373  mov      word ptr [rax + 0x68], cx
0026C377  mov      eax, dword ptr [rip + 0x1b91d37]  ; -> 01DFE0B4 [u32 0x00000001]
0026C37D  cvtsi2ss xmm0, rax
0026C382  mov      rax, qword ptr [rdx + 0xf0]
0026C389  movss    dword ptr [rax + 0x78], xmm0
0026C38E  movzx    ecx, word ptr [rip + 0x1b91d1f]  ; -> 01DFE0B4 [u16 0x0001]
0026C395  mov      rax, qword ptr [rdx + 0xf0]
0026C39C  add      cx, r8w
0026C3A0  mov      word ptr [rax + 0x66], cx
0026C3A4  ret      
```

## 0026D630 (98 B, extent 0026D630-0026D692)

Page context: "ading += +0x3C', wrapped, through 'Actor_SetFacingHeading_Variant0' ('002E5A9E'–'002E5AED') — **a constant spin**, inert only because '+0x3C' is zero unless 'setvelrotangzx' ('0x003C' → '003535C0' → '0026D630' → '002E60C0') set it | '0026C120''s downgrade target | | 2 | heading approaches **the desired movement heading** ('00263CC0': context '+0xA4' for class 3, '+0x38' for class 1) by at most 'turn_step' ('003A1AD0', '002E5A78'–'002E5A"

```
0026D630  movaps   xmm3, xmm1
0026D633  xorps    xmm0, xmm0
0026D636  mulss    xmm3, dword ptr [rip + 0x1b90a7e]  ; -> 01DFE0BC [f32 1]
0026D63E  comiss   xmm3, xmm0
0026D641  jb       0x26d64d  ; -> 0026D64D
0026D643  movss    xmm4, dword ptr [rip + 0x1a7e605]  ; -> 01CEBC50 [f32 3.141593]
0026D64B  jmp      0x26d655  ; -> 0026D655
0026D64D  movss    xmm4, dword ptr [rip + 0x6a7fcb]  ; -> 00915620 [f32 -3.141593]
0026D655  movzx    eax, byte ptr [rcx + 3]
0026D659  addss    xmm3, xmm4
0026D65D  and      al, 0xe0
0026D65F  cmp      al, 0x60
0026D661  jne      0x26d691  ; -> 0026D691
0026D663  movaps   xmm0, xmm3
0026D666  divss    xmm0, dword ptr [rip + 0x1a7e60a]  ; -> 01CEBC78 [f32 6.283185]
0026D66E  cvttss2si eax, xmm0
0026D672  movd     xmm1, eax
0026D676  cvtdq2ps xmm1, xmm1
0026D679  mulss    xmm1, dword ptr [rip + 0x1a7e5f7]  ; -> 01CEBC78 [f32 6.283185]
0026D681  subss    xmm3, xmm1
0026D685  subss    xmm3, xmm4
0026D689  movaps   xmm1, xmm3
0026D68C  jmp      0x2e60c0  ; -> 002E60C0 fn
0026D691  ret      
```

## 002E60C0 (35 B, extent 002E60C0-002E60E3)

Page context: "C', wrapped, through 'Actor_SetFacingHeading_Variant0' ('002E5A9E'–'002E5AED') — **a constant spin**, inert only because '+0x3C' is zero unless 'setvelrotangzx' ('0x003C' → '003535C0' → '0026D630' → '002E60C0') set it | '0026C120''s downgrade target | | 2 | heading approaches **the desired movement heading** ('00263CC0': context '+0xA4' for class 3, '+0x38' for class 1) by at most 'turn_step' ('003A1AD0', '002E5A78'–'002E5A94') — "face "

```
002E60C0  test     rcx, rcx
002E60C3  je       0x2e60e2  ; -> 002E60E2
002E60C5  cmp      qword ptr [rcx + 0xc0], 0
002E60CD  je       0x2e60e2  ; -> 002E60E2
002E60CF  mov      rax, qword ptr [rcx + 0xb8]
002E60D6  mov      rcx, qword ptr [rax + 0xf0]
002E60DD  movss    dword ptr [rcx + 0x3c], xmm1
002E60E2  ret      
```

## 002E8170 (87 B, extent 002E8170-002E81C7)

Page context: "026-09-20) - '003DDAD0' flag-decoded record build measured  '003DDAD0' (100 B) is the coded-arg forward the movement-mode callers run: '00263F40(rcx)' resolves the record and 'byte[+0xD] >> 7' feeds '002E8170'; then 'r8d' bit '0x18' selects a '01EFE9D0' table dword indexed by 'r8d & 0xFFFFFF', or '(byte[rbx+0x15] << 0x14) | r8d | bit 0xC'; the body tails '002EB3E0(rcx, decoded, -1.0f)'. Interior anchor '003DDB2F' (the '002EB3E0' tail). "

```
002E8170  test     rcx, rcx
002E8173  je       0x2e81c6  ; -> 002E81C6
002E8175  mov      rax, qword ptr [rcx + 0xc0]
002E817C  test     rax, rax
002E817F  je       0x2e81c6  ; -> 002E81C6
002E8181  cmp      dword ptr [rax], -1
002E8184  je       0x2e81c6  ; -> 002E81C6
002E8186  movzx    ecx, word ptr [rax]
002E8189  cmp      cx, -1
002E818D  je       0x2e81c6  ; -> 002E81C6
002E818F  movsx    rax, cx
002E8193  imul     rcx, rax, 0x740
002E819A  add      rcx, qword ptr [rip + 0x1fded87]  ; -> 022C6F28
002E81A1  je       0x2e81c6  ; -> 002E81C6
002E81A3  mov      eax, dword ptr [rcx + 0x284]
002E81A9  test     eax, eax
002E81AB  je       0x2e81c6  ; -> 002E81C6
002E81AD  test     edx, edx
002E81AF  je       0x2e81bc  ; -> 002E81BC
002E81B1  bts      eax, 0x13
002E81B5  mov      dword ptr [rcx + 0x284], eax
002E81BB  ret      
002E81BC  btr      eax, 0x13
002E81C0  mov      dword ptr [rcx + 0x284], eax
002E81C6  ret      
```

## 002EA780 (110 B, extent 002EA780-002EA7EE)

Page context: "02E5931') | the timed turns: 'turnt' / 'rturnt' ('003425D0'), 'rturnt_4b' (second site), 'rturnat' / 'turnat' ('0034D9B0'), 'dira' ('0034E040'), 'dir_4e' ('0034E360') — 5 sites pass 4 | | 5 | waits: '002EA780' is true when the render record's '+0x284' is set and '002EA910' returns 1 (an animation-state test); then '0026C120(actor, 0)' ('002E5853'–'002E5A6E') | **nobody found** — all 29 call sites of '0026C120' pass 0, 2, 3 or 4, re-deri"

```
002EA780  push     rbx
002EA782  sub      rsp, 0x20
002EA786  mov      rbx, rcx
002EA789  test     rcx, rcx
002EA78C  je       0x2ea7e6  ; -> 002EA7E6
002EA78E  mov      rax, qword ptr [rcx + 0xc0]
002EA795  test     rax, rax
002EA798  je       0x2ea7e6  ; -> 002EA7E6
002EA79A  cmp      dword ptr [rax], -1
002EA79D  je       0x2ea7e6  ; -> 002EA7E6
002EA79F  movzx    ecx, word ptr [rax]
002EA7A2  cmp      cx, -1
002EA7A6  je       0x2ea7e6  ; -> 002EA7E6
002EA7A8  movsx    rax, cx
002EA7AC  imul     rcx, rax, 0x740
002EA7B3  add      rcx, qword ptr [rip + 0x1fdc76e]  ; -> 022C6F28
002EA7BA  je       0x2ea7e6  ; -> 002EA7E6
002EA7BC  cmp      dword ptr [rcx + 0x284], 0
002EA7C3  je       0x2ea7e6  ; -> 002EA7E6
002EA7C5  call     0x3e6af0  ; -> 003E6AF0 fn
002EA7CA  test     eax, eax
002EA7CC  je       0x2ea7e6  ; -> 002EA7E6
002EA7CE  mov      rcx, rbx
002EA7D1  call     0x2ea910  ; -> 002EA910 fn
002EA7D6  xor      ecx, ecx
002EA7D8  cmp      eax, 1
002EA7DB  sete     cl
002EA7DE  mov      eax, ecx
002EA7E0  add      rsp, 0x20
002EA7E4  pop      rbx
002EA7E5  ret      
002EA7E6  xor      eax, eax
002EA7E8  add      rsp, 0x20
002EA7EC  pop      rbx
002EA7ED  ret      
```

## 002EA910 (96 B, extent 002EA910-002EA970)

Page context: "turnt_4b' (second site), 'rturnat' / 'turnat' ('0034D9B0'), 'dira' ('0034E040'), 'dir_4e' ('0034E360') — 5 sites pass 4 | | 5 | waits: '002EA780' is true when the render record's '+0x284' is set and '002EA910' returns 1 (an animation-state test); then '0026C120(actor, 0)' ('002E5853'–'002E5A6E') | **nobody found** — all 29 call sites of '0026C120' pass 0, 2, 3 or 4, re-derived independently §11 ('0034DC60' does **not** forward: it is 'm"

```
002EA910  sub      rsp, 0x28
002EA914  test     rcx, rcx
002EA917  je       0x2ea966  ; -> 002EA966
002EA919  mov      rax, qword ptr [rcx + 0xc0]
002EA920  test     rax, rax
002EA923  je       0x2ea966  ; -> 002EA966
002EA925  cmp      dword ptr [rax], -1
002EA928  je       0x2ea966  ; -> 002EA966
002EA92A  movzx    ecx, word ptr [rax]
002EA92D  cmp      cx, -1
002EA931  je       0x2ea966  ; -> 002EA966
002EA933  movsx    rax, cx
002EA937  imul     rcx, rax, 0x740
002EA93E  add      rcx, qword ptr [rip + 0x1fdc5e3]  ; -> 022C6F28
002EA945  je       0x2ea966  ; -> 002EA966
002EA947  cmp      dword ptr [rcx + 0x284], 0
002EA94E  je       0x2ea966  ; -> 002EA966
002EA950  call     0x3e6df0  ; -> 003E6DF0 fn
002EA955  test     rax, rax
002EA958  je       0x2ea966  ; -> 002EA966
002EA95A  mov      rcx, rax
002EA95D  add      rsp, 0x28
002EA961  jmp      0x3e2c00  ; -> 003E2C00 fn
002EA966  mov      eax, 1
002EA96B  add      rsp, 0x28
002EA96F  ret      
```

## 003425D0 (110 B, extent 003425D0-0034263E)

Page context: "78 += 1' ('0026C300'); at 't ≥ 1' (or when the manager flag '02099011[…]' forces it) the heading is set to the target and the mode to 0 ('002E5862'–'002E5931') | the timed turns: 'turnt' / 'rturnt' ('003425D0'), 'rturnt_4b' (second site), 'rturnat' / 'turnat' ('0034D9B0'), 'dira' ('0034E040'), 'dir_4e' ('0034E360') — 5 sites pass 4 | | 5 | waits: '002EA780' is true when the render record's '+0x284' is set and '002EA910' returns 1 (an an"

```
003425D0  mov      qword ptr [rsp + 8], rbx
003425D5  mov      qword ptr [rsp + 0x10], rbp
003425DA  mov      qword ptr [rsp + 0x18], rsi
003425DF  push     rdi
003425E0  sub      rsp, 0x20
003425E4  mov      rsi, rcx
003425E7  mov      rbx, r9
003425EA  mov      rcx, r9
003425ED  mov      rdi, r8
003425F0  mov      rbp, rdx
003425F3  call     0x267e10  ; -> 00267E10 fn
003425F8  mov      edx, eax
003425FA  mov      rcx, rbp
003425FD  call     0x26c330  ; -> 0026C330 fn
00342602  xor      edx, edx
00342604  mov      rcx, rbp
00342607  call     0x26a1a0  ; -> 0026A1A0 fn
0034260C  mov      r9, rbx
0034260F  mov      r8, rdi
00342612  mov      rdx, rbp
00342615  mov      rcx, rsi
00342618  call     0x357de0  ; -> 00357DE0 fn
0034261D  mov      edx, 4
00342622  mov      rcx, rbp
00342625  mov      rbx, qword ptr [rsp + 0x30]
0034262A  mov      rbp, qword ptr [rsp + 0x38]
0034262F  mov      rsi, qword ptr [rsp + 0x40]
00342634  add      rsp, 0x20
00342638  pop      rdi
00342639  jmp      0x26c120  ; -> 0026C120 fn
```

## 0034D9B0 (100 B, extent 0034D9B0-0034DA14)

Page context: "2099011[…]' forces it) the heading is set to the target and the mode to 0 ('002E5862'–'002E5931') | the timed turns: 'turnt' / 'rturnt' ('003425D0'), 'rturnt_4b' (second site), 'rturnat' / 'turnat' ('0034D9B0'), 'dira' ('0034E040'), 'dir_4e' ('0034E360') — 5 sites pass 4 | | 5 | waits: '002EA780' is true when the render record's '+0x284' is set and '002EA910' returns 1 (an animation-state test); then '0026C120(actor, 0)' ('002E5853'–'00"

```
0034D9B0  mov      qword ptr [rsp + 8], rbx
0034D9B5  mov      qword ptr [rsp + 0x10], rbp
0034D9BA  mov      qword ptr [rsp + 0x18], rsi
0034D9BF  push     rdi
0034D9C0  sub      rsp, 0x20
0034D9C4  mov      rsi, rcx
0034D9C7  mov      rbx, r9
0034D9CA  mov      rcx, r9
0034D9CD  mov      rdi, r8
0034D9D0  mov      rbp, rdx
0034D9D3  call     0x267e10  ; -> 00267E10 fn
0034D9D8  mov      edx, eax
0034D9DA  mov      rcx, rbp
0034D9DD  call     0x26c330  ; -> 0026C330 fn
0034D9E2  mov      r9, rbx
0034D9E5  mov      r8, rdi
0034D9E8  mov      rdx, rbp
0034D9EB  mov      rcx, rsi
0034D9EE  call     0x34be50  ; -> 0034BE50 fn
0034D9F3  mov      edx, 4
0034D9F8  mov      rcx, rbp
0034D9FB  mov      rbx, qword ptr [rsp + 0x30]
0034DA00  mov      rbp, qword ptr [rsp + 0x38]
0034DA05  mov      rsi, qword ptr [rsp + 0x40]
0034DA0A  add      rsp, 0x20
0034DA0E  pop      rdi
0034DA0F  jmp      0x26c120  ; -> 0026C120 fn
```

## 0034E040 (110 B, extent 0034E040-0034E0AE)

Page context: ") the heading is set to the target and the mode to 0 ('002E5862'–'002E5931') | the timed turns: 'turnt' / 'rturnt' ('003425D0'), 'rturnt_4b' (second site), 'rturnat' / 'turnat' ('0034D9B0'), 'dira' ('0034E040'), 'dir_4e' ('0034E360') — 5 sites pass 4 | | 5 | waits: '002EA780' is true when the render record's '+0x284' is set and '002EA910' returns 1 (an animation-state test); then '0026C120(actor, 0)' ('002E5853'–'002E5A6E') | **nobody f"

```
0034E040  mov      qword ptr [rsp + 8], rbx
0034E045  mov      qword ptr [rsp + 0x10], rbp
0034E04A  mov      qword ptr [rsp + 0x18], rsi
0034E04F  push     rdi
0034E050  sub      rsp, 0x20
0034E054  mov      rbp, rdx
0034E057  mov      rsi, rcx
0034E05A  xor      edx, edx
0034E05C  mov      rcx, r9
0034E05F  mov      rbx, r9
0034E062  mov      rdi, r8
0034E065  call     0x267f90  ; -> 00267F90 fn
0034E06A  mov      rcx, rbx
0034E06D  call     0x267e10  ; -> 00267E10 fn
0034E072  mov      edx, eax
0034E074  mov      rcx, rbp
0034E077  call     0x26c330  ; -> 0026C330 fn
0034E07C  mov      r9, rbx
0034E07F  mov      r8, rdi
0034E082  mov      rdx, rbp
0034E085  mov      rcx, rsi
0034E088  call     0x34be50  ; -> 0034BE50 fn
0034E08D  mov      edx, 4
0034E092  mov      rcx, rbp
0034E095  mov      rbx, qword ptr [rsp + 0x30]
0034E09A  mov      rbp, qword ptr [rsp + 0x38]
0034E09F  mov      rsi, qword ptr [rsp + 0x40]
0034E0A4  add      rsp, 0x20
0034E0A8  pop      rdi
0034E0A9  jmp      0x26c120  ; -> 0026C120 fn
```

## 0034E360 (120 B, extent 0034E360-0034E3D8)

Page context: " the target and the mode to 0 ('002E5862'–'002E5931') | the timed turns: 'turnt' / 'rturnt' ('003425D0'), 'rturnt_4b' (second site), 'rturnat' / 'turnat' ('0034D9B0'), 'dira' ('0034E040'), 'dir_4e' ('0034E360') — 5 sites pass 4 | | 5 | waits: '002EA780' is true when the render record's '+0x284' is set and '002EA910' returns 1 (an animation-state test); then '0026C120(actor, 0)' ('002E5853'–'002E5A6E') | **nobody found** — all 29 call si"

```
0034E360  mov      qword ptr [rsp + 8], rbx
0034E365  mov      qword ptr [rsp + 0x10], rbp
0034E36A  mov      qword ptr [rsp + 0x18], rsi
0034E36F  push     rdi
0034E370  sub      rsp, 0x20
0034E374  mov      rbp, rdx
0034E377  mov      rsi, rcx
0034E37A  xor      edx, edx
0034E37C  mov      rcx, r9
0034E37F  mov      rbx, r9
0034E382  mov      rdi, r8
0034E385  call     0x267f90  ; -> 00267F90 fn
0034E38A  mov      rcx, rbx
0034E38D  call     0x267e10  ; -> 00267E10 fn
0034E392  mov      edx, eax
0034E394  mov      rcx, rbp
0034E397  call     0x26c330  ; -> 0026C330 fn
0034E39C  xor      edx, edx
0034E39E  mov      rcx, rbp
0034E3A1  call     0x26a1a0  ; -> 0026A1A0 fn
0034E3A6  mov      r9, rbx
0034E3A9  mov      r8, rdi
0034E3AC  mov      rdx, rbp
0034E3AF  mov      rcx, rsi
0034E3B2  call     0x357de0  ; -> 00357DE0 fn
0034E3B7  mov      edx, 4
0034E3BC  mov      rcx, rbp
0034E3BF  mov      rbx, qword ptr [rsp + 0x30]
0034E3C4  mov      rbp, qword ptr [rsp + 0x38]
0034E3C9  mov      rsi, qword ptr [rsp + 0x40]
0034E3CE  add      rsp, 0x20
0034E3D2  pop      rdi
0034E3D3  jmp      0x26c120  ; -> 0026C120 fn
```

## 003A1980 (23 B, extent 003A1980-003A1997)

Page context: "dary, no shared ownership.  ## SWE2-EC7-39 update (2026-09-19) - '003EC040'  '003EC040' (433 B) is a movement-mode body - '01DFE0BC'/'022C6F28', '003A1AD0' pair plus '00422D50'/'003E56C0'/'003EC510'/'003A1980'. Interior anchor '003EC0D2' (a '00422D50' call).  ## SWE2-EC7-44 update (2026-09-19) - '00357DE0'  '00357DE0' (273 B) is an effect-element body - '00263D00'/'00265020'/'00265200'/'00267DB0'/'00267F60'/'0026C090'/'0026C120'. Interi"

```
003A1980  xorps    xmm2, xmm2
003A1983  cvtss2sd xmm2, xmm0
003A1987  andps    xmm2, xmmword ptr [rip + 0x194a3f2]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
003A198E  cvtpd2ps xmm0, xmm2
003A1992  minss    xmm0, xmm1
003A1996  ret      
```

## 003EC510 (103 B, extent 003EC510-003EC577)

Page context: " layer boundary, no shared ownership.  ## SWE2-EC7-39 update (2026-09-19) - '003EC040'  '003EC040' (433 B) is a movement-mode body - '01DFE0BC'/'022C6F28', '003A1AD0' pair plus '00422D50'/'003E56C0'/'003EC510'/'003A1980'. Interior anchor '003EC0D2' (a '00422D50' call).  ## SWE2-EC7-44 update (2026-09-19) - '00357DE0'  '00357DE0' (273 B) is an effect-element body - '00263D00'/'00265020'/'00265200'/'00267DB0'/'00267F60'/'0026C090'/'0026C1"

```
003EC510  movss    xmm1, dword ptr [rip + 0x529108]  ; -> 00915620 [f32 -3.141593]
003EC518  comiss   xmm1, xmm0
003EC51B  movss    xmm3, dword ptr [rip + 0x18ff755]  ; -> 01CEBC78 [f32 6.283185]
003EC523  jbe      0x3ec52e  ; -> 003EC52E
003EC525  addss    xmm0, xmm3
003EC529  comiss   xmm1, xmm0
003EC52C  ja       0x3ec525  ; -> 003EC525
003EC52E  movss    xmm1, dword ptr [rip + 0x18ff71a]  ; -> 01CEBC50 [f32 3.141593]
003EC536  comiss   xmm0, xmm1
003EC539  movss    xmm2, dword ptr [rip + 0x5290e3]  ; -> 00915624 [f32 -6.283185]
003EC541  jbe      0x3ec54c  ; -> 003EC54C
003EC543  addss    xmm0, xmm2
003EC547  comiss   xmm0, xmm1
003EC54A  ja       0x3ec543  ; -> 003EC543
003EC54C  xorps    xmm1, xmm1
003EC54F  ucomiss  xmm0, xmm1
003EC552  jp       0x3ec55a  ; -> 003EC55A
003EC554  jne      0x3ec55a  ; -> 003EC55A
003EC556  movaps   xmm0, xmm1
003EC559  ret      
003EC55A  test     edx, edx
003EC55C  je       0x3ec56d  ; -> 003EC56D
003EC55E  cmp      edx, 1
003EC561  jne      0x3ec576  ; -> 003EC576
003EC563  comiss   xmm0, xmm1
003EC566  jbe      0x3ec576  ; -> 003EC576
003EC568  addss    xmm0, xmm2
003EC56C  ret      
003EC56D  comiss   xmm1, xmm0
003EC570  jbe      0x3ec576  ; -> 003EC576
003EC572  addss    xmm0, xmm3
003EC576  ret      
```
