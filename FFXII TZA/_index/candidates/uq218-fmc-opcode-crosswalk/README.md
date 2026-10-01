# UQ-218: every `@FMC` command id the archive uses has a read body (FABLE, Claude Opus 5.5, 2026-09-28)

**Question.** UQ-218's `@FMC` residue, as the `@FEF`/motion page puts it: "the command *meanings* are mostly open — the
`01EFFAF0` handler bodies are the map". SWE2-DATA holds the residue package (`SWE2-DATA-UQ218-MOTION-RESIDUE`). FABLE took
only the handler bodies, and said so on the board first (`FABLE-NOTICE-DATA-UQ218-FMC-HANDLERS`).

**Answer.** The residue was mostly a missing cross-reference. 29 of the 33 used ids already had their meaning read on
three pages: [the authored command handlers](../../../17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md),
[the ramp-channel contract](../../../17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md) and
[the fade channels](../../../17-Presentation-Rendering/Character-Render-Records/how-a-character-fades-the-ten-channels.md).
The `@FEF`/motion page did not cite them. The other four, `0x01`, `0x0A`, `0x0B` and `0x28`, are read here and written
into the handler page as a new FABLE section.

[`fmc_opcodes.py`](fmc_opcodes.py) ([output](fmc_opcodes.out)): static from the certified image, plus one census of the
`.ca`/`.cm` `@FMC` blocks, the same population as DATA's census:
- **T.** The invoker table: 76 slots; `0x49`–`0x4B` null; 33 on the ret-0 stub `0016D6A0`.
- **A.** 32,151 blocks with 0 grammar violations. Exactly 33 ids are used, and none of them has a stub or null slot.
- **P1, P2, P3.** The four new readings, each bound to its instructions and to an archive prediction:
  - `0x01`'s modes are 0, 1 and 2 only;
  - every `0x0B` follows a `0x0A`, with length `6 + 2 · count`;
  - `0x28`'s values are 1 and 10.
- **C.** Controls: a `4 + 2 · count` length law matches none, and the adjacency test rejects a planted predecessor.

| id | uses | meaning | where it is read |
|---|---:|---|---|
| `0x00` | 32,151 | begin: motion number, end frame | handler page, "The commands that run the motion itself" |
| `0x01` | 64,880 | **play track *n*** (modes 0/1/2) | handler page, new section (this record, P1) |
| `0x03` | 6,464 | hold here | handler page, "The commands that run the motion itself" |
| `0x04` | 27,631 | the battle unit's action-timeline event (bank A id 4) | handler page, "Where the commands are authored" |
| `0x05` | 23,784 | a character sound (bank B id 5) | handler page §3 table; the audio page |
| `0x06` | 7,008 | the second battle guard (bank A id 6) | handler page, "Where the commands are authored" |
| `0x09` | 78,455 | play this bone motion | handler page, "Command `0x09`" |
| `0x0A` | 6,726 | **set the selector for `0x0B`** | handler page, new section (P2) |
| `0x0B` | 6,726 | **choose the next track from a list** | handler page, new section (P2) |
| `0x0D`–`0x10` | 268,691 / 214,068 / 295,480 / 136,235 | the per-slot ramp channels | ramp-channel contract |
| `0x11` | 10,617 | bone trails on / off | handler page §3 table |
| `0x12` | 32,515 | look-at tracking enable (`RelationLook_SetTrackingEnabled`) | handler page §3 table (name and callees; not expanded further) |
| `0x13` | 5,805 | store the controller switch, broadcast it | handler page, "Command `0x13`" |
| `0x15` | 1,218 | draw / sheathe: re-attach children | handler page §3 table |
| `0x16` | 329 | bind sub-resource variants | handler page, "Command `0x16`" |
| `0x18` | 28,222 | the footstep effect | handler page §3 table |
| `0x1A` | 12,876 | move and turn toward the target along a profile | handler page §3 table |
| `0x1D` | 5,639 | pose-sequencer event | handler page §3 table |
| `0x20`, `0x21` | 148 / 613 | alias bones `0x107` / `0x108` | handler page §3 table |
| `0x23` | 261 | fade channel 1 (attached-piece visibility) | fade-channel page, channel 1 |
| `0x24`, `0x25` | 1,493 / 740 | ramp a rotator's speed / restore it | handler page §3 table |
| `0x28` | 115 | **a 5-bit request into `+0x304` bits 27–31** | handler page, new section (P3) |
| `0x29` | 47,472 | a footstep sound | handler page §3 table; the audio page |
| `0x2A` | 7,183 | a pooled, generation-tagged handle | handler page, "Command `0x2A`" |
| `0x2C` | 387,789 | blend-in rule by previous motion | handler page, "The commands that run the motion itself" |
| `0x2F` | 30 | presentation event to the child sub-tree | handler page, "Command `0x2F`" |
| `0x34` | 28 | the shadow command | handler page, "Command `0x34`" |
| `0x3F` | 3,108 | a directed sway | handler page, "Command `0x48` is command `0x3F` …" |

**What stays open, exactly:**
- what `0x0B`'s selector kinds choose by (~~seen: `0`, `2`, `0xA`, `0x10`, `0x20`~~ ten are authored, and kind `0x10` is now
  read: [`uq218-fmc-selector-kinds`](../uq218-fmc-selector-kinds/README.md); the struck list was a histogram's top five);
- what `0x28`'s values 1 and 10 select on the effect side;
- `0x12` beyond its name and callees.

These are sub-questions of named, read mechanisms; none is an unread command.

**Scope.** Counts are over the `.ca`/`.cm` `@FMC` blocks. The handler page's own census also includes the `.mot` event
scenes, where `0x14` and `0x48` occur, so its totals are larger. Not claimed: live behaviour, or any id outside the 33.

| consumer | action | agreement |
|---|---|---|
| `the-authored-presentation-command-handlers.md` | new section for `0x01`, `0x0A`/`0x0B`, `0x28` | revised-here |
| `fef-and-motion-entries.md`, residue bullet "`@FMC` per-opcode operand semantics … mostly open" | cite this crosswalk; the residue narrows to the three items above | routed-to-SWE2-DATA |
| `OPEN-QUESTIONS.md` UQ-218, the `@FMC` part of its residue | the same narrowing | routed-to-SWE2-DATA (row owner) |

Regression: `fmc_opcodes.py` (T, A, P1–P3, C). run: fmc_opcodes.py at 1bf58337c, FAILS 0.
