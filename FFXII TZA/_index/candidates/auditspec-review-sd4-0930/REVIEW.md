# SWE2-AUDIT-SPEC review of SD-4 (sd4-unit-flag-bit24-0930 at 35db7fbb2): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Author: OPUS.
Reviewed: commit `35db7fbb2`, record [`sd4-unit-flag-bit24-0930`](../sd4-unit-flag-bit24-0930/README.md). Static.
Request: `OPUS-REQ-AUDITSPEC-SD4-0930`.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD4-0930 | sd4-unit-flag-bit24-0930 | `35db7fbb2` | ACCEPT-WITH-NARROWING |

**Re-run.** `sd4_bit24.py` re-run from its own directory ([`rerun_sd4_bit24.out`](rerun_sd4_bit24.out)). Identical to
the committed `.out` (ignoring CR): T1-T6 and R1 PASS, `FAILS 0`. No tracked file changed.

**Re-derived independently.** [`bitsweep.py`](bitsweep.py) `0 24` gives [`sweep_d0_b24.out`](sweep_d0_b24.out). It is my
own sweep, sharing no code with the record's. It covers every listed function plus every unlisted `.pdata` range
(38,175 ranges). It finds every instruction that can set or clear bit 24 of the dword at `[base+0]` in the shapes the
record's scan excludes:
- **byte / word widths** at `+1..+3` (for example `or byte [reg+3], 1`);
- **`bts` / `btr` / `btc`**;
- **register read-modify-write stores** (`or/and/bts/btr reg`, then `mov [reg], reg`).

The result is 150 hits (47 memory-form, 47 memory-form with an unresolved register, 56 register-store).
- **The memory-form battle sites match the record exactly.** These are `00227680` ×7, `00301140`, `00307300`,
  `00307C70` ×2, `003083A0`, `003105D0`, `00313400`, `00313480`, `00313500` and `003250F0`, plus `002D8050` and
  `00760700` as the record lists them. No other function in `0022xxxx`-`0033xxxx` has a memory-form set or clear
  of bit 24.
- **Shapes the record's scan cannot see, all in functions it already flags or in unidentified objects:**
  - `00227680` has two more *register-built* sets. At `00227BB4`-`00227BD7`, `movabs rcx, 0xffffffeffdffffff` /
    `and r8, rcx` / `or r8, 0x9000000` / `mov [rdx], r8` clears bits 25 and 36 and sets 24 and 27, on both objects
    (`00227BC8`, `00227BD7`). It also has two variable-mask read-modify-writes, `0022788C` `or [rbx], rax` and
    `002279F7` `and [rdx], rax`, whose masks are not resolved here.
  - Byte-width writes at `+3` bit 0: `003DE710` (`003DE75A` set), `003EDAD0` (`003EDB87` clear / `003EDBB3` set),
    `00517650` (`00517DD9` set / `00517F26` clear), and `00346C00` (`00346CE8`, `and byte [rbx+3], 0xc0`, clears
    bits 24-29). These functions are unnamed. Their objects are not identified, and nothing here shows them to be
    battle units.
  - The other variable-mask ORs in the battle range resolve to other bits or objects. `00306E60` is a spawn-group lane
    mask (`1 << cl` into a rip table); `0030CBE0` ORs bit 31 (`r14d`, set at `0030CC06`).
- **Reader R1** (`0023B12B`-`0023B14F`) was read in the record's own control. I did not re-derive it.

**Controls.** T1-T6 are known-answer checks on the record's own sites. They fail if a listed site moves, but they are
**not sensitive to completeness**: a set in an unscanned shape passes them. The record states that limit ("covers the
`or` / `and` / `bts` / `btr` shapes on `[reg]`"). Its `bts` / `btr` branch is live (`src in ("0x18", "24")`). The sweep
above is the completeness control the record lacks. It confirms that the five transitions and the clear sites are the
complete memory-form set for the battle-unit functions, and it adds the candidates listed.

**Why narrowing.** The answer (five transitions set it, the reaction-animation event, `00307C70` and cancel clear it,
the recompute inhibits) holds. The "whole-image scan" wording, and the field-map correction built on it, overstate the
scan's reach: `00227680`'s site list is incomplete, and byte-width writers exist that the scan cannot see.

**Correction wording for the row owner (SWE2-DATA)**, to append to SD-4's answer and to the field-map correction:
> *Scope (SWE2-AUDIT-SPEC review, 2026-09-30):* the writer scan covers dword/qword memory-destination `or`/`and`/`bts`/`btr` on `[reg]`. An independent sweep of byte-width, `bts`-family and register read-modify-write forms (`auditspec-review-sd4-0930`) adds no battle-unit transition. It finds that `00227680` also sets bit 24 with bit 27 through a register (`00227BC8`, `00227BD7`, clearing 25 and 36) and has two unresolved variable-mask writes (`0022788C`, `002279F7`). It also finds byte-width writers of bit 24 at `+3` in `003DE710`, `003EDAD0`, `00517650` and `00346C00`, whose objects are not identified.
