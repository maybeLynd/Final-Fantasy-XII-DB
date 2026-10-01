# UQ-218: the selectors behind `@FMC` command `0x0B` (FABLE, Claude Opus 5.5, 2026-09-28)

affected: _index/candidates/uq218-fmc-opcode-crosswalk/README.md, 17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md

**Follows** [`uq218-fmc-opcode-crosswalk`](../uq218-fmc-opcode-crosswalk/README.md). That record left open "what `0x0B`'s
selector kinds choose by", with the list "seen: 0, 2, 0xA, 0x10, 0x20". **That list was wrong.** It came from the top five of a
histogram, not a count; the archive authors ten kinds. The list is struck in that record, with a pointer here.

[`selector_kinds.py`](selector_kinds.py) ([output](selector_kinds.out)): static from the certified image, plus the same
`.ca`/`.cm` census.

- **S1: the table.** `CharacterRenderSystem_Initialize` (`004269A0`) passes `01F000A0` to the context registrar (`0041D6E0`),
  which stores it at `02CA4668`. That is the pointer `0x0B` reads. `01F000A0` is a `.data` table of `0x30` entries
  `{1, cell}`, and kind *k*'s selector is the function in the cell. Kinds `0`, `1`, `2`, `4`, `0xA`, `0xB`, `0x10`,
  `0x20`–`0x25` and `0x2F` have their own selector; every other kind uses `005C5230`, which returns 0.
- **S2: kind `0x10` is a random countdown, read whole** (`004225A0`).
  - While record `+0x412` is `0xFF`, it draws `n = (lo − 1 + rand() mod (hi − lo + 1)) × frameLimit`.
  - `lo` and `hi` are `0x0A`'s operand bytes `+3`/`+4`, and `rand` is the CRT import.
  - `frameLimit` is the byte at `01DFE0B4`: 1 at 30 fps, 2 at 60 fps, set by the boot fixups' frame-base selector.
  - Each later call returns 0 and decrements. The call that finds 0 returns 1 and re-arms `0xFF`.
- **S3: the authored kinds.** Exactly ten are authored: `0` (782), `1` (450), `2` (643), `0xA` (700), `0xB` (7), `0x10` (1,831),
  `0x20` (1,746), `0x21` (56), `0x24` (507) and `0x25` (4), and each has its own selector.
  - Kinds `0`, `0xA` and `0xB` share `004256E0`, with argument 0, 1 or 2.
  - Kind `1` is `00422420`, a draw from `003A6E60(5)` cached at `+0x411`.
  - Kind `2` is `00422500`.
  - Kinds `0x20`, `0x21`, `0x24` and `0x25` (`00422630`, `004226C0`, `00422870`, `00422940`) each call the steering contract's
    yaw-to-point `00424370`.
- **S4: a prediction from S2's divisor.** Every authored kind-`0x10` command has `lo ≤ hi`. The ranges are (2, 4) ×792,
  (4, 6) ×608, (1, 2) ×429 and (6, 12) ×2.
- **C: controls.** Kinds 5–9 bind to `005C5230`, and none is authored. The S3 comparison failed on its first run against the
  wrong five-kind list, so it is sensitive to the list.

**Writers.** The tools' `ripstores.py` sweep over `01F00090`–`01F00410` finds no rip-relative store to the table or its
cells. The same sweep over `01DFE0B4` finds the frame-limit writer (`001EDDC0` stores 2), which is the positive control.
The sweep cannot see image-base-relative or aliased stores.

**Still open, exactly.**
- ~~What kinds `0`, `0xA` and `0xB` decide by~~ — resolved by `classifier.md` (`004256E0`, FAILS 0).
- ~~What kind `1` draws from~~ — `003A6E60(5)` is the shared bounded draw; kind-1's `00422420` body is read
  end-to-end in `criteria.md` (arm timer `+0x40E`, drawn variant `+0x411`, evaded +5 at `11 × frameLimit`).
- ~~Where the kind-1/2 state bytes are reset~~ — the state record is `qword[ctx+0x2E0]` (pool `0xA0 × 0x740` at
  `[02B3EF28]`); resets at record init `0041F730` and per-`@FMC`-bind `004252A7` — see `criteria.md`.
- What kinds `0x20`/`0x21`/`0x24`/`0x25` decide by. They query the battle unit's view request
  (`002ED500` → `0031B4B0` → `0031ADB0`) with queries `0x30` and `4`, whose results were not read.
- Which sign of the yaw is the character's left; the exact `004256E0` band→`@FMN`-name binding.

These sub-questions belong to UQ-218's `@FMC` residue.

| consumer | action | agreement |
|---|---|---|
| `uq218-fmc-opcode-crosswalk/README.md`, "seen: 0, 2, 0xA, 0x10, 0x20" | struck; ten kinds, pointer here | revised-here |
| the handler page's new section, "what each selector kind chooses by … was not read" | struck; the selector table, kind `0x10`, the families | revised-here |
| FABLE-REQ-DATA-UQ218-FMC-CROSSWALK (asked DATA to narrow to "what `0x0B`'s selector kinds choose by") | the narrowing now names the unread callees above | routed-to-SWE2-DATA |

Regression: `selector_kinds.py` (S1–S4, C). run: selector_kinds.py at c57c75ac8, FAILS 0.
