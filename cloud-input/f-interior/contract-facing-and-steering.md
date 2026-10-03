# F-interior pack: `06-Movement-And-Navigation/CONTRACT-facing-and-steering.md`

Generated 2026-10-02 12:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-facing-and-steering.json`.

Functions: 17. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: FABLE.md, SWE2-FRONTIER.md). OPUS read these before packing.

## 00265550 (43 B, extent 00265550-0026557B)

Page context: "0xDC]' record '+0x34' float, slot-'edx' (clamped) record '+0x34', 'sub[+0x62]>>6 &1', 'sub[+0x28]&0x7F', 'cvttss2si(sub[+0x78])', 'movsx(sub[+0x68])' | whole cluster; leaves at '00265510'/'00265530'/'00265550'/'00265580'/'002655D0'/'00265600'/'00265630'/'00265660'; '002E6300''s 'js' enters the head leaf with 'rcx' still the actor | 1 (static) | PROVEN | | '002627C0' copies the '0x80' steering record from slot '+0xDC' to slot '+0xDC+1' |"

```
00265550  movzx    eax, byte ptr [rcx + 3]
00265554  and      al, 0xe0
00265556  cmp      al, 0x60
00265558  je       0x26555e  ; -> 0026555E
0026555A  xorps    xmm0, xmm0
0026555D  ret      
0026555E  mov      rdx, qword ptr [rcx + 0xb8]
00265565  movsx    rcx, byte ptr [rdx + 0xdc]
0026556D  shl      rcx, 7
00265571  movss    xmm0, dword ptr [rcx + rdx + 0x154]
0026557A  ret      
```

## 00265580 (78 B, extent 00265580-002655CE)

Page context: "rd '+0x34' float, slot-'edx' (clamped) record '+0x34', 'sub[+0x62]>>6 &1', 'sub[+0x28]&0x7F', 'cvttss2si(sub[+0x78])', 'movsx(sub[+0x68])' | whole cluster; leaves at '00265510'/'00265530'/'00265550'/'00265580'/'002655D0'/'00265600'/'00265630'/'00265660'; '002E6300''s 'js' enters the head leaf with 'rcx' still the actor | 1 (static) | PROVEN | | '002627C0' copies the '0x80' steering record from slot '+0xDC' to slot '+0xDC+1' | 'movsx rax"

```
00265580  movzx    eax, byte ptr [rcx + 3]
00265584  and      al, 0xe0
00265586  cmp      al, 0x60
00265588  je       0x26558e  ; -> 0026558E
0026558A  xorps    xmm0, xmm0
0026558D  ret      
0026558E  mov      rcx, qword ptr [rcx + 0xb8]
00265595  test     edx, edx
00265597  jns      0x2655b1  ; -> 002655B1
00265599  movsx    edx, byte ptr [rcx + 0xdc]
002655A0  movsxd   rax, edx
002655A3  shl      rax, 7
002655A7  movss    xmm0, dword ptr [rax + rcx + 0x154]
002655B0  ret      
002655B1  movsx    eax, byte ptr [rcx + 0xdc]
002655B8  cmp      edx, eax
002655BA  cmovg    edx, eax
002655BD  movsxd   rax, edx
002655C0  shl      rax, 7
002655C4  movss    xmm0, dword ptr [rax + rcx + 0x154]
002655CD  ret      
```

## 00265600 (35 B, extent 00265600-00265623)

Page context: "-'edx' (clamped) record '+0x34', 'sub[+0x62]>>6 &1', 'sub[+0x28]&0x7F', 'cvttss2si(sub[+0x78])', 'movsx(sub[+0x68])' | whole cluster; leaves at '00265510'/'00265530'/'00265550'/'00265580'/'002655D0'/'00265600'/'00265630'/'00265660'; '002E6300''s 'js' enters the head leaf with 'rcx' still the actor | 1 (static) | PROVEN | | '002627C0' copies the '0x80' steering record from slot '+0xDC' to slot '+0xDC+1' | 'movsx rax, byte[rcx+0xDC]' / 'i"

```
00265600  movzx    eax, byte ptr [rcx + 3]
00265604  and      al, 0xe0
00265606  cmp      al, 0x60
00265608  je       0x26560d  ; -> 0026560D
0026560A  xor      eax, eax
0026560C  ret      
0026560D  mov      rax, qword ptr [rcx + 0xb8]
00265614  mov      rcx, qword ptr [rax + 0xf0]
0026561B  movzx    eax, byte ptr [rcx + 0x28]
0026561F  and      eax, 0x7f
00265622  ret      
```

## 0026A9C0 (97 B, extent 0026A9C0-0026AA21)

Page context: "B2A0'/'003DBDC0' rows | 1 (static) | PROVEN | | '002EC140' stamps resume shape 2: kind-3 gate, raw '{xmm1,xmm2}' into 'sub+0x10'/'+0x14', '+0x62 = (&0xFA) or 2', then '0026A8E0'/'0026A870' apply and '0026A9C0'/'0026A950' zero | '002EC140'–'002EC1BE' whole body; the '&0xFA or 2' store at '002EC186'–'002EC18A' | 1 (static) | PROVEN | | '002EC1C0' stamps resume shape 3: two-sided wrap (±π offset by arg sign, mod 2π) of '{xmm1,xmm2}' into '"

```
0026A9C0  movaps   xmm3, xmm1
0026A9C3  xorps    xmm0, xmm0
0026A9C6  comiss   xmm3, xmm0
0026A9C9  jb       0x26a9d5  ; -> 0026A9D5
0026A9CB  movss    xmm4, dword ptr [rip + 0x1a8127d]  ; -> 01CEBC50 [f32 3.141593]
0026A9D3  jmp      0x26a9dd  ; -> 0026A9DD
0026A9D5  movss    xmm4, dword ptr [rip + 0x6aac43]  ; -> 00915620 [f32 -3.141593]
0026A9DD  movzx    eax, byte ptr [rcx + 3]
0026A9E1  addss    xmm3, xmm4
0026A9E5  and      al, 0xe0
0026A9E7  cmp      al, 0x60
0026A9E9  jne      0x26aa20  ; -> 0026AA20
0026A9EB  movaps   xmm0, xmm3
0026A9EE  divss    xmm0, dword ptr [rip + 0x1a81282]  ; -> 01CEBC78 [f32 6.283185]
0026A9F6  cvttss2si eax, xmm0
0026A9FA  movd     xmm1, eax
0026A9FE  mov      rax, qword ptr [rcx + 0xb8]
0026AA05  cvtdq2ps xmm1, xmm1
0026AA08  mulss    xmm1, dword ptr [rip + 0x1a81268]  ; -> 01CEBC78 [f32 6.283185]
0026AA10  subss    xmm3, xmm1
0026AA14  subss    xmm3, xmm4
0026AA18  movss    dword ptr [rax + 0xb4], xmm3
0026AA20  ret      
```

## 002EDB30 (72 B, extent 002EDB30-002EDB78)

Page context: "chor '002EC3A4' (function '002EC380').  '002E7A80' (178 B) is the pair-link commit '002EBFA0' runs for two facing records: each argument's '[+0xC0]' block must resolve with a '[0] != -1' head before '002EDB30' is invoked ('ecx = word[rcx-block]', 'edx = 0', 'r8d = [rdx-block]'); afterwards, when 'rbx''s own block carries a live 'u16' index, its 'idx * 0x740 + [022C6F28]' row with '[+0x284] != 0' is committed - '003E6C00(row, 1, 0x30B)' "

```
002EDB30  sub      rsp, 0x28
002EDB34  cmp      cx, -1
002EDB38  je       0x2edb73  ; -> 002EDB73
002EDB3A  mov      qword ptr [rsp + 0x20], rbx
002EDB3F  movsx    rax, cx
002EDB43  imul     rbx, rax, 0x740
002EDB4A  add      rbx, qword ptr [rip + 0x1fd93d7]  ; -> 022C6F28
002EDB51  je       0x2edb6e  ; -> 002EDB6E
002EDB53  cmp      dword ptr [rbx + 0x284], 0
002EDB5A  je       0x2edb6e  ; -> 002EDB6E
002EDB5C  mov      rcx, rbx
002EDB5F  call     0x3e6c00  ; -> 003E6C00 fn
002EDB64  or       dword ptr [rbx + 0x290], 0x800
002EDB6E  mov      rbx, qword ptr [rsp + 0x20]
002EDB73  add      rsp, 0x28
002EDB77  ret      
```

## 00343F90 (103 B, extent 00343F90-00343FF7)

Page context: "y are not read here.  **Script VM — CLIENT.** '002EC380' is called from the script bridge ('0034EB40', '0034F470', '0034FBB0', '003520B0', '00350410', '00357C40', '00357D10', '00357BA0', '00357B10', '00343F90', '003517E0', '00351D10') — the steering-bits write is script-driven, not shared ownership. - **Input - SERVICE (1 edge).** '00263230' reaches bodies filed to input: '00226BE0' (ActorControlMaskPropagationRuntime) - shared machiner"

```
00343F90  mov      qword ptr [rsp + 8], rbx
00343F95  mov      qword ptr [rsp + 0x10], rsi
00343F9A  push     rdi
00343F9B  sub      rsp, 0x20
00343F9F  mov      rcx, r9
00343FA2  mov      rbx, r9
00343FA5  mov      rsi, rdx
00343FA8  call     0x267e10  ; -> 00267E10 fn
00343FAD  mov      rcx, rbx
00343FB0  mov      edi, eax
00343FB2  call     0x267db0  ; -> 00267DB0 fn
00343FB7  xorps    xmm2, xmm2
00343FBA  movaps   xmm1, xmm0
00343FBD  mov      rcx, rsi
00343FC0  call     0x2ec1c0  ; -> 002EC1C0 fn
00343FC5  movd     xmm2, edi
00343FC9  mov      edx, 2
00343FCE  cvtdq2ps xmm2, xmm2
00343FD1  mov      rcx, rsi
00343FD4  call     0x2ec380  ; -> 002EC380 fn
00343FD9  xor      r8d, r8d
00343FDC  mov      rcx, rsi
00343FDF  lea      edx, [r8 + 1]
00343FE3  mov      rbx, qword ptr [rsp + 0x30]
00343FE8  mov      rsi, qword ptr [rsp + 0x38]
00343FED  add      rsp, 0x20
00343FF1  pop      rdi
00343FF2  jmp      0x2ebe50  ; -> 002EBE50 fn
```

## 0034EB40 (121 B, extent 0034EB40-0034EBB9)

Page context: "nd the second reads the party focus actor's world position. They read as positional sound   panning, and they are not read here.  **Script VM — CLIENT.** '002EC380' is called from the script bridge ('0034EB40', '0034F470', '0034FBB0', '003520B0', '00350410', '00357C40', '00357D10', '00357BA0', '00357B10', '00343F90', '003517E0', '00351D10') — the steering-bits write is script-driven, not shared ownership. - **Input - SERVICE (1 edge).**"

```
0034EB40  mov      qword ptr [rsp + 8], rbx
0034EB45  push     rdi
0034EB46  sub      rsp, 0x40
0034EB4A  movaps   xmmword ptr [rsp + 0x30], xmm6
0034EB4F  mov      rcx, r9
0034EB52  movaps   xmmword ptr [rsp + 0x20], xmm7
0034EB57  mov      rbx, r9
0034EB5A  mov      rdi, rdx
0034EB5D  call     0x267db0  ; -> 00267DB0 fn
0034EB62  mov      rcx, rbx
0034EB65  movaps   xmm6, xmm0
0034EB68  call     0x267db0  ; -> 00267DB0 fn
0034EB6D  movaps   xmm1, xmm6
0034EB70  mov      rcx, rdi
0034EB73  movaps   xmm7, xmm0
0034EB76  call     0x26aad0  ; -> 0026AAD0 fn
0034EB7B  xorps    xmm2, xmm2
0034EB7E  movaps   xmm1, xmm7
0034EB81  mov      rcx, rdi
0034EB84  call     0x2ec1c0  ; -> 002EC1C0 fn
0034EB89  xorps    xmm2, xmm2
0034EB8C  xor      edx, edx
0034EB8E  mov      rcx, rdi
0034EB91  call     0x2ec380  ; -> 002EC380 fn
0034EB96  xor      r8d, r8d
0034EB99  mov      rcx, rdi
0034EB9C  lea      edx, [r8 + 1]
0034EBA0  mov      rbx, qword ptr [rsp + 0x50]
0034EBA5  movaps   xmm6, xmmword ptr [rsp + 0x30]
0034EBAA  movaps   xmm7, xmmword ptr [rsp + 0x20]
0034EBAF  add      rsp, 0x40
0034EBB3  pop      rdi
0034EBB4  jmp      0x2ebe50  ; -> 002EBE50 fn
```

## 0034F470 (121 B, extent 0034F470-0034F4E9)

Page context: "d reads the party focus actor's world position. They read as positional sound   panning, and they are not read here.  **Script VM — CLIENT.** '002EC380' is called from the script bridge ('0034EB40', '0034F470', '0034FBB0', '003520B0', '00350410', '00357C40', '00357D10', '00357BA0', '00357B10', '00343F90', '003517E0', '00351D10') — the steering-bits write is script-driven, not shared ownership. - **Input - SERVICE (1 edge).** '00263230' "

```
0034F470  mov      qword ptr [rsp + 8], rbx
0034F475  push     rdi
0034F476  sub      rsp, 0x40
0034F47A  movaps   xmmword ptr [rsp + 0x30], xmm6
0034F47F  mov      rcx, r9
0034F482  movaps   xmmword ptr [rsp + 0x20], xmm7
0034F487  mov      rbx, r9
0034F48A  mov      rdi, rdx
0034F48D  call     0x267db0  ; -> 00267DB0 fn
0034F492  mov      rcx, rbx
0034F495  movaps   xmm6, xmm0
0034F498  call     0x267db0  ; -> 00267DB0 fn
0034F49D  movaps   xmm1, xmm6
0034F4A0  mov      rcx, rdi
0034F4A3  movaps   xmm7, xmm0
0034F4A6  call     0x26aad0  ; -> 0026AAD0 fn
0034F4AB  xorps    xmm2, xmm2
0034F4AE  movaps   xmm1, xmm7
0034F4B1  mov      rcx, rdi
0034F4B4  call     0x2ec140  ; -> 002EC140 fn
0034F4B9  xorps    xmm2, xmm2
0034F4BC  xor      edx, edx
0034F4BE  mov      rcx, rdi
0034F4C1  call     0x2ec380  ; -> 002EC380 fn
0034F4C6  xor      r8d, r8d
0034F4C9  mov      rcx, rdi
0034F4CC  lea      edx, [r8 + 1]
0034F4D0  mov      rbx, qword ptr [rsp + 0x50]
0034F4D5  movaps   xmm6, xmmword ptr [rsp + 0x30]
0034F4DA  movaps   xmm7, xmmword ptr [rsp + 0x20]
0034F4DF  add      rsp, 0x40
0034F4E3  pop      rdi
0034F4E4  jmp      0x2ebe50  ; -> 002EBE50 fn
```

## 0034FBB0 (146 B, extent 0034FBB0-0034FC42)

Page context: "party focus actor's world position. They read as positional sound   panning, and they are not read here.  **Script VM — CLIENT.** '002EC380' is called from the script bridge ('0034EB40', '0034F470', '0034FBB0', '003520B0', '00350410', '00357C40', '00357D10', '00357BA0', '00357B10', '00343F90', '003517E0', '00351D10') — the steering-bits write is script-driven, not shared ownership. - **Input - SERVICE (1 edge).** '00263230' reaches bodi"

```
0034FBB0  mov      qword ptr [rsp + 8], rbx
0034FBB5  push     rdi
0034FBB6  sub      rsp, 0x50
0034FBBA  movaps   xmmword ptr [rsp + 0x40], xmm6
0034FBBF  mov      rcx, r9
0034FBC2  movaps   xmmword ptr [rsp + 0x30], xmm7
0034FBC7  mov      rbx, r9
0034FBCA  movaps   xmmword ptr [rsp + 0x20], xmm8
0034FBD0  mov      rdi, rdx
0034FBD3  call     0x267db0  ; -> 00267DB0 fn
0034FBD8  mov      rcx, rbx
0034FBDB  movaps   xmm7, xmm0
0034FBDE  call     0x267db0  ; -> 00267DB0 fn
0034FBE3  mov      rcx, rbx
0034FBE6  movaps   xmm8, xmm0
0034FBEA  call     0x267db0  ; -> 00267DB0 fn
0034FBEF  movaps   xmm1, xmm7
0034FBF2  mov      rcx, rdi
0034FBF5  movaps   xmm6, xmm0
0034FBF8  call     0x26aad0  ; -> 0026AAD0 fn
0034FBFD  movaps   xmm2, xmm8
0034FC01  movaps   xmm1, xmm6
0034FC04  mov      rcx, rdi
0034FC07  call     0x2ec140  ; -> 002EC140 fn
0034FC0C  xorps    xmm2, xmm2
0034FC0F  xor      edx, edx
0034FC11  mov      rcx, rdi
0034FC14  call     0x2ec380  ; -> 002EC380 fn
0034FC19  xor      r8d, r8d
0034FC1C  mov      rcx, rdi
0034FC1F  lea      edx, [r8 + 1]
0034FC23  mov      rbx, qword ptr [rsp + 0x60]
0034FC28  movaps   xmm6, xmmword ptr [rsp + 0x40]
0034FC2D  movaps   xmm7, xmmword ptr [rsp + 0x30]
0034FC32  movaps   xmm8, xmmword ptr [rsp + 0x20]
0034FC38  add      rsp, 0x50
0034FC3C  pop      rdi
0034FC3D  jmp      0x2ebe50  ; -> 002EBE50 fn
```

## 00350410 (146 B, extent 00350410-003504A2)

Page context: "d position. They read as positional sound   panning, and they are not read here.  **Script VM — CLIENT.** '002EC380' is called from the script bridge ('0034EB40', '0034F470', '0034FBB0', '003520B0', '00350410', '00357C40', '00357D10', '00357BA0', '00357B10', '00343F90', '003517E0', '00351D10') — the steering-bits write is script-driven, not shared ownership. - **Input - SERVICE (1 edge).** '00263230' reaches bodies filed to input: '0022"

```
00350410  mov      qword ptr [rsp + 8], rbx
00350415  push     rdi
00350416  sub      rsp, 0x50
0035041A  movaps   xmmword ptr [rsp + 0x40], xmm6
0035041F  mov      rcx, r9
00350422  movaps   xmmword ptr [rsp + 0x30], xmm7
00350427  mov      rbx, r9
0035042A  movaps   xmmword ptr [rsp + 0x20], xmm8
00350430  mov      rdi, rdx
00350433  call     0x267db0  ; -> 00267DB0 fn
00350438  mov      rcx, rbx
0035043B  movaps   xmm7, xmm0
0035043E  call     0x267db0  ; -> 00267DB0 fn
00350443  mov      rcx, rbx
00350446  movaps   xmm8, xmm0
0035044A  call     0x267db0  ; -> 00267DB0 fn
0035044F  movaps   xmm1, xmm7
00350452  mov      rcx, rdi
00350455  movaps   xmm6, xmm0
00350458  call     0x26aad0  ; -> 0026AAD0 fn
0035045D  movaps   xmm2, xmm8
00350461  movaps   xmm1, xmm6
00350464  mov      rcx, rdi
00350467  call     0x2ec1c0  ; -> 002EC1C0 fn
0035046C  xorps    xmm2, xmm2
0035046F  xor      edx, edx
00350471  mov      rcx, rdi
00350474  call     0x2ec380  ; -> 002EC380 fn
00350479  xor      r8d, r8d
0035047C  mov      rcx, rdi
0035047F  lea      edx, [r8 + 1]
00350483  mov      rbx, qword ptr [rsp + 0x60]
00350488  movaps   xmm6, xmmword ptr [rsp + 0x40]
0035048D  movaps   xmm7, xmmword ptr [rsp + 0x30]
00350492  movaps   xmm8, xmmword ptr [rsp + 0x20]
00350498  add      rsp, 0x50
0035049C  pop      rdi
0035049D  jmp      0x2ebe50  ; -> 002EBE50 fn
```

## 003517E0 (100 B, extent 003517E0-00351844)

Page context: "ad here.  **Script VM — CLIENT.** '002EC380' is called from the script bridge ('0034EB40', '0034F470', '0034FBB0', '003520B0', '00350410', '00357C40', '00357D10', '00357BA0', '00357B10', '00343F90', '003517E0', '00351D10') — the steering-bits write is script-driven, not shared ownership. - **Input - SERVICE (1 edge).** '00263230' reaches bodies filed to input: '00226BE0' (ActorControlMaskPropagationRuntime) - shared machinery across the"

```
003517E0  mov      qword ptr [rsp + 8], rbx
003517E5  push     rdi
003517E6  sub      rsp, 0x30
003517EA  mov      rcx, r9
003517ED  movaps   xmmword ptr [rsp + 0x20], xmm6
003517F2  mov      rbx, r9
003517F5  mov      rdi, rdx
003517F8  call     0x267db0  ; -> 00267DB0 fn
003517FD  mov      rcx, rbx
00351800  movaps   xmm6, xmm0
00351803  call     0x267db0  ; -> 00267DB0 fn
00351808  xorps    xmm2, xmm2
0035180B  movaps   xmm1, xmm0
0035180E  mov      rcx, rdi
00351811  call     0x2ec140  ; -> 002EC140 fn
00351816  movaps   xmm2, xmm6
00351819  mov      edx, 2
0035181E  mov      rcx, rdi
00351821  call     0x2ec380  ; -> 002EC380 fn
00351826  xor      r8d, r8d
00351829  mov      rcx, rdi
0035182C  lea      edx, [r8 + 1]
00351830  mov      rbx, qword ptr [rsp + 0x40]
00351835  movaps   xmm6, xmmword ptr [rsp + 0x20]
0035183A  add      rsp, 0x30
0035183E  pop      rdi
0035183F  jmp      0x2ebe50  ; -> 002EBE50 fn
```

## 00351D10 (121 B, extent 00351D10-00351D89)

Page context: "Script VM — CLIENT.** '002EC380' is called from the script bridge ('0034EB40', '0034F470', '0034FBB0', '003520B0', '00350410', '00357C40', '00357D10', '00357BA0', '00357B10', '00343F90', '003517E0', '00351D10') — the steering-bits write is script-driven, not shared ownership. - **Input - SERVICE (1 edge).** '00263230' reaches bodies filed to input: '00226BE0' (ActorControlMaskPropagationRuntime) - shared machinery across the layer bound"

```
00351D10  mov      qword ptr [rsp + 8], rbx
00351D15  push     rdi
00351D16  sub      rsp, 0x40
00351D1A  movaps   xmmword ptr [rsp + 0x30], xmm6
00351D1F  mov      rcx, r9
00351D22  movaps   xmmword ptr [rsp + 0x20], xmm7
00351D27  mov      rbx, r9
00351D2A  mov      rdi, rdx
00351D2D  call     0x267db0  ; -> 00267DB0 fn
00351D32  mov      rcx, rbx
00351D35  movaps   xmm7, xmm0
00351D38  call     0x267db0  ; -> 00267DB0 fn
00351D3D  mov      rcx, rbx
00351D40  movaps   xmm6, xmm0
00351D43  call     0x267db0  ; -> 00267DB0 fn
00351D48  movaps   xmm2, xmm6
00351D4B  movaps   xmm1, xmm0
00351D4E  mov      rcx, rdi
00351D51  call     0x2ec140  ; -> 002EC140 fn
00351D56  movaps   xmm2, xmm7
00351D59  mov      edx, 2
00351D5E  mov      rcx, rdi
00351D61  call     0x2ec380  ; -> 002EC380 fn
00351D66  xor      r8d, r8d
00351D69  mov      rcx, rdi
00351D6C  lea      edx, [r8 + 1]
00351D70  mov      rbx, qword ptr [rsp + 0x50]
00351D75  movaps   xmm6, xmmword ptr [rsp + 0x30]
00351D7A  movaps   xmm7, xmmword ptr [rsp + 0x20]
00351D7F  add      rsp, 0x40
00351D83  pop      rdi
00351D84  jmp      0x2ebe50  ; -> 002EBE50 fn
```

## 003520B0 (121 B, extent 003520B0-00352129)

Page context: "actor's world position. They read as positional sound   panning, and they are not read here.  **Script VM — CLIENT.** '002EC380' is called from the script bridge ('0034EB40', '0034F470', '0034FBB0', '003520B0', '00350410', '00357C40', '00357D10', '00357BA0', '00357B10', '00343F90', '003517E0', '00351D10') — the steering-bits write is script-driven, not shared ownership. - **Input - SERVICE (1 edge).** '00263230' reaches bodies filed to "

```
003520B0  mov      qword ptr [rsp + 8], rbx
003520B5  push     rdi
003520B6  sub      rsp, 0x40
003520BA  movaps   xmmword ptr [rsp + 0x30], xmm6
003520BF  mov      rcx, r9
003520C2  movaps   xmmword ptr [rsp + 0x20], xmm7
003520C7  mov      rbx, r9
003520CA  mov      rdi, rdx
003520CD  call     0x267db0  ; -> 00267DB0 fn
003520D2  mov      rcx, rbx
003520D5  movaps   xmm7, xmm0
003520D8  call     0x267db0  ; -> 00267DB0 fn
003520DD  mov      rcx, rbx
003520E0  movaps   xmm6, xmm0
003520E3  call     0x267db0  ; -> 00267DB0 fn
003520E8  movaps   xmm2, xmm6
003520EB  movaps   xmm1, xmm0
003520EE  mov      rcx, rdi
003520F1  call     0x2ec1c0  ; -> 002EC1C0 fn
003520F6  movaps   xmm2, xmm7
003520F9  mov      edx, 2
003520FE  mov      rcx, rdi
00352101  call     0x2ec380  ; -> 002EC380 fn
00352106  xor      r8d, r8d
00352109  mov      rcx, rdi
0035210C  lea      edx, [r8 + 1]
00352110  mov      rbx, qword ptr [rsp + 0x50]
00352115  movaps   xmm6, xmmword ptr [rsp + 0x30]
0035211A  movaps   xmm7, xmmword ptr [rsp + 0x20]
0035211F  add      rsp, 0x40
00352123  pop      rdi
00352124  jmp      0x2ebe50  ; -> 002EBE50 fn
```

## 00357B10 (143 B, extent 00357B10-00357B9F)

Page context: "ing, and they are not read here.  **Script VM — CLIENT.** '002EC380' is called from the script bridge ('0034EB40', '0034F470', '0034FBB0', '003520B0', '00350410', '00357C40', '00357D10', '00357BA0', '00357B10', '00343F90', '003517E0', '00351D10') — the steering-bits write is script-driven, not shared ownership. - **Input - SERVICE (1 edge).** '00263230' reaches bodies filed to input: '00226BE0' (ActorControlMaskPropagationRuntime) - sha"

```
00357B10  mov      qword ptr [rsp + 8], rbx
00357B15  mov      qword ptr [rsp + 0x10], rsi
00357B1A  push     rdi
00357B1B  sub      rsp, 0x30
00357B1F  movaps   xmmword ptr [rsp + 0x20], xmm6
00357B24  mov      rbx, r9
00357B27  mov      rdi, rdx
00357B2A  call     0x2640c0  ; -> 002640C0 fn
00357B2F  mov      rcx, rbx
00357B32  call     0x267db0  ; -> 00267DB0 fn
00357B37  mov      rcx, rbx
00357B3A  movaps   xmm6, xmm0
00357B3D  call     0x267e10  ; -> 00267E10 fn
00357B42  mov      rcx, rbx
00357B45  mov      esi, eax
00357B47  call     0x267e10  ; -> 00267E10 fn
00357B4C  mov      ecx, eax
00357B4E  call     0x264010  ; -> 00264010 fn
00357B53  test     rax, rax
00357B56  je       0x357b8a  ; -> 00357B8A
00357B58  movzx    r8d, word ptr [rax]
00357B5C  mov      r9d, esi
00357B5F  movzx    edx, byte ptr [rax + 0x15]
00357B63  mov      rcx, rdi
00357B66  call     0x2ebfa0  ; -> 002EBFA0 fn
00357B6B  movaps   xmm2, xmm6
00357B6E  mov      edx, 2
00357B73  mov      rcx, rdi
00357B76  call     0x2ec380  ; -> 002EC380 fn
00357B7B  xor      r8d, r8d
00357B7E  mov      rcx, rdi
00357B81  lea      edx, [r8 + 1]
00357B85  call     0x2ebe50  ; -> 002EBE50 fn
00357B8A  mov      rbx, qword ptr [rsp + 0x40]
00357B8F  mov      rsi, qword ptr [rsp + 0x48]
00357B94  movaps   xmm6, xmmword ptr [rsp + 0x20]
00357B99  add      rsp, 0x30
00357B9D  pop      rdi
00357B9E  ret      
```

## 00357BA0 (149 B, extent 00357BA0-00357C35)

Page context: "sound   panning, and they are not read here.  **Script VM — CLIENT.** '002EC380' is called from the script bridge ('0034EB40', '0034F470', '0034FBB0', '003520B0', '00350410', '00357C40', '00357D10', '00357BA0', '00357B10', '00343F90', '003517E0', '00351D10') — the steering-bits write is script-driven, not shared ownership. - **Input - SERVICE (1 edge).** '00263230' reaches bodies filed to input: '00226BE0' (ActorControlMaskPropagationRu"

```
00357BA0  mov      qword ptr [rsp + 8], rbx
00357BA5  mov      qword ptr [rsp + 0x10], rsi
00357BAA  push     rdi
00357BAB  sub      rsp, 0x30
00357BAF  mov      rcx, r9
00357BB2  movaps   xmmword ptr [rsp + 0x20], xmm6
00357BB7  mov      rbx, r9
00357BBA  mov      rdi, rdx
00357BBD  call     0x267db0  ; -> 00267DB0 fn
00357BC2  mov      rcx, rbx
00357BC5  movaps   xmm6, xmm0
00357BC8  call     0x267e10  ; -> 00267E10 fn
00357BCD  mov      rcx, rbx
00357BD0  mov      esi, eax
00357BD2  call     0x267e10  ; -> 00267E10 fn
00357BD7  mov      ecx, eax
00357BD9  call     0x264010  ; -> 00264010 fn
00357BDE  mov      rbx, rax
00357BE1  test     rax, rax
00357BE4  je       0x357c20  ; -> 00357C20
00357BE6  movaps   xmm1, xmm6
00357BE9  mov      rcx, rdi
00357BEC  call     0x26aad0  ; -> 0026AAD0 fn
00357BF1  movzx    r8d, word ptr [rbx]
00357BF5  mov      r9d, esi
00357BF8  movzx    edx, byte ptr [rbx + 0x15]
00357BFC  mov      rcx, rdi
00357BFF  call     0x2ebfa0  ; -> 002EBFA0 fn
00357C04  xorps    xmm2, xmm2
00357C07  xor      edx, edx
00357C09  mov      rcx, rdi
00357C0C  call     0x2ec380  ; -> 002EC380 fn
00357C11  xor      r8d, r8d
00357C14  mov      rcx, rdi
00357C17  lea      edx, [r8 + 1]
00357C1B  call     0x2ebe50  ; -> 002EBE50 fn
00357C20  mov      rbx, qword ptr [rsp + 0x40]
00357C25  mov      rsi, qword ptr [rsp + 0x48]
00357C2A  movaps   xmm6, xmmword ptr [rsp + 0x20]
00357C2F  add      rsp, 0x30
00357C33  pop      rdi
00357C34  ret      
```

## 00357C40 (193 B, extent 00357C40-00357D01)

Page context: "They read as positional sound   panning, and they are not read here.  **Script VM — CLIENT.** '002EC380' is called from the script bridge ('0034EB40', '0034F470', '0034FBB0', '003520B0', '00350410', '00357C40', '00357D10', '00357BA0', '00357B10', '00343F90', '003517E0', '00351D10') — the steering-bits write is script-driven, not shared ownership. - **Input - SERVICE (1 edge).** '00263230' reaches bodies filed to input: '00226BE0' (Actor"

```
00357C40  mov      qword ptr [rsp + 8], rbx
00357C45  push     rdi
00357C46  sub      rsp, 0x50
00357C4A  movaps   xmmword ptr [rsp + 0x40], xmm6
00357C4F  mov      rax, qword ptr [rip + 0x1becbda]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00357C56  xor      rax, rsp
00357C59  mov      qword ptr [rsp + 0x30], rax
00357C5E  movss    xmm0, dword ptr [rip + 0x1993f42]  ; -> 01CEBBA8 [f32 1]
00357C66  mov      rcx, r9
00357C69  movss    dword ptr [rsp + 0x2c], xmm0
00357C6F  mov      rbx, r9
00357C72  mov      rdi, rdx
00357C75  call     0x267db0  ; -> 00267DB0 fn
00357C7A  mov      rcx, rbx
00357C7D  movaps   xmm6, xmm0
00357C80  call     0x267db0  ; -> 00267DB0 fn
00357C85  mov      rcx, rdi
00357C88  movss    dword ptr [rsp + 0x28], xmm0
00357C8E  call     0x263d00  ; -> 00263D00 fn
00357C93  test     eax, eax
00357C95  jne      0x357ca1  ; -> 00357CA1
00357C97  mov      rcx, rbx
00357C9A  call     0x267db0  ; -> 00267DB0 fn
00357C9F  jmp      0x357ca4  ; -> 00357CA4
00357CA1  xorps    xmm0, xmm0
00357CA4  mov      rcx, rbx
00357CA7  movss    dword ptr [rsp + 0x24], xmm0
00357CAD  call     0x267db0  ; -> 00267DB0 fn
00357CB2  lea      rdx, [rsp + 0x20]
00357CB7  movss    dword ptr [rsp + 0x20], xmm0
00357CBD  mov      rcx, rdi
00357CC0  call     0x2ec2c0  ; -> 002EC2C0 fn
00357CC5  movaps   xmm2, xmm6
00357CC8  mov      edx, 2
00357CCD  mov      rcx, rdi
00357CD0  call     0x2ec380  ; -> 002EC380 fn
00357CD5  xor      r8d, r8d
00357CD8  mov      rcx, rdi
00357CDB  lea      edx, [r8 + 1]
00357CDF  call     0x2ebe50  ; -> 002EBE50 fn
00357CE4  mov      rcx, qword ptr [rsp + 0x30]
00357CE9  xor      rcx, rsp
00357CEC  call     0x808c40  ; -> 00808C40 fn
00357CF1  mov      rbx, qword ptr [rsp + 0x60]
00357CF6  movaps   xmm6, xmmword ptr [rsp + 0x40]
00357CFB  add      rsp, 0x50
00357CFF  pop      rdi
00357D00  ret      
```

## 00357D10 (206 B, extent 00357D10-00357DDE)

Page context: " positional sound   panning, and they are not read here.  **Script VM — CLIENT.** '002EC380' is called from the script bridge ('0034EB40', '0034F470', '0034FBB0', '003520B0', '00350410', '00357C40', '00357D10', '00357BA0', '00357B10', '00343F90', '003517E0', '00351D10') — the steering-bits write is script-driven, not shared ownership. - **Input - SERVICE (1 edge).** '00263230' reaches bodies filed to input: '00226BE0' (ActorControlMaskP"

```
00357D10  mov      qword ptr [rsp + 8], rbx
00357D15  push     rdi
00357D16  sub      rsp, 0x50
00357D1A  movaps   xmmword ptr [rsp + 0x40], xmm6
00357D1F  mov      rax, qword ptr [rip + 0x1becb0a]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00357D26  xor      rax, rsp
00357D29  mov      qword ptr [rsp + 0x30], rax
00357D2E  mov      rcx, r9
00357D31  mov      rbx, r9
00357D34  mov      rdi, rdx
00357D37  call     0x267db0  ; -> 00267DB0 fn
00357D3C  movss    xmm1, dword ptr [rip + 0x1993e64]  ; -> 01CEBBA8 [f32 1]
00357D44  mov      rcx, rbx
00357D47  movss    dword ptr [rsp + 0x2c], xmm1
00357D4D  movaps   xmm6, xmm0
00357D50  call     0x267db0  ; -> 00267DB0 fn
00357D55  mov      rcx, rdi
00357D58  movss    dword ptr [rsp + 0x28], xmm0
00357D5E  call     0x263d00  ; -> 00263D00 fn
00357D63  test     eax, eax
00357D65  jne      0x357d77  ; -> 00357D77
00357D67  mov      rcx, rbx
00357D6A  call     0x267db0  ; -> 00267DB0 fn
00357D6F  movss    dword ptr [rsp + 0x24], xmm0
00357D75  jmp      0x357d7f  ; -> 00357D7F
00357D77  mov      dword ptr [rsp + 0x24], 0
00357D7F  mov      rcx, rbx
00357D82  call     0x267db0  ; -> 00267DB0 fn
00357D87  movaps   xmm1, xmm6
00357D8A  movss    dword ptr [rsp + 0x20], xmm0
00357D90  mov      rcx, rdi
00357D93  call     0x26aad0  ; -> 0026AAD0 fn
00357D98  lea      rdx, [rsp + 0x20]
00357D9D  mov      rcx, rdi
00357DA0  call     0x2ec2c0  ; -> 002EC2C0 fn
00357DA5  xorps    xmm2, xmm2
00357DA8  xor      edx, edx
00357DAA  mov      rcx, rdi
00357DAD  call     0x2ec380  ; -> 002EC380 fn
00357DB2  xor      r8d, r8d
00357DB5  mov      rcx, rdi
00357DB8  lea      edx, [r8 + 1]
00357DBC  call     0x2ebe50  ; -> 002EBE50 fn
00357DC1  mov      rcx, qword ptr [rsp + 0x30]
00357DC6  xor      rcx, rsp
00357DC9  call     0x808c40  ; -> 00808C40 fn
00357DCE  mov      rbx, qword ptr [rsp + 0x60]
00357DD3  movaps   xmm6, xmmword ptr [rsp + 0x40]
00357DD8  add      rsp, 0x50
00357DDC  pop      rdi
00357DDD  ret      
```
