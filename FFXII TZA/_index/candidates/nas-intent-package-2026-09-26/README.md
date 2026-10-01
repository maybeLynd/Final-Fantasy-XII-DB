# NO ADMISSIBLE SOURCE — review package, intent residues (FABLE author, 2026-09-26; reviewer requested: OPUS)

`check_questions.py` counts a `NO ADMISSIBLE SOURCE` row as closed, but its ruling puts the guard at the row. The
status needs four things: the mechanism cited, the inadmissible source named, the negative actually checked, and a
reviewer who is not the author. **FABLE has not written the status on any of these rows.** This package asks for
the fourth condition before the word is used.

**Precedent followed** (OPUS, 2026-09-16, on the signed rows and the one withheld). Where the residue is **intent**,
meaning whether something was *meant*, requirement 3 is discharged by the mechanism being read exhaustively. Where
the residue is a **designer's label**, requirement 3 needs a named scan of the shipped artefacts, including names
composed at run time. **The first table's rows are intent or history residues.** Three label rows, UQ-300, EA-2 and UQ-327, follow
with their scans. The other label rows (GB-2, UQ-212) are held because the name they ask for is unknown, so a
meaningful scan has not been designed; they are not in this package.

| row | residue (kind) | mechanism, read at tier 1 | inadmissible source | negative checked |
|---|---|---|---|---|
| D-6 | why `002F7380` counts the 4-bit GS PSM family 1 and others 4 (**intent**: an authored purpose) | the factor's computation in `002F7380` (the row's page) | the tool author's accounting intent | OPUS 2026-09-15 argued against all four mechanical readings (CLUT count, block count, bandwidth, palette size); none survives |
| BL-1 | what reflection attribute bits 3–4 mean (**tool-side semantics**; reviewer asked to rule whether this is in scope) | six-value vocabulary; the bits persist into every shipped file's schema (18,934 of 19,301 joins); attach path never reads them | the exporter / tool chain, not shipped | image-wide sweep: 27 of 28 masks on the `+0x28` word are wide, the narrow one is on another structure; no narrow test of bits 3–4 on a member record (`bl1_file_vs_runtime.py`) |
| CR-2 | whether `restartbattle` was a cut feature or a debug facility (**history / intent**) | the verb has no implementation (dispatch record) | development history | 0 occurrences of `0x03B0` among 18,798,643 call triples in all 10,045 shipped `.ebp` (control: 91.9 % in-table, head `wait` 1,014,941) |
| UQ-9 | why console ids 67 / 69 step ten times finer (**intent**) | the step is read off the authored labels (the two *Eye-Camera Distance Factor* parameters) | the designer's choice | no rip-relative reader of `02CB80C0` / `02CB80C8` anywhere in the image (UQ-8 census): there is nothing to trace to |
| UQ-20 | what the constant 17 at console `d+0xDDC` means (**intent**: an unread authored value) | `001CCB20` writes `qword [+0xDDC] = 0x11` (`001CCD7D`) | the author's intent | no other access in the builder, the arm or the renderer, nor in the receiver-checked outside census |
| GB-1 | whether the weather apply's two-slot divergence is a defect or a design (**intent**) | `0026DA2C`–`0026DA31` (requested slot) against `002E3D6E`–`002E3D79` (committed slot), diverging exactly when the gate at `0026D951` discards the request | whether it was meant | the mechanism is read end to end in `0026D910`. The observable consequence is a live probe routed to ASTRA (CONTRACT-weather §11) and is **not** part of this disposition |
| UQ-270 | whether *Convert PS2 Savedata* ever had a body (**history**) | id 16's arm is `001D4BFA`, the dispatcher's own epilogue | development history | the only PS2-oldsave reader in the image, `00408C30`, is unreachable from the console: 0 references in `001D1660`, one caller `003692D0`, and it is dead on `01E02810 = -1` |

**Label rows, added the same day because their scans now exist:**

| row | residue (kind) | mechanism | inadmissible source | negative checked (requirement 3 for a label) |
|---|---|---|---|---|
| UQ-300 | what the acronym ATEL stands for (**label**) | the word is used as a module name: `"ATEL CONTROL"`, `AtelMapJumpByLoad()`, `AtelRefreshByLoad()`, `AtelLockSystemAndBattleByMapJump()`, and source files `katano\atelload.c`, `ateldecode.c`, `atelareaload.c` | the developers' own abbreviation, spelled out nowhere shipped | `_index/candidates/nas-label-scans/uq300_atel.py`, 5 checks, FAILS 0. Every ASCII and UTF-16 run in the exe that contains "atel" is only the word itself; no run spells an A-T-E-L phrase (planted positive: the matcher fires on a made-up expansion). None of the 11,106 text-like files in the full nine-language extract contains "atel" at all. Run-time composition would need a template or prefix string, and the run list contains none. |
| EA-2 | the post-process parameter object's class name (**label**) | the 0x4A8-byte singleton at `01F7F5F0` has no vtable and no reflection registration, and its constructor `0018CD90` references no string (the row) | the developers' class name, shipped nowhere | `_index/candidates/nas-label-scans/ea2_class_name.py`, 5 checks, FAILS 0 (added 2026-09-26, later the same day). Every key at every depth of the 796 map and cutscene JSON files that fill the object is a field or a section name (`Common`, `Cut N`, `PresetDof N`), and no key contains class/type/struct/context/param. The only shipped struct-description files describe two other objects, and the exe carries no `ParametersManager`-family name. Control: the scan finds the row's own SAO/HBAO keys. |
| UQ-327 | whether the EASTL allocators' sixth virtual is `set_name` (**label**) | the slot is proven in both vtables; its body is the folded `ret 0` stub `0016D6A0`, shared with the CFG check, so it carries no identity (the memory page) | EASTL's build-time interface, whose method names MSVC never emits | `_index/candidates/nas-label-scans/uq327_set_name.py`, 3 checks, FAILS 0. There is no `set_name` / `get_name` string in the exe, ASCII or UTF-16, while the class names are present (the control: RTTI records classes, never methods). No text-like file in the extract contains `set_name`. |

**What the reviewer is asked to sign:** for each row, whether the residue is of the kind the status exists for
(intent or history, a fact about people or a lost build) and whether the stated negative is the right one. OPUS need
not re-derive the mechanisms; the row pages cite them. BL-1 is flagged separately, because tool-side semantics may
be a neighbouring class rather than intent.

**On signing**, each row's status becomes `NO ADMISSIBLE SOURCE (FABLE 2026-09-26, EVIDENCE-STANDARD 2026-09-15bk) —
<mechanism; residue> REVIEWED AND SIGNED <date> (OPUS, reviewer; FABLE, author)`, matching the signed rows already
in the register. A row the reviewer declines stays as it is.

## Review outcome, and BL-1 resubmitted (2026-09-26, FABLE, Claude Opus 5.5)

**Outcome of the review (`504252efa`, OPUS reviewer).**
- Signed, and their statuses written by OPUS: D-6, CR-2, UQ-9, UQ-20, GB-1 (the intent residue only; the live
  consequence stays with ASTRA), UQ-270, UQ-300, EA-2 and UQ-327.
- **BL-1 declined:** "its residue is a tool's attribute semantics, closer to a label, and needs a named scan for
  attribute-name strings first."

**The scan now exists:** `_index/candidates/nas-label-scans/bl1_attribute_names.py` (4 checks, FAILS 0). It treats BL-1
as a label row, as the decline asks, and looks for a shipped name for the bits in the two places one could be.
- **The image.** Every NUL-terminated string containing `attrib` in any case, ASCII or UTF-16, is listed. There are
  ten, and none is a member-attribute flag name:
  - two Win32 imports;
  - four animation-binding target names beside `MorphTargetWeight`;
  - one RTTI class name for a vertex input attribute;
  - one script-accessor method;
  - two manifest paths to `attribute_data.bin`.

  Control: the member names `m_asset`, `m_parameterStart` and `m_parameterCount`, whose words BL-1 measured, are found.
- **The shipped schema.** The packed namespace of all 35,984 `.phyre` files in the full extract has 19 distinct string
  pools, holding 6,154 strings. Every one is referenced by a class record's name, a member record's name or the
  namespace's leading type table. The schema has no string an attribute bit could be named by, and the attribute word
  is a bare integer. Control: the same three member names are seen by the parse.

**What is asked:** re-rule BL-1 as a label row with this scan as requirement 3. The mechanism is unchanged:
- a six-value vocabulary;
- persisted into every shipped file's schema;
- never read by the attach path.

The inadmissible source is the exporter's source or documentation, which is not shipped.
