# Homing pack: `00-Engine-Core-Runtime/Application-Root/game-application.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-game-application.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001A49C0 (394 B, extent 001A49C0-001A4B4A)

Entered from (direct sites whose caller this page cites): `008B1B10` + 0x1B (call; `008B1B10` is cited on this page)
Other direct sites: `008A69A0` + 0x1B (call)

Host context: "58]'-keyed once-init blocks ('008092FC'/'0080929C' on '02D3ECE0' and '02D3EC9C') lazily build the '02D3ECB0' tree - self-linked head, allocator vtable '008F6500' at '02D3ECD8', '00808B90'-registered '008B1B10'/'008B1C00' atexit teardowns - and the second guards the one-time '00677030' registration of '"/GameData/D3D11/ArtData/shared/idmaps.txt"' into '02D3ECA8'; the lookup builds its key with '001A5630', walks the tree under the '02D3E8"

```
001A49C0  test     rdx, rdx
001A49C3  je       0x1a4b49  ; -> 001A4B49
001A49C9  mov      qword ptr [rsp + 8], rcx
001A49CE  push     rsi
001A49CF  sub      rsp, 0x20
001A49D3  mov      qword ptr [rsp + 0x38], rbx
001A49D8  mov      rsi, rdx
001A49DB  mov      qword ptr [rsp + 0x40], rbp
001A49E0  mov      rax, rcx
001A49E3  mov      qword ptr [rsp + 0x48], rdi
001A49E8  nop      dword ptr [rax + rax]
001A49F0  mov      rdx, qword ptr [rsi]
001A49F3  mov      rcx, rax
001A49F6  call     0x1a49c0  ; -> 001A49C0 fn
001A49FB  mov      rbp, qword ptr [rsi + 8]
001A49FF  lea      rdi, [rsi + 0x20]
001A4A03  mov      rax, qword ptr [rdi + 0x38]
001A4A07  lea      rbx, [rdi + 0x20]
001A4A0B  cmp      rax, 0x10
001A4A0F  jb       0x1a4a54  ; -> 001A4A54
001A4A11  mov      rcx, qword ptr [rbx]
001A4A14  inc      rax
001A4A17  cmp      rax, 0x1000
001A4A1D  jb       0x1a4a4f  ; -> 001A4A4F
001A4A1F  test     cl, 0x1f
001A4A22  jne      0x1a4b12  ; -> 001A4B12
001A4A28  mov      rax, qword ptr [rcx - 8]
001A4A2C  cmp      rax, rcx
001A4A2F  jae      0x1a4b0b  ; -> 001A4B0B
001A4A35  sub      rcx, rax
001A4A38  cmp      rcx, 8
001A4A3C  jb       0x1a4b04  ; -> 001A4B04
001A4A42  cmp      rcx, 0x27
001A4A46  ja       0x1a4afd  ; -> 001A4AFD
001A4A4C  mov      rcx, rax
001A4A4F  call     0x210eb0  ; -> 00210EB0 fn
001A4A54  mov      qword ptr [rbx + 0x18], 0xf
001A4A5C  cmp      qword ptr [rbx + 0x18], 0x10
001A4A61  mov      qword ptr [rbx + 0x10], 0
001A4A69  jb       0x1a4a6e  ; -> 001A4A6E
001A4A6B  mov      rbx, qword ptr [rbx]
001A4A6E  mov      byte ptr [rbx], 0
001A4A71  mov      rax, qword ptr [rdi + 0x18]
001A4A75  cmp      rax, 0x10
001A4A79  jb       0x1a4ab6  ; -> 001A4AB6
001A4A7B  mov      rcx, qword ptr [rdi]
001A4A7E  inc      rax
001A4A81  cmp      rax, 0x1000
001A4A87  jb       0x1a4ab1  ; -> 001A4AB1
001A4A89  test     cl, 0x1f
001A4A8C  jne      0x1a4b2e  ; -> 001A4B2E
001A4A92  mov      rax, qword ptr [rcx - 8]
001A4A96  cmp      rax, rcx
001A4A99  jae      0x1a4b27  ; -> 001A4B27
001A4A9F  sub      rcx, rax
001A4AA2  cmp      rcx, 8
001A4AA6  jb       0x1a4b20  ; -> 001A4B20
001A4AA8  cmp      rcx, 0x27
001A4AAC  ja       0x1a4b19  ; -> 001A4B19
001A4AAE  mov      rcx, rax
001A4AB1  call     0x210eb0  ; -> 00210EB0 fn
001A4AB6  mov      qword ptr [rdi + 0x18], 0xf
001A4ABE  cmp      qword ptr [rdi + 0x18], 0x10
001A4AC3  mov      qword ptr [rdi + 0x10], 0
001A4ACB  jb       0x1a4ad0  ; -> 001A4AD0
001A4ACD  mov      rdi, qword ptr [rdi]
001A4AD0  mov      rcx, qword ptr [rsp + 0x30]
001A4AD5  mov      r8d, 0x60
001A4ADB  add      rcx, 0x30
001A4ADF  mov      byte ptr [rdi], 0
001A4AE2  mov      rdx, rsi
001A4AE5  mov      rax, qword ptr [rcx]
001A4AE8  call     qword ptr [rax + 0x18]
001A4AEB  mov      rsi, rbp
001A4AEE  test     rbp, rbp
001A4AF1  je       0x1a4b35  ; -> 001A4B35
001A4AF3  mov      rax, qword ptr [rsp + 0x30]
001A4AF8  jmp      0x1a49f0  ; -> 001A49F0
001A4AFD  call     qword ptr [rip + 0x71e2a5]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B03  int3     
001A4B04  call     qword ptr [rip + 0x71e29e]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B0A  int3     
001A4B0B  call     qword ptr [rip + 0x71e297]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B11  int3     
001A4B12  call     qword ptr [rip + 0x71e290]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B18  int3     
001A4B19  call     qword ptr [rip + 0x71e289]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B1F  int3     
001A4B20  call     qword ptr [rip + 0x71e282]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B26  int3     
001A4B27  call     qword ptr [rip + 0x71e27b]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B2D  int3     
001A4B2E  call     qword ptr [rip + 0x71e274]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
001A4B34  int3     
001A4B35  mov      rbp, qword ptr [rsp + 0x40]
001A4B3A  mov      rbx, qword ptr [rsp + 0x38]
001A4B3F  mov      rdi, qword ptr [rsp + 0x48]
001A4B44  add      rsp, 0x20
001A4B48  pop      rsi
001A4B49  ret      
```

## 0025A880 (14 B, extent 0025A880-0025A88E)

Entered from (direct sites whose caller this page cites): `00229590` + 0x293 (call; `00229590` is cited on this page); `00229590` + 0x2F7 (call; `00229590` is cited on this page)
Other direct sites: `003503B0` + 0x12 (jmp)

Host context: "ning-Console/the-282-command-parameter-console.md)) — two axes under one tunable scale. **BE-2 ANSWERED 2026-09-12 (FABLE).**       *The byte is the pause flag.* Its writer is the pause-menu handler '00229590' (registered as a       callback by '002282F0' at '0022832E'; its own debug prints are '"PauseMenu Create\n"' and       '"PauseMenu Open\n"', '0022995A' / '00229864'): the open path sets it through the app's wrapper       '0017E720" / "ning-Console/the-282-command-parameter-console.md)) — two axes under one tunable scale. **BE-2 ANSWERED 2026-09-12 (FABLE).**       *The byte is the pause flag.* Its writer is the pause-menu handler '00229590' (registered as a       callback by '002282F0' at '0022832E'; its own debug prints are '"PauseMenu Create\n"' and       '"PauseMenu Open\n"', '0022995A' / '00229864'): the open path sets it through the app's wrapper       '0017E720"

```
0025A880  xor      eax, eax
0025A882  test     ecx, ecx
0025A884  setne    al
0025A887  mov      dword ptr [rip + 0x1e3dac7], eax  ; -> 02098354
0025A88D  ret      
```
