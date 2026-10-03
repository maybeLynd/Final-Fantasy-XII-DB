# Homing pack: `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-character-render-record-array.json`.

Bodies: 5. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001E1520 (323 B, extent 001E1520-001E1663)

Entered from (direct sites whose caller this page cites): `0015CC90` + 0x10 (call; `0015CC90` is cited on this page)
Other direct sites: none

Host context: "26C59') and the reset helper ('0042ED37') and is neither cleared nor tested. Bit 4 = **external fade enable** — written only by '002E8700(bool)' ('002E8707', '002E871C') from platform-layer callers ('0015CC90', '0017CDF0', '0017CE20', '0017D6E0', '0017DE60'), read only by the fade subtraction at '0042EB79'. Bit 5 = **active list dirty** — set by the promoter ('00428863') and the remover ('00427DB3'), cleared and consumed by '0042ED60' ("

```
001E1520  mov      qword ptr [rsp + 8], rcx
001E1525  push     rbx
001E1526  push     rbp
001E1527  push     rsi
001E1528  push     rdi
001E1529  push     r14
001E152B  push     r15
001E152D  sub      rsp, 0x48
001E1531  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001E153A  mov      r15d, edx
001E153D  mov      r14, rcx
001E1540  xor      edi, edi
001E1542  mov      qword ptr [rcx], rdi
001E1545  mov      qword ptr [rcx + 8], rdi
001E1549  mov      qword ptr [rcx + 0x10], rdi
001E154D  add      rcx, 0x18
001E1551  lea      rdx, [rip + 0x6e4a00]  ; -> 008C5F58 [str "EASTL vector"]
001E1558  call     0x1edf00  ; -> 001EDF00 fn
001E155D  nop      
001E155E  lea      rdx, [rip + 0x71274b]  ; -> 008F3CB0 [str "EASTL set"]
001E1565  lea      rcx, [rsp + 0x90]
001E156D  call     0x1edf00  ; -> 001EDF00 fn
001E1572  lea      rbp, [r14 + 0x20]
001E1576  mov      qword ptr [rsp + 0x98], rbp
001E157E  lea      rbx, [rbp + 8]
001E1582  xor      ecx, ecx
001E1584  mov      qword ptr [rbx], rcx
001E1587  mov      qword ptr [rbx + 8], rcx
001E158B  mov      qword ptr [rbx + 0x10], rcx
001E158F  mov      qword ptr [rbx + 0x18], rcx
001E1593  mov      dword ptr [rbp + 0x28], edi
001E1596  lea      rcx, [rbp + 0x30]
001E159A  mov      rdx, rax
001E159D  call     0x1edf00  ; -> 001EDF00 fn
001E15A2  mov      qword ptr [rbx], rbx
001E15A5  mov      qword ptr [rbp + 0x10], rbx
001E15A9  mov      qword ptr [rbp + 0x18], rdi
001E15AD  mov      byte ptr [rbp + 0x20], dil
001E15B1  mov      dword ptr [rbp + 0x28], edi
001E15B4  lea      rdx, [rip + 0x7126f5]  ; -> 008F3CB0 [str "EASTL set"]
001E15BB  lea      rcx, [rsp + 0x98]
001E15C3  call     0x1edf00  ; -> 001EDF00 fn
001E15C8  lea      rsi, [r14 + 0x58]
001E15CC  mov      qword ptr [rsp + 0x28], rsi
001E15D1  lea      rbx, [rsi + 8]
001E15D5  xor      ecx, ecx
001E15D7  mov      qword ptr [rbx], rcx
001E15DA  mov      qword ptr [rbx + 8], rcx
001E15DE  mov      qword ptr [rbx + 0x10], rcx
001E15E2  mov      qword ptr [rbx + 0x18], rcx
001E15E6  mov      dword ptr [rsi + 0x28], edi
001E15E9  lea      rcx, [rsi + 0x30]
001E15ED  mov      rdx, rax
001E15F0  call     0x1edf00  ; -> 001EDF00 fn
001E15F5  mov      qword ptr [rbx], rbx
001E15F8  mov      qword ptr [rsi + 0x10], rbx
001E15FC  mov      qword ptr [rsi + 0x18], rdi
001E1600  mov      byte ptr [rsi + 0x20], dil
001E1604  mov      dword ptr [rsi + 0x28], edi
001E1607  mov      edx, r15d
001E160A  mov      rcx, r14
001E160D  call     0x1e5370  ; -> 001E5370 fn
001E1612  test     r15d, r15d
001E1615  je       0x1e1653  ; -> 001E1653
001E1617  mov      esi, r15d
001E161A  movzx    ebx, byte ptr [rsp + 0x88]
001E1622  mov      rcx, qword ptr [r14]
001E1625  add      rcx, rdi
001E1628  mov      qword ptr [rsp + 0x90], rcx
001E1630  movzx    r9d, bl
001E1634  lea      r8, [rsp + 0x90]
001E163C  lea      rdx, [rsp + 0x28]
001E1641  mov      rcx, rbp
001E1644  call     0x199db0  ; -> 00199DB0 fn
001E1649  add      rdi, 0x18
001E164D  sub      rsi, 1
001E1651  jne      0x1e1622  ; -> 001E1622
001E1653  mov      rax, r14
001E1656  add      rsp, 0x48
001E165A  pop      r15
001E165C  pop      r14
001E165E  pop      rdi
001E165F  pop      rsi
001E1660  pop      rbp
001E1661  pop      rbx
001E1662  ret      
```

## 002E88A0 (92 B, extent 002E88A0-002E88FC)

Entered from (direct sites whose caller this page cites): `00342410` + 0x21 (call; `00342410` is cited on this page)
Other direct sites: `003429A0` + 0x5 (jmp)

Host context: ", "LOD is scripted" — and '002E89B0(actor, v)', which clamps 'v' to '[0, max]' and stores it at **'+0x27C'**; **'clearshadowlod'** ('0x0287') is '002E8950(actor, 0)'. **'setshadowalpha'** ('0x0284', '00342410') calls '002E88A0(actor, 1)' — bit 2 of '+0xC0' — and '002E8900(actor, a)' → **'+0x274'**; **'clearshadowalpha'** ('0x0285') clears the bit. Both floats reset to 1.0 in 'CharacterRenderRecord_ResetDefaults' ('0041F814', '0041F81E')"

```
002E88A0  test     rcx, rcx
002E88A3  je       0x2e88fb  ; -> 002E88FB
002E88A5  mov      rax, qword ptr [rcx + 0xc0]
002E88AC  test     rax, rax
002E88AF  je       0x2e88fb  ; -> 002E88FB
002E88B1  cmp      dword ptr [rax], -1
002E88B4  je       0x2e88fb  ; -> 002E88FB
002E88B6  movzx    ecx, word ptr [rax]
002E88B9  xor      r8d, r8d
002E88BC  test     edx, edx
002E88BE  setne    r8b
002E88C2  cmp      cx, -1
002E88C6  je       0x2e88fb  ; -> 002E88FB
002E88C8  movsx    rax, cx
002E88CC  imul     rcx, rax, 0x740
002E88D3  add      rcx, qword ptr [rip + 0x1fde64e]  ; -> 022C6F28
002E88DA  je       0x2e88fb  ; -> 002E88FB
002E88DC  cmp      dword ptr [rcx + 0x284], 0
002E88E3  je       0x2e88fb  ; -> 002E88FB
002E88E5  and      byte ptr [rcx + 0xc0], 0xfb
002E88EC  and      r8b, 1
002E88F0  shl      r8b, 2
002E88F4  or       byte ptr [rcx + 0xc0], r8b
002E88FB  ret      
```

## 002E8900 (69 B, extent 002E8900-002E8945)

Entered from (direct sites whose caller this page cites): `00342410` + 0x36 (jmp; `00342410` is cited on this page)
Other direct sites: none

Host context: ", "LOD is scripted" — and '002E89B0(actor, v)', which clamps 'v' to '[0, max]' and stores it at **'+0x27C'**; **'clearshadowlod'** ('0x0287') is '002E8950(actor, 0)'. **'setshadowalpha'** ('0x0284', '00342410') calls '002E88A0(actor, 1)' — bit 2 of '+0xC0' — and '002E8900(actor, a)' → **'+0x274'**; **'clearshadowalpha'** ('0x0285') clears the bit. Both floats reset to 1.0 in 'CharacterRenderRecord_ResetDefaults' ('0041F814', '0041F81E')"

```
002E8900  test     rcx, rcx
002E8903  je       0x2e8944  ; -> 002E8944
002E8905  mov      rax, qword ptr [rcx + 0xc0]
002E890C  test     rax, rax
002E890F  je       0x2e8944  ; -> 002E8944
002E8911  cmp      dword ptr [rax], -1
002E8914  je       0x2e8944  ; -> 002E8944
002E8916  movzx    ecx, word ptr [rax]
002E8919  cmp      cx, -1
002E891D  je       0x2e8944  ; -> 002E8944
002E891F  movsx    rax, cx
002E8923  imul     rcx, rax, 0x740
002E892A  add      rcx, qword ptr [rip + 0x1fde5f7]  ; -> 022C6F28
002E8931  je       0x2e8944  ; -> 002E8944
002E8933  cmp      dword ptr [rcx + 0x284], 0
002E893A  je       0x2e8944  ; -> 002E8944
002E893C  movss    dword ptr [rcx + 0x274], xmm1
002E8944  ret      
```

## 002E8950 (91 B, extent 002E8950-002E89AB)

Entered from (direct sites whose caller this page cites): `00342CF0` + 0x21 (call; `00342CF0` is cited on this page)
Other direct sites: `00343130` + 0x5 (jmp)

Host context: ", with 'kind = (+0x304 >> 12) & 3'; kind 0 keeps only the pool-A object, kind 1 allocates a pool-B object, kinds 2 and 3 leave both off.  The script verbs own the rest: **'setshadowlod'** ('0x0286', '00342CF0') calls '002E8950(actor, 1)' — bit 1 of '+0xC0', "LOD is scripted" — and '002E89B0(actor, v)', which clamps 'v' to '[0, max]' and stores it at **'+0x27C'**; **'clearshadowlod'** ('0x0287') is '002E8950(actor, 0)'. **'setshadowalpha"

```
002E8950  test     rcx, rcx
002E8953  je       0x2e89aa  ; -> 002E89AA
002E8955  mov      rax, qword ptr [rcx + 0xc0]
002E895C  test     rax, rax
002E895F  je       0x2e89aa  ; -> 002E89AA
002E8961  cmp      dword ptr [rax], -1
002E8964  je       0x2e89aa  ; -> 002E89AA
002E8966  movzx    ecx, word ptr [rax]
002E8969  xor      r8d, r8d
002E896C  test     edx, edx
002E896E  setne    r8b
002E8972  cmp      cx, -1
002E8976  je       0x2e89aa  ; -> 002E89AA
002E8978  movsx    rax, cx
002E897C  imul     rcx, rax, 0x740
002E8983  add      rcx, qword ptr [rip + 0x1fde59e]  ; -> 022C6F28
002E898A  je       0x2e89aa  ; -> 002E89AA
002E898C  cmp      dword ptr [rcx + 0x284], 0
002E8993  je       0x2e89aa  ; -> 002E89AA
002E8995  and      byte ptr [rcx + 0xc0], 0xfd
002E899C  and      r8b, 1
002E89A0  add      r8b, r8b
002E89A3  or       byte ptr [rcx + 0xc0], r8b
002E89AA  ret      
```

## 002E89B0 (89 B, extent 002E89B0-002E8A09)

Entered from (direct sites whose caller this page cites): `00342CF0` + 0x36 (jmp; `00342CF0` is cited on this page)
Other direct sites: none

Host context: ", with 'kind = (+0x304 >> 12) & 3'; kind 0 keeps only the pool-A object, kind 1 allocates a pool-B object, kinds 2 and 3 leave both off.  The script verbs own the rest: **'setshadowlod'** ('0x0286', '00342CF0') calls '002E8950(actor, 1)' — bit 1 of '+0xC0', "LOD is scripted" — and '002E89B0(actor, v)', which clamps 'v' to '[0, max]' and stores it at **'+0x27C'**; **'clearshadowlod'** ('0x0287') is '002E8950(actor, 0)'. **'setshadowalpha"

```
002E89B0  test     rcx, rcx
002E89B3  je       0x2e8a08  ; -> 002E8A08
002E89B5  mov      rax, qword ptr [rcx + 0xc0]
002E89BC  test     rax, rax
002E89BF  je       0x2e8a08  ; -> 002E8A08
002E89C1  cmp      dword ptr [rax], -1
002E89C4  je       0x2e8a08  ; -> 002E8A08
002E89C6  xorps    xmm0, xmm0
002E89C9  comiss   xmm0, xmm1
002E89CC  ja       0x2e89da  ; -> 002E89DA
002E89CE  movss    xmm0, dword ptr [rip + 0x1a031d2]  ; -> 01CEBBA8 [f32 1]
002E89D6  minss    xmm0, xmm1
002E89DA  movzx    ecx, word ptr [rax]
002E89DD  cmp      cx, -1
002E89E1  je       0x2e8a08  ; -> 002E8A08
002E89E3  movsx    rax, cx
002E89E7  imul     rcx, rax, 0x740
002E89EE  add      rcx, qword ptr [rip + 0x1fde533]  ; -> 022C6F28
002E89F5  je       0x2e8a08  ; -> 002E8A08
002E89F7  cmp      dword ptr [rcx + 0x284], 0
002E89FE  je       0x2e8a08  ; -> 002E8A08
002E8A00  movss    dword ptr [rcx + 0x27c], xmm0
002E8A08  ret      
```
