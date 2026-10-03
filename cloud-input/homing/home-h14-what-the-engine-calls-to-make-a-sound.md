# Homing pack: `18-Audio/Audio-Boundary/what-the-engine-calls-to-make-a-sound.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-what-the-engine-calls-to-make-a-sound.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00379E60 (43 B, extent 00379E60-00379E8B)

Entered from (direct sites whose caller this page cites): `00379E30` + 0x8 (call; `00379E30` is cited on this page); `00379E30` + 0x1F (call; `00379E30` is cited on this page)
Other direct sites: none

Host context: "8DC45' (an '00202C70' call).  ## SWE2-EC7-40 update (2026-09-19) - '003DEC90'  '003DEC90' (375 B) is a sound-call body - '02B59360'/'02B59C20', '0032E520'/'0035EA30'/'003697F0' pairs plus '002DEE90'/'00379E30'/'003DEB30'. Interior anchor '003DECEF' (a '002DEE90' call).  ## SWE2-EC7-42 update (2026-09-19) - '003F12E0'  '003F12E0' (324 B) is a sound-call body - '01F44830', '00271140'/'00808C40'. Interior anchor '003F13DC' (a '00271140' ca" / "8DC45' (an '00202C70' call).  ## SWE2-EC7-40 update (2026-09-19) - '003DEC90'  '003DEC90' (375 B) is a sound-call body - '02B59360'/'02B59C20', '0032E520'/'0035EA30'/'003697F0' pairs plus '002DEE90'/'00379E30'/'003DEB30'. Interior anchor '003DECEF' (a '002DEE90' call).  ## SWE2-EC7-42 update (2026-09-19) - '003F12E0'  '003F12E0' (324 B) is a sound-call body - '01F44830', '00271140'/'00808C40'. Interior anchor '003F13DC' (a '00271140' ca"

```
00379E60  test     ecx, ecx
00379E62  je       0x379e7e  ; -> 00379E7E
00379E64  mov      eax, ecx
00379E66  lea      r8, [rip + 0x276332b]  ; -> 02ADD198
00379E6D  and      eax, 0xf
00379E70  imul     rdx, rax, 0x70
00379E74  xor      eax, eax
00379E76  cmp      dword ptr [rdx + r8], ecx
00379E7A  sete     al
00379E7D  ret      
00379E7E  xor      eax, eax
00379E80  cmp      qword ptr [rip + 0x27639e9], rax  ; -> 02ADD870
00379E87  setne    al
00379E8A  ret      
```
