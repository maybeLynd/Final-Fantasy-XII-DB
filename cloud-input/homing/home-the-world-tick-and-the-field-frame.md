# Homing pack: `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-world-tick-and-the-field-frame.json`.

Bodies: 13. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00197A20 (18 B, extent 00197A20-00197A32)

Entered from (direct sites whose caller this page cites): `001E0EE0` + 0xC (call; `001E0EE0` is cited on this page)
Other direct sites: none

Host context: "860' resolves, 'rbx+0x60' -> '+0x18' -> '+0x18' -> '+0x60' -> '+8' -> '+0x18' chases the chain to 'rsi', 'dword[rsi+0x50] & 0x3FFFC' bounds the loop, then '00285F40'/'0029FA40'/'002F9860'/'001E0E70'/'001E0EE0'/'0020E620' run per slot - the tick's record walk.  Interior anchor '00287E7A' (function '00287E60').  '002880B0' (561 B) is the sibling record walk '002878E0' calls: '002AB860' resolves, the same '+0x60'->'+0x18'->..->'+0x18' chai"

```
00197A20  movzx    eax, byte ptr [rcx + 0x3a]
00197A24  test     al, 2
00197A26  je       0x197a2b  ; -> 00197A2B
00197A28  mov      al, 1
00197A2A  ret      
00197A2B  test     al, 4
00197A2D  jne      0x197a28  ; -> 00197A28
00197A2F  and      al, 1
00197A31  ret      
```

## 001B15A0 (116 B, extent 001B15A0-001B1614)

Entered from (direct sites whose caller this page cites): `00181540` + 0x19 (jmp; `00181540` is cited on this page)
Other direct sites: none

Host context: "forwarder serves), '00275550' zeroes it twice, fields '+0x838'/'+0x83C'/'+0x850' get '0x3E000000'/1.0f/1, '+0x810'/'+0x814' take the ids, '+0x7E8' gets the lazy '0024A5A0' child ('rbp+0x10F50'), and '00181540'/'00181250'/'00181000'/'00271140'/'002711E0' fill it from the word-offset name tables - the pair-record constructor the manager fan-in drives.  Interior anchor '002913B9' (function '00291320').  '00332FA0' (141 B) is the slot teard"

```
001B15A0  push     rbx
001B15A2  sub      rsp, 0x20
001B15A6  mov      rbx, rcx
001B15A9  call     0x1b1440  ; -> 001B1440 fn
001B15AE  mov      rdx, qword ptr [rbx + 0x2218]
001B15B5  lea      r8, [rbx + 0x2208]
001B15BC  mov      rcx, r8
001B15BF  test     rdx, rdx
001B15C2  je       0x1b15da  ; -> 001B15DA
001B15C4  cmp      dword ptr [rdx + 0x20], eax
001B15C7  jb       0x1b15d2  ; -> 001B15D2
001B15C9  mov      rcx, rdx
001B15CC  mov      rdx, qword ptr [rdx + 8]
001B15D0  jmp      0x1b15d5  ; -> 001B15D5
001B15D2  mov      rdx, qword ptr [rdx]
001B15D5  test     rdx, rdx
001B15D8  jne      0x1b15c4  ; -> 001B15C4
001B15DA  cmp      rcx, r8
001B15DD  je       0x1b15e4  ; -> 001B15E4
001B15DF  cmp      eax, dword ptr [rcx + 0x20]
001B15E2  jae      0x1b15e7  ; -> 001B15E7
001B15E4  mov      rcx, r8
001B15E7  lea      rax, [rbx + 0x2208]
001B15EE  cmp      rcx, rax
001B15F1  je       0x1b160c  ; -> 001B160C
001B15F3  mov      rcx, qword ptr [rcx + 0x28]
001B15F7  call     0x6b5c60  ; -> 006B5C60 fn
001B15FC  test     rax, rax
001B15FF  je       0x1b160c  ; -> 001B160C
001B1601  mov      eax, 1
001B1606  add      rsp, 0x20
001B160A  pop      rbx
001B160B  ret      
001B160C  xor      eax, eax
001B160E  add      rsp, 0x20
001B1612  pop      rbx
001B1613  ret      
```

## 00210D20 (107 B, extent 00210D20-00210D8B)

Entered from (direct sites whose caller this page cites): `001DBF00` + 0x32 (call; `001DBF00` is cited on this page)
Other direct sites: none

Host context: "ps 'word[+0x1C] = 1', and ANDs the bit out of '022BE7C0' — the channel release behind the mask query. Interior anchor '002F1756' (the mask clear).  '002DF150' (17 B) forwards '(1, ecx, edx, 0)' into '001DBF00' — the constant-first-arg call the tick path issues. Interior anchor '002DF15C' (the tail jump).  ## SWE2-EC7-29 update (2026-09-18) — '0032E040'/'002A2830' pump gate + ownership forward  '0032E040' (38 B) is the once-per-frame pum"

```
00210D20  mov      qword ptr [rsp + 8], rbx
00210D25  mov      qword ptr [rsp + 0x10], rbp
00210D2A  mov      qword ptr [rsp + 0x18], rsi
00210D2F  push     rdi
00210D30  sub      rsp, 0x20
00210D34  mov      edi, dword ptr [rsp + 0x50]
00210D38  mov      ebx, r9d
00210D3B  mov      esi, r8d
00210D3E  or       ebx, 0x80000000
00210D44  test     edx, edx
00210D46  mov      rbp, rcx
00210D49  mov      rcx, qword ptr [rcx + 8]
00210D4D  mov      edx, esi
00210D4F  cmovne   ebx, r9d
00210D53  and      edi, 0x7f
00210D56  mov      r9d, edi
00210D59  mov      r8d, ebx
00210D5C  call     0x21b790  ; -> 0021B790 fn
00210D61  test     al, al
00210D63  jne      0x210d76  ; -> 00210D76
00210D65  mov      rcx, qword ptr [rbp + 0x10]
00210D69  mov      r9d, edi
00210D6C  mov      r8d, ebx
00210D6F  mov      edx, esi
00210D71  call     0x21a1e0  ; -> 0021A1E0 fn
00210D76  mov      rbx, qword ptr [rsp + 0x30]
00210D7B  mov      rbp, qword ptr [rsp + 0x38]
00210D80  mov      rsi, qword ptr [rsp + 0x40]
00210D85  add      rsp, 0x20
00210D89  pop      rdi
00210D8A  ret      
```

## 00250960 (64 B, extent 00250960-002509A0)

Entered from (direct sites whose caller this page cites): `0025D580` + 0x18 (call; `0025D580` is cited on this page); `0025D9E0` + 0x476 (call; `0025D9E0` is cited on this page)
Other direct sites: none

Host context: "eader is down** (§2.3 step 20) | | 12 | '00238B00(1)' from '002678C0' (← '0025B600', '0036FCC0') | '00238B00(0)' from 'ActorManager_BindLoadedDefinitionPayload' ('0026C965', when its argument is 0), '0025D580', '002628B0' | the '0x3080' mask | **a definition payload load is in flight** — presentation veto | | 13 | '00238B20(1)' from '0025B740' (← 'ActorManager_RunFieldRuntimePass'): the **focus actor** ('PartyFocus_GetCurrentPackedActor" / "ystem_BindBattleUnitsForEligibleRecords' — installs the callback at record '+0x38' | | '0025DF00' | 1,228 B | 'WorldActor_UpdateRuntimeAndScriptExecutionState' — calls the callback at '0025E222' | | '0025D9E0' | 1,297 B | 'ActorManager_RunFieldRuntimePass(slot)' — [the field runtime pass](../../04-Actor-Entity/the-field-runtime-pass.md) | | '003DB1F0' | 132 B | per-record post-pass: '+0x63' countdown, '+0xA0' state walk, '003DB6E0' | | "

```
00250960  mov      qword ptr [rsp + 8], rbx
00250965  push     rdi
00250966  sub      rsp, 0x20
0025096A  mov      ebx, edx
0025096C  mov      edi, ecx
0025096E  xor      edx, edx
00250970  lea      ecx, [rdx + 1]
00250973  call     0x35c880  ; -> 0035C880 fn
00250978  call     0x35c6f0  ; -> 0035C6F0 fn
0025097D  test     al, 2
0025097F  je       0x25098d  ; -> 0025098D
00250981  mov      edx, 4
00250986  xor      ecx, ecx
00250988  call     0x35c880  ; -> 0035C880 fn
0025098D  mov      edx, ebx
0025098F  mov      ecx, edi
00250991  mov      rbx, qword ptr [rsp + 0x30]
00250996  add      rsp, 0x20
0025099A  pop      rdi
0025099B  jmp      0x28e580  ; -> 0028E580 fn
```

## 00265950 (25 B, extent 00265950-00265969)

Entered from (direct sites whose caller this page cites): `0037B4D0` + 0xB81 (call; `0037B4D0` is cited on this page)
Other direct sites: `00342640` + 0x89 (call); `0034A340` + 0x14 (call); `0034E2F0` + 0xC (call)

Host context: "620' ('02097D20' + consts '008F3108'/'009156E0') | single-global reads | | evaluators | '0037C1A0' (resolve '0020E600' ×2 + '00263750'/'0020E620'/'002DEBD0'/'002DEB90' + '0016D6A0' free + '002EA6A0'/'0037B4D0'), '003DE640' ('003ABD00' ×2 over '02B58C58'/'02B59358'), '003DF670' ('003590D0'/'003588B0'/'002EA6A0'/'0029CAB0'), '004742A0' (777 B — 'sqrtf'/'00861F02' ×2 each + '002DDCF0'/'00380800'), '0046AFA0' ('02CA6040'–'4C' const bank) | "

```
00265950  mov      rax, qword ptr [rcx + 0xc0]
00265957  test     rax, rax
0026595A  je       0x265965  ; -> 00265965
0026595C  movss    xmm0, dword ptr [rax + 0x148]
00265964  ret      
00265965  xorps    xmm0, xmm0
00265968  ret      
```

## 00287850 (72 B, extent 00287850-00287898)

Entered from (direct sites whose caller this page cites): `002878E0` + 0x11D (call; `002878E0` is cited on this page)
Other direct sites: none

Host context: "'0022A770'/'0022B8C0'/'0022BC20')  '0027E9E0' (142 B) — reached through '0022A770', '0022B8C0' and '0022BC20' — is the '0209AC18' singleton ensure: while the slot is null it allocates '00244F50(0xC0, 002878E0)', publishes the object, sets '0209AC50' and '0209AC14' to 1, initialises via '00247570(obj, 0)', then registers it into the '0208EA40' bank with '00246AD0(bank, obj)' — stack-cookie protected throughout. Interior anchor '0027EA1F'"

```
00287850  push     rbx
00287852  sub      rsp, 0x20
00287856  xor      ebx, ebx
00287858  test     rcx, rcx
0028785B  jne      0x287861  ; -> 00287861
0028785D  mov      eax, ebx
0028785F  jmp      0x287869  ; -> 00287869
00287861  mov      rax, qword ptr [rcx + 0x60]
00287865  mov      rax, qword ptr [rax + 0x50]
00287869  mov      rax, qword ptr [rax + 0x18]
0028786D  test     rax, rax
00287870  je       0x28787a  ; -> 0028787A
00287872  mov      rax, qword ptr [rax + 0x60]
00287876  mov      rbx, qword ptr [rax + 0x10]
0028787A  mov      ecx, 0xd3e
0028787F  call     0x2f9860  ; -> 002F9860 fn
00287884  xor      ecx, ecx
00287886  mov      qword ptr [rbx + 0x18], rax
0028788A  call     0x20e620  ; -> 0020E620 fn
0028788F  mov      dword ptr [rbx + 0x20], eax
00287892  add      rsp, 0x20
00287896  pop      rbx
00287897  ret      
```

## 002EDD70 (67 B, extent 002EDD70-002EDDB3)

Entered from (direct sites whose caller this page cites): `002E4A40` + 0x104 (call; `002E4A40` is cited on this page); `002E4A40` + 0x11D (call; `002E4A40` is cited on this page); `002E4A40` + 0x139 (call; `002E4A40` is cited on this page); `002E4A40` + 0x150 (call; `002E4A40` is cited on this page)
Other direct sites: none

Host context: "5F1AF' — run near the frame's tail | ['002E1BA0'](../../_index/ADDRESS-INDEX.md) | | '0037CF00' (67 B) | 4-iteration clear pass: '00263750(i)' for i in 0..3, non-null entries get '002E49B0(obj,0)' + '002E4A40(obj)' | ['0037CF12'](../../_index/ADDRESS-INDEX.md) |  '001EBA40' (the '0x2E0' lazy singleton) and the '0024B9B0'/'0036C1D0'/'0036C140' helpers are shared callees with other callers — deliberately not census members.   ### The '002" / "5F1AF' — run near the frame's tail | ['002E1BA0'](../../_index/ADDRESS-INDEX.md) | | '0037CF00' (67 B) | 4-iteration clear pass: '00263750(i)' for i in 0..3, non-null entries get '002E49B0(obj,0)' + '002E4A40(obj)' | ['0037CF12'](../../_index/ADDRESS-INDEX.md) |  '001EBA40' (the '0x2E0' lazy singleton) and the '0024B9B0'/'0036C1D0'/'0036C140' helpers are shared callees with other callers — deliberately not census members.   ### The '002"

```
002EDD70  cmp      cx, -1
002EDD74  je       0x2eddb2  ; -> 002EDDB2
002EDD76  movsx    rax, cx
002EDD7A  imul     rcx, rax, 0x740
002EDD81  add      rcx, qword ptr [rip + 0x1fd91a0]  ; -> 022C6F28
002EDD88  je       0x2eddb2  ; -> 002EDDB2
002EDD8A  cmp      dword ptr [rcx + 0x284], 0
002EDD91  je       0x2eddb2  ; -> 002EDDB2
002EDD93  or       dword ptr [rcx + 0x290], 8
002EDD9A  movss    dword ptr [rcx + 0x380], xmm1
002EDDA2  movss    dword ptr [rcx + 0x384], xmm2
002EDDAA  movss    dword ptr [rcx + 0x388], xmm3
002EDDB2  ret      
```

## 0035A680 (99 B, extent 0035A680-0035A6E3)

Entered from (direct sites whose caller this page cites): `00356970` + 0xD (jmp; `00356970` is cited on this page)
Other direct sites: none

Host context: " '00238B70(1)', which then posts '0x30B' to every active unit (EE-7): 'SpawnGroup_RecordMemberDeathAndHandleCompletion' on a group's completion ('00306FA4'), '00359A30' (← '00359800'), '0035AB20' (← '00356970', a thunk) | '00238B70(0)' from '0035A6F0' (← '002628B0', '003574B0', a thunk) | 'AiOrder_EvaluateAndResolveActionTarget' ('00301511', returns 0 — no gambit evaluation), 'BattleAction_CheckCurrentActionInterruptReason', 'BattleUnit"

```
0035A680  push     rdi
0035A682  sub      rsp, 0x20
0035A686  xor      ecx, ecx
0035A688  call     0x263ff0  ; -> 00263FF0 fn
0035A68D  mov      rdi, rax
0035A690  test     byte ptr [rax + 0x10], 1
0035A694  je       0x35a6dd  ; -> 0035A6DD
0035A696  mov      qword ptr [rsp + 0x30], rbx
0035A69B  movzx    ebx, word ptr [rax + 0x1de]
0035A6A2  mov      qword ptr [rsp + 0x38], rsi
0035A6A7  movzx    esi, word ptr [rax + 0x1d6]
0035A6AE  add      esi, ebx
0035A6B0  cmp      ebx, esi
0035A6B2  jae      0x35a6d3  ; -> 0035A6D3
0035A6B4  mov      edx, ebx
0035A6B6  mov      rcx, rdi
0035A6B9  call     0x358940  ; -> 00358940 fn
0035A6BE  cmp      qword ptr [rax + 0x30], 0
0035A6C3  je       0x35a6cd  ; -> 0035A6CD
0035A6C5  mov      rcx, rax
0035A6C8  call     0x2eb430  ; -> 002EB430 fn
0035A6CD  inc      ebx
0035A6CF  cmp      ebx, esi
0035A6D1  jl       0x35a6b4  ; -> 0035A6B4
0035A6D3  mov      rbx, qword ptr [rsp + 0x30]
0035A6D8  mov      rsi, qword ptr [rsp + 0x38]
0035A6DD  add      rsp, 0x20
0035A6E1  pop      rdi
0035A6E2  ret      
```

## 00379E60 (43 B, extent 00379E60-00379E8B)

Entered from (direct sites whose caller this page cites): `00379E30` + 0x8 (call; `00379E30` is cited on this page); `00379E30` + 0x1F (call; `00379E30` is cited on this page)
Other direct sites: none

Host context: "SWE2-EC7-39 update (2026-09-19) - '003DEE10'  '003DEE10' (432 B) is the '0x38'-stride streaming-slot drain the page names - '003697F0' quadruple frees plus '0032E520'/'0035EA30' pairs and '002DEE90'/'00379E30'/'003DEB30'/'002DF050', over '02B59360'/'02B59C20'. Interior anchor '003DEE9F' (a '002DEE90' call).  ## SWE2-EC7-39 update (2026-09-19) - '00255FF0'  '00255FF0' (422 B) is a world-tick body - '02096508'/'022C6F28', '00263C30'/'0035" / "SWE2-EC7-39 update (2026-09-19) - '003DEE10'  '003DEE10' (432 B) is the '0x38'-stride streaming-slot drain the page names - '003697F0' quadruple frees plus '0032E520'/'0035EA30' pairs and '002DEE90'/'00379E30'/'003DEB30'/'002DF050', over '02B59360'/'02B59C20'. Interior anchor '003DEE9F' (a '002DEE90' call).  ## SWE2-EC7-39 update (2026-09-19) - '00255FF0'  '00255FF0' (422 B) is a world-tick body - '02096508'/'022C6F28', '00263C30'/'0035"

```
00379E60  test     ecx, ecx
00379E62  je       0x379e7e  ; -> 00379E7E
00379E64  mov      eax, ecx
00379E66  lea      r8, [rip + 0x276332b]  ; -> 02ADD198
00379E6D  and      eax, 0xf
00379E70  imul     rdx, rax, 0x70
00379E74  xor      eax, eax
00379E76  cmp      dword ptr [rdx + r8], ecx
00379E7A  sete     al
00379E7D  ret      
00379E7E  xor      eax, eax
00379E80  cmp      qword ptr [rip + 0x27639e9], rax  ; -> 02ADD870
00379E87  setne    al
00379E8A  ret      
```

## 003BBC80 (71 B, extent 003BBC80-003BBCC7)

Entered from (direct sites whose caller this page cites): `00319140` + 0x26 (call; `00319140` is cited on this page)
Other direct sites: none

Host context: " and tail-calls '00291320' - a plain argument-shuffle into the manager's dispatcher.  Interior anchor '00290338' (function '00290320').  '00290B90' (78 B) is the '+0x10F10' list sweep '0027DE30' and '00319140' call: it walks the '0209BE80' manager's node chain ('next' at '+0x868'), and for every node whose 'dword[+0x810]' matches 'ecx' it bumps 'word[+0x850]' from '2' to 'loopindex+3' ('r8d = eax+3', 'eax' counting hits) and latches '1'"

```
003BBC80  mov      rax, qword ptr [rip + 0x2789b49]  ; -> 02B457D0
003BBC87  xor      r8d, r8d
003BBC8A  mov      r9, rcx
003BBC8D  test     rax, rax
003BBC90  jne      0x3bbc93  ; -> 003BBC93
003BBC92  ret      
003BBC93  mov      rcx, rax
003BBC96  mov      edx, 0x40
003BBC9B  nop      dword ptr [rax + rax]
003BBCA0  cmp      qword ptr [rax], r9
003BBCA3  jne      0x3bbcb5  ; -> 003BBCB5
003BBCA5  xor      r8d, r8d
003BBCA8  mov      qword ptr [rcx], r8
003BBCAB  mov      qword ptr [rcx + 8], r8
003BBCAF  mov      r8d, 1
003BBCB5  add      rcx, 0x50
003BBCB9  add      rax, 0x50
003BBCBD  sub      rdx, 1
003BBCC1  jne      0x3bbca0  ; -> 003BBCA0
003BBCC3  mov      eax, r8d
003BBCC6  ret      
```

## 003DCB90 (43 B, extent 003DCB90-003DCBBB)

Entered from (direct sites whose caller this page cites): `00325B30` + 0x0 (jmp; `00325B30` is cited on this page); `00427320` + 0x32F (call; `00427320` is cited on this page)
Other direct sites: `0050CEF0` + 0x13 (call)

Host context: "032ED70'/'0020E600', '02EBF138'), '0030CE10' ('0020E600' ×5 + '00306BD0'), '0030CBE0' (556 B — '0020E600' ×2 + '0031B7E0'/'00322C50'/'0030C890'/'0030A190'/'00328360'/'003226D0'/'003098D0'/'00325B40'/'00325B30'/'0030CE10'/'00306B10', '022BE978'), '0030C890' ('003098D0'/'00325A20'/'0030A190'/'0031A230'), '00309230' ('00D103B0'/'C0'/'D0' table + '02EBF138') | the per-step bodies the orchestrator's 23 steps call — '022C2160'/'022C2168' is t" / "'. Interior anchor '003E808E' (a '003E8990' call).  ## SWE2-EC7-40 update (2026-09-19) - '00426C90'  '00426C90' (392 B) is a field-frame body - '01F44830'/'022C6F28', '004268D0' pair plus '00426FA0'/'00427320'/'003E5CF0'/'0042F310'/'00808C40'. Interior anchor '00426CEE' (a '00426FA0' call).  ## SWE2-EC7-40 update (2026-09-19) - '0051E3A0'  '0051E3A0' (362 B) is a world-tick body - '01CEBBA8'/'01F44830', '003E7450'/'00428940'/'003B6B10'/"

```
003DCB90  test     ecx, ecx
003DCB92  jns      0x3dcb9a  ; -> 003DCB9A
003DCB94  mov      eax, 3
003DCB99  ret      
003DCB9A  je       0x3dcbb8  ; -> 003DCBB8
003DCB9C  mov      eax, ecx
003DCB9E  lea      rdx, [rip + 0x277b3cb]  ; -> 02B57F70
003DCBA5  and      eax, 0xf
003DCBA8  lea      rax, [rax + rax*4]
003DCBAC  cmp      dword ptr [rdx + rax*4 + 8], ecx
003DCBB0  jne      0x3dcbb8  ; -> 003DCBB8
003DCBB2  movzx    eax, byte ptr [rdx + rax*4 + 6]
003DCBB7  ret      
003DCBB8  xor      eax, eax
003DCBBA  ret      
```

## 003ED7F0 (39 B, extent 003ED7F0-003ED817)

Entered from (direct sites whose caller this page cites): `0036F530` + 0x14 (jmp; `0036F530` is cited on this page)
Other direct sites: `0036F410` + 0x17 (jmp)

Host context: " pair '0036C1D0'/'0036C140'), '003D83A0' (2,190 B: '0020E600' ×3 + 'sqrtf' ×2 + '00430B90'/'004309C0'/'0036DD80'), '003D9150' (float step: '00861F1A' + '0025A520'/'0025A500'/'0025A2C0'), '0036F460', '0036F530', '0037A450', '0037D4C0', '0037D970', '003ECAC0', '003ECCA0', '004678E0', '00468520', '003CD820' | the frame's parameter evaluators and camera-bank ('02AED5F0'–'02AED604', '02AEDF10'–'18', '02CA6010'/'20') writers; '003ECCA0'→'003E"

```
003ED7F0  mov      eax, dword ptr [rip + 0x2acdfda]  ; -> 02EBB7D0
003ED7F6  test     eax, eax
003ED7F8  js       0x3ed816  ; -> 003ED816
003ED7FA  movups   xmm0, xmmword ptr [rip + 0x2acdfcf]  ; -> 02EBB7D0
003ED801  or       edx, 0xffffffff
003ED804  test     ecx, ecx
003ED806  movups   xmmword ptr [rip + 0x2acdfd3], xmm0  ; -> 02EBB7E0
003ED80D  cmovne   eax, edx
003ED810  mov      dword ptr [rip + 0x2acdfba], eax  ; -> 02EBB7D0
003ED816  ret      
```

## 00467620 (61 B, extent 00467620-0046765D)

Entered from (direct sites whose caller this page cites): `00473500` + 0xCA (jmp; `00473500` is cited on this page)
Other direct sites: `00473600` + 0x2 (jmp)

Host context: "that writes '022C7FE0'–'022C8028' | | '003Exxxx' perception update | '003E7EC0' ('02B5D080' gate), '003E8020', '003E8440', '003E85B0', '003E8690', '003E8990', '003EB9A0' | '003E8190' ×N + '004735D0'/'00473500' + '0037A2xx'/'0037Bxxx' + '0026FAxx'/'002700F0' shape; '003E8A10'/'40'/'70' are 38-byte two-arm conditional forwarders ('test edx,edx; je' → call A else call B, 'ecx=0') — '003E8A10' selects between the '0037A3B0' pair, '003E8A40'"

```
00467620  test     ecx, ecx
00467622  js       0x46765c  ; -> 0046765C
00467624  cmp      ecx, dword ptr [rip + 0x2a540b6]  ; -> 02EBB6E0
0046762A  jge      0x46765c  ; -> 0046765C
0046762C  movsxd   rax, ecx
0046762F  lea      rcx, [rax + rax*4]
00467633  shl      rcx, 4
00467637  add      rcx, qword ptr [rip + 0x2a540b2]  ; -> 02EBB6F0
0046763E  cmp      qword ptr [rcx + 8], 0
00467643  je       0x46765c  ; -> 0046765C
00467645  and      dword ptr [rcx + 0x4c], 0xfffffffe
00467649  and      edx, 1
0046764C  mov      eax, edx
0046764E  shl      edx, 4
00467651  or       eax, dword ptr [rcx + 0x4c]
00467654  and      eax, 0xffffffef
00467657  or       eax, edx
00467659  mov      dword ptr [rcx + 0x4c], eax
0046765C  ret      
```
