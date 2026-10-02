# F-interior pack: `01-Script-VM-Native-Bridge/verbs-that-only-wait-and-verbs-that-do-nothing.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/verbs-that-only-wait-and-verbs-that-do-nothing.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 02d59b826	FABLE: question-marker truth - the DD rule counts a '- [~]' partial box as residue (seven pages rate). OPUS read these before packing.

## 00237D60 (31 B, extent 00237D60-00237D7F)

Page context: " use — an instantaneous action  '005C5230' is the 'poll' of **nine** family-0 verbs. Eight are the page's. The ninth is **'callgameover' ('0x04D8')**, whose 'begin' is '0033F640' — 'xor ecx, ecx; jmp 00237D60', real work — with no 'result'. So a stub poll is not only what a removed feature leaves behind: it is also **how a verb says "I did it, don't wait for me."** 'moveblurfadesync' is the mirror case the page already lists, with stubs"

```
00237D60  sub      rsp, 0x28
00237D64  call     0x35c700  ; -> 0035C700 fn
00237D69  test     eax, eax
00237D6B  jne      0x237d75  ; -> 00237D75
00237D6D  lea      ecx, [rax + 0xb]
00237D70  call     0x35c7a0  ; -> 0035C7A0 fn
00237D75  mov      eax, 1
00237D7A  add      rsp, 0x28
00237D7E  ret      
```

## 00264E10 (32 B, extent 00264E10-00264E30)

Page context: "turn**. It needs only the per-frame question *"is it done yet?"* — which is exactly the 'poll' slot.  **Their polls do real work.** 'movesync''s poll ('00356A90') tests the actor pointer and calls '0x00264E10'; 'gillwinsync''s ('0034D4C0') is the whole idiom in seven instructions:  '''asm 0034D4C0  sub  rsp, 0x28 0034D4C4  call 0x2E2520          ; ask the subsystem whether it has finished 0034D4C9  xor  ecx, ecx 0034D4CB  test eax, eax "

```
00264E10  movzx    eax, byte ptr [rcx + 3]
00264E14  and      al, 0xe0
00264E16  cmp      al, 0x60
00264E18  je       0x264e1d  ; -> 00264E1D
00264E1A  xor      eax, eax
00264E1C  ret      
00264E1D  mov      rax, qword ptr [rcx + 0xb8]
00264E24  mov      rcx, qword ptr [rax + 0xf0]
00264E2B  movzx    eax, byte ptr [rcx + 0x29]
00264E2F  ret      
```

## 0034A940 (169 B, extent 0034A940-0034A9E9)

Page context: "CAL (SWE2-EC7-67).** '003B7180''s measured callees '00263750', '003589B0' and '0026DC60' are shared helpers those layers also call — '00307300'/'003082F0'/'00319F50'/'00325260'/'0031ADB0'/'00226BE0'/'0034A940'/'0037CF00'/'0037D000'/'002E5610'/'003A4290'/'003A56F0'/'00465120'/'00465690'. Those bodies are clients of the helpers, not consumers of this verb family; neither reads the wait-list. Read from the shipping bytes 2026-09-19 (SWE2-E"

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

## 0034E3E0 (40 B, extent 0034E3E0-0034E408)

Page context: "s address for address; CORRECTED: the stubbing is in begin and poll only, and three of the nine still run a result (003447F0 sets the FF12CONFIG useHdd global, an answer stranded on the config page), 0034E3E0 is shared by four verbs not two, 005C5230 is the poll of nine including callgameover which has a real begin, and a 0016D6A0 result marks 'no value to push' in four ordinary verbs   last_pass_kind: falsification   crossref_clean: tr"

```
0034E3E0  sub      rsp, 0x28
0034E3E4  call     0x37cb50  ; -> 0037CB50 fn
0034E3E9  test     eax, eax
0034E3EB  je       0x34e3f4  ; -> 0034E3F4
0034E3ED  xor      eax, eax
0034E3EF  add      rsp, 0x28
0034E3F3  ret      
0034E3F4  mov      ecx, 1
0034E3F9  call     0x314d40  ; -> 00314D40 fn
0034E3FE  mov      eax, 1
0034E403  add      rsp, 0x28
0034E407  ret      
```

## 003B7D30 (70 B, extent 003B7D30-003B7D76)

Page context: "ttings-Config/ff12config-and-debglobal.md)   had already recorded this writer). '0034FB20' ('disposesummon') calls '00314D40(1)' and tail-jumps   '003B6F60'; '00350F30' ('changetonormalparty') calls '003B7D30()' and tail-jumps '003B7180'.   **So a "stub" here means a stubbed 'begin' and 'poll', not a stubbed verb.** §7.  ## 6. Evidence  | claim | evidence | tier | |---|---|---| | 26 poll-only, 3 fully-null, 9 stub-shaped | the family-0 "

```
003B7D30  push     rbx
003B7D32  sub      rsp, 0x20
003B7D36  xor      ebx, ebx
003B7D38  cmp      dword ptr [rip + 0x2b04d62], ebx  ; -> 02EBCAA0
003B7D3E  jle      0x3b7d70  ; -> 003B7D70
003B7D40  mov      qword ptr [rsp + 0x30], rdi
003B7D45  lea      rdi, [rip + 0x2b04d34]  ; -> 02EBCA80
003B7D4C  nop      dword ptr [rax]
003B7D50  mov      rcx, qword ptr [rdi]
003B7D53  mov      edx, 1
003B7D58  call     0x26b500  ; -> 0026B500 fn
003B7D5D  inc      ebx
003B7D5F  lea      rdi, [rdi + 8]
003B7D63  cmp      ebx, dword ptr [rip + 0x2b04d37]  ; -> 02EBCAA0
003B7D69  jl       0x3b7d50  ; -> 003B7D50
003B7D6B  mov      rdi, qword ptr [rsp + 0x30]
003B7D70  add      rsp, 0x20
003B7D74  pop      rbx
003B7D75  ret      
```
