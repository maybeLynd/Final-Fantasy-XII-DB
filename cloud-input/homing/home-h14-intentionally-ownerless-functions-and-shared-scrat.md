# Homing pack: `00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-intentionally-ownerless-functions-and-shared-scrat.json`.

Bodies: 10. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

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

## 002DF170 (17 B, extent 002DF170-002DF181)

Entered from (direct sites whose caller this page cites): `003B3EA0` + 0xE (call; `003B3EA0` is cited on this page)
Other direct sites: `0034D970` + 0x2D (jmp)

Host context: "word_global2)', and '[rcx+0xC]' takes 'cvtdq2ps(dword_global1)' - three globals folded into a scale record, call-free. Interior anchor '003ED11F' (the 'divss').  ## SWE2-EC7-89 update (2026-09-20) - '003B3EA0' scratch-slot claim measured  '003B3EA0' (107 B) is the slot claim the shared-scratch callers run: '002DF170()' first, then the '02EBCC80..02EBCD80' ring is scanned 8-at-a-time for a clear flag byte; the free slot takes 'byte'=1, '"

```
002DF170  xor      r8d, r8d
002DF173  mov      r9d, edx
002DF176  mov      edx, ecx
002DF178  lea      ecx, [r8 + 1]
002DF17C  jmp      0x1dbf50  ; -> 001DBF50 fn
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

## 00471310 (18 B, extent 00471310-00471322)

Entered from (direct sites whose caller this page cites): `003E1610` + 0x1E7 (jmp; `003E1610` is cited on this page)
Other direct sites: none

Host context: "5A0'–'B4' cells + '0026A430'/'0026AF80'), '00333520', '00333640', '003A4070' ('02096A20' + '003B0BF0'), '003A7F60' ('02EBEF98' + '003697F0'), '003B8260' (1,028 B — '0020E600' ×7 + resolve '003E1350'/'003E1610' + '003B3CA0' ×2, '00D115BC'–'E0' table + '02EBA4F0'; interior verified 2026-09-17, SWE2-FRONTIER — '0031E880' first at ['003B82D7'](../../_index/ADDRESS-INDEX.md)), '003B99D0' (1,501 B — 24 helpers, '020926F4' + '02EBA4F0'; interi"

```
00471310  mov      eax, 1
00471315  mov      word ptr [rcx + 0xc], 0
0047131B  mov      word ptr [rcx + 2], ax
0047131F  mov      byte ptr [rcx], al
00471321  ret      
```

## 004715D0 (31 B, extent 004715D0-004715EF)

Entered from (direct sites whose caller this page cites): `003E1610` + 0x129 (jmp; `003E1610` is cited on this page)
Other direct sites: none

Host context: "5A0'–'B4' cells + '0026A430'/'0026AF80'), '00333520', '00333640', '003A4070' ('02096A20' + '003B0BF0'), '003A7F60' ('02EBEF98' + '003697F0'), '003B8260' (1,028 B — '0020E600' ×7 + resolve '003E1350'/'003E1610' + '003B3CA0' ×2, '00D115BC'–'E0' table + '02EBA4F0'; interior verified 2026-09-17, SWE2-FRONTIER — '0031E880' first at ['003B82D7'](../../_index/ADDRESS-INDEX.md)), '003B99D0' (1,501 B — 24 helpers, '020926F4' + '02EBA4F0'; interi"

```
004715D0  cmp      byte ptr [rcx], 0
004715D3  jne      0x4715ee  ; -> 004715EE
004715D5  mov      eax, dword ptr [rcx + 0x10]
004715D8  mov      dword ptr [rcx + 0x18], eax
004715DB  mov      eax, dword ptr [rcx + 0x14]
004715DE  mov      dword ptr [rcx + 0x1c], eax
004715E1  mov      dword ptr [rcx], 0x101
004715E7  mov      dword ptr [rcx + 0xc], 0x3f800000
004715EE  ret      
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

## 0051B950 (20 B, extent 0051B950-0051B964)

Entered from (direct sites whose caller this page cites): `003E1610` + 0x24D (jmp; `003E1610` is cited on this page)
Other direct sites: none

Host context: "5A0'–'B4' cells + '0026A430'/'0026AF80'), '00333520', '00333640', '003A4070' ('02096A20' + '003B0BF0'), '003A7F60' ('02EBEF98' + '003697F0'), '003B8260' (1,028 B — '0020E600' ×7 + resolve '003E1350'/'003E1610' + '003B3CA0' ×2, '00D115BC'–'E0' table + '02EBA4F0'; interior verified 2026-09-17, SWE2-FRONTIER — '0031E880' first at ['003B82D7'](../../_index/ADDRESS-INDEX.md)), '003B99D0' (1,501 B — 24 helpers, '020926F4' + '02EBA4F0'; interi"

```
0051B950  movzx    eax, byte ptr [rcx + 0x34]
0051B954  test     al, 1
0051B956  jne      0x51b963  ; -> 0051B963
0051B958  or       al, 1
0051B95A  mov      byte ptr [rcx + 0x34], al
0051B95D  xor      eax, eax
0051B95F  mov      word ptr [rcx + 0x30], ax
0051B963  ret      
```
