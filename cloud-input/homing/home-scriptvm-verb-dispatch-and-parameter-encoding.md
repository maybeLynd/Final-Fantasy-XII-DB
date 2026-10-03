# Homing pack: `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-scriptvm-verb-dispatch-and-parameter-encoding.json`.

Bodies: 8. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0025D460 (20 B, extent 0025D460-0025D474)

Entered from (direct sites whose caller this page cites): `003DBDC0` + 0x3D (call; `003DBDC0` is cited on this page)
Other direct sites: none

Host context: " is 'WorldActorScriptVM_InterpretBytecode' - the actor-side interpreter itself, so its ActorEntity callees ('00268EA0', '003587C0', '00358940', '003DB2A0'/'003DB420'/'003DB550'/'003DB640'/'003DB6E0'/'003DBDC0'/ '003DBF60') are the dispatch's own actor traffic, and the entry's '0032F240' registered-id lookup is ActorEntity-owned and reached the other way from '0026C8C0'. The crossing is the interpreter serving actor scripts; no actor sta"

```
0025D460  xor      eax, eax
0025D462  mov      qword ptr [rcx], rax
0025D465  mov      qword ptr [rcx + 8], rax
0025D469  mov      dword ptr [rcx + 0x10], eax
0025D46C  mov      word ptr [rcx + 0x14], ax
0025D470  mov      byte ptr [rcx + 0x16], al
0025D473  ret      
```

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

## 002D75F0 (117 B, extent 002D75F0-002D7665)

Entered from (direct sites whose caller this page cites): `00511550` + 0x21 (jmp; `00511550` is cited on this page)
Other direct sites: `005115B0` + 0x14 (jmp)

Host context: "decursor' issued **before** 'openmenu' > ('men_z0001' lines 24–29) and 'fsmenu_confirmwinsync' in a later routine. Those are not the null > case: **'fsmenu_openmenu' itself carries the same guard** ('00511550' → '00280120', '*(0209AC30 > + 0xC0) == 0' → skip), and '00280140', the only writer of that slot ('002802A0', '00280429', null at > '0028044C'), is a message handler with no direct caller — so no verb creates the menu object; it > "

```
002D75F0  mov      r8, qword ptr [rip + 0x1dc3639]  ; -> 0209AC30
002D75F7  mov      rax, qword ptr [r8 + 0xd8]
002D75FE  mov      rdx, rax
002D7601  test     rax, rax
002D7604  jne      0x2d760d  ; -> 002D760D
002D7606  mov      rdx, qword ptr [r8 + 0x100]
002D760D  test     rdx, rdx
002D7610  je       0x2d7664  ; -> 002D7664
002D7612  test     rax, rax
002D7615  jne      0x2d7623  ; -> 002D7623
002D7617  mov      rax, qword ptr [r8 + 0x100]
002D761E  test     rax, rax
002D7621  je       0x2d7638  ; -> 002D7638
002D7623  mov      dword ptr [rax + 0xcc], 1
002D762D  mov      qword ptr [rax + 0xc4], 2
002D7638  cmp      ecx, -1
002D763B  jne      0x2d7651  ; -> 002D7651
002D763D  cmp      dword ptr [rdx + 0xc0], 0
002D7644  jne      0x2d7664  ; -> 002D7664
002D7646  mov      dword ptr [rdx + 0xc0], 0xa
002D7650  ret      
002D7651  cmp      dword ptr [rdx + 0xc0], 9
002D7658  jne      0x2d7664  ; -> 002D7664
002D765A  mov      dword ptr [rdx + 0xc0], 1
002D7664  ret      
```

## 0036B060 (29 B, extent 0036B060-0036B07D)

Entered from (direct sites whose caller this page cites): `0037B3D0` + 0xB (call; `0037B3D0` is cited on this page)
Other direct sites: none

Host context: "(../Native-Command-Lifecycle/native-command-lifecycle.md)). > - **'usemoviememory'** — poll '003473C0' returns '0037B380() != 4', where '0037B380' reads byte '02ADD932'. That byte is >   set to 4 by '0037B3D0' after it replaces arena 11's backing store (the 3.75 or 4 MiB choice on >   [where the game's memory comes from](../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md)), >   and by '0037B390'"

```
0036B060  cmp      ecx, 0xe
0036B063  ja       0x36b07a  ; -> 0036B07A
0036B065  movsxd   rax, ecx
0036B068  lea      rcx, [rip + 0x1f6cf61]  ; -> 022D7FD0
0036B06F  imul     rax, rax, 0xa8
0036B076  add      rax, rcx
0036B079  ret      
0036B07A  xor      eax, eax
0036B07C  ret      
```

## 003944D0 (34 B, extent 003944D0-003944F2)

Entered from (direct sites whose caller this page cites): `00511FB0` + 0x4 (call; `00511FB0` is cited on this page)
Other direct sites: none

Host context: "65 include '0x7036''s guarded poll '005113D0')* Family 7's records come in ~~exactly four shapes~~ these four shapes and a fifth, 'poll' only, on 3 records — '0x7036' (guarded '005113D0'), '0x705F' ('00511FB0'), '0x7060' ('00512010') *(corrected 2026-10-02, OPUS: 20 + 22 + 54 + 5 + 3 = 104 under the five command tables read under the accessor frame - begin 'tbl + 8 + 0x20n' ('003DC28E'), poll '+ 0x10' ('003DC25E'), result 'tbl + 0x20(n "

```
003944D0  cmp      byte ptr [rip + 0x1b6673b], 2  ; -> 01EFAC12 [u8 0x06]
003944D7  jne      0x3944ec  ; -> 003944EC
003944D9  mov      rax, qword ptr [rip + 0x2759fe8]  ; -> 02AEE4C8
003944E0  test     byte ptr [rax + 0xc4], 2
003944E7  jne      0x3944ec  ; -> 003944EC
003944E9  xor      eax, eax
003944EB  ret      
003944EC  mov      eax, 1
003944F1  ret      
```

## 003DE700 (16 B, extent 003DE700-003DE710)

Entered from (direct sites whose caller this page cites): `00378230` + 0x152 (call; `00378230` is cited on this page)
Other direct sites: `00379080` + 0x66 (call); `00379110` + 0x2F (call)

Host context: "ge-cited '003A1C50', 'FieldData_CopyIndexedRecordByFormatClass' (003DFD00), '00264B50'); 10 outbound (page-cited '002628B0', '00280140', '00264B50' call WorldAreaField bodies '003DFA50', '003EAA00', '00378230'). Substantive edges include '00280140' calls 'WorldTransition_RequeueCurrentFieldForRestore' (00267C90); '00280140' calls 'WorldPersistence_ResetBanksAndMarkInitializationState' (00268320); '00280140' calls 'WorldTransition_Reques"

```
003DE700  movsx    edx, byte ptr [rip + 0x277ac49]  ; -> 02B59350
003DE707  xor      eax, eax
003DE709  bt       edx, ecx
003DE70C  setb     al
003DE70F  ret      
```

## 005688D0 (104 B, extent 005688D0-00568938)

Entered from (direct sites whose caller this page cites): `005113D0` + 0x14 (call; `005113D0` is cited on this page)
Other direct sites: none

Host context: " is one: 'fsmenu' for the ~~33~~ 42 fullscreen-menu verbs *(corrected 2026-10-02, OPUS: 42 rows carry 'guard = fsmenu', 33 of them with operands; the guard 'call 0x280120' also opens '0x7036''s poll '005113D0')* that   share one null-object test, 'other' for the single family-3 verb with its own. **A guarded verb   that bails does not read its operands** — §12.  - **'pops_int' and 'pops_float' give the operand *types*, not just the coun"

```
005688D0  push     rbx
005688D2  sub      rsp, 0x20
005688D6  mov      rax, qword ptr [rip + 0x1b32353]  ; -> 0209AC30
005688DD  lea      rbx, [rip + 0x2740dfc]  ; -> 02CA96E0
005688E4  mov      rcx, qword ptr [rax + 0x160]
005688EB  mov      rax, qword ptr [rip + 0x295689e]  ; -> 02EBF190
005688F2  movsxd   rdx, dword ptr [rcx + 0xf0]
005688F9  movsxd   rcx, dword ptr [rax + rdx*4 + 0x7370]
00568901  mov      rbx, qword ptr [rbx + rcx*8]
00568905  test     rbx, rbx
00568908  je       0x568928  ; -> 00568928
0056890A  call     0x5683f0  ; -> 005683F0 fn
0056890F  test     byte ptr [rbx + 0x358], 2
00568916  jne      0x568920  ; -> 00568920
00568918  xor      eax, eax
0056891A  add      rsp, 0x20
0056891E  pop      rbx
0056891F  ret      
00568920  add      eax, -2
00568923  cmp      eax, 1
00568926  jbe      0x568918  ; -> 00568918
00568928  call     0x2d6620  ; -> 002D6620 fn
0056892D  mov      eax, 1
00568932  add      rsp, 0x20
00568936  pop      rbx
00568937  ret      
```
