# Homing pack: `06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-how-the-engine-chooses-3d-or-flat-movement.json`.

Bodies: 6. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001AD670 (101 B, extent 001AD670-001AD6D5)

Entered from (direct sites whose caller this page cites): `0017F5B0` + 0x23 (jmp; `0017F5B0` is cited on this page)
Other direct sites: none

Host context: "B7E4C'), '0025A5F0' + '0036D840' ('003B7E55'/'003B7E5C'), '003588B0' on '[02EBCBE0]' ('003B7E6F'), '00265020' ('003B7E8B'), then '003B7F40' on '02EBCAC0' and on '[02EBCC68]' ('003B7EB8'/'003B7EDC'), '0017F5B0' ('003B7EF3'), '002EB030' on '02EBCBC0' ('003B7F0F').  | member | role | interior | | --- | --- | --- | | '003B7E20' | the setup body itself — the thunk's target; see the call list above | ['003B7E4C'](../../_index/ADDRESS-INDEX.md"

```
001AD670  push     rbx
001AD672  sub      rsp, 0x20
001AD676  mov      byte ptr [rcx + 0x244], dl
001AD67C  xor      ebx, ebx
001AD67E  call     0x1a9930  ; -> 001A9930 fn
001AD683  cmp      dword ptr [rax + 0x20], ebx
001AD686  jle      0x1ad6cf  ; -> 001AD6CF
001AD688  mov      qword ptr [rsp + 0x30], rdi
001AD68D  nop      dword ptr [rax]
001AD690  call     0x189120  ; -> 00189120 fn
001AD695  xor      edi, edi
001AD697  cmp      byte ptr [rax + 0x1c], dil
001AD69B  setne    dil
001AD69F  call     0x1a9930  ; -> 001A9930 fn
001AD6A4  mov      rcx, rax
001AD6A7  mov      r8d, ebx
001AD6AA  mov      edx, edi
001AD6AC  call     0x1a7600  ; -> 001A7600 fn
001AD6B1  test     rax, rax
001AD6B4  je       0x1ad6be  ; -> 001AD6BE
001AD6B6  mov      rcx, rax
001AD6B9  call     0x1e6480  ; -> 001E6480 fn
001AD6BE  inc      ebx
001AD6C0  call     0x1a9930  ; -> 001A9930 fn
001AD6C5  cmp      ebx, dword ptr [rax + 0x20]
001AD6C8  jl       0x1ad690  ; -> 001AD690
001AD6CA  mov      rdi, qword ptr [rsp + 0x30]
001AD6CF  add      rsp, 0x20
001AD6D3  pop      rbx
001AD6D4  ret      
```

## 00358420 (38 B, extent 00358420-00358446)

Entered from (direct sites whose caller this page cites): `00262870` + 0x1C (call; `00262870` is cited on this page)
Other direct sites: none

Host context: " party apart and put it back.       - '02B40530' (A): the initialiser '003B6ED0' and the 7-byte setter '003B7E10', whose callers are all engine code (§10:         '0024B6F0', '0024C6B0', '0024C870', '00262870', '003B8670').       - '02B40534' (B), from a full RIP-relative census with eight store sites in eight functions (the register's "nine"         was not reproduced): the initialiser (1), the setter '003B7E00' (argument; one caller, "

```
00358420  sub      rsp, 0x28
00358424  mov      edx, 1
00358429  xor      ecx, ecx
0035842B  call     0x358450  ; -> 00358450 fn
00358430  xor      edx, edx
00358432  lea      ecx, [rdx + 1]
00358435  call     0x358450  ; -> 00358450 fn
0035843A  mov      byte ptr [rip + 0x1f6fb58], 0  ; -> 022C7F99
00358441  add      rsp, 0x28
00358445  ret      
```

## 003631A0 (13 B, extent 003631A0-003631AD)

Entered from (direct sites whose caller this page cites): `00262870` + 0x17 (call; `00262870` is cited on this page)
Other direct sites: `00341460` + 0x39 (jmp); `003417C0` + 0x24 (jmp); `00341D00` + 0x14 (jmp)

Host context: " party apart and put it back.       - '02B40530' (A): the initialiser '003B6ED0' and the 7-byte setter '003B7E10', whose callers are all engine code (§10:         '0024B6F0', '0024C6B0', '0024C870', '00262870', '003B8670').       - '02B40534' (B), from a full RIP-relative census with eight store sites in eight functions (the register's "nine"         was not reproduced): the initialiser (1), the setter '003B7E00' (argument; one caller, "

```
003631A0  mov      byte ptr [rip + 0x1f688eb], cl  ; -> 022CBA91
003631A6  mov      dword ptr [rip + 0x1f688d8], edx  ; -> 022CBA84
003631AC  ret      
```

## 00363B20 (17 B, extent 00363B20-00363B31)

Entered from (direct sites whose caller this page cites): `00262870` + 0xE (call; `00262870` is cited on this page)
Other direct sites: `00341460` + 0x23 (call); `003417C0` + 0x13 (call); `00341D00` + 0x7 (call)

Host context: " party apart and put it back.       - '02B40530' (A): the initialiser '003B6ED0' and the 7-byte setter '003B7E10', whose callers are all engine code (§10:         '0024B6F0', '0024C6B0', '0024C870', '00262870', '003B8670').       - '02B40534' (B), from a full RIP-relative census with eight store sites in eight functions (the register's "nine"         was not reproduced): the initialiser (1), the setter '003B7E00' (argument; one caller, "

```
00363B20  test     ecx, ecx
00363B22  mov      eax, 0xb4
00363B27  cmovg    eax, ecx
00363B2A  mov      dword ptr [rip + 0x1f68000], eax  ; -> 022CBB30
00363B30  ret      
```

## 003B7510 (196 B, extent 003B7510-003B75D4)

Entered from (direct sites whose caller this page cites): `003B6F30` + 0x23 (jmp; `003B6F30` is cited on this page); `003B7080` + 0x28 (jmp; `003B7080` is cited on this page)
Other direct sites: none

Host context: "ch the body of a script verb, named from [the verb table](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv):          | writer | stores | verb |         |---|---|---|         | '003B6F30' ('003B6F37') | 0 | '0x202' 'disposepartywithoutcontrol' |         | '003B7080' ('003B7089') | 0 | '0x2A3' 'duplicatepartyinfo_spattack' |         | '003B72F0' ('003B7308') | 0 ('xor ebx, ebx' just before) | '0x232' 'capturepartyfo" / "tive-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv):          | writer | stores | verb |         |---|---|---|         | '003B6F30' ('003B6F37') | 0 | '0x202' 'disposepartywithoutcontrol' |         | '003B7080' ('003B7089') | 0 | '0x2A3' 'duplicatepartyinfo_spattack' |         | '003B72F0' ('003B7308') | 0 ('xor ebx, ebx' just before) | '0x232' 'capturepartyforsummon' |         | '003B7E20' ('003B7E4C') | 0 (same) | '0x191' 'setpossummon"

```
003B7510  push     rsi
003B7512  sub      rsp, 0x20
003B7516  xor      esi, esi
003B7518  cmp      dword ptr [rip + 0x2b05582], esi  ; -> 02EBCAA0
003B751E  jle      0x3b75ce  ; -> 003B75CE
003B7524  mov      qword ptr [rsp + 0x30], rbx
003B7529  mov      qword ptr [rsp + 0x40], r14
003B752E  lea      r14, [rip + 0x2b0554b]  ; -> 02EBCA80
003B7535  mov      qword ptr [rsp + 0x38], rdi
003B753A  nop      word ptr [rax + rax]
003B7540  mov      rbx, qword ptr [r14]
003B7543  test     rbx, rbx
003B7546  je       0x3b75b1  ; -> 003B75B1
003B7548  mov      rcx, rbx
003B754B  call     0x359b80  ; -> 00359B80 fn
003B7550  mov      rdi, rax
003B7553  test     rax, rax
003B7556  je       0x3b75b1  ; -> 003B75B1
003B7558  lea      r9, [rax + 8]
003B755C  mov      rdx, rax
003B755F  lea      r8, [rax + 4]
003B7563  mov      rcx, rbx
003B7566  call     0x265020  ; -> 00265020 fn
003B756B  lea      r9, [rdi + 0x18]
003B756F  mov      rcx, rbx
003B7572  lea      r8, [rdi + 0x14]
003B7576  lea      rdx, [rdi + 0x10]
003B757A  call     0x265240  ; -> 00265240 fn
003B757F  mov      rcx, rbx
003B7582  call     0x2e9be0  ; -> 002E9BE0 fn
003B7587  mov      rcx, rbx
003B758A  mov      byte ptr [rdi + 0x64], al
003B758D  call     0x263cc0  ; -> 00263CC0 fn
003B7592  mov      rcx, rbx
003B7595  movss    dword ptr [rdi + 0x34], xmm0
003B759A  call     0x265200  ; -> 00265200 fn
003B759F  mov      rcx, rbx
003B75A2  movss    dword ptr [rdi + 0x24], xmm0
003B75A7  call     0x263cc0  ; -> 00263CC0 fn
003B75AC  movss    dword ptr [rdi + 0x34], xmm0
003B75B1  inc      esi
003B75B3  add      r14, 8
003B75B7  cmp      esi, dword ptr [rip + 0x2b054e3]  ; -> 02EBCAA0
003B75BD  jl       0x3b7540  ; -> 003B7540
003B75BF  mov      r14, qword ptr [rsp + 0x40]
003B75C4  mov      rdi, qword ptr [rsp + 0x38]
003B75C9  mov      rbx, qword ptr [rsp + 0x30]
003B75CE  add      rsp, 0x20
003B75D2  pop      rsi
003B75D3  ret      
```

## 003DB150 (94 B, extent 003DB150-003DB1AE)

Entered from (direct sites whose caller this page cites): `002E54A0` + 0xD7 (call; `002E54A0` is cited on this page)
Other direct sites: none

Host context: "ment_IntegratePositionAndMeasureDisplacement  314 B   calls 00264460 : YES  (site 002E56B7) '''  **How it happened:** '002E5380' was carried over from the K-4 open question, which names it alongside '002E54A0', while the caller list came from an xref census that gives call *sites* — '002E56B7', which falls inside '002E5610'. Two rows of source data were combined, so this is a transposition rather than a mistyped label, and the fix is th"

```
003DB150  movss    xmm0, dword ptr [rcx]
003DB154  addss    xmm0, dword ptr [r8]
003DB159  movss    dword ptr [r8], xmm0
003DB15E  movss    xmm1, dword ptr [rcx + 4]
003DB163  addss    xmm1, dword ptr [r8 + 4]
003DB169  movss    dword ptr [r8 + 4], xmm1
003DB16F  movss    xmm0, dword ptr [rcx + 8]
003DB174  addss    xmm0, dword ptr [r8 + 8]
003DB17A  movss    dword ptr [r8 + 8], xmm0
003DB180  test     rdx, rdx
003DB183  je       0x3db1ad  ; -> 003DB1AD
003DB185  mov      eax, dword ptr [r8]
003DB188  mov      dword ptr [rdx + 0x30], eax
003DB18B  mov      eax, dword ptr [r8 + 4]
003DB18F  mov      dword ptr [rdx + 0x34], eax
003DB192  mov      eax, dword ptr [r8 + 8]
003DB196  mov      dword ptr [rdx + 0x38], eax
003DB199  mov      eax, dword ptr [r8 + 4]
003DB19D  mov      dword ptr [rdx + 0xac], eax
003DB1A3  or       eax, 0xffffffff
003DB1A6  mov      word ptr [rdx + 0x82], ax
003DB1AD  ret      
```
