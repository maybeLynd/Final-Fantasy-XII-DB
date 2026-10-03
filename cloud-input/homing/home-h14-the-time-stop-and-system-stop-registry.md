# Homing pack: `00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-the-time-stop-and-system-stop-registry.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

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

## 003B3080 (27 B, extent 003B3080-003B309B)

Entered from (direct sites whose caller this page cites): `0042D830` + 0x62 (call; `0042D830` is cited on this page)
Other direct sites: none

Host context: "B0' call).  ## SWE2-EC7-35 update (2026-09-19) - '0042C8F0'  '0042C8F0' (753 B) is a stop-registry record op - '022C6F28' registry, seven '0020E600' image-pointer resolves plus '003E5710'/'00477480'/'0042D830'/'00426220'/'00421120'. Interior anchor '0042C961' (a '0020E600' call).  ## SWE2-EC7-37 update (2026-09-19) - '004778D0'  '004778D0' (571 B) is a system-stop registry body - '022C6F28'/'01F44830'/'02CA6CA0', '003E55B0'/'005047C0'/'"

```
003B3080  mov      eax, ecx
003B3082  and      eax, 0x3f
003B3085  imul     rdx, rax, 0x38
003B3089  lea      rax, [rip + 0x2b0a3f0]  ; -> 02EBD480
003B3090  cmp      dword ptr [rdx + rax], ecx
003B3093  jne      0x3b309a  ; -> 003B309A
003B3095  or       byte ptr [rdx + rax + 0x30], 1
003B309A  ret      
```

## 003B3AA0 (109 B, extent 003B3AA0-003B3B0D)

Entered from (direct sites whose caller this page cites): `0042D830` + 0x57 (call; `0042D830` is cited on this page)
Other direct sites: none

Host context: "B0' call).  ## SWE2-EC7-35 update (2026-09-19) - '0042C8F0'  '0042C8F0' (753 B) is a stop-registry record op - '022C6F28' registry, seven '0020E600' image-pointer resolves plus '003E5710'/'00477480'/'0042D830'/'00426220'/'00421120'. Interior anchor '0042C961' (a '0020E600' call).  ## SWE2-EC7-37 update (2026-09-19) - '004778D0'  '004778D0' (571 B) is a system-stop registry body - '022C6F28'/'01F44830'/'02CA6CA0', '003E55B0'/'005047C0'/'"

```
003B3AA0  mov      eax, ecx
003B3AA2  lea      r8, [rip + 0x2b099d7]  ; -> 02EBD480
003B3AA9  and      eax, 0x3f
003B3AAC  imul     rax, rax, 0x38
003B3AB0  cmp      dword ptr [rax + r8], ecx
003B3AB4  jne      0x3b3b0c  ; -> 003B3B0C
003B3AB6  mov      rax, qword ptr [rax + r8 + 0x10]
003B3ABB  test     rax, rax
003B3ABE  je       0x3b3b0c  ; -> 003B3B0C
003B3AC0  mov      ecx, 0x4000
003B3AC5  test     word ptr [rax + 0x368], cx
003B3ACC  je       0x3b3af7  ; -> 003B3AF7
003B3ACE  mov      dword ptr [rax + 0x320], 0x3f800000
003B3AD8  mov      dword ptr [rax + 0x324], 0x3f800000
003B3AE2  mov      dword ptr [rax + 0x328], 0x3f800000
003B3AEC  mov      dword ptr [rax + 0x32c], 0x3f800000
003B3AF6  ret      
003B3AF7  movaps   xmm0, xmmword ptr [rdx]
003B3AFA  movdqa   xmmword ptr [rax + 0x320], xmm0
003B3B02  mov      dword ptr [rax + 0x32c], 0x3f800000
003B3B0C  ret      
```
