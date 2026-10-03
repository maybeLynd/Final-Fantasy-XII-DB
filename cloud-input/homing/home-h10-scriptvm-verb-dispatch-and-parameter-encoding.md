# Homing pack: `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-scriptvm-verb-dispatch-and-parameter-encoding.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

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
