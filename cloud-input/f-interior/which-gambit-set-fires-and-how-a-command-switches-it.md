# F-interior pack: `09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/which-gambit-set-fires-and-how-a-command-switches-it.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

## 00346A10 (65 B, extent 00346A10-00346A51)

Page context: " ('0030126B') and '0030F2D0'         ('0030F331'), the handler the verbs **'resetemergency'** ('00347970'),         **'resetemergency_with_animetionmode'** ('003473E0') and **'resetemergency_one'** ('00346A10') call. Each         picks static set '01EEC3C0' for a party-kind record and '01EEC410' otherwise.       - **B '+0x6F8' — the player-issued command's set.** 'BattleUnit_IssueCommand' installs static set '01EEC2D0'         with the "

```
00346A10  mov      qword ptr [rsp + 8], rbx
00346A15  push     rdi
00346A16  sub      rsp, 0x20
00346A1A  mov      rcx, r9
00346A1D  mov      rbx, rdx
00346A20  call     0x267e10  ; -> 00267E10 fn
00346A25  mov      rcx, rbx
00346A28  mov      edi, eax
00346A2A  call     0x263f10  ; -> 00263F10 fn
00346A2F  mov      rcx, rax
00346A32  mov      rbx, rax
00346A35  call     0x30f2d0  ; -> 0030F2D0 fn
00346A3A  mov      r8d, edi
00346A3D  xor      edx, edx
00346A3F  mov      rcx, rbx
00346A42  mov      rbx, qword ptr [rsp + 0x30]
00346A47  add      rsp, 0x20
00346A4B  pop      rdi
00346A4C  jmp      0x2ecf10  ; -> 002ECF10 fn
```

## 003473E0 (92 B, extent 003473E0-0034743C)

Page context: "eUnit_RecoverFromTerminalStatusSetIfClear' ('0030126B') and '0030F2D0'         ('0030F331'), the handler the verbs **'resetemergency'** ('00347970'),         **'resetemergency_with_animetionmode'** ('003473E0') and **'resetemergency_one'** ('00346A10') call. Each         picks static set '01EEC3C0' for a party-kind record and '01EEC410' otherwise.       - **B '+0x6F8' — the player-issued command's set.** 'BattleUnit_IssueCommand' instal"

```
003473E0  mov      qword ptr [rsp + 8], rbx
003473E5  mov      qword ptr [rsp + 0x10], rsi
003473EA  push     rdi
003473EB  sub      rsp, 0x20
003473EF  mov      rcx, r9
003473F2  call     0x267e10  ; -> 00267E10 fn
003473F7  xor      ebx, ebx
003473F9  test     eax, eax
003473FB  mov      esi, ebx
003473FD  setne    sil
00347401  mov      ecx, ebx
00347403  call     0x263750  ; -> 00263750 fn
00347408  mov      rdi, rax
0034740B  test     rax, rax
0034740E  je       0x347425  ; -> 00347425
00347410  mov      rcx, rax
00347413  call     0x30f2d0  ; -> 0030F2D0 fn
00347418  mov      r8d, esi
0034741B  xor      edx, edx
0034741D  mov      rcx, rdi
00347420  call     0x2ecf10  ; -> 002ECF10 fn
00347425  inc      ebx
00347427  cmp      ebx, 4
0034742A  jl       0x347401  ; -> 00347401
0034742C  mov      rbx, qword ptr [rsp + 0x30]
00347431  mov      rsi, qword ptr [rsp + 0x38]
00347436  add      rsp, 0x20
0034743A  pop      rdi
0034743B  ret      
```

## 00347970 (107 B, extent 00347970-003479DB)

Page context: "onState' ('002FED9E'),         '002FEDC0' ('002FEE05'), 'BattleUnit_RecoverFromTerminalStatusSetIfClear' ('0030126B') and '0030F2D0'         ('0030F331'), the handler the verbs **'resetemergency'** ('00347970'),         **'resetemergency_with_animetionmode'** ('003473E0') and **'resetemergency_one'** ('00346A10') call. Each         picks static set '01EEC3C0' for a party-kind record and '01EEC410' otherwise.       - **B '+0x6F8' — the p"

```
00347970  mov      qword ptr [rsp + 8], rbx
00347975  mov      qword ptr [rsp + 0x10], rsi
0034797A  push     rdi
0034797B  sub      rsp, 0x20
0034797F  xor      edx, edx
00347981  mov      rcx, r9
00347984  mov      rbx, r9
00347987  call     0x267f90  ; -> 00267F90 fn
0034798C  mov      rcx, rbx
0034798F  call     0x267e10  ; -> 00267E10 fn
00347994  xor      ebx, ebx
00347996  test     eax, eax
00347998  mov      esi, ebx
0034799A  setne    sil
0034799E  nop      
003479A0  mov      ecx, ebx
003479A2  call     0x263750  ; -> 00263750 fn
003479A7  mov      rdi, rax
003479AA  test     rax, rax
003479AD  je       0x3479c4  ; -> 003479C4
003479AF  mov      rcx, rax
003479B2  call     0x30f2d0  ; -> 0030F2D0 fn
003479B7  mov      r8d, esi
003479BA  xor      edx, edx
003479BC  mov      rcx, rdi
003479BF  call     0x2ecf10  ; -> 002ECF10 fn
003479C4  inc      ebx
003479C6  cmp      ebx, 4
003479C9  jl       0x3479a0  ; -> 003479A0
003479CB  mov      rbx, qword ptr [rsp + 0x30]
003479D0  mov      rsi, qword ptr [rsp + 0x38]
003479D5  add      rsp, 0x20
003479D9  pop      rdi
003479DA  ret      
```
