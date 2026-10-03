# Homing pack: `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-scriptvm-verb-dispatch-and-parameter-encoding.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00264110 (52 B, extent 00264110-00264144)

Entered from (direct sites whose caller this page cites): `00377900` + 0x35 (call; `00377900` is cited on this page)
Other direct sites: none

Host context: "is called by '00266D10'; the remaining edges run through shared helpers the page cites. - **WorldAreaField — CLIENT and SERVICE (16 edges).** 6 inbound (WorldAreaField bodies '00377AB0', '00377A90', '00377900' call page-cited '003A1C50', 'FieldData_CopyIndexedRecordByFormatClass' (003DFD00), '00264B50'); 10 outbound (page-cited '002628B0', '00280140', '00264B50' call WorldAreaField bodies '003DFA50', '003EAA00', '00378230'). Substantive"

```
00264110  sub      rsp, 0x48
00264114  mov      rax, qword ptr [rsp + 0x78]
00264119  mov      qword ptr [rsp + 0x30], rax
0026411E  mov      rax, qword ptr [rsp + 0x70]
00264123  mov      qword ptr [rsp + 0x28], rax
00264128  mov      qword ptr [rsp + 0x20], r9
0026412D  mov      r9, r8
00264130  mov      r8d, edx
00264133  mov      edx, ecx
00264135  mov      ecx, 1
0026413A  call     0x264b90  ; -> 00264B90 fn
0026413F  add      rsp, 0x48
00264143  ret      
```

## 00264B90 (267 B, extent 00264B90-00264C9B)

Entered from (direct sites whose caller this page cites): `00264B50` + 0x27 (call; `00264B50` is cited on this page)
Other direct sites: `00264110` + 0x2A (call)

Host context: "rldAreaField — CLIENT and SERVICE (16 edges).** 6 inbound (WorldAreaField bodies '00377AB0', '00377A90', '00377900' call page-cited '003A1C50', 'FieldData_CopyIndexedRecordByFormatClass' (003DFD00), '00264B50'); 10 outbound (page-cited '002628B0', '00280140', '00264B50' call WorldAreaField bodies '003DFA50', '003EAA00', '00378230'). Substantive edges include '00280140' calls 'WorldTransition_RequeueCurrentFieldForRestore' (00267C90); '0"

```
00264B90  mov      qword ptr [rsp + 0x10], rbx
00264B95  mov      qword ptr [rsp + 0x18], rbp
00264B9A  mov      qword ptr [rsp + 0x20], rsi
00264B9F  push     r12
00264BA1  push     r14
00264BA3  push     r15
00264BA5  sub      rsp, 0x20
00264BA9  mov      r14, qword ptr [rsp + 0x60]
00264BAE  xor      r12d, r12d
00264BB1  mov      r15, qword ptr [rsp + 0x68]
00264BB6  mov      rsi, r9
00264BB9  mov      rbp, qword ptr [rsp + 0x70]
00264BBE  mov      dword ptr [r9], r12d
00264BC1  mov      dword ptr [r14], r12d
00264BC4  movsxd   rax, edx
00264BC7  imul     rdx, rax, 0x288
00264BCE  mov      dword ptr [r15], r12d
00264BD1  lea      rax, [rip + 0x1e34238]  ; -> 02098E10
00264BD8  mov      dword ptr [rbp], r12d
00264BDC  mov      rbx, qword ptr [rdx + rax]
00264BE0  test     rbx, rbx
00264BE3  je       0x264c96  ; -> 00264C96
00264BE9  mov      qword ptr [rsp + 0x40], rdi
00264BEE  cmp      r8d, -1
00264BF2  jne      0x264bf9  ; -> 00264BF9
00264BF4  movsx    r8d, word ptr [rbx + 0x52]
00264BF9  cmp      r8d, -2
00264BFD  jne      0x264c04  ; -> 00264C04
00264BFF  movsx    r8d, word ptr [rbx + 0x78]
00264C04  cmp      r8d, -3
00264C08  jne      0x264c0f  ; -> 00264C0F
00264C0A  movsx    r8d, word ptr [rbx + 0x7a]
00264C0F  test     r8d, r8d
00264C12  jns      0x264c19  ; -> 00264C19
00264C14  movsx    r8d, word ptr [rbx + 0x52]
00264C19  test     r8d, r8d
00264C1C  mov      edi, r12d
00264C1F  cmovns   edi, r8d
00264C23  cmp      word ptr [rbx], 2
00264C27  jbe      0x264c91  ; -> 00264C91
00264C29  test     ecx, ecx
00264C2B  jne      0x264c32  ; -> 00264C32
00264C2D  mov      ecx, dword ptr [rbx + 0x54]
00264C30  jmp      0x264c38  ; -> 00264C38
00264C32  mov      ecx, dword ptr [rbx + 0x84]
00264C38  call     0x20e600  ; -> 0020E600 fn
00264C3D  test     rax, rax
00264C40  je       0x264c91  ; -> 00264C91
00264C42  mov      edx, eax
00264C44  add      rdx, rbx
00264C47  cmp      edi, dword ptr [rdx]
00264C49  jae      0x264c91  ; -> 00264C91
00264C4B  movsxd   rcx, edi
00264C4E  shl      rcx, 5
00264C52  mov      eax, dword ptr [rcx + rdx + 4]
00264C56  mov      dword ptr [rsi], eax
00264C58  mov      eax, dword ptr [rcx + rdx + 8]
00264C5C  mov      dword ptr [r14], eax
00264C5F  mov      eax, dword ptr [rcx + rdx + 0xc]
00264C63  mov      dword ptr [r15], eax
00264C66  mov      eax, dword ptr [rcx + rdx + 0x10]
00264C6A  mov      dword ptr [rbp], eax
00264C6D  mov      eax, 1
00264C72  mov      rdi, qword ptr [rsp + 0x40]
00264C77  mov      rbx, qword ptr [rsp + 0x48]
00264C7C  mov      rbp, qword ptr [rsp + 0x50]
00264C81  mov      rsi, qword ptr [rsp + 0x58]
00264C86  add      rsp, 0x20
00264C8A  pop      r15
00264C8C  pop      r14
00264C8E  pop      r12
00264C90  ret      
00264C91  mov      eax, r12d
00264C94  jmp      0x264c72  ; -> 00264C72
00264C96  mov      eax, r12d
00264C99  jmp      0x264c77  ; -> 00264C77
```

## 003DF7B0 (89 B, extent 003DF7B0-003DF809)

Entered from (direct sites whose caller this page cites): `003546C0` + 0x1D (jmp; `003546C0` is cited on this page); `00354B00` + 0x1A (jmp; `00354B00` is cited on this page)
Other direct sites: `002628B0` + 0x133 (call)

Host context: "-extended word '[rdx]'), and tail-jumps to '0016D6A0' | Interior anchor '003540C5'; Interior anchor '003540D0'; Interior anchor '003540DE'; Interior anchor '003540EE'; Interior anchor '00354102' | | '003546C0' | 34 B | calls '002640C0(rcx)' and tail-jumps to the function at '003546C0' + 0x1D with 'ecx' = 3 when dword '+0x28' of the result is non-zero, else 2, and 'edx' = 1 | Interior anchor '003546C4'; Interior anchor '003546D0'; Interi" / "ith 'ecx' = 3 when dword '+0x28' of the result is non-zero, else 2, and 'edx' = 1 | Interior anchor '003546C4'; Interior anchor '003546D0'; Interior anchor '003546D3'; Interior anchor '003546DD' | | '00354B00' | 31 B | calls '002640C0(rcx)' and tail-jumps to the function at '00354B00' + 0x1A with 'ecx' = 3 when dword '+0x28' of the result is non-zero, else 2, and 'edx' = 0 | Interior anchor '00354B04'; Interior anchor '00354B0B'; Interi"

```
003DF7B0  sub      rsp, 0x28
003DF7B4  mov      eax, dword ptr [rip + 0x277a55e]  ; -> 02B59D18
003DF7BA  test     edx, edx
003DF7BC  je       0x3df7c3  ; -> 003DF7C3
003DF7BE  btr      eax, ecx
003DF7C1  jmp      0x3df7c6  ; -> 003DF7C6
003DF7C3  bts      eax, ecx
003DF7C6  mov      dword ptr [rip + 0x277a54c], eax  ; -> 02B59D18
003DF7CC  test     eax, eax
003DF7CE  jne      0x3df7d9  ; -> 003DF7D9
003DF7D0  add      rsp, 0x28
003DF7D4  jmp      0x3df810  ; -> 003DF810 fn
003DF7D9  xor      r9d, r9d
003DF7DC  xor      r8d, r8d
003DF7DF  xor      edx, edx
003DF7E1  xor      ecx, ecx
003DF7E3  call     0x29cab0  ; -> 0029CAB0 fn
003DF7E8  xor      eax, eax
003DF7EA  mov      qword ptr [rip + 0x277a50f], rax  ; -> 02B59D00
003DF7F1  mov      qword ptr [rip + 0x277a510], rax  ; -> 02B59D08
003DF7F8  mov      dword ptr [rip + 0x277a512], eax  ; -> 02B59D10
003DF7FE  mov      dword ptr [rip + 0x277a510], eax  ; -> 02B59D14
003DF804  add      rsp, 0x28
003DF808  ret      
```

## 003EB700 (23 B, extent 003EB700-003EB717)

Entered from (direct sites whose caller this page cites): `003412B0` + 0x63 (call; `003412B0` is cited on this page); `00351250` + 0x2C (call; `00351250` is cited on this page)
Other direct sites: `00340890` + 0x2A (call); `00340D00` + 0x4E (call); `00346B80` + 0x4E (call); `003471B0` + 0x4E (call); `003518C0` + 0x4E (call); `003EC720` + 0x1E (call); `003EC770` + 0x1E (call)

Host context: " at '00340810+0x5a' with that 'rdx' and 'a' in 'xmm1' | Interior anchor '00340828'; Interior anchor '0034083E'; Interior anchor '00340843'; Interior anchor '00340850'; Interior anchor '0034086A' | | '003412B0' | 167 B | builds a local float array {'f3', 'f2', 'f1', 1.0 ('01CEBBA8')} from three '00267DB0(r9)' calls ('f1' first) and reads 'v' = '00267E10(r9)'; calls '0016D6A0(v)' and 'h' = the function at '003412B0+0x63' with 'v', then '0" / "= dword '+0x28' of that result, 'edx' = b, 'r8d' = a) | Interior anchor '00351220'; Interior anchor '0035122A'; Interior anchor '00351231'; Interior anchor '0035123B'; Interior anchor '00351248' | | '00351250' | 76 B | reads a float f '00267DB0(r9)' and an int n '00267E10(r9)', calls '0016D6A0(n)' and the function at site '00351250' + 0x2C with n, then tail-jumps to the function at site '00351250' + 0x47 with 'rcx' = that result sign-ex"

```
003EB700  cmp      ecx, 0x1f
003EB703  ja       0x3eb714  ; -> 003EB714
003EB705  movsxd   rax, ecx
003EB708  lea      rcx, [rip + 0x2773311]  ; -> 02B5EA20
003EB70F  mov      rax, qword ptr [rcx + rax*8]
003EB713  ret      
003EB714  xor      eax, eax
003EB716  ret      
```
