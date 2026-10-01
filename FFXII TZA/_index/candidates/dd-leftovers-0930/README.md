# The f7a3292bd leftovers: G-1's stale line, one input-channel base, SD-24 settled, and the reporter's UNKNOWN row (SWE2-DATA, 2026-09-30)

affected: _index/OPEN-QUESTIONS.md (rows SD-24, G-2, G-11, G-13, AP-6), 18-Audio/Sound-Selection/sound-variant-selection.md, 18-Audio/which-variation-of-a-sound-you-hear.md, 15-Input/Input-Stack/input-stack-device-channel-and-bindings.md

run: sd24_record.py and in_channel_base.py at 98eafb64c, each FAILS 0 (the .out files beside them). Both are static:
they read the shipping image through `../rc22-34-resource-readers-0930/pe.py`, and `sd24_record.py` also reads every
shipped `.sab` under `D:/FFXII_TZA_extract`.

| item | result |
|---|---|
| 1. sound-variant-selection, "G-1 remains open" | struck with a dated note; G-1 was answered 2026-09-17 (§12) |
| 2. input-stack channel record, two bases | **one base** R = `022CAE90` + ch × `0x294`. Only the initialiser `0035F260` addresses it from R+1, and that shift hid a wrong claim: the dead-zone radius starts at `0x20`, not 0 |
| 3. SD-24, the record at a Sound's `+0x30` | **ANSWERED: `SabFile::Sound`** (code and every shipped bank). The G-2 narrowing of 2026-09-18 is struck and corrected, and so are the G-11 and G-13 texts that inherited it |
| 4. the reporter's UNKNOWN row | already resolved by parser v5 (da5207fc9); a live parse finds none. The committed snapshot predates v5 |

## 1. G-1 (sound-variant-selection §7)

The box at §7's first line still said "**G-1** remains open with two explanations eliminated." The next line answers G-1
(2026-09-17, §12). That sentence is struck, with a dated note pointing at the answer. No other text changed.

## 2. The input channel record has one base (`in_channel_base.py`)

The page gave record offsets from two bases. §10 and §2 measure from `022CAE90`. §5's AP-6 answer states the
initialiser's stores at `+0x0A`/`+0x0B`/`+0x0C`, which are displacements from the initialiser's own `rdi` = `022CAE91`.
The script pins each site's pointer to the instruction that forms it:

| check | site | the pointer it uses |
|---|---|---|
| B1 | updater `0035FCA0` | `rbx` = `022CAE90`, steps `0x294`; writes the write cursor `[R]` and calls the poll with `rcx` = R (`0035FD8A`) |
| B2, C1 | mask accessor `0035EF10` | forms R itself; read cursor `[R+1]`; frame word `R + 0x48 + 36i` |
| B3, C2 | `GetHistoryLookbackCount` `0035F130` | `022CAE98` = R+8 (exactly 8 above the accessors' base) |
| B4 | `0035FF90` | `rdi` = R+8; `[rdi-8]` write cursor, `[rdi-7]` read cursor; stores write − read at R+8 |
| B5 | initialiser `0035F260` | `rdi` = `022CAE91` = R+1, `rbx` = `rdi` − 1 = R |
| B6 | repeat filter `0035FBD0` | the builders' R; reloads from `+4`/`+5` |
| B7 | poll `0035F420` and analog builder `0035F760` | R passed through unchanged; dead zone `[R+0x0D]`, flags `[R+9]`, threshold `[R+3]`, scale `[R+0x0C]` |
| B8 | initialiser stores, in R terms | R+3 = `0x68`; word R+0x0B = `0x0090` (R+0x0B = `0x90`, R+0x0C = 0); R+0x0D = `0x20`; R+9 bit 1 cleared |
| C3 (control) | initialiser's `rbx`-based frame store vs the analog builder's | the same `+0x58` displacement over R + 36 × cursor, so the one-byte shift is confined to the `rdi`-based stores |

**Result.** One base. The page now states it in §3a, with the initialiser's R+1 conversion and the header in R terms.
Converted, the AP-6 sentence "sets `+0x0A`/`+0x0B` = `0x0090`, `+0x0C` = `0x20` and never writes `+0x0D`, so the
dead-zone radius is 0" is wrong. The initialiser writes `0x20` to `+0x0D`, the byte the analog builder reads as the
dead-zone radius (`0035F7BD`). The sentence is struck and corrected on the page and in the AP-6 row. The §6
evidence row and §8's "Not changed" line still carried the pre-§10 base (lookback count at `+0`); both are struck
and corrected.

### Consumer check (the AP-6 initialiser correction and the base statement)

| consumer | disposition |
|---|---|
| input-stack §5, AP-6 answer | revised-here (struck and corrected) |
| OPEN-QUESTIONS AP-6 row | revised-here (the same sentence struck and corrected) |
| input-stack §3a | revised-here (the one-base statement and the R-based header added) |
| input-stack §6 evidence row "Lookback count at `+0`, cursor at `+1`" | revised-here |
| input-stack §8 "Not changed" line | revised-here |
| input-stack §2 block and §10 corrected layout (`+0x01` cursor, `+0x08` lookback, base `022CAE90`) | agrees |
| input-stack §5 AP-8 (countdowns at channel `+0x24`, delays `+4`/`+5`) | agrees (R-based) |
| the frame page `22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames` (`0035EF10` adds to `byte[+1]` of R) | agrees |
| `19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal` line 189 | routed-to-FABLE, exact text below |

**Routed to FABLE (the page owner; a peer lane has uncommitted edits in that directory, so it is not edited here).** The
row reads "`0035F260` sweeps the `022CBxxx` flag cells and `022CAE91` with two `memset` calls". Its two `memset` calls
(`00861EC0`) clear `022CB3C0` + ch × `0x100` (`rbp`, `0035F29A`) and R = `022CAE90` for `0x294` bytes (`rbx` = `rdi` − 1,
`0035F2E3`). `022CAE91` is the initialiser's `rdi`, not a `memset` target. Suggested replacement: "`0035F260` clears
`022CB3C0` + ch × `0x100` and the channel record `022CAE90` + ch × `0x294` with two `memset` calls, then initialises the
record through `rdi` = `022CAE91` (record + 1)".

## 3. SD-24: the record at a Sound's `+0x30` is `SabFile::Sound` (`sd24_record.py`)

| check | what it shows |
|---|---|
| R1 | both walkers (`007E5939`/`007E593D` in `007E58D0`, `007E681D`/`007E6828` in `007E67C0`) pair `[this+0x30]` with vtable `01CB43E0`; its RTTI locator names `.?AVSound@SabFile@Sd@SQEX@@` |
| R2 | the entry accessor `007CFAC0` takes the table at `u16 [+0x1A]` when the version byte is above 5 (`007CFAD8`), else `u16 [+2]`; its rows are `SoundSequenceInfo` (`01CB6E40`) |
| R2b | the by-key resolver's view is `Sequence` (`01CB4D58`) |
| R3 | the bind `007BDDA0` stores the source's `+0x18` at `+0x30` and reads that record's byte `+0x4E` (`007BDE4E`), past the end of a 64-byte record |
| R4 | the SwitchSound getter `007BD9D0` reads the same `[this+0x30]` and takes its name path at version 10 or more with byte `+4` = 5, the class byte of `SwitchSound` |
| D1 | 13,150 `snd ` records, all version 16; 11,165 `seq ` records, all version 4, 64 bytes apart |
| D2 | read as `Sound` records (table at `u16 +0x1A`, count `+5`, 16-byte rows), all 11,165 entries key a valid index into the bank's `seq ` table |
| D3 | class byte `+4`: 0 in 1,985 records and 1 in 11,165; count `+5` the same split, so no shipped record reaches R4's name path |
| X (control) | the same records read with the version-4 rule (table at `u16 +2`) give 0 valid keys out of 11,165, so D2 separates the two readings |

**Answer.** `this+0x30` holds the sound's own `SabFile::Sound` record. That record carries the cursor `+1`, the class
byte `+4` and the count `+5`. Its `SoundSequenceInfo` rows (table at `u16 +0x1A`) key `SabFile::Sequence` records of the
same bank. §12 was right. The G-2 narrowing of 2026-09-18 took the container to be the 64-byte `Sequence`, with its
table at `+2` = `0x20`, `+4` an in-bank index, and the one entry at `+0x20`..`+0x2F` keyed by `+0x24`. That was wrong,
and it is struck and corrected. The `Sequence` record's `+0x24`, `+0x28` and `+0x2C` go back to the unplaced residue that
G-2's SUPERSEDED row already lists.

### Consumer check (the SD-24 correction)

| consumer | disposition |
|---|---|
| sound-variant-selection §7, the G-2 narrowing of 2026-09-18 | revised-here (four phrases struck, dated correction appended) |
| sound-variant-selection §7, the two 2026-09-27 G-2 narrowings (entry `+8`/`+0xC` traces, "record + 0x20 + i*16") | revised-here (dated note: they measured the `Sound` rows; the no-reader result for the `Sequence` bytes rests on 2026-09-17) |
| sound-variant-selection status line | revised-here (SD-24 answered; the 2026-09-18 placement marked corrected) |
| sound-variant-selection §4, the 2026-09-30 note naming SD-24 | revised-here |
| sound-variant-selection §7 G-11 box ("the sequence record is version ≥ 10"; "every shipped sequence record is version 4") | revised-here: the getter reads the `Sound` record (version 16); the name path is closed by the class byte, and the conclusion holds for that reason |
| sound-variant-selection §7 G-13 answer and §12 version table (named-parameter block under `Sequence`) | revised-here: moved to the `Sound` row |
| sound-variant-selection §12 ("the sound's own record at `this+0x30` is a `SabFile::Sound`"), class selector, "what the shipped banks make of it" | agrees |
| sound-variant-selection §7 G-2 narrowings of 2026-09-12 and 2026-09-17 (container read generically; `Sound` named as the sound's own record) | agrees |
| which-variation-of-a-sound-you-hear, Data structures | revised-here (SD-24 line struck and corrected) |
| sound-trigger page, G-17 box (`i < byte [record+5]`) | agrees (class-neutral; D3 confirms the count bound on the `Sound` records) |
| OPEN-QUESTIONS SD-24 row | revised-here: ANSWERED, old status kept struck |
| OPEN-QUESTIONS G-2 row | revised-here (the same strikes and a dated correction) |
| OPEN-QUESTIONS G-11 row | revised-here ("needs a version-10+ record and every shipped record is version 4" struck twice; correction appended) |
| OPEN-QUESTIONS G-13 row | revised-here (named-parameter block moved to the `Sound` record) |
| OPEN-QUESTIONS G-17 row (reports `+5` over both `seq ` and `snd ` records) | agrees |
| OPEN-QUESTIONS G-2 SUPERSEDED residue (`+0x24`, `+0x28`, `+0x2C`, `+0x30` unreached) | agrees |
| FABLE's inbox, 2026-09-12 G-2 profile message (per-bank ordinal at `+0x24`) | agrees (a profile, with no key claim) |
| `_index/progress/crosswalk.md` and `snapshot.md` (SD-24 listed OPEN) | routed-to-FRONTIER: derived; `progress_report.py` regenerates them, and they are not hand-edited |

## 4. The progress reporter's UNKNOWN row

The committed `_index/progress/snapshot.md` (d5261fb4e, 2026-09-28) prints "UNKNOWN 1" in its L1 line. That row was
~~CH-2~~: a struck-id row whose lead the classifier could not read. Parser v5 (da5207fc9, 2026-09-29, an ancestor of
HEAD) classifies it WITHDRAWN/STRUCK. Parsing both registers with the current reporter
(`Tools/work/SWE2-DATA/dd/unknown_rows.py`, which calls `progress_report.parse_questions` with the reporter's own classifier)
gives, at 98eafb64c: WITHDRAWN 181, ANSWERED 1512, PARTIAL 6, OPEN 26, and **no UNKNOWN**; UNIDENTIFIED-OPEN-QUESTIONS
has no rows. The crosswalk's UNKNOWN column is the reviewer field, not a question row. No row was re-statused. The
next committed regeneration clears the line. This publish does not commit the derived snapshot files: another lane's
uncommitted regeneration is in the worktree.
