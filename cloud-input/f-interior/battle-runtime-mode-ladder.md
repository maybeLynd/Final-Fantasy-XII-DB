# F-interior pack: `00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md`

Generated 2026-10-01 15:28 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/battle-runtime-mode-ladder.json`.

Functions: 23. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: f9017b106	SWE2-CONTRACT: repair 807950d2a - restore 18 committed pass-22 section headings it renamed; 807950d2a	SWE2-CONTRACT: pass-22 debt batch A - 37 Engine-Core-Runtime pages' cross-subsystem neighbour bullet; inbox mentions: SWE2-AUDIT-SPEC.md, SWE2-EC7.md, SWE2-FRONTIER.md, repos-78.md). OPUS read these before packing.

## 0025D540 (64 B, extent 0025D540-0025D580)

Page context: " (SWE2-EC7-156, 155 edges).** That layer's bodies consult this page's helpers — '00263660'/'0026C5D0' call '00226280', '0025D9E0' calls '00233AA0', and batch-121's '002E26F0' adds its own '0025D480'/'0025D540'/'002EDAA0'/'0042F3B0' to the same fan-in; the crossing is shared-helper consultation, not a shared responsibility. **Presentation — CLIENT and SERVICE (SWE2-EC7-156, 219 edges).** '001D50D0' is called by '00187950'/'001BC190'/'001"

```
0025D540  sub      rsp, 0x28
0025D544  cmp      byte ptr [rcx + 0x18], 1
0025D548  je       0x25d57b  ; -> 0025D57B
0025D54A  mov      qword ptr [rsp + 0x20], rbx
0025D54F  mov      rbx, qword ptr [rcx + 0xc0]
0025D556  test     rbx, rbx
0025D559  je       0x25d576  ; -> 0025D576
0025D55B  mov      rbx, qword ptr [rbx + 0x138]
0025D562  test     rbx, rbx
0025D565  je       0x25d576  ; -> 0025D576
0025D567  mov      rcx, rbx
0025D56A  call     0x3da9f0  ; -> 003DA9F0 fn
0025D56F  mov      byte ptr [rbx + 0xef], 0
0025D576  mov      rbx, qword ptr [rsp + 0x20]
0025D57B  add      rsp, 0x28
0025D57F  ret      
```

## 0028E970 (122 B, extent 0028E970-0028E9EA)

Page context: "— 'bt r10d, ebx' fails to 0. Past the gate '0017E7D0'/'0035DA80'/ '003C8990' run, then 'ebx - 1 <= 0x17' dispatches a six-arm jump table at '0x134C58'/'0x134C70' ('0035D660', '0035D980', '003C87B0', '0028E970' returning 1, '0035D080'); out-of-range ids fall to '0028F970()' plus a '00280A00(ecx, edx, r8)' passthrough. Interior anchor '00254BF9' (the 'jmp rcx' dispatch).  ## SWE2-EC7-33 update (2026-09-19) - '003B1BA0'  '003B1BA0' (**1,59"

```
0028E970  push     rbx
0028E972  sub      rsp, 0x20
0028E976  mov      rax, qword ptr [rip + 0x1e0d503]  ; -> 0209BE80
0028E97D  mov      ebx, ecx
0028E97F  mov      rcx, qword ptr [rax + 0x10fb0]
0028E986  test     rcx, rcx
0028E989  je       0x28e9ae  ; -> 0028E9AE
0028E98B  call     0x245020  ; -> 00245020 fn
0028E990  mov      rax, qword ptr [rip + 0x1e0d4e9]  ; -> 0209BE80
0028E997  mov      qword ptr [rax + 0x10fb0], 0
0028E9A2  call     0x252d90  ; -> 00252D90 fn
0028E9A7  mov      rax, qword ptr [rip + 0x1e0d4d2]  ; -> 0209BE80
0028E9AE  cmp      qword ptr [rax + 0x10fb0], 0
0028E9B6  jne      0x28e9de  ; -> 0028E9DE
0028E9B8  xor      edx, edx
0028E9BA  mov      ecx, ebx
0028E9BC  call     0x252b40  ; -> 00252B40 fn
0028E9C1  call     0x2d5030  ; -> 002D5030 fn
0028E9C6  mov      rcx, rax
0028E9C9  mov      rax, qword ptr [rip + 0x1e0d4b0]  ; -> 0209BE80
0028E9D0  mov      qword ptr [rax + 0x10fb0], rcx
0028E9D7  mov      rax, qword ptr [rip + 0x1e0d4a2]  ; -> 0209BE80
0028E9DE  mov      eax, dword ptr [rax + 0x10fb0]
0028E9E4  add      rsp, 0x20
0028E9E8  pop      rbx
0028E9E9  ret      
```

## 00296A70 (44 B, extent 00296A70-00296A9C)

Page context: "ts the object's '+0x40' bit '0x10000' when '002544B0()' returns '1', closes it through '00244F00', clears the slot and runs '0028F0C0(0)'; a non-null '[0209BE80 + 0x10FC8]' is then torn down through '00296A70' and cleared - both pending request objects released in one pass  Interior anchor '00290E42' (function '00290E10').  '002970C0' (64 B) is the single-slot close '0028FD70' shares with the '+0x10F78' arm: on a non-null '0209C300' it "

```
00296A70  push     rbx
00296A72  sub      rsp, 0x20
00296A76  mov      rbx, rcx
00296A79  call     0x2544b0  ; -> 002544B0 fn
00296A7E  cmp      eax, 1
00296A81  jne      0x296a8f  ; -> 00296A8F
00296A83  test     rbx, rbx
00296A86  je       0x296a8f  ; -> 00296A8F
00296A88  or       dword ptr [rbx + 0x40], 0x10000
00296A8F  mov      rcx, rbx
00296A92  add      rsp, 0x20
00296A96  pop      rbx
00296A97  jmp      0x244f00  ; -> 00244F00 fn
```

## 00296AA0 (68 B, extent 00296AA0-00296AE4)

Page context: "hared responsibility.  **UI — CLIENT (SWE2-EC7 batch-149).** '0028FD70', a callee the '0035D980' entry's teardown arm cites, sits inside that layer's fan-in: it calls UI bodies '00290E10'/'002964D0'/'00296AA0'/'002970C0'/'00297100'/'003CA1C0'/'003CA1E0' and is itself called by the UI-filed '0035D6B0' - the ladder borrows a shared teardown step; the UI edges are that helper's own traffic, not a UI responsibility of this page.  **WorldAre"

```
00296AA0  push     rbx
00296AA2  sub      rsp, 0x20
00296AA6  xor      r8d, r8d
00296AA9  lea      rdx, [rip + 0x51d0]  ; -> 0029BC80
00296AB0  mov      ecx, 0xc0
00296AB5  call     0x244f50  ; -> 00244F50 fn
00296ABA  mov      rbx, rax
00296ABD  call     0x2544b0  ; -> 002544B0 fn
00296AC2  cmp      eax, 1
00296AC5  jne      0x296ad3  ; -> 00296AD3
00296AC7  test     rbx, rbx
00296ACA  je       0x296ad3  ; -> 00296AD3
00296ACC  or       dword ptr [rbx + 0x40], 0x8000
00296AD3  mov      rcx, rbx
00296AD6  call     0x246ac0  ; -> 00246AC0 fn
00296ADB  mov      rax, rbx
00296ADE  add      rsp, 0x20
00296AE2  pop      rbx
00296AE3  ret      
```

## 00296BE0 (544 B, extent 00296BE0-00296E00)

Page context: "nterior anchor '002549A2' (function '00254980').  '00290500' (26 B) is the conditional forwarder the ladder quartet calls: 'rax = [0209BE80]', 'rcx = [rax+0x10F78]' - a null field returns, otherwise '00296BE0(rcx, ecx)' runs as a tail call on the same '0209BE80' global the gate family reads.  Interior anchor '00290509' (function '00290500').  '002E26F0' (454 B) is the two-record comparator '002E28C0'/'0034A640' call: 'rsi = [rcx+0xC0]' "

```
00296BE0  push     rbx
00296BE2  sub      rsp, 0x20
00296BE6  mov      rbx, rcx
00296BE9  test     rcx, rcx
00296BEC  jne      0x296bf6  ; -> 00296BF6
00296BEE  xor      eax, eax
00296BF0  add      rsp, 0x20
00296BF4  pop      rbx
00296BF5  ret      
00296BF6  test     edx, edx
00296BF8  jne      0x296cae  ; -> 00296CAE
00296BFE  cmp      byte ptr [rcx + 0xb49], 1
00296C05  jne      0x296df5  ; -> 00296DF5
00296C0B  mov      rcx, qword ptr [rcx + 0xb38]
00296C12  mov      qword ptr [rsp + 0x30], rdi
00296C17  call     0x246ac0  ; -> 00246AC0 fn
00296C1C  mov      eax, 0xff7f
00296C21  and      word ptr [rbx + 0xb4a], ax
00296C28  call     0x290630  ; -> 00290630 fn
00296C2D  mov      rcx, rbx
00296C30  mov      byte ptr [rbx + 0xb49], 0
00296C37  call     0x2470c0  ; -> 002470C0 fn
00296C3C  lea      rcx, [rbx + 0xc0]
00296C43  call     0x273a20  ; -> 00273A20 fn
00296C48  test     eax, eax
00296C4A  je       0x296c58  ; -> 00296C58
00296C4C  lea      rcx, [rbx + 0xc0]
00296C53  call     0x244f00  ; -> 00244F00 fn
00296C58  mov      rdi, qword ptr [rsp + 0x30]
00296C5D  mov      eax, 0xfffe
00296C62  and      word ptr [rbx + 0xb4a], ax
00296C69  xor      edx, edx
00296C6B  cmp      byte ptr [rbx + 0xb42], dl
00296C71  jbe      0x296c98  ; -> 00296C98
00296C73  lea      rcx, [rbx + 0x318]
00296C7A  mov      r8d, 0xff78
00296C80  and      word ptr [rcx], r8w
00296C84  lea      rcx, [rcx + 0x160]
00296C8B  movzx    eax, byte ptr [rbx + 0xb42]
00296C92  inc      edx
00296C94  cmp      edx, eax
00296C96  jl       0x296c80  ; -> 00296C80
00296C98  mov      qword ptr [rbx + 0xb20], 0
00296CA3  mov      eax, 1
00296CA8  add      rsp, 0x20
00296CAC  pop      rbx
00296CAD  ret      
00296CAE  movzx    eax, byte ptr [rcx + 0xb49]
00296CB5  cmp      al, 1
00296CB7  je       0x296df5  ; -> 00296DF5
00296CBD  cmp      al, 2
00296CBF  je       0x296bee  ; -> 00296BEE
00296CC5  mov      byte ptr [rcx + 0xb49], 1
00296CCC  call     0x35bae0  ; -> 0035BAE0 fn
00296CD1  mov      byte ptr [rbx + 0xb48], al
00296CD7  mov      rcx, rbx
00296CDA  mov      eax, 0xfffd
00296CDF  mov      qword ptr [rbx + 0xb30], rbx
00296CE6  and      word ptr [rbx + 0xb4a], ax
00296CED  lea      rax, [rip + 0x94c]  ; -> 00297640
00296CF4  mov      qword ptr [rbx + 0xb20], rax
00296CFB  call     0x299bd0  ; -> 00299BD0 fn
00296D00  mov      rcx, qword ptr [rbx + 0xb38]
00296D07  call     0x244dd0  ; -> 00244DD0 fn
00296D0C  movsx    ecx, byte ptr [rbx + 0xb48]
00296D13  call     0x35bb00  ; -> 0035BB00 fn
00296D18  movsx    rdx, byte ptr [rbx + 0xb48]
00296D20  imul     rcx, rdx, 0x160
00296D27  mov      rax, rdx
00296D2A  movzx    eax, word ptr [rcx + rbx + 0x318]
00296D32  test     al, 1
00296D34  je       0x296d47  ; -> 00296D47
00296D36  or       ax, 4
00296D3A  mov      word ptr [rcx + rbx + 0x318], ax
00296D42  jmp      0x296dbc  ; -> 00296DBC
00296D47  movzx    r10d, byte ptr [rbx + 0xb42]
00296D4F  xor      r8d, r8d
00296D52  movsx    r11d, dl
00296D56  mov      edx, r11d
00296D59  test     r10d, r10d
00296D5C  je       0x296d93  ; -> 00296D93
00296D5E  movzx    r9d, byte ptr [rbx + 0xb42]
00296D66  add      edx, 1
00296D69  jns      0x296d6f  ; -> 00296D6F
00296D6B  lea      edx, [r9 - 1]
00296D6F  xor      eax, eax
00296D71  cmp      edx, r9d
00296D74  cmovl    eax, edx
00296D77  movsxd   rdx, eax
00296D7A  imul     rcx, rdx, 0x160
00296D81  test     byte ptr [rcx + rbx + 0x318], 1
00296D89  jne      0x296d96  ; -> 00296D96
00296D8B  inc      r8d
00296D8E  cmp      r8d, r10d
00296D91  jl       0x296d66  ; -> 00296D66
00296D93  mov      edx, r11d
00296D96  mov      byte ptr [rbx + 0xb48], dl
00296D9C  movsx    rax, dl
00296DA0  imul     rcx, rax, 0x160
00296DA7  or       word ptr [rcx + rbx + 0x318], 4
00296DB0  movsx    ecx, byte ptr [rbx + 0xb48]
00296DB7  call     0x35bb00  ; -> 0035BB00 fn
00296DBC  mov      eax, 0xfffe
00296DC1  mov      rcx, rbx
00296DC4  and      word ptr [rbx + 0xb4a], ax
00296DCB  call     0x29c9d0  ; -> 0029C9D0 fn
00296DD0  test     eax, eax
00296DD2  jne      0x296ddc  ; -> 00296DDC
00296DD4  or       word ptr [rbx + 0xb4a], 1
00296DDC  call     0x3678f0  ; -> 003678F0 fn
00296DE1  mov      rcx, rbx
00296DE4  call     0x2470d0  ; -> 002470D0 fn
00296DE9  mov      eax, 0x80
00296DEE  or       word ptr [rbx + 0xb4a], ax
00296DF5  mov      eax, 1
00296DFA  add      rsp, 0x20
00296DFE  pop      rbx
00296DFF  ret      
```

## 00297100 (97 B, extent 00297100-00297161)

Page context: " **UI — CLIENT (SWE2-EC7 batch-149).** '0028FD70', a callee the '0035D980' entry's teardown arm cites, sits inside that layer's fan-in: it calls UI bodies '00290E10'/'002964D0'/'00296AA0'/'002970C0'/'00297100'/'003CA1C0'/'003CA1E0' and is itself called by the UI-filed '0035D6B0' - the ladder borrows a shared teardown step; the UI edges are that helper's own traffic, not a UI responsibility of this page.  **WorldAreaField — CONSULTED BOT"

```
00297100  push     rbx
00297102  sub      rsp, 0x20
00297106  mov      rbx, qword ptr [rip + 0x1e051f3]  ; -> 0209C300
0029710D  test     rbx, rbx
00297110  jne      0x297132  ; -> 00297132
00297112  xor      r8d, r8d
00297115  lea      rdx, [rip + 0x5414]  ; -> 0029C530
0029711C  mov      ecx, 0xf0
00297121  call     0x244f50  ; -> 00244F50 fn
00297126  mov      rbx, rax
00297129  mov      qword ptr [rip + 0x1e051d0], rax  ; -> 0209C300
00297130  jmp      0x29713e  ; -> 0029713E
00297132  mov      eax, 0xfffc
00297137  and      word ptr [rbx + 0xe6], ax
0029713E  call     0x2544b0  ; -> 002544B0 fn
00297143  cmp      eax, 1
00297146  jne      0x297154  ; -> 00297154
00297148  test     rbx, rbx
0029714B  je       0x297154  ; -> 00297154
0029714D  or       dword ptr [rbx + 0x40], 0x8000
00297154  mov      rcx, rbx
00297157  add      rsp, 0x20
0029715B  pop      rbx
0029715C  jmp      0x246ac0  ; -> 00246AC0 fn
```

## 00299B90 (59 B, extent 00299B90-00299BCB)

Page context: "rm of the '00320CA0' gate this page names at the mode-check row: '00320CA0(ecx, &out)' must return 1 and the out-dword must carry none of the '0x80000003' bits - the caller-visible availability test '00299B90'/'00299BD0'/'003F77F0' run.  Interior anchor '002739D9' (function '002739D0').  '00320CA0' (80 B) is the availability gate '002739D0''s predicate wraps: when 'byte[02089340] & 0x10' it runs '003588B0' for the mode object, '00263E30"

```
00299B90  sub      rsp, 0x28
00299B94  call     0x35bb20  ; -> 0035BB20 fn
00299B99  test     rax, rax
00299B9C  jne      0x299ba5  ; -> 00299BA5
00299B9E  xor      eax, eax
00299BA0  add      rsp, 0x28
00299BA4  ret      
00299BA5  mov      ecx, dword ptr [rax + 4]
00299BA8  test     ecx, ecx
00299BAA  je       0x299b9e  ; -> 00299B9E
00299BAC  mov      edx, dword ptr [rax]
00299BAE  test     dl, 1
00299BB1  jne      0x299b9e  ; -> 00299B9E
00299BB3  test     dl, 0x40
00299BB6  jne      0x299b9e  ; -> 00299B9E
00299BB8  call     0x2739d0  ; -> 002739D0 fn
00299BBD  xor      ecx, ecx
00299BBF  test     eax, eax
00299BC1  setne    cl
00299BC4  mov      eax, ecx
00299BC6  add      rsp, 0x28
00299BCA  ret      
```

## 002C6450 (103 B, extent 002C6450-002C64B7)

Page context: "t. Interior anchor '00273997' (the '002E0FA0' call).  ## SWE2-EC7-104 update (2026-09-20) - '0028FA00' measured  '0028FA00' (44 B) is the flag gate '00253C70' and '002736B0' call before tailing into '002C6450': it loads '[0209BE80 + 0x10F80]', returns 0 when that pointer is null, otherwise reads 'word[ptr + 0x1D7A]', computes '(~(w >> 3)) & 1', and only when the bit is set falls through to '002C6450' - a one-bit permission check in fron"

```
002C6450  push     rbx
002C6452  sub      rsp, 0x20
002C6456  mov      rbx, rcx
002C6459  call     0x3590d0  ; -> 003590D0 fn
002C645E  mov      rdx, qword ptr [rbx + 0x1d70]
002C6465  test     rdx, rdx
002C6468  je       0x2c647e  ; -> 002C647E
002C646A  nop      word ptr [rax + rax]
002C6470  cmp      dword ptr [rdx + 0x10], eax
002C6473  je       0x2c6495  ; -> 002C6495
002C6475  mov      rdx, qword ptr [rdx + 0x18]
002C6479  test     rdx, rdx
002C647C  jne      0x2c6470  ; -> 002C6470
002C647E  xor      eax, eax
002C6480  mov      ecx, 0x80
002C6485  cmp      word ptr [rbx + 0x1d78], cx
002C648C  setge    al
002C648F  add      rsp, 0x20
002C6493  pop      rbx
002C6494  ret      
002C6495  movsx    eax, word ptr [rbx + 0x1d78]
002C649C  movzx    ecx, byte ptr [rdx + 0x14]
002C64A0  imul     ecx, eax
002C64A3  xor      eax, eax
002C64A5  and      ecx, 0xffffff80
002C64A8  cmp      ecx, 0x4000
002C64AE  setge    al
002C64B1  add      rsp, 0x20
002C64B5  pop      rbx
002C64B6  ret      
```

## 002EA030 (14 B, extent 002EA030-002EA03E)

Page context: "r anchor '003B1DEB' (an '0020E600' call).  ## SWE2-EC7-37 update (2026-09-19) - '003B4B60'  '003B4B60' (567 B) is a battle-runtime mode body - '02B40512'/'02B4050A'/'02B40508'/'02B40511' byte flags, '002EA030'/'003E56C0' pairs plus '003B54C0'/'003E6AA0'/'003B4FD0'. Interior anchor '003B4BBF' (an '002EA030' call).  ## SWE2-EC7-39 update (2026-09-19) - '003B5520'  '003B5520' (428 B) is a battle-runtime-mode body - '02B40508'..'02B40514' b"

```
002EA030  movsxd   rax, ecx
002EA033  lea      rcx, [rip + 0x1c01a66]  ; -> 01EEBAA0
002EA03A  mov      eax, dword ptr [rcx + rax*4]
002EA03D  ret      
```

## 00309FB0 (318 B, extent 00309FB0-0030A0EE)

Page context: "2026-09-14: the ladder's bodies reach the layers a mode change touches — '0030C470' calls **items/equipment** '00324100' and '00329220' calls '00324020', while '00377C20' is called by the items-side '00309FB0'/'0030FD10' (4 edges), and '00584210' calls **achievements** '00316810' (1). Entering or leaving a battle mode walks equipment state and can report to the achievement layer; these are the ladder's consumers, not its owners.)*  ## T"

```
00309FB0  push     rbx
00309FB2  push     r12
00309FB4  push     r13
00309FB6  push     r14
00309FB8  sub      rsp, 0x28
00309FBC  mov      qword ptr [rsp + 0x50], rbp
00309FC1  mov      eax, 0xffff
00309FC6  mov      qword ptr [rsp + 0x58], rsi
00309FCB  xor      r14d, r14d
00309FCE  mov      qword ptr [rsp + 0x60], rdi
00309FD3  movzx    r12d, cx
00309FD7  mov      qword ptr [rsp + 0x20], r15
00309FDC  cmp      cx, ax
00309FDF  jne      0x309fe6  ; -> 00309FE6
00309FE1  or       ebx, 0xffffffff
00309FE4  jmp      0x30a042  ; -> 0030A042
00309FE6  mov      ecx, 0xf000
00309FEB  movzx    eax, r12w
00309FEF  and      ax, cx
00309FF2  mov      ecx, 0xe000
00309FF7  cmp      ax, cx
00309FFA  jbe      0x30a001  ; -> 0030A001
00309FFC  or       ebx, 0xffffffff
00309FFF  jmp      0x30a042  ; -> 0030A042
0030A001  movzx    eax, r12w
0030A005  shr      rax, 0xc
0030A009  imul     rdx, rax, 0x58
0030A00D  lea      rax, [rip + 0x1be1cac]  ; -> 01EEBCC0
0030A014  movzx    ecx, r12w
0030A018  add      rdx, rax
0030A01B  and      ecx, 0xfff
0030A021  mov      eax, dword ptr [rdx + 0x3c]
0030A024  dec      eax
0030A026  cmp      ecx, eax
0030A028  jg       0x30a03f  ; -> 0030A03F
0030A02A  mov      rax, qword ptr [rdx + 0x50]
0030A02E  test     rax, rax
0030A031  je       0x30a03f  ; -> 0030A03F
0030A033  xor      edx, edx
0030A035  movzx    ecx, r12w
0030A039  call     rax
0030A03B  mov      ebx, eax
0030A03D  jmp      0x30a042  ; -> 0030A042
0030A03F  mov      ebx, r14d
0030A042  mov      r15d, r14d
0030A045  lea      r13, [rip + 0x1fb773c]  ; -> 022C1788
0030A04C  mov      esi, r14d
0030A04F  mov      rdi, r14
0030A052  mov      ecx, esi
0030A054  call     0x31b810  ; -> 0031B810 fn
0030A059  mov      rbp, rax
0030A05C  test     rax, rax
0030A05F  je       0x30a094  ; -> 0030A094
0030A061  mov      rcx, qword ptr [rax + 0x698]
0030A068  test     rcx, rcx
0030A06B  je       0x30a094  ; -> 0030A094
0030A06D  mov      eax, dword ptr [rcx + 0x64]
0030A070  or       eax, dword ptr [rcx + 0x3c]
0030A073  test     eax, 0x80000003
0030A078  je       0x30a083  ; -> 0030A083
0030A07A  call     0x377c20  ; -> 00377C20 fn
0030A07F  test     eax, eax
0030A081  je       0x30a094  ; -> 0030A094
0030A083  cmp      rdi, 4
0030A087  jge      0x30a08e  ; -> 0030A08E
0030A089  mov      qword ptr [r13 + rdi*8], rbp
0030A08E  inc      r15d
0030A091  inc      rdi
0030A094  inc      esi
0030A096  cmp      esi, 4
0030A099  jl       0x30a052  ; -> 0030A052
0030A09B  mov      rdi, qword ptr [rsp + 0x60]
0030A0A0  mov      rsi, qword ptr [rsp + 0x58]
0030A0A5  mov      rbp, qword ptr [rsp + 0x50]
0030A0AA  movsxd   rax, r15d
0030A0AD  mov      r15, qword ptr [rsp + 0x20]
0030A0B2  test     rax, rax
0030A0B5  jle      0x30a0e0  ; -> 0030A0E0
0030A0B7  nop      word ptr [rax + rax]
0030A0C0  mov      rcx, qword ptr [r13 + r14*8]
0030A0C5  inc      r14
0030A0C8  movzx    edx, word ptr [rcx + 0xdc8]
0030A0CF  lea      ecx, [rbx + 1]
0030A0D2  cmp      dx, r12w
0030A0D6  cmovne   ecx, ebx
0030A0D9  mov      ebx, ecx
0030A0DB  cmp      r14, rax
0030A0DE  jl       0x30a0c0  ; -> 0030A0C0
0030A0E0  mov      eax, ebx
0030A0E2  add      rsp, 0x28
0030A0E6  pop      r14
0030A0E8  pop      r13
0030A0EA  pop      r12
0030A0EC  pop      rbx
0030A0ED  ret      
```

## 00321380 (127 B, extent 00321380-003213FF)

Page context: "', the mode-object getter the batch-169 '00320CA0' gate reaches through '[+0x698]', is a shared helper those layers' bodies call directly ('003206E0', '003247F0', '00324F20', '003176E0', '0031ADB0', '00321380', '00386860', '00310DB0', '00301140' among them), while '00309A90', '0030EC00', '0023A570', '00265680', '002ECF10' and '0030C470' exchange calls with the same layers in return - shared-helper fan-in on a runtime getter, not a share"

```
00321380  push     rbx
00321382  sub      rsp, 0x20
00321386  mov      dword ptr [rdx], 0xffffffff
0032138C  mov      rbx, rdx
0032138F  test     byte ptr [rip + 0x1d67faa], 0x10  ; -> 02089340
00321396  je       0x3213f6  ; -> 003213F6
00321398  call     0x3588b0  ; -> 003588B0 fn
0032139D  test     rax, rax
003213A0  je       0x3213f6  ; -> 003213F6
003213A2  mov      rcx, rax
003213A5  call     0x263e30  ; -> 00263E30 fn
003213AA  test     rax, rax
003213AD  je       0x3213f6  ; -> 003213F6
003213AF  mov      dword ptr [rbx], 0xffffffff
003213B5  mov      rax, qword ptr [rax + 0x698]
003213BC  test     rax, rax
003213BF  jne      0x3213cc  ; -> 003213CC
003213C1  mov      eax, 0xfffffffe
003213C6  add      rsp, 0x20
003213CA  pop      rbx
003213CB  ret      
003213CC  mov      dword ptr [rbx], 0xffffffff
003213D2  add      rax, 0x50
003213D6  je       0x3213eb  ; -> 003213EB
003213D8  movzx    ecx, word ptr [rax]
003213DB  mov      rdx, rbx
003213DE  call     0x321400  ; -> 00321400 fn
003213E3  xor      eax, eax
003213E5  add      rsp, 0x20
003213E9  pop      rbx
003213EA  ret      
003213EB  mov      eax, 0xfffffffd
003213F0  add      rsp, 0x20
003213F4  pop      rbx
003213F5  ret      
003213F6  or       eax, 0xffffffff
003213F9  add      rsp, 0x20
003213FD  pop      rbx
003213FE  ret      
```

## 00327240 (39 B, extent 00327240-00327267)

Page context: "→ 'ret' (the doc table's "if bit 0 is still on" reads it the other way; 'je' at '0031365E' jumps on clear) | '00313657' 'test byte [rax+0x5B04], 1' | | 2, 0 | '00304180' | '0031B8C0(3)' object, then '00327240' — the same-mode collect | '00304195' 'mov ecx, 3' | | 2, 1 | '00304400' | clears '+0x5AE0' bit 0, '00327200'→'0031ABF0', clears '022C1F48' bits, tail '002E28D0' | '0030440B' 'and dword [rax+0x5AE0], ~1' | | 2, 2 | '00304060' | '00"

```
00327240  mov      rdx, qword ptr [rip + 0x2b97f49]  ; -> 02EBF190
00327247  movzx    eax, byte ptr [rdx + 0x5aa4]
0032724E  cmp      al, 0x27
00327250  jbe      0x327255  ; -> 00327255
00327252  xor      eax, eax
00327254  ret      
00327255  movzx    eax, al
00327258  imul     rcx, rax, 0x1c8
0032725F  lea      rax, [rdx + 8]
00327263  add      rax, rcx
00327266  ret      
```

## 0034A640 (91 B, extent 0034A640-0034A69B)

Page context: "BE0(rcx, ecx)' runs as a tail call on the same '0209BE80' global the gate family reads.  Interior anchor '00290509' (function '00290500').  '002E26F0' (454 B) is the two-record comparator '002E28C0'/'0034A640' call: 'rsi = [rcx+0xC0]' / 'rdi = [rdx+0xC0]' null-gate, 'byte[rax+0x14F] & 1' runs '002E6B10(rbx)', 'dword[rsi] == -1' sentinels short-circuit, then '0025D480'/'0025D540'/'002EDAA0'/'0042F3B0' compare the pair - the ladder's tran"

```
0034A640  mov      qword ptr [rsp + 8], rbx
0034A645  mov      qword ptr [rsp + 0x10], rsi
0034A64A  push     rdi
0034A64B  sub      rsp, 0x20
0034A64F  mov      rcx, r9
0034A652  mov      rbx, r9
0034A655  mov      rdi, rdx
0034A658  call     0x267e10  ; -> 00267E10 fn
0034A65D  mov      rcx, rbx
0034A660  mov      esi, eax
0034A662  call     0x267e10  ; -> 00267E10 fn
0034A667  mov      ebx, eax
0034A669  call     0x2640c0  ; -> 002640C0 fn
0034A66E  mov      edx, ebx
0034A670  mov      rcx, rax
0034A673  call     0x358940  ; -> 00358940 fn
0034A678  test     rax, rax
0034A67B  je       0x34a68b  ; -> 0034A68B
0034A67D  mov      r8d, esi
0034A680  mov      rdx, rdi
0034A683  mov      rcx, rax
0034A686  call     0x2e26f0  ; -> 002E26F0 fn
0034A68B  mov      rbx, qword ptr [rsp + 0x30]
0034A690  mov      rsi, qword ptr [rsp + 0x38]
0034A695  add      rsp, 0x20
0034A699  pop      rdi
0034A69A  ret      
```

## 0034FE80 (30 B, extent 0034FE80-0034FE9E)

Page context: "scriptvm-verb-table.tsv):  | verb | id | handler | what it does to '+0x5B04' | |---|---:|---|---| | 'summonread' | '0203' | '0034E1F0' → '00313550(1)' | sets bit 0 | | 'summontopartyread' | '0207' | '0034FE80' → '00313550(0)' | clears bit 0 | | 'btlAtelSetSummonMode' | '3044' | '0050FFB0' → '003139C0(esper)' then '00313550(on)' | sets '+0x5AD4' to the Esper's row and bit 0 | | 'getsummonmodebit' / 'getsummonmode' | '0512' / '0408' | thu"

```
0034FE80  sub      rsp, 0x28
0034FE84  xor      ecx, ecx
0034FE86  call     0x313550  ; -> 00313550 fn
0034FE8B  mov      ecx, 1
0034FE90  call     0x314d40  ; -> 00314D40 fn
0034FE95  add      rsp, 0x28
0034FE99  jmp      0x37ca00  ; -> 0037CA00 fn
```

## 0035D660 (75 B, extent 0035D660-0035D6AB)

Page context: " runs) must carry the request's bit — 'bt r10d, ebx' fails to 0. Past the gate '0017E7D0'/'0035DA80'/ '003C8990' run, then 'ebx - 1 <= 0x17' dispatches a six-arm jump table at '0x134C58'/'0x134C70' ('0035D660', '0035D980', '003C87B0', '0028E970' returning 1, '0035D080'); out-of-range ids fall to '0028F970()' plus a '00280A00(ecx, edx, r8)' passthrough. Interior anchor '00254BF9' (the 'jmp rcx' dispatch).  ## SWE2-EC7-33 update (2026-09-"

```
0035D660  push     rbx
0035D662  sub      rsp, 0x20
0035D666  mov      ebx, ecx
0035D668  call     0x2e0fa0  ; -> 002E0FA0 fn
0035D66D  bt       eax, 0xa
0035D671  jae      0x35d67b  ; -> 0035D67B
0035D673  xor      eax, eax
0035D675  add      rsp, 0x20
0035D679  pop      rbx
0035D67A  ret      
0035D67B  call     0x3669d0  ; -> 003669D0 fn
0035D680  test     eax, eax
0035D682  jne      0x35d673  ; -> 0035D673
0035D684  cmp      ebx, 1
0035D687  jne      0x35d699  ; -> 0035D699
0035D689  test     byte ptr [rip + 0x1f6a9d1], bl  ; -> 022C8060
0035D68F  jne      0x35d699  ; -> 0035D699
0035D691  cmp      dword ptr [rip + 0x1f6a9d5], eax  ; -> 022C806C
0035D697  je       0x35d673  ; -> 0035D673
0035D699  mov      ecx, ebx
0035D69B  call     0x28fd50  ; -> 0028FD50 fn
0035D6A0  mov      eax, 1
0035D6A5  add      rsp, 0x20
0035D6A9  pop      rbx
0035D6AA  ret      
```

## 0035D8D0 (171 B, extent 0035D8D0-0035D97B)

Page context: "roed - the flag drop plus head reset the field-frame and runtime arms share. Interior anchor '00238A69' (the first qword clear).  '00254980' (101 B) is the mode-selecting call battery the '0035D6B0'/'0035D8D0'/'0035D980'/'0035DA80' ladder quartet shares: 'ecx == 0' picks '002E1C20', any other mode picks '002E1CA0', and the selected helper runs six '(8, n)' pairs - 'edx' = 1, 8, 0, 0xB, 9, 6 - before a tail '(8, 0x14)'; 'ecx' itself is c"

```
0035D8D0  sub      rsp, 0x28
0035D8D4  call     0x2904b0  ; -> 002904B0 fn
0035D8D9  test     eax, eax
0035D8DB  je       0x35d976  ; -> 0035D976
0035D8E1  mov      ecx, 1
0035D8E6  call     0x290450  ; -> 00290450 fn
0035D8EB  xor      ecx, ecx
0035D8ED  mov      dword ptr [rip + 0x1f6aa89], 0  ; -> 022C8380
0035D8F7  call     0x290500  ; -> 00290500 fn
0035D8FC  and      dword ptr [rip + 0x1f6a75d], 0xfffffffb  ; -> 022C8060
0035D903  call     0x252d90  ; -> 00252D90 fn
0035D908  xor      ecx, ecx
0035D90A  call     0x254980  ; -> 00254980 fn
0035D90F  mov      eax, dword ptr [rip + 0x1f6aad3]  ; -> 022C83E8
0035D915  test     al, 0x10
0035D917  je       0x35d932  ; -> 0035D932
0035D919  or       eax, 0x10
0035D91C  mov      ecx, 1
0035D921  mov      dword ptr [rip + 0x1f6aac1], eax  ; -> 022C83E8
0035D927  call     0x2548f0  ; -> 002548F0 fn
0035D92C  mov      eax, dword ptr [rip + 0x1f6aab6]  ; -> 022C83E8
0035D932  test     al, 1
0035D934  je       0x35d958  ; -> 0035D958
0035D936  or       eax, 1
0035D939  mov      ecx, 1
0035D93E  mov      dword ptr [rip + 0x1f6aaa4], eax  ; -> 022C83E8
0035D944  call     0x254940  ; -> 00254940 fn
0035D949  mov      eax, dword ptr [rip + 0x1f6aa99]  ; -> 022C83E8
0035D94F  and      eax, 0xffffffef
0035D952  mov      dword ptr [rip + 0x1f6aa90], eax  ; -> 022C83E8
0035D958  test     al, 2
0035D95A  je       0x35d976  ; -> 0035D976
0035D95C  or       eax, 2
0035D95F  mov      ecx, 1
0035D964  mov      dword ptr [rip + 0x1f6aa7e], eax  ; -> 022C83E8
0035D96A  call     0x254850  ; -> 00254850 fn
0035D96F  and      dword ptr [rip + 0x1f6aa72], 0xffffffee  ; -> 022C83E8
0035D976  add      rsp, 0x28
0035D97A  ret      
```

## 00363560 (96 B, extent 00363560-003635C0)

Page context: "dio bodies '00229AF0', '003638B0', '00362850' call page-cited '003603C0', '00229EA0', '002E0FA0'); 9 outbound (page-cited '00228C70', '00366870', '00226280' call Audio bodies '002DF370', '002DEE70', '00363560'). Substantive edges include '00228C70' calls '00363560'; '00228C70' calls '00360D70'; '00228C70' calls '00249CA0'; '00228C70' calls '002DEE70'; the remaining edges run through shared helpers the page cites. - **Input — CLIENT and "

```
00363560  sub      rsp, 0x28
00363564  cmp      dword ptr [rip + 0x1f68505], 0  ; -> 022CBA70
0036356B  mov      edx, dword ptr [rip + 0x1f6850b]  ; -> 022CBA7C
00363571  jne      0x363577  ; -> 00363577
00363573  test     edx, edx
00363575  je       0x36357e  ; -> 0036357E
00363577  xor      ecx, ecx
00363579  call     0x2df0f0  ; -> 002DF0F0 fn
0036357E  mov      dword ptr [rip + 0x1f684e8], 0  ; -> 022CBA70
00363588  mov      byte ptr [rip + 0x1f6859e], 0  ; -> 022CBB2D
0036358F  mov      byte ptr [rip + 0x1f68598], 0  ; -> 022CBB2E
00363596  call     0x362850  ; -> 00362850 fn
0036359B  call     0x3636a0  ; -> 003636A0 fn
003635A0  call     0x363750  ; -> 00363750 fn
003635A5  call     0x362850  ; -> 00362850 fn
003635AA  or       ecx, 0xffffffff
003635AD  call     0x2df690  ; -> 002DF690 fn
003635B2  or       edx, 0xffffffff
003635B5  xor      ecx, ecx
003635B7  add      rsp, 0x28
003635BB  jmp      0x2df0f0  ; -> 002DF0F0 fn
```

## 003AA430 (56 B, extent 003AA430-003AA468)

Page context: "r anchor '0027019D' (a '0024F650' call).  ## SWE2-EC7-49 update (2026-09-19) - '003A74F0'  '003A74F0' (189 B) is a battle-runtime ladder body - '003337B0'/'003A7360'/'003A7460'/'003A81E0'/'003A9160'/'003AA430'. Interior anchor '003A74FD' (a '003337B0' call).  ## SWE2-EC7-51 update (2026-09-19) - '003B2830'  '003B2830' (179 B) is a body - '0024FE70'/'0036C140'/'0036C1D0'. Interior anchor '003B288F' (a '0024FE70' call).  ## SWE2-EC7-54 up"

```
003AA430  push     rbx
003AA432  sub      rsp, 0x20
003AA436  mov      rbx, qword ptr [rip + 0x2b14b33]  ; -> 02EBEF70
003AA43D  mov      rbx, qword ptr [rbx]
003AA440  test     rbx, rbx
003AA443  je       0x3aa462  ; -> 003AA462
003AA445  cmp      byte ptr [rbx + 0xe], 0x59
003AA449  jne      0x3aa453  ; -> 003AA453
003AA44B  mov      rcx, rbx
003AA44E  call     0x5043f0  ; -> 005043F0 fn
003AA453  mov      ecx, dword ptr [rbx]
003AA455  call     0x20e600  ; -> 0020E600 fn
003AA45A  mov      rbx, rax
003AA45D  test     rax, rax
003AA460  jne      0x3aa445  ; -> 003AA445
003AA462  add      rsp, 0x20
003AA466  pop      rbx
003AA467  ret      
```

## 003B54C0 (82 B, extent 003B54C0-003B5512)

Page context: "' call).  ## SWE2-EC7-37 update (2026-09-19) - '003B4B60'  '003B4B60' (567 B) is a battle-runtime mode body - '02B40512'/'02B4050A'/'02B40508'/'02B40511' byte flags, '002EA030'/'003E56C0' pairs plus '003B54C0'/'003E6AA0'/'003B4FD0'. Interior anchor '003B4BBF' (an '002EA030' call).  ## SWE2-EC7-39 update (2026-09-19) - '003B5520'  '003B5520' (428 B) is a battle-runtime-mode body - '02B40508'..'02B40514' byte fields/'022C6F28', '003E6AA0'"

```
003B54C0  push     rbx
003B54C2  sub      rsp, 0x20
003B54C6  movzx    eax, word ptr [rcx + 4]
003B54CA  mov      rbx, rcx
003B54CD  cmp      ax, -1
003B54D1  je       0x3b5508  ; -> 003B5508
003B54D3  movsx    rax, ax
003B54D7  imul     rcx, rax, 0x740
003B54DE  xor      eax, eax
003B54E0  add      rcx, qword ptr [rip + 0x1f11a41]  ; -> 022C6F28
003B54E7  cmp      dword ptr [rcx + 0x284], eax
003B54ED  cmove    rcx, rax
003B54F1  test     rcx, rcx
003B54F4  je       0x3b54fe  ; -> 003B54FE
003B54F6  lea      edx, [rax + 2]
003B54F9  call     0x3e6aa0  ; -> 003E6AA0 fn
003B54FE  mov      byte ptr [rbx + 2], 2
003B5502  add      rsp, 0x20
003B5506  pop      rbx
003B5507  ret      
003B5508  mov      byte ptr [rcx + 2], 2
003B550C  add      rsp, 0x20
003B5510  pop      rbx
003B5511  ret      
```

## 003CA1E0 (27 B, extent 003CA1E0-003CA1FB)

Page context: "C7 batch-149).** '0028FD70', a callee the '0035D980' entry's teardown arm cites, sits inside that layer's fan-in: it calls UI bodies '00290E10'/'002964D0'/'00296AA0'/'002970C0'/'00297100'/'003CA1C0'/'003CA1E0' and is itself called by the UI-filed '0035D6B0' - the ladder borrows a shared teardown step; the UI edges are that helper's own traffic, not a UI responsibility of this page.  **WorldAreaField — CONSULTED BOTH DIRECTIONS (SWE2-EC7"

```
003CA1E0  mov      rax, qword ptr [rip + 0x277d571]  ; -> 02B47758
003CA1E7  test     rax, rax
003CA1EA  je       0x3ca1fa  ; -> 003CA1FA
003CA1EC  and      dword ptr [rax + 0xa90], 0xfffffffd
003CA1F3  or       dword ptr [rax + 0xa90], 1
003CA1FA  ret      
```

## 00420E70 (41 B, extent 00420E70-00420E99)

Page context: "one carrying '(+0x304 >> 0xA) & 1' in the stack out-record's flag slot  Interior anchor '0042B6E2' (function '0042B690').  '0042B770' (216 B) is the fourth sibling walk over the same table - visitor '00420E70', flag '(+0x304 >> 0xB) & 1', recursion through '0042EF90' on the '+8'/'+0xA' links - the batch-152 '00429F70'/'00429500' pair completed into a four-visitor ladder  Interior anchor '0042B7C2' (function '0042B770').  '00420D80' (228"

```
00420E70  and      byte ptr [rcx + 0x2ae], 0xfd
00420E77  mov      eax, edx
00420E79  mov      r9d, edx
00420E7C  neg      eax
00420E7E  sbb      r8b, r8b
00420E81  xor      edx, edx
00420E83  and      r8b, 2
00420E87  or       byte ptr [rcx + 0x2ae], r8b
00420E8E  test     r9d, r9d
00420E91  sete     dl
00420E94  jmp      0x421280  ; -> 00421280 fn
```

## 00422E50 (96 B, extent 00422E50-00422EB0)

Page context: "ax') computes 'r8d = sword[rax+0xCC]' and 'edx = (byte[rax+0x40B] << 6) >>s 6'; a non'-1' '0041E5B0' result tail-jumps '00423FC0', otherwise '+0xCC < 0x1000' picks '00422E40(xmm1 = [rdi+0x28])' over '00422E50'  Interior anchor '0042DF66' (function '0042DF10').  '003EBBB0' (148 B) is the '02B5EBC0' '0x14'-row updater '0032A100' calls, the same record shape this page's '003EBC50' commits: '[row] = edx', '[row+4] = r8d'; '00290180()' picks"

```
00422E50  push     rbx
00422E52  sub      rsp, 0x30
00422E56  cmp      dword ptr [rcx + 0xc8], -1
00422E5D  mov      rbx, rcx
00422E60  movaps   xmmword ptr [rsp + 0x20], xmm6
00422E65  movaps   xmm6, xmm1
00422E68  je       0x422e95  ; -> 00422E95
00422E6A  mov      ecx, dword ptr [rcx + 0x10]
00422E6D  call     0x20e600  ; -> 0020E600 fn
00422E72  mov      edx, dword ptr [rbx + 0xc8]
00422E78  mov      rcx, qword ptr [rax + 0xda8]
00422E7F  call     0x51b9e0  ; -> 0051B9E0 fn
00422E84  test     rax, rax
00422E87  je       0x422e95  ; -> 00422E95
00422E89  or       dword ptr [rax + 0xc], 2
00422E8D  mov      rcx, rax
00422E90  call     0x41d790  ; -> 0041D790 fn
00422E95  mov      r8d, 1
00422E9B  movaps   xmm1, xmm6
00422E9E  mov      rcx, rbx
00422EA1  movaps   xmm6, xmmword ptr [rsp + 0x20]
00422EA6  add      rsp, 0x30
00422EAA  pop      rbx
00422EAB  jmp      0x424a40  ; -> 00424A40 fn
```

## 0050FFB0 (59 B, extent 0050FFB0-0050FFEB)

Page context: "---|---:|---|---| | 'summonread' | '0203' | '0034E1F0' → '00313550(1)' | sets bit 0 | | 'summontopartyread' | '0207' | '0034FE80' → '00313550(0)' | clears bit 0 | | 'btlAtelSetSummonMode' | '3044' | '0050FFB0' → '003139C0(esper)' then '00313550(on)' | sets '+0x5AD4' to the Esper's row and bit 0 | | 'getsummonmodebit' / 'getsummonmode' | '0512' / '0408' | thunks '0037C900' → '003135E0', '0037C8F0' → '003135C0' | read bit 0 / the mode | |"

```
0050FFB0  mov      qword ptr [rsp + 8], rbx
0050FFB5  push     rdi
0050FFB6  sub      rsp, 0x20
0050FFBA  mov      rcx, r9
0050FFBD  mov      rbx, r9
0050FFC0  call     0x267e10  ; -> 00267E10 fn
0050FFC5  mov      rcx, rbx
0050FFC8  mov      edi, eax
0050FFCA  call     0x267e10  ; -> 00267E10 fn
0050FFCF  movzx    ecx, dil
0050FFD3  mov      ebx, eax
0050FFD5  call     0x3139c0  ; -> 003139C0 fn
0050FFDA  mov      ecx, ebx
0050FFDC  mov      rbx, qword ptr [rsp + 0x30]
0050FFE1  add      rsp, 0x20
0050FFE5  pop      rdi
0050FFE6  jmp      0x313550  ; -> 00313550 fn
```
