# Homing pack: `16-UI/Widget-Object-Model/CONTRACT-widget-object.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-widget-object.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0027B770 (272 B, extent 0027B770-0027B880)

Entered from (direct sites whose caller this page cites): `0027D700` + 0x31 (jmp; `0027D700` is cited on this page); `0027E4E0` + 0x19 (call; `0027E4E0` is cited on this page); `0027E7B0` + 0x40 (call; `0027E7B0` is cited on this page)
Other direct sites: none

Host context: "ot see. **Every term is confirmed here independently, by asking one question of each candidate: does its address reach a widget constructor's 'proc' slot?**  | term | verdict | |---|---| | **− 5** | '0027D700', '0027D740' (interior read 2026-09-17, SWE2-FRONTIER: '00808F10' first at ['0027D747'](../../_index/ADDRESS-INDEX.md), '00273270' at '0027D819'), '0027E3E0', '0027E4E0', '0027E7B0' reach '00368A50', '002969F0', '00279C48' — **neve" / "rdict | |---|---| | **− 5** | '0027D700', '0027D740' (interior read 2026-09-17, SWE2-FRONTIER: '00808F10' first at ['0027D747'](../../_index/ADDRESS-INDEX.md), '00273270' at '0027D819'), '0027E3E0', '0027E4E0', '0027E7B0' reach '00368A50', '002969F0', '00279C48' — **never a widget constructor**. Not widget procedures | | **+ 14** | all fourteen reach a 'proc' slot: thirteen as 'rdx' into '00244F50', and '002985D0' as 'r8' | | **+ 7** | "

```
0027B770  mov      qword ptr [rsp + 0x10], rbx
0027B775  mov      qword ptr [rsp + 0x18], rbp
0027B77A  push     rdi
0027B77B  sub      rsp, 0x20
0027B77F  movsxd   rbp, r8d
0027B782  mov      edi, edx
0027B784  mov      r8d, dword ptr [rcx + 0x500]
0027B78B  mov      rbx, rcx
0027B78E  cmp      r8d, 1
0027B792  jge      0x27b7a6  ; -> 0027B7A6
0027B794  xor      eax, eax
0027B796  mov      rbx, qword ptr [rsp + 0x38]
0027B79B  mov      rbp, qword ptr [rsp + 0x40]
0027B7A0  add      rsp, 0x20
0027B7A4  pop      rdi
0027B7A5  ret      
0027B7A6  xorps    xmm0, xmm0
0027B7A9  comiss   xmm0, dword ptr [rcx + 0x1540]
0027B7B0  jae      0x27b794  ; -> 0027B794
0027B7B2  mov      rcx, qword ptr [rcx + 0x1510]
0027B7B9  movsx    eax, word ptr [rcx + 0xf2]
0027B7C0  movsx    edx, word ptr [rcx + 0xf4]
0027B7C7  add      edx, eax
0027B7C9  movzx    eax, byte ptr [rcx + 0xec]
0027B7D0  imul     edx, eax
0027B7D3  movsx    eax, byte ptr [rcx + 0xee]
0027B7DA  add      edx, eax
0027B7DC  movsx    eax, byte ptr [rcx + 0xed]
0027B7E3  add      edx, eax
0027B7E5  cmp      edx, r8d
0027B7E8  jge      0x27b794  ; -> 0027B794
0027B7EA  movsxd   rax, edx
0027B7ED  test     byte ptr [rbx + rax*8 + 0x514], 2
0027B7F5  jne      0x27b794  ; -> 0027B794
0027B7F7  mov      ecx, dword ptr [rbx + rax*8 + 0x510]
0027B7FE  mov      qword ptr [rsp + 0x30], rsi
0027B803  xor      esi, esi
0027B805  cmp      ecx, edi
0027B807  je       0x27b871  ; -> 0027B871
0027B809  mov      edx, edi
0027B80B  call     0x27b3b0  ; -> 0027B3B0 fn
0027B810  test     ebp, ebp
0027B812  js       0x27b835  ; -> 0027B835
0027B814  test     byte ptr [rbx + rbp*8 + 0x514], 2
0027B81C  je       0x27b871  ; -> 0027B871
0027B81E  xor      eax, eax
0027B820  mov      rsi, qword ptr [rsp + 0x30]
0027B825  mov      rbx, qword ptr [rsp + 0x38]
0027B82A  mov      rbp, qword ptr [rsp + 0x40]
0027B82F  add      rsp, 0x20
0027B833  pop      rdi
0027B834  ret      
0027B835  movsxd   r8, dword ptr [rbx + 0x500]
0027B83C  mov      edx, esi
0027B83E  mov      rcx, rsi
0027B841  test     r8, r8
0027B844  jle      0x27b81e  ; -> 0027B81E
0027B846  lea      rax, [rbx + 0x510]
0027B84D  nop      dword ptr [rax]
0027B850  cmp      dword ptr [rax], edi
0027B852  je       0x27b864  ; -> 0027B864
0027B854  inc      edx
0027B856  inc      rcx
0027B859  add      rax, 8
0027B85D  cmp      rcx, r8
0027B860  jl       0x27b850  ; -> 0027B850
0027B862  jmp      0x27b81e  ; -> 0027B81E
0027B864  movsxd   rax, edx
0027B867  test     byte ptr [rbx + rax*8 + 0x514], 2
0027B86F  jne      0x27b81e  ; -> 0027B81E
0027B871  comiss   xmm0, dword ptr [rbx + 0x1540]
0027B878  setbe    sil
0027B87C  mov      eax, esi
0027B87E  jmp      0x27b820  ; -> 0027B820
```

## 00299890 (58 B, extent 00299890-002998CA)

Entered from (direct sites whose caller this page cites): `0029A0A0` + 0x3B1 (call; `0029A0A0` is cited on this page)
Other direct sites: none

Host context: "r ranges pop it - the widget's iterative quicksort over the broadcast order.  Interior anchor '00274B82' (function '002748E0').  '00298130' (276 B) is the quad-list alpha ramp the message-30 handler '0029A0A0' runs on the widget: 'byte[rcx+0xD8] & 0x80' picks the direction - 'word[+0x112]' rises '0x20' a tick toward '0x100' or falls '0x20' toward 0 - and 'r8d = (0x100 - level) >> 1' becomes the scale; three linked vertex runs under '[rc"

```
00299890  movzx    eax, word ptr [rcx + 0xd8]
00299897  test     al, 0x10
00299899  je       0x2998c9  ; -> 002998C9
0029989B  add      word ptr [rcx + 0x110], 0x10
002998A3  mov      edx, 0x100
002998A8  cmp      word ptr [rcx + 0x110], dx
002998AF  jl       0x2998c9  ; -> 002998C9
002998B1  xor      edx, edx
002998B3  mov      word ptr [rcx + 0x110], dx
002998BA  mov      edx, 0xffef
002998BF  and      ax, dx
002998C2  mov      word ptr [rcx + 0xd8], ax
002998C9  ret      
```
