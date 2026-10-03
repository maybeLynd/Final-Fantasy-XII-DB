# Homing pack: `00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-time-stop-and-system-stop-registry.json`.

Bodies: 7. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00182610 (40 B, extent 00182610-00182638)

Entered from (direct sites whose caller this page cites): `002F18D0` + 0x74 (jmp; `002F18D0` is cited on this page)
Other direct sites: `002F1950` + 0xA7 (jmp)

Host context: "erior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*  | function | size | what the body does | interior anchors | |---|---|---|---| | '002F18D0' | 121 B | computes n = dword '+4' of 'rcx' plus dword '01DFE0B4' and v = (n minus the integer dword '+0', as floats) / n * 255 ('008C5B40'); when byte '+0x28' has bit '0x4' set it first calls '003587B0(1)' and '00374D40(0, dword +"

```
00182610  push     rbx
00182612  sub      rsp, 0x20
00182616  mov      ebx, ecx
00182618  call     0x189120  ; -> 00189120 fn
0018261D  test     rax, rax
00182620  je       0x182632  ; -> 00182632
00182622  test     ebx, ebx
00182624  setne    bl
00182627  call     0x189120  ; -> 00189120 fn
0018262C  mov      byte ptr [rax + 0xd18], bl
00182632  add      rsp, 0x20
00182636  pop      rbx
00182637  ret      
```

## 001986B0 (18 B, extent 001986B0-001986C2)

Entered from (direct sites whose caller this page cites): `00182CF0` + 0x10 (jmp; `00182CF0` is cited on this page)
Other direct sites: none

Host context: "[probe](../../_experiments/evidence/stop-registry-permission-records/probe.py), [raw records](../../_experiments/evidence/stop-registry-permission-records/records.tsv)): the four callees '00182CD0', '00182CF0', '00182D10' and '002DDC30' were replaced by 'mov eax, 0|1; ret' and change no record byte — only id 0's call path depends on '002DDC30'. The static block at '0022792D' (all-ones, bits 16–17 cleared in both records, tail jump to '0"

```
001986B0  movzx    eax, byte ptr [rcx + 0x3a]
001986B4  test     al, 1
001986B6  jne      0x1986c1  ; -> 001986C1
001986B8  or       al, 1
001986BA  mov      byte ptr [rcx + 0x3b], 1
001986BE  mov      byte ptr [rcx + 0x3a], al
001986C1  ret      
```

## 0029D210 (112 B, extent 0029D210-0029D280)

Entered from (direct sites whose caller this page cites): `002E06B0` + 0x9 (call; `002E06B0` is cited on this page); `002E2400` + 0xD (call; `002E2400` is cited on this page)
Other direct sites: none

Host context: "| 16 | the screen-mask verbs **'maskopen'**, **'maskopenfast'**, **'mesvmaskopen'**, **'mesvmaskopenfast'** ('002E2440') | **'maskclose'**, **'maskclosefast'** ('002E2400'), area unload, '003601D0' ('002E06B0') | | 17 | verbs **'ucon'** / 'ucon_4a5' ('0026C5D0'); '00263660' (← 'ActorManager_RunFieldRuntimePass', '002628B0'); '0026C3E0' | the same functions | | 18 | '0025C830' (← '0025C170') | '0025B500' (← 'WorldActorScriptVM_InterpretB" / "0', '00229510') | the same function | | 16 | the screen-mask verbs **'maskopen'**, **'maskopenfast'**, **'mesvmaskopen'**, **'mesvmaskopenfast'** ('002E2440') | **'maskclose'**, **'maskclosefast'** ('002E2400'), area unload, '003601D0' ('002E06B0') | | 17 | verbs **'ucon'** / 'ucon_4a5' ('0026C5D0'); '00263660' (← 'ActorManager_RunFieldRuntimePass', '002628B0'); '0026C3E0' | the same functions | | 18 | '0025C830' (← '0025C170') | '0025B"

```
0029D210  push     rbx
0029D212  sub      rsp, 0x20
0029D216  mov      ebx, ecx
0029D218  mov      rcx, qword ptr [rip + 0x1dff161]  ; -> 0209C380
0029D21F  and      ebx, 0xffffffef
0029D222  test     rcx, rcx
0029D225  je       0x29d248  ; -> 0029D248
0029D227  cmp      ebx, 1
0029D22A  jne      0x29d230  ; -> 0029D230
0029D22C  xor      edx, edx
0029D22E  jmp      0x29d237  ; -> 0029D237
0029D230  lea      rdx, [rip + 0x6790f9]  ; -> 00916330
0029D237  call     0x247570  ; -> 00247570 fn
0029D23C  mov      rcx, qword ptr [rip + 0x1dff13d]  ; -> 0209C380
0029D243  call     0x244f00  ; -> 00244F00 fn
0029D248  mov      rcx, qword ptr [rip + 0x1dff0c9]  ; -> 0209C318
0029D24F  test     rcx, rcx
0029D252  je       0x29d27a  ; -> 0029D27A
0029D254  cmp      ebx, 1
0029D257  jne      0x29d25d  ; -> 0029D25D
0029D259  xor      edx, edx
0029D25B  jmp      0x29d264  ; -> 0029D264
0029D25D  lea      rdx, [rip + 0x6790cc]  ; -> 00916330
0029D264  call     0x247570  ; -> 00247570 fn
0029D269  mov      rcx, qword ptr [rip + 0x1dff0a8]  ; -> 0209C318
0029D270  add      rsp, 0x20
0029D274  pop      rbx
0029D275  jmp      0x244f00  ; -> 00244F00 fn
0029D27A  add      rsp, 0x20
0029D27E  pop      rbx
0029D27F  ret      
```

## 002FD060 (43 B, extent 002FD060-002FD08B)

Entered from (direct sites whose caller this page cites): `0024BFD0` + 0x67 (call; `0024BFD0` is cited on this page)
Other direct sites: none

Host context: "09-19 (FABLE): what the "rate" triple of the two rate arms below is spent on.** The global the arms ramp, > '020926E8' (target '020926EC', frames '020926E6', step '020926F0'; stepped once a frame by '0024BFD0'), has exactly two > consumers, and both multiply **the alpha of an effect element** by it when the element's container carries bit 2 of > '+0x368' - the bit the 0.0 arm's walk sets. So the triple is the *dimming of effects* under "

```
002FD060  mov      rax, qword ptr [rip + 0x2bc6cf9]  ; -> 02EC3D60
002FD067  test     rax, rax
002FD06A  je       0x2fd08a  ; -> 002FD08A
002FD06C  mov      edx, 0xfffb
002FD071  mov      rcx, qword ptr [rax + 0x10]
002FD075  test     rcx, rcx
002FD078  je       0x2fd081  ; -> 002FD081
002FD07A  and      word ptr [rcx + 0x368], dx
002FD081  mov      rax, qword ptr [rax + 0x28]
002FD085  test     rax, rax
002FD088  jne      0x2fd071  ; -> 002FD071
002FD08A  ret      
```

## 003B1000 (68 B, extent 003B1000-003B1044)

Entered from (direct sites whose caller this page cites): `0024BFD0` + 0x6C (call; `0024BFD0` is cited on this page)
Other direct sites: none

Host context: "09-19 (FABLE): what the "rate" triple of the two rate arms below is spent on.** The global the arms ramp, > '020926E8' (target '020926EC', frames '020926E6', step '020926F0'; stepped once a frame by '0024BFD0'), has exactly two > consumers, and both multiply **the alpha of an effect element** by it when the element's container carries bit 2 of > '+0x368' - the bit the 0.0 arm's walk sets. So the triple is the *dimming of effects* under "

```
003B1000  xor      ecx, ecx
003B1002  lea      rax, [rip + 0x2b0dbff]  ; -> 02EBEC08
003B1009  mov      r9d, 0xfffb
003B100F  nop      
003B1010  cmp      dword ptr [rax - 8], 0
003B1014  je       0x3b1043  ; -> 003B1043
003B1016  mov      rdx, qword ptr [rax]
003B1019  test     rdx, rdx
003B101C  je       0x3b1038  ; -> 003B1038
003B101E  movzx    r8d, word ptr [rdx + 0x368]
003B1026  test     r8b, 4
003B102A  je       0x3b1038  ; -> 003B1038
003B102C  and      r8w, r9w
003B1030  mov      word ptr [rdx + 0x368], r8w
003B1038  inc      ecx
003B103A  add      rax, 0x18
003B103E  cmp      ecx, 0x24
003B1041  jl       0x3b1010  ; -> 003B1010
003B1043  ret      
```

## 003C8B20 (34 B, extent 003C8B20-003C8B42)

Entered from (direct sites whose caller this page cites): `00252E30` + 0x0 (jmp; `00252E30` is cited on this page)
Other direct sites: none

Host context: "y's counted insert.  Interior anchor '0024F261' (function '0024F240').  '003D9E20' (378 B) is the mode toggle '00259990' calls: '00252E50' latches 'al' into '02B4E4A5', zeroes '02B4E4A6'/'02B4E4A4', '00252E30' refreshes, then '02B4E4A0 != eax' selects 'ecx = 1|2' via 'cmovne' and '003588B0'/'002E7F70'/'003D8DA0' run the transition - the registry's armed-mode flip.  Interior anchor '003D9E39' (function '003D9E20').  '0051D2F0' (17 B) is "

```
003C8B20  mov      rax, qword ptr [rip + 0x277ec09]  ; -> 02B47730
003C8B27  test     rax, rax
003C8B2A  je       0x3c8b3f  ; -> 003C8B3F
003C8B2C  test     byte ptr [rax + 0xc0], 4
003C8B33  je       0x3c8b3f  ; -> 003C8B3F
003C8B35  mov      eax, dword ptr [rax + 0xc8]
003C8B3B  test     eax, eax
003C8B3D  jne      0x3c8b41  ; -> 003C8B41
003C8B3F  xor      eax, eax
003C8B41  ret      
```

## 003C9590 (33 B, extent 003C9590-003C95B1)

Entered from (direct sites whose caller this page cites): `00252E50` + 0x0 (jmp; `00252E50` is cited on this page)
Other direct sites: none

Host context: "populate, '0018A330' twice publishes, '003697F0' releases - the registry's counted insert.  Interior anchor '0024F261' (function '0024F240').  '003D9E20' (378 B) is the mode toggle '00259990' calls: '00252E50' latches 'al' into '02B4E4A5', zeroes '02B4E4A6'/'02B4E4A4', '00252E30' refreshes, then '02B4E4A0 != eax' selects 'ecx = 1|2' via 'cmovne' and '003588B0'/'002E7F70'/'003D8DA0' run the transition - the registry's armed-mode flip.  I"

```
003C9590  mov      rcx, qword ptr [rip + 0x277e199]  ; -> 02B47730
003C9597  xor      eax, eax
003C9599  test     rcx, rcx
003C959C  je       0x3c95b0  ; -> 003C95B0
003C959E  test     byte ptr [rcx + 0xc0], 4
003C95A5  je       0x3c95b0  ; -> 003C95B0
003C95A7  cmp      dword ptr [rcx + 0xc8], eax
003C95AD  setne    al
003C95B0  ret      
```
