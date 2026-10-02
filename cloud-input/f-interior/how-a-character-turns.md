# F-interior pack: `06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/how-a-character-turns.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 00269C30 (53 B, extent 00269C30-00269C65)

Page context: "+0x2B '''  '+0x2B' and '+0x2C' are written together by **'setaccr'** ('0x0122', one operand: '00352D10' pushes **4** as the mode before popping) and 'setaccr_123' ('0x0123', '(accel, mode)') through '00269C30': '+0x2C = accel × [01DFE0BC]' (the 'FrameLimit' inverse scale), '+0x2B = mode'. **Shipped scripts call 'setaccr' twice in the whole corpus** ('4e-05' and '0.006', both one-operand, so mode 4) against 5 'setvelr', 546 'setreachr', "

```
00269C30  movzx    eax, byte ptr [rcx + 3]
00269C34  and      al, 0xe0
00269C36  cmp      al, 0x60
00269C38  jne      0x269c64  ; -> 00269C64
00269C3A  mov      rcx, qword ptr [rcx + 0xb8]
00269C41  movss    xmm0, dword ptr [rip + 0x1b94473]  ; -> 01DFE0BC [f32 1]
00269C49  mulss    xmm0, xmm1
00269C4D  mov      rax, qword ptr [rcx + 0xf0]
00269C54  movss    dword ptr [rax + 0x2c], xmm0
00269C59  mov      rax, qword ptr [rcx + 0xf0]
00269C60  mov      byte ptr [rax + 0x2b], r8b
00269C64  ret      
```

## 0026AE30 (82 B, extent 0026AE30-0026AE82)

Page context: "he target point** ('002E462C'–'002E46CD'). 'rec->+0x2A' is the target kind, written by the    two target setters: **0** = the position at 'rec->+0x00..+0x08' ('Movement_SetSteeringTargetPosition'    '0026AE30' stores '(x, y, z, 1.0)'), reach = 'rec->+0x20' ('setreachr' '0x0076' → '0026B450');    **1** = an actor ('Movement_SetSteeringTargetActorRef' '0026ADF0': '+0x00' the ordinal, '+0x04'    the manager index, resolved by '003587C0'; a"

```
0026AE30  sub      rsp, 0x18
0026AE34  movzx    eax, byte ptr [rcx + 3]
0026AE38  movss    xmm0, dword ptr [rip + 0x1a80d68]  ; -> 01CEBBA8 [f32 1]
0026AE40  and      al, 0xe0
0026AE42  movss    dword ptr [rsp], xmm1
0026AE47  movss    dword ptr [rsp + 4], xmm2
0026AE4D  movss    dword ptr [rsp + 8], xmm3
0026AE53  movss    dword ptr [rsp + 0xc], xmm0
0026AE59  cmp      al, 0x60
0026AE5B  jne      0x26ae7d  ; -> 0026AE7D
0026AE5D  mov      rcx, qword ptr [rcx + 0xb8]
0026AE64  movaps   xmm0, xmmword ptr [rsp]
0026AE68  mov      rax, qword ptr [rcx + 0xf0]
0026AE6F  movups   xmmword ptr [rax], xmm0
0026AE72  mov      rax, qword ptr [rcx + 0xf0]
0026AE79  mov      byte ptr [rax + 0x2a], 0
0026AE7D  add      rsp, 0x18
0026AE81  ret      
```

## 0026B450 (35 B, extent 0026B450-0026B473)

Page context: "n by the    two target setters: **0** = the position at 'rec->+0x00..+0x08' ('Movement_SetSteeringTargetPosition'    '0026AE30' stores '(x, y, z, 1.0)'), reach = 'rec->+0x20' ('setreachr' '0x0076' → '0026B450');    **1** = an actor ('Movement_SetSteeringTargetActorRef' '0026ADF0': '+0x00' the ordinal, '+0x04'    the manager index, resolved by '003587C0'; a **negative** '+0x04' means the party focus actor,    'PartyFocus_GetCurrentPacked"

```
0026B450  test     rcx, rcx
0026B453  je       0x26b472  ; -> 0026B472
0026B455  movzx    eax, byte ptr [rcx + 3]
0026B459  and      al, 0xe0
0026B45B  cmp      al, 0x60
0026B45D  jne      0x26b472  ; -> 0026B472
0026B45F  mov      rax, qword ptr [rcx + 0xb8]
0026B466  mov      rcx, qword ptr [rax + 0xf0]
0026B46D  movss    dword ptr [rcx + 0x20], xmm1
0026B472  ret      
```

## 002EA780 (110 B, extent 002EA780-002EA7EE)

Page context: "12   (FABLE)** — class 3, the steerable actor class of 'BV-4'. §2. - [x] ~~**UQ-101.** **Who sets movement mode 5**, whose arm in the facing integrator '002E5750' waits on an   animation-state test ('002EA780'); none of the 29 call sites of '0026C120' passes a constant 5.~~   **Answered 2026-09-14 (FABLE):** the untimed turn body '002690D0' (the turn verbs 'raturn_25e', 'raturna', 'raturnya', '003578B0', 'unkCall_3092') **stores 5 into "

```
002EA780  push     rbx
002EA782  sub      rsp, 0x20
002EA786  mov      rbx, rcx
002EA789  test     rcx, rcx
002EA78C  je       0x2ea7e6  ; -> 002EA7E6
002EA78E  mov      rax, qword ptr [rcx + 0xc0]
002EA795  test     rax, rax
002EA798  je       0x2ea7e6  ; -> 002EA7E6
002EA79A  cmp      dword ptr [rax], -1
002EA79D  je       0x2ea7e6  ; -> 002EA7E6
002EA79F  movzx    ecx, word ptr [rax]
002EA7A2  cmp      cx, -1
002EA7A6  je       0x2ea7e6  ; -> 002EA7E6
002EA7A8  movsx    rax, cx
002EA7AC  imul     rcx, rax, 0x740
002EA7B3  add      rcx, qword ptr [rip + 0x1fdc76e]  ; -> 022C6F28
002EA7BA  je       0x2ea7e6  ; -> 002EA7E6
002EA7BC  cmp      dword ptr [rcx + 0x284], 0
002EA7C3  je       0x2ea7e6  ; -> 002EA7E6
002EA7C5  call     0x3e6af0  ; -> 003E6AF0 fn
002EA7CA  test     eax, eax
002EA7CC  je       0x2ea7e6  ; -> 002EA7E6
002EA7CE  mov      rcx, rbx
002EA7D1  call     0x2ea910  ; -> 002EA910 fn
002EA7D6  xor      ecx, ecx
002EA7D8  cmp      eax, 1
002EA7DB  sete     cl
002EA7DE  mov      eax, ecx
002EA7E0  add      rsp, 0x20
002EA7E4  pop      rbx
002EA7E5  ret      
002EA7E6  xor      eax, eax
002EA7E8  add      rsp, 0x20
002EA7EC  pop      rbx
002EA7ED  ret      
```
