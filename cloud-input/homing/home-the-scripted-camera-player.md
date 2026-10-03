# Homing pack: `17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-scripted-camera-player.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00264CE0 (56 B, extent 00264CE0-00264D18)

Entered from (direct sites whose caller this page cites): `0033F7F0` + 0x21 (call; `0033F7F0` is cited on this page)
Other direct sites: none

Host context: " no shared ownership. - **Script_VM_Native_Bridge - CLIENT and SERVICE (112 edges).** '00203170', '00255C20', '00255CB0', '00257800' (+20 more) are called by bodies filed to Script_VM_Native_Bridge: '0033F7F0', '0033FD60', '00341AB0', '00342490' (+71 more); '003442D0', '00349FA0', '0034E9B0', '0034EDB0' (+13 more) reach bodies filed to Script_VM_Native_Bridge: VMValueStack_PopNumericDiscard ('00267DB0'), VMValueStack_PopInt32CoerceFloat"

```
00264CE0  test     rcx, rcx
00264CE3  je       0x264d10  ; -> 00264D10
00264CE5  mov      rax, qword ptr [rcx]
00264CE8  test     rax, rax
00264CEB  je       0x264d10  ; -> 00264D10
00264CED  cmp      edx, -1
00264CF0  jne      0x264cf6  ; -> 00264CF6
00264CF2  movsx    edx, word ptr [rax + 0x52]
00264CF6  cmp      edx, -2
00264CF9  jne      0x264cff  ; -> 00264CFF
00264CFB  movsx    edx, word ptr [rax + 0x78]
00264CFF  cmp      edx, -3
00264D02  jne      0x264d08  ; -> 00264D08
00264D04  movsx    edx, word ptr [rax + 0x7a]
00264D08  test     edx, edx
00264D0A  jns      0x264d10  ; -> 00264D10
00264D0C  movsx    edx, word ptr [rax + 0x52]
00264D10  xor      eax, eax
00264D12  test     edx, edx
00264D14  cmovns   eax, edx
00264D17  ret      
```

## 004092A0 (89 B, extent 004092A0-004092F9)

Entered from (direct sites whose caller this page cites): `00373640` + 0x83 (jmp; `00373640` is cited on this page)
Other direct sites: `003736D0` + 0xA8 (call)

Host context: "eter halver  '003710E0' (239 B) resolves '[rcx+0x84]' through '0020E600', indexes 'edx' by '0x290' stride, and when 'r9' supplies an output record: 'edi-1' mode selects — mode 1 ('[rsi+0x9C]==2' via '00373640', else 0.0) adds 'xmm0' to '[rbx]' then halves '[rbx]'/'[rbx+4]'/'[rbx+8]'; mode 2 runs the same halve on the '00373640' result alone. Interior anchor '0037110A' (the 'imul 0x290'). ## SWE2-EC7-31 update (2026-09-18) — '0025A500' c"

```
004092A0  cmp      dword ptr [rcx + 4], 2
004092A4  je       0x4092ab  ; -> 004092AB
004092A6  xor      r8d, r8d
004092A9  jmp      0x4092b2  ; -> 004092B2
004092AB  mov      r8d, dword ptr [rcx + 0x34]
004092AF  add      r8d, ecx
004092B2  lea      rax, [rdx + 8]
004092B6  mov      edx, dword ptr [rdx + 4]
004092B9  bt       edx, 0x1e
004092BD  lea      rcx, [rax + 2]
004092C1  cmovae   rcx, rax
004092C5  test     edx, edx
004092C7  lea      r9, [rcx + 2]
004092CB  cmovns   r9, rcx
004092CF  mov      ecx, edx
004092D1  and      ecx, 0x200100
004092D7  bt       edx, 0x16
004092DB  jae      0x4092f5  ; -> 004092F5
004092DD  cmp      ecx, 0x200100
004092E3  lea      rax, [r9 + 0x20]
004092E7  cmovne   rax, r9
004092EB  movzx    eax, word ptr [rax]
004092EE  movss    xmm0, dword ptr [r8 + rax*4]
004092F4  ret      
004092F5  xorps    xmm0, xmm0
004092F8  ret      
```
