# Homing pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-A-ids-12-43.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-arm-catalogue-slice-a-ids-12-43.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001BBF40 (118 B, extent 001BBF40-001BBFB6)

Entered from (direct sites whose caller this page cites): `001BC190` + 0x148 (call; `001BC190` is cited on this page)
Other direct sites: none

Host context: "-byte render body ([the post-process page](../../22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md)'s largest 'UQ-289' member) |         | '+0xC71' | '001BC190', '001E2AF0', '001F8D10' | render support and **character-render material-parameter binding** — the offset the renderer reads with a 'cmp', so a branch condition on both sides |         | '+0xCF4' | '00180090' | a 40-byte float get"

```
001BBF40  mov      qword ptr [rsp + 8], rbx
001BBF45  mov      qword ptr [rsp + 0x10], rbp
001BBF4A  mov      qword ptr [rsp + 0x18], rsi
001BBF4F  push     rdi
001BBF50  sub      rsp, 0x20
001BBF54  mov      rsi, rcx
001BBF57  lea      rbx, [rcx + 0xa0]
001BBF5E  mov      edi, 0x20
001BBF63  mov      rcx, qword ptr [rbx]
001BBF66  test     rcx, rcx
001BBF69  je       0x1bbf70  ; -> 001BBF70
001BBF6B  call     0x183720  ; -> 00183720 fn
001BBF70  add      rbx, 8
001BBF74  sub      rdi, 1
001BBF78  jne      0x1bbf63  ; -> 001BBF63
001BBF7A  xor      edx, edx
001BBF7C  lea      rcx, [rsi + 0xa0]
001BBF83  mov      r8d, 0x100
001BBF89  call     0x861ec0  ; -> 00861EC0 fn
001BBF8E  lea      rcx, [rsi + 0x1a0]
001BBF95  xor      edx, edx
001BBF97  mov      r8d, 0x100
001BBF9D  mov      rbx, qword ptr [rsp + 0x30]
001BBFA2  mov      rbp, qword ptr [rsp + 0x38]
001BBFA7  mov      rsi, qword ptr [rsp + 0x40]
001BBFAC  add      rsp, 0x20
001BBFB0  pop      rdi
001BBFB1  jmp      0x861ec0  ; -> 00861EC0 fn
```

## 001DE180 (116 B, extent 001DE180-001DE1F4)

Entered from (direct sites whose caller this page cites): `001DE5D0` + 0x720 (call; `001DE5D0` is cited on this page)
Other direct sites: `001DE300` + 0x10 (call); `001DE3B0` + 0x14 (call)

Host context: "console formatting fan-in, not an actor relationship of the arm catalogue.  **Save_Load_Settings — MECHANICAL (SWE2-EC7-169, 2 edges).** '0017D280' — the arm's '"get char…"' formatter — is called by '001DE5D0'/'001DF350' of that layer; the same string helper reused, not a save relationship of the console.  **Script_VM_Native_Bridge — MECHANICAL (SWE2-EC7-169, 25 edges).** '0017D280' and '002ED6F0' are the console's shared output helpers"

```
001DE180  mov      qword ptr [rsp + 8], rbx
001DE185  push     rdi
001DE186  sub      rsp, 0x20
001DE18A  mov      rax, qword ptr [rcx - 0x90]
001DE191  mov      rdi, rcx
001DE194  movsxd   rdx, dword ptr [rax + 4]
001DE198  lea      rax, [rip + 0x722e89]  ; -> 00901028
001DE19F  mov      qword ptr [rdx + rcx - 0x90], rax
001DE1A7  mov      rax, qword ptr [rcx - 0x90]
001DE1AE  movsxd   rdx, dword ptr [rax + 4]
001DE1B2  lea      rax, [rip + 0x722d67]  ; -> 00900F20
001DE1B9  lea      r8d, [rdx - 0x90]
001DE1C0  mov      dword ptr [rdx + rcx - 0x94], r8d
001DE1C8  mov      qword ptr [rcx - 0x80], rax
001DE1CC  add      rcx, -0x80
001DE1D0  call     0x1df8c0  ; -> 001DF8C0 fn
001DE1D5  lea      rcx, [rdi - 0x80]
001DE1D9  call     qword ptr [rip + 0x6e45c1]  ; -> 008C27A0 [u64 0x0000000001CCDA9C]
001DE1DF  lea      rcx, [rdi - 0x78]
001DE1E3  mov      rbx, qword ptr [rsp + 0x30]
001DE1E8  add      rsp, 0x20
001DE1EC  pop      rdi
001DE1ED  jmp      qword ptr [rip + 0x6e4354]  ; -> 008C2548 [u64 0x0000000001CCDEFE]
```
