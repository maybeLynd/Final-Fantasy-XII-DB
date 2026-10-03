# Homing pack: `17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-fcp-character-parameter-block.json`.

Bodies: 7. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00263640 (31 B, extent 00263640-0026365F)

Entered from (direct sites whose caller this page cites): `002E28E0` + 0x416 (call; `002E28E0` is cited on this page)
Other direct sites: none

Host context: "n 217 files (124 distinct values), 1.85 for 'c1011', 4.4 for 'm1002' | | '0x9000505' | 9 · 5 | '0053AB50' ('0053AFA6') | — | | '0x9000606', '0x9000707', '0x9001F20', '0x9002021' | 9 · 6, 7, 32, 33 | '002E28E0' ('002E2CA1'–'002E2E88'), the actor re-apply function that also re-posts facing | — | | '0x1002143' / '0x1002244', or '0x1002D4F' / '0x1002E50' when 'FieldData_GetActiveFieldRecordBit15' '00377C20' | 1 · 67 / 68, or 79 / 80 | '002E"

```
00263640  movzx    eax, byte ptr [rcx + 3]
00263644  and      al, 0xe0
00263646  cmp      al, 0x60
00263648  jne      0x26365e  ; -> 0026365E
0026364A  mov      rax, qword ptr [rcx + 0xb8]
00263651  movss    xmm1, dword ptr [rax + 0xe4]
00263659  jmp      0x2e86b0  ; -> 002E86B0 fn
0026365E  ret      
```

## 002644E0 (43 B, extent 002644E0-0026450B)

Entered from (direct sites whose caller this page cites): `00349F10` + 0x23 (call; `00349F10` is cited on this page); `00356740` + 0x23 (call; `00356740` is cited on this page); `00356AF0` + 0x30 (call; `00356AF0` is cited on this page); `00356F20` + 0x30 (call; `00356F20` is cited on this page)
Other direct sites: `00340480` + 0x23 (call); `00340BE0` + 0x23 (call); `00342040` + 0x23 (call); `0034FFF0` + 0x23 (call)

Host context: "x', 'r8', 'r9', then tail-jumps to '0026AC70' with 'rdx' and that float in 'xmm1' | Interior anchor '00344078'; Interior anchor '0034408C'; Interior anchor '00344091'; Interior anchor '003440B0' | | '00349F10' | 108 B | calls '00349F10'+0x2E with 'r9' and the float returned by '00349F10'+0x23('rdx') in 'xmm1', calls '0026A1A0(rdx, 0)' twice, then tail-jumps to '00349F10'+0x67 with the incoming 'rcx', 'rdx', 'r8', 'r9' | Interior anchor " / "9F10'+0x67 with the incoming 'rcx', 'rdx', 'r8', 'r9' | Interior anchor '00349F33'; Interior anchor '00349F3E'; Interior anchor '00349F48'; Interior anchor '00349F52'; Interior anchor '00349F77' | | '00356740' | 114 B | calls '00356740'+0x2E with 'r9' and the float returned by '00356740'+0x23('rdx') in 'xmm1', calls '0026A1A0(rdx, 1)' twice, then tail-jumps to '00356740'+0x6D with the incoming 'rcx', 'rdx', 'r8', 'r9' | Interior anchor "

```
002644E0  movzx    eax, byte ptr [rcx + 3]
002644E4  and      al, 0xe0
002644E6  cmp      al, 0x60
002644E8  je       0x2644fb  ; -> 002644FB
002644EA  movss    xmm0, dword ptr [rip + 0x1b99bca]  ; -> 01DFE0BC [f32 1]
002644F2  mulss    xmm0, dword ptr [rip + 0x6b122e]  ; -> 00915728 [f32 0.2094395]
002644FA  ret      
002644FB  mov      rax, qword ptr [rcx + 0xb8]
00264502  movss    xmm0, dword ptr [rax + 0xb0]
0026450A  ret      
```

## 00269E60 (95 B, extent 00269E60-00269EBF)

Entered from (direct sites whose caller this page cites): `002E28E0` + 0x677 (call; `002E28E0` is cited on this page)
Other direct sites: `0034D260` + 0x1F (call)

Host context: "n 217 files (124 distinct values), 1.85 for 'c1011', 4.4 for 'm1002' | | '0x9000505' | 9 · 5 | '0053AB50' ('0053AFA6') | — | | '0x9000606', '0x9000707', '0x9001F20', '0x9002021' | 9 · 6, 7, 32, 33 | '002E28E0' ('002E2CA1'–'002E2E88'), the actor re-apply function that also re-posts facing | — | | '0x1002143' / '0x1002244', or '0x1002D4F' / '0x1002E50' when 'FieldData_GetActiveFieldRecordBit15' '00377C20' | 1 · 67 / 68, or 79 / 80 | '002E"

```
00269E60  movzx    edx, byte ptr [rcx + 3]
00269E64  mov      r8, rcx
00269E67  shr      edx, 5
00269E6A  sub      edx, 1
00269E6D  je       0x269e9f  ; -> 00269E9F
00269E6F  cmp      edx, 2
00269E72  jne      0x269eb7  ; -> 00269EB7
00269E74  mov      rdx, qword ptr [rcx + 0xb8]
00269E7B  xorps    xmm0, xmm0
00269E7E  comiss   xmm0, xmm1
00269E81  movss    dword ptr [rdx + 0xc0], xmm1
00269E89  movss    dword ptr [rdx + 0xc8], xmm1
00269E91  seta     al
00269E94  mov      byte ptr [rdx + 0xdd], al
00269E9A  jmp      0x268380  ; -> 00268380 fn
00269E9F  mov      rcx, qword ptr [rcx + 0xb8]
00269EA6  xorps    xmm0, xmm0
00269EA9  comiss   xmm0, xmm1
00269EAC  movss    dword ptr [rcx + 0x68], xmm1
00269EB1  seta     al
00269EB4  mov      byte ptr [rcx + 0x5c], al
00269EB7  mov      rcx, r8
00269EBA  jmp      0x268380  ; -> 00268380 fn
```

## 0026A370 (43 B, extent 0026A370-0026A39B)

Entered from (direct sites whose caller this page cites): `002E28E0` + 0x6C5 (call; `002E28E0` is cited on this page)
Other direct sites: `0034F280` + 0x6A (jmp)

Host context: "n 217 files (124 distinct values), 1.85 for 'c1011', 4.4 for 'm1002' | | '0x9000505' | 9 · 5 | '0053AB50' ('0053AFA6') | — | | '0x9000606', '0x9000707', '0x9001F20', '0x9002021' | 9 · 6, 7, 32, 33 | '002E28E0' ('002E2CA1'–'002E2E88'), the actor re-apply function that also re-posts facing | — | | '0x1002143' / '0x1002244', or '0x1002D4F' / '0x1002E50' when 'FieldData_GetActiveFieldRecordBit15' '00377C20' | 1 · 67 / 68, or 79 / 80 | '002E"

```
0026A370  movzx    eax, byte ptr [rcx + 3]
0026A374  and      al, 0xe0
0026A376  cmp      al, 0x60
0026A378  jne      0x26a39a  ; -> 0026A39A
0026A37A  mov      rax, qword ptr [rcx + 0xb8]
0026A381  mov      byte ptr [rax + 0x104], dl
0026A387  mov      byte ptr [rax + 0x105], r8b
0026A38E  mov      byte ptr [rax + 0x106], r9b
0026A395  jmp      0x268380  ; -> 00268380 fn
0026A39A  ret      
```

## 0026AA30 (34 B, extent 0026AA30-0026AA52)

Entered from (direct sites whose caller this page cites): `002E28E0` + 0x66C (call; `002E28E0` is cited on this page)
Other direct sites: none

Host context: "n 217 files (124 distinct values), 1.85 for 'c1011', 4.4 for 'm1002' | | '0x9000505' | 9 · 5 | '0053AB50' ('0053AFA6') | — | | '0x9000606', '0x9000707', '0x9001F20', '0x9002021' | 9 · 6, 7, 32, 33 | '002E28E0' ('002E2CA1'–'002E2E88'), the actor re-apply function that also re-posts facing | — | | '0x1002143' / '0x1002244', or '0x1002D4F' / '0x1002E50' when 'FieldData_GetActiveFieldRecordBit15' '00377C20' | 1 · 67 / 68, or 79 / 80 | '002E"

```
0026AA30  movzx    eax, byte ptr [rcx + 3]
0026AA34  and      al, 0xe0
0026AA36  cmp      al, 0x60
0026AA38  jne      0x26aa51  ; -> 0026AA51
0026AA3A  mov      rax, qword ptr [rcx + 0xb8]
0026AA41  movss    dword ptr [rax + 0x98], xmm1
0026AA49  movss    dword ptr [rax + 0x9c], xmm2
0026AA51  ret      
```

## 002E7C70 (111 B, extent 002E7C70-002E7CDF)

Entered from (direct sites whose caller this page cites): `002E28E0` + 0x735 (call; `002E28E0` is cited on this page)
Other direct sites: `0034D720` + 0x1B (jmp)

Host context: "n 217 files (124 distinct values), 1.85 for 'c1011', 4.4 for 'm1002' | | '0x9000505' | 9 · 5 | '0053AB50' ('0053AFA6') | — | | '0x9000606', '0x9000707', '0x9001F20', '0x9002021' | 9 · 6, 7, 32, 33 | '002E28E0' ('002E2CA1'–'002E2E88'), the actor re-apply function that also re-posts facing | — | | '0x1002143' / '0x1002244', or '0x1002D4F' / '0x1002E50' when 'FieldData_GetActiveFieldRecordBit15' '00377C20' | 1 · 67 / 68, or 79 / 80 | '002E"

```
002E7C70  sub      rsp, 0x28
002E7C74  test     rcx, rcx
002E7C77  je       0x2e7cda  ; -> 002E7CDA
002E7C79  mov      rax, qword ptr [rcx + 0xc0]
002E7C80  test     rax, rax
002E7C83  je       0x2e7cda  ; -> 002E7CDA
002E7C85  mov      r8d, dword ptr [rax]
002E7C88  cmp      r8d, -1
002E7C8C  je       0x2e7cda  ; -> 002E7CDA
002E7C8E  movzx    ecx, r8w
002E7C92  cmp      r8w, -1
002E7C97  je       0x2e7cda  ; -> 002E7CDA
002E7C99  mov      qword ptr [rsp + 0x20], rbx
002E7C9E  movsx    rax, cx
002E7CA2  imul     rbx, rax, 0x740
002E7CA9  add      rbx, qword ptr [rip + 0x1fdf278]  ; -> 022C6F28
002E7CB0  je       0x2e7cd5  ; -> 002E7CD5
002E7CB2  cmp      dword ptr [rbx + 0x284], 0
002E7CB9  je       0x2e7cd5  ; -> 002E7CD5
002E7CBB  mov      r9d, edx
002E7CBE  mov      rcx, rbx
002E7CC1  mov      edx, 1
002E7CC6  call     0x3e6c00  ; -> 003E6C00 fn
002E7CCB  or       dword ptr [rbx + 0x290], 0x800
002E7CD5  mov      rbx, qword ptr [rsp + 0x20]
002E7CDA  add      rsp, 0x28
002E7CDE  ret      
```

## 0046C1E0 (91 B, extent 0046C1E0-0046C23B)

Entered from (direct sites whose caller this page cites): `0041FCF0` + 0x367 (call; `0041FCF0` is cited on this page)
Other direct sites: none

Host context: "tching byte selects animation '[record + 0x2FA] + i' of the model container's own '@FMC' motion entry ('+0x2F8' = the model resource id '+0x408', '+0x2FA' = its first '@FMC' entry index, both set by '0041FCF0' at '0041FE66'–'0041FE97') and starts it through '00423B10' ('0042933F'–'0042936E'); no match → the raw event id is the selector into the loaded motion resource at '+0x390' ('00429395'–'004293B5') | '0x7F' or an empty map → no entr"

```
0046C1E0  push     rbx
0046C1E2  sub      rsp, 0x20
0046C1E6  mov      byte ptr [rcx], 0
0046C1E9  mov      rbx, rcx
0046C1EC  cmp      dx, -1
0046C1F0  je       0x46c235  ; -> 0046C235
0046C1F2  xor      ecx, ecx
0046C1F4  movsx    rax, dx
0046C1F8  imul     rax, rax, 0x740
0046C1FF  add      rax, qword ptr [rip + 0x1e5ad22]  ; -> 022C6F28
0046C206  cmp      dword ptr [rax + 0x284], ecx
0046C20C  cmove    rax, rcx
0046C210  test     rax, rax
0046C213  je       0x46c235  ; -> 0046C235
0046C215  mov      byte ptr [rbx], 1
0046C218  mov      ecx, 9
0046C21D  mov      dword ptr [rbx + 8], edx
0046C220  mov      rax, qword ptr [rax + 0x108]
0046C227  mov      qword ptr [rbx + 0x10], rax
0046C22B  call     0x3a6e60  ; -> 003A6E60 fn
0046C230  add      al, 3
0046C232  mov      byte ptr [rbx + 4], al
0046C235  add      rsp, 0x20
0046C239  pop      rbx
0046C23A  ret      
```
