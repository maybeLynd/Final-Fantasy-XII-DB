# Consumer check: the blinking-icon page's `003BC160` hit test (SWE2-EC7 for OPUS, request OPUS-REQ-EC7-BLINKING-ICON-EQ0-1001, 2026-10-01)

OPUS asked EC7 to carry SWE2-CONTRACT's DD-batch-20 `003BC160` correction onto the blinking-icon page, whose
SWE2-EC7-29 update still carried the old `== 0` reading of the loop's hit test.

- **Corrects:** in the-blinking-icon-and-its-atlas.md, the `SWE2-EC7-29 update` sentence "on `rec[+0] == 1 &&
  rec[+0x14] == 0` it writes `02B457D8 = (i != 0)`". The bytes say the hit needs `rec[+0x14]` non-zero:
  `003BC208` is `cmp dword ptr [rsp + 0x34], ebp` with `ebp` zeroed at `003BC1DC`, and `003BC20C` `jne` goes
  to the hit. Same correction and same bytes as the map-screens page's DD-batch-20 fix.
- **Affected:** 99-Unresolved-Residual/the-blinking-icon-and-its-atlas.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the page's `SWE2-EC7-29` paragraph (the loop's hit test) | revised-here |
  | 16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md (the DD-batch-20 corrections of the same body) | agrees - already carries the corrected reading at HEAD |
  | 00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md (`[02B457D8]` on the `003C18A0` flag path) | agrees - names `02B457D8`, makes no claim on the test |
  | _index/AUDIT-LOG.md, the record-walk entry naming `003BC160` | agrees - states gates and reader, not the test |
  | _index/knowledge.sqlite (holds the old `== 0` text) | derived; regenerated from the pages, never hand-edited |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2contract-ddres-b20-1001/b20_checks.py (E3 rejects the
  `== 0` reading through the `jne` at `003BC20C`; E4/E5 pin the dword store to `02B457D8`).
  run: b20_checks.py at 61d916f19 (FAILS 0), ancestor of this publish's HEAD.
