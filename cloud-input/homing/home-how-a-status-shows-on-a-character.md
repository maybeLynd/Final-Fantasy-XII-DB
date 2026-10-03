# Homing pack: `17-Presentation-Rendering/Character-Render-Records/how-a-status-shows-on-a-character.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-how-a-status-shows-on-a-character.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 004700C0 (23 B, extent 004700C0-004700D7)

Entered from (direct sites whose caller this page cites): `003E7500` + 0x7B (call; `003E7500` is cited on this page)
Other direct sites: none

Host context: "oss-reference, not a claim.  **Movement - CLIENT (SWE2-EC7, batch 166).** '001F1590' — a body this page's EC7-109 section measures — is reached from Movement's '003ED190'/'003ED3F0', and batch-166's '003E7500' (the '02B59D80' slot init) is reached from '002E28E0' on that layer; movement bodies consult the status-show machinery, not a shared responsibility.  ## SWE2-EC7-43 update (2026-09-19) - '00470660'  '00470660' (280 B) is the Berse"

```
004700C0  xor      eax, eax
004700C2  mov      dword ptr [rcx + 4], 0xffff
004700C9  mov      dword ptr [rcx], eax
004700CB  mov      qword ptr [rcx + 8], rax
004700CF  mov      qword ptr [rcx + 0x18], rax
004700D3  mov      dword ptr [rcx + 0x10], edx
004700D6  ret      
```

## 0051E140 (39 B, extent 0051E140-0051E167)

Entered from (direct sites whose caller this page cites): `003E7500` + 0x90 (jmp; `003E7500` is cited on this page)
Other direct sites: none

Host context: "oss-reference, not a claim.  **Movement - CLIENT (SWE2-EC7, batch 166).** '001F1590' — a body this page's EC7-109 section measures — is reached from Movement's '003ED190'/'003ED3F0', and batch-166's '003E7500' (the '02B59D80' slot init) is reached from '002E28E0' on that layer; movement bodies consult the status-show machinery, not a shared responsibility.  ## SWE2-EC7-43 update (2026-09-19) - '00470660'  '00470660' (280 B) is the Berse"

```
0051E140  xor      eax, eax
0051E142  mov      dword ptr [rcx], edx
0051E144  mov      dword ptr [rcx + 0x10], eax
0051E147  mov      qword ptr [rcx + 0x28], rax
0051E14B  mov      qword ptr [rcx + 0x40], rax
0051E14F  mov      byte ptr [rcx + 0x33], al
0051E152  mov      word ptr [rcx + 0x19], 0xff
0051E158  mov      byte ptr [rcx + 0x18], 0xff
0051E15C  mov      word ptr [rcx + 0x31], 0xff
0051E162  mov      byte ptr [rcx + 0x30], 0xff
0051E166  ret      
```
