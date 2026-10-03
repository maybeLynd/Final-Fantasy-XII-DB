# Homing pack: `17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-fcp-character-parameter-block.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003B4750 (30 B, extent 003B4750-003B476E)

Entered from (direct sites whose caller this page cites): `0042CBF0` + 0x130 (call; `0042CBF0` is cited on this page)
Other direct sites: none

Host context: "t is the record's '+0x300', read by four accessors, '003E6680' (from '00425DC0'), '003E66D0' (from '00425E10'),       '003E6710' (from '0041FCF0' and '00520140') and '003E6D40' (from the LOD updates '0042CBF0' and '0042D050', and from       '00421280' and '004213E0').)*       *(2026-09-30, SWE2-STRUCT for OPUS, residue 3: answered. The copy's readers are the six '0051Cxxx'/'0051Dxxx'       routines listed under "Section 8" at the end of"

```
003B4750  sub      rsp, 0x28
003B4754  mov      rdx, qword ptr [rip + 0x1c2031d]  ; -> 01FD4A78
003B475B  call     0x3b4a50  ; -> 003B4A50 fn
003B4760  xor      ecx, ecx
003B4762  test     eax, eax
003B4764  setne    cl
003B4767  mov      eax, ecx
003B4769  add      rsp, 0x28
003B476D  ret      
```

## 004096F0 (29 B, extent 004096F0-0040970D)

Entered from (direct sites whose caller this page cites): `004292B0` + 0xB0 (call; `004292B0` is cited on this page)
Other direct sites: none

Host context: "s declare it instead of '0x104'. '0x106' ('+0x3E') is the shadow's second anchor, and it is bone 0, the root, in every block)* | | '+0x2C'–'+0x31' event map | '0041E5B0(record, state, eventId)' from '004292B0' ('004292D8'–'0042931E'): the index 'i' of the matching byte selects animation '[record + 0x2FA] + i' of the model container's own '@FMC' motion entry ('+0x2F8' = the model resource id '+0x408', '+0x2FA' = its first '@FMC' entry in"

```
004096F0  mov      edx, dword ptr [rcx + 4]
004096F3  test     edx, edx
004096F5  je       0x409704  ; -> 00409704
004096F7  cmp      edx, 1
004096FA  jne      0x409701  ; -> 00409701
004096FC  mov      rax, qword ptr [rcx + 0x30]
00409700  ret      
00409701  xor      eax, eax
00409703  ret      
00409704  add      rcx, 0x10
00409708  jmp      0x6b5c70  ; -> 006B5C70 fn
```
