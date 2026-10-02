# F-interior pack: `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`

Generated 2026-10-02 18:33 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/scriptvm-verb-dispatch-and-parameter-encoding.json`.

Functions: 8. Each is cited on the page only at its entry and is still in the F frontier.

## 00264B50 (49 B, extent 00264B50-00264B81)

Page context: "rldAreaField — CLIENT and SERVICE (16 edges).** 6 inbound (WorldAreaField bodies '00377AB0', '00377A90', '00377900' call page-cited '003A1C50', 'FieldData_CopyIndexedRecordByFormatClass' (003DFD00), '00264B50'); 10 outbound (page-cited '002628B0', '00280140', '00264B50' call WorldAreaField bodies '003DFA50', '003EAA00', '00378230'). Substantive edges include '00280140' calls 'WorldTransition_RequeueCurrentFieldForRestore' (00267C90); '0"

```
00264B50  sub      rsp, 0x48
00264B54  mov      rax, qword ptr [rsp + 0x78]
00264B59  mov      qword ptr [rsp + 0x30], rax
00264B5E  mov      rax, qword ptr [rsp + 0x70]
00264B63  mov      qword ptr [rsp + 0x28], rax
00264B68  mov      qword ptr [rsp + 0x20], r9
00264B6D  mov      r9, r8
00264B70  mov      r8d, edx
00264B73  mov      edx, ecx
00264B75  xor      ecx, ecx
00264B77  call     0x264b90  ; -> 00264B90 fn
00264B7C  add      rsp, 0x48
00264B80  ret      
```

## 003488B0 (101 B, extent 003488B0-00348915)

Page context: " and the command is done in the same call.  ### Which is exactly why the game has '*sync' verbs  | verb | shape | 'begin' | 'poll' | behaviour | |---|---|---|---|---| | 'rmove' '0x0042' | durative | '003488B0' | **—** | **starts a move, returns at once** | | 'movesync' '0x003D' | empty | — | '00356A90' | **waits for it** | | 'rturn' '0x0047' | durative | '0034B670' | **—** | starts a turn, returns at once | | 'turnsync' '0x0046' | empty"

```
003488B0  mov      qword ptr [rsp + 8], rbx
003488B5  mov      qword ptr [rsp + 0x10], rbp
003488BA  mov      qword ptr [rsp + 0x18], rsi
003488BF  push     rdi
003488C0  sub      rsp, 0x20
003488C4  mov      rsi, rcx
003488C7  mov      rbx, r9
003488CA  mov      rcx, rdx
003488CD  mov      rdi, r8
003488D0  mov      rbp, rdx
003488D3  call     0x2640e0  ; -> 002640E0 fn
003488D8  movaps   xmm1, xmm0
003488DB  mov      rcx, rbx
003488DE  call     0x267f60  ; -> 00267F60 fn
003488E3  mov      r9, rbx
003488E6  mov      r8, rdi
003488E9  mov      rdx, rbp
003488EC  mov      rcx, rsi
003488EF  call     0x357a20  ; -> 00357A20 fn
003488F4  mov      edx, 2
003488F9  mov      rcx, rbp
003488FC  mov      rbx, qword ptr [rsp + 0x30]
00348901  mov      rbp, qword ptr [rsp + 0x38]
00348906  mov      rsi, qword ptr [rsp + 0x40]
0034890B  add      rsp, 0x20
0034890F  pop      rdi
00348910  jmp      0x26c120  ; -> 0026C120 fn
```

## 00349680 (117 B, extent 00349680-003496F5)

Page context: "tive edges include 'WorldActorScriptVM_InterpretBytecode' (0025E4C0) is called by 'WorldActor_UpdateRuntimeAndScriptExecutionState' (0025DF00); 'VMValueStack_PushFloat32Bits' (00267F60) is called by '00349680'; 'VMValueStack_PushFloat32Bits' (00267F60) is called by '003548B0'; 'VMValueStack_PushFloat32Bits' (00267F60) is called by '003488B0'; the remaining edges run through shared helpers the page cites. - **Party — MECHANICAL (5 edges)"

```
00349680  mov      qword ptr [rsp + 8], rbx
00349685  mov      qword ptr [rsp + 0x10], rbp
0034968A  mov      qword ptr [rsp + 0x18], rsi
0034968F  push     rdi
00349690  sub      rsp, 0x20
00349694  mov      rsi, rcx
00349697  mov      rbx, r9
0034969A  mov      rcx, rdx
0034969D  mov      rdi, r8
003496A0  mov      rbp, rdx
003496A3  call     0x2640e0  ; -> 002640E0 fn
003496A8  movaps   xmm1, xmm0
003496AB  mov      rcx, rbx
003496AE  call     0x267f60  ; -> 00267F60 fn
003496B3  mov      r9, rbx
003496B6  mov      r8, rdi
003496B9  mov      rdx, rbp
003496BC  mov      rcx, rsi
003496BF  call     0x357a20  ; -> 00357A20 fn
003496C4  mov      rcx, rbp
003496C7  call     0x263f40  ; -> 00263F40 fn
003496CC  mov      rcx, rax
003496CF  call     0x2eb430  ; -> 002EB430 fn
003496D4  mov      edx, 2
003496D9  mov      rcx, rbp
003496DC  mov      rbx, qword ptr [rsp + 0x30]
003496E1  mov      rbp, qword ptr [rsp + 0x38]
003496E6  mov      rsi, qword ptr [rsp + 0x40]
003496EB  add      rsp, 0x20
003496EF  pop      rdi
003496F0  jmp      0x26c120  ; -> 0026C120 fn
```

## 0034A940 (169 B, extent 0034A940-0034A9E9)

Page context: " calls '00229EB0'; '0034CF90' calls '00265880'; the remaining edges run through shared helpers the page cites. - **Movement — CLIENT and SERVICE (76 edges).** 42 inbound (Movement bodies '00350510', '0034A940', '0034EBC0' call page-cited '0026B0C0', 'Actor_SetFacingHeading_Variant1' (0026B620), '0026AF80'); 34 outbound (page-cited '002628B0', '00350510', '00357D10' call Movement bodies '002E4A10', '0026C120', '0026B0C0'). Substantive ed"

```
0034A940  push     rbx
0034A942  sub      rsp, 0x60
0034A946  movaps   xmmword ptr [rsp + 0x50], xmm6
0034A94B  mov      rcx, r9
0034A94E  movaps   xmmword ptr [rsp + 0x40], xmm7
0034A953  mov      rbx, r9
0034A956  movaps   xmmword ptr [rsp + 0x30], xmm8
0034A95C  movaps   xmmword ptr [rsp + 0x20], xmm9
0034A962  call     0x267db0  ; -> 00267DB0 fn
0034A967  mov      rcx, rbx
0034A96A  movaps   xmm6, xmm0
0034A96D  call     0x267db0  ; -> 00267DB0 fn
0034A972  mov      rcx, rbx
0034A975  movaps   xmm7, xmm0
0034A978  call     0x267db0  ; -> 00267DB0 fn
0034A97D  mov      rcx, rbx
0034A980  movaps   xmm8, xmm0
0034A984  call     0x267db0  ; -> 00267DB0 fn
0034A989  mov      rcx, rbx
0034A98C  movaps   xmm9, xmm0
0034A990  call     0x267e10  ; -> 00267E10 fn
0034A995  mov      ecx, eax
0034A997  call     0x263750  ; -> 00263750 fn
0034A99C  mov      rbx, rax
0034A99F  test     rax, rax
0034A9A2  je       0x34a9cd  ; -> 0034A9CD
0034A9A4  movaps   xmm3, xmm7
0034A9A7  movaps   xmm2, xmm8
0034A9AB  movaps   xmm1, xmm9
0034A9AF  mov      rcx, rax
0034A9B2  call     0x26af80  ; -> 0026AF80 fn
0034A9B7  movaps   xmm1, xmm6
0034A9BA  mov      rcx, rbx
0034A9BD  call     0x26b620  ; -> 0026B620 fn
0034A9C2  movaps   xmm1, xmm6
0034A9C5  mov      rcx, rbx
0034A9C8  call     0x26a0d0  ; -> 0026A0D0 fn
0034A9CD  movaps   xmm6, xmmword ptr [rsp + 0x50]
0034A9D2  movaps   xmm7, xmmword ptr [rsp + 0x40]
0034A9D7  movaps   xmm8, xmmword ptr [rsp + 0x30]
0034A9DD  movaps   xmm9, xmmword ptr [rsp + 0x20]
0034A9E3  add      rsp, 0x60
0034A9E7  pop      rbx
0034A9E8  ret      
```

## 0034C570 (79 B, extent 0034C570-0034C5BF)

Page context: "t once | | 'turnsync' '0x0046' | empty | — | '00341D50' | waits for it | | 'wait' '0x0000' | durative | '0034CF90' | '0034DCC0' | genuinely blocks | | 'camerasync' '0x0079' | durative | '0034C290' | '0034C570' | genuinely blocks |  > **Movement and turning verbs do not block.** 'rmove' puts a walk in motion and hands control > straight back to the script; the waiting is a *separate verb*. That is why every move in an FFXII > cutscene is"

```
0034C570  mov      qword ptr [rsp + 8], rbx
0034C575  push     rdi
0034C576  sub      rsp, 0x20
0034C57A  mov      rbx, r8
0034C57D  mov      rdi, rdx
0034C580  call     0x2640c0  ; -> 002640C0 fn
0034C585  mov      edx, dword ptr [rbx]
0034C587  mov      ecx, dword ptr [rax + 0x28]
0034C58A  call     0x3da1a0  ; -> 003DA1A0 fn
0034C58F  test     eax, eax
0034C591  je       0x34c5b0  ; -> 0034C5B0
0034C593  movzx    ecx, byte ptr [rdi + 0x15]
0034C597  call     0x267310  ; -> 00267310 fn
0034C59C  xor      ecx, ecx
0034C59E  test     eax, eax
0034C5A0  sete     cl
0034C5A3  mov      eax, ecx
0034C5A5  mov      rbx, qword ptr [rsp + 0x30]
0034C5AA  add      rsp, 0x20
0034C5AE  pop      rdi
0034C5AF  ret      
0034C5B0  mov      rbx, qword ptr [rsp + 0x30]
0034C5B5  xor      ecx, ecx
0034C5B7  mov      eax, ecx
0034C5B9  add      rsp, 0x20
0034C5BD  pop      rdi
0034C5BE  ret      
```

## 0034EBC0 (116 B, extent 0034EBC0-0034EC34)

Page context: "— and the four values travel over the same operand stack a script would have used. 'ucsetpos' ('0x0168', handler '0034F800') does the same thing by tail jump: it resolves its target and jumps into **'0034EBC0', the handler of '0x0001 setpos' (three arguments)**, or drains three floats and does nothing when the target does not resolve.  Once a callee's own net stack effect is folded in, both shapes measure exactly:  ''' setentrypos : 1 p"

```
0034EBC0  mov      qword ptr [rsp + 8], rbx
0034EBC5  push     rdi
0034EBC6  sub      rsp, 0x40
0034EBCA  movaps   xmmword ptr [rsp + 0x30], xmm6
0034EBCF  mov      rcx, r9
0034EBD2  movaps   xmmword ptr [rsp + 0x20], xmm7
0034EBD7  mov      rbx, r9
0034EBDA  mov      rdi, rdx
0034EBDD  call     0x267db0  ; -> 00267DB0 fn
0034EBE2  mov      rcx, rbx
0034EBE5  movaps   xmm6, xmm0
0034EBE8  call     0x267db0  ; -> 00267DB0 fn
0034EBED  mov      rcx, rbx
0034EBF0  movaps   xmm7, xmm0
0034EBF3  call     0x267db0  ; -> 00267DB0 fn
0034EBF8  cmp      byte ptr [rdi + 0x10], 0
0034EBFC  movaps   xmm3, xmm6
0034EBFF  movaps   xmm2, xmm7
0034EC02  movaps   xmm1, xmm0
0034EC05  mov      rcx, rdi
0034EC08  je       0x34ec11  ; -> 0034EC11
0034EC0A  call     0x26b0c0  ; -> 0026B0C0 fn
0034EC0F  jmp      0x34ec16  ; -> 0034EC16
0034EC11  call     0x26af80  ; -> 0026AF80 fn
0034EC16  xor      edx, edx
0034EC18  mov      rcx, rdi
0034EC1B  mov      rbx, qword ptr [rsp + 0x50]
0034EC20  movaps   xmm6, xmmword ptr [rsp + 0x30]
0034EC25  movaps   xmm7, xmmword ptr [rsp + 0x20]
0034EC2A  add      rsp, 0x40
0034EC2E  pop      rdi
0034EC2F  jmp      0x26ae90  ; -> 0026AE90 fn
```

## 00353D90 (101 B, extent 00353D90-00353DF5)

Page context: "at 99.3 % agreement. Eight rows disagreed. Reading them found two more defects — **in the instrument, not in the table.**  ### DEFECT 3: the count was path-insensitive  'maskopen' ('0x008A', handler '00353D90') is declared with one argument and measured two:  '''asm 00353D96  movzx ecx, byte ptr [rdx + 0x15] 00353D9D  call  0x267310 00353DA5  test  eax, eax 00353DA7  je    0x353DD6 00353DA9  call  0x267E10        ; <-- pop, arm A    ..."

```
00353D90  push     rbx
00353D92  sub      rsp, 0x20
00353D96  movzx    ecx, byte ptr [rdx + 0x15]
00353D9A  mov      rbx, r9
00353D9D  call     0x267310  ; -> 00267310 fn
00353DA2  mov      rcx, rbx
00353DA5  test     eax, eax
00353DA7  je       0x353dd6  ; -> 00353DD6
00353DA9  call     0x267e10  ; -> 00267E10 fn
00353DAE  xor      edx, edx
00353DB0  lea      ecx, [rdx + 1]
00353DB3  call     0x2e2440  ; -> 002E2440 fn
00353DB8  mov      edx, 3
00353DBD  xor      ecx, ecx
00353DBF  call     0x2e1c40  ; -> 002E1C40 fn
00353DC4  mov      edx, 3
00353DC9  lea      ecx, [rdx - 2]
00353DCC  add      rsp, 0x20
00353DD0  pop      rbx
00353DD1  jmp      0x2e1c70  ; -> 002E1C70 fn
00353DD6  call     0x267e10  ; -> 00267E10 fn
00353DDB  xor      edx, edx
00353DDD  xor      ecx, ecx
00353DDF  call     0x2e2440  ; -> 002E2440 fn
00353DE4  mov      edx, 3
00353DE9  xor      ecx, ecx
00353DEB  add      rsp, 0x20
00353DEF  pop      rbx
00353DF0  jmp      0x2e1c40  ; -> 002E1C40 fn
```

## 00377900 (104 B, extent 00377900-00377968)

Page context: "is called by '00266D10'; the remaining edges run through shared helpers the page cites. - **WorldAreaField — CLIENT and SERVICE (16 edges).** 6 inbound (WorldAreaField bodies '00377AB0', '00377A90', '00377900' call page-cited '003A1C50', 'FieldData_CopyIndexedRecordByFormatClass' (003DFD00), '00264B50'); 10 outbound (page-cited '002628B0', '00280140', '00264B50' call WorldAreaField bodies '003DFA50', '003EAA00', '00378230'). Substantive"

```
00377900  mov      qword ptr [rsp + 8], rbx
00377905  mov      qword ptr [rsp + 0x10], rsi
0037790A  mov      qword ptr [rsp + 0x18], rdi
0037790F  push     r14
00377911  sub      rsp, 0x30
00377915  lea      rbx, [rdx + 0xc]
00377919  mov      rdi, rdx
0037791C  lea      rsi, [rdx + 8]
00377920  mov      qword ptr [rsp + 0x28], rbx
00377925  lea      r9, [rdx + 4]
00377929  mov      qword ptr [rsp + 0x20], rsi
0037792E  mov      r8, rdx
00377931  mov      edx, ecx
00377933  xor      ecx, ecx
00377935  call     0x264110  ; -> 00264110 fn
0037793A  test     eax, eax
0037793C  jne      0x377945  ; -> 00377945
0037793E  mov      qword ptr [rdi], rax
00377941  mov      dword ptr [rsi], eax
00377943  mov      dword ptr [rbx], eax
00377945  movss    xmm0, dword ptr [rbx]
00377949  call     0x3a1c50  ; -> 003A1C50 fn
0037794E  mov      rsi, qword ptr [rsp + 0x48]
00377953  mov      rdi, qword ptr [rsp + 0x50]
00377958  movss    dword ptr [rbx], xmm0
0037795C  mov      rbx, qword ptr [rsp + 0x40]
00377961  add      rsp, 0x30
00377965  pop      r14
00377967  ret      
```
