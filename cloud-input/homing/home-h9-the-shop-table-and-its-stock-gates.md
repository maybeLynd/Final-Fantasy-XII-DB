# Homing pack: `12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md`

Generated 2026-10-03 11:24 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h9-the-shop-table-and-its-stock-gates.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002CCA30 (9 B, extent 002CCA30-002CCA39)

Entered from (direct sites whose caller this page cites): `0027F030` + 0xAB (call; `0027F030` is cited on this page)
Other direct sites: none

Host context: "erior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*  | function | size | what the body does | interior anchors | |---|---|---|---| | '0027F030' | 282 B | starts a result at 0; when 'r9d' is 0 and the fifth (stack) argument is not 1 and '002CCA10(r8d)' is non-zero, it calls '0027F030'+0x51('edx') and sets the result to 4 when '0027F030'+0x5F(that value, word '+0xd68' of qw"

```
002CCA30  xor      eax, eax
002CCA32  cmp      ecx, 0x12
002CCA35  sete     al
002CCA38  ret      
```
