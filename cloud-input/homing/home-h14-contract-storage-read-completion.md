# Homing pack: `19-Save-Load-Settings/CONTRACT-storage-read-completion.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-contract-storage-read-completion.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003BB2F0 (48 B, extent 003BB2F0-003BB320)

Entered from (direct sites whose caller this page cites): `00582040` + 0x1B8 (call; `00582040` is cited on this page)
Other direct sites: none

Host context: ", and no live short read was observed. - ~~The callback token/override handling is **ASTRA's reading**, carried forward~~ —   **fully re-derived 2026-09-18.** 'SaveStorageQueue_StartFrontOperation' ('00582040') is   a 13-arm dispatch on 'dword[+0xD8]' (table '0x46220C'), gated three ways before it: null,   '[+0x398]==0', and '+0xDC' bit 0 (the "already started" flag every live arm sets at   '005820BD'). Arm 1 is the only one that touche"

```
003BB2F0  xor      eax, eax
003BB2F2  mov      dword ptr [rip + 0x2785b20], 7  ; -> 02B40E1C
003BB2FC  xor      ecx, ecx
003BB2FE  mov      dword ptr [rip + 0x2785bbc], eax  ; -> 02B40EC0
003BB304  mov      dword ptr [rip + 0x2785b0e], eax  ; -> 02B40E18
003BB30A  mov      dword ptr [rip + 0x2785cd4], eax  ; -> 02B40FE4
003BB310  mov      qword ptr [rip + 0x2785af5], 1  ; -> 02B40E10
003BB31B  jmp      0x3ba5f0  ; -> 003BA5F0 fn
```
