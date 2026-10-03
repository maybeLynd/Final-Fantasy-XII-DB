# Homing pack: `17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-the-scripted-camera-player.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

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
