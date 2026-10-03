# Homing pack: `16-UI/the-selection-the-menu-publishes.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-selection-the-menu-publishes.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00270F50 (11 B, extent 00270F50-00270F5B)

Entered from (direct sites whose caller this page cites): `003F6370` + 0x192 (call; `003F6370` is cited on this page)
Other direct sites: none

Host context: "time' '00291320' reaches '0024A5A0'/'00271140'/ '00273A30'/'00275550' (4 edges); the input-consumer state machines '002BAF80'/'002B7B80' reach '001EDEC0'/'00249C60'/'00275440'; '003F1A60'/'003F5100'/'003F6370'/'003F7200' share '00203080'/ '002703F0'/'002E9D10'; '00506700' shares '0024A5A0'/'002B58B0'/'0035D330'; '00183280' is reached by '00559540'/'0057A1F0'/'00561BE0'/'003F1530'; ShaderMaterial '00366B80' shares '001EDEC0'/'0024A5A0'. "

```
00270F50  mov      r9d, 0x10
00270F56  jmp      0x270f60  ; -> 00270F60 fn
```

## 0039C100 (18 B, extent 0039C100-0039C112)

Entered from (direct sites whose caller this page cites): `0027E530` + 0x188 (call; `0027E530` is cited on this page)
Other direct sites: none

Host context: " kind 1, the top command list; FABLE, reviewed ACCEPT-WITH-NARROWING by SWE2-AUDIT-SEM, C1 and N1 applied) are answered; the dispatch jump table (0027E384, twenty command kinds) walked 2026-09-18 and 0027E530 identified as one of its five installed procedures (owner re-status 2026-10-01, OPUS; documented_rule READY)   # <- corrected 2026-10-02, OPUS - six installed procedures, not five: 0027E050's lea sites name 00276BE0, 0027D240, 0027"

```
0039C100  movsxd   rax, dword ptr [rip + 0x275278d]  ; -> 02AEE894
0039C107  lea      rcx, [rip + 0x275278a]  ; -> 02AEE898
0039C10E  mov      eax, dword ptr [rcx + rax*4]
0039C111  ret      
```

## 0039C120 (36 B, extent 0039C120-0039C144)

Entered from (direct sites whose caller this page cites): `0027E530` + 0x196 (call; `0027E530` is cited on this page)
Other direct sites: none

Host context: " kind 1, the top command list; FABLE, reviewed ACCEPT-WITH-NARROWING by SWE2-AUDIT-SEM, C1 and N1 applied) are answered; the dispatch jump table (0027E384, twenty command kinds) walked 2026-09-18 and 0027E530 identified as one of its five installed procedures (owner re-status 2026-10-01, OPUS; documented_rule READY)   # <- corrected 2026-10-02, OPUS - six installed procedures, not five: 0027E050's lea sites name 00276BE0, 0027D240, 0027"

```
0039C120  mov      eax, 1
0039C125  cmp      ecx, eax
0039C127  cmovge   eax, ecx
0039C12A  mov      ecx, 0x1a
0039C12F  cmp      eax, ecx
0039C131  cmovg    eax, ecx
0039C134  dec      eax
0039C136  movsxd   rcx, eax
0039C139  lea      rax, [rip + 0x2752758]  ; -> 02AEE898
0039C140  mov      eax, dword ptr [rax + rcx*4]
0039C143  ret      
```

## 003F3080 (20 B, extent 003F3080-003F3094)

Entered from (direct sites whose caller this page cites): `002907F0` + 0x30 (call; `002907F0` is cited on this page)
Other direct sites: none

Host context: "00277329' | '002D8BB0', '0029F5D0' ×5, '00229DF0', '00229E70' — the largest arm (~1.2 KB) | | 6 | '00276E14' | leaf (17 B) | | 15 | '00276E25' | '00368A50', '00290CD0' ×2, '003C94F0' ×2, '0035C080', '002907F0', '00275440' | | 18 | '00276F27' | '0028F800', '00296B80', '00275440' ×2 | | 21 | '00276EEA' | indirect 'call rax' — a vtable-style call | | 39 | '002770AB' | '00275440', '0035BB50', '0035C430', '0020E620' | | 46 | '0027780D' | lea"

```
003F3080  test     edx, edx
003F3082  je       0x3f308c  ; -> 003F308C
003F3084  or       byte ptr [rcx + 0x991], 8
003F308B  ret      
003F308C  and      byte ptr [rcx + 0x991], 0xf7
003F3093  ret      
```
