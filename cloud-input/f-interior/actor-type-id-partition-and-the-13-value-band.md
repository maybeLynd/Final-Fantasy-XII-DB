# F-interior pack: `04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/actor-type-id-partition-and-the-13-value-band.json`.

Functions: 7. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ; inbox mentions: ASSIGNMENTS.md, repos-1e.md, repos-c7.md). OPUS read these before packing.

## 00322350 (12 B, extent 00322350-0032235C)

Page context: "y table and its stride | the three '.rdata' constants read from the image plus the literal '0x4E' | 1 | | '7..25' is tested identically at both layers | 'sub al,7 ; cmp al,0x12' in '0050FF87' and in '00322350' | 1 |  **Controls, and a defect in this document's own instrument.** The census keyed on 'mov reg, [reg+4]' followed by an immediate comparison. **That form misses 'cmp byte ptr [reg+4], imm', which never loads into a register** —"

```
00322350  xor      eax, eax
00322352  sub      cl, 7
00322355  cmp      cl, 0x12
00322358  setbe    al
0032235B  ret      
```

## 0034E7D0 (211 B, extent 0034E7D0-0034E8A3)

Page context: "cipients test.  **Script_VM_Native_Bridge — CLIENT and SERVICE (14 edges).** Seven verb bodies read the mapped-slot getter '00320AB0', '0050FD00' to '0050FF20' among them. Five more call '00322350': '0034E7D0', '00351A40', '00352190', '00353460' and '00353CB0'. The ladder '0050FF20' itself pops its argument through 'VMValueStack_PopNumericDiscard' '00267DB0' and returns its class through 'VMResult_WriteInt32' '0026B4E0'. Script reads th"

```
0034E7D0  mov      qword ptr [rsp + 8], rbx
0034E7D5  mov      qword ptr [rsp + 0x10], rbp
0034E7DA  mov      qword ptr [rsp + 0x18], rsi
0034E7DF  push     rdi
0034E7E0  push     r14
0034E7E2  push     r15
0034E7E4  sub      rsp, 0x20
0034E7E8  mov      esi, 4
0034E7ED  mov      r14, r9
0034E7F0  mov      r15, rcx
0034E7F3  xor      ebp, ebp
0034E7F5  lea      ebx, [rsi - 2]
0034E7F8  lea      edi, [rsi - 3]
0034E7FB  nop      dword ptr [rax + rax]
0034E800  mov      rcx, r14
0034E803  call     0x267e10  ; -> 00267E10 fn
0034E808  mov      ecx, eax
0034E80A  test     eax, eax
0034E80C  js       0x34e81f  ; -> 0034E81F
0034E80E  mov      edx, edi
0034E810  shl      edx, cl
0034E812  or       ebp, edx
0034E814  call     0x322350  ; -> 00322350 fn
0034E819  test     eax, eax
0034E81B  je       0x34e81f  ; -> 0034E81F
0034E81D  dec      esi
0034E81F  sub      ebx, edi
0034E821  jns      0x34e800  ; -> 0034E800
0034E823  cmp      esi, 4
0034E826  mov      ebx, 3
0034E82B  cmovne   ebx, esi
0034E82E  call     0x359ba0  ; -> 00359BA0 fn
0034E833  mov      esi, eax
0034E835  call     0x359c00  ; -> 00359C00 fn
0034E83A  and      eax, ebp
0034E83C  cmp      eax, ebp
0034E83E  je       0x34e845  ; -> 0034E845
0034E840  or       ebx, 0xffffffff
0034E843  jmp      0x34e87c  ; -> 0034E87C
0034E845  or       esi, ebp
0034E847  mov      ecx, esi
0034E849  call     0x35a050  ; -> 0035A050 fn
0034E84E  mov      edx, eax
0034E850  rol      edi, 0
0034E853  mov      r8d, 0x10
0034E859  nop      dword ptr [rax]
0034E860  test     edx, edi
0034E862  lea      ecx, [rbx - 1]
0034E865  cmove    ecx, ebx
0034E868  rol      edi, 1
0034E86A  mov      eax, edi
0034E86C  rol      edi, 1
0034E86E  and      eax, edx
0034E870  lea      ebx, [rcx - 1]
0034E873  cmove    ebx, ecx
0034E876  sub      r8, 1
0034E87A  jne      0x34e860  ; -> 0034E860
0034E87C  not      ebx
0034E87E  mov      rcx, r15
0034E881  shr      ebx, 0x1f
0034E884  mov      edx, ebx
0034E886  mov      rbx, qword ptr [rsp + 0x40]
0034E88B  mov      rbp, qword ptr [rsp + 0x48]
0034E890  mov      rsi, qword ptr [rsp + 0x50]
0034E895  add      rsp, 0x20
0034E899  pop      r15
0034E89B  pop      r14
0034E89D  pop      rdi
0034E89E  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00350160 (98 B, extent 00350160-003501C2)

Page context: "yFocus_IsCurrentPackedActorHandle' '003273B0'. '00304180' reads '00320AB0'. Three party verbs call the '7..25' test '00322350' (§6): 'VMPartyCommand_MoveSelector00To06OutOfRuntimeRosterWhenMultiple' '00350160', 'VMPartyCommand_DemoteOtherRuntimeRosterSelectors' '00350CD0' and 'VMPartyCommand_RemoveSelector07To25' '00352AF0'. The '7..25' span is the party layer's guest range, tested identically there and in the Script-VM ladder, and the "

```
00350160  push     rbx
00350162  sub      rsp, 0x40
00350166  mov      rax, qword ptr [rip + 0x1bf46c3]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0035016D  xor      rax, rsp
00350170  mov      qword ptr [rsp + 0x30], rax
00350175  mov      rcx, r9
00350178  call     0x267e10  ; -> 00267E10 fn
0035017D  mov      ecx, 0x13
00350182  mov      ebx, eax
00350184  call     0x3601b0  ; -> 003601B0 fn
00350189  movzx    ecx, bl
0035018C  call     0x322350  ; -> 00322350 fn
00350191  test     eax, eax
00350193  jne      0x3501af  ; -> 003501AF
00350195  lea      edx, [rax + 4]
00350198  lea      rcx, [rsp + 0x20]
0035019D  call     0x31b510  ; -> 0031B510 fn
003501A2  cmp      eax, 1
003501A5  jle      0x3501af  ; -> 003501AF
003501A7  movzx    ecx, bl
003501AA  call     0x3286e0  ; -> 003286E0 fn
003501AF  mov      rcx, qword ptr [rsp + 0x30]
003501B4  xor      rcx, rsp
003501B7  call     0x808c40  ; -> 00808C40 fn
003501BC  add      rsp, 0x40
003501C0  pop      rbx
003501C1  ret      
```

## 00351A40 (81 B, extent 00351A40-00351A91)

Page context: "t.  **Script_VM_Native_Bridge — CLIENT and SERVICE (14 edges).** Seven verb bodies read the mapped-slot getter '00320AB0', '0050FD00' to '0050FF20' among them. Five more call '00322350': '0034E7D0', '00351A40', '00352190', '00353460' and '00353CB0'. The ladder '0050FF20' itself pops its argument through 'VMValueStack_PopNumericDiscard' '00267DB0' and returns its class through 'VMResult_WriteInt32' '0026B4E0'. Script reads the partition "

```
00351A40  mov      qword ptr [rsp + 8], rbx
00351A45  push     rdi
00351A46  sub      rsp, 0x20
00351A4A  mov      rcx, r9
00351A4D  mov      rbx, r9
00351A50  call     0x267e10  ; -> 00267E10 fn
00351A55  mov      rcx, rbx
00351A58  mov      edi, eax
00351A5A  call     0x267e10  ; -> 00267E10 fn
00351A5F  mov      ecx, 0x13
00351A64  mov      ebx, eax
00351A66  call     0x3601b0  ; -> 003601B0 fn
00351A6B  movzx    ecx, bl
00351A6E  call     0x322350  ; -> 00322350 fn
00351A73  test     eax, eax
00351A75  jne      0x351a86  ; -> 00351A86
00351A77  xor      edx, edx
00351A79  movzx    ecx, bl
00351A7C  test     edi, edi
00351A7E  setne    dl
00351A81  call     0x328fb0  ; -> 00328FB0 fn
00351A86  mov      rbx, qword ptr [rsp + 0x30]
00351A8B  add      rsp, 0x20
00351A8F  pop      rdi
00351A90  ret      
```

## 00352190 (94 B, extent 00352190-003521EE)

Page context: "_VM_Native_Bridge — CLIENT and SERVICE (14 edges).** Seven verb bodies read the mapped-slot getter '00320AB0', '0050FD00' to '0050FF20' among them. Five more call '00322350': '0034E7D0', '00351A40', '00352190', '00353460' and '00353CB0'. The ladder '0050FF20' itself pops its argument through 'VMValueStack_PopNumericDiscard' '00267DB0' and returns its class through 'VMResult_WriteInt32' '0026B4E0'. Script reads the partition through the "

```
00352190  mov      qword ptr [rsp + 8], rbx
00352195  push     rdi
00352196  sub      rsp, 0x20
0035219A  mov      rcx, r9
0035219D  call     0x267e10  ; -> 00267E10 fn
003521A2  mov      edi, eax
003521A4  xor      ebx, ebx
003521A6  mov      ecx, ebx
003521A8  call     0x263750  ; -> 00263750 fn
003521AD  test     rax, rax
003521B0  je       0x3521bc  ; -> 003521BC
003521B2  xor      edx, edx
003521B4  mov      rcx, rax
003521B7  call     0x26dc40  ; -> 0026DC40 fn
003521BC  inc      ebx
003521BE  cmp      ebx, 4
003521C1  jl       0x3521a6  ; -> 003521A6
003521C3  mov      ecx, 0x13
003521C8  call     0x3601b0  ; -> 003601B0 fn
003521CD  movzx    ecx, dil
003521D1  call     0x322350  ; -> 00322350 fn
003521D6  test     eax, eax
003521D8  je       0x3521e3  ; -> 003521E3
003521DA  movzx    ecx, dil
003521DE  call     0x3170e0  ; -> 003170E0 fn
003521E3  mov      rbx, qword ptr [rsp + 0x30]
003521E8  add      rsp, 0x20
003521EC  pop      rdi
003521ED  ret      
```

## 00352AF0 (57 B, extent 00352AF0-00352B29)

Page context: "'00322350' (§6): 'VMPartyCommand_MoveSelector00To06OutOfRuntimeRosterWhenMultiple' '00350160', 'VMPartyCommand_DemoteOtherRuntimeRosterSelectors' '00350CD0' and 'VMPartyCommand_RemoveSelector07To25' '00352AF0'. The '7..25' span is the party layer's guest range, tested identically there and in the Script-VM ladder, and the party verbs are what act on it.  **Presentation — SERVICE (1 edge).** '00301AD0' calls 'BattleUnit_TestActorViewFrus"

```
00352AF0  push     rbx
00352AF2  sub      rsp, 0x20
00352AF6  mov      rcx, r9
00352AF9  call     0x267e10  ; -> 00267E10 fn
00352AFE  mov      ecx, 0x13
00352B03  mov      ebx, eax
00352B05  call     0x3601b0  ; -> 003601B0 fn
00352B0A  movzx    ecx, bl
00352B0D  call     0x322350  ; -> 00322350 fn
00352B12  test     eax, eax
00352B14  je       0x352b23  ; -> 00352B23
00352B16  movzx    ecx, bl
00352B19  add      rsp, 0x20
00352B1D  pop      rbx
00352B1E  jmp      0x3288f0  ; -> 003288F0 fn
00352B23  add      rsp, 0x20
00352B27  pop      rbx
00352B28  ret      
```

## 00353CB0 (69 B, extent 00353CB0-00353CF5)

Page context: "and SERVICE (14 edges).** Seven verb bodies read the mapped-slot getter '00320AB0', '0050FD00' to '0050FF20' among them. Five more call '00322350': '0034E7D0', '00351A40', '00352190', '00353460' and '00353CB0'. The ladder '0050FF20' itself pops its argument through 'VMValueStack_PopNumericDiscard' '00267DB0' and returns its class through 'VMResult_WriteInt32' '0026B4E0'. Script reads the partition through the five-way ladder (classes −2"

```
00353CB0  mov      qword ptr [rsp + 8], rbx
00353CB5  push     rdi
00353CB6  sub      rsp, 0x20
00353CBA  mov      rdi, rcx
00353CBD  mov      rcx, r9
00353CC0  call     0x267e10  ; -> 00267E10 fn
00353CC5  movzx    ecx, al
00353CC8  mov      ebx, eax
00353CCA  call     0x322350  ; -> 00322350 fn
00353CCF  mov      ecx, ebx
00353CD1  test     eax, eax
00353CD3  je       0x353cdc  ; -> 00353CDC
00353CD5  call     0x3596d0  ; -> 003596D0 fn
00353CDA  jmp      0x353ce1  ; -> 00353CE1
00353CDC  call     0x359740  ; -> 00359740 fn
00353CE1  mov      edx, eax
00353CE3  mov      rcx, rdi
00353CE6  mov      rbx, qword ptr [rsp + 0x30]
00353CEB  add      rsp, 0x20
00353CEF  pop      rdi
00353CF0  jmp      0x26b4e0  ; -> 0026B4E0 fn
```
