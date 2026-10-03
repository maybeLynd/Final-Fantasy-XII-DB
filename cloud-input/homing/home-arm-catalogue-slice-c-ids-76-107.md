# Homing pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-C-ids-76-107.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-arm-catalogue-slice-c-ids-76-107.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001C1A60 (158 B, extent 001C1A60-001C1AFE)

Entered from (direct sites whose caller this page cites): `001C2790` + 0x6F (call; `001C2790` is cited on this page)
Other direct sites: none

Host context: "0x108' and 'rdx+0x108' and returns the incoming 'rcx' | Interior anchor '001C1C8C'; Interior anchor '001C1CB2'; Interior anchor '001C1CF9'; Interior anchor '001C1D09'; Interior anchor '001C1D0E' | | '001C2790' | 484 B | '001C2D50' + 0x49 | treats qwords 'rcx+0', '+8' and '+0x10' as begin, end and limit of 0x230-byte elements; when end differs from limit, it adds 0x230 to 'r8' if 'r8' lies in ['rdx', end) (unsigned), calls '001C2790' + 0"

```
001C1A60  mov      qword ptr [rsp + 8], rbx
001C1A65  mov      qword ptr [rsp + 0x10], rsi
001C1A6A  push     rdi
001C1A6B  sub      rsp, 0x20
001C1A6F  mov      rbx, r8
001C1A72  mov      rdi, rdx
001C1A75  mov      rsi, rcx
001C1A78  cmp      rdx, rcx
001C1A7B  je       0x1c1aeb  ; -> 001C1AEB
001C1A7D  nop      dword ptr [rax]
001C1A80  sub      rdi, 0x230
001C1A87  sub      rbx, 0x230
001C1A8E  lea      rdx, [rdi + 0x108]
001C1A95  mov      r8, rdi
001C1A98  sub      r8, rbx
001C1A9B  mov      r9d, 0x80
001C1AA1  mov      eax, dword ptr [rdi]
001C1AA3  lea      rcx, [rbx + 8]
001C1AA7  mov      dword ptr [rbx], eax
001C1AA9  mov      eax, dword ptr [rdx - 0x104]
001C1AAF  mov      dword ptr [rbx + 4], eax
001C1AB2  nop      dword ptr [rax]
001C1AB6  nop      word ptr [rax + rax]
001C1AC0  movzx    eax, byte ptr [r8 + rcx]
001C1AC5  mov      byte ptr [rcx], al
001C1AC7  movzx    eax, byte ptr [r8 + rcx + 1]
001C1ACD  mov      byte ptr [rcx + 1], al
001C1AD0  lea      rcx, [rcx + 2]
001C1AD4  sub      r9, 1
001C1AD8  jne      0x1c1ac0  ; -> 001C1AC0
001C1ADA  lea      rcx, [rbx + 0x108]
001C1AE1  call     0x1c22a0  ; -> 001C22A0 fn
001C1AE6  cmp      rdi, rsi
001C1AE9  jne      0x1c1a80  ; -> 001C1A80
001C1AEB  mov      rsi, qword ptr [rsp + 0x38]
001C1AF0  mov      rax, rbx
001C1AF3  mov      rbx, qword ptr [rsp + 0x30]
001C1AF8  add      rsp, 0x20
001C1AFC  pop      rdi
001C1AFD  ret      
```

## 001C1B00 (244 B, extent 001C1B00-001C1BF4)

Entered from (direct sites whose caller this page cites): `001C2790` + 0xF6 (call; `001C2790` is cited on this page); `001C2790` + 0x13F (call; `001C2790` is cited on this page)
Other direct sites: none

Host context: "0x108' and 'rdx+0x108' and returns the incoming 'rcx' | Interior anchor '001C1C8C'; Interior anchor '001C1CB2'; Interior anchor '001C1CF9'; Interior anchor '001C1D09'; Interior anchor '001C1D0E' | | '001C2790' | 484 B | '001C2D50' + 0x49 | treats qwords 'rcx+0', '+8' and '+0x10' as begin, end and limit of 0x230-byte elements; when end differs from limit, it adds 0x230 to 'r8' if 'r8' lies in ['rdx', end) (unsigned), calls '001C2790' + 0" / "0x108' and 'rdx+0x108' and returns the incoming 'rcx' | Interior anchor '001C1C8C'; Interior anchor '001C1CB2'; Interior anchor '001C1CF9'; Interior anchor '001C1D09'; Interior anchor '001C1D0E' | | '001C2790' | 484 B | '001C2D50' + 0x49 | treats qwords 'rcx+0', '+8' and '+0x10' as begin, end and limit of 0x230-byte elements; when end differs from limit, it adds 0x230 to 'r8' if 'r8' lies in ['rdx', end) (unsigned), calls '001C2790' + 0"

```
001C1B00  mov      qword ptr [rsp + 0x18], r8
001C1B05  mov      qword ptr [rsp + 0x10], rdx
001C1B0A  push     rbx
001C1B0B  sub      rsp, 0x30
001C1B0F  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001C1B18  mov      rbx, rcx
001C1B1B  mov      qword ptr [rcx], r9
001C1B1E  cmp      rdx, r8
001C1B21  je       0x1c1beb  ; -> 001C1BEB
001C1B27  nop      word ptr [rax + rax]
001C1B30  mov      r9, qword ptr [rbx]
001C1B33  mov      qword ptr [rsp + 0x40], r9
001C1B38  mov      qword ptr [rsp + 0x28], r9
001C1B3D  test     r9, r9
001C1B40  je       0x1c1bcf  ; -> 001C1BCF
001C1B46  mov      eax, dword ptr [rdx]
001C1B48  mov      dword ptr [r9], eax
001C1B4B  mov      eax, dword ptr [rdx + 4]
001C1B4E  mov      dword ptr [r9 + 4], eax
001C1B52  lea      rax, [r9 + 8]
001C1B56  lea      rcx, [rdx + 8]
001C1B5A  mov      r8d, 2
001C1B60  movups   xmm0, xmmword ptr [rcx]
001C1B63  movups   xmmword ptr [rax], xmm0
001C1B66  movups   xmm1, xmmword ptr [rcx + 0x10]
001C1B6A  movups   xmmword ptr [rax + 0x10], xmm1
001C1B6E  movups   xmm0, xmmword ptr [rcx + 0x20]
001C1B72  movups   xmmword ptr [rax + 0x20], xmm0
001C1B76  movups   xmm1, xmmword ptr [rcx + 0x30]
001C1B7A  movups   xmmword ptr [rax + 0x30], xmm1
001C1B7E  movups   xmm0, xmmword ptr [rcx + 0x40]
001C1B82  movups   xmmword ptr [rax + 0x40], xmm0
001C1B86  movups   xmm1, xmmword ptr [rcx + 0x50]
001C1B8A  movups   xmmword ptr [rax + 0x50], xmm1
001C1B8E  movups   xmm0, xmmword ptr [rcx + 0x60]
001C1B92  movups   xmmword ptr [rax + 0x60], xmm0
001C1B96  lea      rax, [rax + 0x80]
001C1B9D  movups   xmm1, xmmword ptr [rcx + 0x70]
001C1BA1  movups   xmmword ptr [rax - 0x10], xmm1
001C1BA5  lea      rcx, [rcx + 0x80]
001C1BAC  sub      r8, 1
001C1BB0  jne      0x1c1b60  ; -> 001C1B60
001C1BB2  add      rdx, 0x108
001C1BB9  lea      rcx, [r9 + 0x108]
001C1BC0  call     0x1c1e70  ; -> 001C1E70 fn
001C1BC5  mov      r8, qword ptr [rsp + 0x50]
001C1BCA  mov      rdx, qword ptr [rsp + 0x48]
001C1BCF  add      rdx, 0x230
001C1BD6  mov      qword ptr [rsp + 0x48], rdx
001C1BDB  add      qword ptr [rbx], 0x230
001C1BE2  cmp      rdx, r8
001C1BE5  jne      0x1c1b30  ; -> 001C1B30
001C1BEB  mov      rax, rbx
001C1BEE  add      rsp, 0x30
001C1BF2  pop      rbx
001C1BF3  ret      
```

## 001C1E70 (417 B, extent 001C1E70-001C2011)

Entered from (direct sites whose caller this page cites): `001C1C80` + 0x89 (call; `001C1C80` is cited on this page)
Other direct sites: `001C1B00` + 0xC0 (call)

Host context: "very anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*  | function | size | entered from | what the body does | interior anchors | |---|---|---|---|---| | '001C1C80' | 151 B | '001C2D50' + 0x34 | copies dwords '+0' and '+4' of 'rdx' to 'rcx', copies the 0x100 bytes at 'rdx+8' to 'rcx+8' with 16-byte 'movups' moves in a loop of two 0x80-byte passes, then calls '001C1C80' + 0x89 with 'rcx+0x108'"

```
001C1E70  mov      qword ptr [rsp + 8], rcx
001C1E75  push     rdi
001C1E76  sub      rsp, 0x30
001C1E7A  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001C1E83  mov      qword ptr [rsp + 0x48], rbx
001C1E88  mov      rbx, rdx
001C1E8B  mov      rdi, rcx
001C1E8E  movups   xmm0, xmmword ptr [rdx]
001C1E91  movups   xmmword ptr [rcx], xmm0
001C1E94  mov      rax, qword ptr [rdx + 0x10]
001C1E98  mov      qword ptr [rcx + 0x10], rax
001C1E9C  mov      rax, qword ptr [rdx + 0x18]
001C1EA0  mov      qword ptr [rcx + 0x18], rax
001C1EA4  mov      rax, qword ptr [rdx + 0x20]
001C1EA8  mov      qword ptr [rcx + 0x20], rax
001C1EAC  add      rdx, 0x28
001C1EB0  add      rcx, 0x28
001C1EB4  call     0x1c1c00  ; -> 001C1C00 fn
001C1EB9  nop      
001C1EBA  movzx    eax, byte ptr [rbx + 0x38]
001C1EBE  and      eax, 1
001C1EC1  mov      rcx, qword ptr [rbx + 0x38]
001C1EC5  sub      rcx, rax
001C1EC8  call     0x1c26b0  ; -> 001C26B0 fn
001C1ECD  mov      qword ptr [rdi + 0x38], rax
001C1ED1  lea      rdx, [rbx + 0x40]
001C1ED5  lea      rcx, [rdi + 0x40]
001C1ED9  call     0x67acf0  ; -> 0067ACF0 fn
001C1EDE  movups   xmm0, xmmword ptr [rbx + 0x58]
001C1EE2  movups   xmmword ptr [rdi + 0x58], xmm0
001C1EE6  movups   xmm0, xmmword ptr [rbx + 0x68]
001C1EEA  movups   xmmword ptr [rdi + 0x68], xmm0
001C1EEE  movups   xmm0, xmmword ptr [rbx + 0x78]
001C1EF2  movups   xmmword ptr [rdi + 0x78], xmm0
001C1EF6  movups   xmm0, xmmword ptr [rbx + 0x88]
001C1EFD  movups   xmmword ptr [rdi + 0x88], xmm0
001C1F04  movups   xmm0, xmmword ptr [rbx + 0x98]
001C1F0B  movups   xmmword ptr [rdi + 0x98], xmm0
001C1F12  movups   xmm0, xmmword ptr [rbx + 0xa8]
001C1F19  movups   xmmword ptr [rdi + 0xa8], xmm0
001C1F20  movups   xmm0, xmmword ptr [rbx + 0xb8]
001C1F27  movups   xmmword ptr [rdi + 0xb8], xmm0
001C1F2E  movups   xmm0, xmmword ptr [rbx + 0xc8]
001C1F35  movups   xmmword ptr [rdi + 0xc8], xmm0
001C1F3C  movups   xmm0, xmmword ptr [rbx + 0xd8]
001C1F43  movups   xmmword ptr [rdi + 0xd8], xmm0
001C1F4A  movzx    eax, byte ptr [rbx + 0xe8]
001C1F51  mov      byte ptr [rdi + 0xe8], al
001C1F57  movzx    eax, byte ptr [rbx + 0xe9]
001C1F5E  mov      byte ptr [rdi + 0xe9], al
001C1F64  movzx    eax, byte ptr [rbx + 0xea]
001C1F6B  mov      byte ptr [rdi + 0xea], al
001C1F71  mov      eax, dword ptr [rbx + 0xec]
001C1F77  mov      dword ptr [rdi + 0xec], eax
001C1F7D  mov      eax, dword ptr [rbx + 0xf0]
001C1F83  mov      dword ptr [rdi + 0xf0], eax
001C1F89  mov      eax, dword ptr [rbx + 0xf4]
001C1F8F  mov      dword ptr [rdi + 0xf4], eax
001C1F95  mov      eax, dword ptr [rbx + 0xf8]
001C1F9B  mov      dword ptr [rdi + 0xf8], eax
001C1FA1  mov      eax, dword ptr [rbx + 0xfc]
001C1FA7  mov      dword ptr [rdi + 0xfc], eax
001C1FAD  movups   xmm0, xmmword ptr [rbx + 0x100]
001C1FB4  movups   xmmword ptr [rdi + 0x100], xmm0
001C1FBB  mov      eax, dword ptr [rbx + 0x110]
001C1FC1  mov      dword ptr [rdi + 0x110], eax
001C1FC7  mov      eax, dword ptr [rbx + 0x114]
001C1FCD  mov      dword ptr [rdi + 0x114], eax
001C1FD3  mov      eax, dword ptr [rbx + 0x118]
001C1FD9  mov      dword ptr [rdi + 0x118], eax
001C1FDF  mov      eax, dword ptr [rbx + 0x11c]
001C1FE5  mov      dword ptr [rdi + 0x11c], eax
001C1FEB  mov      eax, dword ptr [rbx + 0x120]
001C1FF1  mov      dword ptr [rdi + 0x120], eax
001C1FF7  mov      eax, dword ptr [rbx + 0x124]
001C1FFD  mov      dword ptr [rdi + 0x124], eax
001C2003  mov      rax, rdi
001C2006  mov      rbx, qword ptr [rsp + 0x48]
001C200B  add      rsp, 0x30
001C200F  pop      rdi
001C2010  ret      
```

## 001C2230 (104 B, extent 001C2230-001C2298)

Entered from (direct sites whose caller this page cites): `001C2790` + 0x7A (call; `001C2790` is cited on this page)
Other direct sites: none

Host context: "0x108' and 'rdx+0x108' and returns the incoming 'rcx' | Interior anchor '001C1C8C'; Interior anchor '001C1CB2'; Interior anchor '001C1CF9'; Interior anchor '001C1D09'; Interior anchor '001C1D0E' | | '001C2790' | 484 B | '001C2D50' + 0x49 | treats qwords 'rcx+0', '+8' and '+0x10' as begin, end and limit of 0x230-byte elements; when end differs from limit, it adds 0x230 to 'r8' if 'r8' lies in ['rdx', end) (unsigned), calls '001C2790' + 0"

```
001C2230  push     rbx
001C2232  sub      rsp, 0x20
001C2236  mov      eax, dword ptr [rdx]
001C2238  lea      r8, [rcx + 8]
001C223C  mov      dword ptr [rcx], eax
001C223E  mov      r9, rdx
001C2241  mov      eax, dword ptr [rdx + 4]
001C2244  mov      rbx, rcx
001C2247  mov      dword ptr [rcx + 4], eax
001C224A  sub      r9, rcx
001C224D  mov      r10d, 0x80
001C2253  nop      dword ptr [rax]
001C2257  nop      word ptr [rax + rax]
001C2260  movzx    eax, byte ptr [r9 + r8]
001C2265  mov      byte ptr [r8], al
001C2268  movzx    eax, byte ptr [r9 + r8 + 1]
001C226E  mov      byte ptr [r8 + 1], al
001C2272  lea      r8, [r8 + 2]
001C2276  sub      r10, 1
001C227A  jne      0x1c2260  ; -> 001C2260
001C227C  add      rdx, 0x108
001C2283  add      rcx, 0x108
001C228A  call     0x1c22a0  ; -> 001C22A0 fn
001C228F  mov      rax, rbx
001C2292  add      rsp, 0x20
001C2296  pop      rbx
001C2297  ret      
```
