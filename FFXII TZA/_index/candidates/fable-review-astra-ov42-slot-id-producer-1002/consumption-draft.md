# Consumption draft: ov42-slot-id-producer (FABLE, 2026-10-02)

*Links inside proposed page text are shown as `page-relative link:` paths, because they resolve from the target page, not from this folder.*

This draft is for FABLE to apply. Nothing here has been applied. Its scope is the accepted claims of
[REVIEW.md](REVIEW.md), with the review's five narrowings, at the stated limits. It was drafted against the
availability page at HEAD `e828e3f50`, after the commit "FABLE: an end notification is attempted before the retiring
slot is free ..." landed. The page has CRLF line endings.

## Candidate pages and who leads them

The lead counts come from `git log --format=%s -- <page> | cut -d: -f1 | sort | uniq -c`.

| Page | Cites | Commit subjects by prefix | Lead | Action |
|---|---|---|---|---|
| `07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md` | `0030CFB0`, `0030D14F` (line 774), the OV-42 subsections | FABLE 7, OPUS 2, the rest 1 each | **FABLE** | edits 1-3 (below) |
| `07-Combat-Action/Command-And-Action-Seam/native-command-seam.md` | `0030D070` / `0030CFB0` "presentation slot allocate / acquire" (line 118); UQ-112 slot table "`+0x1C` ... allocator `0030D0AA`, `0030D14F`" (line 522) | FABLE 4, the rest 1 each | FABLE | **agrees**: no edit |
| `07-Combat-Action/CONTRACT-native-command-seam.md` | the slot pool | FABLE 6, OPUS 1 | FABLE | **route to OPUS** (the packet assigns the acquire-versus-allocate ABI, input/return widths, occupancy marker and valid-state qualifications to OPUS); suggested text below |
| `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` | exclusive-subtree table: "`0030CFB0` (`BattleAction_AcquirePresentationSlot`, ~229 B)" and "`r8b = 0` found flag" | Database 28, FABLE 12, SWE2-EC7 9, OPUS 7; that section came from `a3c628f5a` (FRONTIER) | mixed; the section is FRONTIER's | **route to SWE2-FRONTIER**: two label corrections, below |
| `_index/OPEN-QUESTIONS.md`, row OV-42 | the register row | n/a | FABLE (register edit at publish time) | optional status note, below |

Consumer check for the corrected attribution in edit 1. "`0030CFB0` stores the word" appears only on the
availability page (line 774). The seam page's UQ-112 table already credits `0030D14F` to the allocator, and so do
FABLE's `astra-returns-ov42-fable-1002/README.md` (line 144) and SPEC's `auditspec-review-astra-spattack-remap-0930`.
All of them **agree**. The regressions are `rv_slots.py`'s "0030CFB0's own writes ... none at +0x1C" check, with
control 13, and the DX → R10D → `0030D070` + 0xDF check, with controls 5 and 7.

## Edit 1 (FABLE page): attribute the slot word store to the allocator

File: `07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`. Subsection: "FABLE
2026-10-02: which action rows the special-sequence path could turn into a rejected request (OV-42)". Section: "What
does not exclude 511..534". Bullet: "The queue remap".

OLD:

```
  - The queue remap. The queue cell `022C2178` holds `word - 0xD0` (`0030DBDA`, `0030DC7B`, `003068CA`) or -1, and
    its reader `00309C00` consumes the value. The script adapter `0030EEA0` adds `0xD0` back as a 16-bit add
    (`0030EEB2`) before `0030CFB0` stores the word into the slot's `+0x1C` (`0030D14F`). Rows 511..534 queue as
    303..326 and decode unchanged. Only `0xCF` and FFFF read as unavailable, so the remap has no universal inverse.
```

NEW:

```
  - The queue remap. The queue cell `022C2178` holds `word - 0xD0` (`0030DBDA`, `0030DC7B`, `003068CA`) or -1, and
    its reader `00309C00` consumes the value. The script adapter `0030EEA0` adds `0xD0` back as a 16-bit add
    (`0030EEB2`) before ~~`0030CFB0` stores the word into the slot's `+0x1C` (`0030D14F`)~~ the acquire wrapper
    `0030CFB0` passes the word to the slot allocator `0030D070`, whose last store writes it into the slot's `+0x1C`
    (`0030D070` + 0xDF) *(corrected 2026-10-02, FABLE: the store is the allocator's, not the wrapper's; ASTRA's
    `ov42-slot-id-producer`, FABLE review [record] (page-relative link: `../../_index/candidates/fable-review-astra-ov42-slot-id-producer-1002/REVIEW.md`), slot-allocator subsection below)*.
    Rows 511..534 queue as 303..326 and decode unchanged. Only `0xCF` and FFFF read as unavailable, so the remap has
    no universal inverse.
```

The struck span is the page's own old text, including its bare `0030D14F`. If the address gate counts struck text,
use this variant without the strike: the same NEW text, with "~~...~~" removed and the italic note opening
"*(corrected 2026-10-02, FABLE: this said `0030CFB0` stores the word; the store is the allocator's ...)*". The
correction record is this folder: `affected:` the availability page, run `rv_slots.py`.

## Edit 2 (FABLE page): narrow the limit that says no slot allocation is proved

Same subsection, **Limits kept**, last bullet.

OLD:

```
- No slot allocation, command, AI or script selection, successful load, owner submission or rejection is observed or
  proved. Natural rejection and whole OV-42 stay OPEN.
```

NEW:

```
- No natural slot allocation, command, AI or script selection, successful load, owner submission or rejection is
  observed or proved. The slot allocator's own admission is now read: it stores any word into a free slot (the
  slot-allocator subsection below). Natural rejection and whole OV-42 stay OPEN.
```

## Edit 3 (FABLE page): new subsection at the end of the page

Append after the page's current last line, "- Whole OV-42 stays OPEN." (the queue-reader subsection's limits),
separated by one blank line:

```
### FABLE 2026-10-02: what the presentation-slot allocator admits (OV-42)

*From ASTRA's packet [`ov42-slot-id-producer`] (page-relative link: `../../_experiments/evidence/ov42-slot-id-producer/README.md`)
(`0ada51452`), reviewed by FABLE ACCEPT-WITH-NARROWING
([record] (page-relative link: `../../_index/candidates/fable-review-astra-ov42-slot-id-producer-1002/REVIEW.md`), 53 checks, 0 FAIL,
13 controls). Static, plus an emulation of the original bytes on synthetic slots and rows.*

- **The allocator `0030D070` (229 B, one `.pdata` record, no calls).** It scans the 32 slots at `022C17B0` + 48*i
  from slot 0 upward and stops at 32. A slot is free when its WORD `+0x1C` is FFFF, and the first free slot wins.
  - It writes that slot's list links (`+0`, `+8` and the list's head or tail cells), DWORD 1 at `+0x10`, `+0x14`
    and `+0x18`, and the incoming ECX at `+0x20`. Its last store is the incoming DX, zero-extended, at `+0x1C`
    (`0030D070` + 0xDF). It returns EAX = the slot index, 0..31.
  - That store is the action word's only use. No compare in the body reads the word, so there is no action-range,
    category or identity test. Each of 511..534 is stored unchanged when a slot is free.
  - With all 32 slots occupied, it returns AL = FF and writes nothing outside its frame. That is a capacity
    failure, not a refusal of the id. Only AL is defined on that arm.
  - A supplied FFFF is also copied, so the slot is linked and initialised but still reads free. No natural FFFF
    submission is claimed.
- **The acquire wrapper `0030CFB0` (185 B).** It takes the action word in R8W and the identity in EDX. It passes
  them to `0030D070` as EDX (the word, zero-extended) and ECX, then stores the returned AL in unit+4. The wrapper
  itself never writes `+0x1C`; the word store is the allocator's.
  - A unit+4 that is not FF skips the whole acquisition.
  - A row whose `+0x0C` bit 30 is clear allocates directly.
  - With bit 30 set, a word in D0..F1 allocates while `022C2160` is 5 or 6.
  - Every other bit-30 row meets a one-shot flag, bit 1 of `022C2158`. If the bit is set, the row is skipped. If it
    is clear, the wrapper sets it and allocates. The words 511..534 are 303..326 above D0, so they meet this flag.
  - The flag is set *before* the allocator runs, and the wrapper never clears it. That includes the case where the
    array is full and unit+4 stays FF. Whatever clears it is not read.
  - The row comes from `[02EBF138]` through `0020E600` as a zero-extended 32-bit pointer. A null descriptor or a
    null resolve sets that pointer to 0, and the wrapper still reads `+0x0C` (address 0xC). There is no null guard.
- **Direct callers (raw `E8`/`E9` census).** `0030D070` has one direct caller, the wrapper (`0030CFB0` + 0xA1). The
  wrapper has two: the script adapter `0030EEA0` (+ 0x60), and a call in a battle-action routine that this page does
  not otherwise cite. Indirect callers are not covered.

So the slot allocator does not exclude 511..534. Its only refusals are capacity, a slot the unit already holds and,
for bit-30 rows, the special-sequence state and the one-shot flag.

**Limits kept.** These limits are ASTRA's and FABLE's.

- No command, AI or authored-VM producer is read that supplies 511..534 or FFFF.
- Current row and descriptor identity, readable stable rows, and the pool's initialization, ownership and reuse
  are premises. The slot array lies in `.data`'s virtual tail, so its FFFF markers come from the pool reset, which
  is not read here.
- What a FFFF allocation leads to (a linked slot that still reads free) is not claimed.
- No natural slot allocation, command execution or rejection is observed.
- Whole OV-42 stays OPEN.
```

### Citations and the neighbour gate

The only function citation that is new to the page is `0030D070`. `0030CFB0`, `0030EEA0`, `0020E600`, `02EBF138` and
`022C2160` are already cited there. `022C17B0` and `022C2158` are data cells, not functions.

The wrapper's other direct caller is `00304850`, at + 0x5D4, in its chained fragment. It is **named by role** ("a
battle-action routine") rather than by address, so that no new caller edge is imported. Its address is in the review
record.

Pre-check: FABLE's `xlayer.py` on a scratch copy of the page with edit 3 appended, `--only 0030D070,0030CFB0,0030EEA0`.
It reported `UNACCOUNTED: 0`. The only foreign layers are `0030EEA0`'s existing Party and Script_VM_Native_Bridge edges,
and both are already accounted for. Interior `.text` addresses are written `<entry> + 0xNN`.

## Route to OPUS: `07-Combat-Action/CONTRACT-native-command-seam.md` (slot ABI)

This is suggested text for OPUS's slot-ABI qualifications. Placement is OPUS's choice (§3 Types or §10 Failure
paths):

```
- Presentation-slot acquire/allocate ABI (FABLE review of ASTRA `ov42-slot-id-producer`, 2026-10-02):
  - The acquire wrapper `0030CFB0` (185 B): RCX = the unit, EDX = the identity, R8W = the action word. It returns
    nothing; its result is unit+4.
  - The allocator `0030D070` (229 B, no calls): ECX = the identity, DX = the action word (zero-extended; the upper
    RDX bits are ignored).
    - It returns EAX = the slot index 0..31 on success. On a full array it returns AL = FF only, with the upper RAX
      bits undefined.
    - Occupancy is WORD `+0x1C` == FFFF. The word is stored last, so a FFFF word leaves the slot reading free.
  - The flag gate in the wrapper sets bit 1 of `022C2158` before allocating and never clears it.
  - The row read has no null guard: a null `[02EBF138]` reads address 0xC.
```

## Route to SWE2-FRONTIER: `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`

These two label corrections apply to the exclusive-subtree table, in the section that `a3c628f5a` (FRONTIER) wrote:

- "`0030CFB0` (`BattleAction_AcquirePresentationSlot`, ~229 B)" should read **185 B**. 229 B is the allocator
  `0030D070`'s size.
- "`r8b = 0` found flag" should read **"`r8b` = the slot index, 0 to 31"**. `r8b` is the scan counter and becomes the
  return value. It is not a flag.

## Optional: register row OV-42 (FABLE, at publish time)

Append to the OV-42 status cell, keeping its current text:

```
2026-10-02 (FABLE): the presentation-slot allocator 0030D070 admits any word, 511..534 and FFFF included, into a free
slot; its only refusals are capacity, an already-held slot, and for bit-30 rows the special-sequence state and the
022C2158 one-shot flag (ASTRA ov42-slot-id-producer, FABLE review ACCEPT-WITH-NARROWING). Natural producers stay open.
```

Escape any literal `|` before writing it into the row.

- consumer: availability page OV-42 subsections - revised-here (edits 1-3)
- consumer: `native-command-seam.md` UQ-112 table - agrees
- consumer: `CONTRACT-native-command-seam.md` - routed-to OPUS (slot ABI)
- consumer: `the-battle-unit-field-map.md` subtree table - routed-to SWE2-FRONTIER (two labels)

affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

run: `rv_slots.py` at HEAD e828e3f50 (53 checks, 53 PASS, 0 FAIL, 13 controls)
