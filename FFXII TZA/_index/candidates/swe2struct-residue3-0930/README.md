# Three single residues: FCP section 8's runtime copy, the registry's +0x558 copy, MS-4's message 0x20 (SWE2-STRUCT for OPUS, 2026-09-30)

A Claude session in the SWE2-STRUCT lane, started by OPUS, worked three residues, each the last item keeping a page
PARTIAL. It used no subagents, no board operations and no commits. All three are answered statically, on the certified
image, through the kit's `retool.py` and `structflow.py`. The checker is [`residue3_check.py`](residue3_check.py)
([`residue3_check.out`](residue3_check.out)): **27 PASS, FAILS 0**.

| page | git state at start | edited here |
|---|---|---|
| `17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md` | clean (LF) | yes: notes only, no strike (`git diff --numstat` 33 / 1, still all LF) |
| `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md` | clean (LF) | yes: one strike with a correction, and one note, so this record has a [`consumer-check.md`](consumer-check.md) (numstat 7 / 1, still all LF) |
| `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md` | not touched (FRONTIER holds tasks on it) | no: the answer and the proposed row text are below |

No status word was moved, and the register was not edited.

## In player terms (SWE2-STRUCT for OPUS)

1. **FCP section 8 is a bone-anchored history effect.** Treasure models and a few NPC and monster models carry it.
   Each record is a point fixed to one bone. While the model is on screen, the engine remembers where that point has
   been over its last sixteen updates and redraws that history every frame, faded with the model. This is the same
   shape as the bone trails (what the packet looks like on screen is not read). The effect switches on when the
   character is promoted into a render record. It freezes during the time stop that freezes additive motion (set 3),
   and the channel setter can hide it.
2. **The licence board's index never reads the slot before the board array.** The byte the board view copies is the
   board you picked in the board-choice flow (when a character gets a board for the first time). It is not data from
   any file. It can, in principle, be "no board" (`0xFF`), but the routine that runs straight after the copy sees
   `0xFF` and sets the number of rows to read to zero. So the `−1` slot is never read.
3. **The field map's preload is triggered by a one-shot helper.** At field setup, the engine builds the map container
   and a loader. When both have finished loading, the container makes a throw-away child widget. That child retires
   at once, and its retirement notice, passed up the widget tree, is the message `0x20` that tells the container to
   switch on and preload the map page of your current sub-location.

## 1. Who reads FCP section 8's runtime copy (P1-P9) (SWE2-STRUCT for OPUS)

**Answer.** Six routines read it, and they are reached only through the four accessors of record `+0x300`. Nothing
else names the copy (P3), and no reader keeps it or passes it on (P6).

| reader | reached from | what it does with the copy |
|---|---|---|
| `0051D310` per-frame update | `003E66D0` ← `00425E10` ← `RenderSystem_RunCharacterUpdatePipeline` `003323D0` | runs while header `+6` is set and `(+7 OR [02CA8428])` bit 0 is clear. For each `0x1D0` record it maps the point `+0x1A0` (w = 1) through the bone that `+0xC` names on the owning render record (header `+8` indexes `022C6F28`; `00421D70`, `004220F0`). It counts `+0` up to 16 and rewrites the history rows `+0xA0`..`+0x19F` and `+0x10` (P7) |
| `0051CDE0` draw | `003E6680` ← `00425DC0`, the after-emission stage of the pass dispatcher `00332440` | gated on payload `+8` bit 0 and `+0x300 > 0` in the accessor. It runs while `+6` is set and bit 1 is clear. It submits at once, through `00540C70` (its only caller), the template `02AEC180` (0x15 units), then per record the template `02AEC2D0` (0x1E units) with the record's first `0x1A0` bytes spliced in at `+0x10`. The values are scaled by the render record's fade product `003E5770` (`+0x260 x +0x160 x +0x26C`), by record `+0x1C0` and by header `+0xC`. `00425DC0` first runs `0051D1D0`, which binds `02CA8430` / `02CA8438` (P8) |
| `0051DB60` on | `003E6710(rec, 1)` ← the promoter path `0041FCF0`, which passes 1, or command `0x1F`'s handler `00520140`, which passes word+2 AND 1 | `+6` = 1 and `+7` = 0 (one word store). Each record gets `+0` = 0, `+0x10` = 0, `+0x14` = 1.0, `+0x1C4` = 1, and its 0x100-byte history `+0xA0` is zeroed (P9) |
| `00519720` off | `003E6710(rec, 0)` | `+6` = 0 |
| `0051DBE0` LOD scale | `003E6D40` ← `0042CBF0` / `0042D050` (the child and root LOD updates) | header `+0xC` = render record `+0x49C` (P5) |
| `0051D2F0` hide / freeze | `003E6D40` ← `00421280` / `004213E0` | merges into header `+7`. `00421280` passes 4 or 6 (clears or sets bit 1, hide): it passes 4 when its argument is non-zero and `+0x284` bit 5 is set. `004213E0` passes 9 or 8 (sets or clears bit 0, freeze) on `+0x284` bit 24 (P5) |
| `0051D220` one-time init | the initialiser itself (`0041F5F6`) | builds the two resources `02CA8430` / `02CA8438` once (flag `02CA842C`) from the image block `01F2B340` (1 << 6 by 1 << 6), and sets `+6` = 0 (P9) |

**The copy itself (P1).** `0041F340` copies `0x10 + n x 0x1D0` bytes to the aux base plus `ebp` and keeps `ebp` at
record `+0x300` (0 when the section is absent, `0041F5FD`). It stores the record's own word `+0` (its index) at copy
`+8`.

**Census and controls.**
- P3: `add r32, dword ptr [reg + 0x300]` occurs 4 times in the image, all in the four accessors. Of the 55 callers of
  the aux-base getter `003AB7F0`, the only ones that touch `+0x300` are the four accessors and the initialiser, which is
  the writer and the control.
- P4: the accessors have exactly the eight call sites listed, and no rip reference names any of them.
- P6: `structflow` was run from each of the seven entries with the copy in `rcx` (stride `0x1D0`, depth 1). It found no
  escape and no indirect call. The one hand-off is the reset's memset of a record history (`0051DBB5` → `00861EC0`). It
  also found the header offsets the pins name: `0`, `2`, `6`, `7`, `8` and `0xC`.

**What this means for the file layout.** At run time, record `+0`, `+0x10`, `+0x14` and `+0xA0`..`+0x19F` hold the
engine's values, not the file's. The authored values that are read are:
- the bone selector `+0xC`;
- the point `+0x1A0`;
- the tail `+0x1B0`;
- `+0x1C0`;
- the remaining bytes of the first `0x1A0`, which the draw splices into the packet.

This overrides any reading of `+0x10`..`+0x4F` as a static transform at run time. That reading is SWE2-DATA's
2026-09-21 file decode, which stays a statement about the file.

**Not read here.** The packet program that `00540C70` hands the bytes to, and so what is drawn. The time-stop page and
the bone-trails page own the meanings of `+0x284` bit 24 and bit 5. Command `0x1F` is registered but authored by no
shipped motion (the `@FEF` census on the motion-entries page), so in shipped data the effect is switched on only by
promotion.

## 2. Can the registry's index reach −1 through the `0055CD40` copy? (G1-G9) (SWE2-STRUCT for OPUS)

**Answer: it can hold `0xFF` (static code does not exclude it), but the slot is never read at −1.**

**Where the byte comes from (G1-G5).** The view `0055CD40` is created only by `0055C690`, whose only caller is the
licence-screen owner `00561390` (its arm 0x10). At construction the view copies owner `+0x10C` bit 2 into `+0x570`
bit 10 and, under that bit, owner byte `+0x108` into `+0x558`. The owner takes `+0x108` from its creation parameter's
byte `+0x18`, and the bit from parameter `+8` bit 0. The owner has two creators:
- `00560910`, the screen, passes byte `0xFF` with the bit clear (`00560C90`).
- The board-picker panel `00558FB0` passes its `+0xDC` from its destroy arm, when its `+0xE0` bit 1 is set
  (`00559076`..`005590E3`).

The panel's `+0xDC` comes from two places:
- Its creation parameter: the screen passes `0xFF` with the bit clear (`00560C89`), or the owner's destroy arm passes
  the owner's own `+0x108` with bit 1 set when the owner's bit 2 is set (`00561460`..`005614A1`).
- The picker `00557DB0`, the panel's child. It answers `{0xC, 0x8002, value}` with its cursor (`+0x358`, which wraps
  between 0 and 11, and whose `0xFF` start value is normalised to 0) or with −1 on the no-board cancel. Its handler
  writes the panel's `+0xDC` and sets the bit only for a value other than `0xFF` (`005583BE`..`0055840F`).

The view sets owner bit 2 later, without rewriting `+0x108` (`0055D68C`, `0055F4CB`, when the character's board
selector is `0xFF`), and then destroys itself and the owner. That is `UQ-155`'s board-choice flow. G5 censuses every
non-stack store to `+0xDC`/`+0xE0`/`+0x108`/`+0x10C` in the licence-UI band: the panel's 7, the owner's 9, and 5 on
other objects. One of those 5 writes a dword 1, never `0xFF`.

So the copied value is the picker's choice, 0 to 11, in the normal flow. **No file feeds it, so there is no authored
range to census.** A `0xFF` would arrive under bit 10 only if the screen's `0xFF` owner had its bit 2 set by the view
and the panel were then torn down before the picker reported. The static reading does not exclude that sequence. It
would take the on-screen flow to settle it, and it does not matter, because of the guard below.

**Why −1 is never used (G6-G9).**
- G6: an image-wide census finds 33 stores in 23 functions that cover `+0x558`/`+0x559`. In the UI band they are
  exactly `0055B44B`, `0055B45C`, `0055B48A` and `0055CF80`. The control is the two known writers.
- G7: the copy at `0055CF80` reaches `0055B3F0` at `0055D105` with no call in between. The widget is zeroed at creation
  (`002465F0`'s memset), so `+0x128` is null and `0055B3F0` runs in full. Bit 10 skips only the lookup. The test
  `0055B451`..`0055B463` follows both paths and stores 0 into the count word `+0x559` when the index is `0xFF`. The
  rebuild `0055DBD0` frees `+0x128` first, so the guard runs again there.
- G8: the reader `0055BFF0` loads `[0x02EBF1A0 + 8 x idx]` (`0055C0A8`) only inside its `+0x559`-count loop.
- G9: so (index = −1) implies (count = 0) after every run, and nothing else writes either field.

**The correction.** `AG-4`'s 2026-09-18 answer called the byte "an authored record byte" and the copy "the one path on
which a `0xFF` in the data would make the reader dereference slot 50". Both are wrong. That sentence is struck in §7,
with the correction beside it (see [`consumer-check.md`](consumer-check.md)).

## 3. Who sends the map container `[02B47760]` message `0x20` (W1-W9) (SWE2-STRUCT for OPUS)

**Answer: the container's own relay child `002BA240` sends it, through the framework's bubble-up walker.**

**The framework (W1).**
- `00248220` appends a child: `+0x18` is the first child, `+0x20` the next sibling, `+0x10` the parent.
- `00244960` links a child only when it has no parent.
- `00275440(w, msg)` hands the message to every ancestor along `+0x10`. `002753F0(w, msg)` hands it to `w` and its
  whole subtree.
- Destroying a widget (`00245020`) sends the static `{18}` (`00915070`) to it, and `002473B0` sends it to every
  descendant.
- Activation (`00246AD0`) ends with the static `{14}` (`01E0C0E0`).

**The sequence.**
1. **W2.** At field setup, `003CB440` builds the container from the template `00D11770`, so its creation message is
   `{1, 0, 5}` and its mode `+0x179D8` is 5. The only store of the mode in the container procedure is `003CB6B6`. So for
   `[02B47760]` the mode-6 arms (`003BC160`, `002747B0`) never apply, and the `0x20` arm always takes the index from
   `003BFDF0`, the current field's sub-location.
2. **W5.** The same function opens a load group on the container: `00404060` loads into `+0x190` (the location-map
   loader, `Loca.mrp`). It also creates the loader widget `[02B457E0]` (`003BC450(0, 1, container)`), which keeps the
   container at `+0xC0`. When the group's last load completes (`002495C0`), or at close if nothing is pending
   (`00249410`), the container receives `{0x10, 0}`. When the loader first completes, it sends `{0x10, 0x100}`
   (`003BC71E`, through `003BC3E0`).
3. **W3.** The container's `0x10` arm sets `+0x179D2` bit 0 for code `0x100` and bit 1 for codes outside
   `0x100`..`0x102`. When both bits are set and the mode is not 6, it sends itself `0x22` (`003CB760`..`003CB785`). The
   `0x22` arm creates the 0xC0-byte relay `002BA240`, links it as its own child (`00244960` at `003CB7C7`) and activates
   it (`003CB7CF`).
4. **W4.** The relay's activation `{14}` arm opens a completion group, which delivers `{0x10}` to it straight away
   (`003C2100`, or the group's close `00249410`). Its `0x10` arm destroys it (`00245020`). On the resulting `{18}` it
   sends `{0x20, 0, 0}` through `00275440` (`002BA289`..`002BA29F`). The relay's parent is the container, so the
   container's `0x20` arm `003CB7DB` runs: it activates the container under the layer root `[0208EA28]` and creates the
   preload page with `{14, 0, index, 0}`.
5. **W9.** Bits 0 and 1 are never cleared in the container. The only other edits are the masked xors of bits 6 and
   4-5. So every later `{0x10}` notice, codes `0x101` and `0x102` included, repeats `0x22` → relay → `0x20` →
   re-activation and preload.

**Census (W6-W8).**
- W6: 9 calls in the image are handed a stack-built `0x20`. Only the relay's bubble (`002BA29F`) has `[02B47760]` on
  its path:
  - `002B6570` and `002BA040` message `[0209E5C0]` / `[0209E5F0]` directly. These are the track and location
    containers, which copy `[02B47760]+0x190` first.
  - `0027A633` broadcasts over the subtree of its own 0x61F0-byte widget (procedure `00279E20`).
  - `00553F40` bubbles from its own widget.
  - The other three are not widget calls.
- W6: the 14 static structs that begin with `0x20` and are passed in `rdx`/`r8` all go to non-widget calls.
- W7: the only link calls in the container's code, and in every function that names `[02B47760]`, are:
  - `003CB7C7`: the relay under the container;
  - `003CB7CF`: the relay activated;
  - `003CB7DE`: the container under the layer root;
  - `003CB821`: the preload page under the container.

  The page bubbles only `{0x2C}`. The layer roots (procedure `002445D0`) handle only id 1. So before its first `0x20`
  the container has no parent, and afterwards its only ancestor is a root that forwards nothing.
- W8 (control): the same census for id 14 reproduces `ms4_check` M5's two sends.

**Limits.**
- The census sees stack-built and static messages handed to calls in the kit's function extents. A message forwarded
  by a procedure that receives it would have to start from one of these senders, and W6 lists all of them.
- The relay's `0x10` arrives inside its own activation, so the whole chain from the container's `0x22` to the preload
  page runs synchronously in one message delivery. That is read from the code, not observed.

## Proposed status lines and row text (SWE2-STRUCT for OPUS; status words and register rows stay their owners')

- **fcp-character-parameter-block.md:** batch 12's proposed line, with its last clause replaced:
  `… the one-slot-behind default table (UQ-219) and the section-1 pairs (UQ-221) answered 2026-09-18; the readers of the section-8 runtime copy answered 2026-09-30 (swe2struct-residue3-0930 P1-P9: a per-frame update, a draw, on/off, a LOD scale and a hide/freeze merge, reached only through the four +0x300 accessors)`.
  With that, the page has no open prose residue. Batch 12's id-less row P1 can be registered directly as ANSWERED.
  Pipe-free text for SWE2-DATA:

  > **P1 (new row), ANSWERED 2026-09-30 (SWE2-STRUCT for OPUS, swe2struct-residue3-0930, residue3_check.py FAILS 0):**
  > who reads the runtime copy of FCP section 8 (offset at render record +0x300). Six routines, reached only through the
  > accessors 003E6680, 003E66D0, 003E6710 and 003E6D40, read it:
  > - 0051D310, the per-frame update, maps each record's point +0x1A0 through bone +0xC and keeps a 16-row history;
  > - 0051CDE0, the draw, submits the records as immediate packets through 00540C70, scaled by the render record's fade;
  > - 0051DB60 and 00519720 switch it on and off, on at promotion;
  > - 0051DBE0 stores the LOD scale +0x49C;
  > - 0051D2F0 merges the hide and freeze bits from 00421280 and 004213E0.
  >
  > No reader keeps or passes the copy on.

- **authored-data-table-registry.md:** batch 12's proposed line plus:
  `…; the AG-4 remainder (the byte 0055CD40 copies into +0x558) answered 2026-09-30 (never read at −1: the board-choice byte is UI state, and 0055B3F0's 0xFF guard covers the copy path; swe2struct-residue3-0930 G1-G9)`.
  For SWE2-DATA, the `AG-4` row in OPEN-QUESTIONS.md carries the struck sentence verbatim. Pipe-free replacement text:

  > ~~0055CD40 copies an authored record byte +0x108 into +0x558 under +0x570 bit 10 (0055CF73..0055CF80) without
  > touching the counts: that is the one path on which a 0xFF in the data would make the reader dereference slot 50, and
  > its data range is not checked here.~~ **Corrected 2026-09-30 (SWE2-STRUCT for OPUS, swe2struct-residue3-0930
  > G1-G9):** the byte is the licence owner's board-choice byte, not authored data. 0055B3F0 runs straight after the copy
  > (0055D105), and its 0xFF test (0055B451..0055B463) zeroes the count +0x559 on the copy path too. So slot 50 is read
  > on no path.

- **MS-4 (the map-screens page is not edited here).** Pipe-free row text for SWE2-DATA, replacing the narrowed
  wording's "Still open":

  > **ANSWERED 2026-09-30 (SWE2-STRUCT for OPUS, record swe2struct-residue3-0930, residue3_check.py W1-W9 FAILS 0):**
  > the container's message 0x20 is sent by its own relay child 002BA240. The container creates and parents the relay in
  > its 0x22 arm (003CB7AA..003CB7CF), and sends itself 0x22 once both load notices have arrived: its own load group's
  > completion and the loader 02B457E0's code 0x100. The relay retires at once, and on its destroy notice (18) it sends
  > {0x20, 0, 0} to its ancestors through 00275440. The container is the first of them. The container's mode is 5 (its
  > creation message from 00D11770), so the index is always 003BFDF0's, the current field's sub-location. The sequence
  > repeats on every later 0x10 notice. No other 0x20 sender reaches the container: 9 stack-built and 14 static
  > candidates were censused, with the id-14 census as control.

  Suggested page note for the map-screens page §2.6 / §7, for whoever holds it: the same text, plus "in play: when the
  field's map data and the loader have both finished loading, the container switches itself on and preloads the map
  of the sub-location you are in".

## Limits (SWE2-STRUCT for OPUS)

- **Static only.** Nothing was observed in a running game. In item 2, whether a `0xFF` ever reaches the copy under bit
  10 depends on the on-screen order of the licence screens, and it is not settled here. The answer does not depend on
  it.
- **The 32-bit pointer.** The section-8 accessors form the copy pointer in 32 bits (`add eax, [rbx+0x300]`,
  `mov ecx, eax`), as the initialiser does (`movsxd rdi, eax`). This is the same sub-2 GiB-arena assumption as BW-2.
- **The tools' blind spots.**
  - `structflow` does not follow indirect calls (none carried the copy), code outside the function extents, or taint
    through memory other than the stack.
  - The G5/G6 bands are address ranges, and the attribution of the out-of-band stores to other objects is by
    function, not by a dataflow proof. Only the in-band stores bear on the answer.
- **The `0x1D0` record layout.** Bytes that only the packet splices in are not given meanings here.

## Receipts (SWE2-STRUCT for OPUS)

| script | result |
|---|---|
| [`residue3_check.py`](residue3_check.py) ([`residue3_check.out`](residue3_check.out)) | P1-P9, G1-G9, W1-W9: **27 PASS, FAILS 0** (run: residue3_check.py at 4760745aa, re-run by OPUS) |
| `documented_rule.py` ([`documented_rule.out`](documented_rule.out)) | `TALLY NEEDS-POINTER=2 of 2`, FAILS 0. The status lines are not edited, so the disposed-row pointers are still missing: UQ-217 on the FCP page and UQ-80 on the registry page, as in batch 12 |
| [`consumer-check.md`](consumer-check.md) | the one strike, on the registry page only; the `AG-4` register row disagrees and is routed with the text above |

Inputs: the certified image `73461d08…`, the kit's `retool.py` (its v4 extents and the reference cache) and
`structflow.py`. No archive data was needed: none of the three answers rests on file contents.
