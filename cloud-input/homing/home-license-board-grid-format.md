# Homing pack: `12-Items-Equipment-Shops-License/license-board-grid-format.md`

Generated 2026-10-03 09:39 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-license-board-grid-format.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00282F10 (98 B, extent 00282F10-00282F72)

Entered from (direct sites whose caller this page cites): `003FCAD0` + 0xCD (call; `003FCAD0` is cited on this page)
Other direct sites: none

Host context: "erior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*  | function | size | what the body does | interior anchors | |---|---|---|---| | '003FCAD0' | 495 B | for k from 'r8d' to 'r9d' (signed) takes 'E' = qword '[rcx+0x10]'[k], stores word 7 at 'E+0xa', clears bit '0x1' of dword 'E+8' and copies byte '+0x3f' of qword 'E+0x20' to 'E+0x39'; returns if 'w' = word 'rdx+8' is '0xf"

```
00282F10  xor      r9d, r9d
00282F13  lea      eax, [rcx - 0x1000]
00282F19  cmp      eax, 0x1a4
00282F1E  ja       0x282f29  ; -> 00282F29
00282F20  lea      r9d, [rcx - 0x1000]
00282F27  jmp      0x282f4f  ; -> 00282F4F
00282F29  lea      eax, [rcx - 0x4000]
00282F2F  cmp      eax, 0x18
00282F32  ja       0x282f3d  ; -> 00282F3D
00282F34  lea      r9d, [rcx - 0x3e5c]
00282F3B  jmp      0x282f4f  ; -> 00282F4F
00282F3D  lea      eax, [rcx - 0x3000]
00282F43  cmp      eax, 0x51
00282F46  ja       0x282f4f  ; -> 00282F4F
00282F48  lea      r9d, [rcx - 0x2e44]
00282F4F  movzx    ecx, byte ptr [rdx + 0x60]
00282F53  mov      r8d, 1
00282F59  mov      rax, qword ptr [rip + 0x1e17cd0]  ; -> 0209AC30
00282F60  shl      r8d, cl
00282F63  movsxd   rcx, r9d
00282F66  test     byte ptr [rcx + rax + 0xb2e], r8b
00282F6E  setne    al
00282F71  ret      
```
