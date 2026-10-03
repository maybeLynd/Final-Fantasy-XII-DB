# Homing pack: `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-how-a-sound-request-becomes-a-voice.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00205C70 (227 B, extent 00205C70-00205D53)

Entered from (direct sites whose caller this page cites): `00206E90` + 0x16 (call; `00206E90` is cited on this page)
Other direct sites: none

Host context: " bit '0x1B' with '+0x7C == 0x29' asserts ('008C2430', code 5); bit '0x20' with '+0x7C == 0x3F' double-runs '00208CF0' then switches on '+0x7C' - '0x3A' runs '002076D0' returning 1, '0x21'/'0x3D' run '00206E90' with 'dl' 1/0 returning 0, anything else asserts code '0xE'; otherwise 'dword[+0x70] & 0x200' runs '00208C60(rcx+0x40, 8)' into '00206D30' and '00207E90(rsi+0x40, result)' returning 1, else '00206EE0' returning 1 - the state-keyed"

```
00205C70  push     rsi
00205C72  push     rdi
00205C73  push     r14
00205C75  sub      rsp, 0x30
00205C79  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00205C82  mov      qword ptr [rsp + 0x50], rbx
00205C87  movzx    r14d, dl
00205C8B  mov      rsi, rcx
00205C8E  mov      ecx, 0x28
00205C93  call     0x210ec0  ; -> 00210EC0 fn
00205C98  mov      rbx, rax
00205C9B  mov      qword ptr [rsp + 0x60], rax
00205CA0  xor      edi, edi
00205CA2  test     rax, rax
00205CA5  je       0x205cd0  ; -> 00205CD0
00205CA7  mov      eax, edi
00205CA9  test     r14b, r14b
00205CAC  setne    al
00205CAF  add      eax, 0xa
00205CB2  mov      dword ptr [rbx + 8], eax
00205CB5  mov      dword ptr [rbx + 0xc], edi
00205CB8  mov      qword ptr [rbx + 0x10], rdi
00205CBC  mov      qword ptr [rbx + 0x18], rdi
00205CC0  lea      rax, [rip + 0x6ffc29]  ; -> 009058F0
00205CC7  mov      qword ptr [rbx], rax
00205CCA  mov      qword ptr [rbx + 0x20], rdi
00205CCE  jmp      0x205cd3  ; -> 00205CD3
00205CD0  mov      rbx, rdi
00205CD3  mov      qword ptr [rsp + 0x60], rbx
00205CD8  mov      ecx, 0x20
00205CDD  call     0x210ec0  ; -> 00210EC0 fn
00205CE2  mov      r8, rax
00205CE5  test     rax, rax
00205CE8  je       0x205d06  ; -> 00205D06
00205CEA  lea      rax, [rip + 0x6ffbcf]  ; -> 009058C0
00205CF1  mov      qword ptr [r8], rax
00205CF4  mov      qword ptr [r8 + 8], 1
00205CFC  mov      qword ptr [r8 + 0x10], rdi
00205D00  mov      qword ptr [r8 + 0x18], rdi
00205D04  jmp      0x205d09  ; -> 00205D09
00205D06  mov      r8, rdi
00205D09  mov      rax, qword ptr [rsi + 8]
00205D0D  mov      qword ptr [rbx + 0x18], rax
00205D11  mov      rax, qword ptr [rsi + 8]
00205D15  mov      rcx, qword ptr [rax + 0x10]
00205D19  test     rcx, rcx
00205D1C  je       0x205d2e  ; -> 00205D2E
00205D1E  mov      qword ptr [rbx + 0x10], rcx
00205D22  mov      rcx, qword ptr [rsi + 8]
00205D26  mov      rdx, qword ptr [rcx + 0x10]
00205D2A  mov      qword ptr [rdx + 0x18], rbx
00205D2E  mov      rcx, qword ptr [rsi + 8]
00205D32  mov      qword ptr [rcx + 0x10], rbx
00205D36  mov      qword ptr [rbx + 0x20], r8
00205D3A  mov      qword ptr [r8 + 0x18], rbx
00205D3E  mov      qword ptr [rsi + 8], r8
00205D42  mov      rax, rbx
00205D45  mov      rbx, qword ptr [rsp + 0x50]
00205D4A  add      rsp, 0x30
00205D4E  pop      r14
00205D50  pop      rdi
00205D51  pop      rsi
00205D52  ret      
```

## 00212970 (127 B, extent 00212970-002129EF)

Entered from (direct sites whose caller this page cites): `002129F0` + 0x9 (call; `002129F0` is cited on this page)
Other direct sites: none

Host context: "44'](../../_index/ADDRESS-INDEX.md) | | '0021A040' (182 B) | find-or-create — walks the intrusive list at '[ctx + 8]' for an element whose '[elem + 0x10] + 0x38' equals the sound id; on a miss, when '002129F0' reports capacity and the payload is non-null, calls the context vtable '+0x30' factory and hands the fresh object to '00222DC0' | ['0021A0A9'](../../_index/ADDRESS-INDEX.md) | | '00222DC0' (346 B) | record constructor — asserts '["

```
00212970  mov      eax, dword ptr [rip + 0x1dc0d3a]  ; -> 01FD36B0
00212976  lea      r9, [rip + 0x1dc0d43]  ; -> 01FD36C0
0021297D  inc      eax
0021297F  lea      r10, [rip + 0x1dc113a]  ; -> 01FD3AC0
00212986  and      eax, 0x7fffffff
0021298B  mov      r8, rcx
0021298E  mov      ecx, 1
00212993  cmove    eax, ecx
00212996  mov      dword ptr [rip + 0x1dc0d14], eax  ; -> 01FD36B0
0021299C  mov      dword ptr [r8], eax
0021299F  mov      rax, qword ptr [rip + 0x1befe2a]  ; -> 01E027D0 [u64 0x0000000001FD36C0]
002129A6  mov      ecx, dword ptr [rax]
002129A8  test     ecx, ecx
002129AA  je       0x2129ca  ; -> 002129CA
002129AC  add      rax, 8
002129B0  mov      rcx, r9
002129B3  cmp      rax, r10
002129B6  cmovb    rcx, rax
002129BA  cmp      rcx, qword ptr [rip + 0x1befe0f]  ; -> 01E027D0 [u64 0x0000000001FD36C0]
002129C1  mov      rax, rcx
002129C4  jne      0x2129a6  ; -> 002129A6
002129C6  or       eax, 0xffffffff
002129C9  ret      
002129CA  mov      ecx, dword ptr [r8]
002129CD  mov      dword ptr [rax], ecx
002129CF  lea      rcx, [rax + 8]
002129D3  mov      dword ptr [rax + 4], edx
002129D6  cmp      rcx, r10
002129D9  mov      rdx, r9
002129DC  cmovb    rdx, rcx
002129E0  sub      rax, r9
002129E3  sar      rax, 3
002129E7  mov      qword ptr [rip + 0x1befde2], rdx  ; -> 01E027D0 [u64 0x0000000001FD36C0]
002129EE  ret      
```
