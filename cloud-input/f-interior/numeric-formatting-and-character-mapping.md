# F-interior pack: `16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/numeric-formatting-and-character-mapping.json`.

Functions: 10. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 54e8a524e	SWE2-FRONTIER for FABLE: pass-22 unattributed appends - verifier + 23 of 34 PUBLISHABLE pages (batch; inbox mentions: FABLE.md, repos-78.md, repos-9e.md). OPUS read these before packing.

## 001E0C30 (25 B, extent 001E0C30-001E0C49)

Page context: " ('002A2940'), InputGameplay_GetActorStateAwareRemappedMask0C ('002A29A0'), InputGameplay_GetActorStateAwareRemappedMask10 ('002A2A00') (+6 more) reach bodies filed to Input: '001E0A10', '001E0C10', '001E0C30', '001E0E30' (+10 more) - shared machinery across the layer boundary, no shared ownership. - **Resource - SERVICE (4 edges).** '002A7A40', '00579AF0' reach bodies filed to Resource: '00249580', '0024A680', '003933F0', '00393460' - "

```
001E0C30  sub      rsp, 0x28
001E0C34  call     0x796e20  ; -> 00796E20 fn
001E0C39  mov      rcx, qword ptr [rax + 0xdf8]
001E0C40  add      rsp, 0x28
001E0C44  jmp      0x225680  ; -> 00225680 fn
```

## 001E9780 (34 B, extent 001E9780-001E97A2)

Page context: "hunks: each arm fetches the shared context through '001B5FA0' (or '001B5FB0' at '0017F9A4'), passes the incoming 'ecx'/'ebx' through, and tails into a '001E9xxx' formatter — '001E9860' ('0017F8D7'), '001E9780' ('0017F8F2'), '001E9BD0' ('0017F903'), '001E9840' ('0017F939'), '005C52D0' ('0017F950'), '001E9580' ('0017F970'), '001E9610' ('0017F990').  | member | role | interior | | --- | --- | --- | | '001E9860' (51 B) | codepoint → glyph i"

```
001E9780  mov      r9, qword ptr [rcx]
001E9783  test     r9, r9
001E9786  je       0x1e979f  ; -> 001E979F
001E9788  mov      rax, qword ptr [rcx + 0x28]
001E978C  test     rax, rax
001E978F  je       0x1e979f  ; -> 001E979F
001E9791  mov      r8d, edx
001E9794  mov      rcx, r9
001E9797  mov      edx, dword ptr [rax + 0x20]
001E979A  jmp      0x1fddd0  ; -> 001FDDD0 fn
001E979F  xor      eax, eax
001E97A1  ret      
```

## 001E9BD0 (94 B, extent 001E9BD0-001E9C2E)

Page context: "he shared context through '001B5FA0' (or '001B5FB0' at '0017F9A4'), passes the incoming 'ecx'/'ebx' through, and tails into a '001E9xxx' formatter — '001E9860' ('0017F8D7'), '001E9780' ('0017F8F2'), '001E9BD0' ('0017F903'), '001E9840' ('0017F939'), '005C52D0' ('0017F950'), '001E9580' ('0017F970'), '001E9610' ('0017F990').  | member | role | interior | | --- | --- | --- | | '001E9860' (51 B) | codepoint → glyph index — 'r9=[rcx]', 'r8=[r"

```
001E9BD0  mov      qword ptr [rsp + 8], rbx
001E9BD5  push     rdi
001E9BD6  sub      rsp, 0x30
001E9BDA  mov      ebx, edx
001E9BDC  mov      rdi, rcx
001E9BDF  call     0x1b1620  ; -> 001B1620 fn
001E9BE4  test     al, al
001E9BE6  jne      0x1e9c1c  ; -> 001E9C1C
001E9BE8  mov      rcx, qword ptr [rdi]
001E9BEB  test     rcx, rcx
001E9BEE  je       0x1e9c1c  ; -> 001E9C1C
001E9BF0  movaps   xmmword ptr [rsp + 0x20], xmm6
001E9BF5  movd     xmm6, ebx
001E9BF9  cvtdq2ps xmm6, xmm6
001E9BFC  call     0x1fddb0  ; -> 001FDDB0 fn
001E9C01  divss    xmm6, xmm0
001E9C05  movaps   xmm0, xmm6
001E9C08  movaps   xmm6, xmmword ptr [rsp + 0x20]
001E9C0D  mov      rbx, qword ptr [rsp + 0x40]
001E9C12  add      rsp, 0x30
001E9C16  pop      rdi
001E9C17  jmp      0x861f4a  ; -> 00861F4A fn
001E9C1C  movd     xmm0, ebx
001E9C20  mov      rbx, qword ptr [rsp + 0x40]
001E9C25  cvtdq2ps xmm0, xmm0
001E9C28  add      rsp, 0x30
001E9C2C  pop      rdi
001E9C2D  ret      
```

## 001E9C40 (59 B, extent 001E9C40-001E9C7B)

Page context: "to 23.0.       - '0017F8C0' → '001E9860' maps a codepoint to a glyph index.       - '0017FA10' → '001E9920' begins a run.       - '0017FB00' → '001E9C80' sets the 4×4 transform.       - '0017FC90' → '001E9C40' sets the corner gradient.       - '0017FD30' → '001E9D20' selects with an owner key. - [x] **UQ-168.** What the counter capped at '0x14' counts, and what the '[rcx+0x1102]' flag gates.       ***UQ-168 narrowed 2026-09-15 (FABLE): "

```
001E9C40  movaps   xmm0, xmm2
001E9C43  movaps   xmm4, xmm1
001E9C46  mulss    xmm2, dword ptr [rsp + 0x28]
001E9C4C  mulss    xmm1, dword ptr [rsp + 0x28]
001E9C52  mulss    xmm0, xmm3
001E9C56  mulss    xmm4, xmm3
001E9C5A  movss    dword ptr [rcx + 0x137c], xmm0
001E9C62  movss    dword ptr [rcx + 0x1384], xmm2
001E9C6A  movss    dword ptr [rcx + 0x1380], xmm4
001E9C72  movss    dword ptr [rcx + 0x1388], xmm1
001E9C7A  ret      
```

## 00272CB0 (42 B, extent 00272CB0-00272CDA)

Page context: "er columns; no Party body read for this note. - **ActorEntity - CLIENT and SERVICE (13 edges).** '00203170', '00263990' are called by bodies filed to ActorEntity: '0025C230', '0025C830', '00268D10', '00272CB0' (+2 more); '002E09A0', World_UpdateSimulationTick ('00314020'), BattleAction_FindApproachGeometryAroundTarget ('00339630') reach bodies filed to ActorEntity: '0025BFB0', ActorManager_RunFieldRuntimePass ('0025D9E0'), '00263660', '"

```
00272CB0  sub      rsp, 0x28
00272CB4  test     ecx, ecx
00272CB6  jne      0x272cc4  ; -> 00272CC4
00272CB8  lea      rax, [rip + 0x1a78979]  ; -> 01CEB638
00272CBF  add      rsp, 0x28
00272CC3  ret      
00272CC4  call     0x3588b0  ; -> 003588B0 fn
00272CC9  test     rax, rax
00272CCC  je       0x272cb8  ; -> 00272CB8
00272CCE  mov      rcx, rax
00272CD1  add      rsp, 0x28
00272CD5  jmp      0x263990  ; -> 00263990 fn
```

## 002B2D60 (41 B, extent 002B2D60-002B2D89)

Page context: " 'FontBaseWidth', which place the message-log cursor and the select pointer; Y-1, ['y1-layout-key-uses.tsv'](../../_index/candidates/y1-layout-key-uses/y1-layout-key-uses.tsv))* through '00244070' / '002B2D60' / '00368360', and fills the line scratch '0209C630'. '002A6190''s case 4 chooses between them by the flag bits §5 names. The four-field group is the window's list state, named by its writers: **'+0x3BE'** (word) the scroll offset "

```
002B2D60  cmp      byte ptr [rcx + 0xb0], 0
002B2D67  jne      0x2b2d6c  ; -> 002B2D6C
002B2D69  xor      eax, eax
002B2D6B  ret      
002B2D6C  mov      eax, dword ptr [rcx + 0x10]
002B2D6F  mov      dword ptr [rdx], eax
002B2D71  mov      eax, dword ptr [rcx + 0x14]
002B2D74  mov      dword ptr [rdx + 4], eax
002B2D77  mov      eax, dword ptr [rcx + 0x18]
002B2D7A  mov      dword ptr [rdx + 8], eax
002B2D7D  mov      eax, dword ptr [rcx + 0x1c]
002B2D80  mov      dword ptr [rdx + 0xc], eax
002B2D83  mov      eax, 1
002B2D88  ret      
```

## 002B5390 (747 B, extent 002B5390-002B567B)

Page context: "ge** — [the menu screen atlas](../Menu-Screen-Atlas/the-menu-screen-atlas.md) lists it beside '00571A50' and '00579AF0' as handbook content, with dispatch ids 1, 3, 10, 12, 14, 15, 18 | '00573BE0' → '002B5390' → the hub '002B2150', from **cases 1 and 10** ('005745A6', '00574672') |       | '002B0280' | the ShaderMaterial body, 6,441 B | calls the hub directly; its six callers are '002A86A0' (a message-window helper), '002D8690' / '002D8"

```
002B5390  push     rdi
002B5392  push     r14
002B5394  sub      rsp, 0x148
002B539B  mov      rax, qword ptr [rip + 0x1c8f48e]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002B53A2  xor      rax, rsp
002B53A5  mov      qword ptr [rsp + 0x100], rax
002B53AD  mov      qword ptr [rsp + 0x28], rdx
002B53B2  mov      r14, rdx
002B53B5  mov      rdi, rcx
002B53B8  test     rcx, rcx
002B53BB  jne      0x2b53c4  ; -> 002B53C4
002B53BD  xor      eax, eax
002B53BF  jmp      0x2b563a  ; -> 002B563A
002B53C4  mov      qword ptr [rsp + 0x170], rbx
002B53CC  mov      rbx, qword ptr [rcx + 0x10]
002B53D0  mov      qword ptr [rsp + 0x138], rsi
002B53D8  movaps   xmmword ptr [rsp + 0x110], xmm6
002B53E0  mov      byte ptr [rcx + 0x27], 0
002B53E4  test     rbx, rbx
002B53E7  jne      0x2b53ec  ; -> 002B53EC
002B53E9  mov      rbx, qword ptr [rcx]
002B53EC  movsx    eax, word ptr [rcx + 0x24]
002B53F0  lea      rcx, [rsp + 0x30]
002B53F5  movd     xmm6, eax
002B53F9  cvtdq2ps xmm6, xmm6
002B53FC  call     0x2ac1e0  ; -> 002AC1E0 fn
002B5401  mov      rcx, r14
002B5404  test     r14, r14
002B5407  jne      0x2b540d  ; -> 002B540D
002B5409  mov      rcx, qword ptr [rdi + 0x18]
002B540D  call     0x39bad0  ; -> 0039BAD0 fn
002B5412  mov      rcx, qword ptr [rip + 0x1de7827]  ; -> 0209CC40
002B5419  lea      r9, [rsp + 0x24]
002B541E  mov      byte ptr [rsp + 0xd6], al
002B5425  lea      r8, [rsp + 0x20]
002B542A  mov      eax, dword ptr [rdi + 0x28]
002B542D  mov      rdx, rbx
002B5430  mov      dword ptr [rcx + 0x10d0], eax
002B5436  movzx    eax, byte ptr [rsp + 0xca]
002B543E  mov      byte ptr [rcx + 0x1104], al
002B5444  lea      rcx, [rsp + 0x30]
002B5449  call     0x2b2150  ; -> 002B2150 fn
002B544E  mov      r8, qword ptr [rip + 0x1de77eb]  ; -> 0209CC40
002B5455  cvttss2si edx, dword ptr [rsp + 0x20]
002B545B  movsxd   rsi, eax
002B545E  mov      ecx, dword ptr [r8 + 0x10d0]
002B5465  mov      dword ptr [rdi + 0x28], ecx
002B5468  cvttss2si ecx, xmm6
002B546C  cmp      edx, ecx
002B546E  jg       0x2b54b1  ; -> 002B54B1
002B5470  mov      word ptr [rdi + 0x22], si
002B5474  mov      rcx, rsi
002B5477  mov      qword ptr [rdi + 8], rbx
002B547B  movzx    eax, byte ptr [rsi + rbx]
002B547F  xor      esi, esi
002B5481  mov      byte ptr [rdi + 0x26], al
002B5484  test     al, al
002B5486  je       0x2b5491  ; -> 002B5491
002B5488  lea      rax, [rbx + 1]
002B548C  add      rax, rcx
002B548F  jmp      0x2b5494  ; -> 002B5494
002B5491  mov      rax, rsi
002B5494  mov      qword ptr [rdi + 0x10], rax
002B5498  mov      edx, 2
002B549D  cmp      byte ptr [r8 + 0x1104], 0x26
002B54A5  cmove    esi, edx
002B54A8  mov      byte ptr [rdi + 0x27], sil
002B54AC  jmp      0x2b5622  ; -> 002B5622
002B54B1  call     0x254a10  ; -> 00254A10 fn
002B54B6  test     eax, eax
002B54B8  jne      0x2b5509  ; -> 002B5509
002B54BA  mov      word ptr [rdi + 0x22], si
002B54BE  mov      rcx, rsi
002B54C1  mov      qword ptr [rdi + 8], rbx
002B54C5  movzx    eax, byte ptr [rsi + rbx]
002B54C9  xor      esi, esi
002B54CB  mov      byte ptr [rdi + 0x26], al
002B54CE  test     al, al
002B54D0  je       0x2b54db  ; -> 002B54DB
002B54D2  lea      rax, [rbx + 1]
002B54D6  add      rax, rcx
002B54D9  jmp      0x2b54de  ; -> 002B54DE
002B54DB  mov      rax, rsi
002B54DE  mov      rcx, qword ptr [rip + 0x1de775b]  ; -> 0209CC40
002B54E5  mov      edx, 2
002B54EA  mov      byte ptr [rdi + 0x27], 1
002B54EE  mov      qword ptr [rdi + 0x10], rax
002B54F2  cmp      byte ptr [rcx + 0x1104], 0x26
002B54F9  cmove    esi, edx
002B54FC  or       sil, 1
002B5500  mov      byte ptr [rdi + 0x27], sil
002B5504  jmp      0x2b5622  ; -> 002B5622
002B5509  mov      qword ptr [rsp + 0x140], rbp
002B5511  xor      esi, esi
002B5513  mov      qword ptr [rsp + 0x130], r12
002B551B  mov      ebp, esi
002B551D  mov      qword ptr [rsp + 0x128], r13
002B5525  mov      qword ptr [rsp + 0x120], r15
002B552D  test     rbx, rbx
002B5530  je       0x2b55f0  ; -> 002B55F0
002B5536  lea      rcx, [rsp + 0x30]
002B553B  call     0x2ac1e0  ; -> 002AC1E0 fn
002B5540  mov      rcx, r14
002B5543  test     r14, r14
002B5546  jne      0x2b554c  ; -> 002B554C
002B5548  mov      rcx, qword ptr [rdi + 0x18]
002B554C  call     0x39bad0  ; -> 0039BAD0 fn
002B5551  movsxd   rcx, ebp
002B5554  add      rcx, rbx
002B5557  mov      byte ptr [rsp + 0xd6], al
002B555E  call     0x2b1fb0  ; -> 002B1FB0 fn
002B5563  mov      r12d, eax
002B5566  test     eax, eax
002B5568  je       0x2b55f0  ; -> 002B55F0
002B556E  add      ebp, eax
002B5570  xor      r15b, r15b
002B5573  mov      r14d, ebp
002B5576  or       rcx, 0xffffffffffffffff
002B557A  mov      r13d, esi
002B557D  nop      dword ptr [rax]
002B5580  inc      rcx
002B5583  cmp      byte ptr [rbx + rcx], sil
002B5587  jne      0x2b5580  ; -> 002B5580
002B5589  cmp      r14, rcx
002B558C  jae      0x2b559f  ; -> 002B559F
002B558E  movzx    r15d, byte ptr [rbp + rbx]
002B5594  mov      r13d, 1
002B559A  mov      byte ptr [rbp + rbx], sil
002B559F  lea      r9, [rsp + 0x24]
002B55A4  mov      rdx, rbx
002B55A7  lea      r8, [rsp + 0x20]
002B55AC  lea      rcx, [rsp + 0x30]
002B55B1  call     0x2b2150  ; -> 002B2150 fn
002B55B6  test     r13d, r13d
002B55B9  je       0x2b55c0  ; -> 002B55C0
002B55BB  mov      byte ptr [rbp + rbx], r15b
002B55C0  movss    xmm0, dword ptr [rsp + 0x20]
002B55C6  comiss   xmm0, xmm6
002B55C9  ja       0x2b5655  ; -> 002B5655
002B55CF  mov      rax, qword ptr [rip + 0x1de766a]  ; -> 0209CC40
002B55D6  mov      r14, qword ptr [rsp + 0x28]
002B55DB  mov      ecx, dword ptr [rax + 0x10d0]
002B55E1  movsxd   rax, ebp
002B55E4  mov      dword ptr [rdi + 0x28], ecx
002B55E7  add      rax, rbx
002B55EA  jne      0x2b5536  ; -> 002B5536
002B55F0  mov      word ptr [rdi + 0x22], si
002B55F4  xor      eax, eax
002B55F6  mov      byte ptr [rdi + 0x26], sil
002B55FA  mov      qword ptr [rdi + 8], rsi
002B55FE  mov      r15, qword ptr [rsp + 0x120]
002B5606  mov      r13, qword ptr [rsp + 0x128]
002B560E  mov      r12, qword ptr [rsp + 0x130]
002B5616  mov      rbp, qword ptr [rsp + 0x140]
002B561E  mov      qword ptr [rdi + 0x10], rsi
002B5622  mov      rsi, qword ptr [rsp + 0x138]
002B562A  mov      rbx, qword ptr [rsp + 0x170]
002B5632  movaps   xmm6, xmmword ptr [rsp + 0x110]
002B563A  mov      rcx, qword ptr [rsp + 0x100]
002B5642  xor      rcx, rsp
002B5645  call     0x808c40  ; -> 00808C40 fn
002B564A  add      rsp, 0x148
002B5651  pop      r14
002B5653  pop      rdi
002B5654  ret      
002B5655  or       byte ptr [rdi + 0x27], 1
002B5659  sub      ebp, r12d
002B565C  movsxd   rdx, ebp
002B565F  add      rdx, rbx
002B5662  mov      qword ptr [rdi + 8], rbx
002B5666  mov      word ptr [rdi + 0x22], bp
002B566A  movzx    ecx, byte ptr [rdx]
002B566D  test     cl, cl
002B566F  mov      byte ptr [rdi + 0x26], cl
002B5672  cmovne   rsi, rdx
002B5676  mov      rax, rsi
002B5679  jmp      0x2b55fe  ; -> 002B55FE
```

## 002E20D0 (68 B, extent 002E20D0-002E2114)

Page context: "e count; all three pass straight through for a list of more than 32. (3) *Where that mask comes from.* The script verb **'setaskselectignore(window, index)'** ('0475', handler '00348540') tail-calls '002E20D0(window, 1, index)', which ORs '1 << index' into the dword at '+0x18' of the window's '0x68'-byte record at '0215F200' (eight windows; a zero second argument would clear the bit instead). The message-window opener '002E16B0' copies "

```
002E20D0  mov      r9d, edx
002E20D3  cmp      ecx, 8
002E20D6  jge      0x2e2113  ; -> 002E2113
002E20D8  test     ecx, ecx
002E20DA  jns      0x2e20e0  ; -> 002E20E0
002E20DC  xor      ecx, ecx
002E20DE  jmp      0x2e20ea  ; -> 002E20EA
002E20E0  mov      eax, 7
002E20E5  cmp      ecx, eax
002E20E7  cmovg    ecx, eax
002E20EA  movsxd   rax, ecx
002E20ED  mov      ecx, r8d
002E20F0  imul     rdx, rax, 0x68
002E20F4  lea      rax, [rip + 0x1e7d105]  ; -> 0215F200
002E20FB  add      rdx, rax
002E20FE  mov      eax, 1
002E2103  shl      eax, cl
002E2105  test     r9d, r9d
002E2108  je       0x2e210e  ; -> 002E210E
002E210A  or       dword ptr [rdx + 0x18], eax
002E210D  ret      
002E210E  not      eax
002E2110  and      dword ptr [rdx + 0x18], eax
002E2113  ret      
```

## 003F4330 (819 B, extent 003F4330-003F4663)

Page context: "0]'. So the values the parametric setters carry — '4' and '11' from '002A70B0', '6' from '002D66D0', '10' from '00572600', and '0xFF' remapped to '1' inside '002475D0' for '00227EE0', '00241D40' and '003F4330' — are the **widget's** byte and never index the four-group table. That distinction is load-bearing: read as drawer kinds, '4', '6', '10' and '11' would each have run off the end of a 96-byte table straight into the power-of-ten da"

```
003F4330  push     rdi
003F4332  sub      rsp, 0x30
003F4336  mov      rdi, rcx
003F4339  mov      ecx, dword ptr [rdx]
003F433B  sub      ecx, 1
003F433E  je       0x3f43f8  ; -> 003F43F8
003F4344  sub      ecx, 9
003F4347  je       0x3f43bb  ; -> 003F43BB
003F4349  sub      ecx, 4
003F434C  je       0x3f4384  ; -> 003F4384
003F434E  cmp      ecx, 4
003F4351  je       0x3f4360  ; -> 003F4360
003F4353  mov      rcx, rdi
003F4356  add      rsp, 0x30
003F435A  pop      rdi
003F435B  jmp      0x5c5230  ; -> 005C5230 fn
003F4360  mov      rcx, qword ptr [rdi + 0x120]
003F4367  test     rcx, rcx
003F436A  je       0x3f465b  ; -> 003F465B
003F4370  xor      r8d, r8d
003F4373  lea      edx, [r8 + 0x12]
003F4377  call     0x247510  ; -> 00247510 fn
003F437C  xor      eax, eax
003F437E  add      rsp, 0x30
003F4382  pop      rdi
003F4383  ret      
003F4384  mov      rax, qword ptr [rdi + 0x110]
003F438B  mov      ecx, 0x27
003F4390  test     rax, rax
003F4393  je       0x3f43a6  ; -> 003F43A6
003F4395  movzx    edx, word ptr [rax + 6]
003F4399  test     dx, dx
003F439C  je       0x3f43a6  ; -> 003F43A6
003F439E  movsx    ecx, dx
003F43A1  cmp      ecx, -1
003F43A4  je       0x3f43ab  ; -> 003F43AB
003F43A6  call     0x249c60  ; -> 00249C60 fn
003F43AB  mov      rcx, rdi
003F43AE  call     0x2470d0  ; -> 002470D0 fn
003F43B3  xor      eax, eax
003F43B5  add      rsp, 0x30
003F43B9  pop      rdi
003F43BA  ret      
003F43BB  movzx    eax, word ptr [rip + 0x1a17ee2]  ; -> 01E0C2A4 [u16 0x4000]
003F43C2  or       ax, word ptr [rip + 0x1a17ed7]  ; -> 01E0C2A0 [u16 0x2000]
003F43C9  test     word ptr [rip + 0x2ba2f9a], ax  ; -> 02F9736A
003F43D0  je       0x3f465b  ; -> 003F465B
003F43D6  mov      ecx, 3
003F43DB  call     0x249c60  ; -> 00249C60 fn
003F43E0  mov      rcx, rdi
003F43E3  call     0x2470c0  ; -> 002470C0 fn
003F43E8  mov      rcx, rdi
003F43EB  call     0x244f00  ; -> 00244F00 fn
003F43F0  xor      eax, eax
003F43F2  add      rsp, 0x30
003F43F6  pop      rdi
003F43F7  ret      
003F43F8  mov      qword ptr [rsp + 0x50], rbx
003F43FD  mov      r8d, 5
003F4403  mov      rbx, qword ptr [rdx + 8]
003F4407  mov      rcx, rdi
003F440A  mov      rax, qword ptr [rbx]
003F440D  mov      qword ptr [rdi + 0xc0], rax
003F4414  mov      rax, qword ptr [rbx + 8]
003F4418  mov      qword ptr [rdi + 0x108], rax
003F441F  mov      rax, qword ptr [rbx + 0x10]
003F4423  mov      qword ptr [rdi + 0x110], rax
003F442A  mov      rax, qword ptr [rbx + 0x18]
003F442E  mov      qword ptr [rdi + 0x120], rax
003F4435  mov      rdx, qword ptr [rbx + 0x20]
003F4439  call     0x3946b0  ; -> 003946B0 fn
003F443E  xor      edx, edx
003F4440  mov      rcx, rdi
003F4443  call     0x394700  ; -> 00394700 fn
003F4448  xor      r8d, r8d
003F444B  mov      dword ptr [rdi + 0xc8], r8d
003F4452  mov      rax, qword ptr [rbx + 8]
003F4456  test     byte ptr [rax], 1
003F4459  je       0x3f4482  ; -> 003F4482
003F445B  mov      eax, 0xffff
003F4460  mov      word ptr [rdi + 0xcc], ax
003F4467  mov      rax, qword ptr [rbx + 8]
003F446B  movsxd   rcx, dword ptr [rdi + 0xc8]
003F4472  mov      eax, dword ptr [rax + 4]
003F4475  mov      dword ptr [rdi + rcx*8 + 0xd0], eax
003F447C  inc      dword ptr [rdi + 0xc8]
003F4482  mov      rax, qword ptr [rbx + 8]
003F4486  cmp      r8w, word ptr [rax + 8]
003F448B  jae      0x3f44e2  ; -> 003F44E2
003F448D  mov      rdx, r8
003F4490  mov      rax, qword ptr [rbx + 8]
003F4494  movsxd   rcx, dword ptr [rdi + 0xc8]
003F449B  movzx    eax, word ptr [rdx + rax + 0xc]
003F44A0  mov      word ptr [rdi + rcx*8 + 0xcc], ax
003F44A8  mov      rax, qword ptr [rbx + 8]
003F44AC  movzx    ecx, word ptr [rdx + rax + 0xe]
003F44B1  movsxd   rax, dword ptr [rdi + 0xc8]
003F44B8  mov      dword ptr [rdi + rax*8 + 0xd0], ecx
003F44BF  inc      dword ptr [rdi + 0xc8]
003F44C5  cmp      dword ptr [rdi + 0xc8], 3
003F44CC  jge      0x3f44e2  ; -> 003F44E2
003F44CE  mov      rax, qword ptr [rbx + 8]
003F44D2  inc      r8d
003F44D5  add      rdx, 4
003F44D9  movzx    ecx, word ptr [rax + 8]
003F44DD  cmp      r8d, ecx
003F44E0  jl       0x3f4490  ; -> 003F4490
003F44E2  mov      rax, qword ptr [rdi + 0x60]
003F44E6  xor      ecx, ecx
003F44E8  mov      rbx, qword ptr [rax + 0x18]
003F44EC  mov      rax, qword ptr [rdi + 0xc0]
003F44F3  mov      qword ptr [rbx + 0x18], rax
003F44F7  call     0x20e620  ; -> 0020E620 fn
003F44FC  mov      dword ptr [rbx + 0x20], eax
003F44FF  lea      r9, [rsp + 0x40]
003F4504  mov      rcx, qword ptr [rdi + 0xc0]
003F450B  lea      rax, [rsp + 0x48]
003F4510  xorps    xmm2, xmm2
003F4513  mov      qword ptr [rsp + 0x20], rax
003F4518  xor      edx, edx
003F451A  call     0x29cd00  ; -> 0029CD00 fn
003F451F  movsx    ecx, word ptr [rbx + 0xc]
003F4523  mov      rbx, qword ptr [rsp + 0x50]
003F4528  mov      eax, ecx
003F452A  add      eax, dword ptr [rsp + 0x40]
003F452E  lea      r8d, [rax + rcx*2]
003F4532  movsx    eax, word ptr [rdi + 0x9c]
003F4539  mov      edx, r8d
003F453C  mov      dword ptr [rsp + 0x40], r8d
003F4541  sub      edx, eax
003F4543  test     edx, edx
003F4545  jle      0x3f4567  ; -> 003F4567
003F4547  mov      rax, qword ptr [rdi + 0x60]
003F454B  mov      word ptr [rdi + 0x9c], r8w
003F4553  mov      rcx, qword ptr [rax + 0x10]
003F4557  add      word ptr [rcx + 0x10], dx
003F455B  mov      rax, qword ptr [rdi + 0x60]
003F455F  mov      rcx, qword ptr [rax + 0x20]
003F4563  add      word ptr [rcx + 0xc], dx
003F4567  mov      rax, qword ptr [rdi + 0x60]
003F456B  mov      edx, dword ptr [rdi + 0xc8]
003F4571  mov      rcx, qword ptr [rax + 8]
003F4575  mov      rcx, qword ptr [rcx + 0x18]
003F4579  mov      qword ptr [rdi + 0x118], rcx
003F4580  call     0x2d4930  ; -> 002D4930 fn
003F4585  mov      rax, qword ptr [rdi + 0x118]
003F458C  xor      edx, edx
003F458E  and      dword ptr [rax + 0xe0], 0xffdfffff
003F4598  mov      rcx, qword ptr [rdi + 0x118]
003F459F  call     0x2d45c0  ; -> 002D45C0 fn
003F45A4  mov      rax, qword ptr [rdi + 0x118]
003F45AB  lea      rcx, [rip - 0x3f2]  ; -> 003F41C0
003F45B2  mov      qword ptr [rax + 0x120], rcx
003F45B9  mov      rax, qword ptr [rdi + 0x118]
003F45C0  mov      qword ptr [rax + 0xd8], rdi
003F45C7  mov      rax, qword ptr [rdi + 0x118]
003F45CE  movzx    edx, word ptr [rax + 0x100]
003F45D5  mov      eax, 3
003F45DA  sub      eax, dword ptr [rdi + 0xc8]
003F45E0  imul     edx, eax
003F45E3  mov      rax, qword ptr [rdi + 0x60]
003F45E7  sub      word ptr [rdi + 0x9e], dx
003F45EE  mov      dword ptr [rsp + 0x48], edx
003F45F2  mov      rcx, qword ptr [rax + 0x20]
003F45F6  sub      word ptr [rcx + 0xe], dx
003F45FA  call     0x254a10  ; -> 00254A10 fn
003F45FF  test     eax, eax
003F4601  jne      0x3f461f  ; -> 003F461F
003F4603  mov      rax, qword ptr [rdi + 0x60]
003F4607  mov      rcx, qword ptr [rax + 0x20]
003F460B  mov      eax, 0xfffffff6
003F4610  and      dword ptr [rcx + 8], 0xfffffffe
003F4614  sub      ax, word ptr [rcx + 0x12]
003F4618  add      word ptr [rdi + 0x9e], ax
003F461F  mov      eax, dword ptr [rip + 0x1a17bb3]  ; -> 01E0C1D8 [u32 0x00000200]
003F4625  movsx    ecx, word ptr [rdi + 0x9c]
003F462C  or       dword ptr [rdi + 0x40], 0x80
003F4633  sub      eax, ecx
003F4635  cdq      
003F4636  mov      rcx, rdi
003F4639  sub      eax, edx
003F463B  mov      edx, 0xff
003F4640  sar      eax, 1
003F4642  mov      word ptr [rdi + 0x98], ax
003F4649  call     0x2475d0  ; -> 002475D0 fn
003F464E  mov      edx, 0x61
003F4653  mov      rcx, rdi
003F4656  call     0x247930  ; -> 00247930 fn
003F465B  xor      eax, eax
003F465D  add      rsp, 0x30
003F4661  pop      rdi
003F4662  ret      
```

## 00573BE0 (850 B, extent 00573BE0-00573F32)

Page context: "ok content page** — [the menu screen atlas](../Menu-Screen-Atlas/the-menu-screen-atlas.md) lists it beside '00571A50' and '00579AF0' as handbook content, with dispatch ids 1, 3, 10, 12, 14, 15, 18 | '00573BE0' → '002B5390' → the hub '002B2150', from **cases 1 and 10** ('005745A6', '00574672') |       | '002B0280' | the ShaderMaterial body, 6,441 B | calls the hub directly; its six callers are '002A86A0' (a message-window helper), '002D8"

```
00573BE0  mov      qword ptr [rsp + 0x18], rbx
00573BE5  push     rbp
00573BE6  push     rsi
00573BE7  push     rdi
00573BE8  sub      rsp, 0x30
00573BEC  mov      rbx, rcx
00573BEF  mov      byte ptr [rcx + 0x8061], dl
00573BF5  lea      rsi, [rcx + 0xf0]
00573BFC  movzx    edi, dl
00573BFF  mov      rcx, qword ptr [rcx + 0xd8]
00573C06  test     rcx, rcx
00573C09  je       0x573c25  ; -> 00573C25
00573C0B  lea      eax, [rdi + 1]
00573C0E  mov      edx, 1
00573C13  movzx    eax, al
00573C16  xor      r9d, r9d
00573C19  mov      r8d, edx
00573C1C  mov      dword ptr [rsp + 0x20], eax
00573C20  call     0x394800  ; -> 00394800 fn
00573C25  mov      ecx, dword ptr [rbx + 0xc8]
00573C2B  lea      eax, [rdi + 1]
00573C2E  and      cl, 1
00573C31  movzx    ebp, al
00573C34  mov      rcx, qword ptr [rbx + 0xd0]
00573C3B  movzx    eax, dil
00573C3F  cmove    ebp, eax
00573C42  cmp      bpl, byte ptr [rcx + 3]
00573C46  jb       0x573c6c  ; -> 00573C6C
00573C48  mov      byte ptr [rbx + 0x120], 0
00573C4F  mov      edx, 1
00573C54  mov      rcx, qword ptr [rbx + 0xe0]
00573C5B  mov      rbx, qword ptr [rsp + 0x60]
00573C60  add      rsp, 0x30
00573C64  pop      rdi
00573C65  pop      rsi
00573C66  pop      rbp
00573C67  jmp      0x2d48c0  ; -> 002D48C0 fn
00573C6C  mov      byte ptr [rbx + 0x8063], 1
00573C73  movzx    eax, bpl
00573C77  mov      rcx, qword ptr [rcx + rax*8 + 8]
00573C7C  mov      qword ptr [rsi + 8], rcx
00573C80  cmp      byte ptr [rbx + 0x8060], 5
00573C87  jne      0x573d22  ; -> 00573D22
00573C8D  mov      dl, 3
00573C8F  mov      qword ptr [rsp + 0x50], r14
00573C94  xor      edi, edi
00573C96  call     0x2b39a0  ; -> 002B39A0 fn
00573C9B  mov      r14, rax
00573C9E  test     rax, rax
00573CA1  je       0x573d0e  ; -> 00573D0E
00573CA3  mov      rdx, qword ptr [rsi + 8]
00573CA7  mov      ecx, r14d
00573CAA  sub      ecx, dword ptr [rsi + 8]
00573CAD  mov      edi, ecx
00573CAF  mov      r8d, ecx
00573CB2  mov      qword ptr [rsp + 0x58], r15
00573CB7  lea      r15, [rbx + 0x41a0]
00573CBE  mov      rcx, r15
00573CC1  call     0x861eba  ; -> 00861EBA fn
00573CC6  lea      rax, [r14 + 1]
00573CCA  mov      byte ptr [rdi + rbx + 0x41a0], 0
00573CD2  mov      dl, 2
00573CD4  mov      qword ptr [rsi + 8], rax
00573CD8  mov      rcx, r15
00573CDB  call     0x2b39a0  ; -> 002B39A0 fn
00573CE0  test     rax, rax
00573CE3  je       0x573ce8  ; -> 00573CE8
00573CE5  mov      byte ptr [rax], 0
00573CE8  mov      rax, qword ptr [rbx + 0x60]
00573CEC  mov      rdi, qword ptr [rax + 8]
00573CF0  call     0x5766b0  ; -> 005766B0 fn
00573CF5  mov      rcx, rax
00573CF8  mov      qword ptr [rdi + 0x18], r15
00573CFC  call     0x20e620  ; -> 0020E620 fn
00573D01  mov      r15, qword ptr [rsp + 0x58]
00573D06  mov      dword ptr [rdi + 0x20], eax
00573D09  mov      edi, 1
00573D0E  mov      rax, qword ptr [rbx + 0x60]
00573D12  mov      r14, qword ptr [rsp + 0x50]
00573D17  mov      rcx, qword ptr [rax + 8]
00573D1B  and      dword ptr [rcx + 8], 0xfffffffe
00573D1F  or       dword ptr [rcx + 8], edi
00573D22  lea      rax, [rbx + 0x120]
00573D29  mov      qword ptr [rsi + 0x10], 0
00573D31  mov      qword ptr [rsi], rax
00573D34  mov      eax, 0x4000
00573D39  mov      word ptr [rsi + 0x20], ax
00573D3D  call     0x5766b0  ; -> 005766B0 fn
00573D42  cmp      qword ptr [rsi + 8], 0
00573D47  mov      qword ptr [rsi + 0x18], rax
00573D4B  je       0x573ef9  ; -> 00573EF9
00573D51  call     0x254a10  ; -> 00254A10 fn
00573D56  test     eax, eax
00573D58  jne      0x573d82  ; -> 00573D82
00573D5A  mov      eax, 0xf2
00573D5F  cmp      word ptr [rsi + 0x24], ax
00573D63  jne      0x573d6e  ; -> 00573D6E
00573D65  mov      eax, 0x100
00573D6A  mov      word ptr [rsi + 0x24], ax
00573D6E  mov      eax, 0x190
00573D73  cmp      word ptr [rsi + 0x24], ax
00573D77  jne      0x573d82  ; -> 00573D82
00573D79  mov      eax, 0x1a4
00573D7E  mov      word ptr [rsi + 0x24], ax
00573D82  mov      rcx, rsi
00573D85  call     0x2b5240  ; -> 002B5240 fn
00573D8A  xor      edx, edx
00573D8C  mov      rcx, rsi
00573D8F  call     0x2b5390  ; -> 002B5390 fn
00573D94  movzx    ecx, byte ptr [rbx + 0x8063]
00573D9B  mov      r8, rax
00573D9E  dec      ecx
00573DA0  movsxd   rdx, ecx
00573DA3  mov      rcx, qword ptr [rsi + 8]
00573DA7  add      rdx, 0x41e
00573DAE  add      rdx, rdx
00573DB1  mov      qword ptr [rbx + rdx*8], rcx
00573DB5  movzx    ecx, byte ptr [rbx + 0x8063]
00573DBC  dec      ecx
00573DBE  movsxd   rdx, ecx
00573DC1  add      rdx, rdx
00573DC4  mov      dword ptr [rbx + rdx*8 + 0x41e8], 0x80808080
00573DCF  movzx    eax, byte ptr [rbx + 0x8063]
00573DD6  dec      eax
00573DD8  movsxd   rcx, eax
00573DDB  movzx    eax, word ptr [rsi + 0x22]
00573DDF  add      rcx, rcx
00573DE2  mov      word ptr [rbx + rcx*8 + 0x41ec], ax
00573DEA  movzx    eax, byte ptr [rbx + 0x8063]
00573DF1  movzx    edx, byte ptr [rsi + 0x27]
00573DF5  dec      eax
00573DF7  and      dl, 1
00573DFA  movsxd   rcx, eax
00573DFD  add      rcx, rcx
00573E00  mov      byte ptr [rbx + rcx*8 + 0x41ee], dl
00573E07  movzx    eax, byte ptr [rbx + 0x8063]
00573E0E  movzx    edx, byte ptr [rsi + 0x27]
00573E12  dec      eax
00573E14  shr      dl, 1
00573E16  and      dl, 1
00573E19  movsxd   rcx, eax
00573E1C  add      rcx, rcx
00573E1F  mov      byte ptr [rbx + rcx*8 + 0x41ef], dl
00573E26  mov      edi, dword ptr [rsi + 0x28]
00573E29  test     r8, r8
00573E2C  je       0x573eea  ; -> 00573EEA
00573E32  nop      dword ptr [rax]
00573E36  nop      word ptr [rax + rax]
00573E40  inc      byte ptr [rbx + 0x8063]
00573E46  xor      edx, edx
00573E48  mov      rcx, rsi
00573E4B  call     0x2b5390  ; -> 002B5390 fn
00573E50  movzx    ecx, byte ptr [rbx + 0x8063]
00573E57  mov      r8, rax
00573E5A  dec      ecx
00573E5C  movsxd   rdx, ecx
00573E5F  mov      rcx, qword ptr [rsi + 8]
00573E63  add      rdx, 0x41e
00573E6A  add      rdx, rdx
00573E6D  mov      qword ptr [rbx + rdx*8], rcx
00573E71  movzx    ecx, byte ptr [rbx + 0x8063]
00573E78  dec      ecx
00573E7A  movsxd   rdx, ecx
00573E7D  add      rdx, rdx
00573E80  mov      dword ptr [rbx + rdx*8 + 0x41e8], edi
00573E87  movzx    ecx, byte ptr [rbx + 0x8063]
00573E8E  movzx    eax, word ptr [rsi + 0x22]
00573E92  dec      ecx
00573E94  movsxd   rdx, ecx
00573E97  add      rdx, rdx
00573E9A  mov      word ptr [rbx + rdx*8 + 0x41ec], ax
00573EA2  movzx    eax, byte ptr [rbx + 0x8063]
00573EA9  movzx    edx, byte ptr [rsi + 0x27]
00573EAD  dec      eax
00573EAF  and      dl, 1
00573EB2  movsxd   rcx, eax
00573EB5  add      rcx, rcx
00573EB8  mov      byte ptr [rbx + rcx*8 + 0x41ee], dl
00573EBF  movzx    eax, byte ptr [rbx + 0x8063]
00573EC6  movzx    edx, byte ptr [rsi + 0x27]
00573ECA  dec      eax
00573ECC  shr      dl, 1
00573ECE  and      dl, 1
00573ED1  movsxd   rcx, eax
00573ED4  add      rcx, rcx
00573ED7  mov      byte ptr [rbx + rcx*8 + 0x41ef], dl
00573EDE  mov      edi, dword ptr [rsi + 0x28]
00573EE1  test     r8, r8
00573EE4  jne      0x573e40  ; -> 00573E40
00573EEA  mov      qword ptr [rsi + 0x10], 0
00573EF2  mov      dword ptr [rsi + 0x28], 0x80808080
00573EF9  movzx    edx, byte ptr [rbx + 0x8063]
00573F00  mov      rcx, qword ptr [rbx + 0xe0]
00573F07  call     0x2d48c0  ; -> 002D48C0 fn
00573F0C  mov      rcx, qword ptr [rbx + 0xe0]
00573F13  xor      edx, edx
00573F15  call     0x2d46f0  ; -> 002D46F0 fn
00573F1A  movzx    edx, bpl
00573F1E  mov      rcx, rbx
00573F21  mov      rbx, qword ptr [rsp + 0x60]
00573F26  add      rsp, 0x30
00573F2A  pop      rdi
00573F2B  pop      rsi
00573F2C  pop      rbp
00573F2D  jmp      0x574900  ; -> 00574900 fn
```
