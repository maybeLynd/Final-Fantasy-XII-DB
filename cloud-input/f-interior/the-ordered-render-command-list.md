# F-interior pack: `17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-ordered-render-command-list.json`.

Functions: 12. Each is cited on the page only at its entry and is still in the F frontier.

## 001C3590 (108 B, extent 001C3590-001C35FC)

Page context: "] - [rdx]) >> 4' counts the source's '0x10' records, '001EDF00' initialises the destination and '[[rdi+0x18]]->+0x10' allocates 'count*16' bytes, begin/end/capacity land at '[rdi]'/'+8'/'+0x10', and '001C3590' copies the range with the caller's '+0x60' flag byte  Interior anchor '001C3682' (function '001C3600'). "

```
001C3590  mov      qword ptr [rsp + 0x18], r8
001C3595  mov      qword ptr [rsp + 0x10], rdx
001C359A  push     rbx
001C359B  sub      rsp, 0x30
001C359F  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001C35A8  mov      rbx, rcx
001C35AB  mov      qword ptr [rcx], r9
001C35AE  cmp      rdx, r8
001C35B1  je       0x1c35f3  ; -> 001C35F3
001C35B3  nop      dword ptr [rax]
001C35B7  nop      word ptr [rax + rax]
001C35C0  mov      rcx, qword ptr [rbx]
001C35C3  mov      qword ptr [rsp + 0x40], rcx
001C35C8  mov      qword ptr [rsp + 0x28], rcx
001C35CD  test     rcx, rcx
001C35D0  je       0x1c35e1  ; -> 001C35E1
001C35D2  call     0x1fe6b0  ; -> 001FE6B0 fn
001C35D7  mov      r8, qword ptr [rsp + 0x50]
001C35DC  mov      rdx, qword ptr [rsp + 0x48]
001C35E1  add      rdx, 0x10
001C35E5  mov      qword ptr [rsp + 0x48], rdx
001C35EA  add      qword ptr [rbx], 0x10
001C35EE  cmp      rdx, r8
001C35F1  jne      0x1c35c0  ; -> 001C35C0
001C35F3  mov      rax, rbx
001C35F6  add      rsp, 0x30
001C35FA  pop      rbx
001C35FB  ret      
```

## 001D85A0 (21 B, extent 001D85A0-001D85B5)

Page context: "29CE', '00182A44'), '0018B4E0' ('001829F4') or '00189120' ×2 ('00182A77'/'00182A86') and tail into '0018CC60' ('001829B7'), '001D76A0' ('001829E5'), '0018B030' ('00182A00'), '0018C7D0' ('00182A2A'), '001D85A0' ('00182A50'), or '00186910' followed by a 'byte[rax+8]' gate ('00182A96').  | member | role | interior | | --- | --- | --- | | '0018CC60' (143 B) | the frame-open wrapper — 'qword[rsp+0x20] = -2' scope guard ('0018CC66'), '0085E73"

```
001D85A0  mov      dword ptr [rcx + 0x8c], 0x40c00000
001D85AA  mov      dword ptr [rcx + 0x88], 0x437f0000
001D85B4  ret      
```

## 001E5270 (31 B, extent 001E5270-001E528F)

Page context: "g to the manager only. *Corrected 2026-09-15             (FABLE), same day: an earlier wording said all four "allocate nothing", which is true of             two of them.* **Two allocate nothing** — '001E5270' (31 B; its only callees are             '0018B4E0' and '0018AFF0') appends '[this+0x10]', and '001F89B0' (42 B, same two callees)             appends '[this+0x28]' when non-null. **Two allocate from a POOL rather than 'malloc'** —"

```
001E5270  push     rbx
001E5272  sub      rsp, 0x20
001E5276  mov      rbx, rcx
001E5279  call     0x18b4e0  ; -> 0018B4E0 fn
001E527E  mov      rdx, qword ptr [rbx + 0x10]
001E5282  mov      rcx, rax
001E5285  add      rsp, 0x20
001E5289  pop      rbx
001E528A  jmp      0x18aff0  ; -> 0018AFF0 fn
```

## 001F1B80 (68 B, extent 001F1B80-001F1BC4)

Page context: "' | 'CopyFrontBufferForWaterRefraction' | | *(before post-processing)* | '00182A10' | '0018C7D0' | '001F1DC0' | '009031B0' | 'RenderSSSObj' | | '"post-processing render"' | '00182970' | '0018C610' | '001F1B80' | '009031D0' | 'PostProcessObj' | | '"PS2 DOF"' | '001827E0' | '0018C6B0' | '001F1BD0' | '00903070' | 'Ps2DofObj' | | '"Gaussian Filter"' | '0017FD70' | '0018C330' | '001F1A90' | '00903210' | 'GaussianFilterObj' | | *(flush block)"

```
001F1B80  mov      qword ptr [rsp + 8], rbx
001F1B85  push     rdi
001F1B86  sub      rsp, 0x20
001F1B8A  mov      ebx, edx
001F1B8C  mov      rdi, rcx
001F1B8F  call     0x212cc0  ; -> 00212CC0 fn
001F1B94  lea      rax, [rip + 0x711635]  ; -> 009031D0
001F1B9B  mov      dword ptr [rdi + 0x18], ebx
001F1B9E  mov      qword ptr [rdi], rax
001F1BA1  xor      ecx, ecx
001F1BA3  mov      eax, dword ptr [rip + 0x1d91317]  ; -> 01F82EC0
001F1BA9  inc      eax
001F1BAB  test     ebx, ebx
001F1BAD  mov      rbx, qword ptr [rsp + 0x30]
001F1BB2  cmove    eax, ecx
001F1BB5  mov      dword ptr [rip + 0x1d91305], eax  ; -> 01F82EC0
001F1BBB  mov      rax, rdi
001F1BBE  add      rsp, 0x20
001F1BC2  pop      rdi
001F1BC3  ret      
```

## 001F1C30 (118 B, extent 001F1C30-001F1CA6)

Page context: "| '001823B0' | '0018BE70' | '001F19E0' | '00902FD0' | 'EndSceneObj' | | *(draw tail)* | '0017F6B0' | '0018C450' | '001F1B20' | '00903190' | 'MaskBorderObj' | | scope push | '001EB150' | '0018C160' | '001F1C30' | '009032D0' | 'RazorMarkerPushObj' | | scope pop | '001EB110' | '0018C0D0' | '001F1C00' | '009032F0' | 'RazorMarkerPopObj' |  Reading that table back tells you what the passes are *for*, and the readings are physically coherent i"

```
001F1C30  mov      qword ptr [rsp + 8], rcx
001F1C35  push     rdi
001F1C36  sub      rsp, 0x30
001F1C3A  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001F1C43  mov      qword ptr [rsp + 0x48], rbx
001F1C48  mov      rbx, rdx
001F1C4B  mov      rdi, rcx
001F1C4E  call     0x212cc0  ; -> 00212CC0 fn
001F1C53  nop      
001F1C54  lea      rax, [rip + 0x711675]  ; -> 009032D0
001F1C5B  mov      qword ptr [rdi], rax
001F1C5E  mov      qword ptr [rdi + 0x18], 0
001F1C66  mov      ecx, 0x200
001F1C6B  call     0x210ec0  ; -> 00210EC0 fn
001F1C70  mov      qword ptr [rdi + 0x18], rax
001F1C74  xor      edx, edx
001F1C76  mov      r8d, 0x200
001F1C7C  mov      rcx, rax
001F1C7F  call     0x861ec0  ; -> 00861EC0 fn
001F1C84  mov      r8d, 0x1ff
001F1C8A  mov      rdx, rbx
001F1C8D  mov      rcx, qword ptr [rdi + 0x18]
001F1C91  call     qword ptr [rip + 0x6d12d9]  ; -> 008C2F70 [u64 0x0000000001CCEF16]
001F1C97  nop      
001F1C98  mov      rax, rdi
001F1C9B  mov      rbx, qword ptr [rsp + 0x48]
001F1CA0  add      rsp, 0x30
001F1CA4  pop      rdi
001F1CA5  ret      
```

## 001F2520 (79 B, extent 001F2520-001F256F)

Page context: "1') — 40 route through member-dtor '00212CE0' and   'CharacterOrderedObject' '001F4A40' through '00215310'. The exceptions:   'MapOrderedObject' '001E11D0' calls '00212C50', and 'RazorMarkerPushObj' '001F2520'   first **frees its '[+0x18]' member** ('00809950' with size 1) — the only destructor   owning a heap child. - **Slot 1 — execute.** The base class's slot is '00861EC6' = **'jmp _purecall'** — the slot is   *pure virtual* ('= 0'),"

```
001F2520  mov      qword ptr [rsp + 8], rbx
001F2525  push     rdi
001F2526  sub      rsp, 0x20
001F252A  lea      rax, [rip + 0x710d9f]  ; -> 009032D0
001F2531  mov      ebx, edx
001F2533  mov      qword ptr [rcx], rax
001F2536  mov      rdi, rcx
001F2539  mov      rcx, qword ptr [rcx + 0x18]
001F253D  mov      edx, 1
001F2542  call     0x809950  ; -> 00809950 fn
001F2547  mov      rcx, rdi
001F254A  call     0x212ce0  ; -> 00212CE0 fn
001F254F  test     bl, 1
001F2552  je       0x1f2561  ; -> 001F2561
001F2554  mov      edx, 0x20
001F2559  mov      rcx, rdi
001F255C  call     0x809950  ; -> 00809950 fn
001F2561  mov      rax, rdi
001F2564  mov      rbx, qword ptr [rsp + 0x30]
001F2569  add      rsp, 0x20
001F256D  pop      rdi
001F256E  ret      
```

## 001F29E0 (50 B, extent 001F29E0-001F2A12)

Page context: "0x18) == DAT_01F82EC0);   // mode == active screen index     if (FUN_0018E470(FUN_00193D50()) != 0)         FUN_0018EEE0(FUN_00193D50(), ctx, FUN_00193DA0, 1, isCurrentScreen);     ... } '''  '''c // 001F29E0 - BegineSceneObj::Execute, 50 B - the smallest FUN_00188AC0(FUN_00189120()); FUN_005FEFD0(ctx, *(u32*)(this + 0x18)); '''  Three facts a modder can use fall straight out of these:  1. **'DAT_01DFE0C4' is a master render enable.** C"

```
001F29E0  mov      qword ptr [rsp + 8], rbx
001F29E5  push     rdi
001F29E6  sub      rsp, 0x20
001F29EA  mov      rdi, rdx
001F29ED  mov      rbx, rcx
001F29F0  call     0x189120  ; -> 00189120 fn
001F29F5  mov      rcx, rax
001F29F8  call     0x188ac0  ; -> 00188AC0 fn
001F29FD  mov      edx, dword ptr [rbx + 0x18]
001F2A00  mov      rcx, rdi
001F2A03  mov      rbx, qword ptr [rsp + 0x30]
001F2A08  add      rsp, 0x20
001F2A0C  pop      rdi
001F2A0D  jmp      0x5fefd0  ; -> 005FEFD0 fn
```

## 001F32B0 (46 B, extent 001F32B0-001F32DE)

Page context: "render params '+0x198' | | '001F29E0' | 'BegineSceneObj::Execute' | 50 B | the smallest execute body | | '001F3090' | 'GaussianFilterObj::Execute' | 370 B | gated on '+0x19A', '+0x180', '+0x3E8' | | '001F32B0' | 'MaskBorderObj::Execute' | 46 B | | | '001F3300' | 'PostProcessObj::Execute' | 313 B | compares its mode against the screen index | | '001F3440' | 'Ps2DofObj::Execute' | 154 B | | | '001F34F0' | 'RazorMarkerPushObj::Execute' | 1"

```
001F32B0  mov      qword ptr [rsp + 8], rbx
001F32B5  push     rdi
001F32B6  sub      rsp, 0x20
001F32BA  mov      rdi, rdx
001F32BD  mov      rbx, rcx
001F32C0  call     0x193d50  ; -> 00193D50 fn
001F32C5  mov      r8d, dword ptr [rbx + 0x18]
001F32C9  mov      rcx, rax
001F32CC  mov      rdx, rdi
001F32CF  mov      rbx, qword ptr [rsp + 0x30]
001F32D4  add      rsp, 0x20
001F32D8  pop      rdi
001F32D9  jmp      0x191130  ; -> 00191130 fn
```

## 001F39E0 (30 B, extent 001F39E0-001F39FE)

Page context: "001F3300' | 'PostProcessObj::Execute' | 313 B | compares its mode against the screen index | | '001F3440' | 'Ps2DofObj::Execute' | 154 B | | | '001F34F0' | 'RazorMarkerPushObj::Execute' | 16 B | | | '001F39E0' | 'VideoObj::Execute' | 30 B | | | '001F2880' | order key '0x10' | 6 B | shared by the ordinary passes | | '001F28A0' | order key '0x80' | 6 B | 'VideoObj' | | '0053DD10' | order key '1' | 6 B | folded stub; ledger name is unrelat"

```
001F39E0  push     rbx
001F39E2  sub      rsp, 0x20
001F39E6  mov      rbx, rdx
001F39E9  call     0x1b7f20  ; -> 001B7F20 fn
001F39EE  mov      rcx, rax
001F39F1  mov      rdx, rbx
001F39F4  add      rsp, 0x20
001F39F8  pop      rbx
001F39F9  jmp      0x1b7d50  ; -> 001B7D50 fn
```

## 0022A550 (44 B, extent 0022A550-0022A57C)

Page context: "k.       - **The applier runs only under a gate, and the gate is a conjunction.** '001CC600' (from '0017D6E0')         sets '01F81280' to 1 only when '002F1A20''s flag '022BE7C8' is non-zero **and** '0022A550' is, which         needs the mode byte '02064AD3' to equal 2 and '00358330(1)' to be non-zero. It first copies the old         value to '01F81281', and '001C3C30''s first-time block runs on the '0'→'1' edge only.       - **Residue "

```
0022A550  sub      rsp, 0x28
0022A554  cmp      byte ptr [rip + 0x1e3a578], 2  ; -> 02064AD3
0022A55B  jne      0x22a575  ; -> 0022A575
0022A55D  mov      ecx, 1
0022A562  call     0x358330  ; -> 00358330 fn
0022A567  test     eax, eax
0022A569  je       0x22a575  ; -> 0022A575
0022A56B  mov      eax, 1
0022A570  add      rsp, 0x28
0022A574  ret      
0022A575  xor      eax, eax
0022A577  add      rsp, 0x28
0022A57B  ret      
```

## 002640E0 (30 B, extent 002640E0-002640FE)

Page context: "bodies filed to Movement: '002690D0', '0026C3E0'; MainLoop_Draw ('0022B0B0'), '002690D0', '0026C5D0', PartyControl_ApplyAnalogLocomotionToActor ('00358CB0') (+1 more) reach bodies filed to Movement: '002640E0', '00265200', '00265830', '002681D0' (+10 more) - shared machinery across the layer boundary, no shared ownership. - **Resource - CLIENT and SERVICE (34 edges).** '00193D50', '001A0C50', '001A4BF0', '001A52A0' (+9 more) are called "

```
002640E0  movzx    eax, byte ptr [rcx + 3]
002640E4  and      al, 0xe0
002640E6  cmp      al, 0x60
002640E8  je       0x2640ee  ; -> 002640EE
002640EA  xorps    xmm0, xmm0
002640ED  ret      
002640EE  mov      rax, qword ptr [rcx + 0xb8]
002640F5  movss    xmm0, dword ptr [rax + 0xe0]
002640FD  ret      
```

## 002986E0 (2468 B, extent 002986E0-00299084)

Page context: " the layer boundary, no shared ownership. - **UI - CLIENT and SERVICE (14 edges).** '00186660', '001867B0', '001867C0', '0018CD90' (+7 more) are called by bodies filed to UI: '0018EEE0', '00279E20', '002986E0', '00299090' (+2 more); '001F3300' reaches bodies filed to UI: '0018EEE0' - shared machinery across the layer boundary, no shared ownership. - **WorldAreaField - CLIENT and SERVICE (10 edges).** '00263660', '00265920', '002DEBA0', "

```
002986E0  mov      qword ptr [rsp + 0x18], rbx
002986E5  push     rbp
002986E6  push     rsi
002986E7  push     rdi
002986E8  push     r12
002986EA  push     r13
002986EC  push     r14
002986EE  push     r15
002986F0  lea      rbp, [rsp - 0x27]
002986F5  sub      rsp, 0xf0
002986FC  mov      rax, qword ptr [rip + 0x1cac12d]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00298703  xor      rax, rsp
00298706  mov      qword ptr [rbp + 0x1f], rax
0029870A  mov      rsi, rdx
0029870D  mov      dword ptr [rbp + 0x17], 0x820081
00298714  xor      edx, edx
00298716  mov      dword ptr [rbp + 0x1b], 0x810083
0029871D  mov      rdi, rcx
00298720  test     rcx, rcx
00298723  jne      0x29872a  ; -> 0029872A
00298725  mov      r13d, edx
00298728  jmp      0x298732  ; -> 00298732
0029872A  mov      rax, qword ptr [rcx + 0x60]
0029872E  mov      r13, qword ptr [rax + 8]
00298732  mov      rcx, qword ptr [rcx + 0xc0]
00298739  mov      eax, 0x100
0029873E  mov      r10d, 0x4000
00298744  mov      dword ptr [rbp - 0x79], 0x80808080
0029874B  mov      dword ptr [rbp - 0x75], 0x40
00298752  mov      dword ptr [rbp - 0x71], 0x80c0c0c0
00298759  lea      r8d, [rax - 0x80]
0029875D  mov      dword ptr [rbp - 0x6d], 0x20
00298764  mov      dword ptr [rbp - 0x69], 0x80008080
0029876B  mov      dword ptr [rbp - 0x65], 0x10
00298772  mov      dword ptr [rbp - 0x61], 0x80808080
00298779  mov      dword ptr [rbp - 0x5d], 0x10
00298780  movzx    r12d, word ptr [rcx + 4]
00298785  mov      dword ptr [rsp + 0x20], 0x80808080
0029878D  cmp      word ptr [rsi + 0x5e], r10w
00298792  jae      0x2987af  ; -> 002987AF
00298794  cmp      word ptr [rsi + 0x5c], r10w
00298799  jae      0x2987af  ; -> 002987AF
0029879B  test     dword ptr [rsi], eax
0029879D  je       0x2987af  ; -> 002987AF
0029879F  movzx    eax, word ptr [rcx + 0x14]
002987A3  add      eax, 0x10
002987A6  cmp      eax, r8d
002987A9  cmovg    eax, r8d
002987AD  jmp      0x2987b9  ; -> 002987B9
002987AF  movzx    eax, word ptr [rcx + 0x14]
002987B3  sub      eax, 0x10
002987B6  cmovs    eax, edx
002987B9  mov      word ptr [rcx + 0x14], ax
002987BD  lea      r14, [rbp - 0x79]
002987C1  mov      rax, qword ptr [rdi + 0xc0]
002987C8  lea      r15, [rbp + 0x17]
002987CC  mov      ebx, edx
002987CE  movzx    ecx, byte ptr [rax + 0x14]
002987D2  mov      rax, qword ptr [rdi + 0x60]
002987D6  mov      byte ptr [rsp + 0x23], cl
002987DA  mov      rcx, qword ptr [rax + 0x18]
002987DE  mov      eax, dword ptr [rsp + 0x20]
002987E2  mov      dword ptr [rcx + 0x34], eax
002987E5  mov      dword ptr [rcx + 0x30], eax
002987E8  mov      dword ptr [rcx + 0x2c], eax
002987EB  mov      dword ptr [rcx + 0x28], eax
002987EE  nop      
002987F0  movzx    ecx, word ptr [r15]
002987F4  call     0x2dd7e0  ; -> 002DD7E0 fn
002987F9  inc      ebx
002987FB  mov      dword ptr [r14], eax
002987FE  lea      r15, [r15 + 2]
00298802  lea      r14, [r14 + 8]
00298806  cmp      ebx, 4
00298809  jb       0x2987f0  ; -> 002987F0
0029880B  xor      ecx, ecx
0029880D  mov      dword ptr [rbp + 0x17], 0x7b007a
00298814  mov      r14d, ecx
00298817  mov      dword ptr [rbp + 0x1b], 0x7d007c
0029881E  lea      rbx, [rbp - 0x21]
00298822  lea      r15, [rbp + 0x17]
00298826  movzx    ecx, word ptr [r15]
0029882A  call     0x2dd7e0  ; -> 002DD7E0 fn
0029882F  movzx    ecx, al
00298832  inc      r14d
00298835  mov      dword ptr [rbx - 8], ecx
00298838  lea      rbx, [rbx + 0x10]
0029883C  mov      dword ptr [rsp + 0x20], eax
00298840  lea      r15, [r15 + 2]
00298844  movzx    eax, byte ptr [rsp + 0x21]
00298849  mov      dword ptr [rbx - 0x14], eax
0029884C  movzx    eax, byte ptr [rsp + 0x22]
00298851  mov      dword ptr [rbx - 0x10], eax
00298854  movzx    eax, byte ptr [rsp + 0x23]
00298859  mov      dword ptr [rbx - 0xc], eax
0029885C  cmp      r14d, 4
00298860  jb       0x298826  ; -> 00298826
00298862  mov      eax, 0x80
00298867  mov      dword ptr [rbp + 0x17], 0x7f007e
0029886E  mov      word ptr [rbp + 0x1b], ax
00298872  lea      rbx, [rbp - 0x51]
00298876  xor      eax, eax
00298878  lea      r15, [rbp + 0x17]
0029887C  mov      r14d, eax
0029887F  nop      
00298880  movzx    ecx, word ptr [r15]
00298884  call     0x2dd7e0  ; -> 002DD7E0 fn
00298889  movzx    ecx, al
0029888C  inc      r14d
0029888F  mov      dword ptr [rbx - 8], ecx
00298892  lea      rbx, [rbx + 0x10]
00298896  mov      dword ptr [rsp + 0x20], eax
0029889A  lea      r15, [r15 + 2]
0029889E  movzx    eax, byte ptr [rsp + 0x21]
002988A3  mov      dword ptr [rbx - 0x14], eax
002988A6  movzx    eax, byte ptr [rsp + 0x22]
002988AB  mov      dword ptr [rbx - 0x10], eax
002988AE  movzx    eax, byte ptr [rsp + 0x23]
002988B3  mov      dword ptr [rbx - 0xc], eax
002988B6  cmp      r14d, 3
002988BA  jb       0x298880  ; -> 00298880
002988BC  mov      r14d, dword ptr [rsi + 0x40]
002988C0  mov      r8d, 0x64
002988C6  mov      rax, qword ptr [rdi + 0xc0]
002988CD  test     r14d, r14d
002988D0  mov      r15d, dword ptr [rsi + 0x3c]
002988D4  mov      ebx, 0x4000
002988D9  cmove    r14d, r8d
002988DD  movzx    ecx, word ptr [rax + 4]
002988E1  cmp      cx, bx
002988E4  jb       0x2988ef  ; -> 002988EF
002988E6  movzx    eax, word ptr [rsi + 0x5c]
002988EA  cmp      ax, bx
002988ED  jb       0x298905  ; -> 00298905
002988EF  movzx    eax, word ptr [rsi + 0x5c]
002988F3  cmp      cx, ax
002988F6  je       0x298951  ; -> 00298951
002988F8  test     dword ptr [rsi], 0x8000
002988FE  jne      0x298951  ; -> 00298951
00298900  cmp      ax, bx
00298903  jae      0x298951  ; -> 00298951
00298905  test     dword ptr [rsi], 0x2000
0029890B  je       0x298951  ; -> 00298951
0029890D  movzx    edx, ax
00298910  mov      ecx, 0x14
00298915  call     0x35d330  ; -> 0035D330 fn
0029891A  xor      edx, edx
0029891C  mov      rcx, qword ptr [rax + 0x18]
00298920  call     0x2b58b0  ; -> 002B58B0 fn
00298925  xor      ecx, ecx
00298927  mov      qword ptr [r13 + 0x18], rax
0029892B  call     0x20e620  ; -> 0020E620 fn
00298930  mov      rcx, r13
00298933  mov      dword ptr [r13 + 0x20], eax
00298937  call     0x29fb50  ; -> 0029FB50 fn
0029893C  mov      rcx, qword ptr [rdi + 0xc0]
00298943  mov      r8d, 0x64
00298949  movzx    eax, word ptr [rsi + 0x5c]
0029894D  mov      word ptr [rcx + 4], ax
00298951  cmp      word ptr [rsi + 0x5c], bx
00298955  jae      0x298988  ; -> 00298988
00298957  test     dword ptr [rsi], 0x2000
0029895D  je       0x298988  ; -> 00298988
0029895F  mov      rcx, qword ptr [rdi + 0xc0]
00298966  movzx    eax, byte ptr [rcx + 6]
0029896A  cmp      al, 0x80
0029896C  jae      0x2989b2  ; -> 002989B2
0029896E  add      al, 0x10
00298970  xor      edx, edx
00298972  mov      byte ptr [rcx + 6], al
00298975  mov      rax, qword ptr [rdi + 0xc0]
0029897C  cmp      byte ptr [rax + 6], 0x80
00298980  jbe      0x2989b4  ; -> 002989B4
00298982  mov      byte ptr [rax + 6], 0x80
00298986  jmp      0x2989b4  ; -> 002989B4
00298988  mov      rcx, qword ptr [rdi + 0xc0]
0029898F  movzx    eax, byte ptr [rcx + 6]
00298993  test     al, al
00298995  je       0x2989b2  ; -> 002989B2
00298997  test     dword ptr [rsi], 0x8000
0029899D  jne      0x2989b2  ; -> 002989B2
0029899F  movzx    eax, al
002989A2  mov      edx, 0
002989A7  sub      eax, 0x10
002989AA  cmovs    eax, edx
002989AD  mov      byte ptr [rcx + 6], al
002989B0  jmp      0x2989b4  ; -> 002989B4
002989B2  xor      edx, edx
002989B4  test     dword ptr [rsi], 0x1000
002989BA  mov      rax, qword ptr [rdi + 0xc0]
002989C1  je       0x298a17  ; -> 00298A17
002989C3  mov      byte ptr [rax + 0x13], 0x64
002989C7  cmp      dword ptr [rsi + 0x40], 0
002989CB  je       0x2989d2  ; -> 002989D2
002989CD  mov      r15d, r14d
002989D0  jmp      0x2989d8  ; -> 002989D8
002989D2  mov      r14d, r8d
002989D5  mov      r15d, r8d
002989D8  mov      rcx, qword ptr [rdi + 0xc0]
002989DF  movzx    eax, byte ptr [rcx + 7]
002989E3  sub      eax, 0x10
002989E6  cmovs    eax, edx
002989E9  mov      byte ptr [rcx + 7], al
002989EC  mov      rcx, qword ptr [rdi + 0xc0]
002989F3  movzx    eax, word ptr [rcx + 2]
002989F7  test     al, 4
002989F9  jne      0x298aae  ; -> 00298AAE
002989FF  or       ax, 4
00298A03  mov      word ptr [rcx + 2], ax
00298A07  mov      rax, qword ptr [rdi + 0xc0]
00298A0E  mov      word ptr [rax + 8], dx
00298A12  jmp      0x298aae  ; -> 00298AAE
00298A17  mov      ecx, 0xfffb
00298A1C  and      word ptr [rax + 2], cx
00298A20  mov      ecx, 0x400
00298A25  mov      rax, qword ptr [rdi + 0xc0]
00298A2C  mov      word ptr [rax + 8], cx
00298A30  cmp      word ptr [rsi + 0x5c], bx
00298A34  jae      0x298a98  ; -> 00298A98
00298A36  test     dword ptr [rsi], 0x2000
00298A3C  je       0x298a98  ; -> 00298A98
00298A3E  mov      eax, dword ptr [rsi + 0x40]
00298A41  cmp      dword ptr [rsi + 0x3c], eax
00298A44  jl       0x298a7b  ; -> 00298A7B
00298A46  mov      rax, qword ptr [rdi + 0xc0]
00298A4D  mov      r14d, r8d
00298A50  mov      r15d, r8d
00298A53  mov      byte ptr [rax + 0x13], 0x64
00298A57  mov      rcx, qword ptr [rdi + 0xc0]
00298A5E  movzx    eax, byte ptr [rcx + 7]
00298A62  cmp      al, 0x80
00298A64  jae      0x298aae  ; -> 00298AAE
00298A66  movzx    eax, al
00298A69  mov      edx, 0x80
00298A6E  add      eax, 0x10
00298A71  cmp      eax, edx
00298A73  cmovg    eax, edx
00298A76  mov      byte ptr [rcx + 7], al
00298A79  jmp      0x298aae  ; -> 00298AAE
00298A7B  mov      rcx, qword ptr [rdi + 0xc0]
00298A82  movzx    eax, byte ptr [rcx + 7]
00298A86  test     al, al
00298A88  je       0x298aae  ; -> 00298AAE
00298A8A  movzx    eax, al
00298A8D  sub      eax, 0x10
00298A90  cmovs    eax, edx
00298A93  mov      byte ptr [rcx + 7], al
00298A96  jmp      0x298aae  ; -> 00298AAE
00298A98  test     dword ptr [rsi], 0x8000
00298A9E  jne      0x298aab  ; -> 00298AAB
00298AA0  mov      rax, qword ptr [rdi + 0xc0]
00298AA7  mov      byte ptr [rax + 0x13], 0
00298AAB  mov      r15d, edx
00298AAE  call     0x36d830  ; -> 0036D830 fn
00298AB3  mov      ebx, 4
00298AB8  test     eax, eax
00298ABA  jne      0x298ae2  ; -> 00298AE2
00298ABC  mov      rax, qword ptr [rdi + 0xc0]
00298AC3  lea      r9d, [rbx - 3]
00298AC7  mov      edx, ebx
00298AC9  lea      rcx, [rbp - 0x79]
00298ACD  movsx    r8d, word ptr [rax + 8]
00298AD2  call     0x274870  ; -> 00274870 fn
00298AD7  mov      rcx, qword ptr [rdi + 0xc0]
00298ADE  mov      word ptr [rcx + 8], ax
00298AE2  mov      rax, qword ptr [rdi + 0xc0]
00298AE9  lea      rcx, [rbp - 0x79]
00298AED  mov      edx, ebx
00298AEF  movsx    r8d, word ptr [rax + 8]
00298AF4  call     0x271e50  ; -> 00271E50 fn
00298AF9  mov      rbx, qword ptr [rdi + 0xc0]
00298B00  xorps    xmm0, xmm0
00298B03  mov      dword ptr [rbp + 0x17], eax
00298B06  mov      eax, dword ptr [rip + 0x1df6a64]  ; -> 0208F570
00298B0C  cvtsi2ss xmm0, rax
00298B11  mulss    xmm0, dword ptr [rip + 0x1a53137]  ; -> 01CEBC50 [f32 3.141593]
00298B19  divss    xmm0, dword ptr [rip + 0x67d7f3]  ; -> 00916314 [f32 15]
00298B21  call     0x861f0e  ; -> 00861F0E fn
00298B26  movzx    eax, byte ptr [rbx + 7]
00298B2A  mov      edx, 0xff
00298B2F  shl      eax, 6
00298B32  mov      r10d, 0x4000
00298B38  sar      eax, 7
00298B3B  movd     xmm1, eax
00298B3F  movzx    eax, byte ptr [rbp + 0x17]
00298B43  cvtdq2ps xmm1, xmm1
00298B46  mulss    xmm0, xmm1
00298B4A  addss    xmm0, dword ptr [rip + 0x65aeda]  ; -> 008F3A2C [f32 128]
00298B52  cvttss2si rcx, xmm0
00298B57  imul     eax, ecx
00298B5A  shr      eax, 7
00298B5D  cmp      eax, edx
00298B5F  cmovge   eax, edx
00298B62  mov      byte ptr [rbp + 0x17], al
00298B65  movzx    eax, byte ptr [rbp + 0x18]
00298B69  imul     eax, ecx
00298B6C  shr      eax, 7
00298B6F  cmp      eax, edx
00298B71  cmovge   eax, edx
00298B74  mov      byte ptr [rbp + 0x18], al
00298B77  movzx    eax, byte ptr [rbp + 0x19]
00298B7B  imul     eax, ecx
00298B7E  shr      eax, 7
00298B81  cmp      eax, edx
00298B83  cmovge   eax, edx
00298B86  mov      byte ptr [rbp + 0x19], al
00298B89  movzx    eax, byte ptr [rbx + 6]
00298B8D  mov      byte ptr [rbp + 0x1a], al
00298B90  mov      eax, dword ptr [rbp + 0x17]
00298B93  mov      dword ptr [r13 + 0x24], eax
00298B97  test     dword ptr [rsi], 0x8000
00298B9D  je       0x298bb3  ; -> 00298BB3
00298B9F  cmp      r12w, r10w
00298BA3  jae      0x298bb3  ; -> 00298BB3
00298BA5  mov      rax, qword ptr [rdi + 0xc0]
00298BAC  movsx    r8d, byte ptr [rax + 0x13]
00298BB1  jmp      0x298bdb  ; -> 00298BDB
00298BB3  cmp      word ptr [rsi + 0x5c], r10w
00298BB8  jae      0x298bbf  ; -> 00298BBF
00298BBA  cmp      r15d, r14d
00298BBD  jge      0x298bd0  ; -> 00298BD0
00298BBF  mov      rax, qword ptr [rdi + 0xc0]
00298BC6  cmp      byte ptr [rax + 0xa], 1
00298BCA  jne      0x298bd0  ; -> 00298BD0
00298BCC  mov      byte ptr [rax + 0xa], 2
00298BD0  imul     eax, r15d, 0x64
00298BD4  cdq      
00298BD5  idiv     r14d
00298BD8  mov      r8d, eax
00298BDB  mov      rcx, qword ptr [rdi + 0xc0]
00298BE2  mov      eax, 0xfff7
00298BE7  and      word ptr [rcx + 2], ax
00298BEB  test     dword ptr [rsi], 0x1100
00298BF1  je       0x298bff  ; -> 00298BFF
00298BF3  mov      rcx, qword ptr [rdi + 0xc0]
00298BFA  or       word ptr [rcx + 2], 8
00298BFF  test     dword ptr [rsi], 0x8100
00298C05  jne      0x298c20  ; -> 00298C20
00298C07  mov      eax, dword ptr [rsi + 0x40]
00298C0A  cmp      dword ptr [rsi + 0x3c], eax
00298C0D  jge      0x298c20  ; -> 00298C20
00298C0F  mov      rax, qword ptr [rdi + 0xc0]
00298C16  cmp      byte ptr [rax + 0xa], 1
00298C1A  jne      0x298c20  ; -> 00298C20
00298C1C  mov      byte ptr [rax + 0xa], 2
00298C20  mov      rdx, qword ptr [rdi + 0xc0]
00298C27  mov      rax, qword ptr [rdi + 0x60]
00298C2B  movzx    ecx, byte ptr [rdx + 0xa]
00298C2F  mov      r14, qword ptr [rax]
00298C32  test     ecx, ecx
00298C34  je       0x298e8d  ; -> 00298E8D
00298C3A  sub      ecx, 1
00298C3D  je       0x298d67  ; -> 00298D67
00298C43  cmp      ecx, 1
00298C46  jne      0x298d2e  ; -> 00298D2E
00298C4C  add      word ptr [rdx + 0x10], 0x10
00298C51  mov      ecx, 0x100
00298C56  mov      rax, qword ptr [rdi + 0xc0]
00298C5D  cmp      word ptr [rax + 0x10], cx
00298C61  jl       0x298c8a  ; -> 00298C8A
00298C63  mov      word ptr [rax + 0x10], cx
00298C67  mov      rax, qword ptr [rdi + 0xc0]
00298C6E  test     byte ptr [rax + 2], 8
00298C72  je       0x298c7b  ; -> 00298C7B
00298C74  cmp      word ptr [rsi + 0x5c], r10w
00298C79  jb       0x298c8a  ; -> 00298C8A
00298C7B  mov      byte ptr [rax + 0xa], 0
00298C7F  mov      rax, qword ptr [rdi + 0xc0]
00298C86  mov      byte ptr [rax + 0x13], 0
00298C8A  mov      rax, qword ptr [rdi + 0xc0]
00298C91  lea      r8, [rbp + 7]
00298C95  lea      rdx, [rbp - 9]
00298C99  lea      rcx, [rsp + 0x30]
00298C9E  movsx    r9d, word ptr [rax + 0x10]
00298CA3  call     0x2752e0  ; -> 002752E0 fn
00298CA8  mov      rax, qword ptr [rdi + 0xc0]
00298CAF  lea      r8, [rbp - 0x59]
00298CB3  lea      rdx, [rbp - 0x39]
00298CB7  lea      rcx, [rsp + 0x40]
00298CBC  movsx    r9d, word ptr [rax + 0x10]
00298CC1  call     0x2752e0  ; -> 002752E0 fn
00298CC6  movzx    eax, byte ptr [rsp + 0x30]
00298CCB  lea      rdx, [rbp + 0x17]
00298CCF  mov      byte ptr [rbp + 0x17], al
00298CD2  mov      r8d, 1
00298CD8  movzx    eax, byte ptr [rsp + 0x34]
00298CDD  mov      rcx, r14
00298CE0  mov      byte ptr [rbp + 0x18], al
00298CE3  movzx    eax, byte ptr [rsp + 0x38]
00298CE8  mov      byte ptr [rbp + 0x19], al
00298CEB  movzx    eax, byte ptr [rsp + 0x3c]
00298CF0  mov      byte ptr [rbp + 0x1a], al
00298CF3  movzx    eax, byte ptr [rsp + 0x40]
00298CF8  mov      byte ptr [rsp + 0x20], al
00298CFC  movzx    eax, byte ptr [rsp + 0x44]
00298D01  mov      byte ptr [rsp + 0x21], al
00298D05  movzx    eax, byte ptr [rsp + 0x48]
00298D0A  mov      byte ptr [rsp + 0x22], al
00298D0E  movzx    eax, byte ptr [rbp - 0x7d]
00298D12  mov      byte ptr [rsp + 0x23], al
00298D16  call     0x29f480  ; -> 0029F480 fn
00298D1B  mov      r8d, 2
00298D21  lea      rdx, [rsp + 0x20]
00298D26  mov      rcx, r14
00298D29  call     0x29f480  ; -> 0029F480 fn
00298D2E  xor      r15d, r15d
00298D31  test     dword ptr [rsi], 0x1000
00298D37  mov      rax, qword ptr [rdi + 0x60]
00298D3B  mov      dword ptr [rsp + 0x20], 0x80808080
00298D43  mov      rdx, qword ptr [rax + 0x20]
00298D47  jne      0x299022  ; -> 00299022
00298D4D  mov      rcx, qword ptr [rdi + 0xc0]
00298D54  movzx    eax, byte ptr [rcx + 0x12]
00298D58  sub      eax, 0x10
00298D5B  cmovs    eax, r15d
00298D5F  mov      byte ptr [rcx + 0x12], al
00298D62  jmp      0x29903e  ; -> 0029903E
00298D67  or       dword ptr [r14 + 0x20], 0x4000000
00298D6F  mov      rcx, qword ptr [rdi + 0xc0]
00298D76  movzx    eax, byte ptr [rcx + 0xb]
00298D7A  test     al, al
00298D7C  je       0x298d83  ; -> 00298D83
00298D7E  dec      al
00298D80  mov      byte ptr [rcx + 0xb], al
00298D83  mov      rcx, qword ptr [rdi + 0xc0]
00298D8A  test     byte ptr [rcx + 2], 8
00298D8E  jne      0x298d99  ; -> 00298D99
00298D90  movsx    eax, byte ptr [rcx + 0x13]
00298D94  cmp      r8d, eax
00298D97  jge      0x298db8  ; -> 00298DB8
00298D99  cmp      byte ptr [rcx + 0xb], 0
00298D9D  jne      0x298db8  ; -> 00298DB8
00298D9F  mov      byte ptr [rcx + 0xa], 2
00298DA3  xor      ecx, ecx
00298DA5  mov      rax, qword ptr [rdi + 0xc0]
00298DAC  mov      word ptr [rax + 0x10], cx
00298DB0  and      dword ptr [r14 + 0x20], 0xfbffffff
00298DB8  mov      rax, qword ptr [rdi + 0xc0]
00298DBF  xorps    xmm0, xmm0
00298DC2  mov      ecx, dword ptr [rip + 0x1df67a8]  ; -> 0208F570
00298DC8  sub      ecx, dword ptr [rax + 0xc]
00298DCB  mov      eax, ecx
00298DCD  cvtsi2ss xmm0, rax
00298DD2  mulss    xmm0, dword ptr [rip + 0x1a52e76]  ; -> 01CEBC50 [f32 3.141593]
00298DDA  divss    xmm0, dword ptr [rip + 0x67d532]  ; -> 00916314 [f32 15]
00298DE2  call     0x861f0e  ; -> 00861F0E fn
00298DE7  mulss    xmm0, dword ptr [rip + 0x65ac3d]  ; -> 008F3A2C [f32 128]
00298DEF  lea      r8, [rbp - 9]
00298DF3  lea      rdx, [rbp - 0x19]
00298DF7  lea      rcx, [rsp + 0x40]
00298DFC  cvttss2si eax, xmm0
00298E00  movsx    ebx, ax
00298E03  lea      r9d, [rbx + 0x80]
00298E0A  call     0x2752e0  ; -> 002752E0 fn
00298E0F  lea      r9d, [rbx + 0x80]
00298E16  lea      r8, [rbp - 0x39]
00298E1A  lea      rdx, [rbp - 0x49]
00298E1E  lea      rcx, [rsp + 0x30]
00298E23  call     0x2752e0  ; -> 002752E0 fn
00298E28  movzx    eax, byte ptr [rsp + 0x40]
00298E2D  lea      rdx, [rsp + 0x20]
00298E32  mov      byte ptr [rsp + 0x20], al
00298E36  mov      r8d, 1
00298E3C  movzx    eax, byte ptr [rsp + 0x44]
00298E41  mov      rcx, r14
00298E44  mov      byte ptr [rsp + 0x21], al
00298E48  movzx    eax, byte ptr [rsp + 0x48]
00298E4D  mov      byte ptr [rsp + 0x22], al
00298E51  movzx    eax, byte ptr [rbp - 0x7d]
00298E55  mov      byte ptr [rsp + 0x23], al
00298E59  movzx    eax, byte ptr [rsp + 0x30]
00298E5E  mov      byte ptr [rbp + 0x17], al
00298E61  movzx    eax, byte ptr [rsp + 0x34]
00298E66  mov      byte ptr [rbp + 0x18], al
00298E69  movzx    eax, byte ptr [rsp + 0x38]
00298E6E  mov      byte ptr [rbp + 0x19], al
00298E71  movzx    eax, byte ptr [rsp + 0x3c]
00298E76  mov      byte ptr [rbp + 0x1a], al
00298E79  call     0x29f480  ; -> 0029F480 fn
00298E7E  mov      r8d, 2
00298E84  lea      rdx, [rbp + 0x17]
00298E88  jmp      0x298d26  ; -> 00298D26
00298E8D  movzx    eax, byte ptr [rdx + 0x13]
00298E91  xor      r15d, r15d
00298E94  mov      r9d, r15d
00298E97  cmp      al, 0x64
00298E99  jl       0x298ee0  ; -> 00298EE0
00298E9B  cmp      word ptr [rsi + 0x5c], r10w
00298EA0  jae      0x298ee0  ; -> 00298EE0
00298EA2  mov      byte ptr [rdx + 0xa], 1
00298EA6  lea      r9d, [r15 + 1]
00298EAA  mov      eax, dword ptr [rip + 0x1df66c0]  ; -> 0208F570
00298EB0  mov      rcx, qword ptr [rdi + 0xc0]
00298EB7  mov      dword ptr [rcx + 0xc], eax
00298EBA  or       dword ptr [r14 + 0x20], 0x4000000
00298EC2  mov      byte ptr [r14 + 0x21], 0x80
00298EC7  mov      rax, qword ptr [rdi + 0xc0]
00298ECE  mov      byte ptr [rax + 0xb], 8
00298ED2  mov      rax, qword ptr [rdi + 0xc0]
00298ED9  mov      word ptr [rax + 0x16], r15w
00298EDE  jmp      0x298f37  ; -> 00298F37
00298EE0  movsx    eax, al
00298EE3  cmp      r8d, eax
00298EE6  jl       0x298eef  ; -> 00298EEF
00298EE8  mov      word ptr [rdx + 0x16], r15w
00298EED  jmp      0x298f37  ; -> 00298F37
00298EEF  and      dword ptr [r14 + 0x20], 0xfbffffff
00298EF7  mov      rax, qword ptr [rdi + 0xc0]
00298EFE  mov      word ptr [rax + 0x10], r15w
00298F03  mov      rax, qword ptr [rdi + 0xc0]
00298F0A  inc      word ptr [rax + 0x16]
00298F0E  mov      rax, qword ptr [rdi + 0xc0]
00298F15  cmp      word ptr [rax + 0x16], 4
00298F1A  jge      0x298f23  ; -> 00298F23
00298F1C  movsx    r8d, byte ptr [rax + 0x13]
00298F21  jmp      0x298f2c  ; -> 00298F2C
00298F23  mov      ecx, 4
00298F28  mov      word ptr [rax + 0x16], cx
00298F2C  mov      rax, qword ptr [rdi + 0xc0]
00298F33  mov      byte ptr [rax + 0x13], r8b
00298F37  mov      rax, qword ptr [rdi + 0xc0]
00298F3E  shl      r9d, 0x1a
00298F42  mov      byte ptr [rax + 0x13], r8b
00298F46  mov      rax, qword ptr [rdi + 0xc0]
00298F4D  movsx    ecx, byte ptr [rax + 0x13]
00298F51  mov      eax, 0x51eb851f
00298F56  and      dword ptr [r14 + 0x20], 0xfbffffff
00298F5E  or       dword ptr [r14 + 0x20], r9d
00298F62  shl      ecx, 8
00298F65  imul     ecx
00298F67  mov      rcx, r14
00298F6A  mov      ebx, edx
00298F6C  sar      ebx, 5
00298F6F  mov      eax, ebx
00298F71  shr      eax, 0x1f
00298F74  add      ebx, eax
00298F76  mov      rax, qword ptr [rdi + 0xc0]
00298F7D  movsx    edx, byte ptr [rax + 0x13]
00298F81  call     0x225580  ; -> 00225580 fn
00298F86  mov      r9d, ebx
00298F89  mov      byte ptr [r14 + 0x21], 0x80
00298F8E  lea      r8, [rbp - 0x19]
00298F92  lea      rdx, [rbp - 0x29]
00298F96  lea      rcx, [rsp + 0x40]
00298F9B  call     0x2752e0  ; -> 002752E0 fn
00298FA0  mov      r9d, ebx
00298FA3  lea      r8, [rbp - 0x49]
00298FA7  lea      rdx, [rbp - 0x59]
00298FAB  lea      rcx, [rsp + 0x30]
00298FB0  call     0x2752e0  ; -> 002752E0 fn
00298FB5  movzx    eax, byte ptr [rsp + 0x40]
00298FBA  lea      rdx, [rsp + 0x20]
00298FBF  mov      byte ptr [rsp + 0x20], al
00298FC3  mov      r8d, 1
00298FC9  movzx    eax, byte ptr [rsp + 0x44]
00298FCE  mov      rcx, r14
00298FD1  mov      byte ptr [rsp + 0x21], al
00298FD5  movzx    eax, byte ptr [rsp + 0x48]
00298FDA  mov      byte ptr [rsp + 0x22], al
00298FDE  movzx    eax, byte ptr [rbp - 0x7d]
00298FE2  mov      byte ptr [rsp + 0x23], al
00298FE6  movzx    eax, byte ptr [rsp + 0x30]
00298FEB  mov      byte ptr [rbp + 0x17], al
00298FEE  movzx    eax, byte ptr [rsp + 0x34]
00298FF3  mov      byte ptr [rbp + 0x18], al
00298FF6  movzx    eax, byte ptr [rsp + 0x38]
00298FFB  mov      byte ptr [rbp + 0x19], al
00298FFE  movzx    eax, byte ptr [rsp + 0x3c]
00299003  mov      byte ptr [rbp + 0x1a], al
00299006  call     0x29f480  ; -> 0029F480 fn
0029900B  mov      r8d, 2
00299011  lea      rdx, [rbp + 0x17]
00299015  mov      rcx, r14
00299018  call     0x29f480  ; -> 0029F480 fn
0029901D  jmp      0x298d31  ; -> 00298D31
00299022  mov      rax, qword ptr [rdi + 0xc0]
00299029  add      byte ptr [rax + 0x12], 0x10
0029902D  mov      rax, qword ptr [rdi + 0xc0]
00299034  cmp      byte ptr [rax + 0x12], 0x80
00299038  jbe      0x29903e  ; -> 0029903E
0029903A  mov      byte ptr [rax + 0x12], 0x80
0029903E  mov      rax, qword ptr [rdi + 0xc0]
00299045  movzx    ecx, byte ptr [rax + 0x12]
00299049  mov      byte ptr [rsp + 0x23], cl
0029904D  mov      eax, dword ptr [rsp + 0x20]
00299051  mov      dword ptr [rdx + 0x34], eax
00299054  mov      dword ptr [rdx + 0x30], eax
00299057  mov      dword ptr [rdx + 0x2c], eax
0029905A  mov      dword ptr [rdx + 0x28], eax
0029905D  mov      rcx, qword ptr [rbp + 0x1f]
00299061  xor      rcx, rsp
00299064  call     0x808c40  ; -> 00808C40 fn
00299069  mov      rbx, qword ptr [rsp + 0x140]
00299071  add      rsp, 0xf0
00299078  pop      r15
0029907A  pop      r14
0029907C  pop      r13
0029907E  pop      r12
00299080  pop      rdi
00299081  pop      rsi
00299082  pop      rbp
00299083  ret      
```
