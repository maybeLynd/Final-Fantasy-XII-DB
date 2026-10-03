# Homing pack: `06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md`

Generated 2026-10-03 13:52 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h13-how-the-engine-chooses-3d-or-flat-movement.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002E4E00 (78 B, extent 002E4E00-002E4E4E)

Entered from (direct sites whose caller this page cites): `00357F00` + 0x115 (call; `00357F00` is cited on this page)
Other direct sites: none

Host context: "t stance.** '002E8540(actor, on)' ('002E854C'–'002E855B'), reached from verbs         '01A7' 'setfightmode' ('0034CB60'), '0483' / '02E0' 'setforcefight' / 'setforcerelax' through         their tick '00357F00', and '02E1' / '0484' 'clearforcerelax' / 'clearforcefight' ('00343290');         read back by '002E9B40' and, ORed with "controller '+0x12' ≥ 0x10", by '002EA2A0' /         '002EABF0'. The shipped scripts call 'setforcefight(-1)' "

```
002E4E00  test     rcx, rcx
002E4E03  je       0x2e4e4a  ; -> 002E4E4A
002E4E05  mov      rax, qword ptr [rcx + 0xc0]
002E4E0C  test     rax, rax
002E4E0F  je       0x2e4e4a  ; -> 002E4E4A
002E4E11  cmp      dword ptr [rax], -1
002E4E14  je       0x2e4e4a  ; -> 002E4E4A
002E4E16  movzx    ecx, word ptr [rax]
002E4E19  cmp      cx, -1
002E4E1D  jne      0x2e4e28  ; -> 002E4E28
002E4E1F  movss    xmm0, dword ptr [rip + 0x1a06e75]  ; -> 01CEBC9C [f32 -1]
002E4E27  ret      
002E4E28  movsx    rax, cx
002E4E2C  imul     rcx, rax, 0x740
002E4E33  add      rcx, qword ptr [rip + 0x1fe20ee]  ; -> 022C6F28
002E4E3A  je       0x2e4e1f  ; -> 002E4E1F
002E4E3C  cmp      dword ptr [rcx + 0x284], 0
002E4E43  je       0x2e4e1f  ; -> 002E4E1F
002E4E45  jmp      0x423380  ; -> 00423380 fn
002E4E4A  xorps    xmm0, xmm0
002E4E4D  ret      
```

## 002E71C0 (208 B, extent 002E71C0-002E7290)

Entered from (direct sites whose caller this page cites): `00357F00` + 0x7A (call; `00357F00` is cited on this page); `00357F00` + 0x104 (call; `00357F00` is cited on this page); `00357F00` + 0x13E (call; `00357F00` is cited on this page)
Other direct sites: none

Host context: "t stance.** '002E8540(actor, on)' ('002E854C'–'002E855B'), reached from verbs         '01A7' 'setfightmode' ('0034CB60'), '0483' / '02E0' 'setforcefight' / 'setforcerelax' through         their tick '00357F00', and '02E1' / '0484' 'clearforcerelax' / 'clearforcefight' ('00343290');         read back by '002E9B40' and, ORed with "controller '+0x12' ≥ 0x10", by '002EA2A0' /         '002EABF0'. The shipped scripts call 'setforcefight(-1)' " / "t stance.** '002E8540(actor, on)' ('002E854C'–'002E855B'), reached from verbs         '01A7' 'setfightmode' ('0034CB60'), '0483' / '02E0' 'setforcefight' / 'setforcerelax' through         their tick '00357F00', and '02E1' / '0484' 'clearforcerelax' / 'clearforcefight' ('00343290');         read back by '002E9B40' and, ORed with "controller '+0x12' ≥ 0x10", by '002EA2A0' /         '002EABF0'. The shipped scripts call 'setforcefight(-1)' "

```
002E71C0  mov      qword ptr [rsp + 8], rbx
002E71C5  mov      qword ptr [rsp + 0x10], rsi
002E71CA  push     rdi
002E71CB  sub      rsp, 0x20
002E71CF  xor      ebx, ebx
002E71D1  mov      rsi, rcx
002E71D4  test     rcx, rcx
002E71D7  je       0x2e7229  ; -> 002E7229
002E71D9  mov      rax, qword ptr [rcx + 0xc0]
002E71E0  test     rax, rax
002E71E3  je       0x2e7229  ; -> 002E7229
002E71E5  cmp      dword ptr [rax], -1
002E71E8  je       0x2e7229  ; -> 002E7229
002E71EA  movzx    ecx, word ptr [rax]
002E71ED  cmp      cx, -1
002E71F1  jne      0x2e71f7  ; -> 002E71F7
002E71F3  mov      edi, ebx
002E71F5  jmp      0x2e722e  ; -> 002E722E
002E71F7  movsx    rax, cx
002E71FB  imul     rcx, rax, 0x740
002E7202  add      rcx, qword ptr [rip + 0x1fdfd1f]  ; -> 022C6F28
002E7209  jne      0x2e720f  ; -> 002E720F
002E720B  mov      edi, ebx
002E720D  jmp      0x2e722e  ; -> 002E722E
002E720F  cmp      dword ptr [rcx + 0x284], ebx
002E7215  jne      0x2e721b  ; -> 002E721B
002E7217  mov      edi, ebx
002E7219  jmp      0x2e722e  ; -> 002E722E
002E721B  mov      edx, 3
002E7220  call     0x41e690  ; -> 0041E690 fn
002E7225  mov      edi, eax
002E7227  jmp      0x2e722e  ; -> 002E722E
002E7229  mov      edi, 1
002E722E  test     rsi, rsi
002E7231  je       0x2e7277  ; -> 002E7277
002E7233  mov      rax, qword ptr [rsi + 0xc0]
002E723A  test     rax, rax
002E723D  je       0x2e7277  ; -> 002E7277
002E723F  cmp      dword ptr [rax], -1
002E7242  je       0x2e7277  ; -> 002E7277
002E7244  movzx    ecx, word ptr [rax]
002E7247  cmp      cx, -1
002E724B  je       0x2e727c  ; -> 002E727C
002E724D  movsx    rax, cx
002E7251  imul     rcx, rax, 0x740
002E7258  add      rcx, qword ptr [rip + 0x1fdfcc9]  ; -> 022C6F28
002E725F  je       0x2e727c  ; -> 002E727C
002E7261  cmp      dword ptr [rcx + 0x284], ebx
002E7267  je       0x2e727c  ; -> 002E727C
002E7269  mov      edx, 4
002E726E  call     0x41e690  ; -> 0041E690 fn
002E7273  mov      ebx, eax
002E7275  jmp      0x2e727c  ; -> 002E727C
002E7277  mov      ebx, 1
002E727C  mov      rsi, qword ptr [rsp + 0x38]
002E7281  or       ebx, edi
002E7283  mov      eax, ebx
002E7285  mov      rbx, qword ptr [rsp + 0x30]
002E728A  add      rsp, 0x20
002E728E  pop      rdi
002E728F  ret      
```
