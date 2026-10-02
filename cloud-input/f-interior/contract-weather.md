# F-interior pack: `03-World-Area-Field/CONTRACT-weather.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-weather.json`.

Functions: 8. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: acfaf396a	SWE2-CONTRACT: DD residue batch 6 - the 02 top-level pages: atlas bit 7 is the texture-memory layout; inbox mentions: SWE2-CONTRACT.md, SWE2-DATA.md). OPUS read these before packing.

## 0029C530 (569 B, extent 0029C530-0029C769)

Page context: "-filed '00226BE0'.  **UI, PlatformOnlineAchievements and Spawn_Encounter_Lifecycle — CLIENT, seven edges on one getter.** 'WorldTransition_GetActiveOrPendingFieldId' is also read by: - the UI bodies '0029C530', '003C5F00', '003C80C0' and '003F92B0'; - the achievements body '003160C0'; - 'SpawnKeep_RotatePersistenceBanksForAreaTransition'.  *Tier 2: ledger names, sizes and 'edges.tsv', roles as this page reads them; no new body read (OPU"

```
0029C530  push     rbx
0029C532  sub      rsp, 0x20
0029C536  mov      rbx, rcx
0029C539  mov      ecx, dword ptr [rdx]
0029C53B  sub      ecx, 1
0029C53E  je       0x29c589  ; -> 0029C589
0029C540  sub      ecx, 1
0029C543  je       0x29c761  ; -> 0029C761
0029C549  sub      ecx, 1
0029C54C  je       0x29c761  ; -> 0029C761
0029C552  sub      ecx, 0xb
0029C555  je       0x29c579  ; -> 0029C579
0029C557  cmp      ecx, 1
0029C55A  je       0x29c569  ; -> 0029C569
0029C55C  mov      rcx, rbx
0029C55F  add      rsp, 0x20
0029C563  pop      rbx
0029C564  jmp      0x5c5230  ; -> 005C5230 fn
0029C569  or       word ptr [rbx + 0xe6], 4
0029C571  xor      eax, eax
0029C573  add      rsp, 0x20
0029C577  pop      rbx
0029C578  ret      
0029C579  or       word ptr [rbx + 0xe6], 8
0029C581  xor      eax, eax
0029C583  add      rsp, 0x20
0029C587  pop      rbx
0029C588  ret      
0029C589  mov      rax, qword ptr [rip + 0x1dfe6a0]  ; -> 0209AC30
0029C590  lea      rcx, [rbx + 0x50]
0029C594  mov      qword ptr [rsp + 0x30], rbp
0029C599  mov      r9, rbx
0029C59C  mov      qword ptr [rsp + 0x38], rsi
0029C5A1  mov      r8d, 0x14
0029C5A7  mov      qword ptr [rsp + 0x40], rdi
0029C5AC  mov      rdx, qword ptr [rax + 8]
0029C5B0  mov      qword ptr [rsp + 0x48], r14
0029C5B5  call     0x2432b0  ; -> 002432B0 fn
0029C5BA  movzx    ecx, word ptr [rax + 0xa]
0029C5BE  movzx    edx, word ptr [rax + 8]
0029C5C2  movsx    r8d, word ptr [rax + 6]
0029C5C7  test     rbx, rbx
0029C5CA  je       0x29c5ed  ; -> 0029C5ED
0029C5CC  movzx    eax, word ptr [rax + 4]
0029C5D0  mov      word ptr [rbx + 0x98], ax
0029C5D7  mov      word ptr [rbx + 0x9a], r8w
0029C5DF  mov      word ptr [rbx + 0x9c], dx
0029C5E6  mov      word ptr [rbx + 0x9e], cx
0029C5ED  call     0x3148f0  ; -> 003148F0 fn
0029C5F2  mov      ecx, eax
0029C5F4  mov      ebp, eax
0029C5F6  call     0x264f90  ; -> 00264F90 fn
0029C5FB  mov      ecx, eax
0029C5FD  call     0x254380  ; -> 00254380 fn
0029C602  mov      ecx, 0x5e
0029C607  mov      r14d, eax
0029C60A  call     0x32a8a0  ; -> 0032A8A0 fn
0029C60F  test     eax, eax
0029C611  je       0x29c62d  ; -> 0029C62D
0029C613  call     0x314910  ; -> 00314910 fn
0029C618  mov      ecx, eax
0029C61A  call     0x3778b0  ; -> 003778B0 fn
0029C61F  xor      edi, edi
0029C621  mov      rcx, rax
0029C624  test     rbx, rbx
0029C627  jne      0x29c642  ; -> 0029C642
0029C629  mov      esi, edi
0029C62B  jmp      0x29c64a  ; -> 0029C64A
0029C62D  mov      ecx, ebp
0029C62F  call     0x3778b0  ; -> 003778B0 fn
0029C634  xor      edi, edi
0029C636  mov      rcx, rax
0029C639  test     rbx, rbx
0029C63C  jne      0x29c642  ; -> 0029C642
0029C63E  mov      esi, edi
0029C640  jmp      0x29c64a  ; -> 0029C64A
0029C642  mov      rax, qword ptr [rbx + 0x60]
0029C646  mov      rsi, qword ptr [rax + 0x18]
0029C64A  mov      qword ptr [rsi + 0x18], rcx
0029C64E  xor      ecx, ecx
0029C650  call     0x20e620  ; -> 0020E620 fn
0029C655  mov      ecx, ebp
0029C657  mov      dword ptr [rsi + 0x20], eax
0029C65A  call     0x377b60  ; -> 00377B60 fn
0029C65F  mov      rbp, qword ptr [rsp + 0x30]
0029C664  mov      rcx, rax
0029C667  test     rbx, rbx
0029C66A  jne      0x29c671  ; -> 0029C671
0029C66C  mov      rsi, rdi
0029C66F  jmp      0x29c679  ; -> 0029C679
0029C671  mov      rax, qword ptr [rbx + 0x60]
0029C675  mov      rsi, qword ptr [rax + 0x20]
0029C679  mov      qword ptr [rsi + 0x18], rcx
0029C67D  xor      ecx, ecx
0029C67F  call     0x20e620  ; -> 0020E620 fn
0029C684  mov      dword ptr [rsi + 0x20], eax
0029C687  test     rbx, rbx
0029C68A  jne      0x29c691  ; -> 0029C691
0029C68C  mov      rsi, rdi
0029C68F  jmp      0x29c699  ; -> 0029C699
0029C691  mov      rax, qword ptr [rbx + 0x60]
0029C695  mov      rsi, qword ptr [rax + 0x28]
0029C699  mov      ecx, r14d
0029C69C  call     0x2543d0  ; -> 002543D0 fn
0029C6A1  mov      r14, qword ptr [rsp + 0x48]
0029C6A6  mov      word ptr [rsi + 0xa], ax
0029C6AA  mov      rsi, qword ptr [rsp + 0x38]
0029C6AF  test     rbx, rbx
0029C6B2  jne      0x29c6b9  ; -> 0029C6B9
0029C6B4  mov      rcx, rdi
0029C6B7  jmp      0x29c6c1  ; -> 0029C6C1
0029C6B9  mov      rax, qword ptr [rbx + 0x60]
0029C6BD  mov      rcx, qword ptr [rax + 0x18]
0029C6C1  mov      eax, dword ptr [rcx + 0x24]
0029C6C4  mov      edx, 0xa0
0029C6C9  mov      dword ptr [rbx + 0xc0], eax
0029C6CF  movzx    eax, word ptr [rcx + 0xc]
0029C6D3  mov      word ptr [rbx + 0xc4], ax
0029C6DA  movzx    eax, word ptr [rcx + 0xe]
0029C6DE  mov      word ptr [rbx + 0xc6], ax
0029C6E5  movzx    eax, word ptr [rcx + 0x10]
0029C6E9  mov      word ptr [rbx + 0xc8], ax
0029C6F0  movzx    eax, word ptr [rcx + 0x12]
0029C6F4  mov      word ptr [rbx + 0xca], ax
0029C6FB  mov      rax, qword ptr [rbx + 0x60]
0029C6FF  mov      rcx, qword ptr [rax + 0x20]
0029C703  mov      eax, dword ptr [rcx + 0x24]
0029C706  mov      dword ptr [rbx + 0xd0], eax
0029C70C  movzx    eax, word ptr [rcx + 0xc]
0029C710  mov      word ptr [rbx + 0xd4], ax
0029C717  movzx    eax, word ptr [rcx + 0xe]
0029C71B  mov      word ptr [rbx + 0xd6], ax
0029C722  movzx    eax, word ptr [rcx + 0x10]
0029C726  mov      word ptr [rbx + 0xd8], ax
0029C72D  movzx    eax, word ptr [rcx + 0x12]
0029C731  mov      rcx, rbx
0029C734  mov      word ptr [rbx + 0xda], ax
0029C73B  call     0x247930  ; -> 00247930 fn
0029C740  mov      ecx, 3
0029C745  call     0x2735e0  ; -> 002735E0 fn
0029C74A  mov      rdx, rax
0029C74D  mov      rcx, rbx
0029C750  call     0x247570  ; -> 00247570 fn
0029C755  mov      word ptr [rbx + 0xe0], di
0029C75C  mov      rdi, qword ptr [rsp + 0x40]
0029C761  xor      eax, eax
0029C763  add      rsp, 0x20
0029C767  pop      rbx
0029C768  ret      
```

## 0034B7C0 (145 B, extent 0034B7C0-0034B851)

Page context: "apply '0026D8F0' / '0026D910'. - Script handlers also call:   - the event notifier '003601C0', from '00345140', '003464D0', '0034C370' and '003506A0';   - the '02099DBC' reader path '002E9D90', from '0034B7C0', '0034C210' and '0034CA40';   - the '02099DB8' reader '00264180';   - '00265920' and '002E3D40';   - the field-id getter and 'MapRef_GetPrimaryFieldValue';   - '00265450', the second '02099DBC' writer '0026AB40', '0026FAD0' and '0"

```
0034B7C0  mov      qword ptr [rsp + 8], rbx
0034B7C5  mov      qword ptr [rsp + 0x10], rbp
0034B7CA  mov      qword ptr [rsp + 0x18], rsi
0034B7CF  mov      qword ptr [rsp + 0x20], rdi
0034B7D4  push     r14
0034B7D6  sub      rsp, 0x20
0034B7DA  mov      rcx, r9
0034B7DD  mov      rdi, r9
0034B7E0  mov      rsi, rdx
0034B7E3  call     0x267e10  ; -> 00267E10 fn
0034B7E8  mov      rcx, rdi
0034B7EB  mov      ebp, eax
0034B7ED  call     0x267e10  ; -> 00267E10 fn
0034B7F2  mov      rcx, rdi
0034B7F5  mov      r14d, eax
0034B7F8  call     0x267e10  ; -> 00267E10 fn
0034B7FD  mov      rcx, rdi
0034B800  mov      ebx, eax
0034B802  call     0x267e10  ; -> 00267E10 fn
0034B807  mov      r9d, ebx
0034B80A  mov      r8d, eax
0034B80D  mov      edx, 1
0034B812  mov      rcx, rsi
0034B815  call     0x2e9d90  ; -> 002E9D90 fn
0034B81A  movzx    ecx, byte ptr [rsi + 0x15]
0034B81E  mov      ebx, eax
0034B820  call     0x267310  ; -> 00267310 fn
0034B825  test     eax, eax
0034B827  jne      0x34b836  ; -> 0034B836
0034B829  mov      r8d, ebp
0034B82C  mov      edx, r14d
0034B82F  mov      ecx, ebx
0034B831  call     0x3a0e20  ; -> 003A0E20 fn
0034B836  mov      rbx, qword ptr [rsp + 0x30]
0034B83B  mov      rbp, qword ptr [rsp + 0x38]
0034B840  mov      rsi, qword ptr [rsp + 0x40]
0034B845  mov      rdi, qword ptr [rsp + 0x48]
0034B84A  add      rsp, 0x20
0034B84E  pop      r14
0034B850  ret      
```

## 0034C210 (120 B, extent 0034C210-0034C288)

Page context: "8F0' / '0026D910'. - Script handlers also call:   - the event notifier '003601C0', from '00345140', '003464D0', '0034C370' and '003506A0';   - the '02099DBC' reader path '002E9D90', from '0034B7C0', '0034C210' and '0034CA40';   - the '02099DB8' reader '00264180';   - '00265920' and '002E3D40';   - the field-id getter and 'MapRef_GetPrimaryFieldValue';   - '00265450', the second '02099DBC' writer '0026AB40', '0026FAD0' and '003DE920'. - "

```
0034C210  mov      qword ptr [rsp + 8], rbx
0034C215  mov      qword ptr [rsp + 0x10], rbp
0034C21A  mov      qword ptr [rsp + 0x18], rsi
0034C21F  push     rdi
0034C220  sub      rsp, 0x20
0034C224  mov      rcx, r9
0034C227  mov      rbx, r9
0034C22A  mov      rdi, rdx
0034C22D  call     0x267e10  ; -> 00267E10 fn
0034C232  mov      rcx, rbx
0034C235  mov      esi, eax
0034C237  call     0x267e10  ; -> 00267E10 fn
0034C23C  mov      rcx, rbx
0034C23F  mov      ebp, eax
0034C241  call     0x267e10  ; -> 00267E10 fn
0034C246  xor      r9d, r9d
0034C249  mov      r8d, eax
0034C24C  mov      rcx, rdi
0034C24F  lea      edx, [r9 + 2]
0034C253  call     0x2e9d90  ; -> 002E9D90 fn
0034C258  movzx    ecx, byte ptr [rdi + 0x15]
0034C25C  mov      ebx, eax
0034C25E  call     0x267310  ; -> 00267310 fn
0034C263  test     eax, eax
0034C265  jne      0x34c273  ; -> 0034C273
0034C267  mov      r8d, esi
0034C26A  mov      edx, ebp
0034C26C  mov      ecx, ebx
0034C26E  call     0x3a0e20  ; -> 003A0E20 fn
0034C273  mov      rbx, qword ptr [rsp + 0x30]
0034C278  mov      rbp, qword ptr [rsp + 0x38]
0034C27D  mov      rsi, qword ptr [rsp + 0x40]
0034C282  add      rsp, 0x20
0034C286  pop      rdi
0034C287  ret      
```

## 0034CA40 (126 B, extent 0034CA40-0034CABE)

Page context: "0'. - Script handlers also call:   - the event notifier '003601C0', from '00345140', '003464D0', '0034C370' and '003506A0';   - the '02099DBC' reader path '002E9D90', from '0034B7C0', '0034C210' and '0034CA40';   - the '02099DB8' reader '00264180';   - '00265920' and '002E3D40';   - the field-id getter and 'MapRef_GetPrimaryFieldValue';   - '00265450', the second '02099DBC' writer '0026AB40', '0026FAD0' and '003DE920'. - The area initia"

```
0034CA40  mov      qword ptr [rsp + 8], rbx
0034CA45  mov      qword ptr [rsp + 0x10], rbp
0034CA4A  mov      qword ptr [rsp + 0x18], rsi
0034CA4F  push     rdi
0034CA50  sub      rsp, 0x20
0034CA54  mov      rcx, r9
0034CA57  mov      rbx, r9
0034CA5A  mov      rdi, rdx
0034CA5D  call     0x267e10  ; -> 00267E10 fn
0034CA62  mov      rcx, rbx
0034CA65  mov      esi, eax
0034CA67  call     0x267e10  ; -> 00267E10 fn
0034CA6C  mov      rcx, rbx
0034CA6F  mov      ebp, eax
0034CA71  call     0x267e10  ; -> 00267E10 fn
0034CA76  mov      rcx, rbx
0034CA79  call     0x267e10  ; -> 00267E10 fn
0034CA7E  xor      r9d, r9d
0034CA81  mov      r8d, eax
0034CA84  xor      edx, edx
0034CA86  mov      rcx, rdi
0034CA89  call     0x2e9d90  ; -> 002E9D90 fn
0034CA8E  movzx    ecx, byte ptr [rdi + 0x15]
0034CA92  mov      ebx, eax
0034CA94  call     0x267310  ; -> 00267310 fn
0034CA99  test     eax, eax
0034CA9B  jne      0x34caa9  ; -> 0034CAA9
0034CA9D  mov      r8d, esi
0034CAA0  mov      edx, ebp
0034CAA2  mov      ecx, ebx
0034CAA4  call     0x3a0e20  ; -> 003A0E20 fn
0034CAA9  mov      rbx, qword ptr [rsp + 0x30]
0034CAAE  mov      rbp, qword ptr [rsp + 0x38]
0034CAB3  mov      rsi, qword ptr [rsp + 0x40]
0034CAB8  add      rsp, 0x20
0034CABC  pop      rdi
0034CABD  ret      
```

## 00363840 (106 B, extent 00363840-003638AA)

Page context: "The selector calls 'BattleUnit_TestActorViewFrustumAtCurrentPosition'.  **Audio — CLIENT, 13 edges.** - The chain's step '00363B40' (run by '002620E0') calls the audio bodies '002DF190', '003636A0', '00363840' and   '00363E40'. - '00265920' is also called by '002DE800' and '00361810'. - The audio-filed '00261F90' reads the field pass, the field id and the persistent base. - The area initialiser calls '00362F70', and '00361460' calls the"

```
00363840  sub      rsp, 0x28
00363844  mov      ecx, dword ptr [rip + 0x1f68232]  ; -> 022CBA7C
0036384A  test     ecx, ecx
0036384C  jle      0x36388e  ; -> 0036388E
0036384E  mov      eax, dword ptr [rip + 0x1f6821c]  ; -> 022CBA70
00363854  mov      edx, 0x40
00363859  movzx    r8d, byte ptr [rip + 0x1f68231]  ; -> 022CBA92
00363861  mov      dword ptr [rip + 0x1f6820d], eax  ; -> 022CBA74
00363867  mov      dword ptr [rip + 0x1f68207], 0xb4  ; -> 022CBA78
00363871  call     0x2def40  ; -> 002DEF40 fn
00363876  mov      dword ptr [rip + 0x1f681f4], eax  ; -> 022CBA70
0036387C  movzx    eax, byte ptr [rip + 0x1f6820f]  ; -> 022CBA92
00363883  mov      byte ptr [rip + 0x1f6820a], al  ; -> 022CBA93
00363889  add      rsp, 0x28
0036388D  ret      
0036388E  cmp      dword ptr [rip + 0x1f681db], 0  ; -> 022CBA70
00363895  je       0x3638a5  ; -> 003638A5
00363897  mov      ecx, 0xb4
0036389C  add      rsp, 0x28
003638A0  jmp      0x363e40  ; -> 00363E40 fn
003638A5  add      rsp, 0x28
003638A9  ret      
```

## 00379080 (141 B, extent 00379080-0037910D)

Page context: "LIENT, eleven edges.** - The area initialiser calls '00263560', '002EBE40' and '003DAE30'. - The movement bodies '0033A720', '003ED190' and '003ED3F0' read the field id. - '003DE920' is reached from '00379080' / '00379110'. - '00259B30' calls '00380D30'. - The field pass calls 'WorldActor_UpdateRuntimeAndScriptExecutionState'. - '00379290' calls '0026E8D0'.  **CombatAI, CombatAction, Gameplay and Party — CLIENT, 23 edges through the sel"

```
00379080  push     rbx
00379082  sub      rsp, 0x50
00379086  movaps   xmmword ptr [rsp + 0x40], xmm6
0037908B  xor      ebx, ebx
0037908D  movaps   xmmword ptr [rsp + 0x30], xmm7
00379092  movaps   xmm6, xmm2
00379095  movaps   xmmword ptr [rsp + 0x20], xmm8
0037909B  movaps   xmm7, xmm1
0037909E  movaps   xmm8, xmm0
003790A2  movss    dword ptr [rip + 0x1d212ea], xmm7  ; -> 0209A394
003790AA  movss    dword ptr [rip + 0x1d212dd], xmm8  ; -> 0209A390
003790B3  movss    dword ptr [rip + 0x1d212dd], xmm6  ; -> 0209A398
003790BB  movss    dword ptr [rip + 0x1d212d9], xmm3  ; -> 0209A39C
003790C3  movaps   xmm3, xmm6
003790C6  movaps   xmm2, xmm7
003790C9  movaps   xmm1, xmm8
003790CD  mov      ecx, ebx
003790CF  call     0x2ece40  ; -> 002ECE40 fn
003790D4  inc      ebx
003790D6  cmp      ebx, 5
003790D9  jl       0x3790c3  ; -> 003790C3
003790DB  cmp      byte ptr [rip + 0x2764007], 0  ; -> 02ADD0E9
003790E2  jne      0x3790f7  ; -> 003790F7
003790E4  xor      ecx, ecx
003790E6  call     0x3de700  ; -> 003DE700 fn
003790EB  mov      edx, eax
003790ED  xor      r8d, r8d
003790F0  xor      ecx, ecx
003790F2  call     0x3de920  ; -> 003DE920 fn
003790F7  movaps   xmm6, xmmword ptr [rsp + 0x40]
003790FC  movaps   xmm7, xmmword ptr [rsp + 0x30]
00379101  movaps   xmm8, xmmword ptr [rsp + 0x20]
00379107  add      rsp, 0x50
0037910B  pop      rbx
0037910C  ret      
```

## 00379110 (73 B, extent 00379110-00379159)

Page context: " edges.** - The area initialiser calls '00263560', '002EBE40' and '003DAE30'. - The movement bodies '0033A720', '003ED190' and '003ED3F0' read the field id. - '003DE920' is reached from '00379080' / '00379110'. - '00259B30' calls '00380D30'. - The field pass calls 'WorldActor_UpdateRuntimeAndScriptExecutionState'. - '00379290' calls '0026E8D0'.  **CombatAI, CombatAction, Gameplay and Party — CLIENT, 23 edges through the selector and the"

```
00379110  sub      rsp, 0x28
00379114  cmp      byte ptr [rip + 0x2763fce], 0  ; -> 02ADD0E9
0037911B  movss    dword ptr [rip + 0x1d2126d], xmm0  ; -> 0209A390
00379123  movss    dword ptr [rip + 0x1d21269], xmm1  ; -> 0209A394
0037912B  movss    dword ptr [rip + 0x1d21265], xmm2  ; -> 0209A398
00379133  movss    dword ptr [rip + 0x1d21261], xmm3  ; -> 0209A39C
0037913B  jne      0x379154  ; -> 00379154
0037913D  xor      ecx, ecx
0037913F  call     0x3de700  ; -> 003DE700 fn
00379144  mov      edx, eax
00379146  xor      r8d, r8d
00379149  xor      ecx, ecx
0037914B  add      rsp, 0x28
0037914F  jmp      0x3de920  ; -> 003DE920 fn
00379154  add      rsp, 0x28
00379158  ret      
```

## 0040B3B0 (118 B, extent 0040B3B0-0040B426)

Page context: "lyTables'.  The verbs are the script VM's.  **Presentation — CLIENT, 14 edges.** - The apply's tail '002E3D40' → '0040AAD0' sets the environment preset, azimuth and elevation, and '0040AAD0' calls   '0040B3B0' / '0040B430'. - The boot loads motion tables ('AddMotion_LoadSkeletonMapping', 'AddMotion_LoadHighModelReplace'). - The area initialiser calls 'CameraSystem_InitializeRecords' and '003EB750', and 'CameraSystem_InitializeRecords'  "

```
0040B3B0  mov      byte ptr [rip + 0x2898fda], cl  ; -> 02CA4390
0040B3B6  test     ecx, ecx
0040B3B8  je       0x40b425  ; -> 0040B425
0040B3BA  lea      rax, [rip + 0x1af466f]  ; -> 01EFFA30
0040B3C1  lea      edx, [rcx - 1]
0040B3C4  shl      rdx, 5
0040B3C8  movss    xmm0, dword ptr [rdx + rax]
0040B3CD  movss    dword ptr [rip + 0x2898fb3], xmm0  ; -> 02CA4388
0040B3D5  movss    xmm0, dword ptr [rdx + rax + 4]
0040B3DB  movss    dword ptr [rip + 0x2898f9d], xmm0  ; -> 02CA4380
0040B3E3  movss    xmm0, dword ptr [rdx + rax + 8]
0040B3E9  movss    dword ptr [rip + 0x2898f93], xmm0  ; -> 02CA4384
0040B3F1  movss    xmm0, dword ptr [rdx + rax + 0xc]
0040B3F7  movss    dword ptr [rip + 0x2898f99], xmm0  ; -> 02CA4398
0040B3FF  movss    xmm0, dword ptr [rdx + rax + 0x10]
0040B405  movss    dword ptr [rip + 0x2898f8f], xmm0  ; -> 02CA439C
0040B40D  movss    xmm0, dword ptr [rdx + rax + 0x14]
0040B413  mov      eax, dword ptr [rdx + rax + 0x18]
0040B417  movss    dword ptr [rip + 0x2898f6d], xmm0  ; -> 02CA438C
0040B41F  mov      dword ptr [rip + 0x2898f6f], eax  ; -> 02CA4394
0040B425  ret      
```
