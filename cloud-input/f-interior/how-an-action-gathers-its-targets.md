# F-interior pack: `07-Combat-Action/how-an-action-gathers-its-targets.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/how-an-action-gathers-its-targets.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

## 002FFED0 (23 B, extent 002FFED0-002FFEE7)

Page context: "   last_pass: 2026-09-29   last_pass_kind: falsification   last_pass_state: opus-action-targets-falsification-pass-1   note: written by FABLE while placing two of FRONTIER's uncited bodies (0030BB10, 002FFED0). Static plus one data     census. Corrects my own 2026-09-18 sentence on the action-row page that the flag-word immediates 0x200000 and     0x3000000 "are not the action row's" - they are, and this routine is where they are read. "

```
002FFED0  sub      rsp, 0x28
002FFED4  call     0x2fff50  ; -> 002FFF50 fn
002FFED9  xor      ecx, ecx
002FFEDB  test     eax, eax
002FFEDD  sete     cl
002FFEE0  mov      eax, ecx
002FFEE2  add      rsp, 0x28
002FFEE6  ret      
```
