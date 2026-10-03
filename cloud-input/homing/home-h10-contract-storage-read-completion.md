# Homing pack: `19-Save-Load-Settings/CONTRACT-storage-read-completion.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-contract-storage-read-completion.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003688A0 (59 B, extent 003688A0-003688DB)

Entered from (direct sites whose caller this page cites): `002D3BA0` + 0x6AB (call; `002D3BA0` is cited on this page)
Other direct sites: none

Host context: "(=3) with 'word[rsi+0xE8] <= 0xC' reduces the step to 'delta / |delta|' (±1); positive arms bit '0x10', negative bit '0x40', on 'ebp'/'r14d'. Each of '|delta|' steps runs '002D0580(rsi, delta)' then '002D3BA0(rsi, ebp, r14, r12, 0, delta)' then '002D4F10(rsi, delta)' — either non-zero aborts the loop; the no-delta path runs '002D3BA0' once with the raw triple. Interior anchor '002D39E2' (the in-loop 'call 002D3BA0' commit).  ## SWE2-EC7"

```
003688A0  test     byte ptr [rip + 0x1f6358b], 0x10  ; -> 022CBE32
003688A7  je       0x3688da  ; -> 003688DA
003688A9  cmp      ecx, -1
003688AC  mov      word ptr [rip + 0x1f6358c], 0x406  ; -> 022CBE41
003688B5  mov      eax, 2
003688BA  mov      byte ptr [rip + 0x1f63582], 0x1e  ; -> 022CBE43
003688C1  cmove    ecx, eax
003688C4  mov      byte ptr [rip + 0x1f63572], 1  ; -> 022CBE3D
003688CB  xor      eax, eax
003688CD  mov      byte ptr [rip + 0x1f6356d], cl  ; -> 022CBE40
003688D3  mov      word ptr [rip + 0x1f63564], ax  ; -> 022CBE3E
003688DA  ret      
```

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

## 003BB380 (38 B, extent 003BB380-003BB3A6)

Entered from (direct sites whose caller this page cites): `00582040` + 0x1C2 (call; `00582040` is cited on this page)
Other direct sites: `0050C5E0` + 0x0 (jmp)

Host context: ", and no live short read was observed. - ~~The callback token/override handling is **ASTRA's reading**, carried forward~~ —   **fully re-derived 2026-09-18.** 'SaveStorageQueue_StartFrontOperation' ('00582040') is   a 13-arm dispatch on 'dword[+0xD8]' (table '0x46220C'), gated three ways before it: null,   '[+0x398]==0', and '+0xDC' bit 0 (the "already started" flag every live arm sets at   '005820BD'). Arm 1 is the only one that touche"

```
003BB380  xor      eax, eax
003BB382  mov      dword ptr [rip + 0x2785a90], 3  ; -> 02B40E1C
003BB38C  mov      dword ptr [rip + 0x2785b2e], eax  ; -> 02B40EC0
003BB392  mov      dword ptr [rip + 0x2785c4c], eax  ; -> 02B40FE4
003BB398  mov      qword ptr [rip + 0x2785a75], rax  ; -> 02B40E14
003BB39F  mov      dword ptr [rip + 0x2785a6b], eax  ; -> 02B40E10
003BB3A5  ret      
```

## 003BB3B0 (38 B, extent 003BB3B0-003BB3D6)

Entered from (direct sites whose caller this page cites): `00582040` + 0xC9 (call; `00582040` is cited on this page)
Other direct sites: `0050C950` + 0x0 (jmp)

Host context: ", and no live short read was observed. - ~~The callback token/override handling is **ASTRA's reading**, carried forward~~ —   **fully re-derived 2026-09-18.** 'SaveStorageQueue_StartFrontOperation' ('00582040') is   a 13-arm dispatch on 'dword[+0xD8]' (table '0x46220C'), gated three ways before it: null,   '[+0x398]==0', and '+0xDC' bit 0 (the "already started" flag every live arm sets at   '005820BD'). Arm 1 is the only one that touche"

```
003BB3B0  xor      eax, eax
003BB3B2  mov      dword ptr [rip + 0x2785a60], 4  ; -> 02B40E1C
003BB3BC  mov      dword ptr [rip + 0x2785afe], eax  ; -> 02B40EC0
003BB3C2  mov      dword ptr [rip + 0x2785c1c], eax  ; -> 02B40FE4
003BB3C8  mov      qword ptr [rip + 0x2785a45], rax  ; -> 02B40E14
003BB3CF  mov      dword ptr [rip + 0x2785a3b], eax  ; -> 02B40E10
003BB3D5  ret      
```
