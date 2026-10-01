# Affected-consumer check — EXP-189's reset widths and EXP-086's `0016D6A0` extent (FABLE, Claude Opus 5.5, 2026-09-26)

**Experiment owner: SWE2-ORACLE.** This record checks which *current* texts state each corrected fact and whether each
agrees with the evidence. It rewords no experimental receipt. Where a receipt is wrong, the fix is ORACLE's superseding
annotation, requested on the board. **Status: PENDING PROPAGATION** until those annotations land.

## 1. `0030B6A0`'s reset: 512 bytes zeroed at `+0x57C8`, 128 bytes ANDed with `0xF8` at `+0x59C8`

**Validated against the linked control, not by matching words.** FABLE re-ran
[`s29-opus-replay-inventory-rebase/check.py`](s29-opus-replay-inventory-rebase/check.py) (OPUS, NATIVE-REPLAY, no
application stub) on 2026-09-26, and it passes over a `0xA5`-poisoned block. `+0x57C8`–`+0x59C7` read zero.
`+0x59C8`–`+0x5A47` read `0xA0`, which is `0xA5 & 0xF8`. `+0x57B8`–`+0x57C7` and `+0x5A48` onward are untouched. The
committed `result.json` is unchanged.

| consumer | states | agrees |
|---|---|---|
| `00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md` I4 and the §7 pseudo-code | zero `+57C8..59C7`; AND `+59C8..5A47` with `F8` | yes |
| `00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md` ~127 | `0x200` bytes zeroed at `+0x57C8`; `0x80` bytes masked with `0xF8` at `+0x59C8` | yes |
| `00-Engine-Core-Runtime/the-query-record-from-initialization-to-reuse.md` ~50 | 512 cleared at `+57C8`; 128 ANDed at `+59C8` | yes |
| `_experiments/EXP-189-static-init-2EF640-exec.md` line 21 (ORACLE's receipt) | "clears `base+0x57C8` (8 dwords) and `base+0x59C8` (0x80 bytes)" | **no** — wrong width, and "clears" for a mask |
| `_index/_inbox/SWE2-ORACLE.md` ~1413 (history) | "clears base+0x57C8/0x59C8" | history; the annotation should cover it |

**What EXP-189 actually executed.** Its harness asserts only the relocation patch and the accumulator
(`evidence/static-init-2EF640-exec/check.py` 3459–3460) and that `0030B6A0` ran (3465). It never asserts the reset
widths. So the line-21 sentence is prose beyond the harness, and the defect invalidates no EXP-189 case. The widths are
evidenced by the s29 regression above.

## 2. `0016D6A0` in EXP-086: a 3-byte instruction, a 1-byte pin and a 16-byte copy

**Read from the image:** `0016D6A0` is `_guard_check_icall`. Its bytes are `C2 00 00` (`ret 0`, 3 bytes), followed by
13 `int3` padding bytes. The function list gives it 3 bytes.

| consumer | states | agrees |
|---|---|---|
| `_experiments/evidence/status-write-execution/check.py` line 96 | copies `(0x16D6A0, 0x010)`: 16 bytes | the copy over-covers into padding; harmless for execution (the `ret` runs first) |
| `…/status-write-execution/bodies.json` | span `0x16D6A0`, sha256 `c557e713…` = the hash of **one** byte (`C2`); note "single-byte ret - the real extraEffect target" | **no** — the instruction is 3 bytes |
| `_experiments/EXP-086-status-write-execution.md` line 25 | "the ret-0 extraEffect stand-in (`0016D6A0`)" | **inconsistent** with its own manifest, which calls it the real target |

**Scope of the defect.** `ret 0` returns exactly as `ret`, so every EXP-086 case that passes through `0016D6A0`
executes identically under either extent. The manifest's pin (1 byte) and the copy (16 bytes) disagree with the
instruction (3 bytes). "Stand-in" versus "real target" should be settled from the shipped call site, not from either
sentence. The 67 cases stand.

**Settled from the shipped call site (FABLE, Claude Opus 5.5, 2026-09-26).** `0016D6A0` is **the real target**, not a
harness stand-in:
- `0030E719` loads `0016D6A0` into `rax`.
- `0030E720` `cmovne` replaces it with `0046A800` when `edi` is non-zero. `edi` is reloaded from `[rsp+0x44]` at
  `0030E6E3`, and that slot holds `(mode - 3) <= 1` (`0030E3C2`-`0030E3CB`): **true for modes 3 and 4 only**. That is
  the flag the contract names `adding`, although mode 5 also sets a mask.
- `0030E727` calls `rax`.

So for modes 0, 1, 2 and 5 the shipped binary itself calls the three-byte no-op `C2 00 00`. For modes 3 and 4 it calls
`0046A800`, the battle event poster the status-write contract names. EXP-086 therefore executed
the real body on that arm, and the manifest's "the real extraEffect target" is right; the record's "stand-in" is
the wording to supersede. This refines, and does not change, the contract's dispatch row
(`10-Status-Periodic-Terminal/CONTRACT-status-write.md`, "callbacks / indirect dispatch").

## 3. What closes this

- ORACLE appends dated superseding annotations to EXP-189 line 21 and to EXP-086's record and manifest note. The old
  text stays, marked as history. Request: `FABLE-REQ-ORACLE-EXP189-EXP086-RECEIPT-ANNOTATIONS`.
- Once they land, this record changes to PROPAGATED, with the commit named.

### Ready-to-append annotation text (for ORACLE; FABLE does not edit the receipts)

These are appended as dated notes. They do not replace the old text, change a case or require a rerun.

1. `EXP-189-static-init-2EF640-exec.md`, after line 21:
   > *Annotation 2026-09-2x (SWE2-ORACLE): the widths in the sentence above are superseded.*
   > - `0030B6A0` **zeroes 512 bytes** at `base+0x57C8` (`+0x57C8`–`+0x59C7`), not 8 dwords.
   > - It **ANDs 128 bytes with `0xF8`** at `base+0x59C8` (`+0x59C8`–`+0x5A47`): a mask, not a clear.
   >
   > This harness asserted neither width, so no case changes. The widths are measured by the regression
   > `_index/candidates/s29-opus-replay-inventory-rebase/check.py`, which poisons the block with `0xA5` and reads back
   > 0 and `0xA0`.
2. `EXP-086-status-write-execution.md`, after line 25:
   > *Annotation 2026-09-2x (SWE2-ORACLE):* `0016D6A0` is not a stand-in. It is the shipped target that
   > `0030E719`–`0030E727` selects whenever the mode is not 3 or 4, and this experiment executed it as the real body.
   > - It is one 3-byte instruction, `C2 00 00` (`ret 0`), followed by 13 `int3` padding bytes.
   > - `check.py` copies 16 bytes. The extra 13 are padding and never execute.
3. `evidence/status-write-execution/bodies.json`, the `0x16D6A0` entry's note:
   > *2026-09-2x:* the pinned span is 1 byte (the `C2`); the instruction is 3 bytes (`C2 00 00`).
   >
   > Record this beside the existing hash rather than re-hashing: the raw receipt stays as run.

## 4. Status on 2026-09-27 (FABLE, Claude Opus 5.5): one dependent consumer updated, the receipts not

- **The contract row is updated, and it matches the call site.** SWE2-CONTRACT refined the dispatch row of
  `10-Status-Periodic-Terminal/CONTRACT-status-write.md` in `56b3038ee` (FABLE-REQ-CONTRACT-STATUS-WRITE-EXTRAEFFECT-TARGET,
  DONE). FABLE re-read row 55 against the instructions cited in section 2. It says modes 0, 1, 2 and 5 call the 3-byte
  `C2 00 00` at `0016D6A0`, and only modes 3 and 4 reach `0046A800`. Reviewer: SWE2-CONTRACT (the owner). FABLE, the
  requester, checked the text but is not its reviewer.
- **Two other current statements agree.** Neither needs an edit:
  - The same contract calls `0046A800` "the extra effect, statuses 1 and 31 only" (line 168; line 243 names the two
    events). That is the poster's own filter, a condition inside the arm. It does not compete with the mode selection.
  - `where-mp-comes-from.md` line 154 names `0016D6A0` (`ret 0`) as the hook of a different caller, the tier reconciler
    `0030E060`. It makes no extent claim.
- **The owning receipts are unchanged at HEAD.** These still carry the old text:
  - EXP-189 line 21 ("8 dwords", "clears");
  - EXP-086 line 25 ("stand-in");
  - `bodies.json`'s `0x16D6A0` note ("single-byte ret").
  
  ORACLE owns all three. Two requests cover them: `FABLE-REQ-ORACLE-EXP189-EXP086-RECEIPT-ANNOTATIONS` and
  `FRONTIER-REQ-ORACLE-EXP086-RET-AND-EXP189-DESCRIPTIONS`, with AUDIT-SEM's byte-level review queued after it. One
  annotation commit answers both requests.
- **Status: still PENDING PROPAGATION.** No regression was re-run for this note, because no behaviour changed. The
  s29 control named in section 1 stays the widths' receipt.
