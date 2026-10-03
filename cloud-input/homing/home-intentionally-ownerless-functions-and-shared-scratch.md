# Homing pack: `00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-intentionally-ownerless-functions-and-shared-scratch.json`.

Bodies: 12. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001B6B50 (105 B, extent 001B6B50-001B6BB9)

Entered from (direct sites whose caller this page cites): `00188B10` + 0x1CD (call; `00188B10` is cited on this page)
Other direct sites: none

Host context: "e track, are the residue; the identity is settled.  ## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)  | function | size | role (call-signature read) | |---|---:|---| | '00188B10' | 643 | per-entry loop over '[rsi+0xB08..0xB30]' fields: '00258130'/'00259360'/'0025A890' accessors, '00610330', repeating '00182E80' x11/'00182EB0' x11/'001EEE80' x10 |  ## The '003B8670' exclusive subtree — the interpreter's 33 "

```
001B6B50  mov      qword ptr [rsp + 0x10], rbx
001B6B55  push     rdi
001B6B56  sub      rsp, 0x20
001B6B5A  mov      rbx, qword ptr [rcx]
001B6B5D  mov      rdi, rcx
001B6B60  cmp      rbx, qword ptr [rcx + 8]
001B6B64  je       0x1b6bae  ; -> 001B6BAE
001B6B66  mov      qword ptr [rsp + 0x30], rsi
001B6B6B  lea      rsi, [rbx + 8]
001B6B6F  nop      
001B6B70  mov      rcx, qword ptr [rbx]
001B6B73  call     0x1b6a70  ; -> 001B6A70 fn
001B6B78  test     al, al
001B6B7A  je       0x1b6b9b  ; -> 001B6B9B
001B6B7C  mov      r8, qword ptr [rdi + 8]
001B6B80  cmp      rsi, r8
001B6B83  jae      0x1b6b94  ; -> 001B6B94
001B6B85  sub      r8, rsi
001B6B88  mov      rdx, rsi
001B6B8B  mov      rcx, rbx
001B6B8E  call     qword ptr [rip + 0x70beac]  ; -> 008C2A40 [u64 0x0000000001CCEB62]
001B6B94  add      qword ptr [rdi + 8], -8
001B6B99  jmp      0x1b6ba3  ; -> 001B6BA3
001B6B9B  add      rbx, 8
001B6B9F  add      rsi, 8
001B6BA3  cmp      rbx, qword ptr [rdi + 8]
001B6BA7  jne      0x1b6b70  ; -> 001B6B70
001B6BA9  mov      rsi, qword ptr [rsp + 0x30]
001B6BAE  mov      rbx, qword ptr [rsp + 0x38]
001B6BB3  add      rsp, 0x20
001B6BB7  pop      rdi
001B6BB8  ret      
```

## 003339C0 (128 B, extent 003339C0-00333A40)

Entered from (direct sites whose caller this page cites): `003B8670` + 0x4B2 (call; `003B8670` is cited on this page)
Other direct sites: `003B27A0` + 0x72 (call)

Host context: "/Shared-Transform-Workbench/the-shared-transform-workbench.md) §10.  ## 3. Key addresses  Addresses are Ghidra image base '0x00120000'.  | Address | Working name | Body | Role | |---|---|---:|---| | '003B8670' | authored-event / bootstrap coordinator | 4,578 B | **mislabelled** 'ROUTER_ADAPTER_OR_THUNK'; 63 distinct callees, 15 written objects | | '00521BB0' | scratch materializer | 1,757 B | **mislabelled** 'ROUTER_ADAPTER_OR_THUNK'; 1"

```
003339C0  test     rcx, rcx
003339C3  je       0x333a3f  ; -> 00333A3F
003339C5  mov      qword ptr [rsp + 0x20], rsi
003339CA  push     r14
003339CC  sub      rsp, 0x20
003339D0  mov      qword ptr [rsp + 0x30], rbx
003339D5  movzx    esi, dl
003339D8  mov      qword ptr [rsp + 0x38], rbp
003339DD  mov      r14, rcx
003339E0  xor      ebp, ebp
003339E2  mov      qword ptr [rsp + 0x40], rdi
003339E7  mov      ebx, ebp
003339E9  nop      dword ptr [rax]
003339F0  mov      rdi, qword ptr [r14 + rbx*8]
003339F4  test     rdi, rdi
003339F7  je       0x333a13  ; -> 00333A13
003339F9  cmp      byte ptr [rdi + 0x11], sil
003339FD  jne      0x333a13  ; -> 00333A13
003339FF  mov      rcx, rdi
00333A02  call     0x46ee70  ; -> 0046EE70 fn
00333A07  mov      rcx, rdi
00333A0A  call     0x3697f0  ; -> 003697F0 fn
00333A0F  mov      qword ptr [r14 + rbx*8], rbp
00333A13  inc      rbx
00333A16  cmp      rbx, 0x10
00333A1A  jl       0x3339f0  ; -> 003339F0
00333A1C  movzx    ecx, sil
00333A20  call     0x3a87b0  ; -> 003A87B0 fn
00333A25  mov      rdi, qword ptr [rsp + 0x40]
00333A2A  mov      rbp, qword ptr [rsp + 0x38]
00333A2F  mov      rbx, qword ptr [rsp + 0x30]
00333A34  mov      rsi, qword ptr [rsp + 0x48]
00333A39  add      rsp, 0x20
00333A3D  pop      r14
00333A3F  ret      
```

## 00376990 (71 B, extent 00376990-003769D7)

Entered from (direct sites whose caller this page cites): `00461250` + 0x13 (jmp; `00461250` is cited on this page)
Other direct sites: none

Host context: "dex/ADDRESS-INDEX.md) is 'jmp r8' — the body dispatches on 'byte[rcx] - 0x40' through a 0x92-wide two-level table stored inline at '002F32AC'/'002F32C8' (six named case targets '00464050'/'00464B80'/'00461250'/'00465120'/ '003D90C0'/'00460120', default '0043E9C0'), then **unlinks 'rbx' from its intrusive list** ('[rbx+0x28]'/'+0x30' prev/next fixup into 'rdi''s '+0x118'/'+0x128' list heads) and pushes it onto the 'rdi+0x120' list. A typ"

```
00376990  test     ecx, ecx
00376992  je       0x3769d6  ; -> 003769D6
00376994  push     rbx
00376995  sub      rsp, 0x20
00376999  movzx    edx, cl
0037699C  lea      rax, [rip + 0x276519d]  ; -> 02ADBB40
003769A3  lea      rbx, [rdx + rdx*8]
003769A7  shl      rbx, 4
003769AB  add      rbx, rax
003769AE  cmp      dword ptr [rbx], ecx
003769B0  jne      0x3769d1  ; -> 003769D1
003769B2  dec      byte ptr [rip + 0x2765178]  ; -> 02ADBB30
003769B8  mov      dword ptr [rbx], 0
003769BE  mov      ecx, dword ptr [rbx + 0x50]
003769C1  test     ecx, ecx
003769C3  je       0x3769ca  ; -> 003769CA
003769C5  call     0x3abca0  ; -> 003ABCA0 fn
003769CA  mov      dword ptr [rbx + 0x50], 0
003769D1  add      rsp, 0x20
003769D5  pop      rbx
003769D6  ret      
```

## 003A8340 (79 B, extent 003A8340-003A838F)

Entered from (direct sites whose caller this page cites): `003A8AE0` + 0xF1 (call; `003A8AE0` is cited on this page)
Other direct sites: none

Host context: "BA4F0' (the target array) — the heavyweight opcode arms | | '02EBEF88' family + wrappers | '003A8C80', '003A8CB0', '003A8CE0', '003A8D40' (33–89 B each on '02EBEF88'), '003A8DD0' (423 B — '001EDDA0'/'003A8AE0'/'002F31C0'), '003A8290' ('004FF080'/'004FF0D0', '02EBEF98'); wrappers '003326F0'/'00333430'/'003335A0'/'00333A40' (each '0046EE70' + '003697F0' + one '003A8Cxx') | a shared sub-object at '02EBEF88' with four field ops plus one lar"

```
003A8340  mov      rax, qword ptr [rip + 0x2b16c41]  ; -> 02EBEF88
003A8347  add      rax, 0x18
003A834B  xor      r9d, r9d
003A834E  nop      
003A8350  mov      r10d, dword ptr [rax]
003A8353  cmp      r10d, ecx
003A8356  jne      0x3a8362  ; -> 003A8362
003A8358  movzx    r8d, byte ptr [rax + 4]
003A835D  cmp      r8d, edx
003A8360  je       0x3a8377  ; -> 003A8377
003A8362  cmp      r10d, -1
003A8366  je       0x3a837c  ; -> 003A837C
003A8368  inc      r9d
003A836B  add      rax, 8
003A836F  cmp      r9d, 0x20
003A8373  jge      0x3a838e  ; -> 003A838E
003A8375  jmp      0x3a8350  ; -> 003A8350
003A8377  inc      word ptr [rax + 6]
003A837B  ret      
003A837C  and      byte ptr [rax + 5], 0xfe
003A8380  mov      dword ptr [rax], ecx
003A8382  mov      ecx, 1
003A8387  mov      word ptr [rax + 6], cx
003A838B  mov      byte ptr [rax + 4], dl
003A838E  ret      
```

## 003A9590 (104 B, extent 003A9590-003A95F8)

Entered from (direct sites whose caller this page cites): `003A96A0` + 0x6D (call; `003A96A0` is cited on this page)
Other direct sites: none

Host context: "ow down and stamping '0xFFFFFFFF' at the tail, non-zero means 'byte[+5] |= 1' and a 1 return - the tombstone-or-remove branch of the shared table.  Interior anchor '003A90C0' (function '003A9070').  '003A96A0' (142 B) is the resolve-and-bind sibling on '02EBEF90': 'word[rcx]' indexes '[02EBEF90]''s pointer table into 'rbp', '003A9790' resolves 'ecx'/'ebx' into 'rdi', '00861EBA' copies the caller's 'rsi+4' string into it, '00442460' stor"

```
003A9590  mov      rax, qword ptr [rip + 0x2b159f1]  ; -> 02EBEF88
003A9597  mov      rax, qword ptr [rax + 8]
003A959B  test     rax, rax
003A959E  je       0x3a95f7  ; -> 003A95F7
003A95A0  mov      r8, qword ptr [rax + 8]
003A95A4  cmp      qword ptr [rax + 0x100], rcx
003A95AB  jne      0x3a95b4  ; -> 003A95B4
003A95AD  mov      qword ptr [rax + 0x100], rdx
003A95B4  cmp      qword ptr [rax + 0x108], rcx
003A95BB  jne      0x3a95c4  ; -> 003A95C4
003A95BD  mov      qword ptr [rax + 0x108], rdx
003A95C4  mov      rax, qword ptr [rax + 0x118]
003A95CB  test     rax, rax
003A95CE  je       0x3a95ef  ; -> 003A95EF
003A95D0  cmp      qword ptr [rax + 0x18], rcx
003A95D4  jne      0x3a95dc  ; -> 003A95DC
003A95D6  mov      qword ptr [rax + 0x18], rdx
003A95DA  jmp      0x3a95e6  ; -> 003A95E6
003A95DC  cmp      qword ptr [rax + 0x20], rcx
003A95E0  jne      0x3a95e6  ; -> 003A95E6
003A95E2  mov      qword ptr [rax + 0x20], rdx
003A95E6  mov      rax, qword ptr [rax + 0x30]
003A95EA  test     rax, rax
003A95ED  jne      0x3a95d0  ; -> 003A95D0
003A95EF  mov      rax, r8
003A95F2  test     r8, r8
003A95F5  jne      0x3a95a0  ; -> 003A95A0
003A95F7  ret      
```

## 00424040 (59 B, extent 00424040-0042407B)

Entered from (direct sites whose caller this page cites): `003B8670` + 0x7AD (call; `003B8670` is cited on this page)
Other direct sites: `0042B460` + 0x57 (call); `0042B460` + 0x8C (call); `0042E480` + 0x1E (jmp)

Host context: "/Shared-Transform-Workbench/the-shared-transform-workbench.md) §10.  ## 3. Key addresses  Addresses are Ghidra image base '0x00120000'.  | Address | Working name | Body | Role | |---|---|---:|---| | '003B8670' | authored-event / bootstrap coordinator | 4,578 B | **mislabelled** 'ROUTER_ADAPTER_OR_THUNK'; 63 distinct callees, 15 written objects | | '00521BB0' | scratch materializer | 1,757 B | **mislabelled** 'ROUTER_ADAPTER_OR_THUNK'; 1"

```
00424040  push     rbx
00424042  sub      rsp, 0x20
00424046  cmp      dword ptr [rcx + 0xc4], -1
0042404D  mov      rbx, rcx
00424050  je       0x424075  ; -> 00424075
00424052  mov      ecx, dword ptr [rcx + 0x10]
00424055  call     0x20e600  ; -> 0020E600 fn
0042405A  mov      edx, dword ptr [rbx + 0xc4]
00424060  mov      rcx, qword ptr [rax + 0xda8]
00424067  call     0x51b9e0  ; -> 0051B9E0 fn
0042406C  test     rax, rax
0042406F  je       0x424075  ; -> 00424075
00424071  or       dword ptr [rax + 0xc], 0x40
00424075  add      rsp, 0x20
00424079  pop      rbx
0042407A  ret      
```

## 0042FCB0 (7 B, extent 0042FCB0-0042FCB7)

Entered from (direct sites whose caller this page cites): `002EAD00` + 0x26 (call; `002EAD00` is cited on this page)
Other direct sites: none

Host context: "FDF70'/'00615BC0'/'00616700'/'00624660'/'00624670'/'0065C750' - the render-pass record's resize-on-change.  Interior anchor '00193B10' (function '00193AD0').  '002FCCC0' (562 B) is the keyed release '002EAD00' and '003B8670' call: 'r9d & 0x3F < 0x30' selects a 0x38-stride record of '02EC32E0', '[rdi]' must equal the key and 'byte[+0x23] & 0xF == 5', then the '02EC3D60' list sums 'word[+0x20]'-indexed '& 0x1F' fields, '003AFFB0(0x24 - su"

```
0042FCB0  inc      dword ptr [rip + 0x2875226]  ; -> 02CA4EDC
0042FCB6  ret      
```

## 00471140 (10 B, extent 00471140-0047114A)

Entered from (direct sites whose caller this page cites): `003E1350` + 0x1E7 (jmp; `003E1350` is cited on this page)
Other direct sites: none

Host context: "B0' ('020925A0'–'B4' cells + '0026A430'/'0026AF80'), '00333520', '00333640', '003A4070' ('02096A20' + '003B0BF0'), '003A7F60' ('02EBEF98' + '003697F0'), '003B8260' (1,028 B — '0020E600' ×7 + resolve '003E1350'/'003E1610' + '003B3CA0' ×2, '00D115BC'–'E0' table + '02EBA4F0'; interior verified 2026-09-17, SWE2-FRONTIER — '0031E880' first at ['003B82D7'](../../_index/ADDRESS-INDEX.md)), '003B99D0' (1,501 B — 24 helpers, '020926F4' + '02EBA4"

```
00471140  xor      eax, eax
00471142  mov      byte ptr [rcx], 0
00471145  mov      word ptr [rcx + 2], ax
00471149  ret      
```

## 00472550 (41 B, extent 00472550-00472579)

Entered from (direct sites whose caller this page cites): `003E1610` + 0x209 (jmp; `003E1610` is cited on this page)
Other direct sites: none

Host context: "5A0'–'B4' cells + '0026A430'/'0026AF80'), '00333520', '00333640', '003A4070' ('02096A20' + '003B0BF0'), '003A7F60' ('02EBEF98' + '003697F0'), '003B8260' (1,028 B — '0020E600' ×7 + resolve '003E1350'/'003E1610' + '003B3CA0' ×2, '00D115BC'–'E0' table + '02EBA4F0'; interior verified 2026-09-17, SWE2-FRONTIER — '0031E880' first at ['003B82D7'](../../_index/ADDRESS-INDEX.md)), '003B99D0' (1,501 B — 24 helpers, '020926F4' + '02EBA4F0'; interi"

```
00472550  and      byte ptr [rcx + 9], 0xdf
00472554  or       byte ptr [rcx + 9], 0x10
00472558  cmp      byte ptr [rcx + 9], 0x40
0047255C  jae      0x472578  ; -> 00472578
0047255E  cmp      byte ptr [rcx + 8], 0
00472562  jne      0x472578  ; -> 00472578
00472564  mov      eax, 1
00472569  mov      qword ptr [rcx + 0x10], 8
00472571  mov      word ptr [rcx + 0xa], ax
00472575  mov      byte ptr [rcx + 8], al
00472578  ret      
```

## 00515610 (70 B, extent 00515610-00515656)

Entered from (direct sites whose caller this page cites): `003E1350` + 0xB7 (jmp; `003E1350` is cited on this page)
Other direct sites: none

Host context: "B0' ('020925A0'–'B4' cells + '0026A430'/'0026AF80'), '00333520', '00333640', '003A4070' ('02096A20' + '003B0BF0'), '003A7F60' ('02EBEF98' + '003697F0'), '003B8260' (1,028 B — '0020E600' ×7 + resolve '003E1350'/'003E1610' + '003B3CA0' ×2, '00D115BC'–'E0' table + '02EBA4F0'; interior verified 2026-09-17, SWE2-FRONTIER — '0031E880' first at ['003B82D7'](../../_index/ADDRESS-INDEX.md)), '003B99D0' (1,501 B — 24 helpers, '020926F4' + '02EBA4"

```
00515610  push     rbx
00515612  sub      rsp, 0x20
00515616  cmp      byte ptr [rcx + 8], 0
0051561A  mov      rbx, rcx
0051561D  je       0x515650  ; -> 00515650
0051561F  mov      byte ptr [rcx + 8], 0
00515623  mov      dword ptr [rcx + 0x38], 0x3f800000
0051562A  mov      ecx, dword ptr [rcx]
0051562C  call     0x20e600  ; -> 0020E600 fn
00515631  xor      edx, edx
00515633  cmp      dword ptr [rbx + 4], edx
00515636  jbe      0x515650  ; -> 00515650
00515638  lea      rcx, [rax + 0xc]
0051563C  nop      dword ptr [rax]
00515640  mov      eax, dword ptr [rcx - 4]
00515643  inc      edx
00515645  mov      dword ptr [rcx], eax
00515647  lea      rcx, [rcx + 0x50]
0051564B  cmp      edx, dword ptr [rbx + 4]
0051564E  jb       0x515640  ; -> 00515640
00515650  add      rsp, 0x20
00515654  pop      rbx
00515655  ret      
```

## 00516200 (17 B, extent 00516200-00516211)

Entered from (direct sites whose caller this page cites): `003E1350` + 0x14F (jmp; `003E1350` is cited on this page)
Other direct sites: none

Host context: "B0' ('020925A0'–'B4' cells + '0026A430'/'0026AF80'), '00333520', '00333640', '003A4070' ('02096A20' + '003B0BF0'), '003A7F60' ('02EBEF98' + '003697F0'), '003B8260' (1,028 B — '0020E600' ×7 + resolve '003E1350'/'003E1610' + '003B3CA0' ×2, '00D115BC'–'E0' table + '02EBA4F0'; interior verified 2026-09-17, SWE2-FRONTIER — '0031E880' first at ['003B82D7'](../../_index/ADDRESS-INDEX.md)), '003B99D0' (1,501 B — 24 helpers, '020926F4' + '02EBA4"

```
00516200  xor      eax, eax
00516202  mov      byte ptr [rcx + 0xa4], 0
00516209  mov      word ptr [rcx + 0xa6], ax
00516210  ret      
```

## 0065C6B0 (145 B, extent 0065C6B0-0065C741)

Entered from (direct sites whose caller this page cites): `0065C750` + 0x0 (jmp; `0065C750` is cited on this page)
Other direct sites: none

Host context: " five '001EEE80' refreshes across '+0x280'..'+0x298' plus the midpoint-aligned '+0x2A0' write, then '001DC4A0'/'001DC4C0'/'001DC510'/'001DC590'/'001FDF70'/'00615BC0'/'00616700'/'00624660'/'00624670'/'0065C750' - the render-pass record's resize-on-change.  Interior anchor '00193B10' (function '00193AD0').  '002FCCC0' (562 B) is the keyed release '002EAD00' and '003B8670' call: 'r9d & 0x3F < 0x30' selects a 0x38-stride record of '02EC32E0"

```
0065C6B0  mov      qword ptr [rsp + 8], rbx
0065C6B5  mov      qword ptr [rsp + 0x10], rsi
0065C6BA  push     rdi
0065C6BB  sub      rsp, 0x30
0065C6BF  mov      rbx, qword ptr [rcx + 0x50]
0065C6C3  mov      edi, r8d
0065C6C6  mov      esi, edx
0065C6C8  test     rbx, rbx
0065C6CB  je       0x65c72c  ; -> 0065C72C
0065C6CD  cmp      byte ptr [rbx + 8], 0
0065C6D1  jne      0x65c72c  ; -> 0065C72C
0065C6D3  mov      rbx, qword ptr [rbx]
0065C6D6  test     rbx, rbx
0065C6D9  je       0x65c72c  ; -> 0065C72C
0065C6DB  cmp      dword ptr [rbx + 0x28], edx
0065C6DE  jne      0x65c6e6  ; -> 0065C6E6
0065C6E0  cmp      dword ptr [rbx + 0x2c], r8d
0065C6E4  je       0x65c71a  ; -> 0065C71A
0065C6E6  mov      rcx, rbx
0065C6E9  call     0x625f00  ; -> 00625F00 fn
0065C6EE  test     al, al
0065C6F0  je       0x65c6fe  ; -> 0065C6FE
0065C6F2  mov      rcx, rbx
0065C6F5  call     0x62bcb0  ; -> 0062BCB0 fn
0065C6FA  test     eax, eax
0065C6FC  jne      0x65c731  ; -> 0065C731
0065C6FE  mov      r9, qword ptr [rbx]
0065C701  mov      r8d, edi
0065C704  mov      edx, esi
0065C706  mov      dword ptr [rsp + 0x20], 0
0065C70E  mov      rcx, rbx
0065C711  call     0x60dd70  ; -> 0060DD70 fn
0065C716  test     eax, eax
0065C718  jne      0x65c731  ; -> 0065C731
0065C71A  xor      eax, eax
0065C71C  mov      rbx, qword ptr [rsp + 0x40]
0065C721  mov      rsi, qword ptr [rsp + 0x48]
0065C726  add      rsp, 0x30
0065C72A  pop      rdi
0065C72B  ret      
0065C72C  mov      eax, 1
0065C731  mov      rbx, qword ptr [rsp + 0x40]
0065C736  mov      rsi, qword ptr [rsp + 0x48]
0065C73B  add      rsp, 0x30
0065C73F  pop      rdi
0065C740  ret      
```
