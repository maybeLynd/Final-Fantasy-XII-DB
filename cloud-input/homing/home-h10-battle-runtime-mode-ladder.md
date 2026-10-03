# Homing pack: `00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-battle-runtime-mode-ladder.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0031E860 (31 B, extent 0031E860-0031E87F)

Entered from (direct sites whose caller this page cites): `00313DB0` + 0xB3 (call; `00313DB0` is cited on this page)
Other direct sites: `00303E90` + 0x15 (jmp); `00313590` + 0x15 (jmp)

Host context: "unowned; its consumers span seven subsystems status: AUDITED — the ladder and its six modes read (O-4 answered 2026-09-12: summon, chocobo, the field bit, the two event-party modes); the 0035BC50 and 00313DB0 sections' lists are all ticked; status line brought up to date 2026-09-18 (FABLE) evidence_tier: 1 verified_against:   gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9   transfers_to:     parent: 59629b9"

```
0031E860  sub      rsp, 0x28
0031E864  call     0x263750  ; -> 00263750 fn
0031E869  test     rax, rax
0031E86C  jne      0x31e873  ; -> 0031E873
0031E86E  add      rsp, 0x28
0031E872  ret      
0031E873  mov      rcx, rax
0031E876  add      rsp, 0x28
0031E87A  jmp      0x3589b0  ; -> 003589B0 fn
```

## 00422E40 (11 B, extent 00422E40-00422E4B)

Entered from (direct sites whose caller this page cites): `0042DF10` + 0x92 (jmp; `0042DF10` is cited on this page)
Other direct sites: none

Host context: "nterior anchor '002970DF' (function '002970C0').  '00429F70' (223 B) is the recursive record walk '00427DE0' runs over the '022C6F28' '0x740'-stride table: from 'rcx''s u16 head index ('-1' ends) it '0042DF10'-visits each record into a stack out-pair, then recurses through '0042EF90' on the '+8' and '+0xA' u16 links - a depth-first sweep of the chain with the caller's '+0x308' float carried in the out record  Interior anchor '00429FD0' "

```
00422E40  mov      r8d, 1
00422E46  jmp      0x424870  ; -> 00424870 fn
```
