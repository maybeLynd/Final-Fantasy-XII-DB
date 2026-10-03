# Homing pack: `16-UI/Handbook/the-handbooks-monster-viewer.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-the-handbooks-monster-viewer.json`.

Bodies: 6. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001EBA90 (60 B, extent 001EBA90-001EBACC)

Entered from (direct sites whose caller this page cites): `001C6320` + 0x22C (call; `001C6320` is cited on this page)
Other direct sites: none

Host context: "r 002EED80 and per-tick tail     002EF050, and the model-instance container pass 00477F20 with its two callbacks disassembled from the authority     image and read whole, 2026-09-19; the entry reader 001C6320 read at its head, its tail and every call in between     (the light arithmetic 001C65A0..001C6940 by its calls only); its forty key strings read out of the image last_reviewed: 2026-09-29 audit:   passes: 1   last_pass: 2026-09-29 "

```
001EBA90  push     rbx
001EBA92  sub      rsp, 0x20
001EBA96  lea      rbx, [rcx + 0x40]
001EBA9A  movss    dword ptr [rcx + 0x250], xmm1
001EBAA2  mov      rax, qword ptr [rbx]
001EBAA5  mov      rcx, rbx
001EBAA8  movss    dword ptr [rbx + 0xd0], xmm1
001EBAB0  call     qword ptr [rax + 8]
001EBAB3  mov      rax, qword ptr [rbx]
001EBAB6  mov      rcx, rbx
001EBAB9  mov      dword ptr [rbx + 0xd4], 0x3f93cd3a
001EBAC3  add      rsp, 0x20
001EBAC7  pop      rbx
001EBAC8  jmp      qword ptr [rax + 8]
```

## 001EBB70 (128 B, extent 001EBB70-001EBBF0)

Entered from (direct sites whose caller this page cites): `001C6320` + 0x62D (call; `001C6320` is cited on this page)
Other direct sites: none

Host context: "r 002EED80 and per-tick tail     002EF050, and the model-instance container pass 00477F20 with its two callbacks disassembled from the authority     image and read whole, 2026-09-19; the entry reader 001C6320 read at its head, its tail and every call in between     (the light arithmetic 001C65A0..001C6940 by its calls only); its forty key strings read out of the image last_reviewed: 2026-09-29 audit:   passes: 1   last_pass: 2026-09-29 "

```
001EBB70  movups   xmm0, xmmword ptr [rdx]
001EBB73  add      rcx, 0x144
001EBB7A  movups   xmmword ptr [rcx], xmm0
001EBB7D  movups   xmm1, xmmword ptr [rdx + 0x10]
001EBB81  movups   xmmword ptr [rcx + 0x10], xmm1
001EBB85  movups   xmm0, xmmword ptr [rdx + 0x20]
001EBB89  movups   xmmword ptr [rcx + 0x20], xmm0
001EBB8D  movups   xmm1, xmmword ptr [rdx + 0x30]
001EBB91  movups   xmmword ptr [rcx + 0x30], xmm1
001EBB95  movups   xmm0, xmmword ptr [rdx + 0x40]
001EBB99  movups   xmmword ptr [rcx + 0x40], xmm0
001EBB9D  movups   xmm1, xmmword ptr [rdx + 0x50]
001EBBA1  movups   xmmword ptr [rcx + 0x50], xmm1
001EBBA5  movups   xmm0, xmmword ptr [rdx + 0x60]
001EBBA9  movups   xmmword ptr [rcx + 0x60], xmm0
001EBBAD  sub      rcx, -0x80
001EBBB1  movups   xmm0, xmmword ptr [rdx + 0x70]
001EBBB5  movups   xmmword ptr [rcx - 0x10], xmm0
001EBBB9  movups   xmm1, xmmword ptr [rdx + 0x80]
001EBBC0  movups   xmmword ptr [rcx], xmm1
001EBBC3  movups   xmm0, xmmword ptr [rdx + 0x90]
001EBBCA  movups   xmmword ptr [rcx + 0x10], xmm0
001EBBCE  movups   xmm1, xmmword ptr [rdx + 0xa0]
001EBBD5  movups   xmmword ptr [rcx + 0x20], xmm1
001EBBD9  movups   xmm0, xmmword ptr [rdx + 0xb0]
001EBBE0  movups   xmmword ptr [rcx + 0x30], xmm0
001EBBE4  movups   xmm1, xmmword ptr [rdx + 0xc0]
001EBBEB  movups   xmmword ptr [rcx + 0x40], xmm1
001EBBEF  ret      
```

## 001EBBF0 (36 B, extent 001EBBF0-001EBC14)

Entered from (direct sites whose caller this page cites): `001C6320` + 0xE2 (call; `001C6320` is cited on this page); `001C6320` + 0x124 (call; `001C6320` is cited on this page)
Other direct sites: none

Host context: "r 002EED80 and per-tick tail     002EF050, and the model-instance container pass 00477F20 with its two callbacks disassembled from the authority     image and read whole, 2026-09-19; the entry reader 001C6320 read at its head, its tail and every call in between     (the light arithmetic 001C65A0..001C6940 by its calls only); its forty key strings read out of the image last_reviewed: 2026-09-29 audit:   passes: 1   last_pass: 2026-09-29 " / "r 002EED80 and per-tick tail     002EF050, and the model-instance container pass 00477F20 with its two callbacks disassembled from the authority     image and read whole, 2026-09-19; the entry reader 001C6320 read at its head, its tail and every call in between     (the light arithmetic 001C65A0..001C6940 by its calls only); its forty key strings read out of the image last_reviewed: 2026-09-29 audit:   passes: 1   last_pass: 2026-09-29 "

```
001EBBF0  mov      dword ptr [rcx + 0x12c], 0
001EBBFA  test     r8d, r8d
001EBBFD  je       0x1ebc13  ; -> 001EBC13
001EBBFF  movsxd   rax, edx
001EBC02  mov      dword ptr [rcx + rax*4 + 0x124], r8d
001EBC0A  lea      eax, [rdx + 1]
001EBC0D  mov      dword ptr [rcx + 0x12c], eax
001EBC13  ret      
```

## 001EBC20 (44 B, extent 001EBC20-001EBC4C)

Entered from (direct sites whose caller this page cites): `001C6320` + 0x145 (call; `001C6320` is cited on this page)
Other direct sites: none

Host context: "r 002EED80 and per-tick tail     002EF050, and the model-instance container pass 00477F20 with its two callbacks disassembled from the authority     image and read whole, 2026-09-19; the entry reader 001C6320 read at its head, its tail and every call in between     (the light arithmetic 001C65A0..001C6940 by its calls only); its forty key strings read out of the image last_reviewed: 2026-09-29 audit:   passes: 1   last_pass: 2026-09-29 "

```
001EBC20  mov      r8d, edx
001EBC23  mov      byte ptr [rcx + 0x140], 1
001EBC2A  mov      eax, 0x66666667
001EBC2F  imul     edx
001EBC31  sar      edx, 5
001EBC34  mov      eax, edx
001EBC36  shr      eax, 0x1f
001EBC39  add      edx, eax
001EBC3B  lea      eax, [rdx + rdx*4]
001EBC3E  shl      eax, 4
001EBC41  sub      r8d, eax
001EBC44  mov      dword ptr [rcx + 0x224], r8d
001EBC4B  ret      
```

## 002ECBA0 (57 B, extent 002ECBA0-002ECBD9)

Entered from (direct sites whose caller this page cites): `0034B120` + 0x54 (call; `0034B120` is cited on this page)
Other direct sites: none

Host context: "02E28E0' on the Movement layer. Shared-caller fan-in; no Movement relationship to the viewer.  **Script_VM_Native_Bridge - MECHANICAL (SWE2-EC7-97, 2 edges).** The same '002EC6B0' is reached through '0034B120' and '0050D660' on that layer. Shared-caller fan-in; no bridge relationship to the viewer.  ## SWE2-EC7-81 update (2026-09-20) - '00537B10' parameter-pair setter measured  '00537B10' (141 B) is the '(ecx, edx)'-armed writer on the "

```
002ECBA0  test     edx, edx
002ECBA2  js       0x2ecbd8  ; -> 002ECBD8
002ECBA4  movsx    rax, word ptr [rcx + 0x1e]
002ECBA9  test     eax, eax
002ECBAB  js       0x2ecbd8  ; -> 002ECBD8
002ECBAD  lea      r9, [rax + rax*8]
002ECBB1  shl      r9, 5
002ECBB5  lea      rax, [rip + 0x1e751e4]  ; -> 02161DA0
002ECBBC  add      r9, rax
002ECBBF  mov      eax, dword ptr [rcx + 0x24]
002ECBC2  cmp      dword ptr [r9 + 0x5c], eax
002ECBC6  jne      0x2ecbd8  ; -> 002ECBD8
002ECBC8  cmp      r8d, 1
002ECBCC  jne      0x2ecbd8  ; -> 002ECBD8
002ECBCE  mov      eax, r8d
002ECBD1  bts      eax, edx
002ECBD4  or       dword ptr [r9 + 0x44], eax
002ECBD8  ret      
```

## 002F1690 (17 B, extent 002F1690-002F16A1)

Entered from (direct sites whose caller this page cites): `001C6320` + 0x27B (call; `001C6320` is cited on this page)
Other direct sites: none

Host context: "r 002EED80 and per-tick tail     002EF050, and the model-instance container pass 00477F20 with its two callbacks disassembled from the authority     image and read whole, 2026-09-19; the entry reader 001C6320 read at its head, its tail and every call in between     (the light arithmetic 001C65A0..001C6940 by its calls only); its forty key strings read out of the image last_reviewed: 2026-09-29 audit:   passes: 1   last_pass: 2026-09-29 "

```
002F1690  subss    xmm0, dword ptr [rip + 0x5d48e0]  ; -> 008C5F78 [f32 1000]
002F1698  movss    dword ptr [rip + 0x1fcc81c], xmm0  ; -> 022BDEBC
002F16A0  ret      
```
