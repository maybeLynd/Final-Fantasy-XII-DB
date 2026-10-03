# Homing pack: `17-Presentation-Rendering/Effect-File-Formats/the-menu-effect-registry.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-menu-effect-registry.json`.

Bodies: 7. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002C9F80 (65 B, extent 002C9F80-002C9FC1)

Entered from (direct sites whose caller this page cites): `00565E00` + 0x6DA (call; `00565E00` is cited on this page)
Other direct sites: none

Host context: "registry arms issue. Interior anchor '002CDF01' (the '00244F50' call).  ## SWE2-EC7-102 update (2026-09-20) - '00295D20' measured  '00295D20' (39 B) is the three-call command sequence '0055E9E0' and '00565E00' run: '0029E750(0xC8)', then '0029E330' on the argument, then a '0029E730(0, 0)' tail - the id-then-verb-then-close idiom the effect-registry paths share. Interior anchor '00295D2D' (the '0029E750' call).  ## SWE2-EC7-106 update (2"

```
002C9F80  test     rcx, rcx
002C9F83  je       0x2c9fc0  ; -> 002C9FC0
002C9F85  mov      r10, qword ptr [rcx + 8]
002C9F89  xor      eax, eax
002C9F8B  movsx    ecx, word ptr [rcx]
002C9F8E  mov      r9, r10
002C9F91  test     ecx, ecx
002C9F93  jle      0x2c9fc0  ; -> 002C9FC0
002C9F95  cmp      edx, dword ptr [r9]
002C9F98  je       0x2c9fa5  ; -> 002C9FA5
002C9F9A  inc      eax
002C9F9C  add      r9, 0x20
002C9FA0  cmp      eax, ecx
002C9FA2  jl       0x2c9f95  ; -> 002C9F95
002C9FA4  ret      
002C9FA5  test     eax, eax
002C9FA7  js       0x2c9fc0  ; -> 002C9FC0
002C9FA9  cdqe     
002C9FAB  shl      rax, 5
002C9FAF  mov      rcx, qword ptr [rax + r10 + 8]
002C9FB4  test     rcx, rcx
002C9FB7  je       0x2c9fc0  ; -> 002C9FC0
002C9FB9  mov      dword ptr [rcx + 0xe4], r8d
002C9FC0  ret      
```

## 002C9FD0 (51 B, extent 002C9FD0-002CA003)

Entered from (direct sites whose caller this page cites): `00565E00` + 0x69D (call; `00565E00` is cited on this page)
Other direct sites: none

Host context: "registry arms issue. Interior anchor '002CDF01' (the '00244F50' call).  ## SWE2-EC7-102 update (2026-09-20) - '00295D20' measured  '00295D20' (39 B) is the three-call command sequence '0055E9E0' and '00565E00' run: '0029E750(0xC8)', then '0029E330' on the argument, then a '0029E730(0, 0)' tail - the id-then-verb-then-close idiom the effect-registry paths share. Interior anchor '00295D2D' (the '0029E750' call).  ## SWE2-EC7-106 update (2"

```
002C9FD0  xor      eax, eax
002C9FD2  mov      r10, rcx
002C9FD5  cmp      ax, word ptr [rcx]
002C9FD8  jge      0x2ca002  ; -> 002CA002
002C9FDA  mov      r9d, eax
002C9FDD  nop      dword ptr [rax]
002C9FE0  mov      r8, qword ptr [r10 + 8]
002C9FE4  mov      rcx, qword ptr [r9 + r8 + 8]
002C9FE9  test     rcx, rcx
002C9FEC  je       0x2c9ff4  ; -> 002C9FF4
002C9FEE  mov      dword ptr [rcx + 0xe4], edx
002C9FF4  movsx    ecx, word ptr [r10]
002C9FF8  inc      eax
002C9FFA  add      r9, 0x20
002C9FFE  cmp      eax, ecx
002CA000  jl       0x2c9fe0  ; -> 002C9FE0
002CA002  ret      
```

## 00424320 (65 B, extent 00424320-00424361)

Entered from (direct sites whose caller this page cites): `003B8260` + 0x227 (call; `003B8260` is cited on this page)
Other direct sites: `00429A50` + 0x57 (call); `00429A50` + 0x8C (call); `0042DCA0` + 0x1E (jmp)

Host context: "'value' to '[instance + 0x338]' of the record with that id ('003B2F80') |  '0024C460' and '0024B270' are two of the ~~ten~~ **eleven** writers of the effect instance list '02EBEF88'. The eleventh is '003B8260' ('003B860D'), which a census scoped to '0024xxxx' missed; corrected 2026-09-14 (AUDITSEM-CONTRA-FABLE-EFX-REGISTRY) ([effect element type dispatch](effect-element-type-dispatch.md) §2.4). **So registry instances are ordinary effec"

```
00424320  push     rbx
00424322  sub      rsp, 0x20
00424326  mov      ebx, dword ptr [rcx + 0x18]
00424329  cmp      ebx, -1
0042432C  je       0x42435b  ; -> 0042435B
0042432E  mov      ecx, dword ptr [rcx + 0x10]
00424331  call     0x20e600  ; -> 0020E600 fn
00424336  cmp      ebx, -1
00424339  je       0x42435b  ; -> 0042435B
0042433B  mov      rcx, qword ptr [rax + 0xd98]
00424342  mov      edx, ebx
00424344  call     0x2ed570  ; -> 002ED570 fn
00424349  test     rax, rax
0042434C  je       0x42435b  ; -> 0042435B
0042434E  mov      rcx, rax
00424351  add      rsp, 0x20
00424355  pop      rbx
00424356  jmp      0x3723b0  ; -> 003723B0 fn
0042435B  add      rsp, 0x20
0042435F  pop      rbx
00424360  ret      
```

## 00563FC0 (77 B, extent 00563FC0-0056400D)

Entered from (direct sites whose caller this page cites): `00565E00` + 0x4F6 (call; `00565E00` is cited on this page); `00565E00` + 0x5CF (call; `00565E00` is cited on this page)
Other direct sites: none

Host context: "registry arms issue. Interior anchor '002CDF01' (the '00244F50' call).  ## SWE2-EC7-102 update (2026-09-20) - '00295D20' measured  '00295D20' (39 B) is the three-call command sequence '0055E9E0' and '00565E00' run: '0029E750(0xC8)', then '0029E330' on the argument, then a '0029E730(0, 0)' tail - the id-then-verb-then-close idiom the effect-registry paths share. Interior anchor '00295D2D' (the '0029E750' call).  ## SWE2-EC7-106 update (2" / "registry arms issue. Interior anchor '002CDF01' (the '00244F50' call).  ## SWE2-EC7-102 update (2026-09-20) - '00295D20' measured  '00295D20' (39 B) is the three-call command sequence '0055E9E0' and '00565E00' run: '0029E750(0xC8)', then '0029E330' on the argument, then a '0029E730(0, 0)' tail - the id-then-verb-then-close idiom the effect-registry paths share. Interior anchor '00295D2D' (the '0029E750' call).  ## SWE2-EC7-106 update (2"

```
00563FC0  xor      r9d, r9d
00563FC3  lea      r10, [rip + 0x7bf3d6]  ; -> 00D233A0
00563FCA  mov      edx, r9d
00563FCD  mov      r8, r10
00563FD0  movzx    eax, word ptr [r8]
00563FD4  cmp      ecx, eax
00563FD6  je       0x563fe5  ; -> 00563FE5
00563FD8  inc      edx
00563FDA  add      r8, 4
00563FDE  cmp      edx, 0x21
00563FE1  jb       0x563fd0  ; -> 00563FD0
00563FE3  jmp      0x563fee  ; -> 00563FEE
00563FE5  movsxd   rax, edx
00563FE8  movzx    r9d, word ptr [r10 + rax*4 + 2]
00563FEE  mov      rax, qword ptr [rip + 0x1b36c3b]  ; -> 0209AC30
00563FF5  mov      rcx, qword ptr [rax + r9*8 + 0x170]
00563FFD  test     rcx, rcx
00564000  je       0x56400c  ; -> 0056400C
00564002  test     byte ptr [rcx + 0x7c], 0x20
00564006  je       0x244f00  ; -> 00244F00 fn
0056400C  ret      
```

## 00564A60 (87 B, extent 00564A60-00564AB7)

Entered from (direct sites whose caller this page cites): `00565E00` + 0x5A1 (call; `00565E00` is cited on this page)
Other direct sites: none

Host context: "registry arms issue. Interior anchor '002CDF01' (the '00244F50' call).  ## SWE2-EC7-102 update (2026-09-20) - '00295D20' measured  '00295D20' (39 B) is the three-call command sequence '0055E9E0' and '00565E00' run: '0029E750(0xC8)', then '0029E330' on the argument, then a '0029E730(0, 0)' tail - the id-then-verb-then-close idiom the effect-registry paths share. Interior anchor '00295D2D' (the '0029E750' call).  ## SWE2-EC7-106 update (2"

```
00564A60  xor      r9d, r9d
00564A63  lea      r10, [rip + 0x7be936]  ; -> 00D233A0
00564A6A  mov      edx, r9d
00564A6D  mov      r8, r10
00564A70  movzx    eax, word ptr [r8]
00564A74  cmp      ecx, eax
00564A76  je       0x564a88  ; -> 00564A88
00564A78  inc      edx
00564A7A  add      r8, 4
00564A7E  cmp      edx, 0x21
00564A81  jb       0x564a70  ; -> 00564A70
00564A83  mov      eax, r9d
00564A86  jmp      0x564a91  ; -> 00564A91
00564A88  movsxd   rcx, edx
00564A8B  movzx    eax, word ptr [r10 + rcx*4 + 2]
00564A91  mov      rcx, qword ptr [rip + 0x1b36198]  ; -> 0209AC30
00564A98  mov      edx, eax
00564A9A  mov      rax, qword ptr [rcx + rdx*8 + 0x170]
00564AA2  test     rax, rax
00564AA5  je       0x564ab6  ; -> 00564AB6
00564AA7  cmp      qword ptr [rax + 0xe0], r9
00564AAE  setne    r9b
00564AB2  mov      eax, r9d
00564AB5  ret      
00564AB6  ret      
```

## 00565190 (79 B, extent 00565190-005651DF)

Entered from (direct sites whose caller this page cites): `00565E00` + 0x480 (call; `00565E00` is cited on this page)
Other direct sites: none

Host context: "registry arms issue. Interior anchor '002CDF01' (the '00244F50' call).  ## SWE2-EC7-102 update (2026-09-20) - '00295D20' measured  '00295D20' (39 B) is the three-call command sequence '0055E9E0' and '00565E00' run: '0029E750(0xC8)', then '0029E330' on the argument, then a '0029E730(0, 0)' tail - the id-then-verb-then-close idiom the effect-registry paths share. Interior anchor '00295D2D' (the '0029E750' call).  ## SWE2-EC7-106 update (2"

```
00565190  xor      r9d, r9d
00565193  lea      r10, [rip + 0x7be206]  ; -> 00D233A0
0056519A  mov      edx, r9d
0056519D  mov      r8, r10
005651A0  movzx    eax, word ptr [r8]
005651A4  cmp      ecx, eax
005651A6  je       0x5651b5  ; -> 005651B5
005651A8  inc      edx
005651AA  add      r8, 4
005651AE  cmp      edx, 0x21
005651B1  jb       0x5651a0  ; -> 005651A0
005651B3  jmp      0x5651be  ; -> 005651BE
005651B5  movsxd   rax, edx
005651B8  movzx    r9d, word ptr [r10 + rax*4 + 2]
005651BE  mov      rax, qword ptr [rip + 0x1b35a6b]  ; -> 0209AC30
005651C5  mov      rcx, qword ptr [rax + r9*8 + 0x170]
005651CD  test     rcx, rcx
005651D0  je       0x5651dc  ; -> 005651DC
005651D2  mov      edx, 1
005651D7  jmp      0x564e10  ; -> 00564E10 fn
005651DC  xor      eax, eax
005651DE  ret      
```

## 005659B0 (71 B, extent 005659B0-005659F7)

Entered from (direct sites whose caller this page cites): `00565E00` + 0x56A (call; `00565E00` is cited on this page)
Other direct sites: none

Host context: "registry arms issue. Interior anchor '002CDF01' (the '00244F50' call).  ## SWE2-EC7-102 update (2026-09-20) - '00295D20' measured  '00295D20' (39 B) is the three-call command sequence '0055E9E0' and '00565E00' run: '0029E750(0xC8)', then '0029E330' on the argument, then a '0029E730(0, 0)' tail - the id-then-verb-then-close idiom the effect-registry paths share. Interior anchor '00295D2D' (the '0029E750' call).  ## SWE2-EC7-106 update (2"

```
005659B0  xor      r9d, r9d
005659B3  lea      r10, [rip + 0x7bd9e6]  ; -> 00D233A0
005659BA  mov      edx, r9d
005659BD  mov      r8, r10
005659C0  movzx    eax, word ptr [r8]
005659C4  cmp      ecx, eax
005659C6  je       0x5659d5  ; -> 005659D5
005659C8  inc      edx
005659CA  add      r8, 4
005659CE  cmp      edx, 0x21
005659D1  jb       0x5659c0  ; -> 005659C0
005659D3  jmp      0x5659de  ; -> 005659DE
005659D5  movsxd   rax, edx
005659D8  movzx    r9d, word ptr [r10 + rax*4 + 2]
005659DE  mov      rax, qword ptr [rip + 0x1b3524b]  ; -> 0209AC30
005659E5  mov      rcx, qword ptr [rax + r9*8 + 0x170]
005659ED  test     rcx, rcx
005659F0  jne      0x2470d0  ; -> 002470D0 fn
005659F6  ret      
```
