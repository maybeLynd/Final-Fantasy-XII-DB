# F-interior pack: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-00-0a.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-element-types-00-0a.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

## 00430A60 (139 B, extent 00430A60-00430AEB)

Page context: "f a 0x40-byte block | | '0042FCF0' | four heads | rebase a **four-track group** (heads at '+0'/'+0x10'/'+0x20'/'+0x30') | | '00431040' | group | float-scale all three tracks of a group by 'xmm1' via '00430A60' | | '00430A60' | head | scale one keyframe array: resolves '+0', multiplies each 8-byte entry's '+4' float by 'xmm1', entry count = byte '+0xC'; then the same for '+4'/byte '+0xD'. **So each track head owns two 8-byte-record keyfr"

```
00430A60  mov      qword ptr [rsp + 8], rbx
00430A65  push     rdi
00430A66  sub      rsp, 0x30
00430A6A  mov      rdi, rcx
00430A6D  movaps   xmmword ptr [rsp + 0x20], xmm6
00430A72  mov      ecx, dword ptr [rcx]
00430A74  movaps   xmm6, xmm1
00430A77  call     0x20e600  ; -> 0020E600 fn
00430A7C  xor      ebx, ebx
00430A7E  mov      rdx, rax
00430A81  mov      ecx, ebx
00430A83  cmp      byte ptr [rdi + 0xc], cl
00430A86  jbe      0x430aab  ; -> 00430AAB
00430A88  nop      dword ptr [rax + rax]
00430A90  movaps   xmm0, xmm6
00430A93  inc      ecx
00430A95  mulss    xmm0, dword ptr [rdx + 4]
00430A9A  lea      rdx, [rdx + 8]
00430A9E  movss    dword ptr [rdx - 4], xmm0
00430AA3  movzx    eax, byte ptr [rdi + 0xc]
00430AA7  cmp      ecx, eax
00430AA9  jl       0x430a90  ; -> 00430A90
00430AAB  mov      ecx, dword ptr [rdi + 4]
00430AAE  call     0x20e600  ; -> 0020E600 fn
00430AB3  cmp      byte ptr [rdi + 0xd], bl
00430AB6  jbe      0x430adb  ; -> 00430ADB
00430AB8  nop      dword ptr [rax + rax]
00430AC0  movaps   xmm0, xmm6
00430AC3  inc      ebx
00430AC5  mulss    xmm0, dword ptr [rax + 4]
00430ACA  lea      rax, [rax + 8]
00430ACE  movss    dword ptr [rax - 4], xmm0
00430AD3  movzx    ecx, byte ptr [rdi + 0xd]
00430AD7  cmp      ebx, ecx
00430AD9  jl       0x430ac0  ; -> 00430AC0
00430ADB  mov      rbx, qword ptr [rsp + 0x40]
00430AE0  movaps   xmm6, xmmword ptr [rsp + 0x20]
00430AE5  add      rsp, 0x30
00430AE9  pop      rdi
00430AEA  ret      
```
