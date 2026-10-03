# Homing pack: `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-party-read-in-state-machine.json`.

Bodies: 5. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00263640 (31 B, extent 00263640-0026365F)

Entered from (direct sites whose caller this page cites): `002E28E0` + 0x416 (call; `002E28E0` is cited on this page)
Other direct sites: none

Host context: ", '002E4C20' tests '+0x18' bit 1), then writes 3 and applies it in the same arm: '002EBC90', 'ActorHandle_EncodeRegistryEntry', '0031C540', '0026D610', 'ActorHandle_GetPrimaryFormulaResourceByte26', '002E28E0', '002681D0', '002E5C70' (with the three floats at actor '+0xB8'), '002EAC90', '002E49B0', '002E4A40', '002E8450' | 3 ('0037B75D'), falling into 3's arm | | 3 | — (the matched-keys path from 1 re-dispatches here) | 4 ('0037B816') |"

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

## 0026AA30 (34 B, extent 0026AA30-0026AA52)

Entered from (direct sites whose caller this page cites): `002E28E0` + 0x66C (call; `002E28E0` is cited on this page)
Other direct sites: none

Host context: ", '002E4C20' tests '+0x18' bit 1), then writes 3 and applies it in the same arm: '002EBC90', 'ActorHandle_EncodeRegistryEntry', '0031C540', '0026D610', 'ActorHandle_GetPrimaryFormulaResourceByte26', '002E28E0', '002681D0', '002E5C70' (with the three floats at actor '+0xB8'), '002EAC90', '002E49B0', '002E4A40', '002E8450' | 3 ('0037B75D'), falling into 3's arm | | 3 | — (the matched-keys path from 1 re-dispatches here) | 4 ('0037B816') |"

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

Host context: ", '002E4C20' tests '+0x18' bit 1), then writes 3 and applies it in the same arm: '002EBC90', 'ActorHandle_EncodeRegistryEntry', '0031C540', '0026D610', 'ActorHandle_GetPrimaryFormulaResourceByte26', '002E28E0', '002681D0', '002E5C70' (with the three floats at actor '+0xB8'), '002EAC90', '002E49B0', '002E4A40', '002E8450' | 3 ('0037B75D'), falling into 3's arm | | 3 | — (the matched-keys path from 1 re-dispatches here) | 4 ('0037B816') |"

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

## 003B5470 (78 B, extent 003B5470-003B54BE)

Entered from (direct sites whose caller this page cites): `00359B10` + 0x5F (jmp; `00359B10` is cited on this page)
Other direct sites: none

Host context: "riant1', 'Actor_SetDesiredMovementHeading', '002E4A40', '002E8060', '002EB030', **'Actor_SetPresentationVisibilityEnabled'** (shown again), 'BattleUnit_ActivateAppliedDefinitionRuntime', '00263560', '00359B10', '002DEB90' | 23 ('0037C0EB') | | 23 | done: returns 1 ('0037C0EE') | — |  **The entries it loads live in the 128 × 64-byte table at '0215FDA0'** ([how a script names a thing in the world](../how-a-script-names-a-thing-in-the-worl"

```
003B5470  mov      qword ptr [rsp + 8], rbx
003B5475  push     rdi
003B5476  sub      rsp, 0x20
003B547A  cmp      byte ptr [rip + 0x278b091], 0  ; -> 02B40512
003B5481  mov      edi, edx
003B5483  mov      ebx, ecx
003B5485  je       0x3b549a  ; -> 003B549A
003B5487  mov      ecx, 1
003B548C  call     0x2ea030  ; -> 002EA030 fn
003B5491  mov      edx, eax
003B5493  mov      ecx, edi
003B5495  call     0x3b4b60  ; -> 003B4B60 fn
003B549A  cmp      byte ptr [rip + 0x278b069], 0  ; -> 02B4050A
003B54A1  je       0x3b54b3  ; -> 003B54B3
003B54A3  xor      ecx, ecx
003B54A5  call     0x2ea030  ; -> 002EA030 fn
003B54AA  mov      edx, eax
003B54AC  mov      ecx, ebx
003B54AE  call     0x3b4b60  ; -> 003B4B60 fn
003B54B3  mov      rbx, qword ptr [rsp + 0x30]
003B54B8  add      rsp, 0x20
003B54BC  pop      rdi
003B54BD  ret      
```

## 00423280 (76 B, extent 00423280-004232CC)

Entered from (direct sites whose caller this page cites): `002E28E0` + 0x265 (call; `002E28E0` is cited on this page)
Other direct sites: `002E9560` + 0x45 (jmp); `002E95B0` + 0x39 (jmp); `003EB250` + 0x17D (call)

Host context: ", '002E4C20' tests '+0x18' bit 1), then writes 3 and applies it in the same arm: '002EBC90', 'ActorHandle_EncodeRegistryEntry', '0031C540', '0026D610', 'ActorHandle_GetPrimaryFormulaResourceByte26', '002E28E0', '002681D0', '002E5C70' (with the three floats at actor '+0xB8'), '002EAC90', '002E49B0', '002E4A40', '002E8450' | 3 ('0037B75D'), falling into 3's arm | | 3 | — (the matched-keys path from 1 re-dispatches here) | 4 ('0037B816') |"

```
00423280  push     rbx
00423282  sub      rsp, 0x20
00423286  cmp      dword ptr [rcx + 0xc4], -1
0042328D  mov      rbx, rcx
00423290  je       0x4232be  ; -> 004232BE
00423292  mov      ecx, dword ptr [rcx + 0x10]
00423295  call     0x20e600  ; -> 0020E600 fn
0042329A  mov      edx, dword ptr [rbx + 0xc4]
004232A0  mov      rcx, qword ptr [rax + 0xda8]
004232A7  call     0x51b9e0  ; -> 0051B9E0 fn
004232AC  test     rax, rax
004232AF  je       0x4232be  ; -> 004232BE
004232B1  mov      rcx, rax
004232B4  add      rsp, 0x20
004232B8  pop      rbx
004232B9  jmp      0x41c3a0  ; -> 0041C3A0 fn
004232BE  movss    xmm0, dword ptr [rip + 0x4d5aba]  ; -> 008F8D80 [f32 30]
004232C6  add      rsp, 0x20
004232CA  pop      rbx
004232CB  ret      
```
