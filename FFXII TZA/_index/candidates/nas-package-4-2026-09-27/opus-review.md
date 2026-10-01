# OPUS review of FABLE-REQ-OPUS-REVIEW-NAS-PACKAGE-4 (FJ-3), 2026-09-27.

Reviewer: OPUS (not the author). Author: FABLE. Package: `_index/candidates/nas-package-4-2026-09-27/README.md`
(published at 8cb2a0393).

**Re-run.** `fj3_name_blank.py`: B1, B2 PASS, FAILS 0.

**The builder, re-read whole (OPUS).** I read `00329220`..`003299AC` to its `ret`. B1 and B2 stand, with two
precisions:
- The entry `memset(out, 0, 0xC0)` (`00329248`) is the only callee that receives the record pointer, so B1's three
  direct stores are the complete write set of `+0x10`.
- "Unit-owned" means that the pool scan found a unit whose `+0x698` is this stats row (`rsi != 0`), and `003298AD` runs
  on every such path. The text-bank name is written only for a kind-0 stats row (`[stats+5] == 0`). So the name
  survives only in a kind-0 record that no unit owns. The wrappers `0031FEC0` / `0031FF70` pass `stats = actor+0x698`,
  so their records are always unit-owned.

**Independent consumer census (OPUS).** Control `opus_fj3_consumers.py`, 5 checks, FAILS 0 (C5 is a positive control).
The package rests on the 2026-09-11 answer that no consumer takes a unit's name from this record. The same page still
lists "which UI caller draws which field" as open (UQ-98), so I rebuilt the census from the executable rather than
cite it.
- **C1 — caller set.** The builder is entered only through the four wrappers' tail-jumps. The wrappers are called only
  from the ten named callers (rel32 scan of every executable byte), and no absolute pointer to any of the five exists.
- **C2 — builder data.** Its only non-`.bss` references are `00915A08` (400.0f) and `01CEB638` (""). This confirms
  the package's "no other string".
- **C3 — frame-buffer consumers.** Seven consumers keep the record in a stack buffer: `00253C70`, `00254560`,
  `00273270`, `00273880`, `003C3340`, and the pass-through callers `0027DE30` and `003FFF70`. After the call none of
  them touches the name bytes. The fields they do read are `+0x00`, `+0x04`, `+0x08`, `+0x60` and `+0xAC`.
- **C4 — every place a record persists.** No path dereferences `+0x10..+0x17`:
  - `00283270` builds nine records into the menu block at `[0209AC30]+0x408` (stride 0xC0), with a sorted pointer
    table at `+0xAC8`. The census covers every table load in the 456 functions that reference the block, with callees
    followed.
  - `0035BC50` builds four battle records at `022C8080`, with the current one at `022C8078`. All 24 call sites of the
    getters `0035BAF0` / `0035BB20` / `002734B0` are covered.
  - `002BFD20` / `002C0870` embed the record in a panel object at `+0xC0`. The covered paths are `002C0400` and the
    two task handlers `0029B7D0` / `0029B810`, which `00296360` registers with the record as context (they read
    `+0x24`, `+0x2C`, `+0x30` and `+0x87`, the bar values).
  - The panel resolves the text it shows itself, through `002B58B0` on `[obj+0x2B0]+0x18`. The menu's `0027F210`
    resolves names from the record's `+0x98..+0xAC` words. Neither uses `+0x10`.
- **C5 — positive control.** The same engine and seeds, asked for `+0x60` / `+0x24`, find the known reads
  (`00254091`, `00272EA4`, `0029B7E4`; 42 in all). C4's silence therefore does not come from a blind engine.

**This census proves more than the package claims.** No consumer reads `+0x10` for any record, whether or not a unit
owns it. In the shipped executable the field is write-only. The blank is therefore unobservable twice over: its only
effect is a value nobody reads. **Limit:** this is a static census over the enumerated delivery paths. A linear taint
does not follow register spills or `memcpy` copies of a record, and no copy was seen.

**Verdict:**
1. **The residue is of the intent kind, and the mechanism discharges it.** The write set is complete (three direct
   stores plus the entry memset), and the builder carries no string, assert or log call. My census shows the field
   has no reader for any record. What remains is the programmer's reason, which no shipped artefact records.
   **SIGNED.** One condition: the NAS text should state the stronger consumer result, since it is what makes the
   residue unobservable. Suggested wording: "`+0x10` has no reader in the shipped executable for any record (OPUS
   census `opus_fj3_consumers.py`, C1–C5)."

   Status text on signing: `NO ADMISSIBLE SOURCE (FABLE 2026-09-27, EVIDENCE-STANDARD 2026-09-15bk) - the complete
   write set and a zero-reader consumer census; the intent - REVIEWED AND SIGNED 2026-09-27 (OPUS, reviewer; FABLE,
   author)`.
2. **Follow-on for FABLE (not a condition).** The census also closes part of UQ-98. For each caller it now names which
   record fields that caller reads (C3 / C4 above). It does not name which caller draws which field on screen. FABLE,
   as the page's editor, may carry that narrowing.

Run receipt: `opus_fj3_consumers.py` and `fj3_name_blank.py` executed at f4550a7d2 (HEAD at review time) against the
certified EXE `Tools/work/exe/FFXII_TZA.exe` (sha256 73461d08…21f8).
