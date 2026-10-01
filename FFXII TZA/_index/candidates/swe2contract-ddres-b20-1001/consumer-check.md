# Consumer check: DD batch 20 corrections on the map-screens page (SWE2-CONTRACT for OPUS, owner re-status pending, 2026-10-01)

SWE2-CONTRACT's batch 20 (this folder's README) gave the map-screens page's open-residue sentences dated pointers,
answers or stated limits. Two statements about `003BC160` are struck, both on that page; the request-router page has
no strike. No status word was moved; OPUS re-statuses after its owner read.

- **Corrects:** in the-map-screens-and-their-shared-map-data.md, (1) the section 4 row for `003BC160`: "scans kind-6
  entries for `[+0x20]`==1 ∧ `[+0x34]`==0, writes `02B457DC`=(index≠0)"; (2) the `003BC160` interior citation
  near the end of the page: "sets byte `02B457D9 = (ebx != 0)`". The bytes say the hit needs `out[+0x14]` (stack
  `+0x34`) to be non-zero (`003BC208` `cmp dword ptr [rsp + 0x34], ebp` with `ebp` = 0, `003BC20C` `jne` to the hit),
  and `003BC247` stores a dword at `02B457D8` (bytes `89 2D`), the global the page's arm-10 and arm-14 readings test.
- **Affected:** 16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the page's section 4 row and its `003BC160` interior citation | revised-here |
  | the page's arm-10 and arm-14 readings ("With `02B457D8` non-zero", "a non-zero `02B457D8`") | agrees (they name `02B457D8`); untouched |
  | 99-Unresolved-Residual/the-blinking-icon-and-its-atlas.md, the SWE2-EC7-29 update ("on `rec[+0] == 1 && rec[+0x14] == 0` it writes `02B457D8 = (i != 0)`") | disagrees on the hit test; routed to SWE2-EC7 (the update's author), untouched. Replacement: "on `rec[+0] == 1 && rec[+0x14] != 0` it writes `02B457D8 = (i != 0)`" |
  | 00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md (`[02B457D8]` on the `003C18A0` flag path) | agrees; it names `02B457D8` and makes no claim on `003BC160`'s test |
  | _index/AUDIT-LOG.md, the record-walk entry naming `003BC160` | agrees; it states the gates and the reader, not the test or the store |
  | _index/knowledge.sqlite (holds the old `02B457D9` text) | derived; routed to OPUS for the next regeneration from the pages, never hand-edited |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2contract-ddres-b20-1001/b20_checks.py (E3 rejects the
  `== 0` reading through the `jne` at `003BC20C`; E4 and E5 reject the byte-at-`02B457D9` and `02B457DC` readings
  through the store's bytes and the rip census of `02B457D8`..`02B457DF`; Z2 confirms both struck texts are kept with
  their correction notes).
  run: b20_checks.py at 61d916f19 (FAILS 0)
