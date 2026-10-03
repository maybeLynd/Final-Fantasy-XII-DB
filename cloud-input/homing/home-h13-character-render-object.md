# Homing pack: `17-Presentation-Rendering/Character-Rendering/character-render-object.md`

Generated 2026-10-03 13:52 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h13-character-render-object.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001E1440 (80 B, extent 001E1440-001E1490)

Entered from (direct sites whose caller this page cites): `001E2250` + 0xC6 (call; `001E2250` is cited on this page); `001E2250` + 0x19F (call; `001E2250` is cited on this page)
Other direct sites: none

Host context: "very anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*  | function | size | entered from | what the body does | interior anchors | |---|---|---|---|---| | '001E2250' | 928 B | '001E5370' + 0x81 | inserts 'r8d' copies of the 0x18-byte element at 'r9' (qword '+8', byte '+0x10') before 'rdx' into the array with qwords 'B', 'E', 'C' at 'rcx', 'rcx+8', 'rcx+0x10': returns when 'r8d' is 0; when 'r8d" / "very anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*  | function | size | entered from | what the body does | interior anchors | |---|---|---|---|---| | '001E2250' | 928 B | '001E5370' + 0x81 | inserts 'r8d' copies of the 0x18-byte element at 'r9' (qword '+8', byte '+0x10') before 'rdx' into the array with qwords 'B', 'E', 'C' at 'rcx', 'rcx+8', 'rcx+0x10': returns when 'r8d' is 0; when 'r8d"

```
001E1440  cmp      rcx, rdx
001E1443  je       0x1e148c  ; -> 001E148C
001E1445  mov      r9, r8
001E1448  lea      rax, [rcx + 0x10]
001E144C  sub      r9, rcx
001E144F  lea      r10, [rip + 0x71fc62]  ; -> 009010B8
001E1456  lea      r11, [rip + 0x71fc7b]  ; -> 009010D8
001E145D  nop      dword ptr [rax]
001E1460  test     r8, r8
001E1463  je       0x1e147b  ; -> 001E147B
001E1465  mov      qword ptr [r8], r10
001E1468  mov      rcx, qword ptr [rax - 8]
001E146C  mov      qword ptr [r9 + rax - 8], rcx
001E1471  movzx    ecx, byte ptr [rax]
001E1474  mov      byte ptr [r9 + rax], cl
001E1478  mov      qword ptr [r8], r11
001E147B  add      rax, 0x18
001E147F  add      r8, 0x18
001E1483  lea      rcx, [rax - 0x10]
001E1487  cmp      rcx, rdx
001E148A  jne      0x1e1460  ; -> 001E1460
001E148C  mov      rax, r8
001E148F  ret      
```
