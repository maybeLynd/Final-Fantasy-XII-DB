# Homing pack: `00-Engine-Core-Runtime/the-encoded-id-class-registry.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-encoded-id-class-registry.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00243EE0 (133 B, extent 00243EE0-00243F65)

Entered from (direct sites whose caller this page cites): `002C4720` + 0x8D5 (call; `002C4720` is cited on this page)
Other direct sites: none

Host context: "-static-census-0930'](../_index/candidates/rc1-static-census-0930/README.md), commit 'fe5dec46e'):** every remaining   source was read to its end — '002CFEE0' / '002D0100' pass class 1, '002C38B0' / '002C4720' class 2, '0057DAD0''s   six sites classes 5, 7 and 13, '0035E070' class 1, and the six MULTI sites resolve path by path — and the four entry   points ('00322C50', '0031C5D0', '0035D330', '0035D380') have no 8-byte pointer anywhere"

```
00243EE0  xor      r8d, r8d
00243EE3  mov      r11, rcx
00243EE6  test     dword ptr [rcx], 0x3fffc
00243EEC  jbe      0x243f3e  ; -> 00243F3E
00243EEE  mov      r9d, r8d
00243EF1  mov      rax, qword ptr [r11 + 0x10]
00243EF5  mov      rdx, qword ptr [r9 + rax]
00243EF9  mov      eax, dword ptr [rdx + 8]
00243EFC  shr      eax, 2
00243EFF  and      eax, 0xf
00243F02  sub      eax, 2
00243F05  je       0x243f16  ; -> 00243F16
00243F07  sub      eax, 3
00243F0A  je       0x243f16  ; -> 00243F16
00243F0C  sub      eax, 3
00243F0F  je       0x243f3f  ; -> 00243F3F
00243F11  cmp      eax, 1
00243F14  jne      0x243f29  ; -> 00243F29
00243F16  mov      rcx, qword ptr [rdx]
00243F19  movzx    eax, word ptr [rcx + 4]
00243F1D  mov      word ptr [rdx + 0xc], ax
00243F21  movzx    eax, word ptr [rcx + 6]
00243F25  mov      word ptr [rdx + 0xe], ax
00243F29  mov      eax, dword ptr [r11]
00243F2C  inc      r8d
00243F2F  shr      eax, 2
00243F32  add      r9, 8
00243F36  movzx    eax, ax
00243F39  cmp      r8d, eax
00243F3C  jb       0x243ef1  ; -> 00243EF1
00243F3E  ret      
00243F3F  mov      rax, qword ptr [rdx]
00243F42  mov      rcx, qword ptr [rdx + 0x18]
00243F46  movsx    r10d, word ptr [rax + 6]
00243F4B  test     rcx, rcx
00243F4E  je       0x243f29  ; -> 00243F29
00243F50  movzx    eax, word ptr [rax + 4]
00243F54  mov      word ptr [rcx + 0x98], ax
00243F5B  mov      word ptr [rcx + 0x9a], r10w
00243F63  jmp      0x243f29  ; -> 00243F29
```

## 002CFDA0 (146 B, extent 002CFDA0-002CFE32)

Entered from (direct sites whose caller this page cites): `002D0100` + 0x73 (call; `002D0100` is cited on this page)
Other direct sites: `002CFD30` + 0x4A (call); `002CFFE0` + 0x35 (jmp)

Host context: "n OPUS's static census, record   ['rc1-static-census-0930'](../_index/candidates/rc1-static-census-0930/README.md), commit 'fe5dec46e'):** every remaining   source was read to its end — '002CFEE0' / '002D0100' pass class 1, '002C38B0' / '002C4720' class 2, '0057DAD0''s   six sites classes 5, 7 and 13, '0035E070' class 1, and the six MULTI sites resolve path by path — and the four entry   points ('00322C50', '0031C5D0', '0035D330', '0035"

```
002CFDA0  mov      qword ptr [rsp + 8], rbx
002CFDA5  mov      qword ptr [rsp + 0x10], rbp
002CFDAA  mov      qword ptr [rsp + 0x18], rsi
002CFDAF  push     rdi
002CFDB0  sub      rsp, 0x20
002CFDB4  mov      rbp, rdx
002CFDB7  mov      rsi, rcx
002CFDBA  movzx    edx, word ptr [rcx]
002CFDBD  mov      ecx, 1
002CFDC2  shl      edx, 0x10
002CFDC5  movzx    ebx, word ptr [rbp]
002CFDC9  call     0x35d330  ; -> 0035D330 fn
002CFDCE  shl      ebx, 0x10
002CFDD1  mov      ecx, 1
002CFDD6  mov      edx, ebx
002CFDD8  mov      edi, dword ptr [rax + 0x38]
002CFDDB  call     0x35d330  ; -> 0035D330 fn
002CFDE0  sub      edi, dword ptr [rax + 0x38]
002CFDE3  jne      0x2cfe1b  ; -> 002CFE1B
002CFDE5  movzx    esi, word ptr [rsi]
002CFDE8  mov      ecx, 1
002CFDED  movzx    edi, word ptr [rbp]
002CFDF1  mov      edx, esi
002CFDF3  shl      edx, 0x10
002CFDF6  call     0x35d330  ; -> 0035D330 fn
002CFDFB  mov      edx, edi
002CFDFD  mov      ecx, 1
002CFE02  shl      edx, 0x10
002CFE05  mov      ebx, dword ptr [rax + 0x30]
002CFE08  call     0x35d330  ; -> 0035D330 fn
002CFE0D  sub      esi, edi
002CFE0F  sub      ebx, dword ptr [rax + 0x30]
002CFE12  test     ebx, ebx
002CFE14  cmovne   esi, ebx
002CFE17  mov      eax, esi
002CFE19  jmp      0x2cfe1d  ; -> 002CFE1D
002CFE1B  mov      eax, edi
002CFE1D  mov      rbx, qword ptr [rsp + 0x30]
002CFE22  mov      rbp, qword ptr [rsp + 0x38]
002CFE27  mov      rsi, qword ptr [rsp + 0x40]
002CFE2C  add      rsp, 0x20
002CFE30  pop      rdi
002CFE31  ret      
```

## 002D01A0 (82 B, extent 002D01A0-002D01F2)

Entered from (direct sites whose caller this page cites): `002CFEE0` + 0xA2 (call; `002CFEE0` is cited on this page)
Other direct sites: none

Host context: "2-CONTRACT, on OPUS's static census, record   ['rc1-static-census-0930'](../_index/candidates/rc1-static-census-0930/README.md), commit 'fe5dec46e'):** every remaining   source was read to its end — '002CFEE0' / '002D0100' pass class 1, '002C38B0' / '002C4720' class 2, '0057DAD0''s   six sites classes 5, 7 and 13, '0035E070' class 1, and the six MULTI sites resolve path by path — and the four entry   points ('00322C50', '0031C5D0', '003"

```
002D01A0  mov      qword ptr [rsp + 8], rbx
002D01A5  mov      qword ptr [rsp + 0x10], rsi
002D01AA  push     rdi
002D01AB  sub      rsp, 0x20
002D01AF  movzx    esi, word ptr [rcx]
002D01B2  mov      ecx, 1
002D01B7  movzx    edi, word ptr [rdx]
002D01BA  mov      edx, esi
002D01BC  shl      edx, 0x10
002D01BF  call     0x35d330  ; -> 0035D330 fn
002D01C4  mov      edx, edi
002D01C6  mov      ecx, 1
002D01CB  shl      edx, 0x10
002D01CE  mov      ebx, dword ptr [rax + 0x30]
002D01D1  call     0x35d330  ; -> 0035D330 fn
002D01D6  sub      esi, edi
002D01D8  sub      ebx, dword ptr [rax + 0x30]
002D01DB  test     ebx, ebx
002D01DD  cmovne   esi, ebx
002D01E0  mov      rbx, qword ptr [rsp + 0x30]
002D01E5  mov      eax, esi
002D01E7  mov      rsi, qword ptr [rsp + 0x38]
002D01EC  add      rsp, 0x20
002D01F0  pop      rdi
002D01F1  ret      
```
